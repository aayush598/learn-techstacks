# Security Best Practices with FastAPI

## Table of Contents

1. [Password Hashing](#password-hashing)
2. [CORS Configuration](#cors-configuration)
3. [HTTPS Enforcement](#https-enforcement)
4. [Rate Limiting for Auth](#rate-limiting-for-auth)
5. [Account Lockout](#account-lockout)
6. [IP Allowlisting](#ip-allowlisting)
7. [Audit Logging](#audit-logging)
8. [Security Headers](#security-headers)
9. [Input Validation](#input-validation)
10. [Best Practices](#best-practices)
11. [Interview Questions](#interview-questions)

---

## Password Hashing

### Bcrypt

```python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # Work factor
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

### Argon2 (Recommended)

```python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=65536,   # 64 MB
    argon2__time_cost=3,         # 3 iterations
    argon2__parallelism=4,       # 4 threads
)
```

### Password Strength Validation

```python
import re
from pydantic import field_validator

class UserCreate(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Must contain uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Must contain lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Must contain digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Must contain special character")
        return v
```

### Common Password Check

```python
# Check against common passwords
COMMON_PASSWORDS = set(open("common_passwords.txt").read().splitlines())

def is_common_password(password: str) -> bool:
    return password.lower() in COMMON_PASSWORDS

@app.post("/register/")
async def register(user: UserCreate):
    if is_common_password(user.password):
        raise HTTPException(400, "Password is too common")
```

---

## CORS Configuration

### Basic CORS Setup

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com"],  # Specific origins
    allow_credentials=True,               # Allow cookies
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
    max_age=600,  # Cache preflight for 10 minutes
)
```

### Development vs Production

```python
import os

if os.getenv("ENVIRONMENT") == "development":
    # Allow all origins in development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # Restrict in production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://myapp.com",
            "https://www.myapp.com",
            "https://admin.myapp.com",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )
```

### Dynamic CORS

```python
from fastapi.middleware.cors import CORSMiddleware

ALLOWED_ORIGINS = [
    "https://myapp.com",
    "https://www.myapp.com",
]

def verify_origin(origin: str) -> bool:
    """Verify if origin is allowed."""
    return any(origin.endswith(domain) for domain in ALLOWED_ORIGINS)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
)
```

---

## HTTPS Enforcement

### Redirect HTTP to HTTPS

```python
@app.middleware("http")
async def https_redirect(request: Request, call_next):
    if request.url.scheme == "http":
        url = request.url.replace(scheme="https")
        return RedirectResponse(url, status_code=301)
    return await call_next(request)
```

### Trust Proxy Headers

```python
from fastapi import FastAPI

app = FastAPI()

# Trust proxy headers from load balancer
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*.myapp.com", "myapp.com"],
)

# If behind a reverse proxy, trust X-Forwarded headers
# In Starlette:
# request.url.scheme will be "https" if proxy sends X-Forwarded-Proto: https
```

### HSTS Header

```python
@app.middleware("http")
async def add_hsts_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains; preload"
    )
    return response
```

---

## Rate Limiting for Auth

### Login Rate Limiting

```python
import redis.asyncio as redis
from datetime import datetime

class LoginRateLimiter:
    def __init__(self, redis: redis.Redis):
        self.redis = redis

    async def is_locked_out(self, identifier: str) -> bool:
        """Check if identifier is locked out."""
        attempts = await self.redis.get(f"login_attempts:{identifier}")
        if attempts and int(attempts) >= 5:
            lockout = await self.redis.ttl(f"login_attempts:{identifier}")
            if lockout > 0:
                return True
        return False

    async def record_failed_attempt(self, identifier: str):
        """Record a failed login attempt."""
        key = f"login_attempts:{identifier}"
        attempts = await self.redis.incr(key)
        if attempts == 1:
            await self.redis.expire(key, 900)  # 15 minute window

    async def clear_attempts(self, identifier: str):
        """Clear attempts after successful login."""
        await self.redis.delete(f"login_attempts:{identifier}")

rate_limiter = LoginRateLimiter(redis_client)

@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None,
):
    identifier = f"{form_data.username}:{request.client.host}"

    if await rate_limiter.is_locked_out(identifier):
        raise HTTPException(
            status_code=429,
            detail="Too many failed attempts. Try again later.",
        )

    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        await rate_limiter.record_failed_attempt(identifier)
        raise HTTPException(401, "Invalid credentials")

    await rate_limiter.clear_attempts(identifier)
    # Return token...
```

### Per-IP Rate Limiting

```python
async def check_rate_limit(
    request: Request,
    r: redis.Redis = Depends(get_redis),
    max_requests: int = 100,
    window: int = 60,
):
    ip = request.client.host
    key = f"rate:{ip}"

    current = await r.incr(key)
    if current == 1:
        await r.expire(key, window)

    if current > max_requests:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(window)},
        )
```

---

## Account Lockout

### Lockout Strategy

```python
class AccountLockout:
    def __init__(self, redis: redis.Redis):
        self.redis = redis
        self.max_attempts = 5
        self.lockout_duration = 900  # 15 minutes

    async def is_locked(self, user_id: int) -> bool:
        key = f"lockout:{user_id}"
        return await self.redis.exists(key) > 0

    async def record_failure(self, user_id: int):
        key = f"failures:{user_id}"
        failures = await self.redis.incr(key)
        if failures == 1:
            await self.redis.expire(key, self.lockout_duration)

        if failures >= self.max_attempts:
            await self.redis.setex(
                f"lockout:{user_id}",
                self.lockout_duration,
                "locked",
            )

    async def reset(self, user_id: int):
        await self.redis.delete(f"failures:{user_id}")
        await self.redis.delete(f"lockout:{user_id}")

    async def get_remaining_attempts(self, user_id: int) -> int:
        failures = await self.redis.get(f"failures:{user_id}")
        return max(0, self.max_attempts - (int(failures) if failures else 0))

lockout = AccountLockout(redis_client)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user:
        raise HTTPException(401, "Invalid credentials")

    if await lockout.is_locked(user.id):
        raise HTTPException(
            423,
            "Account locked. Try again later.",
        )

    if not verify_password(form_data.password, user.hashed_password):
        await lockout.record_failure(user.id)
        remaining = await lockout.get_remaining_attempts(user.id)
        raise HTTPException(
            401,
            f"Invalid credentials. {remaining} attempts remaining.",
        )

    await lockout.reset(user.id)
    # Return token...
```

### Notification on Lockout

```python
async def record_failure(self, user_id: int):
    failures = await self.redis.incr(f"failures:{user_id}")

    if failures >= self.max_attempts:
        # Send notification
        user = get_user_by_id(user_id)
        await send_email(
            to=user.email,
            subject="Account Locked",
            body="Your account has been locked due to too many failed attempts.",
        )
```

---

## IP Allowlisting

### IP Whitelist

```python
from ipaddress import ip_address, ip_network

ALLOWED_IPS = [
    "192.168.1.0/24",       # Internal network
    "10.0.0.0/8",           # Another internal range
    "203.0.113.50",         # Specific IP
]

ALLOWED_NETWORKS = [ip_network(ip) for ip in ALLOWED_IPS]

def is_allowed_ip(ip: str) -> bool:
    try:
        addr = ip_address(ip)
        return any(addr in network for network in ALLOWED_NETWORKS)
    except ValueError:
        return False

@app.middleware("http")
async def ip_whitelist(request: Request, call_next):
    client_ip = request.client.host

    # Check forwarded headers (for reverse proxy)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()

    if not is_allowed_ip(client_ip):
        raise HTTPException(403, "IP not allowed")

    return await call_next(request)
```

### Admin IP Restriction

```python
admin_router = APIRouter(prefix="/admin")

@admin_router.middleware("http")
async def admin_ip_check(request: Request, call_next):
    client_ip = request.client.host
    if client_ip not in ADMIN_ALLOWED_IPS:
        raise HTTPException(403, "Admin access from this IP is not allowed")
    return await call_next(request)
```

---

## Audit Logging

### Audit Log Model

```python
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: int = mapped_column(primary_key=True)
    user_id: Optional[int] = mapped_column(ForeignKey("users.id"))
    action: str  # "login", "logout", "create", "update", "delete"
    resource: str  # "user", "item", "order"
    resource_id: Optional[str]
    details: Optional[dict]
    ip_address: str
    user_agent: str
    timestamp: datetime = mapped_column(default=datetime.utcnow)
    success: bool
```

### Audit Logger

```python
class AuditLogger:
    def __init__(self, db: Session):
        self.db = db

    def log(
        self,
        user_id: Optional[int],
        action: str,
        resource: str,
        resource_id: Optional[str] = None,
        details: Optional[dict] = None,
        ip_address: str = "",
        user_agent: str = "",
        success: bool = True,
    ):
        entry = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
        )
        self.db.add(entry)
        self.db.commit()

# Usage
@app.post("/login/")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    audit: AuditLogger = Depends(),
):
    user = authenticate_user(form_data.username, form_data.password)

    audit.log(
        user_id=user.id if user else None,
        action="login",
        resource="auth",
        ip_address=request.client.host,
        user_agent=str(request.headers.get("user-agent", "")),
        success=user is not None,
    )

    if not user:
        raise HTTPException(401, "Invalid credentials")
```

### Querying Audit Logs

```python
@app.get("/audit/")
async def get_audit_logs(
    user_id: Optional[int] = None,
    action: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    query = db.query(AuditLog)

    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    if action:
        query = query.filter(AuditLog.action == action)
    if start_date:
        query = query.filter(AuditLog.timestamp >= start_date)
    if end_date:
        query = query.filter(AuditLog.timestamp <= end_date)

    return query.order_by(AuditLog.timestamp.desc()).limit(1000).all()
```

---

## Security Headers

### Security Headers Middleware

```python
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)

    # Prevent MIME sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"

    # Prevent clickjacking
    response.headers["X-Frame-Options"] = "DENY"

    # XSS protection
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # HSTS
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains; preload"
    )

    # Content Security Policy
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
    )

    # Referrer Policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # Permissions Policy
    response.headers["Permissions-Policy"] = (
        "camera=(), microphone=(), geolocation=()"
    )

    # Remove server header
    if "server" in response.headers:
        del response.headers["server"]

    return response
```

---

## Input Validation

### SQL Injection Prevention

```python
# SQLAlchemy ORM prevents SQL injection by default
# BAD: Raw SQL with string formatting
query = f"SELECT * FROM users WHERE name = '{name}'"  # DANGEROUS!

# GOOD: Parameterized queries
from sqlalchemy import text
result = await db.execute(
    text("SELECT * FROM users WHERE name = :name"),
    {"name": name}
)

# GOOD: ORM queries
users = db.query(User).filter(User.name == name).all()
```

### XSS Prevention

```python
from markupsafe import escape

# Escape user input in responses
@app.get("/search/")
async def search(q: str):
    safe_query = escape(q)
    return {"query": safe_query}

# Pydantic automatically escapes in JSON responses
```

### File Upload Validation

```python
import magic

ALLOWED_TYPES = {
    "image/jpeg": [".jpg", ".jpeg"],
    "image/png": [".png"],
    "application/pdf": [".pdf"],
}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@app.post("/upload/")
async def upload_file(file: UploadFile):
    # Check file size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large")

    # Check MIME type
    mime = magic.from_buffer(content, mime=True)
    if mime not in ALLOWED_TYPES:
        raise HTTPException(400, "File type not allowed")

    # Check extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_TYPES[mime]:
        raise HTTPException(400, "File extension doesn't match content")
```

---

## Best Practices

### 1. Never Log Sensitive Data

```python
# BAD
logger.info(f"User login: {username}, password: {password}")

# GOOD
logger.info(f"User login attempt for: {username}")
```

### 2. Use Environment Variables for Secrets

```python
import os

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")
```

### 3. Validate All Input

```python
@app.post("/users/")
async def create_user(user: UserCreate):
    # Pydantic validates:
    # - Required fields
    # - Field types
    # - String lengths
    # - Email format
    # - Custom validators
    ...
```

### 4. Keep Dependencies Updated

```bash
pip-audit  # Check for vulnerabilities
safety check  # Check dependencies
```

### 5. Use Security Headers

```python
# Always include security headers
# See Security Headers section above
```

---

## Interview Questions

### Q1: What is the difference between hashing and encryption?
**Answer:** Hashing is one-way (can't reverse). Encryption is two-way (can decrypt). Passwords should be hashed, not encrypted. Use bcrypt or argon2 for password hashing.

### Q2: Why use bcrypt over MD5/SHA?
**Answer:** MD5/SHA are fast — making brute-force attacks feasible. bcrypt is deliberately slow (configurable work factor). Argon2 is even better — resistant to GPU attacks.

### Q3: How do you configure CORS in FastAPI?
**Answer:** Use `CORSMiddleware` with specific origins, methods, and headers. Never use `allow_origins=["*"]` in production with credentials.

### Q4: What is HSTS?
**Answer:** HTTP Strict Transport Security tells browsers to only use HTTPS for a specified time. Prevents downgrade attacks. Include in security headers.

### Q5: How do you prevent brute-force attacks?
**Answer:** Rate limiting (per IP and per account), account lockout after failed attempts, CAPTCHA after N failures, and monitoring for suspicious patterns.

### Q6: What are security headers?
**Answer:** HTTP headers that tell browsers how to behave securely. Include X-Content-Type-Options, X-Frame-Options, HSTS, CSP, and others.

### Q7: How do you handle file uploads securely?
**Answer:** Validate MIME type and extension, limit file size, store outside webroot, use random filenames, scan for malware, and never execute uploaded files.

### Q8: What is audit logging?
**Answer:** Recording security-relevant events (logins, permission changes, data access). Helps detect breaches, meet compliance requirements, and debug issues.

---

## Summary

Security in FastAPI requires multiple layers: proper password hashing (bcrypt/argon2), CORS configuration, HTTPS enforcement, rate limiting, input validation, security headers, and audit logging. Never store secrets in code, validate all input, and keep dependencies updated.
