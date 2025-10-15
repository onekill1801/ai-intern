# === 1️⃣ Tên file nguồn ===
file1 = "id_list.txt"
file2 = "done.log"

# # === 2️⃣ Đọc danh sách ID từ hai file ===
# with open(file1, "r", encoding="utf-8") as f1:
#     ids1 = set(line.strip() for line in f1 if line.strip())

# with open(file2, "r", encoding="utf-8") as f2:
#     ids2 = set(line.strip() for line in f2 if line.strip())

# # === 3️⃣ Tìm phần không giống nhau ===
# # Những ID chỉ có ở file1 hoặc chỉ có ở file2
# diff_ids = ids1.symmetric_difference(ids2)

# # === 4️⃣ Xuất kết quả ra file mới ===
# output_file = "id_diff.txt"
# with open(output_file, "w", encoding="utf-8") as f:
#     for _id in sorted(diff_ids):
#         f.write(_id + "\n")

# print(f"✅ Đã tìm thấy {len(diff_ids)} ID khác nhau.")
# print(f"📄 Kết quả lưu tại: {output_file}")


# === 1️⃣ Đường dẫn tới 2 file ID ===

# === 2️⃣ Đọc ID từ mỗi file ===
with open(file1, "r", encoding="utf-8") as f1:
    ids1 = set(line.strip() for line in f1 if line.strip())

with open(file2, "r", encoding="utf-8") as f2:
    ids2 = set(line.strip() for line in f2 if line.strip())

# === 3️⃣ Tìm ID có trong file2 nhưng không có trong file1 ===
only_in_file2 = ids2 - ids1

# === 4️⃣ Ghi kết quả ra file mới ===
output_file = "id_only_in_file2.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for _id in sorted(only_in_file2):
        f.write(_id + "\n")

print(f"✅ Có {len(only_in_file2)} ID chỉ có trong file2 (không có trong file1).")
print(f"📄 Kết quả đã lưu tại: {output_file}")