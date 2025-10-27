from collections import Counter

# === 1️⃣ Đường dẫn file ===
file_path = "input.log"   # đổi tên file của bạn ở đây

# === 2️⃣ Đọc toàn bộ danh sách ID ===
with open(file_path, "r", encoding="utf-8") as f:
    ids = [line.strip() for line in f if line.strip()]

# === 3️⃣ Đếm số lần xuất hiện của từng ID ===
counter = Counter(ids)

# === 4️⃣ Lọc ra các ID bị trùng (xuất hiện > 1 lần) ===
duplicates = {k: v for k, v in counter.items() if v > 1}

# === 5️⃣ Xuất kết quả ===
if duplicates:
    print("🔁 Các ID bị trùng trong file:")
    for _id, count in duplicates.items():
        print(f"- {_id} (xuất hiện {count} lần)")
else:
    print("✅ Không có ID nào bị trùng.")
