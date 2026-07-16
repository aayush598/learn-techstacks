# Background Task Patterns

## Table of Contents
1. [Email Sending in Background](#email-sending-in-background)
2. [Image Processing](#image-processing)
3. [PDF Generation](#pdf-generation)
4. [Data Export/Import](#data-exportimport)
5. [Webhook Delivery](#webhook-delivery)
6. [Retry with Exponential Backoff](#retry-with-exponential-backoff)
7. [Dead Letter Queues](#dead-letter-queues)
8. [Task Prioritization](#task-prioritization)
9. [Interview Questions](#interview-questions)

---

## Email Sending in Background

### Using FastAPI BackgroundTasks

```python
from fastapi import FastAPI, BackgroundTasks
from pydantic import EmailStr
from jinja2 import Template

app = FastAPI()

def send_email(to: str, subject: str, body: str):
    import smtplib
    from email.mime.text import MIMEText

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = "noreply@example.com"
    msg["To"] = to

    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login("user", "password")
        server.send_message(msg)

def render_email_template(template_name: str, context: dict) -> str:
    templates = {
        "welcome": "<h1>Welcome {{ name }}!</h1><p>Thanks for registering.</p>",
        "password_reset": "<h1>Password Reset</h1><p>Click <a href='{{ url }}'>here</a> to reset.</p>",
    }
    template = Template(templates[template_name])
    return template.render(context)

@app.post("/register")
async def register(email: EmailStr, name: str, background_tasks: BackgroundTasks):
    user = create_user(email, name)

    body = render_email_template("welcome", {"name": name})
    background_tasks.add_task(send_email, email, "Welcome!", body)

    return {"message": "User created", "user_id": user.id}

@app.post("/password-reset")
async def password_reset(email: EmailStr, background_tasks: BackgroundTasks):
    token = generate_reset_token(email)
    url = f"https://example.com/reset?token={token}"

    body = render_email_template("password_reset", {"url": url})
    background_tasks.add_task(send_email, email, "Password Reset", body)

    return {"message": "Reset email sent"}
```

### Using Celery for Email

```python
# tasks.py
from celery import shared_task

@shared_task(bind=True, max_retries=3)
def send_email_task(self, to: str, subject: str, body: str):
    try:
        import smtplib
        from email.mime.text import MIMEText

        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = "noreply@example.com"
        msg["To"] = to

        with smtplib.SMTP("smtp.example.com", 587) as server:
            server.starttls()
            server.login("user", "password")
            server.send_message(msg)

        return {"status": "sent", "to": to}
    except Exception as exc:
        self.retry(exc=exc, countdown=60)

# main.py
@app.post("/register")
async def register(email: str, name: str):
    user = create_user(email, name)
    send_email_task.delay(email, "Welcome!", f"Hello {name}!")
    return {"message": "User created"}
```

### Using SendGrid/SES

```python
import sendgrid
from sendgrid.helpers.mail import Mail

@shared_task
def send_email_sendgrid(to: str, subject: str, html_content: str):
    sg = sendgrid.SendGridAPIClient(api_key="your_api_key")
    message = Mail(
        from_email="noreply@example.com",
        to_emails=to,
        subject=subject,
        html_content=html_content,
    )
    sg.send(message)

@shared_task
def send_email_ses(to: str, subject: str, html_content: str):
    import boto3
    client = boto3.client("ses", region_name="us-east-1")
    client.send_email(
        Source="noreply@example.com",
        Destination={"ToAddresses": [to]},
        Message={
            "Subject": {"Data": subject},
            "Body": {"Html": {"Data": html_content}},
        }
    )
```

---

## Image Processing

### Resize Images in Background

```python
from PIL import Image
import io
from fastapi import FastAPI, BackgroundTasks, UploadFile

app = FastAPI()

def resize_image(file_path: str, sizes: list[tuple[int, int]]):
    """Resize image to multiple sizes."""
    with Image.open(file_path) as img:
        for width, height in sizes:
            resized = img.copy()
            resized.thumbnail((width, height), Image.Resampling.LANCZOS)
            thumb_path = f"{file_path}_{width}x{height}.jpg"
            resized.save(thumb_path, "JPEG", quality=85)
            resized.close()

@app.post("/upload-image")
async def upload_image(
    file: UploadFile,
    background_tasks: BackgroundTasks
):
    # Save uploaded file
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Process in background
    sizes = [(200, 200), (400, 400), (800, 800)]
    background_tasks.add_task(resize_image, file_path, sizes)

    return {"message": "Image uploaded, processing in background"}
```

### Generate Thumbnails with Celery

```python
from celery import shared_task
from PIL import Image
import boto3

@shared_task
def generate_thumbnails(image_key: str, bucket: str):
    """Generate thumbnails for uploaded image."""
    s3 = boto3.client("s3")

    # Download image
    response = s3.get_object(Bucket=bucket, Key=image_key)
    image_data = response["Body"].read()

    # Generate thumbnails
    sizes = {"small": (150, 150), "medium": (300, 300), "large": (600, 600)}

    for size_name, dimensions in sizes.items():
        with Image.open(io.BytesIO(image_data)) as img:
            img.thumbnail(dimensions, Image.Resampling.LANCZOS)

            buffer = io.BytesIO()
            img.save(buffer, "JPEG", quality=85)
            buffer.seek(0)

            thumb_key = f"thumbnails/{size_name}/{image_key}"
            s3.put_object(
                Bucket=bucket,
                Key=thumb_key,
                Body=buffer,
                ContentType="image/jpeg",
            )

    return {"thumbnails": list(sizes.keys())}
```

### Image Optimization

```python
@shared_task
def optimize_image(file_path: str):
    """Optimize image for web delivery."""
    with Image.open(file_path) as img:
        # Convert to WebP
        webp_path = file_path.rsplit(".", 1)[0] + ".webp"
        img.save(webp_path, "WEBP", quality=80, method=6)

        # Create responsive versions
        widths = [320, 640, 768, 1024, 1280, 1920]
        for width in widths:
            ratio = width / img.width
            height = int(img.height * ratio)
            resized = img.resize((width, height), Image.Resampling.LANCZOS)
            resized.save(
                f"{file_path}_{width}w.webp",
                "WEBP",
                quality=80,
            )
            resized.close()

    return {"optimized": True}
```

---

## PDF Generation

### Using ReportLab

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def generate_invoice_pdf(order_id: int, items: list, total: float, output_path: str):
    """Generate invoice PDF."""
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 24)
    c.drawString(1 * inch, height - 1 * inch, "INVOICE")

    # Order info
    c.setFont("Helvetica", 12)
    c.drawString(1 * inch, height - 1.5 * inch, f"Order #{order_id}")
    c.drawString(1 * inch, height - 1.75 * inch, f"Date: {datetime.now().strftime('%Y-%m-%d')}")

    # Items
    y = height - 2.5 * inch
    for item in items:
        c.drawString(1 * inch, y, f"{item['name']}: ${item['price']:.2f}")
        y -= 0.25 * inch

    # Total
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1 * inch, y - 0.5 * inch, f"Total: ${total:.2f}")

    c.save()

@app.post("/orders/{order_id}/invoice")
async def get_invoice(order_id: int, background_tasks: BackgroundTasks):
    order = get_order(order_id)

    output_path = f"invoices/order_{order_id}.pdf"
    background_tasks.add_task(
        generate_invoice_pdf,
        order_id,
        order.items,
        order.total,
        output_path
    )

    return {"message": "Invoice generating", "order_id": order_id}
```

### Using WeasyPrint

```python
from weasyprint import HTML

def generate_pdf_from_html(html_content: str, output_path: str):
    """Generate PDF from HTML using WeasyPrint."""
    HTML(string=html_content).write_pdf(output_path)

@app.post("/report")
async def generate_report(data: dict, background_tasks: BackgroundTasks):
    # Render HTML template
    html = render_template("report.html", data=data)

    output_path = f"reports/report_{data['id']}.pdf"
    background_tasks.add_task(generate_pdf_from_html, html, output_path)

    return {"message": "Report generating"}
```

---

## Data Export/Import

### CSV Export

```python
import csv
import io

def export_users_to_csv(user_ids: list[int], output_path: str):
    """Export users to CSV file."""
    users = get_users_by_ids(user_ids)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "email", "created_at"])
        writer.writeheader()
        for user in users:
            writer.writerow({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "created_at": user.created_at.isoformat(),
            })

@app.post("/export/users")
async def export_users(background_tasks: BackgroundTasks):
    user_ids = get_all_user_ids()
    output_path = f"exports/users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    background_tasks.add_task(export_users_to_csv, user_ids, output_path)

    return {"message": "Export started", "file": output_path}
```

### Excel Export

```python
import openpyxl

def export_to_excel(data: list[dict], output_path: str, sheet_name: str = "Data"):
    """Export data to Excel file."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet_name

    if not data:
        return

    # Headers
    headers = list(data[0].keys())
    for col, header in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=header)

    # Data
    for row_idx, row_data in enumerate(data, 2):
        for col_idx, header in enumerate(headers, 1):
            ws.cell(row=row_idx, column=col_idx, value=row_data[header])

    wb.save(output_path)

@app.post("/export/orders")
async def export_orders(background_tasks: BackgroundTasks):
    orders = get_all_orders()
    output_path = f"exports/orders_{datetime.now().strftime('%Y%m%d')}.xlsx"

    background_tasks.add_task(export_to_excel, orders, output_path, "Orders")

    return {"message": "Export started"}
```

### Data Import

```python
import csv

def import_users_from_csv(file_path: str):
    """Import users from CSV file."""
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        users_created = 0
        errors = []

        for row in reader:
            try:
                create_user(
                    name=row["name"],
                    email=row["email"],
                )
                users_created += 1
            except Exception as e:
                errors.append({"row": row, "error": str(e)})

    return {"created": users_created, "errors": errors}

@app.post("/import/users")
async def import_users(file: UploadFile, background_tasks: BackgroundTasks):
    file_path = f"imports/{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    background_tasks.add_task(import_users_from_csv, file_path)

    return {"message": "Import started"}
```

---

## Webhook Delivery

### Webhook Sender

```python
import httpx
import hmac
import hashlib
import json

async def deliver_webhook(
    url: str,
    event: str,
    payload: dict,
    secret: str,
    max_retries: int = 3,
):
    """Deliver webhook with retry and signature."""
    headers = {
        "Content-Type": "application/json",
        "X-Webhook-Event": event,
        "X-Webhook-Signature": generate_signature(payload, secret),
    }

    async with httpx.AsyncClient() as client:
        for attempt in range(max_retries):
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=10.0,
                )

                if response.status_code < 400:
                    return {"status": "delivered", "response_code": response.status_code}

                if response.status_code >= 500:
                    # Server error, retry
                    await asyncio.sleep(2 ** attempt)
                    continue

                # Client error, don't retry
                return {"status": "failed", "response_code": response.status_code}

            except httpx.RequestError:
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                return {"status": "failed", "error": "connection_error"}

    return {"status": "failed", "error": "max_retries_exceeded"}

def generate_signature(payload: dict, secret: str) -> str:
    """Generate HMAC signature for webhook."""
    body = json.dumps(payload, sort_keys=True)
    signature = hmac.new(
        secret.encode(),
        body.encode(),
        hashlib.sha256
    ).hexdigest()
    return f"sha256={signature}"

@app.post("/events")
async def trigger_event(event_type: str, data: dict, background_tasks: BackgroundTasks):
    # Find webhooks registered for this event
    webhooks = get_webhooks_for_event(event_type)

    for webhook in webhooks:
        background_tasks.add_task(
            deliver_webhook,
            webhook.url,
            event_type,
            data,
            webhook.secret,
        )

    return {"message": "Event triggered", "webhooks_queued": len(webhooks)}
```

---

## Retry with Exponential Backoff

### Manual Implementation

```python
import asyncio
import random
from functools import wraps

def retry_with_backoff(max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

                    if attempt < max_retries:
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        jitter = random.uniform(0, delay * 0.1)
                        await asyncio.sleep(delay + jitter)

            raise last_exception
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3, base_delay=1.0)
async def call_external_api(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()
        return response.json()
```

### Celery Retry

```python
from celery import shared_task

@shared_task(bind=True, max_retries=5)
def retry_task(self, url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        # Exponential backoff: 60s, 120s, 240s, 480s, 960s
        retry_in = 60 * (2 ** self.request.retries)
        self.retry(exc=exc, countdown=retry_in)
```

---

## Dead Letter Queues

### Concept

A dead letter queue (DLQ) stores messages that couldn't be processed after multiple retries. It allows you to investigate and reprocess failed tasks.

### Implementation

```python
import json
from datetime import datetime

class DeadLetterQueue:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.dlq_key = "dead_letter_queue"

    async def add(self, task_name: str, args: list, kwargs: dict, error: str):
        entry = {
            "task_name": task_name,
            "args": args,
            "kwargs": kwargs,
            "error": error,
            "timestamp": datetime.utcnow().isoformat(),
        }
        await self.redis.rpush(self.dlq_key, json.dumps(entry))

    async def get_all(self) -> list:
        entries = await self.redis.lrange(self.dlq_key, 0, -1)
        return [json.loads(entry) for entry in entries]

    async def retry_entry(self, index: int):
        entry = await self.redis.lindex(self.dlq_key, index)
        if entry:
            data = json.loads(entry)
            # Re-queue the task
            await self.redis.lrem(self.dlq_key, 1, entry)
            return data
        return None

    async def clear(self):
        await self.redis.delete(self.dlq_key)

# Usage in task
@shared_task(bind=True)
def task_with_dlq(self, data: dict):
    try:
        return process(data)
    except Exception as exc:
        if self.request.retries >= self.max_retries:
            # Send to DLQ
            dlq = DeadLetterQueue(redis_client)
            await dlq.add(
                self.name,
                self.request.args,
                self.request.kwargs,
                str(exc)
            )
            return {"error": "moved_to_dlq"}
        raise self.retry(exc=exc, countdown=60)
```

### DLQ Management API

```python
@app.get("/admin/dlq")
async def get_dlq_entries():
    dlq = DeadLetterQueue(redis_client)
    entries = await dlq.get_all()
    return {"entries": entries, "count": len(entries)}

@app.post("/admin/dlq/{index}/retry")
async def retry_dlq_entry(index: int):
    dlq = DeadLetterQueue(redis_client)
    entry = await dlq.retry_entry(index)
    if entry:
        # Re-queue the task
        task = celery_app.send_task(entry["task_name"], args=entry["args"])
        return {"status": "retried", "task_id": task.id}
    return {"status": "not_found"}

@app.delete("/admin/dlq")
async def clear_dlq():
    dlq = DeadLetterQueue(redis_client)
    await dlq.clear()
    return {"status": "cleared"}
```

---

## Task Prioritization

### Queue-Based Prioritization

```python
from kombu import Queue, Exchange

# Define exchanges and queues
default_exchange = Exchange("default", type="direct")
priority_exchange = Exchange("priority", type="direct")

celery_app.conf.task_queues = (
    Queue("high", priority_exchange, routing_key="high"),
    Queue("normal", default_exchange, routing_key="normal"),
    Queue("low", default_exchange, routing_key="low"),
)

celery_app.conf.task_routes = {
    "app.tasks.payment_*": {"queue": "high"},
    "app.tasks.email_*": {"queue": "normal"},
    "app.tasks.report_*": {"queue": "low"},
}

# Worker consumes from queues in order
# Workers should be configured to consume from high-priority queues first
```

### Priority in ARQ

```python
# ARQ doesn't have built-in priority queues
# Implement using multiple queues with separate workers

class HighPriorityWorkerSettings:
    functions = [critical_task]
    queue_name = "arq:high"

class NormalWorkerSettings:
    functions = [normal_task]
    queue_name = "arq:normal"

class LowPriorityWorkerSettings:
    functions = [background_task]
    queue_name = "arq:low"

# Enqueue to specific queue
await redis.enqueue_job("critical_task", queue_name="arq:high")
```

### Dynamic Priority

```python
@app.post("/tasks")
async def create_task(data: dict, priority: str = "normal"):
    queue_map = {
        "high": "arq:high",
        "normal": "arq:normal",
        "low": "arq:low",
    }

    queue = queue_map.get(priority, "arq:normal")

    job = await redis.enqueue_job(
        "process_task",
        data,
        queue_name=queue,
    )

    return {"job_id": job.job_id, "priority": priority}
```

---

## Interview Questions

### Q1: How do you implement email sending in background?
**Answer:** Use FastAPI BackgroundTasks for simple cases, Celery or ARQ for production. Include retry logic, template rendering, and support for multiple email providers.

### Q2: How do you handle image processing in background?
**Answer:** Use Pillow for image manipulation. Generate thumbnails, resize, and optimize in background tasks. Store processed images in cloud storage (S3).

### Q3: What's the best approach for PDF generation?
**Answer:** Use ReportLab for programmatic PDFs, WeasyPrint for HTML-to-PDF. Generate in background tasks since PDF creation can be slow for complex documents.

### Q4: How do you implement CSV/Excel export?
**Answer:** Generate files in background tasks. Use csv module for CSV, openpyxl for Excel. Store generated files and provide download URLs.

### Q5: How do you implement webhook delivery with reliability?
**Answer:** Use async HTTP client with retry logic, exponential backoff, HMAC signatures for verification, and dead letter queues for failed deliveries.

### Q6: What is exponential backoff?
**Answer:** A retry strategy where delay increases exponentially (1s, 2s, 4s, 8s...). Add jitter to prevent thundering herd. Cap the maximum delay.

### Q7: What is a dead letter queue?
**Answer:** A queue that stores messages that failed processing after maximum retries. Allows investigation and manual reprocessing of failed tasks.

### Q8: How do you implement task prioritization?
**Answer:** Use multiple queues with different priorities. Workers consume from high-priority queues first. Route tasks to appropriate queues based on type.

### Q9: How do you handle task failures gracefully?
**Answer:** Implement try/except in tasks, use retry with backoff, move permanently failed tasks to DLQ, log errors, and alert when needed.

### Q10: How do you implement idempotent tasks?
**Answer:** Use unique job IDs to prevent duplicates. Check if a task was already processed before executing. Store task status in Redis/database.

### Q11: What is the difference between at-least-once and at-most-once delivery?
**Answer:** At-least-once: task may run multiple times but never missed. At-most-once: task runs at most once but may be missed. Choose based on your use case.

### Q12: How do you handle large file processing?
**Answer:** Stream files instead of loading entirely into memory. Process in chunks. Use temporary files and clean up after processing.

### Q13: How do you implement task timeout?
**Answer:** Use `time_limit` in Celery, `job_timeout` in ARQ. Implement soft timeouts for graceful shutdown. Handle timeout exceptions.

### Q14: How do you monitor background task health?
**Answer:** Track success/failure rates, processing times, queue depths. Use Flower for Celery, custom monitoring for ARQ. Set up alerts for anomalies.

### Q15: How do you handle task dependencies?
**Answer:** Use Celery chains/chords for dependent tasks. ARQ requires manual chaining. Consider using a workflow engine for complex dependencies.

### Q16: What is idempotency and why is it important for tasks?
**Answer:** Idempotency means a task produces the same result when run multiple times. Critical for reliability because tasks may be retried or duplicated.

### Q17: How do you implement task progress tracking?
**Answer:** Store progress in Redis (e.g., `progress:task_id`). Update during task execution. Provide endpoint for clients to check progress.

### Q18: How do you handle rate-limited external APIs?
**Answer:** Use rate-limited task queues, implement delays between calls, respect API rate limits, and queue excess requests for later processing.

### Q19: What are task workers and how do you scale them?
**Answer:** Workers are processes that consume and execute tasks. Scale by adding more workers (horizontal) or increasing concurrency (vertical).

### Q20: How do you handle task scheduling?
**Answer:** Use Celery Beat or ARQ cron for periodic tasks. Implement task scheduling API for user-defined schedules. Use timezone-aware scheduling.

### Q21: How do you implement task cancellation?
**Answer:** Check for cancellation flag during task execution. Store cancellation flags in Redis. Celery supports `revoke()` but with limitations.

### Q22: How do you handle task results for async clients?
**Answer:** Use WebSockets, Server-Sent Events, or polling. Store results in Redis/database. Provide endpoints to check task status and retrieve results.

### Q23: What is the difference between sync and async task queues?
**Answer:** Sync queues (traditional Celery) use threads/processes. Async queues (ARQ) use asyncio. Async is better for I/O-bound tasks and integrates with FastAPI.

### Q24: How do you implement task queue monitoring?
**Answer:** Track queue depth, processing time, success/failure rates. Use tools like Flower (Celery), custom dashboards, or Prometheus/Grafana.

### Q25: How do you handle task serialization?
**Answer:** Use JSON for portability. Avoid pickling (security risk). Handle complex objects by serializing to JSON-compatible formats.
