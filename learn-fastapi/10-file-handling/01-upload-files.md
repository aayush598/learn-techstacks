# File Upload in FastAPI

## Table of Contents
1. [File Upload with UploadFile](#file-upload-with-uploadfile)
2. [Multiple File Uploads](#multiple-file-uploads)
3. [File Size Limits](#file-size-limits)
4. [File Type Validation](#file-type-validation)
5. [Streaming Uploads](#streaming-uploads)
6. [Temporary File Handling](#temporary-file-handling)
7. [Progress Tracking](#progress-tracking)
8. [Best Practices](#best-practices)
9. [Interview Questions](#interview-questions)

---

## File Upload with UploadFile

### Basic Upload

```python
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size,
    }
```

### Reading File Content

```python
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Read entire file content
    contents = await file.read()

    # Process content
    return {
        "filename": file.filename,
        "size": len(contents),
        "content": contents.decode("utf-8", errors="replace"),
    }
```

### Saving Uploaded File

```python
import os
import shutil

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "path": file_path}
```

### Async File Saving

```python
import aiofiles

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    async with aiofiles.open(file_path, "wb") as buffer:
        content = await file.read()
        await buffer.write(content)

    return {"filename": file.filename, "path": file_path}
```

### UploadFile Attributes

```python
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # File metadata
    filename = file.filename          # Original filename
    content_type = file.content_type  # MIME type
    size = file.size                  # File size (may be None)
    headers = file.headers           # Custom headers

    # File object (SpooledTemporaryFile)
    file.file                        # Underlying file object

    # Methods
    content = await file.read()      # Read content
    await file.seek(0)               # Seek to beginning
    await file.close()               # Close file

    return {"filename": filename, "content_type": content_type}
```

---

## Multiple File Uploads

### Multiple Files with Same Field

```python
@app.post("/upload-multiple")
async def upload_multiple(files: list[UploadFile] = File(...)):
    results = []
    for file in files:
        content = await file.read()
        results.append({
            "filename": file.filename,
            "size": len(content),
            "content_type": file.content_type,
        })
    return {"files": results, "count": len(results)}
```

### Multiple Files with Different Fields

```python
@app.post("/upload-mixed")
async def upload_mixed(
    avatar: UploadFile = File(...),
    documents: list[UploadFile] = File(...),
):
    avatar_content = await avatar.read()

    doc_results = []
    for doc in documents:
        content = await doc.read()
        doc_results.append({
            "filename": doc.filename,
            "size": len(content),
        })

    return {
        "avatar": {"filename": avatar.filename, "size": len(avatar_content)},
        "documents": doc_results,
    }
```

### Saving Multiple Files

```python
@app.post("/upload-multiple")
async def upload_multiple(files: list[UploadFile] = File(...)):
    saved_files = []

    for file in files:
        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1]
        unique_name = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_name)

        async with aiofiles.open(file_path, "wb") as buffer:
            content = await file.read()
            await buffer.write(content)

        saved_files.append({
            "original_name": file.filename,
            "saved_name": unique_name,
            "size": len(content),
        })

    return {"files": saved_files}
```

---

## File Size Limits

### Using Pydantic Validation

```python
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE} bytes"
        )
    # Process file
    return {"filename": file.filename, "size": len(content)}
```

### Middleware Approach

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class FileSizeLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_size: int = 10 * 1024 * 1024):
        super().__init__(app)
        self.max_size = max_size

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_size:
            return JSONResponse(
                status_code=413,
                content={"detail": "File too large"}
            )
        return await call_next(request)

app.add_middleware(FileSizeLimitMiddleware, max_size=5 * 1024 * 1024)
```

### Per-Endpoint Limits

```python
UPLOAD_LIMITS = {
    "/upload/avatar": 5 * 1024 * 1024,      # 5MB
    "/upload/document": 50 * 1024 * 1024,   # 50MB
    "/upload/video": 500 * 1024 * 1024,     # 500MB
}

@app.post("/upload/{upload_type}")
async def upload_with_limit(
    upload_type: str,
    file: UploadFile = File(...),
):
    max_size = UPLOAD_LIMITS.get(f"/upload/{upload_type}", 10 * 1024 * 1024)
    content = await file.read()

    if len(content) > max_size:
        raise HTTPException(status_code=413, detail="File too large")

    return {"filename": file.filename, "size": len(content)}
```

---

## File Type Validation

### MIME Type Validation

```python
ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "application/pdf",
}

@app.post("/upload")
async def upload_validated(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file.content_type} not allowed"
        )
    # Process file
    return {"filename": file.filename}
```

### Extension Validation

```python
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf"}

@app.post("/upload")
async def upload_with_extension(file: UploadFile = File(...)):
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File extension {file_ext} not allowed"
        )
    # Process file
    return {"filename": file.filename}
```

### Magic Bytes Validation

```python
import magic

def validate_file_magic(content: bytes, expected_type: str) -> bool:
    """Validate file content using magic bytes."""
    mime = magic.from_buffer(content, mime=True)
    return mime == expected_type

@app.post("/upload")
async def upload_magic_validated(file: UploadFile = File(...)):
    content = await file.read()

    if not validate_file_magic(content, "image/jpeg"):
        raise HTTPException(status_code=400, detail="Invalid file content")

    return {"filename": file.filename, "size": len(content)}
```

### Comprehensive Validation

```python
from pydantic import BaseModel, validator

class FileUploadConfig:
    MAX_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_TYPES = {"image/jpeg", "image/png", "application/pdf"}
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}

def validate_upload(file: UploadFile, content: bytes) -> list[str]:
    errors = []

    # Check size
    if len(content) > FileUploadConfig.MAX_SIZE:
        errors.append(f"File too large (max {FileUploadConfig.MAX_SIZE} bytes)")

    # Check MIME type
    if file.content_type not in FileUploadConfig.ALLOWED_TYPES:
        errors.append(f"File type {file.content_type} not allowed")

    # Check extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in FileUploadConfig.ALLOWED_EXTENSIONS:
        errors.append(f"File extension {ext} not allowed")

    # Check magic bytes
    mime = magic.from_buffer(content, mime=True)
    if mime not in FileUploadConfig.ALLOWED_TYPES:
        errors.append(f"File content doesn't match declared type")

    return errors

@app.post("/upload")
async def upload_validated(file: UploadFile = File(...)):
    content = await file.read()
    errors = validate_upload(file, content)

    if errors:
        raise HTTPException(status_code=400, detail=errors)

    return {"filename": file.filename, "size": len(content)}
```

---

## Streaming Uploads

### Streaming Large Files

```python
import aiofiles

@app.post("/upload/stream")
async def upload_streaming(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    async with aiofiles.open(file_path, "wb") as buffer:
        while chunk := await file.read(8192):  # 8KB chunks
            await buffer.write(chunk)

    return {"filename": file.filename, "path": file_path}
```

### Streaming with Progress

```python
@app.post("/upload/stream")
async def upload_with_progress(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    total_size = 0

    async with aiofiles.open(file_path, "wb") as buffer:
        while chunk := await file.read(8192):
            await buffer.write(chunk)
            total_size += len(chunk)

            # Store progress in Redis
            progress = total_size / (file.size or 1) * 100
            await redis.set(f"upload:{file.filename}:progress", progress)

    return {"filename": file.filename, "size": total_size}
```

---

## Temporary File Handling

### Using tempfile

```python
import tempfile
import os

@app.post("/upload")
async def upload_temp(file: UploadFile = File(...)):
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # Process temporary file
        result = process_file(tmp_path)
        return {"result": result}
    finally:
        # Clean up
        os.unlink(tmp_path)
```

### Async Temporary Files

```python
import aiofiles.tempfile

@app.post("/upload")
async def upload_async_temp(file: UploadFile = File(...)):
    async with aiofiles.tempfile.NamedTemporaryFile(delete=False) as tmp:
        content = await file.read()
        await tmp.write(content)
        tmp_path = tmp.name

    try:
        result = process_file(tmp_path)
        return {"result": result}
    finally:
        os.unlink(tmp_path)
```

### Cleanup on Error

```python
@app.post("/upload")
async def upload_safe(file: UploadFile = File(...)):
    tmp_path = None
    try:
        # Create temp file
        tmp_path = os.path.join(UPLOAD_DIR, f"tmp_{uuid.uuid4()}")
        async with aiofiles.open(tmp_path, "wb") as buffer:
            content = await file.read()
            await buffer.write(content)

        # Process
        result = process_file(tmp_path)
        return {"result": result}

    except Exception as e:
        # Clean up on error
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise
    finally:
        # Always clean up temp file
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
```

---

## Progress Tracking

### Redis-Based Progress

```python
import redis.asyncio as redis

redis_client = redis.from_url("redis://localhost:6379")

@app.post("/upload")
async def upload_with_redis_progress(file: UploadFile = File(...)):
    upload_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    async with aiofiles.open(file_path, "wb") as buffer:
        uploaded = 0
        total = file.size or 1

        while chunk := await file.read(8192):
            await buffer.write(chunk)
            uploaded += len(chunk)

            # Update progress in Redis
            progress = uploaded / total * 100
            await redis_client.hset(
                f"upload:{upload_id}",
                mapping={
                    "progress": progress,
                    "uploaded": uploaded,
                    "total": total,
                    "status": "uploading",
                }
            )

    await redis_client.hset(
        f"upload:{upload_id}",
        mapping={"status": "complete", "progress": 100}
    )

    return {"upload_id": upload_id, "filename": file.filename}

@app.get("/upload/{upload_id}/progress")
async def get_upload_progress(upload_id: str):
    progress = await redis_client.hgetall(f"upload:{upload_id}")
    if not progress:
        raise HTTPException(status_code=404, detail="Upload not found")
    return progress
```

---

## Best Practices

### 1. Validate File Types

```python
# Check MIME type, extension, AND magic bytes
# Don't rely on just one
```

### 2. Limit File Size

```python
# Set maximum file size
# Check Content-Length header early
# Validate after reading
```

### 3. Use Async I/O

```python
# Use aiofiles for non-blocking file operations
# Don't block the event loop with file I/O
```

### 4. Generate Unique Filenames

```python
# Don't use original filename directly
# Use UUID or hash-based naming
unique_name = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
```

### 5. Handle Cleanup

```python
# Clean up temporary files on error
# Use try/finally for guaranteed cleanup
# Set expiration for uploaded files
```

### 6. Stream Large Files

```python
# Don't load entire file into memory
# Process in chunks
# Use streaming for large uploads
```

### 7. Store Metadata Separately

```python
# Store file metadata (name, type, size) in database
# Store files in filesystem or cloud storage
# Link metadata to file storage
```

---

## Interview Questions

### Q1: What is UploadFile in FastAPI?
**Answer:** UploadFile is a class that provides file upload functionality with attributes like filename, content_type, size, and methods like read(), seek(), and close(). It handles file streaming efficiently.

### Q2: How do you limit file upload size in FastAPI?
**Answer:** Check Content-Length header in middleware, validate content length after reading, and use Pydantic validation. Set appropriate limits per endpoint.

### Q3: How do you validate file types?
**Answer:** Check MIME type, file extension, and magic bytes (file content). Don't rely on just one method as they can be spoofed.

### Q4: What are magic bytes?
**Answer:** The first few bytes of a file that identify its type (e.g., JPEG starts with FFD8FF). Use the `python-magic` library to detect file types from content.

### Q5: How do you handle large file uploads?
**Answer:** Stream the file in chunks instead of loading entirely into memory. Use async I/O with aiofiles. Set appropriate chunk sizes (e.g., 8KB).

### Q6: How do you track upload progress?
**Answer:** Store progress in Redis with upload ID. Update progress during chunk processing. Provide endpoint to query progress.

### Q7: What is the difference between File() and UploadFile?
**Answer:** File() returns raw bytes. UploadFile returns a file-like object with metadata and streaming capabilities. Use UploadFile for large files.

### Q8: How do you handle multiple file uploads?
**Answer:** Use `list[UploadFile] = File(...)` for multiple files with the same field name. Iterate and process each file.

### Q9: How do you generate unique filenames?
**Answer:** Use UUID4 with original extension, or hash the file content. Avoid using original filenames to prevent path traversal and overwrites.

### Q10: How do you clean up temporary files?
**Answer:** Use try/finally blocks to ensure cleanup. Set file expiration. Use tempfile module for automatic cleanup.

### Q11: What is the content_type attribute?
**Answer:** The MIME type of the uploaded file (e.g., "image/jpeg", "application/pdf"). Set by the client, so shouldn't be trusted alone for validation.

### Q12: How do you handle concurrent file uploads?
**Answer:** Use async I/O to handle multiple uploads simultaneously. Implement rate limiting. Use temporary directories with unique names.

### Q13: How do you store uploaded files?
**Answer:** Filesystem (simple), cloud storage (S3, GCS), or database (small files). Consider scalability, cost, and backup requirements.

### Q14: How do you prevent path traversal in filenames?
**Answer:** Never use the original filename directly. Generate unique names using UUID. Sanitize filenames if you must use them.

### Q15: What is the difference between sync and async file uploads?
**Answer:** Sync blocks the event loop during I/O. Async (aiofiles) allows other requests to process during I/O. Always use async for production.

### Q16: How do you handle upload failures?
**Answer:** Implement retry logic, clean up partial files, provide meaningful error messages, and track failed uploads for investigation.

### Q17: How do you validate file content matches the declared type?
**Answer:** Use magic bytes (python-magic) to verify file content. Don't trust client-provided MIME types or extensions alone.

### Q18: How do you implement virus scanning for uploads?
**Answer:** Integrate with ClamAV or cloud-based scanning services. Scan after upload but before processing. Quarantine infected files.

### Q19: How do you handle file uploads in a distributed system?
**Answer:** Use shared storage (S3, NFS). Store upload state in Redis. Handle partial uploads and retries. Consider chunked uploads for large files.

### Q20: How do you optimize file upload performance?
**Answer:** Stream in chunks, use async I/O, compress before upload, implement resumable uploads, and use CDN for distribution.
