# Set Operations UNION INTERSECT EXCEPT — 100 SQL Interview Q&A

## Q1: Write a query to list all distinct customers who placed an order in either the web_orders or the store_orders channel.

**Query:**
```sql
SELECT customer_id FROM web_orders
UNION
SELECT customer_id FROM store_orders;
```
**Explanation:** UNION merges both result sets and removes duplicate customer_ids. Both SELECTs must expose the same number of columns with compatible types.

## Q2: Your report must keep every row, including duplicates, when combining the two order sources. Rewrite the query so no rows are collapsed.

**Query:**
```sql
SELECT customer_id FROM web_orders
UNION ALL
SELECT customer_id FROM store_orders;
```
**Explanation:** UNION ALL appends the second result set to the first without any duplicate removal, so a customer ordering from both channels appears twice.

## Q3: Which of UNION and UNION ALL is faster, and why? Show the faster form.

**Query:**
```sql
SELECT customer_id FROM web_orders
UNION ALL
SELECT customer_id FROM store_orders;
```
**Explanation:** UNION ALL is faster because UNION must run a distinct (sort/hash) pass to eliminate duplicates; if you don't need dedup, UNION ALL avoids that whole stage.

## Q4: Stack the last three years of transactions from sales_2024, sales_2025 and sales_2026 into one result set, ordered by transaction date, keeping every row.

**Query:**
```sql
SELECT id, txn_date, amount FROM sales_2024
UNION ALL
SELECT id, txn_date, amount FROM sales_2025
UNION ALL
SELECT id, txn_date, amount FROM sales_2026
ORDER BY txn_date;
```
**Explanation:** UNION ALL (chained) concatenates three identically shaped tables; ORDER BY acts on the combined result. This is the standard idiom for stacking partitioned tables.

## Q5: MySQL 8.0.30 does not support INTERSECT. Emulate "customers who ordered in both January and February" using an IN subquery.

**Query:**
```sql
-- MySQL
SELECT DISTINCT customer_id FROM orders_jan
WHERE customer_id IN (SELECT customer_id FROM orders_feb);
```
**Alt1:**
```sql
-- MySQL
SELECT customer_id FROM orders_jan j
WHERE EXISTS (SELECT 1 FROM orders_feb f WHERE f.customer_id = j.customer_id);
```
**Explanation:** INTERSECT returns rows in both input sets; an IN (or EXISTS) subquery reproduces that behaviour on older MySQL.

## Q6: Write the same "bought in January AND February" query natively in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT customer_id FROM orders_jan
INTERSECT
SELECT customer_id FROM orders_feb;
```
**Explanation:** INTERSECT emits only rows present in both operands; the result is distinct by default.

## Q7: List products sold this year that were NOT sold last year, using PostgreSQL set syntax.

**Query:**
```sql
-- PostgreSQL
SELECT product_id FROM sales_current
EXCEPT
SELECT product_id FROM sales_last_year;
```
**Explanation:** EXCEPT returns rows in the first set that have no match in the second set, deduplicated.

## Q8: Your data warehouse is Oracle. Write the equivalent of the previous EXCEPT query using Oracle's operator.

**Query:**
```sql
-- Oracle
SELECT product_id FROM sales_current
MINUS
SELECT product_id FROM sales_last_year;
```
**Explanation:** MINUS is Oracle's name for EXCEPT and behaves identically: rows of the first query not found in the second.

## Q9: Emulate EXCEPT on MySQL with NOT IN, then explain what goes wrong if orders_2024 contains NULL customer_ids, and fix it.

**Query:**
```sql
-- MySQL (becomes NULL-poisoned when the subquery contains NULLs)
SELECT DISTINCT customer_id FROM orders_2025
WHERE customer_id NOT IN (SELECT customer_id FROM orders_2024);
```
**Alt1:**
```sql
-- MySQL (NULL-safe)
SELECT DISTINCT customer_id FROM orders_2025 o
WHERE NOT EXISTS (SELECT 1 FROM orders_2024 p WHERE p.customer_id = o.customer_id);
```
**Explanation:** `x NOT IN (... NULL ...)` evaluates to UNKNOWN for every row, returning an empty result; NOT EXISTS compares row-by-row and safely ignores NULLs.

## Q10: Find order records (order_id + amount pair) that appear in BOTH the file_orders and api_orders integration tables, using PostgreSQL set syntax.

**Query:**
```sql
-- PostgreSQL
SELECT order_id, amount FROM file_orders
INTERSECT
SELECT order_id, amount FROM api_orders;
```
**Explanation:** INTERSECT compares whole projected rows, so the intersection matches on order_id AND amount together — not just the key.

## Q11: Find product_ids that are in catalog_a or catalog_b but NOT in both (symmetric difference), PostgreSQL.

**Query:**
```sql
-- PostgreSQL
(SELECT product_id FROM catalog_a
 EXCEPT
 SELECT product_id FROM catalog_b)
UNION
(SELECT product_id FROM catalog_b
 EXCEPT
 SELECT product_id FROM catalog_a);
```
**Alt1:**
```sql
-- PostgreSQL (full-join alternative)
SELECT COALESCE(a.product_id, b.product_id) AS product_id
FROM catalog_a a
FULL OUTER JOIN catalog_b b ON a.product_id = b.product_id
WHERE a.product_id IS NULL OR b.product_id IS NULL;
```
**Explanation:** A minus B merged with B minus A yields exactly the rows exclusive to one side; a FULL OUTER JOIN filtered on the unmatched side is the join-based twin.

## Q12: UNION number columns with text columns. Combine employee_ids (INT) and contractor codes (VARCHAR) in a single result set, fixing the type clash.

**Query:**
```sql
SELECT CAST(employee_id AS VARCHAR(20)) AS worker_code FROM employees
UNION
SELECT contractor_code FROM contractors;
```
**Explanation:** Column position 1 must be type-compatible in every branch; casting the INT inside the first SELECT produces a common string type.

## Q13: invoices has 3 columns but receipts has 2. Write a UNION that doesn't error and keeps the receipt rows aligned.

**Query:**
```sql
SELECT id, name, amount FROM invoices
UNION
SELECT id, name, CAST(NULL AS DECIMAL(10,2)) FROM receipts;
```
**Explanation:** Columns are aligned by position, so the missing third column is padded with a typed NULL; the explicit cast also removes ambiguity for downstream ORDER BY.

## Q14: Both tables hold (first_name, last_name) string pairs but the columns are ordered differently in the second query. What does UNION return, and what is the trap?

**Query:**
```sql
SELECT first_name, last_name FROM contacts
UNION
SELECT last_name, first_name FROM alumni;
```
**Explanation:** UNION aligns by position, not by name, so the two columns silently swap roles for alumni; keep the projection order identical (and alias from the first branch) to stay correct.

## Q15: Find orders that are high-value (amount >= 10000) OR flagged as fraud, using two SELECTs combined with UNION so each predicate can use its own index — this is the single-table UNION filtering idiom.

**Query:**
```sql
SELECT order_id, amount, flagged FROM orders WHERE amount >= 10000
UNION
SELECT order_id, amount, flagged FROM orders WHERE flagged = 1;
```
**Alt1:**
```sql
SELECT order_id, amount, flagged FROM orders
WHERE amount >= 10000 OR flagged = 1;
```
**Explanation:** UNION of two filtered scans is equivalent to OR, but the optimizer can serve each branch independently (e.g. separate indexes); the UNION form simply deduplicates the rows matching both predicates.

## Q16: Rename the first column of a combined result set to `reference` in the output.

**Query:**
```sql
SELECT order_ref AS reference FROM web_orders
UNION
SELECT order_ref FROM store_orders;
```
**Explanation:** The output column name is taken from the FIRST SELECT; names and aliases in later branches are ignored.

## Q17: Fetch the single 5 newest orders across web and store, combined, then ordered and limited.

**Query:**
```sql
-- PostgreSQL
SELECT order_id, placed_at FROM web_orders
UNION ALL
SELECT order_id, placed_at FROM store_orders
ORDER BY placed_at DESC
LIMIT 5;
```
**Alt1:**
```sql
-- PostgreSQL (FETCH FIRST variant)
SELECT order_id, placed_at FROM web_orders
UNION ALL
SELECT order_id, placed_at FROM store_orders
ORDER BY placed_at DESC
FETCH FIRST 5 ROWS ONLY;
```
**Explanation:** ORDER BY and LIMIT/FETCH apply to the combined result as a whole and can reference the first branch's column names.

## Q18: Combine the monthly revenue of two regions into one result set (each branch aggregates before the union).

**Query:**
```sql
SELECT month, SUM(revenue) AS revenue FROM region_north GROUP BY month
UNION ALL
SELECT month, SUM(revenue) FROM region_south GROUP BY month
ORDER BY month;
```
**Explanation:** Each branch aggregates with GROUP BY before the set operator combines them; this stacks two grouped summaries into one grid.

## Q19: Students retook an exam; attempt_1 grades are (A,A,B) and attempt_2 are (A,B,B). Return the grades shared by both attempts, counting duplicates as many times as the SMALLER of the two counts (PostgreSQL).

**Query:**
```sql
-- PostgreSQL
SELECT grade FROM attempt_1
INTERSECT ALL
SELECT grade FROM attempt_2;
```
**Explanation:** INTERSECT ALL keeps duplicates up to the lesser multiplicity (here min(2,1)=1 for A, min(1,2)=1 for B, so A and B each once), while plain INTERSECT would drop to unique values.

## Q20: marketing_batches holds weekly email lists (with repeats) and unsubscribed holds opt-outs. Remove emails that unsubscribed, keeping the leftover multiplicity (PostgreSQL).

**Query:**
```sql
-- PostgreSQL
SELECT email FROM marketing_batches
EXCEPT ALL
SELECT email FROM unsubscribed;
```
**Explanation:** EXCEPT ALL subtracts per-value counts: each occurrence in the second set cancels one occurrence in the first, preserving the remaining duplicates.

## Q21: Your company upgraded MySQL to 8.0.31, which natively supports INTERSECT/EXCEPT. Rewrite Q5's January-February intersection natively.

**Query:**
```sql
-- MySQL 8.0.31+
SELECT customer_id FROM orders_jan
INTERSECT
SELECT customer_id FROM orders_feb;
```
**Explanation:** MySQL 8.0.31 added INTERSECT and EXCEPT; the IN-subquery emulation from Q5 remains useful for older instances.

## Q22: Combine three result sets with a mix of operators: intersect the 2025 and 2024 buyers, then append all 2026 buyers as extra rows (PostgreSQL).

**Query:**
```sql
-- PostgreSQL
(SELECT customer_id FROM orders_2025
 INTERSECT
 SELECT customer_id FROM orders_2024)
UNION ALL
SELECT customer_id FROM orders_2026;
```
**Explanation:** Parentheses force the intersection to be computed first, then UNION ALL appends the third set uncollapsed.

## Q23: Without parentheses, what does `A UNION B INTERSECT C` evaluate as? Show the parenthesized equivalent.

**Query:**
```sql
SELECT id FROM a
UNION
SELECT id FROM b
INTERSECT
SELECT id FROM c;
```
**Alt1:**
```sql
SELECT id FROM a
UNION
(SELECT id FROM b
 INTERSECT
 SELECT id FROM c);
```
**Explanation:** INTERSECT binds tighter than UNION/EXCEPT, so the un-parenthesized form equals `A UNION (B INTERSECT C)`; write the parentheses to make intent explicit.

## Q24: Find newsletter subscribers present in both the 2019 and 2020 signup tables in SQL Server, without duplicates.

**Query:**
```sql
-- SQL Server
SELECT EmailAddress FROM NewsletterSignups2019
INTERSECT
SELECT EmailAddress FROM NewsletterSignups2020;
```
**Explanation:** SQL Server INTERSECT returns rows common to both, deduplicated, comparing full projected rows.

## Q25: Data reconciliation, part 1 (PostgreSQL): list the rows that exist in the new stock snapshot but not in the old one, tagged 'NEW', keeping multiplicity.

**Query:**
```sql
-- PostgreSQL
SELECT 'NEW' AS change_type, product_id, stock
FROM snapshot_new
EXCEPT ALL
SELECT 'NEW', product_id, stock
FROM snapshot_old;
```
**Explanation:** The literal marker 'NEW' is identical in both branches so the difference is computed on (product_id, stock); EXCEPT ALL keeps repeated leftover rows.

## Q26: MySQL: find product_ids sold in 2026 but not in 2025. First write it with NOT IN, then explain why the result is empty when sales_2025 contains an unknown product (NULL).

**Query:**
```sql
-- MySQL (returns nothing if the subquery has NULLs)
SELECT DISTINCT product_id FROM sales_2026
WHERE product_id NOT IN (SELECT product_id FROM sales_2025);
```
**Alt1:**
```sql
-- MySQL (NULL-safe)
SELECT DISTINCT product_id FROM sales_2026 s
WHERE NOT EXISTS (SELECT 1 FROM sales_2025 o WHERE o.product_id = s.product_id);
```
**Explanation:** `NOT IN` with a NULL in the list makes every comparison UNKNOWN (never TRUE), so 0 rows return; NOT EXISTS compares per-row equality and stays correct.

## Q27: Same NOT IN difference, but you are not allowed to switch to NOT EXISTS — sanitize the subquery instead.

**Query:**
```sql
-- MySQL
SELECT DISTINCT product_id FROM sales_2026
WHERE product_id NOT IN (SELECT product_id FROM sales_2025
                         WHERE product_id IS NOT NULL);
```
**Explanation:** Filtering NULLs out of the subquery restores NOT IN's three-valued-logic safety; this is the fastest fix when refactoring is constrained.

## Q28: PostgreSQL: two snapshots both contain a row with product_id NULL. Show that INTERSECT still considers these rows as matching.

**Query:**
```sql
-- PostgreSQL
SELECT product_id FROM snapshot_new
INTERSECT
SELECT product_id FROM snapshot_old;
```
**Explanation:** Set operators treat NULLs as equal for grouping purposes (NULL groups with NULL), so the NULL-keyed row survives the intersection — whereas `a.product_id = b.product_id` would never match it.

## Q29: Extend Q28 to EXCEPT: a NULL product_id in snapshot_old must be subtracted when snapshot_new also has NULL keys. Is this the same behaviour as an equality anti-join?

**Query:**
```sql
-- PostgreSQL
SELECT product_id FROM snapshot_new
EXCEPT
SELECT product_id FROM snapshot_old;
```
**Explanation:** EXCEPT also groups NULLs together, so it subtracts NULL-keyed rows. An equality anti-join (NOT EXISTS / LEFT JOIN ... IS NULL) would NOT remove them — a frequent reconciliation surprise.

## Q30: Compare two MySQL intersection styles: IN subquery vs (8.0.31+) INTERSECT. Which turns into a semijoin, and what are the practical differences?

**Query:**
```sql
-- MySQL 8.0.31+
SELECT customer_id FROM orders_jan
INTERSECT
SELECT customer_id FROM orders_feb;
```
**Alt1:**
```sql
-- MySQL
SELECT DISTINCT customer_id FROM orders_jan
WHERE customer_id IN (SELECT customer_id FROM orders_feb);
```
**Explanation:** IN rewrites into a semijoin (stops scanning the inner side once a match is found); INTERSECT materialises and deduplicates both sides before comparing. For big sets, IN/EXISTS usually wins on cost; INTERSECT wins on readability and guarantees a distinct output.

## Q31: SQL Server: rewrite the EXCEPT "sold 2025 not 2024" as a correlated NOT EXISTS anti-join.

**Query:**
```sql
-- SQL Server
SELECT DISTINCT s.ProductID
FROM Sales_2025 s
WHERE NOT EXISTS (SELECT 1 FROM Sales_2024 o
                  WHERE o.ProductID = s.ProductID);
```
**Alt1:**
```sql
-- SQL Server (EXCEPT version)
SELECT ProductID FROM Sales_2025
EXCEPT
SELECT ProductID FROM Sales_2024;
```
**Explanation:** NOT EXISTS is a NULL-safe anti-join that short-circuits per row; EXCEPT is equivalent for non-NULL keys and is inherently DISTINCT.

## Q32: PostgreSQL: use LEFT JOIN ... IS NULL as an alternative expression of "products in new inventory not in old inventory".

**Query:**
```sql
-- PostgreSQL
SELECT product_id FROM inventory_new
EXCEPT
SELECT product_id FROM inventory_old;
```
**Alt1:**
```sql
-- PostgreSQL (anti-join alternative)
SELECT DISTINCT n.product_id
FROM inventory_new n
LEFT JOIN inventory_old o ON o.product_id = n.product_id
WHERE o.product_id IS NULL;
```
**Explanation:** Both implement set difference; the LEFT JOIN form is plan-friendly on indexed keys, while EXCEPT reads more clearly at small scale.

## Q33: EXCEPT dropped duplicate leftover rows that you actually need. Show the EXCEPT ALL version that keeps them.

**Query:**
```sql
-- PostgreSQL
SELECT product_id FROM stock_today
EXCEPT ALL
SELECT product_id FROM stock_last_week;
```
**Alt1:**
```sql
-- PostgreSQL (unique-only variant)
SELECT product_id FROM stock_today
EXCEPT
SELECT product_id FROM stock_last_week;
```
**Explanation:** EXCEPT collapses its output to distinct values; EXCEPT ALL retains the leftover multiplicity whether or not the second query contained repeats.

## Q34: MySQL has no FULL OUTER JOIN: combine two anti-joins to produce the symmetric difference of a and b, and compare with the NOT IN equivalent.

**Query:**
```sql
-- MySQL (set-style, via NOT IN)
SELECT id FROM a WHERE id NOT IN (SELECT id FROM b WHERE id IS NOT NULL)
UNION ALL
SELECT id FROM b WHERE id NOT IN (SELECT id FROM a WHERE id IS NOT NULL);
```
**Alt1:**
```sql
-- MySQL (join-based symmetric difference)
SELECT a.id FROM a LEFT JOIN b ON a.id = b.id WHERE b.id IS NULL
UNION ALL
SELECT b.id FROM b LEFT JOIN a ON b.id = a.id WHERE a.id IS NULL;
```
**Explanation:** A left-and-right anti-join pair (or two NOT IN) merged with UNION ALL reconstructs FULL OUTER JOIN's unmatched rows where the dialect lacks FULL JOIN syntax.

## Q35: payroll_active and payroll_archive both carry a nullable employee key. Show that IN silently misses NULL-key matches while INTERSECT groups them.

**Query:**
```sql
-- MySQL 8.0.31+ (safe for NULLs)
SELECT emp_no FROM payroll_active
INTERSECT
SELECT emp_no FROM payroll_archive;
```
**Alt1:**
```sql
-- MySQL (NULL-blind)
SELECT DISTINCT emp_no FROM payroll_active
WHERE emp_no IN (SELECT emp_no FROM payroll_archive);
```
**Explanation:** `emp_no IN (... NULL ...)` never yields TRUE, so NULL-keyed rows vanish; INTERSECT treats NULLs as one group so they match — know which semantics your reconciliation needs.

## Q36: SQL Server HR tables: report the (id, name) rows whose content differs between the current and archive snapshots using EXCEPT.

**Query:**
```sql
-- SQL Server
SELECT ID, Name FROM Employee_Current
EXCEPT
SELECT ID, Name FROM Employee_Archive;
```
**Explanation:** Full projection comparison — any row differing in ID or Name is returned; use EXCEPT ALL to also expose repeated differences.

## Q37: PostgreSQL: stock_today has 3 rows for product P, stock_last_week has 2. Show EXCEPT, then EXCEPT ALL, and reason about the outputs. Then give a MySQL 8.0 emulation crossing semantics with ordinals.

**Query:**
```sql
-- PostgreSQL
SELECT product_id FROM stock_today
EXCEPT ALL
SELECT product_id FROM stock_last_week;
```
**Alt1:**
```sql
-- MySQL 8.0+ (EXCEPT ALL emulation via ordinal-matched anti-join)
SELECT t.product_id
FROM (SELECT product_id,
             ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY product_id) AS rn
      FROM stock_today) t
LEFT JOIN (SELECT product_id,
                  ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY product_id) AS rn
           FROM stock_last_week) o
  ON t.product_id = o.product_id AND t.rn = o.rn
WHERE o.product_id IS NULL;
```
**Explanation:** EXCEPT ALL keeps 3-2=1 duplicate of P; EXCEPT yields a single unique P. The MySQL emulation orders duplicates and anti-joins on equal ordinals, cancelling the first 2 occurrences and leaving the 3rd — EXCEPT ALL semantics without the operator.

## Q38: Shared grades across two attempts: (A,A,B) and (A,B,B). Return grades with min-multiplicity in PostgreSQL, then give the MySQL ROW_NUMBER emulation.

**Query:**
```sql
-- PostgreSQL
SELECT grade FROM attempt_1
INTERSECT ALL
SELECT grade FROM attempt_2;
```
**Alt1:**
```sql
-- MySQL 8.0+ (INTERSECT ALL emulation via ordinal-matched inner join)
SELECT t.grade
FROM (SELECT grade, ROW_NUMBER() OVER (PARTITION BY grade ORDER BY grade) AS rn
      FROM attempt_1) t
JOIN (SELECT grade, ROW_NUMBER() OVER (PARTITION BY grade ORDER BY grade) AS rn
      FROM attempt_2) o
  ON t.grade = o.grade AND t.rn = o.rn;
```
**Explanation:** INTERSECT ALL counts each shared grade once per min(each count); pairing duplicates by ordinal reproduces those counts in any MySQL 8.0+ that lacks INTERSECT ALL.

## Q39: SQL Server: apply TOP 3 to the WHOLE intersection result, not to one branch. Explain the naive-placement mistake and show the derived-table fix.

**Query:**
```sql
-- SQL Server (correct: derived table)
SELECT TOP 3 CustomerID
FROM (
  SELECT CustomerID FROM Orders_2025
  INTERSECT
  SELECT CustomerID FROM Orders_2024
) x
ORDER BY CustomerID;
```
**Explanation:** `<SELECT> TOP n INTERSECT <SELECT>` would cap only the first branch; wrapping the intersection in a derived table makes TOP apply to the combined, deduplicated rows.

## Q40: MySQL 8.0.31+: write inventory differences (new minus old) with the native EXCEPT operator.

**Query:**
```sql
-- MySQL 8.0.31+
SELECT product_id FROM inventory_new
EXCEPT
SELECT product_id FROM inventory_old;
```
**Explanation:** MySQL 8.0.31 added INTERSECT and EXCEPT; EXCEPT returns distinct rows of the first query not present in the second.

## Q41: Oracle: sales_2026 vs sales_2025 product differences via MINUS; note how MINUS handles duplicates and NULLs.

**Query:**
```sql
-- Oracle
SELECT product_id FROM sales_2026
MINUS
SELECT product_id FROM sales_2025;
```
**Explanation:** MINUS is Oracle's EXCEPT: distinct rows of the first set not in the second; Oracle groups NULLs as equal during its difference phase.

## Q42: Bidirectional data reconciliation (PostgreSQL): produce every differing row between old_version and new_version (same shape), labelled 'OLD' or 'NEW' against the snapshot it belongs to.

**Query:**
```sql
-- PostgreSQL
SELECT 'OLD' AS side, col1, col2 FROM old_version
EXCEPT ALL
SELECT 'OLD', col1, col2 FROM new_version
UNION ALL
SELECT 'NEW' AS side, col1, col2 FROM new_version
EXCEPT ALL
SELECT 'NEW', col1, col2 FROM old_version;
```
**Explanation:** Each half subtracts the opposite side (the marker literal is identical within a half), tagging every row unique to one snapshot; EXCEPT ALL keeps multiplicity.

## Q43: accounts_old/new differ only in an ignored last_seen timestamp. Reconcile them in PostgreSQL while ignoring that column.

**Query:**
```sql
-- PostgreSQL
SELECT customer_id, name, plan FROM accounts_new
EXCEPT ALL
SELECT customer_id, name, plan FROM accounts_old;
```
**Explanation:** EXCEPT compares only the projected columns, so omitting last_seen keeps the comparison stable and reports business-logic drift alone.

## Q44: Verify that products_old and products_new are logically identical except for updated_at; count the actual business diffs.

**Query:**
```sql
-- PostgreSQL
SELECT COUNT(*) AS real_diffs
FROM (
  SELECT id, title, price FROM products_new
  EXCEPT
  SELECT id, title, price FROM products_old
) d;
```
**Explanation:** A 0 count proves the two snapshots agree on every projected column; any change in the stripped timestamp is invisible to the set operator.

## Q45: Which customers placed an order in EVERY store branch? Give a relational-division version (GROUP BY/HAVING) and the set-based chained-INTERSECT sketch.

**Query:**
```sql
-- PostgreSQL
SELECT customer_id
FROM orders
GROUP BY customer_id
HAVING COUNT(DISTINCT store_id) = (SELECT COUNT(*) FROM stores);
```
**Alt1:**
```sql
-- PostgreSQL (chained INTERSECT for two stores)
SELECT customer_id FROM orders WHERE store_id = 1
INTERSECT
SELECT customer_id FROM orders WHERE store_id = 2;
```
**Explanation:** "In all branches" is relational division: group by customer and test the distinct-store count against the total; with a short fixed branch list, chained INTERSECTs work just as well.

## Q46: Merge the API audit log and the manual audit log into one feed, tagging the origin, newest first.

**Query:**
```sql
SELECT log_ts, 'API' AS source, message FROM api_log
UNION ALL
SELECT log_ts, 'MANUAL', message FROM manual_log
ORDER BY log_ts DESC
LIMIT 100;
```
**Explanation:** UNION ALL stacks the two sources uncollapsed; the constant column tags provenance, and the trailing ORDER BY/LIMIT applies to the combined feed.

## Q47: price_master and price_override both publish prices; keep a single price per product_id, preferring the most recently updated row from either source.

**Query:**
```sql
-- PostgreSQL
SELECT product_id, price FROM (
  SELECT product_id, price, updated_at,
         ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY updated_at DESC) AS rn
  FROM (
    SELECT product_id, price, updated_at FROM price_master
    UNION ALL
    SELECT product_id, price, updated_at FROM price_override
  ) all_prices
) ranked
WHERE rn = 1;
```
**Explanation:** UNION ALL concatenates the sources, then a window re-selects exactly one winner per key — stack first, dedupe deliberately.

## Q48: Produce a channel-wise KPI table (distinct customers per channel) for email, SMS and web as rows of one result set.

**Query:**
```sql
SELECT 'EMAIL' AS channel, COUNT(DISTINCT customer_id) AS customers FROM email_campaigns
UNION ALL
SELECT 'SMS', COUNT(DISTINCT customer_id) FROM sms_campaigns
UNION ALL
SELECT 'WEB', COUNT(DISTINCT customer_id) FROM web_sessions;
```
**Explanation:** Scalar aggregates become rows: each SELECT computes one number and UNION ALL stacks them into a tidy dimension-to-metric grid.

## Q49: Build a clean, de-duplicated list of people who are admins, managers, or both.

**Query:**
```sql
SELECT emp_id, emp_name FROM admins
UNION
SELECT emp_id, emp_name FROM managers;
```
**Explanation:** UNION discards duplicates, so someone in both tables appears exactly once; UNION ALL here would double-count overlaps.

## Q50: Which tags are used on BOTH article 1001 and article 1002? Use INTERSECT, then compare with an EXISTS formulation.

**Query:**
```sql
-- PostgreSQL
SELECT tag_id FROM article_tags WHERE article_id = 1001
INTERSECT
SELECT tag_id FROM article_tags WHERE article_id = 1002;
```
**Alt1:**
```sql
SELECT tag_id
FROM article_tags a1
WHERE a1.article_id = 1001
  AND EXISTS (SELECT 1 FROM article_tags a2
              WHERE a2.article_id = 1002 AND a2.tag_id = a1.tag_id);
```
**Explanation:** Filtering the same table by two conditions with INTERSECT is a set-style AND; EXISTS articulates the same membership test step by step.

## Q51: After a UNION, order the combined result using either a column alias from the first SELECT or a positional reference.

**Query:**
```sql
-- PostgreSQL
SELECT product_id AS id, price FROM price_list
UNION
SELECT product_id, price FROM historic_price
ORDER BY id DESC;
```
**Alt1:**
```sql
-- PostgreSQL
SELECT product_id AS id, price FROM price_list
UNION
SELECT product_id, price FROM historic_price
ORDER BY 1 DESC;
```
**Explanation:** ORDER BY can target the first branch's alias OR the ordinal 1; both evaluate after the union is materialised.

## Q52: Sequential subtraction: master_list minus unsubscribed minus bounced. Write it and explain the evaluation order.

**Query:**
```sql
-- PostgreSQL
SELECT email FROM master_list
EXCEPT
SELECT email FROM unsubscribed_2025
EXCEPT
SELECT email FROM bounced;
```
**Explanation:** Chained EXCEPT is left-associative: `(master_list - unsubscribed) - bounced`. Every set that lists the email removes it, regardless of position.

## Q53: What does `A UNION B EXCEPT C` compute? Show the equivalent parenthesised form and state the precedence rules.

**Query:**
```sql
SELECT id FROM a
UNION
SELECT id FROM b
EXCEPT
SELECT id FROM c;
```
**Alt1:**
```sql
(SELECT id FROM a
 UNION
 SELECT id FROM b)
EXCEPT
SELECT id FROM c;
```
**Explanation:** UNION and EXCEPT share precedence and associate left-to-right, so `A UNION B EXCEPT C` = `(A UNION B) EXCEPT C`; INTERSECT would bind tighter had it been included.

## Q54: Count how many DISTINCT products exist across both the 2025 and 2026 catalogs, combining set operators with an aggregate over a derived table.

**Query:**
```sql
-- PostgreSQL
SELECT COUNT(*) AS distinct_products
FROM (
  SELECT product_id FROM catalog_2025
  UNION
  SELECT product_id FROM catalog_2026
) all_products;
```
**Explanation:** The inner UNION deduplicates across catalogs and COUNT(*) on the derived table measures the union's cardinality — a classic "distinct across sources" pattern.

## Q55: tweets_a and tweets_b are bags of hashtags. Count matching hashtags where each duplicate matches min-count times (PostgreSQL).

**Query:**
```sql
-- PostgreSQL
SELECT COUNT(*) AS shared_tags
FROM (
  SELECT tag FROM tweets_a
  INTERSECT ALL
  SELECT tag FROM tweets_b
) x;
```
**Explanation:** INTERSECT ALL yields one row per min(occurrences_a, occurrences_b); counting the result gives the total multiplicity-aware overlap.

## Q56: A reporting grid must not skip stores with zero sales. Append a store row with 0 orders for stores that produced nothing.

**Query:**
```sql
-- PostgreSQL
SELECT store_id, COUNT(*) AS orders FROM sales GROUP BY store_id
UNION ALL
SELECT store_id, 0 FROM stores
WHERE store_id NOT IN (SELECT store_id FROM sales WHERE store_id IS NOT NULL);
```
**Explanation:** The grouped branch lists real counts; the second branch injects literal (store, 0) rows via UNION ALL, and the NOT IN guard prevents double-counting existing stores.

## Q57: Pick customers who appear in both orders and returns. Write the INTERSECT, EXISTS and IN forms and compare execution shapes.

**Query:**
```sql
-- PostgreSQL
SELECT customer_id FROM orders
INTERSECT
SELECT customer_id FROM returns;
```
**Alt1:**
```sql
SELECT DISTINCT customer_id FROM orders o
WHERE EXISTS (SELECT 1 FROM returns r WHERE r.customer_id = o.customer_id);
```
**Alt2:**
```sql
SELECT customer_id FROM orders
WHERE customer_id IN (SELECT customer_id FROM returns);
```
**Explanation:** INTERSECT materialises both sides, deduplicates and compares; EXISTS is an early-exiting semi-join; IN typically resolves to a semi-join or hashed probe. All return the same distinct set — choose by data sizes and index availability.

## Q58: "products in inventory but not shipped" — compare NOT IN, NOT EXISTS and EXCEPT and their NULL behaviour in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT product_id FROM inventory
EXCEPT
SELECT product_id FROM shipped;
```
**Alt1:**
```sql
SELECT DISTINCT product_id FROM inventory i
WHERE NOT EXISTS (SELECT 1 FROM shipped s WHERE s.product_id = i.product_id);
```
**Alt2:**
```sql
SELECT DISTINCT product_id FROM inventory
WHERE product_id NOT IN (SELECT product_id FROM shipped
                         WHERE product_id IS NOT NULL);
```
**Explanation:** EXCEPT and NOT EXISTS are NULL-safe; NOT IN silently empties the result if shipped contains a NULL product_id unless filtered. EXCEPT is also inherently DISTINCT.

## Q59: Detect customers whose balance changed between accounts_old and accounts_new. Show a set-based version and a side-by-side alternative.

**Query:**
```sql
-- PostgreSQL
SELECT customer_id, balance FROM accounts_new
EXCEPT ALL
SELECT customer_id, balance FROM accounts_old;
```
**Alt1:**
```sql
-- side-by-side view of the changed customers
SELECT o.customer_id, o.balance AS old_balance, n.balance AS new_balance
FROM accounts_old o
JOIN accounts_new n USING (customer_id)
WHERE o.balance IS DISTINCT FROM n.balance;
```
**Explanation:** EXCEPT ALL reports the NEW projection of any changed/inserted row; when both old and new values belong on one line, join on the key and compare with IS DISTINCT FROM.

## Q60: billing_export pads customer codes with spaces but crm_customers is clean. Normalise the keys so the UNION deduplicates logically equal codes.

**Query:**
```sql
SELECT LTRIM(customer_code) FROM billing_export
UNION
SELECT customer_code FROM crm_customers;
```
**Alt1:**
```sql
SELECT customer_code FROM (
  SELECT LTRIM(customer_code) AS customer_code FROM billing_export
  UNION ALL
  SELECT customer_code FROM crm_customers
) normalized;
```
**Explanation:** Set operators compare values verbatim; apply a normalising expression inside the branches so 'ACME' and 'ACME ' collapse into one dedup group.

## Q61: Why does `ORDER BY salary` fail here, and what is the correct fix regardless of branch naming?

**Query:**
```sql
SELECT id, name FROM employees
UNION ALL
SELECT id, name FROM contractors
ORDER BY 2;
```
**Explanation:** Output names come from the first SELECT, so a later branch's own column name is not addressable; ORDER BY on a positional ordinal (2 = name) always works.

## Q62: Return the 3 newest web orders and the 3 newest store orders, merged, then keep only the 5 overall newest.

**Query:**
```sql
-- PostgreSQL
(SELECT order_id, placed_at FROM web_orders ORDER BY placed_at DESC LIMIT 3)
UNION ALL
(SELECT order_id, placed_at FROM store_orders ORDER BY placed_at DESC LIMIT 3)
ORDER BY placed_at DESC
LIMIT 5;
```
**Explanation:** Parentheses scope each branch's ORDER BY/LIMIT to its own SELECT; the outer ORDER BY + LIMIT then trims the combined 6 rows to 5.

## Q63: customers_web and customers_store both list a name with a NULL region. Does UNION produce one row or two?

**Query:**
```sql
SELECT name, region FROM customers_web
UNION
SELECT name, region FROM customers_store;
```
**Explanation:** Exactly one (name, NULL) row: set operators group NULLs together, so NULL belongs to a single dedup group — unlike equality joins, where NULL = NULL is UNKNOWN.

## Q64: Group the distinct regions from Q63 and order the groups with NULLs at the end.

**Query:**
```sql
-- PostgreSQL
SELECT region, COUNT(*) AS customers
FROM (
  SELECT region FROM customers_web
  UNION
  SELECT region FROM customers_store
) r
GROUP BY region
ORDER BY region NULLS LAST;
```
**Explanation:** GROUP BY aggregates the union's distinct regions; NULLS LAST (PostgreSQL) places the NULL bucket at the bottom explicitly.

## Q65: Oracle: MINUS with a renamed output column, ordered by that output name.

**Query:**
```sql
-- Oracle
SELECT product_id AS pid FROM catalog_live
MINUS
SELECT product_id FROM catalog_draft
ORDER BY pid;
```
**Explanation:** MINUS's output is labelled by the first query (here pid), and ORDER BY may reference that alias after the set operation completes.

## Q66: SQL Server QA: how many rows differ between the current and previous payroll snapshots?

**Query:**
```sql
-- SQL Server
SELECT COUNT(*) AS differences
FROM (
  SELECT EmployeeID, Salary FROM HrSnapshotCurrent
  EXCEPT
  SELECT EmployeeID, Salary FROM HrSnapshotPrevious
) d;
```
**Explanation:** The derived table holds exactly the differing rows and COUNT(*) asserts drift magnitude for a CI gate; 0 means content parity.

## Q67: Compare order sets between the prod and staging schemas of the same PostgreSQL instance.

**Query:**
```sql
-- PostgreSQL
SELECT order_id FROM prod.orders
EXCEPT
SELECT order_id FROM staging.orders;
```
**Explanation:** Qualifying tables per-schema lets set operators compare data across logical environments in one query — an effective promotion-readiness smoke test.

## Q68: The ETL result staging.customers must equal dw.customers. Write an assertion returning 0 when the two are identical (multiplicity included).

**Query:**
```sql
-- PostgreSQL
SELECT COUNT(*) AS drift
FROM (
  SELECT * FROM staging.customers
  EXCEPT ALL
  SELECT * FROM dw.customers
) x;
```
**Explanation:** In this direction, leftover rows are entries present more times in staging than in dw; 0 here (combined with the reverse direction from Q91/Q97) proves bag equality.

## Q69: Two partner sources both store customers; merge them and keep, per email, the row with the most recent update.

**Query:**
```sql
-- PostgreSQL
SELECT email, region
FROM (
  SELECT email, region, updated_at,
         ROW_NUMBER() OVER (PARTITION BY email ORDER BY updated_at DESC) AS rn
  FROM (
    SELECT email, region, updated_at FROM source_a
    UNION ALL
    SELECT email, region, updated_at FROM source_b
  ) u
) x
WHERE rn = 1;
```
**Explanation:** UNION ALL preserves both copies of an email; windowing ranks them and picks the freshest — dedupe after stacking with a recency-based tie-breaker.

## Q70: Which (policy_id, coverage_code) pairs exist in BOTH quotes and issued_policies (PostgreSQL)?

**Query:**
```sql
-- PostgreSQL
SELECT policy_id, coverage_code FROM quotes
INTERSECT
SELECT policy_id, coverage_code FROM issued_policies;
```
**Explanation:** The composite projection is compared as a whole; a policy matching only the ID but differing in coverage is correctly excluded.

## Q71: Find customers who ordered from both the flagship store and the outlet store; give INTERSECT and EXISTS forms.

**Query:**
```sql
-- PostgreSQL
SELECT customer_id FROM orders_flagship
INTERSECT
SELECT customer_id FROM orders_outlet;
```
**Alt1:**
```sql
SELECT DISTINCT customer_id FROM orders_flagship f
WHERE EXISTS (SELECT 1 FROM orders_outlet o
              WHERE o.customer_id = f.customer_id);
```
**Explanation:** INTERSECT is the direct expression of "belongs to both sets"; EXISTS formulates the same membership with a correlated probe.

## Q72: Prove EXCEPT is NOT commutative: compare counts of a-b and b-a and explain when they coincide.

**Query:**
```sql
-- PostgreSQL
SELECT 'A_MINUS_B' AS direction, COUNT(*) FROM (SELECT col FROM a EXCEPT SELECT col FROM b) x
UNION ALL
SELECT 'B_MINUS_A', COUNT(*) FROM (SELECT col FROM b EXCEPT SELECT col FROM a) y;
```
**Explanation:** The two SELECTs compute each difference direction and UNION ALL stacks the counts; results differ whenever a and b are asymmetric (equal only when the sets are identical).

## Q73: MySQL bonus payouts: which bonus_id is NOT in paid_bonuses? Contrast the NOT IN (NULL-poisoned) and the 8.0.31 EXCEPT (NULL-safe) answers.

**Query:**
```sql
-- MySQL 8.0.31+
SELECT bonus_id FROM bonuses
EXCEPT
SELECT bonus_id FROM paid_bonuses;
```
**Alt1:**
```sql
-- MySQL (NULL-poisoned form)
SELECT bonus_id FROM bonuses
WHERE bonus_id NOT IN (SELECT bonus_id FROM paid_bonuses);
```
**Explanation:** If paid_bonuses has a NULL bonus_id, NOT IN returns nothing; native EXCEPT groups NULLs like a value and behaves safely. Choose the semantics you need — don't guess.

## Q74: Compare two grouped revenue summaries (staging vs prod) and surface the groups whose totals disagree.

**Query:**
```sql
-- PostgreSQL
SELECT period, SUM(revenue) AS revenue
FROM staging_orders
GROUP BY period
EXCEPT ALL
SELECT period, SUM(revenue)
FROM prod_orders
GROUP BY period;
```
**Explanation:** Each branch is a complete GROUP BY query; the set operator then diffs the aggregated projections, revealing periods where totals differ plus any staging-only periods.

## Q75: Full symmetric price reconciliation (PostgreSQL): list every (sku, price) reading that exists in only one of POS and e-commerce.

**Query:**
```sql
-- PostgreSQL
SELECT sku, unit_price FROM pos_sales
EXCEPT ALL
SELECT sku, unit_price FROM ecom_orders
UNION ALL
SELECT sku, unit_price FROM ecom_orders
EXCEPT ALL
SELECT sku, unit_price FROM pos_sales;
```
**Explanation:** Each difference direction is merged with UNION ALL: pos-only rows first, then ecom-only rows — the complete, multiplicity-preserving snapshot diff.

## Q76: Products sold in EACH of the four quarters of 2026 — chain INTERSECTs and relate the result to relational division.

**Query:**
```sql
-- PostgreSQL
SELECT product_id FROM q1_sales
INTERSECT
SELECT product_id FROM q2_sales
INTERSECT
SELECT product_id FROM q3_sales
INTERSECT
SELECT product_id FROM q4_sales;
```
**Explanation:** Chained INTERSECT keeps only rows present in every operand — membership in all four sets, i.e. the fixed-width division "sold in every quarter".

## Q77: A reconciliation dashboard wants drift direction: count only_new and only_old rows in one query.

**Query:**
```sql
-- PostgreSQL
SELECT 'NEW_ONLY' AS drift, COUNT(*) AS rows
FROM (SELECT * FROM snapshot_new EXCEPT ALL SELECT * FROM snapshot_old) n
UNION ALL
SELECT 'OLD_ONLY', COUNT(*)
FROM (SELECT * FROM snapshot_old EXCEPT ALL SELECT * FROM snapshot_new) o;
```
**Explanation:** Both directions are computed over the same projection and stacked as named rows; the NEW_ONLY vs OLD_ONLY balance reveals which snapshot moved first.

## Q78: Intersect students with a numeric score against a table that lacks that column — pad with a typed NULL and keep NULLs matching.

**Query:**
```sql
-- PostgreSQL
SELECT id, name, CAST(NULL AS numeric) AS score FROM students
INTERSECT
SELECT id, name, score FROM national_scores;
```
**Explanation:** The typed NULL completes the projection and participates as a NULL group — students without a score still intersect against a NULL score instead of erroring on column count.

## Q79: Postgres accepts the explicit DISTINCT spelling. Write UNION DISTINCT explicitly and contrast it with UNION ALL.

**Query:**
```sql
-- PostgreSQL
SELECT id FROM a
UNION DISTINCT
SELECT id FROM b;
```
**Explanation:** `UNION` and `UNION DISTINCT` are identical and accepted explicitly; `UNION DISTINCT` deduplicates while `UNION ALL` simply appends.

## Q80: Find orders that are BOTH high-value AND flagged, using a single-table INTERSECT, then a plain AND predicate.

**Query:**
```sql
-- PostgreSQL
SELECT order_id, amount, flagged FROM orders WHERE amount > 10000
INTERSECT
SELECT order_id, amount, flagged FROM orders WHERE flagged = 1;
```
**Alt1:**
```sql
SELECT order_id, amount, flagged FROM orders
WHERE amount > 10000 AND flagged = 1;
```
**Explanation:** INTERSECT expresses the AND of two predicates as a set operation; the plain AND is simpler, but the INTERSECT shape lets each branch use separate indexes.

## Q81: Classify a snapshot diff into INSERT and DELETE style rows using tagged EXCEPTs (IDs only), and note what this misses.

**Query:**
```sql
-- PostgreSQL
SELECT 'INSERT' AS op, customer_id FROM curated.customers
EXCEPT ALL
SELECT 'INSERT', customer_id FROM raw.customers
UNION ALL
SELECT 'DELETE' AS op, customer_id FROM raw.customers
EXCEPT ALL
SELECT 'DELETE', customer_id FROM curated.customers;
```
**Explanation:** Identity-keyed diff tags only newly-seen and vanished IDs; a key present in both snapshots but with changed attributes appears in neither half — pair this with Q59's value-diff for a full picture.

## Q82: Signup lists use inconsistent casing; deduplicate emails case-insensitively across both sources.

**Query:**
```sql
SELECT LOWER(email) AS email FROM signup_a
UNION
SELECT LOWER(email) FROM signup_b;
```
**Explanation:** Set operators compare values verbatim, so normalising to lowercase inside each branch makes 'John@x.com' and 'john@x.com' a single group.

## Q83: Legacy and new order systems store timestamps; compare which calendar days have orders in both, normalising to dates first.

**Query:**
```sql
-- PostgreSQL
SELECT TO_CHAR(order_date, 'YYYY-MM-DD') FROM legacy_orders
INTERSECT
SELECT TO_CHAR(order_date, 'YYYY-MM-DD') FROM new_orders;
```
**Explanation:** Projecting to the date string lets INTERSECT compare day-level membership; without normalisation, identical calendar days at different times would not intersect.

## Q84: The output name of an INTERSECT comes from the first branch. Confirm with a query and note the consequence for report headers.

**Query:**
```sql
-- PostgreSQL
SELECT worker_id AS id FROM source_a
INTERSECT
SELECT person_id FROM source_b;
```
**Explanation:** The combined set's column is labelled id (from the first branch); person_id — even if semantically correct — is dropped. Order and alias the first query to control headers.

## Q85: MySQL 8.0+: reproduce EXCEPT ALL (leftover duplicates) with a ROW_NUMBER anti-join. stock_today has 3 copies of P, stock_last_week has 2.

**Query:**
```sql
-- MySQL (EXCEPT ALL emulation, ordinal anti-join)
SELECT t.product_id
FROM (SELECT product_id,
             ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY product_id) AS rn
      FROM stock_today) t
LEFT JOIN (SELECT product_id,
                  ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY product_id) AS rn
           FROM stock_last_week) o
  ON t.product_id = o.product_id AND t.rn = o.rn
WHERE o.product_id IS NULL;
```
**Explanation:** Matching first occurrence to first occurrence cancels 2 copies and leaves the 3rd — EXCEPT ALL semantics without the operator. The ORDER BY inside the partition must be deterministic to avoid arbitrary duplicate pairing.

## Q86: MySQL 8.0+: reproduce INTERSECT ALL (min-multiplicity) with a ROW_NUMBER inner join.

**Query:**
```sql
-- MySQL (INTERSECT ALL emulation, ordinal join)
SELECT t.grade
FROM (SELECT grade, ROW_NUMBER() OVER (PARTITION BY grade ORDER BY grade) AS rn
      FROM attempt_1) t
JOIN (SELECT grade, ROW_NUMBER() OVER (PARTITION BY grade ORDER BY grade) AS rn
      FROM attempt_2) o
  ON t.grade = o.grade AND t.rn = o.rn;
```
**Explanation:** Pairing duplicates by ordinal yields exactly min(each count) shared copies per value — the INTERSECT ALL guarantee — available in MySQL long before any INTERSECT ALL existed.

## Q87: Oracle 12c+: order and paginate a UNION with FETCH FIRST 10 ROWS ONLY.

**Query:**
```sql
-- Oracle 12c+
SELECT name FROM (
  SELECT name FROM managers
  UNION
  SELECT name FROM directors
)
ORDER BY name
FETCH FIRST 10 ROWS ONLY;
```
**Explanation:** Wrapping the union in a derived table lets ORDER BY + FETCH FIRST address the combined result (Oracle's equivalent of LIMIT applied post-union).

## Q88: Order a UNION ALL with explicit NULL placement in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
SELECT id FROM source_a
UNION ALL
SELECT id FROM source_b
ORDER BY id NULLS FIRST;
```
**Explanation:** ORDER BY runs after the union; NULLS FIRST pushes unknown keys to the top, giving deliberate placement instead of dialect default.

## Q89: Validate foreign keys WITHOUT joins: list employee department_ids that reference no department (set-difference anti-join).

**Query:**
```sql
-- PostgreSQL
SELECT DISTINCT department_id FROM employees
EXCEPT
SELECT department_id FROM departments;
```
**Explanation:** The orphans are exactly employee_depts minus valid_depts; EXCEPT exposes referential-integrity violations without writing a single JOIN.

## Q90: test_runs logs each attempt twice (statuses 'attempted' and 'passed'). Find tests that have BOTH statuses recorded — a single-table INTERSECT idiom.

**Query:**
```sql
-- PostgreSQL
SELECT test_id FROM test_runs WHERE status = 'attempted'
INTERSECT
SELECT test_id FROM test_runs WHERE status = 'passed';
```
**Alt1:**
```sql
SELECT test_id FROM test_runs t1
WHERE status = 'attempted'
  AND EXISTS (SELECT 1 FROM test_runs t2
              WHERE t2.test_id = t1.test_id AND t2.status = 'passed');
```
**Explanation:** Both predicates target the same table but different rows; the set intersection compactly says "has an attempted row AND has a passed row".

## Q91: Multiset equality: prove tbl_a and tbl_b contain the identical bag of rows (order irrelevant, counts included), using both difference directions.

**Query:**
```sql
-- PostgreSQL
SELECT 'A_EXTRA' AS direction, COUNT(*) FROM (SELECT * FROM tbl_a EXCEPT ALL SELECT * FROM tbl_b) x
UNION ALL
SELECT 'B_EXTRA', COUNT(*) FROM (SELECT * FROM tbl_b EXCEPT ALL SELECT * FROM tbl_a) y;
```
**Explanation:** Both counts being 0 means neither side has leftover multiplicity — the two tables are row-bag identical regardless of physical row order.

## Q92: Merge two enrollment sources and flag primary keys duplicated ACROSS sources.

**Query:**
```sql
SELECT student_id, COUNT(*) AS copies
FROM (
  SELECT student_id FROM enrollments_a
  UNION ALL
  SELECT student_id FROM enrollments_b
) merged
GROUP BY student_id
HAVING COUNT(*) > 1;
```
**Explanation:** UNION ALL preserves both copies so GROUP BY/HAVING count>1 exposes keys present in both sources (or duplicated within one).

## Q93: Customers whose total spend exceed 1000 AND who are campaign-eligible — intersect a grouped set with a plain set.

**Query:**
```sql
-- PostgreSQL
SELECT customer_id FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 1000
INTERSECT
SELECT customer_id FROM campaign_eligible;
```
**Explanation:** A complete GROUP BY/HAVING query forms one operand of the INTERSECT; derived and aggregated sets compose freely with set operators.

## Q94: Mixed ALL semantics: (A INTERSECT ALL B) EXCEPT ALL C — compute the min-count intersection, then subtract C's counts.

**Query:**
```sql
-- PostgreSQL
SELECT grade FROM attempt_1
INTERSECT ALL
SELECT grade FROM attempt_2
EXCEPT ALL
SELECT grade FROM attempt_3;
```
**Explanation:** INTERSECT binds first (higher precedence): compute min(1,2) per grade, then EXCEPT ALL subtracts one copy per occurrence in attempt_3. Stacking ALL-versions keeps duplicates meaningful end to end.

## Q95: Reconciliation pitfall: two tables identical except unprojected columns. Show why EXCEPT reports "no diff" when you forgot the timestamp column.

**Query:**
```sql
-- PostgreSQL
SELECT user_id, email FROM user_prod
EXCEPT ALL
SELECT user_id, email FROM user_staging;
```
**Alt1:**
```sql
-- include the volatile column to actually capture it
SELECT user_id, email, updated_at FROM user_prod
EXCEPT ALL
SELECT user_id, email, updated_at FROM user_staging;
```
**Explanation:** EXCEPT only sees the projected columns, so 0 rows here does not mean equality — updated_at was dropped. Project every column your diff must cover.

## Q96: MySQL symmetric difference WITHOUT any joins or FULL JOIN — two NOT IN (NULL-filtered) subqueries merged.

**Query:**
```sql
-- MySQL
SELECT id FROM a WHERE id NOT IN (SELECT id FROM b WHERE id IS NOT NULL)
UNION ALL
SELECT id FROM b WHERE id NOT IN (SELECT id FROM a WHERE id IS NOT NULL);
```
**Explanation:** Each NOT IN computes one side of the difference; UNION ALL merges both sides, reconstructing the symmetric difference from pure set constructs.

## Q97: Final ETL health gate: one query that prints 'IN_SYNC' when the source and destination are row-bag identical, else 'DRIFT'.

**Query:**
```sql
-- PostgreSQL
SELECT CASE
  WHEN (SELECT COUNT(*) FROM (SELECT * FROM src EXCEPT ALL SELECT * FROM dst) x) = 0
   AND (SELECT COUNT(*) FROM (SELECT * FROM dst EXCEPT ALL SELECT * FROM src) y) = 0
  THEN 'IN_SYNC' ELSE 'DRIFT'
END AS status;
```
**Explanation:** Both directions of EXCEPT ALL must produce zero leftovers for multiset equality; the CASE folds the double-diff check into a pass/fail flag for pipeline tests.

## Q98: Deduplicate a single table using UNION applied to itself (a SELECT DISTINCT alternative) — and state the caveat.

**Query:**
```sql
SELECT region, product FROM transactions
UNION
SELECT region, product FROM transactions;
```
**Alt1:**
```sql
SELECT DISTINCT region, product FROM transactions;
```
**Explanation:** The union collapses the table's rows to one per distinct combination, exactly like SELECT DISTINCT — terser as an idiom, though DISTINCT states the intent more clearly.

## Q99: "amount > 100 OR amount IS NULL" as two UNION branches — include the NULL rows that numeric comparisons skip.

**Query:**
```sql
SELECT order_id, amount FROM orders WHERE amount > 100
UNION
SELECT order_id, amount FROM orders WHERE amount IS NULL;
```
**Alt1:**
```sql
SELECT order_id, amount FROM orders WHERE amount > 100 OR amount IS NULL;
```
**Explanation:** `amount > 100` is UNKNOWN for NULLs, so the branch form adds a dedicated IS NULL scan and UNION deduplicates. Both return the same set; the two-branch shape can exploit a partial index on amount IS NULL.

## Q100: Grand finale reconciliation report (PostgreSQL): decompose curated.customers vs raw.customers into INSERT, DELETE and SAME buckets with counts, using only set operations.

**Query:**
```sql
-- PostgreSQL
WITH only_new AS (
  SELECT customer_id FROM curated.customers
  EXCEPT ALL
  SELECT customer_id FROM raw.customers
),
only_old AS (
  SELECT customer_id FROM raw.customers
  EXCEPT ALL
  SELECT customer_id FROM curated.customers
),
shared AS (
  SELECT * FROM curated.customers
  INTERSECT ALL
  SELECT * FROM raw.customers
)
SELECT 'INSERT' AS bucket, COUNT(*) AS rows FROM only_new
UNION ALL SELECT 'DELETE', COUNT(*) FROM only_old
UNION ALL SELECT 'SAME', COUNT(*) FROM shared;
```
**Explanation:** The three counts partition the multiset universe — INSERT + DELETE + SAME adds up to the source sizes, with SAME measured by INTERSECT ALL on full rows. It is the complete set-operator diff in one query: differences, direction and overlap all visible.
