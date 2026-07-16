# FastAPI Production Checklist

## Table of Contents
1. Gunicorn + Uvicorn Configuration
2. Worker Count
3. Keep-Alive Settings
4. Graceful Shutdown
5. SIGTERM Handling
6. Health Check Endpoints
7. Database Pool Settings
8. Logging Configuration
9. Error Tracking with Sentry
10. Monitoring Setup
11. Complete Production Checklist

---

## 1. Gunicorn + Uvicorn Configuration <a name="gunicorn-uvicorn"></a>

Gunicorn manages multiple Uvicorn worker processes. This is the recommended production setup.

### gunicorn.conf.py

```python
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 120
keepalive = 5
graceful_timeout = 30

# Worker recycling (prevent memory leaks)
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("LOG_LEVEL", "info")

# Preloading (load app before forking workers — saves memory)
preload_app = True

# Process naming
proc_name = "fastapi-app"
```

### CMD in Dockerfile

```dockerfile
CMD ["gunicorn", "app.main:app", "-c", "gunicorn.conf.py"]
```

### Direct Uvicorn (simpler, single-process alternative)

```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--loop", "uvloop", "--http", "httptools", "--log-level", "info"]
```

---

## 2. Worker Count <a name="worker-count"></a>

### Formula

```
CPU-bound: workers = CPU_COUNT * 2 + 1
I/O-bound (FastAPI typical): workers = CPU_COUNT * 4 + 1

Example for 4 CPU server:
  CPU-bound: 4 * 2 + 1 = 9 workers
  I/O-bound: 4 * 4 + 1 = 17 workers
```

### Memory Considerations

```
Each Uvicorn worker uses approximately:
  - Base Python: ~30MB
  - FastAPI + deps: ~50MB
  - Per-request memory: varies
  - Total per worker: ~100-200MB

Example: 4 CPU, 8GB RAM server
  Available for workers: ~6GB (leave 2GB for OS)
  Max workers: 6000MB / 150MB = 40 workers
  Recommended: 17-25 workers
```

### Auto-Detection

```python
import multiprocessing
import os

def get_workers():
    if workers_env := os.environ.get("GUNICORN_WORKERS"):
        return int(workers_env)
    cpu_count = multiprocessing.cpu_count()
    if os.environ.get("WORKER_MODE") == "io":
        return cpu_count * 4 + 1
    return cpu_count * 2 + 1

workers = get_workers()
```

---

## 3. Keep-Alive Settings <a name="keep-alive"></a>

Keep-alive reuses TCP connections between Nginx and Uvicorn/Gunicorn.

```python
# gunicorn.conf.py
keepalive = 5
```

```nginx
# nginx.conf
upstream fastapi_backend {
    server 127.0.0.1:8000;
    keepalive 32;
    keepalive_requests 1000;
    keepalive_timeout 60s;
}
```

---

## 4. Graceful Shutdown <a name="graceful-shutdown"></a>

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.db_pool = await create_db_pool()
    app.state.redis = create_redis_client()
    print("Application started")
    yield
    # Shutdown
    await app.state.db_pool.close()
    await app.state.redis.close()
    print("Shutdown complete")

app = FastAPI(title="My API", lifespan=lifespan)
```

### Gunicorn Hooks

```python
# gunicorn.conf.py
def on_starting(server):
    print("Master process starting...")

def post_fork(server, worker):
    print(f"Worker {worker.pid} spawned.")

def worker_exit(server, worker):
    print(f"Worker {worker.pid} exiting.")

def on_exit(server):
    print("Master process exiting.")
```

---

## 5. SIGTERM Handling <a name="sigterm"></a>

```python
import signal
import asyncio
from fastapi import FastAPI

class GracefulShutdown:
    def __init__(self):
        self.shutdown_event = asyncio.Event()
        self.active_requests = 0

    def handle_signal(self, signum, frame):
        print(f"Received signal {signum}")
        self.shutdown_event.set()

shutdown_manager = GracefulShutdown()

@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            sig, shutdown_manager.handle_signal, sig, None
        )
    yield
    print("Graceful shutdown complete")

app = FastAPI(lifespan=lifespan)
```

### Docker STOPSIGNAL

```dockerfile
STOPSIGNAL SIGTERM
# Send SIGTERM first, then SIGKILL after 30s (configurable)
# docker stop --time=30 <container>
```

---

## 6. Health Check Endpoints <a name="health-checks"></a>

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import time

app = FastAPI()
start_time = time.time()

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/health/live")
async def liveness():
    return {"status": "alive"}

@app.get("/health/ready")
async def readiness():
    checks = {}
    try:
        async with db_pool.acquire():
            await db_pool.execute("SELECT 1")
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"

    try:
        await redis.ping()
        checks["redis"] = "healthy"
    except Exception as e:
        checks["redis"] = f"unhealthy: {str(e)}"

    all_healthy = all(v == "healthy" for v in checks.values())
    return JSONResponse(
        status_code=200 if all_healthy else 503,
        content={"status": "healthy" if all_healthy else "unhealthy", "checks": checks}
    )

@app.get("/health/info")
async def info():
    return {
        "version": "1.2.0",
        "uptime": time.time() - start_time,
        "environment": os.environ.get("ENVIRONMENT", "development"),
    }
```

---

## 7. Database Pool Settings <a name="db-pool"></a>

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

engine = create_async_engine(
    DATABASE_URL,
    pool_size=5,           # Persistent connections
    max_overflow=10,        # Extra connections beyond pool_size
    pool_timeout=30,        # Seconds to wait for a connection
    pool_recycle=1800,      # Recycle connections after 30 minutes
    pool_pre_ping=True,     # Test connections before use
    echo=False,             # Set True for SQL logging in dev
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

### Connection Pool Tuning

```
pool_size: 5-20 (default 5)
  - Each connection uses ~10MB memory
  - More connections = more concurrent DB operations

max_overflow: 10-30
  - Temporary connections beyond pool_size
  - Use for traffic spikes

pool_recycle: 1800-3600
  - Recycle connections to avoid stale connections
  - Match your DB timeout settings

pool_pre_ping: True
  - Tests connections before use
  - Prevents "server closed the connection" errors
```

---

## 8. Logging Configuration <a name="logging"></a>

```python
import logging
import sys
import json
from datetime import datetime, timezone

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        return json.dumps(log_data)

def setup_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    root_logger.handlers = [handler]

    # Reduce noise from libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

setup_logging()
```

### Structured Logging with structlog

```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.BoundLogger,
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(request_id=request_id)
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logger.info("request_completed", method=request.method, path=request.url.path, status=response.status_code, duration=round(duration, 4))
    return response
```

---

## 9. Error Tracking with Sentry <a name="sentry"></a>

### Setup

```python
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=os.environ.get("ENVIRONMENT", "production"),
    release="1.2.0",
    traces_sample_rate=0.1,       # 10% of transactions
    profiles_sample_rate=0.1,     # 10% of profiles
    integrations=[
        SqlalchemyIntegration(),
        RedisIntegration(),
    ],
    before_send=before_send_filter,
    before_send_transaction=before_send_transaction,
)

def before_send(event, hint):
    """Filter or modify events before sending to Sentry."""
    if hint exc_info:
        exc_type = hint["exc_info"][0]
        if exc_type is SystemExit:
            return None  # Don't send SystemExit
    return event

app = FastAPI()
app.add_middleware(SentryAsgiMiddleware)
```

### Custom Error Handler

```python
from fastapi import Request
from fastapi.responses import JSONResponse
import sentry_sdk

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    sentry_sdk.capture_exception(exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
```

### Sentry with Docker

```yaml
environment:
  - SENTRY_DSN=https://xxx@sentry.io/xxx
  - SENTRY_TRACES_SAMPLE_RATE=0.1
  - ENVIRONMENT=production
  - RELEASE=1.2.0
```

---

## 10. Monitoring Setup <a name="monitoring"></a>

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Request, Response

REQUEST_COUNT = Counter(
    "fastapi_requests_total",
    "Total requests",
    ["method", "endpoint", "status_code"]
)

REQUEST_LATENCY = Histogram(
    "fastapi_request_duration_seconds",
    "Request latency",
    ["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

ACTIVE_REQUESTS = Gauge(
    "fastapi_active_requests",
    "Number of active requests"
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    ACTIVE_REQUESTS.inc()
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    ACTIVE_REQUESTS.dec()
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code
    ).inc()
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    return response

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type="text/plain")
```

### Structured Logging for Log Aggregation

```python
# Write logs to stdout for Docker/K8s log collection
# Use JSON format for easy parsing by ELK/Datadog/etc.
import structlog
import logging

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.BoundLogger,
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()
```

### Distributed Tracing

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Initialize tracer
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://jaeger:4317"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

@app.get("/api/data")
async def get_data():
    with tracer.start_as_current_span("fetch_data") as span:
        span.set_attribute("user.id", "123")
        data = await fetch_from_db()
        span.add_event("data_fetched", {"count": len(data)})
        return data
```

---

## 11. Complete Production Checklist <a name="checklist"></a>

### Application Configuration
- [ ] Use environment variables for all configuration
- [ ] Validate settings with Pydantic BaseSettings
- [ ] Never hardcode secrets or API keys
- [ ] Set DEBUG=false in production
- [ ] Configure proper CORS origins
- [ ] Set appropriate rate limits

### Server Configuration
- [ ] Use Gunicorn + UvicornWorker for production
- [ ] Set worker count based on CPU and memory
- [ ] Configure keepalive connections
- [ ] Set proper timeouts (timeout, graceful_timeout, keepalive)
- [ ] Enable worker recycling (max_requests)
- [ ] Configure request size limits

### Health Checks
- [ ] Implement /health/live endpoint (liveness)
- [ ] Implement /health/ready endpoint (readiness)
- [ ] Check database connectivity in readiness
- [ ] Check Redis connectivity in readiness
- [ ] Include version and uptime info

### Database
- [ ] Configure connection pooling
- [ ] Set pool_pre_ping=True
- [ ] Configure pool_recycle
- [ ] Use async drivers (asyncpg, aiomysql)
- [ ] Run migrations before deployment
- [ ] Enable query logging in development only

### Security
- [ ] Use HTTPS everywhere
- [ ] Set security headers (HSTS, CSP, X-Frame-Options)
- [ ] Implement rate limiting
- [ ] Validate all input with Pydantic
- [ ] Use parameterized queries (SQLAlchemy does this)
- [ ] Never expose stack traces in production
- [ ] Run containers as non-root user
- [ ] Scan Docker images for vulnerabilities

### Logging
- [ ] Use structured JSON logging
- [ ] Include request_id in all logs
- [ ] Set appropriate log levels
- [ ] Never log sensitive data (passwords, tokens)
- [ ] Log request/response for debugging

### Monitoring
- [ ] Export Prometheus metrics
- [ ] Track request count, latency, and errors
- [ ] Set up Grafana dashboards
- [ ] Configure alerting rules
- [ ] Set up error tracking (Sentry)
- [ ] Implement distributed tracing

### Docker
- [ ] Use multi-stage builds
- [ ] Use specific base image tags (not latest)
- [ ] Add health checks
- [ ] Run as non-root user
- [ ] Use .dockerignore
- [ ] Minimize image layers
- [ ] Scan for vulnerabilities

### Deployment
- [ ] Use rolling updates (zero downtime)
- [ ] Configure resource limits
- [ ] Set up auto-scaling
- [ ] Test rollback procedures
- [ ] Use blue-green or canary deployments for major changes
- [ ] Monitor deployment metrics
