# 10 - APIRouter

## Table of Contents

1. [APIRouter Usage](#apirouter-usage)
2. [Mounting Routers](#mounting-routers)
3. [Router Prefixes](#router-prefixes)
4. [Router Tags](#router-tags)
5. [Router Dependencies](#router-dependencies)
6. [Router-level Responses](#router-level-responses)
7. [Organizing Routes by Feature](#organizing-routes-by-feature)
8. [Nested Routers](#nested-routers)
9. [Including Routers Dynamically](#including-routers-dynamically)
10. [Router Best Practices for Large Apps](#router-best-practices-for-large-apps)
11. [Interview Questions](#interview-questions)

---

## APIRouter Usage

`APIRouter` is FastAPI's mechanism for splitting your application into separate, modular route files. Instead of defining all endpoints in one file, you create routers for different features and include them in your main app.

### Basic Usage

```python
# app/routers/users.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/users/")
async def list_users():
    return [{"id": 1, "name": "John"}]

@router.post("/users/", status_code=201)
async def create_user(user: UserCreate):
    return {"id": 1, **user.model_dump()}
```

```python
# app/main.py
from fastapi import FastAPI
from app.routers import users

app = FastAPI()
app.include_router(users.router)
```

### Router vs App

`APIRouter` has the same interface as `FastAPI`. You can use the same decorators:

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/")           # ✅ Works
@router.post("/")          # ✅ Works
@router.put("/")           # ✅ Works
@router.delete("/")        # ✅ Works
@router.patch("/")         # ✅ Works
@router.api_route("/")     # ✅ Works
@router.exception_handler  # ✅ Works
@router.middleware("http") # ✅ Works
```

### Full Router Example

```python
# app/routers/items.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

router = APIRouter()

class Item(BaseModel):
    name: str
    price: float

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float

# In-memory storage
items_db: dict[int, Item] = {}
next_id = 1

@router.get("/items/", response_model=list[ItemResponse])
async def list_items(skip: int = 0, limit: int = 10):
    items = list(items_db.values())
    return items[skip: skip + limit]

@router.post("/items/", response_model=ItemResponse, status_code=201)
async def create_item(item: Item):
    global next_id
    items_db[next_id] = item
    item_id = next_id
    next_id += 1
    return {"id": item_id, **item.model_dump()}

@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **items_db[item_id].model_dump()}

@router.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return {"id": item_id, **item.model_dump()}

@router.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
```

---

## Mounting Routers

### Basic Inclusion

```python
# app/main.py
from fastapi import FastAPI
from app.routers import users, items, auth

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(auth.router)
```

### With Prefix

```python
app.include_router(users.router, prefix="/api/v1")
app.include_router(items.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
```

### With Tags

```python
app.include_router(users.router, tags=["users"])
app.include_router(items.router, tags=["items"])
app.include_router(auth.router, tags=["auth"])
```

### With Dependencies

```python
app.include_router(
    users.router,
    prefix="/api/v1",
    tags=["users"],
    dependencies=[Depends(get_db)],
)
```

### With Responses

```python
app.include_router(
    users.router,
    prefix="/api/v1",
    tags=["users"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)
```

---

## Router Prefixes

### Defining Prefix on the Router

```python
# app/routers/users.py
from fastapi import APIRouter

# Prefix defined on the router itself
router = APIRouter(prefix="/users")

@router.get("/")      # → /users/
async def list_users():
    return []

@router.get("/{id}")  # → /users/{id}
async def get_user(id: int):
    return {"id": id}
```

### Defining Prefix When Including

```python
# app/main.py
app.include_router(users.router, prefix="/api/v1")
# All routes from users.router now have /api/v1 prefix
# /users/ → /api/v1/users/
# /users/{id} → /api/v1/users/{id}
```

### Combining Both

```python
# app/routers/users.py
router = APIRouter(prefix="/users")

# app/main.py
app.include_router(router, prefix="/api/v1")
# Route: /users/ → /api/v1/users/
```

### Versioned API Structure

```python
# app/main.py
app.include_router(users.router, prefix="/api/v1")
app.include_router(items.router, prefix="/api/v1")

# V2 routers
app.include_router(users_v2.router, prefix="/api/v2")
app.include_router(items_v2.router, prefix="/api/v2")
```

---

## Router Tags

Tags organize endpoints in the automatic documentation:

```python
# app/routers/users.py
router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/", summary="List all users")
async def list_users():
    """Retrieve a list of all users."""
    return []

@router.post("/", summary="Create a new user")
async def create_user(user: UserCreate):
    """Create a new user with the provided information."""
    return user
```

### Multiple Tags

```python
router = APIRouter(tags=["users", "authentication"])

# Or per-endpoint
@router.get("/", tags=["users", "public"])
async def list_users():
    return []
```

### Tag Descriptions

```python
# In main.py
app = FastAPI()

app.include_router(
    users.router,
    tags=[
        {
            "name": "users",
            "description": "Operations with users (CRUD, profiles, etc.)",
        },
        {
            "name": "authentication",
            "description": "Login, logout, token management",
        },
    ],
)
```

### Tag Metadata in OpenAPI

```python
app = FastAPI(
    openapi_tags=[
        {
            "name": "users",
            "description": "User management operations",
            "externalDocs": {
                "description": "User Guide",
                "url": "https://docs.example.com/users",
            },
        },
    ],
)
```

---

## Router Dependencies

### Router-Level Dependencies

```python
from fastapi import APIRouter, Depends

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "valid-key":
        raise HTTPException(status_code=403, detail="Invalid API key")

async def get_db():
    db = Database()
    try:
        yield db
    finally:
        await db.close()

# All routes in this router require these dependencies
router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(verify_api_key)],
)

@router.get("/stats/")
async def get_stats(db: Database = Depends(get_db)):
    return {"total_users": await db.count_users()}

@router.get("/logs/")
async def get_logs(db: Database = Depends(get_db)):
    return {"logs": await db.get_logs()}
```

### Multiple Dependencies

```python
router = APIRouter(
    dependencies=[
        Depends(verify_api_key),
        Depends(get_db),
        Depends(rate_limit),
    ],
)

# All routes in this router run all three dependencies
```

### Combining Router and Endpoint Dependencies

```python
# Router-level: runs for ALL routes
router = APIRouter(
    prefix="/api/v1",
    dependencies=[Depends(verify_api_key)],
)

# Endpoint-level: runs for THIS route only
@router.get("/users/")
async def list_users(
    db: Database = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await db.get_users(current_user.id)
```

---

## Router-level Responses

### Default Responses for All Routes

```python
router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)

@router.get("/")
async def list_items():
    return []

@router.get("/{item_id}")
async def get_item(item_id: int):
    return {"id": item_id}
```

### Per-Route Response Overrides

```python
router = APIRouter(
    responses={
        404: {"description": "Not found"},
    },
)

@router.get("/", responses={200: {"description": "List of items"}})
async def list_items():
    return []

@router.post("/", responses={201: {"description": "Item created"}})
async def create_item(item: Item):
    return item

# The 404 response from router applies to both routes
# The 200/201 responses are route-specific
```

### Response Model in Responses

```python
from fastapi.responses import JSONResponse

router = APIRouter(
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Resource not found",
        },
        422: {
            "model": ValidationErrorResponse,
            "description": "Validation error",
        },
    },
)
```

---

## Organizing Routes by Feature

### Feature-Based Structure

```
app/
├── main.py
├── routers/
│   ├── __init__.py
│   ├── users.py
│   ├── items.py
│   ├── auth.py
│   ├── orders.py
│   └── health.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── item.py
├── schemas/
│   ├── __init__.py
│   ├── user.py
│   └── item.py
├── services/
│   ├── __init__.py
│   ├── user_service.py
│   └── item_service.py
└── dependencies.py
```

### Example Router Files

```python
# app/routers/users.py
from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 10,
    service: UserService = Depends(),
):
    return await service.list_users(skip=skip, limit=limit)

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user: UserCreate,
    service: UserService = Depends(),
):
    return await service.create_user(user)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    service: UserService = Depends(),
):
    return await service.get_user(user_id)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user: UserUpdate,
    service: UserService = Depends(),
):
    return await service.update_user(user_id, user)

@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    service: UserService = Depends(),
):
    await service.delete_user(user_id)
```

```python
# app/main.py
from fastapi import FastAPI
from app.routers import users, items, auth, health

app = FastAPI(title="My API", version="1.0.0")

# Include all routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(items.router, prefix="/api/v1")
app.include_router(health.router)
```

---

## Nested Routers

### Router with Sub-Routers

```python
# app/routers/admin/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["admin-users"])

@router.get("/")
async def admin_list_users():
    return []

@router.get("/{user_id}")
async def admin_get_user(user_id: int):
    return {"id": user_id}
```

```python
# app/routers/admin/__init__.py
from fastapi import APIRouter
from . import users, audit

router = APIRouter(prefix="/admin", tags=["admin"])
router.include_router(users.router)
router.include_router(audit.router)
```

```python
# app/main.py
from fastapi import FastAPI
from app.routers import users, items
from app.routers.admin import router as admin_router

app = FastAPI()

app.include_router(users.router, prefix="/api/v1")
app.include_router(items.router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")

# Routes:
# /api/v1/users/        (from users.router)
# /api/v1/items/        (from items.router)
# /api/v1/admin/users/  (from admin_router → admin/users.router)
# /api/v1/admin/audit/  (from admin_router → admin/audit.router)
```

---

## Including Routers Dynamically

### Conditional Router Inclusion

```python
from fastapi import FastAPI

app = FastAPI()

# Always include these
from app.routers import users, items
app.include_router(users.router, prefix="/api/v1")
app.include_router(items.router, prefix="/api/v1")

# Conditionally include based on settings
from app.config import settings

if settings.ENABLE_ADMIN_ROUTES:
    from app.routers import admin
    app.include_router(admin.router, prefix="/api/v1")

if settings.ENABLE_MONITORING:
    from app.routers import monitoring
    app.include_router(monitoring.router, prefix="/api/v1")

# Include test routes only in development
if settings.ENVIRONMENT == "development":
    from app.routers import test_routes
    app.include_router(test_routes.router, prefix="/api/test")
```

### Plugin System

```python
def register_plugin(app: FastAPI, plugin_name: str):
    try:
        module = importlib.import_module(f"app.plugins.{plugin_name}")
        if hasattr(module, "router"):
            app.include_router(
                module.router,
                prefix=f"/api/plugins/{plugin_name}",
                tags=[plugin_name],
            )
            logger.info(f"Loaded plugin: {plugin_name}")
    except ImportError:
        logger.warning(f"Plugin {plugin_name} not found")

# In main.py
PLUGINS = ["analytics", "notifications", "audit"]

for plugin in PLUGINS:
    register_plugin(app, plugin)
```

---

## Router Best Practices for Large Apps

### 1. One Router Per Feature

```
app/routers/
├── users.py      # User CRUD + profiles
├── items.py      # Item CRUD + search
├── auth.py       # Login, logout, tokens
├── orders.py     # Order management
└── health.py     # Health checks
```

### 2. Use Prefixes Consistently

```python
# Option A: Prefix on router
router = APIRouter(prefix="/users", tags=["users"])

# Option B: Prefix when including
app.include_router(users.router, prefix="/api/v1/users")

# Choose ONE approach and stick with it
```

### 3. Separate Schemas from Routers

```python
# ❌ Bad: Schemas in router file
from fastapi import APIRouter
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str

router = APIRouter()

@router.post("/users/")
async def create_user(user: UserCreate):
    return user

# ✅ Good: Separate schemas
# app/schemas/user.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str

# app/routers/users.py
from fastapi import APIRouter
from app.schemas.user import UserCreate

router = APIRouter()

@router.post("/users/")
async def create_user(user: UserCreate):
    return user
```

### 4. Use Dependencies for Cross-Cutting Concerns

```python
# app/dependencies.py
async def get_db():
    ...

async def get_current_user(token: str = Header(...)):
    ...

# app/routers/users.py
from app.dependencies import get_db, get_current_user

router = APIRouter(dependencies=[Depends(get_db)])

@router.get("/")
async def list_users(current_user: User = Depends(get_current_user)):
    ...
```

### 5. Document Everything

```python
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    "/",
    summary="List all users",
    description="Retrieve a paginated list of all users.",
    response_model=list[UserResponse],
)
async def list_users(skip: int = 0, limit: int = 10):
    """List users with pagination support.
    
    - **skip**: Number of users to skip (default: 0)
    - **limit**: Maximum users to return (default: 10, max: 100)
    """
    ...
```

### 6. Keep Routers Thin

```python
# ❌ Bad: Business logic in router
@router.post("/users/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Validation logic
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(409, "Email taken")
    
    # Password hashing
    hashed = bcrypt.hash(user.password)
    
    # Database operations
    db_user = User(username=user.username, email=user.email, password=hashed)
    db.add(db_user)
    db.commit()
    
    return db_user

# ✅ Good: Thin router, logic in service
@router.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, service: UserService = Depends()):
    return await service.create_user(user)
```

---

## Interview Questions

### Q1: What is APIRouter and why would you use it?

**Answer:** `APIRouter` is a FastAPI class that lets you split your application into separate route files. It has the same interface as `FastAPI` (supports `@get`, `@post`, etc.) and can be included in the main app with `app.include_router()`. Use it to organize routes by feature, apply shared dependencies, and keep code maintainable.

### Q2: What's the difference between defining a prefix on APIRouter vs when including?

**Answer:** Both achieve the same result. `APIRouter(prefix="/users")` sets the prefix on the router itself. `app.include_router(router, prefix="/api/v1")` adds a prefix when including. You can combine both. Choose one approach and be consistent across your project.

### Q3: How do you share dependencies across multiple routes?

**Answer:** Set dependencies on the router level:

```python
router = APIRouter(dependencies=[Depends(get_db)])
```

All routes in this router will use that dependency. You can also combine router-level and endpoint-level dependencies.

### Q4: Can you include the same router in multiple apps?

**Answer:** Yes, but each inclusion creates separate route registrations. Be careful with prefix conflicts. More commonly, you include multiple routers in one app. For sharing across apps, create the router in a shared module.

### Q5: How do you organize routes in a large FastAPI application?

**Answer:** Use a feature-based structure: one router file per domain feature (users, items, auth). Put schemas in a separate `schemas/` directory, business logic in `services/`, and database operations in `repositories/`. Use a main.py that includes all routers with consistent prefixes.

### Q6: What happens if two routers define the same route?

**Answer:** FastAPI matches routes by their full path (including prefix) and HTTP method. If two routes have the exact same path and method, the first one registered wins. This is why route ordering matters and you should avoid duplicate routes.

### Q7: How do you apply middleware to only some routes?

**Answer:** Use router-level dependencies or include middleware only on specific routers. Alternatively, use the `app.include_router()` with `dependencies` parameter. For true middleware behavior, you can check the request path in a global middleware and skip processing for certain paths.

### Q8: Can you dynamically include/exclude routers based on configuration?

**Answer:** Yes. Use conditional imports and `include_router()`:

```python
if settings.ENABLE_FEATURE_X:
    from app.routers import feature_x
    app.include_router(feature_x.router)
```

This is useful for feature flags, environment-specific routes, and plugin systems.
