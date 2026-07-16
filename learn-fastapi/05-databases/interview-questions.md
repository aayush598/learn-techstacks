# Database Interview Questions with FastAPI

## 30+ Questions for Database Mastery

---

## SQLAlchemy Async

### Q1: Why use async SQLAlchemy with FastAPI?

**Answer:** Async SQLAlchemy prevents database operations from blocking the event loop. While one request waits for a DB response, FastAPI can handle other requests. This significantly improves throughput for I/O-bound applications.

```python
# Sync — blocks event loop
def get_users():
    db = SessionLocal()
    return db.query(User).all()  # Blocks!

# Async — non-blocking
async def get_users():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User))
        return result.scalars().all()  # Non-blocking
```

**When to use async:**
- High-concurrency applications (hundreds of simultaneous requests)
- Applications that call multiple databases or external services
- Microservices that need to handle many connections

**When sync is fine:**
- Low-traffic applications
- Background scripts
- When using an ORM heavily with complex relationships

---

### Q2: What is the difference between `AsyncEngine` and `Engine`?

**Answer:**

| Aspect | `Engine` | `AsyncEngine` |
|--------|----------|---------------|
| Driver | psycopg2, sqlite3 | asyncpg, aiosqlite |
| Execution | Blocking | Non-blocking |
| Session | `Session` | `AsyncSession` |
| Query | `session.execute()` | `await session.execute()` |
| Thread | Main thread | Event loop |

```python
# Sync Engine
from sqlalchemy import create_engine
engine = create_engine("postgresql://user:pass@localhost/db")

# Async Engine
from sqlalchemy.ext.asyncio import create_async_engine
engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
```

---

### Q3: How does `expire_on_commit=False` work?

**Answer:** By default, SQLAlchemy expires all object attributes after commit. Accessing them triggers a lazy reload query. In async code, lazy loading is not supported (raises error).

```python
# Without expire_on_commit=False
async def get_user():
    async with AsyncSessionLocal() as db:
        user = User(name="Alice")
        db.add(user)
        await db.commit()
        print(user.id)  # Error! Attribute expired, lazy load not supported

# With expire_on_commit=False
async def get_user():
    async with AsyncSessionLocal() as db:
        user = User(name="Alice")
        db.add(user)
        await db.commit()
        print(user.id)  # Works! Attribute still available
```

---

### Q4: What is the difference between `flush()` and `commit()`?

**Answer:**

```python
async def transfer_funds():
    async with AsyncSessionLocal() as session:
        # Flush — sends SQL but doesn't commit
        sender.balance -= 100
        receiver.balance += 100
        await session.flush()
        # SQL is sent: UPDATE accounts SET balance = ... WHERE id = ...
        # But transaction is NOT committed yet
        # You can still rollback

        # Commit — finalizes the transaction
        await session.commit()
        # Transaction is committed — can no longer rollback
```

**Key difference:** After `flush()`, you can still rollback. After `commit()`, changes are permanent.

---

### Q5: How do you prevent the N+1 problem?

**Answer:**

```python
# Problem: N+1 queries
users = (await db.execute(select(User))).scalars().all()
for user in users:
    items = await db.run_sync(lambda: user.items)  # N queries!

# Solution 1: selectinload (recommended for collections)
result = await db.execute(
    select(User).options(selectinload(User.items))
)
users = result.scalars().unique().all()

# Solution 2: joinedload (good for to-one)
result = await db.execute(
    select(Item).options(joinedload(Item.owner))
)

# Solution 3: raiseload (prevent N+1 at code level)
result = await db.execute(
    select(User).options(raiseload(User.items))
)
```

**Detection:** Enable `echo=True` on engine to see all queries.

---

### Q6: What are the advantages of `select()` over `query()`?

**Answer:** `select()` is the SQLAlchemy 2.0 API:

```python
# Legacy (1.x)
users = db.query(User).filter(User.name == "Alice").all()

# Modern (2.0)
result = await db.execute(select(User).where(User.name == "Alice"))
users = result.scalars().all()
```

**Advantages:**
- Explicit, Pythonic API
- Works with both sync and async
- Better type checking
- Composable (can build queries step by step)
- Supports subqueries and CTEs more naturally

---

### Q7: How do you handle bulk inserts efficiently?

**Answer:**

```python
# Method 1: add_all
users = [User(name=f"User {i}") for i in range(1000)]
session.add_all(users)
await session.commit()

# Method 2: Core insert (fastest)
from sqlalchemy import insert
await session.execute(
    insert(User),
    [{"name": f"User {i}"} for i in range(1000)],
)
await session.commit()

# Method 3: PostgreSQL COPY (very fast)
from sqlalchemy.dialects.postgresql import insert
# Or use asyncpg's copy method directly

# Benchmark: Core insert is 5-10x faster than add_all for large datasets
```

---

## SQLModel

### Q8: What is SQLModel and when should you use it?

**Answer:** SQLModel by Sebastián Ramírez combines SQLAlchemy ORM and Pydantic validation:

```python
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
```

**Use when:**
- Rapid prototyping
- Simple CRUD applications
- You want less code duplication between ORM and Pydantic

**Don't use when:**
- Complex database patterns (use pure SQLAlchemy)
- Advanced column types needed
- Existing SQLAlchemy codebase

---

### Q9: Can SQLModel and SQLAlchemy be used together?

**Answer:** Yes. SQLModel is built on SQLAlchemy:

```python
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy import Column, Integer, String

# SQLModel table
class User(SQLModel, table=True):
    name: str

# SQLAlchemy table (in same database)
class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    action = Column(String(100))

# Both work with the same engine and session
engine = create_engine("sqlite:///app.db")
SQLModel.metadata.create_all(engine)
Base.metadata.create_all(engine)
```

---

### Q10: How do you do partial updates with SQLModel?

**Answer:**

```python
class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None

@app.patch("/users/{user_id}")
async def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404)

    # Only update provided fields
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```

---

## Alembic

### Q11: What is Alembic and why is it essential?

**Answer:** Alembic is SQLAlchemy's migration tool. It tracks schema changes in version-controlled migration files:

```bash
# Generate migration from model changes
alembic revision --autogenerate -m "add users table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

**Why essential:**
- Version-controlled schema changes
- Reproducible deployments
- Team collaboration (merge migrations)
- Rollback capability
- Data migration support

---

### Q12: How does autogenerate work?

**Answer:** Alembic compares your SQLAlchemy model metadata against the actual database:

```python
# alembic/env.py
target_metadata = Base.metadata  # Your models' metadata

# Detects:
# - New tables
# - Removed tables
# - New columns
# - Removed columns
# - New indexes
# - Changed column types

# Does NOT detect:
# - Data changes
# - Renamed columns (detected as drop + add)
# - Complex type changes
```

---

### Q13: Why are downgrades important?

**Answer:** Downgrades are your safety net:

```python
def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100)),
    )

def downgrade() -> None:
    op.drop_table("users")  # Can rollback!
```

Without downgrades, if a migration breaks production, you can't easily revert. Manual database intervention may be needed.

---

### Q14: How do you handle data migrations?

**Answer:**

```python
def upgrade() -> None:
    # Schema change
    op.add_column("users", sa.Column("full_name", sa.String(200)))

    # Data migration
    conn = op.get_bind()
    conn.execute(sa.text("""
        UPDATE users
        SET full_name = name
        WHERE full_name IS NULL
    """))

    # Drop old column
    op.drop_column("users", "name")

    # Rename
    op.alter_column("users", "full_name", new_column_name="name")
```

---

### Q15: How do you handle migration conflicts in teams?

**Answer:**

```bash
# 1. Communicate about migration timing
# 2. Merge main branch frequently
# 3. When conflicts occur:

# Generate merge migration
alembic merge -m "merge users and products"

# In the merge file, include changes from both branches
def upgrade() -> None:
    # Include all changes from both branches
    ...
```

**Prevention:**
- One migration per PR
- Merge main frequently
- Use descriptive revision messages

---

## MongoDB/Beanie

### Q16: When should you use MongoDB over PostgreSQL?

**Answer:**

| Use MongoDB | Use PostgreSQL |
|-------------|---------------|
| Flexible schema | Complex relationships |
| Rapid prototyping | ACID compliance |
| Document-oriented data | Structured data |
| Horizontal scaling | Advanced queries |
| JSON-heavy applications | Reporting/analytics |
| Content management | Financial data |

---

### Q17: What is embedding vs referencing in MongoDB?

**Answer:**

```python
# Embedding (denormalization)
class Order(Document):
    items: list[OrderItem] = []  # Items stored inside order

# Referencing (normalization)
class Order(Document):
    item_ids: list[str] = []  # Only IDs stored, items in separate collection

# Rule of thumb:
# - Data accessed together → embed
# - Data shared across documents → reference
# - Small, bounded arrays → embed
# - Large, unbounded arrays → reference
```

---

### Q18: How does Beanie differ from raw Motor?

**Answer:**

```python
# Motor (raw)
from motor.motor_asyncio import AsyncIOMotorClient
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["myapp"]

# No validation, raw dict operations
await db.users.insert_one({"name": "Alice", "email": "alice@test.com"})
user = await db.users.find_one({"_id": user_id})

# Beanie (ODM)
from beanie import Document
class User(Document):
    name: str
    email: str

# Pydantic validation, clean API
user = User(name="Alice", email="alice@test.com")
await user.insert()
found = await User.get(user_id)
```

---

### Q19: How do you create indexes in Beanie?

**Answer:**

```python
from beanie import Document, Indexed

class User(Document):
    name: str = Indexed()  # Regular index
    email: str = Indexed(unique=True)  # Unique index

    class Settings:
        indexes = [
            [("created_at", -1)],  # Sort index
            [("name", "text")],    # Text search index
        ]
```

---

### Q20: What is the aggregation pipeline?

**Answer:**

```python
# MongoDB aggregation
pipeline = [
    {"$match": {"status": "active"}},         # Filter
    {"$group": {                               # Group
        "_id": "$category",
        "count": {"$sum": 1},
        "avg_price": {"$avg": "$price"},
    }},
    {"$sort": {"count": -1}},                  # Sort
    {"$limit": 10},                            # Limit
]

results = await Order.aggregate(pipeline).to_list()
```

---

## Redis

### Q21: When would you use Redis in a FastAPI application?

**Answer:**

```python
# 1. Caching
await r.setex("user:1", 300, json.dumps(user_data))

# 2. Session storage
await r.setex(f"session:{session_id}", 3600, json.dumps(session_data))

# 3. Rate limiting
count = await r.incr(f"rate:{ip}:{window}")

# 4. Pub/Sub
await r.publish("notifications", json.dumps(event))

# 5. Job queue
await r.lpush("tasks", json.dumps(task_data))
```

---

### Q22: What is the difference between `redis-py` and `aioredis`?

**Answer:** `aioredis` is deprecated. `redis-py` v4.2+ has native async:

```python
# Current approach
import redis.asyncio as redis
r = redis.Redis.from_url("redis://localhost:6379")
await r.set("key", "value")
```

---

### Q23: How do you implement rate limiting with Redis?

**Answer:**

```python
# Fixed window
async def is_allowed(r: redis.Redis, key: str, max_req: int, window: int) -> bool:
    count = await r.incr(f"rate:{key}:{int(time.time() // window)}")
    if count == 1:
        await r.expire(f"rate:{key}:{int(time.time() // window)}", window)
    return count <= max_req

# Sliding window (more accurate)
async def sliding_window(r: redis.Redis, key: str, max_req: int, window: int) -> bool:
    now = time.time()
    pipe = r.pipeline()
    pipe.zremrangebyscore(key, 0, now - window)
    pipe.zadd(key, {str(now): now})
    pipe.zcard(key)
    pipe.expire(key, window)
    results = await pipe.execute()
    return results[2] <= max_req
```

---

### Q24: What is cache stampede and how do you prevent it?

**Answer:** When many requests simultaneously try to rebuild an expired cache:

```python
# Prevention 1: Locking
async def get_with_lock(r, key, factory):
    value = await r.get(key)
    if value:
        return json.loads(value)

    lock = r.lock(f"lock:{key}", timeout=5)
    if await lock.acquire():
        try:
            value = await factory()
            await r.setex(key, 300, json.dumps(value))
            return value
        finally:
            await lock.release()
    else:
        # Another process is building cache, wait and retry
        await asyncio.sleep(0.1)
        return await get_with_lock(r, key, factory)

# Prevention 2: Stale-while-revalidate
async def swr(r, key, factory, ttl=300, stale_ttl=3600):
    value, stale = await r.get(key), await r.get(f"stale:{key}")
    if value:
        return json.loads(value)
    if stale:
        asyncio.create_task(refresh_cache(r, key, factory, ttl))
        return json.loads(stale)
    return await factory()
```

---

### Q25: How do you handle Redis failures?

**Answer:**

```python
async def get_cached_user(r: redis.Redis, user_id: int):
    try:
        cached = await r.get(f"user:{user_id}")
        if cached:
            return json.loads(cached)
    except (redis.ConnectionError, redis.TimeoutError) as e:
        logger.warning(f"Redis unavailable: {e}")
        # Fall back to database
        pass

    # Database fallback
    return await get_user_from_db(user_id)
```

---

## Database Patterns

### Q26: What is the Repository Pattern?

**Answer:** Abstracts data access behind an interface:

```python
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    async def get(self, id: int) -> User | None: ...

    @abstractmethod
    async def create(self, user: User) -> User: ...

# SQL implementation
class SQLUserRepository(UserRepository):
    async def get(self, id: int):
        return await self.session.get(User, id)

# In-memory for tests
class InMemoryUserRepository(UserRepository):
    async def get(self, id: int):
        return self.users.get(id)
```

**Benefits:** Testability, swappable implementations, separation of concerns.

---

### Q27: What is Unit of Work?

**Answer:** Tracks all changes and coordinates committing as one transaction:

```python
class UnitOfWork:
    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
        self.orders = OrderRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()

# Usage
async with UnitOfWork() as uow:
    user = await uow.users.get(user_id)
    order = Order(user_id=user.id)
    await uow.orders.create(order)
    # Auto-commits on success, auto-rollbacks on failure
```

---

### Q28: What is the difference between Active Record and Data Mapper?

**Answer:**

| Aspect | Active Record | Data Mapper |
|--------|--------------|-------------|
| Model | Has DB methods | Pure domain object |
| DB access | Built into model | Separate repository |
| Testing | Hard (DB coupled) | Easy (mock repo) |
| Example | SQLModel, Django ORM | SQLAlchemy + Repository |

```python
# Active Record
user = User(name="Alice")
await user.save()  # Model knows about DB

# Data Mapper
user = User(name="Alice")  # Pure object
repo = UserRepository(session)
await repo.save(user)  # Repository handles DB
```

---

### Q29: How does connection pooling work?

**Answer:**

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,        # Persistent connections
    max_overflow=10,     # Extra connections beyond pool_size
    pool_timeout=30,     # Seconds to wait for connection
    pool_recycle=1800,   # Recycle connections after 30 min
    pool_pre_ping=True,  # Verify connections before use
)

# Check pool health
pool = engine.pool
print(f"Size: {pool.size()}")
print(f"Checked out: {pool.checkedout()}")
```

---

### Q30: What is the Saga Pattern?

**Answer:** Distributed transaction with compensating actions:

```python
class CreateOrderSaga:
    async def execute(self, order_data):
        try:
            # Step 1: Reserve inventory
            await self.inventory.reserve(order_data.items)

            # Step 2: Process payment
            payment = await self.payment.charge(order_data.total)

            # Step 3: Create order
            order = Order(**order_data.dict())
            self.db.add(order)
            await self.db.commit()

        except Exception as e:
            # Compensate in reverse order
            await self.payment.refund(payment.id)
            await self.inventory.release(order_data.items)
            raise
```

---

### Q31: When should you use read replicas?

**Answer:** When read traffic exceeds single-database capacity:

```python
class DatabaseRouter:
    def get_read_session(self):
        # Route reads to replicas
        engine = random.choice(self.read_engines)
        return AsyncSession(engine)

    def get_write_session(self):
        # Route writes to primary
        return AsyncSession(self.write_engine)

# Usage
@app.get("/users/")
async def list_users(db=Depends(get_read_db)):
    # Read from replica
    ...

@app.post("/users/")
async def create_user(db=Depends(get_write_db)):
    # Write to primary
    ...
```

**Consider:** Replication lag (async replication means replicas may be slightly behind).

---

### Q32: How do you optimize slow queries?

**Answer:**

```python
# 1. Add indexes
class User(Base):
    email: str = mapped_column(index=True)

# 2. Use eager loading
select(User).options(selectinload(User.items))

# 3. Use EXPLAIN
result = await db.execute(text("EXPLAIN ANALYZE SELECT ..."))

# 4. Batch operations
session.add_all(users)
await session.commit()

# 5. Select only needed columns
select(User.id, User.name)  # Not select(User)

# 6. Use subqueries instead of loading
subq = select(func.count(Item.id)).where(Item.owner_id == User.id).scalar_subquery()
select(User, subq.label("item_count"))
```

---

### Q33: What is database sharding?

**Answer:** Splitting data horizontally across multiple servers:

```python
def get_shard(user_id: int, num_shards: int = 4) -> str:
    return f"shard_{user_id % num_shards}"

class ShardedRepository:
    def __init__(self, shards: dict[str, AsyncSession]):
        self.shards = shards

    async def get_user(self, user_id: int):
        shard_key = get_shard(user_id)
        session = self.shards[shard_key]
        return await session.get(User, user_id)
```

**Challenges:** Cross-shard queries, distributed transactions, rebalancing.

---

### Q34: How do you handle database migrations in production?

**Answer:**

```bash
# 1. Test in staging
alembic upgrade head  # staging

# 2. Apply during low traffic
alembic upgrade head  # production

# 3. Rollback plan ready
alembic downgrade -1  # if needed

# 4. Blue-green deployment (zero downtime)
# - Deploy new code with migration
# - Run migration on new database
# - Switch traffic
```

---

### Q35: What is the difference between `selectinload` and `joinedload`?

**Answer:**

```python
# selectinload: separate IN query
# Query 1: SELECT * FROM users
# Query 2: SELECT * FROM items WHERE user_id IN (1, 2, 3, ...)
select(User).options(selectinload(User.items))
# Result: 2-3 queries, no data duplication

# joinedload: JOIN query
# Query 1: SELECT * FROM users JOIN items ON ...
select(User).options(joinedload(User.items))
# Result: 1 query, but user data duplicated for each item

# Use selectinload for collections (many items per user)
# Use joinedload for to-one relationships (one owner per item)
```

---

## Quick Reference

| Pattern | Use Case | Complexity |
|---------|----------|------------|
| Repository | Data access abstraction | Medium |
| Unit of Work | Transaction coordination | High |
| Active Record | Simple CRUD | Low |
| Data Mapper | Complex domains | High |
| Read Replicas | Read scalability | Medium |
| Sharding | Write scalability | Very High |
| Connection Pooling | Performance | Low |
| Caching | Read performance | Low-Medium |
| N+1 Prevention | Query optimization | Low |
| Eager Loading | Relationship loading | Low |

---

## Scenario Questions

### Scenario 1: Design a Database for a Social Media App
**Answer:** PostgreSQL for users/posts (ACID, relationships). Redis for feeds/cache. MongoDB for logs/analytics. Read replicas for feeds. Sharding by user ID for scale.

### Scenario 2: Migrate 1M Rows Without Downtime
**Answer:** Use Alembic data migration with batch processing. Add new column, backfill in batches, switch reads to new column, drop old column. Always have rollback plan.

### Scenario 3: Handle Database Failover
**Answer:** Use connection pooling with retry logic. Implement circuit breaker pattern. Read from replicas during primary failure. Use health checks to detect failures quickly.

### Scenario 4: Optimize a Slow API Endpoint
**Answer:** Enable SQL logging. Identify N+1 queries. Add eager loading. Add indexes for WHERE/ORDER BY clauses. Consider caching. Use EXPLAIN ANALYZE for query plans.

---

## Summary

Database mastery in FastAPI requires understanding async SQLAlchemy, proper indexing, query optimization, caching strategies, and architectural patterns like Repository and Unit of Work. Always consider scalability, reliability, and performance in your designs.
