# PostgreSQL Interview Questions and Answers

## Q1: What is PostgreSQL?
**A:** PostgreSQL is a powerful, open-source object-relational database management system (ORDBMS) known for its reliability, extensibility, and standards compliance. It supports advanced data types, ACID transactions, concurrency control, and features like Multi-Version Concurrency Control (MVCC).

**Code:**
```sql
CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT, active BOOLEAN);
INSERT INTO users (name, active) VALUES ('Ada', true);
SELECT * FROM users;
```

## Q2: What are the key features of PostgreSQL?
**A:** Key features include: ACID compliance, MVCC, JSON/JSONB support, full-text search, custom data types, table inheritance, partitioning, replication (streaming/logical), extensibility (via extensions), window functions, Common Table Expressions (CTEs), and GiST/GIN indexes.

**Code:**
```sql
-- JSONB, window functions, CTEs, and extension support in one query
WITH recent AS (
  SELECT id, name, data FROM users WHERE created_at > now() - interval '1 day'
)
SELECT name, data ->> 'city' AS city,
       row_number() OVER (ORDER BY created_at DESC) AS rn
FROM recent;
```

## Q3: What is MVCC in PostgreSQL?
**A:** Multi-Version Concurrency Control (MVCC) allows multiple transactions to see different versions of data simultaneously. Readers never block writers and writers never block readers. Each transaction sees a snapshot of data as of the start of the transaction.

**Code:**
```sql
-- Session 1
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;

-- Session 2 (concurrent, still sees the old balance until commit)
BEGIN;
SELECT balance FROM accounts WHERE id = 1;
```

## Q4: What is a schema in PostgreSQL?
**A:** A schema is a namespace that contains database objects (tables, views, functions, etc.). It provides logical grouping and access control. The default schema is `public`. Schemas can be chained via `search_path`.

**Code:**
```sql
CREATE SCHEMA analytics;
SET search_path = analytics, public;
CREATE TABLE events (id SERIAL, payload JSONB);
SELECT * FROM events;
```

## Q5: What are the difference between PostgreSQL and MySQL?
**A:** PostgreSQL focuses on standards compliance, extensibility, and advanced features (CTEs, window functions, partial indexes, GiST indexes). MySQL prioritizes speed and ease of use. PostgreSQL supports more advanced data types, better concurrency, and stricter ACID compliance.

**Code:**
```sql
-- Window functions and recursive CTEs: core PostgreSQL features not in MySQL 5.x
SELECT dept_id, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
FROM employees;
```

## Q6: What is the `VACUUM` command?
**A:** `VACUUM` reclaims storage occupied by dead tuples (obsolete row versions). `VACUUM FULL` rewrites the entire table to compact it (locks the table). Autovacuum runs automatically based on configuration thresholds.

**Code:**
```sql
VACUUM ANALYZE users;
VACUUM (VERBOSE, FREEZE) users;
VACUUM FULL users;   -- rewrites the table, takes an exclusive lock
```

## Q7: What is autovacuum in PostgreSQL?
**A:** Autovacuum is a background process that automatically runs `VACUUM` and `ANALYZE` when configured thresholds are met. It prevents table bloat, updates statistics for the query planner, and wraps transaction IDs to prevent transaction ID wraparound.

**Code:**
```sql
SELECT relname, n_live_tup, n_dead_tup, last_autovacuum
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;
```

## Q8: What is a transaction in PostgreSQL?
**A:** A transaction is a unit of work that follows ACID properties. It's started with `BEGIN`, committed with `COMMIT`, or undone with `ROLLBACK`. PostgreSQL ensures atomicity, consistency, isolation, and durability for all transactions.

**Code:**
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;   -- or ROLLBACK;
```

## Q9: What isolation levels does PostgreSQL support?
**A:** PostgreSQL supports: Read Committed (default), Repeatable Read, Serializable. It does not support Read Uncommitted (behaves like Read Committed). Each level provides different guarantees about visibility of concurrent changes.

**Code:**
```sql
BEGIN ISOLATION LEVEL READ COMMITTED;      -- default
BEGIN ISOLATION LEVEL REPEATABLE READ;
BEGIN ISOLATION LEVEL SERIALIZABLE;
```

## Q10: What is `SERIALIZABLE` isolation level?
**A:** The `SERIALIZABLE` level is the strictest isolation level. It ensures transactions execute as if they were run serially (one after another). If a serialization conflict is detected, the transaction is aborted with a `SERIALIZATION_FAILURE` error — retry needed.

**Code:**
```sql
BEGIN ISOLATION LEVEL SERIALIZABLE;
UPDATE accounts SET balance = balance - 50 WHERE id = 1;
-- conflicting transaction is aborted with SQLSTATE 40001; retry in code
COMMIT;
```

## Q11: What is a sequence in PostgreSQL?
**A:** A sequence is a database object that generates a unique integer sequence. Created with `CREATE SEQUENCE` or implicitly via `SERIAL`/`IDENTITY` columns. Accessed via `nextval()`, `currval()`, `setval()` functions.

**Code:**
```sql
CREATE SEQUENCE order_seq START 100 INCREMENT 1;
SELECT nextval('order_seq');   -- 100
SELECT currval('order_seq');   -- 100
SELECT setval('order_seq', 500);
```

## Q12: What is the `SERIAL` type?
**A:** `SERIAL` is a pseudo-type that creates an auto-incrementing integer column. It creates a sequence and sets the column default to `nextval()`. `BIGSERIAL` is the 8-byte version. In modern PostgreSQL, `GENERATED AS IDENTITY` is preferred.

**Code:**
```sql
CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT);
SELECT column_name, column_default, data_type
FROM information_schema.columns WHERE table_name = 'users';
```

## Q13: What is `GENERATED AS IDENTITY`?
**A:** Introduced in PostgreSQL 10, it's the SQL-standard way of creating auto-incrementing columns. `id INT GENERATED ALWAYS AS IDENTITY` or `GENERATED BY DEFAULT AS IDENTITY`. It's more standards-compliant than `SERIAL`.

**Code:**
```sql
CREATE TABLE users (
  id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name TEXT
);
INSERT INTO users (name) VALUES ('Ada');   -- id auto-generated
```

## Q14: What are PostgreSQL data types?
**A:** PostgreSQL supports: numeric (INTEGER, BIGINT, DECIMAL, NUMERIC, REAL, DOUBLE PRECISION), character (CHAR, VARCHAR, TEXT), date/time (DATE, TIME, TIMESTAMP, TIMESTAMPTZ, INTERVAL), boolean, UUID, JSON, JSONB, arrays, hstore (key-value), geometric types, network types (INET, CIDR), and range types.

**Code:**
```sql
CREATE TABLE sample (
  id BIGINT,
  price NUMERIC(10,2),
  created TIMESTAMPTZ,
  meta JSONB,
  tags TEXT[],
  net INET
);
```

## Q15: What is JSONB in PostgreSQL?
**A:** JSONB stores JSON data in a binary decomposed format, allowing indexing (GIN indexes) and efficient querying. Unlike plain JSON (which stores text), JSONB removes whitespace, deduplicates keys, and supports operators like `@>`, `?`, `->>`, and `#>`.

**Code:**
```sql
CREATE TABLE docs (data JSONB);
CREATE INDEX idx_docs_gin ON docs USING GIN (data);

SELECT data -> 'name', data ->> 'tags'
FROM docs
WHERE data @> '{"status": "active"}';
```

## Q16: What is the difference between JSON and JSONB?
**A:** JSON stores an exact copy of the input text (preserving whitespace, order, duplicate keys). JSONB stores data in a decomposed binary format (efficient parsing, indexing). JSONB supports indexing and is faster for queries; JSON is faster for inserts.

**Code:**
```sql
SELECT '{"a": 1, "b": 2}'::json;      -- exact text preserved
SELECT '{"a": 1, "b": 2}'::jsonb;     -- decomposed, keys reordered/deduped
SELECT '{"b":1,"a":1}'::jsonb;        -- jsonb normalizes to {"a":1,"b":1}
```

## Q17: What is `hstore` in PostgreSQL?
**A:** `hstore` is an extension for storing key-value pairs in a single column. It's like a simple dictionary. Operations include `->` (access), `?` (key exists), `||` (concatenate), and `each()` (expand to rows).

**Code:**
```sql
CREATE EXTENSION IF NOT EXISTS hstore;
SELECT 'name=>Ada, role=>admin'::hstore -> 'name';   -- Ada
SELECT 'a=>1'::hstore ? 'a';                          -- true
SELECT 'a=>1'::hstore || 'b=>2'::hstore;              -- a=>1,b=>2
SELECT each('a=>1, b=>2'::hstore);
```

## Q18: How do you create an index in PostgreSQL?
**A:** `CREATE INDEX index_name ON table_name (column_name)`. PostgreSQL supports B-tree (default), Hash, GiST, GIN, SP-GiST, BRIN indexes. Options include `UNIQUE`, `CONCURRENTLY`, `WHERE` (partial), and `INCLUDE` (covering).

**Code:**
```sql
CREATE INDEX idx_users_email ON users (email);               -- B-tree
CREATE UNIQUE INDEX idx_users_email_uq ON users (email);
CREATE INDEX CONCURRENTLY idx_users_active ON users (active) WHERE active;
```

## Q19: What is the difference between B-tree, GiST, and GIN indexes?
**A:** B-tree is the default for equality and range queries. GiST (Generalized Search Tree) supports geometric and full-text search. GIN (Generalized Inverted Index) is for composite types (JSONB, arrays, full-text search). BRIN is for large tables with naturally ordered data.

**Code:**
```sql
CREATE INDEX idx_users_email ON users USING BTREE (email);        -- equality/range
CREATE INDEX idx_locations ON places USING GIST (geom);           -- geometric
CREATE INDEX idx_docs ON docs USING GIN (data jsonb_path_ops);    -- JSONB/full-text
```

## Q20: What is a partial index?
**A:** A partial index is an index created with a `WHERE` clause, indexing only a subset of rows. `CREATE INDEX idx_active ON users (email) WHERE active = true`. It saves space and speeds up queries that match the condition.

**Code:**
```sql
CREATE INDEX idx_active_users_email ON users (email) WHERE active = true;
EXPLAIN SELECT email FROM users WHERE active = true AND email = 'x@y.z';
```

## Q21: What is a covering index (INCLUDE)?
**A:** A covering index includes extra columns in the index (not as search key but as payload). `CREATE INDEX idx ON table (a) INCLUDE (b, c)`. Allows index-only scans for queries selecting `b` and `c` without accessing the table.

**Code:**
```sql
CREATE INDEX idx_users_email_cover ON users (email) INCLUDE (name, created_at);
EXPLAIN SELECT email, name FROM users WHERE email = 'x@y.z';  -- Index Only Scan
```

## Q22: What is `EXPLAIN` in PostgreSQL?
**A:** `EXPLAIN` shows the query execution plan — how PostgreSQL will execute a query. `EXPLAIN ANALYZE` executes the query and provides actual timings and row counts. Essential for query optimization and performance tuning.

**Code:**
```sql
EXPLAIN SELECT * FROM users WHERE email = 'x@y.z';
-- Seq Scan on users (cost=0.00..15.10 rows=1 width=41)
```

## Q23: What is `EXPLAIN ANALYZE`?
**A:** `EXPLAIN ANALYZE` executes the query and shows the plan with actual timing, row counts, and loops. It adds overhead but provides ground truth about query performance. Useful for identifying sequential scans, bad joins, or index misses.

**Code:**
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders JOIN users ON orders.user_id = users.id
WHERE users.email = 'x@y.z';
-- shows actual execution time, rows, and buffer hits/reads
```

## Q24: What are CTEs (Common Table Expressions) in PostgreSQL?
**A:** CTEs are temporary result sets defined with `WITH` that can be referenced in a main query. They improve readability and enable recursive queries. `WITH cte AS (SELECT ...) SELECT * FROM cte`. CTEs act as optimization fences in PostgreSQL.

**Code:**
```sql
WITH expensive AS (
  SELECT id, name FROM products WHERE price > 100
)
SELECT * FROM expensive WHERE name ILIKE '%pro%';
```

## Q25: What are recursive CTEs?
**A:** Recursive CTEs reference themselves, enabling traversal of hierarchical or graph data. Syntax: `WITH RECURSIVE cte AS (base_query UNION ALL recursive_query)`. Used for tree structures, organizational charts, or graph paths.

**Code:**
```sql
WITH RECURSIVE org AS (
  SELECT id, name, manager_id, 1 AS depth
  FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.name, e.manager_id, org.depth + 1
  FROM employees e JOIN org ON e.manager_id = org.id
)
SELECT name, depth FROM org;
```

## Q26: What are window functions in PostgreSQL?
**A:** Window functions perform calculations across a set of rows related to the current row without collapsing them. Examples: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LEAD()`, `LAG()`, `FIRST_VALUE()`, `SUM() OVER (PARTITION BY ... ORDER BY ...)`.

**Code:**
```sql
SELECT name, salary,
       RANK() OVER (ORDER BY salary DESC) AS rnk,
       SUM(salary) OVER (PARTITION BY dept_id) AS dept_total
FROM employees;
```

## Q27: What is `ROW_NUMBER()` and how is it used?
**A:** `ROW_NUMBER()` assigns a unique sequential integer to each row within a partition. `ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC)`. Useful for pagination, deduplication, and ranking.

**Code:**
```sql
SELECT id, name,
       ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rn
FROM employees;

-- dedupe: keep one row per partition
DELETE FROM logs a USING logs b
WHERE a.id > b.id AND a.session_id = b.session_id;
```

## Q28: What is `LAG()` and `LEAD()`?
**A:** `LAG(column, offset, default)` accesses data from a previous row in the same result set. `LEAD()` accesses a following row. Used for comparing values between consecutive rows (e.g., price changes, time differences).

**Code:**
```sql
SELECT day, price,
       LAG(price, 1) OVER (ORDER BY day)  AS prev_day,
       LEAD(price, 1) OVER (ORDER BY day) AS next_day
FROM stock_prices;
```

## Q29: What is `PARTITION BY` in window functions?
**A:** `PARTITION BY` divides the result set into partitions (groups). The window function is applied to each partition independently. Without `PARTITION BY`, the entire result set is treated as a single partition.

**Code:**
```sql
SELECT name, dept_id,
       AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg,
       AVG(salary) OVER () AS company_avg
FROM employees;
```

## Q30: What are PostgreSQL views?
**A:** A view is a named, saved query that acts like a virtual table. `CREATE VIEW active_users AS SELECT * FROM users WHERE active = true`. Views simplify complex queries and provide security by restricting column access.

**Code:**
```sql
CREATE VIEW active_users AS
SELECT id, email FROM users WHERE active = true;

SELECT * FROM active_users;
```

## Q31: What are materialized views?
**A:** Materialized views physically store the query result, unlike regular views that execute the query each time. They're refreshed manually or via `REFRESH MATERIALIZED VIEW`. Useful for expensive queries run frequently (e.g., dashboards).

**Code:**
```sql
CREATE MATERIALIZED VIEW daily_sales AS
SELECT date_trunc('day', created_at) AS day, SUM(total) AS revenue
FROM orders GROUP BY 1;

REFRESH MATERIALIZED VIEW CONCURRENTLY daily_sales;
```

## Q32: What is a trigger in PostgreSQL?
**A:** A trigger is a function that automatically executes when a specified event (INSERT, UPDATE, DELETE, TRUNCATE) occurs on a table. Triggers can be BEFORE, AFTER, or INSTEAD OF, and can fire for each row or each statement.

**Code:**
```sql
CREATE OR REPLACE FUNCTION touch_updated() RETURNS trigger AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER users_upd
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION touch_updated();
```

## Q33: What is the difference between `BEFORE` and `AFTER` triggers?
**A:** `BEFORE` triggers run before the operation, allowing modification or rejection of the row before it's written. `AFTER` triggers run after the operation, useful for actions that depend on the data being committed (logging, auditing).

**Code:**
```sql
-- BEFORE: mutate/reject the row before it is written
CREATE TRIGGER orders_val BEFORE INSERT ON orders
FOR EACH ROW EXECUTE FUNCTION validate_total();

-- AFTER: audit/log after the change lands
CREATE TRIGGER orders_audit AFTER UPDATE ON orders
FOR EACH ROW EXECUTE FUNCTION audit_order();
```

## Q34: What are stored procedures in PostgreSQL?
**A:** Stored procedures (CREATE PROCEDURE) are database objects that can perform transactions (COMMIT/ROLLBACK inside). Unlike functions, they don't return a value. Introduced in PostgreSQL 11. Functions (CREATE FUNCTION) return a value and run within a transaction.

**Code:**
```sql
CREATE PROCEDURE transfer_money(src INT, dst INT, amt NUMERIC) AS $$
BEGIN
  UPDATE accounts SET balance = balance - amt WHERE id = src;
  UPDATE accounts SET balance = balance + amt WHERE id = dst;
  COMMIT;
END $$ LANGUAGE plpgsql;

CALL transfer_money(1, 2, 100);
```

## Q35: What is a user-defined function (UDF) in PostgreSQL?
**A:** UDFs are custom functions written in SQL, PL/pgSQL, C, Python, Perl, or other languages. They accept parameters, perform operations, and return values. Used for encapsulating business logic in the database.

**Code:**
```sql
CREATE FUNCTION discount(price NUMERIC) RETURNS NUMERIC AS $$
  SELECT price * 0.9;
$$ LANGUAGE SQL IMMUTABLE;

SELECT discount(100);
```

## Q36: What is PL/pgSQL?
**A:** PL/pgSQL is PostgreSQL's built-in procedural language. It supports variables, control structures (IF, LOOP, CASE), exception handling, and record types. Ideal for writing functions, triggers, and stored procedures.

**Code:**
```sql
CREATE FUNCTION grade(score INT) RETURNS TEXT AS $$
BEGIN
  IF score >= 90 THEN RETURN 'A';
  ELSIF score >= 80 THEN RETURN 'B';
  ELSE RETURN 'F';
  END IF;
END $$ LANGUAGE plpgsql;

SELECT grade(92);
```

## Q37: What is `pg_stat_statements`?
**A:** `pg_stat_statements` is an extension that tracks execution statistics of all SQL statements: total time, calls, rows, block hits/reads. It's invaluable for identifying slow queries, most frequent queries, and overall database performance.

**Code:**
```sql
CREATE EXTENSION pg_stat_statements;

SELECT query, calls, total_exec_time, mean_exec_time, rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 5;
```

## Q38: What is connection pooling in PostgreSQL?
**A:** Connection pooling manages a pool of database connections, reusing them across client requests. Tools: PgBouncer (lightweight, transaction-level pooling), Pgpool-II (feature-rich). This reduces the overhead of establishing new connections.

**Code:**
```python
import psycopg2
from psycopg2.pool import ThreadedConnectionPool

pool = ThreadedConnectionPool(1, 10, dbname="mydb", host="localhost")
conn = pool.getconn()
cur = conn.cursor()
cur.execute("SELECT count(*) FROM users")
print(cur.fetchone()[0])
pool.putconn(conn)  # return the connection to the pool, not to Postgres
```

## Q39: How do you backup a PostgreSQL database?
**A:** Using `pg_dump` (logical backup of single database), `pg_dumpall` (all databases + globals), or `pg_basebackup` (physical backup for PITR). Restore with `pg_restore` or `psql`. For continuous archiving, use WAL archiving.

**Code:**
```bash
pg_dump -Fc mydb > mydb.dump
pg_dumpall > cluster.sql
pg_basebackup -D /backup/base -X stream -P
```

## Q40: What is Point-in-Time Recovery (PITR)?
**A:** PITR allows restoring a database to any point in time using a base backup and continuous WAL (Write-Ahead Log) archiving. It enables recovery from data corruption accidents by replaying WAL up to a specific timestamp or transaction ID.

**Code:**
```sql
-- postgresql.conf: continuous WAL archiving
wal_level = replica
archive_mode = on
archive_command = 'cp %p /backup/wal/%f'

recovery_target_time = '2024-06-15 14:30:00 UTC'
```

## Q41: What is WAL (Write-Ahead Log)?
**A:** WAL records every change to the database before it's written to data files. It ensures durability (even on crash), enables replication, and supports PITR. WAL files are stored in `pg_wal/` directory.

**Code:**
```sql
SELECT pg_walfile_name(pg_current_wal_lsn()) AS current_wal_segment;
SELECT * FROM pg_ls_waldir() ORDER BY name;
```

## Q42: What is streaming replication?
**A:** Streaming replication copies WAL from a primary server to one or more standby servers in real-time. Standbys can serve read-only queries. It's asynchronous by default, with optional synchronous replication for zero data loss.

**Code:**
```sql
-- primary: postgresql.conf
wal_level = replica
max_wal_senders = 5

-- standby: primary_conninfo in postgresql.auto.conf
SELECT client_addr, state, sync_state FROM pg_stat_replication;
```

## Q43: What is synchronous vs asynchronous replication?
**A:** Synchronous replication waits for at least one standby to confirm WAL write before acknowledging the client, ensuring zero data loss but increasing latency. Asynchronous replication doesn't wait, offering better performance with potential data loss on primary failure.

**Code:**
```sql
SHOW synchronous_commit;   -- on = synchronous, off = asynchronous
SELECT application_name, sync_state, sync_priority FROM pg_stat_replication;
```

## Q44: What is logical replication?
**A:** Logical replication replicates data changes at the row level (not WAL files). It supports selective replication (specific tables), cross-version replication, and bi-directional replication. Uses publication/subscription model.

**Code:**
```sql
-- publisher
CREATE PUBLICATION pub_for_orders FOR TABLE orders, order_items;

-- subscriber (wal_level = logical on the publisher)
CREATE SUBSCRIPTION sub_orders
  CONNECTION 'host=publisher dbname=mydb user=repl password=secret'
  PUBLICATION pub_for_orders;
```

## Q45: What is a `PUBLICATION` and `SUBSCRIPTION`?
**A:** `CREATE PUBLICATION pub FOR TABLE t1` defines which tables to replicate. `CREATE SUBSCRIPTION sub CONNECTION '...' PUBLICATION pub` creates the subscriber that pulls changes. Introduced in PostgreSQL 10 for logical replication.

**Code:**
```sql
-- define which tables to replicate
CREATE PUBLICATION my_pub FOR TABLE t1;

-- subscriber that pulls the changes
CREATE SUBSCRIPTION my_sub
  CONNECTION 'host=pg1 dbname=mydb user=repl'
  PUBLICATION my_pub;
```

## Q46: What are partitions in PostgreSQL?
**A:** Partitioning splits a large table into smaller physical pieces (partitions) while querying the parent table. Types: Range (by date range), List (by discrete values), Hash (by hash of key). Available since PostgreSQL 10 (declarative partitioning).

**Code:**
```sql
CREATE TABLE sales (id BIGSERIAL, created_at DATE, region TEXT, total NUMERIC)
  PARTITION BY RANGE (created_at);

CREATE TABLE sales_2024 PARTITION OF sales
  FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE sales_2025 PARTITION OF sales
  FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
```

## Q47: What is table inheritance in PostgreSQL?
**A:** Table inheritance allows a child table to inherit columns from a parent table. `CREATE TABLE child () INHERITS (parent)`. Different from partitioning — inheritance is more flexible but less performant for large-scale data management.

**Code:**
```sql
CREATE TABLE parent (id SERIAL, name TEXT);
CREATE TABLE child () INHERITS (parent);

INSERT INTO child (name) VALUES ('Ada');
SELECT * FROM parent;      -- includes the child row
SELECT * FROM ONLY parent; -- parent rows only
```

## Q48: What is the `pg_hba.conf` file?
**A:** `pg_hba.conf` (Host-Based Authentication) controls client authentication. It specifies allowed hosts, databases, users, authentication methods (password, md5, scram-sha-256, trust, cert, LDAP), and connection types (local, host, hostssl).

**Code:**
```bash
# TYPE  DATABASE  USER  ADDRESS      METHOD
host    all       all   127.0.0.1/32 scram-sha-256
hostssl all       all   10.0.0.0/8   scram-sha-256
```
```sql
SELECT type, database, user_name, address, auth_method
FROM pg_hba_file_rules;
```

## Q49: What is `postgresql.conf`?
**A:** `postgresql.conf` is the main configuration file for PostgreSQL. Settings include memory (shared_buffers, work_mem, maintenance_work_mem), connections (max_connections), logging (log_statement, log_line_prefix), WAL, replication, and autovacuum.

**Code:**
```sql
SHOW shared_buffers;
SHOW max_connections;
SHOW log_statement;
```

## Q50: What is `shared_buffers`?
**A:** `shared_buffers` is the amount of memory PostgreSQL uses for caching data. Typical recommendation is 25% of RAM (or up to 40% for dedicated DB servers). Too low causes excessive disk reads; too high may cause OS caching conflicts.

**Code:**
```sql
SHOW shared_buffers;                       -- e.g. 4GB
ALTER SYSTEM SET shared_buffers = '6GB';   -- requires restart
```

## Q51: What is `work_mem`?
**A:** `work_mem` is memory used for internal sort operations and hash tables (per operation, not per session). High values speed up sorts and joins but risk out-of-memory errors if too many operations run concurrently.

**Code:**
```sql
SHOW work_mem;                          -- default 4MB
SET work_mem = '128MB';                 -- per sort/hash operation
```

## Q52: What is `maintenance_work_mem`?
**A:** `maintenance_work_mem` is memory available for maintenance operations like VACUUM, CREATE INDEX, and ALTER TABLE ADD FOREIGN KEY. Higher values speed up these operations. Can be set higher than work_mem without risk.

**Code:**
```sql
SHOW maintenance_work_mem;
SET maintenance_work_mem = '1GB';
VACUUM;
```

## Q53: What is `effective_cache_size`?
**A:** `effective_cache_size` is an estimate of how much memory the OS and PostgreSQL combined use for file system caching. It's used by the query planner to estimate whether index scans are cheaper than sequential scans.

**Code:**
```sql
SHOW effective_cache_size;
ALTER SYSTEM SET effective_cache_size = '12GB';
SELECT pg_reload_conf();
```

## Q54: What is `random_page_cost`?
**A:** `random_page_cost` is the planner's estimate of the cost of a non-sequential (random) disk page fetch. Default is 4.0. For SSD storage, lower to 1.0–1.5 to encourage index scans over sequential scans.

**Code:**
```sql
SHOW random_page_cost;                       -- 4.0 default (HDD)
ALTER SYSTEM SET random_page_cost = 1.1;     -- SSD friendly
SELECT pg_reload_conf();
```

## Q55: What is connection limit in PostgreSQL?
**A:** `max_connections` (default 100) limits concurrent connections. Each connection consumes ~10MB of memory. Connection pooling (PgBouncer) allows handling thousands of clients without overwhelming the database.

**Code:**
```sql
SHOW max_connections;
ALTER ROLE app_user CONNECTION LIMIT 25;
SELECT count(*) FROM pg_stat_activity;
```

## Q56: What is a foreign key in PostgreSQL?
**A:** A foreign key enforces referential integrity between two tables. `FOREIGN KEY (col) REFERENCES parent(col)`. Options: `ON DELETE CASCADE`, `ON UPDATE SET NULL`, `ON DELETE RESTRICT`. Ensures child rows have valid parent references.

**Code:**
```sql
CREATE TABLE parent (id INT PRIMARY KEY, name TEXT);
CREATE TABLE child (
  parent_id INT REFERENCES parent(id) ON DELETE CASCADE
);
```

## Q57: What is a `CHECK` constraint?
**A:** A `CHECK` constraint ensures values in a column satisfy a boolean expression. `CHECK (age >= 0 AND age <= 150)`. Enforced at the row level. Can reference multiple columns.

**Code:**
```sql
CREATE TABLE users (
  email TEXT,
  age INT CHECK (age >= 0 AND age <= 150),
  CONSTRAINT chk_email CHECK (email ~* '^.+@.+$')
);
```

## Q58: What is the `EXCLUDE` constraint?
**A:** The `EXCLUDE` constraint ensures that if any two rows are compared on specified columns/expressions, not all comparisons are equal (using GiST or SP-GiST). Useful for preventing overlapping date ranges: `EXCLUDE USING gist (period WITH &&)`.

**Code:**
```sql
CREATE EXTENSION btree_gist;

CREATE TABLE bookings (
  room_id INT,
  period TSRANGE,
  EXCLUDE USING gist (room_id WITH =, period WITH &&)
);
```

## Q59: What is `COPY` command in PostgreSQL?
**A:** `COPY` bulk-loads data from/to a file or stdin/stdout. `COPY table FROM 'file.csv' DELIMITER ',' CSV HEADER`. Much faster than INSERT for large datasets. `\copy` is the psql meta-command version.

**Code:**
```sql
COPY users (name, email)
FROM '/tmp/users.csv' DELIMITER ',' CSV HEADER;

COPY users TO STDOUT WITH (FORMAT csv, HEADER true);
```

## Q60: What is `pg_bulkload`?
**A:** `pg_bulkload` is an extension for high-speed data loading that bypasses shared buffers and WAL (in some modes). Used for very large initial data loads where transaction safety can be sacrificed for speed.

**Code:**
```sql
-- pg_bulkload control file
OUTPUT = users
INPUT = /data/users.csv
DELIMITER = ,
TYPE = CSV
```
```bash
pg_bulkload -d mydb -i /etc/pgbulkload.conf
```

## Q61: What is full-text search in PostgreSQL?
**A:** PostgreSQL's full-text search uses `tsvector` (document representation with lexemes) and `tsquery` (search query). Operators: `@@` (match), `||` (concatenate). Supports ranking (`ts_rank`), stemming, dictionaries, and GIN indexes.

**Code:**
```sql
SELECT title
FROM articles
WHERE to_tsvector('english', title || ' ' || body)
      @@ to_tsquery('english', 'database & indexing')
ORDER BY ts_rank(to_tsvector('english', title), to_tsquery('english', 'database & indexing')) DESC;
```

## Q62: What is `tsvector` and `tsquery`?
**A:** `to_tsvector('english', 'The quick brown fox')` generates a `tsvector` (normalized lexemes with positions). `to_tsquery('english', 'quick & brown')` generates a `tsquery`. Match: `tsvector @@ tsquery`.

**Code:**
```sql
SELECT to_tsvector('english', 'The quick brown fox');
SELECT to_tsquery('english', 'quick & brown');
SELECT to_tsvector('english', 'The quick brown fox') @@ to_tsquery('english', 'quick & brown');
```

## Q63: What are PostgreSQL extensions?
**A:** Extensions add functionality. Common ones: `pg_stat_statements` (query stats), `uuid-ossp` (UUID generation), `postgis` (geospatial), `pgcrypto` (cryptographic functions), `hstore` (key-value), `pg_trgm` (trigram text search).

**Code:**
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS hstore;

SELECT gen_random_uuid();
```

## Q64: How do you enable an extension?
**A:** `CREATE EXTENSION extension_name;` (requires `CREATE` privilege on the database). Extensions must be installed (files in `SHAREDIR/extension/`) and available via `SELECT * FROM pg_available_extensions`.

**Code:**
```sql
CREATE EXTENSION pg_trgm;
SELECT * FROM pg_available_extensions WHERE name = 'pg_trgm';
```

## Q65: What is `pg_stat_activity`?
**A:** `pg_stat_activity` is a system view showing all server processes/connections. It shows query text, state (active, idle, idle in transaction), wait events, application name, client address, and backend start time.

**Code:**
```sql
SELECT pid, usename, state, wait_event, query_start, query
FROM pg_stat_activity
WHERE state = 'active';
```

## Q66: How do you kill a query in PostgreSQL?
**A:** `SELECT pg_cancel_backend(pid)` cancels a running query (graceful cancellation). `SELECT pg_terminate_backend(pid)` terminates the entire backend process (forceful). Find the pid from `pg_stat_activity`.

**Code:**
```sql
SELECT pid, query FROM pg_stat_activity WHERE state = 'active';

SELECT pg_cancel_backend(12345);      -- cancel a running query
SELECT pg_terminate_backend(12345);   -- kill the backend entirely
```

## Q67: What is a deadlock in PostgreSQL?
**A:** A deadlock occurs when two or more transactions hold locks that each other needs. PostgreSQL detects deadlocks automatically (via the deadlock detection process) and aborts one transaction with a `deadlock detected` error.

**Code:**
```sql
-- Session 1
BEGIN;
UPDATE accounts SET balance = 0 WHERE id = 1;
-- Session 2
BEGIN;
UPDATE accounts SET balance = 0 WHERE id = 2;
-- Session 1 now wants row 2, Session 2 wants row 1 -> deadlock detected
UPDATE accounts SET balance = 0 WHERE id = 2;
```

## Q68: What is the difference between `LOCK` and `FOR UPDATE`?
**A:** `LOCK TABLE` locks the entire table at a specified level (ACCESS SHARE, ROW EXCLUSIVE, etc.). `SELECT ... FOR UPDATE` locks only the selected rows, preventing concurrent updates or deletions of those specific rows.

**Code:**
```sql
BEGIN;
LOCK TABLE accounts IN ACCESS EXCLUSIVE MODE;   -- entire table
SELECT * FROM accounts WHERE id = 1 FOR UPDATE; -- specific rows
COMMIT;
```

## Q69: What is advisory lock in PostgreSQL?
**A:** Advisory locks are application-level locks that don't relate to table rows. `pg_advisory_lock(key)` and `pg_advisory_unlock(key)`. Useful for coordinating access to external resources or implementing custom concurrency control.

**Code:**
```sql
SELECT pg_advisory_lock(1234);
-- ... critical section ...
SELECT pg_advisory_unlock(1234);

SELECT pg_try_advisory_lock(99);  -- non-blocking variant
```

## Q70: What is `LISTEN` and `NOTIFY`?
**A:** `NOTIFY channel, payload` sends a notification. `LISTEN channel` subscribes to notifications. Used for real-time event notification between database sessions — useful for cache invalidation, triggering background workers, etc.

**Code:**
```sql
-- Session 1
LISTEN my_channel;

-- Session 2
NOTIFY my_channel, '{"user_id": 1}';
```

## Q71: What is the `pg_notify` channel?
**A:** `pg_notify` is a built-in channel mechanism. Applications (via drivers like `pg` for Node.js, `psycopg2` for Python) can `LISTEN` and receive async notifications without polling the database.

**Code:**
```python
import psycopg2
import select

conn = psycopg2.connect("dbname=mydb")
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
cur.execute("LISTEN user_changes")
select.select([conn], [], [])
conn.poll()
print(conn.notifies[0].payload)
```

## Q72: How do you handle date/time in PostgreSQL?
**A:** Types: `DATE`, `TIME`, `TIMESTAMP` (without timezone), `TIMESTAMPTZ` (with timezone), `INTERVAL`. Functions: `NOW()`, `CURRENT_DATE`, `EXTRACT()`, `DATE_TRUNC()`, `AGE()`. Always prefer `TIMESTAMPTZ` for storing absolute time.

**Code:**
```sql
SELECT NOW(),
       CURRENT_DATE,
       EXTRACT(YEAR FROM NOW()),
       DATE_TRUNC('month', NOW()),
       NOW() - INTERVAL '1 day' AS yesterday;
```

## Q73: What is `TIMESTAMPTZ`?
**A:** `TIMESTAMP WITH TIME ZONE` (timestamptz) stores values internally as UTC and converts to the client's timezone on display. The timezone offset is not stored; the value is normalized to UTC. The best choice for storing global timestamps.

**Code:**
```sql
SET timezone = 'UTC';
SELECT '2024-06-15 12:00:00+05:30'::timestamptz;   -- stored as UTC
SET timezone = 'America/New_York';
SELECT '2024-06-15 12:00:00+05:30'::timestamptz;   -- rendered in session TZ
```

## Q74: What is `DATE_TRUNC`?
**A:** `DATE_TRUNC('month', timestamp)` truncates a timestamp to a specified precision (microsecond, second, minute, hour, day, week, month, quarter, year, decade, century, millennium). Used for grouping time-series data.

**Code:**
```sql
SELECT DATE_TRUNC('month', TIMESTAMP '2024-06-15 12:34:56');  -- 2024-06-01
SELECT DATE_TRUNC('hour', NOW());
```

## Q75: What is an enum in PostgreSQL?
**A:** `CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy')` creates an enumerated type with a fixed set of values. Enums are stored compactly (4 bytes) and support ordering. Altering enums requires `ALTER TYPE ... ADD VALUE`.

**Code:**
```sql
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy');
CREATE TABLE person (name TEXT, current_mood mood);
INSERT INTO person VALUES ('Ada', 'happy');
ALTER TYPE mood ADD VALUE 'ecstatic';
SELECT * FROM person WHERE current_mood > 'ok';
```

## Q76: What is a composite type in PostgreSQL?
**A:** Composite types (row types) represent a structure of multiple fields. `CREATE TYPE address AS (street TEXT, city TEXT, zip TEXT)`. Used for function return types, table columns, and passing structured data in functions.

**Code:**
```sql
CREATE TYPE address AS (street TEXT, city TEXT, zip TEXT);
CREATE TABLE person (name TEXT, home address);
INSERT INTO person VALUES ('Ada', ROW('1 Main St', 'Springfield', '12345'));
SELECT (home).city FROM person;
```

## Q77: What are domain types in PostgreSQL?
**A:** Domains are custom types based on existing types with constraints. `CREATE DOMAIN email AS TEXT CHECK (VALUE ~* '^.+@.+\\..+$')`. They enforce business rules at the column level across multiple tables.

**Code:**
```sql
CREATE DOMAIN email AS TEXT CHECK (VALUE ~* '^.+@.+\.+$');

CREATE TABLE users (id SERIAL, contact email);
INSERT INTO users (contact) VALUES ('ada@example.com');  -- ok
INSERT INTO users (contact) VALUES ('not-an-email');     -- fails CHECK
```

## Q78: What are range types in PostgreSQL?
**A:** Range types represent intervals: `int4range`, `int8range`, `numrange`, `tsrange`, `tstzrange`, `daterange`. Operators: `@>` (contains), `&&` (overlaps), `<<` (strictly left of), `-|-` (adjacent). GiST index supports efficient queries.

**Code:**
```sql
SELECT '[2024-01-01, 2024-02-01)'::tsrange @> '2024-01-15'::timestamp AS contains;
SELECT int4range(1, 10) && int4range(5, 15) AS overlaps;
SELECT daterange('2024-01-01', '2024-01-10') -|- daterange('2024-01-10', '2024-01-20') AS adjacent;
```

## Q79: What is `array_agg` function?
**A:** `array_agg(column)` aggregates values into an array. `SELECT dept_id, array_agg(employee_name ORDER BY salary DESC) FROM employees GROUP BY dept_id`. Inverse of `unnest()`.

**Code:**
```sql
SELECT dept_id, array_agg(name ORDER BY salary DESC) AS employees
FROM employees
GROUP BY dept_id;
```

## Q80: What is `unnest` function?
**A:** `unnest(array)` expands an array into a set of rows. `SELECT unnest(ARRAY[1,2,3])` returns three rows. Used for flattening arrays or joining arrays with table data.

**Code:**
```sql
SELECT unnest(ARRAY[1, 2, 3]) AS n;
SELECT id, unnest(tags) AS tag FROM posts;
```

## Q81: What is the `COALESCE` function?
**A:** `COALESCE(value1, value2, ..., default)` returns the first non-NULL value. `COALESCE(NULL, NULL, 'fallback')` returns 'fallback'. Equivalent to `NVL` in Oracle or `IFNULL` in MySQL.

**Code:**
```sql
SELECT COALESCE(NULL, NULL, 'fallback');            -- 'fallback'
SELECT COALESCE(email, phone, 'unknown') FROM users;
```

## Q82: What is the `NULLIF` function?
**A:** `NULLIF(expr1, expr2)` returns NULL if the two expressions are equal, otherwise returns expr1. Useful for preventing division by zero: `x / NULLIF(y, 0)`.

**Code:**
```sql
SELECT SUM(x / NULLIF(y, 0)) FROM metrics;   -- avoids division-by-zero
SELECT NULLIF('a', 'a');                      -- NULL
SELECT NULLIF(5, 3);                          -- 5
```

## Q83: What is the `GREATEST` and `LEAST` functions?
**A:** `GREATEST(val1, val2, ...)` returns the largest value. `LEAST(val1, val2, ...)` returns the smallest. They work across multiple columns or expressions.

**Code:**
```sql
SELECT GREATEST(1, 5, 3) AS max_val,   -- 5
       LEAST(1, 5, 3) AS min_val;      -- 1
```

## Q84: What is the `FILTER` clause in aggregate functions?
**A:** `FILTER (WHERE condition)` allows aggregating only a subset of rows. `SELECT COUNT(*) FILTER (WHERE status = 'active') AS active_count FROM users`. More efficient than CASE-based conditional aggregation.

**Code:**
```sql
SELECT COUNT(*) FILTER (WHERE status = 'active')  AS active,
       COUNT(*) FILTER (WHERE status = 'banned')  AS banned
FROM users;
```

## Q85: What is the `DISTINCT ON` clause?
**A:** `SELECT DISTINCT ON (column1) column1, column2 FROM table ORDER BY column1, column2` returns the first row for each unique value of column1. Useful for deduplication (e.g., latest order per customer).

**Code:**
```sql
-- newest order per customer
SELECT DISTINCT ON (customer_id) customer_id, order_id, created_at
FROM orders
ORDER BY customer_id, created_at DESC;
```

## Q86: What is `RETURNING` in INSERT/UPDATE/DELETE?
**A:** `INSERT INTO table VALUES (...) RETURNING *` returns the inserted row. `DELETE FROM table WHERE id = 1 RETURNING id` returns deleted data. Useful for getting auto-generated values or auditing.

**Code:**
```sql
INSERT INTO users (email) VALUES ('a@b.c') RETURNING id;
UPDATE users SET status = 'active' WHERE id = 1 RETURNING id, status;
DELETE FROM users WHERE id = 1 RETURNING email;
```

## Q87: What is `FOR SHARE` vs `FOR UPDATE`?
**A:** `FOR UPDATE` locks selected rows for update (prevents other transactions from updating/deleting/locking them). `FOR SHARE` locks selected rows for shared access (prevents updates/deletions but allows other shared locks).

**Code:**
```sql
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;  -- exclusive write lock
SELECT * FROM accounts WHERE id = 2 FOR SHARE;   -- shared read lock
COMMIT;
```

## Q88: What is `SKIP LOCKED`?
**A:** `SELECT ... FOR UPDATE SKIP LOCKED` skips rows that are already locked by other transactions. Useful for implementing job queues where multiple workers pick unprocessed items without contention.

**Code:**
```sql
-- each worker grabs a distinct pending job without waiting
SELECT * FROM jobs
WHERE status = 'pending'
ORDER BY id
LIMIT 1
FOR UPDATE SKIP LOCKED;
```

## Q89: What is `NOWAIT`?
**A:** `SELECT ... FOR UPDATE NOWAIT` fails immediately if the row is locked (instead of waiting). Returns an error. `FOR UPDATE WAIT seconds` (PostgreSQL 15+) allows specifying a timeout.

**Code:**
```sql
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE NOWAIT;  -- error if row is locked
COMMIT;
```

## Q90: What are foreign data wrappers (FDW)?
**A:** FDW allows querying external data sources (other PostgreSQL databases, MySQL, CSV files, web APIs) as if they were local tables. Implemented via the `postgres_fdw` extension and others.

**Code:**
```sql
CREATE EXTENSION postgres_fdw;

CREATE SERVER remote FOREIGN DATA WRAPPER postgres_fdw
  OPTIONS (host 'db2', dbname 'analytics');

CREATE USER MAPPING FOR CURRENT_USER SERVER remote
  OPTIONS (user 'etl', password 'secret');

CREATE FOREIGN TABLE ft_orders (id INT, total NUMERIC)
  SERVER remote OPTIONS (table_name 'orders');

SELECT * FROM ft_orders;
```

## Q91: What is `postgres_fdw`?
**A:** `postgres_fdw` is the built-in foreign data wrapper for accessing remote PostgreSQL servers. `CREATE SERVER`, `CREATE USER MAPPING`, `CREATE FOREIGN TABLE`. Supports pushdown of WHERE conditions and joins.

**Code:**
```sql
CREATE EXTENSION postgres_fdw;

CREATE SERVER srv FOREIGN DATA WRAPPER postgres_fdw
  OPTIONS (host 'remote', port '5432', dbname 'mydb');

CREATE USER MAPPING FOR CURRENT_USER SERVER srv
  OPTIONS (user 'app', password 'pw');

CREATE FOREIGN TABLE ft_users (id INT, name TEXT)
  SERVER srv OPTIONS (schema_name 'public', table_name 'users');

SELECT * FROM ft_users WHERE id = 1;   -- WHERE pushed to the remote server
```

## Q92: What is `pg_dump` vs `pg_dumpall`?
**A:** `pg_dump` backs up a single database (in custom, tar, directory, or plain/text format). `pg_dumpall` backs up all databases plus cluster-wide objects (roles, tablespaces). Use `pg_restore` for custom/tar/directory formats.

**Code:**
```bash
pg_dump -d mydb -Fc > mydb.dump
pg_dumpall > all.sql
pg_restore -d mydb mydb.dump
```

## Q93: What is replication slot?
**A:** A replication slot ensures the primary retains WAL segments needed by subscribers/replicas, preventing premature WAL removal. Required for logical replication and some streaming replication setups.

**Code:**
```sql
SELECT slot_name, slot_type, active, restart_lsn
FROM pg_replication_slots;

SELECT * FROM pg_create_logical_replication_slot('myslot', 'pgoutput');
```

## Q94: What is `pg_wal` directory?
**A:** `pg_wal` (formerly `pg_xlog`) stores WAL segment files (typically 16 MB each). WAL files are written sequentially and archived for PITR. Monitoring WAL generation rate helps size archive storage.

**Code:**
```sql
SELECT * FROM pg_ls_waldir() ORDER BY name;
SELECT pg_walfile_name(pg_current_wal_lsn()) AS active_wal;
```

## Q95: What is `CHECKPOINT` in PostgreSQL?
**A:** A checkpoint flushes all dirty buffers (modified data pages) from shared_buffers to disk, updates the control file. It shortens crash recovery time. Checkpoints occur based on `checkpoint_timeout` or `max_wal_size`.

**Code:**
```sql
CHECKPOINT;
SELECT last_checkpoint_time FROM pg_control_checkpoint();
```

## Q96: What is the `EXPLAIN` output showing a "Seq Scan"?
**A:** A sequential scan reads every row in the table sequentially. It's efficient for small tables or when most rows match. For large tables, it indicates a missing index or a query that would benefit from one.

**Code:**
```sql
EXPLAIN SELECT * FROM users WHERE NOT verified;
-- Seq Scan on users (cost=0.00..15.10 rows=100 width=41)
```

## Q97: What is parallel query in PostgreSQL?
**A:** Parallel queries utilize multiple CPU cores for query execution. Supported for sequential scans, joins (hash join, nested loop), and aggregates. Controlled by `max_parallel_workers_per_gather` and `parallel_tuple_cost`.

**Code:**
```sql
SET max_parallel_workers_per_gather = 4;

EXPLAIN SELECT COUNT(*) FROM orders;
-- Gather / Partial Seq Scan indicates parallel execution
```

## Q98: What is JIT compilation in PostgreSQL?
**A:** Just-In-Time (JIT) compilation (available since PostgreSQL 11 with LLVM support) compiles query expressions to native code, speeding up CPU-bound queries. Controlled by `jit` and `jit_above_cost` settings.

**Code:**
```sql
SHOW jit;                              -- on/off
EXPLAIN ANALYZE SELECT SUM(a * b) FROM metrics WHERE c > 100;
-- plan shows "JIT: <functions/functions: ...>" section
```

## Q99: What are common PostgreSQL monitoring tools?
**A:** pgAdmin (GUI), pg_stat_statements (built-in), pgBadger (log analyzer), pg_top, pgHero, Grafana with postgres_exporter, Prometheus, Datadog, and New Relic PostgreSQL integration.

**Code:**
```sql
SELECT * FROM pg_stat_database;
SELECT query, calls, total_exec_time FROM pg_stat_statements ORDER BY total_exec_time DESC;
```

## Q100: How do you troubleshoot a slow PostgreSQL query?
**A:** Steps: 1) Run `EXPLAIN ANALYZE` to identify bottlenecks. 2) Check for missing indexes (Seq Scan on large tables). 3) Review `pg_stat_statements` for high-total-time queries. 4) Check server configuration (shared_buffers, work_mem). 5) Examine table bloat (VACUUM needed). 6) Check for lock contention in `pg_stat_activity`. 7) Analyze recent schema/data changes.

**Code:**
```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE customer_id = 7;

SELECT calls, total_exec_time, rows, query
FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 5;

SELECT pid, wait_event_type, wait_event, state, query
FROM pg_stat_activity WHERE state = 'active';
```
