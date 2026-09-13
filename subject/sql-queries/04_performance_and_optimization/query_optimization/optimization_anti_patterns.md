# SQL Anti-Patterns and Query Rewrites — 100 SQL Interview Q&A

## Q1: Function on an Indexed Column in WHERE

**Anti-pattern:**
```sql
SELECT *
FROM employees
WHERE LOWER(last_name) = 'smith';
```
**Problem:** Wrapping the indexed column in `LOWER()` makes the index unusable; the engine must scan every row and apply the function.

**Fix:**
```sql
SELECT *
FROM employees
WHERE last_name = 'Smith';
```

**Alt1:** Add a functional index so the function-based query can still use it (PostgreSQL):
```sql
CREATE INDEX idx_employees_lower_lastname ON employees (LOWER(last_name));

SELECT *
FROM employees
WHERE LOWER(last_name) = 'smith';
```

---

## Q2: Using YEAR() on a DATE Column

**Anti-pattern:**
```sql
SELECT COUNT(*) AS cnt
FROM orders
WHERE YEAR(order_date) = 2024;
```
**Problem:** `YEAR(order_date)` is evaluated per row; the B-tree index on `order_date` is completely bypassed.

**Fix:**
```sql
SELECT COUNT(*) AS cnt
FROM orders
WHERE order_date >= '2024-01-01'
  AND order_date <  '2025-01-01';
```

---

## Q3: Using DATE() to Strip Time from a DATETIME Column

**Anti-pattern:**
```sql
SELECT *
FROM events
WHERE DATE(event_ts) = '2024-06-15';
```
**Problem:** Every row must have its timestamp cast to a date, preventing any index seek on `event_ts`.

**Fix:**
```sql
SELECT *
FROM events
WHERE event_ts >= '2024-06-15 00:00:00'
  AND event_ts <  '2024-06-16 00:00:00';
```

---

## Q4: Implicit Type Cast — VARCHAR Compared to INT

**Anti-pattern:**
```sql
SELECT *
FROM orders
WHERE order_id = '12345';
```
**Problem:** If `order_id` is `INT`, comparing to a string literal may force an implicit cast on every value in the column, defeating the index. (Behaviour varies by engine — MySQL historically casts the *column*, PostgreSQL casts the *literal*.)

**Fix:**
```sql
SELECT *
FROM orders
WHERE order_id = 12345;
```

---

## Q5: Implicit Type Cast — INT Compared to VARCHAR Column

**Anti-pattern:**
```sql
SELECT *
FROM users
WHERE phone_number = 5551234;
```
**Problem:** If `phone_number` is `VARCHAR`, the integer literal is promoted and compared against every stored string, bypassing any index on `phone_number`.

**Fix:**
```sql
SELECT *
FROM users
WHERE phone_number = '5551234';
```

---

## Q6: Leading Wildcard in LIKE

**Anti-pattern:**
```sql
SELECT *
FROM products
WHERE product_name LIKE '%widget%';
```
**Problem:** A leading `%` prevents B-tree index usage; the engine performs a full table scan.

**Fix — use a full-text index:**
```sql
ALTER TABLE products ADD FULLTEXT INDEX ft_product_name (product_name);

SELECT *
FROM products
WHERE MATCH(product_name) AGAINST('widget' IN BOOLEAN MODE);
```

**Alt1 — trigram index (PostgreSQL):**
```sql
CREATE INDEX idx_products_name_trgm ON products USING gin (product_name gin_trgm_ops);

SELECT *
FROM products
WHERE product_name LIKE '%widget%';
```

---

## Q7: SELECT * Breaks a Covering Index

**Anti-pattern:**
```sql
SELECT *
FROM orders
WHERE customer_id = 42
ORDER BY order_date DESC;
```
**Problem:** Even with an index on `(customer_id, order_date)`, selecting every column forces a lookup back to the heap for each matching row.

**Fix:**
```sql
SELECT order_id, customer_id, order_date, total
FROM orders
WHERE customer_id = 42
ORDER BY order_date DESC;
```

**Alt1:** If the query needs only indexed columns, the index alone satisfies the query (covering / index-only scan):
```sql
SELECT customer_id, order_date
FROM orders
WHERE customer_id = 42
ORDER BY order_date DESC;
```

---

## Q8: SELECT * Leaks Schema and Wastes Bandwidth

**Anti-pattern:**
```sql
SELECT *
FROM customers;
```
**Problem:** Returns every column including large text/blob fields, doubles network traffic, breaks application code when columns are added or reordered, and prevents covering-index optimisations.

**Fix:**
```sql
SELECT customer_id, first_name, last_name, email
FROM customers;
```

---

## Q9: OR Condition Prevents Single Index Usage

**Anti-pattern:**
```sql
SELECT *
FROM tickets
WHERE status = 'open' OR assignee_id = 7;
```
**Problem:** The engine cannot use one index for two different columns; it falls back to a full scan or a less-efficient index-merge.

**Fix — rewrite to UNION (each branch uses its own index):**
```sql
SELECT *
FROM tickets
WHERE status = 'open'

UNION ALL

SELECT *
FROM tickets
WHERE assignee_id = 7
  AND status <> 'open';
```

**Alt1 — IN where applicable:**
```sql
SELECT *
FROM tickets
WHERE status IN ('open', 'closed', 'pending');
```

---

## Q10: OR on the Same Column — Use IN

**Anti-pattern:**
```sql
SELECT *
FROM products
WHERE category = 'Books'
   OR category = 'Movies'
   OR category = 'Music';
```
**Problem:** Repeated column references are verbose and some optimisers handle `OR` less efficiently than `IN`.

**Fix:**
```sql
SELECT *
FROM products
WHERE category IN ('Books', 'Movies', 'Music');
```

---

## Q11: NOT IN with a Subquery That Returns NULLs

**Anti-pattern:**
```sql
SELECT *
FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM blacklist);
```
**Problem:** If `blacklist.customer_id` contains even one `NULL`, the entire `NOT IN` evaluates to UNKNOWN for every row — returning zero results silently.

**Fix:**
```sql
SELECT *
FROM customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM blacklist b
    WHERE b.customer_id = c.customer_id
);
```

---

## Q12: NOT IN vs NOT EXISTS — Performance on Large Sets

**Anti-pattern:**
```sql
SELECT *
FROM orders
WHERE customer_id NOT IN (
    SELECT customer_id FROM returns WHERE status = 'completed'
);
```
**Problem:** The subquery materialises a list that can be enormous; `NOT IN` performs a linear scan per row. NULLs also cause the silent-zero-rows bug.

**Fix:**
```sql
SELECT o.*
FROM orders o
WHERE NOT EXISTS (
    SELECT 1
    FROM returns r
    WHERE r.customer_id = o.customer_id
      AND r.status = 'completed'
);
```

---

## Q13: Non-Sargable Arithmetic in WHERE

**Anti-pattern:**
```sql
SELECT *
FROM invoices
WHERE amount * 1.1 > 1000;
```
**Problem:** Multiplying the column means every row must be computed; an index on `amount` is useless.

**Fix:**
```sql
SELECT *
FROM invoices
WHERE amount > 1000 / 1.1;
```

**Alt1:** Pre-compute the constant:
```sql
SELECT *
FROM invoices
WHERE amount > 909.09;
```

---

## Q14: Non-Sargable Arithmetic on the Right Side

**Anti-pattern:**
```sql
SELECT *
FROM employees
WHERE salary + bonus > 80000;
```
**Problem:** The expression `salary + bonus` must be evaluated for every row; no index on `salary` alone can help.

**Fix:**
```sql
SELECT *
FROM employees
WHERE salary > 80000 - bonus;
```
**Note:** This is still non-sargable if `bonus` varies per row; consider a computed column with an index, or restructure the schema.

**Alt1 — computed column + index (SQL Server):**
```sql
ALTER TABLE employees ADD total_comp AS (salary + bonus) PERSISTED;
CREATE INDEX idx_employees_total_comp ON employees (total_comp);

SELECT *
FROM employees
WHERE total_comp > 80000;
```

---

## Q15: Redundant BETWEEN with Exclusive Upper Bound

**Anti-pattern:**
```sql
SELECT *
FROM logs
WHERE created_at BETWEEN '2024-01-01' AND '2024-01-31';
```
**Problem:** `BETWEEN` is inclusive on both ends. If `created_at` has time components, rows on `2024-01-31 23:59:59` are included but `2024-02-01 00:00:00` is excluded — which may or may not be intended. More critically, many developers forget the inclusive upper bound and introduce off-by-one bugs.

**Fix:**
```sql
SELECT *
FROM logs
WHERE created_at >= '2024-01-01'
  AND created_at <  '2024-02-01';
```

---

## Q16: Overlap Trap — BETWEEN on Two Ranges

**Anti-pattern:**
```sql
SELECT *
FROM reservations
WHERE '2024-07-01' BETWEEN check_in AND check_out
  AND '2024-07-10' BETWEEN check_in AND check_out;
```
**Problem:** This tests whether two *separate* dates each fall inside a reservation — it does *not* detect overlapping date ranges.

**Fix — proper range overlap:**
```sql
SELECT *
FROM reservations
WHERE check_in  <= '2024-07-10'
  AND check_out >= '2024-07-01';
```

---

## Q17: DISTINCT to Mask Duplicate Rows from Bad Join

**Anti-pattern:**
```sql
SELECT DISTINCT o.order_id, o.total
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id;
```
**Problem:** The many-to-many between orders and products duplicates order rows; `DISTINCT` hides the problem but forces a sort/hash on the entire result set.

**Fix — deduplicate *before* joining:**
```sql
SELECT DISTINCT oi.order_id, o.total
FROM orders o
JOIN (
    SELECT DISTINCT order_id
    FROM order_items
) oi ON oi.order_id = o.order_id;
```

**Alt1 — EXISTS if you only need the order header:**
```sql
SELECT o.order_id, o.total
FROM orders o
WHERE EXISTS (
    SELECT 1
    FROM order_items oi
    JOIN products p ON p.product_id = oi.product_id
    WHERE oi.order_id = o.order_id
);
```

---

## Q18: Cartesian Product — Missing Join Key

**Anti-pattern:**
```sql
SELECT c.name, p.product_name, o.total
FROM customers c
JOIN products p
JOIN orders o;
```
**Problem:** No `ON` clause links the tables; every row in `customers` is paired with every row in `products` × every row in `orders` — a massive cross join.

**Fix:**
```sql
SELECT c.name, p.product_name, o.total
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id;
```

---

## Q19: Accidental Cartesian Product via Missing Condition

**Anti-pattern:**
```sql
SELECT e.name, d.department_name, p.project_name
FROM employees e
JOIN departments d ON d.dept_id = e.dept_id
JOIN projects p ON p.project_id = e.project_id
                 AND p.status = 'active';
```
**Problem:** If an employee can belong to multiple projects, joining on `project_id` *and* `status` still multiplies rows if the join condition is incomplete — ensure the join captures the correct grain.

**Fix — deduplicate with a CTE or subquery first:**
```sql
WITH active_emp_projects AS (
    SELECT DISTINCT employee_id, project_name
    FROM projects
    WHERE status = 'active'
)
SELECT e.name, d.department_name, a.project_name
FROM employees e
JOIN departments d ON d.dept_id = e.dept_id
JOIN active_emp_projects a ON a.employee_id = e.employee_id;
```

---

## Q20: GROUP BY on Non-Indexed Column Forces Sort

**Anti-pattern:**
```sql
SELECT region, COUNT(*) AS cnt
FROM sales
GROUP BY region;
```
**Problem:** If `region` is low-cardinality but has no index, the engine must build a hash table or sort the entire table before grouping.

**Fix — add an index on the grouping column:**
```sql
CREATE INDEX idx_sales_region ON sales (region);

SELECT region, COUNT(*) AS cnt
FROM sales
GROUP BY region;
```

**Alt1 — if the table is scanned anyway, a covering index avoids heap lookups:**
```sql
CREATE INDEX idx_sales_region_covering ON sales (region, sale_id);
```

---

## Q21: HAVING Used Instead of WHERE for Non-Aggregated Filter

**Anti-pattern:**
```sql
SELECT department, AVG(salary) AS avg_salary
FROM employees
HAVING department = 'Engineering';
```
**Problem:** `HAVING` is for post-aggregation filters; filtering non-aggregated columns here may cause the engine to aggregate the entire table first, then discard rows — or produce an error in strict SQL modes.

**Fix:**
```sql
SELECT department, AVG(salary) AS avg_salary
FROM employees
WHERE department = 'Engineering'
GROUP BY department;
```

---

## Q22: HAVING Filter on Non-Aggregated Column with GROUP BY

**Anti-pattern:**
```sql
SELECT customer_id, SUM(amount) AS total
FROM orders
GROUP BY customer_id
HAVING status = 'completed';
```
**Problem:** `status` is not aggregated and not in `GROUP BY`; this is invalid SQL in most engines and certainly wasteful.

**Fix:**
```sql
SELECT customer_id, SUM(amount) AS total
FROM orders
WHERE status = 'completed'
GROUP BY customer_id;
```

---

## Q23: Correlated Subquery in SELECT List (Per-Row Execution)

**Anti-pattern:**
```sql
SELECT
    e.name,
    e.salary,
    (SELECT MAX(salary) FROM employees WHERE dept_id = e.dept_id) AS dept_max
FROM employees e;
```
**Problem:** The subquery executes once *per row* of the outer query — O(n × m) cost on large tables.

**Fix — window function:**
```sql
SELECT
    name,
    salary,
    MAX(salary) OVER (PARTITION BY dept_id) AS dept_max
FROM employees;
```

**Alt1 — JOIN to a pre-aggregated table:**
```sql
SELECT
    e.name,
    e.salary,
    d.dept_max
FROM employees e
JOIN (
    SELECT dept_id, MAX(salary) AS dept_max
    FROM employees
    GROUP BY dept_id
) d ON d.dept_id = e.dept_id;
```

---

## Q24: Correlated Subquery Counts per Row

**Anti-pattern:**
```sql
SELECT
    c.customer_id,
    c.name,
    (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) AS order_count
FROM customers c;
```
**Problem:** The `COUNT(*)` subquery runs for every customer — disastrous on tables with millions of rows.

**Fix — LEFT JOIN + GROUP BY:**
```sql
SELECT
    c.customer_id,
    c.name,
    COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name;
```

**Alt1 — window function (no outer GROUP BY needed):**
```sql
SELECT
    c.customer_id,
    c.name,
    COUNT(o.order_id) OVER (PARTITION BY c.customer_id) AS order_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id;
```

---

## Q25: Correlated EXISTS in Projection Instead of JOIN

**Anti-pattern:**
```sql
SELECT
    p.product_name,
    (SELECT SUM(quantity) FROM order_items oi WHERE oi.product_id = p.product_id) AS total_sold
FROM products p;
```
**Problem:** Each product triggers a separate aggregation scan of `order_items`.

**Fix:**
```sql
SELECT
    p.product_name,
    COALESCE(SUM(oi.quantity), 0) AS total_sold
FROM products p
LEFT JOIN order_items oi ON oi.product_id = p.product_id
GROUP BY p.product_name;
```

---

## Q26: Fan-Out Join — Row Explosion Before GROUP BY

**Anti-pattern:**
```sql
SELECT
    o.order_id,
    COUNT(oi.line_item_id) AS item_count,
    SUM(oi.quantity * oi.unit_price) AS order_total
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
GROUP BY o.order_id;
```
**Problem:** If a product appears in multiple `order_items` rows for the same order (e.g., through a redundant join to a child table), the join multiplies rows *before* the aggregation, inflating counts and sums.

**Fix — deduplicate at the lowest grain first:**
```sql
WITH deduped_items AS (
    SELECT DISTINCT order_id, line_item_id, product_id, quantity, unit_price
    FROM order_items
)
SELECT
    o.order_id,
    COUNT(di.line_item_id) AS item_count,
    SUM(di.quantity * di.unit_price) AS order_total
FROM orders o
JOIN deduped_items di ON di.order_id = o.order_id
JOIN products p ON p.product_id = di.product_id
GROUP BY o.order_id;
```

---

## Q27: Fan-Out from One-to-Many Join Inflates Aggregates

**Anti-pattern:**
```sql
SELECT
    c.customer_id,
    c.name,
    SUM(o.amount) AS total_spent
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY c.customer_id, c.name;
```
**Problem:** Each order is joined to its line items, so the `o.amount` value is repeated per item and summed multiple times — the total is inflated.

**Fix — aggregate orders independently, then join:**
```sql
SELECT
    c.customer_id,
    c.name,
    COALESCE(os.total_spent, 0) AS total_spent
FROM customers c
LEFT JOIN (
    SELECT customer_id, SUM(amount) AS total_spent
    FROM orders
    GROUP BY customer_id
) os ON os.customer_id = c.customer_id;
```

---

## Q28: LEFT JOIN Needed but INNER JOIN Used

**Anti-pattern:**
```sql
SELECT
    c.customer_id,
    c.name,
    o.order_id
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id;
```
**Problem:** Customers without orders vanish from the result; if the report must list *all* customers, this is incorrect.

**Fix:**
```sql
SELECT
    c.customer_id,
    c.name,
    o.order_id
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id;
```

---

## Q29: LEFT JOIN When INNER JOIN Suffices

**Anti-pattern:**
```sql
SELECT
    o.order_id,
    c.name,
    c.email
FROM orders o
LEFT JOIN customers c ON c.customer_id = o.customer_id;
```
**Problem:** Every order *must* have a valid `customer_id` (FK constraint); LEFT JOIN adds unnecessary NULL checks and may prevent the optimiser from choosing the best plan.

**Fix:**
```sql
SELECT
    o.order_id,
    c.name,
    c.email
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id;
```

---

## Q30: Pagination with OFFSET on Large Offsets

**Anti-pattern:**
```sql
SELECT *
FROM products
ORDER BY product_id
LIMIT 20 OFFSET 1000000;
```
**Problem:** The engine reads and discards 1,000,000 rows before returning 20 — performance degrades linearly with page depth.

**Fix — keyset / cursor-based pagination:**
```sql
SELECT *
FROM products
WHERE product_id > 1000000
ORDER BY product_id
LIMIT 20;
```

**Alt1 — remembered-position pagination (if the client stores the last `product_id`):**
```sql
-- Client sends: last_product_id = 1000000
SELECT *
FROM products
WHERE product_id > :last_product_id
ORDER BY product_id
LIMIT 20;
```

---

## Q31: Deep OFFSET with ORDER BY and WHERE

**Anti-pattern:**
```sql
SELECT *
FROM logs
WHERE level = 'ERROR'
ORDER BY created_at DESC
LIMIT 50 OFFSET 500000;
```
**Problem:** Even with a filtered WHERE, the engine must sort all matching rows and skip 500k before returning 50.

**Fix — keyset using the last seen timestamp:**
```sql
SELECT *
FROM logs
WHERE level = 'ERROR'
  AND created_at < '2024-03-15T14:30:00'  -- last row's created_at from previous page
ORDER BY created_at DESC
LIMIT 50;
```

---

## Q32: COUNT(*) on a Huge Table Without an Index

**Anti-pattern:**
```sql
SELECT COUNT(*) FROM audit_log;
```
**Problem:** On a billion-row table with no covering index, this forces a full table scan and can run for minutes.

**Fix — use an approximation if exact count is not required:**
```sql
-- MySQL / InnoDB approximate count:
SHOW TABLE STATUS LIKE 'audit_log';   -- Rows column

-- PostgreSQL approximate count:
SELECT reltuples::BIGTABLE AS estimate
FROM pg_class
WHERE relname = 'audit_log';
```

**Alt1 — maintain a counter table for exact counts:**
```sql
CREATE TABLE row_counts (
    table_name VARCHAR(128) PRIMARY KEY,
    cnt        BIGINT NOT NULL
);

-- Update via triggers or batch jobs
SELECT cnt FROM row_counts WHERE table_name = 'audit_log';
```

---

## Q33: COUNT(*) with a Covering Index

**Anti-pattern:**
```sql
SELECT COUNT(*) FROM orders WHERE status = 'shipped';
```
**Problem:** If `status` is not indexed, every row is scanned. Even if it is, the engine may still visit the heap.

**Fix — covering index so only the index is read:**
```sql
CREATE INDEX idx_orders_status_covering ON orders (status, order_id);

SELECT COUNT(*) FROM orders WHERE status = 'shipped';
```

---

## Q34: Updating Rows One at a Time in a Loop

**Anti-pattern:**
```sql
-- Procedural loop (pseudo-SQL)
FOR rec IN (SELECT order_id FROM orders WHERE status = 'pending') LOOP
    UPDATE orders
    SET status = 'processing', updated_at = NOW()
    WHERE order_id = rec.order_id;
END LOOP;
```
**Problem:** Each iteration is a separate transaction with its own log flush, lock acquisition, and index update — orders of magnitude slower than a single set-based statement.

**Fix:**
```sql
UPDATE orders
SET status = 'processing', updated_at = NOW()
WHERE status = 'pending';
```

---

## Q35: Cursor-Based Processing Instead of Set-Based

**Anti-pattern:**
```sql
DECLARE cur CURSOR FOR
    SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id;

OPEN cur;
FETCH NEXT FROM cur INTO @cid, @total;
WHILE @@FETCH_STATUS = 0
BEGIN
    UPDATE customers SET lifetime_value = @total WHERE customer_id = @cid;
    FETCH NEXT FROM cur INTO @cid, @total;
END
CLOSE cur;
DEALLOCATE cur;
```
**Problem:** Row-by-row cursor processing avoids set-based optimisations; each fetch and update is a separate round-trip.

**Fix:**
```sql
UPDATE customers c
JOIN (
    SELECT customer_id, SUM(amount) AS total
    FROM orders
    GROUP BY customer_id
) o ON o.customer_id = c.customer_id
SET c.lifetime_value = o.total;
```

---

## Q36: Storing Delimited Data in a Single Column

**Anti-pattern:**
```sql
CREATE TABLE products (
    product_id   INT PRIMARY KEY,
    product_name VARCHAR(200),
    tags         VARCHAR(500)   -- e.g. 'electronics,sale,clearance'
);
```
**Problem:** Searching for a tag requires string functions (`FIND_IN_SET`, `LIKE '%sale%'`), which are non-sargable, can't use indexes, and produce false positives (`'onsale'` matches `'%sale%'`).

**Fix — normalise to a junction table:**
```sql
CREATE TABLE product_tags (
    product_id INT NOT NULL,
    tag        VARCHAR(100) NOT NULL,
    PRIMARY KEY (product_id, tag),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

SELECT p.*
FROM products p
JOIN product_tags pt ON pt.product_id = p.product_id
WHERE pt.tag = 'sale';
```

---

## Q37: Entity-Attribute-Value (EAV) Abuse

**Anti-pattern:**
```sql
CREATE TABLE product_attributes (
    product_id   INT,
    attribute    VARCHAR(100),
    value_str    VARCHAR(500),
    value_num    DECIMAL(12,2)
);

-- Query: find products where weight > 5 AND color = 'red'
SELECT *
FROM product_attributes pa1
JOIN product_attributes pa2
    ON pa2.product_id = pa1.product_id
JOIN product_attributes pa3
    ON pa3.product_id = pa1.product_id
WHERE pa1.attribute = 'weight'  AND pa1.value_num > 5
  AND pa2.attribute = 'color'   AND pa2.value_str = 'red';
```
**Problem:** Each attribute filter requires a self-join; query complexity grows linearly with the number of filters; no type safety; no index efficiency.

**Fix — use JSONB (PostgreSQL) or typed columns:**
```sql
CREATE TABLE products (
    product_id   INT PRIMARY KEY,
    product_name VARCHAR(200),
    weight       DECIMAL(8,2),
    color        VARCHAR(50)
);

CREATE INDEX idx_products_color ON products (color);
CREATE INDEX idx_products_weight ON products (weight);

SELECT *
FROM products
WHERE weight > 5
  AND color = 'red';
```

**Alt1 — JSONB for truly dynamic attributes:**
```sql
CREATE TABLE products (
    product_id   INT PRIMARY KEY,
    product_name VARCHAR(200),
    attributes   JSONB
);

CREATE INDEX idx_products_attrs ON products USING gin (attributes);

SELECT *
FROM products
WHERE attributes @> '{"color":"red","weight":5}';
```

---

## Q38: Implicit N+1 in a Stored Procedure (Cursor Over Join)

**Anti-pattern:**
```sql
DECLARE cur CURSOR FOR SELECT order_id FROM orders;

OPEN cur;
FETCH NEXT FROM cur INTO @oid;
WHILE @@FETCH_STATUS = 0
BEGIN
    SELECT o.order_id, c.name, c.email
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    WHERE o.order_id = @oid;

    FETCH NEXT FROM cur INTO @oid;
END
CLOSE cur;
DEALLOCATE cur;
```
**Problem:** The join inside the cursor runs once per order — classic N+1: N separate join scans instead of one.

**Fix:**
```sql
SELECT o.order_id, c.name, c.email
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id;
```

---

## Q39: DISTINCT ON Used Incorrectly (PostgreSQL)

**Anti-pattern:**
```sql
SELECT DISTINCT ON (department)
    employee_id, name, department, salary
FROM employees
ORDER BY department, salary DESC;
```
**Problem:** `DISTINCT ON` keeps the first row per group based on the `ORDER BY`; if the intent is "highest salary per department", the non-deterministic tie-breaking may return inconsistent rows across runs.

**Fix — use a window function for deterministic top-N per group:**
```sql
WITH ranked AS (
    SELECT
        employee_id, name, department, salary,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC, employee_id) AS rn
    FROM employees
)
SELECT employee_id, name, department, salary
FROM ranked
WHERE rn = 1;
```

---

## Q40: DISTINCT ON with Unordered Input

**Anti-pattern:**
```sql
SELECT DISTINCT ON (category)
    product_id, product_name, category, price
FROM products;
```
**Problem:** Without an `ORDER BY`, PostgreSQL picks an arbitrary row per category — the result is non-deterministic.

**Fix:**
```sql
SELECT DISTINCT ON (category)
    product_id, product_name, category, price
FROM products
ORDER BY category, price DESC;
```

---

## Q41: Selecting RAND() / RANDOM() per Row — Non-Deterministic Result

**Anti-pattern:**
```sql
SELECT *, RAND() AS sort_key
FROM products
ORDER BY sort_key
LIMIT 10;
```
**Problem:** `RAND()` is evaluated per row *and* again for each reference; the ordering is non-deterministic and cannot use an index. In MySQL, `RAND()` in `ORDER BY` triggers a filesort with a new random value per comparison — extremely slow on large tables.

**Fix — single random value computed once:**
```sql
SET @seed = RAND();

SELECT *
FROM products
ORDER BY RAND()          -- MySQL: still non-indexed but at least one evaluation
LIMIT 10;
```

**Alt1 — best approach: pick a random ID range:**
```sql
SELECT *
FROM products
WHERE product_id >= FLOOR(1 + RAND() * (SELECT MAX(product_id) FROM products))
ORDER BY product_id
LIMIT 10;
```

---

## Q42: Comparing Floats for Equality

**Anti-pattern:**
```sql
SELECT *
FROM measurements
WHERE value = 3.14;
```
**Problem:** IEEE 754 floating-point values have representation errors (`0.1 + 0.2 ≠ 0.3`); exact equality comparisons almost never match stored values.

**Fix — use an epsilon-based range:**
```sql
SELECT *
FROM measurements
WHERE ABS(value - 3.14) < 0.0001;
```

**Alt1 — use DECIMAL/NUMERIC columns for exact values:**
```sql
CREATE TABLE measurements (
    measurement_id INT PRIMARY KEY,
    value          DECIMAL(12,4)   -- exact to 4 decimal places
);
```

---

## Q43: Float Equality in JOIN Condition

**Anti-pattern:**
```sql
SELECT a.*
FROM sensor_readings a
JOIN sensor_readings b
  ON a.value = b.value
  AND a.sensor_id <> b.sensor_id;
```
**Problem:** Float equality in a join condition is unreliable; matching rows may be missed or spuriously included due to rounding.

**Fix — bucket by rounding to a fixed precision:**
```sql
SELECT a.*
FROM sensor_readings a
JOIN sensor_readings b
  ON ROUND(a.value, 4) = ROUND(b.value, 4)
  AND a.sensor_id <> b.sensor_id;
```

**Alt1 — use DECIMAL column type for exact match joins:**
```sql
-- Schema change: store value as DECIMAL(12,4)
-- Then a direct join works:
SELECT a.*
FROM sensor_readings a
JOIN sensor_readings b
  ON a.value = b.value
  AND a.sensor_id <> b.sensor_id;
```

---

## Q44: Timezone Conversion Inside WHERE Strips Index

**Anti-pattern:**
```sql
SELECT *
FROM events
WHERE CONVERT_TZ(event_ts, 'UTC', 'America/New_York') >= '2024-06-01';
```
**Problem:** `CONVERT_TZ()` is applied to every row; the index on `event_ts` (stored in UTC) is unusable.

**Fix — convert the bounds, not the column:**
```sql
SELECT *
FROM events
WHERE event_ts >= CONVERT_TZ('2024-06-01 00:00:00', 'America/New_York', 'UTC')
  AND event_ts <  CONVERT_TZ('2024-07-01 00:00:00', 'America/New_York', 'UTC');
```

---

## Q45: Timezone-Aware Query Without Converting Bounds

**Anti-pattern:**
```sql
-- Store all timestamps in UTC
SELECT *
FROM appointments
WHERE appointment_ts >= '2024-03-10 00:00:00'
  AND appointment_ts <  '2024-03-11 00:00:00';
```
**Problem:** If the user is in `US/Eastern` and DST spring-forward occurs on 2024-03-10, the UTC range doesn't align with the local midnight-to-midnight the user expects.

**Fix — explicitly convert the user's local bounds to UTC:**
```sql
SELECT *
FROM appointments
WHERE appointment_ts >= AT TIME ZONE 'US/Eastern' AT TIME ZONE 'UTC'
                       = '2024-03-10 00:00:00'
  AND appointment_ts <  (TIMESTAMP '2024-03-11 00:00:00'
                         AT TIME ZONE 'US/Eastern'
                         AT TIME ZONE 'UTC');
```

---

## Q46: UPDATE That Moves Rows Between Pages (Index Fragmentation)

**Anti-pattern:**
```sql
UPDATE orders
SET order_date = DATE_ADD(order_date, INTERVAL 30 DAY)
WHERE order_id = 12345;
```
**Problem:** Changing a clustered-index key forces the engine to delete the row from one page and insert it into another — a "page split" that fragments the index and hurts range-scan performance.

**Fix — avoid updating indexed key columns; use a non-key discriminator:**
```sql
-- Add a status column instead of shifting dates
ALTER TABLE orders ADD COLUMN adjustment_days INT DEFAULT 0;

UPDATE orders
SET adjustment_days = 30
WHERE order_id = 12345;

-- Query-time adjustment:
SELECT *, DATE_ADD(order_date, INTERVAL adjustment_days DAY) AS effective_date
FROM orders
WHERE order_id = 12345;
```

---

## Q47: UPDATE on a Wide Table Moving Most Rows

**Anti-pattern:**
```sql
UPDATE products
SET price = price * 1.10
WHERE category = 'Electronics';
```
**Problem:** If this updates millions of rows, it locks the table for an extended period, generates massive redo/undo logs, and may cause replication lag.

**Fix — batch the update:**
```sql
-- Process 10,000 rows at a time until no rows remain
UPDATE products
SET price = price * 1.10
WHERE category = 'Electronics'
  AND product_id BETWEEN 1 AND 10000;

-- Repeat for subsequent ranges...
```

**Alt1 — if the application can tolerate eventual consistency, use a computed column:**
```sql
ALTER TABLE products ADD COLUMN adjusted_price AS (price * 1.10) PERSISTED;
```

---

## Q48: MAX() + GROUP BY Without a Useful Index

**Anti-pattern:**
```sql
SELECT department_id, MAX(salary) AS max_salary
FROM employees
GROUP BY department_id;
```
**Problem:** Without an index on `department_id` (or a covering index), the engine must scan the entire table and build a hash/sort for the GROUP BY.

**Fix — add a covering index:**
```sql
CREATE INDEX idx_employees_dept_salary ON employees (department_id, salary);

SELECT department_id, MAX(salary) AS max_salary
FROM employees
GROUP BY department_id;
```

---

## Q49: Temporary Filesort for ORDER BY with Low Selectivity

**Anti-pattern:**
```sql
SELECT *
FROM products
WHERE category = 'Books'
ORDER BY created_at DESC
LIMIT 20;
```
**Problem:** If the index is only on `category` (or there is no composite index), the engine sorts all "Books" rows in a temporary file before returning the top 20.

**Fix — composite index matching the WHERE + ORDER BY:**
```sql
CREATE INDEX idx_products_cat_created ON products (category, created_at DESC);

SELECT *
FROM products
WHERE category = 'Books'
ORDER BY created_at DESC
LIMIT 20;
```

---

## Q50: ORDER BY on Non-Indexed Column with Large Result Set

**Anti-pattern:**
```sql
SELECT *
FROM audit_log
ORDER BY event_timestamp DESC
LIMIT 100;
```
**Problem:** Without an index on `event_timestamp`, the entire table is sorted in memory or on disk just to return the last 100 rows.

**Fix:**
```sql
CREATE INDEX idx_audit_log_timestamp ON audit_log (event_timestamp);

SELECT *
FROM audit_log
ORDER BY event_timestamp DESC
LIMIT 100;
```

---

## Q51: Duplicates From Many-to-Many Join Requiring DISTINCT

**Anti-pattern:**
```sql
SELECT DISTINCT s.student_id, s.name
FROM students s
JOIN enrollments e ON e.student_id = s.student_id;
```
**Problem:** A student with multiple enrollments appears once per enrollment; `DISTINCT` fixes the output but forces a deduplication pass and discards meaningful detail.

**Fix — deduplicate the child side at its grain:**
```sql
SELECT student_id, name
FROM students s
WHERE EXISTS (
    SELECT 1
    FROM enrollments e
    WHERE e.student_id = s.student_id
);
```

---

## Q52: DISTINCT on High-Cardinality Result Set

**Anti-pattern:**
```sql
SELECT DISTINCT c.customer_id, c.email, o.order_id, o.created_at
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id;
```
**Problem:** The combination of columns is nearly unique per row already; `DISTINCT` sorts or hashes the entire result only to remove (almost) nothing.

**Fix — remove the DISTINCT and express the true intent:**
```sql
SELECT c.customer_id, c.email, o.order_id, o.created_at
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id;
```

---

## Q53: UNION (deduplicating) When UNION ALL Sufficed

**Anti-pattern:**
```sql
SELECT product_id, product_name FROM products WHERE active = 1
UNION
SELECT product_id, product_name FROM products WHERE featured = 1;
```
**Problem:** `UNION` sorts and dedupes the combined result even though the two branches are disjoint (active vs featured) — the sort is pure waste.

**Fix:**
```sql
SELECT product_id, product_name FROM products WHERE active = 1
UNION ALL
SELECT product_id, product_name FROM products WHERE featured = 1;
```

---

## Q54: Duplicate Branch Rows from UNION ALL

**Anti-pattern:**
```sql
SELECT order_id FROM orders WHERE status = 'new'
UNION ALL
SELECT order_id FROM orders WHERE status IN ('new', 'shipped');
```
**Problem:** First branch is a strict subset of the second, so rows are duplicated in the output.

**Fix — use one branch:**
```sql
SELECT order_id FROM orders WHERE status IN ('new', 'shipped');
```

---

## Q55: Whole-Table Pull With No Pagination

**Anti-pattern:**
```sql
SELECT * FROM transactions;
```
**Problem:** Pulls the entire table across the network, exhausting application memory and database I/O, even when the user only wants a page or a summary.

**Fix:**
```sql
SELECT *
FROM transactions
WHERE account_id = 123
ORDER BY transaction_date DESC
LIMIT 100;
```

---

## Q56: Unbounded Query in a Live Dashboard

**Anti-pattern:**
```sql
SELECT event_type, COUNT(*)
FROM events
GROUP BY event_type;
```
**Problem:** The dashboard shows *all-time* totals, so the aggregation scan grows every day and eventually monopolises the database.

**Fix — bound the window:**
```sql
SELECT event_type, COUNT(*)
FROM events
WHERE event_ts >= NOW() - INTERVAL 30 DAY
GROUP BY event_type;
```

---

## Q57: CTE Without a Join — Accidental Cross Join

**Anti-pattern:**
```sql
WITH product_sales AS (
    SELECT product_id, SUM(quantity) AS total_sold
    FROM order_items
    GROUP BY product_id
)
SELECT p.product_name, ps.total_sold
FROM products p, product_sales ps;   -- trailing comma creates a Cartesian product
```
**Problem:** A missing join between the CTE and the outer table multiplies every product by every aggregated row.

**Fix:**
```sql
WITH product_sales AS (
    SELECT product_id, SUM(quantity) AS total_sold
    FROM order_items
    GROUP BY product_id
)
SELECT p.product_name, ps.total_sold
FROM products p
JOIN product_sales ps ON ps.product_id = p.product_id;
```

---

## Q58: CTE That Is Used Without a Filter

**Anti-pattern:**
```sql
WITH all_orders AS (
    SELECT * FROM orders
)
SELECT *
FROM all_orders;
```
**Problem:** Fully materialising orders adds no value and defeats any index usage that the direct query would have; it's a self-inflicted performance tax.

**Fix:**
```sql
SELECT *
FROM orders;
```

---

## Q59: Selecting BLOB/VARBINARY Unnecessarily

**Anti-pattern:**
```sql
SELECT user_id, avatar_binary, bio, subscription_plan
FROM users
WHERE user_id = 42;
```
**Problem:** The avatar is a large binary object read into memory and shipped over the wire even though the caller only needs profile metadata.

**Fix — select only the columns actually needed:**
```sql
SELECT user_id, bio, subscription_plan
FROM users
WHERE user_id = 42;
```

---

## Q60: Scalar Subquery in Projection Over a Large Set

**Anti-pattern:**
```sql
SELECT
    o.order_id,
    o.total,
    (SELECT AVG(total) FROM orders WHERE customer_id = o.customer_id) AS customer_avg
FROM orders o;
```
**Problem:** This correlated subquery runs once per order row — for a million orders, it recomputes each customer's average a million times.

**Fix — window function computed once per partition:**
```sql
SELECT
    o.order_id,
    o.total,
    AVG(o.total) OVER (PARTITION BY o.customer_id) AS customer_avg
FROM orders o;
```

---

## Q61: Scalar Subquery in SELECT With NULL-Safe Fallback

**Anti-pattern:**
```sql
SELECT
    p.product_id,
    p.product_name,
    COALESCE(
        (SELECT MAX(price) FROM price_history WHERE product_id = p.product_id),
        p.base_price
    ) AS current_price
FROM products p;
```
**Problem:** The MAX subquery fires per product row; on 500k products, that's 500k separate index probes.

**Fix — LEFT JOIN once:**
```sql
SELECT
    p.product_id,
    p.product_name,
    COALESCE(ph.peak_price, p.base_price) AS current_price
FROM products p
LEFT JOIN (
    SELECT product_id, MAX(price) AS peak_price
    FROM price_history
    GROUP BY product_id
) ph ON ph.product_id = p.product_id;
```

---

## Q62: DISTINCT on a Join Then Aggregating Again

**Anti-pattern:**
```sql
SELECT customer_id, COUNT(DISTINCT order_id) AS order_count
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY customer_id;
```
**Problem:** The join duplicates order rows (once per line item), then `COUNT(DISTINCT ...)` is forced to deduplicate — a full sort per group.

**Fix — aggregate before the fan-out join:**
```sql
SELECT customer_id, COUNT(order_id) AS order_count
FROM orders
GROUP BY customer_id;
```

---

## Q63: COUNT(DISTINCT) Over Optimisable Data

**Anti-pattern:**
```sql
SELECT COUNT(DISTINCT customer_id)
FROM orders
WHERE created_at >= '2024-01-01';
```
**Problem:** `COUNT(DISTINCT)` builds a hash of all unique customer IDs in memory; on high-cardinality data this spills to disk.

**Fix — if an approximation is acceptable, use HyperLogLog (PostgreSQL):**
```sql
SELECT pg_stats.cardinality
FROM pg_stats
WHERE tablename = 'orders' AND attname = 'customer_id';
```

**Alt1 — approximation via sampling:**
```sql
SELECT COUNT(DISTINCT customer_id) * AVG(ct) AS approx_distinct
FROM (
    SELECT customer_id, COUNT(*) AS ct
    FROM orders
    WHERE created_at >= '2024-01-01'
      AND customer_id % 100 = 0
    GROUP BY customer_id
) sampled;
```

---

## Q64: GROUP BY Multiple Varying Columns

**Anti-pattern:**
```sql
SELECT event_date, event_type, region, channel, COUNT(*) AS cnt
FROM web_events
GROUP BY event_date, event_type, region, channel;
```
**Problem:** A four-column GROUP BY without a matching composite index forces a sort of the whole table.

**Fix — create a composite index matching the grouping pattern:**
```sql
CREATE INDEX idx_web_events_group ON web_events
    (event_date, event_type, region, channel);

SELECT event_date, event_type, region, channel, COUNT(*) AS cnt
FROM web_events
GROUP BY event_date, event_type, region, channel;
```

---

## Q65: ORDER BY on Low-Selectivity Column

**Anti-pattern:**
```sql
SELECT *
FROM subscriptions
WHERE status = 'active'
ORDER BY plan_id
LIMIT 50;
```
**Problem:** `plan_id` has low cardinality (5 plans). Ordering millions of active subscriptions by it still triggers a filesort because the index on `plan_id` cannot skip directly.

**Fix — page by the distinct key values:**
```sql
SELECT *
FROM subscriptions
WHERE status = 'active'
ORDER BY plan_id DESC, subscription_id DESC
LIMIT 50;
```

**Alt1 — if pagination is the goal, use keyset on the unique key:**
```sql
-- Last page returned subscription_id = 999993
SELECT *
FROM subscriptions
WHERE status = 'active'
  AND subscription_id > 999993
ORDER BY subscription_id
LIMIT 50;
```

---

## Q66: JOIN Condition With NULL-Safe Comparison (Über-Gem)

**Anti-pattern:**
```sql
SELECT *
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id;
```
**Problem:** This is actually a *good* pattern — but a common anti-pattern is joining on a NULLable column with equality, which never matches NULLs, silently dropping rows.

**Fix — understand NULL semantics and use NULLS NOT DISTINCT / IS NOT DISTINCT FROM (PostgreSQL):**
```sql
SELECT *
FROM customers c
LEFT JOIN orders o
    ON o.referrer_code IS NOT DISTINCT FROM c.referrer_code;
```

---

## Q67: Subquery Materialising a Huge Temp Table

**Anti-pattern:**
```sql
SELECT *
FROM orders
JOIN (
    SELECT * FROM customers
) c ON c.customer_id = orders.customer_id;
```
**Problem:** The subquery forces a materialisation of the full customers table before the join, preventing index-driven nested-loop access.

**Fix — join the base table directly:**
```sql
SELECT *
FROM orders
JOIN customers c ON c.customer_id = orders.customer_id;
```

---

## Q68: DISTINCT Combined With ORDER BY on a Different Column

**Anti-pattern:**
```sql
SELECT DISTINCT customer_id
FROM orders
ORDER BY created_at DESC;
```
**Problem:** You must sort by `created_at` even though the output only has `customer_id`; the engine cannot use one index for both a distinct on ID and a sort on timestamp.

**Fix — keyset pagination on the unique id:**
```sql
SELECT customer_id
FROM orders
WHERE customer_id > :last_customer_id
ORDER BY customer_id
LIMIT 50;
```

**Alt1 — window deduplication when the latest order per customer is wanted:**
```sql
WITH ranked AS (
    SELECT
        customer_id, created_at,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC) AS rn
    FROM orders
)
SELECT customer_id, created_at
FROM ranked
WHERE rn = 1;
```

---

## Q69: Non-Sargable Concatenation in WHERE

**Anti-pattern:**
```sql
SELECT *
FROM users
WHERE CONCAT(first_name, ' ', last_name) = 'John Smith';
```
**Problem:** Concatenating columns per row defeats any index on `first_name` or `last_name`.

**Fix:**
```sql
SELECT *
FROM users
WHERE first_name = 'John'
  AND last_name  = 'Smith';
```

---

## Q70: UPPER() on a Case-Sensitive Join

**Anti-pattern:**
```sql
SELECT *
FROM api_keys a
JOIN apps b ON UPPER(a.client_code) = UPPER(b.client_code);
```
**Problem:** Applying `UPPER()` to both sides of the join makes it non-merge-hash-friendly and unusable for any index.

**Fix — store case-normalised keys and join directly:**
```sql
SELECT *
FROM api_keys a
JOIN apps b ON a.client_code = b.client_code;
```

---

## Q71: Nested Subquery for Row-Level Authentication

**Anti-pattern:**
```sql
SELECT *
FROM documents
WHERE owner_id = 8
  AND document_id IN (
      SELECT document_id
      FROM document_permissions
      WHERE user_id = 8
  );
```
**Problem:** The `IN` subquery returns every shared document ID for the user, at full materialisation, before the outer filter runs.

**Fix — join or EXISTS with correlation:**
```sql
SELECT d.*
FROM documents d
WHERE owner_id = 8
   OR EXISTS (
       SELECT 1
       FROM document_permissions dp
       WHERE dp.document_id = d.document_id
         AND dp.user_id = 8
   );
```

---

## Q72: Redundant DELETE Loop With Recheck

**Anti-pattern:**
```sql
-- Application loop
WHILE EXISTS (SELECT 1 FROM sessions WHERE expired_at < NOW() LIMIT 1000)
BEGIN
    DELETE FROM sessions WHERE expired_at < NOW() LIMIT 1000;
END;
```
**Problem:** Repeated `EXISTS` probes and `LIMIT` deletes in a loop produce many small transaction churns instead of one set-based statement.

**Fix:**
```sql
DELETE FROM sessions
WHERE expired_at < NOW() - INTERVAL 7 DAY;
```
**Note:** For very large deletes, still batch, but do it set-based with a bounded range:
```sql
DELETE FROM sessions
WHERE expired_at < NOW() - INTERVAL 7 DAY
  AND session_id < 500000;
```

---

## Q73: UPDATE Using a Subquery That Re-Scans

**Anti-pattern:**
```sql
UPDATE customers
SET last_order_date = (
    SELECT MAX(created_at)
    FROM orders
    WHERE customer_id = customers.customer_id
)
WHERE EXISTS (
    SELECT 1 FROM orders WHERE customer_id = customers.customer_id
);
```
**Problem:** The correlated subquery is executed per customer — an N+1 update that's identical to the set-based alternative.

**Fix:**
```sql
UPDATE customers c
JOIN (
    SELECT customer_id, MAX(created_at) AS last_order_date
    FROM orders
    GROUP BY customer_id
) o ON o.customer_id = c.customer_id
SET c.last_order_date = o.last_order_date;
```

---

## Q74: WHERE With OR on the Same Indexed Column Pair

**Anti-pattern:**
```sql
SELECT *
FROM orders
WHERE customer_id = 5 OR (customer_id = 7 AND status = 'open');
```
**Problem:** The OR confuses the range optimisation; the engine may stop using the index on `customer_id` entirely.

**Fix — rewrite as UNION:**
```sql
SELECT *
FROM orders
WHERE customer_id = 5

UNION ALL

SELECT *
FROM orders
WHERE customer_id = 7
  AND status = 'open';
```

---

## Q75: IN With a Very Large Literal List

**Anti-pattern:**
```sql
SELECT *
FROM users
WHERE id IN (1, 2, 3, ..., 50000);   -- 50k hard-coded IDs
```
**Problem:** Statement size explodes, the query cache is useless, and the planer treats the list as an expensive constant scan instead of leveraging an index range.

**Fix — use a temp table / values list join:**
```sql
CREATE TEMP TABLE wanted_ids (id INT PRIMARY KEY);
INSERT INTO wanted_ids VALUES (1), (2), (3), ...;

SELECT u.*
FROM users u
JOIN wanted_ids w ON w.id = u.id;
```

**Alt1 — PostgreSQL VALUES list join:**
```sql
SELECT u.*
FROM users u
JOIN (VALUES (1), (2), (3)) AS w(id) ON w.id = u.id;
```

---

## Q76: COUNT(*) Inflated by a Fan-Out Join

**Anti-pattern:**
```sql
SELECT COUNT(*) AS total_items
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN inventory_log il ON il.product_id = oi.product_id;
```
**Problem:** If `inventory_log` has one row per stock movement per product, the join fans out and `COUNT(*)` counts inventory movements, not order items.

**Fix — count at the correct grain:**
```sql
SELECT COUNT(*) AS total_items
FROM order_items oi
WHERE oi.order_id IN (
    SELECT order_id FROM orders
);

-- or join only unique keys:
SELECT COUNT(*)
FROM order_items oi
JOIN (
    SELECT DISTINCT order_id FROM orders
) o ON o.order_id = oi.order_id;
```

---

## Q77: LIMIT Without ORDER BY Is Non-Deterministic

**Anti-pattern:**
```sql
SELECT *
FROM products
LIMIT 10;
```
**Problem:** Without `ORDER BY`, the chosen rows are heap order — arbitrary and inconsistent across runs, making pagination meaningless.

**Fix:**
```sql
SELECT *
FROM products
ORDER BY product_id
LIMIT 10;
```

---

## Q78: TRIM() in WHERE Breaks the Index

**Anti-pattern:**
```sql
SELECT *
FROM customers
WHERE TRIM(email) = 'jane@example.com';
```
**Problem:** `TRIM()` on the column forces a per-row evaluation; the index on `email` is bypassed.

**Fix — trim the constant instead:**
```sql
SELECT *
FROM customers
WHERE email = 'jane@example.com';
```

---

## Q79: EXTRACT() in WHERE — Same Class as YEAR()

**Anti-pattern:**
```sql
SELECT *
FROM events
WHERE EXTRACT(YEAR FROM event_ts) = 2024
  AND EXTRACT(MONTH FROM event_ts) = 3;
```
**Problem:** Both functions strip columns per row and make the `event_ts` index unusable.

**Fix:**
```sql
SELECT *
FROM events
WHERE event_ts >= '2024-03-01'
  AND event_ts <  '2024-04-01';
```

---

## Q80: String Transform in WHERE (REPLACE / SUBSTRING)

**Anti-pattern:**
```sql
SELECT *
FROM users
WHERE REPLACE(phone, '-', '') = '2125551234';
```
**Problem:** The column is transformed before comparison — non-sargable, index useless, and every row is scanned.

**Fix — normalise the stored value and query it directly:**
```sql
-- Store phones normalized in the column
SELECT *
FROM users
WHERE phone = '2125551234';
```

**Alt1 — generated column (MySQL 5.7+ / SQL Server):**
```sql
ALTER TABLE users ADD phone_normalized VARCHAR(20)
    GENERATED ALWAYS AS (REPLACE(phone, '-', '')) STORED;
CREATE INDEX idx_users_phone_norm ON users (phone_normalized);

SELECT *
FROM users
WHERE phone_normalized = '2125551234';
```

---

## Q81: DATE_ADD() on the Column Side of the Comparison

**Anti-pattern:**
```sql
SELECT *
FROM subscriptions
WHERE DATE_ADD(expires_at, INTERVAL 30 DAY) < NOW();
```
**Problem:** Date arithmetic is applied per row on the indexed column; the range can't use the index.

**Fix — shift the constant:**
```sql
SELECT *
FROM subscriptions
WHERE expires_at < NOW() - INTERVAL 30 DAY;
```

---

## Q82: Not-Equals Comparison Against NULLable Column

**Anti-pattern:**
```sql
SELECT *
FROM orders
WHERE shipped_at <> NOW() - INTERVAL 7 DAY;
```
**Problem:** Rows where `shipped_at IS NULL` fail the comparison (NULL propagates), yet they're exactly the unshipped orders you may care about — silent data loss.

**Fix — express the intent explicitly:**
```sql
SELECT *
FROM orders
WHERE shipped_at IS NULL
   OR shipped_at < NOW() - INTERVAL 7 DAY;
```

---

## Q83: OR With IS NULL That Kills the Index Plan

**Anti-pattern:**
```sql
SELECT *
FROM documents
WHERE owner_id = 8
   OR owner_id IS NULL;
```
**Problem:** The OR forces a scan because the planter can't decide which branch to index; this gets worse in big tables.

**Fix — UNION ALL, each branch index-friendly:**
```sql
SELECT *
FROM documents
WHERE owner_id = 8

UNION ALL

SELECT *
FROM documents
WHERE owner_id IS NULL;
```

---

## Q84: Non-Sargable BETWEEN With an Expression on the Column

**Anti-pattern:**
```sql
SELECT *
FROM reservations
WHERE DATE(check_in) BETWEEN '2024-05-01' AND '2024-05-31';
```
**Problem:** `DATE(check_in)` re-computed per row; the `check_in` index is unused despite the range shape.

**Fix:**
```sql
SELECT *
FROM reservations
WHERE check_in >= '2024-05-01 00:00:00'
  AND check_in <  '2024-06-01 00:00:00';
```

---

## Q85: GROUP BY on a Formatted Date String

**Anti-pattern:**
```sql
SELECT DATE_FORMAT(created_at, '%Y-%m') AS month, COUNT(*) AS cnt
FROM orders
GROUP BY DATE_FORMAT(created_at, '%Y-%m');
```
**Problem:** Grouping by the *formatted* value is identical to grouping by `EXTRACT(YEAR...)` — the expression defeats the `created_at` index and forces a filesort of the whole table.

**Fix — group by the bare column, format at the end:**
```sql
SELECT DATE_FORMAT(created_at, '%Y-%m') AS month, COUNT(*) AS cnt
FROM orders
WHERE created_at >= '2024-01-01'
  AND created_at <  '2025-01-01'
GROUP BY DATE_FORMAT(created_at, '%Y-%m');
```

**Alt1 — group by the indexable range expression:**
```sql
SELECT
    EXTRACT(YEAR_MONTH FROM created_at) AS ym,
    COUNT(*) AS cnt
FROM orders
WHERE created_at >= '2024-01-01'
  AND created_at <  '2025-01-01'
GROUP BY EXTRACT(YEAR_MONTH FROM created_at);
```

---

## Q86: HAVING Filter Referencing a Non-Aggregated Column

**Anti-pattern:**
```sql
SELECT region, COUNT(*) AS store_count
FROM stores
GROUP BY region
HAVING region = 'EMEA';
```
**Problem:** `region` is a group key, not an aggregate — filtering it belongs in `WHERE`; running it in `HAVING` may compute the full grouping first in some engines and is just confusing.

**Fix:**
```sql
SELECT region, COUNT(*) AS store_count
FROM stores
WHERE region = 'EMEA'
GROUP BY region;
```

---

## Q87: Running an Aggregate Twice via Subquery

**Anti-pattern:**
```sql
SELECT
    customer_id,
    (SELECT SUM(amount) FROM orders WHERE customer_id = c.customer_id) AS total,
    (SELECT COUNT(*)   FROM orders WHERE customer_id = c.customer_id) AS cnt
FROM customers c;
```
**Problem:** Two correlated subqueries scan `orders` per customer when one pass yields both aggregates.

**Fix — one grouped subquery:**
```sql
SELECT
    c.customer_id,
    o.total,
    o.cnt
FROM customers c
LEFT JOIN (
    SELECT customer_id, SUM(amount) AS total, COUNT(*) AS cnt
    FROM orders
    GROUP BY customer_id
) o ON o.customer_id = c.customer_id;
```

---

## Q88: Correlated IN When EXISTS Terminates Early

**Anti-pattern:**
```sql
SELECT *
FROM employees e
WHERE e.manager_id IN (
    SELECT employee_id FROM employees WHERE active = 1
);
```
**Problem:** This `IN` is actually uncorrelated in a benign way, but when the list is large the engine may materialise it. The pattern to avoid is a *correlated* `IN` that re-scans the subquery per outer row:

```sql
SELECT *
FROM documents d
WHERE d.owner_id IN (
    SELECT owner_id FROM shares s WHERE s.document_id = d.document_id
);
```
**Problem:** The correlated `IN` probes the `shares` subquery once per document; `EXISTS` can short-circuit after the first match.

**Fix:**
```sql
SELECT *
FROM documents d
WHERE EXISTS (
    SELECT 1
    FROM shares s
    WHERE s.document_id = d.document_id
);
```

---

## Q89: ORDER BY on a Function of the Column

**Anti-pattern:**
```sql
SELECT *
FROM users
ORDER BY LOWER(username);
```
**Problem:** A function in `ORDER BY` forces a full sort; the index on `username` is useless.

**Fix — order by the raw column:**
```sql
SELECT *
FROM users
ORDER BY username;
```

**Alt1 — functional index if caseless order is required:**
```sql
CREATE INDEX idx_users_lower_username ON users (LOWER(username));

SELECT *
FROM users
ORDER BY LOWER(username);
```

---

## Q90: Fixed-OFFSET Pagination on a Joined Result

**Anti-pattern:**
```sql
SELECT *
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
ORDER BY o.created_at DESC
LIMIT 25 OFFSET 2500;
```
**Problem:** OFFSET 2500 discards 2500 joined rows that the engine has already fetched and wiggled through the join and sort.

**Fix — keyset on the join-driving table:**
```sql
SELECT *
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.created_at < '2024-03-01T10:30:00'   -- last row's created_at
ORDER BY o.created_at DESC
LIMIT 25;
```

---

## Q91: Latest-Row-Per-Group via GROUP BY + JOIN (Tie Hazard)

**Anti-pattern:**
```sql
SELECT o.customer_id, o.order_id, o.created_at
FROM orders o
JOIN (
    SELECT customer_id, MAX(created_at) AS max_ts
    FROM orders
    GROUP BY customer_id
) m ON m.customer_id = o.customer_id
   AND m.max_ts = o.created_at;
```
**Problem:** If two orders share the same `created_at`, the join returns *both* — a row explosion that silently duplicates customers.

**Fix — deterministic window ranking:**
```sql
WITH ranked AS (
    SELECT
        customer_id, order_id, created_at,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY created_at DESC, order_id DESC
        ) AS rn
    FROM orders
)
SELECT customer_id, order_id, created_at
FROM ranked
WHERE rn = 1;
```

---

## Q92: DISTINCT As a Poor Man's Row Filter

**Anti-pattern:**
```sql
SELECT DISTINCT c.name, c.email
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.status = 'active';
```
**Problem:** The LEFT JOIN combined with a WHERE on the right table re-converts it to an inner join, and DISTINCT then dedupes rows that shouldn't have been produced at all — masking a semantic error.

**Fix — say what you mean with EXISTS:**
```sql
SELECT c.name, c.email
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id
      AND o.status = 'active'
);
```

---

## Q93: DELETE With a Correlated Subquery Per Row

**Anti-pattern:**
```sql
DELETE FROM sessions s
WHERE s.session_id IN (
    SELECT s2.session_id FROM sessions s2 WHERE s2.expired_at < NOW()
);
```
**Problem:** The related subquery reads the same table it deletes from — locking storms, and a full scan on `sessions` per candidate row.

**Fix — direct predicate (or windowed batching):**
```sql
DELETE FROM sessions
WHERE expired_at < NOW() - INTERVAL 30 DAY;
```
**Note:** In PostgreSQL you cannot reference the target table in a subquery in the same statement; this anti-pattern also fails outright there.

---

## Q94: Bulk INSERT Executed One Row at a Time

**Anti-pattern:**
```sql
-- Application loop:
INSERT INTO orders (customer_id, total, created_at) VALUES (1, 100, NOW());
INSERT INTO orders (customer_id, total, created_at) VALUES (2, 200, NOW());
INSERT INTO orders (customer_id, total, created_at) VALUES (3, 300, NOW());
```
**Problem:** Each statement is a separate round-trip/log flush/index write — thousands of small transactions instead of a single statement.

**Fix — multi-row INSERT:**
```sql
INSERT INTO orders (customer_id, total, created_at)
VALUES
    (1, 100, NOW()),
    (2, 200, NOW()),
    (3, 300, NOW());
```

**Alt1 — set-based INSERT ... SELECT:**
```sql
INSERT INTO orders (customer_id, total, created_at)
SELECT customer_id, SUM(amount), NOW()
FROM cart_rows
GROUP BY customer_id;
```

---

## Q95: INSERT ... SELECT With an Implicit Cast on the Indexed Column

**Anti-pattern:**
```sql
INSERT INTO orders (customer_id, order_id)
SELECT customer_ref, order_code
FROM staging_import;
```
**Problem:** If `staging_import.order_code` is VARCHAR but `order_id` is INT, every row gets an implicit cast during the insert index build — plus errors or data corruption for non-numeric values.

**Fix — cast explicitly at the source and validate first:**
```sql
INSERT INTO orders (customer_id, order_id)
SELECT
    CAST(customer_ref AS INT),
    CAST(order_code AS INT)
FROM staging_import
WHERE order_code ~ '^[0-9]+$';
```

---

## Q96: Recursive CTE Without a Termination Guard

**Anti-pattern:**
```sql
WITH RECURSIVE tree AS (
    SELECT employee_id, manager_id, 0 AS depth
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.employee_id, e.manager_id, t.depth + 1
    FROM employees e
    JOIN tree t ON e.manager_id = t.employee_id
)
SELECT * FROM tree;
```
**Problem:** A cycle in the data (A manages B, B manages A) makes the recursion spin forever, exhausting CPU and disk.

**Fix — add a depth guard and cycle detection:**
```sql
WITH RECURSIVE tree AS (
    SELECT employee_id, manager_id, 0 AS depth,
           ARRAY[employee_id] AS path
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.employee_id, e.manager_id, t.depth + 1,
           t.path || e.employee_id
    FROM employees e
    JOIN tree t ON e.manager_id = t.employee_id
    WHERE t.depth < 20
      AND NOT e.employee_id = ANY(t.path)
)
SELECT * FROM tree;
```

---

## Q97: WHERE on the Right Table Silently Turns LEFT JOIN Into INNER

**Anti-pattern:**
```sql
SELECT c.customer_id, c.name, o.order_id
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.status = 'completed';
```
**Problem:** Filtering the outer table in `WHERE` discards customers who have no matching orders — the LEFT JOIN's purpose is defeated.

**Fix — push the filter into the JOIN:**
```sql
SELECT c.customer_id, c.name, o.order_id
FROM customers c
LEFT JOIN orders o
    ON o.customer_id = c.customer_id
   AND o.status = 'completed';
```

---

## Q98: Scalar Subquery Re-Evaluated Though Constant

**Anti-pattern:**
```sql
SELECT
    o.order_id,
    o.total,
    o.total / (SELECT AVG(total) FROM orders) AS ratio
FROM orders o;
```
**Problem:** The same global average is recomputed (or worse, re-scanned) for each row — it doesn't depend on the outer row at all.

**Fix — hoist it to a CTE:**
```sql
WITH global_avg AS (
    SELECT AVG(total) AS avg_total FROM orders
)
SELECT
    o.order_id,
    o.total,
    o.total / ga.avg_total AS ratio
FROM orders o
CROSS JOIN global_avg ga;
```

---

## Q99: MAX() Trick That Returns Wrong Sibling Columns

**Anti-pattern:**
```sql
SELECT customer_id, MAX(order_id) AS newest_order_id, created_at
FROM orders
GROUP BY customer_id, created_at;
```
**Problem:** Adding `created_at` to the GROUP BY changes the grouping grain — you get the max order per *timestamp*, not the newest order's timestamp; the "latest order" answer is wrong.

**Fix — window with a deterministic tiebreak:**
```sql
WITH ranked AS (
    SELECT
        customer_id, created_at, order_id,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY created_at DESC, order_id DESC
        ) AS rn
    FROM orders
)
SELECT customer_id, created_at, order_id AS newest_order_id
FROM ranked
WHERE rn = 1;
```

---

## Q100: Unstable Keyset Pagination When the Sort Key Ties

**Anti-pattern:**
```sql
-- Page 2 of a feed sorted only by created_at:
SELECT *
FROM posts
WHERE created_at < '2024-06-20T12:00:00'
ORDER BY created_at DESC
LIMIT 20;
```
**Problem:** If the last row's `created_at` is shared by other posts, the next page's `created_at <` filter silently drops rows that share that timestamp — the feed loses posts and pages overlap.

**Fix — make the sort key unique by appending the primary key:**
```sql
-- Page 1 → remember last row: (created_at = '2024-06-20T12:00:00', post_id = 55921)
SELECT *
FROM posts
WHERE (created_at, post_id) < ('2024-06-20T12:00:00', 55921)
ORDER BY created_at DESC, post_id DESC
LIMIT 20;
```

**Alt1 — tuple/row-value comparison in PostgreSQL:**
```sql
SELECT *
FROM posts
WHERE ROW(created_at, post_id) < ROW('2024-06-20T12:00:00', 55921)
ORDER BY created_at DESC, post_id DESC
LIMIT 20;
```
