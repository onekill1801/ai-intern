import cv2
import pytesseract

img = cv2.imread("captcha.jpg")

# 1️⃣ Chuyển xám
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2️⃣ Giảm noise
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# 3️⃣ Threshold kiểu OTSU (tốt hơn adaptive cho ảnh này)
_, thresh = cv2.threshold(
    blur, 0, 255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

# 4️⃣ Morphology: nối nét chữ
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# 5️⃣ OCR
text = pytesseract.image_to_string(
    thresh,
    config="--psm 6 -c tessedit_char_whitelist=0123456789"
)

print("OCR:", text.strip())
