#
# SQLAlchemy ORM Lab: Demonstrating Sessions, Relationships, and Loading Strategies
#
# This script is a complete, runnable example that uses SQLAlchemy's ORM
# to model a simple user, todo, and comment system. It highlights the
# key differences between lazy (default) and eager loading.
#

import sys
import os

try:
    from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Text, event
    from sqlalchemy.orm import declarative_base, relationship, Session, joinedload
except ImportError:
    print("SQLAlchemy is not installed. Please install it using: pip install SQLAlchemy")
    sys.exit(1)

# --- 1. Declarative Mappings ---
# Create a base class that our ORM models will inherit from.
Base = declarative_base()

# Define the User class, mapped to the "app_user" table.
class User(Base):
    __tablename__ = "app_user"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)

    # Define a one-to-many relationship to the Todo class.
    # The `back_populates` argument creates a two-way link.
    todos = relationship("Todo", back_populates="user")

    def __repr__(self):
        return f"<User(username='{self.username}')>"

# Define the Todo class, with relationships to User and Comment.
class Todo(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    is_done = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("app_user.id"))

    # Define the many-to-one relationship back to the User.
    user = relationship("User", back_populates="todos")
    # Define the one-to-many relationship to comments.
    comments = relationship("Comment", back_populates="todo")

    def __repr__(self):
        return f"<Todo(title='{self.title}', user='{self.user.username if self.user else 'None'}')>"

# Define the Comment class, with a many-to-one relationship to Todo.
class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    todo_id = Column(Integer, ForeignKey("todo.id"))

    # Define the many-to-one relationship back to the Todo.
    todo = relationship("Todo", back_populates="comments")

    def __repr__(self):
        return f"<Comment(body='{self.body}')>"

# --- 2. Engine and Database Setup ---
# --------------------------------------------------------------------------------
print("--- Step 1: Setting up the database engine and tables ---")
engine = create_engine("postgresql+psycopg://learner:mypassword@localhost:5432/pythondb", echo=True)

# Drop and re-create all tables based on the ORM models.
print("Dropping existing tables...")
Base.metadata.drop_all(engine)
print("Creating new tables from ORM models...")
Base.metadata.create_all(engine)
print("Database setup complete.")
print("-" * 50)


# --- 3. Insert Sample Data ---
# --------------------------------------------------------------------------------
print("--- Step 2: Inserting sample data into the database ---")
# Use a session to manage the transaction and object state.
with Session(engine) as session:
    # Create User objects.
    u1 = User(username="alice")
    u2 = User(username="bob")

    # Create Todo objects and link them to users directly via Python.
    t1 = Todo(title="Buy milk", user=u1)
    t2 = Todo(title="Write report", user=u1)
    t3 = Todo(title="Clean room", user=u2)

    # Create Comment objects and link them to todos.
    t1.comments = [Comment(body="remember lactose-free"), Comment(body="urgent!")]
    t2.comments = [Comment(body="due tomorrow")]
    t3.comments = [Comment(body="take out trash")]

    # Add all objects to the session.
    session.add_all([u1, u2])
    print("Objects added to session. Committing...")
    session.commit()
    print("Sample data inserted successfully.")
print("-" * 50)


# --- 4. Test 1: Lazy Loading (The N+1 Problem) ---
# --------------------------------------------------------------------------------
print("--- Step 3: Demonstrating Lazy Loading (The N+1 Problem) ---")
print("This will execute one query for the todos, then a separate query for comments for each todo.")

with Session(engine) as session:
    # Query for the todos. This is 1 query.
    todos = session.query(Todo).all()

    for todo in todos:
        # Accessing `todo.comments` triggers a new query for each iteration.
        print(f"Fetching comments for '{todo.title}'...")
        # `_` is used to trigger the lazy load without storing the result.
        _ = [c.body for c in todo.comments]

print("Lazy loading test complete. Check the 'echo' log above to see the multiple queries.")
print("-" * 50)


# --- 5. Test 2: Eager Loading with joinedload ---
# --------------------------------------------------------------------------------
print("--- Step 4: Demonstrating Eager Loading with joinedload ---")
print("This will fetch all todos and their comments in a single query.")

with Session(engine) as session:
    # Use `.options()` with `joinedload()` to eagerly load the comments.
    todos = session.query(Todo).options(joinedload(Todo.comments)).all()
    
    for todo in todos:
        # Comments are already loaded, so no new query is executed here.
        print(f"Accessing pre-loaded comments for '{todo.title}'...")
        _ = [c.body for c in todo.comments]

print("Eager loading test complete. Check the 'echo' log above to see the single query with a JOIN.")
print("-" * 50)


# --- 6. Test 3: Show Exact Query Counts ---
# --------------------------------------------------------------------------------
print("--- Step 5: Counting the exact number of queries ---")
# This section uses an event listener to provide a precise count of queries.
queries = []
def before_cursor_execute(conn, cursor, statement, params, context, executemany):
    queries.append(statement)

event.listen(engine, "before_cursor_execute", before_cursor_execute)

print("Testing lazy loading and counting queries...")
with Session(engine) as session:
    todos = session.query(Todo).all()
    for todo in todos:
        _ = todo.comments  # Triggers the lazy load for each todo

print(f"Lazy load queries: {len(queries)}")

# Clear the list for the next test.
queries.clear()

print("Testing eager loading and counting queries...")
with Session(engine) as session:
    todos = session.query(Todo).options(joinedload(Todo.comments)).all()
    for todo in todos:
        _ = todo.comments  # No new query is triggered

print(f"Joinedload queries: {len(queries)}")

# Remove the event listener to clean up.
event.remove(engine, "before_cursor_execute", before_cursor_execute)

print("Query count test complete.")
print("-" * 50)
print("Script finished. The output should clearly show the N+1 problem and its solution.")
