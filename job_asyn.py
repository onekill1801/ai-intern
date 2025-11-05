import json

# Đọc dữ liệu JSON từ file
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Lấy toàn bộ jobId
job_ids = [job['jobId'] for job in data]

# Ghi ra file
with open("job_ids_1.txt", "w", encoding="utf-8") as f:
    for job_id in job_ids:
        f.write(str(job_id) + "\n")

print(f"Đã lưu {len(job_ids)} jobId vào file job_ids.txt")
