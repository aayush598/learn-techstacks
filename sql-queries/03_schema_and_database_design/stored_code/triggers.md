# Triggers — 100 SQL Interview Q&A

## Q1: Create a basic AFTER INSERT trigger that logs every new employee into an audit table.

**Query:**
```sql
-- MySQL / PostgreSQL
CREATE TABLE employee_audit (
    audit_id   INT AUTO_INCREMENT PRIMARY KEY,
    emp_id     INT,
    action     VARCHAR(10),
    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //
CREATE TRIGGER trg_after_insert_employee
AFTER INSERT ON employees
FOR EACH ROW
BEGIN
    INSERT INTO employee_audit (emp_id, action, changed_at)
    VALUES (NEW.emp_id, 'INSERT', NOW());
END //
DELIMITER ;
```
**Explanation:** `AFTER INSERT` fires once per inserted row; `NEW.emp_id` references the row just inserted. The audit row is written to a separate log table.

---

## Q2: Create a BEFORE INSERT trigger that automatically set a default department when none is provided.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_default_dept
BEFORE INSERT ON employees
FOR EACH ROW
BEGIN
    IF NEW.dept_id IS NULL THEN
        SET NEW.dept_id = 1;
    END IF;
END //
DELIMITER ;
```
**Explanation:** `BEFORE INSERT` lets you modify `NEW` columns before the row is written; if `dept_id` is NULL it gets replaced with 1.

---

## Q3: Write an AFTER UPDATE trigger that records old and new salary values in an audit trail.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_salary_change
AFTER UPDATE ON employees
FOR EACH ROW
BEGIN
    IF OLD.salary <> NEW.salary THEN
        INSERT INTO salary_audit (emp_id, old_salary, new_salary, changed_at)
        VALUES (OLD.emp_id, OLD.salary, NEW.salary, NOW());
    END IF;
END //
DELIMITER ;
```
**Explanation:** `OLD` holds pre-update values; `NEW` holds post-update values. The audit row is only inserted when the salary actually changes.

**Alt1:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_salary_audit() RETURNS TRIGGER AS $$
BEGIN
    IF OLD.salary IS DISTINCT FROM NEW.salary THEN
        INSERT INTO salary_audit (emp_id, old_salary, new_salary, changed_at)
        VALUES (OLD.emp_id, OLD.salary, NEW.salary, NOW());
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_salary_change
AFTER UPDATE ON employees
FOR EACH ROW
EXECUTE FUNCTION fn_salary_audit();
```
**Explanation:** PostgreSQL requires a PL/pgSQL function body; `IS DISTINCT FROM` safely handles NULL comparisons.

---

## Q4: Write an AFTER DELETE trigger that archives the deleted row into a history table.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_archive_employee
AFTER DELETE ON employees
FOR EACH ROW
BEGIN
    INSERT INTO employees_archive (emp_id, name, dept_id, salary, deleted_at)
    VALUES (OLD.emp_id, OLD.name, OLD.dept_id, OLD.salary, NOW());
END //
DELIMITER ;
```
**Explanation:** On deletion, `OLD` captures the disappearing row. The trigger copies it into an archive table before it is gone forever.

**Alt1:**
```sql
-- SQL Server
CREATE TRIGGER trg_archive_employee
ON employees
AFTER DELETE
AS
BEGIN
    INSERT INTO employees_archive (emp_id, name, dept_id, salary, deleted_at)
    SELECT emp_id, name, dept_id, salary, GETDATE()
    FROM deleted;
END;
```
**Explanation:** SQL Server uses the virtual `deleted` table (which holds all rows affected by DELETE) instead of `OLD`.

---

## Q5: Create a statement-level trigger in PostgreSQL that fires once per DELETE statement, not per row.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_row_count_log() RETURNS TRIGGER AS $$
BEGIN
    RAISE NOTICE 'Rows affected: %', (SELECT count(*) FROM deleted_rows());
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_statement_delete
AFTER DELETE ON employees
FOR EACH STATEMENT
EXECUTE FUNCTION fn_row_count_log();
```
**Explanation:** `FOR EACH STATEMENT` fires the trigger once regardless of how many rows were deleted, unlike `FOR EACH ROW`.

---

## Q6: Create a statement-level trigger in SQL Server that fires once per UPDATE.

**Query:**
```sql
-- SQL Server
CREATE TRIGGER trg_statement_update
ON employees
AFTER UPDATE
AS
BEGIN
    DECLARE @count INT = (SELECT COUNT(*) FROM inserted);
    INSERT INTO trigger_log (table_name, action, row_count, fired_at)
    VALUES ('employees', 'UPDATE', @count, GETDATE());
END;
```
**Explanation:** SQL Server triggers are statement-level by default. The `inserted` table holds all post-update rows for the entire statement.

---

## Q7: Write a BEFORE UPDATE trigger that prevents salary from going below the minimum wage.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_min_salary_check
BEFORE UPDATE ON employees
FOR EACH ROW
BEGIN
    IF NEW.salary < 30000 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Salary cannot be below minimum wage';
    END IF;
END //
DELIMITER ;
```
**Explanation:** `SIGNAL SQLSTATE '45000'` raises a user-defined error that rolls back the entire statement when the check fails.

**Alt1:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_min_salary() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.salary < 30000 THEN
        RAISE EXCEPTION 'Salary cannot be below minimum wage';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_min_salary_check
BEFORE UPDATE ON employees
FOR EACH ROW
EXECUTE FUNCTION fn_min_salary();
```
**Explanation:** PostgreSQL uses `RAISE EXCEPTION` in a function to abort the transaction and return the error to the client.

---

## Q8: Use a trigger in SQL Server to block all DELETE operations on a critical table.

**Query:**
```sql
-- SQL Server
CREATE TRIGGER trg_block_delete
ON employees
INSTEAD OF DELETE
AS
BEGIN
    RAISERROR ('Deleting employees is not allowed', 16, 1);
END;
```
**Explanation:** `INSTEAD OF DELETE` intercepts the delete and never executes it; the raiserror tells the client why it failed.

**Alt1:**
```sql
-- PostgreSQL (row-level equivalent)
CREATE OR REPLACE FUNCTION fn_block_delete() RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Deleting employees is not allowed';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_block_delete
BEFORE DELETE ON employees
FOR EACH ROW
EXECUTE FUNCTION fn_block_delete();
```
**Explanation:** PostgreSQL has no `INSTEAD OF` at the table level, so a `BEFORE DELETE` trigger raising an exception achieves the same block.

---

## Q9: Write an INSTEAD OF INSERT trigger on a view that inserts into the underlying base tables.

**Query:**
```sql
-- SQL Server
CREATE VIEW v_employee_detail AS
SELECT e.emp_id, e.name, d.dept_name
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id;

CREATE TRIGGER trg_instead_insert
ON v_employee_detail
INSTEAD OF INSERT
AS
BEGIN
    INSERT INTO departments (dept_name)
    SELECT DISTINCT dept_name FROM inserted
    WHERE dept_name NOT IN (SELECT dept_name FROM departments);

    INSERT INTO employees (emp_id, name, dept_id)
    SELECT i.emp_id, i.name, d.dept_id
    FROM inserted i
    JOIN departments d ON i.dept_name = d.dept_name;
END;
```
**Explanation:** A view with JOINs is not directly updatable. `INSTEAD OF INSERT` lets you decompose the insert into the correct base tables.

---

## Q10: Write an INSTEAD OF DELETE trigger on a view to cascade deletes into the correct base table.

**Query:**
```sql
-- SQL Server
CREATE TRIGGER trg_instead_delete
ON v_employee_detail
INSTEAD OF DELETE
AS
BEGIN
    DELETE FROM employees
    WHERE emp_id IN (SELECT emp_id FROM deleted);
END;
```
**Explanation:** The view cannot support a native DELETE because it joins two tables. The trigger delegates to a delete on the base `employees` table.

---

## Q11: Create a trigger that automatically updates the `updated_at` timestamp column on every UPDATE.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_set_updated_at
BEFORE UPDATE ON employees
FOR EACH ROW
BEGIN
    SET NEW.updated_at = NOW();
END //
DELIMITER ;
```
**Explanation:** The `BEFORE UPDATE` timing lets the trigger overwrite `updated_at` with the current time before the row is persisted.

**Alt1:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_set_updated_at() RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_set_updated_at
BEFORE UPDATE ON employees
FOR EACH ROW
EXECUTE FUNCTION fn_set_updated_at();
```
**Explanation:** PostgreSQL uses a function; the modified `NEW` is returned so the row includes the fresh timestamp.

---

## Q12: Maintain a running total (denormalized) in a summary table via a trigger after INSERT on orders.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_update_revenue
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE revenue_summary
    SET    total_revenue = total_revenue + NEW.amount,
           order_count   = order_count + 1
    WHERE  month = DATE_FORMAT(NEW.order_date, '%Y-%m');

    IF ROW_COUNT() = 0 THEN
        INSERT INTO revenue_summary (month, total_revenue, order_count)
        VALUES (DATE_FORMAT(NEW.order_date, '%Y-%m'), NEW.amount, 1);
    END IF;
END //
DELIMITER ;
```
**Explanation:** Each new order increments the denormalized totals in `revenue_summary`. If no row exists for that month, one is created.

---

## Q13: Keep an inventory stock counter updated with a trigger on INSERT into order_items.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_decrement_stock
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE products
    SET    stock = stock - NEW.quantity
    WHERE  product_id = NEW.product_id;

    IF (SELECT stock FROM products WHERE product_id = NEW.product_id) < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Insufficient stock';
    END IF;
END //
DELIMITER ;
```
**Explanation:** The trigger decrements the stock column and raises an error if stock goes negative. In production the stock check should happen BEFORE the insert to avoid the rollback.

---

## Q14: Write a BEFORE INSERT trigger that auto-generates a sequential ID using a custom counter instead of an identity column.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_custom_id
BEFORE INSERT ON invoices
FOR EACH ROW
BEGIN
    DECLARE next_id INT;
    SELECT counter_value + 1 INTO next_id
    FROM id_counters
    WHERE counter_name = 'invoices'
    FOR UPDATE;

    UPDATE id_counters
    SET    counter_value = next_id
    WHERE  counter_name = 'invoices';

    SET NEW.invoice_id = next_id;
END //
DELIMITER ;
```
**Explanation:** The trigger reads the current counter under a lock, increments it, and assigns the new value to `invoice_id` before the row is written.

**Alt1:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_custom_id() RETURNS TRIGGER AS $$
DECLARE
    next_id INT;
BEGIN
    UPDATE id_counters
    SET    counter_value = counter_value + 1
    WHERE  counter_name = 'invoices'
    RETURNING counter_value INTO next_id;

    NEW.invoice_id = next_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_custom_id
BEFORE INSERT ON invoices
FOR EACH ROW
EXECUTE FUNCTION fn_custom_id();
```
**Explanation:** PostgreSQL's `RETURNING` clause simplifies the read-then-update pattern into a single atomic statement.

---

## Q15: Fire a trigger only when a specific column (`salary`) is updated in SQL Server.

**Query:**
```sql
-- SQL Server
CREATE TRIGGER trg_salary_only
ON employees
AFTER UPDATE
AS
BEGIN
    IF UPDATE(salary)
    BEGIN
        INSERT INTO salary_audit (emp_id, old_salary, new_salary, changed_at)
        SELECT d.emp_id, d.salary, i.salary, GETDATE()
        FROM deleted d
        JOIN inserted i ON d.emp_id = i.emp_id
        WHERE d.salary <> i.salary;
    END;
END;
```
**Explanation:** `IF UPDATE(col)` is a SQL Server construct that checks whether the column appeared in the SET clause, even if the value didn't change.

---

## Q16: Fire a trigger only when the `salary` column actually changed value in Oracle.

**Query:**
```sql
-- Oracle
CREATE OR REPLACE TRIGGER trg_salary_change
AFTER UPDATE OF salary ON employees
FOR EACH ROW
BEGIN
    IF :OLD.salary != :NEW.salary THEN
        INSERT INTO salary_audit (emp_id, old_salary, new_salary, changed_at)
        VALUES (:OLD.emp_id, :OLD.salary, :NEW.salary, SYSDATE);
    END IF;
END;
/
```
**Explanation:** `UPDATE OF salary` ensures the trigger fires only when the `salary` column is part of the SET clause. The `:OLD` and `:NEW` bind variables access pre- and post-update values.

---

## Q17: Log all DDL schema changes (CREATE, ALTER, DROP) in SQL Server using a database-level trigger.

**Query:**
```sql
-- SQL Server
CREATE TRIGGER trg_ddl_audit
ON DATABASE
FOR CREATE_TABLE, ALTER_TABLE, DROP_TABLE
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO ddl_audit_log (event_type, object_name, tsql_command, login_name, event_time)
    VALUES (
        EVENTDATA().value('(/EVENT_INSTANCE/EventType)[1]', 'NVARCHAR(128)'),
        EVENTDATA().value('(/EVENT_INSTANCE/ObjectName)[1]', 'NVARCHAR(128)'),
        EVENTDATA().value('(/EVENT_INSTANCE/TSQLCommand/CommandText)[1]', 'NVARCHAR(MAX)'),
        ORIGINAL_LOGIN(),
        GETDATE()
    );
END;
```
**Explanation:** A DDL trigger on `DATABASE` captures schema events. `EVENTDATA()` is an XML function returning details about the DDL operation.

---

## Q18: Log DDL changes in Oracle using a SYSTEM-level trigger.

**Query:**
```sql
-- Oracle
CREATE TABLE ddl_audit_log (
    log_id     NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    event_type VARCHAR2(30),
    object_owner VARCHAR2(30),
    object_name VARCHAR2(128),
    event_time TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE OR REPLACE TRIGGER trg_ddl_audit
AFTER DDL ON SCHEMA
BEGIN
    INSERT INTO ddl_audit_log (event_type, object_owner, object_name, event_time)
    VALUES (ORA_SYSEVENT, ORA_DICT_OBJ_OWNER, ORA_DICT_OBJ_NAME, SYSTIMESTAMP);
END;
/
```
**Explanation:** Oracle fires DDL triggers at the schema or database level. `ORA_SYSEVENT` and `ORA_DICT_OBJ_NAME` provide event metadata.

---

## Q19: Write a trigger that validates email format before INSERT in MySQL.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_validate_email
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    IF NEW.email NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid email format';
    END IF;
END //
DELIMITER ;
```
**Explanation:** The `REGEXP` operator tests the email against a standard pattern. A failed check raises an error and prevents the insert.

**Alt1:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_validate_email() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RAISE EXCEPTION 'Invalid email format';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_email
BEFORE INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION fn_validate_email();
```
**Explanation:** PostgreSQL uses the `!~` operator for a regex negative match inside a PL/pgSQL trigger function.

---

## Q20: Write a trigger that prevents DELETE on employees who are managers in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_block_manager_delete() RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM employees WHERE manager_id = OLD.emp_id) THEN
        RAISE EXCEPTION 'Cannot delete an employee who is a manager';
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_block_manager_delete
BEFORE DELETE ON employees
FOR EACH ROW
EXECUTE FUNCTION fn_block_manager_delete();
```
**Explanation:** The trigger checks for subordinates before allowing the delete. If the employee manages anyone, the delete is rejected.

**Alt1:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_block_manager_delete
BEFORE DELETE ON employees
FOR EACH ROW
BEGIN
    DECLARE cnt INT;
    SELECT COUNT(*) INTO cnt FROM employees WHERE manager_id = OLD.emp_id;
    IF cnt > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete an employee who is a manager';
    END IF;
END //
DELIMITER ;
```
**Explanation:** MySQL requires a slightly different syntax using DECLARE and SIGNAL for the same logic.

---

## Q21: Demonstrate OLD and NEW pseudo-rows in a MySQL BEFORE UPDATE trigger that normalizes a name.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_normalize_name
BEFORE UPDATE ON employees
FOR EACH ROW
BEGIN
    SET NEW.name = TRIM(CONCAT(
        UPPER(LEFT(NEW.name, 1)),
        LOWER(SUBSTRING(NEW.name, 2))
    ));
END //
DELIMITER ;
```
**Explanation:** `NEW.name` is read/write in a BEFORE trigger — the trigger modifies it so the stored value is always title-cased. `OLD.name` would hold the original.

---

## Q22: Access the `inserted` and `deleted` tables in SQL Server to compare old and new department values.

**Query:**
```sql
-- SQL Server
CREATE TRIGGER trg_dept_change
ON employees
AFTER UPDATE
AS
BEGIN
    INSERT INTO dept_change_log (emp_id, old_dept, new_dept, changed_at)
    SELECT d.emp_id, d.dept_id, i.dept_id, GETDATE()
    FROM deleted d
    JOIN inserted i ON d.emp_id = i.emp_id
    WHERE d.dept_id <> i.dept_id;
END;
```
**Explanation:** In SQL Server, `deleted` holds pre-update rows and `inserted` holds post-update rows. The JOIN on the primary key lets you compare column-by-column.

---

## Q23: Show how `:OLD` and `:NEW` work in an Oracle BEFORE DELETE trigger.

**Query:**
```sql
-- Oracle
CREATE OR REPLACE TRIGGER trg_before_delete
BEFORE DELETE ON employees
FOR EACH ROW
BEGIN
    INSERT INTO delete_log (emp_id, name, dept_id, deleted_by, deleted_at)
    VALUES (:OLD.emp_id, :OLD.name, :OLD.dept_id, USER, SYSDATE);
END;
/
```
**Explanation:** In Oracle, `:OLD` contains the existing row values being deleted. `:NEW` is NULL for DELETE operations. The trigger logs the row before removal.

---

## Q24: Create a recursive trigger in SQL Server that fires when the audit table itself is updated.

**Query:**
```sql
-- SQL Server
-- Step 1: Enable recursive triggers at the database level
ALTER DATABASE mydb SET RECURSIVE_TRIGGERS ON;

-- Step 2: Create the trigger
CREATE TRIGGER trg_audit_recursive
ON employee_audit
AFTER UPDATE
AS
BEGIN
    INSERT INTO meta_audit (source_table, action, fired_at)
    VALUES ('employee_audit', 'UPDATE', GETDATE());
END;
```
**Explanation:** Recursive triggers allow a trigger to fire another trigger on the same table. This is off by default in SQL Server for safety.

---

## Q25: Disable a trigger in SQL Server and then re-enable it.

**Query:**
```sql
-- SQL Server
DISABLE TRIGGER trg_salary_change ON employees;
-- Perform a bulk update without audit logging
UPDATE employees SET salary = salary * 1.05;
ENABLE TRIGGER trg_salary_change ON employees;
```
**Explanation:** `DISABLE TRIGGER` suppresses the trigger for the duration of maintenance operations. `ENABLE TRIGGER` restores it.

**Alt1:**
```sql
-- MySQL
ALTER TABLE employees DISABLE TRIGGER trg_salary_change;
-- perform bulk work
ALTER TABLE employees ENABLE TRIGGER trg_salary_change;
```
**Explanation:** MySQL (8.0+) supports `DISABLE/ENABLE TRIGGER` syntax directly on the table.


## Q26: Disable and re-enable a trigger in Oracle.

**Query:**
```sql
-- Oracle
ALTER TRIGGER trg_salary_change DISABLE;
-- Bulk update without audit
UPDATE employees SET salary = salary * 1.05;
ALTER TRIGGER trg_salary_change ENABLE;
```
**Explanation:** Oracle uses `ALTER TRIGGER ... DISABLE/ENABLE` at the individual trigger level.

---

## Q27: Disable all triggers on a table in MySQL with a single statement.

**Query:**
```sql
-- MySQL 8.0+
ALTER TABLE employees DISABLE TRIGGER ALL;
-- Bulk operations here
ALTER TABLE employees ENABLE TRIGGER ALL;
```
**Explanation:** `DISABLE TRIGGER ALL` turns off every trigger on the table at once, useful during large data loads.

---

## Q28: Drop a trigger in MySQL, PostgreSQL, SQL Server, and Oracle.

**Query:**
```sql
-- MySQL
DROP TRIGGER IF EXISTS trg_salary_change;

-- PostgreSQL
DROP TRIGGER IF EXISTS trg_salary_change ON employees;

-- SQL Server
DROP TRIGGER IF EXISTS trg_salary_change;

-- Oracle
DROP TRIGGER trg_salary_change;
```
**Explanation:** MySQL and SQL Server drop by trigger name. PostgreSQL requires the table name. Oracle has no `IF EXISTS` so handle the error externally.

---

## Q29: Demonstrate a BEFORE INSERT trigger that sets a UUID when the application forgets to provide one.

**Query:**
```sql
-- MySQL 8.0+
DELIMITER //
CREATE TRIGGER trg_auto_uuid
BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
    IF NEW.order_uuid IS NULL THEN
        SET NEW.order_uuid = UUID_TO_BIN(UUID(), TRUE);
    END IF;
END //
DELIMITER ;
```
**Explanation:** The trigger fills in a UUID only when the column is NULL, so the application can still supply its own if desired.

**Alt1:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_auto_uuid() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.order_uuid IS NULL THEN
        NEW.order_uuid = gen_random_uuid();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_auto_uuid
BEFORE INSERT ON orders
FOR EACH ROW
EXECUTE FUNCTION fn_auto_uuid();
```
**Explanation:** PostgreSQL's `gen_random_uuid()` generates a v4 UUID natively without extensions.

---

## Q30: Write a trigger that prevents circular references in a self-referencing table (e.g., employees.manager_id).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_prevent_circular
BEFORE UPDATE ON employees
FOR EACH ROW
BEGIN
    DECLARE current_id INT;
    DECLARE mgr_id    INT;
    SET current_id = NEW.emp_id;
    SET mgr_id    = NEW.manager_id;

    WHILE mgr_id IS NOT NULL DO
        IF mgr_id = current_id THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Circular manager reference detected';
        END IF;
        SELECT manager_id INTO mgr_id
        FROM employees WHERE emp_id = mgr_id;
    END WHILE;
END //
DELIMITER ;
```
**Explanation:** The trigger walks up the management chain and aborts if it encounters the employee's own ID, preventing cycles.

---

## Q31: Use a trigger to automatically assign a default value for `created_at` on INSERT.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_set_created_at() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.created_at IS NULL THEN
        NEW.created_at = NOW();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_set_created_at
BEFORE INSERT ON audit_log
FOR EACH ROW
EXECUTE FUNCTION fn_set_created_at();
```
**Explanation:** While `DEFAULT CURRENT_TIMESTAMP` is preferred, a trigger guarantees the value is set even if the column has no default in the schema.

---

## Q32: Write a trigger that cascades a soft-delete flag from a parent table to its children.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_soft_delete_cascade
AFTER UPDATE ON departments
FOR EACH ROW
BEGIN
    IF OLD.is_active = TRUE AND NEW.is_active = FALSE THEN
        UPDATE employees
        SET    is_active = FALSE
        WHERE  dept_id = NEW.dept_id AND is_active = TRUE;
    END IF;
END //
DELIMITER ;
```
**Explanation:** When a department is deactivated, the trigger deactivates all active employees in that department in one go.

---

## Q33: Show how a trigger interacts with a transaction — roll back the whole statement when validation fails.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_salary_cap
BEFORE INSERT ON employees
FOR EACH ROW
BEGIN
    IF NEW.salary > 500000 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Salary exceeds cap';
    END IF;
END //
DELIMITER ;

-- This entire multi-row insert rolls back if even one row violates the cap
INSERT INTO employees (name, salary) VALUES
    ('Alice', 80000),
    ('Bob',   600000),  -- triggers error
    ('Carol', 90000);   -- never inserted either
```
**Explanation:** A trigger error rolls back the entire triggering statement, not just the offending row. All rows in the INSERT are undone.

**Alt1:**
```sql
-- SQL Server
CREATE TRIGGER trg_salary_cap
ON employees
INSTEAD OF INSERT
AS
BEGIN
    IF EXISTS (SELECT 1 FROM inserted WHERE salary > 500000)
    BEGIN
        RAISERROR ('Salary exceeds cap', 16, 1);
        RETURN;
    END
    INSERT INTO employees (name, salary)
    SELECT name, salary FROM inserted;
END;
```
**Explanation:** With `INSTEAD OF`, you can reject the entire batch or selectively insert valid rows, giving you finer control.

---

## Q34: Write a trigger that rejects deletes on a table during business hours (9 AM – 6 PM).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_block_business_hours_delete
BEFORE DELETE ON orders
FOR EACH ROW
BEGIN
    IF HOUR(NOW()) BETWEEN 9 AND 17 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Deletion blocked during business hours';
    END IF;
END //
DELIMITER ;
```
**Explanation:** The trigger checks the current hour and rejects the delete if it falls within business hours. This protects data during working time.

---

## Q35: Create a trigger that logs every failed login attempt by using an INSTEAD OF trigger on a security view.

**Query:**
```sql
-- SQL Server
CREATE VIEW v_login_attempts AS
SELECT user_id, attempt_time FROM login_log;

CREATE TRIGGER trg_log_login
ON v_login_attempts
INSTEAD OF INSERT
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO login_log (user_id, attempt_time)
    SELECT user_id, attempt_time FROM inserted;

    DECLARE @fail_count INT;
    SELECT @fail_count = COUNT(*)
    FROM login_log
    WHERE user_id = (SELECT user_id FROM inserted)
      AND attempt_time >= DATEADD(MINUTE, -15, GETDATE());

    IF @fail_count >= 5
    BEGIN
        UPDATE users SET is_locked = 1
        WHERE user_id = (SELECT user_id FROM inserted);
    END
END;
```
**Explanation:** The INSTEAD OF trigger wraps the insert with additional logic to count recent failures and lock the account if the threshold is exceeded.

---

## Q36: Demonstrate nested triggers — INSERT into a table whose trigger INSERTs into another triggered table.

**Query:**
```sql
-- SQL Server
-- Trigger on orders inserts into order_items_audit
CREATE TRIGGER trg_orders_audit
ON orders
AFTER INSERT
AS
BEGIN
    INSERT INTO order_items_audit (order_id, product_id, qty, logged_at)
    SELECT oi.order_id, oi.product_id, oi.quantity, GETDATE()
    FROM inserted i
    JOIN order_items oi ON i.order_id = oi.order_id;
END;

-- Trigger on order_items_audit inserts into meta_audit
CREATE TRIGGER trg_order_items_meta
ON order_items_audit
AFTER INSERT
AS
BEGIN
    INSERT INTO meta_audit (source_table, action, fired_at)
    VALUES ('order_items_audit', 'INSERT', GETDATE());
END;
```
**Explanation:** A row inserted by the first trigger causes the second trigger to fire. Nested triggers are enabled by default but can be turned off with `sp_configure`.

---

## Q37: Show the difference between FOR EACH ROW and FOR EACH STATEMENT in PostgreSQL with a practical example.

**Query:**
```sql
-- PostgreSQL
-- Statement-level trigger: logs once per INSERT
CREATE OR REPLACE FUNCTION fn_statement_log() RETURNS TRIGGER AS $$
BEGIN
    RAISE NOTICE 'Statement-level trigger fired at %', NOW();
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_statement
AFTER INSERT ON employees
FOR EACH STATEMENT
EXECUTE FUNCTION fn_statement_log();

-- Row-level trigger: logs once per row
CREATE OR REPLACE FUNCTION fn_row_log() RETURNS TRIGGER AS $$
BEGIN
    RAISE NOTICE 'Row-level trigger fired for emp_id=%', NEW.emp_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_row
AFTER INSERT ON employees
FOR EACH ROW
EXECUTE FUNCTION fn_row_log();

-- Running this:
INSERT INTO employees (name, dept_id) VALUES
    ('Alice', 1), ('Bob', 2), ('Carol', 1);
-- Statement trigger fires once; Row trigger fires three times.
```
**Explanation:** `FOR EACH STATEMENT` fires once regardless of row count; `FOR EACH ROW` fires for every individual row affected.

---

## Q38: Prevent a table from being dropped using a DDL trigger in SQL Server.

**Query:**
```sql
-- SQL Server
CREATE TRIGGER trg_block_drop
ON DATABASE
FOR DROP_TABLE
AS
BEGIN
    DECLARE @obj NVARCHAR(128) = EVENTDATA().value('(/EVENT_INSTANCE/ObjectName)[1]', 'NVARCHAR(128)');
    IF @obj IN ('employees', 'orders', 'customers')
    BEGIN
        RAISERROR ('Cannot drop critical table %s', 16, 1, @obj);
        ROLLBACK;
    END;
END;
```
**Explanation:** The DDL trigger inspects the object name from EVENTDATA and issues a ROLLBACK to abort the DROP if it targets a protected table.

---

## Q39: Write a trigger that validates a CHECK constraint programmatically (e.g., end_date must be after start_date).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_validate_dates
BEFORE INSERT ON contracts
FOR EACH ROW
BEGIN
    IF NEW.end_date <= NEW.start_date THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'end_date must be after start_date';
    END IF;
END //
DELIMITER ;
```
**Explanation:** The trigger compares the two date columns and rejects the row if the logic is violated, providing a descriptive error message.

**Alt1:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_validate_dates() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.end_date <= NEW.start_date THEN
        RAISE EXCEPTION 'end_date must be after start_date';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_dates
BEFORE INSERT ON contracts
FOR EACH ROW
EXECUTE FUNCTION fn_validate_dates();
```
**Explanation:** Same logic with PostgreSQL syntax; the function returns the modified NEW row to allow the insert.

---

## Q40: Use a trigger to maintain a materialized/summary count of active users per role.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_update_role_count_insert
AFTER INSERT ON users
FOR EACH ROW
BEGIN
    INSERT INTO role_user_count (role_id, active_count)
    VALUES (NEW.role_id, 1)
    ON DUPLICATE KEY UPDATE active_count = active_count + 1;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_update_role_count_delete
AFTER DELETE ON users
FOR EACH ROW
BEGIN
    UPDATE role_user_count
    SET    active_count = active_count - 1
    WHERE  role_id = OLD.role_id;
END //
DELIMITER ;
```
**Explanation:** Two triggers (INSERT and DELETE) keep the summary count in sync. `ON DUPLICATE KEY UPDATE` handles first-row creation.

---

## Q41: Write a trigger that rejects INSERTs if the referenced foreign key row does not exist, even when the FK constraint is disabled.

**Query:**
```sql
-- SQL Server
CREATE TRIGGER trg_validate_fk
ON order_items
INSTEAD OF INSERT
AS
BEGIN
    IF EXISTS (
        SELECT 1 FROM inserted i
        LEFT JOIN products p ON i.product_id = p.product_id
        WHERE p.product_id IS NULL
    )
    BEGIN
        RAISERROR ('Referenced product does not exist', 16, 1);
        RETURN;
    END
    INSERT INTO order_items (order_id, product_id, quantity)
    SELECT order_id, product_id, quantity FROM inserted;
END;
```
**Explanation:** When FK constraints are intentionally disabled for performance, the trigger enforces referential integrity manually.

---

## Q42: Create a trigger that automatically generates an audit hash for change detection (row fingerprinting).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_compute_hash
BEFORE UPDATE ON products
FOR EACH ROW
BEGIN
    SET NEW.row_hash = SHA2(CONCAT(
        IFNULL(NEW.product_name, ''),
        IFNULL(NEW.price, ''),
        IFNULL(NEW.stock, '')
    ), 256);
END //
DELIMITER ;
```
**Explanation:** The trigger recomputes a SHA-256 hash of the row's key columns on every update, enabling downstream consumers to detect changes by comparing hashes.

---

## Q43: Write a trigger that prevents duplicate inserts based on a composite unique key at the application level (when the DB index is deferred).

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_block_duplicate_assignment() RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM student_courses
        WHERE student_id = NEW.student_id
          AND course_id  = NEW.course_id
          AND id <> NEW.id
    ) THEN
        RAISE EXCEPTION 'Student is already enrolled in this course';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_block_duplicate
BEFORE INSERT OR UPDATE ON student_courses
FOR EACH ROW
EXECUTE FUNCTION fn_block_duplicate_assignment();
```
**Explanation:** The trigger checks for an existing matching row and raises an exception if a duplicate is found, acting as an application-level constraint.

---

## Q44: Use a trigger to track who modified a row and when, by writing a composite audit record.

**Query:**
```sql
-- SQL Server
CREATE TRIGGER trg_who_modified
ON employees
AFTER UPDATE
AS
BEGIN
    INSERT INTO change_history (emp_id, column_name, old_value, new_value, modified_by, modified_at)
    SELECT d.emp_id, 'salary', CAST(d.salary AS VARCHAR), CAST(i.salary AS VARCHAR), SYSTEM_USER, GETDATE()
    FROM deleted d
    JOIN inserted i ON d.emp_id = i.emp_id
    WHERE d.salary <> i.salary
    UNION ALL
    SELECT d.emp_id, 'dept_id', CAST(d.dept_id AS VARCHAR), CAST(i.dept_id AS VARCHAR), SYSTEM_USER, GETDATE()
    FROM deleted d
    JOIN inserted i ON d.emp_id = i.emp_id
    WHERE d.dept_id <> i.dept_id;
END;
```
**Explanation:** The trigger compares old and new values column by column and writes one audit row per changed column, tagging it with the login name.

---

## Q45: Write a trigger that prevents INSERT if the current user is not in an allowed list.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_allowed_user_check() RETURNS TRIGGER AS $$
BEGIN
    IF CURRENT_USER NOT IN ('app_admin', 'etl_service') THEN
        RAISE EXCEPTION 'User % is not allowed to insert into this table', CURRENT_USER;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_allowed_user
BEFORE INSERT ON sensitive_data
FOR EACH ROW
EXECUTE FUNCTION fn_allowed_user_check();
```
**Explanation:** The trigger inspects `CURRENT_USER` and rejects the operation if the caller is not authorized, acting as a database-level guard.

**Alt1:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_allowed_user
BEFORE INSERT ON sensitive_data
FOR EACH ROW
BEGIN
    IF CURRENT_USER() NOT IN ('app_admin', 'etl_service') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Unauthorized user';
    END IF;
END //
DELIMITER ;
```
**Explanation:** MySQL uses `CURRENT_USER()` function instead of `CURRENT_USER`.

---

## Q46: Demonstrate trigger execution order: two BEFORE triggers on the same table in MySQL.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_before_a
BEFORE INSERT ON employees
FOR EACH ROW
BEGIN
    SET NEW.name = TRIM(NEW.name);
    -- Log that trigger A fired first
    INSERT INTO trigger_log (trigger_name) VALUES ('before_a');
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_before_b
BEFORE INSERT ON employees
FOR EACH ROW
BEGIN
    SET NEW.name = UPPER(NEW.name);
    INSERT INTO trigger_log (trigger_name) VALUES ('before_b');
END //
DELIMITER ;
```
**Explanation:** MySQL fires BEFORE triggers in creation order. Trigger A trims first, then trigger B uppercases the result. The log confirms the sequence.

---

## Q47: Demonstrate trigger execution order: AFTER triggers fire in creation order in SQL Server.

**Query:**
```sql
-- SQL Server
CREATE TRIGGER trg_after_a
ON employees
AFTER INSERT
AS
BEGIN
    INSERT INTO trigger_log (trigger_name, fired_at) VALUES ('after_a', GETDATE());
END;

CREATE TRIGGER trg_after_b
ON employees
AFTER INSERT
AS
BEGIN
    INSERT INTO trigger_log (trigger_name, fired_at) VALUES ('after_b', GETDATE());
END;

-- Execution order: after_a fires first, then after_b.
-- To change order, use sp_settriggerorder:
EXEC sp_settriggerorder @triggername = 'trg_after_b', @statementorder = 'First', @orderid = 0;
```
**Explanation:** SQL Server fires AFTER triggers in creation order by default. `sp_settriggerorder` can explicitly set First, Last, or None.

---

## Q48: Use `sp_settriggerorder` in SQL Server to make a specific trigger fire first.

**Query:**
```sql
-- SQL Server
EXEC sp_settriggerorder
    @triggername = 'trg_after_b',
    @statementorder = 'First',
    @orderid = 0;
```
**Explanation:** This system procedure overrides the default creation-order firing for AFTER triggers. Only one trigger can be First and one Last per event.

---

## Q49: Write a trigger that prevents UPDATE if the row was already modified by another user (optimistic locking check).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_optimistic_lock
BEFORE UPDATE ON documents
FOR EACH ROW
BEGIN
    IF OLD.version <> NEW.version THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Row was modified by another user; refresh and retry';
    END IF;
    SET NEW.version = OLD.version + 1;
END //
DELIMITER ;
```
**Explanation:** The trigger checks that the version number matches (the app must pass the original version). If it matches, the version is incremented. If not, the update is rejected.

---

## Q50: Write a trigger that auto-generates a human-readable document number (e.g., DOC-2026-00001).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_doc_number
BEFORE INSERT ON documents
FOR EACH ROW
BEGIN
    DECLARE seq INT;
    SELECT COALESCE(MAX(seq_num), 0) + 1 INTO seq
    FROM documents
    WHERE doc_year = YEAR(NOW());

    SET NEW.doc_number = CONCAT('DOC-', YEAR(NOW()), '-', LPAD(seq, 5, '0'));
    SET NEW.doc_year   = YEAR(NOW());
END //
DELIMITER ;
```
**Explanation:** The trigger computes the next sequence number for the current year and formats it into a padded document number string.


## Q51: Write a trigger that syncs a denormalized `total_items` and `order_total` in an orders table when order_items are modified.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_sync_order_totals_insert
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE orders
    SET    total_items = (SELECT COALESCE(SUM(quantity), 0) FROM order_items WHERE order_id = NEW.order_id),
           order_total = (SELECT COALESCE(SUM(quantity * unit_price), 0) FROM order_items WHERE order_id = NEW.order_id)
    WHERE  order_id = NEW.order_id;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_sync_order_totals_delete
AFTER DELETE ON order_items
FOR EACH ROW
BEGIN
    UPDATE orders
    SET    total_items = (SELECT COALESCE(SUM(quantity), 0) FROM order_items WHERE order_id = OLD.order_id),
           order_total = (SELECT COALESCE(SUM(quantity * unit_price), 0) FROM order_items WHERE order_id = OLD.order_id)
    WHERE  order_id = OLD.order_id;
END //
DELIMITER ;
```
**Explanation:** Separate INSERT and DELETE triggers recompute totals from order_items whenever the line items change.

**Alt1:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_sync_order_totals() RETURNS TRIGGER AS $$
DECLARE
    target_order INT;
BEGIN
    target_order := COALESCE(NEW.order_id, OLD.order_id);
    UPDATE orders
    SET    total_items = (SELECT COALESCE(SUM(quantity), 0) FROM order_items WHERE order_id = target_order),
           order_total = (SELECT COALESCE(SUM(quantity * unit_price), 0) FROM order_items WHERE order_id = target_order)
    WHERE  order_id = target_order;
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_sync_order_totals
AFTER INSERT OR DELETE ON order_items
FOR EACH ROW
EXECUTE FUNCTION fn_sync_order_totals();
```
**Explanation:** PostgreSQL supports a single trigger function for multiple events (`INSERT OR DELETE`), reducing code duplication.

---

## Q52: Write a trigger that automatically creates a user profile row when a new user signs up.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_create_profile
AFTER INSERT ON users
FOR EACH ROW
BEGIN
    INSERT INTO user_profiles (user_id, display_name, bio, created_at)
    VALUES (NEW.user_id, NEW.username, 'New member', NOW());
END //
DELIMITER ;
```
**Explanation:** The trigger ensures every user always has a corresponding profile row, enforcing a one-to-one relationship that application code might forget.

---

## Q53: Use a trigger to enforce a maximum number of rows per group (e.g., max 3 projects per department).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_max_projects
BEFORE INSERT ON projects
FOR EACH ROW
BEGIN
    DECLARE cnt INT;
    SELECT COUNT(*) INTO cnt FROM projects WHERE dept_id = NEW.dept_id;
    IF cnt >= 3 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Department cannot have more than 3 projects';
    END IF;
END //
DELIMITER ;
```
**Explanation:** The trigger counts existing projects in the department and blocks the insert if the limit is reached.

---

## Q54: Write a trigger that rejects UPDATE if a critical column was changed (e.g., order_status from 'completed' to 'pending').

**Query:**
```sql
-- SQL Server
CREATE TRIGGER trg_block_status_regression
ON orders
AFTER UPDATE
AS
BEGIN
    IF EXISTS (
        SELECT 1 FROM deleted d
        JOIN inserted i ON d.order_id = i.order_id
        WHERE d.order_status = 'completed' AND i.order_status = 'pending'
    )
    BEGIN
        RAISERROR ('Cannot revert a completed order to pending', 16, 1);
        ROLLBACK;
    END;
END;
```
**Explanation:** The trigger compares old and new status values and rolls back the statement if a status regression is detected.

**Alt1:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_block_status_regression
BEFORE UPDATE ON orders
FOR EACH ROW
BEGIN
    IF OLD.order_status = 'completed' AND NEW.order_status = 'pending' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot revert a completed order to pending';
    END IF;
END //
DELIMITER ;
```
**Explanation:** MySQL uses `BEFORE UPDATE` with `OLD`/`NEW` pseudo-rows and `SIGNAL` instead of SQL Server's `deleted`/`inserted` tables.

---

## Q55: Create a trigger that writes a full historical snapshot of a row on every UPDATE (slowly changing dimension Type 2).

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_scd2_snapshot() RETURNS TRIGGER AS $$
BEGIN
    UPDATE customer_history
    SET    valid_to = NOW()
    WHERE  customer_id = OLD.customer_id AND valid_to IS NULL;

    INSERT INTO customer_history (customer_id, name, email, address, valid_from, valid_to)
    VALUES (OLD.customer_id, OLD.name, OLD.email, OLD.address, NOW(), NULL);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_scd2
AFTER UPDATE ON customers
FOR EACH ROW
EXECUTE FUNCTION fn_scd2_snapshot();
```
**Explanation:** On UPDATE, the trigger closes the current history row (sets valid_to) and inserts a new open row. This creates a full audit trail of all historical values.

---

## Q56: Write a trigger that prevents a user from modifying their own privileges (self-escalation prevention).

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_block_self_privilege_change() RETURNS TRIGGER AS $$
BEGIN
    IF OLD.role_id <> NEW.role_id AND current_user = OLD.username THEN
        RAISE EXCEPTION 'Users cannot modify their own role';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_block_self_privilege
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION fn_block_self_privilege_change();
```
**Explanation:** The trigger compares the `current_user` to the row being modified and blocks role changes on the caller's own account.

---

## Q57: Use a trigger to maintain a last_updated_by column with the database session user.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_set_updated_by
BEFORE UPDATE ON orders
FOR EACH ROW
BEGIN
    SET NEW.updated_by = CURRENT_USER();
END //
DELIMITER ;
```
**Explanation:** `CURRENT_USER()` returns the authenticated MySQL user. The trigger stamps every update with who made the change.

**Alt1:**
```sql
-- SQL Server
CREATE TRIGGER trg_set_updated_by
ON orders
AFTER UPDATE
AS
BEGIN
    UPDATE o
    SET    updated_by = SYSTEM_USER
    FROM   orders o
    JOIN   inserted i ON o.order_id = i.order_id;
END;
```
**Explanation:** SQL Server triggers are AFTER by default for non-INSTEAD-OF, so the value is written back in a post-update step.

---

## Q58: Create a trigger that enforces referential integrity for a polymorphic association (no FK constraint possible).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_validate_polymorphic
BEFORE INSERT ON comments
FOR EACH ROW
BEGIN
    IF NEW.commentable_type = 'post' THEN
        IF NOT EXISTS (SELECT 1 FROM posts WHERE post_id = NEW.commentable_id) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Referenced post does not exist';
        END IF;
    ELSEIF NEW.commentable_type = 'photo' THEN
        IF NOT EXISTS (SELECT 1 FROM photos WHERE photo_id = NEW.commentable_id) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Referenced photo does not exist';
        END IF;
    END IF;
END //
DELIMITER ;
```
**Explanation:** Polymorphic associations cannot use foreign keys. The trigger checks the type and validates existence in the correct table.

---

## Q59: Write a trigger that auto-generates a slug from a title column before INSERT.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_auto_slug() RETURNS TRIGGER AS $$
BEGIN
    NEW.slug := LOWER(REGEXP_REPLACE(TRIM(NEW.title), '[^a-zA-Z0-9]+', '-', 'g'));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_auto_slug
BEFORE INSERT ON articles
FOR EACH ROW
EXECUTE FUNCTION fn_auto_slug();
```
**Explanation:** The function strips non-alphanumeric characters, replaces them with hyphens, lowercases the result, and stores it in `slug`.

**Alt1:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_auto_slug
BEFORE INSERT ON articles
FOR EACH ROW
BEGIN
    SET NEW.slug = LOWER(REPLACE(TRIM(NEW.title), ' ', '-'));
END //
DELIMITER ;
```
**Explanation:** MySQL's simpler version replaces spaces with hyphens; a regex-based version would require `REGEXP_REPLACE` (MySQL 8.0+).

---

## Q60: Write a trigger that prevents deletion of records that are older than 7 years (data retention policy).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_retention_policy
BEFORE DELETE ON financial_records
FOR EACH ROW
BEGIN
    IF OLD.record_date < DATE_SUB(CURDATE(), INTERVAL 7 YEAR) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Records older than 7 years cannot be deleted via application';
    END IF;
END //
DELIMITER ;
```
**Explanation:** The trigger enforces a data retention policy at the database level. Archives older than 7 years can only be purged by an admin with the trigger disabled.

---

## Q61: Use a trigger to implement a "moving average" cache updated on every INSERT.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_moving_avg
AFTER INSERT ON daily_sales
FOR EACH ROW
BEGIN
    DECLARE avg_val DECIMAL(10,2);
    SELECT AVG(amount) INTO avg_val
    FROM daily_sales
    WHERE sale_date >= DATE_SUB(NEW.sale_date, INTERVAL 30 DAY);

    INSERT INTO sales_metrics (metric_date, moving_avg_30d)
    VALUES (NEW.sale_date, avg_val)
    ON DUPLICATE KEY UPDATE moving_avg_30d = avg_val;
END //
DELIMITER ;
```
**Explanation:** Each new sale triggers a recalculation of the 30-day moving average, which is upserted into a metrics summary table.

---

## Q62: Write a trigger that logs both the user and the application name when a row is modified in SQL Server.

**Query:**
```sql
-- SQL Server
CREATE TRIGGER trg_who_and_what
ON employees
AFTER UPDATE
AS
BEGIN
    INSERT INTO audit_trail (emp_id, old_salary, new_salary, db_user, app_name, fired_at)
    SELECT d.emp_id, d.salary, i.salary, SYSTEM_USER, APP_NAME(), GETDATE()
    FROM deleted d
    JOIN inserted i ON d.emp_id = i.emp_id
    WHERE d.salary <> i.salary;
END;
```
**Explanation:** `SYSTEM_USER` returns the database login, `APP_NAME()` returns the client application name (set via `SET APP_NAME = 'xxx'`), providing full traceability.

---

## Q63: Write a trigger that enforces a maximum salary increase percentage per UPDATE.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_salary_increase_cap
BEFORE UPDATE ON employees
FOR EACH ROW
BEGIN
    DECLARE pct DECIMAL(5,2);
    IF OLD.salary > 0 AND NEW.salary > OLD.salary THEN
        SET pct = ((NEW.salary - OLD.salary) / OLD.salary) * 100;
        IF pct > 20 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Salary increase cannot exceed 20%';
        END IF;
    END IF;
END //
DELIMITER ;
```
**Explanation:** The trigger calculates the percentage increase and rejects the update if it exceeds the 20% cap, enforcing a business rule.

---

## Q64: Use a trigger to keep an Elasticsearch-compatible JSON column synchronized with relational columns.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_sync_search_json() RETURNS TRIGGER AS $$
BEGIN
    NEW.search_payload := jsonb_build_object(
        'id',      NEW.product_id,
        'name',    NEW.product_name,
        'price',   NEW.price,
        'category', NEW.category_name,
        'in_stock', NEW.stock > 0,
        'updated', NOW()
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_sync_search_json
BEFORE INSERT OR UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION fn_sync_search_json();
```
**Explanation:** The trigger builds a JSONB document from the row's columns on every write, keeping the search payload always current.

---

## Q65: Write a trigger that prevents circular department hierarchies by walking the tree on INSERT.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_prevent_dept_cycle() RETURNS TRIGGER AS $$
DECLARE
    current_parent INT;
BEGIN
    current_parent := NEW.parent_dept_id;
    WHILE current_parent IS NOT NULL LOOP
        IF current_parent = NEW.dept_id THEN
            RAISE EXCEPTION 'Circular department hierarchy detected';
        END IF;
        SELECT parent_dept_id INTO current_parent
        FROM departments WHERE dept_id = current_parent;
    END LOOP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_dept_cycle
BEFORE INSERT OR UPDATE ON departments
FOR EACH ROW
EXECUTE FUNCTION fn_prevent_dept_cycle();
```
**Explanation:** The trigger traverses the parent chain and aborts if it loops back to the inserting department's own ID.

---

## Q66: Use a trigger to implement row-level security beyond what native RLS provides (e.g., date-based access).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_future_records_blocked
BEFORE INSERT ON exams
FOR EACH ROW
BEGIN
    IF NEW.exam_date > DATE_ADD(CURDATE(), INTERVAL 30 DAY) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot schedule exams more than 30 days in advance';
    END IF;
END //
DELIMITER ;
```
**Explanation:** The trigger enforces a business rule that limits how far in the future records can be created, acting as temporal access control.

---

## Q67: Write a trigger that merges duplicate rows when an INSERT would create a duplicate based on a fuzzy match.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_fuzzy_dedup() RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM contacts
        WHERE SOUNDEX(name) = SOUNDEX(NEW.name)
          AND email = NEW.email
    ) THEN
        RAISE NOTICE 'Duplicate contact detected — skipping insert';
        RETURN NULL;  -- skip the insert
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_fuzzy_dedup
BEFORE INSERT ON contacts
FOR EACH ROW
EXECUTE FUNCTION fn_fuzzy_dedup();
```
**Explanation:** Returning NULL from a BEFORE trigger in PostgreSQL silently skips the insert. The trigger uses `SOUNDEX` for approximate name matching.

---

## Q68: Create a trigger that logs every TRUNCATE operation in Oracle.

**Query:**
```sql
-- Oracle
CREATE OR REPLACE TRIGGER trg_truncate_log
BEFORE TRUNCATE ON SCHEMA
BEGIN
    INSERT INTO ddl_audit_log (event_type, object_name, event_time)
    VALUES ('TRUNCATE', ORA_DICT_OBJ_NAME, SYSTIMESTAMP);
END;
/
```
**Explanation:** Oracle fires `BEFORE TRUNCATE` or `AFTER TRUNCATE` at the schema level. `ORA_DICT_OBJ_NAME` provides the table name being truncated.

---

## Q69: Write a trigger that auto-creates database partition-like buckets by inserting into a monthly summary table.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_monthly_bucket
AFTER INSERT ON events
FOR EACH ROW
BEGIN
    INSERT INTO monthly_event_summary (event_year, event_month, event_count)
    VALUES (YEAR(NEW.event_time), MONTH(NEW.event_time), 1)
    ON DUPLICATE KEY UPDATE event_count = event_count + 1;
END //
DELIMITER ;
```
**Explanation:** Every new event triggers an upsert into a monthly bucket, maintaining a lightweight partition summary without actual table partitioning.

---

## Q70: Use a trigger to enforce that only one row can exist in a configuration table (singleton pattern).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_singleton_config
BEFORE INSERT ON app_config
FOR EACH ROW
BEGIN
    DECLARE cnt INT;
    SELECT COUNT(*) INTO cnt FROM app_config;
    IF cnt > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Only one configuration row is allowed';
    END IF;
END //
DELIMITER ;
```
**Explanation:** The trigger counts existing rows and blocks the insert if a row already exists, enforcing a single-row constraint.

**Alt1:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_singleton_config() RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT COUNT(*) FROM app_config) > 0 THEN
        RAISE EXCEPTION 'Only one configuration row is allowed';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_singleton_config
BEFORE INSERT ON app_config
FOR EACH ROW
EXECUTE FUNCTION fn_singleton_config();
```
**Explanation:** PostgreSQL uses the same pattern with function-based trigger syntax.

---

## Q71: Write a trigger that rejects INSERT if a required parent row is soft-deleted (is_active = FALSE).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_validate_active_parent
BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
    DECLARE active BOOLEAN;
    SELECT is_active INTO active FROM customers WHERE customer_id = NEW.customer_id;
    IF active IS NULL OR active = FALSE THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot create order for inactive or non-existent customer';
    END IF;
END //
DELIMITER ;
```
**Explanation:** The trigger verifies the parent customer exists and is active before allowing the order to be inserted.

---

## Q72: Use a trigger to automatically update a `last_accessed` timestamp when a row is SELECTed — is this possible?

**Query:**
```sql
-- NOTE: Standard SQL triggers cannot fire on SELECT.
-- This is a common interview "trick question."
-- Workaround: Use a view with an AFTER INSERT on a separate tracking table.

-- PostgreSQL
CREATE TABLE row_access_log (
    table_name TEXT,
    row_id     INT,
    accessed_at TIMESTAMP DEFAULT NOW()
);

-- Application-level approach: INSERT into access_log on read
-- (requires application cooperation, not a true trigger)
```
**Explanation:** Triggers in standard SQL only fire on DML (INSERT, UPDATE, DELETE), never on SELECT. This is a critical interview knowledge point.

---

## Q73: Write a trigger that generates a TOAST-safe audit by writing only changed columns (not all columns).

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_selective_audit() RETURNS TRIGGER AS $$
DECLARE
    changes JSONB := '{}'::JSONB;
BEGIN
    IF OLD.name IS DISTINCT FROM NEW.name THEN
        changes := changes || jsonb_build_object('name', jsonb_build_object('old', OLD.name, 'new', NEW.name));
    END IF;
    IF OLD.email IS DISTINCT FROM NEW.email THEN
        changes := changes || jsonb_build_object('email', jsonb_build_object('old', OLD.email, 'new', NEW.email));
    END IF;
    IF OLD.dept_id IS DISTINCT FROM NEW.dept_id THEN
        changes := changes || jsonb_build_object('dept_id', jsonb_build_object('old', OLD.dept_id, 'new', NEW.dept_id));
    END IF;

    IF changes <> '{}'::JSONB THEN
        INSERT INTO employee_audit (emp_id, changed_columns, changed_at)
        VALUES (OLD.emp_id, changes, NOW());
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_selective_audit
AFTER UPDATE ON employees
FOR EACH ROW
EXECUTE FUNCTION fn_selective_audit();
```
**Explanation:** The trigger only logs columns that actually changed, producing compact audit rows. `IS DISTINCT FROM` safely handles NULL comparisons.

---

## Q74: Write a trigger that prevents modification of a row after it has been finalized (immutable record pattern).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_prevent_update_finalized
BEFORE UPDATE ON invoices
FOR EACH ROW
BEGIN
    IF OLD.is_finalized = TRUE THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot modify a finalized invoice';
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_prevent_delete_finalized
BEFORE DELETE ON invoices
FOR EACH ROW
BEGIN
    IF OLD.is_finalized = TRUE THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete a finalized invoice';
    END IF;
END //
DELIMITER ;
```
**Explanation:** Two triggers protect finalized records from both UPDATE and DELETE, enforcing immutability at the database level.

---

## Q75: Write a trigger that cascades an UPDATE to denormalized data in a related table (e.g., category name changes).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_sync_category_name
AFTER UPDATE ON categories
FOR EACH ROW
BEGIN
    IF OLD.category_name <> NEW.category_name THEN
        UPDATE products
        SET    category_display = NEW.category_name
        WHERE  category_id = NEW.category_id;
    END IF;
END //
DELIMITER ;
```
**Explanation:** When a category name is updated, the trigger propagates the change to all products in that category, keeping denormalized data in sync.


## Q76: Write a trigger that prevents a table from being locked by blocking `SELECT ... FOR UPDATE` on certain conditions.

**Query:**
```sql
-- NOTE: Standard triggers cannot intercept SELECT ... FOR UPDATE.
-- This is another interview "trick question."
-- Workaround in PostgreSQL: Use row-level security policies.

-- PostgreSQL (RLS approach, not a trigger)
ALTER TABLE sensitive_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY no_select_for_update
    ON sensitive_data
    FOR SELECT
    USING (current_user = 'admin');
```
**Explanation:** Triggers do not fire on SELECT or locking reads. Row-level security or application logic must handle read-level access control.

---

## Q77: Write a trigger that prevents duplicate concurrent inserts using advisory locks in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_prevent_concurrent_insert() RETURNS TRIGGER AS $$
BEGIN
    PERFORM pg_advisory_xact_lock(NEW.customer_id);
    IF EXISTS (SELECT 1 FROM orders WHERE customer_id = NEW.customer_id AND status = 'pending') THEN
        RAISE EXCEPTION 'Customer already has a pending order';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_concurrent
BEFORE INSERT ON orders
FOR EACH ROW
EXECUTE FUNCTION fn_prevent_concurrent_insert();
```
**Explanation:** `pg_advisory_xact_lock` acquires a session-level lock on the customer_id, preventing two concurrent inserts for the same customer from passing the check simultaneously.

---

## Q78: Write a trigger that writes a CDC (Change Data Capture) compatible event to a queue table for downstream consumers.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_cdc_events
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    INSERT INTO cdc_events (event_type, payload, created_at)
    VALUES (
        'ORDER_CREATED',
        JSON_OBJECT(
            'order_id',   NEW.order_id,
            'customer_id', NEW.customer_id,
            'amount',     NEW.total_amount,
            'status',     NEW.status
        ),
        NOW()
    );
END //
DELIMITER ;
```
**Explanation:** The trigger writes a structured JSON event that downstream CDC consumers (Kafka, Debezium) can pick up from the queue table.

---

## Q79: Use a trigger to maintain a bitmask column tracking which fields have been modified in a single UPDATE.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_modification_bitmask
BEFORE UPDATE ON profiles
FOR EACH ROW
BEGIN
    SET NEW.modification_flags = 0;
    IF OLD.first_name <> NEW.first_name THEN SET NEW.modification_flags = NEW.modification_flags | 1; END IF;
    IF OLD.last_name  <> NEW.last_name  THEN SET NEW.modification_flags = NEW.modification_flags | 2; END IF;
    IF OLD.email      <> NEW.email      THEN SET NEW.modification_flags = NEW.modification_flags | 4; END IF;
    IF OLD.phone      <> NEW.phone      THEN SET NEW.modification_flags = NEW.modification_flags | 8; END IF;
END //
DELIMITER ;
```
**Explanation:** Each bit position represents a column. The bitmask lets downstream consumers quickly determine which columns changed without comparing old and new values.

---

## Q80: Write a trigger that validates that a JSON column contains all required keys before INSERT.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_validate_json_schema() RETURNS TRIGGER AS $$
BEGIN
    IF NOT (
        NEW.metadata ? 'name' AND
        NEW.metadata ? 'version' AND
        NEW.metadata ? 'created_by'
    ) THEN
        RAISE EXCEPTION 'JSON metadata must contain keys: name, version, created_by';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_json
BEFORE INSERT ON configurations
FOR EACH ROW
EXECUTE FUNCTION fn_validate_json_schema();
```
**Explanation:** The `?` operator checks for key existence in a JSONB object. The trigger rejects rows missing any required key.

**Alt1:**
```sql
-- MySQL 8.0+
DELIMITER //
CREATE TRIGGER trg_validate_json
BEFORE INSERT ON configurations
FOR EACH ROW
BEGIN
    IF NOT (
        JSON_CONTAINS_PATH(NEW.metadata, 'one', '$.name') AND
        JSON_CONTAINS_PATH(NEW.metadata, 'one', '$.version') AND
        JSON_CONTAINS_PATH(NEW.metadata, 'one', '$.created_by')
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'JSON metadata must contain keys: name, version, created_by';
    END IF;
END //
DELIMITER ;
```
**Explanation:** MySQL uses `JSON_CONTAINS_PATH` to verify key presence in a JSON column.

---

## Q81: Write a trigger that auto-generates a tree path string (materialized path pattern) for hierarchical data.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_compute_tree_path() RETURNS TRIGGER AS $$
DECLARE
    parent_path TEXT;
BEGIN
    IF NEW.parent_id IS NULL THEN
        NEW.tree_path := '/' || NEW.node_id::TEXT || '/';
    ELSE
        SELECT tree_path INTO parent_path FROM tree_nodes WHERE node_id = NEW.parent_id;
        NEW.tree_path := parent_path || NEW.node_id::TEXT || '/';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_compute_tree_path
BEFORE INSERT ON tree_nodes
FOR EACH ROW
EXECUTE FUNCTION fn_compute_tree_path();
```
**Explanation:** The trigger materializes the full path (e.g., `/1/5/12/`) on insert, enabling efficient ancestor/descendant queries without recursive CTEs.

---

## Q82: Write a trigger that records the duration of an order (time between creation and completion) on UPDATE.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_order_duration
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    IF OLD.status <> 'completed' AND NEW.status = 'completed' THEN
        UPDATE orders
        SET    completion_hours = TIMESTAMPDIFF(HOUR, created_at, NOW())
        WHERE  order_id = NEW.order_id;
    END IF;
END //
DELIMITER ;
```
**Explanation:** The trigger detects when an order transitions to 'completed' and computes the elapsed time since creation.

---

## Q83: Demonstrate the InnoDB vs MyISAM trigger limitation in MySQL.

**Query:**
```sql
-- MyISAM does not support triggers at all.
-- InnoDB is required for trigger support in MySQL.
-- This is a common interview knowledge point.

-- Verify engine:
SELECT TABLE_NAME, ENGINE
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'employees';
```
**Explanation:** MySQL triggers only work with transactional engines like InnoDB. MyISAM ignores triggers entirely, which is a subtle source of bugs.

---

## Q84: Write a trigger that enforces a minimum time gap between consecutive inserts for the same user (rate limiting).

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_rate_limit() RETURNS TRIGGER AS $$
DECLARE
    last_insert TIMESTAMP;
BEGIN
    SELECT MAX(created_at) INTO last_insert
    FROM audit_log
    WHERE user_id = NEW.user_id;

    IF last_insert IS NOT NULL AND (NOW() - last_insert) < INTERVAL '5 seconds' THEN
        RAISE EXCEPTION 'Rate limit: wait at least 5 seconds between actions';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_rate_limit
BEFORE INSERT ON audit_log
FOR EACH ROW
EXECUTE FUNCTION fn_rate_limit();
```
**Explanation:** The trigger enforces a 5-second minimum gap between consecutive inserts for the same user, preventing rapid-fire abuse.

---

## Q85: Write a trigger that auto-archives old rows by moving them to a partition table on INSERT (sliding window).

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_auto_archive() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.created_at < NOW() - INTERVAL '90 days' THEN
        INSERT INTO logs_archive SELECT NEW.*;
        RETURN NULL;  -- do not insert into the live table
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_auto_archive
BEFORE INSERT ON logs
FOR EACH ROW
EXECUTE FUNCTION fn_auto_archive();
```
**Explanation:** Rows older than 90 days are redirected to an archive table instead of the live table, maintaining a sliding window without manual cleanup.

---

## Q86: Use a trigger to implement optimistic concurrency control with a version column.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_version_check
BEFORE UPDATE ON products
FOR EACH ROW
BEGIN
    IF NEW.version <> OLD.version THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Concurrent modification detected — version mismatch';
    END IF;
    SET NEW.version = OLD.version + 1;
END //
DELIMITER ;
```
**Explanation:** The application must send the original version value. The trigger verifies it hasn't changed since the read, then increments it.

---

## Q87: Write a trigger that prevents changes to audit columns (`created_at`, `created_by`) on UPDATE.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_protect_audit_cols
BEFORE UPDATE ON orders
FOR EACH ROW
BEGIN
    SET NEW.created_at = OLD.created_at;
    SET NEW.created_by = OLD.created_by;
END //
DELIMITER ;
```
**Explanation:** Even if the UPDATE statement tries to modify audit columns, the trigger overwrites them with the original values, ensuring immutability.

---

## Q88: Write a trigger that writes to a dead-letter queue when an INSERT violates a business rule instead of raising an error.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_dead_letter
BEFORE INSERT ON payments
FOR EACH ROW
BEGIN
    IF NEW.amount <= 0 THEN
        INSERT INTO dead_letter_queue (table_name, payload, reason, created_at)
        VALUES ('payments', JSON_OBJECT('amount', NEW.amount, 'customer_id', NEW.customer_id),
                'Invalid amount', NOW());
        SET NEW.amount = NULL;  -- will be caught by NOT NULL constraint or ignored
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid payment amount — logged to dead letter queue';
    END IF;
END //
DELIMITER ;
```
**Explanation:** The trigger first saves the problematic row to a dead-letter queue for manual review before rejecting it, ensuring no bad data is silently lost.

---

## Q89: Write a trigger that automatically updates a全文 full-text search vector column in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_update_search_vector() RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.body, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(NEW.tags, '')), 'C');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_search_vector
BEFORE INSERT OR UPDATE ON articles
FOR EACH ROW
EXECUTE FUNCTION fn_update_search_vector();
```
**Explanation:** The trigger rebuilds the tsvector column on every write, combining weighted title, body, and tags for full-text search.

---

## Q90: Write a trigger that enforces business hour restrictions only on DELETE, not INSERT or UPDATE.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_business_hours_only() RETURNS TRIGGER AS $$
BEGIN
    IF EXTRACT(DOW FROM NOW()) IN (0, 6) THEN
        RAISE EXCEPTION 'Deletes are not allowed on weekends';
    END IF;
    IF EXTRACT(HOUR FROM NOW()) NOT BETWEEN 9 AND 17 THEN
        RAISE EXCEPTION 'Deletes are only allowed during business hours (9 AM - 5 PM)';
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_business_hours_delete
BEFORE DELETE ON transactions
FOR EACH ROW
EXECUTE FUNCTION fn_business_hours_only();
```
**Explanation:** The trigger allows the DELETE only during weekday business hours. It is only attached to the DELETE event, leaving INSERT/UPDATE unrestricted.

---

## Q91: Write a trigger that computes and stores the Levenshtein distance between old and new values for change magnitude tracking.

**Query:**
```sql
-- PostgreSQL (requires pg_trgm extension)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE OR REPLACE FUNCTION fn_change_magnitude() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO change_magnitude_log (emp_id, field_name, old_val, new_val, distance, changed_at)
    SELECT
        OLD.emp_id,
        'name',
        OLD.name,
        NEW.name,
        levenshtein(OLD.name, NEW.name),
        NOW()
    WHERE OLD.name IS DISTINCT FROM NEW.name;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_change_magnitude
AFTER UPDATE ON employees
FOR EACH ROW
EXECUTE FUNCTION fn_change_magnitude();
```
**Explanation:** `levenshtein()` computes the edit distance between strings. The trigger logs how much a name changed, not just that it changed.

---

## Q92: Write a trigger that aggregates child data into a parent JSON array on every child INSERT.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_aggregate_tags() RETURNS TRIGGER AS $$
BEGIN
    UPDATE posts
    SET    tags_array = (
               SELECT COALESCE(JSON_AGG(t.tag_name ORDER BY t.tag_name), '[]'::JSON)
               FROM post_tags pt
               JOIN tags t ON pt.tag_id = t.tag_id
               WHERE pt.post_id = NEW.post_id
           )
    WHERE  post_id = NEW.post_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_aggregate_tags
AFTER INSERT OR DELETE ON post_tags
FOR EACH ROW
EXECUTE FUNCTION fn_aggregate_tags();
```
**Explanation:** The trigger rebuilds the full tags JSON array on the parent post whenever a tag is added or removed, maintaining a pre-aggregated view.

---

## Q93: Write a trigger that enforces that a numeric column can only increase (monotonically increasing sequence).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_monotonic_sequence
BEFORE UPDATE ON sequences
FOR EACH ROW
BEGIN
    IF NEW.current_value <= OLD.current_value THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Sequence value can only increase';
    END IF;
END //
DELIMITER ;
```
**Explanation:** The trigger ensures the sequence counter never decreases, preventing accidental rollbacks or duplicate key assignments.

---

## Q94: Use a trigger to prevent batch operations from exceeding a row-count threshold.

**Query:**
```sql
-- SQL Server
CREATE TRIGGER trg_batch_limit
ON order_items
AFTER INSERT
AS
BEGIN
    DECLARE @count INT = (SELECT COUNT(*) FROM inserted);
    IF @count > 1000
    BEGIN
        RAISERROR ('Batch size exceeds maximum of 1000 rows', 16, 1);
        ROLLBACK;
    END;
END;
```
**Explanation:** The trigger counts rows in the `inserted` virtual table and rolls back if the batch is too large, protecting against accidental mass inserts.

---

## Q95: Write a trigger that writes to a remote database via a database link when a row is inserted (Oracle).

**Query:**
```sql
-- Oracle
CREATE OR REPLACE TRIGGER trg_remote_sync
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    INSERT INTO orders_remote@remote_db (order_id, customer_id, amount, created_at)
    VALUES (:NEW.order_id, :NEW.customer_id, :NEW.amount, SYSDATE);
END;
/
```
**Explanation:** Oracle database links allow triggers to write to remote databases. The `@remote_db` suffix specifies the database link. Network failures will cause the trigger to fail and rollback the local transaction.

---

## Q96: Write a trigger that normalizes text input (trim, collapse whitespace, lowercase email) on INSERT.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_normalize_text() RETURNS TRIGGER AS $$
BEGIN
    NEW.email  := LOWER(TRIM(NEW.email));
    NEW.name   := REGEXP_REPLACE(TRIM(NEW.name), '\s+', ' ', 'g');
    NEW.phone  := REGEXP_REPLACE(NEW.phone, '[^0-9+]', '', 'g');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_normalize_text
BEFORE INSERT OR UPDATE ON contacts
FOR EACH ROW
EXECUTE FUNCTION fn_normalize_text();
```
**Explanation:** The trigger applies multiple normalization rules — lowercasing email, collapsing whitespace in names, stripping non-numeric characters from phone — before the row is stored.

---

## Q97: Write a trigger that prevents DELETE on a parent table when child rows exist (manual ON DELETE RESTRICT).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_manual_restrict_delete
BEFORE DELETE ON departments
FOR EACH ROW
BEGIN
    DECLARE child_count INT;
    SELECT COUNT(*) INTO child_count FROM employees WHERE dept_id = OLD.dept_id;
    IF child_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete department with existing employees';
    END IF;
END //
DELIMITER ;
```
**Explanation:** When the FK constraint is intentionally disabled for performance, this trigger enforces RESTRICT behavior manually.

**Alt1:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_manual_restrict() RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM employees WHERE dept_id = OLD.dept_id) THEN
        RAISE EXCEPTION 'Cannot delete department with existing employees';
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_manual_restrict_delete
BEFORE DELETE ON departments
FOR EACH ROW
EXECUTE FUNCTION fn_manual_restrict();
```
**Explanation:** Same logic in PostgreSQL. The EXISTS check is more efficient than COUNT for large child tables.

---

## Q98: Write a trigger that populates a materialized summary table using a CTE-style aggregation on every INSERT.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_update_category_stats() RETURNS TRIGGER AS $$
BEGIN
    WITH category_stats AS (
        SELECT
            category_id,
            COUNT(*)        AS product_count,
            AVG(price)      AS avg_price,
            SUM(stock)      AS total_stock
        FROM products
        WHERE category_id = NEW.category_id
        GROUP BY category_id
    )
    INSERT INTO category_summary (category_id, product_count, avg_price, total_stock, last_updated)
    SELECT cs.*, NOW()
    FROM category_stats cs
    ON CONFLICT (category_id) DO UPDATE
    SET product_count  = EXCLUDED.product_count,
        avg_price      = EXCLUDED.avg_price,
        total_stock    = EXCLUDED.total_stock,
        last_updated   = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_category_stats
AFTER INSERT OR DELETE OR UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION fn_update_category_stats();
```
**Explanation:** The trigger uses a CTE to recompute category statistics and upserts the result into a summary table, keeping aggregated data always current.

---

## Q99: Write a trigger that implements a state machine, enforcing valid state transitions on UPDATE.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE TRIGGER trg_state_machine
BEFORE UPDATE ON tickets
FOR EACH ROW
BEGIN
    IF OLD.status = 'open' AND NEW.status NOT IN ('in_progress', 'closed') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Open tickets can only move to in_progress or closed';
    ELSEIF OLD.status = 'in_progress' AND NEW.status NOT IN ('resolved', 'closed') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'In-progress tickets can only move to resolved or closed';
    ELSEIF OLD.status = 'resolved' AND NEW.status NOT IN ('closed', 'reopened') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Resolved tickets can only move to closed or reopened';
    ELSEIF OLD.status = 'closed' AND NEW.status <> 'reopened' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Closed tickets can only be reopened';
    END IF;
END //
DELIMITER ;
```
**Explanation:** The trigger encodes a state transition table as conditional logic, ensuring tickets follow the defined workflow (open -> in_progress -> resolved -> closed).

---

## Q100: Write a comprehensive trigger that combines audit logging, validation, and denormalized column maintenance in a single AFTER UPDATE trigger.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION fn_comprehensive_trigger() RETURNS TRIGGER AS $$
DECLARE
    changes JSONB := '{}'::JSONB;
BEGIN
    -- 1. Validation
    IF NEW.salary < 0 THEN
        RAISE EXCEPTION 'Salary cannot be negative';
    END IF;
    IF NEW.email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RAISE EXCEPTION 'Invalid email format';
    END IF;

    -- 2. Selective audit logging (only changed columns)
    IF OLD.name IS DISTINCT FROM NEW.name THEN
        changes := changes || jsonb_build_object('name', jsonb_build_object('old', OLD.name, 'new', NEW.name));
    END IF;
    IF OLD.salary IS DISTINCT FROM NEW.salary THEN
        changes := changes || jsonb_build_object('salary', jsonb_build_object('old', OLD.salary, 'new', NEW.salary));
    END IF;
    IF OLD.dept_id IS DISTINCT FROM NEW.dept_id THEN
        changes := changes || jsonb_build_object('dept_id', jsonb_build_object('old', OLD.dept_id, 'new', NEW.dept_id));
    END IF;

    IF changes <> '{}'::JSONB THEN
        INSERT INTO employee_audit (emp_id, changed_columns, changed_by, changed_at)
        VALUES (OLD.emp_id, changes, current_user, NOW());
    END IF;

    -- 3. Denormalized column maintenance
    UPDATE department_summary
    SET    total_salary = (SELECT COALESCE(SUM(salary), 0) FROM employees WHERE dept_id = NEW.dept_id),
           headcount    = (SELECT COUNT(*) FROM employees WHERE dept_id = NEW.dept_id)
    WHERE  dept_id = NEW.dept_id;

    -- If department changed, also update the old department summary
    IF OLD.dept_id IS DISTINCT FROM NEW.dept_id THEN
        UPDATE department_summary
        SET    total_salary = (SELECT COALESCE(SUM(salary), 0) FROM employees WHERE dept_id = OLD.dept_id),
               headcount    = (SELECT COUNT(*) FROM employees WHERE dept_id = OLD.dept_id)
        WHERE  dept_id = OLD.dept_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_comprehensive
AFTER UPDATE ON employees
FOR EACH ROW
EXECUTE FUNCTION fn_comprehensive_trigger();
```
**Explanation:** A single trigger function handles three concerns: input validation, selective audit logging of only changed columns, and denormalized summary maintenance for both old and new departments. This demonstrates real-world trigger composition.

