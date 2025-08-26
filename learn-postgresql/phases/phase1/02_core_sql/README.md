## 📚 concepts to master

### 1. **create / drop tables**

* `CREATE TABLE name (...);`
* `DROP TABLE name;`
* use `IF EXISTS` or `IF NOT EXISTS` to avoid errors.

### 2. **common data types**

* **identity/serial** → auto-increment primary key

  * `SERIAL` (older) vs `GENERATED ALWAYS AS IDENTITY` (preferred in new postgres).
* **numeric types** → `INT`, `BIGINT`, `NUMERIC(p,s)` for precision.
* **text** → `TEXT`, `VARCHAR(n)` (text recommended).
* **boolean** → `BOOLEAN` (true/false).
* **jsonb** → binary json (indexable).
* **timestamp** → `TIMESTAMP` (no tz) vs `TIMESTAMPTZ` (with tz, recommended).
* **uuid** → `UUID DEFAULT gen_random_uuid()` (needs `pgcrypto` extension).

### 3. **constraints**

* **primary key (PK)** → unique + not null.
* **foreign key (FK)** → references another table.
* **unique** → disallows duplicate values.
* **check** → custom boolean condition.
* **not null** → disallows nulls.

### 4. **crud**

* **insert**: add rows.
* **update**: change rows.
* **delete**: remove rows.
* **select**: query rows.

### 5. **returning clause**

* lets you get back values from insert/update/delete without separate select.

  ```sql
  INSERT INTO todo (title) VALUES ('Buy milk') RETURNING id;
  ```

---

## 🧪 hands-on test: “todo” table

### step 1 — Extensions in Postgresql

How to Get a List of Available Extensions
```sql
SELECT * FROM pg_available_extensions;
```

Enable Extension
```sql
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
```

Get a List of Installed Extensions
```sql
\dx
```

Note: The \dx command is a shortcut for the following SQL query:
```sql
SELECT * FROM pg_extension;
```

Drop Extension
```sql
DROP EXTENSION IF EXISTS extension_name;
```

Sample output
```
  oid  | extname  | extowner | extnamespace | extrelocatable | extversion | extconfig | extcondition 
-------+----------+----------+--------------+----------------+------------+-----------+--------------
 13644 | plpgsql  |       10 |           11 | f              | 1.0        |           | 
 16429 | pgcrypto |       10 |         2200 | t              | 1.3        |           | 
(2 rows)
```

### step 2 — create table

Drop table if already exists
```sql
DROP TABLE IF EXISTS todo;
```

Create Table
```sql
CREATE TABLE todo (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    due_date TIMESTAMPTZ NOT NULL,
    is_done BOOLEAN NOT NULL DEFAULT false,
    priority INT NOT NULL CHECK (priority BETWEEN 1 AND 5),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

Print available tables
```sql
\dt
```

Sample output
```
        List of relations
 Schema | Name | Type  |  Owner   
--------+------+-------+----------
 public | todo | table | postgres
(1 row)
```

Detailed table info
```sql
\d todo
```

Sample output 
```
                               Table "public.todo"
   Column   |           Type           | Collation | Nullable |      Default      
------------+--------------------------+-----------+----------+-------------------
 id         | uuid                     |           | not null | gen_random_uuid()
 title      | text                     |           | not null | 
 due_date   | timestamp with time zone |           | not null | 
 is_done    | boolean                  |           | not null | false
 priority   | integer                  |           | not null | 
 metadata   | jsonb                    |           |          | '{}'::jsonb
 created_at | timestamp with time zone |           | not null | now()
 updated_at | timestamp with time zone |           | not null | now()
Indexes:
    "todo_pkey" PRIMARY KEY, btree (id)
Check constraints:
    "todo_priority_check" CHECK (priority >= 1 AND priority <= 5)
```

### step 3 — insert rows

Good Insert
```sql
-- good insert
INSERT INTO todo (title, due_date, priority)
VALUES ('Finish SQL lab', now() + interval '1 day', 3)
RETURNING *;
```

Output
```
                  id                  |     title      |             due_date             | is_done | priority | metadata |            created_at            |            updated_at            
--------------------------------------+----------------+----------------------------------+---------+----------+----------+----------------------------------+----------------------------------
 21e3deb6-25b7-4b8d-be2b-87562cce55a8 | Finish SQL lab | 2025-08-27 22:47:32.098344+05:30 | f       |        3 | {}       | 2025-08-26 22:47:32.098344+05:30 | 2025-08-26 22:47:32.098344+05:30
 ```
 
Bad insert: missing NOT NULL
```sql
INSERT INTO todo (priority) VALUES (2);
```

Output
```
ERROR:  null value in column "title" of relation "todo" violates not-null constraint
DETAIL:  Failing row contains (ab5c544c-89d5-4f69-b333-3a4a0f2515f5, null, null, f, 2, {}, 2025-08-26 22:55:20.758017+05:30, 2025-08-26 22:55:20.758017+05:30).
```

Bad insert: priority check fails
```sql
INSERT INTO todo (title, due_date, priority)
VALUES ('Impossible priority', now(), 10);
```

Output
```
ERROR:  new row for relation "todo" violates check constraint "todo_priority_check"
DETAIL:  Failing row contains (8e70da7f-2bfe-4c74-a52a-a1618409328f, Impossible priority, 2025-08-26 22:56:26.847795+05:30, f, 10, {}, 2025-08-26 22:56:26.847795+05:30, 2025-08-26 22:56:26.847795+05:30).
```

View table
```sql
SELECT * FROM todo
```

Output
```
     id                  |     title      |             due_date             | is_done | priority | metadata |            created_at            |            updated_at            
--------------------------------------+----------------+----------------------------------+---------+----------+----------+----------------------------------+----------------------------------
 21e3deb6-25b7-4b8d-be2b-87562cce55a8 | Finish SQL lab | 2025-08-27 22:47:32.098344+05:30 | f       |        3 | {}       | 2025-08-26 22:47:32.098344+05:30 | 2025-08-26 22:47:32.098344+05:30
 ```

### step 4 — update rows

```sql
UPDATE todo
SET is_done = true, updated_at = now()
WHERE title = 'Finish SQL lab'
RETURNING *;
```

Output
```

                  id                  |     title      |             due_date             | is_done | priority | metadata |            created_at            |            updated_at            
--------------------------------------+----------------+----------------------------------+---------+----------+----------+----------------------------------+----------------------------------
 21e3deb6-25b7-4b8d-be2b-87562cce55a8 | Finish SQL lab | 2025-08-27 22:47:32.098344+05:30 | t       |        3 | {}       | 2025-08-26 22:47:32.098344+05:30 | 2025-08-26 23:00:57.097567+05:30
 ```

### step 5 — delete rows

```sql
DELETE FROM todo
WHERE is_done = true
RETURNING *;
```

### step 6 — drop the table (clean up)

```sql
DROP TABLE todo;
```
