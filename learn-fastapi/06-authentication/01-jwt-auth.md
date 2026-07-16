# JWT Authentication with FastAPI

## Table of Contents

1. [What is JWT](#what-is-jwt)
2. [JWT Structure](#jwt-structure)
3. [Access Tokens vs Refresh Tokens](#access-tokens-vs-refresh-tokens)
4. [JWT with FastAPI](#jwt-with-fastapi)
5. [python-jose](#python-jose)
6. [passlib for Password Hashing](#passlib-for-password-hashing)
7. [Token Expiration](#token-expiration)
8. [Token Revocation](#token-revocation)
9. [JWT Best Practices](#jwt-best-practices)
10. [RS256 vs HS256](#rs256-vs-hs256)
11. [Best Practices](#best-practices-1)
12. [Interview Questions](#interview-questions)

---

## What is JWT

JSON Web Token (JWT) is an open standard (RFC 7519) for securely transmitting information between parties as a JSON object. JWTs are commonly used for authentication and authorization.

### Why JWT?

- **Stateless**: Server doesn't store session data
- **Scalable**: Any server with the secret can verify the token
- **Self-contained**: Token contains all needed user information
- **Cross-domain**: Works across different domains and services

---

## JWT Structure

A JWT consists of three parts separated by dots: `header.payload.signature`

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

### Header

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

- `alg`: Algorithm used (HS256, RS256, ES256)
- `typ`: Token type (JWT)

### Payload

```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "admin",
  "iat": 1516239022,
  "exp": 1516242622,
  "jti": "unique-token-id"
}
```

**Standard Claims:**
- `sub`: Subject (user ID)
- `iss`: Issuer
- `aud`: Audience
- `exp`: Expiration time
- `nbf`: Not before
- `iat`: Issued at
- `jti`: JWT ID (unique identifier)

### Signature

```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

The signature ensures the token hasn't been tampered with.

---

## Access Tokens vs Refresh Tokens

### Access Token

- Short-lived (15-60 minutes)
- Used to access protected resources
- Contains user identity and permissions
- Sent with every API request

### Refresh Token

- Long-lived (7-30 days)
- Used to obtain new access tokens
- Stored securely (httpOnly cookie or secure storage)
- Sent only when access token expires

### Flow

```
1. User logs in with credentials
2. Server returns access token (short) + refresh token (long)
3. Client sends access token with API requests
4. When access token expires:
   a. Client sends refresh token to /refresh endpoint
   b. Server validates refresh token
   c. Server returns new access token + refresh token
5. When refresh token expires:
   a. User must re-authenticate
```

---

## JWT with FastAPI

### Complete Implementation

```python
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# Configuration
SECRET_KEY = "your-secret-key-keep-it-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# Models
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None

class User(BaseModel):
    id: int
    username: str
    email: str
    disabled: Optional[bool] = False

class UserInDB(User):
    hashed_password: str

# Mock database
fake_users_db = {
    "johndoe": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "hashed_password": pwd_context.hash("secret"),
        "disabled": False,
    }
}

# Password utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# User lookup
def get_user(db: dict, username: str) -> Optional[UserInDB]:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

# Token creation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Token verification
def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return TokenData(username=username, user_id=user_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

# Authentication dependency
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    token_data = verify_token(token)
    user = get_user(fake_users_db, token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Disabled user",
        )
    return user

# Routes
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(fake_users_db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username, "user_id": user.id}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@app.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=400, detail="Invalid token type")

        username = payload.get("sub")
        user = get_user(fake_users_db, username)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        new_access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        new_refresh_token = create_refresh_token(
            data={"sub": user.username, "user_id": user.id}
        )

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

---

## python-jose

### Installation

```bash
pip install python-jose[cryptography]
```

### Encoding and Decoding

```python
from jose import jwt, JWTError

# Encode
payload = {"sub": "user123", "name": "John"}
token = jwt.encode(payload, "secret", algorithm="HS256")

# Decode
try:
    payload = jwt.decode(token, "secret", algorithms=["HS256"])
except JWTError as e:
    print(f"Invalid token: {e}")
```

### Working with Claims

```python
from datetime import datetime, timedelta

payload = {
    "sub": "user123",
    "name": "John",
    "exp": datetime.utcnow() + timedelta(hours=1),
    "iat": datetime.utcnow(),
    "jti": str(uuid.uuid4()),
}

token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
```

---

## passlib for Password Hashing

### Installation

```bash
pip install passlib[bcrypt]
pip install argon2-cffi  # For argon2
```

### Bcrypt

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
hashed = pwd_context.hash("mypassword")
# $2b$12$LJ3m4ys3Lz2YBpDprxOqOeW3wYbQx1v4t2e3r4y5u6i7o8p9a0s1d

# Verify password
is_valid = pwd_context.verify("mypassword", hashed)  # True
is_valid = pwd_context.verify("wrongpassword", hashed)  # False
```

### Argon2 (More Secure)

```python
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

# argon2 is the default if available
hashed = pwd_context.hash("mypassword")
```

### Password Validation

```python
from pydantic import BaseModel, field_validator

class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain lowercase")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        return v
```

---

## Token Expiration

### Checking Expiration

```python
from datetime import datetime, timezone

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Check expiration
        exp = payload.get("exp")
        if exp:
            exp_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
            if datetime.now(timezone.utc) > exp_datetime:
                raise HTTPException(status_code=401, detail="Token expired")

        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Graceful Expiration

```python
# Allow expired tokens within grace period
def verify_token_with_grace(token: str, grace_seconds: int = 300) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False},  # Don't auto-verify
        )

        exp = payload.get("exp")
        if exp:
            exp_time = datetime.fromtimestamp(exp, tz=timezone.utc)
            now = datetime.now(timezone.utc)

            if now > exp_time + timedelta(seconds=grace_seconds):
                raise HTTPException(status_code=401, detail="Token expired")

        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

---

## Token Revocation

### Blocklist Approach

```python
# Store revoked tokens in Redis
import redis

r = redis.Redis()

def revoke_token(token: str, expires_in: int):
    """Add token to blocklist until it expires."""
    r.setex(f"revoked:{token}", expires_in, "revoked")

def is_token_revoked(token: str) -> bool:
    """Check if token is revoked."""
    return r.exists(f"revoked:{token}") > 0

def verify_token(token: str):
    if is_token_revoked(token):
        raise HTTPException(status_code=401, detail="Token revoked")
    # ... rest of verification
```

### Logout Endpoint

```python
@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    # Decode to get expiration
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    exp = payload.get("exp")
    ttl = exp - datetime.utcnow().timestamp()

    # Add to blocklist
    revoke_token(token, int(ttl))
    return {"message": "Logged out"}
```

### Token Version Approach

```python
class User(BaseModel):
    id: int
    token_version: int = 0

def create_access_token(user: User):
    payload = {
        "sub": user.id,
        "token_version": user.token_version,
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# To invalidate all tokens for a user, increment token_version
async def invalidate_all_tokens(user_id: int, db: Session):
    user = db.query(User).get(user_id)
    user.token_version += 1
    db.commit()

# Verify includes version check
def verify_token(token: str, db: Session):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user = db.query(User).get(payload["sub"])
    if user.token_version != payload["token_version"]:
        raise HTTPException(401, "Token revoked")
    return user
```

---

## JWT Best Practices

### 1. Use Strong Secrets

```python
# Generate a strong secret
import secrets
SECRET_KEY = secrets.token_urlsafe(64)

# Never hardcode secrets
# Use environment variables
import os
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
```

### 2. Set Short Expiration

```python
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 15 minutes
REFRESH_TOKEN_EXPIRE_DAYS = 7     # 7 days
```

### 3. Use HTTPS Only

```python
# Tokens should only be sent over HTTPS
# In production, always use HTTPS
```

### 4. Validate All Claims

```python
def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": True},  # Always verify expiration
        )

        # Validate issuer
        if payload.get("iss") != "your-app":
            raise HTTPException(401, "Invalid issuer")

        # Validate audience
        if payload.get("aud") != "your-api":
            raise HTTPException(401, "Invalid audience")

        return payload
    except JWTError:
        raise HTTPException(401, "Invalid token")
```

### 5. Don't Store Sensitive Data in Payload

```python
# BAD: Sensitive data in token
payload = {
    "sub": "user123",
    "password_hash": "...",  # NEVER
    "credit_card": "...",    # NEVER
}

# GOOD: Only necessary claims
payload = {
    "sub": "user123",
    "role": "admin",
    "exp": datetime.utcnow() + timedelta(minutes=15),
}
```

### 6. Use Token IDs for Revocation

```python
import uuid

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({
        "jti": str(uuid.uuid4()),  # Unique token ID
        "exp": datetime.utcnow() + timedelta(minutes=15),
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

---

## RS256 vs HS256

### HS256 (HMAC with SHA-256)

```python
# Symmetric: same key for signing and verification
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

# Pros: Simple, fast
# Cons: Same key for signing and verification
# Use when: Single service, same server signs and verifies
```

### RS256 (RSA with SHA-256)

```python
from jose import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Generate RSA key pair
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Serialize keys
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

# Sign with private key
token = jwt.encode(payload, private_pem, algorithm="RS256")

# Verify with public key
decoded = jwt.decode(token, public_pem, algorithms=["RS256"])

# Pros: Different keys for signing and verification
# Cons: Slower, more complex
# Use when: Multiple services, need to share verification without signing ability
```

### Comparison

| Aspect | HS256 | RS256 |
|--------|-------|-------|
| Key type | Symmetric | Asymmetric |
| Speed | Faster | Slower |
| Key sharing | Same key | Public key can be shared |
| Use case | Single service | Microservices |
| Security | Key compromise = full control | More secure key distribution |

---

## Best Practices

### 1. Rotate Secrets Regularly

```python
# Support multiple valid secrets during rotation
VALID_SECRETS = [current_secret, previous_secret]

def verify_token(token: str):
    for secret in VALID_SECRETS:
        try:
            return jwt.decode(token, secret, algorithms=[ALGORITHM])
        except JWTError:
            continue
    raise HTTPException(401, "Invalid token")
```

### 2. Use httpOnly Cookies for Refresh Tokens

```python
from fastapi import Response

@app.post("/token")
async def login(response: Response, ...):
    # ...
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,     # Not accessible via JavaScript
        secure=True,       # HTTPS only
        samesite="lax",   # CSRF protection
        max_age=7 * 24 * 60 * 60,  # 7 days
    )
```

### 3. Log Token Operations

```python
import logging

logger = logging.getLogger("auth")

def create_access_token(data: dict):
    logger.info(f"Creating token for user: {data.get('sub')}")
    # ...

def verify_token(token: str):
    try:
        # ...
        logger.info(f"Token verified for user: {payload.get('sub')}")
    except JWTError as e:
        logger.warning(f"Token verification failed: {e}")
        raise
```

---

## Interview Questions

### Q1: What is JWT and how does it work?
**Answer:** JWT is a stateless authentication token with three parts: header (algorithm), payload (claims), and signature (verification). The server signs the token; any server with the secret can verify it. The client sends it with each request.

### Q2: What is the difference between access and refresh tokens?
**Answer:** Access tokens are short-lived (15-60 min) and used for API access. Refresh tokens are long-lived (7-30 days) and used to obtain new access tokens. This limits exposure if an access token is compromised.

### Q3: Why use JWT over session cookies?
**Answer:** JWTs are stateless (no server-side storage), scalable (any server can verify), and work across domains. Sessions require server storage and are tied to a single domain.

### Q4: What are the security risks of JWT?
**Answer:** Token theft (XSS, CSRF), no built-in revocation, payload is readable (not encrypted), and algorithm confusion attacks. Mitigate with short expiration, httpOnly cookies, HTTPS, and proper validation.

### Q5: How do you revoke a JWT?
**Answer:** JWTs can't be revoked directly. Options: blocklist in Redis, token version per user, or short expiration with refresh tokens. The blocklist approach is most common.

### Q6: What is the difference between HS256 and RS256?
**Answer:** HS256 uses a shared secret (symmetric). RS256 uses a private/public key pair (asymmetric). Use HS256 for single services, RS256 for microservices where you want to share verification without signing ability.

### Q7: How should you store JWTs on the client?
**Answer:** Access tokens: in memory or httpOnly cookie. Refresh tokens: always httpOnly cookie with secure flag. Never use localStorage (vulnerable to XSS).

### Q8: What claims should be in a JWT?
**Answer:** `sub` (user ID), `exp` (expiration), `iat` (issued at), `jti` (unique ID), `iss` (issuer), `aud` (audience). Don't include sensitive data like passwords or PII.

### Q9: How do you handle JWT expiration gracefully?
**Answer:** Implement refresh token flow. When access token expires, use refresh token to get a new pair. Use httpOnly cookies for refresh tokens. Allow a grace period for overlapping requests.

### Q10: What is the `sub` claim?
**Answer:** The "subject" claim identifies the principal entity (usually the user ID). It's the primary way to identify who the token belongs to.

### Q11: How do you validate a JWT?
**Answer:** 1) Verify signature with secret/public key. 2) Check expiration (`exp`). 3) Validate issuer (`iss`) and audience (`aud`). 4) Check if token is revoked. 5) Validate token version if using.

### Q12: Can JWTs be encrypted?
**Answer:** Yes, using JWE (JSON Web Encryption). However, most applications only sign JWTs (JWS) and rely on HTTPS for transport encryption. JWE adds complexity.

### Q13: What is the `jti` claim?
**Answer:** JWT ID — a unique identifier for the token. Used for token revocation. Store `jti` in a blocklist when revoking. Check blocklist during verification.

### Q14: How do you implement token rotation?
**Answer:** Issue new refresh token with each access token refresh. Revoke old refresh token. This limits the window if a refresh token is compromised.

### Q15: What is algorithm confusion in JWT?
**Answer:** An attack where the attacker changes the `alg` header to `none` or switches from RS256 to HS256. Prevent by explicitly specifying allowed algorithms during verification.

---

## Summary

JWT authentication in FastAPI provides stateless, scalable authentication. Use short-lived access tokens with refresh token flow. Always validate all claims. Use httpOnly cookies for refresh tokens. Consider RS256 for microservices. Implement token revocation via blocklist or token versions.
