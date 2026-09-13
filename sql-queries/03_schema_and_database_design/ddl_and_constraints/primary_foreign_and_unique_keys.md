# Primary, Foreign and Unique Keys — 100 SQL Interview Q&A

## Q1: Create a table with a single-column integer primary key.

**Query:**
```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(255)
);
```
**Explanation:** The `PRIMARY KEY` inline constraint marks `customer_id` as the unique identifier; it implicitly adds NOT NULL and a unique index.

**Alt1:**
```sql
-- MySQL
CREATE TABLE customers (
    customer_id INT NOT NULL,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(255),
    PRIMARY KEY (customer_id)
);
```
**Explanation:** MySQL also supports the table-level `PRIMARY KEY` syntax, which is functionally identical.

---

## Q2: Create a table with a composite primary key on two columns.

**Query:**
```sql
CREATE TABLE enrollments (
    student_id INT NOT NULL,
    course_id  INT NOT NULL,
    enrolled_on DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (student_id, course_id)
);
```
**Explanation:** A composite primary key ensures the combination of `student_id` and `course_id` is unique; each column alone can repeat.

---

## Q3: Add a primary key to an existing table using ALTER TABLE.

**Query:**
```sql
ALTER TABLE legacy_users
    ADD CONSTRAINT pk_legacy_users PRIMARY KEY (user_id);
```
**Explanation:** Adding a named PK constraint after creation lets you control the constraint name and is the standard approach across all major RDBMS.

---

## Q4: Create a table where the primary key is a UUID.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE documents (
    doc_id  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title   VARCHAR(255) NOT NULL,
    body    TEXT
);
```
**Explanation:** `gen_random_uuid()` generates a v4 UUID automatically on insert, avoiding sequential ID guessability and enabling distributed key generation.

**Alt1:**
```sql
-- MySQL 8.0+
CREATE TABLE documents (
    doc_id  BINARY(16) PRIMARY KEY DEFAULT (UUID_TO_BIN(UUID(), 1)),
    title   VARCHAR(255) NOT NULL,
    body    TEXT
);
```
**Explanation:** MySQL stores UUIDs as `BINARY(16)` for efficiency; the `1` argument stores time-ordered bytes first for better index performance.

---

## Q5: Define a foreign key that references the primary key of another table.

**Query:**
```sql
CREATE TABLE orders (
    order_id    INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date  DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);
```
**Explanation:** The `FOREIGN KEY … REFERENCES` clause enforces that every `customer_id` in `orders` must exist in `customers`.

**Alt1:**
```sql
-- SQL Server
CREATE TABLE dbo.orders (
    order_id    INT PRIMARY KEY,
    customer_id INT NOT NULL,
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id) REFERENCES dbo.customers (customer_id)
);
```
**Explanation:** SQL Server requires `CONSTRAINT` naming for table-level FKs; the schema-qualified name avoids ambiguity.

---

## Q6: Create an inline foreign key constraint.

**Query:**
```sql
CREATE TABLE order_items (
    item_id   INT PRIMARY KEY,
    order_id  INT NOT NULL REFERENCES orders (order_id),
    product_id INT NOT NULL,
    quantity  INT DEFAULT 1
);
```
**Explanation:** Inline `REFERENCES` is concise but cannot carry `ON DELETE` or `ON UPDATE` actions; use table-level syntax for those.

---

## Q7: Add a foreign key to an existing table.

**Query:**
```sql
ALTER TABLE orders
    ADD CONSTRAINT fk_orders_customer
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id);
```
**Explanation:** The named constraint makes future drops or modifications predictable; the table must already have matching values or be empty.

**Alt1:**
```sql
-- MySQL
ALTER TABLE orders
    ADD FOREIGN KEY (customer_id) REFERENCES customers (customer_id);
```
**Explanation:** MySQL generates a name like `orders_ibfk_1` when you omit `CONSTRAINT`, which makes later maintenance harder.

---

## Q8: Create a foreign key with ON DELETE CASCADE.

**Query:**
```sql
CREATE TABLE order_items (
    item_id    INT PRIMARY KEY,
    order_id   INT NOT NULL,
    product_id INT NOT NULL,
    quantity   INT DEFAULT 1,
    FOREIGN KEY (order_id) REFERENCES orders (order_id)
        ON DELETE CASCADE
);
```
**Explanation:** When a parent row in `orders` is deleted, all child rows in `order_items` are automatically deleted.

**Alt1:**
```sql
-- Oracle
CREATE TABLE order_items (
    item_id    NUMBER(8) PRIMARY KEY,
    order_id   NUMBER(8) NOT NULL,
    quantity   NUMBER(4) DEFAULT 1,
    CONSTRAINT fk_item_order FOREIGN KEY (order_id)
        REFERENCES orders (order_id) ON DELETE CASCADE
);
```
**Explanation:** Oracle boosts maintainability by naming the constraint inline with the FK definition.

---

## Q9: Create a foreign key with ON DELETE SET NULL.

**Query:**
```sql
CREATE TABLE employees (
    emp_id        INT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments (department_id)
        ON DELETE SET NULL
);
```
**Explanation:** If the referenced department is deleted, `department_id` becomes NULL rather than the row being removed.

---

## Q10: Create a foreign key with ON UPDATE CASCADE.

**Query:**
```sql
CREATE TABLE order_items (
    item_id    INT PRIMARY KEY,
    order_id   INT NOT NULL,
    product_id INT NOT NULL,
    quantity   INT DEFAULT 1,
    FOREIGN KEY (order_id) REFERENCES orders (order_id)
        ON UPDATE CASCADE
);
```
**Explanation:** If a parent `order_id` changes, every child row's `order_id` is updated automatically to match.

**Alt1:**
```sql
-- SQL Server
CREATE TABLE order_items (
    item_id    INT PRIMARY KEY,
    order_id   INT NOT NULL,
    product_id INT NOT NULL,
    quantity   INT DEFAULT 1,
    CONSTRAINT fk_item_order FOREIGN KEY (order_id)
        REFERENCES orders (order_id) ON UPDATE CASCADE
);
```
**Explanation:** SQL Server supports `ON UPDATE CASCADE` identically but requires a named constraint for the inline FK.

---

## Q11: Create a foreign key with ON DELETE SET DEFAULT.

**Query:**
```sql
-- SQL Server
CREATE TABLE employees (
    emp_id        INT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    department_id INT DEFAULT 1,
    FOREIGN KEY (department_id) REFERENCES departments (department_id)
        ON DELETE SET DEFAULT
);
```
**Explanation:** On department deletion, `department_id` is set to the column's default (1). The default value must itself exist in the parent table.

**Alt1:**
```sql
-- PostgreSQL
CREATE TABLE employees (
    emp_id        INT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    department_id INT DEFAULT 1,
    FOREIGN KEY (department_id) REFERENCES departments (department_id)
        ON DELETE SET DEFAULT
);
```
**Explanation:** PostgreSQL supports `SET DEFAULT` similarly; ensure the default value exists in the parent or the delete will fail.

---

## Q12: Create a foreign key with ON DELETE RESTRICT.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE order_items (
    item_id    INT PRIMARY KEY,
    order_id   INT NOT NULL,
    product_id INT NOT NULL,
    quantity   INT DEFAULT 1,
    FOREIGN KEY (order_id) REFERENCES orders (order_id)
        ON DELETE RESTRICT
);
```
**Explanation:** `RESTRICT` prevents deletion of the parent row if any child rows reference it; the delete fails immediately.

---

## Q13: Demonstrate NO ACTION vs RESTRICT.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE invoices (
    invoice_id  INT PRIMARY KEY,
    customer_id INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        ON DELETE NO ACTION
);
```
**Explanation:** In PostgreSQL, `NO ACTION` (the default) checks at the end of the transaction, while `RESTRICT` checks immediately; both block the delete if a child exists.

**Alt1:**
```sql
-- SQL Server — NO ACTION and RESTRICT are equivalent
CREATE TABLE invoices (
    invoice_id  INT PRIMARY KEY,
    customer_id INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        ON DELETE NO ACTION
);
```
**Explanation:** SQL Server treats `NO ACTION` and `RESTRICT` identically; both prevent deletion of referenced parent rows.

---

## Q14: Create a UNIQUE constraint on a single column.

**Query:**
```sql
CREATE TABLE users (
    user_id  INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email    VARCHAR(255) NOT NULL
);
```
**Explanation:** The `UNIQUE` inline constraint creates an implicit unique index and ensures no duplicate values in `username`.

**Alt1:**
```sql
CREATE TABLE users (
    user_id  INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email    VARCHAR(255) NOT NULL,
    CONSTRAINT uq_users_username UNIQUE (username)
);
```
**Explanation:** The table-level form lets you name the constraint and group it with other constraints logically.

---

## Q15: Create a table-level UNIQUE constraint.

**Query:**
```sql
CREATE TABLE users (
    user_id  INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email    VARCHAR(255) NOT NULL,
    CONSTRAINT uq_users_username UNIQUE (username),
    CONSTRAINT uq_users_email    UNIQUE (email)
);
```
**Explanation:** Named table-level constraints improve readability and make `DROP CONSTRAINT` calls explicit.

---

## Q16: Add a UNIQUE constraint to an existing column.

**Query:**
```sql
ALTER TABLE users
    ADD CONSTRAINT uq_users_email UNIQUE (email);
```
**Explanation:** The database verifies existing data has no duplicates before applying the constraint; if duplicates exist the ALTER fails.

---

## Q17: Create a composite UNIQUE constraint.

**Query:**
```sql
CREATE TABLE room_bookings (
    room_id    INT NOT NULL,
    booking_date DATE NOT NULL,
    guest_name VARCHAR(100),
    CONSTRAINT uq_room_date UNIQUE (room_id, booking_date)
);
```
**Explanation:** The composite UNIQUE ensures one booking per room per date; individual columns can repeat across different rows.

---

## Q18: Explain how UNIQUE differs from PRIMARY KEY.

**Query:**
```sql
CREATE TABLE products (
    sku         VARCHAR(20) PRIMARY KEY,
    barcode     VARCHAR(20) UNIQUE,
    name        VARCHAR(200) NOT NULL,
    price       DECIMAL(10,2)
);
```
**Explanation:** A table can have only one PRIMARY KEY but multiple UNIQUE constraints; PK columns cannot be NULL while UNIQUE columns can (except in some RDBMS where only one NULL is allowed).

---

## Q19: Demonstrate NULL behavior in UNIQUE constraints (MySQL).

**Query:**
```sql
-- MySQL (InnoDB)
CREATE TABLE tags (
    tag_id   INT PRIMARY KEY,
    tag_name VARCHAR(50) UNIQUE
);

INSERT INTO tags VALUES (1, 'sql');
INSERT INTO tags VALUES (2, NULL);
INSERT INTO tags VALUES (3, NULL);
```
**Explanation:** MySQL allows multiple NULLs in a UNIQUE column because NULL != NULL per the SQL standard; no duplicate is detected.

---

## Q20: Demonstrate NULL behavior in UNIQUE constraints (PostgreSQL).

**Query:**
```sql
-- PostgreSQL
CREATE TABLE tags (
    tag_id   INT PRIMARY KEY,
    tag_name VARCHAR(50) UNIQUE
);

INSERT INTO tags VALUES (1, 'sql');
INSERT INTO tags VALUES (2, NULL);
INSERT INTO tags VALUES (3, NULL);
```
**Explanation:** PostgreSQL also allows multiple NULLs in a UNIQUE column, consistent with the SQL standard treating NULLs as incomparable.

---

## Q21: Demonstrate NULL behavior in UNIQUE constraints (SQL Server).

**Query:**
```sql
-- SQL Server
CREATE TABLE tags (
    tag_id   INT PRIMARY KEY,
    tag_name VARCHAR(50) UNIQUE
);

INSERT INTO tags VALUES (1, 'sql');
INSERT INTO tags VALUES (2, NULL);
INSERT INTO tags VALUES (3, NULL);
```
**Explanation:** SQL Server permits multiple NULLs in a UNIQUE column because NULL is not considered equal to NULL.

---

## Q22: Demonstrate NULL behavior in UNIQUE constraints (Oracle).

**Query:**
```sql
-- Oracle
CREATE TABLE tags (
    tag_id   NUMBER PRIMARY KEY,
    tag_name VARCHAR2(50) UNIQUE
);

INSERT INTO tags VALUES (1, 'sql');
INSERT INTO tags VALUES (2, NULL);
INSERT INTO tags VALUES (3, NULL);
```
**Explanation:** Oracle allows multiple NULLs in a UNIQUE column, following the SQL standard; two NULLs are never duplicates.

---

## Q23: Create a UNIQUE INDEX explicitly instead of a UNIQUE constraint.

**Query:**
```sql
CREATE UNIQUE INDEX idx_users_email ON users (email);
```
**Explanation:** A unique index enforces uniqueness like a UNIQUE constraint but is not listed in `information_schema.table_constraints`; use constraints for logical design and indexes for performance.

---

## Q24: Drop a UNIQUE constraint by name.

**Query:**
```sql
ALTER TABLE users
    DROP CONSTRAINT uq_users_email;
```
**Explanation:** Dropping the constraint removes the uniqueness enforcement; existing duplicate values are not retroactively checked.

---

## Q25: Drop a unique index.

**Query:**
```sql
-- PostgreSQL
DROP INDEX idx_users_email;
```
**Explanation:** `DROP INDEX` removes the unique index; unlike dropping a constraint, this is purely an index-level operation.

**Alt1:**
```sql
-- MySQL
DROP INDEX idx_users_email ON users;
```
**Explanation:** MySQL requires the table name in the `DROP INDEX` statement.

## Q26: Drop a primary key along with the implicit index (PostgreSQL).

**Query:**
```sql
-- PostgreSQL
ALTER TABLE customers
    DROP CONSTRAINT customers_pkey;
```
**Explanation:** Dropping the PK constraint automatically drops the backing unique index; the constraint name follows the `<table>_<column>_pkey` convention.

**Alt1:**
```sql
-- Oracle
ALTER TABLE customers
    DROP CONSTRAINT sys_c001234;
```
**Explanation:** Oracle auto-generates constraint names (e.g. `SYS_C001234`); query `USER_CONSTRAINTS` to find the actual name before dropping.

---

## Q27: Create a unique index on multiple columns.

**Query:**
```sql
CREATE UNIQUE INDEX idx_pairs ON mappings (source_id, target_id);
```
**Explanation:** A composite unique index enforces that the pair `(source_id, target_id)` is unique across the table.

---

## Q28: Create a foreign key referencing a UNIQUE column instead of the primary key.

**Query:**
```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    ssn         VARCHAR(11) UNIQUE,
    name        VARCHAR(100) NOT NULL
);

CREATE TABLE credit_reports (
    report_id INT PRIMARY KEY,
    ssn       VARCHAR(11) NOT NULL,
    score     INT,
    FOREIGN KEY (ssn) REFERENCES customers (ssn)
);
```
**Explanation:** A foreign key can reference any column or column set with a UNIQUE constraint, not just the primary key.

---

## Q29: Alter a table to add a composite foreign key referencing a composite unique key.

**Query:**
```sql
ALTER TABLE deliveries
    ADD CONSTRAINT fk_deliveries_orders
    FOREIGN KEY (region, route_id)
    REFERENCES routes (region, route_id);
```
**Explanation:** The referencing columns must match the referenced unique key columns in number and data type.

---

## Q30: Create a self-referencing foreign key for an employee-manager hierarchy.

**Query:**
```sql
CREATE TABLE employees (
    emp_id        INT PRIMARY KEY,
    manager_id    INT,
    name          VARCHAR(100) NOT NULL,
    FOREIGN KEY (manager_id) REFERENCES employees (emp_id)
);
```
**Explanation:** A self-referencing FK lets a row point at another row within the same table, modelling trees like manager chains.

**Alt1:**
```sql
-- Oracle
CREATE TABLE employees (
    emp_id     NUMBER(6) PRIMARY KEY,
    manager_id NUMBER(6),
    name       VARCHAR2(100) NOT NULL,
    CONSTRAINT fk_emp_manager FOREIGN KEY (manager_id)
        REFERENCES employees (emp_id)
);
```
**Explanation:** Oracle requires the constraint to reference the same table explicitly via a named constraint declaration.

---

## Q31: Create a self-referencing FK with ON DELETE SET NULL to protect the hierarchy root.

**Query:**
```sql
CREATE TABLE employees (
    emp_id        INT PRIMARY KEY,
    manager_id    INT,
    name          VARCHAR(100) NOT NULL,
    FOREIGN KEY (manager_id) REFERENCES employees (emp_id)
        ON DELETE SET NULL
);
```
**Explanation:** Deleting a manager sets subordinates' `manager_id` to NULL instead of failing or cascading away the whole tree.

---

## Q32: Create two tables that reference each other (FK cycle) with deferrable constraints.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE authors (
    author_id    INT PRIMARY KEY,
    favorite_book_id INT
);

CREATE TABLE books (
    book_id      INT PRIMARY KEY,
    author_id    INT NOT NULL
);

ALTER TABLE authors
    ADD CONSTRAINT fk_authors_book
    FOREIGN KEY (favorite_book_id) REFERENCES books (book_id)
    DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE books
    ADD CONSTRAINT fk_books_author
    FOREIGN KEY (author_id) REFERENCES authors (author_id);
```
**Explanation:** The cycle requires at least one `DEFERRABLE INITIALLY DEFERRED` constraint so both inserts can complete before constraints are checked at commit.

---

## Q33: Use SET CONSTRAINTS to defer a foreign key check mid-transaction.

**Query:**
```sql
-- PostgreSQL
BEGIN;
SET CONSTRAINTS fk_authors_book DEFERRED;

INSERT INTO authors (author_id, favorite_book_id)
VALUES (1, 10);
INSERT INTO books (book_id, author_id)
VALUES (10, 1);

COMMIT;
```
**Explanation:** Deferring the cyclic FK lets the transaction insert rows referencing not-yet-existing rows; checks run at COMMIT time.

---

## Q34: Demonstrate ON DELETE CASCADE ordering across two levels.

**Query:**
```sql
CREATE TABLE regions (
    region_id INT PRIMARY KEY
);

CREATE TABLE countries (
    country_id INT PRIMARY KEY,
    region_id  INT NOT NULL,
    FOREIGN KEY (region_id) REFERENCES regions (region_id)
        ON DELETE CASCADE
);

CREATE TABLE cities (
    city_id    INT PRIMARY KEY,
    country_id INT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES countries (country_id)
        ON DELETE CASCADE
);
```
**Explanation:** Deleting a region cascades to countries and then to cities; cascading deletes propagate through the chain automatically.

---

## Q35: Prevent a delete while child rows exist using default behavior.

**Query:**
```sql
-- PostgreSQL (NO ACTION is the default)
CREATE TABLE customers (
    customer_id INT PRIMARY KEY
);

CREATE TABLE orders (
    order_id    INT PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers (customer_id)
);

DELETE FROM customers WHERE customer_id = 1;
```
**Explanation:** The DELETE fails with a foreign key violation because default `NO ACTION` blocks deletion while `orders` rows reference the customer.

---

## Q36: Create a foreign key with a composite key referencing a composite primary key.

**Query:**
```sql
CREATE TABLE seats (
    aircraft_id   INT NOT NULL,
    seat_number   VARCHAR(3) NOT NULL,
    is_available  BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (aircraft_id, seat_number)
);

CREATE TABLE bookings (
    booking_id    INT PRIMARY KEY,
    aircraft_id   INT NOT NULL,
    seat_number   VARCHAR(3) NOT NULL,
    passenger     VARCHAR(100),
    FOREIGN KEY (aircraft_id, seat_number)
        REFERENCES seats (aircraft_id, seat_number)
);
```
**Explanation:** The child FK must list the same columns in the same order and types as the parent's composite primary key.

**Alt1:**
```sql
-- Oracle — omit the constraint, rely on the implicit composite pair
ALTER TABLE bookings
    ADD CONSTRAINT fk_booking_seat
    FOREIGN KEY (aircraft_id, seat_number)
    REFERENCES seats (aircraft_id, seat_number);
```
**Explanation:** Adding the composite FK after creation is equivalent, and Oracle always demands an explicit or generated constraint name.

---

## Q37: Add multiple foreign keys to one table.

**Query:**
```sql
CREATE TABLE order_shipments (
    shipment_id  INT PRIMARY KEY,
    order_id     INT NOT NULL,
    address_id   INT NOT NULL,
    courier_id   INT NOT NULL,
    shipped_on   DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (order_id)   REFERENCES orders (order_id),
    FOREIGN KEY (address_id) REFERENCES addresses (address_id),
    FOREIGN KEY (courier_id) REFERENCES couriers (courier_id)
);
```
**Explanation:** Multiple independent FKs enforce referential integrity against several parent tables in a single child table.

---

## Q38: Enforce a foreign key with ON DELETE CASCADE and ON UPDATE CASCADE together.

**Query:**
```sql
CREATE TABLE order_items (
    item_id    INT PRIMARY KEY,
    order_id   INT NOT NULL,
    quantity   INT DEFAULT 1,
    FOREIGN KEY (order_id) REFERENCES orders (order_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);
```
**Explanation:** Parent deletes cascade to children; parent key updates propagate to children automatically.

---

## Q39: Add a column and make it a foreign key in the same ALTER statement.

**Query:**
```sql
-- PostgreSQL
ALTER TABLE employees
    ADD COLUMN team_id INT,
    ADD CONSTRAINT fk_employees_team
    FOREIGN KEY (team_id) REFERENCES teams (team_id);
```
**Explanation:** Multiple actions in one ALTER add the column then bind it to the parent table; the column starts as NULL so no rows violate the FK.

---

## Q40: Drop a foreign key constraint.

**Query:**
```sql
ALTER TABLE order_items
    DROP CONSTRAINT fk_order_items_orders;
```
**Explanation:** Dropping the FK removes referential enforcement; orphaned child rows are not deleted or modified.

**Alt1:**
```sql
-- MySQL
ALTER TABLE order_items
    DROP FOREIGN KEY fk_order_items_orders;
```
**Explanation:** MySQL reuses the same `DROP FOREIGN KEY` syntax; note the auto-generated name if you never named the constraint.

---

## Q41: Create a UNIQUE constraint that also serves as a table's alternate key.

**Query:**
```sql
CREATE TABLE passengers (
    passenger_id  INT PRIMARY KEY,
    passport_no   VARCHAR(20) UNIQUE,
    ssn           VARCHAR(11) UNIQUE,
    full_name     VARCHAR(150) NOT NULL
);
```
**Explanation:** Alternate (candidate) keys beyond the PK are implemented as UNIQUE constraints; they guarantee domain-level uniqueness.

---

## Q42: Identify candidate keys and promote one to primary key.

**Query:**
```sql
CREATE TABLE members (
    member_id  INT,
    email      VARCHAR(255) NOT NULL,
    phone      VARCHAR(20),
    name       VARCHAR(100)
);

-- Promote email as the PK
ALTER TABLE members
    ALTER COLUMN email SET NOT NULL;
ALTER TABLE members
    ADD CONSTRAINT pk_members PRIMARY KEY (email);
```
**Explanation:** The domain identifies a candidate key (email) from the columns and promotes it after guaranteeing NOT NULL.

**Alt1:**
```sql
-- SQL Server — drop the old surrogate before promoting
ALTER TABLE members ADD CONSTRAINT uq_members_email UNIQUE (email);
ALTER TABLE members DROP COLUMN member_id;
```
**Explanation:** The ALTERNATE path keeps a UNIQUE on email and drops the unused surrogate column instead of re-keying.

---

## Q43: Compare surrogate vs natural keys in DDL.

**Query:**
```sql
CREATE TABLE countries (
    country_code CHAR(2) PRIMARY KEY,          -- natural key
    name         VARCHAR(100) NOT NULL
);

CREATE TABLE users (
    user_id      SERIAL PRIMARY KEY,           -- surrogate key
    email        VARCHAR(255) UNIQUE NOT NULL
);
```
**Explanation:** Natural keys come from real-world data (ISO country codes); surrogate keys are generated and independent of business data.

---

## Q44: Create a natural key constraint that is also the primary key.

**Query:**
```sql
CREATE TABLE countries (
    iso_code   CHAR(2),
    iso_numeric CHAR(3) UNIQUE,
    name       VARCHAR(100) NOT NULL,
    PRIMARY KEY (iso_code)
);
```
**Explanation:** Choosing the natural business attribute as PK avoids joins on meaningless IDs but commits the app to that data never changing.

---

## Q45: Define a surrogate key with a sequence (PostgreSQL SERIAL).

**Query:**
```sql
-- PostgreSQL
CREATE TABLE users (
    user_id  SERIAL PRIMARY KEY,
    email    VARCHAR(255) NOT NULL UNIQUE
);
```
**Explanation:** `SERIAL` creates a sequence-backed auto-increment surrogate key; newer PostgreSQL prefers `GENERATED ALWAYS AS IDENTITY`.

**Alt1:**
```sql
-- MySQL — AUTO_INCREMENT
CREATE TABLE users (
    user_id  INT AUTO_INCREMENT PRIMARY KEY,
    email    VARCHAR(255) NOT NULL UNIQUE
);
```
**Explanation:** MySQL's `AUTO_INCREMENT` plays the same surrogate-key role but with a single monotonically increasing counter per table.

---

## Q46: Decide FK column type when the parent uses UUID.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE accounts (
    account_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name       VARCHAR(100) NOT NULL
);

CREATE TABLE transactions (
    tx_id      BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    account_id UUID NOT NULL,
    amount     NUMERIC(12,2) NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts (account_id)
);
```
**Explanation:** The child FK column must match the parent type exactly — here UUID to UUID — or the FK creation fails with a type mismatch.

---

## Q47: Insert rows in PK dependency order when FKs are not deferrable.

**Query:**
```sql
INSERT INTO countries (country_code, name) VALUES ('US', 'United States');
INSERT INTO cities (city_id, country_code, name)
VALUES (1, 'US', 'New York');
```
**Explanation:** With immediate FKs, parents must be inserted before children; inserting a city with an unknown country code violates the constraint.

**Alt1:**
```sql
-- PostgreSQL — defer the check to batch both inserts
BEGIN;
SET CONSTRAINTS fk_cities_country DEFERRED;
INSERT INTO cities (city_id, country_code, name) VALUES (1, 'US', 'NYC');
INSERT INTO countries (country_code, name) VALUES ('US', 'United States');
COMMIT;
```
**Explanation:** Deferring the FK check allows child-first inserts within one transaction as long as parents exist by COMMIT.

---

## Q48: Delete rows in the correct order when FKs are immediate.

**Query:**
```sql
DELETE FROM order_items
WHERE order_id IN (SELECT order_id FROM orders WHERE status = 'cancelled');

DELETE FROM orders
WHERE status = 'cancelled';
```
**Explanation:** Children must be removed before their parents; deleting the parent first triggers a foreign key violation.

---

## Q49: Truncate a parent table with dependent child rows.

**Query:**
```sql
-- PostgreSQL
TRUNCATE TABLE order_items;
TRUNCATE TABLE orders;
```
**Explanation:** TRUNCATE bypasses FK checks row-by-row; truncate children first or use `TRUNCATE orders CASCADE` to extend the operation to dependencies.

---

## Q50: Drop the child table before the parent when dropping FKs.

**Query:**
```sql
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
```
**Explanation:** Drop order matters only for tables with self-contained schemas; dropping the child first avoids dangling references, though modern RDBMS handle parent drops via CASCADE.

## Q51: Drop a parent table while other tables reference it (PostgreSQL).

**Query:**
```sql
-- PostgreSQL
DROP TABLE customers CASCADE;
```
**Explanation:** `CASCADE` automatically drops the dependent FK constraints (but not the child tables), allowing the parent to be removed.

**Alt1:**
```sql
-- Oracle
DROP TABLE customers CASCADE CONSTRAINTS;
```
**Explanation:** Oracle's `CASCADE CONSTRAINTS` drops only the dependent FK constraints, keeping the child tables and data intact.

---

## Q52: Create a UNIQUE constraint on a column that can contain NULLs.

**Query:**
```sql
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    ean        VARCHAR(13) UNIQUE
);
```
**Explanation:** `ean` allows NULL (and multiple NULLs); only non-NULL values are checked for uniqueness.

---

## Q53: Create a UNIQUE constraint over a generated/stored column.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE accounts (
    account_id     BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email_local    TEXT,
    email_domain   TEXT,
    email          TEXT GENERATED ALWAYS AS (email_local || '@' || email_domain) STORED
);
```
**Explanation:** Deriving a full email from stored parts lets you enforce integrity while normalizing the input; the generated column can hold a UNIQUE constraint.

---

## Q54: Enforce uniqueness where the pair is case-insensitive.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE users (
    user_id  INT PRIMARY KEY,
    username TEXT NOT NULL
);
CREATE UNIQUE INDEX uq_users_username_ci
    ON users (LOWER(username));
```
**Explanation:** A unique index on an expression treats `Admin` and `admin` as duplicates, giving case-insensitive uniqueness.

**Alt1:**
```sql
-- SQL Server
CREATE UNIQUE INDEX uq_users_username_ci
    ON users (username);
```
**Explanation:** Under a case-insensitive collation, SQL Server already treats `Admin` and `admin` as equal within the plain unique index.

---

## Q55: Create a table with a UNIQUE constraint on multiple nullable columns.

**Query:**
```sql
CREATE TABLE discounts (
    discount_id INT PRIMARY KEY,
    product_id  INT,
    coupon_code VARCHAR(20) UNIQUE (coupon_code)
);
```
**Explanation:** Although shown inline for one column here, composite UNIQUE with NULLs follows the same rules: any row where all columns are NULL is still allowed as a distinct combination.

**Alt1:**
```sql
CREATE TABLE pairings (
    left_id  INT,
    right_id INT,
    CONSTRAINT uq_pair UNIQUE (left_id, right_id)
);
```
**Explanation:** MySQL/Postgres allow multiple pairs sharing NULLs as long as at least one member differs; each all-NULL combo is counted once.

---

## Q56: Create a foreign key with ON DELETE SET NULL on a composite key.

**Query:**
```sql
CREATE TABLE shipments (
    shipment_id  INT PRIMARY KEY,
    region_id    INT,
    route_id     INT,
    carrier      VARCHAR(100),
    CONSTRAINT fk_shipments_route
        FOREIGN KEY (region_id, route_id)
        REFERENCES routes (region_id, route_id)
        ON DELETE SET NULL
);
```
**Explanation:** Deleting the parent route sets both child columns to NULL so the shipment row survives without its route.

---

## Q57: Create a foreign key with ON DELETE SET NULL where the FK column is NOT NULL.

**Query:**
```sql
-- This statement intentionally fails
CREATE TABLE orders (
    order_id    INT PRIMARY KEY,
    customer_id INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        ON DELETE SET NULL
);
```
**Explanation:** A NOT NULL FK column cannot use `ON DELETE SET NULL`; the combination is rejected at creation because the action would violate NOT NULL.

---

## Q58: Create a foreign key to a table in another schema.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE sales.orders (
    order_id   INT PRIMARY KEY,
    customer_id INT NOT NULL,
    FOREIGN KEY (customer_id)
        REFERENCES hr.customers (customer_id)
);
```
**Explanation:** Cross-schema FKs require the referenced table's schema-qualified name and appropriate privileges on both objects.

**Alt1:**
```sql
-- Oracle — schema-qualified REFERENCES
CREATE TABLE sales.orders (
    order_id    NUMBER(8) PRIMARY KEY,
    customer_id NUMBER(8) NOT NULL,
    CONSTRAINT fk_order_customer FOREIGN KEY (customer_id)
        REFERENCES hr.customers (customer_id)
);
```
**Explanation:** Oracle follows the same pattern; the caller needs REFERENCES privilege on the target schema's table.

---

## Q59: Create a UNIQUE constraint across two schemas is impossible.

**Query:**
```sql
-- Cross-schema constraint is not possible; enforce in one table
CREATE TABLE hr.employees (
    emp_id   INT PRIMARY KEY,
    email    VARCHAR(255) UNIQUE
);
```
**Explanation:** UNIQUE applies within a single table only; cross-table uniqueness across schemas requires app-level checks or a trigger.

---

## Q60: Check for orphaned rows before adding a foreign key.

**Query:**
```sql
SELECT o.customer_id
FROM orders o
LEFT JOIN customers c ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL;
```
**Explanation:** Any rows returned would cause the `ALTER TABLE … ADD CONSTRAINT` FK creation to fail; fix or delete them first.

---

## Q61: Find all foreign keys referencing a particular table (informational schema).

**Query:**
```sql
-- ANSI SQL
SELECT tc.table_name,
       kcu.column_name,
       rc.update_rule,
       rc.delete_rule
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
     ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.referential_constraints rc
     ON tc.constraint_name = rc.constraint_name
WHERE rc.unique_constraint_schema = 'public'
  AND rc.unique_constraint_name = 'customers_pkey';
```
**Explanation:** This introspection query lists every child table and the delete/update action of FKs pointing at the target parent.

---

## Q62: List all UNIQUE constraints and indexes on a table (PostgreSQL).

**Query:**
```sql
-- PostgreSQL
SELECT conname, contype
FROM pg_constraint
WHERE conrelid = 'users'::regclass
  AND contype IN ('u', 'p');

SELECT indexname
FROM pg_indexes
WHERE tablename = 'users'
  AND indexdef ILIKE '%unique%';
```
**Explanation:** `contype = 'u'` lists UNIQUE constraints; the index query reveals unique indexes, which may not be constraint-backed.

---

## Q63: Create a foreign key that enforces a "status" reference list.

**Query:**
```sql
CREATE TABLE order_status (
    status_code CHAR(2) PRIMARY KEY,
    label       VARCHAR(50) NOT NULL
);

CREATE TABLE orders (
    order_id    INT PRIMARY KEY,
    status_code CHAR(2) NOT NULL,
    FOREIGN KEY (status_code) REFERENCES order_status (status_code)
);
```
**Explanation:** A small lookup table referenced by an FK is the relational way to constrain an enum-like column.

---

## Q64: Use a composite foreign key where one column is the parent PK and others are data.

**Query:**
```sql
CREATE TABLE invoices (
    invoice_id INT PRIMARY KEY,
    customer_id INT NOT NULL
);

CREATE TABLE payments (
    payment_id  INT PRIMARY KEY,
    invoice_id  INT NOT NULL,
    customer_id INT NOT NULL,
    amount      NUMERIC(12,2) NOT NULL,
    FOREIGN KEY (invoice_id, customer_id)
        REFERENCES invoices (invoice_id, customer_id)
);
```
**Explanation:** This requires a UNIQUE on `(invoice_id, customer_id)` in the parent and is a classic redundant-FK anti-pattern — avoided unless the extra column is genuinely needed.

---

## Q65: Performance DDL — avoid FK on a write-hot, sharded table.

**Query:**
```sql
-- MySQL — FK omitted intentionally on sharded analytics
CREATE TABLE events (
    event_id   BIGINT NOT NULL,
    user_id    BIGINT NOT NULL,
    epoch_ms   BIGINT NOT NULL,
    payload    JSON,
    PRIMARY KEY (event_id, user_id)
);
```
**Explanation:** Skipping the FK to a sharded `users` table avoids cross-shard lookups and insertion latency; correctness is enforced by the producer application.

---

## Q66: Create a partial unique index to enforce uniqueness only for active users.

**Query:**
```sql
-- PostgreSQL
CREATE UNIQUE INDEX uq_active_user_email
    ON users (email)
    WHERE is_active = TRUE;
```
**Explanation:** Partial unique indexes allow duplicate emails among inactive accounts while keeping active emails unique.

---

## Q67: Close the SQL Server "one NULL per unique column" difference using a filtered index.

**Query:**
```sql
-- SQL Server — unique filtered index instead of KEY (default differs by column)
CREATE TABLE tags (
    tag_id   INT PRIMARY KEY,
    tag_name VARCHAR(50)
);
CREATE UNIQUE INDEX uq_tags_name
    ON tags (tag_name)
    WHERE tag_name IS NOT NULL;
```
**Explanation:** This yields standard behavior (multiple NULLs allowed) and is the documented workaround when a DB enforces single-NULL.

---

## Q68: Create a surrogate PK with IDENTITY and a natural-key UNIQUE.

**Query:**
```sql
-- SQL Server
CREATE TABLE users (
    user_id  INT IDENTITY(1,1) PRIMARY KEY,
    email    VARCHAR(255) NOT NULL,
    CONSTRAINT uq_users_email UNIQUE (email)
);
```
**Explanation:** The IDENTITY surrogate avoids business-key coupling, while the natural `email` UNIQUE guarantees domain integrity.

---

## Q69: Use a sequence to pre-allocate IDs for an FK batch load.

**Query:**
```sql
-- PostgreSQL
CREATE SEQUENCE order_seq START 1001;
INSERT INTO orders (order_id, customer_id)
VALUES (nextval('order_seq'), 7);
INSERT INTO order_items (item_id, order_id, quantity)
VALUES (1, currval('order_seq'), 2);
```
**Explanation:** `currval()` lets an insert script link the child row to the freshly generated parent ID in the same session.

---

## Q70: Create an FK whose parent key is a UNIQUE index, not a constraint (Oracle).

**Query:**
```sql
-- Oracle
CREATE TABLE departments (
    dept_no  NUMBER(4),
    dept_name VARCHAR2(100)
);
CREATE UNIQUE INDEX dept_no_uk ON departments (dept_no);

CREATE TABLE employees (
    emp_id NUMBER(6),
    dept_no NUMBER(4),
    FOREIGN KEY (dept_no) REFERENCES departments (dept_no)
);
```
**Explanation:** Oracle accepts a UNIQUE index (not only a UNIQUE constraint) as the target of a foreign key.

---

## Q71: Build a "bill of materials" table with both FKs referencing the same parent.

**Query:**
```sql
CREATE TABLE parts (
    part_id INT PRIMARY KEY,
    name    VARCHAR(100) NOT NULL
);

CREATE TABLE bom_lines (
    line_id     INT PRIMARY KEY,
    parent_part INT NOT NULL,
    child_part  INT NOT NULL,
    qty         DECIMAL(10,2) NOT NULL DEFAULT 1,
    FOREIGN KEY (parent_part) REFERENCES parts (part_id),
    FOREIGN KEY (child_part)  REFERENCES parts (part_id)
);
```
**Explanation:** Two FKs to the same table model a many-to-many self-relationship with distinct roles per column.

---

## Q72: Make a friendship table with a composite PK that itself is two FKs.

**Query:**
```sql
CREATE TABLE friendships (
    user_a    INT NOT NULL,
    user_b    INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_a, user_b),
    FOREIGN KEY (user_a) REFERENCES users (user_id),
    FOREIGN KEY (user_b) REFERENCES users (user_id)
);
```
**Explanation:** The composite PK prevents duplicate pairs; each component also functions as an FK pointing at `users`.

---

## Q73: Order of unique index columns vs WHERE filters.

**Query:**
```sql
-- MySQL
CREATE TABLE notifications (
    user_id INT NOT NULL,
    kind    VARCHAR(20) NOT NULL,
    created_at DATETIME NOT NULL,
    UNIQUE KEY uq_notif (user_id, kind, created_at)
);
```
**Explanation:** Column order matters for lookups; this pair-then-timestamp layout serves queries filtering by `user_id` and `kind` first.

---

## Q74: Create a foreign key with a MATCH SIMPLE composite check (SQL Server/Firebird semantics).

**Query:**
```sql
-- SQL Server — MATCH SIMPLE is applied implicitly
CREATE TABLE readonly_copies (
    chapter_id INT,
    book_id    INT,
    FOREIGN KEY (chapter_id, book_id)
        REFERENCES chapters (chapter_id, book_id)
);
```
**Explanation:** SQL Server only implements `MATCH SIMPLE`: if any child column is NULL, the FK is not enforced; partial matches are disallowed.

---

## Q75: Add a DEFAULT and FK together when creating a column (SQL Server).

**Query:**
```sql
-- SQL Server
ALTER TABLE employees
    ADD department_id INT NOT NULL
        CONSTRAINT df_employees_dept DEFAULT 1,
    CONSTRAINT fk_employees_dept
        FOREIGN KEY (department_id) REFERENCES departments (department_id);
```
**Explanation:** The NOT NULL default satisfies immediate FK checks for existing rows as long as department 1 already exists in the parent.

## Q76: Rename a primary key constraint.

**Query:**
```sql
-- PostgreSQL
ALTER TABLE customers
    RENAME CONSTRAINT customers_pkey TO pk_customers;
```
**Explanation:** Renaming keeps the same backing index but gives the constraint a readable, project-consistent name.

**Alt1:**
```sql
-- Oracle
ALTER TABLE customers
    RENAME CONSTRAINT sys_c00234 TO pk_customers;
```
**Explanation:** Oracle allows renaming constraints similarly, which is handy for auto-named `SYS_C*` constraints.

---

## Q77: Create a UNIQUE constraint with a max length prefix (MySQL).

**Query:**
```sql
-- MySQL (older versions / utf8mb4 row-size limits)
CREATE TABLE articles (
    article_id INT PRIMARY KEY,
    slug       VARCHAR(255) NOT NULL
);
CREATE UNIQUE INDEX uq_articles_slug ON articles (slug(100));
```
**Explanation:** A prefix-length unique index avoids the byte-size limit of full-length keys in old InnoDB; it only enforces uniqueness on the first 100 characters.

---

## Q78: Include a key column in a foreign-key relationship that references a non-key UNIQUE — a "business key" link.

**Query:**
```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_ref VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE invoices (
    invoice_id   INT PRIMARY KEY,
    customer_ref VARCHAR(20) NOT NULL,
    issued_on DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (customer_ref) REFERENCES customers (customer_ref)
);
```
**Explanation:** Using the stable business reference as the FK target keeps DDL readable in reporting, but prefer the surrogate if the reference can ever change.

---

## Q79: Enforce that each row has exactly one active primary (PostgreSQL partial unique).

**Query:**
```sql
-- PostgreSQL
CREATE TABLE addresses (
    addr_id   INT PRIMARY KEY,
    person_id INT NOT NULL,
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    label     VARCHAR(50)
);
CREATE UNIQUE INDEX uq_one_primary_per_person
    ON addresses (person_id)
    WHERE is_primary = TRUE;
```
**Explanation:** The partial unique index guarantees at most one primary address per person without blocking historical rows.

---

## Q80: Model a one-to-one relationship by making the FK column unique.

**Query:**
```sql
CREATE TABLE wallets (
    wallet_id INT PRIMARY KEY,
    user_id   INT NOT NULL UNIQUE,
    balance   DECIMAL(12,2) DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
```
**Explanation:** `UNIQUE` on the FK column turns the otherwise one-to-many relationship into a one-to-one: each user maps to at most one wallet.

**Alt1:**
```sql
-- Oracle — also enforce via an indexed unique FK
CREATE TABLE wallets (
    wallet_id NUMBER(8) PRIMARY KEY,
    user_id   NUMBER(8) NOT NULL UNIQUE,
    balance   NUMBER(14,2) DEFAULT 0,
    CONSTRAINT fk_wallet_user FOREIGN KEY (user_id)
        REFERENCES users (user_id)
);
```
**Explanation:** Oracle adds the unique index and FK in one DDL; the two constraints commute for enforcement purposes.

---

## Q81: Add a foreign key with a non-default collation matching the parent key.

**Query:**
```sql
-- SQL Server
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    email       VARCHAR(255) COLLATE Latin1_General_CI_AS UNIQUE NOT NULL
);

CREATE TABLE campaigns (
    campaign_id INT PRIMARY KEY,
    email       VARCHAR(255) COLLATE Latin1_General_CI_AS NOT NULL,
    FOREIGN KEY (email) REFERENCES customers (email)
);
```
**Explanation:** FK columns must match the referenced key's collation exactly in SQL Server, or the constraint creation fails.

---

## Q82: Create an FK that points to a table in a different database (SQL Server).

**Query:**
```sql
-- SQL Server (cross-database, same instance)
CREATE TABLE [sales].[dbo].[orders] (
    order_id    INT PRIMARY KEY,
    customer_id INT NOT NULL,
    FOREIGN KEY (customer_id)
        REFERENCES [crm].[dbo].[customers] (customer_id)
);
```
**Explanation:** SQL Server supports cross-database FKs on the same instance so long as both remain online; cross-instance FKs are not supported.

---

## Q83: Generate the DDL script to force all FKs to use a matching delete rule.

**Query:**
```sql
-- MySQL: rewrite a NO ACTION FK to CASCADE
ALTER TABLE order_items
    DROP FOREIGN KEY fk_order_items_orders;

ALTER TABLE order_items
    ADD CONSTRAINT fk_order_items_orders
    FOREIGN KEY (order_id) REFERENCES orders (order_id)
    ON DELETE CASCADE;
```
**Explanation:** MySQL cannot alter FK rules in place; you must drop and re-add the constraint to change its action.

---

## Q84: Check before deleting to avoid FK errors (child existence query).

**Query:**
```sql
SELECT COUNT(*) AS child_count
FROM order_items
WHERE order_id IN (
    SELECT order_id FROM orders WHERE status = 'cancelled'
);
```
**Explanation:** Pre-checking child counts lets application code decide between CASCADE-style cleanup and refusing the delete.

---

## Q85: Create a UNIQUE constraint on a nullable column where the type needs care (Oracle empty strings).

**Query:**
```sql
-- Oracle: empty string is NULL, so this allows blanks
CREATE TABLE app_settings (
    key_name  VARCHAR2(64) PRIMARY KEY,
    alt_key   VARCHAR2(64) UNIQUE
);
```
**Explanation:** Oracle treats `''` as NULL, so multiple empty `alt_key` values are permitted under UNIQUE; two non-NULL equal values still conflict.

---

## Q86: Use a UNIQUE constraint to back a queue with no duplicates.

**Query:**
```sql
CREATE TABLE job_queue (
    job_id   INT PRIMARY KEY,
    job_key  VARCHAR(64) UNIQUE NOT NULL,
    payload  TEXT,
    status   VARCHAR(20) DEFAULT 'pending'
);
INSERT INTO job_queue (job_id, job_key, payload)
VALUES (1, 'import:user:42', '{"user":42}');
-- Duplicate insert fails:
INSERT INTO job_queue (job_id, job_key, payload)
VALUES (2, 'import:user:42', '{"user":42}');
```
**Explanation:** The UNIQUE `job_key` makes the queue idempotent — re-delivering the same key is rejected instead of double-processing.

---

## Q87: Add an ON UPDATE CASCADE FK and propagate the change.

**Query:**
```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY
);
CREATE TABLE orders (
    order_id    INT PRIMARY KEY,
    customer_id INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        ON UPDATE CASCADE
);

UPDATE customers SET customer_id = 5000 WHERE customer_id = 10;
```
**Explanation:** Updating the parent key from 10 to 5000 automatically rewrites every `orders.customer_id` that referenced 10.

---

## Q88: Design around a foreign key cycle that cannot be deferred.

**Query:**
```sql
-- Insert parents first where possible; else accept deadlock at design time
INSERT INTO permits (permit_id, holder_id) VALUES (1, NULL);
INSERT INTO holders (holder_id, permit_id) VALUES (10, 1);
UPDATE permits SET holder_id = 10 WHERE permit_id = 1;
```
**Explanation:** With immediate constraints, inserting a NULL placeholder then an UPDATE fakes deferral — but a nullable FK side is the cleaner design.

---

## Q89: Replace a natural-key FK with a surrogate-key FK to cut update spikes.

**Query:**
```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_ref VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100)
);

CREATE TABLE invoices (
    invoice_id   INT PRIMARY KEY,
    customer_id  INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);
```
**Explanation:** FKs to immutable surrogate keys avoid `ON UPDATE CASCADE` storms when a business reference (email, ref) changes.

---

## Q90: Enforce uniqueness across a "soft-deleted" set only (MySQL).

**Query:**
```sql
-- MySQL — emulate partial unique after delete
CREATE TABLE users (
    user_id    INT PRIMARY KEY,
    email      VARCHAR(255) NOT NULL,
    deleted_at DATETIME NULL
);
CREATE UNIQUE INDEX uq_email_active
    ON users (email, IFNULL(deleted_at, 0));
```
**Explanation:** By mixing the email with a never-NULL deleted marker, the index collapses all active rows on the same email while separate soft-deletes stay distinct.

---

## Q91: Convert an inline FK to a named table-level constraint (Oracle).

**Query:**
```sql
-- Oracle
CREATE TABLE order_items (
    item_id NUMBER PRIMARY KEY,
    order_id NUMBER NOT NULL CONSTRAINT fk_detail_order REFERENCES orders (order_id)
);
```
**Explanation:** Oracle supports naming an inline FK with `CONSTRAINT`, giving it a stable name without a separate table-level clause.

---

## Q92: Create a foreign key on a partitioned table (PostgreSQL).

**Query:**
```sql
-- PostgreSQL
CREATE TABLE events_2024 (
    event_id BIGINT PRIMARY KEY,
    user_id  BIGINT NOT NULL REFERENCES users (user_id)
) PARTITION BY RANGE (event_id);

CREATE TABLE events_2024_q1
    PARTITION OF events_2024
    FOR VALUES FROM (1) TO (100000);
```
**Explanation:** FKs may be defined on partitioned tables; the child partitions inherit the constraint, but partition keys cannot be part of a referenced unique key.

---

## Q93: Build a junction table where the PK is the pair of FKs.

**Query:**
```sql
CREATE TABLE course_registrations (
    student_id  INT NOT NULL,
    course_id   INT NOT NULL,
    registered  DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students (student_id),
    FOREIGN KEY (course_id)  REFERENCES courses (course_id)
);
```
**Explanation:** The composite PK doubles as both FKs, preventing duplicate registrations and enforcing both relationships at once.

**Alt1:**
```sql
-- SQL Server — the composite PK plus separate named FKs
CREATE TABLE course_registrations (
    student_id  INT NOT NULL,
    course_id   INT NOT NULL,
    registered  DATE DEFAULT CAST(GETDATE() AS DATE),
    CONSTRAINT pk_reg PRIMARY KEY (student_id, course_id),
    CONSTRAINT fk_reg_student FOREIGN KEY (student_id)
        REFERENCES students (student_id),
    CONSTRAINT fk_reg_course FOREIGN KEY (course_id)
        REFERENCES courses (course_id)
);
```
**Explanation:** SQL Server lets the composite PK and the two FKs share their key columns without conflict.

---

## Q94: Add a foreign key where the parent was already truncated but children remain.

**Query:**
```sql
-- Must clean orphans before re-adding the FK
DELETE FROM orders o
WHERE NOT EXISTS (
    SELECT 1 FROM customers c WHERE c.customer_id = o.customer_id
);

ALTER TABLE orders
    ADD CONSTRAINT fk_orders_customer
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id);
```
**Explanation:** After a careless TRUNCATE of the parent, fixing orphans with an anti-join unblocks the `ALTER` that would otherwise fail.

---

## Q95: Create a pair of mutually-referencing tables without cycles via a separate link table.

**Query:**
```sql
CREATE TABLE articles (
    article_id INT PRIMARY KEY,
    title VARCHAR(200) NOT NULL
);
CREATE TABLE revisions (
    revision_id INT PRIMARY KEY,
    article_id  INT NOT NULL,
    FOREIGN KEY (article_id) REFERENCES articles (article_id)
);
CREATE TABLE article_head (
    article_id  INT PRIMARY KEY,
    revision_id INT NOT NULL UNIQUE,
    FOREIGN KEY (article_id) REFERENCES articles (article_id),
    FOREIGN KEY (revision_id) REFERENCES revisions (revision_id)
);
```
**Explanation:** Making the "current revision" its own link table removes the direct FK cycle between parent and child.

---

## Q96: Copy a UNIQUE constraint from a template table (PostgreSQL).

**Query:**
```sql
-- PostgreSQL
CREATE TABLE users_backup (LIKE users INCLUDING ALL);

ALTER TABLE users_backup
    ADD CONSTRAINT uq_users_backup_email UNIQUE (email);
```
**Explanation:** `INCLUDING ALL` copies constraints; explicitly re-adding the constraint after gives full control over the clone's schema.

---

## Q97: Ensure FK inserts respect auto-increment sequencing (MySQL).

**Query:**
```sql
-- MySQL
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY
);
CREATE TABLE order_items (
    item_id  INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders (order_id)
);

INSERT INTO orders () VALUES ();
SET @oid = LAST_INSERT_ID();
INSERT INTO order_items (order_id, qty) VALUES (@oid, 2);
```
**Explanation:** Capturing `LAST_INSERT_ID()` after the parent insert lets the child insert reference the correct generated key.

---

## Q98: Create a UNIQUE constraint combined with a CHECK on the same column.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    email   VARCHAR(255) NOT NULL,
    CONSTRAINT uq_users_email UNIQUE (email),
    CONSTRAINT chk_email_shape CHECK (email ~ '^[^@]+@[^@]+$')
);
```
**Explanation:** UNIQUE handles non-duplication while CHECK handles format; constraints compose but stay independent on the same column.

---

## Q99: Find every table with a missing on-delete action (no CASCADE/SET NULL) used for an audit log.

**Query:**
```sql
-- PostgreSQL
SELECT tc.table_name AS child,
       kcu.column_name,
       rc.delete_rule
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
     ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.referential_constraints rc
     ON tc.constraint_name = rc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND rc.delete_rule = 'NO ACTION';
```
**Explanation:** Auditing the delete rules shows which child tables keep history rows because deletes are blocked rather than propagated.

---

## Q100: Full design with surrogate PKs, natural-key UNIQUEs, deferrable cyclic FKs, and cascade policy.

**Query:**
```sql
-- PostgreSQL — realistic composite schema
CREATE TABLE teams (
    team_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    lead_id INT
);

CREATE TABLE users (
    user_id  INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email    TEXT NOT NULL CONSTRAINT uq_users_email UNIQUE,
    team_id  INT NOT NULL,
    CONSTRAINT fk_users_team FOREIGN KEY (team_id)
        REFERENCES teams (team_id)
        ON UPDATE CASCADE ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED
);

ALTER TABLE teams
    ADD CONSTRAINT fk_teams_lead FOREIGN KEY (lead_id)
        REFERENCES users (user_id) ON DELETE SET NULL;
```
**Explanation:** The schema combines surrogate identity keys, a natural-key unique email, a deferrable many-to-one FK avoiding insert-order coupling, and a self-cycle broken by the deferral plus SET NULL.
