# API Versioning for FastAPI

## Table of Contents
1. [Why Version APIs](#why-version)
2. [URL Versioning](#url-versioning)
3. [Header Versioning](#header-versioning)
4. [Query Param Versioning](#query-versioning)
5. [Media Type Versioning](#media-type-versioning)
6. [Versioning Strategies](#strategies)
7. [Deprecation Policy](#deprecation)
8. [Multiple Versions Simultaneously](#multiple-versions)

---

## Why Version APIs <a name="why-version"></a>

API versioning allows you to evolve your API without breaking existing clients. When you make changes—renaming fields, changing response structure, altering behavior—versioning ensures backward compatibility.

**When to version:**
- Removing or renaming response fields
- Changing URL structure
- Modifying authentication requirements
- Changing business logic behavior
- Adding breaking changes to error responses

**When NOT to version:**
- Adding new optional fields to responses
- Adding new endpoints
- Adding optional query parameters
- Fixing bugs (not breaking changes)

---

## URL Versioning <a name="url-versioning"></a>

The most common and visible approach. The version is part of the URL path.

### Basic Implementation

```python
from fastapi import FastAPI, APIRouter

app = FastAPI(title="My API")

# V1 Router
v1_router = APIRouter(prefix="/api/v1")

@v1_router.get("/users")
async def get_users_v1():
    return {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"}
        ]
    }

@v1_router.get("/users/{user_id}")
async def get_user_v1(user_id: int):
    return {"id": user_id, "name": "Alice", "email": "alice@example.com"}

# V2 Router
v2_router = APIRouter(prefix="/api/v2")

@v2_router.get("/users")
async def get_users_v2():
    return {
        "data": [
            {"id": 1, "attributes": {"name": "Alice", "email": "alice@example.com"}}
        ],
        "meta": {"total": 1}
    }

@v2_router.get("/users/{user_id}")
async def get_user_v2(user_id: int):
    return {
        "data": {"id": user_id, "attributes": {"name": "Alice", "email": "alice@example.com"}}
    }

app.include_router(v1_router)
app.include_router(v2_router)
```

### File Structure

```
app/
├── main.py
├── v1/
│   ├── __init__.py
│   ├── router.py
│   ├── models.py
│   └── schemas.py
└── v2/
    ├── __init__.py
    ├── router.py
    ├── models.py
    └── schemas.py
```

### Version-Dependent Schemas

```python
# app/v1/schemas.py
from pydantic import BaseModel

class UserResponseV1(BaseModel):
    id: int
    name: str
    email: str

class UserListResponseV1(BaseModel):
    users: list[UserResponseV1]
```

```python
# app/v2/schemas.py
from pydantic import BaseModel

class UserAttributes(BaseModel):
    name: str
    email: str

class UserResponseV2(BaseModel):
    id: int
    attributes: UserAttributes
    links: dict[str, str]

class UserListResponseV2(BaseModel):
    data: list[UserResponseV2]
    meta: dict[str, int]
```

### Router with Dependency Injection

```python
# app/v1/router.py
from fastapi import APIRouter, Depends
from app.deps import get_db_v1

router = APIRouter(prefix="/api/v1", tags=["v1"])

@router.get("/users")
async def list_users(db=Depends(get_db_v1)):
    users = await db.fetch_all("SELECT * FROM users")
    return {"users": users}
```

---

## Header Versioning <a name="header-versioning"></a>

The version is specified in an HTTP header. Keeps URLs clean.

```python
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

SUPPORTED_VERSIONS = {"1.0", "2.0"}
DEFAULT_VERSION = "2.0"

@app.get("/api/users")
async def get_users(request: Request):
    version = request.headers.get("API-Version", DEFAULT_VERSION)

    if version not in SUPPORTED_VERSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported API version. Supported: {SUPPORTED_VERSIONS}"
        )

    if version == "1.0":
        return {"users": [{"id": 1, "name": "Alice"}]}
    else:
        return {"data": [{"id": 1, "attributes": {"name": "Alice"}}]}
```

### Using Dependency Injection

```python
from fastapi import Header, HTTPException
from typing import Annotated

async def get_api_version(
    api_version: Annotated[str | None, Header()] = None
) -> str:
    version = api_version or "2.0"
    if version not in SUPPORTED_VERSIONS:
        raise HTTPException(status_code=400, detail="Unsupported version")
    return version

@app.get("/api/users")
async def get_users(version: Annotated[str, Depends(get_api_version)]):
    if version == "1.0":
        return {"users": [{"id": 1, "name": "Alice"}]}
    return {"data": [{"id": 1, "attributes": {"name": "Alice"}}]}
```

---

## Query Param Versioning <a name="query-versioning"></a>

Version specified as a query parameter. Simple but less clean.

```python
from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()

@app.get("/api/users")
async def get_users(
    version: Annotated[str, Query(alias="api-version")] = "2.0"
):
    if version == "1.0":
        return {"users": [{"id": 1, "name": "Alice"}]}
    return {"data": [{"id": 1, "attributes": {"name": "Alice"}}]}

# Usage: GET /api/users?api-version=1.0
```

---

## Media Type Versioning <a name="media-type-versioning"></a>

Version specified in the Accept header using content negotiation.

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/api/users")
async def get_users(request: Request):
    accept = request.headers.get("accept", "application/json")
    version = "2.0"

    # Parse version from Accept header
    # Example: application/vnd.myapi.v1+json
    if "vnd.myapi.v1" in accept:
        version = "1.0"
    elif "vnd.myapi.v2" in accept:
        version = "2.0"

    if version == "1.0":
        return JSONResponse(
            content={"users": [{"id": 1, "name": "Alice"}]},
            headers={"X-API-Version": "1.0"}
        )
    return JSONResponse(
        content={"data": [{"id": 1, "attributes": {"name": "Alice"}}]},
        headers={"X-API-Version": "2.0"}
    )

# Usage: Accept: application/vnd.myapi.v1+json
```

---

## Versioning Strategies <a name="strategies"></a>

### Strategy Comparison

| Strategy | Pros | Cons |
|----------|------|------|
| URL Versioning | Visible, cacheable, easy to test | URLs change, breaks REST purism |
| Header Versioning | Clean URLs, flexible | Harder to test, less visible |
| Query Param | Easy to implement | Clutters URLs, less standard |
| Media Type | RESTful, precise | Complex, hard to test |

### Hybrid Approach (Recommended)

```python
# Support URL versioning (primary) and header versioning (alternative)
from fastapi import FastAPI, APIRouter, Header, Request
from typing import Annotated

app = FastAPI()

def create_versioned_app():
    v1 = APIRouter(prefix="/api/v1", tags=["v1"])
    v2 = APIRouter(prefix="/api/v2", tags=["v2"])

    @v1.get("/users")
    async def list_users_v1():
        return {"users": [{"id": 1, "name": "Alice"}]}

    @v2.get("/users")
    async def list_users_v2():
        return {"data": [{"id": 1, "attributes": {"name": "Alice"}}]}

    # Default route uses latest version
    @app.get("/api/users")
    async def list_users_default(
        api_version: Annotated[str | None, Header()] = None
    ):
        if api_version and api_version.startswith("1"):
            return {"users": [{"id": 1, "name": "Alice"}]}
        return {"data": [{"id": 1, "attributes": {"name": "Alice"}}]}

    app.include_router(v1)
    app.include_router(v2)

create_versioned_app()
```

---

## Deprecation Policy <a name="deprecation"></a>

```python
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta

app = FastAPI()

v1_router = APIRouter(
    prefix="/api/v1",
    tags=["v1 (deprecated)"],
    responses={
        200: {
            "headers": {
                "Deprecation": {
                    "description": "Date when this version was deprecated",
                    "schema": {"type": "string"}
                },
                "Sunset": {
                    "description": "Date when this version will be removed",
                    "schema": {"type": "string"}
                },
                "Link": {
                    "description": "Link to new version docs",
                    "schema": {"type": "string"}
                },
            }
        }
    }
)

@v1_router.get("/users")
async def list_users_v1():
    deprecation_date = "2025-01-01"
    sunset_date = "2025-06-01"
    return JSONResponse(
        content={"users": [{"id": 1, "name": "Alice"}]},
        headers={
            "Deprecation": deprecation_date,
            "Sunset": sunset_date,
            "Link": '</api/v2/users>; rel="successor-version"',
        }
    )
```

### Deprecation Timeline

```
Phase 1: Announce deprecation
  - Add Deprecation header to responses
  - Add Sunset header with removal date
  - Document migration guide
  - Notify API consumers

Phase 2: Warning period (3-6 months)
  - Keep v1 fully functional
  - Log v1 usage to identify remaining consumers
  - Send migration reminders

Phase 3: Removal
  - Remove v1 routes
  - Return 410 Gone for v1 endpoints
  - Update documentation
```

---

## Multiple Versions Simultaneously <a name="multiple-versions"></a>

### Shared Business Logic

```python
# app/core/user_service.py
class UserService:
    async def get_user(self, user_id: int) -> dict:
        user = await self.db.get_user(user_id)
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at.isoformat(),
        }

# app/v1/router.py
@router.get("/users/{user_id}")
async def get_user_v1(user_id: int, service: UserService = Depends()):
    user = await service.get_user(user_id)
    return user  # V1 returns flat structure

# app/v2/router.py
@router.get("/users/{user_id}")
async def get_user_v2(user_id: int, service: UserService = Depends()):
    user = await service.get_user(user_id)
    return {
        "data": {
            "id": user["id"],
            "attributes": {k: v for k, v in user.items() if k != "id"},
            "links": {"/self": f"/api/v2/users/{user['id']}"},
        }
    }
```

### Version Router Factory

```python
from fastapi import APIRouter
from typing import Callable

def create_user_router(version: str) -> APIRouter:
    router = APIRouter(prefix=f"/api/{version}", tags=[f"users-{version}")

    @router.get("/users")
    async def list_users():
        users = await get_all_users()
        return format_response(users, version)

    return router

def format_response(data, version):
    if version == "v1":
        return {"users": data}
    return {"data": data, "meta": {"count": len(data)}}

# Register versions
app.include_router(create_user_router("v1"))
app.include_router(create_user_router("v2"))
```

---

## Interview Questions

1. **What are the pros and cons of URL versioning vs header versioning?**
URL versioning is visible, cacheable, and easy to test with browser/curl. But it clutters URLs and technically violates REST principles. Header versioning keeps URLs clean and is more RESTful but harder to test and less visible. URL versioning is more popular in practice.

2. **When should you create a new API version vs adding to the existing one?**
Create a new version for breaking changes: removing fields, changing data types, modifying authentication, or altering URL structure. Add to existing version for non-breaking changes: new endpoints, new optional fields, new optional query parameters.

3. **How do you handle deprecation of an old API version?**
Set Deprecation and Sunset headers, document migration guide, notify consumers, monitor usage to identify remaining consumers, set a removal timeline (3-6 months), and return 410 Gone after removal.

4. **How would you implement versioning in a large FastAPI application?**
Use separate routers per version (`v1/`, `v2/`), share business logic in core services, use Pydantic models per version, configure each router independently, and use a version registry pattern for managing multiple versions.

5. **What is content negotiation and how does it relate to API versioning?**
Content negotiation uses the Accept header to specify media types. In versioning, you can use vendor-specific media types like `application/vnd.myapi.v2+json`. The server inspects the Accept header and returns the appropriate version. This is the most RESTful approach but harder to test.
