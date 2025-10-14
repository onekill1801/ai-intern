import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = "https://kyta.fpt.com/bldt/services/egenid/api/incr/e-qdtha"
PARAMS = {
    "agencyCode": "dangnd4",
    "documentType": "test"
}
HEADERS = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aSI6eyJncm91cHNOYW1lIjpbIkFETUlOIiwia3l0YS5mcHQuZGVtb0BnbWFpbC5jb20iXSwicm9sZXMiOltdLCJncm91cHMiOlsxMTQ3NywxNDY3NV0sImlwQWNjZXNzIjpbXSwibG9naW4iOiJreXRhLmZwdC5kZW1vQGdtYWlsLmNvbSIsImZvbGRlcklkIjoiMDAwMDYxN244SFE1WFRiRGI1NlhxbVRCZDBhIiwiZm9sZGVyUGF0aCI6Ii9zdG9yYWdlLTAxLzU2ODIiLCJkYlN1ZmZpeCI6IjAwMDA2IiwibGFuZ0tleSI6InZpIiwiY3VzdElkIjo1NjgyLCJvcmdJbiI6Ii81NjgyLzEyMTYwIiwiaWQiOjE0MDIwMCwiZW1haWwiOiJreXRhLmZwdC5kZW1vQGdtYWlsLmNvbSJ9LCJ1c2VyX25hbWUiOiJreXRhLmZwdC5kZW1vQGdtYWlsLmNvbSIsInNjb3BlIjpbIm9wZW5pZCJdLCJleHAiOjE3NjAwMTg0MjcsImlhdCI6MTc2MDAxNjYyNywiYXV0aG9yaXRpZXMiOlsiUk9MRV9PUkdfQ0hBTUVMRU9OIiwiUk9MRV9DVVNUX0RPQyIsIlJPTEVfT1JHX0FETUlOIiwiUk9MRV9VU0VSIl0sImp0aSI6IjI5YTUyZDkxLWVmZjEtNDg4OS04MjRkLTVhYTFmZDkzMDNlMyIsImNsaWVudF9pZCI6IndlYl9hcHAifQ.HmvuuSEGIYUK9JWNzUIfi6iKNQc-zNihcruBXNSHohMgKI7n_Giu2v12VisASoKL0jyiZEIUJ_Mmn2j6X6dMMD6KQ0Ayiw4rW6vAi1jAX-XZwVrS7WIfPuADvpRgKM8RsHkKdMSRgEuKxZwluK0lks7hZJyeb9b6TSaTHHNcizEpxi8C3tECSbFtknD61nTY_kt7ZXc86WGmb1CBimhYyPuJxZDYHtpOjOHnDW9QogNe16E_MM_xip-e6TEwP5BH4r2tRGs3tXRbZgUCXBbeJFq7PtXFYbVN6To_rZm9RM5fMCpcg0KpJ5VTsqEVXbDEjmgaRLVLJZ3MLp-_lFa2wQ"
}

def call_once(i):
    """Gọi API 1 lần và trả về kết quả"""
    try:
        r = requests.get(URL, headers=HEADERS, params=PARAMS, timeout=5)
        return (i, r.status_code, r.text.strip())
    except Exception as e:
        return (i, "ERROR", str(e))

def main():
    total_requests = 1000
    concurrency = 20  # số request chạy song song

    results = []
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(call_once, i) for i in range(1, total_requests + 1)]
        for f in as_completed(futures):
            i, status, result = f.result()
            print(f"[{i:04d}] {status} -> {result}")
            results.append((i, status, result))

    # Tổng kết
    ok = sum(1 for _, s, _ in results if s == 200)
    print(f"\n✅ Hoàn tất {total_requests} lần gọi, thành công {ok} lần.")

if __name__ == "__main__":
    main()
