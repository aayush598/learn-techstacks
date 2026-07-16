# Advanced GraphQL with FastAPI

## Table of Contents
1. [GraphQL Subscriptions (WebSocket)](#subscriptions)
2. [Authentication in GraphQL](#authentication)
3. [Authorization](#authorization)
4. [Pagination (Relay-style)](#pagination)
5. [Error Handling](#error-handling)
6. [File Uploads](#file-uploads)
7. [Custom Scalars](#custom-scalars)
8. [Federation Gateway](#federation)

---

## 1. GraphQL Subscriptions (WebSocket) <a name="subscriptions"></a>

### Subscription with Strawberry

```python
import strawberry
from strawberry.subscriptions import GRAPHQL_TRANSPORT_WS_PROTOCOL
import asyncio
from typing import AsyncGenerator

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def on_message_sent(self, channel_id: int) -> AsyncGenerator[Message, None]:
        pubsub = info.context["pubsub"]
        async with pubsub.subscribe(f"channel:{channel_id}") as subscriber:
            async for event in subscriber:
                yield Message.from_event(event)

    @strawberry.subscription
    async def order_status_updates(
        self, order_id: int
    ) -> AsyncGenerator[OrderStatusUpdate, None]:
        async with redis.pubsub() as pubsub:
            await pubsub.subscribe(f"order:{order_id}:status")
            async for message in pubsub.listen():
                if message["type"] == "message":
                    data = json.loads(message["data"])
                    yield OrderStatusUpdate(**data)

    @strawberry.subscription
    async def live_metrics(self) -> AsyncGenerator[MetricUpdate, None]:
        while True:
            metrics = await collect_metrics()
            yield MetricUpdate(
                requests_per_second=metrics.rps,
                error_rate=metrics.error_rate,
                latency_p99=metrics.latency_p99,
            )
            await asyncio.sleep(5)

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
    subscription_protocols=[GRAPHQL_TRANSPORT_WS_PROTOCOL],
)
```

### Redis PubSub for Multi-Instance Subscriptions

```python
import redis.asyncio as redis

class RedisPubSub:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)

    async def publish(self, channel: str, data: dict):
        await self.redis.publish(channel, json.dumps(data))

    async def subscribe(self, channel: str):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(channel)
        return pubsub

# Usage in mutation
@strawberry.mutation
async def send_message(
    self, channel_id: int, text: str
) -> Message:
    message = await message_service.create(channel_id, text)
    # Publish event for subscription delivery
    await pubsub.publish(f"channel:{channel_id}", message.to_dict())
    return message
```

### Subscription Authentication

```python
@strawberry.subscription
async def authenticated_subscription(
    self, info
) -> AsyncGenerator[Notification, None]:
    user = info.context.get("user")
    if not user:
        raise strawberry.exceptions.Unauthorized("Not authenticated")

    async with pubsub.subscribe(f"user:{user.id}:notifications") as sub:
        async for event in sub:
            yield Notification(**event)
```

---

## 2. Authentication in GraphQL <a name="authentication"></a>

### Context-Based Authentication

```python
# app/graphql/context.py
from fastapi import Request
from typing import Any

class GraphQLContext:
    def __init__(self, request: Request):
        self.request = request
        self.user = None

    async def authenticate(self):
        token = self.request.headers.get("Authorization", "").replace("Bearer ", "")
        if token:
            self.user = await decode_token(token)

# app/main.py
async def get_context(request: Request) -> GraphQLContext:
    context = GraphQLContext(request)
    await context.authenticate()
    return context

graphql_app = GraphQLRouter(schema, context_getter=get_context)
```

### Authentication in Queries

```python
@strawberry.type
class Query:
    @strawberry.field
    async def me(self, info) -> User:
        user = info.context.get("user")
        if not user:
            raise strawberry.exceptions.Unauthorized("Please log in")
        return User.from_orm(user)

    @strawberry.field
    async def public_data(self) -> str:
        return "Anyone can see this"
```

### JWT Authentication Middleware

```python
from fastapi.security import HTTPBearer
import jwt

class JWTAuth:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def authenticate(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise strawberry.exceptions.Unauthorized("Token expired")
        except jwt.InvalidTokenError:
            raise strawberry.exceptions.Unauthorized("Invalid token")

jwt_auth = JWTAuth(secret_key=os.environ["SECRET_KEY"])

async def get_context(request: Request) -> dict:
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user = None
    if token:
        try:
            payload = jwt_auth.authenticate(token)
            user = await user_service.get_by_id(payload["sub"])
        except Exception:
            pass

    return {"user": user, "request": request}
```

---

## 3. Authorization <a name="authorization"></a>

### Role-Based Authorization

```python
from enum import Enum

class Permission(strawberry.enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

def require_role(*roles):
    def resolver(func):
        async def wrapper(self, info, *args, **kwargs):
            user = info.context.get("user")
            if not user:
                raise strawberry.exceptions.Unauthorized("Not authenticated")
            if user.role not in roles:
                raise strawberry.exceptions.Forbidden("Insufficient permissions")
            return await func(self, info, *args, **kwargs)
        return wrapper
    return resolver

@strawberry.type
class Mutation:
    @strawberry.mutation
    @require_role(Permission.ADMIN)
    async def delete_user(self, id: int) -> bool:
        await user_service.delete(id)
        return True

    @strawberry.mutation
    @require_role(Permission.ADMIN, Permission.MODERATOR)
    async def moderate_post(self, post_id: int, action: str) -> Post:
        return await post_service.moderate(post_id, action)
```

### Object-Level Authorization

```python
@strawberry.federation.object(keys=("id",))
class Post:
    id: int
    title: str
    author_id: int
    published: bool

    @strawberry.field
    async def author(self) -> User:
        return await user_loader.load(self.author_id)

    def can_edit(self, user) -> bool:
        return user.id == self.author_id or user.role == "admin"

    def can_delete(self, user) -> bool:
        return user.id == self.author_id or user.role in ["admin", "moderator"]

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def update_post(
        self, info, id: int, input: UpdatePostInput
    ) -> Post:
        user = info.context["user"]
        post = await post_service.get_by_id(id)

        if not post.can_edit(user):
            raise strawberry.exceptions.Forbidden(
                "You can only edit your own posts"
            )

        return await post_service.update(id, **input.__dict__)
```

### Directive-Based Authorization

```python
import strawberry
from strawberry.permission import Permission

@strawberry.type
class Query:
    @strawberry.field(
        permission_classes=[IsAuthenticated]
    )
    async def me(self, info) -> User:
        return info.context["user"]

    @strawberry.field(
        permission_classes=[IsAdmin]
    )
    async def admin_dashboard(self, info) -> AdminDashboard:
        return await admin_service.get_dashboard()

class IsAuthenticated(Permission):
    message = "Not authenticated"
    async def has_permission(self, source, info, **kwargs) -> bool:
        return info.context.get("user") is not None

class IsAdmin(Permission):
    message = "Admin access required"
    async def has_permission(self, source, info, **kwargs) -> bool:
        user = info.context.get("user")
        return user and user.role == "admin"
```

---

## 4. Pagination (Relay-style) <a name="pagination"></a>

### Relay Connection Specification

```python
import strawberry
from typing import Optional

@strawberry.type
class PageInfo:
    start_cursor: Optional[str]
    end_cursor: Optional[str]
    has_next_page: bool
    has_previous_page: bool

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
    async def users(
        self,
        first: Optional[int] = None,
        after: Optional[str] = None,
        last: Optional[int] = None,
        before: Optional[str] = None,
        search: Optional[str] = None,
    ) -> UserConnection:
        # Decode cursor to get offset
        after_offset = decode_cursor(after) if after else 0
        before_offset = decode_cursor(before) if before else float("inf")

        # Fetch data
        users, total = await user_service.list_users(
            offset=after_offset,
            limit=first or 20,
            search=search,
        )

        # Build edges
        edges = [
            UserEdge(
                node=User.from_orm(u),
                cursor=encode_cursor(after_offset + i + 1),
            )
            for i, u in enumerate(users)
        ]

        return UserConnection(
            edges=edges,
            page_info=PageInfo(
                start_cursor=edges[0].cursor if edges else None,
                end_cursor=edges[-1].cursor if edges else None,
                has_next_page=after_offset + len(users) < total,
                has_previous_page=after_offset > 0,
            ),
            total_count=total,
        )

def encode_cursor(offset: int) -> str:
    import base64
    return base64.b64encode(f"cursor:{offset}".encode()).decode()

def decode_cursor(cursor: str) -> int:
    import base64
    decoded = base64.b64decode(cursor).decode()
    return int(decoded.split(":")[1])
```

### Client Query

```graphql
query GetUsers {
  users(first: 10, after: "Y3Vyc29yOjEw") {
    edges {
      node {
        id
        name
        email
      }
      cursor
    }
    pageInfo {
      hasNextPage
      endCursor
    }
    totalCount
  }
}
```

---

## 5. Error Handling <a name="error-handling"></a>

### Custom Error Types

```python
import strawberry
from typing import Union

@strawberry.type
class ValidationError:
    field: str
    message: str

@strawberry.type
class NotFoundError:
    message: str
    resource_type: str

@strawberry.type
class ForbiddenError:
    message: str

@strawberry.union
class CreateUserResult = User | ValidationError | ForbiddenError

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(
        self, input: CreateUserInput
    ) -> CreateUserResult:
        try:
            user = await user_service.create(**input.__dict__)
            return user
        except ValueError as e:
            return ValidationError(field="email", message=str(e))
        except PermissionError as e:
            return ForbiddenError(message=str(e))
```

### Global Error Handling

```python
# GraphQL errors are automatically formatted
# But you can customize error formatting

def custom_error_formatter(error: GraphQLGraphQLError) -> dict:
    result = error.formatted
    if isinstance(error.original_error, strawberry.exceptions.Unauthorized):
        result["extensions"]["code"] = "UNAUTHENTICATED"
    elif isinstance(error.original_error, strawberry.exceptions.Forbidden):
        result["extensions"]["code"] = "FORBIDDEN"
    return result

schema = strawberry.Schema(
    query=Query,
    error_formatter=custom_error_formatter,
)
```

### Validation Error Handling

```python
from pydantic import ValidationError as PydanticValidationError

@strawberry.mutation
async def create_user(self, input: CreateUserInput) -> CreateUserResult:
    try:
        # Pydantic validation
        user_data = CreateUserInput(**input.__dict__)
        user = await user_service.create(**user_data.__dict__)
        return user
    except PydanticValidationError as e:
        errors = [
            ValidationError(field=err["loc"][-1], message=err["msg"])
            for err in e.errors()
        ]
        return errors[0] if errors else ValidationError(field="unknown", message=str(e))
```

---

## 6. File Uploads <a name="file-uploads"></a>

### Using graphql-upload

```bash
pip install python-multipart
```

```python
import strawberry
from fastapi import UploadFile, File

@strawberry.type
class UploadResponse:
    filename: str
    url: str
    size: int

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def upload_avatar(
        self, file: UploadFile
    ) -> UploadResponse:
        contents = await file.read()

        # Upload to S3/GCS
        url = await storage_service.upload(
            file=contents,
            filename=f"avatars/{file.filename}",
            content_type=file.content_type,
        )

        return UploadResponse(
            filename=file.filename,
            url=url,
            size=len(contents),
        )

    @strawberry.mutation
    async def upload_multiple_files(
        self, files: list[UploadFile]
    ) -> list[UploadResponse]:
        results = []
        for file in files:
            contents = await file.read()
            url = await storage_service.upload(
                file=contents,
                filename=f"uploads/{file.filename}",
                content_type=file.content_type,
            )
            results.append(UploadResponse(
                filename=file.filename,
                url=url,
                size=len(contents),
            ))
        return results
```

### Client Upload

```graphql
mutation UploadAvatar($file: Upload!) {
  uploadAvatar(file: $file) {
    filename
    url
    size
  }
}
```

```javascript
// Apollo Client
const formData = new FormData();
formData.append(
  "operations",
  JSON.stringify({
    query: `mutation UploadAvatar($file: Upload!) {
      uploadAvatar(file: $file) { filename url size }
    }`,
    variables: { file: null },
  })
);
formData.append("map", JSON.stringify({ "0": ["variables.file"] }));
formData.append("0", fileObject);
```

---

## 7. Custom Scalars <a name="custom-scalars"></a>

```python
import strawberry
from typing import NewType
from datetime import datetime, date
from pydantic import EmailStr

# Custom scalar type
DateTime = NewType("DateTime", str)
Email = NewType("Email", str)
JSON = NewType("JSON", str)

# Register custom scalar type
@strawberry.scalar
class DateTimeScalar:
    @staticmethod
    def serialize(value: datetime) -> str:
        return value.isoformat()

    @staticmethod
    def parse_value(value: str) -> datetime:
        return datetime.fromisoformat(value)

    @staticmethod
    def parse_literal(value_node) -> datetime:
        return datetime.fromisoformat(value_node.value)

@strawberry.scalar
class EmailScalar:
    @staticmethod
    def serialize(value: str) -> str:
        return value

    @staticmethod
    def parse_value(value: str) -> str:
        if "@" not in value:
            raise ValueError("Invalid email")
        return value

# Use in types
@strawberry.type
class User:
    id: int
    name: str
    email: EmailScalar
    created_at: DateTimeScalar
```

### PositiveInt Scalar

```python
@strawberry.scalar
class PositiveInt:
    @staticmethod
    def serialize(value: int) -> int:
        return value

    @staticmethod
    def parse_value(value: int) -> int:
        if value <= 0:
            raise ValueError("Must be a positive integer")
        return value
```

---

## 8. Federation Gateway <a name="federation"></a>

### Supergraph Configuration

```yaml
# supergraph-config.yaml
federation_version: 2
subgraphs:
  users:
    routing_url: http://user-service:4001/graphql
    schema:
      subgraph_url: http://user-service:4001/graphql
  posts:
    routing_url: http://post-service:4002/graphql
    schema:
      subgraph_url: http://post-service:4002/graphql
  comments:
    routing_url: http://comment-service:4003/graphql
    schema:
      subgraph_url: http://comment-service:4003/graphql
```

### User Subgraph

```python
# user-service/main.py
import strawberry
from strawberry.federation import Schema

@strawberry.federation.object(keys=("id",))
class User:
    id: int
    name: str
    email: str

@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: int) -> User:
        return await user_service.get_by_id(id)

    @strawberry.field
    async def users(self) -> list[User]:
        return await user_service.get_all()

schema = Schema(query=Query, enable_federation_2=True)
graphql_app = GraphQLRouter(schema)
```

### Post Subgraph (extending User)

```python
# post-service/main.py
import strawberry
from strawberry.federation import Schema

@strawberry.federation.object(keys=("id",))
class User:
    id: int

    @strawberry.federation.field(requires=["name"])
    async def posts(self) -> list["Post"]:
        return await post_service.get_by_author_id(self.id)

@strawberry.federation.object(keys=("id",))
class Post:
    id: int
    title: str
    content: str
    author_id: int

    @strawberry.field
    async def author(self) -> User:
        return User(id=self.author_id)

@strawberry.type
class Query:
    @strawberry.field
    async def post(self, id: int) -> Post:
        return await post_service.get_by_id(id)

schema = Schema(query=Query, enable_federation_2=True)
```

### Running the Gateway

```bash
# Using Apollo Router
apollo-router --supergraph supergraph.graphql

# Using Strawberry Gateway
pip install strawberry-graphql[fastapi]
python -m strawberry gateway --config supergraph-config.yaml
```

---

## Interview Questions

1. **How do GraphQL subscriptions work over WebSocket?**
The client opens a WebSocket connection and sends a `subscribe` message with the GraphQL subscription query. The server keeps the connection open and pushes data whenever the subscription event occurs. Strawberry uses the `graphql-transport-ws` protocol.

2. **How do you handle authentication in GraphQL?**
Use FastAPI's dependency injection or a custom `context_getter` to extract and validate the JWT token from the Authorization header. The authenticated user is stored in the GraphQL context and accessed in resolvers via `info.context["user"]`.

3. **How do you implement authorization in GraphQL?**
Use decorator-based permission classes, role-checking decorators (`@require_role`), or object-level authorization methods. Check permissions in resolvers before returning data. Use GraphQL's custom scalar types for role definitions.

4. **What is Relay-style pagination?**
Relay pagination uses a connection/edge/cursor pattern. Each page returns edges (containing nodes and cursors), pageInfo (hasNextPage, endCursor), and totalCount. Cursors are opaque strings (base64-encoded offsets). This enables efficient forward and backward pagination.

5. **How do you handle file uploads in GraphQL?**
GraphQL doesn't natively support file uploads. Use the `graphql-upload` specification where files are sent as multipart form data alongside the GraphQL query. Strawberry supports `UploadFile` type for handling file uploads in mutations.
