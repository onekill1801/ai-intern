import json

# Đọc dữ liệu JSON từ file
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Lọc ra những job có retryCount == 5 (ở cấp ngoài)
job_ids = [
    job["jobId"]
    for job in data
    if isinstance(job, dict) and job.get("retryCount") == 5
]

# Ghi ra file
with open("job_step_id.txt", "w", encoding="utf-8") as f:
    for job_id in job_ids:
        f.write(str(job_id) + "\n")

print(f"✅ Đã lưu {len(job_ids)} jobId (retryCount=5) vào file job_step_id.txt")
