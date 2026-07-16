# SQLAlchemy Async with FastAPI

## Table of Contents

1. [SQLAlchemy Async Setup](#sqlalchemy-async-setup)
2. [AsyncEngine](#asyncengine)
3. [AsyncSession](#asyncsession)
4. [Async Session Lifecycle](#async-session-lifecycle)
5. [Async CRUD Operations](#async-crud-operations)
6. [Relationships with Async](#relationships-with-async)
7. [Lazy Loading vs Eager Loading](#lazy-loading-vs-eager-loading)
8. [N+1 Problem](#n1-problem)
9. [Query Building](#query-building)
10. [select(), where, join, subquery, exists, count](#select-where-join-subquery-exists-count)
11. [Best Practices](#best-practices)
12. [Interview Questions](#interview-questions)

---

## SQLAlchemy Async Setup

### Installation

```bash
pip install sqlalchemy[asyncio] asyncpg aiosqlite
# asyncpg — async PostgreSQL driver
# aiosqlite — async SQLite driver
# For MySQL: pip install aiomysql
```

### Project Structure

```
myapp/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py      # Engine, session, base
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/
│   │   └── ...
│   └── routers/
│       └── ...
└── requirements.txt
```

### Configuration

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/mydb"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 1800

    class Config:
        env_file = ".env"

settings = Settings()
```

### Database Module

```python
# database.py
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    pool_recycle=settings.DATABASE_POOL_RECYCLE,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
```

### Main Application

```python
# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import create_tables, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await create_tables()
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
```

---

## AsyncEngine

### Engine Creation

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

# Basic engine
engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")

# Engine with full configuration
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    echo=True,                    # Log SQL statements
    echo_pool=True,               # Log pool checkouts
    pool_size=20,                 # Persistent connections
    max_overflow=10,              # Extra connections beyond pool_size
    pool_timeout=30,              # Seconds to wait for a connection
    pool_recycle=1800,            # Recycle connections after 30 min
    pool_pre_ping=True,           # Verify connections before use
    connect_args={"server_settings": {"application_name": "myapp"}},
)

# Engine lifecycle
async def startup():
    # Engine created — pool initialized lazily

async def shutdown():
    # Dispose all pool connections
    await engine.dispose()
```

### Engine Properties

```python
# Check pool status
pool = engine.pool
print(f"Pool size: {pool.size()}")
print(f"Checked out: {pool.checkedout()}")
print(f"Checked in: {pool.checkedin()}")
print(f"Overflow: {pool.overflow()}")

# Execute raw SQL
async with engine.connect() as conn:
    result = await conn.execute(text("SELECT 1"))
    print(result.scalar())  # 1
```

---

## AsyncSession

### Session Creation

```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

# Using async_sessionmaker (recommended)
session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async with session_factory() as session:
    # Use session
    pass

# Direct creation
async with AsyncSession(engine) as session:
    pass
```

### Session Configuration

```python
session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Objects remain accessible after commit
    autocommit=False,         # Manual transaction control
    autoflush=False,          # Manual flush control
)
```

### Session Methods

```python
async def session_operations(session: AsyncSession):
    # Add a single object
    user = User(name="Alice", email="alice@example.com")
    session.add(user)

    # Add multiple objects
    session.add_all([user1, user2, user3])

    # Flush — send SQL to DB without committing
    await session.flush()

    # Refresh — reload object from DB
    await session.refresh(user)

    # Merge — attach detached object
    merged_user = await session.merge(user)

    # Delete
    await session.delete(user)

    # Commit — finalize transaction
    await session.commit()

    # Rollback — undo transaction
    await session.rollback()

    # Close session
    await session.close()
```

---

## Async Session Lifecycle

### Standard Lifecycle

```python
# 1. Session created
async with AsyncSessionLocal() as session:
    # 2. Transaction begins (automatically on first operation)
    user = User(name="Alice")
    session.add(user)

    # 3. Flush — SQL sent to DB
    await session.flush()

    # 4. Commit — transaction finalized
    await session.commit()

# 5. Session closed
```

### Transaction Management

```python
async def transaction_example(session: AsyncSession):
    # Manual transaction
    async with session.begin():
        # Auto-commit when block exits successfully
        # Auto-rollback on exception
        user = User(name="Alice")
        session.add(user)

    # Or manual control
    try:
        user = User(name="Bob")
        session.add(user)
        await session.commit()
    except Exception:
        await session.rollback()
        raise
```

### Session Per Request Pattern

```python
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# Or using begin():
async def get_db():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session
        # Auto-commits on success, auto-rollbacks on failure
```

### Long-Running Sessions

```python
# For background tasks or complex operations
async def long_operation():
    async with AsyncSessionLocal() as session:
        # Step 1
        result1 = await session.execute(select(Item).where(Item.active == True))
        items = result1.scalars().all()

        # Step 2 — may take time
        for item in items:
            item.status = "processed"

        # Step 3 — commit all changes
        await session.commit()
```

---

## Async CRUD Operations

### Create

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User, UserCreate

async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    user = User(**user_data.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def create_users_bulk(db: AsyncSession, users_data: list[UserCreate]) -> list[User]:
    users = [User(**data.model_dump()) for data in users_data]
    db.add_all(users)
    await db.commit()
    for user in users:
        await db.refresh(user)
    return users
```

### Read

```python
async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()

async def list_users(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> list[User]:
    result = await db.execute(
        select(User).offset(skip).limit(limit)
    )
    return list(result.scalars().all())
```

### Update

```python
async def update_user(
    db: AsyncSession,
    user_id: int,
    user_data: dict,
) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return None

    for key, value in user_data.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user

async def update_user_partial(
    db: AsyncSession,
    user_id: int,
    **kwargs,
) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user:
        for key, value in kwargs.items():
            if value is not None:
                setattr(user, key, value)
        await db.commit()
        await db.refresh(user)
    return user
```

### Delete

```python
async def delete_user(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return False
    await db.delete(user)
    await db.commit()
    return True

async def delete_users_bulk(db: AsyncSession, user_ids: list[int]) -> int:
    result = await db.execute(
        select(User).where(User.id.in_(user_ids))
    )
    users = result.scalars().all()
    for user in users:
        await db.delete(user)
    await db.commit()
    return len(users)
```

### Upsert (Insert or Update)

```python
from sqlalchemy.dialects.postgresql import insert

async def upsert_user(db: AsyncSession, user_data: dict) -> User:
    stmt = insert(User).values(**user_data)
    stmt = stmt.on_conflict_do_update(
        index_elements=["email"],
        set_={
            "name": user_data["name"],
            "updated_at": func.now(),
        },
    )
    await db.execute(stmt)
    await db.commit()

    result = await db.execute(
        select(User).where(User.email == user_data["email"])
    )
    return result.scalar_one()
```

---

## Relationships with Async

### Model Definitions

```python
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)

    # One-to-many: User has many Items
    items: Mapped[list["Item"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
    )

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Many-to-one: Item belongs to User
    owner: Mapped["User"] = relationship(back_populates="items")

    # Many-to-many: Item has many Tags
    tags: Mapped[list["Tag"]] = relationship(
        secondary="item_tags",
        back_populates="items",
    )

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    items: Mapped[list["Item"]] = relationship(
        secondary="item_tags",
        back_populates="tags",
    )

# Association table for many-to-many
from sqlalchemy import Table, Column, Integer, ForeignKey

item_tags = Table(
    "item_tags",
    Base.metadata,
    Column("item_id", Integer, ForeignKey("items.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)
```

### Loading Relationships

```python
# Lazy loading (default) — N+1 problem
async def get_users_lazy(db: AsyncSession):
    result = await db.execute(select(User))
    users = result.scalars().all()
    for user in users:
        # Each access triggers a new query!
        items = await db.run_sync(lambda: user.items)
    return users

# Eager loading with selectinload — separate IN query
async def get_users_eager_selectin(db: AsyncSession):
    from sqlalchemy.orm import selectinload

    result = await db.execute(
        select(User).options(selectinload(User.items))
    )
    users = result.scalars().all()
    # Items already loaded — no N+1
    return users

# Eager loading with joinedload — JOIN query
async def get_users_eager_join(db: AsyncSession):
    from sqlalchemy.orm import joinedload

    result = await db.execute(
        select(User).options(joinedload(User.items))
    )
    users = result.unique().scalars().all()
    # Items loaded via JOIN
    return users
```

---

## Lazy Loading vs Eager Loading

### Lazy Loading

```python
# Default behavior — loads relationship on access
class User(Base):
    items: Mapped[list["Item"]] = relationship(lazy="select")

# When you access user.items, SQLAlchemy runs:
# SELECT * FROM items WHERE items.owner_id = user.id

# Pros: Only loads when needed
# Cons: N+1 query problem
```

### Eager Loading Options

```python
from sqlalchemy.orm import (
    selectinload,    # Separate IN query (recommended for collections)
    joinedload,      # JOIN query (good for to-one relationships)
    subqueryload,    # Subquery (legacy, use selectinload)
    lazyload,        # Disable eager loading
    raiseload,       # Raise error if accessed (prevents N+1)
    noload,          # Don't load, return empty
)

# selectinload — best for collections
result = await db.execute(
    select(User).options(selectinload(User.items))
)

# joinedload — best for to-one relationships
result = await db.execute(
    select(Item).options(joinedload(Item.owner))
)

# Combined
result = await db.execute(
    select(User).options(
        selectinload(User.items).selectinload(Item.tags)
    )
)

# raiseload — prevent accidental lazy loading
result = await db.execute(
    select(User).options(raiseload(User.items))
)
# Accessing user.items raises an error
```

### Relationship Lazy Strategies

```python
class User(Base):
    # Lazy select (default)
    items: Mapped[list["Item"]] = relationship(lazy="select")

    # Lazy select with raise for unknown access
    items: Mapped[list["Item"]] = relationship(lazy="raise")

    # Subquery loading
    items: Mapped[list["Item"]] = relationship(lazy="subquery")

    # Dynamic loading (legacy — use .select() instead)
    items: Mapped[list["Item"]] = relationship(lazy="dynamic")
```

---

## N+1 Problem

### What is N+1?

```
Query 1: SELECT * FROM users                    → returns N users
Query 2: SELECT * FROM items WHERE user_id = 1  → for user 1
Query 3: SELECT * FROM items WHERE user_id = 2  → for user 2
...
Query N+1: SELECT * FROM items WHERE user_id = N → for user N

Total: 1 + N queries instead of 2
```

### Solutions

```python
# Problem: N+1
async def get_users_items_bad(db: AsyncSession):
    users = (await db.execute(select(User))).scalars().all()
    for user in users:
        print(user.items)  # N+1 queries!

# Solution 1: selectinload
async def get_users_items_selectin(db: AsyncSession):
    users = (
        await db.execute(
            select(User).options(selectinload(User.items))
        )
    ).scalars().unique().all()
    for user in users:
        print(user.items)  # No extra queries

# Solution 2: joinedload
async def get_users_items_joined(db: AsyncSession):
    users = (
        await db.execute(
            select(User).options(joinedload(User.items))
        )
    ).scalars().unique().all()
    for user in users:
        print(user.items)  # No extra queries

# Solution 3: raiseload (prevent N+1 at the code level)
async def get_users_raiseload(db: AsyncSession):
    users = (
        await db.execute(
            select(User).options(raiseload(User.items))
        )
    ).scalars().all()
    # user.items raises InvalidRequestError — forces you to load explicitly
```

### Detection

```python
# Enable SQL logging to see queries
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Shows all SQL queries
)

# Count queries using events
from sqlalchemy import event

query_count = 0

@event.listens_for.engine.sync_engine, "before_cursor_execute")
def count_queries(conn, cursor, statement, parameters, context, executemany):
    global query_count
    query_count += 1

# Reset per request
query_count = 0
```

---

## Query Building

### The `select()` Statement

```python
from sqlalchemy import select, and_, or_, not_, func

# Basic select
stmt = select(User)

# Select specific columns
stmt = select(User.id, User.name)

# With where clause
stmt = select(User).where(User.name == "Alice")

# With multiple conditions
stmt = select(User).where(
    and_(User.age >= 18, User.is_active == True)
)

# With OR
stmt = select(User).where(
    or_(User.role == "admin", User.role == "superadmin")
)

# With NOT
stmt = select(User).where(not_(User.is_banned))

# Order by
stmt = select(User).order_by(User.created_at.desc())

# Limit and offset
stmt = select(User).offset(10).limit(20)

# Distinct
stmt = select(User.name).distinct()

# Execute
result = await db.execute(stmt)
users = result.scalars().all()
```

### Where Clauses

```python
# Equality
stmt = select(User).where(User.name == "Alice")
stmt = select(User).where(User.name != "Bob")

# Comparison
stmt = select(User).where(User.age > 18)
stmt = select(User).where(User.age >= 18)
stmt = select(User).where(User.age < 65)
stmt = select(User).where(User.age <= 65)

# IN
stmt = select(User).where(User.id.in_([1, 2, 3]))
stmt = select(User).where(User.id.notin_([4, 5]))

# LIKE
stmt = select(User).where(User.name.like("%alice%"))
stmt = select(User).where(User.name.ilike("%alice%"))  # Case insensitive

# IS NULL / IS NOT NULL
stmt = select(User).where(User.deleted_at.is_(None))
stmt = select(User).where(User.deleted_at.isnot(None))

# BETWEEN
stmt = select(User).where(User.age.between(18, 65))

# CONTAINS (for arrays in PostgreSQL)
stmt = select(User).where(User.tags.contains(["python", "fastapi"]))

# Regex
stmt = select(User).where(User.name.regexp_match("^A.*"))
```

### Joins

```python
# Inner join
stmt = select(User, Item).join(Item, User.id == Item.owner_id)

# Left outer join
stmt = select(User, Item).outerjoin(Item, User.id == Item.owner_id)

# Explicit join with ON clause
stmt = select(User).join(
    Item,
    User.id == Item.owner_id,
    isouter=True,  # LEFT JOIN
)

# Multiple joins
stmt = (
    select(User, Item, Tag)
    .join(Item, User.id == Item.owner_id)
    .join(Tag, Item.tags)
)

# Self-join
stmt = select(User).join(
    User,
    User.manager_id == User.id,
    aliased=True,
)
```

### Subqueries

```python
# Scalar subquery
subq = select(func.avg(Item.price)).scalar_subquery()
stmt = select(Item).where(Item.price > subq)

# FROM subquery
subq = (
    select(User.id, User.name)
    .where(User.is_active == True)
    .subquery()
)
stmt = select(subq).where(subq.c.name == "Alice")

# Correlated subquery
subq = (
    select(func.count(Item.id))
    .where(Item.owner_id == User.id)
    .correlate(User)
    .scalar_subquery()
)
stmt = select(User.name, subq.label("item_count"))
```

### Exists and Count

```python
from sqlalchemy import exists, func

# EXISTS subquery
stmt = select(User).where(
    exists().where(Item.owner_id == User.id)
)

# NOT EXISTS
stmt = select(User).where(
    not_(exists().where(Item.owner_id == User.id))
)

# COUNT
stmt = select(func.count(User.id)).where(User.is_active == True)
result = await db.execute(stmt)
count = result.scalar()  # Returns integer

# COUNT with group by
stmt = (
    select(User.role, func.count(User.id).label("count"))
    .group_by(User.role)
)
result = await db.execute(stmt)
for role, count in result.all():
    print(f"{role}: {count}")

# HAVING
stmt = (
    select(User.role, func.count(User.id).label("count"))
    .group_by(User.role)
    .having(func.count(User.id) > 5)
)

# COUNT with subquery
subq = select(func.count(Item.id)).where(Item.owner_id == User.id).scalar_subquery()
stmt = select(User.name, subq.label("item_count"))
```

---

## Best Practices

### 1. Always Use Eager Loading in Queries

```python
# BAD: N+1
users = (await db.execute(select(User))).scalars().all()

# GOOD: Eager load relationships
users = (
    await db.execute(
        select(User).options(selectinload(User.items))
    )
).scalars().unique().all()
```

### 2. Useexpire_on_commit=False

```python
# BAD: Objects expire after commit
async with AsyncSessionLocal() as session:
    user = User(name="Alice")
    session.add(user)
    await session.commit()
    print(user.id)  # Triggers lazy load — may fail

# GOOD: Objects remain accessible
session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
```

### 3. Handle Commits Explicitly

```python
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### 4. Use `select()` Instead of Legacy `query()`

```python
# BAD (legacy)
users = db.query(User).filter(User.name == "Alice").all()

# GOOD (modern)
result = await db.execute(select(User).where(User.name == "Alice"))
users = result.scalars().all()
```

### 5. Batch Operations

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

---

## Interview Questions

### Q1: Why use async SQLAlchemy with FastAPI?
**Answer:** Async SQLAlchemy prevents database operations from blocking the event loop, allowing FastAPI to handle other requests while waiting for database responses. This significantly improves throughput for I/O-bound applications.

### Q2: What is the difference between `AsyncEngine` and `Engine`?
**Answer:** `AsyncEngine` uses async drivers (asyncpg, aiosqlite) and can execute queries with `await`. `Engine` uses synchronous drivers (psycopg2, sqlite3) and blocks the event loop. FastAPI should use `AsyncEngine` for non-blocking operation.

### Q3: How do you prevent the N+1 problem in async SQLAlchemy?
**Answer:** Use eager loading options: `selectinload()` for collections (uses IN query), `joinedload()` for to-one relationships (uses JOIN). Apply them via `.options()` on the select statement.

### Q4: What does `expire_on_commit=False` do?
**Answer:** By default, SQLAlchemy expires (invalidates) all attributes of a persisted object after commit. Accessing them triggers a lazy reload query. `expire_on_commit=False` keeps objects usable after commit without additional queries.

### Q5: How do you handle transactions in async SQLAlchemy?
**Answer:** Use `async with session.begin()` for automatic commit/rollback. Or manually call `await session.commit()` and `await session.rollback()` in try/except blocks.

### Q6: What is the difference between `flush()` and `commit()`?
**Answer:** `flush()` sends pending SQL to the database within the current transaction but doesn't finalize it. `commit()` commits the transaction, making changes permanent. You can rollback after flush but not after commit.

### Q7: How do you perform bulk inserts efficiently?
**Answer:** Use `session.add_all()` for multiple objects, or `insert().on_conflict_do_update()` for upserts. For maximum performance, use `connection.execute()` with bulk insert statements.

### Q8: What is `selectinload` vs `joinedload`?
**Answer:** `selectinload` issues a separate `IN` query to load related objects (2-3 queries total). `joinedload` uses a `JOIN` (1 query but may duplicate parent data). Use `selectinload` for collections, `joinedload` for to-one relationships.

---

## Summary

Async SQLAlchemy with FastAPI provides a fully non-blocking database layer. Key concepts: use `AsyncEngine` and `AsyncSession`, handle transactions explicitly, use eager loading to prevent N+1, and always manage sessions with proper cleanup in yield dependencies.
