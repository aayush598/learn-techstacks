# Deployment Interview Questions

## Table of Contents
1. [Docker & Containerization](#docker--containerization)
2. [Kubernetes](#kubernetes)
3. [Cloud Deployment](#cloud-deployment)
4. [Reverse Proxy & Load Balancing](#reverse-proxy--load-balancing)
5. [Production Readiness](#production-readiness)
6. [Scaling & Performance](#scaling--performance)
7. [Environment Management](#environment-management)
8. [Health Checks & Monitoring](#health-checks--monitoring)
9. [Security](#security)
10. [Scenario-Based](#scenario-based)

---

## Docker & Containerization

### Q1: Why use multi-stage Docker builds for FastAPI?
**Answer:** Multi-stage builds separate the build environment from the runtime environment. Build stages include compilers and dev dependencies (gcc, python-dev) that aren't needed at runtime. The final image only contains the application and runtime dependencies, resulting in smaller images (150MB vs 900MB), faster pulls, and reduced attack surface.

```dockerfile
# Build stage
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Runtime stage
FROM python:3.12-slim AS runtime
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
RUN useradd --create-home appuser
USER appuser
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Q2: How do you optimize Docker layer caching for Python applications?
**Answer:** Order Dockerfile instructions from least to most frequently changing. Copy `requirements.txt` first, run `pip install`, then copy application code. This way, if only application code changes, Docker reuses the cached pip install layer. Use `--no-cache-dir` for pip, combine `RUN` commands, and leverage BuildKit's cache mounts.

### Q3: What is the difference between `CMD` and `ENTRYPOINT` in a Dockerfile?
**Answer:** `CMD` provides default arguments that can be overridden at runtime. `ENTRYPOINT` defines the executable that always runs. They work together: `ENTRYPOINT ["python"]` with `CMD ["main.py"]` runs `python main.py`. If you override the CMD, it replaces the arguments. `ENTRYPOINT` is harder to override.

### Q4: Why should containers run as a non-root user?
**Answer:** If an attacker gains code execution inside a container, running as root means they have root privileges. If they escape the container, they get root on the host. A non-root user limits privilege escalation. Create a dedicated user with `useradd`, set file ownership with `--chown`, and switch with `USER appuser` before `CMD`.

### Q5: Explain the difference between bind mounts and named volumes in Docker.
**Answer:** Bind mounts reference a specific path on the host (`./app:/app`). They're useful for development (hot reload) but depend on the host filesystem. Named volumes (`postgres_data:/var/lib/postgresql/data`) are Docker-managed, stored in `/var/lib/docker/volumes/`, portable, and better for persistent data in production.

### Q6: How do you handle secrets in Docker containers?
**Answer:** Never hardcode secrets in Dockerfiles or environment variables in docker-compose files. Use Docker secrets (Swarm mode), mount secrets as files from `/run/secrets/`, use external secret managers (AWS Secrets Manager, HashiCorp Vault), or inject via environment variables from a secure source. Use `.env` files only for development.

### Q7: What health check parameters would you configure for a FastAPI container?
**Answer:**
- `interval: 30s` — balances responsiveness with overhead
- `timeout: 10s` — enough time for database health check queries
- `start_period: 10-30s` — allows time for application startup and DB connection
- `retries: 3` — prevents flapping from transient issues
- Use curl or python commands; check specific endpoints, not just port availability.

### Q8: How do you structure a production Docker Compose setup for FastAPI?
**Answer:**

```yaml
version: '3.8'
services:
  api:
    build:
      context: .
      target: runtime
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    secrets:
      - db_password
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
    healthcheck:
      test: ["CMD", "python", "-c", "import httpx; httpx.get('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - api

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

---

## Kubernetes

### Q9: What is the difference between a liveness probe and a readiness probe in Kubernetes?
**Answer:** Liveness probe checks if the container is alive. Failure triggers a container restart (the pod is restarted). Readiness probe checks if the container is ready to accept traffic. Failure removes the pod from Service endpoints (no traffic is routed). Use startup probe for slow-starting applications to delay liveness/readiness checks.

### Q10: How does Kubernetes HPA (Horizontal Pod Autoscaler) work with FastAPI?
**Answer:** HPA monitors metrics (CPU, memory, custom metrics) and adjusts replica count. For FastAPI, configure HPA with CPU target (70%), memory target (80%), and custom metrics like requests per second. Use `stabilizationWindowSeconds` to prevent flapping. Scale up aggressively (quick policies) but scale down conservatively (long stabilization).

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fastapi-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fastapi-app
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
```

### Q11: Explain rolling update strategy with maxSurge and maxUnavailable.
**Answer:** `maxSurge: 1` allows one extra pod during update. `maxUnavailable: 0` ensures the desired count is always maintained. During update: new pod starts → passes readiness → old pod terminates → repeat. This guarantees zero downtime. For more aggressive updates, increase maxSurge. For safer updates, keep maxUnavailable at 0.

### Q12: What is Kustomize and when would you use it over Helm?
**Answer:** Kustomize customizes YAML manifests using overlays and patches without templating. Use it when you have multiple environments (dev/staging/prod) with minimal differences. Helm uses Go templates and is better for complex charts with many configurable parameters. Kustomize is built into `kubectl` and is simpler; Helm is better for distributing packages.

### Q13: How do ConfigMaps and Secrets differ in Kubernetes?
**Answer:** ConfigMaps store non-sensitive configuration (database hosts, feature flags). Secrets store sensitive data (passwords, API keys) and are base64-encoded. ConfigMaps are logged in plain text; Secrets should be encrypted at rest. Both can be mounted as files or environment variables. Secrets are not encrypted by default — enable encryption at rest for true security.

### Q14: How do you deploy FastAPI with Gunicorn and Uvicorn workers on Kubernetes?
**Answer:**

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER appuser
CMD ["gunicorn", "main:app", \
     "-w", "4", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "-b", "0.0.0.0:8000", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
```

Worker count: `CPU_COUNT * 2 + 1` for CPU-bound or `CPU_COUNT * 4 + 1` for I/O-bound. Enable `preload_app` for memory efficiency. Set `max_requests = 1000` and `max_requests_jitter = 50` to recycle workers.

---

## Cloud Deployment

### Q15: Compare ECS Fargate, Lambda+Mangum, and App Runner for FastAPI deployment.
**Answer:**
- **ECS Fargate**: Best for production workloads. Consistent performance, auto-scaling, no cold starts. More complex setup. Cost: ~$16-50/month.
- **Lambda + Mangum**: Best for sporadic traffic. Scales to zero. Cold starts (1-5s). Limited to 15min execution. Cost: pay-per-request.
- **App Runner**: Simplest setup. Auto-scaling, HTTPS, custom domains. Less control over infrastructure. Cost: ~$56/month.

### Q16: How do you deploy FastAPI to AWS Lambda using Mangum?
**Answer:** Install `mangum`, create handler: `handler = Mangum(app)`. Package as container image using Lambda base image (`public.ecr.aws/lambda/python:3.12`). Set CMD to the handler module. Deploy with AWS CLI or SAM. Connect to API Gateway. Optimize cold starts with ARM64 (Graviton2), minimal dependencies, and Provisioned Concurrency.

```python
from mangum import Mangum
from main import app

handler = Mangum(app, lifespan="off")
```

### Q17: What is the advantage of using Cloud Run for FastAPI?
**Answer:** Cloud Run is serverless containers that scale to zero. No cluster management. Built-in HTTPS, custom domains, IAM integration. Pay-per-request pricing. Automatic scaling. Simple `gcloud run deploy` command. Limitations: no persistent connections, 60-minute timeout.

### Q18: How do you connect a FastAPI app on Cloud Run to Cloud SQL?
**Answer:** Use Cloud SQL Auth Proxy as a sidecar container. The proxy connects to Cloud SQL via private IP without exposing it to the internet. Or use the Cloud SQL Python Connector library. Both methods provide IAM-based authentication. Never expose Cloud SQL with a public IP.

---

## Reverse Proxy & Load Balancing

### Q19: Why use Nginx in front of Uvicorn/Gunicorn?
**Answer:** Nginx provides SSL termination, static file serving, rate limiting, request buffering (protects against slow loris), gzip compression, load balancing across multiple workers, and security headers. Uvicorn is optimized for handling ASGI connections, not for all these proxy concerns.

### Q20: Explain the difference between upstream load balancing algorithms in Nginx.
**Answer:**
- **Round Robin** (default): Distributes equally across servers
- **Least Connections**: Routes to server with fewest active connections
- **IP Hash**: Consistent routing by client IP (session affinity)
- **Generic Hash**: Consistent hashing by custom key
- **Random with Two Least Connections**: Good for large clusters

### Q21: How do you configure rate limiting in Nginx for a FastAPI API?
**Answer:**

```nginx
http {
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=auth:10m rate=5r/m;

    server {
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            limit_req_status 429;
            proxy_pass http://backend;
        }

        location /api/auth/ {
            limit_req zone=auth burst=3 nodelay;
            limit_req_status 429;
            proxy_pass http://backend;
        }
    }
}
```

### Q22: How do you set up WebSocket proxying through Nginx for FastAPI?
**Answer:**

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}

server {
    location /ws/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_buffering off;
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
}
```

### Q23: How do you configure Nginx as a load balancer for multiple FastAPI instances?
**Answer:**

```nginx
upstream fastapi_backend {
    least_conn;
    server 10.0.0.1:8000 weight=3;
    server 10.0.0.2:8000 weight=2;
    server 10.0.0.3:8000 weight=1;

    keepalive 32;
}

server {
    location / {
        proxy_pass http://fastapi_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Production Readiness

### Q24: How do you configure Gunicorn workers for a FastAPI application?
**Answer:** Use `UvicornWorker` as `worker_class`. Set workers to `CPU_COUNT * 2 + 1` for CPU-bound or `CPU_COUNT * 4 + 1` for I/O-bound. Enable `preload_app` for memory efficiency. Set `max_requests = 1000` and `max_requests_jitter = 50` to recycle workers and prevent memory leaks.

### Q25: What is graceful shutdown and why is it important?
**Answer:** When Kubernetes sends SIGTERM, the application needs to finish in-flight requests, close database connections, flush logs, and cancel background tasks before exiting. Without graceful shutdown, requests may fail, transactions may be incomplete, and data may be corrupted.

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    await init_redis()

    yield

    # Shutdown - finish in-flight requests
    await db.close_all()
    await redis.close()

app = FastAPI(lifespan=lifespan)
```

### Q26: How do you configure database connection pooling for production FastAPI?
**Answer:** Use SQLAlchemy's async engine with `pool_size=5-20`, `max_overflow=10-30`, `pool_timeout=30`, `pool_recycle=1800`, and `pool_pre_ping=True`. In containerized environments, pool sizing must account for multiple replicas. Formula: `total_connections = pool_size * replicas`. Ensure database max_connections > total_connections from all replicas.

### Q27: How would you set up error tracking with Sentry in a FastAPI production app?
**Answer:** Initialize Sentry SDK with DSN, environment, and release version. Add `SentryAsgiMiddleware` to the app. Integrate SQLAlchemy and Redis integrations. Set `traces_sample_rate=0.1` for performance monitoring. Filter sensitive data with `before_send`.

```python
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    environment=settings.ENVIRONMENT,
    release=settings.APP_VERSION,
    traces_sample_rate=0.1,
    before_send=lambda event, hint: scrub_sensitive_data(event),
)

app.add_middleware(SentryAsgiMiddleware)
```

### Q28: What logging configuration do you recommend for production FastAPI?
**Answer:** Use structured JSON logging with `structlog`. Include timestamp, level, logger name, message, module, function, and line. Add `request_id` middleware for correlation. Write to stdout for Docker/K8s log collection. Set library loggers to WARNING. Never log sensitive data.

```python
import structlog

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)
```

### Q29: How do you implement zero-downtime deployments?
**Answer:** Use rolling updates with `maxUnavailable: 0` and `maxSurge: 1`. Implement readiness probes so new pods only receive traffic when ready. Use pre-stop hooks (`sleep 5`) to allow time for pod removal from endpoints. For database changes, use expand-contract pattern: add new columns before removing old ones.

### Q30: What metrics should you monitor in a production FastAPI application?
**Answer:**
- **RED metrics**: Rate (requests/sec), Errors (error rate), Duration (latency percentiles)
- **USE metrics**: Utilization, Saturation, Errors for infrastructure
- **Application-specific**: DB pool usage, cache hit rate, background task queue depth
- **Business metrics**: Active users, conversion rate, API usage by client
- **Infrastructure**: CPU, memory, disk, network per container/pod

---

## Scaling & Performance

### Q31: How do you optimize FastAPI for high throughput?
**Answer:**
- Use async I/O everywhere (don't block the event loop)
- Enable connection pooling for databases and Redis
- Use GZip compression at Nginx level
- Implement response caching with Redis
- Use background tasks for non-critical operations
- Profile with py-spy to find bottlenecks
- Use Uvicorn with multiple workers
- Consider using orjson for faster JSON serialization

### Q32: How do you handle database connection exhaustion at scale?
**Answer:**

```python
# Configure connection pool carefully
engine = create_async_engine(
    DATABASE_URL,
    pool_size=5,           # Connections per worker
    max_overflow=10,       # Extra connections allowed
    pool_timeout=30,       # Wait time for available connection
    pool_recycle=1800,     # Recycle connections every 30 min
    pool_pre_ping=True,    # Verify connections before use
)

# Monitor pool usage
@app.get("/metrics/db-pool")
async def db_pool_metrics():
    return {
        "size": engine.pool.size(),
        "checked_in": engine.pool.checkedin(),
        "checked_out": engine.pool.checkedout(),
        "overflow": engine.pool.overflow(),
    }
```

**Critical calculation:** If each pod has `pool_size=10` and you run 20 pods, that's 200 connections to the database. Ensure `max_connections` in PostgreSQL is configured accordingly.

### Q33: How do you implement horizontal scaling for CPU-bound operations?
**Answer:** Move CPU-bound work to background task queues with dedicated workers. Use Celery with prefork pool for true parallelism. Scale API servers and task workers independently. For real-time processing, consider using multiprocessing within the worker.

---

## Environment Management

### Q34: How do you manage configuration across environments (dev/staging/prod)?
**Answer:**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    SENTRY_DSN: str | None = None
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Per-environment overrides
# .env.development
# DATABASE_URL=sqlite:///./dev.db
# DEBUG=true

# .env.production
# DATABASE_URL=postgresql+asyncpg://prod-user:pass@db:5432/prod
# SENTRY_DSN=https://...
```

### Q35: How do you manage environment-specific secrets securely?
**Answer:** Use Kubernetes Secrets for container orchestration, AWS Secrets Manager / GCP Secret Manager for cloud deployments, HashiCorp Vault for self-hosted, and CI/CD secret injection (GitHub Actions secrets, GitLab CI variables). Never commit secrets to Git. Use sealed secrets or external secret operators for GitOps workflows.

### Q36: How do you set up CI/CD for a FastAPI application?
**Answer:**

```yaml
# GitHub Actions example
name: Deploy
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: pytest --cov=app --cov-report=xml
      - run: ruff check .

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t $ECR_REGISTRY/$APP_NAME:$GITHUB_SHA .
      - run: docker push $ECR_REGISTRY/$APP_NAME:$GITHUB_SHA
      - run: kubectl set image deployment/fastapi app=$ECR_REGISTRY/$APP_NAME:$GITHUB_SHA
```

---

## Health Checks & Monitoring

### Q37: How do you implement comprehensive health checks?
**Answer:**

```python
@app.get("/health")
async def health_check():
    checks = {}
    healthy = True

    # Database check
    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {str(e)}"
        healthy = False

    # Redis check
    try:
        await redis.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {str(e)}"
        healthy = False

    # Disk space check
    import shutil
    total, used, free = shutil.disk_usage("/")
    if free / total < 0.1:  # Less than 10% free
        checks["disk"] = f"warning: {free // (1024**3)}GB free"
    else:
        checks["disk"] = "ok"

    status_code = 200 if healthy else 503
    return JSONResponse(
        status_code=status_code,
        content={"status": "healthy" if healthy else "unhealthy", "checks": checks}
    )
```

### Q38: How do you implement a startup probe for slow-starting applications?
**Answer:**

```yaml
startupProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
  failureThreshold: 30  # Allow up to 150 seconds for startup
livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
  periodSeconds: 15
  failureThreshold: 3
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  periodSeconds: 10
  failureThreshold: 3
```

### Q39: How do you implement alerting for a FastAPI application?
**Answer:** Define Prometheus alerting rules:

```yaml
groups:
  - name: fastapi_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status_class="5xx"}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate on {{ $labels.instance }}"

      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning

      - alert: LowReplicas
        expr: count(up{job="fastapi"}) < 3
        for: 1m
        labels:
          severity: critical
```

---

## Security

### Q40: How do you secure a production FastAPI deployment?
**Answer:**
- Run containers as non-root user
- Use TLS everywhere (HTTPS, WSS)
- Implement rate limiting at Nginx level
- Set security headers (HSTS, CSP, X-Frame-Options)
- Use secrets management (not env vars for sensitive data)
- Enable CORS with specific origins (not *)
- Disable docs endpoints in production
- Implement request size limits
- Use container image scanning (Trivy, Snyk)
- Enable audit logging

### Q41: How do you implement canary deployments for FastAPI?
**Answer:**

```yaml
# Canary deployment with traffic splitting
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: fastapi-vs
spec:
  hosts:
  - fastapi-app
  http:
  - route:
    - destination:
        host: fastapi-app
        subset: stable
      weight: 90
    - destination:
        host: fastapi-app
        subset: canary
      weight: 10
```

Start with 5-10% traffic to canary. Monitor error rates, latency, and business metrics. Gradually increase traffic. Roll back if any metric degrades.

---

## Scenario-Based

### Q42: Your FastAPI application is experiencing OOM (Out of Memory) errors in production. How do you debug and fix it?
**Answer:**

1. **Identify the cause:** Check if it's a memory leak or legitimate memory usage
2. **Profile memory:** Use `tracemalloc` or `memory_profiler` to find the leak
3. **Common causes:** Unbounded caches, connection pool exhaustion, large request/response buffering, accumulating background tasks
4. **Immediate fix:** Increase container memory limits
5. **Long-term fix:** Fix the leak, implement memory limits per worker, set `max_requests` for worker recycling

```python
import tracemalloc

@app.on_event("startup")
async def start_tracing():
    tracemalloc.start()

@app.get("/debug/memory")
async def memory_debug():
    current, peak = tracemalloc.get_traced_memory()
    return {"current_mb": current / 1024 / 1024, "peak_mb": peak / 1024 / 1024}
```

### Q43: You need to deploy FastAPI with PostgreSQL, Redis, and a Celery worker. Design the complete deployment.
**Answer:** Use Kubernetes with separate Deployments for API, worker, and PostgreSQL. Redis as a managed service or Deployment. Use Services for internal communication. Configure HPA for API and worker based on CPU/queue depth. Use PVCs for PostgreSQL persistent storage. Configure network policies for security.

### Q44: How do you handle database migrations in a Kubernetes deployment?
**Answer:** Use an init container or Kubernetes Job for migrations:

```yaml
initContainers:
- name: migrate
  image: myapp:latest
  command: ["alembic", "upgrade", "head"]
  env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: db-secrets
        key: url
```

Run migrations before the application starts. Use expand-contract pattern for zero-downtime schema changes.

### Q45: How do you implement blue-green deployments for FastAPI?
**Answer:** Deploy new version alongside old version. Switch traffic at load balancer level once new version is healthy. Keep old version running for quick rollback. Use separate Services or Ingress rules for blue/green.

### Q46: How do you optimize FastAPI startup time for serverless environments?
**Answer:** Lazy-load heavy dependencies, minimize imports at module level, use connection pooling with warm-up, reduce package size (remove unused deps), use ARM64 architecture for Lambda, and consider Provisioned Concurrency to eliminate cold starts entirely.

### Q47: How do you implement disaster recovery for a FastAPI application?
**Answer:**
- Multi-AZ deployment for database
- Regular database backups (automated + manual)
- Cross-region replication for critical data
- Infrastructure as Code (Terraform/Pulumi) for reproducible deployments
- Runbook for failover procedures
- Regular DR testing (quarterly)

### Q48: How do you handle SSL/TLS termination for FastAPI?
**Answer:** Terminate TLS at the load balancer or Nginx level, not at the application level. Use Let's Encrypt for certificates with auto-renewal. Configure HSTS headers. Redirect HTTP to HTTPS. Use cert-manager in Kubernetes for automatic certificate management.

```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /etc/ssl/certs/app.crt;
    ssl_certificate_key /etc/ssl/private/app.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    add_header Strict-Transport-Security "max-age=63072000" always;

    location / {
        proxy_pass http://fastapi_backend;
    }
}
```

### Q49: How do you implement feature flags in a FastAPI deployment?
**Answer:** Use a feature flag service (LaunchDarkly, Unleash) or implement with Redis:

```python
class FeatureFlags:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def is_enabled(self, flag: str, default: bool = False) -> bool:
        value = await self.redis.get(f"feature:{flag}")
        if value is None:
            return default
        return value.decode().lower() == "true"

    async def get_variant(self, flag: str, user_id: str, variants: list[str]) -> str:
        variant = await self.redis.get(f"feature:{flag}:{user_id}")
        if variant:
            return variant.decode()
        # Deterministic assignment based on user_id
        idx = hash(f"{user_id}:{flag}") % len(variants)
        return variants[idx]

@app.get("/api/feature")
async def check_feature(feature: str, user: User = Depends(get_current_user)):
    enabled = await flags.is_enabled(feature)
    return {"feature": feature, "enabled": enabled}
```

### Q50: Design a complete production deployment checklist for FastAPI.
**Answer:**
- [ ] Docker multi-stage build with non-root user
- [ ] Health check endpoints (liveness, readiness, startup)
- [ ] Graceful shutdown handling
- [ ] Structured logging with correlation IDs
- [ ] Error tracking (Sentry)
- [ ] Metrics endpoint (Prometheus)
- [ ] Rate limiting (Nginx + application)
- [ ] CORS configured with specific origins
- [ ] Security headers (HSTS, CSP, X-Frame-Options)
- [ ] Database connection pooling configured
- [ ] Redis connection pooling
- [ ] Background task queue with workers
- [ ] TLS termination at load balancer
- [ ] Kubernetes HPA configured
- [ ] PDB (Pod Disruption Budget) for zero-downtime maintenance
- [ ] Network policies for service isolation
- [ ] Secret management (not env vars)
- [ ] CI/CD pipeline with tests
- [ ] Canary/blue-green deployment strategy
- [ ] Disaster recovery plan
- [ ] SLO defined and monitored
- [ ] Runbook for common issues
