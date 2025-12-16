import requests

session = requests.Session()

url = "https://www.moj.gov.vn/UserControls/JpegImage.aspx"
resp = session.get(url)

# Lưu ảnh captcha
with open("captcha.jpg", "wb") as f:
    f.write(resp.content)

# Lấy cookie
print(session.cookies.get_dict())

