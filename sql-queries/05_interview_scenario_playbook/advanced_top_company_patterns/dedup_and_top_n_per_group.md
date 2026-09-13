# Deduplication and Top-N-Per-Group — 100 Interview Q&A

## Q1: Remove Exact Duplicate Rows (Keep One)

*Scenario:* Table `employees` has rows where every column is identical. Retain exactly one copy of each unique row.

*Schema hint:* `employees(id INT PRIMARY KEY, name VARCHAR(50), dept VARCHAR(30), salary DECIMAL(10,2))`

**Query:**
```sql
WITH dupes AS (
  SELECT id,
         ROW_NUMBER() OVER (
           PARTITION BY name, dept, salary ORDER BY id
         ) AS rn
  FROM employees
)
DELETE FROM employees
WHERE id IN (SELECT id FROM dupes WHERE rn > 1);
```
**Explanation:** Partitions by all value columns, assigns rn=1 to one copy per group, deletes the rest.

**Alt1:**
```sql
DELETE e1
  FROM employees e1
  INNER JOIN employees e2
    ON  e1.name   = e2.name
    AND e1.dept   = e2.dept
    AND e1.salary = e2.salary
    AND e1.id     > e2.id;
```
**Explanation:** Self-join pairs each duplicate with its lowest-id twin; the `>` condition makes only higher-id rows eligible for deletion.

**Alt2:**
```sql
DELETE FROM employees
WHERE id NOT IN (
  SELECT MIN(id) FROM employees
  GROUP BY name, dept, salary
);
```
**Explanation:** GROUP BY identifies the canonical row (min id) per unique combination; everything else is removed.

---

## Q2: De-duplicate by Key, Keep the Row with the Maximum id

*Scenario:* `orders` has duplicate `(customer_id, product)` combinations. Keep the row with the highest `order_id`.

*Schema hint:* `orders(order_id INT PK, customer_id INT, product VARCHAR(50), amount DECIMAL(10,2), order_date DATE)`

**Query:**
```sql
WITH ranked AS (
  SELECT order_id,
         ROW_NUMBER() OVER (
           PARTITION BY customer_id, product ORDER BY order_id DESC
         ) AS rn
  FROM orders
)
DELETE FROM orders
WHERE order_id IN (SELECT order_id FROM ranked WHERE rn > 1);
```
**Explanation:** Rows within each (customer, product) pair are sorted by `order_id DESC`; rn=1 is the latest, the rest are deleted.

**Alt1:**
```sql
DELETE o1
  FROM orders o1
  INNER JOIN orders o2
    ON  o1.customer_id = o2.customer_id
    AND o1.product     = o2.product
    AND o1.order_id    < o2.order_id;
```
**Explanation:** Self-join deletes any row whose order_id is smaller than another row in the same group.

---

## Q3: DELETE Duplicates — "Keep the Row with the Smallest id" (Self-Join)

*Scenario:* Classic interview pattern. Delete duplicates from `products` keeping the row with the lowest `id`.

*Schema hint:* `products(id INT PK, sku VARCHAR(20), name VARCHAR(100), price DECIMAL(10,2))`

**Query:**
```sql
DELETE p1
  FROM products p1
  INNER JOIN products p2
    ON  p1.sku   = p2.sku
    AND p1.name  = p2.name
    AND p1.price = p2.price
    AND p1.id    > p2.id;
```
**Explanation:** Each duplicate pairs with the row that has the smaller id; the larger-id row is deleted.

**Alt1:**
```sql
WITH ranked AS (
  SELECT id, ROW_NUMBER() OVER (
    PARTITION BY sku, name, price ORDER BY id ASC
  ) AS rn
  FROM products
)
DELETE FROM products WHERE id IN (SELECT id FROM ranked WHERE rn > 1);
```
**Explanation:** Window function assigns rn=1 to the smallest id per group; delete all the rest.

---

## Q4: DELETE Duplicates with ROW_NUMBER + CTE (MySQL 8+)

*Scenario:* MySQL 8+ supports CTEs and window functions. Dedup `login_events` by `(user_id, event_time)`.

*Schema hint:* `login_events(id INT PK AUTO_INCREMENT, user_id INT, event_time DATETIME, ip_address VARCHAR(45))`

**Query:**
```sql
WITH ranked AS (
  SELECT id,
         ROW_NUMBER() OVER (
           PARTITION BY user_id, event_time ORDER BY id
         ) AS rn
  FROM login_events
)
DELETE FROM login_events
WHERE id IN (SELECT id FROM ranked WHERE rn > 1);
```
**Explanation:** MySQL 8+ allows CTE-based DELETE; ROW_NUMBER names the duplicates and the subquery supplies their ids.

**Alt1 (MySQL 5.7 and older):**
```sql
DELETE le1
  FROM login_events le1
  INNER JOIN login_events le2
    ON  le1.user_id    = le2.user_id
    AND le1.event_time = le2.event_time
    AND le1.id         > le2.id;
```
**Explanation:** Self-join works on all MySQL versions since it needs no window functions or CTEs.

---

## Q5: UPDATE + Mark Duplicates, Then DELETE

*Scenario:* Some systems prohibit CTE-based DELETE or need an audit trail of what was removed. Mark duplicates first, then delete.

*Schema hint:* `transactions(id INT PK, account_id INT, txn_ref VARCHAR(20), amount DECIMAL(12,2))`

**Query:**
```sql
-- Step 1: Add a staging flag column
ALTER TABLE transactions ADD COLUMN is_dup TINYINT DEFAULT 0;

-- Step 2: Mark duplicates
WITH ranked AS (
  SELECT id, ROW_NUMBER() OVER (
    PARTITION BY account_id, txn_ref ORDER BY id
  ) AS rn
  FROM transactions
)
UPDATE transactions t
JOIN ranked r ON t.id = r.id
SET t.is_dup = 1
WHERE r.rn > 1;

-- Step 3: Delete marked rows
DELETE FROM transactions WHERE is_dup = 1;

-- Step 4: Drop the helper column
ALTER TABLE transactions DROP COLUMN is_dup;
```
**Explanation:** Two-step mark-then-delete pattern is useful when CTE-based DELETE is unsupported or when you need to audit the deletion.

**Alt1 (New-table swap):**
```sql
CREATE TABLE transactions_clean AS
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY account_id, txn_ref ORDER BY id
  ) AS rn
  FROM transactions
) t WHERE rn = 1;

TRUNCATE TABLE transactions;
INSERT INTO transactions SELECT id, account_id, txn_ref, amount FROM transactions_clean;
DROP TABLE transactions_clean;
```
**Explanation:** Copies only canonical rows to a clean table, then swaps it back into place. Atomic when wrapped in a transaction.

---

## Q6: Dedup Emails — Keep the Most Recent Record

*Scenario:* `users` has duplicate emails. Keep the row with the latest `created_at`.

*Schema hint:* `users(id INT PK, email VARCHAR(255), name VARCHAR(100), created_at TIMESTAMP)`

**Query:**
```sql
WITH ranked AS (
  SELECT id,
         ROW_NUMBER() OVER (
           PARTITION BY LOWER(TRIM(email)) ORDER BY created_at DESC
         ) AS rn
  FROM users
)
DELETE FROM users WHERE id IN (SELECT id FROM ranked WHERE rn > 1);
```
**Explanation:** Normalises email with LOWER+TRIM before partitioning; keeps the newest account per email.

**Alt1:**
```sql
DELETE u1
  FROM users u1
  INNER JOIN users u2
    ON  LOWER(TRIM(u1.email)) = LOWER(TRIM(u2.email))
    AND u1.created_at          < u2.created_at;
```
**Explanation:** Self-join keeps the row with the later `created_at`; the `<` comparison deletes the older one.

**Alt2:**
```sql
DELETE FROM users
WHERE id NOT IN (
  SELECT MAX(id) FROM users
  GROUP BY LOWER(TRIM(email))
);
```
**Explanation:** MAX(id) approximates "most recent" when ids are auto-incrementing.

---

## Q7: INSERT IGNORE to Prevent Duplicates (MySQL)

*Scenario:* Bulk-insert log rows; silently skip rows whose `(source, event_id)` already exists.

*Schema hint:* `event_log(id INT PK AUTO_INCREMENT, source VARCHAR(30), event_id VARCHAR(50), payload JSON, logged_at TIMESTAMP, UNIQUE KEY uq_event (source, event_id))`

**Query:**
```sql
INSERT IGNORE INTO event_log (source, event_id, payload, logged_at)
VALUES
  ('web', 'evt-101', '{"page":"/home"}', NOW()),
  ('app', 'evt-102', '{"action":"click"}', NOW()),
  ('web', 'evt-101', '{"page":"/home"}', NOW());  -- duplicate, silently skipped
```
**Explanation:** INSERT IGNORE turns duplicate-key errors into warnings; the third row is skipped.

**Alt1:**
```sql
INSERT INTO event_log (source, event_id, payload, logged_at)
SELECT 'web', 'evt-101', '{"page":"/home"}', NOW()
FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM event_log WHERE source = 'web' AND event_id = 'evt-101'
);
```
**Explanation:** Explicit existence check before inserting — works on every SQL dialect.

---

## Q8: ON DUPLICATE KEY UPDATE (MySQL Upsert)

*Scenario:* Upsert inventory counts — insert a new product row or add to the quantity if the SKU already exists.

*Schema hint:* `inventory(product_id INT PK, quantity INT, last_updated TIMESTAMP)`

**Query:**
```sql
INSERT INTO inventory (product_id, quantity, last_updated)
VALUES (101, 50, NOW())
ON DUPLICATE KEY UPDATE
  quantity     = quantity + VALUES(quantity),
  last_updated = NOW();
```
**Explanation:** If `product_id=101` exists, the quantity is incremented; otherwise a new row is inserted.

**Alt1 (Overwrite upsert):**
```sql
INSERT INTO inventory (product_id, quantity, last_updated)
VALUES (101, 50, NOW())
ON DUPLICATE KEY UPDATE
  quantity     = VALUES(quantity),
  last_updated = VALUES(last_updated);
```
**Explanation:** Uses VALUES() to replace rather than add — full overwrite upsert variant.

---

## Q9: INSERT ... ON CONFLICT DO UPDATE (Postgres Upsert)

*Scenario:* Upsert user preferences — set a key-value pair, overwriting any prior value.

*Schema hint:* `user_preferences(user_id INT, setting_key VARCHAR(50), setting_value TEXT, UNIQUE(user_id, setting_key))`

**Query:**
```sql
INSERT INTO user_preferences (user_id, setting_key, setting_value)
VALUES (7, 'theme', 'dark')
ON CONFLICT (user_id, setting_key)
DO UPDATE SET setting_value = EXCLUDED.setting_value;
```
**Explanation:** `EXCLUDED` refers to the row that would have been inserted; on conflict the old value is replaced.

**Alt1:**
```sql
INSERT INTO user_preferences (user_id, setting_key, setting_value)
VALUES (7, 'theme', 'dark')
ON CONFLICT (user_id, setting_key)
DO NOTHING;
```
**Explanation:** Silently discards the new value when a conflict exists — a no-op upsert.

---

## Q10: SELECT DISTINCT ON (Postgres) vs ROW_NUMBER

*Scenario:* Fetch the latest log entry per service.

*Schema hint:* `log_entries(id SERIAL PK, service VARCHAR(30), level VARCHAR(10), message TEXT, created_at TIMESTAMPTZ)`

**Query:**
```sql
SELECT DISTINCT ON (service) *
  FROM log_entries
 ORDER BY service, created_at DESC;
```
**Explanation:** Postgres-specific. Returns one row per `service` — the one with the latest `created_at`.

**Alt1 (Portable):**
```sql
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY service ORDER BY created_at DESC
  ) AS rn
  FROM log_entries
) ranked WHERE rn = 1;
```
**Explanation:** Standard SQL. Works on any database that supports window functions.

---

## Q11: Dedup Across Two Tables (Merge / Reconcile)

*Scenario:* `customers_old` and `customers_new` have overlapping records. Produce a deduplicated `customers_merged` table preferring the newer record.

*Schema hint:* Both tables share `(id INT PK, name VARCHAR, email VARCHAR, updated_at TIMESTAMP)`

**Query:**
```sql
INSERT INTO customers_merged (id, name, email, updated_at)
SELECT id, name, email, updated_at FROM customers_new
ON CONFLICT (id) DO UPDATE SET
  name       = EXCLUDED.name,
  email      = EXCLUDED.email,
  updated_at = EXCLUDED.updated_at;
```
**Explanation:** Postgres upsert merges both tables by primary key, always landing on the new data.

**Alt1 (UNION ALL + self-join delete):**
```sql
CREATE TABLE customers_merged AS
SELECT * FROM customers_old
UNION ALL
SELECT * FROM customers_new;

DELETE cm1
  FROM customers_merged cm1
  INNER JOIN customers_merged cm2
    ON  cm1.id = cm2.id
    AND cm1.updated_at < cm2.updated_at;
```
**Explanation:** UNION ALL stacks both sources, then a self-join delete keeps the latest record per id.

---

## Q12: Keep Only the Newest N Versions Per Entity

*Scenario:* Each document has many versions. Retain only the latest 3 version rows per document.

*Schema hint:* `doc_versions(id SERIAL PK, doc_id INT, content TEXT, version_num INT, created_at TIMESTAMPTZ)`

**Query:**
```sql
WITH ranked AS (
  SELECT id,
         ROW_NUMBER() OVER (
           PARTITION BY doc_id ORDER BY created_at DESC
         ) AS rn
  FROM doc_versions
)
DELETE FROM doc_versions WHERE id IN (SELECT id FROM ranked WHERE rn > 3);
```
**Explanation:** Partitions by document, ranks by recency; only rows with rn <= 3 survive.

**Alt1 (Inline view):**
```sql
DELETE dv1
  FROM doc_versions dv1
  INNER JOIN (
    SELECT id, ROW_NUMBER() OVER (
      PARTITION BY doc_id ORDER BY created_at DESC
    ) AS rn
    FROM doc_versions
  ) ranked ON dv1.id = ranked.id
WHERE ranked.rn > 3;
```
**Explanation:** Same logic with the ranked set joined in an inline view — some DBs optimise this differently.

---

## Q13: Historical Snapshots — Keep the Latest Reading Per Day Per Sensor

*Scenario:* Sensors report readings every minute. Store only the last reading per sensor per calendar day.

*Schema hint:* `sensor_data(id SERIAL PK, sensor_id INT, reading DECIMAL(8,2), recorded_at TIMESTAMPTZ)`

**Query:**
```sql
WITH ranked AS (
  SELECT id,
         ROW_NUMBER() OVER (
           PARTITION BY sensor_id, DATE(recorded_at)
           ORDER BY recorded_at DESC
         ) AS rn
  FROM sensor_data
)
DELETE FROM sensor_data WHERE id IN (SELECT id FROM ranked WHERE rn > 1);
```
**Explanation:** Partitions by sensor plus calendar day; keeps only the latest reading of each day.

**Alt1:**
```sql
DELETE sd1
  FROM sensor_data sd1
  INNER JOIN sensor_data sd2
    ON  sd1.sensor_id = sd2.sensor_id
    AND DATE(sd1.recorded_at) = DATE(sd2.recorded_at)
    AND sd1.recorded_at < sd2.recorded_at;
```
**Explanation:** Self-join on same sensor with the same day, keeping the later timestamp.

---

## Q14: Top-N Per Group with ROW_NUMBER

*Scenario:* Find the top 3 highest-paid employees in each department.

*Schema hint:* `employees(id INT PK, name VARCHAR(50), dept VARCHAR(30), salary DECIMAL(10,2))`

**Query:**
```sql
SELECT * FROM (
  SELECT *,
         ROW_NUMBER() OVER (
           PARTITION BY dept ORDER BY salary DESC
         ) AS rn
  FROM employees
) ranked
WHERE rn <= 3;
```
**Explanation:** ROW_NUMBER assigns 1..N inside each department ordered by salary; the filter keeps the top 3.

**Alt1 (Tie-inclusive):**
```sql
SELECT e.*
  FROM employees e
  INNER JOIN (
    SELECT dept, salary,
           DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS dr
    FROM employees
  ) r ON e.dept = r.dept AND e.salary = r.salary
WHERE r.dr <= 3;
```
**Explanation:** DENSE_RANK includes ties — if two people share the 3rd salary, both appear.

---

## Q15: RANK vs DENSE_RANK vs ROW_NUMBER — Choice Matrix

*Scenario:* Students have scores per subject. Compare the three ranking functions side by side before choosing one.

*Schema hint:* `scores(student_id INT, subject VARCHAR(30), score INT)`

**Query:**
```sql
SELECT
  student_id, subject, score,
  ROW_NUMBER() OVER w AS row_num,
  RANK()       OVER w AS rank_val,
  DENSE_RANK() OVER w AS dense_rank_val
FROM scores
WINDOW w AS (PARTITION BY subject ORDER BY score DESC);
```
**Explanation:** ROW_NUMBER is unique per row; RANK skips numbers after ties; DENSE_RANK never skips.

**Alt1 (Tie-inclusive practical filter):**
```sql
SELECT * FROM (
  SELECT *, DENSE_RANK() OVER (
    PARTITION BY subject ORDER BY score DESC
  ) AS dr
  FROM scores
) t WHERE dr <= 5;
```
**Explanation:** Use DENSE_RANK when "top 5" should mean the 5 best distinct scores regardless of how many people tie.

---

## Q16: Top-1 Per Group Without Window Functions (Correlated Subquery)

*Scenario:* Find the most expensive product in each category. No window functions allowed (legacy SQL).

*Schema hint:* `products(id INT PK, category VARCHAR(30), name VARCHAR(100), price DECIMAL(10,2))`

**Query:**
```sql
SELECT p.*
  FROM products p
  INNER JOIN (
    SELECT category, MAX(price) AS max_price
    FROM products
    GROUP BY category
  ) m ON p.category = m.category AND p.price = m.max_price;
```
**Explanation:** GROUP BY computes the max price per category; joining back brings the full matching rows.

**Alt1:**
```sql
SELECT * FROM products p
WHERE price = (
  SELECT MAX(price) FROM products WHERE category = p.category
);
```
**Explanation:** Correlated subquery checks each row against its category's max. Returns ties.

---

## Q17: Top-1 Per Group Using GROUP BY + Self-Join

*Scenario:* Find the best-performing sales rep in each region.

*Schema hint:* `sales_reps(id INT PK, name VARCHAR(50), region VARCHAR(30), total_sales DECIMAL(12,2))`

**Query:**
```sql
SELECT sr.*
  FROM sales_reps sr
  INNER JOIN (
    SELECT region, MAX(total_sales) AS max_sales
    FROM sales_reps
    GROUP BY region
  ) m ON sr.region = m.region AND sr.total_sales = m.max_sales;
```
**Explanation:** Identifies the max sales value per region, then retrieves the full rep record for that value.

**Alt1 (Anti-join):**
```sql
SELECT sr.*
  FROM sales_reps sr
  WHERE NOT EXISTS (
    SELECT 1 FROM sales_reps sr2
    WHERE sr2.region = sr.region AND sr2.total_sales > sr.total_sales
  );
```
**Explanation:** A row survives only if no other row in the same region has a higher sales value.

---

## Q18: Finding the SECOND Record Per Group

*Scenario:* For each customer, find their second order by date.

*Schema hint:* `orders(order_id INT PK, customer_id INT, order_date DATE, total DECIMAL(10,2))`

**Query:**
```sql
SELECT * FROM (
  SELECT *,
         ROW_NUMBER() OVER (
           PARTITION BY customer_id ORDER BY order_date, order_id
         ) AS rn
  FROM orders
) ranked
WHERE rn = 2;
```
**Explanation:** ROW_NUMBER assigns positions 1, 2, 3... per customer by date; the filter isolates position 2.

**Alt1 (No window function):**
```sql
SELECT o.*
  FROM orders o
  INNER JOIN (
    SELECT customer_id, MIN(order_date) AS second_date
    FROM orders o1
    WHERE order_date > (
      SELECT MIN(order_date) FROM orders o2
      WHERE o2.customer_id = o1.customer_id
    )
    GROUP BY customer_id
  ) s ON o.customer_id = s.customer_id AND o.order_date = s.second_date;
```
**Explanation:** Finds each customer's minimum date that is strictly after their first date — the second order.

---

## Q19: Select All Rows of Top-Scoring Group Members

*Scenario:* Identify the top 3 customers by lifetime value, then retrieve ALL of their orders (multiple rows per member).

*Schema hint:* `customers(id INT PK, name VARCHAR, total_value DECIMAL)`, `orders(id INT PK, customer_id INT, amount DECIMAL, order_date DATE)`

**Query:**
```sql
WITH top_customers AS (
  SELECT id FROM (
    SELECT id, DENSE_RANK() OVER (ORDER BY total_value DESC) AS dr
    FROM customers
  ) r WHERE dr <= 3
)
SELECT o.*
  FROM orders o
  INNER JOIN top_customers tc ON o.customer_id = tc.id
 ORDER BY o.customer_id, o.order_date;
```
**Explanation:** CTE isolates the top-3 customer ids, then a join pulls all their orders (many rows per customer).

**Alt1:**
```sql
SELECT o.*
  FROM orders o
  WHERE o.customer_id IN (
    SELECT id FROM customers
     ORDER BY total_value DESC
     LIMIT 3
  )
 ORDER BY o.customer_id, o.order_date;
```
**Explanation:** IN-list subquery with LIMIT picks the top-3 customers; all their orders are returned.

---

## Q20: Top-N Per Composite Key (Top 2 Products Per Category Per Month)

*Scenario:* For each (category, month) combination, find the top 2 products by revenue.

*Schema hint:* `product_revenue(id INT PK, product_id INT, category VARCHAR(30), month DATE, revenue DECIMAL(12,2))`

**Query:**
```sql
SELECT * FROM (
  SELECT *,
         ROW_NUMBER() OVER (
           PARTITION BY category, DATE_FORMAT(month, '%Y-%m')
           ORDER BY revenue DESC
         ) AS rn
  FROM product_revenue
) ranked
WHERE rn <= 2;
```
**Explanation:** A two-column PARTITION BY creates (category, month) groups; ROW_NUMBER ranks inside each one.

**Alt1 (Tie-inclusive):**
```sql
SELECT pr.*
  FROM product_revenue pr
  INNER JOIN (
    SELECT category,
           DATE_FORMAT(month, '%Y-%m') AS ym,
           revenue,
           DENSE_RANK() OVER (
             PARTITION BY category, DATE_FORMAT(month, '%Y-%m')
             ORDER BY revenue DESC
           ) AS dr
    FROM product_revenue
  ) r ON pr.category = r.category
     AND DATE_FORMAT(pr.month, '%Y-%m') = r.ym
     AND pr.revenue = r.revenue
WHERE r.dr <= 2;
```
**Explanation:** DENSE_RANK variant that includes ties for the 2nd position as well.

---

## Q21: Bottom-N Per Group

*Scenario:* Find the bottom 2 lowest-scoring students in each subject.

*Schema hint:* `exam_results(id INT PK, student_id INT, subject VARCHAR(30), score INT)`

**Query:**
```sql
SELECT * FROM (
  SELECT *,
         ROW_NUMBER() OVER (
           PARTITION BY subject ORDER BY score ASC, id ASC
         ) AS rn
  FROM exam_results
) ranked
WHERE rn <= 2;
```
**Explanation:** ORDER BY ASC flips the ranking so the lowest scores receive rn=1 and 2.

**Alt1:**
```sql
SELECT er.*
  FROM exam_results er
  INNER JOIN (
    SELECT subject, MIN(score) AS min_score
    FROM exam_results
    GROUP BY subject
  ) m ON er.subject = m.subject AND er.score = m.min_score;
```
**Explanation:** GROUP BY + MIN finds the absolute lowest score per subject — returns ties at the bottom.

---

## Q22: Handling Ties in Top-N

*Scenario:* Race results — when two runners tie for 3rd place, both should appear in the "top 3".

*Schema hint:* `race_results(id INT PK, runner VARCHAR(50), race VARCHAR(30), position INT)`

**Query:**
```sql
SELECT * FROM (
  SELECT *,
         DENSE_RANK() OVER (
           PARTITION BY race ORDER BY position ASC
         ) AS dr
  FROM race_results
) ranked
WHERE dr <= 3;
```
**Explanation:** DENSE_RANK counts distinct positions, so every runner tied at position 3 is included.

**Alt1 (Explicit tie handling):**
```sql
SELECT rr.*
  FROM race_results rr
  WHERE rr.position <= 3
     OR rr.id IN (
       SELECT rr2.id FROM race_results rr2
       WHERE rr2.race = rr.race AND rr2.position = 3
         AND rr2.id <> rr.id
     );
```
**Explanation:** Keeps everything at position <= 3 plus any extra runners tied at exactly position 3.

---

## Q23: Dedup While Preserving Ordinal Ranking

*Scenario:* A task list has duplicate task names within categories. After dedup, re-sequence the position column.

*Schema hint:* `task_list(id INT PK, task_name VARCHAR(100), category VARCHAR(30), position INT)`

**Query:**
```sql
WITH resequenced AS (
  SELECT category, task_name,
         ROW_NUMBER() OVER (
           PARTITION BY category ORDER BY MIN(position)
         ) AS new_position
  FROM task_list
  GROUP BY category, task_name
)
UPDATE task_list t
INNER JOIN resequenced r
  ON  t.category  = r.category
  AND t.task_name = r.task_name
SET t.position = r.new_position;
```
**Explanation:** GROUP BY collapses duplicates first; ROW_NUMBER re-assigns ordinal positions within each category.

**Alt1 (New-table swap):**
```sql
CREATE TABLE task_list_clean AS
SELECT category, task_name,
       ROW_NUMBER() OVER (PARTITION BY category ORDER BY MIN(position)) AS position
FROM task_list
GROUP BY category, task_name;

TRUNCATE TABLE task_list;
INSERT INTO task_list (task_name, category, position)
SELECT task_name, category, position FROM task_list_clean;
DROP TABLE task_list_clean;
```
**Explanation:** Builds a clean table with re-sequenced positions, then replaces the original table.

---

## Q24: Unique Index as Enforced Deduplication

*Scenario:* Stop duplicate registrations at the database level using a unique index rather than relying on app logic.

*Schema hint:* `registrations(id INT PK, event_id INT, attendee_email VARCHAR(255))`

**Query:**
```sql
CREATE UNIQUE INDEX uq_event_email ON registrations (event_id, attendee_email);

INSERT IGNORE INTO registrations (event_id, attendee_email)
VALUES (42, 'alice@example.com');
```
**Explanation:** Unique index prevents duplicates at the storage level; INSERT IGNORE makes the skip explicit.

**Alt1 (Postgres):**
```sql
INSERT INTO registrations (event_id, attendee_email)
VALUES (42, 'alice@example.com')
ON CONFLICT (event_id, attendee_email) DO NOTHING;
```
**Explanation:** Postgres ON CONFLICT DO NOTHING provides the same skip-on-duplicate behaviour.

**Alt2 (Dialect-agnostic gate):**
```sql
INSERT INTO registrations (event_id, attendee_email)
SELECT 42, 'alice@example.com'
WHERE NOT EXISTS (
  SELECT 1 FROM registrations
  WHERE event_id = 42 AND attendee_email = 'alice@example.com'
);
```
**Explanation:** Pre-checks existence in a WHERE — portable across every SQL dialect.

---

## Q25: Deleting Orphan Rows After Foreign Key (No Matching Parent)

*Scenario:* `order_items` references `orders` via FK, but some parent orders were removed, leaving orphaned items.

*Schema hint:* `order_items(id INT PK, order_id INT, product VARCHAR, qty INT)`, `orders(id INT PK, ...)`

**Query:**
```sql
DELETE oi
  FROM order_items oi
  LEFT JOIN orders o ON oi.order_id = o.id
 WHERE o.id IS NULL;
```
**Explanation:** LEFT JOIN finds items whose order_id has no matching parent; those orphans get deleted.

**Alt1 (NOT IN):**
```sql
DELETE FROM order_items
WHERE order_id NOT IN (SELECT id FROM orders);
```
**Explanation:** NOT IN subquery identifies orphaned order_ids. Beware: fails if `orders.id` ever contains NULL.

**Alt2 (NOT EXISTS — NULL-safe):**
```sql
DELETE FROM order_items
WHERE NOT EXISTS (
  SELECT 1 FROM orders WHERE orders.id = order_items.order_id
);
```
**Explanation:** Correlated NOT EXISTS handles NULLs safely — the most robust orphan-deletion pattern.

---

## Q26: Cleaning Name Variations (Case / Whitespace) as Dedup

*Scenario:* `contacts` has the same person stored as 'John Smith', 'john smith', and 'John  Smith' (extra spaces). Normalise before dedup.

*Schema hint:* `contacts(id INT PK, full_name VARCHAR(100), email VARCHAR(255))`

**Query:**
```sql
WITH normalised AS (
  SELECT id,
         LOWER(TRIM(REGEXP_REPLACE(full_name, '\\s+', ' '))) AS norm_name,
         email,
         ROW_NUMBER() OVER (
           PARTITION BY LOWER(TRIM(REGEXP_REPLACE(full_name, '\\s+', ' '))), email
           ORDER BY id
         ) AS rn
  FROM contacts
)
DELETE FROM contacts WHERE id IN (SELECT id FROM normalised WHERE rn > 1);
```
**Explanation:** Collapses internal whitespace and lowercases before partitioning, so name case/spacing variants collapse into one group.

**Alt1 (Find-first diagnostic):**
```sql
SELECT MIN(id) AS keep_id,
       LOWER(TRIM(REGEXP_REPLACE(full_name, '\\s+', ' '))) AS norm_name,
       email
  FROM contacts
 GROUP BY LOWER(TRIM(REGEXP_REPLACE(full_name, '\\s+', ' '))), email
HAVING COUNT(*) > 1;
```
**Explanation:** Find step that lists every normalised group containing more than one row — verify before deleting.

---

## Q27: Time-Series Dedup — Same Reading Within a 5-Minute Window

*Scenario:* A sensor may retry and report the same value twice within a 5-minute window. Keep only the first reading of each window.

*Schema hint:* `metrics(id SERIAL PK, device_id INT, value DECIMAL(10,4), ts TIMESTAMPTZ)`

**Query:**
```sql
WITH flagged AS (
  SELECT id, device_id, value, ts,
         LAG(value) OVER (PARTITION BY device_id ORDER BY ts)  AS prev_value,
         LAG(ts)    OVER (PARTITION BY device_id ORDER BY ts)  AS prev_ts
  FROM metrics
)
DELETE FROM metrics
WHERE id IN (
  SELECT id FROM flagged
  WHERE value = prev_value
    AND ts - prev_ts < INTERVAL '5 minutes'
);
```
**Explanation:** LAG exposes the previous reading; a duplicate is any row with the same value arriving within 5 minutes of the prior one.

**Alt1 (Self-join):**
```sql
DELETE m1
  FROM metrics m1
  INNER JOIN metrics m2
    ON  m1.device_id = m2.device_id
    AND m1.value     = m2.value
    AND m1.ts        > m2.ts
    AND m1.ts        <= m2.ts + INTERVAL '5 minutes';
```
**Explanation:** Self-joins each row with earlier same-value rows from the same device within the 5-minute window.

---

## Q28: Top-N Per Group — Keeping ALL Tied Rows at the Boundary

*Scenario:* Find the top 3 products per category by revenue. If products tie at rank 3, include every tied product.

*Schema hint:* `product_sales(product_id INT PK, category VARCHAR(30), revenue DECIMAL(12,2))`

**Query:**
```sql
SELECT * FROM (
  SELECT *,
         DENSE_RANK() OVER (
           PARTITION BY category ORDER BY revenue DESC
         ) AS dr
  FROM product_sales
) ranked
WHERE dr <= 3;
```
**Explanation:** DENSE_RANK counts distinct revenue values, so every product tied at the 3rd distinct value appears.

**Alt1 (Group + join):**
```sql
SELECT ps.*
  FROM product_sales ps
  INNER JOIN (
    SELECT category, revenue,
           DENSE_RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS dr
    FROM product_sales
    GROUP BY category, revenue
  ) r ON ps.category = r.category AND ps.revenue = r.revenue
WHERE r.dr <= 3;
```
**Explanation:** First ranks only the distinct (category, revenue) pairs, then joins full product rows back in.

---

## Q29: Multi-Column Dedup with NULL Handling

*Scenario:* `addresses` contains duplicate (street, city, zip) groups, but NULLs complicate equality (NULL <> NULL).

*Schema hint:* `addresses(id INT PK, street VARCHAR(100), city VARCHAR(50), zip VARCHAR(10))`

**Query:**
```sql
WITH normalised AS (
  SELECT id,
         COALESCE(UPPER(TRIM(street)), '___NULL___') AS n_street,
         COALESCE(UPPER(TRIM(city)),   '___NULL___') AS n_city,
         COALESCE(TRIM(zip),           '___NULL___') AS n_zip,
         ROW_NUMBER() OVER (
           PARTITION BY
             COALESCE(UPPER(TRIM(street)), '___NULL___'),
             COALESCE(UPPER(TRIM(city)),   '___NULL___'),
             COALESCE(TRIM(zip),           '___NULL___')
           ORDER BY id
         ) AS rn
  FROM addresses
)
DELETE FROM addresses WHERE id IN (SELECT id FROM normalised WHERE rn > 1);
```
**Explanation:** COALESCE swaps NULLs for a sentinel string so PARTITION BY treats equal NULLs as one group.

**Alt1 (Self-join with NULL-safe equality):**
```sql
DELETE a1
  FROM addresses a1
  INNER JOIN addresses a2
    ON  COALESCE(UPPER(TRIM(a1.street)), '') = COALESCE(UPPER(TRIM(a2.street)), '')
    AND COALESCE(UPPER(TRIM(a1.city)),   '') = COALESCE(UPPER(TRIM(a2.city)),   '')
    AND COALESCE(TRIM(a1.zip),           '') = COALESCE(TRIM(a2.zip),           '')
    AND a1.id > a2.id;
```
**Explanation:** Self-join with COALESCE-to-empty-string makes NULL-safe comparisons without window functions.

---

## Q30: Find-Then-Delete Pattern Using GROUP BY + HAVING COUNT

*Scenario:* Classic interview sequence: first find duplicate groups, then remove all but one row from each.

*Schema hint:* `payments(id INT PK, txn_code VARCHAR(20), payer_id INT, amount DECIMAL(10,2))`

**Query:**
```sql
-- Step 1: identify duplicate groups
SELECT txn_code, payer_id, COUNT(*) AS cnt
  FROM payments
 GROUP BY txn_code, payer_id
HAVING COUNT(*) > 1;

-- Step 2: delete all but the lowest id in each duplicate group
DELETE p1
  FROM payments p1
  INNER JOIN (
    SELECT txn_code, payer_id, MIN(id) AS keep_id
      FROM payments
     GROUP BY txn_code, payer_id
    HAVING COUNT(*) > 1
  ) dup ON p1.txn_code = dup.txn_code
       AND p1.payer_id = dup.payer_id
       AND p1.id       <> dup.keep_id;
```
**Explanation:** Step 1 lists duplicate groups; Step 2 deletes everything inside those groups except the MIN(id) row.

**Alt1 (NOT IN against canonical ids):**
```sql
DELETE FROM payments
WHERE id NOT IN (
  SELECT keep_id FROM (
    SELECT MIN(id) AS keep_id
      FROM payments
     GROUP BY txn_code, payer_id
  ) t
);
```
**Explanation:** Subquery computes one canonical id per group; NOT IN deletes all others. The extra wrapper avoids MySQL's "can't specify target table" error.

---

## Q31: Nested Top-N — Top Departments Then Top Employees Within

*Scenario:* First identify the top 3 departments by total salary, then list the top 2 earners inside each of those departments.

*Schema hint:* `employees(id INT PK, name VARCHAR(50), dept VARCHAR(30), salary DECIMAL(10,2))`

**Query:**
```sql
WITH dept_totals AS (
  SELECT dept, SUM(salary) AS total_salary,
         DENSE_RANK() OVER (ORDER BY SUM(salary) DESC) AS dept_rank
  FROM employees
  GROUP BY dept
),
top_depts AS (
  SELECT dept FROM dept_totals WHERE dept_rank <= 3
),
ranked_emps AS (
  SELECT e.*, ROW_NUMBER() OVER (
    PARTITION BY e.dept ORDER BY e.salary DESC
  ) AS emp_rank
  FROM employees e
  INNER JOIN top_depts td ON e.dept = td.dept
)
SELECT * FROM ranked_emps WHERE emp_rank <= 2;
```
**Explanation:** CTE pipeline: compute dept totals -> rank departments -> keep top 3 -> rank employees inside them -> keep top 2.

**Alt1 (Subquery with OFFSET):**
```sql
SELECT e.*
  FROM employees e
  INNER JOIN (
    SELECT dept FROM employees GROUP BY dept
     ORDER BY SUM(salary) DESC LIMIT 3
  ) td ON e.dept = td.dept
  WHERE e.salary >= (
    SELECT DISTINCT salary FROM employees e2
    WHERE e2.dept = e.dept
     ORDER BY salary DESC LIMIT 1 OFFSET 1
  );
```
**Explanation:** LIMIT ranks departments; OFFSET 1 finds the 2nd-highest salary threshold per department.

---

## Q32: Running Dedup on an Append-Only Event Log

*Scenario:* An append-only `event_log` receives duplicates. Dedup only events older than 24 hours because recent events may still arrive out of order.

*Schema hint:* `event_log(id BIGINT PK, event_id VARCHAR(50), source VARCHAR(30), payload JSON, logged_at TIMESTAMPTZ)`

**Query:**
```sql
WITH old_events AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY event_id, source ORDER BY logged_at
  ) AS rn
  FROM event_log
  WHERE logged_at < NOW() - INTERVAL '24 hours'
)
DELETE FROM event_log
WHERE id IN (SELECT id FROM old_events WHERE rn > 1);
```
**Explanation:** Only processing data older than 24h protects in-flight late arrivals; dedup keys on (event_id, source).

**Alt1 (EXISTS correlation):**
```sql
DELETE el1
  FROM event_log el1
  WHERE el1.logged_at < NOW() - INTERVAL '24 hours'
    AND EXISTS (
      SELECT 1 FROM event_log el2
      WHERE el2.event_id = el1.event_id
        AND el2.source   = el1.source
        AND el2.logged_at < el1.logged_at
    );
```
**Explanation:** Exists only when an earlier row with the same key exists — delete the later duplicate.

---

## Q33: Dedup on an Entity-Attribute-Value (EAV) Schema

*Scenario:* An EAV table has multiple value rows per (entity, attribute). Keep only the most recent value.

*Schema hint:* `entity_attrs(id SERIAL PK, entity_id INT, attr_name VARCHAR(50), attr_value TEXT, updated_at TIMESTAMPTZ)`

**Query:**
```sql
WITH ranked AS (
  SELECT id, ROW_NUMBER() OVER (
    PARTITION BY entity_id, attr_name ORDER BY updated_at DESC
  ) AS rn
  FROM entity_attrs
)
DELETE FROM entity_attrs WHERE id IN (SELECT id FROM ranked WHERE rn > 1);
```
**Explanation:** EAV dedup is the same pattern as any column dedup — partition by the logical key (entity + attribute).

**Alt1:**
```sql
DELETE ea1
  FROM entity_attrs ea1
  INNER JOIN entity_attrs ea2
    ON  ea1.entity_id = ea2.entity_id
    AND ea1.attr_name = ea2.attr_name
    AND ea1.updated_at < ea2.updated_at;
```
**Explanation:** Self-join keeps the row with the later `updated_at` per (entity, attribute) pair.

---

## Q34: Fuzzy Dedup Using SOUNDEX

*Scenario:* `companies` has near-duplicates like 'Acme Corp' and 'ACME Corporation'. Use phonetic SOUNDEX keys to merge them.

*Schema hint:* `companies(id INT PK, name VARCHAR(100), city VARCHAR(50), founded_year INT)`

**Query:**
```sql
WITH phonetic AS (
  SELECT id, name, city, founded_year,
         SOUNDEX(name) AS sndx,
         ROW_NUMBER() OVER (
           PARTITION BY SOUNDEX(name), city ORDER BY id
         ) AS rn
  FROM companies
)
DELETE FROM companies WHERE id IN (SELECT id FROM phonetic WHERE rn > 1);
```
**Explanation:** SOUNDEX converts names to a phonetic code; names sharing a code and city are treated as duplicates.

**Alt1 (Postgres Levenshtein):**
```sql
DELETE FROM companies
WHERE id IN (
  SELECT c2.id
    FROM companies c1
    INNER JOIN companies c2
      ON  c1.city = c2.city
      AND c1.id < c2.id
      AND levenshtein(LOWER(c1.name), LOWER(c2.name)) <= 2
);
```
**Explanation:** Delete the higher-id record when two names in the same city differ by at most 2 edit operations.

---

## Q35: Top-N Per Group With Pre-Filter (Only Active Records)

*Scenario:* Top 3 salespeople per region, counting only active employees.

*Schema hint:* `sales_team(id INT PK, name VARCHAR(50), region VARCHAR(30), sales DECIMAL(12,2), is_active BOOLEAN)`

**Query:**
```sql
SELECT * FROM (
  SELECT *,
         ROW_NUMBER() OVER (
           PARTITION BY region ORDER BY sales DESC
         ) AS rn
  FROM sales_team
  WHERE is_active = TRUE
) ranked
WHERE rn <= 3;
```
**Explanation:** Inactive rows are filtered out before windowing, so rankings reflect only active people.

**Alt1 (Correlated count):**
```sql
SELECT st.*
  FROM sales_team st
  WHERE st.is_active = TRUE
    AND (
      SELECT COUNT(*) FROM sales_team st2
      WHERE st2.region      = st.region
        AND st2.is_active   = TRUE
        AND st2.sales       > st.sales
    ) < 3;
```
**Explanation:** Include a person when fewer than 3 active colleagues in the same region have higher sales.

---

## Q36: Delete Duplicates — Keep the Row With the Most Non-NULL Values

*Scenario:* `leads` has duplicate emails. When choosing which row to keep, prefer the most complete record.

*Schema hint:* `leads(id INT PK, email VARCHAR(255), name VARCHAR(100), phone VARCHAR(20), company VARCHAR(100), source VARCHAR(30))`

**Query:**
```sql
DELETE FROM leads
WHERE id IN (
  SELECT id FROM (
    SELECT id,
           ROW_NUMBER() OVER (
             PARTITION BY LOWER(email)
             ORDER BY
               (CASE WHEN name    IS NOT NULL THEN 1 ELSE 0 END +
                CASE WHEN phone   IS NOT NULL THEN 1 ELSE 0 END +
                CASE WHEN company IS NOT NULL THEN 1 ELSE 0 END +
                CASE WHEN source  IS NOT NULL THEN 1 ELSE 0 END) DESC,
               id DESC
           ) AS rn
    FROM leads
  ) t WHERE rn > 1
);
```
**Explanation:** Rows are scored by how many optional columns are populated; the most complete row per email wins.

**Alt1 (Self-join + completeness):**
```sql
DELETE l1
  FROM leads l1
  INNER JOIN leads l2
    ON  LOWER(l1.email) = LOWER(l2.email)
    AND (
      (COALESCE(l2.name IS NOT NULL,0) + COALESCE(l2.phone IS NOT NULL,0) +
       COALESCE(l2.company IS NOT NULL,0) + COALESCE(l2.source IS NOT NULL,0))
      >
      (COALESCE(l1.name IS NOT NULL,0) + COALESCE(l1.phone IS NOT NULL,0) +
       COALESCE(l1.company IS NOT NULL,0) + COALESCE(l1.source IS NOT NULL,0))
    );
```
**Explanation:** Deletes l1 whenever l2 has more populated fields for the same email address.

---

## Q37: Top-1 Per Group From Multiple Candidate Tables

*Scenario:* For each student, find the best score, whether it comes from the `midterm` or the `final` exam table.

*Schema hint:* `midterm(student_id INT PK, score INT)`, `final(student_id INT PK, score INT)`

**Query:**
```sql
WITH combined AS (
  SELECT student_id, score, 'midterm' AS source FROM midterm
  UNION ALL
  SELECT student_id, score, 'final'   AS source FROM final
),
ranked AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY student_id ORDER BY score DESC
  ) AS rn
  FROM combined
)
SELECT student_id, score, source FROM ranked WHERE rn = 1;
```
**Explanation:** UNION ALL merges both exam tables; ROW_NUMBER picks the higher score per student.

**Alt1 (FULL OUTER JOIN + GREATEST):**
```sql
SELECT COALESCE(m.student_id, f.student_id) AS student_id,
       GREATEST(COALESCE(m.score, 0), COALESCE(f.score, 0)) AS best_score
  FROM midterm m
  FULL OUTER JOIN final f ON m.student_id = f.student_id;
```
**Explanation:** FULL OUTER JOIN aligns both scores per student; GREATEST selects the higher value.

---

## Q38: Dedup Inside a CTE That Feeds Further Analysis

*Scenario:* Deduplicate transactions first, then compute monthly totals per customer from the clean set.

*Schema hint:* `transactions(id INT PK, customer_id INT, amount DECIMAL(10,2), txn_date DATE)`

**Query:**
```sql
WITH unique_txns AS (
  SELECT *,
         ROW_NUMBER() OVER (
           PARTITION BY customer_id, amount, txn_date ORDER BY id
         ) AS rn
  FROM transactions
)
SELECT customer_id,
       DATE_FORMAT(txn_date, '%Y-%m') AS month,
       SUM(amount) AS monthly_total
  FROM unique_txns
 WHERE rn = 1
 GROUP BY customer_id, DATE_FORMAT(txn_date, '%Y-%m')
 ORDER BY customer_id, month;
```
**Explanation:** The CTE deduplicates first; downstream aggregation runs only on clean rows.

**Alt1 (Exclude dup ids):**
```sql
WITH dup_ids AS (
  SELECT id FROM (
    SELECT id, ROW_NUMBER() OVER (
      PARTITION BY customer_id, amount, txn_date ORDER BY id
    ) AS rn
    FROM transactions
  ) t WHERE rn > 1
)
SELECT customer_id,
       DATE_FORMAT(txn_date, '%Y-%m') AS month,
       SUM(amount) AS monthly_total
  FROM transactions
 WHERE id NOT IN (SELECT id FROM dup_ids)
 GROUP BY customer_id, DATE_FORMAT(txn_date, '%Y-%m');
```
**Explanation:** Identifies duplicate ids in a CTE, then aggregates the base table while excluding them.

---

## Q39: Top-N Per Group With OFFSET/LIMIT Pagination

*Scenario:* Page through the top 10 products per category, 5 at a time (page 2 = rows 6-10).

*Schema hint:* `products(id INT PK, category VARCHAR(30), name VARCHAR(100), rating DECIMAL(3,2))`

**Query:**
```sql
SELECT * FROM (
  SELECT *,
         ROW_NUMBER() OVER (
           PARTITION BY category ORDER BY rating DESC
         ) AS rn
  FROM products
) ranked
WHERE rn BETWEEN 6 AND 10;
```
**Explanation:** ROW_NUMBER yields a stable in-group position; BETWEEN implements offset (5) and limit (5) per category.

**Alt1 (LIMIT/OFFSET suffix):**
```sql
SELECT *
  FROM (
    SELECT *, ROW_NUMBER() OVER (
      PARTITION BY category ORDER BY rating DESC
    ) AS rn
    FROM products
  ) ranked
 WHERE rn > 5
 LIMIT 5;
```
**Explanation:** Cleaner offset limit after windowing — the LIMIT applies across the whole ranked set.

---

## Q40: Dedup With Custom Business Priority Rules

*Scenario:* When duplicates exist in `orders`, keep the order from the highest-priority channel (web > app > api > email).

*Schema hint:* `orders(id INT PK, customer_id INT, product VARCHAR(30), channel VARCHAR(10), created_at TIMESTAMP)`

**Query:**
```sql
WITH prioritised AS (
  SELECT *,
         ROW_NUMBER() OVER (
           PARTITION BY customer_id, product
           ORDER BY
             CASE channel
               WHEN 'web'   THEN 1
               WHEN 'app'   THEN 2
               WHEN 'api'   THEN 3
               WHEN 'email' THEN 4
               ELSE 5
             END,
             created_at DESC
         ) AS rn
  FROM orders
)
DELETE FROM orders WHERE id IN (SELECT id FROM prioritised WHERE rn > 1);
```
**Explanation:** A CASE-declared priority drives the window ORDER BY; channel priority then recency decides the keeper.

**Alt1 (FIELD-based join, MySQL):**
```sql
DELETE o1
  FROM orders o1
  INNER JOIN orders o2
    ON  o1.customer_id = o2.customer_id
    AND o1.product     = o2.product
    AND (
      FIELD(o1.channel, 'email','api','app','web') < FIELD(o2.channel, 'email','api','app','web')
      OR (o1.channel = o2.channel AND o1.created_at < o2.created_at)
    );
```
**Explanation:** MySQL FIELD() reverses the priority weights; self-join keeps the higher-priority (or newer) row.

---

## Q41: Top-N With Aggregation Tiebreaker (COUNT then SUM)

*Scenario:* Rank employees by number of deals closed; break ties by total deal value.

*Schema hint:* `deals(id INT PK, employee_id INT, deal_value DECIMAL(12,2), closed_date DATE)`

**Query:**
```sql
WITH stats AS (
  SELECT employee_id,
         COUNT(*)       AS deal_count,
         SUM(deal_value) AS total_value
  FROM deals
  GROUP BY employee_id
),
ranked AS (
  SELECT *,
         ROW_NUMBER() OVER (
           ORDER BY deal_count DESC, total_value DESC
         ) AS rn
  FROM stats
)
SELECT * FROM ranked WHERE rn <= 5;
```
**Explanation:** Aggregates first, then ranks by deal count DESC with total value DESC as the tiebreaker.

**Alt1 (RANK to allow ties):**
```sql
SELECT employee_id, deal_count, total_value
  FROM (
    SELECT employee_id,
           COUNT(*)        AS deal_count,
           SUM(deal_value) AS total_value,
           RANK() OVER (ORDER BY COUNT(*) DESC, SUM(deal_value) DESC) AS r
    FROM deals
    GROUP BY employee_id
  ) t
WHERE r <= 5;
```
**Explanation:** RANK in the grouped select lets employees with identical count+value share a rank.

---

## Q42: Recursive CTE Dedup for Hierarchical Data

*Scenario:* An org chart has duplicate employee entries at different levels. Dedup by email while keeping the tree connected.

*Schema hint:* `org_tree(id INT PK, employee_name VARCHAR(100), email VARCHAR(255), manager_id INT)` (recursive via manager_id)

**Query:**
```sql
WITH RECURSIVE tree AS (
  SELECT id, employee_name, email, manager_id, 0 AS depth
  FROM org_tree WHERE manager_id IS NULL
  UNION ALL
  SELECT t.id, t.employee_name, t.email, t.manager_id, tree.depth + 1
  FROM org_tree t INNER JOIN tree ON t.manager_id = tree.id
),
ranked AS (
  SELECT id, ROW_NUMBER() OVER (
    PARTITION BY LOWER(email) ORDER BY depth, id
  ) AS rn
  FROM tree
)
DELETE FROM org_tree WHERE id IN (SELECT id FROM ranked WHERE rn > 1);
```
**Explanation:** BFS depth order lets the shallowest record per email survive, preserving the tree's root structure.

**Alt1 (GROUP BY canonical ids):**
```sql
DELETE FROM org_tree
WHERE id NOT IN (
  SELECT id FROM (
    SELECT MIN(id) AS id FROM org_tree GROUP BY LOWER(email)
  ) t
);
```
**Explanation:** Keeps the MIN(id) per email and removes all other rows — simpler but ignores tree depth.

---

## Q43: Dedup Keeping the Most Complete Contact Record

*Scenario:* Merge duplicate contact records, preferring the row with the fewest NULL columns.

*Schema hint:* `contacts(id INT PK, first_name VARCHAR(50), last_name VARCHAR(50), phone VARCHAR(20), email VARCHAR(255), address TEXT)`

**Query:**
```sql
WITH scored AS (
  SELECT id, first_name, last_name,
         (CASE WHEN phone   IS NOT NULL THEN 1 ELSE 0 END +
          CASE WHEN email   IS NOT NULL THEN 1 ELSE 0 END +
          CASE WHEN address IS NOT NULL THEN 1 ELSE 0 END) AS filled_cols,
         ROW_NUMBER() OVER (
           PARTITION BY LOWER(first_name), LOWER(last_name)
           ORDER BY
             (CASE WHEN phone IS NOT NULL THEN 1 ELSE 0 END +
              CASE WHEN email IS NOT NULL THEN 1 ELSE 0 END +
              CASE WHEN address IS NOT NULL THEN 1 ELSE 0 END) DESC,
             id ASC
         ) AS rn
  FROM contacts
)
DELETE FROM contacts WHERE id IN (SELECT id FROM scored WHERE rn > 1);
```
**Explanation:** Each row counts how many optional columns are filled; the best-filled record survives.

**Alt1 (Self-join + completeness comparison):**
```sql
DELETE c1
  FROM contacts c1
  INNER JOIN contacts c2
    ON  LOWER(c1.first_name) = LOWER(c2.first_name)
    AND LOWER(c1.last_name)  = LOWER(c2.last_name)
    AND (
      (COALESCE(c2.email   IS NOT NULL,0) + COALESCE(c2.phone IS NOT NULL,0) +
       COALESCE(c2.address IS NOT NULL,0))
      >
      (COALESCE(c1.email   IS NOT NULL,0) + COALESCE(c1.phone IS NOT NULL,0) +
       COALESCE(c1.address IS NOT NULL,0))
    );
```
**Explanation:** Self-join deletes c1 whenever c2 is more complete for the same name pair.

---

## Q44: Top-N Per Group Using LATERAL Join (Postgres)

*Scenario:* For each department, fetch the 3 most recent hires. LATERAL gives efficient per-group access.

*Schema hint:* `employees(id INT PK, name VARCHAR, dept VARCHAR, hire_date DATE)`

**Query:**
```sql
SELECT d.dept, e.*
  FROM (SELECT DISTINCT dept FROM employees) d
  CROSS JOIN LATERAL (
    SELECT * FROM employees
    WHERE dept = d.dept
    ORDER BY hire_date DESC
    LIMIT 3
  ) e;
```
**Explanation:** LATERAL runs the correlated subquery once per department; an index on (dept, hire_date) makes it fast.

**Alt1 (Window function):**
```sql
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY dept ORDER BY hire_date DESC
  ) AS rn
  FROM employees
) t WHERE rn <= 3;
```
**Explanation:** Simpler but typically scans the whole table before ranking.

---

## Q45: Top-N Per Group Using CROSS APPLY (SQL Server)

*Scenario:* SQL Server's CROSS APPLY is the equivalent of Postgres LATERAL. Fetch the top 3 orders per customer.

*Schema hint:* `orders(order_id INT PK, customer_id INT, order_date DATE, total DECIMAL(10,2))`

**Query:**
```sql
SELECT c.customer_id, c.name, o.*
  FROM customers c
  CROSS APPLY (
    SELECT TOP 3 *
    FROM orders
    WHERE customer_id = c.customer_id
    ORDER BY order_date DESC
  ) o;
```
**Explanation:** CROSS APPLY evaluates the inner query per customer row; TOP 3 caps each customer's result set.

**Alt1 (Portable ROW_NUMBER):**
```sql
SELECT * FROM (
  SELECT o.*, ROW_NUMBER() OVER (
    PARTITION BY o.customer_id ORDER BY o.order_date DESC
  ) AS rn
  FROM orders o
) ranked
WHERE rn <= 3;
```
**Explanation:** Standard window-function approach — portable across every modern SQL database.

---

## Q46: Dedup Consecutive Identical Values With LAG

*Scenario:* In a metrics stream, remove a reading when the previous reading from the same device is identical.

*Schema hint:* `readings(id SERIAL PK, device_id INT, value DECIMAL(10,3), ts TIMESTAMPTZ)`

**Query:**
```sql
WITH with_prev AS (
  SELECT id, device_id, value, ts,
         LAG(value) OVER (
           PARTITION BY device_id ORDER BY ts
         ) AS prev_value
  FROM readings
)
DELETE FROM readings
WHERE id IN (
  SELECT id FROM with_prev WHERE value = prev_value
);
```
**Explanation:** LAG reads the previous row's value; identical consecutive values are flagged and deleted.

**Alt1 (No window — strict predecessor check):**
```sql
DELETE r1
  FROM readings r1
  INNER JOIN readings r2
    ON  r1.device_id = r2.device_id
    AND r1.value     = r2.value
    AND r1.ts        > r2.ts
    AND NOT EXISTS (
      SELECT 1 FROM readings r3
      WHERE r3.device_id = r1.device_id
        AND r3.ts > r2.ts AND r3.ts < r1.ts
    );
```
**Explanation:** Deletes a row only when the immediately preceding reading (no middle row) has the same value.

---

## Q47: Slowly Changing Dimension (SCD) Dedup — Enforce One Current Row Per Customer

*Scenario:* `customer_dim` is an SCD Type-2 table. Verify and enforce that one row is marked current per customer.

*Schema hint:* `customer_dim(id INT PK, customer_id INT, name VARCHAR, email VARCHAR, valid_from DATE, valid_to DATE, is_current BOOLEAN)`

**Query:**
```sql
SELECT customer_id, COUNT(*) AS current_rows
  FROM customer_dim
 WHERE is_current = TRUE
 GROUP BY customer_id
HAVING COUNT(*) > 1;

WITH ranked AS (
  SELECT id, ROW_NUMBER() OVER (
    PARTITION BY customer_id ORDER BY valid_from DESC
  ) AS rn
  FROM customer_dim
  WHERE is_current = TRUE
)
UPDATE customer_dim SET is_current = FALSE
WHERE id IN (SELECT id FROM ranked WHERE rn > 1);
```
**Explanation:** Detects multiple current rows per customer, then demotes all but the latest valid_from version.

**Alt1 (Self-join):**
```sql
DELETE cd1
  FROM customer_dim cd1
  INNER JOIN customer_dim cd2
    ON  cd1.customer_id = cd2.customer_id
    AND cd1.is_current  = TRUE
    AND cd2.is_current  = TRUE
    AND cd1.valid_from  < cd2.valid_from;
```
**Explanation:** Among pairs of current rows, the older valid_from row is removed.

---

## Q48: Top-N Per Group With Dynamic N From a Reference Table

*Scenario:* Different categories have different limits. `category_limits` defines how many top products each category shows.

*Schema hint:* `products(id INT PK, category VARCHAR(30), name VARCHAR, revenue DECIMAL)`, `category_limits(category VARCHAR(30) PK, top_n INT)`

**Query:**
```sql
WITH ranked AS (
  SELECT p.*,
         ROW_NUMBER() OVER (
           PARTITION BY p.category ORDER BY p.revenue DESC
         ) AS rn
  FROM products p
)
SELECT r.*
  FROM ranked r
  INNER JOIN category_limits cl ON r.category = cl.category
WHERE r.rn <= cl.top_n;
```
**Explanation:** ROW_NUMBER ranks inside each category; joining the limits table applies a per-category cutoff.

**Alt1 (Correlated count):**
```sql
SELECT p.*
  FROM products p
  WHERE (
    SELECT COUNT(*) FROM products p2
    WHERE p2.category = p.category AND p2.revenue > p.revenue
  ) < (
    SELECT top_n FROM category_limits WHERE category = p.category
  );
```
**Explanation:** Keep a product when fewer than `top_n` products in its category outsell it.

---

## Q49: Dedup a Wide Table Using a Hash

*Scenario:* A 50+ column table makes PARTITION BY impractical. Hash all columns into one key, then partition on the hash.

*Schema hint:* `wide_table(id INT PK, col_a TEXT, col_b TEXT, col_c TEXT /* ... up to col_z */)`

**Query:**
```sql
WITH hashed AS (
  SELECT id,
         MD5(CONCAT_WS('|', col_a, col_b, col_c)) AS row_hash,
         ROW_NUMBER() OVER (
           PARTITION BY MD5(CONCAT_WS('|', col_a, col_b, col_c))
           ORDER BY id
         ) AS rn
  FROM wide_table
)
DELETE FROM wide_table WHERE id IN (SELECT id FROM hashed WHERE rn > 1);
```
**Explanation:** CONCAT_WS joins every column into a delimited string; MD5 hashes it so PARTITION BY is one expression. Ensure the delimiter cannot appear in your data.

**Alt1 (SQL Server HASHBYTES):**
```sql
WITH hashed AS (
  SELECT id,
         HASHBYTES('SHA2_256',
           CONCAT(col_a, '|', col_b, '|', col_c)) AS row_hash,
         ROW_NUMBER() OVER (
           PARTITION BY HASHBYTES('SHA2_256',
             CONCAT(col_a, '|', col_b, '|', col_c))
           ORDER BY id
         ) AS rn
  FROM wide_table
)
DELETE FROM wide_table WHERE id IN (SELECT id FROM hashed WHERE rn > 1);
```
**Explanation:** HASHBYTES produces a binary hash in SQL Server — same idea with a different function name.

---

## Q50: Top-N Per Group Using a Named WINDOW Clause (Postgres / MySQL 8+)

*Scenario:* Multiple ranking columns should share one window definition to keep the query readable.

*Schema hint:* `scores(student_id INT, subject VARCHAR(30), score INT, exam_date DATE)`

**Query:**
```sql
SELECT student_id, subject, score, exam_date,
       ROW_NUMBER() OVER w AS seq,
       RANK()       OVER w AS rnk,
       PERCENT_RANK() OVER w AS pct
FROM scores
WINDOW w AS (PARTITION BY subject ORDER BY score DESC)
LIMIT 20;
```
**Explanation:** The named WINDOW clause reuses one partition/ordering across several window functions.

**Alt1 (CTE-factored ranking):**
```sql
WITH ranked AS (
  SELECT *,
         ROW_NUMBER() OVER (
           PARTITION BY subject ORDER BY score DESC
         ) AS rn
  FROM scores
)
SELECT * FROM ranked WHERE rn <= 5
ORDER BY subject, rn;
```
**Explanation:** The CTE approach is portable to every database that supports window functions.
---

## Q51: Top-N Per Group With a Tiebreaker Chain

*Scenario:* Rank the top 2 products per category, ordering by revenue DESC, then units_sold DESC, then id ASC.

*Schema hint:* `product_stats(id INT PK, product_name VARCHAR, category VARCHAR(30), revenue DECIMAL(12,2), units_sold INT)`

**Query:**
```sql
SELECT * FROM (
  SELECT *,
         ROW_NUMBER() OVER (
           PARTITION BY category
           ORDER BY revenue DESC, units_sold DESC, id ASC
         ) AS rn
  FROM product_stats
) ranked
WHERE rn <= 2;
```
**Explanation:** A multi-key window ORDER BY chains tiebreakers from left to right, guaranteeing a deterministic rank.

**Alt1 (Join on id):**
```sql
SELECT ps.*
  FROM product_stats ps
  INNER JOIN (
    SELECT id,
           ROW_NUMBER() OVER (
             PARTITION BY category
             ORDER BY revenue DESC, units_sold DESC, id ASC
           ) AS rn
    FROM product_stats
  ) r ON ps.id = r.id
WHERE r.rn <= 2;
```
**Explanation:** Same ranking, expressed as a join so the windowed subquery touches only narrow columns.

---

## Q52: Dedup With Generated / Computed Columns

*Scenario:* Add a generated `dedup_key` column so dedup can GROUP BY a single pre-computed column instead of several.

*Schema hint:* `orders(id INT PK, customer_id INT, product VARCHAR, order_date DATE, amount DECIMAL)`

**Query:**
```sql
ALTER TABLE orders
  ADD COLUMN dedup_key VARCHAR(200)
  GENERATED ALWAYS AS (CONCAT(customer_id, '|', product, '|', order_date)) STORED;

WITH ranked AS (
  SELECT id, ROW_NUMBER() OVER (
    PARTITION BY dedup_key ORDER BY id
  ) AS rn
  FROM orders
)
DELETE FROM orders WHERE id IN (SELECT id FROM ranked WHERE rn > 1);
```
**Explanation:** The generated column pre-computes the composite key, so PARTITION BY references one expression.

**Alt1 (Postgres integer hash):**
```sql
ALTER TABLE orders
  ADD COLUMN dedup_key INT
  GENERATED ALWAYS AS (
    hashtext(CONCAT(customer_id, '|', product, '|', order_date))
  ) STORED;

CREATE INDEX idx_dedup ON orders(dedup_key);
```
**Explanation:** An integer hash key is faster to index and partition than a long concatenated string.

---

## Q53: Top-N Per Group in a Recursive CTE

*Scenario:* A task tree has parent-child links. Find the top 2 priority tasks at each tree depth.

*Schema hint:* `tasks(id INT PK, name VARCHAR, parent_id INT NULL, priority INT, level INT)`

**Query:**
```sql
WITH RECURSIVE tree AS (
  SELECT id, name, parent_id, priority, 1 AS lvl FROM tasks WHERE parent_id IS NULL
  UNION ALL
  SELECT t.id, t.name, t.parent_id, t.priority, tree.lvl + 1
  FROM tasks t INNER JOIN tree ON t.parent_id = tree.id
)
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY lvl ORDER BY priority DESC
  ) AS rn
  FROM tree
) ranked WHERE rn <= 2;
```
**Explanation:** The recursive CTE materialises the tree with levels; ranking by level isolates the top 2 priorities per depth.

**Alt1 (Flat after recursion):**
```sql
WITH RECURSIVE tree AS (
  SELECT id, name, parent_id, priority, 1 AS lvl FROM tasks WHERE parent_id IS NULL
  UNION ALL
  SELECT t.id, t.name, t.parent_id, t.priority, tree.lvl + 1
  FROM tasks t INNER JOIN tree ON t.parent_id = tree.id
)
SELECT * FROM tasks
WHERE priority >= (
  SELECT MAX(t2.priority) - 1 FROM tasks t2 WHERE t2.level = tasks.level
)
ORDER BY level, priority DESC;
```
**Explanation:** A threshold-based shortcut keeps rows within one point of each level's max priority — no window function.

---

## Q54: Fuzzy Dedup With Trigram Similarity (Postgres pg_trgm)

*Scenario:* `vendors` holds near-duplicate names like 'Blue Sky Labs' and 'Blu Sky Lab'. Merge them with similarity scoring.

*Schema hint:* `vendors(id INT PK, name VARCHAR(100), city VARCHAR(50))`

**Query:**
```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

DELETE FROM vendors
WHERE id IN (
  SELECT b.id
    FROM vendors a
    INNER JOIN vendors b
      ON  a.id < b.id
      AND a.city = b.city
      AND similarity(a.name, b.name) > 0.6
);
```
**Explanation:** pg_trgm's `similarity()` scores shared trigrams; pairs above 0.6 in the same city are treated as duplicates.

**Alt1 (SOUNDEX, dialect-agnostic):**
```sql
DELETE v1
  FROM vendors v1
  INNER JOIN vendors v2
    ON  SOUNDEX(v1.name) = SOUNDEX(v2.name)
    AND v1.city = v2.city
    AND v1.id > v2.id;
```
**Explanation:** Phonetic SOUNDEX grouping — less precise but requires no extensions.

---

## Q55: Top-N With the QUALIFY Clause (Teradata / Snowflake / BigQuery)

*Scenario:* Snowflake/BigQuery let QUALIFY filter window-function output directly in the SELECT.

*Schema hint:* `sales(rep_id INT, region VARCHAR(30), quarter VARCHAR(6), revenue DECIMAL(12,2))`

**Query:**
```sql
SELECT rep_id, region, quarter, revenue
  FROM sales
QUALIFY ROW_NUMBER() OVER (PARTITION BY region ORDER BY revenue DESC) <= 3;
```
**Explanation:** QUALIFY filters right after window computation — no subquery nesting is required.

**Alt1 (Portable subquery):**
```sql
SELECT * FROM (
  SELECT rep_id, region, quarter, revenue,
         ROW_NUMBER() OVER (PARTITION BY region ORDER BY revenue DESC) AS rn
  FROM sales
) t
WHERE rn <= 3;
```
**Explanation:** Standard subquery wrapper gives the same result on any window-function-capable database.

---

## Q56: Partition-Aware Dedup (Operate on One Partition at a Time)

*Scenario:* A huge monthly-partitioned `events` table. Dedup only the September 2026 partition without touching older data.

*Schema hint:* `events(id BIGINT PK, event_type VARCHAR, event_date DATE, payload JSON) PARTITION BY RANGE (event_date)`

**Query:**
```sql
WITH ranked AS (
  SELECT id, ROW_NUMBER() OVER (
    PARTITION BY event_type, event_date ORDER BY id
  ) AS rn
  FROM events
  WHERE event_date >= '2026-09-01' AND event_date < '2026-10-01'
)
DELETE FROM events WHERE id IN (
  SELECT id FROM ranked WHERE rn > 1
);
```
**Explanation:** The WHERE clause enables partition pruning, so only the September partition is scanned and modified.

**Alt1 (Stage, dedup, swap):**
```sql
CREATE TABLE events_stage AS
SELECT * FROM events
WHERE event_date >= '2026-09-01' AND event_date < '2026-10-01';

DELETE FROM events
WHERE event_date >= '2026-09-01' AND event_date < '2026-10-01';

INSERT INTO events
SELECT DISTINCT ON (event_type, event_date) * FROM events_stage
ORDER BY event_type, event_date, id;
```
**Explanation:** Extract the partition, DISTINCT ON to dedup, then swap clean rows back — standard for very large tables.

---

## Q57: Top-N Using PERCENT_RANK / CUME_DIST

*Scenario:* Find products in the top 10% of their category by revenue.

*Schema hint:* `products(id INT PK, name VARCHAR, category VARCHAR(30), revenue DECIMAL(12,2))`

**Query:**
```sql
SELECT * FROM (
  SELECT *,
         PERCENT_RANK() OVER (
           PARTITION BY category ORDER BY revenue DESC
         ) AS pct_rank
  FROM products
) ranked
WHERE pct_rank <= 0.10;
```
**Explanation:** PERCENT_RANK returns a value in [0, 1]; rows at or below 0.10 are the top decile per category.

**Alt1 (NTILE-based):**
```sql
SELECT * FROM (
  SELECT *,
         NTILE(10) OVER (PARTITION BY category ORDER BY revenue DESC) AS decile
  FROM products
) ranked
WHERE decile = 1;
```
**Explanation:** NTILE(10) splits each category into 10 buckets; decile 1 is the top 10%.

---

## Q58: Batch Dedup for Large Tables (Chunked Deletes)

*Scenario:* Deleting millions of duplicate rows at once locks the table. Delete in 1000-row chunks.

*Schema hint:* `massive_log(id BIGINT PK, trace_id VARCHAR(50), ts TIMESTAMP)`

**Query (MySQL stored procedure):**
```sql
DELIMITER //
CREATE PROCEDURE batch_dedup()
BEGIN
  DECLARE affected INT DEFAULT 1;
  WHILE affected > 0 DO
    DELETE FROM massive_log
    WHERE id IN (
      SELECT id FROM (
        SELECT id, ROW_NUMBER() OVER (
          PARTITION BY trace_id ORDER BY ts
        ) AS rn
        FROM massive_log
      ) t WHERE rn > 1
      LIMIT 1000
    );
    SET affected = ROW_COUNT();
  END WHILE;
END //
DELIMITER ;
```
**Explanation:** Deletes 1000 duplicates per iteration, releasing table locks between chunks.

**Alt1 (Reusable CTE loop):**
```sql
WITH dupes AS (
  SELECT id FROM (
    SELECT id, ROW_NUMBER() OVER (PARTITION BY trace_id ORDER BY ts) AS rn
    FROM massive_log
  ) t WHERE rn > 1
  LIMIT 1000
)
DELETE FROM massive_log WHERE id IN (SELECT id FROM dupes);
-- Execute repeatedly until 0 rows affected
```
**Explanation:** The CTE caps each run at 1000 duplicates; re-run until the CTE returns no rows.

---

## Q59: Top-N Per Group With Multi-Level Aggregation (Company + Department)

*Scenario:* Rank the top 3 employees per department AND the top 3 company-wide in a single query.

*Schema hint:* `employees(id INT PK, name VARCHAR, dept VARCHAR, salary DECIMAL)`

**Query:**
```sql
WITH combined AS (
  SELECT id, name, dept, salary, dept AS grp FROM employees
  UNION ALL
  SELECT id, name, dept, salary, 'COMPANY' AS grp FROM employees
)
SELECT name, dept, grp, salary
  FROM (
    SELECT c.*,
           ROW_NUMBER() OVER (
             PARTITION BY grp ORDER BY salary DESC
           ) AS rn
    FROM combined c
  ) ranked
WHERE rn <= 3
ORDER BY grp, rn;
```
**Explanation:** UNION ALL duplicates each row under a "department" and a "COMPANY" group key; one window ranks both levels.

**Alt1 (Two separate queries):**
```sql
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
  FROM employees
) t WHERE rn <= 3;

SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn
  FROM employees
) t WHERE rn <= 3;
```
**Explanation:** Simpler to read, but computes two full scans instead of one combined pass.

---

## Q60: Dedup a Table Without an ID Column

*Scenario:* The table has no primary key and no timestamp. Use Postgres `ctid` (physical row id) as the tiebreaker.

*Schema hint:* `raw_data(col_a VARCHAR, col_b VARCHAR, col_c VARCHAR)` — no PK

**Query:**
```sql
WITH numbered AS (
  SELECT ctid AS phys_id,
         ROW_NUMBER() OVER (
           PARTITION BY col_a, col_b, col_c
           ORDER BY ctid
         ) AS rn
  FROM raw_data
)
DELETE FROM raw_data
WHERE ctid IN (SELECT phys_id FROM numbered WHERE rn > 1);
```
**Explanation:** ctid is the physical location of a row; ordering by it yields a stable "keep-first" choice.

**Alt1 (Staging table):**
```sql
CREATE TEMPORARY TABLE tmp_numbered AS
SELECT ctid, col_a, col_b, col_c,
       ROW_NUMBER() OVER (PARTITION BY col_a, col_b, col_c ORDER BY ctid) AS rn
FROM raw_data;

DELETE FROM raw_data
WHERE ctid IN (SELECT ctid FROM tmp_numbered WHERE rn > 1);

DROP TABLE tmp_numbered;
```
**Explanation:** Materialising the ranked set first avoids re-evaluating the window during the DELETE.

---

## Q61: Top-N Per Group Collected Into a JSON / ARRAY Column

*Scenario:* For each department, collect the top 3 employee names into one JSON array.

*Schema hint:* `employees(id INT PK, name VARCHAR, dept VARCHAR, salary DECIMAL)`

**Query (Postgres):**
```sql
SELECT dept,
       JSON_AGG(name ORDER BY salary DESC) FILTER (WHERE rn <= 3) AS top_3_names
FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
  FROM employees
) t
GROUP BY dept;
```
**Explanation:** ROW_NUMBER marks the top 3; JSON_AGG with a FILTER packs those names into one array per department.

**Alt1 (ARRAY_AGG):**
```sql
SELECT dept,
       ARRAY_AGG(name ORDER BY salary DESC) AS top_3_names
FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
  FROM employees
) t
WHERE rn <= 3
GROUP BY dept;
```
**Explanation:** ARRAY_AGG builds a text[] — simpler than JSON and indexed consistently by the window ordering.

---

## Q62: Cross-Schema Dedup (Staging into Production)

*Scenario:* Merge `staging.orders` into `production.orders`, deduplicating by primary key and preferring staging data.

*Schema hint:* `staging.orders(id INT PK, customer_id INT, order_date DATE, total DECIMAL)`, `production.orders` (same shape)

**Query (Postgres):**
```sql
INSERT INTO production.orders
SELECT * FROM staging.orders s
ON CONFLICT (id) DO UPDATE SET
  customer_id = EXCLUDED.customer_id,
  order_date  = EXCLUDED.order_date,
  total       = EXCLUDED.total;
```
**Explanation:** Cross-schema upsert: new ids insert, colliding ids are overwritten with staging values.

**Alt1 (Diff-first diagnosis):**
```sql
-- Rows present only in staging (candidates to insert)
SELECT s.* FROM staging.orders s
LEFT JOIN production.orders p ON s.id = p.id
WHERE p.id IS NULL;

-- Rows present only in production
SELECT p.* FROM production.orders p
LEFT JOIN staging.orders s ON p.id = s.id
WHERE s.id IS NULL;
```
**Explanation:** LEFT JOIN diffs both sides first so you can review exactly what the merge will change.

---

## Q63: Top-N Using MATCH_RECOGNIZE (Oracle / Postgres 17+)

*Scenario:* Find the longest consecutive streak of winning results per player, then rank the players.

*Schema hint:* `game_results(player_id INT, game_date DATE, result VARCHAR(1))`

**Query:**
```sql
SELECT player_id, start_date, end_date, streak_length
FROM game_results
MATCH_RECOGNIZE (
  PARTITION BY player_id
  ORDER BY game_date
  MEASURES
    FIRST(game_date) AS start_date,
    LAST(game_date)  AS end_date,
    COUNT(*)         AS streak_length
  PATTERN (WIN+)
  DEFINE WIN AS result = 'W'
)
ORDER BY streak_length DESC
FETCH FIRST 3 ROWS ONLY;
```
**Explanation:** MATCH_RECOGNIZE isolates consecutive wins (`WIN+`) per player and reports each streak's boundaries.

**Alt1 (Gaps-and-islands):**
```sql
WITH flagged AS (
  SELECT player_id, game_date,
         game_date - ROW_NUMBER() OVER (
           PARTITION BY player_id, result ORDER BY game_date
         ) AS grp
  FROM game_results
  WHERE result = 'W'
)
SELECT player_id, MIN(game_date) AS start_date, MAX(game_date) AS end_date,
       COUNT(*) AS streak_length
FROM flagged
GROUP BY player_id, grp
ORDER BY streak_length DESC;
```
**Explanation:** Consecutive wins share the same (date minus row_number) group — a classic gaps-and-islands trick.

---

## Q64: Dedup Temporal Tables (SQL Server FOR SYSTEM_TIME)

*Scenario:* A SQL Server temporal table has multiple "current" rows per id. Ensure exactly one current version.

*Schema hint:* `product_t(id INT, name VARCHAR, price DECIMAL, valid_from DATETIME2, valid_to DATETIME2)`

**Query:**
```sql
-- Detect duplicates among current rows
SELECT id, COUNT(*) AS cnt
FROM product_t
WHERE valid_to = '9999-12-31'
GROUP BY id
HAVING COUNT(*) > 1;

-- Demote extra current rows to history
WITH ranked AS (
  SELECT id, valid_from,
         ROW_NUMBER() OVER (PARTITION BY id ORDER BY valid_from DESC) AS rn
  FROM product_t
  WHERE valid_to = '9999-12-31'
)
UPDATE product_t
SET valid_to = DATEADD(SECOND, -1, valid_from)
WHERE id IN (SELECT id FROM ranked WHERE rn > 1);
```
**Explanation:** Temporal tables auto-version history; duplicated current rows are fixed by closing their validity window.

**Alt1 (Postgres range handling):**
```sql
DELETE FROM product_t
WHERE id IN (
  SELECT id FROM (
    SELECT id, ROW_NUMBER() OVER (
      PARTITION BY id ORDER BY valid_from DESC
    ) AS rn
    FROM product_t
    WHERE valid_from <= NOW() AND (valid_to IS NULL OR valid_to >= NOW())
  ) t WHERE rn > 1
);
```
**Explanation:** Postgres-style open/closed range check: delete extra rows that overlap the current moment.

---

## Q65: Top-N Using NTILE (Quartile Selection)

*Scenario:* Split each department's employees into 4 salary quartiles and report the top quartile.

*Schema hint:* `employees(id INT PK, name VARCHAR, dept VARCHAR, salary DECIMAL)`

**Query:**
```sql
SELECT * FROM (
  SELECT *,
         NTILE(4) OVER (PARTITION BY dept ORDER BY salary DESC) AS quartile
  FROM employees
) t
WHERE quartile = 1;
```
**Explanation:** NTILE(4) divides each department evenly into 4 buckets; bucket 1 holds the highest salaries.

**Alt1 (PERCENTILE_CONT threshold):**
```sql
SELECT e.*
  FROM employees e
  WHERE e.salary >= (
    SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY salary)
    FROM employees WHERE dept = e.dept
  );
```
**Explanation:** The 75th percentile of each department's salaries becomes the threshold for the top quartile.

---

## Q66: Dedup on Encrypted / Tokenized Columns

*Scenario:* PII columns are encrypted at rest. Dedup must compare encrypted values, which are deterministic.

*Schema hint:* `customer_pii(id INT PK, enc_name VARBINARY(255), enc_email VARBINARY(255), enc_ssn VARBINARY(255))`

**Query:**
```sql
WITH hashed AS (
  SELECT id,
         SHA2(CAST(enc_name AS CHAR) || '|' || CAST(enc_email AS CHAR) || '|' || CAST(enc_ssn AS CHAR),
              256) AS row_hash,
         ROW_NUMBER() OVER (
           PARTITION BY SHA2(CAST(enc_name AS CHAR) || '|' || CAST(enc_email AS CHAR)
                            || '|' || CAST(enc_ssn AS CHAR), 256)
           ORDER BY id
         ) AS rn
  FROM customer_pii
)
DELETE FROM customer_pii WHERE id IN (SELECT id FROM hashed WHERE rn > 1);
```
**Explanation:** Hashing the ciphertext yields a dedup key — identical plaintext encrypts to identical bytes.

**Alt1 (Direct ciphertext comparison):**
```sql
DELETE p1
  FROM customer_pii p1
  INNER JOIN customer_pii p2
    ON  p1.enc_name  = p2.enc_name
    AND p1.enc_email = p2.enc_email
    AND p1.enc_ssn   = p2.enc_ssn
    AND p1.id > p2.id;
```
**Explanation:** Deterministic encryption produces identical ciphertext for identical plaintext, so direct joins work.

---

## Q67: Top-N Per Group With an Aggregate Condition

*Scenario:* Find departments whose top earner makes more than twice the department average.

*Schema hint:* `employees(id INT PK, name VARCHAR, dept VARCHAR, salary DECIMAL)`

**Query:**
```sql
WITH ranked AS (
  SELECT e.*,
         ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn,
         AVG(salary) OVER (PARTITION BY dept) AS dept_avg
  FROM employees e
)
SELECT name, dept, salary, dept_avg
FROM ranked
WHERE rn = 1 AND salary > 2 * dept_avg;
```
**Explanation:** One pass computes the top-1 rank and the department average via two window functions; the outer WHERE filters.

**Alt1 (GROUP BY + self-join, no windows):**
```sql
SELECT e.name, e.dept, e.salary, d.dept_avg
  FROM employees e
  INNER JOIN (
    SELECT dept, AVG(salary) AS dept_avg, MAX(salary) AS dept_max
    FROM employees GROUP BY dept
  ) d ON e.dept = d.dept AND e.salary = d.dept_max
WHERE d.dept_max > 2 * d.dept_avg;
```
**Explanation:** Aggregated department stats join back to the top earner; the condition filters departments.

---

## Q68: Dedup a Self-Referencing Tree Without Orphaning Children

*Scenario:* `org` is a self-referencing table with duplicate email nodes. Re-parent children before deleting duplicates.

*Schema hint:* `org(id INT PK, name VARCHAR, email VARCHAR, manager_id INT REFERENCES org(id))`

**Query (Postgres):**
```sql
WITH dupes AS (
  SELECT email, MIN(id) AS keep_id, ARRAY_AGG(id ORDER BY id) AS all_ids
  FROM org
  GROUP BY email
  HAVING COUNT(*) > 1
),
to_delete AS (
  SELECT u AS del_id
  FROM dupes, UNNEST(all_ids[2:]) AS u
)
UPDATE org SET manager_id = d.keep_id
FROM dupes d, to_delete t
WHERE org.id IN (SELECT del_id FROM to_delete)  -- rows whose id is a duplicate
  AND org.manager_id = t.del_id;

WITH dupes AS (
  SELECT email, ARRAY_AGG(id ORDER BY id) AS all_ids
  FROM org GROUP BY email HAVING COUNT(*) > 1
),
to_delete AS (SELECT u AS del_id FROM dupes, UNNEST(all_ids[2:]) AS u)
DELETE FROM org WHERE id IN (SELECT del_id FROM to_delete);
```
**Explanation:** The first CTE computes keep + delete ids; the UPDATE repoints children at the canonical record; the DELETE then removes the rest.

**Alt1 (Manual two-table approach):**
```sql
SELECT email, MIN(id) AS keep_id, MAX(id) AS del_id
FROM org GROUP BY email HAVING COUNT(*) > 1;

-- For each pair: repoint then delete
UPDATE org SET manager_id = <keep_id> WHERE manager_id = <del_id>;
DELETE FROM org WHERE id = <del_id>;
```
**Explanation:** Straightforward row-by-row fix — simple to reason about, verbose for large datasets.

---

## Q69: Top-N Per Group Pivoted into Columns (CASE)

*Scenario:* For each department, present the top 3 earners' names and salaries as separate columns.

*Schema hint:* `employees(id INT PK, name VARCHAR, dept VARCHAR, salary DECIMAL)`

**Query:**
```sql
WITH ranked AS (
  SELECT dept, name, salary,
         ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
  FROM employees
)
SELECT dept,
       MAX(CASE WHEN rn = 1 THEN name   END) AS emp1_name,
       MAX(CASE WHEN rn = 1 THEN salary  END) AS emp1_salary,
       MAX(CASE WHEN rn = 2 THEN name   END) AS emp2_name,
       MAX(CASE WHEN rn = 2 THEN salary  END) AS emp2_salary,
       MAX(CASE WHEN rn = 3 THEN name   END) AS emp3_name,
       MAX(CASE WHEN rn = 3 THEN salary  END) AS emp3_salary
FROM ranked
WHERE rn <= 3
GROUP BY dept;
```
**Explanation:** CASE pivots ranked rows into named columns; GROUP BY collapses each department to one row.

**Alt1 (ARRAY_AGG):**
```sql
SELECT dept,
       ARRAY_AGG(name ORDER BY salary DESC) FILTER (WHERE rn <= 3) AS top_3
FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
  FROM employees
) t
GROUP BY dept;
```
**Explanation:** ARRAY_AGG yields a single array column — cleaner than three fixed CASE columns.

---

## Q70: Dedup Under Row-Level Security

*Scenario:* Orders are multi-tenant with RLS. Dedup must respect tenant boundaries — only touch rows the current session may see.

*Schema hint:* `orders(id INT PK, customer_id INT, tenant_id INT, total DECIMAL)` with an RLS policy on `tenant_id`

**Query:**
```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = CAST(current_setting('app.tenant_id') AS INT));

SET app.tenant_id = '7';

-- RLS automatically scopes the DELETE to tenant 7
WITH ranked AS (
  SELECT id, ROW_NUMBER() OVER (
    PARTITION BY customer_id, total ORDER BY id
  ) AS rn
  FROM orders
)
DELETE FROM orders WHERE id IN (SELECT id FROM ranked WHERE rn > 1);
```
**Explanation:** The policy filters every statement to the session's tenant; dedup therefore touches only visible rows.

**Alt1 (Explicit tenant filter):**
```sql
DELETE o1
  FROM orders o1
  INNER JOIN orders o2
    ON  o1.customer_id = o2.customer_id
    AND o1.total       = o2.total
    AND o1.tenant_id   = o2.tenant_id
    AND o1.id > o2.id
 WHERE o1.tenant_id = CAST(current_setting('app.tenant_id') AS INT);
```
**Explanation:** Manual tenant scoping inside the self-join — no RLS required, but enforcement lives in the query.

---

## Q71: Top-N With LIMIT ... WITH TIES

*Scenario:* Return the top 5 sales reps by total sales, including every rep tied at position 5.

*Schema hint:* `sales_reps(id INT PK, name VARCHAR, region VARCHAR, total_sales DECIMAL)`

**Query (SQL Server):**
```sql
SELECT TOP 5 WITH TIES *
FROM sales_reps
ORDER BY total_sales DESC;
```
**Explanation:** WITH TIES extends the result with any rows sharing the 5th-highest total_sales.

**Alt1 (SQL:2008 FETCH WITH TIES):**
```sql
SELECT * FROM sales_reps
ORDER BY total_sales DESC
FETCH FIRST 5 ROWS WITH TIES;
```
**Explanation:** The standard FETCH variant of the same tie-aware limiting.

**Alt2 (Portable DENSE_RANK):**
```sql
SELECT * FROM (
  SELECT *, DENSE_RANK() OVER (ORDER BY total_sales DESC) AS dr
  FROM sales_reps
) t WHERE dr <= 5;
```
**Explanation:** DENSE_RANK reproduces the tie logic on any window-function-capable database.

---

## Q72: Dedup Through an Updatable View (INSTEAD OF Trigger)

*Scenario:* Expose a deduplicated view of a log table; route inserts through it to the raw table.

*Schema hint:* `raw_logs(id INT PK, event_type VARCHAR, payload JSON, created_at TIMESTAMP)`

**Query (Postgres):**
```sql
CREATE VIEW clean_logs AS
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY event_type ORDER BY created_at DESC
  ) AS rn
  FROM raw_logs
) t WHERE rn = 1;

CREATE FUNCTION insert_clean_log() RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO raw_logs (event_type, payload, created_at)
  VALUES (NEW.event_type, NEW.payload, NEW.created_at);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_clean_log_insert
  INSTEAD OF INSERT ON clean_logs
  FOR EACH ROW EXECUTE FUNCTION insert_clean_log();
```
**Explanation:** The view hides duplicates; the INSTEAD OF trigger redirects inserts to the underlying table.

**Alt1 (Materialized view):**
```sql
CREATE MATERIALIZED VIEW clean_logs AS
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY event_type ORDER BY created_at DESC) AS rn
  FROM raw_logs
) t WHERE rn = 1;

REFRESH MATERIALIZED VIEW clean_logs;
```
**Explanation:** A materialized view pre-computes the dedup and can be refreshed on a schedule.

---

## Q73: Top-N Per Group With Correlated EXISTS (No Window Functions)

*Scenario:* Which employees sit in their department's top 3, using only a correlated subquery?

*Schema hint:* `employees(id INT PK, name VARCHAR, dept VARCHAR, salary DECIMAL)`

**Query:**
```sql
SELECT e.*
  FROM employees e
  WHERE (
    SELECT COUNT(DISTINCT e2.salary)
    FROM employees e2
    WHERE e2.dept = e.dept AND e2.salary > e.salary
  ) < 3;
```
**Explanation:** If fewer than 3 distinct salaries in the department exceed this salary, the employee is in the top 3.

**Alt1 (EXISTS against top-3 salary list):**
```sql
SELECT e.*
  FROM employees e
  WHERE EXISTS (
    SELECT 1 FROM (
      SELECT DISTINCT salary FROM employees
      WHERE dept = e.dept ORDER BY salary DESC LIMIT 3
    ) top_salaries
    WHERE top_salaries.salary = e.salary
  );
```
**Explanation:** Exists only if the employee's salary appears in the department's top-3 distinct salary list.

---

## Q74: Dedup With the MERGE Statement (SQL Server / Oracle)

*Scenario:* Use MERGE to locate duplicate rows and delete them atomically.

*Schema hint:* `transactions(id INT PK, account_id INT, ref_code VARCHAR(20), amount DECIMAL)`

**Query (SQL Server):**
```sql
WITH dupes AS (
  SELECT id,
         ROW_NUMBER() OVER (
           PARTITION BY account_id, ref_code ORDER BY id
         ) AS rn
  FROM transactions
)
MERGE transactions AS target
USING (SELECT id FROM dupes WHERE rn > 1) AS source
ON target.id = source.id
WHEN MATCHED THEN DELETE;
```
**Explanation:** MERGE treats the duplicate ids as a source and deletes every match in one statement.

**Alt1 (Oracle ROWID):**
```sql
DELETE FROM transactions
WHERE ROWID IN (
  SELECT rid FROM (
    SELECT ROWID AS rid,
           ROW_NUMBER() OVER (
             PARTITION BY account_id, ref_code ORDER BY ROWID
           ) AS rn
    FROM transactions
  ) WHERE rn > 1
);
```
**Explanation:** Oracle's ROWID acts as the physical row identity for ranking and targeted deletion.

---

## Q75: Top-N Using FETCH FIRST ROWS ONLY (SQL:2008)

*Scenario:* Use the standard FETCH clause to get the top 3 orders per customer.

*Schema hint:* `orders(id INT PK, customer_id INT, order_date DATE, total DECIMAL)`

**Query:**
```sql
SELECT c.customer_id, o.*
  FROM (SELECT DISTINCT customer_id FROM orders) c
  CROSS JOIN LATERAL (
    SELECT * FROM orders
    WHERE customer_id = c.customer_id
    ORDER BY order_date DESC
    FETCH FIRST 3 ROWS ONLY
  ) o;
```
**Explanation:** LATERAL + FETCH FIRST is the standard-SQL, index-friendly pattern for per-group top-N.

**Alt1 (Correlated FETCH via EXISTS):**
```sql
SELECT o.*
  FROM orders o
  WHERE o.id IN (
    SELECT o2.id FROM orders o2
    WHERE o2.customer_id = o.customer_id
    ORDER BY o2.order_date DESC
    FETCH FIRST 3 ROWS ONLY
  );
```
**Explanation:** Correlates on customer_id and limits inside the subquery with FETCH FIRST.
---

## Q76: Dedup With a Sliding Window Frame (ROWS BETWEEN)

*Scenario:* Remove any reading equal to the previous reading from the same device — using an explicit window frame.

*Schema hint:* `readings(id SERIAL PK, device_id INT, value DECIMAL(10,3), ts TIMESTAMPTZ)`

**Query:**
```sql
WITH framed AS (
  SELECT id, device_id, value, ts,
         AVG(value) OVER (
           PARTITION BY device_id
           ORDER BY ts
           ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING
         ) AS prev_value
  FROM readings
)
DELETE FROM readings
WHERE id IN (
  SELECT id FROM framed WHERE value = prev_value
);
```
**Explanation:** The frame `ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING` exposes exactly the preceding row's value.

**Alt1 (LAG — simpler):**
```sql
WITH with_prev AS (
  SELECT id, value,
         LAG(value) OVER (PARTITION BY device_id ORDER BY ts) AS prev_value
  FROM readings
)
DELETE FROM readings
WHERE id IN (SELECT id FROM with_prev WHERE value = prev_value);
```
**Explanation:** LAG is the idiomatic, more readable way to reach one row back without an explicit frame.

---

## Q77: Top-N in a Graph / Path Context

*Scenario:* In a directed task graph, rank paths by total cost and report the top 2 cheapest paths.

*Schema hint:* `path_edges(from_node INT, to_node INT, cost DECIMAL)`

**Query:**
```sql
WITH RECURSIVE paths AS (
  SELECT from_node, to_node, cost, ARRAY[from_node] AS visited, 1 AS length
  FROM path_edges
  UNION ALL
  SELECT p.from_node, e.to_node, p.cost + e.cost, p.visited || e.from_node, p.length + 1
  FROM paths p
  INNER JOIN path_edges e ON p.to_node = e.from_node
  WHERE NOT e.to_node = ANY(p.visited)
    AND p.length < 10
)
SELECT to_node AS head, cost, visited, length,
       ROW_NUMBER() OVER (ORDER BY cost ASC) AS rn
FROM paths
QUALIFY rn <= 2;
```
**Explanation:** The recursive CTE enumerates simple paths; ROW_NUMBER (via QUALIFY here) keeps the 2 cheapest.

**Alt1 (Where VARIANT stores paths):**
```sql
WITH RECURSIVE paths AS (
  SELECT from_node, to_node, cost, CAST(to_node AS VARCHAR) AS route
  FROM path_edges
  WHERE from_node = 1
  UNION ALL
  SELECT p.from_node, e.to_node, p.cost + e.cost,
         CONCAT(p.route, '->', e.to_node)
  FROM paths p
  INNER JOIN path_edges e ON p.to_node = e.from_node
  WHERE position(CONCAT('->', e.to_node) IN p.route) = 0
)
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (ORDER BY cost ASC) AS rn
  FROM paths
) t WHERE rn <= 2;
```
**Explanation:** Cycle-safe path concatenation, then a plain subquery keeps the two least-expensive paths.

---

## Q78: Dedup With an Aggregate FILTER (Postgres)

*Scenario:* Count and summarise duplicate emails per user while deleting extras — all in one reporting query.

*Schema hint:* `users(id INT PK, email VARCHAR(255), age INT)`

**Query:**
```sql
SELECT LOWER(email) AS norm_email,
       COUNT(*) AS total_rows,
       COUNT(*) FILTER (WHERE id = MIN(id) OVER (PARTITION BY LOWER(email))) AS keep_rows
FROM users
GROUP BY LOWER(email)
HAVING COUNT(*) > 1;
```
**Explanation:** FILTER narrows aggregate counts to a subset of rows; here it distinguishes keep vs duplicate counts.

**Alt1 (Delete + verify count):**
```sql
WITH ranked AS (
  SELECT id, ROW_NUMBER() OVER (PARTITION BY LOWER(email) ORDER BY id) AS rn
  FROM users
)
DELETE FROM users WHERE id IN (SELECT id FROM ranked WHERE rn > 1);

-- Verify remaining duplicates
SELECT LOWER(email), COUNT(*) FROM users GROUP BY LOWER(email) HAVING COUNT(*) > 1;
```
**Explanation:** Deleting first, then a HAVING count verifies the table is clean — a common QA loop.

---

## Q79: Approximate Top-N Using TABLESAMPLE

*Scenario:* For a quick estimate, sample a fraction of a huge table to judge the top categories.

*Schema hint:* `events_log(id BIGINT PK, event_type VARCHAR, ts TIMESTAMP)`

**Query (Postgres):**
```sql
SELECT event_type, COUNT(*) AS cnt
FROM events_log TABLESAMPLE SYSTEM (10)
GROUP BY event_type
ORDER BY cnt DESC
LIMIT 5;
```
**Explanation:** TABLESAMPLE reads roughly 10% of pages, so ranking is approximate but dramatically faster.

**Alt1 (Exact answer):**
```sql
SELECT event_type, COUNT(*) AS cnt
FROM events_log
GROUP BY event_type
ORDER BY cnt DESC
LIMIT 5;
```
**Explanation:** The exact equivalent for smaller datasets — same result without sampling uncertainty.

---

## Q80: Dedup on a Columnstore-Indexed Table

*Scenario:* A columnstore-heavy analytics table accumulates duplicates on reload. Dedup efficiently.

*Schema hint:* `analytics_fact(id BIGINT PK, skey INT, metric DECIMAL, load_ts TIMESTAMP)`

**Query (SQL Server):**
```sql
ALTER TABLE analytics_fact REBUILD PARTITION = ALL
  WITH (DATA_COMPRESSION = COLUMNSTORE);

WITH ranked AS (
  SELECT id, ROW_NUMBER() OVER (
    PARTITION BY skey, CAST(load_ts AS DATE) ORDER BY id
  ) AS rn
  FROM analytics_fact
)
DELETE FROM analytics_fact WHERE id IN (SELECT id FROM ranked WHERE rn > 1);

-- Rebuild the columnstore after delete to reclaim space
ALTER TABLE analytics_fact REBUILD;
```
**Explanation:** Columnstore rebuilds tuck the table; dedup keys on the natural grain; a final rebuild reclaims deleted space.

**Alt1 (Partition swap):**
```sql
-- Dedup into a fresh table, then swap
CREATE TABLE analytics_fact_clean AS
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY skey, CAST(load_ts AS DATE) ORDER BY id
  ) AS rn
  FROM analytics_fact
) t WHERE rn = 1;

ALTER TABLE analytics_fact SWITCH PARTITION ALL TO analytics_fact_clean;
```
**Explanation:** Build a clean table then swap partitions — avoids a slow in-place delete on columnstore.

---

## Q81: Top-N With LEAD/LAG Gap Analysis

*Scenario:* Find employees whose salary jump is within the top 3 of the biggest year-over-year raises in each department.

*Schema hint:* `salaries(id INT PK, employee_id INT, dept VARCHAR, year INT, salary DECIMAL)`

**Query:**
```sql
WITH gaps AS (
  SELECT id, employee_id, dept, year, salary,
         salary - LAG(salary) OVER (
           PARTITION BY employee_id ORDER BY year
         ) AS raise_amount
  FROM salaries
),
ranked AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY dept ORDER BY raise_amount DESC
  ) AS rn
  FROM gaps
  WHERE raise_amount IS NOT NULL
)
SELECT * FROM ranked WHERE rn <= 3;
```
**Explanation:** LAG computes each year-over-year raise; ROW_NUMBER ranks raises within each department.

**Alt1 (Join-to-previous style):**
```sql
SELECT s.*, s.salary - p.salary AS raise_amount
  FROM salaries s
  INNER JOIN salaries p
    ON  p.employee_id = s.employee_id
    AND p.year = s.year - 1
QUALIFY ROW_NUMBER() OVER (PARTITION BY s.dept ORDER BY s.salary - p.salary DESC) <= 3;
```
**Explanation:** A self-join replaces LAG; QUALIFY provides the in-select top-3 filter.

---

## Q82: Dedup With Valid-Time Range Overlaps

*Scenario:* `coverage` rows for the same customer overlap in time. Collapse to non-overlapping valid periods.

*Schema hint:* `coverage(id INT PK, customer_id INT, coverage_from TIMESTAMP, coverage_to TIMESTAMP)`

**Query (Postgres):**
```sql
WITH ranked AS (
  SELECT id, customer_id, coverage_from, coverage_to,
         MAX(coverage_to) OVER (
           PARTITION BY customer_id
           ORDER BY coverage_from, id
           ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
         ) AS prev_max_to
  FROM coverage
),
islands AS (
  SELECT id, customer_id, coverage_from, coverage_to,
         CASE WHEN coverage_from <= prev_max_to THEN NULL ELSE 1 END AS island_boundary
  FROM ranked
)
SELECT customer_id, MIN(coverage_from) AS merged_from,
       MAX(coverage_to) AS merged_to
FROM (
  SELECT customer_id, coverage_from, coverage_to,
         COUNT(island_boundary) OVER (
           PARTITION BY customer_id ORDER BY coverage_from ROWS UNBOUNDED PRECEDING
         ) AS island_id
  FROM islands
) collapsed
GROUP BY customer_id, island_id;
```
**Explanation:** Gaps-and-islands collapses overlapping validity windows into continuous merged ranges.

**Alt1 (Exclusion delete):**
```sql
DELETE c1
  FROM coverage c1
  INNER JOIN coverage c2
    ON  c1.customer_id = c2.customer_id
    AND c1.coverage_from >= c2.coverage_from
    AND c1.coverage_to   <= c2.coverage_to
    AND c1.id <> c2.id;
```
**Explanation:** Any row fully contained inside another row of the same customer is redundant and deleted.

---

## Q83: Top-N Per Group Using generate_series (Postgres)

*Scenario:* Build a date-spine list of the top 1 product per region for every month of 2026.

*Schema hint:* `sales(product_id INT, region VARCHAR(30), amount DECIMAL, sold_month DATE)`

**Query:**
```sql
SELECT months.month_start, ranked.region, ranked.product_id
FROM generate_series('2026-01-01'::DATE, '2026-12-01'::DATE, INTERVAL '1 month') AS months(month_start)
CROSS JOIN LATERAL (
  SELECT region, product_id, amount,
         ROW_NUMBER() OVER (
           PARTITION BY region ORDER BY amount DESC
         ) AS rn
  FROM sales
  WHERE DATE_TRUNC('month', sold_month) = months.month_start
) ranked
WHERE ranked.rn = 1
ORDER BY months.month_start, ranked.region;
```
**Explanation:** LATERAL evaluation runs per generated month; ROW_NUMBER keeps the top product per region per month.

**Alt1 (Prune with WHERE):**
```sql
SELECT region, DATE_TRUNC('month', sold_month) AS mth, product_id, amount
FROM (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY region, DATE_TRUNC('month', sold_month)
    ORDER BY amount DESC
  ) AS rn
  FROM sales
  WHERE sold_month >= '2026-01-01' AND sold_month < '2027-01-01'
) t WHERE rn = 1;
```
**Explanation:** Pruning to the year plus a composite PARTITION BY produces the same top-of-month rank.

---

## Q84: Dedup With HASHBYTES (SQL Server)

*Scenario:* Compare candidate duplicate rows by hashing a variable-length concatenation of columns.

*Schema hint:* `varying_rows(id INT PK, code VARCHAR(20), detail TEXT, created_at DATETIME2)`

**Query:**
```sql
WITH hashed AS (
  SELECT id,
         HASHBYTES('SHA2_256',
            CONCAT(code, '|', LEN(detail), '|', detail)
         ) AS row_hash,
         ROW_NUMBER() OVER (
           PARTITION BY HASHBYTES('SHA2_256',
              CONCAT(code, '|', LEN(detail), '|', detail)
           ) ORDER BY id
         ) AS rn
  FROM varying_rows
)
DELETE FROM varying_rows WHERE id IN (SELECT id FROM hashed WHERE rn > 1);
```
**Explanation:** Including LEN(detail) avoids delimiter collisions for variable-length text; SHA2_256 hashes the combined key.

**Alt1 (CHECKSUM at low cost but riskier):**
```sql
WITH hashed AS (
  SELECT id,
         CHECKSUM(CONCAT(code, '|', detail)) AS row_hash,
         ROW_NUMBER() OVER (
           PARTITION BY CHECKSUM(CONCAT(code, '|', detail)) ORDER BY id
         ) AS rn
  FROM varying_rows
)
SELECT * FROM hashed WHERE rn > 1;
```
**Explanation:** CHECKSUM is cheap but collision-prone — safe only for a first pass that still needs a full verification join.

---

## Q85: Top-N Per Group With Conditional Aggregates

*Scenario:* Rank employees by their Q4 sales only, but still show full-year totals.

*Schema hint:* `sales_by_quarter(employee_id INT, quarter VARCHAR(2), amount DECIMAL)`

**Query:**
```sql
WITH agg AS (
  SELECT employee_id,
         SUM(amount) AS fy_total,
         SUM(CASE WHEN quarter = 'Q4' THEN amount ELSE 0 END) AS q4_sales
  FROM sales_by_quarter
  GROUP BY employee_id
)
SELECT *, RANK() OVER (ORDER BY q4_sales DESC) AS q4_rank
FROM agg
WHERE q4_sales > 0
ORDER BY q4_rank
LIMIT 10;
```
**Explanation:** CASE aggregation computes Q4 sales inside the same pass as the full-year total; RANK sorts by Q4 only.

**Alt1 (FILTER in Postgres):**
```sql
SELECT employee_id,
       SUM(amount) AS fy_total,
       SUM(amount) FILTER (WHERE quarter = 'Q4') AS q4_sales
FROM sales_by_quarter
GROUP BY employee_id
ORDER BY q4_sales DESC NULLS LAST
LIMIT 10;
```
**Explanation:** The Postgres FILTER variant is more readable and treats non-Q4 quarters as NULL rather than zero.

---

## Q86: Multi-Source UNION Dedup

*Scenario:* Three POS systems each dump `sales` tables. Merge them into one deduplicated ledger keyed on a global receipt id.

*Schema hint:* `pos_a.receipts(receipt_id INT, amount DECIMAL, ts TIMESTAMP)`, `pos_b`, `pos_c` (same shape)

**Query:**
```sql
WITH all_rows AS (
  SELECT receipt_id, amount, ts, 'A' AS source FROM pos_a.receipts
  UNION ALL
  SELECT receipt_id, amount, ts, 'B' FROM pos_b.receipts
  UNION ALL
  SELECT receipt_id, amount, ts, 'C' FROM pos_c.receipts
),
ranked AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY receipt_id ORDER BY ts DESC, source
  ) AS rn
  FROM all_rows
)
INSERT INTO consolidated (receipt_id, amount, ts, source)
SELECT receipt_id, amount, ts, source FROM ranked WHERE rn = 1;
```
**Explanation:** UNION ALL stacks the sources; ROW_NUMBER per receipt keeps the newest row from any source.

**Alt1 (FULL OUTER JOIN coalescing):**
```sql
SELECT COALESCE(a.receipt_id, b.receipt_id, c.receipt_id) AS receipt_id,
       COALESCE(a.amount, b.amount, c.amount) AS amount,
       GREATEST(a.ts, b.ts, c.ts) AS ts
FROM pos_a.receipts a
FULL OUTER JOIN pos_b.receipts b ON a.receipt_id = b.receipt_id
FULL OUTER JOIN pos_c.receipts c ON COALESCE(a.receipt_id, b.receipt_id) = c.receipt_id;
```
**Explanation:** FULL OUTER JOINS align by receipt id; COALESCE/GREATEST pick the dominating values.

---

## Q87: Top-N With JSON Path Expressions

*Scenario:* Rank clicks into session buckets extracted from a JSON payload.

*Schema hint:* `clicks(id INT PK, session_id INT, payload JSONB, clicked_at TIMESTAMP)`

**Query (Postgres):**
```sql
SELECT session_id, (payload->>'page') AS page,
       ROW_NUMBER() OVER (
         PARTITION BY session_id ORDER BY clicked_at ASC
       ) AS seq
FROM clicks
WHERE payload @> '{"kind": "page_view"}'
  AND (payload->>'page') IS NOT NULL;
```
**Explanation:** JSONB operators filter payloads; ROW_NUMBER sequences page views inside each session.

**Alt1 (Aggregate into JSON):**
```sql
SELECT session_id,
       JSON_AGG(JSON_BUILD_OBJECT('page', payload->>'page', 'at', clicked_at)
                ORDER BY clicked_at) AS pages
FROM clicks
WHERE payload->>'kind' = 'page_view'
GROUP BY session_id;
```
**Explanation:** Builds the per-session navigation path as a JSON array ordered by click time.

---

## Q88: Dedup on a Table With Sparse Columns

*Scenario:* A wide table stores most columns as NULL. Dedup using only the non-NULL, meaningful subset.

*Schema hint:* `user_activity(id INT PK, user_id INT, a VARCHAR, b VARCHAR, c VARCHAR)` (mostly NULL)

**Query (SQL Server):**
```sql
ALTER TABLE user_activity REBUILD;

WITH sig AS (
  SELECT id, user_id,
         CONCAT_WS('|', a, b, c) AS signature,
         ROW_NUMBER() OVER (
           PARTITION BY user_id, CONCAT_WS('|', a, b, c) ORDER BY id
         ) AS rn
  FROM user_activity
)
DELETE FROM user_activity WHERE id IN (SELECT id FROM sig WHERE rn > 1);
```
**Explanation:** CONCAT_WS turns the sparse set into a signature; NULLs collapse into the separator so they align.

**Alt1 (Ignore fully empty rows first):**
```sql
DELETE FROM user_activity
WHERE (a IS NULL AND b IS NULL AND c IS NULL)
   OR id IN (
     SELECT id FROM (
       SELECT id, ROW_NUMBER() OVER (
         PARTITION BY user_id, COALESCE(a,''), COALESCE(b,''), COALESCE(c,'')
         ORDER BY id
       ) AS rn
       FROM user_activity
     ) t WHERE rn > 1
   );
```
**Explanation:** Dropping completely empty rows first narrows the partition; COALESCE makes the rest compare safely.

---

## Q89: Top-N Per Group With a Named WINDOW Clause Reused by Three Rankings

*Scenario:* Show employees with their dept rank, company rank, and decile — all sharing one window definition.

*Schema hint:* `employees(id INT PK, name VARCHAR, dept VARCHAR, salary DECIMAL)`

**Query:**
```sql
SELECT name, dept, salary,
       ROW_NUMBER() OVER w  AS dept_rank,
       RANK()       OVER w2 AS company_rank,
       NTILE(4)     OVER w  AS salary_quartile
FROM employees
WINDOW w  AS (PARTITION BY dept ORDER BY salary DESC),
       w2 AS (ORDER BY salary DESC);
```
**Explanation:** Named windows let one definition drive multiple functions and keep the SELECT readable.

**Alt1 (Repeated inline definitions):**
```sql
SELECT name, dept, salary,
       ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS dept_rank,
       RANK()       OVER (ORDER BY salary DESC)                  AS company_rank,
       NTILE(4)     OVER (PARTITION BY dept ORDER BY salary DESC) AS salary_quartile
FROM employees;
```
**Explanation:** Explicitly repeating the clauses works on every database, at the cost of verbosity.

---

## Q90: MERGE + OUTPUT for an Audited Dedup

*Scenario:* Dedup a table and log every deleted row to an audit table at the same time.

*Schema hint:* `dedup_target(id INT PK, email VARCHAR, created_at DATE)`, `dedup_audit(id INT, reason VARCHAR, deleted_at DATETIME2)`

**Query (SQL Server):**
```sql
MERGE dedup_target AS t
USING (
  SELECT id, ROW_NUMBER() OVER (PARTITION BY email ORDER BY created_at DESC) AS rn
  FROM dedup_target
) s ON t.id = s.id AND s.rn > 1
WHEN MATCHED THEN DELETE
OUTPUT DELETED.id, 'duplicate_email', GETDATE()
INTO dedup_audit (id, reason, deleted_at);
```
**Explanation:** MERGE's OUTPUT clause writes deleted rows into `dedup_audit` in the same statement.

**Alt1 (INSERT ... SELECT before DELETE):**
```sql
INSERT INTO dedup_audit (id, reason, deleted_at)
SELECT id, 'duplicate_email', GETDATE()
FROM (
  SELECT id, ROW_NUMBER() OVER (PARTITION BY email ORDER BY created_at DESC) AS rn
  FROM dedup_target
) t WHERE rn > 1;

DELETE FROM dedup_target
WHERE id IN (
  SELECT id FROM (
    SELECT id, ROW_NUMBER() OVER (PARTITION BY email ORDER BY created_at DESC) AS rn
    FROM dedup_target
  ) t WHERE rn > 1
);
```
**Explanation:** Two statements: snapshot duplicates to audit first, then delete them.

---

## Q91: Top-N Distribution Using WIDTH_BUCKET (Oracle / Postgres)

*Scenario:* Slice salaries into 10 equal-width buckets and report the bucket containing the highest-earning employees per department.

*Schema hint:* `employees(id INT PK, name VARCHAR, dept VARCHAR, salary DECIMAL)`

**Query (Postgres):**
```sql
WITH bounds AS (
  SELECT dept, MIN(salary) AS lo, MAX(salary) AS hi
  FROM employees GROUP BY dept
)
SELECT e.dept, e.name, e.salary,
       WIDTH_BUCKET(e.salary, b.lo, b.hi + 1, 10) AS bucket
FROM employees e
JOIN bounds b ON e.dept = b.dept
WHERE WIDTH_BUCKET(e.salary, b.lo, b.hi + 1, 10) = 10;
```
**Explanation:** WIDTH_BUCKET maps salary into 10 equal-width buckets; bucket 10 holds the department's top earners.

**Alt1 (NTILE quartile equivalent):**
```sql
SELECT * FROM (
  SELECT *, NTILE(10) OVER (PARTITION BY dept ORDER BY salary DESC) AS decile
  FROM employees
) t WHERE decile = 1;
```
**Explanation:** NTILE produces equal-count buckets, whereas WIDTH_BUCKET produces equal-width buckets.

---

## Q92: Dedup Approximate Numeric Columns

*Scenario:* FLOAT readings have tiny representation errors. Dedup values within a tolerance instead of exact equality.

*Schema hint:* `readings(id INT PK, device_id INT, value DOUBLE, ts TIMESTAMP)`

**Query:**
```sql
WITH rounded AS (
  SELECT id, device_id, value, ts,
         ROUND(value, 3) AS norm_value,
         ROW_NUMBER() OVER (
           PARTITION BY device_id, ROUND(value, 3), DATE(ts)
           ORDER BY ts
         ) AS rn
  FROM readings
)
DELETE FROM readings WHERE id IN (SELECT id FROM rounded WHERE rn > 1);
```
**Explanation:** ROUND(value, 3) absorbs floating-point jitter before partitioning, so near-equal readings merge.

**Alt1 (Band comparison):**
```sql
DELETE r1
  FROM readings r1
  INNER JOIN readings r2
    ON  r1.device_id = r2.device_id
    AND ABS(r1.value - r2.value) < 0.0005
    AND r1.ts > r2.ts
    AND r1.ts <= r2.ts + INTERVAL '5 minutes';
```
**Explanation:** Band-based: any reading within 0.0005 and 5 minutes of an earlier one is deleted.

---

## Q93: Top-N Per Group Expressed With LISTAGG / STRING_AGG

*Scenario:* For each region, output the top 3 products as a comma-separated string.

*Schema hint:* `sales(region VARCHAR(30), product VARCHAR(50), revenue DECIMAL)`

**Query (Postgres):**
```sql
SELECT region,
       STRING_AGG(product, ',' ORDER BY revenue DESC) AS top_products
FROM (
  SELECT region, product, revenue,
         ROW_NUMBER() OVER (PARTITION BY region ORDER BY revenue DESC) AS rn
  FROM sales
) t
WHERE rn <= 3
GROUP BY region;
```
**Explanation:** Filtering to the top 3 before aggregation lets STRING_AGG emit "prod1,prod2,prod3" per region.

**Alt1 (Oracle LISTAGG classic):**
```sql
SELECT region,
       LISTAGG(product, ',') WITHIN GROUP (ORDER BY revenue DESC) AS top_products
FROM (
  SELECT region, product, revenue,
         ROW_NUMBER() OVER (PARTITION BY region ORDER BY revenue DESC) AS rn
  FROM sales
  WHERE rn <= 3
) t
GROUP BY region;
```
**Explanation:** Oracle's LISTAGG with WITHIN GROUP ordering matches the Postgres behaviour.

---

## Q94: Dedup Analysis Using PIVOT / UNPIVOT

*Scenario:* A signup log stores one row per touchpoint. Pivot to see whether "multiple email rows" hide true duplicates.

*Schema hint:* `signups(user_id INT, email VARCHAR(255), touchpoint VARCHAR(10), created_at TIMESTAMP)`

**Query:**
```sql
SELECT user_id, email,
       COUNT(*) FILTER (WHERE touchpoint = 'web')   AS web_cnt,
       COUNT(*) FILTER (WHERE touchpoint = 'app')   AS app_cnt,
       COUNT(*) FILTER (WHERE touchpoint = 'api')   AS api_cnt,
       COUNT(*) AS total
FROM signups
GROUP BY user_id, email
HAVING COUNT(*) > 1;
```
**Explanation:** Conditional COUNT pivots touchpoints into columns, surfacing who genuinely duplicated an email.

**Alt1 (PIVOT operator, SQL Server):**
```sql
SELECT user_id, email, [web], [app], [api]
FROM (
  SELECT user_id, email, touchpoint
  FROM signups
) src
PIVOT (
  COUNT(touchpoint)
  FOR touchpoint IN ([web], [app], [api])
) pvt;
```
**Explanation:** The PIVOT operator rotates touchpoints into columns directly.

---

## Q95: Top-N Per Group With IGNORE NULLS

*Scenario:* Rank customers by their last order value, skipping rows where the null amount column would pollute the order.

*Schema hint:* `orders(id INT PK, customer_id INT, order_date DATE, amount DECIMAL)`

**Query (Oracle / DuckDB):**
```sql
SELECT customer_id, order_date, amount,
       FIRST_VALUE(amount IGNORE NULLS) OVER (
         PARTITION BY customer_id ORDER BY order_date DESC
       ) AS most_recent_amount
FROM orders;
```
**Explanation:** IGNORE NULLS makes FIRST_VALUE skip null amounts and return the last real value.

**Alt1 (Windowing without IGNORE NULLS):**
```sql
SELECT customer_id, order_date, amount,
       MAX(amount) OVER (PARTITION BY customer_id) AS most_recent_amount
FROM orders;
```
**Explanation:** Cross-dialect fallback — MAX over the partition yields the latest non-null value when the column is monotonic.

---

## Q96: Index-Supported Dedup Strategy

*Scenario:* Speed up dedup on a huge table by creating a covering index for the dedup predicate.

*Schema hint:* `huge_log(id BIGINT PK, tenant_id INT, event_id VARCHAR(50), ts TIMESTAMP)`

**Query:**
```sql
CREATE INDEX ix_tenant_event ON huge_log (tenant_id, event_id, id);

WITH ranked AS (
  SELECT id, ROW_NUMBER() OVER (
    PARTITION BY tenant_id, event_id ORDER BY id
  ) AS rn
  FROM huge_log
)
DELETE FROM huge_log WHERE id IN (SELECT id FROM ranked WHERE rn > 1);
```
**Explanation:** The index covers the partition/order columns, so the window scans index pages instead of the heap.

**Alt1 (Recursive batched delete):**
```sql
DELETE FROM huge_log
WHERE id IN (
  SELECT id FROM (
    SELECT id, ROW_NUMBER() OVER (PARTITION BY tenant_id, event_id ORDER BY id) AS rn
    FROM huge_log
  ) t WHERE rn > 1
  LIMIT 5000
);
-- Re-run until 0 rows affected
```
**Explanation:** Recursive chunking keeps each delete small; the covering index keeps each scan cheap.

---

## Q97: Top-N Per Group With ROLLUP

*Scenario:* Report top salespeople per region, plus an overall company winner, using ROLLUP grouping.

*Schema hint:* `sales(rep_name VARCHAR, region VARCHAR(30), amount DECIMAL)`

**Query:**
```sql
WITH ranked AS (
  SELECT rep_name, region, amount,
         ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC) AS rn
  FROM sales
)
SELECT region, rep_name, amount
FROM ranked
WHERE rn = 1

UNION ALL

SELECT 'COMPANY' AS region, rep_name, amount
FROM sales
ORDER BY amount DESC
LIMIT 1;
```
**Explanation:** Per-region winners come from the window; the company-wide winner comes from a plain LIMIT on the union.

**Alt1 (GROUPING SETS everywhere):**
```sql
SELECT COALESCE(region, 'COMPANY') AS region, rep_name, amount
FROM (
  SELECT region, rep_name, amount,
         ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC) AS rn
  FROM sales
) a
WHERE region IS NOT NULL AND rn = 1
UNION
SELECT 'COMPANY', rep_name, amount
FROM sales ORDER BY amount DESC LIMIT 1;
```
**Explanation:** Same outcome, organised so the ROLLUP-like company row is clearly identified.

---

## Q98: Dedup Using a Computed Expression in PARTITION BY

*Scenario:* Dedup sales by month, ignoring the day granularity: the partition key is itself a function.

*Schema hint:* `sales_fact(id INT PK, product_id INT, sold_at DATE, amount DECIMAL)`

**Query:**
```sql
WITH ranked AS (
  SELECT id, ROW_NUMBER() OVER (
    PARTITION BY product_id, DATE_TRUNC('month', sold_at)
    ORDER BY sold_at DESC, id DESC
  ) AS rn
  FROM sales_fact
)
DELETE FROM sales_fact WHERE id IN (SELECT id FROM ranked WHERE rn > 1);
```
**Explanation:** DATE_TRUNC in the PARTITION BY turns daily rows into monthly groups without a separate column.

**Alt1 (Extracted grouping column):**
```sql
ALTER TABLE sales_fact ADD COLUMN sold_month DATE GENERATED ALWAYS
  AS (DATE_TRUNC('month', sold_at)) STORED;

CREATE INDEX ix_sold_month ON sales_fact (product_id, sold_month, sold_at);

WITH ranked AS (
  SELECT id, ROW_NUMBER() OVER (
    PARTITION BY product_id, sold_month ORDER BY sold_at DESC
  ) AS rn
  FROM sales_fact
)
DELETE FROM sales_fact WHERE id IN (SELECT id FROM ranked WHERE rn > 1);
```
**Explanation:** Materialising the month into a stored generated column lets an index serve the partition directly.

---

## Q99: Cumulative (RANGE UNBOUNDED) Frame for Running Ranks

*Scenario:* Show each customer's running total at every order, then flag the order that pushes them into the top-3 cohort.

*Schema hint:* `orders(id INT PK, customer_id INT, amount DECIMAL, order_date DATE)`

**Query:**
```sql
WITH running AS (
  SELECT customer_id, order_date, amount,
         SUM(amount) OVER (
           PARTITION BY customer_id
           ORDER BY order_date, id
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
         ) AS running_total
  FROM orders
)
SELECT customer_id, order_date, amount, running_total
FROM running
ORDER BY customer_id, order_date;
```
**Explanation:** An unbounded-preceding frame accumulates each customer's lifetime total incrementally.

**Alt1 (Rank the accumulators):**
```sql
WITH running AS (
  SELECT customer_id, order_date, amount,
         SUM(amount) OVER (
           PARTITION BY customer_id ORDER BY order_date
           ROWS UNBOUNDED PRECEDING
         ) AS running_total
  FROM orders
)
SELECT * FROM (
  SELECT *, DENSE_RANK() OVER (
    PARTITION BY customer_id ORDER BY running_total DESC
  ) AS cohort_rank
  FROM running
) t WHERE cohort_rank <= 3;
```
**Explanation:** Ranking the running totals reuses the frame and identifies the top-3 cumulative cohorts.

---

## Q100: Master Pattern — A Complete Dedup & Top-N ETL Pipeline

*Scenario:* A full nightly job: dedup raw feeds, keep the newest version per entity, then emit the top 3 per category into a report table.

*Schema hint:* `raw_feed(id SERIAL PK, entity_id INT, category VARCHAR(30), val DECIMAL, seen_ts TIMESTAMPTZ)`, `report(category VARCHAR(30), entity_id INT, val DECIMAL, ranked_at TIMESTAMPTZ)`

**Query (Postgres transaction):**
```sql
BEGIN;

-- 1) Keep only the newest snapshot per entity in the raw feed
WITH keep_newest AS (
  SELECT id FROM (
    SELECT id, ROW_NUMBER() OVER (
      PARTITION BY entity_id ORDER BY seen_ts DESC, id DESC
    ) AS rn
    FROM raw_feed
  ) t WHERE rn > 1
)
DELETE FROM raw_feed WHERE id IN (SELECT id FROM keep_newest);

-- 2) Drop exact-duplicate rows that survived step 1
WITH exact_dupes AS (
  SELECT id FROM (
    SELECT id, ROW_NUMBER() OVER (
      PARTITION BY entity_id, category, val, seen_ts::date ORDER BY id
    ) AS rn
    FROM raw_feed
  ) t WHERE rn > 1
)
DELETE FROM raw_feed WHERE id IN (SELECT id FROM exact_dupes);

-- 3) Rebuild the report from the top 3 per category
TRUNCATE report;
INSERT INTO report (category, entity_id, val, ranked_at)
SELECT category, entity_id, val, NOW()
FROM (
  SELECT category, entity_id, val,
         ROW_NUMBER() OVER (
           PARTITION BY category ORDER BY val DESC
         ) AS rn
  FROM raw_feed
) t
WHERE rn <= 3;

COMMIT;
```
**Explanation:** One transaction chains the three idioms — newest-version pruning, exact-dup delete, and top-N-per-group projection — into an idempotent nightly job.

**Alt1 (Snapshot table + recompute without deleting):**
```sql
CREATE MATERIALIZED VIEW clean_feed AS
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY entity_id, category, val
    ORDER BY seen_ts DESC, id DESC
  ) AS rn
  FROM raw_feed
) t WHERE rn = 1;

TRUNCATE report;
INSERT INTO report (category, entity_id, val, ranked_at)
SELECT category, entity_id, val, NOW()
FROM (
  SELECT category, entity_id, val,
         ROW_NUMBER() OVER (PARTITION BY category ORDER BY val DESC) AS rn
  FROM clean_feed
) t WHERE rn <= 3;
```
**Explanation:** A materialised view gives repeatable reads, and the report is rebuilt each run without touching the raw table.
---
