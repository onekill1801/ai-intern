import requests
import re
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# ===== Cấu hình =====
ids_file = "ids.txt"
download_dir = "downloads2"
os.makedirs(download_dir, exist_ok=True)

log_file = "download_log.txt"

# ⚠️ Cập nhật token thật ở đây
AUTH_TOKEN = "Bearer "  

API_TEMPLATE = "https://econtract.capitaland.kytaplatform.com/app/services/envelope/api/envelope/{id}/doc/contentall"

headers = {
    "accept": "application/json, text/plain, */*",
    "Authorization": AUTH_TOKEN,
}


# ===== Hàm sinh tên file không trùng =====
def get_unique_filename(directory, filename):
    """
    Nếu file đã tồn tại, thêm _1, _2,... vào sau tên.
    """
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1

    return new_filename


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

            # Kiểm tra trùng tên
            unique_filename = get_unique_filename(download_dir, filename)
            filepath = os.path.join(download_dir, unique_filename)

            # Ghi file
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            # Log kết quả
            if unique_filename != filename:
                message = f"⚠️ {doc_id}: Tên trùng, đổi thành '{unique_filename}'"
            else:
                message = f"✅ {doc_id} → {unique_filename}"

            with open(log_file, "a", encoding="utf-8") as log:
                log.write(message + "\n")

            return message

        else:
            message = f"❌ {doc_id}: HTTP {response.status_code}"
            with open(log_file, "a", encoding="utf-8") as log:
                log.write(message + "\n")
            return message

    except Exception as e:
        message = f"⚠️ {doc_id}: Lỗi {e}"
        with open(log_file, "a", encoding="utf-8") as log:
            log.write(message + "\n")
        return message


# ===== Đọc danh sách ID =====
with open(ids_file, "r", encoding="utf-8") as f:
    ids = [line.strip() for line in f if line.strip()]

print(f"📄 Đã đọc {len(ids)} ID từ {ids_file}")

# ===== Chạy đa luồng =====
MAX_THREADS = 15  # có thể tăng lên 10 nếu mạng ổn định

with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    futures = {executor.submit(download_file, doc_id): doc_id for doc_id in ids}

    for future in as_completed(futures):
        print(future.result())

print("🎉 Hoàn tất tải toàn bộ file! Xem log chi tiết trong:", log_file)
