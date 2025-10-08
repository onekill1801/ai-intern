import datetime
import hashlib
import os
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
    """
    Upload file lên MinIO (hoặc AWS S3 compatible) với chữ ký AWS Signature V4 tự sinh.
    """

    # ====== 1. Chuẩn bị dữ liệu ======
    with open(file_path, "rb") as f:
        file_data = f.read()

    content_length = str(len(file_data))
    content_type = "application/octet-stream"

    # endpoint (vd: https://minio-api.sabeco-app.vn)
    host = endpoint_url.replace("https://", "").replace("http://", "")

    # URL đầy đủ của object
    url = f"{endpoint_url}/{bucket}/{object_key}"

    # ====== 2. Tạo headers cơ bản ======
    amz_date = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    headers = {
        "Host": host,
        "x-amz-date": amz_date,
        "x-amz-acl": acl,
        "x-amz-content-sha256": hashlib.sha256(file_data).hexdigest(),
        "Content-Type": content_type,
        "Content-Length": content_length,
    }

    # ====== 3. Tạo request và ký AWS4 ======
    credentials = Credentials(access_key, secret_key)
    request = AWSRequest(method="PUT", url=url, data=file_data, headers=headers)
    SigV4Auth(credentials, "s3", region).add_auth(request)

    # ====== 4. Gửi request ======
    response = requests.put(url, data=file_data, headers=dict(request.headers))

    # ====== 5. Kiểm tra kết quả ======
    if response.status_code in [200, 201]:
        print(f"Upload thành công: {url}")
    else:
        print(f"Upload failed ({response.status_code}): {response.text}")

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
        "x-amz-content-sha256": "UNSIGNED-PAYLOAD",
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

    print("\n=== CURL COMMAND (copy vao Postman or terminal) ===\n")
    print(curl_command)
    print("\n=====================================================")

    return curl_command
