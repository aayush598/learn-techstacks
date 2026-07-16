# Strawberry GraphQL with FastAPI

## Table of Contents
1. [GraphQL vs REST](#graphql-vs-rest)
2. [Strawberry Setup](#setup)
3. [Type Definitions](#types)
4. [Queries](#queries)
5. [Mutations](#mutations)
6. [Subscriptions](#subscriptions)
7. [DataLoader for N+1](#dataloader)
8. [Schema-First vs Code-First](#schema-first)
9. [GraphQL Federation](#federation)

---

## GraphQL vs REST <a name="graphql-vs-rest"></a>

| Feature | REST | GraphQL |
|---------|------|---------|
| Endpoints | Multiple (one per resource) | Single endpoint |
| Data fetching | Over/under fetching common | Exact data you need |
| Type system | Optional (OpenAPI) | Built-in (schema) |
| Versioning | URL/header versioning | Schema evolution |
| Caching | HTTP caching built-in | Requires custom solution |
| Real-time | WebSocket/polling | Subscriptions built-in |
| File upload | Native | Requires specification |
| Tooling | Mature | Growing ecosystem |

### When to Use GraphQL

```
Use GraphQL when:
- Multiple clients need different data shapes
- Complex data with many relationships
- Mobile clients need bandwidth efficiency
- Rapid frontend iteration without backend changes
- API is consumed by multiple teams

Use REST when:
- Simple CRUD operations
- HTTP caching is critical
- File upload/download is primary
- Team is more familiar with REST
- API is simple and stable
```

---

## Strawberry Setup <a name="setup"></a>

### Installation

```bash
pip install strawberry-graphql[fastapi]
```

### Basic Setup

```python
# app/main.py
import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello, World!"

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
```

### Full Application Structure

```
app/
├── main.py
├── graphql/
│   ├── __init__.py
│   ├── schema.py          # Root schema
│   ├── types/
│   │   ├── __init__.py
│   │   ├── user.py         # User types
│   │   ├── post.py         # Post types
│   │   └── common.py       # Shared types
│   ├── queries/
│   │   ├── __init__.py
│   │   ├── user.py         # User queries
│   │   └── post.py         # Post queries
│   ├── mutations/
│   │   ├── __init__.py
│   │   ├── user.py         # User mutations
│   │   └── post.py         # Post mutations
│   ├── subscriptions/
│   │   └── ...
│   └── dataloaders/
│       ├── __init__.py
│       └── user_loader.py
├── models/                 # SQLAlchemy models
├── services/               # Business logic
└── database.py
```

---

## Type Definitions <a name="types"></a>

```python
# app/graphql/types/user.py
import strawberry
from strawberry.scalars import JSON
from datetime import datetime
from typing import Optional

@strawberry.enum
class UserRole(strawberry.enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

@strawberry.type
class User:
    id: int
    name: str
    email: str
    role: UserRole
    created_at: datetime
    is_active: bool = True

    @strawberry.field
    async def posts(self) -> list["Post"]:
        """Resolve user's posts."""
        return await post_service.get_by_user_id(self.id)

    @strawberry.field
    async def post_count(self) -> int:
        return await post_service.count_by_user_id(self.id)

@strawberry.type
class UserConnection:
    items: list[User]
    total_count: int
    has_next_page: bool
    has_previous_page: bool

@strawberry.type
class PageInfo:
    start_cursor: str | None
    end_cursor: str | None
    has_next_page: bool
    has_previous_page: bool

@strawberry.type
class UserEdge:
    node: User
    cursor: str

@strawberry.type
class UserConnectionRelay:
    edges: list[UserEdge]
    page_info: PageInfo
    total_count: int
```

```python
# app/graphql/types/post.py
import strawberry
from datetime import datetime

@strawberry.type
class Post:
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    @strawberry.field
    async def author(self) -> User:
        return await user_service.get_by_id(self.author_id)

    @strawberry.field
    async def comments(self) -> list["Comment"]:
        return await comment_service.get_by_post_id(self.id)

@strawberry.type
class Comment:
    id: int
    text: str
    created_at: datetime

    @strawberry.field
    async def author(self) -> User:
        return await user_service.get_by_id(self.author_id)
```

---

## Queries <a name="queries"></a>

```python
# app/graphql/queries/user.py
import strawberry
from typing import Optional

@strawberry.type
class UserQuery:
    @strawberry.field
    async def user(self, id: int) -> Optional[User]:
        user = await user_service.get_by_id(id)
        if not user:
            return None
        return User(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            created_at=user.created_at,
        )

    @strawberry.field
    async def users(
        self,
        skip: int = 0,
        limit: int = 20,
        search: str | None = None,
    ) -> UserConnection:
        users, total = await user_service.list_users(
            skip=skip, limit=limit, search=search
        )
        return UserConnection(
            items=[
                User(
                    id=u.id,
                    name=u.name,
                    email=u.email,
                    role=u.role,
                    created_at=u.created_at,
                )
                for u in users
            ],
            total_count=total,
            has_next_page=skip + limit < total,
            has_previous_page=skip > 0,
        )

    @strawberry.field
    async def me(self, info) -> Optional[User]:
        """Get current authenticated user."""
        user = info.context["user"]
        if not user:
            return None
        return User(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            created_at=user.created_at,
        )
```

```python
# app/graphql/schema.py
import strawberry
from app.graphql.queries.user import UserQuery
from app.graphql.queries.post import PostQuery
from app.graphql.mutations.user import UserMutation
from app.graphql.mutations.post import PostMutation

@strawberry.type
class Query(UserQuery, PostQuery):
    @strawberry.field
    def version(self) -> str:
        return "1.0.0"

@strawberry.type
class Mutation(UserMutation, PostMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
```

---

## Mutations <a name="mutations"></a>

```python
# app/graphql/mutations/user.py
import strawberry
from typing import Optional

@strawberry.input
class CreateUserInput:
    name: str
    email: str
    password: str

@strawberry.input
class UpdateUserInput:
    name: Optional[str] = None
    email: Optional[str] = None

@strawberry.type
class CreateUserPayload:
    user: Optional[User]
    errors: list[str] = strawberry.field(default_factory=list)

@strawberry.type
class UpdateUserPayload:
    user: Optional[User]
    errors: list[str] = strawberry.field(default_factory=list)

@strawberry.type
class UserMutation:
    @strawberry.mutation
    async def create_user(
        self, input: CreateUserInput
    ) -> CreateUserPayload:
        try:
            user = await user_service.create(
                name=input.name,
                email=input.email,
                password=input.password,
            )
            return CreateUserPayload(
                user=User(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    role=user.role,
                    created_at=user.created_at,
                )
            )
        except ValueError as e:
            return CreateUserPayload(errors=[str(e)])

    @strawberry.mutation
    async def update_user(
        self, id: int, input: UpdateUserInput
    ) -> UpdateUserPayload:
        try:
            user = await user_service.update(id, **input.__dict__)
            return UpdateUserPayload(
                user=User(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    role=user.role,
                    created_at=user.created_at,
                )
            )
        except ValueError as e:
            return UpdateUserPayload(errors=[str(e)])

    @strawberry.mutation
    async def delete_user(self, id: int) -> bool:
        await user_service.delete(id)
        return True
```

### Mutation Response Pattern

```python
@strawberry.type
class MutationError:
    field: str
    message: str

@strawberry.union
class CreateUserResult = User | MutationError

@strawberry.mutation
async def create_user(self, input: CreateUserInput) -> CreateUserResult:
    try:
        user = await user_service.create(**input.__dict__)
        return user
    except ValidationError as e:
        return MutationError(field="email", message=str(e))
```

---

## Subscriptions <a name="subscriptions"></a>

```python
# app/graphql/subscriptions/__init__.py
import strawberry
from strawberry.subscriptions import GRAPHQL_TRANSPORT_WS_PROTOCOL
import asyncio

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count(self, target: int = 10) -> AsyncGenerator[int, None]:
        for i in range(target):
            yield i
            await asyncio.sleep(1)

    @strawberry.subscription
    async def user_created(self) -> AsyncGenerator[User, None]:
        """Subscribe to new user creation events."""
        async with event_bus.subscribe("user.created") as event:
            while True:
                user_data = await event.get()
                yield User(**user_data)

    @strawberry.subscription
    async def order_status_changed(
        self, order_id: int
    ) -> AsyncGenerator[OrderStatus, None]:
        """Subscribe to order status changes."""
        async with event_bus.subscribe(f"order.{order_id}.status") as event:
            while True:
                status_data = await event.get()
                yield OrderStatus(**status_data)

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
    subscription_protocols=[GRAPHQL_TRANSPORT_WS_PROTOCOL],
)
```

### WebSocket Endpoint

```python
# GraphQL subscriptions use WebSocket
# Strawberry provides the WebSocket endpoint automatically
# Connect at: ws://localhost:8000/graphql
```

---

## DataLoader for N+1 <a name="dataloader"></a>

```python
# app/graphql/dataloaders/user_loader.py
from strawberry.dataloader import DataLoader
from typing import List

async def load_users(user_ids: List[int]) -> List[User]:
    """Batch load users by IDs."""
    users = await user_service.get_by_ids(user_ids)
    user_map = {u.id: u for u in users}
    return [user_map.get(uid) for uid in user_ids]

user_loader: DataLoader[int, User] = DataLoader(load_fn=load_users)

# Usage in type
@strawberry.type
class Post:
    id: int
    title: str
    author_id: int

    @strawberry.field
    async def author(self) -> User:
        return await user_loader.load(self.author_id)
```

### Batch Loading in Practice

```python
# Without DataLoader (N+1 problem):
# Query posts → 1 query for posts
# For each post, resolve author → N queries for users
# Total: N+1 queries

# With DataLoader:
# Query posts → 1 query for posts
# Collect all author_ids → 1 batch query for users
# Total: 2 queries

# DataLoader automatically batches and caches within a single request
```

---

## Schema-First vs Code-First <a name="schema-first"></a>

### Code-First (Strawberry)

```python
# Define types in Python, schema is generated
import strawberry

@strawberry.type
class User:
    id: int
    name: str
    email: str

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> User:
        return get_user(id)

schema = strawberry.Schema(query=Query)

# Generated SDL:
# type User {
#   id: Int!
#   name: String!
#   email: String!
# }
# type Query {
#   user(id: Int!): User
# }
```

### Schema-First (Raw SDL)

```graphql
# schema.graphql
type User {
  id: Int!
  name: String!
  email: String!
}

type Query {
  user(id: Int!): User
  users(skip: Int, limit: Int): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}
```

### Comparison

| Aspect | Code-First | Schema-First |
|--------|-----------|-------------|
| Type safety | Python type hints | SDL types |
| Resolvers | Python methods | Separate resolver code |
| IDE support | Full Python IDE | GraphQL IDE |
| Validation | Pydantic-like | SDL validation |
| Collaboration | Python developers | Frontend + backend |
| Refactoring | Easy with Python tools | Schema migration tools |

---

## GraphQL Federation <a name="federation"></a>

Federation allows splitting a GraphQL schema across multiple services.

### Subgraph

```python
# User Service (subgraph)
import strawberry
from strawberry.federation import Schema

@strawberry.federation.object(keys=("id",))
class User:
    id: int
    name: str
    email: str

    @strawberry.federation.field(requires=["email"])
    async def orders(self) -> list["Order"]:
        return await order_service.get_by_user_id(self.id)

@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: int) -> User:
        return await user_service.get_by_id(id)

schema = Schema(query=Query, enable_federation_2=True)
```

### Gateway

```python
# API Gateway (federated)
from strawberry.federation import Schema

schema = Schema(query=Query, enable_federation_2=True)

# The gateway composes the schema from all subgraphs
# and routes queries to the appropriate service
```

### Federation Commands

```bash
# Print subgraph schema for federation
strawberry print-schema --federation > schema.graphql

# Compose supergraph schema
rover supergraph compose --config ./supergraph-config.yaml
```

---

## Interview Questions

1. **What is Strawberry and how does it integrate with FastAPI?**
Strawberry is a Python GraphQL library that uses type hints to define schemas. It integrates with FastAPI via `GraphQLRouter` which provides a `/graphql` endpoint. Strawberry handles query parsing, validation, execution, and WebSocket subscriptions.

2. **How does DataLoader solve the N+1 problem?**
DataLoader batches multiple individual requests into a single database query. When resolving a list of posts and their authors, instead of querying the user table for each post, DataLoader collects all author IDs and makes one batch query. It also caches results within a single request.

3. **What is the difference between schema-first and code-first in GraphQL?**
Schema-first: Write the SDL schema first, then implement resolvers. Good for frontend-backend collaboration. Code-first: Define types in Python with Strawberry, schema is generated. Benefits from Python type safety and IDE support. Strawberry is code-first.

4. **How do GraphQL subscriptions work?**
Subscriptions use WebSocket connections for real-time updates. The client subscribes to a GraphQL subscription field. When data changes on the server, the server pushes updates to the client. Strawberry supports the `graphql-transport-ws` protocol.

5. **What is GraphQL federation?**
Federation splits a GraphQL schema across multiple services. Each service owns its types and resolvers. A gateway composes the schema and routes queries. Use federation when multiple teams own different parts of the API.
