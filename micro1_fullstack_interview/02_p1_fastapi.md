# Priority 1 — FastAPI (Q41–Q78)

**Why these matter for micro1:** FastAPI is explicitly in the role's requirements. Expect: fundamentals → Pydantic validation → dependencies → middleware → architecture → testing. micro1 drills on async behavior, dependency injection, and production structure.

---

## Q41: What is FastAPI?

A modern, high-performance **Python web framework** for building APIs, built on **Starlette** (ASGI server layer) and **Pydantic** (data validation). Key characteristics:

- **Async-native** (ASGI) — supports `async def` endpoints and high concurrency (Uvicorn).
- **Automatic interactive docs** — Swagger UI (`/docs`) and ReDoc (`/redoc`) generated from type hints.
- **Type-hint driven** — request validation, serialization, and dependency injection from Python type annotations.
- **Data validation** with Pydantic models.
- OpenAPI-compliant schemas generated automatically.
- Zero-boilerplate: edit code → reload with `uvicorn app:app --reload`.

---

## Q42: Why would you choose FastAPI over Flask or Django?

| | **Flask** | **Django** | **FastAPI** |
|---|---|---|---|
| Type | Microframework | Full-stack MVC | API-first microframework |
| Async | No (sync WSGI; Flask 2 has some) | Limited | Native ASGI async |
| Validation | Manual | Serializers | Pydantic (automatic) |
| OpenAPI docs | Manual | Manual | Automatic |
| Dependencies | No built-in | Limited | First-class DI (`Depends`) |
| Batteries | Minimal | ORM, admin, auth, migrations | Minimal (bring your own) |
| Performance | Moderate | Heavier | High (Starlette/Uvicorn) |
| Best for | Small apps, maximum flexibility | Big CRUD apps with admin | High-concurrency APIs + ML/AI backends |

**For micro1:** FastAPI fits their stack (async Python, LLM integrations, high-concurrency APIs). Django wins when you need the full admin/batteries; Flask when you want minimalism and sync simplicity.

---

## Q43: What are the advantages of FastAPI?

1. **High performance** — comparable to NodeJS/Go in benchmarks (Uvicorn + async).
2. **Automatic validation + serialization** via Pydantic (declarative, type-safe).
3. **Automatic interactive docs** (Swagger/ReDoc + OpenAPI).
4. **Async support** for I/O-bound concurrency (WebSockets, streaming, external APIs, LLMs).
5. **Dependency injection** built-in — clean, testable, reusable logic.
6. **Type hints everywhere** — editor autocomplete, static checking, self-documenting.
7. **Fast development** — minimal boilerplate, `--reload` for dev.
8. **Testable** — `TestClient` (Starlette) + httpx-based `AsyncClient`.
9. **Standard-based** — OpenAPI, JSON Schema, ASGI; broad ecosystem compatibility.

---

## Q44: How do you create a basic FastAPI application?

```python
from fastapi import FastAPI

app = FastAPI(title="Example API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Hello"}
```

Run: `uvicorn main:app --reload --port 8000`

- `app = FastAPI(...)` — configurable (title, docs URLs, middleware, lifespan).
- `@app.get("/path")` — route decorators; functions can be `def` (sync) or `async def`.
- Return value is auto-serialized to JSON by FastAPI's response model logic.
- Docs at `http://localhost:8000/docs`.

---

## Q45: How do you define GET, POST, PUT, PATCH, and DELETE endpoints?

```python
@app.get("/users/{user_id}")        # read
def get_user(user_id: int): ...

@app.post("/users", status_code=201) # create
def create_user(payload: UserCreate): ...

@app.put("/users/{user_id}")         # full replace
def update_user(user_id: int, payload: UserUpdate): ...

@app.patch("/users/{user_id}")       # partial update
def patch_user(user_id: int, payload: UserPatch): ...

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int): ...
```

- REST semantics: `POST` create, `PUT` idempotent full replace, `PATCH` partial, `DELETE` remove.
- Same path with different methods is fine.
- Path ops also accept `tags=`, `summary=`, `responses={...}` for OpenAPI documentation.

---

## Q46: What is Pydantic?

The **data validation and settings library** used by FastAPI. You declare data models as Python classes with type annotations; Pydantic:

- Validates input at runtime.
- Coerces types (e.g., `"123"` → `123` for `int`).
- Serializes objects to/from JSON (v2 uses Rust-based `pydantic-core`).
- Generates JSON Schema (used for OpenAPI).
- Also powers `BaseSettings` for config management.

**v2 notes:** models inherit from `BaseModel`; use `model_validate()`/`model_dump()` (replacing v1's `parse_obj()`/`dict()`); serialization via `model_dump_json()`. Validation is ~50x faster than v1 thanks to the Rust core.

---

## Q47: How does Pydantic validation work?

1. When you instantiate `Model(**data)`, Pydantic:
   - Parses/coerces fields to declared types (`str`, `int`, `EmailStr`, nested models, `datetime`, etc.).
   - Runs field-level **validators** (`@field_validator`) and model-level validators (`@model_validator`).
   - Applies constraints (`Field(gt=0, max_length=50)`, `conint`, `SecretStr`, etc.).
2. On failure it raises `ValidationError` with structured error list (FastAPI converts to **422 Unprocessable Entity**).
3. Extra fields are **ignored** by default (`model_config = ConfigDict(extra="forbid")` to reject).

```python
from pydantic import BaseModel, Field, field_validator

class User(BaseModel):
    email: str
    age: int = Field(ge=0, le=150)

    @field_validator("email")
    @classmethod
    def check_email(cls, v):
        if "@" not in v: raise ValueError("invalid email")
        return v
```

- Validators: `@field_validator` (per field), `@model_validator` (whole model, `mode="before"/"after"`).
- `mode="before"` runs on raw input (good for normalizing), `mode="after"` on validated values.
- v2 uses **validator decorators on class methods** with `@classmethod` (or `@staticmethod`).

---

## Q48: What is a Pydantic model?

A class inheriting `BaseModel` that declares typed fields and validation rules — it's the blueprint for structured data in/out of the API.

```python
from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    price: float
    tags: list[str] = []
```

- Used as **request bodies** (FastAPI validates incoming JSON), **response models**, nested schemas, config objects.
- Supports inheritance (`class ItemCreate(Item)`), generics, computed fields, aliases, `model_config` options.
- Nested models validate recursively: `class Order(BaseModel): items: list[Item]`.

---

## Q49: How do you validate request data in FastAPI?

You don't write manual validation — you **declare types**, and FastAPI validates automatically:

- **Path params:** `user_id: int` (else → 422).
- **Query params:** `q: str = Query(min_length=3, max_length=50)`.
- **Body:** `payload: UserCreate` (Pydantic).
- **Headers:** `x_token: str = Header(...)`.
- **Cookies:** `session_id: str = Cookie()`.
- **Path/Query constraints:** `Path(gt=0)`, `Query(ge=1, le=100)`.

Invalid data → automatic `422 Unprocessable Entity` with a structured error body. You can customize by adding your own validators inside Pydantic models (Q47).

---

## Q50: What is the difference between path parameters and query parameters?

- **Path parameters:** part of the URL path, used to identify a resource. `GET /users/42`.
  - Declared inside `{braces}`; strongly typed; order in the function args doesn't matter.
  - Required by nature (a path without it is a different route).
- **Query parameters:** after `?`, optional key=value pairs, used for filters/options. `GET /users?page=2&limit=50`.
  - Declared as function params with defaults; **optional unless given a required type without default**.

```python
@app.get("/users/{user_id}")
def get(user_id: int, include_details: bool = False, page: int = 1):
    ...
```

- Rule of thumb: **path** = what resource; **query** = how to shape the response.

---

## Q51: How do you define a request body in FastAPI?

Declare a parameter whose type is a Pydantic model (or a list of them) — FastAPI parses the JSON body into it.

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
def create(item: Item):          # body → validated Item
    return item
```

- Multiple body params: `def f(item: Item, user: User)` → each is a top-level body field.
- Embed: `body: Item = Body(embed=True)` → expects `{"item": {...}}`.
- Raw body: `payload: bytes = Body()`, or use `Request` for full access.
- `str`, `int`, `dict`, lists of models (`list[Item]`) all work as bodies.

---

## Q52: What is a response model?

The declared Pydantic model FastAPI uses to **validate, filter, and serialize** what your endpoint returns.

```python
class UserOut(BaseModel):
    id: int
    email: str

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    user = {"id": 1, "email": "a@b.c", "password": "secret"}  # extra keys dropped
    return user
```

- Extra fields in the returned data are **stripped** by default (`response_model_exclude_unset` etc. to tune).
- Responses are coerced into the model (e.g., datetime serialization).
- Can use `response_model=dict[str, UserOut]` or `list[UserOut]`.

---

## Q53: Why should you use response models?

1. **API contract** — clients see exactly what's documented (OpenAPI generates schemas).
2. **Security** — prevents leaking internal fields (passwords, hashes, secrets) that exist in DB/ORM objects.
3. **Type safety & autocompletion** for consumers and tests.
4. **Consistent serialization** (datetimes, enums, decimals) and stable output shapes.
5. **Documentation accuracy** — `/docs` shows real response schemas.
6. **Validation of output** — catches bugs where code returns wrong shape.

> Rule: never return ORM/DB objects directly; always map to a response model.

---

## Q54: How do you return different HTTP status codes from FastAPI?

```python
from fastapi import FastAPI, status, HTTPException

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create(item: Item): ...

# dynamic:
@app.get("/x")
def x(ok: bool):
    if not ok:
        raise HTTPException(status_code=404, detail="Not found")
    return JSONResponse(content={...}, status_code=200)

# custom:
from fastapi.responses import Response
@app.post("/items")
def create(item: Item, response: Response):
    response.status_code = status.HTTP_201_CREATED
    return item
```

- Set `status_code=` in the decorator (default 200, POST default 201 not automatic — set explicitly).
- `Response.status_code` for dynamic cases.
- Raise `HTTPException` for error paths; register custom exception handlers for others (Q56).
- Response classes: `JSONResponse`, `PlainTextResponse`, `HTMLResponse`, `StreamingResponse`, `FileResponse`, `RedirectResponse`.

---

## Q55: How do you handle exceptions in FastAPI?

Three layers, most to least granular:

1. **`HTTPException`** (raise in code) — returns JSON `{"detail": ...}` with chosen status.
2. **Exception handlers** — `@app.exception_handler(SomeError)` for custom exception types or e.g. `ValueError`.
3. **Global defaults** — unhandled errors → `500` (with `debug=False`, detail hidden).

```python
from fastapi import HTTPException

@app.get("/items/{id}")
def get_item(id: int):
    item = db.get(id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

- Custom handler example: `@app.exception_handler(CustomError)` returning a JSONResponse.
- For `ValidationError`/422, customize via a handler for `RequestValidationError`.
- Never leak stack traces; log full errors, return sanitized messages (Q77).

---

## Q56: How do you create custom exceptions?

Define your own exception class and register a handler; raising it returns a clean, consistent response.

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class OutOfStockError(Exception):
    def __init__(self, sku: str):
        self.sku = sku

app = FastAPI()

@app.exception_handler(OutOfStockError)
async def out_of_stock_handler(request: Request, exc: OutOfStockError):
    return JSONResponse(status_code=409,
                        content={"error": "out_of_stock", "sku": exc.sku})

@app.post("/order")
def order(...):
    if not in_stock(sku): raise OutOfStockError(sku)
```

- Raise anywhere (services too), handle centrally.
- Common pattern: a base `AppError` with code + status + detail for a consistent error envelope (see Q77).

---

## Q57: What is `HTTPException`?

FastAPI's built-in exception for returning an HTTP error with a JSON body:

```python
raise HTTPException(status_code=401, detail="Not authenticated", headers={"WWW-Authenticate": "Bearer"})
```

- `detail` can be a string or structured data (dict/list) — serialized into `{"detail": ...}`.
- `headers` adds response headers (e.g., for auth challenges).
- It's the idiomatic way to fail with 4xx/5xx inside endpoints.
- Difference from `raise` + handler: `HTTPException` is FastAPI-specific and produces a standardized body; custom handlers give you full control of the envelope.

---

## Q58: What is dependency injection in FastAPI?

A pattern where functions/endpoints **declare what they need** as parameters, and FastAPI provides them automatically — instead of constructing dependencies manually inside each endpoint.

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

- `Depends(get_db)` tells FastAPI: call `get_db()`, pass the result as `db`.
- Dependencies can themselves depend on other dependencies (nesting) — FastAPI builds the graph.
- Caching: `Depends(x)` with the same dependency in one request is called once (cached per-request) unless `use_cache=False`.
- Lifecycle via `yield` (setup → yield value → teardown in `finally`), which supports the exit after the response.

---

## Q59: How does `Depends()` work?

1. At route registration, FastAPI inspects parameters; ones with `Depends(...)` are dependencies.
2. When a request arrives, FastAPI **resolves the dependency graph**: calls each dependency function, injecting its own dependencies recursively.
3. Results are passed to the endpoint.
4. If a dependency uses `yield`, teardown runs after the response completes.
5. Dependencies that raise `HTTPException` short-circuit with that error; they can also override (e.g., the `Depends` returning a 401).

```python
async def require_user(authorization: str = Header(...)):
    user = await verify_token(authorization)
    if not user: raise HTTPException(401)
    return user

@app.get("/me")
def me(user: User = Depends(require_user)):
    return user
```

---

## Q60: What are common use cases for FastAPI dependencies?

1. **Database sessions** — create/close per request (Q61).
2. **Authentication/authorization** — verify tokens, inject current user (Q62).
3. **Shared service objects** — HTTP clients, repositories, caches (Redis client).
4. **Configuration/settings** — inject validated settings.
5. **Validation/coercion** — parse auth headers, pagination params.
6. **Rate limiting** — check usage counters.
7. **Request context** — current user/tenant for downstream services.
8. **Logging/metrics** — instrument request flows.
9. **Permissions/roles** — guard routes via composed dependencies.
10. **Testing overrides** — swap real deps for mocks/fakes (`app.dependency_overrides`).

---

## Q61: How would you inject a database session into an endpoint?

Yield-based dependency guarantees the session closes after the request.

```python
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from .db import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

- **Per-request session**: one session per request (cheap; don't reuse across requests/threads).
- `finally: db.close()` prevents connection leaks (returns connection to pool).
- For async: use `async_sessionmaker` + `AsyncSession` (Q353).
- Tests: `app.dependency_overrides[get_db] = get_test_db`.

---

## Q62: How would you implement authentication using FastAPI dependencies?

```python
from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError

SECRET = settings.jwt_secret

def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing bearer token")
    token = authorization.removeprefix("Bearer ")
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        user_id = payload["sub"]
    except JWTError:
        raise HTTPException(401, "Invalid token")
    return load_user(user_id)

@app.get("/me")
def me(user = Depends(get_current_user)):
    return user
```

- Pattern: a dependency that (a) extracts credentials, (b) verifies them, (c) raises `HTTPException(401/403)`, (d) returns the authenticated principal.
- Add a role check dependency: `RoleChecker("admin")` composed on top.
- Route-level: `dependencies=[Depends(get_current_user)]` on the decorator when the endpoint doesn't need the user object.
- Production: OAuth2 password flow (`OAuth2PasswordRequestForm`), refresh tokens, HTTP-only cookies, scopes (Q408–Q413).

---

## Q63: What is middleware?

A component that runs **for every request** before it reaches the route handler, and again **after** the response is generated — like a processing pipeline layer. Used for cross-cutting concerns.

```python
@app.middleware("http")
async def add_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)   # pass request down the stack
    response.headers["X-Process-Time"] = str(time.perf_counter() - start)
    return response
```

- Common uses: request logging, CORS, compression, auth (at the edge), rate limiting, request id injection, response headers.
- Runs for all paths including 404s.
- Middleware ordering matters; can be sync/async; must call `call_next(request)` exactly once per request.

---

## Q64: How does FastAPI middleware work?

1. **Registration:** `@app.middleware("http")` (or `app.add_middleware(SomeMiddleware, ...)`).
2. **Flow:** request → outer middleware → ... → route handler → response → back out through middleware (reverse order — like onion layers).
3. Each middleware wraps the next with `call_next(request)`.
4. On the way out it can modify headers/body (careful: body already streaming).

```python
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])
```

- Starlette provides `BaseHTTPMiddleware` for custom classes; FastAPI's decorator is sugar over it.
- Note: ASGI middleware (`app.add_middleware`) and HTTP middleware (`@app.middleware("http")`) — `add_middleware` wraps the app, runs for WebSockets too; the decorator is HTTP-only.
- Keep middleware light — it adds latency to every request; avoid blocking I/O inside it.

---

## Q65: How would you implement request logging middleware?

```python
import time, logging
from starlette.requests import Request

logger = logging.getLogger("api")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or uuid4().hex
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    logger.info(
        "method=%s path=%s status=%s dur=%.0fms request_id=%s",
        request.method, request.url.path, response.status_code,
        duration * 1000, request_id,
    )
    response.headers["X-Request-ID"] = request_id
    return response
```

- Log: method, path, status, duration, request_id, client IP.
- Add request_id early so logs correlate across services (propagate to DB calls, LLM calls).
- Use async logging or structured logs; never log sensitive body content (passwords/tokens).
- For latency percentiles, push to metrics, not just logs (Q628).

---

## Q66: How would you implement CORS in FastAPI?

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],   # NOT "*" in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
```

- CORS: browsers block cross-origin reads unless the server allows it via headers (Q406).
- `allow_origins` — restrict to your frontend domains; `allow_credentials=True` + `"*"` is invalid for browsers (credentials require explicit origins).
- Preflight `OPTIONS` requests are auto-handled by the middleware.
- Backend-to-backend calls (non-browser) don't need CORS.

---

## Q67: How do you structure a large FastAPI project?

Feature-based (recommended) layout:

```
app/
  main.py            # create_app(), include routers, middleware, exception handlers
  core/              # config.py (Settings), security.py, logging.py, exceptions.py
  db/                # session.py, base.py, models/, migrations/
  api/               # routers/
    routes/
      users.py
      auth.py
    deps.py          # shared dependencies
  schemas/           # Pydantic request/response models
  services/          # business logic
  repositories/      # data access
  models/            # ORM models
  utils/
tests/
```

- `main.py` keeps an `app` factory (`create_app()`) — enables testability and multiple app instances.
- Each router module: `router = APIRouter(prefix="/users", tags=["users"])`; `main` includes them.
- `core/config.py` holds pydantic-settings (Q69).
- Separate **schemas** (Pydantic) from **models** (ORM) — never return ORM objects directly.

---

## Q68: How do you separate routers, services, models, and repositories?

Layered architecture:

1. **Router (presentation):** HTTP verbs, params, status codes, request/response mapping. *No business logic.*
2. **Service (business logic):** validation rules, workflows, orchestration, transaction boundaries. Called by routers.
3. **Repository (data access):** DB queries, CRUD. Called by services. Isolates ORM from the rest.
4. **Model (domain/data):** ORM models (SQLAlchemy) and Pydantic schemas. Models are data, not logic.

```python
# router
@router.get("/{id}", response_model=UserOut)
def get_user(id: int, service: UserService = Depends(get_user_service)):
    return service.get_user(id)

# service
class UserService:
    def __init__(self, repo: UserRepository): ...
    def get_user(self, id): 
        user = self.repo.get(id)
        if not user: raise HTTPException(404, "User not found")
        return user

# repository
class UserRepository:
    def get(self, id): return db.query(User).filter_by(id=id).first()
```

- Benefits: single responsibility, testability (mock repos), swap ORM later, and the FastAPI `Depends` graph wires them together.

---

## Q69: How do you handle configuration and environment variables?

Use **pydantic-settings** (`BaseSettings`) — validated, typed config loaded from env vars and `.env` files.

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "zara"
    database_url: str
    redis_url: str
    llm_api_key: str = ""
    model_config = SettingsConfigDict(env_file=".env", env_prefix="")

settings = Settings()   # reads env vars + .env; missing required → error at startup
```

- Precedence: actual env vars > `.env` file > defaults.
- No secrets in code; `SECRET_*` types redact on print.
- Expose a module-level `settings` singleton (or dependency for tests).
- Per-environment: `.env.development`, `.env.production`; CI injects real values.
- Related: `config` management chapter in the trading resource (CH_31/03).

---

## Q70: How do you manage secrets in a FastAPI application?

1. **Never in code or git.** Not hardcoded, not committed in `.env` (gitignore it).
2. Load via environment variables → validated `Settings` (Q69).
3. In production use a **secrets manager**: AWS Secrets Manager / Parameter Store (Q609, Q610), Vault, or container secrets.
4. Rotate regularly; inject at deploy time, not baked into images.
5. Use `SecretStr`/`SecretBytes` types so secrets don't leak into logs/tracebacks.
6. Keep API keys out of `/docs` examples and response models.
7. Least-privilege IAM roles (Lambda/ECS) instead of long-lived keys where possible (Q617).

```python
class Settings(BaseSettings):
    llm_api_key: SecretStr
# settings.llm_api_key.get_secret_value()  # only when needed
```

---

## Q71: How would you test a FastAPI endpoint?

Use Starlette's `TestClient` (based on httpx) against the app.

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_user():
    resp = client.get("/users/1")
    assert resp.status_code == 200
    assert resp.json()["email"] == "a@b.c"

def test_create_user_invalid():
    resp = client.post("/users", json={"email": "not-an-email"})
    assert resp.status_code == 422
```

- TestClient runs the full ASGI app in-process (synchronous interface, even for async endpoints).
- Set up test DB (fixture), override dependencies, cleanup in fixtures.
- Also test: status codes, response schema (validate with Pydantic), errors, auth, pagination.
- For async tests, prefer `httpx.AsyncClient(transport=ASGITransport(app=app))` with pytest-asyncio (Q457).

---

## Q72: What is FastAPI's `TestClient`?

A test client provided by Starlette (re-exported by FastAPI) that lets you make requests to your app **without starting a server**:

- Wraps `httpx.Client` with an `ASGITransport` → runs the whole ASGI stack in-process.
- Same API as httpx: `.get()`, `.post(json=)`, `.put()`, `.delete()`, `.headers`, `.cookies`, `.files`, `with TestClient(app) as client` for lifespan events.
- Works with sync `pytest` functions even for `async` endpoints.
- Caveat: some async-only features (e.g., background tasks need `with` block) behave slightly differently; for WebSocket/streaming use `client.websocket_connect` or httpx AsyncClient.

---

## Q73: How do you mock dependencies in FastAPI tests?

Override the dependency graph — no mocks inside endpoints needed.

```python
from app.deps import get_db
from app.main import app
from fastapi.testclient import TestClient

def get_test_db():
    yield test_session()          # in-memory / test database session

app.dependency_overrides[get_db] = get_test_db
client = TestClient(app)
```

- `app.dependency_overrides[original] = replacement` swaps any `Depends` (db, auth, services, HTTP clients).
- Pattern: a pytest fixture that sets overrides and resets (`app.dependency_overrides.clear()`) after each test.
- For external APIs (LLM calls, third-party HTTP): monkeypatch/override an `httpx.AsyncClient` dependency or patch the client method.
- Keeps tests fast, deterministic, offline.

---

## Q74: How would you implement pagination in a FastAPI API?

Offset-based (common):

```python
from fastapi import Query

@app.get("/users")
def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    items = db.query(User).order_by(User.id).offset((page - 1) * limit).limit(limit).all()
    total = db.query(User).count()
    return {"items": items, "page": page, "limit": limit, "total": total, "pages": ceil(total / limit)}
```

- Always cap `limit` (avoid unbounded responses).
- Return envelope: items + metadata (page, limit, total, pages) OR use `Link` headers.
- For large datasets / live data prefer **cursor pagination** (keyset) — stable under inserts, O(1) offset cost (Q257, Q390).
- Filtering/sorting (Q75) composes with pagination; keep it simple, use indexes.

---

## Q75: How would you implement filtering and sorting?

```python
@app.get("/users")
def list_users(
    role: str | None = None,
    sort: str = "id",
    order: Literal["asc", "desc"] = "asc",
    db: Session = Depends(get_db),
):
    q = db.query(User)
    if role:
        q = q.filter(User.role == role)
    col = getattr(User, sort, None)
    if col is None:
        raise HTTPException(400, f"invalid sort field: {sort}")
    q = q.order_by(col.asc() if order == "asc" else col.desc())
    return q.all()
```

- **Allow-list sortable fields** — never pass raw column names into SQL (injection).
- Filters: exact (`==`), `in_`, ranges (`>=`, `<=`), text search (`ilike`), boolean flags.
- Combine with pagination (Q74). Ensure indexes cover filtered+ordered columns for large tables.
- For complex search, consider query params that map to `Query`/`FilterSet` (e.g., FastAPI filter libraries) — keep it readable.

---

## Q76: How would you version a FastAPI API?

Options (pick one strategy, be consistent):

1. **URL versioning (most common):** `/api/v1/users`, `/api/v2/users` — explicit, simple, cache-friendly.
2. **Header versioning:** `Accept: application/vnd.myapi.v2+json` — cleaner URL, more complex clients.
3. **Query param:** `?version=2` — simplest but pollutes URLs and caches.

Implementation (URL versioning):

```python
from fastapi import FastAPI
app = FastAPI()

v1 = APIRouter(prefix="/api/v1")
v2 = APIRouter(prefix="/api/v2")

v1.get("/users")(old_users)
v2.get("/users")(new_users)
app.include_router(v1); app.include_router(v2)
```

- Keep old versions alive for a deprecation window; document breaking changes; aim for backward-compatible additions first.

---

## Q77: How would you handle API errors consistently?

Standardize an **error envelope** across the API.

```python
class Error(BaseModel):
    error: str          # machine-readable code
    message: str        # human message
    details: list | None = None
    request_id: str | None = None
```

- Register a base `AppError` (code + status) and raise it anywhere in services.
- A single exception handler renders every AppError/HTTPException into the same shape.
- Include a `request_id` (from middleware, Q65) so logs link to client reports.
- Never leak internals: log full exception server-side; return sanitized messages.
- Document codes in OpenAPI (`responses={404: {"model": Error}}`).

```python
@app.exception_handler(AppError)
async def app_error_handler(request, exc):
    return JSONResponse(status_code=exc.status,
        content={"error": exc.code, "message": exc.message})
```

---

## Q78: How would you design a production-ready FastAPI application?

**Checklist (say this out loud — it maps to the role's requirements):**

1. **Structure:** feature-based layout; routers/schemas/services/repositories (Q67–68).
2. **Config:** pydantic-settings + secrets manager (Q69–70).
3. **Database:** connection pool (size tuned), session-per-request dependency, migrations (Alembic), indexes.
4. **Async correctness:** `async def` for I/O; never block the loop (Q90–92); timeouts on all outbound calls (Q116); semaphores for concurrency (Q97).
5. **Security:** auth dependency (JWT/OAuth), input validation (Pydantic), CORS locked down, rate limiting, no secrets in logs (Q400–420).
6. **Observability:** structured logging + request_id (Q65), metrics (Prometheus middleware) (Q629), health/live/ready endpoints.
7. **Resilience:** retries with backoff (Q113), circuit breaker for external/LLM calls, graceful degradation, idempotency keys for POST.
8. **Testing:** unit + integration (TestClient), dependency overrides, CI gate (Q621).
9. **Deployment:** Docker multi-stage build (Q383), Uvicorn behind reverse proxy, multiple workers (Q652), health checks, zero-downtime deploys.
10. **Performance:** pagination everywhere, response models to trim payloads, caching (Redis) for hot endpoints, DB query tuning (EXPLAIN, Q166).
