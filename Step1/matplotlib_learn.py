import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu sau khi đã xử lý
# df = pd.read_csv("scores_with_avg.csv")

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

# Vẽ biểu đồ cột so sánh điểm trung bình
plt.bar(df["Name"], df["Average"])
plt.title("Điểm trung bình của học sinh")
plt.xlabel("Tên học sinh")
plt.ylabel("Điểm trung bình")

plt.savefig("charts_1.png")

# Vẽ biểu đồ hộp (boxplot) phân bố điểm
df[["Math", "Physics", "Chemistry"]].plot(kind="box")
plt.title("Phân bố điểm theo môn học")

plt.savefig("charts_2.png")
