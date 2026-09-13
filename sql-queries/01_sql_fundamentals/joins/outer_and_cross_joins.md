# LEFT, RIGHT, FULL and CROSS JOINs — 100 SQL Interview Q&A

## Q1: Write a query to list all customers, including those who never placed an order.
**Query:**
```sql
SELECT c.customer_id, c.name, o.order_id, o.order_date
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id;
```
**Explanation:** LEFT JOIN keeps every row from `customers`; orders columns are NULL on the right when no order matches.
**Alt1:**
```sql
SELECT c.customer_id, c.name, o.order_id, o.order_date
FROM customers c
LEFT OUTER JOIN orders o ON o.customer_id = c.customer_id;
```
`LEFT JOIN` and `LEFT OUTER JOIN` are synonymous; `OUTER` is optional.

## Q2: Write a query to show every department, even if it currently has no employees.
**Query:**
```sql
SELECT d.department_id, d.dept_name, e.employee_id, e.name AS employee_name
FROM departments d
LEFT JOIN employees e ON e.department_id = d.department_id;
```
**Explanation:** Departments without employees appear with NULL employee columns because the LEFT side wins.

## Q3: Find all customers who have placed zero orders.
**Query:**
```sql
SELECT c.customer_id, c.name
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;
```
**Explanation:** After the join, the WHERE filters to rows where the RIGHT-side key stayed NULL — the classic "anti-join".
**Alt1:**
```sql
SELECT c.customer_id, c.name
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);
```
`NOT EXISTS` is the explicit anti-join: it reads as "no order exists" instead of fabricating NULL rows.

## Q4: List all products and their category names, including products that have no category.
**Query:**
```sql
SELECT p.product_id, p.name AS product, c.name AS category
FROM products p
LEFT JOIN categories c ON c.category_id = p.category_id;
```
**Explanation:** `category` shows NULL when `p.category_id` is NULL or unmatched; LEFT JOIN guarantees every product still appears.

## Q5: Show every employee, and include a department label even for those without one.
**Query:**
```sql
SELECT e.employee_id, e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON d.department_id = e.department_id;
```
**Explanation:** NULL `dept_name` flags unassigned employees instead of dropping their rows.

## Q6: Write a query to list all authors and any books they have written, keeping authors with no books.
**Query:**
```sql
SELECT a.author_id, a.author_name, b.book_id, b.title
FROM authors a
LEFT JOIN books b ON b.author_id = a.author_id;
```
**Explanation:** LEFT JOIN preserves all authors; missing books yield NULL for the `books` columns.

## Q7: Return every category even when it has no products, listing products on the right.
**Query:**
```sql
SELECT c.category_id, c.name AS category, p.product_id, p.name AS product
FROM categories c
RIGHT JOIN products p ON p.category_id = c.category_id;
```
**Explanation:** This RIGHT JOIN (categories on the right) still emits all categories; `product` may be NULL for empty categories.
**Alt1:**
```sql
SELECT c.category_id, c.name AS category, p.product_id, p.name AS product
FROM products p
LEFT JOIN categories c ON c.category_id = p.category_id;
```
Swapping the table order converts the RIGHT JOIN into a LEFT JOIN with identical results.

## Q8: Find suppliers that currently supply nothing (orphan-supplier anti-join).
**Query:**
```sql
SELECT s.supplier_id, s.supplier_name
FROM suppliers s
LEFT JOIN product_supplier ps ON ps.supplier_id = s.supplier_id
WHERE ps.supplier_id IS NULL;
```
**Explanation:** Suppliers failing to match any link row keep NULL `ps.supplier_id`, which the WHERE excludes them from: an anti-join.

## Q9: Show every student, plus their enrolled course names, including non-enrolled students.
**Query:**
```sql
SELECT st.student_id, st.student_name, e.course_id, c.course_name
FROM students st
LEFT JOIN enrollments e ON e.student_id = st.student_id
LEFT JOIN courses c ON c.course_id = e.course_id;
```
**Explanation:** Two chained LEFT JOINs: the first preserves all students, the second preserves all enrollment rows.

## Q10: List all movies, and for each one show any ratings, keeping movies with no ratings.
**Query:**
```sql
SELECT m.movie_id, m.title, r.rating, r.review_text
FROM movies m
LEFT JOIN ratings r ON r.movie_id = m.movie_id;
```
**Explanation:** Movies never rated appear once with NULL rating/review columns.

## Q11: Find customers who placed at least one order but never wrote a review.
**Query:**
```sql
SELECT DISTINCT c.customer_id, c.name
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
LEFT JOIN reviews r ON r.order_id = o.order_id
WHERE r.review_id IS NULL;
```
**Explanation:** The plain JOIN restricts to customers with orders; the LEFT JOIN anti-test keeps those with no matching review.

## Q12: Display all branches, including branches that have recorded no transactions.
**Query:**
```sql
SELECT b.branch_id, b.branch_name, t.transaction_id, t.amount
FROM branches b
LEFT JOIN transactions t ON t.branch_id = b.branch_id;
```
**Explanation:** Branches without transactions surface with NULL `t.transaction_id` because they remain rows on the left.

## Q13: Return every blog post with its comments, not excluding posts that have zero comments.
**Query:**
```sql
SELECT p.post_id, p.title, cm.content
FROM blog_posts p
LEFT JOIN comments cm ON cm.post_id = p.post_id;
```
**Explanation:** Commentless posts produce a single row with `content` NULL rather than vanishing.

## Q14: Write a query to find rooms that have never been booked.
**Query:**
```sql
SELECT r.room_id, r.room_number
FROM rooms r
LEFT JOIN bookings b ON b.room_id = r.room_id
WHERE b.booking_id IS NULL;
```
**Explanation:** After the LEFT JOIN, `b.booking_id IS NULL` isolates rooms with no booking row — the anti-join idiom.
**Alt1:**
```sql
SELECT r.room_id, r.room_number
FROM rooms r
WHERE r.room_id NOT IN (SELECT room_id FROM bookings WHERE room_id IS NOT NULL);
```
`NOT_IN` only works if the subquery can never return NULL — one NULL poisons the entire set, so it must be filtered out.

## Q15: Show all tasks with the name of their assignee, including tasks with no assignee.
**Query:**
```sql
SELECT t.task_id, t.title, e.name AS assignee
FROM tasks t
LEFT JOIN employees e ON e.employee_id = t.assignee_id;
```
**Explanation:** Unassigned tasks remain visible with `assignee` NULL because the employee side is optional.

## Q16: List every guest and the events they registered for, keeping guests with no registrations.
**Query:**
```sql
SELECT g.guest_id, g.guest_name, e.event_id, e.event_name
FROM guests g
LEFT JOIN registrations r ON r.guest_id = g.guest_id
LEFT JOIN events e ON e.event_id = r.event_id;
```
**Explanation:** Both joins are LEFT so a guest with no registration still appears; `event_id` is NULL for them.

## Q17: Find all vehicles that have no maintenance record on file.
**Query:**
```sql
SELECT v.vehicle_id, v.license_plate
FROM vehicles v
LEFT JOIN maintenance m ON m.vehicle_id = v.vehicle_id
WHERE m.maintenance_id IS NULL;
```
**Explanation:** Vehicles with no maintenance row keep NULL `m.maintenance_id`; the WHERE drops any vehicle that did match.

## Q18: Show every store together with its stock entries, including stores with empty stock shelves.
**Query:**
```sql
SELECT s.store_id, s.store_name, st.item_id, st.quantity
FROM stores s
LEFT JOIN stock st ON st.store_id = s.store_id;
```
**Explanation:** Stores with zero stock still appear once, with NULL `item_id` and `quantity`.

## Q19: List all conference rooms and any meetings booked in them, preserving rooms with no meetings.
**Query:**
```sql
SELECT r.room_id, r.room_name, m.meeting_id, m.meeting_time
FROM conference_rooms r
LEFT JOIN meetings m ON m.room_id = r.room_id;
```
**Explanation:** Meetings columns come back NULL for rooms never booked; the rooms themselves always survive.

## Q20: Find subscribers who have never watched a single video.
**Query:**
```sql
SELECT s.subscriber_id, s.email
FROM subscribers s
LEFT JOIN watch_history w ON w.subscriber_id = s.subscriber_id
WHERE w.watch_id IS NULL;
```
**Explanation:** The anti-join keeps only subscribers whose LEFT JOINed `watch_history` produced no row.

## Q21: Return all employees even when their department lookup is missing, and fill the gap with a placeholder.
**Query:**
```sql
SELECT e.employee_id, e.name,
       COALESCE(d.dept_name, 'Unassigned') AS department
FROM employees e
LEFT JOIN departments d ON d.department_id = e.department_id;
```
**Explanation:** LEFT JOIN preserves every employee; COALESCE swaps the NULL `dept_name` for a readable placeholder.

## Q22: Write a query that returns every order, whether or not it was ever fulfilled.
**Query:**
```sql
SELECT o.order_id, o.order_date, f.fulfillment_date, f.carrier
FROM orders o
LEFT JOIN fulfillments f ON f.order_id = o.order_id;
```
**Explanation:** Unfulfilled orders keep the order columns and show NULL in the `fulfillments` side.

## Q23: List all payment methods alongside any payments using them, including never-used methods.
**Query:**
```sql
SELECT pm.payment_method_id, pm.method_name, p.payment_id, p.order_id
FROM payment_methods pm
LEFT JOIN payments p ON p.payment_method_id = pm.payment_method_id;
```
**Explanation:** Methods nobody paid with still appear; their `payments` columns are NULL.

## Q24: Find regions that produced zero sales in the current quarter.
**Query:**
```sql
SELECT rg.region_id, rg.region_name
FROM regions rg
LEFT JOIN sales s ON s.region_id = rg.region_id
    AND s.sale_date >= DATE '2026-01-01'
    AND s.sale_date < DATE '2026-04-01'
WHERE s.sale_id IS NULL;
```
**Explanation:** The quarter filter lives in the ON clause so it cannot convert the anti-join back into an inner join.

## Q25: Show every priority level and the tickets assigned to it, even empty ones.
**Query:**
```sql
SELECT p.priority_id, p.priority_level, t.ticket_id, t.subject
FROM priorities p
LEFT JOIN tickets t ON t.priority_id = p.priority_id;
```
**Explanation:** Priorities with no tickets return with NULL ticket columns; LEFT JOIN never drops the driver table.

## Q26: Write a query that counts how many employees fall into each department, including departments with zero employees.
**Query:**
```sql
SELECT d.department_id, d.dept_name, COUNT(e.employee_id) AS headcount
FROM departments d
LEFT JOIN employees e ON e.department_id = d.department_id
GROUP BY d.department_id, d.dept_name
ORDER BY d.department_id;
```
**Explanation:** COUNT on `e.employee_id` (not `e.*`) counts only matched employees, so empty departments show 0 instead of 1.
**Alt1:**
```sql
SELECT d.department_id, d.dept_name, COUNT(DISTINCT e.employee_id) AS headcount
FROM departments d
LEFT JOIN employees e ON e.department_id = d.department_id
GROUP BY d.department_id, d.dept_name;
```
`COUNT(DISTINCT ...)` guards against a many-to-many join inflating the headcount.

## Q27: Write a query to compare two runs of a nightly process and show which record IDs exist only on one side.
**Query:**
```sql
-- PostgreSQL / SQL Server / Oracle (FULL OUTER JOIN)
SELECT COALESCE(t1.record_id, t2.record_id) AS record_id,
       t1.value AS run1_value,
       t2.value AS run2_value
FROM run1 t1
FULL OUTER JOIN run2 t2 ON t2.record_id = t1.record_id;
```
**Explanation:** FULL OUTER JOIN keeps unmatched rows from both tables; the source is identifiable by which side is NULL.

## Q28: Emulate a FULL OUTER JOIN in MySQL, which lacks the syntax.
**Query:**
```sql
-- MySQL
SELECT COALESCE(t1.record_id, t2.record_id) AS record_id,
       t1.value AS run1_value, t2.value AS run2_value
FROM run1 t1
LEFT JOIN run2 t2 ON t2.record_id = t1.record_id
UNION
SELECT t2.record_id, t1.value, t2.value
FROM run2 t2
LEFT JOIN run1 t1 ON t1.record_id = t2.record_id
WHERE t1.record_id IS NULL;
```
**Explanation:** The LEFT JOIN covers run1-side rows, the UNION leg's second LEFT JOIN adds only run2 rows that run1 missed.

## Q29: Show all books and all reviews such that a book without reviews and a review without a book both appear.
**Query:**
```sql
-- PostgreSQL
SELECT b.book_id, b.title, r.review_id, r.rating
FROM books b
FULL OUTER JOIN reviews r ON r.book_id = b.book_id;
```
**Explanation:** Orphan reviews (book deleted) and reviewless books each survive; the other side is NULL.
**Alt1:**
```sql
-- MySQL (no FULL OUTER JOIN)
SELECT COALESCE(b.book_id, r.book_id) AS book_id, b.title, r.review_id, r.rating
FROM books b
LEFT JOIN reviews r ON r.book_id = b.book_id
UNION ALL
SELECT r.book_id, NULL, r.review_id, r.rating
FROM reviews r
LEFT JOIN books b ON b.book_id = r.book_id
WHERE b.book_id IS NULL;
```
One LEFT-JOIN leg plus a right-only remainder leg reproduces FULL OUTER JOIN where the dialect lacks the keyword.

## Q30: Write a query that lists every possible (shirt_size, shirt_color) combination for an apparel catalog.
**Query:**
```sql
SELECT sz.size_name, c.color_name
FROM sizes sz
CROSS JOIN colors c;
```
**Explanation:** CROSS JOIN produces a Cartesian product: every size paired with every color, no ON condition.

**Alt1:**
```sql
SELECT sz.size_name, c.color_name
FROM sizes sz
JOIN colors c ON 1 = 1;
```
`JOIN ... ON 1 = 1` is an always-true predicate that yields the same Cartesian product.

## Q31: Generate a complete matrix of every department paired with every work shift for a staffing plan.
**Query:**
```sql
SELECT d.dept_name, sh.shift_name
FROM departments d
CROSS JOIN shifts sh;
```
**Explanation:** CROSS JOIN pairs each department with every shift, producing a full schedule grid with no join key.

## Q32: Write a query to produce every combination of a product and its possible prices before deciding which prices to list.
**Query:**
```sql
SELECT p.product_id, price.tier, price.amount
FROM products p
CROSS JOIN (SELECT 'List' AS tier, 1.00 AS amount
            UNION ALL SELECT 'Member', 0.90
            UNION ALL SELECT 'Bulk',   0.75) price;
```
**Explanation:** CROSS JOIN with an inline price table expands each product into its pricing variants.

## Q33: For a delivery grid, generate all (zone, day) combinations so every zone has a row for every day of the week.
**Query:**
```sql
SELECT z.zone_name, d.day_name
FROM delivery_zones z
CROSS JOIN (SELECT 'Monday' AS day_name UNION ALL SELECT 'Tuesday'
            UNION ALL SELECT 'Wednesday' UNION ALL SELECT 'Thursday'
            UNION ALL SELECT 'Friday' UNION ALL SELECT 'Saturday'
            UNION ALL SELECT 'Sunday') d;
```
**Explanation:** CROSS JOIN between zones and the seven literal days yields a complete service matrix.

## Q34: Generate a row for each of the first five order numbers so later joins can expand against it.
**Query:**
```sql
SELECT n.n
FROM (SELECT 1 AS n UNION ALL SELECT 2 UNION ALL SELECT 3
      UNION ALL SELECT 4 UNION ALL SELECT 5) n;
```
**Explanation:** A UNION ALL literal sequence is a portable generator; CROSS JOINing it later inflates rows.

**Alt1:**
```sql
-- PostgreSQL
SELECT gs AS n FROM generate_series(1, 5) gs;
```
`generate_series` is PostgreSQL's native row generator.

**Alt2:**
```sql
-- SQL Server / Oracle
SELECT value AS n FROM STRING_SPLIT(REPLICATE('a,', 5), ',');  -- SQL Server
```
A dialect-native trick: 5 tokens → 5 rows; Oracle can do the same with `REGEXP_SUBSTR` on a repeating string.

## Q35: Write a query to expand each bulk invoice line into as many rows as the paid installment count.
**Query:**
```sql
-- PostgreSQL
SELECT inv.invoice_id, inst.n AS installment_no
FROM invoices inv
CROSS JOIN generate_series(1, inv.installments) AS inst;
```
**Explanation:** `generate_series` bounded by a per-row column emits one output row per installment per invoice.

## Q36: List every customer and, for any that lack a profile, show the customer anyway with a placeholder.
**Query:**
```sql
SELECT c.customer_id, c.name,
       COALESCE(p.phone, 'No phone on file') AS contact
FROM customers c
LEFT JOIN customer_profiles p ON p.customer_id = c.customer_id;
```
**Explanation:** The LEFT JOIN keeps all customers; COALESCE converts the NULL right-side column into text.

## Q37: Show all products and their brands, and for products with no brand display 'Unknown Brand'.
**Query:**
```sql
SELECT p.product_id, p.product_name,
       COALESCE(b.brand_name, 'Unknown Brand') AS brand
FROM products p
LEFT JOIN brands b ON b.brand_id = p.brand_id;
```
**Explanation:** COALESCE returns the first non-NULL argument, so unmatched brand lookups become the literal string.
**Alt1:**
```sql
SELECT p.product_id, p.product_name,
       CASE WHEN b.brand_name IS NULL THEN 'Unknown Brand'
            ELSE b.brand_name END AS brand
FROM products p
LEFT JOIN brands b ON b.brand_id = p.brand_id;
```
`CASE` is the verbose twin of COALESCE; use it when the NULL fallback has to vary by column.

## Q38: Write a query that demonstrates how filtering the RIGHT table in WHERE silently turns a LEFT JOIN into an INNER JOIN.
**Query:**
```sql
SELECT c.customer_id, o.order_id
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_date >= '2026-01-01';
```
**Explanation:** The WHERE on the right table discards NULL order rows, so customers without qualifying orders vanish — INNER semantics.

## Q39: Rewrite the previous query so that ALL customers are kept, filtering orders only.
**Query:**
```sql
SELECT c.customer_id, o.order_id
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
    AND o.order_date >= '2026-01-01';
```
**Explanation:** Moving the date test into the ON clause preserves the NULL row for no-order customers; WHERE would have destroyed it.

## Q40: Show all departments and count only employees hired after 2024, but keep departments with zero hires.
**Query:**
```sql
SELECT d.department_id, d.dept_name, COUNT(e.employee_id) AS hires_after_2024
FROM departments d
LEFT JOIN employees e ON e.department_id = d.department_id
    AND e.hire_date > '2024-12-31'
GROUP BY d.department_id, d.dept_name;
```
**Explanation:** The hire-date predicate inside ON lets older employees fail the join without deleting their department row.

## Q41: For a matchmaking report, list all men and women such that every man appears even with no match, and every woman appears even with no match.
**Query:**
```sql
-- SQL Server (FULL OUTER JOIN)
SELECT COALESCE(m.person_id, w.person_id) AS person_id,
       m.name AS male, w.name AS female, r.score
FROM men m
FULL OUTER JOIN women w ON w.person_id = m.person_id
LEFT JOIN matches r ON r.male_id = m.person_id AND r.female_id = w.person_id;
```
**Explanation:** The FULL OUTER JOIN keeps everyone; the LEFT JOIN to matches adds a score only where a match exists.

## Q42: Generate all (employee, skill) pairs so the training matrix includes every possible assignment.
**Query:**
```sql
SELECT e.employee_id, s.skill_name, e.level
FROM employees e
CROSS JOIN skills s;
```
**Explanation:** Cartesian product of employees and skills; the ad-hoc `level` column (unused) hints at filling gaps later.

## Q43: Write a query to produce the multiplication table (1..5) x (1..5).
**Query:**
```sql
SELECT a.n AS a, b.n AS b, a.n * b.n AS product
FROM (SELECT 1 AS n UNION ALL SELECT 2 UNION ALL SELECT 3
      UNION ALL SELECT 4 UNION ALL SELECT 5) a
CROSS JOIN (SELECT 1 AS n UNION ALL SELECT 2 UNION ALL SELECT 3
            UNION ALL SELECT 4 UNION ALL SELECT 5) b;
```
**Explanation:** Two literal number generators crossed produce the 25-cell multiplication grid.

## Q44: Emulate a RIGHT JOIN using a LEFT JOIN by swapping the table roles.
**Query:**
```sql
SELECT b.title, a.author_name
FROM books b
RIGHT JOIN authors a ON a.author_id = b.author_id;
```
**Explanation:** RIGHT JOIN keeps all authors; rewriting with tables swapped as `authors LEFT JOIN books` returns identical rows.
**Alt1:**
```sql
SELECT b.title, a.author_name
FROM authors a
LEFT JOIN books b ON b.author_id = a.author_id;
```
Same result — RIGHT JOIN is syntactic sugar for a LEFT JOIN with the operands reversed.

## Q45: Show every supplier with all the parts stocked, and also show parts that no supplier stocks.
**Query:**
```sql
-- PostgreSQL
SELECT COALESCE(sp.supplier_id, p.part_id) AS id,
       sp.supplier_name, p.part_name
FROM suppliers sp
FULL OUTER JOIN parts p ON p.supplier_id = sp.supplier_id;
```
**Explanation:** Null on either side marks rows unmatched on the other table; COALESCE normalizes the identifier for display.

## Q46: Produce every possible pairing of teams for a round-robin (each team plays each other once).
**Query:**
```sql
SELECT a.team_name AS home, b.team_name AS away
FROM teams a
CROSS JOIN teams b
WHERE a.team_id < b.team_id;
```
**Explanation:** CROSS JOIN gives all ordered pairs; `a.team_id < b.team_id` keeps each unordered pair once, avoiding byes.
**Alt1:**
```sql
SELECT a.team_name AS home, b.team_name AS away
FROM teams a
JOIN teams b ON a.team_id < b.team_id;
```
The inequality predicate on the JOIN produces the same set, skipping duplicates and self-pairs.

## Q47: Find every city pair (both directions) that could be a flight route.
**Query:**
```sql
SELECT a.city AS origin, b.city AS destination
FROM cities a
CROSS JOIN cities b
WHERE a.city <> b.city;
```
**Explanation:** The `<>` filter removes zero-length routes; both directions remain, so the matrix is symmetric.

## Q48: Write a query to give every employee three slack-budget rows — normal, medium, high.
**Query:**
```sql
SELECT e.employee_id, b.budget_name, b.amount
FROM employees e
CROSS JOIN (SELECT 'Normal' AS budget_name, 100 AS amount
            UNION ALL SELECT 'Medium', 250
            UNION ALL SELECT 'High', 500) b;
```
**Explanation:** CROSS JOIN against an inline three-row budget table triples each employee row.

## Q49: Return all insurance policies and their claims, preserving policies that have never been claimed.
**Query:**
```sql
SELECT p.policy_id, p.policy_holder, c.claim_id, c.claim_amount
FROM policies p
LEFT JOIN claims c ON c.policy_id = p.policy_id;
```
**Explanation:** Claimless policies persist with NULL claim columns because the LEFT side dominates.
**Alt1:**
```sql
SELECT p.policy_id, p.policy_holder, c.claim_id, c.claim_amount
FROM claims c
RIGHT JOIN policies p ON p.policy_id = c.policy_id;
```
Flipping the table order turns the RIGHT JOIN into the same survivor set as the LEFT version — SQL's symmetric outer join.

## Q50: Show every class and its enrolled students alongside classes nobody enrolled in.
**Query:**
```sql
SELECT cl.class_id, cl.class_name, en.student_id, st.student_name
FROM classes cl
LEFT JOIN enrollments en ON en.class_id = cl.class_id
LEFT JOIN students st ON st.student_id = en.student_id;
```
**Explanation:** The first LEFT JOIN survives empty classes; the second survives any malformed enrollment rows.

## Q51: Write a query that merges the employee rosters of two offices, showing everyone even if only one office knows about them.
**Query:**
```sql
-- SQL Server
SELECT COALESCE(a.emp_id, b.emp_id) AS emp_id,
       COALESCE(a.name, b.name) AS name,
       a.office_ticket_count, b.remote_ticket_count
FROM office_a a
FULL OUTER JOIN office_b b ON b.emp_id = a.emp_id;
```
**Explanation:** Both unmatched and matched employees survive; COALESCE generates a unified key and name.

## Q52: Generate a full calendar cover: every product for every month of 2026, so later LEFT JOINs can fill in actuals.
**Query:**
```sql
SELECT p.product_id, ym.year_month
FROM products p
CROSS JOIN (SELECT TO_CHAR(mn, 'YYYY-MM') AS year_month
            FROM (SELECT DATE '2026-01-01' + INTERVAL '1' MONTH * (LEVEL - 1) AS mn
                  FROM dual CONNECT BY LEVEL <= 12) x) ym;
```
**Explanation:** Oracle's `CONNECT BY` fabricates 12 months; CROSS JOIN binds each to every product, forming the base matrix.

**Alt1:**
```sql
-- MySQL
SELECT p.product_id, ym.year_month
FROM products p
CROSS JOIN (SELECT DATE_FORMAT(date_added, '%Y-%m') AS year_month
            FROM (SELECT '2026-01-01' + INTERVAL seq MONTH AS date_added
                  FROM seq_0_to_11) dates) ym;
```
MySQL 8 stores `seq_0_to_11`; the INTERVAL ladder yields January through December for each product.

## Q53: Write a query that generates every slot (hour) of the working day x every consult room.
**Query:**
```sql
SELECT hr.slot_start, rm.room_id
FROM (SELECT TIMESTAMP '2026-01-05 09:00:00' + INTERVAL '1' HOUR * (lvl - 1) AS slot_start
      FROM (SELECT LEVEL AS lvl FROM dual CONNECT BY LEVEL <= 8) x) hr
CROSS JOIN rooms rm;
```
**Explanation:** Oracle's CONNECT BY emits 9 AM to 4 PM; CROSS JOIN against rooms builds the full booking grid.

## Q54: Show every campaign and its clicks, and also surface orphan clicks whose campaign was deleted.
**Query:**
```sql
-- PostgreSQL
SELECT COALESCE(c.campaign_id, cl.campaign_id) AS campaign_id,
       c.campaign_name, cl.click_id, cl.clicked_at
FROM campaigns c
FULL OUTER JOIN clicks cl ON cl.campaign_id = c.campaign_id;
```
**Explanation:** The FULL OUTER JOIN keeps both sides, revealing orphan clicks as rows with NULL campaign_name.

## Q55: List all customers and the count of their 2026 orders, but keep customers with none and show 0.
**Query:**
```sql
SELECT c.customer_id, c.name,
       COUNT(o.order_id) AS orders_2026
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
    AND o.order_date >= DATE '2026-01-01'
    AND o.order_date <  DATE '2027-01-01'
GROUP BY c.customer_id, c.name;
```
**Explanation:** The 2026 filter sits in ON so matches are merely skipped, not rows dropped; COUNT gives 0 for NULL groups.

## Q56: Write a query to show each airport's outbound routes, including airports with no scheduled routes.
**Query:**
```sql
SELECT ap.airport_id, ap.iata_code, rt.destination_iata
FROM airports ap
LEFT JOIN routes rt ON rt.origin_iata = ap.iata_code;
```
**Explanation:** Airports without routes surface with NULL destination; LEFT JOIN preserves the full airport list.

## Q57: Emulate a FULL OUTER JOIN in SQLite-style tooling by combining LEFT JOIN and RIGHT JOIN results.
**Query:**
```sql
-- SQLite / MySQL (no FULL OUTER JOIN)
SELECT a.id, b.id AS bid
FROM a
LEFT JOIN b ON b.id = a.id
UNION
SELECT b.id, b.id
FROM b
LEFT JOIN a ON a.id = b.id
WHERE a.id IS NULL;
```
**Explanation:** The second leg contributes only b-side rows absent from a, so UNION merges both unmatched populations.

## Q58: Return all articles and all tags, tagging gaps included on both sides of the relationship.
**Query:**
```sql
SELECT COALESCE(ar.article_id, tg.article_id) AS article_id,
       ar.title, tg.tag_name
FROM articles ar
FULL OUTER JOIN article_tags tg ON tg.article_id = ar.article_id;
```
**Explanation:** Articles with no tags and tags pointing to deleted articles both survive as NULL-padded rows.

## Q59: For a sales dashboard, generate all (region x quarter) combos so empty cells can be charted as zero.
**Query:**
```sql
SELECT rg.region_id, q.qtr,
       COUNT(s.sale_id) AS sales_count
FROM regions rg
CROSS JOIN (SELECT '2026Q1' AS qtr UNION ALL SELECT '2026Q2'
            UNION ALL SELECT '2026Q3' UNION ALL SELECT '2026Q4') q
LEFT JOIN sales s ON s.region_id = rg.region_id
    AND s.sale_date >= DATE '2026-01-01' AND s.sale_date < DATE '2027-01-01'
    AND (q.qtr = '2026Q1' AND EXTRACT(QUARTER FROM s.sale_date) = 1
      OR q.qtr = '2026Q2' AND EXTRACT(QUARTER FROM s.sale_date) = 2
      OR q.qtr = '2026Q3' AND EXTRACT(QUARTER FROM s.sale_date) = 3
      OR q.qtr = '2026Q4' AND EXTRACT(QUARTER FROM s.sale_date) = 4)
GROUP BY rg.region_id, q.qtr;
```
**Explanation:** CROSS JOIN seeds all region-quarter cells; LEFT JOIN attaches actuals, and COUNT on the sales key yields 0 for empty cells.

**Alt1:**
```sql
-- PostgreSQL
SELECT rg.region_id, q.qtr, COUNT(s.sale_id) AS sales_count
FROM regions rg
CROSS JOIN (VALUES ('2026Q1'), ('2026Q2'), ('2026Q3'), ('2026Q4')) AS q(qtr)
LEFT JOIN sales s ON s.region_id = rg.region_id
    AND to_char(s.sale_date, 'YYYY"Q"Q') = q.qtr
GROUP BY rg.region_id, q.qtr;
```
`VALUES` rows simplify the quarter list, and `to_char` formats the join predicate portably.

## Q60: Write a query to diff expected vs actual delivery rows, exposing rows only in one system.
**Query:**
```sql
-- SQL Server
SELECT COALESCE(e.delivery_id, a.delivery_id) AS delivery_id,
       e.expected_eta, a.actual_eta
FROM expected_deliveries e
FULL OUTER JOIN actual_deliveries a ON a.delivery_id = e.delivery_id;
```
**Explanation:** NULL on either side flags rows missing from the other system, so discrepancies are greppable.

## Q61: Generate a row for every combination of a quiz's questions and answer options.
**Query:**
```sql
SELECT q.question_id, o.option_id, o.option_text
FROM questions q
CROSS JOIN options o;
```
**Explanation:** Even if some options belong to other questions, CROSS JOIN naively pairs all with all — intentional for seeding.

**Alt1:**
```sql
SELECT q.question_id, o.option_id, o.option_text
FROM questions q
JOIN options o ON o.question_id = q.question_id;
```
A keyed JOIN keeps only legitimate pairs; CROSS JOIN is only correct when the relationship is truly many-to-many.

## Q62: Show each employee's manager name, employees with no manager still listed.
**Query:**
```sql
SELECT e.employee_id, e.name, m.name AS manager_name
FROM employees e
LEFT JOIN employees m ON m.employee_id = e.manager_id;
```
**Explanation:** Self-LEFT-JOIN aligns each row with its own manager row; top-level staff keep NULL manager.
**Alt1:**
```sql
SELECT e.employee_id, e.name,
       (SELECT m.name FROM employees m WHERE m.employee_id = e.manager_id) AS manager_name
FROM employees e;
```
A correlated subquery performs the same lookup; the LEFT self-join wins when manager attributes are needed as columns.

## Q63: Write a query that returns all orders joined to shipment details, flagging orders never shipped.
**Query:**
```sql
SELECT o.order_id, sh.shipment_id, sh.tracking_no
FROM orders o
LEFT JOIN shipments sh ON sh.order_id = o.order_id;
```
**Explanation:** Orders lacking shipments keep NULL tracking columns; LEFT JOIN retains the entire order set.

## Q64: Build a routing matrix pairing every warehouse with every route, then keep only feasible pairs via a second table.
**Query:**
```sql
SELECT w.warehouse_id, r.route_id
FROM warehouses w
CROSS JOIN routes r
JOIN feasibility f ON f.warehouse_id = w.warehouse_id
    AND f.route_id = r.route_id
    AND f.is_feasible = 1;
```
**Explanation:** CROSS JOIN first builds all pairs; the subsequent keyed JOIN prunes to just the feasible subset.

## Q65: Find pairs of employees who share an overlapping shift window, showing both directions.
**Query:**
```sql
SELECT a.employee_id AS e1, b.employee_id AS e2
FROM employees a
CROSS JOIN employees b
WHERE a.employee_id < b.employee_id
  AND EXISTS (SELECT 1 FROM shifts s1
              JOIN shifts s2 ON s1.employee_id = a.employee_id
                            AND s2.employee_id = b.employee_id
                            AND s1.start_time < s2.end_time
                            AND s2.start_time < s1.end_time);
```
**Explanation:** The deck is the unordered pair; EXISTS filters to pairs sharing at least one temporally overlapping shift.

## Q66: Show every product and for each the count of returns, including products with no returns (count 0).
**Query:**
```sql
SELECT p.product_id, p.name, COUNT(CASE WHEN r.return_date IS NOT NULL THEN 1 END) AS return_count
FROM products p
LEFT JOIN returns r ON r.product_id = p.product_id
GROUP BY p.product_id, p.name;
```
**Explanation:** Counting a CASE that maps NULL to NULL keeps unmatched products at 0; LEFT JOIN preserves them.

**Alt1:**
```sql
SELECT p.product_id, p.name, COUNT(r.return_id) AS return_count
FROM products p
LEFT JOIN returns r ON r.product_id = p.product_id
GROUP BY p.product_id, p.name;
```
`COUNT(r.return_id)` ignores NULL return keys directly, giving the same 0-safe count without CASE.

## Q67: Merge two backup tables (full and incremental) so records present in either surface once.
**Query:**
```sql
-- PostgreSQL
SELECT COALESCE(f.id, i.id) AS id
FROM full_backup f
FULL OUTER JOIN incremental_backup i ON i.id = f.id;
```
**Explanation:** FULL OUTER JOIN unifies both row sets; rows appearing in both collapse onto one line with no duplication.

## Q68: Write a query to tag unmatched rows from both sides with the name of the source table.
**Query:**
```sql
SELECT COALESCE(lc.person_id, rc.person_id) AS person_id,
       lc.name, rc.name AS alt_name,
       CASE WHEN lc.person_id IS NULL THEN 'RIGHT_ONLY'
            WHEN rc.person_id IS NULL THEN 'LEFT_ONLY'
            ELSE 'BOTH' END AS source
FROM left_table lc
FULL OUTER JOIN right_table rc ON rc.person_id = lc.person_id;
```
**Explanation:** The CASE reads which side went NULL, yielding a source tag without losing any row.

## Q69: Generate every (ad, placement) slot so the ad server can pre-seed the inventory matrix.
**Query:**
```sql
SELECT a.ad_id, pl.placement_name
FROM ads a
CROSS JOIN placements pl;
```
**Explanation:** Pure Cartesian product; every ad is assigned every placement as an available scheduling slot.

## Q70: Show the union of two departments' staff—those in both appear once, those in one appear with a NULL gap.
**Query:**
```sql
-- SQL Server
SELECT COALESCE(d1.emp_id, d2.emp_id) AS emp_id,
       d1.name AS sales_name, d2.name AS support_name
FROM sales_staff d1
FULL OUTER JOIN support_staff d2 ON d2.emp_id = d1.emp_id;
```
**Explanation:** Both-side matches merge; single-side staff carry NULL in the other branch — a readable person-by-person diff.

## Q71: Write a query that lists every possible product-feature pairing for the configurator.
**Query:**
```sql
SELECT p.product_id, p.product_name, f.feature_id, f.feature_name
FROM products p
CROSS JOIN features f;
```
**Explanation:** Combinatorial expansion: each of N products meets each of M features regardless of applicability.

## Q72: For an energy meter, expand each annual contract into rows for every billing month.
**Query:**
```sql
-- PostgreSQL
SELECT ct.contract_id, to_char(m, 'YYYY-MM') AS bill_month
FROM contracts ct
CROSS JOIN generate_series(
    date_trunc('month', ct.start_date),
    date_trunc('month', ct.end_date),
    interval '1 month') m;
```
**Explanation:** `generate_series` with per-row bounds stretches each contract into one row per month from start to end.

## Q73: List each patient's most recent secondary doctor, and show patients who have no secondary link yet.
**Query:**
```sql
SELECT p.patient_id, p.patient_name, d.doctor_name
FROM patients p
LEFT JOIN assignments a ON a.patient_id = p.patient_id AND a.role = 'secondary'
LEFT JOIN doctors d ON d.doctor_id = a.doctor_id;
```
**Explanation:** Joining the `assignments` bridge as LEFT keeps role-less patients; the doctor hop is also LEFT so no row drops.

## Q74: Show all ingredients and all dishes such that ingredients never used still appear.
**Query:**
```sql
SELECT i.ingredient_id, i.ingredient_name, d.dish_name
FROM ingredients i
LEFT JOIN recipe_ingredients ri ON ri.ingredient_id = i.ingredient_id
LEFT JOIN dishes d ON d.dish_id = ri.dish_id;
```
**Explanation:** The chain keeps unused ingredients visible; the second link simply fills dish names when a usage exists.

## Q75: Write a query that returns every match in a chess tournament where both players appear, even if only one played.
**Query:**
```sql
SELECT COALESCE(w.player_id, bl.player_id) AS player_id,
       w.name AS white_name, bl.name AS black_name, m.result
FROM players w
FULL OUTER JOIN players bl ON bl.player_id = w.player_id
LEFT JOIN matches m ON m.white_id = w.player_id AND m.black_id = bl.player_id;
```
**Explanation:** FULL OUTER JOIN preserves all roster rows; the match LEFT JOIN adds the result only to genuine pairings.

## Q76: Write a MySQL query that emulates the FULL OUTER JOIN semantics precisely, preserving NULL groups on both sides.
**Query:**
```sql
-- MySQL
SELECT COALESCE(a.id, b.id) AS id,
       a.val AS left_val, b.val AS right_val
FROM table_a a
LEFT JOIN table_b b ON b.id = a.id
UNION ALL
SELECT b.id, a.val, b.val
FROM table_b b
LEFT JOIN table_a a ON a.id = b.id
WHERE a.id IS NULL;
```
**Explanation:** The first leg emits all A rows (even unmatched); the UNION ALL leg emits only B-only rows, skipping the overlap A already produced.

**Alt1:**
```sql
-- MySQL
SELECT id, MAX(CASE WHEN src = 1 THEN val END) AS left_val,
       MAX(CASE WHEN src = 2 THEN val END) AS right_val
FROM (SELECT id, val, 1 AS src FROM table_a
      UNION ALL
      SELECT id, val, 2 FROM table_b) u
GROUP BY id;
```
Tag-and-merge: UNION ALL both sides, then collapse by id — an aggregate emulation with identical unmatched coverage.

## Q77: Write a query to generate all possible (permission x role) pairs to pre-seed a new RBAC matrix.
**Query:**
```sql
SELECT perm.permission_code, rol.role_code
FROM permissions perm
CROSS JOIN roles rol;
```
**Explanation:** Each permission meets every role; admins later delete or keep pairs rather than inserting them.

## Q78: Expand a single summary row (min_zoom..max_zoom) into one row per integer zoom level.
**Query:**
```sql
-- PostgreSQL
SELECT t.tile_set, z.zoom_level
FROM tile_sets t
CROSS JOIN generate_series(t.min_zoom, t.max_zoom) AS z(zoom_level);
```
**Explanation:** The series bounds come from columns, so one summary row fans out into N integer rows.

## Q79: Show both matched and unmatched customers AND orders in a single query with a source label.
**Query:**
```sql
SELECT COALESCE(c.customer_id, o.customer_id) AS customer_id,
       c.name, o.order_id,
       CASE WHEN o.order_id IS NULL THEN 'NO_ORDERS'
            WHEN c.customer_id IS NULL THEN 'ORPHAN_ORDER'
            ELSE 'MATCHED' END AS status
FROM customers c
FULL OUTER JOIN orders o ON o.customer_id = c.customer_id;
```
**Explanation:** The outer join free-for-all exposes every state, and the CASE tag makes each NULL group explicit.
**Alt1:**
```sql
-- MySQL
SELECT c.customer_id, c.name, o.order_id, 'NO_ORDERS' AS status
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL
UNION ALL
SELECT o.customer_id, NULL, o.order_id, 'ORPHAN_ORDER' AS status
FROM orders o
LEFT JOIN customers c ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL;
```
Splitting the unmatched populations into two anti-join legs is the MySQL idiom when a source column isn't wanted.

## Q80: Write a query that finds orphaned order_details (details whose order header was deleted).
**Query:**
```sql
SELECT od.order_detail_id, od.order_id
FROM order_details od
LEFT JOIN orders o ON o.order_id = od.order_id
WHERE o.order_id IS NULL;
```
**Explanation:** Anti-join via LEFT JOIN: details whose header lookup returns NULL are the orphans heading an integrity fix.

## Q81: List every physician and the same-day patients they saw, keeping physicians with no same-day visits.
**Query:**
```sql
SELECT phy.physician_id, phy.name, ap.patient_id
FROM physicians phy
LEFT JOIN appointments ap ON ap.physician_id = phy.physician_id
    AND ap.appointment_date = CURRENT_DATE;
```
**Explanation:** The CURRENT_DATE test inside ON excludes older appointments without erasing the physician rows.

**Alt1:**
```sql
SELECT phy.physician_id, phy.name, ap.patient_id
FROM physicians phy
LEFT JOIN appointments ap ON ap.physician_id = phy.physician_id
WHERE ap.appointment_date = CURRENT_DATE OR ap.appointment_date IS NULL;
```
The explicit `IS NULL` in WHERE re-admits the unmatched rows the date filter would otherwise have killed.

## Q82: Cross every student with every advisor to identify who could advise whom, prior to matching.
**Query:**
```sql
SELECT st.student_id, ad.advisor_id
FROM students st
CROSS JOIN advisors ad;
```
**Explanation:** Full candidate pool; later business rules (FieldDistance, capacity) prune it without touching this join.

## Q83: Write a MySQL query to show every employee with a budget row, or a budget row with no owner, both labeled.
**Query:**
```sql
-- MySQL
SELECT e.emp_id, e.emp_name, b.budget_id
FROM employees e
LEFT JOIN budgets b ON b.owner_id = e.emp_id
UNION ALL
SELECT b.owner_id, NULL, b.budget_id
FROM budgets b
LEFT JOIN employees e ON e.emp_id = b.owner_id
WHERE e.emp_id IS NULL;
```
**Explanation:** Standard FULL emulation: LEFT mix plus the RIGHT-only remainder appended, NULLs preserved for orphan budgets.

## Q84: Produce every (route, vehicle) slot used to pre-assign a daily fleet schedule.
**Query:**
```sql
SELECT r.route_id, v.vehicle_id
FROM routes r
CROSS JOIN vehicles v;
```
**Explanation:** Cartesian fleet matrix; dispatchers then filter to capacity-compatible slots.

## Q85: Show every warehouse and the stock count for one SKU, warehouses without the SKU shown with 0.
**Query:**
```sql
SELECT w.warehouse_id, w.name, COUNT(i.inventory_id) AS sku_on_hand
FROM warehouses w
LEFT JOIN inventory i ON i.warehouse_id = w.warehouse_id
    AND i.sku = 'SKU-1001'
GROUP BY w.warehouse_id, w.name;
```
**Explanation:** The SKU predicate in ON lets other-SKU stocks simply not match; each warehouse still returns, NULL-counted as 0.

## Q86: Write a query that merges location data from two sources when either source is the only one that knows the location.
**Query:**
```sql
-- PostgreSQL
SELECT COALESCE(s1.loc_id, s2.loc_id) AS loc_id,
       s1.address AS source1_address, s2.address AS source2_address
FROM locations_s1 s1
FULL OUTER JOIN locations_s2 s2 ON s2.loc_id = s1.loc_id;
```
**Explanation:** One source's exclusive rows still appear; the other columns read NULL, showing exactly where data is missing.

## Q87: Generate a date x department matrix and LEFT JOIN the daily OT hours so every cell exists.
**Query:**
```sql
-- PostgreSQL
SELECT d.department_id, dt.day,
       COALESCE(ot.hours, 0) AS overtime_hours
FROM departments d
CROSS JOIN (SELECT generate_series(DATE '2026-03-01', DATE '2026-03-07',
                                   interval '1 day')::date AS day) dt
LEFT JOIN overtime ot ON ot.department_id = d.department_id
    AND ot.work_date = dt.day;
```
**Explanation:** CROSS JOIN seeds all 7-day x department cells; the LEFT JOIN attaches hours, COALESCE zero-fills gaps.

## Q88: Show all categories and every product in each, where a product missing its category still appears (with NULL category).
**Query:**
```sql
SELECT c.name AS category, p.product_name
FROM products p
LEFT JOIN categories c ON c.category_id = p.category_id;
```
**Explanation:** Swapping the narrative to product-first proves LEFT JOIN results are order-sensitive only in column layout.

**Alt1:**
```sql
SELECT c.name AS category, p.product_name
FROM categories c
RIGHT JOIN products p ON p.category_id = c.category_id;
```
RIGHT JOIN keeps products as the survivor set — the same rows, mirroring the LEFT formulation.

## Q89: Create a matrix pairing each logged-in user with each message template for a bulk-campaign dry run.
**Query:**
```sql
SELECT u.user_id, t.template_id
FROM users u
CROSS JOIN message_templates t;
```
**Explanation:** Every user meets every template; a dry run then previews NxM combinations before any sending.

## Q90: Write a query to list family members and every household plus orphaned household records.
**Query:**
```sql
SELECT COALESCE(fm.member_id, hh.household_id) AS id,
       fm.member_name, hh.address
FROM family_members fm
FULL OUTER JOIN households hh ON hh.head_member_id = fm.member_id;
```
**Explanation:** Members without a household they head, and households with no head member, all remain visible.

## Q91: Show every country and the sports it medals in, plus sports a country has never medalled in from the sports master.
**Query:**
```sql
SELECT DISTINCT c.country_id, s.sport_name, m.medal_type
FROM countries c
CROSS JOIN sports s
LEFT JOIN medals m ON m.country_id = c.country_id
    AND m.sport_id = s.sport_id;
```
**Explanation:** CROSS JOIN pre-seeds all country-sport cells; the LEFT JOIN attaches medals, DISTINCT removes duplicate medal rows per cell.

## Q92: Emulate FULL OUTER JOIN in MySQL comparing three columns, and tag the source of each row.
**Query:**
```sql
-- MySQL
SELECT COALESCE(x.id, y.id) AS id,
       x.a, x.b, x.c, y.p, y.q, y.r,
       CASE WHEN x.id IS NULL THEN 'Y_ONLY'
            WHEN y.id IS NULL THEN 'X_ONLY'
            ELSE 'MATCH' END AS src
FROM table_x x
LEFT JOIN table_y y ON y.id = x.id
UNION ALL
SELECT y.id, x.a, x.b, x.c, y.p, y.q, y.r, 'Y_ONLY'
FROM table_y y
LEFT JOIN table_x x ON x.id = y.id
WHERE x.id IS NULL;
```
**Explanation:** The composite test is trivial per-key; the UNION leg restricts to Y-exclusive keys so no row double-counts.

**Alt1:**
```sql
-- MySQL
SELECT x.id AS left_id, y.id AS right_id, x.a, y.p
FROM table_x x
FULL JOIN table_y y ON y.id = x.id;
```
MySQL 8.0.31+ actually accepts `FULL JOIN`; use the UNION approach if your MySQL build rejects it.

## Q93: For a hiring pipeline, show every opening and the candidates who applied, including unfilled openings.
**Query:**
```sql
SELECT op.opening_id, op.title, ap.candidate_id, ap.applied_on
FROM openings op
LEFT JOIN applications ap ON ap.opening_id = op.opening_id;
```
**Explanation:** Unfilled openings surface with NULL candidate columns; LEFT JOIN does not require any application to exist.

## Q94: Generate all ordered pairs of teammates for a pairing tournament, excluding a team playing itself.
**Query:**
```sql
SELECT a.team_id AS team_a, b.team_id AS team_b
FROM teams a
CROSS JOIN teams b
WHERE a.team_id <> b.team_id;
```
**Explanation:** Cartesian output retains both directions; the `<>` test alone removes the self-pair diagonals.

## Q95: Find inventory rows whose source-of-truth store lookup fails, reporting the offending row.
**Query:**
```sql
SELECT iv.inventory_id, iv.store_id, iv.sku
FROM inventory iv
LEFT JOIN stores st ON st.store_id = iv.store_id
WHERE st.store_id IS NULL;
```
**Explanation:** The anti-join exposes inventory pointing at a deleted store; a cleanup task can then re-key or archive them.
**Alt1:**
```sql
SELECT iv.inventory_id, iv.store_id, iv.sku
FROM inventory iv
WHERE NOT EXISTS (SELECT 1 FROM stores st WHERE st.store_id = iv.store_id);
```
`NOT EXISTS` restates the orphan check with no nullable join columns needed — identical result, clearer intent.

## Q96: Write a query joining three tables with LEFT joins, keeping the driver rows at every stage.
**Query:**
```sql
SELECT c.customer_id, o.order_id, od.product_id, od.quantity
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
LEFT JOIN order_details od ON od.order_id = o.order_id;
```
**Explanation:** Two cascading LEFT JOINs never discard a customer even if both order and detail links fail.

**Alt1:**
```sql
SELECT c.customer_id, o.order_id, od.product_id, od.quantity
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'confirmed'
LEFT JOIN order_details od ON od.order_id = o.order_id;
```
Adding a status predicate inside ON keeps unmatched confirmed-orders, but note details then only attach to confirmed orders.

## Q97: Produce a matrix where every weekend is paired with every venue for event planning.
**Query:**
```sql
SELECT dt.weekend_date, v.venue_id, v.venue_name
FROM venues v
CROSS JOIN (SELECT DATE '2026-01-03' AS weekend_date
            UNION ALL SELECT DATE '2026-01-10'
            UNION ALL SELECT DATE '2026-01-17') dt;
```
**Explanation:** Facade weekends crossed with all venues produce candidate (date, venue) bookings before availability checks.

## Q98: Show every customer with order totals, keeping customers with no orders and labeling the gap.
**Query:**
```sql
SELECT c.customer_id, c.name,
       COALESCE(SUM(o.amount), 0) AS lifetime_spend
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name;
```
**Explanation:** LEFT JOIN then COALESCE around the aggregate turns NULL sums into explicit 0 spend.
**Alt1:**
```sql
SELECT c.customer_id, c.name, SUM(o.amount) AS lifetime_spend
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
HAVING SUM(o.amount) IS NULL OR SUM(o.amount) = 0;
```
`HAVING` isolates the NULL-aggregate groups when distinguishing 'no orders' from 'zero-amount orders' matters.

## Q99: Write a query that finds every task lacking any subtask, and subtasks whose parent task is gone.
**Query:**
```sql
-- SQL Server
SELECT COALESCE(t.task_id, st.parent_task_id) AS task_id,
       t.task_name AS parent_name, st.subtask_name
FROM tasks t
FULL OUTER JOIN tasks st ON st.parent_task_id = t.task_id;
```
**Explanation:** A single FULL self-join pits each task against its would-be parent; NULLs expose both missing children and missing parents.

## Q100: Build a reconciliation query that fuses a LEFT anti-join, a CROSS JOIN generator, and a FULL emulation to grade each warehouse-day cell.
**Query:**
```sql
-- MySQL (FULL OUTER JOIN emulation)
SELECT COALESCE(l.wh_id, r.wh_id) AS wh_id,
       COALESCE(l.day, r.day) AS day,
       COALESCE(l.expected, 0) AS expected_count,
       COALESCE(r.expected, 0) AS actual_differences
FROM (SELECT w.warehouse_id AS wh_id, dy.day,
             COUNT(COALESCE(s.sale_id, 0)) AS expected
      FROM warehouses w
      CROSS JOIN (SELECT DATE '2026-01-01' AS day UNION ALL
                  SELECT DATE '2026-01-02' UNION ALL SELECT DATE '2026-01-03') dy
      LEFT JOIN sales s ON s.warehouse_id = w.warehouse_id
          AND s.sale_date = dy.day
      GROUP BY w.warehouse_id, dy.day) l
LEFT JOIN (SELECT warehouse_id AS wh_id, sale_date AS day, AVG(qty) AS expected
           FROM sales_snapshot
           GROUP BY warehouse_id, sale_date) r
    ON r.wh_id = l.wh_id AND r.day = l.day
UNION ALL
SELECT r.wh_id, r.day, 0, r.expected
FROM (SELECT warehouse_id AS wh_id, sale_date AS day, AVG(qty) AS expected
      FROM sales_snapshot
      GROUP BY warehouse_id, sale_date) r
LEFT JOIN (SELECT w.warehouse_id AS wh_id, dy.day
           FROM warehouses w
           CROSS JOIN (SELECT DATE '2026-01-01' AS day UNION ALL
                       SELECT DATE '2026-01-02' UNION ALL SELECT DATE '2026-01-03') dy) l
    ON l.wh_id = r.wh_id AND l.day = r.day
WHERE l.wh_id IS NULL;
```
**Explanation:** The inner LEFT legs build a dense warehouse-day grid with actual counts; the outer LEFT + UNION remainder emulates FULL OUTER JOIN, so live-data-only days are graded 0 rather than lost.
