# Database (SQL + NoSQL) — 400+ Interview Questions & Answers

> YC / Top-Company Level. Detailed answers with SQL queries & code examples.

---

## Table of Contents

1. [SQL & Relational Databases (Q1–Q150)](#sql--relational-databases-q1-q150)
2. [PostgreSQL Deep (Q151–Q220)](#postgresql-deep-q151-q220)
3. [NoSQL & MongoDB (Q221–Q300)](#nosql--mongodb-q221-q300)
4. [Database Design & Architecture (Q301–Q350)](#database-design--architecture-q301-q350)
5. [Interview Query Problems (Q351–Q400)](#interview-query-problems-q351-q400)

---

# SQL & Relational Databases (Q1–Q150)

### Q1: What is a database?
A database is an organized collection of structured data stored electronically. Examples: MySQL, PostgreSQL, Oracle, SQLite.

### Q2: What is DBMS?
A Database Management System (DBMS) is software that interacts with end users, applications, and the database itself to capture and analyze data. It provides CRUD operations, security, concurrency, and recovery.

### Q3: What is RDBMS? How is it different from DBMS?
RDBMS (Relational DBMS) stores data in tables with rows and columns, enforces schema, supports relationships via foreign keys, and guarantees ACID. DBMS is broader — includes hierarchical, network, and NoSQL systems.

| Feature | DBMS | RDBMS |
|---------|------|-------|
| Storage | Files, hierarchical, network | Tables (relations) |
| Relationships | Pointers/links | Foreign keys + JOINs |
| Normalization | Not enforced | Supported |
| ACID | Not guaranteed | Guaranteed (most) |
| Example | MongoDB, Redis | PostgreSQL, MySQL |

### Q4: What are ACID properties?
- **Atomicity**: A transaction is all-or-nothing. If any part fails, the whole transaction rolls back.
- **Consistency**: A transaction brings the database from one valid state to another, respecting all constraints/rules.
- **Isolation**: Concurrent transactions execute as if they were serialized (one after another).
- **Durability**: Once committed, data persists even after a system crash.

### Q5: Explain Atomicity with an example.
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```
If the second UPDATE fails, the first is rolled back automatically.

### Q6: Explain Consistency with an example.
```sql
-- If balance >= 0 is a constraint:
CHECK (balance >= 0)

BEGIN;
UPDATE accounts SET balance = balance - 200 WHERE id = 1; -- balance becomes -50, violates CHECK
COMMIT; -- fails, transaction rolls back
```

### Q7: Explain Isolation with an example.
Two concurrent transactions see data as if they ran one at a time. The level of isolation depends on the isolation level.

### Q8: Explain Durability with an example.
After `COMMIT`, data is written to disk (WAL — Write-Ahead Log). Even if the power fails immediately after, the data is recovered on restart.

### Q9: What is Normalization?
Normalization organizes data to reduce redundancy and dependency by dividing large tables into smaller related tables.

### Q10: What is 1NF (First Normal Form)?
- Each column contains atomic (indivisible) values
- Each column contains values of a single type
- Each row is unique

**Before 1NF:**
| id | name | phones |
|----|------|--------|
| 1 | Alice | 123, 456 |

**After 1NF:**
| id | name | phone |
|----|------|-------|
| 1 | Alice | 123 |
| 1 | Alice | 456 |

### Q11: What is 2NF (Second Normal Form)?
- In 1NF
- Every non-key column is fully functionally dependent on the entire primary key (no partial dependency)

### Q12: What is 3NF (Third Normal Form)?
- In 2NF
- No transitive dependency (non-key column does not depend on another non-key column)

### Q13: What is BCNF (Boyce-Codd Normal Form)?
- A stronger version of 3NF where for every functional dependency X → Y, X must be a super key.

### Q14: What is Denormalization? When and why?
Denormalization intentionally adds redundancy by combining tables to improve read performance. Used in read-heavy systems, reporting, analytics.

### Q15: What is a Primary Key?
A column (or set of columns) that uniquely identifies each row. Must be NOT NULL and UNIQUE.
```sql
CREATE TABLE users (id BIGSERIAL PRIMARY KEY, email VARCHAR(255) UNIQUE NOT NULL);
```

### Q16: What is a Foreign Key?
A column that references a Primary Key in another table, enforcing referential integrity.
```sql
CREATE TABLE orders (id BIGSERIAL PRIMARY KEY, user_id BIGINT REFERENCES users(id), amount DECIMAL(10,2));
```

### Q17: What is a Unique Key?
Ensures all values in a column (or column set) are distinct. Allows NULLs (one NULL allowed in most RDBMS).
```sql
CREATE TABLE users (id BIGSERIAL PRIMARY KEY, email VARCHAR(255) UNIQUE, username VARCHAR(100) UNIQUE);
```

### Q18: What is a Composite Key?
A primary/unique key consisting of multiple columns.
```sql
CREATE TABLE order_items (order_id BIGINT, product_id BIGINT, quantity INT, PRIMARY KEY (order_id, product_id));
```

### Q19: What is an Index?
A data structure that speeds up data retrieval at the cost of slower writes and extra storage.
```sql
CREATE INDEX idx_users_email ON users(email);
```

### Q20: How does a B-tree index work?
B-tree is a balanced tree data structure. Keys are stored in sorted order. Leaf nodes contain pointers to actual rows. Search, insert, delete are O(log n).

### Q21: How does a Hash index work?
Hash indexes apply a hash function to the key and store the hash → pointer mapping. Only supports equality lookups (`=`), not range queries (`<`, `>`).

### Q22: What is a Clustered Index?
The index determines the physical order of data in the table. A table can have only one clustered index. InnoDB uses the primary key as clustered index by default.

### Q23: What is a Non-Clustered Index?
A separate structure that contains index keys and pointers to the actual rows. A table can have many non-clustered indexes.
```sql
CREATE INDEX idx_name ON users(name);
```

### Q24: What is a Composite Index?
An index on multiple columns. Column order matters.
```sql
CREATE INDEX idx_name_age ON users(name, age);
```

### Q25: When do indexes help?
- Filtering: `WHERE`, `HAVING`
- Joining: `JOIN ... ON`
- Sorting: `ORDER BY`
- Aggregation: `GROUP BY`
- Uniqueness enforcement: `UNIQUE`, `PRIMARY KEY`

### Q26: When do indexes hurt?
- Slow writes: Every `INSERT`, `UPDATE`, `DELETE` must update the index
- Storage overhead
- Low-cardinality columns: Indexing a boolean column rarely helps
- Small tables: Full table scan is faster

### Q27: What is EXPLAIN? How to read query plans?
EXPLAIN shows how the database executes a query — which indexes it uses, join order, estimated costs.
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'alice@x.com';
```

### Q28: What is an INNER JOIN?
Returns rows where there is a match in both tables.
```sql
SELECT u.name, o.amount FROM users u INNER JOIN orders o ON u.id = o.user_id;
```

### Q29: What is a LEFT JOIN?
Returns all rows from the left table and matching rows from the right. NULLs for non-matches.

### Q30: What is a RIGHT JOIN?
Same as LEFT JOIN but preserves all rows from the right table.

### Q31: What is a FULL OUTER JOIN?
Returns all rows from both tables, with NULLs where there is no match.
```sql
SELECT u.name, o.amount FROM users u FULL OUTER JOIN orders o ON u.id = o.user_id;
```

### Q32: What is a CROSS JOIN?
Cartesian product — every row from table A matched with every row from table B.

### Q33: What is a SELF JOIN?
Joining a table with itself using aliases.
```sql
SELECT e1.name AS employee, e2.name AS manager FROM employees e1 LEFT JOIN employees e2 ON e1.manager_id = e2.id;
```

### Q34: JOIN vs Subquery — which is faster?
JOINs are generally faster because the optimizer can materialize and index the joined results. However, correlated subqueries can sometimes be optimized into JOINs.

### Q35: What is GROUP BY?
Groups rows that have the same values in specified columns, allowing aggregate calculations per group.
```sql
SELECT user_id, COUNT(*) AS order_count, SUM(amount) AS total_spent FROM orders GROUP BY user_id;
```

### Q36: What is HAVING?
Filters groups after aggregation (unlike WHERE, which filters before aggregation).
```sql
SELECT user_id, COUNT(*) AS order_count FROM orders GROUP BY user_id HAVING COUNT(*) > 5;
```

### Q37: What are aggregate functions?
- `COUNT(*)` — counts rows
- `SUM(column)` — sum of values
- `AVG(column)` — average
- `MIN(column)` — minimum
- `MAX(column)` — maximum
- `STRING_AGG(column, delimiter)` — concatenates values (PostgreSQL)
- `ARRAY_AGG(column)` — aggregates into array

### Q38: WHERE vs HAVING — what's the difference?
- `WHERE` filters rows **before** aggregation (on raw data)
- `HAVING` filters groups **after** aggregation

### Q39: What is ORDER BY?
Sorts result set.
```sql
SELECT * FROM users ORDER BY created_at DESC;
```

### Q40: What is LIMIT and OFFSET?
`LIMIT` restricts rows returned; `OFFSET` skips rows.
```sql
SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 20;
```

### Q41: How to paginate efficiently? (Offset vs Cursor)
**Offset pagination** (bad for large offsets): `SELECT * FROM posts ORDER BY id LIMIT 10 OFFSET 100000;`
**Cursor-based pagination** (efficient): `SELECT * FROM posts WHERE id > last_seen_id ORDER BY id LIMIT 10;`

### Q42: What is UNION?
Combines result sets of two queries, removing duplicates.
```sql
SELECT name FROM employees UNION SELECT name FROM contractors;
```

### Q43: What is UNION ALL?
Same as UNION but keeps duplicate rows (faster).

### Q44: What is INTERSECT?
Returns rows common to both queries.
```sql
SELECT user_id FROM orders_2023 INTERSECT SELECT user_id FROM orders_2024;
```

### Q45: What is EXCEPT?
Returns rows from the first query that are NOT in the second.
```sql
SELECT user_id FROM orders_2023 EXCEPT SELECT user_id FROM orders_2024;
```

### Q46: What is a View?
A saved query that acts like a virtual table. Useful for encapsulating complex logic, security, and reusability.
```sql
CREATE VIEW active_users AS SELECT id, name, email FROM users WHERE deleted_at IS NULL AND email_verified = TRUE;
```

### Q47: Why use Views?
- Security: expose only specific columns
- Simplification: encapsulate complex JOINs
- Consistency: reusable logic

### Q48: What is a Materialized View?
A view whose result set is physically stored (snapshot). Refreshed manually or on schedule. Faster reads but stale data.
```sql
CREATE MATERIALIZED VIEW monthly_sales AS SELECT DATE_TRUNC('month', order_date) AS month, SUM(amount) AS total_sales FROM orders GROUP BY 1;
REFRESH MATERIALIZED VIEW monthly_sales;
```

### Q49: What is a Stored Procedure?
A pre-compiled collection of SQL statements with procedural logic (IF, loops, variables).
```sql
CREATE PROCEDURE transfer_funds(from_id INT, to_id INT, amount DECIMAL) LANGUAGE plpgsql AS $$
BEGIN
  UPDATE accounts SET balance = balance - amount WHERE id = from_id;
  UPDATE accounts SET balance = balance + amount WHERE id = to_id;
  COMMIT;
END;
$$;
```

### Q50: What is a Function? (vs Stored Procedure)
Functions return a value and can be used in SQL expressions. Stored procedures do not return values.
```sql
CREATE FUNCTION get_employee_count(dept_id INT) RETURNS INT LANGUAGE SQL AS $$
  SELECT COUNT(*) FROM employees WHERE department_id = dept_id;
$$;
```

### Q51: What is a Trigger?
Code that automatically runs before/after an event (INSERT, UPDATE, DELETE) on a table.
```sql
CREATE TRIGGER set_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_timestamp();
```

### Q52: Stored Procedure vs Function vs Trigger — when to use?
- **Stored Procedure**: Complex business logic, batch operations
- **Function**: Computed values, reusable SQL logic inside queries
- **Trigger**: Audit logs, cascading updates, validation

### Q53: What is a Transaction?
A sequence of operations executed as a single unit of work, with ACID guarantees.
```sql
BEGIN; UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 100; INSERT INTO orders (user_id, product_id) VALUES (1, 100); COMMIT;
```

### Q54: What does BEGIN do?
Starts a transaction block. Until `COMMIT` or `ROLLBACK`, changes are visible only within the current session.

### Q55: What does COMMIT do?
Makes all changes in the transaction permanent and visible to other transactions.

### Q56: What does ROLLBACK do?
Undoes all changes in the current transaction, restoring the state to before `BEGIN`.

### Q57: What is a SAVEPOINT?
A point within a transaction that you can roll back to without aborting the entire transaction.
```sql
BEGIN; SAVEPOINT sp1; INSERT INTO log (msg) VALUES ('step 2'); ROLLBACK TO SAVEPOINT sp1; COMMIT;
```

### Q58: What isolation levels exist in SQL standard?
1. **Read Uncommitted**: Lowest. Sees uncommitted changes (dirty reads).
2. **Read Committed**: Only sees committed data (prevents dirty reads). PostgreSQL default.
3. **Repeatable Read**: Same read returns same result (prevents non-repeatable reads). MySQL/InnoDB default.
4. **Serializable**: Highest. Transactions execute as if serial.

### Q59: What is a Dirty Read?
Reading uncommitted data from another transaction. Prevented by Read Committed and above.

### Q60: What is a Non-Repeatable Read?
Same query in one transaction returns different results because another transaction committed a change. Prevented by Repeatable Read and above.

### Q61: What is a Phantom Read?
A query returns different sets of rows in the same transaction because another transaction inserted/deleted rows. Prevented by Serializable.

### Q62: What is the difference between Non-Repeatable Read and Phantom Read?
- Non-repeatable read: Same row, different value (UPDATE)
- Phantom read: Different set of rows (INSERT/DELETE)

### Q63: What are the different types of locks?
- **Row-level**: Locks specific rows (most granular)
- **Table-level**: Locks entire table (simplest)
- **Page-level**: Locks a page of data
- **Shared (S)**: Multiple transactions can read; no one can write
- **Exclusive (X)**: Only one transaction can read/write

### Q64: What is a Deadlock?
Two or more transactions each holding locks the other needs, causing infinite wait.
```sql
-- T1 locks row 1, T2 locks row 2. T1 wants row 2, T2 wants row 1 → DEADLOCK
```

### Q65: How to prevent deadlocks?
- Access tables in the same order in all transactions
- Keep transactions short
- Use timeout
- Use deadlock detection

### Q66: What is Connection Pooling?
Reusing database connections instead of opening/closing them per request. Saves TCP handshake overhead and authentication.

### Q67: Why is connection pooling important?
- Creating a new connection costs ~5-50ms
- Databases limit `max_connections` (e.g., 100–500)
- Pooling allows thousands of concurrent requests with a fixed pool

### Q68: What is the N+1 Query Problem?
When you query a list of N items, then issue N additional queries to get related data.
```python
# Bad (N+1):
users = User.query.all()  # 1 query
for user in users:
    orders = Order.query.filter_by(user_id=user.id).all()  # N queries
```
**Fix: Eager loading / JOIN**

### Q69: How to detect N+1?
- Use database query logs
- Look for repetitive queries with same pattern but different IDs
- Use tools: Django Debug Toolbar, Rails Bullet gem

### Q70: What is Database Sharding?
Horizontal partitioning of data across multiple database instances (shards). Each shard holds a subset of data.
- **Horizontal sharding**: Split rows across shards
- **Vertical sharding**: Split columns across shards

### Q71: What is Database Replication?
Copying data from one database server to another.
- **Master-Slave**: One primary handles writes; replicas handle reads
- **Multi-Master**: Multiple primaries accept writes
- **Synchronous**: Write confirmed by replicas before committing
- **Asynchronous**: Write committed immediately; replicas eventually catch up

### Q72: What is SQL Injection? How to prevent?
SQL injection occurs when user input is embedded directly into SQL strings.
```python
# Vulnerable:
query = f"SELECT * FROM users WHERE email = '{email}'"
# Input: email = "' OR '1'='1" → returns ALL users

# Prevention — Parameterized queries:
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
```

### Q73: What are Window Functions?
Functions that perform calculations across a set of rows related to the current row, without collapsing rows.
```sql
SELECT name, department_id, salary, AVG(salary) OVER (PARTITION BY department_id) AS dept_avg FROM employees;
```

### Q74: What is ROW_NUMBER()?
Assigns a unique sequential integer to each row within a partition.
```sql
SELECT name, salary, ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn FROM employees;
```

### Q75: What is RANK()?
Assigns a rank; tied rows get same rank, and the next rank skips a position. (100, 90, 90, 80 → ranks: 1, 2, 2, 4)

### Q76: What is DENSE_RANK()?
Similar to RANK but without gaps. (100, 90, 90, 80 → ranks: 1, 2, 2, 3)

### Q77: What is LAG()?
Accesses data from a previous row (offset) within the same result set.
```sql
SELECT date, revenue, LAG(revenue, 1) OVER (ORDER BY date) AS prev_day_revenue FROM daily_revenue;
```

### Q78: What is LEAD()?
Accesses data from a following row.
```sql
SELECT date, revenue, LEAD(revenue, 1) OVER (ORDER BY date) AS next_day_revenue FROM daily_revenue;
```

### Q79: What is NTILE()?
Divides rows into N approximately equal groups (buckets).
```sql
SELECT name, salary, NTILE(4) OVER (ORDER BY salary DESC) AS quartile FROM employees;
```

### Q80: What is a CTE (Common Table Expression)?
A named temporary result set that exists only for the duration of a query.
```sql
WITH dept_stats AS (SELECT department_id, AVG(salary) AS avg_salary FROM employees GROUP BY department_id)
SELECT e.name, e.salary FROM employees e JOIN dept_stats d ON e.department_id = d.department_id WHERE e.salary > d.avg_salary;
```

### Q81: What is a Recursive CTE?
A CTE that references itself, useful for hierarchical/tree data.
```sql
WITH RECURSIVE org_chart AS (
  SELECT id, name, manager_id, 1 AS level FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.name, e.manager_id, oc.level + 1 FROM employees e JOIN org_chart oc ON e.manager_id = oc.id
) SELECT * FROM org_chart;
```

### Q82: What is a NOT NULL constraint?
Ensures a column cannot store NULL values.

### Q83: What is a UNIQUE constraint?
Ensures all values in a column (or column set) are distinct.

### Q84: What is a CHECK constraint?
Ensures values meet a condition.
```sql
CREATE TABLE products (price DECIMAL(10,2) CHECK (price >= 0));
```

### Q85: What is a DEFAULT constraint?
Provides a default value when none is specified.
```sql
CREATE TABLE users (created_at TIMESTAMP DEFAULT NOW(), is_active BOOLEAN DEFAULT TRUE);
```

### Q86: What is a Partial Index?
Indexes only a subset of rows, reducing index size.
```sql
CREATE INDEX idx_active_users ON users(email) WHERE is_active = TRUE;
```

### Q87: What is a Covering Index?
An index that contains all columns needed for a query, allowing index-only scans.
```sql
CREATE INDEX idx_covering ON users(email, name, age);
```

### Q88: What is an Index-Only Scan?
When the query can be answered entirely from the index without touching the table heap.

### Q89: What is Full-Text Search in PostgreSQL?
PostgreSQL's native text search using tsvector and tsquery.
```sql
CREATE INDEX idx_articles_search ON articles USING GIN(to_tsvector('english', title || ' ' || body));
SELECT title FROM articles WHERE to_tsvector('english', title || ' ' || body) @@ to_tsquery('english', 'database & performance');
```

### Q90: What is JSON/JSONB in PostgreSQL?
PostgreSQL supports JSON (text) and JSONB (binary, indexed) data types.
```sql
CREATE TABLE events (id BIGSERIAL PRIMARY KEY, payload JSONB);
CREATE INDEX idx_events_payload ON events USING GIN(payload);
SELECT * FROM events WHERE payload @> '{"type": "click"}';
```

### Q91: PostgreSQL vs MySQL — when to use which?
**Choose PostgreSQL for:** Complex queries, analytics, JSON, GIS, data integrity, advanced features.
**Choose MySQL for:** Simplicity, WordPress, legacy apps, replication topology.

### Q92: ORM vs Raw SQL — tradeoffs?
| ORM | Raw SQL |
|-----|---------|
| Faster development | Full control |
| Less error-prone | Optimizable per query |
| Portability | Best performance |
| Can encourage N+1 | Requires deep SQL knowledge |

### Q93: What are Database Migrations?
Version-controlled scripts that evolve the database schema over time. Tools: Alembic, Flyway, Prisma Migrate.

### Q94: Schema Design Best Practices
1. Use proper data types
2. Normalize until you need denormalization
3. Primary keys: BIGSERIAL or UUID
4. Index foreign keys
5. Use NOT NULL by default
6. Avoid SELECT *
7. Use consistent naming
8. Soft deletes with deleted_at
9. Created/updated timestamps on every table
10. Constraints over application logic

### Q95: What is a database transaction log / WAL?
A write-ahead log that records every change before applying it to data files. Used for crash recovery and replication.

### Q96: What is MVCC?
Multi-Version Concurrency Control. Each transaction sees a snapshot of data from its start time. Writers don't block readers. PostgreSQL implements this by keeping multiple row versions.

### Q97: What is a table scan vs index scan?
- **Seq Scan**: Reads every row sequentially (bad for large tables)
- **Index Scan**: Uses index structure to find rows (faster for selective queries)

### Q98: What is cardinality?
Number of distinct values in a column. High cardinality (email, id) → good for indexing. Low cardinality (gender, status) → bad for indexing.

### Q99: What is selectivity?
Fraction of rows selected by a query predicate. High selectivity (few rows) → index is useful.

### Q100: What is a composite index column order rule?
Put the most selective column first (highest cardinality). PostgreSQL can still use the index for the second column alone, but less efficiently.

### Q101: What is auto-increment / serial?
```sql
-- PostgreSQL: CREATE TABLE users (id BIGSERIAL PRIMARY KEY);
-- MySQL: CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY);
```

### Q102: What is a sequence?
A database object that generates unique numeric values.
```sql
CREATE SEQUENCE order_seq START 1000;
SELECT nextval('order_seq');
```

### Q103: What is UUID vs Serial?
| UUID | BIGSERIAL |
|------|-----------|
| 128-bit, globally unique | 64-bit, local to DB |
| Good for distributed systems | Good for single-node |

### Q104: What is ON DELETE CASCADE?
When a parent row is deleted, all referencing child rows are automatically deleted.
```sql
CREATE TABLE orders (user_id BIGINT REFERENCES users(id) ON DELETE CASCADE);
```

### Q105: What is ON DELETE SET NULL?
When a parent row is deleted, the foreign key column in child rows is set to NULL.

### Q106: What is ON DELETE RESTRICT?
Prevents deletion of a parent row if any child rows reference it.

### Q107: What is a natural key vs surrogate key?
- **Natural key**: Meaningful business value (SSN, email)
- **Surrogate key**: Artificial, meaningless (auto-increment id)
**Recommendation:** Use surrogate keys as PRIMARY KEY, UNIQUE constraints on natural keys.

### Q108: What is an ER diagram?
Entity-Relationship diagram — visual representation of entities, attributes, and relationships.

### Q109: What is cardinality in relationships?
- **1:1**: User ↔ UserProfile
- **1:N**: User → Orders
- **M:N**: Student ↔ Course (requires junction table)

### Q110: What is a junction table?
Bridges a many-to-many relationship.
```sql
CREATE TABLE enrollments (student_id BIGINT REFERENCES students(id), course_id BIGINT REFERENCES courses(id), PRIMARY KEY (student_id, course_id));
```

### Q111: What is data integrity?
Accuracy and consistency of data. Enforced by constraints and triggers.

### Q112: What is referential integrity?
Ensures foreign key values point to existing primary keys.

### Q113: What is a schema in a database?
A namespace containing database objects. PostgreSQL uses `public` by default.
```sql
CREATE SCHEMA sales; CREATE TABLE sales.orders (id INT);
```

### Q114: What is a correlated subquery?
A subquery that references columns from the outer query. Evaluated row-by-row.
```sql
SELECT e.name FROM employees e WHERE salary > (SELECT AVG(salary) FROM employees WHERE department_id = e.department_id);
```

### Q115: What is EXISTS vs IN?
- `EXISTS`: Checks if any rows exist (short-circuits, good for large subqueries)
- `IN`: Checks if value is in a list (materializes the subquery result)

### Q116: What is DISTINCT?
Removes duplicate rows from the result.
```sql
SELECT DISTINCT department_id FROM employees;
```

### Q117: What is DISTINCT ON (PostgreSQL)?
Returns the first row per group based on ORDER BY.
```sql
SELECT DISTINCT ON (department_id) department_id, name, salary FROM employees ORDER BY department_id, salary DESC;
```

### Q118: What is COALESCE?
Returns the first non-NULL value.
```sql
SELECT COALESCE(phone, email, 'No contact') AS contact FROM users;
```

### Q119: What is NULLIF?
Returns NULL if two expressions are equal, else returns the first.

### Q120: What is CAST?
Converts a value from one type to another.
```sql
SELECT CAST('100' AS INTEGER); SELECT '100'::INTEGER;
```

### Q121: CHAR, VARCHAR, TEXT differences?
| Type | Storage | Max | Use |
|------|---------|-----|-----|
| CHAR(n) | Fixed | 255 | Fixed codes |
| VARCHAR(n) | Variable + length prefix | 65,535 | Limited strings |
| TEXT | Variable | Unlimited | Large strings |

### Q122: What is TIMESTAMPTZ?
Stores UTC internally and converts to session timezone on retrieval.
```sql
CREATE TABLE events (occurred_at TIMESTAMPTZ DEFAULT NOW());
```

### Q123: What is TRUNCATE vs DELETE?
- `DELETE`: DML, row-by-row, triggers fire, can be rolled back, slower
- `TRUNCATE`: DDL, deallocates pages, no triggers, faster, cannot be rolled back

### Q124: What is UPSERT (INSERT ... ON CONFLICT)?
```sql
INSERT INTO users (id, name) VALUES (1, 'Alice') ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
```

### Q125: What is RETURNING (PostgreSQL)?
Returns values from modified rows.
```sql
INSERT INTO orders (user_id, amount) VALUES (1, 100) RETURNING id, created_at;
```

### Q126: What is LATERAL JOIN (PostgreSQL)?
Allows a subquery in FROM clause to reference columns from preceding FROM items.
```sql
SELECT u.name, o.amount FROM users u LEFT JOIN LATERAL (SELECT amount FROM orders WHERE user_id = u.id ORDER BY created_at DESC LIMIT 1) o ON TRUE;
```

### Q127: What is FILTER (PostgreSQL)?
Conditional aggregation within aggregate functions.
```sql
SELECT department_id, COUNT(*) FILTER (WHERE salary > 80000) AS high_earners FROM employees GROUP BY department_id;
```

### Q128: What is ROLLUP, CUBE, GROUPING SETS?
Extensions of GROUP BY for multiple grouping levels in one query.
```sql
SELECT COALESCE(department, 'All'), COUNT(*) FROM employees GROUP BY ROLLUP(department, status);
```

### Q129: What is a generated column?
A column whose value is computed automatically.
```sql
CREATE TABLE products (price DECIMAL(10,2), quantity INT, total_value GENERATED ALWAYS AS (price * quantity) STORED);
```

### Q130: What is WHERE vs ON in JOINs?
- `ON` defines the join condition (rows matched between tables)
- `WHERE` filters the result after the join

### Q131-Q150: Additional SQL fundamentals
```sql
-- Q131: Find duplicate emails
SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;

-- Q132: Nth highest salary
SELECT DISTINCT salary FROM employees ORDER BY salary DESC OFFSET 1 LIMIT 1;

-- Q133: Employees earning more than manager
SELECT e.name FROM employees e JOIN employees m ON e.manager_id = m.id WHERE e.salary > m.salary;

-- Q134: Department max salary
SELECT DISTINCT ON (department_id) department_id, name, salary FROM employees ORDER BY department_id, salary DESC;

-- Q135: Running total
SELECT order_date, amount, SUM(amount) OVER (ORDER BY order_date) AS running_total FROM orders;

-- Q136: Moving average
SELECT date, revenue, AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma_7d FROM daily_revenue;

-- Q137: Median
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median FROM employees;

-- Q138: Consecutive streaks
WITH numbered AS (SELECT user_id, login_date, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn FROM user_logins)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_length
FROM (SELECT user_id, login_date, login_date - INTERVAL '1 day' * rn AS grp FROM numbered) sub
GROUP BY user_id, grp HAVING COUNT(*) >= 3;

-- Q139: Overlapping date ranges
SELECT a.id, b.id FROM bookings a JOIN bookings b ON a.id < b.id AND a.start_date < b.end_date AND a.end_date > b.start_date;

-- Q140: Sessionization (30-min timeout)
WITH numbered AS (SELECT user_id, action_time, LAG(action_time) OVER (PARTITION BY user_id ORDER BY action_time) AS prev_time FROM user_actions)
SELECT user_id, SUM(CASE WHEN prev_time IS NULL OR action_time - prev_time > INTERVAL '30 min' THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY action_time) AS session_id, action_time FROM numbered;

-- Q141: Compare two tables
(SELECT * FROM table_a EXCEPT SELECT * FROM table_b) UNION ALL (SELECT * FROM table_b EXCEPT SELECT * FROM table_a);

-- Q142: PIVOT using FILTER
SELECT department_id, COUNT(*) FILTER (WHERE status = 'active') AS active, COUNT(*) FILTER (WHERE status = 'inactive') AS inactive FROM employees GROUP BY department_id;

-- Q143: UNPIVOT using LATERAL
SELECT id, quarter, revenue FROM quarterly_revenue CROSS JOIN LATERAL (VALUES ('q1', q1), ('q2', q2)) AS q(quarter, revenue);

-- Q144: Recursive org chart
WITH RECURSIVE org AS (SELECT id, name, manager_id, 1 AS level FROM employees WHERE manager_id IS NULL UNION ALL SELECT e.id, e.name, e.manager_id, org.level + 1 FROM employees e JOIN org ON e.manager_id = org.id) SELECT * FROM org;

-- Q145: Gap detection
SELECT id, LAG(id) OVER (ORDER BY id) AS prev_id, id - LAG(id) OVER (ORDER BY id) - 1 AS gap FROM sequence_table WHERE id - LAG(id) OVER (ORDER BY id) > 1;

-- Q146: Most recent order per user
SELECT DISTINCT ON (user_id) * FROM orders ORDER BY user_id, created_at DESC;

-- Q147: Month-over-month change
SELECT DATE_TRUNC('month', order_date) AS month, SUM(amount) AS revenue, LAG(SUM(amount)) OVER (ORDER BY DATE_TRUNC('month', order_date)) AS prev, (SUM(amount) - LAG(SUM(amount)) OVER (ORDER BY DATE_TRUNC('month', order_date))) / NULLIF(LAG(SUM(amount)) OVER (ORDER BY DATE_TRUNC('month', order_date)), 0) * 100 AS mom_pct FROM orders GROUP BY 1;

-- Q148: Cumulative count by month
SELECT DATE_TRUNC('month', created_at) AS month, COUNT(*) AS new_users, SUM(COUNT(*)) OVER (ORDER BY DATE_TRUNC('month', created_at)) AS cumulative FROM users GROUP BY month;

-- Q149: Find users who bought all products in a category
SELECT user_id FROM orders o JOIN order_items oi ON o.id = oi.order_id JOIN products p ON oi.product_id = p.id WHERE p.category_id = 1 GROUP BY user_id HAVING COUNT(DISTINCT p.id) = (SELECT COUNT(*) FROM products WHERE category_id = 1);

-- Q150: JSON extraction in PostgreSQL
SELECT id, metadata->>'city' AS city FROM users WHERE metadata @> '{"country": "US"}';
```

---

# PostgreSQL Deep (Q151–Q220)

### Q151: Describe PostgreSQL's architecture (processes).
PostgreSQL uses a **process-per-connection** model (not threaded). Key processes: Postmaster (main daemon), Backend (per connection), Background writer, WAL writer, Autovacuum launcher/workers, Checkpointer, Stats collector, Logger, Archiver.

### Q152: What is PostgreSQL's memory architecture?
**Shared Memory**: Shared Buffers (data cache), WAL Buffers, Lock Space.
**Per-Backend**: work_mem (sorting), maintenance_work_mem (VACUUM, CREATE INDEX), temp_buffers.

### Q153: What is shared_buffers?
Amount of memory for caching data. Typically 15–25% of RAM.
```ini
shared_buffers = 4GB  # on a 16GB machine
```

### Q154: What is work_mem?
Memory for sorting operations, hash tables, bitmap operations. Per operation per connection.
```ini
work_mem = 64MB
```

### Q155: What is effective_cache_size?
Estimate of OS + PostgreSQL disk cache available. Tells planner about cache size for index scan cost estimation.
```ini
effective_cache_size = 12GB
```

### Q156: What is maintenance_work_mem?
Memory for VACUUM, CREATE INDEX, ALTER TABLE. Can be set higher than work_mem.
```ini
maintenance_work_mem = 1GB
```

### Q157: What is VACUUM in PostgreSQL?
VACUUM reclaims storage occupied by dead tuples.
```sql
VACUUM table_name;        -- reclaims space, does NOT reduce table size
VACUUM FULL table_name;   -- locks table, rebuilds it, reduces size
```

### Q158: What is Autovacuum?
PostgreSQL automatically vacuums tables based on thresholds. Enabled by default.
```ini
autovacuum = on
autovacuum_vacuum_threshold = 50
autovacuum_vacuum_scale_factor = 0.2
```

### Q159: Why is Autovacuum important?
- Prevents transaction ID wraparound (disaster)
- Keeps statistics up-to-date
- Prevents table bloat

### Q160: What is a dead tuple?
In PostgreSQL's MVCC, UPDATE creates a new row version; DELETE marks a row as deleted. The old version is a "dead tuple." Must be cleaned by VACUUM.

### Q161: What is PostgreSQL Streaming Replication?
Primary sends WAL to standby as generated. Standby applies WAL in real-time.
```ini
# Primary: wal_level = replica, max_wal_senders = 3
# Standby: hot_standby = on, creates standby.signal
```

### Q162: Synchronous vs Asynchronous replication?
- **Async**: Primary commits immediately; standby may lag. Default. Fast, potential data loss.
- **Sync**: Primary waits for standby to confirm. Zero data loss, slower.

### Q163: What is Logical Replication?
Publishes changes as logical rows (INSERT, UPDATE, DELETE). Can replicate selected tables, between versions.
```sql
CREATE PUBLICATION my_pub FOR TABLE users, orders;
CREATE SUBSCRIPTION my_sub CONNECTION 'host=primary dbname=db' PUBLICATION my_pub;
```

### Q164: What is PostgreSQL Partitioning?
Dividing a large table into smaller physical pieces (partitions) while treating as one logical table.
**Types:** Range, List, Hash.
```sql
CREATE TABLE orders (id BIGSERIAL, order_date DATE) PARTITION BY RANGE (order_date);
CREATE TABLE orders_2024 PARTITION OF orders FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

### Q165: What is Range Partitioning?
Partitions based on a range of values.

### Q166: What is List Partitioning?
Partitions based on discrete values.
```sql
CREATE TABLE customers (id INT, region TEXT) PARTITION BY LIST (region);
CREATE TABLE customers_us PARTITION OF customers FOR VALUES IN ('US', 'CA');
```

### Q167: What is Hash Partitioning?
Partitions based on hash of a key. Good for even distribution.
```sql
CREATE TABLE events (id BIGSERIAL) PARTITION BY HASH (id);
CREATE TABLE events_0 PARTITION OF events FOR VALUES WITH (MODULUS 4, REMAINDER 0);
```

### Q168: What is PostgreSQL GiST index?
Generalized Search Tree. Supports geometric data, full-text search, range types.
```sql
CREATE INDEX idx_locations ON places USING GIST (location);
```

### Q169: What is PostgreSQL GIN index?
Generalized Inverted Index. Good for arrays, JSONB, full-text search.
```sql
CREATE INDEX idx_tags ON posts USING GIN (tags);
CREATE INDEX idx_json ON events USING GIN (payload);
```

### Q170: What is PostgreSQL BRIN index?
Block Range INdex. For large tables where data is naturally ordered (time series). Very small index size.
```sql
CREATE INDEX idx_brin_created ON logs USING BRIN (created_at);
```

### Q171: How does EXPLAIN ANALYZE work?
Executes the query and shows the actual execution plan with timing.
```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = 42;
```

### Q172: What is a sequential scan? When is it okay?
Reading entire table sequentially. OK when: table is small, query returns > 10–30% of rows, no suitable index.

### Q173: What is parallel query in PostgreSQL?
PostgreSQL can use multiple CPUs to answer a query.
```ini
max_parallel_workers_per_gather = 2
```

### Q174: What is a Foreign Data Wrapper (FDW)?
Allows querying external systems as local tables.
```sql
CREATE EXTENSION postgres_fdw;
CREATE FOREIGN TABLE remote_orders (id INT) SERVER other_server;
```

### Q175: What is an UNLOGGED table?
Does not write to WAL. Faster writes, lost on crash.
```sql
CREATE UNLOGGED TABLE temp_events (id BIGSERIAL, data TEXT);
```

### Q176: What is pg_stat_statements?
Tracks query execution statistics.
```sql
CREATE EXTENSION pg_stat_statements;
SELECT query, calls, total_time / calls AS avg_time FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;
```

### Q177: What is pg_stat_activity?
Shows current backend processes and their queries.
```sql
SELECT pid, state, query, query_start FROM pg_stat_activity WHERE state != 'idle' ORDER BY query_start;
```

### Q178: How to kill a query in PostgreSQL?
```sql
SELECT pg_cancel_backend(pid);   -- cancel query
SELECT pg_terminate_backend(pid); -- terminate connection
```

### Q179: What is a WAL (Write-Ahead Log)?
Every change is written to WAL before data files. Ensures durability and enables recovery/replication.

### Q180: What is a checkpoint?
The point at which all dirty pages in shared buffers are written to disk.
```ini
checkpoint_timeout = 5min
max_wal_size = 1GB
```

### Q181: What is PITR (Point-In-Time Recovery)?
Recovering to a specific time using WAL archives + base backup.
```ini
recovery_target_time = '2024-06-20 14:30:00'
```

### Q182: What is pg_dump?
Logical backup tool.
```bash
pg_dump dbname > backup.sql
pg_dump -Fc dbname > backup.dump
```

### Q183: What is pg_restore?
Restores from pg_dump custom format.
```bash
pg_restore -d dbname backup.dump
pg_restore -d dbname -t users backup.dump
```

### Q184: What is pg_basebackup?
Creates a physical base backup for replication.
```bash
pg_basebackup -h primary -D /data/standby -P -R
```

### Q185: What is pgbouncer?
A lightweight connection pooler for PostgreSQL.
```ini
pool_mode = transaction
default_pool_size = 20
```

### Q186: What is PostgreSQL's connection limit?
Configured via `max_connections`. Default is 100. Each connection requires ~5-10 MB.

### Q187: What is the pg_hba.conf file?
Host-Based Authentication — controls which hosts/users/databases can connect.

### Q188: What are PostgreSQL roles?
Access control mechanism. Roles can be login-enabled, have passwords, and be grouped.
```sql
CREATE ROLE app_user WITH LOGIN PASSWORD 'secure_pass';
CREATE ROLE readonly; GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
```

### Q189: What is GRANT vs REVOKE?
```sql
GRANT SELECT, INSERT ON orders TO app_user;
REVOKE DELETE ON orders FROM app_user;
```

### Q190: What is row-level security (RLS)?
Restricts which rows users can see based on a policy.
```sql
ALTER TABLE accounts ENABLE ROW LEVEL SECURITY;
CREATE POLICY user_policy ON accounts USING (owner = current_user);
```

### Q191: What is a PostgreSQL extension?
Packages that add functionality.
```sql
CREATE EXTENSION postgis;    -- GIS support
CREATE EXTENSION pgvector;   -- vector similarity search
CREATE EXTENSION pgcrypto;   -- cryptographic functions
CREATE EXTENSION "uuid-ossp"; -- UUID generation
CREATE EXTENSION hstore;     -- key-value store
CREATE EXTENSION pg_trgm;    -- trigram text search
```

### Q192: What is PostGIS?
Spatial database extender for PostgreSQL.
```sql
CREATE EXTENSION postgis;
CREATE TABLE places (id BIGSERIAL, name TEXT, location GEOGRAPHY(Point, 4326));
SELECT name FROM places WHERE ST_DWithin(location, ST_MakePoint(-73.9, 40.7)::geography, 10000);
```

### Q193: What is pgvector?
Extension for vector similarity search (embeddings for LLMs/ML).
```sql
CREATE EXTENSION vector;
CREATE TABLE items (id BIGSERIAL, embedding VECTOR(384));
CREATE INDEX ON items USING ivfflat (embedding vector_cosine_ops);
SELECT id FROM items ORDER BY embedding <=> '[0.1, 0.2, ...]' LIMIT 10;
```

### Q194: What is hstore?
Key-value store within PostgreSQL.
```sql
CREATE EXTENSION hstore;
CREATE TABLE products (id BIGSERIAL, attributes hstore);
INSERT INTO products (attributes) VALUES ('color => red, size => M');
SELECT attributes -> 'color' FROM products;
```

### Q195: What is pg_trgm?
Trigram-based text search (fuzzy matching, LIKE optimization).
```sql
CREATE EXTENSION pg_trgm;
CREATE INDEX ON users USING GIN (name gin_trgm_ops);
SELECT * FROM users WHERE name ILIKE '%alice%';
SELECT * FROM users WHERE similarity(name, 'alic') > 0.3;
```

### Q196: What is pgcrypto?
Cryptographic functions.
```sql
CREATE EXTENSION pgcrypto;
SELECT crypt('password123', gen_salt('bf'));  -- bcrypt hash
SELECT gen_random_uuid();
```

### Q197: Can PostgreSQL do an UPDATE with JOIN?
```sql
UPDATE products p SET price = price * 1.1 FROM categories c WHERE p.category_id = c.id AND c.name = 'Electronics';
```

### Q198: How to find table size in PostgreSQL?
```sql
SELECT relname, pg_size_pretty(pg_total_relation_size(relid)) FROM pg_catalog.pg_statio_user_tables ORDER BY pg_total_relation_size(relid) DESC;
```

### Q199: How to find database size?
```sql
SELECT pg_size_pretty(pg_database_size('mydb'));
```

### Q200: What is TOAST in PostgreSQL?
Oversized-Attribute Storage Technique. Large values (> ~2KB) are compressed and stored in a separate TOAST table.

### Q201: What is Table Bloat?
When a table contains many dead tuples without sufficient VACUUM. Causes slower queries.
```sql
SELECT schemaname, tablename, n_dead_tup, n_live_tup, round(n_dead_tup::numeric / NULLIF(n_live_tup, 0), 2) AS dead_ratio FROM pg_stat_user_tables WHERE n_dead_tup > 1000 ORDER BY dead_ratio DESC;
```

### Q202: What is a HOT (Heap-Only Tuple) Update?
When UPDATE doesn't change indexed columns, the new tuple stays on the same page. Reduces index maintenance.

### Q203: VACUUM vs ANALYZE?
- `VACUUM`: Removes dead tuples
- `ANALYZE`: Updates table statistics

### Q204: What is autovacuum_vacuum_cost_delay?
Controls how aggressive autovacuum is. Prevents consuming too many I/O resources.

### Q205: What is an EXCLUDE constraint?
Ensures no two rows have overlapping values (for range types).
```sql
CREATE TABLE reservations (room_id INT, during TSRANGE, EXCLUDE USING GIST (room_id WITH =, during WITH &&));
```

### Q206: What are PostgreSQL range types?
int4range, int8range, numrange, tsrange, tstzrange, daterange.
```sql
SELECT * FROM events WHERE duration @> '2024-01-01 11:00'::timestamp;
```

### Q207: What is an array in PostgreSQL?
```sql
CREATE TABLE projects (id INT, tags TEXT[]);
INSERT INTO projects VALUES (1, ARRAY['python', 'postgres']);
SELECT * FROM projects WHERE 'postgres' = ANY(tags);
SELECT unnest(tags) FROM projects;
```

### Q208: How to create a custom data type?
```sql
CREATE TYPE mood AS ENUM ('happy', 'sad', 'neutral');
CREATE TYPE address AS (street TEXT, city TEXT, zip TEXT);
```

### Q209: What is a DOMAIN in PostgreSQL?
Reusable constraint wrapper.
```sql
CREATE DOMAIN positive_int AS INT CHECK (VALUE > 0);
```

### Q210: What is CIDR/INET types?
Types for IP addresses with subnet support.
```sql
SELECT * FROM servers WHERE ip << '192.168.0.0/16';
```

### Q211: What is ON CONFLICT DO NOTHING?
Skip insertion on conflict without error.
```sql
INSERT INTO users (id, name) VALUES (1, 'Alice') ON CONFLICT (id) DO NOTHING;
```

### Q212: What is INHERITS in PostgreSQL?
Table inheritance (rarely used — use partitioning instead).

### Q213: What is a custom scan / FDW for external data?
See Q174.

### Q214: What is the difference between VACUUM FREEZE and regular VACUUM?
FREEZE marks tuples as frozen to prevent transaction ID wraparound.

### Q215: What are PostgreSQL replication slots?
Ensure the primary retains WAL until all connected standbys have received it. Prevents WAL cleanup before standby processes it.

### Q216: What is pg_rewind?
Used to re-sync a former primary after failover, without full base backup.

### Q217: What is pg_stat_replication?
Shows replication status.
```sql
SELECT application_name, state, sync_state, write_lag FROM pg_stat_replication;
```

### Q218: What is max_wal_size and min_wal_size?
Control WAL file retention. Checkpoints trigger when WAL reaches max_wal_size.

### Q219: How does PostgreSQL handle full-text search ranking?
```sql
SELECT title, ts_rank(search_vector, query) AS rank FROM articles, to_tsquery('english', 'database') AS query WHERE search_vector @@ query ORDER BY rank DESC;
```

### Q220: What is pg_stat_user_tables?
Shows per-table statistics (scans, tuples fetched, dead tuples, last vacuum/analyze).
```sql
SELECT relname, seq_scan, idx_scan, n_live_tup, n_dead_tup, last_vacuum, last_analyze FROM pg_stat_user_tables;
```

---

# NoSQL & MongoDB (Q221–Q300)

### Q221: What is NoSQL?
Non-relational databases designed for flexible schemas, horizontal scaling, and specific data models (document, key-value, column-family, graph).

### Q222: When to use NoSQL vs SQL?
| Use NoSQL | Use SQL |
|-----------|--------|
| Flexible/unpredictable schema | Well-defined schema |
| Horizontal scaling needed | Complex JOINs and aggregations |
| High-velocity writes | ACID transactions required |
| Simple access patterns | Complex queries/reports |

### Q223: What is the CAP theorem?
A distributed system can have at most 2 of 3 guarantees: **Consistency**, **Availability**, **Partition tolerance**. Since P is necessary in distributed systems, you choose CP or AP.

### Q224: Explain CAP with examples.
- **CP (Consistency + Partition)**: MongoDB (default), HBase
- **AP (Availability + Partition)**: Cassandra, CouchDB, DynamoDB
- **CA**: Only single-node (single PostgreSQL)

### Q225: What are consistency models?
- **Strong consistency**: Latest write always read
- **Eventual consistency**: Converges over time
- **Causal consistency**: Causally related events seen in order
- **Read-your-writes**: Client sees its own writes

### Q226: What is MongoDB?
Document-oriented NoSQL database. Stores data as BSON (binary JSON) documents in collections.

### Q227: What is the MongoDB document model?
```json
{"_id": ObjectId("..."), "name": "Alice", "email": "alice@x.com", "addresses": [{"city": "NYC"}]}
```

### Q228: MongoDB vs PostgreSQL?
| MongoDB | PostgreSQL |
|---------|-----------|
| Flexible schema | Rigid schema |
| Nested documents (no JOINs) | Normalized + JOINs |
| Auto-sharding | Manual partitioning |
| Eventual consistency (default) | Strong consistency |
| ACID limited (v4.0+) | Full ACID |

### Q229: What is a MongoDB Index?
```javascript
db.users.createIndex({ email: 1 });  // 1 = ascending
db.users.createIndex({ email: 1 }, { unique: true });
```

### Q230: What is a Compound Index in MongoDB?
```javascript
db.orders.createIndex({ user_id: 1, created_at: -1 });
// ESR Rule: Equality, Sort, Range
```

### Q231: What is a Multikey Index?
Index on an array field — creates index entry for each array element.

### Q232: What is a Text Index in MongoDB?
```javascript
db.articles.createIndex({ title: "text", body: "text" });
db.articles.find({ $text: { $search: "database performance" } });
```

### Q233: What is a Geospatial Index?
```javascript
db.places.createIndex({ location: "2dsphere" });
db.places.find({ location: { $near: { $geometry: { type: "Point", coordinates: [-73.9, 40.7] }, $maxDistance: 1000 } } });
```

### Q234: What is the MongoDB Aggregation Pipeline?
```javascript
db.orders.aggregate([
  { $match: { status: "completed" } },
  { $group: { _id: "$user_id", total: { $sum: "$amount" } } },
  { $sort: { total: -1 } },
  { $limit: 10 },
  { $lookup: { from: "users", localField: "_id", foreignField: "_id", as: "user" } },
  { $unwind: "$user" },
  { $project: { name: "$user.name", total: 1 } }
]);
```

### Q235: What is $match in Aggregation?
Filters documents (like WHERE).

### Q236: What is $group in Aggregation?
Groups documents and computes aggregates.
```javascript
{ $group: { _id: "$category", totalRevenue: { $sum: "$price" }, avgPrice: { $avg: "$price" }, count: { $sum: 1 } } }
```

### Q237: What is $sort, $limit in Aggregation?
```javascript
{ $sort: { total: -1 } }, { $limit: 10 }
```

### Q238: What is $project in Aggregation?
Shapes documents.
```javascript
{ $project: { name: 1, fullAddress: { $concat: ["$street", ", ", "$city"] }, _id: 0 } }
```

### Q239: What is $lookup in Aggregation?
LEFT JOIN equivalent across collections.
```javascript
{ $lookup: { from: "reviews", localField: "_id", foreignField: "product_id", as: "reviews" } }
```

### Q240: What is $unwind in Aggregation?
Deconstructs array into multiple documents.

### Q241: What is a MongoDB Replica Set?
Group of mongod processes maintaining same data. Primary (accepts writes), Secondaries (replicate), Arbiter (votes).

### Q242: How does MongoDB replication work?
- Primary records writes in **oplog**
- Secondaries copy and apply oplog
- If primary fails, election picks new primary

### Q243: What is MongoDB Sharding?
Distributes data across servers. Components: mongos (router), config servers (metadata), shards (data).

### Q244: What is a Shard Key?
Field determining data distribution across shards.
```javascript
sh.shardCollection("mydb.orders", { user_id: "hashed" });
```

### Q245: Good Shard Key characteristics?
High cardinality, even distribution, supports common query patterns.

### Q246: What is chunk splitting?
When a shard chunk grows beyond chunk size (default 64MB), balancer splits and migrates chunks.

### Q247: Does MongoDB support ACID?
Since MongoDB 4.0, multi-document ACID transactions are supported (slower, used selectively).
```javascript
const session = client.startSession();
session.startTransaction();
try { await collection1.insertOne({...}, {session}); await session.commitTransaction(); }
catch (e) { await session.abortTransaction(); }
finally { session.endSession(); }
```

### Q248: MongoDB schema design: embedding vs referencing?
| Embed (denormalize) | Reference (normalize) |
|---------------------|----------------------|
| One-to-few | One-to-many |
| Data read together | Data independent |
| Rarely changes | Grows unbounded |

### Q249: What is $set in MongoDB?
```javascript
db.users.updateOne({ _id: 1 }, { $set: { name: "Bob" } });
```

### Q250: What is $unset?
```javascript
db.users.updateOne({ _id: 1 }, { $unset: { temp_field: "" } });
```

### Q251: What is $push?
Appends to array.
```javascript
db.posts.updateOne({ _id: 1 }, { $push: { comments: { user: "Alice", text: "Great!" } } });
```

### Q252: What is $inc?
Increments numeric field.
```javascript
db.products.updateOne({ _id: 1 }, { $inc: { stock: -1 } });
```

### Q253: What is $pull?
Removes matching elements from array.
```javascript
db.posts.updateOne({ _id: 1 }, { $pull: { comments: { user: "Alice" } } });
```

### Q254: What is $addToSet?
Adds to array if not present.
```javascript
db.users.updateOne({ _id: 1 }, { $addToSet: { roles: "admin" } });
```

### Q255: What is a TTL index?
Auto-removes documents after specified time.
```javascript
db.sessions.createIndex({ createdAt: 1 }, { expireAfterSeconds: 3600 });
```

### Q256: What is a Unique Index in MongoDB?
```javascript
db.users.createIndex({ email: 1 }, { unique: true });
```

### Q257: What is a Sparse Index?
Only indexes documents containing the indexed field.
```javascript
db.users.createIndex({ optional_field: 1 }, { sparse: true });
```

### Q258: What is a Covered Query in MongoDB?
All fields in query are in the index — no document fetch needed.

### Q259: What is explain() in MongoDB?
```javascript
db.users.find({ email: "alice@x.com" }).explain("executionStats");
// Shows IXSCAN vs COLLSCAN
```

### Q260: What is MongoDB Atlas?
MongoDB's managed cloud service. Automated backups, monitoring, auto-scaling, global clusters.

### Q261: What are Change Streams?
Real-time data changes feed.
```javascript
const changeStream = db.orders.watch([{ $match: { "fullDocument.status": "completed" } }]);
changeStream.on("change", (change) => console.log(change.fullDocument));
```

### Q262: When to use MongoDB vs PostgreSQL?
**MongoDB**: Rapid prototyping, nested data, horizontal scaling, high write throughput.
**PostgreSQL**: Complex queries, ACID, stable schema, advanced indexing, spatial data.

### Q263: What is BSON?
Binary JSON with additional types: ObjectId, Date, Binary, Decimal128.

### Q264: What is ObjectId?
12-byte identifier: 4 bytes timestamp + 5 bytes random + 3 bytes counter.

### Q265: MongoDB vs Cassandra?
| MongoDB | Cassandra |
|---------|-----------|
| Document model | Wide-column |
| Primary-secondary | Peer-to-peer |
| Strong consistency (default) | Eventual consistency (tunable) |
| Rich query language | CQL (limited) |

### Q266: What is Redis?
In-memory key-value store with optional persistence. Used for caching, sessions, pub/sub.
```
SET user:1:name "Alice"
GET user:1:name
ZADD leaderboard 1000 "player1"
```

### Q267: What is Cassandra?
Wide-column NoSQL for high write throughput and availability (AP). Uses CQL.
```cql
CREATE TABLE users (id UUID PRIMARY KEY, name TEXT, email TEXT);
INSERT INTO users (id, name, email) VALUES (uuid(), 'Alice', 'alice@x.com');
```

### Q268: What is a Wide-Column Store?
Data stored in rows with flexible columns. Each row can have different columns. Examples: Cassandra, HBase.

### Q269: What is HBase?
Wide-column store on HDFS. Good for large-scale batch processing.

### Q270: What is Neo4j?
Graph database. Data as nodes and relationships.
```cypher
CREATE (alice:User {name: "Alice"})-[:FOLLOWS]->(bob:User {name: "Bob"});
MATCH (u:User {name: "Alice"})-[:FOLLOWS]->(friends) RETURN friends;
```

### Q271: What is a Key-Value Store?
Simplest NoSQL model. Examples: Redis, DynamoDB (key-value mode).

### Q272: What is a Document Store?
Stores data as documents (JSON, BSON). Examples: MongoDB, CouchDB, Firestore.

### Q273: What is Write Concern in MongoDB?
Controls write durability.
```javascript
{ w: "majority", j: true, wtimeout: 5000 }
```

### Q274: What is Read Concern in MongoDB?
Controls read consistency.
```javascript
db.orders.find().readConcern("majority")
```

### Q275: What is Read Preference in MongoDB?
Where to route reads in a replica set.
```javascript
db.orders.find().readPref("secondaryPreferred")
```

### Q276: What is $elemMatch in MongoDB?
Matches documents containing an array element matching all criteria.
```javascript
db.users.find({ scores: { $elemMatch: { subject: "math", score: { $gte: 90 } } } });
```

### Q277: What is $bucket in aggregation?
```javascript
{ $bucket: { groupBy: "$price", boundaries: [0, 50, 100], output: { count: { $sum: 1 } } } }
```

### Q278: What is $facet in aggregation?
```javascript
{ $facet: { byStatus: [{ $group: { _id: "$status", count: { $sum: 1 } } }], byYear: [{ $group: { _id: { $year: "$orderDate" }, total: { $sum: "$amount" } } }] } }
```

### Q279: What is $graphLookup?
Recursive lookup for graph/tree data.
```javascript
{ $graphLookup: { from: "employees", startWith: "$_id", connectFromField: "_id", connectToField: "manager_id", as: "reports", maxDepth: 5 } }
```

### Q280: How to do pagination in MongoDB?
```javascript
// Skip/limit (bad): db.users.find().skip(100).limit(10);
// Cursor (efficient): db.users.find({ _id: { $gt: lastSeenId } }).limit(10);
```

### Q281: What is MongoDB's oplog?
Capped collection recording all write operations. Secondaries tail the oplog to replicate.

### Q282: What is WiredTiger?
Default storage engine since MongoDB 3.2. Document-level locking, compression, snapshots.

### Q283: What is the $regex operator?
```javascript
db.users.find({ name: { $regex: /^ali/i } });
```

### Q284: What is $in and $all?
```javascript
db.orders.find({ status: { $in: ["pending", "processing"] } });
db.posts.find({ tags: { $all: ["mongodb", "database"] } });
```

### Q285: What is $expr in MongoDB?
Allows aggregation expressions in query language.
```javascript
db.orders.find({ $expr: { $gt: ["$amount", "$min_amount"] } });
```

### Q286: What is $cond in aggregation?
```javascript
{ $cond: { if: { $gte: ["$amount", 100] }, then: "High", else: "Regular" } }
```

### Q287: What is Firestore?
Google's document NoSQL database. Real-time updates, serverless, auto-scaling.

### Q288: What is the difference between NoSQL and NewSQL?
- **NoSQL**: Sacrifices ACID for scaling (MongoDB, Cassandra)
- **NewSQL**: Maintains SQL/ACID + horizontal scaling (CockroachDB, Spanner)

### Q289: What is CockroachDB?
Distributed SQL (NewSQL), PostgreSQL-compatible, horizontal scaling, strong consistency.

### Q290: What is $merge in aggregation?
Writes aggregation results to a collection.
```javascript
{ $merge: { into: "user_totals", whenMatched: "replace" } }
```

### Q291: MongoDB $bucketAuto?
Auto-determines bucket boundaries.
```javascript
{ $bucketAuto: { groupBy: "$price", buckets: 5 } }
```

### Q292: What is a MongoDB transaction?
See Q247.

### Q293: MongoDB $sample?
Random sampling.
```javascript
db.users.aggregate([{ $sample: { size: 100 } }]);
```

### Q294: MongoDB $replaceRoot?
Replaces document root.
```javascript
{ $replaceRoot: { newRoot: "$embedded" } }
```

### Q295: What is MongoDB $out?
Writes aggregation results to a collection (replaces collection entirely).

### Q296: How to create index on nested field?
```javascript
db.orders.createIndex({ "address.city": 1 });
```

### Q297: What is the difference between $push and $addToSet?
`$push` always adds (duplicates allowed). `$addToSet` only adds if not present.

### Q298: What is a MongoDB projection?
Second argument to find — specifies which fields to return.
```javascript
db.users.find({}, { name: 1, email: 1, _id: 0 });
```

### Q299: MongoDB index intersection?
MongoDB can use multiple indexes to satisfy a query (similar to PostgreSQL bitmap scans).

### Q300: MongoDB $convert?
Type conversion in aggregation.
```javascript
{ $convert: { input: "$age", to: "int", onError: 0, onNull: null } }
```

---

# Database Design & Architecture (Q301–Q350)

### Q301: What is an ER diagram?
Visual representation of entities (tables), attributes (columns), and relationships (foreign keys).

### Q302: Design schema for social media (users, posts, likes, comments).
```sql
CREATE TABLE users (id BIGSERIAL PRIMARY KEY, username VARCHAR(100) UNIQUE NOT NULL, email VARCHAR(255) UNIQUE NOT NULL, created_at TIMESTAMPTZ DEFAULT NOW());
CREATE TABLE posts (id BIGSERIAL PRIMARY KEY, user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE, content TEXT NOT NULL, created_at TIMESTAMPTZ DEFAULT NOW());
CREATE TABLE likes (user_id BIGINT NOT NULL REFERENCES users(id), post_id BIGINT NOT NULL REFERENCES posts(id), PRIMARY KEY (user_id, post_id));
CREATE TABLE comments (id BIGSERIAL PRIMARY KEY, post_id BIGINT NOT NULL REFERENCES posts(id), user_id BIGINT NOT NULL REFERENCES users(id), content TEXT NOT NULL, created_at TIMESTAMPTZ DEFAULT NOW());
-- Optional: denormalized counters ALTER TABLE posts ADD COLUMN likes_count INT DEFAULT 0;
```

### Q303: Design schema for e-commerce (products, orders, inventory).
```sql
CREATE TABLE categories (id BIGSERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, parent_id BIGINT REFERENCES categories(id));
CREATE TABLE products (id BIGSERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, price DECIMAL(10,2) NOT NULL CHECK (price >= 0), category_id BIGINT REFERENCES categories(id));
CREATE TABLE inventory (product_id BIGINT PRIMARY KEY REFERENCES products(id), quantity INT NOT NULL DEFAULT 0 CHECK (quantity >= 0), reserved INT NOT NULL DEFAULT 0);
CREATE TABLE orders (id BIGSERIAL PRIMARY KEY, user_id BIGINT NOT NULL REFERENCES users(id), status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending','confirmed','shipped','delivered','cancelled')), total_amount DECIMAL(12,2) NOT NULL, created_at TIMESTAMPTZ DEFAULT NOW());
CREATE TABLE order_items (id BIGSERIAL PRIMARY KEY, order_id BIGINT NOT NULL REFERENCES orders(id) ON DELETE CASCADE, product_id BIGINT NOT NULL REFERENCES products(id), quantity INT NOT NULL CHECK (quantity > 0), unit_price DECIMAL(10,2) NOT NULL);
```

### Q304: Design schema for messaging app.
```sql
CREATE TABLE conversations (id BIGSERIAL PRIMARY KEY, is_group BOOLEAN DEFAULT FALSE, name VARCHAR(255));
CREATE TABLE conversation_participants (conversation_id BIGINT REFERENCES conversations(id) ON DELETE CASCADE, user_id BIGINT REFERENCES users(id) ON DELETE CASCADE, PRIMARY KEY (conversation_id, user_id));
CREATE TABLE messages (id BIGSERIAL PRIMARY KEY, conversation_id BIGINT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE, sender_id BIGINT NOT NULL REFERENCES users(id), content TEXT NOT NULL, created_at TIMESTAMPTZ DEFAULT NOW());
CREATE INDEX idx_messages_conversation ON messages(conversation_id, created_at);
```

### Q305: Design schema for ride-sharing.
```sql
CREATE TABLE riders (id BIGSERIAL PRIMARY KEY, name VARCHAR(255), phone VARCHAR(20) UNIQUE, rating DECIMAL(2,1) DEFAULT 5.0);
CREATE TABLE drivers (id BIGSERIAL PRIMARY KEY, name VARCHAR(255), phone VARCHAR(20) UNIQUE, license_plate VARCHAR(20), status VARCHAR(20) DEFAULT 'offline' CHECK (status IN ('online','offline','on_trip')));
CREATE TABLE rides (id BIGSERIAL PRIMARY KEY, rider_id BIGINT REFERENCES riders(id), driver_id BIGINT REFERENCES drivers(id), status VARCHAR(20) DEFAULT 'requested', pickup_lat DECIMAL(10,7), pickup_lng DECIMAL(10,7), fare DECIMAL(10,2), requested_at TIMESTAMPTZ DEFAULT NOW());
```

### Q306: How to model hierarchical data?
**Adjacency List** (recursive CTE needed):
```sql
CREATE TABLE employees (id BIGSERIAL PRIMARY KEY, name TEXT, manager_id BIGINT REFERENCES employees(id));
```
**Materialized Path**: `path TEXT` e.g., "001.002.003"
**Nested Sets**: `lft INT, rgt INT`

### Q307: Normalization vs Denormalization trade-offs?
| | Normalized | Denormalized |
|--|-----------|-------------|
| Storage | Minimal | Redundant |
| Write speed | Faster | Slower |
| Read speed (JOINs) | Slower | Faster |
| Consistency | High | Risk of anomalies |

### Q308: What are caching strategies?
- **Cache Aside**: App checks cache → miss → read DB → write cache
- **Read Through**: Cache auto-loads from DB on miss
- **Write Through**: Write to cache, cache writes to DB synchronously
- **Write Behind**: Write to cache, async batch to DB (fast, risk data loss)

### Q309: How to model time-series data?
**Partitioned PostgreSQL:**
```sql
CREATE TABLE sensor_readings (sensor_id INT, ts TIMESTAMPTZ, value DOUBLE PRECISION) PARTITION BY RANGE (ts);
```
**TimescaleDB:**
```sql
CREATE EXTENSION timescaledb; SELECT create_hypertable('sensor_data', 'time');
```
**MongoDB bucket pattern:**
```javascript
{ sensor_id: 1, hour: ISODate("..."), readings: [{ ts: ..., value: 25.3 }] }
```

### Q310: What is polyglot persistence?
Using different databases for different use cases: PostgreSQL (structured), Redis (cache), Elasticsearch (search), Cassandra (analytics).

### Q311: What is CQRS?
Separating write models (commands) from read models (queries). Often combined with event sourcing.

### Q312: What is Event Sourcing?
Storing state changes as a sequence of events. Current state = replay(events).

### Q313: What is a star schema?
Fact table (measures) + dimension tables (attributes).
```sql
CREATE TABLE sales_fact (product_id INT, customer_id INT, date_id INT, amount DECIMAL(10,2));
CREATE TABLE dim_product (id INT, name TEXT, category TEXT);
```

### Q314: What is Snowflake schema?
Star schema where dimension tables are normalized.

### Q315: What is a partial unique index?
```sql
CREATE UNIQUE INDEX idx_unique_active_email ON users(email) WHERE is_active = TRUE;
```

### Q316: What is table partitioning vs sharding?
- **Partitioning**: Split table within same server (performance/manageability)
- **Sharding**: Split across servers (horizontal scaling)

### Q317: What is a hot spot / hot key?
A shard receiving disproportionate traffic. Avoid with good shard key.

### Q318: What is read replica?
Copy of database for read-only queries. Offloads read traffic.

### Q319: What is idle in transaction?
Transaction started but not committed. Holds resources. Detect via `pg_stat_activity`.

### Q320: What is the expand-migrate-contract pattern?
1. Expand: Add new columns
2. Migrate: Update application
3. Contract: Remove old columns

### Q321: What is soft delete?
```sql
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMPTZ;
SELECT * FROM users WHERE deleted_at IS NULL;
```

### Q322: What is OLTP vs OLAP?
| OLTP | OLAP |
|------|------|
| Many small transactions | Few complex queries |
| Row-oriented | Column-oriented |
| Normalized | Star/snowflake |

### Q323: What is a columnar database?
Stores data by column (ClickHouse, Redshift, BigQuery). Better for analytics.

### Q324: What is a data lake?
Central repository for raw data in any format. Used for big data/ML.

### Q325: What is a data warehouse?
Specialized database for analytics (Snowflake, Redshift, BigQuery).

### Q326: What is ETL vs ELT?
- **ETL**: Extract → Transform → Load (transform before loading)
- **ELT**: Extract → Load → Transform (transform in warehouse)

### Q327: What is database failover?
Automatic switch to standby when primary fails. Tools: Patroni, pg_auto_failover.

### Q328: What is RTO and RPO?
- **RTO**: Max acceptable downtime
- **RPO**: Max acceptable data loss

### Q329: What is a distributed transaction (XA)?
Transaction spanning multiple databases using 2-phase commit. Use Saga pattern for microservices.

### Q330: What is the Saga pattern?
Distributed transaction without 2PC. Each step is a local transaction + event. Compensating actions on failure.

### Q331: What is database idempotency?
Operation with same effect regardless of how many times applied.
```sql
INSERT INTO users (id, name) VALUES (1, 'Alice') ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
```

### Q332: How to model tags?
**Array (PostgreSQL):**
```sql
CREATE TABLE posts (id BIGSERIAL, tags TEXT[]); CREATE INDEX ON posts USING GIN (tags);
```
**Junction table:**
```sql
CREATE TABLE post_tags (post_id BIGINT REFERENCES posts(id), tag_id BIGINT REFERENCES tags(id), PRIMARY KEY (post_id, tag_id));
```

### Q333: How to model a rating system?
```sql
CREATE TABLE reviews (id BIGSERIAL, product_id BIGINT REFERENCES products(id), user_id BIGINT REFERENCES users(id), rating INT CHECK (rating >= 1 AND rating <= 5), UNIQUE (product_id, user_id));
```

### Q334: What is CDC (Change Data Capture)?
Capturing database changes in real-time. Tools: Debezium, PostgreSQL logical replication.

### Q335: What is a database proxy?
Intermediary between app and DB. Provides pooling, read/write splitting. PgBouncer, ProxySQL.

### Q336: What is ORM?
Object-Relational Mapping. Maps tables to objects.
```python
class User(Base): __tablename__ = "users"; id = Column(Integer, primary_key=True)
```

### Q337: What are migration tools?
Python: Alembic, Django migrations. Java: Flyway, Liquibase. Node: Prisma Migrate.

### Q338: What is zero-downtime migration?
Schema changes without taking app offline. Use expand-migrate-contract, online schema change tools.

### Q339: What is a database audit log?
Recording who did what. Implemented via triggers, pgaudit extension, application logging.

### Q340: What is denormalization for read-heavy workloads?
Pre-join tables, store counters, embed frequently accessed data. Increases write complexity but speeds reads.

### Q341: What is a database connection string?
```text
postgresql://user:password@host:5432/dbname?sslmode=require
mongodb://user:password@host:27017/dbname?replicaSet=rs0
```

### Q342: What is connection pooling in code?
```python
from sqlalchemy import create_engine
engine = create_engine("postgresql://user:pass@host/db", pool_size=10, max_overflow=20)
```

### Q343: What is statement_timeout?
```sql
SET statement_timeout = '30s';
```

### Q344: What is a database driver?
Library implementing wire protocol: psycopg2 (Python), node-postgres (Node), pgx (Go).

### Q345: What is charset/collation?
Charset: UTF-8, Latin1. Collation: sort/compare rules.
```sql
CREATE DATABASE mydb ENCODING 'UTF8' LC_COLLATE 'en_US.UTF-8';
```

### Q346: What is index intersection?
Using multiple indexes for one query. Both PostgreSQL (bitmap scan) and MongoDB support this.

### Q347: What is an expression index?
```sql
CREATE INDEX idx_lower_email ON users(LOWER(email));
```

### Q348: What is a partial index?
```sql
CREATE INDEX idx_active ON users(email) WHERE is_active = TRUE;
```

### Q349: What is an included column index (SQL Server)?
Extra columns in non-key index for covering, without affecting index order.

### Q350: What is a filtered index (SQL Server)?
Same as PostgreSQL partial index. Only indexes rows meeting a condition.

---

# Interview Query Problems (Q351–Q400)

### Q351: Find duplicate emails.
```sql
SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;
```

### Q352: Find the Nth highest salary.
```sql
SELECT DISTINCT salary FROM employees ORDER BY salary DESC OFFSET 1 LIMIT 1;  -- 2nd highest
-- Using window:
SELECT DISTINCT salary FROM (SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk FROM employees) ranked WHERE rnk = 3;
```

### Q353: Employees earning more than their manager.
```sql
SELECT e.name FROM employees e JOIN employees m ON e.manager_id = m.id WHERE e.salary > m.salary;
```

### Q354: Department-wise highest salary.
```sql
SELECT DISTINCT ON (department_id) department_id, name, salary FROM employees ORDER BY department_id, salary DESC;
-- Or with RANK():
SELECT department_id, name, salary FROM (SELECT *, RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rnk FROM employees) ranked WHERE rnk = 1;
```

### Q355: Running total / cumulative sum.
```sql
SELECT order_date, amount, SUM(amount) OVER (ORDER BY order_date) AS running_total FROM orders;
-- Partitioned:
SELECT user_id, order_date, amount, SUM(amount) OVER (PARTITION BY user_id ORDER BY order_date) AS user_total FROM orders;
```

### Q356: Moving average (7-day).
```sql
SELECT date, revenue, AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7d FROM daily_revenue;
```

### Q357: Finding consecutive rows (streaks).
```sql
WITH numbered AS (SELECT user_id, login_date, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn FROM user_logins)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_length
FROM (SELECT user_id, login_date, login_date - INTERVAL '1 day' * rn AS grp FROM numbered) sub
GROUP BY user_id, grp HAVING COUNT(*) >= 3;
```

### Q358: Finding overlapping date ranges.
```sql
SELECT a.id, b.id FROM bookings a JOIN bookings b ON a.id < b.id AND a.start_date < b.end_date AND a.end_date > b.start_date;
```

### Q359: Offset vs cursor-based pagination.
```sql
-- Offset (bad): SELECT * FROM posts ORDER BY id LIMIT 10 OFFSET 100000;
-- Cursor (efficient): SELECT * FROM posts WHERE id > 100000 ORDER BY id LIMIT 10;
```

### Q360: Second highest salary without LIMIT/OFFSET.
```sql
SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);
```

### Q361: Rank scores with DENSE_RANK.
```sql
SELECT score, DENSE_RANK() OVER (ORDER BY score DESC) AS rank FROM scores ORDER BY score DESC;
```

### Q362: Tree — find all descendants (recursive CTE).
```sql
WITH RECURSIVE descendants AS (SELECT id, name, parent_id FROM categories WHERE id = 1 UNION ALL SELECT c.id, c.name, c.parent_id FROM categories c JOIN descendants d ON c.parent_id = d.id) SELECT * FROM descendants;
```

### Q363: Tree — find all ancestors.
```sql
WITH RECURSIVE ancestors AS (SELECT id, name, parent_id FROM categories WHERE id = 10 UNION ALL SELECT c.id, c.name, c.parent_id FROM categories c JOIN ancestors a ON c.id = a.parent_id) SELECT * FROM ancestors WHERE id != 10;
```

### Q364: Time-series downsampling (hourly).
```sql
SELECT DATE_TRUNC('hour', ts) AS hour, sensor_id, AVG(value), MIN(value), MAX(value), COUNT(*) FROM sensor_data GROUP BY hour, sensor_id ORDER BY hour;
```

### Q365: Recursive CTE for org chart with path.
```sql
WITH RECURSIVE org_chart AS (
  SELECT id, name, manager_id, 1 AS level, name::TEXT AS path FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.name, e.manager_id, oc.level + 1, oc.path || ' -> ' || e.name FROM employees e JOIN org_chart oc ON e.manager_id = oc.id
) SELECT * FROM org_chart ORDER BY path;
```

### Q366: LATERAL join for top-N per group.
```sql
SELECT u.name, o.amount FROM users u CROSS JOIN LATERAL (SELECT amount FROM orders WHERE user_id = u.id ORDER BY created_at DESC LIMIT 3) o ORDER BY u.name;
```

### Q367: Find users who bought all products in a category.
```sql
SELECT o.user_id FROM orders o JOIN order_items oi ON o.id = oi.order_id JOIN products p ON oi.product_id = p.id WHERE p.category_id = 1 GROUP BY o.user_id HAVING COUNT(DISTINCT p.id) = (SELECT COUNT(*) FROM products WHERE category_id = 1);
```

### Q368: Median salary.
```sql
-- PostgreSQL:
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) FROM employees;
-- Generic:
SELECT AVG(salary) FROM (SELECT salary, ROW_NUMBER() OVER (ORDER BY salary) AS rn, COUNT(*) OVER () AS cnt FROM employees) ranked WHERE rn IN ((cnt+1)/2, (cnt+2)/2);
```

### Q369: Find gaps in a sequence.
```sql
SELECT id, LAG(id) OVER (ORDER BY id) AS prev_id, id - LAG(id) OVER (ORDER BY id) - 1 AS gap FROM sequence_table WHERE id > LAG(id) OVER (ORDER BY id) + 1;
-- Or:
WITH ordered AS (SELECT id, LAG(id) OVER (ORDER BY id) AS prev_id FROM sequence_table) SELECT prev_id + 1 AS gap_start, id - 1 AS gap_end FROM ordered WHERE id != prev_id + 1;
```

### Q370: Most recent order per user.
```sql
SELECT DISTINCT ON (user_id) * FROM orders ORDER BY user_id, created_at DESC;
-- Or ROW_NUMBER:
SELECT * FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn FROM orders) ranked WHERE rn = 1;
```

### Q371: Employees hired on their birthday.
```sql
SELECT * FROM employees WHERE EXTRACT(MONTH FROM hire_date) = EXTRACT(MONTH FROM birth_date) AND EXTRACT(DAY FROM hire_date) = EXTRACT(DAY FROM birth_date);
```

### Q372: Cumulative count by month.
```sql
SELECT DATE_TRUNC('month', created_at) AS month, COUNT(*) AS new_users, SUM(COUNT(*)) OVER (ORDER BY DATE_TRUNC('month', created_at)) AS cumulative FROM users GROUP BY month ORDER BY month;
```

### Q373: Sessionization — group user actions within 30-min gaps.
```sql
WITH numbered AS (SELECT user_id, action_time, LAG(action_time) OVER (PARTITION BY user_id ORDER BY action_time) AS prev_time FROM user_actions),
sessions AS (SELECT user_id, action_time, SUM(CASE WHEN prev_time IS NULL OR action_time - prev_time > INTERVAL '30 minutes' THEN 1 ELSE 0 END) OVER (PARTITION BY user_id ORDER BY action_time) AS session_id FROM numbered)
SELECT user_id, session_id, MIN(action_time) AS start, MAX(action_time) AS end, COUNT(*) AS actions FROM sessions GROUP BY user_id, session_id ORDER BY user_id, start;
```

### Q374: PIVOT — rows to columns.
```sql
SELECT department_id, COUNT(*) FILTER (WHERE status = 'active') AS active, COUNT(*) FILTER (WHERE status = 'inactive') AS inactive FROM employees GROUP BY department_id;
```

### Q375: UNPIVOT — columns to rows.
```sql
SELECT id, quarter, revenue FROM quarterly_revenue CROSS JOIN LATERAL (VALUES ('q1', q1), ('q2', q2), ('q3', q3), ('q4', q4)) AS q(quarter, revenue);
```

### Q376: JSON extraction in PostgreSQL.
```sql
SELECT id, metadata->>'city' FROM users WHERE metadata @> '{"country": "US"}';
```

### Q377: Find orphaned records (no FK match).
```sql
SELECT o.* FROM orders o LEFT JOIN users u ON o.user_id = u.id WHERE u.id IS NULL;
-- Or: SELECT * FROM orders WHERE NOT EXISTS (SELECT 1 FROM users WHERE id = user_id);
```

### Q378: Compare two tables for differences.
```sql
(SELECT * FROM table_a EXCEPT SELECT * FROM table_b) UNION ALL (SELECT * FROM table_b EXCEPT SELECT * FROM table_a);
```

### Q379: Find consecutive date ranges (condense dates).
```sql
WITH numbered AS (SELECT date, date - ROW_NUMBER() OVER (ORDER BY date)::INT AS grp FROM calendar_dates WHERE is_working_day = TRUE)
SELECT MIN(date) AS range_start, MAX(date) AS range_end, COUNT(*) AS days FROM numbered GROUP BY grp ORDER BY range_start;
```

### Q380: Recursive CTE for Fibonacci sequence.
```sql
WITH RECURSIVE fib(n, a, b) AS (VALUES (1, 0, 1) UNION ALL SELECT n + 1, b, a + b FROM fib WHERE n < 20) SELECT n, b AS fib_number FROM fib;
```

### Q381: Month-over-month revenue comparison.
```sql
SELECT DATE_TRUNC('month', order_date) AS month, SUM(amount) AS revenue,
  LAG(SUM(amount)) OVER (ORDER BY DATE_TRUNC('month', order_date)) AS prev,
  ROUND((SUM(amount) - LAG(SUM(amount)) OVER (ORDER BY DATE_TRUNC('month', order_date))) / NULLIF(LAG(SUM(amount)) OVER (ORDER BY DATE_TRUNC('month', order_date)), 0) * 100, 2) AS mom_pct
FROM orders GROUP BY month ORDER BY month;
```

### Q382: Find session duration per user.
```sql
SELECT user_id, MIN(created_at) AS start, MAX(created_at) AS end, EXTRACT(EPOCH FROM MAX(created_at) - MIN(created_at)) AS duration_seconds
FROM (SELECT *, ROW_NUMBER() OVER (ORDER BY created_at) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) AS grp FROM user_actions) sub
GROUP BY user_id, grp ORDER BY user_id, start;
```

### Q383: Daily active users with rolling 28-day MAU.
```sql
WITH daily AS (SELECT DATE(login_time) AS login_date, COUNT(DISTINCT user_id) AS dau FROM user_logins WHERE login_time >= NOW() - INTERVAL '30 days' GROUP BY login_date)
SELECT login_date, dau, SUM(dau) OVER (ORDER BY login_date ROWS BETWEEN 27 PRECEDING AND CURRENT ROW) AS mau_rolling FROM daily ORDER BY login_date;
```

### Q384: Employees hired in last 90 days with salary above department average.
```sql
SELECT e.name, e.salary FROM employees e JOIN (SELECT department_id, AVG(salary) AS avg_salary FROM employees GROUP BY department_id) d ON e.department_id = d.department_id WHERE e.hire_date >= NOW() - INTERVAL '90 days' AND e.salary > d.avg_salary;
```

### Q385: MongoDB — Top 5 most ordered products.
```javascript
db.orders.aggregate([
  { $unwind: "$items" },
  { $group: { _id: "$items.product_id", totalOrdered: { $sum: "$items.quantity" } } },
  { $sort: { totalOrdered: -1 } },
  { $limit: 5 }
]);
```

### Q386: MongoDB — Average rating per product.
```javascript
db.reviews.aggregate([
  { $group: { _id: "$product_id", avgRating: { $avg: "$rating" }, count: { $sum: 1 } } },
  { $sort: { avgRating: -1 } }
]);
```

### Q387: MongoDB — User activity feed (latest 10 posts from followed users).
```javascript
db.posts.aggregate([
  { $match: { user_id: { $in: db.follows.findOne({ follower_id: currentUser }).following } } },
  { $sort: { created_at: -1 } },
  { $limit: 10 }
]);
```

### Q388: MongoDB — Add comment and increment count atomically.
```javascript
db.posts.updateOne(
  { _id: postId },
  { $push: { comments: { user: userId, text: "Nice!", created_at: new Date() } }, $inc: { comment_count: 1 } }
);
```

### Q389: MongoDB — Find products with reviews containing specific keyword.
```javascript
db.products.aggregate([
  { $lookup: { from: "reviews", localField: "_id", foreignField: "product_id", as: "reviews" } },
  { $match: { "reviews.text": { $regex: /amazing/i } } },
  { $project: { name: 1, "reviews.text": 1 } }
]);
```

### Q390: MongoDB — Cursor-based pagination.
```javascript
const pageSize = 10;
// First page:
db.posts.find().sort({ _id: -1 }).limit(pageSize);
// Next page (pass last _id from previous):
db.posts.find({ _id: { $lt: lastId } }).sort({ _id: -1 }).limit(pageSize);
```

### Q391: PostgreSQL — Find products that have never been ordered.
```sql
SELECT p.* FROM products p LEFT JOIN order_items oi ON p.id = oi.product_id WHERE oi.product_id IS NULL;
```

### Q392: PostgreSQL — Update with JOIN (bulk price update).
```sql
UPDATE products p SET price = price * 1.15 FROM categories c WHERE p.category_id = c.id AND c.name = 'Electronics';
```

### Q393: PostgreSQL — Delete duplicates keeping lowest ID.
```sql
DELETE FROM users WHERE id NOT IN (SELECT MIN(id) FROM users GROUP BY email);
-- Or using window:
DELETE FROM users WHERE id IN (SELECT id FROM (SELECT id, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS rn FROM users) dup WHERE rn > 1);
```

### Q394: PostgreSQL — Random sampling.
```sql
SELECT * FROM users ORDER BY RANDOM() LIMIT 100;
-- For large tables (more efficient):
SELECT * FROM users TABLESAMPLE SYSTEM(1);  -- 1% sample
```

### Q395: PostgreSQL — Find the most common value (mode).
```sql
SELECT status, COUNT(*) AS cnt FROM orders GROUP BY status ORDER BY cnt DESC LIMIT 1;
```

### Q396: PostgreSQL — Find first and last value in a group.
```sql
SELECT user_id, MIN(created_at) AS first_order, MAX(created_at) AS last_order, COUNT(*) AS total FROM orders GROUP BY user_id;
```

### Q397: PostgreSQL — Split delimited string into rows.
```sql
SELECT id, unnest(string_to_array(tags, ',')) AS tag FROM projects;
```

### Q398: PostgreSQL — String aggregation (rows to comma-separated).
```sql
SELECT department_id, STRING_AGG(name, ', ' ORDER BY name) AS employees FROM employees GROUP BY department_id;
```

### Q399: PostgreSQL — FOR UPDATE locking (pessimistic locking).
```sql
BEGIN;
SELECT * FROM inventory WHERE product_id = 101 FOR UPDATE;
-- Now we have an exclusive lock on this row
UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 101;
COMMIT;
```

### Q400: PostgreSQL — Upsert with complex logic.
```sql
INSERT INTO user_stats (user_id, total_orders, total_spent, last_order_date)
VALUES (1, 1, 100.00, NOW())
ON CONFLICT (user_id) DO UPDATE SET
  total_orders = user_stats.total_orders + 1,
  total_spent = user_stats.total_spent + EXCLUDED.total_spent,
  last_order_date = EXCLUDED.last_order_date;
```

---

> **Pro Tip:** For interviews, focus on understanding the trade-offs between SQL vs NoSQL, normalization vs denormalization, indexing strategies, transaction isolation levels, and being able to write complex queries (window functions, recursive CTEs, LATERAL JOINs). Practice the query problems in the last section — they appear frequently at YC and top-company interviews.

### Q401: PostgreSQL — Weighted moving average.
```sql
SELECT date, revenue,
  SUM(revenue * weight) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) / SUM(weight) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS wma_7d
FROM daily_revenue, LATERAL (VALUES (1.0)) AS t(weight);
```

### Q402: PostgreSQL — Generate series of dates.
```sql
SELECT generate_series('2024-01-01'::DATE, '2024-12-31'::DATE, '1 day'::INTERVAL)::DATE AS date;
-- Fill missing dates:
SELECT g.date, COALESCE(SUM(s.amount), 0) AS revenue
FROM generate_series('2024-01-01'::DATE, '2024-12-31'::DATE, '1 day') g(date)
LEFT JOIN sales s ON s.sale_date = g.date
GROUP BY g.date ORDER BY g.date;
```

### Q403: PostgreSQL — JSONB aggregation.
```sql
SELECT user_id, JSONB_AGG(JSONB_BUILD_OBJECT('id', id, 'amount', amount)) AS orders_json
FROM orders GROUP BY user_id;
```

### Q404: PostgreSQL — Array contains any element.
```sql
SELECT * FROM projects WHERE tags && ARRAY['python', 'postgres'];  -- overlap
```

### Q405: PostgreSQL — Array contains all elements.
```sql
SELECT * FROM projects WHERE tags @> ARRAY['python', 'postgres'];  -- contains
```

### Q406: PostgreSQL — Fuzzy string matching with pg_trgm.
```sql
SELECT * FROM users WHERE similarity(name, 'jon') > 0.5 ORDER BY similarity(name, 'jon') DESC;
```

### Q407: PostgreSQL — Conditional unique index.
```sql
CREATE UNIQUE INDEX idx_one_active_email ON users(email) WHERE is_active = TRUE;
```

### Q408: PostgreSQL — Find table bloat.
```sql
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)), n_dead_tup,
  ROUND(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS bloat_pct
FROM pg_stat_user_tables WHERE n_dead_tup > 1000 ORDER BY bloat_pct DESC;
```

### Q409: PostgreSQL — Counting distinct values with multiple conditions.
```sql
SELECT COUNT(DISTINCT CASE WHEN status = 'active' THEN user_id END) AS active_users,
       COUNT(DISTINCT CASE WHEN status = 'inactive' THEN user_id END) AS inactive_users
FROM subscriptions;
```

### Q410: PostgreSQL — Find rows with matching arrays.
```sql
SELECT * FROM posts WHERE tags @> ARRAY['database', 'sql'];
```

### Q411: PostgreSQL — Pivot with crosstab (tablefunc).
```sql
CREATE EXTENSION IF NOT EXISTS tablefunc;
SELECT * FROM crosstab(
  $$SELECT department_id, status::TEXT, COUNT(*)::INT FROM employees GROUP BY 1, 2 ORDER BY 1, 2$$,
  $$VALUES ('active'), ('inactive'), ('terminated')$$
) AS ct(dept_id INT, active INT, inactive INT, terminated INT);
```

### Q412: PostgreSQL — Percentile and distribution.
```sql
SELECT PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY salary) AS q1,
       PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY salary) AS median,
       PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY salary) AS q3,
       PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY salary) AS p90
FROM employees;
```

### Q413: PostgreSQL — Width_bucket for histogram.
```sql
SELECT width_bucket(salary, 0, 200000, 10) AS bucket,
       MIN(salary) AS min_sal, MAX(salary) AS max_sal, COUNT(*)
FROM employees GROUP BY bucket ORDER BY bucket;
```

### Q414: PostgreSQL — Recursive CTE for tree path enumeration.
```sql
WITH RECURSIVE cat_tree AS (
  SELECT id, name, parent_id, name::TEXT AS path FROM categories WHERE parent_id IS NULL
  UNION ALL
  SELECT c.id, c.name, c.parent_id, ct.path || ' > ' || c.name
  FROM categories c JOIN cat_tree ct ON c.parent_id = ct.id
) SELECT * FROM cat_tree ORDER BY path;
```

### Q415: PostgreSQL — Materialized view for dashboard.
```sql
CREATE MATERIALIZED VIEW mv_dashboard AS
SELECT DATE_TRUNC('day', created_at) AS day, COUNT(DISTINCT user_id) AS dau,
       COUNT(*) AS events, SUM(revenue) AS revenue
FROM user_events GROUP BY 1;
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_dashboard;  -- non-blocking refresh
```

### Q416: PostgreSQL — Advisory locks for application-level coordination.
```sql
SELECT pg_advisory_lock(12345);   -- acquire app-level lock
-- ... critical section ...
SELECT pg_advisory_unlock(12345); -- release
```

### Q417: PostgreSQL — LISTEN/NOTIFY for real-time notifications.
```sql
-- Session 1: LISTEN channel;
LISTEN new_order;
-- Session 2: NOTIFY channel, payload;
NOTIFY new_order, '{"order_id": 42}';
```

### Q418: PostgreSQL — Using pg_try_advisory_lock for non-blocking lock.
```sql
SELECT pg_try_advisory_lock(12345);  -- returns true if lock acquired, false if not
```

### Q419: PostgreSQL — Multicolumn GIN index for JSONB.
```sql
CREATE INDEX idx_events_custom ON events USING GIN (payload jsonb_path_ops);
-- jsonb_path_ops is smaller and faster for path queries
```

### Q420: PostgreSQL — Incremental materialized view maintenance using triggers.
```sql
CREATE OR REPLACE FUNCTION refresh_dashboard() RETURNS TRIGGER AS $$
BEGIN
  REFRESH MATERIALIZED VIEW CONCURRENTLY mv_dashboard;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_refresh_dashboard AFTER INSERT ON user_events FOR EACH STATEMENT EXECUTE FUNCTION refresh_dashboard();
```
