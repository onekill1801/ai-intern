import json
import geopandas as gpd
import unicodedata
from shapely.geometry import shape
from shapely.validation import make_valid

# ===============================
# 1. Chuẩn hóa tên tỉnh
# ===============================
def normalize_name(name: str) -> str:
    if name is None:
        return ""

    name = name.lower()
    name = name.replace("tỉnh ", "")
    name = name.replace("thành phố ", "")

    name = unicodedata.normalize("NFD", name)
    name = "".join(c for c in name if unicodedata.category(c) != "Mn")

    return name.strip()


# ===============================
# 2. Fix ring chưa đóng
# ===============================
def close_ring(coords):
    if coords[0] != coords[-1]:
        coords.append(coords[0])
    return coords


def fix_coordinates(coords):
    if isinstance(coords[0][0], (float, int)):
        return close_ring(coords)
    return [fix_coordinates(c) for c in coords]


# ===============================
# 3. Load GeoJSON + fix geometry
# ===============================
def load_geojson_fixed(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for feature in data["features"]:
        geom = feature["geometry"]
        geom["coordinates"] = fix_coordinates(geom["coordinates"])

        # Convert sang shapely & fix invalid
        fixed_geom = make_valid(shape(geom))
        feature["geometry"] = json.loads(
            json.dumps(fixed_geom.__geo_interface__)
        )

    return gpd.GeoDataFrame.from_features(
        data["features"],
        crs="EPSG:4326"
    )


# ===============================
# 4. Load 2 file (AN TOÀN)
# ===============================

file1_path = "/home/chungtv8/Downloads/BieuDo/DiaPhan_CapTinh_2025.geojson"  # geometry nhẹ
file2_path = "/home/chungtv8/Downloads/BieuDo/vietnam.geojson"       

gdf_geom = gpd.read_file(file1_path)   # geometry chuẩn
gdf_prop = load_geojson_fixed(file2_path)      # properties chuẩn (đã fix)


# ===============================
# 5. Map theo tên tỉnh
# ===============================
gdf_geom["key"] = gdf_geom["tenTinh"].apply(normalize_name)
gdf_prop["key"] = gdf_prop["NAME_1"].apply(normalize_name)

gdf_geom = gdf_geom.set_index("key")
gdf_prop = gdf_prop.set_index("key")

# ===============================
# 6. Check thiếu tỉnh
# ===============================
missing = set(gdf_prop.index) - set(gdf_geom.index)
if missing:
    print("❌ Thiếu geometry cho:")
    for m in missing:
        print(" -", m)
    raise ValueError("Tên tỉnh không khớp")
else:
    print("✅ Tất cả tỉnh đã khớp")

# ===============================
# 7. Replace geometry
# ===============================
gdf_prop["geometry"] = gdf_prop.index.map(
    lambda k: gdf_geom.loc[k, "geometry"]
)

# ===============================
# 8. Xuất file
# ===============================
gdf_prop = gdf_prop.reset_index(drop=True)

gdf_prop.to_file(
    "output.geojson",
    driver="GeoJSON",
    encoding="utf-8"
)

print("🎉 DONE: output.geojson")
