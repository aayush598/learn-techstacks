# Secrets Management

## Table of Contents

1. [Introduction](#1-introduction)
2. [Environment Variables](#2-env-vars)
3. [pydantic-settings](#3-pydantic-settings)
4. [.env Files](#4-dotenv)
5. [AWS Secrets Manager](#5-aws)
6. [HashiCorp Vault](#6-vault)
7. [Docker Secrets](#7-docker)
8. [Secret Rotation](#8-rotation)
9. [Logging and Auditing](#9-logging)
10. [Secret Scanning in CI](#10-scanning)
11. [Best Practices](#11-best-practices)

---

## 1. Introduction <a name="1-introduction"></a>

Secrets are sensitive data that must be protected: API keys, database passwords,
encryption keys, JWT signing keys, etc. Improper secrets management is one of the
most common security vulnerabilities.

### Common Secrets in FastAPI Applications

- Database connection strings
- JWT signing keys
- API keys (Stripe, SendGrid, AWS, etc.)
- Redis passwords
- OAuth client secrets
- Encryption keys
- Webhook signing secrets

### Secrets Management Principles

1. **Never commit secrets to version control**
2. **Use environment variables or secret managers**
3. **Rotate secrets regularly**
4. **Limit access to secrets**
5. **Audit secret usage**
6. **Don't log secrets**

---

## 2. Environment Variables <a name="2-env-vars"></a>

### Basic Usage

```python
import os

# Read from environment
DATABASE_URL = os.environ["DATABASE_URL"]  # Raises KeyError if missing
SECRET_KEY = os.environ.get("SECRET_KEY", "default-dev-key")  # With default

# With validation
def get_database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL environment variable is required")
    return url
```

### Environment Variable Configuration

```python
import os
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Settings:
    # Required - no defaults
    DATABASE_URL: str = os.environ["DATABASE_URL"]
    SECRET_KEY: str = os.environ["SECRET_KEY"]
    JWT_SECRET_KEY: str = os.environ["JWT_SECRET_KEY"]

    # Optional with defaults
    REDIS_URL: str = os.environ.get("REDIS_URL", "redis://localhost:6379")
    DEBUG: bool = os.environ.get("DEBUG", "false").lower() == "true"
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")

    # API Keys
    STRIPE_API_KEY: str = os.environ.get("STRIPE_API_KEY", "")
    SENDGRID_API_KEY: str = os.environ.get("SENDGRID_API_KEY", "")
    AWS_ACCESS_KEY_ID: Optional[str] = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.environ.get("AWS_SECRET_ACCESS_KEY")

    def __post_init__(self):
        # Validate required settings
        if self.ENVIRONMENT == "production":
            if self.DEBUG:
                raise ValueError("DEBUG cannot be True in production")
            if "localhost" in self.DATABASE_URL:
                raise ValueError("Cannot use localhost database in production")

settings = Settings()
```

### Setting Environment Variables

```bash
# Linux/Mac
export DATABASE_URL="postgresql://user:pass@localhost/db"
export SECRET_KEY="your-secret-key"

# Windows
set DATABASE_URL=postgresql://user:pass@localhost/db

# In .env file (load with python-dotenv)
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=your-secret-key
```

### Docker Environment Variables

```yaml
# docker-compose.yml
services:
  api:
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - SECRET_KEY=${SECRET_KEY}
    env_file:
      - .env
```

---

## 3. pydantic-settings <a name="3-pydantic-settings"></a>

### Basic Configuration

```python
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import Optional

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "MyApp"
    ENVIRONMENT: str = Field("development", description="Environment name")
    DEBUG: bool = Field(False, description="Enable debug mode")

    # Database
    DATABASE_URL: str = Field(..., description="Database connection URL")
    DATABASE_POOL_SIZE: int = Field(20, ge=1, le=100)
    DATABASE_MAX_OVERFLOW: int = Field(10, ge=0, le=50)

    # Redis
    REDIS_URL: str = Field("redis://localhost:6379", description="Redis URL")

    # Security
    SECRET_KEY: str = Field(..., min_length=32, description="Application secret key")
    JWT_SECRET_KEY: str = Field(..., min_length=32, description="JWT signing key")
    JWT_ALGORITHM: str = Field("HS256", description="JWT algorithm")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, ge=1)
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(7, ge=1)

    # API Keys
    STRIPE_API_KEY: Optional[str] = Field(None, description="Stripe API key")
    SENDGRID_API_KEY: Optional[str] = Field(None, description="SendGrid API key")
    AWS_ACCESS_KEY_ID: Optional[str] = Field(None)
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(None)

    # CORS
    CORS_ORIGINS: list[str] = Field(
        ["http://localhost:3000"],
        description="Allowed CORS origins",
    )

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v):
        if not v.startswith(("postgresql://", "postgresql+asyncpg://", "sqlite://")):
            raise ValueError("Invalid database URL scheme")
        return v

    @field_validator("SECRET_KEY", "JWT_SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v):
        if v in ("secret", "change-me", "default-secret-key"):
            raise ValueError("Secret key must be changed from default")
        return v

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "env_prefix": "APP_",  # Environment variables prefixed with APP_
    }

# Usage
settings = Settings()

# Access settings
print(settings.DATABASE_URL)
print(settings.DEBUG)
```

### With Environment Prefix

```python
# If env_prefix = "MYAPP_", then:
# MYAPP_DATABASE_URL maps to DATABASE_URL
# MYAPP_SECRET_KEY maps to SECRET_KEY

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    model_config = {"env_prefix": "MYAPP_"}

# Environment: MYAPP_DATABASE_URL=postgresql://...
```

### Nested Settings

```python
from pydantic import BaseModel
from pydantic_settings import BaseSettings

class DatabaseSettings(BaseModel):
    URL: str = "postgresql://localhost/mydb"
    POOL_SIZE: int = 20
    MAX_OVERFLOW: int = 10
    ECHO: bool = False

class RedisSettings(BaseModel):
    URL: str = "redis://localhost:6379"
    MAX_CONNECTIONS: int = 20

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    SECRET_KEY: str

    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()

    model_config = {"env_file": ".env"}

settings = Settings()
print(settings.database.URL)
print(settings.redis.URL)
```

---

## 4. .env Files <a name="4-dotenv"></a>

### Using python-dotenv

```python
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()  # Loads from .env in current directory
load_dotenv(".env.local")  # Load specific file
load_dotenv(override=True)  # Override existing env vars

# Now access via os.environ
DATABASE_URL = os.environ["DATABASE_URL"]
```

### .env File Structure

```bash
# .env - Development defaults (safe to commit)
APP_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite:///./dev.db
SECRET_KEY=dev-secret-key-not-for-production
CORS_ORIGINS=["http://localhost:3000"]

# .env.local - Local overrides (NEVER commit)
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
SECRET_KEY=your-actual-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
STRIPE_API_KEY=sk_test_your_stripe_key
SENDGRID_API_KEY=SG.your_sendgrid_key
```

### .env.example (Commit to Git)

```bash
# .env.example - Template for other developers
APP_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
REDIS_URL=redis://localhost:6379
SECRET_KEY=generate-a-strong-secret-key
JWT_SECRET_KEY=generate-another-strong-secret-key
CORS_ORIGINS=["http://localhost:3000"]
STRIPE_API_KEY=sk_test_your_stripe_key
SENDGRID_API_KEY=SG.your_sendgrid_key
```

### .gitignore

```gitignore
# .gitignore
.env
.env.local
.env.*.local
*.env
```

### Pydantic Settings with .env

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    DEBUG: bool = False

    model_config = {
        "env_file": (".env", ".env.local"),  # Load in order, later overrides earlier
        "env_file_encoding": "utf-8",
    }
```

---

## 5. AWS Secrets Manager <a name="5-aws"></a>

### Setup

```bash
pip install boto3
```

### Basic Usage

```python
import boto3
import json
from functools import lru_cache

@lru_cache()
def get_secrets() -> dict:
    """Fetch secrets from AWS Secrets Manager."""
    session = boto3.session.client(
        service_name="secretsmanager",
        region_name="us-east-1",
    )
    response = session.get_secret_value(SecretId="myapp/production")
    return json.loads(response["SecretString"])

# Usage
secrets = get_secrets()
DATABASE_URL = secrets["DATABASE_URL"]
SECRET_KEY = secrets["SECRET_KEY"]
```

### With pydantic-settings

```python
import boto3
import json
from pydantic_settings import BaseSettings
from functools import lru_cache

@lru_cache()
def get_aws_secrets(secret_name: str) -> dict:
    client = boto3.client("secretsmanager", region_name="us-east-1")
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])

class Settings(BaseSettings):
    ENVIRONMENT: str = "production"

    @classmethod
    def settings_customise_sources(cls, settings_cls, init_settings, env_settings, dotenv_settings):
        # Load from AWS Secrets Manager
        try:
            secrets = get_aws_secrets(f"myapp/{settings_cls.ENVIRONMENT}")
            return init_settings, env_settings, dotenv_settings, secrets
        except Exception:
            return init_settings, env_settings, dotenv_settings

    model_config = {"env_file": ".env"}
```

### Secrets Manager with IAM

```python
import boto3
import json
from botocore.exceptions import ClientError

class SecretsManager:
    def __init__(self, region_name: str = "us-east-1"):
        self.client = boto3.client(
            "secretsmanager",
            region_name=region_name,
        )

    def get_secret(self, secret_id: str) -> dict:
        try:
            response = self.client.get_secret_value(SecretId=secret_id)
            return json.loads(response["SecretString"])
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                raise ValueError(f"Secret {secret_id} not found")
            elif e.response["Error"]["Code"] == "AccessDeniedException":
                raise PermissionError(f"Access denied to secret {secret_id}")
            raise

    def create_secret(self, name: str, secret_dict: dict) -> str:
        response = self.client.create_secret(
            Name=name,
            SecretString=json.dumps(secret_dict),
        )
        return response["ARN"]

    def rotate_secret(self, secret_id: str, new_value: dict):
        self.client.put_secret_value(
            SecretId=secret_id,
            SecretString=json.dumps(new_value),
        )

# Usage
sm = SecretsManager()
db_secrets = sm.get_secret("myapp/database")
```

---

## 6. HashiCorp Vault <a name="6-vault"></a>

### Setup

```bash
pip install hvac
```

### Basic Usage

```python
import hvac

def get_vault_client():
    client = hvac.Client(
        url="https://vault.example.com:8200",
        token="your-vault-token",  # Use AppRole or Kubernetes auth in production
    )
    if not client.is_authenticated():
        raise ConnectionError("Vault authentication failed")
    return client

def get_vault_secrets(path: str) -> dict:
    client = get_vault_client()
    response = client.secrets.kv.v2.read_secret_version(path=path)
    return response["data"]["data"]

# Usage
secrets = get_vault_secrets("myapp/production")
DATABASE_URL = secrets["DATABASE_URL"]
```

### Vault with AppRole Auth

```python
import hvac

def get_vault_client_with_approle():
    client = hvac.Client(url="https://vault.example.com:8200")

    # Authenticate with AppRole
    response = client.auth.approle.login(
        role_id="your-role-id",
        secret_id="your-secret-id",
    )
    client.token = response["auth"]["client_token"]

    return client
```

### FastAPI Integration

```python
from fastapi import FastAPI
import hvac

app = FastAPI()

class VaultSettings:
    def __init__(self, vault_url: str, vault_token: str = None):
        self.client = hvac.Client(url=vault_url)
        if vault_token:
            self.client.token = vault_token

    def get_secret(self, path: str) -> dict:
        response = self.client.secrets.kv.v2.read_secret_version(path=path)
        return response["data"]["data"]

# Startup event
@app.on_event("startup")
async def load_secrets():
    vault = VaultSettings(vault_url="https://vault.example.com:8200")
    app.state.secrets = vault.get_secret("myapp/production")
```

---

## 7. Docker Secrets <a name="7-docker"></a>

### Docker Compose

```yaml
# docker-compose.yml
version: "3.8"

services:
  api:
    image: myapp:latest
    secrets:
      - db_password
      - jwt_secret
      - stripe_api_key
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password
      - JWT_SECRET_FILE=/run/secrets/jwt_secret
      - STRIPE_API_KEY_FILE=/run/secrets/stripe_api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  jwt_secret:
    file: ./secrets/jwt_secret.txt
  stripe_api_key:
    file: ./secrets/stripe_api_key.txt
```

### Reading Docker Secrets

```python
import os
from pathlib import Path

def get_docker_secret(secret_name: str) -> str:
    """Read Docker secret from file."""
    secret_path = Path(f"/run/secrets/{secret_name}")
    if secret_path.exists():
        return secret_path.read_text().strip()
    # Fallback to environment variable
    return os.environ.get(secret_name.upper(), "")

# Usage
DATABASE_PASSWORD = get_docker_secret("db_password")
JWT_SECRET = get_docker_secret("jwt_secret")
STRIPE_KEY = get_docker_secret("stripe_api_key")
```

### Docker Swarm Secrets

```bash
# Create secrets
echo "my-password" | docker secret create db_password -
echo "my-jwt-secret" | docker secret create jwt_secret -

# List secrets
docker secret ls

# Deploy with secrets
docker stack deploy -c docker-compose.yml myapp
```

---

## 8. Secret Rotation <a name="8-rotation"></a>

### Database Password Rotation

```python
import asyncio
from datetime import datetime, timedelta

class SecretRotator:
    def __init__(self, db, redis):
        self.db = db
        self.redis = redis

    async def rotate_database_password(self):
        """Rotate database password and update all services."""
        import secrets
        import string

        # Generate new password
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        new_password = ''.join(secrets.choice(alphabet) for _ in range(32))

        # Update in database
        await self.db.execute(
            text("ALTER USER app_user WITH PASSWORD :password"),
            {"password": new_password},
        )

        # Update in secrets store
        await self.update_secrets_store("database", {"password": new_password})

        # Update application config
        await self.update_application_config(new_password)

        # Log rotation
        await self.log_rotation("database_password", "success")

    async def rotate_jwt_secret(self):
        """Rotate JWT signing secret."""
        import secrets

        new_secret = secrets.token_urlsafe(64)

        # Update in secrets store
        await self.update_secrets_store("jwt", {"secret_key": new_secret})

        # Invalidate all existing tokens
        await self.redis.flushdb()

        # Log rotation
        await self.log_rotation("jwt_secret", "success")
```

### Automated Rotation Schedule

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job("interval", days=30)
async def rotate_jwt_secret():
    """Rotate JWT secret every 30 days."""
    rotator = SecretRotator(db, redis)
    await rotator.rotate_jwt_secret()

@scheduler.scheduled_job("interval", days=90)
async def rotate_database_password():
    """Rotate database password every 90 days."""
    rotator = SecretRotator(db, redis)
    await rotator.rotate_database_password()

scheduler.start()
```

---

## 9. Logging and Auditing <a name="9-logging"></a>

### Never Log Secrets

```python
import logging
import re

logger = logging.getLogger(__name__)

class SecretFilter(logging.Filter):
    """Filter to remove secrets from log messages."""

    SECRET_PATTERNS = [
        (r'password[=:]\s*\S+', 'password=***'),
        (r'api_key[=:]\s*\S+', 'api_key=***'),
        (r'secret[=:]\s*\S+', 'secret=***'),
        (r'token[=:]\s*\S+', 'token=***'),
        (r'Bearer\s+\S+', 'Bearer ***'),
        (r'SG\.\S+', 'SG.***'),
        (r'sk_live_\S+', 'sk_live_***'),
        (r'sk_test_\S+', 'sk_test_***'),
    ]

    def filter(self, record):
        message = record.getMessage()
        for pattern, replacement in self.SECRET_PATTERNS:
            message = re.sub(pattern, replacement, message, flags=re.IGNORECASE)
        record.msg = message
        record.args = ()
        return True

# Add filter to root logger
logging.getLogger().addFilter(SecretFilter())

# Usage
logger.info("Connecting with password=secret123")  # Logged as: password=***
logger.info("API key: sk_live_abc123")  # Logged as: sk_live_***
```

### Audit Secret Access

```python
from datetime import datetime

class SecretAuditLog:
    def __init__(self, db):
        self.db = db

    async def log_access(
        self,
        secret_name: str,
        user_id: int,
        action: str,
        ip_address: str,
    ):
        await self.db.execute(
            audit_logs_table.insert().values(
                secret_name=secret_name,
                user_id=user_id,
                action=action,
                ip_address=ip_address,
                timestamp=datetime.utcnow(),
            )
        )
        await self.db.commit()

    async def log_rotation(
        self,
        secret_name: str,
        rotated_by: int,
        success: bool,
    ):
        await self.db.execute(
            audit_logs_table.insert().values(
                secret_name=secret_name,
                user_id=rotated_by,
                action="rotate",
                details={"success": success},
                timestamp=datetime.utcnow(),
            )
        )
        await self.db.commit()
```

---

## 10. Secret Scanning in CI <a name="10-scanning"></a>

### Git Secrets

```bash
# Install git-secrets
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets
make install

# Add hooks
git secrets --install
git secrets --register-aws
```

### detect-secrets

```bash
pip install detect-secrets

# Scan for secrets
detect-secrets scan

# Initialize baseline
detect-secrets scan --all-files > .secrets.baseline

# Audit
detect-secrets audit .secrets.baseline
```

### GitHub Secret Scanning

```yaml
# .github/workflows/secret-scan.yml
name: Secret Scan

on: [push, pull_request]

jobs:
  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: TruffleHog
        uses: trufflesecurity/trufflehog@main
        with:
          extra_args: --only-verified

      - name: Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  - repo: https://github.com/awslabs/git-secrets
    rev: master
    hooks:
      - id: git-secrets
        args: ['--register-aws']
```

---

## 11. Best Practices <a name="11-best-practices"></a>

### 1. Never Commit Secrets

```gitignore
# .gitignore
.env
.env.local
*.pem
*.key
*.p12
secrets/
credentials/
```

### 2. Use Secret Managers in Production

```python
# Development: Use .env files
# Production: Use AWS Secrets Manager, Vault, or similar

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Production will override these from secret manager
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///dev.db")
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret")
```

### 3. Rotate Secrets Regularly

```python
# Schedule regular rotation
SCHEDULED_ROTATIONS = {
    "jwt_secret": {"days": 30},
    "database_password": {"days": 90},
    "api_keys": {"days": 180},
}
```

### 4. Use Different Secrets Per Environment

```bash
# Development
SECRET_KEY=dev-key-not-for-production

# Staging
SECRET_KEY=staging-key-not-for-production

# Production
SECRET_KEY=production-real-secret-key
```

### 5. Audit Secret Access

```python
# Log who accesses secrets and when
logger.info(
    "Secret accessed",
    secret_name="database_password",
    user_id=current_user.id,
    ip_address=request.client.host,
)
```

### 6. Use Short-Lived Credentials

```python
# Prefer temporary credentials (AWS STS)
import boto3

sts = boto3.client("sts")
credentials = sts.assume_role(
    RoleArn="arn:aws:iam::123456789012:role/myapp-role",
    RoleSessionName="myapp-session",
    DurationSeconds=3600,  # 1 hour
)
```

---

## Summary

| Method | Best For | Security Level |
|--------|----------|---------------|
| Environment Variables | Development, simple deployments | Medium |
| .env files | Local development only | Low |
| pydantic-settings | Type-safe configuration | Medium |
| AWS Secrets Manager | Production (AWS) | High |
| HashiCorp Vault | Production (any cloud) | High |
| Docker Secrets | Container orchestration | High |

### Quick Start

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    JWT_SECRET_KEY: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

settings = Settings()
```

### Key Rules

1. Never commit secrets to Git
2. Use different secrets per environment
3. Rotate secrets regularly
4. Audit secret access
5. Don't log secrets
6. Use secret managers in production
