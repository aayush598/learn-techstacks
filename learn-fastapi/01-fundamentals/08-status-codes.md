# 08 - Status Codes

## Table of Contents

1. [HTTPStatus Enum](#httpstatus-enum)
2. [Status Code Modules](#status-code-modules)
3. [Custom Status Codes](#custom-status-codes)
4. [Status Code with response_model](#status-code-with-response_model)
5. [Status Code Reference](#status-code-reference)
6. [When to Use Each Status Code](#when-to-use-each-status-code)
7. [Status Code Best Practices for REST APIs](#status-code-best-practices-for-rest-apis)
8. [Interview Questions](#interview-questions)

---

## HTTPStatus Enum

FastAPI includes the `HTTPStatus` enum from Python's `http` module, which provides human-readable names for HTTP status codes:

```python
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

# Using status constants (recommended - most readable)
@app.get("/items/")
async def list_items():
    return {"items": []}

@app.post("/items/")
async def create_item(item: Item):
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"id": 1, **item.model_dump()},
    )

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
```

### All HTTPStatus Values

```python
from http import HTTPStatus

# 2xx Success
HTTPStatus.OK                    # 200
HTTPStatus.CREATED               # 201
HTTPStatus.ACCEPTED              # 202
HTTPStatus.NON_AUTHORITATIVE_INFORMATION  # 203
HTTPStatus.NO_CONTENT            # 204
HTTPStatus.RESET_CONTENT         # 205
HTTPStatus.PARTIAL_CONTENT       # 206

# 3xx Redirection
HTTPStatus.MULTIPLE_CHOICES      # 300
HTTPStatus.MOVED_PERMANENTLY     # 301
HTTPStatus.FOUND                 # 302
HTTPStatus.SEE_OTHER             # 303
HTTPStatus.NOT_MODIFIED          # 304
HTTPStatus.TEMPORARY_REDIRECT    # 307
HTTPStatus.PERMANENT_REDIRECT    # 308

# 4xx Client Error
HTTPStatus.BAD_REQUEST           # 400
HTTPStatus.UNAUTHORIZED          # 401
HTTPStatus.PAYMENT_REQUIRED      # 402
HTTPStatus.FORBIDDEN             # 403
HTTPStatus.NOT_FOUND             # 404
HTTPStatus.METHOD_NOT_ALLOWED    # 405
HTTPStatus.NOT_ACCEPTABLE        # 406
HTTPStatus.CONFLICT              # 409
HTTPStatus.GONE                  # 410
HTTPStatus.UNPROCESSABLE_ENTITY  # 422
HTTPStatus.TOO_MANY_REQUESTS     # 429

# 5xx Server Error
HTTPStatus.INTERNAL_SERVER_ERROR # 500
HTTPStatus.NOT_IMPLEMENTED       # 501
HTTPStatus.BAD_GATEWAY           # 502
HTTPStatus.SERVICE_UNAVAILABLE   # 503
HTTPStatus.GATEWAY_TIMEOUT       # 504
```

---

## Status Code Modules

### Using `status` from FastAPI

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    return user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    return None
```

### Using `status` from `http` Module

```python
from http import HTTPStatus

@app.post("/items/")
async def create_item(item: Item):
    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content=item.model_dump(),
    )
```

### Integer Status Codes (Less Recommended)

```python
@app.post("/items/", status_code=201)
async def create_item(item: Item):
    return item

@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    return None
```

---

## Custom Status Codes

### Using Non-Standard Status Codes

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/custom/")
async def custom_status():
    return JSONResponse(
        status_code=418,  # I'm a Teapot
        content={"message": "I'm a teapot"},
    )

# Define custom status codes
@app.get("/custom2/")
async def custom_status2():
    return JSONResponse(
        status_code=429,  # Too Many Requests
        content={"detail": "Rate limit exceeded"},
        headers={"Retry-After": "60"},
    )
```

### Custom Status Code in Exception

```python
from fastapi import HTTPException

@app.get("/strict/")
async def strict_endpoint():
    raise HTTPException(
        status_code=418,
        detail="I'm a teapot, not a coffee maker",
        headers={"X-Teapot": "true"},
    )
```

---

## Status Code with response_model

### Combining Status Code and Response Model

```python
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: str

@app.post(
    "/users/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a user with username, email, and password.",
    response_description="The created user object",
    responses={
        409: {"description": "Username already exists"},
        422: {"description": "Validation error"},
    },
)
async def create_user(user: UserCreate):
    """Create a new user account.
    
    - **username**: unique username (3-50 chars)
    - **email**: valid email address
    - **password**: minimum 8 characters
    """
    # Check for duplicates
    existing_user = get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )
    
    # Create user
    new_user = create_user_in_db(user)
    return new_user
```

### Multiple Response Status Codes

```python
@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={
        200: {"description": "Item found"},
        404: {"description": "Item not found"},
        500: {"description": "Server error"},
    },
)
async def get_item(item_id: int):
    item = get_item_from_db(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

---

## Status Code Reference

### 2xx Success Codes

| Code | Name | When to Use |
|------|------|-------------|
| **200** | OK | GET success, PUT success, general success |
| **201** | Created | POST success (resource created) |
| **202** | Accepted | Async operation accepted (not yet complete) |
| **204** | No Content | DELETE success (no body returned) |

### 3xx Redirection Codes

| Code | Name | When to Use |
|------|------|-------------|
| **301** | Moved Permanently | Resource permanently moved |
| **302** | Found | Temporary redirect |
| **304** | Not Modified | Cached response is still valid |

### 4xx Client Error Codes

| Code | Name | When to Use |
|------|------|-------------|
| **400** | Bad Request | Invalid request format |
| **401** | Unauthorized | Authentication required |
| **403** | Forbidden | Authenticated but not authorized |
| **404** | Not Found | Resource doesn't exist |
| **405** | Method Not Allowed | HTTP method not supported |
| **409** | Conflict | Resource conflict (duplicate, etc.) |
| **422** | Unprocessable Entity | Validation error (FastAPI default) |
| **429** | Too Many Requests | Rate limit exceeded |

### 5xx Server Error Codes

| Code | Name | When to Use |
|------|------|-------------|
| **500** | Internal Server Error | Unexpected server error |
| **502** | Bad Gateway | Upstream service error |
| **503** | Service Unavailable | Server temporarily unavailable |
| **504** | Gateway Timeout | Upstream service timeout |

---

## When to Use Each Status Code

### 200 OK

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = get_user(user_id)
    return user  # 200 OK (default)

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    updated = update_user_in_db(user_id, user)
    return updated  # 200 OK
```

### 201 Created

```python
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    new_user = create_user_in_db(user)
    return new_user
```

### 204 No Content

```python
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    delete_user_from_db(user_id)
    return None  # No response body
```

### 400 Bad Request

```python
@app.post("/orders/")
async def create_order(order: OrderCreate):
    if order.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be positive"
        )
    return create_order_in_db(order)
```

### 401 Unauthorized

```python
@app.get("/profile/")
async def get_profile(authorization: str = Header(...)):
    if not is_valid_token(authorization):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return get_user_profile(authorization)
```

### 403 Forbidden

```python
@app.delete("/users/{user_id}")
async def delete_user(user_id: int, current_user = Depends(get_current_user)):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    delete_user_from_db(user_id)
```

### 404 Not Found

```python
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    item = get_item_from_db(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return item
```

### 409 Conflict

```python
@app.post("/users/")
async def create_user(user: UserCreate):
    existing = get_user_by_email(user.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    return create_user_in_db(user)
```

### 422 Unprocessable Entity

```python
# FastAPI automatically returns 422 for validation errors
@app.post("/items/")
async def create_item(item: Item):
    # If item doesn't match the Item schema
    # FastAPI returns 422 with detailed error info
    return item
```

---

## Status Code Best Practices for REST APIs

### DO: Use Appropriate Status Codes

```python
# ✅ Good
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    return create_user(user)

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    delete_user(user_id)

# ❌ Bad
@app.post("/users/")
async def create_user(user: UserCreate):
    return {"status": "created", "user": create_user(user)}
    # Should be 201, not 200

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    return {"status": "deleted"}
    # Should be 204, not 200
```

### DON'T: Use 200 for Everything

```python
# ❌ Bad - 200 for errors
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    item = get_item(item_id)
    if not item:
        return {"error": "Not found"}  # Wrong! Should be 404
    return item

# ✅ Good - proper status codes
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    item = get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

### DO: Include Error Details

```python
@app.post("/users/")
async def create_user(user: UserCreate):
    errors = validate_user(user)
    if errors:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=errors,
        )
    return create_user_in_db(user)
```

### DON'T: Leak Internal Details

```python
# ❌ Bad - exposes internal error
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    try:
        return get_item_from_db(item_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)  # Exposes internal error message
        )

# ✅ Good - generic error message
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    try:
        return get_item_from_db(item_id)
    except Exception:
        logger.exception("Database error")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
```

### DO: Be Consistent

```
GET /users/        → 200 + list of users
GET /users/{id}    → 200 + user object OR 404
POST /users/       → 201 + created user
PUT /users/{id}    → 200 + updated user
DELETE /users/{id} → 204 (no body)

GET /items/        → 200 + list of items
POST /items/       → 201 + created item
```

---

## Interview Questions

### Q1: What status code should you return when creating a resource?

**Answer:** `201 Created`. This is the standard HTTP status code for successful resource creation. Always set it explicitly for POST endpoints that create resources:

```python
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    return create_user(user)
```

### Q2: When should you use 204 No Content?

**Answer:** Use 204 for successful operations that don't return a body, typically DELETE operations. The client knows the operation succeeded but there's no data to return:

```python
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    delete_user_from_db(user_id)
    return None
```

### Q3: Why does FastAPI use 422 for validation errors instead of 400?

**Answer:** FastAPI follows the OpenAPI specification which uses 422 (Unprocessable Entity) for validation errors. 400 (Bad Request) is for malformed requests that can't be parsed. 422 means the request was parsed but the data failed validation. However, you can customize this behavior.

### Q4: What's the difference between 401 and 403?

**Answer:** 401 (Unauthorized) means the user is not authenticated - they need to provide valid credentials. 403 (Forbidden) means the user is authenticated but doesn't have permission for the requested resource. 401 should include a `WWW-Authenticate` header.

### Q5: When should you use 409 Conflict?

**Answer:** Use 409 when a request conflicts with the current state of the resource. Common cases: duplicate email/username during registration, concurrent edit conflicts, attempting to create a resource that already exists.

### Q6: Should you always return 200 for GET requests?

**Answer:** Generally yes, but with exceptions. 200 for successful retrieval, 404 if the resource doesn't exist, 403 if the user lacks access, and 304 for cached responses. For list endpoints that return empty results, 200 with an empty array is correct (not 404).

### Q7: How do you handle rate limiting status codes?

**Answer:** Use 429 (Too Many Requests) with a `Retry-After` header:

```python
raise HTTPException(
    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    detail="Rate limit exceeded",
    headers={"Retry-After": "60"},
)
```
