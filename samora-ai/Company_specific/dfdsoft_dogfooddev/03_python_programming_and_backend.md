# DFDSOFT / DogFoodDev — Python Programming & Backend (100 Q&A)
> Role: AI Coding & Agent Development Specialist  > Candidate: Aayush Gid (Python/FastAPI/Flask/async/APIs/pytest background)

---

## Python Fundamentals

**Q1: What are Python's built-in mutable and immutable data types?**
A: Immutable: `int`, `float`, `str`, `bool`, `tuple`, `frozenset`, `bytes`. Mutable: `list`, `dict`, `set`, `bytearray`. Mutability matters for function arguments — passing a list mutates the caller's object; passing a tuple does not.

**Q2: When would you use a tuple instead of a list?**
A: When the collection should not change — dictionary keys, function return values with fixed structure, or named tuples for lightweight records. Tuples are slightly faster and hashable (if elements are hashable), so they're preferred for fixed-schema data.
```python
Point = tuple[float, float]
def centroid(pts: list[Point]) -> Point:
    return (sum(p[0] for p in pts) / len(pts),
            sum(p[1] for p in pts) / len(pts))
```

**Q3: What is the difference between `is` and `==`?**
A: `==` calls `__eq__` and compares values. `is` checks identity — whether two names refer to the exact same object in memory. Use `is` only for `None`, `True`, `False`, and sentinel objects.
```python
a = [1, 2]
b = [1, 2]
a == b   # True (equal values)
a is b   # False (different objects)
```

**Q4: Explain dictionary comprehensions with a practical example.**
A: A concise way to build dicts from iterables. Common in FastAPI for transforming response payloads or building query param maps.
```python
headers = {"Content-Type": "text/html", "X-Request-Id": "abc", "Authorization": "Bearer tok"}
filtered = {k.lower(): v for k, v in headers.items() if k != "Authorization"}
# {'content-type': 'text/html', 'x-request-id': 'abc'}
```

**Q5: What is the difference between a list comprehension and a generator expression?**
A: List comprehension builds the full list in memory. Generator expression yields items lazily — one at a time — saving memory for large datasets. Use generators for streaming processing; use lists when you need indexing or `len()`.
```python
sum(x * x for x in range(1_000_000))   # generator — constant memory
[x * x for x in range(1_000_000)]      # list — ~40 MB allocated
```

**Q6: How do generators work, and when are they useful in backend services?**
A: Generators use `yield` to produce a sequence lazily. In backends, they're ideal for streaming large CSV/JSON exports or paginating database results without buffering everything in RAM.
```python
def stream_rows(db, batch_size=1000):
    offset = 0
    while True:
        rows = db.execute("SELECT * FROM events LIMIT ? OFFSET ?", batch_size, offset).fetchall()
        if not rows:
            break
        yield from rows
        offset += batch_size
```

**Q7: What is `itertools`, and which functions do you use most?**
A: `itertools` provides fast, memory-efficient iterator tools. Key ones: `chain` (flatten sequences), `groupby` (group consecutive elements), `islice` (slice iterators), `product` (Cartesian product), `combinations`.
```python
from itertools import chain, groupby
combined = chain([1, 2], [3, 4])  # 1,2,3,4
data = sorted(["a-1", "a-2", "b-1"], key=lambda x: x[0])
for key, group in groupby(data, key=lambda x: x[0]):
    print(key, list(group))  # a: ['a-1','a-2'], b: ['b-1']
```

**Q8: Explain context managers and how to write a custom one.**
A: Context managers manage setup/teardown via `with` statement (file handles, DB connections, locks). Implement `__enter__`/`__exit__` or use `contextlib.contextmanager`.
```python
from contextlib import contextmanager

@contextmanager
def db_transaction(connection):
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()

with db_transaction(conn) as cur:
    cur.execute("INSERT INTO logs VALUES (?)", (msg,))
```

**Q9: What are decorators, and how do you write one that preserves the original function's signature?**
A: Decorators are functions that wrap other functions to add behavior. Use `functools.wraps` to preserve `__name__`, `__doc__`, and type hints — critical for FastAPI route introspection.
```python
import functools, time

def retry(max_attempts: int = 3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts:
                        raise
                    time.sleep(2 ** attempt)
        return wrapper
    return decorator

@retry(max_attempts=5)
def call_external_api(url: str) -> dict: ...
```

**Q10: What is a closure, and how does it differ from a decorator?**
A: A closure is a nested function that captures variables from its enclosing scope. A decorator is a specific use of closures — it takes a function and returns a wrapper. All decorators use closures; not all closures are decorators.
```python
def make_multiplier(n):
    def multiplier(x):  # 'n' is captured from enclosing scope
        return x * n
    return multiplier

double = make_multiplier(2)
double(5)  # 10
```

**Q11: What is the difference between `*args` and `**kwargs`?**
A: `*args` collects positional arguments into a tuple. `**kwargs` collects keyword arguments into a dict. Common in FastAPI dependency injection and wrapper functions.
```python
def log_call(func, *args, **kwargs):
    print(f"Calling {func.__name__} with {args}, {kwargs}")
    return func(*args, **kwargs)
```

**Q12: Explain Python's `str` immutability and its performance implications.**
A: Strings are immutable — every concatenation creates a new object. Use `"".join(parts)` for many pieces instead of `+=` in a loop (O(n) vs O(n²)). For f-strings, Python optimizes them internally.
```python
# Bad: O(n²)
result = ""
for word in words:
    result += word + " "

# Good: O(n)
result = " ".join(words)
```

**Q13: What are `__slots__` and when should you use them?**
A: `__slots__` restricts instance attributes to a fixed set, eliminating `__dict__` per instance. Saves memory for millions of instances (e.g., data model objects, ORM rows).
```python
class Point:
    __slots__ = ("x", "y")
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

p = Point(1.0, 2.0)
p.z = 3.0  # AttributeError — no __dict__
```

**Q14: What is the difference between deep copy and shallow copy?**
A: Shallow copy creates a new container but references the same inner objects. Deep copy recursively copies everything. Use `copy.deepcopy()` when nested mutable objects must be independent.
```python
import copy
a = [[1, 2], [3, 4]]
b = copy.copy(a)       # shallow — b[0] is a[0]
c = copy.deepcopy(a)   # deep — c[0] is independent
a[0].append(99)
# b[0] == [1, 2, 99]  (affected)
# c[0] == [1, 2]       (unaffected)
```

**Q15: Explain Python's garbage collection and reference counting.**
A: Python uses reference counting as primary mechanism (object freed when refcount drops to 0) plus a cyclic garbage collector for reference cycles. `gc.collect()` forces collection; `weakref` allows references without preventing cleanup.

---

## OOP in Python

**Q16: How do you define a class with `__init__`, and what is `self`?**
A: `self` is the instance — passed implicitly as first argument to methods. `__init__` is the constructor called after `__new__`.
```python
class Agent:
    def __init__(self, name: str, model: str = "gpt-4"):
        self.name = name
        self.model = model

    def greet(self) -> str:
        return f"I'm {self.name}, running {self.model}"
```

**Q17: Explain single, multiple, and multilevel inheritance. Give a practical example.**
A: Single: one parent. Multiple: multiple parents (Python supports it; watch for diamond problem). Multilevel: chain (A → B → C).
```python
class BaseTool:
    def execute(self): raise NotImplementedError

class APITool(BaseTool):
    def execute(self): return self._call_api()

class APICacheTool(APITool):  # multilevel
    def execute(self):
        if cached := self._get_cache():
            return cached
        return self._call_api()
```

**Q18: What is MRO (Method Resolution Order) and how does C3 linearization work?**
A: MRO determines the order Python searches for methods in inheritance hierarchies. C3 linearization ensures: children before parents, left-to-right in `__bases__`, no class appears before its descendants. Check with `ClassName.__mro__`.
```python
class A:
    def greet(self): return "A"

class B(A):
    def greet(self): return "B"

class C(A):
    def greet(self): return "C"

class D(B, C): pass

print(D.__mro__)  # D → B → C → A → object
D().greet()        # "B" (leftmost first)
```

**Q19: What are dunder methods, and which ones are most important?**
A: Dunder (double underscore) methods define operator overloading and object behavior. Key ones: `__init__`, `__str__`, `__repr__`, `__eq__`, `__lt__`, `__hash__`, `__getitem__`, `__enter__`/`__exit__`, `__call__`.
```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self): return f"Vector({self.x}, {self.y})"
    def __add__(self, other): return Vector(self.x + other.x, self.y + other.y)
    def __abs__(self): return (self.x**2 + self.y**2) ** 0.5
    def __eq__(self, other): return (self.x, self.y) == (other.x, other.y)
```

**Q20: When should you use `@dataclass` vs a regular class?**
A: `@dataclass` auto-generates `__init__`, `__repr__`, `__eq__` from field annotations — perfect for DTOs, config objects, Pydantic-adjacent models. Use regular classes for complex logic.
```python
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class ToolConfig:
    name: str
    timeout: float = 30.0
    retries: int = 3
    tags: list[str] = field(default_factory=list)
```

**Q21: What are `Enum` classes and when do you use them?**
A: Enums represent fixed sets of constants (statuses, roles, API versions). Prefer over raw strings/integers for type safety and readability.
```python
from enum import StrEnum

class AgentStatus(StrEnum):
    IDLE = "idle"
    RUNNING = "running"
    FAILED = "failed"

def handle(status: AgentStatus):
    match status:
        case AgentStatus.IDLE: return "Ready"
        case AgentStatus.RUNNING: return "Busy"
```

**Q22: Explain Abstract Base Classes (ABCs) and when to use them.**
A: ABCs define interfaces via `@abstractmethod` — forcing subclasses to implement specific methods. Use when designing plugin systems, tool registries, or agent base classes.
```python
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @abstractmethod
    def run(self, prompt: str) -> str: ...

    @abstractmethod
    def validate_input(self, prompt: str) -> bool: ...

    def safe_run(self, prompt: str) -> str:
        if not self.validate_input(prompt):
            raise ValueError("Invalid prompt")
        return self.run(prompt)
```

**Q23: Composition vs inheritance — when to choose which?**
A: Composition (has-a) is preferred for flexibility — swap behaviors at runtime, avoid deep inheritance trees. Inheritance (is-a) is appropriate when there's a true Liskov-substitution relationship.
```python
# Composition: flexible, testable
class Agent:
    def __init__(self, llm: LLMBackend, memory: MemoryStore):
        self.llm = llm
        self.memory = memory

# Inheritance: shared interface
class SQLAgent(BaseAgent):  # truly IS a BaseAgent
    ...
```

**Q24: What are properties and when to use them?**
A: `@property` provides getter/setter syntax without changing the calling interface. Use for computed attributes, validation on set, or backward-compatible API changes.
```python
class Config:
    def __init__(self, raw_timeout: float):
        self._raw_timeout = raw_timeout

    @property
    def timeout(self) -> float:
        return self._raw_timeout

    @timeout.setter
    def timeout(self, value: float):
        if value <= 0:
            raise ValueError("Timeout must be positive")
        self._raw_timeout = value
```

**Q25: What is `__new__` vs `__init__`, and when would you override `__new__`?**
A: `__new__` creates the instance (class method), `__init__` initializes it. Override `__new__` for singletons, immutable subclassing (like `str`, `int`), or caching.
```python
class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

---

## Async Programming

**Q26: Explain `async`/`await` and the event loop.**
A: `async def` defines a coroutine; `await` suspends execution until the awaited coroutine completes. The event loop schedules and runs coroutines cooperatively — one runs at a time, switching at `await` points. This enables thousands of concurrent I/O operations on a single thread.
```python
import asyncio

async def fetch(url: str) -> dict:
    reader, writer = await asyncio.open_connection(url, 443)
    writer.write(b"GET / HTTP/1.1\r\nHost: ...\r\n\r\n")
    data = await reader.read(1024)
    return data

async def main():
    results = await asyncio.gather(fetch("a.com"), fetch("b.com"))
```

**Q27: What is the difference between concurrency and parallelism?**
A: Concurrency is dealing with multiple things at once (task switching). Parallelism is doing multiple things at once (multiple CPU cores). Asyncio provides concurrency on one thread; `multiprocessing` provides parallelism across cores. Use async for I/O-bound; multiprocessing for CPU-bound.

**Q28: When would you use threads vs processes vs asyncio?**
A: **Threads**: I/O-bound with blocking libraries (file I/O, some DB drivers). **Processes**: CPU-bound work (pandas transformations, ML inference). **Asyncio**: high-concurrency I/O (API gateways, WebSocket servers, webhooks). In FastAPI, async is default for request handlers.
```python
# CPU-bound: use ProcessPoolExecutor
from concurrent.futures import ProcessPoolExecutor
with ProcessPoolExecutor() as pool:
    results = pool.map(process_chunk, large_dataset)

# I/O-bound: use asyncio or ThreadPoolExecutor
async def handler():
    async with httpx.AsyncClient() as client:
        return await client.get("https://api.example.com")
```

**Q29: What is the GIL, and how does it affect Python concurrency?**
A: The Global Interpreter Lock allows only one thread to execute Python bytecode at a time. This makes threads ineffective for CPU-bound parallelism but irrelevant for I/O-bound work (I/O releases the GIL). For CPU parallelism, use `multiprocessing` or `concurrent.futures.ProcessPoolExecutor`.
```python
# GIL doesn't affect this — I/O releases the lock
async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        return await asyncio.gather(*tasks)
```

**Q30: How do you use `asyncio.gather` vs `asyncio.create_task`?**
A: `gather` runs multiple coroutines concurrently and returns results in order. `create_task` schedules a coroutine and returns a `Task` immediately — useful when you need to start work before awaiting it later.
```python
async def process():
    # gather: wait for all, return list of results
    results = await asyncio.gather(
        fetch_user(uid),
        fetch_orders(uid),
        fetch_preferences(uid),
    )
    return dict(zip(["user", "orders", "prefs"], results))
```

**Q31: What is an async context manager, and how do you write one?**
A: Uses `__aenter__`/`__aexit__` for async resource management. Essential for async DB connections, HTTP sessions, and file I/O in FastAPI.
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_db():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()

async def handler():
    async with get_db() as db:
        rows = await db.fetch("SELECT * FROM users")
```

**Q32: How does async FastAPI work under the hood?**
A: FastAPI uses Starlette, which runs on uvicorn (ASGI server). When a route is `async def`, the event loop handles it directly — no thread pool needed. When it's `def` (sync), FastAPI runs it in a threadpool via `run_in_executor`. Prefer `async def` when doing any I/O inside the handler.
```python
from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/proxy")
async def proxy_endpoint():
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.example.com/data")
        return resp.json()  # non-blocking
```

**Q33: What is `aiohttp`, and when would you use it over `httpx`?**
A: `aiohttp` is a mature async HTTP client/server library. `httpx` has a cleaner API and supports both sync/async. Use `aiohttp` for long-lived server connections or when you need its connector pooling; use `httpx` for simpler client code in FastAPI projects.
```python
# aiohttp client
async with aiohttp.ClientSession() as session:
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
        data = await resp.json()

# httpx async client (preferred for new projects)
async with httpx.AsyncClient(timeout=10) as client:
    resp = await client.get(url)
    data = resp.json()
```

**Q34: How do you handle exceptions inside async code?**
A: Use `try`/`except` inside coroutines just like sync code. In `asyncio.gather`, pass `return_exceptions=True` to prevent one failure from cancelling all tasks. For background tasks, always wrap in try/except.
```python
async def safe_task(name: str):
    try:
        await risky_operation()
    except Exception as e:
        logger.error(f"Task {name} failed: {e}")

results = await asyncio.gather(*[safe_task(f"t-{i}") for i in range(5)])
```

**Q35: What are Python async generators, and how do they differ from regular generators?**
A: Async generators use `async for` and `yield` — they produce values asynchronously. Useful for streaming data from async sources (DB cursors, WebSocket messages).
```python
async def stream_events(source):
    async for message in source:
        yield json.loads(message)

async def handler(websocket: WebSocket):
    async for event in stream_events(websocket):
        await process_event(event)
```

---

## FastAPI

**Q36: How do you define a basic FastAPI route with path and query parameters?**
A: Path parameters are defined in the URL string; query parameters come from function signature defaults. FastAPI validates types automatically via Pydantic.
```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/agents/{agent_id}")
async def get_agent(
    agent_id: int,
    verbose: bool = Query(False, description="Include full logs"),
):
    agent = await db.get_agent(agent_id)
    if verbose:
        agent["logs"] = await db.get_logs(agent_id)
    return agent
```

**Q37: Explain request body validation with Pydantic models.**
A: Pydantic `BaseModel` defines the request body schema. FastAPI parses JSON, validates types, and raises 422 on failure automatically.
```python
from pydantic import BaseModel, Field

class CreateAgentRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    model: str = Field(default="gpt-4", pattern="^(gpt-4|gpt-3.5-turbo|claude-3)$")
    system_prompt: str = Field(default="", max_length=10000)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

@app.post("/agents", status_code=201)
async def create_agent(req: CreateAgentRequest):
    return {"id": generate_id(), "config": req.model_dump()}
```

**Q38: How do you structure response models to control what gets returned?**
A: Use `response_model` to exclude internal fields (like passwords, internal IDs) from the response. Pydantic strips extra fields automatically.
```python
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = await db.get_user(user_id)
    return user  # password_hash, internal fields stripped automatically
```

**Q39: How does FastAPI dependency injection work? Give a practical example.**
A: Dependencies are functions/classes declared in route signatures via `Depends()`. FastAPI resolves them, caches per-request, and handles cleanup. Perfect for DB sessions, auth, and shared logic.
```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@app.get("/me")
async def read_me(user = Depends(get_current_user)):
    return {"user_id": user.id, "email": user.email}
```

**Q40: What are middleware and how do you add custom middleware in FastAPI?**
A: Middleware runs before/after every request — for logging, CORS, auth, metrics. Add via `app.add_middleware()`.
```python
from fastapi import Request
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{duration:.4f}"
    return response
```

**Q41: How do you handle errors globally in FastAPI?**
A: Use `exception_handler` to catch specific exceptions across the app. Return consistent error responses.
```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

class AgentNotFound(Exception):
    def __init__(self, agent_id: int):
        self.agent_id = agent_id

app = FastAPI()

@app.exception_handler(AgentNotFound)
async def agent_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": f"Agent {exc.agent_id} not found"},
    )
```

**Q42: How do you use background tasks in FastAPI?**
A: `BackgroundTasks` runs functions after sending the response — for sending emails, writing logs, or triggering webhooks. Dependencies can also add background tasks.
```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

def send_notification(user_id: int, message: str):
    email_service.send(user_id, message)

@app.post("/agents/{agent_id}/trigger")
async def trigger_agent(agent_id: int, bg: BackgroundTasks):
    result = await run_agent(agent_id)
    bg.add_task(send_notification, result.user_id, f"Agent finished: {result.status}")
    return {"status": "triggered"}
```

**Q43: How do you implement WebSocket endpoints in FastAPI?**
A: Use `@app.websocket("/ws")` for real-time bidirectional communication. Manage connections with a set for broadcasting.
```python
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active.remove(ws)

    async def broadcast(self, message: str):
        for conn in self.active:
            await conn.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/agent/{agent_id}")
async def agent_ws(websocket: WebSocket, agent_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            result = await process_agent_input(agent_id, data)
            await websocket.send_json(result)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

**Q44: How do you document your FastAPI app with OpenAPI?**
A: FastAPI generates OpenAPI docs automatically from type hints and Pydantic models. Customize with `tags`, `summary`, `description`, `response_description`. Access at `/docs` (Swagger UI) or `/redoc`.
```python
@app.post(
    "/agents",
    tags=["agents"],
    summary="Create a new agent",
    description="Creates an AI agent with the given configuration.",
    response_model=AgentResponse,
    status_code=201,
)
async def create_agent(req: CreateAgentRequest): ...
```

**Q45: How do you mount a sub-application or router in FastAPI?**
A: Use `app.include_router()` for grouping routes, or `app.mount()` for separate ASGI apps (like serving static files or a separate FastAPI app).
```python
from fastapi import APIRouter

agent_router = APIRouter(prefix="/agents", tags=["agents"])
agent_router.get("/{id}")(get_agent)
agent_router.post("")(create_agent)

app.include_router(agent_router)

# Mount static files
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
```

**Q46: How do you implement pagination in FastAPI?**
A: Use query parameters for `offset`/`limit` or cursor-based pagination. Return metadata alongside results.
```python
from fastapi import Query

class PaginatedResponse(BaseModel):
    items: list[dict]
    total: int
    offset: int
    limit: int
    has_more: bool

@app.get("/agents", response_model=PaginatedResponse)
async def list_agents(offset: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    total = await db.count_agents()
    items = await db.get_agents(offset=offset, limit=limit)
    return PaginatedResponse(
        items=items, total=total, offset=offset, limit=limit,
        has_more=(offset + limit) < total,
    )
```

**Q47: How do you handle file uploads in FastAPI?**
A: Use `UploadFile` for streaming uploads (handles large files without loading into memory) or `bytes` for small files.
```python
from fastapi import UploadFile, File

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    # For large files: stream to disk
    with open(f"uploads/{file.filename}", "wb") as f:
        while chunk := await file.read(8192):
            f.write(chunk)
    return {"filename": file.filename, "size": len(content)}
```

**Q48: How do you implement rate limiting in FastAPI?**
A: Use `slowapi` or implement a token-bucket algorithm with Redis. Rate limiting prevents abuse and protects downstream services.
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/api/data")
@limiter.limit("100/minute")
async def get_data(request: Request):
    return {"data": await fetch_data()}
```

**Q49: How do you manage CORS in FastAPI?**
A: Use `CORSMiddleware` to specify allowed origins, methods, and headers. In development, allow all origins; in production, whitelist specific domains.
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dogfooddev.dfsoft.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Q50: How do you test a FastAPI app?**
A: Use `TestClient` from Starlette (sync) or `httpx.AsyncClient` (async) to make requests against the app in tests.
```python
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

# Sync
client = TestClient(app)
response = client.post("/agents", json={"name": "test-agent"})
assert response.status_code == 201

# Async
async def test_create_agent():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/agents", json={"name": "test"})
        assert resp.status_code == 201
```

---

## Flask

**Q51: What are Flask blueprints and how do you use them?**
A: Blueprints modularize Flask applications — grouping routes, templates, and static files into reusable components. Essential for scaling beyond a single file.
```python
from flask import Blueprint

agents_bp = Blueprint("agents", __name__, url_prefix="/agents")

@agents_bp.route("/<int:agent_id>")
def get_agent(agent_id):
    return {"id": agent_id}

# In app factory
app.register_blueprint(agents_bp)
```

**Q52: Explain Flask's request and application context.**
A: Flask uses application context (`g`, `current_app`) and request context (`request`, `session`) — thread-local proxies that let you access request data without passing it everywhere. Pushed/popped automatically per request.
```python
from flask import request, g, current_app

@app.before_request
def load_user():
    g.user = db.get_user(request.headers.get("X-User-Id"))

@app.route("/data")
def get_data():
    return {"user": g.user.name, "app": current_app.config["ENV"]}
```

**Q53: How does Flask session management work?**
A: Flask uses signed cookies for client-side sessions (default) or server-side sessions via extensions like `Flask-Session`. The session is a dict accessible from anywhere in the request.
```python
from flask import session

@app.route("/login", methods=["POST"])
def login():
    user = authenticate(request.form["email"], request.form["password"])
    session["user_id"] = user.id
    session.permanent = True  # use PERMANENT_SESSION_LIFETIME
    return {"status": "logged_in"}
```

**Q54: How do you structure a Flask project for production?**
A: Use the application factory pattern with blueprints, separate config files, and a `wsgi.py` entrypoint. Follow the "Flask 2.x+" pattern.
```
project/
├── wsgi.py
├── config.py
├── app/
│   ├── __init__.py      # create_app()
│   ├── models.py
│   ├── agents/
│   │   ├── __init__.py  # Blueprint
│   │   └── routes.py
│   └── templates/
```

**Q55: What is Flask-RESTful and when should you use it?**
A: Flask-RESTful adds class-based views for REST APIs with automatic request parsing and output formatting. Use when building structured REST APIs with Flask (though FastAPI is often preferred for new projects).
```python
from flask_restful import Resource, reqparse

class AgentResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True)

    def get(self, agent_id):
        return get_agent(agent_id)

    def put(self, agent_id):
        args = self.parser.parse_args()
        return update_agent(agent_id, args)
```

**Q56: How do you handle authentication in Flask?**
A: Use Flask-Login for session-based auth or Flask-JWT-Extended for token-based auth. For APIs, JWT is preferred.
```python
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@app.route("/login", methods=["POST"])
def login():
    user = User.query.filter_by(email=request.json["email"]).first()
    if user and user.check_password(request.json["password"]):
        token = create_access_token(identity=user.id)
        return {"access_token": token}
    return {"error": "Invalid credentials"}, 401

@app.route("/protected")
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    return {"user_id": user_id}
```

**Q57: What is Jinja2, and how do you use it effectively in Flask?**
A: Jinja2 is Flask's default templating engine — supports template inheritance, macros, filters, and control structures. Use `{{ }}` for expressions, `{% %}` for statements.
```python
# base.html
<!DOCTYPE html>
<html>
<head><title>{% block title %}{% endblock %}</title></head>
<body>
    {% block content %}{% endblock %}
</body>
</html>

# agent.html
{% extends "base.html" %}
{% block title %}Agent {{ agent.name }}{% endblock %}
{% block content %}
<h1>{{ agent.name }}</h1>
<p>Status: {{ agent.status | upper }}</p>
{% endblock %}
```

**Q58: What are the key differences between Flask and FastAPI?**
A: Flask is synchronous by default (WSGI); FastAPI is async-native (ASGI). FastAPI includes auto-generated OpenAPI docs, Pydantic validation, and dependency injection built-in. Flask is more mature with a larger ecosystem. For new API projects, FastAPI is generally preferred; for existing Flask apps or server-rendered pages, Flask remains solid.

---

## Testing

**Q59: How do you write pytest fixtures, and where do you put them?**
A: Fixtures are functions decorated with `@pytest.fixture` that provide test setup/teardown. Put shared fixtures in `conftest.py` (auto-discovered by pytest).
```python
# conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def sample_agent():
    return {"name": "test-agent", "model": "gpt-4", "temperature": 0.7}
```

**Q60: How does `@pytest.mark.parametrize` work?**
A: Runs the same test with multiple input sets — reduces duplication and makes edge cases explicit.
```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("", 0),
    ("a" * 1000, 1000),
    ("  spaces  ", 9),
])
def test_string_length(input, expected):
    assert len(input.strip()) == expected

@pytest.mark.parametrize("model", ["gpt-4", "gpt-3.5-turbo", "claude-3"])
def test_model_availability(model):
    assert model in supported_models()
```

**Q61: Explain pytest markers and how to use custom ones.**
A: Markers tag tests for selective execution: `@pytest.mark.slow`, `@pytest.mark.skip`, `@pytest.mark.xfail`. Register custom markers in `pyproject.toml`.
```python
# pyproject.toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks integration tests",
]

# Usage
@pytest.mark.integration
@pytest.mark.slow
async def test_full_agent_pipeline():
    ...

# Run only integration tests
# pytest -m integration
```

**Q62: How do you mock external services in pytest?**
A: Use `unittest.mock` or `pytest-mock` to replace external calls. `monkeypatch` fixture is pytest's built-in for patching.
```python
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_llm():
    with patch("app.agents.llm.LLMClient.generate", new_callable=AsyncMock) as m:
        m.return_value = {"text": "Mocked response", "tokens": 42}
        yield m

async def test_agent_runs(mock_llm):
    result = await agent.run("Hello")
    assert result == "Mocked response"
    mock_llm.assert_called_once()
```

**Q63: What is `conftest.py` and why is it important?**
A: `conftest.py` is pytest's plugin/configuration file — fixtures defined here are automatically available to all tests in the directory and subdirectories. It's also used for hooks, custom markers, and test session setup.
```python
# conftest.py
import pytest

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    db = create_test_database()
    yield db
    db.drop_all()
```

**Q64: How do you test async functions with pytest?**
A: Install `pytest-asyncio` and mark tests with `@pytest.mark.asyncio`. Configure `asyncio_mode = "auto"` in `pyproject.toml` to skip the decorator.
```python
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"

# test file
async def test_fetch_agent(client):
    resp = await client.get("/agents/1")
    assert resp.status_code == 200
```

**Q65: How do you measure test coverage?**
A: Use `pytest-cov` to generate coverage reports. Aim for >80% on business logic; 100% is often impractical.
```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
```
```python
# pyproject.toml
[tool.coverage.run]
source = ["app"]
omit = ["app/tests/*", "app/migrations/*"]

[tool.coverage.report]
fail_under = 80
show_missing = true
```

**Q66: What is TDD and how do you practice it?**
A: Test-Driven Development: write a failing test first, write minimal code to pass, then refactor. Red → Green → Refactor cycle. Forces clear requirements and catches edge cases early.
```python
# Step 1: Write failing test
def test_calculate_token_cost():
    assert calculate_cost(input_tokens=1000, output_tokens=500, model="gpt-4") == 0.045

# Step 2: Implement minimally
def calculate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    rates = {"gpt-4": (0.03, 0.06), "gpt-3.5-turbo": (0.001, 0.002)}
    in_rate, out_rate = rates[model]
    return (input_tokens * in_rate + output_tokens * out_rate) / 1000

# Step 3: Refactor if needed
```

**Q67: How do you test FastAPI endpoints with authentication?**
A: Mock the auth dependency or create test tokens. Use dependency overrides for test isolation.
```python
from app.auth import get_current_user

def override_get_current_user():
    return User(id=1, email="test@example.com", role="admin")

app.dependency_overrides[get_current_user] = override_get_current_user

def test_protected_endpoint(client):
    resp = client.get("/admin/dashboard")
    assert resp.status_code == 200
```

**Q68: What is the difference between unit, integration, and end-to-end tests?**
A: **Unit**: test individual functions/classes in isolation (fast, many). **Integration**: test multiple components together (DB + API, moderate speed). **E2E**: test full user flows through HTTP (slow, few). Aim for pyramid: many unit, some integration, few E2E.
```python
# Unit
def test_parse_agent_config():
    config = parse_config({"name": "a", "temp": 0.5})
    assert config.temperature == 0.5

# Integration
async def test_create_agent_db(client, db):
    resp = await client.post("/agents", json={"name": "test"})
    assert resp.status_code == 201
    assert await db.get_agent(resp.json()["id"]) is not None

# E2E
async def test_full_agent_lifecycle(client):
    create = await client.post("/agents", json={"name": "e2e"})
    agent_id = create.json()["id"]
    run = await client.post(f"/agents/{agent_id}/run", json={"prompt": "hi"})
    assert run.json()["status"] == "completed"
```

**Q69: How do you handle database testing (test isolation)?**
A: Use transactions that roll back after each test, or create/destroy test databases per test session. For async DBs, use async fixtures.
```python
@pytest.fixture
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        transaction = await conn.begin()
        session = AsyncSession(bind=conn)
        yield session
        await transaction.rollback()
        await session.close()
```

**Q70: How do you test error handling and edge cases effectively?**
A: Use `pytest.raises` for expected exceptions, test boundary values, and verify error response shapes. Always test auth failures, validation errors, and 404s.
```python
import pytest
from fastapi import HTTPException

async def test_agent_not_found(client):
    resp = await client.get("/agents/999999")
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()

def test_invalid_config_rejected():
    with pytest.raises(ValidationError) as exc_info:
        CreateAgentRequest(name="", temperature=-1.0)
    assert "name" in str(exc_info.value)
    assert "temperature" in str(exc_info.value)
```

---

## API Design & Authentication

**Q71: What makes an API RESTful?**
A: REST uses: resources as URLs (`/agents/{id}`), HTTP methods for actions (GET/POST/PUT/DELETE), stateless requests, proper status codes, HATEOAS links, and content negotiation via Accept headers.
```python
# RESTful routes
POST   /agents          → 201 Created
GET    /agents           → 200 OK (list)
GET    /agents/{id}      → 200 OK / 404 Not Found
PUT    /agents/{id}      → 200 OK / 422 Invalid
DELETE /agents/{id}      → 204 No Content
```

**Q72: When should you use PUT vs PATCH vs POST?**
A: **POST**: create new resource. **PUT**: full replace of a resource (client sends complete representation). **PATCH**: partial update (only changed fields). PUT is idempotent; PATCH may or may not be.
```python
@app.put("/agents/{id}", response_model=AgentResponse)
async def replace_agent(id: int, data: AgentFullUpdate):
    """Client must send ALL fields — complete replacement."""
    return await db.replace_agent(id, data)

@app.patch("/agents/{id}", response_model=AgentResponse)
async def update_agent(id: int, data: AgentPartialUpdate):
    """Client sends only fields to change."""
    return await db.update_agent(id, data.model_dump(exclude_unset=True))
```

**Q73: What HTTP status codes should every developer know?**
A: **2xx**: 200 OK, 201 Created, 204 No Content. **3xx**: 301 Moved, 304 Not Modified. **4xx**: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable, 429 Too Many Requests. **5xx**: 500 Internal Error, 502 Bad Gateway, 503 Service Unavailable.

**Q74: How does JWT authentication work?**
A: Server signs a payload (user ID, role, expiry) with a secret key → token. Client sends token in `Authorization: Bearer <token>`. Server verifies signature (no DB lookup needed). Stateless and scalable.
```python
from datetime import datetime, timedelta
import jwt

SECRET = "your-secret-key"

def create_token(user_id: int, role: str) -> str:
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
```

**Q75: What is OAuth2 and how is it different from JWT?**
A: OAuth2 is an authorization framework (not authentication). JWT is a token format. OAuth2 often uses JWTs as access tokens. OAuth2 supports flows for third-party access (Google login, API access grants). In FastAPI, use `OAuth2PasswordBearer` for the password flow.
```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate(form.username, form.password)
    if not user:
        raise HTTPException(401)
    return {"access_token": create_token(user.id), "token_type": "bearer"}
```

**Q76: What are API keys and when should you use them?**
A: Simple tokens passed in headers (`X-API-Key: ...`) for server-to-server auth. Use for machine-to-machine communication, rate limiting by client, and simple integrations. Less secure than OAuth2 for user-facing apps.
```python
from fastapi import Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(key: str = Security(api_key_header)):
    if key not in VALID_API_KEYS:
        raise HTTPException(403, "Invalid API key")
    return key
```

**Q77: How do you implement CORS properly in production?**
A: Never use `allow_origins=["*"]` in production. Whitelist specific origins. Use environment variables for origins to avoid hardcoding.
```python
import os

ALLOWED_ORIGINS = os.environ.get("CORS_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=3600,
)
```

**Q78: What are webhooks and how do you implement them safely?**
A: Webhooks are HTTP callbacks your API sends when events happen. Implement with: payload signing (HMAC), retry logic, idempotency keys, and a webhook event log.
```python
import hmac, hashlib

def sign_payload(payload: bytes, secret: str) -> str:
    return hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()

@app.post("/webhooks/outbound")
async def send_webhook(event: WebhookEvent):
    payload = json.dumps(event.dict()).encode()
    signature = sign_payload(payload, WEBHOOK_SECRET)
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            event.callback_url,
            content=payload,
            headers={"X-Webhook-Signature": signature, "Content-Type": "application/json"},
            timeout=10,
        )
```

**Q79: How do you version your API?**
A: Common strategies: URL path (`/v1/agents`), header (`Accept: application/vnd.api.v1+json`), or query param (`?version=1`). URL path is simplest and most common.
```python
v1 = APIRouter(prefix="/v1", tags=["v1"])
v2 = APIRouter(prefix="/v2", tags=["v2"])

@v1.get("/agents")
async def list_agents_v1(): ...

@v2.get("/agents")
async def list_agents_v2():  # different response format
    ...

app.include_router(v1)
app.include_router(v2)
```

**Q80: What is rate limiting and how do you implement it?**
A: Limits requests per client/time window to prevent abuse. Implement with Redis-backed token bucket or sliding window algorithms.
```python
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

limiter = Limiter(key_func=get_remote_address, storage_uri="redis://localhost:6379")

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(status_code=429, content={"error": "Rate limit exceeded"})

@app.get("/search")
@limiter.limit("10/second")
async def search(request: Request, q: str):
    return await perform_search(q)
```

---

## File I/O & Data Processing

**Q81: How do you work with files using `pathlib`?**
A: `pathlib` provides object-oriented paths — cleaner than `os.path`. Use it for all file operations.
```python
from pathlib import Path

config_dir = Path("config")
config_dir.mkdir(exist_ok=True)

# Read/write
config_file = config_dir / "settings.json"
config_file.write_text(json.dumps({"debug": True}))
data = json.loads(config_file.read_text())

# Glob
for py_file in Path("src").rglob("*.py"):
    print(py_file.relative_to("src"))

# Iterate
for p in Path(".").iterdir():
    if p.is_file() and p.suffix == ".log":
        print(p.name, p.stat().st_size)
```

**Q82: How do you handle JSON serialization/deserialization efficiently?**
A: Use `json` for standard cases, `orjson` for performance (3-6x faster), and handle date/datetime with custom encoders.
```python
import json
from datetime import datetime

# Standard
data = json.loads('{"ts": "2024-01-15T10:30:00Z"}')

# With custom encoder
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

json.dumps({"timestamp": datetime.now()}, cls=DateTimeEncoder)

# orjson (fast)
import orjson
data = orjson.loads(b'{"key": "value"}')  # returns dict
payload = orjson.dumps({"key": "value"})   # returns bytes
```

**Q83: How do you read and write CSV files in Python?**
A: Use `csv.DictReader`/`DictWriter` for labeled columns, or `pandas` for complex transformations. For large files, process line-by-line.
```python
import csv
from pathlib import Path

# Read
with open("data.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        process(row["name"], row["email"])

# Write
with open("output.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "name", "status"])
    writer.writeheader()
    writer.writerows(records)

# Large file: pandas chunked read
import pandas as pd
for chunk in pd.read_csv("huge.csv", chunksize=10_000):
    process(chunk)
```

**Q84: When and how do you use pandas in a backend service?**
A: Use pandas for data transformation, aggregation, and reporting. In async FastAPI, run CPU-bound pandas operations in a thread/process pool to avoid blocking the event loop.
```python
import pandas as pd
from concurrent.futures import ProcessPoolExecutor

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("category")
        .agg(total=("value", "sum"), count=("value", "count"))
        .sort_values("total", ascending=False)
    )

@app.post("/reports/summary")
async def generate_summary(data: list[dict]):
    df = pd.DataFrame(data)
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, transform_data, df)
    return result.to_dict(orient="records")
```

**Q85: How do you handle large file uploads without running out of memory?**
A: Stream the upload to disk in chunks instead of loading everything into memory. Use FastAPI's `UploadFile` which supports async reading.
```python
from fastapi import UploadFile, File

CHUNK_SIZE = 8192

@app.post("/upload/large")
async def upload_large(file: UploadFile = File(...)):
    total = 0
    with open(f"uploads/{file.filename}", "wb") as buffer:
        while chunk := await file.read(CHUNK_SIZE):
            buffer.write(chunk)
            total += len(chunk)
    return {"filename": file.filename, "bytes": total}
```

**Q86: How do you implement streaming responses in FastAPI?**
A: Use `StreamingResponse` to send data in chunks — for large JSON exports, log streams, or SSE (Server-Sent Events).
```python
from fastapi.responses import StreamingResponse
import json

async def event_generator():
    for i in range(100):
        yield f"data: {json.dumps({'progress': i})}\n\n"
    yield "data: [DONE]\n\n"

@app.get("/stream")
async def stream_endpoint():
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

**Q87: How do you work with `io.BytesIO` and `io.StringIO`?**
A: In-memory file-like objects — useful for testing, passing binary/string data to APIs that expect file handles, or buffering.
```python
import io
import pandas as pd

# Test without writing to disk
csv_buffer = io.StringIO()
csv_buffer.write("name,score\nAlice,95\nBob,87\n")
csv_buffer.seek(0)
df = pd.read_csv(csv_buffer)

# Binary buffer
pdf_buffer = io.BytesIO()
generate_pdf(report_data, output=pdf_buffer)
pdf_buffer.seek(0)
```

**Q88: How do you process data from multiple sources (e.g., CSV + API + DB) in a pipeline?**
A: Abstract each source behind a common interface, use generators for lazy loading, and compose transformations.
```python
from typing import Iterator

def from_csv(path: str) -> Iterator[dict]:
    with open(path) as f:
        yield from csv.DictReader(f)

async def from_api(url: str) -> Iterator[dict]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        yield from resp.json()["results"]

def merge_streams(*streams: Iterator) -> Iterator[dict]:
    seen = set()
    for stream in streams:
        for record in stream:
            key = record["id"]
            if key not in seen:
                seen.add(key)
                yield record
```

---

## Error Handling & Debugging

**Q89: What is the correct `try`/`except` pattern in Python?**
A: Catch specific exceptions — never bare `except`. Use `except Exception as e` as last resort. Always include `else` (success path) and `finally` (cleanup) when needed.
```python
try:
    result = await call_api(url)
except httpx.TimeoutException:
    logger.warning("API timeout, retrying...")
    result = await call_api(url, timeout=30)
except httpx.HTTPStatusError as e:
    if e.response.status_code == 429:
        raise RateLimitedError()
    raise
else:
    cache.set(url, result, ttl=300)
finally:
    connection_pool.release(conn)
```

**Q90: How do you create custom exception classes?**
A: Create specific exception hierarchies for your domain. Include context data in the exception for structured error handling.
```python
class AppError(Exception):
    """Base exception for all app errors."""
    def __init__(self, message: str, code: str = "UNKNOWN"):
        super().__init__(message)
        self.code = code

class AgentError(AppError):
    def __init__(self, agent_id: int, message: str):
        super().__init__(message, code="AGENT_ERROR")
        self.agent_id = agent_id

class LLMError(AppError):
    def __init__(self, model: str, reason: str):
        super().__init__(f"LLM {model} failed: {reason}", code="LLM_ERROR")
        self.model = model
```

**Q91: Explain exception chaining with `raise ... from ...`.**
A: Preserves the original exception as `__context__` — essential for debugging when wrapping exceptions. Use `raise NewError("msg") from original_error`.
```python
try:
    raw = json.loads(response.text)
except json.JSONDecodeError as e:
    raise APIResponseError(f"Invalid JSON from {url}") from e

# In traceback, you see both:
# APIResponseError: Invalid JSON from https://...
# The above exception was the direct cause of the following exception:
# json.decoder.JSONDecodeError: ...
```

**Q92: How do you set up structured logging in a FastAPI project?**
A: Use `structlog` for JSON-structured logs — machine-readable, grep-friendly, with context binding.
```python
import structlog

logger = structlog.get_logger()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    log = logger.bind(method=request.method, path=request.url.path)
    log.info("request_started")
    response = await call_next(request)
    log.info("request_completed", status=response.status_code)
    return response

# Bind context per-request
log = logger.bind(user_id=user.id, agent_id=agent.id)
log.info("agent_started", model="gpt-4")
log.error("agent_failed", error=str(e), duration=2.3)
```

**Q93: How do you use the Python debugger effectively?**
A: Use `breakpoint()` (Python 3.7+) instead of `import pdb; pdb.set_trace()`. For async debugging, use `aiodebug` or `breakpoint()` with uvicorn's `--reload`. For production debugging, use `py-spy` or ` Austin`.
```python
def complex_calculation(data):
    result = transform(data)
    breakpoint()  # drops into debugger here
    return finalize(result)

# pdb commands:
# n (next line)  s (step into)  c (continue)
# p variable     l (list code)  q (quit)
# w (where)      h (help)       b 10 (breakpoint at line 10)
```

**Q94: What are the best practices for error responses in APIs?**
A: Return consistent error shape with error code, message, and optional details. Use HTTP status codes correctly. Log errors server-side with full context.
```python
class ErrorResponse(BaseModel):
    error: str
    code: str
    details: dict | None = None
    request_id: str | None = None

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    logger.error("app_error", error=str(exc), code=exc.code, path=request.url.path)
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error=str(exc),
            code=exc.code,
            request_id=request.state.request_id,
        ).model_dump(),
    )
```

**Q95: How do you debug slow queries or slow API endpoints?**
A: Use `cProfile` for CPU profiling, `pyinstrument` for wall-clock profiling, and database query logging. In FastAPI, add timing middleware.
```python
import cProfile
import pyinstrument

# CPU profiling
cProfile.run("process_data()", "profile_output")
# Then: snakeviz profile_output

# Wall-clock (shows I/O waits)
profiler = pyinstrument.Profiler()
profiler.start()
result = await complex_operation()
profiler.stop()
profiler.print()
```

---

## Python Best Practices

**Q96: How do you use type hints effectively in Python?**
A: Type hints improve IDE support, catch bugs early, and serve as documentation. Use `Optional[X]` (or `X | None` in 3.10+), `Literal`, `Protocol`, and `TypeVar` for generics.
```python
from typing import Protocol, TypeVar
from collections.abc import Callable

# Basic
def process(agent_id: int, config: dict[str, Any] | None = None) -> AgentResponse: ...

# Protocol (structural typing)
class Serializable(Protocol):
    def to_dict(self) -> dict: ...

def save(item: Serializable) -> None:
    db.insert(item.to_dict())

# TypeVar for generics
T = TypeVar("T")
def first(items: list[T]) -> T | None:
    return items[0] if items else None
```

**Q97: How do you manage Python virtual environments and dependencies?**
A: Always use isolated environments. `uv` is fastest (Rust-based), `poetry` for dependency management, `pip` + `venv` for simplicity. Pin exact versions in production.
```bash
# uv (fastest)
uv venv .venv
uv pip install fastapi uvicorn httpx pytest

# poetry
poetry init
poetry add fastapi uvicorn
poetry add --group dev pytest pytest-asyncio

# pip + venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Q98: What code quality tools should you use and how do you configure them?**
A: `ruff` (linting + formatting, replaces flake8/black/isort), `mypy` (static type checking), `pre-commit` (git hooks). Configure in `pyproject.toml`.
```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "SIM", "ASYNC"]

[tool.mypy]
python_version = "3.11"
strict = true
plugins = ["pydantic.mypy", "pydantic.mypy"]

[tool.ruff.format]
quote-style = "double"
```

**Q99: What is the ideal project structure for a FastAPI backend?**
A: Layered architecture: routers (HTTP layer) → services (business logic) → repositories (data access). Keep dependencies flowing inward.
```
project/
├── pyproject.toml
├── alembic/           # DB migrations
├── app/
│   ├── __init__.py
│   ├── main.py        # FastAPI app creation
│   ├── config.py      # Settings via pydantic-settings
│   ├── dependencies.py
│   ├── models/        # DB models (SQLAlchemy)
│   ├── schemas/       # Pydantic request/response
│   ├── routers/       # API routes
│   │   ├── agents.py
│   │   └── users.py
│   ├── services/      # Business logic
│   │   ├── agent_service.py
│   │   └── llm_service.py
│   └── utils/
├── tests/
│   ├── conftest.py
│   ├── test_agents.py
│   └── test_users.py
└── docker-compose.yml
```

**Q100: How do you package and distribute a Python project?**
A: Use `pyproject.toml` (PEP 621) as single source of truth. For libraries: build with `build` package, publish to PyPI. For applications: Docker containerization is standard.
```toml
# pyproject.toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "agent-toolkit"
version = "0.1.0"
description = "AI agent development toolkit"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.104",
    "pydantic>=2.5",
    "httpx>=0.25",
]

[project.optional-dependencies]
dev = ["pytest>=7.4", "pytest-asyncio", "ruff", "mypy"]
```
```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir .
COPY app/ app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
