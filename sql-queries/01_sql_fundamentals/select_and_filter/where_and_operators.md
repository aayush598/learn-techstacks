# WHERE Clause and Operators — 100 SQL Interview Q&A

## Q1: Find all employees whose salary is greater than 70000.

**Query:**
```sql
SELECT *
FROM employees
WHERE salary > 70000;
```
**Explanation:** The `>` operator filters rows where salary exceeds 70000.

---

## Q2: Retrieve all products that cost exactly $29.99.

**Query:**
```sql
SELECT *
FROM products
WHERE price = 29.99;
```
**Explanation:** The `=` operator matches rows where price equals the given literal.

---

## Q3: List all customers who do not live in Texas.

**Query:**
```sql
SELECT *
FROM customers
WHERE state <> 'TX';
```
**Explanation:** `<>` is the ANSI-standard not-equal operator.

**Alt1:**
```sql
SELECT *
FROM customers
WHERE state != 'TX';
```

---

## Q4: Find orders placed between January 1 and March 31, 2025.

**Query:**
```sql
SELECT *
FROM orders
WHERE order_date BETWEEN '2025-01-01' AND '2025-03-31';
```
**Explanation:** `BETWEEN` is inclusive on both ends, covering the full date range.

---

## Q5: Retrieve all employees hired in the year 2024.

**Query:**
```sql
SELECT *
FROM employees
WHERE hire_date >= '2024-01-01' AND hire_date <= '2024-12-31';
```
**Explanation:** A range with `>=` and `<=` is explicit and avoids any edge-case issues with `BETWEEN` on dates.

**Alt1:**
```sql
SELECT *
FROM employees
WHERE hire_date BETWEEN '2024-01-01' AND '2024-12-31';
```

---

## Q6: List all active users whose age is between 18 and 25 inclusive.

**Query:**
```sql
SELECT *
FROM users
WHERE is_active = 1 AND age BETWEEN 18 AND 25;
```
**Explanation:** `AND` combines two conditions; both must be true for a row to be included.

---

## Q7: Find all orders that are either pending or processing.

**Query:**
```sql
SELECT *
FROM orders
WHERE status = 'pending' OR status = 'processing';
```
**Explanation:** `OR` includes a row if at least one condition is true.

**Alt1:**
```sql
SELECT *
FROM orders
WHERE status IN ('pending', 'processing');
```

---

## Q8: Retrieve all products that are NOT discontinued and cost more than $10.

**Query:**
```sql
SELECT *
FROM products
WHERE is_discontinued = 0 AND price > 10;
```
**Explanation:** `AND` ensures both conditions are satisfied simultaneously.

---

## Q9: Find customers whose last name starts with 'S'.

**Query:**
```sql
SELECT *
FROM customers
WHERE last_name LIKE 'S%';
```
**Explanation:** `S%` matches any string beginning with 'S' followed by zero or more characters.

**Alt1:**
```sql
-- PostgreSQL
SELECT *
FROM customers
WHERE last_name ~ '^S';
```
**Explanation:** The regex anchor `^` matches the start of the string.

---

## Q10: List all employees who do not have a middle name.

**Query:**
```sql
SELECT *
FROM employees
WHERE middle_name IS NULL;
```
**Explanation:** `IS NULL` is the correct way to test for NULL; `= NULL` never evaluates to true.

---

## Q11: Find all invoices that are not null and have a total above 500.

**Query:**
```sql
SELECT *
FROM invoices
WHERE total IS NOT NULL AND total > 500;
```
**Explanation:** `IS NOT NULL` excludes rows with missing values before the comparison.

---

## Q12: Retrieve all customers from California, Florida, or New York.

**Query:**
```sql
SELECT *
FROM customers
WHERE state IN ('CA', 'FL', 'NY');
```
**Explanation:** `IN` is a shorthand for multiple `OR` equality checks.

**Alt1:**
```sql
SELECT *
FROM customers
WHERE state = 'CA' OR state = 'FL' OR state = 'NY';
```
**Explanation:** Equivalent of `IN`, useful when the list is dynamic or built from parameters.

---

## Q13: Find all products whose name is exactly 10 characters long and ends with 'Pro'.

**Query:**
```sql
SELECT *
FROM products
WHERE name LIKE '_______Pro';
```
**Explanation:** Each underscore `_` matches exactly one character; seven underscores plus 'Pro' equals ten characters.

---

## Q14: List all employees whose salary is not in the range 40000 to 60000.

**Query:**
```sql
SELECT *
FROM employees
WHERE salary NOT BETWEEN 40000 AND 60000;
```
**Explanation:** `NOT BETWEEN` excludes the inclusive range, returning salaries below 40000 or above 60000.

---

## Q15: Find all customers whose email does not contain the substring 'test'.

**Query:**
```sql
SELECT *
FROM customers
WHERE email NOT LIKE '%test%';
```
**Explanation:** `NOT LIKE` with `%test%` excludes any row where 'test' appears anywhere in the email.

---

## Q16: Retrieve all orders where the shipping address is missing.

**Query:**
```sql
SELECT *
FROM orders
WHERE shipping_address IS NULL;
```
**Explanation:** Checking for NULL shipping addresses identifies incomplete orders.

---

## Q17: Find all employees who earn more than the employee with ID 1001.

**Query:**
```sql
SELECT *
FROM employees
WHERE salary > (SELECT salary FROM employees WHERE employee_id = 1001);
```
**Explanation:** A scalar subquery returns a single value used for comparison in the outer WHERE.

---

## Q18: List all products whose price is not 0 and not NULL.

**Query:**
```sql
SELECT *
FROM products
WHERE price > 0 AND price IS NOT NULL;
```
**Explanation:** Two separate checks handle the zero-value and NULL cases independently.

---

## Q19: Find all customers whose name starts with 'A' and ends with 'n'.

**Query:**
```sql
SELECT *
FROM customers
WHERE name LIKE 'A%n';
```
**Explanation:** `A%n` matches strings that begin with 'A' and end with 'n', with any characters in between.

---

## Q20: Retrieve all employees who are in the 'Engineering' or 'Marketing' department and have a salary above 50000.

**Query:**
```sql
SELECT *
FROM employees
WHERE (department = 'Engineering' OR department = 'Marketing')
  AND salary > 50000;
```
**Explanation:** Parentheses enforce that the `OR` is evaluated before the `AND`.

**Alt1:**
```sql
SELECT *
FROM employees
WHERE department IN ('Engineering', 'Marketing')
  AND salary > 50000;
```

---

## Q21: Find all orders placed on weekends (Saturday or Sunday).

**Query:**
```sql
-- PostgreSQL
SELECT *
FROM orders
WHERE EXTRACT(DOW FROM order_date) IN (0, 6);
```
**Explanation:** `EXTRACT(DOW ...)` returns the day of week; 0 = Sunday, 6 = Saturday in PostgreSQL.

---

## Q22: Find all orders placed on weekends (Saturday or Sunday).

**Query:**
```sql
-- MySQL
SELECT *
FROM orders
WHERE DAYOFWEEK(order_date) IN (1, 7);
```
**Explanation:** MySQL's `DAYOFWEEK` returns 1 for Sunday and 7 for Saturday.

---

## Q23: List all employees whose name does NOT start with 'J'.

**Query:**
```sql
SELECT *
FROM employees
WHERE NOT name LIKE 'J%';
```
**Explanation:** `NOT` negates the `LIKE` predicate, excluding names beginning with 'J'.

---

## Q24: Find all products that are either free (price = 0) or in the 'Clearance' category.

**Query:**
```sql
SELECT *
FROM products
WHERE price = 0 OR category = 'Clearance';
```
**Explanation:** `OR` includes rows satisfying either condition.

---

## Q25: Retrieve all customers whose phone number starts with '555' and has exactly 12 characters.

**Query:**
```sql
SELECT *
FROM customers
WHERE phone LIKE '555__________';
```
**Explanation:** `555` followed by nine underscores matches a 12-character string starting with '555'.

---
## Q26: Find all employees whose email address is not stored.

**Query:**
```sql
SELECT *
FROM employees
WHERE email IS NULL;
```
**Explanation:** `IS NULL` tests for a missing value; `email = NULL` always yields NULL and never true.

**Alt1:**
```sql
SELECT *
FROM employees
WHERE NVL(email, 'missing') = 'missing';
```
**Explanation:** Oracle's `NVL` substitutes a sentinel so the equality test can run.

---

## Q27: List all orders where a discount code was not applied.

**Query:**
```sql
SELECT *
FROM orders
WHERE discount_code IS NULL;
```
**Explanation:** Unset discount codes are stored as NULL, so the NULL check identifies them.

---

## Q28: Find all customers whose signup date is within the last 30 days.

**Query:**
```sql
-- PostgreSQL
SELECT *
FROM customers
WHERE signup_date >= CURRENT_DATE - INTERVAL '30 days';
```
**Explanation:** Interval arithmetic computes the cut-off date dynamically.

---

## Q29: Find all customers whose signup date is within the last 30 days.

**Query:**
```sql
-- MySQL
SELECT *
FROM customers
WHERE signup_date >= CURDATE() - INTERVAL 30 DAY;
```
**Explanation:** MySQL expresses relative date ranges with `INTERVAL` and `CURDATE()`.

---

## Q30: Retrieve all employees whose salary is between two values passed as parameters, inclusive.

**Query:**
```sql
SELECT *
FROM employees
WHERE salary BETWEEN ? AND ?;
```
**Explanation:** `BETWEEN` is inclusive of both bounds and works cleanly with bind parameters.

---

## Q31: Find all orders that are NOT in 'cancelled' or 'refunded' status.

**Query:**
```sql
SELECT *
FROM orders
WHERE status NOT IN ('cancelled', 'refunded');
```
**Explanation:** `NOT IN` excludes rows whose status matches any listed value.

---

## Q32: List all products whose name contains the word 'Pro' anywhere.

**Query:**
```sql
SELECT *
FROM products
WHERE name LIKE '%Pro%';
```
**Explanation:** `%Pro%` matches 'Pro' anywhere in the string, at the start, middle, or end.

---

## Q33: Find all employees hired after Jan 1, 2023 and before Dec 31, 2024.

**Query:**
```sql
SELECT *
FROM employees
WHERE hire_date > '2023-01-01' AND hire_date < '2024-12-31';
```
**Explanation:** Strict `>` and `<` exclude both boundary dates, unlike `BETWEEN`.

**Alt1:**
```sql
SELECT *
FROM employees
WHERE hire_date BETWEEN '2023-01-02' AND '2024-12-30';
```

---

## Q34: Retrieve all invoices that are overdue, where the due date is in the past.

**Query:**
```sql
SELECT *
FROM invoices
WHERE due_date < CURRENT_DATE;
```
**Explanation:** Comparing a date column against today's date flags past-due invoices.

**Alt1:**
```sql
-- MySQL
SELECT *
FROM invoices
WHERE DATEDIFF(CURDATE(), due_date) > 0;
```
**Explanation:** `DATEDIFF` gives the sign of the overdue amount directly.

---

## Q35: Find all customers whose name starts with any letter between A and M.

**Query:**
```sql
SELECT *
FROM customers
WHERE name >= 'A' AND name < 'N';
```
**Explanation:** String comparisons sort lexically, so this range covers A through M regardless of prefix.

---

## Q36: List all employees whose first name is John and last name is Smith.

**Query:**
```sql
SELECT *
FROM employees
WHERE first_name = 'John' AND last_name = 'Smith';
```
**Explanation:** Both equality conditions must hold for a row to be returned.

---

## Q37: Find all products that are in stock and cost less than 50.

**Query:**
```sql
SELECT *
FROM products
WHERE quantity_in_stock > 0 AND price < 50;
```
**Explanation:** Positive stock plus a price below 50 defines the eligible set.

---

## Q38: Retrieve all orders with a total not equal to 0.

**Query:**
```sql
SELECT *
FROM orders
WHERE total != 0;
```
**Explanation:** `!=` behaves identically to `<>` in every major dialect.

**Alt1:**
```sql
SELECT *
FROM orders
WHERE total <> 0;
```

---

## Q39: Find all employees who earn at least 45000.

**Query:**
```sql
SELECT *
FROM employees
WHERE salary >= 45000;
```
**Explanation:** `>=` includes employees earning exactly the minimum threshold.

---

## Q40: Find all employees who earn at most 45000.

**Query:**
```sql
SELECT *
FROM employees
WHERE salary <= 45000;
```
**Explanation:** `<=` includes employees earning exactly the maximum threshold.

---

## Q41: List all customers who registered in 2023 and made at least one order in 2024.

**Query:**
```sql
SELECT *
FROM customers c
WHERE c.registered_at BETWEEN '2023-01-01' AND '2023-12-31'
  AND EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
              AND o.order_date BETWEEN '2024-01-01' AND '2024-12-31');
```
**Explanation:** `EXISTS` (light use) checks for the presence of a matching order row.

---

## Q42: Find all products with no price assigned.

**Query:**
```sql
SELECT *
FROM products
WHERE price IS NULL;
```
**Explanation:** `IS NULL` catches unassigned prices; a `= NULL` test would silently return no rows.

---

## Q43: Retrieve all employees hired in January, February, or March regardless of year.

**Query:**
```sql
-- PostgreSQL
SELECT *
FROM employees
WHERE EXTRACT(MONTH FROM hire_date) BETWEEN 1 AND 3;
```
**Explanation:** Extracting the month component isolates the seasonal filter from the year.

---

## Q44: Find all orders placed today.

**Query:**
```sql
-- PostgreSQL
SELECT *
FROM orders
WHERE order_date = CURRENT_DATE;
```
**Explanation:** Direct equality against `CURRENT_DATE` matches today's orders exactly.

**Alt1:**
```sql
-- PostgreSQL
SELECT *
FROM orders
WHERE order_date >= CURRENT_DATE AND order_date < CURRENT_DATE + 1;
```
**Explanation:** A half-open range works even when the timestamp carries a time component.

---

## Q45: Find all orders placed today.

**Query:**
```sql
-- SQL Server
SELECT *
FROM orders
WHERE CAST(order_date AS DATE) = GETDATE();
```
**Explanation:** Casting to `DATE` strips the time component before comparing to the current date.

---

## Q46: List all customers who did not provide a state.

**Query:**
```sql
SELECT *
FROM customers
WHERE state IS NULL OR state = '';
```
**Explanation:** Both missing and empty-string states are treated as absent.

---

## Q47: Find all employees with a bonus, where bonus is a nullable column.

**Query:**
```sql
SELECT *
FROM employees
WHERE bonus IS NOT NULL AND bonus > 0;
```
**Explanation:** Two predicates: the bonus must exist and must be greater than zero.

---

## Q48: Retrieve all products whose stock count is less than half of the reorder threshold.

**Query:**
```sql
SELECT *
FROM products
WHERE quantity_in_stock * 2 < reorder_threshold;
```
**Explanation:** Arithmetic inside the WHERE clause filters on a derived condition.

---

## Q49: Find all orders where the quantity ordered is at least the quantity on hand.

**Query:**
```sql
SELECT *
FROM orders
WHERE quantity_ordered >= quantity_on_hand;
```
**Explanation:** Comparing two columns directly is allowed inside the predicate.

---

## Q50: Retrieve all customers whose first name is exactly 'Sam' and has an email like 'sam%'.

**Query:**
```sql
SELECT *
FROM customers
WHERE first_name = 'Sam' AND email LIKE 'sam%@%';
```
**Explanation:** An equality on the full first name combines with a prefix pattern on email.

---
## Q51: Find all employees whose tenured years of service is at least 5.

**Query:**
```sql
-- SQL Server
SELECT *
FROM employees
WHERE DATEDIFF(YEAR, hire_date, GETDATE()) >= 5;
```
**Explanation:** `DATEDIFF` computes elapsed years from the hire date to today.

---

## Q52: List all products whose color is not specified and price is between 20 and 80.

**Query:**
```sql
SELECT *
FROM products
WHERE color IS NULL AND price BETWEEN 20 AND 80;
```
**Explanation:** A missing color combined with a price band narrows the result set.

---

## Q53: Retrieve all users whose role is either 'admin' or 'superadmin' but whose account is locked.

**Query:**
```sql
SELECT *
FROM users
WHERE role IN ('admin', 'superadmin') AND account_locked = 1;
```
**Explanation:** `IN` handles the role list while `AND` adds the locked flag.

---

## Q54: Find all orders that are neither paid nor shipped.

**Query:**
```sql
SELECT *
FROM orders
WHERE paid_at IS NULL AND shipped_at IS NULL;
```
**Explanation:** Both timestamps being NULL indicates an order in an incomplete state.

---

## Q55: Retrieve all customers whose shipping country is not the USA.

**Query:**
```sql
SELECT *
FROM customers
WHERE country != 'USA';
```
**Explanation:** Not-equal filters out USA customers regardless of other attributes.

**Alt1:**
```sql
SELECT *
FROM customers
WHERE NOT (country = 'USA');
```

---

## Q56: Find all products priced above 100 that are either 'Electronics' or 'Toys'.

**Query:**
```sql
SELECT *
FROM products
WHERE price > 100 AND (category = 'Electronics' OR category = 'Toys');
```
**Explanation:** Parentheses are required so the price condition applies to both categories.

**Alt1:**
```sql
SELECT *
FROM products
WHERE price > 100 AND category IN ('Electronics', 'Toys');
```

---

## Q57: List active users who have not been verified.

**Query:**
```sql
SELECT *
FROM users
WHERE is_active = 1 AND verified_at IS NULL;
```
**Explanation:** The active flag combined with a NULL verification timestamp selects the target group.

---

## Q58: Find all employees whose department is not in the given list.

**Query:**
```sql
SELECT *
FROM employees
WHERE department NOT IN ('Human Resources', 'Legal');
```
**Explanation:** `NOT IN` excludes any row matching any listed department.

---

## Q59: Retrieve all rows from a table where a boolean field is false.

**Query:**
```sql
-- PostgreSQL
SELECT *
FROM users
WHERE is_admin = FALSE;
```
**Explanation:** PostgreSQL supports native `TRUE`/`FALSE` literals in the predicate.

---

## Q60: Retrieve all rows from a table where a boolean field is false.

**Query:**
```sql
-- MySQL
SELECT *
FROM users
WHERE is_admin = 0;
```
**Explanation:** MySQL stores booleans as 0 or 1, so numeric comparison works.

---

## Q61: Find all employees with a salary greater than the average salary.

**Query:**
```sql
SELECT *
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```
**Explanation:** A scalar aggregate subquery provides the comparison threshold.

**Alt1:**
```sql
SELECT e.*
FROM employees e
CROSS JOIN (SELECT AVG(salary) AS avg_salary FROM employees) a
WHERE e.salary > a.avg_salary;
```
**Explanation:** A derived table exposes the aggregate as a column available to the WHERE clause.

---

## Q62: List all products where the description references 'v2' anywhere after position 10.

**Query:**
```sql
-- SQL Server
SELECT *
FROM products
WHERE CHARINDEX('v2', description) > 10;
```
**Explanation:** `CHARINDEX` returns the position of the substring, letting us require it later in the text.

---

## Q63: Find all customers who joined in 2024 but have not placed any order.

**Query:**
```sql
SELECT *
FROM customers c
WHERE c.joined_at BETWEEN '2024-01-01' AND '2024-12-31'
  AND NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);
```
**Explanation:** `NOT EXISTS` verifies the absence of any matching order.

**Alt1:**
```sql
SELECT *
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE c.joined_at BETWEEN '2024-01-01' AND '2024-12-31'
  AND o.order_id IS NULL;
```
**Explanation:** A left join plus NULL probe yields the anti-join result.

---

## Q64: Retrieve all orders where the total is NULL because the order is unpaid.

**Query:**
```sql
SELECT *
FROM orders
WHERE total IS NULL;
```
**Explanation:** A NULL total identifies orders for which no amount has been recorded.

---

## Q65: Find all products whose price, tax, and shipping costs are all NULL.

**Query:**
```sql
SELECT *
FROM products
WHERE price IS NULL AND tax IS NULL AND shipping_cost IS NULL;
```
**Explanation:** Independent NULL checks on three columns must all pass.

---

## Q66: List employees whose last name is longer than 10 characters.

**Query:**
```sql
SELECT *
FROM employees
WHERE LENGTH(last_name) > 10;
```
**Explanation:** The string function computes length, and the predicate compares it.

---

## Q67: Find all products whose name contains 'X' as the second character.

**Query:**
```sql
SELECT *
FROM products
WHERE name LIKE '_X%';
```
**Explanation:** A single underscore matches the first character, then literal 'X' follows.

---

## Q68: Retrieve all customers whose email ends with '.edu'.

**Query:**
```sql
SELECT *
FROM customers
WHERE email LIKE '%.edu';
```
**Explanation:** The `%` wildcard matches any prefix before the literal `.edu` suffix.

---

## Q69: Find all orders delivered in Q2 2025.

**Query:**
```sql
SELECT *
FROM orders
WHERE delivered_at BETWEEN '2025-04-01' AND '2025-06-30';
```
**Explanation:** The Q2 calendar range is expressed with inclusive `BETWEEN`.

---

## Q70: Find all employees with no manager (the top of the hierarchy).

**Query:**
```sql
SELECT *
FROM employees
WHERE manager_id IS NULL;
```
**Explanation:** A NULL manager_id marks the root-level employees.

---

## Q71: Retrieve all products whose stock is running low (lower than a warning threshold) or discontinued.

**Query:**
```sql
SELECT *
FROM products
WHERE quantity_in_stock < warning_threshold OR is_discontinued = 1;
```
**Explanation:** Either condition being true brings the product into the result.

---

## Q72: Find all transactions valued between 100 and 200 that were refunded.

**Query:**
```sql
SELECT *
FROM transactions
WHERE amount BETWEEN 100 AND 200 AND refunded = 1;
```
**Explanation:** Range plus flag composition across two columns.

---

## Q73: Find all transactions valued between 100 and 200 that were refunded.

**Query:**
```sql
SELECT *
FROM transactions
WHERE amount >= 100 AND amount <= 200 AND refunded = 1;
```
**Explanation:** The same range stated with explicit comparison operators.

---

## Q74: List all orders where the customer name is 'Unknown' or the customer ID is missing.

**Query:**
```sql
SELECT *
FROM orders
WHERE customer_name = 'Unknown' OR customer_id IS NULL;
```
**Explanation:** An `OR` branch handles the sentinel value and the NULL case separately.

---

## Q75: Find employees whose first name is NULL but who still have a username.

**Query:**
```sql
SELECT *
FROM employees
WHERE first_name IS NULL AND username IS NOT NULL;
```
**Explanation:** Mixed NULL and non-NULL tests refine which records qualify.

---
## Q76: Find all customers not in the VIP list, where the VIP table may contain NULL admin IDs.

**Query:**
```sql
SELECT *
FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM vip_list WHERE customer_id IS NOT NULL);
```
**Explanation:** The inner filter removes NULLs, which would otherwise poison `NOT IN` with unknown results.

**Alt1:**
```sql
SELECT *
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM vip_list v WHERE v.customer_id = c.customer_id);
```

---

## Q77: Retrieve all orders where the status is not one of the finished statuses, using NOT IN safely.

**Query:**
```sql
SELECT *
FROM orders
WHERE status NOT IN (SELECT final_status FROM status_codes WHERE final_status IS NOT NULL);
```
**Explanation:** Filtering NULLs in the subquery prevents the `NOT IN` NULL pitfall.

---

## Q78: Find products whose price field may be NULL but should be treated as 0 in the comparison.

**Query:**
```sql
SELECT *
FROM products
WHERE COALESCE(price, 0) < 50;
```
**Explanation:** `COALESCE` substitutes 0 for NULL so unknown prices survive the comparison.

---

## Q79: List all employees whose bonus is at least 5000, treating missing bonus as 0.

**Query:**
```sql
-- PostgreSQL
SELECT *
FROM employees
WHERE COALESCE(bonus, 0) >= 5000;
```
**Explanation:** `COALESCE` substitutes 0 for NULL bonus values before the test.

**Alt1:**
```sql
-- MySQL
SELECT *
FROM employees
WHERE IFNULL(bonus, 0) >= 5000;
```

---

## Q80: Find all books whose title is either entirely missing or blank.

**Query:**
```sql
SELECT *
FROM books
WHERE TRIM(title) IS NULL OR TRIM(title) = '';
```
**Explanation:** Whitespace-only titles are normalized with `TRIM` before the empty check.

**Alt1:**
```sql
SELECT *
FROM books
WHERE NULLIF(TRIM(title), '') IS NULL;
```

---

## Q81: Retrieve all customers whose name matches a pattern but case-insensitively.

**Query:**
```sql
-- PostgreSQL
SELECT *
FROM customers
WHERE name ILIKE 'john%';
```
**Explanation:** `ILIKE` performs a case-insensitive prefix match in PostgreSQL.

---

## Q82: Find all products where the name contains a literal percent sign.

**Query:**
```sql
-- SQL Server
SELECT *
FROM products
WHERE name LIKE '%\%%' ESCAPE '\';
```
**Explanation:** `ESCAPE` declares `\` so the inner `\%` matches a literal percent character.

---

## Q83: Find all products where the name contains a literal percent sign.

**Query:**
```sql
-- MySQL
SELECT *
FROM products
WHERE name LIKE '%|%' ESCAPE '|';
```
**Explanation:** `ESCAPE` declares `|` as the escape character so the inner `%` matches a literal percent.

**Alt1:**
```sql
-- SQL Server
SELECT *
FROM products
WHERE name LIKE '%[%]%';
```
**Explanation:** In T-SQL, brackets form a character class, making `%` literal inside `[%]`.

---

## Q84: Find all employees whose name ends with an underscore character.

**Query:**
```sql
SELECT *
FROM employees
WHERE name LIKE '%\_' ESCAPE '\';
```
**Explanation:** The escape character makes `\_` match a literal underscore instead of the single-char wildcard.

---

## Q85: Filter rows where a trimmed, case-normalized column equals a value using a derived table.

**Query:**
```sql
SELECT sku, total
FROM (SELECT sku, price * quantity AS total FROM line_items) t
WHERE t.total > 500;
```
**Explanation:** The derived table computes `total`, and the outer WHERE filters on that alias.

---

## Q86: Filter on a computed column alias via a derived table.

**Query:**
```sql
-- PostgreSQL
SELECT sku, price * quantity AS total
FROM line_items
WHERE price * quantity > 500;
```
**Explanation:** SQL evaluates WHERE before SELECT, so aliases are unusable there; the expression must be repeated.

**Alt1:**
```sql
-- SQL Server
SELECT *
FROM (SELECT sku, price * quantity AS total FROM line_items) t
WHERE t.total > 500;
```
**Explanation:** The derived table exposes the alias to the outer WHERE clause.

---

## Q87: Find customers with extreme order totals using a lateral join to isolate the computation.

**Query:**
```sql
-- PostgreSQL
SELECT c.name, sub.total
FROM customers c
CROSS JOIN LATERAL (SELECT SUM(o.total) AS total FROM orders o WHERE o.customer_id = c.customer_id) sub
WHERE sub.total > 5000;
```
**Explanation:** `LATERAL` evaluates the subquery per row, exposing the alias to the WHERE clause.

---

## Q88: List all products whose discount percentage is not known using IFNULL in the predicate.

**Query:**
```sql
-- MySQL
SELECT *
FROM products
WHERE IFNULL(discount_pct, 0) = 0 AND discount_pct IS NULL;
```
**Explanation:** The first branch asserts the substituted value, the second that it was truly missing.

---

## Q89: Find all orders whose total_outstanding is NULL and should be reported as 0.

**Query:**
```sql
SELECT *
FROM orders
WHERE IFNULL(total_outstanding, 0) <> total_outstanding;
```
**Explanation:** Only NULL rows differ from their substituted value, isolating them.

---

## Q90: Retrieve records where at least one column among three is populated.

**Query:**
```sql
SELECT *
FROM contacts
WHERE phone IS NOT NULL OR email IS NOT NULL OR address IS NOT NULL;
```
**Explanation:** The `OR` chain keeps any row with at least one contact channel.

**Alt1:**
```sql
-- PostgreSQL
SELECT *
FROM contacts
WHERE COALESCE(phone, email, address) IS NOT NULL;
```
**Explanation:** `COALESCE` returns the first non-NULL argument, or NULL when all are missing.

---

## Q91: Find all employees whose name, after trimming, begins with 'R' using scalar logic in WHERE.

**Query:**
```sql
SELECT *
FROM employees
WHERE LEFT(TRIM(name), 1) = 'R';
```
**Explanation:** The leading character is isolated after trimming whitespace.

**Alt1:**
```sql
SELECT *
FROM employees
WHERE TRIM(name) LIKE 'R%';
```

---

## Q92: Retrieve all transactions that happened during business hours (9 AM to 5 PM).

**Query:**
```sql
-- PostgreSQL
SELECT *
FROM transactions
WHERE EXTRACT(HOUR FROM occurred_at) BETWEEN 9 AND 17;
```
**Explanation:** `EXTRACT` on the hour component tests if the time falls in business hours.

---

## Q93: Find all events that overlap a given time window using range operators.

**Query:**
```sql
-- PostgreSQL (range type)
SELECT *
FROM events
WHERE event_window && tsrange('2025-06-01 00:00', '2025-06-30 00:00');
```
**Explanation:** The `&&` overlap operator returns true when two ranges intersect.

---

## Q94: Filter using an array membership test without a subquery.

**Query:**
```sql
-- PostgreSQL
SELECT *
FROM users
WHERE 'paying' = ANY(roles);
```
**Explanation:** `ANY` against an array column tests membership directly.

---

## Q95: Find orders whose amount is greater than every amount in the free-tier table.

**Query:**
```sql
SELECT *
FROM orders
WHERE amount > ALL (SELECT max_amount FROM free_tier);
```
**Explanation:** `> ALL` requires the amount to exceed every value in the subquery result.

---

## Q96: Find orders whose amount is greater than at least one amount in the promo table.

**Query:**
```sql
SELECT *
FROM orders
WHERE amount > ANY (SELECT max_amount FROM promo_tier);
```
**Explanation:** `> ANY` passes when the amount beats any single value from the subquery.

---

## Q97: Find orders whose amount exceeds every value in the promo table, using SOME.

**Query:**
```sql
SELECT *
FROM orders
WHERE amount > SOME (SELECT max_amount FROM promo_tier);
```
**Explanation:** `SOME` is an exact synonym for `ANY`, so the semantics are identical.

---

## Q98: Combine NOT with AND/OR to find all non-urgent, non-null priority issues.

**Query:**
```sql
SELECT *
FROM issues
WHERE NOT (priority = 'urgent' OR priority IS NULL);
```
**Explanation:** `NOT` wraps the whole boolean expression to exclude urgent or missing priorities.

**Alt1:**
```sql
SELECT *
FROM issues
WHERE priority <> 'urgent' AND priority IS NOT NULL;
```

---

## Q99: Use boolean literal logic to select records explicitly flagged in a PostgreSQL table.

**Query:**
```sql
-- PostgreSQL
SELECT *
FROM features
WHERE enabled = TRUE AND beta IS NOT TRUE;
```
**Explanation:** Careful: `enabled = TRUE` tests equality, while `IS NOT TRUE` treats NULL as not-true instead of excluding it as `<> TRUE` would on NULL.

---

## Q100: Replace an OR-heavy condition with an IN list wrapped in a NOT-IN-safe pattern.

**Query:**
```sql
SELECT *
FROM orders
WHERE status IN ('submitted', 'paid', 'fulfilled')
  AND NOT EXISTS (SELECT 1 FROM retries r WHERE r.order_id = orders.order_id AND r.final_status IS NULL);
```
**Explanation:** The `IN` whitelist plus `NOT EXISTS` mirrors boolean precedence without NULL pitfalls.

---
