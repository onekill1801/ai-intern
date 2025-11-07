import asyncio
import aiohttp
import json

API_BASE = "https://eaccount.kyta.fpt.com/services/eintelligent/api/jobs/"
TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aSI6eyJncm91cHNOYW1lIjpbXSwicm9sZXMiOlsxNzk5LDE4NzldLCJncm91cHMiOltdLCJpcEFjY2VzcyI6W10sImxvZ2luIjoiY2hhcGhhbmh2aWVudGVzdEB5b3BtYWlsLmNvbSIsImZvbGRlcklkIjoiMDAwMDYxMDBrdTVtNGYyNXdLQkt5SmlLUDU0IiwiZm9sZGVyUGF0aCI6Ii9zdG9yYWdlLTAxLzU2ODIiLCJkYlN1ZmZpeCI6IjAwMDA2IiwibGFuZ0tleSI6bnVsbCwiY3VzdElkIjo1NjgyLCJvcmdJbiI6Ii81NjgyLzEyMTYwLzEyMTYxIiwiaWQiOjE0MDIzMCwiZW1haWwiOiJjaGFwaGFuaHZpZW50ZXN0QHlvcG1haWwuY29tIn0sInVzZXJfbmFtZSI6ImNoYXBoYW5odmllbnRlc3RAeW9wbWFpbC5jb20iLCJzY29wZSI6WyJvcGVuaWQiXSwiZXhwIjoxNzYyMTY0OTY0LCJpYXQiOjE3NjIxNjMxNjQsImF1dGhvcml0aWVzIjpbIlJPTEVfVVNFUl9SRVNUUklDVCIsIlJPTEVfQ1VTVF9SRVBPUlQiLCJST0xFX1VTRVIiLCJST0xFX0NVU1RfRE9DIiwiUk9MRV9PUkdfQURNSU4iLCJST0xFX0NVU1RfU1RBRkYiLCJST0xFX0NVU1RfVklFV0VSIl0sImp0aSI6IjliOTM2OWM1LTM5ZTktNDMzMC1hYjU2LWViZjRlMDRkZjY3MyIsImNsaWVudF9pZCI6IndlYl9hcHAifQ.U3aCYV7dkWFNpSjT0kKJYtqa4A3B8ZuRhpp_uDCcRZ3I2Z7EZTPWUhqCIqKOa1oJwMwJI_gxtGEKVudPEznpD-o1Ios6zXj_p3EApDLZj_vYYjuM2lm-4FpB50FFz1QjbBowVrNOzIKP8Or8CXq8q8ExjGiG05lSRtPwAFSqyUXp3t17rYJgHmqNhNVHcWB5-ecmIvy4g2dEhOF7pd75ajF-MBDfrBwV0FLt4uF5PoEKARo2KvSLxZK6zfNXkwiSd97QfyG5acHq-MQ4ZMpdZ-K6efxa4X1vx5KXszxAqHUaVSOQDlTuw04LGKX4Zrbcy2Zdug4fr6zJqvMd1vhjxA"   # <-- thay token thật vào đây
JOB_FILE = "job_ids_1.txt"                # file chứa danh sách jobId (mỗi dòng 1 id)
OUTPUT_FILE = "not_done_jobs.txt"              # file ghi job chưa DONE kèm refId
CONCURRENCY = 5                                # số luồng đồng thời


async def fetch_job_status(session, job_id):
    """Gọi API lấy status và refId của từng job."""
    url = f"{API_BASE}{job_id}"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        async with session.get(url, headers=headers) as resp:
            text = await resp.text()
            try:
                data = json.loads(text)
                status = data.get("status")
                ref_id = data.get("refId")  # <-- thêm lấy refId
                print(f"[{resp.status}] Job {job_id}: status={status}, refId={ref_id}")
                return job_id, status, ref_id
            except json.JSONDecodeError:
                print(f"[{resp.status}] Job {job_id}: Không parse được JSON")
                return job_id, None, None
    except Exception as e:
        print(f"[ERR] Job {job_id}: {e}")
        return job_id, None, None


async def worker(job_ids, output_queue):
    """Mỗi worker gọi API cho danh sách job_ids."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_job_status(session, job_id) for job_id in job_ids]
        results = await asyncio.gather(*tasks)
        for job_id, status, ref_id in results:
            if status != "DONE":
                await output_queue.put((job_id, status, ref_id))


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
        for job_id, status, ref_id in not_done_jobs:
            f.write(f"{ref_id}\n")

    print(f"\n✅ Hoàn thành! {len(not_done_jobs)} job chưa DONE được lưu vào {OUTPUT_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
