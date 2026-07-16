# S3 Integration with FastAPI

## Table of Contents
1. [Boto3 with FastAPI](#boto3-with-fastapi)
2. [Async S3 (aioboto3)](#async-s3-aioboto3)
3. [Presigned URLs](#presigned-urls)
4. [File Upload to S3](#file-upload-to-s3)
5. [Multipart Upload](#multipart-upload)
6. [S3 Event Notifications](#s3-event-notifications)
7. [MinIO for Local Dev](#minio-for-local-dev)
8. [Best Practices](#best-practices)
9. [Interview Questions](#interview-questions)

---

## Boto3 with FastAPI

### Basic Setup

```python
import boto3
from fastapi import FastAPI
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: str

    class Config:
        env_file = ".env"

settings = Settings()

app = FastAPI()

def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )

@app.on_event("startup")
async def startup():
    app.state.s3 = get_s3_client()

@app.get("/buckets")
async def list_buckets():
    s3 = app.state.s3
    response = s3.list_buckets()
    return {"buckets": [b["Name"] for b in response["Buckets"]]}
```

### Dependency Injection

```python
from fastapi import Depends

async def get_s3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )
    try:
        yield s3
    finally:
        s3.close()

@app.get("/files")
async def list_files(s3 = Depends(get_s3)):
    response = s3.list_objects_v2(Bucket=settings.S3_BUCKET)
    files = [
        {"key": obj["Key"], "size": obj["Size"]}
        for obj in response.get("Contents", [])
    ]
    return {"files": files}
```

---

## Async S3 (aioboto3)

### Setup

```python
import aioboto3
from fastapi import FastAPI

app = FastAPI()

session = aioboto3.Session()

async def get_async_s3():
    async with session.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    ) as s3:
        yield s3

@app.get("/files")
async def list_files(s3 = Depends(get_async_s3)):
    response = await s3.list_objects_v2(Bucket=settings.S3_BUCKET)
    files = [
        {"key": obj["Key"], "size": obj["Size"]}
        for obj in response.get("Contents", [])
    ]
    return {"files": files}
```

### Async Upload

```python
@app.post("/upload")
async def upload_to_s3(
    file: UploadFile = File(...),
    s3 = Depends(get_async_s3),
):
    content = await file.read()

    await s3.put_object(
        Bucket=settings.S3_BUCKET,
        Key=f"uploads/{file.filename}",
        Body=content,
        ContentType=file.content_type,
    )

    return {"key": f"uploads/{file.filename}"}
```

### Async Download

```python
@app.get("/download/{key:path}")
async def download_from_s3(key: str, s3 = Depends(get_async_s3)):
    response = await s3.get_object(Bucket=settings.S3_BUCKET, Key=key)
    content = await response["Body"].read()

    return Response(
        content=content,
        media_type=response.get("ContentType", "application/octet-stream"),
        headers={
            "Content-Disposition": f'attachment; filename="{key.split("/")[-1]}"'
        },
    )
```

---

## Presigned URLs

### Generate Upload URL

```python
@app.get("/presigned-upload")
async def get_upload_url(
    filename: str,
    content_type: str,
    s3 = Depends(get_s3),
):
    key = f"uploads/{uuid.uuid4()}/{filename}"

    presigned_url = s3.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": settings.S3_BUCKET,
            "Key": key,
            "ContentType": content_type,
        },
        ExpiresIn=3600,  # 1 hour
    )

    return {"upload_url": presigned_url, "key": key}
```

### Generate Download URL

```python
@app.get("/presigned-download/{key:path}")
async def get_download_url(key: str, s3 = Depends(get_s3)):
    presigned_url = s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.S3_BUCKET,
            "Key": key,
        },
        ExpiresIn=3600,
    )

    return {"download_url": presigned_url}
```

### Generate Multiple Presigned URLs

```python
@app.post("/presigned-urls")
async def get_multiple_presigned_urls(
    files: list[dict],
    s3 = Depends(get_s3),
):
    urls = []
    for file_info in files:
        key = f"uploads/{uuid.uuid4()}/{file_info['filename']}"

        url = s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": settings.S3_BUCKET,
                "Key": key,
                "ContentType": file_info["content_type"],
            },
            ExpiresIn=3600,
        )

        urls.append({
            "filename": file_info["filename"],
            "upload_url": url,
            "key": key,
        })

    return {"urls": urls}
```

### Presigned Post (Browser Upload)

```python
@app.post("/presigned-post")
async def create_presigned_post(
    filename: str,
    content_type: str,
    s3 = Depends(get_s3),
):
    key = f"uploads/{uuid.uuid4()}/{filename}"

    presigned_post = s3.generate_presigned_post(
        Bucket=settings.S3_BUCKET,
        Key=key,
        Fields={"Content-Type": content_type},
        Conditions=[
            {"Content-Type": content_type},
            ["content-length-range", 1, 10 * 1024 * 1024],  # 10MB max
        ],
        ExpiresIn=3600,
    )

    return {
        "url": presigned_post["url"],
        "fields": presigned_post["fields"],
        "key": key,
    }
```

---

## File Upload to S3

### Direct Upload

```python
@app.post("/upload/direct")
async def upload_direct(
    file: UploadFile = File(...),
    s3 = Depends(get_s3),
):
    content = await file.read()

    s3.put_object(
        Bucket=settings.S3_BUCKET,
        Key=f"uploads/{file.filename}",
        Body=content,
        ContentType=file.content_type,
    )

    return {"key": f"uploads/{file.filename}"}
```

### Streaming Upload

```python
@app.post("/upload/streaming")
async def upload_streaming(
    file: UploadFile = File(...),
    s3 = Depends(get_s3),
):
    key = f"uploads/{file.filename}"

    # Upload in chunks
    chunk_size = 5 * 1024 * 1024  # 5MB
    content = await file.read()

    if len(content) <= chunk_size:
        # Small file, direct upload
        s3.put_object(
            Bucket=settings.S3_BUCKET,
            Key=key,
            Body=content,
            ContentType=file.content_type,
        )
    else:
        # Large file, multipart upload
        multipart = s3.create_multipart_upload(
            Bucket=settings.S3_BUCKET,
            Key=key,
            ContentType=file.content_type,
        )

        parts = []
        for i in range(0, len(content), chunk_size):
            chunk = content[i:i + chunk_size]
            part = s3.upload_part(
                Bucket=settings.S3_BUCKET,
                Key=key,
                PartNumber=len(parts) + 1,
                UploadId=multipart["UploadId"],
                Body=chunk,
            )
            parts.append({"PartNumber": len(parts) + 1, "ETag": part["ETag"]})

        s3.complete_multipart_upload(
            Bucket=settings.S3_BUCKET,
            Key=key,
            UploadId=multipart["UploadId"],
            MultipartUpload={"Parts": parts},
        )

    return {"key": key}
```

### Upload with Metadata

```python
@app.post("/upload/metadata")
async def upload_with_metadata(
    file: UploadFile = File(...),
    user_id: int = Form(...),
    description: str = Form(None),
    s3 = Depends(get_s3),
):
    content = await file.read()
    key = f"uploads/{user_id}/{file.filename}"

    metadata = {
        "user-id": str(user_id),
        "original-name": file.filename,
    }
    if description:
        metadata["description"] = description

    s3.put_object(
        Bucket=settings.S3_BUCKET,
        Key=key,
        Body=content,
        ContentType=file.content_type,
        Metadata=metadata,
    )

    return {"key": key, "metadata": metadata}
```

---

## Multipart Upload

### Complete Multipart Upload Implementation

```python
class MultipartUploadManager:
    def __init__(self, s3_client, bucket: str):
        self.s3 = s3_client
        self.bucket = bucket

    async def initiate(self, key: str, content_type: str) -> dict:
        response = self.s3.create_multipart_upload(
            Bucket=self.bucket,
            Key=key,
            ContentType=content_type,
        )
        return {
            "upload_id": response["UploadId"],
            "key": key,
        }

    async def upload_part(
        self,
        key: str,
        upload_id: str,
        part_number: int,
        data: bytes,
    ) -> dict:
        response = self.s3.upload_part(
            Bucket=self.bucket,
            Key=key,
            PartNumber=part_number,
            UploadId=upload_id,
            Body=data,
        )
        return {
            "part_number": part_number,
            "etag": response["ETag"],
        }

    async def complete(
        self,
        key: str,
        upload_id: str,
        parts: list[dict],
    ):
        self.s3.complete_multipart_upload(
            Bucket=self.bucket,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={
                "Parts": [
                    {"PartNumber": p["part_number"], "ETag": p["etag"]}
                    for p in parts
                ]
            },
        )

    async def abort(self, key: str, upload_id: str):
        self.s3.abort_multipart_upload(
            Bucket=self.bucket,
            Key=key,
            UploadId=upload_id,
        )
```

---

## S3 Event Notifications

### Configure S3 Events

```python
# S3 can send events to SQS, SNS, or Lambda when objects are created/deleted

# Example: Notify when file is uploaded
import json
import boto3

def configure_s3_events():
    s3 = boto3.client("s3")

    s3.put_bucket_notification_configuration(
        Bucket=settings.S3_BUCKET,
        NotificationConfiguration={
            "QueueConfigurations": [
                {
                    "QueueArn": "arn:aws:sqs:us-east-1:123456789:upload-queue",
                    "Events": ["s3:ObjectCreated:*"],
                    "Filter": {
                        "Key": {
                            "FilterRules": [
                                {"Name": "prefix", "Value": "uploads/"}
                            ]
                        }
                    },
                }
            ]
        },
    )
```

### Process S3 Events

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/s3-events")
async def handle_s3_events(request: Request):
    body = await request.json()

    for record in body.get("Records", []):
        event_name = record["eventName"]
        key = record["s3"]["object"]["key"]
        bucket = record["s3"]["bucket"]["name"]

        if event_name.startswith("ObjectCreated"):
            # Process new file
            await process_new_file(bucket, key)
        elif event_name.startswith("ObjectRemoved"):
            # Process deleted file
            await process_deleted_file(bucket, key)

    return {"status": "processed"}
```

---

## MinIO for Local Dev

### Docker Setup

```yaml
# docker-compose.yml
services:
  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    ports:
      - "9000:9000"
      - "9001:9001"  # Console
    volumes:
      - minio_data:/data

volumes:
  minio_data:
```

### FastAPI with MinIO

```python
import boto3

# MinIO is S3-compatible
minio_client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
    region_name="us-east-1",
)

# Create bucket
minio_client.create_bucket(Bucket="my-bucket")

@app.post("/upload")
async def upload_to_minio(file: UploadFile = File(...)):
    content = await file.read()

    minio_client.put_object(
        Bucket="my-bucket",
        Key=file.filename,
        Body=content,
        ContentType=file.content_type,
    )

    return {"key": file.filename}
```

### Environment-Based Configuration

```python
class S3Settings(BaseSettings):
    USE_MINIO: bool = False
    MINIO_ENDPOINT: str = "http://localhost:9000"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: str = ""

    def get_s3_client(self):
        if self.USE_MINIO:
            return boto3.client(
                "s3",
                endpoint_url=self.MINIO_ENDPOINT,
                aws_access_key_id="minioadmin",
                aws_secret_access_key="minioadmin",
                region_name="us-east-1",
            )
        return boto3.client(
            "s3",
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
            region_name=self.AWS_REGION,
        )
```

---

## Best Practices

### 1. Use Presigned URLs

```python
# Don't proxy uploads through your server
# Generate presigned URLs for direct browser-to-S3 uploads
```

### 2. Use Async Clients

```python
# Use aioboto3 for non-blocking S3 operations
# Don't block the event loop with boto3
```

### 3. Implement Multipart for Large Files

```python
# Use multipart upload for files > 100MB
# Enable resumable uploads
```

### 4. Set Proper Permissions

```python
# Use IAM roles instead of access keys
# Apply least privilege principle
# Use bucket policies for public access
```

### 5. Use CloudFront for Distribution

```python
# CDN for static assets
# Reduce latency and bandwidth costs
```

### 6. Clean Up Incomplete Multipart Uploads

```python
# Set lifecycle policies to abort incomplete uploads
# Clean up failed uploads regularly
```

---

## Interview Questions

### Q1: How do you integrate S3 with FastAPI?
**Answer:** Use boto3 for sync operations or aioboto3 for async. Create S3 client with credentials, mount as dependency, and use for upload/download operations.

### Q2: What are presigned URLs?
**Answer:** URLs that grant temporary access to S3 objects. Generated server-side with expiration. Allow direct browser-to-S3 uploads/downloads without proxying through the server.

### Q3: When should you use multipart upload?
**Answer:** For files larger than 100MB. Multipart uploads split the file into chunks, enabling parallel uploads, resumability, and better error handling.

### Q4: How do you handle S3 event notifications?
**Answer:** Configure S3 to send events to SQS/SNS/Lambda. Process events in a separate worker. Handle object creation, deletion, and other events.

### Q5: What is MinIO and when should you use it?
**Answer:** MinIO is an S3-compatible object storage server. Use it for local development and testing. Provides the same API as S3 without cloud dependencies.

### Q6: How do you secure S3 access?
**Answer:** Use IAM roles, apply least privilege, use presigned URLs for temporary access, enable bucket versioning, and block public access unless needed.

### Q7: How do you handle large file uploads to S3?
**Answer:** Use presigned URLs for direct browser upload, implement multipart upload for resumability, and stream chunks to avoid memory issues.

### Q8: What is the difference between boto3 and aioboto3?
**Answer:** boto3 is synchronous and blocks the event loop. aioboto3 is async and integrates with asyncio. Use aioboto3 in FastAPI for non-blocking operations.

### Q9: How do you list files in S3?
**Answer:** Use `list_objects_v2` with prefix filtering. Paginate results for large buckets. Return file metadata (key, size, last modified).

### Q10: How do you delete files from S3?
**Answer:** Use `delete_object` for single files, `delete_objects` for batch deletion. Implement lifecycle policies for automatic cleanup.

### Q11: How do you handle S3 errors?
**Answer:** Catch `ClientError`, handle specific error codes (NoSuchKey, AccessDenied), implement retry with exponential backoff, and log errors.

### Q12: How do you store metadata with S3 objects?
**Answer:** Use the `Metadata` parameter in `put_object`. Metadata must be string key-value pairs. Retrieve with `head_object`.

### Q13: How do you copy files within S3?
**Answer:** Use `copy_object` for same-bucket copies. Use `upload_part_copy` for multipart copies of large files.

### Q14: How do you generate download URLs?
**Answer:** Use `generate_presigned_url` with `get_object` action. Set expiration time. Return URL to client for direct download.

### Q15: How do you handle S3 in a serverless FastAPI deployment?
**Answer:** Use IAM roles for credentials. Configure appropriate memory and timeout. Use presigned URLs to minimize data passing through Lambda.

### Q16: How do you version objects in S3?
**Answer:** Enable bucket versioning. S3 automatically versions objects. Use version IDs to retrieve specific versions. Implement lifecycle policies for version cleanup.

### Q17: How do you organize files in S3?
**Answer:** Use prefixes (folders) for organization. Common patterns: `uploads/{user_id}/{filename}`, `dates/{year}/{month}/{day}/{file}`.

### Q18: How do you handle concurrent uploads?
**Answer:** Use unique keys (UUID) to prevent conflicts. Implement multipart upload for large files. Use ETags for conditional uploads.

### Q19: How do you optimize S3 costs?
**Answer:** Use appropriate storage classes, implement lifecycle policies, clean up incomplete multipart uploads, and use CloudFront for caching.

### Q20: How do you test S3 integration?
**Answer:** Use moto for unit tests (mocks S3). Use MinIO for integration tests. Test error scenarios, retries, and edge cases.
