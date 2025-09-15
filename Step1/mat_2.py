import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")  

# Dữ liệu mảng (list of dict)
data = [
    {"Name": "An",    "Math": 8, "Physics": 7, "Chemistry": 6, "Average": (8+7+6)/3},
    {"Name": "Binh",  "Math": 9, "Physics": 6, "Chemistry": 7, "Average": (9+6+7)/3},
    {"Name": "Cuong", "Math": 5, "Physics": 8, "Chemistry": 6, "Average": (5+8+6)/3},
    {"Name": "Dung",  "Math": 7, "Physics": 9, "Chemistry": 8, "Average": (7+9+8)/3},
    {"Name": "Hoa",   "Math": 6, "Physics": 5, "Chemistry": 9, "Average": (6+5+9)/3},
]

# Tạo DataFrame từ dữ liệu mảng
df = pd.DataFrame(data)

# Tạo figure với 2 subplot (1 hàng, 2 cột)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Biểu đồ cột: điểm trung bình
axes[0].bar(df["Name"], df["Average"], color="skyblue")
axes[0].set_title("Điểm trung bình của học sinh")
axes[0].set_xlabel("Tên học sinh")
axes[0].set_ylabel("Điểm trung bình")

# Biểu đồ hộp: phân bố điểm theo môn
df[["Math", "Physics", "Chemistry"]].plot(
    kind="box", ax=axes[1], color="blue", patch_artist=True
)
axes[1].set_title("Phân bố điểm theo môn học")

# Hiển thị cả 2 biểu đồ cùng lúc
plt.tight_layout()
# plt.savefig("charts.png")
plt.show()
