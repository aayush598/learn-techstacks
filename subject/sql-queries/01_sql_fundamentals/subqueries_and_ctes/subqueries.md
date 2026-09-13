# Subqueries — 100 SQL Interview Q&A

## Q1: Write a query to find employees who earn more than the average salary.
**Query:**
```sql
SELECT employee_id, name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```
**Explanation:** A scalar subquery computes the company-wide average once and the outer query filters rows against that single value.

**Alt1:**
```sql
SELECT e.employee_id, e.name, e.salary
FROM employees e
CROSS JOIN (SELECT AVG(salary) AS avg_sal FROM employees) a
WHERE e.salary > a.avg_sal;
```
Offloads the average into a derived table; handy when the aggregate is needed again elsewhere in the query.

## Q2: Write a query to show each employee's salary alongside the company's average salary.
**Query:**
```sql
-- PostgreSQL / MySQL
SELECT employee_id, name, salary,
       (SELECT AVG(salary) FROM employees) AS company_avg_salary
FROM employees;
```
**Explanation:** A scalar subquery in the SELECT list is evaluated once and repeated for every output row, so the result is a constant column.

**Alt1:**
```sql
SELECT e.employee_id, e.name, e.salary, a.company_avg_salary
FROM employees e
CROSS JOIN (SELECT AVG(salary) AS company_avg_salary FROM employees) a;
```
The `CROSS JOIN` form makes the "one value for every row" intent explicit and avoids re-parsing the subquery per projection.

## Q3: Find products that cost more than the average price of products in the catalog.
**Query:**
```sql
SELECT product_id, product_name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);
```
**Explanation:** The inner query returns one number (the average price) and the outer filter uses it as a threshold. The subquery is evaluated before the outer scan.

## Q4: Show the total amount of every order and the overall average order amount in one result set.
**Query:**
```sql
SELECT order_id,
       SUM(quantity * unit_price) AS order_total,
       (SELECT AVG(quantity * unit_price) FROM order_items) AS avg_item_amount
FROM order_items
GROUP BY order_id;
```
**Explanation:** The grouped subquery in the SELECT list is independent of the grouping, so it returns the same average for every group. Scalar subqueries in a grouped query must not reference the outer grouping columns.

## Q5: Find the employee with the highest salary by comparing to a scalar value rather than using ORDER BY LIMIT.
**Query:**
```sql
SELECT employee_id, name, salary
FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees);
```
**Explanation:** The subquery returns the single highest salary and the equality filter returns all employees tied at the top — unlike `LIMIT 1`, no top earner is dropped.

**Alt1:**
```sql
SELECT employee_id, name, salary
FROM employees
WHERE salary >= ALL (SELECT salary FROM employees);
```
`= (SELECT MAX(...))` reads better and uses an index on salary; `>= ALL` generalizes when you compare against a computed list rather than a single max.

## Q6: Write a query that lists every department along with a count of its employees using a subquery instead of a JOIN.
**Query:**
```sql
SELECT d.department_id,
       d.name,
       (SELECT COUNT(*) FROM employees e WHERE e.department_id = d.department_id) AS employee_count
FROM departments d;
```
**Explanation:** The subquery in the SELECT list is correlated to the outer row, but you can also answer this with a derived table. See Alt1 for the version that stays inside this file's scope.

**Alt1:**
```sql
SELECT d.department_id, d.name, cnt.employee_count
FROM departments d
LEFT JOIN (SELECT department_id, COUNT(*) AS employee_count
           FROM employees GROUP BY department_id) cnt
  ON cnt.department_id = d.department_id;
```
The derived-table version evaluates the count once per department instead of once per department row, which is faster on large department tables.

## Q7: Find all customers who have placed at least one order using IN with a subquery.
**Query:**
```sql
SELECT customer_id, name
FROM customers
WHERE customer_id IN (SELECT DISTINCT customer_id FROM orders);
```
**Explanation:** The inner query returns the set of distinct customer ids with orders and `IN` keeps only matching outer rows.

**Alt1:**
```sql
SELECT customer_id, name
FROM customers
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = customers.customer_id);
```
`IN` shines when the subquery returns a small static set; `EXISTS` often wins on big tables because it stops after the first match and is evaluated row-by-row.

## Q8: Find all customers who have never placed an order, using NOT IN.
**Query:**
```sql
SELECT customer_id, name
FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders);
```
**Explanation:** Rows whose id is absent from the order set survive the filter. This works only if the subquery never returns NULL — see Q11 and Q53.

## Q9: Reproduce the previous query with NOT EXISTS and explain a key difference.
**Query:**
```sql
SELECT c.customer_id, c.name
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);
```
**Explanation:** This is the NULL-safe version of Q8 — `NOT EXISTS` ignores NULL ids in orders and never silently drops customers the way `NOT IN` can.

## Q10: Demonstrate the classic NULL pitfall: show why NOT IN silently returns an empty result.
**Query:**
```sql
-- PostgreSQL / SQL Server
SELECT name
FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders);
-- If orders.customer_id contains even one NULL, this returns ZERO rows.
```
**Explanation:** `x NOT IN (1, 2, NULL)` is `x <> 1 AND x <> 2 AND x <> NULL`, and `x <> NULL` is unknown, so every row's test is unknown and nothing matches.

**Alt1:**
```sql
SELECT name
FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL);
```
Fixing the subquery so it never emits NULL restores the intended result without switching to `NOT EXISTS`.

## Q11: Find employees whose salary is greater than that of AT LEAST ONE employee in department 3, using ANY.
**Query:**
```sql
SELECT employee_id, name, salary
FROM employees
WHERE salary > ANY (SELECT salary FROM employees WHERE department_id = 3);
```
**Explanation:** `> ANY` is true when the outer value beats the smallest value in the subquery result, so it behaves like "greater than the minimum of the list".

## Q12: Find employees whose salary is greater than the salary of EVERY employee in department 3, using ALL.
**Query:**
```sql
SELECT employee_id, name, salary
FROM employees
WHERE salary > ALL (SELECT salary FROM employees WHERE department_id = 3);
```
**Explanation:** `> ALL` requires beating every value, which is equivalent to "greater than the maximum of the list".

## Q13: Rewrite Q12 without ALL, using a scalar aggregate, and note the empty-list difference.
**Query:**
```sql
SELECT employee_id, name, salary
FROM employees
WHERE salary > (SELECT MAX(salary) FROM employees WHERE department_id = 3);
```
**Explanation:** Identical result, but if department 3 has no rows, `MAX` yields NULL and the filter matches nothing, whereas `> ALL (empty set)` evaluates TRUE for every row — a classic trap worth knowing.

## Q14: Prove SOME and ANY are interchangeable keywords.
**Query:**
```sql
-- MySQL / PostgreSQL
SELECT name
FROM employees
WHERE salary >= SOME (SELECT salary FROM employees WHERE department_id = 1);

SELECT name
FROM employees
WHERE salary >= ANY (SELECT salary FROM employees WHERE department_id = 1);
```
**Explanation:** `ANY` and `SOME` are synonyms in standard SQL and every major dialect; pick ANY for readability.

## Q15: Find products whose price equals the highest price in the table, using an IN instead of = with the aggregate.
**Query:**
```sql
SELECT product_id, product_name, price
FROM products
WHERE price IN (SELECT MAX(price) FROM products);
```
**Explanation:** Slightly unusual but valid — `IN` against a one-row subquery. You could equally write `= (SELECT MAX...)`; the IN form tolerates a subquery that occasionally returns a list.

## Q16: Show each product's price as a percentage of the maximum price.
**Query:**
```sql
SELECT product_id,
       product_name,
       price,
       ROUND(price * 100.0 / (SELECT MAX(price) FROM products), 2) AS pct_of_max
FROM products;
```
**Explanation:** The scalar subquery in the SELECT list is used arithmetically inside the projection, converting an absolute price into a relative measure.

## Q17: Find orders whose total value exceeds the average total value of all orders.
**Query:**
```sql
SELECT o.order_id,
       SUM(oi.quantity * oi.unit_price) AS order_total
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.order_id
HAVING SUM(oi.quantity * oi.unit_price) >
       (SELECT AVG(quantity * unit_price) FROM order_items);
```
**Explanation:** Aggregates of the outer query can only be filtered in HAVING, and a scalar subquery there gives the comparison threshold.

## Q18: Find employees who earn more than the average salary of employees in the highest-paying department, in one query.
**Query:**
```sql
SELECT employee_id, name, salary
FROM employees
WHERE salary > (SELECT AVG(salary)
                FROM employees
                WHERE department_id =
                      (SELECT department_id
                       FROM (SELECT department_id, AVG(salary) AS avg_sal
                             FROM employees GROUP BY department_id) dept_avg
                       ORDER BY avg_sal DESC
                       LIMIT 1));
```
**Explanation:** A two-step subquery of a subquery: innermost ranks departments by average salary, the middle SELECT rescans employees for that department's average, and the outer query filters on the single number.

## Q19: Find departments whose average salary is above the company average, using a derived table in FROM.
**Query:**
```sql
SELECT depart_avg.department_id, depart_avg.avg_salary
FROM (SELECT department_id, AVG(salary) AS avg_salary
      FROM employees
      GROUP BY department_id) AS depart_avg
WHERE depart_avg.avg_salary > (SELECT AVG(salary) FROM employees);
```
**Explanation:** The grouped subquery in FROM is a derived table that must be aliased; the outer WHERE then compares each group's average to a scalar subquery.

## Q20: List each employee with their salary and their department's average salary using a derived table.
**Query:**
```sql
SELECT e.name, e.salary, d.avg_salary
FROM employees e
JOIN (SELECT department_id, AVG(salary) AS avg_salary
      FROM employees GROUP BY department_id) AS d
  ON d.department_id = e.department_id;
```
**Explanation:** The derived table computes one average per department once, and the JOIN fans that value out to every employee — the standard non-correlated way to attach a group aggregate.

## Q21: Find all employees who work in a department listed in the departments table, using IN with a multi-row subquery.
**Query:**
```sql
SELECT employee_id, name
FROM employees
WHERE department_id IN (SELECT department_id FROM departments WHERE active = 1);
```
**Explanation:** The subquery returns many rows and `IN` expands to a membership test; the optimizer can build a hash set from the subquery result.

## Q22: Find products that have never appeared in any order using two different approaches.
**Query:**
```sql
-- Approach 1: NOT IN
SELECT product_id, product_name
FROM products
WHERE product_id NOT IN (SELECT product_id FROM order_items);

-- Approach 2: NOT EXISTS (NULL-safe)
SELECT p.product_id, p.product_name
FROM products p
WHERE NOT EXISTS (SELECT 1 FROM order_items oi WHERE oi.product_id = p.product_id);
```
**Explanation:** Both find products with no matching order line. Prefer `NOT EXISTS` because it is immune to the NULL trap and stops scanning after the first counterexample.

## Q23: Filter grouped results with a subquery in HAVING: keep departments whose employee count exceeds the count of department 10.
**Query:**
```sql
SELECT department_id, COUNT(*)
FROM employees
GROUP BY department_id
HAVING COUNT(*) > (SELECT COUNT(*) FROM employees WHERE department_id = 10);
```
**Explanation:** HAVING can reference a scalar subquery even though it is evaluated after grouping — handy for comparing each group against a precomputed baseline.

## Q24: Use a subquery inside ORDER BY to sort departments by their headcount without revealing the count.
**Query:**
```sql
-- PostgreSQL / SQL Server
SELECT department_id, name
FROM departments d
ORDER BY (SELECT COUNT(*) FROM employees e WHERE e.department_id = d.department_id) DESC;
```
**Explanation:** The subquery in ORDER BY computes each department's size "on the fly" for sorting. For large tables prefer a derived table (Alt1) so the count is computed once.

**Alt1:**
```sql
SELECT d.department_id, d.name
FROM departments d
JOIN (SELECT department_id, COUNT(*) AS cnt FROM employees GROUP BY department_id) e
  ON e.department_id = d.department_id
ORDER BY e.cnt DESC;
```
Correlated ORDER BY subqueries re-execute per row; a precomputed derived table avoids the repeated work.

## Q25: Compute a column with a scalar subquery in SELECT and then use that value in the WHERE clause in a separate query.
**Query:**
```sql
-- PostgreSQL / MySQL
SELECT name, salary - (SELECT AVG(salary) FROM employees) AS diff_from_avg
FROM employees;
```
**Explanation:** You cannot reference a SELECT alias inside the same WHERE clause. The fix is to wrap the projection in a derived table so the computed value becomes a filterable column.

**Alt1:**
```sql
SELECT * FROM (
  SELECT name, salary - (SELECT AVG(salary) FROM employees) AS diff_from_avg
  FROM employees
) AS with_diff
WHERE diff_from_avg > 0;
```
The outer query of the derived table can filter on the alias — this is the canonical "compute then use" reshuffling.

## Q26: Find the second highest salary in the employees table using a subquery of a subquery.
**Query:**
```sql
SELECT MAX(salary)
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```
**Explanation:** The inner subquery finds the top salary and the outer MAX picks the highest value strictly below it. Nesting lets you build answers as a chain of thin subqueries.

**Alt1:**
```sql
SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 1;
```
`LIMIT/OFFSET` is terser but tie-prone without DISTINCT; the nested-MAX form is portable and returns the true second-highest distinct value.

## Q27: Find all employees who earn the second highest salary, without LIMIT/OFFSET.
**Query:**
```sql
SELECT employee_id, name, salary
FROM employees
WHERE salary = (SELECT MAX(salary)
                FROM employees
                WHERE salary < (SELECT MAX(salary) FROM employees));
```
**Explanation:** The innermost query gets the top salary, the middle one gets the max below that, and the WHERE picks every employee tied at that level — no row is dropped.

## Q28: Find the department name and the average salary of the highest-paying department, using a nested subquery.
**Query:**
```sql
-- MySQL / PostgreSQL
SELECT d.name, top.avg_salary
FROM departments d
JOIN (SELECT department_id, AVG(salary) AS avg_salary
      FROM employees
      GROUP BY department_id
      HAVING AVG(salary) = (SELECT MAX(avg_sal)
                            FROM (SELECT department_id, AVG(salary) AS avg_sal
                                  FROM employees GROUP BY department_id) dept_avgs)) top
  ON top.department_id = d.department_id;
```
**Explanation:** A derived table in FROM feeds an aggregate into a scalar subquery, forming a subquery-of-a-subquery-of-a-derived-table pipeline.

## Q29: Count how many employees in each department earn more than the company average, using a derived table.
**Query:**
```sql
SELECT dept_summary.department_id, dept_summary.above_avg_count
FROM (SELECT e.department_id, COUNT(*) AS above_avg_count
      FROM employees e
      WHERE e.salary > (SELECT AVG(salary) FROM employees)
      GROUP BY e.department_id) AS dept_summary;
```
**Explanation:** The scalar average is computed once for every row, but that is still one aggregate per row; for performance, hoist the average into a derived table (Alt1).

**Alt1:**
```sql
SELECT e.department_id, COUNT(*)
FROM employees e
CROSS JOIN (SELECT AVG(salary) AS avg_sal FROM employees) a
WHERE e.salary > a.avg_sal
GROUP BY e.department_id;
```
Computing the average once in the derived table avoids re-running the aggregation for each employee row.

## Q30: Return employees hired before the average hire date of employees in any single department older than... using nested subqueries.
**Query:**
```sql
SELECT employee_id, name, hire_date
FROM employees
WHERE hire_date < (SELECT MIN(hire_date)
                   FROM (SELECT hire_date FROM employees
                         WHERE department_id = (SELECT department_id FROM departments ORDER BY founded_on LIMIT 1)) oldest_hires);
```
**Explanation:** Three levels of nesting feed one boundary value outward: an inner scalar picks a department, the middle finds that department's earliest hire date, and the outer WHERE compares hire dates against it.

## Q31: List each department with a salary-column note: how many employees are above vs below the company average, using a JOIN of two derived tables.
**Query:**
```sql
SELECT COALESCE(above.department_id, below.department_id) AS department_id,
       COALESCE(above.cnt, 0) AS above_avg,
       COALESCE(below.cnt, 0) AS below_avg
FROM (SELECT department_id, COUNT(*) AS cnt
      FROM employees
      WHERE salary > (SELECT AVG(salary) FROM employees)
      GROUP BY department_id) above
FULL OUTER JOIN (SELECT department_id, COUNT(*) AS cnt
                 FROM employees
                 WHERE salary <= (SELECT AVG(salary) FROM employees)
                 GROUP BY department_id) below
  ON above.department_id = below.department_id;
```
**Explanation:** Two derived tables are combined to produce opposing counts side by side; `FULL OUTER JOIN` keeps departments that appear in only one bucket. (PostgreSQL)

## Q32: Write a query that filters groups using a subquery in HAVING to keep departments with above-average headcount.
**Query:**
```sql
SELECT department_id, COUNT(*) AS headcount
FROM employees
GROUP BY department_id
HAVING COUNT(*) > (SELECT AVG(cnt)
                   FROM (SELECT department_id, COUNT(*) AS cnt
                         FROM employees GROUP BY department_id) dept_counts);
```
**Explanation:** The inner derived table computes every department's size, the scalar subquery averages those sizes, and HAVING keeps only departments bigger than that average.

## Q33: Sort employees by how far their salary is from the company average, using a subquery in ORDER BY.
**Query:**
```sql
SELECT employee_id, name, salary
FROM employees
ORDER BY ABS(salary - (SELECT AVG(salary) FROM employees)) DESC;
```
**Explanation:** ORDER BY accepts a scalar subquery as any other expression, so the distance from average becomes the sort key.

## Q34: Find each product's price rank (1 = lowest) without window functions, using a subquery counting cheaper products.
**Query:**
```sql
SELECT p.product_id, p.product_name, p.price,
       (SELECT COUNT(*) FROM products p2
        WHERE p2.price < p.price) + 1 AS price_rank
FROM products p;
```
**Explanation:** This is a correlated subquery counting rivals. For a purely non-correlated phrasing, use the derived-table self-join in Alt1.

**Alt1:**
```sql
SELECT a.product_id, a.product_name, a.price, COUNT(b.product_id) + 1 AS price_rank
FROM products a
LEFT JOIN products b ON b.price < a.price
GROUP BY a.product_id, a.product_name, a.price;
```
A self-join of the same table to itself counts strictly cheaper products — fully non-correlated and index-friendly when b.price is indexed.

## Q35: Get the top 2 earning employees per department without window functions, using a derived table and a self-join.
**Query:**
```sql
SELECT e.department_id, e.name, e.salary
FROM employees e
LEFT JOIN employees e2
  ON e2.department_id = e.department_id AND e2.salary > e.salary
GROUP BY e.department_id, e.name, e.salary
HAVING COUNT(e2.employee_id) < 2
ORDER BY e.department_id, e.salary DESC;
```
**Explanation:** Each employee is compared against colleagues earning more, and those with fewer than two superiors survive — a classic "top N per group without window functions" pattern built from a self-join derived relationship.

## Q36: Find customers who have placed orders using EXISTS.
**Query:**
```sql
SELECT c.customer_id, c.name
FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);
```
**Explanation:** EXISTS does not care which columns or how many rows the subquery returns; it only reports whether at least one row exists. The optimizer typically short-circuits on the first match and can use an index on orders.customer_id.

## Q37: Find customers who have placed no orders in the last 90 days, using NOT EXISTS.
**Query:**
```sql
SELECT c.customer_id, c.name
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o
                  WHERE o.customer_id = c.customer_id
                    AND o.order_date >= CURRENT_DATE - INTERVAL '90 days');
```
**Explanation:** NOT EXISTS is NULL-safe and composable: extra predicates just get ANDed into the probe, so no ordering of conditions changes the answer.

## Q38: Find employees assigned to at least one project AND booked in at least one timesheet, using two EXISTS clauses.
**Query:**
```sql
SELECT e.employee_id, e.name
FROM employees e
WHERE EXISTS (SELECT 1 FROM project_assignments pa WHERE pa.employee_id = e.employee_id)
  AND EXISTS (SELECT 1 FROM timesheets t WHERE t.employee_id = e.employee_id);
```
**Explanation:** Multiple EXISTS tests combine like any boolean conditions, and each one can be satisfied by an index scan on the foreign key.

## Q39: Explain why SELECT 1 vs SELECT * inside EXISTS makes no difference, and show it.
**Query:**
```sql
-- All three are equivalent in efficiency and result:
SELECT c.customer_id FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);

SELECT c.customer_id FROM customers c
WHERE EXISTS (SELECT o.order_id FROM orders o WHERE o.customer_id = c.customer_id);

SELECT c.customer_id FROM customers c
WHERE EXISTS (SELECT o.* FROM orders o WHERE o.customer_id = c.customer_id);
```
**Explanation:** EXISTS only tests row existence; the select list is ignored entirely, so the canonical form is `SELECT 1`.

## Q40: Write a query where a cheap filter runs BEFORE an EXISTS test to shrink the scan. Show both orders.
**Query:**
```sql
-- Selective predicate first: skips expensive existence check for most rows
SELECT c.customer_id, c.name
FROM customers c
WHERE c.status = 'active'
  AND EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);

-- Analytical equivalence, but the bad shaping:
SELECT c.customer_id, c.name
FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
  AND c.status = 'active';
```
**Explanation:** Both return the same rows, but drilling the cheap, indexable `status` filter first lets the engine explore fewer candidate rows before running the subquery — the classic EXISTS-vs-IN performance shaping.

## Q41: Contrast IN and EXISTS performance shape for a small static list versus a huge subquery.
**Query:**
```sql
-- Small static-ish list: IN flattens to a fast membership probe
SELECT * FROM employees
WHERE department_id IN (SELECT department_id FROM department_codes);   -- few hundred rows

-- Huge generated set: EXISTS finds the first match and stops per row
SELECT e.* FROM employees e
WHERE EXISTS (SELECT 1 FROM all_activity a WHERE a.employee_id = e.employee_id);
```
**Explanation:** With a small subquery an IN hash-set lookup is cheap and readable; with a large subquery, EXISTS's early termination and index-driven probing usually dominate. Modern optimizers sometimes rewrite them to the same plan, but the shapes are the intuition interviewers want.

## Q42: Join two derived tables: show departments with above-average headcount and above-average salary together.
**Query:**
```sql
SELECT dc.department_id, dc.cnt AS headcount, sc.avg_salary
FROM (SELECT department_id, COUNT(*) AS cnt
      FROM employees GROUP BY department_id
      HAVING COUNT(*) > (SELECT AVG(cnt2)
                         FROM (SELECT COUNT(*) AS cnt2 FROM employees GROUP BY department_id) all_cnts)) dc
JOIN (SELECT department_id, AVG(salary) AS avg_salary
      FROM employees GROUP BY department_id
      HAVING AVG(salary) > (SELECT AVG(salary) FROM employees)) sc
  ON dc.department_id = sc.department_id;
```
**Explanation:** Each derived table independently applies a subquery threshold, and the final JOIN intersects the departments that pass both tests.

## Q43: Show the ERROR when a derived table has no alias, then the fixed version.
**Query:**
```sql
-- PostgreSQL: ERROR: subquery in FROM must have an alias
SELECT * FROM (SELECT department_id, COUNT(*) FROM employees GROUP BY department_id);

-- Fixed: alias required
SELECT dept_stats.department_id, dept_stats.count
FROM (SELECT department_id, COUNT(*) FROM employees GROUP BY department_id) AS dept_stats;
```
**Explanation:** Every derived table in the FROM clause must carry an alias so its columns can be qualified; the fix is appending `AS` plus a name.

## Q44: Show each department's headcount as a percentage of the total headcount using a scalar subquery in SELECT.
**Query:**
```sql
SELECT dept_id, cnt,
       ROUND(100.0 * cnt / (SELECT COUNT(*) FROM employees), 2) AS pct_of_total
FROM (SELECT department_id AS dept_id, COUNT(*) AS cnt
      FROM employees GROUP BY department_id) dept_counts;
```
**Explanation:** The inner derived table supplies per-department counts and a second scalar subquery supplies the grand total, combined arithmetically in the outer projection.

## Q45: Count how many products have been ordered more times than the average product, using a grouped subquery feeding IN.
**Query:**
```sql
SELECT COUNT(*)
FROM (SELECT product_id
      FROM order_items
      GROUP BY product_id
      HAVING COUNT(*) > (SELECT AVG(oc.cnt)
                         FROM (SELECT product_id, COUNT(*) AS cnt
                               FROM order_items GROUP BY product_id) oc)) popular;
```
**Explanation:** The innermost derived table computes per-product order counts, the scalar subquery averages them, HAVING keeps popular products, and the outer COUNT totals the survivors.

## Q46: Find products whose price is above their category's average price, using a non-correlated derived table.
**Query:**
```sql
SELECT p.product_id, p.product_name, p.price, cat_avg.category_avg
FROM products p
JOIN (SELECT category_id, AVG(price) AS category_avg
      FROM products GROUP BY category_id) cat_avg
  ON cat_avg.category_id = p.category_id
WHERE p.price > cat_avg.category_avg;
```
**Explanation:** Grouping the whole table by category computes each average once, then the JOIN rescans products against its own category — no per-row correlated execution.

**Alt1:**
```sql
SELECT p.product_id, p.product_name, p.price
FROM products p
WHERE p.price > (SELECT AVG(p2.price)
                 FROM products p2
                 WHERE p2.category_id = p.category_id);
```
The correlated scalar version is shorter but re-runs the inner aggregate for every product row; the derived-table JOIN is usually the better plan on wide tables.

## Q47: Flag each product as "above" or "below" the max price its category ever had, with a CASE on a scalar subquery.
**Query:**
```sql
SELECT p.product_id, p.product_name,
       CASE WHEN p.price > priced.category_max THEN 'ABOVE'
            ELSE 'AT_OR_BELOW' END AS vs_category_max
FROM products p
JOIN (SELECT category_id, MAX(price) AS category_max
      FROM products GROUP BY category_id) priced
  ON priced.category_id = p.category_id;
```
**Explanation:** The derived table precomputes each category's ceiling and the CASE labels every product; a correlated subquery would repeat the MAX per row instead.

## Q48: Use a row value in a WHERE clause comparing against a single subquery row (PostgreSQL).
**Query:**
```sql
-- PostgreSQL
SELECT employee_id, name, department_id, salary
FROM employees
WHERE (department_id, salary) =
      (SELECT department_id, MAX(salary)
       FROM employees
       WHERE department_id IN (SELECT department_id FROM departments WHERE region = 'EU')
       GROUP BY department_id
       ORDER BY MAX(salary) DESC
       LIMIT 1);
```
**Explanation:** The row constructor `(department_id, salary)` is compared as a tuple against the one row the subquery returns, so both columns must match together — a paired comparison the optimizer can satisfy without disassembling.

## Q49: Find duplicate product names using a derived table with GROUP BY and HAVING.
**Query:**
```sql
SELECT dups.product_name, dups.occurrences
FROM (SELECT product_name, COUNT(*) AS occurrences
      FROM products
      GROUP BY product_name
      HAVING COUNT(*) > 1) dups
ORDER BY dups.occurrences DESC;
```
**Explanation:** The inner derived table collapses products by name and keeps only repeated ones; the outer query simply presents them.

**Alt1:**
```sql
SELECT p1.product_name, COUNT(*) AS occurrences
FROM products p1
JOIN products p2 ON p2.product_name = p1.product_name AND p2.product_id >= p1.product_id
GROUP BY p1.product_name
HAVING COUNT(DISTINCT p1.product_id) > 1;
```
Self-join pairing counts pairs instead of rows; the derived-table GROUP BY version is the more natural "pick and count the duplicates".

## Q50: Use a scalar subquery in the SELECT list to generate a per-row note that is then filtered by an enclosing derived table.
**Query:**
```sql
-- MySQL / PostgreSQL
SELECT employee_id, name, salary FROM (
  SELECT employee_id, name, salary,
         salary - (SELECT AVG(salary) FROM employees) AS gap
  FROM employees
) AS salaried
WHERE gap > (SELECT 5000);
```
**Explanation:** The inner SELECT computes `gap` from a scalar subquery, and the outer WHERE turns the derived column into a filter — one pattern for "make a subquery result usable twice".

**Alt1:**
```sql
SELECT employee_id, name, salary
FROM employees
WHERE salary - (SELECT AVG(salary) FROM employees) > 5000;
```
Inlining the subquery avoids the wrapper, at the cost of repeating the expression if it is ever needed elsewhere.

## Q51: Show the error when a scalar subquery returns multiple rows, then fix it.
**Query:**
```sql
-- ERROR (all dialects): more than one row returned by a subquery used as an expression
SELECT name FROM employees
WHERE salary = (SELECT salary FROM employees WHERE department_id = 5);
-- department 5 has many salaries -> runtime error

-- Fix: make the subquery return exactly one value
SELECT name FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees WHERE department_id = 5);
```
**Explanation:** A scalar subquery (in SELECT, WHERE `=`, or expressions) is a single value; feeding it a multi-row set raises a runtime error, so constrain it with an aggregate or LIMIT 1.

## Q52: Handle a scalar subquery that can legitimately return NULL by falling back with COALESCE.
**Query:**
```sql
SELECT product_id, product_name,
       COALESCE((SELECT MAX(price) FROM products WHERE category_id = 0), 0) AS ghost_max
FROM products;
```
**Explanation:** If the subquery matches no rows, aggregate MAX yields NULL and COALESCE swaps in 0 so the projection stays numerically safe.

## Q53: Give the full treatment of the NOT IN NULL trap: write the failing query, the truth-table, and the fix.
**Query:**
```sql
-- 1) The trap: this silently returns NOTHING when a NULL id exists in orders
SELECT customer_id FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders);

-- 2) The truth table that explains it:
--    x NOT IN (1, 2, NULL)  ==  x<>1 AND x<>2 AND x<>NULL ==  UNKNOWN for every x

-- 3) The NULL-safe fix with NOT EXISTS
SELECT c.customer_id
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);
```
**Explanation:** A single NULL inside the IN list poisons every comparison to UNKNOWN, so NOT IN returns zero rows. NOT EXISTS treats NULL ids as plain non-matches and keeps the intended rows.

**Alt1:**
```sql
SELECT customer_id FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL);
```
Adding `WHERE customer_id IS NOT NULL` to the subquery also tames NOT IN, but purists prefer NOT EXISTS for self-documenting intent.

## Q54: Write a retail report: customers whose lifetime spend is below the overall average lifetime spend, computed via a derived table of aggregates.
**Query:**
```sql
SELECT c.customer_id, c.name, life.lifetime_spend
FROM customers c
JOIN (SELECT customer_id, SUM(quantity * unit_price) AS lifetime_spend
      FROM order_items JOIN orders USING (order_id)
      GROUP BY customer_id) life
  ON life.customer_id = c.customer_id
WHERE life.lifetime_spend < (SELECT AVG(quantity * unit_price)
                             FROM order_items JOIN orders USING (order_id));
```
**Explanation:** The derived table precomputes each customer's spend, and the scalar subquery computes the benchmark once in WHERE. (MySQL / PostgreSQL)

## Q55: Demonstrate ANY over an empty result set, and show the practical danger.
**Query:**
```sql
SELECT employee_id, name
FROM employees
WHERE salary > ANY (SELECT salary FROM employees WHERE department_id = 99);
-- department 99 does not exist -> subquery returns 0 rows
-- In PostgreSQL/SQL Server: > ANY behaves as "greater than no value" => ALL rows returned
```
**Explanation:** `> ANY (empty)` evaluates TRUE for every row because there is no value to beat — a silent no-filter. Wrap the subquery in EXISTS-aware logic or guard the list when empty is not intended.

## Q56: Show that ALL over an empty set also returns TRUE, and how to guard it.
**Query:**
```sql
-- Returns EVERY employee: > ALL (empty) is TRUE
SELECT name FROM employees
WHERE salary > ALL (SELECT salary FROM employees WHERE department_id = 99);

-- Guard: require the benchmark to exist
SELECT name FROM employees
WHERE salary > ALL (SELECT salary FROM employees WHERE department_id = 99)
  AND EXISTS (SELECT 1 FROM employees WHERE department_id = 99);
```
**Explanation:** `ALL` with zero rows is vacuously true; pairing it with an EXISTS guard restores "only when the set is real".

## Q57: Write four equivalent ways to find the maximum salary, cycling scalar-aggregate and ALL forms.
**Query:**
```sql
SELECT name FROM employees WHERE salary = (SELECT MAX(salary) FROM employees);
SELECT name FROM employees WHERE salary >= ALL (SELECT salary FROM employees);
SELECT name FROM employees WHERE salary >= (SELECT MAX(salary) FROM employees);
SELECT name FROM employees WHERE salary NOT < (SELECT MAX(salary) FROM employees);
```
**Explanation:** `MAX`, `>= ALL`, `>= scalar-MAX`, and logically negated literals all select the top salary; the MAX form reads best and uses indexes most predictably.

## Q58: Find employees whose salary is below at least one other salary (i.e., not top-paid) using ANY, and its MIN form.
**Query:**
```sql
SELECT name FROM employees WHERE salary < ANY (SELECT salary FROM employees);
-- equivalent to:
SELECT name FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);
```
**Explanation:** `< ANY` means "less than some value", which for a salary scale is the same as "below the max"; the aggregate version documents intent better.

## Q59: Re-express "not equal to any value in a set" using <> ALL and compare with NOT IN semantics.
**Query:**
```sql
SELECT product_id FROM products
WHERE product_id <> ALL (SELECT product_id FROM discontinued_products);
-- same as NOT IN, BUT both share the NULL poison:
--   <> ALL (…) fails silently if the subquery yields a NULL.
```
**Explanation:** `<> ALL` is the SYMMETRIC synonym of NOT IN, so it inherits the NULL trap; use `NOT EXISTS` when NULLs are possible.

## Q60: Re-express IN with = ANY and note when the ANY spelling is useful.
**Query:**
```sql
SELECT employee_id FROM employees
WHERE department_id IN (SELECT department_id FROM departments WHERE active = 1);
-- equivalent:
SELECT employee_id FROM employees
WHERE department_id = ANY (SELECT department_id FROM departments WHERE active = 1);
```
**Explanation:** `= ANY` is the canonical expansion of IN; it is handy when you want to mix operators, e.g. `>= ANY (...)` to combine equality and inequality in one comparison.

## Q61: Use a row constructor with IN to test a multi-column membership (PostgreSQL).
**Query:**
```sql
-- PostgreSQL
SELECT employee_id, name, department_id, salary
FROM employees
WHERE (department_id, salary) IN (
      SELECT department_id, MAX(salary)
      FROM employees
      GROUP BY department_id);
```
**Explanation:** The row `(department_id, salary)` matches only rows whose department AND salary both appear together in the grouped subquery — a multi-column `IN` that returns the top earner(s) per department.

**Alt1:**
```sql
SELECT e.employee_id, e.name, e.department_id, e.salary
FROM employees e
JOIN (SELECT department_id, MAX(salary) AS max_sal
      FROM employees GROUP BY department_id) top
  ON top.department_id = e.department_id AND top.max_sal = e.salary;
```
The JOIN drops the row-constructor syntax and works on every dialect; the tuple-IN version is shorter where dialects support it.

## Q62: Filter on a whole row at once: pick orders that exactly match a "reference order" row returned by a subquery.
**Query:**
```sql
-- PostgreSQL
SELECT order_id, customer_id, order_total
FROM orders
WHERE (customer_id, order_total) =
      (SELECT customer_id, order_total
       FROM orders
       WHERE order_id = 999);
```
**Explanation:** The subquery returns ONE row with two columns and the outer WHERE compares it as a tuple — both columns must line up, so it finds orders identical to order 999 on those fields.

## Q63: Pull two summary columns from a single-row subquery in FROM and use them with a percentage.
**Query:**
```sql
SELECT p.product_id, p.price,
       ROUND(p.price * 100.0 / m.max_price, 2) AS pct_of_max
FROM products p
CROSS JOIN (SELECT MAX(price) AS max_price FROM products) m;
```
**Explanation:** The derived table returns a single row of scalars; CROSS JOIN vends `max_price` to every product row for the ratio.

## Q64: Return a multi-column subquery result in the SELECT list via a single-row derived table (SQL Server-friendly pattern).
**Query:**
```sql
-- SQL Server / PostgreSQL
SELECT e.employee_id, e.name, x.avg_sal, x.max_sal
FROM employees e
CROSS JOIN (SELECT AVG(salary) AS avg_sal, MAX(salary) AS max_sal FROM employees) x;
```
**Explanation:** A subquery in the SELECT list can return only one scalar, but a derived table in FROM may expose many columns — this is how you fan a two-number summary out to the full table.

## Q65: Find employees in the two departments with the highest average salary, using a nested subquery chain.
**Query:**
```sql
-- MySQL / PostgreSQL
SELECT employee_id, name, salary, department_id
FROM employees
WHERE department_id IN (
      SELECT department_id
      FROM (SELECT department_id
            FROM (SELECT department_id, AVG(salary) AS avg_sal
                  FROM employees GROUP BY department_id) ranked
            ORDER BY avg_sal DESC
            LIMIT 2) top2);
```
**Explanation:** The inner derived table computes averages, the middle ORDER/LIMIT keeps the top two departments, and the outer membership test selects all their employees.

**Alt1:**
```sql
SELECT e.employee_id, e.name, e.salary, e.department_id
FROM employees e
JOIN (
  SELECT department_id FROM (
    SELECT department_id, ROW_NUMBER() OVER (ORDER BY AVG(salary) DESC) AS rn
    FROM employees GROUP BY department_id
  ) ranked WHERE rn <= 2
) top2 ON top2.department_id = e.department_id;
```
The ORDER/LIMIT variant is cleaner for "top N" when ties don't matter; the windowed version still stays a single derived-table chain.

## Q66: Find managers who manage more employees than the average manager does, aggregating via a derived table.
**Query:**
```sql
SELECT mgr.manager_id, cnt.managed_count
FROM (SELECT manager_id, COUNT(*) AS managed_count
      FROM employees WHERE manager_id IS NOT NULL
      GROUP BY manager_id) cnt
JOIN employees mgr ON mgr.employee_id = cnt.manager_id
WHERE cnt.managed_count > (SELECT AVG(mc)
                           FROM (SELECT COUNT(*) AS mc
                                 FROM employees WHERE manager_id IS NOT NULL
                                 GROUP BY manager_id) all_managers);
```
**Explanation:** Two derived tables count reports per manager and total them; the scalar subquery averages team sizes and WHERE keeps above-average managers.

## Q67: Add a "distance from the top salary" column for every employee using a scalar subquery in SELECT.
**Query:**
```sql
SELECT employee_id, name,
       (SELECT MAX(salary) FROM employees) - salary AS distance_from_top
FROM employees
ORDER BY distance_from_top;
```
**Explanation:** The scalar subquery feeds an arithmetic expression and the result alias is reusable in ORDER BY (though not in the same-level WHERE).

## Q68: Compare each quarter's revenue against the previous quarter using two derived tables joined on a rank.
**Query:**
```sql
-- PostgreSQL / SQL Server
SELECT cur.qtr, cur.revenue, prev.revenue AS prev_revenue,
       cur.revenue - prev.revenue AS delta
FROM (SELECT EXTRACT(QUARTER FROM order_date) AS qtr,
             SUM(total) AS revenue
      FROM orders GROUP BY EXTRACT(QUARTER FROM order_date)) cur
JOIN (SELECT EXTRACT(QUARTER FROM order_date) AS qtr,
             SUM(total) AS revenue
      FROM orders GROUP BY EXTRACT(QUARTER FROM order_date)) prev
  ON prev.qtr = cur.qtr - 1;
```
**Explanation:** Both derived tables are independent aggregations over the same table; joining them on a quarter offset produces the quarter-over-quarter delta without window functions.

## Q69: Deduplicate a sales feed in a derived table BEFORE aggregating, so double-counted rows don't skew totals.
**Query:**
```sql
SELECT feed.product_id, COUNT(*) AS distinct_buyers
FROM (SELECT DISTINCT order_id, product_id, customer_id FROM sales_feed) feed
JOIN customers c ON c.customer_id = feed.customer_id
GROUP BY feed.product_id;
```
**Explanation:** The inner derived table collapses duplicate feed rows first; the outer aggregation counts only distinct buyer/product pairs, preventing inflated totals.

## Q70: Answer the same question two ways — subquery vs JOIN — and discuss when to pick each. (Which products were ordered?)
**Query:**
```sql
-- Subquery flavor
SELECT p.product_id, p.product_name
FROM products p
WHERE p.product_id IN (SELECT DISTINCT oi.product_id FROM order_items oi);

-- JOIN flavor
SELECT DISTINCT p.product_id, p.product_name
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id;
```
**Explanation:** Semantically identical. IN is compact and requires no dedupe thought; the JOIN reveals every matched row so DISTINCT is needed. Pick IN for "does it exist", JOIN when you also need joined columns or already have unique keys.

## Q71: Use a subquery in WHERE to isolate rows at the low end of a distribution: products cheaper than the 5th cheapest? Nope — cheaper than the average of the cheapest product per category.
**Query:**
```sql
SELECT p.product_id, p.product_name, p.price
FROM products p
JOIN (SELECT category_id, MIN(price) AS cheapest
      FROM products GROUP BY category_id) cheap
  ON cheap.category_id = p.category_id
WHERE p.price > (SELECT AVG(cheapest) FROM (
      SELECT MIN(price) AS cheapest FROM products GROUP BY category_id) t)
  AND p.price = cheap.cheapest;
```
**Explanation:** The innermost derived table computes a min per category, the scalar subquery averages those minimums, and the JOIN resolves prices to their category floor — producing a comparably-filtered set.

## Q72: Sort products by their margin rank (price rank minus cost rank) using subqueries in ORDER BY.
**Query:**
```sql
SELECT p.product_id, p.product_name, p.price, p.cost
FROM products p
ORDER BY (SELECT COUNT(*) FROM products p2 WHERE p2.price < p.price)
       - (SELECT COUNT(*) FROM products p2 WHERE p2.cost < p.cost) DESC;
```
**Explanation:** ORDER BY accepts two scalar subqueries per row and sorts on their difference; understandably slow on big tables, which is the point of the Alt1 alternative.

**Alt1:**
```sql
SELECT p.product_id, p.product_name, p.price, p.cost,
       (SELECT COUNT(*) FROM products p2 WHERE p2.price < p.price) AS price_rank
FROM products p
ORDER BY price_rank DESC;
```
Computing ranks in the SELECT once, then sorting by the alias, avoids re-running one of the correlated subqueries.

## Q73: Use a subquery in HAVING with a non-trivial expression: keep departments whose average salary beats the company average by more than 10%.
**Query:**
```sql
SELECT department_id, AVG(salary) AS dept_avg
FROM employees
GROUP BY department_id
HAVING AVG(salary) > 1.10 * (SELECT AVG(salary) FROM employees);
```
**Explanation:** The scalar subquery supplies the company average and HAVING applies an arithmetic threshold across the comparison.

## Q74: Avoid writing the same subquery twice by hoisting it into a derived table used by both SELECT and WHERE.
**Query:**
```sql
-- Wasteful: same subquery computed twice
SELECT name, salary - (SELECT AVG(salary) FROM employees) AS gap
FROM employees
WHERE salary - (SELECT AVG(salary) FROM employees) > 0;

-- Hoisted: compute once, reuse for projection and filter
SELECT e.name, e.salary, d.avg_sal, e.salary - d.avg_sal AS gap
FROM employees e
CROSS JOIN (SELECT AVG(salary) AS avg_sal FROM employees) d
WHERE e.salary - d.avg_sal > 0;
```
**Explanation:** The CROSS JOIN derived table evaluates the average once and both the projection and predicate read from the single value — the textbook "avoid subquery repetition" move.

## Q75: Solve a three-level nesting where the innermost value feeds a middle filter that feeds an outer projection.
**Query:**
```sql
-- PostgreSQL
SELECT employee_id, name, salary
FROM employees
WHERE department_id IN (
      SELECT department_id
      FROM (SELECT department_id, AVG(salary) AS a
            FROM employees
            WHERE hire_date > (SELECT MIN(hire_date) + INTERVAL '300 days' FROM employees)
            GROUP BY department_id
            HAVING AVG(salary) > (SELECT AVG(salary) FROM employees)) mid
      WHERE a = (SELECT MAX(a) FROM
                 (SELECT department_id, AVG(salary) AS a
                  FROM employees WHERE hire_date > (SELECT MIN(hire_date)
                  + INTERVAL '300 days' FROM employees)
                  GROUP BY department_id HAVING AVG(salary) > (SELECT AVG(salary) FROM employees)) t));
```
**Explanation:** Three independent scalar subqueries (a hire-date boundary, a company average) gate a grouped derived table, whose winner department is then matched against employees — deep but fully non-correlated composition.

## Q76: Show that a scalar subquery in SELECT recomputes per row, then eliminate the waste with a derived table.
**Query:**
```sql
-- PostgreSQL: evaluate per row (EXPLAIN shows a Seq Scan w/ scalar subplan)
SELECT order_id, (SELECT MAX(order_date) FROM orders) AS last_order_date
FROM orders;

-- Hoisted: computed once as a nested-loop outer constant
SELECT o.order_id, m.last_order_date
FROM orders o
CROSS JOIN (SELECT MAX(order_date) AS last_order_date FROM orders) m;
```
**Explanation:** Both return identical columns, but the CROSS JOIN derived table is evaluated once; on a million-row orders table the difference is dramatic.

## Q77: Find products that share a price with at least one other product using a grouped derived table plus a JOIN back.
**Query:**
```sql
SELECT p.product_id, p.product_name, p.price
FROM products p
JOIN (SELECT price FROM products GROUP BY price HAVING COUNT(*) > 1) shared
  ON shared.price = p.price
ORDER BY p.price;
```
**Explanation:** The derived table isolates prices that occur more than once and the JOIN fans them back out to every product at those prices.

## Q78: Keep products priced above the 75th-percentile price using an order-statistics subquery.
**Query:**
```sql
-- MySQL
SELECT p.product_id, p.product_name, p.price
FROM products p
WHERE p.price >= (SELECT price
                  FROM (SELECT price FROM products
                        ORDER BY price LIMIT 1 OFFSET
                          (SELECT CAST(0.75 * (SELECT COUNT(*) FROM products) AS UNSIGNED))) pct);
```
**Explanation:** The innermost scalar supplies the offset, the middle SELECT grabs the threshold price for the 75th percentile, and WHERE filters the catalog.

## Q79: Build a read-only pipeline with three stacked derived tables: normalize, enrich, then filter.
**Query:**
```sql
-- PostgreSQL
SELECT * FROM (
  SELECT * FROM (
    SELECT product_id, price, ROUND(price * 1.21, 2) AS price_with_vat
    FROM products
    WHERE discontinued = 0
  ) enriched
  WHERE price_with_vat > (SELECT AVG(price_with_vat) FROM (
        SELECT ROUND(price * 1.21, 2) AS price_with_vat FROM products) base)
) final
ORDER BY price_with_vat DESC;
```
**Explanation:** Each derived layer transforms or narrows the row set, and the final SELECT does presentation — the non-correlated, write-once version of a CTE pipeline.

## Q80: Guard NOT IN against NULL three ways in one answer choice list.
**Query:**
```sql
-- Guard A: sanitize the subquery
SELECT customer_id FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL);

-- Guard B: swap to NOT EXISTS
SELECT c.customer_id FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);

-- Guard C: (PostgreSQL) use IS DISTINCT FROM on a NOT-EXISTS-style anti-join already shown in B.
```
**Explanation:** Sanitizing the inner set or switching to NOT EXISTS both neutralize the NULL poison — prefer Guard B for clarity, Guard A when you must keep NOT IN for the planner.

## Q81: Use EXISTS inside a GROUP BY filter: keep only customers with ≥ 3 orders, expressed without HAVING on raw COUNT.
**Query:**
```sql
SELECT oc.customer_id
FROM (SELECT customer_id, COUNT(*) AS orders_count
      FROM orders GROUP BY customer_id) oc
WHERE EXISTS (SELECT 1 FROM orders o
              WHERE o.customer_id = oc.customer_id
              GROUP BY o.customer_id HAVING COUNT(*) >= 3);
```
**Explanation:** EXISTS can wrap a grouped subquery whose HAVING decides existence — redundancy here is deliberate to show EXISTS tolerating an aggregate inside.

**Alt1:**
```sql
SELECT customer_id FROM orders GROUP BY customer_id HAVING COUNT(*) >= 3;
```
The plain GROUP BY/HAVING is the real-world answer; the EXISTS wrapper matters when you need to gate on a second table's coarse fact first.

## Q82: Compute the average of the top 5 salaries using a derived table.
**Query:**
```sql
-- MySQL / PostgreSQL
SELECT AVG(top5.salary) AS avg_top5_salary
FROM (SELECT salary FROM employees ORDER BY salary DESC LIMIT 5) top5;
```
**Explanation:** The derived table reduces employees to exactly five rows and the outer aggregate averages only them.

**Alt1:**
```sql
SELECT AVG(salary) FROM (
  SELECT salary, ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn
  FROM employees
) ranked WHERE rn <= 5;
```
The LIMIT version is concise; the windowed version snapshots the rank so ties are handled explicitly.

## Q83: Show each employee's salary gap to the second-highest salary using a nested scalar subquery in SELECT.
**Query:**
```sql
SELECT employee_id, name,
       (SELECT MAX(salary) FROM employees
        WHERE salary < (SELECT MAX(salary) FROM employees)) - salary AS gap_to_2nd
FROM employees;
```
**Explanation:** The middle SELECT computes the second-highest salary via the inner MAX, and the projection subtracts the employee's own salary.

## Q84: Find the customer with the most orders using a derived table plus a scalar match.
**Query:**
```sql
SELECT c.customer_id, c.name, ord.cnt
FROM customers c
JOIN (SELECT customer_id, COUNT(*) AS cnt
      FROM orders GROUP BY customer_id) ord
  ON ord.customer_id = c.customer_id
WHERE ord.cnt = (SELECT MAX(cnt)
                 FROM (SELECT COUNT(*) AS cnt FROM orders GROUP BY customer_id) all_counts);
```
**Explanation:** The inner derived table counts per customer; the scalar subquery finds the maximum count; the JOIN exposes the winning customer row(s).

## Q85: Reimplement RANK manually by nesting derived tables to yield ordinal positions with no ties.
**Query:**
```sql
SELECT r1.product_id, COUNT(r2.product_id) + 1 AS manual_rank
FROM products r1
LEFT JOIN products r2 ON r2.price > r1.price
GROUP BY r1.product_id
ORDER BY manual_rank;
```
**Explanation:** Each product is compared against strictly pricier products; the count of those pricier equals "rows ahead" + 1, giving a dense, tie-free ordinal rank through a pure self-join.

## Q86: Detect gaps in a sequence of invoice numbers using a derived table and a scalar minimum check.
**Query:**
```sql
SELECT i.invoice_id, i.next_id - i.invoice_id AS gap_size
FROM (SELECT invoice_id,
             LEAD(invoice_id) OVER (ORDER BY invoice_id) AS next_id
      FROM invoices) i
WHERE i.next_id - i.invoice_id > 1
ORDER BY i.invoice_id;
```
**Explanation:** The derived table materializes each invoice's successor via LEAD; the outer WHERE keeps rows where the successor is not adjacent, exposing the missing numbers.

**Alt1:**
```sql
SELECT invoice_id
FROM invoices
WHERE invoice_id NOT IN (SELECT invoice_id + 1 FROM invoices);
```
The NOT IN form flags the last row before a hole (plus the final invoice), which is the classic pre-window-functions gap check.

## Q87: Find employees hired earlier than the earliest hire in the Sales department.
**Query:**
```sql
SELECT employee_id, name, hire_date
FROM employees
WHERE hire_date < (SELECT MIN(hire_date)
                   FROM employees
                   WHERE department_id = (SELECT department_id
                                          FROM departments WHERE name = 'Sales'));
```
**Explanation:** The innermost scalar resolves Sales to an id, the middle MIN finds its earliest hire, and the outer WHERE keeps everyone hired before that date — an entirely non-correlated chain.

## Q88: Use a subquery over the SAME table as the outer query without correlating: filter employees whose salary is above the company median via a computed list.
**Query:**
```sql
-- MySQL 8 doesn't have MEDIAN(); emulate with a middle-value subquery
SELECT employee_id, name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM (
                 SELECT salary FROM employees
                 ORDER BY salary DESC
                 LIMIT 1 OFFSET (SELECT CAST((SELECT COUNT(*) FROM employees) / 2 AS UNSIGNED))) median)
ORDER BY salary;
```
**Explanation:** The derived table hunts the middle salary (median stand-in) regardless of the outer scan; the outer query compares employees to that one value with zero correlation between the levels.

## Q89: Build a grandparent–parent–child nesting: departments feeding products feeding line items.
**Query:**
```sql
SELECT li.order_id, li.product_id, p.product_name, p.department_id
FROM order_items li
JOIN products p ON p.product_id = li.product_id
WHERE p.department_id IN (
      SELECT d.department_id
      FROM departments d
      WHERE d.budget > (SELECT AVG(budget)
                        FROM departments d2
                        WHERE d2.budget > (SELECT MIN(budget) FROM departments)))
ORDER BY li.order_id;
```
**Explanation:** The innermost scalar supplies the floor budget, the middle averages the departments above that floor, and the outer membership test only admits line items from generous departments.

## Q90: Show that mixed NULLs inside an IN list are harmless, unlike NOT IN, with a demonstration.
**Query:**
```sql
-- IN survives embedded NULLs correctly
SELECT customer_id FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders);  -- NULLs are just never equal, fine

-- The same data through NOT IN collapses:
SELECT customer_id FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL);
-- (the IS NOT NULL is what keeps this second query honest)
```
**Explanation:** `x IN (1, NULL)` is `x=1 OR x=NULL` — the OR makes the NULL harmless, while `x NOT IN`'s AND chain makes NULL fatal. The IN form needs no guard.

## Q91: Use ANY/ALL with an expression list instead of a subquery and compare to the subquery form.
**Query:**
```sql
-- MySQL / PostgreSQL
SELECT name FROM employees
WHERE salary > ANY (30000, 45000, 60000);                       -- vs the lowest entry

-- The subquery equivalent:
SELECT name FROM employees
WHERE salary > ANY (SELECT salary FROM salary_bands);           -- any band value
```
**Explanation:** ANY/ALL accept both literal lists and subqueries; lists are handy for hardcoded thresholds while subqueries keep the set dynamic and indexable.

## Q92: Compare `> (SELECT MAX(x))` with `> ALL (SELECT x)` on an edge case.
**Query:**
```sql
SELECT name FROM employees WHERE salary > (SELECT MAX(salary) FROM employees);
-- NULL when no rows -> no employees selected

SELECT name FROM employees WHERE salary > ALL (SELECT salary FROM employees);
-- TRUE for the empty set -> EVERY employee selected
```
**Explanation:** The MAX version degrades to NULL and filters everything out; the ALL version degrades to TRUE and keeps everything. Know which behavior you want for empty tables.

## Q93: Use EXISTS to enforce an "at least one" invariant: products that have a purchase record AND a supplier contract.
**Query:**
```sql
SELECT p.product_id, p.product_name
FROM products p
WHERE EXISTS (SELECT 1 FROM purchases pu WHERE pu.product_id = p.product_id)
  AND EXISTS (SELECT 1 FROM supplier_contracts sc WHERE sc.product_id = p.product_id);
```
**Explanation:** Two independent existence probes both must pass; each can use its own index and stop on the first hit, keeping the probe cheap.

## Q94: Sort customers by their most recent order date using ORDER BY with a scalar subquery.
**Query:**
```sql
SELECT c.customer_id, c.name
FROM customers c
ORDER BY (SELECT MAX(o.order_date) FROM orders o WHERE o.customer_id = c.customer_id) DESC NULLS LAST;
```
**Explanation:** The scalar subquery yields each customer's latest order date (NULL for never-ordered), and `NULLS LAST` keeps the zero-order customers at the bottom.
(PostgreSQL)

**Alt1:**
```sql
SELECT c.customer_id, c.name
FROM customers c
LEFT JOIN (SELECT customer_id, MAX(order_date) AS last_order
           FROM orders GROUP BY customer_id) l
  ON l.customer_id = c.customer_id
ORDER BY l.last_order DESC;
```
The join-to-derived-table version computes each max once, versus the per-row subquery in ORDER BY.

## Q95: Combine two scalar subqueries arithmetically in the SELECT list to produce a "headroom" metric.
**Query:**
```sql
SELECT d.department_id,
       (SELECT MAX(salary) FROM employees e WHERE e.department_id = d.department_id)
       - (SELECT MIN(salary) FROM employees e WHERE e.department_id = d.department_id) AS salary_span,
       (SELECT AVG(salary) FROM employees e WHERE e.department_id = d.department_id) AS dept_average
FROM departments d;
```
**Explanation:** Multiple scalar subqueries can be combined as operands of one arithmetic/display expression; each is a single value, so the projection stays scalar. For heavy tables, prefer Alt1.

**Alt1:**
```sql
SELECT d.department_id, s.salary_span, s.dept_average
FROM departments d
JOIN (SELECT department_id,
             MAX(salary) - MIN(salary) AS salary_span,
             AVG(salary) AS dept_average
      FROM employees GROUP BY department_id) s
  ON s.department_id = d.department_id;
```
Three correlated subqueries become one grouped derived table — one scan of employees instead of three per department.

## Q96: Compute month-over-month revenue by joining two derived tables aggregated over different date ranges.
**Query:**
```sql
-- SQL Server
SELECT cur.yr, cur.mo, cur.revenue, prev.revenue AS prev_month_revenue
FROM (SELECT YEAR(order_date) AS yr, MONTH(order_date) AS mo, SUM(total) AS revenue
      FROM orders GROUP BY YEAR(order_date), MONTH(order_date)) cur
LEFT JOIN (SELECT YEAR(order_date) AS yr, MONTH(order_date) AS mo, SUM(total) AS revenue
      FROM orders GROUP BY YEAR(order_date), MONTH(order_date)) prev
  ON prev.yr = CASE WHEN cur.mo = 1 THEN cur.yr - 1 ELSE cur.yr END
 AND prev.mo = CASE WHEN cur.mo = 1 THEN 12 ELSE cur.mo - 1 END
ORDER BY cur.yr, cur.mo;
```
**Explanation:** Two independent grouped derived tables, joined with a month-rollover key built from CASE expressions, recreate lagged revenue without window functions.

## Q97: Clean a messy aggregation by deduplicating inside a subquery before it feeds an outer GROUP BY.
**Query:**
```sql
SELECT source.channel, COUNT(*) AS signups
FROM (SELECT DISTINCT email, channel FROM signup_events) source
GROUP BY source.channel
ORDER BY signups DESC;
```
**Explanation:** The inner DISTINCT collapses duplicate signup events per email; the outer GROUP BY then counts real signups per channel rather than raw event rows.

## Q98: Represent set intersection with EXISTS: employees who are both engineers and project leads.
**Query:**
```sql
SELECT e.employee_id, e.name
FROM employees e
WHERE EXISTS (SELECT 1 FROM roles r WHERE r.employee_id = e.employee_id AND r.role = 'engineer')
  AND EXISTS (SELECT 1 FROM project_lead pl WHERE pl.employee_id = e.employee_id);
```
**Explanation:** Two EXISTS tests implement an intersection without JOINs; each probe is index-driven and exits on the first match, which is the standard anti-large-IN shape.

## Q99: Boss level: combine IN, ALL, ANY, and EXISTS in one uncorrelated query that finds the best employee per salary-fund band.
**Query:**
```sql
-- PostgreSQL
SELECT e.employee_id, e.name, e.salary
FROM employees e
WHERE e.salary IN (                           -- IN: membership in the top bands
      SELECT band_top FROM salary_bands b
      WHERE b.band_top > ANY (                -- ANY: bands above the 25th percentile
            SELECT price FROM (SELECT ROUND(0.25 * (SELECT MAX(salary) FROM employees))
                               AS price) q))
  AND e.salary >= ALL (SELECT band_floor FROM salary_bands)  -- ALL: above every floor
  AND EXISTS (SELECT 1 FROM awards a WHERE a.employee_id = e.employee_id)  -- EXISTS: has an award
ORDER BY e.salary DESC;
```
**Explanation:** Four subquery flavors cooperate in one WHERE clause: `IN` filters by band ceilings, `ANY` widens to bands above a derived percentile, `ALL` enforces the floor for every band, and `EXISTS` requires award history — all non-correlated.

## Q100: Final boss: multi-column row IN + derived table for per-category "best value" products, then rank those with a manual nested counter.
**Query:**
```sql
-- PostgreSQL / MySQL (row constructor supported in both)
SELECT wide.category_id, wide.product_name,
       wide.price / wide.category_avg AS value_ratio,
       (SELECT COUNT(*) FROM products pX
        WHERE pX.category_id = wide.category_id
          AND pX.price >= wide.category_avg) AS products_at_or_above
FROM (
  SELECT p.category_id, p.product_name, p.price, cat.category_avg
  FROM products p
  JOIN (SELECT category_id, AVG(price) AS category_avg
        FROM products GROUP BY category_id) cat
    ON cat.category_id = p.category_id
  WHERE (p.category_id, p.price) IN (              -- ROW IN: tied at category max
        SELECT category_id, MAX(price)
        FROM products GROUP BY category_id)
) wide
WHERE wide.category_id IN (SELECT category_id FROM active_categories)
ORDER BY wide.value_ratio DESC;
```
**Explanation:** A grouped derived table (averages) feeds a JOIN; a row-constructor `IN` isolates per-category maximum-priced products; a WHERE member check against an active-categories subquery thins results; and a final scalar counter attaches an ordinal — a layered composition exercising nearly every technique in this file.
