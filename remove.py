# Đường dẫn đến file gốc
input_file = "du_lieu_khong_trung.txt"
# File sau khi loại bỏ dữ liệu trùng
output_file = "out.txt"

# Đọc file và loại bỏ trùng lặp
with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Sử dụng set để loại bỏ trùng và giữ nguyên thứ tự xuất hiện đầu tiên
unique_lines = list(dict.fromkeys(line.strip() for line in lines))

# Ghi lại vào file mới
with open(output_file, "w", encoding="utf-8") as f:
    for line in unique_lines:
        f.write(line + "\n")

print(f"Đã loại bỏ trùng lặp. Kết quả lưu trong: {output_file}")
