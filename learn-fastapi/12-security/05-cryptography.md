# Cryptography

## Table of Contents

1. [Introduction](#1-introduction)
2. [Password Hashing (bcrypt, Argon2)](#2-password-hashing)
3. [Encryption (Fernet, AES)](#3-encryption)
4. [HMAC Signatures](#4-hmac)
5. [Certificate Management](#5-certificates)
6. [TLS/SSL Configuration](#6-tls)
7. [JWT Security](#7-jwt)
8. [Best Practices](#8-best-practices)

---

## 1. Introduction <a name="1-introduction"></a`

Cryptography is essential for protecting data in transit and at rest. FastAPI
applications need proper cryptographic practices for password storage, data
encryption, API authentication, and secure communication.

### Cryptographic Primitives

| Primitive | Use Case | Python Library |
|-----------|----------|---------------|
| Hashing | Password storage, integrity checks | passlib, hashlib |
| Symmetric Encryption | Encrypting data at rest | cryptography (Fernet, AES) |
| Asymmetric Encryption | Key exchange, digital signatures | cryptography (RSA, ECC) |
| HMAC | Message authentication | hmac, hashlib |
| JWT | Token-based authentication | python-jose, PyJWT |

### Installation

```bash
pip install passlib[bcrypt]  # Password hashing
pip install argon2-cffi       # Argon2 password hashing
pip install cryptography      # General cryptography
pip install python-jose[cryptography]  # JWT with RSA support
```

---

## 2. Password Hashing <a name="2-password-hashing"></a>

### Why Hash Passwords?

- Never store plaintext passwords
- One-way function (can't reverse)
- Salt prevents rainbow table attacks
- Slow hashing prevents brute force

### bcrypt

```python
from passlib.context import CryptContext

# Create hashing context
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # Work factor (default: 12)
)

def hash_password(password: str) -> str:
    """Hash a password for storage."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def needs_rehash(hashed_password: str) -> bool:
    """Check if password hash needs updating."""
    return pwd_context.needs_update(hashed_password)

# Usage
hashed = hash_password("my_secure_password")
print(hashed)  # $2b$12$LJ3m4ys3Pz8Vz5z5z5z5zO...
print(verify_password("my_secure_password", hashed))  # True
print(verify_password("wrong_password", hashed))  # False
```

### Argon2 (Recommended)

```python
from passlib.context import CryptContext

# Argon2 is the most secure password hashing algorithm
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=65536,  # 64 MB
    argon2__time_cost=3,        # 3 iterations
    argon2__parallelism=4,      # 4 threads
    argon2__hash_len=32,        # 32 byte hash
    argon2__salt_len=16,        # 16 byte salt
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Usage
hashed = hash_password("my_secure_password")
# $argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ$...
```

### Using bcrypt Directly

```python
import bcrypt

def hash_password_bcrypt(password: str) -> str:
    """Hash password using bcrypt directly."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password_bcrypt(password: str, hashed: str) -> bool:
    """Verify password using bcrypt directly."""
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed.encode("utf-8"),
    )
```

### FastAPI User Model with Password Hashing

```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=12, max_length=128)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain lowercase")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v):
            raise ValueError("Password must contain special character")
        return v

class User(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str
    created_at: datetime
    is_active: bool = True

class UserInDB(User):
    hashed_password: str

# Database operations
async def create_user(db: Session, user_create: UserCreate) -> User:
    hashed_password = hash_password(user_create.password)
    db_user = UserInDB(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password,
        created_at=datetime.utcnow(),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if needs_rehash(user.hashed_password):
        user.hashed_password = hash_password(password)
        db.commit()
    return user
```

---

## 3. Encryption <a name="3-encryption"></a>

### Fernet (Symmetric Encryption)

```python
from cryptography.fernet import Fernet
import os

# Generate a key (store securely!)
def generate_key() -> bytes:
    return Fernet.generate_key()

# Or derive from password
def derive_key_from_password(password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes

    if salt is None:
        salt = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

class FernetEncryption:
    def __init__(self, key: bytes):
        self.fernet = Fernet(key)

    def encrypt(self, data: str) -> str:
        """Encrypt a string."""
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt a string."""
        return self.fernet.decrypt(encrypted_data.encode()).decode()

    def encrypt_dict(self, data: dict) -> str:
        """Encrypt a dictionary."""
        import json
        return self.encrypt(json.dumps(data))

    def decrypt_dict(self, encrypted_data: str) -> dict:
        """Decrypt to dictionary."""
        import json
        return json.loads(self.decrypt(encrypted_data))

# Usage
key = generate_key()
crypto = FernetEncryption(key)

# Encrypt
encrypted = crypto.encrypt("sensitive data")
print(f"Encrypted: {encrypted}")

# Decrypt
decrypted = crypto.decrypt(encrypted)
print(f"Decrypted: {decrypted}")

# Encrypt dict
user_data = {"ssn": "123-45-6789", "credit_card": "4111111111111111"}
encrypted_dict = crypto.encrypt_dict(user_data)
decrypted_dict = crypto.decrypt_dict(encrypted_dict)
```

### AES Encryption

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

class AESEncryption:
    def __init__(self, key: bytes = None):
        if key is None:
            key = os.urandom(32)  # 256-bit key
        self.key = key

    def encrypt(self, data: bytes) -> tuple[bytes, bytes, bytes]:
        """Encrypt data using AES-GCM. Returns (ciphertext, tag, nonce)."""
        nonce = os.urandom(12)
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.GCM(nonce),
            backend=default_backend(),
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        return ciphertext, encryptor.tag, nonce

    def decrypt(
        self,
        ciphertext: bytes,
        tag: bytes,
        nonce: bytes,
    ) -> bytes:
        """Decrypt AES-GCM encrypted data."""
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.GCM(nonce, tag),
            backend=default_backend(),
        )
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()

# Usage
aes = AESEncryption()
plaintext = b"sensitive data to encrypt"

ciphertext, tag, nonce = aes.encrypt(plaintext)
decrypted = aes.decrypt(ciphertext, tag, nonce)
assert decrypted == plaintext
```

### AES with Padding (CBC Mode)

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

class AESCBCEncryption:
    def __init__(self, key: bytes = None):
        if key is None:
            key = os.urandom(32)
        self.key = key

    def encrypt(self, data: bytes) -> tuple[bytes, bytes]:
        """Encrypt using AES-CBC. Returns (ciphertext, iv)."""
        iv = os.urandom(16)

        # PKCS7 padding
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend(),
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return ciphertext, iv

    def decrypt(self, ciphertext: bytes, iv: bytes) -> bytes:
        """Decrypt AES-CBC encrypted data."""
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend(),
        )
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()

        # Remove padding
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()
```

---

## 4. HMAC Signatures <a name="4-hmac"></a>

### Basic HMAC

```python
import hmac
import hashlib

def create_hmac_signature(data: str, secret: str) -> str:
    """Create HMAC-SHA256 signature."""
    return hmac.new(
        secret.encode(),
        data.encode(),
        hashlib.sha256,
    ).hexdigest()

def verify_hmac_signature(
    data: str,
    signature: str,
    secret: str,
) -> bool:
    """Verify HMAC signature."""
    expected = create_hmac_signature(data, secret)
    return hmac.compare_digest(expected, signature)

# Usage
secret = "my-secret-key"
data = "important data to sign"

signature = create_hmac_signature(data, secret)
print(f"Signature: {signature}")

# Verify
is_valid = verify_hmac_signature(data, signature, secret)
print(f"Valid: {is_valid}")  # True

# Tampered data
is_valid = verify_hmac_signature("tampered data", signature, secret)
print(f"Valid: {is_valid}")  # False
```

### Webhook Signature Verification

```python
import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

WEBHOOK_SECRET = "whsec_your_webhook_secret"

def verify_webhook_signature(
    payload: bytes,
    signature_header: str,
    secret: str,
) -> bool:
    """Verify Stripe-style webhook signature."""
    expected_signature = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()

    # Stripe format: t=timestamp,v1=signature
    parts = dict(item.split("=") for item in signature_header.split(","))
    received_signature = parts.get("v1", "")

    return hmac.compare_digest(expected_signature, received_signature)

@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("stripe-signature", "")

    if not verify_webhook_signature(body, signature, WEBHOOK_SECRET):
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Process webhook
    import json
    event = json.loads(body)
    return {"received": True}
```

### HMAC for API Authentication

```python
import hmac
import hashlib
import time

def create_api_signature(
    method: str,
    path: str,
    body: str,
    timestamp: str,
    secret: str,
) -> str:
    """Create API request signature."""
    message = f"{method}\n{path}\n{timestamp}\n{body}"
    return hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256,
    ).hexdigest()

def verify_api_signature(
    method: str,
    path: str,
    body: str,
    timestamp: str,
    signature: str,
    secret: str,
    max_age: int = 300,
) -> bool:
    """Verify API request signature with timestamp."""
    # Check timestamp freshness
    request_time = int(timestamp)
    current_time = int(time.time())
    if abs(current_time - request_time) > max_age:
        return False  # Request too old

    expected = create_api_signature(method, path, body, timestamp, secret)
    return hmac.compare_digest(expected, signature)
```

---

## 5. Certificate Management <a name="5-certificates"></a>

### Self-Signed Certificates (Development)

```python
# Generate self-signed certificate
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime

def generate_self_signed_cert():
    # Generate private key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Create certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "MyApp"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )

    # Save certificate
    with open("cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    # Save private key
    with open("key.pem", "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    return cert, key
```

### Certificate Validation

```python
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def load_and_validate_cert(cert_path: str) -> dict:
    """Load and validate a certificate."""
    with open(cert_path, "rb") as f:
        cert_data = f.read()

    cert = x509.load_pem_x509_certificate(cert_data, default_backend())

    return {
        "subject": cert.subject.rfc4514_string(),
        "issuer": cert.issuer.rfc4514_string(),
        "serial_number": cert.serial_number,
        "not_valid_before": cert.not_valid_before_utc,
        "not_valid_after": cert.not_valid_after_utc,
        "is_expired": cert.not_valid_after_utc < datetime.datetime.now(datetime.timezone.utc),
    }
```

---

## 6. TLS/SSL Configuration <a name="6-tls"></a>

### FastAPI with SSL

```python
import uvicorn
import ssl

# Create SSL context
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain("cert.pem", "key.pem")

# Run with HTTPS
uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=443,
    ssl_certfile="cert.pem",
    ssl_keyfile="key.pem",
)
```

### TLS Configuration

```python
import ssl

def create_ssl_context():
    """Create a secure SSL context."""
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    # Minimum TLS version
    context.minimum_version = ssl.TLSVersion.TLSv1_3

    # Disable old protocols
    context.options |= ssl.OP_NO_SSLv2
    context.options |= ssl.OP_NO_SSLv3
    context.options |= ssl.OP_NO_TLSv1
    context.options |= ssl.OP_NO_TLSv1_1

    # Load certificates
    context.load_cert_chain("cert.pem", "key.pem")
    context.load_verify_locations("ca-bundle.crt")

    # Verify client certificates (mutual TLS)
    context.verify_mode = ssl.CERT_REQUIRED

    return context
```

### Production TLS with Nginx

```nginx
# /etc/nginx/sites-available/myapp
server {
    listen 443 ssl http2;
    server_name myapp.com;

    ssl_certificate /etc/letsencrypt/live/myapp.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/myapp.com/privkey.pem;

    # Modern TLS configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # HSTS
    add_header Strict-Transport-Security "max-age=63072000" always;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name myapp.com;
    return 301 https://$server_name$request_uri;
}
```

---

## 7. JWT Security <a name="7-jwt"></a>

### Secure JWT Implementation

```python
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from pydantic import BaseModel

class TokenPayload(BaseModel):
    sub: str
    exp: datetime
    iat: datetime
    type: str  # "access" or "refresh"
    jti: str  # Unique token ID

class JWTManager:
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 15,
        refresh_token_expire_days: int = 7,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    def create_access_token(
        self,
        subject: str,
        extra_claims: Optional[dict] = None,
    ) -> str:
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=self.access_token_expire_minutes)

        payload = {
            "sub": subject,
            "exp": expire,
            "iat": now,
            "type": "access",
            "jti": secrets.token_urlsafe(32),
        }
        if extra_claims:
            payload.update(extra_claims)

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, subject: str) -> str:
        now = datetime.now(timezone.utc)
        expire = now + timedelta(days=self.refresh_token_expire_days)

        payload = {
            "sub": subject,
            "exp": expire,
            "iat": now,
            "type": "refresh",
            "jti": secrets.token_urlsafe(32),
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str, expected_type: str = "access") -> dict:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )

            # Verify token type
            if payload.get("type") != expected_type:
                raise JWTError("Invalid token type")

            return payload

        except JWTError as e:
            raise ValueError(f"Invalid token: {e}")

# Usage
jwt_manager = JWTManager(
    secret_key=settings.JWT_SECRET_KEY,
    algorithm="HS256",
    access_token_expire_minutes=15,
    refresh_token_expire_days=7,
)

# Create tokens
access_token = jwt_manager.create_access_token(subject="user123")
refresh_token = jwt_manager.create_refresh_token(subject="user123")

# Verify tokens
payload = jwt_manager.verify_token(access_token, expected_type="access")
```

### JWT with RSA (Asymmetric)

```python
from jose import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

class RSAJWTManager:
    def __init__(self, private_key_path: str, public_key_path: str):
        with open(private_key_path, "r") as f:
            self.private_key = f.read()
        with open(public_key_path, "r") as f:
            self.public_key = f.read()

    def create_token(self, subject: str) -> str:
        payload = {
            "sub": subject,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(
            payload,
            self.private_key,
            algorithm="RS256",
        )

    def verify_token(self, token: str) -> dict:
        return jwt.decode(
            token,
            self.public_key,
            algorithms=["RS256"],
        )
```

---

## 8. Best Practices <a name="8-best-practices"></a>

### 1. Use Strong Algorithms

```python
# GOOD
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# BAD
pwd_context = CryptContext(schemes=["md5"], deprecated="auto")  # Never use MD5!
pwd_context = CryptContext(schemes=["sha1"], deprecated="auto")  # Never use SHA1!
```

### 2. Generate Secure Random Values

```python
import secrets

# GOOD - Cryptographically secure
token = secrets.token_urlsafe(32)
key = secrets.token_hex(32)
number = secrets.randbelow(100)

# BAD - Not cryptographically secure
import random
token = str(random.randint(0, 99999999))  # Predictable!
```

### 3. Use Constant-Time Comparison

```python
import hmac

# GOOD - Constant-time comparison
hmac.compare_digest(expected, actual)

# BAD - Variable-time comparison (vulnerable to timing attacks)
if expected == actual:  # VULNERABLE!
    pass
```

### 4. Protect Keys in Memory

```python
# Store keys securely
import os
from pathlib import Path

def load_key_from_file(key_path: str) -> bytes:
    """Load encryption key from file with restricted permissions."""
    path = Path(key_path)
    if path.stat().st_mode & 0o777 != 0o600:
        raise ValueError(f"Key file {key_path} has insecure permissions")
    return path.read_bytes()
```

### 5. Use Environment Variables for Keys

```python
import os

# NEVER hardcode keys
SECRET_KEY = os.environ["SECRET_KEY"]  # From environment

# NEVER commit keys to Git
# .gitignore should include: *.pem, *.key, .env
```

---

## Summary

| Operation | Algorithm | Library | Use Case |
|-----------|-----------|---------|----------|
| Password Hashing | Argon2/bcrypt | passlib | User authentication |
| Symmetric Encryption | AES-GCM | cryptography | Data at rest |
| Asymmetric Encryption | RSA/ECC | cryptography | Key exchange |
| Message Auth | HMAC-SHA256 | hmac | Webhook verification |
| Token Signing | RS256/ES256 | python-jose | JWT tokens |
| TLS | TLS 1.3 | ssl | HTTPS |

### Key Rules

1. Never store plaintext passwords (use Argon2/bcrypt)
2. Use AES-GCM for encryption (not ECB/CBC without care)
3. Use HMAC-SHA256 for message authentication
4. Use TLS 1.3 for all connections
5. Generate secrets with `secrets` module (not `random`)
6. Use constant-time comparison for hashes
7. Rotate encryption keys regularly
