import easyocr
import cv2

reader = easyocr.Reader(['en'], gpu=False)

img = cv2.imread("captcha.jpg")

results = reader.readtext(
    img,
    allowlist='0123456789',
    detail=0
)

print("OCR:", results)
