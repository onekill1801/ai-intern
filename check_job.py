import asyncio
import aiohttp
import json

API_BASE = "https://eaccount.kyta.fpt.com/services/eintelligent/api/jobs/"
TOKEN = ""   # <-- thay token thật vào đây
JOB_FILE = "job_failed_ids.txt"                        # file chứa danh sách jobId (mỗi dòng 1 id)
OUTPUT_FILE = "not_done_jobs.txt"               # file ghi job chưa DONE
CONCURRENCY = 5                                 # số luồng đồng thời


async def fetch_job_status(session, job_id):
    """Gọi API lấy status của từng job."""
    url = f"{API_BASE}{job_id}"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        async with session.get(url, headers=headers) as resp:
            text = await resp.text()
            try:
                data = json.loads(text)
                status = data.get("status")
                print(f"[{resp.status}] Job {job_id}: status={status}")
                return job_id, status
            except json.JSONDecodeError:
                print(f"[{resp.status}] Job {job_id}: Không parse được JSON")
                return job_id, None
    except Exception as e:
        print(f"[ERR] Job {job_id}: {e}")
        return job_id, None


async def worker(job_ids, output_queue):
    """Mỗi worker gọi API cho danh sách job_ids."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_job_status(session, job_id) for job_id in job_ids]
        results = await asyncio.gather(*tasks)
        for job_id, status in results:
            if status != "DONE":
                await output_queue.put(job_id)


async def main():
    # Đọc danh sách jobId từ file
    with open(JOB_FILE, "r", encoding="utf-8") as f:
        job_ids = [line.strip() for line in f if line.strip()]

    output_queue = asyncio.Queue()
    not_done_jobs = []

    # Xử lý theo batch (5 job/lần)
    for i in range(0, len(job_ids), CONCURRENCY):
        batch = job_ids[i:i + CONCURRENCY]
        print(f"\n=== Đang kiểm tra batch {i//CONCURRENCY + 1}: {batch} ===")
        await worker(batch, output_queue)

    # Lấy các job chưa DONE
    while not output_queue.empty():
        not_done_jobs.append(await output_queue.get())

    # Ghi ra file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for job_id in not_done_jobs:
            f.write(str(job_id) + "\n")

    print(f"\n✅ Hoàn thành! {len(not_done_jobs)} job chưa DONE được lưu vào {OUTPUT_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
