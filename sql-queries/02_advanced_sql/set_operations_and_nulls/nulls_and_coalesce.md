# NULLs and COALESCE in SQL — 100 Interview Q&A

## Q1: Write a query that returns a default value of 0 whenever the bonus column holds NULL.

**Query:**
```sql
SELECT employee_id,
       salary,
       COALESCE(bonus, 0) AS effective_bonus
FROM employees;
```
**Explanation:** COALESCE returns the first non-NULL argument it meets, so a NULL bonus becomes 0 without touching real values.

## Q2: Return the first non-NULL contact method for each customer across the phone, email, and telegram columns.

**Query:**
```sql
SELECT customer_id,
       COALESCE(phone, email, telegram) AS primary_contact
FROM customers;
```
**Explanation:** COALESCE scans left to right and stops at the first non-NULL value it finds.

**Alt1:**
```sql
-- SQL Server
SELECT customer_id,
       ISNULL(ISNULL(phone, email), telegram) AS primary_contact
FROM customers;
```
**Explanation:** SQL Server's ISNULL takes exactly two arguments, so you must nest calls for the same effect.

## Q3: Find every employee who reports to nobody — meaning manager_id was never assigned.

**Query:**
```sql
SELECT employee_id, full_name
FROM employees
WHERE manager_id IS NULL;
```
**Explanation:** You must test missing data with `IS NULL`; `= NULL` is never TRUE.

## Q4: Fix a broken filter that returns no rows at all: `WHERE salary = NULL`.

**Query:**
```sql
SELECT * FROM employees WHERE salary IS NULL;
```
**Explanation:** `salary = NULL` yields UNKNOWN for every row, so the original query is empty no matter how many salaries are missing.

**Alt1:**
```sql
SELECT * FROM employees WHERE NOT (salary IS NOT NULL);
```
**Explanation:** Logically equivalent, but harder to read; prefer the plain `IS NULL`.

## Q5: Prove that `NULL = NULL` evaluates to UNKNOWN, not TRUE.

**Query:**
```sql
-- MySQL / PostgreSQL
SELECT NULL = NULL AS is_equal;
```
**Explanation:** Comparing two unknowns produces UNKNOWN, which every database displays as NULL rather than TRUE.

**Alt1:**
```sql
-- PostgreSQL
SELECT (NULL = NULL) IS NULL AS proves_unknown;  -- true
```
**Explanation:** Checking whether the comparison result "is NULL" confirms it never became TRUE.

## Q6: Show total row count and the number of rows with a missing salary side by side.

**Query:**
```sql
SELECT COUNT(*) AS total_rows,
       COUNT(CASE WHEN salary IS NULL THEN 1 END) AS missing_salary
FROM employees;
```
**Explanation:** COUNT(*) counts physical rows; COUNT(<expression>) only counts results that are not NULL.

## Q7: Return rows where at least one of city, state, or zipcode is missing.

**Query:**
```sql
SELECT * FROM addresses
WHERE city IS NULL
   OR state IS NULL
   OR zipcode IS NULL;
```
**Explanation:** Each `IS NULL` test is independently TRUE/FALSE and the OR combines them.

## Q8: Show users with a display-only column that substitutes 'No City' for a NULL city.

**Query:**
```sql
SELECT name, COALESCE(city, 'No City') AS location
FROM users;
```
**Explanation:** COALESCE swaps the NULL for a literal fallback at display time only.

**Alt1:**
```sql
-- Oracle
SELECT name, NVL(city, 'No City') AS location FROM users;
```
**Explanation:** Oracle's NVL is the two-argument ancestor of COALESCE with the same end result.

## Q9: Using Oracle syntax, echo a dash wherever the phone column holds NULL.

**Query:**
```sql
-- Oracle
SELECT customer_id, NVL(phone, '-') AS phone_display
FROM customers;
```
**Explanation:** NVL returns its first argument unless it is NULL, in which case it returns the second.

## Q10: Create a flag column that is 1 when a user has no city and 0 otherwise.

**Query:**
```sql
SELECT name,
       CASE WHEN city IS NULL THEN 1 ELSE 0 END AS missing_city
FROM users;
```
**Explanation:** CASE tests `IS NULL` explicitly, so the flag is always a definite 1 or 0.

**Alt1:**
```sql
-- PostgreSQL
SELECT name, (city IS NULL)::int AS missing_city FROM users;
```
**Explanation:** Casting the boolean result of `IS NULL` to int yields the same 1/0 flag.

## Q11: Show that negating an UNKNOWN result is still UNKNOWN, never TRUE or FALSE.

**Query:**
```sql
SELECT * FROM orders
WHERE NOT (paid_at = NULL);
```
**Explanation:** `paid_at = NULL` is UNKNOWN per row, and `NOT UNKNOWN` is still UNKNOWN, so the filter keeps nothing.

## Q12: Write a filter that is TRUE only when a product is active AND still on sale, and explain how AND treats the combination.

**Query:**
```sql
SELECT * FROM products
WHERE active = 1
  AND disposal_date IS NULL;
```
**Explanation:** If the product is active (TRUE) and on sale (TRUE) the row survives; had you written `disposal_date = NULL`, the right side would be UNKNOWN and `TRUE AND UNKNOWN = UNKNOWN` would discard valid rows.

## Q13: Demonstrate that `delivered = 5 OR delivered IS NULL` keeps NULL-delivery rows while `delivered = 5 OR delivered = NULL` drops them.

**Query:**
```sql
SELECT order_id FROM orders
WHERE delivered = 5 OR delivered IS NULL;
```
**Explanation:** `delivered = NULL` is UNKNOWN, and `UNKNOWN OR TRUE` only becomes TRUE through the IS NULL branch — OR, like AND, obeys the three-valued truth table.

**Alt1:**
```sql
SELECT order_id FROM orders
WHERE COALESCE(delivered, -1) IN (5, -1);
```
**Explanation:** Folding NULL into a sentinel lets ordinary equality and IN handle the missing rows.

## Q14: Resolve transactions to a category with CASE, then keep only rows whose resolution is known.

**Query:**
```sql
SELECT * FROM (
  SELECT t.*,
         CASE WHEN t.category IS NULL THEN NULL
              ELSE 'C-' || t.category END AS resolved
  FROM transactions t
) x
WHERE x.resolved IS NOT NULL;
```
**Explanation:** The inner CASE can still emit NULL, so the outer predicate filters unresolved rows out.

## Q15: Substitute 'N/A' for a NULL middle initial using MySQL-compatible syntax.

**Query:**
```sql
-- MySQL / SQLite
SELECT employee_id, IFNULL(middle_initial, 'N/A') AS mi
FROM employees;
```
**Explanation:** IFNULL is the two-argument MySQL/SQLite shorthand for a NULL fallback.

**Alt1:**
```sql
SELECT employee_id, COALESCE(middle_initial, 'N/A') AS mi FROM employees;
```
**Explanation:** COALESCE delivers the same result portably.

## Q16: Show 'Unknown' in place of NULL nicknames.

**Query:**
```sql
SELECT user_id, COALESCE(nick, 'Unknown') AS display_name
FROM users;
```
**Explanation:** NULL nicknames are replaced only for display; the stored NULL is untouched.

**Alt1:**
```sql
-- SQL Server
SELECT user_id, ISNULL(nick, 'Unknown') AS display_name FROM users;
```
**Explanation:** ISNULL is SQL Server's two-argument form of the same idea.

## Q17: Return employees whose security_clearance was never stored.

**Query:**
```sql
SELECT * FROM employees WHERE security_clearance IS NULL;
```
**Explanation:** "Missing" is detected with `IS NULL` because no value can equal its own absence.

## Q18: List shipments that have a valid order_date but no ship_date yet.

**Query:**
```sql
SELECT shipment_id FROM shipments
WHERE order_date IS NOT NULL
  AND ship_date IS NULL;
```
**Explanation:** Each `IS (NOT) NULL` test is TRUE or FALSE — never UNKNOWN — so the AND composes cleanly.

## Q19: Return NULL wherever the attempts column holds 0, while keeping other values unchanged.

**Query:**
```sql
SELECT test_id, NULLIF(attempts, 0) AS clean_attempts
FROM test_runs;
```
**Explanation:** NULLIF(a, b) yields NULL when a equals b, otherwise a — a compact way to blank a sentinel value.

## Q20: Rewrite this CASE fallback with COALESCE: `CASE WHEN rating IS NULL THEN 'NR' ELSE rating END`.

**Query:**
```sql
SELECT movie_id, COALESCE(rating, 'NR') AS rating_display
FROM movies;
```
**Explanation:** Both forms output 'NR' for NULL; COALESCE is the compact, portable equivalent.

## Q21: Use COALESCE inside WHERE so that blank and NULL notes both match a filter for empty notes.

**Query:**
```sql
SELECT * FROM contacts
WHERE COALESCE(note, '') = '';
```
**Explanation:** Folding NULL into '' lets one ordinary equality cover both the missing and the blank case.

**Alt1:**
```sql
-- SQL Server
SELECT * FROM contacts WHERE ISNULL(note, '') = '';
```
**Explanation:** ISNULL is the SQL Server equivalent of the fold.

## Q22: A scalar subquery looks up each employee's manager; the lookup is NULL for unrecorded managers. Show how a `= (subquery)` silently drops those rows, then fix it.

**Query:**
```sql
-- drops top-level staff: NULL = NULL is UNKNOWN
SELECT e.employee_id
FROM employees e
WHERE e.manager_id = (SELECT m.id FROM managers m WHERE m.employee_id = e.manager_id);
```
**Explanation:** When no manager row matches, the subquery is NULL and the comparison is UNKNOWN, so the equation drops the employee.

**Alt1:**
```sql
SELECT e.employee_id
FROM employees e
WHERE COALESCE((SELECT m.id FROM managers m
                WHERE m.employee_id = e.manager_id), -1)
      = COALESCE(e.manager_id, -1);
```
**Explanation:** Both sides become -1 when missing, so NULLs compare equal and the top-level rows survive; a plain `IS NULL` branch is usually clearer.

## Q23: Bucket movie ratings into 'High', 'Mid', 'Low', and 'Unrated', treating NULL as its own bucket.

**Query:**
```sql
SELECT title,
       CASE WHEN rating IS NULL THEN 'Unrated'
            WHEN rating >= 4    THEN 'High'
            WHEN rating >= 2    THEN 'Mid'
            ELSE 'Low' END AS band
FROM movies;
```
**Explanation:** The IS NULL branch runs first, so NULL ratings never fall through into `<`/`>=` comparisons.

## Q24: Write both filters — the wrong one that finds nothing and the right one that finds users with no name — to make the `= NULL` vs `IS NULL` difference visible.

**Query:**
```sql
SELECT * FROM users WHERE name = NULL;    -- always empty
SELECT * FROM users WHERE name IS NULL;   -- users with no name
```
**Explanation:** String NULLs behave exactly like numeric ones: `=` is UNKNOWN, `IS NULL` is TRUE.

## Q25: Build a "first_name from city" profile string, showing 'Nowhere' when the city is missing, without the concatenation becoming NULL.

**Query:**
```sql
SELECT first_name || ' from ' || COALESCE(city, 'Nowhere') AS profile
FROM users;
```
**Explanation:** COALESCE runs before the concat, so the `||` operator never touches a NULL operand (works on PostgreSQL, Oracle, SQL Server).

**Alt1:**
```sql
-- MySQL
SELECT CONCAT(first_name, ' from ', IFNULL(city, 'Nowhere')) AS profile FROM users;
```
**Explanation:** MySQL's CONCAT silently drops NULL arguments, so the city must be pre-folded with IFNULL.

## Q26: Show how `salary + bonus` propagates NULL for employees who have no bonus.

**Query:**
```sql
SELECT employee_id, salary, bonus,
       salary + bonus AS total_pay
FROM employees;
```
**Explanation:** Any arithmetic with NULL yields NULL, so a missing bonus poisons the whole total instead of defaulting to salary + 0.

## Q27: Rewrite the Q26 query so total pay falls back to salary when bonus is NULL.

**Query:**
```sql
SELECT employee_id,
       salary + COALESCE(bonus, 0) AS total_pay
FROM employees;
```
**Explanation:** COALESCE supplies 0 before the addition, so NULL never enters the arithmetic.

**Alt1:**
```sql
-- SQL Server
SELECT employee_id, salary + ISNULL(bonus, 0) AS total_pay FROM employees;
```
**Explanation:** ISNULL is the SQL Server two-argument alternative for the same protection.

## Q28: Demonstrate that SUM ignores NULL contributions by comparing SUM(bonus) with a version that treats missing bonuses as zero.

**Query:**
```sql
SELECT SUM(bonus)             AS sum_skips_null,
       SUM(COALESCE(bonus, 0)) AS sum_includes_zero
FROM employees;
```
**Explanation:** Aggregates skip NULL inputs, so both expressions agree — a sparse column never corrupts a SUM.

## Q29: Explain the difference between COUNT(*) and COUNT(salary) and show both in one query.

**Query:**
```sql
SELECT COUNT(*)       AS rows_total,
       COUNT(salary)  AS rows_with_salary
FROM employees;
```
**Explanation:** COUNT(*) counts every physical row; COUNT(column) ignores rows where that column is NULL.

## Q30: Values [10, NULL, 20] are on the score column — write the query that returns AVG = 15 and explain why it isn't 10.

**Query:**
```sql
SELECT AVG(score) AS avg_score
FROM (SELECT 10 AS score UNION ALL SELECT NULL UNION ALL SELECT 20) s;
```
**Explanation:** AVG ignores the NULL and averages only 10 and 20 to 15, rather than dividing by all three rows.

## Q31: Show that MIN and MAX ignore NULL values and only return NULL when every input is NULL.

**Query:**
```sql
SELECT MIN(shoe_size) AS min_size, MAX(shoe_size) AS max_size
FROM inventory
WHERE category = 'kids';
```
**Explanation:** MIN/MAX skip NULLs; the result is NULL only when the group holds no non-NULL value at all.

## Q32: Protect a click-through-rate division so a missing or zero views count cannot raise an error.

**Query:**
```sql
SELECT page_id,
       clicks * 1.0 / NULLIF(views, 0) AS ctr
FROM pages;
```
**Explanation:** NULLIF turns 0 into NULL, and any value divided by NULL is NULL — so the ratio degrades gracefully instead of erroring.

## Q33: Compute a running total over a ledger, treating a missing amount as 0 so the running value never blanks out.

**Query:**
```sql
-- PostgreSQL
SELECT id,
       amount,
       SUM(COALESCE(amount, 0)) OVER (ORDER BY id) AS running_total
FROM ledger;
```
**Explanation:** Window aggregates skip NULLs, and the explicit COALESCE makes the "missing means 0" policy visible to the reader.

**Alt1:**
```sql
-- MySQL 8.0+
SELECT id, amount,
       SUM(IFNULL(amount, 0)) OVER (ORDER BY id) AS running_total
FROM ledger;
```
**Explanation:** IFNULL is MySQL's two-argument spelling of the same protection.

## Q34: In a region whose revenue column holds only NULLs, show that COUNT gives 0 while SUM gives NULL.

**Query:**
```sql
SELECT region,
       SUM(revenue)   AS sum_revenue,
       COUNT(revenue) AS cnt_revenue,
       COUNT(*)       AS cnt_rows
FROM sales
GROUP BY region;
```
**Explanation:** For an all-NULL group SUM is NULL and COUNT(revenue) is 0, yet COUNT(*) still reports the physical rows that carry those NULLs.

## Q35: Show that BETWEEN with a NULL upper boundary evaluates to UNKNOWN and drops every row.

**Query:**
```sql
SELECT * FROM products
WHERE price BETWEEN 10 AND NULL;
```
**Explanation:** `BETWEEN 10 AND NULL` expands to `price >= 10 AND price <= NULL`; the second comparison is UNKNOWN, and UNKNOWN AND anything is UNKNOWN, so no row passes.

## Q36: Why does `priority IN (1, NULL)` only ever match value 1 — demonstrate it.

**Query:**
```sql
SELECT order_id FROM orders
WHERE priority IN (1, NULL);
```
**Explanation:** IN expands to `priority = 1 OR priority = NULL`; the NULL branch is UNKNOWN, and `TRUE OR UNKNOWN = TRUE` only saves rows that already matched the first branch.

**Alt1:**
```sql
SELECT order_id FROM orders
WHERE priority = 1 OR priority IS NULL;
```
**Explanation:** To actually include the NULL-priority rows you must add the explict IS NULL test.

## Q37: Reproduce the classic NOT IN bug — a NULL inside the subquery results and the whole outer query returns nothing.

**Query:**
```sql
SELECT * FROM customers
WHERE id NOT IN (SELECT customer_id FROM orders);
```
**Explanation:** If any order has a NULL customer_id, NOT IN becomes `id <> 1 AND ... AND id <> NULL`; the last term is UNKNOWN and UNKNOWN AND TRUE is UNKNOWN, so the predicate is never TRUE — the query empties.

## Q38: Fix the Q37 query so it behaves correctly even when the subquery contains NULL.

**Query:**
```sql
SELECT c.* FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```
**Explanation:** NOT EXISTS tests presence per outer row; a NULL customer_id can never create a matching row, so nothing is wrongly dropped.

**Alt1:**
```sql
SELECT * FROM customers
WHERE id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL);
```
**Explanation:** Scrubbing NULLs out of the subquery neutralizes the pitfall, though NOT EXISTS is the more idiomatic fix.

## Q39: Without any hint, where do NULLs sort in MySQL, PostgreSQL, and SQL Server on an ascending query?

**Query:**
```sql
SELECT name, deleted_at FROM users ORDER BY deleted_at;
```
**Explanation:** Defaults differ per dialect: MySQL and SQL Server put NULLs first on ASC, PostgreSQL puts them last; on DESC the positions flip — never rely on the default.

## Q40: Portably force NULL names to the bottom of an ascending sorted list using COALESCE in ORDER BY.

**Query:**
```sql
SELECT name FROM users
ORDER BY COALESCE(name, '~') ASC;
```
**Explanation:** Replacing NULL with a high sort key approximates "NULLs last" on any engine.

**Alt1:**
```sql
-- PostgreSQL / Oracle / SQL Server 2022+
SELECT name FROM users ORDER BY name ASC NULLS LAST;
```
**Explanation:** Native ANSI NULLS LAST is the cleanest spelling where it is supported.

## Q41: Sort employees by commission so that employees without a recorded commission appear first in the list.

**Query:**
```sql
-- PostgreSQL / Oracle / SQL Server 2022+
SELECT * FROM employees ORDER BY commission ASC NULLS FIRST;
```
**Explanation:** NULLS FIRST overrides the dialect default so commission-less rows lead regardless of sort direction.

**Alt1:**
```sql
SELECT * FROM employees
ORDER BY CASE WHEN commission IS NULL THEN 0 ELSE 1 END, commission;
```
**Explanation:** A numeric rank key makes the ordering explicit and portable across every engine.

## Q42: Show that DISTINCT collapses all NULL department values into a single output row.

**Query:**
```sql
SELECT DISTINCT department FROM employees;
```
**Explanation:** DISTINCT treats every NULL as equal for grouping purposes, so all the missing departments render as one NULL row.

## Q43: GROUP BY department and show that employees with a missing department all land in a single NULL bucket.

**Query:**
```sql
SELECT department, COUNT(*) AS staff
FROM employees
GROUP BY department;
```
**Explanation:** GROUP BY groups missing values together — NULL forms one group whose label is NULL.

## Q44: A report wants departments whose total sales exceed 1000; explain why a department summing to NULL is excluded, then include it only when it has real data.

**Query:**
```sql
SELECT department, SUM(amount) AS total
FROM sales
GROUP BY department
HAVING SUM(amount) > 1000;
```
**Explanation:** A group with no non-NULL amounts yields NULL for SUM; `NULL > 1000` is UNKNOWN so HAVING discards the group.

**Alt1:**
```sql
SELECT department, SUM(amount) AS total
FROM sales
GROUP BY department
HAVING COALESCE(SUM(amount), 0) > 1000;
```
**Explanation:** Folding NULL to 0 turns the comparison from UNKNOWN into FALSE, changing which groups survive the HAVING clause.

## Q45: Show that a UNIQUE constraint rejects duplicate values yet cheerfully allows many NULLs.

**Query:**
```sql
CREATE UNIQUE INDEX idx_coupon ON coupons (code);
-- PostgreSQL / MySQL / SQLite: these two NULLs both succeed...
INSERT INTO coupons (code) VALUES (NULL), (NULL);
-- ...while the duplicate 'A' below fails
INSERT INTO coupons (code) VALUES ('A'), ('A');
```
**Explanation:** In most engines NULLs are not considered equal to each other for uniqueness, so a UNIQUE index tolerates unlimited missing values.

**Alt1:**
```sql
-- PostgreSQL: unique only over the non-NULL rows
CREATE UNIQUE INDEX idx_coupon_nn ON coupons (code) WHERE code IS NOT NULL;
```
**Explanation:** A partial index makes the "non-NULLs must be unique" rule explicit and documented.

## Q46: COALESCE-fill a LEFT JOIN so missing right-side values become 0 for numbers and a placeholder for labels.

**Query:**
```sql
SELECT o.id,
       COALESCE(p.name, 'Returned') AS product,
       COALESCE(o.total, 0)         AS total
FROM orders o
LEFT JOIN products p ON p.id = o.product_id;
```
**Explanation:** LEFT JOIN leaves NULLs on the unmatched side; COALESCE substitutes the display and arithmetic fallbacks where they appear.

**Alt1:**
```sql
-- Oracle
SELECT o.id,
       NVL(p.name, 'Returned') AS product,
       NVL(o.total, 0)         AS total
FROM orders o
LEFT JOIN products p ON p.id = o.product_id;
```
**Explanation:** Oracle's NVL fills the same gaps with two-argument simplicity.

## Q47: Explain why a JOIN on a NULL key never produces a match, and demonstrate it.

**Query:**
```sql
SELECT e.name, m.name AS manager
FROM employees e
JOIN employees m ON m.id = e.manager_id;
```
**Explanation:** Top-level staff have a NULL manager_id; `m.id = NULL` is UNKNOWN so those rows never satisfy the join predicate.

**Alt1:**
```sql
SELECT e.name, m.name AS manager
FROM employees e
LEFT JOIN employees m ON m.id = e.manager_id;
```
**Explanation:** LEFT JOIN keeps the NULL-key rows, leaving manager NULL for you to COALESCE afterward.

## Q48: Show that COUNT(DISTINCT column) skips NULL values, returning 2 for inputs ['A', NULL, 'A'].

**Query:**
```sql
SELECT COUNT(DISTINCT color) AS n_colors
FROM (SELECT 'A' AS color UNION ALL SELECT NULL UNION ALL SELECT 'A') t;
```
**Explanation:** DISTINCT collapses the duplicate 'A' and drops the NULL entirely, leaving a count of 2.

## Q49: Use COUNT over a COALESCE-wrapped metric so rows whose value is stored NULL still get counted.

**Query:**
```sql
SELECT COUNT(COALESCE(impressions, 0)) AS row_count
FROM ad_server;
```
**Explanation:** COALESCE emits a non-NULL 0 for every row, so COUNT sees a value in all of them — identical to COUNT(*).

**Alt1:**
```sql
SELECT COUNT(*) AS row_count FROM ad_server;
```
**Explanation:** When you simply want every row counted, COUNT(*) is the clearer spelling.

## Q50: Filter rows whose nickname is either NULL or an empty string, portably across MySQL and PostgreSQL.

**Query:**
```sql
SELECT * FROM users
WHERE nick IS NULL OR nick = '';
```
**Explanation:** NULL and '' are different things — absence versus an empty value — so both predicates are required.

**Alt1:**
```sql
SELECT * FROM users WHERE COALESCE(nick, '') = '';
```
**Explanation:** Coalescing NULL to '' lets one equality cover both cases.

## Q51: Compare ISNULL (SQL Server) with COALESCE when picking the first non-NULL of three columns.

**Query:**
```sql
-- SQL Server
SELECT ISNULL(ISNULL(a, b), c) AS first_value
FROM data_rows;
```
**Explanation:** ISNULL accepts exactly two arguments, so three columns force nested calls that read right-to-left.

**Alt1:**
```sql
-- portable
SELECT COALESCE(a, b, c) AS first_value FROM data_rows;
```
**Explanation:** COALESCE takes any number of arguments and stops at the first non-NULL.

## Q52: In Oracle, both NVL and COALESCE fill NULLs — when would you reach for one over the other?

**Query:**
```sql
-- Oracle
SELECT employee_id,
       NVL(middle_name, '') AS mi
FROM employees;
```
**Explanation:** NVL is a two-argument special case; for a single fallback it is the most direct Oracle idiom.

**Alt1:**
```sql
-- Oracle
SELECT employee_id,
       COALESCE(first_choice, second_choice, 'FALLBACK') AS chosen
FROM employees;
```
**Explanation:** COALESCE shines when there are several ordered fallbacks because it accepts them all at once.

## Q53: Show IFNULL (MySQL) and COALESCE achieving the same fallback result but note the type-casting caveat.

**Query:**
```sql
-- MySQL
SELECT IFNULL(price, 0) AS fallback_price FROM products;
```
**Explanation:** IFNULL is MySQL's two-argument fill; both functions return the first non-NULL argument.

**Alt1:**
```sql
-- MySQL
SELECT COALESCE(price, 0) AS fallback_price FROM products;
```
**Explanation:** Identical result here; prefer COALESCE when the query may be ported because its argument types must unify under a common type.

## Q54: NULLIF supplies no fallback — it returns NULL. Give a realistic use: blanking a sentinel value before aggregation.

**Query:**
```sql
SELECT AVG(NULLIF(age_years, -1)) AS avg_age
FROM census;
```
**Explanation:** The -1 sentinel becomes NULL and AVG ignores it, so a coded "unknown age" no longer drags the mean toward -1.

## Q55: Show nested COALESCE resolving left to right and give its explicit CASE equivalent.

**Query:**
```sql
SELECT COALESCE(nick, first_name, 'Unknown') AS name FROM users;
```
**Explanation:** The first non-NULL among nick, first_name, and the literal wins; all-NULL rows print 'Unknown'.

**Alt1:**
```sql
SELECT CASE WHEN nick        IS NOT NULL THEN nick
            WHEN first_name  IS NOT NULL THEN first_name
            ELSE 'Unknown' END AS name
FROM users;
```
**Explanation:** CASE spells out the same left-to-right precedence when a function call feels too terse.

## Q56: COALESCE is not guaranteed to short-circuit on every engine — give an example that is safe on PostgreSQL but can error on SQL Server.

**Query:**
```sql
-- PostgreSQL / MySQL: usually fine, name wins before 1/0 is reached
SELECT COALESCE(name, 1 / 0) FROM users;
```
**Explanation:** Engines like PostgreSQL evaluate arguments lazily; SQL Server may evaluate the division regardless of the branch taken.

**Alt1:**
```sql
-- SQL Server: may raise "Divide by zero" during evaluation
SELECT COALESCE(name, 1 / 0) FROM users;
```
**Explanation:** Do not rely on short-circuiting — fold values safely before the expression or avoid side-effecting fallbacks.

## Q57: Show that PostgreSQL's `||` turns `'Alice' || NULL` into NULL, not 'Alice'.

**Query:**
```sql
-- PostgreSQL
SELECT 'Alice' || NULL AS result;
```
**Explanation:** PostgreSQL's `||` is strict — any NULL operand propagates and the whole expression becomes NULL.

**Alt1:**
```sql
-- PostgreSQL
SELECT 'Alice' || COALESCE(NULL, '') AS result;  -- 'Alice'
```
**Explanation:** Pre-folding NULL to '' with COALESCE keeps the concatenation meaningful.

## Q58: Contrast MySQL's CONCAT, which silently drops NULL arguments, with the strict `||` behavior on other engines.

**Query:**
```sql
-- MySQL
SELECT CONCAT('Alice', NULL) AS result;   -- 'Alice', the NULL vanishes
```
**Explanation:** MySQL's CONCAT skips NULL arguments entirely, while the `||` operator of PostgreSQL propagates them.

**Alt1:**
```sql
-- Oracle
SELECT 'Alice' || NULL AS result FROM dual;  -- 'Alice'
```
**Explanation:** Oracle's `||` conveniently degrades NULL to an empty string — behavior differs by vendor, so verify rather than assume.

## Q59: Write inserts that store '' and NULL in the same column, then filters that prove the two live in different buckets.

**Query:**
```sql
INSERT INTO users (name) VALUES ('');
INSERT INTO users (name) VALUES (NULL);

SELECT COUNT(*) AS empty_strings FROM users WHERE name = '';    -- 1
SELECT COUNT(*) AS null_names     FROM users WHERE name IS NULL; -- 1
```
**Explanation:** '' is a zero-length value while NULL is the absence of a value; the two predicates are mutually exclusive.

## Q60: LEFT JOIN a rating list and use COALESCE so products without ratings report a total of 0 instead of NULL.

**Query:**
```sql
SELECT p.id,
       COALESCE(SUM(r.score), 0) AS total_score
FROM products p
LEFT JOIN ratings r ON r.product_id = p.id
GROUP BY p.id;
```
**Explanation:** Products with no ratings form an all-NULL SUM group; COALESCE turns that NULL total into 0.

**Alt1:**
```sql
-- Oracle
SELECT p.id, NVL(SUM(r.score), 0) AS total_score
FROM products p LEFT JOIN ratings r ON r.product_id = p.id
GROUP BY p.id;
```
**Explanation:** NVL fills the same all-NULL aggregate result on Oracle.

## Q61: Show the ISNULL (SQL Server) limitations: it takes exactly two arguments and may evaluate them eagerly.

**Query:**
```sql
-- SQL Server
SELECT ISNULL(a, b) FROM t;                  -- two arguments only
SELECT ISNULL(ISNULL(a, b), c) FROM t;       -- nesting required for a third column
```
**Explanation:** One missing argument breaks the call, and unlike COALESCE, ISNULL arguments in some plans are all evaluated — plan around that.

## Q62: Explain the COALESCE type-coercion gotcha when mixing an integer column with a text fallback, and show the safe spelling.

**Query:**
```sql
-- PostgreSQL
SELECT COALESCE(visits, 'unknown') AS visits FROM analytics;  -- likely hits a casts conflict
```
**Explanation:** COALESCE must resolve one common type for all its arguments; an int column and a text literal may refuse to unify.

**Alt1:**
```sql
SELECT COALESCE(visits, 0) AS visits FROM analytics;  -- int + int, no surprise casts
```
**Explanation:** Keeping fallback types consistent sidesteps coercion errors entirely.

## Q63: Demonstrate that AND short-circuits on FALSE: `WHERE 1 = 0 AND flag IS NULL` must return nothing even when flag is NULL.

**Query:**
```sql
SELECT * FROM accounts WHERE 1 = 0 AND flag IS NULL;
```
**Explanation:** `FALSE AND anything` is FALSE — including `FALSE AND UNKNOWN` — so no row can survive, which is exactly the AND truth table at work.

## Q64: What does `WHERE NULL = 0` return and why — demonstrate with a count.

**Query:**
```sql
SELECT COUNT(*) AS matches FROM accounts WHERE NULL = 0;
```
**Explanation:** `NULL = 0` is UNKNOWN for every row and WHERE keeps only TRUE rows, so the count is 0.

## Q65: Two nullable columns, home_phone and work_phone — return customers whose phones are "equal", including when both are NULL.

**Query:**
```sql
SELECT * FROM customers
WHERE home_phone = work_phone
   OR (home_phone IS NULL AND work_phone IS NULL);
```
**Explanation:** `NULL = NULL` is UNKNOWN, so the extra both-NULL branch is required for a real NULL-safe equality.

**Alt1:**
```sql
-- PostgreSQL / SQLite
SELECT * FROM customers WHERE home_phone IS NOT DISTINCT FROM work_phone;
```
**Explanation:** `IS NOT DISTINCT FROM` treats NULL as equal to NULL natively, expressing the same rule in one operator.

## Q66: Introduce `IS NOT DISTINCT FROM` and use it for a NULL-safe match on an optional email address.

**Query:**
```sql
-- PostgreSQL
SELECT * FROM signups
WHERE email IS NOT DISTINCT FROM contact_email;
```
**Explanation:** It is TRUE when both values are NULL and when they are equal; engines without it fall back to the OR-IS NULL idiom from Q65.

## Q67: List customers where ALL of the address columns are missing — fully anonymous rows.

**Query:**
```sql
SELECT * FROM customers
WHERE street IS NULL AND city IS NULL AND zip IS NULL;
```
**Explanation:** AND demands every IS NULL test be TRUE, which happens only when none of the three fields is present.

## Q68: Group subscribers by country, pushing missing countries into an 'Unknown' label so the report key is never NULL.

**Query:**
```sql
SELECT COALESCE(country, 'Unknown') AS region,
       COUNT(*) AS subscribers
FROM subscriber_list
GROUP BY COALESCE(country, 'Unknown');
```
**Explanation:** Grouping on the COALESCE result both labels the NULL bucket and keeps it logically separate from real countries.

## Q69: Rank players while moving NULL scores to the bottom, expressed inside a window function.

**Query:**
```sql
-- PostgreSQL / Oracle
SELECT player_id,
       RANK() OVER (ORDER BY score DESC NULLS LAST) AS rnk
FROM scores;
```
**Explanation:** NULLS LAST governs window ordering exactly as it does a plain ORDER BY, so unknown scores never top the ranking.

## Q70: Fill the gap LAG leaves on the first row by falling back to the row's own price.

**Query:**
```sql
SELECT day_id,
       price,
       COALESCE(LAG(price) OVER (ORDER BY day_id), price) AS prev_price
FROM prices;
```
**Explanation:** LAG returns NULL before the first row exists; COALESCE substitutes the row's own price there.

**Alt1:**
```sql
-- SQL Server
SELECT day_id, price,
       ISNULL(LAG(price) OVER (ORDER BY day_id), price) AS prev_price
FROM prices;
```
**Explanation:** ISNULL is SQL Server's equivalent two-argument fill for the same first-row gap.

## Q71: Pivot monthly revenue into month columns and turn empty cells into 0.

**Query:**
```sql
SELECT product_id,
       COALESCE(SUM(CASE WHEN month = 1 THEN revenue END), 0) AS jan,
       COALESCE(SUM(CASE WHEN month = 2 THEN revenue END), 0) AS feb
FROM sales
GROUP BY product_id;
```
**Explanation:** CASE emits NULL for months that don't match, SUM skips them, and COALESCE converts the empty totals into zeros.

**Alt1:**
```sql
-- SQL Server
SELECT product_id,
       ISNULL([1], 0) AS jan,
       ISNULL([2], 0) AS feb
FROM sales
PIVOT (SUM(revenue) FOR month IN ([1], [2])) AS pvt;
```
**Explanation:** A native PIVOT leaves NULL in missing cells, and ISNULL repaints them as 0.

## Q72: Prevent duplicate emails while still allowing any number of NULLs, using a partial unique index.

**Query:**
```sql
-- PostgreSQL / SQLite
CREATE UNIQUE INDEX uq_email ON members (email) WHERE email IS NOT NULL;
```
**Explanation:** The WHERE clause limits the index to rows that actually carry an email, so missing emails never collide with each other.

**Alt1:**
```sql
-- Oracle
CREATE UNIQUE INDEX uq_email ON members (CASE WHEN email IS NULL THEN NULL ELSE email END);
```
**Explanation:** Oracle lacks partial indexes, so a function on the column converts NULLs to all-identical NULL index entries that are ignored by uniqueness.

## Q73: Explain how a B-tree index interacts with the predicate `WHERE manager_id IS NULL`.

**Query:**
```sql
CREATE INDEX idx_mgr ON employees (manager_id);
SELECT * FROM employees WHERE manager_id IS NULL;
```
**Explanation:** A B-tree can store and scan NULL entries, but engines may still prefer a full scan for sparse NULL predicates; writing `IS NULL` (never `= NULL`) at least keeps index use possible.

## Q74: Emulate boolean columns from a nullable field — count present vs missing bios with COUNT and CASE.

**Query:**
```sql
SELECT COUNT(CASE WHEN bio IS NULL THEN 1 END)     AS missing_bio,
       COUNT(CASE WHEN bio IS NOT NULL THEN 1 END) AS present_bio
FROM profiles;
```
**Explanation:** Each CASE yields a non-NULL 1 only for matching rows, so COUNT tallies exactly that branch's rows.

## Q75: Join two tables on nullable keys so NULL matches NULL, via COALESCE on both sides — and name the trade-off.

**Query:**
```sql
-- PostgreSQL / MySQL
SELECT a.*, b.*
FROM audit a
JOIN ledger b
  ON COALESCE(a.txn_ref, '') = COALESCE(b.txn_ref, '');
```
**Explanation:** Coalescing both sides to a sentinel lets NULL collide with NULL, but a real '' on one side could falsely match — prefer the explicit IS NULL OR-form or `IS NOT DISTINCT FROM` when false matches are unacceptable.

## Q76: Diagnose why switching NOT IN to NOT EXISTS changes the returned row count when the subquery contains NULLs.

**Query:**
```sql
SELECT COUNT(*) AS filtered_out
FROM customers
WHERE id NOT IN (SELECT customer_id FROM orders);
```

**Query:**
```sql
SELECT COUNT(*) AS kept
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```
**Explanation:** NOT IN empties out the moment its subquery list touches NULL; NOT EXISTS compares per row and keeps every customer whose orders never match.

**Alt1:**
```sql
SELECT COUNT(*) AS kept
FROM customers
WHERE id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL);
```
**Explanation:** Scrubbing NULLs from the subquery restores correct NOT IN behavior, though NOT EXISTS remains the clearer intent.

## Q77: Reconstruct the three-valued-logic AND truth table with a single query.

**Query:**
```sql
-- PostgreSQL
SELECT a, b,
       (a AND b)::text AS "a AND b"
FROM (VALUES
  (TRUE, TRUE),    (TRUE, NULL),    (TRUE, FALSE),
  (NULL, TRUE),    (NULL, NULL),    (NULL, FALSE),
  (FALSE, TRUE),   (FALSE, NULL),   (FALSE, FALSE)
) AS t(a, b);
```
**Explanation:** The matrix prints TRUE/TRUE/FALSE for TRUE rows, TRUE/NULL/FALSE for NULL rows, and all FALSE for FALSE rows — proof that `TRUE AND UNKNOWN` is UNKNOWN while `FALSE AND UNKNOWN` is FALSE.

**Alt1:**
```sql
-- MySQL
SELECT a, b, (a AND b) AS "a AND b"
FROM (VALUES ROW(TRUE,TRUE), ROW(TRUE,NULL), ROW(TRUE,FALSE),
             ROW(NULL,TRUE), ROW(NULL,NULL), ROW(NULL,FALSE),
             ROW(FALSE,TRUE), ROW(FALSE,NULL), ROW(FALSE,FALSE)) t(a,b);
```
**Explanation:** MySQL renders the same table, with UNKNOWN shown as NULL.

## Q78: Compute a click rate that yields 0 — neither an error nor NULL — when a page had zero views.

**Query:**
```sql
SELECT page_id,
       COALESCE(clicks * 1.0 / NULLIF(views, 0), 0) AS ctr
FROM analytics;
```
**Explanation:** NULLIF maps 0 views to NULL, the division turns NULL, and COALESCE converts that NULL into the 0 fallback — an error-free, NULL-free ratio.

## Q79: Normalize a text column so empty strings become NULL.

**Query:**
```sql
SELECT customer_id, NULLIF(email, '') AS normalized_email
FROM customers;
```
**Explanation:** NULLIF swaps '' for NULL in the output, matching the common convention that "no email is stored as NULL".

**Alt1:**
```sql
SELECT customer_id, COALESCE(email, '') AS stored_email
FROM customers;
```
**Explanation:** The reverse direction treats NULL as '' — choose one policy and apply it consistently.

## Q80: In one expression, strip the -1 sentinel from an age field and then give missing ages a display fallback of 0.

**Query:**
```sql
SELECT user_id,
       COALESCE(NULLIF(age_years, -1), 0) AS clean_age
FROM users;
```
**Explanation:** Piping NULLIF into COALESCE first blanks the -1 sentinel, then supplies 0 for anything still NULL.

## Q81: Write a CASE that has an explicit missing-value branch and explain the NULL leak when you omit it.

**Query:**
```sql
SELECT n,
       CASE WHEN n IS NULL THEN 'missing'
            WHEN n % 2 = 0 THEN 'even'
            ELSE 'odd' END AS parity
FROM numbers;
```
**Explanation:** When n is NULL, `n % 2` is NULL, `NULL = 0` is UNKNOWN, so the CASE falls into ELSE 'odd' — the first IS NULL branch prevents that wrong label.

## Q82: Show how PostgreSQL's bool_and/bool_or treat NULL entries when aggregating a boolean column.

**Query:**
```sql
-- PostgreSQL
SELECT bool_and(flag) AS all_on,
       bool_or(flag)  AS any_on
FROM (VALUES (TRUE), (FALSE), (NULL)) t(flag);
```
**Explanation:** bool_and is FALSE if any input is FALSE (NULL is ignored, not treated as FALSE); bool_or is TRUE if any input is TRUE — both only return NULL when every input is NULL.

## Q83: Count distinct badges per team and use HAVING to require at least two, showing how NULL badges vanish from the tally.

**Query:**
```sql
SELECT team_id, COUNT(DISTINCT badge) AS n_badges
FROM roster
GROUP BY team_id
HAVING COUNT(DISTINCT badge) >= 2;
```
**Explanation:** COUNT(DISTINCT badge) drops both duplicate and NULL badges, so a team whose only badge is NULL scores 0 and misses the HAVING bar.

## Q84: Deduplicate event-log rows whose natural key can be NULL, partitioning RIGHT? use COALESCE so all NULL-key rows share one partition.

**Query:**
```sql
-- PostgreSQL / SQL Server
WITH ranked AS (
  SELECT *,
         ROW_NUMBER() OVER (
           PARTITION BY COALESCE(user_id, -1)
           ORDER BY id
         ) AS rn
  FROM event_log
)
DELETE FROM ranked WHERE rn > 1;
```
**Explanation:** Partitioning on a coalesced key herds every NULL-user_id row into one partition, so duplicates collapse instead of each NULL forming its own singleton partition.

## Q85: Label the NULL group in a GROUP BY report as 'Uncategorized' without merging any real categories.

**Query:**
```sql
SELECT COALESCE(category, 'Uncategorized') AS bucket,
       COUNT(*) AS items
FROM inventory
GROUP BY category;
```
**Explanation:** Grouping by the raw column keeps real categories separate, while the SELECT-level COALESCE only renames the NULL bucket in the output.

**Alt1:**
```sql
SELECT COALESCE(category, 'Uncategorized') AS bucket, COUNT(*) AS items
FROM inventory
GROUP BY COALESCE(category, 'Uncategorized');
```
**Explanation:** The stricter form groups on the exact output expression; results are identical because the mapping is one-to-one over the grouped column.

## Q86: Compose a full address from nullable, possibly-blank parts, dropping the gaps.

**Query:**
```sql
-- MySQL / PostgreSQL
SELECT customer_id,
       CONCAT_WS(', ',
                 NULLIF(street, ''),
                 NULLIF(city,   ''),
                 NULLIF(zip,    '')) AS address
FROM customers;
```
**Explanation:** CONCAT_WS ignores NULL arguments, and NULLIF first converts blank strings into NULL so empty fields disappear from the join too.

## Q87: Compute an invoice total across several nullable columns: subtotal, tax, shipping, and discount.

**Query:**
```sql
SELECT invoice_id,
       subtotal
       + COALESCE(tax, 0)
       + COALESCE(shipping, 0)
       - COALESCE(discount, 0) AS total_owed
FROM invoices;
```
**Explanation:** Each nullable term is folded to 0 before arithmetic, so the total is never silently poisoned by a single NULL.

**Alt1:**
```sql
-- SQL Server
SELECT invoice_id,
       subtotal + ISNULL(tax, 0) + ISNULL(shipping, 0) - ISNULL(discount, 0) AS total_owed
FROM invoices;
```
**Explanation:** ISNULL supplies the same 0-folds with SQL Server's two-argument flavor.

## Q88: Compute each department's share of total spend, guarding against a zero or NULL grand total.

**Query:**
```sql
SELECT dept,
       COALESCE(amount * 100.0 / NULLIF(SUM(amount) OVER (), 0), 0) AS pct
FROM budget;
```
**Explanation:** NULLIF turns a zero-or-empty grand total into NULL, and COALESCE renders the resulting NULL share as 0.

## Q89: After a LEFT JOIN, report stores with no sales as having a total of 0 rather than NULL.

**Query:**
```sql
-- SQL Server / PostgreSQL
SELECT st.id AS store_id,
       COALESCE(SUM(o.amount), 0) AS sales_total
FROM stores st
LEFT JOIN orders o ON o.store_id = st.id
GROUP BY st.id;
```
**Explanation:** LEFT JOIN preserves every store; stores without orders produce an all-NULL SUM group, which COALESCE turns into zero.

**Alt1:**
```sql
-- Oracle
SELECT st.id AS store_id, NVL(SUM(o.amount), 0) AS sales_total
FROM stores st LEFT JOIN orders o ON o.store_id = st.id
GROUP BY st.id;
```
**Explanation:** Oracle's NVL fills the identical all-NULL aggregate output.

## Q90: Build a readable full name in MySQL, treating a NULL or blank middle name as an empty component.

**Query:**
```sql
-- MySQL
SELECT CONCAT_WS(' ', first_name, middle_name, last_name) AS full_name
FROM members;
```
**Explanation:** CONCAT_WS ignores NULL middle names on its own, which keeps the three-part name free of double spaces.

**Alt1:**
```sql
-- Oracle
SELECT first_name || ' ' || NVL2(middle_name, middle_name || ' ', '') || last_name AS full_name
FROM members;
```
**Explanation:** Oracle's `||` is NULL-tolerant and NVL2 injects the middle segment only when it exists.

## Q91: Use Oracle's old outer-join (+) syntax with NVL to show 'Unknown' for regions that never matched.

**Query:**
```sql
-- Oracle
SELECT e.name, NVL(r.region_name, 'Unknown') AS region
FROM employees e, regions r
WHERE e.region_id = r.region_id(+);
```
**Explanation:** The (+) marks the nullable side of the join; unmatched rows receive NULL region columns, then NVL supplies the placeholder.

**Alt1:**
```sql
-- Oracle (modern form)
SELECT e.name, NVL(r.region_name, 'Unknown') AS region
FROM employees e LEFT JOIN regions r ON e.region_id = r.region_id;
```
**Explanation:** The ANSI LEFT JOIN expresses the same thing more readably; the NVL applies identically.

## Q92: Show why `ISNULL(price, 'N/A')` on SQL Server behaves differently from COALESCE, and fix it.

**Query:**
```sql
-- SQL Server
SELECT ISNULL(price, 0)     AS price  -- fine: int + int
     , ISNULL(price, 'N/A') AS label  -- coerces price to the 1st arg type / may error
FROM products;
```
**Explanation:** ISNULL adopts the first argument's data type, so a text fallback on a numeric column misbehaves, whereas COALESCE resolves a common type between arguments.

**Alt1:**
```sql
-- SQL Server
SELECT COALESCE(CAST(price AS varchar(20)), 'N/A') AS label FROM products;
```
**Explanation:** Casting first removes the ambiguity so the text fallback is type-consistent.

## Q93: Scrub NULL amounts in a derived table before window math so the denominator can never be NULL or zero.

**Query:**
```sql
SELECT id, amount,
       ROUND(amount * 100.0 /
             (SELECT SUM(amount) FROM payments WHERE amount IS NOT NULL), 2) AS share
FROM payments
WHERE amount IS NOT NULL;
```
**Explanation:** Scraping NULLs in both the scalar subquery and the outer WHERE keeps the denominator null-free, making the ratio arithmetic safe.

## Q94: Show that DISTINCT and GROUP BY produce the same NULL handling and one merged NULL row.

**Query:**
```sql
SELECT DISTINCT region FROM territories;      -- one NULL row appears
SELECT region FROM territories GROUP BY region;  -- same single NULL row
```
**Explanation:** Both rely on "NULL IS NULL" during grouping, so every missing region merges into one NULL output row.

## Q95: Anti-join — find products that were never ordered using LEFT JOIN ... IS NULL.

**Query:**
```sql
SELECT p.id, p.name
FROM products p
LEFT JOIN order_items oi ON oi.product_id = p.id
WHERE oi.product_id IS NULL;
```
**Explanation:** A missing match leaves the right-side key NULL, and that IS NULL test isolates exactly the un-ordered products — immune to the NOT IN NULL trap.

**Alt1:**
```sql
SELECT id, name FROM products p
WHERE NOT EXISTS (SELECT 1 FROM order_items oi WHERE oi.product_id = p.id);
```
**Explanation:** The NOT EXISTS anti-join avoids the join-null filtering entirely and is idomatic for "has no related rows."

## Q96: When an access-policy subquery returns NULL or no rows at all, show how IN silently shrinks the answer and how EXISTS fixes it.

**Query:**
```sql
SELECT * FROM employees
WHERE department_id IN (SELECT allowed_dept
                        FROM policies
                        WHERE active = 1);
```
**Explanation:** If the subquery returns NULL for a department, `department_id = NULL` is UNKNOWN and the row is dropped; an empty list simply yields no match.

**Alt1:**
```sql
SELECT * FROM employees e
WHERE EXISTS (SELECT 1 FROM policies p
              WHERE p.active = 1
                AND p.allowed_dept = e.department_id);
```
**Explanation:** EXISTS evaluates per row, so NULLs inside the list are irrelevant and the query returns exactly the departments actually allowed.

## Q97: Treat a NULL opt-in flag as FALSE when filtering active accounts.

**Query:**
```sql
SELECT * FROM accounts
WHERE COALESCE(opted_in, 0) = 1;
```
**Explanation:** Folding NULL to 0 makes one strict boolean out of the three-valued field — only a real 1 matches.

**Alt1:**
```sql
-- PostgreSQL
SELECT * FROM accounts WHERE opted_in IS NOT FALSE;
```
**Explanation:** `IS NOT FALSE` is NULL-safe: it is TRUE for both TRUE and NULL, which is the same as treating missing as "allowed."

## Q98: Group a status column that uses -1 as a sentinel, collapsing all sentinel rows into the NULL group.

**Query:**
```sql
SELECT NULLIF(status, -1) AS status, COUNT(*) AS cnt
FROM jobs
GROUP BY NULLIF(status, -1);
```
**Explanation:** Grouping by the NULLIF result merges every -1 sentinel row into the NULL bucket, cleaning the report without a CASE.

## Q99: Fill missing daily prices by carrying forward the most recent known price (last-non-NULL interpolation).

**Query:**
```sql
-- Oracle
SELECT day_id, price,
       LAST_VALUE(price IGNORE NULLS)
         OVER (ORDER BY day_id) AS filled_price
FROM daily_prices;
```
**Explanation:** LAST_VALUE with IGNORE NULLS copies the most recent real price forward across every NULL gap — an Oracle-specific window nicety.

**Alt1:**
```sql
-- PostgreSQL (lateral lookback emulates the same fill)
SELECT p.day_id,
       COALESCE(p.price, prev.price) AS filled_price
FROM daily_prices p
LEFT JOIN LATERAL (
  SELECT price FROM daily_prices q
  WHERE q.day_id < p.day_id AND q.price IS NOT NULL
  ORDER BY q.day_id DESC
  LIMIT 1
) prev ON TRUE;
```
**Explanation:** A correlated lateral subquery fetches the nearest earlier known price and COALESCE fills gaps — portable closer to standard SQL than IGNORE NULLS.

## Q100: The hardest — write a NULL-safe equi-join across several nullable key columns so that NULL keys pair with NULL keys.

**Query:**
```sql
-- PostgreSQL / SQLite
SELECT a.*, b.*
FROM events a
JOIN events b
  ON a.key1 IS NOT DISTINCT FROM b.key1
 AND a.key2 IS NOT DISTINCT FROM b.key2;
```
**Explanation:** `IS NOT DISTINCT FROM` yields TRUE for both equality and both-NULL, so missing keys pair correctly — a genuine NULL-safe equi-join in one shot.

**Alt1 (portable OR-join):**
```sql
SELECT a.*, b.*
FROM events a
JOIN events b
  ON (a.key1 = b.key1 OR (a.key1 IS NULL AND b.key1 IS NULL))
 AND (a.key2 = b.key2 OR (a.key2 IS NULL AND b.key2 IS NULL));
```
**Explanation:** Explicit `OR ... IS NULL` branches reproduce `IS NOT DISTINCT FROM` on engines that lack the operator — same result, more typing, fully portable.
