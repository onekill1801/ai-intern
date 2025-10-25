import requests
import json
import time

# Cấu hình API
base_url = "https://econtract.capitaland.kytaplatform.com/app/services/envelope/api/envelope/status/completed"
headers = {
    "accept": "application/json, text/plain, */*",
    "Authorization": "Bearer "  # thay token thật vào đây
}

# File đầu ra
output_file = "data_1.json"

page = 0
page_size = 50
all_items = []

while True:
    params = {
        "page": page,
        "size": page_size,
        "sort": "lastModifiedDate,desc",
        "search": '{"owner":"nguyen.mauthanh@capitaland.com","orgIn":"/6155/14267/14318/14319/14320/14321/14324"}'
    }

    print(f"🔄 Đang tải trang {page}...")

    resp = requests.get(base_url, headers=headers, params=params)

    if resp.status_code != 200:
        print(f"❌ Lỗi khi gọi API (HTTP {resp.status_code}): {resp.text}")
        break

    data = resp.json()
    if not data:
        print("✅ Hết dữ liệu.")
        break

    # Append dữ liệu mới vào list tổng
    all_items.extend(data)

    # Nếu số phần tử < page_size thì dừng (hết trang)
    if len(data) < page_size:
        break

    page += 1
    time.sleep(0.5)  # nghỉ nhẹ để tránh spam server


# Ghi dữ liệu vào file (append, không ghi đè)
try:
    with open(output_file, "r", encoding="utf-8") as f:
        existing_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    existing_data = []

# Gộp dữ liệu cũ và mới
existing_data.extend(all_items)

# Ghi lại vào file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=4)

print(f"✅ Đã tải xong {len(all_items)} phần tử và lưu vào '{output_file}'")
