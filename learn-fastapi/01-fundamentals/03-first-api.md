# 03 - First API

## Table of Contents

1. [Hello World](#hello-world)
2. [Creating HTTP Endpoints](#creating-http-endpoints)
3. [The @app Decorator](#the-app-decorator)
4. [Automatic Documentation](#automatic-documentation)
5. [Request/Response Flow](#requestresponse-flow)
6. [Status Codes](#status-codes)
7. [JSON Responses](#json-responses)
8. [Testing with curl/httpie](#testing-with-curlhttpie)
9. [Testing in Swagger UI](#testing-in-swagger-ui)
10. [Interview Questions](#interview-questions)

---

## Hello World

### The Absolute Minimum

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}
```

Run it:

```bash
uvicorn main:app --reload
```

Visit:
- `http://localhost:8000` - Your API response
- `http://localhost:8000/docs` - Swagger UI
- `http://localhost:8000/redoc` - ReDoc

### What's Happening Under the Hood?

```python
# 1. We create a FastAPI application instance
app = FastAPI()

# 2. We use the @app.get("/") decorator to create a GET endpoint at "/"
@app.get("/")
async def root():
    # 3. This async function is the "path operation function"
    #    It runs when a client sends a GET request to "/"
    return {"message": "Hello, World!"}
    # 4. FastAPI automatically converts the dict to JSON
    #    and wraps it in a proper HTTP response
```

### Synchronous vs Async

```python
# Async (recommended for I/O-bound operations)
@app.get("/async")
async def async_endpoint():
    result = await some_async_operation()
    return {"result": result}

# Synchronous (use for CPU-bound operations)
@app.get("/sync")
def sync_endpoint():
    result = some_sync_operation()
    return {"result": result}

# FastAPI runs sync endpoints in a threadpool automatically
# so they don't block the event loop
```

> **When to use which?**
> - Use `async def` when you have `await` calls (database queries with async driver, HTTP requests, etc.)
> - Use `def` (sync) when doing CPU-bound work or using synchronous libraries
> - Both perform similarly for simple endpoints

---

## Creating HTTP Endpoints

### GET Endpoint

```python
from fastapi import FastAPI

app = FastAPI()

# Simple GET
@app.get("/")
async def root():
    return {"message": "Hello World"}

# GET with path parameter
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}

# GET with query parameters
@app.get("/search/")
async def search(q: str, page: int = 1):
    return {"query": q, "page": page}
```

### POST Endpoint

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/", status_code=201)
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
```

### PUT Endpoint

```python
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}
```

### PATCH Endpoint

```python
from pydantic import BaseModel

class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None

@app.patch("/items/{item_id}")
async def partial_update_item(item_id: int, item: ItemUpdate):
    update_data = item.model_dump(exclude_unset=True)
    return {"item_id": item_id, **update_data}
```

### DELETE Endpoint

```python
@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    # Perform deletion logic here
    return None  # 204 No Content
```

### All CRUD Operations Together

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    published_year: int
    genre: str = "general"

# In-memory storage for demonstration
books: dict[int, Book] = {}
next_id = 1

@app.get("/books/", response_model=list[Book])
async def list_books():
    """List all books."""
    return list(books.values())

@app.post("/books/", response_model=Book, status_code=201)
async def create_book(book: Book):
    """Create a new book."""
    global next_id
    books[next_id] = book
    book_id = next_id
    next_id += 1
    return books[book_id]

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    """Get a specific book by ID."""
    if book_id not in books:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book: Book):
    """Update a book completely."""
    if book_id not in books:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Book not found")
    books[book_id] = book
    return books[book_id]

@app.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: int):
    """Delete a book."""
    if book_id not in books:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Book not found")
    del books[book_id]
    return None
```

---

## The @app Decorator

### How Decorators Work in FastAPI

```python
# This decorator:
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}

# Is equivalent to:
async def get_item(item_id: int):
    return {"item_id": item_id}

app.add_api_route("/items/{item_id}", get_item, methods=["GET"])
```

### HTTP Method Decorators

```python
@app.get("/path")      # GET requests
@app.post("/path")     # POST requests
@app.put("/path")      # PUT requests
@app.delete("/path")   # DELETE requests
@app.patch("/path")    # PATCH requests
@app.options("/path")  # OPTIONS requests
@app.head("/path")     # HEAD requests
@app.trace("/path")    # TRACE requests
```

### Decorator Parameters

```python
@app.get(
    "/items/{item_id}",
    response_model=Item,               # Response validation
    status_code=200,                    # Default status code
    tags=["items"],                     # Tags for documentation
    summary="Get an item",             # Short summary
    description="Get a specific item by its ID",  # Long description
    response_description="The requested item",    # Response description
    deprecated=True,                    # Mark as deprecated
    include_in_schema=True,            # Include in OpenAPI docs
    name="get_item",                   # Unique operation name
)
async def get_item(item_id: int):
    return {"item_id": item_id}
```

### Custom HTTP Method

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.api_route("/items/{item_id}", methods=["GET", "HEAD"])
async def get_item(item_id: int, request: Request):
    return {"item_id": item_id, "method": request.method}
```

---

## Automatic Documentation

### Swagger UI (/docs)

Navigate to `http://localhost:8000/docs` in your browser. You'll see an interactive UI where you can:

1. See all endpoints organized by tags
2. View request/response schemas
3. Execute requests directly from the browser
4. View example values for all fields

```python
app = FastAPI(
    title="My Awesome API",
    description="This API does amazing things",
    version="2.0.0",
    terms_of_service="https://example.com/terms",
    contact={
        "name": "API Support",
        "url": "https://example.com/support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",         # Default: /docs
    redoc_url="/redoc",       # Default: /redoc
    openapi_url="/openapi.json",  # Default: /openapi.json
)
```

### ReDoc (/redoc)

Navigate to `http://localhost:8000/redoc` for an alternative documentation style. ReDoc provides:

- A three-panel layout (navigation, documentation, examples)
- Better readability for complex APIs
- Print-friendly format

### OpenAPI Schema

The raw OpenAPI schema is available at `http://localhost:8000/openapi.json`:

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "My Awesome API",
    "version": "2.0.0"
  },
  "paths": {
    "/items/{item_id}": {
      "get": {
        "summary": "Get an item",
        "parameters": [
          {
            "name": "item_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "integer"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "item_id": {
                      "type": "integer"
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### Using Tags for Organization

```python
@app.get("/users/", tags=["users"])
async def list_users():
    return []

@app.post("/users/", tags=["users"])
async def create_user():
    return {}

@app.get("/items/", tags=["items"])
async def list_items():
    return []

@app.get("/health/", tags=["monitoring"])
async def health_check():
    return {"status": "ok"}
```

This groups endpoints in the docs UI under "users", "items", and "monitoring" sections.

### Disabling Documentation

```python
# Disable Swagger UI
app = FastAPI(docs_url=None)

# Disable ReDoc
app = FastAPI(redoc_url=None)

# Disable both
app = FastAPI(docs_url=None, redoc_url=None)

# Custom docs URL
app = FastAPI(docs_url="/swagger", redoc_url="/api-docs")
```

---

## Request/Response Flow

### Complete Request Lifecycle

```
1. Client sends HTTP request
       ↓
2. Uvicorn (ASGI server) receives the raw bytes
       ↓
3. ASGI converts to scope/receive/send
       ↓
4. Starlette middleware processes request:
   - CORS middleware
   - Trusted host middleware
   - Other custom middleware
       ↓
5. Starlette routes the request:
   - Matches URL path to a route
   - Extracts path parameters
       ↓
6. FastAPI processes the request:
   - Validates path parameters
   - Validates query parameters
   - Validates request body (if any)
   - Resolves dependencies
       ↓
7. Your path operation function runs
       ↓
8. FastAPI processes the response:
   - Validates response against response_model
   - Serializes to JSON
   - Sets appropriate headers
       ↓
9. Starlette formats the HTTP response
       ↓
10. Uvicorn sends the response to the client
```

### Middleware Processing

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### Request Object

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
        "client": {"host": request.client.host, "port": request.client.port},
    }
```

---

## Status Codes

### Setting Status Codes

```python
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

# Method 1: In the decorator
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

# Method 2: Return a JSONResponse with status code
@app.post("/items-alt/")
async def create_item_alt(item: Item):
    return JSONResponse(
        content={"id": 1, **item.model_dump()},
        status_code=status.HTTP_201_CREATED,
    )

# Method 3: Raise an exception with status code
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id == 0:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return {"item_id": item_id}
```

---

## JSON Responses

### Returning Dictionaries and Lists

```python
@app.get("/dict/")
async def return_dict():
    return {"name": "John", "age": 30}

@app.get("/list/")
async def return_list():
    return [{"name": "John"}, {"name": "Jane"}]

@app.get("/nested/")
async def return_nested():
    return {
        "users": [
            {"name": "John", "address": {"city": "NYC"}},
            {"name": "Jane", "address": {"city": "LA"}},
        ]
    }
```

### Returning Pydantic Models

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

@app.get("/user/", response_model=User)
async def get_user():
    return User(id=1, name="John", email="john@example.com")
```

### Response Headers

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/custom-headers/")
async def custom_headers():
    return JSONResponse(
        content={"message": "Hello"},
        headers={
            "X-Custom-Header": "custom-value",
            "X-Request-Id": "12345",
        },
    )
```

---

## Testing with curl/httpie

### curl Examples

```bash
# GET request
curl http://localhost:8000/

# GET with path parameter
curl http://localhost:8000/items/42

# GET with query parameters
curl http://localhost:8000/search/?q=hello&page=2

# POST with JSON body
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99}'

# PUT with JSON body
curl -X PUT http://localhost:8000/items/42 \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop Pro", "price": 1299.99}'

# DELETE request
curl -X DELETE http://localhost:8000/items/42

# Verbose output (see headers)
curl -v http://localhost:8000/

# Pretty print JSON
curl http://localhost:8000/ | python -m json.tool
```

### httpie Examples

httpie is a user-friendly HTTP client:

```bash
# Install httpie
pip install httpie

# GET request
http GET :8000/

# GET with path parameter
http GET :8000/items/42

# GET with query parameters
http GET :8000/search/ q=hello page==2

# POST with JSON body
http POST :8000/items/ name=Laptop price:=999.99

# PUT with JSON body
http PUT :8000/items/42 name="Laptop Pro" price:=1299.99

# DELETE request
http DELETE :8000/items/42

# With authentication
http GET :8000/protected/ Authorization:"Bearer token123"

# Form data
http --form POST :8000/upload/ file@/path/to/file.pdf

# Download file
http --download GET :8000/files/document.pdf
```

> **Note:** In httpie, `:=` sends raw JSON types (numbers, booleans), `==` sends query parameters, and `:` sends string values.

---

## Testing in Swagger UI

### Step-by-Step

1. **Navigate** to `http://localhost:8000/docs`
2. **Expand** an endpoint by clicking on it
3. **Click** "Try it out"
4. **Fill in** the request parameters/body
5. **Click** "Execute"
6. **View** the response

### What You Can Test

- **Path parameters**: Enter values in the path parameter fields
- **Query parameters**: Fill in query parameter forms
- **Request bodies**: Edit the JSON body directly in the textarea
- **File uploads**: Select files from your computer
- **Headers**: Add custom headers (Authorization, etc.)

### Swagger UI Features

- **Authorize**: Add authentication tokens (JWT, API keys)
- **Model**: View the schema definition for request/response models
- **Response**: See status code, headers, and body
- **Curl**: Copy the equivalent curl command
- **Download**: Download the OpenAPI schema

---

## Interview Questions

### Q1: What happens when you return a dict from a FastAPI endpoint?

**Answer:** FastAPI automatically serializes the dict to JSON, sets the `Content-Type: application/json` header, and wraps it in an HTTP response. It also validates the response against the `response_model` if specified.

### Q2: What is the difference between `async def` and `def` in FastAPI?

**Answer:** `async def` creates an async path operation that runs directly on the event loop, ideal for I/O-bound operations with `await`. `def` (sync) is run in a threadpool by FastAPI, so it doesn't block the event loop. Use `async def` when you have async operations; use `def` for CPU-bound or synchronous library code.

### Q3: How do you disable the automatic docs?

**Answer:** Pass `docs_url=None` and/or `redoc_url=None` to the FastAPI constructor:

```python
app = FastAPI(docs_url=None, redoc_url=None)
```

This is useful in production to hide your API schema from unauthorized users.

### Q4: Can you have multiple HTTP methods on the same path?

**Answer:** Yes, as long as each method is unique for that path. FastAPI uses both the path and HTTP method to differentiate routes:

```python
@app.get("/items/{item_id}")
async def get_item(item_id: int): ...

@app.post("/items/{item_id}")
async def create_item(item_id: int): ...
```

### Q5: What status code does FastAPI use by default?

**Answer:** FastAPI uses `200 OK` by default for successful responses. For POST operations, you typically set `status_code=201` explicitly. For DELETE operations that return no content, use `status_code=204`.

### Q6: How does FastAPI handle HEAD and OPTIONS requests automatically?

**Answer:** FastAPI automatically handles HEAD requests for GET endpoints (returns headers without body) and OPTIONS requests (including CORS preflight). You don't need to manually define these.
