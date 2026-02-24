import geopandas as gpd
import unicodedata

# ===============================
# 1. Hàm chuẩn hóa tên tỉnh
# ===============================
def normalize_name(name: str) -> str:
    """
    Chuẩn hóa tên tỉnh:
    - bỏ dấu
    - lowercase
    - bỏ 'tỉnh', 'thành phố'
    - strip space
    """
    if name is None:
        return ""

    name = name.lower()
    name = name.replace("tỉnh ", "")
    name = name.replace("thành phố ", "")

    # Bỏ dấu tiếng Việt
    name = unicodedata.normalize("NFD", name)
    name = "".join(c for c in name if unicodedata.category(c) != "Mn")

    return name.strip()


# ===============================
# 2. Đọc 2 file GeoJSON
# ===============================
file1_path = "/home/chungtv8/Downloads/BieuDo/DiaPhan_CapTinh_2025.geojson"  # geometry nhẹ
file2_path = "/home/chungtv8/Downloads/BieuDo/vietnam.geojson"          # properties chuẩn

gdf_geom = gpd.read_file(file1_path)
gdf_prop = gpd.read_file(file2_path)


# ===============================
# 3. Tạo key để map
# ===============================
gdf_geom["key"] = gdf_geom["tenTinh"].apply(normalize_name)
gdf_prop["key"] = gdf_prop["NAME_1"].apply(normalize_name)

gdf_geom = gdf_geom.set_index("key")
gdf_prop = gdf_prop.set_index("key")


# ===============================
# 4. Kiểm tra tỉnh bị thiếu
# ===============================
missing = set(gdf_prop.index) - set(gdf_geom.index)
if missing:
    print("⚠️ Các tỉnh KHÔNG tìm thấy geometry:")
    for m in missing:
        print(" -", m)
    raise ValueError("Dữ liệu không khớp, cần kiểm tra lại tên tỉnh")
else:
    print("✅ Tất cả tỉnh đều khớp geometry")


# ===============================
# 5. Replace geometry
# ===============================
gdf_prop["geometry"] = gdf_prop.index.map(
    lambda k: gdf_geom.loc[k, "geometry"]
)


# ===============================
# 6. Reset index & xuất file
# ===============================
gdf_prop = gdf_prop.reset_index(drop=True)

output_path = "output.geojson"
gdf_prop.to_file(
    output_path,
    driver="GeoJSON",
    encoding="utf-8"
)

print(f"🎉 Hoàn tất! File xuất ra: {output_path}")
