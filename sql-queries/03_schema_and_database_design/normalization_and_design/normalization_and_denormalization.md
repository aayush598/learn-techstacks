# Normalization and Schema Design — 100 SQL Interview Q&A

## Q1: What is database normalization and why is it important?

**Answer:**
Normalization is the process of organizing a relational database to reduce redundancy and improve data integrity. It involves decomposing tables into smaller, well-structured tables linked by relationships. This prevents update, insertion, and deletion anomalies and ensures that each fact is stored in exactly one place.

```sql
-- Unnormalized: everything in one table
CREATE TABLE orders_flat (
    order_id INT,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    product_name VARCHAR(100),
    product_price DECIMAL(10,2),
    order_date DATE
);

-- Normalized: customers and products separated
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    product_id INT REFERENCES products(product_id),
    order_date DATE
);
```

## Q2: Explain First Normal Form (1NF) with an example.

**Answer:**
1NF requires that every column contains only atomic (indivisible) values and that there are no repeating groups. Each row must be unique, identified by a primary key. A table violates 1NF if a column stores a comma-separated list or an array of values.

```sql
-- Violates 1NF: hobbies column has multiple values
CREATE TABLE persons_bad (
    person_id INT PRIMARY KEY,
    name VARCHAR(100),
    hobbies VARCHAR(500)  -- 'reading,swimming,coding'
);

-- 1NF-compliant: one hobby per row
CREATE TABLE persons (
    person_id INT,
    name VARCHAR(100),
    hobby VARCHAR(100),
    PRIMARY KEY (person_id, hobby)
);
```

**Variant:** Some DBMS allow array columns (e.g., PostgreSQL), but they still violate 1NF. Normalize on read:

```sql
-- PostgreSQL unnest of a 1NF-violating array
SELECT student_id, unnest(courses) AS course
FROM students;

-- Enforce atomicity at write time if keeping the array
CREATE TABLE students_ok (
    student_id INT PRIMARY KEY,
    name VARCHAR(100)
);
CREATE TABLE student_course (
    student_id INT,
    course VARCHAR(100),
    PRIMARY KEY (student_id, course)
);
```

## Q3: What is a repeating group and how do you eliminate it?

**Answer:**
A repeating group is a set of columns that store multiple values of the same type for a single entity, such as `phone1`, `phone2`, `phone3`. Eliminate it by moving the repeating values into a separate table with a foreign key back to the original entity.

```sql
-- Repeating group
CREATE TABLE employees_bad (
    emp_id INT PRIMARY KEY,
    name VARCHAR(100),
    skill1 VARCHAR(50),
    skill2 VARCHAR(50),
    skill3 VARCHAR(50)
);

-- Eliminated: separate table
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE employee_skills (
    emp_id INT REFERENCES employees(emp_id),
    skill VARCHAR(50),
    PRIMARY KEY (emp_id, skill)
);
```

## Q4: Explain Second Normal Form (2NF).

**Answer:**
2NF requires the table to be in 1NF and that every non-key column is fully functionally dependent on the entire primary key. This matters only when the primary key is composite. If a non-key attribute depends on only part of the composite key, it violates 2NF and should be moved to a separate table.

```sql
-- Violates 2NF: student_name depends only on student_id, not (student_id, course_id)
CREATE TABLE enrollments_bad (
    student_id INT,
    course_id INT,
    student_name VARCHAR(100),   -- partial dependency
    enrollment_date DATE,
    PRIMARY KEY (student_id, course_id)
);

-- 2NF-compliant
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE enrollments (
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
```

**Variant:** Detect a partial dependency in an existing table before refactoring:

```sql
-- If this query returns rows, student_name is NOT fully dependent on the PK
SELECT student_id, COUNT(DISTINCT student_name) AS name_count
FROM enrollments
GROUP BY student_id
HAVING COUNT(DISTINCT student_name) > 1;
```

## Q5: What is a partial dependency?

**Answer:**
A partial dependency occurs when a non-key attribute depends on only a portion of a composite primary key rather than the whole key. For example, if the PK is `(student_id, course_id)` and `student_name` depends only on `student_id`, that is a partial dependency. 2NF eliminates all partial dependencies.

```sql
-- Partial dependency example
-- PK: (student_id, course_id)
-- student_name → student_id (only part of PK) — VIOLATION
-- grade → (student_id, course_id) — OK

-- Fix: move student_name to a students table
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100)
);

CREATE TABLE grades (
    student_id INT,
    course_id INT,
    grade CHAR(2),
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
```

## Q6: Explain Third Normal Form (3NF) with an example.

**Answer:**
3NF requires the table to be in 2NF and that no non-key attribute transitively depends on the primary key. In other words, every non-key attribute must depend directly on the key, not on another non-key attribute. If `order_id → customer_id → customer_city`, then `customer_city` transitively depends on `order_id` and should be moved to a customers table.

```sql
-- Violates 3NF: city depends on zip_code, not directly on order_id
CREATE TABLE orders_bad (
    order_id INT PRIMARY KEY,
    customer_id INT,
    zip_code VARCHAR(10),
    city VARCHAR(100)  -- transitive: order_id → zip_code → city
);

-- 3NF-compliant
CREATE TABLE zip_codes (
    zip_code VARCHAR(10) PRIMARY KEY,
    city VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    zip_code VARCHAR(10),
    FOREIGN KEY (zip_code) REFERENCES zip_codes(zip_code)
);
```

## Q7: What is a transitive dependency?

**Answer:**
A transitive dependency is an indirect functional dependency where `A → B → C`, meaning `C` depends on `A` through `B`. In a table with key `A`, if a non-key column `C` is determined by another non-key column `B` rather than directly by `A`, that is transitive. 3NF removes transitive dependencies by placing `B` and `C` in their own table.

```sql
-- Transitive dependency: emp_id → dept_id → dept_name
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(100),
    dept_id INT,
    dept_name VARCHAR(100)  -- depends on dept_id, not emp_id
);

-- Decomposed to remove transitive dependency
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(100)
);

CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(100),
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);
```

## Q8: What is Boyce-Codd Normal Form (BCNF)?

**Answer:**
BCNF is a stricter version of 3NF. A table is in BCNF if for every non-trivial functional dependency `X → Y`, `X` is a superkey. The difference from 3NF is that 3NF allows `Y` to be a prime attribute even if `X` is not a superkey; BCNF does not. BCNF eliminates all anomalies arising from functional dependencies.

```sql
-- Example: teacher teaches subject, subject has one teacher
-- Dependencies: (teacher, subject) → room; teacher → subject
-- teacher is NOT a superkey, so not BCNF

-- BCNF decomposition
CREATE TABLE teacher_subject (
    teacher VARCHAR(100) PRIMARY KEY,
    subject VARCHAR(100)
);

CREATE TABLE teacher_room (
    teacher VARCHAR(100),
    subject VARCHAR(100),
    room VARCHAR(50),
    PRIMARY KEY (teacher, subject),
    FOREIGN KEY (teacher) REFERENCES teacher_subject(teacher)
);
```

## Q9: Give an example where 3NF and BCNF differ.

**Answer:**
Consider a table with attributes `(student, subject, professor)` where each professor teaches only one subject, but a subject can be taught by multiple professors, and each student takes one professor per subject. The dependency `professor → subject` holds, but `professor` is not a superkey. This satisfies 3NF (subject is prime) but violates BCNF.

```sql
-- Original: (student, subject, professor)
-- FDs: (student, subject) → professor; professor → subject
-- professor is not a superkey → violates BCNF

-- BCNF decomposition
CREATE TABLE prof_subject (
    professor VARCHAR(100) PRIMARY KEY,
    subject VARCHAR(100)
);

CREATE TABLE student_prof (
    student VARCHAR(100),
    subject VARCHAR(100),
    professor VARCHAR(100),
    PRIMARY KEY (student, subject),
    FOREIGN KEY (professor) REFERENCES prof_subject(professor)
);
```

## Q10: What is Fourth Normal Form (4NF)?

**Answer:**
4NF addresses multi-valued dependencies. A table is in 4NF if it is in BCNF and has no non-trivial multi-valued dependencies. A multi-valued dependency `X →→ Y` means that for each value of `X`, there is a set of values of `Y` independent of other attributes. The fix is to decompose into separate tables for each independent multi-valued fact.

```sql
-- Violates 4NF: two independent multi-valued facts
CREATE TABLE teacher_courses_books (
    teacher VARCHAR(100),
    course VARCHAR(100),
    book VARCHAR(100),
    PRIMARY KEY (teacher, course, book)
);
-- teacher →→ course and teacher →→ book are independent MVDs

-- 4NF decomposition
CREATE TABLE teacher_courses (
    teacher VARCHAR(100),
    course VARCHAR(100),
    PRIMARY KEY (teacher, course)
);

CREATE TABLE teacher_books (
    teacher VARCHAR(100),
    book VARCHAR(100),
    PRIMARY KEY (teacher, book)
);
```

**Variant:** Verify a 4NF problem with sample data before decomposing (e.g., the same course and book rows repeat for every book — a red flag):

```sql
-- Given rows: ('Mr. X','Math','B1'), ('Mr. X','Math','B2'),
-- ('Mr. X','Physics','B1'), ('Mr. X','Physics','B2')
-- The course and book sets are independent → split into two tables
SELECT teacher, course, COUNT(*) AS rows_per_course
FROM teacher_courses_books
GROUP BY teacher, course;
-- A 4NF anomaly shows up as cartesian blow-up, not a FK violation
```

## Q11: What is Fifth Normal Form (5NF)?

**Answer:**
5NF, also called Project-Join Normal Form (PJ/NF), deals with join dependencies. A table is in 5NF if every join dependency is implied by the candidate keys. In practice, 5NF addresses cases where a table can be losslessly decomposed into three or more smaller tables but not into two. It is rarely encountered in real-world design.

```sql
-- 5NF example: a sales agent can sell certain products for certain companies
-- The triples (agent, product, company) can be decomposed but pairs cannot

CREATE TABLE agent_product (
    agent_id INT,
    product_id INT,
    PRIMARY KEY (agent_id, product_id)
);

CREATE TABLE agent_company (
    agent_id INT,
    company_id INT,
    PRIMARY KEY (agent_id, company_id)
);

CREATE TABLE product_company (
    product_id INT,
    company_id INT,
    PRIMARY KEY (product_id, company_id)
);

-- The original relationship is reconstructed by joining all three
-- SELECT * FROM agent_product
-- JOIN agent_company USING (agent_id)
-- JOIN product_company USING (product_id);
```

## Q12: What is a functional dependency?

**Answer:**
A functional dependency (FD) `X → Y` means that for every pair of rows with the same value of `X`, they must also have the same value of `Y`. In other words, `X` uniquely determines `Y`. FDs are the foundation of normalization theory; they are used to identify keys, check normal forms, and decompose tables.

```sql
-- If every customer has exactly one city:
-- customer_id → city

-- We can verify FDs with queries:
SELECT customer_id, city
FROM customers
GROUP BY customer_id, city
HAVING COUNT(DISTINCT city) > 1;
-- If this returns rows, customer_id → city is violated
```

**Variant:** The same check inverted to assert that an FD *holds*:

```sql
SELECT CASE WHEN COUNT(*) = 0 THEN 'HOLDS' ELSE 'VIOLATED' END AS status
FROM (
    SELECT customer_id
    FROM customers
    GROUP BY customer_id
    HAVING COUNT(DISTINCT city) > 1
) v;
```

## Q13: How do you find all functional dependencies from a sample dataset?

**Answer:**
To discover FDs from data, group by each attribute (or set of attributes) and check whether it uniquely determines other attributes. In practice, you test every candidate determinant by grouping on it and counting distinct values of each dependent attribute. If the count is always 1 for every group, the FD holds.

```sql
-- Test if department_id → department_name
SELECT department_id, COUNT(DISTINCT department_name) AS name_count
FROM employees
GROUP BY department_id
HAVING COUNT(DISTINCT department_name) > 1;
-- If no rows returned, department_id → department_name holds

-- Automated: test single-column determinant → every other column
-- (repeat for each candidate determinant column)
SELECT 'department_id → department_name' AS fd_test,
    CASE WHEN COUNT(*) = 0 THEN 'HOLDS' ELSE 'VIOLATED' END AS status
FROM (
    SELECT department_id
    FROM employees
    GROUP BY department_id
    HAVING COUNT(DISTINCT department_name) > 1
) v;
```

## Q14: What is a candidate key?

**Answer:**
A candidate key is a minimal set of attributes that uniquely identifies every row in a table. Minimal means no proper subset of the candidate key can serve as a unique identifier. A table can have multiple candidate keys; one is chosen as the primary key, and the others become alternate keys.

```sql
CREATE TABLE users (
    user_id INT,
    email VARCHAR(200),
    username VARCHAR(50),
    -- Three candidate keys:
    CONSTRAINT pk_users PRIMARY KEY (user_id),
    CONSTRAINT uq_email UNIQUE (email),
    CONSTRAINT uq_username UNIQUE (username)
);
```

**Variant:** Find candidate keys programmatically by testing every single column as a determinant:

```sql
SELECT 'user_id' AS determinant,
       COUNT(*) - COUNT(DISTINCT user_id) AS not_unique
FROM users
UNION ALL
SELECT 'email', COUNT(*) - COUNT(DISTINCT email) FROM users
UNION ALL
SELECT 'username', COUNT(*) - COUNT(DISTINCT username) FROM users;
-- Any row with not_unique = 0 is a single-attribute superkey
```

## Q15: How do you find all candidate keys of a table given its data?

**Answer:**
To find candidate keys, first identify attributes that appear in no FD right-hand side (these must be in every key). Then test combinations of remaining attributes to see which subsets uniquely determine all columns. In practice, test whether the combination has a unique value per row using `COUNT(DISTINCT ...)` or `GROUP BY`.

```sql
-- Step 1: Find attributes never on the right side of any FD (key candidates)
-- Step 2: Test if (attr1) determines all columns
SELECT COUNT(*) - COUNT(DISTINCT attr1 || '-' || attr2 || '-' || attr3) AS dupes
FROM my_table;
-- If dupes = 0, {attr1} is a candidate key

-- For composite key candidates, test:
SELECT attr1, attr2
FROM my_table
GROUP BY attr1, attr2
HAVING COUNT(*) > 1;
-- If no rows, (attr1, attr2) is a candidate key (if minimal)
```

## Q16: What is a superkey vs. a candidate key vs. a primary key?

**Answer:**
A **superkey** is any set of attributes that uniquely identifies rows (may include extra attributes). A **candidate key** is a minimal superkey (no subset is also a superkey). A **primary key** is the candidate key chosen by the designer to be the main identifier. Alternate keys are the remaining candidate keys, typically constrained with `UNIQUE`.

```sql
CREATE TABLE employees (
    emp_id INT,
    ssn VARCHAR(12),
    email VARCHAR(200),
    emp_code VARCHAR(10),
    -- Superkeys include: {emp_id, ssn}, {emp_id, email, ssn}, etc.
    -- Candidate keys: {emp_id}, {ssn}, {email}
    -- Primary key chosen:
    CONSTRAINT pk_emp PRIMARY KEY (emp_id),
    -- Alternate keys:
    CONSTRAINT uq_ssn UNIQUE (ssn),
    CONSTRAINT uq_email UNIQUE (email)
);
```

## Q17: Explain surrogate keys vs. natural keys. When would you use each?

**Answer:**
A **surrogate key** is an artificially generated identifier (e.g., auto-increment or UUID) with no business meaning. A **natural key** is an attribute that already uniquely identifies the entity (e.g., SSN, ISBN). Surrogate keys are preferred when natural keys are wide, mutable, or composite. Natural keys are preferred when they are stable, short, and meaningful.

```sql
-- Natural key approach
CREATE TABLE countries_natural (
    iso_code CHAR(2) PRIMARY KEY,  -- natural key
    name VARCHAR(100) NOT NULL
);

-- Surrogate key approach
CREATE TABLE countries_surrogate (
    country_id SERIAL PRIMARY KEY,   -- surrogate
    iso_code CHAR(2) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL
);

-- Use surrogate when natural key changes:
-- e.g., company changes its tax ID — surrogate key stays stable
```

**Alt1:** PostgreSQL identity columns (standard, recommended) vs. MySQL `AUTO_INCREMENT`:

```sql
-- PostgreSQL
CREATE TABLE customers (
    customer_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email VARCHAR(200) UNIQUE
);

-- MySQL
CREATE TABLE customers (
    customer_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(200) UNIQUE
);
```

## Q18: What are insert, update, and delete anomalies?

**Answer:**
**Insert anomaly**: you cannot insert data about an entity without unrelated data (e.g., can't add a department without an employee). **Update anomaly**: changing one fact requires updating multiple rows, risking inconsistency. **Delete anomaly**: deleting a row unintentionally loses unrelated data. Normalization eliminates these by separating entities into distinct tables.

```sql
-- Anomaly example: departments stored with employees
CREATE TABLE emp_dept_bad (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100),
    dept_id INT,
    dept_name VARCHAR(100)
);

-- Insert anomaly: can't store a new department with no employees yet
INSERT INTO emp_dept_bad (emp_id, emp_name, dept_id, dept_name)
VALUES (NULL, NULL, 10, 'Research');  -- emp_id can't be NULL

-- Fix: separate tables
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(100)
);
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100),
    dept_id INT REFERENCES departments(dept_id)
);
-- Now you can insert a department without an employee
INSERT INTO departments VALUES (10, 'Research');
```

## Q19: How do you identify the normal form of an existing table?

**Answer:**
To determine the normal form: (1) List all FDs from the schema and data. (2) Find candidate keys. (3) Check 1NF: are all values atomic? (4) Check 2NF: is there any partial dependency on composite keys? (5) Check 3NF: is there any transitive dependency? (6) Check BCNF: is every determinant a superkey?

```sql
-- Check 1NF: look for multi-valued columns
SELECT order_id, LENGTH(tags) - LENGTH(REPLACE(tags, ',', '')) + 1 AS value_count
FROM orders
WHERE tags LIKE '%,%';
-- If any count > 1, the table is not in 1NF

-- Check for partial dependencies: test each non-key column
-- against subsets of the composite PK
SELECT student_id, COUNT(DISTINCT student_name)
FROM enrollments
GROUP BY student_id
HAVING COUNT(DISTINCT student_name) > 1;
-- If returns rows, student_name depends on only part of the PK
```

## Q20: What is a lossless (lossless-join) decomposition?

**Answer:**
A lossless decomposition is one where the original table can be exactly reconstructed by joining the decomposed tables without producing spurious (extra) rows. A decomposition of `R` into `R1` and `R2` is lossless if the intersection of their attributes is a superkey of at least one of them: `R1 ∩ R2 → R1` or `R1 ∩ R2 → R2`.

```sql
-- Original table
CREATE TABLE enrollment (
    student_id INT,
    course_id INT,
    instructor VARCHAR(100),
    grade CHAR(2),
    PRIMARY KEY (student_id, course_id)
);

-- Lossless decomposition (common attribute is student_id, which is part of PK in both)
CREATE TABLE student_courses (
    student_id INT,
    course_id INT,
    grade CHAR(2),
    PRIMARY KEY (student_id, course_id)
);

CREATE TABLE course_instructor (
    course_id INT PRIMARY KEY,
    instructor VARCHAR(100)
);

-- Reconstruction (lossless):
-- SELECT s.student_id, s.course_id, c.instructor, s.grade
-- FROM student_courses s
-- JOIN course_instructor c ON s.course_id = c.course_id;
```

**Variant:** Verify losslessness with a duplicate-free reconstruction in one query:

```sql
SELECT COUNT(*) AS extra_rows
FROM (
    SELECT s.student_id, s.course_id, c.instructor, s.grade
    FROM student_courses s
    JOIN course_instructor c ON s.course_id = c.course_id
    EXCEPT
    SELECT student_id, course_id, instructor, grade FROM enrollment
) diff;
-- 0 rows means nothing spurious was introduced
```

## Q21: What is a dependency-preserving decomposition?

**Answer:**
A dependency-preserving decomposition is one where all original functional dependencies can be enforced by checking constraints on the individual decomposed tables, without needing to join them. This is desirable but not always achievable, especially when decomposing to BCNF. You can verify dependency preservation by checking that the closure of the union of FDs from each fragment equals the original FD closure.

```sql
-- Original with FDs: A → B, B → C
CREATE TABLE abc (
    A INT PRIMARY KEY,
    B INT,
    C INT
);

-- Decompose:
CREATE TABLE ab (
    A INT PRIMARY KEY,
    B INT
);

CREATE TABLE bc (
    B INT PRIMARY KEY,
    C INT
);

-- FD A → B is preserved in table ab
-- FD B → C is preserved in table bc
-- Both FDs can be enforced independently → dependency-preserving

-- To verify: check if constraints hold
SELECT CASE WHEN COUNT(*) = 0 THEN 'A → B holds' ELSE 'VIOLATED' END
FROM (SELECT A, COUNT(DISTINCT B) c FROM ab GROUP BY A HAVING COUNT(DISTINCT B) > 1) t;
```

## Q22: Given a table with FDs A→B, B→C, C→D, what is the candidate key and what normal form is it in?

**Answer:**
The only candidate key is `{A}`, because `A → B → C → D` means `A` determines all attributes. The table is in 2NF (no partial dependency since the key is single-attribute), but not in 3NF because `A → C` is transitive through `B`, and `A → D` is transitive through `B → C`. To reach 3NF, decompose into `(A,B)`, `(B,C)`, and `(C,D)`.

```sql
-- Decompose to 3NF
CREATE TABLE ab (
    A INT PRIMARY KEY,
    B INT
);

CREATE TABLE bc (
    B INT PRIMARY KEY,
    C INT
);

CREATE TABLE cd (
    C INT PRIMARY KEY,
    D INT
);

-- Verify reconstruction:
-- SELECT ab.A, ab.B, bc.C, cd.D
-- FROM ab
-- JOIN bc ON ab.B = bc.B
-- JOIN cd ON bc.C = cd.C;
```

## Q23: Decompose the following into 2NF: R(A,B,C,D,E) with PK(A,B), FDs: A→C, (A,B)→D, B→E.

**Answer:**
`A→C` is a partial dependency (C depends on only A, not the full PK). `B→E` is also a partial dependency (E depends on only B). Only `D` depends on the full key. Decompose into three tables: `AC(A,C)`, `BE(B,E)`, and `ABD(A,B,D)`.

```sql
CREATE TABLE ac (
    A INT,
    C INT,
    PRIMARY KEY (A)
);

CREATE TABLE be (
    B INT,
    E INT,
    PRIMARY KEY (B)
);

CREATE TABLE abd (
    A INT,
    B INT,
    D INT,
    PRIMARY KEY (A, B),
    FOREIGN KEY (A) REFERENCES ac(A),
    FOREIGN KEY (B) REFERENCES be(B)
);
```

## Q24: What is the difference between 3NF and BCNF in simple terms?

**Answer:**
In 3NF, a non-key attribute can determine another non-key attribute if that other attribute is prime (part of a candidate key). In BCNF, every determinant—regardless of whether the dependent is prime or not—must be a superkey. BCNF is strictly stronger; every BCNF table is in 3NF, but not vice versa.

```sql
-- Example that is 3NF but not BCNF
-- Table R(beer, manufacturer, beer_type)
-- FDs: (beer, manufacturer) → beer_type; manufacturer → beer_type
-- manufacturer is not a superkey → not BCNF
-- But beer_type is prime → satisfies 3NF

-- BCNF decomposition
CREATE TABLE manufacturer_type (
    manufacturer VARCHAR(100) PRIMARY KEY,
    beer_type VARCHAR(100)
);

CREATE TABLE beer_mfg (
    beer VARCHAR(100),
    manufacturer VARCHAR(100),
    PRIMARY KEY (beer, manufacturer),
    FOREIGN KEY (manufacturer) REFERENCES manufacturer_type(manufacturer)
);
```

## Q25: How do you check if a decomposition is lossless using SQL?

**Answer:**
You can check if a decomposition is lossless by performing a natural join on the decomposed tables and comparing the row count with the original. If the join produces no spurious rows (row count matches and all original data is recoverable), the decomposition is lossless.

```sql
-- Decompose R(A,B,C) into R1(A,B) and R2(B,C)
-- Lossless check: join R1 and R2 on B

-- Count rows in original
SELECT COUNT(*) AS original_count FROM original_table;

-- Count rows in reconstructed view
SELECT COUNT(*) AS reconstructed_count
FROM r1
JOIN r2 ON r1.B = r2.B;

-- If counts match AND no duplicates introduced, it's likely lossless
-- More precise check:
SELECT COUNT(*) AS spurious_rows
FROM r1 JOIN r2 ON r1.B = r2.B
LEFT JOIN original_table o ON r1.A = o.A AND r1.B = o.B AND r2.C = o.C
WHERE o.A IS NULL;
-- If spurious_rows = 0, the decomposition is lossless
```

**Variant:** Compare row counts instead when you trust the natural join:

```sql
SELECT
    (SELECT COUNT(*) FROM original_table) AS original_rows,
    (SELECT COUNT(*) FROM r1 JOIN r2 ON r1.B = r2.B) AS joined_rows;
-- If equal AND no NULL keys in B, decomposition is very likely lossless
```

## Q26: Normalize an orders table from UNF to 3NF. The raw table has: order_id, customer_name, customer_city, product1, qty1, product2, qty2.

**Answer:**
The table violates 1NF (repeating product/qty columns). First, eliminate repeating groups. Then remove partial dependencies (customer_name, customer_city depend only on customer). Finally, remove transitive dependencies if any remain.

```sql
-- UNF raw table
CREATE TABLE orders_unf (
    order_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_city VARCHAR(100),
    product1 VARCHAR(100),
    qty1 INT,
    product2 VARCHAR(100),
    qty2 INT
);

-- 1NF: flatten repeating groups
CREATE TABLE orders_1nf (
    order_id INT,
    product_name VARCHAR(100),
    quantity INT,
    customer_name VARCHAR(100),
    customer_city VARCHAR(100),
    PRIMARY KEY (order_id, product_name)
);

-- 2NF: remove partial dependencies (customer info depends only on order_id)
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(100)
);

CREATE TABLE orders_2nf (
    order_id INT PRIMARY KEY,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items_2nf (
    order_id INT,
    product_name VARCHAR(100),
    quantity INT,
    PRIMARY KEY (order_id, product_name),
    FOREIGN KEY (order_id) REFERENCES orders_2nf(order_id)
);

-- 3NF: if city determines state/zip, extract further
-- Assuming no further transitive dependencies, 2NF = 3NF here
```

## Q27: Write a denormalized reporting table that precomputes monthly sales totals per product.

**Answer:**
Denormalization for read-heavy reporting creates precomputed aggregate tables that avoid expensive GROUP BY queries at read time. You trade write performance for read performance by materializing summaries.

```sql
CREATE TABLE monthly_sales_report (
    report_month DATE NOT NULL,
    product_id INT NOT NULL,
    product_name VARCHAR(100),
    total_quantity INT,
    total_revenue DECIMAL(12,2),
    avg_unit_price DECIMAL(10,2),
    order_count INT,
    PRIMARY KEY (report_month, product_id)
);

-- Populate with aggregated data
INSERT INTO monthly_sales_report
SELECT
    DATE_TRUNC('month', o.order_date) AS report_month,
    p.product_id,
    p.name,
    SUM(oi.quantity),
    SUM(oi.quantity * oi.unit_price),
    AVG(oi.unit_price),
    COUNT(DISTINCT o.order_id)
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY DATE_TRUNC('month', o.order_date), p.product_id, p.name;
```

## Q28: Explain the star schema and when to use it.

**Answer:**
A star schema places a central fact table surrounded by dimension tables. The fact table contains numeric measures and foreign keys to dimensions. Dimension tables contain descriptive attributes. It is optimized for analytical queries (OLAP) because it minimizes joins and is intuitive for business users.

```sql
-- Fact table
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    product_key INT REFERENCES dim_product(product_key),
    customer_key INT REFERENCES dim_customer(customer_key),
    store_key INT REFERENCES dim_store(store_key),
    quantity INT,
    revenue DECIMAL(12,2),
    cost DECIMAL(12,2)
);

-- Dimension tables
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    day_of_week VARCHAR(10)
);

CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_name VARCHAR(200),
    category VARCHAR(100),
    brand VARCHAR(100)
);

CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY,
    customer_name VARCHAR(200),
    segment VARCHAR(50),
    city VARCHAR(100),
    country VARCHAR(100)
);

CREATE TABLE dim_store (
    store_key INT PRIMARY KEY,
    store_name VARCHAR(200),
    region VARCHAR(100),
    manager VARCHAR(100)
);
```

**Variant:** A star schema can also handle multi-valued facts with a fact-per-grain design:

```sql
-- One fact row per product line, not per order
CREATE TABLE fact_sales_lines (
    order_id BIGINT,
    product_key INT REFERENCES dim_product(product_key),
    customer_key INT REFERENCES dim_customer(customer_key),
    date_key INT REFERENCES dim_date(date_key),
    quantity INT,
    line_total DECIMAL(12,2),
    PRIMARY KEY (order_id, product_key)
);
```

## Q29: What is the difference between a star schema and a snowflake schema?

**Answer:**
In a star schema, dimension tables are denormalized (flat). In a snowflake schema, dimension tables are normalized into sub-dimension tables. Snowflake saves storage but requires more joins. Star is preferred for query performance and simplicity in OLAP. Snowflake is preferred when storage is expensive or dimensions have deep hierarchies.

```sql
-- Star schema: flat dimension
CREATE TABLE dim_product_star (
    product_key INT PRIMARY KEY,
    product_name VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100)
);

-- Snowflake schema: normalized dimensions
CREATE TABLE dim_category (
    category_key INT PRIMARY KEY,
    category_name VARCHAR(100)
);

CREATE TABLE dim_subcategory (
    subcategory_key INT PRIMARY KEY,
    subcategory_name VARCHAR(100),
    category_key INT REFERENCES dim_category(category_key)
);

CREATE TABLE dim_brand (
    brand_key INT PRIMARY KEY,
    brand_name VARCHAR(100)
);

CREATE TABLE dim_product_snowflake (
    product_key INT PRIMARY KEY,
    product_name VARCHAR(200),
    subcategory_key INT REFERENCES dim_subcategory(subcategory_key),
    brand_key INT REFERENCES dim_brand(brand_key)
);
```

## Q30: What are fact tables and dimension tables?

**Answer:**
**Fact tables** store measurable, quantitative data (metrics/measures) at a specific grain, along with foreign keys to dimension tables. **Dimension tables** store descriptive, categorical attributes that provide context for the facts. Facts are typically numeric and additive; dimensions are typically text and used for filtering/grouping.

```sql
-- Fact table: one row per line item
CREATE TABLE fact_orders (
    order_line_id BIGINT PRIMARY KEY,
    order_date_key INT,
    product_key INT,
    customer_key INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    discount DECIMAL(5,2),
    total_amount DECIMAL(12,2)
);

-- Dimension: product
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    sku VARCHAR(50),
    product_name VARCHAR(200),
    category VARCHAR(100),
    unit_cost DECIMAL(10,2)
);

-- Dimension: customer
CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY,
    name VARCHAR(200),
    email VARCHAR(200),
    segment VARCHAR(50),
    region VARCHAR(100)
);
```

## Q31: Design a junction table for a many-to-many relationship between students and courses. What redundancy checks apply?

**Answer:**
A junction (bridge/associative) table resolves M:N relationships by holding foreign keys to both entities. The composite of the two foreign keys should be the primary key to prevent duplicate associations. Redundancy checks ensure no duplicate pairs and optionally track relationship attributes.

```sql
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    title VARCHAR(200)
);

-- Junction table with relationship attributes
CREATE TABLE enrollments (
    student_id INT,
    course_id INT,
    enrolled_date DATE DEFAULT CURRENT_DATE,
    grade CHAR(2),
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- Redundancy check: find duplicate enrollments
SELECT student_id, course_id, COUNT(*) AS dup_count
FROM enrollments
GROUP BY student_id, course_id
HAVING COUNT(*) > 1;

-- Check for students enrolled in the same course with different grades
SELECT student_id, course_id, COUNT(DISTINCT grade) AS grade_variants
FROM enrollments
GROUP BY student_id, course_id
HAVING COUNT(DISTINCT grade) > 1;
```

## Q32: When should you denormalize a database, and what trade-offs are involved?

**Answer:**
Denormalize when read performance is critical and joins are expensive (reporting dashboards, high-traffic OLTP reads, data warehousing). Trade-offs: increased storage, slower writes (must maintain redundancy), and risk of inconsistency if updates are not carefully managed. Always measure query performance before and after.

```sql
-- Example: add customer_name to orders for faster reads
-- Normalized: JOIN required
SELECT o.order_id, c.name, o.total
FROM orders o JOIN customers c ON o.customer_id = c.id;

-- Denormalized: add customer_name directly to orders
ALTER TABLE orders ADD COLUMN customer_name VARCHAR(100);

-- Must maintain consistency on customer name change:
CREATE TRIGGER trg_sync_customer_name
AFTER UPDATE OF name ON customers
FOR EACH ROW
BEGIN
    UPDATE orders SET customer_name = NEW.name WHERE customer_id = NEW.id;
END;
```

**Alt1:** For read-heavy analytics, consider a materialized view instead of physical denormalization:

```sql
-- PostgreSQL materialized view
CREATE MATERIALIZED VIEW mv_order_summary AS
SELECT o.order_id, c.name AS customer_name,
       SUM(oi.quantity * oi.price) AS total
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, c.name;

-- Refresh periodically
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_order_summary;
```

## Q33: What are slowly changing dimensions (SCD) and explain Type 2.

**Answer:**
SCDs handle how dimension attribute changes over time. **Type 2** preserves history by adding a new row for each change, with `valid_from`, `valid_to`, and an `is_current` flag. The original row is marked as expired. This allows historical fact rows to reference the correct version of the dimension.

```sql
CREATE TABLE dim_customer_scd2 (
    customer_sk SERIAL PRIMARY KEY,
    customer_id INT,
    name VARCHAR(200),
    city VARCHAR(100),
    valid_from DATE NOT NULL,
    valid_to DATE,
    is_current BOOLEAN DEFAULT TRUE
);

-- Insert initial version
INSERT INTO dim_customer_scd2 (customer_id, name, city, valid_from, valid_to, is_current)
VALUES (101, 'Alice', 'New York', '2024-01-01', NULL, TRUE);

-- Customer moves to Boston: expire old, insert new
UPDATE dim_customer_scd2
SET valid_to = CURRENT_DATE - INTERVAL '1 day', is_current = FALSE
WHERE customer_id = 101 AND is_current = TRUE;

INSERT INTO dim_customer_scd2 (customer_id, name, city, valid_from, valid_to, is_current)
VALUES (101, 'Alice', 'Boston', CURRENT_DATE, NULL, TRUE);

-- Query facts with correct historical dimension
SELECT f.*, c.city
FROM fact_sales f
JOIN dim_customer_scd2 c
  ON f.customer_sk = c.customer_sk  -- uses the surrogate key
WHERE c.is_current = TRUE;
```

**Variant:** Compare with SCD Type 1 (overwrite, no history) and Type 3 (add a column for previous value, limited history):

```sql
-- SCD Type 1: just UPDATE, no history kept
UPDATE dim_customer SET city = 'Boston' WHERE customer_id = 101;

-- SCD Type 3: keeps previous value in a separate column
ALTER TABLE dim_customer ADD COLUMN prev_city VARCHAR(100);
UPDATE dim_customer
SET prev_city = city, city = 'Boston'
WHERE customer_id = 101;
```

## Q34: Design an ER-to-relational mapping for a 1:1 relationship between employees and parking_spaces.

**Answer:**
For a 1:1 relationship, merge the two entities into one table, or place the FK in either table with a UNIQUE constraint. If the relationship is optional on both sides, separate tables with a shared PK or FK with UNIQUE is cleaner.

```sql
-- Option 1: merge into one table (if 1:1 is mandatory)
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(100),
    parking_spot VARCHAR(20)
);

-- Option 2: separate tables with shared PK
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE parking_spaces (
    emp_id INT PRIMARY KEY REFERENCES employees(emp_id),
    spot_number VARCHAR(20) UNIQUE NOT NULL,
    floor INT
);

-- Query
SELECT e.name, p.spot_number, p.floor
FROM employees e
LEFT JOIN parking_spaces p ON e.emp_id = p.emp_id;
```

## Q35: Map a 1:N relationship (department → employees) to a relational schema.

**Answer:**
Place the foreign key on the "many" side. Each employee row holds a reference to their single department. This is the standard and most efficient mapping for 1:N relationships.

```sql
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(100),
    budget DECIMAL(14,2)
);

CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(100),
    hire_date DATE,
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

-- Find department for each employee
SELECT e.name, d.dept_name
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id;
```

## Q36: Map a M:N relationship (students ↔ courses) to a relational schema using a junction table.

**Answer:**
A many-to-many relationship requires a junction (associative) table with foreign keys to both entities. The junction table's primary key is typically the composite of both foreign keys. Additional relationship attributes (grade, enrollment date) can live in the junction table.

```sql
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    title VARCHAR(200),
    credits INT
);

-- Junction table
CREATE TABLE enrollments (
    student_id INT,
    course_id INT,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    grade DECIMAL(4,2),
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- Students with most enrollments
SELECT s.name, COUNT(*) AS course_count
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.name
ORDER BY course_count DESC;
```

**Variant:** A junction table can also store composite-unique business rules, e.g., prevent the same course being taught by two teachers in the same room:

```sql
CREATE TABLE enrollments (
    student_id INT,
    course_id INT,
    room VARCHAR(20),
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (student_id, course_id, room),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

## Q37: How do you identify entity boundaries when designing a schema?

**Answer:**
An entity boundary is determined by: (1) whether the concept has its own identity (primary key), (2) whether it has attributes that describe only itself, (3) whether multiple instances of the parent can have different values for it, and (4) lifecycle independence (can it exist without the parent?). If it fails these, it may be an attribute, not an entity.

```sql
-- Is "address" an entity or an attribute?
-- If customers have only one address → attribute
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    address VARCHAR(300)
);

-- If customers have multiple addresses → entity
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE addresses (
    address_id INT PRIMARY KEY,
    customer_id INT,
    street VARCHAR(200),
    city VARCHAR(100),
    is_primary BOOLEAN,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

## Q38: Given these query patterns on an e-commerce schema, validate whether the current design supports them efficiently.

**Answer:**
Validate schema design by mapping each frequent query to its required joins and checking for missing indexes, unnecessary joins, or denormalization opportunities.

```sql
-- Query pattern: "Get all orders for a customer, sorted by date"
-- Current design: orders(order_id, customer_id, order_date)
-- Validate: customer_id needs an index
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- Query pattern: "Top 10 products by revenue this month"
-- Current design requires joining orders → order_items → products
-- Validate: composite index on order_items
CREATE INDEX idx_oi_product_order ON order_items(product_id, order_id, quantity, unit_price);

-- Query pattern: "Customer's most recent order"
-- Validate: covering index
CREATE INDEX idx_orders_cust_date ON orders(customer_id, order_date DESC);

-- Verify query performance with EXPLAIN
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE customer_id = 1234
ORDER BY order_date DESC
LIMIT 10;
```

## Q39: What is a snapshot table in data warehousing?

**Answer:**
A snapshot table captures the state of data at a specific point in time. Unlike transactional tables (which record events), snapshots record periodic snapshots (daily, monthly) of measures. They are used for tracking balances, inventory levels, or account states over time.

```sql
-- Daily inventory snapshot
CREATE TABLE inventory_snapshot (
    snapshot_date DATE NOT NULL,
    product_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    quantity_on_hand INT,
    quantity_reserved INT,
    unit_cost DECIMAL(10,2),
    PRIMARY KEY (snapshot_date, product_id, warehouse_id)
);

-- Monthly account balance snapshot
CREATE TABLE account_snapshot (
    snapshot_month DATE NOT NULL,
    account_id INT NOT NULL,
    balance DECIMAL(14,2),
    interest_earned DECIMAL(10,2),
    PRIMARY KEY (snapshot_month, account_id)
);

-- Compare snapshots over time
SELECT a.product_id,
       a.quantity_on_hand AS start_month,
       b.quantity_on_hand AS end_month,
       b.quantity_on_hand - a.quantity_on_hand AS change
FROM inventory_snapshot a
JOIN inventory_snapshot b
  ON a.product_id = b.product_id
  AND a.snapshot_date = '2025-01-01'
  AND b.snapshot_date = '2025-02-01';
```

**Variant:** Compare two snapshots with a `LEFT JOIN` to catch products with zero-ending stock:

```sql
SELECT a.product_id,
       COALESCE(b.quantity_on_hand, 0) AS end_quantity,
       a.quantity_on_hand - COALESCE(b.quantity_on_hand, 0) AS delta
FROM inventory_snapshot a
LEFT JOIN inventory_snapshot b
  ON a.product_id = b.product_id AND b.snapshot_date = '2025-02-01'
WHERE a.snapshot_date = '2025-01-01';
```

## Q40: Design a hospital schema for patients, doctors, visits, diagnoses, and prescriptions in 3NF.

**Answer:**
Separate entities: patients, doctors, visits (1:N from patient and doctor), diagnoses (M:N via junction), and prescriptions (1:N from visit). Ensure no transitive dependencies.

```sql
CREATE TABLE patients (
    patient_id INT PRIMARY KEY,
    name VARCHAR(100),
    dob DATE,
    insurance_id VARCHAR(50)
);

CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY,
    name VARCHAR(100),
    specialty VARCHAR(100),
    department_id INT
);

CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    name VARCHAR(100),
    floor INT
);

-- doctor → department is 1:N, department is a separate entity (3NF)

CREATE TABLE visits (
    visit_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    visit_date TIMESTAMP,
    chief_complaint TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

CREATE TABLE diagnoses (
    visit_id INT,
    diagnosis_code VARCHAR(10),
    description VARCHAR(300),
    PRIMARY KEY (visit_id, diagnosis_code),
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id)
);

CREATE TABLE prescriptions (
    prescription_id INT PRIMARY KEY,
    visit_id INT,
    medication VARCHAR(200),
    dosage VARCHAR(100),
    duration_days INT,
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id)
);
```

## Q41: Design a banking schema for accounts, transactions, and customers in 3NF.

**Answer:**
Customers, accounts, and transactions are distinct entities. A customer can have multiple accounts (1:N). An account can have multiple transactions (1:N). Transaction type (deposit, withdrawal) can be an attribute or a small lookup table.

```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(200),
    ssn_hash VARCHAR(64),
    date_of_birth DATE,
    address VARCHAR(300)
);

CREATE TABLE accounts (
    account_id INT PRIMARY KEY,
    customer_id INT,
    account_type VARCHAR(20),  -- 'checking', 'savings'
    balance DECIMAL(14,2),
    opened_date DATE,
    status VARCHAR(10),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE transaction_types (
    type_code VARCHAR(10) PRIMARY KEY,
    description VARCHAR(50)
);

CREATE TABLE transactions (
    transaction_id BIGINT PRIMARY KEY,
    account_id INT,
    type_code VARCHAR(10),
    amount DECIMAL(12,2),
    transaction_date TIMESTAMP,
    description VARCHAR(300),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (type_code) REFERENCES transaction_types(type_code)
);

-- Index for common query: transactions by account ordered by date
CREATE INDEX idx_txn_account_date ON transactions(account_id, transaction_date DESC);
```

**Alt1:** For high-volume banking, consider partitioning the transactions table:

```sql
-- PostgreSQL range partitioning by transaction date
CREATE TABLE transactions (
    transaction_id BIGINT,
    account_id INT,
    type_code VARCHAR(10),
    amount DECIMAL(12,2),
    transaction_date TIMESTAMP
) PARTITION BY RANGE (transaction_date);

CREATE TABLE transactions_2025_q1 PARTITION OF transactions
    FOR VALUES FROM ('2025-01-01') TO ('2025-04-01');
```

## Q42: What is an update anomaly and how do you prevent it?

**Answer:**
An update anomaly occurs when updating a single fact requires modifying multiple rows, risking inconsistency. For example, if a customer's city is stored in every order row, changing the city requires updating all those rows. Prevention: separate the data into its own table and reference it via foreign key.

```sql
-- Anomaly: customer city stored in every order
CREATE TABLE orders_bad (
    order_id INT PRIMARY KEY,
    customer_id INT,
    customer_city VARCHAR(100)  -- duplicated in every order row
);

-- Fix: normalize
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Now city is updated in one place only
UPDATE customers SET city = 'Chicago' WHERE customer_id = 42;
```

## Q43: What is a delete anomaly?

**Answer:**
A delete anomaly is when deleting a row unintentionally removes the only record of some other fact. For example, if the only employee in a department is deleted and the department information is stored only with employees, the department is lost. Normalization prevents this by storing independent entities separately.

```sql
-- Delete anomaly: department info stored only with employees
CREATE TABLE emp_dept_bad (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100),
    dept_id INT,
    dept_name VARCHAR(100)
);

-- Deleting the only employee in dept 10 loses the department
DELETE FROM emp_dept_bad WHERE emp_id = 5;
-- Now dept_id=10, dept_name='Research' no longer exists anywhere

-- Fix: normalize
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(100)
);

CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100),
    dept_id INT REFERENCES departments(dept_id)
);

-- Now deleting the employee does NOT lose the department
DELETE FROM employees WHERE emp_id = 5;
-- departments row for dept 10 still exists
```

## Q44: Design an ecommerce schema: users, products, orders, order_items, reviews, and categories. Keep it in 3NF.

**Answer:**
Map entities with proper relationships: users place orders (1:N), orders contain order_items (1:N), products belong to categories (N:1), users review products (M:N via reviews junction). Avoid storing derived data.

```sql
CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    name VARCHAR(100),
    parent_category_id INT REFERENCES categories(category_id)
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name VARCHAR(200),
    description TEXT,
    price DECIMAL(10,2),
    category_id INT,
    stock_quantity INT,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(200) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20),
    total_amount DECIMAL(12,2),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),  -- snapshot of price at time of order
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE reviews (
    review_id INT PRIMARY KEY,
    user_id INT,
    product_id INT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    UNIQUE (user_id, product_id)  -- one review per user per product
);
```

## Q45: How do you validate a schema given a set of query patterns?

**Answer:**
For each query pattern, trace the required tables, joins, filters, and sorts. Check that the necessary foreign keys exist, indexes support the access path, and the grain of the data allows the aggregation without double-counting. Use `EXPLAIN` to verify the execution plan.

```sql
-- Query pattern: "Daily revenue by category for the last 30 days"
-- Trace: orders → order_items → products → categories

EXPLAIN ANALYZE
SELECT DATE(o.order_date) AS sale_date,
       c.name AS category,
       SUM(oi.quantity * oi.unit_price) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
WHERE o.order_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY sale_date, c.name
ORDER BY sale_date, revenue DESC;

-- Check: does this query hit the right indexes?
-- Ensure: idx_orders_date, idx_oi_order, idx_products_category
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_oi_order ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
```

**Alt1:** Also verify the grain: if both `order_items` and `orders` get summed in the same query, you risk double-counting. Check cardinality first:

```sql
-- If this returns more than 1, the grain is wrong for aggregation
SELECT o.order_id, COUNT(oi.order_id) AS line_count
FROM orders o
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id
HAVING COUNT(oi.order_id) > 1;
```

## Q46: Given a denormalized table `student_courses(student_id, student_name, course_id, course_name, teacher_id, teacher_name)`, normalize it to 3NF.

**Answer:**
The table violates 2NF and 3NF: student_name depends only on student_id, course_name on course_id, teacher_name on teacher_id. Create separate tables for students, courses, and teachers. The relationship between students and courses goes through a junction table.

```sql
-- Denormalized original
CREATE TABLE student_courses_denorm (
    student_id INT,
    student_name VARCHAR(100),
    course_id INT,
    course_name VARCHAR(200),
    teacher_id INT,
    teacher_name VARCHAR(100)
);

-- 3NF decomposition
CREATE TABLE teachers (
    teacher_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(200),
    teacher_id INT,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);

CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE enrollments (
    student_id INT,
    course_id INT,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

## Q47: What are precomputed aggregates and how do you keep them consistent?

**Answer:**
Precomputed aggregates store summary results (totals, counts, averages) in a separate table to avoid recalculating them on every read. Consistency is maintained via triggers, batch jobs, or incremental updates when source data changes.

```sql
-- Precomputed: total revenue per product
CREATE TABLE product_revenue (
    product_id INT PRIMARY KEY,
    total_revenue DECIMAL(14,2) DEFAULT 0,
    total_quantity INT DEFAULT 0,
    order_count INT DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Method 1: Trigger-based maintenance
CREATE OR REPLACE FUNCTION update_product_revenue()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO product_revenue (product_id, total_revenue, total_quantity, order_count)
    SELECT product_id,
           SUM(quantity * unit_price),
           SUM(quantity),
           COUNT(DISTINCT order_id)
    FROM order_items
    WHERE product_id = COALESCE(NEW.product_id, OLD.product_id)
    GROUP BY product_id
    ON CONFLICT (product_id) DO UPDATE
    SET total_revenue = EXCLUDED.total_revenue,
        total_quantity = EXCLUDED.total_quantity,
        order_count = EXCLUDED.order_count,
        last_updated = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_order_item_change
AFTER INSERT OR UPDATE OR DELETE ON order_items
FOR EACH ROW EXECUTE FUNCTION update_product_revenue();

-- Method 2: Batch refresh (nightly job)
INSERT INTO product_revenue (product_id, total_revenue, total_quantity, order_count)
SELECT product_id,
       SUM(quantity * unit_price),
       SUM(quantity),
       COUNT(DISTINCT order_id)
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
GROUP BY product_id
ON CONFLICT (product_id) DO UPDATE
SET total_revenue = EXCLUDED.total_revenue,
    total_quantity = EXCLUDED.total_quantity,
    order_count = EXCLUDED.order_count,
    last_updated = CURRENT_TIMESTAMP;
```

## Q48: Design a data warehouse schema for a retail chain with dimensions: time, product, store, promotion, and a fact table for sales.

**Answer:**
A retail star schema has a central fact_sales table with measures like quantity, revenue, cost, and discount. Dimensions capture time, product details, store info, and promotion details. Degenerate dimensions (like order number) go directly in the fact table.

```sql
CREATE TABLE dim_time (
    time_key INT PRIMARY KEY,       -- YYYYMMDD format
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    week INT,
    day_of_week VARCHAR(10),
    is_holiday BOOLEAN
);

CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    sku VARCHAR(50),
    product_name VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    unit_cost DECIMAL(10,2),
    unit_price DECIMAL(10,2)
);

CREATE TABLE dim_store (
    store_key INT PRIMARY KEY,
    store_name VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(50),
    region VARCHAR(50),
    store_type VARCHAR(50),
    open_date DATE
);

CREATE TABLE dim_promotion (
    promotion_key INT PRIMARY KEY,
    promo_name VARCHAR(200),
    discount_type VARCHAR(20),
    discount_pct DECIMAL(5,2),
    start_date DATE,
    end_date DATE
);

CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    time_key INT,
    product_key INT,
    store_key INT,
    promotion_key INT,
    order_number VARCHAR(50),       -- degenerate dimension
    quantity INT,
    revenue DECIMAL(12,2),
    cost DECIMAL(12,2),
    discount_amount DECIMAL(10,2),
    FOREIGN KEY (time_key) REFERENCES dim_time(time_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key),
    FOREIGN KEY (promotion_key) REFERENCES dim_promotion(promotion_key)
);
```

## Q49: Explain the difference between snapshot tables and transactional (event) tables in a data warehouse.

**Answer:**
**Transactional (fact) tables** record individual events/transactions (a sale, a click, a shipment). They are append-only and the grain is one row per event. **Snapshot tables** record the state of something at a point in time (daily balance, monthly inventory). They have a date key as part of the primary key and enable point-in-time analysis.

```sql
-- Transactional fact: one row per sale event
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    time_key INT,
    product_key INT,
    store_key INT,
    quantity INT,
    revenue DECIMAL(12,2)
);

-- Snapshot fact: one row per product per day
CREATE TABLE fact_inventory_snapshot (
    time_key INT,       -- part of PK
    product_key INT,    -- part of PK
    warehouse_key INT,  -- part of PK
    quantity_on_hand INT,
    quantity_in_transit INT,
    reorder_point INT,
    PRIMARY KEY (time_key, product_key, warehouse_key)
);

-- Query transactional: "How many sales yesterday?"
SELECT SUM(quantity) FROM fact_sales WHERE time_key = 20250901;

-- Query snapshot: "What was inventory on Sep 1?"
SELECT product_key, quantity_on_hand
FROM fact_inventory_snapshot
WHERE time_key = 20250901;
```

**Variant:** Transactional tables can be made *accumulating snapshots* (SCD-style for workflows) by adding status dates:

```sql
CREATE TABLE fact_order_pipeline (
    order_id BIGINT PRIMARY KEY,
    order_placed_date_key INT,
    payment_date_key INT,
    shipped_date_key INT,
    delivered_date_key INT,
    total_revenue DECIMAL(12,2)
);
-- NULL dates mean "step not yet reached" — accumulates status over time
```

## Q50: What is a degenerate dimension and when do you use it?

**Answer:**
A degenerate dimension is a dimension attribute that is stored directly in the fact table because it has no associated dimension table. Common examples are order numbers, invoice numbers, or transaction IDs. They are used when the attribute is the key identifier of the transaction and does not need further descriptive attributes.

```sql
CREATE TABLE fact_invoices (
    invoice_number VARCHAR(20) PRIMARY KEY,  -- degenerate dimension
    time_key INT,
    customer_key INT,
    total_amount DECIMAL(12,2),
    tax DECIMAL(10,2),
    FOREIGN KEY (time_key) REFERENCES dim_time(time_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key)
);

-- Query using degenerate dimension
SELECT invoice_number, total_amount
FROM fact_invoices
WHERE time_key = 20250901
ORDER BY total_amount DESC;
```

## Q51: Normalize this table from UNF to 3NF: R(order_id, product_name, product_category, customer_name, customer_city, order_date, quantity, price).

**Answer:**
First, check 1NF (all values atomic — yes, it's already flat). For 2NF: the PK is likely `(order_id, product_name)` since one order can have multiple products. `customer_name`, `customer_city`, and `order_date` depend only on `order_id` (partial dependency). `product_category` depends only on `product_name` (partial). Decompose to remove all partial dependencies. For 3NF: `customer_city` might depend on a customer-level attribute rather than directly on customer — but assuming customer is identified by name alone, we add a customer_id.

```sql
-- UNF / 1NF (already flat)
CREATE TABLE orders_raw (
    order_id INT,
    product_name VARCHAR(200),
    product_category VARCHAR(100),
    customer_name VARCHAR(100),
    customer_city VARCHAR(100),
    order_date DATE,
    quantity INT,
    price DECIMAL(10,2)
);

-- 2NF / 3NF decomposition
CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name VARCHAR(200),
    category_id INT,
    price DECIMAL(10,2),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

**Variant:** If a customer can have multiple shipping addresses, promote `shipping_address` to its own entity and reference it instead of embedding it in the order:

```sql
CREATE TABLE addresses (
    address_id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    street VARCHAR(200),
    city VARCHAR(100),
    zip VARCHAR(20)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    shipping_address_id INT REFERENCES addresses(address_id),
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

## Q52: What are the signs that a table needs denormalization?

**Answer:**
Signs include: (1) frequent queries require 3+ table joins with large result sets, (2) reports are slow despite proper indexing, (3) the data is read-heavy and rarely updated, (4) aggregate queries repeatedly compute the same summaries, and (5) the application is latency-sensitive and joins are the bottleneck. Always benchmark before deciding.

```sql
-- Symptom: slow report query with many joins
EXPLAIN ANALYZE
SELECT c.name, p.category, SUM(oi.quantity * oi.unit_price) AS total
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE o.date >= '2025-01-01'
GROUP BY c.name, p.category;
-- If this consistently exceeds SLA, consider denormalization

-- Denormalized report table
CREATE TABLE customer_category_sales (
    customer_name VARCHAR(100),
    category VARCHAR(100),
    total_sales DECIMAL(14,2),
    last_refreshed TIMESTAMP
);
```

## Q53: Explain how to normalize a table with repeating groups using PostgreSQL array columns.

**Answer:**
Even though PostgreSQL supports arrays, they violate 1NF because they store multiple values in a single column. Normalize by unnesting the array into rows and creating a separate table. Arrays can be useful for storage but should not be used for joins or filtering in normalized designs.

```sql
-- Violates 1NF: using PostgreSQL array
CREATE TABLE students_bad (
    student_id INT PRIMARY KEY,
    name VARCHAR(100),
    courses TEXT[]  -- {'Math','Physics','CS'}
);

-- Unnest to verify data
SELECT student_id, unnest(courses) AS course
FROM students_bad;

-- Normalize
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE enrollments (
    student_id INT,
    course VARCHAR(100),
    PRIMARY KEY (student_id, course),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
```

## Q54: Map an ER diagram with a weak entity (order_line depends on order) to relational tables.

**Answer:**
A weak entity has no independent identity and depends on an identifying owner entity. Its primary key includes the owner's primary key. An order line cannot exist without an order, so its PK is `(order_id, line_number)`.

```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE
);

-- Weak entity: order_line
CREATE TABLE order_lines (
    order_id INT,
    line_number INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    PRIMARY KEY (order_id, line_number),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
```

**Variant:** In a strict 1NF flattening of a weak entity, use `WITH ORDINALITY` in PostgreSQL to generate line numbers:

```sql
SELECT o.order_id, ol.product_id, ol.quantity,
       ROW_NUMBER() OVER (PARTITION BY o.order_id ORDER BY ol.product_id) AS line_number
FROM orders o
CROSS JOIN LATERAL unnest(o.products) WITH ORDINALITY AS ol(product_id, quantity);
```

## Q55: What is the difference between logical and physical schema design?

**Answer:**
**Logical design** models entities, relationships, attributes, and constraints independent of any DBMS (ER diagrams, normalization). **Physical design** maps the logical model to specific storage structures: choosing data types, indexes, partitioning, tablespace placement, and denormalization decisions. Physical design optimizes for performance on a specific platform.

```sql
-- Logical design (conceptual)
-- Customer {customer_id, name, email}
-- Order {order_id, customer_id, order_date}

-- Physical design (PostgreSQL-specific)
CREATE TABLE customers (
    customer_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(320) NOT NULL UNIQUE
) WITH (fillfactor = 90);  -- physical tuning

CREATE TABLE orders (
    order_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customers(customer_id),
    order_date TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (order_date);  -- physical: partitioning
```

## Q56: Given an unnormalized table R(A, B, C, D, E) where A→B, A→C, B→D, (A,B)→E, find the candidate keys and normalize to 3NF.

**Answer:**
`A` determines `B` and `C`, and `B→D` means `A→D` transitively. `A` determines `B`, `C`, `D`, but not `E` directly — `(A,B)→E` means `A→E` (since `A→B`). So `A` determines everything: candidate key is `{A}`. Not in 3NF because of transitive dependency `A→B→D`. Decompose: `(A,B,C,E)` and `(B,D)`.

```sql
CREATE TABLE abc (
    A INT PRIMARY KEY,
    B INT,
    C INT,
    E INT
);

CREATE TABLE bd (
    B INT PRIMARY KEY,
    D INT
);

-- Verify: original data is reconstructable
SELECT a.A, a.B, a.C, b.D, a.E
FROM abc a
JOIN bd b ON a.B = b.B;
```

**Variant:** If `(A,B)→E` but `A` alone does not determine `E` (if we reinterpret), then the candidate key is `{A,B}`. In that case, `A→B` is a partial dependency and `B→D` is also partial. Decompose: `(A,B,C,E)` and `(B,D)` — same result but the reasoning differs.

## Q57: Design a reporting denormalization for a banking dashboard that shows account balance, last transaction, and customer info.

**Answer:**
For a read-heavy banking dashboard, create a denormalized materialized view that pre-joins accounts, customers, and the latest transaction. Refresh it periodically or via trigger on transaction inserts.

```sql
-- Materialized view approach (PostgreSQL)
CREATE MATERIALIZED VIEW mv_account_dashboard AS
SELECT
    a.account_id,
    a.account_type,
    a.balance,
    c.name AS customer_name,
    c.email AS customer_email,
    t.transaction_id AS last_txn_id,
    t.amount AS last_txn_amount,
    t.transaction_date AS last_txn_date,
    t.description AS last_txn_desc
FROM accounts a
JOIN customers c ON a.customer_id = c.customer_id
LEFT JOIN LATERAL (
    SELECT *
    FROM transactions
    WHERE account_id = a.account_id
    ORDER BY transaction_date DESC
    LIMIT 1
) t ON TRUE;

-- Refresh nightly
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_account_dashboard;

-- Query is now a simple single-table scan
SELECT * FROM mv_account_dashboard WHERE customer_name LIKE 'Smith%';
```

## Q58: What is a junk dimension and when would you use one?

**Answer:**
A junk dimension combines several low-cardinality flags and indicators (e.g., is_returned, is_gift, is_international) into a single dimension table. It avoids having many small flag columns in the fact table or numerous tiny dimension tables. The junk dimension rows are all possible combinations of the flags.

```sql
CREATE TABLE dim_flags (
    flag_key INT PRIMARY KEY,
    is_returned BOOLEAN,
    is_gift_wrapped BOOLEAN,
    is_international BOOLEAN,
    payment_method VARCHAR(20),
    shipping_method VARCHAR(20)
);

-- Populate with all combinations
INSERT INTO dim_flags (flag_key, is_returned, is_gift_wrapped, is_international, payment_method, shipping_method)
SELECT
    ROW_NUMBER() OVER () AS flag_key,
    f.is_returned,
    f.is_gift_wrapped,
    f.is_international,
    f.payment_method,
    f.shipping_method
FROM (
    SELECT DISTINCT
        is_returned, is_gift_wrapped, is_international,
        payment_method, shipping_method
    FROM raw_orders
) f;

-- Fact table references the junk dimension
CREATE TABLE fact_orders (
    order_id BIGINT PRIMARY KEY,
    time_key INT,
    product_key INT,
    customer_key INT,
    flag_key INT,       -- references junk dimension
    quantity INT,
    revenue DECIMAL(12,2),
    FOREIGN KEY (flag_key) REFERENCES dim_flags(flag_key)
);
```

## Q59: What is a role-playing dimension and how do you implement it?

**Answer:**
A role-playing dimension is a single dimension table that serves multiple roles in a fact table. For example, a `dim_date` table can be referenced as `order_date`, `ship_date`, and `delivery_date`. Implement it using multiple foreign keys in the fact table, each referencing the same dimension.

```sql
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    day_of_week VARCHAR(10)
);

CREATE TABLE fact_orders (
    order_id BIGINT PRIMARY KEY,
    order_date_key INT REFERENCES dim_date(date_key),     -- role: order date
    ship_date_key INT REFERENCES dim_date(date_key),      -- role: ship date
    delivery_date_key INT REFERENCES dim_date(date_key),  -- role: delivery date
    product_key INT,
    customer_key INT,
    quantity INT,
    revenue DECIMAL(12,2)
);

-- Query: average days from order to delivery
SELECT AVG(d2.full_date - d1.full_date) AS avg_delivery_days
FROM fact_orders f
JOIN dim_date d1 ON f.order_date_key = d1.date_key
JOIN dim_date d2 ON f.delivery_date_key = d2.date_key;
```

## Q60: What is a conformed dimension and why does it matter?

**Answer:**
A conformed dimension is shared across multiple fact tables with the same structure, attributes, and values. It ensures consistency when combining data from different fact tables (e.g., sales and inventory both use the same `dim_date` or `dim_product`). Conformed dimensions are essential for a consistent enterprise data warehouse.

```sql
-- Same dim_product used by multiple facts
CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    sku VARCHAR(50),
    name VARCHAR(200),
    category VARCHAR(100)
);

CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    time_key INT,
    product_key INT REFERENCES dim_product(product_key),
    revenue DECIMAL(12,2)
);

CREATE TABLE fact_inventory (
    snapshot_date INT,
    product_key INT REFERENCES dim_product(product_key),
    quantity_on_hand INT
);

-- Cross-fact query using conformed dimension
SELECT p.category,
       SUM(f.revenue) AS total_sales,
       AVG(i.quantity_on_hand) AS avg_inventory
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
JOIN fact_inventory i ON f.product_key = i.product_key AND f.time_key = i.snapshot_date
GROUP BY p.category;
```

## Q61: Given R(A,B,C,D,E) with FDs: {A,B}→C, C→D, D→E. Find candidate keys and normalize to BCNF.

**Answer:**
`{A,B}` determines `C`, then `C→D→E`, so `{A,B}` determines everything. Candidate key: `{A,B}`. BCNF violation: `C→D` and `C` is not a superkey. Also `D→E` and `D` is not a superkey. Decompose: `CD(C,D)`, `DE(D,E)`, and `ABC(A,B,C)`.

```sql
CREATE TABLE abc (
    A INT,
    B INT,
    C INT,
    PRIMARY KEY (A, B)
);

CREATE TABLE cd (
    C INT PRIMARY KEY,
    D INT
);

CREATE TABLE de (
    D INT PRIMARY KEY,
    E INT
);

-- Reconstruction:
SELECT a.A, a.B, a.C, c.D, d.E
FROM abc a
JOIN cd c ON a.C = c.C
JOIN de d ON c.D = d.D;
```

## Q62: How do you handle multi-valued dependencies in a real-world scenario?

**Answer:**
Multi-valued dependencies arise when one attribute has multiple independent sets of values. A classic example: an employee can have multiple skills AND multiple languages, independently. The fix is to decompose so each independent multi-valued fact gets its own table.

```sql
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(100)
);

-- Each independent MVD gets its own table
CREATE TABLE employee_skills (
    emp_id INT,
    skill VARCHAR(100),
    PRIMARY KEY (emp_id, skill),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);

CREATE TABLE employee_languages (
    emp_id INT,
    language VARCHAR(50),
    PRIMARY KEY (emp_id, language),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);

-- Insert independent facts
INSERT INTO employee_skills VALUES (1, 'SQL'), (1, 'Python');
INSERT INTO employee_languages VALUES (1, 'English'), (1, 'Hindi');

-- Query: employees with both SQL skill AND English language
SELECT e.name
FROM employees e
JOIN employee_skills s ON e.emp_id = s.emp_id
JOIN employee_languages l ON e.emp_id = l.emp_id
WHERE s.skill = 'SQL' AND l.language = 'English';
```

## Q63: Explain the concept of a data vault modeling approach vs. 3NF.

**Answer:**
Data Vault uses three types of tables: **hubs** (business keys), **links** (relationships), and **satellites** (descriptive attributes with history). Unlike 3NF, Data Vault is append-only, never updates/deletes, and tracks full history with load timestamps. It is designed for auditability and parallel loading in data warehouses, while 3NF optimizes for storage efficiency and integrity in OLTP.

```sql
-- Data Vault example
CREATE TABLE hub_customer (
    customer_hk VARCHAR(64) PRIMARY KEY,  -- hash key
    customer_bk VARCHAR(50),              -- business key (natural)
    load_date TIMESTAMP,
    record_source VARCHAR(100)
);

CREATE TABLE sat_customer_details (
    customer_hk VARCHAR(64),
    load_date TIMESTAMP,
    load_end_date TIMESTAMP,
    name VARCHAR(200),
    email VARCHAR(200),
    city VARCHAR(100),
    record_source VARCHAR(100),
    PRIMARY KEY (customer_hk, load_date),
    FOREIGN KEY (customer_hk) REFERENCES hub_customer(customer_hk)
);

-- 3NF equivalent (for comparison)
CREATE TABLE customers_3nf (
    customer_id INT PRIMARY KEY,
    name VARCHAR(200),
    email VARCHAR(200),
    city VARCHAR(100)
);
```

## Q64: What is a ranked/dimension table pattern in data warehousing?

**Answer:**
Ranked dimensions store pre-computed rankings for dimension attributes (e.g., top 10 products by sales). This is a denormalization technique that avoids expensive window functions at query time. Rankings are refreshed periodically.

```sql
CREATE TABLE dim_product_ranked (
    product_key INT PRIMARY KEY,
    product_name VARCHAR(200),
    category VARCHAR(100),
    total_revenue DECIMAL(14,2),
    revenue_rank INT,
    category_rank INT,
    last_refreshed TIMESTAMP
);

-- Populate with rankings
INSERT INTO dim_product_ranked
SELECT
    p.product_key,
    p.name,
    p.category,
    rev.total_revenue,
    RANK() OVER (ORDER BY rev.total_revenue DESC) AS revenue_rank,
    RANK() OVER (PARTITION BY p.category ORDER BY rev.total_revenue DESC) AS category_rank,
    CURRENT_TIMESTAMP
FROM dim_product p
JOIN (
    SELECT product_key, SUM(revenue) AS total_revenue
    FROM fact_sales
    GROUP BY product_key
) rev ON p.product_key = rev.product_key;

-- Dashboard query is simple
SELECT * FROM dim_product_ranked WHERE revenue_rank <= 10;
```

## Q65: How do you handle slowly changing dimensions with Type 1, 2, and 3? Give a comparison.

**Answer:**
**Type 1**: Overwrite — no history kept. Simple but loses track of changes. **Type 2**: Add new row — full history with `valid_from`, `valid_to`, `is_current` flags. Best for historical reporting. **Type 3**: Add column for old value — limited history (only previous value). Choose based on how much history you need.

```sql
-- SCD Type 1: simple overwrite
CREATE TABLE dim_customer_t1 (
    customer_id INT PRIMARY KEY,
    name VARCHAR(200),
    city VARCHAR(100),
    updated_at TIMESTAMP
);

UPDATE dim_customer_t1 SET city = 'Boston', updated_at = NOW()
WHERE customer_id = 101;

-- SCD Type 2: full history (detailed in Q33)
CREATE TABLE dim_customer_t2 (
    customer_sk SERIAL PRIMARY KEY,
    customer_id INT,
    name VARCHAR(200),
    city VARCHAR(100),
    valid_from DATE,
    valid_to DATE,
    is_current BOOLEAN
);

-- SCD Type 3: limited history (previous value)
CREATE TABLE dim_customer_t3 (
    customer_id INT PRIMARY KEY,
    name VARCHAR(200),
    current_city VARCHAR(100),
    previous_city VARCHAR(100),
    city_changed_date DATE
);
```

## Q66: What is a junk dimension alternative using bitmap indexes?

**Answer:**
Instead of creating a physical junk dimension table, you can use bitmap indexes on boolean/flag columns in the fact table. This is efficient for low-cardinality flags in columnar or data warehouse databases. However, it's a physical optimization, not a logical normalization choice.

```sql
-- Flag columns directly in fact table
CREATE TABLE fact_orders (
    order_id BIGINT PRIMARY KEY,
    time_key INT,
    product_key INT,
    is_returned BOOLEAN,
    is_gift BOOLEAN,
    is_international BOOLEAN,
    quantity INT,
    revenue DECIMAL(12,2)
);

-- PostgreSQL: GIN index on jsonb flags (alternative approach)
ALTER TABLE fact_orders ADD COLUMN flags JSONB;
UPDATE fact_orders SET flags = jsonb_build_object(
    'returned', is_returned,
    'gift', is_gift,
    'international', is_international
);

CREATE INDEX idx_flags ON fact_orders USING GIN (flags);

-- Query using flags
SELECT * FROM fact_orders WHERE flags @> '{"returned": true, "gift": false}';
```

## Q67: Design a slowly changing dimension Type 2 for a product dimension in a retail data warehouse.

**Answer:**
SCD Type 2 for products tracks changes in name, category, price, and status over time. Each change creates a new row with updated attributes, while the old row is marked as expired.

```sql
CREATE TABLE dim_product_scd2 (
    product_sk SERIAL PRIMARY KEY,
    product_id INT,               -- business key
    product_name VARCHAR(200),
    category VARCHAR(100),
    brand VARCHAR(100),
    unit_price DECIMAL(10,2),
    status VARCHAR(20),           -- 'active', 'discontinued'
    valid_from DATE NOT NULL,
    valid_to DATE,
    is_current BOOLEAN DEFAULT TRUE
);

-- Initial load
INSERT INTO dim_product_scd2 (product_id, product_name, category, brand, unit_price, status, valid_from, valid_to, is_current)
VALUES (501, 'Widget Pro', 'Electronics', 'Acme', 29.99, 'active', '2025-01-01', NULL, TRUE);

-- Price change → new version
UPDATE dim_product_scd2
SET valid_to = '2025-06-30', is_current = FALSE
WHERE product_id = 501 AND is_current = TRUE;

INSERT INTO dim_product_scd2 (product_id, product_name, category, brand, unit_price, status, valid_from, valid_to, is_current)
VALUES (501, 'Widget Pro', 'Electronics', 'Acme', 34.99, 'active', '2025-07-01', NULL, TRUE);

-- Join with fact using surrogate key
SELECT f.time_key, p.product_name, p.unit_price, f.revenue
FROM fact_sales f
JOIN dim_product_scd2 p ON f.product_sk = p.product_sk;
```

## Q68: What are the pros and cons of surrogate keys vs. natural keys in a data warehouse?

**Answer:**
**Surrogate keys pros**: compact, stable (no business changes), uniform (integer), enable SCD Type 2, avoid composite keys. **Cons**: extra join needed, harder to debug. **Natural keys pros**: meaningful, no extra join, no mapping table. **Cons**: can be wide/composite, may change (requiring updates), harder for SCD. In data warehouses, surrogate keys are strongly preferred.

```sql
-- Surrogate key approach (recommended for DW)
CREATE TABLE dim_customer (
    customer_sk SERIAL PRIMARY KEY,  -- surrogate
    customer_id INT NOT NULL,         -- business key
    name VARCHAR(200),
    email VARCHAR(200),
    valid_from DATE,
    valid_to DATE,
    is_current BOOLEAN
);

-- Natural key approach (avoid in DW)
CREATE TABLE dim_customer_natural (
    customer_id INT PRIMARY KEY,      -- natural key, no surrogate
    name VARCHAR(200),
    email VARCHAR(200)
);
-- Problem: SCD Type 2 requires a new customer_id, which conflicts with the natural key
```

## Q69: How do you avoid update anomalies in a junction table?

**Answer:**
Update anomalies in junction tables include duplicate rows and inconsistent foreign keys. Prevent them with: (1) composite primary key or unique constraint, (2) foreign key constraints, (3) application-level checks, and (4) unique constraints on business keys if the junction table has additional attributes.

```sql
CREATE TABLE enrollments (
    student_id INT,
    course_id INT,
    semester VARCHAR(20),
    grade CHAR(2),
    -- Prevent duplicate enrollments
    PRIMARY KEY (student_id, course_id, semester),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- Check for anomalies: duplicate enrollments
SELECT student_id, course_id, semester, COUNT(*) AS dupes
FROM enrollments
GROUP BY student_id, course_id, semester
HAVING COUNT(*) > 1;

-- Check for orphaned foreign keys
SELECT e.student_id
FROM enrollments e
LEFT JOIN students s ON e.student_id = s.student_id
WHERE s.student_id IS NULL;
```

## Q70: What is the purpose of a bridge table in dimensional modeling?

**Answer:**
A bridge table handles many-to-many relationships between a fact table and a dimension. For example, an order can have multiple promotions applied. The bridge table sits between `fact_orders` and `dim_promotion`, allowing multiple associations per fact row.

```sql
CREATE TABLE bridge_order_promotions (
    order_id INT,
    promotion_key INT,
    discount_applied DECIMAL(10,2),
    PRIMARY KEY (order_id, promotion_key),
    FOREIGN KEY (order_id) REFERENCES fact_orders(order_id),
    FOREIGN KEY (promotion_key) REFERENCES dim_promotion(promotion_key)
);

-- Query: orders with total discount per promotion
SELECT p.promo_name, COUNT(DISTINCT b.order_id) AS orders_used,
       SUM(b.discount_applied) AS total_discount
FROM bridge_order_promotions b
JOIN dim_promotion p ON b.promotion_key = p.promotion_key
GROUP BY p.promo_name;
```

## Q71: Normalize a hospital database with patients, doctors, appointments, medical_records, medications, and prescriptions. Show both the raw denormalized table and the 3NF result.

**Answer:**
A single denormalized table stores redundant doctor info, patient info, and repeated appointment data. Normalization splits this into separate entity tables and uses foreign keys.

```sql
-- Denormalized raw table
CREATE TABLE hospital_raw (
    patient_name VARCHAR(100),
    patient_dob DATE,
    patient_phone VARCHAR(20),
    doctor_name VARCHAR(100),
    doctor_specialty VARCHAR(100),
    appointment_date TIMESTAMP,
    diagnosis VARCHAR(200),
    medication VARCHAR(200),
    dosage VARCHAR(100)
);

-- 3NF decomposition
CREATE TABLE patients (
    patient_id INT PRIMARY KEY,
    name VARCHAR(100),
    dob DATE,
    phone VARCHAR(20)
);

CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY,
    name VARCHAR(100),
    specialty VARCHAR(100),
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

CREATE TABLE medical_records (
    record_id INT PRIMARY KEY,
    appointment_id INT,
    diagnosis VARCHAR(200),
    notes TEXT,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id)
);

CREATE TABLE medications (
    medication_id INT PRIMARY KEY,
    name VARCHAR(200),
    category VARCHAR(100)
);

CREATE TABLE prescriptions (
    prescription_id INT PRIMARY KEY,
    record_id INT,
    medication_id INT,
    dosage VARCHAR(100),
    frequency VARCHAR(50),
    duration_days INT,
    FOREIGN KEY (record_id) REFERENCES medical_records(record_id),
    FOREIGN KEY (medication_id) REFERENCES medications(medication_id)
);
```

## Q72: What is a junk dimension vs. a degenerate dimension?

**Answer:**
A **junk dimension** is a separate table that combines multiple low-cardinality flags/indicators (e.g., is_returned, is_gift, payment_method). A **degenerate dimension** is an attribute stored directly in the fact table because it doesn't need its own dimension table (e.g., order_number, invoice_id). Junk dimensions are explicit tables; degenerate dimensions live in the fact table.

```sql
-- Degenerate dimension: order number in fact table
CREATE TABLE fact_sales (
    order_number VARCHAR(50) PRIMARY KEY,  -- degenerate
    time_key INT,
    product_key INT,
    quantity INT,
    revenue DECIMAL(12,2)
);

-- Junk dimension: combined flags
CREATE TABLE dim_order_flags (
    flag_key INT PRIMARY KEY,
    is_returned BOOLEAN,
    is_gift_wrapped BOOLEAN,
    is_expedited BOOLEAN,
    payment_method VARCHAR(20)
);

CREATE TABLE fact_sales_full (
    sale_id BIGINT PRIMARY KEY,
    order_number VARCHAR(50),  -- degenerate
    flag_key INT,              -- references junk dimension
    time_key INT,
    product_key INT,
    quantity INT,
    revenue DECIMAL(12,2),
    FOREIGN KEY (flag_key) REFERENCES dim_order_flags(flag_key)
);
```

## Q73: Design a retail data warehouse with both a fact_sales (transaction) and fact_inventory (snapshot) table. Show how they share dimensions.

**Answer:**
Both fact tables share `dim_date` and `dim_product` as conformed dimensions. The sales table records individual transactions while the inventory table captures periodic snapshots. This dual-fact design supports both event analysis and state analysis.

```sql
-- Shared dimensions (conformed)
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    day_of_week VARCHAR(10)
);

CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    sku VARCHAR(50),
    name VARCHAR(200),
    category VARCHAR(100),
    brand VARCHAR(100)
);

CREATE TABLE dim_store (
    store_key INT PRIMARY KEY,
    name VARCHAR(200),
    city VARCHAR(100),
    region VARCHAR(50)
);

-- Transaction fact
CREATE TABLE fact_sales (
    sale_id BIGINT PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    product_key INT REFERENCES dim_product(product_key),
    store_key INT REFERENCES dim_store(store_key),
    quantity INT,
    revenue DECIMAL(12,2),
    cost DECIMAL(12,2)
);

-- Snapshot fact
CREATE TABLE fact_inventory (
    date_key INT,
    product_key INT,
    store_key INT,
    quantity_on_hand INT,
    quantity_reserved INT,
    reorder_point INT,
    PRIMARY KEY (date_key, product_key, store_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key)
);

-- Cross-fact analysis
SELECT p.name,
       SUM(s.revenue) AS total_sales,
       AVG(i.quantity_on_hand) AS avg_stock
FROM fact_sales s
JOIN dim_product p ON s.product_key = p.product_key
JOIN fact_inventory i ON s.product_key = i.product_key AND s.date_key = i.date_key
GROUP BY p.name;
```

## Q74: Explain how to denormalize for caching derived columns with trigger-based consistency.

**Answer:**
Derived columns store precomputed results (like `total_amount = quantity × unit_price`). Triggers on the source tables automatically update the derived column when underlying data changes. This trades write overhead for read speed.

```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    total_amount DECIMAL(12,2) DEFAULT 0  -- derived, denormalized
);

CREATE TABLE order_items (
    item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- Trigger to maintain derived column
CREATE OR REPLACE FUNCTION recalculate_order_total()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE orders
    SET total_amount = COALESCE((
        SELECT SUM(quantity * unit_price)
        FROM order_items
        WHERE order_id = COALESCE(NEW.order_id, OLD.order_id)
    ), 0)
    WHERE order_id = COALESCE(NEW.order_id, OLD.order_id);
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_order_total
AFTER INSERT OR UPDATE OR DELETE ON order_items
FOR EACH ROW EXECUTE FUNCTION recalculate_order_total();

-- Now reads are fast: no join needed
SELECT order_id, total_amount FROM orders WHERE customer_id = 123;
```

## Q75: What is the difference between normalization for OLTP vs. dimensional modeling for OLAP?

**Answer:**
**OLTP normalization** (3NF/BCNF) minimizes redundancy for efficient inserts/updates/deletes and enforces integrity. **OLAP dimensional modeling** (star/snowflake) intentionally denormalizes for fast reads and intuitive business queries. OLTP optimizes for transactions; OLAP optimizes for analytics.

```sql
-- OLTP: 3NF schema
CREATE TABLE oltp_customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    city_id INT,
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

CREATE TABLE oltp_cities (
    city_id INT PRIMARY KEY,
    name VARCHAR(100),
    state_id INT,
    FOREIGN KEY (state_id) REFERENCES states(state_id)
);

-- OLAP: star schema (denormalized dimension)
CREATE TABLE dim_customer_olap (
    customer_key INT PRIMARY KEY,
    customer_id INT,
    name VARCHAR(100),
    city VARCHAR(100),       -- flattened, no JOIN needed
    state VARCHAR(100),      -- flattened
    country VARCHAR(100)     -- flattened
);
```

## Q76: Given R(A,B,C,D,E,F) with FDs: A→B, BC→D, D→E, A→F. Find all candidate keys.

**Answer:**
`A→B` and `A→F` mean `A` determines `B` and `F`. But `A` does not determine `C`, `D`, or `E` directly. `BC→D` and `D→E` mean `BC→E`. So `{A,C}` determines `B` (via A), `C`, `F` (via A), and `D` (via BC→D), then `E` (via D→E). Candidate key: `{A,C}`. Check minimality: removing `A` leaves `{C}` — `C` alone cannot determine `B`, so not a superkey. Removing `C` leaves `{A}` — `A` cannot determine `C`. So `{A,C}` is the only candidate key.

```sql
-- Verify: {A,C} is a candidate key
SELECT A, C, COUNT(*) AS dupes
FROM my_table
GROUP BY A, C
HAVING COUNT(*) > 1;
-- If 0 rows, (A,C) is a superkey

-- Check minimality: does A alone determine everything?
SELECT A, COUNT(DISTINCT C) AS c_count
FROM my_table
GROUP BY A
HAVING COUNT(DISTINCT C) > 1;
-- If rows returned, A alone is not a superkey
```

## Q77: Decompose R(A,B,C,D,E) with FDs {AB→C, C→D, D→B} into BCNF. Is it dependency-preserving?

**Answer:**
Candidate keys: `{A,B}` (since AB→C→D, AB determines everything). BCNF violation: `C→D` and `C` is not a superkey. Also `D→B` and `D` is not a superkey. Decompose on `C→D`: get `CD(C,D)` and `ABCE(A,B,C,E)`. In `ABCE`, `AB→C` still holds (AB is key). But `D→B` cannot be checked in either fragment — it's lost. This decomposition is **not** dependency-preserving.

```sql
CREATE TABLE cd (
    C INT PRIMARY KEY,
    D INT
);

CREATE TABLE abce (
    A INT,
    B INT,
    C INT,
    E INT,
    PRIMARY KEY (A, B),
    FOREIGN KEY (C) REFERENCES cd(C)
);

-- D→B cannot be enforced without joining
-- To verify dependency preservation:
SELECT CASE WHEN COUNT(*) = 0 THEN 'Preserved' ELSE 'Lost: D->B' END
FROM (
    SELECT t1.D, COUNT(DISTINCT t1.B) AS b_count
    FROM cd t1
    JOIN abce t2 ON t1.D = t2.D  -- hypothetical join
    GROUP BY t1.D
    HAVING COUNT(DISTINCT t2.B) > 1
) check_fd;
```

## Q78: Design a schema for a university system with students, courses, professors, departments, enrollments, grades, prerequisites, and office_hours. Normalize to 3NF.

**Answer:**
Separate entities: students, professors, departments (1:N), courses (N:1 to department and professor), enrollments (junction of students and courses with grade), prerequisites (M:N between courses), office_hours (1:N from professor). All relationships use foreign keys.

```sql
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    name VARCHAR(100),
    building VARCHAR(50)
);

CREATE TABLE professors (
    prof_id INT PRIMARY KEY,
    name VARCHAR(100),
    dept_id INT,
    hire_date DATE,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100),
    major_dept_id INT,
    enrollment_year INT,
    FOREIGN KEY (major_dept_id) REFERENCES departments(dept_id)
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_code VARCHAR(20) UNIQUE,
    title VARCHAR(200),
    credits INT,
    dept_id INT,
    prof_id INT,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id),
    FOREIGN KEY (prof_id) REFERENCES professors(prof_id)
);

CREATE TABLE prerequisites (
    course_id INT,
    prereq_id INT,
    PRIMARY KEY (course_id, prereq_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (prereq_id) REFERENCES courses(course_id)
);

CREATE TABLE enrollments (
    student_id INT,
    course_id INT,
    semester VARCHAR(20),
    year INT,
    grade CHAR(2),
    PRIMARY KEY (student_id, course_id, semester, year),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE office_hours (
    office_hour_id INT PRIMARY KEY,
    prof_id INT,
    day_of_week VARCHAR(10),
    start_time TIME,
    end_time TIME,
    room VARCHAR(20),
    FOREIGN KEY (prof_id) REFERENCES professors(prof_id)
);
```

## Q79: What is the impact of denormalization on write performance?

**Answer:**
Denormalization slows writes because every insert or update must maintain consistency across redundant data. This can require triggers, additional UPDATE statements, or batch synchronization jobs. In write-heavy OLTP systems, denormalization should be avoided or carefully limited. The trade-off is justified only when read performance gains outweigh write costs.

```sql
-- Denormalized: total stored with order
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    total DECIMAL(12,2)
);

-- Every item change requires updating the order total
UPDATE order_items SET quantity = 5 WHERE item_id = 10;
-- Then must also:
UPDATE orders
SET total = (SELECT SUM(quantity * unit_price) FROM order_items WHERE order_id = 100)
WHERE order_id = 100;

-- Compare: normalized (total not stored, computed on read)
SELECT SUM(quantity * unit_price) AS total
FROM order_items
WHERE order_id = 100;
-- Reads are slower (aggregation), writes are faster (no redundant update)
```

## Q80: How do you validate that a decomposition is lossless using Armstrong's axioms?

**Answer:**
Armstrong's axioms (reflexivity, augmentation, transitivity) derive all FDs from a given set. To check losslessness, compute the closure of the intersection of attributes in two fragments. If the closure of `R1 ∩ R2` includes all attributes of `R1` or `R2`, the decomposition is lossless: `R1 ∩ R2 → R1` or `R1 ∩ R2 → R2`.

```sql
-- Given FDs: A→B, B→C, C→D, and decomposition:
-- R1(A,B,C) and R2(C,D)
-- Intersection: {C}
-- Closure of C: C → D (from FD C→D), so {C}+ = {C,D}
-- This does NOT include all of R1(A,B,C), so check R2:
-- {C}+ = {C,D} includes all of R2(C,D) → lossless!

-- Verify with SQL:
-- Can we reconstruct R2 from the intersection?
SELECT COUNT(*) AS can_reconstruct
FROM (
    SELECT DISTINCT C, D FROM r2
    EXCEPT
    SELECT r1.C, r2.D FROM r1 JOIN r2 ON r1.C = r2.C
) diff;
-- If 0, the decomposition is lossless for R2
```

## Q81: What is the role of indexes in a normalized schema vs. a denormalized schema?

**Answer:**
In a **normalized schema**, indexes on foreign keys and frequently joined columns are critical for join performance. In a **denormalized schema**, indexes are less critical for joins (fewer joins needed) but important for WHERE clause filtering on the redundant columns. Denormalization trades index dependency for pre-joined data.

```sql
-- Normalized: need indexes on FKs for efficient joins
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_products_category ON products(category_id);

-- Denormalized: customer_name stored in orders
CREATE TABLE orders_denorm (
    order_id INT PRIMARY KEY,
    customer_id INT,
    customer_name VARCHAR(100),  -- denormalized
    order_date DATE
);

-- Need index only for filtering, not for joins
CREATE INDEX idx_orders_cust_name ON orders_denorm(customer_name);
-- No need for FK join index since customer_name is inline
```

## Q82: Design a banking ledger schema that supports double-entry bookkeeping in 3NF.

**Answer:**
Double-entry bookkeeping requires every transaction to have balanced debits and credits. The schema needs accounts, journal entries (header), and journal lines (details with debit/credit amounts). Each journal entry must have equal total debits and credits.

```sql
CREATE TABLE accounts (
    account_id INT PRIMARY KEY,
    account_name VARCHAR(200),
    account_type VARCHAR(20),  -- 'asset', 'liability', 'equity', 'revenue', 'expense'
    normal_balance VARCHAR(5)  -- 'debit' or 'credit'
);

CREATE TABLE journal_entries (
    entry_id INT PRIMARY KEY,
    entry_date DATE,
    description TEXT,
    created_by INT,
    posted_at TIMESTAMP
);

CREATE TABLE journal_lines (
    line_id INT PRIMARY KEY,
    entry_id INT,
    account_id INT,
    debit_amount DECIMAL(14,2) DEFAULT 0,
    credit_amount DECIMAL(14,2) DEFAULT 0,
    description VARCHAR(300),
    FOREIGN KEY (entry_id) REFERENCES journal_entries(entry_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    CHECK (debit_amount >= 0 AND credit_amount >= 0),
    CHECK (debit_amount > 0 OR credit_amount > 0)  -- at least one must be > 0
);

-- Validate balanced entries
SELECT je.entry_id,
       SUM(jl.debit_amount) AS total_debit,
       SUM(jl.credit_amount) AS total_credit,
       CASE WHEN ABS(SUM(jl.debit_amount) - SUM(jl.credit_amount)) < 0.01
            THEN 'Balanced' ELSE 'UNBALANCED' END AS status
FROM journal_entries je
JOIN journal_lines jl ON je.entry_id = jl.entry_id
GROUP BY je.entry_id
HAVING ABS(SUM(jl.debit_amount) - SUM(jl.credit_amount)) >= 0.01;
```

## Q83: How do you handle a many-to-many relationship with attributes on the relationship in a normalized schema?

**Answer:**
A many-to-many relationship with attributes is resolved with a junction (associative) table that includes the foreign keys and the relationship attributes. The junction table's PK is the composite of the FKs (plus any additional attribute needed for uniqueness).

```sql
-- Students enroll in courses with a grade and semester
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    title VARCHAR(200)
);

-- Junction with relationship attributes
CREATE TABLE enrollments (
    student_id INT,
    course_id INT,
    semester VARCHAR(20),
    year INT,
    grade DECIMAL(4,2),
    status VARCHAR(20),  -- 'enrolled', 'completed', 'dropped'
    PRIMARY KEY (student_id, course_id, semester, year),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

## Q84: What is a hierarchy bridge table and when do you use it?

**Answer:**
A hierarchy bridge table materializes recursive hierarchies (like org charts or category trees) for efficient querying without recursive CTEs. It stores every ancestor-descendant pair with the distance between them. Use it when hierarchies are deep and queried frequently.

```sql
CREATE TABLE dim_employee (
    emp_key INT PRIMARY KEY,
    emp_name VARCHAR(100),
    manager_key INT
);

-- Hierarchy bridge table
CREATE TABLE bridge_org_hierarchy (
    ancestor_key INT,
    descendant_key INT,
    distance INT,
    is_direct_report BOOLEAN,
    PRIMARY KEY (ancestor_key, descendant_key)
);

-- Populate with recursive query
INSERT INTO bridge_org_hierarchy
WITH RECURSIVE org AS (
    SELECT emp_key AS ancestor, emp_key AS descendant, 0 AS distance, TRUE AS is_direct
    FROM dim_employee
    UNION ALL
    SELECT o.ancestor, e.manager_key, o.distance + 1, FALSE
    FROM org o
    JOIN dim_employee e ON o.descendant = e.emp_key
    WHERE o.descendant != o.ancestor
)
SELECT ancestor, descendant, distance, is_direct FROM org;

-- Query: all descendants of manager 5 at any depth
SELECT e.emp_name, b.distance
FROM bridge_org_hierarchy b
JOIN dim_employee e ON b.descendant_key = e.emp_key
WHERE b.ancestor_key = 5
ORDER BY b.distance;
```

## Q85: Given a denormalized sales table, write the SQL to transform it into a 3NF schema.

**Answer:**
The denormalized table stores redundant customer, product, and region info. Transform by extracting each entity into its own table, generating surrogate keys, and populating junction/relationship tables.

```sql
-- Denormalized source
CREATE TABLE sales_raw (
    sale_id INT,
    customer_name VARCHAR(100),
    customer_email VARCHAR(200),
    customer_city VARCHAR(100),
    customer_country VARCHAR(100),
    product_name VARCHAR(200),
    product_category VARCHAR(100),
    product_price DECIMAL(10,2),
    sale_date DATE,
    quantity INT,
    salesperson VARCHAR(100)
);

-- 3NF target tables
CREATE TABLE regions (
    region_id SERIAL PRIMARY KEY,
    city VARCHAR(100),
    country VARCHAR(100),
    UNIQUE (city, country)
);

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(200),
    region_id INT,
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(200),
    category_id INT,
    price DECIMAL(10,2),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE salespersons (
    salesperson_id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    salesperson_id INT,
    sale_date DATE,
    quantity INT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (salesperson_id) REFERENCES salespersons(salesperson_id)
);

-- Transform data
INSERT INTO regions (city, country)
SELECT DISTINCT customer_city, customer_country FROM sales_raw;

INSERT INTO customers (name, email, region_id)
SELECT DISTINCT sr.customer_name, sr.customer_email, r.region_id
FROM sales_raw sr
JOIN regions r ON sr.customer_city = r.city AND sr.customer_country = r.country;

INSERT INTO categories (name)
SELECT DISTINCT product_category FROM sales_raw;

INSERT INTO products (name, category_id, price)
SELECT DISTINCT sr.product_name, c.category_id, sr.product_price
FROM sales_raw sr
JOIN categories c ON sr.product_category = c.name;

INSERT INTO salespersons (name)
SELECT DISTINCT salesperson FROM sales_raw;

INSERT INTO sales
SELECT sr.sale_id,
       cu.customer_id,
       p.product_id,
       sp.salesperson_id,
       sr.sale_date,
       sr.quantity
FROM sales_raw sr
JOIN customers cu ON sr.customer_name = cu.name
JOIN products p ON sr.product_name = p.name
JOIN salespersons sp ON sr.salesperson = sp.name;
```

## Q86: Explain how to detect and fix a schema that violates 3NF by having transitive dependencies.

**Answer:**
Detect transitive dependencies by finding non-key attributes that determine other non-key attributes. Fix by decomposing: move the determinant and its dependents to a new table, keeping the determinant as a foreign key in the original table. Verify with `GROUP BY` and `COUNT(DISTINCT ...)` queries.

```sql
-- Violation: emp_id → dept_id → dept_name (transitive)
CREATE TABLE employees_violation (
    emp_id INT PRIMARY KEY,
    name VARCHAR(100),
    dept_id INT,
    dept_name VARCHAR(100),  -- transitive dependency
    dept_location VARCHAR(100)  -- transitive dependency
);

-- Detect: test dept_id → dept_name
SELECT dept_id, COUNT(DISTINCT dept_name) AS name_variants
FROM employees_violation
GROUP BY dept_id
HAVING COUNT(DISTINCT dept_name) > 1;
-- If 0 rows, dept_id → dept_name holds (transitive through dept_id)

-- Fix: extract departments
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(100),
    location VARCHAR(100)
);

CREATE TABLE employees_fixed (
    emp_id INT PRIMARY KEY,
    name VARCHAR(100),
    dept_id INT,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

-- Migrate data
INSERT INTO departments (dept_id, dept_name, location)
SELECT DISTINCT dept_id, dept_name, dept_location
FROM employees_violation;

INSERT INTO employees_fixed (emp_id, name, dept_id)
SELECT emp_id, name, dept_id FROM employees_violation;
```

## Q87: Design an event-sourcing compatible schema for order state changes.

**Answer:**
Event sourcing stores every state change as an immutable event rather than overwriting the current state. The events table captures the full history, and the current state is derived by replaying events.

```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    current_status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Event store: append-only
CREATE TABLE order_events (
    event_id BIGSERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    event_type VARCHAR(50),  -- 'created', 'confirmed', 'shipped', 'delivered', 'cancelled'
    event_data JSONB,
    occurred_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- Get current state by latest event
SELECT o.order_id, o.current_status, e.event_type AS last_event, e.occurred_at
FROM orders o
JOIN order_events e ON o.order_id = e.order_id
WHERE e.occurred_at = (
    SELECT MAX(occurred_at) FROM order_events WHERE order_id = o.order_id
);

-- Reconstruct full history
SELECT event_type, event_data, occurred_at
FROM order_events
WHERE order_id = 1001
ORDER BY occurred_at;
```

**Alt1:** Add a projections table for materialized current state:

```sql
CREATE TABLE order_projections (
    order_id INT PRIMARY KEY,
    status VARCHAR(20),
    total_amount DECIMAL(12,2),
    last_updated TIMESTAMP,
    version INT  -- event version, for optimistic concurrency
);
```

## Q88: What is the impact of normalization on query performance?

**Answer:**
Normalization increases the number of joins required for queries, which can degrade read performance. However, smaller tables have better cache utilization, less data per page, and more efficient index scans. The net effect depends on the workload: OLTP benefits from normalization; analytical queries with many joins may suffer. Indexes and materialized views mitigate join costs.

```sql
-- Normalized: 4-way join
SELECT c.name, p.name, o.order_date, oi.quantity
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= '2025-01-01';

-- Measure with EXPLAIN ANALYZE
EXPLAIN ANALYZE
SELECT c.name, p.name, o.order_date, oi.quantity
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= '2025-01-01';

-- Denormalized alternative: pre-joined table
SELECT customer_name, product_name, order_date, quantity
FROM orders_denormalized
WHERE order_date >= '2025-01-01';
-- Faster reads, but slower writes and more storage
```

## Q89: Design a multi-tenant SaaS schema using normalization principles.

**Answer:**
Multi-tenant schemas can use shared tables with a `tenant_id` column (silo-per-row), separate schemas per tenant, or separate databases. The shared-table approach requires `tenant_id` in every table and a composite primary key including `tenant_id`.

```sql
-- Shared tables with tenant_id
CREATE TABLE tenants (
    tenant_id INT PRIMARY KEY,
    name VARCHAR(200),
    plan VARCHAR(50),
    created_at TIMESTAMP
);

CREATE TABLE users (
    tenant_id INT,
    user_id INT,
    name VARCHAR(100),
    email VARCHAR(200),
    role VARCHAR(50),
    PRIMARY KEY (tenant_id, user_id),
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
);

CREATE TABLE projects (
    tenant_id INT,
    project_id INT,
    name VARCHAR(200),
    owner_id INT,
    PRIMARY KEY (tenant_id, project_id),
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id),
    FOREIGN KEY (tenant_id, owner_id) REFERENCES users(tenant_id, user_id)
);

CREATE TABLE tasks (
    tenant_id INT,
    task_id INT,
    project_id INT,
    assignee_id INT,
    title VARCHAR(300),
    status VARCHAR(20),
    PRIMARY KEY (tenant_id, task_id),
    FOREIGN KEY (tenant_id, project_id) REFERENCES projects(tenant_id, project_id),
    FOREIGN KEY (tenant_id, assignee_id) REFERENCES users(tenant_id, user_id)
);

-- All queries must filter by tenant_id
CREATE INDEX idx_tasks_tenant_project ON tasks(tenant_id, project_id);
CREATE INDEX idx_users_tenant_email ON users(tenant_id, email);
```

## Q90: How do you handle a recursive hierarchy (org chart) in a normalized relational schema?

**Answer:**
Model with a self-referencing foreign key. Each row points to its parent. Query with recursive CTEs to traverse the hierarchy. This is the standard normalized approach for hierarchical data.

```sql
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(100),
    manager_id INT,
    FOREIGN KEY (manager_id) REFERENCES employees(emp_id)
);

-- Find all subordinates of employee 1
WITH RECURSIVE subordinates AS (
    SELECT emp_id, name, manager_id, 1 AS depth
    FROM employees
    WHERE emp_id = 1
    UNION ALL
    SELECT e.emp_id, e.name, e.manager_id, s.depth + 1
    FROM employees e
    JOIN subordinates s ON e.manager_id = s.emp_id
)
SELECT * FROM subordinates ORDER BY depth;

-- Find the management chain for employee 5
WITH RECURSIVE chain AS (
    SELECT emp_id, name, manager_id
    FROM employees WHERE emp_id = 5
    UNION ALL
    SELECT e.emp_id, e.name, e.manager_id
    FROM employees e
    JOIN chain c ON e.emp_id = c.manager_id
)
SELECT * FROM chain;
```

## Q91: What is a conformed aggregate and how does it differ from a precomputed aggregate?

**Answer:**
A **precomputed aggregate** is a summary stored in a table/materialized view for a specific query pattern (e.g., daily product revenue). A **conformed aggregate** is an aggregate that is consistent across multiple fact tables because it uses the same conformed dimensions and the same aggregation logic. Conformed aggregates enable cross-fact analysis without double-counting.

```sql
-- Precomputed: specific to one fact
CREATE TABLE daily_product_sales (
    date_key INT,
    product_key INT,
    total_revenue DECIMAL(14,2),
    PRIMARY KEY (date_key, product_key)
);

-- Conformed: uses same dimensions across facts
-- Both fact_sales and fact_returns use dim_product and dim_date
SELECT p.category,
       SUM(CASE WHEN f.type = 'sale' THEN f.amount ELSE 0 END) AS gross_sales,
       SUM(CASE WHEN f.type = 'return' THEN f.amount ELSE 0 END) AS returns,
       SUM(CASE WHEN f.type = 'sale' THEN f.amount ELSE 0 END) -
       SUM(CASE WHEN f.type = 'return' THEN f.amount ELSE 0 END) AS net_sales
FROM fact_transactions f
JOIN dim_product p ON f.product_key = p.product_key
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2025
GROUP BY p.category;
```

## Q92: Design a hospital appointment system schema that supports room scheduling without conflicts.

**Answer:**
The schema needs rooms, doctors, patients, and appointments. A constraint ensures no two appointments overlap in the same room at the same time. This requires checking for time range overlaps.

```sql
CREATE TABLE rooms (
    room_id INT PRIMARY KEY,
    room_number VARCHAR(20) UNIQUE,
    room_type VARCHAR(50),
    floor INT
);

CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY,
    name VARCHAR(100),
    specialty VARCHAR(100)
);

CREATE TABLE patients (
    patient_id INT PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20)
);

CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    room_id INT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id),
    CHECK (end_time > start_time)
);

-- Prevent room conflicts with a partial unique index (PostgreSQL)
CREATE UNIQUE INDEX idx_no_room_overlap
ON appointments (room_id, start_time)
WHERE end_time IS NOT NULL;

-- Check for existing conflicts before insert
SELECT a.appointment_id, a.start_time, a.end_time
FROM appointments a
WHERE a.room_id = 201
  AND a.start_time < '2025-09-15 15:00:00'
  AND a.end_time > '2025-09-15 14:00:00';
-- If any rows returned, there is a conflict
```

## Q93: What is the difference between vertical and horizontal partitioning and how do they relate to normalization?

**Answer:**
**Vertical partitioning** splits a table by columns (like normalization splits by entities). It separates frequently accessed columns from rarely accessed ones. **Horizontal partitioning** splits a table by rows (e.g., by date range or tenant). Normalization is a logical design principle; partitioning is a physical storage optimization that can complement normalization.

```sql
-- Vertical partitioning: split wide table
-- Before: one wide table
CREATE TABLE users_wide (
    user_id INT PRIMARY KEY,
    name VARCHAR(100),
    bio TEXT,
    profile_pic BYTEA,
    preferences JSONB
);

-- After: split hot/cold data
CREATE TABLE users_core (
    user_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE users_profile (
    user_id INT PRIMARY KEY REFERENCES users_core(user_id),
    bio TEXT,
    profile_pic BYTEA,
    preferences JSONB
);

-- Horizontal partitioning (PostgreSQL)
CREATE TABLE logs (
    log_id BIGSERIAL,
    user_id INT,
    action VARCHAR(100),
    created_at TIMESTAMP
) PARTITION BY RANGE (created_at);

CREATE TABLE logs_2025_q1 PARTITION OF logs
    FOR VALUES FROM ('2025-01-01') TO ('2025-04-01');

CREATE TABLE logs_2025_q2 PARTITION OF logs
    FOR VALUES FROM ('2025-04-01') TO ('2025-07-01');
```

## Q94: How do you denormalize a normalized schema for a search-heavy application?

**Answer:**
For search-heavy applications, denormalize by creating a flattened search table that concatenates related fields into a single searchable row. This avoids multi-table joins at query time. Use full-text indexes or search engine sync (Elasticsearch) for advanced search.

```sql
-- Normalized schema
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name VARCHAR(200),
    category_id INT,
    brand_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id)
);

CREATE TABLE product_tags (
    product_id INT,
    tag VARCHAR(50),
    PRIMARY KEY (product_id, tag)
);

-- Denormalized search table
CREATE TABLE product_search (
    product_id INT PRIMARY KEY,
    search_text TEXT,  -- concatenated name, category, brand, tags
    category_name VARCHAR(100),
    brand_name VARCHAR(100),
    price DECIMAL(10,2),
    updated_at TIMESTAMP
);

-- Populate search table
INSERT INTO product_search (product_id, search_text, category_name, brand_name, price)
SELECT
    p.product_id,
    p.name || ' ' || c.name || ' ' || b.name || ' ' ||
    COALESCE(string_agg(t.tag, ' '), ''),
    c.name,
    b.name,
    p.price
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN brands b ON p.brand_id = b.brand_id
LEFT JOIN product_tags t ON p.product_id = t.product_id
GROUP BY p.product_id, p.name, c.name, b.name, p.price;

-- Full-text search
CREATE INDEX idx_search ON product_search USING GIN (to_tsvector('english', search_text));

SELECT * FROM product_search
WHERE to_tsvector('english', search_text) @@ plainto_tsquery('english', 'wireless headphones');
```

## Q95: Design a data mart for a hospital with dimensions: date, doctor, department, patient, procedure and facts: visits and billing.

**Answer:**
A hospital data mart follows a star schema with conformed dimensions. The visits fact captures clinical events; the billing fact captures financial events. Both share date, doctor, department, and patient dimensions.

```sql
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    day_of_week VARCHAR(10)
);

CREATE TABLE dim_doctor (
    doctor_key INT PRIMARY KEY,
    doctor_id INT,
    name VARCHAR(100),
    specialty VARCHAR(100),
    department_key INT
);

CREATE TABLE dim_department (
    department_key INT PRIMARY KEY,
    department_name VARCHAR(100),
    floor INT,
    head_doctor_key INT
);

CREATE TABLE dim_patient (
    patient_key INT PRIMARY KEY,
    patient_id INT,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    insurance_type VARCHAR(50)
);

CREATE TABLE dim_procedure (
    procedure_key INT PRIMARY KEY,
    procedure_code VARCHAR(20),
    procedure_name VARCHAR(200),
    category VARCHAR(100),
    base_cost DECIMAL(10,2)
);

CREATE TABLE fact_visits (
    visit_key BIGINT PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    doctor_key INT REFERENCES dim_doctor(doctor_key),
    department_key INT REFERENCES dim_department(department_key),
    patient_key INT REFERENCES dim_patient(patient_key),
    procedure_key INT REFERENCES dim_procedure(procedure_key),
    duration_minutes INT,
    diagnosis_count INT,
    is_emergency BOOLEAN
);

CREATE TABLE fact_billing (
    billing_key BIGINT PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    patient_key INT REFERENCES dim_patient(patient_key),
    procedure_key INT REFERENCES dim_procedure(procedure_key),
    department_key INT REFERENCES dim_department(department_key),
    charge_amount DECIMAL(12,2),
    insurance_paid DECIMAL(12,2),
    patient_paid DECIMAL(12,2),
    adjustment_amount DECIMAL(10,2)
);

-- Cross-fact query
SELECT dept.department_name,
       SUM(b.charge_amount) AS total_charges,
       COUNT(v.visit_key) AS total_visits
FROM fact_billing b
JOIN dim_department dept ON b.department_key = dept.department_key
JOIN fact_visits v ON b.patient_key = v.patient_key AND b.date_key = v.date_key
GROUP BY dept.department_name;
```

## Q96: What are the key differences between 3NF and star schema design?

**Answer:**
3NF eliminates all redundancy through decomposition; star schema intentionally introduces redundancy (denormalized dimensions) for query simplicity. 3NF uses composite FKs and many-to-many junctions; star schema uses single FKs from fact to dimension. 3NF is for OLTP; star schema is for OLAP/data warehousing.

```sql
-- 3NF: normalized
CREATE TABLE orders_3nf (
    order_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    store_id INT,
    date_id INT,
    quantity INT,
    revenue DECIMAL(12,2)
);

-- Star schema: denormalized dimensions
CREATE TABLE fact_orders_star (
    order_id BIGINT PRIMARY KEY,
    date_key INT,
    customer_key INT,
    product_key INT,
    store_key INT,
    quantity INT,
    revenue DECIMAL(12,2)
);

CREATE TABLE dim_customer_star (
    customer_key INT PRIMARY KEY,
    name VARCHAR(200),
    email VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(50),
    country VARCHAR(100),
    segment VARCHAR(50)
);

-- 3NF requires joining through city → state → country tables
-- Star schema: all customer attributes in one row
```

## Q97: Given R(A,B,C,D) with FDs: A→B, B→C, C→D, D→A. What is the candidate key and what normal form?

**Answer:**
Every attribute determines every other attribute through the cycle: A→B→C→D→A. So `{A}` is a superkey (and candidate key), and so is `{B}`, `{C}`, `{D}`. There are four candidate keys, each a single attribute. The table is in BCNF because every determinant (A, B, C, D) is a candidate key.

```sql
-- All four are candidate keys
CREATE TABLE r_abcd (
    A INT PRIMARY KEY,
    B INT UNIQUE,
    C INT UNIQUE,
    D INT UNIQUE
);

-- In BCNF: every determinant is a superkey
-- No decomposition needed; already in BCNF
```

## Q98: How do you denormalize for a read-heavy cache layer in a web application?

**Answer:**
Create a cache table (or materialized view) that pre-joins and pre-aggregates data for specific API endpoints. Populate it asynchronously (via triggers, CDC, or scheduled jobs). Invalidate and refresh when source data changes.

```sql
-- Cache table for user dashboard
CREATE TABLE user_dashboard_cache (
    user_id INT PRIMARY KEY,
    display_name VARCHAR(100),
    total_orders INT,
    total_spent DECIMAL(14,2),
    last_order_date DATE,
    favorite_category VARCHAR(100),
    loyalty_tier VARCHAR(20),
    refreshed_at TIMESTAMP
);

-- Refresh via scheduled job
INSERT INTO user_dashboard_cache
SELECT
    u.user_id,
    u.name,
    COUNT(DISTINCT o.order_id),
    COALESCE(SUM(oi.quantity * oi.unit_price), 0),
    MAX(o.order_date),
    MODE() WITHIN GROUP (ORDER BY p.category),
    CASE
        WHEN SUM(oi.quantity * oi.unit_price) > 10000 THEN 'gold'
        WHEN SUM(oi.quantity * oi.unit_price) > 5000 THEN 'silver'
        ELSE 'bronze'
    END,
    NOW()
FROM users u
LEFT JOIN orders o ON u.user_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.product_id
GROUP BY u.user_id, u.name
ON CONFLICT (user_id) DO UPDATE
SET total_orders = EXCLUDED.total_orders,
    total_spent = EXCLUDED.total_spent,
    last_order_date = EXCLUDED.last_order_date,
    favorite_category = EXCLUDED.favorite_category,
    loyalty_tier = EXCLUDED.loyalty_tier,
    refreshed_at = NOW();
```

## Q99: Design a complete ecommerce data warehouse: fact tables for orders, returns, and page_views with shared dimensions.

**Answer:**
Three fact tables share conformed dimensions (date, product, customer, channel). Orders and returns are transaction facts; page_views are events with lower grain. Each fact has measures specific to its business process.

```sql
-- Conformed dimensions
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    week INT,
    day_of_week VARCHAR(10)
);

CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    sku VARCHAR(50),
    name VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    unit_cost DECIMAL(10,2)
);

CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY,
    customer_id INT,
    name VARCHAR(200),
    segment VARCHAR(50),
    city VARCHAR(100),
    country VARCHAR(100)
);

CREATE TABLE dim_channel (
    channel_key INT PRIMARY KEY,
    channel_name VARCHAR(50),  -- 'web', 'mobile', 'store', 'marketplace'
    device_type VARCHAR(20),
    platform VARCHAR(20)
);

-- Fact: orders
CREATE TABLE fact_orders (
    order_key BIGINT PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    product_key INT REFERENCES dim_product(product_key),
    customer_key INT REFERENCES dim_customer(customer_key),
    channel_key INT REFERENCES dim_channel(channel_key),
    order_number VARCHAR(50),
    quantity INT,
    revenue DECIMAL(12,2),
    cost DECIMAL(12,2),
    discount DECIMAL(10,2)
);

-- Fact: returns
CREATE TABLE fact_returns (
    return_key BIGINT PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    product_key INT REFERENCES dim_product(product_key),
    customer_key INT REFERENCES dim_customer(customer_key),
    order_key BIGINT,
    return_reason VARCHAR(100),
    return_quantity INT,
    refund_amount DECIMAL(12,2)
);

-- Fact: page views (higher grain, one row per view)
CREATE TABLE fact_page_views (
    view_key BIGINT PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    product_key INT REFERENCES dim_product(product_key),
    customer_key INT REFERENCES dim_customer(customer_key),
    channel_key INT REFERENCES dim_channel(channel_key),
    session_id VARCHAR(100),
    page_url VARCHAR(500),
    time_on_page_sec INT,
    bounce BOOLEAN
);

-- Cross-fact: return rate by category
SELECT p.category,
       SUM(o.quantity) AS total_sold,
       COALESCE(SUM(r.return_quantity), 0) AS total_returned,
       ROUND(COALESCE(SUM(r.return_quantity), 0)::DECIMAL / NULLIF(SUM(o.quantity), 0) * 100, 2) AS return_rate_pct
FROM fact_orders o
JOIN dim_product p ON o.product_key = p.product_key
LEFT JOIN fact_returns r ON o.product_key = r.product_key AND o.date_key = r.date_key
GROUP BY p.category;
```

## Q100: Given a complete ecommerce schema, perform a full normalization audit: identify violations, decompose step-by-step from UNF to 3NF, and write validation queries for each step.

**Answer:**
Perform a systematic audit: (1) Check 1NF by looking for multi-valued columns and repeating groups. (2) Check 2NF by testing partial dependencies on composite keys. (3) Check 3NF by testing transitive dependencies. (4) Write validation queries for each step.

```sql
-- ====== STEP 0: UNF raw table ======
CREATE TABLE ecommerce_raw (
    order_id INT,
    order_date DATE,
    customer_name VARCHAR(100),
    customer_email VARCHAR(200),
    customer_city VARCHAR(100),
    product_name VARCHAR(200),
    product_category VARCHAR(100),
    product_price DECIMAL(10,2),
    quantity INT,
    payment_method VARCHAR(20),
    shipping_city VARCHAR(100)
);

-- ====== STEP 1: Check 1NF ======
-- Check for multi-valued columns
SELECT order_id, product_name
FROM ecommerce_raw
WHERE product_name LIKE '%,%';
-- If rows returned, violates 1NF

-- Check for repeating groups (product1, product2, etc.)
SELECT column_name FROM information_schema.columns
WHERE table_name = 'ecommerce_raw' AND column_name LIKE 'product%';
-- If multiple product columns exist, violates 1NF

-- ====== STEP 2: Check 2NF (after flattening to 1NF) ======
-- Assuming PK is (order_id, product_name)
-- Test: customer_name depends only on order_id (partial)
SELECT order_id, COUNT(DISTINCT customer_name) AS name_variants
FROM ecommerce_raw
GROUP BY order_id
HAVING COUNT(DISTINCT customer_name) > 1;
-- If 0 rows, customer_name → order_id (partial dependency detected)

-- Test: product_category depends only on product_name (partial)
SELECT product_name, COUNT(DISTINCT product_category) AS cat_variants
FROM ecommerce_raw
GROUP BY product_name
HAVING COUNT(DISTINCT product_category) > 1;
-- If 0 rows, product_name → product_category (partial dependency)

-- ====== STEP 3: Check 3NF ======
-- Test: customer_city depends on customer_name (transitive if customer_name → customer_id → city)
SELECT customer_name, COUNT(DISTINCT customer_city) AS city_variants
FROM ecommerce_raw
GROUP BY customer_name
HAVING COUNT(DISTINCT customer_city) > 1;
-- If 0 rows, customer_name → customer_city (potential transitive dependency)

-- ====== STEP 4: Decompose ======
CREATE TABLE dim_customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(200),
    city VARCHAR(100)
);

CREATE TABLE dim_products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(200),
    category VARCHAR(100),
    price DECIMAL(10,2)
);

CREATE TABLE dim_payments (
    payment_method VARCHAR(20) PRIMARY KEY
);

CREATE TABLE fact_orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    payment_method VARCHAR(20),
    shipping_city VARCHAR(100),
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
    FOREIGN KEY (payment_method) REFERENCES dim_payments(payment_method)
);

CREATE TABLE fact_order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES fact_orders(order_id),
    FOREIGN KEY (product_id) REFERENCES dim_products(product_id)
);

-- ====== STEP 5: Validate decomposition ======
-- Lossless join check
SELECT COUNT(*) AS original_count FROM ecommerce_raw;
SELECT COUNT(*) AS reconstructed_count
FROM fact_order_items fi
JOIN fact_orders fo ON fi.order_id = fo.order_id
JOIN dim_customers dc ON fo.customer_id = dc.customer_id
JOIN dim_products dp ON fi.product_id = dp.product_id;

-- Dependency preservation check: customer_name → customer_city
SELECT CASE WHEN COUNT(*) = 0 THEN 'PRESERVED' ELSE 'VIOLATED' END
FROM (
    SELECT customer_id, COUNT(DISTINCT city) AS city_count
    FROM dim_customers
    GROUP BY customer_id
    HAVING COUNT(DISTINCT city) > 1
) v;

-- Anomaly check: no orphaned foreign keys
SELECT fo.order_id
FROM fact_orders fo
LEFT JOIN dim_customers dc ON fo.customer_id = dc.customer_id
WHERE dc.customer_id IS NULL;
-- Should return 0 rows
```
