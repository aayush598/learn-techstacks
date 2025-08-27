## 📚 concepts to master

### 1. **declarative mappings**

* classes ↔ tables using `declarative_base()` (or `sqlalchemy.orm.declarative_base`).
* attributes map to `Column`s, relationships declared via `relationship()`.

### 2. **sessions & identity map**

* `Session` = unit of work + identity map (first-level cache).
* identity map ensures each row instance is unique per session → prevents duplicates and enables auto-dirty checking.

### 3. **relationships**

* `relationship("OtherClass", back_populates="…")` links objects.
* `one-to-many`, `many-to-one`, `many-to-many`.

### 4. **loading strategies**

* **lazy (default):** triggers separate query when accessing related attribute (can cause N+1).
* **joinedload:** eager load via `JOIN`.
* **subqueryload:** eager load via subquery.

### 5. **N+1 query problem**

* when you fetch N parents lazily, then access children → one query for parents + N queries for children.
* must recognize and fix with eager loading.

---

## 🧪 lab: users + todos + comments

### schema (3 related tables)

```python
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship, Session, joinedload

Base = declarative_base()

class User(Base):
    __tablename__ = "app_user"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)

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

### engine & setup

```python
engine = create_engine("postgresql+psycopg://learner:mypassword@localhost:5432/pythondb", echo=True)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
```

### insert sample data

```python
with Session(engine) as session:
    u1 = User(username="alice")
    u2 = User(username="bob")

    t1 = Todo(title="Buy milk", user=u1)
    t2 = Todo(title="Write report", user=u1)
    t3 = Todo(title="Clean room", user=u2)

    t1.comments = [Comment(body="remember lactose-free"), Comment(body="urgent!")]
    t2.comments = [Comment(body="due tomorrow")]
    t3.comments = [Comment(body="take out trash")]

    session.add_all([u1, u2])
    session.commit()
```

---

## 🔬 test 1: lazy loading (default)

```python
with Session(engine) as session:
    todos = session.query(Todo).limit(5).all()
    for todo in todos:
        print(todo.title, [c.body for c in todo.comments])
```

**echo log shows:**

* 1 query to fetch todos.
* then N queries (one per todo) when accessing `comments`.
* classic N+1.

---

## 🔬 test 2: eager loading with joinedload

```python
with Session(engine) as session:
    todos = session.query(Todo).options(joinedload(Todo.comments)).limit(5).all()
    for todo in todos:
        print(todo.title, [c.body for c in todo.comments])
```

**echo log shows:**

* 1 query with a `LEFT OUTER JOIN` → todos + comments in one shot.
* avoids N+1.

---

## 🔬 test 3: show query count difference

to see exact query counts:

```python
from sqlalchemy import event

queries = []
def before_cursor_execute(conn, cursor, statement, params, context, executemany):
    queries.append(statement)

event.listen(engine, "before_cursor_execute", before_cursor_execute)

with Session(engine) as session:
    todos = session.query(Todo).limit(5).all()
    for todo in todos:
        _ = todo.comments  # triggers lazy load

print("Lazy load queries:", len(queries))

queries.clear()
with Session(engine) as session:
    todos = session.query(Todo).options(joinedload(Todo.comments)).limit(5).all()
    for todo in todos:
        _ = todo.comments

print("Joinedload queries:", len(queries))
```

expected:

* lazy load → `1 + N` queries.
* joinedload → `1` query total.
