import os
import requests
import threading
import time
from dotenv import load_dotenv

# === 1. Đọc biến môi trường ===
load_dotenv()
API_KEYS = os.getenv("API_KEYS", "").split(",")

if not API_KEYS or API_KEYS == [""]:
    raise ValueError("⚠️ Không tìm thấy API_KEYS trong file .env")

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/files"

# === 2. Hàm lấy danh sách file ===
def list_files(api_key, page_token=None):
    params = {}
    if page_token:
        params["pageToken"] = page_token
    headers = {"x-goog-api-key": api_key}

    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code != 200:
        print(f"[{api_key[:8]}...] ❌ Lỗi khi gọi list_files: {response.status_code} {response.text}")
        return [], None

    data = response.json()
    files = data.get("files", [])
    next_page = data.get("nextPageToken")
    return files, next_page

# === 3. Hàm xóa file ===
def delete_file(api_key, file_id):
    url = f"{BASE_URL}/{file_id}"
    headers = {"x-goog-api-key": api_key}
    resp = requests.delete(url, headers=headers)
    if resp.status_code in (200, 204):
        print(f"[{api_key[:8]}...] ✅ Xóa thành công: {file_id}")
    else:
        print(f"[{api_key[:8]}...] ❌ Lỗi xóa {file_id}: {resp.status_code} {resp.text}")

# === 4. Luồng worker ===
def worker(api_key):
    print(f"🚀 Bắt đầu thread với API key {api_key[:8]}...")
    page_token = None

    while True:
        files, next_token = list_files(api_key, page_token)
        if not files:
            print(f"[{api_key[:8]}...] Không còn file nào hoặc lỗi API.")
            break

        for f in files:
            name = f.get("name")  # ví dụ: "files/abcd1234"
            if name and name.startswith("files/"):
                file_id = name.split("/")[1]
                delete_file(api_key, file_id)
                time.sleep(0.2)  # delay nhẹ để tránh giới hạn rate

        if not next_token:
            print(f"[{api_key[:8]}...] ✅ Đã xử lý hết trang cuối.")
            break
        else:
            page_token = next_token
            time.sleep(1)  # nghỉ 1s giữa các page

# === 5. Tạo & chạy 10 thread song song ===
threads = []
for key in API_KEYS:
    t = threading.Thread(target=worker, args=(key.strip(),))
    t.start()
    threads.append(t)
    time.sleep(0.5)  # khởi động luồng cách nhau 0.5s để tránh dồn tải

# === 6. Chờ tất cả thread kết thúc ===
for t in threads:
    t.join()

print("🎉 Hoàn tất xoá toàn bộ file trên tất cả API keys.")
