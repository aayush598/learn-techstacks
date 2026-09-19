# FastAPI Interview Questions and Answers

## Q1: What is FastAPI?
**A:** FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. It's built on Starlette (for web routing) and Pydantic (for data validation). Key features include automatic OpenAPI documentation, async support, and high performance.


**Code:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

## Q2: What are the key features of FastAPI?
**A:** Key features include: automatic OpenAPI/Swagger documentation, request validation via Pydantic models, async/await support, dependency injection system, security utilities (OAuth2, JWT), GraphQL support, background tasks, CORS handling, WebSocket support, and high performance comparable to Node.js and Go.


**Code:**
```python
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

## Q3: How does FastAPI compare to Flask?
**A:** FastAPI is asynchronous by default, automatically generates OpenAPI docs, uses Pydantic for validation, and is faster (Starlette-based). Flask is synchronous, doesn't auto-generate docs, uses manual validation, and has a larger ecosystem. FastAPI is better for modern async APIs; Flask is simpler for smaller projects.


**Code:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"async": True, "validation": "typed"}
```

## Q4: How does FastAPI handle request validation?
**A:** FastAPI uses Pydantic models for request validation. Define models with type annotations: `class Item(BaseModel): name: str; price: float`. FastAPI automatically validates request bodies, query parameters, and path parameters against these models, returning detailed 422 validation errors for invalid data.


**Code:**
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
async def create_item(item: Item):
    return {"name": item.name, "price": item.price}
```

## Q5: How do you define path parameters in FastAPI?
**A:** Path parameters are defined in the path string with `{}`: `@app.get("/items/{item_id}")`. The function parameter must match: `async def read_item(item_id: int)`. FastAPI automatically validates type and extracts from path. Path parameters can have predefined values using `Path` and `Enum`.


**Code:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

## Q6: How do you define query parameters in FastAPI?
**A:** Function parameters not in the path are query parameters. Example: `@app.get("/items/") async def list_items(skip: int = 0, limit: int = 10)`. Optional parameters have defaults. Required query parameters raise 422 if missing. `Query(None)` makes a parameter optional with None default.


**Code:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

## Q7: How does FastAPI generate OpenAPI documentation?
**A:** FastAPI automatically generates OpenAPI (Swagger) spec from your route definitions, type hints, docstrings, and Pydantic models. Accessible at `/docs` (Swagger UI) and `/redoc` (ReDoc). You can customize with `title`, `description`, `version`, `tags`, `summary`, and `response_description` parameters.


**Code:**
```python
from fastapi import FastAPI

app = FastAPI(title="My API", description="Example", version="1.0.0")

# Auto-generated OpenAPI spec is served at /openapi.json, UI at /docs
```

## Q8: What is Pydantic and how is it used in FastAPI?
**A:** Pydantic is a data validation library using Python type annotations. In FastAPI, it defines request/response models. Features: automatic type validation, JSON schema generation, custom validators, nested models, ORM mode, and `model_dump()` serialization. FastAPI uses Pydantic v2 (v1.0+ uses v1).


**Code:**
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

item = Item(name="Widget", price=9.99)
print(item.model_dump())
```

## Q9: How do you create a Pydantic model?
**A:** `from pydantic import BaseModel; class Item(BaseModel): name: str; price: float; is_offer: bool = False`. Fields are defined with type annotations. Default values make fields optional. Models validate data on creation. Access fields as attributes: `item.name`. Convert to dict: `item.model_dump()`.


**Code:**
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

item = Item(name="Widget", price=9.99)
print(item.is_offer)
```

## Q10: What are Pydantic validators?
**A:** Validators in Pydantic v2 use `@field_validator` (for single fields) and `@model_validator` (for multiple fields). Example: `@field_validator('name') @classmethod def name_must_be_whitespace_stripped(cls, v: str) -> str: return v.strip()`. Before/after modes control when validation runs.


**Code:**
```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()

user = User(name="  Alice  ")
print(user.name)
```

## Q11: How do you handle errors in FastAPI?
**A:** Raising `HTTPException(status_code=404, detail="Item not found")` returns error responses. Custom exception handlers with `@app.exception_handler(MyException)` handle specific exception types. `RequestValidationError` for validation errors. Override default exception handlers for custom error formatting.


**Code:**
```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id <= 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}
```

## Q12: What is FastAPI's dependency injection system?
**A:** `Depends()` allows injecting dependencies into path operations. Dependencies are callables (functions, classes, generators) that can share logic. Example: `def get_db(): db = Session(); yield db; db.close()`. Dependencies can be nested, cached, and used across routes. Great for authentication, DB sessions, and common logic.


**Code:**
```python
from fastapi import FastAPI, Depends

app = FastAPI()

def common_params(q: str | None = None, limit: int = 10):
    return {"q": q, "limit": limit}

@app.get("/items")
async def read_items(params: dict = Depends(common_params)):
    return params
```

## Q13: How do you use dependency injection for authentication?
**A:** Create dependency: `async def get_current_user(token: str = Depends(oauth2_scheme)) -> User`. Path operations use `current_user: User = Depends(get_current_user)`. FastAPI automatically calls the dependency and injects the result. Dependencies can be reused, scoped, and composed.


**Code:**
```python
from fastapi import FastAPI, Depends
from jose import jwt

app = FastAPI()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload["sub"]

@app.get("/users/me")
async def read_me(current_user=Depends(get_current_user)):
    return {"user": current_user}
```

## Q14: How does FastAPI handle CORS?
**A:** Using `CORSMiddleware`: `app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])`. Configures which origins, methods, and headers are allowed. `allow_origins=["*"]` allows all origins (not with credentials). Preflight OPTIONS requests are handled automatically.


**Code:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Q15: How do you handle authentication in FastAPI?
**A:** FastAPI provides `OAuth2PasswordBearer` (token URL), `OAuth2PasswordRequestForm` (login form), and utilities for JWT (python-jose). Flow: user logs in -> server validates -> returns JWT token -> client sends token in Authorization header -> dependency decodes JWT -> returns authenticated user.


**Code:**
```python
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    token = jwt.encode({"sub": form.username}, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

@app.get("/users/me")
async def read_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

## Q16: What are background tasks in FastAPI?
**A:** Background tasks run after returning a response. `from fastapi import BackgroundTasks`. Add tasks: `background_tasks.add_task(send_email, user_email)`. Pass as dependency or parameter. For heavy async tasks, use Celery or Redis Queue. Background tasks don't block response. Useful for logging, notifications, cleanup.


**Code:**
```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def send_email(email: str):
    print(f"sending email to {email}")

@app.post("/send-email")
async def notify(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email)
    return {"status": "queued"}
```

## Q17: How do you handle file uploads in FastAPI?
**A:** Use `UploadFile` from `fastapi`: `async def upload(file: UploadFile = File(...))`. `UploadFile` provides `.filename`, `.content_type`, `.file` (SpooledTemporaryFile), `.read()`, `.write()`, `.seek()`. For multiple files: `files: list[UploadFile] = File(...)`. Files are streamed (not loaded into memory fully).


**Code:**
```python
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File()):
    content = await file.read()
    return {"filename": file.filename, "size": len(content)}
```

## Q18: How does FastAPI handle form data?
**A:** Use `Form()` for form fields: `def login(username: str = Form(), password: str = Form())`. For file + form mix: use both `Form` and `File`. OAuth2 form: `OAuth2PasswordRequestForm` provides `username`, `password`, `scope`, `client_id`, `client_secret`. Form data requires `python-multipart` package.


**Code:**
```python
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}
```

## Q19: What is WebSocket support in FastAPI?
**A:** FastAPI supports WebSockets via `@app.websocket("/ws")`. Use `WebSocket` parameter: `async def websocket_endpoint(websocket: WebSocket)`. Methods: `await websocket.accept()`, `send_text()`, `send_json()`, `receive_text()`, `receive_json()`, `close()`. Dependencies work with WebSockets.


**Code:**
```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello!")
    await websocket.close()
```

## Q20: How does FastAPI handle routing?
**A:** Routes are defined with decorators: `@app.get()`, `@app.post()`, `@app.put()`, `@app.delete()`, `@app.patch()`, `@app.options()`, `@app.head()`, `@app.websocket()`. Path operations can have path params, query params, request body, dependencies, tags, summary, description, and response model. Routes are matched in order.


**Code:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items")
async def read_items():
    return []

@app.post("/items")
async def create_item():
    return {"created": True}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"deleted": item_id}
```

## Q21: What is `APIRouter` in FastAPI?
**A:** `APIRouter` allows organizing routes into separate modules: `router = APIRouter(prefix="/items", tags=["items"])`. Include in app: `app.include_router(router)`. Each router can have its own prefix, tags, dependencies, and responses. Enables clean project structure with concerns separated by module.


**Code:**
```python
from fastapi import FastAPI, APIRouter

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
async def read_items():
    return []

app = FastAPI()
app.include_router(router)
```

## Q22: How do you handle database operations with FastAPI?
**A:** FastAPI is database-agnostic. Common patterns: SQLAlchemy with dependency injection (session per request), Tortoise-ORM (async ORM), MongoDB with Beanie/Motor. SQLAlchemy example: `async def get_db(): db = SessionLocal(); yield db; db.close()`. Use `AsyncSession` for async database operations.


**Code:**
```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items")
async def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

## Q23: What is SQLAlchemy's `AsyncSession` and how is it used?
**A:** `AsyncSession` from SQLAlchemy 1.4+ enables async database operations. Setup: `create_async_engine(url)`, `AsyncSession(engine)`. Queries use `await session.execute(select(Model))`. `.scalars().all()` returns results. Commit: `await session.commit()`. Requires async database drivers (asyncpg, aiosqlite, aiomysql).


**Code:**
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select

engine = create_async_engine("sqlite+aiosqlite:///db.sqlite3")

async def get_user(username: str):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(User).where(User.name == username))
        return result.scalars().first()
```

## Q24: How do you configure database migrations with FastAPI?
**A:** Alembic is the standard migration tool with SQLAlchemy. Initialize: `alembic init alembic`. Configure `env.py` with your models and database URL. Generate migrations: `alembic revision --autogenerate -m "description"`. Apply: `alembic upgrade head`. Integrate with FastAPI startup events for auto-migration.


**Code:**
```python
from alembic.config import Config
from alembic import command

config = Config("alembic.ini")
config.set_main_option("script_location", "alembic")
command.upgrade(config, "head")
```

## Q25: How do FastAPI's startup and shutdown events work?
**A:** `@app.on_event("startup")` registers coroutines that run at startup (DB connection, cache init). `@app.on_event("shutdown")` for cleanup (close connections, stop background tasks). For lifespan management, use `async with app.lifespan_context(...)` (Starlette) or `@asynccontextmanager` pattern.


**Code:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    app.state.db = await connect_db()

@app.on_event("shutdown")
async def on_shutdown():
    await app.state.db.close()
```

## Q26: What is the `lifespan` parameter in FastAPI 0.90+?
**A:** FastAPI 0.90+ uses `lifespan` context manager instead of startup/shutdown events. Define: `@asynccontextmanager async def lifespan(app: FastAPI): await startup(); yield; await shutdown()`. Pass to `FastAPI(lifespan=lifespan)`. Centralizes lifecycle logic and is the modern recommended approach.


**Code:**
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    await open_connections()
    yield
    await close_connections()

app = FastAPI(lifespan=lifespan)
```

## Q27: How do you add middleware in FastAPI?
**A:** `@app.middleware("http")` decorator creates middleware: `async def add_header(request: Request, call_next): response = await call_next(request); response.headers["X-Custom"] = "value"; return response`. BaseHTTPMiddleware for classes. Middleware processes every request/response. Use for logging, timing, CORS, etc.


**Code:**
```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Custom"] = "value"
    return response
```

## Q28: What is `BaseHTTPMiddleware`?
**A:** `BaseHTTPMiddleware` from Starlette allows class-based middleware. Implement `async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response`. Called for every request. More powerful than decorator middleware but slightly slower. Used for complex middleware with state.


**Code:**
```python
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Process-Time"] = "0.01s"
        return response

app = FastAPI()
app.add_middleware(CustomMiddleware)
```

## Q29: How does FastAPI handle response serialization?
**A:** FastAPI automatically serializes return values to JSON using `response_model`. Models are serialized via `model_dump()`. Use `response_model_exclude_unset`, `response_model_include`, `response_model_exclude` for fine control. Return `dict`, Pydantic model, ORM model, or custom `Response` object.


**Code:**
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ItemOut(BaseModel):
    name: str

@app.get("/items/{item_id}", response_model=ItemOut)
async def read_item(item_id: int):
    return {"name": "Widget", "secret": "hidden"}
```

## Q30: What is `response_model` in FastAPI?
**A:** `response_model` parameter filters and serializes the response: `@app.get("/item/{id}", response_model=ItemOut)`. It ensures only specified fields are returned, handles type conversion, and generates proper OpenAPI schema. Used for data hiding (e.g., excluding password fields from API responses).


**Code:**
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserOut(BaseModel):
    id: int
    email: str

@app.get("/users/{user_id}", response_model=UserOut)
async def read_user(user_id: int):
    return {"id": user_id, "email": "a@b.com", "password_hash": "xx"}
```

## Q31: How do you handle SQL (relational) databases in FastAPI?
**A:** SQLAlchemy is the most common ORM. Pattern: define models with `declarative_base()`, create engine and session, use `SessionLocal()` as dependency. For async: `AsyncEngine`, `async_sessionmaker`, `AsyncSession`. Use Alembic for migrations. Repository pattern separates DB logic from route handlers.


**Code:**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///./app.db")
SessionLocal = sessionmaker(bind=engine)
```

## Q32: How do you handle NoSQL databases like MongoDB with FastAPI?
**A:** Use Motor (async MongoDB driver) or Beanie (ODM). Motor: `client = AsyncIOMotorClient()`, `db = client.database`. Beanie: define documents as classes inheriting `Document`, supports validation, indexes, and relationships. Connect in lifespan: `await init_beanie(database, document_models=[User])`.


**Code:**
```python
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.mydatabase

async def find_user(user_id: str):
    return await db.users.find_one({"_id": user_id})
```

## Q33: How does FastAPI handle concurrency?
**A:** FastAPI leverages Python's async/await for concurrency. I/O-bound operations (DB queries, HTTP calls, file I/O) can run concurrently using `asyncio.gather()` or `async` dependencies. For CPU-bound tasks, use thread pool (`run_in_executor`) or process pool to avoid blocking the event loop.


**Code:**
```python
import asyncio

async def fetch(url: str):
    return f"data from {url}"

async def main():
    results = await asyncio.gather(fetch("a"), fetch("b"))
    print(results)
```

## Q34: What is `run_in_executor` and when is it used?
**A:** `loop.run_in_executor(None, sync_function, args)` runs synchronous CPU-bound or blocking I/O functions in a thread pool, preventing event loop blocking. Example: `await asyncio.get_event_loop().run_in_executor(None, pd.read_csv, "file.csv")`. Essential when using synchronous libraries in async FastAPI.


**Code:**
```python
import asyncio
import time

def blocking_work():
    time.sleep(1)
    return "done"

async def main():
    result = await asyncio.to_thread(blocking_work)
    return result
```

## Q35: How does FastAPI handle request/response models with relationships?
**A:** Pydantic models can have nested models for relationships. Use separate schemas for create/read/update operations. Example: `class UserRead(BaseModel): items: list[ItemRead] = []`. For ORM integration, use `model_config = {"from_attributes": True}` in Pydantic v2. Avoid circular references with `model_serializer`.


**Code:**
```python
from pydantic import BaseModel

class ItemRead(BaseModel):
    id: int
    name: str

class UserRead(BaseModel):
    id: int
    items: list[ItemRead] = []

    model_config = {"from_attributes": True}
```

## Q36: What is Pydantic v2's `from_attributes`?
**A:** `model_config = {"from_attributes": True}` (Pydantic v2) or `class Config: orm_mode = True` (v1) enables creating Pydantic models from ORM objects. FastAPI uses this to serialize SQLAlchemy models. The ORM object's attributes are read directly. Required for response_model with ORM data.


**Code:**
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

    model_config = {"from_attributes": True}

item = Item.model_validate(orm_item)
```

## Q37: How do you implement pagination in FastAPI?
**A:** Common approach: query params `skip` and `limit`: `def get_items(skip: int = 0, limit: int = 10)`. Return `{"items": items, "total": total, "skip": skip, "limit": limit}`. Libraries like `fastapi-pagination` provide reusable Pagination classes. For cursor-based pagination, use `cursor` param with `WHERE id > cursor`.


**Code:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    items = db.query(Item).offset(skip).limit(limit).all()
    total = db.query(Item).count()
    return {"items": items, "total": total, "skip": skip, "limit": limit}
```

## Q38: How does FastAPI handle rate limiting?
**A:** FastAPI itself doesn't include rate limiting. Implement with: middleware + Redis (store IP/counter, TTL), `slowapi` library (FastAPI integration), or API gateway (NGINX, Cloudflare, AWS API Gateway). Manual approach: use dependency with `Depends(rate_limiter())` checking Redis for request counts.


**Code:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/items")
@limiter.limit("100/minute")
async def read_items(request: Request):
    return []
```

## Q39: What is the `Header` dependency in FastAPI?
**A:** `Header()` extracts HTTP headers: `def read_items(user_agent: str = Header())`. Header names are case-insensitive; underscores become hyphens (e.g., `user_agent` becomes `User-Agent`). Supports duplicate headers as lists: `x_token: list[str] = Header()`. Useful for API keys, custom headers.


**Code:**
```python
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items")
async def read_items(user_agent: str | None = Header(default=None)):
    return {"user_agent": user_agent}
```

## Q40: How does FastAPI handle cookies?
**A:** `Cookie()` extracts cookies: `def read_items(session_id: str = Cookie())`. Set cookies: `response.set_cookie(key="session_id", value=token)`. Use `Response` parameter or `JSONResponse`. Options: max_age, expires, path, domain, secure, httponly, samesite. Delete: `response.delete_cookie("session_id")`.


**Code:**
```python
from fastapi import FastAPI, Cookie, Response

app = FastAPI()

@app.get("/items")
async def read_items(response: Response, session_id: str | None = Cookie(default=None)):
    response.set_cookie(key="session_id", value="abc123")
    return {"session_id": session_id}
```

## Q41: What is `JSONResponse` in FastAPI?
**A:** `JSONResponse(content, status_code, headers, media_type)` returns custom JSON responses. Inherits from Starlette's `Response`. Use for non-standard status codes or custom headers. Other response types: `HTMLResponse`, `PlainTextResponse`, `RedirectResponse`, `StreamingResponse`, `FileResponse`.


**Code:**
```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/custom")
async def custom():
    return JSONResponse(content={"ok": True}, status_code=201, headers={"X-A": "1"})
```

## Q42: How do you handle static files in FastAPI?
**A:** Mount static files: `from fastapi.staticfiles import StaticFiles; app.mount("/static", StaticFiles(directory="static"), name="static")`. Serves files at `/static/filename.ext`. For single-file downloads, use `FileResponse`. For streaming large files, use `StreamingResponse`.


**Code:**
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
```

## Q43: What is `StreamingResponse` in FastAPI?
**A:** `StreamingResponse(content, media_type)` streams data without loading everything into memory. Content is an iterable (generator). Used for: large file downloads, progressive responses, server-sent events. Example: `StreamingResponse(generate_large_csv(), media_type="text/csv")`.


**Code:**
```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

def generate_rows():
    for i in range(100):
        yield f"row {i}\n"

@app.get("/export")
async def export():
    return StreamingResponse(generate_rows(), media_type="text/plain")
```

## Q44: How does FastAPI handle testing?
**A:** Use `TestClient` from `httpx`: `from fastapi.testclient import TestClient; client = TestClient(app)`. Test routes: `response = client.get("/items/1")`. Assert on `response.status_code`, `response.json()`, `response.text`. For async tests, use `httpx.AsyncClient`. Override dependencies with `app.dependency_overrides`.


**Code:**
```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["item_id"] == 1
```

## Q45: How do you override dependencies in FastAPI tests?
**A:** `app.dependency_overrides[get_current_user] = mock_get_user`. This replaces a real dependency with a mock during testing. Clear after tests: `app.dependency_overrides.clear()`. Necessary for testing authentication flows without real tokens. Override database sessions for integration tests.


**Code:**
```python
from main import app, get_current_user

async def fake_get_current_user():
    return {"username": "tester"}

app.dependency_overrides[get_current_user] = fake_get_current_user
```

## Q46: How does FastAPI handle environment configuration?
**A:** Use Pydantic's `BaseSettings`: `from pydantic_settings import BaseSettings; class Settings(BaseSettings): database_url: str; secret_key: str`. Loads from environment variables, `.env` files, or defaults. FastAPI's `lifespan` creates settings once and injects via dependencies.


**Code:**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str

    model_config = {"env_file": ".env"}

settings = Settings()
```

## Q47: What is Pydantic `BaseSettings`?
**A:** Pydantic's `BaseSettings` loads configuration from environment variables, `.env` files, secrets, etc. Fields are automatically populated from env vars matching the field name (case-insensitive). Example: `class Settings(BaseSettings): app_name: str = "MyAPI"`. Use `model_config = {"env_file": ".env"}` for file loading.


**Code:**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "MyAPI"
    debug: bool = False

    model_config = {"env_file": ".env"}

settings = Settings()
print(settings.app_name)
```

## Q48: How do you add logging to FastAPI?
**A:** Configure Python's `logging` module at startup. Example: `logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")`. Use `logger = logging.getLogger(__name__)` in modules. Add request logging middleware: log method, path, status code, and duration.


**Code:**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("App starting")
```

## Q49: How does FastAPI handle request body size limits?
**A:** FastAPI (via Starlette) has a default max body size of 16MB. Configure with: `app = FastAPI()`, then `app.add_middleware(RequestSizeLimitMiddleware, max_size=1_000_000)` or set on ASGI server level (Uvicorn's `--limit-concurrency`). Custom middleware can check `Content-Length` header.


**Code:**
```python
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

class BodySizeLimit(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if int(request.headers.get("content-length", 0)) > 1_000_000:
            return JSONResponse({"detail": "Body too large"}, status_code=413)
        return await call_next(request)
```

## Q50: How do you use `@app.exception_handler`?
**A:** Custom exception handlers: `@app.exception_handler(ValueError) async def value_error_handler(request, exc): return JSONResponse(status_code=400, content={"detail": str(exc)})`. Override default handlers: `@app.exception_handler(RequestValidationError)` for custom validation error format.


**Code:**
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
```

## Q51: What is `ValidationException` in Pydantic v2?
**A:** Pydantic v2 raises `ValidationError` when data is invalid. FastAPI catches this and returns 422 with details. Customize with `@app.exception_handler(RequestValidationError)`. Access `exc.errors()` for field-level error details. Pydantic v2 errors have different structure from v1.


**Code:**
```python
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"errors": exc.errors()})
```

## Q52: How do you implement caching in FastAPI?
**A:** Options: in-memory cache (dict with TTL), Redis (redis-py), or `fastapi-cache` library. Middleware can cache GET responses based on path/query. Manual: dependency that checks cache before DB query. Use `Cache-Control` and `ETag` headers for HTTP caching. Invalidate cache on write operations.


**Code:**
```python
import time
from functools import lru_cache

@lru_cache(maxsize=128)
def get_slow_data():
    time.sleep(2)
    return {"data": [1, 2, 3]}
```

## Q53: How does FastAPI support versioning?
**A:** URL versioning: `@app.get("/v1/items")` or use `APIRouter(prefix="/v1")`. Header versioning: check `Accept-Version` header in dependency. Query parameter versioning: `?version=1`. Combine with `app.include_router(v1_router)` for separate version modules. Deprecate old versions with warning headers.


**Code:**
```python
from fastapi import FastAPI, APIRouter

app = FastAPI()

v1 = APIRouter(prefix="/v1")

@v1.get("/items")
async def items_v1():
    return {"version": 1}

app.include_router(v1)
```

## Q54: What is `HTTPException` and how is it used?
**A:** `HTTPException(status_code, detail, headers)` raises HTTP errors. FastAPI catches it and returns JSON. Example: `raise HTTPException(status_code=404, detail="Item not found")`. `detail` can be a string or dict for structured errors. `headers` adds custom response headers.


**Code:**
```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id < 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}
```

## Q55: How do you handle 404 errors globally in FastAPI?
**A:** Override default 404 handler: `@app.exception_handler(404) async def not_found_handler(request, exc): return JSONResponse(status_code=404, content={"message": "Resource not found"})`. Or catch Starlette's `HTTPException` with status 404 specifically.


**Code:**
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(status_code=404, content={"message": "Resource not found"})
```

## Q56: What is `Depends()` with `yield` (generator dependencies)?
**A:** Dependencies using `yield` instead of `return` provide setup/teardown. Code before `yield` runs on request start; code after `yield` runs on response completion. Used for DB sessions (commit/rollback), file cleanup, connection release. Requires `async` for async generators.


**Code:**
```python
from fastapi import FastAPI, Depends

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
async def read_users(db=Depends(get_db)):
    return db.query(User).all()
```

## Q57: How does sub-dependency work in FastAPI?
**A:** Dependencies can depend on other dependencies. Example: `def get_user(db = Depends(get_db), token = Depends(get_token))`. FastAPI resolves the full dependency tree automatically. Nested dependencies are cached per request (same dependency called once). Override for testing.


**Code:**
```python
from fastapi import Depends

def get_token():
    return "token"

def get_current_user(token: str = Depends(get_token)):
    return {"user": token}

def read_me(current_user=Depends(get_current_user)):
    return current_user
```

## Q58: What is dependency caching in FastAPI?
**A:** FastAPI caches dependency results per request by default. If the same dependency is called multiple times in a request (via `Depends()`), it runs once and reuses the result. Disable with `Depends(get_db, use_cache=False)`. Useful when you want fresh results on each call.


**Code:**
```python
from fastapi import Depends

def get_db():
    return "session"

@app.get("/a")
async def read_a(db=Depends(get_db)):
    return db

@app.get("/b")
async def read_b(db=Depends(get_db, use_cache=False)):
    return db
```

## Q59: How does FastAPI handle security?
**A:** FastAPI provides security utilities: `HTTPBasic`, `HTTPBearer`, `OAuth2PasswordBearer`, `OAuth2AuthorizationCodeBearer`, `APIKeyHeader`, `APIKeyQuery`, `APIKeyCookie`. Combine with JWT (python-jose) for token-based auth. Security dependencies can be composed and reused across routes.


**Code:**
```python
from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader

app = FastAPI()
api_key_header = APIKeyHeader(name="X-API-Key")

@app.get("/secure")
async def secure(api_key: str = Depends(api_key_header)):
    return {"api_key": api_key}
```

## Q60: What is OAuth2PasswordBearer?
**A:** `OAuth2PasswordBearer(tokenUrl="token")` creates a security scheme expecting Bearer token in Authorization header. FastAPI shows auth button in Swagger UI. Use as dependency: `token: str = Depends(oauth2_scheme)`. The tokenUrl tells the client where to get the token (login endpoint).


**Code:**
```python
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
async def read_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

## Q61: How do you create JWT tokens in FastAPI?
**A:** Use `python-jose` library. Create token: `access_token = jwt.encode({"sub": user_id, "exp": exp_time}, SECRET_KEY, algorithm="HS256")`. Decode: `payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])`. Integrate with OAuth2PasswordBearer and get_current_user dependency.


**Code:**
```python
from jose import jwt

SECRET_KEY = "secret-key"
ALGORITHM = "HS256"

token = jwt.encode({"sub": "123"}, SECRET_KEY, algorithm=ALGORITHM)
payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
print(payload["sub"])
```

## Q62: What is `OAuth2PasswordRequestForm`?
**A:** A dependency for OAuth2 login form: `def login(form_data: OAuth2PasswordRequestForm = Depends())`. Provides `username`, `password`, `scope`, `grant_type`, `client_id`, `client_secret`. Typically used in `/token` endpoint to validate credentials and return JWT token.


**Code:**
```python
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

@app.post("/token")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    return {"username": form.username, "grant_type": form.grant_type}
```

## Q63: How do you implement refresh tokens in FastAPI?
**A:** Two endpoints: `/token` returns `access_token` (short-lived) and `refresh_token` (long-lived). `/refresh` validates refresh token (check DB/Redis), issues new access token. Refresh tokens are stored securely (hashed). Invalidated on use (rotation) or on logout. Prevents re-issuing stolen tokens.


**Code:**
```python
from fastapi import FastAPI, Depends
from jose import jwt
from datetime import timedelta, datetime

app = FastAPI()

SECRET_KEY = "secret"
ALGORITHM = "HS256"

def create_token(data: dict, minutes: int) -> str:
    return jwt.encode({"exp": datetime.utcnow() + timedelta(minutes=minutes), **data}, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/refresh")
async def refresh(refresh_token: str):
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    return {"access_token": create_token({"sub": payload["sub"]}, 30)}
```

## Q64: How does FastAPI handle WebSocket authentication?
**A:** Authenticate during WebSocket handshake: check query params, cookies, or token in first message. Example: `async def ws(websocket: WebSocket, token: str = Query()): user = verify_token(token); await websocket.accept()`. Or use dependency: `websocket: WebSocket, user: User = Depends(get_user_from_cookie)`.


**Code:**
```python
from fastapi import FastAPI, WebSocket, Query

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str | None = Query(default=None)):
    user = verify_token(token)
    if user is None:
        await websocket.close(code=4001)
        return
    await websocket.accept()
```

## Q65: What is `JSONDecoder` customization in FastAPI?
**A:** Override `app.json_encoder` or provide custom `json.dumps` via `JSONResponse`. For custom serialization, implement `__json__` method on objects or use Pydantic's custom serializers: `@field_serializer('date') def serialize_date(self, d: date): return d.isoformat()`.


**Code:**
```python
from pydantic import BaseModel, field_serializer
from datetime import date

class Event(BaseModel):
    when: date

    @field_serializer("when")
    def serialize_date(self, d: date) -> str:
        return d.isoformat()

event = Event(when=date(2026, 1, 1))
print(event.model_dump_json())
```

## Q66: How do you implement custom response classes?
**A:** Subclass Starlette's `Response`: `class CustomResponse(Response): media_type = "application/xml"; def render(self, content) -> bytes: return xml_encode(content)`. Use in path operations: `return CustomResponse(content=data)`. Or use `Response` directly with custom headers and status.


**Code:**
```python
from starlette.responses import Response
from fastapi import FastAPI, Request

class XMLResponse(Response):
    media_type = "application/xml"

    def render(self, content: str) -> bytes:
        return content.encode("utf-8")

app = FastAPI()

@app.get("/xml")
async def xml():
    return XMLResponse(content="<root/>")
```

## Q67: What is `ORJSONResponse`?
**A:** `ORJSONResponse` uses `orjson` library for faster JSON serialization (3-5x faster than stdlib). Enable globally: `app = FastAPI(default_response_class=ORJSONResponse)`. Or per-route: `@app.get("/", response_class=ORJSONResponse)`. Requires `pip install orjson`. Benefits: speed, datetime handling, bytes support.


**Code:**
```python
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(default_response_class=ORJSONResponse)
```

## Q68: How do you use `uvicorn` with FastAPI?
**A:** Run: `uvicorn main:app --reload --port 8000`. `main:app` = module:app_instance. Options: `--host` (default 127.0.0.1), `--workers` (multiple processes), `--ssl-keyfile`/`--ssl-certfile` (HTTPS). For production: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`. Uvicorn is the ASGI server FastAPI runs on.


**Code:**
```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

## Q69: What is `gunicorn` and how is it used with FastAPI?
**A:** Gunicorn is a WSGI server; for FastAPI (ASGI), use with Uvicorn worker: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`. Manages multiple worker processes. Options: `--worker-class`, `--timeout`, `--keep-alive`. For async workers: `uvicorn.workers.UvicornWorker`. Provides process management and signals.


**Code:**
```python
# Run in a terminal:
#   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Q70: How does FastAPI handle database transactions?
**A:** Using SQLAlchemy's session: `db.begin()`, `db.commit()`, `db.rollback()`. Recommended pattern: dependency with `yield` auto-commits on success, rolls back on error. For distributed transactions, use saga pattern or two-phase commit. Async: `async with session.begin(): await session.execute(...)`.


**Code:**
```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
```

## Q71: How do you implement soft deletes in FastAPI?
**A:** Add `is_deleted` boolean field and `deleted_at` timestamp to models. Filter queries: `query.filter(Model.is_deleted == False)`. Default `is_deleted` scopes on SQLAlchemy: `@property def active(self): return select(self).where(self.is_deleted == False)`. Override delete methods to set flag instead of deleting.


**Code:**
```python
from sqlalchemy import Column, Boolean, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    is_deleted = Column(Boolean, default=False)

users = db.query(User).filter(User.is_deleted == False).all()
```

## Q72: What is `alembic` and how do you use it?
**A:** Alembic is a lightweight database migration tool for SQLAlchemy. Manage schema changes with version-controlled migration scripts. Commands: `alembic init alembic` (setup), `alembic revision --autogenerate -m "message"` (auto-detect changes), `alembic upgrade head` (apply). Supports downgrade with `alembic downgrade -1`.


**Code:**
```python
# In a terminal:
#   alembic init alembic
#   alembic revision --autogenerate -m "create users table"
#   alembic upgrade head
```

## Q73: How do you handle many-to-many relationships in FastAPI?
**A:** SQLAlchemy: create association table with `Table('association', Base.metadata, Column('left_id', ForeignKey...), Column('right_id', ForeignKey...))`. Pydantic: `class UserRead(BaseModel): groups: list[GroupRead] = []`. Use `relationship(secondary=association_table)` in ORM models. Handle serialization carefully to avoid recursion.


**Code:**
```python
from sqlalchemy import Table, Column, ForeignKey

association = Table(
    "user_groups",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("group_id", ForeignKey("groups.id")),
)
```

## Q74: What is Tortoise-ORM and how does it integrate with FastAPI?
**A:** Tortoise-ORM is an async ORM inspired by Django ORM. Define models as classes inheriting `Model`. Integrate: `register_tortoise(app, db_url="sqlite://db.sqlite3", modules={"models": ["app.models"]})`. Provides `pydantic_model_creator()` for automatic Pydantic schema generation from models.


**Code:**
```python
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI

app = FastAPI()

register_tortoise(
    app,
    db_url="sqlite:////tmp/db.sqlite3",
    modules={"models": ["app.models"]},
    generate_schemas=True,
)
```

## Q75: How does FastAPI handle GraphQL?
**A:** FastAPI integrates with GraphQL via Strawberry or Graphene libraries. Strawberry example: `@strawberry.type class Query { @strawberry.field def hello(self) -> str: return "World" }`. Mount: `app.add_route("/graphql", GraphQLRouter(schema))`. Supports subscriptions, mutations, and async resolvers.


**Code:**
```python
import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "World"

app = FastAPI()
schema = strawberry.Schema(query=Query)
app.include_router(GraphQLRouter(schema), prefix="/graphql")
```

## Q76: How do you implement WebSocket rooms/broadcast in FastAPI?
**A:** Using a connection manager pattern: `class ConnectionManager: active_connections: dict[str, list[WebSocket]]`. Methods: `connect(room, websocket)`, `disconnect(room, websocket)`, `broadcast(room, message)`. For multi-process: use Redis pub/sub via `redis-py` with async pub/sub listeners.


**Code:**
```python
class ConnectionManager:
    def __init__(self):
        self.rooms: dict[str, list[WebSocket]] = {}

    async def broadcast(self, room: str, message: str):
        for ws in self.rooms.get(room, []):
            await ws.send_text(message)
```

## Q77: What is `Server-Sent Events` (SSE) in FastAPI?
**A:** SSE pushes real-time events from server to client over HTTP. Implement with `StreamingResponse` and generator: `async def event_generator(): while True: yield f"data: {json.dumps(data)}\n\n"; await asyncio.sleep(1)`. Client uses `EventSource` API. Simpler than WebSocket for one-way data flow.


**Code:**
```python
import asyncio, json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def event_generator():
    while True:
        yield f"data: {json.dumps({'time': 1})}\n\n"
        await asyncio.sleep(1)

@app.get("/events")
async def events():
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

## Q78: How do you implement Celery with FastAPI?
**A:** Create Celery app instance, define tasks with `@celery.task`, pass to Celery worker. In FastAPI: call `task.delay()` or `task.apply_async()` from route handlers. Store Celery app in module-level variable or dependency. For results: use `AsyncResult(task_id)` with Redis/DB backend.


**Code:**
```python
from celery import Celery
from fastapi import FastAPI

celery = Celery("tasks", broker="redis://localhost:6379")
app = FastAPI()

@celery.task
def send_email(email: str):
    return f"sending to {email}"

@app.post("/send-email")
async def notify(email: str):
    send_email.delay(email)
    return {"status": "queued"}
```

## Q79: How does FastAPI handle timeouts?
**A:** FastAPI routes don't have built-in timeouts. Implement with: `asyncio.wait_for(coro, timeout=30)`, middleware timing out slow requests, or ASGI server timeouts (Uvicorn's `--timeout-keep-alive`, Gunicorn's `--timeout`). For long-running tasks, use background tasks or Celery with status polling.


**Code:**
```python
import asyncio
from fastapi import FastAPI

app = FastAPI()

async def slow_work():
    await asyncio.sleep(10)
    return "done"

@app.get("/slow")
async def endpoint():
    return await asyncio.wait_for(slow_work(), timeout=5)
```

## Q80: How do you implement request logging middleware in FastAPI?
**A:** `@app.middleware("http") async def log_requests(request: Request, call_next): start = time.time(); response = await call_next(request); duration = time.time() - start; logger.info(f"{request.method} {request.url.path} {response.status_code} {duration:.3f}s"); return response`. Attach request ID via middleware for tracing.


**Code:**
```python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logger.info(f"{request.method} {request.url.path} {response.status_code} {duration:.3f}s")
    return response
```

## Q81: What is `HTTP/2` support in FastAPI?
**A:** FastAPI (via Uvicorn with `h11` or `httptools`) supports HTTP/1.1. For HTTP/2: use `uvicorn --http h11` with a reverse proxy (NGINX with HTTP/2, or Hypercorn ASGI server which supports HTTP/2). HTTP/2 multiplexing requires proper TLS termination.


**Code:**
```python
# FastAPI/Starlette serve HTTP/1.1; terminate HTTP/2 at a reverse proxy (Caddy/NGINX)
# or run uvicorn with the httptools HTTP parser:
#   uvicorn main:app --http httptools
```

## Q82: How do you implement health checks in FastAPI?
**A:** Simple endpoint: `@app.get("/health") def health(): return {"status": "healthy"}`. Advanced: check DB connectivity, Redis ping, external service availability. Use `@app.get("/ready")` for readiness (dependencies ready) and `@app.get("/live")` for liveness (process alive). Return 200 or 503.


**Code:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/ready")
async def ready():
    return {"status": "ready"}
```

## Q83: What are `middleware` vs `dependencies` in FastAPI?
**A:** Middleware processes every request/response at the ASGI level (before routing). Dependencies are injected into specific routes (after routing). Middleware is broader, dependencies are more granular. Dependencies access route-specific context; middleware accesses raw request. Both can modify request/response.


**Code:**
```python
from fastapi import FastAPI, Depends, Request

app = FastAPI()

@app.middleware("http")
async def mw(request: Request, call_next):
    return await call_next(request)

def get_limit():
    return 10

@app.get("/items")
async def read_items(limit: int = Depends(get_limit)):
    return {"limit": limit}
```

## Q84: How do you handle trailing slashes in FastAPI routes?
**A:** FastAPI (Starlette) with `redirect_slashes=True` (default) redirects `/path` to `/path/` or vice versa based on route definition. Configure with `app = FastAPI()` and Starlette's `Router`. For strict slashes: set `redirect_slashes=False`. Be consistent across routes.


**Code:**
```python
from fastapi import FastAPI

app = FastAPI()

# starlette redirects /items/ -> /items (redirect_slashes=True by default)
@app.get("/items")
async def read_items():
    return []
```

## Q85: What is `HttpUrl` in Pydantic?
**A:** `HttpUrl` is a Pydantic type for URL validation. Ensures valid URL format, scheme (http/https), and max length. Example: `class Config(BaseModel): webhook_url: HttpUrl`. Validates on model creation. Provides parsed attributes like `.scheme`, `.host`, `.path`. Accepts string or pre-parsed URL.


**Code:**
```python
from pydantic import BaseModel, HttpUrl

class Config(BaseModel):
    webhook_url: HttpUrl

cfg = Config(webhook_url="https://example.com/hook")
print(cfg.webhook_url.host)
```

## Q86: How do you implement custom OpenAPI schema generation?
**A:** Use `@app.get("/openapi.json", include_in_schema=False)` to customize or replace OpenAPI schema. Subclass `FastAPI` and override `openapi()` method. Use `get_openapi()` from `fastapi.openapi.utils` for manual construction. Add custom schemas via `openapi_schema` property. Extend with `extra_schemas`.


**Code:**
```python
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    app.openapi_schema = get_openapi(
        title="My API",
        version="2.0.0",
        description="Custom schema",
        routes=app.routes,
    )
    return app.openapi_schema

app.openapi = custom_openapi
```

## Q87: How do you add tags to FastAPI routes?
**A:** `@app.get("/items", tags=["items"])`. Tags group operations in Swagger UI. Define tag metadata: `app = FastAPI(openapi_tags=[{"name": "items", "description": "Item operations"}])`. Tags can include `externalDocs`. Tag schemas auto-generated from route tags.


**Code:**
```python
from fastapi import FastAPI

app = FastAPI(
    openapi_tags=[{"name": "items", "description": "Item operations"}]
)

@app.get("/items", tags=["items"])
async def read_items():
    return []
```

## Q88: What is `JSON` encoding of Pydantic models?
**A:** Pydantic models serialize to JSON via `.model_dump_json()` (v2) or `.json()` (v1). FastAPI uses this internally. Custom encoders: `class Item(BaseModel): model_config = {"json_encoders": {datetime: lambda v: v.isoformat()}}`. Field-level: `@field_serializer`. Use `orjson` for speed.


**Code:**
```python
from pydantic import BaseModel
from datetime import datetime

class Item(BaseModel):
    name: str
    created_at: datetime

item = Item(name="Widget", created_at=datetime.utcnow())
print(item.model_dump_json())
```

## Q89: How do you handle partial updates (PATCH) in FastAPI?
**A:** Use Pydantic model with all fields optional: `class ItemUpdate(BaseModel): name: str | None = None; price: float | None = None`. In route: `@app.patch("/items/{id}") async def update_item(id: int, item: ItemUpdate)`. Apply only non-None fields: `update_data = item.model_dump(exclude_unset=True)`.


**Code:**
```python
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None

@app.patch("/items/{item_id}")
async def update_item(item_id: int, payload: ItemUpdate):
    data = payload.model_dump(exclude_unset=True)
    return {"item_id": item_id, "updated": data}
```

## Q90: What is `Field` in Pydantic?
**A:** `Field()` adds validation and metadata to Pydantic fields. Options: `default`, `default_factory`, `alias`, `title`, `description`, `gt`, `ge`, `lt`, `le`, `min_length`, `max_length`, `regex`, `examples`. Example: `name: str = Field(min_length=1, max_length=100)`. Used with Pydantic models.


**Code:**
```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(ge=0.0, le=1000.0)
```

## Q91: What is `HTTPBasic` auth in FastAPI?
**A:** `from fastapi.security import HTTPBasic, HTTPBasicCredentials; security = HTTPBasic()`. Use: `credentials: HTTPBasicCredentials = Depends(security)`. Provides `username` and `password`. Validate against stored credentials. For production, use hash verification (bcrypt). Not secure over HTTP without TLS.


**Code:**
```python
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

@app.get("/secure")
async def secure(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username}
```

## Q92: How does FastAPI handle large file uploads?
**A:** FastAPI streams files via `UploadFile` (SpooledTemporaryFile) - files are written to disk when exceeding threshold (default 500KB). For very large files: use chunked reading with `file.read(chunk_size)`. Configure limits: Uvicorn's `--limit-concurrency`. Consider direct-to-cloud upload (S3 presigned URLs).


**Code:**
```python
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File()):
    total = 0
    while chunk := await file.read(1024 * 1024):
        total += len(chunk)
    return {"size": total}
```

## Q93: What is `fastapi.testclient` based on?
**A:** `TestClient` is based on `httpx` library (not `requests`). It makes synchronous calls to the ASGI app without running a server. Supports streaming, cookies, headers, file uploads. For async tests, use `httpx.AsyncClient`. TestClient can run as context manager for lifespan events.


**Code:**
```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
```

## Q94: How do you implement rate limiting per user in FastAPI?
**A:** Use user ID (from auth token) as Redis key. Dependency: `async def rate_limit(user: User = Depends(get_current_user)): key = f"rate:{user.id}"; count = await redis.incr(key); if count == 1: await redis.expire(key, 60); if count > 100: raise HTTPException(429)`. Apply with `Depends(rate_limit)`.


**Code:**
```python
from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

async def rate_limit(user=Depends(get_current_user)):
    key = f"rate:{user.id}"
    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, 60)
    if count > 100:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

@app.get("/items", dependencies=[Depends(rate_limit)])
async def read_items():
    return []
```

## Q95: How does FastAPI handle ETag and conditional requests?
**A:** Not built-in. Implement middleware: compute ETag (hash of response body), store ETag in response headers. Check `If-None-Match` request header. If matches: return `304 Not Modified`. Implement `If-Modified-Since` for time-based caching. Use `fastapi-cache` or `starlette-etag` libraries.


**Code:**
```python
import hashlib
from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.middleware("http")
async def etag_middleware(request: Request, call_next):
    response = await call_next(request)
    etag = hashlib.md5(response.body).hexdigest()
    response.headers["ETag"] = etag
    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304)
    return response
```

## Q96: What is `@app.api_route` in FastAPI?
**A:** `@app.api_route("/path", methods=["GET", "POST"])` handles multiple HTTP methods in one function. Less common than specific decorators (`@app.get`, `@app.post`). Useful for simple handlers that respond similarly to different methods. Method-specific decorators are preferred for clarity.


**Code:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.api_route("/ping", methods=["GET", "POST"])
async def ping():
    return {"pong": True}
```

## Q97: How do you implement request ID tracing in FastAPI?
**A:** Middleware generates UUID per request: `request_id = str(uuid.uuid4())`. Add to response headers: `response.headers["X-Request-ID"] = request_id`. Pass to logger with contextvars: `request_id_var.set(request_id)`. Include in log format: `logging.Formatter(fmt="%(request_id)s %(message)s")`.


**Code:**
```python
import uuid
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def request_id(request: Request, call_next):
    rid = uuid.uuid4().hex
    response = await call_next(request)
    response.headers["X-Request-ID"] = rid
    return response
```

## Q98: What is `jsonable_encoder` in FastAPI?
**A:** `jsonable_encoder(data)` converts Pydantic models, datetimes, UUIDs, etc. to JSON-compatible Python types (dicts, lists, strings). Used internally by FastAPI for response serialization. Can be used manually when you need JSON-friendly data. Converts `datetime` to ISO format string.


**Code:**
```python
from fastapi.encoders import jsonable_encoder
from datetime import datetime

data = {"when": datetime.utcnow(), "ids": [1, 2]}
print(jsonable_encoder(data))
```

## Q99: How does FastAPI handle CORS preflight?
**A:** When `CORSMiddleware` is added, FastAPI automatically adds `Access-Control-Allow-Origin` and related headers. Preflight OPTIONS requests are intercepted by the middleware and return 200 with appropriate CORS headers. The middleware runs before route handlers, so preflight never reaches your route code.


**Code:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Q100: What are the best practices for FastAPI project structure?
**A:** Recommended structure: `app/` with `main.py` (app creation), `api/` (routers by resource), `models/` (SQLAlchemy models), `schemas/` (Pydantic models), `core/` (config, security, deps), `crud/` (database operations), `tests/` (test files). Use `APIRouter` for resources. Use dependency injection for cross-cutting concerns. Environment-based config with `BaseSettings`.


**Code:**
```python
# Recommended layout
# app/
#   main.py   -> FastAPI() + include_router
#   api/      -> APIRouter per resource
#   models/   -> SQLAlchemy models
#   schemas/  -> Pydantic schemas
#   core/     -> config, security, deps
#   crud/     -> database operations
#   tests/    -> pytest + TestClient
```
