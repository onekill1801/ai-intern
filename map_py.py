import geopandas as gpd
import json

# Simplify
gdf = gpd.read_file("/home/chungtv8/Downloads/BieuDo/DiaPhan_CapTinh_2025.geojson")
gdf["geometry"] = gdf["geometry"].simplify(
    tolerance=0.001,
    preserve_topology=True
)

# Ghi tạm
temp_file = "temp.geojson"
gdf.to_file(temp_file, driver="GeoJSON")

# Round tọa độ
with open(temp_file, "r", encoding="utf-8") as f:
    data = json.load(f)

def round_coords(coords, precision=5):
    if isinstance(coords[0], (float, int)):
        return [round(coords[0], precision), round(coords[1], precision)]
    return [round_coords(c, precision) for c in coords]

for feature in data["features"]:
    feature["geometry"]["coordinates"] = round_coords(
        feature["geometry"]["coordinates"],
        precision=5
    )

with open("output.geojson", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
