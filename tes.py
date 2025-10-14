import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = "https://kyta.fpt.com/bldt/services/egenid/api/incr/e-qdtha"
HEADERS = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aSI6eyJncm91cHNOYW1lIjpbIkFETUlOIiwia3l0YS5mcHQuZGVtb0BnbWFpbC5jb20iXSwicm9sZXMiOltdLCJncm91cHMiOlsxMTQ3NywxNDY3NV0sImlwQWNjZXNzIjpbXSwibG9naW4iOiJreXRhLmZwdC5kZW1vQGdtYWlsLmNvbSIsImZvbGRlcklkIjoiMDAwMDYxN244SFE1WFRiRGI1NlhxbVRCZDBhIiwiZm9sZGVyUGF0aCI6Ii9zdG9yYWdlLTAxLzU2ODIiLCJkYlN1ZmZpeCI6IjAwMDA2IiwibGFuZ0tleSI6InZpIiwiY3VzdElkIjo1NjgyLCJvcmdJbiI6Ii81NjgyLzEyMTYwIiwiaWQiOjE0MDIwMCwiZW1haWwiOiJreXRhLmZwdC5kZW1vQGdtYWlsLmNvbSJ9LCJ1c2VyX25hbWUiOiJreXRhLmZwdC5kZW1vQGdtYWlsLmNvbSIsInNjb3BlIjpbIm9wZW5pZCJdLCJleHAiOjE3NjAwMTg0MjcsImlhdCI6MTc2MDAxNjYyNywiYXV0aG9yaXRpZXMiOlsiUk9MRV9PUkdfQ0hBTUVMRU9OIiwiUk9MRV9DVVNUX0RPQyIsIlJPTEVfT1JHX0FETUlOIiwiUk9MRV9VU0VSIl0sImp0aSI6IjI5YTUyZDkxLWVmZjEtNDg4OS04MjRkLTVhYTFmZDkzMDNlMyIsImNsaWVudF9pZCI6IndlYl9hcHAifQ.HmvuuSEGIYUK9JWNzUIfi6iKNQc-zNihcruBXNSHohMgKI7n_Giu2v12VisASoKL0jyiZEIUJ_Mmn2j6X6dMMD6KQ0Ayiw4rW6vAi1jAX-XZwVrS7WIfPuADvpRgKM8RsHkKdMSRgEuKxZwluK0lks7hZJyeb9b6TSaTHHNcizEpxi8C3tECSbFtknD61nTY_kt7ZXc86WGmb1CBimhYyPuJxZDYHtpOjOHnDW9QogNe16E_MM_xip-e6TEwP5BH4r2tRGs3tXRbZgUCXBbeJFq7PtXFYbVN6To_rZm9RM5fMCpcg0KpJ5VTsqEVXbDEjmgaRLVLJZ3MLp-_lFa2wQ"
}

# ✅ Danh sách tham số khác nhau cho từng request
PARAM_LIST = [
    {"agencyCode": "dangnd4", "documentType": "test"},
    {"agencyCode": "dangnd5", "documentType": "test"},
    {"agencyCode": "dangnd6", "documentType": "test"},
]

def call_api(i, params):
    """Gọi API với param cụ thể"""
    try:
        r = requests.get(URL, headers=HEADERS, params=params, timeout=5)
        return (i, params, r.status_code, r.text.strip())
    except Exception as e:
        return (i, params, "ERROR", str(e))

def main():
    concurrency = 20  # Số request chạy song song
    results = []

    # Tạo nhiều request (mỗi param gọi 10 lần để test)
    jobs = []
    for repeat in range(1000):
        for p in PARAM_LIST:
            jobs.append(p)

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(call_api, i, p) for i, p in enumerate(jobs, 1)]
        for f in as_completed(futures):
            i, params, status, result = f.result()
            print(f"[{i:04d}] {status} {params} -> {result}")
            results.append((i, params, status, result))

    ok = sum(1 for _, _, s, _ in results if s == 200)
    print(f"\n✅ Tổng cộng {len(results)} request, thành công {ok}.")

if __name__ == "__main__":
    main()
