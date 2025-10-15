import json
from collections import Counter

# === 1️⃣ Đọc dữ liệu từ file JSON ===
input_file = "data.json"  # đổi tên file nếu cần

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# === 2️⃣ Thu thập tất cả các giá trị keyNameIn ===
key_names = [item["keyNameIn"] for item in data if "keyNameIn" in item and item["keyNameIn"]]

# === 3️⃣ Đếm số lần xuất hiện của từng keyNameIn ===
counter = Counter(key_names)

# === 4️⃣ Lọc ra những giá trị trùng (xuất hiện > 1 lần) ===
duplicates = {k: v for k, v in counter.items() if v > 1}

# === 5️⃣ In kết quả ===
if duplicates:
    print("🔁 Các keyNameIn bị trùng:")
    for key, count in duplicates.items():
        print(f"- {key} (xuất hiện {count} lần)")
else:
    print("✅ Không có keyNameIn nào bị trùng.")
