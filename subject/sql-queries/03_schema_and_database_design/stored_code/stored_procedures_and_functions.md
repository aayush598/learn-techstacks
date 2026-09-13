# Stored Procedures and Functions — 100 SQL Interview Q&A

## Q1: Create a simple stored procedure that selects all rows from an employees table.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE get_all_employees()
BEGIN
    SELECT * FROM employees;
END //
DELIMITER ;

-- PostgreSQL
CREATE OR REPLACE PROCEDURE get_all_employees()
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT * FROM employees;
END;
$$;

-- SQL Server
CREATE PROCEDURE get_all_employees
AS
BEGIN
    SELECT * FROM employees;
END;
```
**Explanation:** The basic `CREATE PROCEDURE` syntax varies by dialect; MySQL uses `DELIMITER` for body delimiters, PostgreSQL uses `PL/pgSQL`, and SQL Server uses a simpler `AS BEGIN` block.

---

## Q2: Call a stored procedure that takes no parameters.

**Query:**
```sql
-- MySQL
CALL get_all_employees();

-- PostgreSQL
CALL get_all_employees();

-- SQL Server
EXEC get_all_employees;
-- or
EXECUTE get_all_employees;

-- Oracle
BEGIN
    get_all_employees;
END;
/
```
**Explanation:** MySQL and PostgreSQL use `CALL`, SQL Server uses `EXEC`/`EXECUTE`, and Oracle invokes procedures within anonymous `BEGIN...END` blocks.

---

## Q3: Create a procedure with one `IN` parameter to filter employees by department.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE get_employees_by_dept(IN p_dept_id INT)
BEGIN
    SELECT * FROM employees WHERE department_id = p_dept_id;
END //
DELIMITER ;

-- PostgreSQL
CREATE OR REPLACE PROCEDURE get_employees_by_dept(p_dept_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY SELECT * FROM employees WHERE department_id = p_dept_id;
END;
$$;

-- SQL Server
CREATE PROCEDURE get_employees_by_dept
    @dept_id INT
AS
BEGIN
    SELECT * FROM employees WHERE department_id = @dept_id;
END;
```
**Explanation:** `IN` parameters pass values into the procedure. The prefix `p_` or `@` is a naming convention; the parameter is read-only inside the body.

**Alt1:** Oracle `IN` parameter with `%TYPE` anchoring:
```sql
-- Oracle
CREATE OR REPLACE PROCEDURE get_employees_by_dept(
    p_dept_id IN employees.department_id%TYPE
)
AS
BEGIN
    FOR rec IN (SELECT * FROM employees WHERE department_id = p_dept_id) LOOP
        DBMS_OUTPUT.PUT_LINE(rec.last_name || ': ' || rec.salary);
    END LOOP;
END;
/

BEGIN
    get_employees_by_dept(5);
END;
/
```

---

## Q4: Create a procedure with an `OUT` parameter that returns a count.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE count_employees(OUT p_total INT)
BEGIN
    SELECT COUNT(*) INTO p_total FROM employees;
END //
DELIMITER ;

-- Call it
CALL count_employees(@total);
SELECT @total;

-- SQL Server
CREATE PROCEDURE count_employees
    @total INT OUTPUT
AS
BEGIN
    SELECT @total = COUNT(*) FROM employees;
END;

DECLARE @total INT;
EXEC count_employees @total OUTPUT;
SELECT @total;
```
**Explanation:** `OUT` parameters send values back to the caller. In MySQL you retrieve the value from a session variable; in SQL Server you pass the variable with the `OUTPUT` keyword.

---

## Q5: Create a procedure with an `INOUT` parameter that doubles a value.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE double_value(INOUT p_num INT)
BEGIN
    SET p_num = p_num * 2;
END //
DELIMITER ;

SET @val = 10;
CALL double_value(@val);
SELECT @val; -- 20

-- SQL Server
CREATE PROCEDURE double_value
    @num INT OUTPUT
AS
BEGIN
    SET @num = @num * 2;
END;

DECLARE @v INT = 10;
EXEC double_value @v OUTPUT;
SELECT @v; -- 20
```
**Explanation:** `INOUT` (MySQL) lets a parameter be both read and written. SQL Server doesn't have `INOUT`; you use `OUTPUT` and pass the same variable back.

---

## Q6: Create a scalar function that returns the full name from first and last name.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE FUNCTION full_name(p_first VARCHAR(50), p_last VARCHAR(50))
RETURNS VARCHAR(100)
DETERMINISTIC
BEGIN
    RETURN CONCAT(p_first, ' ', p_last);
END //
DELIMITER ;

-- PostgreSQL
CREATE OR REPLACE FUNCTION full_name(p_first TEXT, p_last TEXT)
RETURNS TEXT
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT p_first || ' ', p_last;
$$;

-- SQL Server
CREATE FUNCTION full_name(@first NVARCHAR(50), @last NVARCHAR(50))
RETURNS NVARCHAR(100)
AS
BEGIN
    RETURN @first + ' ' + @last;
END;
```
**Explanation:** Scalar functions return a single value. MySQL requires `DETERMINISTIC`, PostgreSQL uses `IMMUTABLE`/`STABLE`/`VOLATILE`, and SQL Server scalar functions use `BEGIN...RETURN`.

---

## Q7: Create a function and use it inside a SELECT statement.

**Query:**
```sql
-- MySQL
SELECT employee_id, full_name(first_name, last_name) AS name
FROM employees;

-- PostgreSQL
SELECT employee_id, full_name(first_name, last_name) AS name
FROM employees;

-- SQL Server
SELECT employee_id, dbo.full_name(first_name, last_name) AS name
FROM employees;
```
**Explanation:** Functions can be used inline in `SELECT`. SQL Server requires the schema prefix (e.g., `dbo.`) when calling user-defined functions in queries.

---

## Q8: Declare a variable and assign a value using `DECLARE` and `SET`.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE demo_variables()
BEGIN
    DECLARE v_name VARCHAR(100);
    DECLARE v_salary DECIMAL(10,2) DEFAULT 50000.00;

    SET v_name = 'Alice';
    SELECT v_name, v_salary;
END //
DELIMITER ;

-- SQL Server
CREATE PROCEDURE demo_variables
AS
BEGIN
    DECLARE @name NVARCHAR(100);
    DECLARE @salary DECIMAL(10,2) = 50000.00;

    SET @name = 'Alice';
    SELECT @name AS name, @salary AS salary;
END;
```
**Explanation:** `DECLARE` creates local variables scoped to the procedure body. `SET` assigns values; `DEFAULT` provides initial values. SQL Server also supports inline `= value` in `DECLARE`.

**Alt1:** PostgreSQL variable handling in PL/pgSQL:
```sql
-- PostgreSQL
CREATE OR REPLACE PROCEDURE demo_variables()
LANGUAGE plpgsql
AS $$
DECLARE
    v_name TEXT;
    v_salary NUMERIC := 50000.00;
BEGIN
    v_name := 'Alice';
    RAISE NOTICE 'name=% salary=%', v_name, v_salary;
END;
$$;
```

---

## Q9: Use `SELECT INTO` to assign a query result to a variable.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE get_max_salary(OUT p_max_sal DECIMAL(10,2))
BEGIN
    SELECT MAX(salary) INTO p_max_sal FROM employees;
END //
DELIMITER ;

-- SQL Server
CREATE PROCEDURE get_max_salary
    @max_sal DECIMAL(10,2) OUTPUT
AS
BEGIN
    SELECT @max_sal = MAX(salary) FROM employees;
END;

-- PostgreSQL
CREATE OR REPLACE FUNCTION get_max_salary()
RETURNS DECIMAL(10,2)
LANGUAGE plpgsql
AS $$
DECLARE
    v_max_sal DECIMAL(10,2);
BEGIN
    SELECT MAX(salary) INTO v_max_sal FROM employees;
    RETURN v_max_sal;
END;
$$;
```
**Explanation:** `SELECT INTO` (MySQL/PL/pgSQL) or direct assignment in SQL Server fetches a scalar result into a variable in a single statement.

---

## Q10: Use an `IF/ELSE` block inside a procedure.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE check_salary(IN p_emp_id INT)
BEGIN
    DECLARE v_sal DECIMAL(10,2);
    SELECT salary INTO v_sal FROM employees WHERE employee_id = p_emp_id;

    IF v_sal > 100000 THEN
        SELECT 'High earner' AS category;
    ELSE
        SELECT 'Standard earner' AS category;
    END IF;
END //
DELIMITER ;

-- SQL Server
CREATE PROCEDURE check_salary @emp_id INT
AS
BEGIN
    DECLARE @sal DECIMAL(10,2);
    SELECT @sal = salary FROM employees WHERE employee_id = @emp_id;

    IF @sal > 100000
        SELECT 'High earner' AS category;
    ELSE
        SELECT 'Standard earner' AS category;
END;
```
**Explanation:** `IF/ELSE` provides conditional branching. MySQL wraps the block in `BEGIN...END IF`, while SQL Server uses `IF...ELSE` without a closing keyword.

**Alt1:** Oracle uses `IF/ELSIF/ELSE ... END IF`:
```sql
-- Oracle
CREATE OR REPLACE PROCEDURE check_salary(p_emp_id IN NUMBER)
AS
    v_sal NUMBER;
BEGIN
    SELECT salary INTO v_sal FROM employees WHERE employee_id = p_emp_id;

    IF v_sal > 100000 THEN
        DBMS_OUTPUT.PUT_LINE('High earner');
    ELSIF v_sal > 50000 THEN
        DBMS_OUTPUT.PUT_LINE('Mid earner');
    ELSE
        DBMS_OUTPUT.PUT_LINE('Standard earner');
    END IF;
END;
/
```

---

## Q11: Use `CASE` inside a procedure to categorize data.

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE categorize_employees
AS
BEGIN
    SELECT
        employee_id,
        first_name,
        salary,
        CASE
            WHEN salary >= 150000 THEN 'Executive'
            WHEN salary >= 80000 THEN 'Senior'
            WHEN salary >= 40000 THEN 'Mid-level'
            ELSE 'Junior'
        END AS tier
    FROM employees;
END;

-- MySQL
DELIMITER //
CREATE PROCEDURE categorize_employees()
BEGIN
    SELECT
        employee_id,
        first_name,
        salary,
        CASE
            WHEN salary >= 150000 THEN 'Executive'
            WHEN salary >= 80000 THEN 'Senior'
            WHEN salary >= 40000 THEN 'Mid-level'
            ELSE 'Junior'
        END AS tier
    FROM employees;
END //
DELIMITER ;
```
**Explanation:** `CASE` expressions allow branching logic directly within a `SELECT` statement, useful for classification without procedural `IF` blocks.

---

## Q12: Use a `WHILE` loop to generate a sequence of numbers.

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE generate_numbers @count INT
AS
BEGIN
    DECLARE @i INT = 1;
    WHILE @i <= @count
    BEGIN
        SELECT @i AS number;
        SET @i = @i + 1;
    END;
END;

-- MySQL
DELIMITER //
CREATE PROCEDURE generate_numbers(IN p_count INT)
BEGIN
    DECLARE v_i INT DEFAULT 1;
    WHILE v_i <= p_count DO
        SELECT v_i AS number;
        SET v_i = v_i + 1;
    END WHILE;
END //
DELIMITER ;
```
**Explanation:** `WHILE` loops repeat a block until a condition is false. MySQL requires `DO...END WHILE`; SQL Server uses `BEGIN...END` inside the loop body.

**Alt1:** PostgreSQL `WHILE` loop with `FOREACH` style control in PL/pgSQL:
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION generate_numbers(p_count INT)
RETURNS SETOF INT
LANGUAGE plpgsql
AS $$
DECLARE
    v_i INT := 1;
BEGIN
    WHILE v_i <= p_count LOOP
        RETURN NEXT v_i;
        v_i := v_i + 1;
    END LOOP;
END;
$$;

SELECT * FROM generate_numbers(5);
```

---

## Q13: Create a procedure that inserts multiple rows using a loop.

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE insert_log_entries @num_rows INT
AS
BEGIN
    DECLARE @i INT = 1;
    WHILE @i <= @num_rows
    BEGIN
        INSERT INTO audit_log (message, created_at)
        VALUES (CONCAT('Log entry ', @i), GETDATE());
        SET @i = @i + 1;
    END;
END;

-- MySQL
DELIMITER //
CREATE PROCEDURE insert_log_entries(IN p_num_rows INT)
BEGIN
    DECLARE v_i INT DEFAULT 1;
    WHILE v_i <= p_num_rows DO
        INSERT INTO audit_log (message, created_at)
        VALUES (CONCAT('Log entry ', v_i), NOW());
        SET v_i = v_i + 1;
    END WHILE;
END //
DELIMITER ;
```
**Explanation:** Loops inside procedures enable bulk operations row-by-row. Note that set-based approaches are generally preferred over row-by-row inserts for performance.

**Alt1:** Set-based alternative using a recursive CTE instead of a loop:
```sql
-- SQL Server
CREATE PROCEDURE insert_log_entries @num_rows INT
AS
BEGIN
    WITH seq AS (
        SELECT 1 AS n
        UNION ALL
        SELECT n + 1 FROM seq WHERE n < @num_rows
    )
    INSERT INTO audit_log (message, created_at)
    SELECT CONCAT('Log entry ', n), GETDATE() FROM seq
    OPTION (MAXRECURSION 32767);
END;
```

---

## Q14: Create a procedure using a `DECLARE HANDLER` for error handling (MySQL).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE safe_insert_employee(
    IN p_first VARCHAR(50),
    IN p_last VARCHAR(50),
    IN p_email VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR 1062
    BEGIN
        SELECT 'Duplicate email error' AS error_message;
    END;

    INSERT INTO employees (first_name, last_name, email)
    VALUES (p_first, p_last, p_email);
END //
DELIMITER ;
```
**Explanation:** MySQL's `DECLARE HANDLER` catches specific error codes (1062 = duplicate key). `EXIT HANDLER` rolls back and exits the `BEGIN...END` block on error.

---

## Q15: Create a procedure with `EXCEPTION` handling in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE PROCEDURE safe_insert_employee(
    p_first TEXT,
    p_last TEXT,
    p_email TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO employees (first_name, last_name, email)
    VALUES (p_first, p_last, p_email);
    COMMIT;

EXCEPTION
    WHEN unique_violation THEN
        RAISE NOTICE 'Duplicate email: %', p_email;
    WHEN OTHERS THEN
        RAISE NOTICE 'Unexpected error: %', SQLERRM;
END;
$$;
```
**Explanation:** PostgreSQL procedures use `EXCEPTION` blocks with `WHEN` clauses. `WHEN OTHERS` catches all remaining errors. `SQLERRM` holds the error message text.

---

## Q16: Create a procedure with `TRY/CATCH` in SQL Server.

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE safe_insert_employee
    @first NVARCHAR(50),
    @last NVARCHAR(50),
    @email NVARCHAR(100)
AS
BEGIN
    BEGIN TRY
        INSERT INTO employees (first_name, last_name, email)
        VALUES (@first, @last, @email);
    END TRY
    BEGIN CATCH
        SELECT
            ERROR_NUMBER() AS error_number,
            ERROR_MESSAGE() AS error_message;
    END CATCH;
END;
```
**Explanation:** SQL Server wraps risky code in `BEGIN TRY...END TRY BEGIN CATCH...END CATCH`. Functions like `ERROR_NUMBER()` and `ERROR_MESSAGE()` provide diagnostic info.

---

## Q17: Create a procedure with exception handling in Oracle using `PRAGMA EXCEPTION_INIT`.

**Query:**
```sql
-- Oracle
CREATE OR REPLACE PROCEDURE safe_insert_employee(
    p_first IN VARCHAR2,
    p_last  IN VARCHAR2,
    p_email IN VARCHAR2
)
AS
    dup_val EXCEPTION;
    PRAGMA EXCEPTION_INIT(dup_val, -1);
BEGIN
    INSERT INTO employees (first_name, last_name, email)
    VALUES (p_first, p_last, p_email);
    COMMIT;
EXCEPTION
    WHEN dup_val THEN
        DBMS_OUTPUT.PUT_LINE('Duplicate email: ' || p_email);
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
        ROLLBACK;
END;
/
```
**Explanation:** Oracle uses `PRAGMA EXCEPTION_INIT` to associate a named exception with an Oracle error number (-1 is `ORA-00001` unique constraint violation).

---

## Q18: Create a dynamic SQL statement using `EXECUTE IMMEDIATE` in Oracle.

**Query:**
```sql
-- Oracle
CREATE OR REPLACE PROCEDURE get_table_count(
    p_table_name IN VARCHAR2,
    p_count      OUT NUMBER
)
AS
    v_sql VARCHAR2(500);
BEGIN
    v_sql := 'SELECT COUNT(*) FROM ' || DBMS_ASSERT.SQL_OBJECT_NAME(p_table_name);
    EXECUTE IMMEDIATE v_sql INTO p_count;
END;
/

-- Usage
DECLARE
    v_cnt NUMBER;
BEGIN
    get_table_count('employees', v_cnt);
    DBMS_OUTPUT.PUT_LINE('Rows: ' || v_cnt);
END;
/
```
**Explanation:** `EXECUTE IMMEDIATE` runs dynamically constructed SQL. `DBMS_ASSERT.SQL_OBJECT_NAME` sanitizes the table name to prevent SQL injection.

**Alt1:** Same dynamic count with parameterized `sp_executesql` in SQL Server:
```sql
-- SQL Server
CREATE PROCEDURE get_table_count
    @table NVARCHAR(128),
    @count INT OUTPUT
AS
BEGIN
    DECLARE @sql NVARCHAR(MAX);
    SET @sql = N'SELECT @cnt = COUNT(*) FROM ' + QUOTENAME(@table);
    IF OBJECT_ID(@table, 'U') IS NULL
        THROW 51000, 'Unknown table', 1;
    EXEC sp_executesql @sql, N'@cnt INT OUTPUT', @cnt = @count OUTPUT;
END;

DECLARE @c INT;
EXEC get_table_count 'employees', @c OUTPUT;
SELECT @c;
```

---

## Q19: Create dynamic SQL using `PREPARE`/`EXECUTE` in MySQL.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE dynamic_search(
    IN p_table VARCHAR(64),
    IN p_col VARCHAR(64),
    IN p_val VARCHAR(255)
)
BEGIN
    SET @sql = CONCAT('SELECT * FROM ', p_table, ' WHERE ', p_col, ' = ?');
    SET @p = p_val;
    PREPARE stmt FROM @sql;
    EXECUTE stmt USING @p;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;
```
**Explanation:** MySQL uses `PREPARE` to compile a string into a statement, `EXECUTE ... USING` to bind parameters safely, and `DEALLOCATE PREPARE` to free resources.

---

## Q20: Create dynamic SQL in SQL Server using `sp_executesql`.

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE dynamic_search
    @table NVARCHAR(128),
    @column NVARCHAR(128),
    @value NVARCHAR(255)
AS
BEGIN
    DECLARE @sql NVARCHAR(MAX);
    DECLARE @params NVARCHAR(200);
    SET @sql = N'SELECT * FROM ' + QUOTENAME(@table) + N' WHERE ' + QUOTENAME(@column) + N' = @p_val';
    SET @params = N'@p_val NVARCHAR(255)';
    EXEC sp_executesql @sql, @params, @p_val = @value;
END;
```
**Explanation:** `sp_executesql` supports parameter binding, preventing SQL injection. `QUOTENAME` safely brackets identifiers. Always prefer `sp_executesql` over `EXEC(@sql)`.

---

## Q21: Demonstrate the difference between a procedure and a function.

**Query:**
```sql
-- A function (can be used in SELECT, returns a value)
-- SQL Server
CREATE FUNCTION calc_bonus(@salary DECIMAL(10,2))
RETURNS DECIMAL(10,2)
AS
BEGIN
    RETURN @salary * 0.10;
END;

-- A procedure (cannot be used in SELECT, can perform actions)
CREATE PROCEDURE give_bonus @emp_id INT
AS
BEGIN
    UPDATE employees SET salary = salary * 1.10 WHERE employee_id = @emp_id;
END;

-- Function in a query
SELECT employee_id, dbo.calc_bonus(salary) AS bonus FROM employees;

-- Procedure call
EXEC give_bonus @emp_id = 101;
```
**Explanation:** Functions return a value and can appear in `SELECT`; they cannot modify database state (in SQL Server/PostgreSQL). Procedures perform actions, support transactions, but cannot be used in `SELECT`.

---

## Q22: Create a table-valued function that returns a result set.

**Query:**
```sql
-- SQL Server (inline table-valued function)
CREATE FUNCTION get_dept_employees(@dept_id INT)
RETURNS TABLE
AS
RETURN
(
    SELECT employee_id, first_name, last_name, salary
    FROM employees
    WHERE department_id = @dept_id
);

-- Usage
SELECT * FROM dbo.get_dept_employees(5);

-- SQL Server (multi-statement table-valued function)
CREATE FUNCTION get_senior_employees()
RETURNS @result TABLE
(
    employee_id INT,
    full_name NVARCHAR(100),
    salary DECIMAL(10,2)
)
AS
BEGIN
    INSERT INTO @result
    SELECT employee_id, first_name + ' ' + last_name, salary
    FROM employees WHERE salary >= 100000;
    RETURN;
END;
```
**Explanation:** Inline TVFs return a single `SELECT` and are optimized like views. Multi-statement TVFs declare a table variable, populate it, and return it.

**Alt1:** PostgreSQL equivalent using `RETURNS SETOF`:
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION get_dept_employees(p_dept_id INT)
RETURNS SETOF employees
LANGUAGE sql
STABLE
AS $$
    SELECT * FROM employees WHERE department_id = p_dept_id;
$$;

SELECT employee_id, last_name FROM get_dept_employees(5);
```

---

## Q23: Create a table-valued function in PostgreSQL using `RETURNS TABLE`.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION get_dept_employees(p_dept_id INT)
RETURNS TABLE (
    emp_id INT,
    emp_name TEXT,
    emp_salary NUMERIC
)
LANGUAGE sql
AS $$
    SELECT employee_id, first_name || ' ' || last_name, salary
    FROM employees
    WHERE department_id = p_dept_id;
$$;

-- Usage
SELECT * FROM get_dept_employees(5);
```
**Explanation:** PostgreSQL table-valued functions use `RETURNS TABLE` with column definitions and can be called directly in `FROM` or `SELECT` like a table.

---

## Q24: Use a `RETURN` statement to exit a procedure early.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE process_employee(IN p_emp_id INT)
BEGIN
    DECLARE v_active BOOLEAN;

    SELECT is_active INTO v_active FROM employees WHERE employee_id = p_emp_id;

    IF v_active = FALSE THEN
        SELECT 'Employee inactive, skipping.' AS status;
        RETURN;
    END IF;

    -- continue processing active employee
    UPDATE employees SET last_processed = NOW() WHERE employee_id = p_emp_id;
    SELECT 'Processed.' AS status;
END //
DELIMITER ;

-- SQL Server
CREATE PROCEDURE process_employee @emp_id INT
AS
BEGIN
    DECLARE @active BIT;

    SELECT @active = is_active FROM employees WHERE employee_id = @emp_id;

    IF @active = 0
    BEGIN
        SELECT 'Employee inactive, skipping.' AS status;
        RETURN;
    END;

    UPDATE employees SET last_processed = GETDATE() WHERE employee_id = @emp_id;
    SELECT 'Processed.' AS status;
END;
```
**Explanation:** `RETURN` exits the procedure immediately. In SQL Server, `RETURN` can also send an integer status code; in MySQL, it simply stops execution.

---

## Q25: Use a `RETURN` value from a function in Oracle.

**Query:**
```sql
-- Oracle
CREATE OR REPLACE FUNCTION calc_tax(p_salary IN NUMBER)
RETURN NUMBER
AS
    v_tax NUMBER;
BEGIN
    IF p_salary > 100000 THEN
        v_tax := p_salary * 0.30;
    ELSIF p_salary > 50000 THEN
        v_tax := p_salary * 0.20;
    ELSE
        v_tax := p_salary * 0.10;
    END IF;

    RETURN v_tax;
END;
/

-- Usage in a query
SELECT employee_id, calc_tax(salary) AS tax FROM employees;
```
**Explanation:** Oracle functions must have a `RETURN` clause in the header and at least one `RETURN` statement in the body. The returned value is a scalar used in SQL expressions.

---

## Q26: Use a `WHILE` loop with `BREAK` and `CONTINUE`.

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE loop_demo @max INT
AS
BEGIN
    DECLARE @i INT = 0;
    WHILE @i <= @max
    BEGIN
        SET @i = @i + 1;
        IF @i % 2 = 0
            CONTINUE;  -- skip even numbers
        IF @i > 10
            BREAK;     -- stop after 11
        SELECT @i AS odd_number;
    END;
END;
```
**Explanation:** `CONTINUE` skips to the next iteration; `BREAK` exits the loop entirely. SQL Server supports both inside `WHILE`; MySQL supports `ITERATE` (equivalent to `CONTINUE`) and `LEAVE` (equivalent to `BREAK`).

**Alt1:** MySQL equivalent with `ITERATE`/`LEAVE`:
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE loop_demo(IN p_max INT)
BEGIN
    DECLARE v_i INT DEFAULT 0;
    my_loop: WHILE v_i <= p_max DO
        SET v_i = v_i + 1;
        IF v_i % 2 = 0 THEN
            ITERATE my_loop;
        END IF;
        IF v_i > 10 THEN
            LEAVE my_loop;
        END IF;
        SELECT v_i AS odd_number;
    END WHILE my_loop;
END //
DELIMITER ;
```

---

## Q27: Declare and use a `CURSOR` to iterate over rows (MySQL).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE iterate_employees()
BEGIN
    DECLARE v_id INT;
    DECLARE v_name VARCHAR(100);
    DECLARE v_done BOOLEAN DEFAULT FALSE;
    DECLARE emp_cursor CURSOR FOR
        SELECT employee_id, CONCAT(first_name, ' ', last_name) FROM employees;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = TRUE;

    OPEN emp_cursor;
    read_loop: LOOP
        FETCH emp_cursor INTO v_id, v_name;
        IF v_done THEN
            LEAVE read_loop;
        END IF;
        -- process each row
        INSERT INTO employee_log (emp_id, emp_name, processed_at)
        VALUES (v_id, v_name, NOW());
    END LOOP;
    CLOSE emp_cursor;
END //
DELIMITER ;
```
**Explanation:** Cursors allow row-by-row processing. `DECLARE CONTINUE HANDLER FOR NOT FOUND` sets a flag when no more rows exist. Always `OPEN`, `FETCH`, and `CLOSE` cursors in order.

---

## Q28: Declare and use a `CURSOR` in SQL Server.

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE iterate_employees
AS
BEGIN
    DECLARE @id INT, @name NVARCHAR(100);

    DECLARE emp_cursor CURSOR FOR
        SELECT employee_id, first_name + ' ' + last_name FROM employees;

    OPEN emp_cursor;
    FETCH NEXT FROM emp_cursor INTO @id, @name;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        INSERT INTO employee_log (emp_id, emp_name, processed_at)
        VALUES (@id, @name, GETDATE());
        FETCH NEXT FROM emp_cursor INTO @id, @name;
    END;

    CLOSE emp_cursor;
    DEALLOCATE emp_cursor;
END;
```
**Explanation:** SQL Server cursors use `@@FETCH_STATUS` to detect end-of-data. `DEALLOCATE` releases cursor resources after `CLOSE`.

---

## Q29: Declare a cursor in PostgreSQL using `REFCURSOR`.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE PROCEDURE iterate_employees()
LANGUAGE plpgsql
AS $$
DECLARE
    emp_record RECORD;
    emp_cursor CURSOR FOR
        SELECT employee_id, first_name || ' ' || last_name AS emp_name FROM employees;
BEGIN
    OPEN emp_cursor;
    LOOP
        FETCH emp_cursor INTO emp_record;
        EXIT WHEN NOT FOUND;
        INSERT INTO employee_log (emp_id, emp_name, processed_at)
        VALUES (emp_record.employee_id, emp_record.emp_name, NOW());
    END LOOP;
    CLOSE emp_cursor;
END;
$$;
```
**Explanation:** PostgreSQL cursors use `FETCH ... INTO` with a `RECORD` variable and `EXIT WHEN NOT FOUND` to stop iteration.

---

## Q30: Return a result set from a procedure using `REFCURSOR` (PostgreSQL).

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE PROCEDURE get_employees_refcursor(
    p_dept_id INT,
    INOUT ref REFCURSOR
)
LANGUAGE plpgsql
AS $$
BEGIN
    OPEN ref FOR
        SELECT employee_id, first_name, last_name
        FROM employees
        WHERE department_id = p_dept_id;
END;
$$;

-- Usage
BEGIN;
CALL get_employees_refcursor(5, 'my_cursor');
FETCH ALL FROM my_cursor;
COMMIT;
```
**Explanation:** `REFCURSOR` lets a procedure return an open cursor to the caller. The caller must `FETCH` from it and eventually `COMMIT` or `CLOSE` the transaction.

**Alt1:** Oracle equivalent using `SYS_REFCURSOR`:
```sql
-- Oracle
CREATE OR REPLACE PROCEDURE get_employees_refcursor(
    p_dept_id IN NUMBER,
    p_cursor   OUT SYS_REFCURSOR
)
AS
BEGIN
    OPEN p_cursor FOR
        SELECT employee_id, first_name, last_name
        FROM employees WHERE department_id = p_dept_id;
END;
/

DECLARE
    cur SYS_REFCURSOR;
    v_id NUMBER; v_fn VARCHAR2(50); v_ln VARCHAR2(50);
BEGIN
    get_employees_refcursor(5, cur);
    LOOP
        FETCH cur INTO v_id, v_fn, v_ln;
        EXIT WHEN cur%NOTFOUND;
        DBMS_OUTPUT.PUT_LINE(v_id || ' ' || v_fn || ' ' || v_ln);
    END LOOP;
    CLOSE cur;
END;
/
```

---

## Q31: Alter an existing stored procedure.

**Query:**
```sql
-- SQL Server (must drop and recreate)
ALTER PROCEDURE get_employees_by_dept
    @dept_id INT
AS
BEGIN
    SELECT employee_id, first_name, salary
    FROM employees
    WHERE department_id = @dept_id
    ORDER BY salary DESC;
END;

-- MySQL (drop and recreate with DELIMITER)
DROP PROCEDURE IF EXISTS get_employees_by_dept;
DELIMITER //
CREATE PROCEDURE get_employees_by_dept(IN p_dept_id INT)
BEGIN
    SELECT employee_id, first_name, salary
    FROM employees
    WHERE department_id = p_dept_id
    ORDER BY salary DESC;
END //
DELIMITER ;

-- PostgreSQL
CREATE OR REPLACE PROCEDURE get_employees_by_dept(p_dept_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT employee_id, first_name, salary
    FROM employees
    WHERE department_id = p_dept_id
    ORDER BY salary DESC;
END;
$$;
```
**Explanation:** SQL Server and PostgreSQL support `ALTER PROCEDURE` / `CREATE OR REPLACE`. MySQL requires `DROP` followed by `CREATE` since it has no `OR REPLACE` for procedures.

---

## Q32: Drop a stored procedure safely.

**Query:**
```sql
-- SQL Server
DROP PROCEDURE IF EXISTS get_employees_by_dept;

-- MySQL
DROP PROCEDURE IF EXISTS get_employees_by_dept;

-- PostgreSQL
DROP PROCEDURE IF EXISTS get_employees_by_dept;

-- Oracle
BEGIN
    EXECUTE IMMEDIATE 'DROP PROCEDURE get_employees_by_dept';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
```
**Explanation:** `DROP PROCEDURE IF EXISTS` prevents errors if the procedure doesn't exist. Oracle uses dynamic SQL in an anonymous block to handle the "not found" exception gracefully.

---

## Q33: Create a `DETERMINISTIC` function (MySQL).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE FUNCTION calc_tax_rate(p_salary DECIMAL(10,2))
RETURNS DECIMAL(5,2)
DETERMINISTIC
BEGIN
    IF p_salary > 100000 THEN RETURN 0.30;
    ELSEIF p_salary > 50000 THEN RETURN 0.20;
    ELSE RETURN 0.10;
    END IF;
END //
DELIMITER ;

-- Usage
SELECT employee_id, calc_tax_rate(salary) AS tax_rate FROM employees;
```
**Explanation:** `DETERMINISTIC` tells MySQL the function always returns the same result for the same inputs, enabling the optimizer to cache results and avoid redundant calls.

**Alt1:** PostgreSQL marks the same function `IMMUTABLE` for functional indexes:
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION calc_tax_rate(p_salary NUMERIC)
RETURNS NUMERIC
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT CASE
        WHEN p_salary > 100000 THEN 0.30
        WHEN p_salary > 50000  THEN 0.20
        ELSE 0.10
    END;
$$;

SELECT employee_id, calc_tax_rate(salary) AS tax_rate FROM employees;
```

---

## Q34: Demonstrate `STABLE` vs `IMMUTABLE` vs `VOLATILE` functions in PostgreSQL.

**Query:**
```sql
-- IMMUTABLE: pure function, same inputs always give same output, can be used in indexes
CREATE OR REPLACE FUNCTION double_it(p_val INT)
RETURNS INT
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT p_val * 2;
$$;

-- STABLE: same inputs within a single statement, safe for WHERE clauses in indexes
CREATE OR REPLACE FUNCTION current_tax_rate()
RETURNS NUMERIC
LANGUAGE sql
STABLE
AS $$
    SELECT rate FROM tax_config WHERE effective_date <= CURRENT_DATE
    ORDER BY effective_date DESC LIMIT 1;
$$;

-- VOLATILE: can change between calls (default), e.g. NOW(), RANDOM()
CREATE OR REPLACE FUNCTION gen_random_id()
RETURNS INT
LANGUAGE sql
VOLATILE
AS $$
    SELECT (RANDOM() * 1000000)::INT;
$$;

-- Create an index using an IMMUTABLE function
CREATE INDEX idx_double_salary ON employees (double_it(salary));
```
**Explanation:** PostgreSQL uses volatility categories to optimize queries. `IMMUTABLE` enables indexing; `STABLE` avoids repeated evaluation within a query; `VOLATILE` (default) re-evaluates every call.

---

## Q35: Create a function that checks a business rule and returns a boolean.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION can_approve_expense(p_emp_id INT, p_amount NUMERIC)
RETURNS BOOLEAN
LANGUAGE sql
STABLE
AS $$
    SELECT EXISTS (
        SELECT 1 FROM employees
        WHERE employee_id = p_emp_id
          AND salary >= 80000
          AND is_active = TRUE
    )
    AND p_amount <= 10000;
$$;

-- Usage
SELECT employee_id, can_approve_expense(employee_id, 5000) AS can_approve
FROM employees;
```
**Explanation:** Boolean-returning functions encapsulate business rules. `STABLE` is appropriate since the result depends on data that won't change within a single statement.

---

## Q36: Create a procedure that uses a temp table for intermediate results.

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE dept_salary_report
AS
BEGIN
    CREATE TABLE #dept_summary (
        dept_id INT,
        avg_salary DECIMAL(10,2),
        emp_count INT
    );

    INSERT INTO #dept_summary
    SELECT department_id, AVG(salary), COUNT(*)
    FROM employees
    GROUP BY department_id;

    SELECT d.department_name, ts.avg_salary, ts.emp_count
    FROM #dept_summary ts
    JOIN departments d ON d.department_id = ts.dept_id
    ORDER BY ts.avg_salary DESC;

    DROP TABLE #dept_summary;
END;

-- MySQL
DELIMITER //
CREATE PROCEDURE dept_salary_report()
BEGIN
    CREATE TEMPORARY TABLE tmp_dept_summary (
        dept_id INT,
        avg_salary DECIMAL(10,2),
        emp_count INT
    );

    INSERT INTO tmp_dept_summary
    SELECT department_id, AVG(salary), COUNT(*)
    FROM employees
    GROUP BY department_id;

    SELECT d.department_name, t.avg_salary, t.emp_count
    FROM tmp_dept_summary t
    JOIN departments d ON d.department_id = t.dept_id
    ORDER BY t.avg_salary DESC;

    DROP TEMPORARY TABLE tmp_dept_summary;
END //
DELIMITER ;
```
**Explanation:** Temp tables hold intermediate results within a procedure. SQL Server uses `#table`, MySQL uses `TEMPORARY TABLE`, and PostgreSQL uses `CREATE TEMP TABLE`. They are automatically dropped when the session ends.

**Alt1:** PostgreSQL version using `CREATE TEMP TABLE`:
```sql
-- PostgreSQL
CREATE OR REPLACE PROCEDURE dept_salary_report()
LANGUAGE plpgsql
AS $$
BEGIN
    CREATE TEMP TABLE tmp_dept_summary AS
    SELECT department_id, AVG(salary) AS avg_salary, COUNT(*) AS emp_count
    FROM employees GROUP BY department_id;

    SELECT d.department_name, t.avg_salary, t.emp_count
    FROM tmp_dept_summary t
    JOIN departments d ON d.department_id = t.dept_id
    ORDER BY t.avg_salary DESC;

    DROP TABLE tmp_dept_summary;
END;
$$;
```

---

## Q37: Create a procedure that controls transactions with `COMMIT` and `ROLLBACK`.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE PROCEDURE transfer_funds(
    p_from_acct INT,
    p_to_acct INT,
    p_amount NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_balance NUMERIC;
BEGIN
    SELECT balance INTO v_balance FROM accounts WHERE account_id = p_from_acct;

    IF v_balance < p_amount THEN
        RAISE EXCEPTION 'Insufficient funds: balance is %', v_balance;
    END IF;

    UPDATE accounts SET balance = balance - p_amount WHERE account_id = p_from_acct;
    UPDATE accounts SET balance = balance + p_amount WHERE account_id = p_to_acct;

    INSERT INTO txn_log (from_acct, to_acct, amount, txn_date)
    VALUES (p_from_acct, p_to_acct, p_amount, NOW());

    COMMIT;
END;
$$;
```
**Explanation:** PostgreSQL procedures (not functions) can issue `COMMIT`/`ROLLBACK`. Functions cannot commit mid-transaction. If an exception occurs, you can `ROLLBACK` to undo all changes.

---

## Q38: Demonstrate transaction control in SQL Server (nesting transactions).

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE transfer_funds
    @from_acct INT,
    @to_acct INT,
    @amount DECIMAL(10,2)
AS
BEGIN
    SET XACT_ABORT ON;
    BEGIN TRANSACTION;

    BEGIN TRY
        UPDATE accounts SET balance = balance - @amount WHERE account_id = @from_acct;
        UPDATE accounts SET balance = balance + @amount WHERE account_id = @to_acct;
        INSERT INTO txn_log (from_acct, to_acct, amount, txn_date)
        VALUES (@from_acct, @to_acct, @amount, GETDATE());
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
END;
```
**Explanation:** SQL Server procedures manage transactions explicitly. `XACT_ABORT ON` ensures automatic rollback on error. Always check `@@TRANCOUNT > 0` before rolling back to avoid errors.

---

## Q39: Demonstrate transaction control in MySQL (autocommit considerations).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE transfer_funds(
    IN p_from_acct INT,
    IN p_to_acct INT,
    IN p_amount DECIMAL(10,2)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    UPDATE accounts SET balance = balance - p_amount WHERE account_id = p_from_acct;
    UPDATE accounts SET balance = balance + p_amount WHERE account_id = p_to_acct;
    INSERT INTO txn_log (from_acct, to_acct, amount, txn_date)
    VALUES (p_from_acct, p_to_acct, p_amount, NOW());

    COMMIT;
END //
DELIMITER ;
```
**Explanation:** MySQL disables autocommit inside procedures. The `EXIT HANDLER` ensures `ROLLBACK` on any error. `RESIGNAL` re-raises the error to the caller after rollback.

---

## Q40: Wrap a complex business rule in a procedure: `create_employee` with validation.

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE create_employee
    @first NVARCHAR(50),
    @last NVARCHAR(50),
    @email NVARCHAR(100),
    @dept_id INT,
    @salary DECIMAL(10,2),
    @new_id INT OUTPUT
AS
BEGIN
    SET XACT_ABORT ON;

    -- validate inputs
    IF @first IS NULL OR @last IS NULL
        RAISERROR('First and last name are required.', 16, 1);

    IF @salary < 0
        RAISERROR('Salary cannot be negative.', 16, 1);

    IF NOT EXISTS (SELECT 1 FROM departments WHERE department_id = @dept_id)
        RAISERROR('Invalid department ID.', 16, 1);

    IF EXISTS (SELECT 1 FROM employees WHERE email = @email)
        RAISERROR('Email already in use.', 16, 1);

    BEGIN TRANSACTION;
        INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
        VALUES (@first, @last, @email, @dept_id, @salary, GETDATE());
        SET @new_id = SCOPE_IDENTITY();
    COMMIT;

    SELECT @new_id AS new_employee_id;
END;
```
**Explanation:** This procedure validates all inputs before inserting, enforces business invariants, and returns the new ID via an `OUTPUT` parameter. `RAISERROR` with severity 16 signals a user error.

**Alt1:** PostgreSQL version using `RAISE EXCEPTION` for validation and `RETURNING`:
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION create_employee(
    p_first TEXT, p_last TEXT, p_email TEXT,
    p_dept_id INT, p_salary NUMERIC
)
RETURNS INT
LANGUAGE plpgsql
AS $$
DECLARE
    v_new_id INT;
BEGIN
    IF p_first IS NULL OR p_last IS NULL THEN
        RAISE EXCEPTION 'First and last name are required';
    END IF;
    IF p_salary < 0 THEN
        RAISE EXCEPTION 'Salary cannot be negative';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM departments WHERE department_id = p_dept_id) THEN
        RAISE EXCEPTION 'Invalid department ID';
    END IF;
    IF EXISTS (SELECT 1 FROM employees WHERE email = p_email) THEN
        RAISE EXCEPTION 'Email already in use';
    END IF;

    INSERT INTO employees (first_name, last_name, email, department_id, salary, hire_date)
    VALUES (p_first, p_last, p_email, p_dept_id, p_salary, CURRENT_DATE)
    RETURNING employee_id INTO v_new_id;

    RETURN v_new_id;
END;
$$;

SELECT create_employee('Bob', 'Newman', 'bob@corp.com', 5, 85000);
```

---

## Q41: Create a procedure for an ETL step: truncate and reload a summary table.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE PROCEDURE refresh_sales_summary()
LANGUAGE plpgsql
AS $$
BEGIN
    TRUNCATE TABLE sales_summary;

    INSERT INTO sales_summary (region, product_id, total_qty, total_revenue, period)
    SELECT
        s.region,
        od.product_id,
        SUM(od.quantity),
        SUM(od.quantity * od.unit_price),
        DATE_TRUNC('month', s.order_date)
    FROM sales s
    JOIN order_details od ON od.order_id = s.order_id
    GROUP BY s.region, od.product_id, DATE_TRUNC('month', s.order_date);

    COMMIT;
    RAISE NOTICE 'Sales summary refreshed at %', NOW();
END;
$$;
```
**Explanation:** ETL procedures wrap data transformation logic. `TRUNCATE` + `INSERT` is faster than `DELETE` + `INSERT`. The procedure commits the atomic batch and notifies completion.

**Alt1:** SQL Server ETL with staging guard — only reload on new source data:
```sql
-- SQL Server
CREATE PROCEDURE refresh_sales_summary
AS
BEGIN
    SET XACT_ABORT ON;
    BEGIN TRANSACTION;
        TRUNCATE TABLE sales_summary;

        INSERT INTO sales_summary (region, product_id, total_qty, total_revenue, period)
        SELECT s.region, od.product_id,
               SUM(od.quantity),
               SUM(od.quantity * od.unit_price),
               DATEADD(month, DATEDIFF(month, 0, s.order_date), 0)
        FROM sales s
        JOIN order_details od ON od.order_id = s.order_id
        GROUP BY s.region, od.product_id,
                 DATEADD(month, DATEDIFF(month, 0, s.order_date), 0);
    COMMIT;

    SELECT COUNT(*) AS summary_rows FROM sales_summary;
END;
```

---

## Q42: Procedure calling another procedure (nested procedure calls).

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE log_action @action NVARCHAR(200)
AS
BEGIN
    INSERT INTO audit_log (action_text, created_at)
    VALUES (@action, GETDATE());
END;

CREATE PROCEDURE deactivate_employee @emp_id INT
AS
BEGIN
    UPDATE employees SET is_active = 0, termination_date = GETDATE()
    WHERE employee_id = @emp_id;

    EXEC log_action @action = CONCAT('Deactivated employee ', @emp_id);
END;

-- MySQL
DELIMITER //
CREATE PROCEDURE log_action(IN p_action VARCHAR(200))
BEGIN
    INSERT INTO audit_log (action_text, created_at)
    VALUES (p_action, NOW());
END //

CREATE PROCEDURE deactivate_employee(IN p_emp_id INT)
BEGIN
    UPDATE employees SET is_active = 0, termination_date = NOW()
    WHERE employee_id = p_emp_id;

    CALL log_action(CONCAT('Deactivated employee ', p_emp_id));
END //
DELIMITER ;
```
**Explanation:** Procedures can call other procedures to compose reusable logic. `EXEC` (SQL Server) or `CALL` (MySQL) invokes the nested procedure. Keep call depth reasonable to avoid stack issues.

---

## Q43: Create a procedure that returns multiple result sets (SQL Server).

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE get_org_overview
AS
BEGIN
    -- Result set 1: department summary
    SELECT d.department_name, COUNT(e.employee_id) AS headcount
    FROM departments d
    LEFT JOIN employees e ON e.department_id = d.department_id
    GROUP BY d.department_name;

    -- Result set 2: top earners
    SELECT TOP 10 first_name, last_name, salary
    FROM employees
    ORDER BY salary DESC;

    -- Result set 3: recent hires
    SELECT TOP 10 first_name, last_name, hire_date
    FROM employees
    ORDER BY hire_date DESC;
END;
```
**Explanation:** SQL Server procedures can return multiple result sets by having multiple `SELECT` statements. The client application processes each result set sequentially.

---

## Q44: Return multiple result sets from a procedure (MySQL).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE get_org_overview()
BEGIN
    -- Result set 1
    SELECT d.department_name, COUNT(e.employee_id) AS headcount
    FROM departments d
    LEFT JOIN employees e ON e.department_id = d.department_id
    GROUP BY d.department_name;

    -- Result set 2
    SELECT first_name, last_name, salary
    FROM employees
    ORDER BY salary DESC
    LIMIT 10;
END //
DELIMITER ;

-- Call it
CALL get_org_overview();
```
**Explanation:** MySQL procedures also support multiple result sets. The client must consume each result set before accessing the next. `CALL` returns all result sets.

---

## Q45: Demonstrate privilege requirements for executing procedures.

**Query:**
```sql
-- Grant execute privilege on a procedure
-- MySQL
GRANT EXECUTE ON PROCEDURE get_employees_by_dept TO 'analyst_user'@'localhost';

-- PostgreSQL
GRANT EXECUTE ON PROCEDURE get_employees_by_dept TO analyst_user;

-- SQL Server
GRANT EXECUTE ON get_employees_by_dept TO analyst_user;

-- Revoke
-- MySQL
REVOKE EXECUTE ON PROCEDURE get_employees_by_dept FROM 'analyst_user'@'localhost';

-- PostgreSQL
REVOKE EXECUTE ON PROCEDURE get_employees_by_dept FROM analyst_user;

-- SQL Server
REVOKE EXECUTE ON get_employees_by_dept FROM analyst_user;
```
**Explanation:** By default, only the procedure owner can execute it. `GRANT EXECUTE` allows specific users or roles to call the procedure. This supports the principle of least privilege.

---

## Q46: Demonstrate SQL injection inside dynamic SQL and how to prevent it.

**Query:**
```sql
-- UNSAFE: vulnerable to SQL injection
-- MySQL
DELIMITER //
CREATE PROCEDURE unsafe_search(IN p_name VARCHAR(100))
BEGIN
    SET @sql = CONCAT('SELECT * FROM employees WHERE name = ''', p_name, '''');
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;
-- An attacker could pass: ' OR '1'='1' --

-- SAFE: using bind variables
DELIMITER //
CREATE PROCEDURE safe_search(IN p_name VARCHAR(100))
BEGIN
    SET @sql = 'SELECT * FROM employees WHERE name = ?';
    SET @p = p_name;
    PREPARE stmt FROM @sql;
    EXECUTE stmt USING @p;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

-- SAFE: SQL Server with sp_executesql
CREATE PROCEDURE safe_search @name NVARCHAR(100)
AS
BEGIN
    DECLARE @sql NVARCHAR(MAX) = N'SELECT * FROM employees WHERE name = @p_name';
    EXEC sp_executesql @sql, N'@p_name NVARCHAR(100)', @p_name = @name;
END;
```
**Explanation:** Concatenating user input into SQL strings creates injection vulnerabilities. Always use parameterized queries (`?` / `@param`) to bind values safely.

---

## Q47: Use `QUOTENAME` and `DBMS_ASSERT` to safely use dynamic identifiers.

**Query:**
```sql
-- SQL Server: QUOTENAME wraps identifiers in brackets
CREATE PROCEDURE safe_column_sort
    @table NVARCHAR(128),
    @column NVARCHAR(128),
    @direction NVARCHAR(4) = 'ASC'
AS
BEGIN
    DECLARE @sql NVARCHAR(MAX);
    SET @sql = N'SELECT * FROM ' + QUOTENAME(@table)
             + N' ORDER BY ' + QUOTENAME(@column) + N' '
             + CASE WHEN @direction IN ('ASC','DESC') THEN @direction ELSE 'ASC' END;
    EXEC sp_executesql @sql;
END;

-- Oracle: DBMS_ASSERT validates identifiers
CREATE OR REPLACE PROCEDURE safe_column_sort(
    p_table    IN VARCHAR2,
    p_column   IN VARCHAR2,
    p_direction IN VARCHAR2 DEFAULT 'ASC'
)
AS
    v_sql VARCHAR2(1000);
BEGIN
    v_sql := 'SELECT * FROM '
          || DBMS_ASSERT.SQL_OBJECT_NAME(p_table)
          || ' ORDER BY '
          || DBMS_ASSERT.SQL_OBJECT_NAME(p_column)
          || ' '
          || CASE WHEN p_direction IN ('ASC','DESC') THEN p_direction ELSE 'ASC' END;
    EXECUTE IMMEDIATE v_sql;
END;
/
```
**Explanation:** `QUOTENAME` (SQL Server) and `DBMS_ASSERT.SQL_OBJECT_NAME` (Oracle) sanitize identifiers. Additionally validate `direction` via `CASE` to prevent injection through non-identifier parts.

---

## Q48: Demonstrate procedure caching and recompilation in SQL Server.

**Query:**
```sql
-- SQL Server: Force recompilation with RECOMPILE option
CREATE PROCEDURE get_employees_filtered
    @dept_id INT = NULL,
    @min_salary DECIMAL(10,2) = NULL
WITH RECOMPILE
AS
BEGIN
    SELECT * FROM employees
    WHERE (@dept_id IS NULL OR department_id = @dept_id)
      AND (@min_salary IS NULL OR salary >= @min_salary);
END;

-- Recompile a specific procedure
EXEC sp_recompile 'get_employees_filtered';

-- Check procedure cache usage
SELECT objtype, cacheobjtype, objname, uses
FROM sys.dm_exec_cached_plans cp
CROSS APPLY sys.dm_exec_plan_attributes(cp.plan_handle) pa
JOIN sys.objects o ON o.object_id = pa.value
WHERE o.name = 'get_employees_filtered';
```
**Explanation:** `WITH RECOMPILE` forces a new execution plan on every call — useful for procedures with highly variable parameter distributions. `sp_recompile` marks a procedure for recompilation on its next call.

---

## Q49: Demonstrate the `NOCOMPILE` option in MySQL 8.0+.

**Query:**
```sql
-- MySQL 8.0+: store procedure without caching the plan
DELIMITER //
CREATE PROCEDURE get_employees_by_dept(IN p_dept_id INT)
SQL SECURITY DEFINER
NOT DETERMINISTIC
READS SQL DATA
BEGIN
    SELECT * FROM employees WHERE department_id = p_dept_id;
END //
DELIMITER ;

-- Check procedure characteristics
SHOW CREATE PROCEDURE get_employees_by_dept;
```
**Explanation:** MySQL's `CREATE PROCEDURE` does not have an explicit `NOCOMPILE` directive like SQL Server, but the `NOT DETERMINISTIC` / `READS SQL DATA` annotations guide the optimizer. MySQL generally re-parses SQL on each call.

---

## Q50: Create a `DETERMINISTIC` function that can be used in an index (MySQL).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE FUNCTION lower_name(p_name VARCHAR(100))
RETURNS VARCHAR(100)
DETERMINISTIC
READS SQL DATA
BEGIN
    RETURN LOWER(p_name);
END //
DELIMITER ;

-- Create a functional index using the function
ALTER TABLE employees ADD INDEX idx_lower_name ((lower_name(last_name)));

-- Use the index
SELECT * FROM employees WHERE lower_name(last_name) = 'smith';
```
**Explanation:** A `DETERMINISTIC` function enables MySQL to create functional indexes. The double parentheses `(())` in `CREATE INDEX` are MySQL's syntax for expression indexes.

---

## Q51: Create a function with a `FOR` loop in PL/pgSQL.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION sum_series(p_max INT)
RETURNS INT
LANGUAGE plpgsql
AS $$
DECLARE
    v_total INT := 0;
BEGIN
    FOR v_i IN 1..p_max LOOP
        v_total := v_total + v_i;
    END LOOP;
    RETURN v_total;
END;
$$;

SELECT sum_series(10); -- 55

-- With STEP
CREATE OR REPLACE FUNCTION sum_even(p_max INT)
RETURNS INT
LANGUAGE plpgsql
AS $$
DECLARE
    v_total INT := 0;
BEGIN
    FOR v_i IN 0..p_max BY 2 LOOP
        v_total := v_total + v_i;
    END LOOP;
    RETURN v_total;
END;
$$;
```
**Explanation:** PL/pgSQL supports numeric `FOR` loops with optional `BY` step. The loop variable is automatically declared and scoped to the loop.

---

## Q52: Use a `FOR` loop to query rows in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION process_active_employees()
RETURNS VOID
LANGUAGE plpgsql
AS $$
DECLARE
    emp RECORD;
BEGIN
    FOR emp IN SELECT employee_id, first_name, last_name
               FROM employees WHERE is_active = TRUE
    LOOP
        INSERT INTO employee_log (emp_id, emp_name, processed_at)
        VALUES (emp.employee_id, emp.first_name || ' ' || emp.last_name, NOW());
    END LOOP;
END;
$$;
```
**Explanation:** A `FOR ... IN SELECT` loop iterates over query results without an explicit cursor — PL/pgSQL manages opening, fetching, and closing internally.

---

## Q53: Create an Oracle procedure using a `FOR` loop.

**Query:**
```sql
-- Oracle
CREATE OR REPLACE PROCEDURE process_departments
AS
BEGIN
    FOR dept_rec IN (
        SELECT department_id, department_name FROM departments
    )
    LOOP
        DBMS_OUTPUT.PUT_LINE('Dept ' || dept_rec.department_id || ': '
                            || dept_rec.department_name);
    END LOOP;
END;
/

BEGIN
    process_departments;
END;
/
```
**Explanation:** Oracle's `FOR ... IN` loop uses an implicit cursor and record; no explicit `OPEN`/`FETCH`/`CLOSE` is required. `DBMS_OUTPUT` prints to the console.

---

## Q54: Use a `LOOP` with a `LEAVE` condition in MySQL.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE countdown(IN p_start INT)
BEGIN
    DECLARE v_count INT DEFAULT p_start;

    my_loop: LOOP
        IF v_count = 0 THEN
            LEAVE my_loop;
        END IF;
        SELECT v_count AS current_value;
        SET v_count = v_count - 1;
    END LOOP;
END //
DELIMITER ;

CALL countdown(5);
```
**Explanation:** MySQL's bare `LOOP` has no built-in exit condition; label the loop and use `LEAVE label` to exit. This gives full control over iteration.

---

## Q55: Create a trigger-like audit function using a stored function (MySQL).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE FUNCTION audit_username()
RETURNS VARCHAR(100)
NO SQL
BEGIN
    RETURN COALESCE(@audit_user, CURRENT_USER());
END //
DELIMITER ;

-- Use it as a default value
ALTER TABLE employees
    MODIFY COLUMN created_by VARCHAR(100) DEFAULT (audit_username());
```
**Explanation:** Nondeterministic functions can capture session context. `NO SQL` declares the function doesn't read or write data, which is required for use in column defaults in MySQL.

---

## Q56: Create a scalar function that uses other functions (composable functions).

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION redact_name(p_name TEXT)
RETURNS TEXT
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT CASE
        WHEN p_name IS NULL THEN NULL
        ELSE LEFT(p_name, 1) || repeat('*', GREATEST(LENGTH(p_name) - 1, 0))
    END;
$$;

CREATE OR REPLACE FUNCTION employee_display_row(p_first TEXT, p_last TEXT)
RETURNS TEXT
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT redact_name(p_first) || ' ' || redact_name(p_last);
$$;

SELECT employee_display_row('Alice', 'Wonderland');
```
**Explanation:** Functions can call other functions, promoting reuse. Marking both `IMMUTABLE` lets PostgreSQL inline or optimize the composed call chains.

---

## Q57: Create a procedure with `RAISE NOTICE` / `RAISE EXCEPTION` in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE PROCEDURE apply_raise(
    p_emp_id INT,
    p_pct NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_salary NUMERIC;
BEGIN
    IF p_pct < 0 OR p_pct > 1 THEN
        RAISE EXCEPTION 'Invalid raise percent: % (must be between 0 and 1)', p_pct
            USING HINT = 'Use a decimal fraction, e.g. 0.10 for 10%';
    END IF;

    SELECT salary INTO v_salary FROM employees WHERE employee_id = p_emp_id;

    RAISE NOTICE 'Applied % percent raise to employee % (old salary: %)',
        p_pct * 100, p_emp_id, v_salary;

    UPDATE employees
    SET salary = salary * (1 + p_pct)
    WHERE employee_id = p_emp_id;
END;
$$;
```
**Explanation:** `RAISE EXCEPTION` aborts the transaction with a user-defined error; `RAISE NOTICE` logs an informational message. `USING HINT` attaches guidance to the error.

---

## Q58: Handle SQL Server errors with `THROW` instead of `RAISERROR`.

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE validate_hire_date @hire_date DATE
AS
BEGIN
    IF @hire_date > GETDATE()
        THROW 50001, 'Hire date cannot be in the future.', 1;

    IF YEAR(@hire_date) < 1900
        THROW 50002, 'Hire date is before the earliest allowed date.', 1;

    SELECT 'Hire date is valid.' AS status;
END;
```
**Explanation:** `THROW` is the modern SQL Server error mechanism. It aborts the batch and sets `XACT_STATE` to uncommittable unless handled in `CATCH`. `RAISERROR` is deprecated for new code.

---

## Q59: Create a procedure that returns a dataset as XML or JSON (SQL Server).

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE get_departments_json
AS
BEGIN
    SELECT d.department_name,
           (SELECT e.employee_id, e.first_name, e.salary
            FROM employees e
            WHERE e.department_id = d.department_id
            FOR JSON PATH) AS employees_json
    FROM departments d
    FOR JSON PATH;
END;

-- Call to get JSON output
EXEC get_departments_json;
```
**Explanation:** `FOR JSON PATH` serializes a result set to JSON, allowing procedures to return structured data for APIs. SQL Server 2016+ supports JSON output directly.

---

## Q60: Create an Oracle procedure that returns a dataset (pipelined function).

**Query:**
```sql
-- Oracle
CREATE OR REPLACE TYPE emp_row AS OBJECT (
    emp_id NUMBER,
    emp_name VARCHAR2(100)
);
/

CREATE OR REPLACE TYPE emp_tab AS TABLE OF emp_row;
/

CREATE OR REPLACE FUNCTION get_emp_rows(p_dept_id IN NUMBER)
RETURN emp_tab PIPELINED
AS
BEGIN
    FOR rec IN (SELECT employee_id, first_name || ' ' || last_name AS name
                FROM employees WHERE department_id = p_dept_id)
    LOOP
        PIPE ROW (emp_row(rec.employee_id, rec.name));
    END LOOP;
    RETURN;
END;
/

-- Use in SQL
SELECT * FROM TABLE(get_emp_rows(5));
```
**Explanation:** Pipelined functions stream rows one at a time without buffering, and can be queried like a table with `TABLE()`. This is Oracle's table-valued function equivalent.

---

## Q61: Pass a table type as a parameter in SQL Server (table-valued parameter).

**Query:**
```sql
-- SQL Server
CREATE TYPE dept_members AS TABLE
(
    employee_id INT,
    role NVARCHAR(50)
);

CREATE PROCEDURE bulk_add_project_members
    @project_id INT,
    @members dept_members READONLY
AS
BEGIN
    INSERT INTO project_members (project_id, employee_id, role)
    SELECT @project_id, employee_id, role FROM @members;
END;

-- Usage
DECLARE @members dept_members;
INSERT INTO @members VALUES (101, 'Developer'), (102, 'QA');
EXEC bulk_add_project_members @project_id = 7, @members = @members;
```
**Explanation:** Table-valued parameters let you pass multi-row data into a procedure. The parameter must be `READONLY`; the client (e.g., .NET) passes arrays as TVPs.

---

## Q62: Create a function that returns the nth highest salary.

**Query:**
```sql
-- SQL Server
CREATE FUNCTION get_nth_salary(@n INT)
RETURNS DECIMAL(10,2)
AS
BEGIN
    DECLARE @result DECIMAL(10,2);
    SELECT @result = salary
    FROM (
        SELECT DISTINCT salary,
               DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
        FROM employees
    ) ranked
    WHERE rnk = @n;
    RETURN @result;
END;

SELECT dbo.get_nth_salary(3) AS third_highest_salary;

-- PostgreSQL
CREATE OR REPLACE FUNCTION get_nth_salary(p_n INT)
RETURNS NUMERIC
LANGUAGE sql
STABLE
AS $$
    SELECT DISTINCT salary
    FROM employees
    ORDER BY salary DESC
    LIMIT 1 OFFSET p_n - 1;
$$;
```
**Explanation:** Window functions (`DENSE_RANK`) or `OFFSET` give the Nth-highest value. Wrapping the logic in a function makes it reusable and testable.

---

## Q63: Demonstrate `REFCURSOR` returning to a .NET/Python-style client in SQL Server using output parameters.

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE get_dept_info
    @dept_id INT,
    @dept_name NVARCHAR(100) OUTPUT,
    @emp_count INT OUTPUT,
    @curs CURSOR VARYING OUTPUT
AS
BEGIN
    SELECT @dept_name = department_name
    FROM departments WHERE department_id = @dept_id;

    SET @emp_count = (SELECT COUNT(*) FROM employees WHERE department_id = @dept_id);

    SET @curs = CURSOR FOR
        SELECT employee_id, first_name, last_name FROM employees WHERE department_id = @dept_id;
    OPEN @curs;
END;

-- Caller fetches from the returned cursor
DECLARE @c CURSOR;
DECLARE @name NVARCHAR(100), @count INT;
EXEC get_dept_info @dept_id = 5, @dept_name = @name OUTPUT, @emp_count = @count OUTPUT, @curs = @c OUTPUT;
SELECT @name AS dept_name, @count AS emp_count;
WHILE @@FETCH_STATUS = 0
BEGIN
    FETCH NEXT FROM @c;
END;
CLOSE @c;
DEALLOCATE @c;
```
**Explanation:** SQL Server supports `CURSOR VARYING OUTPUT` for returning a cursor result set to the caller. This is the SQL Server cousin of PostgreSQL's `REFCURSOR`.

---

## Q64: Demonstrate recursive procedure calls in PostgreSQL.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION factorial_rec(p_n INT)
RETURNS BIGINT
LANGUAGE plpgsql
IMMUTABLE
AS $$
BEGIN
    IF p_n <= 1 THEN
        RETURN 1;
    ELSE
        RETURN p_n * factorial_rec(p_n - 1);
    END IF;
END;
$$;

SELECT factorial_rec(10); -- 3628800
```
**Explanation:** Functions can call themselves recursively. PostgreSQL allows recursion depth. `IMMUTABLE` marks this pure function as cacheable; recursion should have a well-defined base case.

---

## Q65: Use a procedure with `SQL SECURITY DEFINER` in MySQL.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE DEFINER = 'admin'@'localhost'
PROCEDURE get_employee_salary(IN p_emp_id INT, OUT p_salary DECIMAL(10,2))
SQL SECURITY DEFINER
BEGIN
    SELECT salary INTO p_salary FROM employees WHERE employee_id = p_emp_id;
END //
DELIMITER ;

-- Grant EXECUTE to a limited user
GRANT EXECUTE ON PROCEDURE get_employee_salary TO 'bi_user'@'localhost';
```
**Explanation:** `SQL SECURITY DEFINER` executes the procedure with the definer's privileges, letting low-privilege users run procedure logic without direct table access. `SQL SECURITY INVOKER` runs with the caller's privileges. Similarly, PostgreSQL uses `SECURITY DEFINER` in `CREATE FUNCTION` (default is `INVOKER`). 

**Alt1:** PostgreSQL equivalent:
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION get_employee_salary(p_emp_id INT)
RETURNS NUMERIC
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
STABLE
AS $$
DECLARE
    v_salary NUMERIC;
BEGIN
    SELECT salary INTO v_salary FROM employees WHERE employee_id = p_emp_id;
    RETURN v_salary;
END;
$$;
```

---

## Q66: Track procedure execution times with `GETDATE()` timestamps.

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE monitored_etl_run
AS
BEGIN
    DECLARE @start DATETIME = GETDATE();
    DECLARE @rows INT;

    INSERT INTO sales_summary (region, total, period)
    SELECT region, SUM(amount), CAST(order_date AS DATE)
    FROM sales GROUP BY region, CAST(order_date AS DATE);
    SET @rows = @@ROWCOUNT;

    INSERT INTO etl_audit (proc_name, rows_affected, duration_ms, started_at)
    VALUES ('monitored_etl_run', @rows, DATEDIFF(ms, @start, GETDATE()), @start);
END;
```
**Explanation:** Capture `@@ROWCOUNT` and `DATEDIFF` before/after the operation to audit ETL performance. This is a lightweight observability pattern inside procedures.

---

## Q67: Create a procedure with a `WHILE` loop and nested `TRY/CATCH` in SQL Server.

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE batch_upsert_temp
AS
BEGIN
    DECLARE @retry INT = 0;
    DECLARE @i INT = 1;

    WHILE @i <= 3
    BEGIN
        BEGIN TRY
            BEGIN TRANSACTION;
                INSERT INTO target_table
                SELECT * FROM source_table WHERE batch_id = @i;
                UPDATE batch_tracker SET status = 'done' WHERE batch_id = @i;
            COMMIT TRANSACTION;
            SET @i = @i + 1;
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION;
            SET @retry = @retry + 1;
            SELECT @retry AS retry_attempt, ERROR_NUMBER() AS err_no;
        END CATCH;
    END;
END;
```
**Explanation:** Nested loops with `TRY/CATCH` implement retry patterns with rollback. Each batch is a separate transaction so failures don't poison the whole run.

---

## Q68: Implement a fuzzy search stored function using `LIKE`.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE FUNCTION matches_pattern(p_value VARCHAR(255), p_pattern VARCHAR(255))
RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    RETURN p_value LIKE CONCAT('%', p_pattern, '%');
END //
DELIMITER ;

-- Pass-through to procedure
DELIMITER //
CREATE PROCEDURE search_customers(IN p_criteria VARCHAR(255))
BEGIN
    SELECT customer_id, name, email
    FROM customers
    WHERE matches_pattern(name, p_criteria)
       OR matches_pattern(email, p_criteria);
END //
DELIMITER ;

CALL search_customers('smith');
```
**Explanation:** Encapsulating `LIKE` logic in a deterministic function centralizes the matching rule. Note `%`-based `LIKE` can't use a btree index, so this suits small reference tables.

---

## Q69: Create an Oracle procedure using `MERGE` for upsert.

**Query:**
```sql
-- Oracle
CREATE OR REPLACE PROCEDURE upsert_customer(
    p_id        IN customers.customer_id%TYPE,
    p_name      IN customers.name%TYPE,
    p_email     IN customers.email%TYPE
)
AS
BEGIN
    MERGE INTO customers c
    USING (SELECT p_id AS customer_id FROM DUAL) src
    ON (c.customer_id = src.customer_id)
    WHEN MATCHED THEN
        UPDATE SET c.name = p_name, c.email = p_email
    WHEN NOT MATCHED THEN
        INSERT (customer_id, name, email, created_at)
        VALUES (p_id, p_name, p_email, SYSDATE);

    DBMS_OUTPUT.PUT_LINE('Upserted customer ' || p_id);
END;
/
```
**Explanation:** `MERGE` performs conditional insert-or-update in one statement. Using `%TYPE` attributes ties parameter types to the table columns, keeping signatures in sync.

---

## Q70: Create a procedure that uses `MERGE` in SQL Server (upsert pattern).

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE upsert_product
    @product_id INT,
    @name NVARCHAR(100),
    @price DECIMAL(10,2)
AS
BEGIN
    SET XACT_ABORT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
            MERGE products AS target
            USING (SELECT @product_id, @name, @price) AS source (product_id, name, price)
            ON (target.product_id = source.product_id)
            WHEN MATCHED THEN
                UPDATE SET name = source.name, price = source.price
            WHEN NOT MATCHED THEN
                INSERT (product_id, name, price) VALUES (source.product_id, source.name, source.price);
        COMMIT;
    END TRY
    BEGIN CATCH
        ROLLBACK;
        THROW;
    END CATCH;
END;
```
**Explanation:** Same `MERGE` pattern in SQL Server; note the `USING` clause requires an aliased source. `ROLLBACK` in `CATCH` plus `THROW` preserves the error while undoing partial work.

---

## Q71: Create a procedure using a temporary table with a `WHILE` loop for daily aggregation.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE generate_daily_report(IN p_start_date DATE, IN p_end_date DATE)
BEGIN
    CREATE TEMPORARY TABLE tmp_daily (
        txn_date DATE,
        total_sales DECIMAL(14,2),
        txn_count INT
    );

    WHILE p_start_date <= p_end_date DO
        INSERT INTO tmp_daily
        SELECT p_start_date,
               COALESCE(SUM(amount), 0),
               COUNT(*)
        FROM sales WHERE txn_date = p_start_date;
        SET p_start_date = DATE_ADD(p_start_date, INTERVAL 1 DAY);
    END WHILE;

    SELECT * FROM tmp_daily ORDER BY txn_date;
    DROP TEMPORARY TABLE tmp_daily;
END //
DELIMITER ;
```
**Explanation:** The while-loop fills a temporary table day by day, guaranteeing a row even for zero-sale days. Temp tables are scoped to the session and auto-dropped on disconnect.

---

## Q72: Handle `NULL` and empty sets inside procedures safely.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION avg_salary_or_zero(p_dept_id INT)
RETURNS NUMERIC
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
    v_avg NUMERIC;
BEGIN
    SELECT AVG(salary) INTO v_avg
    FROM employees WHERE department_id = p_dept_id;

    RETURN COALESCE(v_avg, 0);
END;
$$;

-- Test no employees / no rows
SELECT avg_salary_or_zero(999) AS result; -- 0 instead of NULL
```
**Explanation:** `SELECT INTO` leaves a variable `NULL` when no rows match. `COALESCE` provides a safe fallback so downstream logic never receives an unexpected `NULL`.

---

## Q73: Create a procedure that dynamically renames a column (safe dynamic DDL).

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE rename_column_safe
    @table NVARCHAR(128),
    @new_name NVARCHAR(128)
AS
BEGIN
    DECLARE @old_name NVARCHAR(128);
    SELECT @old_name = name
    FROM sys.columns
    WHERE object_id = OBJECT_ID(@table) AND column_id = 2; -- 2nd column

    IF @old_name IS NULL
    BEGIN
        THROW 51000, 'Could not determine source column.', 1;
    END;

    DECLARE @sql NVARCHAR(MAX) = N'EXEC sp_rename '''
        + QUOTENAME(@table) + '.' + QUOTENAME(@old_name)
        + ''', ''' + @new_name + ''', ''COLUMN'';';

    EXEC sp_executesql @sql;
END;
```
**Explanation:** Dynamic DDL driven by catalog metadata prevents injection because identifiers come from the system catalog, not directly from the user. `sp_rename` renames the column.

---

## Q74: Create an Oracle function using `NVL` and `IF` logic.

**Query:**
```sql
-- Oracle
CREATE OR REPLACE FUNCTION format_salary(p_salary IN NUMBER)
RETURN VARCHAR2
AS
    v_text VARCHAR2(50) := NULL; 
BEGIN
    IF p_salary IS NULL THEN
        v_text := 'N/A';
    ELSIF p_salary >= 1000000 THEN
        v_text := 'Salary: ' || TO_CHAR(ROUND(p_salary/1000000, 1)) || 'M';
    ELSE
        v_text := 'Salary: ' || TO_CHAR(p_salary, 'FM$999,999,999');
    END IF;

    RETURN v_text;
END;
/
```
**Explanation:** `IF`/`ELSIF` branch inside Oracle functions. The `:=' operator initializes the local variable; `TO_CHAR` formats numbers and `NVL`/`COALESCE` patterns guard nulls.

---

## Q75: Demonstrate check constraints vs. procedure-enforced rules with `SIGNAL` (MySQL).

**Query:**
```sql
-- MySQL 8.0+: CREATE procedure that raises user-defined errors with SIGNAL
DELIMITER //
CREATE PROCEDURE set_employee_salary(IN p_emp_id INT, IN p_new_salary DECIMAL(10,2))
BEGIN
    IF p_new_salary <= 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Salary must be positive',
                MYSQL_ERRNO = 1001;
    END IF;

    IF EXISTS (SELECT 1 FROM salary_changes
               WHERE employee_id = p_emp_id AND effective_date = CURDATE()) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Salary already updated today';
    END IF;

    UPDATE employees SET salary = p_new_salary WHERE employee_id = p_emp_id;
    INSERT INTO salary_changes (employee_id, effective_date, new_salary)
    VALUES (p_emp_id, CURDATE(), p_new_salary);
END //
DELIMITER ;
```
**Explanation:** `SIGNAL` raises a user-defined exception with a custom message. This lets procedures enforce business rules that go beyond simple `CHECK` constraints, such as "one raise per day."

**Alt1:** Use `SIGNAL` with a variable message:
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE require_field(IN p_value VARCHAR(255), IN p_field_name VARCHAR(50))
BEGIN
    IF p_value IS NULL OR p_value = '' THEN
        SET @msg = CONCAT('Field "', p_field_name, '" is required');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = @msg;
    END IF;
END //
DELIMITER ;
```

---

## Q76: Create a procedure that uses a stored function to generate a unique employee code.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION make_emp_code(p_dept TEXT, p_seq INT)
RETURNS TEXT
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT UPPER(LEFT(p_dept, 3)) || '-' || LPAD(p_seq::TEXT, 4, '0');
$$;

CREATE OR REPLACE PROCEDURE add_employee(
    p_first TEXT, p_last TEXT, p_dept TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_seq INT;
    v_code TEXT;
BEGIN
    SELECT COALESCE(MAX(employee_id), 0) + 1 INTO v_seq FROM employees;
    v_code := make_emp_code(p_dept, v_seq);

    INSERT INTO employees (employee_code, first_name, last_name)
    VALUES (v_code, p_first, p_last);
END;
$$;
```
**Explanation:** Composing small pure functions (e.g., code generators) inside procedures keeps logic testable. In real apps, use a SEQUENCE rather than `MAX+1` for concurrency safety.

---

## Q77: Create a procedure to page results using `OFFSET/FETCH`.

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE get_emp_page
    @page_size INT,
    @page_num INT
AS
BEGIN
    DECLARE @offset INT = (@page_num - 1) * @page_size;

    SELECT employee_id, first_name, last_name, salary
    FROM employees
    ORDER BY employee_id
    OFFSET @offset ROWS
    FETCH NEXT @page_size ROWS ONLY;
END;

EXEC get_emp_page @page_size = 20, @page_num = 3;
```
**Explanation:** `OFFSET/FETCH` (SQL Server 2012+) provides reliable pagination; the procedure hides offset math from callers. MySQL uses `LIMIT offset, size` and PostgreSQL uses `LIMIT/OFFSET` instead.

**Alt1:** MySQL/PostgreSQL variant:
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE get_emp_page(IN p_page_size INT, IN p_page_num INT)
BEGIN
    SELECT employee_id, first_name, last_name, salary
    FROM employees
    ORDER BY employee_id
    LIMIT p_page_size OFFSET (p_page_num - 1) * p_page_size;
END //
DELIMITER ;

-- PostgreSQL
CREATE OR REPLACE PROCEDURE get_emp_page(p_page_size INT, p_page_num INT)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT employee_id, first_name, last_name, salary
    FROM employees
    ORDER BY employee_id
    LIMIT p_page_size OFFSET (p_page_num - 1) * p_page_size;
END;
$$;
```

---

## Q78: Use `RESIGNAL` in MySQL to re-throw an exception after handling.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE guarded_update(IN p_emp_id INT, IN p_salary DECIMAL(10,2))
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- log the failure then propagate
        INSERT INTO error_log (occurred_at, message)
        VALUES (NOW(), 'guarded_update failed');
        RESIGNAL;
    END;

    UPDATE employees SET salary = p_salary WHERE employee_id = p_emp_id;
END //
DELIMITER ;
```
**Explanation:** `RESIGNAL` re-raises the current error after the handler does cleanup, so the caller still sees the original failure. Without it, the handler would swallow the exception.

---

## Q79: Create a stacked exception handler with `CONTINUE` in MySQL.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE seed_if_empty()
BEGIN
    DECLARE v_done BOOLEAN DEFAULT FALSE;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = TRUE;

    IF NOT EXISTS (SELECT 1 FROM config WHERE param = 'seed') THEN
        INSERT INTO config (param, value) VALUES ('seed', 'done');
    END IF;

    SELECT 'Config checked.' AS status;
END //
DELIMITER ;
```
**Explanation:** `CONTINUE HANDLER` executes its statements, then the procedure continues at the next statement (unlike `EXIT HANDLER`). `NOT FOUND` triggers on end-of-resultset, useful for cursor-style loops.

---

## Q80: Create a procedure with a `FOREIGN KEY` friendly delete using `IF EXISTS`.

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE delete_department_safe @dept_id INT
AS
BEGIN
    IF EXISTS (SELECT 1 FROM employees WHERE department_id = @dept_id)
    BEGIN
        THROW 50001, 'Cannot delete department with active employees.', 1;
    END;

    DELETE FROM departments WHERE department_id = @dept_id;
    IF @@ROWCOUNT = 0
        THROW 50002, 'Department not found.', 1;
END;
```
**Explanation:** Checking dependent rows before delete prevents FK violations, and `@@ROWCOUNT = 0` detects a missing row. This procedural guard is clearer than relying on raw FK errors.

**Alt1:** MySQL equivalent with `HANDLER`:
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE delete_department_safe(IN p_dept_id INT)
BEGIN
    DECLARE EXIT HANDLER FOR 1451
    BEGIN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Cannot delete; department has employees';
    END;

    DELETE FROM departments WHERE department_id = p_dept_id;
    IF ROW_COUNT() = 0 THEN
        SELECT 'Department not found.' AS warning;
    END IF;
END //
DELIMITER ;
```

---

## Q81: Create a procedure that conditionally `COMMIT` or `ROLLBACK` based on row counts.

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE import_batch_if_valid @batch_id INT
AS
BEGIN
    BEGIN TRANSACTION;
        INSERT INTO staging_audit (batch_id) VALUES (@batch_id);

        DELETE FROM staging_audit WHERE batch_id = @batch_id AND source_line IS NULL;

        IF @@ROWCOUNT > 100
        BEGIN
            ROLLBACK TRANSACTION;
            THROW 51000, 'Batch failed validation: too many bad rows.', 1;
        END;

        INSERT INTO final_data
        SELECT * FROM staging WHERE batch_id = @batch_id;
    COMMIT TRANSACTION;
END;
```
**Explanation:** The procedure inspects validation results inside the transaction and decides between `COMMIT` and `ROLLBACK`, keeping the atomic import self-contained.

---

## Q82: Use `GET DIAGNOSTICS` in PostgreSQL to capture affected row counts.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE PROCEDURE archive_old_sales(p_before DATE)
LANGUAGE plpgsql
AS $$
DECLARE
    v_archived INT;
BEGIN
    INSERT INTO sales_archive SELECT * FROM sales WHERE txn_date < p_before;

    GET DIAGNOSTICS v_archived = ROW_COUNT;

    DELETE FROM sales WHERE txn_date < p_before;

    RAISE NOTICE 'Archived % rows', v_archived;
END;
$$;
```
**Explanation:** `GET DIAGNOSTICS ... ROW_COUNT` reports how many rows the last statement affected, giving the procedure visibility into its own work for logging or branching.

---

## Q83: Create a procedure that guards against duplicate concurrent inserts in MySQL.

**Query:**
```sql
-- MySQL (using GET_LOCK for a named lock / advisory lock)
DELIMITER //
CREATE PROCEDURE create_customer_unique(IN p_email VARCHAR(255), IN p_name VARCHAR(255))
BEGIN
    DECLARE v_lock_result INT;
    SELECT GET_LOCK('customer_insert_lock', 5) INTO v_lock_result;

    IF v_lock_result = 1 THEN
        IF NOT EXISTS (SELECT 1 FROM customers WHERE email = p_email) THEN
            INSERT INTO customers (email, name) VALUES (p_email, p_name);
            SELECT 'Inserted' AS status;
        ELSE
            SELECT 'Duplicate email, skipped' AS status;
        END IF;
        SELECT RELEASE_LOCK('customer_insert_lock');
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Could not acquire lock';
    END IF;
END //
DELIMITER ;
```
**Explanation:** `GET_LOCK`/`RELEASE_LOCK` implement application-level advisory locks to serialize critical sections that a unique index alone cannot express (e.g. insert-if-absent logic).

---

## Q84: Create a scalar function decorated `IMMUTABLE` used in a partial index.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION active_email_domain(p_email TEXT)
RETURNS TEXT
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT COALESCE(NULLIF(split_part(p_email, '@', 2), ''), 'unknown');
$$;

-- Partial index keyed on the function
CREATE INDEX idx_active_emails
ON employees (active_email_domain(email))
WHERE is_active = TRUE;

-- Query that uses the partial index
SELECT * FROM employees
WHERE is_active = TRUE AND active_email_domain(email) = 'company.com';
```
**Explanation:** Partial indexes over expressions let the optimizer skip scans. `IMMUTABLE` is mandatory before PostgreSQL will use a planner-supplied function as an index key.

---

## Q85: Create a procedure with a `SET` of statement options using SQL Server query hints.

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE get_big_report @dept_id INT
AS
BEGIN
    SELECT employee_id, first_name, salary
    FROM employees WITH (NOLOCK)
    WHERE department_id = @dept_id
    ORDER BY salary DESC
    OPTION (RECOMPILE, MAXDOP 4);
END;
```
**Explanation:** `WITH (NOLOCK)` reads without locks and `OPTION (RECOMPILE, MAXDOP 4)` overrides plan caching and parallelism for this procedure — place hints carefully to avoid stale plans on volatile data.

---

## Q86: Create a stored function that returns a table of date buckets (MySQL).

**Query:**
```sql
-- MySQL 8.0+: helper in a procedure to expand week buckets
DELIMITER //
CREATE PROCEDURE week_overview(IN p_start DATE, IN p_weeks INT)
BEGIN
    DECLARE v_i INT DEFAULT 0;
    CREATE TEMPORARY TABLE tmp_buckets (bucket_start DATE, bucket_end DATE);

    WHILE v_i < p_weeks DO
        INSERT INTO tmp_buckets
        VALUES (DATE_ADD(p_start, INTERVAL v_i WEEK),
                DATE_ADD(DATE_ADD(p_start, INTERVAL (v_i + 1) WEEK), INTERVAL -1 DAY));
        SET v_i = v_i + 1;
    END WHILE;

    SELECT b.bucket_start, COUNT(s.txn_id) AS sales
    FROM tmp_buckets b
    LEFT JOIN sales s ON s.txn_date BETWEEN b.bucket_start AND b.bucket_end
    GROUP BY b.bucket_start ORDER BY b.bucket_start;

    DROP TEMPORARY TABLE tmp_buckets;
END //
DELIMITER ;
```
**Explanation:** Generating a calendar/bucket temp table inside a procedure guarantees a row per bucket even with missing sales — a common reporting pattern.

---

## Q87: Create a procedure that uses `RETURNS TABLE` + `RETURN` to return multiple rows in a multi-statement TVF.

**Query:**
```sql
-- SQL Server
CREATE FUNCTION get_hierarchy(@manager_id INT)
RETURNS @tree TABLE (employee_id INT, level INT, path NVARCHAR(400))
AS
BEGIN
    INSERT INTO @tree
    SELECT employee_id, 0, CAST(employee_id AS NVARCHAR) FROM employees
    WHERE manager_id = @manager_id;

    WHILE @@ROWCOUNT > 0
    BEGIN
        INSERT INTO @tree
        SELECT e.employee_id, t.level + 1, t.path + '> ' + CAST(e.employee_id AS NVARCHAR)
        FROM employees e
        JOIN @tree t ON e.manager_id = t.employee_id
        WHERE NOT EXISTS (SELECT 1 FROM @tree x WHERE x.employee_id = e.employee_id);
    END;

    RETURN;
END;

SELECT * FROM dbo.get_hierarchy(10);
```
**Explanation:** Multi-statement TVFs support loops and multiple inserts, enabling recursive-style traversal inside a function while `RETURN` (no expression) finishes the body.

---

## Q88: Create a procedure that uses `COMMIT` inside a PostgreSQL function-vs-procedure distinction.

**Query:**
```sql
-- PostgreSQL: COMMIT is INVALID inside a FUNCTION
-- (this will raise: cannot commit while a function is executing)
CREATE OR REPLACE FUNCTION commit_inside()
RETURNS VOID LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO audit_log (message) VALUES ('attempt');
    COMMIT;  -- ERROR
END;
$$;

-- PostgreSQL: COMMIT is VALID inside a PROCEDURE
CREATE OR REPLACE PROCEDURE commit_inside()
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO audit_log (message) VALUES ('ok');
    COMMIT;
END;
$$;

CALL commit_inside();
```
**Explanation:** Functions must be atomic and cannot control transactions; procedures can `COMMIT`/`ROLLBACK`. This is a key interview distinction between the two object types.

---

## Q89: Create a procedure that opens a `REFCURSOR`, then a caller converts it to a row set.

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION open_emp_cursor(p_dept INT)
RETURNS REFCURSOR
LANGUAGE plpgsql
AS $$
DECLARE
    cur REFCURSOR;
BEGIN
    OPEN cur FOR
        SELECT employee_id, first_name, last_name
        FROM employees WHERE department_id = p_dept;
    RETURN cur;
END;
$$;

-- Caller: must pair with a transaction that stays open
BEGIN;
SELECT open_emp_cursor(5) AS cursor_name;
FETCH ALL FROM "<cursor_name>";  -- substitute returned name
COMMIT;
```
**Explanation:** `RETURN REFCURSOR` hands an open cursor back to the caller. PostgreSQL ties the cursor to the transaction, so the caller must `FETCH` before the transaction ends.

---

## Q90: Demonstrate using bind variables to prevent injection inside dynamic SQL (Oracle).

**Query:**
```sql
-- Oracle
CREATE OR REPLACE PROCEDURE login_check(
    p_email  IN VARCHAR2,
    p_status OUT VARCHAR2
)
AS
    v_count NUMBER;
BEGIN
    -- SAFE: bind variable
    SELECT COUNT(*)
    INTO v_count
    FROM users
    WHERE email = p_email AND is_active = 1;

    v_status := CASE WHEN v_count > 0 THEN 'valid' ELSE 'invalid' END;
END;
/

-- Dynamic variant with bind variable
CREATE OR REPLACE PROCEDURE count_rows_matching(
    p_column IN VARCHAR2,
    p_value  IN VARCHAR2,
    p_count  OUT NUMBER
)
AS
    v_sql VARCHAR2(500);
BEGIN
    v_sql := 'SELECT COUNT(*) FROM users WHERE ' || DBMS_ASSERT.SIMPLE_SQL_NAME(p_column) || ' = :1';
    EXECUTE IMMEDIATE v_sql INTO p_count USING p_value;
END;
/
```
**Explanation:** Values flow through bind variables (`:1`) so they're never parsed as SQL. Only identifiers (validated with `DBMS_ASSERT`) are concatenated. This is the core injection defense.

---

## Q91: Create a procedure returning multiple `OUT` values in MySQL.

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE get_employee_stats(
    IN  p_dept_id INT,
    OUT p_total_emp INT,
    OUT p_max_salary DECIMAL(10,2),
    OUT p_min_salary DECIMAL(10,2)
)
BEGIN
    SELECT COUNT(*)    INTO p_total_emp FROM employees WHERE department_id = p_dept_id;
    SELECT MAX(salary) INTO p_max_salary FROM employees WHERE department_id = p_dept_id;
    SELECT MIN(salary) INTO p_min_salary FROM employees WHERE department_id = p_dept_id;
END //
DELIMITER ;

CALL get_employee_stats(5, @total, @max, @min);
SELECT @total, @max, @min;
```
**Explanation:** Multiple `OUT` parameters let a procedure return a small structured result without a result set, ideal for flag/count patterns on clients that prefer scalars.

---

## Q92: Create a procedure that recompiles a misbehaving sibling procedure (SQL Server).

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE refresh_performance
AS
BEGIN
    DECLARE @sql NVARCHAR(200);

    -- Recompile high-frequency procedures
    EXEC sp_recompile 'get_employees_filtered';
    EXEC sp_recompile 'get_org_overview';

    -- Drop and flush the plan cache for a specific procedure
    SET @sql = N'DBCC FREEPROCCACHE';
    EXEC sp_executesql @sql;

    SELECT 'Procedures recompiled.' AS status;
END;
```
**Explanation:** `sp_recompile` invalidates cached plans; `DBCC FREEPROCCACHE` flushes the whole cache (heavy-handed — use only in maintenance windows). Site-specific recompilation is preferable.

---

## Q93: Create a procedure that safely escapes `%` and `_` in `LIKE` (dynamic pure function).

**Query:**
```sql
-- SQL Server
CREATE FUNCTION escape_like(@input NVARCHAR(4000))
RETURNS NVARCHAR(4000)
AS
BEGIN
    RETURN REPLACE(REPLACE(@input, '[', '[[]'), '%', '[%]');
END;

CREATE PROCEDURE search_products @term NVARCHAR(100)
AS
BEGIN
    SELECT product_id, name
    FROM products
    WHERE name LIKE '%' + dbo.escape_like(@term) + '%' ESCAPE '';
END;
```
**Explanation:** User input that reaches `LIKE` must be escaped so wildcard characters like `%`/`_` don't corrupt matching. The helper function centralizes escaping for reuse.

**Alt1:** PostgreSQL variant using regex-free `replace`:
```sql
-- PostgreSQL
CREATE OR REPLACE FUNCTION escape_like_predicate(p_input TEXT)
RETURNS TEXT
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT replace(replace(p_input, '\', '\\'), '%', '\%');
$$;

CREATE OR REPLACE FUNCTION search_products(p_term TEXT)
RETURNS SETOF products
LANGUAGE sql
STABLE
AS $$
    SELECT * FROM products
    WHERE name LIKE '%' || escape_like_predicate(p_term) || '%' ESCAPE '\';
$$;
```

---

## Q94: Create a procedure that uses `GET LOCK` to prevent concurrent ETL runs (MySQL).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE run_etl_once()
BEGIN
    DECLARE v_lock INT;
    SELECT GET_LOCK('etl_runtime_lock', 0) INTO v_lock;

    IF v_lock <> 1 THEN
        SELECT 'Another ETL is running' AS status;
        RETURN;
    END IF;

    -- actual ETL work
    START TRANSACTION;
        INSERT INTO sales_summary (region, total, period)
        SELECT region, SUM(amount), CURDATE() FROM sales GROUP BY region;
    COMMIT;

    SELECT RELEASE_LOCK('etl_runtime_lock') INTO v_lock;
    SELECT 'ETL complete' AS status;
END //
DELIMITER ;
```
**Explanation:** `GET_LOCK(name, timeout)` returns 1 if acquired, 0 if timeout. Using timeout `0` makes it a non-blocking guard so concurrent ETL invocations fail fast instead of double-running.

---

## Q95: Create an Oracle function returning a date formatter with `IF` and `RETURN` alternatives.

**Query:**
```sql
-- Oracle
CREATE OR REPLACE FUNCTION fmt_hire_date(p_hire_dt IN DATE)
RETURN VARCHAR2
AS
BEGIN
    IF p_hire_dt IS NULL THEN
        RETURN 'no record';
    ELSIF p_hire_dt < DATE '2010-01-01' THEN
        RETURN 'legacy hire on ' || TO_CHAR(p_hire_dt, 'DD-MON-YYYY');
    ELSE
        RETURN 'modern hire on ' || TO_CHAR(p_hire_dt, 'YYYY-MM-DD');
    END IF;
END;
/

SELECT employee_id, fmt_hire_date(hire_date) AS hire_label FROM employees;
```
**Explanation:** Oracle functions allow `RETURN` inside each branch as an early-exit pattern; the header `RETURN VARCHAR2` declares the result type. `DATE '2010-01-01'` is an ANSI date literal.

---

## Q96: Create a procedure that uses a `MERGE`-style upsert with dynamic schema (PostgreSQL).

**Query:**
```sql
-- PostgreSQL
CREATE OR REPLACE PROCEDURE upsert_row_multi_key(
    p_table TEXT,
    p_ids INT[],
    p_values TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_sql TEXT;
    i INT;
BEGIN
    -- build INSERT ... ON CONFLICT with dynamic name using quote_ident
    v_sql := format(
        'INSERT INTO %I (id, val) SELECT * FROM unnest($1::int[], $2::text[]) ON CONFLICT (id) DO UPDATE SET val = EXCLUDED.val',
        p_table
    );
    EXECUTE v_sql USING p_ids, p_values;
    RAISE NOTICE 'Upsert executed on table %', p_table;
END;
$$;
```
**Explanation:** `format('%I', ...)` safely quotes identifiers, and `$1`/`$2` are bind parameters for arrays. `EXECUTE ... USING` binds values, so both identifiers and data are injection-safe.

---

## Q97: Create a procedure that audits whether a called procedure succeeded (MySQL).

**Query:**
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE run_nested_with_audit()
BEGIN
    DECLARE v_start TIMESTAMP DEFAULT NOW();

    CALL get_org_overview();

    INSERT INTO proc_audit (proc_name, ran_at, status)
    VALUES ('get_org_overview', v_start, 'ok');
END //
DELIMITER ;
```
**Explanation:** Wrapping a `CALL` in another procedure lets you timestamp and log execution after the child completes. If the child raises, the caller can catch it or let it propagate.

**Alt1:** With explicit exception logging:
```sql
-- MySQL
DELIMITER //
CREATE PROCEDURE run_nested_with_audit_safe()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        INSERT INTO proc_audit (proc_name, ran_at, status)
        VALUES ('get_org_overview', NOW(), 'failed');
        RESIGNAL;
    END;

    CALL get_org_overview();
    INSERT INTO proc_audit (proc_name, ran_at, status)
    VALUES ('get_org_overview', NOW(), 'ok');
END //
DELIMITER ;
```

---

## Q98: Create a table-valued function in SQL Server used in a `JOIN`.

**Query:**
```sql
-- SQL Server
CREATE FUNCTION get_department_roster(@dept_id INT)
RETURNS TABLE
AS
RETURN
(
    SELECT employee_id, first_name, last_name, salary,
           ROW_NUMBER() OVER (ORDER BY salary DESC) AS rank_in_dept
    FROM employees
    WHERE department_id = @dept_id
);

-- Join-friendly usage
SELECT d.department_name, r.first_name, r.salary, r.rank_in_dept
FROM departments d
CROSS APPLY dbo.get_department_roster(d.department_id) r
ORDER BY d.department_name, r.rank_in_dept;
```
**Explanation:** Inline TVFs are joinable like tables; `CROSS APPLY` passes each outer row's value to the function — ideal for "top N per group" reports.

---

## Q99: Create a procedure with a `RETURN` status code in SQL Server.

**Query:**
```sql
-- SQL Server
CREATE PROCEDURE delete_employee_if_terminated @emp_id INT
AS
BEGIN
    IF EXISTS (SELECT 1 FROM employees WHERE employee_id = @emp_id AND termination_date IS NOT NULL)
    BEGIN
        DELETE FROM employees WHERE employee_id = @emp_id;
        RETURN 0;   -- success
    END

    RETURN 1;   -- not terminated or missing
END;

DECLARE @status INT;
EXEC @status = delete_employee_if_terminated @emp_id = 202;
IF @status = 0
    PRINT 'Deleted';
ELSE
    PRINT 'Skipped';
```
**Explanation:** SQL Server procedures return an integer status code via `RETURN n`; callers capture it with `EXEC @var = proc`. This complements `OUTPUT` parameters for signaling outcomes.

---

## Q100: Create a complete end-to-end procedure that composes many patterns: validation, transactions, nested calls, dynamic SQL, function use, and auditing.

**Query:**
```sql
-- PostgreSQL (final capstone pattern)
CREATE OR REPLACE FUNCTION emp_display(p_first TEXT, p_last TEXT)
RETURNS TEXT
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT initcap(p_first) || ' ' || initcap(p_last);
$$;

CREATE OR REPLACE PROCEDURE onboard_employee(
    p_first       TEXT,
    p_last        TEXT,
    p_email       TEXT,
    p_dept_id     INT,
    p_start_salary NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_emp_id INT;
    v_assignment_ref REFCURSOR;
    v_notice TEXT;
BEGIN
    -- 1. validation (business rule)
    IF p_first IS NULL OR p_last IS NULL OR p_email IS NULL THEN
        RAISE EXCEPTION 'All identity fields are required';
    END IF;
    IF p_start_salary <= 0 THEN
        RAISE EXCEPTION 'Salary must be positive';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM departments WHERE department_id = p_dept_id) THEN
        RAISE EXCEPTION 'Unknown department %', p_dept_id;
    END IF;
    IF EXISTS (SELECT 1 FROM employees WHERE email = p_email) THEN
        RAISE EXCEPTION 'Email % already in use', p_email;
    END IF;

    -- 2. transaction body
    INSERT INTO employees (first_name, last_name, email, department_id, salary)
    VALUES (p_first, p_last, p_email, p_dept_id, p_start_salary)
    RETURNING employee_id INTO v_emp_id;

    -- 3. nested procedure-style call (functions here)
    v_notice := 'Onboarded ' || emp_display(p_first, p_last) || ' (id ' || v_emp_id || ')';

    INSERT INTO employment_events (emp_id, event_type, event_note)
    VALUES (v_emp_id, 'onboard', v_notice);

    -- 4. transaction commit inside procedure
    COMMIT;

    -- 5. audit + return REFCURSOR for downstream report
    INSERT INTO proc_audit (proc_name, detail)
    VALUES ('onboard_employee', v_notice);

    OPEN v_assignment_ref FOR
        SELECT employee_id, emp_display(first_name, last_name) AS name, department_id
        FROM employees WHERE employee_id = v_emp_id;

    RAISE NOTICE '%', v_notice;
END;
$$;
```
**Explanation:** This capstone combines input validation, procedural business rules, function composition, transactional `COMMIT`, auditing, and a `REFCURSOR` result — demonstrating how all prior patterns integrate into one production-grade procedure.

**Alt1:** The same pattern in SQL Server:
```sql
-- SQL Server
CREATE PROCEDURE onboard_employee
    @first NVARCHAR(50),
    @last NVARCHAR(50),
    @email NVARCHAR(100),
    @dept_id INT,
    @start_salary DECIMAL(10,2)
AS
BEGIN
    SET XACT_ABORT ON;
    DECLARE @new_id INT;

    IF @first IS NULL OR @last IS NULL OR @email IS NULL
        THROW 51001, 'All identity fields are required', 1;
    IF @start_salary <= 0
        THROW 51002, 'Salary must be positive', 1;
    IF NOT EXISTS (SELECT 1 FROM departments WHERE department_id = @dept_id)
        THROW 51003, 'Unknown department', 1;
    IF EXISTS (SELECT 1 FROM employees WHERE email = @email)
        THROW 51004, 'Email already in use', 1;

    BEGIN TRANSACTION;
        INSERT INTO employees (first_name, last_name, email, department_id, salary)
        VALUES (@first, @last, @email, @dept_id, @start_salary);
        SET @new_id = SCOPE_IDENTITY();

        INSERT INTO employment_events (emp_id, event_type, event_note)
        VALUES (@new_id, 'onboard', @first + ' ' + @last);
    COMMIT;

    SELECT * FROM employees WHERE employee_id = @new_id;
END;
```
