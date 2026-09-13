# String Manipulation in SQL — 100 Interview Q&A

## Q1: Concatenate two columns 'first_name' and 'last_name' with a space in between.

**Query:**
```sql
SELECT CONCAT(first_name, ' ', last_name) AS full_name
FROM employees;
```
**Explanation:** `CONCAT` treats NULL as empty string in MySQL/PostgreSQL. SQL Server also supports `CONCAT`.

**Alt1 (SQL Server — `+` operator):**
```sql
-- SQL Server
SELECT first_name + ' ' + last_name AS full_name
FROM employees;
```
**Explanation:** The `+` operator in SQL Server propagates NULL — if either column is NULL the result is NULL. Use `CONCAT` to avoid that.

---

## Q2: Concatenate two columns using the `||` operator.

**Query:**
```sql
SELECT first_name || ' ' || last_name AS full_name
FROM employees;
```
**Explanation:** `||` is standard SQL and works in PostgreSQL, Oracle, and SQLite. MySQL ignores `||` in default mode (treats it as OR).

**Alt1 (MySQL — enable PIPES_AS_CONCAT):**
```sql
-- MySQL
SET sql_mode = 'PIPES_AS_CONCAT';
SELECT first_name || ' ' || last_name AS full_name
FROM employees;
```
**Explanation:** Enabling `PIPES_AS_CONCAT` makes MySQL treat `||` as string concatenation instead of logical OR.

---

## Q3: Convert all product names to uppercase.

**Query:**
```sql
SELECT UPPER(product_name) AS product_name_upper
FROM products;
```
**Explanation:** `UPPER` is supported across all major SQL dialects.

**Alt1 (PostgreSQL — `UPPER` is standard):**
```sql
-- PostgreSQL (identical, shown for dialect clarity)
SELECT UPPER(product_name) AS product_name_upper
FROM products;
```
**Explanation:** `UPPER` behaves identically in PostgreSQL. Some databases (Oracle) also offer `UPPER` with NLS-awareness.

---

## Q4: Convert a string to lowercase.

**Query:**
```sql
SELECT LOWER(email) AS email_lower
FROM users;
```
**Explanation:** `LOWER` is the standard counterpart to `UPPER` and works in all dialects.

---

## Q5: Capitalize the first letter of each word in a customer's name.

**Query:**
```sql
-- PostgreSQL
SELECT INITCAP(first_name || ' ' || last_name) AS full_name
FROM customers;
```
**Explanation:** `INITCAP` uppercases the first letter of each word and lowercases the rest. It is PostgreSQL/Oracle-specific.

**Alt1 (MySQL — manual approach):**
```sql
-- MySQL
SELECT CONCAT(
  UCASE(LEFT(first_name, 1)),
  LCASE(SUBSTRING(first_name, 2)),
  ' ',
  UCASE(LEFT(last_name, 1)),
  LCASE(SUBSTRING(last_name, 2))
) AS full_name
FROM customers;
```
**Explanation:** MySQL lacks `INITCAP`, so we capitalize the first character and lowercase the rest for each name part.

**Alt2 (SQL Server):**
```sql
-- SQL Server
SELECT STRING_AGG(
  UPPER(LEFT(value, 1)) + LOWER(SUBSTRING(value, 2, LEN(value))),
  ' '
) WITHIN GROUP (ORDER BY ordinal)
FROM (
  SELECT value, ordinal
  FROM STRING_SPLIT('john doe', ' ')
) parts;
```
**Explanation:** SQL Server can simulate `INITCAP` using `STRING_SPLIT` with ordinal support (2022+) or a CLR function.

---

## Q6: Trim leading and trailing spaces from a product description.

**Query:**
```sql
SELECT TRIM(description) AS cleaned_description
FROM products;
```
**Explanation:** `TRIM` removes leading and trailing whitespace. Supported in all dialects.

**Alt1 (SQL Server — `LTRIM` + `RTRIM`):**
```sql
-- SQL Server (older versions)
SELECT RTRIM(LTRIM(description)) AS cleaned_description
FROM products;
```
**Explanation:** Older SQL Server versions required nesting `LTRIM` and `RTRIM`. SQL Server 2017+ supports `TRIM`.

---

## Q7: Remove only leading spaces from a text column.

**Query:**
```sql
SELECT LTRIM(raw_text) AS left_trimmed
FROM staging;
```
**Explanation:** `LTRIM` removes leading whitespace only. Works across all dialects.

---

## Q8: Remove only trailing spaces from a text column.

**Query:**
```sql
SELECT RTRIM(raw_text) AS right_trimmed
FROM staging;
```
**Explanation:** `RTRIM` removes trailing whitespace only. Works across all dialects.

---

## Q9: Extract the first 5 characters from a order_code column.

**Query:**
```sql
-- PostgreSQL / MySQL
SELECT SUBSTRING(order_code, 1, 5) AS prefix
FROM orders;
```
**Explanation:** `SUBSTRING(string, start, length)` extracts a portion. SQL Server uses the same syntax; Oracle uses `SUBSTR`.

**Alt1 (Oracle):**
```sql
-- Oracle
SELECT SUBSTR(order_code, 1, 5) AS prefix
FROM orders;
```
**Explanation:** Oracle uses `SUBSTR` instead of `SUBSTRING`. Both start at position 1 by default.

---

## Q10: Extract the last 4 characters from a phone number column.

**Query:**
```sql
-- PostgreSQL / MySQL
SELECT SUBSTRING(phone, LENGTH(phone) - 3, 4) AS last_four
FROM contacts;
```
**Explanation:** We calculate the starting position using `LENGTH` and extract the last 4 characters.

**Alt1 (SQL Server — `RIGHT`):**
```sql
-- SQL Server
SELECT RIGHT(phone, 4) AS last_four
FROM contacts;
```
**Explanation:** `RIGHT` extracts characters from the end of a string. MySQL also supports `RIGHT`.

---

## Q11: Use `LEFT` to grab the area code (first 3 digits) from a phone number.

**Query:**
```sql
SELECT LEFT(phone, 3) AS area_code
FROM contacts;
```
**Explanation:** `LEFT(string, n)` returns the first `n` characters. Works in MySQL and SQL Server.

**Alt1 (PostgreSQL — `SUBSTRING`):**
```sql
-- PostgreSQL
SELECT SUBSTRING(phone FROM 1 FOR 3) AS area_code
FROM contacts;
```
**Explanation:** PostgreSQL supports the `SUBSTRING(string FROM start FOR length)` standard SQL syntax.

---

## Q12: Get the length of a string in characters (not bytes).

**Query:**
```sql
-- MySQL / PostgreSQL
SELECT CHAR_LENGTH(description) AS char_count
FROM products;
```
**Explanation:** `CHAR_LENGTH` returns the number of characters. `LENGTH` in MySQL returns bytes (important for multibyte encodings).

**Alt1 (SQL Server — `LEN`):**
```sql
-- SQL Server
SELECT LEN(description) AS char_count
FROM products;
```
**Explanation:** `LEN` in SQL Server counts characters and trims trailing spaces. MySQL's `CHAR_LENGTH` is the equivalent.

**Alt2 (Oracle):**
```sql
-- Oracle
SELECT LENGTH(description) AS char_count
FROM products;
```
**Explanation:** Oracle's `LENGTH` returns characters (not bytes). Use `LENGTHB` for byte count.

---

## Q13: Replace all occurrences of ' Inc' with ' Inc.' in company names.

**Query:**
```sql
SELECT REPLACE(company_name, ' Inc', ' Inc.') AS corrected_name
FROM companies;
```
**Explanation:** `REPLACE(string, old, new)` substitutes all occurrences. Supported across all dialects.

---

## Q14: Use `TRANSLATE` to swap vowels with dashes in a username.

**Query:**
```sql
-- PostgreSQL / Oracle
SELECT TRANSLATE(username, 'aeiou', '-----') AS masked_name
FROM users;
```
**Explanation:** `TRANSLATE` performs character-by-character substitution. Each character in the second argument is replaced by the corresponding character in the third.

**Alt1 (MySQL — `REPLACE` chain):**
```sql
-- MySQL
SELECT REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
  username, 'a', '-'), 'e', '-'), 'i', '-'), 'o', '-'), 'u', '-') AS masked_name
FROM users;
```
**Explanation:** MySQL lacks `TRANSLATE`, so we chain nested `REPLACE` calls for each character.

---

## Q15: Find the position of '@' in an email address.

**Query:**
```sql
SELECT POSITION('@' IN email) AS at_position
FROM users;
```
**Explanation:** `POSITION(substring IN string)` is standard SQL. Returns 0 if not found.

**Alt1 (MySQL — `LOCATE`):**
```sql
-- MySQL
SELECT LOCATE('@', email) AS at_position
FROM users;
```
**Explanation:** MySQL uses `LOCATE(substring, string)`. Returns 0 if not found.

**Alt2 (SQL Server — `CHARINDEX`):**
```sql
-- SQL Server
SELECT CHARINDEX('@', email) AS at_position
FROM users;
```
**Explanation:** SQL Server uses `CHARINDEX`. Returns 0 if not found. An optional third parameter sets the start position.

---

## Q16: Extract the domain (everything after '@') from an email address.

**Query:**
```sql
SELECT SUBSTRING(email FROM POSITION('@' IN email) + 1) AS domain
FROM users;
```
**Explanation:** We find the position of `@` and extract everything after it using `SUBSTRING`.

**Alt1 (MySQL — `SUBSTRING_INDEX`):**
```sql
-- MySQL
SELECT SUBSTRING_INDEX(email, '@', -1) AS domain
FROM users;
```
**Explanation:** `SUBSTRING_INDEX` with a negative count returns everything after the last occurrence of the delimiter.

**Alt2 (PostgreSQL — `SPLIT_PART`):**
```sql
-- PostgreSQL
SELECT SPLIT_PART(email, '@', 2) AS domain
FROM users;
```
**Explanation:** `SPLIT_PART(string, delimiter, position)` splits on the delimiter and returns the specified part.

---

## Q17: Extract the username (everything before '@') from an email address.

**Query:**
```sql
SELECT SUBSTRING(email, 1, POSITION('@' IN email) - 1) AS username
FROM users;
```
**Explanation:** We extract characters from position 1 up to (but not including) the `@` sign.

**Alt1 (MySQL):**
```sql
-- MySQL
SELECT SUBSTRING_INDEX(email, '@', 1) AS username
FROM users;
```
**Explanation:** `SUBSTRING_INDEX` with count `1` returns everything before the first occurrence of the delimiter.

---

## Q18: Extract the domain name without the TLD (e.g., 'gmail' from 'user@gmail.com').

**Query:**
```sql
-- MySQL
SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(email, '@', -1), '.', 1) AS domain_name
FROM users;
```
**Explanation:** First extract the domain with `SUBSTRING_INDEX(..., '@', -1)`, then extract the part before the first dot.

**Alt1 (PostgreSQL):**
```sql
-- PostgreSQL
SELECT SPLIT_PART(SPLIT_PART(email, '@', 2), '.', 1) AS domain_name
FROM users;
```
**Explanation:** Nested `SPLIT_PART` calls: first get the domain, then get the part before the first dot.

---

## Q19: Extract the first name from a full name column that uses space as delimiter.

**Query:**
```sql
SELECT SUBSTRING_INDEX(full_name, ' ', 1) AS first_name
FROM customers;
```
**Explanation:** `SUBSTRING_INDEX` with count `1` returns everything before the first space.

**Alt1 (PostgreSQL):**
```sql
-- PostgreSQL
SELECT SPLIT_PART(full_name, ' ', 1) AS first_name
FROM customers;
```
**Explanation:** `SPLIT_PART` with position `1` returns the first token.

---

## Q20: Extract the last name from a full name column.

**Query:**
```sql
-- MySQL
SELECT SUBSTRING_INDEX(full_name, ' ', -1) AS last_name
FROM customers;
```
**Explanation:** Negative index `-1` returns everything after the last space, giving the last name.

**Alt1 (PostgreSQL):**
```sql
-- PostgreSQL
SELECT SPLIT_PART(full_name, ' ', ARRAY_LENGTH(STRING_TO_ARRAY(full_name, ' '), 1)) AS last_name
FROM customers;
```
**Explanation:** Calculate the number of parts and use that as the position in `SPLIT_PART`.

---

## Q21: Extract the middle name from a three-part full name (first middle last).

**Query:**
```sql
-- MySQL
SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(full_name, ' ', 2), ' ', -1) AS middle_name
FROM customers;
```
**Explanation:** First get the first two parts with `SUBSTRING_INDEX(..., ' ', 2)`, then extract the last part of that result.

**Alt1 (PostgreSQL):**
```sql
-- PostgreSQL
SELECT SPLIT_PART(full_name, ' ', 2) AS middle_name
FROM customers;
```
**Explanation:** Since we know there are exactly 3 parts, position `2` gives the middle name directly.

---

## Q22: Remove all spaces from a string.

**Query:**
```sql
SELECT REPLACE(whole_address, ' ', '') AS no_spaces
FROM addresses;
```
**Explanation:** Replacing space with empty string effectively removes all spaces.

---

## Q23: Replace multiple consecutive spaces with a single space.

**Query:**
```sql
-- MySQL
SELECT TRIM(REGEXP_REPLACE(description, '\\s+', ' ')) AS cleaned
FROM articles;
```
**Explanation:** `REGEXP_REPLACE` replaces runs of whitespace with a single space, then `TRIM` removes leading/trailing.

**Alt1 (PostgreSQL):**
```sql
-- PostgreSQL
SELECT TRIM(REGEXP_REPLACE(description, '\s+', ' ', 'g')) AS cleaned
FROM articles;
```
**Explanation:** PostgreSQL's `REGEXP_REPLACE` requires the `'g'` flag for global replacement.

**Alt2 (SQL Server):**
```sql
-- SQL Server
SELECT TRIM(REGEXP_REPLACE(description, '\s+', ' ')) AS cleaned
FROM articles;
```
**Explanation:** SQL Server 2017+ supports `REGEXP_REPLACE`. Earlier versions need a recursive CTE or CLR function.

---

## Q24: Pad a numeric ID with leading zeros to make it 6 digits wide.

**Query:**
```sql
-- MySQL
SELECT LPAD(CAST(id AS CHAR), 6, '0') AS padded_id
FROM orders;
```
**Explanation:** `LPAD(string, length, pad_char)` pads on the left. We cast the integer to string first.

**Alt1 (PostgreSQL):**
```sql
-- PostgreSQL
SELECT LPAD(id::TEXT, 6, '0') AS padded_id
FROM orders;
```
**Explanation:** PostgreSQL uses `::TEXT` for casting. `LPAD` works the same.

**Alt2 (Oracle):**
```sql
-- Oracle
SELECT LPAD(TO_CHAR(id), 6, '0') AS padded_id
FROM orders;
```
**Explanation:** Oracle uses `TO_CHAR` for number-to-string conversion.

**Alt3 (SQL Server — `FORMAT`):**
```sql
-- SQL Server
SELECT FORMAT(id, 'D6') AS padded_id
FROM orders;
```
**Explanation:** `FORMAT(id, 'D6')` produces a 6-digit decimal string with leading zeros.

---

## Q25: Right-pad a product code to a fixed width of 10 characters with asterisks.

**Query:**
```sql
SELECT RPAD(product_code, 10, '*') AS padded_code
FROM products;
```
**Explanation:** `RPAD` pads on the right with the specified fill character. Works in MySQL, PostgreSQL, and Oracle.

**Alt1 (SQL Server):**
```sql
-- SQL Server (no built-in RPAD before 2022)
SELECT product_code + REPLICATE('*', 10 - LEN(product_code)) AS padded_code
FROM products
WHERE LEN(product_code) <= 10;
```
**Explanation:** SQL Server uses `REPLICATE` to repeat a character, then concatenates it to the right of the string.


## Q26: Count how many times the letter 'a' appears in each sentence.

**Query:**
```sql
SELECT sentence,
       CHAR_LENGTH(sentence) - CHAR_LENGTH(REPLACE(sentence, 'a', '')) AS count_a
FROM sentences;
```
**Explanation:** The classic trick — remove the target character, then the difference in length equals the number of occurrences.

**Alt1 (SQL Server — `LEN`):**
```sql
-- SQL Server
SELECT sentence,
       LEN(sentence) - LEN(REPLACE(sentence, 'a', '')) AS count_a
FROM sentences;
```
**Explanation:** Same length-difference approach using SQL Server's `LEN`.

**Alt2 (PostgreSQL — `ARRAY_LENGTH`):**
```sql
-- PostgreSQL
SELECT sentence,
       ARRAY_LENGTH(STRING_TO_ARRAY(sentence, ''), 1) -
       ARRAY_LENGTH(STRING_TO_ARRAY(REPLACE(sentence, 'a', ''), ''), 1) AS count_a
FROM sentences;
```
**Explanation:** Convert the string (and the string without 'a') into arrays of characters and compare array lengths.

---

## Q27: Count the occurrences of the substring 'the' (case-insensitive) in a body of text.

**Query:**
```sql
-- MySQL
SELECT title,
       (CHAR_LENGTH(LOWER(text_body))
        - CHAR_LENGTH(REPLACE(LOWER(text_body), 'the', ''))) / CHAR_LENGTH('the') AS count_the
FROM articles;
```
**Explanation:** Lowercase both sides first for case-insensitivity, then use the length-difference trick divided by the search string length.

**Alt1 (PostgreSQL — `REGEXP_COUNT`):**
```sql
-- PostgreSQL
SELECT title,
       REGEXP_COUNT(text_body, 'the', 'i') AS count_the
FROM articles;
```
**Explanation:** `REGEXP_COUNT` (Oracle and PostgreSQL 15+) counts regex matches directly with the `'i'` flag for case-insensitive.

---

## Q28: Find all email addresses that belong to the 'example.com' domain.

**Query:**
```sql
SELECT email
FROM users
WHERE email LIKE '%@example.com';
```
**Explanation:** `LIKE` with a `%` wildcard matches the ending `@example.com`.

**Alt1 (Exact suffix check with `RIGHT`):**
```sql
SELECT email
FROM users
WHERE RIGHT(email, 12) = '@example.com';
```
**Explanation:** `RIGHT` extracts the suffix and compares with `=`. Avoids wildcard issues if `@` appears more than once.

---

## Q29: Filter rows where the name starts with 'A' followed by exactly two characters.

**Query:**
```sql
SELECT name
FROM students
WHERE name LIKE 'A__';
```
**Explanation:** The single-underscore wildcard `_` matches exactly one character.

---

## Q30: Find names containing a literal percent sign.

**Query:**
```sql
SELECT name
FROM products
WHERE name LIKE '%\%%' ESCAPE '\';
```
**Explanation:** Without an escape character, `%` is a wildcard. The `ESCAPE '\'` clause lets us match a literal `%`.

**Alt1 (PostgreSQL — positional escape):**
```sql
-- PostgreSQL
SELECT name
FROM products
WHERE name LIKE '%!%%' ESCAPE '!';
```
**Explanation:** Any character can be the escape character; here `!` escapes the literal `%`.

---

## Q31: Compare two strings case-insensitively.

**Query:**
```sql
SELECT username
FROM users
WHERE LOWER(username) = LOWER('JohnDoe');
```
**Explanation:** Normalizing both sides with `LOWER` makes the comparison case-insensitive.

**Alt1 (Oracle — `NLS_UPPER` with sort):**
```sql
-- Oracle
SELECT username
FROM users
WHERE NLS_UPPER(username) = NLS_UPPER('JohnDoe');
```
**Explanation:** `NLS_UPPER` performs a linguistic uppercase which handles accents and locale rules.

**Alt2 (PostgreSQL — `ILIKE`):**
```sql
-- PostgreSQL
SELECT username
FROM users
WHERE username ILIKE 'johndoe';
```
**Explanation:** `ILIKE` is PostgreSQL's built-in case-insensitive `LIKE`. `= ~*` (case-insensitive regex match) is another option.

---

## Q32: Find rows where a search term appears inside a sentence regardless of surrounding spaces.

**Query:**
```sql
SELECT body
FROM posts
WHERE LOWER(TRIM(body)) LIKE '%sql%';
```
**Explanation:** Trim then lowercase to handle ragged whitespace and mixed case before pattern matching.

---

## Q33: Reverse a string so 'abc' becomes 'cba'.

**Query:**
```sql
-- PostgreSQL / Oracle
SELECT REVERSE('abc') AS reversed;
```
**Explanation:** `REVERSE` returns the string in reverse order.

**Alt1 (MySQL):**
```sql
-- MySQL
SELECT REVERSE('abc') AS reversed;
```
**Explanation:** MySQL also supports `REVERSE`. SQL Server also has `REVERSE(string)` since 2008.

---

## Q34: Check if a word is a palindrome (reads the same forwards and backwards).

**Query:**
```sql
SELECT word,
       CASE WHEN word = REVERSE(word) THEN 'Palindrome' ELSE 'Not' END AS result
FROM words;
```
**Explanation:** A word equals its own reverse iff it is a palindrome.

---

## Q35: Convert a string representation of a number ('1234') into an actual numeric type.

**Query:**
```sql
SELECT CAST('1234.56' AS DECIMAL(10,2)) AS numeric_value;
```
**Explanation:** `CAST` is standard SQL and converts between string and numeric types.

**Alt1 (PostgreSQL — `::` shorthand):**
```sql
-- PostgreSQL
SELECT '1234.56'::DECIMAL(10,2) AS numeric_value;
```
**Explanation:** PostgreSQL's `::` operator is a shorthand for `CAST`.

**Alt2 (SQL Server — `TRY_CAST` for safety):**
```sql
-- SQL Server
SELECT TRY_CAST('1234.56' AS DECIMAL(10,2)) AS numeric_value;
```
**Explanation:** `TRY_CAST` returns NULL instead of raising an error if the conversion fails.

---

## Q36: Convert a price column (numeric) into a string.

**Query:**
```sql
SELECT CAST(price AS CHAR(10)) AS price_str
FROM products;
```
**Explanation:** Standard `CAST` converts numeric to string.

**Alt1 (MySQL — `CONCAT` auto-cast):**
```sql
-- MySQL
SELECT CONCAT('$', price) AS price_label
FROM products;
```
**Explanation:** Concatenating a string literal with a number implicitly casts the number to string.

---

## Q37: Format a number with commas as thousands separators (e.g., 1234567 -> 1,234,567).

**Query:**
```sql
-- SQL Server
SELECT FORMAT(1234567, 'N0') AS formatted;
```
**Explanation:** SQL Server's `FORMAT` uses .NET format strings; `'N0'` adds thousands separators with no decimals.

**Alt1 (MySQL — `FORMAT`):**
```sql
-- MySQL
SELECT FORMAT(1234567, 0) AS formatted;
```
**Explanation:** MySQL's `FORMAT(number, decimals)` adds comma separators.

**Alt2 (SQLite — `printf`):**
```sql
-- SQLite
SELECT PRINTF('%,d', 1234567) AS formatted;
```
**Explanation:** SQLite's `PRINTF` supports the `%d` conversion with grouping flags.

---

## Q38: Cast a string column to a date safely.

**Query:**
```sql
-- PostgreSQL
SELECT '2024-05-17'::DATE AS parsed_date;
```
**Explanation:** PostgreSQL's `::DATE` casts an ISO-formatted string directly.

**Alt1 (MySQL):**
```sql
-- MySQL
SELECT STR_TO_DATE('17/05/2024', '%d/%m/%Y') AS parsed_date;
```
**Explanation:** `STR_TO_DATE` parses non-ISO formats by providing a format string.

**Alt2 (Oracle):**
```sql
-- Oracle
SELECT TO_DATE('17/05/2024', 'DD/MM/YYYY') AS parsed_date
FROM DUAL;
```
**Explanation:** Oracle's `TO_DATE` requires the format model. `FROM DUAL` supplies the dummy row.

---

## Q39: Trim trailing punctuation (periods, commas, exclamation marks) from the end of sentences.

**Query:**
```sql
-- PostgreSQL
SELECT TRIM(TRAILING '.' FROM TRIM(TRAILING ',' FROM TRIM(TRAILING '!' FROM sentence))) AS cleaned
FROM quotes;
```
**Explanation:** Nested `TRIM` calls each remove one trailing character type. Note PostgreSQL only allows one char per TRIM.

**Alt1 (regex — handles all at once):**
```sql
-- PostgreSQL
SELECT REGEXP_REPLACE(sentence, '[.,!]+$', '') AS cleaned
FROM quotes;
```
**Explanation:** The regex `[.,!]+$` matches one or more trailing punctuation chars and removes them in a single pass.

---

## Q40: Map a month number (1-12) to its calendar month name.

**Query:**
```sql
-- SQLite
SELECT CASE month_num
  WHEN 1 THEN 'January' WHEN 2 THEN 'February' WHEN 3 THEN 'March'
  WHEN 4 THEN 'April' WHEN 5 THEN 'May' WHEN 6 THEN 'June'
  WHEN 7 THEN 'July' WHEN 8 THEN 'August' WHEN 9 THEN 'September'
  WHEN 10 THEN 'October' WHEN 11 THEN 'November' ELSE 'December'
END AS month_name
FROM sales;
```
**Explanation:** A `CASE` expression is the fully portable way to map numbers to names without date functions.

**Alt1 (PostgreSQL — `TO_CHAR`):**
```sql
-- PostgreSQL
SELECT TO_CHAR(MAKE_DATE(2024, month_num, 1), 'Month') AS month_name
FROM sales;
```
**Explanation:** Build a date from the month number and format it with `TO_CHAR`.

---

## Q41: Detect duplicate adjacent letters in a word (e.g., 'letter' has 'tt').

**Query:**
```sql
-- PostgreSQL
SELECT word
FROM words
WHERE word ~ '([a-zA-Z])\1';
```
**Explanation:** The regex `([a-zA-Z])\1` matches a letter followed by itself using a backreference.

**Alt1 (MySQL):**
```sql
-- MySQL
SELECT word
FROM words
WHERE word REGEXP '([a-z])\\\\1';
```
**Explanation:** MySQL's `REGEXP` supports backreferences with a double-escaped `\\1`.

---

## Q42: Build a comma-separated list of product names per category.

**Query:**
```sql
-- MySQL
SELECT category_id, GROUP_CONCAT(product_name ORDER BY product_name SEPARATOR ', ') AS products
FROM products
GROUP BY category_id;
```
**Explanation:** `GROUP_CONCAT` concatenates values within each group. MySQL-specific but widely used.

**Alt1 (PostgreSQL — `STRING_AGG`):**
```sql
-- PostgreSQL
SELECT category_id, STRING_AGG(product_name, ', ' ORDER BY product_name) AS products
FROM products
GROUP BY category_id;
```
**Explanation:** PostgreSQL's `STRING_AGG` supports an inline `ORDER BY`.

**Alt2 (SQL Server):**
```sql
-- SQL Server
SELECT category_id,
       STRING_AGG(product_name, ', ') WITHIN GROUP (ORDER BY product_name) AS products
FROM products
GROUP BY category_id;
```
**Explanation:** SQL Server requires the `WITHIN GROUP (ORDER BY ...)` clause.

**Alt3 (Oracle — `LISTAGG`):**
```sql
-- Oracle
SELECT category_id, LISTAGG(product_name, ', ') WITHIN GROUP (ORDER BY product_name) AS products
FROM products
GROUP BY category_id;
```
**Explanation:** Oracle's `LISTAGG` uses the same `WITHIN GROUP` clause as SQL Server.

---

## Q43: Concatenate column values into a single CSV row using a cross-join.

**Query:**
```sql
-- SQL Server 2017+
SELECT STRING_AGG(CAST(id AS VARCHAR(10)), ',') AS id_csv
FROM (SELECT 1 AS id UNION ALL SELECT 2 UNION ALL SELECT 3) t;
```
**Explanation:** `STRING_AGG` collapses multiple rows into one delimited string.

---

## Q44: Parse a CSV string 'apple,banana,orange' into separate rows.

**Query:**
```sql
-- PostgreSQL
SELECT UNNEST(STRING_TO_ARRAY('apple,banana,orange', ',')) AS fruit;
```
**Explanation:** `STRING_TO_ARRAY` splits into an array and `UNNEST` expands it into rows.

**Alt1 (SQL Server):**
```sql
-- SQL Server
SELECT value FROM STRING_SPLIT('apple,banana,orange', ',');
```
**Explanation:** `STRING_SPLIT` (2016+) returns each element as a row in the `value` column.

**Alt2 (MySQL):**
```sql
-- MySQL 8.0 (JSON_TABLE)
SELECT fruit
FROM JSON_TABLE(
  '["apple","banana","orange"]',
  '$[*]' COLUMNS (fruit VARCHAR(255) PATH '$')
) AS jt;
```
**Explanation:** There is no native `STRING_SPLIT` in MySQL; `JSON_TABLE` converts a JSON array to rows. Recursive CTEs are the older workaround.

---

## Q45: Split a pipe-delimited field and take the third element.

**Query:**
```sql
-- PostgreSQL
SELECT SPLIT_PART('red|green|blue|yellow', '|', 3) AS third;
```
**Explanation:** `SPLIT_PART(string, delimiter, n)` returns the nth part. PostgreSQL-specific.

**Alt1 (MySQL — `SUBSTRING_INDEX`):**
```sql
-- MySQL
SELECT SUBSTRING_INDEX(SUBSTRING_INDEX('red|green|blue|yellow', '|', 3), '|', -1) AS third;
```
**Explanation:** Nested `SUBSTRING_INDEX` — take the first 3 parts, then take the last of those.

---

## Q46: Extract text between two delimiters (e.g., 'abc[target]xyz' -> 'target').

**Query:**
```sql
-- Oracle
SELECT SUBSTR('abc[target]xyz',
              INSTR('abc[target]xyz', '[') + 1,
              INSTR('abc[target]xyz', ']') - INSTR('abc[target]xyz', '[') - 1) AS inner_text
FROM DUAL;
```
**Explanation:** `INSTR` finds the delimiters; `SUBSTR` extracts the span between them.

**Alt1 (regex):**
```sql
-- PostgreSQL
SELECT (REGEXP_MATCH('abc[target]xyz', '\[([^]]+)\]'))[1] AS inner_text;
```
**Explanation:** A capturing group extracts the text inside the brackets directly.

---

## Q47: Extract all uppercase words from a sentence.

**Query:**
```sql
-- PostgreSQL
SELECT REGEXP_MATCHES('Hello WORLD, this is SQL TEST', '[A-Z]+', 'g') AS upper_words;
```
**Explanation:** The `'g'` flag returns every regex match, not just the first.

**Alt1 (MySQL):**
```sql
-- MySQL
SELECT REGEXP_SUBSTR('Hello WORLD, this is SQL TEST', '[A-Z]+', 1, 1) AS first_upper;
```
**Explanation:** `REGEXP_SUBSTR` (MySQL 8+ / Oracle) returns one match; the 4th argument selects which match to return.

---

## Q48: Remove all non-digit characters from a phone number.

**Query:**
```sql
-- MySQL
SELECT REGEXP_REPLACE(phone, '[^0-9]', '') AS digits_only
FROM contacts;
```
**Explanation:** `[^0-9]` matches anything that is not a digit, and we replace it with empty string.

**Alt1 (PostgreSQL):**
```sql
-- PostgreSQL
SELECT REGEXP_REPLACE(phone, '\D', '', 'g') AS digits_only
FROM contacts;
```
**Explanation:** `\D` is the shorthand for non-digit characters; the `'g'` flag makes it replace all occurrences.

---

## Q49: Extract the zip code from a US address stored in a single text column.

**Query:**
```sql
-- PostgreSQL
SELECT REGEXP_MATCH(address, '\d{5}(?:-\d{4})?') AS zip_code
FROM addresses;
```
**Explanation:** The regex matches exactly 5 digits with an optional 4-digit extension.

---

## Q50: Extract every email address from a notes text column.

**Query:**
```sql
-- PostgreSQL
SELECT notes, REGEXP_MATCHES(notes, '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', 'g') AS emails
FROM customer_notes;
```
**Explanation:** A pragmatic email regex extracts all matching substrings via the global flag.


## Q51: Format a phone number '2125551234' as '(212) 555-1234'.

**Query:**
```sql
-- PostgreSQL
SELECT '(' || SUBSTRING(phone FROM 1 FOR 3) || ') '
       || SUBSTRING(phone FROM 4 FOR 3) || '-' || SUBSTRING(phone FROM 7 FOR 4) AS formatted
FROM contacts;
```
**Explanation:** Slice the digits into area code, exchange, and line number, then rejoin with formatting characters.

**Alt1 (SQL Server):**
```sql
-- SQL Server
SELECT '(' + LEFT(phone, 3) + ') ' + SUBSTRING(phone, 4, 3) + '-' + RIGHT(phone, 4) AS formatted
FROM contacts;
```
**Explanation:** Uses `LEFT`, `SUBSTRING`, and `RIGHT` to slice and the `+` operator to join.

**Alt2 (regex — strip then rebuild):**
```sql
-- MySQL
SELECT CONCAT(
  '(', REGEXP_SUBSTR(phone, '^[0-9]{3}'), ') ',
  REGEXP_SUBSTR(phone, '(?<=^[0-9]{3})[0-9]{3}'),
  '-', REGEXP_SUBSTR(phone, '[0-9]{4}$')
) AS formatted
FROM contacts;
```
**Explanation:** Regex lookarounds carve the digit groups out of a raw phone column in one pass.

---

## Q52: Mask a credit card number so only the last 4 digits are visible.

**Query:**
```sql
-- MySQL
SELECT CONCAT(REPEAT('*', CHAR_LENGTH(card_number) - 4), RIGHT(card_number, 4)) AS masked
FROM payments;
```
**Explanation:** `REPEAT` fills the front with asterisks and `RIGHT` keeps the last 4 digits.

**Alt1 (PostgreSQL):**
```sql
-- PostgreSQL
SELECT LPAD(RIGHT(card_number, 4), CHAR_LENGTH(card_number), '*') AS masked
FROM payments;
```
**Explanation:** `LPAD` pads the last 4 digits with `*` up to the original length.

**Alt2 (SQL Server — `REPLICATE`):**
```sql
-- SQL Server
SELECT REPLICATE('*', LEN(card_number) - 4) + RIGHT(card_number, 4) AS masked
FROM payments;
```
**Explanation:** `REPLICATE` is SQL Server's `REPEAT` equivalent.

---

## Q53: Use `TRANSLATE` to convert a string with mixed separators (dashes, slashes) into a uniform format.

**Query:**
```sql
-- Oracle
SELECT TRANSLATE('2024-05/17', '/-', '--') AS normalized
FROM DUAL;
```
**Explanation:** `TRANSLATE` swaps each `/` for `-` and leaves existing `-` characters unchanged (swapped with themselves).

---

## Q54: Find the second occurrence position of a substring inside a string.

**Query:**
```sql
-- MySQL
SELECT LOCATE('a', 'banana', LOCATE('a', 'banana') + 1) AS second_position;
```
**Explanation:** `LOCATE` accepts a starting position; we pass one past the first match.

**Alt1 (SQL Server — `CHARINDEX`):**
```sql
-- SQL Server
SELECT CHARINDEX('a', 'banana', CHARINDEX('a', 'banana') + 1) AS second_position;
```
**Explanation:** `CHARINDEX` also takes a start offset, so the same nesting works.

---

## Q55: Find the position of the LAST occurrence of a character.

**Query:**
```sql
-- PostgreSQL
SELECT LENGTH('product/parts/final') - POSITION('/' IN REVERSE('product/parts/final')) + 1 AS last_slash;
```
**Explanation:** Reverse the string, find the first slash, and translate that position back to the original string.

**Alt1 (Oracle/MSSQL — `INSTR` with negative):**
```sql
-- Oracle
SELECT INSTR('product/parts/final', '/', -1) AS last_slash
FROM DUAL;
```
**Explanation:** A negative start position in `INSTR` makes it search backward for the last occurrence.

**Alt2 (MySQL — `LOCATE` reverse trick):**
```sql
-- MySQL
SELECT CHAR_LENGTH('product/parts/final')
       - LOCATE('/', REVERSE('product/parts/final')) + 1 AS last_slash;
```
**Explanation:** Same reverse-and-measure approach using MySQL functions.

---

## Q56: Turn a word into a title-cased slug for URLs (e.g., 'Hello World' -> 'hello-world').

**Query:**
```sql
-- PostgreSQL
SELECT LOWER(REGEXP_REPLACE(title, '[^a-zA-Z0-9]+', '-', 'g')) AS slug
FROM articles;
```
**Explanation:** Replace every run of non-alphanumeric characters with a dash, then lowercase the whole thing.

**Alt1 (SQL Server):**
```sql
-- SQL Server
SELECT LOWER(REPLACE(REPLACE(title, ' ', '-'), '&', 'and')) AS slug
FROM articles;
```
**Explanation:** Without regex, chain targeted `REPLACE` calls for the known problem characters.

---

## Q57: Validate that a username matches `[a-z0-9_]{3,16}`.

**Query:**
```sql
-- PostgreSQL
SELECT username
FROM users
WHERE username ~ '^[a-z0-9_]{3,16}$';
```
**Explanation:** Anchors `^` and `$` ensure the entire string matches; `{3,16}` enforces the length range.

**Alt1 (MySQL):**
```sql
-- MySQL
SELECT username
FROM users
WHERE username REGEXP '^[a-z0-9_]{3,16}$';
```
**Explanation:** MySQL's `REGEXP` operator follows the same regex syntax.

---

## Q58: Write a query that splits a sentence into individual words (rows).

**Query:**
```sql
-- PostgreSQL
SELECT UNNEST(STRING_TO_ARRAY('the quick brown fox', ' ')) AS word;
```
**Explanation:** `STRING_TO_ARRAY` + `UNNEST` yields one row per word.

**Alt1 (MySQL 8 — recursive CTE):**
```sql
-- MySQL
WITH RECURSIVE splitter AS (
  SELECT 1 AS n,
         SUBSTRING_INDEX('the quick brown fox', ' ', 1) AS word,
         TRIM(SUBSTRING('the quick brown fox', CHAR_LENGTH(SUBSTRING_INDEX('the quick brown fox', ' ', 1)) + 2)) AS rest
  UNION ALL
  SELECT n + 1,
         SUBSTRING_INDEX(rest, ' ', 1),
         TRIM(SUBSTRING(rest, CHAR_LENGTH(SUBSTRING_INDEX(rest, ' ', 1)) + 2))
  FROM splitter WHERE rest <> ''
)
SELECT word FROM splitter;
```
**Explanation:** The recursive CTE peels one word off at a time until nothing remains — the standard MySQL workaround for missing `STRING_SPLIT`.

---

## Q59: Count the number of words in a sentence.

**Query:**
```sql
-- PostgreSQL
SELECT sentence,
       CARDINALITY(STRING_TO_ARRAY(TRIM(sentence), ' ')) AS word_count
FROM sentences;
```
**Explanation:** `CARDINALITY` returns the size of the array produced by splitting on spaces.

**Alt1 (SQL Server):**
```sql
-- SQL Server
SELECT sentence,
       LEN(sentence) - LEN(REPLACE(LTRIM(sentence), ' ', '')) + 1 AS word_count
FROM sentences;
```
**Explanation:** The number of spaces plus one approximates the word count.

**Alt2 (MySQL):**
```sql
-- MySQL
SELECT sentence,
       (CHAR_LENGTH(TRIM(sentence)) - CHAR_LENGTH(REPLACE(TRIM(sentence), ' ', ''))) + 1 AS word_count
FROM sentences;
```
**Explanation:** Same space-counting logic, expressed with `CHAR_LENGTH`.

---

## Q60: Remove all HTML tags from a snippet of markup.

**Query:**
```sql
-- PostgreSQL
SELECT REGEXP_REPLACE(html, '<[^>]*>', '', 'g') AS plain_text
FROM blog_posts;
```
**Explanation:** `<[^>]*>` matches any tag from `<` to the next `>`; the global flag removes them all.

---

## Q61: Convert camelCase identifiers to snake_case (e.g., 'firstName' -> 'first_name').

**Query:**
```sql
-- PostgreSQL
SELECT REGEXP_REPLACE('firstName', '([a-z])([A-Z])', '\1_\2', 'g') AS snake;
```
**Explanation:** The regex captures a lowercase letter followed by an uppercase one and inserts an underscore between them via backreferences.

**Alt1 (Snowflake-style regex in MySQL):**
```sql
-- MySQL
SELECT REGEXP_REPLACE('firstName', '([a-z])([A-Z])', '\\1_\\2') AS snake;
```
**Explanation:** MySQL needs the backreferences double-escaped `\\1` inside the replacement string.

---

## Q62: Extract the substring before a comma in 'Apple, Inc.'.

**Query:**
```sql
-- MySQL
SELECT SUBSTRING_INDEX('Apple, Inc.', ',', 1) AS first_part;
```
**Explanation:** A positive count returns everything before the first comma.

**Alt1 (PostgreSQL):**
```sql
-- PostgreSQL
SELECT SPLIT_PART('Apple, Inc.', ',', 1) AS first_part;
```
**Explanation:** `SPLIT_PART` with position `1` is the PostgreSQL equivalent.

**Alt2 (SQL Server):**
```sql
-- SQL Server
SELECT LEFT('Apple, Inc.', CHARINDEX(',', 'Apple, Inc.') - 1) AS first_part;
```
**Explanation:** Locate the comma with `CHARINDEX`, subtract 1, and take the left portion.

---

## Q63: Build a JSON string from a name column (e.g., `{"name": "Alice"}`).

**Query:**
```sql
-- PostgreSQL
SELECT TO_JSONB(ROW_TO_JSON(t)) #>> '{name}' AS name_json
FROM (SELECT 'Alice' AS name) t;
```
**Explanation:** `ROW_TO_JSON` shapes a row; simpler output via `CONCAT('{"name": "', name, '"}')` does the same literally.

**Alt1 (hand-built JSON):**
```sql
SELECT CONCAT('{"name": "', name, '"}') AS name_json
FROM customers;
```
**Explanation:** Explicit string concatenation is the most portable way to emit small JSON fragments.

---

## Q64: Pull a value out of a JSON object stored in a text column.

**Query:**
```sql
-- PostgreSQL
SELECT email_json -> 'address' AS address
FROM user_profiles;
```
**Explanation:** The `->` operator extracts a JSON field (as JSON). `->>` returns it as text.

**Alt1 (MySQL):**
```sql
-- MySQL
SELECT JSON_UNQUOTE(JSON_EXTRACT(profile, '$.address')) AS address
FROM user_profiles;
```
**Explanation:** `JSON_EXTRACT` + `JSON_UNQUOTE` returns the field's string value. MySQL also supports `->>` shorthand (8.0+).

---

## Q65: Use the JSON path operator to compare a nested string field against a literal.

**Query:**
```sql
-- PostgreSQL
SELECT profile
FROM user_profiles
WHERE profile ->> 'address' = 'Maple St';
```
**Explanation:** `->>` yields text, so it can be compared directly to a string literal.

**Alt1 (MySQL):**
```sql
-- MySQL
SELECT profile
FROM user_profiles
WHERE JSON_UNQUOTE(JSON_EXTRACT(profile, '$.address')) = 'Maple St';
```
**Explanation:** Explicit `JSON_EXTRACT`+`JSON_UNQUOTE` is needed in MySQL (or the `->>` shorthand, which does both).

---

## Q66: Find employees whose first and last name together spell out a palindrome.

**Query:**
```sql
SELECT first_name || last_name AS joined,
       CASE WHEN first_name || last_name = REVERSE(first_name || last_name)
            THEN 'Palindrome' ELSE 'No' END AS result
FROM employees;
```
**Explanation:** Concatenate both names and compare against the reversed concatenation.

---

## Q67: Extract the initials from a full name ('John Fitzgerald Kennedy' -> 'JFK').

**Query:**
```sql
-- PostgreSQL
SELECT REGEXP_REPLACE(full_name, '\s*([A-Za-z])\w*', '\1', 'g') AS initials
FROM people;
```
**Explanation:** The regex captures each word's first letter and discards the rest, leaving a concatenation of initials.

---

## Q68: Remove the country calling code from an international phone number ' +44 20 7946 0958'.

**Query:**
```sql
SELECT REGEXP_REPLACE(phone, '^\+?\d{1,3}\s?', '') AS local_number
FROM contacts;
```
**Explanation:** The regex strips an optional `+` followed by 1-3 country-code digits and the trailing space.

---

## Q69: Prefix every line of a multi-line address with a tab character.

**Query:**
```sql
-- PostgreSQL
SELECT REGEXP_REPLACE(address, '(?m)^', '\t', 'g') AS tabbed
FROM customers;
```
**Explanation:** With the `(?m)` multiline flag, `^` matches the start of every line and the tab is inserted there.

---

## Q70: Strip trailing spaces from every value in a comma-separated string.

**Query:**
```sql
-- MySQL
SELECT TRIM(REGEXP_REPLACE('apple , banana ,cherry', ' ?([^,]+?) ?', '$1')) AS cleaned;
```
**Explanation:** Capture each field without its surrounding spaces via a non-greedy regex and re-emit it trimmed.

**Alt1 (PostgreSQL — row-based):**
```sql
-- PostgreSQL
SELECT STRING_AGG(TRIM(word), ',' ORDER BY ord) AS cleaned
FROM UNNEST(STRING_TO_ARRAY('apple , banana ,cherry', ',')) WITH ORDINALITY AS w(word, ord);
```
**Explanation:** Split to rows, `TRIM` each element, then re-aggregate with `STRING_AGG`. `WITH ORDINALITY` preserves order.

---

## Q71: Detect strings that contain every letter of the alphabet (a pangram check).

**Query:**
```sql
-- PostgreSQL
SELECT phrase
FROM phrases
WHERE CARDINALITY(ARRAY(
  SELECT DISTINCT ch FROM UNNEST(STRING_TO_ARRAY(LOWER(REGEXP_REPLACE(phrase, '[^a-z]', '', 'g')), '')) AS ch
)) = 26;
```
**Explanation:** Strip non-letters, split into characters, count distinct letters, and require 26.

---

## Q72: Find strings where a character repeats itself more than twice in a row (e.g., 'aaa').

**Query:**
```sql
SELECT word
FROM words
WHERE word REGEXP '(.)\1{2}';
```
**Explanation:** `(.)` captures any character and `\1{2}` requires two more copies of it immediately after.

---

## Q73: Compute a simple Levenshtein edit distance between two names.

**Query:**
```sql
-- PostgreSQL
SELECT LEVENSHTEIN('kitten', 'sitting') AS distance;
```
**Explanation:** The `fuzzystrmatch` extension supplies `LEVENSHTEIN`. Load it with `CREATE EXTENSION fuzzystrmatch;` first. Result is 3.

---

## Q74: Match names that sound alike using `SOUNDEX`.

**Query:**
```sql
-- MySQL
SELECT word
FROM words
WHERE SOUNDEX(word) = SOUNDEX('wright');
```
**Explanation:** `SOUNDEX` encodes pronunciation; equal codes indicate similar-sounding words (e.g., 'write', 'right').

---

## Q75: Generate character n-grams (e.g., 3-grams) from a word.

**Query:**
```sql
-- PostgreSQL
SELECT word,
       (SELECT ARRAY_AGG(SUBSTRING(word FROM g FOR 3))
        FROM GENERATE_SERIES(1, LENGTH(word) - 2) AS g) AS trigrams
FROM words
WHERE LENGTH(word) >= 3;
```
**Explanation:** `GENERATE_SERIES` produces starting offsets and `SUBSTRING` grabs each 3-character window.


## Q76: Split a full address '123 Main St, Apt 4B, Springfield, IL 62704' into street, unit, city, state.

**Query:**
```sql
-- PostgreSQL
SELECT SPLIT_PART(address, ',', 1) AS street,
       SPLIT_PART(address, ',', 2) AS unit,
       SPLIT_PART(address, ',', 3) AS city,
       SPLIT_PART(address, ',', 4) AS state_zip
FROM customers;
```
**Explanation:** Each comma-separated position maps to a part of the address via sequential `SPLIT_PART` calls.

---

## Q77: Parse a full name that may contain an optional middle initial ('Smith, John A.' -> last='Smith', first='John', middle='A').

**Query:**
```sql
-- PostgreSQL
SELECT SPLIT_PART(full_name, ',', 1) AS last_name,
       SPLIT_PART(TRIM(SPLIT_PART(full_name, ',', 2)), ' ', 1) AS first_name,
       NULLIF(SPLIT_PART(TRIM(SPLIT_PART(full_name, ',', 2)), ' ', 2), '') AS middle_initial
FROM people;
```
**Explanation:** Split on the comma first (last vs. rest), then split the remainder on spaces, tolerating a missing middle initial via `NULLIF`.

---

## Q78: Identify duplicated words back-to-back in text ('the the').

**Query:**
```sql
-- PostgreSQL
SELECT body
FROM posts
WHERE body ~ '\b(\w+)\s+\1\b';
```
**Explanation:** The backreference `\1` matches the same captured word again immediately after whitespace.

---

## Q79: Find the most frequent first character across all product names.

**Query:**
```sql
SELECT LEFT(product_name, 1) AS first_char, COUNT(*) AS cnt
FROM products
GROUP BY LEFT(product_name, 1)
ORDER BY cnt DESC
LIMIT 1;
```
**Explanation:** Group by the first character and take the top count. Works in all dialects; Oracle/SQL Server would use `FETCH FIRST 1 ROW` or `TOP` respectively.

---

## Q80: Extract the file extension from a filename.

**Query:**
```sql
-- PostgreSQL
SELECT filename, SPLIT_PART(filename, '.', -1) AS extension
FROM files;
```
**Explanation:** `SPLIT_PART` with a negative position counts from the end of the split array.

**Alt1 (MySQL):**
```sql
-- MySQL
SELECT filename, SUBSTRING_INDEX(filename, '.', -1) AS extension
FROM files;
```
**Explanation:** Negative `SUBSTRING_INDEX` returns everything after the last dot.

---

## Q81: Strip the file extension off a filename.

**Query:**
```sql
-- MySQL
SELECT SUBSTRING_INDEX(filename, '.', 1) AS basename
FROM files;
```
**Explanation:** Positive count gives everything before the first dot.

**Alt1 (PostgreSQL):**
```sql
-- PostgreSQL
SELECT LEFT(filename, POSITION('.' IN filename) - 1) AS basename
FROM files
WHERE filename LIKE '%.%';
```
**Explanation:** `POSITION` finds the dot and `LEFT` keeps the name before it.

---

## Q82: Insert a dash into a 10-digit number every 3 digits ('1234567890' -> '123-456-789-0').

**Query:**
```sql
-- PostgreSQL
SELECT REGEXP_REPLACE('1234567890', '(\d{3})(?=\d)', '\1-', 'g') AS dashed;
```
**Explanation:** A zero-width lookahead `(?=\d)` inserts a dash after each group of 3 digits except the last.

---

## Q83: Find all rows where the string looks like a valid IPv4 address.

**Query:**
```sql
SELECT ip
FROM hosts
WHERE ip REGEXP '^([0-9]{1,3}\.){3}[0-9]{1,3}$';
```
**Explanation:** The pattern enforces three groups of 1-3 digits separated by dots and a final group.

---

## Q84: Compute a running, cumulative concatenation over a column (e.g., 'a', 'ab', 'abc', ...).

**Query:**
```sql
-- MySQL
SELECT id, letter,
       (SELECT GROUP_CONCAT(l2 ORDER BY l2.id SEPARATOR '')
        FROM letters l2 WHERE l2.id <= l1.id) AS running
FROM letters l1
ORDER BY id;
```
**Explanation:** A correlated subquery concatenates all letters up to the current row's id in order.

**Alt1 (PostgreSQL — window function):**
```sql
-- PostgreSQL
SELECT id, letter,
       STRING_AGG(letter, '') OVER (ORDER BY id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running
FROM letters;
```
**Explanation:** `STRING_AGG` as a window function naturally produces the running concatenation in PostgreSQL/SQL Server 2022.

---

## Q85: Use `STRING_AGG` with a WHERE filter to build a comma list of only active users.

**Query:**
```sql
-- PostgreSQL
SELECT department_id,
       STRING_AGG(first_name, ', ') FILTER (WHERE is_active) AS active_users
FROM employees
GROUP BY department_id;
```
**Explanation:** The `FILTER` clause restricts which rows feed the aggregate without changing the grouping.

**Alt1 (conditional inside aggregate):**
```sql
-- MySQL
SELECT department_id,
       GROUP_CONCAT(CASE WHEN is_active THEN first_name END SEPARATOR ', ') AS active_users
FROM employees
GROUP BY department_id;
```
**Explanation:** `GROUP_CONCAT` skips NULLs, so rows failing the `CASE` are silently excluded.

---

## Q86: Build a CSV where each value must have quotes around it.

**Query:**
```sql
-- SQL Server
SELECT STRING_AGG('"' + REPLACE(name, '"', '""') + '"', ',') AS quoted_csv
FROM customers;
```
**Explanation:** Each name gets wrapped in quotes and embedded quotes are doubled, following CSV escaping rules.

---

## Q87: Detect first names that look like numbers ('12345').

**Query:**
```sql
SELECT first_name
FROM employees
WHERE first_name NOT REGEXP '^[0-9]+$'
  AND first_name REGEXP '[0-9]';
```
**Explanation:** The NOT forces rejection of purely numeric names while still flagging names containing any digit.

---

## Q88: Extract the value of a `?key=value` query parameter from a URL.

**Query:**
```sql
-- PostgreSQL
SELECT (REGEXP_MATCH(url, 'id=([^&]+)'))[1] AS id_value
FROM logs;
```
**Explanation:** The capturing group `([^&]+)` grabs all characters up to the next `&`.

**Alt1 (Oracle — `REGEXP_SUBSTR` with subexpression):**
```sql
-- Oracle
SELECT REGEXP_SUBSTR(url, 'id=([^&]+)', 1, 1, NULL, 1) AS id_value
FROM logs;
```
**Explanation:** The 6th argument (1) tells `REGEXP_SUBSTR` to return the first capturing group instead of the whole match.

---

## Q89: Replace newline characters with a space to flatten a multiline comment column.

**Query:**
```sql
-- MySQL
SELECT REGEXP_REPLACE(comment_text, '\r?\n', ' ') AS one_line
FROM comments;
```
**Explanation:** `\r?\n` matches both LF and CRLF line endings so the text is flattened onto one line.

---

## Q90: Remove emoji or non-BMP characters from strings.

**Query:**
```sql
-- null-safe replacement using MySQL's CHAR_LENGTH vs LENGTH
SELECT id,
       CASE WHEN CHAR_LENGTH(text) = LENGTH(text) THEN text
            ELSE REGEXP_REPLACE(text, '[^\u0000-\uFFFF]', '', 1, 0)
       END AS ascii_safe
FROM reviews;
```
**Explanation:** Emoji are multi-byte; when byte length exceeds character length, the regex strips characters outside the BMP range.

---

## Q91: Extract the 3-letter month abbreviation from a date literal, using string functions.

**Query:**
```sql
-- SQLite
SELECT SUBSTR(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
  '2024-05-17','01',''),'02',''),'03',''),'04',''),'05','MAY'),'06',''),'07',''),'08',''),'09',''),'10',''),'11',''),'12','') AS mmm;
```
**Explanation:** A brute-force mapping table assembled purely from `REPLACE`. In practice, use `DATE_FORMAT`/`TO_CHAR` for month names.

---

## Q92: Produce the weekday name from a date using string-based lookup.

**Query:**
```sql
-- PostgreSQL
SELECT TO_CHAR('2024-05-17'::DATE, 'Day') AS weekday;
```
**Explanation:** `TO_CHAR` formats the date directly into a weekday name; the same job a `CASE` mapping would do portably.

---

## Q93: Convert a delimited string into key/value pairs ('a=1,b=2,c=3') and pivot to columns.

**Query:**
```sql
-- PostgreSQL
SELECT MAX(CASE WHEN pair ~ '^a=' THEN SUBSTRING(pair FROM 3) END) AS a,
       MAX(CASE WHEN pair ~ '^b=' THEN SUBSTRING(pair FROM 3) END) AS b,
       MAX(CASE WHEN pair ~ '^c=' THEN SUBSTRING(pair FROM 3) END) AS c
FROM (
  SELECT UNNEST(STRING_TO_ARRAY('a=1,b=2,c=3', ',')) AS pair
) t;
```
**Explanation:** Split into pairs, then conditionally pull each key's value with pattern-matched `CASE` expressions.

---

## Q94: Find strings that are near-duplicates using a Levenshtein threshold.

**Query:**
```sql
-- PostgreSQL
SELECT a.name, b.name, LEVENSHTEIN(a.name, b.name) AS distance
FROM products a
JOIN products b ON a.id < b.id
  AND LEVENSHTEIN(a.name, b.name) <= 1
WHERE NOT a.name = b.name;
```
**Explanation:** Self-join with `LEVENSHTEIN <= 1` flags single-edit-difference names that are likely typos.

---

## Q95: Handle NULL gracefully inside a concatenation chain.

**Query:**
```sql
-- PostgreSQL
SELECT CONCAT_WS(' ', first_name, NULLIF(middle_name,''), last_name) AS full_name
FROM employees;
```
**Explanation:** `CONCAT_WS` skips NULL arguments entirely, and `NULLIF` converts empty strings to NULL so they are skipped too.

**Alt1 (Oracle — `NVL2`-style):**
```sql
-- Oracle
SELECT TRIM(first_name || ' ' || NVL2(middle_name, middle_name || ' ', '') || last_name) AS full_name
FROM employees;
```
**Explanation:** `NVL2` conditionally includes the middle name plus a trailing space; `TRIM` cleans up the joins.

---

## Q96: Trim variable whitespace including tabs inside a field.

**Query:**
```sql
-- PostgreSQL
SELECT REGEXP_REPLACE(raw, '\s+', ' ', 'g') AS normalized
FROM staging;
```
**Explanation:** `\s` matches spaces, tabs, and line breaks; collapsing every run to a single space normalizes the field.

---

## Q97: Concatenate two strings with a separator only when both are present.

**Query:**
```sql
-- PostgreSQL
SELECT CONCAT_WS(' - ', first_name, last_name) AS display_name
FROM employees;
```
**Explanation:** `CONCAT_WS` inserts the separator only between non-NULL values, so a missing part never leaves an orphan dash.

---

## Q98: Extract every hashtag from a tweet text.

**Query:**
```sql
-- PostgreSQL
SELECT tweet, REGEXP_MATCHES(tweet, '#[A-Za-z_][A-Za-z0-9_]*', 'g') AS hashtags
FROM tweets;
```
**Explanation:** The pattern matches a `#` followed by a valid tag word; the global flag returns all of them.

---

## Q99: Convert a name to a phone-dial-safe string by removing all characters except digits and letters.

**Query:**
```sql
SELECT REGEXP_REPLACE(name, '[^a-zA-Z0-9]', '', 'g') AS safe_name
FROM contacts;
```
**Explanation:** The negated class `[^a-zA-Z0-9]` matches everything except letters/digits and deletes it in one pass.

---

## Q100: Split a full name into salutation, first, and last name where names may contain titles.

**Query:**
```sql
-- PostgreSQL
SELECT
  CASE WHEN full_name ~ '^(Mr\.|Mrs\.|Ms\.|Dr\.)' THEN SPLIT_PART(full_name, ' ', 1) END AS salutation,
  SPLIT_PART(full_name, ' ', 2) AS first_name,
  SPLIT_PART(full_name, ' ', -1) AS last_name
FROM people;
```
**Explanation:** Named patterns detect the salutation, and positional splits handle first/last, with the salutation NULL when absent.

