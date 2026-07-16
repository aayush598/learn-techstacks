# File Handling Patterns in FastAPI

## Table of Contents
1. [Image Processing (Pillow)](#image-processing-pillow)
2. [PDF Generation](#pdf-generation)
3. [CSV/Excel Export](#csvexcel-export)
4. [File Validation](#file-validation)
5. [Virus Scanning Integration](#virus-scanning-integration)
6. [File Storage Abstraction](#file-storage-abstraction)
7. [Interview Questions](#interview-questions)

---

## Image Processing (Pillow)

### Installation

```bash
pip install Pillow
```

### Basic Image Operations

```python
from PIL import Image
import io

def resize_image(image_bytes: bytes, width: int, height: int) -> bytes:
    """Resize image to specified dimensions."""
    with Image.open(io.BytesIO(image_bytes)) as img:
        img.thumbnail((width, height), Image.Resampling.LANCZOS)
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        return buffer.getvalue()

def crop_image(image_bytes: bytes, box: tuple) -> bytes:
    """Crop image to specified box (left, top, right, bottom)."""
    with Image.open(io.BytesIO(image_bytes)) as img:
        cropped = img.crop(box)
        buffer = io.BytesIO()
        cropped.save(buffer, format="JPEG", quality=85)
        return buffer.getvalue()

def convert_format(image_bytes: bytes, to_format: str) -> bytes:
    """Convert image to different format."""
    with Image.open(io.BytesIO(image_bytes)) as img:
        buffer = io.BytesIO()
        img.save(buffer, format=to_format)
        return buffer.getvalue()
```

### Image Upload and Processing

```python
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import Response
from PIL import Image, ImageDraw, ImageFont
import io

app = FastAPI()

@app.post("/process-image")
async def process_image(
    file: UploadFile = File(...),
    width: int = Form(800),
    height: int = Form(600),
    format: str = Form("JPEG"),
):
    content = await file.read()

    # Validate image
    try:
        img = Image.open(io.BytesIO(content))
        img.verify()
    except Exception:
        raise HTTPException(400, "Invalid image file")

    # Process
    processed = resize_image(content, width, height)

    return Response(
        content=processed,
        media_type=f"image/{format.lower()}",
    )
```

### Thumbnail Generation

```python
SIZES = {
    "small": (150, 150),
    "medium": (300, 300),
    "large": (600, 600),
}

async def generate_thumbnails(
    image_bytes: bytes,
    filename: str,
) -> dict[str, bytes]:
    """Generate multiple thumbnail sizes."""
    thumbnails = {}

    with Image.open(io.BytesIO(image_bytes)) as img:
        for size_name, dimensions in SIZES.items():
            thumb = img.copy()
            thumb.thumbnail(dimensions, Image.Resampling.LANCZOS)

            buffer = io.BytesIO()
            thumb.save(buffer, format="JPEG", quality=85)
            thumbnails[size_name] = buffer.getvalue()
            thumb.close()

    return thumbnails

@app.post("/upload-with-thumbnails")
async def upload_with_thumbnails(file: UploadFile = File(...)):
    content = await file.read()

    thumbnails = await generate_thumbnails(content, file.filename)

    # Save original and thumbnails
    saved = {}
    for size_name, thumb_data in thumbnails.items():
        path = f"media/thumbnails/{size_name}/{file.filename}"
        with open(path, "wb") as f:
            f.write(thumb_data)
        saved[size_name] = path

    return {"thumbnails": saved}
```

### Image Watermarking

```python
def add_watermark(
    image_bytes: bytes,
    watermark_text: str,
    position: str = "bottom-right",
    opacity: int = 128,
) -> bytes:
    """Add text watermark to image."""
    with Image.open(io.BytesIO(image_bytes)) as img:
        # Create watermark layer
        watermark = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)

        # Use default font (or load custom font)
        font = ImageFont.load_default()

        # Calculate position
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if position == "bottom-right":
            x = img.width - text_width - 10
            y = img.height - text_height - 10
        elif position == "center":
            x = (img.width - text_width) // 2
            y = (img.height - text_height) // 2
        else:  # top-left
            x = 10
            y = 10

        # Draw text with opacity
        draw.text(
            (x, y),
            watermark_text,
            font=font,
            fill=(255, 255, 255, opacity),
        )

        # Composite
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        watermarked = Image.alpha_composite(img, watermark)

        # Convert back to RGB for JPEG
        if watermarked.mode == "RGBA":
            background = Image.new("RGB", watermarked.size, (255, 255, 255))
            background.paste(watermarked, mask=watermarked.split()[3])
            watermarked = background

        buffer = io.BytesIO()
        watermarked.save(buffer, format="JPEG", quality=85)
        return buffer.getvalue()
```

### Image Metadata (EXIF)

```python
from PIL.ExifTags import TAGS

def get_image_metadata(image_bytes: bytes) -> dict:
    """Extract EXIF metadata from image."""
    metadata = {}

    with Image.open(io.BytesIO(image_bytes)) as img:
        # Basic info
        metadata["format"] = img.format
        metadata["mode"] = img.mode
        metadata["size"] = img.size

        # EXIF data
        if hasattr(img, "_getexif"):
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    metadata[str(tag)] = str(value)

    return metadata
```

---

## PDF Generation

### Using ReportLab

```python
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_simple_pdf(output_path: str, data: dict):
    """Generate a simple PDF document."""
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(1 * inch, height - 1 * inch, data.get("title", "Document"))

    # Content
    c.setFont("Helvetica", 12)
    y = height - 1.5 * inch
    for line in data.get("content", []):
        c.drawString(1 * inch, y, line)
        y -= 0.25 * inch

    c.save()

def generate_table_pdf(output_path: str, headers: list, rows: list):
    """Generate PDF with table."""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    elements = []

    # Create table
    table_data = [headers] + rows
    table = Table(table_data)

    # Style table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)

    elements.append(table)
    doc.build(elements)
```

### Using WeasyPrint (HTML to PDF)

```python
from weasyprint import HTML

def html_to_pdf(html_content: str, output_path: str):
    """Convert HTML to PDF using WeasyPrint."""
    HTML(string=html_content).write_pdf(output_path)

@app.post("/generate-report")
async def generate_report(data: dict):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #333; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
        </style>
    </head>
    <body>
        <h1>{data['title']}</h1>
        <table>
            <tr><th>Name</th><th>Value</th></tr>
            {"".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in data['items'].items())}
        </table>
    </body>
    </html>
    """

    output_path = f"reports/report_{data['id']}.pdf"
    html_to_pdf(html, output_path)

    return {"path": output_path}
```

### PDF with FastAPI Response

```python
@app.post("/download-report")
async def download_report(data: dict):
    buffer = io.BytesIO()

    # Generate PDF to buffer
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, f"Report: {data['title']}")
    c.save()
    buffer.seek(0)

    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="report_{data["id"]}.pdf"'
        },
    )
```

---

## CSV/Excel Export

### CSV Export

```python
import csv
import io
from fastapi.responses import StreamingResponse

def generate_csv(headers: list, rows: list) -> str:
    """Generate CSV string from headers and rows."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)
    return output.getvalue()

@app.get("/export/csv")
async def export_csv():
    headers = ["ID", "Name", "Email", "Created At"]
    rows = [
        [1, "Alice", "alice@example.com", "2024-01-01"],
        [2, "Bob", "bob@example.com", "2024-01-02"],
    ]

    csv_content = generate_csv(headers, rows)

    return StreamingResponse(
        io.StringIO(csv_content),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=export.csv"},
    )
```

### Streaming CSV for Large Datasets

```python
async def stream_csv_data(query):
    """Stream CSV data from database query."""
    yield "ID,Name,Email\n"

    async for row in query:
        yield f"{row.id},{row.name},{row.email}\n"

@app.get("/export/csv/streaming")
async def export_csv_streaming():
    query = get_all_users_query()

    return StreamingResponse(
        stream_csv_data(query),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=users.csv"},
    )
```

### Excel Export

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

def generate_excel(
    data: list[dict],
    sheet_name: str = "Data",
    filename: str = "export.xlsx",
) -> bytes:
    """Generate Excel file from list of dictionaries."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet_name

    if not data:
        return io.BytesIO()

    # Headers
    headers = list(data[0].keys())
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4CAF50", end_color="4CAF50", fill_type="solid")

    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center")

    # Data
    for row_idx, row_data in enumerate(data, 2):
        for col_idx, header in enumerate(headers, 1):
            ws.cell(row=row_idx, column=col_idx, value=row_data[header])

    # Auto-adjust column widths
    for col in ws.columns:
        max_length = 0
        column_letter = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        ws.column_dimensions[column_letter].width = max_length + 2

    # Save to bytes
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()

@app.get("/export/excel")
async def export_excel():
    data = [
        {"ID": 1, "Name": "Alice", "Email": "alice@example.com"},
        {"ID": 2, "Name": "Bob", "Email": "bob@example.com"},
    ]

    excel_bytes = generate_excel(data)

    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=export.xlsx"},
    )
```

---

## File Validation

### Comprehensive File Validator

```python
import magic
import hashlib
from typing import Optional

class FileValidator:
    def __init__(
        self,
        max_size: int = 10 * 1024 * 1024,  # 10MB
        allowed_types: Optional[set] = None,
        allowed_extensions: Optional[set] = None,
    ):
        self.max_size = max_size
        self.allowed_types = allowed_types or set()
        self.allowed_extensions = allowed_extensions or set()

    def validate(
        self,
        content: bytes,
        filename: str,
        content_type: Optional[str] = None,
    ) -> list[str]:
        errors = []

        # Size check
        if len(content) > self.max_size:
            errors.append(f"File too large (max {self.max_size} bytes)")

        # Extension check
        if self.allowed_extensions:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in self.allowed_extensions:
                errors.append(f"File extension {ext} not allowed")

        # MIME type check (from magic bytes)
        detected_type = magic.from_buffer(content, mime=True)
        if self.allowed_types and detected_type not in self.allowed_types:
            errors.append(f"File type {detected_type} not allowed")

        # Content type vs magic bytes mismatch
        if content_type and content_type != detected_type:
            errors.append(f"Content type mismatch: declared {content_type}, detected {detected_type}")

        return errors

# Usage
image_validator = FileValidator(
    max_size=5 * 1024 * 1024,
    allowed_types={"image/jpeg", "image/png", "image/gif"},
    allowed_extensions={".jpg", ".jpeg", ".png", ".gif"},
)

@app.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    content = await file.read()
    errors = image_validator.validate(content, file.filename, file.content_type)

    if errors:
        raise HTTPException(400, detail=errors)

    # Process valid file
    return {"filename": file.filename, "size": len(content)}
```

### Hash-Based Validation

```python
def compute_file_hash(content: bytes, algorithm: str = "sha256") -> str:
    """Compute file hash for integrity checking."""
    h = hashlib.new(algorithm)
    h.update(content)
    return h.hexdigest()

@app.post("/upload/verified")
async def upload_verified(file: UploadFile = File(...)):
    content = await file.read()
    file_hash = compute_file_hash(content)

    # Check if file already exists
    existing = await check_file_exists(file_hash)
    if existing:
        return {"status": "duplicate", "existing_file": existing}

    # Store file with hash
    path = f"uploads/{file_hash}/{file.filename}"
    with open(path, "wb") as f:
        f.write(content)

    return {"filename": file.filename, "hash": file_hash}
```

---

## Virus Scanning Integration

### ClamAV Integration

```python
import pyclamd

class VirusScanner:
    def __init__(self, host: str = "localhost", port: int = 3310):
        self.cd = pyclamd.ClamdNetworkSocket(host, port)

    def scan(self, content: bytes) -> dict:
        """Scan content for viruses."""
        result = self.cd.instream(io.BytesIO(content))

        if result is None:
            return {"clean": True, "viruses": []}
        else:
            return {"clean": False, "viruses": result}

scanner = VirusScanner()

@app.post("/upload/scanned")
async def upload_scanned(file: UploadFile = File(...)):
    content = await file.read()

    # Scan for viruses
    scan_result = scanner.scan(content)
    if not scan_result["clean"]:
        raise HTTPException(
            status_code=400,
            detail=f"Virus detected: {scan_result['viruses']}"
        )

    # Save clean file
    path = f"uploads/{file.filename}"
    with open(path, "wb") as f:
        f.write(content)

    return {"filename": file.filename, "status": "clean"}
```

### Async Virus Scanning

```python
import asyncio

class AsyncVirusScanner:
    def __init__(self, host: str = "localhost", port: int = 3310):
        self.host = host
        self.port = port

    async def scan(self, content: bytes) -> dict:
        """Scan content asynchronously."""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self._scan_sync, content)
        return result

    def _scan_sync(self, content: bytes) -> dict:
        cd = pyclamd.ClamdNetworkSocket(self.host, self.port)
        result = cd.instream(io.BytesIO(content))

        if result is None:
            return {"clean": True, "viruses": []}
        return {"clean": False, "viruses": result}

async_scanner = AsyncVirusScanner()

@app.post("/upload/async-scan")
async def upload_async_scan(file: UploadFile = File(...)):
    content = await file.read()

    scan_result = await async_scanner.scan(content)
    if not scan_result["clean"]:
        raise HTTPException(400, f"Virus detected: {scan_result['viruses']}")

    return {"filename": file.filename, "status": "clean"}
```

---

## File Storage Abstraction

### Abstract Storage Interface

```python
from abc import ABC, abstractmethod

class FileStorage(ABC):
    @abstractmethod
    async def upload(self, key: str, content: bytes, content_type: str) -> str:
        """Upload file and return URL."""
        pass

    @abstractmethod
    async def download(self, key: str) -> bytes:
        """Download file content."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete file."""
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if file exists."""
        pass

    @abstractmethod
    async def get_url(self, key: str) -> str:
        """Get file URL."""
        pass
```

### Local File Storage

```python
class LocalFileStorage(FileStorage):
    def __init__(self, base_path: str):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    async def upload(self, key: str, content: bytes, content_type: str) -> str:
        file_path = os.path.join(self.base_path, key)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)

        return f"/files/{key}"

    async def download(self, key: str) -> bytes:
        file_path = os.path.join(self.base_path, key)
        async with aiofiles.open(file_path, "rb") as f:
            return await f.read()

    async def delete(self, key: str) -> bool:
        file_path = os.path.join(self.base_path, key)
        if os.path.exists(file_path):
            os.unlink(file_path)
            return True
        return False

    async def exists(self, key: str) -> bool:
        file_path = os.path.join(self.base_path, key)
        return os.path.exists(file_path)

    async def get_url(self, key: str) -> str:
        return f"/files/{key}"
```

### S3 File Storage

```python
class S3FileStorage(FileStorage):
    def __init__(self, bucket: str, region: str = "us-east-1"):
        self.bucket = bucket
        self.s3 = boto3.client("s3", region_name=region)

    async def upload(self, key: str, content: bytes, content_type: str) -> str:
        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=content,
            ContentType=content_type,
        )
        return f"https://{self.bucket}.s3.amazonaws.com/{key}"

    async def download(self, key: str) -> bytes:
        response = self.s3.get_object(Bucket=self.bucket, Key=key)
        return response["Body"].read()

    async def delete(self, key: str) -> bool:
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=key)
            return True
        except Exception:
            return False

    async def exists(self, key: str) -> bool:
        try:
            self.s3.head_object(Bucket=self.bucket, Key=key)
            return True
        except:
            return False

    async def get_url(self, key: str) -> str:
        return self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": key},
            ExpiresIn=3600,
        )
```

### Storage Factory

```python
class StorageFactory:
    @staticmethod
    def create(storage_type: str, **kwargs) -> FileStorage:
        if storage_type == "local":
            return LocalFileStorage(kwargs["base_path"])
        elif storage_type == "s3":
            return S3FileStorage(kwargs["bucket"], kwargs.get("region"))
        else:
            raise ValueError(f"Unknown storage type: {storage_type}")

# Usage
storage = StorageFactory.create(
    "s3",
    bucket=settings.S3_BUCKET,
    region=settings.AWS_REGION,
)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    key = f"uploads/{uuid.uuid4()}/{file.filename}"

    url = await storage.upload(key, content, file.content_type)

    return {"url": url, "key": key}
```

---

## Interview Questions

### Q1: How do you process images in FastAPI?
**Answer:** Use Pillow (PIL) for image manipulation. Read image bytes, process (resize, crop, convert), and return processed bytes. Use async operations to avoid blocking.

### Q2: How do you generate PDFs in FastAPI?
**Answer:** Use ReportLab for programmatic PDFs, WeasyPrint for HTML-to-PDF. Generate in memory or temp files, return as Response with appropriate content type.

### Q3: How do you export CSV/Excel files?
**Answer:** Use csv module for CSV, openpyxl for Excel. Generate in memory, return as StreamingResponse. For large datasets, stream rows instead of loading all into memory.

### Q4: How do you validate file types?
**Answer:** Check MIME type with python-magic, verify extension, validate magic bytes, and optionally compare declared vs detected types. Don't rely on just one method.

### Q5: What is a file storage abstraction?
**Answer:** An interface that standardizes file operations (upload, download, delete) across different backends (local, S3, GCS). Makes it easy to switch storage providers.

### Q6: How do you integrate virus scanning?
**Answer:** Use ClamAV via pyclamd. Scan file content before processing. Block infected files. Use async scanning for non-blocking operation.

### Q7: How do you handle image thumbnails?
**Answer:** Use Pillow to resize images to multiple sizes. Store thumbnails alongside originals. Generate on upload or on-demand with caching.

### Q8: How do you add watermarks to images?
**Answer:** Use Pillow to create a transparent layer with text, composite it over the original image. Handle positioning, opacity, and font selection.

### Q9: How do you stream large CSV exports?
**Answer:** Use StreamingResponse with a generator that yields rows one at a time. Don't load entire dataset into memory. Query database in batches.

### Q10: How do you extract image metadata?
**Answer:** Use Pillow's _getexif() method to read EXIF data. Parse tags using PIL.ExifTags. Handle missing or corrupt metadata gracefully.

### Q11: How do you handle file format conversion?
**Answer:** Use Pillow to open image in any format, save in desired format. For documents, use libraries like LibreOffice or cloud services.

### Q12: How do you compute file hashes?
**Answer:** Use hashlib to compute SHA256/MD5. Read file in chunks for large files. Use hash for deduplication and integrity checking.

### Q13: How do you generate Excel with styling?
**Answer:** Use openpyxl to set fonts, fills, borders, and alignment. Apply styles to headers and cells. Auto-adjust column widths based on content.

### Q14: How do you handle concurrent file processing?
**Answer:** Use async operations with aiofiles. Process files in background tasks. Use semaphores to limit concurrent processing.

### Q15: How do you implement file deduplication?
**Answer:** Compute file hash before storage. Check if hash exists in database. Return existing file reference if duplicate detected.

### Q16: How do you handle corrupt files?
**Answer:** Validate file integrity during upload. Use try/except for processing. Log errors and return meaningful messages. Implement retry for transient failures.

### Q17: How do you optimize image processing performance?
**Answer:** Process in background tasks, use efficient algorithms (LANCZOS for resizing), limit output quality, and cache processed images.

### Q18: How do you handle different image formats?
**Answer:** Use Pillow's format-agnostic API. Convert between formats as needed. Handle transparency (PNG) vs no transparency (JPEG) appropriately.

### Q19: How do you implement file access control?
**Answer:** Use storage abstraction with permission checks. Implement presigned URLs for temporary access. Use signed URLs for secure downloads.

### Q20: How do you test file handling code?
**Answer:** Create test fixtures with sample files. Mock external services (S3, virus scanner). Test validation, processing, and error scenarios. Use pytest with tmp directories.
