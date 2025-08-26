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

            # --- Step 2: Create a test table ---
            # Use `cur.execute()` to run DDL (Data Definition Language) commands.
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

            # --- Step 4: Insert some data (optional) ---
            print("\nInserting sample data into 'test_users'...")
            insert_sql = "INSERT INTO test_users (name, email) VALUES (%s, %s);"
            sample_data = [
                ('Alice Johnson', 'alice.j@example.com'),
                ('Bob Smith', 'bob.s@example.com')
            ]
            cur.executemany(insert_sql, sample_data)
            print(f"Inserted {cur.rowcount} rows.")
            
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
