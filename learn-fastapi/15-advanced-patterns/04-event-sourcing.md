# Event Sourcing Pattern

## Table of Contents
1. [What is Event Sourcing](#what-is)
2. [Event Store](#event-store)
3. [Aggregate Roots](#aggregates)
4. [Event Replay](#replay)
5. [Snapshots](#snapshots)
6. [Eventual Consistency](#consistency)
7. [Event Sourcing with FastAPI](#fastapi)
8. [Event-Driven Architecture](#event-driven)

---

## What is Event Sourcing <a name="what-is"></a>

Event sourcing stores every change to application state as an immutable event. Instead of storing current state, you store the sequence of events that led to the current state. The current state is derived by replaying events.

### Traditional vs Event Sourcing

```
Traditional (Current State):
  Database stores: {"id": 1, "name": "Alice", "balance": 500}
  When deposit $200: UPDATE users SET balance = 700 WHERE id = 1
  Previous state is lost

Event Sourcing:
  Event store stores:
    1. UserCreated: {id: 1, name: "Alice", initial_balance: 0}
    2. MoneyDeposited: {id: 1, amount: 500}
    3. MoneyDeposited: {id: 1, amount: 200}
  Current state: replay events → balance = 700
  Complete history is preserved
```

### Core Concepts

```
Event: An immutable fact that happened in the past
  - UserCreated, MoneyDeposited, OrderPlaced
  - Contains: event type, data, timestamp, version

Aggregate: A cluster of domain objects treated as a single unit
  - User aggregate, Order aggregate, Account aggregate
  - Each aggregate has an event stream

Event Store: Persistent storage for events
  - Append-only log
  - Events are never modified or deleted

Projection: Derived view built from events
  - User summary, order history, analytics dashboard
  - Can be rebuilt from events
```

---

## Event Store <a name="event-store"></a>

### Event Schema

```python
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Any
import uuid

class EventType(str, Enum):
    USER_CREATED = "user.created"
    USER_EMAIL_CHANGED = "user.email_changed"
    USER_DEACTIVATED = "user.deactivated"
    ACCOUNT_FUNDED = "account.funded"
    ACCOUNT_WITHDRAWN = "account.withdrawn"
    ORDER_PLACED = "order.placed"
    ORDER_SHIPPED = "order.shipped"
    ORDER_DELIVERED = "order.delivered"

class StoredEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType
    aggregate_type: str       # "user", "order", "account"
    aggregate_id: str         # ID of the aggregate
    version: int              # Version of the aggregate after this event
    data: dict[str, Any]      # Event payload
    metadata: dict[str, Any] = {}  # Correlation ID, causation ID, etc.
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class EventPayload(BaseModel):
    """Specific event payloads"""
    class UserCreated(BaseModel):
        user_id: int
        name: str
        email: str

    class MoneyDeposited(BaseModel):
        account_id: int
        amount: float
        balance_after: float

    class OrderPlaced(BaseModel):
        order_id: int
        user_id: int
        items: list[dict]
        total: float
```

### Event Store Implementation

```python
# app/events/store.py
from sqlalchemy import Column, String, Integer, DateTime, JSON, Text
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import json

class EventStoreEntry(Base):
    __tablename__ = "event_store"

    event_id = Column(String(36), primary_key=True)
    event_type = Column(String(100), nullable=False, index=True)
    aggregate_type = Column(String(50), nullable=False, index=True)
    aggregate_id = Column(String(36), nullable=False, index=True)
    version = Column(Integer, nullable=False)
    data = Column(JSON, nullable=False)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (
        # Ensure unique version per aggregate
        UniqueConstraint("aggregate_id", "version", name="uq_aggregate_version"),
    )

class EventStore:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def append(self, event: StoredEvent) -> None:
        entry = EventStoreEntry(
            event_id=event.event_id,
            event_type=event.event_type.value,
            aggregate_type=event.aggregate_type,
            aggregate_id=event.aggregate_id,
            version=event.version,
            data=event.data,
            metadata=event.metadata,
            created_at=event.timestamp,
        )
        self.session.add(entry)
        await self.session.commit()

    async def get_events(
        self,
        aggregate_id: str,
        after_version: int = 0,
    ) -> list[StoredEvent]:
        result = await self.session.execute(
            select(EventStoreEntry)
            .where(EventStoreEntry.aggregate_id == aggregate_id)
            .where(EventStoreEntry.version > after_version)
            .order_by(EventStoreEntry.version)
        )
        rows = result.scalars().all()
        return [self._to_event(row) for row in rows]

    async def get_all_events(
        self,
        event_type: EventType | None = None,
        after_timestamp: datetime | None = None,
        limit: int = 1000,
    ) -> list[StoredEvent]:
        query = select(EventStoreEntry).order_by(EventStoreEntry.created_at)
        if event_type:
            query = query.where(EventStoreEntry.event_type == event_type.value)
        if after_timestamp:
            query = query.where(EventStoreEntry.created_at > after_timestamp)
        query = query.limit(limit)
        result = await self.session.execute(query)
        return [self._to_event(row) for row in result.scalars().all()]

    async def get_latest_version(self, aggregate_id: str) -> int:
        result = await self.session.execute(
            select(func.max(EventStoreEntry.version))
            .where(EventStoreEntry.aggregate_id == aggregate_id)
        )
        return result.scalar() or 0

    def _to_event(self, row: EventStoreEntry) -> StoredEvent:
        return StoredEvent(
            event_id=row.event_id,
            event_type=EventType(row.event_type),
            aggregate_type=row.aggregate_type,
            aggregate_id=row.aggregate_id,
            version=row.version,
            data=row.data,
            metadata=row.metadata,
            timestamp=row.created_at,
        )
```

---

## Aggregate Roots <a name="aggregates"></a>

Aggregates are consistency boundaries. They enforce business rules and produce events.

### Aggregate Base

```python
# app/events/aggregate.py
from typing import Any

class AggregateRoot:
    def __init__(self, aggregate_id: str):
        self.aggregate_id = aggregate_id
        self.version = 0
        self._events: list[StoredEvent] = []
        self._uncommitted_events: list[StoredEvent] = []

    def _apply(self, event_type: EventType, data: dict) -> None:
        """Apply an event and add to uncommitted events."""
        self.version += 1
        event = StoredEvent(
            event_type=event_type,
            aggregate_type=self.__class__.__name__,
            aggregate_id=self.aggregate_id,
            version=self.version,
            data=data,
        )
        self._events.append(event)
        self._uncommitted_events.append(event)

    def get_uncommitted_events(self) -> list[StoredEvent]:
        return self._uncommitted_events.copy()

    def clear_uncommitted_events(self) -> None:
        self._uncommitted_events.clear()

    def load_from_history(self, events: list[StoredEvent]) -> None:
        """Rebuild state from event history."""
        for event in events:
            self._apply_event(event)
            self.version = event.version

    def _apply_event(self, event: StoredEvent) -> None:
        """Apply a single event (to be overridden by subclasses)."""
        handler = getattr(self, f"_on_{event.event_type.value.replace('.', '_')}", None)
        if handler:
            handler(event.data)
```

### User Aggregate

```python
# app/aggregates/user.py
from app.events.aggregate import AggregateRoot

class UserAggregate(AggregateRoot):
    def __init__(self, user_id: int):
        super().__init__(str(user_id))
        self.user_id = user_id
        self.name: str = ""
        self.email: str = ""
        self.is_active: bool = True

    @classmethod
    def create(cls, user_id: int, name: str, email: str) -> "UserAggregate":
        user = cls(user_id)
        user._apply(EventType.USER_CREATED, {
            "user_id": user_id,
            "name": name,
            "email": email,
        })
        return user

    def change_email(self, new_email: str) -> None:
        if not self.is_active:
            raise ValueError("Cannot change email of inactive user")
        self._apply(EventType.USER_EMAIL_CHANGED, {
            "user_id": self.user_id,
            "old_email": self.email,
            "new_email": new_email,
        })

    def deactivate(self) -> None:
        if not self.is_active:
            raise ValueError("User already inactive")
        self._apply(EventType.USER_DEACTIVATED, {
            "user_id": self.user_id,
        })

    # Event handlers (apply events to state)
    def _on_user_created(self, data: dict) -> None:
        self.name = data["name"]
        self.email = data["email"]
        self.is_active = True

    def _on_user_email_changed(self, data: dict) -> None:
        self.email = data["new_email"]

    def _on_user_deactivated(self, data: dict) -> None:
        self.is_active = False
```

### Bank Account Aggregate

```python
class AccountAggregate(AggregateRoot):
    def __init__(self, account_id: int):
        super().__init__(str(account_id))
        self.account_id = account_id
        self.balance: float = 0.0
        self.is_frozen: bool = False

    @classmethod
    def create(cls, account_id: int, initial_balance: float = 0) -> "AccountAggregate":
        account = cls(account_id)
        account._apply(EventType.ACCOUNT_CREATED, {
            "account_id": account_id,
            "initial_balance": initial_balance,
        })
        return account

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        if self.is_frozen:
            raise ValueError("Account is frozen")
        new_balance = self.balance + amount
        self._apply(EventType.ACCOUNT_FUNDED, {
            "account_id": self.account_id,
            "amount": amount,
            "balance_after": new_balance,
        })

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.is_frozen:
            raise ValueError("Account is frozen")
        if self.balance < amount:
            raise ValueError("Insufficient funds")
        new_balance = self.balance - amount
        self._apply(EventType.ACCOUNT_WITHDRAWN, {
            "account_id": self.account_id,
            "amount": amount,
            "balance_after": new_balance,
        })

    def _on_account_created(self, data: dict) -> None:
        self.balance = data["initial_balance"]

    def _on_account_funded(self, data: dict) -> None:
        self.balance = data["balance_after"]

    def _on_account_withdrawn(self, data: dict) -> None:
        self.balance = data["balance_after"]
```

---

## Event Replay <a name="replay"></a>

### Rebuilding Aggregate State

```python
class EventRepository:
    def __init__(self, event_store: EventStore):
        self.event_store = event_store

    async def load(self, aggregate_class, aggregate_id: str) -> AggregateRoot:
        aggregate = aggregate_class.__init__.__self__
        events = await self.event_store.get_events(aggregate_id)
        if not events:
            raise ValueError(f"Aggregate {aggregate_id} not found")
        aggregate.load_from_history(events)
        return aggregate

    async def save(self, aggregate: AggregateRoot) -> None:
        events = aggregate.get_uncommitted_events()
        for event in events:
            await self.event_store.append(event)
        aggregate.clear_uncommitted_events()

# Usage
async def handle_deposit(account_id: int, amount: float):
    repo = EventRepository(event_store)
    account = await repo.load(AccountAggregate, str(account_id))
    account.deposit(amount)
    await repo.save(account)
    return account.balance
```

### Rebuilding Projections

```python
async def rebuild_user_projection():
    """Rebuild the user read model from all events."""
    async with read_db_session() as session:
        # Clear existing projection
        await session.execute(delete(UserReadModel))

        # Get all user events
        events = await event_store.get_all_events(
            event_type=None,  # All event types
            limit=100000,
        )

        # Apply events in order
        for event in events:
            if event.event_type == EventType.USER_CREATED:
                user = UserReadModel(
                    id=event.data["user_id"],
                    name=event.data["name"],
                    email=event.data["email"],
                )
                session.add(user)
            elif event.event_type == EventType.USER_EMAIL_CHANGED:
                user = await session.get(UserReadModel, event.data["user_id"])
                if user:
                    user.email = event.data["new_email"]
            elif event.event_type == EventType.USER_DEACTIVATED:
                user = await session.get(UserReadModel, event.data["user_id"])
                if user:
                    user.is_active = False

        await session.commit()
```

---

## Snapshots <a name="snapshots"></a>

Snapshots capture aggregate state at a point in time, avoiding replaying all events.

```python
# app/events/snapshot.py
class Snapshot(BaseModel):
    aggregate_id: str
    aggregate_type: str
    version: int
    state: dict
    timestamp: datetime

class SnapshotStore:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, aggregate: AggregateRoot) -> None:
        snapshot = Snapshot(
            aggregate_id=aggregate.aggregate_id,
            aggregate_type=aggregate.__class__.__name__,
            version=aggregate.version,
            state=aggregate.__dict__,
            timestamp=datetime.utcnow(),
        )
        self.session.add(SnapshotEntry(**snapshot.model_dump()))
        await self.session.commit()

    async def load(self, aggregate_id: str) -> Snapshot | None:
        result = await self.session.execute(
            select(SnapshotEntry)
            .where(SnapshotEntry.aggregate_id == aggregate_id)
            .order_by(SnapshotEntry.version.desc())
            .limit(1)
        )
        entry = result.scalar_one_or_none()
        if entry:
            return Snapshot(**entry.__dict__)
        return None

class SnapshotRepository:
    SNAPSHOT_INTERVAL = 100  # Create snapshot every 100 events

    def __init__(self, event_store: EventStore, snapshot_store: SnapshotStore):
        self.event_store = event_store
        self.snapshot_store = snapshot_store

    async def load(self, aggregate_class, aggregate_id: str) -> AggregateRoot:
        # Try loading from snapshot first
        snapshot = await self.snapshot_store.load(aggregate_id)
        if snapshot:
            aggregate = aggregate_class.__dict__(aggregate_id)
            aggregate.__dict__.update(snapshot.state)
            aggregate.version = snapshot.version

            # Load events after snapshot
            events = await self.event_store.get_events(
                aggregate_id, after_version=snapshot.version
            )
            aggregate.load_from_history(events)
            return aggregate

        # No snapshot, load all events
        aggregate = aggregate_class(aggregate_id)
        events = await self.event_store.get_events(aggregate_id)
        if events:
            aggregate.load_from_history(events)
        return aggregate

    async def save(self, aggregate: AggregateRoot) -> None:
        await self.event_store.save_all(aggregate.get_uncommitted_events())
        aggregate.clear_uncommitted_events()

        # Create snapshot periodically
        if aggregate.version % self.SNAPSHOT_INTERVAL == 0:
            await self.snapshot_store.save(aggregate)
```

---

## Eventual Consistency <a name="consistency"></a>

```python
# Read model may lag behind write model
# Handle this in the API layer

class ConsistencyStrategy:
    def __init__(self, event_bus: EventBus, read_store: ReadStore):
        self.event_bus = event_bus
        self.read_store = read_store
        self._pending_projections: dict[str, asyncio.Event] = {}

    async def wait_for_projection(
        self, aggregate_id: str, timeout: float = 5.0
    ) -> bool:
        """Wait until the read model is up to date."""
        event = asyncio.Event()
        self._pending_projections[aggregate_id] = event
        try:
            await asyncio.wait_for(event.wait(), timeout=timeout)
            return True
        except asyncio.TimeoutError:
            return False

    def on_projection_applied(self, aggregate_id: str) -> None:
        if aggregate_id in self._pending_projections:
            self._pending_projections[aggregate_id].set()
            del self._pending_projections[aggregate_id]

# Use in endpoint
@router.post("/accounts/{account_id}/deposit")
async def deposit(
    account_id: int,
    amount: float,
    consistency: ConsistencyStrategy = Depends(),
):
    # Execute command
    account = await repo.load(AccountAggregate, str(account_id))
    account.deposit(amount)
    await repo.save(account)

    # Optionally wait for projection
    await consistency.wait_for_projection(str(account_id))

    return {"balance": account.balance}
```

---

## Event Sourcing with FastAPI <a name="fastapi"></a>

### Complete Application

```python
# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize event store
    app.state.event_store = EventStore(db_session)
    app.state.event_bus = EventBus()
    app.state.snapshot_store = SnapshotStore(db_session)
    app.state.repository = SnapshotRepository(
        app.state.event_store, app.state.snapshot_store
    )

    # Register event handlers
    register_projections(app.state.event_bus)

    yield

    # Cleanup
    await app.state.event_store.close()

app = FastAPI(title="Event Sourced API", lifespan=lifespan)

@app.post("/api/users", status_code=201)
async def create_user(
    name: str,
    email: str,
    request: Request,
):
    user_id = generate_user_id()
    user = UserAggregate.create(user_id, name, email)
    await request.app.state.repository.save(user)

    return {"user_id": user_id, "version": user.version}

@app.get("/api/users/{user_id}")
async def get_user(user_id: int, request: Request):
    user = await request.app.state.repository.load(
        UserAggregate, str(user_id)
    )
    return {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "version": user.version,
    }

@app.post("/api/accounts/{account_id}/deposit")
async def deposit(
    account_id: int,
    amount: float,
    request: Request,
):
    account = await request.app.state.repository.load(
        AccountAggregate, str(account_id)
    )
    account.deposit(amount)
    await request.app.state.repository.save(account)
    return {"balance": account.balance, "version": account.version}

@app.get("/api/events/{aggregate_id}")
async def get_events(
    aggregate_id: str,
    request: Request,
):
    events = await request.app.state.event_store.get_events(aggregate_id)
    return {"events": events, "count": len(events)}
```

---

## Event-Driven Architecture <a name="event-driven"></a>

### Producers and Consumers

```python
# Producer: publishes events when commands are processed
async def publish_events(events: list[StoredEvent]):
    for event in events:
        await event_bus.publish(event)
        await message_broker.publish("events", event.model_dump_json())

# Consumer: listens for events and updates projections
async def consume_events():
    while True:
        message = await message_broker.consume("events")
        event = StoredEvent.model_validate_json(message.body)
        await handle_event(event)
        await message_broker.ack(message)

# Multiple consumers can process the same event
# - Projection updater (updates read database)
# - Notification service (sends emails/SMS)
# - Analytics service (updates analytics)
# - Search indexer (updates search index)
```

### Dead Letter Queue

```python
class DeadLetterQueue:
    def __init__(self, broker):
        self.broker = broker

    async def send_to_dlq(self, event: StoredEvent, error: Exception):
        dlq_message = {
            "event": event.model_dump(),
            "error": str(error),
            "timestamp": datetime.utcnow().isoformat(),
            "retry_count": 0,
        }
        await self.broker.publish("dead_letter_queue", json.dumps(dlq_message))

    async def retry_from_dlq(self):
        message = await self.broker.consume("dead_letter_queue")
        if message:
            data = json.loads(message.body)
            event = StoredEvent(**data["event"])
            try:
                await handle_event(event)
                await self.broker.ack(message)
            except Exception as e:
                data["retry_count"] += 1
                if data["retry_count"] < 3:
                    await self.broker.publish("dead_letter_queue", json.dumps(data))
                await self.broker.ack(message)
```

---

## Interview Questions

1. **What is event sourcing and how does it differ from CRUD?**
Event sourcing stores every state change as an immutable event, while CRUD overwrites current state. Event sourcing preserves complete history, enables temporal queries, and supports event replay. CRUD is simpler but loses history.

2. **What is an aggregate root in event sourcing?**
An aggregate root is a consistency boundary that groups related entities. It enforces business rules, produces events, and maintains its own version. Events are applied to the aggregate to build its current state. Examples: UserAggregate, OrderAggregate.

3. **How do you handle event schema evolution?**
Use upcasters to transform old event schemas to new ones. Add optional fields with defaults. Never remove or rename fields. Use versioned event types. For breaking changes, create new event types rather than modifying existing ones.

4. **What are snapshots and when should you use them?**
Snapshots capture aggregate state at a point in time. Use them when aggregates have many events (hundreds+) to avoid replaying all events on every load. Create snapshots periodically (e.g., every 100 events) and load from snapshot + subsequent events.

5. **How does event sourcing support audit trails?**
Every state change is recorded as an immutable event with timestamp, user info, and metadata. You can reconstruct the exact state at any point in time. This provides a complete audit trail without additional logging infrastructure.
