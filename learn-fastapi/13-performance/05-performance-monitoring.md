# Performance Monitoring

## Table of Contents

1. [Introduction](#1-introduction)
2. [Profiling FastAPI](#2-profiling)
3. [cProfile](#3-cprofile)
4. [py-spy](#4-py-spy)
5. [Memory Profiling](#5-memory)
6. [Response Time Monitoring](#6-response-time)
7. [Slow Query Detection](#7-slow-queries)
8. [APM Tools](#8-apm)
9. [Benchmarking](#9-benchmarking)
10. [Best Practices](#10-best-practices)

---

## 1. Introduction <a name="1-introduction"></a>

Performance monitoring is essential for identifying bottlenecks, optimizing response
times, and ensuring your FastAPI application scales effectively.

### What to Monitor

- Response times (p50, p95, p99)
- Request throughput (requests per second)
- Error rates
- Database query performance
- Memory usage
- CPU usage
- Connection pool health
- Cache hit rates

---

## 2. Profiling FastAPI <a name="2-profiling"></a>

### Middleware Profiling

```python
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("performance")

class PerformanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        # Process request
        response = await call_next(request)

        # Calculate duration
        duration = time.perf_counter() - start_time

        # Add timing header
        response.headers["X-Process-Time"] = f"{duration:.4f}"

        # Log slow requests
        if duration > 1.0:
            logger.warning(
                "Slow request",
                method=request.method,
                path=request.url.path,
                duration=duration,
                status_code=response.status_code,
            )

        # Log all requests
        logger.info(
            "Request",
            method=request.method,
            path=request.url.path,
            duration=duration,
            status_code=response.status_code,
        )

        return response

app.add_middleware(PerformanceMiddleware)
```

### Profiling with contextlib

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(operation_name: str):
    """Context manager to time operations."""
    start = time.perf_counter()
    yield
    duration = time.perf_counter() - start
    logger.info(f"{operation_name} took {duration:.4f}s")

# Usage
async def get_user_profile(user_id: int):
    with timer("database_query"):
        user = db.query(User).get(user_id)

    with timer("order_fetch"):
        orders = db.query(Order).filter(Order.user_id == user_id).all()

    return {"user": user, "orders": orders}
```

---

## 3. cProfile <a name="3-cprofile"></a>

### Basic cProfile Usage

```bash
# Profile entire application
python -m cProfile -s cumtime app.py

# Profile specific function
python -m cProfile -s cumulative -m pytest tests/test_performance.py

# Save profile to file
python -m cProfile -o profile.prof app.py

# Analyze saved profile
python -c "
import pstats
stats = pstats.Stats('profile.prof')
stats.sort_stats('cumulative')
stats.print_stats(20)
"
```

### cProfile in Tests

```python
import cProfile
import pstats
from io import StringIO

def profile_endpoint(endpoint_func, *args, **kwargs):
    """Profile a FastAPI endpoint."""
    pr = cProfile.Profile()
    pr.enable()

    result = endpoint_func(*args, **kwargs)

    pr.disable()

    # Print stats
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
    ps.print_stats(20)
    print(s.getvalue())

    return result

# Usage
profile_endpoint(get_items, skip=0, limit=100)
```

### cProfile with pytest

```python
# conftest.py
import cProfile
import pstats
import pytest

@pytest.fixture(autouse=True)
def profile_tests(request):
    """Profile each test."""
    pr = cProfile.Profile()
    pr.enable()

    yield

    pr.disable()

    # Only profile slow tests
    if request.node.rep_call and hasattr(request.node, "duration"):
        if request.node.duration > 1.0:
            s = StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
            ps.print_stats(20)
            print(f"\nProfile for {request.node.name}:")
            print(s.getvalue())
```

---

## 4. py-spy <a name="4-py-spy"></a>

### Installation

```bash
pip install py-spy
```

### Basic Usage

```bash
# Record CPU profile
py-spy record -o profile.svg --duration 30 --pid <PID>

# Top-like view
py-spy top --pid <PID>

# Record from Python script
py-spy record -o profile.svg -- python -m uvicorn app:app

# Record with line numbers
py-spy record -o profile.svg --function --duration 30 -- python app.py
```

### py-spy in Docker

```bash
# Profile container
docker exec -it <container_id> py-spy top

# Record from host
py-spy record -o profile.svg --pid $(docker inspect -f '{{.State.Pid}}' <container>)
```

### Reading py-spy Output

```
%   Cumulative   Self  Self%  Command
50.00    0.05s   0.05s  50.00  get_user_profile
20.00    0.07s   0.02s  20.00  db.query(User).filter
15.00    0.085s  0.015s 15.00  db.query(Order).filter
10.00    0.095s  0.01s  10.00  json.dumps
5.00     0.1s    0.005s 5.00   response.json()
```

---

## 5. Memory Profiling <a name="5-memory"></a>

### memory_profiler

```bash
pip install memory_profiler
```

```python
from memory_profiler import profile

@profile
def memory_intensive_function():
    """Function to profile memory usage."""
    data = [i for i in range(1000000)]
    result = sum(data)
    return result

# Run with: python -m memory_profiler script.py
```

### tracemalloc

```python
import tracemalloc

# Start tracing
tracemalloc.start()

# Your code here
data = [i for i in range(1000000)]

# Take snapshot
snapshot = tracemalloc.take_snapshot()

# Display top memory consumers
top_stats = snapshot.statistics("lineno")

print("[ Top 10 memory consumers ]")
for stat in top_stats[:10]:
    print(stat)
```

### FastAPI Memory Monitoring

```python
import tracemalloc
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.on_event("startup")
async def start_memory_tracking():
    tracemalloc.start()

@app.get("/memory-stats")
async def memory_stats():
    current, peak = tracemalloc.get_traced_memory()
    snapshot = tracemalloc.take_snapshot()

    top_stats = snapshot.statistics("lineno")[:10]

    return {
        "current_memory_mb": current / 1024 / 1024,
        "peak_memory_mb": peak / 1024 / 1024,
        "top_consumers": [
            {"file": str(stat.traceback), "size_kb": stat.size / 1024}
            for stat in top_stats
        ],
    }
```

---

## 6. Response Time Monitoring <a name="6-response-time"></a>

### Detailed Response Time Tracking

```python
import time
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware

class ResponseTimeTracker:
    def __init__(self):
        self.times = defaultdict(list)

    def record(self, path: str, duration: float):
        self.times[path].append(duration)

    def get_stats(self, path: str = None) -> dict:
        if path:
            times = self.times.get(path, [])
            return self._calculate_stats(times)

        return {
            path: self._calculate_stats(times)
            for path, times in self.times.items()
        }

    def _calculate_stats(self, times: list[float]) -> dict:
        if not times:
            return {}

        times_sorted = sorted(times)
        n = len(times_sorted)

        return {
            "count": n,
            "min": times_sorted[0],
            "max": times_sorted[-1],
            "mean": sum(times) / n,
            "p50": times_sorted[n // 2],
            "p95": times_sorted[int(n * 0.95)],
            "p99": times_sorted[int(n * 0.99)],
        }

tracker = ResponseTimeTracker()

class MonitoringMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start

        tracker.record(request.url.path, duration)
        response.headers["X-Response-Time"] = f"{duration:.4f}s"

        return response

app.add_middleware(MonitoringMiddleware)

@app.get("/stats")
async def get_stats():
    return tracker.get_stats()
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge
import time

# Metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

ACTIVE_REQUESTS = Gauge(
    "http_active_requests",
    "Number of active requests",
)

@app.middleware("http")
async def prometheus_middleware(request, call_next):
    ACTIVE_REQUESTS.inc()
    start = time.perf_counter()

    try:
        response = await call_next(request)
        duration = time.perf_counter() - start

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code,
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.url.path,
        ).observe(duration)

        return response
    finally:
        ACTIVE_REQUESTS.dec()
```

---

## 7. Slow Query Detection <a name="7-slow-queries"></a>

### SQLAlchemy Query Logging

```python
import logging
import time
from sqlalchemy import event

# Enable query logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Custom slow query detection
SLOW_QUERY_THRESHOLD = 1.0  # seconds

@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(time.perf_counter())

@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.perf_counter() - conn.info["query_start_time"].pop(-1)

    if total > SLOW_QUERY_THRESHOLD:
        logging.warning(
            "Slow query detected",
            duration=total,
            statement=statement,
            parameters=parameters,
        )
```

### Async Slow Query Detection

```python
from sqlalchemy.ext.asyncio import AsyncEngine
import time

class SlowQueryDetector:
    def __init__(self, engine: AsyncEngine, threshold: float = 1.0):
        self.engine = engine
        self.threshold = threshold

    async def detect_slow_queries(self):
        """Monitor for slow queries."""
        # Implementation depends on database
        pass

# Middleware approach
@app.middleware("http")
async def query_monitoring(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start

    if duration > 2.0:
        logger.warning(
            "Slow endpoint",
            path=request.url.path,
            duration=duration,
        )

    return response
```

---

## 8. APM Tools <a name="8-apm"></a>

### Datadog Integration

```python
# pip install ddtrace
from ddtrace import patch_all
patch_all()

from fastapi import FastAPI

app = FastAPI()

# Datadog automatically instruments FastAPI
# View traces in Datadog dashboard
```

### New Relic Integration

```python
# newrelic.ini
# [newrelic]
# app_name = My FastAPI App
# license_key = your-license-key

# Run with: newrelic-admin run-program uvicorn app:app

import newrelic.agent
newrelic.agent.initialize()

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### OpenTelemetry Integration

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Setup
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    with tracer.start_as_current_span("get_item") as span:
        span.set_attribute("item_id", item_id)

        item = db.query(Item).get(item_id)
        span.set_attribute("item_found", item is not None)

        return item.dict()
```

---

## 9. Benchmarking <a name="9-benchmarking"></a>

### wrk (HTTP Benchmarking)

```bash
# Basic benchmark
wrk -t12 -c400 -d30s http://localhost:8000/

# With Lua script for custom requests
wrk -t12 -c400 -d30s -s scripts/post.lua http://localhost:8000/items/

# Lua script for POST requests
# scripts/post.lua
wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"
wrk.body = '{"name": "Benchmark Item", "price": 10.0}'
```

### hey (HTTP Load Testing)

```bash
# Install
go install github.com/rakyll/hey@latest

# Basic benchmark
hey -n 10000 -c 100 http://localhost:8000/

# With POST request
hey -n 10000 -c 100 -m POST \
    -H "Content-Type: application/json" \
    -d '{"name": "Test"}' \
    http://localhost:8000/items/
```

### Locust (Python-based)

```python
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def view_items(self):
        self.client.get("/items/")

    @task(1)
    def create_item(self):
        self.client.post("/items/", json={
            "name": "Load Test Item",
            "price": 10.0,
        })

    @task(2)
    def view_item(self):
        self.client.get("/items/1")
```

### pytest-benchmark

```python
import pytest

def test_get_items(benchmark, client):
    """Benchmark GET /items/ endpoint."""
    def make_request():
        return client.get("/items/")

    result = benchmark(make_request)
    assert result.status_code == 200

def test_create_item(benchmark, client):
    """Benchmark POST /items/ endpoint."""
    def make_request():
        return client.post("/items/", json={
            "name": "Benchmark Item",
            "price": 10.0,
        })

    result = benchmark(make_request)
    assert result.status_code == 201
```

---

## 10. Best Practices <a name="10-best-practices"></a>

### 1. Monitor Key Metrics

```python
# Always track
METRICS = {
    "response_time": ["p50", "p95", "p99"],
    "throughput": "requests_per_second",
    "error_rate": "percentage",
    "database_queries": "per_request",
    "memory_usage": "mb",
    "cpu_usage": "percentage",
}
```

### 2. Set Performance Budgets

```python
PERFORMANCE_BUDGETS = {
    "api_response_time": 0.5,  # 500ms
    "database_query_time": 0.1,  # 100ms
    "page_load_time": 2.0,  # 2 seconds
    "error_rate": 0.01,  # 1%
}

def check_budget(metric: str, value: float):
    budget = PERFORMANCE_BUDGETS.get(metric)
    if budget and value > budget:
        logger.warning(f"Performance budget exceeded: {metric}={value} > {budget}")
```

### 3. Use Structured Logging

```python
import structlog

logger = structlog.get_logger()

@app.middleware("http")
async def structured_logging(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start

    logger.info(
        "request",
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        duration=duration,
        ip=request.client.host,
    )
    return response
```

### 4. Alert on Anomalies

```python
# Alert if p99 > 2 seconds
# Alert if error rate > 5%
# Alert if throughput drops > 50%
```

### 5. Profile Regularly

```bash
# Profile in CI/CD
pytest --benchmark-compare --benchmark-max-time=10

# Profile in production (sampling)
py-spy record -o profile.svg --duration 30 --pid $(pgrep uvicorn)
```

---

## Summary

| Tool | Purpose | Use Case |
|------|---------|----------|
| cProfile | CPU profiling | Find slow functions |
| py-spy | Sampling profiler | Production profiling |
| memory_profiler | Memory profiling | Find memory leaks |
| tracemalloc | Memory tracking | Detailed memory analysis |
| wrk/hey | Load testing | Benchmark endpoints |
| Locust | Load testing | Complex scenarios |
| Prometheus | Metrics collection | Time-series monitoring |
| Datadog/APM | Full observability | Production monitoring |

### Key Metrics

1. Response time (p50, p95, p99)
2. Throughput (requests/second)
3. Error rate (%)
4. Database query time
5. Memory usage
6. CPU usage
7. Connection pool health
8. Cache hit rate
