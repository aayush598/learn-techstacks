# Docker for FastAPI — Complete Deployment Guide

## Table of Contents
1. [Docker Fundamentals for FastAPI](#docker-fundamentals)
2. [Basic Dockerfile](#basic-dockerfile)
3. [Multi-Stage Builds](#multi-stage-builds)
4. [Layer Optimization](#layer-optimization)
5. [.dockerignore](#dockerignore)
6. [Docker Compose](#docker-compose)
7. [Dev vs Production Setup](#dev-vs-production)
8. [Health Checks](#health-checks)
9. [Non-Root User](#non-root-user)
10. [Docker Networking](#docker-networking)
11. [Volumes](#volumes)
12. [Environment Variables](#environment-variables)
13. [Best Practices](#best-practices)

---

## Docker Fundamentals for FastAPI <a name="docker-fundamentals"></a>

Docker containers package your FastAPI application with all its dependencies into a single, reproducible unit. This eliminates the "works on my machine" problem and ensures consistency across environments.

**Key Concepts:**
- **Image**: Read-only template containing your app, dependencies, and OS layers
- **Container**: Running instance of an image
- **Dockerfile**: Instruction set for building an image
- **Layer**: Each Dockerfile instruction creates a cached layer
- **Registry**: Storage for images (Docker Hub, ECR, GCR)

---

## Basic Dockerfile <a name="basic-dockerfile"></a>

```dockerfile
# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy requirements first (leverages Docker layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Simple project structure:**
```
my-fastapi-app/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   └── database.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

**requirements.txt:**
```
fastapi==0.115.0
uvicorn[standard]==0.30.0
sqlalchemy==2.0.35
pydantic==2.9.0
python-dotenv==1.0.1
```

**app/main.py:**
```python
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database connection pool
    print("Starting up: connecting to database...")
    yield
    # Shutdown: close connections
    print("Shutting down: closing connections...")

app = FastAPI(title="My API", version="1.0.0", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello from Docker!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

---

## Multi-Stage Builds <a name="multi-stage-builds"></a>

Multi-stage builds separate the build environment from the runtime environment, producing smaller, more secure images.

### Production Multi-Stage Dockerfile

```dockerfile
# ============================================
# Stage 1: Builder
# ============================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ============================================
# Stage 2: Production
# ============================================
FROM python:3.12-slim AS production

# Install only runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 curl && \
    rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser ./app ./app

# Switch to non-root user
USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Why Multi-Stage?

| Aspect | Single Stage | Multi-Stage |
|--------|-------------|-------------|
| Image Size | ~900MB | ~150MB |
| Build Tools in Prod | Yes (gcc, dev headers) | No |
| Attack Surface | Larger | Smaller |
| Build Cache Efficiency | Lower | Higher |

### Slim vs Alpine vs Full

```dockerfile
# Full image (~900MB) — has everything
FROM python:3.12

# Slim image (~150MB) — Debian-based, no dev tools
FROM python:3.12-slim

# Alpine image (~50MB) — musl libc, may cause issues
FROM python:3.12-alpine

# Recommended: slim for most use cases
# Alpine when image size is critical but test thoroughly
# Some C extensions don't compile cleanly on Alpine
```

---

## Layer Optimization <a name="layer-optimization"></a>

Each instruction in a Dockerfile creates a layer. Layers are cached and reused. Order matters for cache efficiency.

### Bad Ordering (Invalidates cache frequently)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .                          # Copies EVERYTHING — any change invalidates all below
RUN pip install -r requirements.txt
RUN python -m pytest               # Tests baked into image!
```

### Good Ordering (Maximizes cache hits)

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Layer 1: System dependencies (rarely changes)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Layer 2: Python dependencies (changes only when requirements change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Layer 3: Application code (changes most frequently)
COPY ./app ./app

# Cleanup build dependencies (reduces final image size)
RUN apt-get purge -y gcc && \
    apt-get autoremove -y
```

### Layer Size Reduction Techniques

```dockerfile
# Combine RUN commands to reduce layers
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Use --no-cache-dir for pip
RUN pip install --no-cache-dir -r requirements.txt

# Clean up in the same layer you install
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache

# Use .dockerignore to prevent unnecessary COPY context
```

---

## .dockerignore <a name="dockerignore"></a>

Prevent files from being sent to the Docker daemon, reducing build context size and preventing accidental inclusion of sensitive files.

```dockerignore
# Version control
.git
.gitignore

# Python artifacts
__pycache__
*.pyc
*.pyo
*.egg-info
dist/
build/
*.egg

# Virtual environments
venv/
.venv/
env/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/
tests/

# Documentation
docs/
*.md
LICENSE

# Docker files (prevent recursive builds)
Dockerfile*
docker-compose*.yml

# Environment files (use Docker secrets or env vars instead)
.env
.env.*
!.env.example

# OS files
.DS_Store
Thumbs.db

# CI/CD
.github/
.gitlab-ci.yml
.circleci/

# Node (if using frontend build stages)
node_modules/
npm-debug.log
```

---

## Docker Compose <a name="docker-compose"></a>

### Development Compose

```yaml
# docker-compose.yml
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: development        # Use development stage
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app/app           # Hot reload: mount source code
      - ./tests:/app/tests
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:secret@db:5432/myapp
      - REDIS_URL=redis://redis:6379/0
      - ENVIRONMENT=development
      - DEBUG=true
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Production Compose

```yaml
# docker-compose.prod.yml
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - ENVIRONMENT=production
      - DEBUG=false
      - SENTRY_DSN=${SENTRY_DSN}
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
        reservations:
          cpus: "0.5"
          memory: 256M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    depends_on:
      - db
      - redis
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - backend

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/certs:/etc/nginx/certs:ro
    depends_on:
      - app
    networks:
      - backend

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend
    # No port mapping — only accessible within the backend network

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - backend

networks:
  backend:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

---

## Dev vs Production Setup <a name="dev-vs-production"></a>

### Multi-Stage Dockerfile with Dev and Prod Targets

```dockerfile
# ============================================
# Base stage — shared between dev and prod
# ============================================
FROM python:3.12-slim AS base

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        curl && \
    rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ============================================
# Development stage
# ============================================
FROM base AS development

# Install dev dependencies
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "debug"]

# ============================================
# Testing stage
# ============================================
FROM base AS testing

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

CMD ["pytest", "-v", "--cov=app", "--cov-report=term-missing"]

# ============================================
# Production stage
# ============================================
FROM python:3.12-slim AS production

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 \
        curl && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

COPY --from=base /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY --chown=appuser:appuser ./app ./app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["gunicorn", "app.main:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "4", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120", \
     "--graceful-timeout", "30", \
     "--keep-alive", "5"]
```

### Development Requirements

```txt
# requirements-dev.txt
-r requirements.txt
pytest==8.3.0
pytest-asyncio==0.24.0
pytest-cov==5.0.0
httpx==0.27.0
black==24.8.0
ruff==0.6.0
mypy==1.11.0
```

---

## Health Checks <a name="health-checks"></a>

### Dockerfile Health Check

```dockerfile
# Simple HTTP check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Using Python (no curl dependency)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Check specific endpoint with expected response
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health | python -c "import sys,json; d=json.load(sys.stdin); exit(0 if d.get('status')=='healthy' else 1)" || exit 1
```

### Health Check Parameters

| Parameter | Description | Recommended |
|-----------|-------------|-------------|
| `interval` | Time between checks | 15-60s |
| `timeout` | Max time per check | 5-10s |
| `start_period` | Grace period for startup | 10-30s |
| `retries` | Consecutive failures before unhealthy | 3 |

### FastAPI Health Endpoint

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import asyncio
import asyncpg

app = FastAPI()

async def check_database() -> bool:
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute("SELECT 1")
        await conn.close()
        return True
    except Exception:
        return False

async def check_redis() -> bool:
    try:
        redis = aioredis.from_url(REDIS_URL)
        await redis.ping()
        await redis.close()
        return True
    except Exception:
        return False

@app.get("/health")
async def health_check():
    checks = {
        "database": await check_database(),
        "redis": await check_redis(),
    }
    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "healthy" if all_healthy else "unhealthy",
            "checks": checks,
        }
    )

@app.get("/health/ready")
async def readiness():
    """Readiness probe: is the service ready to accept traffic?"""
    return {"status": "ready"}

@app.get("/health/live")
async def liveness():
    """Liveness probe: is the service alive?"""
    return {"status": "alive"}
```

---

## Non-Root User <a name="non-root-user"></a>

Running containers as root is a security vulnerability. Always use a non-root user.

```dockerfile
FROM python:3.12-slim

# Create a dedicated user and group
RUN groupadd -r appuser && \
    useradd -r -g appuser -d /app -s /sbin/nologin -c "Application User" appuser

WORKDIR /app

# Set ownership during COPY
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser ./app ./app

# Create directories the app needs, with proper ownership
RUN mkdir -p /app/logs /app/tmp && \
    chown -R appuser:appuser /app

# Switch to non-root user BEFORE CMD
USER appuser

# Ensure the user can't escalate privileges
# Do NOT use --cap-add or --privileged in docker run

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Why Non-Root?

```
Risk: If attacker escapes the container, they get root on the host.
Mitigation: Non-root user limits the blast radius.

# Check if your container runs as root:
docker run --rm myimage whoami    # Should NOT output "root"

# Audit existing images:
docker run --rm --entrypoint "" myimage id
```

---

## Docker Networking <a name="docker-networking"></a>

```yaml
# docker-compose.yml networking
version: "3.9"

services:
  app:
    build: .
    networks:
      - frontend
      - backend
    # DNS: other services on the same network are reachable by service name
    # e.g., "db" resolves to the db service's IP

  nginx:
    image: nginx:alpine
    networks:
      - frontend
    # Only accessible from the frontend network

  db:
    image: postgres:16-alpine
    networks:
      - backend
    # NOT accessible from outside — no port mapping + isolated network

  redis:
    image: redis:7-alpine
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true    # No external access — backend-only network
```

### Network Types

| Type | Description | Use Case |
|------|-------------|----------|
| `bridge` | Default. Isolated network on single host | Most common for docker-compose |
| `host` | Container uses host's network stack | Performance-critical apps |
| `overlay` | Multi-host networking | Docker Swarm, multi-node |
| `none` | No networking | Security-sensitive containers |
| `internal` | No external access | Database/backend services |

### Service Discovery

```python
# FastAPI connecting to services by Docker service name
DATABASE_URL = "postgresql+asyncpg://user:pass@db:5432/myapp"
#                                              ^^
#                                    Docker service name, not localhost

REDIS_URL = "redis://redis:6379/0"
#                    ^^^^^
#              Docker service name

# In docker-compose, services find each other via DNS
# The Docker DNS resolver maps service names to container IPs
```

---

## Volumes <a name="volumes"></a>

### Types of Volumes

```yaml
services:
  app:
    build: .
    volumes:
      # Named volume (managed by Docker)
      - app_data:/app/data

      # Bind mount (mount host directory)
      - ./app:/app/app                    # Dev: hot reload
      - ./logs:/app/logs                  # Persist logs

      # Read-only bind mount
      - ./config:/app/config:ro

      # tmpfs mount (temporary, in-memory)
      - type: tmpfs
        target: /app/tmp
        tmpfs:
          size: 100M

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data    # Named volume for DB
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro  # Init script

volumes:
  app_data:
  postgres_data:
```

### Volume Management Commands

```bash
# List volumes
docker volume ls

# Inspect a volume
docker volume inspect postgres_data

# Remove unused volumes
docker volume prune

# Backup a volume
docker run --rm -v postgres_data:/data -v $(pwd):/backup \
    alpine tar czf /backup/postgres_backup.tar.gz -C /data .

# Restore a volume
docker run --rm -v postgres_data:/data -v $(pwd):/backup \
    alpine tar xzf /backup/postgres_backup.tar.gz -C /data
```

---

## Environment Variables <a name="environment-variables"></a>

### Methods of Setting Environment Variables

```yaml
# docker-compose.yml
services:
  app:
    build: .

    # Method 1: Inline environment variables
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/myapp
      - REDIS_URL=redis://redis:6379/0
      - ENVIRONMENT=production

    # Method 2: From .env file
    env_file:
      - .env
      - .env.production

    # Method 3: Variable substitution from host
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - API_KEY=${API_KEY}
```

### .env File

```bash
# .env (development)
DATABASE_URL=postgresql+asyncpg://postgres:secret@db:5432/myapp_dev
REDIS_URL=redis://redis:6379/0
SECRET_KEY=dev-secret-key-not-for-production
DEBUG=true
ENVIRONMENT=development

# .env.production (use Docker secrets in real production)
DATABASE_URL=postgresql+asyncpg://prod_user:strong_pass@db:5432/myapp
REDIS_URL=redis://redis:6379/0
SECRET_KEY=production-secret-key
DEBUG=false
ENVIRONMENT=production
SENTRY_DSN=https://xxx@sentry.io/xxx
```

### Docker Secrets (Swarm / Compose)

```yaml
# docker-compose.yml
version: "3.9"

services:
  app:
    build: .
    secrets:
      - db_password
      - api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    file: ./secrets/api_key.txt
```

```python
# Reading secrets in FastAPI
from pathlib import Path

def read_secret(name: str) -> str:
    secret_path = Path(f"/run/secrets/{name}")
    if secret_path.exists():
        return secret_path.read_text().strip()
    return os.environ.get(name.upper(), "")

DATABASE_PASSWORD = read_secret("db_password")
API_KEY = read_secret("api_key")
```

### Accessing Secrets via Environment Variables

```python
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://localhost:5432/myapp"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "change-me"
    debug: bool = False
    environment: str = "development"
    sentry_dsn: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

---

## Best Practices <a name="best-practices"></a>

### Dockerfile Best Practices

```dockerfile
# 1. Use specific tags, not :latest
FROM python:3.12.5-slim    # Good
FROM python:latest          # Bad

# 2. Order instructions from least to most frequently changing
COPY requirements.txt .    # Rarely changes
RUN pip install ...        # Depends on requirements.txt
COPY ./app ./app           # Changes often

# 3. Use COPY instead of ADD
COPY requirements.txt .    # Good
ADD requirements.txt .     # Bad (ADD has hidden features like tar extraction)

# 4. Use --no-cache-dir for pip
RUN pip install --no-cache-dir -r requirements.txt

# 5. Clean up in the same layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y gcc && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# 6. Use LABEL for metadata
LABEL maintainer="team@example.com"
LABEL version="1.0"
LABEL description="FastAPI application"

# 7. Set PYTHONUNBUFFERED for proper logging
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
```

### Security Best Practices

```bash
# Scan images for vulnerabilities
docker scan myimage:latest

# Use Trivy for comprehensive scanning
trivy image myimage:latest

# Pin base image digests for reproducibility
FROM python:3.12-slim@sha256:abc123...

# Never store secrets in images
# Use Docker secrets, environment variables at runtime, or vault solutions
```

### Build Optimization

```bash
# Build with BuildKit (faster, better caching)
DOCKER_BUILDKIT=1 docker build -t myapp:latest .

# Build specific target
docker build --target production -t myapp:prod .

# Build with build args
docker build --build-arg PYTHON_VERSION=3.12 -t myapp:latest .

# Multi-platform builds
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest .
```

### Production Runtime

```bash
# Run with resource limits
docker run -d \
    --name myapp \
    --memory 512m \
    --cpus 1.0 \
    --restart unless-stopped \
    -p 8000:8000 \
    myapp:latest

# Run with read-only filesystem
docker run -d \
    --read-only \
    --tmpfs /tmp \
    --tmpfs /app/tmp \
    myapp:latest
```

---

## Interview Questions <a name="interview-questions"></a>

1. **Why use multi-stage Docker builds?**
   Separates build dependencies from runtime, reducing image size and attack surface. Build tools like gcc don't ship in production.

2. **What is Docker layer caching and how do you optimize it?**
   Each Dockerfile instruction creates a layer. Docker reuses cached layers on rebuilds. Place rarely-changing instructions (apt-get, pip install) before frequently-changing ones (COPY . .).

3. **Why should you copy `requirements.txt` before `COPY . .`?**
   Dependencies change less frequently than code. By copying requirements first, Docker caches the pip install layer and only rebuilds it when requirements change.

4. **What is the difference between `CMD` and `ENTRYPOINT`?**
   `CMD` provides default arguments that can be overridden. `ENTRYPOINT` defines the executable. Use `ENTRYPOINT` with `CMD` for flexibility: `ENTRYPOINT ["python"]`, `CMD ["main.py"]`.

5. **Why run containers as non-root?**
   If an attacker escapes the container, they get root on the host. A non-root user limits privilege escalation. It's a Docker security best practice.

6. **What is the purpose of `.dockerignore`?**
   Prevents sending unnecessary files (`.git`, `venv`, `tests`) to the Docker daemon, reducing build context size and build time. Also prevents accidental inclusion of secrets.

7. **Explain the difference between `docker-compose.yml` and `docker-compose.prod.yml`.**
   Dev compose includes hot-reload volumes, debug ports, and test databases. Prod compose uses health checks, resource limits, no debug volumes, and secure networking.

8. **How do you handle database migrations in Docker?**
   Run migrations as an init container or entrypoint script before starting the app. Use Alembic: `CMD ["bash", "-c", "alembic upgrade head && gunicorn ..."]`.

9. **What health check parameters would you configure and why?**
   `interval: 30s` (balance between responsiveness and overhead), `timeout: 10s` (enough for DB check), `start_period: 10s` (app startup time), `retries: 3` (avoid flapping).

10. **How do you manage secrets in Docker?**
    Use Docker secrets (Swarm), mounted files (`/run/secrets/`), or environment variables from a secrets manager. Never hardcode secrets in Dockerfiles or images.

11. **What is Docker BuildKit and why use it?**
    BuildKit is the modern build engine for Docker. It provides parallel layer builds, better caching, secret mounting during build, and improved output formatting.

12. **How do you reduce Docker image size for Python apps?**
    Use slim base images, multi-stage builds, `--no-cache-dir` for pip, remove build dependencies in the same layer, and use `.dockerignore`.

13. **Explain Docker networking modes.**
    `bridge` (default, isolated), `host` (shares host network), `overlay` (multi-host), `none` (disabled), `internal` (no external access). Use internal for databases.

14. **How do you handle logging in Docker containers?**
    Write logs to stdout/stderr. Docker captures them via the `json-file` or `fluentd` logging driver. Use structured JSON logging for easy parsing.

15. **What's the difference between a bind mount and a named volume?**
    Bind mounts reference a specific host path. Named volumes are Docker-managed and stored in `/var/lib/docker/volumes/`. Named volumes are portable; bind mounts are for development.
