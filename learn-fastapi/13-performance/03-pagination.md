# Pagination

## Table of Contents

1. [Introduction](#1-introduction)
2. [Offset-Based Pagination](#2-offset)
3. [Cursor-Based Pagination](#3-cursor)
4. [Keyset Pagination](#4-keyset)
5. [Page/Size Parameters](#5-page-size)
6. [Link Header Pagination](#6-link-header)
7. [Pagination with Total Count](#7-total-count)
8. [Infinite Scroll Patterns](#8-infinite-scroll)
9. [GraphQL-Style Cursor Pagination](#9-graphql-cursor)
10. [Performance Considerations](#10-performance)
11. [Best Practices](#11-best-practices)

---

## 1. Introduction <a name="1-introduction"></a>

Pagination is essential for APIs that return large datasets. It limits the amount
of data transferred per request, improving performance and reducing memory usage.

### Pagination Types

| Type | Use Case | Performance | Consistency |
|------|----------|-------------|-------------|
| Offset | Simple listing | Degrades with large offsets | May miss items |
| Cursor | Infinite scroll | Consistent | Consistent |
| Keyset | High performance | Best | Consistent |
| Page/Size | Simple UI | Degrades | May miss items |

---

## 2. Offset-Based Pagination <a name="2-offset"></a>

### Basic Implementation

```python
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_previous: bool

@app.get("/items/", response_model=PaginatedResponse[Item])
async def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(20, ge=1, le=100, description="Max items to return"),
    db: Session = Depends(get_db),
):
    # Get total count
    total = db.query(Item).count()

    # Get items with offset
    items = db.query(Item).offset(skip).limit(limit).all()

    return PaginatedResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit,
        has_next=skip + limit < total,
        has_previous=skip > 0,
    )
```

### Advanced Offset Pagination

```python
from pydantic import BaseModel
from typing import TypeVar, Generic, Optional
from fastapi import Query

T = TypeVar("T")

class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 20
    total: int = 0

    @property
    def has_next(self) -> bool:
        return self.skip + self.limit < self.total

    @property
    def has_previous(self) -> bool:
        return self.skip > 0

    @property
    def total_pages(self) -> int:
        return (self.total + self.limit - 1) // self.limit

    @property
    def current_page(self) -> int:
        return (self.skip // self.limit) + 1

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    pagination: PaginationParams

def paginate_query(
    query,
    skip: int = 0,
    limit: int = 20,
) -> tuple[list, PaginationParams]:
    """Generic pagination helper."""
    total = query.count()
    items = query.offset(skip).limit(limit).all()

    params = PaginationParams(
        skip=skip,
        limit=limit,
        total=total,
    )

    return items, params

@app.get("/items/", response_model=PaginatedResponse[Item])
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Item)
    items, params = paginate_query(query, skip, limit)

    return PaginatedResponse(items=items, pagination=params)
```

### Offset Pagination with Filters

```python
@app.get("/items/", response_model=PaginatedResponse[Item])
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    sort_by: str = Query("created_at", pattern=r'^(name|created_at|price)$'),
    order: str = Query("desc", pattern=r'^(asc|desc)$'),
    db: Session = Depends(get_db),
):
    query = db.query(Item)

    # Apply filters
    if category:
        query = query.filter(Item.category == category)
    if min_price is not None:
        query = query.filter(Item.price >= min_price)
    if max_price is not None:
        query = query.filter(Item.price <= max_price)

    # Apply sorting
    sort_column = getattr(Item, sort_by)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    items, params = paginate_query(query, skip, limit)
    return PaginatedResponse(items=items, pagination=params)
```

---

## 3. Cursor-Based Pagination <a name="3-cursor"></a>

### Basic Cursor Pagination

```python
import base64
import json
from typing import Optional
from pydantic import BaseModel

class CursorPagination(BaseModel):
    cursor: Optional[str] = None
    limit: int = 20
    has_next: bool = False
    next_cursor: Optional[str] = None

def encode_cursor(data: dict) -> str:
    """Encode cursor data to base64."""
    return base64.urlsafe_b64encode(
        json.dumps(data).encode()
    ).decode()

def decode_cursor(cursor: str) -> dict:
    """Decode base64 cursor to data."""
    return json.loads(
        base64.urlsafe_b64decode(cursor.encode()).decode()
    )

@app.get("/items/")
async def list_items(
    cursor: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Item)

    # Apply cursor filter
    if cursor:
        cursor_data = decode_cursor(cursor)
        query = query.filter(
            Item.id > cursor_data["last_id"],
            Item.created_at >= cursor_data["last_created_at"],
        )

    # Fetch one extra to check if there's a next page
    items = query.order_by(Item.id).limit(limit + 1).all()

    has_next = len(items) > limit
    if has_next:
        items = items[:limit]

    next_cursor = None
    if has_next and items:
        last_item = items[-1]
        next_cursor = encode_cursor({
            "last_id": last_item.id,
            "last_created_at": last_item.created_at.isoformat(),
        })

    return {
        "items": [item.dict() for item in items],
        "pagination": {
            "cursor": cursor,
            "limit": limit,
            "has_next": has_next,
            "next_cursor": next_cursor,
        },
    }
```

### Cursor with Composite Keys

```python
def encode_composite_cursor(id: int, created_at: str, name: str) -> str:
    """Encode composite cursor."""
    data = {"id": id, "created_at": created_at, "name": name}
    return base64.urlsafe_b64encode(json.dumps(data).encode()).decode()

@app.get("/items/")
async def list_items(
    cursor: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Item)

    if cursor:
        cursor_data = decode_cursor(cursor)
        # Composite cursor: greater than OR (equal AND greater)
        query = query.filter(
            db.or_(
                Item.created_at > cursor_data["created_at"],
                db.and_(
                    Item.created_at == cursor_data["created_at"],
                    Item.id > cursor_data["id"],
                ),
            )
        )

    items = query.order_by(
        Item.created_at, Item.id
    ).limit(limit + 1).all()

    has_next = len(items) > limit
    items = items[:limit]

    next_cursor = None
    if has_next and items:
        last = items[-1]
        next_cursor = encode_composite_cursor(
            last.id,
            last.created_at.isoformat(),
            last.name,
        )

    return {
        "items": items,
        "pagination": {"has_next": has_next, "next_cursor": next_cursor},
    }
```

---

## 4. Keyset Pagination <a name="4-keyset"></a>

Keyset pagination (also known as "seek method") uses the last seen value as the
starting point for the next page.

```python
from typing import Optional
from datetime import datetime

@app.get("/items/")
async def list_items(
    last_id: Optional[int] = Query(None, description="Last seen item ID"),
    last_created_at: Optional[datetime] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Item)

    if last_id is not None and last_created_at is not None:
        # Keyset filter: items after the last seen item
        query = query.filter(
            db.or_(
                Item.created_at > last_created_at,
                db.and_(
                    Item.created_at == last_created_at,
                    Item.id > last_id,
                ),
            )
        )

    # Fetch one extra to detect end of data
    items = query.order_by(
        Item.created_at, Item.id
    ).limit(limit + 1).all()

    has_more = len(items) > limit
    items = items[:limit]

    # Build next page parameters
    next_params = {}
    if has_more and items:
        last = items[-1]
        next_params = {
            "last_id": last.id,
            "last_created_at": last.created_at.isoformat(),
        }

    return {
        "items": [item.dict() for item in items],
        "pagination": {
            "has_more": has_more,
            "next_params": next_params,
        },
    }
```

### Keyset with Sorting

```python
@app.get("/items/")
async def list_items(
    last_price: Optional[float] = Query(None),
    last_id: Optional[int] = Query(None),
    sort_by: str = Query("price", pattern=r'^(price|created_at|name)$'),
    order: str = Query("asc", pattern=r'^(asc|desc)$'),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Item)
    sort_col = getattr(Item, sort_by)

    if last_price is not None and last_id is not None:
        if order == "asc":
            query = query.filter(
                db.or_(
                    sort_col > last_price,
                    db.and_(sort_col == last_price, Item.id > last_id),
                )
            )
        else:
            query = query.filter(
                db.or_(
                    sort_col < last_price,
                    db.and_(sort_col == last_price, Item.id < last_id),
                )
            )

    if order == "asc":
        query = query.order_by(sort_col, Item.id)
    else:
        query = query.order_by(sort_col.desc(), Item.id.desc())

    items = query.limit(limit + 1).all()
    has_more = len(items) > limit
    items = items[:limit]

    return {
        "items": items,
        "pagination": {"has_more": has_more},
    }
```

---

## 5. Page/Size Parameters <a name="5-page-size"></a>

### Simple Page/Size

```python
from fastapi import FastAPI, Query
from pydantic import BaseModel

class PageResponse(BaseModel):
    items: list
    page: int
    size: int
    total: int
    pages: int

@app.get("/items/", response_model=PageResponse)
async def list_items(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db),
):
    total = db.query(Item).count()
    pages = (total + size - 1) // size

    offset = (page - 1) * size
    items = db.query(Item).offset(offset).limit(size).all()

    return PageResponse(
        items=items,
        page=page,
        size=size,
        total=total,
        pages=pages,
    )
```

### Page/Size with Links

```python
from fastapi.responses import JSONResponse

@app.get("/items/")
async def list_items(
    request: Request,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total = db.query(Item).count()
    pages = (total + size - 1) // size
    offset = (page - 1) * size

    items = db.query(Item).offset(offset).limit(size).all()

    # Build response with links
    base_url = str(request.base_url)

    response = {
        "items": items,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "pages": pages,
        },
        "links": {
            "self": f"{base_url}items/?page={page}&size={size}",
            "first": f"{base_url}items/?page=1&size={size}",
            "last": f"{base_url}items/?page={pages}&size={size}",
            "next": f"{base_url}items/?page={page+1}&size={size}" if page < pages else None,
            "prev": f"{base_url}items/?page={page-1}&size={size}" if page > 1 else None,
        },
    }

    return response
```

---

## 6. Link Header Pagination <a name="6-link-header"></a>

```python
from fastapi import Response

def create_link_header(base_url: str, page: int, pages: int, size: int) -> str:
    """Create Link header for pagination."""
    links = []

    # First page
    links.append(f'<{base_url}?page=1&size={size}>; rel="first"')

    # Previous page
    if page > 1:
        links.append(f'<{base_url}?page={page-1}&size={size}>; rel="prev"')

    # Next page
    if page < pages:
        links.append(f'<{base_url}?page={page+1}&size={size}>; rel="next"')

    # Last page
    links.append(f'<{base_url}?page={pages}&size={size}>; rel="last"')

    return ", ".join(links)

@app.get("/items/")
async def list_items(
    request: Request,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total = db.query(Item).count()
    pages = (total + size - 1) // size
    offset = (page - 1) * size

    items = db.query(Item).offset(offset).limit(size).all()

    base_url = str(request.base_url).rstrip("/")
    link_header = create_link_header(f"{base_url}/items", page, pages, size)

    response = JSONResponse(content={"items": items})
    response.headers["Link"] = link_header
    response.headers["X-Total-Count"] = str(total)
    response.headers["X-Page-Count"] = str(pages)

    return response
```

---

## 7. Pagination with Total Count <a name="7-total-count"></a>

### Conditional Total Count

```python
@app.get("/items/")
async def list_items(
    include_total: bool = Query(True, description="Include total count"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Item)

    # Optionally skip expensive count query
    total = None
    if include_total:
        total = db.query(func.count(Item.id)).scalar()

    items = query.offset(skip).limit(limit).all()

    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
    }
```

### Approximate Count for Large Tables

```python
def get_approximate_count(db, model) -> int:
    """Get approximate count without COUNT query."""
    # PostgreSQL: Use pg_class for approximate count
    result = db.execute(text(
        """
        SELECT reltuples::bigint AS estimate
        FROM pg_class
        WHERE relname = :table_name
        """
    ), {"table_name": model.__tablename__})

    row = result.fetchone()
    return max(0, row[0]) if row else 0

@app.get("/items/")
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    # Fast approximate count
    total = get_approximate_count(db, Item)

    items = db.query(Item).offset(skip).limit(limit).all()

    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
    }
```

---

## 8. Infinite Scroll Patterns <a name="8-infinite-scroll"></a>

### Backend Support for Infinite Scroll

```python
@app.get("/items/")
async def list_items(
    cursor: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    query = db.query(Item)

    if cursor:
        cursor_data = decode_cursor(cursor)
        query = query.filter(
            db.or_(
                Item.created_at < cursor_data["created_at"],
                db.and_(
                    Item.created_at == cursor_data["created_at"],
                    Item.id < cursor_data["id"],
                ),
            )
        )

    # Order descending for infinite scroll
    items = query.order_by(
        Item.created_at.desc(),
        Item.id.desc(),
    ).limit(limit + 1).all()

    has_more = len(items) > limit
    items = items[:limit]

    next_cursor = None
    if has_more and items:
        last = items[-1]
        next_cursor = encode_cursor({
            "created_at": last.created_at.isoformat(),
            "id": last.id,
        })

    return {
        "items": [item.dict() for item in items],
        "next_cursor": next_cursor,
        "has_more": has_more,
    }
```

---

## 9. GraphQL-Style Cursor Pagination <a name="9-graphql-cursor"></a>

### Relay-Style Connections

```python
from typing import Optional, Any
from pydantic import BaseModel

class PageInfo(BaseModel):
    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str]
    end_cursor: Optional[str]

class Edge(BaseModel):
    node: Any
    cursor: str

class Connection(BaseModel):
    edges: list[Edge]
    page_info: PageInfo
    total_count: Optional[int]

def encode_global_cursor(data: dict) -> str:
    """Encode cursor with type prefix."""
    return base64.urlsafe_b64encode(
        json.dumps({"type": "item", **data}).encode()
    ).decode()

@app.get("/items/", response_model=Connection)
async def list_items(
    first: Optional[int] = Query(None, ge=1, le=100),
    after: Optional[str] = Query(None),
    last: Optional[int] = Query(None, ge=1, le=100),
    before: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Item)

    # Forward pagination
    if after:
        cursor_data = json.loads(base64.urlsafe_b64decode(after.encode()))
        query = query.filter(Item.id > cursor_data["id"])

    if first:
        items = query.order_by(Item.id).limit(first + 1).all()
        has_next = len(items) > first
        items = items[:first]
    elif last:
        items = query.order_by(Item.id.desc()).limit(last + 1).all()
        has_previous = len(items) > last
        items = items[:last]
        items.reverse()
        has_next = False
    else:
        items = query.order_by(Item.id).limit(20).all()
        has_next = False

    edges = [
        Edge(
            node=item.dict(),
            cursor=encode_global_cursor({"id": item.id}),
        )
        for item in items
    ]

    page_info = PageInfo(
        has_next_page=has_next if first else False,
        has_previous_page=False,
        start_cursor=edges[0].cursor if edges else None,
        end_cursor=edges[-1].cursor if edges else None,
    )

    total_count = db.query(func.count(Item.id)).scalar()

    return Connection(
        edges=edges,
        page_info=page_info,
        total_count=total_count,
    )
```

---

## 10. Performance Considerations <a name="10-performance"></a>

### Efficient Offset Pagination

```python
# BAD: Slow for large offsets
items = db.query(Item).offset(100000).limit(20).all()
# This scans 100,000 rows!

# GOOD: Use keyset for large datasets
items = db.query(Item).filter(
    Item.id > last_id
).order_by(Item.id).limit(20).all()
# This uses the index!
```

### Index for Pagination

```python
# Create index for pagination performance
from sqlalchemy import Index

# For offset pagination
Index("ix_items_created_at", Item.created_at)

# For cursor/keyset pagination
Index("ix_items_cursor", Item.created_at, Item.id)
```

### Cache Total Count

```python
from datetime import datetime, timedelta

async def get_cached_total(db, model) -> int:
    """Cache total count to avoid expensive COUNT queries."""
    cache_key = f"total:{model.__tablename__}"
    cached = await redis.get(cache_key)

    if cached:
        return int(cached)

    total = db.query(func.count(model.id)).scalar()
    await redis.setex(cache_key, 300, str(total))  # Cache for 5 minutes
    return total
```

---

## 11. Best Practices <a name="11-best-practices"></a>

### 1. Choose the Right Pagination Type

```python
# Simple UI with page numbers → Offset
# Infinite scroll → Cursor
# Large datasets → Keyset
# API consumers → Link headers
```

### 2. Set Maximum Page Size

```python
@app.get("/items/")
async def list_items(
    limit: int = Query(20, ge=1, le=100),  # Enforce max
):
    pass
```

### 3. Use Consistent Response Format

```python
class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    pagination: PaginationMeta
    links: Optional[dict] = None
```

### 4. Document Pagination Behavior

```python
@app.get("/items/")
async def list_items(
    """
    List items with pagination.

    Pagination types:
    - offset: Use skip and limit parameters
    - cursor: Use cursor parameter for infinite scroll
    - keyset: Use last_id parameter for efficient large dataset pagination
    """
):
    pass
```

### 5. Handle Edge Cases

```python
@app.get("/items/")
async def list_items(skip: int = 0, limit: int = 20):
    total = db.query(Item).count()

    # Handle empty results
    if total == 0:
        return {"items": [], "total": 0}

    # Handle skip beyond total
    skip = min(skip, total)

    items = db.query(Item).offset(skip).limit(limit).all()
    return {"items": items, "total": total}
```

---

## Summary

| Type | Best For | Pros | Cons |
|------|----------|------|------|
| Offset | Page numbers | Simple, familiar | Slow for large offsets |
| Cursor | Infinite scroll | Consistent, fast | More complex |
| Keyset | Large datasets | Fastest, uses index | Requires ordered column |
| Page/Size | Simple UI | Easy to understand | Same as offset |

### Quick Implementation

```python
from fastapi import Query
from typing import Optional

@app.get("/items/")
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total = db.query(Item).count()
    items = db.query(Item).offset(skip).limit(limit).all()
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_next": skip + limit < total,
    }
```

### Key Rules

1. Always set a maximum page size
2. Use keyset/cursor for large datasets
3. Cache total counts
4. Index columns used for pagination
5. Handle edge cases (empty, beyond total)
6. Use consistent response format
7. Document pagination behavior
