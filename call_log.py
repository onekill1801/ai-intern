import json
import requests

# === 1️⃣ Đọc data list từ file JSON ===
input_file = "data.json"  # đổi tên file nếu cần
with open(input_file, "r", encoding="utf-8") as f:
    data_list = json.load(f)

# === 2️⃣ Cấu hình API ===
url = "https://eaccount.kyta.fpt.com/services/document-service/api/call-log"

token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aSI6eyJncm91cHNOYW1lIjpbXSwicm9sZXMiOlsxNzk5LDE4NzldLCJncm91cHMiOltdLCJpcEFjY2VzcyI6W10sImxvZ2luIjoiY2hhcGhhbmh2aWVudGVzdEB5b3BtYWlsLmNvbSIsImZvbGRlcklkIjoiMDAwMDYxMDBrdTVtNGYyNXdLQkt5SmlLUDU0IiwiZm9sZGVyUGF0aCI6Ii9zdG9yYWdlLTAxLzU2ODIiLCJkYlN1ZmZpeCI6IjAwMDA2IiwibGFuZ0tleSI6bnVsbCwiY3VzdElkIjo1NjgyLCJvcmdJbiI6Ii81NjgyLzEyMTYwLzEyMTYxIiwiaWQiOjE0MDIzMCwiZW1haWwiOiJjaGFwaGFuaHZpZW50ZXN0QHlvcG1haWwuY29tIn0sInVzZXJfbmFtZSI6ImNoYXBoYW5odmllbnRlc3RAeW9wbWFpbC5jb20iLCJzY29wZSI6WyJvcGVuaWQiXSwiZXhwIjoxNzYwNDE0ODg2LCJpYXQiOjE3NjA0MTMwODYsImF1dGhvcml0aWVzIjpbIlJPTEVfVVNFUl9SRVNUUklDVCIsIlJPTEVfQ1VTVF9SRVBPUlQiLCJST0xFX1VTRVIiLCJST0xFX0NVU1RfRE9DIiwiUk9MRV9PUkdfQURNSU4iLCJST0xFX0NVU1RfU1RBRkYiLCJST0xFX0NVU1RfVklFV0VSIl0sImp0aSI6IjY4YjA0MjJkLTFiMGYtNDllMS1iNmYzLTk2ZDI0MWI0MDJjNCIsImNsaWVudF9pZCI6IndlYl9hcHAifQ.CAtu3_-2DufmVFM3rFU7CCBomMkvAngt4KWI0KLAIUs8snCbIlvRDvqPWneSqKYFZXreN_PzAL-jgYQKZGea2kD5moE8EFCbhgCfmHL_g9tFQGt_tG6CbkmLNTERIoGfy4ine83m_DuBAmB5vA3SB4u0FUle3EjnKQMAXM0PHpgRuCwJZfGipTKVT0GDLe1ZilAQ65hodb3Xb_Vb4dOyNBXepoLf4nc2_8WTJ14GuRfOij2-9gYQ_caziCLQ_3xtcZI5ACRp4WBYzKxHVeHCnrbPMSslr0oU8pC9u7QK0XF5BW5kceOelExF84WPUZCIfIfBMcetlqK07YPbuo2f8g"  # Dán token thật của bạn vào đây

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# === 3️⃣ instId mới cần sửa ===
# new_inst_id = 0
num_inst = 5

# === 4️⃣ Gửi PUT request cho từng phần tử ===
for idx, item in enumerate(data_list):
    new_inst_id = idx % num_inst  # chia đều theo vị trí
    item["instId"] = new_inst_id

    response = requests.put(url, headers=headers, json=item)

    print(f"📦 Gửi PUT cho id={item['id']} ... status_code={response.status_code}")
    if response.ok:
        print("✅ Thành công:", response.text)
    else:
        print("❌ Lỗi:", response.text)

print("✅ Hoàn tất cập nhật instId cho toàn bộ dữ liệu.")
