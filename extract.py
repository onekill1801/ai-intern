import json

# File đầu vào chứa dữ liệu JSON
input_file = "data_1.json"  # đổi tên file cho phù hợp

# File đầu ra lưu danh sách id
output_file = "ids.txt"

# Đọc file JSON
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Mở file đích ở chế độ append
with open(output_file, "a", encoding="utf-8") as f:
    for item in data:
        id_value = item.get("id")
        if id_value:
            f.write(id_value + "\n")

print("✅ Đã tách và lưu ID vào", output_file)
