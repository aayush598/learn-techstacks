import psycopg
import os

# --- 1. The DSN (Data Source Name) ---
# A DSN is a connection string that contains all the information
# needed to connect to the database. It is the best practice
# because it keeps sensitive credentials in a single string that
# can be managed easily (e.g., in environment variables).

# Option A: The recommended URL-style DSN
# This is a concise, standard format.
# Replace the placeholders with your actual database details.
dsn_url = "postgresql://learner:mypassword@localhost:5432/learndb"

# Option B: The key-value style DSN
# This format is also common and very readable.
dsn_kv = "dbname=learndb user=learner password=mypassword host=localhost port=5432"

# Best practice for real-world applications:
# Get your DSN from an environment variable for security.
# This avoids hardcoding sensitive information in your source code.
dsn_from_env = os.getenv('DB_DSN', dsn_url)

# --- 2. Connection Management with a Context Manager ---
# Using the `with` statement is the safest and most modern way to
# handle connections. It guarantees that the connection is
# closed automatically when the block is exited, even if an error occurs.

try:
    print(f"Attempting to connect with DSN: {dsn_from_env}")
    
    # Establish the connection using the DSN
    with psycopg.connect(dsn_from_env) as conn:
        print("Connection successful!")
        
        # --- 3. Example of using the connection ---
        # A connection by itself can't do much. You need a cursor.
        # The 'with' block for the connection handles the closing.
        # Now we'll use a cursor to execute a simple query.
        with conn.cursor() as cur:
            # Execute a simple query to get the current database version
            cur.execute("SELECT version();")
            
            # Fetch the single result
            db_version = cur.fetchone()
            
            print("Successfully executed a query.")
            print(f"Database version: {db_version[0]}")

            # --- Step 2: Drop and recreate the table for a clean slate ---
            print("\nDropping 'test_users' table if it exists...")
            cur.execute("DROP TABLE IF EXISTS test_users;")
            print("Table dropped.")

            print("\nCreating a test table named 'test_users'...")
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS test_users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            );
            """
            cur.execute(create_table_sql)
            print("Table 'test_users' created or already exists.")
            
            # --- Step 3: Verify the table was created ---
            # You can query the information schema to check for the table's existence.
            print("Verifying the existence of 'test_users' table...")
            verify_sql = """
            SELECT EXISTS (
               SELECT FROM pg_tables
               WHERE schemaname = 'public' AND tablename = 'test_users'
            );
            """
            cur.execute(verify_sql)
            table_exists = cur.fetchone()[0]
            
            if table_exists:
                print("Verification successful: 'test_users' table exists.")
            else:
                print("Verification failed: 'test_users' table was not found.")

            # --- Step 4: Insert with parameters ---
            print("\nInserting a single record with parameters...")
            insert_sql_single = "INSERT INTO test_users (name, email) VALUES (%s, %s);"
            user_data = ('Charlie Brown', 'charlie.b@example.com')
            cur.execute(insert_sql_single, user_data)
            print("Successfully inserted one record.")

            # --- Step 5: Insert multiple records with parameters ---
            print("\nInserting multiple records with parameters...")
            insert_sql_multiple = "INSERT INTO test_users (name, email) VALUES (%s, %s);"
            users_data = [
                ('Alice Johnson', 'alice.j@example.com'),
                ('Bob Smith', 'bob.s@example.com')
            ]
            cur.executemany(insert_sql_multiple, users_data)
            print(f"Inserted {cur.rowcount} records.")

            # --- Step 6: Verify inserted data ---
            print("\nRetrieving and verifying all records from 'test_users'...")
            cur.execute("SELECT id, name, email FROM test_users ORDER BY id;")
            all_users = cur.fetchall()
            
            print("Found the following records:")
            for user in all_users:
                print(f"  ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")

            # --- Step 7: Demonstrate Rollback ---
            print("\n--- Demonstrating Transaction Rollback ---")
            try:
                # Begin a new operation
                print("Attempting to insert a valid record and a duplicate record...")
                cur.execute(insert_sql_single, ('David Green', 'david.g@example.com'))
                print("Successfully inserted 'David Green'.")
                
                # This next line will cause a unique constraint violation and an error.
                cur.execute(insert_sql_single, ('Duplicate User', 'alice.j@example.com'))

            except psycopg.Error as e:
                print(f"An error occurred: {e}")
                print("Rolling back the transaction...")
                conn.rollback() # This undoes the insert of 'David Green'
                print("Rollback successful.")

            finally:
                # Verify that the rolled-back record is not in the database
                print("\nVerifying the database state after rollback...")
                cur.execute("SELECT id, name, email FROM test_users ORDER BY id;")
                final_users = cur.fetchall()
                
                print("Final records in the table:")
                for user in final_users:
                    print(f"  ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
                
    # The connection is automatically closed here
    print("\nConnection automatically closed.")

except psycopg.OperationalError as e:
    # This block catches errors related to the connection itself,
    # such as wrong credentials, host not found, or database doesn't exist.
    print(f"\nError: Could not connect to the database. Check your DSN and server status.")
    print(f"Details: {e}")

except Exception as e:
    # A generic catch-all for any other errors
    print(f"\nAn unexpected error occurred during the database operation.")
    print(f"Details: {e}")

# --- Step 8: Demonstrate Server-Side Cursor (Streaming Large Results) ---
# This is useful for fetching very large result sets without consuming a lot of memory.
# The `psycopg` driver streams the results from the server in chunks.
print("\n--- Step 8: Demonstrating Server-Side Cursor for Streaming ---")
try:
    with psycopg.connect(dsn_from_env) as conn:
        print("New connection for server-side cursor established.")
        
        # NOTE: A server-side cursor requires an active transaction.
        # By default, psycopg manages transactions, so we don't need `conn.autocommit = True`.
        # This fixes the "DECLARE CURSOR can only be used in transaction blocks" error.

        # Let's drop and recreate the table to insert a large number of users
        cur = conn.cursor()
        print("\nDropping and recreating 'test_users' table for streaming demo...")
        cur.execute("DROP TABLE IF EXISTS test_users;")
        cur.execute("""
            CREATE TABLE test_users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            );
        """)
        
        # Insert a large number of records to make streaming worthwhile
        print("Inserting 10000 records...")
        users_to_insert = [
            (f"User_{i}", f"user_{i}@example.com") for i in range(10000)
        ]
        cur.executemany("INSERT INTO test_users (name, email) VALUES (%s, %s);", users_to_insert)
        print("Insertion of 10000 records complete.")

        # Create a named cursor for server-side processing
        # The name 'large_data_cursor' is arbitrary but helps identify it.
        # This cursor doesn't load the entire result set into memory.
        print("\nCreating a server-side cursor to stream data...")
        with conn.cursor('large_data_cursor') as s_cur:
            s_cur.execute("SELECT name, email FROM test_users;")
            
            print("Streaming results in batches. Reading first 5 rows...")
            count = 0
            for row in s_cur:
                print(f"  - {row}")
                count += 1
                if count >= 5:
                    break # Stop after a few rows for the demonstration
            print(f"\nStreaming complete after reading {count} rows.")

except psycopg.OperationalError as e:
    print(f"\nError in streaming demonstration: Could not connect to the database.")
    print(f"Details: {e}")
    
except Exception as e:
    print(f"\nAn unexpected error occurred during the streaming operation.")
    print(f"Details: {e}")
