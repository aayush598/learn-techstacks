# DBMS Concepts for Infosys SP DSE Interview

## Table of Contents
1. [ACID Properties](#acid-properties)
2. [Normalization](#normalization)
3. [SQL Joins](#sql-joins)
4. [Indexing](#indexing)
5. [Transactions and Isolation Levels](#transactions-and-isolation-levels)
6. [CAP Theorem](#cap-theorem)
7. [SQL Queries Practice](#sql-queries-practice)
8. [Common Interview Questions](#common-interview-questions)

---

## ACID Properties

| Property | Description | Example |
|----------|-------------|---------|
| **Atomicity** | All or nothing - transaction either completes fully or not at all | Bank transfer: both debit and credit happen, or neither |
| **Consistency** | Database moves from one valid state to another | Total balance remains same after transfer |
| **Isolation** | Concurrent transactions don't interfere with each other | Two transfers on same account don't corrupt data |
| **Durability** | Once committed, data persists even after system failure | Committed transaction survives power outage |

```sql
-- Transaction example
BEGIN TRANSACTION;

-- Debit from Account A
UPDATE accounts SET balance = balance - 500 WHERE account_id = 1;

-- Credit to Account B
UPDATE accounts SET balance = balance + 500 WHERE account_id = 2;

-- Verify total balance remains same
-- (Atomicity: if either fails, both roll back)
-- (Consistency: total balance before = total after)
-- (Isolation: other transactions see either both or neither)
-- (Durability: once committed, data is permanent)

COMMIT;
-- or ROLLBACK if something went wrong
```

---

## Normalization

### 1NF (First Normal Form)
- Each column contains atomic (indivisible) values
- No repeating groups

```sql
-- BAD (violates 1NF)
+----+------------------+
| id | courses          |
+----+------------------+
| 1  | Math, Science    |  -- Multi-valued!
| 2  | English          |
+----+------------------+

-- GOOD (1NF)
+----+---------+
| id | course  |
+----+---------+
| 1  | Math    |
| 1  | Science |
| 2  | English |
+----+---------+
```

### 2NF (Second Normal Form)
- Must be in 1NF
- No partial dependency (non-key attribute depends on entire composite primary key)

```sql
-- BAD (violates 2NF)
-- Composite PK: (student_id, course_id)
+------------+-----------+--------+------------------+
| student_id | course_id | grade  | student_name     |
+------------+-----------+--------+------------------+
| 1          | 101       | A      | Alice            |
-- student_name depends only on student_id, not course_id (partial dependency)

-- GOOD (2NF)
-- Table 1: Students
+------------+------------------+
| student_id | student_name     |
+------------+------------------+
| 1          | Alice            |

-- Table 2: Enrollments
+------------+-----------+--------+
| student_id | course_id | grade  |
+------------+-----------+--------+
| 1          | 101       | A      |
```

### 3NF (Third Normal Form)
- Must be in 2NF
- No transitive dependency (non-key attribute depends on another non-key attribute)

```sql
-- BAD (violates 3NF)
+----+------+-----------+-----------+
| id | name | dept_id   | dept_name |
+----+------+-----------+-----------+
| 1  | Alice| D001      | Engineering|
-- dept_name depends on dept_id, which depends on id (transitive dependency)

-- GOOD (3NF)
-- Table 1: Employees
+----+------+-----------+
| id | name | dept_id   |
+----+------+-----------+
| 1  | Alice| D001      |

-- Table 2: Departments
+-----------+-------------+
| dept_id   | dept_name   |
+-----------+-------------+
| D001      | Engineering |
```

### BCNF (Boyce-Codd Normal Form)
- Must be in 3NF
- For every functional dependency X → Y, X must be a superkey

```sql
-- Example: Student-Course-Professor
-- Dependency: course_id → professor_id (each course has one professor)
-- But student_id, course_id is the key

-- If professor_id is not a superkey, violates BCNF
-- Solution: Split into separate tables

CREATE TABLE course_professor (
    course_id INT PRIMARY KEY,
    professor_id INT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (professor_id) REFERENCES professors(professor_id)
);
```

### Normalization Summary

| Normal Form | Requirement | Eliminates |
|-------------|-------------|------------|
| 1NF | Atomic values | Repeating groups |
| 2NF | 1NF + no partial dependency | Partial dependencies |
| 3NF | 2NF + no transitive dependency | Transitive dependencies |
| BCNF | 3NF + every determinant is superkey | All anomalies |

---

## SQL Joins

```sql
-- Sample tables
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    dept_id INT
);

CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(100)
);

CREATE TABLE projects (
    project_id INT PRIMARY KEY,
    emp_id INT,
    project_name VARCHAR(100)
);

-- Insert sample data
INSERT INTO employees VALUES (1, 'Alice', 1), (2, 'Bob', 2), (3, 'Charlie', 1), (4, 'Diana', NULL);
INSERT INTO departments VALUES (1, 'Engineering'), (2, 'Marketing'), (3, 'Sales');
INSERT INTO projects VALUES (101, 1, 'ProjectA'), (102, 2, 'ProjectB'), (103, 5, 'ProjectC');
```

### INNER JOIN
Returns only matching rows from both tables.

```sql
SELECT e.name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id;

-- Result:
-- Alice | Engineering
-- Bob   | Marketing
-- Charlie | Engineering
-- (Diana excluded - no matching dept)
-- (Sales excluded - no matching employee)
```

### LEFT JOIN (LEFT OUTER JOIN)
All rows from left table + matching from right.

```sql
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id;

-- Result:
-- Alice   | Engineering
-- Bob     | Marketing
-- Charlie | Engineering
-- Diana   | NULL  (no matching dept)
```

### RIGHT JOIN (RIGHT OUTER JOIN)
All rows from right table + matching from left.

```sql
SELECT e.name, d.dept_name
FROM employees e
RIGHT JOIN departments d ON e.dept_id = d.dept_id;

-- Result:
-- Alice   | Engineering
-- Bob     | Marketing
-- Charlie | Engineering
-- NULL    | Sales  (no matching employee)
```

### FULL JOIN (FULL OUTER JOIN)
All rows from both tables, NULL where no match.

```sql
-- Note: MySQL doesn't support FULL JOIN directly
-- Use UNION of LEFT and RIGHT joins
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id
UNION
SELECT e.name, d.dept_name
FROM employees e
RIGHT JOIN departments d ON e.dept_id = d.dept_id;

-- Result:
-- Alice   | Engineering
-- Bob     | Marketing
-- Charlie | Engineering
-- Diana   | NULL
-- NULL    | Sales
```

### CROSS JOIN
Cartesian product - every row from left paired with every row from right.

```sql
SELECT e.name, d.dept_name
FROM employees e
CROSS JOIN departments d;

-- Result: 4 employees × 3 departments = 12 rows
-- Alice | Engineering, Alice | Marketing, Alice | Sales
-- Bob   | Engineering, Bob   | Marketing, Bob   | Sales
-- ...
```

### SELF JOIN
Table joined with itself.

```sql
-- Find employees and their managers
CREATE TABLE emp_with_mgr (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    manager_id INT
);

INSERT INTO emp_with_mgr VALUES
(1, 'Alice', NULL),
(2, 'Bob', 1),
(3, 'Charlie', 1),
(4, 'Diana', 2);

SELECT e.name AS employee, m.name AS manager
FROM emp_with_mgr e
LEFT JOIN emp_with_mgr m ON e.manager_id = m.id;

-- Result:
-- Alice   | NULL   (no manager)
-- Bob     | Alice
-- Charlie | Alice
-- Diana   | Bob
```

---

## Indexing

### B-Tree Index
Most common index type. Maintains sorted order, allows range queries.

```sql
-- Create index
CREATE INDEX idx_emp_name ON employees(name);

-- Composite index
CREATE INDEX idx_emp_dept ON employees(dept_id, name);

-- Clustered index (one per table, determines physical order)
CREATE CLUSTERED INDEX idx_emp_id ON employees(id);
```

### Hash Index
Good for exact match queries, not for range queries.

```sql
-- PostgreSQL syntax
CREATE INDEX idx_emp_id_hash ON employees USING hash(id);

-- Good for: WHERE id = 5
-- Bad for: WHERE id > 5
```

### When to Use Indexes
```sql
-- Use indexes for:
-- 1. WHERE clause columns
-- 2. JOIN columns
-- 3. ORDER BY columns
-- 4. Columns with high cardinality (many unique values)

-- Avoid indexes for:
-- 1. Small tables
-- 2. Columns with low cardinality (few unique values)
-- 3. Frequently updated columns
-- 4. Tables with heavy INSERT/UPDATE/DELETE
```

### Index Query Analysis
```sql
-- Check query execution plan
EXPLAIN SELECT * FROM employees WHERE name = 'Alice';

-- Key things to look for:
-- "Using index" = covering index (good)
-- "Using filesort" = no index used (bad)
-- "Using temporary" = temporary table created (often bad)
```

---

## Transactions and Isolation Levels

### ACID Recap
```sql
BEGIN TRANSACTION;
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

### Isolation Levels

| Level | Dirty Read | Non-Repeatable Read | Phantom Read |
|-------|-----------|-------------------|--------------|
| READ UNCOMMITTED | Yes | Yes | Yes |
| READ COMMITTED | No | Yes | Yes |
| REPEATABLE READ | No | No | Yes |
| SERIALIZABLE | No | No | No |

```sql
-- Set isolation level
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Or per session
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- MySQL InnoDB default: REPEATABLE READ
-- PostgreSQL default: READ COMMITTED
```

### Problems Explained

```sql
-- DIRTY READ: Reading uncommitted data
-- Transaction A: UPDATE balance = 900 (not committed)
-- Transaction B: SELECT balance → reads 900
-- Transaction A: ROLLBACK (balance is actually 1000)
-- Transaction B has wrong data!

-- NON-REPEATABLE READ: Same query, different results
-- Transaction A: SELECT balance → 1000
-- Transaction B: UPDATE balance = 900, COMMIT
-- Transaction A: SELECT balance → 900 (different!)

-- PHANTOM READ: New rows appear
-- Transaction A: SELECT COUNT(*) WHERE age > 25 → 5
-- Transaction B: INSERT new employee (age 30), COMMIT
-- Transaction A: SELECT COUNT(*) WHERE age > 25 → 6 (phantom!)
```

---

## CAP Theorem

For a distributed system, you can only guarantee 2 of 3:

```
        Consistency
           /\
          /  \
         /    \
        /  CA  \
       /________\
      /    CP    \
     /            \
    /______________\
   AP              BP

C: Consistency - Every read receives the most recent write
A: Availability - Every request receives a response
P: Partition Tolerance - System continues despite network failures

Real-world systems:
- CA: Traditional RDBMS (MySQL, PostgreSQL) - no partition tolerance
- CP: MongoDB, Redis, HBase - sacrifice availability
- AP: Cassandra, DynamoDB - sacrifice consistency
```

---

## SQL Queries Practice

### Q1: Find Second Highest Salary

```sql
-- Method 1: Using LIMIT/OFFSET
SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 1;

-- Method 2: Using subquery
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- Method 3: Using DENSE_RANK
SELECT salary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rank
    FROM employees
) ranked
WHERE rank = 2;

-- Method 4: Using NOT IN
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary NOT IN (SELECT MAX(salary) FROM employees);
```

### Q2: Find Employees with No Manager

```sql
-- Using LEFT JOIN
SELECT e.name AS employee
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id
WHERE m.id IS NULL;

-- Using NOT EXISTS
SELECT e.name
FROM employees e
WHERE NOT EXISTS (
    SELECT 1 FROM employees m WHERE m.id = e.manager_id
);

-- Using NOT IN (careful with NULLs)
SELECT name
FROM employees
WHERE manager_id NOT IN (SELECT id FROM employees);
```

### Q3: Rank Employees by Salary

```sql
-- Using ROW_NUMBER (unique ranks, no ties)
SELECT name, salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num
FROM employees;

-- Using RANK (ties get same rank, gaps in ranking)
SELECT name, salary,
    RANK() OVER (ORDER BY salary DESC) AS rank
FROM employees;

-- Using DENSE_RANK (ties get same rank, no gaps)
SELECT name, salary,
    DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank
FROM employees;

-- Example:
-- salary: 1000, 1000, 900, 800
-- ROW_NUMBER: 1, 2, 3, 4
-- RANK:       1, 1, 3, 4  (gap after tie)
-- DENSE_RANK: 1, 1, 2, 3  (no gap)

-- Rank within each department
SELECT name, dept_id, salary,
    RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dept_rank
FROM employees;
```

### Q4: Find Duplicate Records

```sql
-- Find duplicate names
SELECT name, COUNT(*) AS count
FROM employees
GROUP BY name
HAVING COUNT(*) > 1;

-- Find all duplicate rows (including all columns)
SELECT *
FROM employees
WHERE name IN (
    SELECT name
    FROM employees
    GROUP BY name
    HAVING COUNT(*) > 1
);

-- Find duplicates with specific columns
SELECT name, dept_id, COUNT(*) AS count
FROM employees
GROUP BY name, dept_id
HAVING COUNT(*) > 1;
```

### Q5: Delete Duplicate Rows

```sql
-- Keep one copy, delete rest (MySQL)
DELETE FROM employees
WHERE id NOT IN (
    SELECT min_id FROM (
        SELECT MIN(id) AS min_id
        FROM employees
        GROUP BY name, dept_id
    ) AS keepers
);

-- Using ROW_NUMBER (MySQL 8.0+)
DELETE FROM employees
WHERE id IN (
    SELECT id FROM (
        SELECT id,
            ROW_NUMBER() OVER (PARTITION BY name, dept_id ORDER BY id) AS rn
        FROM employees
        ) ranked
    WHERE rn > 1
);

-- PostgreSQL: Using CTE
WITH cte AS (
    SELECT ctid,
        ROW_NUMBER() OVER (PARTITION BY name, dept_id ORDER BY ctid) AS rn
    FROM employees
)
DELETE FROM employees
WHERE ctid IN (SELECT ctid FROM cte WHERE rn > 1);
```

### Q6: Find Department with Maximum Employees

```sql
SELECT dept_id, COUNT(*) AS emp_count
FROM employees
GROUP BY dept_id
ORDER BY emp_count DESC
LIMIT 1;

-- Alternative with subquery
SELECT dept_id, COUNT(*) AS emp_count
FROM employees
GROUP BY dept_id
HAVING COUNT(*) = (
    SELECT MAX(cnt) FROM (
        SELECT COUNT(*) AS cnt
        FROM employees
        GROUP BY dept_id
    ) AS dept_counts
);
```

### Q7: Find Employees Who Earn More Than Their Manager

```sql
SELECT e.name AS employee, e.salary AS emp_salary,
       m.name AS manager, m.salary AS mgr_salary
FROM employees e
JOIN employees m ON e.manager_id = m.id
WHERE e.salary > m.salary;
```

### Q8: Year-over-Year Growth

```sql
WITH monthly_sales AS (
    SELECT
        YEAR(order_date) AS year,
        MONTH(order_date) AS month,
        SUM(amount) AS total_sales
    FROM orders
    GROUP BY YEAR(order_date), MONTH(order_date)
)
SELECT
    year,
    month,
    total_sales,
    LAG(total_sales) OVER (ORDER BY year, month) AS prev_month_sales,
    ROUND(
        (total_sales - LAG(total_sales) OVER (ORDER BY year, month))
        / LAG(total_sales) OVER (ORDER BY year, month) * 100, 2
    ) AS growth_pct
FROM monthly_sales;
```

---

## Common Interview Questions

### Q1: What is the difference between WHERE and HAVING?

```sql
-- WHERE: Filters rows before GROUP BY
-- HAVING: Filters groups after GROUP BY

-- WHERE example
SELECT dept_id, COUNT(*) AS count
FROM employees
WHERE salary > 5000  -- Filter individual rows first
GROUP BY dept_id;

-- HAVING example
SELECT dept_id, COUNT(*) AS count
FROM employees
GROUP BY dept_id
HAVING COUNT(*) > 3;  -- Filter groups after aggregation
```

### Q2: Difference between DELETE, TRUNCATE, and DROP?

| Feature | DELETE | TRUNCATE | DROP |
|---------|--------|----------|------|
| Type | DML | DDL | DDL |
| WHERE clause | Yes | No | No |
| Rollback | Yes | No (usually) | No |
| Speed | Slow | Fast | Fastest |
| Identity reset | No | Yes | N/A |
| Triggers | Yes | No | No |

```sql
DELETE FROM employees WHERE id = 1;    -- Delete specific rows
DELETE FROM employees;                  -- Delete all rows (slow)

TRUNCATE TABLE employees;              -- Delete all rows (fast, reset identity)

DROP TABLE employees;                  -- Remove table entirely
```

### Q3: What is a View?

```sql
-- Virtual table based on query result
CREATE VIEW high_earners AS
SELECT name, salary, dept_id
FROM employees
WHERE salary > 8000;

-- Use like a regular table
SELECT * FROM high_earners;

-- Benefits:
-- 1. Simplify complex queries
-- 2. Security (hide columns/rows)
-- 3. Data independence

-- Materialized View (actual data stored)
CREATE MATERIALIZED VIEW dept_stats AS
SELECT dept_id, COUNT(*) AS emp_count, AVG(salary) AS avg_salary
FROM employees
GROUP BY dept_id;

-- Refresh when needed
REFRESH MATERIALIZED VIEW dept_stats;
```

### Q4: What is a Stored Procedure?

```sql
-- Reusable SQL code block
DELIMITER //
CREATE PROCEDURE GetEmployeesByDept(IN dept INT)
BEGIN
    SELECT name, salary
    FROM employees
    WHERE dept_id = dept
    ORDER BY salary DESC;
END //
DELIMITER ;

-- Call the procedure
CALL GetEmployeesByDept(1);

-- With output parameter
DELIMITER //
CREATE PROCEDURE GetDeptStats(
    IN dept INT,
    OUT emp_count INT,
    OUT avg_salary DECIMAL
)
BEGIN
    SELECT COUNT(*), AVG(salary)
    INTO emp_count, avg_salary
    FROM employees
    WHERE dept_id = dept;
END //
DELIMITER ;

-- Call with output
CALL GetDeptStats(1, @count, @avg);
SELECT @count, @avg;
```

### Q5: What is a Trigger?

```sql
-- Automatically execute code on certain events
CREATE TRIGGER before_employee_insert
BEFORE INSERT ON employees
FOR EACH ROW
BEGIN
    SET NEW.created_at = NOW();
    IF NEW.salary < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Salary cannot be negative';
    END IF;
END;

-- Audit trigger
CREATE TRIGGER after_employee_update
AFTER UPDATE ON employees
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (emp_id, old_salary, new_salary, changed_at)
    VALUES (OLD.id, OLD.salary, NEW.salary, NOW());
END;
```

### Q6: Window Functions vs Aggregate Functions

```sql
-- Aggregate: Groups rows, returns one row per group
SELECT dept_id, AVG(salary) AS avg_salary
FROM employees
GROUP BY dept_id;
-- Returns: dept_id, avg_salary (one row per dept)

-- Window: Preserves rows, adds calculation
SELECT name, dept_id, salary,
    AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg
FROM employees;
-- Returns: all original rows + dept_avg column

-- Common window functions:
-- ROW_NUMBER() - sequential number
-- RANK() - rank with gaps
-- DENSE_RANK() - rank without gaps
-- LAG(col, n) - value n rows before
-- LEAD(col, n) - value n rows after
-- SUM() OVER - running total
-- NTILE(n) - divide into n groups
```

### Q7: How to optimize slow queries?

```sql
-- 1. Use EXPLAIN to analyze
EXPLAIN SELECT * FROM employees WHERE name = 'Alice';

-- 2. Add appropriate indexes
CREATE INDEX idx_emp_name ON employees(name);

-- 3. Avoid SELECT *
SELECT id, name FROM employees WHERE id = 1;

-- 4. Use LIMIT for large results
SELECT * FROM employees ORDER BY salary DESC LIMIT 10;

-- 5. Avoid functions on indexed columns
-- Bad: WHERE YEAR(hire_date) = 2024
-- Good: WHERE hire_date >= '2024-01-01' AND hire_date < '2025-01-01'

-- 6. Use JOIN instead of subqueries
-- Often faster, optimizer can choose better plan

-- 7. Avoid LIKE 'abc%'
-- Can't use index. Use FULLTEXT search instead.

-- 8. Batch inserts
INSERT INTO employees (name, salary) VALUES
('Alice', 5000),
('Bob', 6000),
('Charlie', 7000);
-- Instead of 3 separate INSERT statements
```

### Q8: What are CTEs (Common Table Expressions)?

```sql
-- Temporary named result set
WITH dept_stats AS (
    SELECT dept_id, COUNT(*) AS emp_count, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY dept_id
)
SELECT d.dept_name, ds.emp_count, ds.avg_salary
FROM departments d
JOIN dept_stats ds ON d.dept_id = ds.dept_id
WHERE ds.avg_salary > 7000;

-- Recursive CTE (for hierarchical data)
WITH RECURSIVE org_chart AS (
    -- Base case: top-level manager
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case: employees under managers
    SELECT e.id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT * FROM org_chart ORDER BY level, name;
```

---

## Quick Reference Cheat Sheet

| Topic | Key Points |
|-------|-----------|
| ACID | Atomicity, Consistency, Isolation, Durability |
| 1NF | Atomic values, no repeating groups |
| 2NF | 1NF + no partial dependency |
| 3NF | 2NF + no transitive dependency |
| BCNF | 3NF + every determinant is superkey |
| INNER JOIN | Only matching rows |
| LEFT JOIN | All from left + matching from right |
| RIGHT JOIN | All from right + matching from left |
| FULL JOIN | All from both tables |
| CROSS JOIN | Cartesian product |
| SELF JOIN | Table joined with itself |
| B-Tree Index | Sorted, supports range queries |
| Hash Index | Exact match only, fast |
| Isolation Levels | READ UNCOMMITTED → READ COMMITTED → REPEATABLE READ → SERIALIZABLE |
| CAP | Consistency, Availability, Partition Tolerance (pick 2) |
| DELETE | DML, can rollback, triggers |
| TRUNCATE | DDL, fast, reset identity |
| DROP | DDL, remove table entirely |
