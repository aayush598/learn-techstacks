# Connection Pooling

## Table of Contents

1. [Introduction](#1-introduction)
2. [SQLAlchemy Pool Configuration](#2-sqlalchemy)
3. [asyncpg Connection Pool](#3-asyncpg)
4. [Pool Sizing Formula](#4-sizing)
5. [Redis Connection Pool](#5-redis)
6. [HTTP Connection Pool (httpx)](#6-httpx)
7. [Connection Pool Monitoring](#7-monitoring)
8. [Best Practices](#8-best-practices)

---

## 1. Introduction <a name="1-introduction"></a>

Connection pooling reuses database connections instead of creating new ones for
each request. This dramatically reduces overhead and improves performance.

### Why Connection Pooling?

- **Reduced Latency**: No connection setup overhead per request
- **Resource Management**: Limit total connections to database
- **Load Balancing**: Distribute connections across pool
- **Health Monitoring**: Detect and replace broken connections
- **Memory Efficiency**: Share connections across requests

### Connection Overhead

```
Without pooling (per request):
TCP handshake:     ~1ms
SSL handshake:     ~5ms (if TLS)
Authentication:    ~2ms
Query execution:   ~1ms
Total:             ~9ms overhead

With pooling:
Connection reuse:  ~0ms
Query execution:   ~1ms
Total:             ~1ms overhead
```

---

## 2. SQLAlchemy Pool Configuration <a name="2-sqlalchemy"></a>

### Sync Connection Pool

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool, NullPool, StaticPool

# Production: QueuePool (default)
engine = create_engine(
    "postgresql://user:pass@localhost/db",
    poolclass=QueuePool,
    pool_size=20,           # Max persistent connections
    max_overflow=10,        # Extra connections beyond pool_size
    pool_timeout=30,        # Seconds to wait for a connection
    pool_recycle=1800,      # Recycle connections after 30 minutes
    pool_pre_ping=True,     # Verify connections before use
    pool_use_lifo=True,     # Use last-in-first-out (better caching)
    echo=False,             # Don't log SQL
)

# Development: NullPool (no pooling)
engine = create_engine(
    "sqlite:///./dev.db",
    poolclass=NullPool,
)

# Testing: StaticPool (single connection)
from sqlalchemy.pool import StaticPool
engine = create_engine(
    "sqlite://",
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)
```

### Async Connection Pool

```python
from sqlalchemy.ext.asyncio import create_async_engine

# Async engine with pool configuration
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)

# Using context manager
async with engine.connect() as conn:
    result = await conn.execute(query)
```

### Pool Configuration Best Practices

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
import os

def get_database_engine():
    """Create engine with production-ready pool configuration."""
    database_url = os.environ["DATABASE_URL"]

    # Calculate pool size based on CPU cores
    import multiprocessing
    cpu_count = multiprocessing.cpu_count()
    pool_size = min(cpu_count * 2 + 1, 20)

    engine = create_engine(
        database_url,
        poolclass=QueuePool,
        pool_size=pool_size,
        max_overflow=pool_size // 2,
        pool_timeout=30,
        pool_recycle=3600,  # 1 hour
        pool_pre_ping=True,
        pool_use_lifo=True,
        echo=os.getenv("SQL_ECHO", "false").lower() == "true",
    )

    return engine
```

---

## 3. asyncpg Connection Pool <a name="3-asyncpg"></a>

### Basic asyncpg Pool

```python
import asyncpg

# Create pool
pool = await asyncpg.create_pool(
    "postgresql://user:pass@localhost/db",
    min_size=5,
    max_size=20,
    timeout=30,
    command_timeout=60,
    max_inactive_connection_lifetime=300,
)

# Using the pool
async with pool.acquire() as conn:
    result = await conn.fetch("SELECT * FROM users")
    return [dict(row) for row in result]

# With transaction
async with pool.acquire() as conn:
    async with conn.transaction():
        await conn.execute(
            "INSERT INTO users (name, email) VALUES ($1, $2)",
            "Alice", "alice@example.com",
        )
```

### FastAPI with asyncpg

```python
from fastapi import FastAPI
import asyncpg

app = FastAPI()

# Global pool
pool: asyncpg.Pool = None

@app.on_event("startup")
async def startup():
    global pool
    pool = await asyncpg.create_pool(
        "postgresql://user:pass@localhost/db",
        min_size=5,
        max_size=20,
    )

@app.on_event("shutdown")
async def shutdown():
    global pool
    if pool:
        await pool.close()

@app.get("/users/")
async def list_users():
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM users")
        return [dict(row) for row in rows]

@app.post("/users/")
async def create_user(name: str, email: str):
    async with pool.acquire() as conn:
        async with conn.transaction():
            row = await conn.fetchrow(
                "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *",
                name, email,
            )
            return dict(row)
```

### Connection Pool with Health Check

```python
class DatabasePool:
    def __init__(self, dsn: str, **kwargs):
        self.dsn = dsn
        self.pool = None
        self.kwargs = kwargs

    async def initialize(self):
        self.pool = await asyncpg.create_pool(
            self.dsn,
            min_size=self.kwargs.get("min_size", 5),
            max_size=self.kwargs.get("max_size", 20),
            timeout=self.kwargs.get("timeout", 30),
            command_timeout=self.kwargs.get("command_timeout", 60),
        )

    async def close(self):
        if self.pool:
            await self.pool.close()

    async def health_check(self) -> bool:
        try:
            async with self.pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            return True
        except Exception:
            return False

    async def get_pool_stats(self) -> dict:
        return {
            "size": self.pool.get_size(),
            "free_size": self.pool.get_idle_size(),
            "min_size": self.pool.get_min_size(),
            "max_size": self.pool.get_max_size(),
        }
```

---

## 4. Pool Sizing Formula <a name="4-sizing"></a>

### Formula

```
Pool Size = (Number of CPU cores × 2) + Number of Disk Spindles

For web applications:
Pool Size = (CPU cores × 2) + 1

For database servers:
Pool Size = CPU cores × 2 + effective_spindle_count
```

### Practical Examples

```python
import multiprocessing

# Web server with 8 cores
cpu_count = multiprocessing.cpu_count()  # 8
web_pool_size = (cpu_count * 2) + 1  # 17
web_max_overflow = web_pool_size // 2  # 8

# Database server with 4 cores
db_pool_size = (4 * 2) + 1  # 9

# Shared database for multiple services
# Each service gets: total_pool / num_services
total_pool = 50
num_services = 4
per_service_pool = total_pool // num_services  # 12
```

### Environment-Based Configuration

```python
import os

def get_pool_config():
    environment = os.getenv("ENVIRONMENT", "development")

    configs = {
        "development": {
            "pool_size": 5,
            "max_overflow": 2,
            "pool_timeout": 30,
            "pool_recycle": 300,
        },
        "staging": {
            "pool_size": 10,
            "max_overflow": 5,
            "pool_timeout": 30,
            "pool_recycle": 1800,
        },
        "production": {
            "pool_size": 20,
            "max_overflow": 10,
            "pool_timeout": 30,
            "pool_recycle": 3600,
        },
    }

    return configs.get(environment, configs["development"])
```

### Monitoring Pool Usage

```python
from sqlalchemy import event

@event.listens_for(engine, "checkout")
def on_checkout(dbapi_conn, connection_rec, connection_proxy):
    """Log connection checkout."""
    logger.debug(f"Connection checked out: {id(dbapi_conn)}")

@event.listens_for(engine, "checkin")
def on_checkin(dbapi_conn, connection_rec):
    """Log connection checkin."""
    logger.debug(f"Connection checked in: {id(dbapi_conn)}")

@event.listens_for(engine, "connect")
def on_connect(dbapi_conn, connection_record):
    """Log new connection creation."""
    logger.info(f"New connection created: {id(dbapi_conn)}")

def get_pool_status(engine):
    """Get pool status information."""
    pool = engine.pool
    return {
        "size": pool.size(),
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
    }
```

---

## 5. Redis Connection Pool <a name="5-redis"></a>

### Basic Redis Pool

```python
import redis
from redis.connection import ConnectionPool

# Create connection pool
pool = ConnectionPool(
    host="localhost",
    port=6379,
    db=0,
    password="",
    max_connections=20,
    socket_timeout=5,
    socket_connect_timeout=5,
    retry_on_timeout=True,
    decode_responses=True,
)

# Create client with pool
r = redis.Redis(connection_pool=pool)

# Use client
r.set("key", "value")
value = r.get("key")
```

### Redis Sentinel Pool (High Availability)

```python
from redis.sentinel import Sentinel

sentinel = Sentinel(
    [("sentinel-1", 26379), ("sentinel-2", 26379)],
    socket_timeout=0.5,
)

# Get master for writes
master = sentinel.master_for("mymaster", socket_timeout=0.5)

# Get slave for reads
slave = sentinel.slave_for("mymaster", socket_timeout=0.5)

# Use
master.set("key", "value")
value = slave.get("key")
```

### FastAPI Redis Pool

```python
import redis.asyncio as aioredis
from fastapi import FastAPI

app = FastAPI()

# Redis pool
redis_pool = None

@app.on_event("startup")
async def startup():
    global redis_pool
    redis_pool = aioredis.ConnectionPool.from_url(
        "redis://localhost:6379",
        max_connections=20,
        decode_responses=True,
    )

@app.on_event("shutdown")
async def shutdown():
    global redis_pool
    if redis_pool:
        await redis_pool.aclose()

@app.get("/cache/{key}")
async def get_cached(key: str):
    r = aioredis.Redis(connection_pool=redis_pool)
    value = await r.get(key)
    return {"value": value}

@app.set("/cache/{key}")
async def set_cached(key: str, value: str):
    r = aioredis.Redis(connection_pool=redis_pool)
    await r.setex(key, 300, value)
    return {"detail": "Set"}
```

---

## 6. HTTP Connection Pool (httpx) <a name="6-httpx"></a`

### httpx Connection Pool

```python
import httpx

# Create client with connection pool
client = httpx.AsyncClient(
    limits=httpx.Limits(
        max_connections=100,       # Total connections
        max_keepalive_connections=20,  # Keep-alive connections
        keepalive_expiry=30,       # Seconds to keep alive
    ),
    timeout=httpx.Timeout(
        connect=5.0,
        read=30.0,
        write=10.0,
        pool=5.0,
    ),
)

# Using the client
async def fetch_data():
    async with client:
        response = await client.get("https://api.example.com/data")
        return response.json()
```

### Persistent Client in FastAPI

```python
from fastapi import FastAPI
import httpx

app = FastAPI()
http_client: httpx.AsyncClient = None

@app.on_event("startup")
async def startup():
    global http_client
    http_client = httpx.AsyncClient(
        limits=httpx.Limits(
            max_connections=100,
            max_keepalive_connections=20,
            keepalive_expiry=30,
        ),
        timeout=httpx.Timeout(30.0),
    )

@app.on_event("shutdown")
async def shutdown():
    global http_client
    if http_client:
        await http_client.aclose()

@app.get("/proxy/{path:path}")
async def proxy(path: str):
    response = await http_client.get(f"https://api.example.com/{path}")
    return response.json()
```

---

## 7. Connection Pool Monitoring <a name="7-monitoring"></a>

### Metrics Collection

```python
from prometheus_client import Gauge, Counter, Histogram
import time

# Prometheus metrics
db_pool_size = Gauge("db_pool_size", "Database pool size")
db_pool_checked_out = Gauge("db_pool_checked_out", "Connections checked out")
db_pool_waiting = Gauge("db_pool_waiting", "Waiting for connection")
db_pool_timeout = Counter("db_pool_timeout", "Connection timeout count")
db_query_duration = Histogram("db_query_duration_seconds", "Query duration")

def monitor_pool(engine):
    """Update pool metrics periodically."""
    pool = engine.pool

    db_pool_size.set(pool.size())
    db_pool_checked_out.set(pool.checkedout())
    db_pool_waiting.set(pool.checkedin())

# Middleware for query timing
@app.middleware("http")
async def db_timing_middleware(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    db_query_duration.observe(duration)
    return response
```

### Health Check Endpoint

```python
@app.get("/health")
async def health_check():
    db_healthy = await check_database()
    redis_healthy = await check_redis()
    http_healthy = await check_external_services()

    status = {
        "status": "healthy" if all([db_healthy, redis_healthy]) else "degraded",
        "checks": {
            "database": "ok" if db_healthy else "error",
            "redis": "ok" if redis_healthy else "error",
            "external_services": "ok" if http_healthy else "degraded",
        },
        "pool_stats": get_pool_status(engine),
    }

    return JSONResponse(
        status_code=200 if status["status"] == "healthy" else 503,
        content=status,
    )
```

---

## 8. Best Practices <a name="8-best-practices"></a>

### 1. Right-Size Your Pool

```python
# Too small: Connection waiting, timeouts
# Too large: Database overload, memory waste

# Monitor and adjust
def calculate_optimal_pool_size():
    """Calculate pool size based on workload."""
    import multiprocessing
    cpu_cores = multiprocessing.cpu_count()

    # For CPU-bound work
    pool_size = cpu_cores + 1

    # For I/O-bound work (most web apps)
    pool_size = cpu_cores * 2 + 1

    # Limit by database capacity
    max_db_connections = 100
    num_app_instances = 4
    pool_size = min(pool_size, max_db_connections // num_app_instances)

    return pool_size
```

### 2. Enable Connection Recycling

```python
# Recycle connections to avoid stale connections
engine = create_engine(
    DATABASE_URL,
    pool_recycle=3600,  # Recycle every hour
    pool_pre_ping=True,  # Verify connection before use
)
```

### 3. Handle Connection Failures

```python
from sqlalchemy.exc import OperationalError, DBAPIError

def get_db_with_retry(max_retries: int = 3):
    """Get database connection with retry logic."""
    for attempt in range(max_retries):
        try:
            db = SessionLocal()
            # Test connection
            db.execute(text("SELECT 1"))
            return db
        except (OperationalError, DBAPIError) as e:
            logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### 4. Use Connection Timeouts

```python
# Always set timeouts
engine = create_engine(
    DATABASE_URL,
    pool_timeout=30,  # Don't wait forever
    connect_args={
        "connect_timeout": 5,
        "options": "-c statement_timeout=30000",
    },
)
```

### 5. Monitor Pool Health

```python
@app.on_event("startup")
async def monitor_pool_health():
    """Periodically check pool health."""
    while True:
        stats = get_pool_status(engine)

        if stats["checked_out"] > stats["size"] * 0.9:
            logger.warning("Connection pool nearly exhausted")

        if stats["overflow"] > 0:
            logger.info(f"Pool overflow: {stats['overflow']}")

        await asyncio.sleep(60)
```

---

## Summary

| Component | Recommended Pool Size | Key Settings |
|-----------|----------------------|--------------|
| PostgreSQL (asyncpg) | (CPU × 2) + 1 | min_size=5, max_size=20 |
| SQLAlchemy | (CPU × 2) + 1 | pool_pre_ping=True |
| Redis | 20-50 connections | max_connections=20 |
| HTTP (httpx) | 100 connections | keepalive_expiry=30 |

### Key Rules

1. Right-size your pool for your workload
2. Enable connection recycling and pre-ping
3. Set appropriate timeouts
4. Monitor pool health metrics
5. Handle connection failures gracefully
6. Use connection pooling for all external services
