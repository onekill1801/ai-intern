import pandas as pd

# Đọc dữ liệu
df = pd.read_csv("scores.csv")

# Tính điểm trung bình từng học sinh
df["Average"] = df[["Math", "Physics", "Chemistry"]].mean(axis=1)

# Học sinh có điểm Toán cao nhất
top_math = df.loc[df["Math"].idxmax()]

# Xuất kết quả ra file mới
df.to_csv("scores_with_avg.csv", index=False)

print("=== DỮ LIỆU SAU KHI TÍNH ĐIỂM TRUNG BÌNH ===")
print(df)
print("\nHọc sinh có điểm Toán cao nhất:")
print(top_math)
