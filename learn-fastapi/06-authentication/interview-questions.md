# Authentication Interview Questions

## 30+ Questions for Authentication Mastery

---

## JWT

### Q1: What is JWT and what are its three parts?

**Answer:** JWT (JSON Web Token) has three Base64-encoded parts separated by dots:

```
Header.Payload.Signature
```

**Header:**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload (claims):**
```json
{
  "sub": "user123",
  "role": "admin",
  "exp": 1700000000,
  "iat": 1699996400
}
```

**Signature:**
```
HMACSHA256(base64(header) + "." + base64(payload), secret)
```

The signature ensures the token hasn't been tampered with. Anyone can decode the header and payload, but only the server can create/verify the signature.

---

### Q2: What is the difference between HS256 and RS256?

**Answer:**

| Aspect | HS256 | RS256 |
|--------|-------|-------|
| Key type | Symmetric (shared secret) | Asymmetric (private/public) |
| Signing | Same key | Private key |
| Verification | Same key | Public key |
| Speed | Faster | Slower |
| Key sharing | Must keep secret | Public key can be shared |
| Use case | Single service | Microservices |

```python
# HS256
token = jwt.encode(payload, "shared-secret", algorithm="HS256")
decoded = jwt.decode(token, "shared-secret", algorithms=["HS256"])

# RS256
token = jwt.encode(payload, private_key, algorithm="RS256")
decoded = jwt.decode(token, public_key, algorithms=["RS256"])
```

**When to use RS256:** When multiple services need to verify tokens but shouldn't be able to create them.

---

### Q3: Why are access tokens short-lived?

**Answer:** Short-lived tokens (15-60 minutes) limit exposure if a token is compromised:

- If stolen, attacker has limited time window
- Forces use of refresh tokens (stored more securely)
- Balances security with user experience
- Enables automatic session expiry

```python
# Access token: 15 minutes
access_token = create_access_token(
    data={"sub": user.id},
    expires_delta=timedelta(minutes=15)
)

# Refresh token: 7 days
refresh_token = create_refresh_token(
    data={"sub": user.id},
    expires_delta=timedelta(days=7)
)
```

---

### Q4: How do you handle JWT revocation?

**Answer:** JWTs are stateless — can't be revoked directly. Options:

**1. Blocklist in Redis:**
```python
async def revoke_token(token: str, r: redis.Redis):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    ttl = payload["exp"] - datetime.utcnow().timestamp()
    await r.setex(f"revoked:{token}", int(ttl), "1")

async def is_revoked(token: str, r: redis.Redis) -> bool:
    return await r.exists(f"revoked:{token}") > 0
```

**2. Token version per user:**
```python
# Store token_version in user record
# Increment to invalidate all tokens
# Include version in token payload
```

**3. Short expiration (simplest):**
```python
# Just let tokens expire naturally
# Use refresh tokens for renewal
```

---

### Q5: What should you never store in a JWT payload?

**Answer:** Sensitive data — JWT payloads are Base64-encoded, NOT encrypted:

```python
# BAD
payload = {
    "sub": "user123",
    "password": "secret123",      # NEVER
    "credit_card": "4111...",     # NEVER
    "ssn": "123-45-6789",         # NEVER
}

# GOOD
payload = {
    "sub": "user123",
    "role": "admin",
    "exp": datetime.utcnow() + timedelta(minutes=15),
}
```

Anyone can decode a JWT payload. Only store non-sensitive claims.

---

### Q6: What is the `jti` claim used for?

**Answer:** JWT ID — unique identifier for each token. Essential for revocation:

```python
import uuid

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["jti"] = str(uuid.uuid4())  # Unique ID
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=15)
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

# On logout, add jti to blocklist
async def logout(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    jti = payload["jti"]
    ttl = payload["exp"] - datetime.utcnow().timestamp()
    await redis.setex(f"revoked:{jti}", int(ttl), "1")

# On verification, check blocklist
async def verify_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    if await redis.exists(f"revoked:{payload['jti']}"):
        raise HTTPException(401, "Token revoked")
    return payload
```

---

### Q7: How do you implement token refresh flow?

**Answer:**

```python
@app.post("/token")
async def login(credentials: LoginRequest):
    user = authenticate_user(credentials.email, credentials.password)
    return {
        "access_token": create_access_token({"sub": user.id}, timedelta(minutes=15)),
        "refresh_token": create_refresh_token({"sub": user.id}, timedelta(days=7)),
    }

@app.post("/refresh")
async def refresh(refresh_token: str):
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])

    if payload.get("type") != "refresh":
        raise HTTPException(400, "Invalid token type")

    # Issue new pair
    user_id = payload["sub"]
    return {
        "access_token": create_access_token({"sub": user_id}, timedelta(minutes=15)),
        "refresh_token": create_refresh_token({"sub": user_id}, timedelta(days=7)),
    }
```

---

### Q8: What is algorithm confusion in JWT?

**Answer:** Attack where the attacker changes the `alg` header:

```python
# Attack: Change RS256 to HS256
# Attacker signs with public key as HMAC secret
# Server verifies with public key (as HMAC) — succeeds!

# Prevention
def verify_token(token: str):
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=["HS256"],  # ALWAYS specify allowed algorithms
        options={"verify_signature": True},
    )
```

**Never trust the header's `alg` field.** Always specify allowed algorithms explicitly.

---

## OAuth2

### Q9: What is the difference between OAuth2 and OpenID Connect?

**Answer:**

| Aspect | OAuth2 | OpenID Connect |
|--------|--------|---------------|
| Purpose | Authorization | Authentication + Authorization |
| Token | Access token | ID token + Access token |
| User info | Not standardized | Standard claims (email, name) |
| Protocol | Built on | Built on OAuth2 |

```python
# OAuth2: "Can this app access your GitHub repos?"
# OIDC: "Who are you? (and can this app access your profile?)"

# OIDC adds:
# - ID token (JWT with user identity)
# - UserInfo endpoint
# - Standard scopes (openid, email, profile)
```

---

### Q10: When should you use Client Credentials flow?

**Answer:** Machine-to-machine (M2M) — no user involved:

```python
@app.post("/token")
async def get_token():
    # Service authenticates with its own credentials
    data = {
        "grant_type": "client_credentials",
        "client_id": "service-a",
        "client_secret": "secret",
    }
    response = await httpx.post("https://auth.example.com/token", data=data)
    return response.json()

# Use cases:
# - Backend service calling another backend service
# - Cron jobs accessing APIs
# - Microservice-to-microservice communication
```

---

### Q11: What is PKCE and why is it required?

**Answer:** Proof Key for Code Exchange prevents authorization code interception:

```python
import hashlib, base64, secrets

# 1. Generate code_verifier
code_verifier = secrets.token_urlsafe(32)

# 2. Create code_challenge
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b"=").decode()

# 3. Send code_challenge with authorization request
redirect_url = f"https://provider.com/authorize?code_challenge={code_challenge}"

# 4. Store code_verifier in session

# 5. On callback, send code_verifier to exchange code for token
token = await exchange_code(code, code_verifier)
```

**Required for:** SPAs, mobile apps, desktop apps — any public client.

---

### Q12: Why was the OAuth2 Password Grant deprecated?

**Answer:** Security issues:

1. User sends credentials directly to client app (not authorization server)
2. Client app handles plaintext password
3. No support for MFA
4. No support for consent screen
5. OAuth 2.1 removes it entirely

**Replacement:** Authorization Code + PKCE for all client types.

---

### Q13: How do scopes work in OAuth2?

**Answer:** Scopes define access level:

```python
# Client requests scopes
redirect_url = "https://provider.com/authorize?scope=read+write+admin"

# User approves scopes
# Token contains granted scopes
token = {
    "access_token": "...",
    "scope": "read write",  # admin denied
}

# API validates scopes
@app.get("/admin/")
async def admin_route(token: str = Security(oauth2_scheme, scopes=["admin"])):
    # Raises 403 if scope not in token
    ...
```

---

### Q14: What is the difference between OAuth2 and API keys?

**Answer:**

| Aspect | OAuth2 | API Keys |
|--------|--------|----------|
| Identifies | User | Application |
| Lifetime | Short-lived | Long-lived |
| Revocation | Easy | Harder |
| Permissions | Fine-grained (scopes) | Binary (has/doesn't have) |
| Flow | Authorization code | Direct |
| Use case | User authorization | App identification |

---

## API Keys

### Q15: When should you use API keys vs JWT?

**Answer:**

**API Keys for:**
- Machine-to-machine communication
- Third-party API access (Stripe, GitHub)
- Rate limiting per client
- Usage tracking and billing

**JWT for:**
- User authentication
- Session management
- Microservices auth
- Cross-domain scenarios

```python
# API Key: identifies the calling app
# "This request comes from Stripe integration"

# JWT: identifies the user
# "This request comes from user Alice"
```

---

### Q16: How should API keys be stored?

**Answer:**

```python
# NEVER
API_KEY = "sk_live_abc123"  # In source code!
os.environ["API_KEY"]  # In .env committed to git!

# GOOD
# Server: environment variable
import os
API_KEY = os.getenv("API_KEY")

# Database: store only hash
import hashlib
key_hash = hashlib.sha256(api_key.encode()).hexdigest()
# Store key_hash, not api_key

# Client: secure storage
# iOS: Keychain
# Android: Keystore
# Web: httpOnly cookie or backend proxy
```

---

### Q17: What is API key rotation?

**Answer:**

```python
def rotate_api_key(old_key: str):
    # 1. Create new key
    new_key = f"sk_{secrets.token_urlsafe(32)}"
    new_hash = hashlib.sha256(new_key.encode()).hexdigest()

    # 2. Store new hash
    db.query(APIKey).filter(APIKey.key_hash == old_hash).update({
        "key_hash": new_hash,
        "rotated_at": datetime.now(),
        "is_active": True,
    })

    # 3. Deprecate old key (with grace period)
    db.query(APIKey).filter(APIKey.key_hash == old_hash).update({
        "is_active": False,
    })

    # 4. Return new key (shown once)
    return new_key
```

**Grace period:** Keep old key active for 24 hours after rotation.

---

### Q18: Why hash API keys?

**Answer:** Database compromise protection:

```python
# If database leaks with plain keys:
# attacker can use all keys immediately

# If database leaks with hashed keys:
# attacker can't use keys (can't reverse hash)
# would need to brute-force each key

import hashlib, secrets

def create_api_key():
    plain_key = f"sk_{secrets.token_urlsafe(32)}"
    key_hash = hashlib.sha256(plain_key.encode()).hexdigest()
    return plain_key, key_hash  # Store hash, return plain key once
```

---

## Sessions

### Q19: What is the difference between session and JWT authentication?

**Answer:**

| Aspect | Sessions | JWT |
|--------|----------|-----|
| Storage | Server-side | Client-side |
| Lookup | DB/Redis per request | No lookup needed |
| Revocation | Delete session | Blocklist |
| Scalability | Shared store required | Stateless |
| Cross-domain | Cookie limitations | Works anywhere |
| Mobile | Cookie challenges | Natural fit |

```python
# Session: server stores data, client has ID
request.session["user_id"] = 1  # Stored in Redis/DB

# JWT: client stores data, server verifies
token = jwt.encode({"sub": 1}, secret)  # Data in token
```

---

### Q20: How do you prevent session fixation?

**Answer:** Regenerate session ID on login:

```python
@app.post("/login")
async def login(request: Request, credentials: LoginRequest):
    user = authenticate_user(credentials.email, credentials.password)

    # Delete old session
    old_session_id = request.cookies.get("session_id")
    if old_session_id:
        await session_store.delete(old_session_id)

    # Create new session
    session_id = await session_store.create({
        "user_id": user.id,
        "role": user.role,
    })

    response = Response()
    response.set_cookie(
        "session_id",
        session_id,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return response
```

---

### Q21: Why use Redis for session storage?

**Answer:**

- **Speed:** In-memory, sub-millisecond reads
- **Persistence:** Configurable (RDB/AOF)
- **TTL:** Automatic session expiration
- **Scalability:** Cluster mode for horizontal scaling
- **Atomic operations:** INCR, EXPIRE for rate limiting

```python
import redis.asyncio as redis

r = redis.Redis.from_url("redis://localhost:6379")

# Create session
await r.setex(f"session:{session_id}", 3600, json.dumps(data))

# Get session
data = await r.get(f"session:{session_id}")

# Delete session (logout)
await r.delete(f"session:{session_id}")
```

---

### Q22: What is SameSite cookie attribute?

**Answer:** Controls cross-site cookie behavior:

```python
# Lax (recommended default)
# Cookies sent for top-level navigation and GET requests
response.set_cookie("session_id", value, samesite="lax")

# Strict
# Cookies only sent for same-site requests
response.set_cookie("session_id", value, samesite="strict")

# None
# Cookies sent for all requests (requires Secure=True)
response.set_cookie("session_id", value, samesite="none", secure=True)
```

**CSRF protection:** `Lax` prevents most CSRF attacks. Use `Strict` for banking/high-security.

---

## RBAC

### Q23: What is RBAC?

**Answer:** Role-Based Access Control:

```
User → Role → Permissions → Access

Alice → Admin → [users:read, users:write, users:delete]
Bob → Editor → [articles:read, articles:write]
Charlie → Viewer → [articles:read]
```

```python
class UserRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

def require_role(*roles: str):
    async def checker(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(403, f"Required role: {roles}")
        return user
    return checker

@app.delete("/users/{id}")
async def delete_user(user=Depends(require_role("admin"))):
    ...
```

---

### Q24: What is the difference between RBAC and ABAC?

**Answer:**

| Aspect | RBAC | ABAC |
|--------|------|------|
| Decision based on | Role | Attributes |
| Simplicity | Simple | Complex |
| Flexibility | Limited | Very flexible |
| Example | "Is admin?" | "Is owner AND time > 9am?" |

```python
# RBAC
if user.role == "admin":
    allow()

# ABAC
if (user.department == resource.department and
    user.clearance >= resource.classification and
    time.hour >= 9 and time.hour <= 17):
    allow()
```

---

### Q25: How do you implement RBAC in FastAPI?

**Answer:**

```python
# Permission definitions
PERMISSIONS = {
    "admin": ["users:*", "items:*", "orders:*"],
    "editor": ["items:read", "items:write", "orders:read"],
    "viewer": ["items:read", "orders:read"],
}

# Dependency
def require_permission(*required: str):
    async def checker(user: User = Depends(get_current_user)):
        user_perms = PERMISSIONS.get(user.role, [])
        if not any(p in user_perms for p in required):
            raise HTTPException(403, "Permission denied")
        return user
    return checker

# Usage
@app.get("/items/")
async def list_items(user=Depends(require_permission("items:read"))):
    ...
```

---

### Q26: What is row-level security?

**Answer:** Users access only their own data:

```python
@app.get("/orders/")
async def list_my_orders(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Only return user's orders
    return db.query(Order).filter(Order.user_id == user.id).all()

@app.get("/orders/{order_id}")
async def get_order(
    order_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = db.query(Order).get(order_id)
    if order.user_id != user.id and user.role != "admin":
        raise HTTPException(403, "Access denied")
    return order
```

---

### Q27: How do you handle role hierarchies?

**Answer:**

```python
ROLE_LEVELS = {
    "superadmin": 4,
    "admin": 3,
    "moderator": 2,
    "user": 1,
    "viewer": 0,
}

def require_role_level(min_level: str):
    async def checker(user: User = Depends(get_current_user)):
        user_level = ROLE_LEVELS.get(user.role, 0)
        required_level = ROLE_LEVELS.get(min_level, 0)
        if user_level < required_level:
            raise HTTPException(403, "Insufficient role level")
        return user
    return checker

# Usage
@app.get("/admin/")
async def admin_route(user=Depends(require_role_level("admin"))):
    # admin and superadmin can access
    ...
```

---

## Security

### Q28: How do you hash passwords in FastAPI?

**Answer:**

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# Registration
@app.post("/register/")
async def register(data: UserCreate):
    hashed = hash_password(data.password)
    user = User(email=data.email, hashed_password=hashed)
    db.add(user)
    db.commit()

# Login
@app.post("/login/")
async def login(data: LoginRequest):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
```

---

### Q29: What is the purpose of CORS configuration?

**Answer:** Controls which domains can access your API:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com"],  # Specific origins only
    allow_credentials=True,               # Allow cookies
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
```

**Never use `allow_origins=["*"]` with `allow_credentials=True`** — it's a security vulnerability.

---

### Q30: How do you prevent brute-force attacks?

**Answer:**

```python
import redis.asyncio as redis

async def check_brute_force(
    identifier: str,
    r: redis.Redis,
    max_attempts: int = 5,
    window: int = 900,
) -> bool:
    """Returns True if should block."""
    key = f"login_attempts:{identifier}"
    attempts = await r.incr(key)
    if attempts == 1:
        await r.expire(key, window)
    return attempts > max_attempts

@app.post("/login/")
async def login(
    credentials: LoginRequest,
    r: redis.Redis = Depends(get_redis),
):
    identifier = f"{credentials.email}:{request.client.host}"

    if await check_brute_force(identifier, r):
        raise HTTPException(429, "Too many attempts")

    user = authenticate_user(credentials.email, credentials.password)
    if not user:
        await r.incr(f"login_attempts:{identifier}")
        raise HTTPException(401, "Invalid credentials")

    await r.delete(f"login_attempts:{identifier}")
    # Return token...
```

---

### Q31: What security headers should you always include?

**Answer:**

```python
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response
```

---

### Q32: What is audit logging and why is it important?

**Answer:** Recording security events:

```python
class AuditLog(Base):
    user_id: int
    action: str          # "login", "logout", "create", "delete"
    resource: str        # "user", "order", "item"
    resource_id: str
    ip_address: str
    success: bool
    timestamp: datetime

@app.post("/login/")
async def login(...):
    user = authenticate_user(...)
    audit_log.log(
        user_id=user.id if user else None,
        action="login",
        resource="auth",
        ip_address=request.client.host,
        success=user is not None,
    )
```

**Why important:** Breach detection, compliance (GDPR, SOC2), debugging, forensics.

---

### Q33: How do you handle file upload security?

**Answer:**

```python
import magic

ALLOWED_TYPES = {"image/jpeg", "image/png", "application/pdf"}
MAX_SIZE = 5 * 1024 * 1024  # 5MB

@app.post("/upload/")
async def upload(file: UploadFile):
    content = await file.read()

    # Size check
    if len(content) > MAX_SIZE:
        raise HTTPException(400, "File too large")

    # MIME check
    mime = magic.from_buffer(content, mime=True)
    if mime not in ALLOWED_TYPES:
        raise HTTPException(400, "Invalid file type")

    # Extension check
    ext = Path(file.filename).suffix.lower()
    expected_ext = {".jpg": "image/jpeg", ".png": "image/png", ".pdf": "application/pdf"}
    if expected_ext.get(ext) != mime:
        raise HTTPException(400, "Extension mismatch")

    # Store with random filename
    random_name = f"{uuid.uuid4()}{ext}"
    # Save to non-webroot location
```

---

### Q34: What is the principle of least privilege?

**Answer:** Give only minimum permissions needed:

```python
# BAD
@app.get("/users/")
async def list_users(user=Depends(require_role("admin"))):
    # Admin can view users, but do they need to?

# GOOD
@app.get("/users/")
async def list_users(user=Depends(require_role("viewer"))):
    # Minimal role that can access

# BETTER: Granular permissions
@app.get("/users/")
async def list_users(
    user=Depends(require_permission("users:read"))
):
    # Explicit permission check
```

---

## Quick Reference

| Topic | Key Concept | Recommendation |
|-------|-------------|----------------|
| Passwords | Hash with bcrypt/argon2 | Never MD5/SHA |
| Tokens | Short-lived JWT + refresh | 15min access, 7d refresh |
| API Keys | Hash before storage | Rotate regularly |
| Sessions | Redis-backed | Regenerate on login |
| RBAC | Roles + Permissions | Follow least privilege |
| CORS | Specific origins only | Never `*` with credentials |
| Headers | Security headers always | HSTS, CSP, X-Frame-Options |
| Audit | Log all security events | Who, what, when, outcome |

---

## Scenario Questions

### Scenario 1: Design Auth for a SaaS App
**Answer:** JWT for API auth, OAuth2 for Google/GitHub login, RBAC for tenant-level permissions, Redis for rate limiting, audit logging for compliance.

### Scenario 2: Multi-Tenant Authentication
**Answer:** JWT with tenant claim, role hierarchy per tenant, row-level security for data isolation, separate admin panels, tenant-scoped sessions.

### Scenario 3: Mobile App Authentication
**Answer:** OAuth2 + PKCE for social login, short-lived JWTs, refresh token rotation, secure storage (Keychain/Keystore), certificate pinning.

### Scenario 4: Microservices Auth
**Answer:** JWT with RS256, API gateway validates tokens, service-to-service with client credentials, distributed session store, centralized authorization service.

---

## Summary

Authentication mastery requires understanding JWT internals, OAuth2 flows, secure password handling, RBAC implementation, and security best practices. Always prioritize: least privilege, secure storage, proper hashing, comprehensive audit logging, and defense in depth.
