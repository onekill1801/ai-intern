import asyncio
import aiohttp

API_BASE = "https://eaccount.kyta.fpt.com/services/eintelligent/api/job-steps-asyncs/retry/"
TOKEN = ""  # <-- Dán token thật của bạn ở đây
JOB_FILE = "job_ids_1.txt"  # file chứa danh sách jobId, mỗi dòng 1 id
MAX_CONCURRENT = 3  # số luồng chạy song song


async def call_api(session, job_id):
    url = f"{API_BASE}{job_id}"
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    try:
        async with session.get(url, headers=headers) as resp:
            text = await resp.text()
            print(f"[{resp.status}] Job {job_id}: {text[:100]}")  # in 100 ký tự đầu
    except Exception as e:
        print(f"[ERR] Job {job_id}: {e}")


async def main():
    # Đọc danh sách job_id từ file
    with open(JOB_FILE, "r", encoding="utf-8") as f:
        job_ids = [line.strip() for line in f if line.strip()]

    conn = aiohttp.TCPConnector(limit=MAX_CONCURRENT)
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = [call_api(session, job_id) for job_id in job_ids]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
