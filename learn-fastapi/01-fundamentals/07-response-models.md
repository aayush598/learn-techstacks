# 07 - Response Models

## Table of Contents

1. [response_model Parameter](#response_model-parameter)
2. [Status Code in Decorator](#status-code-in-decorator)
3. [Response Classes](#response-classes)
4. [response_model_exclude_unset](#response_model_exclude_unset)
5. [response_model_include / response_model_exclude](#response_model_include--response_model_exclude)
6. [Custom Serialization](#custom-serialization)
7. [FastAPI Response Classes](#fastapi-response-classes)
8. [Annotated vs Return Annotation](#annotated-vs-return-annotation)
9. [Interview Questions](#interview-questions)

---

## response_model Parameter

The `response_model` parameter validates and serializes the return value of your endpoint. It ensures the response always matches a specific schema, regardless of what your function returns.

### Basic Usage

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    # Even if you return a dict, it's validated against User
    return {
        "id": user_id,
        "username": "johndoe",
        "email": "john@example.com",
        "full_name": "John Doe",
        "is_active": True,
    }
```

### What response_model Does

1. **Filters the response**: Only fields defined in the model are included
2. **Validates the response**: Checks the return value matches the schema
3. **Serializes to JSON**: Converts the Pydantic model to JSON
4. **Generates documentation**: Creates the response schema in OpenAPI docs

```python
@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    return {
        "id": user_id,
        "username": "johndoe",
        "email": "john@example.com",
        "full_name": "John Doe",
        "is_active": True,
        "password": "secret123",  # ⚠️ This field is FILTERED OUT
        "internal_id": 456,       # ⚠️ This field is FILTERED OUT
    }
# Response: {"id": 1, "username": "johndoe", "email": "john@example.com", ...}
# password and internal_id are NOT in the response
```

### response_model vs Return Type Annotation

```python
# These two are equivalent:

# Method 1: response_model parameter
@app.get("/users/", response_model=list[User])
async def list_users():
    return [{"id": 1, "username": "john"}]

# Method 2: Return type annotation (Python 3.10+)
@app.get("/users/")
async def list_users() -> list[User]:
    return [{"id": 1, "username": "john"}]

# Method 3: Annotated (Python 3.10+)
from typing import Annotated
from fastapi import Depends

@app.get("/users/")
async def list_users() -> Annotated[list[User], Depends()]:
    return [{"id": 1, "username": "john"}]
```

### Different Response Models for Input vs Output

```python
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

@app.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    # user is UserCreate (includes password)
    # Response is UserResponse (excludes password)
    return UserResponse(
        id=1,
        username=user.username,
        email=user.email,
        created_at=datetime.now(),
    )
```

---

## Status Code in Decorator

### Setting Status Codes

```python
from fastapi import FastAPI, status

app = FastAPI()

# Using status constants (recommended)
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    return None

# Using integer directly
@app.post("/items2/", status_code=201)
async def create_item2(item: Item):
    return item
```

### Status Code with Response Model

```python
@app.post(
    "/users/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a user with the provided information.",
    response_description="The created user object",
)
async def create_user(user: UserCreate):
    return UserResponse(id=1, username=user.username, email=user.email)
```

### Status Code Override with JSONResponse

```python
from fastapi.responses import JSONResponse

@app.post("/items/")
async def create_item(item: Item):
    if not item.name:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Name is required"},
        )
    return {"id": 1, **item.model_dump()}
```

---

## Response Classes

### JSONResponse (Default)

```python
from fastapi.responses import JSONResponse

@app.get("/items/")
async def list_items():
    return JSONResponse(
        content={"items": [{"id": 1}, {"id": 2}]},
        status_code=200,
        headers={"X-Total-Count": "2"},
    )
```

### RedirectResponse

```python
from fastapi.responses import RedirectResponse

@app.get("/old-endpoint/")
async def old_endpoint():
    return RedirectResponse(url="/new-endpoint/")

@app.get("/new-endpoint/")
async def new_endpoint():
    return {"message": "This is the new endpoint"}
```

### HTMLResponse

```python
from fastapi.responses import HTMLResponse

@app.get("/page/", response_class=HTMLResponse)
async def get_page():
    return """
    <html>
        <head><title>My Page</title></head>
        <body>
            <h1>Hello, World!</h1>
            <p>This is an HTML response.</p>
        </body>
    </html>
    """

# Or return HTML from a file
from pathlib import Path

@app.get("/page2/", response_class=HTMLResponse)
async def get_page2():
    html_content = Path("templates/index.html").read_text()
    return HTMLResponse(content=html_content)
```

### StreamingResponse

```python
from fastapi.responses import StreamingResponse
import io

@app.get("/stream/")
async def stream_data():
    async def generate():
        for i in range(100):
            yield f"data: {i}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
    )

# Stream a file
@app.get("/large-file/")
async def stream_file():
    def file_generator():
        with open("large_file.csv", "rb") as f:
            while chunk := f.read(8192):
                yield chunk
    
    return StreamingResponse(
        file_generator(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=data.csv"},
    )
```

### FileResponse

```python
from fastapi.responses import FileResponse

@app.get("/files/{filename}")
async def get_file(filename: str):
    file_path = f"./files/{filename}"
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream",
    )

# With custom headers
@app.get("/download/{filename}")
async def download_file(filename: str):
    return FileResponse(
        path=f"./files/{filename}",
        filename=filename,
        headers={"X-Custom-Header": "download"},
    )
```

### PlainTextResponse

```python
from fastapi.responses import PlainTextResponse

@app.get("/plain/", response_class=PlainTextResponse)
async def plain_text():
    return "This is plain text"
```

### Custom Response Class

```python
from fastapi.responses import Response

class XMLResponse(Response):
    media_type = "application/xml"

@app.get("/xml/", response_class=XMLResponse)
async def xml_response():
    return "<root><item>value</item></root>"
```

---

## response_model_exclude_unset

This is useful when you want to return only the fields that were explicitly set, not the default values.

### Problem Without exclude_unset

```python
class User(BaseModel):
    id: int
    name: str
    is_active: bool = True
    age: int | None = None

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate):
    # If user only sends {"name": "New Name"}
    # The response would include defaults: {"id": ..., "name": "New Name", "is_active": True, "age": None}
    # This is misleading - the client didn't set is_active or age
    ...
```

### Solution with exclude_unset

```python
@app.put("/users/{user_id}", response_model=User, response_model_exclude_unset=True)
async def update_user(user_id: int, user: UserUpdate):
    # Now only fields the client explicitly set are in the response
    # If client sent {"name": "New Name"}, response is {"name": "New Name"}
    ...
```

### Practical Example

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None
    bio: str = "No bio provided"

users_db = {1: User(id=1, name="John", email="john@example.com", age=30, bio="Developer")}

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    age: int | None = None
    bio: str | None = None

@app.put("/users/{user_id}", response_model=User, response_model_exclude_unset=True)
async def update_user(user_id: int, updates: UserUpdate):
    user = users_db[user_id]
    update_data = updates.model_dump(exclude_unset=True)
    user_dict = user.model_dump()
    user_dict.update(update_data)
    users_db[user_id] = User(**user_dict)
    return users_db[user_id]

# If client sends: {"name": "Jane"}
# Response: {"id": 1, "name": "Jane", "email": "john@example.com"}
# age and bio are NOT included (they weren't set in the update)
```

---

## response_model_include / response_model_exclude

### response_model_include

Only include specific fields in the response:

```python
@app.get("/users/{user_id}", response_model=User, response_model_include={"id", "name"})
async def get_user(user_id: int):
    return User(id=1, name="John", email="john@example.com", age=30)
# Response: {"id": 1, "name": "John"}
```

### response_model_exclude

Exclude specific fields from the response:

```python
@app.get("/users/{user_id}", response_model=User, response_model_exclude={"email", "age"})
async def get_user(user_id: int):
    return User(id=1, name="John", email="john@example.com", age=30)
# Response: {"id": 1, "name": "John", "bio": "..."}
```

### Use Cases

```python
# Public profile (minimal info)
@app.get("/public/users/{user_id}", response_model=User, response_model_include={"id", "name"})
async def get_public_user(user_id: int):
    return get_user_from_db(user_id)

# Admin view (everything except sensitive data)
@app.get("/admin/users/{user_id}", response_model=User, response_model_exclude={"password_hash"})
async def get_admin_user(user_id: int):
    return get_user_from_db(user_id)

# List view (lightweight)
@app.get("/users/", response_model=User, response_model_include={"id", "name", "email"})
async def list_users():
    return get_all_users()
```

---

## Custom Serialization

### model_serializer

```python
from pydantic import BaseModel, model_serializer

class User(BaseModel):
    id: int
    username: str
    email: str
    password_hash: str

    @model_serializer
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            # password_hash is automatically excluded
        }

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    return User(
        id=1,
        username="johndoe",
        email="john@example.com",
        password_hash="hashed_password",
    )
```

### field_serializer

```python
from pydantic import BaseModel, field_serializer
from datetime import datetime

class Event(BaseModel):
    name: str
    date: datetime

    @field_serializer("date")
    def serialize_date(self, date: datetime):
        return date.isoformat()

@app.get("/events/", response_model=Event)
async def get_event():
    return Event(name="Conference", date=datetime.now())
```

### Computed Fields

```python
from pydantic import BaseModel, Field, computed_field

class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height

@app.get("/rectangle/", response_model=Rectangle)
async def get_rectangle():
    return Rectangle(width=5.0, height=3.0)
# Response: {"width": 5.0, "height": 3.0, "area": 15.0}
```

---

## FastAPI Response Classes

### Using response_class in Decorator

```python
from fastapi.responses import HTMLResponse, PlainTextResponse, ORJSONResponse

@app.get("/", response_class=HTMLResponse)
async def root():
    return "<h1>Hello, World!</h1>"

@app.get("/text/", response_class=PlainTextResponse)
async def text():
    return "Plain text response"

@app.get("/fast-json/", response_class=ORJSONResponse)
async def fast_json():
    return {"message": "Fast JSON response"}
```

### ORJSONResponse (Faster JSON)

```python
from fastapi.responses import ORJSONResponse

app = FastAPI(default_response_class=ORJSONResponse)

# ORJSON is written in Rust and is significantly faster
# than standard json for serialization
```

### Custom Response with Headers

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/custom/")
async def custom_response():
    return JSONResponse(
        content={"message": "Hello"},
        status_code=200,
        headers={
            "X-Custom-Header": "value",
            "Cache-Control": "max-age=3600",
            "X-Request-Id": "12345",
        },
    )
```

---

## Annotated vs Return Annotation

### Python 3.10+ with Annotated

```python
from typing import Annotated
from fastapi import FastAPI, Query, Path, Body

app = FastAPI()

# Clean, readable parameter definitions
@app.get("/items/{item_id}")
async def get_item(
    item_id: Annotated[int, Path(..., gt=0)],
    q: Annotated[str | None, Query(min_length=3, max_length=50)] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    return {"item_id": item_id, "q": q, "skip": skip, "limit": limit}
```

### Return Type Annotation

```python
# Using -> for return type
@app.get("/users/")
async def list_users() -> list[User]:
    return [{"id": 1, "name": "John"}]

# Using response_model (equivalent)
@app.get("/users/", response_model=list[User])
async def list_users():
    return [{"id": 1, "name": "John"}]

# Both generate the same OpenAPI schema and validation
```

### When to Use Which

| Approach | When to Use |
|----------|-------------|
| `response_model=X` | When you need `response_model_exclude_unset`, `include`, `exclude` |
| `-> X` (return type) | Simple cases without extra options |
| `Annotated[X, ...]` | For parameter validation (not response models) |

### Full Example with Both

```python
from typing import Annotated
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str

# response_model for response options
@app.get(
    "/users/{user_id}",
    response_model=User,
    response_model_exclude_unset=True,
)
async def get_user(
    user_id: Annotated[int, Path(..., gt=0)],
    fields: Annotated[list[str] | None, Query()] = None,
) -> User:
    # Annotated for parameter validation
    # -> User for return type
    return User(id=user_id, name="John", email="john@example.com")
```

---

## Interview Questions

### Q1: What is the difference between `response_model` and `response_model_exclude_unset`?

**Answer:** `response_model` validates and serializes the entire response. `response_model_exclude_unset=True` filters the response to only include fields that were explicitly set (not default values). This is useful for PATCH/PUT endpoints where you only want to return what the client actually updated.

### Q2: How does FastAPI filter response data?

**Answer:** FastAPI uses the `response_model` to filter. It only includes fields defined in the model, excluding any extra fields your function might return (like `password_hash`). It also applies Pydantic's serialization rules, so computed fields, validators, and serializers all run.

### Q3: When should you use `JSONResponse` instead of returning a dict?

**Answer:** Use `JSONResponse` when you need to set custom status codes, headers, or media types beyond what `status_code` in the decorator provides. For simple cases, returning a dict is cleaner and FastAPI handles the conversion automatically.

### Q4: What is the difference between `response_model` and `response_class`?

**Answer:** `response_model` defines the Pydantic model for validation and filtering. `response_class` defines the HTTP response type (JSONResponse, HTMLResponse, etc.). They serve different purposes and can be used together.

### Q5: How do you return different response schemas for the same endpoint?

**Answer:** Use `response_model_include` or `response_model_exclude` parameters, or create separate endpoints for different views. You can also use `model.model_dump()` with specific fields and return a dict.

### Q6: What is ORJSONResponse and when should you use it?

**Answer:** `ORJSONResponse` uses the `orjson` library (written in Rust) for JSON serialization, which is significantly faster than Python's built-in `json` module. Use it for endpoints that return large JSON payloads or need high throughput. Set it as the default with `FastAPI(default_response_class=ORJSONResponse)`.

### Q7: Can you use `-> list[User]` instead of `response_model=list[User]`?

**Answer:** Yes, they are equivalent for basic cases. However, `response_model` supports extra options like `response_model_exclude_unset`, `response_model_include`, and `response_model_exclude`. If you don't need those, the return type annotation is cleaner.
