# Security Interview Questions

## Table of Contents

1. [Basic Level (1-10)](#1-basic)
2. [Intermediate Level (11-20)](#2-intermediate)
3. [Advanced Level (21-30)](#3-advanced)
4. [Expert Level (31-40)](#4-expert)
5. [Practical Scenarios](#5-scenarios)
6. [Code Review Questions](#6-code-review)

---

## 1. Basic Level (1-10) <a name="1-basic"></a>

### Q1: What is the OWASP Top 10?

**Answer:** The OWASP Top 10 is a standard awareness document listing the most
critical web application security risks. The 2021 version includes:

1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable and Outdated Components
7. Identification and Authentication Failures
8. Software and Data Integrity Failures
9. Security Logging and Monitoring Failures
10. Server-Side Request Forgery (SSRF)

### Q2: What is SQL Injection and how to prevent it?

**Answer:** SQL Injection occurs when user input is directly included in SQL queries,
allowing attackers to manipulate the query.

```python
# VULNERABLE
query = f"SELECT * FROM users WHERE name = '{user_input}'"

# SAFE - Parameterized query
query = "SELECT * FROM users WHERE name = :name"
result = db.execute(text(query), {"name": user_input})

# SAFE - SQLAlchemy ORM
user = db.query(User).filter(User.name == user_input).first()
```

### Q3: What is XSS and how to prevent it?

**Answer:** XSS (Cross-Site Scripting) injects malicious scripts into web pages.

**Prevention:**
- Escape all user output in HTML
- Use Content-Security-Policy headers
- Validate and sanitize input
- Use templating engines with auto-escaping

```python
# Escape HTML
from markupsafe import escape
safe_output = escape(user_input)

# CSP header
response.headers["Content-Security-Policy"] = "script-src 'self'"
```

### Q4: What is CSRF?

**Answer:** Cross-Site Request Forgery tricks users into submitting requests they
didn't intend. FastAPI's `SameSite` cookie attribute and CSRF tokens prevent this.

```python
from starlette.middleware.csrf import CSRFMiddleware
app.add_middleware(CSRFMiddleware, secret=settings.CSRF_SECRET)
```

### Q5: How do you hash passwords in FastAPI?

**Answer:**
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

hashed = pwd_context.hash("password")
is_valid = pwd_context.verify("password", hashed)
```

### Q6: What is HTTPS and why is it important?

**Answer:** HTTPS encrypts data in transit using TLS. It prevents:
- Man-in-the-middle attacks
- Data eavesdropping
- Data tampering
- Session hijacking

```python
# Force HTTPS
@app.middleware("http")
async def redirect_https(request, call_next):
    if request.url.scheme == "http":
        return RedirectResponse(request.url.replace(scheme="https"))
    return await call_next(request)
```

### Q7: What are security headers?

**Answer:** HTTP headers that protect against common attacks:
- `Content-Security-Policy`: Prevents XSS
- `X-Frame-Options`: Prevents clickjacking
- `Strict-Transport-Security`: Forces HTTPS
- `X-Content-Type-Options`: Prevents MIME sniffing

### Q8: What is CORS?

**Answer:** Cross-Origin Resource Sharing controls which origins can access your API.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com"],  # NOT ["*"]
    allow_credentials=True,
    allow_methods=["GET", "POST"],
)
```

### Q9: What is rate limiting?

**Answer:** Rate limiting restricts how many requests a client can make in a time
period, preventing abuse.

```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.get("/api/data")
@limiter.limit("100/minute")
async def get_data():
    return {"data": "value"}
```

### Q10: What is input validation?

**Answer:** Validating all user input to ensure it meets expected formats.

```python
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    age: int = Field(..., ge=0, le=150)
```

---

## 2. Intermediate Level (11-20) <a name="2-intermediate"></a>

### Q11: What is Broken Access Control?

**Answer:** When users can access resources or perform actions beyond their
permissions.

```python
# VULNERABLE - No ownership check
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return db.query(Item).get(item_id)

# SAFE - Ownership check
@app.get("/items/{item_id}")
async def get_item(item_id: int, user: User = Depends(get_current_user)):
    item = db.query(Item).get(item_id)
    if item.owner_id != user.id:
        raise HTTPException(403, "Not authorized")
    return item
```

### Q12: What is Cryptographic Failure?

**Answer:** Exposure of sensitive data due to weak cryptography:
- Using MD5/SHA1 for passwords
- Storing data in plaintext
- Using weak encryption keys
- Not using HTTPS

### Q13: What is Insecure Design?

**Answer:** Security flaws in the design phase, including:
- Missing rate limiting
- No account lockout
- No input validation
- Missing security headers

### Q14: What is Security Misconfiguration?

**Answer:** Default or incomplete configurations:
- Default credentials
- Debug mode in production
- Missing security headers
- Open CORS policies
- Verbose error messages

### Q15: How do you secure JWT tokens?

**Answer:**
```python
# Short-lived access tokens (15 minutes)
access_token = create_access_token(data, expires_delta=timedelta(minutes=15))

# Longer-lived refresh tokens (7 days)
refresh_token = create_refresh_token(data, expires_delta=timedelta(days=7))

# Use RS256 (asymmetric) in production
token = jwt.encode(payload, private_key, algorithm="RS256")

# Store securely (HttpOnly, Secure, SameSite cookies)
response.set_cookie(
    "access_token",
    token,
    httponly=True,
    secure=True,
    samesite="strict",
)
```

### Q16: What is SSRF?

**Answer:** Server-Side Request Forgery makes the server fetch attacker-controlled
URLs.

```python
# VULNERABLE
@app.get("/fetch")
async def fetch(url: str):
    response = await httpx.get(url)  # Attacker can access internal services!

# SAFE - Validate URL
@app.get("/fetch")
async def fetch(url: str):
    if not is_safe_url(url):
        raise HTTPException(400, "Invalid URL")
    response = await httpx.get(url)
    return response.json()
```

### Q17: How do you secure file uploads?

**Answer:**
```python
@app.post("/upload")
async def upload(file: UploadFile):
    # Validate MIME type
    content = await file.read()
    mime = magic.from_buffer(content, mime=True)
    if mime not in ALLOWED_TYPES:
        raise HTTPException(400, "Invalid file type")

    # Validate size
    if len(content) > MAX_SIZE:
        raise HTTPException(413, "File too large")

    # Sanitize filename
    safe_name = sanitize_filename(file.filename)

    # Save outside web root
    save_path = UPLOAD_DIR / safe_name
```

### Q18: What is the difference between authentication and authorization?

**Answer:**
- **Authentication**: Verifying identity (who you are)
- **Authorization**: Verifying permissions (what you can do)

```python
# Authentication
@app.post("/login")
async def login(credentials: LoginRequest):
    user = authenticate_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")
    return {"token": create_token(user)}

# Authorization
@app.get("/admin/dashboard")
async def admin_dashboard(user: User = Depends(require_role("admin"))):
    return {"message": "Welcome, admin"}
```

### Q19: How do you implement account lockout?

**Answer:**
```python
@app.post("/login")
async def login(request: Request, credentials: LoginRequest, db = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()

    if user and user.failed_attempts >= 5:
        if user.lockout_until > datetime.utcnow():
            raise HTTPException(429, "Account locked")

    if not verify_password(credentials.password, user.hashed_password):
        if user:
            user.failed_attempts += 1
            if user.failed_attempts >= 5:
                user.lockout_until = datetime.utcnow() + timedelta(minutes=15)
            db.commit()
        raise HTTPException(401, "Invalid credentials")

    user.failed_attempts = 0
    db.commit()
    return {"token": create_token(user)}
```

### Q20: What is Content Security Policy?

**Answer:** CSP restricts which resources can be loaded, preventing XSS.

```python
response.headers["Content-Security-Policy"] = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self' 'unsafe-inline'; "
    "img-src 'self' data: https:; "
    "frame-ancestors 'none';"
)
```

---

## 3. Advanced Level (21-30) <a name="3-advanced"></a>

### Q21: How do you implement RBAC in FastAPI?

**Answer:**
```python
from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

def require_role(allowed_roles: list[Role]):
    async def role_checker(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(403, "Insufficient permissions")
        return user
    return role_checker

@app.get("/admin/users")
async def admin_only(user = Depends(require_role([Role.ADMIN]))):
    return db.query(User).all()

@app.get("/mod/queue")
async def moderator_queue(user = Depends(require_role([Role.ADMIN, Role.MODERATOR]))):
    return db.query(Report).filter(Report.status == "pending").all()
```

### Q22: How do you prevent timing attacks?

**Answer:**
```python
import hmac

# VULNERABLE - Variable-time comparison
if stored_hash == computed_hash:
    pass

# SAFE - Constant-time comparison
if hmac.compare_digest(stored_hash, computed_hash):
    pass
```

### Q23: How do you implement mutual TLS?

**Answer:**
```python
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_cert_chain("client-cert.pem", "client-key.pem")
context.load_verify_locations("ca-cert.pem")
context.verify_mode = ssl.CERT_REQUIRED

# Server-side verification
@app.middleware("http")
async def verify_client_cert(request, call_next):
    cert = request.scope.get("ssl_object")
    if not cert:
        raise HTTPException(401, "Client certificate required")
    # Verify certificate against trusted CAs
    return await call_next(request)
```

### Q24: How do you secure API keys?

**Answer:**
```python
# 1. Never expose in responses
@app.post("/api-keys")
async def create_api_key(user = Depends(get_current_user)):
    key = secrets.token_urlsafe(32)
    # Store hash, not the key itself
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    db.add(ApiKey(hash=key_hash, user_id=user.id))
    return {"key": key}  # Only shown once!

# 2. Verify by hashing
def verify_api_key(provided_key: str) -> bool:
    key_hash = hashlib.sha256(provided_key.encode()).hexdigest()
    return db.query(ApiKey).filter(ApiKey.hash == key_hash).first() is not None
```

### Q25: How do you implement request signing?

**Answer:**
```python
import hmac
import hashlib
import time

def sign_request(
    method: str,
    path: str,
    body: str,
    timestamp: str,
    secret: str,
) -> str:
    message = f"{method}\n{path}\n{timestamp}\n{body}"
    return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()

@app.middleware("http")
async def verify_request_signature(request, call_next):
    signature = request.headers.get("X-Signature")
    timestamp = request.headers.get("X-Timestamp")

    if not signature or not timestamp:
        raise HTTPException(401, "Missing signature")

    # Check freshness
    if abs(time.time() - float(timestamp)) > 300:
        raise HTTPException(401, "Request expired")

    body = (await request.body()).decode()
    expected = sign_request(
        request.method, request.url.path, body, timestamp, SECRET_KEY
    )

    if not hmac.compare_digest(expected, signature):
        raise HTTPException(401, "Invalid signature")

    return await call_next(request)
```

### Q26: How do you handle secrets in microservices?

**Answer:**
```python
# 1. Use a secret manager (Vault, AWS Secrets Manager)
# 2. Never pass secrets in URLs or logs
# 3. Use service mesh for service-to-service auth
# 4. Rotate secrets regularly
# 5. Use short-lived tokens

# HashiCorp Vault example
import hvac

client = hvac.Client(url="https://vault.internal:8200")
secrets = client.secrets.kv.v2.read_secret_version(path="myapp/db")
db_password = secrets["data"]["data"]["password"]
```

### Q27: How do you implement audit logging?

**Answer:**
```python
import structlog

logger = structlog.get_logger("audit")

@app.middleware("http")
async def audit_log(request, call_next):
    start = datetime.utcnow()
    response = await call_next(request)

    logger.info(
        "api_request",
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        ip=request.client.host,
        duration=(datetime.utcnow() - start).total_seconds(),
        user_id=getattr(request.state, "user_id", None),
    )
    return response
```

### Q28: How do you secure WebSocket connections?

**Answer:**
```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Authenticate before accepting
    token = websocket.query_params.get("token")
    if not token or not verify_token(token):
        await websocket.close(code=1008)  # Policy Violation
        return

    await websocket.accept()
    # ... handle messages
```

### Q29: How do you implement zero-trust security?

**Answer:**
```python
# 1. Verify every request
@app.middleware("http")
async def verify_everything(request, call_next):
    # Verify authentication
    # Verify authorization
    # Validate input
    # Check rate limits
    # Log the request
    return await call_next(request)

# 2. Principle of least privilege
@app.get("/items/{item_id}")
async def get_item(item_id: int, user = Depends(get_current_user)):
    item = db.query(Item).get(item_id)
    if item.owner_id != user.id and user.role != "admin":
        raise HTTPException(403, "Not authorized")
```

### Q30: How do you secure GraphQL APIs?

**Answer:**
```python
from strawberry.fastapi import GraphQLRouter
import strawberry

@strawberry.type
class Query:
    @strawberry.field
    async def users(self, info) -> list[User]:
        # Authenticate
        user = info.context.get("user")
        if not user:
            raise Exception("Not authenticated")

        # Authorize
        if user.role != "admin":
            raise Exception("Not authorized")

        return db.query(User).all()
```

---

## 4. Expert Level (31-40) <a name="4-expert"></a>

### Q31: How do you implement defense in depth?

**Answer:** Multiple layers of security controls:

```python
# Layer 1: Network (TLS, firewall)
# Layer 2: Rate limiting
@app.get("/api/data")
@limiter.limit("100/minute")
async def get_data(request: Request):
    # Layer 3: Authentication
    user = Depends(get_current_user)
    # Layer 4: Authorization
    if user.role != "admin":
        raise HTTPException(403)
    # Layer 5: Input validation
    # Layer 6: Output encoding
    # Layer 7: Audit logging
```

### Q32: How do you detect and prevent credential stuffing?

**Answer:**
```python
# 1. Rate limiting per IP
@limiter.limit("5/minute")
async def login(request: Request):
    pass

# 2. Account lockout after failed attempts
# 3. CAPTCHA after failed attempts
# 4. Detect patterns (many accounts, same IP)
# 5. Use breached password databases
# 6. Monitor for unusual login patterns
```

### Q33: How do you implement data encryption at rest?

**Answer:**
```python
from cryptography.fernet import Fernet

class FieldEncryptor:
    def __init__(self, key: bytes):
        self.fernet = Fernet(key)

    def encrypt_field(self, value: str) -> str:
        return self.fernet.encrypt(value.encode()).decode()

    def decrypt_field(self, encrypted: str) -> str:
        return self.fernet.decrypt(encrypted.encode()).decode()

# SQLAlchemy column type
from sqlalchemy import TypeDecorator

class EncryptedString(TypeDecorator):
    impl = String

    def __init__(self, key: bytes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.encryptor = FieldEncryptor(key)

    def process_bind_param(self, value, dialect):
        if value is not None:
            return self.encryptor.encrypt_field(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return self.encryptor.decrypt_field(value)
        return value
```

### Q34: How do you implement secure session management?

**Answer:**
```python
import secrets
from datetime import datetime, timedelta

class SessionManager:
    def __init__(self, redis):
        self.redis = redis
        self.session_ttl = timedelta(hours=24)

    def create_session(self, user_id: int) -> str:
        session_id = secrets.token_urlsafe(32)
        session_data = {
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "ip_address": None,
            "user_agent": None,
        }
        self.redis.setex(
            f"session:{session_id}",
            self.session_ttl,
            json.dumps(session_data),
        )
        return session_id

    def validate_session(self, session_id: str, request: Request) -> dict:
        data = self.redis.get(f"session:{session_id}")
        if not data:
            return None

        session = json.loads(data)

        # Validate IP and User-Agent (optional)
        if session.get("ip_address") != request.client.host:
            self.invalidate_session(session_id)
            return None

        return session
```

### Q35: How do you implement OAuth 2.0 correctly?

**Answer:**
```python
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@app.get("/auth/google")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/google/callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    # Create or login user
```

### Q36: How do you handle security incidents?

**Answer:**
1. **Detection**: Monitor logs, alerts, anomalies
2. **Containment**: Isolate affected systems
3. **Eradication**: Remove threat
4. **Recovery**: Restore from clean backups
5. **Lessons Learned**: Update security measures

### Q37: How do you implement audit trails?

**Answer:**
```python
from datetime import datetime

class AuditTrail:
    def __init__(self, db):
        self.db = db

    async def log(
        self,
        action: str,
        resource_type: str,
        resource_id: str,
        user_id: int,
        details: dict = None,
        ip_address: str = None,
    ):
        audit = AuditLog(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            details=details,
            ip_address=ip_address,
            timestamp=datetime.utcnow(),
        )
        self.db.add(audit)
        await self.db.commit()
```

### Q38: How do you secure Docker containers?

**Answer:**
```dockerfile
# Run as non-root user
FROM python:3.12-slim
RUN useradd --create-home appuser
WORKDIR /app
COPY --chown=appuser:appuser . .
USER appuser

# Don't store secrets in image
# Use Docker secrets or environment variables
# Scan image for vulnerabilities
```

### Q39: How do you implement secrets rotation?

**Answer:**
```python
class SecretRotator:
    def __init__(self, secret_manager, db):
        self.secret_manager = secret_manager
        self.db = db

    async def rotate_database_password(self):
        new_password = generate_strong_password()

        # Update database
        await self.db.execute(
            text("ALTER USER app WITH PASSWORD :pw"),
            {"pw": new_password},
        )

        # Update secret store
        await self.secret_manager.update_secret(
            "database/password",
            new_password,
        )

        # Update application (restart or hot-reload)
        await self.restart_application()
```

### Q40: How do you perform security testing?

**Answer:**
```python
# 1. Static Analysis (SAST)
# bandit -r app/

# 2. Dynamic Analysis (DAST)
# OWASP ZAP, Burp Suite

# 3. Dependency Scanning
# safety check -r requirements.txt

# 4. Penetration Testing
# Manual testing of authentication, authorization, input validation

# 5. Security Headers Check
# curl -I https://yourapp.com

# 6. SSL/TLS Testing
# ssllabs.com/ssltest/
```

---

## 5. Practical Scenarios <a name="5-scenarios"></a>

### Scenario 1: "Your API has a SQL injection vulnerability"

**Answer:**
```python
# 1. Find and fix the vulnerability
# Replace string interpolation with parameterized queries
# 2. Deploy fix immediately
# 3. Audit all database queries
# 4. Add automated security testing
# 5. Review access logs for exploitation
```

### Scenario 2: "A user claims their account was hacked"

**Answer:**
```python
# 1. Check login history for unusual activity
# 2. Verify authentication logs
# 3. Check for credential stuffing
# 4. Force password reset
# 5. Enable MFA
# 6. Review session management
```

### Scenario 3: "You need to secure a payment API"

**Answer:**
```python
# 1. Never store card numbers (use Stripe/Braintree)
# 2. Validate all input
# 3. Use idempotency keys
# 4. Implement webhook signature verification
# 5. Log all transactions
# 6. Use PCI-compliant payment processor
```

---

## 6. Code Review Questions <a name="6-code-review"></a>

### Q: Find the security issues

```python
@app.get("/users/")
async def get_users(name: str):
    query = f"SELECT * FROM users WHERE name = '{name}'"
    result = db.execute(query)
    return result.fetchall()
```

**Issues:**
1. SQL Injection - string interpolation in query
2. No authentication required
3. No input validation
4. No rate limiting

### Q: Fix this code

```python
@app.post("/login")
async def login(email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if user.password == password:
        return {"token": "abc123"}
    return {"error": "wrong password"}
```

**Issues:**
1. Plaintext password comparison
2. Hardcoded token
3. No rate limiting
4. Error message reveals user existence
5. No password hashing

---

## Summary

### Security Checklist

- [ ] Input validation on all endpoints
- [ ] Parameterized queries (SQLAlchemy)
- [ ] Password hashing (Argon2/bcrypt)
- [ ] HTTPS enforced
- [ ] Security headers configured
- [ ] CORS properly configured
- [ ] Rate limiting implemented
- [ ] Authentication on sensitive endpoints
- [ ] Authorization checks on all resources
- [ ] No secrets in code/logs
- [ ] Audit logging enabled
- [ ] Error messages don't leak info
- [ ] File upload validation
- [ ] CSRF protection
- [ ] XSS prevention

### Quick Reference

| Threat | Prevention |
|--------|-----------|
| SQL Injection | Parameterized queries, ORM |
| XSS | Output escaping, CSP |
| CSRF | SameSite cookies, CSRF tokens |
| Brute Force | Rate limiting, account lockout |
| MITM | HTTPS, HSTS |
| Clickjacking | X-Frame-Options, CSP |
| Data Breach | Encryption at rest, access control |
| Secret Exposure | Secret managers, env variables |
