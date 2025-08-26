
### **Prerequisites: Lab Setup**

First, ensure you are connected to your database and have the `app_user` and `todo` tables created with the sample data from our previous discussions. If you need to re-create them, here are the commands:

```sql
-- Connect to your database
psql -U learner -d learndb -h localhost

-- Re-create the tables cleanly
DROP TABLE IF EXISTS app_user CASCADE;
CREATE TABLE app_user (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

DROP TABLE IF EXISTS todo CASCADE;
CREATE TABLE todo (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES app_user(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    due_date TIMESTAMPTZ NOT NULL,
    is_done BOOLEAN NOT NULL DEFAULT false,
    priority INT NOT NULL CHECK (priority BETWEEN 1 AND 5),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Insert sample data
INSERT INTO app_user (username) VALUES ('alice'), ('bob'), ('charlie');

INSERT INTO todo (user_id, title, due_date, priority, is_done)
SELECT id, 'Task ' || g, now() + (g || ' days')::interval, (g % 5) + 1, (g % 2 = 0)
FROM app_user, generate_series(1,6) g;
```

-----

### **Part 1: `SELECT` Basics**

These commands show you how to retrieve data with filters, sorting, and pagination.

**1. `SELECT` All Columns and Rows (`SELECT *`)**

```sql
-- See all the data in your todo table.
SELECT * FROM todo;
```

*Output:* All columns and rows from the `todo` table.

```
 id                  |               user_id                | title  |             due_date             | is_done | priority |            created_at            
--------------------------------------+--------------------------------------+--------+----------------------------------+---------+----------+----------------------------------
 3896377e-aa03-4cbc-a9ee-d0e7de6916e2 | 78d2eec1-b7e4-4a8c-be00-fd415208959d | Task 1 | 2025-08-28 01:36:08.667843+05:30 | f       |        2 | 2025-08-27 01:36:08.667843+05:30
 fd9dbada-a24c-462d-a97b-213eda321053 | 068ec14b-653a-4d71-a0a8-e31bc3343dcd | Task 1 | 2025-08-28 01:36:08.667843+05:30 | f       |        2 | 2025-08-27 01:36:08.667843+05:30
 162fbdfa-c74a-4c66-91e5-247814fa03ef | d203e50b-7276-4f5a-b063-58320b3d2834 | Task 1 | 2025-08-28 01:36:08.667843+05:30 | f       |        2 | 2025-08-27 01:36:08.667843+05:30
 96cbcd63-91c0-4851-8dac-371bae31d1c8 | 78d2eec1-b7e4-4a8c-be00-fd415208959d | Task 2 | 2025-08-29 01:36:08.667843+05:30 | t       |        3 | 2025-08-27 01:36:08.667843+05:30
 e9f99db3-9cc6-4eee-ac50-41b8cb5311c8 | 068ec14b-653a-4d71-a0a8-e31bc3343dcd | Task 2 | 2025-08-29 01:36:08.667843+05:30 | t       |        3 | 2025-08-27 01:36:08.667843+05:30
 6909e3d4-f91d-4a99-8bbe-a754d50dd424 | d203e50b-7276-4f5a-b063-58320b3d2834 | Task 2 | 2025-08-29 01:36:08.667843+05:30 | t       |        3 | 2025-08-27 01:36:08.667843+05:30
 2d035db3-b6ef-4877-b3be-74490eaa3f22 | 78d2eec1-b7e4-4a8c-be00-fd415208959d | Task 3 | 2025-08-30 01:36:08.667843+05:30 | f       |        4 | 2025-08-27 01:36:08.667843+05:30
 76089d5a-9c48-435e-b5ec-53777cb6b45f | 068ec14b-653a-4d71-a0a8-e31bc3343dcd | Task 3 | 2025-08-30 01:36:08.667843+05:30 | f       |        4 | 2025-0
:
```

**2. `SELECT` Specific Columns**

```sql
-- Only retrieve the task's title and priority.
SELECT title, priority FROM todo;
```

*Output:* A result set with only two columns: `title` and `priority`.
```
 title  | priority 
--------+----------
 Task 1 |        2
 Task 1 |        2
 Task 1 |        2
 Task 2 |        3
 Task 2 |        3
 Task 2 |        3
 Task 3 |        4
 Task 3 |        4
 Task 3 |        4
 ```

**3. `WHERE` Clause (Filtering Rows)**

```sql
-- Get all tasks that are not yet done.
SELECT title, priority FROM todo WHERE is_done = false;
```

*Output:* Only tasks where the `is_done` column is `false`.
```
 title  | priority 
--------+----------
 Task 1 |        2
 Task 1 |        2
 Task 1 |        2
 Task 3 |        4
 Task 3 |        4
 Task 3 |        4
 Task 5 |        1
 Task 5 |        1
 Task 5 |        1
 ```
**4. `ORDER BY` (Sorting Results)**

```sql
-- Get all tasks, ordered by priority (highest first) and due date (soonest first).
SELECT title, priority FROM todo ORDER BY priority DESC, due_date ASC;
```

*Output:* The rows will be sorted according to your rules.
```
 title  | priority 
--------+----------
 Task 4 |        5
 Task 4 |        5
 Task 4 |        5
 Task 3 |        4
 Task 3 |        4
 Task 3 |        4
 Task 2 |        3
 Task 2 |        3
 Task 2 |        3
 Task 1 |        2
 Task 1 |        2
 Task 1 |        2
 Task 6 |        2
 Task 6 |        2
 Task 6 |        2
 Task 5 |        1
 Task 5 |        1
 Task 5 |        1
 ```

**5. `LIMIT` and `OFFSET` (Pagination)**

Get the first 3 tasks, ordered by creation date.
```sql
SELECT title, priority FROM todo ORDER BY created_at ASC LIMIT 3;
```

Output 
```
 title  | priority 
--------+----------
 Task 1 |        2
 Task 1 |        2
 Task 1 |        2
 ```

Get the next 3 tasks (skipping the first 3).
```sql
SELECT title, priority FROM todo ORDER BY created_at ASC LIMIT 3 OFFSET 1;
```

*Output:* The first query shows rows 1-3. The second shows rows 4-6.
```
 title  | priority 
--------+----------
 Task 1 |        2
 Task 2 |        3
 Task 1 |        2
 ```

-----

### **Part 2: `JOINS`**

`JOINS` combine columns from different tables based on a common value.

**1. `INNER JOIN` (Matching Rows)**

```sql
-- Get the username for each task.
SELECT u.username, t.title
FROM app_user u
INNER JOIN todo t ON u.id = t.user_id;
```

*Output:* A list of tasks showing both the `username` and `title`. Rows where no match exists are excluded.
```
 username | title  
----------+--------
 alice    | Task 1
 bob      | Task 1
 charlie  | Task 1
 alice    | Task 2
 bob      | Task 2
 charlie  | Task 2
 alice    | Task 3
 bob      | Task 3
 charlie  | Task 3
 alice    | Task 4
 bob      | Task 4
 charlie  | Task 4
 alice    | Task 5
 bob      | Task 5
 charlie  | Task 5
 alice    | Task 6
 bob      | Task 6
 charlie  | Task 6
 ```

**2. `LEFT JOIN` (All from Left)**

```sql
-- Insert a new user with no tasks to test this.
INSERT INTO app_user (username) VALUES ('dave');

-- Find users who have no tasks.
SELECT u.username, t.title
FROM app_user u
LEFT JOIN todo t ON u.id = t.user_id
WHERE t.id IS NULL;
```

*Output:* You should see `dave` listed with a `NULL` in the `title` column, because there were no matching tasks for him.

```
 username | title 
----------+-------
 dave     | 
 ```
-----

### **Part 3: `SET` Operations**

`SET` operations combine rows from different queries.

**1. `UNION ALL` (Combine with Duplicates)**

```sql
-- Combine all tasks with a priority of 1 and a priority of 2 into one list.
SELECT title FROM todo WHERE priority = 1
UNION ALL
SELECT title FROM todo WHERE priority = 2;
```

*Output:* A single result set showing the titles of all tasks with priority 1 and priority 2.

```
 title  
--------
 Task 5
 Task 5
 Task 5
 Task 1
 Task 1
 Task 1
 Task 6
 Task 6
 Task 6
 ```

**2. `INTERSECT` (Find Overlap)**

```sql
-- Find tasks that are both high priority (4) and not done.
SELECT title FROM todo WHERE priority = 4
INTERSECT
SELECT title FROM todo WHERE is_done = false;
```

*Output:* Only the title of the tasks that meet *both* conditions.

```
 title  
--------
 Task 3
 ```

-----

### **Part 4: Subqueries**

A subquery is a query nested inside another query, used to get a temporary result set.

**1. Subquery in the `WHERE` Clause**

```sql
-- Find all tasks assigned to the user named 'bob'.
SELECT title, priority
FROM todo
WHERE user_id = (SELECT id FROM app_user WHERE username = 'bob');
```

*Output:* The rows for the tasks assigned to `bob`. The inner query finds `bob`'s ID, and the outer query uses that ID to filter the tasks.

```
 title  | priority 
--------+----------
 Task 1 |        2
 Task 2 |        3
 Task 3 |        4
 Task 4 |        5
 Task 5 |        1
 Task 6 |        2
 ```
-----

### **Part 5: CTEs (Common Table Expressions)**

CTEs make complex queries readable by breaking them into logical, named parts.

**1. A Simple CTE**

Think of a CTE as a temporary, scratch-pad table that you can create and name at the very beginning of your query. This temporary table only exists for the duration of that single query.

The problem they solve is that complex queries can get messy when you start nesting SELECT statements inside each other. A CTE lets you define a complex piece of logic and give it a simple name, so you can use it later in your query just like a regular table.

```sql
-- Use a CTE to filter for 'done' tasks before selecting from them.
WITH done_tasks AS (
    SELECT * FROM todo WHERE is_done = true
)
SELECT id, title FROM done_tasks;
```

*Output:* A simple list of the `id` and `title` for all completed tasks.

```
                  id                  | title  
--------------------------------------+--------
 96cbcd63-91c0-4851-8dac-371bae31d1c8 | Task 2
 e9f99db3-9cc6-4eee-ac50-41b8cb5311c8 | Task 2
 6909e3d4-f91d-4a99-8bbe-a754d50dd424 | Task 2
 b82bed47-ad71-4d3a-8893-77f46494a327 | Task 4
 57250e6c-99c7-41d7-84b0-63bfb661ba3a | Task 4
 cbee8c55-c301-4c6d-a9e7-f61d0836eb52 | Task 4
 991d7541-7197-4835-bd4f-db15b7a4a3de | Task 6
 89ca0b9c-2b75-4725-8a75-8c731853ff45 | Task 6
 2b71c3d9-9379-4425-8990-db82e890a73a | Task 6
 ```

**2. Complex CTE (Top N Per Group)**

This line of code is a powerful single instruction that tells the database to perform a complex sorting and numbering task in a single step.

Let's break it down piece by piece.

The Big Picture

This command creates a new column named `rnk` (for rank) and puts a number in that column for every row. That number tells you how recent a task is for a specific user.

---
Breakdown of the Code

**`ROW_NUMBER()`**:
- This is the **function** itself. Its only job is to assign a unique, sequential number to each row it sees. The counting always starts from 1.

**`OVER ( ... )`**:
- This is the **magic keyword** that makes `ROW_NUMBER()` a "window function." The `OVER` clause defines the **window** or the group of rows that the function should look at. Without `OVER`, `ROW_NUMBER()` wouldn't know how to count.

**`PARTITION BY user_id`**:
- This is the **grouping instruction**. It tells the database to divide all the rows into separate, independent groups based on the `user_id`.
- **In simple terms:** The `ROW_NUMBER()` function will start a new count (restarting at 1) for every single user. It will count all of Alice's tasks, then restart and count all of Bob's tasks, and so on.

**`ORDER BY created_at DESC`**:
- This is the **sorting instruction**. It tells the database how to order the rows **within each group**.
- `DESC` stands for "descending." This means the tasks will be sorted from the newest one (the highest `created_at` timestamp) to the oldest.
- By sorting this way, the newest task will get the number `1`, the second newest will get the number `2`, and so on.

**`AS rnk`**:
- This is the **alias** for the new column. It gives a simple name to the result of the entire `ROW_NUMBER()` calculation, making it easy to refer to in the rest of the query.

Putting It All Together: A Simple, Step-by-Step Process

1.  The database looks at the entire `todo` table.
2.  It creates separate groups of rows for each unique `user_id`.
3.  Inside each group, it sorts the tasks by `created_at` from newest to oldest.
4.  It then assigns a sequential number (1, 2, 3...) to each row in that sorted list.
5.  Finally, it adds a new column named `rnk` to the table and puts that number in the column for each row.

This is what allows the final `WHERE rnk <= 3` clause to work so simply: it's just filtering for the rows that were given a rank of 1, 2, or 3 within their user group.

```sql
-- Find the latest 3 tasks for each user.
WITH ranked_tasks AS (
    SELECT
        title,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rnk
    FROM todo
)
SELECT *
FROM ranked_tasks
WHERE rnk <= 3;
```

*Output:* For each user (`alice`, `bob`, `charlie`), you should see exactly 3 tasks listed, which are their most recent ones.

```
 title  | rnk 
--------+-----
 Task 6 |   1
 Task 3 |   2
 Task 4 |   3
 Task 1 |   1
 Task 2 |   2
 Task 3 |   3
 Task 1 |   1
 Task 2 |   2
 Task 5 |   3
 ```
-----

### **Lab Cleanup**

When you are finished, you can drop the tables to clean up your database.

```sql
DROP TABLE IF EXISTS app_user CASCADE;
DROP TABLE IF EXISTS todo CASCADE;
```