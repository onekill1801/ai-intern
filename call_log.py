import json
import requests

# === 1️⃣ Đọc data list từ file JSON ===
input_file = "data.json"  # đổi tên file nếu cần
with open(input_file, "r", encoding="utf-8") as f:
    data_list = json.load(f)

# === 2️⃣ Cấu hình API ===
url = ""

token = ""  # Dán token thật của bạn vào đây

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# === 3️⃣ instId mới cần sửa ===
new_inst_id = 0

# === 4️⃣ Gửi PUT request cho từng phần tử ===
for item in data_list:
    item["instId"] = new_inst_id  # cập nhật instId

    response = requests.put(url, headers=headers, json=item)

    print(f"📦 Gửi PUT cho id={item['id']} ... status_code={response.status_code}")
    if response.ok:
        print("✅ Thành công:", response.text)
    else:
        print("❌ Lỗi:", response.text)

print("✅ Hoàn tất cập nhật instId cho toàn bộ dữ liệu.")
