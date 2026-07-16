# File Handling Interview Questions

## Table of Contents
1. [File Upload](#file-upload)
2. [UploadFile vs File](#uploadfile-vs-file)
3. [File Size & Limits](#file-size--limits)
4. [S3 Integration & Presigned URLs](#s3-integration--presigned-urls)
5. [Streaming Uploads](#streaming-uploads)
6. [File Validation](#file-validation)
7. [Static Files & CDN](#static-files--cdn)
8. [Image Processing](#image-processing)
9. [File Security](#file-security)
10. [Architecture & Design](#architecture--design)
11. [Scenario-Based](#scenario-based)

---

## File Upload

### Q1: What is UploadFile in FastAPI and how does it work?
**Answer:** UploadFile is a class that provides file upload functionality with streaming capabilities. It uses SpooledTemporaryFile to handle files efficiently — small files are stored in memory, large files are spilled to disk. Attributes include filename, content_type, file (file-like object), and size. Methods include read(), write(), seek(), and close().

```python
@app.post("/upload")
async def upload_file(file: UploadFile):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents), "content_type": file.content_type}
```

### Q2: What is the difference between File() and UploadFile?
**Answer:** File() returns raw bytes loaded entirely into memory — suitable for small files under a few MB. UploadFile returns a file-like object with streaming capabilities — use for large files, files of unknown size, or when you need to process files in chunks.

```python
# File() - loads entire content into memory
@app.post("/small-upload")
async def small_upload(file: bytes = File(...)):
    return {"size": len(file)}

# UploadFile - streaming, memory-efficient
@app.post("/large-upload")
async def large_upload(file: UploadFile):
    while chunk := await file.read(8192):
        process_chunk(chunk)
    return {"filename": file.filename}
```

### Q3: How do you handle multiple file uploads?
**Answer:** Use `list[UploadFile]` or multiple parameters with different field names:

```python
@app.post("/multi-upload")
async def multi_upload(files: list[UploadFile] = File(...)):
    results = []
    for file in files:
        content = await file.read()
        results.append({"filename": file.filename, "size": len(content)})
    return {"files": results}

@app.post("/document-upload")
async def doc_upload(
    avatar: UploadFile = File(...),
    resume: UploadFile = File(...),
    portfolio: UploadFile = File(None),
):
    return {"avatar": avatar.filename, "resume": resume.filename}
```

### Q4: How do you generate unique filenames?
**Answer:** Never use the original filename directly — it can cause path traversal, overwrites, and conflicts:

```python
import uuid
from pathlib import Path

def generate_unique_filename(original_filename: str) -> str:
    ext = Path(original_filename).suffix.lower()
    return f"{uuid.uuid4()}{ext}"

import hashlib

def hash_filename(original_filename: str, content: bytes) -> str:
    ext = Path(original_filename).suffix.lower()
    content_hash = hashlib.sha256(content).hexdigest()[:16]
    return f"{content_hash}{ext}"
```

---

## UploadFile vs File

### Q5: When should you use UploadFile vs File()?
**Answer:**

| Criteria | File() | UploadFile |
|----------|--------|------------|
| Memory usage | Entire file in memory | Streaming, memory-efficient |
| Best for | Small files (< 1MB) | Large files, unknown size |
| Speed | Faster for small files | Better for large files |
| Features | Raw bytes | filename, content_type, seek, etc. |
| Processing | Read all at once | Read in chunks |
| Validation | Basic | Full metadata available |

### Q6: How do you get file metadata with UploadFile?
**Answer:**

```python
@app.post("/upload")
async def upload(file: UploadFile):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size,
        "file_id": file.file.tell(),
    }
```

### Q7: How do you handle UploadFile lifecycle?
**Answer:** UploadFile uses SpooledTemporaryFile which auto-cleans. But always close explicitly in error cases:

```python
@app.post("/upload")
async def upload(file: UploadFile):
    try:
        content = await file.read()
        return {"status": "ok"}
    finally:
        await file.close()
```

---

## File Size & Limits

### Q8: How do you limit file upload size?
**Answer:** Multiple approaches, often combined:

```python
# Approach 1: Check Content-Length in middleware
@app.middleware("http")
async def limit_upload_size(request: Request, call_next):
    if request.method == "POST" and "multipart/form-data" in request.headers.get("content-type", ""):
        content_length = request.headers.get("content-length", 0)
        if int(content_length) > 10 * 1024 * 1024:
            return JSONResponse(status_code=413, content={"detail": "File too large"})
    return await call_next(request)

# Approach 2: Streaming validation
@app.post("/upload")
async def upload(file: UploadFile):
    max_size = 10 * 1024 * 1024
    total = 0
    while chunk := await file.read(8192):
        total += len(chunk)
        if total > max_size:
            raise HTTPException(status_code=413, detail="File too large")
    return {"size": total}
```

### Q9: What are the practical file size limits in FastAPI?
**Answer:** FastAPI/Starlette doesn't impose a default limit. Uvicorn has a default max_body_size. In production, set limits at multiple levels: reverse proxy (Nginx: client_max_body_size), application middleware (Content-Length check), route handler (validate after reading), and streaming validation (check during chunk reads).

### Q10: How do you handle very large file uploads (GB+)?
**Answer:** Use chunked processing and avoid loading the entire file in memory:

```python
@app.post("/large-upload")
async def large_upload(file: UploadFile):
    upload_dir = Path("/uploads")
    file_path = upload_dir / generate_unique_filename(file.filename)

    total_size = 0
    with open(file_path, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            buffer.write(chunk)
            total_size += len(chunk)

    return {"filename": file_path.name, "size": total_size}
```

---

## S3 Integration & Presigned URLs

### Q11: How do you integrate S3 with FastAPI?
**Answer:** Use boto3 for sync or aioboto3 for async operations:

```python
import aioboto3

session = aioboto3.Session()

@app.post("/upload-url")
async def get_upload_url(filename: str):
    async with session.client("s3") as s3:
        presigned_url = await s3.generate_presigned_url(
            "put_object",
            Params={"Bucket": "my-bucket", "Key": f"uploads/{filename}"},
            ExpiresIn=3600,
        )
    return {"upload_url": presigned_url}

@app.post("/upload-direct")
async def upload_direct(file: UploadFile):
    async with session.client("s3") as s3:
        content = await file.read()
        await s3.put_object(
            Bucket="my-bucket",
            Key=f"uploads/{file.filename}",
            Body=content,
        )
    return {"status": "uploaded"}
```

### Q12: What are presigned URLs and when should you use them?
**Answer:** Presigned URLs grant temporary access to S3 objects. Generated server-side with expiration time. Allow direct browser-to-S3 operations without proxying through your server, reducing server load and bandwidth.

Use presigned URLs when:
- Upload directly from browser (bypass server)
- Download files without proxying
- Share files temporarily without making them public
- Large file uploads (resumable with multipart)

### Q13: How do you implement presigned URL generation for uploads?
**Answer:**

```python
@app.post("/presigned-upload")
async def create_presigned_upload(filename: str = Query(...), content_type: str = Query(...)):
    key = f"uploads/{uuid.uuid4()}/{filename}"

    async with session.client("s3") as s3:
        presigned = await s3.generate_presigned_url(
            "put_object",
            Params={"Bucket": settings.S3_BUCKET, "Key": key, "ContentType": content_type},
            ExpiresIn=3600,
        )

    return {"upload_url": presigned, "key": key, "expires_in": 3600}
```

### Q14: How do you handle S3 multipart upload for large files?
**Answer:**

```python
@app.post("/multipart/init")
async def init_multipart_upload(filename: str, content_type: str):
    key = f"uploads/{uuid.uuid4()}/{filename}"
    async with session.client("s3") as s3:
        response = await s3.create_multipart_upload(
            Bucket=settings.S3_BUCKET, Key=key, ContentType=content_type,
        )
    return {"upload_id": response["UploadId"], "key": key}

@app.post("/multipart/presigned-part")
async def get_part_upload_url(upload_id: str, key: str, part_number: int):
    async with session.client("s3") as s3:
        url = await s3.generate_presigned_url(
            "upload_part",
            Params={"Bucket": settings.S3_BUCKET, "Key": key, "UploadId": upload_id, "PartNumber": part_number},
            ExpiresIn=3600,
        )
    return {"url": url, "part_number": part_number}

@app.post("/multipart/complete")
async def complete_multipart(upload_id: str, key: str, parts: list[dict]):
    async with session.client("s3") as s3:
        await s3.complete_multipart_upload(
            Bucket=settings.S3_BUCKET, Key=key, UploadId=upload_id,
            MultipartUpload={"Parts": parts},
        )
    return {"key": key, "status": "complete"}
```

### Q15: How do you secure S3 access?
**Answer:** Use IAM roles with least privilege, presigned URLs for temporary access, block public access, enable bucket versioning, encrypt at rest (SSE-S3/SSE-KMS), encrypt in transit (HTTPS only), and audit access with CloudTrail.

### Q16: What is MinIO and when should you use it?
**Answer:** MinIO is an S3-compatible object storage server for local development and on-premise deployments. Provides the same API as S3 without cloud dependencies. Use for development, testing, and edge deployments where S3 isn't available.

---

## Streaming Uploads

### Q17: How do you stream large file uploads?
**Answer:** Process files in chunks without loading everything into memory:

```python
@app.post("/stream-upload")
async def stream_upload(file: UploadFile):
    chunk_size = 1024 * 1024
    total = 0
    hasher = hashlib.sha256()

    async with aiofiles.open(f"/uploads/{file.filename}", "wb") as f:
        while chunk := await file.read(chunk_size):
            await f.write(chunk)
            hasher.update(chunk)
            total += len(chunk)

    return {"size": total, "hash": hasher.hexdigest()}
```

### Q18: How do you implement streaming to S3?
**Answer:** Use aioboto3's streaming upload:

```python
@app.post("/stream-s3")
async def stream_to_s3(file: UploadFile):
    async with session.client("s3") as s3:
        await s3.put_object(
            Bucket=settings.S3_BUCKET,
            Key=f"uploads/{file.filename}",
            Body=file.file,
        )
    return {"status": "uploaded"}
```

### Q19: How do you implement resumable uploads?
**Answer:** Track upload progress and allow resumption:

```python
@app.post("/resumable/init")
async def init_resumable(filename: str, total_size: int):
    upload_id = str(uuid.uuid4())
    await redis.hset(f"upload:{upload_id}", mapping={
        "filename": filename,
        "total_size": total_size,
        "uploaded_bytes": 0,
        "status": "in_progress",
    })
    return {"upload_id": upload_id}

@app.post("/resumable/chunk/{upload_id}")
async def upload_chunk(upload_id: str, chunk_number: int, file: UploadFile):
    info = await redis.hgetall(f"upload:{upload_id}")
    if not info:
        raise HTTPException(404, "Upload not found")

    chunk = await file.read()
    await store_chunk(upload_id, chunk_number, chunk)

    uploaded = int(info[b"uploaded_bytes"]) + len(chunk)
    await redis.hset(f"upload:{upload_id}", "uploaded_bytes", uploaded)

    return {"uploaded": uploaded, "total": int(info[b"total_size"])}

@app.get("/resumable/status/{upload_id}")
async def get_upload_status(upload_id: str):
    info = await redis.hgetall(f"upload:{upload_id}")
    return {
        "uploaded_bytes": int(info.get(b"uploaded_bytes", 0)),
        "total_size": int(info.get(b"total_size", 0)),
    }
```

---

## File Validation

### Q20: How do you validate file types reliably?
**Answer:** Don't rely solely on filename extension or MIME type (both can be spoofed). Use magic bytes:

```python
import magic

def validate_file_type(file: UploadFile, allowed_types: list[str]) -> bool:
    content = file.read(2048)
    await file.seek(0)

    detected = magic.from_buffer(content, mime=True)
    if detected not in allowed_types:
        return False

    ext = Path(file.filename).suffix.lower()
    type_ext_map = {
        "image/jpeg": [".jpg", ".jpeg"],
        "image/png": [".png"],
        "application/pdf": [".pdf"],
    }
    return ext in type_ext_map.get(detected, [])

@app.post("/upload")
async def upload(file: UploadFile):
    if not validate_file_type(file, ["image/jpeg", "image/png", "application/pdf"]):
        raise HTTPException(400, "Invalid file type")
```

### Q21: How do you validate image dimensions and quality?
**Answer:** Use Pillow to validate image properties:

```python
from PIL import Image
import io

async def validate_image(file: UploadFile, max_width=4096, max_height=4096, max_size_mb=10):
    content = await file.read()
    await file.seek(0)

    if len(content) > max_size_mb * 1024 * 1024:
        raise ValueError(f"Image exceeds {max_size_mb}MB limit")

    try:
        img = Image.open(io.BytesIO(content))
        width, height = img.size

        if width > max_width or height > max_height:
            raise ValueError(f"Image dimensions {width}x{height} exceed {max_width}x{max_height}")

        if img.format not in ["JPEG", "PNG", "WEBP"]:
            raise ValueError(f"Unsupported image format: {img.format}")

        return {"width": width, "height": height, "format": img.format}
    except Exception as e:
        raise ValueError(f"Invalid image: {e}")
```

### Q22: How do you validate file content (not just type)?
**Answer:** Validate the actual content structure:

```python
import csv
import io
import json

async def validate_csv_content(file: UploadFile) -> dict:
    content = await file.read()
    await file.seek(0)

    text = content.decode("utf-8")
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)

    if not rows:
        raise ValueError("CSV is empty")

    headers = rows[0]
    if len(headers) < 2:
        raise ValueError("CSV must have at least 2 columns")

    return {"headers": headers, "row_count": len(rows) - 1}

async def validate_json_content(file: UploadFile) -> dict:
    content = await file.read()
    await file.seek(0)

    try:
        data = json.loads(content)
        return {"valid": True, "type": type(data).__name__}
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")
```

### Q23: How do you implement PDF validation beyond file extension?
**Answer:** Check PDF magic bytes (`%PDF`), use PyPDF2 to validate structure, extract metadata, check page count, and scan for JavaScript:

```python
import PyPDF2

async def validate_pdf(file: UploadFile) -> dict:
    content = await file.read()
    await file.seek(0)

    if not content[:5] == b'%PDF-':
        raise ValueError("Not a valid PDF file")

    reader = PyPDF2.PdfReader(io.BytesIO(content))

    metadata = {
        "pages": len(reader.pages),
        "title": reader.metadata.get("/Title", ""),
        "encrypted": reader.is_encrypted,
    }

    if metadata["encrypted"]:
        raise ValueError("Encrypted PDFs are not allowed")

    # Check for JavaScript
    for page in reader.pages:
        if "/JS" in page or "/JavaScript" in page:
            raise ValueError("PDFs with JavaScript are not allowed")

    return metadata
```

---

## Static Files & CDN

### Q24: How do you serve static files in FastAPI?
**Answer:**

```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/app", StaticFiles(directory="frontend/build", html=True), name="spa")
```

### Q25: Should you serve static files from FastAPI in production?
**Answer:** Generally no. Use Nginx, CDN, or cloud storage. FastAPI should focus on API endpoints. Static file serving adds overhead and bypasses CDN caching. Exception: admin dashboards or small internal tools where simplicity matters.

### Q26: How do you set cache headers for static files?
**Answer:** Create a custom StaticFiles subclass:

```python
from starlette.staticfiles import StaticFiles
from starlette.responses import Response

class CachedStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        if path.endswith(('.js', '.css', '.woff2', '.ttf')):
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        elif path.endswith(('.png', '.jpg', '.gif', '.svg')):
            response.headers["Cache-Control"] = "public, max-age=86400"
        return response

app.mount("/static", CachedStaticFiles(directory="static"), name="static")
```

### Q27: How do you implement cache busting?
**Answer:** Include content hash in filenames during build. Reference in templates with the hashed filename. Set long cache times since filename changes when content changes.

### Q28: How do you implement a CDN for static files?
**Answer:** Use CloudFront (AWS), Cloudflare, or Fastly. Configure origin as S3 bucket or your server. Set cache policies per file type. Use signed URLs for private content. Implement cache invalidation for updates. Use edge locations for global distribution.

---

## Image Processing

### Q29: How do you process uploaded images?
**Answer:** Use Pillow (PIL) for manipulation:

```python
from PIL import Image
import io

@app.post("/resize")
async def resize_image(file: UploadFile, width: int = 800, height: int = 600):
    content = await file.read()
    img = Image.open(io.BytesIO(content))

    img.thumbnail((width, height), Image.Resampling.LANCZOS)

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    buffer.seek(0)

    return Response(content=buffer.read(), media_type="image/jpeg")
```

### Q30: How do you generate thumbnails?
**Answer:**

```python
async def generate_thumbnail(file: UploadFile, size=(200, 200)):
    content = await file.read()
    img = Image.open(io.BytesIO(content))

    img.thumbnail(size, Image.Resampling.LANCZOS)

    if img.mode == "RGBA":
        img = img.convert("RGB")

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=80)
    return buffer.getvalue()
```

### Q31: How do you add watermarks to images?
**Answer:**

```python
from PIL import Image, ImageDraw, ImageFont

def add_watermark(image_bytes: bytes, text: str) -> bytes:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    font = ImageFont.truetype("arial.ttf", 36)
    bbox = draw.textbbox((0, 0), text, font=font)
    txt_width = bbox[2] - bbox[0]
    txt_height = bbox[3] - bbox[1]

    x = img.width - txt_width - 20
    y = img.height - txt_height - 20

    draw.text((x, y), text, font=font, fill=(255, 255, 255, 128))

    result = Image.alpha_composite(img, txt_layer)
    buffer = io.BytesIO()
    result.save(buffer, format="PNG")
    return buffer.getvalue()
```

### Q32: How do you extract image metadata?
**Answer:**

```python
from PIL import Image
from PIL.ExifTags import TAGS

async def extract_metadata(file: UploadFile) -> dict:
    content = await file.read()
    img = Image.open(io.BytesIO(content))

    metadata = {
        "format": img.format,
        "mode": img.mode,
        "size": img.size,
        "info": dict(img.info),
    }

    exif_data = img.getexif()
    if exif_data:
        exif = {}
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            exif[tag] = str(value)
        metadata["exif"] = exif

    return metadata
```

---

## File Security

### Q33: How do you prevent path traversal in file operations?
**Answer:** Never use user-provided filenames directly. Use UUID-based names and validate paths:

```python
import os
from pathlib import Path

def safe_file_path(upload_dir: Path, filename: str) -> Path:
    safe_name = Path(filename).name
    unique_name = f"{uuid.uuid4()}{Path(safe_name).suffix}"
    full_path = upload_dir / unique_name

    resolved = full_path.resolve()
    if not str(resolved).startswith(str(upload_dir.resolve())):
        raise ValueError("Path traversal detected")

    return resolved
```

### Q34: How do you implement virus scanning for uploads?
**Answer:** Use ClamAV via pyclamd:

```python
import pyclamd

cd = pyclamd.ClamdNetworkSocket()

async def scan_file(file: UploadFile) -> bool:
    content = await file.read()
    await file.seek(0)

    result = cd.scan_buffer(content)
    if result:
        logger.warning(f"Virus detected in {file.filename}: {result}")
        return False
    return True

@app.post("/upload")
async def upload(file: UploadFile):
    if not await scan_file(file):
        raise HTTPException(400, "File contains malware")
```

### Q35: How do you prevent file upload DoS attacks?
**Answer:**
- Limit file size (middleware + route validation)
- Rate limit uploads per IP/user
- Limit concurrent uploads
- Validate file type early (reject before processing)
- Clean up temp files on error
- Set upload directory on a separate volume
- Use background tasks for processing (don't block the event loop)
- Set maximum filename length

### Q36: How do you secure file downloads?
**Answer:** Use presigned URLs for temporary access, validate authorization before serving, sanitize file paths, set Content-Disposition headers, and implement access logging.

### Q37: How do you handle sensitive file uploads?
**Answer:** Encrypt at rest (S3 SSE-KMS), use HTTPS for transfer, implement access logging, apply retention policies, consider client-side encryption, and use separate buckets for sensitive data.

---

## Architecture & Design

### Q38: How do you design a file storage abstraction?
**Answer:** Create an interface that works across backends:

```python
from abc import ABC, abstractmethod

class FileStorage(ABC):
    @abstractmethod
    async def upload(self, key: str, data: bytes) -> str:
        pass

    @abstractmethod
    async def download(self, key: str) -> bytes:
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        pass

    @abstractmethod
    async def get_url(self, key: str, expires: int = 3600) -> str:
        pass

class LocalStorage(FileStorage):
    async def upload(self, key, data):
        path = Path(self.base_dir) / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return str(path)

    async def download(self, key):
        return Path(self.base_dir, key).read_bytes()

class S3Storage(FileStorage):
    async def upload(self, key, data):
        async with self.client as s3:
            await s3.put_object(Bucket=self.bucket, Key=key, Body=data)
        return f"s3://{self.bucket}/{key}"

    async def download(self, key):
        async with self.client as s3:
            response = await s3.get_object(Bucket=self.bucket, Key=key)
            return await response["Body"].read()
```

### Q39: How do you handle file uploads in a distributed system?
**Answer:** Use shared storage (S3, NFS, GCS). Store metadata in database. Handle concurrent uploads with unique keys. Implement retry and idempotency. Use presigned URLs for direct browser-to-storage uploads. Process files with background tasks.

### Q40: How do you optimize file upload performance?
**Answer:** Stream chunks, use async I/O, implement resumable uploads, compress before upload, use presigned URLs for direct upload, process in background, and use CDN for distribution.

### Q41: How do you implement file versioning?
**Answer:** Use S3 versioning (automatic), store version metadata in database, implement version comparison, provide rollback capability. Keep N recent versions. Use content-addressable storage for deduplication.

---

## Scenario-Based

### Q42: Design a profile picture upload system.
**Answer:** Accept upload, validate type/size/dimensions, generate multiple sizes (thumbnail, medium, large), store in S3 with UUID naming, update user record in database, invalidate CDN cache for old image, and use presigned URLs for secure access.

```python
@app.post("/profile-picture")
async def upload_profile_picture(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
):
    # Validate
    content = await file.read()
    await file.seek(0)
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(413, "Image too large (max 5MB)")

    img = Image.open(io.BytesIO(content))
    if img.format not in ["JPEG", "PNG", "WEBP"]:
        raise HTTPException(400, "Invalid image format")

    # Generate sizes
    sizes = {"thumbnail": (150, 150), "medium": (400, 400), "large": (800, 800)}
    urls = {}

    for size_name, dimensions in sizes.items():
        resized = img.copy()
        resized.thumbnail(dimensions, Image.Resampling.LANCZOS)

        buffer = io.BytesIO()
        resized.save(buffer, format="JPEG", quality=85)
        buffer.seek(0)

        key = f"profiles/{user.id}/{size_name}.jpg"
        await s3.upload(key, buffer.read())
        urls[size_name] = await s3.get_url(key, expires=3600)

    await db.update(user.id, profile_picture=urls)
    return urls
```

### Q43: How do you implement a document management system?
**Answer:** Accept upload with metadata, validate content type, extract metadata (PDF pages, word count), store in S3, create search index (Elasticsearch), implement versioning, access control per document, audit logging, and preview generation.

### Q44: How do you handle concurrent file uploads to the same path?
**Answer:** Use unique keys (UUID) to prevent conflicts. If overwriting is intended, use optimistic locking (ETags for S3). Implement atomic file operations. For local storage, use file locks or temp files with rename.

### Q45: How do you implement file sharing with access control?
**Answer:** Store access permissions in database. Generate presigned URLs with appropriate permissions. Implement time-limited links. Support public and private sharing. Audit access. Revoke access by invalidating tokens.

### Q46: How do you implement file cleanup and retention?
**Answer:** Implement TTL policies, use lifecycle rules for cloud storage (S3 lifecycle policies), clean up temp files on error, archive old files to cold storage, and schedule regular cleanup tasks.

### Q47: How do you implement a file upload progress tracking system?
**Answer:** Use Redis to track upload progress in real-time:

```python
@app.post("/upload/init")
async def init_upload(filename: str, total_size: int):
    upload_id = str(uuid.uuid4())
    await redis.hset(f"upload_progress:{upload_id}", mapping={
        "filename": filename, "total_size": total_size,
        "uploaded_bytes": 0, "status": "uploading",
    })
    return {"upload_id": upload_id}

@app.post("/upload/chunk/{upload_id}")
async def upload_chunk(upload_id: str, chunk: UploadFile):
    content = await chunk.read()
    chunk_key = f"chunks:{upload_id}:{uuid.uuid4()}"
    await redis.setex(chunk_key, 3600, content)

    uploaded = await redis.hincrby(f"upload_progress:{upload_id}", "uploaded_bytes", len(content))
    total = int(await redis.hget(f"upload_progress:{upload_id}", "total_size"))

    # Publish progress event for WebSocket notification
    await redis.publish(f"upload:{upload_id}", json.dumps({"uploaded": uploaded, "total": total}))

    return {"uploaded": uploaded, "total": total}

@app.post("/upload/complete/{upload_id}")
async def complete_upload(upload_id: str):
    # Assemble chunks and store final file
    progress = await redis.hgetall(f"upload_progress:{upload_id}")
    await redis.hset(f"upload_progress:{upload_id}", "status", "complete")
    await redis.publish(f"upload:{upload_id}", json.dumps({"status": "complete"}))
    return {"status": "complete"}
```

### Q48: How do you implement a drag-and-drop upload with chunked processing?
**Answer:** Use the resumable upload pattern with chunk validation. Client splits file into chunks (e.g., 1MB each), sends each with chunk number. Server validates chunk numbers are sequential, stores each chunk, and assembles on completion. Return upload progress via WebSocket.

### Q49: How do you handle file uploads through a reverse proxy (Nginx)?
**Answer:** Configure Nginx for large uploads:

```nginx
client_max_body_size 100M;
client_body_buffer_size 128k;
client_body_timeout 300s;
proxy_request_buffering off;  # Stream directly to backend

location /upload {
    proxy_pass http://backend;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
    proxy_buffering off;
}
```

**Key considerations:**
- Disable proxy buffering for large uploads
- Set appropriate timeouts for large file transfers
- Use chunked transfer encoding
- Monitor disk usage for temporary files

### Q50: How do you implement a complete file lifecycle management system?
**Answer:** Design a system that tracks files from upload through processing, storage, serving, and eventual cleanup. Use metadata database for file records, S3 for storage, background tasks for processing, Redis for upload tracking, and scheduled jobs for cleanup and retention enforcement.
