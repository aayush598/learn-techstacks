# Database Patterns with FastAPI

## Table of Contents

1. [Repository Pattern](#repository-pattern)
2. [Unit of Work](#unit-of-work)
3. [Active Record vs Data Mapper](#active-record-vs-data-mapper)
4. [Query Optimization](#query-optimization)
5. [Connection Pooling](#connection-pooling)
6. [Transaction Management](#transaction-management)
7. [Database Sharding Concepts](#database-sharding-concepts)
8. [Read Replicas](#read-replicas)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## Repository Pattern

The Repository Pattern abstracts data access behind a clean interface. It separates the "how" of data storage from the "what" of business logic.

### Abstract Interface

```python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional

T = TypeVar("T")

class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    async def get(self, id: int) -> Optional[T]:
        ...

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        ...

    @abstractmethod
    async def create(self, entity: T) -> T:
        ...

    @abstractmethod
    async def update(self, id: int, entity: T) -> Optional[T]:
        ...

    @abstractmethod
    async def delete(self, id: int) -> bool:
        ...

    @abstractmethod
    async def count(self) -> int:
        ...
```

### SQLAlchemy Repository

```python
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

class SQLAlchemyRepository(AbstractRepository[T]):
    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model

    async def get(self, id: int) -> Optional[T]:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def create(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def update(self, id: int, entity: T) -> Optional[T]:
        existing = await self.get(id)
        if not existing:
            return None
        for key, value in entity.__dict__.items():
            if not key.startswith("_"):
                setattr(existing, key, value)
        await self.session.commit()
        await self.session.refresh(existing)
        return existing

    async def delete(self, id: int) -> bool:
        entity = await self.get(id)
        if not entity:
            return False
        await self.session.delete(entity)
        await self.session.commit()
        return True

    async def count(self) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(self.model)
        )
        return result.scalar()
```

### Concrete Repositories

```python
class UserRepository(SQLAlchemyRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_active_users(self) -> list[User]:
        result = await self.session.execute(
            select(User).where(User.is_active == True)
        )
        return list(result.scalars().all())

class ItemRepository(SQLAlchemyRepository[Item]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Item)

    async def get_by_owner(self, owner_id: int) -> list[Item]:
        result = await self.session.execute(
            select(Item).where(Item.owner_id == owner_id)
        )
        return list(result.scalars().all())
```

### DI Integration

```python
def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_item_repo(db: AsyncSession = Depends(get_db)) -> ItemRepository:
    return ItemRepository(db)

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    repo: UserRepository = Depends(get_user_repo),
):
    user = await repo.get(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user
```

---

## Unit of Work

Unit of Work tracks all changes to objects and coordinates committing them as a single transaction.

### Implementation

```python
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession

class UnitOfWork:
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.users: UserRepository = None
        self.items: ItemRepository = None

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
        self.items = ItemRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def flush(self):
        await self.session.flush()
```

### Usage

```python
async def transfer_items(
    from_user_id: int,
    to_user_id: int,
    item_ids: list[int],
):
    async with UnitOfWork(session_factory) as uow:
        # All operations in one transaction
        for item_id in item_ids:
            item = await uow.items.get(item_id)
            if item.owner_id != from_user_id:
                raise ValueError("Not your item")
            item.owner_id = to_user_id
            await uow.items.update(item_id, item)

        # Auto-commits on successful exit
        # Auto-rollbacks on exception
```

### Unit of Work with Service Layer

```python
class OrderService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_order(self, user_id: int, items: list[dict]):
        async with self.uow:
            # Create order
            order = Order(user_id=user_id, total=sum(i["price"] for i in items))
            await self.uow.orders.create(order)

            # Update inventory
            for item_data in items:
                product = await self.uow.products.get(item_data["product_id"])
                product.stock -= item_data["quantity"]
                await self.uow.products.update(product.id, product)

            # Process payment
            payment = Payment(order_id=order.id, amount=order.total)
            await self.uow.payments.create(payment)

            return order
```

---

## Active Record vs Data Mapper

### Active Record

```python
# Active Record: Model knows about the database
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    # Model has database methods
    async def save(self, session):
        session.add(self)
        await session.commit()

    async def delete(self, session):
        await session.delete(self)
        await session.commit()

    @classmethod
    async def find_by_id(cls, session, id):
        return await session.get(cls, id)

# Usage
user = User(name="Alice")
await user.save(session)
found = await User.find_by_id(session, 1)
```

### Data Mapper

```python
# Data Mapper: Separate mapper between model and database
class User:
    def __init__(self, name: str):
        self.name = name

class UserRepository:
    def __init__(self, session):
        self.session = session

    async def save(self, user: User):
        self.session.add(user)
        await self.session.commit()

    async def find_by_id(self, id: int):
        return await self.session.get(User, id)

# Usage
user = User(name="Alice")
repo = UserRepository(session)
await repo.save(user)
found = await repo.find_by_id(1)
```

### Comparison

| Aspect | Active Record | Data Mapper |
|--------|--------------|-------------|
| Model | Has DB methods | Pure domain object |
| Testing | Hard to test (DB coupled) | Easy to test (mock repo) |
| Multiple DBs | Difficult | Easy (different repos) |
| Complexity | Lower | Higher |
| FastAPI/SQLModel | Active Record style | Repository pattern |

---

## Query Optimization

### Use Eager Loading

```python
# BAD: N+1
users = (await db.execute(select(User))).scalars().all()
for user in users:
    items = await db.run_sync(lambda: user.items)  # N queries!

# GOOD: Eager load
result = await db.execute(
    select(User).options(selectinload(User.items))
)
users = result.scalars().unique().all()
```

### Use Indexes

```python
class User(Base):
    __tablename__ = "users"

    id: int = mapped_column(primary_key=True)
    email: str = mapped_column(index=True)          # Single column index
    name: str = mapped_column(index=True)
    created_at: datetime = mapped_column(index=True)

    __table_args__ = (
        Index("ix_user_email_name", "email", "name"),  # Composite index
        Index("ix_user_active", "is_active", "created_at"),  # Partial index
    )
```

### Use Bulk Operations

```python
# BAD: Individual inserts
for data in large_dataset:
    user = User(**data)
    session.add(user)
    await session.commit()  # N commits!

# GOOD: Bulk insert
users = [User(**data) for data in large_dataset]
session.add_all(users)
await session.commit()  # 1 commit
```

### Use Subqueries Instead of Loading

```python
# BAD: Load all to count
users = await db.execute(select(User))
all_users = users.scalars().all()
active_count = sum(1 for u in all_users if u.is_active)

# GOOD: Database-level count
result = await db.execute(
    select(func.count(User.id)).where(User.is_active == True)
)
active_count = result.scalar()
```

### Use Window Functions

```python
from sqlalchemy import over, func

# Rank users by score
stmt = select(
    User.name,
    User.score,
    func.rank().over(order_by=User.score.desc()).label("rank"),
)
```

---

## Connection Pooling

### SQLAlchemy Pool Configuration

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool, NullPool

# Production: QueuePool with limits
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,        # Persistent connections
    max_overflow=10,     # Extra connections beyond pool_size
    pool_timeout=30,     # Seconds to wait for connection
    pool_recycle=1800,   # Recycle connections after 30 min
    pool_pre_ping=True,  # Verify connections before use
)

# Testing: NullPool (no pooling)
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
)
```

### Async Pool Configuration

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)
```

### Monitoring Pool Health

```python
@app.get("/health/pool")
async def pool_health(engine: AsyncEngine = Depends(get_engine)):
    pool = engine.pool
    return {
        "pool_size": pool.size(),
        "checked_out": pool.checkedout(),
        "checked_in": pool.checkedin(),
        "overflow": pool.overflow(),
    }
```

---

## Transaction Management

### Auto-Commit Pattern

```python
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()  # Auto-commit
        except Exception:
            await session.rollback()  # Auto-rollback
            raise
```

### Manual Transaction Control

```python
async def complex_operation(db: AsyncSession):
    async with db.begin():
        # All operations in one transaction
        user = User(name="Alice")
        db.add(user)
        # Auto-commits on success, auto-rollbacks on failure
```

### Savepoints

```python
async def with_savepoint(db: AsyncSession):
    async with db.begin():
        user = User(name="Alice")
        db.add(user)

        async with db.begin_nested():  # Savepoint
            item = Item(name="Widget", owner=user)
            db.add(item)
            # If this fails, only the savepoint is rolled back
```

### Distributed Transactions (Saga Pattern)

```python
class OrderSaga:
    def __init__(self, db: AsyncSession, payment_service, inventory_service):
        self.db = db
        self.payment = payment_service
        self.inventory = inventory_service
        self.compensations = []

    async def execute(self, order_data):
        try:
            # Step 1: Reserve inventory
            await self.inventory.reserve(order_data.items)
            self.compensations.append(
                lambda: self.inventory.release(order_data.items)
            )

            # Step 2: Process payment
            payment = await self.payment.charge(order_data.total)
            self.compensations.append(
                lambda: self.payment.refund(payment.id)
            )

            # Step 3: Create order
            order = Order(**order_data.dict())
            self.db.add(order)
            await self.db.commit()

            return order

        except Exception as e:
            # Compensate in reverse order
            for compensation in reversed(self.compensations):
                await compensation()
            raise
```

---

## Database Sharding Concepts

### What is Sharding?

Sharding splits a database horizontally across multiple servers. Each shard contains a subset of the data.

### Sharding Strategies

```python
# Hash-based sharding
def get_shard(user_id: int, num_shards: int = 4) -> int:
    return user_id % num_shards

# Range-based sharding
def get_shard_by_date(date: datetime) -> str:
    return f"shard_{date.year}_{date.month:02d}"

# Geographic sharding
def get_shard_by_region(region: str) -> str:
    region_map = {
        "us": "shard_us",
        "eu": "shard_eu",
        "asia": "shard_asia",
    }
    return region_map.get(region, "shard_default")
```

### Shard-Aware Repository

```python
class ShardedUserRepository:
    def __init__(self, shards: dict[str, AsyncSession]):
        self.shards = shards

    def _get_shard(self, user_id: int) -> AsyncSession:
        shard_key = f"shard_{user_id % len(self.shards)}"
        return self.shards[shard_key]

    async def get(self, user_id: int) -> User:
        session = self._get_shard(user_id)
        return await session.get(User, user_id)

    async def create(self, user: User) -> User:
        session = self._get_shard(user.id)
        session.add(user)
        await session.commit()
        return user
```

---

## Read Replicas

### Read/Write Splitting

```python
class DatabaseRouter:
    def __init__(self, write_engine, read_engines):
        self.write_engine = write_engine
        self.read_engines = read_engines
        self.counter = 0

    def get_write_session(self) -> AsyncSession:
        return AsyncSession(self.write_engine)

    def get_read_session(self) -> AsyncSession:
        # Round-robin across read replicas
        engine = self.read_engines[self.counter % len(self.read_engines)]
        self.counter += 1
        return AsyncSession(engine)

# Usage
router = DatabaseRouter(
    write_engine=write_engine,
    read_engines=[read_engine_1, read_engine_2],
)

async def get_read_db():
    session = router.get_read_session()
    try:
        yield session
    finally:
        await session.close()

async def get_write_db():
    session = router.get_write_session()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()

@app.get("/users/")
async def list_users(db: AsyncSession = Depends(get_read_db)):
    # Reads go to replicas
    result = await db.execute(select(User))
    return result.scalars().all()

@app.post("/users/")
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_write_db),
):
    # Writes go to primary
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    return db_user
```

---

## Best Practices

### 1. Use Repository Pattern for Complex Applications

```python
# Simple CRUD: Direct model access is fine
@app.get("/users/{id}")
async def get_user(id: int, db=Depends(get_db)):
    return await db.get(User, id)

# Complex business logic: Use repositories
@app.get("/users/{id}/dashboard")
async def get_dashboard(
    id: int,
    user_repo: UserRepository = Depends(get_user_repo),
    order_repo: OrderRepository = Depends(get_order_repo),
):
    user = await user_repo.get(id)
    orders = await order_repo.get_by_user(id)
    return build_dashboard(user, orders)
```

### 2. Keep Transactions Short

```python
# BAD: Long transaction
async def long_operation(db):
    async with db.begin():
        # Do lots of stuff
        # External API calls (don't do this in transactions!)
        await call_external_api()
        # More DB operations
        db.add(...)

# GOOD: Short transaction
async def short_operation(db):
    # External API call outside transaction
    api_result = await call_external_api()

    # Transaction only for DB operations
    async with db.begin():
        db.add(...)
```

### 3. Use Appropriate Isolation Levels

```python
# Read Committed (default)
# Suitable for most operations

# Repeatable Read
# For consistent reads within a transaction
await db.execute(
    text("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")
)

# Serializable
# For strict consistency (performance cost)
await db.execute(
    text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
)
```

---

## Interview Questions

### Q1: What is the Repository Pattern?
**Answer:** An abstraction layer between business logic and data access. It provides a clean interface for CRUD operations, making the data layer swappable and testable.

### Q2: What is Unit of Work?
**Answer:** A pattern that tracks all changes to objects and coordinates committing them as a single transaction. It ensures atomicity and provides rollback capabilities.

### Q3: What's the difference between Active Record and Data Mapper?
**Answer:** Active Record: model knows about the database (SQLModel style). Data Mapper: separate mapper between model and database (Repository pattern). Data Mapper is more testable and flexible.

### Q4: How do you optimize N+1 queries?
**Answer:** Use eager loading (selectinload, joinedload) to load relationships in the initial query. Or use subqueries/aggregation to get all needed data in fewer queries.

### Q5: What is connection pooling?
**Answer:** Maintaining a pool of reusable database connections. Avoids the overhead of creating new connections per request. Configure pool_size based on expected concurrency.

### Q6: When should you use read replicas?
**Answer:** When read traffic exceeds what a single database can handle. Split reads to replicas while keeping writes on the primary. Introduces replication lag — consider for consistency-sensitive reads.

### Q7: What is the Saga Pattern?
**Answer:** A distributed transaction pattern where each step has a compensating action. If any step fails, compensating actions undo previous steps. Used across multiple services.

### Q8: How do you handle database sharding?
**Answer:** Split data across multiple databases using a sharding key (hash, range, or geographic). Route queries to the correct shard. Handle cross-shard queries carefully.

---

## Summary

Database patterns in FastAPI applications scale with complexity. Start with direct model access for simple apps. Introduce Repository pattern as business logic grows. Use Unit of Work for complex transactions. Optimize queries with eager loading and indexes. Use connection pooling and read replicas for scalability.
