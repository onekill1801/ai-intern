import json

# Đọc dữ liệu JSON từ file đầu vào
with open('job_step.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Lọc các job có countStep = 3
# filtered_job_ids = [
#     job['jobId']
#     for job in data
#     if job.get('metaData', {}).get('countStep') == 3
# ]

filtered_job_ids = [
    job["id"]
    for job in data
    if job.get("input", {}).get("input", {}).get("agentActionId") != "0000115yIdwUgKlPxrVy"
]

# Ghi các jobId đã lọc ra file riêng
with open('job_ids_step_1.txt', 'w', encoding='utf-8') as f:
    for job_id in filtered_job_ids:
        f.write(str(job_id) + '\n')

print(f"Đã lưu {len(filtered_job_ids)} jobId vào file job_ids.txt")
