# 09 - Error Handling

## Table of Contents

1. [HTTPException](#httpexception)
2. [Custom Exception Handlers](#custom-exception-handlers)
3. [RequestValidationError vs ValidationError](#requestvalidationerror-vs-validationerror)
4. [Custom Exceptions Hierarchy](#custom-exceptions-hierarchy)
5. [Exception Handler for Validation Errors](#exception-handler-for-validation-errors)
6. [Custom Error Response Format](#custom-error-response-format)
7. [Logging Exceptions](#logging-exceptions)
8. [Production Error Handling Patterns](#production-error-handling-patterns)
9. [Interview Questions](#interview-questions)

---

## HTTPException

The most common way to signal errors in FastAPI is raising `HTTPException`:

### Basic Usage

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": {"name": "Foo", "price": 50.0}}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail=f"Item {item_id} not found",
        )
    return items[item_id]
```

### HTTPException with Headers

```python
@app.get("/secret/")
async def secret_endpoint(token: str = Header(...)):
    if token != "secret-token":
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Access granted"}
```

### Common HTTPException Patterns

```python
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    # Check for duplicate
    existing = get_user_by_email(user.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    return create_user(user)

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = get_user_from_db(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    return user

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate, current_user = Depends(get_current_user)):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return update_user_in_db(user_id, user)

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    user = get_user_from_db(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    delete_user_from_db(user_id)
```

---

## Custom Exception Handlers

### Using @app.exception_handler

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

class UnicornNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornNotFoundException)
async def unicorn_not_found_handler(request: Request, exc: UnicornNotFoundException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} does not exist. Here, take this coffee."},
    )

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "jeff":
        raise UnicornNotFoundException(name=name)
    return {"unicorn": name}
```

### Multiple Exception Handlers

```python
class DatabaseError(Exception):
    def __init__(self, message: str, query: str = ""):
        self.message = message
        self.query = query

class ExternalServiceError(Exception):
    def __init__(self, service: str, status_code: int, detail: str):
        self.service = service
        self.status_code = status_code
        self.detail = detail

class RateLimitExceeded(Exception):
    def __init__(self, retry_after: int):
        self.retry_after = retry_after

@app.exception_handler(DatabaseError)
async def db_error_handler(request: Request, exc: DatabaseError):
    logger.error(f"Database error: {exc.message}, Query: {exc.query}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": "database_error"},
    )

@app.exception_handler(ExternalServiceError)
async def external_service_handler(request: Request, exc: ExternalServiceError):
    logger.error(f"External service error: {exc.service} - {exc.detail}")
    return JSONResponse(
        status_code=502,
        content={"detail": f"Service {exc.service} is unavailable"},
    )

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
        headers={"Retry-After": str(exc.retry_after)},
    )
```

### Overriding Default FastAPI Handlers

```python
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Override the default 422 validation error handler
@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": errors},
    )

# Override the default HTTP exception handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
```

---

## RequestValidationError vs ValidationError

### RequestValidationError

Raised when the request data (path params, query params, body) fails validation. This is a **client error** - the client sent invalid data.

```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def request_validation_handler(request: Request, exc: RequestValidationError):
    # exc.errors() returns a list of validation error details
    errors = exc.errors()
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation failed", "errors": errors},
    )
```

### ValidationError (Pydantic)

Raised when Pydantic validation fails in your own code (not from request data):

```python
from pydantic import ValidationError

@app.post("/items/")
async def create_item(item: Item):
    try:
        # Manual validation
        validated = SomeModel.model_validate(item.model_dump())
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return validated
```

### Differences

| Feature | RequestValidationError | ValidationError |
|---------|----------------------|-----------------|
| Source | FastAPI request parsing | Pydantic manual validation |
| When raised | Invalid request data | Invalid data in your code |
| HTTP status | 422 (automatic) | You handle manually |
| Error format | FastAPI's standard format | Pydantic's error format |
| Client error | Yes | Depends on context |

---

## Custom Exceptions Hierarchy

### Building an Exception Hierarchy

```python
from fastapi import HTTPException, status

class AppException(HTTPException):
    """Base application exception."""
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = "UNKNOWN_ERROR",
        headers: dict | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code

class NotFoundError(AppException):
    def __init__(self, resource: str, resource_id: int | str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} with id '{resource_id}' not found",
            error_code="NOT_FOUND",
        )

class AlreadyExistsError(AppException):
    def __init__(self, resource: str, field: str, value: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{resource} with {field} '{value}' already exists",
            error_code="ALREADY_EXISTS",
        )

class ForbiddenError(AppException):
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="FORBIDDEN",
        )

class BadRequestError(AppException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="BAD_REQUEST",
        )
```

### Using Custom Exceptions

```python
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    existing = get_user_by_email(user.email)
    if existing:
        raise AlreadyExistsError("User", "email", user.email)
    
    return create_user_in_db(user)

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = get_user_from_db(user_id)
    if not user:
        raise NotFoundError("User", user_id)
    return user

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate, current_user = Depends(get_current_user)):
    if current_user.id != user_id and not current_user.is_admin:
        raise ForbiddenError("You can only update your own profile")
    return update_user_in_db(user_id, user)
```

---

## Exception Handler for Validation Errors

### Custom Validation Error Format

```python
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def custom_validation_error_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = []
    for error in exc.errors():
        field = " -> ".join(
            str(loc) for loc in error["loc"] if loc != "body"
        )
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"],
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": errors,
            },
        },
    )
```

### Simplified Validation Messages

```python
@app.exception_handler(RequestValidationError)
async def simplified_validation_handler(
    request: Request,
    exc: RequestValidationError
):
    # Create user-friendly messages
    messages = []
    for error in exc.errors():
        loc = error["loc"]
        msg = error["msg"]
        
        # Build readable field name
        if len(loc) > 1:
            field = loc[-1]  # Just the field name
        else:
            field = loc[0]
        
        messages.append(f"{field}: {msg}")
    
    return JSONResponse(
        status_code=422,
        content={"detail": "; ".join(messages)},
    )
```

---

## Custom Error Response Format

### Standardized API Error Response

```python
from pydantic import BaseModel
from typing import Any

class ErrorResponse(BaseModel):
    success: bool = False
    error: dict[str, Any]

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: list[dict] | None = None

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=ErrorDetail(
                code=exc.error_code,
                message=exc.detail,
            ).model_dump(),
        ).model_dump(),
    )

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
        })
    
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Request validation failed",
                details=errors,
            ).model_dump(),
        ).model_dump(),
    )

# All errors now have consistent format:
# {
#     "success": false,
#     "error": {
#         "code": "NOT_FOUND",
#         "message": "User with id '42' not found"
#     }
# }
```

---

## Logging Exceptions

### Basic Exception Logging

```python
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()
logger = logging.getLogger(__name__)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(
        f"HTTP {exc.status_code}: {exc.detail} "
        f"[{request.method} {request.url.path}]"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc}")  # Includes traceback
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
```

### Structured Logging

```python
import logging
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("api")
app = FastAPI()

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    request.state.request_id = request_id
    
    # Add request_id to all log entries in this context
    extra = {"request_id": request_id, "method": request.method, "path": request.url.path}
    
    logger.info("Request started", extra=extra)
    try:
        response = await call_next(request)
        logger.info("Request completed", extra={**extra, "status_code": response.status_code})
        return response
    except Exception as e:
        logger.exception("Request failed", extra={**extra, "error": str(e)})
        raise

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logger.exception(
        "Unhandled exception",
        extra={
            "request_id": getattr(request.state, "request_id", "unknown"),
            "method": request.method,
            "path": request.url.path,
            "error": str(exc),
        },
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
```

---

## Production Error Handling Patterns

### Error Handler Registry

```python
# app/exceptions.py
from fastapi import HTTPException, status

class AppException(HTTPException):
    def __init__(self, status_code: int, detail: str, error_code: str):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code

class NotFoundError(AppException):
    def __init__(self, resource: str, id: int | str):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            f"{resource} '{id}' not found",
            "NOT_FOUND",
        )

class ConflictError(AppException):
    def __init__(self, detail: str):
        super().__init__(status.HTTP_409_CONFLICT, detail, "CONFLICT")

class UnauthorizedError(AppException):
    def __init__(self, detail: str = "Authentication required"):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, "UNAUTHORIZED")

class ForbiddenError(AppException):
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(status.HTTP_403_FORBIDDEN, detail, "FORBIDDEN")
```

### Centralized Error Handler

```python
# app/error_handlers.py
import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .exceptions import AppException

logger = logging.getLogger("api")

def register_error_handlers(app: FastAPI):
    
    @app.exception_handler(AppException)
    async def app_error_handler(request: Request, exc: AppException):
        logger.warning(f"App error: {exc.error_code} - {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.error_code,
                    "message": exc.detail,
                },
            },
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            field = " -> ".join(str(loc) for loc in error["loc"] if loc != "body")
            errors.append({"field": field, "message": error["msg"]})
        
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Validation failed",
                    "details": errors,
                },
            },
        )
    
    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception):
        logger.exception(f"Unhandled error: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred",
                },
            },
        )

# In main.py:
# from app.error_handlers import register_error_handlers
# register_error_handlers(app)
```

---

## Interview Questions

### Q1: What is the difference between HTTPException and RequestValidationError?

**Answer:** `HTTPException` is raised explicitly by your code to signal an error (like 404 Not Found). `RequestValidationError` is raised automatically by FastAPI when request data fails validation. Both result in HTTP error responses, but the trigger is different.

### Q2: How do you create custom exception handlers in FastAPI?

**Answer:** Use `@app.exception_handler(ExceptionClass)`:

```python
@app.exception_handler(MyCustomError)
async def handler(request: Request, exc: MyCustomError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
```

You can override FastAPI's built-in handlers the same way.

### Q3: What's the difference between RequestValidationError and Pydantic's ValidationError?

**Answer:** `RequestValidationError` is raised by FastAPI when parsing request data (path params, query params, body). `ValidationError` is raised by Pydantic during manual validation in your code. FastAPI automatically handles `RequestValidationError` with 422 responses.

### Q4: How do you implement a global error handler for consistent error responses?

**Answer:** Register exception handlers on the app that return a standardized format:

```python
@app.exception_handler(Exception)
async def handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "INTERNAL_ERROR", "message": "..."}}
    )
```

Use a central `register_error_handlers(app)` function called during app initialization.

### Q5: Should you catch all exceptions or let some propagate?

**Answer:** Catch known exceptions (NotFound, Conflict, etc.) and return appropriate status codes. Let unexpected exceptions bubble up to a global handler that logs them and returns 500. Never silently swallow exceptions.

### Q6: How do you log errors in production FastAPI applications?

**Answer:** Use Python's `logging` module with structured logging. Log at appropriate levels: `warning` for client errors (4xx), `exception` for server errors (5xx). Include request context (method, path, request_id) in log entries. Never log sensitive data (passwords, tokens).

### Q7: What should an error response format look like?

**Answer:** Consistent, structured, and informative without leaking internals:

```json
{
    "success": false,
    "error": {
        "code": "NOT_FOUND",
        "message": "User not found"
    }
}
```

Include a machine-readable error code, a human-readable message, and optionally details for validation errors.
