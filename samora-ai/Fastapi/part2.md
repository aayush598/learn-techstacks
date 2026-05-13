# FastAPI Interview Questions and Answers - Part 2

## Q1: How does FastAPI handle concurrent requests with async def vs def?
**A:** FastAPI distinguishes between `async def` (coroutine) and `def` (regular function) path operations. `async def` endpoints are run directly on the ASGI server's event loop, handling concurrent I/O-bound tasks without blocking. `def` endpoints are run in a thread pool (via `run_in_executor`), preventing them from blocking the event loop. For I/O-bound operations (database queries, HTTP calls, file reads), use `async def` for true concurrency. For CPU-bound operations, `def` is fine (thread pool provides parallelism). The thread pool size defaults to `min(32, os.cpu_count() + 4)`. Mixing both types in one app works seamlessly — FastAPI handles the scheduling transparently.

## Q2: Explain FastAPI's dependency injection system for database sessions.
**A:** FastAPI dependencies typically use generators with `yield` for managing database sessions:

```python
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()
```

The `yield` pattern ensures cleanup (closing the session) even if an exception occurs. Dependencies with `yield` are `ContextManagers` — the code before `yield` runs on setup, after `yield` runs on teardown. Multiple dependencies with `yield` execute in reverse order for cleanup. This pattern works with any database library: SQLAlchemy, asyncpg with `async def`, Beanie for MongoDB, etc. For async databases, use `async def` with `async for` in the dependency.

## Q3: How do you implement pagination in FastAPI?
**A:** FastAPI supports pagination via query parameters:

```python
from fastapi import Query

@app.get("/items/")
def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Items per page")
):
    items = db.query(Item).offset(skip).limit(limit).all()
    total = db.query(Item).count()
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
    }
```

For cursor-based pagination, use a `cursor` parameter (typically a base64-encoded ID or timestamp). FastAPI's validation ensures `skip`/`limit` constraints. For reusable pagination, create a dependency: `def pagination(skip: int = 0, limit: int = 10) -> tuple[int, int]`. Libraries like `fastapi-pagination` provide decorators and response models for consistent pagination across endpoints. Consider returning metadata (total count, next/previous URLs) for better client experience.

## Q4: What is FastAPI's `BackgroundTasks` and how is it different from Celery?
**A:** `BackgroundTasks` (from `fastapi.BackgroundTasks`) runs lightweight background operations within the same process after returning the response. Use cases: sending emails, logging, notification dispatch, file cleanup. Limitations: (1) tasks run synchronously in the same process, (2) no retry mechanism, (3) no distributed execution, (4) tasks are lost if the server crashes, (5) blocks the worker if CPU-bound. Celery is a distributed task queue with: (1) separate worker processes, (2) retry and error handling, (3) task scheduling/cron, (4) result storage, (5) multiple brokers (Redis, RabbitMQ), (6) task prioritization. FastAPI + Celery is common: FastAPI handles HTTP requests and enqueues tasks; Celery workers process them asynchronously.

## Q5: How do you implement rate limiting in FastAPI?
**A:** FastAPI doesn't have built-in rate limiting, but it can be implemented via: (1) middleware — check request IP rate in a cache (Redis), (2) dependencies — per-endpoint rate limiting, (3) `slowapi` library (built on top of `limits`), (4) `fastapi-limiter` (Redis-based). Example with middleware:

```python
from fastapi import FastAPI, Request, HTTPException
import time

class RateLimitMiddleware:
    def __init__(self, app, max_requests=100, window=60):
        self.app = app
        self.max_requests = max_requests
        self.window = window
        self.requests = {}
    
    async def __call__(self, scope, receive, send):
        # Implement rate limiting logic here
        pass
```

Production-grade rate limiting uses Redis (distributed, atomic, time-based expiration). For serverless/docker, use API gateway rate limiting (AWS API Gateway, Cloudflare, Nginx). Consider different limits per endpoint (login: stricter, public endpoints: moderate).

## Q6: Explain FastAPI's `Response` model and custom response types.
**A:** FastAPI provides multiple response classes beyond `JSONResponse`: `HTMLResponse`, `PlainTextResponse`, `RedirectResponse`, `StreamingResponse`, `FileResponse`, `ORJSONResponse` (via `orjson`), `UJSONResponse` (via `ujson`). Custom responses:

```python
from fastapi.responses import StreamingResponse, FileResponse
from fastapi import Response

@app.get("/stream")
async def stream_data():
    async def generate():
        for i in range(100):
            yield f"data {i}\n"
    return StreamingResponse(generate(), media_type="text/plain")

@app.get("/download")
async def download():
    return FileResponse("report.pdf", filename="report.pdf", media_type="application/pdf")
```

`StreamingResponse` is essential for large datasets (DB cursors, file downloads). `FileResponse` handles range requests (partial content for video/audio). Custom response classes can extend `Response` with custom `.render()` methods. The `Response` parameter in path operations allows direct response manipulation (setting headers, cookies, status codes).

## Q7: How do you handle file uploads with progress in FastAPI?
**A:** FastAPI uses `UploadFile` for file uploads, which provides a file-like object with `.read()`, `.write()`, `.seek()`, `.file` (raw SpooledTemporaryFile). For progress tracking, implement a custom file-like wrapper or a WebSocket-based progress reporter:

```python
from fastapi import UploadFile, WebSocket

class ProgressFile:
    def __init__(self, file: UploadFile, websocket: WebSocket):
        self.file = file
        self.ws = websocket
        self.total = 0
    
    async def read(self, size=-1):
        data = await self.file.read(size)
        self.total += len(data)
        await self.ws.send_json({"progress": self.total})
        return data
```

For large files, use `StreamingResponse` with async chunked reading. FastAPI's `UploadFile` handles streaming internally — files are stored in memory up to `SPOOL_MAX_SIZE` (default 1MB) then spooled to disk. Set `max_file_size` in the ASGI server (Uvicorn: `--max-file-size`). For chunked uploads, implement client-side chunking with server-side reassembly. Consider using presigned URLs (S3, GCS) for very large files.

## Q8: Explain FastAPI's `WebSocket` disconnect handling and reconnection.
**A:** FastAPI WebSocket endpoints should handle disconnect gracefully:

```python
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup resources
        pass
```

For reconnection, implement on the client side: (1) exponential backoff for reconnection attempts, (2) heartbeat/ping-pong to detect stale connections, (3) message ID tracking for idempotent retries. Server-side: use `websocket.state` to check connection state (`websocket.client_state == WebSocketState.CONNECTED`). For production: use Redis pub/sub to broadcast messages across multiple server instances, and track connection health with periodic pings.

## Q9: How do you implement OAuth2 with multiple providers in FastAPI?
**A:** FastAPI's `OAuth2PasswordBearer` is for first-party auth. For third-party providers (Google, GitHub), use libraries like `authlib` or `python-social-auth`:

```python
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

config = Config('.env')
oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=...,
    client_secret=...,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@app.get('/auth/google')
async def login_via_google(request: Request):
    redirect_uri = request.url_for('auth_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)
```

After OAuth callback, create a JWT token for your application (session management). Store provider info in the user database for account linking. For multiple providers, use a common `User` model with `social_accounts` relationship. Consider using FastAPI's dependency injection to inject the current user and their auth provider info.

## Q10: What is FastAPI's `APIRouter` and how does it help with modularization?
**A:** `APIRouter` (from `fastapi.APIRouter`) enables modular route organization:

```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def list_users(): ...

@router.post("/")
def create_user(): ...

# In main app:
app.include_router(router)
```

`APIRouter` supports: `prefix` (all routes relative), `tags` (OpenAPI grouping), `dependencies` (apply to all routes), `responses` (shared response models), `default_response_class`, `route_class`, `on_event` (lifespan events per router). Routers can be nested (include routers within routers). This enables: (1) feature-based directory structure, (2) reusable API modules, (3) separate versioning (`/v1/`, `/v2/`), (4) cleaner main app file. Each router can have its own dependencies, middlewares, exception handlers, and response models.

## Q11: How does FastAPI handle CORS in production?
**A:** FastAPI's `CORSMiddleware` handles CORS:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com", "https://admin.myapp.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["X-Total-Count"],
    max_age=600,
)
```

Production best practices: (1) specify exact origins (not `["*"]`), (2) use environment variables for origins, (3) restrict methods and headers to what's needed, (4) set appropriate `max_age` to reduce preflight requests, (5) use `expose_headers` for custom response headers the client needs to read, (6) consider using a reverse proxy (Nginx, Cloudflare) for CORS instead of the application layer for better performance. For subdomain-based apps, use regex origins: `allow_origin_regex=["https://.*\\.myapp\\.com"]`.

## Q12: Explain FastAPI's `jsonable_encoder` and its purpose.
**A:** `fastapi.encoders.jsonable_encoder` converts complex Python objects (dataclasses, Pydantic models, datetime, Decimal, UUID, etc.) to JSON-compatible Python types (dicts, lists, strings, numbers). It's used internally by FastAPI's response serialization. Manual use cases: (1) encoding objects for custom JSON serialization, (2) storing complex objects in Redis/Session, (3) logging/dumping objects to files, (4) pre-serializing responses for caching. The encoder handles: Pydantic models (recursively), datetimes (to ISO format), UUIDs (to strings), Decimals (to floats by default, configurable), bytes (to base64), sets (to sorted lists), Enums (to values). Custom encoders can be registered via `json_encoders` in the app config.

## Q13: How do you implement caching in FastAPI?
**A:** Caching strategies in FastAPI: (1) **Response-level caching**: use `fastapi-cache` or `aiocache` with Redis/Memcached backend, (2) **ETag/If-None-Match**: return `ETag` header with response hash, check `If-None-Match` to return `304 Not Modified`, (3) **Cache-Control headers**: `@cache(expire=300)` decorators, (4) **Application-level caching**: `functools.lru_cache` for deterministic computations, (5) **Database query caching**: SQLAlchemy's `caching_query`, Redis caching of query results. Example with `fastapi-cache`:

```python
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

@cache(expire=60)
@app.get("/expensive")
async def expensive_endpoint():
    return {"data": compute_slow_thing()}
```

Cache invalidation strategies: (1) time-based expiration (TTL), (2) event-based invalidation (clear on data mutation), (3) versioned cache keys. Consider cache stampede prevention with probabilistic early expiration.

## Q14: What is FastAPI's `StreamingResponse` and when should it be used?
**A:** `StreamingResponse` sends data in chunks as it becomes available, without loading the entire response into memory. Use cases: (1) large file downloads (CSV exports, video files), (2) server-sent events (SSE), (3) database cursor streaming, (4) proxy responses (streaming from another server), (5) real-time data (log tailing, progress updates). Example for CSV streaming:

```python
@app.get("/export.csv")
async def export_csv():
    async def generate():
        yield "id,name,email\n"
        async for user in db.query(User).stream():
            yield f"{user.id},{user.name},{user.email}\n"
    return StreamingResponse(generate(), media_type="text/csv", 
                             headers={"Content-Disposition": "attachment; filename=users.csv"})
```

Benefits: (1) O(1) memory for arbitrarily large responses, (2) starts sending data immediately (lower Time-To-First-Byte), (3) enables "infinite" streams. Async generators (`async def` with `yield`) work best with `StreamingResponse`.

## Q15: Explain FastAPI's `OAuth2PasswordBearer` and token refresh flow.
**A:** `OAuth2PasswordBearer(tokenUrl="/auth/login")` extracts and validates Bearer tokens from the `Authorization` header. Token refresh flow:

```python
@app.post("/auth/refresh")
async def refresh_token(refresh_token: str = Body(...)):
    payload = verify_refresh_token(refresh_token)
    new_access = create_access_token({"sub": payload["sub"]}, expires=timedelta(minutes=30))
    new_refresh = create_refresh_token({"sub": payload["sub"]}, expires=timedelta(days=7))
    return {"access_token": new_access, "refresh_token": new_refresh, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = await get_user(payload.get("sub"))
        if user is None:
            raise HTTPException(status_code=401)
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
```

Access tokens: short-lived (15-30 min). Refresh tokens: long-lived (7-30 days), stored securely (HttpOnly cookie), rotated on use. Implement token revocation for security (blacklist Redis). The `scopes` parameter in `OAuth2PasswordBearer` supports permission scoping.

## Q16: How do you implement health checks and readiness probes in FastAPI?
**A:** Health check endpoints for container orchestration (K8s, Docker):

```python
@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/ready")
async def readiness(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Database unavailable")
```

Liveness probe (`/health`): checks if the process is alive (lightweight). Readiness probe (`/ready`): checks if dependencies are available (DB, Redis, external services). Startup probe: for slow-starting apps. Best practices: (1) keep liveness probes cheap (don't check DB every few seconds), (2) use readiness probes to check all critical dependencies, (3) set appropriate timeouts (`timeoutSeconds: 3`), (4) implement graceful shutdown (handle `SIGTERM`, stop accepting new requests, finish in-flight requests), (5) add version/build info to health responses for deployment tracking.

## Q17: Explain FastAPI's `Lifespan` events (startup/shutdown).
**A:** FastAPI supports lifespan context manager (Python 3.7+, preferred over `on_event` decorator):

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.db = await create_pool()
    app.state.redis = await redis.create_pool()
    yield
    # Shutdown
    await app.state.db.close()
    await app.state.redis.close()

app = FastAPI(lifespan=lifespan)
```

The `lifespan` async context manager replaces the deprecated `@app.on_event("startup")`/`@app.on_event("shutdown")` pattern. Benefits: (1) proper exception handling, (2) context manager cleanup guaranteed, (3) type-safe `app.state`, (4) avoids event ordering issues. Use for: DB connection pool initialization, Redis connections, loading ML models, initializing third-party clients, warming caches. Store shared resources on `app.state` for access in dependencies.

## Q18: How do you implement request logging and correlation IDs in FastAPI?
**A:** Middleware-based logging with correlation/trace IDs:

```python
import uuid
import time
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    start = time.time()
    
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    
    duration = time.time() - start
    logger.info({
        "correlation_id": correlation_id,
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "duration_ms": round(duration * 1000, 2),
        "ip": request.client.host,
    })
    return response
```

Structured logging (JSON format) enables log aggregation (ELK, Datadog, Loki). Pass `correlation_id` to downstream services via HTTP headers. Use `contextvars` for thread-safe correlation ID access in async code. Include correlation IDs in error responses for client debugging. For OpenTelemetry integration, use `fastapi-instrumentation` or manual span creation with correlation ID propagation.

## Q19: What is FastAPI's `HTTPException` and custom exception handling?
**A:** FastAPI's `HTTPException` raises HTTP errors:

```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Not found"):
        super().__init__(status_code=404, detail=detail)

@app.exception_handler(NotFoundException)
async def not_found_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error_code": "NOT_FOUND", "path": request.url.path},
    )
```

Exception handlers can be global (`@app.exception_handler`) or per-router. Multiple handlers: (1) custom exceptions, (2) Python built-ins (`ValueError`, `KeyError`), (3) web-specific (`HTTPException` subclasses), (4) generic 500 handler for unexpected errors. Best practices: (1) use descriptive error codes, (2) include correlation IDs in error responses, (3) log full tracebacks server-side, (4) never expose stack traces in production, (5) use Pydantic models for consistent error response schemas.

## Q20: How do you implement database migrations with FastAPI?
**A:** FastAPI doesn't include a migration tool — use Alembic (SQLAlchemy) or third-party libraries:

```bash
alembic init alembic
alembic revision --autogenerate -m "create users table"
alembic upgrade head
```

Best practices: (1) run migrations automatically on startup (for development only), (2) use separate migration step in CI/CD for production, (3) always review autogenerated migrations, (4) version control migration files, (5) test migrations with rollback. For production: run migrations as a separate deployment step before starting the new app version (zero-downtime). For async databases (SQLAlchemy 2.0 async), Alembic works synchronously by default — use a separate sync connection for migrations. For MongoDB, use `mongoengine` migrations or manual scripts.

## Q21: Explain FastAPI's `Depends()` caching behavior.
**A:** `Depends()` caches dependency results within the same request scope — if the same dependency is used multiple times in a request, it's only called once and the result is reused:

```python
@app.get("/items")
async def get_items(
    common: CommonParams = Depends(get_common_params),
    auth: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pass  # get_db is called once even if used by multiple sub-dependencies
```

This caching is request-scoped (not global). Dependencies with different parameters are treated as separate. `Depends` uses `functools.lru_cache`-like behavior based on the dependency function identity. To force re-evaluation, use different dependency instances. The cache doesn't apply across different requests. Sub-dependencies are also cached — if both `get_items` and `get_current_user` depend on `get_db`, the database session is created only once.

## Q22: How do you implement soft deletes in FastAPI?
**A:** Soft deletes mark records as deleted without removing them:

```python
from sqlalchemy import Column, Boolean, DateTime
from datetime import datetime

class BaseModel:
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()

# Query filter
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).filter(User.is_deleted == False).all()
```

For automatic filtering, use SQLAlchemy's `@event.listens_for` or a custom query class that always adds `is_deleted == False`. For unique constraints on soft-deletable entities, include `is_deleted` in the constraint (partial unique index in PostgreSQL). Restore endpoint: `PUT /users/{id}/restore`. Cascade soft deletes to related models when appropriate. Consider `deleted_at` timestamp for cleanup job tracking.

## Q23: What is FastAPI's `FileResponse` and range request support?
**A:** `FileResponse(path, status_code=200, headers=None, media_type=None, filename=None, content_disposition_type="attachment")` serves files with automatic range request support (HTTP 206 Partial Content). Range requests enable: (1) video/audio seeking, (2) resume interrupted downloads, (3) parallel chunk downloads. `FileResponse` handles `If-Range`, `If-Modified-Since`, and `Last-Modified` headers. For static files, use `StaticFiles` mounting instead:

```python
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
```

`StaticFiles` supports `Cache-Control`, `ETag`, and `Last-Modified` headers automatically. For streaming large files, `FileResponse` is preferred over reading the whole file into memory. `FileResponse` uses `aiofiles` internally for async file I/O.

## Q24: How do you implement multi-tenancy in FastAPI?
**A:** Multi-tenancy strategies for FastAPI: (1) **Schema-based** (PostgreSQL): each tenant has a separate DB schema, identified by subdomain or header. (2) **Database-based**: each tenant has a separate database. (3) **Row-based**: shared tables with `tenant_id` column. Implementation:

```python
async def get_tenant_id(request: Request):
    tenant = request.headers.get("X-Tenant-ID")
    if not tenant:
        raise HTTPException(400, "X-Tenant-ID header required")
    return tenant

async def get_session(tenant_id: str = Depends(get_tenant_id)):
    engine = get_tenant_engine(tenant_id)  # Cache engines per tenant
    async with AsyncSession(engine) as session:
        yield session
```

For schema-based: switch PostgreSQL schema with `SET search_path TO tenant_schema`. Use middleware to set tenant context per request. Cache database connections per tenant (connection pooling per tenant). Ensure tenant isolation is tested thoroughly. Consider rate limiting per tenant. For B2B SaaS, allow tenant admin to configure custom domains and branding.

## Q25: Explain FastAPI's `Request` object and its properties.
**A:** The `Request` object (from `starlette.requests.Request`) provides access to request details:

```python
from fastapi import Request

@app.post("/submit")
async def handle(request: Request):
    body = await request.body()           # Raw bytes
    json = await request.json()            # Parsed JSON
    form = await request.form()            # Form data
    headers = request.headers              # Case-insensitive dict
    query_params = request.query_params    # Query string
    path_params = request.path_params      # URL path params
    cookies = request.cookies              # Cookie dict
    client = request.client                # Client host/port
    url = request.url                      # Full URL object
    state = request.state                  # Custom state (app.state, middleware data)
    method = request.method                # HTTP method
```

`request.state` is used by middleware to attach data (e.g., `request.state.user`). `request.scope` provides raw ASGI scope. `request.app` references the FastAPI app. `request.receive` allows reading the request body stream. For performance, access body once and reuse (`request.body()` caches the result).

## Q26: How do you implement GraphQL with FastAPI?
**A:** FastAPI integrates with Graphene (sync) or Strawberry (async, preferred for FastAPI):

```python
import strawberry
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class User:
    id: int
    name: str

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> User:
        return User(id=id, name="John")

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
```

Strawberry supports: FastAPI dependency injection in resolvers, file uploads, subscriptions (via WebSocket), dataloaders (N+1 prevention), and federation. For performance: use `DataLoader` for batching database queries. For existing REST endpoints, consider adding GraphQL alongside (not replacing). Strawberry's FastAPI integration respects FastAPI's exception handlers and middleware.

## Q27: What are FastAPI's `middleware` types and execution order?
**A:** FastAPI supports two middleware types: (1) **HTTP middleware** (`@app.middleware("http")`) — wraps the entire request/response cycle, applied to all routes. (2) **ASGI middleware** — lower-level, wraps the ASGI application. HTTP middlewares are executed in reverse order of addition (last added runs first on request, last on response):

```python
@app.middleware("http")
async def middleware1(request, call_next):
    response = await call_next(request)
    return response

@app.middleware("http")  # Runs before middleware1 on request
async def middleware2(request, call_next):
    response = await call_next(request)
    return response
```

Common middleware: CORS, trusted host, HTTPS redirect, GZip, session, authentication, rate limiting, request ID, logging, timing. Middleware can: modify request/response, short-circuit (return response without calling `call_next`), add headers, and handle exceptions. ASGI middleware wraps the entire `app` instance.

## Q28: How do you implement API versioning in FastAPI?
**A:** API versioning strategies: (1) **URL path versioning**: `/v1/users`, `/v2/users` — most common. (2) **Header versioning**: `Accept: application/vnd.api+json;version=2`. (3) **Query parameter**: `/users?version=2`. (4) **Subdomain**: `v1.api.example.com`. Implementation:

```python
from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1")
v2_router = APIRouter(prefix="/v2")

@v1_router.get("/users")
def get_users_v1(): ...

@v2_router.get("/users")
def get_users_v2(): ...

app.include_router(v1_router)
app.include_router(v2_router)
```

For shared logic between versions: (1) use base Pydantic models with version-specific extensions, (2) compose dependencies, (3) use a single codebase with conversion logic. Maintain backward compatibility during deprecation — document sunset dates. Consider content negotiation for more granular versioning.

## Q29: Explain FastAPI's `TestClient` and async testing strategies.
**A:** FastAPI's `TestClient` (from `starlette.testclient`) enables test-driven development:

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

For async tests with pytest:

```python
import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_async():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
```

Best practices: (1) use dependency overrides (`app.dependency_overrides[get_db] = test_db`) for test isolation, (2) create test database with migrations, (3) use factories (factory_boy) for test data, (4) clean up data between tests, (5) use `httpx.AsyncClient` for async endpoint tests, (6) test both success and error paths, (7) test middleware and exception handlers, (8) use `pytest.fixture` for reusable test setup.

## Q30: How do you implement request body size limits in FastAPI?
**A:** FastAPI doesn't have built-in body size limits, but they can be configured at: (1) **ASGI server level** (Uvicorn): `uvicorn.run(app, max_body_size=1_000_000)` (bytes), (2) **Nginx reverse proxy**: `client_max_body_size 10m`, (3) **Middleware**: custom body size check:

```python
from fastapi import Request, HTTPException

@app.middleware("http")
async def limit_body_size(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 1_000_000:
        raise HTTPException(413, "Request body too large")
    return await call_next(request)
```

Note: `content-length` header may not be present for chunked transfer encoding. For more robust limits, read the body in chunks. Set appropriate limits per endpoint (file upload endpoints have higher limits). Consider streaming large bodies directly to storage to avoid memory issues.

## Q31: What are FastAPI's `dependencies` with `yield` (context managers)?
**A:** Dependencies with `yield` act as context managers, with setup code before `yield` and teardown after:

```python
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
```

The `yield` separator: (1) code before `yield` runs when the dependency is resolved, (2) the yielded value is injected, (3) code after `yield` runs after the response is sent. If an exception occurs, the `finally` block still executes. Multiple `yield` dependencies execute cleanup in reverse order (LIFO). Dependencies can yield multiple times (generator) though this is unusual. FastAPI handles exceptions in `yield` dependencies properly.

## Q32: How do you implement server-sent events (SSE) in FastAPI?
**A:** SSE provides real-time updates over HTTP using `StreamingResponse`:

```python
import asyncio
from fastapi.responses import StreamingResponse

@app.get("/events")
async def event_stream():
    async def generate():
        while True:
            data = f"data: {datetime.now()}\n\n"
            yield data
            await asyncio.sleep(1)
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )
```

SSE vs WebSocket: SSE is simpler (one-way server→client), works over HTTP/1.1 and HTTP/2, has automatic reconnection, but limited to text data and fewer concurrent connections per browser. WebSocket supports bidirectional communication. For SSE in production: (1) handle client disconnect (check `await request.is_disconnected()`), (2) use Redis pub/sub for multi-process broadcasting, (3) set `X-Accel-Buffering: no` for Nginx compatibility, (4) include heartbeat pings to detect stale connections.

## Q33: Explain FastAPI's `Form` and `File` parameter dependencies.
**A:** FastAPI handles form data and file uploads via `Form` and `File` from `fastapi`:

```python
from fastapi import Form, File, UploadFile

@app.post("/upload")
async def upload(
    name: str = Form(...),
    bio: str = Form(""),
    file: UploadFile = File(...),
    extra: list[UploadFile] = File(None)
):
    content = await file.read()
    return {"filename": file.filename, "content_type": file.content_type, "size": len(content)}
```

`Form(...)` declares form fields; `File(...)` declares file fields. `UploadFile` provides async file-like interface with: `.read()`, `.write()`, `.seek()`, `.close()`, `.file` (raw SpooledTemporaryFile). Multiple file uploads: `files: list[UploadFile] = File(...)`. Files are stored temporarily — process immediately or save to persistent storage. For large files, read in chunks: `while chunk := await file.read(1024*1024): process(chunk)`.

## Q34: How do you implement data export (CSV, Excel) in FastAPI?
**A:** Streaming data export using `StreamingResponse` + CSV writer:

```python
import csv, io
from fastapi.responses import StreamingResponse

@app.get("/export/csv")
async def export_csv(db: Session = Depends(get_db)):
    def generate():
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["ID", "Name", "Email"])
        yield buffer.getvalue()
        buffer.seek(0)
        buffer.truncate(0)
        
        for user in db.query(User).yield_per(1000):
            writer.writerow([user.id, user.name, user.email])
            yield buffer.getvalue()
            buffer.seek(0)
            buffer.truncate(0)
    
    return StreamingResponse(generate(), media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=users.csv"})
```

For Excel: use `openpyxl` or `xlsxwriter` with `StreamingResponse`. For large exports: (1) stream results (don't load all into memory), (2) use database cursors (`yield_per` for SQLAlchemy), (3) implement pagination limits, (4) use background tasks for very large exports (generate file, email link), (5) compress responses with gzip. For PDF: use `ReportLab` or `WeasyPrint` with `FileResponse` or `StreamingResponse`.

## Q35: What is FastAPI's `StaticFiles` mounting and its options?
**A:** `StaticFiles` serves static directories:

```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static", html=False, check_dir=True), name="static")
```

Options: `directory` (source directory), `html` (if True, serves index.html for directory paths — enables SPA mode), `check_dir` (validate directory exists at startup), `follow_symlink` (follow symbolic links). `StaticFiles` supports: `If-Modified-Since`, `ETag`, `Cache-Control`, range requests, and directory listing (when `html=True`). For production: serve static files via reverse proxy (Nginx, CDN) instead of FastAPI for better performance. `StaticFiles` can also serve from package resources or in-memory. For SPA (React, Vue), mount at `/` with `html=True` after all API routes.

## Q36: How do you implement WebSocket authentication in FastAPI?
**A:** WebSocket authentication requires custom handling since cookies/headers are sent in the initial handshake:

```python
from fastapi import WebSocket, WebSocketDisconnect, HTTPException, Cookie

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Cookie(None)):
    if not token:
        await websocket.close(code=4001)
        return
    try:
        user = verify_token(token)
    except:
        await websocket.close(code=4001)
        return
    
    await websocket.accept()
    await websocket.send_json({"msg": f"Welcome {user.name}"})
    # ... handle messages
```

Alternative: validate token in the first WebSocket message (application-level auth). Since WebSocket headers can't be easily set by browsers, use query parameters (less secure — logged in server logs) or cookies (more secure). For production: (1) use `SameSite=Strict` cookies, (2) validate origin header to prevent CSWSH (Cross-Site WebSocket Hijacking), (3) implement token expiry and refresh for long-lived connections, (4) rate-limit WebSocket connections per user.

## Q37: Explain FastAPI's `HTTP/2` and `HTTP/3` support.
**A:** FastAPI (via Starlette/Uvicorn) supports HTTP/2 when using the `h2` library with `uvicorn`:

```bash
uvicorn main:app --http h2
```

HTTP/2 benefits: multiplexing (multiple requests over single connection), server push, header compression (HPACK), binary protocol. HTTP/2 requires TLS (HTTPS) — most browsers won't negotiate HTTP/2 over cleartext. HTTP/3 (QUIC) is supported via `uvicorn` with `--http httptools` and a QUIC-capable reverse proxy (Caddy, Nginx with quiche). For most deployments, terminate TLS at a reverse proxy (Nginx, Caddy, Cloudflare) which handles HTTP/2 and HTTP/3, then proxy to FastAPI via HTTP/1.1. This is simpler and more performant than FastAPI handling HTTP/2 directly.

## Q38: How do you implement database connection pooling in FastAPI?
**A:** FastAPI uses SQLAlchemy's connection pooling:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    DATABASE_URL,
    pool_size=10,           # Number of connections to maintain
    max_overflow=20,        # Extra connections allowed beyond pool_size
    pool_timeout=30,        # Seconds to wait before timeout
    pool_recycle=3600,      # Recycle connections after 1 hour
    pool_pre_ping=True,     # Verify connections before use
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

For async:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True,
)
```

`pool_pre_ping` detects stale connections (common with load balancers, DB restarts). `pool_recycle` prevents long-lived connection timeout by database. Connection pool sizing: monitor database connections and adjust. Too few: request queuing. Too many: database resource exhaustion. Use `pool_size` = `max_workers` of ASGI server for optimal throughput.

## Q39: What is FastAPI's `JSONResponse` and custom encoders?
**A:** `JSONResponse(content, status_code=200, headers=None, media_type="application/json")` is the default response type. Custom JSON encoders:

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import orjson

class ORJSONResponse(JSONResponse):
    media_type = "application/json"
    
    def render(self, content: Any) -> bytes:
        return orjson.dumps(content, option=orjson.OPT_UTC_Z)

app = FastAPI(default_response_class=ORJSONResponse)
```

Or set per-endpoint: `@app.get("/", response_class=ORJSONResponse)`. Custom encoders handle: datetime (ISO format), UUID, Decimal, bytes (base64), Enum, Pydantic models, dataclasses, and custom types. `orjson` is significantly faster than the default `json` module. `ujson` is another alternative. For security, avoid `json.dumps` default handler that calls `str()` on unknown types (information leakage risk). Always validate response content matches the schema.

## Q40: How do you implement idempotency in FastAPI APIs?
**A:** Idempotency prevents duplicate operations (critical for payment APIs):

```python
from fastapi import Header, HTTPException
import uuid

@app.post("/payments")
async def create_payment(
    payment: PaymentCreate,
    idempotency_key: str = Header(None, alias="Idempotency-Key")
):
    if not idempotency_key:
        idempotency_key = str(uuid.uuid4())
    
    # Check if already processed
    existing = await redis.get(f"idempotency:{idempotency_key}")
    if existing:
        return JSONResponse(content=json.loads(existing), status_code=200)
    
    # Process payment
    result = await process_payment(payment)
    
    # Store result with TTL
    await redis.setex(f"idempotency:{idempotency_key}", 86400, result.json())
    return result
```

Best practices: (1) client generates the idempotency key (UUID), (2) server stores completed results with TTL (24h typical), (3) return 200 (not 201) for duplicate requests with same key, (4) return 409 Conflict if different request body with same key, (5) use Redis for distributed idempotency storage, (6) consider using idempotency for all state-changing mutations. The idempotency key should be unique per operation and per user.

## Q41: Explain FastAPI's `response_model` and its serialization behavior.
**A:** `response_model` controls serialization of the response, filtering out fields not in the model:

```python
class UserOut(BaseModel):
    id: int
    name: str
    email: str  # Note: no password field

class UserIn(BaseModel):
    name: str
    email: str
    password: str

@app.post("/users", response_model=UserOut)
def create_user(user: UserIn):
    db_user = create_user_in_db(user)
    return db_user  # password field is automatically excluded
```

`response_model` is applied after the function returns — it filters and validates the output. `response_model_exclude_unset=True` excludes fields not explicitly set. `response_model_include`/`response_model_exclude` for field-level control. `response_model_by_alias` controls alias usage. `response_model_exclude_none=True` excludes None values. The function can return ORM objects or dicts — Pydantic handles conversion. Response model affects OpenAPI schema generation.

## Q42: How do you implement Row-Level Security (RLS) in FastAPI?
**A:** RLS enforces that users can only access their own data:

```python
async def get_current_user(token: str = Depends(oauth2_scheme)):
    return decode_token(token)

@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(403, "Access denied")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404)
    return user
```

For PostgreSQL, implement RLS at the database level with policies, then set `app.current_user_id` in the database session:

```python
@app.middleware("http")
async def set_rls_context(request: Request, call_next):
    token = request.headers.get("Authorization")
    if token:
        user = decode_token(token)
        async with engine.connect() as conn:
            await conn.execute(text(f"SET app.current_user_id = '{user.id}'"))
    return await call_next(request)
```

Combining application-level checks with database RLS provides defense in depth. For multi-tenant apps, ensure tenant isolation at both levels. Consider using SQLAlchemy's `viewonly=True` for read-only access patterns.

## Q43: What is FastAPI's `timeout` mechanisms for requests?
**A:** FastAPI doesn't have built-in request timeouts, but they can be implemented at multiple levels: (1) **ASGI server** (Uvicorn): `--timeout-keep-alive 5`, `--limit-concurrency`, `--limit-max-requests`, (2) **HTTP client timeouts** for outgoing requests (httpx, aiohttp), (3) **Database query timeouts**: `db.execute(query).execution_options(timeout=5)`, (4) **Background task timeouts**: `asyncio.wait_for(task, timeout=30)`, (5) **Nginx reverse proxy**: `proxy_read_timeout 30s`, (6) **Application-level middleware**:

```python
import asyncio
from fastapi import Request, HTTPException

@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    try:
        return await asyncio.wait_for(call_next(request), timeout=30)
    except asyncio.TimeoutError:
        raise HTTPException(504, "Request timeout")
```

Set timeouts based on endpoint characteristics: (1) simple reads: 10s, (2) complex operations: 30s, (3) file uploads: 5min+, (4) streaming: no hard timeout (handle disconnect). Use `asyncio.shield()` for critical cleanup that shouldn't be interrupted by timeout.

## Q44: Explain FastAPI's `validation_alias` and `serialization_alias` in Pydantic V2.
**A:** Pydantic V2 (FastAPI's default since 0.100.0) separates aliases for validation (input) and serialization (output):

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(validation_alias="userName", serialization_alias="user_name")
    email: str = Field(alias="email_address")  # Same for both

# Input: {"userName": "John", "email_address": "john@test.com"}
# Output: {"user_name": "John", "email_address": "john@test.com"}
```

This decouples the external API contract from internal field names. `validation_alias` affects how data is parsed (from JSON, form data, etc.). `serialization_alias` affects how data is output (JSON response). `by_alias=True` in response models uses aliases. `populate_by_name=True` allows using both aliased and original names for input. This is useful for: (1) camelCase input, snake_case output, (2) backward-compatible API evolution, (3) decoupling internal and external schemas.

## Q45: How do you implement request validation with custom validators in Pydantic V2?
**A:** Pydantic V2 uses `@field_validator` and `@model_validator`:

```python
from pydantic import BaseModel, field_validator, model_validator
from typing import Self

class OrderCreate(BaseModel):
    items: list[ItemCreate]
    coupon_code: str | None = None
    
    @field_validator("coupon_code")
    @classmethod
    def validate_coupon(cls, v: str | None) -> str | None:
        if v and len(v) < 3:
            raise ValueError("Coupon code too short")
        return v.upper() if v else v
    
    @model_validator(mode="after")
    def validate_order(self) -> Self:
        if len(self.items) > 100:
            raise ValueError("Too many items")
        return self
```

Pydantic V2 validators: `mode="before"` (pre-parse), `mode="wrap"` (flexible), `mode="after"` (post-parse, on the validated model). `@field_validator` validates single fields. `@model_validator` validates the whole model. For cross-field validation, use `model_validator`. Validators can transform values (e.g., trimming whitespace, normalizing formats). For async validators, use `@field_validator` with `@classmethod` and `async def`. FastAPI catches validation errors automatically as 422 responses.

## Q46: What is FastAPI's `exception_handlers` registry?
**A:** The `exception_handlers` dict maps exception types to handler functions:

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

def custom_404_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=404, content={"message": "Custom not found"})

app = FastAPI()
app.add_exception_handler(HTTPException, custom_404_handler)
```

Or using decorator: `@app.exception_handler(HTTPException)`. Handler receives request and exception, returns a Response. Multiple handlers can be registered — the most specific match wins (subclass before parent). Handlers can be added to routers (per-router exception handling). Exception handlers work for: FastAPI `HTTPException`, Python built-in exceptions, custom exceptions, ASGI errors, WebSocket errors. For unhandled exceptions, FastAPI returns a 500 internal server error (stack trace in debug mode).

## Q47: How do you implement ETag-based caching in FastAPI?
**A:** ETags provide conditional request handling (HTTP 304 Not Modified):

```python
import hashlib
from fastapi import Request, Response

@app.get("/users/{user_id}")
async def get_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    content = user.json()
    etag = hashlib.md5(content.encode()).hexdigest()
    
    if_none_match = request.headers.get("if-none-match")
    if if_none_match == etag:
        return Response(status_code=304)
    
    return Response(content=content, media_type="application/json", 
                    headers={"ETag": etag})
```

Better: use middleware for automatic ETag generation. Weak ETags (`W/"etag"`) for byte-level equivalence. Strong ETags for byte-exact equivalence. For dynamic content, include `Last-Modified` alongside ETag. For cache invalidation: update ETag when data changes. `Cache-Control: no-cache` forces revalidation (ETag check) while allowing caching. `Cache-Control: max-age=3600` allows caching without revalidation for 1 hour.

## Q48: Explain FastAPI's `route` classes and custom route handling.
**A:** FastAPI's `APIRouter.route()` and custom route classes allow behavior customization:

```python
from fastapi.routing import APIRoute

class TimedRoute(APIRoute):
    def get_route_handler(self):
        original_handler = super().get_route_handler()
        async def custom_handler(request):
            start = time.time()
            response = await original_handler(request)
            duration = time.time() - start
            response.headers["X-Process-Time"] = str(duration)
            return response
        return custom_handler

app = FastAPI(route_class=TimedRoute)
```

`APIRoute` methods you can override: `get_route_handler()` (wrap the handler), `serialize_response()` (custom response serialization). Route classes are applied at the app or router level. Custom route classes enable: (1) request/response timing, (2) request logging, (3) response transformation, (4) custom error handling, (5) authentication at the route level. They're more granular than middleware (applied per-route) but more powerful than decorators (access to route metadata).

## Q49: How do you implement slow API query detection in FastAPI?
**A:** Detect and log slow queries:

```python
import time
from fastapi import Request

@app.middleware("http")
async def slow_query_detector(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    
    if duration > 1.0:  # Slow query threshold
        logger.warning({
            "slow_query": True,
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "duration_ms": round(duration * 1000, 2),
            "ip": request.client.host,
        })
    return response
```

For database query profiling, instrument SQLAlchemy:

```python
import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# Or use SQLALCHEMY_ECHO=True
engine = create_engine(DATABASE_URL, echo=True)
```

For async databases, use `asyncpg` query logging hooks. Integrate with APM tools (Datadog, New Relic, Sentry) for production monitoring. Set per-endpoint slow thresholds (file uploads vs simple reads). Use `EXPLAIN ANALYZE` for identifying slow SQL queries. Consider adding query timing to response headers (`X-DB-Query-Time`) for debugging.

## Q50: What are FastAPI's `response_class` and how to use custom responses?
**A:** FastAPI's `response_class` parameter controls the response type:

```python
from fastapi.responses import HTMLResponse, PlainTextResponse, ORJSONResponse

@app.get("/html", response_class=HTMLResponse)
async def get_html():
    return "<html><body><h1>Hello</h1></body></html>"

@app.get("/text", response_class=PlainTextResponse)
async def get_text():
    return "Hello, World!"

@app.get("/orjson", response_class=ORJSONResponse)
async def get_orjson():
    return {"message": "fast with orjson"}
```

Built-in response classes: `JSONResponse`, `HTMLResponse`, `PlainTextResponse`, `RedirectResponse`, `StreamingResponse`, `FileResponse`, `ORJSONResponse`, `UJSONResponse`, `Response` (base). The `response_class` affects: (1) how the return value is serialized, (2) the `Content-Type` header, (3) rendering behavior. Combine `response_class` with `response_model` — the model validates, the class serializes. For custom media types, extend `Response` and override `.render()`.

## Q51: How do you handle database N+1 queries in FastAPI?
**A:** The N+1 problem occurs when lazy loading causes extra queries. Solutions for SQLAlchemy:

```python
# Eager loading
from sqlalchemy.orm import joinedload, selectinload

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    # Single query with JOIN
    return db.query(User).options(joinedload(User.posts)).all()
    # Or: selectinload for collections (separate query, often faster)
    return db.query(User).options(selectinload(User.posts)).all()

# Async SQLAlchemy
@app.get("/users-async")
async def get_users_async(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).options(selectinload(User.posts))
    )
    return result.scalars().all()
```

Detection: (1) enable SQLAlchemy echo logging, (2) use `sqlalchemy_panel` for dev monitoring, (3) check number of queries in tests. `joinedload` uses LEFT OUTER JOIN (single query, can cause duplicate rows — use `distinct=True`). `selectinload` uses a second query with IN clause (better for large collections). For GraphQL-like APIs, consider dataloader patterns (collect IDs, batch query).

## Q52: Explain FastAPI's `openapi_prefix` and server customization.
**A:** `openapi_prefix` (deprecated, replaced by `servers` and `root_path`) configures the OpenAPI server URL:

```python
app = FastAPI(
    servers=[
        {"url": "https://api.example.com/v1", "description": "Production"},
        {"url": "https://staging.example.com/v1", "description": "Staging"},
    ],
    root_path="/api/v1"  # For behind-reverse-proxy
)
```

`root_path` handles reverse proxy path prefix (the ASGI server strips the prefix, but FastAPI needs it for OpenAPI generation). `servers` shows available server URLs in Swagger UI. For dynamically determining the server URL (behind load balancer), use middleware to set `request.scope["root_path"]`. The OpenAPI schema supports server variables: `{"url": "https://{environment}.example.com", "variables": {"environment": {"default": "api"}}}`.

## Q53: How do you implement database encryption at rest with FastAPI?
**A:** Application-level encryption for sensitive fields:

```python
from cryptography.fernet import Fernet
from pydantic import field_serializer, field_validator

class PatientRecord(BaseModel):
    id: int
    name: str
    ssn: str  # Encrypted at rest
    
    @field_validator("ssn", mode="before")
    @classmethod
    def decrypt_ssn(cls, v: str) -> str:
        if v and not v.startswith("encrypted:"):  # Already decrypted
            return v
        return cipher.decrypt(v.replace("encrypted:", "").encode()).decode()
    
    @field_serializer("ssn")
    def encrypt_ssn(self, v: str) -> str:
        return "encrypted:" + cipher.encrypt(v.encode()).decode()
```

For column-level encryption in the database (PostgreSQL `pgcrypto`):

```python
from sqlalchemy import Column, LargeBinary
from sqlalchemy.ext.hybrid import hybrid_property

class Patient(Base):
    _ssn = Column("ssn", LargeBinary)
    
    @hybrid_property
    def ssn(self):
        return decrypt(self._ssn)
    
    @ssn.setter
    def ssn(self, value):
        self._ssn = encrypt(value)
```

Consider: (1) key management (HSM, KMS, environment variables), (2) key rotation strategy, (3) search limitations on encrypted data, (4) performance impact of encryption/decryption, (5) audit logging for sensitive data access. For full DB encryption, use Transparent Data Encryption (TDE) at the database level.

## Q54: What is FastAPI's `app.state` and how is it used?
**A:** `app.state` stores application-level attributes accessible across requests:

```python
app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.db_pool = await create_db_pool()
    app.state.redis = await aioredis.create_redis_pool("redis://localhost")
    app.state.ml_model = load_model()

@app.get("/predict")
async def predict(features: Features, request: Request):
    model = request.app.state.ml_model
    return {"prediction": model.predict(features)}
```

Dependencies access `app.state` via `request.app.state` or `BackgroundTasks`. Use cases: database connection pools, Redis clients, ML model instances, configuration objects, HTTP clients, cache objects. `app.state` is a simple attribute container — it's not typed. For type safety, use a dataclass or Pydantic model for the state. Thread-safety: `app.state` is read-mostly (written at startup), safe for async code.

## Q55: How do you implement feature flags in FastAPI?
**A:** Feature flags control feature availability without deployment:

```python
from fastapi import Request, HTTPException

FEATURE_FLAGS = {
    "new_checkout": {"enabled": True, "users": [1, 2, 3]},
    "beta_search": {"enabled": False},
}

def feature_flag(flag_name: str):
    async def checker(request: Request):
        user = request.state.user
        config = FEATURE_FLAGS.get(flag_name, {})
        if config.get("enabled"):
            allowed_users = config.get("users", [])
            if not allowed_users or user.id in allowed_users:
                return True
        raise HTTPException(404, detail="Feature not found")
    return Depends(checker)

@app.get("/v2/checkout")
async def new_checkout(_=Depends(feature_flag("new_checkout"))):
    return {"checkout_v2": True}
```

For production: (1) use a database or Redis-backed flag store (not hardcoded), (2) implement gradual rollout (percentage-based), (3) support A/B testing, (4) add metrics for each feature variant, (5) implement kill switches for emergency disable. Libraries: `flipper`, `gunicorn-featureflags`, or custom solution with Redis. FastAPI's dependency injection makes per-route feature flags clean and testable.

## Q56: Explain FastAPI's `OpenAPI` schema customization.
**A:** FastAPI generates OpenAPI documentation automatically. Customization options:

```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        version="2.5.0",
        description="Custom API description",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {"url": "https://example.com/logo.png"}
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

OpenAPI extensions: (1) `x-tagGroups` for grouping endpoints, (2) `x-logo` for custom logo, (3) custom security schemes, (4) examples and descriptions. The `openapi_tags` parameter on `FastAPI()` sets tag metadata. Response models and request bodies are automatically extracted from Pydantic models. For fine-grained control, override `app.openapi()` function. The OpenAPI JSON is available at `/openapi.json`.

## Q57: How do you handle database migrations rollback in FastAPI?
**A:** Alembic rollback support:

```python
# Downgrade one revision
alembic downgrade -1
# Downgrade to specific revision
alembic downgrade <revision_id>
# Rollback all
alembic downgrade base
```

Best practices: (1) test upgrades AND downgrades in development, (2) verify downgrades restore data correctly, (3) write explicit downgrade functions (don't rely on autogenerate), (4) include data migrations in both directions, (5) version control migration scripts, (6) lock deployment to prevent concurrent migrations. For FastAPI lifecycle:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("RUN_MIGRATIONS"):
        os.system("alembic upgrade head")
    yield
```

Never auto-run migrations in production — use separate deployment step. For zero-downtime migrations: expand-contract pattern (additive changes first, backward-compatible code, remove old schema later).

## Q58: What is FastAPI's `BackgroundTasks` error handling?
**A:** FastAPI `BackgroundTasks` doesn't propagate errors to the response (the response is already sent):

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    try:
        with open("log.txt", "a") as f:
            f.write(message)
    except Exception as e:
        logger.error(f"Background task failed: {e}")

@app.post("/send-notification")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification sent"}
```

Error handling strategies: (1) wrap task body in try/except, (2) log all exceptions, (3) use `asyncio.shield()` for critical cleanup, (4) monitor background task failure metrics, (5) for reliability, use Celery instead of `BackgroundTasks`. Background tasks run in the same process — a crash affects the server. For long-running tasks, consider a separate worker process. Async background tasks: `background_tasks.add_task(async_function, arg)`.

## Q59: How do you implement API documentation with examples in FastAPI?
**A:** FastAPI supports OpenAPI examples in multiple ways:

```python
from pydantic import BaseModel, Field
from fastapi import Body

class Item(BaseModel):
    name: str = Field(examples=["Widget"])
    price: float = Field(examples=[19.99])
    tags: list[str] = Field(examples=[["new", "featured"]])

@app.post("/items")
async def create_item(
    item: Item,
    x_debug: bool = Body(False, examples=[True]),
):
    return item

# Config-level examples
class ItemWithExample(BaseModel):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "Widget", "price": 19.99, "tags": ["new"]}
            ]
        }
    }
```

FastAPI 0.103.0+ uses Pydantic V2's `Field(examples=...)` syntax (single example per field). OpenAPI 3.1 supports multiple examples per property. For request bodies, use `Body(example=...)` for the whole body or individual field examples. Test endpoint examples render in Swagger UI and ReDoc. For complex schemas, provide multiple examples showing different use cases.

## Q60: Explain FastAPI's `middleware` vs `exception_handler` order.
**A:** The execution order: (1) incoming request → middlewares (first added, last executed on request), (2) route handler, (3) `response_model` validation, (4) returning response → middlewares (last added, last executed on response). Exception handlers run when an exception is raised, in this order: (1) route-level exception handlers, (2) router-level, (3) app-level, (4) default error handler (500). A middleware can catch exceptions if it wraps `call_next` in try/except — the exception won't reach the exception handler. If a middleware calls `call_next` and an exception occurs, the middleware's except block runs, then the response continues through outer middlewares.

## Q61: How do you implement request/response compression in FastAPI?
**A:** FastAPI (via Starlette) supports GZip compression via middleware:

```python
from starlette.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)  # Compress responses larger than 1KB
```

The `GZipMiddleware` compress responses conditionally (checks `Accept-Encoding` header). For Brotli compression (better compression ratio), use a custom middleware or handle at the reverse proxy level. Client-side compression: accept `Content-Encoding: gzip` requests by inspecting `Content-Encoding` header and decompressing. For large request bodies (file uploads), consider accepting compressed uploads to reduce transfer time. At the reverse proxy level (Nginx): `gzip on; gzip_types application/json;` — more efficient than app-level compression.

## Q62: What are FastAPI's `json_schema_extra` and custom JSON Schema?
**A:** Pydantic V2's `json_schema_extra` extends the generated JSON Schema:

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str
    price: float = Field(ge=0, json_schema_extra={"example": 29.99})
    
    model_config = {
        "json_schema_extra": {
            "examples": [{"name": "Widget", "price": 29.99}],
            "x-custom-field": "This is a custom extension"
        }
    }
```

Uses: (1) adding `examples` for documentation, (2) adding vendor extensions (`x-*`), (3) custom validation metadata consumed by frontend generators (OpenAPI → TypeScript), (4) UI hints (field order, grouping). The `json_schema_extra` at the field level merges with model-level extras. For full control, override `model_json_schema()` method. FastAPI passes the schema to OpenAPI automatically.

## Q63: How do you implement rate limiting per user in FastAPI?
**A:** Per-user rate limiting with Redis:

```python
import aioredis
from fastapi import Request, HTTPException, Depends

redis = aioredis.from_url("redis://localhost")

async def rate_limit(request: Request, user: User = Depends(get_current_user)):
    key = f"ratelimit:{user.id}:{request.url.path}"
    current = await redis.incr(key)
    if current == 1:
        await redis.expire(key, 60)  # 60 second window
    if current > 100:  # Max 100 requests per minute
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    return True

@app.get("/protected", dependencies=[Depends(rate_limit)])
async def protected_endpoint():
    return {"data": "sensitive"}
```

Strategy: (1) sliding window (more accurate, more Redis operations), (2) fixed window (simpler, burst at boundaries), (3) token bucket (smooth rate). Include rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`. Different limits per endpoint (login: 5/min, API: 100/min, admin: 1000/min). For distributed rate limiting, use Redis sorted sets or the `sliding-window-counter` algorithm.

## Q64: Explain FastAPI's `Form` validation with Pydantic models.
**A:** Form data validation with Pydantic (FastAPI 0.103+):

```python
from fastapi import Form
from pydantic import BaseModel

class LoginForm(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(data: Annotated[LoginForm, Form()]):  # or: data: LoginForm = Form()
    return {"username": data.username}
```

Older approach (individual form fields): `username: str = Form(...)`. Newer approach: Pydantic model with `Annotated[Model, Form()]`. Form data is `application/x-www-form-urlencoded` (not JSON). FastAPI handles parsing automatically. For file uploads in forms, use `UploadFile = File(...)` alongside `Form()` fields. Form data can't be mixed with JSON bodies in the same request. For complex form submissions, consider using multipart form data with JSON-encoded fields.

## Q65: How do you implement database auditing in FastAPI?
**A:** Database auditing tracks who changed what and when:

```python
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_mixin, declared_attr
from datetime import datetime

@declarative_mixin
class AuditMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=datetime.utcnow, nullable=False)
    
    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @declared_attr
    def created_by(cls):
        return Column(Integer, nullable=True)
    
    @declared_attr
    def updated_by(cls):
        return Column(Integer, nullable=True)

class User(Base, AuditMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
```

For full audit trails, use SQLAlchemy event listeners or PostgreSQL triggers to log changes to an audit table:

```python
from sqlalchemy import event

@event.listens_for(User, "before_update")
def receive_before_update(mapper, connection, target):
    audit_entry = AuditLog(
        table_name="users",
        record_id=target.id,
        action="UPDATE",
        changed_by=get_current_user_id(),
        timestamp=datetime.utcnow(),
    )
    connection.execute(audit_table.insert().values(audit_entry.dict()))
```

Consider using `sqlalchemy-continuum` or `django-simple-history`-like patterns for automatic versioning. For GDPR compliance, ensure audit logs don't store PII indefinitely.

## Q66: What is FastAPI's `app.openapi()` method for custom schema?
**A:** Override `app.openapi()` to customize the OpenAPI schema:

```python
from fastapi.openapi.utils import get_openapi

app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="This is a custom OpenAPI schema",
        routes=app.routes,
    )
    
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
        }
    }
    
    # Add global security
    openapi_schema["security"] = [{"ApiKeyAuth": []}]
    
    # Merge with custom schema
    openapi_schema["info"]["x-logo"] = {"url": "https://example.com/logo.svg"}
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

Common customizations: (1) adding re-used response schemas, (2) adding webhook definitions, (3) adding custom security schemes, (4) modifying or filtering routes, (5) adding external documentation links. Cache the schema (`app.openapi_schema`) as shown — it's expensive to regenerate on every request.

## Q67: How do you implement database transactions in FastAPI?
**A:** SQLAlchemy transaction management in FastAPI:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()  # Auto-commit on success
    except Exception:
        db.rollback()  # Rollback on error
        raise
    finally:
        db.close()

@app.post("/transfer")
def transfer_funds(
    from_id: int, to_id: int, amount: float,
    db: Session = Depends(get_db)
):
    # In or out of transaction context:
    from_account = db.query(Account).with_for_update().filter(Account.id == from_id).first()
    to_account = db.query(Account).filter(Account.id == to_id).first()
    
    from_account.balance -= amount
    to_account.balance += amount
    # db.commit() is called by get_db dependency
```

For explicit transaction control:

```python
@app.post("/transfer")
def transfer_funds(from_id: int, to_id: int, amount: float, db: Session = Depends(get_db)):
    with db.begin():  # Explicit transaction
        from_account = db.query(Account).with_for_update().filter(Account.id == from_id).first()
        to_account = db.query(Account).filter(Account.id == to_id).first()
        from_account.balance -= amount
        to_account.balance += amount
    # Auto-committed or rolled back on exception
```

`with_for_update()` provides row-level locking (SELECT ... FOR UPDATE) to prevent race conditions. For async, use `async with session.begin()`. Set isolation levels per transaction or globally. Always handle concurrent modifications with pessimistic (row locks) or optimistic (version column) locking.

## Q68: Explain FastAPI's `WebSocket` connection management for chat applications.
**A:** WebSocket connection manager for multi-client chat:

```python
from fastapi import WebSocket
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        self.active_connections[user_id].remove(websocket)
        if not self.active_connections[user_id]:
            del self.active_connections[user_id]
    
    async def send_personal(self, message: dict, user_id: int):
        for ws in self.active_connections.get(user_id, []):
            await ws.send_json(message)
    
    async def broadcast(self, message: dict):
        for user_connections in self.active_connections.values():
            for ws in user_connections:
                await ws.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        await manager.broadcast({"msg": f"User {user_id} disconnected"})
```

For horizontal scaling (multiple server instances), use Redis pub/sub to broadcast messages across instances. Store WebSocket connections per server; use Redis channel for cross-server message delivery.

## Q69: How do you implement data sanitization and validation in FastAPI?
**A:** Pydantic provides comprehensive validation and sanitization:

```python
from pydantic import BaseModel, field_validator
import html

class UserInput(BaseModel):
    name: str
    email: str
    bio: str | None = None
    
    @field_validator("name", "bio")
    @classmethod
    def sanitize_html(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return html.escape(v.strip())
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = v.strip().lower()
        if "@" not in v:
            raise ValueError("Invalid email")
        return v
    
    @field_validator("bio")
    @classmethod
    def limit_length(cls, v: str | None) -> str | None:
        if v and len(v) > 1000:
            raise ValueError("Bio too long (max 1000 characters)")
        return v
```

Sanitization strategies: (1) strip whitespace (`strip()`), (2) escape HTML (`html.escape`), (3) normalize Unicode (`unicodedata.normalize`), (4) remove control characters, (5) limit string lengths, (6) whitelist patterns (regex validation), (7) use libraries like `bleach` for HTML sanitization. For SQL injection: use parameterized queries (SQLAlchemy ORM handles this). For NoSQL injection: validate and sanitize query parameters. For file uploads: validate content type, scan for malware, limit file size.

## Q70: What are FastAPI's hooks for OpenAPI documentation customization?
**A:** FastAPI provides several hooks for OpenAPI customization:

```python
from fastapi import FastAPI
from fastapi.openapi.constants import REF_PREFIX

app = FastAPI(
    title="API Documentation",
    description="Detailed API docs with examples",
    version="2.0.0",
    openapi_tags=[
        {"name": "users", "description": "User operations"},
        {"name": "items", "description": "Item operations"},
    ],
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,  # Hide schemas section
        "docExpansion": "none",
        "displayRequestDuration": True,
        "filter": True,
        "syntaxHighlight.theme": "monokai",
    },
)
```

Swagger UI parameters: `deepLinking`, `defaultModelRendering`, `displayOperationId`, `showExtensions`, `showCommonExtensions`, `tryItOutEnabled`, `persistAuthorization`. You can also serve custom Swagger UI HTML:

```python
from fastapi.openapi.docs import get_swagger_ui_html

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Custom Docs",
        swagger_favicon_url="/static/favicon.ico",
    )
```

Customize ReDoc similarly with `get_redoc_html()`.

## Q71: How do you manage secrets and configuration in FastAPI?
**A:** Configuration management with Pydantic `Settings`:

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "My API"
    database_url: str
    redis_url: str = "redis://localhost:6379"
    secret_key: str
    allowed_hosts: list[str] = ["*"]
    debug: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()

@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {"app_name": settings.app_name}
```

`pydantic-settings` reads from: (1) environment variables, (2) `.env` file, (3) default values. Secret management: (1) use `secrets` module for API keys, (2) HashiCorp Vault, (3) AWS Secrets Manager / GCP Secret Manager, (4) Kubernetes secrets, (5) Docker secrets. Never hardcode secrets. Use `SecretStr` type (Pydantic) to prevent accidental logging. For production: use environment variables (injected by container orchestration), with `.env` only for development.

## Q72: How do you implement WebSocket rooms/channels in FastAPI?
**A:** WebSocket rooms organize connections into groups:

```python
class RoomManager:
    def __init__(self):
        self.rooms: dict[str, set[WebSocket]] = {}
    
    async def join_room(self, room: str, websocket: WebSocket):
        if room not in self.rooms:
            self.rooms[room] = set()
        self.rooms[room].add(websocket)
    
    async def leave_room(self, room: str, websocket: WebSocket):
        self.rooms[room].discard(websocket)
        if not self.rooms[room]:
            del self.rooms[room]
    
    async def broadcast_to_room(self, room: str, message: dict):
        for ws in self.rooms.get(room, set()):
            await ws.send_json(message)

manager = RoomManager()

@app.websocket("/chat/{room_id}")
async def chat_websocket(websocket: WebSocket, room_id: str):
    await websocket.accept()
    await manager.join_room(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast_to_room(room_id, {
                "user": data["user"],
                "message": data["message"],
                "room": room_id
            })
    except WebSocketDisconnect:
        await manager.leave_room(room_id, websocket)
        await manager.broadcast_to_room(room_id, {"system": f"{data['user']} left"})
```

For multi-server setups, use Redis pub/sub: each server subscribes to room channels. When a message is broadcast, publish to Redis; all servers receive and forward to local connections.

## Q73: Explain FastAPI's `Dependencies` with `yield` and `asyncio` context.
**A:** Async dependencies with `yield` for managing resources:

```python
async def get_db():
    async with AsyncSession(engine) as session:
        yield session

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(User.token == token))
    return user.scalar_one_or_none()

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

Context manager behavior: (1) `async with` for async context managers, (2) `try/finally` for sync context managers, (3) the `yield` point divides setup from teardown. Exceptions propagate through the dependency chain — if `get_current_user` raises, `get_db`'s cleanup still runs (the `async with` handles this). Multiple dependencies with `yield` teardown in reverse order. Background tasks don't run until after the response is sent, so dependencies with `yield` teardown happens after the response but before background tasks.

## Q74: How do you implement API key authentication in FastAPI?
**A:** API key authentication via header or query parameter:

```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader, APIKeyQuery

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
api_key_query = APIKeyQuery(name="api_key", auto_error=False)

async def verify_api_key(
    header_key: str | None = Security(api_key_header),
    query_key: str | None = Security(api_key_query),
):
    api_key = header_key or query_key
    if not api_key:
        raise HTTPException(401, "API key required")
    
    # Verify against database or cache
    key_data = await redis.get(f"apikey:{api_key}")
    if not key_data:
        raise HTTPException(403, "Invalid API key")
    
    return json.loads(key_data)

@app.get("/api/data")
async def get_data(api_key: ApiKey = Depends(verify_api_key)):
    return {"data": "sensitive", "tenant": api_key["tenant_id"]}
```

API key management: (1) generate with `secrets.token_urlsafe(32)`, (2) hash keys before storing (like passwords), (3) support key rotation, (4) track usage per key, (5) allow key revocation, (6) set expiration, (7) rate limit per key. Use `Security()` instead of `Depends()` for API key dependencies to show the security scheme in OpenAPI.

## Q75: What is FastAPI's `route` decorator parameters for operation IDs?
**A:** Operation ID customization:

```python
@app.get(
    "/users/{user_id}",
    operation_id="getUserById",  # Override auto-generated ID
    summary="Get a specific user",
    description="Retrieve user details including profile information",
    response_description="User details",
    deprecated=False,
    tags=["users"],
    include_in_schema=True,
)
async def get_user(user_id: int):
    return {"user_id": user_id}
```

Operation ID is used in OpenAPI and by code generators (OpenAPI Generator, `openapi-typescript`). Auto-generated: `{endpoint}_{path}_{method}`. Override for: (1) clean client SDK method names, (2) backward compatibility when renaming endpoints, (3) matching existing API conventions. The `operation_id` must be unique across the API. Other route parameters: `responses` (additional response models), `callbacks` (webhook definitions), `openapi_extra` (arbitrary OpenAPI fields).

## Q76: How do you implement data versioning in FastAPI?
**A:** Data versioning strategies for APIs:

```python
from pydantic import BaseModel
from datetime import datetime

class UserV1(BaseModel):
    id: int
    name: str

class UserV2(UserV1):
    email: str | None = None
    phone: str | None = None

@app.get("/v1/users/{user_id}", response_model=UserV1)
async def get_user_v1(user_id: int):
    user = get_user(user_id)
    return user  # Extra fields are stripped

@app.get("/v2/users/{user_id}", response_model=UserV2)
async def get_user_v2(user_id: int):
    user = get_user(user_id)
    return user
```

Database versioning: (1) add `version` column (integer, auto-increment), (2) implement optimistic locking (check version on update), (3) maintain event log for audit. Schema evolution: (1) additive changes only (don't remove columns), (2) nullable new fields, (3) use `response_model_exclude_unset=True` for gradual rollout. Long-term: maintain multiple API versions with deprecation timeline. Use content negotiation (`Accept: application/vnd.api+json;version=2`) for cleaner versioning.

## Q77: Explain FastAPI's `json` module configuration and performance.
**A:** FastAPI uses Python's `json` module by default. Performance optimization:

```python
import orjson
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(default_response_class=ORJSONResponse)

# Or for more control:
class FastORJSONResponse(ORJSONResponse):
    def render(self, content: Any) -> bytes:
        return orjson.dumps(
            content,
            option=orjson.OPT_UTC_Z | orjson.OPT_SERIALIZE_DATACLASS,
            default=str,
        )
```

`orjson` is 2-3x faster than standard `json` for serialization, and 4-5x faster for deserialization. `ujson` is another option. For Pydantic models, Pydantic V2 uses Rust-based `pydantic-core` internally, which is significantly faster than V1. Response serialization: (1) Pydantic model → dict, (2) dict → JSON. Optimizations: (1) pre-serialize cached responses, (2) use `__slots__` on dataclasses, (3) avoid unnecessary serialization cycles. For large responses, consider streaming or pagination.

## Q78: How do you implement database read/write splitting in FastAPI?
**A:** CQRS pattern with separate read/write databases:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

write_engine = create_engine(WRITE_DATABASE_URL, pool_size=20)
read_engine = create_engine(READ_DATABASE_URL, pool_size=40, echo=True)

WriteSession = sessionmaker(bind=write_engine)
ReadSession = sessionmaker(bind=read_engine)

def get_write_db():
    db = WriteSession()
    try:
        yield db
    finally:
        db.close()

def get_read_db():
    db = ReadSession()
    try:
        yield db
    finally:
        db.close()

@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_write_db)):
    db.add(User(**user.model_dump()))
    db.commit()
    return user

@app.get("/users")
def list_users(db: Session = Depends(get_read_db)):
    return db.query(User).all()
```

Replication lag: (1) use read-after-write consistency for critical reads (route to write DB), (2) use `db.commit()` and then read from replica after a short delay, (3) use `SELECT ... FOR UPDATE` on write DBs. For async with SQLAlchemy, create separate async engines. For ORM-level routing, use SQLAlchemy's `RoutingSession` or libraries like `sqlalchemy-replica`.

## Q79: What are FastAPI's exception handlers for integrated error monitoring?
**A:** Integrate with error monitoring services (Sentry, Datadog):

```python
import sentry_sdk
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="https://...",
    integrations=[
        StarletteIntegration(),
        FastApiIntegration(),
    ],
    traces_sample_rate=1.0,
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Sentry captures automatically via integration
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error_id": str(uuid.uuid4())},
    )
```

Custom error tracking:

```python
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code >= 500:
        logger.error(f"Server error: {exc.detail}", exc_info=exc)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
```

Monitoring: (1) log all errors with structure, (2) send 5xx errors to APM tools, (3) track error rates and patterns, (4) set up alerts for error spikes, (5) include correlation IDs, (6) sanitize PII from error logs. For async error monitoring, ensure integrations support asyncio.

## Q80: How do you implement database partitioning with FastAPI?
**A:** Database partitioning splits large tables for performance. PostgreSQL declarative partitioning:

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = {
        'postgresql_partition_by': 'RANGE (created_at)'
    }
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    amount = Column(Integer)
    created_at = Column(DateTime, nullable=False)

# Create partitions manually:
# CREATE TABLE orders_2024_01 PARTITION OF orders
# FOR VALUES FROM ('2024-01-01') TO ('2024-02-01')
```

Application-level partitioning: (1) shard by tenant ID (separate databases/schemas), (2) time-based table rotation (logs, events), (3) hash-based partitioning (user ID). FastAPI with partitioning: (1) route queries to appropriate partition (time ranges, tenant IDs), (2) manage partition creation in Alembic migrations, (3) use PostgreSQL's partition pruning for query efficiency. Consider using `pg_partman` for automated partition management. For sharding, use database proxy (MaxScale, pgpool-II) or application-level routing.

## Q81: Explain FastAPI's `docs_url`, `redoc_url`, and `openapi_url` configuration.
**A:** These parameters control OpenAPI and documentation URLs:

```python
app = FastAPI(
    docs_url="/api/docs",           # Swagger UI (None to disable)
    redoc_url="/api/redoc",          # ReDoc (None to disable)
    openapi_url="/api/openapi.json", # OpenAPI schema (None to disable)
    swagger_ui_oauth2_redirect_url="/api/docs/oauth2-redirect",
)
```

Disabling docs in production: `docs_url=None, redoc_url=None`. Hiding the OpenAPI schema: `openapi_url=None`. Best practice: (1) enable docs in staging/development, (2) disable or protect with auth in production, (3) serve docs behind VPN or SSO. For internal APIs, document via version-controlled API specifications (Stoplight, Postman collections) instead of live docs. The `swagger_ui_oauth2_redirect_url` is needed when using OAuth2 flows in Swagger UI.

## Q82: How do you implement database connection retry in FastAPI?
**A:** Automatic retry for database connection failures:

```python
from tenacity import retry, stop_after_attempt, wait_exponential
from sqlalchemy.exc import OperationalError

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry_error_callback=lambda retry_state: None,
)
def get_db_connection():
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    return engine.connect()

# Async retry
from asyncio import sleep

async def get_async_db():
    for attempt in range(3):
        try:
            engine = create_async_engine(ASYNC_DATABASE_URL)
            async with engine.connect() as conn:
                yield conn
                return
        except OperationalError:
            if attempt == 2:
                raise
            await sleep(2 ** attempt)
```

`pool_pre_ping=True` in SQLAlchemy checks connection health before use (reduces stale connection errors). For connection timeouts, set `pool_timeout` and `pool_recycle`. For PostgreSQL, configure `statement_timeout` and `lock_timeout` at the connection level. Retry only transient errors (connection lost, timeout), not syntax/logic errors. Use exponential backoff with jitter to avoid thundering herd.

## Q83: What are FastAPI's hooks for request validation customization?
**A:** Custom request validation via dependency injection and middleware:

```python
from fastapi import Request, HTTPException
from fastapi.routing import APIRoute

class CustomValidationRoute(APIRoute):
    def get_route_handler(self):
        original_handler = super().get_route_handler()
        async def custom_handler(request: Request):
            # Pre-validation
            if request.method == "POST":
                body = await request.json()
                if "password" in body and len(body["password"]) < 8:
                    raise HTTPException(422, "Password too short")
            
            response = await original_handler(request)
            return response
        return custom_handler

app = FastAPI(route_class=CustomValidationRoute)
```

Alternative: middleware-based validation:

```python
@app.middleware("http")
async def validate_request(request: Request, call_next):
    if request.url.path.startswith("/api/"):
        if request.method in ("POST", "PUT", "PATCH"):
            body = await request.json()
            # Custom validation logic
    return await call_next(request)
```

For field-level custom validation: Pydantic validators (`@field_validator`, `@model_validator`). For complex business rules: use dependency injection (validate in dependencies before route handler runs). For XML/CSV body validation: parse in middleware or dependency, wrap in Pydantic model.

## Q84: How do you implement database full-text search in FastAPI?
**A:** PostgreSQL full-text search integration:

```python
from sqlalchemy import func, Column, Integer, String, TSVECTOR

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    search_vector = Column(TSVECTOR)

# Create GIN index: CREATE INDEX article_search_idx ON articles USING GIN(search_vector)

@app.get("/search")
def search_articles(q: str, db: Session = Depends(get_db)):
    query = db.query(Article).filter(
        Article.search_vector.op("@@")(func.plainto_tsquery("english", q))
    ).order_by(
        func.ts_rank(Article.search_vector, func.plainto_tsquery("english", q)).desc()
    )
    return query.all()
```

For Elasticsearch integration:

```python
from elasticsearch import AsyncElasticsearch

es = AsyncElasticsearch(["http://localhost:9200"])

@app.get("/search")
async def search(q: str):
    result = await es.search(
        index="articles",
        body={"query": {"multi_match": {"query": q, "fields": ["title^2", "content"]}}}
    )
    return result["hits"]["hits"]
```

Full-text search strategies: (1) PostgreSQL `tsvector` (good for small-medium datasets, no extra infrastructure), (2) Elasticsearch/OpenSearch (distributed, advanced scoring, faceted search), (3) Meilisearch (simple, fast), (4) SQLite FTS5 (embedded, lightweight). Considerations: (1) relevance scoring, (2) typo tolerance, (3) stemming/lemmatization, (4) highlighting, (5) filtering/aggregation, (6) indexing strategy (batch vs real-time).

## Q85: Explain FastAPI's `middleware` for production security headers.
**A:** Security headers middleware:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
        return response

app.add_middleware(SecurityHeadersMiddleware)
```

Security header descriptions: (1) `X-Content-Type-Options` — prevent MIME sniffing, (2) `X-Frame-Options` — prevent clickjacking, (3) `Strict-Transport-Security` — enforce HTTPS, (4) `Content-Security-Policy` — prevent XSS (most important), (5) `Referrer-Policy` — control referrer info, (6) `Permissions-Policy` — control browser features. The OWASP Secure Headers Project provides recommended configurations. For APIs, CSP is less critical (no HTML rendering) but HSTS and X-Content-Type-Options are essential.

## Q86: How do you implement database migration testing in FastAPI?
**A:** Test migrations with Alembic:

```python
import pytest
from alembic.config import Config
from alembic.command import upgrade, downgrade
from sqlalchemy import create_engine

def test_migration_upgrade_downgrade():
    engine = create_engine("sqlite:///:memory:")
    
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", "sqlite:///:memory:")
    
    # Upgrade to latest
    upgrade(alembic_cfg, "head")
    
    # Verify schema
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "users" in tables
    
    # Downgrade to base
    downgrade(alembic_cfg, "base")
    
    # Verify tables are gone
    inspector = inspect(engine)
    assert "users" not in inspector.get_table_names()

def test_migration_data_preservation():
    # Test that data migrations preserve/transform data correctly
    pass
```

Best practices: (1) test both upgrade and downgrade, (2) test data migration (rows are transformed correctly), (3) test with production-like data volume, (4) test concurrent migrations, (5) test migration from different baseline versions, (6) include migration tests in CI pipeline. Use `pytest-alembic` plugin for comprehensive migration testing. Always test migrations against a copy of production data before deploying.

## Q87: What are FastAPI's `router` specific configurations and customizations?
**APIRouter** supports many of the same configurations as the main app:

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(admin_only)],
    responses={404: {"description": "Not found"}},
    default_response_class=ORJSONResponse,
    route_class=TimedRoute,
    deprecated=False,
    include_in_schema=True,
)
```

Router-level settings: (1) `prefix` — all routes are relative to this, (2) `tags` — OpenAPI grouping, (3) `dependencies` — applied to all routes in the router, (4) `responses` — shared response schemas, (5) `default_response_class` — serialization format, (6) `route_class` — custom route behavior. Routers can include other routers (`router.include_router(sub_router)`). Each router can have its own `lifespan` context. Routers support `on_event` (deprecated) for startup/shutdown callbacks.

## Q88: How do you implement distributed tracing in FastAPI?
**A:** OpenTelemetry integration for distributed tracing:

```python
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
trace.set_tracer_provider(provider)

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

# Manual instrumentation
from opentelemetry import trace

@app.get("/users/{user_id}")
async def get_user(user_id: int, tracer: trace.Tracer = Depends(get_tracer)):
    with tracer.start_as_current_span("get_user") as span:
        span.set_attribute("user.id", user_id)
        user = await fetch_user(user_id)
        span.set_attribute("user.found", user is not None)
        return user
```

Tracing with `opentelemetry-instrumentation` auto-instruments: FastAPI, SQLAlchemy, HTTPX, Redis, and more. Trace context propagates via HTTP headers (`traceparent`, `tracestate`). For Jaeger/Zipkin: use their exporters. For Datadog: use `dd-trace-py`. For Sentry: enable tracing in Sentry SDK. Best practices: (1) trace all external calls (DB, cache, external API), (2) add business-relevant span attributes, (3) sample appropriately in production, (4) trace error paths thoroughly.

## Q89: Explain FastAPI's `request.state` and `app.state` lifecycle.
**A:** `request.state` is request-scoped (per-request), `app.state` is application-scoped (lives for app lifetime). `request.state` is populated by middleware and dependencies:

```python
@app.middleware("http")
async def set_request_state(request: Request, call_next):
    request.state.start_time = time.time()
    request.state.user = None
    request.state.correlation_id = str(uuid.uuid4())
    return await call_next(request)

@app.get("/")
async def root(request: Request):
    duration = time.time() - request.state.start_time
    return {"correlation_id": request.state.correlation_id, "duration": duration}
```

Lifecycle: `request.state` is created per request, accessible in middleware, dependencies, and route handlers. Not persisted across requests. For async context, use `contextvars` instead of `request.state` when you need to access request data outside of request scope (e.g., in background tasks, logging). `app.state` is initialized in lifespan, should be read-only after startup for thread safety.

## Q90: How do you implement database replication and failover in FastAPI?
**A:** High-availability database configuration:

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

# Primary
primary_engine = create_engine(PRIMARY_URL, pool_size=20, pool_pre_ping=True)
# Replicas
replica_engines = [
    create_engine(url, pool_size=10, pool_pre_ping=True)
    for url in REPLICA_URLS
]

def get_db():
    # Check primary health, failover if needed
    try:
        db = SessionLocal(bind=primary_engine)
        yield db
    except:
        # Fallback to replica for reads
        engine = random.choice(replica_engines)
        db = SessionLocal(bind=engine)
        yield db
    finally:
        db.close()
```

Automated failover: (1) use PostgreSQL `pg_auto_failover`, (2) Patroni + etcd/consul for HA, (3) cloud-managed DB (RDS Multi-AZ, Cloud SQL). Connection handling: (1) detect primary failure (pool_pre_ping, timeout), (2) redirect reads to replicas, (3) queue writes during failover, (4) retry with exponential backoff, (5) circuit breaker pattern to avoid overwhelming failing DB. For zero-downtime failover, use a connection pooler (PgBouncer, Pgpool-II) in front of the database.

## Q91: What are FastAPI's WebSocket event types and handling?
**A:** WebSocket events beyond basic text/binary:

```python
from fastapi import WebSocket, WebSocketDisconnect
import json

@app.websocket("/ws")
async def websocket_handler(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive various event types
            text = await websocket.receive_text()      # Text message
            # binary = await websocket.receive_bytes()  # Binary message
            # json_data = await websocket.receive_json()  # JSON message
            
            data = json.loads(text)
            event_type = data.get("type")
            
            if event_type == "ping":
                await websocket.send_json({"type": "pong"})
            elif event_type == "message":
                await broadcast_message(data["content"])
            elif event_type == "subscribe":
                await subscribe_channel(data["channel"])
            
    except WebSocketDisconnect:
        handle_disconnect()
    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})
```

WebSocket events: `receive_text()`, `receive_bytes()`, `receive_json()`. Send: `send_text()`, `send_bytes()`, `send_json()`. Connection states: `CONNECTING`, `CONNECTED`, `DISCONNECTED`. Use a `while True` loop with proper exception handling. Implement custom event types (ping/pong for heartbeat, subscribe/unsubscribe for channels). For large payloads, consider chunking or streaming. For binary protocols, define message format (length-prefixed, protobuf, msgpack).

## Q92: How do you implement database connection encryption (TLS) in FastAPI?
**A:** TLS connection to the database:

```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://user:password@host:5432/db",
    connect_args={
        "sslmode": "require",          # require, verify-ca, verify-full
        "sslrootcert": "/path/to/ca.pem",
        "sslcert": "/path/to/client-cert.pem",
        "sslkey": "/path/to/client-key.pem",
    }
)

# For async
engine = create_async_engine(
    "postgresql+asyncpg://user:password@host:5432/db",
    connect_args={
        "ssl": "require",
    }
)
```

SSL modes: (1) `disable` — no encryption, (2) `allow` — try encryption, not required, (3) `prefer` — prefer encryption, (4) `require` — enforce encryption, (5) `verify-ca` — require + verify server cert against CA, (6) `verify-full` — require + verify CA + verify hostname. Best practice: `verify-full` for production (prevents MITM). For cloud databases (RDS, Cloud SQL): download CA certificate bundle, set `sslrootcert`. Test SSL connection with `sslmode=verify-full`. For Redis SSL: `rediss://` URL scheme.

## Q93: Explain FastAPI's `route` `dependencies` parameter for global validation.
**A:** Router-level dependencies apply to all router endpoints:

```python
from fastapi import Depends, HTTPException, Header

async def verify_content_type(content_type: str = Header(...)):
    if "application/json" not in content_type:
        raise HTTPException(415, "Unsupported media type")

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(verify_content_type)],
)

@admin_router.get("/users")
async def list_users():  # Has verify_content_type applied
    return []

@admin_router.post("/users")
async def create_user():  # Has verify_content_type applied
    return []
```

Dependencies at router level are applied automatically to all routes within that router. At the app level: `app = FastAPI(dependencies=[Depends(global_dep)])`. At the route level: `@router.get("/", dependencies=[Depends(route_dep)])`. Order: route-level → router-level → app-level dependencies all apply. Use router-level dependencies for: (1) auth requirements for an admin section, (2) rate limiting per feature group, (3) feature flags for beta features, (4) content type enforcement.

## Q94: How do you implement database change data capture (CDC) with FastAPI?
**A:** CDC captures database changes for event-driven architectures:

```python
# PostgreSQL logical replication via asyncpg + LISTEN/NOTIFY
import asyncpg

async def listen_for_changes():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.add_listener("table_changes", callback)
    
    # Create trigger in PostgreSQL:
    # CREATE OR REPLACE FUNCTION notify_change()
    # RETURNS trigger AS $$
    # BEGIN
    #   PERFORM pg_notify('table_changes', row_to_json(NEW)::text);
    #   RETURN NEW;
    # END;
    # $$ LANGUAGE plpgsql;
    
    # CREATE TRIGGER users_change
    # AFTER INSERT OR UPDATE OR DELETE ON users
    # FOR EACH ROW EXECUTE FUNCTION notify_change();

@asynccontextmanager
async def lifespan(app):
    task = asyncio.create_task(listen_for_changes())
    yield
    task.cancel()
```

Alternative approaches: (1) Debezium + Kafka — captures changes from DB transaction logs (no trigger overhead), (2) outbox pattern — write events to an `outbox` table, poll in background and publish to message broker, (3) `django-events` / SQLAlchemy event listeners. CDC enables: (1) real-time search indexing, (2) cache invalidation, (3) event-sourced architectures, (4) cross-service data synchronization.

## Q95: What are FastAPI's server event hooks for graceful shutdown?
**A:** Graceful shutdown hooks:

```python
import asyncio, signal

@asynccontextmanager
async def lifespan(app):
    # Startup
    app.state.shutdown_event = asyncio.Event()
    yield
    # Shutdown
    app.state.shutdown_event.set()
    await asyncio.sleep(5)  # Allow in-flight requests to complete
    await cleanup_resources()

# Or with uvicorn hooks:
class CustomServer:
    async def handle_sigterm(self):
        logger.info("Received SIGTERM, shutting down gracefully...")
        await asyncio.sleep(5)
        await super().handle_sigterm()
```

For production: (1) register `SIGTERM` and `SIGINT` handlers, (2) stop accepting new requests (drain connections), (3) wait for in-flight requests (configurable timeout, default 30s), (4) close database pools, (5) cancel background tasks, (6) close cache connections. Uvicorn's graceful shutdown: sends `SIGTERM`, waits for `--timeout-graceful-shutdown` (default: None, no timeout). For Kubernetes: configure `preStop` hook and `terminationGracePeriodSeconds`. For async: use `asyncio.shield()` for critical cleanup that shouldn't be interrupted.

## Q96: How do you implement database pool sizing and monitoring in FastAPI?
**A:** Connection pool optimization:

```python
from sqlalchemy import create_engine, event

engine = create_engine(
    DATABASE_URL,
    pool_size=10,           # Base pool connections
    max_overflow=20,         # Additional connections allowed
    pool_timeout=30,         # Seconds before timeout waiting for connection
    pool_recycle=3600,       # Recycle connections (prevent stale connections)
    pool_pre_ping=True,      # Check connection before use
    pool_use_lifo=False,     # LIFO vs FIFO (LIFO reduces age of idle connections)
)

# Pool stats endpoint
@app.get("/debug/pool")
def pool_stats():
    return {
        "size": engine.pool.size(),
        "checked_in": engine.pool.checkedin(),
        "checked_out": engine.pool.checkedout(),
        "overflow": engine.pool.overflow(),
    }
```

Pool sizing formula: `connections = (max_workers * (db_time / total_time)) + spares`. For async SQLAlchemy, use `AsyncAdaptedQueuePool`. Monitoring: (1) track pool utilization (active connections / pool size), (2) set alert for pool exhaustion (pool_timeout errors), (3) monitor connection age (reconnect before database timeout), (4) watch for connection leaks (steadily increasing checked_out), (5) for PostgreSQL: monitor `pg_stat_activity` for idle-in-transaction connections.

## Q97: Explain FastAPI's `JSON` encoding custom types.
**A:** Custom JSON encoding for non-standard types:

```python
from fastapi import FastAPI
from pydantic import BaseModel
from decimal import Decimal
from datetime import date
import json

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

app = FastAPI()

@app.get("/custom")
def custom_type():
    return {"price": Decimal("19.99"), "date": date.today()}
# ORJSON handles these natively
```

Pydantic V2 handles: Decimal (as float by default), datetime (ISO 8601), UUID (string), bytes (base64), Enum (value), set (sorted list). Custom types in Pydantic:

```python
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

class MyCustomType:
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v):
        return MyCustomType(v)
```

Register custom encoder with FastAPI: `app = FastAPI(json_encoders={Decimal: str})`. For `orjson`, use `option=orjson.OPT_SERIALIZE_NUMPY` for numpy types.

## Q98: How do you implement async task scheduling in FastAPI?
**A:** Background task scheduling (beyond `BackgroundTasks`):

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app):
    scheduler.add_job(clean_expired_sessions, "interval", hours=1)
    scheduler.add_job(sync_external_data, "cron", hour=3, minute=0)
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)

async def clean_expired_sessions():
    async with AsyncSession(engine) as session:
        await session.execute(delete(Session).where(Session.expires_at < datetime.utcnow()))
        await session.commit()

async def sync_external_data():
    # Long-running scheduled task
    pass
```

Task scheduling options: (1) **APScheduler** — flexible, supports cron/interval/date triggers, (2) **Celery beat** — distributed, requires Redis/DB, (3) **Arq** — Redis-based, lightweight async scheduler, (4) **Huey** — Redis-backed, simple. For distributed scheduling: (1) use Redis locking to prevent duplicate execution, (2) use Celery beat with shared scheduler, (3) run scheduler as a separate service. Monitor scheduled tasks (execution time, failures, next run). For simple interval tasks: `asyncio.create_task` with `while True` loop.

## Q99: What are FastAPI's customization points for OpenAPI schema groups?
**A:** Customize OpenAPI tag groups and endpoint organization:

```python
app = FastAPI(
    openapi_tags=[
        {
            "name": "users",
            "description": "User management endpoints",
            "externalDocs": {
                "description": "User docs",
                "url": "https://docs.example.com/users"
            }
        },
        {
            "name": "admin",
            "description": "Admin-only operations",
        },
    ]
)

# Group endpoints by tag
@router.get("/users", tags=["users"], operation_id="listUsers")
async def list_users(): ...

@router.post("/users/{user_id}/disable", tags=["admin"], operation_id="disableUser")
async def disable_user(user_id: int): ...
```

OpenAPI tags can have: `name`, `description`, `externalDocs`. Tags order in the array determines display order in Swagger UI. Endpoints can have multiple tags (appears in multiple groups). For advanced grouping, use `x-tagGroups` vendor extension:

```python
openapi_schema["x-tagGroups"] = [
    {"name": "User Management", "tags": ["users", "profiles"]},
    {"name": "Administration", "tags": ["admin", "audit"]},
]
```

This collapses tagged endpoints into named groups in Swagger UI.

## Q100: How do you implement end-to-end encryption in FastAPI?
**A:** E2E encryption ensures data is encrypted on the client before reaching the server:

```python
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.fernet import Fernet
import base64

# Client-side (pseudo-code):
# const encrypted = await encryptWithPublicKey(data, serverPublicKey)
# await fetch('/api/sensitive', { body: encrypted })

# Server stores encrypted data (never decrypted server-side)
@app.post("/api/e2e-data")
async def store_e2e_data(
    encrypted_payload: str,
    user: User = Depends(get_current_user)
):
    # Store encrypted data — server cannot read it
    await db.execute(
        insert(UserData).values(
            user_id=user.id,
            encrypted_content=encrypted_payload,
        )
    )
    return {"status": "stored"}

# For search: use encrypted search schemes
# For sharing: use key encapsulation
```

E2E encryption considerations: (1) key management is the hardest part (key exchange, recovery, rotation), (2) not all features work with E2E (search, sort, analytics), (3) metadata (subject lines, timestamps) may leak information, (4) client-side crypto requires secure random number generation, (5) web crypto API (`SubtleCrypto`) for browser-side encryption, (6) hybrid encryption (asymmetric for key exchange, symmetric for payload). Common patterns: (1) Signal Protocol (messaging), (2) MLS (Messaging Layer Security), (3) NaCl/libsodium for simpler needs.
