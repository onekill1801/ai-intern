from dotenv import load_dotenv
import os
import asyncio
import aiohttp
import time

load_dotenv() 

API_BASE = "https://eaccount.kyta.fpt.com/services/eintelligent/api/job-steps-asyncs/retry/"
# API_BASE = "https://eaccount.kyta.fpt.com/services/eintelligent/api/job-steps/retry/"
TOKEN = os.getenv("EREQUEST_TOKEN")
JOB_FILE = "job_ids_1.txt"  # file chứa danh sách jobId (mỗi dòng 1 ID)
BATCH_SIZE = 5            # số job xử lý mỗi đợt
DELAY_SECONDS = 20        # thời gian nghỉ giữa các đợt (20 giây)


async def call_api(session, job_id):
    url = f"{API_BASE}{job_id}"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        async with session.get(url, headers=headers) as resp:
            text = await resp.text()
            print(f"[{resp.status}] Job {job_id}: {text[:100]}")
    except Exception as e:
        print(f"[ERR] Job {job_id}: {e}")


async def process_batch(session, batch):
    tasks = [call_api(session, job_id) for job_id in batch]
    await asyncio.gather(*tasks)


async def main():
    # Đọc danh sách job_id từ file
    with open(JOB_FILE, "r", encoding="utf-8") as f:
        job_ids = [line.strip() for line in f if line.strip()]

    async with aiohttp.ClientSession() as session:
        for i in range(0, len(job_ids), BATCH_SIZE):
            batch = job_ids[i:i + BATCH_SIZE]
            print(f"\n=== Đang xử lý batch {i//BATCH_SIZE + 1}: {batch} ===")
            await process_batch(session, batch)

            # Nếu chưa hết file thì chờ 20 giây
            if i + BATCH_SIZE < len(job_ids):
                print(f"⏳ Chờ {DELAY_SECONDS} giây trước batch tiếp theo...\n")
                await asyncio.sleep(DELAY_SECONDS)

    print("\n✅ Hoàn thành toàn bộ job!")


if __name__ == "__main__":
    asyncio.run(main())
