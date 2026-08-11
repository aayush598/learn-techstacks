# Priority 2 — SQLAlchemy / ORM (Q341–Q354)

**Why these matter for micro1:** FastAPI + PostgreSQL + SQLAlchemy is their stack. Expect: what an ORM is, sessions, lazy/eager loading, **N+1** (a favorite), async usage, and session lifecycle in FastAPI.

---

## Q341: Have you used SQLAlchemy?

**Answer with specifics:** "Yes — SQLAlchemy 2.0 with FastAPI. I use the **ORM** for most CRUD and the **Core/expression language** for complex queries; **Alembic** for migrations. I've worked with both sync (psycopg2) and async (`asyncpg` + `AsyncSession`) modes, and tuned queries with eager loading and EXPLAIN."

**Ready to demo:** a model, a session dependency, a join query, `selectinload` for N+1, async session, Alembic migration.

---

## Q342: What is an ORM?

**Object-Relational Mapping** — a library that maps **database tables to classes and rows to objects**, letting you work with data as objects instead of raw SQL.

```python
# raw SQL
rows = session.execute(text("SELECT * FROM users WHERE email = :e"), {"e": email})

# ORM
user = session.execute(select(User).where(User.email == email)).scalar_one()
```

- Provides: schema definition (models), CRUD, relationships (FK joins), transaction/session management, query builder.
- SQLAlchemy, Django ORM, SQLModel (Pydantic+SQLAlchemy), SQLObject.
- **Under the hood** it still generates and executes SQL — it's an abstraction, not a replacement.

---

## Q343: Why use an ORM?

1. **Productivity** — CRUD + queries in Python, less SQL boilerplate.
2. **Type safety & IDE support** — typed models, autocompletion, static checks.
3. **Portability** — mostly DB-agnostic SQL generation (dialects).
4. **Relationships** — declare FK relationships once; load data conveniently.
5. **Migrations** — Alembic derives schema changes from model changes.
6. **Security** — parameterized queries by default (no manual string concatenation → no SQL injection, Q400).
7. **Domain modeling** — objects + relationships mirror business concepts.

---

## Q344: What are the disadvantages of an ORM?

1. **Performance pitfalls** — **N+1** (lazy loading in loops), over-fetching, hidden queries, cartesian fan-out from joins.
2. **Abstraction leakage / complexity** — complex SQL (window functions, recursive CTEs, bulk upserts) is harder or clumsier; you fight the API.
3. **Less control** — the generated SQL isn't always what you'd write; tuning (index hints, lock hints) is limited.
4. **Onboarding/debugging** — developers must know the ORM's conventions; SQL-level issues hidden behind objects.
5. **Schema drift risk** — model ↔ DB mismatch if migrations aren't disciplined.
6. **Memory** — loading many objects (identity map) uses more RAM than raw rows.

**Balance answer:** "ORM for 90% of CRUD and relationships; raw SQL/Core for the 10% that needs performance or expressiveness — and always verify hot paths with EXPLAIN."

---

## Q345: What is a SQLAlchemy model?

A class (subclass of `DeclarativeBase` in 2.0) mapping to a table — attributes map to columns.

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase): pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    orders: Mapped[list["Order"]] = relationship(back_populates="user")

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    amount: Mapped[float]
    user: Mapped[User] = relationship(back_populates="orders")
```

- `Mapped[type]` (2.0 style) gives full typing; `relationship` declares joins between models.
- Create tables via `Base.metadata.create_all(engine)` (dev) or **Alembic migrations** (production).

---

## Q346: What is a SQLAlchemy session?

A **workspace/unit-of-work** for database operations — tracks objects, queues changes, and flushes/commits to the DB.

```python
with Session(engine) as session:
    user = session.get(User, 1)
    user.name = "New Name"        # tracked
    session.commit()              # flush INSERT/UPDATE + COMMIT
# session closed (connection returned to pool)
```

- **Key facts:**
  - **Not thread-safe** — one session per thread/task/request (Q353).
  - Begins a transaction implicitly; `commit()` commits, `rollback()` discards.
  - Objects loaded stay in the **identity map** (same PK → same object) — saves queries, but stale within the session unless refreshed.
  - `SessionLocal` from `sessionmaker(engine)` creates new sessions.

---

## Q347: How do transactions work in SQLAlchemy?

The session manages the transaction lifecycle:

```python
with Session(engine) as session:
    try:
        user = session.get(User, 1)
        user.balance -= 100
        order = Order(user_id=user.id, amount=100)
        session.add(order)
        session.commit()          # flush all pending + COMMIT (atomic)
    except Exception:
        session.rollback()        # discard pending changes
        raise
```

- Pending objects are flushed on `commit()` (or explicit `flush()`); the `BEGIN`/`COMMIT`/`ROLLBACK` is handled automatically.
- Use `session.begin()`/`session.begin_nested()` (savepoints) for finer control.
- Keep the transaction **short** — commit promptly; holding sessions across network/LLM calls holds locks (Q174).
- Async sessions commit/rollback the same way (`await session.commit()`).

---

## Q348: What is lazy loading?

Loading a relationship **only when first accessed** (default). SQLAlchemy issues an extra query at attribute access time.

```python
user = session.get(User, 1)     # query 1
print(user.orders)              # query 2 — SELECT * FROM orders WHERE user_id=1 (on access)
```

- Convenient, but the source of **N+1** (Q350) — accessing a relationship in a loop fires one query per item.

---

## Q349: What is eager loading?

Loading related objects **in the same query** (or a batched second query) to avoid the N+1.

- **`joinedload`** — a `LEFT OUTER JOIN`, one query.

```python
users = session.execute(select(User).options(joinedload(User.orders))).scalars().all()
```

- **`selectinload`** — a second query with `IN (ids...)`; **preferred for collections** (avoids row fan-out with many-to-many and pagination issues).

```python
users = session.execute(select(User).options(selectinload(User.orders))).scalars().all()
```

- Rule: `joinedload` good for single-related (`User.profile`), `selectinload` for collections.

---

## Q350: What is the N+1 problem in SQLAlchemy?

Fetching N parent rows, then triggering **one extra query per row** because a relationship is lazy-loaded in a loop:

```python
users = session.execute(select(User)).scalars().all()   # 1 query (N users)
for u in users:
    print(u.orders)              # N lazy queries — 1 + N total
```

- Same problem as Q170, but in ORM terms.
- **Fix:**
  1. `selectinload(User.orders)` / `joinedload(User.orders)` (Q349).
  2. Batch load in one `IN` query instead of per-row.
  3. Avoid lazy access in loops; pre-load what serializers need.
  4. **Detect it:** enable SQLAlchemy's "raise" lazy strategy (`lazy="raise"` on relationships) so accidental lazy loads error in dev/CI instead of silently hammering the DB.

---

## Q351: How do you perform joins using SQLAlchemy?

**ORM 2.0 style (Core `select` + `join`):**

```python
stmt = (
    select(User, Order)
    .join(Order, Order.user_id == User.id)        # INNER
    .where(User.id == 1)
)
rows = session.execute(stmt).all()

# LEFT JOIN with options
stmt = select(User, Order).outerjoin(Order, Order.user_id == User.id)
```

- **Relationship-based joins:** `select(User).join(User.orders)` (uses the relationship's FK).
- Legacy query API: `session.query(User).join(Order).filter(...)`.
- **Raw SQL** for complex cases: `session.execute(text("SELECT ... JOIN ..."))`.
- Always **index FKs** (Q155) and check the generated SQL with `EXPLAIN` for hot queries.

---

## Q352: How do you use SQLAlchemy asynchronously?

Use the **async engine + AsyncSession** with an async driver (`asyncpg`).

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine("postgresql+asyncpg://user:pass@host/db",
                             pool_size=10, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_user(user_id: int) -> User | None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
```

- All session operations are awaited: `await session.execute(...)`, `await session.commit()`, `await session.scalars(...)`.
- Async relationships need async loading; `selectinload`/`joinedload` work, but you **cannot trigger lazy loads** implicitly (raises) — load eagerly or manually.
- **In FastAPI:** inject an `AsyncSession` via a dependency (Q353).

---

## Q353: How do you manage database sessions in FastAPI?

**Dependency with `yield`** — one session per request, closed in `finally` (returns connection to pool):

```python
from fastapi import Depends

async def get_db():
    async with AsyncSessionLocal() as session:   # commit/rollback+close handled
        yield session

@app.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()
```

Or explicit lifecycle:

```python
def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
        # optionally: db.commit() if your service doesn't
    except Exception:
        db.rollback()
        raise
    finally:
        await db.close()      # returns connection to the pool
```

- **One session per request** — never share across requests/tasks/threads (Session is not thread-safe, Q346).
- `expire_on_commit=False` avoids accessing-expired-attributes errors after serialization.
- Tests: `app.dependency_overrides[get_db] = get_test_db` (Q73).

---

## Q354: How do you prevent database connection leaks?

1. **Session-per-request dependency with `finally: close()`** — always returns the connection (Q353).
2. **Pool with timeouts/recycling:** `pool_size`, `max_overflow`, `pool_pre_ping=True`, `pool_recycle=1800` so stale connections are replaced.
3. **Async engines:** always `await session.close()` or use `async with AsyncSessionLocal()` (context manager).
4. **Never stash sessions in global/request-long-lived objects.**
5. **Background tasks:** give them their **own** session; close it explicitly.
6. **Exception paths:** close in `finally`, not just on success.
7. **Monitor:** connection count vs pool (`SELECT count(*) FROM pg_stat_activity`), pool exhaustion logs; alert on "queue pool limit reached" (Q109–110).
8. **Fix leaks properly** — a leak is a bug (unclosed session), not a symptom to tune around; make it fail loudly with warnings in dev.

**Answer:** "Every request gets one session created in a dependency and closed in `finally`; pools are bounded and pre-pinged; background jobs use their own sessions; and I monitor `pg_stat_activity` for connection creep."