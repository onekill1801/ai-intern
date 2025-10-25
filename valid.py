from collections import Counter

# ===== Đọc file =====
ids_file = "ids.txt"

with open(ids_file, "r", encoding="utf-8") as f:
    ids = [line.strip() for line in f if line.strip()]

# ===== Đếm số lần xuất hiện =====
counter = Counter(ids)

# ===== Lọc ra các ID bị trùng =====
duplicates = {k: v for k, v in counter.items() if v > 1}

if duplicates:
    print("⚠️ Các ID bị trùng trong ids.txt:")
    for k, v in duplicates.items():
        print(f"  • {k} xuất hiện {v} lần")
else:
    print("✅ Không có ID nào bị trùng trong ids.txt.")
