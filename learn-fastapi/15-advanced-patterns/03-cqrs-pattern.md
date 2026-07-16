# CQRS Pattern — Command Query Responsibility Segregation

## Table of Contents
1. [What is CQRS](#what-is)
2. [Separate Read/Write Models](#separate-models)
3. [Event-Driven CQRS](#event-driven)
4. [CQRS with FastAPI](#fastapi)
5. [When to Use CQRS](#when-to-use)
6. [Trade-offs](#trade-offs)

---

## What is CQRS <a name="what-is"></a>

CQRS separates read and write operations into different models. Commands (write operations) go through one model, queries (read operations) go through another. This allows independent optimization of reads and writes.

### Traditional CRUD vs CQRS

```
CRUD (single model):
  Client → Same Model → Database (same tables for read/write)

CQRS (separate models):
  Client → Command Model → Write Database → Event → Read Model → Read Database → Client
```

### Core Concepts

```
Command: An intent to change state (CreateUser, UpdateOrder, CancelPayment)
  - Mutates data
  - Returns void or confirmation
  - Can be validated before execution

Query: An intent to read data (GetUser, ListOrders, SearchProducts)
  - Does not mutate data
  - Returns data
  - Can be highly optimized for reads

Read Model: Optimized for querying (denormalized, materialized views)
Write Model: Optimized for writes (normalized, business rules)
```

---

## Separate Read/Write Models <a name="separate-models"></a>

### Command Side

```python
# app/commands/models.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

class CreateUserCommand(BaseModel):
    name: str
    email: EmailStr
    password: str

class UpdateUserCommand(BaseModel):
    user_id: int
    name: str | None = None
    email: EmailStr | None = None

class DeleteUserCommand(BaseModel):
    user_id: int
    reason: str | None = None

class CreateOrderCommand(BaseModel):
    user_id: int
    items: list[dict]
    shipping_address: str

class CancelOrderCommand(BaseModel):
    order_id: int
    reason: str
```

### Query Side

```python
# app/queries/models.py
from pydantic import BaseModel
from datetime import datetime

class UserReadModel(BaseModel):
    id: int
    name: str
    email: str
    order_count: int = 0
    total_spent: float = 0.0
    created_at: datetime

class UserListReadModel(BaseModel):
    users: list[UserReadModel]
    total: int
    page: int
    per_page: int

class OrderReadModel(BaseModel):
    id: int
    user_id: int
    user_name: str  # Denormalized from users table
    status: str
    total: float
    item_count: int
    created_at: datetime

class DashboardReadModel(BaseModel):
    total_users: int
    total_orders: int
    revenue: float
    orders_today: int
    active_users: int
```

### Separate Databases

```python
# Write side: normalized relational database
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class UserWrite(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

class OrderWrite(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), nullable=False)
    total = Column(Float, nullable=False)

# Read side: denormalized / document database
class UserRead(Base):
    __tablename__ = "users_read"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(255))
    order_count = Column(Integer, default=0)
    total_spent = Column(Float, default=0.0)

class OrderRead(Base):
    __tablename__ = "orders_read"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    user_name = Column(String(100))  # Denormalized
    status = Column(String(50))
    total = Column(Float)
    item_count = Column(Integer)
```

---

## Event-Driven CQRS <a name="event-driven"></a>

### Event Types

```python
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
import uuid

class EventType(str, Enum):
    USER_CREATED = "user.created"
    USER_UPDATED = "user.updated"
    USER_DELETED = "user.deleted"
    ORDER_CREATED = "order.created"
    ORDER_CANCELLED = "order.cancelled"

class DomainEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    aggregate_id: str
    data: dict
    metadata: dict = {}

class UserCreatedEvent(DomainEvent):
    event_type: EventType = EventType.USER_CREATED
    data: dict  # {"user_id": 1, "name": "Alice", "email": "alice@example.com"}

class OrderCreatedEvent(DomainEvent):
    event_type: EventType = EventType.ORDER_CREATED
    data: dict  # {"order_id": 100, "user_id": 1, "total": 99.99}
```

### Event Bus

```python
# app/core/events.py
from collections import defaultdict
from typing import Callable, Any
import asyncio

class EventBus:
    def __init__(self):
        self._handlers: dict[str, list[Callable]] = defaultdict(list)
        self._event_history: list[DomainEvent] = []

    def subscribe(self, event_type: EventType, handler: Callable):
        self._handlers[event_type.value].append(handler)

    def unsubscribe(self, event_type: EventType, handler: Callable):
        self._handlers[event_type.value].remove(handler)

    async def publish(self, event: DomainEvent):
        self._event_history.append(event)
        handlers = self._handlers.get(event.event_type.value, [])
        for handler in handlers:
            if asyncio.iscoroutinefunction(handler):
                await handler(event)
            else:
                handler(event)

    def get_event_history(self, event_type: EventType | None = None) -> list[DomainEvent]:
        if event_type:
            return [e for e in self._event_history if e.event_type == event_type]
        return self._event_history.copy()

event_bus = EventBus()
```

### Event Handlers (Read Model Projection)

```python
# app/projections/user_projection.py
async def on_user_created(event: UserCreatedEvent):
    """Update the read model when a user is created."""
    async with read_db_session() as session:
        user_read = UserRead(
            id=event.data["user_id"],
            name=event.data["name"],
            email=event.data["email"],
            order_count=0,
            total_spent=0.0,
        )
        session.add(user_read)
        await session.commit()

async def on_user_updated(event: UserUpdatedEvent):
    """Update the read model when a user is updated."""
    async with read_db_session() as session:
        user = await session.get(UserRead, event.data["user_id"])
        if user:
            for key, value in event.data.items():
                if key != "user_id" and hasattr(user, key):
                    setattr(user, key, value)
            await session.commit()

# Register handlers
event_bus.subscribe(EventType.USER_CREATED, on_user_created)
event_bus.subscribe(EventType.USER_UPDATED, on_user_updated)
```

---

## CQRS with FastAPI <a name="fastapi"></a>

### Command Handlers

```python
# app/commands/handlers.py
from sqlalchemy.ext.asyncio import AsyncSession

class UserCommandHandler:
    def __init__(self, db: AsyncSession, event_bus: EventBus):
        self.db = db
        self.event_bus = event_bus

    async def handle_create_user(self, command: CreateUserCommand) -> int:
        # Validate
        existing = await self.db.execute(
            select(UserWrite).where(UserWrite.email == command.email)
        )
        if existing.scalar_one_or_none():
            raise ValueError("Email already exists")

        # Create write model
        user = UserWrite(
            name=command.name,
            email=command.email,
            password_hash=hash_password(command.password),
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        # Publish event
        await self.event_bus.publish(UserCreatedEvent(
            aggregate_id=str(user.id),
            data={"user_id": user.id, "name": user.name, "email": user.email},
        ))

        return user.id

    async def handle_update_user(self, command: UpdateUserCommand) -> None:
        user = await self.db.get(UserWrite, command.user_id)
        if not user:
            raise ValueError("User not found")

        if command.name:
            user.name = command.name
        if command.email:
            user.email = command.email

        await self.db.commit()

        await self.event_bus.publish(UserUpdatedEvent(
            aggregate_id=str(command.user_id),
            data={"user_id": command.user_id, "name": command.name, "email": command.email},
        ))
```

### Query Handlers

```python
# app/queries/handlers.py
from sqlalchemy.ext.asyncio import AsyncSession

class UserQueryHandler:
    def __init__(self, read_db: AsyncSession):
        self.read_db = read_db

    async def get_user(self, user_id: int) -> UserReadModel:
        user = await self.read_db.get(UserRead, user_id)
        if not user:
            raise ValueError("User not found")
        return UserReadModel.model_validate(user)

    async def list_users(self, page: int = 1, per_page: int = 20) -> UserListReadModel:
        offset = (page - 1) * per_page
        result = await self.read_db.execute(
            select(UserRead).offset(offset).limit(per_page).order_by(UserRead.id)
        )
        users = result.scalars().all()

        count_result = await self.read_db.execute(select(func.count(UserRead.id)))
        total = count_result.scalar()

        return UserListReadModel(
            users=[UserReadModel.model_validate(u) for u in users],
            total=total,
            page=page,
            per_page=per_page,
        )
```

### FastAPI Endpoints

```python
# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from app.commands.handlers import UserCommandHandler
from app.queries.handlers import UserQueryHandler

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/", status_code=201)
async def create_user(
    command: CreateUserCommand,
    command_handler: UserCommandHandler = Depends(get_command_handler),
):
    try:
        user_id = await command_handler.handle_create_user(command)
        return {"user_id": user_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}")
async def get_user(
    user_id: int,
    query_handler: UserQueryHandler = Depends(get_query_handler),
):
    try:
        return await query_handler.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/")
async def list_users(
    page: int = 1,
    per_page: int = 20,
    query_handler: UserQueryHandler = Depends(get_query_handler),
):
    return await query_handler.list_users(page, per_page)
```

---

## When to Use CQRS <a name="when-to-use"></a>

### Good Fit

```
- Read and write workloads have different scaling requirements
- Read models need to be denormalized for performance
- Complex domain with many business rules on write side
- Audit logging is important (events provide natural audit trail)
- Multiple consumers need different views of the same data
- Event sourcing is being used alongside
- Teams can work independently on read and write sides
```

### Bad Fit

```
- Simple CRUD applications (overkill)
- Small applications with simple domains
- When consistency is critical and eventual consistency is unacceptable
- When team doesn't have experience with distributed systems
- When the overhead of maintaining two models isn't justified
```

---

## Trade-offs <a name="trade-offs"></a>

### Advantages

| Advantage | Description |
|-----------|-------------|
| Independent Scaling | Scale reads and writes separately |
| Optimized Models | Read models denormalized for query performance |
| Flexibility | Multiple read models for different use cases |
| Audit Trail | Events provide natural audit log |
| Performance | Read queries hit optimized read stores |
| Team Autonomy | Teams can work on read/write sides independently |

### Disadvantages

| Disadvantage | Description |
|--------------|-------------|
| Complexity | More code, more infrastructure, more deployment |
| Eventual Consistency | Reads may be slightly behind writes |
| Event Schema Evolution | Changing event schemas requires careful handling |
| Debugging | Harder to trace issues across read/write sides |
| Learning Curve | Team needs to understand distributed patterns |
| Infrastructure | May need multiple databases, message brokers |

### Mitigating Eventual Consistency

```python
# Option 1: Return write model immediately for the mutating client
@router.post("/users")
async def create_user(command: CreateUserCommand, ...):
    user_id = await command_handler.handle_create_user(command)
    # Wait for projection to be applied
    await event_bus.wait_for_projection(EventType.USER_CREATED, timeout=1.0)
    return {"user_id": user_id}

# Option 2: Use read-your-writes consistency
@router.get("/users/{user_id}")
async def get_user(user_id: int, request: Request):
    # Check if user recently modified their own data
    last_write = await cache.get(f"user:{user_id}:last_write")
    if last_write:
        # Read from write database
        return await read_from_write_db(user_id)
    # Normal read from read database
    return await query_handler.get_user(user_id)
```

---

## Interview Questions

1. **What is CQRS and when should you use it?**
CQRS separates read and write operations into different models. Use it when read and write workloads have different scaling needs, when read models need denormalization, or when multiple consumers need different data views. Don't use it for simple CRUD apps.

2. **How does CQRS handle eventual consistency?**
When a write occurs, it updates the write database and publishes an event. The read model is updated asynchronously by event handlers. During the propagation window, reads may return stale data. Mitigate with read-your-writes patterns, version vectors, or waiting for projection completion.

3. **What is the relationship between CQRS and event sourcing?**
They're independent but complementary. CQRS separates read/write models. Event sourcing stores state as a sequence of events rather than current state. CQRS naturally works with event sourcing because events can be used to build read model projections. But you can use CQRS without event sourcing and vice versa.

4. **How do you implement CQRS with FastAPI?**
Create separate command and query handlers. Commands go through a write database, queries through a read database. Use an event bus to publish events from write side. Register event handlers that update read model projections. Use dependency injection to inject the appropriate handlers.

5. **What are the infrastructure requirements for CQRS?**
At minimum: separate read and write databases (or separate schemas), an event bus (Redis, RabbitMQ, Kafka), and potentially a read-optimized store (Elasticsearch, Redis, materialized views). For production, add monitoring for projection lag, dead letter queues, and event replay capability.
