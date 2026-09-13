# Basic SELECT Queries — 100 SQL Interview Q&A

## Q1: Write a query to select all columns from the employees table.
**Query:**
```sql
SELECT * FROM employees;
```
**Explanation:** The `*` expands to every column of the table in its defined order, used for quick table exploration.

## Q2: Write a query to select only the first_name and last_name columns from the employees table.
**Query:**
```sql
SELECT first_name, last_name FROM employees;
```
**Explanation:** Listing columns explicitly returns just those columns; the result order follows the select list.

## Q3: Write a query to display last_name, hire_date, and first_name from the employees table in that exact column order.
**Query:**
```sql
SELECT last_name, hire_date, first_name FROM employees;
```
**Explanation:** Columns appear in the order they are written in the select list, independent of table definition order.

## Q4: Write a query to select the pay column from the employees table and rename it to salary.
**Query:**
```sql
SELECT pay AS salary FROM employees;
```
**Explanation:** `AS` assigns the output column header `salary` without changing the underlying column.

## Q5: Write a query that renames the title column to job_title in the output, without using the AS keyword.
**Query:**
```sql
SELECT title job_title FROM employees;
```
**Explanation:** The `AS` keyword is optional in most dialects; the alias may directly follow the column.

## Q6: Write a query that returns the pay column under an alias containing a space, "Annual Pay".
**Query:**
```sql
SELECT pay AS "Annual Pay" FROM employees;
```
**Explanation:** Aliases with spaces must be double-quoted so the engine reads them as a single identifier.

## Q7: Write a query that returns the literal string 'Hello World' without selecting from any table.
**Query:**
```sql
SELECT 'Hello World';
```
**Explanation:** SELECT can serve as a calculator/printer without FROM; Oracle requires a dummy table.
**Alt1:**
```sql
-- Oracle
SELECT 'Hello World' FROM DUAL;
```

## Q8: Write a query, without a FROM clause, that computes the product 5 * 7.
**Query:**
```sql
SELECT 5 * 7;
```
**Explanation:** Constants and operators can be evaluated directly in the select list with no table scan.

## Q9: Write a query that shows each employee's salary increased by 10 percent as a new computed column.
**Query:**
```sql
SELECT salary * 1.1 AS raised_salary FROM employees;
```
**Explanation:** Arithmetic is applied per row; the computed value is labeled `raised_salary`.
**Alt1:**
```sql
SELECT salary + salary * 0.10 AS raised_salary FROM employees;
```

## Q10: Write a query to compute each employee's annual compensation as monthly salary times 12 plus bonus.
**Query:**
```sql
SELECT salary * 12 + bonus AS annual_compensation FROM employees;
```
**Explanation:** `*` binds tighter than `+`, so this correctly computes `(salary*12) + bonus` per row.
**Alt1:**
```sql
SELECT (salary * 12) + bonus AS annual_compensation FROM employees;
```

## Q11: Write a query to show each employee's full name as first_name and last_name joined by a single space.
**Query:**
```sql
-- PostgreSQL
SELECT first_name || ' ' || last_name AS full_name FROM employees;
```
**Explanation:** `||` concatenates strings left to right in PostgreSQL and standard SQL; a padding space is inserted between names.

## Q12: Write a query using the MySQL CONCAT function to build an employee's full name from first_name and last_name.
**Query:**
```sql
-- MySQL
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM employees;
```
**Explanation:** `CONCAT` joins its arguments with the literal space in between; MySQL treats `||` pragmatically so CONCAT is the portable choice.

## Q13: Write a query to assemble a customer's address as city, state, and zip_code separated by commas and spaces.
**Query:**
```sql
-- PostgreSQL
SELECT city || ', ' || state || ' ' || zip_code AS full_address FROM customers;
```
**Explanation:** Each literal separator is its own string glued between column values.
**Alt1:**
```sql
-- MySQL
SELECT CONCAT(city, ', ', state, ' ', zip_code) AS full_address FROM customers;
```

## Q14: Write a query that returns the literal 'Employee' as a label next to each employee's first_name.
**Query:**
```sql
SELECT 'Employee' AS row_label, first_name FROM employees;
```
**Explanation:** A string constant repeats on every row, acting as a static column in the result set.

## Q15: Write a query, without a FROM clause, that returns today's date.
**Query:**
```sql
SELECT CURRENT_DATE AS today;
```
**Explanation:** `CURRENT_DATE` is a standard SQL date function usable without a table reference.

## Q16: Write a query that selects the first_name column using its fully qualified name employees.first_name.
**Query:**
```sql
SELECT employees.first_name FROM employees;
```
**Explanation:** Prefixing the column with the table name removes ambiguity and is safe in multi-table queries.

## Q17: Write a query that aliases the employees table as e and selects e.first_name using the alias.
**Query:**
```sql
SELECT e.first_name FROM employees AS e;
```
**Explanation:** The table alias `e` replaces the full name for column qualification everywhere in the query.

## Q18: Write a query that returns the first_name column twice in the same result set.
**Query:**
```sql
SELECT first_name, first_name FROM employees;
```
**Explanation:** Repeating a column in the select list produces duplicate output columns; it is legal but rarely intended.

## Q19: Write a query that returns all employee columns plus a computed column showing years of service.
**Query:**
```sql
-- MySQL
SELECT e.*, YEAR(CURRENT_DATE) - YEAR(hire_date) AS years_of_service FROM employees AS e;
```
**Explanation:** `e.*` expands every base column while the extra expression is appended as a new computed column.

## Q20: Write a query to list the unique job_title values from the employees table.
**Query:**
```sql
SELECT DISTINCT job_title FROM employees;
```
**Explanation:** `DISTINCT` collapses duplicate job titles so each value appears exactly once.

## Q21: Write a query to list each distinct country and region pairing from the customers table.
**Query:**
```sql
SELECT DISTINCT country, region FROM customers;
```
**Explanation:** DISTINCT is applied to the whole row combination, so `country,region` must both match to be a duplicate.

## Q22: Write a query that returns the distinct job_title values from the employees table under the alias role.
**Query:**
```sql
SELECT DISTINCT job_title AS role FROM employees;
```
**Explanation:** DISTINCT removes duplicates before the alias is applied to the output header.

## Q23: Write a query to count how many distinct job_title values exist in the employees table.
**Query:**
```sql
SELECT COUNT(DISTINCT job_title) AS role_count FROM employees;
```
**Explanation:** `COUNT(DISTINCT ...)` deduplicates values before counting and, without GROUP BY, returns a single row.
**Alt1:**
```sql
SELECT COUNT(DISTINCT role) FROM (SELECT DISTINCT job_title AS role FROM employees) t;
```

## Q24: Write a query to return only the first 5 rows of the employees table.
**Query:**
```sql
-- MySQL
SELECT * FROM employees LIMIT 5;
```
**Explanation:** `LIMIT n` caps the number of rows returned after the select list is evaluated.
**Alt1:**
```sql
-- SQL Server
SELECT TOP 5 * FROM employees;
```

## Q25: Write a query to return employees 11 through 15 from the employees table (5 rows, skipping the first 10).
**Query:**
```sql
-- MySQL
SELECT * FROM employees LIMIT 5 OFFSET 10;
```
**Explanation:** `OFFSET` skips 10 rows before returning the next 5, implementing page 3 of a 5-row page.
**Alt1:**
```sql
-- PostgreSQL
SELECT * FROM employees OFFSET 10 FETCH FIRST 5 ROWS ONLY;
```
## Q26: Write a query to return the first 10 rows of the products table using ANSI-standard row limiting.
**Query:**
```sql
SELECT * FROM products FETCH FIRST 10 ROWS ONLY;
```
**Explanation:** `FETCH FIRST n ROWS ONLY` is the ISO-standard limit, supported in PostgreSQL, Oracle 12c+, and SQL Server 2012+.
**Alt1:**
```sql
-- Oracle
SELECT * FROM products WHERE ROWNUM <= 10;
```

## Q27: Write a query to return only the first 3 rows of the orders table using SQL Server syntax.
**Query:**
```sql
-- SQL Server
SELECT TOP 3 * FROM orders;
```
**Explanation:** `TOP n` in SQL Server limits the result set before it is sent to the client.

## Q28: Write a query to return the top 25 percent of rows from the employees table.
**Query:**
```sql
-- SQL Server
SELECT TOP 25 PERCENT * FROM employees;
```
**Explanation:** `TOP` also accepts a percentage, rounding the row count up to the nearest whole row.

## Q29: Write a query that returns the first 5 rows of a computed line_total column (price times quantity).
**Query:**
```sql
-- MySQL
SELECT product_name, price * quantity AS line_total FROM order_items LIMIT 5;
```
**Explanation:** The expression is evaluated on every row and LIMIT then keeps only the first 5 results.

## Q30: Write a query that calculates tax as amount times tax_rate, noting what happens when tax_rate is NULL.
**Query:**
```sql
SELECT amount, tax_rate, amount * tax_rate AS tax FROM invoices;
```
**Explanation:** Any arithmetic involving NULL evaluates to NULL, so rows with a NULL tax_rate return NULL for tax.
**Alt1:**
```sql
SELECT amount, COALESCE(amount * tax_rate, 0) AS tax FROM invoices;
```

## Q31: Write a query that evaluates 7 divided by 2 using PostgreSQL integer division.
**Query:**
```sql
-- PostgreSQL
SELECT 7 / 2;
```
**Explanation:** Integer divided by integer truncates in PostgreSQL, returning 3; adding a decimal operand gives 3.5.
**Alt1:**
```sql
-- PostgreSQL
SELECT 7 / 2.0;
```

## Q32: Write a query that returns the remainder of 17 divided by 5.
**Query:**
```sql
-- MySQL
SELECT 17 % 5;
```
**Explanation:** The `%` operator returns the modulo (2) in MySQL and PostgreSQL.
**Alt1:**
```sql
-- Oracle
SELECT MOD(17, 5) FROM DUAL;
```

## Q33: Write a query to compute each order item's total as quantity times (list_price minus discount).
**Query:**
```sql
SELECT (list_price - discount) * quantity AS line_total FROM order_items;
```
**Explanation:** Parentheses force subtraction before multiplication, matching the business rule of discounting first.

## Q34: Write a query to show each order item's gross total (price * quantity * 1.08) rounded to 2 decimals.
**Query:**
```sql
SELECT ROUND(price * quantity * 1.08, 2) AS total_with_tax FROM order_items;
```
**Explanation:** ROUND truncates the computed value to two decimal places for currency display.
**Alt1:**
```sql
SELECT CAST(price * quantity * 1.08 AS DECIMAL(10, 2)) AS total_with_tax FROM order_items;
```

## Q35: Write a query to display each customer's first_name converted to uppercase.
**Query:**
```sql
SELECT UPPER(first_name) AS first_name_upper FROM customers;
```
**Explanation:** UPPER transforms each row's value at selection time without modifying the stored data.
**Alt1:**
```sql
SELECT LOWER(last_name) AS last_name_lower FROM customers;
```

## Q36: Write a query to report the number of characters in each employee's first_name.
**Query:**
```sql
-- Oracle
SELECT LENGTH(first_name) AS name_length FROM employees;
```
**Explanation:** LENGTH counts characters per row in Oracle, PostgreSQL, and other ANSI systems.
**Alt1:**
```sql
-- SQL Server
SELECT LEN(first_name) AS name_length FROM employees;
```

## Q37: Write a query that removes surrounding whitespace from the display_name column of the users table.
**Query:**
```sql
SELECT TRIM(display_name) AS cleaned_name FROM users;
```
**Explanation:** TRIM strips leading and trailing spaces from the value in each selected row.
**Alt1:**
```sql
SELECT LTRIM(RTRIM(display_name)) AS cleaned_name FROM users;
```

## Q38: Write a query to show the first 5 characters of each customer's email address.
**Query:**
```sql
SELECT SUBSTRING(email, 1, 5) AS email_prefix FROM customers;
```
**Explanation:** SUBSTRING pulls 5 characters starting at position 1; same basic syntax in MySQL and SQL Server.
**Alt1:**
```sql
-- Oracle
SELECT SUBSTR(email, 1, 5) AS email_prefix FROM customers;
```

## Q39: Write a query to build a label such as 'Employee #42' by concatenating text with the employee_id number.
**Query:**
```sql
-- PostgreSQL
SELECT 'Employee #' || employee_id AS id_label FROM employees;
```
**Explanation:** `||` coerces the numeric id to text and concatenates left to right.
**Alt1:**
```sql
-- MySQL
SELECT CONCAT('Employee #', employee_id) AS id_label FROM employees;
```

## Q40: Write a query that renames first_name, last_name, and hire_date to fname, lname, and start_date.
**Query:**
```sql
SELECT first_name AS fname, last_name AS lname, hire_date AS start_date FROM employees;
```
**Explanation:** Every output column can carry its own alias, so the result is relabeled without touching column names.

## Q41: Write a query that aliases the status column as "order" even though order is a reserved word.
**Query:**
```sql
SELECT status AS "order" FROM orders;
```
**Explanation:** Double-quoting an alias lets reserved words and mixed case survive as an identifier.

## Q42: In one select list you need a 10% raised salary and its yearly total; write the query, noting aliases cannot be reused inside the same list.
**Query:**
```sql
SELECT salary * 1.10 AS increased, (salary * 1.10) * 12 AS annual FROM employees;
```
**Explanation:** A select-list alias is not referenceable elsewhere in the same SELECT, so the expression is repeated rather than reusing `increased`.

## Q43: Write a query to list the distinct salary bands produced by rounding each salary to the nearest 1000.
**Query:**
```sql
SELECT DISTINCT ROUND(salary, -3) AS salary_band FROM employees;
```
**Explanation:** DISTINCT collapses rows whose computed rounded value is the same, yielding one row per band.

## Q44: Write a query to list all distinct manager_id values, including groups of employees with no manager.
**Query:**
```sql
SELECT DISTINCT manager_id FROM employees;
```
**Explanation:** DISTINCT treats NULLs as equal to each other for deduplication, so a single NULL row appears once.

## Q45: Write a query that returns only 5 distinct job_title values.
**Query:**
```sql
SELECT DISTINCT job_title FROM employees LIMIT 5;
```
**Explanation:** Duplicate removal happens first, then LIMIT keeps 5 rows from the deduplicated set.
**Alt1:**
```sql
-- PostgreSQL
SELECT DISTINCT job_title FROM employees FETCH FIRST 5 ROWS ONLY;
```

## Q46: Write a query to list the distinct salary bands 'High' (>= 100000) or 'Standard' produced by a CASE expression.
**Query:**
```sql
SELECT DISTINCT CASE WHEN salary >= 100000 THEN 'High' ELSE 'Standard' END AS band FROM employees;
```
**Explanation:** The CASE runs per row, then DISTINCT collapses identical bands so each band appears once.

## Q47: Write a query that returns middle_name but substitutes an empty string when the value is NULL.
**Query:**
```sql
SELECT first_name, COALESCE(middle_name, '') AS middle_name FROM employees;
```
**Explanation:** COALESCE returns the first non-NULL argument, replacing missing middle names with an empty string.

## Q48: Write a query that maps order status codes ('S' shipped, 'P' pending, anything else unknown) into readable labels.
**Query:**
```sql
SELECT order_id, CASE status WHEN 'S' THEN 'Shipped' WHEN 'P' THEN 'Pending' ELSE 'Unknown' END AS status_label FROM orders;
```
**Explanation:** The simple CASE compares `status` against each `WHEN` value and returns the first match.
**Alt1:**
```sql
SELECT order_id, CASE WHEN status = 'S' THEN 'Shipped' WHEN status = 'P' THEN 'Pending' ELSE 'Unknown' END AS status_label FROM orders;
```

## Q49: Write a query that classifies each employee's salary level as Senior, Mid, or Junior.
**Query:**
```sql
SELECT first_name, CASE WHEN salary >= 100000 THEN 'Senior' WHEN salary >= 60000 THEN 'Mid' ELSE 'Junior' END AS level FROM employees;
```
**Explanation:** The searched CASE evaluates conditions top-down and returns the first true branch.

## Q50: Write a query that charges 2.5 per unit of weight for EMEA orders and 1.5 for all other regions, computed in the select list.
**Query:**
```sql
SELECT order_id, CASE WHEN region = 'EMEA' THEN weight * 2.5 ELSE weight * 1.5 END AS shipping_cost FROM shipments;
```
**Explanation:** CASE selects which arithmetic expression produces each row's shipping cost.
## Q51: Write a query that grades a numeric score as A, B+, B, or C using nested CASE branches.
**Query:**
```sql
SELECT student_id, score, CASE WHEN score >= 90 THEN 'A'
                              WHEN score >= 80 THEN CASE WHEN score >= 85 THEN 'B+' ELSE 'B' END
                              ELSE 'C' END AS grade FROM results;
```
**Explanation:** A CASE inside a WHEN branch refines the B bucket; the inner CASE only runs when the outer branch is reached.

## Q52: Write a query that prefixes each user's first_name with ': active' or ': inactive' based on a boolean flag, using CASE inside a concatenation.
**Query:**
```sql
-- PostgreSQL
SELECT first_name || ': ' || CASE WHEN active THEN 'active' ELSE 'inactive' END AS line FROM users;
```
**Explanation:** The CASE result is a string literal that becomes part of the concatenated output value.

## Q53: Write a query that multiplies an order's quantity by 2 when the expedited flag is true, else by 1.
**Query:**
```sql
SELECT order_id, quantity * CASE WHEN expedited THEN 2 ELSE 1 END AS weighted_qty FROM line_items;
```
**Explanation:** CASE returns a numeric factor that participates directly in the row's arithmetic.

## Q54: Write a query to compute each patient's BMI as weight divided by height squared.
**Query:**
```sql
SELECT patient_id, weight_kg / (height_m * height_m) AS bmi FROM patients;
```
**Explanation:** The denominator is computed as a subexpression before division is applied per row.

## Q55: Write a query to display each employee's approximate age computed from birth_date.
**Query:**
```sql
-- MySQL
SELECT first_name, YEAR(CURRENT_DATE) - YEAR(birth_date) AS age FROM employees;
```
**Explanation:** Extracting the year from both dates and subtracting gives a whole-year age approximation.
**Alt1:**
```sql
-- PostgreSQL
SELECT first_name, EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM birth_date) AS age FROM employees;
```

## Q56: Write a query that shows how many days have passed since each order was placed.
**Query:**
```sql
-- PostgreSQL
SELECT order_id, CURRENT_DATE - order_date AS days_since_order FROM orders;
```
**Explanation:** In PostgreSQL, subtracting a date from a date returns an integer day count.

## Q57: Write a query that shows each order's due date as 30 days after order_date.
**Query:**
```sql
-- MySQL
SELECT order_id, DATE_ADD(order_date, INTERVAL 30 DAY) AS due_date FROM orders;
```
**Explanation:** DATE_ADD shifts the stored date by the given interval and returns a date value.
**Alt1:**
```sql
-- PostgreSQL
SELECT order_id, order_date + INTERVAL '30 days' AS due_date FROM orders;
```

## Q58: Write a query (Oracle) that shows each insurance policy's renewal date one year after its start_date.
**Query:**
```sql
-- Oracle
SELECT policy_id, ADD_MONTHS(start_date, 12) AS renewal_date FROM policies;
```
**Explanation:** ADD_MONTHS adds 12 calendar months to the date, handling month-end rollover automatically.
**Alt1:**
```sql
-- MySQL
SELECT policy_id, DATE_ADD(start_date, INTERVAL 1 YEAR) AS renewal_date FROM policies;
```

## Q59: Write a query to report only the month portion of each order's order_date.
**Query:**
```sql
-- PostgreSQL
SELECT order_id, EXTRACT(MONTH FROM order_date) AS order_month FROM orders;
```
**Explanation:** EXTRACT pulls one date part (month here) out of the value into a numeric column.
**Alt1:**
```sql
-- MySQL
SELECT order_id, MONTH(order_date) AS order_month FROM orders;
```

## Q60: Write a query that casts the price column to a fixed two-decimal DECIMAL for consistent display.
**Query:**
```sql
SELECT product_name, CAST(price AS DECIMAL(10, 2)) AS price_2dp FROM products;
```
**Explanation:** CAST converts the value's type at selection time, normalizing precision across rows.
**Alt1:**
```sql
-- MySQL
SELECT product_name, FORMAT(price, 2) AS price_2dp FROM products;
```

## Q61: Write an Oracle query that formats the salary column as currency with commas, e.g. '$100,000.00'.
**Query:**
```sql
-- Oracle
SELECT employee_id, TO_CHAR(salary, 'FM$999,999.00') AS formatted_salary FROM employees;
```
**Explanation:** TO_CHAR renders the number into the given money mask; FM removes leading blank padding.

## Q62: Write an Oracle query that converts order_date into the text format YYYY-MM-DD.
**Query:**
```sql
-- Oracle
SELECT order_id, TO_CHAR(order_date, 'YYYY-MM-DD') AS order_date_text FROM orders;
```
**Explanation:** TO_CHAR reformats the date value into a display string without changing the column's type.

## Q63: Write a query to list the distinct full names built from first_name and last_name.
**Query:**
```sql
-- PostgreSQL
SELECT DISTINCT first_name || ' ' || last_name AS full_name FROM employees;
```
**Explanation:** Each row's concatenated name is deduplicated so identical full names appear once.
**Alt1:**
```sql
-- MySQL
SELECT DISTINCT CONCAT(first_name, ' ', last_name) AS full_name FROM employees;
```

## Q64: Write a query using SQL Server's + operator to build distinct full names.
**Query:**
```sql
-- SQL Server
SELECT DISTINCT first_name + ' ' + last_name AS full_name FROM customers;
```
**Explanation:** SQL Server uses `+` for string concatenation (and for numeric addition, hence the DISTINCT protects intent).

## Q65: Write a query that maps single-letter gender codes M and F to readable labels.
**Query:**
```sql
SELECT employee_id, CASE gender WHEN 'M' THEN 'Male' WHEN 'F' THEN 'Female' ELSE 'Unspecified' END AS gender_label FROM employees;
```
**Explanation:** Simple CASE compares the column against each literal and substitutes the matching label.
**Alt1:**
```sql
SELECT employee_id, CASE WHEN gender = 'M' THEN 'Male' WHEN gender = 'F' THEN 'Female' ELSE 'Unspecified' END AS gender_label FROM employees;
```

## Q66: Write a query that caps total pay (base salary plus bonus) at 200000, using COALESCE inside the CASE condition and result.
**Query:**
```sql
SELECT employee_id, CASE WHEN base_salary + COALESCE(bonus, 0) > 200000 THEN 200000 ELSE base_salary + COALESCE(bonus, 0) END AS capped_total FROM employees;
```
**Explanation:** COALESCE nulls out missing bonuses before the sum, and CASE returns the cap or the true total.
**Alt1:**
```sql
SELECT employee_id, LEAST(base_salary + COALESCE(bonus, 0), 200000) AS capped_total FROM employees;
```

## Q67: Write a query that selects every employee column except the department_id column by listing them explicitly.
**Query:**
```sql
SELECT employee_id, first_name, last_name, email, hire_date, salary FROM employees;
```
**Explanation:** There is no portable "all columns except one" syntax, so the wanted columns are enumerated by name.

## Q68: Write a query that lists the distinct country values using a fully qualified column name.
**Query:**
```sql
SELECT DISTINCT customers.country FROM customers;
```
**Explanation:** The table-qualified reference resolves the column even if another table in scope shares the name.

## Q69: Write a query to show distinct effective prices computed as price reduced by its discount.
**Query:**
```sql
SELECT DISTINCT ROUND(price * (1 - discount), 2) AS effective_price FROM products;
```
**Explanation:** The discounted value is computed and rounded per row, then duplicates collapse across rows.

## Q70: Write a SQL Server query returning the top 5 rows of a margin column (price minus cost).
**Query:**
```sql
-- SQL Server
SELECT TOP 5 product_name, price - cost AS margin FROM products;
```
**Explanation:** The computed margin is produced for every row before TOP trims the result to 5 rows.

## Q71: Write a query that skips the first 1000 rows and returns the next 20 (page 51 of 20-row pages).
**Query:**
```sql
-- MySQL
SELECT * FROM employees LIMIT 20 OFFSET 1000;
```
**Explanation:** OFFSET discards rows before LIMIT picks the following 20, enabling deep pagination.
**Alt1:**
```sql
-- SQL Server
SELECT * FROM employees ORDER BY employee_id OFFSET 1000 ROWS FETCH NEXT 20 ROWS ONLY;
```

## Q72: Write an Oracle query returning the first 10 rows of the orders table using ROWNUM.
**Query:**
```sql
-- Oracle
SELECT * FROM orders WHERE ROWNUM <= 10;
```
**Explanation:** ROWNUM assigns a row number before the limit is applied, so filtering it yields the first 10 rows.

## Q73: Write an Oracle 12c+ query returning the first 10 rows using the ANSI FETCH clause.
**Query:**
```sql
-- Oracle
SELECT * FROM orders FETCH FIRST 10 ROWS ONLY;
```
**Explanation:** FETCH FIRST is the modern, readable row-limiting replacement for ROWNUM in Oracle.

## Q74: Write a query that returns the higher of the paid price and 90 percent of the list price for each sale.
**Query:**
```sql
SELECT sale_id, GREATEST(price_paid, list_price * 0.9) AS effective_price FROM sales;
```
**Explanation:** GREATEST evaluates both arguments per row and returns the larger, functioning as an in-line max.
**Alt1:**
```sql
SELECT sale_id, CASE WHEN price_paid > list_price * 0.9 THEN price_paid ELSE list_price * 0.9 END AS effective_price FROM sales;
```

## Q75: Write a query that computes each account's future value using compound interest: deposit * (1 + rate) raised to the power of years.
**Query:**
```sql
SELECT account_id, deposit * POWER(1 + interest_rate, years) AS future_value FROM accounts;
```
**Explanation:** POWER computes the compound factor and the deposit multiplies it in the same select expression.
## Q76: Write a query to list every distinct combination of city, state, and zip_code from the customers table.
**Query:**
```sql
SELECT DISTINCT city, state, zip_code FROM customers;
```
**Explanation:** Deduplication applies to the full three-column tuple; a row is dropped only if all three match.

## Q77: Write a query computing total pay as salary * 12 plus a bracketed mix of bonus and stock value.
**Query:**
```sql
SELECT employee_id, salary * 12 + (bonus + stocks * 100) AS total_pay FROM employees;
```
**Explanation:** The inner expression is evaluated first, then added to the annual salary figure per row.

## Q78: Write a query that labels Engineer and Scientist job titles as Technical and everything else Other.
**Query:**
```sql
SELECT first_name, CASE WHEN job_title IN ('Engineer', 'Scientist') THEN 'Technical' ELSE 'Other' END AS class FROM employees;
```
**Explanation:** IN inside the searched CASE branch tests the column against a small set in one condition.

## Q79: Write a query that prioritizes open orders over 1000 as 'urgent' and everything else 'normal'.
**Query:**
```sql
SELECT order_id, CASE WHEN status = 'open' AND amount > 1000 THEN 'urgent' ELSE 'normal' END AS priority FROM orders;
```
**Explanation:** AND combines two predicates in the CASE branch so both must hold for the urgent label.

## Q80: Write a query listing the distinct regional labels US/CA = 'North America', DE/FR/ES = 'Europe', else 'Other'.
**Query:**
```sql
SELECT DISTINCT CASE WHEN country IN ('US', 'CA') THEN 'North America' WHEN country IN ('DE', 'FR', 'ES') THEN 'Europe' ELSE 'Other' END AS region FROM customers;
```
**Explanation:** Each row's country maps to a region via CASE, and DISTINCT collapses repeated region labels.

## Q81: Write a query that selects first_name and last_name from the customers table aliased as c using the alias for qualification.
**Query:**
```sql
SELECT c.first_name, c.last_name FROM customers AS c;
```
**Explanation:** Qualified names through the alias keep the select list readable and unambiguous for later joins.

## Q82: Write a query, without a FROM clause, that returns the current timestamp.
**Query:**
```sql
SELECT CURRENT_TIMESTAMP;
```
**Explanation:** CURRENT_TIMESTAMP yields date and time together; CURRENT_DATE would give the date only.
**Alt1:**
```sql
-- Oracle
SELECT SYSDATE FROM DUAL;
```

## Q83: Write a query that strips the hyphens from each customer's phone number.
**Query:**
```sql
SELECT customer_id, REPLACE(phone, '-', '') AS phone_digits FROM customers;
```
**Explanation:** REPLACE swaps every '-' with an empty string as the value is projected.

## Q84: Write a query that reports where '@' first appears inside each customer's email address.
**Query:**
```sql
-- PostgreSQL
SELECT email, POSITION('@' IN email) AS at_pos FROM customers;
```
**Explanation:** POSITION returns the 1-based index of the substring, which is 0 when absent.
**Alt1:**
```sql
-- SQL Server
SELECT email, CHARINDEX('@', email) AS at_pos FROM customers;
```

## Q85: Write a query extracting the local part of each email address, the text before '@'.
**Query:**
```sql
-- PostgreSQL
SELECT email, SUBSTRING(email, 1, POSITION('@' IN email) - 1) AS local_part FROM customers;
```
**Explanation:** POSITION locates '@' and the SUBSTRING length argument trims one character to cut it off.

## Q86: Write a query to count the distinct full names built from first_name and last_name.
**Query:**
```sql
-- PostgreSQL
SELECT COUNT(DISTINCT first_name || ' ' || last_name) AS unique_names FROM employees;
```
**Explanation:** Concatenated names are deduplicated before counting, returning a scalar row count.

## Q87: Write a query that removes completely duplicate rows from the employees result.
**Query:**
```sql
SELECT DISTINCT * FROM employees;
```
**Explanation:** DISTINCT over * drops rows where every column exactly matches another row's.
**Alt1:**
```sql
SELECT DISTINCT employee_id, first_name, last_name, email, hire_date, salary FROM employees;
```

## Q88: Write a query classifying products as 'Deep discount', 'Promo', or 'Regular' by their discount values.
**Query:**
```sql
SELECT product_name, CASE WHEN discount > 0.5 THEN 'Deep discount' WHEN discount BETWEEN 0.2 AND 0.5 THEN 'Promo' ELSE 'Regular' END AS tier FROM products;
```
**Explanation:** BETWEEN in the second branch forms an inclusive range; the ELSE catches everything below 0.2.

## Q89: Write a query computing each ad's click-through rate as clicks divided by impressions as a percentage.
**Query:**
```sql
SELECT ad_id, clicks * 100.0 / impressions AS ctr FROM ads;
```
**Explanation:** Multiplying by 100.0 first promotes the arithmetic to decimals, avoiding integer truncation.
**Alt1:**
```sql
SELECT ad_id, ROUND(clicks * 100.0 / impressions, 2) AS ctr FROM ads;
```

## Q90: Write a SQL Server query computing each employee's age in years from birth_date using DATEDIFF.
**Query:**
```sql
-- SQL Server
SELECT first_name, DATEDIFF(YEAR, birth_date, GETDATE()) AS age FROM employees;
```
**Explanation:** DATEDIFF counts year boundaries between the two dates; GETDATE() supplies today.
**Alt1:**
```sql
-- SQL Server
SELECT first_name, DATEDIFF(YEAR, birth_date, CURRENT_TIMESTAMP) AS age FROM employees;
```

## Q91: Write a MySQL query reporting how many whole days each order has been open.
**Query:**
```sql
-- MySQL
SELECT order_id, TIMESTAMPDIFF(DAY, order_date, CURRENT_DATE) AS days_open FROM orders;
```
**Explanation:** TIMESTAMPDIFF returns the full interval units between two dates in the requested part.

## Q92: Write a query that returns the first 3 rows of a stock status label ('Low' when stock is below 10).
**Query:**
```sql
SELECT product_name, CASE WHEN stock < 10 THEN 'Low' ELSE 'OK' END AS stock_status FROM inventory LIMIT 3;
```
**Explanation:** The CASE label is computed per row, then LIMIT trims the output to the first 3 rows.

## Q93: Write a query showing the distinct payment methods, substituting 'Unknown' for NULL values.
**Query:**
```sql
SELECT DISTINCT COALESCE(payment_method, 'Unknown') AS method FROM payments;
```
**Explanation:** COALESCE fills missing methods before DISTINCT deduplicates the normalized values.

## Q94: Write a query that builds a full name after trimming spaces from first_name and last_name.
**Query:**
```sql
-- PostgreSQL
SELECT TRIM(first_name) || ' ' || TRIM(last_name) AS full_name FROM employees;
```
**Explanation:** Values are cleaned with TRIM before concatenation so stray spaces never inflate the name.

## Q95: Write a query showing each product's profit margin percentage as (price - cost) / cost * 100, rounded to 1 decimal.
**Query:**
```sql
SELECT product_name, ROUND((price - cost) * 100.0 / cost, 1) AS margin_pct FROM products;
```
**Explanation:** The margin fraction is scaled by 100.0 (avoiding integer division) and rounded to one decimal.

## Q96: Write a query computing each line item's final total as quantity * price after applying a promo percentage discount.
**Query:**
```sql
SELECT order_id, quantity * price * (1 - COALESCE(promo_pct, 0)) AS final_total FROM line_items;
```
**Explanation:** COALESCE converts a missing promo to zero, then the parenthesized factor applies the discount.

## Q97: Write a query that returns only employees earning over 100000 and labels their salary band High or Mid in the select list.
**Query:**
```sql
SELECT first_name, salary, CASE WHEN salary >= 120000 THEN 'High' ELSE 'Mid' END AS band FROM employees WHERE salary > 100000;
```
**Explanation:** WHERE narrows the rows first and the CASE derives the band from each surviving row's salary.

## Q98: Write a query listing the distinct job titles held by employees in the Sales department.
**Query:**
```sql
SELECT DISTINCT job_title FROM employees WHERE department = 'Sales';
```
**Explanation:** DISTINCT applies after the WHERE filter, so each Sales title is reported exactly once.

## Q99: Write a query that returns 10 active employees, selecting id, first_name, and last_name.
**Query:**
```sql
SELECT employee_id, first_name, last_name FROM employees WHERE status = 'active' LIMIT 10;
```
**Explanation:** The status filter runs first, then LIMIT keeps the first 10 matching rows.

## Q100: Write a query that returns the first 10 distinct rows of full names alongside a concatenated salary label such as 'Salary: 85000'.
**Query:**
```sql
-- PostgreSQL
SELECT DISTINCT
  first_name || ' ' || last_name AS full_name,
  'Salary: ' || CAST(salary AS TEXT) AS salary_label
FROM employees
FETCH FIRST 10 ROWS ONLY;
```
**Explanation:** It combines concatenation, CAST to text, literal suffix, DISTINCT dedup, aliases, and FETCH limiting — a full tour of SELECT techniques in one query.
