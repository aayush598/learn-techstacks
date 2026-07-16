# HATEOAS — Hypermedia As The Engine Of Application State

## Table of Contents
1. [What is HATEOAS](#what-is)
2. [Link Relations](#link-relations)
3. [HAL Format](#hal)
4. [Building HATEOAS with FastAPI](#fastapi)
5. [JSON:API Spec](#jsonapi)
6. [Link Header](#link-header)
7. [Discoverability](#discoverability)

---

## What is HATEOAS <a name="what-is"></a>

HATEOAS is the highest level of REST maturity. Clients interact with the API entirely through hypermedia links provided in responses. The client doesn't need to hardcode URLs — it follows links from the response.

### REST Maturity Model

```
Level 0: Swamp of POX
  - Single URL, single method (POST everything)
  - Example: SOAP services

Level 1: Resources
  - Multiple URLs representing resources
  - Example: /users, /orders

Level 2: HTTP Verbs
  - Use HTTP methods properly (GET, POST, PUT, DELETE)
  - Use status codes correctly

Level 3: HATEOAS (Hypermedia Controls)
  - Responses include links to related actions
  - Client discovers available actions from responses
  - Example: Response includes {"links": {"self": "/users/1", "orders": "/users/1/orders"}}
```

### Without HATEOAS

```json
// Client hardcodes URLs
GET /api/users/1
{
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
}

// Client knows to call:
POST /api/users/1/orders
DELETE /api/users/1
PUT /api/users/1
```

### With HATEOAS

```json
GET /api/users/1
{
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "_links": {
        "self": {"href": "/api/users/1", "method": "GET"},
        "update": {"href": "/api/users/1", "method": "PUT"},
        "delete": {"href": "/api/users/1", "method": "DELETE"},
        "orders": {"href": "/api/users/1/orders", "method": "GET"},
        "create_order": {"href": "/api/users/1/orders", "method": "POST"}
    }
}

// Client only needs to know the base URL
// All actions are discoverable from the response
```

---

## Link Relations <a name="link-relations"></a>

Link relations (`rel`) describe the relationship between resources.

### Standard Link Relations (RFC 5988)

| Relation | Description |
|----------|-------------|
| `self` | The current resource |
| `next` | Next page |
| `prev` | Previous page |
| `first` | First page |
| `last` | Last page |
| `parent` | Parent resource |
| `child` | Child resource |
| `related` | Related resource |
| `canonical` | Canonical version of this resource |
| `alternate` | Alternative representation |
| `enclosure` | Related payload (like attachments) |

### Custom Link Relations

```json
{
    "id": 1,
    "status": "pending",
    "_links": {
        "self": "/api/orders/1",
        "approve": {
            "href": "/api/orders/1/approve",
            "method": "POST",
            "title": "Approve this order"
        },
        "cancel": {
            "href": "/api/orders/1/cancel",
            "method": "POST",
            "title": "Cancel this order"
        },
        "payment": {
            "href": "/api/orders/1/payment",
            "method": "GET"
        }
    }
}
```

---

## HAL Format <a name="hal"></a>

HAL (Hypertext Application Language) is a simple format for hypermedia APIs.

```json
{
    "_links": {
        "self": {"href": "/api/users/1"},
        "curies": [
            {
                "name": "acme",
                "href": "http://api.example.com/docs/{rel}",
                "templated": true
            }
        ],
        "acme:orders": {"href": "/api/users/1/orders"},
        "acme:avatar": {"href": "/api/users/1/avatar"}
    },
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
}
```

### HAL with Pagination

```json
{
    "_links": {
        "self": {"href": "/api/users?page=2"},
        "next": {"href": "/api/users?page=3"},
        "prev": {"href": "/api/users?page=1"},
        "first": {"href": "/api/users?page=1"},
        "last": {"href": "/api/users?page=10"}
    },
    "count": 50,
    "page": 2,
    "per_page": 5,
    "_embedded": {
        "users": [
            {"id": 6, "name": "Frank"},
            {"id": 7, "name": "Grace"},
            {"id": 8, "name": "Heidi"}
        ]
    }
}
```

---

## Building HATEOAS with FastAPI <a name="fastapi"></a>

### Link Builder

```python
from pydantic import BaseModel
from typing import Any
from fastapi import Request

class Link(BaseModel):
    href: str
    method: str = "GET"
    title: str | None = None
    templated: bool = False

class HATEOASResponse(BaseModel):
    _links: dict[str, Link | list[Link]]
    data: Any

class LinkBuilder:
    def __init__(self, request: Request, base_url: str | None = None):
        self.request = request
        self.base_url = base_url or str(request.base_url).rstrip("/")

    def link(self, rel: str, path: str, method: str = "GET", title: str | None = None) -> dict:
        return {rel: Link(href=f"{self.base_url}{path}", method=method, title=title)}

    def self_link(self, path: str) -> dict:
        return {"self": Link(href=f"{self.base_url}{path}", method="GET")}

    def collection_links(self, path: str, page: int, total_pages: int) -> dict:
        links = {"self": Link(href=f"{self.base_url}{path}?page={page}")}
        if page > 1:
            links["prev"] = Link(href=f"{self.base_url}{path}?page={page - 1}")
        if page < total_pages:
            links["next"] = Link(href=f"{self.base_url}{path}?page={page + 1}")
        links["first"] = Link(href=f"{self.base_url}{path}?page=1")
        links["last"] = Link(href=f"{self.base_url}{path}?page={total_pages}")
        return links
```

### HATEOAS User Endpoints

```python
from fastapi import FastAPI, Request, Depends
from typing import Annotated

app = FastAPI()

@app.get("/api/users/{user_id}")
async def get_user(user_id: int, request: Request):
    builder = LinkBuilder(request)
    user = await get_user_from_db(user_id)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "_links": {
            **builder.self_link(f"/api/users/{user_id}"),
            "update": Link(
                href=f"{request.base_url}api/users/{user_id}",
                method="PUT",
                title="Update user"
            ),
            "delete": Link(
                href=f"{request.base_url}api/users/{user_id}",
                method="DELETE",
                title="Delete user"
            ),
            "orders": Link(
                href=f"{request.base_url}api/users/{user_id}/orders",
                method="GET",
                title="User orders"
            ),
        }
    }

@app.get("/api/users/{user_id}/orders")
async def get_user_orders(
    user_id: int,
    request: Request,
    page: int = 1,
    per_page: int = 20,
):
    builder = LinkBuilder(request)
    orders, total = await get_user_orders_from_db(user_id, page, per_page)
    total_pages = (total + per_page - 1) // per_page

    return {
        "data": [
            {
                "id": order.id,
                "status": order.status,
                "_links": {
                    "self": Link(href=f"{request.base_url}api/orders/{order.id}"),
                    "items": Link(href=f"{request.base_url}api/orders/{order.id}/items"),
                }
            }
            for order in orders
        ],
        "_links": builder.collection_links(f"/api/users/{user_id}/orders", page, total_pages),
        "meta": {"total": total, "page": page, "per_page": per_page}
    }
```

### State-Aware Links

```python
@app.get("/api/orders/{order_id}")
async def get_order(order_id: int, request: Request):
    order = await get_order_from_db(order_id)
    builder = LinkBuilder(request)

    links = {
        "self": Link(href=f"{request.base_url}api/orders/{order.id}"),
    }

    # Add action links based on current state
    if order.status == "pending":
        links["approve"] = Link(
            href=f"{request.base_url}api/orders/{order.id}/approve",
            method="POST",
            title="Approve order"
        )
        links["cancel"] = Link(
            href=f"{request.base_url}api/orders/{order.id}/cancel",
            method="POST",
            title="Cancel order"
        )
    elif order.status == "approved":
        links["ship"] = Link(
            href=f"{request.base_url}api/orders/{order.id}/ship",
            method="POST",
            title="Ship order"
        )
    elif order.status == "shipped":
        links["track"] = Link(
            href=f"{request.base_url}api/orders/{order.id}/tracking",
            method="GET",
            title="Track shipment"
        )

    return {
        "id": order.id,
        "status": order.status,
        "_links": links
    }
```

---

## JSON:API Spec <a name="jsonapi"></a>

JSON:API is a specification for building APIs with consistent structure.

```json
{
    "jsonapi": {"version": "1.0"},
    "data": {
        "type": "users",
        "id": "1",
        "attributes": {
            "name": "Alice",
            "email": "alice@example.com"
        },
        "relationships": {
            "orders": {
                "links": {
                    "self": "/api/users/1/relationships/orders",
                    "related": "/api/users/1/orders"
                }
            }
        },
        "links": {
            "self": "/api/users/1"
        }
    }
}
```

### JSON:API Collection

```json
{
    "jsonapi": {"version": "1.0"},
    "data": [
        {
            "type": "users",
            "id": "1",
            "attributes": {"name": "Alice"}
        },
        {
            "type": "users",
            "id": "2",
            "attributes": {"name": "Bob"}
        }
    ],
    "links": {
        "self": "/api/users?page[offset]=0&page[limit]=10",
        "next": "/api/users?page[offset]=10&page[limit]=10",
        "last": "/api/users?page[offset]=90&page[limit]=10"
    },
    "meta": {
        "total": 95
    }
}
```

---

## Link Header <a name="link-header"></a>

RFC 8288 defines the Link HTTP header for conveying link relations.

```python
from fastapi import Response

@app.get("/api/users")
async def list_users(response: Response, page: int = 1, per_page: int = 20):
    users, total = await get_users(page, per_page)
    total_pages = (total + per_page - 1) // per_page

    links = []
    links.append(f'<{build_url("/api/users", page=page)}>; rel="self"')
    if page > 1:
        links.append(f'<{build_url("/api/users", page=page-1)}>; rel="prev"')
    if page < total_pages:
        links.append(f'<{build_url("/api/users", page=page+1)}>; rel="next"')
    links.append(f'<{build_url("/api/users", page=1)}>; rel="first"')
    links.append(f'<{build_url("/api/users", page=total_pages)}>; rel="last"')

    response.headers["Link"] = ", ".join(links)

    return {"users": users, "total": total}
```

---

## Discoverability <a name="discoverability"></a>

### API Root / Entry Point

```python
@app.get("/api")
async def api_root(request: Request):
    base = str(request.base_url).rstrip("/")
    return {
        "name": "My API",
        "version": "2.0",
        "_links": {
            "self": {"href": f"{base}/api"},
            "users": {"href": f"{base}/api/users", "method": "GET"},
            "orders": {"href": f"{base}/api/orders", "method": "GET"},
            "auth": {
                "login": {"href": f"{base}/api/auth/login", "method": "POST"},
                "register": {"href": f"{base}/api/auth/register", "method": "POST"},
            },
            "docs": {"href": f"{base}/docs"},
            "openapi": {"href": f"{base}/openapi.json"},
        }
    }
```

### Auto-Discovery Middleware

```python
class HATEOASMiddleware:
    async def __call__(self, request: Request, call_next):
        response = await call_next(request)

        if response.headers.get("content-type", "").startswith("application/json"):
            body = await self.add_discovery_links(request, response)
            return JSONResponse(content=body, headers=dict(response.headers))

        return response

    async def add_discovery_links(self, request: Request, response):
        body = json.loads(response.body)
        path = request.url.path

        if "_links" not in body:
            body["_links"] = {}

        # Add common discovery links
        body["_links"]["api_root"] = {"href": "/api"}
        body["_links"]["docs"] = {"href": "/docs"}

        return body
```

---

## Interview Questions

1. **What is HATEOAS and why is it important?**
HATEOAS means responses include links that tell the client what actions are available. It makes the API self-documenting and discoverable. Clients only need to know the entry point URL; everything else is discovered from links. This decouples client and server, allowing the server to change URLs without breaking clients.

2. **How do you implement HATEOAS in FastAPI?**
Create a LinkBuilder utility that generates links based on the request context. Add `_links` dictionaries to response models with `self`, `related`, and action links. Include state-dependent links (e.g., "approve" only appears when order is pending). Use Pydantic models for consistent link structure.

3. **What is HAL format?**
HAL (Hypertext Application Language) is a simple format for hypermedia APIs. Resources include `_links` (for navigation) and `_embedded` (for related resources). HAL supports link relations, URI templates, and curies. It's simple, widely adopted, and works well with JSON.

4. **How does pagination work with HATEOAS?**
Include `first`, `prev`, `next`, `last` links in collection responses. Each link points to the appropriate page. The client navigates pages by following links rather than constructing URLs. Include metadata like `total`, `page`, `per_page`.

5. **What are link relations?**
Link relations (`rel`) describe the relationship between resources. Standard relations include `self`, `next`, `prev`, `parent`, `child`, `related`. Custom relations (like `approve`, `cancel`) describe available actions. They help clients understand what each link does without hardcoding behavior.
