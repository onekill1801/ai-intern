
import requests

url = "https://www.moj.gov.vn/UserControls/BinhChon/pAction.aspx?sukienID=204&MaCapCha=03199"

session_id = "xzw1nc3ap2fbuepgcrpto2vk"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": f"""
        _gid=GA1.3.1345235290.1765784934;
        _gtpk_testcookie..undefined=1;
        _gtpk_testcookie.241.38c1=1;
        ASP.NET_SessionId={session_id}
    """.replace("\n", "").replace(" ", "")
}

response = requests.post(url, headers=headers)

print("Status code:", response.status_code)
print("Response text:", response.text)
