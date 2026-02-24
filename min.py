import geopandas as gpd

# Đọc GeoJSON
gdf = gpd.read_file("/home/chungtv8/Downloads/BieuDo/DiaPhan_CapXa_2025.geojson")

# Simplify geometry
# 0.001 độ ≈ ~100m (rất hợp cho bản đồ cấp tỉnh)
gdf["geometry"] = gdf["geometry"].simplify(
    tolerance=0.001,
    preserve_topology=True
)

# Ghi ra GeoJSON mới (giữ nguyên tất cả field)
gdf.to_file(
    "output_2.geojson",
    driver="GeoJSON"
)
