# 05 - Query Parameters

## Table of Contents

1. [Query Parameter Syntax](#query-parameter-syntax)
2. [Optional Parameters](#optional-parameters)
3. [Query Parameter Validation](#query-parameter-validation)
4. [Alias Parameters](#alias-parameters)
5. [Deprecated Parameters](#deprecated-parameters)
6. [List Query Parameters](#list-query-parameters)
7. [Boolean Query Parameters](#boolean-query-parameters)
8. [Query Parameter Constraints](#query-parameter-constraints)
9. [Encoding Issues](#encoding-issues)
10. [Extra Query Parameters Behavior](#extra-query-parameters-behavior)
11. [Interview Questions](#interview-questions)

---

## Query Parameter Syntax

Query parameters are the key-value pairs after `?` in a URL:

```
https://example.com/items?skip=0&limit=10&category=electronics
         ↑ path       ↑ query parameters (key=value pairs)
```

In FastAPI, query parameters are function parameters that are **not** part of the path template:

```python
from fastapi import FastAPI

app = FastAPI()

# item_id is a PATH parameter (in the path template)
# skip and limit are QUERY parameters (not in the path template)
@app.get("/items/{item_id}")
async def read_items(item_id: int, skip: int = 0, limit: int = 10):
    return {
        "item_id": item_id,
        "skip": skip,
        "limit": limit,
    }

# GET /items/42?skip=0&limit=20
# → {"item_id": 42, "skip": 0, "limit": 20}

# GET /items/42
# → {"item_id": 42, "skip": 0, "limit": 10}  (defaults used)
```

### How FastAPI Determines Parameter Type

```python
@app.get("/example/")
async def example(
    path_param: int,           # In path template? → No, so it's query
    query_param: str,          # Has a default? → No required query
    optional_param: str = "default",  # Has default → Optional query
):
    pass

# The key rules:
# 1. If the parameter name appears in the path template → path parameter
# 2. If the parameter has a default value → optional query parameter
# 3. If the parameter has no default and isn't in path → required query parameter
# 4. If the type is Pydantic model → request body
```

### Multiple Query Parameters

```python
@app.get("/search/")
async def search(
    q: str,                     # Required query param
    category: str = "all",      # Optional with default
    min_price: float = 0.0,     # Optional with default
    max_price: float = 1000.0,  # Optional with default
    sort_by: str = "relevance", # Optional with default
    page: int = 1,              # Optional with default
    per_page: int = 20,         # Optional with default
):
    return {
        "q": q,
        "category": category,
        "price_range": [min_price, max_price],
        "sort_by": sort_by,
        "page": page,
        "per_page": per_page,
    }
```

---

## Optional Parameters

### Using None Default

```python
from typing import Optional

@app.get("/items/")
async def list_items(q: Optional[str] = None):
    if q is None:
        return {"items": ["item1", "item2", "item3"]}
    return {"items": [item for item in ["item1", "item2", "item3"] if q in item]}

# GET /items/          → {"items": ["item1", "item2", "item3"]}
# GET /items/?q=item1  → {"items": ["item1"]}
```

### Python 3.10+ Syntax

```python
@app.get("/items/")
async def list_items(q: str | None = None):
    if q is None:
        return {"items": ["item1", "item2"]}
    return {"items": [item for item in ["item1", "item2"] if q in item]}
```

### Optional Parameters with None vs Empty String

```python
@app.get("/search/")
async def search(q: str | None = None):
    # GET /search/      → q is None
    # GET /search/?q=   → q is "" (empty string)
    # GET /search/?q=hi → q is "hi"
    return {"q": q}
```

### Multiple Optional Parameters

```python
@app.get("/products/")
async def list_products(
    category: str | None = None,
    brand: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    in_stock: bool | None = None,
):
    filters = {}
    if category is not None:
        filters["category"] = category
    if brand is not None:
        filters["brand"] = brand
    if min_price is not None:
        filters["min_price"] = min_price
    if max_price is not None:
        filters["max_price"] = max_price
    if in_stock is not None:
        filters["in_stock"] = in_stock
    
    return {"filters": filters}

# GET /products/                           → all filters empty
# GET /products/?category=electronics      → category filter only
# GET /products/?min_price=100&max_price=500 → price range only
```

---

## Query Parameter Validation

### Using Query() Function

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def list_items(
    q: str = Query(
        ...,                     # Required (no default)
        min_length=3,           # Minimum length
        max_length=50,          # Maximum length
        pattern=r"^[a-zA-Z0-9 ]+$",  # Regex pattern
        title="Search Query",   # Title in docs
        description="Search items by name or description",
        alias="search-query",   # URL alias
        deprecated=False,       # Mark as deprecated
        include_in_schema=True, # Include in OpenAPI
        examples=[              # Examples in docs
            "laptop",
            "wireless keyboard",
        ],
    ),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max items to return"),
):
    return {"q": q, "skip": skip, "limit": limit}
```

### Required vs Optional Query Parameters

```python
# Required (no default value)
@app.get("/search/")
async def search(q: str):
    return {"q": q}

# Using Query with ellipsis (required)
@app.get("/search2/")
async def search2(q: str = Query(...)):
    return {"q": q}

# Optional (has default value)
@app.get("/browse/")
async def browse(category: str = "all"):
    return {"category": category}

# Optional with None
@app.get("/filter/")
async def filter_items(q: str | None = None):
    return {"q": q}

# Using Query with None default (optional)
@app.get("/filter2/")
async def filter_items2(q: str | None = Query(None)):
    return {"q": q}
```

---

## Alias Parameters

Aliases allow you to use different parameter names in the URL than in your code:

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def list_items(
    search_query: str = Query(
        ..., 
        alias="search-query",  # URL uses "search-query"
        description="The search query to filter items"
    ),
    page_number: int = Query(
        1, 
        alias="page-number",   # URL uses "page-number"
        ge=1
    ),
):
    return {
        "search_query": search_query,
        "page_number": page_number,
    }

# URL: /items/?search-query=laptop&page-number=2
# Note: hyphens in the URL are converted to underscores in Python
```

### Alias Generator

```python
from pydantic import BaseModel, Field, AliasGenerator

class FilterParams(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            to_alias=str,           # Python name → URL name
        ),
        populate_by_name=True,     # Allow both name and alias
    )
    
    max_price: float = Field(..., alias="max-price")
    min_price: float = Field(..., alias="min-price")
    category: str | None = None

@app.get("/products/")
async def list_products(filters: FilterParams = Depends()):
    return filters.model_dump(by_alias=True)
```

---

## Deprecated Parameters

Mark query parameters as deprecated to guide API consumers:

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def list_items(
    q: str,
    version: int = Query(
        1,
        deprecated=True,  # Marked as deprecated in docs
        description="API version to use. Use v2 endpoint instead."
    ),
    format: str = Query(
        "json",
        deprecated=True,  # Deprecated
        description="Response format. Always returns JSON now."
    ),
):
    """
    List items with optional filtering.
    
    - **q**: Search query (required)
    - **version**: Deprecated, use `/api/v2/items` instead
    - **format**: Deprecated, response is always JSON
    """
    return {"items": [], "version": version}

# In Swagger UI, deprecated params appear with a strikethrough
```

### Deprecating Entire Endpoints

```python
@app.get("/items/", deprecated=True)
async def list_items_old():
    """Deprecated: Use /api/v2/items/ instead."""
    return []

@app.get("/api/v2/items/")
async def list_items_new():
    """List items with improved filtering."""
    return []
```

---

## List Query Parameters

### Repeated Query Parameters

When a query parameter appears multiple times, you can collect them as a list:

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def list_items(
    tags: list[str] = Query(
        ...,
        description="Filter by tags (repeat for multiple)"
    ),
):
    return {"tags": tags}

# GET /items/?tags=python&tags=fastapi&tags=async
# → {"tags": ["python", "fastapi", "async"]}
```

### Optional List Query Parameters

```python
@app.get("/filter/")
async def filter_items(
    tags: list[str] = Query(
        default=[],             # Default to empty list
        description="Filter by tags"
    ),
    categories: list[str] | None = Query(
        None,                   # Default to None
        description="Filter by categories"
    ),
):
    return {
        "tags": tags,
        "categories": categories,
    }

# GET /filter/                          → {"tags": [], "categories": null}
# GET /filter/?tags=a&tags=b            → {"tags": ["a", "b"], "categories": null}
# GET /filter/?categories=x&categories=y → {"tags": [], "categories": ["x", "y"]}
```

### List with Validation

```python
@app.get("/search/")
async def search(
    q: str,
    sort_by: list[str] = Query(
        default=["relevance"],
        min_length=1,           # At least one sort field
        max_length=3,           # Max 3 sort fields
        description="Sort fields (max 3)"
    ),
    exclude_ids: list[int] = Query(
        default=[],
        ge=1,                   # Each ID must be >= 1
        description="IDs to exclude"
    ),
):
    return {"sort_by": sort_by, "exclude_ids": exclude_ids}

# GET /search/?q=laptop&sort_by=price&sort_by=rating&exclude_ids=1&exclude_ids=5
```

### Using Annotated (Python 3.10+)

```python
from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def list_items(
    tags: Annotated[list[str], Query(description="Filter by tags")] = [],
    q: Annotated[str | None, Query(min_length=3, max_length=50)] = None,
):
    return {"tags": tags, "q": q}
```

---

## Boolean Query Parameters

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def list_items(
    is_active: bool = Query(True, description="Filter active items"),
    is_featured: bool = Query(False, description="Show only featured"),
    include_deleted: bool = Query(False, description="Include deleted items"),
):
    return {
        "is_active": is_active,
        "is_featured": is_featured,
        "include_deleted": include_deleted,
    }

# GET /items/?is_active=true              → is_active=True
# GET /items/?is_active=false             → is_active=False
# GET /items/?is_active=1                 → is_active=True
# GET /items/?is_active=0                 → is_active=False
# GET /items/                             → is_active=True (default)
# GET /items/?is_active=true&is_active=false  → Error: too many values
```

### Boolean Conversion

| Query Value | Python Value |
|-------------|--------------|
| `true`, `True`, `1`, `yes` | `True` |
| `false`, `False`, `0`, `no` | `False` |
| (not provided) | Default value |

### Optional Boolean

```python
@app.get("/items/")
async def list_items(
    is_active: bool | None = Query(None, description="Filter by status (null = all)")
):
    if is_active is None:
        return {"filter": "all items"}
    return {"filter": "active" if is_active else "inactive"}

# GET /items/              → filter all items
# GET /items/?is_active=true  → filter active only
# GET /items/?is_active=false → filter inactive only
```

---

## Query Parameter Constraints

### String Constraints

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/search/")
async def search(
    q: str = Query(
        ...,
        min_length=1,           # At least 1 character
        max_length=200,         # Max 200 characters
        pattern=r"^[a-zA-Z0-9 ]+$",  # Alphanumeric and spaces only
    )
):
    return {"q": q}
```

### Numeric Constraints

```python
@app.get("/pagination/")
async def paginate(
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    min_price: float = Query(0.0, ge=0.0, description="Minimum price"),
    max_price: float = Query(1000.0, gt=0.0, le=10000.0, description="Maximum price"),
    discount: float = Query(0.0, ge=0.0, le=1.0, description="Discount percentage (0-1)"),
):
    return {
        "page": page,
        "per_page": per_page,
        "price_range": [min_price, max_price],
        "discount": discount,
    }
```

### Complete Constraint Example

```python
from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()

@app.get("/advanced-search/")
async def advanced_search(
    # String constraints
    q: Annotated[str, Query(min_length=2, max_length=100)] = "",
    
    # Numeric constraints
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=100)] = 20,
    min_price: Annotated[float, Query(ge=0.0)] = 0.0,
    max_price: Annotated[float, Query(gt=0.0)] = 10000.0,
    
    # List constraints
    tags: Annotated[list[str], Query(max_length=10)] = [],
    
    # Pattern matching
    sku: Annotated[str | None, Query(pattern=r"^[A-Z]{2,4}-\d{4,8}$")] = None,
):
    return {
        "q": q,
        "page": page,
        "per_page": per_page,
        "price_range": [min_price, max_price],
        "tags": tags,
        "sku": sku,
    }
```

---

## Encoding Issues

### URL Encoding

Special characters in query parameters must be URL-encoded:

```
Space → %20 or +
@     → %40
&     → %26
=     → %3D
/     → %2F
```

```python
@app.get("/search/")
async def search(q: str):
    return {"q": q}

# GET /search/?q=hello%20world   → q="hello world"
# GET /search/?q=hello+world     → q="hello world"
# GET /search/?q=hello%40world   → q="hello@world"
```

### Handling Special Characters

```python
from fastapi import FastAPI, Query
from urllib.parse import unquote

app = FastAPI()

@app.get("/search/")
async def search(q: str = Query(...)):
    # FastAPI automatically decodes URL-encoded values
    return {"q": q, "decoded": unquote(q)}

# The client should encode:
# curl "http://localhost:8000/search/?q=hello%20world"
# FastAPI receives: q="hello world"
```

### Query Parameters with Special Characters

```python
@app.get("/filter/")
async def filter_items(
    q: str = Query(..., description="Search query"),
    sort: str = Query("relevance", description="Sort order"),
):
    return {"q": q, "sort": sort}

# Correct URL encoding:
# /filter/?q=python%20tutorial&sort=price%20asc
# FastAPI decodes to: q="python tutorial", sort="price asc"
```

---

## Extra Query Parameters Behavior

### Default Behavior: Reject Extra Parameters

By default, FastAPI **rejects** extra query parameters with a 422 error:

```python
@app.get("/items/")
async def list_items(q: str, limit: int = 10):
    return {"q": q, "limit": limit}

# GET /items/?q=test&limit=5&extra=hello
# → 422 Error: "Unexpected query parameter: extra"
```

### Allow Extra Query Parameters with model_config

```python
from pydantic import BaseModel, ConfigDict

class FilterParams(BaseModel):
    model_config = ConfigDict(extra="allow")  # or "ignore"
    
    q: str
    limit: int = 10

@app.get("/items/")
async def list_items(params: FilterParams = Depends()):
    return params.model_dump()

# GET /items/?q=test&limit=5&extra=hello
# → {"q": "test", "limit": 5, "extra": "hello"}
```

### Extra Parameters with Depends

```python
from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel

app = FastAPI()

class PaginationParams(BaseModel):
    page: int = 1
    per_page: int = 20

async def get_pagination(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
) -> PaginationParams:
    return PaginationParams(page=page, per_page=per_page)

@app.get("/items/")
async def list_items(pagination: PaginationParams = Depends(get_pagination)):
    return {
        "page": pagination.page,
        "per_page": pagination.per_page,
    }
```

---

## Interview Questions

### Q1: How does FastAPI determine if a parameter is a path parameter or query parameter?

**Answer:** If the parameter name appears in the path template (e.g., `{item_id}`), it's a path parameter. If it doesn't appear in the path template, it's a query parameter. Path parameters are always required; query parameters can be optional with default values.

### Q2: What happens when you send extra query parameters to a FastAPI endpoint?

**Answer:** By default, FastAPI rejects extra query parameters with a 422 Unprocessable Entity error. This is intentional for type safety. To allow extra parameters, use `model_config = ConfigDict(extra="allow")` on a Pydantic model.

### Q3: How do you make a query parameter optional?

**Answer:** Give it a default value of `None`:

```python
@app.get("/items/")
async def list_items(q: str | None = None):
    return {"q": q}
```

When the parameter is not provided, `q` will be `None`.

### Q4: Can query parameters be lists?

**Answer:** Yes. Declare the type as `list[str]` (or `list[int]`, etc.) and repeat the parameter in the URL:

```python
@app.get("/items/")
async def list_items(tags: list[str] = Query(default=[])):
    return {"tags": tags}

# URL: /items/?tags=a&tags=b&tags=c
# Result: {"tags": ["a", "b", "c"]}
```

### Q5: How do you validate query parameters?

**Answer:** Use `Query()` with constraints:

```python
@app.get("/search/")
async def search(
    q: str = Query(..., min_length=3, max_length=50),
    page: int = Query(1, ge=1),
):
    return {"q": q, "page": page}
```

Invalid values return a 422 error with detailed validation messages.

### Q6: What is a query parameter alias and when would you use one?

**Answer:** An alias lets you use a different name in the URL than in your Python code:

```python
@app.get("/items/")
async def list_items(
    search_query: str = Query(..., alias="search-query")
):
    return {"search_query": search_query}
# URL: /items/?search-query=laptop
```

Use aliases when the URL convention uses hyphens but Python variables use underscores.

### Q7: How do you handle boolean query parameters?

**Answer:** Declare the parameter as `bool`. FastAPI converts string values: `true`/`True`/`1`/`yes` → `True`, `false`/`False`/`0`/`no` → `False`. Use `bool | None` for optional booleans where `None` means "not specified."

### Q8: What's the difference between `q: str = None` and `q: str = Query(None)`?

**Answer:** Functionally they're identical - both make `q` an optional query parameter with a `None` default. `Query(None)` gives you more control (validation, alias, description, etc.). Use `Query()` when you need validation or documentation features.
