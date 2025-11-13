import os
import requests
import time
from dotenv import load_dotenv

# --- 1. Đọc token từ .env ---
load_dotenv()
TOKEN = os.getenv("EREQUEST_TOKEN")

if not TOKEN:
    raise ValueError("⚠️ Thiếu token trong file .env (EACCOUNT_TOKEN)")

# --- 2. Cấu hình API ---
BASE_URL = "https://eaccount.kyta.fpt.com/services/eintelligent/api/job-backups"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

# --- 3. Hàm gọi API cho 1 ID ---
def call_api(job_id):
    url = f"{BASE_URL}/{job_id}"
    try:
        response = requests.delete(url, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            print(f"✅ ID {job_id}: OK")
            # nếu bạn muốn xem dữ liệu trả về:
            # print(response.json())
        elif response.status_code == 404:
            print(f"⚠️ ID {job_id}: Không tìm thấy (404)")
        else:
            print(f"❌ ID {job_id}: lỗi {response.status_code} - {response.text[:200]}")
    except requests.RequestException as e:
        print(f"🚨 Lỗi khi gọi ID {job_id}: {e}")

# --- 4. Chạy từ m đến n ---
def run_range(m, n, delay=0.2):
    print(f"🔄 Bắt đầu gọi API từ {m} đến {n}")
    for job_id in range(m, n + 1):
        call_api(job_id)
        # time.sleep(delay)  # tránh bị rate-limit (giới hạn tốc độ)
    print("🎉 Hoàn tất.")

# --- 5. Nhập khoảng ID muốn gọi ---
if __name__ == "__main__":
    # m = int(input("Nhập ID bắt đầu (m): "))
    # n = int(input("Nhập ID kết thúc (n): "))
    m, n  = 64836,66953  # <-- Thay giá trị này nếu muốn chạy cố định
    run_range(m, n)
