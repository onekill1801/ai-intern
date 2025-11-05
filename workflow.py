from dotenv import load_dotenv
import os
import requests
import json
import time

load_dotenv() 

# === Cấu hình cơ bản ===
BASE_URL = "https://erequest.kyta.fpt.com/services/erequest/api"
TOKEN = os.getenv("EREQUEST_TOKEN")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}",  # bỏ comment nếu có token
}

process = 0
faild = 0
arr_process = []
arr_faild = []
arr_network = []
arr_done = []
arr_none = []
arr_ai1 = []

# === Hàm tiện ích ===
def call_api(url, method="GET", data=None):
    try:
        if method == "GET":
            resp = requests.get(url, headers=HEADERS, timeout=30)
        elif method == "POST":
            resp = requests.post(url, headers=HEADERS, json=data, timeout=30)
        elif method == "DELETE":
            resp = requests.delete(url, headers=HEADERS, timeout=30)
        else:
            raise ValueError(f"Unsupported method {method}")
        print(f"👉 [{method}] {url} -> {resp.status_code}")
        return resp
    except Exception as e:
        print(f"❌ Error calling {url}: {e}")
        return None


# === Logic xử lý cho từng ticket ===
def process_ticket(ticket_id):
    global process, faild
    print(f"\n=== 🔹 Đang xử lý ticketId: {ticket_id} ===")

    # 1️⃣ Gọi API1 để lấy recipients
    url1 = f"{BASE_URL}/ticket-recipients/statusRaw/{ticket_id}"
    resp1 = call_api(url1)
    if not resp1 or resp1.status_code != 200:
        print("❌ Không lấy được dữ liệu từ API1")
        return

    data1 = resp1.json()
    recipients = data1.get("party", {}).get("recipients", [])

    # 2️⃣ Tìm AI 1 + AI 2
    ai12 = next((r for r in recipients if "AI 1 + AI 2" in r.get("notionName", "")), None)
    ai11 = next((r for r in recipients if "AI 1" in r.get("notionName", "")), None)
    ai3 = next((r for r in recipients if "AI3: Tổng hợp các khoản thi hành án" in r.get("notionName", "")), None)

    if not ai12:
        print("⚠️ Không thấy recipient AI 1 + AI 2")
        if not ai11:
            print("⚠️ Không thấy recipient AI 1")
            return
        arr_ai1.append(ticket_id)
        if ai11.get("implementerId") is None:
            target_id = ai11["id"]
            print(f"✅ Sử dụng AI 1 (implementerId=null) -> {target_id}")
        else:
            print("🛑 implementerId của AI1 cũng khác null -> Dừng.")
            return
    # 3️⃣ Kiểm tra implementerId theo logic
    else:
        if ai12.get("implementerId") is None:
            target_id = ai12["id"]
            print(f"✅ Sử dụng AI 1 + AI 2 (implementerId=null) -> {target_id}")
        else:
            if not ai3:
                print("⚠️ Không thấy recipient AI3")
                return
            if ai3.get("implementerId") is None:
                target_id = ai3["id"]
                print(f"✅ Sử dụng AI3 (implementerId=null) -> {target_id}")
            else:
                print("🛑 implementerId của cả AI1+2 và AI3 đều khác null -> Dừng.")
                return

    # 4️⃣ Gọi API2
    url2 = f"{BASE_URL}/ai-response-content/getAiResponseActive/{ticket_id}/{target_id}"
    resp2 = call_api(url2)
    if not resp2 or resp2.status_code != 200:
        print("❌ Lỗi khi gọi API2 -> Thử recall (API4)")
        url4 = f"{BASE_URL}/ai-response-content/recallOcrTicket/{ticket_id}/{target_id}"
        call_api(url4, method="POST")
        return
        
    try:
        _ = resp2.json()
    except json.JSONDecodeError:
        print("⚠️ API2 trả về không phải JSON hợp lệ -> dừng xử lý.")
        return

    data2 = resp2.json()
    output = data2.get("output", {})
    status = output.get("status") or data2.get("status")
    message = output.get("message")
    api2_id = data2.get("id")

    print(f"📊 API2 status: {status}")

    # 5️⃣ Kiểm tra trạng thái để quyết định bước tiếp theo
    if status == "DONE":
        print("✅ Hoàn tất (status=DONE)")
        arr_done.append(ticket_id)
        return
    elif status is None or output is None:
        print("⚠️ Không có output/status -> recall OCR")
        arr_none.append(ticket_id)
        url4 = f"{BASE_URL}/ai-response-content/recallOcrTicket/{ticket_id}/{target_id}"
        call_api(url4, method="POST")
        return
    elif status == "ERROR":
        print("❌ status=ERROR -> gọi API3 (DELETE)")
        arr_faild.append(ticket_id)
        url3 = f"{BASE_URL}/ai-response-contents/{api2_id}"
        resp3 = call_api(url3, method="DELETE")
        if resp3 and resp3.status_code == 204:
            print("✅ API3 xoá thành công, recall lại API4")
            url4 = f"{BASE_URL}/ai-response-content/recallOcrTicket/{ticket_id}/{target_id}"
            call_api(url4, method="POST")
        else:
            print("⚠️ API3 xoá thất bại hoặc không trả 204")
    elif status == "PROCESSING":
        print("❌ status=PROCESSING -> gọi API3 (DELETE)")
        arr_process.append(ticket_id)
        process += 1
        url3 = f"{BASE_URL}/ai-response-contents/{api2_id}"
        resp3 = call_api(url3, method="DELETE")
        if resp3 and resp3.status_code == 204:
            print("✅ API3 xoá thành công, recall lại API4")
            url4 = f"{BASE_URL}/ai-response-content/recallOcrTicket/{ticket_id}/{target_id}"
            call_api(url4, method="POST")
        else:
            print("⚠️ API3 xoá thất bại hoặc không trả 204")
        return
    else:
        if message is not None:
            faild += 1
            arr_network.append(ticket_id)
            print(f"❗ Message từ API2: {message}")
            url3 = f"{BASE_URL}/ai-response-contents/{api2_id}"
            resp3 = call_api(url3, method="DELETE")
            if resp3 and resp3.status_code == 204:
                print("✅ API3 xoá thành công, recall lại API4")
                url4 = f"{BASE_URL}/ai-response-content/recallOcrTicket/{ticket_id}/{target_id}"
                call_api(url4, method="POST")
        else:
            print("⚠️ Trạng thái không xác định, dừng xử lý.")


# === MAIN ===
if __name__ == "__main__":
    # đọc danh sách ticket từ file (mỗi dòng 1 ticketId)
    with open("out.txt") as f:
        ticket_ids = [line.strip() for line in f if line.strip()]

    for tid in ticket_ids:
        process_ticket(tid)
        time.sleep(2)  # tránh spam server

    print(f"\n=== Kết thúc xử lý ===\nTổng ticket đang PROCESSING: {process}\nTổng ticket bị FAILD: {faild}")
    print(f"Ticket PROCESSING: {arr_process}")
    print(f"Ticket FAILD: {arr_faild}")
    print(f"Ticket DONE: {arr_done}")
    print(f"Ticket NONE: {arr_none}")
    print(f"Ticket AI1 only: {arr_ai1}")
    print(f"Ticket NETWORK issues: {arr_network}")
