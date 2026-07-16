# API Key Authentication with FastAPI

## Table of Contents

1. [API Key Authentication](#api-key-authentication)
2. [APIKeyHeader, APIKeyQuery, APIKeyCookie](#apikeyheader-apikeyquery-apikeycookie)
3. [API Key Rotation](#api-key-rotation)
4. [Hashed API Keys](#hashed-api-keys)
5. [API Key Management](#api-key-management)
6. [Best Practices](#best-practices)
7. [Interview Questions](#interview-questions)

---

## API Key Authentication

API keys are long-lived tokens used to identify and authenticate applications (not users). They're simpler than OAuth2 but less secure for user-facing applications.

### When to Use API Keys

- **Machine-to-machine** communication
- **Third-party API** access
- **Rate limiting** per client
- **Usage tracking** and billing
- **Internal services** authentication

### When NOT to Use API Keys

- User authentication (use OAuth2/JWT)
- Public-facing applications
- When you need fine-grained permissions
- When you need token revocation

### How API Keys Work

```
1. Developer signs up for API access
2. Server generates API key
3. Developer includes key in requests
4. Server validates key and processes request
```

---

## APIKeyHeader, APIKeyQuery, APIKeyCookie

### Installation

```bash
# Built into FastAPI — no extra installation needed
```

### APIKeyHeader

```python
from fastapi import FastAPI, Security, HTTPException
from fastapi.security import APIKeyHeader

app = FastAPI()

API_KEY = "your-secret-api-key"
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key",
        )
    return api_key

@app.get("/protected/")
async def protected_route(api_key: str = Depends(verify_api_key)):
    return {"message": "Access granted"}
```

### APIKeyQuery

```python
from fastapi.security import APIKeyQuery

api_key_query = APIKeyQuery(name="api_key", auto_error=True)

@app.get("/public-data/")
async def public_data(api_key: str = Security(api_key_query)):
    # ?api_key=your-key
    return {"data": "value"}
```

### APIKeyCookie

```python
from fastapi.security import APIKeyCookie

api_key_cookie = APIKeyCookie(name="api_key", auto_error=True)

@app.get("/dashboard/")
async def dashboard(api_key: str = Security(api_key_cookie)):
    # Cookie: api_key=your-key
    return {"dashboard": "data"}
```

### Multiple Sources

```python
from fastapi.security import APIKeyHeader, APIKeyQuery, APIKeyCookie

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
api_key_query = APIKeyQuery(name="api_key", auto_error=False)
api_key_cookie = APIKeyCookie(name="api_key", auto_error=False)

async def verify_api_key(
    header_key: str | None = Security(api_key_header),
    query_key: str | None = Security(api_key_query),
    cookie_key: str | None = Security(api_key_cookie),
):
    api_key = header_key or query_key or cookie_key

    if not api_key:
        raise HTTPException(
            status_code=403,
            detail="No API key provided",
        )

    if api_key != VALID_API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key",
        )

    return api_key
```

---

## API Key Rotation

### Rotation Strategy

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class APIKey(BaseModel):
    key: str
    name: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    is_active: bool = True
    rotated_at: Optional[datetime] = None

class APIKeyManager:
    def __init__(self, db: Session):
        self.db = db

    def create_key(self, name: str, expires_in_days: int = 90) -> APIKey:
        key = f"sk_{secrets.token_urlsafe(32)}"
        api_key = APIKey(
            key=key,
            name=name,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=expires_in_days),
        )
        self.db.add(api_key)
        self.db.commit()
        return api_key

    def rotate_key(self, old_key: str) -> APIKey:
        """Create new key, mark old as rotated, keep active for grace period."""
        old = self.db.query(APIKey).filter(APIKey.key == old_key).first()
        if not old:
            raise ValueError("Key not found")

        # Create new key
        new_key = self.create_key(old.name)

        # Mark old key as rotated
        old.rotated_at = datetime.now()
        old.is_active = False  # Or keep active for grace period
        self.db.commit()

        return new_key

    def revoke_key(self, key: str):
        api_key = self.db.query(APIKey).filter(APIKey.key == key).first()
        if api_key:
            api_key.is_active = False
            self.db.commit()

# Rotation endpoint
@app.post("/api-keys/rotate")
async def rotate_api_key(
    current_key: str = Security(api_key_header),
    manager: APIKeyManager = Depends(get_api_key_manager),
):
    new_key = manager.rotate_key(current_key)
    return {
        "new_key": new_key.key,
        "message": "Rotate your API key. Old key will be deprecated in 24 hours.",
    }
```

### Grace Period During Rotation

```python
def verify_api_key(key: str, db: Session) -> APIKey:
    api_key = db.query(APIKey).filter(APIKey.key == key).first()

    if not api_key:
        raise HTTPException(403, "Invalid API key")

    if api_key.is_active:
        return api_key

    # Check grace period after rotation
    if api_key.rotated_at:
        grace_period = timedelta(hours=24)
        if datetime.now() - api_key.rotated_at < grace_period:
            # Still valid during grace period
            return api_key

    raise HTTPException(403, "API key is revoked")
```

---

## Hashed API Keys

### Why Hash?

Store hashed API keys in the database. If the database is compromised, attackers can't use the keys.

```python
import hashlib
import secrets

def generate_api_key() -> tuple[str, str]:
    """Generate API key and its hash."""
    key = f"sk_{secrets.token_urlsafe(32)}"
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    return key, key_hash

def verify_api_key(plain_key: str, stored_hash: str) -> bool:
    """Verify API key against stored hash."""
    key_hash = hashlib.sha256(plain_key.encode()).hexdigest()
    return secrets.compare_digest(key_hash, stored_hash)

# Database stores only the hash
class APIKeyRecord(BaseModel):
    id: int
    name: str
    key_hash: str  # Never store plain key
    created_at: datetime
    expires_at: Optional[datetime] = None

# On creation, return plain key once
@app.post("/api-keys/")
async def create_api_key(name: str, db: Session = Depends(get_db)):
    plain_key, key_hash = generate_api_key()

    record = APIKeyRecord(
        name=name,
        key_hash=key_hash,
        created_at=datetime.now(),
    )
    db.add(record)
    db.commit()

    # Return plain key — shown only once
    return {
        "key": plain_key,
        "message": "Save this key — it won't be shown again",
        "name": name,
    }
```

### Constant-Time Comparison

```python
import hmac

def verify_api_key_constant_time(provided: str, stored: str) -> bool:
    """Constant-time comparison to prevent timing attacks."""
    return hmac.compare_digest(provided.encode(), stored.encode())
```

---

## API Key Management

### Full CRUD

```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class APIKeyCreate(BaseModel):
    name: str
    scopes: list[str] = ["read"]
    expires_in_days: Optional[int] = 90

class APIKeyResponse(BaseModel):
    id: int
    name: str
    scopes: list[str]
    created_at: datetime
    expires_at: Optional[datetime]
    last_used: Optional[datetime]

class APIKeyCreateResponse(APIKeyResponse):
    key: str  # Only returned on creation

@app.post("/api-keys/", response_model=APIKeyCreateResponse)
async def create_api_key(
    data: APIKeyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plain_key, key_hash = generate_api_key()

    record = APIKeyDB(
        user_id=current_user.id,
        name=data.name,
        key_hash=key_hash,
        scopes=data.scopes,
        created_at=datetime.now(),
        expires_at=datetime.now() + timedelta(days=data.expires_in_days)
            if data.expires_in_days else None,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return APIKeyCreateResponse(
        id=record.id,
        key=plain_key,
        name=record.name,
        scopes=record.scopes,
        created_at=record.created_at,
        expires_at=record.expires_at,
    )

@app.get("/api-keys/", response_model=list[APIKeyResponse])
async def list_api_keys(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    keys = db.query(APIKeyDB).filter(
        APIKeyDB.user_id == current_user.id
    ).all()
    return keys

@app.delete("/api-keys/{key_id}")
async def delete_api_key(
    key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    key = db.query(APIKeyDB).filter(
        APIKeyDB.id == key_id,
        APIKeyDB.user_id == current_user.id,
    ).first()
    if not key:
        raise HTTPException(404, "API key not found")

    db.delete(key)
    db.commit()
    return {"message": "API key deleted"}
```

### Usage Tracking

```python
class APIKeyDB(BaseModel):
    # ... existing fields ...
    last_used: Optional[datetime] = None
    usage_count: int = 0

async def track_api_usage(api_key: APIKeyDB, db: Session):
    api_key.last_used = datetime.now()
    api_key.usage_count += 1
    db.commit()

async def verify_and_track(
    api_key: str = Security(api_key_header),
    db: Session = Depends(get_db),
):
    key_record = verify_api_key_from_db(api_key, db)
    await track_api_usage(key_record, db)
    return key_record
```

---

## Best Practices

### 1. Prefix API Keys

```python
# Use prefixes to identify key type
key = f"sk_live_{secrets.token_urlsafe(32)}"  # Production
key = f"sk_test_{secrets.token_urlsafe(32)}"  # Testing
```

### 2. Never Log Full API Keys

```python
import logging

logger = logging.getLogger(__name__)

def log_api_key_usage(api_key: str):
    # Mask the key
    masked = api_key[:8] + "..." + api_key[-4:]
    logger.info(f"API key used: {masked}")
```

### 3. Set Expiration

```python
# Always set expiration
expires_at = datetime.now() + timedelta(days=90)

# Check expiration
if datetime.now() > api_key.expires_at:
    raise HTTPException(403, "API key expired")
```

### 4. Rate Limit per API Key

```python
async def rate_limit_per_key(
    api_key: str = Security(api_key_header),
    r: redis.Redis = Depends(get_redis),
):
    key = f"rate_limit:{api_key}"
    count = await r.incr(key)
    if count == 1:
        await r.expire(key, 60)  # 1 minute window

    if count > 100:  # 100 requests per minute
        raise HTTPException(429, "Rate limit exceeded")
```

### 5. Use HTTPS Only

```python
# API keys should only be sent over HTTPS
# Configure your server to reject HTTP requests
```

---

## Interview Questions

### Q1: When should you use API keys vs JWT?
**Answer:** API keys: machine-to-machine, third-party API access, rate limiting. JWT: user authentication, session management, fine-grained permissions. API keys identify applications; JWTs identify users.

### Q2: How should API keys be stored?
**Answer:** Never in source code. Use environment variables or secrets managers. Hash before storing in database. Use httpsOnly cookies or secure storage on the client side.

### Q3: Why hash API keys?
**Answer:** If the database is compromised, hashed keys can't be used directly. Attackers would need to brute-force the hash, which is computationally expensive with proper algorithms.

### Q4: What is API key rotation?
**Answer:** Periodically replacing API keys. Create new key, deprecate old key with a grace period, then revoke. This limits exposure if a key is compromised.

### Q5: How do you prevent timing attacks on API key verification?
**Answer:** Use constant-time comparison (hmac.compare_digest). This prevents attackers from inferring the correct key by measuring response times.

### Q6: What are the risks of API key authentication?
**Answer:** Keys can be leaked in logs, source code, or client-side. They don't identify users. No built-in expiration. No fine-grained permissions. Use additional security measures.

### Q7: How do you implement API key scoping?
**Answer:** Store allowed scopes with the API key. Validate scopes during request processing. Use the same scope system as OAuth2 for consistency.

### Q8: What is the difference between live and test API keys?
**Answer:** Live keys access real data and services. Test keys access sandbox environments. Always use test keys during development to prevent accidental data modification.

---

## Summary

API key authentication is simple and effective for machine-to-machine communication. Always hash keys before storage, implement rotation with grace periods, rate limit per key, and use HTTPS. For user authentication, prefer OAuth2/JWT.
