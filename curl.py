import datetime
from datetime import timezone
import hashlib
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.credentials import Credentials


def upload_to_minio(
    file_path: str,
    bucket: str,
    object_key: str,
    access_key: str,
    secret_key: str,
    region: str,
    endpoint_url: str,
    acl: str = "public-read",
):
    with open(file_path, "rb") as f:
        file_data = f.read()

    content_length = str(len(file_data))
    content_type = "application/octet-stream"

    host = endpoint_url.replace("https://", "").replace("http://", "")
    url = f"{endpoint_url}/{bucket}/{object_key}"

    amz_date = datetime.datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    headers = {
        "Host": host,
        "x-amz-date": amz_date,
        "x-amz-acl": acl,
        "x-amz-content-sha256": hashlib.sha256(file_data).hexdigest(),
        "Content-Type": content_type,
        "Content-Length": content_length,
    }

    credentials = Credentials(access_key, secret_key)
    request = AWSRequest(method="PUT", url=url, data=file_data, headers=headers)
    SigV4Auth(credentials, "s3", region).add_auth(request)

    response = requests.put(url, data=file_data, headers=dict(request.headers))

    if response.status_code in [200, 201]:
        print(f"Upload thành công: {url}")
    else:
        print(f"Upload thất bại ({response.status_code}): {response.text}")

    return response

def generate_signed_curl(
    file_path: str,
    bucket: str,
    object_key: str,
    access_key: str,
    secret_key: str,
    region: str,
    endpoint_url: str,
    acl: str = "public-read",
):
    """
    Sinh ra lệnh cURL có chữ ký AWS Signature V4 hợp lệ
    để upload file lên MinIO (hoặc AWS S3).
    """

    # ===== 1. Đọc file =====
    with open(file_path, "rb") as f:
        file_data = f.read()

    content_length = str(len(file_data))
    content_type = "application/octet-stream"
    host = endpoint_url.replace("https://", "").replace("http://", "")
    url = f"{endpoint_url}/{bucket}/{object_key}"

    # ===== 2. Sinh header & ký AWS4 =====
    amz_date = datetime.datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    payload_hash = hashlib.sha256(file_data).hexdigest()
    headers = {
        "Host": host,
        "x-amz-date": amz_date,
        "x-amz-acl": acl,
        "x-amz-content-sha256": payload_hash,
        "Content-Type": content_type,
        "Content-Length": content_length,
    }

    credentials = Credentials(access_key, secret_key)
    request = AWSRequest(method="PUT", url=url, data=file_data, headers=headers)
    SigV4Auth(credentials, "s3", region).add_auth(request)

    signed_headers = dict(request.headers)

    # ===== 3. Sinh cURL command =====
    curl_parts = [f"curl --location --request PUT '{url}'"]
    for key, value in signed_headers.items():
        curl_parts.append(f"--header '{key}: {value}'")
    curl_parts.append(f"--data-binary '@{file_path}'")

    curl_command = " \\\n  ".join(curl_parts)

    print("\n=== CURL COMMAND (copy vào Postman hoặc terminal) ===\n")
    print(curl_command)
    print("\n=====================================================")

    return curl_command


generate_signed_curl(
    file_path="./error_eaccount_policy.txt",
    bucket="econ-eform-demo",
    object_key="anonymous/20251008/1759901420839_file.txt",
    access_key="DGVcQ504aqm9nkP32GoS",
    secret_key="PgJO79x6hFCb2EIEmI02d8HSAZHXJDjnGCWYHdQp",
    region="sabeco",
    endpoint_url="https://minio-api.sabeco-app.vn"
)


upload_to_minio(
    file_path="./error_eaccount_policy.txt",
    bucket="econ-eform-demo",
    object_key="anonymous/20251008/1759901420839_file.txt",
    access_key="DGVcQ504aqm9nkP32GoS",
    secret_key="PgJO79x6hFCb2EIEmI02d8HSAZHXJDjnGCWYHdQp",
    region="sabeco",
    endpoint_url="https://minio-api.sabeco-app.vn"
)