# DBMS — 100 Interview Q&A

---

## Q1: What is a DBMS?
**A:** A Database Management System (DBMS) is software that allows users to define, create, maintain, and control access to the database. It provides an interface between the data and the user or application.

**Code:**
```sql
-- A DBMS sits between applications and the stored data, adding DDL/DML,
-- security, and concurrency control on top of raw storage.
CREATE TABLE employees (
  emp_id   INT PRIMARY KEY,
  emp_name VARCHAR(100)
);

INSERT INTO employees VALUES (1, 'Alice');
SELECT * FROM employees;
```

## Q2: What is a database?
**A:** A database is an organized collection of structured data stored electronically, typically in a computer system, and managed by a DBMS.

**Code:**
```sql
-- The database is the managed, organized collection of structured data.
CREATE DATABASE school;

USE school;

CREATE TABLE students (id INT PRIMARY KEY, name VARCHAR(50));
INSERT INTO students VALUES (1, 'Aayush');
SELECT * FROM students;
```

## Q3: What are the advantages of DBMS over file systems?
**A:** Data redundancy control, data consistency, data sharing, security, backup or recovery, concurrency control, and data independence.

**Code:**
```sql
-- Multiple users see ONE consistent, shared source of truth (file systems
-- would give each user a separate, possibly stale copy).
CREATE TABLE accounts (
  account_id INT PRIMARY KEY,
  balance    DECIMAL(10, 2) NOT NULL CHECK (balance >= 0)   -- consistency
);

BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
COMMIT;

SELECT * FROM accounts WHERE account_id = 1;   -- data sharing, single truth
```

## Q4: What is RDBMS?
**A:** Relational DBMS stores data in tables (relations) with rows and columns, and relationships are established using keys. Examples: MySQL, Oracle, PostgreSQL.

**Code:**
```sql
-- Data lives in tables; relations are expressed through keys.
CREATE TABLE departments (dept_id INT PRIMARY KEY, name VARCHAR(50));

CREATE TABLE employees (
  emp_id  INT PRIMARY KEY,
  dept_id INT,
  FOREIGN KEY (dept_id) REFERENCES departments(dept_id)   -- relationship
);
```

## Q5: What is a primary key?
**A:** A primary key is a column or set of columns that uniquely identifies each row in a table. It cannot be NULL and must be unique.

**Code:**
```sql
CREATE TABLE users (
  user_id INT PRIMARY KEY,        -- unique AND NOT NULL
  email   VARCHAR(100)
);

INSERT INTO users VALUES (1, 'a@b.com');
INSERT INTO users VALUES (1, 'c@d.com');       -- ERROR: duplicate key
INSERT INTO users VALUES (NULL, 'e@f.com');    -- ERROR: NULL not allowed
```

## Q6: What is a foreign key?
**A:** A foreign key is a column that creates a link between two tables. It references the primary key of another table to enforce referential integrity.

**Code:**
```sql
CREATE TABLE orders (
  order_id    INT PRIMARY KEY,
  customer_id INT,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- customer_id must exist in customers (or be NULL):
INSERT INTO orders VALUES (10, 999);   -- ERROR if no customer 999
```

## Q7: What is a candidate key?
**A:** A candidate key is a set of attributes that can uniquely identify a row. A table may have multiple candidate keys; one becomes the primary key.

**Code:**
```sql
-- Both employee_code and email can uniquely identify a row,
-- so each is a candidate key; exactly one is promoted to PRIMARY KEY.
CREATE TABLE employee (
  employee_code VARCHAR(10) UNIQUE,
  email         VARCHAR(100) UNIQUE,
  name          VARCHAR(50)
);
```

## Q8: What is a super key?
**A:** A super key is any set of attributes that uniquely identifies rows. It may contain extra attributes not needed for uniqueness.

**Code:**
```sql
-- {employee_code} identifies rows AND {employee_code, name} does too —
-- the second is a super key carrying a redundant, non-required attribute.
CREATE TABLE employee (
  employee_code VARCHAR(10) PRIMARY KEY,
  name          VARCHAR(50)
);

-- Prove redundancy: uniqueness already guaranteed by the code alone.
SELECT employee_code, name FROM employee;
```

## Q9: What is an alternate key?
**A:** An alternate key is a candidate key not chosen as the primary key.

**Code:**
```sql
-- candidate keys: employee_code and email
-- employee_code is chosen as PK; email — an alternate key — stays UNIQUE.
CREATE TABLE employee (
  employee_code VARCHAR(10) PRIMARY KEY,
  email         VARCHAR(100) UNIQUE,    -- alternate key
  name          VARCHAR(50)
);
```

## Q10: What is a composite key?
**A:** A composite key is a primary key made of two or more columns together to uniquely identify a row.

**Code:**
```sql
-- A student can take many courses and a course has many students;
-- only the PAIR is unique.
CREATE TABLE course_enrollment (
  student_id INT NOT NULL,
  course_id  INT NOT NULL,
  grade      CHAR(1),
  PRIMARY KEY (student_id, course_id)   -- composite primary key
);
```

## Q11: What is a surrogate key?
**A:** A surrogate key is an artificial key (for example, auto-increment ID) used as a primary key, having no business meaning.

**Code:**
```sql
-- order_id has no real-world meaning; the DB generates it automatically.
CREATE TABLE orders (
  order_id  INT AUTO_INCREMENT PRIMARY KEY,   -- surrogate key
  customer_id INT,
  placed_on   DATETIME
);
```

## Q12: What is normalization?
**A:** Normalization is the process of organizing data to minimize redundancy and dependency by dividing tables into smaller related tables.

**Code:**
```sql
-- Before: product data repeats on every order row (redundant).
CREATE TABLE orders_flat (order_id INT, customer VARCHAR(50),
                          product VARCHAR(50), qty INT);

-- After: split into related tables, redundancy removed.
CREATE TABLE orders (order_id INT PRIMARY KEY, customer VARCHAR(50));
CREATE TABLE order_items (
  order_id INT,
  product  VARCHAR(50),
  qty      INT,
  PRIMARY KEY (order_id, product)
);
```

## Q13: What is 1NF?
**A:** First Normal Form: each table cell holds a single atomic value, and each record is unique.

**Code:**
```sql
-- Violates 1NF: a cell holds multiple values (comma-separated list).
CREATE TABLE bad_orders (cust_id INT, products VARCHAR(100));
INSERT INTO bad_orders VALUES (1, 'apple,banana');

-- 1NF: one atomic value per cell, one row per product.
CREATE TABLE orders_1nf (
  cust_id  INT,
  product  VARCHAR(20),
  PRIMARY KEY (cust_id, product)
);
INSERT INTO orders_1nf VALUES (1, 'apple'), (1, 'banana');
```

## Q14: What is 2NF?
**A:** Second Normal Form: table is in 1NF and all non-key attributes are fully functionally dependent on the primary key (no partial dependency).

**Code:**
```sql
-- 1NF, but subject_name depends on only PART of the composite key.
CREATE TABLE enrollment (
  student_id INT, course_id INT, subject_name VARCHAR(50),
  grade CHAR(1), PRIMARY KEY (student_id, course_id)
);

-- 2NF: move the partially-dependent column into its own table.
CREATE TABLE subjects (course_id INT PRIMARY KEY, subject_name VARCHAR(50));
CREATE TABLE enrollment_2nf (
  student_id INT, course_id INT, grade CHAR(1),
  PRIMARY KEY (student_id, course_id)
);
```

## Q15: What is 3NF?
**A:** Third Normal Form: table is in 2NF and has no transitive dependency (non-key attributes depend only on the key).

**Code:**
```sql
-- 2NF, but city depends on zip_code, not on the key: transitive dependency.
CREATE TABLE customers (
  customer_id INT PRIMARY KEY, zip_code VARCHAR(10), city VARCHAR(50)
);

-- 3NF: move the dependent column out; city now depends only on the key.
CREATE TABLE customers_3nf (customer_id INT PRIMARY KEY, zip_code VARCHAR(10));
CREATE TABLE zip_codes (zip_code VARCHAR(10) PRIMARY KEY, city VARCHAR(50));
```

## Q16: What is BCNF?
**A:** Boyce-Codd Normal Form: a stronger 3NF; for every functional dependency X to Y, X must be a super key.

**Code:**
```sql
-- Violates BCNF: professor -> subject, yet professor is not a super key.
CREATE TABLE assignment (
  professor VARCHAR(50), subject VARCHAR(50), student VARCHAR(50),
  PRIMARY KEY (student, subject)
);

-- BCNF: split so every determinant is a super key in its table.
CREATE TABLE enrollment (student VARCHAR(50), subject VARCHAR(50),
                         PRIMARY KEY (student, subject));
CREATE TABLE teaches (professor VARCHAR(50), subject VARCHAR(50),
                      PRIMARY KEY (professor, subject));
```

## Q17: What is 4NF?
**A:** Fourth Normal Form: table is in BCNF and has no multi-valued dependencies.

**Code:**
```sql
-- Multi-valued dependency: skills and languages vary independently, so the
-- table multiplies rows for no reason.
CREATE TABLE employee (
  emp_name VARCHAR(50), skill VARCHAR(50), language VARCHAR(50)
);

-- 4NF: put each independent multi-valued fact into its own table.
CREATE TABLE emp_skills (emp_name VARCHAR(50), skill VARCHAR(50),
                         PRIMARY KEY (emp_name, skill));
CREATE TABLE emp_languages (emp_name VARCHAR(50), language VARCHAR(50),
                            PRIMARY KEY (emp_name, language));
```

## Q18: What is 5NF?
**A:** Fifth Normal Form: table is in 4NF and cannot be decomposed into smaller tables without loss (join dependency).

**Code:**
```sql
-- A join dependency: the supplier/product/project ternary relationship is
-- reconstructed by joining three projections.
CREATE TABLE contracts (product VARCHAR(20), supplier VARCHAR(20), project VARCHAR(20));

-- 5NF decomposition — the three tables join back losslessly.
CREATE TABLE supply (product VARCHAR(20), supplier VARCHAR(20),
                     PRIMARY KEY (product, supplier));
CREATE TABLE uses_product (product VARCHAR(20), project VARCHAR(20),
                           PRIMARY KEY (product, project));
CREATE TABLE procures (supplier VARCHAR(20), project VARCHAR(20),
                       PRIMARY KEY (supplier, project));
```

## Q19: What is denormalization?
**A:** Denormalization is the process of adding redundant data to tables to improve read performance at the cost of write complexity.

**Code:**
```sql
-- Normalized: aggregation on every read.
SELECT order_id, SUM(qty * price) AS total
FROM order_items GROUP BY order_id;

-- Denormalized: redundant total column avoids the aggregation at read time.
ALTER TABLE orders ADD COLUMN total_amount DECIMAL(10, 2);
UPDATE orders o
SET total_amount = (SELECT SUM(qty * price) FROM order_items i
                    WHERE i.order_id = o.order_id);
```

## Q20: What is a transaction?
**A:** A transaction is a logical unit of work consisting of one or more database operations (read or write) executed as a whole.

**Code:**
```sql
START TRANSACTION;
  UPDATE accounts SET balance = balance - 500 WHERE account_id = 1;
  UPDATE accounts SET balance = balance + 500 WHERE account_id = 2;
COMMIT;   -- both updates apply (or neither) as one unit of work
```

## Q21: What are ACID properties?
**A:** Atomicity, Consistency, Isolation, Durability — guarantees a transaction is reliable.

**Code:**
```sql
-- Atomicity: both updates succeed or neither does.
START TRANSACTION;
  UPDATE accounts SET balance = balance - 500 WHERE account_id = 1;
  UPDATE accounts SET balance = balance + 500 WHERE account_id = 2;
COMMIT;

-- Isolation is chosen per transaction:
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- (Consistency: CHECK/FK constraints; Durability: COMMIT above.)
```

## Q22: Explain Atomicity.
**A:** Atomicity ensures a transaction is all-or-nothing; either all operations complete or none do.

**Code:**
```sql
START TRANSACTION;
  UPDATE accounts SET balance = balance - 500 WHERE account_id = 1;
  UPDATE accounts SET balance = balance + 500 WHERE account_id = 2;
ROLLBACK;   -- encountered an error mid-flight:
            -- BOTH updates are undone — all-or-nothing
```

## Q23: Explain Consistency.
**A:** Consistency ensures a transaction brings the database from one valid state to another, preserving invariants.

**Code:**
```sql
-- Invariants enforced with CHECK and FK: the DB rejects invalid states.
CREATE TABLE accounts (
  account_id INT PRIMARY KEY,
  balance    DECIMAL(10,2) NOT NULL CHECK (balance >= 0),  -- no negatives
  cust_id    INT REFERENCES customers(cust_id)             -- valid links
);

UPDATE accounts SET balance = -50 WHERE account_id = 1;    -- ERROR
```

## Q24: Explain Isolation.
**A:** Isolation ensures concurrent transactions do not interfere; each appears to run independently.

**Code:**
```sql
-- Session A                                          Session B
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN;
  UPDATE accounts SET balance = 900 WHERE account_id = 1;
                                                     SELECT balance
                                                       FROM accounts
                                                      WHERE account_id = 1;
                                                     -- still 100: cannot see
                                                     -- uncommitted data
  COMMIT;                        -- now B's next read sees 900
```

## Q25: Explain Durability.
**A:** Durability ensures once a transaction commits, its changes persist even after a system failure.

**Code:**
```sql
BEGIN;
  UPDATE accounts SET balance = 0 WHERE account_id = 1;
COMMIT;   -- once COMMIT returns, this change survives crashes/restarts
```

## Q26: What is a join?
**A:** A join combines rows from two or more tables based on a related column.

**Code:**
```sql
SELECT o.order_id, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;   -- related column
```

## Q27: What is an inner join?
**A:** Inner join returns only rows with matching values in both tables.

**Code:**
```sql
SELECT e.name, d.name AS dept
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id;
-- employees without a department are NOT returned
```

## Q28: What is a left join?
**A:** Left join returns all rows from the left table and matched rows from the right; unmatched right side is NULL.

**Code:**
```sql
SELECT c.name, o.order_id
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id;
-- every customer returned; those with no orders get NULL order_id
```

## Q29: What is a right join?
**A:** Right join returns all rows from the right table and matched rows from the left; unmatched left side is NULL.

**Code:**
```sql
SELECT o.order_id, c.name
FROM orders o
RIGHT JOIN customers c ON o.customer_id = c.customer_id;
-- every customer (right side) returned; unmatched left side is NULL
```

## Q30: What is a full outer join?
**A:** Full outer join returns all rows from both tables, with NULLs where there is no match.

**Code:**
```sql
SELECT c.name, o.order_id
FROM customers c
FULL OUTER JOIN orders o ON o.customer_id = c.customer_id;
-- all rows from BOTH sides; NULLs fill whichever side has no match
```

## Q31: What is a self join?
**A:** A self join joins a table with itself to compare rows within the same table.

**Code:**
```sql
SELECT e.name AS employee, m.name AS manager
FROM employees e
JOIN employees m ON e.manager_id = m.emp_id;   -- table joined with itself
```

## Q32: What is a cross join?
**A:** A cross join returns the Cartesian product of two tables (every row combined with every row).

**Code:**
```sql
SELECT s.size, c.color
FROM sizes s
CROSS JOIN colors c;
-- 3 sizes x 4 colors = 12 rows (every combination)
```

## Q33: What is SQL?
**A:** SQL (Structured Query Language) is used to manage and manipulate relational databases.

**Code:**
```sql
-- One language for defining and manipulating relational data.
CREATE TABLE products (id INT PRIMARY KEY, name VARCHAR(50), price DECIMAL(8,2));
INSERT INTO products VALUES (1, 'Keyboard', 49.99);
SELECT name FROM products WHERE price < 100;
```

## Q34: What are DDL commands?
**A:** Data Definition Language commands define structure: CREATE, ALTER, DROP, TRUNCATE.

**Code:**
```sql
CREATE TABLE t (id INT);                 -- CREATE: define structure
ALTER TABLE t ADD COLUMN name VARCHAR(50); -- ALTER: change structure
TRUNCATE TABLE t;                        -- TRUNCATE: clear rows, keep structure
DROP TABLE t;                            -- DROP: remove structure
```

## Q35: What are DML commands?
**A:** Data Manipulation Language commands manage data: SELECT, INSERT, UPDATE, DELETE.

**Code:**
```sql
INSERT INTO products (id, name) VALUES (1, 'Mouse');   -- INSERT
SELECT * FROM products;                                 -- SELECT
UPDATE products SET price = 20.00 WHERE id = 1;         -- UPDATE
DELETE FROM products WHERE id = 1;                      -- DELETE
```

## Q36: What are DCL commands?
**A:** Data Control Language commands manage access: GRANT, REVOKE.

**Code:**
```sql
GRANT SELECT, INSERT ON products TO analyst;   -- give permissions
REVOKE INSERT ON products FROM analyst;        -- take them away
```

## Q37: What are TCL commands?
**A:** Transaction Control Language: COMMIT, ROLLBACK, SAVEPOINT, SET TRANSACTION.

**Code:**
```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

SAVEPOINT sp1;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
ROLLBACK TO sp1;     -- undo just the update, keep earlier work

COMMIT;              -- make remaining changes permanent
```

## Q38: Difference between TRUNCATE and DELETE?
**A:** TRUNCATE removes all rows without logging individual deletions (cannot roll back in some DBs), resets identity; DELETE removes specific rows with logging and can be rolled back.

**Code:**
```sql
-- DELETE: row-by-row, logged, rollback-able, WHERE allowed.
DELETE FROM orders WHERE status = 'cancelled';

-- TRUNCATE: all rows instantly, minimal logging, resets the identity column.
TRUNCATE TABLE orders;
```

## Q39: Difference between DROP and TRUNCATE?
**A:** DROP removes the table structure and data; TRUNCATE removes only data, keeping the structure.

**Code:**
```sql
TRUNCATE TABLE orders;   -- removes all rows, structure stays usable
SELECT * FROM orders;    -- works: empty table

DROP TABLE orders;       -- removes structure AND data
SELECT * FROM orders;    -- ERROR: table no longer exists
```

## Q40: What is an index?
**A:** An index is a data structure (often B-tree) that improves query speed by providing fast lookup on columns.

**Code:**
```sql
-- A B-tree index makes equality/range lookups logarithmic instead of a scan.
CREATE INDEX idx_users_email ON users (email);

EXPLAIN SELECT * FROM users WHERE email = 'a@b.com';
-- planner switches from Seq Scan to Index Scan using idx_users_email
```

## Q41: What is a clustered index?
**A:** A clustered index determines the physical order of data in a table; a table can have only one.

**Code:**
```sql
-- SQL Server: the clustered index physically orders the rows, so exactly one.
CREATE TABLE users (
  user_id INT PRIMARY KEY CLUSTERED,   -- only one CLUSTERED index per table
  email   VARCHAR(100)
);
```

## Q42: What is a non-clustered index?
**A:** A non-clustered index stores a separate structure with pointers to the actual data rows; a table can have many.

**Code:**
```sql
-- Separate structure: key values + row pointers. Many allowed per table.
CREATE NONCLUSTERED INDEX idx_users_email ON users (email);

SELECT * FROM users WHERE email = 'a@b.com';
-- fast key lookup, then a pointer hop to the actual data row
```

## Q43: What is a unique index?
**A:** A unique index ensures the indexed column has no duplicate values.

**Code:**
```sql
CREATE UNIQUE INDEX idx_users_email ON users (email);

INSERT INTO users (id, email) VALUES (1, 'a@b.com');
INSERT INTO users (id, email) VALUES (2, 'a@b.com');   -- ERROR: duplicate
```

## Q44: When should you avoid indexes?
**A:** On small tables, columns with few distinct values, or frequently updated columns where write overhead outweighs read benefit.

**Code:**
```sql
-- Tiny table (10 rows): a full scan beats index-maintenance overhead.
CREATE TABLE flags (id INT PRIMARY KEY, status CHAR(1));

EXPLAIN SELECT * FROM flags WHERE status = 'Y';   -- Seq Scan, no index needed

-- 'status' has 2 distinct values -> selectivity too low to index.
-- Frequently-updated columns pay the index update on EVERY write:
UPDATE flags SET status = 'N' WHERE id = 1;       -- now updates the index too
```

## Q45: What is a view?
**A:** A view is a virtual table based on a SQL query; it does not store data itself (except materialized views).

**Code:**
```sql
CREATE VIEW active_customers AS
SELECT customer_id, name FROM customers WHERE active = 1;

-- Queries treat the view like a table, but no data is stored by it.
SELECT * FROM active_customers;
```

## Q46: What is a materialized view?
**A:** A materialized view stores the query result physically and must be refreshed; good for expensive aggregations.

**Code:**
```sql
-- Result is physically stored, so the aggregation is not re-run per query.
CREATE MATERIALIZED VIEW mv_sales_totals AS
SELECT product_id, SUM(amount) AS total
FROM sales GROUP BY product_id;

-- Refresh it when the underlying sales change.
REFRESH MATERIALIZED VIEW mv_sales_totals;
```

## Q47: What is a stored procedure?
**A:** A stored procedure is a precompiled set of SQL statements stored in the database, callable by name.

**Code:**
```sql
CREATE PROCEDURE get_customer(IN cid INT)
BEGIN
  SELECT name FROM customers WHERE customer_id = cid;
END;

CALL get_customer(42);   -- invoke the precompiled procedure by name
```

## Q48: What is a trigger?
**A:** A trigger is a stored procedure that automatically executes in response to INSERT, UPDATE, or DELETE events.

**Code:**
```sql
-- Runs automatically after any row is inserted into orders.
CREATE TRIGGER trg_audit AFTER INSERT ON orders
FOR EACH ROW
INSERT INTO audit_log (action, order_id, at)
VALUES ('INSERT', NEW.order_id, NOW());
```

## Q49: What is a cursor?
**A:** A cursor is a database object used to retrieve and process rows one at a time within a result set.

**Code:**
```sql
DECLARE cur CURSOR FOR SELECT emp_id FROM employees;
OPEN cur;
FETCH NEXT FROM cur;      -- process rows one at a time...
CLOSE cur;
```

## Q50: What is a constraint?
**A:** Constraints enforce rules on data: NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK, DEFAULT.

**Code:**
```sql
CREATE TABLE orders (
  order_id        INT PRIMARY KEY,                    -- PRIMARY KEY
  cust_id         INT NOT NULL,                       -- NOT NULL
  order_reference VARCHAR(20) UNIQUE,                 -- UNIQUE
  status          VARCHAR(10) DEFAULT 'PENDING',      -- DEFAULT
  total           DECIMAL(10,2) CHECK (total >= 0),   -- CHECK
  FOREIGN KEY (cust_id) REFERENCES customers(customer_id)  -- FOREIGN KEY
);
```

## Q51: What is the difference between WHERE and HAVING?
**A:** WHERE filters rows before aggregation; HAVING filters groups after aggregation.

**Code:**
```sql
SELECT dept_id, COUNT(*) AS headcount
FROM employees
WHERE salary > 30000        -- rows filtered BEFORE grouping
GROUP BY dept_id
HAVING COUNT(*) > 5;        -- GROUPS filtered AFTER aggregation
```

## Q52: What are aggregate functions?
**A:** Functions that compute a single value from a set: COUNT, SUM, AVG, MIN, MAX.

**Code:**
```sql
SELECT COUNT(id)     AS num_rows,
       SUM(price)    AS total,
       AVG(price)    AS avg_price,
       MIN(price)    AS min_price,
       MAX(price)    AS max_price
FROM products;
```

## Q53: What is GROUP BY?
**A:** GROUP BY groups rows sharing a value so aggregate functions can be applied to each group.

**Code:**
```sql
SELECT dept_id, COUNT(*) AS headcount
FROM employees
GROUP BY dept_id;      -- one result row per distinct dept_id
```

## Q54: What is a subquery?
**A:** A subquery is a query nested inside another query, used to return data the outer query needs.

**Code:**
```sql
SELECT name FROM customers
WHERE customer_id IN (
  SELECT customer_id FROM orders WHERE total > 1000   -- nested query
);
```

## Q55: What is a correlated subquery?
**A:** A subquery that references columns from the outer query and executes once per outer row.

**Code:**
```sql
SELECT e.name, e.dept_id,
       (SELECT AVG(salary) FROM employees t
        WHERE t.dept_id = e.dept_id) AS dept_avg   -- reruns per outer row
FROM employees e;
```

## Q56: Difference between subquery and join?
**A:** Subqueries are nested and often used for existence checks; joins combine datasets and are usually faster for large sets.

**Code:**
```sql
-- Subquery: existence / value check.
SELECT name FROM customers
WHERE customer_id NOT IN (SELECT DISTINCT customer_id FROM orders);

-- Join: equivalent result, combines datasets (often faster at scale).
SELECT c.name FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.customer_id IS NULL;
```

## Q57: What is a UNION?
**A:** UNION combines results of two queries and removes duplicates.

**Code:**
```sql
SELECT city FROM customers_2023
UNION
SELECT city FROM customers_2024;
-- duplicate cities appear only once
```

## Q58: What is UNION ALL?
**A:** UNION ALL combines results including duplicates and is faster than UNION.

**Code:**
```sql
SELECT city FROM customers_2023
UNION ALL
SELECT city FROM customers_2024;
-- no dedup + no sort => faster, but duplicates are kept
```

## Q59: What is a schema?
**A:** A schema is the logical structure or blueprint of a database: tables, views, indexes, and relationships.

**Code:**
```sql
CREATE SCHEMA sales;                    -- namespace / blueprint
CREATE TABLE sales.orders (
  order_id INT PRIMARY KEY,
  amount   DECIMAL(10,2)
);
CREATE INDEX idx_orders_amount ON sales.orders (amount);

SELECT * FROM sales.orders;
```

## Q60: What is a data dictionary?
**A:** A data dictionary (system catalog) stores metadata about the database structure.

**Code:**
```sql
-- The system catalog / data dictionary stores metadata about objects.
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'orders';
```

## Q61: What is concurrency control?
**A:** Techniques to manage simultaneous transactions so they do not conflict, preserving consistency.

**Code:**
```sql
-- Locking is one concurrency-control technique: Session A locks the row.
BEGIN;
  SELECT * FROM accounts WHERE account_id = 1 FOR UPDATE;   -- lock acquired
  UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
COMMIT;   -- lock released; Session B, which was waiting, may now proceed
```

## Q62: What is a lock?
**A:** A lock restricts access to data by a transaction to prevent conflicts during concurrent operations.

**Code:**
```sql
-- Session A acquires an exclusive row lock:
BEGIN;
  SELECT * FROM accounts WHERE account_id = 1 FOR UPDATE;

-- Session B: this statement BLOCKS until A commits or rolls back.
  UPDATE accounts SET balance = 0 WHERE account_id = 1;

COMMIT;   -- A releases the lock; B's update now proceeds
```

## Q63: What is a shared lock?
**A:** A shared lock allows multiple transactions to read but not modify the data.

**Code:**
```sql
-- Session A                           Session B
BEGIN;                                 BEGIN;
LOCK TABLE accounts IN SHARE MODE;     LOCK TABLE accounts IN SHARE MODE;  -- ok
SELECT * FROM accounts;                SELECT * FROM accounts;             -- ok

-- Neither can grab an EXCLUSIVE lock while shared locks are held:
LOCK TABLE accounts IN EXCLUSIVE MODE; -- BLOCKS until the shared locks go away
COMMIT;                                COMMIT;
```

## Q64: What is an exclusive lock?
**A:** An exclusive lock allows a transaction to read and write; no other transaction can lock it.

**Code:**
```sql
-- Session A
BEGIN;
LOCK TABLE accounts IN ACCESS EXCLUSIVE MODE;   -- only A may touch it
UPDATE accounts SET balance = 0;                -- both read AND write allowed

-- Session B
INSERT INTO accounts VALUES (2, 50);            -- BLOCKS until A commits
-- Session A
COMMIT;                                         -- B proceeds now
```

## Q65: What is deadlock?
**A:** A deadlock occurs when two or more transactions wait indefinitely for each other to release locks.

**Code:**
```sql
-- Session A                        Session B
BEGIN;                              BEGIN;
UPDATE accounts SET balance=0       UPDATE accounts SET balance=0
 WHERE id=1;                         WHERE id=2;
UPDATE accounts SET balance=0       UPDATE accounts SET balance=0
 WHERE id=2;        -- waits on B     WHERE id=1;        -- waits on A
-- both wait forever => deadlock, reported as an error by the DBMS
```

## Q66: How are deadlocks resolved?
**A:** Databases use detection (wait-for graph) and resolution by aborting or rolling back a transaction (victim selection).

**Code:**
```sql
-- The DBMS builds a wait-for graph, finds a cycle, and aborts a victim.
-- Session A (victim)                  Session B (winner)
UPDATE t SET x=1 WHERE id=1;           UPDATE t SET x=2 WHERE id=2;
UPDATE t SET x=1 WHERE id=2;           UPDATE t SET x=2 WHERE id=1;
-- ERROR: deadlock detected           -- continues and COMMITs
-- A is rolled back (must be retried)
```

## Q67: What is a deadlock prevention method?
**A:** Use consistent lock ordering, wait-die or wound-wait schemes, or acquire all locks upfront.

**Code:**
```sql
-- Consistent lock ordering: both transactions lock rows in the SAME order
-- (id=1 then id=2), so no circular wait can form.
-- Session A                       Session B
BEGIN;                             BEGIN;
UPDATE t SET x=1 WHERE id=1;       UPDATE t SET x=9 WHERE id=1;  -- same first lock
UPDATE t SET x=1 WHERE id=2;       UPDATE t SET x=9 WHERE id=2;  -- same second
COMMIT;                            COMMIT;
-- alternatively: acquire all locks upfront, e.g. LOCK TABLE t;
```

## Q68: What is two-phase locking (2PL)?
**A:** A concurrency protocol: growing phase (acquire locks) then shrinking phase (release locks); guarantees serializability.

**Code:**
```sql
-- 1) Growing phase: acquire all needed locks without releasing any.
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;  -- lock A
UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;  -- lock B

-- 2) Shrinking phase: release locks, all at once at COMMIT.
COMMIT;   -- serializable execution
```

## Q69: What is a dirty read?
**A:** A dirty read occurs when a transaction reads uncommitted data from another transaction that may roll back.

**Code:**
```sql
-- Session A (uncommitted)      Session B (READ UNCOMMITTED)
BEGIN;
UPDATE accounts SET balance=900 WHERE id=1;
                                SELECT balance FROM accounts WHERE id=1;
                                -- returns 900: data A hasn't committed
ROLLBACK;                       -- the 900 never existed (dirty read!)
```

## Q70: What is a lost update?
**A:** A lost update happens when two transactions read and write the same data, and one update is overwritten.

**Code:**
```sql
-- Session A            Session B
BEGIN;                  BEGIN;
SELECT bal FROM acc     SELECT bal FROM acc
 WHERE id=1;   -- 100    WHERE id=1;   -- 100  (both read 100)
UPDATE acc SET bal=90   UPDATE acc SET bal=120
 WHERE id=1;             WHERE id=1;
COMMIT;                 COMMIT;
-- B's write overwrites A's: final 120, A's update is LOST
```

## Q71: What is a phantom read?
**A:** A phantom read occurs when a transaction re-executes a query and finds new rows inserted by another transaction.

**Code:**
```sql
-- Session A (REPEATABLE READ)          Session B
BEGIN;
SELECT COUNT(*) FROM emp
 WHERE sal > 5000;   -- returns 2
                                        INSERT INTO emp VALUES (3, 6000);
                                        COMMIT;
SELECT COUNT(*) FROM emp
 WHERE sal > 5000;   -- returns 3: a "phantom" row appeared
```

## Q72: What is a non-repeatable read?
**A:** A non-repeatable read happens when a transaction reads the same row twice and gets different values due to another transaction's update.

**Code:**
```sql
-- Session A (READ COMMITTED)           Session B
BEGIN;
SELECT name FROM emp WHERE id=1;        -- 'Alice'
                                        UPDATE emp SET name='Bob' WHERE id=1;
                                        COMMIT;
SELECT name FROM emp WHERE id=1;        -- 'Bob': same row, new value
```

## Q73: What are transaction isolation levels?
**A:** READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE — controlling anomalies.

**Code:**
```sql
-- SQL Standard (from weakest to strongest):
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;   -- allows dirty / non-repeatable / phantom
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;     -- stops dirty reads
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;    -- stops non-repeatable reads
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;       -- stops all anomalies

-- (Per-database syntax may vary, e.g. MySQL: SET SESSION TRANSACTION ISOLATION LEVEL...)
```

## Q74: What does READ COMMITTED prevent?
**A:** Prevents dirty reads but allows non-repeatable and phantom reads.

**Code:**
```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN;

SELECT balance FROM accounts WHERE id=1;   -- sees only committed data (no dirty read)

-- But a later rerun can still differ if another session commits:
-- Session B: UPDATE accounts SET balance=77 WHERE id=1; COMMIT;
SELECT balance FROM accounts WHERE id=1;   -- may now be 77 (non-repeatable)
```

## Q75: What does SERIALIZABLE guarantee?
**A:** The highest isolation; transactions behave as if executed serially, preventing all anomalies.

**Code:**
```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;

-- Range reads get locks that block concurrent inserts/updates,
-- so reads are repeatable and no phantom rows can appear:
SELECT COUNT(*) FROM emp WHERE sal > 5000;   -- 2
-- Session B: INSERT ... (sal 6000);  -> BLOCKS until A commits
SELECT COUNT(*) FROM emp WHERE sal > 5000;   -- still 2
COMMIT;
```

## Q76: What is a database anomaly?
**A:** Anomalies are problems in data (insertion, update, deletion) caused by poor design or redundancy.

**Code:**
```sql
-- Bad design with redundancy (composite PK reused across rows):
CREATE TABLE bad (dept VARCHAR(20), emp VARCHAR(20), project VARCHAR(20),
                  PRIMARY KEY (dept, emp, project));
INSERT INTO bad VALUES ('IT','Alice','Alpha'), ('IT','Alice','Beta');

-- UPDATE anomaly: moving Alice to HR must touch BOTH rows.
UPDATE bad SET dept='HR' WHERE emp='Alice';    -- easy to miss one

-- DELETE anomaly: deleting Alice's last project deletes Alice's info too.
DELETE FROM bad WHERE emp='Alice';             -- employee record vanishes

-- INSERT anomaly: can't add a new employee or project until both are filled.
```

## Q77: What is functional dependency?
**A:** A functional dependency X to Y means the value of X uniquely determines Y.

**Code:**
```sql
-- emp_id -> emp_name: one emp_id always maps to a single emp_name.
CREATE TABLE emp (
  emp_id   INT PRIMARY KEY,
  emp_name VARCHAR(50) NOT NULL      -- functionally determined by emp_id
);

-- Verify the dependency holds: no id may map to >1 distinct name.
SELECT emp_id, COUNT(DISTINCT emp_name)
FROM emp
GROUP BY emp_id
HAVING COUNT(DISTINCT emp_name) > 1;   -- empty result => dependency holds
```

## Q78: What is a candidate key in normalization?
**A:** A minimal set of attributes that can uniquely identify a tuple and has no proper subset with that property.

**Code:**
```sql
-- {student_id, course_id} uniquely identifies a grade row, and neither
-- column alone does -> a minimal candidate key (chosen here as the PK).
CREATE TABLE enrollment (
  student_id INT NOT NULL,
  course_id  INT NOT NULL,
  grade      CHAR(1),
  PRIMARY KEY (student_id, course_id)   -- candidate key -> PK
);
```

## Q79: What is referential integrity?
**A:** A rule ensuring foreign key values match a primary key value in the referenced table or are NULL.

**Code:**
```sql
CREATE TABLE customers (customer_id INT PRIMARY KEY, name VARCHAR(50));
CREATE TABLE orders (
  order_id   INT PRIMARY KEY,
  customer_id INT,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

INSERT INTO orders VALUES (1, 99);             -- ERROR: no customer 99
DELETE FROM customers WHERE customer_id = 1;   -- ERROR: orders still reference it
```

## Q80: What is a checkpoint in databases?
**A:** A checkpoint is a point where all dirty pages are written to disk, shortening recovery time.

**Code:**
```sql
-- Postgres / SQLite: force dirty (changed) buffers to disk now, so crash
-- recovery only has to replay the log since this point.
CHECKPOINT;

-- MySQL alternative:
ALTER SYSTEM CHECKPOINT;
```

## Q81: What is a log file?
**A:** A log records all transaction operations for recovery and rollback purposes.

**Code:**
```sql
-- Every change is written to the log as it happens.
BEGIN;
UPDATE accounts SET balance = 100 WHERE id = 1;   -- log entry: UPDATE (redo/undo)

-- Crash recovery replays the committed entries:
COMMIT;   -- "COMMIT" entry marks the transaction as durable / redoable
```

## Q82: What is write-ahead logging (WAL)?
**A:** WAL ensures changes are written to the log before they are written to the database, enabling recovery.

**Code:**
```sql
-- SQLite: turn on WAL mode — writers append to a -wal file first.
PRAGMA journal_mode = WAL;      -- returns 'wal'
PRAGMA synchronous = NORMAL;    -- safe with WAL

BEGIN;
UPDATE accounts SET balance = 10 WHERE id = 1;   -- written to the WAL first
COMMIT;                                          -- then flushed to the main DB
```

## Q83: What is a backup?
**A:** A copy of the database saved to restore data in case of failure or loss.

**Code:**
```bash
# PostgreSQL — logical backup & restore:
pg_dump mydb > backup.sql          # save a copy
psql mydb < backup.sql             # restore it later

# MySQL equivalent:
mysqldump -u root mydb > backup.sql
```

## Q84: What is a full backup?
**A:** A complete copy of the entire database at a point in time.

**Code:**
```bash
# PostgreSQL — full, complete snapshot in one file:
pg_dump -Fc mydb > full_2026-09-19.dump

# Restore it later:
pg_restore -d mydb full_2026-09-19.dump
```

## Q85: What is an incremental backup?
**A:** A backup of only the data changed since the last backup.

**Code:**
```bash
# Postgres point-in-time recovery = full base + replayed WAL segments:
# 1) one-time base backup:
pg_basebackup -Ft -z -D /backups/full_base

# 2) postgresql.conf: archive every new WAL segment since that backup
archive_command = 'cp %p /wal_archive/%f'

# restore = base backup + replay/apply the archived WAL segments after it
```

## Q86: What is database replication?
**A:** Replication copies and maintains database data across multiple servers for availability and load distribution.

**Code:**
```bash
# PostgreSQL logical replication: publisher -> subscriber
# publisher (postgresql.conf):
wal_level = logical

# publisher:
CREATE PUBLICATION pub_orders FOR TABLE orders;
# subscriber:
CREATE SUBSCRIPTION sub_orders
CONNECTION 'host=publisher dbname=mydb'
PUBLICATION pub_orders;
```

## Q87: What is master-slave replication?
**A:** One master handles writes; slaves replicate and handle reads.

**Code:**
```bash
# Slave points at the master and stays current via streaming replication.
# standby.signal + postgresql.conf on the slave:
primary_conninfo = 'host=master port=5432 user=repl dbname=mydb'

# Route reads to the slave, writes go to the master:
psql -h slave  -c "SELECT COUNT(*) FROM orders;"   # read
psql -h master -c "INSERT INTO orders ...;"        # write

# On master failure the slave is promoted:
pg_ctl promote -D /var/lib/postgresql/data
```

## Q88: What is sharding?
**A:** Sharding horizontally partitions data across multiple databases or servers based on a shard key.

**Code:**
```sql
-- A shard key decides which shard owns a row — here hashed by user_id.
SELECT user_id,
       CASE MOD(user_id, 4)
         WHEN 0 THEN 'shard_a'
         WHEN 1 THEN 'shard_b'
         WHEN 2 THEN 'shard_c'
         ELSE        'shard_d'
       END AS shard
FROM users;
-- every query routes by user_id so each shard holds the same subset of rows
```

## Q89: What is partitioning?
**A:** Partitioning divides a table into smaller pieces (by range, list, hash) within the same database.

**Code:**
```sql
-- Range partitioning: one partition per year, still "one" logical table.
CREATE TABLE sales (
  sale_date DATE NOT NULL,
  amount    DECIMAL(10,2)
) PARTITION BY RANGE (sale_date);

CREATE TABLE sales_2024 PARTITION OF sales
  FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
CREATE TABLE sales_2025 PARTITION OF sales
  FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

-- The planner prunes to just the right partition.
SELECT * FROM sales WHERE sale_date = '2025-06-01';
```

## Q90: What is a NoSQL database?
**A:** NoSQL databases store non-relational data (document, key-value, columnar, graph) and scale horizontally.

**Code:**
```bash
# Document store (MongoDB): no fixed schema, JSON documents, embedded data.
mongosh db.testdb <<'EOF'
db.users.insertOne({
  _id: 1,
  name: "Aayush",
  email: "a@b.com",
  address: { city: "Mumbai" },          # nested/embedded document
  orders: [101, 102]                    # embedded array, denormalized
})
db.users.findOne({ name: "Aayush" })
EOF
```

## Q91: Difference between SQL and NoSQL?
**A:** SQL is relational, schema-based, ACID; NoSQL is flexible-schema, distributed, often BASE.

**Code:**
```bash
# Relational (SQL): rigid schema + relations + ACID.
psql mydb -c "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(50));"
psql mydb -c "INSERT INTO users VALUES (1, 'Aayush');"

# NoSQL (MongoDB): flexible schema, embedded documents, horizontal scale.
mongosh mydb --eval "db.users.insertOne({ name: 'Aayush', city: 'Mumbai' })"
# no table defined ahead of time — any field is accepted
```

## Q92: What is CAP theorem?
**A:** In distributed systems, you can have only two of Consistency, Availability, and Partition tolerance.

**Code:**
```python
# Under a partition the two nodes cannot talk — choose one guarantee.

def replica_under_partition(data, accept_local_write, can_replicate):
    if can_replicate:                      # both sides stay in sync
        data["B"] = data["A"] = "synced"
        return "C + A (no partition: choose any two)"
    if accept_local_write:
        data["A"] = "new"                  # B stays stale underneath
        return "AP: available, eventual consistency"
    return "CP: write refused, all copies stay consistent"

replicas = {"A": "old", "B": "old"}
print(replica_under_partition(replicas, accept_local_write=True, can_replicate=False))
```

## Q93: What is BASE?
**A:** BASE (Basically Available, Soft state, Eventual consistency) is the consistency model for many NoSQL systems.

**Code:**
```python
# Eventual consistency: a read replica may briefly lag, then converge.
primary   = {"balance": 50}          # primary already updated
replica   = {"balance": 100}         # propagation not complete yet

print("read from replica:", replica["balance"])    # 100 (stale — Basic Availability/Soft state)

replica = {"balance": 50}                           # replication catches up
print("read from replica:", replica["balance"])     # 50  (Eventual consistency)
```

## Q94: What is a query optimizer?
**A:** A component that determines the most efficient execution plan for a SQL query.

**Code:**
```sql
-- Before the index, the optimizer can only full-scan:
EXPLAIN SELECT * FROM users WHERE email = 'a@b.com';   -- Seq Scan

CREATE INDEX idx_users_email ON users (email);

-- Now the optimizer picks the cheaper plan:
EXPLAIN SELECT * FROM users WHERE email = 'a@b.com';   -- Index Scan
```

## Q95: What is a query execution plan?
**A:** A step-by-step strategy the DBMS uses to execute a query, showing operations like scans and joins.

**Code:**
```sql
EXPLAIN ANALYZE
SELECT c.name, SUM(o.amount)
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.placed_at > '2026-01-01'
GROUP BY c.name;

-- output lists each step (Index/Seq Scan -> Hash Join -> Hash Aggregate)
-- with actual row counts and timings, e.g.:
--   Hash Join (actual time=0.5..3.2 rows=400)
--   HashAggregate (actual time=4.1..4.5 rows=120)
```

## Q96: What is cardinality in SQL?
**A:** Cardinality refers to the number of distinct rows or the relationship count (one-to-one, one-to-many).

**Code:**
```sql
-- One-to-many cardinality: one customer -> many orders.
SELECT c.customer_id, COUNT(o.order_id) AS num_orders
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id;

-- Column cardinality used by the optimizer for its estimates:
SELECT COUNT(DISTINCT status) AS distinct_statuses, COUNT(*) AS total_rows
FROM orders;
```

## Q97: What is a clustered versus heap table?
**A:** A clustered table orders data by the clustered index; a heap has no clustering, data stored unordered.

**Code:**
```sql
-- SQL Server: CLUSTERED index physically orders the rows.
CREATE TABLE users (
  user_id INT PRIMARY KEY CLUSTERED     -- rows stored in user_id order
);

-- A heap has no clustered index; rows live in unordered pages.
CREATE TABLE audit_log (
  id      INT PRIMARY KEY NONCLUSTERED,  -- keeps it a heap
  message VARCHAR(100)
);
```

## Q98: What is a NULL value?
**A:** NULL represents missing or unknown data, not zero or empty string.

**Code:**
```sql
INSERT INTO t (id, col) VALUES (1, NULL);   -- unknown/missing, not 0 or ''

SELECT * FROM t WHERE col = NULL;     -- returns NO rows: NULL = unknown
SELECT * FROM t WHERE col IS NULL;    -- correct way to test for NULL
SELECT * FROM t WHERE col IS NOT NULL;
SELECT COALESCE(col, 'n/a') FROM t;   -- replace NULL with a default
```

## Q99: What is the difference between CHAR and VARCHAR?
**A:** CHAR is fixed-length (padded); VARCHAR is variable-length, storing only used space.

**Code:**
```sql
CREATE TABLE t (c CHAR(5) NOT NULL, v VARCHAR(5) NOT NULL);
INSERT INTO t VALUES ('a', 'b');

SELECT LENGTH(c) AS char_len, LENGTH(v) AS varchar_len FROM t;
--  char_len: 5  (padded)   |   varchar_len: 1 (only what was stored)
```

## Q100: What is database tuning?
**A:** Database tuning optimizes performance via indexing, query rewriting, configuration, and schema design.

**Code:**
```sql
-- 1) Index the hot query's filter + sort columns.
CREATE INDEX idx_orders_customer ON orders (customer_id, placed_at);

-- 2) Confirm the optimizer actually uses it.
EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 42 ORDER BY placed_at;

-- 3) Refresh statistics so the optimizer has accurate estimates.
ANALYZE orders;
```