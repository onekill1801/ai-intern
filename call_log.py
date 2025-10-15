import json
import requests

# === 1️⃣ Đọc data list từ file JSON ===
input_file = "data.json"  # đổi tên file nếu cần
with open(input_file, "r", encoding="utf-8") as f:
    data_list = json.load(f)

# === 2️⃣ Cấu hình API ===
url = "https://eaccount.kyta.fpt.com/services/document-service/api/call-log"

token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aSI6eyJncm91cHNOYW1lIjpbXSwicm9sZXMiOlsxNzk5LDE4NzldLCJncm91cHMiOltdLCJpcEFjY2VzcyI6W10sImxvZ2luIjoiY2hhcGhhbmh2aWVudGVzdEB5b3BtYWlsLmNvbSIsImZvbGRlcklkIjoiMDAwMDYxMDBrdTVtNGYyNXdLQkt5SmlLUDU0IiwiZm9sZGVyUGF0aCI6Ii9zdG9yYWdlLTAxLzU2ODIiLCJkYlN1ZmZpeCI6IjAwMDA2IiwibGFuZ0tleSI6bnVsbCwiY3VzdElkIjo1NjgyLCJvcmdJbiI6Ii81NjgyLzEyMTYwLzEyMTYxIiwiaWQiOjE0MDIzMCwiZW1haWwiOiJjaGFwaGFuaHZpZW50ZXN0QHlvcG1haWwuY29tIn0sInVzZXJfbmFtZSI6ImNoYXBoYW5odmllbnRlc3RAeW9wbWFpbC5jb20iLCJzY29wZSI6WyJvcGVuaWQiXSwiZXhwIjoxNzYwNTU3MzMyLCJpYXQiOjE3NjA1NTU1MzIsImF1dGhvcml0aWVzIjpbIlJPTEVfVVNFUl9SRVNUUklDVCIsIlJPTEVfQ1VTVF9SRVBPUlQiLCJST0xFX1VTRVIiLCJST0xFX0NVU1RfRE9DIiwiUk9MRV9PUkdfQURNSU4iLCJST0xFX0NVU1RfU1RBRkYiLCJST0xFX0NVU1RfVklFV0VSIl0sImp0aSI6ImE4NmJiNTI1LWViYWYtNDRmNy1iMDYxLTFhMzI5MTgwZDQ4ZSIsImNsaWVudF9pZCI6IndlYl9hcHAifQ.cYKuht8tGtDpBlN4Dd2JfoMer-1PRzyF2zAl5LEjn3WuCYhiZl1I4GEyTgBCSzA0Zx8-j_k6eRrOc-GDbdcfJzhvucqWZbY60OwIdn89Nez3BFw8lp_90ee4A-T__PmOxj_tCTKqCzs6JLIXeCsrtbCSTEXQwwUwpWKo0kbTZSxd7S0X3Fvag8d5UpHtccmRn15D85WIq8tX-nGfC32Ltk-dezJtNsfww6rILuiXuuM0EyFl35s7PozKFhfnPBVlXt5FXNFAh3h99iuxMkDop5RDYCrgHYJPQdV6TXJ7I0Knmpxc5rLGW3e_GFWrPlBRRF4ay7MQPwdHTYKi-NLUuA"  # Dán token thật của bạn vào đây

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# === 3️⃣ instId mới cần sửa ===
# new_inst_id = 0
num_inst = 2
num_workers = 10
index = 0

# === 4️⃣ Gửi PUT request cho từng phần tử ===
for idx, item in enumerate(data_list):
    # if item["instId"] == 0 or item["instId"] == "1":
    #     continue # bỏ qua instId=0 và instId=1
    new_inst_id = idx % num_inst 
    new_worker_id = idx % num_workers 
    item["instId"] = new_inst_id
    item["workerId"] = new_worker_id
    item["status"] = "processing"

    response = requests.put(url, headers=headers, json=item)
    index += 1
    print(f"📦 Gửi PUT cho id={item['id']} ... status_code={response.status_code}")
    if response.ok:
        print("✅ Thành công:", response.text)
    else:
        print("❌ Lỗi:", response.text)

print("✅ Hoàn tất cập nhật instId cho toàn bộ dữ liệu." + f" Tổng số phần tử đã xử lý: {index}")
