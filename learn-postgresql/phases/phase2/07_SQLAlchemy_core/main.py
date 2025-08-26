#
# Complete SQLAlchemy Core Bank Transfer Lab
#
# This script re-implements a bank transfer and rollback
# using SQLAlchemy Core, demonstrating key concepts like
# connection pooling and transaction scopes.
#

import sys
import os

try:
    from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Numeric, CheckConstraint, text
except ImportError:
    print("SQLAlchemy is not installed. Please install it using: pip install SQLAlchemy")
    sys.exit(1)

# Step 1: Setup the Engine and Metadata
# --------------------------------------------------------------------------------
print("--- Step 1: Setting up the database engine ---")
# The engine manages the connection to the database, including connection pooling.
# `echo=True` will print all SQL statements executed.
engine = create_engine(
    "postgresql+psycopg://learner:mypassword@localhost:5432/pythondb", 
    echo=True,
    # The pool_size and overflow are for demonstration purposes
    pool_size=5,
    max_overflow=10
)
metadata = MetaData()
print("Engine and MetaData initialized successfully.")
print("-" * 50)

# Step 2: Define the Table Schema in Core
# --------------------------------------------------------------------------------
print("--- Step 2: Defining the 'bank' table schema ---")
# Define the table structure programmatically using SQLAlchemy's Core API.
bank = Table(
    "bank", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("owner", String, nullable=False),
    Column("balance", Numeric, nullable=False),
    # This constraint will cause the transfer to fail later on.
    CheckConstraint("balance >= 0", name="positive_balance")
)

# Clean up any existing table and create a new one based on our schema.
print("Dropping existing 'bank' table...")
metadata.drop_all(engine)
print("Creating a new 'bank' table...")
metadata.create_all(engine)
print("Table 'bank' created successfully.")
print("-" * 50)

# Step 3: Insert initial rows
# --------------------------------------------------------------------------------
print("--- Step 3: Inserting initial bank account data ---")
# Use the `with engine.begin()` context manager for a single transaction.
with engine.begin() as conn:
    insert_stmt = bank.insert()
    print("Executing insert statement...")
    conn.execute(insert_stmt, [
        {"owner": "alice", "balance": 100},
        {"owner": "bob", "balance": 50},
    ])
print("Initial data inserted. Alice: $100, Bob: $50.")
print("-" * 50)

# Step 4: Simulate Transfer with Rollback
# --------------------------------------------------------------------------------
print("--- Step 4: Simulating bank transfer with a forced rollback ---")
print("Attempting to transfer $20 from Alice to Bob...")
# The `engine.begin()` context manager ensures all operations
# are atomic. If any fail, all are rolled back.
try:
    with engine.begin() as conn:
        # Transfer $20 from Alice
        conn.execute(
            bank.update()
            .where(bank.c.owner == "alice")
            .values(balance=bank.c.balance - 20)
        )

        # Transfer $20 to Bob
        conn.execute(
            bank.update()
            .where(bank.c.owner == "bob")
            .values(balance=bank.c.balance + 20)
        )
        print("Transfer part 1 (Alice -> Bob) completed.")

        # This invalid operation will fail due to the CheckConstraint,
        # triggering a rollback of the entire transaction.
        print("Executing invalid operation to force a rollback...")
        conn.execute(
            bank.update()
            .where(bank.c.owner == "bob")
            .values(balance=bank.c.balance - 200)
        )
except Exception as e:
    print("\n--- Rollback Triggered ---")
    print(f"Error caught: {e}")
    print("The transaction was automatically rolled back.")
print("-" * 50)

# Step 5: Verify the results after the rollback
# --------------------------------------------------------------------------------
print("--- Step 5: Verifying account balances after the rollback ---")
# Use a new connection for a simple query to see the final state.
with engine.connect() as conn:
    result = conn.execute(bank.select()).all()
    print("Current balances in the database:")
    for row in result:
        print(f"  - {row.owner}: ${row.balance}")
    print("Balances should be at their initial values (Alice: $100, Bob: $50).")
print("-" * 50)

# Step 6: Compiled SQL Peek
# --------------------------------------------------------------------------------
print("--- Step 6: Peeking at the compiled SQL ---")
# This shows the final SQL string that SQLAlchemy generates from our
# programmatic expression.
stmt = bank.select().where(bank.c.owner == "alice")
print("SQL expression for 'SELECT FROM bank WHERE owner = alice':")
print(str(stmt.compile(compile_kwargs={"literal_binds": True})))
print("-" * 50)


# Step 7: Check Connection Pool Reuse
# --------------------------------------------------------------------------------
print("--- Step 7: Demonstrating connection pool with concurrent usage ---")
conn_ids = []

# Open two connections simultaneously by nesting the 'with' statements.
# This forces the pool to hand out two distinct connections.
print("Attempting to open two connections simultaneously...")
with engine.connect() as conn1:
    conn_ids.append(id(conn1.connection))
    print(f"Conn1 ID: {conn_ids[0]}")
    
    with engine.connect() as conn2:
        conn_ids.append(id(conn2.connection))
        print(f"Conn2 ID: {conn_ids[1]}")
    
        # Check that the IDs are different since both connections are active.
        if conn_ids[0] != conn_ids[1]:
            print("✅ Success! Both connections are active and have different IDs.")
        else:
            print("❌ Failure! Connections share the same ID while both are active.")

print("Both connections (conn1 and conn2) have been released back to the pool.")

# Now, open a third connection. Its ID should match one of the previous two.
print("Opening third connection (conn3) to check for reuse...")
with engine.connect() as conn3:
    conn3_id = id(conn3.connection)
    print(f"Conn3 ID: {conn3_id}")

    if conn3_id in conn_ids:
        print("✅ Success! Connection pool reused a connection.")
    else:
        print("❌ Failure! A new connection was created instead of being reused.")

print("-" * 50)
print("Script finished.")
