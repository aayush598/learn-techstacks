# 04 - Path Parameters

## Table of Contents

1. [Path Parameter Syntax](#path-parameter-syntax)
2. [Type Conversion](#type-conversion)
3. [Validation](#validation)
4. [UUID Path Parameters](#uuid-path-parameters)
5. [Enum Path Parameters](#enum-path-parameters)
6. [Path Parameter Ordering](#path-parameter-ordering)
7. [Multiple Path Parameters](#multiple-path-parameters)
8. [Path Parameter Constraints](#path-parameter-constraints)
9. [Documented Examples](#documented-examples)
10. [Interview Questions](#interview-questions)

---

## Path Parameter Syntax

Path parameters are parts of the URL that are variable. They are defined using curly braces `{}` in the path string.

```python
from fastapi import FastAPI

app = FastAPI()

# Basic path parameter
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

# Multiple path parameters
@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(user_id: int, item_id: int):
    return {"user_id": user_id, "item_id": item_id}

# Path parameter with any type (string by default)
@app.get("/items/{item_id}")
async def get_item(item_id):
    return {"item_id": item_id}
```

### How It Works

When a request comes in:

1. FastAPI matches the URL against registered routes
2. Extracts the value from the `{placeholder}` position
3. Converts the string value to the declared Python type
4. Passes it to your function

```
GET /users/42
        ↑
   This value is extracted as user_id=42 (int)
```

### Path Parameters vs URL Segments

```python
# Path parameter (variable)
@app.get("/items/{item_id}")     # Matches /items/1, /items/abc, etc.

# Static path (fixed)
@app.get("/items/static")        # Only matches /items/static
```

---

## Type Conversion

FastAPI automatically converts string path parameters to the declared Python type:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    # Request: GET /items/42
    # item_id is automatically converted: "42" → 42 (int)
    return {"item_id": item_id, "type": type(item_id).__name__}

@app.get("/float/{value}")
async def get_float(value: float):
    # Request: GET /float/3.14
    # value: "3.14" → 3.14 (float)
    return {"value": value, "type": type(value).__name__}

@app.get("/bool/{flag}")
async def get_bool(flag: bool):
    # Request: GET /bool/true
    # flag: "true" → True (bool)
    return {"flag": flag, "type": type(flag).__name__}
```

### Boolean Conversion Rules

FastAPI uses `strtobool` conversion for path parameters:

| Input String | Converted To |
|-------------|--------------|
| `true`, `True`, `1`, `yes` | `True` |
| `false`, `False`, `0`, `no` | `False` |
| Anything else | Raises validation error |

```python
@app.get("/flag/{is_active}")
async def get_flag(is_active: bool):
    return {"is_active": is_active}

# These all work:
# GET /flag/true  → True
# GET /flag/True  → True
# GET /flag/1     → True
# GET /flag/false → False
# GET /flag/0     → False
```

### Invalid Type Conversion

```python
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}

# GET /items/abc
# Returns 422 Unprocessable Entity with error:
# {
#   "detail": [{
#     "type": "int_parsing",
#     "loc": ["path", "item_id"],
#     "msg": "Input should be a valid integer..."
#   }]
# }
```

---

## Validation

FastAPI validates path parameters using the declared types. If validation fails, it returns a `422 Unprocessable Entity` error with detailed information.

```python
from pydantic import Field

@app.get("/items/{item_id}")
async def get_item(item_id: int = Path(..., gt=0)):
    """Get an item by ID.
    
    - **item_id**: Must be a positive integer
    """
    return {"item_id": item_id}

# GET /items/-1 → 422 error: "Input should be greater than 0"
# GET /items/0  → 422 error: "Input should be greater than 0"
# GET /items/1  → 200 OK
```

### Pydantic Path Parameter Validation

```python
from pydantic import BaseModel, Field, field_validator
from fastapi import FastAPI, Path

app = FastAPI()

class UserID(BaseModel):
    id: int = Field(..., gt=0, description="User ID must be positive")

@app.get("/users/{user_id}")
async def get_user(user_id: int = Path(..., gt=0)):
    return {"user_id": user_id}
```

---

## UUID Path Parameters

UUIDs are commonly used for public-facing identifiers (more secure than sequential integers).

```python
from fastapi import FastAPI
from uuid import UUID

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: UUID):
    """Get a user by UUID.
    
    Example: GET /users/550e8400-e29b-41d4-a716-446655440000
    """
    return {"user_id": str(user_id)}

# GET /users/550e8400-e29b-41d4-a716-446655440000 → 200 OK
# GET /users/not-a-uuid → 422 Validation Error
```

### UUID Version Support

```python
from uuid import UUID

@app.get("/v1/{uuid_v1}")
async def get_uuid_v1(uuid_v1: UUID):
    """Supports UUID version 1 (time-based)."""
    return {"uuid": str(uuid_v1), "version": 1}

@app.get("/v4/{uuid_v4}")
async def get_uuid_v4(uuid_v4: UUID):
    """Supports UUID version 4 (random)."""
    return {"uuid": str(uuid_v4), "version": 4}
```

### UUID in Pydantic Models

```python
from uuid import UUID
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID):
    return UserResponse(
        id=user_id,
        name="John Doe",
        email="john@example.com"
    )
```

---

## Enum Path Parameters

When you want to restrict a path parameter to a set of fixed values:

```python
from enum import Enum
from fastapi import FastAPI

app = FastAPI()

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}
```

### How It Works

1. FastAPI validates that the path parameter matches one of the enum values
2. In the docs, the enum values appear as a dropdown
3. Invalid values return 422 with allowed values listed

```
GET /models/alexnet  → 200 OK
GET /models/resnet   → 200 OK
GET /models/lenet    → 200 OK
GET /models/vgg      → 422 Error (not in enum)
```

### Enum in Documentation

The Swagger UI shows a dropdown with all allowed values:

```
Model name:
  ▼ alexnet
    resnet
    lenet
```

### Advanced Enum Usage

```python
from enum import Enum
from fastapi import FastAPI

app = FastAPI()

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

class Category(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    books = "books"

@app.get("/products/{category}/{sort_order}")
async def list_products(category: Category, sort_order: SortOrder):
    return {
        "category": category,
        "sort_order": sort_order,
    }
```

---

## Path Parameter Ordering

Route order matters! FastAPI matches routes in the order they are defined.

### The Problem with Overlapping Routes

```python
# ⚠️ DANGER: Route ordering matters!
@app.get("/users/me")
async def read_current_user():
    return {"user_id": "current"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```

**Correct!** `/users/me` is defined first, so it matches before the pattern `/users/{user_id}`.

### The Problem (Wrong Order)

```python
# ❌ WRONG ORDER: /users/{user_id} will match /users/me too!
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    # When you request /users/me, user_id will be "me"
    return {"user_id": user_id}

@app.get("/users/me")
async def read_current_user():
    # This will NEVER be reached!
    return {"user_id": "current"}
```

### Best Practice: Put Static Routes First

```python
# ✅ CORRECT ORDER
@app.get("/users/me")        # Static route first
async def read_current_user():
    return {"user_id": "current"}

@app.get("/users/{user_id}")  # Parameterized route second
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/users/")           # List endpoint
async def list_users():
    return [{"user_id": "1"}, {"user_id": "2"}]
```

### Complete Route Ordering Example

```python
from fastapi import FastAPI
from uuid import UUID

app = FastAPI()

# 1. Health check (static)
@app.get("/api/health")
async def health():
    return {"status": "ok"}

# 2. Current user (static, before parameterized)
@app.get("/api/users/me")
async def current_user():
    return {"id": "current"}

# 3. User by ID (parameterized)
@app.get("/api/users/{user_id}")
async def get_user(user_id: UUID):
    return {"id": str(user_id)}

# 4. User items (nested parameterized)
@app.get("/api/users/{user_id}/items")
async def get_user_items(user_id: UUID):
    return {"items": []}
```

---

## Multiple Path Parameters

### Basic Multiple Path Parameters

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: int):
    return {"user_id": user_id, "item_id": item_id}

# GET /users/42/items/7 → {"user_id": 42, "item_id": 7}
```

### Mixed Types

```python
from uuid import UUID
from fastapi import FastAPI

app = FastAPI()

@app.get("/organizations/{org_id}/users/{user_id}")
async def get_org_user(org_id: UUID, user_id: UUID):
    return {"org_id": str(org_id), "user_id": str(user_id)}
```

### Deep Nested Paths

```python
@app.get("/companies/{company_id}/departments/{dept_id}/employees/{emp_id}")
async def get_employee(
    company_id: int,
    dept_id: int,
    emp_id: int,
):
    return {
        "company_id": company_id,
        "department_id": dept_id,
        "employee_id": emp_id,
    }
```

### Practical RESTful Example

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Comment(BaseModel):
    text: str
    author: str

# Resource hierarchy:
# /companies → /companies/{id}
# /companies/{id}/departments → /companies/{id}/departments/{dept_id}
# /companies/{id}/departments/{dept_id}/employees

@app.get("/companies/")
async def list_companies():
    return []

@app.get("/companies/{company_id}")
async def get_company(company_id: int):
    return {"id": company_id}

@app.get("/companies/{company_id}/departments/")
async def list_departments(company_id: int):
    return []

@app.get("/companies/{company_id}/departments/{dept_id}")
async def get_department(company_id: int, dept_id: int):
    return {"company_id": company_id, "dept_id": dept_id}

@app.get("/companies/{company_id}/departments/{dept_id}/employees/")
async def list_employees(company_id: int, dept_id: int):
    return []

@app.get("/companies/{company_id}/departments/{dept_id}/employees/{emp_id}")
async def get_employee(company_id: int, dept_id: int, emp_id: int):
    return {
        "company_id": company_id,
        "dept_id": dept_id,
        "emp_id": emp_id,
    }
```

---

## Path Parameter Constraints

### Using Path() for Constraints

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def get_item(
    item_id: int = Path(
        ...,                    # Required (no default)
        title="Item ID",        # Title in docs
        description="The ID of the item to retrieve",
        gt=0,                   # Greater than 0
        le=1000,                # Less than or equal to 1000
    )
):
    return {"item_id": item_id}
```

### All Path() Constraints

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/validate/{value}")
async def validate_value(
    value: str = Path(
        ...,
        min_length=3,           # Minimum string length
        max_length=50,          # Maximum string length
        pattern=r"^[a-zA-Z0-9]+$",  # Regex pattern
    )
):
    return {"value": value}

@app.get("/numbers/{num}")
async def validate_number(
    num: int = Path(
        ...,                    # Required
        gt=0,                   # Greater than (exclusive)
        ge=1,                   # Greater than or equal to (inclusive)
        lt=100,                 # Less than (exclusive)
        le=99,                  # Less than or equal to (inclusive)
        multiple_of=5,          # Must be multiple of 5
    )
):
    return {"num": num}
```

### Constraint Reference Table

| Constraint | Type | Description | Example |
|-----------|------|-------------|---------|
| `min_length` | str | Minimum length | `min_length=3` |
| `max_length` | str | Maximum length | `max_length=50` |
| `pattern` | str | Regex pattern | `pattern=r"^[a-z]+$"` |
| `gt` | numeric | Greater than | `gt=0` |
| `ge` | numeric | Greater than or equal | `ge=1` |
| `lt` | numeric | Less than | `lt=100` |
| `le` | numeric | Less than or equal | `le=99` |
| `multiple_of` | numeric | Multiple of | `multiple_of=5` |

### Practical Examples

```python
# Age must be between 0 and 150
@app.get("/users/{age}")
async def get_by_age(age: int = Path(..., ge=0, le=150)):
    return {"age": age}

# Username: 3-50 chars, alphanumeric and underscore
@app.get("/users/{username}")
async def get_by_username(
    username: str = Path(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
    )
):
    return {"username": username}

# Quantity must be positive and multiple of 5
@app.get("/orders/{quantity}")
async def get_quantity(
    quantity: int = Path(..., gt=0, multiple_of=5)
):
    return {"quantity": quantity}
```

---

## Documented Examples

### Complete Example with Documentation

```python
from fastapi import FastAPI, Path
from enum import Enum
from uuid import UUID

app = FastAPI()

class OrderStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

@app.get(
    "/orders/{order_id}",
    summary="Get an order by ID",
    description="Retrieve detailed information about a specific order including status and items.",
    response_model=dict,
    tags=["orders"],
)
async def get_order(
    order_id: UUID = Path(
        ...,
        title="Order ID",
        description="The unique identifier of the order (UUID v4)",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
):
    """
    Get detailed information about an order.
    
    - **order_id**: UUID of the order to retrieve
    - Returns order details including items, status, and total
    """
    return {
        "order_id": str(order_id),
        "status": "pending",
        "total": 99.99,
    }

@app.get(
    "/stores/{store_id}/products/{product_id}",
    summary="Get a product in a store",
    tags=["products"],
)
async def get_store_product(
    store_id: int = Path(..., gt=0, description="Store ID"),
    product_id: int = Path(..., gt=0, description="Product ID"),
):
    return {
        "store_id": store_id,
        "product_id": product_id,
    }

@app.get(
    "/users/{username}",
    summary="Get user by username",
    tags=["users"],
)
async def get_user(
    username: str = Path(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Username (3-50 chars, alphanumeric and underscores only)",
        examples=["john_doe"],
    )
):
    return {"username": username}
```

### Testing This API

```bash
# Valid requests
curl http://localhost:8000/orders/550e8400-e29b-41d4-a716-446655440000
curl http://localhost:8000/stores/1/products/42
curl http://localhost:8000/users/john_doe

# Invalid requests (will return 422)
curl http://localhost:8000/orders/not-a-uuid
curl http://localhost:8000/stores/-1/products/42
curl http://localhost:8000/users/ab
```

---

## Interview Questions

### Q1: How does FastAPI differentiate between path parameters and query parameters?

**Answer:** Path parameters are defined in the URL path with `{}` syntax (e.g., `/items/{item_id}`), while query parameters are defined as function parameters with defaults (e.g., `q: str = None`). If a parameter is in the path template, it's a path parameter. If it's a function parameter not in the path, it's a query parameter.

### Q2: What happens if you have two routes with overlapping paths?

**Answer:** FastAPI matches routes in definition order. If you define `/users/{user_id}` before `/users/me`, the pattern route will match `/users/me` first, and `user_id` will be `"me"`. Always define static routes before parameterized routes.

### Q3: Can path parameters be optional?

**Answer:** No. Path parameters are always required because they are part of the URL structure. If you need optional values, use query parameters instead. You can make query parameters optional with `None` defaults.

### Q4: How does FastAPI validate UUID path parameters?

**Answer:** When you declare a path parameter as `UUID`, FastAPI validates that the string matches the UUID format (e.g., `550e8400-e29b-41d4-a716-446655440000`). Invalid UUIDs return a 422 error. FastAPI supports all UUID versions.

### Q5: What is the difference between `gt` and `ge` in Path constraints?

**Answer:** `gt` means "greater than" (exclusive) - the value must be strictly greater than the limit. `ge` means "greater than or equal to" (inclusive) - the value can equal the limit. Similarly, `lt` is "less than" (exclusive) and `le` is "less than or equal to" (inclusive).

### Q6: Can you use regex patterns for path parameter validation?

**Answer:** Yes, using the `pattern` parameter in `Path()`:

```python
@app.get("/users/{username}")
async def get_user(
    username: str = Path(..., pattern=r"^[a-zA-Z0-9_]+$")
):
    return {"username": username}
```

This validates the path parameter against the regex before passing it to your function.
