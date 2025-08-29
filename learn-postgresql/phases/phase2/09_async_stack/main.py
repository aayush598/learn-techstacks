# async_stack_lab.py
import asyncio
import time
from sqlalchemy import (
    Column, Integer, String, Boolean, Text, ForeignKey, select
)
from sqlalchemy.orm import (
    DeclarativeBase, relationship, joinedload
)
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
)

# ----------------------------------------------------------------------
# 1) Database URL (asyncpg)
# ----------------------------------------------------------------------
DB_URL = "postgresql+asyncpg://learner:mypassword@localhost:5432/pythondb"

# ----------------------------------------------------------------------
# 2) Engine and Session
# ----------------------------------------------------------------------
engine = create_async_engine(
    DB_URL,
    echo=False,            # set True to see SQL queries
    pool_size=5,
    max_overflow=10,
)
Session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# ----------------------------------------------------------------------
# 3) Models
# ----------------------------------------------------------------------
class Base(DeclarativeBase):
    pass

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

# ----------------------------------------------------------------------
# 4) Reset DB and Seed Data
# ----------------------------------------------------------------------
async def reset_and_seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with Session() as s:
        users = [User(username=f"user{i}") for i in range(1, 21)]
        s.add_all(users)
        await s.flush()

        # 100 todos per user, 2 comments each
        for u in users:
            for t in range(100):
                td = Todo(
                    title=f"{u.username}-task-{t}",
                    user=u,
                    is_done=(t % 3 == 0),
                )
                td.comments = [
                    Comment(body=f"c1-{t}"),
                    Comment(body=f"c2-{t}")
                ]
                s.add(td)
        await s.commit()

# ----------------------------------------------------------------------
# 5) Workloads: lazy vs joinedload
# ----------------------------------------------------------------------
PAGE_SIZE = 20

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

# ----------------------------------------------------------------------
# 6) Benchmark Runner
# ----------------------------------------------------------------------
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

# ----------------------------------------------------------------------
# 7) Main
# ----------------------------------------------------------------------
async def main():
    await reset_and_seed()

    # warm-up
    await page_lazy(0)
    await page_joined(0)

    for c in (5, 10, 20, 50, 100, 500, 1000):
        print(f"\n== concurrency={c} ==")
        await bench("lazy", page_lazy, pages=50, concurrency=c)
        await bench("joined", page_joined, pages=50, concurrency=c)

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
