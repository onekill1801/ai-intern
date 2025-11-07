import aiohttp
import asyncio
import json

TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aSI6eyJncm91cHNOYW1lIjpbXSwicm9sZXMiOlsxNzk5LDE4NzldLCJncm91cHMiOltdLCJpcEFjY2VzcyI6W10sImxvZ2luIjoiY2hhcGhhbmh2aWVudGVzdEB5b3BtYWlsLmNvbSIsImZvbGRlcklkIjoiMDAwMDYxMDBrdTVtNGYyNXdLQkt5SmlLUDU0IiwiZm9sZGVyUGF0aCI6Ii9zdG9yYWdlLTAxLzU2ODIiLCJkYlN1ZmZpeCI6IjAwMDA2IiwibGFuZ0tleSI6bnVsbCwiY3VzdElkIjo1NjgyLCJvcmdJbiI6Ii81NjgyLzEyMTYwLzEyMTYxIiwiaWQiOjE0MDIzMCwiZW1haWwiOiJjaGFwaGFuaHZpZW50ZXN0QHlvcG1haWwuY29tIn0sInVzZXJfbmFtZSI6ImNoYXBoYW5odmllbnRlc3RAeW9wbWFpbC5jb20iLCJzY29wZSI6WyJvcGVuaWQiXSwiZXhwIjoxNzYyMTY2NDQwLCJpYXQiOjE3NjIxNjQ2NDAsImF1dGhvcml0aWVzIjpbIlJPTEVfVVNFUl9SRVNUUklDVCIsIlJPTEVfQ1VTVF9SRVBPUlQiLCJST0xFX1VTRVIiLCJST0xFX0NVU1RfRE9DIiwiUk9MRV9PUkdfQURNSU4iLCJST0xFX0NVU1RfU1RBRkYiLCJST0xFX0NVU1RfVklFV0VSIl0sImp0aSI6ImQyNjY1OThhLTVlNmItNGRiMy04NzA5LTVmNjA5ZDY2NzAzMSIsImNsaWVudF9pZCI6IndlYl9hcHAifQ.gmU8VeX4f1Ty9-kLE2UT0f6lmZAiG-hRhAVM_yIY9PDiaG15nypACdas9as-1--P4QYYke5MHE03V9XCMc2PYk0Cl6urs1zYlq7cpervTMFzQ4ZXw5Jt9nkJ8lYTm2sWlN8omfMbaj17b7_n4Rq9yk2DNFiKsHPrA746Ow-g1NBHUI-9HM3I6rrPsHDLG-oHG9eZI6b4DnWYw60AHm18aq5FcuVY7gXcXtSFCj3OvBhkflF98Lgu-Co61cUODG_DXpVLS3DiefziPMkd4ICYNHGVdbzNMhH2m-9relfznTkMiDR-uC8Yd1lxPsbaKN0Jmv_2Ot53H8tTk6XH8Yp18g"  # <-- Thay token thật
TICKET_FILE = "tickets.txt"

API_BASE = "https://erequest.kyta.fpt.com/services/erequest/api"

# ======== HÀM GỌI CHUNG =========
async def call_api(session, method, url, json_data=None):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    try:
        async with session.request(method, url, headers=headers, json=json_data) as resp:
            text = await resp.text()
            try:
                data = json.loads(text) if text else None
            except json.JSONDecodeError:
                data = None
            print(f"[{resp.status}] {method} {url}")
            return resp.status, data
    except Exception as e:
        print(f"❌ Error calling {url}: {e}")
        return None, None


# ======== CÁC HÀM XỬ LÝ LOGIC =========
async def handle_ticket(session, ticket_id):
    print(f"\n🎟️ Đang xử lý ticketId = {ticket_id}")
    
    # --- 1. GỌI API 1 ---
    url1 = f"{API_BASE}/ticket-recipients/statusRaw/{ticket_id}"
    status1, data1 = await call_api(session, "GET", url1)
    if not data1:
        print("⚠️ Không lấy được dữ liệu từ API1")
        return
    
    chosen_obj = None

    # --- Tìm "AI 1 + AI 2" ---
    for obj in data1:
        if "AI 1 + AI 2" in obj.get("name", ""):
            if obj.get("implementerId") is None:
                chosen_obj = obj
                break
            else:
                # Nếu AI 1 + 2 đã có implementerId, thử tìm AI3
                for o2 in data1:
                    if "AI3: Tổng hợp các khoản thi hành án" in o2.get("name", "") and o2.get("implementerId") is None:
                        chosen_obj = o2
                        break
                break

    if not chosen_obj:
        print("⚠️ Không tìm thấy đối tượng hợp lệ trong API1")
        return

    obj_id = chosen_obj.get("id")
    print(f"✅ Chọn object id={obj_id} từ API1")

    # --- 2. GỌI API 2 ---
    url2 = f"{API_BASE}/ai-response-content/getAiResponseActive/{ticket_id}/{obj_id}"
    status2, data2 = await call_api(session, "GET", url2)

    if not data2:
        print("⚠️ Không có dữ liệu API2 → gọi API4")
        await recall_ticket(session, ticket_id, obj_id)
        return

    status_field = data2.get("status")
    output_field = data2.get("output")

    if status_field == "DONE":
        print("✅ DONE → Dừng.")
        return

    if status_field == "ERROR":
        error_id = data2.get("id")
        if error_id:
            print(f"⚠️ ERROR → Gọi API3 xoá id={error_id}")
            await delete_ai_response(session, ticket_id, obj_id, error_id)
        return

    # status hoặc output không có → recall
    if not status_field or not output_field:
        print("⚠️ Chưa có status hoặc output → Gọi API4")
        await recall_ticket(session, ticket_id, obj_id)
        return


async def delete_ai_response(session, ticket_id, obj_id, error_id):
    url3 = f"{API_BASE}/ai-response-contents/{error_id}"
    status3, _ = await call_api(session, "DELETE", url3)
    if status3 == 204:
        print("🗑️ Xoá thành công → recall OCR")
        await recall_ticket(session, ticket_id, obj_id)
    else:
        print("❌ Xoá thất bại hoặc không trả về 204")


async def recall_ticket(session, ticket_id, obj_id):
    url4 = f"{API_BASE}/ai-response-content/recallOcrTicket/{ticket_id}/{obj_id}"
    await call_api(session, "POST", url4)
    print("🔄 Đã recall OCR ticket")


# ======== CHƯƠNG TRÌNH CHÍNH =========
async def main():
    async with aiohttp.ClientSession() as session:
        with open(TICKET_FILE, "r", encoding="utf-8") as f:
            ticket_ids = [line.strip() for line in f if line.strip()]

        for ticket_id in ticket_ids:
            await handle_ticket(session, ticket_id)


if __name__ == "__main__":
    asyncio.run(main())
