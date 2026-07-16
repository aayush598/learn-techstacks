# Health Checks for FastAPI

## Table of Contents
1. [Health Check Endpoints](#endpoints)
2. [Readiness vs Liveness Probes](#probes)
3. [Deep Health Checks](#deep)
4. [Health Check Patterns](#patterns)
5. [Graceful Degradation](#degradation)

---

## Health Check Endpoints <a name="endpoints"></a>

### Basic Health Endpoint

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
    """Is the application alive?"""
    return {"status": "alive"}

@app.get("/health/ready")
async def readiness():
    """Is the application ready to accept traffic?"""
    return {"status": "ready"}

@app.get("/health/info")
async def health_info():
    """Application information."""
    return {
        "version": "1.2.0",
        "uptime": time.time() - start_time,
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "python_version": sys.version,
    }
```

### Health Check with Dependencies

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import asyncpg
import redis.asyncio as redis

app = FastAPI()

class HealthChecker:
    def __init__(self, db_pool, redis_client):
        self.db_pool = db_pool
        self.redis = redis_client

    async def check_database(self) -> dict:
        try:
            async with self.db_pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            return {"status": "healthy", "latency_ms": 0}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    async def check_redis(self) -> dict:
        try:
            start = time.time()
            await self.redis.ping()
            latency = (time.time() - start) * 1000
            return {"status": "healthy", "latency_ms": round(latency, 2)}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    async def check_external_api(self, url: str) -> dict:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                return {"status": "healthy" if response.status_code == 200 else "unhealthy"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

checker = HealthChecker(db_pool, redis_client)

@app.get("/health")
async def health():
    checks = {
        "database": await checker.check_database(),
        "redis": await checker.check_redis(),
    }

    all_healthy = all(c["status"] == "healthy" for c in checks.values())
    status_code = 200 if all_healthy else 503

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "healthy" if all_healthy else "unhealthy",
            "checks": checks,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )
```

---

## Readiness vs Liveness Probes <a name="probes"></a>

### Liveness Probe

```
Purpose: Is the container alive?
Action on failure: Container is restarted
Use cases:
  - Application is stuck (deadlock)
  - Application is in an unrecoverable state
  - Memory leak causing OOM

Implementation:
  - Light check (no external dependencies)
  - Check if main event loop is responsive
  - Don't check database (it might be temporarily down)
```

```python
@app.get("/health/live")
async def liveness():
    """
    Liveness probe: is the process alive and responsive?
    Keep this lightweight — no external dependency checks.
    """
    return {"status": "alive"}
```

### Readiness Probe

```
Purpose: Is the container ready to accept traffic?
Action on failure: Removed from Service endpoints (no traffic)
Use cases:
  - Application is still starting up
  - Database connection not established
  - Required dependencies unavailable
  - Application is overloaded

Implementation:
  - Check all critical dependencies
  - Return 503 if not ready
  - More expensive than liveness
```

```python
@app.get("/health/ready")
async def readiness():
    """
    Readiness probe: is the application ready to handle requests?
    Check all critical dependencies.
    """
    checks = {}

    # Database check
    try:
        async with db_pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        checks["database"] = "ready"
    except Exception:
        checks["database"] = "not_ready"

    # Redis check
    try:
        await redis_client.ping()
        checks["redis"] = "ready"
    except Exception:
        checks["redis"] = "not_ready"

    # Application state check
    if not app.state.initialized:
        checks["app"] = "not_ready"
    else:
        checks["app"] = "ready"

    all_ready = all(v == "ready" for v in checks.values())

    return JSONResponse(
        status_code=200 if all_ready else 503,
        content={
            "status": "ready" if all_ready else "not_ready",
            "checks": checks,
        }
    )
```

### Startup Probe

```
Purpose: Has the container finished starting?
Action on failure: Container is restarted (if startup probe fails)
Use cases:
  - Slow-starting applications
  - Applications with heavy initialization
  - Database migrations at startup

Implementation:
  - More lenient than liveness
  - Higher failure threshold
  - Disabled once it passes
```

```python
@app.get("/health/startup")
async def startup():
    """
    Startup probe: has initialization completed?
    More lenient than other probes.
    """
    if not app.state.startup_complete:
        return JSONResponse(
            status_code=503,
            content={"status": "starting"}
        )
    return {"status": "started"}
```

### Kubernetes Probe Configuration

```yaml
containers:
  - name: fastapi
    startupProbe:
      httpGet:
        path: /health/startup
        port: 8000
      initialDelaySeconds: 5
      periodSeconds: 5
      failureThreshold: 30  # 150s max startup

    livenessProbe:
      httpGet:
        path: /health/live
        port: 8000
      periodSeconds: 15
      timeoutSeconds: 5
      failureThreshold: 3

    readinessProbe:
      httpGet:
        path: /health/ready
        port: 8000
      periodSeconds: 10
      timeoutSeconds: 5
      failureThreshold: 3
```

---

## Deep Health Checks <a name="deep"></a>

### Database Health

```python
class DatabaseHealth:
    def __init__(self, engine):
        self.engine = engine

    async def check(self) -> dict:
        checks = {}

        # Connection pool status
        pool = self.engine.pool
        checks["pool"] = {
            "size": pool.size(),
            "checked_in": pool.checkedin(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow(),
        }

        # Query execution
        try:
            start = time.time()
            async with self.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            checks["query"] = {
                "status": "healthy",
                "latency_ms": round((time.time() - start) * 1000, 2),
            }
        except Exception as e:
            checks["query"] = {"status": "unhealthy", "error": str(e)}

        # Replication lag (for read replicas)
        try:
            async with self.engine.connect() as conn:
                result = await conn.execute(
                    text("SHOW slave_status")
                )
                row = result.fetchone()
                if row:
                    checks["replication_lag"] = row Seconds_Behind_Master
        except Exception:
            pass

        return checks
```

### Redis Health

```python
class RedisHealth:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def check(self) -> dict:
        checks = {}

        # Ping
        try:
            start = time.time()
            await self.redis.ping()
            checks["ping"] = {
                "status": "healthy",
                "latency_ms": round((time.time() - start) * 1000, 2),
            }
        except Exception as e:
            checks["ping"] = {"status": "unhealthy", "error": str(e)}

        # Memory usage
        try:
            info = await self.redis.info("memory")
            checks["memory"] = {
                "used_bytes": info["used_memory"],
                "max_bytes": info.get("maxmemory", 0),
                "fragmentation_ratio": info.get("mem_fragmentation_ratio", 0),
            }
        except Exception:
            pass

        # Connection count
        try:
            info = await self.redis.info("clients")
            checks["connections"] = {
                "connected": info["connected_clients"],
                "blocked": info.get("blocked_clients", 0),
            }
        except Exception:
            pass

        return checks
```

### External Service Health

```python
class ExternalServiceHealth:
    def __init__(self):
        self.services = {
            "payment_api": "https://api.stripe.com/health",
            "email_service": "https://api.sendgrid.com/v3/health",
            "search_api": "http://elasticsearch:9200/_cluster/health",
        }

    async def check_all(self) -> dict:
        checks = {}
        for name, url in self.services.items():
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    start = time.time()
                    response = await client.get(url)
                    latency = (time.time() - start) * 1000

                    checks[name] = {
                        "status": "healthy" if response.status_code < 500 else "unhealthy",
                        "status_code": response.status_code,
                        "latency_ms": round(latency, 2),
                    }
            except httpx.TimeoutException:
                checks[name] = {"status": "unhealthy", "error": "timeout"}
            except Exception as e:
                checks[name] = {"status": "unhealthy", "error": str(e)}

        return checks
```

### Comprehensive Health Endpoint

```python
@app.get("/health")
async def comprehensive_health():
    start = time.time()

    db_health = await DatabaseHealth(db_engine).check()
    redis_health = await RedisHealth(redis_client).check()
    external_health = await ExternalServiceHealth().check_all()

    all_checks = {**db_health, **redis_health, **external_health}

    # Determine overall status
    statuses = [
        check.get("status", "unknown")
        for check in all_checks.values()
        if isinstance(check, dict)
    ]

    if all(s == "healthy" for s in statuses):
        overall = "healthy"
        status_code = 200
    elif any(s == "unhealthy" for s in statuses):
        overall = "unhealthy"
        status_code = 503
    else:
        overall = "degraded"
        status_code = 200

    return JSONResponse(
        status_code=status_code,
        content={
            "status": overall,
            "checks": all_checks,
            "duration_ms": round((time.time() - start) * 1000, 2),
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.2.0",
            "uptime": time.time() - app.state.start_time,
        }
    )
```

---

## Health Check Patterns <a name="patterns"></a>

### Sidecar Pattern

```
Main App (port 8000)
  └── Health Sidecar (port 8080)
        - Monitors main app
        - Reports to orchestrator
        - Independent of main app
```

### Push vs Pull

```
Pull (Prometheus, Kubernetes):
  - Orchestrator/monitoring system pulls health endpoint
  - Application doesn't need to know about monitoring

Push (Pushgateway, Webhooks):
  - Application pushes health status to monitoring
  - Useful when app can't expose endpoints
```

### Circuit Breaker Integration

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = "closed"  # closed, open, half-open
        self.last_failure_time = None

    async def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is open")

        try:
            result = await func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            raise

# Use in health check
payment_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=30)

@app.get("/health")
async def health():
    checks = {}

    # Database
    checks["database"] = await check_database()

    # Payment service (with circuit breaker)
    try:
        await payment_breaker.call(check_payment_service)
        checks["payment"] = {"status": "healthy"}
    except Exception:
        checks["payment"] = {"status": "unhealthy", "circuit": payment_breaker.state}

    return checks
```

---

## Graceful Degradation <a name="degradation"></a>

```python
@app.get("/api/recommendations")
async def get_recommendations(user_id: int):
    # Primary: personalized recommendations
    try:
        recs = await recommendation_service.get_personalized(user_id)
        return {"recommendations": recs, "source": "personalized"}
    except Exception:
        pass

    # Fallback: popular items
    try:
        recs = await recommendation_service.get_popular()
        return {"recommendations": recs, "source": "popular"}
    except Exception:
        pass

    # Fallback: static recommendations
    return {
        "recommendations": DEFAULT_RECOMMENDATIONS,
        "source": "default",
        "degraded": True,
    }

@app.get("/api/products/{product_id}")
async def get_product(product_id: int):
    # Try cache first
    cached = await cache.get(f"product:{product_id}")
    if cached:
        return {"product": cached, "source": "cache"}

    try:
        product = await db.get_product(product_id)
        await cache.set(f"product:{product_id}", product, ttl=300)
        return {"product": product, "source": "database"}
    except Exception:
        # Serve from cache even if stale
        stale = await cache.get(f"product:{product_id}", allow_stale=True)
        if stale:
            return {"product": stale, "source": "stale_cache", "degraded": True}
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
```

### Readiness with Degradation

```python
@app.get("/health/ready")
async def readiness():
    checks = {}
    degraded = False

    # Database (critical)
    try:
        async with db_pool.acquire():
            await db_pool.execute("SELECT 1")
        checks["database"] = "ready"
    except Exception:
        checks["database"] = "not_ready"
        # Database is critical — return 503
        return JSONResponse(status_code=503, content={"status": "not_ready", "checks": checks})

    # Redis (degradable)
    try:
        await redis_client.ping()
        checks["redis"] = "ready"
    except Exception:
        checks["redis"] = "degraded"
        degraded = True

    # Search (degradable)
    try:
        await search_client.ping()
        checks["search"] = "ready"
    except Exception:
        checks["search"] = "degraded"
        degraded = True

    status_code = 200 if not degraded else 200  # Still accept traffic
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "ready" if not degraded else "degraded",
            "checks": checks,
        }
    )
```

---

## Interview Questions

1. **What is the difference between a liveness probe and a readiness probe?**
Liveness: Is the container alive? Failure triggers restart. Use for unrecoverable states (deadlock, crash loop). Readiness: Is the container ready for traffic? Failure removes from Service endpoints. Use for temporary issues (DB down, starting up).

2. **What should a health check endpoint verify?**
Liveness: Keep it lightweight — just check the process is responsive. Readiness: Check all critical dependencies (database, Redis, external APIs). Include connection pool status, query latency, and application state. Don't check non-critical services in readiness.

3. **How do you implement graceful degradation?**
Implement fallback mechanisms: cache → database → static data. Return cached data when the database is unavailable. Serve default recommendations when personalized ones fail. Always indicate degraded state in response headers or fields.

4. **What is a circuit breaker and how does it relate to health checks?**
A circuit breaker tracks failures and "opens" after a threshold, preventing further calls to a failing service. After a recovery timeout, it goes to "half-open" to test if the service recovered. Integrate with health checks to report circuit state.

5. **How do you handle health checks in a microservices architecture?**
Each service has its own health endpoints. Use deep health checks (verify all dependencies). Set up synthetic monitoring (continuously test health endpoints). Aggregate health status across services. Use circuit breakers for cross-service dependencies. Return partial health (degraded) for non-critical failures.
