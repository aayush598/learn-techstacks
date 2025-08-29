# 0) install (choose one async driver)

**option A (recommended): asyncpg**

```bash
source ~/.venvs/pglearn/bin/activate
pip install "SQLAlchemy>=2.0" asyncpg
```

URL: `postgresql+asyncpg://learner:mypassword@localhost:5432/pythondb`

**option B: psycopg3 (async)**

```bash
pip install "SQLAlchemy>=2.0" "psycopg[binary]"
```

URL: `postgresql+psycopg://learner:mypassword@localhost:5432/pythondb?async=1`

> pick one driver and stick to its URL everywhere below.

---

# 1) async engine + session factory

```python
# async_stack_lab.py
import asyncio, time
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, relationship, joinedload
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DB_URL = "postgresql+asyncpg://learner:mypassword@localhost:5432/pythondb"  # or psycopg async URL

engine = create_async_engine(DB_URL, echo=False, pool_size=5, max_overflow=10)
Session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase): pass

class User(Base):
    __tablename__ = "app_user"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    todos = relationship("Todo", back_populates="user")

class Todo(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    is_done = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("app_user.id"))
    user = relationship("User", back_populates="todos")
    comments = relationship("Comment", back_populates="todo")

class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    todo_id = Column(Integer, ForeignKey("todo.id"))
    todo = relationship("Todo", back_populates="comments")
```

---

# 2) schema create + seed (async)

```python
async def reset_and_seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with Session() as s:
        users = [User(username=f"user{i}") for i in range(1, 21)]
        s.add_all(users)
        await s.flush()

        # 100 todos per user, 2 comments each → sizable dataset
        for u in users:
            for t in range(100):
                td = Todo(title=f"{u.username}-task-{t}", user=u, is_done=(t % 3 == 0))
                td.comments = [Comment(body=f"c1-{t}"), Comment(body=f"c2-{t}")]
                s.add(td)
        await s.commit()
```

---

# 3) “paginated list view” workload (lazy vs joinedload)

Each “page” fetches 20 todos and renders their comments.

```python
from sqlalchemy.orm import selectinload, joinedload

async def page_lazy(page: int):
    """Simulate N+1, but in async we need selectinload to make it legal."""
    offset = page * PAGE_SIZE
    async with Session() as s:
        q = (
            select(Todo)
            .options(selectinload(Todo.comments))  # async-safe lazy-ish
            .order_by(Todo.id)
            .offset(offset)
            .limit(PAGE_SIZE)
        )
        todos = (await s.execute(q)).scalars().all()
        rendered = [(t.title, [c.body for c in t.comments]) for t in todos]
        return len(rendered)

async def page_joined(page: int):
    offset = page * PAGE_SIZE
    async with Session() as s:
        q = (
            select(Todo)
            .options(joinedload(Todo.comments))
            .order_by(Todo.id)
            .offset(offset)
            .limit(PAGE_SIZE)
        )
        todos = (await s.execute(q)).scalars().unique().all()
        rendered = [(t.title, [c.body for c in t.comments]) for t in todos]
        return len(rendered)
```

---

# 4) run single-page check + measure query counts (optional)

To see query counts, set `echo=True` on the engine temporarily and observe:

* **lazy**: 1 select for todos + up to 20 selects for comments (N+1).
* **joinedload**: a single `LEFT OUTER JOIN` (or a couple of queries, but not N+1).

---

# 5) concurrency benchmark: async vs sync

Simulate many users requesting pages concurrently and compare **lazy vs joinedload**. (You already saw sync in step-8; re-run it similarly and compare timings.)

```python
async def bench(name, fn, pages=25, concurrency=10):
    sem = asyncio.Semaphore(concurrency)

    async def run_page(p):
        async with sem:
            return await fn(p)

    t0 = time.perf_counter()
    results = await asyncio.gather(*(run_page(p) for p in range(pages)))
    dt = (time.perf_counter() - t0) * 1000
    print(
        f"{name}: {pages} pages in {dt:.1f} ms — {sum(results)} rows rendered"
    )
    return dt

async def bench(name, fn, pages=25, concurrency=10):
    sem = asyncio.Semaphore(concurrency)

    async def run_page(p):
        async with sem:
            return await fn(p)

    t0 = time.perf_counter()
    results = await asyncio.gather(*(run_page(p) for p in range(pages)))
    dt = (time.perf_counter() - t0) * 1000
    print(
        f"{name}: {pages} pages in {dt:.1f} ms — {sum(results)} rows rendered"
    )
    return dt

if __name__ == "__main__":
    asyncio.run(main())
```

**what to look for**

* Under concurrency, **joinedload** should drastically reduce total SQL statements and wall-time vs lazy (which suffers N+1).
* With a real Postgres and modest hardware, you’ll usually see better p95 latency and throughput with `joinedload` for this access pattern.

---

# 6) notes & gotchas

* **pool sizing**: for asyncpg, `pool_size` is on the SQLAlchemy engine (QueuePool analogue). Keep `pool_size` ≤ PgBouncer server limits later.
* **unique().all()**: when using `joinedload` on one-to-many, call `.unique()` to dedupe ORM rows after the JOIN.
* **timeouts**: consider `statement_timeout` at the DB and `execution_options(timeout=…)` for requests.
* **backpressure**: the `Semaphore` in the benchmark prevents runaway connection usage; tune it.
* **sync vs async**: async helps when you have lots of concurrent I/O wait; it won’t make single queries compute faster.
