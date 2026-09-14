# ORDER BY, Sorting and Pagination — 100 SQL Interview Q&A

## Q1: Return all employees sorted by last name alphabetically.

**Query:**
```sql
SELECT first_name, last_name, department
FROM employees
ORDER BY last_name ASC;
```
**Explanation:** `ASC` is the default sort direction, but including it explicitly improves readability and signals intent.
**Alt1:**
```sql
SELECT first_name, last_name, department
FROM employees
ORDER BY last_name;
```
Omitting `ASC` is equivalent; the direction defaults to ascending.

---

## Q2: Return all products sorted by price from highest to lowest.

**Query:**
```sql
SELECT product_name, price
FROM products
ORDER BY price DESC;
```
**Explanation:** `DESC` reverses the default ascending order so the most expensive rows appear first.
**Alt1:**
```sql
SELECT product_name, price
FROM products
ORDER BY price DESC, product_name ASC;
```
Adding a secondary sort key turns the tie order into a deterministic, reproducible sequence.

---

## Q3: Return customers sorted by last name ascending, then by first name ascending.

**Query:**
```sql
SELECT first_name, last_name, city
FROM customers
ORDER BY last_name ASC, first_name ASC;
```
**Explanation:** Multi-column sorting resolves ties — customers sharing a last name are sub-sorted by first name.

---

## Q4: Sort orders by order date descending, then by total amount descending.

**Query:**
```sql
SELECT order_id, order_date, total_amount
FROM orders
ORDER BY order_date DESC, total_amount DESC;
```
**Explanation:** The most recent orders appear first; among same-date orders the highest-value ones surface first.

---

## Q5: Return employees sorted by hire date ascending and then by salary descending.

**Query:**
```sql
SELECT first_name, last_name, hire_date, salary
FROM employees
ORDER BY hire_date ASC, salary DESC;
```
**Explanation:** Mixed ASC/DESC directions per column — earliest hires first, highest salary among same-date hires.
**Alt1:**
```sql
SELECT first_name, last_name, hire_date, salary
FROM employees
ORDER BY hire_date ASC, salary DESC, employee_id ASC;
```
Appending a unique id as the final key removes any ambiguity when both previous keys tie.

---

## Q6: Sort the employee table by department ascending, then by last name ascending.

**Query:**
```sql
SELECT first_name, last_name, department
FROM employees
ORDER BY department ASC, last_name ASC;
```
**Explanation:** Grouping by department with alphabetical names within each group — a classic tie-breaking pattern.

---

## Q7: Return all orders sorted by total amount descending.

**Query:**
```sql
SELECT order_id, customer_id, total_amount
FROM orders
ORDER BY total_amount DESC;
```
**Explanation:** Simple single-column descending sort to find the highest-value orders.

---

## Q8: Sort products by category ascending, then by unit price descending.

**Query:**
```sql
SELECT product_name, category, unit_price
FROM products
ORDER BY category ASC, unit_price DESC;
```
**Explanation:** Categories are alphabetically ordered; within each category, the priciest items come first.
**Alt1:**
```sql
SELECT product_name, category, unit_price
FROM products
ORDER BY 2 ASC, 3 DESC;
```
Positional sort keys are a MySQL/PostgreSQL shorthand that mirrors the SELECT list when column names get verbose.

---

## Q9: Return all customers sorted by city, then by last name, both ascending.

**Query:**
```sql
SELECT first_name, last_name, city
FROM customers
ORDER BY city ASC, last_name ASC;
```
**Explanation:** Groups customers geographically first, then alphabetically within each city.

---

## Q10: Sort employees by department ascending, then by hire date descending (most recent first within department).

**Query:**
```sql
SELECT first_name, last_name, department, hire_date
FROM employees
ORDER BY department ASC, hire_date DESC;
```
**Explanation:** Newest hires within each department appear at the top of that department's block.

---

## Q11: Sort a query by the alias "total" which is computed as quantity * unit_price.

**Query:**
```sql
SELECT product_name, quantity, unit_price, quantity * unit_price AS total
FROM order_items
ORDER BY total DESC;
```
**Explanation:** ORDER BY can reference column aliases defined in the SELECT list, letting you sort by computed values cleanly.

---

## Q12: Return all employees sorted by the second column in the SELECT list.

**Query:**
```sql
SELECT first_name, last_name, department
FROM employees
ORDER BY 2 ASC;
```
**Explanation:** ORDER BY accepts ordinal position matching the SELECT list; `2` refers to `last_name`. Readable for ad-hoc queries but fragile when columns change.

---

## Q13: Sort employees by department, then by salary descending using column positions.

**Query:**
```sql
SELECT first_name, last_name, department, salary
FROM employees
ORDER BY 3 ASC, 4 DESC;
```
**Explanation:** Position `3` is `department` and `4` is `salary` — multi-column positional sorting works in MySQL and PostgreSQL.

---

## Q14: Sort employees by the length of their last name, longest first.

**Query:**
```sql
SELECT first_name, last_name
FROM employees
ORDER BY LENGTH(last_name) DESC;
```
**Explanation:** ORDER BY accepts arbitrary expressions; `LENGTH()` returns the character count of the string.
**Alt1:**
```sql
SELECT first_name, last_name, LENGTH(last_name) AS name_len
FROM employees
ORDER BY name_len DESC;
```
Recomputing the expression via an alias is cleaner when the length is also projected for display.

---

## Q15: Sort customers alphabetically by last name, ignoring case sensitivity.

**Query:**
```sql
-- PostgreSQL
SELECT first_name, last_name
FROM customers
ORDER BY last_name COLLATE "en-US-x-icu" ASC;
```
**Explanation:** COLLATE overrides the column's default collation, ensuring case-insensitive or locale-specific alphabetical order.

---

## Q16: Sort products by a custom category priority: Electronics, Furniture, Clothing, then everything else alphabetically.

**Query:**
```sql
SELECT product_name, category
FROM products
ORDER BY
  CASE category
    WHEN 'Electronics' THEN 1
    WHEN 'Furniture'  THEN 2
    WHEN 'Clothing'   THEN 3
    ELSE 4
  END ASC,
  category ASC;
```
**Explanation:** CASE in ORDER BY assigns a numeric rank to specific values for logical custom ordering; ties in the same rank sort alphabetically.
**Alt1:**
```sql
SELECT product_name, category
FROM products
ORDER BY
  CASE WHEN category IN ('Electronics', 'Furniture', 'Clothing')
       THEN 'zzz' ELSE category END DESC;
```
A string-substitution trick can force chosen categories above the rest, though the numeric CASE is clearer for three or more tiers.

---

## Q17: Sort order status so that 'Shipped' appears first, then 'Processing', then 'Pending', then all others alphabetically.

**Query:**
```sql
SELECT order_id, status
FROM orders
ORDER BY
  CASE status
    WHEN 'Shipped'    THEN 1
    WHEN 'Processing' THEN 2
    WHEN 'Pending'    THEN 3
    ELSE 4
  END,
  status;
```
**Explanation:** CASE-based custom sort places defined statuses in a specific order before falling back to alphabetical for remaining values.

---

## Q18: Sort employees so that NULL salaries appear at the top.

**Query:**
```sql
-- PostgreSQL / Oracle
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary ASC NULLS FIRST;
```
**Explanation:** `NULLS FIRST` explicitly places NULLs before all non-NULL values regardless of sort direction.

---

## Q19: Sort employees so that NULL salaries appear last.

**Query:**
```sql
-- PostgreSQL / Oracle
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary ASC NULLS LAST;
```
**Explanation:** `NULLS LAST` is the inverse; in Oracle `NULLS LAST` is the default for ASC, in PostgreSQL you must specify it.
**Alt1:**
```sql
-- PostgreSQL
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary IS NULL ASC, salary ASC;
```
The `IS NULL` expression trick works on every engine, so this is the portable way to express the same rule in MySQL or SQLite.

---

## Q20: Sort employees by salary ascending, making NULLs appear last in MySQL.

**Query:**
```sql
-- MySQL
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary IS NULL ASC, salary ASC;
```
**Explanation:** MySQL lacks `NULLS LAST`; `IS NULL` evaluates to 0 for non-NULL and 1 for NULL — sorting it ASC pushes NULLs after all real values.

---

## Q21: Sort employees by salary descending, making NULLs appear last in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT first_name, last_name, salary
FROM employees
ORDER BY
  CASE WHEN salary IS NULL THEN 1 ELSE 0 END ASC,
  salary DESC;
```
**Explanation:** SQL Server has no `NULLS LAST` syntax; the CASE expression creates a secondary sort key that flags NULLs as 1, placing them after non-NULL rows.

---

## Q22: Sort employees by salary descending, making NULLs appear first in Oracle.

**Query:**
```sql
-- Oracle
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary DESC NULLS FIRST;
```
**Explanation:** Oracle defaults `NULLS LAST` for DESC; `NULLS FIRST` overrides this to surface NULLs at the top.

---

## Q23: Sort customers by last name using a case-insensitive collation in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT first_name, last_name
FROM customers
ORDER BY last_name COLLATE SQL_Latin1_General_CP1_CI_AS ASC;
```
**Explanation:** The `CI` collation flag makes the sort case-insensitive; 'smith' and 'Smith' compare as equal and stable-sort by physical row order.

---

## Q24: Sort products by price ascending, then by product name descending, using column aliases and expressions.

**Query:**
```sql
SELECT product_name, price, price * 1.1 AS adjusted_price
FROM products
ORDER BY price ASC, product_name DESC;
```
**Explanation:** Demonstrates mixing a base column sort with an expression and alias in the same query.

---

## Q25: Sort employees by a computed bonus (salary * 0.1) descending.

**Query:**
```sql
SELECT first_name, last_name, salary, salary * 0.1 AS bonus
FROM employees
ORDER BY salary * 0.1 DESC;
```
**Explanation:** ORDER BY accepts the full expression directly; the computed column doesn't need an alias in the SELECT list.
**Alt1:**
```sql
SELECT first_name, last_name, salary, salary * 0.1 AS bonus
FROM employees
ORDER BY bonus DESC;
```
Aliasing the expression once keeps ORDER BY readable and avoids recomputing it twice in the written query.

---
## Q26: Sort students by grade descending and, for ties, place null grades last.

**Query:**
```sql
-- PostgreSQL
SELECT student_name, grade
FROM students
ORDER BY grade DESC NULLS LAST;
```
**Explanation:** `NULLS LAST` forces students without a grade to appear after all graded students even though `DESC` in PostgreSQL puts NULLs first by default.

---

## Q27: Return only the first 5 products ordered by price descending, in MySQL.

**Query:**
```sql
-- MySQL
SELECT product_name, price
FROM products
ORDER BY price DESC
LIMIT 5;
```
**Explanation:** `LIMIT 5` truncates the sorted result set to five rows — the standard MySQL/Postgres/SQLite pagination primitive.
**Alt1:**
```sql
-- PostgreSQL
SELECT product_name, price
FROM products
ORDER BY price DESC
FETCH FIRST 5 ROWS ONLY;
```
PostgreSQL and Oracle 12c+ accept the ISO `FETCH FIRST` form, which reads identically to SQL Server's `FETCH NEXT`.

---

## Q28: Return rows 6 through 10 of the products sorted by price descending, in MySQL.

**Query:**
```sql
-- MySQL
SELECT product_name, price
FROM products
ORDER BY price DESC
LIMIT 5 OFFSET 5;
```
**Explanation:** `OFFSET 5` skips the first five rows, then `LIMIT 5` returns five — giving page 2 of a page-size-5 result set.

---

## Q29: Return rows 6 through 10 of the products sorted by price descending, in SQL Server.

**Query:**
```sql
-- SQL Server
SELECT product_name, price
FROM products
ORDER BY price DESC
OFFSET 5 ROWS FETCH NEXT 5 ROWS ONLY;
```
**Explanation:** `OFFSET ... ROWS FETCH NEXT ... ROWS ONLY` is the ISO standard pagination syntax used by SQL Server; ORDER BY is mandatory with it.
**Alt1:**
```sql
-- SQL Server
SELECT TOP 5 product_name, price
FROM (
  SELECT product_name, price, ROW_NUMBER() OVER (ORDER BY price DESC) AS rn
  FROM products
) sub
WHERE rn BETWEEN 6 AND 10
ORDER BY rn;
```
ROW_NUMBER-based paging works on older SQL Server builds that predate `OFFSET/FETCH`.

---

## Q30: Return rows 6 through 10 of the products sorted by price descending, in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT product_name, price
FROM products
ORDER BY price DESC
OFFSET 5 ROWS FETCH NEXT 5 ROWS ONLY;
```
**Explanation:** PostgreSQL supports both `LIMIT/OFFSET` and the standard `OFFSET ... FETCH` syntax; `FETCH NEXT` is equivalent to `LIMIT`.

---

## Q31: Fetch the first 10 rows of the employees table with no guaranteed order.

**Query:**
```sql
-- SQLite
SELECT employee_id, first_name
FROM employees
LIMIT 10;
```
**Explanation:** Without ORDER BY, which 10 rows you get is nondeterministic; the engine may return rows in physical storage order.
**Alt1:**
```sql
-- MySQL
SELECT employee_id, first_name
FROM employees
ORDER BY (SELECT NULL)
LIMIT 10;
```
Adding a constant ORDER BY key is a common trick to satisfy tools that require ORDER BY while keeping the natural access path.

---

## Q32: Fetch the most recently hired employee.

**Query:**
```sql
SELECT employee_id, first_name, hire_date
FROM employees
ORDER BY hire_date DESC
LIMIT 1;
```
**Explanation:** Sort descending by hire date and take the single first row — a common "latest row" pattern.

---

## Q33: Find the top 3 highest-paid employees.

**Query:**
```sql
SELECT employee_id, first_name, last_name, salary
FROM employees
ORDER BY salary DESC
LIMIT 3;
```
**Explanation:** `ORDER BY salary DESC LIMIT 3` is the canonical "top-N" query pattern.
**Alt1:**
```sql
-- Oracle
SELECT employee_id, first_name, last_name, salary
FROM (
  SELECT employee_id, first_name, last_name, salary
  FROM employees
  ORDER BY salary DESC
)
WHERE ROWNUM <= 3;
```
Oracle pre-12c has no LIMIT, so ORDER BY in an inline view is wrapped with a `ROWNUM <= N` filter.

---

## Q34: Find the top 5 most expensive orders using SQL Server's TOP clause with ORDER BY.

**Query:**
```sql
-- SQL Server
SELECT TOP 5 order_id, total_amount
FROM orders
ORDER BY total_amount DESC;
```
**Explanation:** SQL Server's `TOP` must be combined with an explicit `ORDER BY` to guarantee the top rows by a meaningful criterion.

---

## Q35: Return the bottom 3 cheapest products using SQL Server's TOP.

**Query:**
```sql
-- SQL Server
SELECT TOP 3 product_name, price
FROM products
ORDER BY price ASC;
```
**Explanation:** Order ascending so the cheapest products sort first, then cap the result with `TOP 3`.

---

## Q36: Retrieve page 100 of a catalog sorted by product name, 10 per page, in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT product_name
FROM products
ORDER BY product_name ASC
LIMIT 10 OFFSET 990;
```
**Explanation:** `OFFSET = (page_number - 1) * page_size` = 990; rows 991–1000 come back.

---

## Q37: Retrieve the first 10 rows on the very first page of employees ordered by last name in SQLite.

**Query:**
```sql
-- SQLite
SELECT employee_id, last_name
FROM employees
ORDER BY last_name ASC
LIMIT 10;
```
**Explanation:** The first page is simply `LIMIT page_size` with no OFFSET, which is also a keyset-pagination-friendly starting point.

---

## Q38: Paginate a result set by 25 rows per page using SQL Server, returning page 3.

**Query:**
```sql
-- SQL Server
SELECT order_id, order_date
FROM orders
ORDER BY order_date ASC, order_id ASC
OFFSET 50 ROWS FETCH NEXT 25 ROWS ONLY;
```
**Explanation:** Page 3 skips 2 previous pages (2 × 25 = 50) and fetches the next 25 rows, ordered for determinism.

---

## Q39: Fetch the last 5 employees added to the employees table.

**Query:**
```sql
SELECT employee_id, first_name, hire_date
FROM employees
ORDER BY employee_id DESC
LIMIT 5;
```
**Explanation:** Descending order by the auto-increment id surfaces the most recently inserted rows as the "last" ones.

---

## Q40: In Oracle, return the first 5 rows sorted by salary descending, without a LIMIT clause.

**Query:**
```sql
-- Oracle
SELECT first_name, last_name, salary
FROM employees
WHERE ROWNUM <= 5
ORDER BY salary DESC;
```
**Explanation:** Oracle applies the WHERE/ROWNUM filter before ORDER BY, so this is only correct if rows were already sorted — on data this is wrong; see next question for the fix.
**Alt1:**
```sql
-- Oracle 12c+
SELECT first_name, last_name, salary
FROM employees
ORDER BY salary DESC
FETCH FIRST 5 ROWS ONLY;
```
Oracle 12c added `FETCH FIRST`, removing the need for the ROWNUM gymnastics entirely.

---

## Q41: In Oracle, correctly return the top 5 rows sorted by salary descending.

**Query:**
```sql
-- Oracle
SELECT *
FROM (
  SELECT first_name, last_name, salary
  FROM employees
  ORDER BY salary DESC
) 
WHERE ROWNUM <= 5;
```
**Explanation:** The inline view orders rows first, and the outer `ROWNUM <= 5` then picks the top 5 in that order — the classic top-N Oracle idiom.

---

## Q42: In Oracle, paginate employees sorting by salary, 10 per page, returning page 2.

**Query:**
```sql
-- Oracle
SELECT employee_id, first_name, salary
FROM (
  SELECT e.*, ROWNUM AS rn
  FROM (
    SELECT employee_id, first_name, salary
    FROM employees
    ORDER BY salary DESC
  ) e
)
WHERE rn BETWEEN 11 AND 20;
```
**Explanation:** ROWNUM is assigned before sorting, so the inner view sorts, the middle view tags a row number, and the outer filter slices page 2 (rows 11–20).

---

## Q43: Paginate with page numbers using ROW_NUMBER in Oracle, returning page 3 of 10.

**Query:**
```sql
-- Oracle
SELECT employee_id, first_name, salary
FROM (
  SELECT employee_id, first_name, salary,
         ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn
  FROM employees
)
WHERE rn BETWEEN 21 AND 30;
```
**Explanation:** `ROW_NUMBER()` numbers results after ordering; filtering on `rn` yields any page. Oracle 12c+ also offers `OFFSET/FETCH` as a simpler alternative.
**Alt1:**
```sql
-- Oracle 12c+
SELECT employee_id, first_name, salary
FROM employees
ORDER BY salary DESC
OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;
```
The ISO `OFFSET/FETCH` form is the modern, shorter way to express the same page in Oracle 12c+.

---

## Q44: In Oracle 12c+, return the next 10 rows after skipping the first 20, ordered by last name.

**Query:**
```sql
-- Oracle
SELECT employee_id, last_name
FROM employees
ORDER BY last_name
OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;
```
**Explanation:** Oracle added ISO `OFFSET/FETCH` in 12c, making modern pagination identical in feel to SQL Server and PostgreSQL.

---

## Q45: Fetch the first 5 orders after (strictly greater than) order_id 100, sorted by order_id, using keyset pagination.

**Query:**
```sql
SELECT order_id, total_amount
FROM orders
WHERE order_id > 100
ORDER BY order_id ASC
LIMIT 5;
```
**Explanation:** Keyset/cursor pagination filters on the last seen key and orders by it; every page is a small, index-friendly lookup instead of a big skip.
**Alt1:**
```sql
-- PostgreSQL
SELECT order_id, total_amount
FROM orders
WHERE order_id > 100
ORDER BY order_id ASC
FETCH FIRST 5 ROWS ONLY;
```
PostgreSQL accepts the standard `FETCH FIRST` synonym for `LIMIT` — identical semantics, different spelling.

---

## Q46: Fetch the next 10 products after (less than) product_id 5000, sorted by product_id descending.

**Query:**
```sql
SELECT product_id, product_name
FROM products
WHERE product_id < 5000
ORDER BY product_id DESC
LIMIT 10;
```
**Explanation:** Backwards keyset: use the exclusive `<` bound with a descending sort so the query reads just 10 index rows past the cursor.

---

## Q47: Keyset-paginate customers by last name, returning the next page after the customer 'Miller'.

**Query:**
```sql
SELECT customer_id, last_name, first_name
FROM customers
WHERE last_name > 'Miller'
ORDER BY last_name ASC, customer_id ASC
LIMIT 10;
```
**Explanation:** Non-unique sort keys require a tie-breaker: after 'Miller', filter lexically and include a unique id to keep pagination exact.

---

## Q48: Keyset-paginate orders sorted by order_date, returning the page after a specific (date, id) cursor of ('2024-01-15', 42).

**Query:**
```sql
SELECT order_id, order_date
FROM orders
WHERE (order_date > '2024-01-15')
   OR (order_date = '2024-01-15' AND order_id > 42)
ORDER BY order_date ASC, order_id ASC
LIMIT 10;
```
**Explanation:** The composite WHERE encodes the full cursor position — a tuple comparison — so both dimensions advance correctly in one statement.
**Alt1:**
```sql
-- PostgreSQL
SELECT order_id, order_date
FROM orders
WHERE (order_date, order_id) > ('2024-01-15', 42)
ORDER BY order_date ASC, order_id ASC
LIMIT 10;
```
PostgreSQL's row-value syntax compresses the two-column cursor into a single expression with identical lexicographic semantics.

---

## Q49: Return the most recently updated 10 records, then the page after the current cursor using updated_at.

**Query:**
```sql
SELECT id, title, updated_at
FROM posts
WHERE updated_at < '2024-06-01 10:30:00'
ORDER BY updated_at DESC, id DESC
LIMIT 10;
```
**Explanation:** Descending keyset on a timestamp: pass the newest seen `updated_at` as the bound to walk back through history page by page.

---

## Q50: Deterministically sort employees by salary descending, breaking ties by hire_date then by employee_id.

**Query:**
```sql
SELECT employee_id, first_name, salary, hire_date
FROM employees
ORDER BY salary DESC, hire_date ASC, employee_id ASC;
```
**Explanation:** Adding a unique key as the final sort column guarantees total ordering so every run returns identical pagination pages.

---
## Q51: Return the employees with the 3 lowest salaries, treating ties by including all employees with the same salary as the 3rd.

**Query:**
```sql
SELECT employee_id, first_name, salary
FROM employees
ORDER BY salary ASC
LIMIT 3;
```
**Explanation:** A plain LIMIT can split a tie at the boundary; use RANK()-style logic or keyset on salary if ties must stay intact (see next).

---

## Q52: Return employees sorted so that those in the SALES department come first, then marketing, then everyone else by hire date.

**Query:**
```sql
SELECT employee_id, first_name, department, hire_date
FROM employees
ORDER BY
  CASE WHEN department = 'SALES'     THEN 1
       WHEN department = 'MARKETING' THEN 2
       ELSE 3
  END ASC,
  hire_date ASC;
```
**Explanation:** CASE in ORDER BY handles an arbitrary priority order, with a fallback sort on hire date for the rest.
**Alt1:**
```sql
SELECT employee_id, first_name, department, hire_date
FROM employees
ORDER BY
  FIELD(department, 'SALES', 'MARKETING') = 0 ASC,
  FIELD(department, 'SALES', 'MARKETING') ASC,
  hire_date ASC;
```
MySQL's `FIELD()` returns the index of a value in a list; unknown departments get 0 and sink below the ranked ones.

---

## Q53: Sort orders by status so 'Urgent' orders come first, then sort by created_at descending.

**Query:**
```sql
SELECT order_id, status, created_at
FROM orders
ORDER BY
  CASE WHEN status = 'Urgent' THEN 0 ELSE 1 END,
  created_at DESC;
```
**Explanation:** Flags the urgent rows with a low sort key so they lead, while all others follow by most recent first.

---

## Q54: Sort employees by last name ignoring case and accents where possible, in MySQL using a collation.

**Query:**
```sql
-- MySQL
SELECT first_name, last_name
FROM employees
ORDER BY last_name COLLATE utf8mb4_unicode_ci ASC;
```
**Explanation:** `utf8mb4_unicode_ci` compares case- and accent-insensitively, giving linguistically sensible ordering for many Latin-script names.

---

## Q55: Sort products by a nullable discount column, placing the highest non-null discount first and all NULL discounts last.

**Query:**
```sql
-- PostgreSQL
SELECT product_name, discount
FROM products
ORDER BY discount DESC NULLS LAST;
```
**Explanation:** `DESC` + `NULLS LAST` orders non-null discounts from high to low while pinning rows without a discount to the end.
**Alt1:**
```sql
-- MySQL
SELECT product_name, discount
FROM products
ORDER BY discount IS NULL ASC, discount DESC;
```
The `IS NULL` guard is the portable MySQL equivalent when `NULLS LAST` is unavailable.

---

## Q56: Sort products so that NULL discounts are treated as 0 and sort lowest first.

**Query:**
```sql
-- SQL Server / SQLite
SELECT product_name, discount
FROM products
ORDER BY COALESCE(discount, 0) ASC;
```
**Explanation:** `COALESCE(discount, 0)` substitutes 0 for NULL, so missing discounts sort as if they were the smallest value instead of floating to an end.

---

## Q57: Sort employees by salary in MySQL, guaranteeing NULLs first.

**Query:**
```sql
-- MySQL
SELECT employee_id, salary
FROM employees
ORDER BY salary IS NOT NULL ASC, salary ASC;
```
**Explanation:** `IS NOT NULL` yields 1 for non-NULL and 0 for NULL; ascending on it puts NULL rows before real salaries.

---

## Q58: Sort by the second column then the fourth column of a SELECT that mixes aliases, in MySQL.

**Query:**
```sql
-- MySQL
SELECT first_name, last_name, salary, salary * 0.05 AS bonus
FROM employees
ORDER BY 2 ASC, 4 DESC;
```
**Explanation:** You can mix positional references (column 2 = last_name, 4 = bonus expression) in a single ORDER BY in MySQL.

---

## Q59: Return the top 10 bestselling products by quantity sold.

**Query:**
```sql
SELECT product_id, product_name, SUM(quantity) AS units_sold
FROM order_items
GROUP BY product_id
ORDER BY units_sold DESC
LIMIT 10;
```
**Explanation:** Sorting an aggregation by its alias works because GROUP BY collapses rows before ORDER BY applies; ties may appear arbitrarily.

---

## Q60: Return 10 random customers using ORDER BY with a random function, and explain why it's slow on big tables.

**Query:**
```sql
-- PostgreSQL
SELECT customer_id, first_name
FROM customers
ORDER BY RANDOM()
LIMIT 10;
```
**Explanation:** `RANDOM()` is evaluated per row as a sort key so the whole table must be scanned and sorted — an O(n log n) full-table sort on every call.

---

## Q61: Retrieve the first page of comments ordered newest first, using keyset pagination on comment_id.

**Query:**
```sql
SELECT comment_id, body, created_at
FROM comments
ORDER BY comment_id DESC
LIMIT 20;
```
**Explanation:** Page one is plain `LIMIT 20` and the cursor becomes the smallest id seen (the 20th row).

---

## Q62: Fetch the second page of comments after the cursor comment_id = 500.

**Query:**
```sql
SELECT comment_id, body, created_at
FROM comments
WHERE comment_id < 500
ORDER BY comment_id DESC
LIMIT 20;
```
**Explanation:** The next page filters `comment_id < 500` (the last id of page one), so the engine scans only the index beyond the cursor.

---

## Q63: Sort orders by total_amount descending, ties broken by order_id ascending.

**Query:**
```sql
SELECT order_id, total_amount
FROM orders
ORDER BY total_amount DESC, order_id ASC;
```
**Explanation:** The unique `order_id` tie-breaker makes the sort deterministic and makes keyset pagination on this query possible.

---

## Q64: Return the last 5 orders placed, using OFFSET against the full item count.

**Query:**
```sql
SELECT order_id, order_date
FROM orders
ORDER BY order_id ASC
OFFSET (
  SELECT COUNT(*) - 5 FROM orders
) ROWS;
```
**Explanation:** OFFSET can be a subquery; here it jumps to five rows before the end without knowing the total ahead of time (works in PostgreSQL/SQL Server).

---

## Q65: Return the 11th to 20th most expensive products, sorted by price, on rows that can repeat price values.

**Query:**
```sql
SELECT product_id, product_name, price
FROM products
ORDER BY price DESC, product_id ASC
LIMIT 10 OFFSET 10;
```
**Explanation:** Sorting by price plus a unique tie-breaker guarantees the same 10 rows populate page 2 every time, even with duplicate prices.
**Alt1:**
```sql
-- PostgreSQL
SELECT product_id, product_name, price
FROM products
ORDER BY price DESC, product_id ASC
OFFSET 10 ROWS FETCH NEXT 10 ROWS ONLY;
```
The same page expressible in `OFFSET/FETCH` syntax; semantics are identical to LIMIT/OFFSET.

---

## Q66: Sort posts by a "pinned" flag so pinned posts surface first, then by created_at descending.

**Query:**
```sql
SELECT id, title, pinned, created_at
FROM posts
ORDER BY pinned DESC, created_at DESC;
```
**Explanation:** Sorting the boolean `pinned` descending puts `1` (TRUE/pinned) rows before regular posts, then recency takes over.
**Alt1:**
```sql
SELECT id, title, pinned, created_at
FROM posts
ORDER BY pinned DESC, created_at DESC, id DESC;
```
A unique id guard keeps pinned feeds stable in ordering even when two posts share a timestamp.

---

## Q67: Sort employees by full name (last + first concatenated) alphabetically.

**Query:**
```sql
SELECT employee_id, first_name, last_name
FROM employees
ORDER BY CONCAT(last_name, ', ', first_name) ASC;
```
**Explanation:** The concatenation expression is evaluated and sorted just like any other ORDER BY expression.

---

## Q68: Sort customers by their birth date descending then by last name ascending, in Oracle with NULLs last on the date.

**Query:**
```sql
-- Oracle
SELECT customer_id, last_name, birth_date
FROM customers
ORDER BY birth_date DESC NULLS LAST, last_name ASC;
```
**Explanation:** Explicit `NULLS LAST` on a DESC timestamp keeps records with unknown birth dates at the bottom of each page.

---

## Q69: Retrieve the first 15 rows of a large table using keyset pagination when ids are not sequential.

**Query:**
```sql
SELECT id, title
FROM articles
WHERE id > 0
ORDER BY id ASC
LIMIT 15;
```
**Explanation:** `id > 0` acts as a no-op cursor start; each following page replaces the bound with the last id from the prior page, so gaps don't shift pages.

---

## Q70: Paginate a phone directory by last name, first name, and phone id, returning the page after ('Brown', 'Ann', 7).

**Query:**
```sql
SELECT last_name, first_name, phone_id, phone_number
FROM phone_directory
WHERE (last_name > 'Brown')
   OR (last_name = 'Brown' AND (first_name > 'Ann'
       OR (first_name = 'Ann' AND phone_id > 7)))
ORDER BY last_name ASC, first_name ASC, phone_id ASC
LIMIT 25;
```
**Explanation:** A nested tuple-style condition advances all three sort keys at once — the general keyset form for any arity of ORDER BY columns.

---

## Q71: Sort department rows by a custom hierarchy order: 'Engineering', 'Finance', 'HR', 'Sales', then unknown departments last.

**Query:**
```sql
SELECT department
FROM employees
ORDER BY
  CASE department
    WHEN 'Engineering' THEN 1
    WHEN 'Finance'     THEN 2
    WHEN 'HR'          THEN 3
    WHEN 'Sales'       THEN 4
    ELSE 5
  END;
```
**Explanation:** A complete lookup mapping in CASE gives a fully controlled, non-alphabetical business order; any other value falls to tier 5.

---

## Q72: Return the newest 20 articles by published_at, and fetch the page after a nullable published_at cursor.

**Query:**
```sql
-- PostgreSQL
SELECT article_id, title, published_at
FROM articles
WHERE published_at < '2024-11-30 00:00:00'
ORDER BY published_at DESC NULLS LAST, article_id DESC
LIMIT 20;
```
**Explanation:** Sorting `published_at DESC NULLS LAST` means NULL timestamps cluster at the end; filtering with `<` before sorting keeps pages positionally stable.

---

## Q73: Sort orders so that completed orders sink to the bottom while the rest are sorted by created_at descending.

**Query:**
```sql
SELECT order_id, status, created_at
FROM orders
ORDER BY
  CASE WHEN status = 'completed' THEN 1 ELSE 0 END,
  created_at DESC;
```
**Explanation:** The CASE first segregates completed (1) from active (0) orders, then the recency sort applies within each bucket.

---

## Q74: Return the 5 newest employees per department using LIMIT within a partitioned window-like approach (single query).

**Query:**
```sql
-- PostgreSQL
SELECT department, first_name, hire_date
FROM employees e1
WHERE (
  SELECT COUNT(*)
  FROM employees e2
  WHERE e2.department = e1.department
    AND (e2.hire_date > e1.hire_date
         OR (e2.hire_date = e1.hire_date AND e2.employee_id > e1.employee_id))
) < 5
ORDER BY department ASC, hire_date DESC, employee_id DESC;
```
**Explanation:** A correlated subquery counts a row's newest-siblings; keeping count < 5 returns only the top 5 per department using the sort keys.

---

## Q75: Sort products with a boolean "featured" flag and a priority number, featured flag winning first.

**Query:**
```sql
SELECT product_id, product_name, featured, priority
FROM products
ORDER BY featured DESC, priority ASC, product_id ASC;
```
**Explanation:** The boolean separates featured products, priority orders them within both groups, and id breaks final ties deterministically.

---
## Q76: Sort customers in SQL Server with case-insensitive ordering and no collation knowledge, using a functional trick.

**Query:**
```sql
-- SQL Server
SELECT customer_id, last_name
FROM customers
ORDER BY LOWER(last_name) ASC;
```
**Explanation:** Wrapping the key in `LOWER()` forces comparable case, and a `last_name` suffix tie-breaker could follow for stability.

---

## Q77: Return products sorted by price but keeping NULLs in the middle.

**Query:**
```sql
-- PostgreSQL
SELECT product_id, price
FROM products
ORDER BY
  CASE WHEN price IS NULL THEN 1 ELSE 0 END,
  price;
```
**Explanation:** NULL gets band rank 1, sandwiched between non-NULL block 0 and (implicitly, the next bucket) so NULLs stay in the middle; use separate CASE values for before/after.

---

## Q78: Return the exact 100th most expensive product in the catalog, sorted by price descending with ties.

**Query:**
```sql
SELECT product_id, product_name, price
FROM products
ORDER BY price DESC, product_id ASC
LIMIT 1 OFFSET 99;
```
**Explanation:** OFFSET 99 skips the top 99 rows and LIMIT 1 returns one — deterministic only because of the unique tie-breaker.

---

## Q79: Fetch orders more than 10 rows past the cursor on a created_at + id order using a tuple comparison in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT order_id, created_at
FROM orders
WHERE (created_at, order_id) > ('2024-03-01 12:00:00', 100)
ORDER BY created_at ASC, order_id ASC
LIMIT 10;
```
**Explanation:** Row-value comparison `(a, b) > (x, y)` is lexicographic, matching the ORDER BY key exactly — MySQL and SQLite also support row constructors.
**Alt1:**
```sql
SELECT order_id, created_at
FROM orders
WHERE created_at > '2024-03-01 12:00:00'
   OR (created_at = '2024-03-01 12:00:00' AND order_id > 100)
ORDER BY created_at ASC, order_id ASC
LIMIT 10;
```
The expanded OR form is portable to every SQL dialect; the tuple expression is simply syntactic sugar for it.

---

## Q80: Paginate users in SQLite sorted by name descending using keyset on a text key.

**Query:**
```sql
-- SQLite
SELECT user_id, name
FROM users
WHERE name < 'last_returned_name'
ORDER BY name DESC
LIMIT 20;
```
**Explanation:** For DESC text, the cursor moves downward: filter `name <` the previous page's last row and keep a unique secondary key for exactness.

---

## Q81: Get the 3 most recent log entries per device with keyset pagination for the next page.

**Query:**
```sql
SELECT device_id, entry_id, logged_at
FROM logs
WHERE device_id = 7
  AND entry_id < 900
ORDER BY entry_id DESC
LIMIT 3;
```
**Explanation:** Filtering the devices to one yields a plain keyset page; production systems usually keep per-device cursors.

---

## Q82: Order a list so rows where a flag is NULL sort at the very end.

**Query:**
```sql
-- MySQL
SELECT id, row_num, flag
FROM items
ORDER BY flag IS NULL ASC, row_num ASC;
```
**Explanation:** `flag IS NULL` produces 0 for valid flags and 1 for NULL, so NULL rows sort after all valid rows while row_num keeps the rest ordered.

---

## Q83: Sort a "to-do" table by due_date but put overdue items on top, then by priority.

**Query:**
```sql
SELECT task_id, title, due_date, priority
FROM tasks
ORDER BY
  CASE WHEN due_date < CURRENT_DATE THEN 0 ELSE 1 END,
  priority ASC,
  due_date ASC;
```
**Explanation:** A computed "overdue" binary turns the sort into: overdue first, then priority, then due date for incomplete scheduling.

---

## Q84: Paginate by a non-contiguous key to fetch the next 5 rows after 89 in MySQL, without OFFSET.

**Query:**
```sql
SELECT id, name
FROM cities
WHERE id > 89
ORDER BY id ASC
LIMIT 5;
```
**Explanation:** Keyset needs no consecutive keys — it jumps straight past whatever was seen, immune to inserts and deletes shifting pages.

---

## Q85: Return employees sorted by department in a custom order, then by salary descending, NULLs last, in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT employee_id, department, salary
FROM employees
ORDER BY
  CASE department WHEN 'Eng' THEN 1 WHEN 'Ops' THEN 2 WHEN 'Bus' THEN 3 ELSE 4 END,
  salary DESC NULLS LAST;
```
**Explanation:** Two-stage sort: CASE ranks departments, then `DESC NULLS LAST` orders salaries within the tier while pushing NULL salaries behind real ones.

---

## Q86: Sort a numeric string column (e.g., zip codes stored as text) naturally so 9 < 100.

**Query:**
```sql
SELECT store_id, zip_code
FROM stores
ORDER BY CAST(zip_code AS INTEGER) ASC;
```
**Explanation:** Casting text digits to an integer compares numerically rather than lexicographically, so '9' sorts before '100'.

---

## Q87: Return the newest product per catalog page using keyset pagination on an auto-incrementing id with a soft-delete column.

**Query:**
```sql
SELECT product_id, product_name, deleted
FROM products
WHERE deleted = 0
  AND product_id > 5000
ORDER BY product_id ASC
LIMIT 12;
```
**Explanation:** Keyset over an id plus a `deleted` predicate stays efficient: the id bound stops deep OFFSET scans and the flag filters permanently-removed rows.

---

## Q88: Force a stable sort on a query that has no unique key by simulating one.

**Query:**
```sql
-- PostgreSQL
SELECT employee_id, first_name, salary
FROM employees
ORDER BY salary DESC, employee_id ASC;
```
**Explanation:** A guaranteed-unique id column appended as the last key creates total order — the practical definition of a stable sort.

---

## Q89: Return 5 random users with a fast alternative approach that avoids sorting the entire table.

**Query:**
```sql
-- SQLite
SELECT user_id, name
FROM users
ORDER BY RANDOM()
LIMIT 5;
```
**Explanation:** A full random sort is the classic method; bigger systems prefer sampling a random id offset or TABLESAMPLE to avoid scanning everything.
**Alt1:**
```sql
-- PostgreSQL
SELECT user_id, name
FROM users
TABLESAMPLE BERNOULLI (1)
ORDER BY RANDOM()
LIMIT 5;
```
Sampling a small fraction first, then randomizing, keeps the point-in-time random page cheap on large tables.

---

## Q90: Paginate notifications by a user with keyset on a boolean read/watched flag plus id.

**Query:**
```sql
SELECT id, title, is_read
FROM notifications
WHERE user_id = 42
  AND NOT is_read
  AND id > 800
ORDER BY id ASC
LIMIT 20;
```
**Explanation:** The cursor rides the id, while `NOT is_read` is a constant filter — pages stay correct even after older rows are marked read mid-pagination.

---

## Q91: Return, per company, the latest 2 news items you would later keyset-paginate from.

**Query:**
```sql
SELECT company_id, news_id, published_at
FROM news n1
WHERE (
  SELECT COUNT(*)
  FROM news n2
  WHERE n2.company_id = n1.company_id
    AND (n2.published_at > n1.published_at
         OR (n2.published_at = n1.published_at AND n2.news_id > n1.news_id))
) < 2
ORDER BY company_id ASC, published_at DESC, news_id DESC;
```
**Explanation:** The correlated COUNT counts strictly-newer siblings per company; selecting those with fewer than 2 yields the top-2 rows with a deterministic tie-break.

---

## Q92: Get the second page of the above query using keyset on the minimal (company, published_at, news_id) cursor.

**Query:**
```sql
SELECT company_id, news_id, published_at
FROM news
WHERE company_id = 5
  AND (published_at, news_id) < ('2024-02-14 08:00:00', 312)
ORDER BY published_at DESC, news_id DESC
LIMIT 2;
```
**Explanation:** After reading company 5's two newest, the last row (date, id) becomes the cursor bound for the next two — no OFFSET rescan required.

---

## Q93: Order articles by relevance: full-title match first, then prefix match, then alphabetical.

**Query:**
```sql
SELECT id, title
FROM articles
ORDER BY
  CASE
    WHEN title = 'SQL'            THEN 1
    WHEN title LIKE 'SQL%'        THEN 2
    ELSE 3
  END,
  title ASC;
```
**Explanation:** Layered CASE ranks match quality before falling back to alphabetical order; exact matches cap each relevance tier.

---

## Q94: Sort a nullable numeric column so zeros sort after positives in a business rule.

**Query:**
```sql
SELECT item_id, stock
FROM inventory
ORDER BY
  CASE WHEN stock > 0 THEN 0
       WHEN stock = 0 THEN 1
       ELSE 2
  END ASC,
  stock ASC;
```
**Explanation:** CASE maps stock bands (positive/zero/negative) into a priority key, then the raw value orders within the band — a stock-aware ranking.

---

## Q95: Paginate a feed of a post plus comments using keyset on a composite cursor of posted_on and id.

**Query:**
```sql
SELECT feed_id, posted_on
FROM feed_items
WHERE posted_on < '2024-09-20 00:00:00'
   OR (posted_on = '2024-09-20 00:00:00' AND feed_id > 1000)
ORDER BY posted_on DESC, feed_id DESC
LIMIT 30;
```
**Explanation:** DESC keyset uses `<` for the primary key and shifts the id bound with `>`, preserving exact ordering as the cursor walks backward in time.

---

## Q96: Sort by a nullable date so the most recent come first, the oldest tied NULLs last.

**Query:**
```sql
-- SQL Server
SELECT id, last_login
FROM users
ORDER BY
  CASE WHEN last_login IS NOT NULL THEN 1 ELSE 2 END DESC,
  last_login DESC;
```
**Explanation:** First key pushes non-NULL users (band 1) before NULL (band 2) regardless of date value; second key sorts the real dates the correct direction.

---

## Q97: Fetch the first 10 posts for a feed mixing pinned and non-pinned while retaining keyset feasibility.

**Query:**
```sql
SELECT post_id, pinned, created_at
FROM feed_members
WHERE post_id > 0
ORDER BY pinned DESC, created_at DESC, post_id DESC
LIMIT 10;
```
**Explanation:** The ORDER BY is keyset-compatible: page N replaces `post_id > <last>` while pinned order and recency stay fixed.

---

## Q98: Return each department's highest-paid employee using ordering and a top-N per group pattern.

**Query:**
```sql
SELECT department, first_name, salary
FROM employees e1
WHERE (
  SELECT COUNT(*)
  FROM employees e2
  WHERE e2.department = e1.department
    AND (e2.salary > e1.salary
         OR (e2.salary = e1.salary AND e2.employee_id < e1.employee_id))
) = 0
ORDER BY department ASC;
```
**Explanation:** A self-join subquery counts strictly better-paid employees; zero better-paid means it's the top earner, output ordered by department.

---

## Q99: Implement OFFSET-style pagination in SQLite querying the same table with OFFSET plus a keyset data snapshot.

**Query:**
```sql
-- SQLite
SELECT id, title
FROM articles
WHERE id > :last_cursor
ORDER BY id ASC
LIMIT 25;
```
**Explanation:** A parameterized keyset cursor is the recommended SQLite pattern for stable pagination and avoids OFFSET re-scan; snapshot-free and index-friendly.

---

## Q100: Build a reusable "next page" query for a messaging list that combines two-order keyset and a boolean filter.

**Query:**
```sql
SELECT message_id, sent_at, is_draft
FROM messages
WHERE user_id = :user
  AND NOT is_draft
  AND (sent_at, message_id) < (:cursor_sent_at, :cursor_message_id)
ORDER BY sent_at DESC, message_id DESC
LIMIT 20;
```
**Explanation:** Tuple comparison + boolean predicate + per-user keying yields a parameterizable, cursor-driven page that stays correct on inserts, updates, and deletes.
**Alt1:**
```sql
SELECT message_id, sent_at, is_draft
FROM messages
WHERE user_id = :user
  AND NOT is_draft
  AND (sent_at < :cursor_sent_at
       OR (sent_at = :cursor_sent_at AND message_id < :cursor_message_id))
ORDER BY sent_at DESC, message_id DESC
LIMIT 20;
```
Expanding the row-value cursor into OR predicates keeps the same behavior in every DBMS, at the cost of a longer WHERE clause.

---
