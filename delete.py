import json
import requests

# === 1️⃣ Đọc data_list từ file JSON ===
input_file = "out.json"
with open(input_file, "r", encoding="utf-8") as f:
    data_list = json.load(f)

# === 2️⃣ Lấy danh sách ID ===
ids = [item["id"] for item in data_list]

print(f"🔍 Tổng số ID cần xử lý: {len(ids)}")

# === 3️⃣ Cấu hình API ===
base_url = "/api/job-step-asyncs"
token = ""  # Dán token thật vào đây

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# === 4️⃣ Gọi API cho từng ID ===
for id_value in ids:
    url = f"{base_url}/{id_value}"
    print(f"📡 Gọi API: {url}")

    try:
        response = requests.delete(url, headers=headers)
        print(f"➡️ Status: {response.status_code}")
        if response.ok:
            print("✅ Kết quả:", response.text[:200], "...\n")  # in tóm tắt
        else:
            print("❌ Lỗi:", response.text, "\n")
    except Exception as e:
        print(f"⚠️ Lỗi khi gọi {url}: {e}\n")

print("🎯 Hoàn tất gọi API cho toàn bộ ID.")
