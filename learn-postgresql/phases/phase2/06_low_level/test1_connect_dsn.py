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
            
    # The connection is automatically closed here
    print("Connection automatically closed.")

except psycopg.OperationalError as e:
    # This block catches errors related to the connection itself,
    # such as wrong credentials, host not found, or database doesn't exist.
    print(f"\nError: Could not connect to the database. Check your DSN and server status.")
    print(f"Details: {e}")

except Exception as e:
    # A generic catch-all for any other errors
    print(f"\nAn unexpected error occurred during the database operation.")
    print(f"Details: {e}")
