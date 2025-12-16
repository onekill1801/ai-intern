import requests

# ================== CONFIG ==================
CAPTCHA_URL = "https://www.moj.gov.vn/UserControls/JpegImage.aspx"
VOTE_URL = "https://www.moj.gov.vn/UserControls/BinhChon/pAction.aspx"

SUKIEN_ID = 204

# ================== MAIN LOOP ==================
while True:
    print("\n=== NEW ROUND ===")

    # 1️⃣ Tạo session mới (cookie mới)
    session = requests.Session()

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # 2️⃣ GET captcha để server set cookie
    resp = session.get(CAPTCHA_URL, headers=headers, timeout=10)

    # 3️⃣ Lưu captcha
    with open("captcha.jpg", "wb") as f:
        f.write(resp.content)

    # 4️⃣ In cookie (debug)
    cookies = session.cookies.get_dict()
    print("Cookies:", cookies)

    session_id = cookies.get("ASP.NET_SessionId")
    print("ASP.NET_SessionId:", session_id)

    # 5️⃣ Chờ user nhập captcha
    captcha_code = input("Nhập mã captcha (hoặc q để thoát): ").strip()
    if captcha_code.lower() == "q":
        break

    # 6️⃣ POST vote (DÙNG CÙNG SESSION)
    params = {
        "sukienID": SUKIEN_ID,
        "MaCapCha": captcha_code
    }

    vote_resp = session.post(
        VOTE_URL,
        params=params,
        headers=headers,
        timeout=10
    )

    print("Vote status:", vote_resp.status_code)
    print("Vote response:", vote_resp.text)

    # 7️⃣ Clear cookie & đóng session
    session.cookies.clear()
    session.close()

    print("Session cleared, ready for next round.")
