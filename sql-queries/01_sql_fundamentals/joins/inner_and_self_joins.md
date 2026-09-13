# INNER JOIN and SELF JOIN — 100 SQL Interview Q&A

## Q1: Write a query to return each order with its customer name.

**Query:**
```sql
SELECT o.order_id, c.customer_name
FROM orders o
INNER JOIN customers c ON c.customer_id = o.customer_id;
```
**Explanation:** Inner join pairs each order with its matching customer row; only orders that have a customer are returned.

## Q2: Write a query to list every employee together with the name of their department.

**Query:**
```sql
SELECT e.employee_name, d.dept_name
FROM employees e
JOIN departments d ON d.dept_id = e.dept_id;
```
**Explanation:** The `JOIN` keyword defaults to `INNER JOIN`; employees with no department are excluded.

## Q3: Write a query returning each book with its author's name using the shorthand JOIN syntax.

**Query:**
```sql
SELECT b.title, a.name AS author
FROM books b
JOIN authors a ON a.author_id = b.author_id;
```
**Explanation:** Shorthand `JOIN` is equivalent to `INNER JOIN`. Only books tied to an author appear.

## Q4: Write a query to list all enrollments with the student's full name and course title.

**Query:**
```sql
SELECT e.enrollment_id, s.full_name, c.title
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id;
```
**Explanation:** Two separate inner joins chain the enrollment row to both its student and its course.

## Q5: Write a query to show each payment with the invoice number and the customer who must pay it.

**Query:**
```sql
SELECT p.payment_id, i.invoice_no, i.customer_name
FROM payments p
JOIN invoices i ON i.invoice_id = p.invoice_id;
```
**Explanation:** The join key (`invoice_id`) maps each payment to exactly one invoice row.

## Q6: Write a query to return every line item with its product name and quantity.

**Query:**
```sql
SELECT li.order_id, li.quantity, p.product_name
FROM line_items li
JOIN products p ON p.product_id = li.product_id;
```
**Explanation:** The line-item table carries the foreign key `product_id` used to look up product details.

## Q7: Write a query returning each order along with the customer's country.

**Query:**
```sql
SELECT o.order_id, c.country
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;
```
**Explanation:** Column order in the equality (`o.customer_id = c.customer_id`) is irrelevant; the join is symmetric.

## Q8: Write a query to list each flight with the departure airport's city.

**Query:**
```sql
SELECT f.flight_no, a.city AS departure_city
FROM flights f
JOIN airports a ON a.airport_code = f.dep_airport;
```
**Explanation:** The join uses a non-sequential key (a code, not an integer id); both columns must share the same value.

## Q9: Write a query to show each shipment with its warehouse location name.

**Query:**
```sql
SELECT s.shipment_id, w.location_name
FROM shipments s
JOIN warehouses w ON w.warehouse_id = s.warehouse_id;
```
**Explanation:** The foreign key `warehouse_id` in shipments resolves the location from the warehouses dimension table.

## Q10: Write a query to list each employee with their manager's name using a self join on employees.

**Query:**
```sql
SELECT e.employee_name, m.employee_name AS manager_name
FROM employees e
JOIN employees m ON m.employee_id = e.manager_id;
```
**Explanation:** The same table is joined to itself under aliases `e` and `m`; each employee rows matches its manager row.

**Alt1:** Use explicit `INNER JOIN` for clarity:
```sql
SELECT e.employee_name, m.employee_name AS manager_name
FROM employees e
INNER JOIN employees m ON m.employee_id = e.manager_id;
```

## Q11: Write a query to find all pairs of employees who work in the same city (each pair once).

**Query:**
```sql
SELECT a.employee_name AS emp1, b.employee_name AS emp2
FROM employees a
JOIN employees b ON a.city = b.city
WHERE a.employee_id < b.employee_id;
```
**Explanation:** Cross-like self join with the `a.id < b.id` guard prevents self-pairs and duplicate reversed pairs.

**Alt1:** Use `<>` plus a name-ordering guard when no numeric id exists:
```sql
SELECT a.employee_name, b.employee_name
FROM employees a
JOIN employees b ON a.city = b.city AND a.name < b.name;
```

## Q12: Write a query to return each product and a same-priced product (distinct pairs).

**Query:**
```sql
SELECT p1.product_name AS cheaper_or_equal, p2.product_name AS other
FROM products p1
JOIN products p2 ON p1.price = p2.price
WHERE p1.product_id < p2.product_id;
```
**Explanation:** Self join on the non-key column `price` plus an inequality guard yields each matching pair exactly once.

## Q13: Write a query to list all stores that have at least one active order (using a subquery filter with joins).

**Query:**
```sql
SELECT DISTINCT s.store_name
FROM stores s
JOIN orders o ON o.store_id = s.store_id
WHERE o.status = 'ACTIVE';
```
**Explanation:** Inner join plus `DISTINCT` collapses the multiple matching orders to one store row.

## Q14: Write a query to return each customer who has placed an order, using a join with DISTINCT.

**Query:**
```sql
SELECT DISTINCT c.customer_id, c.customer_name
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id;
```
**Explanation:** The inner join already filters customers without orders; `DISTINCT` removes the per-order duplicates.

**Alt1:** Equivalent with `EXISTS` (no duplicate issue at all and often faster):
```sql
SELECT c.customer_id, c.customer_name
FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);
```

## Q15: Write a query to show order IDs that have more than one shipping address on file, revealing address duplicates.

**Query:**
```sql
SELECT DISTINCT a.order_id
FROM addresses a
JOIN addresses a2 ON a.order_id = a2.order_id
WHERE a.address_id <> a2.address_id;
```
**Explanation:** Self join on `order_id` with different address keys finds orders carrying two distinct addresses.

## Q16: Write a query to return employees who earned the same salary as someone else (duplicate salary detection).

**Query:**
```sql
SELECT DISTINCT e.employee_name
FROM employees e
JOIN employees e2 ON e.salary = e2.salary
WHERE e.employee_id <> e2.employee_id;
```
**Explanation:** Matching a non-key column (salary) against a different row flags every employee with a shared value.

**Alt1:** Also show the shared salary:
```sql
SELECT DISTINCT e.salary
FROM employees e
JOIN employees e2 ON e.salary = e2.salary
WHERE e.employee_id <> e2.employee_id;
```

## Q17: Write a query to return cities where two or more employees live (duplicate detection on a column).

**Query:**
```sql
SELECT DISTINCT e.city
FROM employees e
JOIN employees e2 ON e.city = e2.city
WHERE e.employee_id <> e2.employee_id;
```
**Explanation:** Any self-matched pair is proof the value exists at least twice in the table.

## Q18: Write a query to find employees whose city matches their manager's city.

**Query:**
```sql
SELECT e.employee_name
FROM employees e
JOIN employees m ON m.employee_id = e.manager_id
WHERE e.city = m.city;
```
**Explanation:** The self join supplies the manager row; the WHERE clause filters on a column from each side.

## Q19: Write a query to list supplier orders where the billing country differs from the shipping country.

**Query:**
```sql
SELECT o.order_id
FROM orders o
JOIN addresses bill ON bill.order_id = o.order_id AND bill.addr_type = 'BILLING'
JOIN addresses ship ON ship.order_id = o.order_id AND ship.addr_type = 'SHIPPING'
WHERE bill.country <> ship.country;
```
**Explanation:** Two self-ish joins on the same table with role filters materialize both addresses as separate rows.

## Q20: Write a query to return each employee and their direct manager using a table alias and explicit join.

**Query:**
```sql
SELECT e.name AS employee, m.name AS manager
FROM employees AS e
INNER JOIN employees AS m ON m.employee_id = e.manager_id;
```
**Explanation:** Aliases `e`/`m` disambiguate the two copies of the employees table in the same query.

## Q21: Write a query to list order items where a product was reordered by the same customer in another order.

**Query:**
```sql
SELECT DISTINCT o1.customer_id
FROM orders o1
JOIN order_items oi1 ON oi1.order_id = o1.order_id
JOIN order_items oi2 ON oi2.product_id = oi1.product_id
JOIN orders o2 ON o2.order_id = oi2.order_id
WHERE o2.order_id <> o1.order_id;
```
**Explanation:** Item and order self joins trace the same product back to a different order for the same customer.

## Q22: Write a query that uses an implicit (comma) join to list employees with their departments.

**Query:**
```sql
SELECT e.employee_name, d.dept_name
FROM employees e, departments d
WHERE e.dept_id = d.dept_id;
```
**Explanation:** Theta-style join: comma separates tables and the join condition lives in WHERE; works but is easy to get wrong.

## Q23: Write the same employee–department query using an explicit INNER JOIN, and explain why it is preferred.

**Query:**
```sql
SELECT e.employee_name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id;
```
**Explanation:** Explicit joins keep the join condition next to the join, prevent accidental cross joins, and are clearer to read.

## Q24: Write a query to find the third-level relationship: employees and their manager's name only for departments in 'Sales' or 'Marketing'.

**Query:**
```sql
SELECT e.employee_name, m.employee_name AS manager
FROM employees e
JOIN employees m ON m.employee_id = e.manager_id
JOIN departments d ON d.dept_id = e.dept_id
WHERE d.dept_name IN ('Sales', 'Marketing');
```
**Explanation:** The two joins (self for manager, dept for department) are followed by a WHERE filter on the department side.

## Q25: Write a query to return each part with its currently listed supplier, using a composite key join.

**Query:**
```sql
SELECT p.part_no, s.supplier_name
FROM parts p
JOIN suppliers s ON s.supplier_id = p.supplier_id AND s.active = 1;
```
**Explanation:** The ON clause combines the key match with a row-level condition, reducing the supplier candidates before matching.

## Q26: Write a query to return order rows only for customers present in the customers table.

**Query:**
```sql
SELECT o.* FROM orders o
JOIN customers c ON c.customer_id = o.customer_id;
```
**Explanation:** Inner join inherently drops orders whose `customer_id` has no matching customers row.

**Alt1:** Same result with the condition folded into WHERE:
```sql
SELECT o.* FROM orders o, customers c
WHERE c.customer_id = o.customer_id;
```

## Q27: Write a query to return orders placed on the same date as another order (non-key column join).

**Query:**
```sql
SELECT DISTINCT o1.order_id
FROM orders o1
JOIN orders o2 ON o1.order_date = o2.order_date
WHERE o1.order_id <> o2.order_id;
```
**Explanation:** Self join on a non-key column (`order_date`) with a key inequality isolates shared-date orders.

## Q28: Write a query listing all customers and the single most relevant contact, using a join to a filtered subquery.

**Query:**
```sql
SELECT c.customer_name, t.phone
FROM customers c
JOIN (SELECT MIN(contact_id) AS contact_id FROM contacts GROUP BY customer_id) best
  ON best.customer_id = c.customer_id
JOIN contacts t ON t.contact_id = best.contact_id;
```
**Explanation:** A derived table pre-selects one contact per customer, then joins it back to pull the phone number.

## Q29: Write a query to return employees hired after their manager was hired (row-to-row comparison).

**Query:**
```sql
SELECT e.employee_name, e.hire_date, m.hire_date AS manager_hired
FROM employees e
JOIN employees m ON m.employee_id = e.manager_id
WHERE e.hire_date > m.hire_date;
```
**Explanation:** Columns from both alias copies of the table are compared in WHERE after the self join pairs them.

## Q30: Write a query to find products that cost more than a same-category product.

**Query:**
```sql
SELECT DISTINCT p1.product_name
FROM products p1
JOIN products p2 ON p1.category_id = p2.category_id
WHERE p1.product_id <> p2.product_id AND p1.price > p2.price;
```
**Explanation:** Self join groups products by category; the WHERE compares prices between the two copies.

## Q31: Write a query that returns each team member and their teammate's name within the same team.

**Query:**
```sql
SELECT m1.member_name AS member, m2.member_name AS teammate
FROM team_members m1
JOIN team_members m2 ON m1.team_id = m2.team_id
WHERE m1.member_id < m2.member_id;
```
**Explanation:** Self join on team plus an ordering guard yields unordered teammate pairs without self-pairs.

## Q32: Write a query to return orders whose region matches the customer's region, joining with a condition in ON.

**Query:**
```sql
SELECT o.order_id
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id AND c.tier = o.order_tier;
```
**Explanation:** Placing the extra equality in ON both filters and matches in one step, keeping WHERE for unrelated filters.

## Q33: Write a query listing each movie along with any movie sharing its release year.

**Query:**
```sql
SELECT m1.title AS movie, m2.title AS same_year
FROM movies m1
JOIN movies m2 ON m1.release_year = m2.release_year
WHERE m1.movie_id <> m2.movie_id;
```
**Explanation:** Non-key self join; the inequality keeps each row from pairing with itself.

## Q34: Write a query to return managers who manage at least two people (without aggregate functions).

**Query:**
```sql
SELECT DISTINCT m.employee_id, m.employee_name
FROM employees m
JOIN employees e ON e.manager_id = m.employee_id
JOIN employees e2 ON e2.manager_id = m.employee_id
WHERE e2.employee_id <> e.employee_id;
```
**Explanation:** Each manager is self-joined to two distinct reports, proving two or more direct subordinates exist.

**Alt1:** Count-based equivalent that is simpler but uses GROUP BY (aggregation covered elsewhere):
```sql
SELECT m.employee_name
FROM employees m
JOIN employees e ON e.manager_id = m.employee_id
GROUP BY m.employee_id, m.employee_name
HAVING COUNT(*) >= 2;
```

## Q35: Write a query to find duplicate email addresses among users using a self join.

**Query:**
```sql
SELECT DISTINCT u1.email
FROM users u1
JOIN users u2 ON u1.email = u2.email
WHERE u1.user_id <> u2.user_id;
```
**Explanation:** Any email joining to a different user_id is duplicated; DISTINCT prints each duplicate email once.

## Q36: Write a query to return each row of a survey where the respondent gave the same answer to two questions.

**Query:**
```sql
SELECT DISTINCT s1.respondent_id
FROM survey_answers s1
JOIN survey_answers s2 ON s1.respondent_id = s2.respondent_id
WHERE s1.question_id <> s2.question_id AND s1.answer = s2.answer;
```
**Explanation:** The self join pairs answers of one respondent; filtering on different questions with equal answers finds the pattern.

## Q37: Write a query to list parts whose primary part number matches another part's cross-reference number.

**Query:**
```sql
SELECT p1.part_no
FROM parts p1
JOIN part_xref x ON x.cross_ref_no = p1.part_no;
```
**Explanation:** The join key is a column (`part_no`) on one side and a cross-reference column on the other — still just an equality.

## Q38: Write a query that returns each employee's boss, and shows employees who are also managers by joining to the same table.

**Query:**
```sql
SELECT e.employee_name,
       m.employee_name AS boss,
       mm.employee_name AS boss_of_boss
FROM employees e
JOIN employees m ON m.employee_id = e.manager_id
JOIN employees mm ON mm.employee_id = m.manager_id;
```
**Explanation:** Two chained self joins climb two levels of the hierarchy in a single query.

## Q39: Write a query to return orders shipped to a state where no warehouse exists (join eliminating unmatched then outer check is left for another file — here use join + NOT IN is forbidden, so filter via join).

**Query:**
```sql
SELECT DISTINCT o.order_id
FROM orders o
JOIN warehouses w ON w.state = o.ship_state;
```
**Explanation:** Because warehouses are unique per state, the inner join simply keeps orders whose ship state has a warehouse.

## Q40: Write a query to list employees whose first name matches their manager's first name.

**Query:**
```sql
SELECT e.employee_name
FROM employees e
JOIN employees m ON m.employee_id = e.manager_id
WHERE e.first_name = m.first_name;
```
**Explanation:** A non-key name column from both alias copies is compared after the self join.

**Alt1:** Same using a name-prefix partial match:
```sql
SELECT e.employee_name
FROM employees e
JOIN employees m ON m.employee_id = e.manager_id
WHERE LEFT(e.first_name, 1) = LEFT(m.first_name, 1);
```

## Q41: Write a query to return advertisements that ran on the same channel as another ad (pair detection).

**Query:**
```sql
SELECT a1.ad_title AS ad_a, a2.ad_title AS ad_b
FROM ads a1
JOIN ads a2 ON a1.channel_id = a2.channel_id
WHERE a1.ad_id < a2.ad_id;
```
**Explanation:** Self join on channel plus the id guard returns each channel-sharing pair exactly once.

## Q42: Write a query to return films that share at least one actor, using distinct film pairs.

**Query:**
```sql
SELECT DISTINCT f1.film_id, f2.film_id
FROM film_roles f1
JOIN film_roles f2 ON f1.actor_id = f2.actor_id
JOIN films film1 ON film1.film_id = f1.film_id
JOIN films film2 ON film2.film_id = f2.film_id
WHERE f1.film_id < f2.film_id;
```
**Explanation:** Cast membership self join plus films join expands common-actor pairs; `<` guard and DISTINCT clean the output.

## Q43: Write a query to return each employee together with a derived table counting their orders, but only keep employees with orders (join to subquery).

**Query:**
```sql
SELECT e.employee_name, t.order_count
FROM employees e
JOIN (SELECT sales_rep_id, COUNT(*) AS order_count
      FROM orders GROUP BY sales_rep_id) t
  ON t.sales_rep_id = e.employee_id;
```
**Explanation:** The pre-aggregated derived table is joined to employees; employees with zero orders never match and drop out.

## Q44: Write a query to find tags that appear on more than one article using a self join on the article_tags link table.

**Query:**
```sql
SELECT DISTINCT t1.tag_id
FROM article_tags t1
JOIN article_tags t2 ON t1.tag_id = t2.tag_id
WHERE t1.article_id <> t2.article_id;
```
**Explanation:** Self join on the link table proves one tag is attached to two different articles.

## Q45: Write the explicit INNER JOIN version of "each student and their advisor" where advisor is also a student.

**Query:**
```sql
SELECT s.student_name, a.student_name AS advisor
FROM students s
INNER JOIN students a ON a.student_id = s.advisor_id;
```
**Explanation:** A self-referencing relation (advisor_id) is resolved through two aliases of the same table.

## Q46: Write a query to return products that appear in two different categories (odd? no — their category history) — use a join to the product_category_history twice.

**Query:**
```sql
SELECT DISTINCT p.product_id
FROM product_category_history c1
JOIN product_category_history c2 ON c1.product_id = c2.product_id
JOIN products p ON p.product_id = c1.product_id
WHERE c1.category_id <> c2.category_id;
```
**Explanation:** History self join on the product key, with different category ids, detects products that ever switched categories.

## Q47: Write a query to list nodes that are children of the same parent, returned as parent-child-child pairs.

**Query:**
```sql
SELECT p.node_name AS parent,
       c1.node_name AS child_a,
       c2.node_name AS child_b
FROM nodes p
JOIN nodes c1 ON c1.parent_id = p.node_id
JOIN nodes c2 ON c2.parent_id = p.node_id
WHERE c1.node_id < c2.node_id;
```
**Explanation:** Two self joins fan out each parent to a pair of its children; the guard avoids duplicate pairs.

## Q48: Write a query that pairs each adventure trip with another trip using the same difficulty rating.

**Query:**
```sql
SELECT t1.trip_name AS trip, t2.trip_name AS similar
FROM trips t1
JOIN trips t2 ON t1.difficulty = t2.difficulty
WHERE t1.trip_id < t2.trip_id;
```
**Explanation:** Self join on the `difficulty` attribute with an id guard enumerates distinct trip pairs.

## Q49: Write a query to return orders and their customers using a join on the natural key `customer_code` rather than the surrogate id.

**Query:**
```sql
SELECT o.order_id, c.customer_name
FROM orders o
JOIN customers c ON c.customer_code = o.customer_code;
```
**Explanation:** Natural keys can act as join keys; ensure they are unique per row to avoid fan-out duplicates.

## Q50: Write a query to return employees who share the same last name, materialized as distinct pairs.

**Query:**
```sql
SELECT a.employee_name AS emp_a, b.employee_name AS emp_b
FROM employees a
JOIN employees b ON a.last_name = b.last_name
WHERE a.employee_id < b.employee_id;
```
**Explanation:** The guarded self join on `last_name` yields each same-last-name pair once, ordered and without self rows.

## Q51: Write a query to return each ingredient used by a dish and the ingredient's supplier region.

**Query:**
```sql
SELECT d.dish_name, i.ingredient_name, sup.region
FROM dishes d
JOIN recipe_items ri ON ri.dish_id = d.dish_id
JOIN ingredients i ON i.ingredient_id = ri.ingredient_id
JOIN suppliers sup ON sup.supplier_id = i.supplier_id;
```
**Explanation:** Three inner joins traverse the chain dish → recipe item → ingredient → supplier, each on its foreign key.

## Q52: Write a query to detect duplicate product codes where codes differ only by case.

**Query:**
```sql
SELECT DISTINCT p1.product_code
FROM products p1
JOIN products p2 ON UPPER(p1.product_code) = UPPER(p2.product_code)
WHERE p1.product_id <> p2.product_id;
```
**Explanation:** Normalizing both sides with UPPER before the equality catches case-insensitive duplicates in one join.

**Alt1:** PostgreSQL `LOWER` variant of the same idea:
```sql
SELECT DISTINCT p1.product_code
FROM products p1
JOIN products p2 ON LOWER(p1.product_code) = LOWER(p2.product_code)
WHERE p1.product_id <> p2.product_id;
```

## Q53: Write a query returning network edges from the `connections` table with both endpoint names.

**Query:**
```sql
SELECT c.connection_id,
       u1.user_name AS user_a,
       u2.user_name AS user_b
FROM connections c
JOIN users u1 ON u1.user_id = c.user_a
JOIN users u2 ON u2.user_id = c.user_b;
```
**Explanation:** Two joins resolve both endpoint ids of each edge row into display names from the same users table.

## Q54: Write a query to list employees whose manager works in a different country.

**Query:**
```sql
SELECT e.employee_name
FROM employees e
JOIN employees m ON m.employee_id = e.manager_id
WHERE e.country <> m.country;
```
**Explanation:** After the self join, the WHERE compares country columns belonging to the two alias copies.

## Q55: Write a query to return jobs and the recruiter handles, pairing each job with a recruiter through a join table.

**Query:**
```sql
SELECT j.job_title, r.recruiter_name
FROM jobs j
JOIN job_assignments ja ON ja.job_id = j.job_id
JOIN recruiters r ON r.recruiter_id = ja.recruiter_id;
```
**Explanation:** The link table `job_assignments` is joined twice: once toward jobs, once toward recruiters.

## Q56: Write a query to list articles whose headline contains a keyword that appears in another article's tags.

**Query:**
```sql
SELECT DISTINCT a.article_id
FROM articles a
JOIN article_tags t ON t.article_id = a.article_id
JOIN articles a2 ON a2.title LIKE '%' || t.tag_name || '%';
```
**Explanation:** A LIKE-based join on a non-key column matches articles whose title contains a sibling article's tag.

**Alt1:** MySQL uses `CONCAT` instead of the `||` operator:
```sql
SELECT DISTINCT a.article_id
FROM articles a
JOIN article_tags t ON t.article_id = a.article_id
JOIN articles a2 ON a2.title LIKE CONCAT('%', t.tag_name, '%');
```

## Q57: Write a query to return version rows that share a document but conflict in revision order (rows relate to rows).

**Query:**
```sql
SELECT DISTINCT v1.document_id
FROM document_versions v1
JOIN document_versions v2 ON v1.document_id = v2.document_id
WHERE v1.revision_no <> v2.revision_no;
```
**Explanation:** Self join on the document key paired with different revision numbers flags documents with multiple revisions.

## Q58: Write a query listing teachers and, for each teacher, another teacher sharing the same subject department.

**Query:**
```sql
SELECT t1.teacher_name AS teacher, t2.teacher_name AS colleague
FROM teachers t1
JOIN teachers t2 ON t1.department = t2.department
WHERE t1.teacher_id < t2.teacher_id;
```
**Explanation:** The department self join with the id guard produces unique colleague pairs within each department.

## Q59: Write a query to find orders placed on the same day by the same customer, as distinct pairs.

**Query:**
```sql
SELECT a.order_id AS order_a, b.order_id AS order_b
FROM orders a
JOIN orders b ON a.customer_id = b.customer_id
             AND a.order_date = b.order_date
WHERE a.order_id < b.order_id;
```
**Explanation:** A compound ON condition matches rows on both keys while the WHERE guard kills self and mirrored pairs.

## Q60: Write a query returning bank transfers where the receiving account is also the sender of another transfer.

**Query:**
```sql
SELECT DISTINCT t1.transfer_id
FROM transfers t1
JOIN transfers t2 ON t2.from_account = t1.to_account;
```
**Explanation:** The join links a transfer to another whose source account is this transfer's destination.

## Q61: Write a query to return the raw material name and the supplier's status, but only for supplies in stock.

**Query:**
```sql
SELECT rm.material_name, s.status
FROM raw_materials rm
JOIN stock st ON st.material_id = rm.material_id
JOIN suppliers s ON s.supplier_id = rm.supplier_id
WHERE st.qty_on_hand > 0;
```
**Explanation:** Joins resolve both dimensions; the WHERE filter on the stock side trims depletable rows.

## Q62: Write a query to list employees whose phone number prefix matches their own office extension (self-ish join on derived columns).

**Query:**
```sql
SELECT DISTINCT e.employee_name
FROM employees e
JOIN offices o ON o.employee_id = e.employee_id
WHERE LEFT(e.phone, 3) = EXTRACT('hour', o.opened_at); 
```
**Explanation:** A column from each joined side is passed through an expression before comparison; hard-coding is avoided.

## Q63: Write a query returning customers who have shipped to both the 'EAST' and 'WEST' regions using two joins with DISTINCT.

**Query:**
```sql
SELECT DISTINCT c.customer_name
FROM customers c
JOIN shipments se ON se.customer_id = c.customer_id AND se.region = 'EAST'
JOIN shipments sw ON sw.customer_id = c.customer_id AND sw.region = 'WEST';
```
**Explanation:** Two inner joins to the same table with region filters force the customer to satisfy both regions at once.

## Q64: Write a query to return employee pairs where one earns within 10% of the other.

**Query:**
```sql
SELECT a.employee_name, b.employee_name
FROM employees a
JOIN employees b ON a.salary BETWEEN b.salary * 0.9 AND b.salary * 1.1
WHERE a.employee_id < b.employee_id;
```
**Explanation:** A range condition in ON pairs comparable salaries; the guard prevents self-pairs and duplicates.

## Q65: Write a query to find products whose unit price is duplicated in the catalog (value appears on two rows).

**Query:**
```sql
SELECT DISTINCT p1.unit_price
FROM products p1
JOIN products p2 ON p1.unit_price = p2.unit_price
WHERE p1.product_id <> p2.product_id;
```
**Explanation:** The non-key price self join surfaces any price stored on two or more different products.

## Q66: Write a query to list each attendee and their plus-one as stored in the reservations table.

**Query:**
```sql
SELECT a.attendee_name, p.attendee_name AS plus_one
FROM attendees a
JOIN attendees p ON p.attendee_id = a.plus_one_id;
```
**Explanation:** `plus_one_id` references another row of the same table, resolved through a basic two-alias self join.

## Q67: Write a query returning pairs of airports connected by a direct route, showing both airport names.

**Query:**
```sql
SELECT a1.city AS origin, a2.city AS destination
FROM routes r
JOIN airports a1 ON a1.airport_code = r.origin_code
JOIN airports a2 ON a2.airport_code = r.dest_code;
```
**Explanation:** Each route id is resolved to two airport names through separate joins, like an edge-to-nodes pattern.

## Q68: Write a query to return employees in overlapping time zones? Not needed — return employees whose manager was hired in the same month as them.

**Query:**
```sql
SELECT e.employee_name
FROM employees e
JOIN employees m ON m.employee_id = e.manager_id
WHERE DATE_FORMAT(e.hire_date, '%Y-%m') = DATE_FORMAT(m.hire_date, '%Y-%m');
```
**Explanation:** Date formatting normalizes both hire dates to month granularity before comparing them.

**Alt1:** PostgreSQL equivalent truncates the date directly:
```sql
SELECT e.employee_name
FROM employees e
JOIN employees m ON m.employee_id = e.manager_id
WHERE date_trunc('month', e.hire_date) = date_trunc('month', m.hire_date);
```

## Q69: Write a query to find orders where the billing customer differs from the shipping customer.

**Query:**
```sql
SELECT o1.order_id
FROM orders o1
JOIN orders o2 ON o1.order_id = o2.order_id
JOIN order_addresses ba ON ba.order_id = o1.order_id AND ba.kind = 'BILL'
JOIN order_addresses sa ON sa.order_id = o1.order_id AND sa.kind = 'SHIP'
WHERE ba.customer_id <> sa.customer_id;
```
**Explanation:** Two role-filtered joins materialize billing and shipping customers independently for comparison.

## Q70: Write a query to list courses a student can take because they completed their prerequisite (prereq is another course row).

**Query:**
```sql
SELECT DISTINCT c.course_title
FROM courses c
JOIN prerequisites pr ON pr.course_id = c.course_id
JOIN completions cp ON cp.course_id = pr.prereq_course_id
JOIN students s ON s.student_id = cp.student_id
WHERE s.student_id = 42;
```
**Explanation:** Chain joins from course → prerequisite → completion proves the prereq was finished before allowing the course.

## Q71: Write a query listing tracks that belong to the same genre and appear within 30 seconds duration of each other.

**Query:**
```sql
SELECT t1.title AS track_a, t2.title AS track_b
FROM tracks t1
JOIN tracks t2 ON t1.genre_id = t2.genre_id
              AND ABS(t1.duration_sec - t2.duration_sec) <= 30
WHERE t1.track_id < t2.track_id;
```
**Explanation:** A compound ON pairs by genre and duration proximity, while the guard prevents self-pairs.

## Q72: Write a query to return companies that share a domain name with another company.

**Query:**
```sql
SELECT DISTINCT c1.company_name
FROM companies c1
JOIN companies c2 ON SUBSTRING_INDEX(c1.website, '.', -1) = SUBSTRING_INDEX(c2.website, '.', -1)
WHERE c1.company_id <> c2.company_id;
```
**Explanation:** Both websites are reduced to their TLD before the equality, finding same-TLD companies.

**Alt1:** PostgreSQL split-part variant:
```sql
SELECT DISTINCT c1.company_name
FROM companies c1
JOIN companies c2 ON SPLIT_PART(c1.website, '.', 2) = SPLIT_PART(c2.website, '.', 2)
WHERE c1.company_id <> c2.company_id;
```

## Q73: Write a query returning each checklist item with its parent checklist item's name (single-level hierarchy).

**Query:**
```sql
SELECT i.item_name AS task, p.item_name AS parent_task
FROM checklist_items i
JOIN checklist_items p ON p.item_id = i.parent_id;
```
**Explanation:** A `parent_id` column pointing at the same table resolves one level of hierarchy via self join.

## Q74: Write a query to count cities containing at least two customers by returning each such city once.

**Query:**
```sql
SELECT DISTINCT c1.city
FROM customers c1
JOIN customers c2 ON c1.city = c2.city
WHERE c1.customer_id <> c2.customer_id;
```
**Explanation:** The non-key city self join returns every customer pair; DISTINCT collapses them to the qualifying cities.

## Q75: Write a query to return SKUs that map to the same barcode using an inner join on product variants.

**Query:**
```sql
SELECT DISTINCT v1.sku
FROM product_variants v1
JOIN product_variants v2 ON v1.barcode = v2.barcode
WHERE v1.variant_id <> v2.variant_id;
```
**Explanation:** Barcode equality against a different variant id reveals barcodes reused across SKUs.

## Q76: Write a query returning session pairs where one session's room is another session's feed region is not a thing — instead return sessions whose facilitator also facilitated a different session in the same track.

**Query:**
```sql
SELECT s1.session_title
FROM sessions s1
JOIN sessions s2 ON s1.track_id = s2.track_id
                AND s1.facilitator_id = s2.facilitator_id
WHERE s1.session_id <> s2.session_id;
```
**Explanation:** Compound ON matches on both track and facilitator; the inequality proves two distinct sessions.

## Q77: Write a query to find defects and their parent defects in a single-level defect tree.

**Query:**
```sql
SELECT d.defect_code AS defect, p.defect_code AS parent_defect
FROM defects d
JOIN defects p ON p.defect_id = d.parent_defect_id;
```
**Explanation:** The self-referencing `parent_defect_id` climbs one level of the defect hierarchy.

**Alt1:** Show only root children where the parent itself has no parent:
```sql
SELECT d.defect_code
FROM defects d
JOIN defects p ON p.defect_id = d.parent_defect_id
LEFT JOIN defects pp ON pp.defect_id = p.parent_defect_id
WHERE pp.defect_id IS NULL;
```

## Q78: Write a query to return doctors and the doctors who referred patients to them, using the referrals table twice.

**Query:**
```sql
SELECT r.referring_doctor_id, target.doctor_name AS target, referrer.doctor_name AS referred_by
FROM referrals r
JOIN doctors target ON target.doctor_id = r.referring_doctor_id
JOIN doctors referrer ON referrer.doctor_id = r.referral_source_id;
```
**Explanation:** Two joins interpret both ids of each referral row through the doctors table.

## Q79: Write a query to detect rows in a dedup log where a record was inserted and deleted, i.e. two events for the same entity.

**Query:**
```sql
SELECT DISTINCT i.entity_id
FROM audit_log i
JOIN audit_log d ON d.entity_id = i.entity_id
WHERE i.action = 'INSERT' AND d.action = 'DELETE';
```
**Explanation:** Self join on entity_id filtered to differing action types surfaces entities with both events.

**Alt1:** Guarded against the same-row edge case by adding key inequality:
```sql
SELECT DISTINCT i.entity_id
FROM audit_log i
JOIN audit_log d ON d.entity_id = i.entity_id AND d.log_id <> i.log_id
WHERE i.action = 'INSERT' AND d.action = 'DELETE';
```

## Q80: Write a query to list mentors and mentees from a mentor_map where every row is a mentor-mentee link.

**Query:**
```sql
SELECT m.mentor_name, t.mentee_name
FROM mentor_map mm
JOIN people m ON m.person_id = mm.mentor_id
JOIN people t ON t.person_id = mm.mentee_id;
```
**Explanation:** The link table fans out to two role-joined copies of the people table.

## Q81: Write a query returning employees at the same job level who report up the same chain one level (shared direct manager).

**Query:**
```sql
SELECT e1.employee_name AS emp_a, e2.employee_name AS emp_b, m.employee_name AS manager
FROM employees e1
JOIN employees e2 ON e1.manager_id = e2.manager_id
JOIN employees m ON m.employee_id = e1.manager_id
WHERE e1.employee_id < e2.employee_id;
```
**Explanation:** Self join on `manager_id` plus a third alias for the manager names every pair of coworkers.

## Q82: Write a query to find zip codes shared by customers in different states.

**Query:**
```sql
SELECT DISTINCT c1.zip
FROM customers c1
JOIN customers c2 ON c1.zip = c2.zip
WHERE c1.state <> c2.state;
```
**Explanation:** Self join on zip comparing state columns across copies flags cross-state zips.

## Q83: Write a query that returns, for a chess tournament, players who faced each other more than once.

**Query:**
```sql
SELECT DISTINCT g1.player_a, g1.player_b
FROM games g1
JOIN games g2 ON g1.player_a = g2.player_a AND g1.player_b = g2.player_b
WHERE g1.game_id <> g2.game_id;
```
**Explanation:** Compound join on the full pair of players with key inequality detects repeated matchups.

## Q84: Write a query to return invoices where the total as recomputed from line items disagrees, keeping only matched invoices and items.

**Query:**
```sql
SELECT DISTINCT i.invoice_id
FROM invoices i
JOIN invoice_lines il ON il.invoice_id = i.invoice_id
JOIN invoice_lines il2 ON il.invoice_id = i.invoice_id
WHERE il.line_no <> il2.line_no
  AND il.qty * il.unit_price + il2.qty * il2.unit_price <> i.total;
```
**Explanation:** A joined duplicates tricks the recompute; conceptually use single line scan — the self join just requires two distinct lines to flag mismatch.

## Q85: Write a query to pair each product with a competitor product at the same price point (banded).

**Query:**
```sql
SELECT p1.product_name, p2.product_name AS competitor
FROM products p1
JOIN products p2 ON p2.price = p1.price AND p1.brand <> p2.brand
WHERE p1.product_id < p2.product_id;
```
**Explanation:** Price equality plus different brand filters out same-brand rows while the guard dedupes pairs.

## Q86: Write a query to list branches tied to the same franchise group.

**Query:**
```sql
SELECT b1.branch_name AS branch, b2.branch_name AS sibling
FROM branches b1
JOIN branches b2 ON b1.franchise_id = b2.franchise_id
WHERE b1.branch_id < b2.branch_id;
```
**Explanation:** Franchise-key self join with ordering guard enumerates sibling pairs within each group.

## Q87: Write a query to return customers whose primary contact and backup contact have the same phone number.

**Query:**
```sql
SELECT c.customer_id
FROM customers c
JOIN contacts primary_cont ON primary_cont.contact_id = c.primary_contact_id
JOIN contacts backup_cont ON backup_cont.contact_id = c.backup_contact_id
WHERE primary_cont.phone = backup_cont.phone;
```
**Explanation:** Two joins load both contacts of each customer; the WHERE compares phone columns across the two copies.

## Q88: Write a query to find tournaments in which the same pair of players faced each other under reversed seating.

**Query:**
```sql
SELECT DISTINCT g1.tournament_id
FROM games g1
JOIN games g2 ON g1.player_a = g2.player_b AND g1.player_b = g2.player_a
WHERE g1.tournament_id = g2.tournament_id;
```
**Explanation:** The join condition flips the roles, matching a game to its mirrored rematch in the same tournament.

## Q89: Write a query that returns employees older than the employee who hired them (a compare on the same table).

**Query:**
```sql
SELECT e.employee_name
FROM employees e
JOIN employees h ON h.employee_id = e.hired_by_employee_id
WHERE e.birth_date < h.birth_date;
```
**Explanation:** A custom `hired_by_employee_id` foreign key plus an age-direction comparison in WHERE.

## Q90: Write a query to return dataset rows that are exact duplicates on (a, b) with a self join.

**Query:**
```sql
SELECT DISTINCT r1.row_id
FROM raw_rows r1
JOIN raw_rows r2 ON r1.a = r2.a AND r1.b = r2.b
WHERE r1.row_id <> r2.row_id;
```
**Explanation:** Compound equality on the key columns plus key inequality flags any row sharing an (a, b) tuple.

## Q91: Write a query to pair each order with the previous order number of the same customer without window functions — force with a self join on order numbering.

**Query:**
```sql
SELECT o1.order_id, o2.order_id AS prior_order
FROM orders o1
JOIN orders o2 ON o2.customer_id = o1.customer_id
              AND o2.order_seq < o1.order_seq
WHERE o2.order_seq = (SELECT MAX(o3.order_seq) FROM orders o3
                      WHERE o3.customer_id = o1.customer_id
                        AND o3.order_seq < o1.order_seq);
```
**Explanation:** A self join supplies candidate priors and a correlated MAX keeps only the immediately preceding order.

## Q92: Write a query to find parts that are components of a part that is itself a component (level-two composition).

**Query:**
```sql
SELECT c1.component_part_id
FROM bill_of_materials c1
JOIN bill_of_materials c2 ON c2.assembly_part_id = c1.component_part_id;
```
**Explanation:** Joining the BOM to itself moves one level deeper: c1's component is c2's assembly.

## Q93: Write a query returning duplicate newsletter subscriptions by (subscriber_id, list_id) pairs.

**Query:**
```sql
SELECT DISTINCT s1.subscriber_id, s1.list_id
FROM subscriptions s1
JOIN subscriptions s2 ON s1.subscriber_id = s2.subscriber_id
                      AND s1.list_id = s2.list_id
WHERE s1.subscription_id <> s2.subscription_id;
```
**Explanation:** Compound equality on the natural pair with key inequality identifies duplicated subscriptions.

## Q94: Write a query to return flights where the arriving aircraft is later (same tail number) outbound to a different city.

**Query:**
```sql
SELECT DISTINCT f1.flight_id
FROM flights f1
JOIN flights f2 ON f2.tail_number = f1.tail_number
WHERE f2.departs_after = f1.arrives_at
  AND f2.route != f1.route;
```
**Explanation:** The self join matches on equipment and connectivity; the WHERE excludes same-route turnarounds.

## Q95: Write a query to list calls between employees where both are in different floors.

**Query:**
```sql
SELECT DISTINCT c.call_id
FROM calls c
JOIN employees a ON a.employee_id = c.caller_id
JOIN employees b ON b.employee_id = c.callee_id
WHERE a.floor <> b.floor;
```
**Explanation:** Two joins fetch both participants; the floor comparison discards same-floor calls.

## Q96: Write a query to return meal combos sharing two or more identical ingredients using two chained self joins.

**Query:**
```sql
SELECT DISTINCT m1.combo_id AS combo_a, m2.combo_id AS combo_b
FROM combo_ingredients m1
JOIN combo_ingredients m2 ON m2.combo_id <> m1.combo_id
                         AND m2.ingredient_id = m1.ingredient_id
JOIN combo_ingredients m3 ON m3.combo_id = m2.combo_id
                         AND m3.ingredient_id <> m1.ingredient_id
WHERE m3.ingredient_id = m1.ingredient_id;
```
**Explanation:** Two self joins prove combo_b shares ingredient with combo_a via two separate rows, forcing more than one shared item.

## Q97: Write a query to find category values that appear both as a parent and as a child in one level.

**Query:**
```sql
SELECT DISTINCT p.parent_category_id
FROM categories p
JOIN categories c ON c.parent_category_id = p.parent_category_id
WHERE p.category_id = c.parent_category_id;
```
**Explanation:** Joining parent ids to child parent-ids exposes values used in both roles simultaneously.

## Q98: Write a query to return employees whose name string is a prefix of their manager's name.

**Query:**
```sql
SELECT e.employee_name
FROM employees e
JOIN employees m ON m.employee_id = e.manager_id
WHERE m.name LIKE e.name || '%';
```
**Explanation:** The LIKE pattern is built from the joined employee's name to test the manager's name for the prefix.

**Alt1:** PostgreSQL LEFT()-based equivalent:
```sql
SELECT e.employee_name
FROM employees e
JOIN employees m ON m.employee_id = e.manager_id
WHERE LEFT(m.name, LENGTH(e.name)) = e.name;
```

## Q99: Write a query to detect cities recorded twice in a geolocation table under different names.

**Query:**
```sql
SELECT DISTINCT g1.lat, g1.lng
FROM geo g1
JOIN geo g2 ON g1.lat = g2.lat AND g1.lng = g2.lng
WHERE UPPER(g1.city_name) <> UPPER(g2.city_name);
```
**Explanation:** Coordinate equality combined with differing city names across copies reveals duplicates.

## Q100: Write a query that returns each category and its subcategories (single level) along with products per subcategory, by joining categories to itself then to products.

**Query:**
```sql
SELECT parent.category_name AS category,
       child.category_name AS subcategory,
       p.product_name
FROM categories parent
JOIN categories child ON child.parent_id = parent.category_id
JOIN products p ON p.category_id = child.category_id;
```
**Explanation:** The parent-child category self join, then a product join on the child key, yields the two-level rollup in one query.
