# Creating Tables and Constraints (DDL) — 100 SQL Interview Q&A

## Q1: Write a basic CREATE TABLE statement for an `employees` table with `id`, `name`, and `hire_date` columns.

**Query:**
```sql
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    hire_date DATE
);
```
**Explanation:** Defines a simple three-column table with a primary key, a required name, and a nullable hire date.

---

## Q2: Create a `products` table where `id` auto-increments in MySQL.

**Query:**
```sql
-- MySQL
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10, 2)
);
```
**Explanation:** `AUTO_INCREMENT` lets MySQL generate sequential IDs automatically on insert.

---

## Q3: Create the same `products` table using PostgreSQL's SERIAL shortcut.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price NUMERIC(10, 2)
);
```
**Explanation:** `SERIAL` is a PostgreSQL shorthand that creates an integer column backed by a sequence.

**Alt1:**
```sql
-- PostgreSQL
CREATE TABLE products (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price NUMERIC(10, 2)
);
```
Uses the SQL-standard `GENERATED ALWAYS AS IDENTITY` instead of the legacy `SERIAL` shortcut.

---

## Q4: Create a `customers` table in SQL Server with an identity column.

**Query:**
```sql
-- SQL Server
CREATE TABLE customers (
    id INT IDENTITY(1,1) PRIMARY KEY,
    full_name NVARCHAR(150) NOT NULL,
    email NVARCHAR(255) NOT NULL UNIQUE
);
```
**Explanation:** `IDENTITY(1,1)` seeds at 1 and increments by 1; `NVARCHAR` supports Unicode.

---

## Q5: Create a `users` table in Oracle using a GENERATED ALWAYS AS IDENTITY column.

**Query:**
```sql
-- Oracle
CREATE TABLE users (
    user_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR2(50) NOT NULL,
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP
);
```
**Explanation:** Oracle's identity column is the modern replacement for manual sequences.

---

## Q6: Create an `orders` table with a `DEFAULT` value for `status` and `created_at`.

**Query:**
```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** `DEFAULT` clauses populate columns automatically when no value is supplied.

---

## Q7: Create a `payments` table with a `DECIMAL` column for monetary amounts and a `NOT NULL` constraint on `amount`.

**Query:**
```sql
CREATE TABLE payments (
    payment_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    method VARCHAR(30)
);
```
**Explanation:** `DECIMAL(12,2)` stores up to 99,999,999,999.99 with exact precision — ideal for money.

**Alt1:**
```sql
-- Oracle
CREATE TABLE payments (
    payment_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id NUMBER NOT NULL,
    amount NUMBER(12, 2) NOT NULL,
    method VARCHAR2(30)
);
```
Oracle uses `NUMBER(12,2)` for exact-precision monetary storage.

---

## Q8: Create a `phone_directory` table choosing an appropriate type for a 10-digit US phone number.

**Query:**
```sql
CREATE TABLE phone_directory (
    entry_id INT PRIMARY KEY,
    phone CHAR(10) NOT NULL,
    owner_name VARCHAR(100) NOT NULL
);
```
**Explanation:** `CHAR(10)` is fixed-length and appropriate since US phone numbers are always 10 digits; no leading zeros to preserve.

---

## Q9: Create a `flags` table with a `BOOLEAN` column and a `TEXT` column.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE flags (
    flag_id SERIAL PRIMARY KEY,
    is_active BOOLEAN DEFAULT TRUE,
    description TEXT
);
```
**Explanation:** PostgreSQL has a native `BOOLEAN` type; `TEXT` stores unlimited-length strings.

**Alt1:**
```sql
-- MySQL
CREATE TABLE flags (
    flag_id INT AUTO_INCREMENT PRIMARY KEY,
    is_active TINYINT(1) DEFAULT 1,
    description TEXT
);
```
MySQL uses `TINYINT(1)` as a surrogate for boolean.

---

## Q10: Create a `documents` table with a `JSON` column for flexible metadata.

**Query:**
```sql
-- MySQL
CREATE TABLE documents (
    doc_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    metadata JSON
);
```
**Explanation:** MySQL's `JSON` type enforces valid JSON syntax and enables JSON path queries.

**Alt1:**
```sql
-- PostgreSQL
CREATE TABLE documents (
    doc_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    metadata JSONB
);
```
PostgreSQL's `JSONB` is binary-stored, indexable, and preferred over plain `JSON`.

**Alt2:**
```sql
-- SQL Server
CREATE TABLE documents (
    doc_id INT IDENTITY(1,1) PRIMARY KEY,
    title NVARCHAR(255) NOT NULL,
    metadata NVARCHAR(MAX)
);
```
SQL Server stores JSON as text; no native JSON type, so use `NVARCHAR(MAX)` and `ISJSON()` check.

---

## Q11: Create a `sessions` table with a `UUID` primary key in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE sessions (
    session_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id INT NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** `gen_random_uuid()` generates a v4 UUID at insert time, ideal for distributed systems.

**Alt1:**
```sql
-- MySQL 8.0+
CREATE TABLE sessions (
    session_id BINARY(16) PRIMARY KEY,
    user_id INT NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
MySQL lacks a UUID type; store as `BINARY(16)` and use `UUID_TO_BIN()` / `BIN_TO_UUID()`.

---

## Q12: Add a column `phone` to an existing `employees` table in MySQL.

**Query:**
```sql
-- MySQL
ALTER TABLE employees
ADD COLUMN phone VARCHAR(20);
```
**Explanation:** `ADD COLUMN` appends a new nullable column to the table.

---

## Q13: Drop the `phone` column from `employees` in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
ALTER TABLE employees
DROP COLUMN phone;
```
**Explanation:** `DROP COLUMN` removes the column and its data permanently.

---

## Q14: Modify the `name` column in `employees` to increase its maximum length to 200 in MySQL.

**Query:**
```sql
-- MySQL
ALTER TABLE employees
MODIFY COLUMN name VARCHAR(200) NOT NULL;
```
**Explanation:** MySQL uses `MODIFY COLUMN` to redefine a column's type and constraints in place.

**Alt1:**
```sql
-- PostgreSQL
ALTER TABLE employees
ALTER COLUMN name TYPE VARCHAR(200);
```
PostgreSQL uses `ALTER COLUMN ... TYPE` for type changes.

**Alt2:**
```sql
-- SQL Server
ALTER TABLE employees
ALTER COLUMN name NVARCHAR(200) NOT NULL;
```
SQL Server uses `ALTER COLUMN` without the `MODIFY` keyword.

---

## Q15: Rename the `employees` table to `staff` in Oracle.

**Query:**
```sql
-- Oracle
RENAME employees TO staff;
```
**Explanation:** Oracle's `RENAME ... TO` renames a table at the schema level.

**Alt1:**
```sql
-- MySQL / PostgreSQL
ALTER TABLE employees RENAME TO staff;
```
Most dialects support `ALTER TABLE ... RENAME TO`.

---

## Q16: Create a `departments` table with a foreign key referencing `employees(id)`.

**Query:**
```sql
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    manager_id INT,
    FOREIGN KEY (manager_id) REFERENCES employees(id)
);
```
**Explanation:** The inline `FOREIGN KEY` clause ensures `manager_id` references a valid employee.

---

## Q17: Create a `tags` table with a composite primary key on `(post_id, tag_name)`.

**Query:**
```sql
CREATE TABLE tags (
    post_id INT NOT NULL,
    tag_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (post_id, tag_name)
);
```
**Explanation:** A composite PK enforces uniqueness across both columns together.

---

## Q18: Create a `check_test` table with a `CHECK` constraint on `age`.

**Query:**
```sql
CREATE TABLE check_test (
    id INT PRIMARY KEY,
    age INT NOT NULL CHECK (age >= 0 AND age <= 150)
);
```
**Explanation:** The `CHECK` constraint rejects any value outside the valid range.

**Alt1:**
```sql
-- MySQL (named constraint)
CREATE TABLE check_test (
    id INT PRIMARY KEY,
    age INT NOT NULL,
    CONSTRAINT chk_age CHECK (age >= 0 AND age <= 150)
);
```
Named constraints produce clearer error messages.

---

## Q19: Create a `logs` table with a `TEXT` column and a `TIMESTAMP` column that defaults to the current time.

**Query:**
```sql
CREATE TABLE logs (
    log_id INT PRIMARY KEY,
    message TEXT NOT NULL,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** `TEXT` holds long log messages; `CURRENT_TIMESTAMP` stamps insert time automatically.

---

## Q20: Create an `archive_orders` table using `CREATE TABLE AS SELECT` from `orders` with a filter.

**Query:**
```sql
CREATE TABLE archive_orders AS
SELECT * FROM orders
WHERE created_at < '2025-01-01';
```
**Explanation:** `CREATE TABLE AS` (CTAS) copies both schema and filtered data into a new table.

**Alt1:**
```sql
-- SQL Server
SELECT *
INTO archive_orders
FROM orders
WHERE created_at < '2025-01-01';
```
SQL Server uses `SELECT ... INTO` for the same purpose.

---

## Q21: Create a `temp_results` temporary table in MySQL that drops when the session ends.

**Query:**
```sql
-- MySQL
CREATE TEMPORARY TABLE temp_results (
    id INT,
    score DECIMAL(5,2)
);
```
**Explanation:** `TEMPORARY` tables are session-scoped and automatically dropped on disconnect.

---

## Q22: Create a temporary table in PostgreSQL that is visible only within the current transaction.

**Query:**
```sql
-- PostgreSQL
CREATE TEMPORARY TABLE temp_results (
    id INT,
    score NUMERIC(5,2)
) ON COMMIT DROP;
```
**Explanation:** `ON COMMIT DROP` makes the table vanish at the end of the transaction, not just the session.

---

## Q23: Create a `temp_results` table in SQL Server that is visible only to the current session.

**Query:**
```sql
-- SQL Server
CREATE TABLE #temp_results (
    id INT,
    score DECIMAL(5,2)
);
```
**Explanation:** The `#` prefix makes it a local temp table; `##` would be global across sessions.

---

## Q24: Create a table only if it does not already exist in MySQL.

**Query:**
```sql
-- MySQL
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
```
**Explanation:** `IF NOT EXISTS` prevents errors when the table already exists.

---

## Q25: Create a table only if it does not already exist in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
```
**Explanation:** PostgreSQL supports `IF NOT EXISTS` natively, identical semantics to MySQL.

---

## Q26: Copy an existing table's structure without data in PostgreSQL using `LIKE`.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE orders_backup (LIKE orders);
```
**Explanation:** `LIKE` copies columns, types, defaults, and constraints but not data or indexes.

**Alt1:**
```sql
-- PostgreSQL (include constraints too)
CREATE TABLE orders_backup (LIKE orders INCLUDING CONSTRAINTS INCLUDING DEFAULTS);
```
`INCLUDING CONSTRAINTS` also copies check, unique, and foreign key constraints.

---

## Q27: Copy an existing table's structure without data in MySQL using `LIKE`.

**Query:**
```sql
-- MySQL
CREATE TABLE orders_backup LIKE orders;
```
**Explanation:** MySQL's `LIKE` copies the full structure including indexes and auto_increment settings.

---

## Q28: Truncate the `logs` table efficiently in MySQL.

**Query:**
```sql
-- MySQL
TRUNCATE TABLE logs;
```
**Explanation:** `TRUNCATE` removes all rows faster than `DELETE`, resets auto_increment, and logs less.

---

## Q29: Explain the difference between `TRUNCATE` and `DELETE` on `logs` with a `WHERE` clause in SQL Server.

**Query:**
```sql
-- SQL Server
-- DELETE supports WHERE:
DELETE FROM logs WHERE logged_at < '2024-01-01';

-- TRUNCATE does not support WHERE:
-- TRUNCATE TABLE logs;  -- removes ALL rows
```
**Explanation:** `DELETE` is row-by-row (slower, logged, fires triggers) and supports `WHERE`; `TRUNCATE` is all-or-nothing (faster, minimal logging).

**Alt1:**
```sql
-- PostgreSQL
TRUNCATE logs RESTART IDENTITY;
```
`RESTART IDENTITY` resets the sequence — equivalent to MySQL's auto_increment reset.

---

## Q30: Drop the `archive_orders` table if it exists in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
DROP TABLE IF EXISTS archive_orders;
```
**Explanation:** `IF EXISTS` prevents an error when the table is absent.

---

## Q31: Drop a table with dependent foreign keys in MySQL using `CASCADE`.

**Query:**
```sql
-- MySQL
DROP TABLE departments CASCADE;
```
**Explanation:** `CASCADE` automatically drops foreign keys in other tables that reference this table.

**Alt1:**
```sql
-- SQL Server
DROP TABLE departments;
-- SQL Server drops FKs automatically when the referenced table is dropped.
```
SQL Server's default behavior handles dependent FKs without explicit `CASCADE`.

---

## Q32: Drop a table with dependent objects in PostgreSQL using `RESTRICT`.

**Query:**
```sql
-- PostgreSQL
DROP TABLE departments RESTRICT;
```
**Explanation:** `RESTRICT` (the default) blocks the drop if any other object depends on it.

---

## Q33: Create a `sales` table with a `CHECK` constraint on `quantity > 0` and `discount >= 0`.

**Query:**
```sql
CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    discount DECIMAL(5, 2) NOT NULL CHECK (discount >= 0)
);
```
**Explanation:** Separate inline `CHECK` constraints ensure positive quantities and non-negative discounts.

---

## Q34: Create a `users` table with a generated/stored column that concatenates first and last name.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    full_name VARCHAR(101) GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED
);
```
**Explanation:** A `STORED` generated column is computed on write and physically stored; no triggers needed.

**Alt1:**
```sql
-- MySQL
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    full_name VARCHAR(101) GENERATED ALWAYS AS (CONCAT(first_name, ' ', last_name)) STORED
);
```
MySQL's `GENERATED ALWAYS AS` uses `CONCAT` instead of the `||` operator.

**Alt2:**
```sql
-- SQL Server
CREATE TABLE users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    full_name AS first_name + N' ' + last_name PERSISTED
);
```
SQL Server uses `AS <expr> PERSISTED` for computed columns.

---

## Q35: Create a `products` table where the `sku` column has a unique constraint and a default value.

**Query:**
```sql
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    sku VARCHAR(30) NOT NULL UNIQUE DEFAULT 'SKU-000',
    name VARCHAR(200) NOT NULL
);
```
**Explanation:** `UNIQUE` prevents duplicate SKUs; `DEFAULT` provides a fallback when none is supplied.

---

## Q36: Create an `audit_log` table with a column comment describing its purpose in MySQL.

**Query:**
```sql
-- MySQL
CREATE TABLE audit_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    action VARCHAR(50) NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) COMMENT = 'Records all data modification events for compliance';
```
**Explanation:** MySQL supports table-level comments via `COMMENT`; useful for documentation in ORMs.

**Alt1:**
```sql
-- PostgreSQL
COMMENT ON TABLE audit_log IS 'Records all data modification events for compliance';
```
PostgreSQL uses a separate `COMMENT ON` statement after table creation.

---

## Q37: Add a `NOT NULL` constraint to an existing nullable column `phone` in PostgreSQL using `ALTER TABLE`.

**Query:**
```sql
-- PostgreSQL
ALTER TABLE employees
ALTER COLUMN phone SET NOT NULL;
```
**Explanation:** PostgreSQL uses `ALTER COLUMN ... SET NOT NULL` — a separate statement from type change.

---

## Q38: Add a `NOT NULL` constraint to an existing column in SQL Server.

**Query:**
```sql
-- SQL Server
ALTER TABLE employees
ALTER COLUMN phone VARCHAR(20) NOT NULL;
```
**Explanation:** SQL Server requires restating the full column definition including type when altering nullability.

---

## Q39: Add a named `UNIQUE` constraint on `email` in an existing `customers` table in MySQL.

**Query:**
```sql
-- MySQL
ALTER TABLE customers
ADD CONSTRAINT uq_customer_email UNIQUE (email);
```
**Explanation:** Named constraints make error messages and future `DROP CONSTRAINT` calls clearer.

---

## Q40: Add a `CHECK` constraint on an existing `products` table so that `price` must be positive, in Oracle.

**Query:**
```sql
-- Oracle
ALTER TABLE products
ADD CONSTRAINT chk_price_positive CHECK (price > 0);
```
**Explanation:** Oracle supports `ADD CONSTRAINT ... CHECK` directly via `ALTER TABLE`.

---

## Q41: Drop a `CHECK` constraint named `chk_age` from a table in SQL Server.

**Query:**
```sql
-- SQL Server
ALTER TABLE check_test
DROP CONSTRAINT chk_age;
```
**Explanation:** Use the constraint name in `DROP CONSTRAINT` regardless of type.

---

## Q42: Drop a default value from the `status` column in a MySQL table.

**Query:**
```sql
-- MySQL
ALTER TABLE orders
ALTER COLUMN status DROP DEFAULT;
```
**Explanation:** `DROP DEFAULT` removes the server-side default so inserts must supply a value.

---

## Q43: Create a `transactions` table with a composite foreign key referencing `(customer_id, order_id)` in another table.

**Query:**
```sql
CREATE TABLE transactions (
    txn_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_id INT NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (customer_id, order_id) REFERENCES orders(customer_id, order_id)
);
```
**Explanation:** A composite FK ensures both columns together match a valid row in the parent table.

---

## Q44: Create a `reviews` table with a `TEXT` primary key alternative — use a surrogate `id` instead and explain why.

**Query:**
```sql
CREATE TABLE reviews (
    review_id INT PRIMARY KEY,
    product_id INT NOT NULL,
    author VARCHAR(100) NOT NULL,
    body TEXT NOT NULL
);
```
**Explanation:** Text columns are poor PKs (wide, slow comparisons, collation issues); a surrogate integer PK is preferable.

---

## Q45: Create a `categories` table with a self-referencing foreign key for a tree structure.

**Query:**
```sql
CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_id INT,
    FOREIGN KEY (parent_id) REFERENCES categories(category_id)
);
```
**Explanation:** A self-referencing FK models hierarchical data — each category optionally points to its parent.

---

## Q46: Use `ALTER TABLE` to rename a column `full_name` to `display_name` in MySQL.

**Query:**
```sql
-- MySQL
ALTER TABLE users
RENAME COLUMN full_name TO display_name;
```
**Explanation:** MySQL 8.0+ supports `RENAME COLUMN`; earlier versions required `CHANGE`.

**Alt1:**
```sql
-- MySQL (legacy)
ALTER TABLE users
CHANGE COLUMN full_name display_name VARCHAR(200) NOT NULL;
```
`CHANGE` requires restating the full column definition.

---

## Q47: Rename a column in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
ALTER TABLE users
RENAME COLUMN full_name TO display_name;
```
**Explanation:** PostgreSQL supports `RENAME COLUMN` syntax directly.

---

## Q48: Add a `DEFAULT` value to an existing column `status` in SQL Server.

**Query:**
```sql
-- SQL Server
ALTER TABLE orders
ADD CONSTRAINT df_status DEFAULT 'pending' FOR status;
```
**Explanation:** SQL Server uses `ADD CONSTRAINT ... DEFAULT ... FOR` to attach defaults after creation.

**Alt1:**
```sql
-- PostgreSQL
ALTER TABLE orders
ALTER COLUMN status SET DEFAULT 'pending';
```
PostgreSQL uses `ALTER COLUMN ... SET DEFAULT`.

---

## Q49: Create a `tickets` table with an auto-generated UUID primary key in SQL Server.

**Query:**
```sql
-- SQL Server
CREATE TABLE tickets (
    ticket_id UNIQUEIDENTIFIER DEFAULT NEWID() PRIMARY KEY,
    subject NVARCHAR(200) NOT NULL,
    created_at DATETIME2 DEFAULT SYSUTCDATETIME()
);
```
**Explanation:** `NEWID()` generates a random UUID; `DATETIME2` is the modern timestamp type in SQL Server.

**Alt1:**
```sql
-- SQL Server (sequential UUID for better index performance)
CREATE TABLE tickets (
    ticket_id UNIQUEIDENTIFIER DEFAULT NEWSEQUENTIALID() PRIMARY KEY,
    subject NVARCHAR(200) NOT NULL,
    created_at DATETIME2 DEFAULT SYSUTCDATETIME()
);
```
`NEWSEQUENTIALID()` produces time-ordered UUIDs, reducing B-tree page splits.

---

## Q50: Create an `inventory` table with a `TIMESTAMP` column in MySQL that auto-updates on row modification.

**Query:**
```sql
-- MySQL
CREATE TABLE inventory (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    quantity INT NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```
**Explanation:** `ON UPDATE CURRENT_TIMESTAMP` automatically refreshes the timestamp on every `UPDATE`.

---

## Q51: Create an `inventory` table with an auto-updating timestamp in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE inventory (
    item_id SERIAL PRIMARY KEY,
    quantity INT NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** PostgreSQL lacks `ON UPDATE`; use a trigger or application logic to refresh the timestamp.

**Alt1:**
```sql
-- PostgreSQL (trigger-based auto-update)
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_inventory_updated
BEFORE UPDATE ON inventory
FOR EACH ROW EXECUTE FUNCTION update_timestamp();
```
A `BEFORE UPDATE` trigger sets `updated_at` on every row modification.

---

## Q52: Create a `bookings` table in Oracle with a `DATE` column and a `TIMESTAMP` column.

**Query:**
```sql
-- Oracle
CREATE TABLE bookings (
    booking_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    booking_date DATE NOT NULL,
    booked_at TIMESTAMP DEFAULT SYSTIMESTAMP
);
```
**Explanation:** Oracle distinguishes `DATE` (includes time to the second internally) from `TIMESTAMP` (fractional seconds).

---

## Q53: Create a `legacy_data` table with a `CHAR(36)` column for UUID storage in MySQL.

**Query:**
```sql
-- MySQL
CREATE TABLE legacy_data (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    external_uuid CHAR(36) NOT NULL,
    payload TEXT
);
```
**Explanation:** `CHAR(36)` stores UUIDs as human-readable strings; less efficient than `BINARY(16)` but simpler for debugging.

---

## Q54: Create a `config` table with a `JSONB` column and a GIN index in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE config (
    key VARCHAR(100) PRIMARY KEY,
    value JSONB NOT NULL
);

CREATE INDEX idx_config_value ON config USING GIN (value);
```
**Explanation:** `JSONB` stores parsed binary JSON; a GIN index enables fast containment (`@>`) and key-existence queries.

---

## Q55: Create an `employees` table with a `BIGINT` primary key for a table expected to exceed 2 billion rows.

**Query:**
```sql
CREATE TABLE employees (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100)
);
```
**Explanation:** `BIGINT` supports up to ~9.2 × 10^18 values — necessary when `INT` (max ~2.1 billion) is insufficient.

---

## Q56: Create a `countries` table with a fixed-length `CHAR(2)` column for ISO country codes.

**Query:**
```sql
CREATE TABLE countries (
    code CHAR(2) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    population BIGINT
);
```
**Explanation:** ISO 3166-1 alpha-2 codes are always 2 characters; `CHAR` avoids wasted storage vs `VARCHAR`.

---

## Q57: Create a `subscriptions` table with a `BOOLEAN` flag and a `NOT NULL` constraint in MySQL.

**Query:**
```sql
-- MySQL
CREATE TABLE subscriptions (
    sub_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    started_at DATE NOT NULL
);
```
**Explanation:** `TINYINT(1)` is MySQL's boolean representation; `NOT NULL DEFAULT 1` ensures every row has a value.

---

## Q58: Create a `sensor_readings` table with a `NUMERIC` column for high-precision scientific data.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE sensor_readings (
    reading_id SERIAL PRIMARY KEY,
    sensor_id INT NOT NULL,
    temperature NUMERIC(8, 4) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** `NUMERIC(8,4)` stores values like 36.5123 with exact precision — no floating-point rounding.

---

## Q59: Create a `pricing` table with a `DECIMAL` column that disallows zero values via a `CHECK` constraint.

**Query:**
```sql
CREATE TABLE pricing (
    product_id INT PRIMARY KEY,
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price > 0),
    currency CHAR(3) NOT NULL DEFAULT 'USD'
);
```
**Explanation:** `CHECK (unit_price > 0)` combined with `NOT NULL` ensures only positive prices.

---

## Q60: Create a `migrations` table to track schema changes, including a `CHAR(40)` column for SHA-1 hashes.

**Query:**
```sql
CREATE TABLE migrations (
    migration_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    hash CHAR(40) NOT NULL,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** `CHAR(40)` is exactly the length of a SHA-1 hex digest; fixed length for efficient storage.

---

## Q61: Create a `webhooks` table with a `TEXT` URL column and a `BOOLEAN` enabled flag in SQL Server.

**Query:**
```sql
-- SQL Server
CREATE TABLE webhooks (
    webhook_id INT IDENTITY(1,1) PRIMARY KEY,
    url NVARCHAR(2048) NOT NULL,
    enabled BIT NOT NULL DEFAULT 1,
    secret NVARCHAR(255)
);
```
**Explanation:** `BIT` is SQL Server's boolean type; `NVARCHAR(2048)` accommodates long URLs with Unicode.

---

## Q62: Create an `audit_trail` table with a `TIMESTAMP` column that stores only the date in MySQL.

**Query:**
```sql
-- MySQL
CREATE TABLE audit_trail (
    trail_id INT AUTO_INCREMENT PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    event_date DATE NOT NULL
);
```
**Explanation:** `DATE` stores only `YYYY-MM-DD` without time — appropriate when time-of-day is irrelevant.

---

## Q63: Create a `user_preferences` table with a `JSONB` column as the primary key's companion in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE user_preferences (
    user_id INT PRIMARY KEY,
    preferences JSONB NOT NULL DEFAULT '{}'::jsonb
);
```
**Explanation:** `DEFAULT '{}'::jsonb` ensures the column starts with an empty JSON object, not null.

---

## Q64: Create a `coupon_codes` table with a `VARCHAR(8)` primary key and an expiry `DATE`.

**Query:**
```sql
CREATE TABLE coupon_codes (
    code VARCHAR(8) PRIMARY KEY,
    discount_pct DECIMAL(5, 2) NOT NULL,
    expires_on DATE NOT NULL
);
```
**Explanation:** Short coupon codes make natural PKs; `DATE` without time is sufficient for expiry.

---

## Q65: Create a `sessions` table and demonstrate how `ON DELETE CASCADE` propagates deletes from `users`.

**Query:**
```sql
CREATE TABLE sessions (
    session_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
```
**Explanation:** When a user is deleted, all their sessions are automatically removed.

---

## Q66: Create a `user_roles` junction table with `ON DELETE SET NULL` for a soft assignment pattern.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE user_roles (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE SET NULL
);
```
**Explanation:** If a role is deleted, `role_id` in the junction becomes `NULL` — but since it's part of the PK, this pattern requires careful design; typically `ON DELETE CASCADE` is preferred for junction tables.

---

## Q67: Create a `products` table with a `CHECK` constraint that ensures `end_date > start_date`.

**Query:**
```sql
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    CHECK (end_date > start_date)
);
```
**Explanation:** Cross-column `CHECK` constraints validate relationships between fields.

---

## Q68: Create a `file_uploads` table with a `BIGINT` column for file size in bytes.

**Query:**
```sql
CREATE TABLE file_uploads (
    upload_id INT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_size BIGINT NOT NULL CHECK (file_size >= 0),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** `BIGINT` supports files up to ~8 exabytes; `CHECK (>= 0)` prevents nonsensical negative sizes.

---

## Q69: Create an `api_keys` table with a `CHAR(64)` column for a hex-encoded SHA-256 key.

**Query:**
```sql
CREATE TABLE api_keys (
    key_id INT PRIMARY KEY,
    key_hash CHAR(64) NOT NULL UNIQUE,
    owner_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** `CHAR(64)` is exactly 64 hex characters (256 bits); `UNIQUE` prevents duplicate keys.

---

## Q70: Create a `geolocation` table with `DECIMAL(9,6)` for latitude and longitude.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE geolocation (
    location_id SERIAL PRIMARY KEY,
    latitude NUMERIC(9, 6) NOT NULL CHECK (latitude BETWEEN -90 AND 90),
    longitude NUMERIC(9, 6) NOT NULL CHECK (longitude BETWEEN -180 AND 180),
    label VARCHAR(100)
);
```
**Explanation:** `NUMERIC(9,6)` gives ~11cm precision at the equator; `CHECK` constraints enforce valid ranges.

---

## Q71: Create a `time_entries` table with a `TIME` column for daily work-hour tracking.

**Query:**
```sql
CREATE TABLE time_entries (
    entry_id INT PRIMARY KEY,
    employee_id INT NOT NULL,
    clock_in TIME NOT NULL,
    clock_out TIME,
    entry_date DATE NOT NULL
);
```
**Explanation:** `TIME` stores hours/minutes/seconds without a date — perfect for shift-start and shift-end.

---

## Q72: Create a `currencies` table with a `CHAR(3)` ISO code and a `SMALLINT` minor-unit exponent.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE currencies (
    code CHAR(3) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    minor_unit_exponent SMALLINT NOT NULL DEFAULT 2
);
```
**Explanation:** `SMALLINT` (2 bytes) suffices for values like 0, 2, or 3; saves space vs `INT`.

---

## Q73: Create a `password_history` table with a `VARCHAR(255)` for bcrypt hashes.

**Query:**
```sql
CREATE TABLE password_history (
    history_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** `VARCHAR(255)` comfortably holds bcrypt hashes (60 chars) and future hash formats.

---

## Q74: Create a `search_index` table with a `TSVECTOR` column in PostgreSQL for full-text search.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE search_index (
    doc_id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    search_vector TSVECTOR
);

CREATE INDEX idx_search ON search_index USING GIN (search_vector);
```
**Explanation:** `TSVECTOR` stores preprocessed tokens for fast full-text search; the GIN index speeds up `@@` queries.

---

## Q75: Create a `measurements` table with a `REAL` column for approximate scientific float storage.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE measurements (
    measurement_id SERIAL PRIMARY KEY,
    sensor_id INT NOT NULL,
    value REAL NOT NULL,
    unit VARCHAR(10) NOT NULL,
    measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** `REAL` (4 bytes) is a single-precision float — sufficient when exact precision isn't required and storage matters.

---

## Q76: Create a `measurements` table with a `DOUBLE PRECISION` column for high-accuracy scientific data.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE measurements (
    measurement_id SERIAL PRIMARY KEY,
    sensor_id INT NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(10) NOT NULL,
    measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** `DOUBLE PRECISION` (8 bytes) offers ~15 decimal digits — use when `REAL` precision is insufficient.

---

## Q77: Create a `transactions` table with a `MONEY` type in SQL Server.

**Query:**
```sql
-- SQL Server
CREATE TABLE transactions (
    txn_id INT IDENTITY(1,1) PRIMARY KEY,
    account_id INT NOT NULL,
    amount MONEY NOT NULL,
    txn_date DATETIME2 DEFAULT SYSUTCDATETIME()
);
```
**Explanation:** SQL Server's `MONEY` type is 8 bytes and stores values with 4 decimal places — convenient but `DECIMAL` offers more control.

**Alt1:**
```sql
-- SQL Server (preferred)
CREATE TABLE transactions (
    txn_id INT IDENTITY(1,1) PRIMARY KEY,
    account_id INT NOT NULL,
    amount DECIMAL(19, 4) NOT NULL,
    txn_date DATETIME2 DEFAULT SYSUTCDATETIME()
);
```
`DECIMAL(19,4)` is often preferred over `MONEY` for portability and precision control.

---

## Q78: Create a `news_articles` table with a `TEXT` body, a `VARCHAR` title, and a `BOOLEAN` published flag in MySQL.

**Query:**
```sql
-- MySQL
CREATE TABLE news_articles (
    article_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(300) NOT NULL,
    body TEXT NOT NULL,
    published TINYINT(1) NOT NULL DEFAULT 0,
    published_at TIMESTAMP NULL
);
```
**Explanation:** `TEXT` handles long-form content; `TINYINT(1)` is MySQL's boolean; `published_at TIMESTAMP NULL` allows nullable timestamps.

---

## Q79: Create a `shopping_cart` table with a `JSONB` column for item storage in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE shopping_cart (
    cart_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    items JSONB NOT NULL DEFAULT '[]'::jsonb,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** `JSONB` with `DEFAULT '[]'::jsonb` starts each cart with an empty array; flexible schema for varying item structures.

---

## Q80: Create a `server_config` table in MySQL with a `TEXT` column for YAML configuration and `IF NOT EXISTS`.

**Query:**
```sql
-- MySQL
CREATE TABLE IF NOT EXISTS server_config (
    config_key VARCHAR(100) PRIMARY KEY,
    config_value TEXT NOT NULL,
    updated_by VARCHAR(50),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```
**Explanation:** `IF NOT EXISTS` is safe for idempotent migrations; `TEXT` holds arbitrarily large YAML/JSON config.

---

## Q81: Create a `versioned_config` table that stores the previous configuration via `CREATE TABLE AS` snapshot pattern.

**Query:**
```sql
-- MySQL
CREATE TABLE versioned_config AS
SELECT config_key, config_value, updated_at AS snapshot_at
FROM server_config
WHERE 1 = 0;
```
**Explanation:** `WHERE 1 = 0` copies the schema without any rows — a common pattern for creating an empty structural copy.

**Alt1:**
```sql
-- PostgreSQL
CREATE TABLE versioned_config (LIKE server_config INCLUDING DEFAULTS);
```
`LIKE` without data is cleaner and also copies constraints and defaults.

---

## Q82: Create a `notifications` table with a `VARCHAR(20)` column for notification type using an ENUM-like approach in MySQL.

**Query:**
```sql
-- MySQL
CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    type ENUM('email', 'sms', 'push', 'in_app') NOT NULL,
    payload TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** MySQL's `ENUM` stores a fixed set of allowed values as integers internally — compact and constrained.

**Alt1:**
```sql
-- PostgreSQL
CREATE TABLE notifications (
    notification_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('email', 'sms', 'push', 'in_app')),
    payload TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
PostgreSQL uses `CHECK` with `IN` list instead of `ENUM` for simpler maintenance.

---

## Q83: Create a `shipping_addresses` table with a `BOOLEAN NOT NULL DEFAULT FALSE` for the `is_default` flag in SQL Server.

**Query:**
```sql
-- SQL Server
CREATE TABLE shipping_addresses (
    address_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    street NVARCHAR(255) NOT NULL,
    city NVARCHAR(100) NOT NULL,
    is_default BIT NOT NULL DEFAULT 0
);
```
**Explanation:** `BIT NOT NULL DEFAULT 0` ensures the column is always populated with a boolean value.

---

## Q84: Create a `data_migrations` table with a `SERIAL` primary key and a `TEXT` column for SQL statements in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE data_migrations (
    migration_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    up_sql TEXT NOT NULL,
    down_sql TEXT,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** `TEXT` stores unbounded SQL strings; `SERIAL` auto-generates migration IDs.

---

## Q85: Create a `cache_entries` table with a `TIMESTAMP` column that expires entries using a computed expression in Oracle.

**Query:**
```sql
-- Oracle
CREATE TABLE cache_entries (
    cache_key VARCHAR(200) PRIMARY KEY,
    cache_value CLOB NOT NULL,
    expires_at TIMESTAMP GENERATED ALWAYS AS (created_at + INTERVAL '1' HOUR) STORED,
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP
);
```
**Explanation:** Oracle's generated column computes `expires_at` as one hour after creation — no application logic needed.

**Alt1:**
```sql
-- PostgreSQL
CREATE TABLE cache_entries (
    cache_key VARCHAR(200) PRIMARY KEY,
    cache_value TEXT NOT NULL,
    expires_at TIMESTAMP GENERATED ALWAYS AS (created_at + INTERVAL '1 hour') STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
PostgreSQL supports the same `GENERATED ALWAYS AS ... STORED` syntax.

---

## Q86: Create an `i18n_strings` table with a `CHAR(5)` column for locale codes like `en-US`.

**Query:**
```sql
CREATE TABLE i18n_strings (
    string_key VARCHAR(100) NOT NULL,
    locale CHAR(5) NOT NULL,
    translation TEXT NOT NULL,
    PRIMARY KEY (string_key, locale)
);
```
**Explanation:** `CHAR(5)` fits locale codes like `en-US` or `fr-FR` exactly; composite PK ensures unique translations per key-locale pair.

---

## Q87: Create a `feature_flags` table with a `BOOLEAN` toggle, a `JSONB` targeting rules column, and a `TEXT` description in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE feature_flags (
    flag_name VARCHAR(100) PRIMARY KEY,
    enabled BOOLEAN NOT NULL DEFAULT FALSE,
    targeting_rules JSONB DEFAULT '{}'::jsonb,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** Combines a boolean toggle with flexible JSON targeting rules — a common feature-flag table design.

---

## Q88: Create a `resume_sections` table with a `VARCHAR(20)` column for section type and a `SMALLINT` for sort order in MySQL.

**Query:**
```sql
-- MySQL
CREATE TABLE resume_sections (
    section_id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT NOT NULL,
    section_type VARCHAR(20) NOT NULL,
    sort_order SMALLINT NOT NULL DEFAULT 0,
    content TEXT NOT NULL
);
```
**Explanation:** `SMALLINT` (max 32,767) is sufficient for sort order and saves a byte vs `INT`.

---

## Q89: Create a `case_study` table with a `VARCHAR(3)` column for priority levels using `CHECK` constraint in SQL Server.

**Query:**
```sql
-- SQL Server
CREATE TABLE case_study (
    case_id INT IDENTITY(1,1) PRIMARY KEY,
    title NVARCHAR(200) NOT NULL,
    priority CHAR(3) NOT NULL CHECK (priority IN ('LOW', 'MED', 'HI ')),
    status VARCHAR(20) NOT NULL DEFAULT 'open'
);
```
**Explanation:** `CHAR(3)` stores fixed-length priority codes; `CHECK` restricts allowed values.

---

## Q90: Create a `sessions` table demonstrating the trade-off between identity columns and UUID primary keys.

**Query:**
```sql
-- PostgreSQL (identity approach)
CREATE TABLE sessions_v1 (
    session_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PostgreSQL (UUID approach)
CREATE TABLE sessions_v2 (
    session_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** Identity/BIGINT is compact and ordered (better index performance); UUID is globally unique (better for distributed systems, no central coordination needed).

---

## Q91: Create a `survey_responses` table with a `BOOLEAN NOT NULL` for a required yes/no answer field.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE survey_responses (
    response_id SERIAL PRIMARY KEY,
    survey_id INT NOT NULL,
    respondent_id INT NOT NULL,
    answer BOOLEAN NOT NULL,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** `BOOLEAN NOT NULL` forces every response to have an explicit true/false — no ambiguity.

---

## Q92: Create a `cdn_files` table with a `BIGINT` column for file size and a `VARCHAR(100)` MIME type in MySQL.

**Query:**
```sql
-- MySQL
CREATE TABLE cdn_files (
    file_id INT AUTO_INCREMENT PRIMARY KEY,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** `BIGINT` handles files up to 8 EB; `VARCHAR(100)` stores MIME types like `application/pdf`.

---

## Q93: Create a `stock_prices` table with a `NUMERIC(12, 4)` for price and a `NUMERIC(14, 4)` for market cap.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE stock_prices (
    ticker VARCHAR(10) NOT NULL,
    trade_date DATE NOT NULL,
    price NUMERIC(12, 4) NOT NULL CHECK (price >= 0),
    market_cap NUMERIC(14, 4) CHECK (market_cap >= 0),
    PRIMARY KEY (ticker, trade_date)
);
```
**Explanation:** `NUMERIC(12,4)` handles prices up to ~999M with 4 decimal places; composite PK prevents duplicate entries per ticker-day.

---

## Q94: Create a `case_notes` table with a `TIMESTAMP` column that stores both date and time to microsecond precision in Oracle.

**Query:**
```sql
-- Oracle
CREATE TABLE case_notes (
    note_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    case_number VARCHAR2(30) NOT NULL,
    note_text CLOB NOT NULL,
    created_at TIMESTAMP(6) DEFAULT SYSTIMESTAMP
);
```
**Explanation:** `TIMESTAMP(6)` stores fractional seconds to 6 decimal places (microseconds); `CLOB` holds arbitrarily long notes.

---

## Q95: Create a `chat_messages` table with a `BOOLEAN` edited flag and a nullable `TIMESTAMP` for edit time in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
CREATE TABLE chat_messages (
    message_id SERIAL PRIMARY KEY,
    channel_id INT NOT NULL,
    sender_id INT NOT NULL,
    body TEXT NOT NULL,
    was_edited BOOLEAN NOT NULL DEFAULT FALSE,
    edited_at TIMESTAMP,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** `was_edited` is a required flag; `edited_at` is nullable — only set when `was_edited` becomes true.

---

## Q96: Create a `price_history` table with a `DECIMAL(8, 2)` and a composite PK including a date range using `DATE` columns.

**Query:**
```sql
CREATE TABLE price_history (
    product_id INT NOT NULL,
    effective_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    price DECIMAL(8, 2) NOT NULL CHECK (price > 0),
    PRIMARY KEY (product_id, effective_date),
    CHECK (expiry_date > effective_date)
);
```
**Explanation:** Composite PK on product + effective date; `CHECK` ensures the validity window is logical.

---

## Q97: Create a `user_sessions` table in MySQL using `GENERATED ALWAYS AS IDENTITY` (MySQL 8.0+).

**Query:**
```sql
-- MySQL 8.0+
CREATE TABLE user_sessions (
    session_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Explanation:** `GENERATED ALWAYS AS IDENTITY` is the SQL-standard syntax supported from MySQL 8.0 — more portable than `AUTO_INCREMENT`.

---

## Q98: Create a `project_tasks` table with a `VARCHAR(20)` for status and a `TIMESTAMP` deadline, using constraint ordering to place the `CHECK` after column definitions in Oracle.

**Query:**
```sql
-- Oracle
CREATE TABLE project_tasks (
    task_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_id NUMBER NOT NULL,
    title VARCHAR2(200) NOT NULL,
    status VARCHAR2(20) NOT NULL,
    deadline TIMESTAMP,
    CONSTRAINT chk_task_status CHECK (status IN ('todo', 'in_progress', 'done', 'blocked')),
    CONSTRAINT chk_task_deadline CHECK (deadline IS NULL OR deadline > created_at),
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP
);
```
**Explanation:** Named `CHECK` constraints after column definitions improve readability; `chk_task_deadline` enforces a cross-column business rule.

---

## Q99: Create a `multi_step_example` demonstrating an interactive ALTER scenario: start with a minimal table, add columns, add constraints, and rename the table — all in sequence.

**Query:**
```sql
-- Step 1: Create minimal table
CREATE TABLE tmp_contacts (
    id INT PRIMARY KEY
);

-- Step 2: Add columns
ALTER TABLE tmp_contacts ADD COLUMN name VARCHAR(100) NOT NULL;
ALTER TABLE tmp_contacts ADD COLUMN email VARCHAR(255);
ALTER TABLE tmp_contacts ADD COLUMN phone VARCHAR(20);

-- Step 3: Add constraints
ALTER TABLE tmp_contacts ADD CONSTRAINT uq_tmp_email UNIQUE (email);
ALTER TABLE tmp_contacts ADD CONSTRAINT chk_tmp_name CHECK (LENGTH(name) > 0);

-- Step 4: Rename the table to its final name
ALTER TABLE tmp_contacts RENAME TO contacts;
```
**Explanation:** Incremental `ALTER TABLE` steps build up a table from a skeleton — useful in migration scripts that need fine-grained control.

---

## Q100: Create a `schema_comparison` table demonstrating storage engine choice in MySQL (InnoDB vs MyISAM), character set configuration, and collation in a single statement.

**Query:**
```sql
-- MySQL
CREATE TABLE schema_comparison (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci
  COMMENT = 'Demonstrates engine, charset, and collation in one DDL';
```
**Explanation:** `InnoDB` supports transactions, row-level locking, and foreign keys (MyISAM does not); `utf8mb4` is the full Unicode character set (including emoji); `utf8mb4_unicode_ci` provides case-insensitive Unicode sorting.
