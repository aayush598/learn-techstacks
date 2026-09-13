# Multi-Table Join Scenarios — 100 SQL Interview Q&A

## Q1: Write a query to show each student, the courses they are enrolled in, and the instructor teaching each course (3-way join).
**Query:**
```sql
SELECT s.name AS student, c.title AS course, i.name AS instructor
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id
JOIN instructors i ON i.id = c.instructor_id;
```

**Explanation:** Four INNER joins chained on FK lineage; each ON clause ties the newest table to a key a previous join already proved present.

## Q2: Write a query to show each order, every item line on it, and the product name for that line (3-way join).
**Query:**
```sql
SELECT o.id AS order_id, p.name AS product, oi.quantity, oi.unit_price
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id;
```

**Explanation:** orders→order_items is a 1-to-many parent/child hop; the products hop resolves product_id to a display name without multiplying rows.

## Q3: Write a query to list each employee, the department they belong to, and the region that department operates in.
**Query:**
```sql
SELECT e.name AS employee, d.name AS department, r.name AS region
FROM employees e
JOIN departments d ON d.id = e.dept_id
JOIN regions r ON r.id = d.region_id;
```

**Explanation:** The join order follows the FK walk employee→department→region; every one-to-one parent hop preserves employee rows.

## Q4: Write a query to show each book with its author and its publisher (3-way join).
**Query:**
```sql
SELECT b.title, a.name AS author, p.name AS publisher
FROM books b
JOIN authors a ON a.id = b.author_id
JOIN publishers p ON p.id = b.publisher_id;
```

**Explanation:** Author and publisher lookups are two independent branches hanging off the same book row, so the row count stays at one per book.

## Q5: Write a query to list every shipment with the warehouse it left from and the region that warehouse serves.
**Query:**
```sql
SELECT s.id AS shipment_id, s.ship_date, w.name AS warehouse, r.name AS region
FROM shipments s
JOIN warehouses w ON w.id = s.warehouse_id
JOIN regions r ON r.id = w.region_id;
```

**Explanation:** A straight 2-hop chain; shipment rows are preserved as long as both parent-row lookups succeed.

**Alt1:** Alias swap for readability, same plan.
```sql
SELECT sh.id, sh.ship_date, wh.name, rg.name
FROM shipments sh
JOIN warehouses wh ON wh.id = sh.warehouse_id
JOIN regions rg ON rg.id = wh.region_id;
```

## Q6: Write a query to show each booking with the airline operating it and the route flown, rendering the route as one string.
**Query:**
```sql
-- PostgreSQL
SELECT b.id AS booking_id, a.name AS airline,
       rt.origin || ' -> ' || rt.destination AS route
FROM bookings b
JOIN airlines a ON a.id = b.airline_id
JOIN routes rt ON rt.id = b.route_id;
```

**Explanation:** bookings→airline and bookings→route are independent FK lookups from the same row; the string build is pure display logic.

## Q7: Rewrite the student–course–instructor query using short table aliases and fully qualified columns.
**Query:**
```sql
SELECT s.name, c.title, i.name
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id
JOIN instructors i ON i.id = c.instructor_id;
```

**Explanation:** One-letter aliases keep a four-table join scannable, and every ON direction is obvious: e→s, e→c, c→i.

## Q8: Write a query listing order id, customer name, and product name for every order line, using aliases throughout (4 tables).
**Query:**
```sql
SELECT o.id AS order_id, cu.name AS customer, p.name AS product, oi.quantity
FROM orders o
JOIN customers cu ON cu.id = o.customer_id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id;
```

**Explanation:** Each hop introduces exactly one new table bound to the running lineage, so the 4-table join reads cleanly left to right.

## Q9: Write a query to list ALL students including those with no enrollments, showing course and instructor when present (multi-way LEFT join).
**Query:**
```sql
SELECT s.name AS student, c.title AS course, i.name AS instructor
FROM students s
LEFT JOIN enrollments e ON e.student_id = s.id
LEFT JOIN courses c ON c.id = e.course_id
LEFT JOIN instructors i ON i.id = c.instructor_id;
```

**Explanation:** The LEFT joins chain so a student with zero enrollments still yields a row; missing courses/instructors come back NULL.

**Alt1:** Same list re-rooted at courses, keeping unassigned courses visible even if students later drop:
```sql
SELECT s.name, c.title, i.name
FROM courses c
LEFT JOIN enrollments e ON e.course_id = c.id
LEFT JOIN students s ON s.id = e.student_id
LEFT JOIN instructors i ON i.id = c.instructor_id;
```

## Q10: Write a query to list all products including unsold ones, showing order id and order date when purchased (3-way LEFT).
**Query:**
```sql
SELECT p.name AS product, o.id AS order_id, o.order_date
FROM products p
LEFT JOIN order_items oi ON oi.product_id = p.id
LEFT JOIN orders o ON o.id = oi.order_id;
```

**Explanation:** products drives; both extensions are LEFT, so never-sold products keep one row with NULL order columns — not zero rows.

## Q11: Write a query to list every author with their books and each book's publisher, including authors who have no books.
**Query:**
```sql
SELECT a.name AS author, b.title AS book, p.name AS publisher
FROM authors a
LEFT JOIN books b ON b.author_id = a.id
LEFT JOIN publishers p ON p.id = b.publisher_id;
```

**Explanation:** Both hops are LEFT; the publisher hop attaches only to a real book row, so NULLs appear exactly where data is missing.

**Alt1:** Force authors without books to sort last:
```sql
SELECT a.name, b.title, p.name
FROM authors a
LEFT JOIN books b ON b.author_id = a.id
LEFT JOIN publishers p ON p.id = b.publisher_id
ORDER BY (b.title IS NULL), a.name;
```

## Q12: Write a query to list all regions with their warehouses and the shipments from each, including regions that have no warehouses.
**Query:**
```sql
SELECT r.name AS region, w.name AS warehouse, s.id AS shipment_id
FROM regions r
LEFT JOIN warehouses w ON w.region_id = r.id
LEFT JOIN shipments s ON s.warehouse_id = w.id;
```

**Explanation:** A cascade of LEFT joins: an empty region keeps a row, and a warehouse with no shipments shows NULL shipment columns.

## Q13: Write a query to list all airlines, the routes they fly, and the bookings on each route; include airlines with no routes.
**Query:**
```sql
SELECT a.name AS airline, rt.origin, rt.destination, b.id AS booking_id
FROM airlines a
LEFT JOIN routes rt ON rt.airline_id = a.id
LEFT JOIN bookings b ON b.route_id = rt.id;
```

**Explanation:** Each LEFT hop degrades to NULL rather than deleting the parent row, preserving airlines that fly nothing (yet).

## Q14: Write a query to show every course with its instructor and the instructor's department, including courses with no instructor assigned.
**Query:**
```sql
SELECT c.title AS course, i.name AS instructor, d.name AS department
FROM courses c
LEFT JOIN instructors i ON i.id = c.instructor_id
LEFT JOIN departments d ON d.id = i.dept_id;
```

**Explanation:** Course→instructor LEFT keeps unstaffed courses; the second LEFT only fires when an instructor row exists, so both gaps read as NULL.

## Q15: Write a query joining through the enrollment junction in both directions: student, course title, and course category.
**Query:**
```sql
SELECT s.name AS student, c.title, c.category
FROM enrollments e
JOIN students s ON s.id = e.student_id
JOIN courses c ON c.id = e.course_id;
```

**Explanation:** The junction sits in the middle; both direction joins are guaranteed non-NULL because an enrollment references real student and course rows.

## Q16: List each instructor and every student they teach through courses - a 2-hop relationship via the enrollment junction table.
**Query:**
```sql
SELECT DISTINCT i.name AS instructor, s.name AS student
FROM instructors i
JOIN courses c ON c.instructor_id = i.id
JOIN enrollments e ON e.course_id = c.id
JOIN students s ON s.id = e.student_id;
```

**Explanation:** No direct instructor→student link exists; travel instructor→course→enrollment→student, then dedupe repeated pairs.

**Alt1:** Same path read from the junction outward:
```sql
SELECT DISTINCT i.name, s.name
FROM enrollments e
JOIN students s ON s.id = e.student_id
JOIN courses c ON c.id = e.course_id
JOIN instructors i ON i.id = c.instructor_id;
```

## Q17: order_items and line_details share a composite key (order_id, item_seq). Join them and then to products.
**Query:**
```sql
SELECT oi.order_id, oi.item_seq, p.name AS product, ld.ship_by_date
FROM order_items oi
JOIN line_details ld
  ON ld.order_id = oi.order_id AND ld.item_seq = oi.item_seq
JOIN products p ON p.id = oi.product_id;
```

**Explanation:** When no single column identifies a row, the ON clause must repeat the whole composite key; both halves must match exactly.

## Q18: Match each sale to a price quote on the product AND a validity date window (multiple join conditions on one table).
**Query:**
```sql
SELECT p.name AS product, s.sale_id, s.sale_date, q.unit_price
FROM sales s
JOIN products p ON p.id = s.product_id
JOIN quotes q
  ON q.product_id = s.product_id
 AND s.sale_date BETWEEN q.valid_from AND q.valid_to;
```

**Explanation:** Join-by-identity alone is not enough here; the second condition picks the quote whose date range contains the sale.

**Alt1:** Same, using an explicit half-open interval to control boundary semantics:
```sql
SELECT p.name, s.sale_id, q.unit_price
FROM sales s
JOIN products p ON p.id = s.product_id
JOIN quotes q ON q.product_id = s.product_id
 AND s.sale_date >= q.valid_from AND s.sale_date < q.valid_to;
```

## Q19: Students↔courses is many-to-many and courses can be co-taught. Write the join and control the row fan-out.
**Query:**
```sql
SELECT DISTINCT s.name AS student, c.title AS course
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id
LEFT JOIN course_staff cs ON cs.course_id = c.id;
```

**Explanation:** Each co-teacher would otherwise add one row per (student, course); DISTINCT collapses back to the set you actually want.

## Q20: Show each employee, their manager's name, and their manager's manager's name (self-join chain on employees).
**Query:**
```sql
SELECT e.name AS employee, m.name AS manager, mm.name AS skip_level
FROM employees e
JOIN employees m ON m.id = e.manager_id
JOIN employees mm ON mm.id = m.manager_id;
```

**Explanation:** Two self-joins under different aliases climb two org levels; each alias is a distinct view of the same physical table.

**Alt1:** Make the second hop LEFT so employees whose manager has no manager still appear:
```sql
SELECT e.name, m.name AS manager, mm.name AS skip_level
FROM employees e
JOIN employees m ON m.id = e.manager_id
LEFT JOIN employees mm ON mm.id = m.manager_id;
```

## Q21: A task row references the same users table twice (assigned_to, approved_by). Return both names in one query.
**Query:**
```sql
SELECT t.id, ua.name AS assignee, up.name AS approver
FROM tasks t
JOIN users ua ON ua.id = t.assigned_to
JOIN users up ON up.id = t.approved_by;
```

**Explanation:** Joining one table under two aliases reads two FK roles from a single row without column-name collisions.

**Alt1:** With approval still optional (NULL-safe and kept visible):
```sql
SELECT t.id, ua.name AS assignee, up.name AS approver
FROM tasks t
JOIN users ua ON ua.id = t.assigned_to
LEFT JOIN users up ON up.id = t.approved_by;
```

## Q22: Mix an INNER join after a LEFT join and show the NULL-widening hazard, then fix it.
**Query:**
```sql
SELECT s.name AS student, c.title
FROM students s
LEFT JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id;
```

**Explanation:** The trailing INNER join rejects the NULL rows the LEFT produced (students with no enrollments vanish), so the LEFT is wasted.

**Fix:** Make every subsequent join LEFT to keep unenrolled students:
```sql
SELECT s.name, c.title
FROM students s
LEFT JOIN enrollments e ON e.student_id = s.id
LEFT JOIN courses c ON c.id = e.course_id;
```

## Q23: Join orders to a derived table of customers who ordered in 2025, then to the customer master for names.
**Query:**
```sql
SELECT o.id AS order_id, c.name AS customer
FROM orders o
JOIN (SELECT DISTINCT customer_id
      FROM orders
      WHERE order_date >= DATE '2025-01-01') recent
  ON recent.customer_id = o.customer_id
JOIN customers c ON c.id = o.customer_id;
```

**Explanation:** The derived table pre-filters the customer population before the multi-way join; the master lookup then adds display names.

**Alt1:** Same filter expressed as a CTE for readability:
```sql
WITH recent AS (
  SELECT DISTINCT customer_id FROM orders WHERE order_date >= DATE '2025-01-01'
)
SELECT o.id, c.name
FROM orders o
JOIN recent ON recent.customer_id = o.customer_id
JOIN customers c ON c.id = o.customer_id;
```

## Q24: Offerings are keyed by (course_id, semester). Join offerings, teaching staff, and enrollments on the composite key.
**Query:**
```sql
SELECT o.course_id, o.semester, st.name AS instructor, s.name AS student
FROM offerings o
JOIN course_staff st
  ON st.course_id = o.course_id AND st.semester = o.semester
JOIN enrollments e
  ON e.course_id = o.course_id AND e.semester = o.semester
JOIN students s ON s.id = e.student_id;
```

**Explanation:** Identity spans two columns, so every hop must reproduce (course_id, semester) in its ON clause or rows misalign.

**Alt1:** Restrict to one semester before joining so fewer rows flow through every hop:
```sql
SELECT o.course_id, st.name, s.name
FROM offerings o
JOIN course_staff st ON st.course_id = o.course_id AND st.semester = o.semester
JOIN enrollments e  ON e.course_id = o.course_id AND e.semester = o.semester
JOIN students s     ON s.id = e.student_id
WHERE o.semester = '2025-Fall';
```

## Q25: Write a 4-table join across customers → orders → order_items → products, and state what each hop contributes.
**Query:**
```sql
SELECT cu.name AS customer, o.id AS order_id, oi.quantity, p.name AS product
FROM customers cu
JOIN orders o ON o.customer_id = cu.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id;
```

**Explanation:** customers→orders collects a customer's orders; orders→items expands each order into lines; items→products resolves product ids to names.

**Alt1:** Left-drive from customers to keep customers who never ordered:
```sql
SELECT cu.name, o.id, p.name
FROM customers cu
LEFT JOIN orders o ON o.customer_id = cu.id
LEFT JOIN order_items oi ON oi.order_id = o.id
LEFT JOIN products p ON p.id = oi.product_id;
```
## Q26: Show each book with its author and publisher, but only books published after 2020.
**Query:**
```sql
SELECT b.title, a.name AS author, p.name AS publisher, b.pub_year
FROM books b
JOIN authors a ON a.id = b.author_id
JOIN publishers p ON p.id = b.publisher_id
WHERE b.pub_year > 2020;
```

**Explanation:** The two joins associate matching rows; the WHERE runs after joining, so filtering one table does not disturb the others.

## Q27: Demonstrate the WHERE-vs-ON trap: filtering the right side of a LEFT join with WHERE silently converts it to an INNER join.
**Query:**
```sql
SELECT a.name AS author, b.title
FROM authors a
LEFT JOIN books b ON b.author_id = a.id
WHERE b.pub_year > 2015;
```

**Explanation:** WHERE runs after the LEFT join and drops rows where b is NULL — the "authors without matching books" rows vanish.

**Alt1:** Move the filter into the ON clause to keep the LEFT semantics:
```sql
SELECT a.name, b.title
FROM authors a
LEFT JOIN books b ON b.author_id = a.id AND b.pub_year > 2015;
```

**Alt2:** Keep WHERE but explicitly re-admit the NULLs that mean "no matching book":
```sql
SELECT a.name, b.title
FROM authors a
LEFT JOIN books b ON b.author_id = a.id
WHERE b.pub_year > 2015 OR b.author_id IS NULL;
```

## Q28: Shipments depart on a shipping lane keyed by the composite (warehouse_id, region_id). Join to the lane rates table on both columns.
**Query:**
```sql
SELECT s.id, l.rate, w.name AS warehouse
FROM shipments s
JOIN lane_rates l
  ON l.warehouse_id = s.warehouse_id AND l.region_id = s.region_id
JOIN warehouses w ON w.id = s.warehouse_id;
```

**Explanation:** The lane rate is found by the composite key; the warehouse hop is an ordinary FK lookup after that.

**Alt1:** Straighten the hop order — resolve warehouse first, then the composite lane rate:
```sql
SELECT s.id, l.rate, w.name
FROM shipments s
JOIN warehouses w ON w.id = s.warehouse_id
JOIN lane_rates l
  ON l.warehouse_id = s.warehouse_id AND l.region_id = s.region_id;
```

## Q29: List each department, the region it sits in, and the head instructor of the department. Include departments with no head assigned.
**Query:**
```sql
SELECT d.name AS department, rg.name AS region, i.name AS head
FROM departments d
JOIN regions rg ON rg.id = d.region_id
LEFT JOIN instructors i ON i.id = d.head_instructor_id;
```

**Explanation:** The INNER region hop shrinks nothing (a department's region is mandatory); the head hop is LEFT so unassigned departments stay visible.

## Q30: A document row stores created_by and last_edited_by FKs to the same users table. Return both names plus the document title.
**Query:**
```sql
SELECT t.title, u1.name AS created_by, u2.name AS last_edited_by
FROM documents t
JOIN users u1 ON u1.id = t.created_by
LEFT JOIN users u2 ON u2.id = t.last_edited_by;
```

**Explanation:** The same table appears twice under two aliases; the second is LEFT because a never-edited document has a NULL editor.

## Q31: List every product with its category and every 2024 sale, keeping all products (date filter moved into the ON clause).
**Query:**
```sql
SELECT p.name AS product, c.name AS category, s.sale_id
FROM products p
JOIN categories c ON c.id = p.category_id
LEFT JOIN sales s
  ON s.product_id = p.id
 AND s.sale_date >= DATE '2024-01-01' AND s.sale_date < DATE '2025-01-01';
```

**Explanation:** The date constraint lives in the ON clause, so unsold products and non-2024 sales still display alongside their product rows.

**Alt1:** Break the year check into two columns for a filter-friendly shape:
```sql
SELECT p.name, c.name, s.sale_id
FROM products p
JOIN categories c ON c.id = p.category_id
LEFT JOIN sales s
  ON s.product_id = p.id
 AND EXTRACT(YEAR FROM s.sale_date) = 2024;
```

## Q32: Anti-join: find courses that have no enrolled students, using a 3-table LEFT chain and a NULL test.
**Query:**
```sql
SELECT DISTINCT c.title
FROM courses c
LEFT JOIN enrollments e ON e.course_id = c.id
LEFT JOIN students s ON s.id = e.student_id
WHERE s.id IS NULL;
```

**Explanation:** If no student row survived the joins, the course had zero enrollments; the NULL filter is the anti-join test.

**Alt1:** A NOT EXISTS anti-join expresses the intent even more directly:
```sql
SELECT c.title
FROM courses c
WHERE NOT EXISTS (SELECT 1 FROM enrollments e WHERE e.course_id = c.id);
```

## Q33: Find products that have never been ordered, along with their category name.
**Query:**
```sql
SELECT p.name AS product, c.name AS category
FROM products p
JOIN categories c ON c.id = p.category_id
LEFT JOIN order_items oi ON oi.product_id = p.id
WHERE oi.order_id IS NULL;
```

**Explanation:** The LEFT join manufactures NULL order columns for unsold products; the WHERE then keeps exactly those orphans.

**Alt1:** Same outcome via NOT EXISTS on the item table:
```sql
SELECT p.name, c.name
FROM products p
JOIN categories c ON c.id = p.category_id
WHERE NOT EXISTS (SELECT 1 FROM order_items oi WHERE oi.product_id = p.id);
```

## Q34: Find instructors who are teaching zero students (LEFT chain across courses and enrollments, NULL test).
**Query:**
```sql
SELECT DISTINCT i.name AS instructor
FROM instructors i
LEFT JOIN courses c ON c.instructor_id = i.id
LEFT JOIN enrollments e ON e.course_id = c.id
WHERE e.student_id IS NULL;
```

**Explanation:** An instructor with no courses (or only empty courses) never produces an enrollment row, leaving e NULL for the filter.

## Q35: Chained-join lineage bug: this query is wrong because the last ON references the wrong alias. Diagnose and fix it.
**Query:**
```sql
SELECT s.name, c.title
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = s.id;   -- BUG: should be e.course_id
```

**Explanation:** Comparing c.id = s.id pairs a course identity with a student id; the mismatch silently yields a hidden cross-product.

**Alt1:** Correct product with the lineage restored:
```sql
SELECT s.name, c.title
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id;
```

## Q36: Courses are co-taught via a course_instructors junction. List each course, every co-teacher, and the co-teacher's department.
**Query:**
```sql
SELECT c.title AS course, i.name AS co_teacher, d.name AS department
FROM courses c
JOIN course_instructors ci ON ci.course_id = c.id
JOIN instructors i ON i.id = ci.instructor_id
JOIN departments d ON d.id = i.dept_id;
```

**Explanation:** The junction contributes one row per (course, co-teacher); the department hop rides along per instructor row without extra fan-out.

## Q37: A store stocks products (unique store_id+product_id). Show each stocked store, the product, and the product's supplier, only where stock is positive.
**Query:**
```sql
SELECT so.name AS store, p.name AS product, su.name AS supplier
FROM stock st
JOIN stores so ON so.id = st.store_id
JOIN products p ON p.id = st.product_id
JOIN suppliers su ON su.id = p.supplier_id
WHERE st.qty > 0;
```

**Explanation:** stock is the junction tying stores and products; supplier is an extra lookup off products; the WHERE trims the output set only.

## Q38: Customers get loyalty tiers via a membership table with a validity window. Show customer, order, and tier when the order falls in the window.
**Query:**
```sql
SELECT cu.name AS customer, o.id AS order_id, lt.name AS tier
FROM customers cu
JOIN orders o ON o.customer_id = cu.id
LEFT JOIN memberships m
  ON m.customer_id = cu.id
 AND o.order_date BETWEEN m.start_date AND m.end_date
LEFT JOIN loyalty_tiers lt ON lt.id = m.tier_id;
```

**Explanation:** The BETWEEN in the ON picks only the membership active at order time; LEFT keeps customers with no matching membership.

## Q39: Find all students who share at least one course with the student named 'Alice', excluding Alice herself (2-hop through the junction).
**Query:**
```sql
SELECT DISTINCT s.name
FROM students s
JOIN enrollments e2 ON e2.student_id = s.id
JOIN enrollments e1 ON e1.course_id = e2.course_id
JOIN students alice ON alice.id = e1.student_id
WHERE alice.name = 'Alice' AND s.id <> alice.id;
```

**Explanation:** Coupling two enrollments on course_id finds co-enrollees; DISTINCT removes duplicate classmates from multiple shared courses.

**Alt1:** Self-contained with the target student's id computed up front in a CTE:
```sql
WITH target AS (SELECT id FROM students WHERE name = 'Alice')
SELECT DISTINCT s.name
FROM students s
JOIN enrollments e2 ON e2.student_id = s.id
JOIN enrollments e1 ON e1.course_id = e2.course_id
JOIN target t ON t.id = e1.student_id
WHERE s.id <> t.id;
```

## Q40: Climb three org levels with self-joins: employee, manager, middle manager, and director (three hops on employees).
**Query:**
```sql
SELECT e.name AS employee, m.name AS manager, mm.name AS middle, mmm.name AS director
FROM employees e
JOIN employees m ON m.id = e.manager_id
JOIN employees mm ON mm.id = m.manager_id
JOIN employees mmm ON mmm.id = mm.manager_id;
```

**Explanation:** Each alias advances one hop of the manager pointer; four aliases produce a single flat row of the full reporting line.

## Q41: 5-way chain: orders → order_items → products → suppliers → regions, filtered to one region.
**Query:**
```sql
SELECT o.id AS order_id, p.name AS product, su.name AS supplier, r.name AS region
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
JOIN suppliers su ON su.id = p.supplier_id
JOIN regions r ON r.id = su.region_id
WHERE r.name = 'West';
```

**Explanation:** Five tables in one chain; the WHERE targets the far end of the lineage, and since every hop is INNER no row is wrongly dropped.

**Alt1:** Filter the supplier at the source with an ON clause instead, keeping the detail rows:
```sql
SELECT o.id, p.name, su.name, r.name
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
JOIN suppliers su ON su.id = p.supplier_id
JOIN regions r ON r.id = su.region_id
WHERE r.id = 7;
```

## Q42: Three tables each contain a `name` column. Write an unambiguous 3-way join with every column qualified.
**Query:**
```sql
SELECT p.name AS product, c.name AS category, s.name AS supplier
FROM products p
JOIN categories c ON c.id = p.category_id
JOIN suppliers s ON s.id = p.supplier_id;
```

**Explanation:** Unqualified `name` would be ambiguous or resolve unpredictably; every projected column is pinned to its table alias.

**Alt1:** Use positional "select only what is needed" so no name column collides:
```sql
SELECT p.name, c.name
FROM products p
JOIN categories c ON c.id = p.category_id
JOIN suppliers s ON s.id = p.supplier_id;
```

## Q43: Explain and fix the Cartesian trap: comma-joining three tables with a meaningless predicate.
**Query:**
```sql
SELECT s.name, c.title
FROM students s, courses c, instructors i
WHERE s.id = i.id;   -- one pointless predicate; still a cross product
```

**Explanation:** Missing or irrelevant join conditions with comma-joins multiply every row of each table by the other tables' rows.

**Alt1:** Explicit joins against the real foreign keys restore only genuine facts:
```sql
SELECT s.name, c.title, i.name
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id
JOIN instructors i ON i.id = c.instructor_id;
```

## Q44: Find shipments whose warehouse region differs from the shipment's destination region (same table read twice).
**Query:**
```sql
SELECT s.id AS shipment_id, w.name AS warehouse, rg.name AS origin_region, rg2.name AS dest_region
FROM shipments s
JOIN warehouses w ON w.id = s.warehouse_id
JOIN regions rg ON rg.id = w.region_id
JOIN regions rg2 ON rg2.id = s.dest_region_id
WHERE rg.id <> rg2.id;
```

**Explanation:** regions appears under two aliases (origin vs destination); the inequality filters to cross-region shipments.

## Q45: Show the discipline of running INNER hops first and keeping LEFT hops at the end of a mixed multi-join.
**Query:**
```sql
SELECT s.name AS student, c.title, i.name AS instructor, d.name AS department
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id
JOIN instructors i ON i.id = c.instructor_id
LEFT JOIN departments d ON d.id = i.dept_id;
```

**Explanation:** All mandatory INNER hops narrow the population first; the single trailing LEFT adds optional data without resurrecting or dropping rows.

**Alt1:** The same data with the LEFT earlier — results look identical here only because nothing INNER follows it:
```sql
SELECT s.name, c.title, i.name, d.name
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id
LEFT JOIN departments d ON d.id = c.dept_id
JOIN instructors i ON i.id = c.instructor_id;
```

## Q46: Prefilter a wide table in a derived table, then 3-way join: enrollments for '2025-Fall' joined to students and courses.
**Query:**
```sql
SELECT s.name, c.title
FROM (SELECT * FROM enrollments WHERE semester = '2025-Fall') fall
JOIN students s ON s.id = fall.student_id
JOIN courses c ON c.id = fall.course_id;
```

**Explanation:** The derived table shrinks enrollments before any join, so every downstream hop touches far fewer rows.

**Alt1:** Same via CTE, materializing the filter once and reusing it:
```sql
WITH fall AS (SELECT * FROM enrollments WHERE semester = '2025-Fall')
SELECT s.name, c.title
FROM fall
JOIN students s ON s.id = fall.student_id
JOIN courses c ON c.id = fall.course_id;
```

## Q47: Products have versioned masters keyed by (product_id, version). Join product, version, and price list on the composite key.
**Query:**
```sql
SELECT p.sku, v.version, v.description, pl.retail_price
FROM products p
JOIN product_versions v ON v.product_id = p.id
JOIN price_list pl ON pl.product_id = v.product_id AND pl.version = v.version
WHERE p.id = 2048 AND v.version = 3;
```

**Explanation:** price_list is only meaningful per exact version, so its ON repeats the composite key; the WHERE freezes one version.

## Q48: 4-way finance chain: transactions → cards → accounts → customers, filtered to large transactions.
**Query:**
```sql
SELECT cu.name AS customer, t.id AS tx_id, t.amount
FROM transactions t
JOIN cards cd ON cd.id = t.card_id
JOIN accounts ac ON ac.id = cd.account_id
JOIN customers cu ON cu.id = ac.customer_id
WHERE t.amount > 1000;
```

**Explanation:** Four tables bound by FK lineage; the amount filter can ride last without changing any join result.

**Alt1:** Restrict the big-value set inside a derived table first:
```sql
SELECT cu.name, x.id AS tx_id, x.amount
FROM (SELECT id, amount, card_id FROM transactions WHERE amount > 1000) x
JOIN cards cd ON cd.id = x.card_id
JOIN accounts ac ON ac.id = cd.account_id
JOIN customers cu ON cu.id = ac.customer_id;
```

## Q49: With all INNER joins, join order is a plan detail, not a result detail. Demonstrate the same 3-way query as all-INNER vs all-LEFT.
**Query:**
```sql
SELECT s.name, c.title, i.name
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id
JOIN instructors i ON i.id = c.instructor_id;
```

**Alt1:**
```sql
SELECT s.name, c.title, i.name
FROM students s
LEFT JOIN enrollments e ON e.student_id = s.id
LEFT JOIN courses c ON c.id = e.course_id
LEFT JOIN instructors i ON i.id = c.instructor_id;
```

**Explanation:** The only divergent rows are unenrolled students: INNER deletes them, LEFT preserves them as NULLs — a deliberate choice, not an accident.

## Q50: 5-table chain from order back to country: orders → customers → addresses → cities → countries.
**Query:**
```sql
SELECT o.id AS order_id, cu.name AS customer, cy.name AS city, co.name AS country
FROM orders o
JOIN customers cu ON cu.id = o.customer_id
JOIN addresses ad ON ad.id = cu.address_id
JOIN cities cy ON cy.id = ad.city_id
JOIN countries co ON co.id = cy.country_id;
```

**Explanation:** The join key of each hop is the FK produced by the previous hop — column lineage runs in one direction end to end.

**Alt1:** Package the country derivation as a CTE, then attach orders:
```sql
WITH customer_country AS (
  SELECT cu.id, co.name AS country
  FROM customers cu
  JOIN addresses ad ON ad.id = cu.address_id
  JOIN cities cy ON cy.id = ad.city_id
  JOIN countries co ON co.id = cy.country_id
)
SELECT o.id, cu.name, cc.country
FROM orders o
JOIN customers cu ON cu.id = o.customer_id
JOIN customer_country cc ON cc.id = o.customer_id;
```
## Q51: Courses are team-taught via the course_instructors junction. List each course, every co-teacher, and their home department.
**Query:**
```sql
SELECT c.title AS course, i.name AS co_teacher, d.name AS department
FROM courses c
JOIN course_instructors ci ON ci.course_id = c.id
JOIN instructors i ON i.id = ci.instructor_id
JOIN departments d ON d.id = i.dept_id;
```

**Explanation:** The junction yields one row per (course, instructor) and the department hop rides along per instructor row.

**Alt1:** Read from the instructor side instead, per-co-teacher course list:
```sql
SELECT i.name AS co_teacher, c.title AS course, d.name AS department
FROM instructors i
JOIN course_instructors ci ON ci.instructor_id = i.id
JOIN courses c ON c.id = ci.course_id
JOIN departments d ON d.id = i.dept_id;
```

## Q52: Hospital reporting: patients → visits → doctors → departments (4-way) with a diagnosis filter.
**Query:**
```sql
SELECT pt.name AS patient, d.name AS doctor, dp.name AS department
FROM patients pt
JOIN visits v ON v.patient_id = pt.id
JOIN doctors d ON d.id = v.doctor_id
JOIN departments dp ON dp.id = d.dept_id
WHERE v.diagnosis = 'flu';
```

**Explanation:** Each hop walks one FK; the WHERE trims rows after the full chain is assembled.

**Alt1:** Move the diagnosis into the visits hop to shrink the join seeded first:
```sql
SELECT pt.name, d.name, dp.name
FROM patients pt
JOIN (SELECT * FROM visits WHERE diagnosis = 'flu') v ON v.patient_id = pt.id
JOIN doctors d ON d.id = v.doctor_id
JOIN departments dp ON dp.id = d.dept_id;
```

## Q53: Enrollment report: students → enrollments → courses → departments, showing the department of each course.
**Query:**
```sql
SELECT s.name AS student, c.title AS course, d.name AS department
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id
JOIN departments d ON d.id = c.dept_id;
```

**Explanation:** The department attaches to the course, not the enrollment, so the third hop targets c.dept_id.

**Alt1:** Barn-shaped variant with instructors resolved as the fourth right-hand column separate from the department column:
```sql
SELECT s.name, c.title, d.name AS department, i.name AS instructor
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id
JOIN departments d ON d.id = c.dept_id
JOIN instructors i ON i.id = c.instructor_id;
```

## Q54: Products have a category, and categories can nest (parent_category_id). Show product, category, and parent category.
**Query:**
```sql
SELECT p.name AS product, c.name AS category, pc.name AS parent_category
FROM products p
JOIN categories c ON c.id = p.category_id
LEFT JOIN categories pc ON pc.id = c.parent_id;
```

**Explanation:** categories is aliased twice — the product's own category and its ancestor; LEFT keeps top-level categories with no parent.

## Q55: Find colleagues — employees who report to the same manager — and show their shared department.
**Query:**
```sql
SELECT m.name AS manager, e1.name AS employee_1, e2.name AS employee_2, d.name
FROM employees m
JOIN employees e1 ON e1.manager_id = m.id
JOIN employees e2 ON e2.manager_id = m.id
JOIN departments d ON d.id = e1.dept_id
WHERE e1.id < e2.id;
```

**Explanation:** Two self-joins fan out every manager/direct-report pair; e1.id < e2.id removes mirrored duplicates.

## Q56: Cartesian-explosion trap: joining students, courses, and instructors "all at once" multiplies rows. Show the trap and the correct route through the junction.
**Query:**
```sql
SELECT DISTINCT s.name, c.title, i.name
FROM students s, courses c, instructors i;
```

**Alt1 (correct):**
```sql
SELECT DISTINCT s.name, c.title, i.name
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id
JOIN instructors i ON i.id = c.instructor_id;
```

**Explanation:** Without the junction, three independent attribute domains multiply to a cross product; the junction path yields only facts that truly exist.

## Q57: Report items for orders placed in the last 7 days: filter first in a derived table, then join items and products.
**Query:**
```sql
SELECT oi.order_id, p.name, oi.quantity
FROM (SELECT id FROM orders WHERE order_date >= CURRENT_DATE - 7) fresh
JOIN order_items oi ON oi.order_id = fresh.id
JOIN products p ON p.id = oi.product_id;
```

**Explanation:** Narrowing to recent order ids up front trims order_items early; the product hop then adds display names.

**Alt1:** Same filter placed directly on orders with the items hop still after it:
```sql
SELECT oi.order_id, p.name, oi.quantity
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
WHERE o.order_date >= CURRENT_DATE - 7;
```

## Q58: Date-overlap join: list bookings whose stay overlaps a room's maintenance window (rooms + bookings + maintenance).
**Query:**
```sql
SELECT bk.id AS booking_id, rm.name AS room, mt.maintenance_start, mt.maintenance_end
FROM bookings bk
JOIN rooms rm ON rm.id = bk.room_id
JOIN maintenance mt ON mt.room_id = rm.id
  AND bk.check_in <= mt.maintenance_end
  AND bk.check_out >= mt.maintenance_start;
```

**Explanation:** The overlap test is the join condition itself: two rows match only when their date spans intersect.

**Alt1:** Overlap expressed with explicit NOT-gap logic (equivalent, some find it clearer):
```sql
SELECT bk.id, rm.name, mt.maintenance_start
FROM bookings bk
JOIN rooms rm ON rm.id = bk.room_id
JOIN maintenance mt ON mt.room_id = rm.id
WHERE NOT (bk.check_out <= mt.maintenance_start OR bk.check_in >= mt.maintenance_end);
```

## Q59: Mix a self-join into a chain: shipments → warehouses → regions, plus the region's assigned manager (from employees).
**Query:**
```sql
SELECT s.id AS shipment_id, w.name AS warehouse, r.name AS region, e.name AS regional_manager
FROM shipments s
JOIN warehouses w ON w.id = s.warehouse_id
JOIN regions r ON r.id = w.region_id
LEFT JOIN employees e ON e.id = r.manager_id;
```

**Explanation:** The fourth hop is an ordinary FK join into employees on the region's manager; LEFT keeps regions with no manager assigned.

## Q60: Full reporting line lenient with gaps: employee, manager, and director, keeping rows wherever a level is missing (3-level LEFT self-join).
**Query:**
```sql
SELECT e.name AS employee, m.name AS manager, mm.name AS director
FROM employees e
LEFT JOIN employees m ON m.id = e.manager_id
LEFT JOIN employees mm ON mm.id = m.manager_id;
```

**Explanation:** Both hops are LEFT; top-of-tree people show manager NULL, and people whose manager has no manager show director NULL.

## Q61: Match a product price quote on THREE conditions: product, currency, and validity window, across 3 tables.
**Query:**
```sql
SELECT p.name AS product, q.currency, q.unit_price, s.sale_id
FROM sales s
JOIN products p ON p.id = s.product_id
JOIN quotes q
  ON q.product_id = s.product_id
 AND q.currency = s.currency
 AND s.sale_date BETWEEN q.valid_from AND q.valid_to;
```

**Explanation:** A three-part ON — identity, currency, time; any weaker condition grabs the wrong quote.

**Alt1:** Convert currency to a canonical code first so non-matching currency rows are excluded before the range test:
```sql
SELECT p.name, q.unit_price, s.sale_id
FROM sales s
JOIN products p ON p.id = s.product_id
JOIN quotes q ON q.product_id = s.product_id
JOIN currencies cu ON cu.code = s.currency AND cu.code = q.currency
WHERE s.sale_date BETWEEN q.valid_from AND q.valid_to;
```

## Q62: Lineage slip: the last join in this query references the FIRST table by mistake. Diagnose and fix.
**Query:**
```sql
SELECT o.id, p.name
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = o.id;      -- BUG: should be oi.product_id
```

**Explanation:** p.id = o.id compares a product id to an order id; no sane match — the query returns junk or a full cross product.

**Alt1 (fix):**
```sql
SELECT o.id, p.name
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id;
```

## Q63: Derived table of instructors on a fixed-term contract, then a 3-way join to the courses and students they teach.
**Query:**
```sql
SELECT i.name AS instructor, c.title AS course, s.name AS student
FROM (SELECT id, name FROM instructors WHERE contract_type = 'contract') i
JOIN courses c ON c.instructor_id = i.id
JOIN enrollments e ON e.course_id = c.id
JOIN students s ON s.id = e.student_id;
```

**Explanation:** Contract filtering happens once inside the derived table; downstream joins only ever see eligible instructors.

## Q64: Phones → SIM cards → networks → data plans: 4-way join, alias every table.
**Query:**
```sql
SELECT ph.number, se.iccid, nw.name AS network, pl.plan_name
FROM phones ph
JOIN sims se ON se.phone_id = ph.id
JOIN networks nw ON nw.id = se.network_id
JOIN plans pl ON pl.id = se.plan_id;
```

**Explanation:** Four hops, one alias each; SIM is the bridge tying phone, network, and plan together.

## Q65: LEFT-heavy 4-way with NULL flags: enrollment, course, instructor, and grade — keep ungraded enrollments.
**Query:**
```sql
SELECT s.name AS student, c.title AS course, i.name AS instructor, g.score AS grade_score
FROM enrollments e
JOIN students s ON s.id = e.student_id
LEFT JOIN courses c ON c.id = e.course_id
LEFT JOIN instructors i ON i.id = c.instructor_id
LEFT JOIN grades g ON g.enrollment_id = e.id;
```

**Explanation:** The first INNER anchors the fact rows; every optional extension is LEFT, so ungraded enrollments still appear with a NULL score.

**Alt1:** Flag incomplete records instead of hiding them:
```sql
SELECT s.name, c.title,
       CASE WHEN g.score IS NULL THEN 'INCOMPLETE' ELSE 'GRADED' END AS status
FROM enrollments e
JOIN students s ON s.id = e.student_id
LEFT JOIN courses c ON c.id = e.course_id
LEFT JOIN grades g ON g.enrollment_id = e.id;
```

## Q66: Learning-path chain: courses → modules → lessons → quiz questions (4-way), returning the full path.
**Query:**
```sql
SELECT c.title AS course, m.title AS module, l.title AS lesson, q.prompt
FROM courses c
JOIN modules m ON m.course_id = c.id
JOIN lessons l ON l.module_id = m.id
JOIN questions q ON q.lesson_id = l.id;
```

**Explanation:** Every hop descends a parent/child level; the row count multiplies down the tree at each level by design.

## Q67: An order carries two address FKs (billing, shipping) into the same addresses table, plus the customer. Resolve both.
**Query:**
```sql
SELECT o.id AS order_id, cu.name AS customer, ab.street AS bill_to, ash.street AS ship_to
FROM orders o
JOIN customers cu ON cu.id = o.customer_id
JOIN addresses ab ON ab.id = o.billing_address_id
JOIN addresses ash ON ash.id = o.shipping_address_id;
```

**Explanation:** addresses is joined twice under role aliases; each maps a different FK column to its own row.

**Alt1:** Flag orders whose addresses match, using the two address aliases in one comparison:
```sql
SELECT o.id, cu.name,
       CASE WHEN ab.id = ash.id THEN 'SAME ADDRESS' ELSE 'DIFFERENT' END AS addr
FROM orders o
JOIN customers cu ON cu.id = o.customer_id
JOIN addresses ab ON ab.id = o.billing_address_id
JOIN addresses ash ON ash.id = o.shipping_address_id;
```

## Q68: employees → departments → companies, plus each employee's manager from the same employees table (self-join mixed into a chain).
**Query:**
```sql
SELECT e.name AS employee, m.name AS manager, d.name AS department, co.name AS company
FROM employees e
JOIN employees m ON m.id = e.manager_id
JOIN departments d ON d.id = e.dept_id
JOIN companies co ON co.id = d.company_id;
```

**Explanation:** The self-join is just another hop in the chain; the three other FKs resolve normally around it.

## Q69: Rewrite a multi-key 3-way join using USING to merge identically named composite columns.
**Query:**
```sql
-- PostgreSQL
SELECT o.course_id, o.semester, st.name AS instructor
FROM offerings o
JOIN course_staff st USING (course_id, semester)
JOIN enrollments e USING (course_id, semester);
```

**Explanation:** USING coalesces the composite key and dedupes the output columns — cleaner syntax that is only valid when key names match.

**Alt1:** The same join spelled with explicit ON for portability:
```sql
SELECT o.course_id, o.semester, st.name
FROM offerings o
JOIN course_staff st ON st.course_id = o.course_id AND st.semester = o.semester
JOIN enrollments e ON e.course_id = o.course_id AND e.semester = o.semester;
```

## Q70: departments → courses → sections → instructors: find who teaches which section in which department (4-way).
**Query:**
```sql
SELECT d.name AS department, c.title AS course, sec.day_of_week, i.name AS instructor
FROM departments d
JOIN courses c ON c.dept_id = d.id
JOIN sections sec ON sec.course_id = c.id
JOIN instructors i ON i.id = sec.instructor_id;
```

**Explanation:** sections is where a concrete instructor attaches; the upstream rows supply the department and course context columns.

## Q71: Offerings per semester joined to enrollments and to the instructor who staffed that offering (composite key on both hops).
**Query:**
```sql
SELECT o.course_id, o.semester, i.name AS instructor, s.name AS student
FROM offerings o
JOIN course_staff st ON st.course_id = o.course_id AND st.semester = o.semester
JOIN instructors i ON i.id = st.instructor_id
JOIN enrollments e ON e.course_id = o.course_id AND e.semester = o.semester
JOIN students s ON s.id = e.student_id;
```

**Explanation:** Composite keys gate both the staff and enrollment hops; instructors come via staff, students via enrollments.

## Q72: 5-way finance chain: transactions → cards → accounts → customers → regions, with account and customer fields shown.
**Query:**
```sql
SELECT t.id AS tx_id, ac.acct_number, cu.name AS customer, rg.name AS region
FROM transactions t
JOIN cards cd ON cd.id = t.card_id
JOIN accounts ac ON ac.id = cd.account_id
JOIN customers cu ON cu.id = ac.customer_id
JOIN regions rg ON rg.id = cu.region_id;
```

**Explanation:** Five hops along real FKs; column lineage runs strictly left to right, one new table per ON clause.

**Alt1:** Same lineage with the customer's regional lookup spelling out its origin:
```sql
SELECT t.id, ac.acct_number, cu.name, rg.name
FROM regions rg
JOIN customers cu ON cu.region_id = rg.id
JOIN accounts ac ON ac.customer_id = cu.id
JOIN cards cd ON cd.account_id = ac.id
JOIN transactions t ON t.card_id = cd.id
WHERE t.amount > 500;
```

## Q73: Cascade problem: an optional middle table is LEFT but the third is INNER, so rows vanish. Show the broken SQL and the fix.
**Query:**
```sql
SELECT s.name, c.title
FROM students s
LEFT JOIN enrollments e ON e.student_id = s.id
INNER JOIN courses c ON c.id = e.course_id;   -- drops unenrolled students
```

**Alt1 (fixed):**
```sql
SELECT s.name, c.title
FROM students s
LEFT JOIN enrollments e ON e.student_id = s.id
LEFT JOIN courses c ON c.id = e.course_id;
```

**Explanation:** One INNER late in the chain reverses every earlier LEFT that feeds it — mix join types only when the row cutoff is deliberate.

## Q74: Composite-key chain to pricing: order_items → line_details on (order_id, item_seq) → products → current prices.
**Query:**
```sql
SELECT oi.order_id, p.name, ld.promised_date, pl.retail_price
FROM order_items oi
JOIN line_details ld ON ld.order_id = oi.order_id AND ld.item_seq = oi.item_seq
JOIN products p ON p.id = oi.product_id
JOIN price_list pl ON pl.product_id = p.id AND pl.effective_to IS NULL;
```

**Explanation:** One composite registration hop plus two plain lookups; the price hop grabs the "current" row via an open-ended validity flag.

**Alt1:** Pin the price to the exact order date instead of "current":
```sql
SELECT oi.order_id, p.name, pl.retail_price
FROM order_items oi
JOIN products p ON p.id = oi.product_id
JOIN orders o ON o.id = oi.order_id
JOIN price_list pl
  ON pl.product_id = p.id
 AND o.order_date BETWEEN pl.effective_from AND COALESCE(pl.effective_to, o.order_date);
```

## Q75: projects → project_assignments (junction with role attribute) → employees → departments: roster with role per employee.
**Query:**
```sql
SELECT pr.title AS project, pa.role, e.name AS member, d.name AS department
FROM projects pr
JOIN project_assignments pa ON pa.project_id = pr.id
JOIN employees e ON e.id = pa.employee_id
JOIN departments d ON d.id = e.dept_id;
```

**Explanation:** The junction carries its own attribute (role) shown per line; employees and departments resolve that employee's details.
## Q76: Diamond join: students reach a course both via enrollments and via attendance records — two paths to the same fact. Show the explosion and the DISTINCT fix.
**Query:**
```sql
SELECT DISTINCT s.name, c.title
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id
JOIN attendance a ON a.student_id = s.id AND a.course_id = c.id;
```

**Explanation:** The second path to (student, course) multiplies rows for anyone who attended more than once; DISTINCT restores one row per student-course.

## Q77: Junction with a payload: enrollments.grade. One report row = student, course, grade, plus the instructor.
**Query:**
```sql
SELECT s.name AS student, c.title AS course, e.grade, i.name AS instructor
FROM enrollments e
JOIN students s ON s.id = e.student_id
JOIN courses c ON c.id = e.course_id
JOIN instructors i ON i.id = c.instructor_id;
```

**Explanation:** The middle table's extra column (grade) is read straight off the junction row, which the joins never disturb.

## Q78: A shipment has both origin and destination region FKs into the same regions table, plus its warehouse. Resolve both.
**Query:**
```sql
SELECT s.id AS shipment_id, w.name AS warehouse, ro.name AS origin, rd.name AS destination
FROM shipments s
JOIN warehouses w ON w.id = s.warehouse_id
JOIN regions ro ON ro.id = s.origin_region_id
JOIN regions rd ON rd.id = s.dest_region_id;
```

**Explanation:** regions is joined twice — once per role — mapping each FK column to its own aliased row.

## Q79: Multi-tenant schema: every table carries tenant_id, and every join must pin the tenant or rows bleed across tenants.
**Query:**
```sql
SELECT o.id, cu.name
FROM orders o
JOIN customers cu
  ON cu.tenant_id = o.tenant_id AND cu.id = o.customer_id
JOIN regions r
  ON r.tenant_id = o.tenant_id AND r.id = cu.region_id;
```

**Explanation:** The composite ON (tenant_id, business key) gates every hop; dropping tenant_id cross-pollinates unrelated customers.

**Alt1:** Shorten the second hop by joining regions through the already-scoped customer row:
```sql
SELECT o.id, cu.name, rg.name
FROM orders o
JOIN customers cu ON cu.tenant_id = o.tenant_id AND cu.id = o.customer_id
JOIN regions rg ON rg.tenant_id = cu.tenant_id AND rg.id = cu.region_id;
```

## Q80: employees appears in three roles: as the employee, as their manager, and as the department head.
**Query:**
```sql
SELECT e.name AS employee, m.name AS manager, h.name AS dept_head, d.name AS department
FROM employees e
JOIN employees m ON m.id = e.manager_id
JOIN departments d ON d.id = e.dept_id
JOIN employees h ON h.id = d.head_employee_id;
```

**Explanation:** Three aliases of one table serve three distinct FK roles; each ON targets its own column.

## Q81: Non-equi time overlap across a chain: promotions overlapping a campaign window, joined to product and region.
**Query:**
```sql
SELECT p.name AS product, rg.name AS region,
       promo.promo_name, promo.start_day, promo.end_day
FROM promotions promo
JOIN products p ON p.id = promo.product_id
JOIN regions rg ON rg.id = promo.region_id
JOIN campaigns cmp
  ON cmp.region_id = rg.id AND cmp.product_id = p.id
 AND promo.start_day <= cmp.end_day AND promo.end_day >= cmp.start_day;
```

**Explanation:** The campaign hop is legal only when the two date spans intersect — a range join, not a key join.

**Alt1:** Report only fully-conflicting windows (campaign entirely inside a promotion):
```sql
SELECT promo.promo_name, cmp.name AS campaign
FROM promotions promo
JOIN campaigns cmp
  ON cmp.region_id = promo.region_id AND cmp.product_id = promo.product_id
 AND cmp.start_day >= promo.start_day AND cmp.end_day <= promo.end_day;
```

## Q82: Keys with identical names but different meanings: courses.id vs students.id. Show the classic confusion and the fixed version.
**Query:**
```sql
SELECT s.name, c.title
FROM students s
JOIN enrollments e ON e.course_id = s.id   -- BUG: course vs student id
JOIN courses c ON c.id = e.course_id;
```

**Explanation:** `s.id` is a student id but the condition needs the enrollment's course id — same-named `id` columns are not interchangeable.

**Alt1 (fixed):**
```sql
SELECT s.name, c.title
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id;
```

## Q83: Pre-collapse a many side before joining: a derived DISTINCT over instructors-per-course, then attach students.
**Query:**
```sql
SELECT x.course_id, x.instructor_name, s.name AS student
FROM (SELECT DISTINCT c.id AS course_id, i.name AS instructor_name
      FROM courses c JOIN instructors i ON i.id = c.instructor_id) x
JOIN enrollments e ON e.course_id = x.course_id
JOIN students s ON s.id = e.student_id;
```

**Explanation:** Deduplication happens inside the derived table once instead of fanning rows out and deduping after every student line.

**Alt1:** Keep the natural join then dedupe once at the end — same answer, more work:
```sql
SELECT DISTINCT c.id AS course_id, i.name AS instructor_name, s.name AS student
FROM courses c
JOIN instructors i ON i.id = c.instructor_id
JOIN enrollments e ON e.course_id = c.id
JOIN students s ON s.id = e.student_id;
```

## Q84: Fan-out removal: same 4-way query with and without DISTINCT — show what changes.
**Query:**
```sql
SELECT s.name, c.title, i.name
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id
JOIN course_instructors ci ON ci.course_id = c.id
JOIN instructors i ON i.id = ci.instructor_id;
```

**Alt1 (DISTINCT-collapsed):**
```sql
SELECT DISTINCT s.name, c.title, i.name
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id
JOIN course_instructors ci ON ci.course_id = c.id
JOIN instructors i ON i.id = ci.instructor_id;
```

**Explanation:** Without DISTINCT, one row per instructor in a team; with it, the unique fact set — pick DISTINCT only when duplicating rows carry no information.

## Q85: Join-type ordering discipline: run INNER hops before LEFT hops so the LEFT join's NULL preservation actually survives.
**Query:**
```sql
SELECT s.name, c.semester, i.name AS instructor, d.name AS department
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN offerings o ON o.course_id = e.course_id AND o.semester = e.semester
JOIN courses co ON co.id = o.course_id
JOIN instructors i ON i.id = co.instructor_id
LEFT JOIN departments d ON d.id = i.dept_id;
```

**Explanation:** All mandatory hops come first; the single LEFT (department) attaches optional data last so no later INNER can undo it.

**Alt1:** The same joins with the LEFT for department attached directly to courses instead:
```sql
SELECT s.name, c.title, i.name AS instructor, d.name AS department
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id
LEFT JOIN departments d ON d.id = c.dept_id
JOIN instructors i ON i.id = c.instructor_id;
```

## Q86: Six-table star around orders: customer, item lines, product, the sales rep, and the shipper.
**Query:**
```sql
SELECT o.id AS order_id, cu.name AS customer, p.name AS product, oi.quantity,
       r.name AS sales_rep, sh.name AS shipper
FROM orders o
JOIN customers cu ON cu.id = o.customer_id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
JOIN staff r ON r.id = o.rep_id
JOIN shippers sh ON sh.id = o.shipper_id;
```

**Explanation:** orders is the hub; four child/spoke lookups radiate from it and the result has one row per order line.

## Q87: Versioned composite keys with effective dating across three tables (product, version, price) — pick the row valid today per product.
**Query:**
```sql
SELECT p.sku, v.version, pl.retail_price
FROM products p
JOIN product_versions v ON v.product_id = p.id
JOIN price_lists pl
  ON pl.product_id = v.product_id
 AND pl.version = v.version
 AND CURRENT_DATE BETWEEN pl.effective_from AND pl.effective_to;
```

**Explanation:** The third hop is a composite plus range join — it validates both the version and that today falls inside the price window.

**Alt1:** Trim to the latest version per product with a window-free NOT EXISTS guard:
```sql
SELECT p.sku, v.version, pl.retail_price
FROM products p
JOIN product_versions v ON v.product_id = p.id
JOIN price_lists pl ON pl.product_id = v.product_id AND pl.version = v.version
WHERE CURRENT_DATE BETWEEN pl.effective_from AND pl.effective_to
  AND NOT EXISTS (
    SELECT 1 FROM product_versions v2
    WHERE v2.product_id = p.id AND v2.version > v.version);
```

## Q88: Music catalog: artists → albums → tracks → studios → labels (5-way).
**Query:**
```sql
SELECT ar.name AS artist, al.title AS album, t.title AS track,
       s.name AS studio, lb.name AS label
FROM artists ar
JOIN albums al ON al.artist_id = ar.id
JOIN tracks t ON t.album_id = al.id
JOIN studios s ON s.id = t.studio_id
JOIN labels lb ON lb.id = al.label_id;
```

**Explanation:** Two branches off `albums` (a tracks chain and a label single-hop) and one off `tracks` — the aliases keep the branches unambiguous.

## Q89: Two independent paths into the same employees table: the line manager and the department head might be different people.
**Query:**
```sql
SELECT e.name AS employee, m.name AS line_manager, h.name AS dept_head
FROM employees e
JOIN employees m ON m.id = e.manager_id
JOIN departments d ON d.id = e.dept_id
JOIN employees h ON h.id = d.head_employee_id
WHERE m.id <> h.id;
```

**Explanation:** Two different aliases into employees via different routes; the pair is often not the same person, and the WHERE surfaces those cases.

**Alt1:** Same comparison rendered as an asserted column instead of a filter:
```sql
SELECT e.name AS employee,
       CASE WHEN m.id = h.id THEN 'SAME' ELSE 'DIFFERENT' END AS same_person
FROM employees e
JOIN employees m ON m.id = e.manager_id
JOIN departments d ON d.id = e.dept_id
JOIN employees h ON h.id = d.head_employee_id;
```

## Q90: Org chart to three levels, tolerant of gaps at every level, with COALESCE fallbacks for display.
**Query:**
```sql
SELECT e.name AS employee,
       COALESCE(m.name, '(none)') AS manager,
       COALESCE(mm.name, '(none)') AS director
FROM employees e
LEFT JOIN employees m ON m.id = e.manager_id
LEFT JOIN employees mm ON mm.id = m.manager_id;
```

**Explanation:** LEFT at each hop keeps the whole population; COALESCE turns NULLs into readable placeholders without changing the joins.

## Q91: Flights reference the airports table twice (origin, destination) plus their airline: self-join the same table twice.
**Query:**
```sql
SELECT f.flight_no, a.name AS airline, ao.code AS origin, ad.code AS destination
FROM flights f
JOIN airlines a ON a.id = f.airline_id
JOIN airports ao ON ao.id = f.origin_id
JOIN airports ad ON ad.id = f.destination_id;
```

**Explanation:** Two aliases of airports decode each end of the flight; the airline hop is a normal lookup.

**Alt1:** Flag hub-turnaround flights where origin and destination airports coincide:
```sql
SELECT f.flight_no, a.name
FROM flights f
JOIN airlines a ON a.id = f.airline_id
JOIN airports ao ON ao.id = f.origin_id
JOIN airports ad ON ad.id = f.destination_id
WHERE ao.id = ad.id;
```

## Q92: Courses have prerequisites (self-referential) and instructors. Show course, prerequisite, and instructor in one row.
**Query:**
```sql
SELECT c.title AS course, p.title AS prerequisite, i.name AS instructor
FROM courses c
JOIN course_prereqs cp ON cp.course_id = c.id
JOIN courses p ON p.id = cp.prereq_id
JOIN instructors i ON i.id = c.instructor_id;
```

**Explanation:** `courses` is aliased twice — the course itself and its prerequisite — linked through the junction that stores the dependency edges.

## Q93: Find students who share a course with the student named 'Alice', restricted to courses taught by instructor 17 (two junction constraints).
**Query:**
```sql
SELECT DISTINCT s.name
FROM students s
JOIN enrollments e2 ON e2.student_id = s.id
JOIN courses c ON c.id = e2.course_id
JOIN enrollments e1 ON e1.course_id = c.id
JOIN students alice ON alice.id = e1.student_id AND alice.name = 'Alice'
JOIN course_instructors ci ON ci.course_id = c.id AND ci.instructor_id = 17
WHERE s.id <> alice.id;
```

**Explanation:** Two passes over the enrollment junction (one for Alice, one for classmates) plus a junction constraint on instructor 17, all deduped once.

## Q94: Composite plus range on the same table: find the shipping cost effective for a shipment's date and lane.
**Query:**
```sql
SELECT s.id AS shipment_id, l.zones, c.cost
FROM shipments s
JOIN lanes l ON l.warehouse_id = s.warehouse_id AND l.region_id = s.region_id
JOIN lane_costs c
  ON c.lane_id = l.id
 AND s.ship_date BETWEEN c.effective_from AND c.effective_to;
```

**Explanation:** Lane identity is composite (warehouse_id, region_id); cost is versioned by date, so the second hop is composite-lookup plus range-match.

## Q95: Join-time filter (ON) vs post-join filter (WHERE) in a multi-hop LEFT chain — the difference in retained rows.
**Query:**
```sql
SELECT s.name, e.semester
FROM students s
LEFT JOIN enrollments e ON e.student_id = s.id AND e.semester = '2025-Fall'
LEFT JOIN courses c ON c.id = e.course_id;
```

**Alt1:**
```sql
SELECT s.name, e.semester
FROM students s
LEFT JOIN enrollments e ON e.student_id = s.id
LEFT JOIN courses c ON c.id = e.course_id
WHERE e.semester = '2025-Fall';
```

**Explanation:** The ON version keeps every student (semester is just a join predicate); the WHERE version silently drops students with no Fall-2025 enrollment.

## Q96: Two independent many-to-many connections on the same row explode the result. Show the explosion and the intended deduped query.
**Query:**
```sql
SELECT DISTINCT s.name AS student, c.title AS course, i.name AS instructor
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id
JOIN course_instructors ci ON ci.course_id = c.id
JOIN instructors i ON i.id = ci.instructor_id;
```

**Explanation:** Enrollments (student↔course M:N) crossed with instructors (course↔instructor M:N) multiplies on the same course row; DISTINCT is the safety net.

**Alt1:** Pre-collapse the instructor side so the fan-out never happens at all:
```sql
SELECT s.name, c.title, x.instructor
FROM students s
JOIN enrollments e ON e.student_id = s.id
JOIN courses c ON c.id = e.course_id
JOIN (SELECT DISTINCT course_id, name AS instructor
      FROM course_instructors ci JOIN instructors i ON i.id = ci.instructor_id) x
  ON x.course_id = c.id;
```

## Q97: Chain of LEFT joins all the way down, rendering missing values with COALESCE — full reporting view with zero row loss.
**Query:**
```sql
SELECT s.name AS student,
       COALESCE(c.title, '(no course)') AS course,
       COALESCE(i.name, '(no instructor)') AS instructor
FROM students s
LEFT JOIN enrollments e ON e.student_id = s.id
LEFT JOIN courses c ON c.id = e.course_id
LEFT JOIN instructors i ON i.id = c.instructor_id;
```

**Explanation:** Every hop stays LEFT so even a student with no enrollment survives; COALESCE merely dresses NULLs for output.

## Q98: Two junction tables bridging unrelated fact tables: students↔courses via enrollments and courses↔instructors via course_instructors. Produce unique (student, instructor) pairs.
**Query:**
```sql
SELECT DISTINCT st.name AS student, i.name AS instructor
FROM enrollments e
JOIN students st ON st.id = e.student_id
JOIN course_instructors ci ON ci.course_id = e.course_id
JOIN instructors i ON i.id = ci.instructor_id;
```

**Explanation:** The two junctions share `course` as the pivot, forming a 5-table hop from student to instructor; DISTINCT wins the unique pair set.

## Q99: A multi-condition LEFT join carrying an inequality — and an explanation of how many rows it legitimately yields.
**Query:**
```sql
SELECT st.name AS student, a.balance
FROM students st
LEFT JOIN accounts a ON a.student_id = st.id AND a.balance > 1000;
```

**Explanation:** The inequality tags only "high-value" accounts; a student with several qualifying accounts legitimately repeats, one row per account.

**Alt1:** Make repeat rows explicit as a flag instead of accepting the fan-out:
```sql
SELECT st.name,
       CASE WHEN a.id IS NULL THEN 0 ELSE COUNT(a.id) OVER (PARTITION BY st.id) END AS high_balance_accounts
FROM students st
LEFT JOIN accounts a ON a.student_id = st.id AND a.balance > 1000;
```

## Q100: Capstone: 7-table reporting query mixing composite keys, two roles of the same table, and INNER-first-then-LEFT ordering.
**Query:**
```sql
SELECT s.name AS student,
       c.title AS course,
       ti.name AS teacher,
       d.name AS department,
       COALESCE(hi.name, '(vacant)') AS dept_head
FROM students s
JOIN enrollments e
  ON e.student_id = s.id AND e.semester = '2025-Fall'
JOIN offerings o
  ON o.course_id = e.course_id AND o.semester = e.semester
JOIN courses c ON c.id = o.course_id
JOIN departments d ON d.id = c.dept_id
JOIN instructors ti ON ti.id = c.instructor_id
LEFT JOIN instructors hi ON hi.id = d.head_instructor_id;
```

**Explanation:** Composite (course_id, semester) gates both the enrollment and offering hops; all INNERs run before the single LEFT, so NULL preservation is never undone.
