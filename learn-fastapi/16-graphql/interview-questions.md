# GraphQL with FastAPI — Interview Questions

## Table of Contents
1. [Basics](#basics)
2. [Queries & Types](#queries--types)
3. [Mutations](#mutations)
4. [Subscriptions](#subscriptions)
5. [Pagination](#pagination)
6. [Security](#security)
7. [Federation](#federation)
8. [Performance](#performance)
9. [Error Handling](#error-handling)
10. [Schema Design](#schema-design)
11. [Production](#production)

---

## Basics

### Q1: What is GraphQL and how does it differ from REST?
**Answer:** GraphQL is a query language for APIs that lets clients request exactly the data they need. REST uses multiple endpoints with fixed data shapes. GraphQL uses a single endpoint where clients specify what fields they want. This eliminates over-fetching and under-fetching.

| Feature | REST | GraphQL |
|---------|------|---------|
| Endpoints | Multiple | Single |
| Data shape | Server-defined | Client-defined |
| Over-fetching | Common | Eliminated |
| Under-fetching | Common (N+1 calls) | Eliminated |
| Versioning | URL/header versioning | Schema evolution |
| Caching | HTTP caching built-in | Requires custom caching |
| Real-time | WebSocket/SSE separate | Subscriptions built-in |
| Type system | OpenAPI (optional) | Mandatory, introspectable |

### Q2: What is Strawberry and why use it with FastAPI?
**Answer:** Strawberry is a Python GraphQL library using type hints. It integrates with FastAPI via `GraphQLRouter`. Benefits: Python-native type safety, code-first approach, async support, automatic schema generation, and built-in subscriptions support.

```python
import strawberry
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class User:
    id: int
    name: str
    email: str

@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: int) -> User:
        return await db.get(User, id)

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
```

### Q3: What is a GraphQL schema?
**Answer:** A schema defines the types, queries, mutations, and subscriptions available in the API. It's the contract between client and server. In Strawberry, the schema is generated from Python type hints and decorators.

### Q4: Explain the difference between queries, mutations, and subscriptions.
**Answer:**
- **Queries**: Read data (like GET in REST). Don't modify state.
- **Mutations**: Write data (like POST/PUT/DELETE). Return the modified object.
- **Subscriptions**: Real-time data over WebSocket. Server pushes updates.

```python
@strawberry.type
class Query:
    @strawberry.field
    async def users(self) -> list[User]:
        return await db.get_all(User)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, name: str, email: str) -> User:
        user = User(id=generate_id(), name=name, email=email)
        await db.insert(user)
        return user

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def user_created(self) -> AsyncGenerator[User, None]:
        async for event in event_bus.subscribe("user.created"):
            yield User(**event.data)

schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)
```

---

## Queries & Types

### Q5: How do you handle nested data in GraphQL?
**Answer:** Define nested types and use field resolvers. For example, a `Post` type has an `author` field that resolves to a `User` type. Strawberry automatically handles the resolution chain. Use DataLoader to avoid N+1 queries when resolving collections.

```python
@strawberry.type
class Post:
    id: int
    title: str
    author_id: int

    @strawberry.field
    async def author(self) -> User:
        return await db.get(User, self.author_id)

    @strawberry.field
    async def comments(self) -> list[Comment]:
        return await db.query(Comment, post_id=self.id)
```

### Q6: What is the N+1 problem in GraphQL?
**Answer:** When resolving a list of items, each item's related data triggers a separate database query. Example: 10 posts × 1 query for author = 11 queries. DataLoader solves this by batching and caching within a single request.

```python
# WITHOUT DataLoader: N+1 queries
@strawberry.type
class Post:
    @strawberry.field
    async def author(self) -> User:
        return await db.get(User, self.author_id)  # Called once per post!

# WITH DataLoader: 2 queries total (1 for posts, 1 for all authors)
@strawberry.type
class Post:
    @strawberry.field
    async def author(self, info) -> User:
        return await info.context["user_loader"].load(self.author_id)
```

### Q7: How does DataLoader work?
**Answer:** DataLoader collects all individual load requests within a single tick of the event loop and batches them into one database query. It also caches results within the request to prevent duplicate queries.

```python
from strawberry.dataloader import DataLoader

async def load_users(ids: list[int]) -> list[User]:
    users = await db.query(User, id__in=ids)
    user_map = {u.id: u for u in users}
    return [user_map.get(id) for id in ids]

user_loader = DataLoader(load_fn=load_users)

# In resolver
@strawberry.field
async def author(self, info) -> User:
    return await info.context["user_loader"].load(self.author_id)
```

### Q8: How do you implement custom scalar types in GraphQL?
**Answer:** Define custom scalars for types like DateTime, Email, URL:

```python
import strawberry
from datetime import datetime

@strawberry.scalar(name="DateTime")
class DateTimeScalar:
    @staticmethod
    def serialize(value: datetime) -> str:
        return value.isoformat()

    @staticmethod
    def parse_value(value: str) -> datetime:
        return datetime.fromisoformat(value)

@strawberry.type
class Event:
    id: int
    name: str
    created_at: DateTimeScalar  # Custom scalar
```

---

## Mutations

### Q9: How do you handle mutation errors in GraphQL?
**Answer:** Return typed error payloads instead of throwing exceptions. Define union types like `User | ValidationError | ForbiddenError`. This gives clients structured error information without relying on GraphQL's error field.

```python
import strawberry
from typing import Union

@strawberry.type
class ValidationError:
    field: str
    message: str

@strawberry.type
class ForbiddenError:
    message: str

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, name: str, email: str) -> User | ValidationError:
        if not email or "@" not in email:
            return ValidationError(field="email", message="Invalid email")
        if len(name) < 2:
            return ValidationError(field="name", message="Name too short")

        user = User(id=generate_id(), name=name, email=email)
        await db.insert(user)
        return user
```

### Q10: What is input validation in GraphQL mutations?
**Answer:** Use Pydantic models or Strawberry input types. Validate data before processing. Return typed validation errors with field-level messages. Strawberry supports `@strawberry.input` for mutation arguments.

```python
@strawberry.input
class CreateUserInput:
    name: str
    email: str
    age: int | None = None

    def validate(self) -> list[str]:
        errors = []
        if len(self.name) < 2:
            errors.append("Name must be at least 2 characters")
        if "@" not in self.email:
            errors.append("Invalid email address")
        if self.age is not None and self.age < 0:
            errors.append("Age must be positive")
        return errors

@strawberry.mutation
async def create_user(self, input: CreateUserInput) -> User:
    errors = input.validate()
    if errors:
        raise ValidationError(errors)
    user = User(id=generate_id(), name=input.name, email=input.email)
    await db.insert(user)
    return user
```

---

## Subscriptions

### Q11: How do GraphQL subscriptions differ from WebSockets?
**Answer:** Subscriptions use WebSocket as transport but add a GraphQL protocol layer. The client sends a GraphQL subscription query, and the server pushes matching data. Strawberry uses the `graphql-transport-ws` protocol.

### Q12: How do you scale subscriptions across multiple server instances?
**Answer:** Use Redis PubSub or a message broker (Kafka, RabbitMQ) for event distribution. When a mutation occurs on one instance, it publishes to Redis. All instances subscribe to Redis and deliver events to their connected WebSocket clients.

```python
import redis.asyncio as redis

class SubscriptionManager:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)

    async def publish(self, channel: str, data: dict):
        await self.redis.publish(channel, json.dumps(data))

    async def subscribe(self, channel: str):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(channel)
        async for message in pubsub.listen():
            if message["type"] == "message":
                yield json.loads(message["data"])
```

---

## Pagination

### Q13: What is Relay-style pagination?
**Answer:** Uses connection/edge/cursor pattern. Each page returns edges (nodes + cursors), pageInfo (hasNextPage, endCursor), and totalCount. Cursors are opaque strings. Supports efficient forward/backward pagination and consistent page boundaries.

```python
@strawberry.type
class PageInfo:
    has_next_page: bool
    has_previous_page: bool
    end_cursor: str | None
    start_cursor: str | None

@strawberry.type
class UserEdge:
    node: User
    cursor: str

@strawberry.type
class UserConnection:
    edges: list[UserEdge]
    page_info: PageInfo
    total_count: int

@strawberry.type
class Query:
    @strawberry.field
    async def users(self, first: int = 10, after: str = None) -> UserConnection:
        cursor = decode_cursor(after) if after else 0
        users = await db.query(User).offset(cursor).limit(first + 1).all()
        has_next = len(users) > first
        users = users[:first]

        return UserConnection(
            edges=[UserEdge(node=u, cursor=encode_cursor(cursor + i)) for i, u in enumerate(users)],
            page_info=PageInfo(
                has_next_page=has_next,
                has_previous_page=cursor > 0,
                end_cursor=encode_cursor(cursor + len(users) - 1) if users else None,
                start_cursor=encode_cursor(cursor) if users else None,
            ),
            total_count=await db.count(User),
        )
```

### Q14: How do you implement cursor-based pagination?
**Answer:** Encode an offset or ID into a base64 cursor string. On each query, decode the cursor to get the starting position. Return the next cursor based on the last item in the results. Clients pass the cursor in `after`/`before` arguments.

```python
import base64

def encode_cursor(value: int) -> str:
    return base64.b64encode(f"cursor:{value}".encode()).decode()

def decode_cursor(cursor: str) -> int:
    return int(base64.b64decode(cursor).decode().split(":")[1])
```

---

## Security

### Q15: How do you prevent GraphQL denial-of-service attacks?
**Answer:**
- Set query depth limits (prevent deeply nested queries)
- Limit query complexity (score each field)
- Set timeout on query execution
- Rate limit by client/IP
- Disable introspection in production
- Use persisted queries (only allow pre-approved queries)

```python
from strawberry.extensions import QueryDepthLimiter

schema = strawberry.Schema(
    query=Query,
    extensions=[
        QueryDepthLimiter(max_depth=10),
    ],
)
```

### Q16: How do you implement query complexity analysis?
**Answer:** Assign a cost to each field. Sum the total cost of a query. Reject queries exceeding a threshold. Example: list fields cost `limit × field_cost`, single fields cost 1.

```python
class ComplexityAnalyzer:
    def __init__(self, max_complexity: int = 1000):
        self.max_complexity = max_complexity

    def analyze(self, query: str, variables: dict) -> int:
        # Parse query and calculate total complexity
        # Each list field costs 10 × the limit argument
        # Each object field costs 1
        pass

    def validate(self, query: str, variables: dict):
        complexity = self.analyze(query, variables)
        if complexity > self.max_complexity:
            raise QueryTooComplexError(f"Query complexity {complexity} exceeds max {self.max_complexity}")
```

### Q17: How do you handle authentication in GraphQL subscriptions?
**Answer:** Validate the JWT token during the WebSocket connection initialization (the `connection_init` message). Store the authenticated user in the subscription context. Reject subscriptions without valid authentication.

```python
@strawberry.type
class Subscription:
    @strawberry.subscription
    async def order_updates(self, info, user_id: int) -> AsyncGenerator[OrderUpdate, None]:
        user = info.context.get("user")
        if not user:
            raise AuthenticationError("Not authenticated")

        async for event in event_bus.subscribe(f"user:{user_id}:orders"):
            yield OrderUpdate(**event.data)
```

---

## Federation

### Q18: What is GraphQL Federation?
**Answer:** Federation splits a GraphQL schema across multiple services. Each service owns its types and resolvers. A gateway composes the schema and routes queries. Use federation when multiple teams own different API domains.

```python
# Users service
@strawberry.federation.type(keys=["id"])
class User:
    id: int
    name: str
    email: str

    @strawberry.field
    async def orders(self) -> list["Order"]:
        return await order_service.get_orders_for_user(self.id)

# Orders service
@strawberry.federation.type(keys=["id"])
class Order:
    id: int
    total: float
    user_id: int

    @strawberry.field
    async def user(self) -> User:
        return await user_service.get_user(self.user_id)
```

### Q19: How does schema composition work in federation?
**Answer:** Each subgraph defines its portion of the schema. The gateway merges all subgraphs into a supergraph schema. Types can be extended across services using `@key` and `@requires` directives. The gateway resolves cross-service references.

---

## Performance

### Q20: How do you cache GraphQL responses?
**Answer:**
- Use HTTP caching with `@cache` directives
- Implement DataLoader-level caching (per-request)
- Use Redis caching for expensive queries
- Persisted queries enable CDN caching
- Response-level caching with cache keys based on query + variables

```python
from functools import lru_cache

@strawberry.type
class Query:
    @strawberry.field
    async def popular_products(self) -> list[Product]:
        cache_key = "popular_products"
        cached = await redis.get(cache_key)
        if cached:
            return json.loads(cached)

        products = await db.query(Product, is_popular=True).limit(10).all()
        await redis.setex(cache_key, 300, json.dumps([p.dict() for p in products]))
        return products
```

### Q21: How do you optimize GraphQL for mobile clients?
**Answer:** Use field-level selection to send only requested fields. Implement query complexity limits. Use persisted queries to reduce payload size. Add connection-based pagination. Use `@defer` and `@stream` for progressive data loading.

### Q22: What are persisted queries and how do they improve performance?
**Answer:** Persisted queries replace full query strings with hashes. The client sends only the hash, reducing bandwidth. Server pre-stores the full query. Also improves security by only allowing known queries.

```python
# Client sends: {"extensions": {"persistedQuery": {"sha256Hash": "abc123"}}}
# Instead of the full query string

# Server stores known queries
PERSISTED_QUERIES = {
    "abc123": "query GetUser($id: Int!) { user(id: $id) { name email } }",
    "def456": "query ListProducts { products { name price } }",
}
```

---

## Error Handling

### Q23: How do you implement structured error handling in GraphQL?
**Answer:** GraphQL has two error mechanisms: the `errors` field in the response and typed union returns. Use typed unions for expected errors (validation, authorization) and the `errors` field for unexpected errors.

```python
@strawberry.type
class NotFoundError:
    message: str

@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: int) -> User | NotFoundError:
        user = await db.get(User, id)
        if not user:
            return NotFoundError(message=f"User {id} not found")
        return user
```

### Q24: How do you handle partial failures in GraphQL?
**Answer:** GraphQL supports partial data - some fields resolve successfully while others fail. The response includes both `data` (partial) and `errors` (failures). Implement graceful degradation by returning available data and reporting errors for unavailable fields.

```python
@strawberry.type
class User:
    id: int
    name: str

    @strawberry.field
    async def recent_orders(self) -> list[Order]:
        try:
            return await order_service.get_recent(self.id)
        except ServiceUnavailableError:
            # Return empty list and add error to context
            return []
```

---

## Schema Design

### Q25: What are the best practices for GraphQL schema design?
**Answer:**
- Use nouns for types (User, Order), verbs for mutations (CreateUser, UpdateOrder)
- Use connection types for lists (UserConnection, not [User])
- Make IDs opaque (cursors, not database IDs)
- Use input types for mutations
- Design for the client's needs, not the database schema
- Use enums for fixed sets of values
- Keep the schema flat when possible (avoid deep nesting)
- Version through schema evolution, not URL versioning

### Q26: How do you design a GraphQL schema for a multi-tenant application?
**Answer:**

```python
@strawberry.type
class Tenant:
    id: str
    name: str
    plan: str

@strawberry.type
class Query:
    @strawberry.field
    async def current_tenant(self, info) -> Tenant:
        user = info.context["user"]
        return await db.get(Tenant, user.tenant_id)

    @strawberry.field
    async def tenant_users(self, info) -> list[User]:
        user = info.context["user"]
        return await db.query(User, tenant_id=user.tenant_id)

# Middleware to inject tenant context
async def tenant_middleware(request, call_next):
    user = await get_current_user(request)
    request.scope["user"] = user
    response = await call_next(request)
    return response
```

---

## Production

### Q27: How do you monitor GraphQL in production?
**Answer:** Track query performance per resolver, track field-level latency, monitor query complexity distribution, set up alerts for slow queries, track error rates by type, and use query tracing to identify bottlenecks.

```python
import time

class MetricsExtension:
    async def resolve(self, _next, source, info, **kwargs):
        start = time.perf_counter()
        result = await _next(source, info, **kwargs)
        duration = time.perf_counter() - start

        # Record metrics
        resolver_name = f"{info.parent_type.name}.{info.field_name}"
        FIELD_LATENCY.labels(resolver=resolver_name).observe(duration)
        FIELD_CALLS.labels(resolver=resolver_name).inc()

        return result
```

### Q28: How do you implement rate limiting for GraphQL?
**Answer:** Rate limit by query complexity rather than request count. Track complexity points per client. Reject queries that exceed the budget. Reset the budget periodically.

```python
class ComplexityRateLimiter:
    def __init__(self, redis_client, max_complexity_per_minute=10000):
        self.redis = redis_client
        self.max_complexity = max_complexity_per_minute

    async def check_rate_limit(self, client_id: str, query_complexity: int) -> bool:
        key = f"graphql:rate:{client_id}:{int(time.time()) // 60}"
        current = await self.redis.incrby(key, query_complexity)
        if current == 1:
            await self.redis.expire(key, 120)
        return current <= self.max_complexity
```

### Q29: How do you handle GraphQL in a microservices architecture?
**Answer:** Use a GraphQL gateway that composes schemas from multiple services. Each service exposes its own GraphQL or REST API. The gateway handles query routing, schema stitching, and response merging. Use federation for large-scale deployments.

### Q30: How do you test GraphQL endpoints?
**Answer:** Write unit tests for resolvers, integration tests for queries and mutations, and end-to-end tests for complete workflows. Mock external services. Test error cases and edge cases. Use snapshot testing for schema changes.

```python
import pytest
from strawberry.testing import SchemaTester

@pytest.mark.asyncio
async def test_get_user():
    result = await schematester.query("{ user(id: 1) { name email } }")
    assert result.errors is None
    assert result.data["user"]["name"] == "John"

@pytest.mark.asyncio
async def test_create_user():
    result = await schematester.query(
        'mutation { createUser(name: "Jane", email: "jane@test.com") { id name } }'
    )
    assert result.errors is None
    assert result.data["createUser"]["name"] == "Jane"
```
