# Input Validation with FastAPI

## Table of Contents

1. [Introduction](#1-introduction)
2. [Pydantic Validation](#2-pydantic)
3. [Query and Path Validation](#3-query-path)
4. [Regex Patterns](#4-regex)
5. [Email and URL Validation](#5-email-url)
6. [SQL Injection Prevention](#6-sql-injection)
7. [XSS Prevention](#7-xss)
8. [File Upload Validation](#8-file-upload)
9. [Input Sanitization](#9-sanitization)
10. [Custom Validators](#10-custom)
11. [Advanced Validation Patterns](#11-advanced)
12. [Best Practices](#12-best-practices)

---

## 1. Introduction <a name="1-introduction"></a>

Input validation is the first line of defense against malicious data. FastAPI
provides powerful validation through Pydantic models and parameter annotations,
making it easy to validate all incoming data.

### Why Input Validation Matters

- **Security**: Prevents injection attacks (SQL, XSS, command injection)
- **Data Integrity**: Ensures data conforms to expected formats
- **Error Handling**: Provides clear, actionable error messages
- **Documentation**: Validation rules appear in OpenAPI docs
- **Type Safety**: Catches type errors at runtime

### FastAPI Validation Layers

```
Request → Path Parameters → Query Parameters → Headers → Body → Pydantic Model
          (int, float)     (int, str, bool)   (str)     (JSON)  (validated)
```

---

## 2. Pydantic Validation <a name="2-pydantic"></a>

### Basic Field Validation

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from datetime import datetime
from enum import Enum

class UserCreate(BaseModel):
    # String validation
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="User's full name",
        examples=["John Doe"],
    )

    # Email validation (built-in)
    email: str = Field(
        ...,
        max_length=255,
        description="User's email address",
    )

    # Password with custom validation
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Strong password required",
    )

    # Integer validation
    age: int = Field(
        ...,
        ge=0,      # Greater than or equal
        le=150,    # Less than or equal
        description="User's age",
    )

    # Float validation
    balance: float = Field(
        ...,
        gt=0,      # Greater than
        lt=1000000, # Less than
        description="Account balance",
    )

    # Optional fields
    bio: Optional[str] = Field(
        None,
        max_length=500,
        description="User biography",
    )

    # With examples
    website: Optional[str] = Field(
        None,
        examples=["https://example.com"],
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty or whitespace")
        if any(char.isdigit() for char in v):
            raise ValueError("Name cannot contain digits")
        return v.strip()

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError("Invalid email format")
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v):
            raise ValueError("Password must contain special character")
        return v
```

### Model-Level Validation

```python
class OrderCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    total_price: float = Field(..., gt=0)
    discount_code: Optional[str] = None

    @model_validator(mode="after")
    def validate_price_quantity(self):
        """Validate total_price matches quantity."""
        expected_total = self.quantity * 100.0  # Assume $100 per item
        if self.discount_code:
            expected_total *= 0.9  # 10% discount
        if abs(self.total_price - expected_total) > 0.01:
            raise ValueError(
                f"Total price {self.total_price} doesn't match "
                f"expected {expected_total}"
            )
        return self

class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date >= self.end_date:
            raise ValueError("Start date must be before end date")
        if (self.end_date - self.start_date).days > 365:
            raise ValueError("Date range cannot exceed 1 year")
        return self
```

### Nested Models

```python
class Address(BaseModel):
    street: str = Field(..., min_length=1, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., pattern=r'^[A-Z]{2}$')  # Two-letter state
    zip_code: str = Field(..., pattern=r'^\d{5}(-\d{4})?$')
    country: str = Field(..., min_length=2, max_length=2)

class UserWithAddress(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str
    addresses: list[Address] = Field(..., min_length=1, max_length=5)
    primary_address_index: int = Field(0, ge=0)

    @model_validator(mode="after")
    def validate_primary_address(self):
        if self.primary_address_index >= len(self.addresses):
            raise ValueError("Primary address index out of range")
        return self
```

### Enums and Literals

```python
from enum import Enum
from typing import Literal

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class UserCreate(BaseModel):
    name: str
    role: UserRole = UserRole.USER

class OrderUpdate(BaseModel):
    status: OrderStatus
    notes: Optional[str] = None
    priority: Literal["low", "medium", "high"] = "medium"
```

---

## 3. Query and Path Validation <a name="3-query-path"></a>

### Query Parameter Validation

```python
from fastapi import FastAPI, Query, Path

app = FastAPI()

@app.get("/items/")
async def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max items to return"),
    sort_by: str = Query("created_at", pattern=r'^(name|created_at|price)$'),
    order: str = Query("desc", pattern=r'^(asc|desc)$'),
    search: Optional[str] = Query(None, min_length=1, max_length=100),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
):
    """List items with filtering and pagination."""
    pass

@app.get("/search/")
async def search(
    q: str = Query(..., min_length=1, max_length=200, description="Search query"),
    category: Optional[str] = Query(None, max_length=50),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
):
    """Search items with pagination."""
    pass

# Validate query parameters with custom regex
@app.get("/filter/")
async def filter_items(
    status: str = Query(..., pattern=r'^(active|inactive|pending)$'),
    type: str = Query(..., pattern=r'^(physical|digital|service)$'),
):
    pass
```

### Path Parameter Validation

```python
@app.get("/items/{item_id}")
async def get_item(
    item_id: int = Path(..., gt=0, description="Item ID"),
):
    """Get item by ID (must be positive integer)."""
    pass

@app.get("/users/{username}")
async def get_user(
    username: str = Path(
        ...,
        min_length=3,
        max_length=32,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description="Username",
    ),
):
    """Get user by username (alphanumeric, 3-32 chars)."""
    pass

@app.get("/products/{category}/{product_id}")
async def get_product(
    category: str = Path(..., pattern=r'^[a-z-]+$'),
    product_id: str = Path(..., pattern=r'^[A-Z]{2}\d{6}$'),  # e.g., AB123456
):
    """Get product by category and ID."""
    pass
```

### Combined Validation

```python
@app.get("/reports/")
async def generate_report(
    # Query params
    start_date: datetime = Query(..., description="Report start date"),
    end_date: datetime = Query(..., description="Report end date"),
    format: str = Query("json", pattern=r'^(json|csv|pdf)$'),
    # Path params
    report_type: str = Path(..., pattern=r'^(daily|weekly|monthly)$'),
    # Header
    request: Request,
):
    # Validate date range
    if start_date >= end_date:
        raise HTTPException(400, "start_date must be before end_date")
    if (end_date - start_date).days > 365:
        raise HTTPException(400, "Date range cannot exceed 1 year")
    pass
```

---

## 4. Regex Patterns <a name="4-regex"></a>

### Common Validation Patterns

```python
import re
from pydantic import Field, field_validator

class ValidationPatterns:
    # Email
    EMAIL = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Phone (US)
    PHONE_US = r'^(\+1)?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'

    # International phone
    PHONE_INTL = r'^\+?[1-9]\d{1,14}$'

    # URL
    URL = r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?:/[-\w./?%&=]*)?$'

    # IPv4
    IPV4 = r'^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$'

    # UUID
    UUID = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'

    # Date (YYYY-MM-DD)
    DATE = r'^\d{4}-\d{2}-\d{2}$'

    # DateTime (ISO 8601)
    DATETIME = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'

    # Credit card
    CREDIT_CARD = r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})$'

    # Hex color
    HEX_COLOR = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'

    # Strong password
    STRONG_PASSWORD = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,}$'

    # Username
    USERNAME = r'^[a-zA-Z0-9_-]{3,32}$'

    # Slug
    SLUG = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'

class ValidatedModel(BaseModel):
    email: str = Field(..., pattern=ValidationPatterns.EMAIL)
    phone: str = Field(..., pattern=ValidationPatterns.PHONE_US)
    website: Optional[str] = Field(None, pattern=ValidationPatterns.URL)
    ip_address: str = Field(..., pattern=ValidationPatterns.IPV4)
    uuid: str = Field(..., pattern=ValidationPatterns.UUID)
    color: str = Field(..., pattern=ValidationPatterns.HEX_COLOR)
    username: str = Field(..., pattern=ValidationPatterns.USERNAME)
    slug: str = Field(..., pattern=ValidationPatterns.SLUG)
```

### Pydantic Pattern Validation

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    # Simple pattern
    sku: str = Field(..., pattern=r'^[A-Z]{2}-\d{4}-[A-Z]$')

    # Complex patterns
    barcode: str = Field(..., pattern=r'^\d{13}$')  # EAN-13
    isbn: str = Field(..., pattern=r'^(?:\d{10}|\d{13})$')
    color: str = Field(..., pattern=r'^#[0-9A-Fa-f]{6}$')

    # Conditional patterns (use validators)
    value: str

    @field_validator("value")
    @classmethod
    def validate_value(cls, v, info):
        # Custom validation logic
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError("Value must be alphanumeric")
        return v
```

---

## 5. Email and URL Validation <a name="5-email-url"></a>

### Email Validation

```python
from pydantic import BaseModel, Field, field_validator
import re

class EmailValidation:
    """Comprehensive email validation."""

    # Basic pattern
    BASIC_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Stricter pattern
    STRICT_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Disposable email domains
    DISPOSABLE_DOMAINS = {
        'tempmail.com', 'throwaway.email', 'guerrillamail.com',
        'mailinator.com', 'yopmail.com', 'temp-mail.org',
    }

    @classmethod
    def is_valid(cls, email: str) -> bool:
        if not re.match(cls.BASIC_PATTERN, email):
            return False
        domain = email.split('@')[1].lower()
        if domain in cls.DISPOSABLE_DOMAINS:
            return False
        return True

class ContactForm(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., max_length=255)
    subject: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=10, max_length=5000)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if not EmailValidation.is_valid(v):
            raise ValueError("Invalid or disposable email address")
        return v.lower()
```

### URL Validation

```python
from pydantic import BaseModel, Field, field_validator, HttpUrl
from urllib.parse import urlparse

class URLValidation:
    ALLOWED_SCHEMES = {"http", "https"}
    BLOCKED_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "metadata.google.internal"}
    BLOCKED_PORTS = {22, 23, 25, 53, 110, 143, 3389, 5432, 6379, 27017}

    @classmethod
    def is_safe(cls, url: str) -> bool:
        try:
            parsed = urlparse(url)

            if parsed.scheme not in cls.ALLOWED_SCHEMES:
                return False
            if parsed.hostname in cls.BLOCKED_HOSTS:
                return False
            if parsed.port and parsed.port in cls.BLOCKED_PORTS:
                return False
            return True
        except Exception:
            return False

class WebhookCreate(BaseModel):
    url: str = Field(..., max_length=2048)
    events: list[str] = Field(..., min_length=1)

    @field_validator("url")
    @classmethod
    def validate_url(cls, v):
        if not URLValidation.is_safe(v):
            raise ValueError("URL is not safe or uses disallowed scheme")
        return v

class WebsiteSettings(BaseModel):
    homepage_url: HttpUrl  # Built-in URL validation
    logo_url: Optional[HttpUrl] = None
    favicon_url: Optional[HttpUrl] = None
```

---

## 6. SQL Injection Prevention <a name="6-sql-injection"></a>

### SQLAlchemy Protection

```python
from sqlalchemy import text
from sqlalchemy.orm import Session

# GOOD - Parameterized query (SAFE)
def get_user_by_email(db: Session, email: str):
    result = db.execute(
        text("SELECT * FROM users WHERE email = :email"),
        {"email": email},
    )
    return result.fetchone()

# BAD - String concatenation (VULNERABLE)
def get_user_bad(db: Session, email: str):
    query = f"SELECT * FROM users WHERE email = '{email}'"  # DANGEROUS!
    result = db.execute(query)
    return result.fetchone()

# GOOD - SQLAlchemy ORM (SAFE)
def get_user_orm(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# GOOD - Dynamic query building (SAFE)
def search_users(db: Session, name: str = None, email: str = None, role: str = None):
    query = db.query(User)
    if name:
        query = query.filter(User.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(User.email == email)
    if role:
        query = query.filter(User.role == role)
    return query.all()
```

### Raw SQL Safety

```python
from fastapi import FastAPI, Query
from sqlalchemy import text

app = FastAPI()

@app.get("/search/")
async def search(
    q: str = Query(..., min_length=1, max_length=100),
    db: Session = Depends(get_db),
):
    # SAFE - Using parameterized query
    result = db.execute(
        text("SELECT * FROM items WHERE name ILIKE :search"),
        {"search": f"%{q}%"},
    )
    return result.fetchall()

@app.get("/users/")
async def list_users(
    sort_by: str = Query("name", pattern=r'^(name|email|created_at)$'),
    order: str = Query("asc", pattern=r'^(asc|desc)$'),
    db: Session = Depends(get_db),
):
    # SAFE - Sort field is validated by regex pattern
    query = f"SELECT * FROM users ORDER BY {sort_by} {order}"
    result = db.execute(text(query))
    return result.fetchall()
```

---

## 7. XSS Prevention <a name="7-xss"></a>

### Output Escaping

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from markupsafe import escape
import html

app = FastAPI()

@app.get("/profile/{username}")
async def get_profile(username: str):
    # Escape user input for HTML responses
    safe_username = html.escape(username)
    return HTMLResponse(
        f"<html><body><h1>Welcome, {safe_username}!</h1></body></html>"
    )

# Use with Jinja2 templates
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.get("/profile/{username}", response_class=HTMLResponse)
async def profile(request: Request, username: str):
    # Jinja2 auto-escapes by default
    return templates.TemplateResponse(
        "profile.html",
        {"request": request, "username": username},
    )
```

### Content Security Policy

```python
from starlette.middleware.base import BaseHTTPMiddleware

class CSPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )
        return response

app.add_middleware(CSPMiddleware)
```

### JSON Response Safety

```python
from fastapi.responses import JSONResponse
import json

@app.get("/api/data")
async def get_data():
    data = {"message": "Safe JSON response"}
    # JSON responses are automatically safe from XSS
    return JSONResponse(content=data)

# If returning HTML, always escape
@app.get("/search-results")
async def search_results(q: str):
    safe_q = html.escape(q)
    return HTMLResponse(
        f"<html><body>Results for: {safe_q}</body></html>"
    )
```

---

## 8. File Upload Validation <a name="8-file-upload"></a>

### Basic File Validation

```python
from fastapi import FastAPI, File, UploadFile, HTTPException
import magic
from pathlib import Path

app = FastAPI()

ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "application/pdf",
    "text/plain",
}

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".pdf", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_ext} not allowed",
        )

    # Read file content
    content = await file.read()

    # Check file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB",
        )

    # Check MIME type using magic bytes
    mime = magic.from_buffer(content, mime=True)
    if mime not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type {mime} not allowed",
        )

    # Verify file content matches extension
    if mime == "image/jpeg" and file_ext not in (".jpg", ".jpeg"):
        raise HTTPException(400, "File content doesn't match extension")

    return {"filename": file.filename, "size": len(content), "type": mime}
```

### Image Validation

```python
from PIL import Image
import io

@app.post("/upload/image/")
async def upload_image(file: UploadFile = File(...)):
    content = await file.read()

    # Validate MIME type
    mime = magic.from_buffer(content, mime=True)
    if not mime.startswith("image/"):
        raise HTTPException(400, "File must be an image")

    # Validate image dimensions
    try:
        img = Image.open(io.BytesIO(content))
        width, height = img.size

        if width < 100 or height < 100:
            raise HTTPException(400, "Image must be at least 100x100 pixels")
        if width > 4096 or height > 4096:
            raise HTTPException(400, "Image cannot exceed 4096x4096 pixels")

        # Verify format matches content
        format_map = {
            "image/jpeg": "JPEG",
            "image/png": "PNG",
            "image/gif": "GIF",
            "image/webp": "WEBP",
        }
        expected_format = format_map.get(mime)
        if expected_format and img.format != expected_format:
            raise HTTPException(400, "Image format doesn't match content")

    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(400, "Invalid image file")

    return {
        "filename": file.filename,
        "size": len(content),
        "dimensions": f"{width}x{height}",
        "format": img.format,
    }
```

### Multiple File Upload

```python
@app.post("/upload/multiple/")
async def upload_multiple_files(
    files: list[UploadFile] = File(..., max_length=10),
):
    results = []

    for file in files:
        content = await file.read()

        # Validate each file
        mime = magic.from_buffer(content, mime=True)
        if mime not in ALLOWED_MIME_TYPES:
            results.append({
                "filename": file.filename,
                "status": "rejected",
                "reason": f"Invalid file type: {mime}",
            })
            continue

        if len(content) > MAX_FILE_SIZE:
            results.append({
                "filename": file.filename,
                "status": "rejected",
                "reason": "File too large",
            })
            continue

        results.append({
            "filename": file.filename,
            "status": "accepted",
            "size": len(content),
        })

    return {"files": results}
```

---

## 9. Input Sanitization <a name="9-sanitization"></a>

### Text Sanitization

```python
import re
import html
from pydantic import field_validator

class SanitizedString:
    """String sanitization utilities."""

    @staticmethod
    def strip_html(text: str) -> str:
        """Remove HTML tags."""
        clean = re.sub(r'<[^>]+>', '', text)
        return html.unescape(clean)

    @staticmethod
    def sanitize_for_sql(text: str) -> str:
        """Basic SQL injection prevention."""
        dangerous_patterns = [
            r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE)\b)",
            r"(--|#|/\*|\*/)",
            r"(';|\";)",
        ]
        for pattern in dangerous_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        return text

    @staticmethod
    def sanitize_for_html(text: str) -> str:
        """Escape HTML entities."""
        return html.escape(text)

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Normalize whitespace."""
        return re.sub(r'\s+', ' ', text).strip()

    @staticmethod
    def remove_null_bytes(text: str) -> str:
        """Remove null bytes."""
        return text.replace('\x00', '')

class Comment(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)
    author_name: str = Field(..., min_length=1, max_length=100)

    @field_validator("content")
    @classmethod
    def sanitize_content(cls, v):
        v = SanitizedString.remove_null_bytes(v)
        v = SanitizedString.strip_html(v)
        v = SanitizedString.normalize_whitespace(v)
        return v

    @field_validator("author_name")
    @classmethod
    def sanitize_author(cls, v):
        v = SanitizedString.remove_null_bytes(v)
        v = SanitizedString.strip_html(v)
        v = SanitizedString.normalize_whitespace(v)
        if not v:
            raise ValueError("Author name cannot be empty")
        return v
```

### Filename Sanitization

```python
import os
import re
from pathlib import Path

def sanitize_filename(filename: str) -> str:
    """Sanitize a filename for safe storage."""
    # Remove null bytes
    filename = filename.replace('\x00', '')

    # Remove path separators
    filename = filename.replace('/', '').replace('\\', '')

    # Remove special characters
    filename = re.sub(r'[<>:"|?*]', '', filename)

    # Limit length
    name, ext = os.path.splitext(filename)
    if len(name) > 200:
        name = name[:200]

    # Prevent hidden files
    if name.startswith('.'):
        name = 'file' + name

    # Prevent reserved names (Windows)
    reserved = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'LPT1'}
    if name.upper() in reserved:
        name = 'file_' + name

    return name + ext

# Usage
@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    safe_name = sanitize_filename(file.filename)
    # Save with safe_name
```

---

## 10. Custom Validators <a name="10-custom"></a>

### Custom Pydantic Validators

```python
from pydantic import BaseModel, field_validator, model_validator
from typing import Any

class StrongPassword(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        errors = []
        if len(v) < 12:
            errors.append("at least 12 characters")
        if not any(c.isupper() for c in v):
            errors.append("an uppercase letter")
        if not any(c.islower() for c in v):
            errors.append("a lowercase letter")
        if not any(c.isdigit() for c in v):
            errors.append("a digit")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v):
            errors.append("a special character")

        # Check for common passwords
        common_passwords = {
            "password123", "123456789", "qwerty123",
            "admin123", "letmein123",
        }
        if v.lower() in common_passwords:
            errors.append("not a common password")

        if errors:
            raise ValueError(f"Password must contain: {', '.join(errors)}")
        return v

class ValidatedRegistration(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]{2,31}$', v):
            raise ValueError(
                "Username must start with a letter, be 3-32 chars, "
                "and contain only letters, numbers, underscores, or hyphens"
            )
        # Check for reserved words
        reserved = {'admin', 'root', 'system', 'api', 'www'}
        if v.lower() in reserved:
            raise ValueError("Username is reserved")
        return v.lower()

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError("Invalid email format")
        return v.lower()

    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
```

### Custom Type Validators

```python
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

class PhoneNumber(str):
    """Custom type for phone numbers."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(
            cls.validate_phone,
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def validate_phone(cls, v: str) -> str:
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', v)

        # US phone number
        if len(digits) == 10:
            return f"+1{digits}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"+{digits}"

        raise ValueError("Invalid phone number")

class ContactForm(BaseModel):
    name: str
    phone: PhoneNumber
```

---

## 11. Advanced Validation Patterns <a name="11-advanced"></a>

### Conditional Validation

```python
from pydantic import BaseModel, model_validator
from typing import Optional

class PaymentMethod(BaseModel):
    type: str  # "credit_card" or "paypal"
    card_number: Optional[str] = None
    card_expiry: Optional[str] = None
    paypal_email: Optional[str] = None

    @model_validator(mode="after")
    def validate_payment_method(self):
        if self.type == "credit_card":
            if not self.card_number:
                raise ValueError("Card number required for credit card")
            if not self.card_expiry:
                raise ValueError("Card expiry required for credit card")
            # Validate card number format
            if not re.match(r'^\d{16}$', self.card_number):
                raise ValueError("Invalid card number format")
        elif self.type == "paypal":
            if not self.paypal_email:
                raise ValueError("PayPal email required")
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.paypal_email):
                raise ValueError("Invalid PayPal email")
        return self
```

### Cross-Field Validation

```python
class EventCreate(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    min_attendees: int = 1
    max_attendees: int = 100
    venue_capacity: int

    @model_validator(mode="after")
    def validate_event(self):
        if self.start_date >= self.end_date:
            raise ValueError("Start date must be before end date")
        if self.min_attendees > self.max_attendees:
            raise ValueError("Min attendees cannot exceed max")
        if self.max_attendees > self.venue_capacity:
            raise ValueError("Max attendees cannot exceed venue capacity")
        if (self.end_date - self.start_date).total_seconds() < 3600:
            raise ValueError("Event must be at least 1 hour long")
        return self
```

### Dynamic Validation

```python
from pydantic import BaseModel, field_validator
from typing import Any

class DynamicForm(BaseModel):
    fields: dict[str, Any]
    field_types: dict[str, str]

    @field_validator("fields", mode="before")
    @classmethod
    def validate_fields(cls, v, info):
        if not isinstance(v, dict):
            raise ValueError("Fields must be a dictionary")
        return v

    def validate_field_values(self):
        """Validate field values against their declared types."""
        errors = {}
        for field_name, value in self.fields.items():
            field_type = self.field_types.get(field_name)
            if not field_type:
                continue

            try:
                if field_type == "email":
                    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', str(value)):
                        errors[field_name] = "Invalid email"
                elif field_type == "phone":
                    if not re.match(r'^\+?[1-9]\d{1,14}$', str(value)):
                        errors[field_name] = "Invalid phone"
                elif field_type == "url":
                    parsed = urlparse(str(value))
                    if not parsed.scheme or not parsed.netloc:
                        errors[field_name] = "Invalid URL"
            except Exception:
                errors[field_name] = f"Invalid {field_type}"

        if errors:
            raise ValueError(f"Validation errors: {errors}")
```

---

## 12. Best Practices <a name="12-best-practices"></a>

### 1. Validate Early, Validate Often

```python
# Validate at every layer
@app.post("/users/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Pydantic validates the schema
    # Additional business logic validation
    if await db.query(User).filter(User.email == user.email).first():
        raise HTTPException(400, "Email already registered")
    # Create user
```

### 2. Use Type Hints

```python
# GOOD - Type hints enable validation
def process_items(items: list[ItemCreate]) -> list[ItemResponse]:
    pass

# BAD - No validation
def process_items(items):
    pass
```

### 3. Return Consistent Error Responses

```python
from fastapi import HTTPException

class ValidationErrorDetail(BaseModel):
    field: str
    message: str
    type: str

class ValidationErrorResponse(BaseModel):
    detail: str
    errors: list[ValidationErrorDetail]

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": errors,
        },
    )
```

### 4. Use Pydantic v2 Features

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,  # Auto-strip strings
        validate_default=True,      # Validate default values
        extra="forbid",             # Forbid extra fields
    )

    name: str
    email: str
```

### 5. Test Your Validators

```python
import pytest
from pydantic import ValidationError

def test_valid_user():
    user = UserCreate(
        name="John",
        email="john@example.com",
        password="StrongP@ss123",
    )
    assert user.name == "John"

def test_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(name="John", email="invalid", password="StrongP@ss123")

def test_weak_password():
    with pytest.raises(ValidationError):
        UserCreate(name="John", email="john@example.com", password="weak")
```

---

## Summary

| Validation Type | FastAPI Tool | Example |
|----------------|-------------|---------|
| String length | `Field(min_length, max_length)` | `name: str = Field(min_length=1)` |
| Numeric range | `Field(ge, le, gt, lt)` | `age: int = Field(ge=0, le=150)` |
| Pattern match | `Field(pattern=...)` | `email: str = Field(pattern=r'...')` |
| Email format | Pydantic EmailStr | `email: EmailStr` |
| URL format | Pydantic HttpUrl | `url: HttpUrl` |
| Enum values | Python Enum | `role: UserRole` |
| Literal values | `Literal[...]` | `status: Literal["active", "inactive"]` |
| Custom logic | `@field_validator` | Complex business rules |
| Model-level | `@model_validator` | Cross-field validation |

### Security Checklist

- [ ] Validate all inputs at API boundary
- [ ] Use parameterized queries for SQL
- [ ] Escape HTML output
- [ ] Validate file uploads (type, size, content)
- [ ] Sanitize filenames
- [ ] Implement rate limiting
- [ ] Return consistent error responses
- [ ] Test all validation rules
