# OWASP Top 10 with FastAPI

## Table of Contents

1. [Introduction](#1-introduction)
2. [A01: Broken Access Control](#2-broken-access-control)
3. [A02: Cryptographic Failures](#3-cryptographic-failures)
4. [A03: Injection](#4-injection)
5. [A04: Insecure Design](#5-insecure-design)
6. [A05: Security Misconfiguration](#6-security-misconfiguration)
7. [A06: Vulnerable and Outdated Components](#7-vulnerable-components)
8. [A07: Identification and Authentication Failures](#8-auth-failures)
9. [A08: Software and Data Integrity Failures](#9-integrity-failures)
10. [A09: Security Logging and Monitoring Failures](#10-logging-failures)
11. [A10: Server-Side Request Forgery (SSRF)](#11-ssrf)
12. [OWASP Checklist](#12-checklist)

---

## 1. Introduction <a name="1-introduction"></a>

The OWASP Top 10 is a standard awareness document for web application security,
published by the Open Worldwide Application Security Project (OWASP). It represents
a broad consensus about the most critical security risks to web applications.

FastAPI provides many built-in protections, but developers must understand and
properly use these features to build secure applications.

---

## 2. A01: Broken Access Control <a name="2-broken-access-control"></a>

### What It Is

Broken Access Control allows users to act outside their intended permissions.
This can lead to unauthorized data disclosure, modification, or destruction.

**Common Vulnerabilities:**
- Violation of the principle of least privilege
- Bypassing access control checks by modifying the URL, API requests, or HTML page
- Viewing or editing someone else's account by providing its unique identifier
- Accessing API with missing access controls for POST, PUT, and DELETE
- Escalating privileges by acting as a user without being logged in

### How FastAPI Helps

FastAPI's dependency injection system makes access control straightforward:

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Role-based access control
class Role:
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

def require_role(allowed_roles: list[str]):
    async def role_checker(token: str = Depends(oauth2_scheme)):
        user = await get_current_user(token)
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user
    return role_checker

# Resource-based access control
def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get("/users/me")
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
):
    return current_user

@app.get("/users/{user_id}")
async def read_user(
    user_id: int,
    current_user: User = Depends(require_role([Role.ADMIN])),
):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Admin-only endpoint
@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_role([Role.ADMIN])),
):
    if current_user.id == user_id:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete yourself",
        )
    await delete_user_service(user_id)
    return {"detail": "User deleted"}
```

### How to Fix

```python
# 1. Always verify ownership of resources
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: ItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Check ownership
    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Update item
    for key, value in item.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    return db_item

# 2. Use row-level security in database queries
@app.get("/orders/")
async def list_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Only return orders belonging to the current user
    orders = db.query(Order).filter(
        Order.user_id == current_user.id
    ).all()
    return orders

# 3. Implement proper CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

---

## 3. A02: Cryptographic Failures <a name="3-cryptographic-failures"></a>

### What It Is

Cryptographic Failures occur when sensitive data is exposed due to weak or
improperly implemented cryptography.

**Common Vulnerabilities:**
- Data transmitted in clear text (HTTP, FTP, SMTP)
- Old or weak cryptographic algorithms
- Default crypto keys in use
- Missing or weak crypto key management
- Missing enforced TLS/HTTPS

### How FastAPI Helps

```python
from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

# Force HTTPS in production
@app.middleware("http")
async def force_https(request, call_next):
    if request.url.scheme == "http":
        url = request.url.replace(scheme="https")
        return RedirectResponse(url, status_code=301)
    response = await call_next(request)
    return response
```

### How to Fix

```python
# 1. Password hashing with bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 2. Password hashing with Argon2 (recommended)
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto",
    argon2__memory_cost=65536,  # 64MB
    argon2__time_cost=3,
    argon2__parallelism=4,
)

# 3. Encrypt sensitive data at rest
from cryptography.fernet import Fernet

# Generate key: Fernet.generate_key()
SECRET_KEY = "your-secret-key-here"
cipher = Fernet(SECRET_KEY)

def encrypt_data(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    return cipher.decrypt(encrypted_data.encode()).decode()

# 4. Environment-based configuration
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    REDIS_URL: str
    JWT_SECRET_KEY: str

    class Config:
        env_file = ".env"

# 5. JWT with proper signing
from datetime import datetime, timedelta
from jose import jwt

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm="HS256",  # Use RS256 for production
    )
```

---

## 4. A03: Injection <a name="4-injection"></a>

### What It Is

Injection vulnerabilities occur when untrusted data is sent to an interpreter as
part of a command or query.

**Types:**
- SQL Injection
- NoSQL Injection
- OS Command Injection
- LDAP Injection
- Cross-Site Scripting (XSS)

### How FastAPI Helps

FastAPI with Pydantic provides automatic input validation, and SQLAlchemy uses
parameterized queries by default:

```python
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
import re

app = FastAPI()

# Pydantic validates input automatically
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

# SQLAlchemy uses parameterized queries
@app.post("/users/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # SQL Injection PREVENTED - SQLAlchemy parameterizes this
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    return db_user
```

### How to Fix

```python
# 1. SQL Injection Prevention
# BAD - NEVER do this
@app.get("/users/")
async def get_user(name: str):
    query = f"SELECT * FROM users WHERE name = '{name}'"  # VULNERABLE!
    result = db.execute(query)

# GOOD - Use SQLAlchemy ORM or parameterized queries
@app.get("/users/")
async def get_user(name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == name).first()
    return user

# GOOD - Even raw SQL with parameters
@app.get("/users/")
async def get_user(name: str, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT * FROM users WHERE name = :name"),
        {"name": name},
    )
    return result.fetchone()

# 2. XSS Prevention
from markupsafe import escape

@app.get("/search")
async def search(q: str):
    # Escape user input for HTML responses
    safe_query = escape(q)
    return {"query": safe_query}

# 3. NoSQL Injection Prevention
@app.post("/users/")
async def create_user(user: UserCreate):
    # BAD - vulnerable to NoSQL injection
    # user_dict = {"$where": "function() { return true; }"}

    # GOOD - validate input types
    if not isinstance(user.name, str):
        raise HTTPException(status_code=400, detail="Invalid name")
    return await db.users.insert_one(user.dict())

# 4. Command Injection Prevention
import subprocess

@app.get("/ping/")
async def ping(host: str = Query(..., pattern=r'^[a-zA-Z0-9.-]+$')):
    # BAD - vulnerable to command injection
    # result = subprocess.run(f"ping -c 1 {host}", shell=True)

    # GOOD - use list form with validated input
    result = subprocess.run(
        ["ping", "-c", "1", host],
        capture_output=True,
        text=True,
        timeout=5,
    )
    return {"output": result.stdout}

# 5. Input Validation with Pydantic
from pydantic import field_validator

class SafeInput(BaseModel):
    name: str
    email: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not re.match(r'^[a-zA-Z\s]+$', v):
            raise ValueError("Name must contain only letters and spaces")
        if len(v) > 100:
            raise ValueError("Name too long")
        return v.strip()
```

---

## 5. A04: Insecure Design <a name="5-insecure-design"></a>

### What It Is

Insecure Design refers to risks related to design flaws, missing or ineffective
security controls, and poor security architecture patterns.

### How to Fix

```python
# 1. Implement rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter

@app.get("/login")
@limiter.limit("5/minute")
async def login(request: Request, credentials: LoginRequest):
    user = await authenticate(credentials)
    if not user:
        raise HTTPException(status_code=401)
    return {"token": create_token(user)}

# 2. Implement account lockout
@app.post("/login")
async def login(request: Request, credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()

    if user and user.failed_login_attempts >= 5:
        if user.lockout_until > datetime.utcnow():
            raise HTTPException(
                status_code=429,
                detail="Account locked. Try again later.",
            )
        # Reset lockout
        user.failed_login_attempts = 0
        user.lockout_until = None

    if not user or not verify_password(credentials.password, user.hashed_password):
        if user:
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:
                user.lockout_until = datetime.utcnow() + timedelta(minutes=15)
            db.commit()
        raise HTTPException(status_code=401)

    # Reset failed attempts on success
    user.failed_login_attempts = 0
    user.lockout_until = None
    db.commit()

    return {"token": create_token(user)}

# 3. Implement proper password policy
from pydantic import field_validator

class PasswordChange(BaseModel):
    old_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 12:
            raise ValueError("Password must be at least 12 characters")
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must contain uppercase letter")
        if not re.search(r'[a-z]', v):
            raise ValueError("Password must contain lowercase letter")
        if not re.search(r'\d', v):
            raise ValueError("Password must contain digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Password must contain special character")
        return v

# 4. Implement idempotency for critical operations
import uuid

@app.post("/orders/")
async def create_order(
    order: OrderCreate,
    idempotency_key: str = Header(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check if this idempotency key was already used
    existing = db.query(Order).filter(
        Order.idempotency_key == idempotency_key
    ).first()

    if existing:
        return existing  # Return existing order

    # Create new order
    order = Order(
        user_id=current_user.id,
        idempotency_key=idempotency_key,
        **order.dict(),
    )
    db.add(order)
    db.commit()
    return order
```

---

## 6. A05: Security Misconfiguration <a name="6-security-misconfiguration"></a>

### What It Is

Security Misconfiguration is the most common vulnerability, including:
- Default credentials
- Incomplete or ad hoc configurations
- Open cloud storage
- Verbose error messages
- Missing security headers

### How to Fix

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

# 1. CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com"],  # NOT ["*"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# 2. Trusted Hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["myapp.com", "*.myapp.com"],
)

# 3. Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )
        return response

app.add_middleware(SecurityHeadersMiddleware)

# 4. Disable debug mode in production
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool = False
    TESTING: bool = False

    class Config:
        env_file = ".env"

settings = Settings()

if settings.DEBUG:
    # Only expose detailed errors in development
    @app.exception_handler(Exception)
    async def generic_exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

# 5. Custom error handlers (don't expose internals)
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
```

---

## 7. A06: Vulnerable and Outdated Components <a name="7-vulnerable-components"></a>

### What It Is

Using components with known vulnerabilities, including libraries, frameworks, and
other software modules.

### How to Fix

```bash
# 1. Check for known vulnerabilities
pip install safety
safety check -r requirements.txt

# 2. Use pip-audit
pip install pip-audit
pip-audit -r requirements.txt

# 3. Keep dependencies updated
pip install --upgrade pip
pip install --upgrade -r requirements.txt

# 4. Use dependabot or renovate for automated updates
# .github/dependabot.yml
```

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

```python
# 5. Pin dependencies
# requirements.txt
fastapi==0.109.0
uvicorn==0.27.0
sqlalchemy==2.0.25
pydantic==2.5.3

# 6. Use lock files
# pip install pip-tools
# pip-compile requirements.in
```

---

## 8. A07: Identification and Authentication Failures <a name="8-auth-failures"></a>

### What It Is

Weaknesses in authentication mechanisms, including:
- Permitting brute force attacks
- Permitting weak passwords
- Missing multi-factor authentication
- Exposing session identifiers in URLs

### How to Fix

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
import secrets

app = FastAPI()

# 1. Strong JWT configuration
SECRET_KEY = secrets.token_urlsafe(32)  # Generate a strong key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # Short-lived access tokens
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 2. Secure token refresh
@app.post("/token/refresh")
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    new_access_token = create_access_token(data={"sub": user_id})
    return {"access_token": new_access_token, "token_type": "bearer"}

# 3. Password validation
from pydantic import field_validator

class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 12:
            raise ValueError("Password must be at least 12 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain lowercase")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        if not any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in v):
            raise ValueError("Password must contain special character")
        return v

# 4. Implement logout (token blacklist)
from redis import Redis

redis = Redis()
TOKEN_BLACKLIST_PREFIX = "blacklist:"

@app.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme),
    current_user: User = Depends(get_current_user),
):
    # Add token to blacklist
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        ttl = exp - datetime.utcnow().timestamp()
        if ttl > 0:
            redis.setex(
                f"{TOKEN_BLACKLIST_PREFIX}{token}",
                int(ttl),
                "blacklisted",
            )
    except JWTError:
        pass
    return {"detail": "Logged out"}

# 5. Session management
@app.post("/login")
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    # Store session info
    session_id = secrets.token_urlsafe(32)
    redis.setex(
        f"session:{session_id}",
        timedelta(days=7),
        json.dumps({"user_id": user.id, "refresh_token": refresh_token}),
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "session_id": session_id,
        "token_type": "bearer",
    }
```

---

## 9. A08: Software and Data Integrity Failures <a name="9-integrity-failures"></a>

### What It Is

Failures related to code and infrastructure that does not protect against integrity
violations, such as insecure CI/CD pipelines or auto-updates without verification.

### How to Fix

```python
# 1. Verify file integrity
import hashlib

def verify_file_hash(file_path: str, expected_hash: str) -> bool:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest() == expected_hash

# 2. Use signed JWTs
from jose import jwt

# Verify JWT signature
def verify_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["RS256"],  # Use asymmetric signing
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# 3. Implement CSRF protection
from starlette.middleware.csrf import CSRFMiddleware

app.add_middleware(CSRFMiddleware, secret=settings.CSRF_SECRET)

# 4. Secure data serialization
import json
from cryptography.fernet import Fernet

def secure_serialize(data: dict) -> str:
    """Serialize and encrypt data."""
    json_data = json.dumps(data, sort_keys=True)
    cipher = Fernet(settings.DATA_KEY)
    return cipher.encrypt(json_data.encode()).decode()

def secure_deserialize(encrypted_data: str) -> dict:
    """Decrypt and deserialize data."""
    cipher = Fernet(settings.DATA_KEY)
    json_data = cipher.decrypt(encrypted_data.encode()).decode()
    return json.loads(json_data)
```

---

## 10. A09: Security Logging and Monitoring Failures <a name="10-logging-failures"></a>

### What It Is

Insufficient logging, detection, monitoring, and active response allows attackers
to further attack systems, maintain persistence, and tamper with data.

### How to Fix

```python
import logging
from datetime import datetime

# 1. Configure structured logging
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
)

logger = structlog.get_logger()

# 2. Log security events
@app.post("/login")
async def login(request: Request, credentials: LoginRequest, db: Session = Depends(get_db)):
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent", "unknown")

    user = authenticate_user(db, credentials.email, credentials.password)

    if not user:
        logger.warning(
            "Failed login attempt",
            email=credentials.email,
            ip_address=ip_address,
            user_agent=user_agent,
            event_type="auth_failure",
        )
        raise HTTPException(status_code=401, detail="Invalid credentials")

    logger.info(
        "Successful login",
        user_id=user.id,
        ip_address=ip_address,
        event_type="auth_success",
    )

    return {"token": create_token(user)}

# 3. Audit trail
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    action = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    resource_id = Column(String, nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

def log_audit(
    db: Session,
    action: str,
    resource_type: str,
    resource_id: str = None,
    details: dict = None,
    user_id: int = None,
    ip_address: str = None,
):
    audit = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address,
    )
    db.add(audit)
    db.commit()

# 4. Security event monitoring
@app.middleware("http")
async def security_monitoring(request: Request, call_next):
    start_time = datetime.utcnow()

    # Check for suspicious patterns
    suspicious_patterns = [
        "../",  # Path traversal
        "<script>",  # XSS
        "UNION SELECT",  # SQL injection
        "etc/passwd",  # File inclusion
    ]

    request_str = str(request.url) + str(request.headers)
    for pattern in suspicious_patterns:
        if pattern.lower() in request_str.lower():
            logger.warning(
                "Suspicious request detected",
                url=str(request.url),
                pattern=pattern,
                ip_address=request.client.host,
                event_type="suspicious_request",
            )
            break

    response = await call_next(request)

    duration = (datetime.utcnow() - start_time).total_seconds()
    logger.info(
        "Request processed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration=duration,
        ip_address=request.client.host,
    )

    return response
```

---

## 11. A10: Server-Side Request Forgery (SSRF) <a name="11-ssrf"></a>

### What It Is

SSRF flaws occur when a web application fetches a remote resource without
validating the user-supplied URL, allowing an attacker to force the application
to send crafted requests to unexpected destinations.

### How to Fix

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import HttpUrl, field_validator
import ipaddress
import socket
from urllib.parse import urlparse

app = FastAPI()

# 1. URL Validation
def validate_url(url: str) -> bool:
    """Validate URL is safe to fetch."""
    try:
        parsed = urlparse(url)

        # Only allow HTTP and HTTPS
        if parsed.scheme not in ("http", "https"):
            return False

        # Resolve hostname to IP
        hostname = parsed.hostname
        if not hostname:
            return False

        ip = socket.gethostbyname(hostname)

        # Block private IPs
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_private:
            return False
        if ip_obj.is_loopback:
            return False
        if ip_obj.is_link_local:
            return False

        # Block common internal services
        blocked_ports = {22, 23, 25, 53, 110, 143, 3389, 5432, 6379, 27017}
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        if port in blocked_ports:
            return False

        return True

    except (socket.gaierror, ValueError):
        return False

@app.get("/fetch-url")
async def fetch_url(url: str = Query(...)):
    if not validate_url(url):
        raise HTTPException(
            status_code=400,
            detail="Invalid or disallowed URL",
        )

    # Safe to fetch
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=5.0)
        return {"content": response.text[:1000]}

# 2. Pydantic URL validation
class WebhookCreate(BaseModel):
    url: HttpUrl

    @field_validator("url")
    @classmethod
    def validate_webhook_url(cls, v):
        if not validate_url(str(v)):
            raise ValueError("URL points to a private/internal resource")
        return v

@app.post("/webhooks/")
async def create_webhook(webhook: WebhookCreate):
    # URL is validated
    return {"url": webhook.url, "status": "created"}

# 3. Allowlist approach
ALLOWED_HOSTS = ["api.external-service.com", "cdn.example.com"]

def is_url_allowed(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.hostname in ALLOWED_HOSTS
```

---

## 12. OWASP Checklist <a name="12-checklist"></a>

### FastAPI Security Checklist

```markdown
## Access Control
- [ ] Implement role-based access control (RBAC)
- [ ] Verify resource ownership on every request
- [ ] Use dependency injection for auth checks
- [ ] Implement CORS with specific origins
- [ ] Add rate limiting

## Cryptography
- [ ] Use bcrypt or Argon2 for passwords
- [ ] Use RS256 for JWT signing in production
- [ ] Enforce HTTPS
- [ ] Don't store secrets in code
- [ ] Use environment variables

## Input Validation
- [ ] Validate all inputs with Pydantic
- [ ] Use parameterized queries (SQLAlchemy)
- [ ] Escape output for HTML responses
- [ ] Validate file uploads
- [ ] Implement input length limits

## Configuration
- [ ] Disable debug mode in production
- [ ] Add security headers
- [ ] Use trusted hosts
- [ ] Remove default credentials
- [ ] Minimize error messages

## Dependencies
- [ ] Pin all dependencies
- [ ] Run security scans regularly
- [ ] Use dependabot for updates
- [ ] Audit dependencies periodically

## Authentication
- [ ] Implement account lockout
- [ ] Use strong password policies
- [ ] Implement token refresh
- [ ] Add multi-factor authentication
- [ ] Invalidate tokens on logout

## Logging
- [ ] Log all security events
- [ ] Monitor for suspicious activity
- [ ] Don't log sensitive data
- [ ] Implement audit trails
- [ ] Set up alerts for anomalies

## SSRF Prevention
- [ ] Validate all URLs
- [ ] Block private IP ranges
- [ ] Use allowlists for external URLs
- [ ] Implement request timeouts
- [ ] Monitor outgoing requests
```

---

## Summary

| OWASP Risk | FastAPI Protection | Key Fix |
|-----------|-------------------|---------|
| Broken Access Control | Dependency injection | Verify ownership on every request |
| Cryptographic Failures | Built-in HTTPS support | Use bcrypt/Argon2, strong JWT keys |
| Injection | Pydantic + SQLAlchemy | Parameterized queries, input validation |
| Insecure Design | N/A (design-time) | Rate limiting, account lockout |
| Security Misconfiguration | CORS middleware | Security headers, disable debug |
| Vulnerable Components | N/A (dependency mgmt) | Pin deps, run security scans |
| Auth Failures | OAuth2 support | Strong passwords, MFA, short tokens |
| Integrity Failures | JWT verification | Signed tokens, CSRF protection |
| Logging Failures | N/A (manual setup) | Structured logging, audit trails |
| SSRF | N/A (manual validation) | URL validation, block private IPs |
