import json
import requests
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# === 1️⃣ Đọc data list từ file JSON ===
input_file = "data.json"  # đổi tên file nếu cần
with open(input_file, "r", encoding="utf-8") as f:
    data_list = json.load(f)

# === 2️⃣ Cấu hình API ===
url = "https://eaccount.kyta.fpt.com/services/document-service/api/call-log"

token = os.getenv("EREQUEST_TOKEN")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# === 3️⃣ instId mới cần sửa ===
# new_inst_id = 0
num_inst = 5
num_workers = 10
index = 0
max_threads = 100  # Số luồng tối đa

# === 4️⃣ Gửi PUT request cho từng phần tử ===
# for idx, item in enumerate(data_list):
#     # if item["instId"] == 0 or item["instId"] == "1":
#     #     continue # bỏ qua instId=0 và instId=1
#     new_inst_id = idx % num_inst 
#     new_worker_id = idx % num_workers 
#     item["instId"] = new_inst_id
#     item["workerId"] = new_worker_id
#     item["status"] = "processing"

#     response = requests.put(url, headers=headers, json=item)
#     index += 1
#     print(f"📦 Gửi PUT cho id={item['id']} ... status_code={response.status_code}")
#     if response.ok:
#         print("✅ Thành công:", response.text)
#     else:
#         print("❌ Lỗi:", response.text)

# print("✅ Hoàn tất cập nhật instId cho toàn bộ dữ liệu." + f" Tổng số phần tử đã xử lý: {index}")


# ==== Hàm gửi PUT request ====
def update_item(idx, item):
    new_inst_id = random.randint(0, num_inst - 1)
    new_worker_id = random.randint(0, num_workers - 1)

    item["instId"] = new_inst_id
    item["workerId"] = new_worker_id
    item["status"] = "processing"

    try:
        response = requests.put(url, headers=headers, json=item, timeout=10)
        if response.ok:
            return f"✅ Thành công: id={item['id']} status_code={response.status_code}"
        else:
            return f"❌ Lỗi: id={item['id']} status_code={response.status_code} | {response.text}"
    except Exception as e:
        return f"💥 Lỗi exception: id={item['id']} | {e}"

# ==== Chạy đa luồng ====
def run_multithread(data_list):
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(update_item, idx, item): item for idx, item in enumerate(data_list)}
        for i, future in enumerate(as_completed(futures)):
            print(f"[{i+1}/{len(futures)}] {future.result()}")

# ==== Chạy ====
if __name__ == "__main__":
    # Giả sử bạn đã có data_list (đọc từ file hoặc API)
    # with open("data.json", "r", encoding="utf-8") as f:
    #     data_list = json.load(f)

    # Ví dụ demo:
    run_multithread(data_list)