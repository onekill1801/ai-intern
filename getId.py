import json

# === 1️⃣ Đọc dữ liệu từ file JSON ===
input_file = "data.json"   # đổi tên file nếu cần
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# === 2️⃣ Hàm loại bỏ tiền tố "sid_" ===
def clean_id(value):
    if isinstance(value, str) and value.startswith("sid_"):
        return value.replace("sid_", "", 1)
    return value

# === 3️⃣ Thu thập tất cả các ID ===
all_ids = []

for item in data:
    # id ở cấp 1
    if "id" in item:
        all_ids.append(clean_id(item["resourceId"]))
    
    # id trong recipients (nếu có)
    # if "recipients" in item and isinstance(item["recipients"], list):
    #     for rec in item["recipients"]:
    #         if "id" in rec:
    #             all_ids.append(clean_id(rec["id"]))

# === 4️⃣ In danh sách id ===
print("Danh sách ID (đã bỏ 'sid_'):")
for i in all_ids:
    print(i)
