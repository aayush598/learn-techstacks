# EXPLAIN and Execution Plans — 100 SQL Interview Q&A

## Q1: What does the MySQL EXPLAIN command reveal about a simple SELECT?

**Query:**
```sql
EXPLAIN SELECT id, name FROM employees WHERE department_id = 5;
```
**Explanation:** EXPLAIN shows the execution plan: which index MySQL picks, the access type (ALL, ref, range, etc.), estimated rows scanned, and any extra operations like filesort or temporary tables.

The output might look like:
```text
+----+-------------+------------+------+---------------+------+---------+------+------+----------+-------------+
| id | select_type | table      | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra       |
+----+-------------+------------+------+---------------+------+---------+------+------+----------+-------------+
|  1 | SIMPLE      | employees  | ref  | idx_dept      | idx_dept | 5     | const|  42  | 100.00   | Using index |
+----+-------------+------------+------+---------------+------+---------+------+------+----------+-------------+
```

## Q2: How does EXPLAIN ANALYZE differ from EXPLAIN in MySQL?

**Query:**
```sql
EXPLAIN ANALYZE SELECT id, name FROM employees WHERE department_id = 5;
```
**Explanation:** EXPLAIN ANALYZE actually executes the query and shows real execution time alongside the optimizer's estimates, exposing where the optimizer's row estimates were wrong.

A sample output:
```text
-> Index lookup on employees using idx_dept (department_id=5)  (cost=4.25 rows=42) (actual time=0.031..0.089 rows=150 loops=1)
    -> Multi-range index lookup  (cost=4.25 rows=42) (actual time=0.029..0.078 rows=150 loops=1)
```

**Alt1:** In PostgreSQL you achieve the same with `EXPLAIN (ANALYZE, BUFFERS) SELECT ...;` which also reports shared buffer hits and reads.

## Q3: What does the `type` column in MySQL EXPLAIN mean, from best to worst?

**Query:**
```sql
EXPLAIN SELECT * FROM orders WHERE id = 1001;
EXPLAIN SELECT * FROM orders WHERE customer_id = 42;
EXPLAIN SELECT * FROM orders WHERE amount > 500;
EXPLAIN SELECT * FROM orders WHERE status = 'pending';
```
**Explanation:** The `type` column indicates the access method. `const` is best (single row by primary key), followed by `eq_ref`, `ref`, `range`, `index`, and `ALL` (full table scan, worst). `ALL` signals a missing index or poor selectivity.

```text
type=const   -- primary key lookup, exactly one row
type=eq_ref  -- join using a unique/primary key, one row per combination
type=ref     -- non-unique index lookup, potentially many rows
type=range   -- index range scan (BETWEEN, >, <, IN list)
type=index   -- full index scan (reads every index entry)
type=ALL     -- full table scan, every row read
```

## Q4: How do you read a PostgreSQL EXPLAIN output?

**Query:**
```sql
EXPLAIN SELECT id, name FROM employees WHERE department_id = 5;
```
**Explanation:** PostgreSQL EXPLAIN returns a tree of plan nodes. Read top-down: the topmost node is the final output, leaf nodes are the data sources. Each node shows estimated cost, estimated rows, and width.

```text
Seq Scan on employees  (cost=0.00..35.50 rows=42 width=20)
  Filter: (department_id = 5)
```

## Q5: What extra information does `EXPLAIN (ANALYZE, BUFFERS)` provide in PostgreSQL?

**Query:**
```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT id, name FROM employees WHERE department_id = 5;
```
**Explanation:** ANALYZE executes the query and adds actual time and rows. BUFFERS adds shared hit/read/disk statistics, showing how many blocks came from cache vs. disk, which reveals I/O bottlenecks.

```text
Seq Scan on employees  (cost=0.00..35.50 rows=42 width=20) (actual time=0.012..0.485 rows=150 loops=1)
  Filter: (department_id = 5)
  Rows Removed by Filter: 850
  Shared Buffers: hit=12 read=3
Planning Time: 0.089 ms
Execution Time: 0.562 ms
```

**Alt1:** Add `SETTINGS` to also show which planner settings influenced the plan: `EXPLAIN (ANALYZE, BUFFERS, SETTINGS) SELECT ...;`

## Q6: How does `EXPLAIN FORMAT=JSON` in MySQL differ from the default tabular output?

**Query:**
```sql
EXPLAIN FORMAT=JSON SELECT o.id, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.amount > 500;
```
**Explanation:** JSON format gives a hierarchical view with nested cost estimates, actual rows, and access details per table. It is easier to parse programmatically and shows cost estimates at each step.

```json
{
  "query_block": {
    "select_id": 1,
    "cost_info": { "query_cost": "156.23" },
    "nested_loop": [
      {
        "table": {
          "table_name": "o",
          "access_type": "range",
          "key": "idx_amount",
          "rows_examined_per_scan": 312,
          "rows_produced_per_join": 312,
          "filtered": "100.00",
          "cost_info": { "read_cost": "125.00", "eval_cost": "31.20", "total_cost": "156.20" }
        }
      },
      {
        "table": {
          "table_name": "c",
          "access_type": "eq_ref",
          "key": "PRIMARY",
          "cost_info": { "read_cost": "0.03", "eval_cost": "0.31", "total_cost": "0.34" }
        }
      }
    ]
  }
}
```

## Q7: What does `EXPLAIN (FORMAT=TREE)` show in PostgreSQL?

**Query:**
```sql
EXPLAIN (FORMAT=TREE)
SELECT department_id, COUNT(*)
FROM employees
GROUP BY department_id
ORDER BY COUNT(*) DESC;
```
**Explanation:** TREE format shows a compact indented tree with cost, rows, and actual time per node. It is the most readable format for understanding plan hierarchy at a glance.

```text
Sort  (cost=41.18..42.18 rows=100 width=12) (actual time=0.142..0.151 rows=8 loops=1)
  Sort Key: (count(*)) DESC
  Sort Method: quicksort  Memory: 49kB
  ->  HashAggregate  (cost=35.50..38.50 rows=100 width=12) (actual time=0.101..0.119 rows=8 loops=1)
        Group Key: department_id
        Batches: 1  Memory Usage: 24kB
        ->  Seq Scan on employees  (cost=0.00..28.00 rows=1000 width=4) (actual time=0.011..0.068 rows=1000 loops=1)
Planning Time: 0.125 ms
Execution Time: 0.218 ms
```

## Q8: How do you read estimated vs. actual rows in a PostgreSQL plan?

**Query:**
```sql
EXPLAIN (ANALYZE)
SELECT * FROM orders WHERE customer_id = 7 AND status = 'shipped';
```
**Explanation:** The `rows=` after `actual time` is the actual count; the first `rows=` in the cost section is the estimate. A large mismatch (e.g., estimated 10 but actual 5000) means stale statistics causing poor plan choice.

```text
Seq Scan on orders  (cost=0.00..1850.00 rows=10 width=50) (actual time=0.023..12.456 rows=5000 loops=1)
  Filter: ((customer_id = 7) AND (status = 'shipped'))
  Rows Removed by Filter: 945000
Planning Time: 0.102 ms
Execution Time: 12.890 ms
```

**Alt1:** Run `ANALYZE orders;` first, then re-check the plan to see if the estimates now match actuals more closely.

## Q9: What does `SET STATISTICS IO ON` do in SQL Server?

**Query:**
```sql
SET STATISTICS IO ON;
SELECT id, name FROM employees WHERE department_id = 5;
SET STATISTICS IO OFF;
```
**Explanation:** It outputs logical/physical/read-ahead reads per table. `logical reads` is the most important number — it shows total page accesses and directly correlates with query cost.

```text
Table 'employees'. Scan count 1, logical reads 12, physical reads 0, read-ahead reads 0.
```

**Alt1:** Also run `SET STATISTICS TIME ON;` to get CPU and elapsed time for the full query.

## Q10: What is the difference between estimated and actual execution plans in SQL Server?

**Query:**
```sql
SET SHOWPLAN_XML ON;
SELECT * FROM orders WHERE order_date > '2025-01-01';
SET SHOWPLAN_XML OFF;
```
**Explanation:** The estimated plan is built by the optimizer before execution using statistics; the actual plan is captured after execution and includes real row counts, grants, and warnings. Mismatches reveal stale statistics or parameter sniffing.

**Alt1:** Use `SET STATISTICS PROFILE ON;` to see both estimated and actual rows side by side in a single result set.

## Q11: How do you use `EXPLAIN PLAN FOR` in Oracle?

**Query:**
```sql
EXPLAIN PLAN FOR
SELECT e.name, d.department_name
FROM employees e
JOIN departments d ON e.department_id = d.department_id
WHERE e.salary > 50000;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```
**Explanation:** Oracle stores the plan in `PLAN_TABLE`. `DBMS_XPLAN.DISPLAY` formats it into a readable tree showing operation, options, object name, cost, and cardinality for each step.

```text
----------------------------------------------------------------------------------------------
| Id  | Operation                    | Name        | Rows  | Bytes | Cost (%CPU)| Time     |
----------------------------------------------------------------------------------------------
|   0 | SELECT STATEMENT             |             |   500 | 23000 |    15  (7)| 00:00:01 |
|   1 |  NESTED LOOPS                |             |   500 | 23000 |    15  (7)| 00:00:01 |
|   2 |   TABLE ACCESS FULL          | EMPLOYEES   |   500 | 15000 |    10  (0)| 00:00:01 |
|   3 |   TABLE ACCESS BY INDEX ROWID| DEPARTMENTS |     1 |    16 |     1  (0)| 00:00:01 |
|   4 |    INDEX UNIQUE SCAN         | DEPT_ID_PK  |     1 |       |     0  (0)| 00:00:01 |
----------------------------------------------------------------------------------------------
```

## Q12: How do you read a plan top-down vs. bottom-up in PostgreSQL?

**Query:**
```sql
EXPLAIN
SELECT c.name, COUNT(o.id)
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.name;
```
**Explanation:** Read PostgreSQL plans top-down — the topmost node is the final result. Execution actually happens bottom-up: leaf nodes (Seq Scan, Index Scan) produce rows first, which flow upward through joins and aggregates. The highest-cost node at the top is where most time is spent.

```text
HashAggregate  (cost=285.40..285.41 rows=1 width=40)
  Group Key: c.name
  ->  Hash Join  (cost=1.05..256.00 rows=2940 width=36)
        Hash Cond: (o.customer_id = c.id)
        ->  Seq Scan on orders o  (cost=0.00..208.00 rows=10000 width=8)
        ->  Hash  (cost=1.10..1.10 rows=10 width=36)
              ->  Seq Scan on customers c  (cost=0.00..1.10 rows=10 width=36)
```

## Q13: What is a Seq Scan and when does PostgreSQL choose it?

**Query:**
```sql
EXPLAIN SELECT * FROM audit_log WHERE event_type = 'login';
```
**Explanation:** Seq Scan reads every row in the heap. PostgreSQL chooses it when the table is small, when no suitable index exists, or when the query planner estimates that scanning the entire table is cheaper than index lookups (poor selectivity or many rows needed).

```text
Seq Scan on audit_log  (cost=0.00..52340.00 rows=480000 width=80)
  Filter: (event_type = 'login')
```

**Alt1:** If you force an index with `SET enable_seqscan = OFF;` and re-run EXPLAIN, you can see what an alternative index-based plan would look like (never do this in production — use it only for analysis).

## Q14: When does MySQL choose `ALL` (full table scan) over an index?

**Query:**
```sql
EXPLAIN SELECT * FROM products WHERE stock_quantity > 0;
```
**Explanation:** MySQL chooses ALL when the WHERE clause matches a large fraction of the table (optimizer estimates full scan is cheaper), when no usable index exists, or when the optimizer considers index lookups + bookmark lookups more expensive than sequential reads.

```text
+----+-------------+----------+------+---------------+------+---------+------+------+-------------+
| id | select_type | table    | type | possible_keys | key  | key_len | ref  | rows | Extra       |
+----+-------------+----------+------+---------------+------+---------+------+------+-------------+
|  1 | SIMPLE      | products | ALL  | NULL          | NULL | NULL    | NULL | 9850 | Using where |
+----+-------------+----------+------+---------------+------+---------+------+------+-------------+
```

## Q15: What is an Index Only Scan in PostgreSQL and how do you identify it?

**Query:**
```sql
EXPLAIN SELECT customer_id FROM orders WHERE status = 'shipped';
```
**Explanation:** Index Only Scan reads all needed data directly from the index without visiting the heap. It appears when all requested columns are in the index and visibility map confirms all tuples are visible, making it the fastest scan type.

```text
Index Only Scan using idx_orders_status on orders  (cost=0.29..8234.56 rows=3500 width=4)
  Index Cond: (status = 'shipped')
```

## Q16: What does MySQL `const` type mean?

**Query:**
```sql
EXPLAIN SELECT * FROM users WHERE id = 42;
```
**Explanation:** `const` means MySQL reads exactly one row from the table using a unique or primary key lookup. The optimizer reads the row once at optimization time and substitutes the value, making it the fastest access method.

```text
+----+-------------+-------+-------+---------------+---------+---------+-------+------+-------+
| id | select_type | table | type  | possible_keys | key     | key_len | ref   | rows | Extra |
+----+-------------+-------+-------+---------------+---------+---------+-------+------+-------+
|  1 | SIMPLE      | users | const | PRIMARY       | PRIMARY | 4       | const |    1 |       |
+----+-------------+-------+-------+---------------+---------+---------+-------+------+-------+
```

## Q17: What does a SQL Server Clustered Index Seek look like?

**Query:**
```sql
SET SHOWPLAN_XML ON;
SELECT id, name FROM employees WHERE id = 100;
SET SHOWPLAN_XML OFF;
```
**Explanation:** A Clustered Index Seek reads rows directly from the B-tree of the clustered index using a key lookup. It is the most efficient access method in SQL Server — equivalent to PostgreSQL's Index Scan on a primary key, costing proportional to tree depth rather than table size.

```text
|--Clustered Index Seek(OBJECT([dbo].[employees]), SEEK([dbo].[employees].[id] = (100)) ORDERED FORWARD)
```

**Alt1:** A non-clustered index on a covering set of columns produces an Index Seek instead, avoiding the key lookup to the clustered index entirely.

## Q18: How do you interpret the `rows` vs. `rows examined` in a MySQL EXPLAIN ANALYZE?

**Query:**
```sql
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE customer_id = (SELECT id FROM customers WHERE email = 'alice@example.com');
```
**Explanation:** `rows` in EXPLAIN output is the optimizer's estimate of how many rows will be processed. In EXPLAIN ANALYZE, `actual rows` is the real count. When `rows examined` is much higher than `rows` sent, the query is reading far more data than it returns — a sign of missing indexes or poor filtering.

```text
-> Index lookup on customers using idx_email (email='alice@example.com')  (cost=1.02 rows=1) (actual time=0.024..0.025 rows=1 loops=1)
-> Filter: (o.customer_id = 1)  (cost=1850.00 rows=5000) (actual time=0.031..45.678 rows=4521 loops=1)
    -> Full scan on orders o  (cost=1850.00 rows=500000) (actual time=0.030..38.123 rows=500000 loops=1)
```

## Q19: What does "Using index" mean in the MySQL EXPLAIN Extra column?

**Query:**
```sql
EXPLAIN SELECT customer_id, order_date FROM orders WHERE status = 'pending';
```
**Explanation:** "Using index" (covering index) means MySQL satisfies the query entirely from the index without touching the table data. This dramatically reduces I/O since the index is smaller than the full row.

```text
+----+-------------+--------+-------+-------------------+---------+---------+------+------+--------------------------+
| id | select_type | table  | type  | possible_keys     | key     | key_len | ref  | rows | Extra                    |
+----+-------------+--------+-------+-------------------+---------+---------+------+------+--------------------------+
|  1 | SIMPLE      | orders | index | idx_status_cover   | idx_status_cover | NULL | NULL |  500 | Using where; Using index |
+----+-------------+--------+-------+-------------------+---------+---------+------+------+--------------------------+
```

## Q20: How do you identify a Nested Loop join in a plan?

**Query:**
```sql
EXPLAIN
SELECT e.name, d.department_name
FROM employees e
JOIN departments d ON e.department_id = d.id
WHERE e.salary > 60000;
```
**Explanation:** Nested Loop appears as "Nested Loop" (PostgreSQL/SQL Server) or "NESTED LOOPS" (Oracle) in the plan. For each row from the outer input, it seeks a matching row in the inner input. It is optimal when the outer input is small or the inner input has an efficient index.

```text
Nested Loop  (cost=0.85..48.20 rows=30 width=40)
  ->  Index Scan using idx_emp_salary on employees e  (cost=0.29..35.12 rows=30 width=20)
        Index Cond: (salary > 60000)
  ->  Index Scan using departments_pkey on departments d  (cost=0.14..0.35 rows=1 width=24)
        Index Cond: (id = e.department_id)
```

## Q21: How do you identify a Hash Join in PostgreSQL?

**Query:**
```sql
EXPLAIN
SELECT o.id, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.id;
```
**Explanation:** Hash Join builds a hash table from the smaller input (inner), then probes it with the larger input (outer). It appears as "Hash Join" in the plan. It is optimal for equijoins between large unsorted sets where neither side has an index on the join column.

```text
Hash Join  (cost=1.30..2356.40 rows=10000 width=28)
  Hash Cond: (o.customer_id = c.id)
  ->  Seq Scan on orders o  (cost=0.00..1850.00 rows=100000 width=8)
  ->  Hash  (cost=1.10..1.10 rows=10 width=28)
        ->  Seq Scan on customers c  (cost=0.00..1.10 rows=10 width=28)
```

## Q22: When does a Merge Join get chosen over Hash Join?

**Query:**
```sql
EXPLAIN
SELECT a.id, b.value
FROM large_table_a a
JOIN large_table_b b ON a.id = b.id;
```
**Explanation:** Merge Join is chosen when both inputs are sorted or cheaply sortable on the join key and are of similar size. It streams both inputs once, so it avoids the memory overhead of a hash table. Common when both sides already have matching indexes.

```text
Merge Join  (cost=0.87..24567.89 rows=500000 width=12)
  ->  Index Scan using idx_a_id on large_table_a a  (cost=0.43..12345.67 rows=500000 width=8)
  ->  Index Scan using idx_b_id on large_table_b b  (cost=0.43..11987.54 rows=500000 width=8)
```

## Q23: How does the database determine join order in a multi-table join?

**Query:**
```sql
EXPLAIN
SELECT o.id, c.name, p.product_name
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id;
```
**Explanation:** The optimizer picks join order to minimize total cost. It generally starts with the most selective join (driving from a table with fewest rows after filtering) and joins progressively larger tables. The plan tree reveals this: the leftmost leaf is the driving table.

```text
Nested Loop  (cost=4.56..98.12 rows=15 width=80)
  ->  Nested Loop  (cost=3.28..82.34 rows=15 width=56)
        ->  Nested Loop  (cost=2.01..65.42 rows=15 width=44)
              ->  Index Scan using idx_cust_email on customers c  (cost=0.56..1.12 rows=1 width=20)
                    Filter: (name IS NOT NULL)
              ->  Index Scan using idx_orders_cust on orders o  (cost=1.45..62.50 rows=15 width=24)
                    Index Cond: (customer_id = c.id)
        ->  Index Scan using idx_order_items_order on order_items oi  (cost=1.27..1.68 rows=3 width=12)
              Index Cond: (order_id = o.id)
  ->  Index Scan using products_pkey on products p  (cost=1.14..1.16 rows=1 width=24)
        Index Cond: (id = oi.product_id)
```

## Q24: What does `Using filesort` mean in MySQL EXPLAIN?

**Query:**
```sql
EXPLAIN SELECT id, customer_id, order_date FROM orders ORDER BY total_amount DESC LIMIT 10;
```
**Explanation:** `Using filesort` means MySQL must perform an extra sorting pass because it cannot use an index to retrieve rows in the requested order. Despite the name, it does not always write to disk — it may sort in memory using a sort buffer.

```text
+----+-------------+--------+------+---------------+------+---------+------+------+----------------+
| id | select_type | table  | type | possible_keys | key  | key_len | ref  | rows | Extra          |
+----+-------------+--------+------+---------------+------+---------+------+------+----------------+
|  1 | SIMPLE      | orders | ALL  | NULL          | NULL | NULL    | NULL | 100K | Using filesort |
+----+-------------+--------+------+---------------+------+---------+------+------+----------------+
```

**Alt1:** Add a composite index on `(total_amount DESC, id, customer_id, order_date)` to eliminate the filesort and enable an index scan in the desired order.

## Q25: What does `Using temporary` mean in MySQL EXPLAIN?

**Query:**
```sql
EXPLAIN SELECT department_id, COUNT(*)
FROM employees
GROUP BY department_id
ORDER BY department_id;
```
**Explanation:** `Using temporary` means MySQL creates a temporary table to hold intermediate results, typically for GROUP BY or DISTINCT when it cannot use an index efficiently. Temp tables may be written to disk if they exceed `tmp_table_size`.

```text
+----+-------------+------------+-------+---------------+-----------+---------+------+------+------------------------------+
| id | select_type | table      | type  | possible_keys | key       | key_len | ref  | rows | Extra                        |
+----+-------------+------------+-------+---------------+-----------+---------+------+------+------------------------------+
|  1 | SIMPLE      | employees  | index | idx_dept      | idx_dept  | 5       | NULL | 1000 | Using temporary; Using index |
+----+-------------+------------+-------+---------------+-----------+---------+------+------+------------------------------+
```

## Q26: Why would an index be eliminated from the plan even though it exists?

**Query:**
```sql
EXPLAIN SELECT * FROM orders WHERE status = 'shipped' AND amount > 100;
```
**Explanation:** An existing index is skipped when the optimizer estimates the index is not selective enough (too many matching rows), when it cannot help with the filter, or when another index is cheaper. The absence of the key in the EXPLAIN `key` column shows it was eliminated.

## Q27: How does using a function on an indexed column kill index usage?

**Query:**
```sql
EXPLAIN SELECT * FROM orders WHERE YEAR(order_date) = 2025;
```
**Explanation:** Wrapping the indexed column in a function (YEAR, UPPER, DATE) means the stored index values do not match the search key, forcing a full scan (type ALL). Avoid the function or use a function-based / expression index.

```text
+----+-------------+--------+------+---------------+------+---------+------+------+-------------+
| id | select_type | table  | type | possible_keys | key  | key_len | ref  | rows | Extra       |
+----+-------------+--------+------+---------------+------+---------+------+------+-------------+
|  1 | SIMPLE      | orders | ALL  | NULL          | NULL | NULL    | NULL | 100K | Using where |
+----+-------------+--------+------+---------------+------+---------+------+------+-------------+
```

**Alt1:** Rewrite as a `BETWEEN` comparison on the raw column: `WHERE order_date >= '2025-01-01' AND order_date < '2026-01-01'`.

## Q28: How do implicit type casts cause full scans?

**Query:**
```sql
EXPLAIN SELECT * FROM users WHERE phone = 1234567890;
```
**Explanation:** If `phone` is VARCHAR, comparing it to a numeric literal forces MySQL to cast the column to a number for every row, disabling the index. The fix is to compare against a string literal so the cast is applied to the constant instead.

**Alt1:** In PostgreSQL the same trap applies: `WHERE phone::int = 12345` never uses the index unless you build an expression index on `(phone::int)`.

## Q29: Why do OR conditions often disable index usage?

**Query:**
```sql
EXPLAIN SELECT * FROM orders
WHERE status = 'shipped' OR customer_id = 42;
```
**Explanation:** A single index cannot serve two disjoint predicates in a straightforward Index Scan. Without index merge, MySQL falls back to ALL. Rewriting as a UNION ALL with separate index-friendly branches, or adding a composite index, often restores index usage.

```text
+----+-------------+--------+------+---------------+------+---------+------+------+-------------+
| id | select_type | table  | type | possible_keys | key  | key_len | ref  | rows | Extra       |
+----+-------------+--------+------+---------------+------+---------+------+------+-------------+
|  1 | SIMPLE      | orders | ALL  | idx_status,idx_customer | NULL | NULL | NULL | 100K | Using where |
+----+-------------+--------+------+---------------+------+---------+------+------+-------------+
```

**Alt1:** MySQL 8.0 can use index merge — EXPLAIN shows `Extra: Using union(idx_status,idx_customer)` when the optimizer merges two range scans.

## Q30: Why does LIKE with a leading wildcard prevent index usage?

**Query:**
```sql
EXPLAIN SELECT * FROM products WHERE name LIKE '%laptop%';
```
**Explanation:** A leading wildcard (`%laptop%`, `_laptop%`) means the prefix of the value is unknown, so the B-tree index cannot be navigated. Only suffix-prefixed patterns (`laptop%`) can use a range scan. Use full-text search or a trigram index for infix matching.

## Q31: Look at this plan — why is the IN list being handled poorly?

**Query:**
```sql
EXPLAIN SELECT * FROM orders WHERE customer_id IN (1, 2, 3, 4, 5);
```
**Explanation:** The plan shows a range scan on the customer index, which is good. The problem would be if EXPLAIN shows ALL — which happens when the list is very long (thousands of values), exceeds `in` trimming thresholds, or no index exists. Each IN value is internally a range probe on the index.

```text
+----+-------------+--------+-------+---------------+---------+---------+------+------+-------------+
| id | select_type | table  | type  | possible_keys | key     | key_len | ref  | rows | Extra       |
+----+-------------+--------+-------+---------------+---------+---------+------+------+-------------+
|  1 | SIMPLE      | orders | range | idx_customer  | idx_customer | 5 | NULL | 1452 | Using where |
+----+-------------+--------+-------+---------------+---------+---------+------+------+-------------+
```

**Alt1:** For very large IN lists, a temp-table JOIN is sometimes faster: `SELECT o.* FROM orders o JOIN (VALUES (1),(2),(3)) AS v(cid) ON o.customer_id = v.cid;`

## Q32: Why do correlated subqueries re-evaluate per row and how does the plan show it?

**Query:**
```sql
EXPLAIN
SELECT e.name,
       (SELECT MAX(o.amount) FROM orders o WHERE o.customer_id = e.id)
FROM employees e;
```
**Explanation:** Correlated subqueries depend on the outer row, so MySQL materializes or re-executes them per outer row (`loops=1000` in EXPLAIN ANALYZE means 1000 executions). The plan shows "Select tables optimized away" only when the subquery can be un-correlated.

```text
-> Select #2 (subquery in projection; run only once)  (cost=... rows=1) (actual time=0.012..0.045 rows=1 loops=1000)
    -> Filter: (o.customer_id = e.id)  (cost=1.25 rows=1)
        -> Index lookup on orders using idx_customer (customer_id=e.id)
```

**Alt1:** Rewrite as a left join with a GROUP BY or use a lateral join (PostgreSQL: `LEFT JOIN LATERAL`) to push the join to the planner instead of re-evaluating.

## Q33: How do you spot a sort without an index in a plan?

**Query:**
```sql
EXPLAIN
SELECT id, customer_id, order_date FROM orders ORDER BY order_date DESC, id DESC;
```
**Explanation:** PostgreSQL shows a `Sort` node and MySQL shows `Using filesort` when ordered retrieval needs an explicit sort. If the ORDER BY columns matched the index column order, the scan itself would produce rows in order and the Sort node would disappear.

```text
Sort  (cost=8450.23..8700.34 rows=100000 width=20)
  Sort Key: order_date DESC, id DESC
  Sort Method: external merge  Disk: 2344kB
  ->  Seq Scan on orders  (cost=0.00..1850.00 rows=100000 width=20)
```

**Alt1:** Add `CREATE INDEX idx_orders_date_id ON orders (order_date DESC, id DESC);` — the Sort node vanishes from the plan and disk spill is eliminated.

## Q34: This table has an index on status. Why is EXPLAIN showing a full scan?

**Query:**
```sql
EXPLAIN SELECT * FROM orders WHERE status = 'failed';
```
**Explanation:** If 60% of rows are 'failed', the optimizer estimates the index scan plus row lookups is more expensive than a sequential read. `rows` will show a large fraction of the table. Low selectivity makes the index useless to the planner.

```text
+----+-------------+--------+------+---------------+------+---------+------+--------+-------------+
| id | select_type | table  | type | possible_keys | key  | key_len | ref  | rows   | Extra       |
+----+-------------+--------+------+---------------+------+---------+------+--------+-------------+
|  1 | SIMPLE      | orders | ALL  | idx_status    | NULL | NULL    | NULL | 600000 | Using where |
+----+-------------+--------+------+---------------+------+---------+------+--------+-------------+
```

## Q35: What is limit pushdown and how does it appear in a plan?

**Query:**
```sql
EXPLAIN SELECT id, amount FROM orders WHERE status = 'shipped' ORDER BY order_date DESC LIMIT 5;
```
**Explanation:** Limit pushdown means the planner understands only a few rows are needed and applies the limit early. PostgreSQL shows `Limit` at the top that stops the underlying index scan early; MySQL shows `rows <= 5` before the ORDER BY when the sort can be partially satisfied.

```text
Limit  (cost=0.29..32.12 rows=5 width=20)
  ->  Index Scan Backward using idx_orders_date_status on orders  (cost=0.29..2345.45 rows=427 width=20)
        Index Cond: (status = 'shipped')
```

## Q36: What do "temp files", "external merge", and "Disk:" mean in a PostgreSQL EXPLAIN ANALYZE?

**Query:**
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT customer_id, COUNT(*)
FROM orders
GROUP BY customer_id
ORDER BY COUNT(*) DESC;
```
**Explanation:** `Sort Method: external merge Disk:` means the sort spilled to disk because it exceeded `work_mem`; `Batches:` in HashAggregate means the hash table spilled to temp files. Both signal memory pressure — the fix is raising work_mem or rewriting the query.

```text
Sort  (cost=12000.44..12312.56 rows=50000 width=12) (actual time=67.45..75.89 rows=50000 loops=1)
  Sort Key: (count(*)) DESC
  Sort Method: external merge  Disk: 8912kB
  ->  Finalize GroupAggregate  (cost=4000.12..8901.34 rows=50000 width=12) (actual time=12.33..34.56 rows=50000 loops=1)
        Group Key: customer_id
        ->  Gather Merge  (cost=4000.12..8801.22 rows=100000 width=12) (actual time=11.22..30.11 rows=100000 loops=1)
```

**Alt1:** `SET work_mem = '64MB';` for the session and re-run — if the plan changes and disk spill disappears, work_mem was the bottleneck.

## Q37: Why does estimated `rows` differ wildly from actual `rows`?

**Query:**
```sql
EXPLAIN (ANALYZE) SELECT * FROM orders WHERE created_at > now() - interval '1 hour';
```
**Explanation:** If statistics are stale or no histogram data covers the range, the optimizer guesses. Stale `pg_statistic` from infrequent ANALYZE, or a correlated column the statistics do not capture, produces estimates like `rows=10` while actual is `rows=50000`. The plan then often picks the wrong join type.

## Q38: How do stale statistics change a plan?

**Query:**
```sql
EXPLAIN (ANALYZE)
SELECT * FROM orders
WHERE customer_id = 9999 AND order_date >= '2025-01-01';
```
**Explanation:** The planner estimates based on cached statistics, not current data. After a bulk insert, statistics might say 5 rows per customer when reality is 5000, pushing the planner to a Nested Loop (fast for small input) that performs terribly at runtime. Fix with `ANALYZE`.

## Q39: You changed an index. How do you verify the fix with EXPLAIN?

**Query:**
```sql
CREATE INDEX idx_orders_cust_date ON orders (customer_id, order_date DESC);
EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 9999 AND order_date >= '2025-01-01';
```
**Explanation:** Before the fix you saw `Seq Scan`/`ALL` with an `rows` estimate mismatch; after the fix the plan should show an index range scan with `rows` matching actuals. If EXPLAIN still shows the old scan, analyze the table so the optimizer recognizes the new index.

```text
Index Scan using idx_orders_cust_date on orders  (cost=0.29..45.67 rows=150 width=50)
  Index Cond: ((customer_id = 9999) AND (order_date >= '2025-01-01'))
  Filter: (order_date >= '2025-01-01')
```
Additional over-filtering may be visible as `Rows Removed by Filter` — read it to confirm no secondary predicates linger.

**Alt1:** Compare before and after with `EXPLAIN (ANALYZE, BUFFERS)` and check both `Execution Time` and whether `Rows Removed by Filter` dropped to zero.

## Q40: Reading this plan, what index would you propose?

**Query:**
```sql
EXPLAIN
SELECT product_id, SUM(quantity)
FROM order_items
WHERE order_date BETWEEN '2025-01-01' AND '2025-01-31'
GROUP BY product_id;
```
**Explanation:** The planner used a filter scan because there is no index combining all predicates. An index on `(order_date, product_id)` — with quantity added for a covering index — allows range scan on order_date and keeps GROUP BY orderable. The plan then shows an Index Range Scan plus Index Only Scan.

```text
Finalize GroupAggregate  (cost=0.44..2456.30 rows=5230 width=12)
  Group Key: product_id
  ->  Incremental Sort  (cost=0.44..1895.55 rows=5230 width=12)
        Sort Key: product_id
        ->  Index Scan using idx_order_date on order_items  (cost=0.44..1234.11 rows=5230 width=12)
              Index Cond: (order_date BETWEEN ... AND ...)
```

## Q41: Reading this plan, what schema change would you propose?

**Query:**
```sql
EXPLAIN
SELECT c.country, AVG(o.amount)
FROM orders o
JOIN customers c ON o.customer_id = c.id
GROUP BY c.country;
```
**Explanation:** The plan shows a huge Hash Join on a materialized hash of customers — fine for one off, bad for a hot dashboard. Schema-level options: add an index on `orders(customer_id)` so the join can stream, or add generated columns / a pre-aggregated summary table on `(country, month)` to eliminate the scan entirely.

## Q42: Reading this plan, what query rewrite would you propose?

**Query:**
```sql
EXPLAIN
SELECT e.id
FROM employees e
WHERE e.salary > (SELECT AVG(salary) FROM employees);
```
**Explanation:** The subquery is re-evaluated or materialized per row, and EXPLAIN shows it under the outer scan. Rewriting with a CROSS JOIN to a single materialized average lets the planner compute the average once and removes per-row re-evaluation.

**Alt1:** PostgreSQL form: `WITH avg_sal AS (SELECT AVG(salary) FROM employees) SELECT e.id FROM employees e, avg_sal WHERE e.salary > avg_sal.avg;` — the plan shows a single GroupAggregate feeding the scan.

## Q43: What does the MySQL `USE INDEX` hint do?

**Query:**
```sql
SELECT * FROM orders USE INDEX (idx_customer) WHERE customer_id = 5;
```
**Explanation:** `USE INDEX` tells MySQL to restrict its search to the named index (it may still fall back if unusable). MySQL 8.0 uses `/*+ INDEX(orders idx_customer) */` optimizer hints instead; the plan's `key` column reflects which index was honored.

## Q44: What does the MySQL `IGNORE INDEX` hint do?

**Query:**
```sql
SELECT * FROM orders IGNORE INDEX (idx_status) WHERE status = 'pending';
```
**Explanation:** `IGNORE INDEX` prevents MySQL from using the listed index even if it looks attractive, forcing it to consider other indexes or a full scan. Useful when a stale-statistics-driven choice is known bad. Use with caution — the hint applies to the whole statement lifetime.

```text
+----+-------------+--------+------+---------------+------+---------+------+------+-------------+
| id | select_type | table  | type | possible_keys | key  | key_len | ref  | rows | Extra       |
+----+-------------+--------+------+---------------+------+---------+------+------+-------------+
|  1 | SIMPLE      | orders | ALL  | NULL          | NULL | NULL    | NULL | 100K | Using where |
+----+-------------+--------+------+---------------+------+---------+------+------+-------------+
```

## Q45: What does the SQL Server `FORCESEEK` hint do?

**Query:**
```sql
SELECT * FROM orders WITH (FORCESEEK) WHERE customer_id = 42;
```
**Explanation:** `FORCESEEK` forces the optimizer to use an index seek instead of a table scan. Options like `WITH (FORCESEEK, INDEX(idx_customer))` also pin the index. It is a tuning tool for pathological plans, not a permanent fix — prefer fixing statistics or the schema.

**Alt1:** Use query hints in `OPTION (RECOMPILE)` or `OPTION (HASH JOIN, MERGE JOIN)` as alternatives to FORCESEEK when testing plan variants.

## Q46: PostgreSQL has no optimizer hints by default. How do you influence plan choice?

**Query:**
```sql
EXPLAIN
SELECT * FROM orders WHERE customer_id = 42;
```
**Explanation:** Default PostgreSQL honors planner settings per session: `SET enable_seqscan = off;` disables sequence scans (useful for seeing alternative plans), but the documented recommendation is the `pg_hint_plan` extension for real hints. Prefer rewriting queries and improving statistics over hints.

## Q47: What are join hints in SQL Server?

**Query:**
```sql
SELECT o.id, c.name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
OPTION (MERGE JOIN);
```
**Explanation:** `OPTION (LOOP JOIN)`, `(HASH JOIN)`, or `(MERGE JOIN)` constrains the join strategy. The plan operator changes accordingly (Nested Loops, Hash Match, or Merge Join). Used to test hypotheses during tuning; a well-optimized plan should not need them.

## Q48: What is the difference between ANALYZE and VACUUM in PostgreSQL?

**Query:**
```sql
ANALYZE orders;
VACUUM ANALYZE orders;
```
**Explanation:** ANALYZE collects statistics (row counts, histogram data) used by the planner; it does not reclaim storage. VACUUM reclaims dead tuple space. `VACUUM ANALYZE` does both. Stale statistics cause bad plans; dead tuples cause bloat and slow scans.

## Q49: What does `UPDATE STATISTICS` do in SQL Server?

**Query:**
```sql
UPDATE STATISTICS dbo.orders WITH FULLSCAN;
```
**Explanation:** It rebuilds the statistics histogram for the index/table. FULLSCAN samples every row for accuracy at higher cost, while the default samples a subset. After bulk loads, run this before trusting the execution plan; SELECT queries never auto-trigger stats refresh for new columns.

**Alt1:** Check freshness first: `SELECT name, last_updated, rows, rows_sampled FROM sys.dm_db_stats_properties(OBJECT_ID('dbo.orders'), 1);`

## Q50: What are histograms and how do they matter in plans?

**Query:**
```sql
EXPLAIN SELECT * FROM orders WHERE amount BETWEEN 100 AND 110;
```
**Explanation:** A histogram stores value-frequency distribution for a column, letting the planner estimate how many rows fall in a range. If the histogram is stale or missing for that column, the estimate goes to a fraction heuristic (e.g., default selectivity), causing rows-count mismatches and wrong join/scan decisions.

## Q51: What are startup cost and total cost in a PostgreSQL plan?

**Query:**
```sql
EXPLAIN (FORMAT TEXT, COSTS ON)
SELECT * FROM orders WHERE status = 'shipped';
```
**Explanation:** `startup cost` is the work before the node emits the first row (building a hash table, sorting, reaching the first index entry). `total cost` is projected work to emit all rows. When choosing between plans, the optimizer maximizes how cheaply the first row appears — crucial for LIMIT queries.

```text
Index Scan using idx_orders_status on orders  (cost=0.29..8234.56 rows=3500 width=50)
  Startup cost high (0.29), total cost high (8234.56)
Hash Join  (cost=1.30..2356.40 rows=10000 width=28)
  Startup cost low (1.30) vs total cost low (2356.40)
```

## Q52: How do you find the dominant cost node in a nested plan?

**Query:**
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT o.id, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.status = 'shipped' AND c.plan = 'premium';
```
**Explanation:** The dominant node is where the highest `actual time` and `buffers hit` accumulate — usually the leaf doing the largest scan. Look for the biggest `actual time` spread and `Rows Removed by Filter`; that node is the bottleneck to attack first with an index.

```text
Hash Join  (cost=240.56..12876.89 rows=4521 width=28) (actual time=12.44..234.56 rows=4521 loops=1)
  Hash Cond: (o.customer_id = c.id)
  ->  Index Scan using idx_orders_status on orders o  (cost=0.29..10456.78 rows=4521 width=20) (actual time=0.012..218.456 rows=4521 loops=1)
        Index Cond: (status = 'shipped')
  ->  Hash  (cost=240.00..240.00 rows=4000 width=12) (actual time=0.400..0.401 rows=4000 loops=1)
        Buckets: 8192  Batches: 1  Memory Usage: 198kB
        ->  Seq Scan on customers c  (cost=0.00..240.00 rows=4000 width=12) (actual time=0.023..0.134 rows=4000 loops=1)
```

## Q53: When should the optimizer pick Nested Loop over Hash Join?

**Query:**
```sql
EXPLAIN
SELECT o.id, o.amount
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE c.country = 'US' AND o.status = 'shipped';
```
**Explanation:** Nested Loop wins when the driving side (outer) is small — e.g., after filtering `country = 'US'` only 200 customers remain — and the inner side has an index on the join key. Each of the 200 outer rows does an index seek; total cost stays low. Hash Join wins when both sides are large and unindexed.

```text
Nested Loop  (cost=1.25..568.34 rows=1800 width=16) (actual time=0.045..22.30 rows=1800 loops=1)
  ->  Index Scan using idx_customers_country on customers c  (cost=0.44..34.12 rows=200 width=8) (actual time=0.021..1.23 rows=200 loops=1)
        Index Cond: (country = 'US')
  ->  Index Scan using idx_orders_customer on orders o  (cost=0.28..2.55 rows=9 width=12) (actual time=0.045..0.089 rows=9 loops=200)
        Index Cond: (customer_id = c.id)
```

**Alt1:** If the inner index is missing, the optimizer shows a `Materialize` or `Seq Scan` on orders instead of an index seek. Adding `idx_orders_customer(customer_id)` is the fix that converts the plan from Hash to Nested Loop.

## Q54: When does Hash Join beat Merge Join, and vice versa?

**Query:**
```sql
EXPLAIN
SELECT a.id, b.val
FROM events_a a
JOIN events_b b ON a.key = b.key;
```
**Explanation:** Hash wins when inputs are large, unsorted, and equi-join keyed — building a hash table on the smaller input is O(n log n)-ish with cheap probes. Merge wins when both inputs are already sorted on the join key (e.g., both from an index), streaming both with zero hash-table memory.

```text
Hash Join  (cost=4567.89..12890.45 rows=1000000 width=16)
  Hash Cond: (a.key = b.key)
  ->  Seq Scan on events_a a  (cost=0.00..4567.00 rows=1000000 width=8)
  ->  Hash  (cost=1789.00..1789.00 rows=500000 width=8)
        ->  Seq Scan on events_b b  (cost=0.00..1789.00 rows=500000 width=8)
```

## Q55: What is parameter sniffing in SQL Server?

**Query:**
```sql
CREATE PROC dbo.GetOrders @cust INT AS
  SELECT * FROM orders WHERE customer_id = @cust;
GO
EXEC dbo.GetOrders @cust = 5;     -- compiles plan for sniffer value 5
EXEC dbo.GetOrders @cust = 99999; -- reuses the cached plan
```
**Explanation:** SQL Server compiles the plan using the first parameter value it sees and caches it for reuse. If that value represents few rows but a later value matches millions, the cached Nested Loop plan performs terribly. The mismatch is exposed by comparing estimated vs. actual rows in the captured plan.

**Alt1:** Fixes include `OPTION (RECOMPILE)`, `OPTION (OPTIMIZE FOR UNKNOWN)`, forcing a `MERGE/HASH JOIN`, or using `WITH (RECOMPILE)` on the proc.

## Q56: How do you detect and diagnose parameter sniffing in a captured plan?

**Query:**
```sql
SET SHOWPLAN_XML ON;
EXEC dbo.GetOrders @cust = 99999;
SET SHOWPLAN_XML OFF;
```
**Explanation:** The actual plan shows `Actual Rows` far above `Estimated Rows` on an operator, and the plan shape is a narrow Nested Loop styled for a small result. That mismatch against a high-selectivity sniffed value is the classic sniffing fingerprint.

**Alt1:** Query plan cache metadata to confirm reuse: `SELECT plan_handle, usecounts FROM sys.dm_exec_cached_plans WHERE objtype='Proc' AND cacheobjtype='Compiled Plan';` with `sys.dm_exec_query_stats`.

## Q57: How does plan caching reduce query latency, and what breaks it?

**Query:**
```sql
SELECT * FROM orders WHERE customer_id = 42 AND status = 'shipped';
```
**Explanation:** The optimizer skips re-optimization when it finds a matching cached plan — cutting compile time. Breaks: every literal differs (no parameterization, generating separate plans per value), schema/index changes invalidate plans, and memory pressure evicts them. Plan cache bloat itself adds lookup overhead.

## Q58: How do you read `EXPLAIN FORMAT=JSON` and inspect actual execution time in MySQL?

**Query:**
```sql
EXPLAIN FORMAT=JSON
SELECT o.id, o.amount
FROM orders o
WHERE o.customer_id = 7 AND o.status = 'shipped';
```
**Explanation:** The JSON contains `"cost_info"`, `"rows_examined_per_scan"`, and `"rows_produced_per_join"` per table. But note: raw EXPLAIN (even JSON) is an estimate — actual time requires EXPLAIN ANALYZE. A JSON plan showing `"rows_examined_per_scan": 500000` with `"rows_produced_per_join": 5` flags a missing index.

## Q59: How do you interpret a MySQL `EXPLAIN FORMAT=TREE` output?

**Query:**
```sql
EXPLAIN FORMAT=TREE
SELECT c.name, COUNT(o.id)
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.name;
```
**Explanation:** TREE output nests operators with cost, actual rows, and loops — identical to PostgreSQL. The root is the final projection; each indented level is a child node. `loops` reveals re-execution; a join node with `loops=1000` and index lookups inside signals N+1.

```text
-> Group aggregation: (count(o.id))  (cost=48.31 rows=10) (actual time=0.123..6.456 rows=10 loops=1)
    -> Nested loop left join  (cost=26.77 rows=5230) (actual time=0.023..4.890 rows=5230 loops=1)
        -> Covering index scan on c using PRIMARY  (cost=1.10 rows=10) (actual time=0.011..0.045 rows=10 loops=1)
        -> Index lookup on o using idx_customer_id (customer_id=c.id)  (cost=2.55 rows=523) (actual time=0.012..0.389 rows=523 loops=10)
```

## Q60: What is the difference between an Index Scan and an Index Only Scan?

**Query:**
```sql
EXPLAIN (ANALYZE)
-- Query A: needs extra column not in index
SELECT * FROM products WHERE category_id = 4;
-- Query B: columns fully in index
SELECT category_id id, name FROM products WHERE category_id = 4;
```
**Explanation:** Query A does an Index Scan: index finds the matching row pointers, then the heap (`factor table`) must be visited per row — visible as a `Heap Fetches` or a separate `Table Access by Index RowID`. Query B does an Index Only Scan because every requested column is in the index (covering index), avoiding heap visits entirely.

**Alt1:** Add a covering index `(category_id, name)` to turn Query A into an Index Only Scan, removing heap fetches from the plan.

## Q61: What is a Parallel Seq Scan in PostgreSQL?

**Query:**
```sql
EXPLAIN (ANALYZE)
SELECT COUNT(*) FROM events WHERE occurred_at >= '2025-01-01';
```
**Explanation:** Parallel workers split the table into chunks scanned concurrently. The plan shows workers launching under a Gather node; each worker reports its own rows and time. Parallelism is capped by `max_parallel_workers_per_gather` and only kicks in above the `min_parallel_table_scan_size` threshold.

```text
Finalize Aggregate  (cost=2345.67..2345.68 rows=1 width=8) (actual time=3.452..3.678 rows=1 loops=1)
  ->  Gather  (cost=2345.11..2345.32 rows=2 width=8) (actual time=3.001..3.410 rows=3 loops=1)
        Workers Planned: 2
        Workers Launched: 2
        ->  Partial Aggregate  (cost=2345.11..2345.12 rows=1 width=8) (actual time=0.023..0.045 rows=1 loops=3)
              ->  Parallel Seq Scan on events  (cost=0.00..1756.00 rows=356000 width=8) (actual time=0.011..1.967 rows=355000 loops=3)
                    Filter: (occurred_at >= '2025-01-01')
                    Rows Removed by Filter: 45000
Planning Time: 0.176 ms
Execution Time: 4.012 ms
```

## Q62: What is a Bitmap Index Scan in PostgreSQL?

**Query:**
```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE status IN ('shipped', 'in_transit');
```
**Explanation:** The planner reads index entries for both values into a bitmap, then merges/hashes them before heap scanning once. It avoids touching heap pages multiple times. The plan shows `BitmapAnd`/`BitmapOr` combining term bitmaps into `Bitmap Heap Scan`.

```text
Bitmap Heap Scan on orders  (cost=84.43..7234.12 rows=4500 width=50) (actual time=0.456..34.12 rows=4521 loops=1)
  Recheck Cond: (status = ANY ('{shipped,in_transit}'::text[]))
  Heap Blocks: exact=789
  ->  Bitmap Index Scan on idx_orders_status  (cost=0.00..83.56 rows=4500 width=0) (actual time=0.342..0.343 rows=4521 loops=1)
        Index Cond: (status = ANY ('{shipped,in_transit}'::text[]))
```

## Q63: How do CTEs (WITH ... AS) appear in a PostgreSQL plan?

**Query:**
```sql
EXPLAIN ANALYZE
WITH recent AS (SELECT * FROM orders WHERE order_date > '2025-01-01')
SELECT customer_id, COUNT(*) FROM recent GROUP BY customer_id;
```
**Explanation:** In PostgreSQL, a plain CTE is materialized (a `CTE Scan` node reads its materialized result) unless marked `MATERIALIZED` off or inlined. Since v12, materialization happens only when beneficial; a CTE that the optimizer decides to inline disappears from the plan. The materialization point is where the CTE's `rows` and `actual time` get reported.

**Alt1:** Use `WITH ... AS MATERIALIZED` vs `WITH ... AS NOT MATERIALIZED` explicitly to control whether it caches rows for repeated scans or inlines into the outer query.

## Q64: What does subquery join elimination look like in a PostgreSQL plan?

**Query:**
```sql
EXPLAIN
SELECT c.id
FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```
**Explanation:** The planner can push the EXISTS check into a join and remove the subquery node entirely. When it does, the plan shows a plain join (`Semi Join` in SQL Server terms) with an index on `orders(customer_id)`; the subquery plan node disappears from the tree.

## Q65: What is a residual predicate in a SQL Server plan?

**Query:**
```sql
SET SHOWPLAN_XML ON;
SELECT * FROM orders WHERE status = 'shipped' AND amount % 100 = 0;
SET SHOWPLAN_XML OFF;
```
**Explanation:** A residual predicate (shown as `Residual:` on an operator) is checked for every row the index seek returns, because the seek could only narrow on `status`. The plan reads more rows than ultimately match — costing extra CPU per row. It is distinct from the seek predicate that prunes the B-tree navigation.

**Alt1:** Adding both columns to the index (`status, amount`) lets `amount % 100 = 0` become a residual-only check instead of a post-scan filter — or with an expression index, a real seek.

## Q66: What does a Key Lookup indicate in a SQL Server plan?

**Query:**
```sql
SET SHOWPLAN_XML ON;
SELECT id, name, email, address FROM employees WHERE department_id = 3;
SET SHOWPLAN_XML OFF;
```
**Explanation:** Key Lookup follows the non-clustered index row to the clustered index to fetch columns not in the non-clustered index. The plan shows the Index Seek feeding a Key Lookup, which then joins into Nested Loops. Each lookup is a separate ordered seek, so wide extra columns make it the dominant cost — fix with covering columns.

**Alt1:** INCLUDE the extra columns: `CREATE INDEX ix_emp_dept ON dbo.employees(department_id) INCLUDE (name, email, address);` — the plan becomes a single covering Index Seek with no Key Lookup.

## Q67: What is a RID Lookup and when does it appear?

**Query:**
```sql
-- heap table (no clustered index), non-clustered index exists
SET SHOWPLAN_XML ON;
SELECT * FROM logs WHERE created_by = 101;
SET SHOWPLAN_XML OFF;
```
**Explanation:** RID Lookup is the heap-table equivalent of Key Lookup: the non-clustered index points to a Row Identifier (file:page:slot), and each fetched heap row costs an additional seek. Appears only on heaps. Converting the heap to a clustered index or covering the columns removes it.

**Alt1:** To spot RID lookups in the cheaper text plan, run `SET STATISTICS PROFILE ON;` — the `Index Seek` step will show a `RID Lookup` child with `Estimated Rows` equal to the number of matched seeds.

## Q68: How do you use execution plans with missing index suggestion?

**Query:**
```sql
SET SHOWPLAN_XML ON;
SELECT department_id, AVG(salary) FROM employees GROUP BY department_id;
SET SHOWPLAN_XML OFF;
```
**Explanation:** Missing-index hints appear in the XML as `<MissingIndexes>` with equality columns, inequality columns, and INCLUDE columns, plus an impact estimate. Treat them as suggestions, not gospel — test the suggested index with EXPLAIN before applying.

## Q69: This slow query shows a Hash Join with a Seq Scan on the hot table. What index fixes it?

**Query:**
```sql
EXPLAIN ANALYZE
SELECT c.name, SUM(o.amount)
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE o.order_date >= '2025-01-01'
GROUP BY c.name;
```
**Explanation:** The planner used a Seq Scan on orders because no index covers `(customer_id, order_date, amount)`. A composite index `(customer_id, order_date) INCLUDE amount` lets the join probe per customer and range-scan the date, converting the plan from one big Seq Scan to a Nested Loop of Index Scans.

## Q70: This is an N+1 query pattern hidden in a plan. How do you rewrite it?

**Query:**
```sql
EXPLAIN ANALYZE
SELECT u.name,
       (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) AS order_count
FROM users u;
```
**Explanation:** The subquery runs per user — with 10,000 users, `loops=10000` on the index lookup node. That is N+1 inside SQL. Rewrite as a plain `LEFT JOIN` with `GROUP BY` so the count is computed in one pass; the plan then shows a single HashAggregate instead of 10k executions.

**Alt1:** A lateral join shows the same per-row loops but makes the batching explicit: `SELECT u.name, x.cnt FROM users u LEFT JOIN LATERAL (SELECT COUNT(*) cnt FROM orders o WHERE o.user_id = u.id) x ON true;`

## Q71: How do you read an Oracle EXPLAIN PLAN output?

**Query:**
```sql
EXPLAIN PLAN FOR
SELECT d.department_name, COUNT(e.employee_id)
FROM departments d
LEFT JOIN employees e ON e.department_id = d.department_id
GROUP BY d.department_name;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```
**Explanation:** Oracle's plan is an indented operation tree: the most-indented line executes first (bottom-up). Each line shows Operation, Options, Object name, Cardinality (rows), Bytes, Cost, and Time. Rows are estimates derived from statistics — the same estimate/actual gap logic applies.

## Q72: What is the difference between INDEX FAST FULL SCAN and INDEX FULL SCAN (Oracle)?

**Query:**
```sql
EXPLAIN PLAN FOR
SELECT COUNT(*) FROM orders;
EXPLAIN PLAN FOR
SELECT order_id FROM orders ORDER BY order_id;
```
**Explanation:** INDEX FULL SCAN reads the index in sorted key order (used for ORDER BY — no sort needed). INDEX FAST FULL SCAN multiblocks-reads the index out of order (used for full coverage queries like COUNT) and cannot preserve order. The plan's `OPTIONS` column disambiguates the two.

## Q73: How does an aggregation pattern using a materialized view appear in a plan?

**Query:**
```sql
EXPLAIN PLAN FOR
SELECT country, COUNT(*)
FROM customers
GROUP BY country;
```
**Explanation:** The base table plan shows a `TABLE ACCESS FULL` with matching GROUP BY cost. If a materialized view exists with `QUERY REWRITE` enabled, the same query plans as `MAT_VIEW REWRITE ACCESS FULL` plus a `MAT_VIEW ACCESS` node — the planner reads the pre-aggregated summary instead of scanning the base table.

**Alt1:** PostgreSQL equivalent: a mat view scan appears as `Seq Scan on customers_mv` with no GROUP BY node, confirming the rewrite path.

## Q74: A plan ignores the first column benefit of a composite index. Why?

**Query:**
```sql
EXPLAIN SELECT * FROM transactions WHERE status = 'completed' AND account_id = 55;
```
**Explanation:** The composite index across `(account_id, status)` — by definition `account_id` must be the leading column to seek it. If status is seekable and account_id is not in the index, the planner can only use the index to filter status; MySQL EXPLAIN shows `possible_keys` with the composite but `key=NULL` when it cannot reach the account_id column.

## Q75: How does a covering index eliminate a Key Lookup in SQL Server?

**Query:**
```sql
SET SHOWPLAN_XML ON;
SELECT department_id, COUNT(*) FROM employees GROUP BY department_id;
SET SHOWPLAN_XML OFF;
```
**Explanation:** Before the covering index, the plan shows an Index Scan plus Key Lookup to fetch salary rows. After creating `(department_id) INCLUDE (salary)`, the plan reduces to an ordered Index Scan performing the COUNT and feeding the aggregation with no lookups. The XML operator list after the fix contains no Key Lookup.

## Q76: A monthly report is slow. Read this plan, what do you change?

**Query:**
```sql
EXPLAIN ANALYZE
SELECT c.name, SUM(oi.quantity * oi.unit_price) AS total
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN order_items oi ON o.id = oi.order_id
WHERE o.order_date >= '2025-01-01' AND o.order_date < '2025-02-01'
GROUP BY c.name;
```
**Explanation:** The plan shows a full scan on orders and order_items because there is no index serving `order_date`, then a Hash Join materializing the entire month. Fix: create `(order_date, id)` on orders and `(order_id) INCLUDE (quantity, unit_price)` on order_items, then re-run EXPLAIN — the Seq Scan on orders becomes an Index Range Scan and order_items is fetched per matched order.

**Alt1:** If the report runs often, pre-aggregate by `(customer_id, month)` into a summary table so the query never touches order_items at all.

## Q77: Pagination with OFFSET is slow. Read this plan and fix it.

**Query:**
```sql
EXPLAIN ANALYZE
SELECT id, title
FROM articles
WHERE status = 'published'
ORDER BY published_at DESC
LIMIT 20 OFFSET 100000;
```
**Explanation:** The plan shows the Limit node with the backend still scanning and sorting all 100,020 rows to discard 100,000 (`Rows Removed by Limit` in EXPLAIN ANALYZE). The deeper the offset, the more it reads. Fix with keyset pagination — filter on the last seen `published_at`/`id` instead of OFFSET — so the index scan stops early.

```text
Limit  (cost=0.56..89.12 rows=20 width=...) (actual time=245.678..245.789 rows=20 loops=1)
  ->  Index Scan Backward using idx_articles_published_at on articles  (cost=0.56..... rows=...)
        Index Cond: (status = 'published')
        Filter: (status = 'published')
        Rows Removed by Limit: 100000
```

## Q78: DELETE with a subplan is slow. What does the plan say?

**Query:**
```sql
EXPLAIN ANALYZE
DELETE FROM orders
WHERE customer_id IN (SELECT id FROM customers WHERE active = 0);
```
**Explanation:** The plan materializes the inactive customers (Hash Semi Join) then scans all of orders once, checking membership. With millions of inactive customers, the hash resizes and the scan must read every order row. Fix: add an index on `orders(customer_id)` and consider batch deletion with `LIMIT` within a procedure to avoid long-running locks.

**Alt1:** When deleting from huge tables, chunked delete in a loop with `Rows Affected` checks keeps the plan stable and the transaction short, and the index keeps each batch's membership probe cheap.

## Q79: How do you convert a correlated subquery to a LATERAL join and verify with EXPLAIN?

**Query:**
```sql
EXPLAIN ANALYZE
SELECT c.name, top_orders.amount
FROM customers c
LEFT JOIN LATERAL (
    SELECT amount FROM orders o WHERE o.customer_id = c.id
    ORDER BY o.amount DESC LIMIT 1
) top_orders ON true;
```
**Explanation:** The lateral join makes the per-row dependency explicit to the planner: it can run the subquery against the index `idx_orders_customer` once per customer — but still one execution per row. The plan keeps this an index-backed loop; the win is that the index now carries `(customer_id, amount DESC)` so the top-order lookup is indexed, not a re-scan.

## Q80: Why does rewriting a UNION to UNION ALL change the plan dramatically?

**Query:**
```sql
EXPLAIN ANALYZE
SELECT id FROM users WHERE role = 'admin'
UNION
SELECT id FROM audit_log WHERE action = 'delete';
```
**Explanation:** UNION forces deduplication, adding a Sort (or a HashAggregate) to compare and merge the two result sets. Switching to UNION ALL removes the dedup step — plans show two Index Scans feeding directly into `Append` with no Sort node. If the two branches cannot overlap, UNION ALL is always cheaper.

## Q81: How does partition pruning show up in a plan?

**Query:**
```sql
EXPLAIN (ANALYZE)
SELECT * FROM orders_parted WHERE order_date = '2025-06-15';
```
**Explanation:** With partition pruning, the plan references only the matching partition — `Partition Prune: [4, 4]` or `Partitions scanned: 1`. Without pruning, the plan lists multiple partitions or all of them, meaning the partition key was not used as a constant filter.

```text
Index Scan using orders_parted_pkey on orders_parted  (cost=0.44..... rows=...) (actual time=... rows=...)
  Index Cond: (order_date = '2025-06-15')
  Partitions scanned: 1
  Partition Prune: [4, 4]
```

## Q82: A window function introduces a costly Sort. How do you fix the plan?

**Query:**
```sql
EXPLAIN ANALYZE
SELECT customer_id,
       order_date,
       SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS running_total
FROM orders;
```
**Explanation:** The plan shows a `WindowAgg` node with a preceding `Sort` on `(customer_id, order_date)` because the window needs ordered input. If no index matches that order, PostgreSQL sorts the whole table. Adding `(customer_id, order_date) INCLUDE (amount)` makes the scan ordered, and the Sort node disappears.

```text
WindowAgg  (cost=... rows=...) (actual time=34.567..67.890 rows=100000 loops=1)
  Run Condition (running_total >= 0)
  ->  Sort  (cost=... rows=...) (actual time=30.001..45.678 rows=100000 loops=1)
        Sort Key: customer_id, order_date
```

## Q83: This self-join is slow. What does the plan indicate?

**Query:**
```sql
EXPLAIN ANALYZE
SELECT e1.name, e2.name AS manager
FROM employees e1
JOIN employees e2 ON e1.manager_id = e2.id;
```
**Explanation:** The plan shows a self-join executed with one side as a full scan or index scan because no index covers `employees(manager_id)`. Add `CREATE INDEX idx_emp_manager ON employees (manager_id);` so the lookup side of the self-join can seek instead of scan — the plan changes from Hash to Nested Loop index seeks.

## Q84: EXISTS vs IN — how do the plans differ?

**Query:**
```sql
EXPLAIN ANALYZE
SELECT c.id FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id AND o.status='shipped');

EXPLAIN ANALYZE
SELECT c.id FROM customers c
WHERE c.id IN (SELECT o.customer_id FROM orders o WHERE o.status = 'shipped');
```
**Explanation:** For equi-predicates both compile to the same semi-join in MySQL/Postgres (the planner treats them identically). The difference shows when NULLs exist: IN with NULLs has three-valued logic, and a NOT IN (`NOT IN (SELECT ...)`) plan can flatten to a full anti-join with different cardinality estimates. NOT EXISTS avoids the NULL trap entirely.

**Alt1:** In PostgreSQL the plan prints `Hash Semi Join` (EXISTS) vs `Hash Anti Join` (with NOT conditions); in SQL Server these show as `Nested Loops Left Semi Join` / `Left Anti Semi Join`.

## Q85: NOT EXISTS vs NOT IN — which plan is safer and why?

**Query:**
```sql
EXPLAIN ANALYZE
SELECT p.id FROM products p
WHERE NOT EXISTS (SELECT 1 FROM order_items oi WHERE oi.product_id = p.id);

EXPLAIN ANALYZE
SELECT p.id FROM products p
WHERE p.id NOT IN (SELECT oi.product_id FROM order_items oi WHERE oi.quantity = 0);
```
**Explanation:** Both produce an anti-join. But NOT IN with a NULL in the subquery result silently drops all rows because `x NOT IN (…, NULL, …)` is UNKNOWN, not TRUE. The plans look similar — the difference is correctness. Prefer NOT EXISTS (and use EXPLAIN to confirm a semi/anti join with no surprise filtering).

## Q86: When should a CTE materialize, and how does the plan tell you?

**Query:**
```sql
EXPLAIN ANALYZE
WITH total AS (SELECT SUM(amount) AS s FROM orders)
SELECT customer_id, amount / total.s AS share
FROM orders CROSS JOIN total;
```
**Explanation:** Materialization is beneficial when a CTE is referenced several times. The plan shows a `CTE Scan on orders` node with a single materialized evaluation, versus a `Subquery Scan` that re-runs the CTE body per reference. PostgreSQL marks NOT MATERIALIZED inline; the optimizer decides this per query.

**Alt1:** To force the one-pass behavior, use `WITH total AS MATERIALIZED (...)` — the plan then guarantees a single evaluation feeding all subsequent scans.

## Q87: Many OR conditions produced an Index Merge. Is that good?

**Query:**
```sql
EXPLAIN SELECT * FROM orders
WHERE status = 'shipped' OR priority = 'high';
```
**Explanation:** An Index Merge (`Extra: Using union(idx_status, idx_priority)`) is better than a full scan but still reads two indexes and deduplicates. Prefer a single composite index if one predicate dominates. Index merge scales poorly with more OR branches, so very long OR lists call for a UNION ALL rewrite.

```text
+----+-------------+--------+-------------+------------------+------------------+---------+------+------+-------------------------------------------------+
| id | select_type | table  | type        | possible_keys    | key              | key_len | ref  | rows | Extra                                           |
+----+-------------+--------+-------------+------------------+------------------+---------+------+------+-------------------------------------------------+
|  1 | SIMPLE      | orders | index_merge | idx_status,idx_priority | idx_status,idx_priority | 5,5 | NULL | 312 | Using union(idx_status,idx_priority); Using where |
+----+-------------+--------+-------------+------------------+------------------+---------+------+------+-------------------------------------------------+
```

## Q88: How does aggregate pushdown change an aggregation plan?

**Query:**
```sql
EXPLAIN ANALYZE
SELECT o.customer_id, COUNT(*)
FROM orders o
GROUP BY o.customer_id;
```
**Explanation:** On partitioned tables, PostgreSQL pushes partial aggregates per partition (`Partial Aggregate` per partition worker) before a `Finalize Aggregate`/Gather merges them — visible as `Partial`/`Finalize` node pairs. This reduces bytes moving up the tree and cuts memory for grouped queries at scale.

## Q89: How do you enable and verify Index Skip Scan in MySQL?

**Query:**
```sql
SET optimizer_switch = 'skip_scan=on';
EXPLAIN SELECT count(*) FROM employees
WHERE manager_id = 5
  AND department_id IN (4, 8, 12);
```
**Explanation:** When the composite index leading column is filtered with IN (not equality), MySQL 8.0+ can skip distinct leading values instead of scanning all. The plan shows `type=range` with `Using index for skip scan`. If the leading column has huge cardinality, skip scan is not chosen — the plan degrades to a full scan.

## Q90: What is a Loose Index Scan and when is it used?

**Query:**
```sql
EXPLAIN SELECT department_id, MIN(salary)
FROM employees
GROUP BY department_id;
```
**Explanation:** With a composite index `(department_id, salary)`, MySQL can jump from one department's first row straight to the next department — "loose" scanning skips groups in between. The plan shows `type=range` with `Using index for group-by`.

## Q91: What is Multi-Range Read (MRR) optimization?

**Query:**
```sql
EXPLAIN SELECT * FROM orders
WHERE customer_id IN (100, 200, 300) AND order_date > '2025-01-01';
```
**Explanation:** MRR buffers the row IDs from secondary index lookups and sorts them by heap order before fetching, avoiding random I/O. The plan shows `rows` with MRR under `Using MRR`. It helps most on HDD and large tables, and is controlled by `mrr=on`, `mrr_cost_based=on`.

**Alt1:** When MRR is cost-disabled, the same plan appears without `Using MRR`; forcing `SET optimizer_switch='mrr=on,mrr_cost_based=off';` reveals the row-ID ordering benefit in the EXPLAIN output.

## Q92: What is Block Nested Loop join in MySQL and what shows it in the plan?

**Query:**
```sql
EXPLAIN
SELECT a.id, b.val
FROM small_join_buffer a
JOIN big_table b ON a.key = b.key;
```
**Explanation:** When the join key has no index, MySQL buffers a block of outer rows into a `join_buffer` and matches the whole block against the inner table in one nested pass. It shows as `Using join buffer (Block Nested Loop)`. It is a fallback — add an index on the inner join column so MySQL can probe instead.

```text
+----+-------------+-------+------+---------------+------+---------+------+------+----------------------------------------------------+
| id | select_type | table | type | possible_keys | key  | key_len | ref  | rows | Extra                                              |
+----+-------------+-------+------+---------------+------+---------+------+------+----------------------------------------------------+
|  1 | SIMPLE      | b     | ALL  | NULL          | NULL | NULL    | NULL | 500K | Using where; Using join buffer (Block Nested Loop)   |
+----+-------------+-------+------+---------------+------+---------+------+------+----------------------------------------------------+
```

## Q93: What is an Adaptive Join in SQL Server and when does it appear?

**Query:**
```sql
SET SHOWPLAN_XML ON;
SELECT c.id, o.amount
FROM customers c
JOIN orders o ON c.id = o.customer_id;
SET SHOWPLAN_XML OFF;
```
**Explanation:** Adaptive joins (SQL Server 2017+, under CE 150) start one join type and switch at runtime when the actual row count makes the other cheaper. The XML operator is `Adaptive Join` with two alternative children (Hash vs Nested Loop). If the estimate was wrong, the "actual" branch it picked is visible in the plan after execution.

## Q94: A Hash Match shows a memory grant warning. What does it mean?

**Query:**
```sql
SET STATISTICS XML ON;
SELECT c.country, SUM(o.amount)
FROM orders o
JOIN customers c ON o.customer_id = c.id
GROUP BY c.country;
SET STATISTICS XML OFF;
```
**Explanation:** The plan's `<MemoryGrantWarning>` reports `Grant of X was refused because the grant exceeded the internal threshold` — the estimated spill (predicted for a much larger result) exceeded the query memory grant, forcing `TempDB` spills. Symptom: Hash Match spills and the plan is fast once with full memory, slow under concurrent load. Fix: fix the cardinality estimate or grant the query `min_grant_percent`/`max_grant_percent` hints.

**Alt1:** Lower memory pressure by reducing the work: add a covering index on the join keys so the hash builds off a narrow index scan instead of full rows.

## Q95: PostgreSQL work_mem is too small. How does EXPLAIN expose it?

**Query:**
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT customer_id, COUNT(*)
FROM orders
GROUP BY customer_id
ORDER BY customer_id;
```
**Explanation:** `Sort Method: external merge Disk:` (sort spilled) or `Batches: 4 Memory Usage: 512kB` (hash spilled) under the node name reports the spill. Rising them per-session (`SET work_mem = '256MB';`) and re-running shows the spill vanish from ANALYZE and the plan flatten to a pure memory sort.

**Alt1:** Too-large work_mem hurts the whole instance — tune it with `work_mem` per autovacuum/backend context, and check `pg_stat_activity` for memory pressure rather than guessing.

## Q96: A very wide table gets slow full scans. What index pattern helps?

**Query:**
```sql
EXPLAIN SELECT id, status, created_at
FROM giant_documents
WHERE workspace_id = 12 AND status <> 'archived'
ORDER BY created_at DESC;
```
**Explanation:** `status <> 'archived'` is a negative condition — a B-tree index cannot seek it. A partial index `ON giant_documents (workspace_id, created_at DESC) WHERE status <> 'archived'` keeps only the rows the query cares about. The plan then shows an Index Scan that navigates only the non-archived subset and returns matching rows ordered without a Sort.

## Q97: How do function-based indexes fix an Oracle predicate?

**Query:**
```sql
CREATE INDEX idx_customers_upper ON customers (UPPER(last_name));
EXPLAIN PLAN FOR
SELECT * FROM customers WHERE UPPER(last_name) = 'SMITH';
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```
**Explanation:** The predicate `UPPER(last_name) = 'SMITH'` would normally force a `TABLE ACCESS FULL`. The function-based index matches the exact expression, and the plan converts to `INDEX RANGE SCAN` on `IDX_CUSTOMERS_UPPER` plus a rowid fetch. The index expression must match the query expression character-for-character.

## Q98: The composite index column order changed the plan. Why does order matter?

**Query:**
```sql
EXPLAIN SELECT * FROM sales
WHERE region = 'EU' AND product_id = 90210;
```
**Explanation:** With index `(product_id, region)`, the planner seeks `product_id=90210` first then filters region. With `(region, product_id)`, it seeks region then product. The leading column must match the most selective or most-commonly-filtered predicate; reordering can turn an Index Only Scan into a scan with residual filtering. The plan's `Index Cond` shows which column did the seek.

```text
-- Before reorder: seek on product_id, region as filter
Index Scan using idx_sales_p_id_r on sales
  Index Cond: (product_id = 90210)
  Filter: (region = 'EU')

-- After reorder (region first):
Index Scan using idx_sales_r_p_id on sales
  Index Cond: ((region = 'EU') AND (product_id = 90210))
```

## Q99: Before/after EXPLAIN shows the power of a fix. Reproduce and explain the change.

**Query:**
```sql
-- BEFORE
EXPLAIN ANALYZE
SELECT o.id FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE c.country = 'IT' AND o.status = 'paid';
```
**Explanation:** Before, the plan has a full `Seq Scan on orders` feeding a Hash Join — every order page touched just to find paid rows. After adding `idx_orders(status, customer_id)` and running ANALYZE, the appended plan shows `Index Scan using idx_orders (status='paid')` and a Nested Loop to customers via its PK, with `Rows Removed` null. The same logical result, an order of magnitude less I/O.

```text
-- AFTER FIX
CREATE INDEX idx_orders_status_cust ON orders (status, customer_id);
ANALYZE orders;

Index Scan using idx_orders_status_cust on orders o  (cost=0.29..2245.67 rows=4100 width=8)
  Index Cond: (status = 'paid')
  ->  Nested Loop  (cost=0.56..2301.22 rows=4100 width=16)
        ->  Index Scan using customers_pkey on customers c  (cost=0.28..1.01 rows=1 width=8)
              Filter: (country = 'IT')
```

## Q100: A production query suddenly slowed. Walk through triage from the plan.

**Query:**
```sql
EXPLAIN (ANALYZE, BUFFERS, SETTINGS)
SELECT * FROM ledger
WHERE account_id = 44 AND entry_date >= '2025-01-01';
```
**Explanation:** Triage order: (1) read the plan — if `Index Scan` has `Index Cond` only on `entry_date` and a `Filter` on `account_id`, a selective seek is missing; `Rows Removed by Filter` quantifies waste. (2) check `actual time` vs `planning time`. (3) run `ANALYZE ledger;` — stale statistics after the recent import are the first suspect; re-EXPLAIN. (4) check the index actually exists and is being used; if not, created it with the correct column order `(account_id, entry_date)`. (5) measure with EXPLAIN ANALYZE until `Rows Removed by Filter` ~0 and Estimated Rows ≈ Actual Rows.
