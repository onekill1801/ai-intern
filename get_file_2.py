import requests
import re
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# ===== Cấu hình =====
ids_file = "ids.txt"
download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)

# ⚠️ Cập nhật token thật ở đây
AUTH_TOKEN = "Bearer "  

API_TEMPLATE = "https://econtract.capitaland.kytaplatform.com/app/services/envelope/api/envelope/{id}/doc/contentall"

headers = {
    "accept": "application/json, text/plain, */*",
    "Authorization": AUTH_TOKEN,
}

# ===== Hàm tải 1 file =====
def download_file(doc_id):
    try:
        url = API_TEMPLATE.format(id=doc_id)
        response = requests.get(url, headers=headers, stream=True, timeout=60)

        if response.status_code == 200:
            # Lấy tên file từ header
            content_disp = response.headers.get("Content-Disposition", "")
            match = re.search(r'filename="?([^"]+)"?', content_disp)
            filename = match.group(1) if match else f"{doc_id}.bin"

            filepath = os.path.join(download_dir, filename)

            # Ghi file
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            return f"✅ {doc_id} → {filename}"
        else:
            return f"❌ {doc_id}: HTTP {response.status_code}"
    except Exception as e:
        return f"⚠️ {doc_id}: Lỗi {e}"

# ===== Đọc danh sách ID =====
with open(ids_file, "r", encoding="utf-8") as f:
    ids = [line.strip() for line in f if line.strip()]

print(f"📄 Đã đọc {len(ids)} ID từ {ids_file}")

# ===== Chạy đa luồng =====
MAX_THREADS = 5  # số luồng song song, có thể tăng lên 10–15 nếu mạng ổn định

with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    futures = {executor.submit(download_file, doc_id): doc_id for doc_id in ids}

    for future in as_completed(futures):
        print(future.result())

print("🎉 Hoàn tất tải toàn bộ file!")
