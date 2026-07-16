# 06 - Request Body

## Table of Contents

1. [Request Body with Pydantic](#request-body-with-pydantic)
2. [POST with Body](#post-with-body)
3. [Body Field Parameters](#body-field-parameters)
4. [Nested Models](#nested-models)
5. [Body Field Options](#body-field-options)
6. [Form Data](#form-data)
7. [File Upload Combined with Body](#file-upload-combined-with-body)
8. [JSON vs Form Data](#json-vs-form-data)
9. [Request Object Access](#request-object-access)
10. [Interview Questions](#interview-questions)

---

## Request Body with Pydantic

When you need to send data from a client to your API, you send it as a **request body**. In FastAPI, request bodies are declared using **Pydantic models**.

### Basic Request Body

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int
    email: str
    is_active: bool = True

@app.post("/users/")
async def create_user(user: User):
    return {
        "name": user.name,
        "age": user.age,
        "email": user.email,
        "is_active": user.is_active,
    }
```

### What Happens When You Send a Request

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "age": 30, "email": "john@example.com"}'
```

FastAPI will:
1. Read the request body as JSON
2. Validate the JSON against the `User` model schema
3. Convert the JSON to a `User` Pydantic model instance
4. Pass the validated model to your function
5. If validation fails, return a 422 error with detailed error information

### Request Body + Path + Query Parameters

You can combine all parameter types in a single endpoint:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,           # Path parameter
    q: str | None = None,   # Query parameter
    item: Item = None,      # Request body (optional)
):
    result = {"item_id": item_id}
    if q:
        result["q"] = q
    if item:
        result["item"] = item.model_dump()
    return result

# PUT /items/42?q=some-query
# Body: {"name": "Laptop", "price": 999.99}
```

### Single Body Value

If you want to send a single value (not an object) as the request body:

```python
from fastapi import Body

@app.put("/items/{item_id}")
async def update_item(item_id: int, name: str = Body(...)):
    return {"item_id": item_id, "name": name}

# Body: "Laptop"  (raw string, not JSON object)
# Content-Type: application/json
```

---

## POST with Body

### Creating Resources

```python
from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str | None
    is_active: bool

@app.post(
    "/users/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
async def create_user(user: UserCreate):
    """Create a new user with the provided information."""
    # In real app: hash password, save to database, etc.
    return UserResponse(
        id=1,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        is_active=True,
    )
```

### Multiple Body Parameters

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

class User(BaseModel):
    username: str

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
):
    return {
        "item_id": item_id,
        "item": item.model_dump(),
        "user": user.model_dump(),
    }
```

### Embedding a Single Body Parameter

By default, FastAPI expects the body to match the model directly. To nest it in a key:

```python
@app.post("/items/")
async def create_item(item: Item, embed: bool = Body(False)):
    return item

# Without embed (default):
# {"name": "Laptop", "price": 999.99}

# With embed=True:
# {"item": {"name": "Laptop", "price": 999.99}}
```

---

## Body Field Parameters

### Using Body() for Validation

```python
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
async def create_item(
    item: Item,
    importance: int = Body(
        ...,
        gt=0,
        le=10,
        description="Importance level (1-10)",
    ),
    notes: str = Body(
        None,
        max_length=500,
        description="Optional notes about the item",
    ),
):
    return {
        "item": item.model_dump(),
        "importance": importance,
        "notes": notes,
    }
```

### Body with Examples

```python
@app.post("/users/")
async def create_user(
    username: str = Body(
        ...,
        min_length=3,
        max_length=50,
        examples=["john_doe"],  # Examples in docs
        description="Unique username",
    ),
    age: int = Body(
        ...,
        gt=0,
        lt=150,
        examples=[25],
        description="User age",
    ),
):
    return {"username": username, "age": age}
```

### Body with Alias

```python
@app.post("/items/")
async def create_item(
    item_name: str = Body(..., alias="itemName"),
    item_price: float = Body(..., alias="itemPrice"),
):
    return {"name": item_name, "price": item_price}

# Body: {"itemName": "Laptop", "itemPrice": 999.99}
```

---

## Nested Models

### Simple Nesting

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "US"

class User(BaseModel):
    name: str
    email: str
    address: Address

@app.post("/users/")
async def create_user(user: User):
    return {
        "name": user.name,
        "city": user.address.city,
    }

# Body:
# {
#     "name": "John",
#     "email": "john@example.com",
#     "address": {
#         "street": "123 Main St",
#         "city": "Springfield",
#         "state": "IL",
#         "zip_code": "62704"
#     }
# }
```

### Deeply Nested Models

```python
class PhoneNumber(BaseModel):
    type: str  # "home", "work", "mobile"
    number: str

class ContactInfo(BaseModel):
    emails: list[str]
    phones: list[PhoneNumber]

class Profile(BaseModel):
    bio: str | None = None
    avatar_url: str | None = None
    contact: ContactInfo

class User(BaseModel):
    name: str
    profile: Profile

@app.post("/users/")
async def create_user(user: User):
    return user.model_dump()

# Body:
# {
#     "name": "John",
#     "profile": {
#         "bio": "Software developer",
#         "avatar_url": "https://example.com/avatar.jpg",
#         "contact": {
#             "emails": ["john@example.com"],
#             "phones": [
#                 {"type": "mobile", "number": "+1-555-0100"},
#                 {"type": "work", "number": "+1-555-0101"}
#             ]
#         }
#     }
# }
```

### Lists of Models

```python
class Item(BaseModel):
    name: str
    quantity: int
    price: float

class Order(BaseModel):
    customer_name: str
    items: list[Item]
    notes: str | None = None

@app.post("/orders/")
async def create_order(order: Order):
    total = sum(item.quantity * item.price for item in order.items)
    return {
        "customer": order.customer_name,
        "item_count": len(order.items),
        "total": total,
    }

# Body:
# {
#     "customer_name": "John",
#     "items": [
#         {"name": "Laptop", "quantity": 1, "price": 999.99},
#         {"name": "Mouse", "quantity": 2, "price": 29.99}
#     ],
#     "notes": "Gift wrap please"
# }
```

### Union Types in Models

```python
from pydantic import BaseModel, Field

class TextContent(BaseModel):
    type: str = "text"
    text: str

class ImageContent(BaseModel):
    type: str = "image"
    url: str
    alt_text: str

class VideoContent(BaseModel):
    type: str = "video"
    url: str
    duration_seconds: int

class Message(BaseModel):
    content: TextContent | ImageContent | VideoContent

@app.post("/messages/")
async def send_message(message: Message):
    return {"received": type(message.content).__name__}
```

### Discriminated Unions (Recommended)

```python
from typing import Literal, Annotated
from pydantic import BaseModel, Field

class Cat(BaseModel):
    type: Literal["cat"] = "cat"
    meow_volume: int

class Dog(BaseModel):
    type: Literal["dog"] = "dog"
    bark_volume: int

class Pet(BaseModel):
    owner_name: str
    pet: Annotated[Cat | Dog, Field(discriminator="type")]

@app.post("/pets/")
async def register_pet(pet: Pet):
    if isinstance(pet.pet, Cat):
        return {"message": f"Cat registered for {pet.owner_name}"}
    return {"message": f"Dog registered for {pet.owner_name}"}
```

---

## Body Field Options

### Embed

```python
# Without embed (default)
@app.post("/items/")
async def create_item(item: Item):
    return item
# Body: {"name": "Laptop", "price": 999.99}

# With embed
@app.post("/items/")
async def create_item(item: Item = Body(..., embed=True)):
    return item
# Body: {"item": {"name": "Laptop", "price": 999.99}}
```

### Alias in Body

```python
@app.post("/items/")
async def create_item(
    name: str = Body(..., alias="itemName"),
    price: float = Body(..., alias="itemPrice"),
):
    return {"name": name, "price": price}

# Body: {"itemName": "Laptop", "itemPrice": 999.99}
```

### Example Values

```python
@app.post("/users/")
async def create_user(
    username: str = Body(
        ...,
        examples=["john_doe", "jane_smith"],
        description="Unique username (3-50 chars)"
    ),
    age: int = Body(
        ...,
        examples=[25, 30],
        description="User age"
    ),
):
    return {"username": username, "age": age}
```

### Media Type

```python
@app.post("/data/")
async def receive_data(
    data: str = Body(
        ...,
        media_type="text/plain",
        description="Raw text data",
    )
):
    return {"received": data}

# Content-Type: text/plain
# Body: Hello, World!
```

---

## Form Data

### Basic Form Data

```python
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(
    username: str = Form(...),
    password: str = Form(...),
):
    return {"username": username}

# Content-Type: application/x-www-form-urlencoded
# Body: username=john&password=secret123
```

### Form Data + File Upload

```python
from fastapi import FastAPI, Form, File, UploadFile

@app.post("/upload-profile/")
async def upload_profile(
    username: str = Form(...),
    bio: str = Form(""),
    avatar: UploadFile = File(...),
):
    return {
        "username": username,
        "bio": bio,
        "filename": avatar.filename,
        "content_type": avatar.content_type,
    }
```

### Form Data with Validation

```python
from fastapi import Form

@app.post("/submit/")
async def submit_form(
    name: str = Form(..., min_length=1, max_length=100),
    email: str = Form(..., max_length=200),
    age: int = Form(..., ge=0, le=150),
    agree_terms: bool = Form(...),
):
    if not agree_terms:
        from fastapi import HTTPException
        raise HTTPException(400, "Must agree to terms")
    return {"name": name, "email": email, "age": age}
```

### Multiple Form Values

```python
from fastapi import Form
from typing import Annotated

@app.post("/tags/")
async def create_tags(
    tags: Annotated[list[str], Form()],
):
    return {"tags": tags}

# Content-Type: application/x-www-form-urlencoded
# Body: tags=python&tags=fastapi&tags=async
```

---

## File Upload Combined with Body

### Basic File Upload

```python
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents),
    }
```

### Multiple File Upload

```python
@app.post("/upload-multiple/")
async def upload_multiple(files: list[UploadFile] = File(...)):
    results = []
    for file in files:
        contents = await file.read()
        results.append({
            "filename": file.filename,
            "size": len(contents),
        })
    return {"files": results}
```

### File + Metadata

```python
from pydantic import BaseModel

class DocumentMeta(BaseModel):
    title: str
    description: str
    tags: list[str] = []

@app.post("/documents/")
async def upload_document(
    meta: DocumentMeta,
    file: UploadFile = File(...),
):
    contents = await file.read()
    return {
        "metadata": meta.model_dump(),
        "filename": file.filename,
        "size": len(contents),
    }
```

### File with Form Data

```python
@app.post("/products/")
async def create_product(
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(..., gt=0),
    image: UploadFile = File(...),
):
    contents = await image.read()
    return {
        "name": name,
        "description": description,
        "price": price,
        "image_filename": image.filename,
        "image_size": len(contents),
    }
```

### File Validation

```python
from fastapi import HTTPException

ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]
MAX_SIZE = 5 * 1024 * 1024  # 5MB

@app.post("/avatar/")
async def upload_avatar(avatar: UploadFile = File(...)):
    if avatar.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {ALLOWED_TYPES}"
        )
    
    contents = await avatar.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {MAX_SIZE / 1024 / 1024}MB"
        )
    
    return {"filename": avatar.filename, "size": len(contents)}
```

---

## JSON vs Form Data

| Feature | JSON Body | Form Data |
|---------|-----------|-----------|
| Content-Type | `application/json` | `application/x-www-form-urlencoded` or `multipart/form-data` |
| Data types | Supports nested objects, arrays | Flat key-value pairs |
| File upload | No (use multipart) | Yes (multipart/form-data) |
| Human readable | Yes | Somewhat |
| Validation | Pydantic models | Form() parameters |
| Browser support | Fetch/AJAX | HTML forms |
| Binary data | No | Yes (multipart) |
| Use case | API-to-API | HTML forms, file uploads |

### When to Use Which

```python
# Use JSON body for:
# - REST APIs
# - Nested data structures
# - API-to-API communication
@app.post("/api/users/")
async def create_user(user: UserCreate):
    return user

# Use Form data for:
# - HTML form submissions
# - File uploads
# - Simple flat data
@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"token": "..."}
```

---

## Request Object Access

### Full Request Object

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/request-info/")
async def get_request_info(request: Request):
    return {
        "method": request.method,
        "url": str(request.url),
        "path": request.url.path,
        "query_params": dict(request.query_params),
        "headers": dict(request.headers),
        "client": {
            "host": request.client.host,
            "port": request.client.port,
        },
        "cookies": request.cookies,
    }
```

### Request Headers

```python
@app.get("/headers/")
async def get_headers(request: Request):
    return {
        "content_type": request.headers.get("content-type"),
        "user_agent": request.headers.get("user-agent"),
        "authorization": request.headers.get("authorization"),
        "all_headers": dict(request.headers),
    }
```

### Request Cookies

```python
@app.get("/cookies/")
async def get_cookies(request: Request):
    return {
        "session_id": request.cookies.get("session_id"),
        "theme": request.cookies.get("theme"),
        "all_cookies": request.cookies,
    }
```

### Request State

```python
@app.middleware("http")
async def add_user_to_state(request: Request, call_next):
    # Add custom data to request state
    request.state.user_id = "anonymous"
    response = await call_next(request)
    return response

@app.get("/profile/")
async def get_profile(request: Request):
    return {"user_id": request.state.user_id}
```

### Request Body (Raw)

```python
@app.post("/raw-body/")
async def receive_raw_body(request: Request):
    body = await request.body()
    return {
        "body": body.decode("utf-8"),
        "size": len(body),
    }

@app.post("/json-body/")
async def receive_json_body(request: Request):
    json_body = await request.json()
    return {"data": json_body}
```

---

## Interview Questions

### Q1: What is the difference between a path parameter, query parameter, and request body?

**Answer:** Path parameters are part of the URL path (`/items/{id}`), query parameters are after the `?` in the URL (`?q=search`), and request body is sent in the HTTP body (usually JSON). FastAPI distinguishes them: path params come from the URL template, query params from non-path function parameters, and request body from Pydantic model parameters.

### Q2: How does FastAPI validate request body data?

**Answer:** FastAPI uses Pydantic models for validation. When a request arrives, it parses the JSON body, validates every field against the model's type hints and constraints, and returns a 422 error with detailed messages if validation fails. The validation happens before your endpoint code runs.

### Q3: Can you have both a request body and query parameters in the same endpoint?

**Answer:** Yes. FastAPI distinguishes them based on parameter type. Path/query params are simple types, request bodies are Pydantic models:

```python
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,           # Path param
    q: str | None = None,   # Query param
    item: Item = ...,       # Request body
):
    pass
```

### Q4: When should you use Form data vs JSON body?

**Answer:** Use JSON for REST APIs with nested data structures. Use Form data for HTML form submissions, file uploads (multipart/form-data), or when the client doesn't support JSON. Form data is flat key-value pairs; JSON supports nested objects and arrays.

### Q5: What is the `embed` option in Body()?

**Answer:** `embed=True` wraps the request body in a key matching the parameter name. Without embed, the body is the model directly. With embed, it's nested:

```python
# Without embed: {"name": "Laptop", "price": 999}
# With embed: {"item": {"name": "Laptop", "price": 999}}
async def create(item: Item = Body(..., embed=True)):
    pass
```

### Q6: How do you access raw request data in FastAPI?

**Answer:** Use the `Request` object:

```python
@app.get("/info/")
async def info(request: Request):
    body = await request.body()          # Raw bytes
    json_data = await request.json()     # Parsed JSON
    headers = request.headers            # Headers dict
    cookies = request.cookies            # Cookies dict
    query = request.query_params         # Query params dict
    state = request.state                # Custom state
```

### Q7: How do you handle file uploads in FastAPI?

**Answer:** Use `UploadFile = File(...)`:

```python
@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}
```

For multiple files: `files: list[UploadFile] = File(...)`. Always validate file type and size in production.
