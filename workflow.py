from dotenv import load_dotenv
import os
import requests
import json
import time
from datetime import datetime, timezone

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
arr_hold = []
arr_api5 = []

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

def is_older_than(last_modified_str: str, cutoff_str: str) -> bool:
    """
    So sánh 2 thời gian dạng ISO (VD: '2025-11-12T03:20:42Z').
    Trả về True nếu last_modified_str < cutoff_str.
    """
    if not last_modified_str:
        print("⚠️ last_modified_str bị None hoặc rỗng.")
        return False

    try:
        last_modified = datetime.strptime(last_modified_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        cutoff_time = datetime.strptime(cutoff_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        return last_modified < cutoff_time
    except Exception as e:
        print(f"⚠️ Lỗi khi parse thời gian: {e}")
        return False

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
        # urlcheckjob = f"https://eaccount.kyta.fpt.com/services/eintelligent/api/v4/process?jobId={jobId}"
        # respcheck = call_api(urlcheckjob)
        # checkdata = respcheck.json()
        # checkstatus = checkdata.get("status")
        # print(f"📊 Kiểm tra jobId {jobId} status: {checkstatus}")
        if ai11.get("implementerId") is None:
            arr_ai1.append(ticket_id)
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
                arr_done.append(ticket_id)
                return

    # 4️⃣ Gọi API2
    url2 = f"{BASE_URL}/ai-response-content/getAiResponseActive/{ticket_id}/{target_id}"
    url5 = f"{BASE_URL}/tickets/callback/saveFormDataByVariables/{ticket_id}/{target_id}"
    resp2 = call_api(url2)
    if not resp2 or resp2.status_code != 200:
        print("❌ Lỗi khi gọi API2 -> Thử recall (API4)")
        arr_hold.append(ticket_id)
        # url4 = f"{BASE_URL}/ai-response-content/recallOcrTicket/{ticket_id}/{target_id}"
        # call_api(url4, method="POST")
        return
        
    try:
        _ = resp2.json()
    except json.JSONDecodeError:
        print("⚠️ API2 trả về không phải JSON hợp lệ -> call API5")
        resp5 = call_api(url5)
        arr_api5.append(ticket_id)
        try :
            _ = resp5.json()
            print("✅ API5 recallForm thành công, recall lại API4")
            # url4 = f"{BASE_URL}/ai-response-content/recallOcrTicket/{ticket_id}/{target_id}"
            # call_api(url4, method="POST")
        except json.JSONDecodeError:
            print("⚠️ API5 trả về không phải JSON hợp lệ -> dừng xử lý.")
            return
        return

    data2 = resp2.json()
    output = data2.get("output", {})
    status = output.get("status") or data2.get("status")
    data = output.get("data") or {}
    jobId = data.get("jobId")
    last_modified_str = data2.get("lastModifiedDate")
    if is_older_than(last_modified_str, "2025-11-13T09:00:00Z"):
        print("DONE")
        # return
    else: 
        print("False")
        return
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
        # url4 = f"{BASE_URL}/ai-response-content/recallOcrTicket/{ticket_id}/{target_id}"
        # call_api(url4, method="POST")
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
        # urlcheckjob = f"https://eaccount.kyta.fpt.com/services/eintelligent/api/v4/process?jobId={jobId}"
        # respcheck = call_api(urlcheckjob)
        # checkdata = respcheck.json()
        # checkstatus = checkdata.get("status")
        # print(f"📊 Kiểm tra jobId {jobId} status: {checkstatus}")

        # # save file
        # log_file = os.path.join("results2", "job_status_log.csv")
        # os.makedirs("results2", exist_ok=True)
        # with open(log_file, "a", encoding="utf-8") as f:
        #     f.write(f"{ticket_id},{jobId},{checkstatus}\n")
        # print(f"📝 Đã ghi log job status vào {log_file}")

        # if checkstatus == "DONE":
        #     return
        # url3 = f"{BASE_URL}/ai-response-contents/{api2_id}"
        # resp3 = call_api(url3, method="DELETE")
        # if resp3 and resp3.status_code == 204:
        #     print("✅ API3 xoá thành công, recall lại API4")
        #     url4 = f"{BASE_URL}/ai-response-content/recallOcrTicket/{ticket_id}/{target_id}"
        #     call_api(url4, method="POST")
        # else:
        #     print("⚠️ API3 xoá thất bại hoặc không trả 204")
        # return
    else:
        if message is not None:
            faild += 1
            arr_network.append(ticket_id)
            print(f"❗ Message từ API2: {message}")
            # url3 = f"{BASE_URL}/ai-response-contents/{api2_id}"
            # resp3 = call_api(url3, method="DELETE")
            # if resp3 and resp3.status_code == 204:
            #     print("✅ API3 xoá thành công, recall lại API4")
            #     url4 = f"{BASE_URL}/ai-response-content/recallOcrTicket/{ticket_id}/{target_id}"
            #     call_api(url4, method="POST")
        else:
            arr_none.append(ticket_id)
            print("⚠️ Trạng thái không xác định, dừng xử lý.")


# === MAIN ===
if __name__ == "__main__":
    # đọc danh sách ticket từ file (mỗi dòng 1 ticketId)
    print("=== Start time ===", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    with open("job_step_id.txt") as f:
        ticket_ids = [line.strip() for line in f if line.strip()]

    for tid in ticket_ids:
        process_ticket(tid)
        time.sleep(0.5)  # tránh spam server

    print(f"\n=== Kết thúc xử lý ===\nTổng ticket đang PROCESSING: {process}\nTổng ticket bị FAILD: {faild}")
    print(f"Ticket PROCESSING: {arr_process}")
    print(f"Ticket FAILD: {arr_faild}")
    print(f"Ticket DONE: {arr_done}")
    print(f"Ticket NONE: {arr_none}")
    print(f"Ticket AI1 only: {arr_ai1}")
    print(f"Ticket NETWORK issues: {arr_network}")
    print("=== END time ===", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


    process = len(arr_process)
    faild = len(arr_faild)

    # --- Thư mục để chứa kết quả ---
    output_dir = "results3"
    os.makedirs(output_dir, exist_ok=True)

    # --- Ghi tóm tắt chung ---
    summary_file = os.path.join(output_dir, "summary.txt")
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("=== Kết thúc xử lý ===\n")
        f.write(f"Tổng ticket đang PROCESSING: {process}\n")
        f.write(f"Tổng ticket bị FAILD: {faild}\n")
        f.write(f"=== END time === {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n")

    print(f"📄 Đã ghi file tóm tắt: {summary_file}")

    # --- Danh sách các list cần ghi ---
    data_lists = {
        "processing": arr_process,
        "faild": arr_faild,
        "done": arr_done,
        "none": arr_none,
        "ai1_only": arr_ai1,
        "network": arr_network,
        "hold": arr_hold,
        "api5": arr_api5
    }

    # --- Ghi từng list ra file riêng ---
    for name, data in data_lists.items():
        file_path = os.path.join(output_dir, f"{name}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"=== Ticket {name.upper()} ({len(data)}) ===\n")
            for item in data:
                f.write(f"{item}\n")
        print(f"✅ Đã ghi {len(data)} dòng vào {file_path}")

    print("\n🎉 Hoàn tất ghi toàn bộ file!")
