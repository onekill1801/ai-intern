import json

# === 1️⃣ Đọc dữ liệu từ file JSON ===
input_file = "data.json"      # file chứa dữ liệu gốc
output_file = "id_list.txt"   # file để lưu kết quả

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# === 2️⃣ Lấy danh sách tất cả id (nếu có nhiều phần tử) ===
id_list = [item["id"] for item in data if "id" in item]

# === 3️⃣ Ghi danh sách id ra file ===
with open(output_file, "w", encoding="utf-8") as f:
    for _id in id_list:
        f.write(_id + "\n")

print(f"✅ Đã xuất {len(id_list)} ID ra file: {output_file}")
