# Correlated Subqueries — 100 SQL Interview Q&A

## Q1: Write a query to list each employee along with the name of their department using a correlated scalar subquery.

**Query:**
```sql
SELECT e.name,
       (SELECT d.name
          FROM departments d
         WHERE d.id = e.dept_id) AS dept_name
  FROM employees e;
```
**Explanation:** For every outer row e, the inner query runs once, keyed on e.dept_id, and returns that employee's department name.

## Q2: Write a query to list each employee along with the highest salary in their department.

**Query:**
```sql
SELECT e.name,
       e.salary,
       (SELECT MAX(e2.salary)
          FROM employees e2
         WHERE e2.dept_id = e.dept_id) AS dept_max_salary
  FROM employees e;
```
**Explanation:** The correlated subquery conceptually groups by dept_id and returns the max salary for the outer row's department.

**Alt1:** JOIN + GROUP BY computes the aggregate once instead of once per row — usually faster on large tables:
```sql
SELECT e.name, e.salary, d.max_salary
  FROM employees e
  JOIN (SELECT dept_id, MAX(salary) AS max_salary
          FROM employees
         GROUP BY dept_id) d
    ON d.dept_id = e.dept_id;
```
**Note:** Both return the same per-employee number; the JOIN+GROUP BY version rewrites the correlated aggregate into an equijoin on the grouped result.

## Q3: Use a correlated COUNT to list each customer with the number of orders they have placed.

**Query:**
```sql
SELECT c.name,
       (SELECT COUNT(*)
          FROM orders o
         WHERE o.customer_id = c.id) AS order_count
  FROM customers c;
```
**Explanation:** Each outer customer triggers the inner COUNT(*) over only their own orders.

**Alt1:** OUTER JOIN + GROUP BY — also returns 0 rows for customers with no orders and is generally cheaper:
```sql
SELECT c.name, COUNT(o.id) AS order_count
  FROM customers c
  LEFT JOIN orders o ON o.customer_id = c.id
 GROUP BY c.id, c.name;
```
**Note:** The correlated version is only competitive when the outer table is tiny or the correlated spot is indexed.

## Q4: Write a query to list each customer with the total value of all of their orders.

**Query:**
```sql
SELECT c.name,
       (SELECT SUM(o.amount)
          FROM orders o
         WHERE o.customer_id = c.id) AS total_spent
  FROM customers c;
```
**Explanation:** Correlated aggregate — SUM is computed over the current customer's rows only and fed straight into the outer SELECT list.

## Q5: Write a query to list each product with its average review rating.

**Query:**
```sql
SELECT p.name,
       (SELECT AVG(r.rating)
          FROM reviews r
         WHERE r.product_id = p.id) AS avg_rating
  FROM products p;
```
**Explanation:** AVG ignores NULL ratings in SQL; a product with no reviews yields a NULL, not zero — handle with COALESCE if needed.

## Q6: Write a query to show each employee and the average salary of their department.

**Query:**
```sql
SELECT e.name,
       (SELECT AVG(e2.salary)
          FROM employees e2
         WHERE e2.dept_id = e.dept_id) AS dept_avg
  FROM employees e;
```
**Explanation:** The correlation column (dept_id) is read from the outer row; employees with a NULL dept_id can't match, so the subquery returns NULL.

## Q7: Find all employees whose salary is above the average salary of their own department.

**Query:**
```sql
SELECT e.name, e.salary
  FROM employees e
 WHERE e.salary > (SELECT AVG(e2.salary)
                     FROM employees e2
                    WHERE e2.dept_id = e.dept_id);
```
**Explanation:** Comparative correlated WHERE — each outer row is tested against the aggregate of its own group.

**Alt1:** Derived table computes AVG once up front, then joins:
```sql
SELECT e.name, e.salary
  FROM employees e
  JOIN (SELECT dept_id, AVG(salary) AS avg_sal
          FROM employees
         GROUP BY dept_id) d
    ON d.dept_id = e.dept_id
 WHERE e.salary > d.avg_sal;
```
**Note:** Identical result; the JOIN+GROUP BY rewrite is the go-to fix when the correlated version gets slow.

## Q8: Find departments that have at least one employee earning more than 100,000 (EXISTS pattern).

**Query:**
```sql
SELECT d.name
  FROM departments d
 WHERE EXISTS (SELECT 1
                 FROM employees e
                WHERE e.dept_id = d.id
                  AND e.salary > 100000);
```
**Explanation:** EXISTS is a semi-join — it stops at the first matching row and only tests presence.

**Alt1:** JOIN + DISTINCT expresses the same semi-join:
```sql
SELECT DISTINCT d.name
  FROM departments d
  JOIN employees e ON e.dept_id = d.id
 WHERE e.salary > 100000;
```
**Note:** The JOIN may multiply rows when many employees match; EXISTS reads less when an early match is likely and uses a dept_id index better.

## Q9: Find customers who placed at least one order within the last 30 days.

**Query:**
```sql
SELECT c.name
  FROM customers c
 WHERE EXISTS (SELECT 1
                 FROM orders o
                WHERE o.customer_id = c.id
                  AND o.order_date >= CURRENT_DATE - INTERVAL 30 DAY);
```
**Explanation:** Correlated EXISTS on the customer's orders, with the recency predicate pushed inside the subquery so it can short-circuit on a filtered index.

## Q10: Find all products that have never been ordered (NOT EXISTS anti-join).

**Query:**
```sql
SELECT p.name
  FROM products p
 WHERE NOT EXISTS (SELECT 1
                     FROM order_items oi
                    WHERE oi.product_id = p.id);
```
**Explanation:** NOT EXISTS keeps an outer row only when the correlated subquery yields zero rows — a true anti-join with no NULL pitfalls.

## Q11: List all employees who have no direct reports.

**Query:**
```sql
SELECT e.name
  FROM employees e
 WHERE NOT EXISTS (SELECT 1
                     FROM employees sub
                    WHERE sub.manager_id = e.id);
```
**Explanation:** Self-referencing anti-join: each employee is kept only if nobody in the table points back at them as a manager.

## Q12: Find customers who have never placed any order.

**Query:**
```sql
SELECT c.name
  FROM customers c
 WHERE NOT EXISTS (SELECT 1
                     FROM orders o
                    WHERE o.customer_id = c.id);
```
**Explanation:** Classic anti-join — keeps customers whose correlated result set is empty.

**Alt1:** The same anti-join written as an outer join with a NULL probe:
```sql
SELECT c.name
  FROM customers c
  LEFT JOIN orders o ON o.customer_id = c.id
 WHERE o.id IS NULL;
```
**Note:** LEFT JOIN ... IS NULL is usually the faster plan on wide fact tables; NOT EXISTS wins when a covering index on orders(customer_id) exists.

## Q13: Find departments that currently have no employees.

**Query:**
```sql
SELECT d.name
  FROM departments d
 WHERE NOT EXISTS (SELECT 1
                     FROM employees e
                    WHERE e.dept_id = d.id);
```
**Explanation:** The correlation is driven by the dimension table: each department probes the employee table for any member.

## Q14: Find students who have never sat any exam.

**Query:**
```sql
SELECT s.name
  FROM students s
 WHERE NOT EXISTS (SELECT 1
                     FROM exams x
                    WHERE x.student_id = s.id);
```
**Explanation:** Same anti-join pattern as Q12; guaranteed correct even if the exams table later gains NULL student_ids.

## Q15: Using EXISTS, find departments that contain more than five employees.

**Query:**
```sql
SELECT d.name
  FROM departments d
 WHERE EXISTS (SELECT 1
                 FROM employees e
                WHERE e.dept_id = d.id
                HAVING COUNT(*) > 5);
```
**Explanation:** The correlated subquery aggregates the group (HAVING without GROUP BY aggregates the filtered set) and EXISTS turns the aggregate into a presence test.

## Q16: Find products that have been ordered more than 10 times in total.

**Query:**
```sql
SELECT p.name
  FROM products p
 WHERE EXISTS (SELECT 1
                 FROM order_items oi
                WHERE oi.product_id = p.id
                HAVING SUM(oi.quantity) > 10);
```
**Explanation:** Same present-aggregate-in-EXISTS idiom: presence of a group whose SUM exceeds 10 decides the outer row.

## Q17: Find the highest-paid employee in each department WITHOUT using window functions.

**Query:**
```sql
SELECT e.name, e.salary, e.dept_id
  FROM employees e
 WHERE e.salary = (SELECT MAX(e2.salary)
                     FROM employees e2
                    WHERE e2.dept_id = e.dept_id);
```
**Explanation:** Row-to-group maximum: keep every row whose salary ties the max of its own department. Ties yield multiple rows per department.

**Alt1:** Window function equivalent (same semantics, one pass over the table):
```sql
SELECT name, salary, dept_id
  FROM (SELECT e.*, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) rnk
          FROM employees e) t
 WHERE rnk = 1;
```
**Note:** RANK keeps all tied maxes exactly like the correlated version; prefer the window version at scale.

## Q18: Find the most recent order for every customer WITHOUT window functions.

**Query:**
```sql
SELECT o.*
  FROM orders o
 WHERE o.order_date = (SELECT MAX(o2.order_date)
                         FROM orders o2
                        WHERE o2.customer_id = o.customer_id);
```
**Explanation:** Max-of-group equality correlation; a customer with two orders on the same max date returns both rows.

**Alt1:** ORDER BY ... LIMIT 1 inside the correlated subquery forces exactly one row per customer:
```sql
-- MySQL / PostgreSQL / SQL Server (TOP 1 in T-SQL)
SELECT o.*
  FROM orders o
 WHERE o.id = (SELECT o2.id
                 FROM orders o2
                WHERE o2.customer_id = o.customer_id
                ORDER BY o2.order_date DESC, o2.id DESC
                LIMIT 1);
```
**Note:** Deterministic with the id tiebreak, but the LIMIT-1 form typically forces a scan of each bucket.

## Q19: Find the latest login time for each user (assume a logins table keyed by user_id).

**Query:**
```sql
SELECT l.user_id, l.logged_in_at
  FROM logins l
 WHERE l.logged_in_at = (SELECT MAX(l2.logged_in_at)
                           FROM logins l2
                          WHERE l2.user_id = l.user_id);
```
**Explanation:** A pure per-group max via equality correlation — no ranking machinery needed.

## Q20: Find the earliest-hired employee in each department.

**Query:**
```sql
SELECT e.name, e.hire_date, e.dept_id
  FROM employees e
 WHERE e.hire_date = (SELECT MIN(e2.hire_date)
                        FROM employees e2
                       WHERE e2.dept_id = e.dept_id);
```
**Explanation:** MIN per department correlated back to each outer employee; co-founders hired on the same date both appear.

## Q21: Find the cheapest product within each category.

**Query:**
```sql
SELECT p.name, p.price, p.category_id
  FROM products p
 WHERE p.price = (SELECT MIN(p2.price)
                    FROM products p2
                   WHERE p2.category_id = p.category_id);
```
**Explanation:** The row is identified by matching the per-category minimum price instead of by its own primary key, so all tied-cheapest products are returned.

## Q22: Find the last transaction record per bank account (transactions: id, account_id, amount, tx_time).

**Query:**
```sql
SELECT t.id, t.account_id, t.amount, t.tx_time
  FROM transactions t
 WHERE t.tx_time = (SELECT MAX(t2.tx_time)
                      FROM transactions t2
                     WHERE t2.account_id = t.account_id);
```
**Explanation:** Equality comparison against the per-account maximum timestamp; duplicate max timestamps mean multiple rows per account.

## Q23: Find employees who earn more than their department's average AND more than the company-wide average.

**Query:**
```sql
SELECT e.name, e.salary
  FROM employees e
 WHERE e.salary > (SELECT AVG(e2.salary)
                     FROM employees e2
                    WHERE e2.dept_id = e.dept_id)   -- correlated
   AND e.salary > (SELECT AVG(e3.salary)
                     FROM employees e3);              -- not correlated
```
**Explanation:** The first subquery is correlated (recomputed per row); the second has no correlation and can be computed once — a good demonstration of the two kinds side by side.

## Q24: Find customers whose number of orders is greater than the average number of orders per customer.

**Query:**
```sql
SELECT c.name
  FROM customers c
 WHERE (SELECT COUNT(*)
          FROM orders o
         WHERE o.customer_id = c.id) >
       (SELECT AVG(cnt)
          FROM (SELECT customer_id, COUNT(*) AS cnt
                  FROM orders
                 GROUP BY customer_id) t);
```
**Explanation:** Left side is a correlated COUNT per customer; the right side is a scalar over a derived table (one COUNT per customer, then averaged).

## Q25: Find employees who earn more than every other employee in the same department (ALL comparison).

**Query:**
```sql
SELECT e.name, e.salary
  FROM employees e
 WHERE e.salary > ALL (SELECT e2.salary
                         FROM employees e2
                        WHERE e2.dept_id = e.dept_id
                          AND e2.id <> e.id);
```
**Explanation:** `> ALL` is true only when the salary beats every value the correlated list returns; if that list could contain NULL, the comparison silently becomes UNKNOWN, which `> ALL` treats as false.
## Q26: Using a correlated HAVING, find which job roles within each department earn above that department's own average salary.

**Query:**
```sql
SELECT e.dept_id, e.job, AVG(e.salary) AS job_avg
  FROM employees e
 GROUP BY e.dept_id, e.job
HAVING AVG(e.salary) > (SELECT AVG(e2.salary)
                          FROM employees e2
                         WHERE e2.dept_id = e.dept_id);
```
**Explanation:** The HAVING subquery is correlated to the outer group — it reads e.dept_id from the grouped row and keeps only (dept, job) groups whose average beats the whole department's average.

## Q27: Find each customer's top-spending product category using a correlated HAVING.

**Query:**
```sql
SELECT o.customer_id, o.category, SUM(o.amount) AS total
  FROM orders o
 GROUP BY o.customer_id, o.category
HAVING SUM(o.amount) = (SELECT MAX(s)
                          FROM (SELECT customer_id, category,
                                       SUM(amount) AS s
                                  FROM orders
                                 GROUP BY customer_id, category) t
                         WHERE t.customer_id = o.customer_id);
```
**Explanation:** Each grouped row's SUM is compared against a correlated subquery that computes the max category total for that same customer.

**Alt1:** ROW_NUMBER per customer-category group gives the same answer and is usually faster:
```sql
SELECT customer_id, category, total
  FROM (SELECT customer_id, category, SUM(amount) AS total,
               ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY SUM(amount) DESC) rn
          FROM orders
         GROUP BY customer_id, category) t
 WHERE rn = 1;
```
**Note:** The correlated version needs the two-level self aggregate; the window rewrite scans once — but the correlated form is the classic no-window answer.

## Q28: List departments where the highest salary is more than double the lowest salary, using HAVING.

**Query:**
```sql
SELECT e.dept_id, MIN(e.salary) AS lo, MAX(e.salary) AS hi
  FROM employees e
 GROUP BY e.dept_id
HAVING MAX(e.salary) > 2 * MIN(e.salary);
```
**Explanation:** A group-level filter comparing two aggregates of the same group; simplest when it needs no outside value.

**Alt1:** To compare against an external benchmark, correlate to the company average:
```sql
SELECT e.dept_id
  FROM employees e
 GROUP BY e.dept_id
HAVING MAX(e.salary) > 2 * (SELECT AVG(e2.salary) FROM employees e2);
```
**Note:** The second form triggers once globally — it is correlated to no group, so it remains a one-time scalar despite living inside HAVING.

## Q29: Find departments whose headcount is greater than the average headcount across all departments.

**Query:**
```sql
SELECT e.dept_id, COUNT(*) AS headcount
  FROM employees e
 GROUP BY e.dept_id
HAVING COUNT(*) > (SELECT AVG(cnt)
                     FROM (SELECT dept_id, COUNT(*) AS cnt
                             FROM employees
                            GROUP BY dept_id) t);
```
**Explanation:** Group-level filter: each department's COUNT(*) is tested against the average of all counts computed from a derived table.

**Alt1:** Correlated variant that keeps only groups bigger than their own sub-aggregate row:
```sql
SELECT e.dept_id, COUNT(*) AS headcount
  FROM employees e
 GROUP BY e.dept_id
HAVING COUNT(*) > (SELECT AVG(cnt)
                     FROM (SELECT dept_id, COUNT(*) AS cnt
                             FROM employees
                            GROUP BY dept_id) t
                    WHERE t.dept_id = e.dept_id);
```
**Note:** Trivially true here because each group is always equal to itself — a live demonstration that correlation must reference an actual outer group value to be meaningful.

## Q30: For each store, find the nearest other store by Manhattan distance, WITHOUT window functions.

**Query:**
```sql
SELECT s1.name,
       (SELECT s2.name
          FROM stores s2
         WHERE s2.id <> s1.id
         ORDER BY ABS(s1.x - s2.x) + ABS(s1.y - s2.y), s2.name
         LIMIT 1) AS nearest_store
  FROM stores s1;
```
**Explanation:** Nearest-neighbor per group: the correlated subquery sorts the candidate stores by distance and pulls the closest one with LIMIT 1.

## Q31: For each employee, find the colleague in the same department whose salary is closest to their own.

**Query:**
```sql
SELECT e1.name,
       (SELECT e2.name
          FROM employees e2
         WHERE e2.dept_id = e1.dept_id
           AND e2.id <> e1.id
         ORDER BY ABS(e2.salary - e1.salary), e2.name
         LIMIT 1) AS closest_salary_peer
  FROM employees e1;
```
**Explanation:** Nearest-neighbor on a scalar attribute: ORDER BY the absolute difference, tie-break deterministically, LIMIT 1 per outer row.

## Q32: For each order, show the amount of the customer's previous order using an inequality correlated subquery.

**Query:**
```sql
SELECT o.id, o.customer_id, o.order_date, o.amount,
       (SELECT MAX(o2.order_date)
          FROM orders o2
         WHERE o2.customer_id = o.customer_id
           AND o2.order_date < o.order_date) AS prev_order_date
  FROM orders o;
```
**Explanation:** Inequality correlation (`<` on the ordering key) finds the most recent row strictly before the outer row — a self-join-like lookup without window functions.

**Alt1:** LAG() makes the same "previous row" explicit:
```sql
SELECT id, customer_id, order_date, amount,
       LAG(amount, 1) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_amount
  FROM orders;
```
**Note:** The correlated version survives ties correctly only with a strict `<` + MAX; LAG is simpler and O(n log n) overall.

## Q33: For each transaction, find the amount of the next transaction on the same account in chronological order.

**Query:**
```sql
SELECT t.id, t.account_id, t.amount,
       (SELECT t2.amount
          FROM transactions t2
         WHERE t2.account_id = t.account_id
           AND t2.tx_time > t.tx_time
         ORDER BY t2.tx_time, t2.id
         LIMIT 1) AS next_amount
  FROM transactions t;
```
**Explanation:** Forward-looking inequality: ORDER BY ascending then LIMIT 1 gives the immediate successor for the outer row's account.

## Q34: For each employee, using ORDER BY ... LIMIT 1, return the salary of the next-better-paid colleague in the same department.

**Query:**
```sql
SELECT e1.name, e1.salary,
       (SELECT e2.salary
          FROM employees e2
         WHERE e2.dept_id = e1.dept_id
           AND e2.salary > e1.salary
         ORDER BY e2.salary, e2.name
         LIMIT 1) AS next_higher_salary
  FROM employees e1;
```
**Explanation:** A ranked-value fetch: after filtering to strictly-higher salaries, ORDER BY + LIMIT 1 grabs the smallest qualifying one (the immediate neighbor).

## Q35: Find the second-highest salary in each department using ORDER BY ... LIMIT 1 OFFSET 1.

**Query:**
```sql
SELECT e1.name, e1.salary AS second_highest
  FROM employees e1
 WHERE e1.salary = (SELECT DISTINCT e2.salary
                      FROM employees e2
                     WHERE e2.dept_id = e1.dept_id
                     ORDER BY e2.salary DESC
                     LIMIT 1 OFFSET 1);
```
**Explanation:** The correlated subquery sorts that department's distinct salaries descending and takes the second one; equality then finds who holds it.

**Alt1:** MySQL 8 / PostgreSQL / SQL Server can express the same via a window:
```sql
SELECT name, salary, dept_id
  FROM (SELECT e.*, DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) dr
          FROM employees e) t
 WHERE dr = 2;
```
**Note:** DISTINCT inside the correlated query collapses ties for the rank computation; the window version is the engine-optimized equivalent.

## Q36: Find the third-highest salary per department using the same LIMIT/OFFSET pattern.

**Query:**
```sql
SELECT e1.name, e1.dept_id, e1.salary
  FROM employees e1
 WHERE e1.salary = (SELECT DISTINCT e2.salary
                      FROM employees e2
                     WHERE e2.dept_id = e1.dept_id
                     ORDER BY e2.salary DESC
                     LIMIT 1 OFFSET 2);
```
**Explanation:** Same correlated ORDER BY ... OFFSET idiom; departments with fewer than three distinct salaries simply match nothing.

## Q37: Rewrite the correlated COUNT of Q3 as a JOIN + GROUP BY and comment on the tradeoff.

**Query:**
```sql
SELECT c.id, c.name, COUNT(o.id) AS order_count
  FROM customers c
  LEFT JOIN orders o ON o.customer_id = c.id
 GROUP BY c.id, c.name;
```
**Explanation:** One scan plus a hash join replaces n lookups; the LEFT JOIN preserves customers with zero orders (their COUNT is 0).

**Alt1:** The original correlated version for reference:
```sql
SELECT c.id, c.name,
       (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) AS order_count
  FROM customers c;
```
**Note:** Use the JOIN when orders is wide (it aggregates once in one pass); keep the correlated form when the driving table is small and orders(customer_id) is indexed.

## Q38: Rewrite the NOT EXISTS anti-join of Q12 using LEFT JOIN ... IS NULL.

**Query:**
```sql
SELECT c.name
  FROM customers c
  LEFT JOIN orders o ON o.customer_id = c.id
 WHERE o.id IS NULL;
```
**Explanation:** Every customer is kept; only those with no matching order row survive the NULL probe on orders.id.

**Alt1:** The NOT EXISTS original:
```sql
SELECT c.name
  FROM customers c
 WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```
**Note:** Both are anti-joins; NULL probes in the join column are irrelevant here because NULL order ids can never join, so results agree.

## Q39: Rewrite the EXISTS query of Q8 as a JOIN + DISTINCT and explain what changes (duplicates).

**Query:**
```sql
SELECT DISTINCT d.name
  FROM departments d
  JOIN employees e ON e.dept_id = d.id
 WHERE e.salary > 100000;
```
**Explanation:** The JOIN can emit a department once per qualifying employee; DISTINCT collapses the fan-out back to the EXISTS result.

**Alt1:** The plain EXISTS form:
```sql
SELECT d.name
  FROM departments d
 WHERE EXISTS (SELECT 1 FROM employees e
                WHERE e.dept_id = d.id AND e.salary > 100000);
```
**Note:** Same results; EXISTS stops early like a semi-join, the JOIN must materialize the product first — for big inner tables the semi-join plan usually reads fewer rows.

## Q40: Give an example where a correlated subquery is the most practical option: a per-row LIMIT 1 fetch.

**Query:**
```sql
SELECT e.name,
       (SELECT o.order_date
          FROM orders o
         WHERE o.customer_id = e.customer_id
         ORDER BY o.order_date DESC, o.id DESC
         LIMIT 1) AS latest_order_date
  FROM employees e;
```
**Explanation:** No plain JOIN reproduces "the newest row per grouping key" without either a window or a second correlation; LIMIT-1 correlated subqueries fit naturally.

**Alt1:** PostgreSQL LATERAL expresses the same intent with a named alias:
```sql
SELECT e.name, latest.order_date
  FROM employees e
  CROSS JOIN LATERAL (SELECT o.order_date
                        FROM orders o
                       WHERE o.customer_id = e.customer_id
                       ORDER BY o.order_date DESC, o.id DESC
                       LIMIT 1) latest;
```
**Note:** LATERAL is the relational spelling of the correlated LIMIT-1 and is easier to debug and extend.

## Q41: Show the structural difference between a correlated and a non-correlated subquery.

**Query:**
```sql
-- Correlated: inner WHERE references the outer alias
SELECT e.name,
       (SELECT MAX(e2.salary)
          FROM employees e2
         WHERE e2.dept_id = e.dept_id) AS dept_max
  FROM employees e;

-- Non-correlated: inner query is standalone, computed once
SELECT e.name,
       (SELECT MAX(salary) FROM employees) AS company_max
  FROM employees e;
```
**Explanation:** The first re-executes per outer row; the second is a constant scalar evaluated a single time regardless of row count.

## Q42: Demonstrate that a correlated subquery is evaluated once per outer row with a traceable example.

**Query:**
```sql
-- employees(id,name,salary); this query logs one subquery execution per outer row
SELECT e.id,
       e.name,
       (SELECT COUNT(*) FROM employees e2 WHERE e2.salary < e.salary) AS cheaper_colleagues
  FROM employees e
 ORDER BY e.salary;
```
**Explanation:** For three employees the inner query fires three times; instrumented engines (EXPLAIN ANALYZE) show an index scan per probe — the origin of the "N+1" cost model.

## Q43: Use COALESCE around a correlated scalar subquery that may return NULL for rows with no matches.

**Query:**
```sql
SELECT c.name,
       COALESCE((SELECT SUM(o.amount)
                   FROM orders o
                  WHERE o.customer_id = c.id), 0) AS total_spent
  FROM customers c;
```
**Explanation:** Customers with zero orders yield NULL from the empty correlated aggregate; COALESCE normalizes it to 0 for reporting.

## Q44: Find employees who earn less than at least one other employee in the same department (ANY comparative).

**Query:**
```sql
SELECT e1.name, e1.salary
  FROM employees e1
 WHERE e1.salary < ANY (SELECT e2.salary
                          FROM employees e2
                         WHERE e2.dept_id = e1.dept_id
                           AND e2.id <> e1.id);
```
**Explanation:** ANY is satisfied as soon as one peer earns more — a correlated existence test over a value list.

**Alt1:** EXISTS makes the intent (existence) explicit:
```sql
SELECT e1.name, e1.salary
  FROM employees e1
 WHERE EXISTS (SELECT 1
                 FROM employees e2
                WHERE e2.dept_id = e1.dept_id
                  AND e2.id <> e1.id
                  AND e2.salary > e1.salary);
```
**Note:** Semantically identical; EXISTS short-circuits on the first hit and is the form most optimizers handle best.

## Q45: Find customers whose latest order amount is greater than their own average order amount.

**Query:**
```sql
SELECT c.id, c.name
  FROM customers c
 WHERE (SELECT o.amount
          FROM orders o
         WHERE o.customer_id = c.id
         ORDER BY o.order_date DESC, o.id DESC
         LIMIT 1)
       >
       (SELECT AVG(o2.amount)
          FROM orders o2
         WHERE o2.customer_id = c.id);
```
**Explanation:** Two correlated subqueries — one returns the latest order's amount, the other the customer's average — compared in the outer WHERE.

**Alt1:** ROW_NUMBER + window AVG expresses the comparison in one scan:
```sql
SELECT customer_id
  FROM (SELECT customer_id, amount, AVG(amount) OVER (PARTITION BY customer_id) avg_o,
               ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, id DESC) rn
          FROM orders) t
 WHERE rn = 1 AND amount > avg_o;
```
**Note:** The window alternative scans the base table once instead of nesting the orders read twice per customer.

## Q46: Using a doubly-correlated NOT EXISTS, return the name of the highest-paid employee in each department.

**Query:**
```sql
SELECT e.name, e.dept_id, e.salary
  FROM employees e
 WHERE NOT EXISTS (SELECT 1
                     FROM employees e2
                    WHERE e2.dept_id = e.dept_id
                      AND e2.salary > e.salary);
```
**Explanation:** The inner query correlates back to the outer row (e.dept_id, e.salary): an employee survives only when no one in their department is paid more — a "top of group" anti-join.

## Q47: Write a SELECT with a correlated subquery that references a column from a table joined in the outer query.

**Query:**
```sql
SELECT e.name, d.name AS dept,
       (SELECT COUNT(*)
          FROM projects p
         WHERE p.dept_id = d.id) AS dept_project_count
  FROM employees e
  JOIN departments d ON d.id = e.dept_id;
```
**Explanation:** The correlation binds to the joined alias d, not the driving table — the subquery is per-department even though the outer query iterates per employee.

## Q48: Update each employee's bonus to 10 percent of their department's average salary using a correlated UPDATE.

**Query:**
```sql
UPDATE employees e
   SET e.bonus = ROUND(0.10 * (SELECT AVG(e2.salary)
                                 FROM employees e2
                                WHERE e2.dept_id = e.dept_id));
```
**Explanation:** In an UPDATE, the correlation reads the target row's dept_id; the derived average is what is written back to bonus.

## Q49: Delete all duplicate login rows, keeping only the latest login per user, using a correlated subquery.

**Query:**
```sql
DELETE FROM logins l
 WHERE l.logged_in_at < (SELECT MAX(l2.logged_in_at)
                           FROM logins l2
                          WHERE l2.user_id = l.user_id);
```
**Explanation:** Any row that is not the max timestamp for its user is a duplicate and is removed; the newest per user survives. (T-SQL/SQLite forbid touching the same table in-line — denormalize to a temp/derived table there.)

**Alt1:** SQL Server 2008+: use a deletable CTE:
```sql
;WITH tracked AS (
   SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY logged_in_at DESC) rn
     FROM logins)
DELETE FROM tracked WHERE rn > 1;
```
**Note:** The window version is portable across the major engines and single-scan; the correlated DELETE is the ANSI-only fallback.

## Q50: Write a CASE expression that buckets each employee's salary relative to their department's average using a correlated subquery.

**Query:**
```sql
SELECT e.name, e.salary,
       CASE
         WHEN e.salary > (SELECT AVG(e2.salary)
                            FROM employees e2
                           WHERE e2.dept_id = e.dept_id) THEN 'ABOVE'
         WHEN e.salary < (SELECT AVG(e2.salary)
                            FROM employees e2
                           WHERE e2.dept_id = e.dept_id) THEN 'BELOW'
         ELSE 'AT'
       END AS dept_band
  FROM employees e;
```
**Explanation:** The correlated AVG appears inside a searched CASE; the subquery repeats per row unless the planner memoizes it — compute it once via a derived table when the driving table is large.
## Q51: Find the top 3 products per category WITHOUT window functions, using a correlated COUNT.

**Query:**
```sql
SELECT p.name, p.category_id, p.price
  FROM products p
 WHERE (SELECT COUNT(*)
          FROM products p2
         WHERE p2.category_id = p.category_id
           AND p2.price > p.price) < 3;
```
**Explanation:** A product is in the top 3 when fewer than 3 same-category products are strictly pricier — ties all qualify because the count goes against the outer product.

**Alt1:** ROW_NUMBER over a partition gives an unambiguous top-N when ties must be broken:
```sql
SELECT name, category_id, price
  FROM (SELECT p.*, ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY price DESC) rn
          FROM products p) t
 WHERE rn <= 3;
```
**Note:** The correlated count is O(n^2) in the worst case; the window scan is linear.

## Q52: Rank products inside each category (1 = most expensive) using a correlated COUNT of higher-priced items.

**Query:**
```sql
SELECT p.name, p.category_id, p.price,
       1 + (SELECT COUNT(*)
              FROM products p2
             WHERE p2.category_id = p.category_id
               AND p2.price > p.price) AS price_rank
  FROM products p;
```
**Explanation:** COUNT of strictly higher prices plus one ranks each product within its category; equal prices share a rank (fragmented).

**Alt1:** RANK() reproduces the same shared-rank behavior in one scan:
```sql
SELECT p.name, p.category_id, p.price,
       RANK() OVER (PARTITION BY category_id ORDER BY price DESC) AS price_rank
  FROM products p;
```
**Note:** Both give 1,2,2,4 on ties; RANK is the engine-optimized version the correlated COUNT is teaching you to reason about.

## Q53: Find customers whose total spend exceeds the average total spend across all customers.

**Query:**
```sql
SELECT c.name
  FROM customers c
 WHERE (SELECT SUM(o.amount)
          FROM orders o
         WHERE o.customer_id = c.id) >
       (SELECT AVG(total)
          FROM (SELECT customer_id, SUM(amount) AS total
                  FROM orders
                 GROUP BY customer_id) t);
```
**Explanation:** Correlated per-customer SUM is compared against a derived-table scalar (average of per-customer totals) — a row-vs-population comparison.

## Q54: Find employees whose salary is at or above the median salary of their own department (PostgreSQL; note MySQL limits).

**Query:**
```sql
-- PostgreSQL
SELECT e.name, e.salary
  FROM employees e
 WHERE e.salary >= (SELECT e2.salary
                      FROM employees e2
                     WHERE e2.dept_id = e.dept_id
                     ORDER BY e2.salary
                     LIMIT 1 OFFSET (SELECT COUNT(*) / 2
                                       FROM employees e3
                                      WHERE e3.dept_id = e.dept_id));
```
**Explanation:** A correlated OFFSET computed from a second correlated COUNT selects the middle salary value per department. MySQL requires a constant OFFSET, so precompute the count in a derived table there.

## Q55: Show each employee's salary as a percentage of their department's maximum salary.

**Query:**
```sql
SELECT e.name, e.salary,
       ROUND(100.0 * e.salary /
             (SELECT MAX(e2.salary)
                FROM employees e2
               WHERE e2.dept_id = e.dept_id), 1) AS pct_of_dept_max
  FROM employees e;
```
**Explanation:** Correlated MAX in the denominator; a NULL would overflow the ratio, so COALESCE it when departments can be empty.

**Alt1:** MAX() as a window gives the same ratio in a single table scan:
```sql
SELECT e.name, e.salary,
       ROUND(100.0 * e.salary / MAX(e.salary) OVER (PARTITION BY dept_id), 1) AS pct_of_dept_max
  FROM employees e;
```
**Note:** Identical numbers; the window version is the production answer at scale, the correlated form is the interview-grade "show you understand correlation" answer.

## Q56: Find employees who are the only person in their department with their exact salary.

**Query:**
```sql
SELECT e.name, e.salary, e.dept_id
  FROM employees e
 WHERE (SELECT COUNT(*)
          FROM employees e2
         WHERE e2.dept_id = e.dept_id
           AND e2.salary = e.salary) = 1;
```
**Explanation:** Correlated COUNT over same-department same-salary peers; exactly one match (the outer row itself) proves uniqueness.

## Q57: List managers who earn less than at least one of their direct reports.

**Query:**
```sql
SELECT m.name, m.salary
  FROM employees m
 WHERE EXISTS (SELECT 1
                 FROM employees sub
                WHERE sub.manager_id = m.id
                  AND sub.salary > m.salary);
```
**Explanation:** The EXISTS subquery correlates the manager alias m with subordinate rows; it is true as soon as any report outearns the manager.

## Q58: Find orders that are the single largest order for their customer.

**Query:**
```sql
SELECT o.id, o.customer_id, o.amount
  FROM orders o
 WHERE o.amount = (SELECT MAX(o2.amount)
                     FROM orders o2
                    WHERE o2.customer_id = o.customer_id);
```
**Explanation:** Equality against the per-customer max; tied largest orders all qualify.

**Alt1:** Windowing the maximum keeps the rows without a self-scan:
```sql
SELECT id, customer_id, amount
  FROM (SELECT o.*, MAX(amount) OVER (PARTITION BY customer_id) mx
          FROM orders o) t
 WHERE amount = mx;
```
**Note:** The MAX window computes over the whole partition in one pass; the correlated version probes once per order row.

## Q59: Find orders that are larger than EVERY earlier order placed by the same customer (running maximum via inequality correlation).

**Query:**
```sql
SELECT o.id, o.customer_id, o.order_date, o.amount
  FROM orders o
 WHERE o.amount > ALL (SELECT o2.amount
                         FROM orders o2
                        WHERE o2.customer_id = o.customer_id
                          AND o2.order_date < o.order_date);
```
**Explanation:** The correlated subquery returns every earlier amount; `> ALL` holds only when the current order beats them all — a strict running-max filter. The first order passes vacuously (empty list).

## Q60: Flag employees whose salary exceeds twice their department's average, using a correlated CASE in the SELECT list.

**Query:**
```sql
SELECT e.name, e.salary,
       CASE
         WHEN e.salary > 2 * (SELECT AVG(e2.salary)
                                FROM employees e2
                               WHERE e2.dept_id = e.dept_id)
              THEN 'YES'
         ELSE 'no'
       END AS over_2x_dept_avg
  FROM employees e;
```
**Explanation:** The correlated AVG feeds a boolean in the SELECT list — aggregates embedded in expressions of the outer projection are a staple of "per-row attribute from related rows".

## Q61: Detect customer emails that appear more than once in the customers table.

**Query:**
```sql
SELECT c.id, c.email
  FROM customers c
 WHERE (SELECT COUNT(*)
          FROM customers c2
         WHERE c2.email = c.email) > 1;
```
**Explanation:** Correlated COUNT over the duplicate key; every row of a repeated email group is flagged.

**Alt1:** GROUP BY + HAVING is the far cheaper duplicate detector:
```sql
SELECT email, COUNT(*) AS cnt
  FROM customers
 GROUP BY email
HAVING COUNT(*) > 1;
```
**Note:** The correlated form is O(n^2) and returns every dup row; the grouped form is one scan and one row per duplicate key — complete rewrite when the table is large.

## Q62: Return the newest-hired employee of each department, INCLUDING departments with no employees.

**Query:**
```sql
SELECT d.name,
       (SELECT e.name
          FROM employees e
         WHERE e.dept_id = d.id
         ORDER BY e.hire_date DESC, e.id DESC
         LIMIT 1) AS newest_hire
  FROM departments d;
```
**Explanation:** Driving the correlation from the dimension table means empty departments still surface as rows with a NULL newest_hire — an outer-pyramid query.

## Q63: Compute a 3-order moving average of spending per customer WITHOUT window functions.

**Query:**
```sql
-- MySQL / PostgreSQL
SELECT o.id, o.customer_id, o.order_date,
       (SELECT AVG(o2.amount)
          FROM (SELECT o3.amount
                  FROM orders o3
                 WHERE o3.customer_id = o.customer_id
                   AND o3.order_date <= o.order_date
                 ORDER BY o3.order_date DESC, o3.id DESC
                 LIMIT 3) o2) AS moving_avg_3
  FROM orders o;
```
**Explanation:** The inner derived table fetches the three most recent (same customer, same-or-earlier date) amounts; the correlated wrapper averages them per row.

**Alt1:** AVG as a window over a preceding frame is the canonical production form:
```sql
SELECT o.id, o.customer_id, o.order_date, o.amount,
       AVG(o.amount) OVER (PARTITION BY customer_id
                           ORDER BY order_date, id
                           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_3
  FROM orders o;
```
**Note:** The correlated version re-queries a 3-row bucket per outer row; the window frame slides across a single sorted scan.

## Q64: Compute the running (cumulative) total of transactions per account WITHOUT window functions.

**Query:**
```sql
SELECT t.id, t.account_id, t.amount,
       (SELECT SUM(t2.amount)
          FROM transactions t2
         WHERE t2.account_id = t.account_id
           AND t2.tx_time <= t.tx_time) AS running_total
  FROM transactions t;
```
**Explanation:** Inequality correlation (`<=` on the ordering key) accumulates every prior-or-equal transaction per account — a hand-rolled running total.

**Alt1:** SUM as a window frame achieves the same numbers in one pass:
```sql
SELECT t.id, t.account_id, t.amount,
       SUM(t.amount) OVER (PARTITION BY account_id ORDER BY tx_time, id) AS running_total
  FROM transactions t;
```
**Note:** The correlated cumulative sum is O(n^2); the window is the scalable rewrite you would ship.

## Q65: Number each customer's orders chronologically (1 = first) using a correlated COUNT.

**Query:**
```sql
SELECT o.id, o.customer_id, o.order_date,
       1 + (SELECT COUNT(*)
              FROM orders o2
             WHERE o2.customer_id = o.customer_id
               AND o2.order_date < o.order_date) AS order_seq
  FROM orders o;
```
**Explanation:** Counting strictly-earlier orders plus one yields each order's chronological position; ties share a sequence number, unlike ROW_NUMBER.

## Q66: Find customers who had a gap of more than 60 days between two consecutive orders.

**Query:**
```sql
SELECT DISTINCT o.customer_id
  FROM orders o
 WHERE EXISTS (
   SELECT 1
     FROM orders o2
    WHERE o2.customer_id = o.customer_id
      AND o2.order_date > o.order_date
      AND (o2.order_date - o.order_date) > INTERVAL 60 DAY
      AND NOT EXISTS (
          SELECT 1 FROM orders o3
           WHERE o3.customer_id = o.customer_id
             AND o3.order_date > o.order_date
             AND o3.order_date < o2.order_date));
```
**Explanation:** EXISTS finds a later order more than 60 days out that has no order strictly between them; the doubly-correlated NOT EXISTS guarantees the pair is consecutive.

**Alt1:** LAG-based diff makes consecutiveness explicit and indexes well:
```sql
WITH tagged AS (
  SELECT customer_id, order_date,
         LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) prev
    FROM orders)
SELECT DISTINCT customer_id FROM tagged
 WHERE order_date - prev > INTERVAL 60 DAY;
```
**Note:** The correlated double-negative is correct but expensive; the LAG rewrite computes the same jumps in one ordered scan.

## Q67: Find customers whose most recent order was more than 90 days ago (correlated MAX).

**Query:**
```sql
SELECT c.name
  FROM customers c
 WHERE (SELECT MAX(o.order_date)
          FROM orders o
         WHERE o.customer_id = c.id) < CURRENT_DATE - INTERVAL 90 DAY;
```
**Explanation:** The correlated MAX yields the customer's last purchase; the outer predicate churns that value — customers with no orders at all are excluded by the NULL comparison.

## Q68: For each order, show how its amount compares with the customer's very first order amount.

**Query:**
```sql
SELECT o.id, o.customer_id, o.amount,
       (SELECT o2.amount
          FROM orders o2
         WHERE o2.customer_id = o.customer_id
         ORDER BY o2.order_date, o2.id
         LIMIT 1) AS first_order_amount
  FROM orders o;
```
**Explanation:** ORDER BY ... LIMIT 1 inside the correlated subquery pins the customer's earliest order; the first order equals itself.

**Alt1:** Replacing the LIMIT with a correlated MIN-of-date join reads clearer to some teams:
```sql
SELECT o.id, o.customer_id, o.amount,
       first.amount AS first_order_amount
  FROM orders o
  JOIN (SELECT customer_id, MIN(order_date) AS d
          FROM orders
         GROUP BY customer_id) f
    ON f.customer_id = o.customer_id
  JOIN orders first ON first.customer_id = f.customer_id
                   AND first.order_date = f.d;
```
**Note:** The LIMIT-1 corner is cheaper (no dedupe join); the join chain gets unwieldy when first dates tie.

## Q69: For each store, find the nearest store that opened at least a year earlier.

**Query:**
```sql
SELECT s1.name,
       (SELECT s2.name
          FROM stores s2
         WHERE s2.id <> s1.id
           AND s2.opened_at <= s1.opened_at - INTERVAL 1 YEAR
         ORDER BY ABS(s1.x - s2.x) + ABS(s1.y - s2.y), s2.name
         LIMIT 1) AS nearest_older_store
  FROM stores s1;
```
**Explanation:** Nearest-neighbor combined with an inequality correlation on the business key — the ORDER BY and the `<=` filter run against the same correlated candidate set.

## Q70: For every login, show the user's previous login timestamp.

**Query:**
```sql
SELECT l.user_id, l.logged_in_at,
       (SELECT MAX(l2.logged_in_at)
          FROM logins l2
         WHERE l2.user_id = l.user_id
           AND l2.logged_in_at < l.logged_in_at) AS prev_login
  FROM logins l;
```
**Explanation:** Classic previous-row correlation: MAX over a strict `<` of the ordering key per partition key.

## Q71: Identify users who made a second purchase within 7 days of their first purchase.

**Query:**
```sql
SELECT DISTINCT c.id, c.name
  FROM customers c
 WHERE EXISTS (
   SELECT 1
     FROM orders first
     JOIN orders second ON second.customer_id = first.customer_id
    WHERE first.customer_id = c.id
      AND second.id <> first.id
      AND second.order_date BETWEEN first.order_date
                               AND first.order_date + INTERVAL 7 DAY);
```
**Explanation:** The EXISTS subquery correlates on c.id and treats the pair of orders as first-vs-second; any qualifying repeat purchase proves retention.

## Q72: Return the second-order date for each customer using a correlated LIMIT ... OFFSET.

**Query:**
```sql
SELECT DISTINCT o.customer_id,
       (SELECT o2.order_date
          FROM orders o2
         WHERE o2.customer_id = o.customer_id
         ORDER BY o2.order_date, o2.id
         LIMIT 1 OFFSET 1) AS second_order_date
  FROM orders o;
```
**Explanation:** Offset 1 skips the earliest order, so the correlated fetch is the second one; customers with a single order return NULL.

## Q73: Write a correlated subquery that matches on TWO outer columns: the nearest city within the same region.

**Query:**
```sql
SELECT c1.name, c1.region,
       (SELECT c2.name
          FROM cities c2
         WHERE c2.region = c1.region
           AND c2.id <> c1.id
         ORDER BY ABS(c1.x - c2.x) + ABS(c1.y - c2.y), c2.name
         LIMIT 1) AS nearest_in_region
  FROM cities c1;
```
**Explanation:** Multi-column correlation — both region equality and the distance ordering consume outer values, so the inner result set is scoped by region before ranking.

## Q74: Find employees whose salary is unlike every colleague in their department (no one else earns the same amount).

**Query:**
```sql
SELECT e.name, e.salary, e.dept_id
  FROM employees e
 WHERE NOT EXISTS (SELECT 1
                     FROM employees e2
                    WHERE e2.dept_id = e.dept_id
                      AND e2.salary = e.salary
                      AND e2.id <> e.id);
```
**Explanation:** The anti-join checks same-department, same-salary peers other than the outer row; surviving employees are unique earners.

## Q75: Rewrite a correlated salary-vs-department-average query using a CTE, and state when the rewrite is equivalent.

**Query:**
```sql
WITH dept_avg AS (
  SELECT dept_id, AVG(salary) AS avg_sal
    FROM employees
   GROUP BY dept_id)
SELECT e.name, e.salary, d.avg_sal
  FROM employees e
  JOIN dept_avg d ON d.dept_id = e.dept_id
 WHERE e.salary > d.avg_sal;
```
**Explanation:** The CTE computes each department's average exactly once and the join reproduces the correlated comparison row by row — equivalent because the correlated term depends only on dept_id.

**Alt1:** The correlated original:
```sql
SELECT e.name, e.salary
  FROM employees e
 WHERE e.salary > (SELECT AVG(e2.salary)
                     FROM employees e2
                    WHERE e2.dept_id = e.dept_id);
```
**Note:** The rewrite is guaranteed equivalent when the subquery's only outer dependency is the equi-matded grouping key; if it also used LIMIT/inequality, the JOIN version usually cannot replicate it — that is when the correlated form is truly needed.
## Q76: Show the classic performance caveat of correlated subqueries and provide the JOIN rewrite — the "N+1" problem.

**Query:**
```sql
-- Slow on big tables: one probe per outer row (N+1 pattern)
SELECT c.name,
       (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) AS order_count
  FROM customers c;

-- Fast: one scan + one aggregation
SELECT c.name, COUNT(o.id) AS order_count
  FROM customers c
  LEFT JOIN orders o ON o.customer_id = c.id
 GROUP BY c.id, c.name;
```
**Explanation:** The correlated version costs N lookups, each of which must resolve orders(customer_id); the JOIN+GROUP BY collapses that to one pass over orders and is the standard remediation.

## Q77: Rewrite a correlated scalar to a derived table + self-JOIN and show both forms.

**Query:**
```sql
-- Correlated: dept max next to each employee
SELECT e.name, e.salary,
       (SELECT MAX(e2.salary) FROM employees e2
         WHERE e2.dept_id = e.dept_id) AS dept_max
  FROM employees e;

-- Rewritten: precomputed dept max joined back
SELECT e.name, e.salary, m.dept_max
  FROM employees e
  JOIN (SELECT dept_id, MAX(salary) AS dept_max
          FROM employees
         GROUP BY dept_id) m
    ON m.dept_id = e.dept_id;
```
**Explanation:** Both list each employee with their department maximum; the derived table is scanned once and hash-joined, so the rewrite scales where the correlated version would do n index probes.

## Q78: Explain how an index changes correlated-subquery performance, with an indexed LIMIT-1 "latest per group" query.

**Query:**
```sql
-- With an index on (customer_id, order_date DESC, id DESC) this becomes an index-order scan fetch
SELECT o.*
  FROM orders o
 WHERE o.id = (SELECT o2.id
                 FROM orders o2
                WHERE o2.customer_id = o.customer_id
                ORDER BY o2.order_date DESC, o2.id DESC
                LIMIT 1);
```
**Explanation:** A B-tree on (customer_id, order_date) lets each correlated probe walk straight to the newest row instead of scanning the bucket; index design, not SQL shape, often decides whether the correlated form is tolerable.

**Alt1:** PostgreSQL LATERAL lets the same idea reuse the index and stay readable:
```sql
SELECT o.*
  FROM customers c
  CROSS JOIN LATERAL (SELECT o2.*
                        FROM orders o2
                       WHERE o2.customer_id = c.id
                       ORDER BY o2.order_date DESC, o2.id DESC
                       LIMIT 1) o;
```
**Note:** LATERAL is the same correlated execution but names the driving row explicitly and composes with other joins.

## Q79: Contrast NOT EXISTS with NOT IN for the anti-join, with the NULL gotcha, and give the safe rewrite.

**Query:**
```sql
-- WRONG if orders.customer_id can contain NULL: NOT IN returns no rows at all
SELECT c.name FROM customers c
 WHERE c.id NOT IN (SELECT customer_id FROM orders);

-- Correct: NOT EXISTS has no NULL trap
SELECT c.name FROM customers c
 WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```
**Explanation:** NOT IN reduces to `val = NULL` comparisons which are UNKNOWN and filter everything out; NOT EXISTS evaluates presence per row and is immune.

**Alt1:** Explicitly closing the NULL hole keeps NOT IN but pins the semantics:
```sql
SELECT c.name FROM customers c
 WHERE c.id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL);
```
**Note:** Still correct after the guard, but NOT EXISTS remains the canonical anti-join — it is what the optimizer can turn into an anti semi-join.

## Q80: Distinguish equality-correlated from inequality-correlated subqueries by purpose.

**Query:**
```sql
-- Equality correlation: per-group aggregate or existence (matches group key exactly)
SELECT e.name,
       (SELECT AVG(e2.salary) FROM employees e2
         WHERE e2.dept_id = e.dept_id) AS dept_avg
  FROM employees e;

-- Inequality correlation: previous/next row, running totals, nearest neighbor (orders the key)
SELECT t.id,
       (SELECT MAX(t2.amount) FROM transactions t2
         WHERE t2.account_id = t.account_id
           AND t2.tx_time < t.tx_time) AS prev_amount
  FROM transactions t;
```
**Explanation:** `=`-correlation answers "what is true of my group"; `<`/`>`-correlation answers "what happened before/after or closest to me" and is how self-join-like behavior is expressed without window functions.

## Q81: Compute a year-to-date running total per salesperson using double inequality correlation.

**Query:**
```sql
-- PostgreSQL / MySQL both support EXTRACT in this shape
SELECT s.employee_id, s.sale_date, s.amount,
       (SELECT SUM(s2.amount)
          FROM sales s2
         WHERE s2.employee_id = s.employee_id
           AND EXTRACT(YEAR FROM s2.sale_date) = EXTRACT(YEAR FROM s.sale_date)
           AND s2.sale_date <= s.sale_date) AS ytd_total
  FROM sales s;
```
**Explanation:** Two correlated predicates — same year (equality on the derived year) and at-or-before the current row (inequality on the date) — accumulate the running YTD per seller.

## Q82: Compute month-over-month spend growth per customer using a correlated lookup of the prior month.

**Query:**
```sql
-- PostgreSQL (DATE_TRUNC); MySQL uses DATE_FORMAT + DATE_SUB
SELECT m.customer_id,
       m.month,
       m.monthly,
       (SELECT SUM(o.amount)
          FROM orders o
         WHERE o.customer_id = m.customer_id
           AND o.order_date >= m.month - INTERVAL 1 MONTH
           AND o.order_date <  m.month) AS prev_month_total
  FROM (SELECT customer_id,
               DATE_TRUNC('month', order_date) AS month,
               SUM(amount) AS monthly
          FROM orders
         GROUP BY customer_id, DATE_TRUNC('month', order_date)) m;
```
**Explanation:** The outer query aggregates by month; the correlated subquery re-reads orders for that customer one month earlier, yielding a per-customer MoM pair.

**Alt1:** LAG on the aggregated set avoids the second scan of orders:
```sql
WITH monthly AS (
  SELECT customer_id, DATE_TRUNC('month', order_date) AS month, SUM(amount) AS monthly
    FROM orders
   GROUP BY customer_id, DATE_TRUNC('month', order_date))
SELECT *, LAG(monthly) OVER (PARTITION BY customer_id ORDER BY month) AS prev_month_total
  FROM monthly;
```
**Note:** The window rewrite scans the monthly summary instead of the raw orders once per aggregate row; the correlated version is the classic fallback when LAG is unavailable.

## Q83: Compare the equality-correlated (MAX) and ORDER BY-LIMIT forms for "latest hire per department" and state the tie behavior.

**Query:**
```sql
-- Equality form: all employees tied on the max date are kept
SELECT e.name, e.dept_id, e.hire_date
  FROM employees e
 WHERE e.hire_date = (SELECT MAX(e2.hire_date)
                        FROM employees e2
                       WHERE e2.dept_id = e.dept_id);

-- LIMIT 1 form: exactly one row per department (deterministic with id tiebreak)
SELECT e.name, e.dept_id, e.hire_date
  FROM employees e
 WHERE e.id = (SELECT e2.id
                 FROM employees e2
                WHERE e2.dept_id = e.dept_id
                ORDER BY e2.hire_date DESC, e2.id DESC
                LIMIT 1);
```
**Explanation:** MAX preserves ties (two co-newest hires both appear); the LIMIT-1 variant forces a single representative per group — pick deliberately based on whether ties are meaningful.

## Q84: Return each product with its category name AND a correlated COUNT of pricier products in that same category (two correlated subqueries).

**Query:**
```sql
SELECT p.name,
       (SELECT c.name FROM categories c WHERE c.id = p.category_id) AS category,
       (SELECT COUNT(*) FROM products p2
         WHERE p2.category_id = p.category_id
           AND p2.price > p.price) AS pricier_count
  FROM products p;
```
**Explanation:** Two independent correlated subqueries serve two different purposes — a lookup (category name) and an aggregate (count of competitors) — both reevaluated per product row.

## Q85: For each booking, count overlapping bookings of the same room using a range-interval correlation (bookings: id, room_id, start_at, end_at).

**Query:**
```sql
SELECT b1.id, b1.room_id, b1.start_at, b1.end_at,
       (SELECT COUNT(*)
          FROM bookings b2
         WHERE b2.room_id = b1.room_id
           AND b2.id <> b1.id
           AND b2.start_at < b1.end_at
           AND b2.end_at   > b1.start_at) AS overlapping
  FROM bookings b1;
```
**Explanation:** Two back-to-back inequality predicates implement interval overlap (`starts before I end, ends after I start`), correlated per room — a range anti-self-join without window assistance.

## Q86: Write a correlated HAVING that checks students' per-year average grade against their own overall average.

**Query:**
```sql
SELECT s.student_id, EXTRACT(YEAR FROM s.enrolled_on) AS yr, AVG(s.grade) AS yr_avg
  FROM students s
 GROUP BY s.student_id, EXTRACT(YEAR FROM s.enrolled_on)
HAVING AVG(s.grade) > (SELECT AVG(s2.grade)
                         FROM students s2
                        WHERE s2.student_id = s.student_id);
```
**Explanation:** The HAVING subquery reads the outer group's student_id and compares the year group average with the student's lifetime average — correlation applied at the group-filter level.

## Q87: Find customers who placed no order in 2020 but at least one order in 2021.

**Query:**
```sql
SELECT c.name
  FROM customers c
 WHERE NOT EXISTS (SELECT 1 FROM orders o
                    WHERE o.customer_id = c.id
                      AND o.order_date BETWEEN '2020-01-01' AND '2020-12-31')
   AND EXISTS     (SELECT 1 FROM orders o
                    WHERE o.customer_id = c.id
                      AND o.order_date BETWEEN '2021-01-01' AND '2021-12-31');
```
**Explanation:** An anti-join and a semi-join on the same correlation column; the AND combines "never in 2020" with "active in 2021" for a re-engagement cohort.

## Q88: List products whose current stock is below their own average monthly sales volume (correlated over a derived monthly aggregate).

**Query:**
```sql
-- MySQL (YEAR/MONTH)
SELECT p.name, p.stock_qty
  FROM products p
 WHERE p.stock_qty < (SELECT AVG(m.monthly)
                        FROM (SELECT YEAR(o.order_date) AS yy,
                                     MONTH(o.order_date) AS mm,
                                     SUM(oi.quantity) AS monthly
                                FROM orders o
                                JOIN order_items oi ON oi.order_id = o.id
                               WHERE oi.product_id = p.id
                               GROUP BY YEAR(o.order_date), MONTH(o.order_date)) m);
```
**Explanation:** The correlated inner derived table aggregates sales by month for the current product; the outer row compares its stock against that average — a reorder-alert.

## Q89: Show each employee together with the number of employees in their department (department size).

**Query:**
```sql
SELECT e.name,
       e.dept_id,
       (SELECT COUNT(*) FROM employees e2
         WHERE e2.dept_id = e.dept_id) AS dept_size
  FROM employees e;
```
**Explanation:** A correlated COUNT in the projection — same value repeated for each member of a department, identical to what a window COUNT(PARTITION BY dept_id) produces.

**Alt1:** Idiomatic join form for the same size value:
```sql
SELECT e.name, e.dept_id, agg.dept_size
  FROM employees e
  JOIN (SELECT dept_id, COUNT(*) AS dept_size
          FROM employees
         GROUP BY dept_id) agg
    ON agg.dept_id = e.dept_id;
```
**Note:** Both print the identical dept_size; the grouped join is the scalable rewrite, the correlated form is the "show correlation" interview answer.

## Q90: Find the earliest-hired employee per (department, role) pair using two-column correlation.

**Query:**
```sql
SELECT e.name, e.dept_id, e.role, e.hire_date
  FROM employees e
 WHERE e.hire_date = (SELECT MIN(e2.hire_date)
                        FROM employees e2
                       WHERE e2.dept_id = e.dept_id
                         AND e2.role    = e.role);
```
**Explanation:** The correlation key is the pair (dept_id, role), so the MIN is scoped by both columns — per-segment earliest hire.

## Q91: For each stop, find the nearest other stop on the same route using Euclidean distance (2-D nearest neighbor per group).

**Query:**
```sql
SELECT r1.id, r1.route_id,
       (SELECT r2.id
          FROM rest_stops r2
         WHERE r2.route_id = r1.route_id
           AND r2.id <> r1.id
         ORDER BY SQRT(POWER(r1.x - r2.x, 2) + POWER(r1.y - r2.y, 2)), r2.id
         LIMIT 1) AS nearest_stop
  FROM rest_stops r1;
```
**Explanation:** The correlated ORDER BY computes the distance inside the subquery per candidate row, so the LIMIT 1 grabs the closest stop within the same route group.

## Q92: Rank employees within each department by salary using a correlated COUNT (fragmented ranks).

**Query:**
```sql
SELECT e.name, e.dept_id, e.salary,
       1 + (SELECT COUNT(*)
              FROM employees e2
             WHERE e2.dept_id = e.dept_id
               AND e2.salary > e.salary) AS sal_rank
  FROM employees e;
```
**Explanation:** "People strictly paid more than me, plus one" — identical to RANK() output including ties and gaps.

**Alt1:** RANK() as the one-scan equivalent:
```sql
SELECT e.name, e.dept_id, e.salary,
       RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS sal_rank
  FROM employees e;
```
**Note:** Matching results on ties; the correlated COUNT is the pedagogical tool, RANK the production craft.

## Q93: Build a DENSE rank inside each category by counting DISTINCT higher prices (no window functions).

**Query:**
```sql
SELECT p.name, p.category_id, p.price,
       1 + (SELECT COUNT(DISTINCT p2.price)
              FROM products p2
             WHERE p2.category_id = p.category_id
               AND p2.price > p.price) AS dense_rnk
  FROM products p;
```
**Explanation:** Counting distinct higher prices collapses ties, so equal prices share a rank with no gaps — exactly DENSE_RANK semantics.

## Q94: Explain tie handling when finding the per-department max row, and give the query that keeps ALL tied winners.

**Query:**
```sql
-- Keeps every employee tied at the department maximum
SELECT e.name, e.dept_id, e.salary
  FROM employees e
 WHERE NOT EXISTS (SELECT 1
                     FROM employees e2
                    WHERE e2.dept_id = e.dept_id
                      AND e2.salary > e.salary);
```
**Explanation:** The anti-join keeps everyone whom nobody in the department outearns; ties are naturally preserved, unlike a LIMIT-1 approach which picks a single representative.

## Q95: A production table has a million orders. Rewrite a correlated COUNT, explain the plan cost, and note when the correlated form still wins.

**Query:**
```sql
-- Correlated count (n probes) -- keep only when customers is small and orders(customer_id) is indexed
SELECT c.id,
       (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) AS cnt
  FROM customers c;

-- Aggregated rewrite (one scan of orders + hash join)
SELECT c.id, COALESCE(agg.cnt, 0) AS cnt
  FROM customers c
  LEFT JOIN (SELECT customer_id, COUNT(*) AS cnt
               FROM orders GROUP BY customer_id) agg
    ON agg.customer_id = c.id;
```
**Explanation:** The rewrite reads orders once instead of once per customer row; the correlated form is acceptable only for a tiny driving set or when an index makes probes O(log n) so n probes beat a full scan.

## Q96: In a grouped query, add a correlated subquery that references the outer group — each department's average plus how many of its employees exceed it.

**Query:**
```sql
WITH depts AS (
  SELECT dept_id, AVG(salary) AS dept_avg
    FROM employees
   GROUP BY dept_id)
SELECT d.dept_id,
       d.dept_avg,
       (SELECT COUNT(*)
          FROM employees e
         WHERE e.dept_id = d.dept_id
           AND e.salary > d.dept_avg) AS above_avg_count
  FROM depts d;
```
**Explanation:** The correlated subquery consumes both the grouping key (dept_id) and the group's aggregate (dept_avg) from the outer grouped row; aggregates cannot be referenced directly inside such a subquery, hence the CTE indirection.

## Q97: Return the third order of every customer using a correlated LIMIT ... OFFSET.

**Query:**
```sql
SELECT o.customer_id, o.id, o.order_date, o.amount
  FROM orders o
 WHERE o.id = (SELECT o2.id
                 FROM orders o2
                WHERE o2.customer_id = o.customer_id
                ORDER BY o2.order_date, o2.id
                LIMIT 1 OFFSET 2);
```
**Explanation:** Offset 2 skips the first two chronological orders, so the correlated fetch isolates exactly the third one per customer; customers with fewer than three orders match nothing.

## Q98: Convert the "latest order per customer" correlated query to a CTE + ROW_NUMBER and back, then note the execution difference.

**Query:**
```sql
-- Correlated LIMIT-1 form
SELECT o.*
  FROM orders o
 WHERE o.id = (SELECT o2.id
                 FROM orders o2
                WHERE o2.customer_id = o.customer_id
                ORDER BY o2.order_date DESC, o2.id DESC
                LIMIT 1);

-- CTE + ROW_NUMBER form
WITH ranked AS (
  SELECT o.*, ROW_NUMBER() OVER (PARTITION BY customer_id
                                 ORDER BY order_date DESC, id DESC) rn
    FROM orders o)
SELECT * FROM ranked WHERE rn = 1;
```
**Explanation:** Same rows, different engines: the correlated version keeps a per-(customer) probe pattern that an index on (customer_id, order_date) serves; ROW_NUMBER sorts the whole table once and is the safer plan on very wide buckets.

## Q99: Show each employee's salary against the total payroll of their department excluding themselves (correlated SUM with a self-exclusion).

**Query:**
```sql
SELECT e.name, e.dept_id, e.salary,
       (SELECT SUM(e2.salary)
          FROM employees e2
         WHERE e2.dept_id = e.dept_id
           AND e2.id <> e.id) AS department_excl_me
  FROM employees e;
```
**Explanation:** The self-exclusion predicate (e2.id <> e.id) makes the correlation sensitive to the row identity, not just the group key — the sum represents your colleagues.

## Q100: Capstone — combine correlated scalar (SELECT), correlated anti-join (WHERE), and correlated aggregation into one realistic query listing each employee with department name, department average, and a top-earner flag.

**Query:**
```sql
SELECT e.name,
       (SELECT d.name FROM departments d
         WHERE d.id = e.dept_id) AS dept,             -- correlated scalar lookup
       e.salary,
       (SELECT AVG(e2.salary) FROM employees e2
         WHERE e2.dept_id = e.dept_id) AS dept_avg,   -- correlated aggregate
       CASE
         WHEN NOT EXISTS (SELECT 1 FROM employees e9
                           WHERE e9.dept_id = e.dept_id
                             AND e9.salary > e.salary)
              THEN 'TOP EARner'
         ELSE 'no'
       END AS flag                                    -- correlated anti-join
  FROM employees e;
```
**Explanation:** All three staple correlated patterns (projection scalar, projection aggregate, WHERE anti-join) operate on the same outer row, showing that correlation is one mechanism serving every clause.

**Alt1:** Everything the correlated version computes, folded into one pass with window functions:
```sql
SELECT e.name, d.name AS dept, e.salary,
       AVG(e.salary) OVER (PARTITION BY e.dept_id) AS dept_avg,
       CASE WHEN e.salary = MAX(e.salary) OVER (PARTITION BY e.dept_id) THEN 'TOP EARner' ELSE 'no' END AS flag
  FROM employees e
  JOIN departments d ON d.id = e.dept_id;
```
**Note:** Same columns, two indexed-friendly scans; the correlated version is the reference implementation the window version replaces at scale — both are answers, pick by table size.
