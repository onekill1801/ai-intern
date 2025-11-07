import asyncio
import aiohttp
import time

# -------- CONFIG --------
API_TEMPLATE = "https://eaccount.kyta.fpt.com/services/eintelligent/api/job-backups/{}"
AUTH_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aSI6eyJncm91cHNOYW1lIjpbXSwicm9sZXMiOlsxNzk5LDE4NzldLCJncm91cHMiOltdLCJpcEFjY2VzcyI6W10sImxvZ2luIjoiY2hhcGhhbmh2aWVudGVzdEB5b3BtYWlsLmNvbSIsImZvbGRlcklkIjoiMDAwMDYxMDBrdTVtNGYyNXdLQkt5SmlLUDU0IiwiZm9sZGVyUGF0aCI6Ii9zdG9yYWdlLTAxLzU2ODIiLCJkYlN1ZmZpeCI6IjAwMDA2IiwibGFuZ0tleSI6bnVsbCwiY3VzdElkIjo1NjgyLCJvcmdJbiI6Ii81NjgyLzEyMTYwLzEyMTYxIiwiaWQiOjE0MDIzMCwiZW1haWwiOiJjaGFwaGFuaHZpZW50ZXN0QHlvcG1haWwuY29tIn0sInVzZXJfbmFtZSI6ImNoYXBoYW5odmllbnRlc3RAeW9wbWFpbC5jb20iLCJzY29wZSI6WyJvcGVuaWQiXSwiZXhwIjoxNzkyMTgxMjA4LCJpYXQiOjE3NjIxNzk0MDgsImF1dGhvcml0aWVzIjpbIlJPTEVfVVNFUl9SRVNUUklDVCIsIlJPTEVfQ1VTVF9SRVBPUlQiLCJST0xFX1VTRVIiLCJST0xFX0NVU1RfRE9DIiwiUk9MRV9PUkdfQURNSU4iLCJST0xFX0NVU1RfU1RBRkYiLCJST0xFX0NVU1RfVklFV0VSIl0sImp0aSI6Ijc1ZjM3OGU3LTZlYWUtNGRkMC1hYTcyLWQxYjk5ZDgwZWUwYiIsImNsaWVudF9pZCI6IndlYl9hcHAifQ.jpLRLZM8K689L4Hnwi9XPzY--KSV0UNKH6FdUDFX2CBjL_lWvkQbcxHNAo9iduV47lO3ImE00r5A_Q8l_ebLt8PDvhE1m8LQGsqBHMOyLV4OkzCSgM-SxFKIMRS_lNI-DKQ1mLA9vMn0vRvFy-gmejE5Jk2iTgTSSkl42Y5P4zrlqxPA_fcxJopvYFHBUBcV0D-1LsIXk2_5m778ywK3u3BP65xc26JeOHjZG-yXlylsTDdvbT-GAmhTpYdo-E1XJ-QELqJ5YK24pDRGlb3YfGJo-gXkzNILZ_wvoNcVVeii9q-dn_Nm5HyUoJy3NyFHrPQZK__cHzeJJzXLWzuR6g"
START_ID = 3635       # m
END_ID = 5737        # n
BATCH_SIZE = 25
DELAY_SECONDS = 1
# ------------------------

headers = {"Authorization": AUTH_TOKEN}


async def call_api(session, job_id):
    url = API_TEMPLATE.format(job_id)
    try:
        async with session.delete(url, headers=headers, timeout=300) as resp:
            text = await resp.text()
            print(f"[{job_id}] ✅ Status {resp.status}")
            return (job_id, resp.status, text)
    except Exception as e:
        print(f"[{job_id}] ❌ Error: {e}")
        return (job_id, None, str(e))


async def process_range():
    async with aiohttp.ClientSession() as session:
        job_ids = list(range(START_ID, END_ID + 1))
        for i in range(0, len(job_ids), BATCH_SIZE):
            batch = job_ids[i:i + BATCH_SIZE]
            print(f"\n🚀 Batch {i // BATCH_SIZE + 1} — IDs: {batch}")
            results = await asyncio.gather(*[call_api(session, jid) for jid in batch])
            # (Optional) Save results, log, etc.
            print(f"⏳ Waiting {DELAY_SECONDS}s before next batch...\n")
            await asyncio.sleep(DELAY_SECONDS)
        print("✅ All jobs done.")


if __name__ == "__main__":
    asyncio.run(process_range())
