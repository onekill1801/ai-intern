import requests
import re
import os

# Đường dẫn file chứa danh sách ID
ids_file = "ids.txt"

# Thư mục lưu file tải về
download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)

# Token (cập nhật token hợp lệ tại đây)
AUTH_TOKEN = "Bearer "  # ⚠️ thay token thật

# Mẫu URL API
API_TEMPLATE = "https://econtract.capitaland.kytaplatform.com/app/services/envelope/api/envelope/{id}/doc/contentall"

# Header chung
headers = {
    "accept": "application/json, text/plain, */*",
    "Authorization": AUTH_TOKEN,
}

# Đọc danh sách ID từ file
with open(ids_file, "r", encoding="utf-8") as f:
    ids = [line.strip() for line in f if line.strip()]

print(f"🔍 Đã đọc {len(ids)} ID từ {ids_file}")

# Duyệt từng ID để tải file
for idx, doc_id in enumerate(ids, start=1):
    url = API_TEMPLATE.format(id=doc_id)
    print(f"📥 [{idx}/{len(ids)}] Đang tải ID: {doc_id}")

    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:
        # Lấy tên file từ header Content-Disposition
        content_disp = response.headers.get("Content-Disposition", "")
        match = re.search(r'filename="?([^"]+)"?', content_disp)
        filename = match.group(1) if match else f"{doc_id}.bin"

        filepath = os.path.join(download_dir, filename)

        # Ghi file ra đĩa
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print(f"✅ Đã lưu: {filepath}")
    else:
        print(f"❌ Lỗi khi tải {doc_id}: {response.status_code}")
        try:
            print("Chi tiết:", response.json())
        except Exception:
            print("Chi tiết:", response.text)
