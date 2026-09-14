# Recursive CTEs and Hierarchical Queries — 100 Interview Q&A

## Q1: Basic recursive CTE anatomy — list all employees in a manager tree

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT * FROM org;
```

**Explanation:** The anchor member seeds the query with root nodes (no manager), then the recursive term repeatedly joins back until no more children are found. `UNION ALL` merges each generation.

**Alt1:**
```sql
SELECT id, name, manager_id
FROM employees
START WITH manager_id IS NULL
CONNECT BY PRIOR id = manager_id;
```
**Explanation:** Same tree with Oracle-native syntax — CONNECT BY PRIOR id = manager_id replaces the whole recursive term.

---

## Q2: Identifying the anchor vs recursive term

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org_tree AS (
    SELECT id, name, manager_id, 0 AS depth
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, t.depth + 1
    FROM employees e
    JOIN org_tree t ON e.manager_id = t.id
)
SELECT * FROM org_tree;
```

**Explanation:** The first SELECT before `UNION ALL` is the anchor (non-recursive). Everything after `UNION ALL` is the recursive term that references the CTE itself.

---

## Q3: Adding depth / level numbers to every node

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, o.level + 1
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT id, name, level FROM org ORDER BY level, name;
```

**Explanation:** Each recursive step increments `level` by 1, giving the depth of every employee in the hierarchy starting from 1 at the root.

**Alt1:**
```sql
SELECT id, name, LEVEL
FROM employees
START WITH manager_id IS NULL
CONNECT BY PRIOR id = manager_id;
```
**Explanation:** LEVEL is Oracle's built-in depth pseudo-column, so no hand-rolled counter exists.

---

## Q4: Recursive CTE without `RECURSIVE` keyword (MySQL <8 error)

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
-- MySQL 8+ / Postgres / SQL Server / Oracle
WITH RECURSIVE org AS (
    SELECT id, name, manager_id
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT * FROM org;
```

**Explanation:** The `RECURSIVE` keyword is mandatory in Postgres, MySQL 8+, and SQL Server. Omitting it causes a syntax error. Oracle's `CONNECT BY` does not need it.

---

## Q5: Simple adjacency list — list all subordinates of a specific manager

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE subordinates AS (
    SELECT id, name, manager_id
    FROM employees
    WHERE id = 42

    UNION ALL

    SELECT e.id, e.name, e.manager_id
    FROM employees e
    JOIN subordinates s ON e.manager_id = s.id
)
SELECT id, name FROM subordinates WHERE id <> 42;
```

**Explanation:** Anchor on the target manager, then recurse downward through `manager_id` links. Exclude the manager itself from the result for a pure subordinates list.

---

## Q6: Count of all subordinates per manager

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE subordinates AS (
    SELECT id AS root_manager, id, manager_id
    FROM employees

    UNION ALL

    SELECT s.root_manager, e.id, e.manager_id
    FROM employees e
    JOIN subordinates s ON e.manager_id = s.id
    WHERE e.id <> s.root_manager
)
SELECT root_manager, COUNT(*) - 1 AS subordinate_count
FROM subordinates
GROUP BY root_manager;
```

**Explanation:** Cross-join every employee as a potential root, then count reachable descendants. Subtract 1 to exclude the node itself. This is an "all-pairs" subtree count pattern.

---

## Q7: Count of direct + indirect subordinates per manager (optimized single-root)

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE sub AS (
    SELECT id, name, manager_id
    FROM employees
    WHERE id = 1

    UNION ALL

    SELECT e.id, e.name, e.manager_id
    FROM employees e
    JOIN sub s ON e.manager_id = s.id
)
SELECT (SELECT COUNT(*) FROM sub) - 1 AS total_subordinates;
```

**Explanation:** Starting from employee 1, recurse to find every reachable descendant, then count them all (minus the anchor itself).

---

## Q8: Maximum depth of the organization

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id, 1 AS depth
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, o.depth + 1
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT MAX(depth) AS max_depth FROM org;
```

**Explanation:** Recurse the full tree with depth tracking, then take the maximum. This reveals how many levels exist in the hierarchy.

**Alt1:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id, CAST('' AS VARCHAR(500)) AS dots
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, o.dots || '.'
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT MAX(LENGTH(dots)) AS max_depth FROM org;
```
**Explanation:** Instead of an integer counter, append one dot per level and measure its length — an equivalent depth probe.

---

## Q9: Path from root to every node (concatenated names)

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id,
           CAST(name AS VARCHAR(1000)) AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id,
           o.path || ' → ' || e.name
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT id, name, path FROM org ORDER BY path;
```

**Explanation:** The anchor stores the root name as the initial path string. Each recursive step appends `' → ' || child_name`, building a full lineage trail.

---

## Q10: Path from root using `string_agg` (Postgres)

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id, ARRAY[name] AS name_path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id,
           o.name_path || e.name
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT id, name,
       array_to_string(name_path, ' → ') AS path
FROM org;
```

**Explanation:** Postgres arrays grow naturally in recursion. `array_to_string` converts the array into a delimited path string at the end.

**Alt1:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id, ARRAY[name] AS trail
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, o.trail || e.name
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT id, name,
       (SELECT string_agg(x, ' → ') FROM unnest(trail) x) AS path
FROM org;
```
**Explanation:** unnest plus string_agg in a subquery produces the identical trail as array_to_string.

---

## Q11: Path collection in SQL Server using `STRING_AGG` equivalent

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id,
           CAST(name AS NVARCHAR(MAX)) AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id,
           CAST(o.path + N' → ' + e.name AS NVARCHAR(MAX))
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT id, name, path FROM org;
```

**Explanation:** SQL Server requires explicit `CAST` to `NVARCHAR(MAX)` to prevent truncation during string concatenation in recursion.

---

## Q12: Cycle detection using an array of visited IDs (Postgres)

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id,
           ARRAY[id] AS visited
    FROM employees
    WHERE id = 1

    UNION ALL

    SELECT e.id, e.name, e.manager_id,
           o.visited || e.id
    FROM employees e
    JOIN org o ON e.manager_id = o.id
    WHERE e.id <> ALL(o.visited)
)
SELECT id, name, visited FROM org;
```

**Explanation:** The `visited` array accumulates every ancestor. The `WHERE` clause prevents revisiting any ID already in the path, stopping infinite loops from cycles in the data.

**Alt1:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id, CAST(id AS VARCHAR(1000)) AS path_ids
    FROM employees
    WHERE id = 1

    UNION ALL

    SELECT e.id, e.name, e.manager_id,
           o.path_ids || ',' || e.id
    FROM employees e
    JOIN org o ON e.manager_id = o.id
    WHERE POSITION(',' || e.id || ',' IN ',' || o.path_ids || ',') = 0
)
SELECT id, name FROM org;
```
**Explanation:** Padding the delimiter on both sides turns POSITION into a reliable membership test on the visited set — array-free cycle guard.

---

## Q13: Cycle detection using a path string (MySQL 8+ / SQL Server)

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id,
           CAST(id AS CHAR(1000)) AS path_ids
    FROM employees
    WHERE id = 1

    UNION ALL

    SELECT e.id, e.name, e.manager_id,
           CONCAT(o.path_ids, ',', e.id)
    FROM employees e
    JOIN org o ON e.manager_id = o.id
    WHERE FIND_IN_SET(e.id, o.path_ids) = 0
)
SELECT id, name FROM org;
```

**Explanation:** IDs are concatenated into a comma-separated string. `FIND_IN_SET` checks if the child ID already appears in the ancestry path, preventing revisits.

---

## Q14: Finding leaf nodes (nodes with no children)

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
SELECT e.id, e.name
FROM employees e
WHERE NOT EXISTS (
    SELECT 1 FROM employees c WHERE c.manager_id = e.id
);
```

**Explanation:** A leaf is any employee who is not a manager of anyone else. The `NOT EXISTS` subquery confirms no child rows reference this employee as manager.

---

## Q15: Finding leaf nodes via recursive CTE (set-based)

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT o.id, o.name
FROM org o
WHERE NOT EXISTS (
    SELECT 1 FROM employees e WHERE e.manager_id = o.id
);
```

**Explanation:** First materialize the full tree via recursion, then filter to nodes that have no children in the original table. Useful when the tree must be reconstructed first.

---

## Q16: All ancestors of a given node (walking upward)

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE ancestors AS (
    SELECT id, name, manager_id
    FROM employees
    WHERE id = 99

    UNION ALL

    SELECT e.id, e.name, e.manager_id
    FROM employees e
    JOIN ancestors a ON e.id = a.manager_id
)
SELECT * FROM ancestors;
```

**Explanation:** Anchor on the target node, then join upward via `e.id = a.manager_id` — each step finds the parent. Recursion stops at the root (where `manager_id IS NULL`).

---

## Q17: All ancestors of a node with level distance (Postgres)

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE ancestors AS (
    SELECT id, name, manager_id, 0 AS dist
    FROM employees
    WHERE id = 99

    UNION ALL

    SELECT e.id, e.name, e.manager_id, a.dist + 1
    FROM employees e
    JOIN ancestors a ON e.id = a.manager_id
)
SELECT id, name, dist
FROM ancestors
ORDER BY dist;
```

**Explanation:** Each upward step increments `dist`, telling you how many levels above the target each ancestor sits.

---

## Q18: Shortest path / degree of separation between two employees (BFS)

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE bfs AS (
    SELECT id, manager_id, 0 AS hops
    FROM employees
    WHERE id = 10

    UNION ALL

    SELECT e.id, e.manager_id, b.hops + 1
    FROM employees e
    JOIN bfs b ON e.manager_id = b.id
    WHERE b.hops < 20
)
SELECT hops AS degree_of_separation
FROM bfs
WHERE id = 42
LIMIT 1;
```

**Explanation:** Starting from employee 10, BFS expands outward level by level. The first time we reach employee 42, that `hops` value is the shortest upward distance. The `hops < 20` cap prevents runaway recursion.

**Alt1:**
```sql
WITH RECURSIVE org AS (
    SELECT id, manager_id, 1 AS depth
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.manager_id, o.depth + 1
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT ABS(a.depth - b.depth) AS chain_gap
FROM org a, org b
WHERE a.id = 10 AND b.id = 42;
```
**Explanation:** In a single-rooted strict tree the only connection is up-then-down, so the depth difference is the exact separation — cheaper than a BFS walk.

---

## Q19: Degree of separation in a bidirectional friend graph

**Schema:** `friends(user_a INT, user_b INT)`

**Query:**
```sql
WITH RECURSIVE bfs AS (
    SELECT user_a AS current, user_b AS next_user, 1 AS hops
    FROM friends
    WHERE user_a = 1

    UNION ALL

    SELECT b.next_user,
           CASE WHEN f.user_a = b.next_user THEN f.user_b ELSE f.user_a END,
           b.hops + 1
    FROM bfs b
    JOIN friends f ON f.user_a = b.next_user OR f.user_b = b.next_user
    WHERE b.hops < 10
)
SELECT MIN(hops) - 1 AS separation
FROM bfs
WHERE current = 50;
```

**Explanation:** BFS traverses the undirected friend graph bidirectionally. We expand both sides of each edge and track hops. The minimum hops to reach the target gives the degree of separation.

---

## Q20: All paths (walks) between two nodes — not just shortest

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE walks AS (
    SELECT id, manager_id,
           CAST(id AS VARCHAR(500)) AS path,
           1 AS hops
    FROM employees
    WHERE id = 10

    UNION ALL

    SELECT e.id, e.manager_id,
           w.path || '→' || CAST(e.id AS VARCHAR(500)),
           w.hops + 1
    FROM employees e
    JOIN walks w ON e.manager_id = w.id
    WHERE w.hops < 15
      AND e.id <> ALL(
          SELECT CAST(unnest::INT FROM unnest(string_to_array(w.path, '→')))
      )
)
SELECT path, hops
FROM walks
WHERE id = 42;
```

**Explanation:** Unlike BFS, this enumerates all walks (paths without revisiting nodes) by tracking the full path and excluding already-visited IDs. More expensive but shows every possible route.

---

## Q21: Simple path detection — no repeated vertices

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE paths AS (
    SELECT id, manager_id, ARRAY[id] AS visited, ARRAY[id] AS path
    FROM employees
    WHERE id = 10

    UNION ALL

    SELECT e.id, e.manager_id,
           p.visited || e.id,
           p.path || e.id
    FROM employees e
    JOIN paths p ON e.manager_id = p.id
    WHERE e.id <> ALL(p.visited)
)
SELECT path, array_length(path, 1) - 1 AS length
FROM paths
WHERE id = 42;
```

**Explanation:** The `visited` array tracks every vertex seen so far, guaranteeing no node is revisited. This produces only simple paths, not arbitrary walks.

---

## Q22: Generating a sequence of numbers (1 to 100) with recursion

**Schema:** none (pure generation)

**Query:**
```sql
WITH RECURSIVE nums AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM nums WHERE n < 100
)
SELECT n FROM nums;
```

**Explanation:** The anchor produces 1, and each recursive step adds 1 until reaching 100. MySQL 8+ and SQL Server require this approach; Postgres can also use `generate_series(1,100)`.

**Alt1:**
```sql
SELECT generate_series(1, 100) AS n;
```
**Explanation:** Postgres generates ranges natively; the recursive CTE is only required on MySQL 8+ and SQL Server, which lack generate_series.

---

## Q23: Generating a date series (Postgres `generate_series` vs recursive)

**Schema:** none

**Query:**
```sql
-- Recursive CTE approach (works on all platforms)
WITH RECURSIVE dates AS (
    DATE '2025-01-01' AS dt
    UNION ALL
    SELECT dt + INTERVAL '1 day' FROM dates WHERE dt < '2025-12-31'
)
SELECT dt FROM dates;

-- Postgres idiomatic alternative
SELECT generate_series(
    '2025-01-01'::date,
    '2025-12-31'::date,
    '1 day'::interval
)::date AS dt;
```

**Explanation:** The recursive CTE works universally. Postgres `generate_series` is cleaner and generally faster for date ranges. The recursive approach is needed on MySQL and SQL Server.

**Alt1:**
```sql
WITH RECURSIVE dates AS (
    SELECT CAST('2025-01-01' AS DATE) AS dt
    UNION ALL
    SELECT DATEADD(DAY, 1, dt)
    FROM dates
    WHERE dt < '2025-12-31'
)
SELECT dt FROM dates OPTION (MAXRECURSION 400);
```
**Explanation:** DATEADD powers the increment, and OPTION (MAXRECURSION 400) is required because a full year exceeds SQL Server's default 100 iterations.

---

## Q24: Generating a date series in MySQL 8+

**Schema:** none

**Query:**
```sql
WITH RECURSIVE dates AS (
    CAST('2025-01-01' AS DATE) AS dt
    UNION ALL
    SELECT DATE_ADD(dt, INTERVAL 1 DAY) FROM dates WHERE dt < '2025-12-31'
)
SELECT dt FROM dates;
```

**Explanation:** MySQL 8+ supports recursive CTEs. `DATE_ADD` increments the date. The `CAST` in the anchor ensures proper DATE type for the recursion.

---

## Q25: Splitting a delimited string into rows (recursive splitter — Postgres)

**Schema:** none

**Query:**
```sql
WITH RECURSIVE split AS (
    SELECT
        CAST('apple,banana,cherry' AS TEXT) AS remaining,
        CAST('' AS TEXT) AS value
    UNION ALL
    SELECT
        CASE WHEN position(',' in remaining) > 0
             THEN substring(remaining from position(',' in remaining) + 1)
             ELSE ''
        END,
        CASE WHEN position(',' in remaining) > 0
             THEN substring(remaining from 1 for position(',' in remaining) - 1)
             ELSE remaining
        END
    FROM split
    WHERE remaining <> ''
)
SELECT value FROM split WHERE value <> '';
```

**Explanation:** Each recursive step extracts the first element before the comma, then feeds the remainder back. Recursion ends when no comma is left. Postgres also has `string_to_array` and `unnest` as simpler alternatives.

**Alt1:**
```sql
SELECT unnest(string_to_array('apple,banana,cherry', ',')) AS value;
```
**Explanation:** Postgres one-liner for the same split; recursion earns its keep only on platforms without array support.

---

## Q26: Splitting a string into rows (MySQL 8+ recursive splitter)

**Schema:** none

**Query:**
```sql
WITH RECURSIVE split AS (
    SELECT 1 AS pos, 'apple,banana,cherry' AS rest
    UNION ALL
    SELECT pos + 1, SUBSTRING_INDEX('apple,banana,cherry', ',', pos * -1)
    FROM split
    WHERE pos < 3
)
SELECT SUBSTRING_INDEX(
    SUBSTRING_INDEX('apple,banana,cherry', ',', pos),
    ',', -1
) AS value
FROM split;
```

**Explanation:** `SUBSTRING_INDEX` with a negative count grabs the tail section; the outer `SUBSTRING_INDEX` extracts the last element at each position. The recursion drives `pos` from 1 to the element count.

---

## Q27: Splitting a string into rows (SQL Server recursive splitter)

**Schema:** none

**Query:**
```sql
WITH RECURSIVE split AS (
    SELECT
        1 AS start_pos,
        CHARINDEX(',', 'apple,banana,cherry') AS sep_pos
    UNION ALL
    SELECT
        sep_pos + 1,
        NULLIF(CHARINDEX(',', 'apple,banana,cherry', sep_pos + 1), 0)
    FROM split
    WHERE sep_pos > 0
)
SELECT
    CASE WHEN sep_pos > 0
         THEN SUBSTRING('apple,banana,cherry', start_pos, sep_pos - start_pos)
         ELSE SUBSTRING('apple,banana,cherry', start_pos, 5000)
    END AS value
FROM split;
```

**Explanation:** `start_pos` scans past the previous comma; `CHARINDEX` finds the next one; `NULLIF` turns "no more commas" into NULL so recursion stops. Final `SUBSTRING` yields each delimited element.

---

## Q28: Materialized path vs adjacency list — converting adjacency to materialized path

**Schema:** `categories(id, name, parent_id)`

**Query:**
```sql
WITH RECURSIVE cat AS (
    SELECT id, name, parent_id,
           CAST('/' || name AS VARCHAR(2000)) AS path
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.parent_id,
           cat.path || '/' || e.name
    FROM categories e
    JOIN cat ON e.parent_id = cat.id
)
SELECT id, name, path FROM cat;
```

**Explanation:** The `path` column represents the materialized path equivalent of the adjacency list. Each level appends its name to the parent's path, producing a full `root/a/b/c` lineage.

**Alt1:**
```sql
WITH RECURSIVE cat AS (
    SELECT id, name, parent_id, '/' || CAST(id AS VARCHAR(20)) AS path_ids
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.parent_id,
           cat.path_ids || '/' || CAST(e.id AS VARCHAR(20))
    FROM categories e
    JOIN cat ON e.parent_id = cat.id
)
SELECT id, name, path_ids FROM cat;
```
**Explanation:** ID-based materialized paths survive renames; names read better on reports, ids stay correct through data edits.

---

## Q29: Converting a materialized path table back to adjacency (parent_id) form

**Schema:** `categories_mp(id, name, path VARCHAR)` — root is `/root`, leaf is `/root/phones/iphone`

**Query:**
```sql
SELECT c.id, c.name, c.path,
       p.id AS parent_id
FROM categories_mp c
LEFT JOIN categories_mp p
  ON p.path = left(c.path,
                   length(c.path) - length(split_part(c.path, '/', -1)) - 1)
ORDER BY c.path;
```

**Explanation:** The parent's materialized path is the node's path minus the trailing `'/' + last-segment`. `split_part(path, '/', -1)` extracts that last segment, so subtracting its length plus 1 yields the exact prefix. Roots end up with parent_id NULL.

---

## Q30: Subtree descendants via materialized-path prefix match

**Schema:** `categories_mp(id, name, path VARCHAR)` — path `/electronics/phones/iphone`

**Query:**
```sql
SELECT id, name, path
FROM categories_mp
WHERE path = '/electronics'
   OR path LIKE '/electronics/%'
ORDER BY path;
```

**Explanation:** With a materialized path, a whole subtree is one prefix predicate — no recursion needed, and an index on `path` makes it fast. This is why materialized paths beat adjacency lists for read-heavy trees.

**Alt1:**
```sql
WITH RECURSIVE sub AS (
    SELECT id, name
    FROM categories
    WHERE id = 3

    UNION ALL

    SELECT c.id, c.name
    FROM categories c
    JOIN sub s ON c.parent_id = s.id
)
SELECT * FROM sub;
```
**Explanation:** The same '/electronics' subtree via adjacency-list recursion — each level re-scans categories, which is why the prefix scan wins on reads.

---

## Q31: Ancestors of a category using materialized path (no recursion)

**Schema:** `categories_mp(id, name, path)` — path like `/electronics/phones/iphone`

**Query:**
```sql
SELECT c.id, c.name, x.pos
FROM categories_mp c
JOIN LATERAL (
    SELECT generate_series(1, array_length(
        string_to_array('/electronics/phones/iphone', '/'), 1) - 1
    ) AS pos
) x ON true
WHERE c.path = '/' || (string_to_array(
    '/electronics/phones/iphone', '/'))[x.pos + 1];
```

**Explanation:** Splitting the path into its parts yields each ancestor name, so we can look up ancestor rows by their position. This demonstrates why materialized paths make upward queries trivial.

**Alt1:**
```sql
WITH RECURSIVE ancestors AS (
    SELECT id, name, parent_id
    FROM categories
    WHERE id = 9

    UNION ALL

    SELECT c.id, c.name, c.parent_id
    FROM categories c
    JOIN ancestors a ON c.id = a.parent_id
)
SELECT name FROM ancestors;
```
**Explanation:** Path splits serve materialized-path tables; for adjacency lists the upward walk on parent_id is the direct equivalent.

---

## Q32: Hierarchical categories with product counts rolled up per branch

**Schema:** `categories(id, name, parent_id)`, `products(id, category_id)`

**Query:**
```sql
WITH RECURSIVE cat_tree AS (
    SELECT id, name, parent_id
    FROM categories
    UNION ALL
    SELECT c.id, c.name, c.parent_id
    FROM categories c
    JOIN cat_tree ct ON c.parent_id = ct.id
)
SELECT ct.name AS category,
       COUNT(p.id) AS product_count
FROM cat_tree ct
LEFT JOIN products p ON p.category_id = ct.id
GROUP BY ct.id, ct.name;
```

**Explanation:** This counts products in each category plus all its descendants. For a true per-branch rollup (including subcategories' products), count products assigned to any node in the subtree.

---

## Q33: Aggregate products into parent categories with rollup (correct version)

**Schema:** `categories(id, name, parent_id)`, `products(id, category_id)`

**Query:**
```sql
WITH RECURSIVE cat_tree AS (
    SELECT root.id AS root_id, leaf.id AS leaf_id
    FROM categories root
    JOIN categories leaf ON 1 = 1

    UNION ALL

    SELECT ct.root_id, c.id
    FROM categories c
    JOIN cat_tree ct ON c.parent_id = ct.leaf_id
)
SELECT root_id,
       COUNT(DISTINCT p.id) AS total_products
FROM cat_tree ct
JOIN products p ON p.category_id = ct.leaf_id
GROUP BY root_id;
```

**Explanation:** For each root category we enumerate every descendant leaf, then join products to the leaves. This gives a true rollup: a parent's count includes all grandchildren's products. Recursion count is bounded by tree depth, not node count.

**Alt1:**
```sql
SELECT root.name,
       COUNT(p.id) AS products_in_branch
FROM categories root
LEFT JOIN categories c1 ON root.id = c1.parent_id
LEFT JOIN categories c2 ON c1.id = c2.parent_id
LEFT JOIN products p
  ON p.category_id IN (root.id, c1.id, c2.id)
WHERE root.parent_id IS NULL
GROUP BY root.id, root.name;
```
**Explanation:** Fixed-depth trees need no recursion — three self-joins enumerate the same rollup with predictable plan cost.

---

## Q34: Subtree size (number of nodes) for every node in a category tree

**Schema:** `categories(id, name, parent_id)`

**Query:**
```sql
WITH RECURSIVE subtree AS (
    SELECT root_id, leaf_id
    FROM (SELECT DISTINCT id AS root_id FROM categories) r
    CROSS JOIN (SELECT DISTINCT id AS leaf_id FROM categories) l

    UNION ALL

    SELECT s.root_id, c.id
    FROM categories c
    JOIN subtree s ON c.parent_id = s.leaf_id
)
SELECT root_id, COUNT(DISTINCT leaf_id) AS subtree_size
FROM subtree
GROUP BY root_id;
```

**Explanation:** The anchor enumerates all candidate (root, leaf) pairs with recursion adding any descendant. Counting distinct leaves per root yields subtree size for every node in one pass.

---

## Q35: Managing infinite loops — cap recursion depth

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id, 1 AS depth
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, o.depth + 1
    FROM employees e
    JOIN org o ON e.manager_id = o.id
    WHERE o.depth < 10   -- hard cap
)
SELECT * FROM org WHERE depth <= 10;
```

**Explanation:** The `depth < 10` guard in the recursive term stops iteration at 10 levels even if cyclic or pathological data exists. A depth cap is the simplest protection against infinite loops.

---

## Q36: SQL Server `MAXRECURSION` option to guard runaway recursion

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT * FROM org
OPTION (MAXRECURSION 50);
```

**Explanation:** `OPTION (MAXRECURSION n)` limits recursive iterations to `n`. When exceeded, SQL Server aborts with error 530. A value of 0 means unlimited.

---

## Q37: Detecting a cycle and reporting the offending IDs (Postgres)

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id,
           ARRAY[id] AS path_ids,
           false AS cyclic
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id,
           o.path_ids || e.id,
           e.id = ANY(o.path_ids)
    FROM employees e
    JOIN org o ON e.manager_id = o.id
    WHERE NOT o.cyclic
)
SELECT id, path_ids
FROM org
WHERE cyclic;
```

**Explanation:** Each row tracks its ancestry array and a `cyclic` flag. When a child already exists in the path, that row is marked cyclic, exposing exactly where the loop closes.

---

## Q38: Oracle `CONNECT BY` — the classic hierarchical traversal

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
SELECT id, name, manager_id, LEVEL
FROM employees
START WITH manager_id IS NULL
CONNECT BY PRIOR id = manager_id;
```

**Explanation:** `START WITH` is the anchor; `CONNECT BY PRIOR id = manager_id` links each row to its child. `LEVEL` gives the depth automatically. Oracle-only syntax, no `UNION ALL` needed.

---

## Q39: Oracle `CONNECT BY` with `ORDER SIBLINGS BY` for tree-ordered output

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
SELECT id, name, LEVEL
FROM employees
START WITH manager_id IS NULL
CONNECT BY PRIOR id = manager_id
ORDER SIBLINGS BY name;
```

**Explanation:** `ORDER SIBLINGS BY` sorts children under the same parent within the tree ordering, preserving each subtree as a contiguous block — unlike a plain `ORDER BY`.

---

## Q40: Oracle cycle detection with `NOCYCLE` and `CONNECT_BY_ISCYCLE`

**Schema:** `employees(id, name, manager_id)` (may contain cycles)

**Query:**
```sql
SELECT id, name, LEVEL,
       CONNECT_BY_ISCYCLE AS is_cycle
FROM employees
START WITH manager_id IS NULL
CONNECT BY NOCYCLE PRIOR id = manager_id;
```

**Explanation:** `NOCYCLE` tells Oracle to stop descending when a node repeats; `CONNECT_BY_ISCYCLE` flags which rows closed a loop. Clean one-line cycle handling.

---

## Q41: Convert an Oracle `CONNECT BY` query to a Postgres recursive CTE

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
-- Oracle CONNECT BY
SELECT id, name, LEVEL
FROM employees
START WITH manager_id IS NULL
CONNECT BY PRIOR id = manager_id;

-- Equivalent Postgres recursive CTE
WITH RECURSIVE org AS (
    SELECT id, name, 1 AS level
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, o.level + 1
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT id, name, level FROM org;
```

**Explanation:** `START WITH` maps to the anchor; `CONNECT BY PRIOR id = manager_id` maps to the join in the recursive term; `LEVEL` maps to a manually tracked counter.

---

## Q42: Oracle top-down path with `SYS_CONNECT_BY_PATH`

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
SELECT id, name, LEVEL,
       SYS_CONNECT_BY_PATH(name, ' → ') AS path
FROM employees
START WITH manager_id IS NULL
CONNECT BY PRIOR id = manager_id;
```

**Explanation:** `SYS_CONNECT_BY_PATH(name, ' → ')` builds the name trail from root to each row automatically. The separator is passed as the second argument.

**Alt1:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id, CAST(name AS VARCHAR(2000)) AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, o.path || ' → ' || e.name
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT id, name, path FROM org;
```
**Explanation:** SYS_CONNECT_BY_PATH is Oracle's helper; the Postgres recursive CTE builds the identical trail by appending in the recursive term.

---

## Q43: Tree path to root with indentation (using recursive CTE)

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id, 0 AS depth,
           CAST('' AS VARCHAR(500)) AS prefix
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, o.depth + 1,
           o.prefix || '  '
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT prefix || name AS indented_name, depth
FROM org
ORDER BY prefix, name;
```

**Explanation:** Each level adds two spaces to the prefix string, visually indenting children beneath their parents when ordered depth-first.

---

## Q44: Computing balances up a hierarchy — sum children into parents

**Schema:** `accounts(id, account_number, parent_id, balance)`

**Query:**
```sql
WITH RECURSIVE account_tree AS (
    SELECT id, account_number, parent_id, balance
    FROM accounts

    UNION ALL

    SELECT a.id, a.account_number, a.parent_id,
           t.balance
    FROM accounts a
    JOIN account_tree t ON a.id = t.parent_id
)
SELECT id, account_number, SUM(balance) AS rolled_balance
FROM account_tree
GROUP BY id, account_number;
```

**Explanation:** Each account acts as a root; recursion accumulates every descendant's balance. Summing per root gives every node's balance including all sub-accounts.

**Alt1:**
```sql
SELECT CONNECT_BY_ROOT id AS root_id,
       SUM(balance) AS rolled_balance
FROM accounts
START WITH parent_id IS NULL
CONNECT BY PRIOR id = parent_id
GROUP BY CONNECT_BY_ROOT id;
```
**Explanation:** Oracle folds the whole subtree sum into one statement via GROUP BY CONNECT_BY_ROOT.

---

## Q45: Balance rollup with level, excluding the anchor's own double-count

**Schema:** `accounts(id, account_number, parent_id, balance)`

**Query:**
```sql
WITH RECURSIVE tree AS (
    SELECT root_id, id, balance
    FROM (SELECT DISTINCT id AS root_id FROM accounts) r
    CROSS JOIN accounts a
    WHERE a.id = r.root_id

    UNION ALL

    SELECT t.root_id, a.id, t.balance + a.balance
    FROM accounts a
    JOIN tree t ON a.parent_id = t.id
)
SELECT root_id, MAX(balance) AS subtotal
FROM tree
GROUP BY root_id;
```

**Explanation:** The anchor establishes each root with its own balance; each recursive join adds a child's balance to the running total. The root is included exactly once each — no double counting.

---

## Q46: Order tree traversal — siblings first, then children (breadth-first)

**Schema:** `categories(id, name, parent_id)`

**Query:**
```sql
WITH RECURSIVE cat AS (
    SELECT id, name, parent_id, 0 AS depth,
           CAST(id AS VARCHAR(100)) AS sort_key
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name, c.parent_id, cat.depth + 1,
           cat.sort_key || '.' || CAST(c.id AS VARCHAR(100))
    FROM categories c
    JOIN cat ON c.parent_id = cat.id
)
SELECT id, name, depth
FROM cat
ORDER BY depth, name;
```

**Explanation:** BFS ordering is achieved trivially by sorting on the depth level generated. All siblings at a depth appear together before any deeper node.

---

## Q47: Depth-first ordering of a tree (pre-order with recursive sort key)

**Schema:** `categories(id, name, parent_id)`

**Query:**
```sql
WITH RECURSIVE cat AS (
    SELECT id, name, parent_id,
           CAST(name AS VARCHAR(2000)) AS dfs_path
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name, c.parent_id,
           cat.dfs_path || '/' || c.name
    FROM categories c
    JOIN cat ON c.parent_id = cat.id
)
SELECT id, name
FROM cat
ORDER BY dfs_path;
```

**Explanation:** The accumulated path string `root/a/b` sorts lexicographically in pre-order: each parent and its whole subtree appear before the next sibling subtree.

---

## Q48: Nested comment threads with resolved depth (Reddit-style)

**Schema:** `comments(id, post_id, parent_id, body)`

**Query:**
```sql
WITH RECURSIVE thread AS (
    SELECT id, post_id, parent_id, body, 0 AS depth
    FROM comments
    WHERE parent_id IS NULL AND post_id = 7

    UNION ALL

    SELECT c.id, c.post_id, c.parent_id, c.body, t.depth + 1
    FROM comments c
    JOIN thread t ON c.parent_id = t.id
)
SELECT id, body, depth
FROM thread
ORDER BY depth, id;
```

**Explanation:** Comments anchor at top-level replies, then each child comment recurses with an incremented depth. Sort produces level-grouped threads rather than true nesting order.

---

## Q49: Comment threads in actual nesting order (DFS path ordering)

**Schema:** `comments(id, post_id, parent_id, body)`

**Query:**
```sql
WITH RECURSIVE thread AS (
    SELECT id, parent_id, body,
           CAST(LPAD(CAST(id AS VARCHAR), 10, '0') AS VARCHAR(500)) AS order_key
    FROM comments
    WHERE parent_id IS NULL AND post_id = 7

    UNION ALL

    SELECT c.id, c.parent_id, c.body,
           t.order_key || '.' || LPAD(CAST(c.id AS VARCHAR), 10, '0')
    FROM comments c
    JOIN thread t ON c.parent_id = t.id
)
SELECT id, body
FROM thread
ORDER BY order_key;
```

**Explanation:** Each child's order key extends the parent's with its own zero-padded ID. Lexicographic sorting renders the full nesting structure — parent immediately followed by its descendants.

---

## Q50: Bill-of-materials explosion — multiply quantities down the tree

**Schema:** `parts(part_id, parent_id, qty_per_parent)`

**Query:**
```sql
WITH RECURSIVE bom AS (
    SELECT part_id, parent_id, qty_per_parent, qty_per_parent AS total_qty,
           1 AS depth
    FROM parts
    WHERE parent_id IS NULL

    UNION ALL

    SELECT p.part_id, p.parent_id, p.qty_per_parent,
           b.total_qty * p.qty_per_parent,
           b.depth + 1
    FROM parts p
    JOIN bom b ON p.parent_id = b.part_id
)
SELECT part_id, total_qty
FROM bom
ORDER BY total_qty DESC;
```

**Explanation:** Like factorial recursion, each level multiplies the running total by the child's per-parent quantity — e.g., 3 engines × 4 bolts each = 12 bolts total needed for the final product.

**Alt1:**
```sql
SELECT part_id, LEVEL,
       SYS_CONNECT_BY_PATH(qty_per_parent, ' * ') AS qty_chain
FROM parts
START WITH parent_id IS NULL
CONNECT BY PRIOR part_id = parent_id;
```
**Explanation:** Oracle prints every multiplication chain; the total for a node is the product of the factors in its path.

---

## Q51: Bill-of-materials with per-level quantity and cycle cap

**Schema:** `parts(part_id, parent_id, qty_per_parent)`

**Query:**
```sql
WITH RECURSIVE bom AS (
    SELECT part_id, parent_id, qty_per_parent,
           qty_per_parent AS total_qty, 1 AS depth,
           ARRAY[part_id] AS visited
    FROM parts
    WHERE parent_id IS NULL

    UNION ALL

    SELECT p.part_id, p.parent_id, p.qty_per_parent,
           b.total_qty * p.qty_per_parent,
           b.depth + 1,
           b.visited || p.part_id
    FROM parts p
    JOIN bom b ON p.parent_id = b.part_id
    WHERE b.depth < 20
      AND p.part_id <> ALL(b.visited)
)
SELECT part_id, total_qty, depth FROM bom;
```

**Explanation:** A depth cap plus a `visited` array protects the BOM explosion against loops in part diagrams. The multiplication rolls quantities down the assembly tree.

---

## Q52: Total required quantity per part (all branches aggregated)

**Schema:** `parts(part_id, parent_id, qty_per_parent)`

**Query:**
```sql
WITH RECURSIVE bom AS (
    SELECT part_id, parent_id, qty_per_parent,
           qty_per_parent AS total_qty
    FROM parts
    WHERE parent_id IS NULL

    UNION ALL

    SELECT p.part_id, p.parent_id, p.qty_per_parent,
           b.total_qty * p.qty_per_parent
    FROM parts p
    JOIN bom b ON p.parent_id = b.part_id
)
SELECT part_id,
       SUM(CASE WHEN parent_id IS NOT NULL THEN total_qty END) AS qty_needed
FROM bom
GROUP BY part_id;
```

**Explanation:** A single part can appear in many assemblies; each lineage contributes a multiplied quantity. Grouping by part and summing gives the total needed across the whole product.

---

## Q53: Depth-first pre-order numbering (tie siblings by name)

**Schema:** `categories(id, name, parent_id)`

**Query:**
```sql
WITH RECURSIVE cat AS (
    SELECT id, name, parent_id,
           CAST(name AS VARCHAR(2000)) AS path
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name, c.parent_id,
           cat.path || '/' || c.name
    FROM categories c
    JOIN cat ON c.parent_id = cat.id
)
SELECT id, name,
       ROW_NUMBER() OVER (ORDER BY path) AS dfs_number
FROM cat
ORDER BY path;
```

**Explanation:** DFS pre-order assigns each node the next number as it is visited. Because the path string sorts the whole subtree contiguously, `ROW_NUMBER()` over it reproduces recursive pre-order numbering.

**Alt1:**
```sql
WITH RECURSIVE dfs AS (
    SELECT id, name, parent_id,
           CAST(ROW_NUMBER() OVER (ORDER BY name) AS VARCHAR(50)) AS key
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name, c.parent_id,
           dfs.key || '.' ||
           CAST(ROW_NUMBER() OVER (PARTITION BY dfs.id ORDER BY c.name)
                AS VARCHAR(50))
    FROM categories c
    JOIN dfs ON c.parent_id = dfs.id
)
SELECT id, name FROM dfs ORDER BY key;
```
**Explanation:** Partitioning by parent ranks each sibling locally; the dotted key sorts into DFS order without an outer ROW_NUMBER.

---

## Q54: Post-order numbering via recursive pass

**Schema:** `categories(id, name, parent_id)`

**Query:**
```sql
WITH RECURSIVE cat AS (
    SELECT id, name, parent_id,
           CAST(name AS VARCHAR(2000)) AS path
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name, c.parent_id,
           cat.path || '/' || c.name
    FROM categories c
    JOIN cat ON c.parent_id = cat.id
),
size AS (
    SELECT id, COUNT(*) AS descendants
    FROM cat c
    GROUP BY id,
             (SELECT c2.id FROM cat c2 WHERE substring(c.path, 1, length(c2.path)) = c2.path AND c.path <> c2.path)
)
SELECT c.id, c.name,
       ROW_NUMBER() OVER (ORDER BY c.path) + s.descendants AS post_order
FROM cat c
JOIN (
    SELECT c3.id, COUNT(*) AS descendants
    FROM cat c3
    WHERE EXISTS (
        SELECT 1 FROM cat c4
        WHERE c4.path LIKE c3.path || '/%'
    )
    GROUP BY c3.id
) s ON s.id = c.id
ORDER BY post_order;
```

**Explanation:** In post-order every node is numbered after its whole subtree. If pre-order position is `pre` and a node has `d` descendants, its post-order number is `pre + d`. The subquery counts descendants via path prefix.

---

## Q55: Flatten a team — every report of a manager regardless of depth

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE team AS (
    SELECT id, name, manager_id, 0 AS depth
    FROM employees
    WHERE manager_id = 17

    UNION ALL

    SELECT e.id, e.name, e.manager_id, t.depth + 1
    FROM employees e
    JOIN team t ON e.manager_id = t.id
)
SELECT id, name, depth
FROM team
ORDER BY depth, name;
```

**Explanation:** The manager's direct reports seed the recursion; the recursive join follows `manager_id` chains through the whole org, flattening any depth into a table.

---

## Q56: When a recursive CTE is the wrong tool — huge graphs and indexing

**Schema:** `graph(a_id, b_id)` — 10M edges

**Query:**
```sql
-- Prefer an iterative BFS or a precomputed closure table when:
--  1) the graph is cyclic and enormous (path arrays blow up memory)
--  2) you need many repeated ancestor lookups
--  3) recursion depth exceeds engine limits (SQL Server 32k, MySQL 255*cte_max_recursion_depth)

CREATE INDEX idx_graph_b ON graph(b_id);
CREATE INDEX idx_graph_a ON graph(a_id);

WITH RECURSIVE reach AS (
    SELECT a_id, b_id, 1 AS depth
    FROM graph WHERE a_id = 5
    UNION ALL
    SELECT r.a_id, g.b_id, r.depth + 1
    FROM graph g JOIN reach r ON g.a_id = r.b_id
    WHERE r.depth < 15
)
SELECT DISTINCT b_id FROM reach;
```

**Explanation:** Recursive CTEs are single-query tools. Deep, repeatedly-queried or cyclic graphs are better served by closure tables, windowed iterative loops, or graph engines — and recursion only performs if the join columns are indexed.

---

## Q57: Using a window function inside the recursive term (ROW_NUMBER per level)

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id, 1 AS depth
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, o.depth + 1
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT depth,
       id, name,
       ROW_NUMBER() OVER (PARTITION BY depth ORDER BY name) AS rank_in_level
FROM org;
```

**Explanation:** Window functions cannot run inside the recursive term itself (no `OVER` there), but they apply cleanly over the fully materialized recursive result. Partitioning by depth ranks each generation independently.

**Alt1:**
```sql
SELECT depth, name, salary,
       VAR_POP(salary) OVER (PARTITION BY depth) AS variance_within_level
FROM org;
```
**Explanation:** Any aggregate at level-granularity can be layered on the materialized set afterward — the recursion itself must simply stay window-free.

---

## Q58: Mutually exclusive recursion levels — read recursion once per level

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
-- You cannot reference a recursive CTE in TWO different places per iteration.
-- This ill-formed double-read pattern throws "recursive reference must not
-- appear within a subquery / must appear only once":
WITH RECURSIVE bad AS (
    SELECT id, name, manager_id, 1 AS depth
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, bad.depth + 1
    FROM employees e
    JOIN bad b1 ON e.manager_id = b1.id
    JOIN bad b2 ON e.name                 -- second reference: ERROR
    WHERE b1.id = b2.id
)
SELECT * FROM bad;
```

**Explanation:** In Postgres, MySQL and SQL Server the recursive term may reference the CTE exactly once per iteration. To combine passes, join against a materialized copy: `SELECT * FROM bad b, LATERAL (SELECT ... FROM bad b2 ...)`, or stage an intermediate CTE.

---

## Q59: Rolling contributions up the tree with a percentage share

**Schema:** `accounts(id, parent_id, name, balance)`

**Query:**
```sql
WITH RECURSIVE rollup AS (
    SELECT id, parent_id, name, balance, 1.0 AS share
    FROM accounts
    WHERE parent_id IS NULL

    UNION ALL

    SELECT a.id, a.parent_id, a.name, a.balance,
           r.share * 0.25                       -- each level keeps 25% of value
    FROM accounts a
    JOIN rollup r ON a.parent_id = r.id
)
SELECT name, balance * share AS effective_balance
FROM rollup
ORDER BY effective_balance DESC;
```

**Explanation:** Multiplying a running factor down the chain discounts deeper nodes, simulating value decay or attribution across a hierarchy — the financial analogue of BOM quantity multiplication.

---

## Q60: Comment threads with both indent and depth

**Schema:** `comments(id, post_id, parent_id, body)`

**Query:**
```sql
WITH RECURSIVE thread AS (
    SELECT id, parent_id, body, 0 AS depth,
           CAST(id AS VARCHAR(300)) AS order_key
    FROM comments
    WHERE parent_id IS NULL AND post_id = 7

    UNION ALL

    SELECT c.id, c.parent_id, c.body, t.depth + 1,
           t.order_key || '.' || CAST(c.id AS VARCHAR(300))
    FROM comments c
    JOIN thread t ON c.parent_id = t.id
)
SELECT depth,
       REPEAT('  ', depth) || body AS indented_body
FROM thread
ORDER BY order_key;
```

**Explanation:** The depth column feeds `REPEAT` for visual indentation while the dotted order key keeps true nesting order. Real forums render both together from one recursion.

---

## Q61: Employee count per level of the whole org

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, manager_id, 1 AS depth
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.manager_id, o.depth + 1
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT depth, COUNT(*) AS employees_at_level
FROM org
GROUP BY depth
ORDER BY depth;
```

**Explanation:** Depth is incremented once per recursion iteration, so grouping by it counts how many employees sit at each generation of the tree.

**Alt1:**
```sql
SELECT LEVEL, COUNT(*)
FROM employees
START WITH manager_id IS NULL
CONNECT BY PRIOR id = manager_id
GROUP BY LEVEL
ORDER BY LEVEL;
```
**Explanation:** Oracle's LEVEL exposes the generation directly from the engine, so a level histogram is a GROUP BY away.

---

## Q62: Which managers have only leaf reports (every child is a leaf)

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
SELECT DISTINCT m.id, m.name
FROM employees m
WHERE EXISTS (SELECT 1 FROM employees c WHERE c.manager_id = m.id)
  AND NOT EXISTS (
      SELECT 1
      FROM employees c
      WHERE c.manager_id = m.id
        AND EXISTS (SELECT 1 FROM employees g WHERE g.manager_id = c.id)
  );
```

**Explanation:** A manager qualifies when they have children, but none of those children manage anyone below them. The inner `EXISTS` check ensures every direct report is a leaf.

---

## Q63: Detect all cycles in a directed graph (report every loop)

**Schema:** `graph(from_id, to_id)`

**Query:**
```sql
WITH RECURSIVE walk AS (
    SELECT from_id, to_id, ARRAY[from_id, to_id] AS visited, 1 AS depth
    FROM graph

    UNION ALL

    SELECT w.from_id, g.to_id,
           w.visited || g.to_id, w.depth + 1
    FROM graph g
    JOIN walk w ON g.from_id = w.to_id
    WHERE w.depth < 10 AND g.to_id <> ALL(w.visited[1:array_length(w.visited,1)-1])
)
SELECT DISTINCT visited
FROM walk
WHERE to_id = ANY(visited[1:array_length(visited,1)-1]);
```

**Explanation:** Every edge seeds a walk. A row is cyclic when its `to_id` reappears inside the visited path — the array slice `[1..-1]` stops the immediate 2-node back-edge, letting propagation distinguish real cycles.

---

## Q64: Friends-of-friends recommendations within 2 hops

**Schema:** `friendships(user_id, friend_id)`

**Query:**
```sql
WITH RECURSIVE hops AS (
    SELECT friend_id, 0 AS hops
    FROM friendships
    WHERE user_id = 10

    UNION ALL

    SELECT f.friend_id, h.hops + 1
    FROM friendships f
    JOIN hops h ON f.user_id = h.friend_id
    WHERE h.hops < 2
      AND f.friend_id <> 10
)
SELECT friend_id, MAX(hops) AS min_hop
FROM hops
GROUP BY friend_id
HAVING MAX(hops) = 2;
```

**Explanation:** Iterating twice through the friendship edges yields distance-2 people. Excluding the seed user and direct friends leaves the actual recommendations (suggested friends).

---

## Q65: MySQL 8 — org path with CONCAT and cycle guard

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id,
           CAST(name AS CHAR(2000)) AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id,
           CONCAT(o.path, ' > ', e.name)
    FROM employees e
    JOIN org o ON e.manager_id = o.id
    WHERE NOT FIND_IN_SET(e.id,
          REPLACE(o.path, ' > ', ',') = o.path
              AND o.id IN (SELECT 1))   -- placeholder guard, keep cycles out
)
SELECT id, name, path FROM org;
```

**Explanation:** MySQL concatenates strings with `CONCAT`. A robust cycle guard tracks integer IDs in a separate list — paths mixing names and IDs make string-based guards brittle, so prefer an explicit ID array where supported.

---

## Q66: UNION vs UNION ALL inside a recursive CTE

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id
    FROM employees
    WHERE manager_id IS NULL

    UNION  -- deduplicates every hatch of rows each iteration (slower)

    SELECT e.id, e.name, e.manager_id
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT * FROM org;
```

**Explanation:** `UNION` forces a dedup pass per iteration on top of the entire accumulated set. For trees — where each node has exactly one parent and rows are inherently unique — `UNION ALL` is always correct and far faster.

---

## Q67: Every manager with the full list of descendant names (array_agg)

**Schema:** `employees(id, name, manager_id)`, `org_rollup(manager_id, member_id)` — union table of all (manager, report) pairs

**Query:**
```sql
WITH RECURSIVE rollup AS (
    SELECT m.id AS manager_id, m.id AS member_id
    FROM employees m

    UNION ALL

    SELECT r.manager_id, e.id
    FROM employees e
    JOIN rollup r ON e.manager_id = r.member_id
)
SELECT r.manager_id,
       array_agg(e.name ORDER BY e.name) AS descendant_names
FROM rollup r
JOIN employees e ON e.id = r.member_id
GROUP BY r.manager_id;
```

**Explanation:** The union table enumerates every (manager, descendant) pair, then one GROUP BY with `array_agg` lists the full reporting line for each manager .

**Alt1:**
```sql
WITH RECURSIVE rollup AS (
    SELECT m.id AS manager_id, m.id AS member_id
    FROM employees m

    UNION ALL

    SELECT r.manager_id, e.id
    FROM employees e
    JOIN rollup r ON e.manager_id = r.member_id
)
SELECT r.manager_id,
       GROUP_CONCAT(e.name ORDER BY e.name SEPARATOR ' | ') AS descendant_names
FROM rollup r
JOIN employees e ON e.id = r.member_id
GROUP BY r.manager_id;
```
**Explanation:** MySQL's GROUP_CONCAT is the string-combining sibling of Postgres's array_agg.

---

## Q68: An employee's manager's manager (grandparent lookup)

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE up AS (
    SELECT id, manager_id, 0 AS up_depth
    FROM employees
    WHERE id = 55

    UNION ALL

    SELECT e.id, e.manager_id, u.up_depth + 1
    FROM employees e
    JOIN up u ON e.id = u.manager_id
)
SELECT e.name AS grandparent
FROM up u
JOIN employees e ON e.id = u.manager_id
WHERE u.up_depth = 2;
```

**Explanation:** Walking upward, `up_depth = 2` identifies the grandparent level. Joining back to employees resolves that manager's id into a name.

---

## Q69: Full report chain from one leaf up to the CEO

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE up AS (
    SELECT id, name, manager_id,
           CAST(name AS VARCHAR(1000)) AS chain
    FROM employees
    WHERE id = 99

    UNION ALL

    SELECT e.id, e.name, e.manager_id,
           up.chain || ' ↑ ' || e.name
    FROM employees e
    JOIN up ON e.id = up.manager_id
)
SELECT chain FROM up ORDER BY length(chain) DESC LIMIT 1;
```

**Explanation:** The anchor names the leaf, and each upward join appends the parent to the chain string. The longest chain ends at the CEO, giving the complete "reports-to" line.

---

## Q70: Prune a whole subtree when a node fails a predicate

**Schema:** `employees(id, name, manager_id, status)`

**Query:**
```sql
WITH RECURSIVE active_org AS (
    SELECT id, name, manager_id, status
    FROM employees
    WHERE manager_id IS NULL AND status = 'Active'

    UNION ALL

    SELECT e.id, e.name, e.manager_id, e.status
    FROM employees e
    JOIN active_org a ON e.manager_id = a.id
    WHERE e.status = 'Active'
)
SELECT id, name FROM active_org;
```

**Explanation:** Filtering in the recursive term's `WHERE` removes a node and, because its row is never produced, all of its descendants vanish too. One predicate prunes entire branches.

---

## Q71: Find orphaned employees not reachable from any root

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE reachable AS (
    SELECT id FROM employees WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id
    FROM employees e
    JOIN reachable r ON e.manager_id = r.id
)
SELECT e.id, e.name
FROM employees e
LEFT JOIN reachable r ON r.id = e.id
WHERE r.id IS NULL;
```

**Explanation:** Compute the connected component rooted at managers, then anti-join to expose employees whose manager chain never reaches a root — typical of cycles or dangling `manager_id` values.

---

## Q72: LATERAL join with a recursive subquery (per-manager subtree counts)

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
SELECT e.id, e.name, s.team_size
FROM employees e
JOIN LATERAL (
    WITH RECURSIVE sub AS (
        SELECT e.id
        UNION ALL
        SELECT c.id
        FROM employees c
        JOIN sub ON c.manager_id = sub.id
    )
    SELECT COUNT(*) AS team_size FROM sub
) s ON TRUE
WHERE e.manager_id IS NULL
ORDER BY s.team_size DESC;
```

**Explanation:** `LATERAL` lets the inner recursive CTE reference the outer row's `e.id`, computing a subtree count per manager — a lazy, row-driven alternative to the all-pairs pattern.

---

## Q73: Chaining two recursive CTEs in one query

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id, 1 AS depth
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, o.depth + 1
    FROM employees e
    JOIN org o ON e.manager_id = o.id
),
paths AS (
    SELECT id, name, CAST(name AS VARCHAR(1000)) AS breadcrumb
    FROM org
    WHERE manager_id IS NULL

    UNION ALL

    SELECT o.id, o.name, paths.breadcrumb || ' → ' || o.name
    FROM org o
    JOIN paths ON o.manager_id = paths.id
)
SELECT id, name, breadcrumb FROM paths;
```

**Explanation:** A second recursive CTE (`paths`) can iterate over the result of the first (`org`) with the same `RECURSIVE` keyword. This composes depth and lineage in a single statement.

---

## Q74: Generate only business days for a range

**Schema:** none

**Query:**
```sql
WITH RECURSIVE days AS (
    SELECT DATE '2025-01-01' AS dt
    UNION ALL
    SELECT dt + INTERVAL '1 day'
    FROM days
    WHERE dt < DATE '2025-12-31'
)
SELECT dt
FROM days
WHERE EXTRACT(ISODOW FROM dt) BETWEEN 1 AND 5;
```

**Explanation:** The recursion enumerates every calendar day; the final `WHERE` filters weekends via `ISODOW`. It is simple and portable, at the cost of stepping through non-business days.

---

## Q75: Weighted rollup — propagate balances up a hierarchy with level decay

**Schema:** `accounts(id, parent_id, balance)`

**Query:**
```sql
WITH RECURSIVE agg AS (
    SELECT id, parent_id, balance,
           1 AS depth
    FROM accounts
    WHERE id = 1

    UNION ALL

    SELECT a.id, a.parent_id, a.balance,
           agg.depth + 1
    FROM accounts a
    JOIN agg ON a.parent_id = agg.id
)
SELECT SUM(balance) AS total_balance,
       MAX(depth) AS levels
FROM agg;
```

**Explanation:** Starting at account 1, recursion fans out to every descendant; summing balances rolls the whole subtree into one figure while `MAX(depth)` reports how many levels contributed.

---

## Q76: Capstone combo — depth, path, cycle-guard and subtree rollup in one pass

**Schema:** `employees(id, name, manager_id, salary)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id, salary,
           1 AS depth,
           CAST(name AS VARCHAR(2000)) AS path,
           ARRAY[id] AS visited
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, e.salary,
           f.depth + 1,
           f.path || ' → ' || e.name,
           f.visited || e.id
    FROM employees e
    JOIN org f ON e.manager_id = f.id
    WHERE e.id <> ALL(f.visited)
)
SELECT id, name, depth, path,
       (SELECT COUNT(*)
        FROM org d
        WHERE d.path LIKE o.path || ' → %')            AS subtree_size,
       (SELECT COALESCE(SUM(d.salary), 0)
        FROM org d
        WHERE d.path LIKE o.path || ' → %')            AS subtree_salary
FROM org o
ORDER BY path;
```

**Explanation:** Every building block — anchor/recursive split, depth counter, name trail, visited-array cycle guard, and prefix-matching subqueries against the materialized CTE — combines into one complete, cycle-safe hierarchy report.

**Alt1:**
```sql
SELECT id, name, LEVEL,
       SYS_CONNECT_BY_PATH(name, ' → ') AS path,
       CONNECT_BY_ISCYCLE,
       CONNECT_BY_ROOT id AS root_id
FROM employees
START WITH id = 1
CONNECT BY NOCYCLE PRIOR id = manager_id;
```
**Explanation:** Oracle packs hierarchy, path, root and the loop flag into a single CONNECT BY — a compact stand-in for the full recursive capstone.

---

## Q77: Deepest employee(s) with their chain length

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id, 1 AS depth
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, o.depth + 1
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT id, name, depth
FROM org
WHERE depth = (SELECT MAX(depth) FROM org);
```

**Explanation:** Filter to employees at the maximum computed depth. This answers "who is furthest from a manager?" — the tail of the longest chain.

---

## Q78: Cumulative headcount as you walk down the levels

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, manager_id, 1 AS depth
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.manager_id, o.depth + 1
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT depth,
       COUNT(*) AS hires_at_level,
       SUM(COUNT(*)) OVER (ORDER BY depth) AS cumulative_headcount
FROM org
GROUP BY depth
ORDER BY depth;
```

**Explanation:** Recursion buckets employees by depth, then a window function over the grouped result turns level sizes into a running total.

---

## Q79: Least common ancestor (LCA) of two employees

**Schema:** `employees(id, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, manager_id, ARRAY[id] AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.manager_id, o.path || e.id
    FROM employees e
    JOIN org o ON e.manager_id = o.id
),
pa AS (SELECT path FROM org WHERE id = 10),
pb AS (SELECT path FROM org WHERE id = 42),
cpr AS (
    SELECT i, pa.path[i] AS node_id
    FROM pa, pb,
         generate_series(1, LEAST(array_length(pa.path, 1),
                                  array_length(pb.path, 1))) AS i
    WHERE pa.path[i] = pb.path[i]
)
SELECT node_id AS least_common_ancestor FROM cpr ORDER BY i DESC LIMIT 1;
```

**Explanation:** Both root-to-node paths live in arrays. The longest shared prefix is the LCA — compare element-by-element and take the deepest matching index.

**Alt1:**
```sql
WITH RECURSIVE up_a AS (
    SELECT id, manager_id, 0 AS d FROM employees WHERE id = 10
    UNION ALL
    SELECT e.id, e.manager_id, u.d + 1
    FROM employees e JOIN up_a u ON e.id = u.manager_id
),
up_b AS (
    SELECT id FROM employees WHERE id = 42
    UNION ALL
    SELECT e.id FROM employees e JOIN up_b u ON e.id = u.manager_id
)
SELECT a.id AS lca_id
FROM up_a a JOIN up_b b ON a.id = b.id
ORDER BY a.d DESC
LIMIT 1;
```
**Explanation:** Compute both ancestor sets upward, intersect them, and take the row deepest from A — a marked-set LCA algorithm.

---

## Q80: Permission inheritance — everything a user inherits from ancestors

**Schema:** `folders(id, parent_id, perm)`

**Query:**
```sql
WITH RECURSIVE ancestors AS (
    SELECT id, parent_id, perm
    FROM folders
    WHERE id = 21

    UNION ALL

    SELECT f.id, f.parent_id, f.perm
    FROM folders f
    JOIN ancestors a ON f.id = a.parent_id
)
SELECT ARRAY_AGG(DISTINCT perm) AS effective_permissions
FROM ancestors;
```

**Explanation:** Start at the folder in question and walk creationward. `ARRAY_AGG(DISTINCT ...)` merges the folding of inherited grants into a single result set.

---

## Q81: Powers of two — doubling series

**Schema:** none

**Query:**
```sql
WITH RECURSIVE doubles AS (
    SELECT 1 AS n, 2 AS v
    UNION ALL
    SELECT n + 1, v * 2
    FROM doubles
    WHERE n < 15
)
SELECT n, v FROM doubles;
```

**Explanation:** The recursive term doubles the previous value. This is the simplest numerical recursion — pattern that underlies growth/exponential sequences.

---

## Q82: Fibonacci numbers with a recursive CTE

**Schema:** none

**Query:**
```sql
WITH RECURSIVE fib AS (
    SELECT 0 AS n, 0 AS a, 1 AS b

    UNION ALL

    SELECT n + 1, b, a + b
    FROM fib
    WHERE n < 20
)
SELECT n, a AS fibonacci FROM fib;
```

**Explanation:** Each row carries the previous pair (a, b); the next is (b, a+b). Carrying two values per row makes the "two-step" recurrence fit recursion.

**Alt1:**
```sql
WITH RECURSIVE fib AS (
    SELECT 0 AS a, 1 AS b

    UNION ALL

    SELECT b, a + b
    FROM fib
    WHERE b <= 1000
)
SELECT a AS fibonacci FROM fib;
```
**Explanation:** Carrying the previous pair forward makes the recurrence tail-friendly; the WHERE bound replaces the n counter as the stop condition.

---

## Q83: Factorial with recursion

**Schema:** none

**Query:**
```sql
WITH RECURSIVE fact AS (
    SELECT 1 AS n, 1 AS f
    UNION ALL
    SELECT n + 1, (n + 1) * f
    FROM fact
    WHERE n < 10
)
SELECT n, f FROM fact;
```

**Explanation:** Each iteration multiplies the running product by the next integer. The recursion is identical to the mathematical definition `n! = n × (n-1)!`.

---

## Q84: Collatz sequence for a starting number

**Schema:** none

**Query:**
```sql
WITH RECURSIVE collatz AS (
    SELECT 27 AS element, 0 AS step

    UNION ALL

    SELECT CASE WHEN element % 2 = 0 THEN element / 2
                ELSE 3 * element + 1
           END,
           step + 1
    FROM collatz
    WHERE element <> 1
)
SELECT step, element FROM collatz ORDER BY step;
```

**Explanation:** A branching rule — even halves, odd triples-plus-one — recomputed each iteration until the sequence reaches 1. Recursion handles the dynamic termination cleanly.

---

## Q85: Hourly timetable generation in a window

**Schema:** none

**Query:**
```sql
WITH RECURSIVE hours AS (
    SELECT TIMESTAMP '2025-01-01 00:00' AS ts
    UNION ALL
    SELECT ts + INTERVAL '1 hour'
    FROM hours
    WHERE ts < TIMESTAMP '2025-01-02 00:00'
)
SELECT ts FROM hours;
```

**Explanation:** Interval arithmetic in the recursive term marches the clock forward by one hour per row — perfect for gap-free time grids used in reporting and dashboards.

---

## Q86: Counting immediate reports without aggregating inside recursion

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id, 1 AS depth
    FROM employees
    WHERE id = 1

    UNION ALL

    SELECT e.id, e.name, e.manager_id, o.depth + 1
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT id, name, depth,
       (SELECT COUNT(*) FROM employees c WHERE c.manager_id = o.id) AS direct_reports
FROM org o;
```

**Explanation:** Aggregates are not allowed to reference the recursive table inside its own term, so compute counts afterward — a correlated subquery over the original table against each materialized row.

---

## Q87: Index guidance — make recursive joins fast

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
CREATE INDEX idx_employees_manager ON employees(manager_id);

EXPLAIN (ANALYZE)
WITH RECURSIVE org AS (
    SELECT id, name, manager_id
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT * FROM org;
```

**Explanation:** Each iteration probes `employees.manager_id = o.id`. A b-tree on `manager_id` turns that look-up into a point read instead of a full scan — often the difference between milliseconds and minutes.

---

## Q88: Postgres runaway protection — there is no MAXRECURSION

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
SET statement_timeout = '5s';

WITH RECURSIVE org AS (
    SELECT id, name, manager_id, 1 AS depth
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, o.depth + 1
    FROM employees e
    JOIN org o ON e.manager_id = o.id
    WHERE o.depth < 50
)
SELECT * FROM org;
```

**Explanation:** Postgres lacks SQL Server's recursion budget, so guard cycles with an explicit `depth < 50` filter and a `statement_timeout` safety net to cap runaway iterations.

---

## Q89: MySQL 8 recursion budget — `cte_max_recursion_depth`

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
SET cte_max_recursion_depth = 1000;

WITH RECURSIVE org AS (
    SELECT id, name, manager_id, 1 AS depth
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, o.depth + 1
    FROM employees e
    JOIN org o ON e.manager_id = o.id
    WHERE o.depth < 800
)
SELECT * FROM org;
```

**Explanation:** Iterations above `cte_max_recursion_depth` raise error 3636 (ER_CTE_MAX_RECURSION_DEPTH). Raising the ceiling plus a depth filter keeps deep trees legal yet bounded.

---

## Q90: SQL Server — `OPTION (MAXRECURSION 0)` means unlimited

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT * FROM org OPTION (MAXRECURSION 0);
```

**Explanation:** `0` disables the default 100-iteration limit. Only use it on guaranteed-acyclic data, otherwise an unresolvable loop crashes the statement against the recursion boundary.

---

## Q91: Convert adjacency list to nested set (lft / rgt)

**Schema:** `categories(id, name, parent_id)`

**Query:**
```sql
WITH RECURSIVE tree AS (
    SELECT id, name, parent_id,
           CAST(name AS VARCHAR(2000)) AS path
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name, c.parent_id, t.path || '/' || c.name
    FROM categories c
    JOIN tree t ON c.parent_id = t.id
)
SELECT t.id, t.name,
       ROW_NUMBER() OVER (ORDER BY t.path, t.id) AS lft,
       ROW_NUMBER() OVER (ORDER BY t.path, t.id)
         + (SELECT COUNT(*) FROM tree d
            WHERE d.path LIKE t.path || '/%')
         + 1 AS rgt
FROM tree t
ORDER BY lft;
```

**Explanation:** Subtree nodes are contiguous in pre-order, so `lft` is the pre-order rank and `rgt = lft + size(subtree)` gives the enclosing interval. Nested sets make subtree queries single-range scans.

---

## Q92: Convert nested set back to adjacency (find each parent interval)

**Schema:** `categories_ns(id, name, lft, rgt)`

**Query:**
```sql
SELECT c.id, c.name, c.lft, c.rgt,
       (SELECT p.id
        FROM categories_ns p
        WHERE p.lft < c.lft AND p.rgt > c.rgt
        ORDER BY p.lft DESC
        LIMIT 1) AS parent_id
FROM categories_ns c
ORDER BY c.lft;
```

**Explanation:** Any row whose interval strictly contains this one is an ancestor; the one with the largest `lft` (smallest interval) is the immediate parent — the inverse of interval containment.

---

## Q93: Oracle — sum balances per subtree with `CONNECT_BY_ROOT`

**Schema:** `accounts(id, parent_id, balance)`

**Query:**
```sql
SELECT CONNECT_BY_ROOT id AS root_id,
       SUM(balance) AS subtree_balance
FROM accounts
START WITH parent_id IS NULL
CONNECT BY PRIOR id = parent_id
GROUP BY CONNECT_BY_ROOT id;
```

**Explanation:** `CONNECT_BY_ROOT id` exposes each root id on every row of its subtree, so a single GROUP BY performs the whole rollup — Oracle's compact alternative to the recursive CTE.

**Alt1:**
```sql
WITH RECURSIVE org AS (
    SELECT id, id AS root_id, balance
    FROM accounts WHERE parent_id IS NULL

    UNION ALL

    SELECT e.id, o.root_id, e.balance
    FROM accounts e JOIN org o ON e.parent_id = o.id
)
SELECT root_id, SUM(balance) AS subtree_balance
FROM org GROUP BY root_id;
```
**Explanation:** A root_id column threaded by recursion reproduces CONNECT_BY_ROOT in portable SQL.

---

## Q94: Oracle — paths and leaf detection in one shot

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
SELECT id, name, LEVEL,
       SYS_CONNECT_BY_PATH(name, ' → ') AS path,
       CONNECT_BY_ISLEAF AS is_leaf
FROM employees
START WITH manager_id IS NULL
CONNECT BY PRIOR id = manager_id
ORDER SIBLINGS BY name;
```

**Explanation:** Three Oracle-only features — `LEVEL`, `SYS_CONNECT_BY_PATH` and `CONNECT_BY_ISLEAF` — cover depth, lineage and leaves in a single hierarchical pass.

**Alt1:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id, CAST(name AS VARCHAR(2000)) AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, o.path || ' → ' || e.name
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT o.id, o.name, o.path,
       NOT EXISTS (SELECT 1 FROM employees c WHERE c.manager_id = o.id) AS is_leaf
FROM org o;
```
**Explanation:** Path-handed recursion plus an EXISTS check emulates SYS_CONNECT_BY_PATH and CONNECT_BY_ISLEAF.

---

## Q95: Co-workers sharing one top-level department (path element)

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id, ARRAY[name] AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, o.path || e.name
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT a.id AS emp_a, a.name, a.dept, b.id AS emp_b, b.name
FROM (SELECT id, name, path[2] AS dept FROM org) a
JOIN (SELECT id, name, path[2] AS dept FROM org) b
  ON a.dept = b.dept AND a.id < b.id
ORDER BY a.dept;
```

**Explanation:** The second element of each path array identifies the top-level department. Joining on it lists every pair of co-workers that share the same first-level manager.

---

## Q96: Emulating recursion without a recursive CTE (MySQL 5.7 loop)

**Schema:** `employees(id, name, manager_id)`

**Query:**
```sql
DELIMITER $$
CREATE PROCEDURE org_walk(IN root_id INT)
BEGIN
    CREATE TEMPORARY TABLE tmp_org (
        id INT, name VARCHAR(100), depth INT,
        PRIMARY KEY (id)
    );

    INSERT INTO tmp_org SELECT id, name, 1
    FROM employees WHERE id = root_id;

    REPEAT
        INSERT INTO tmp_org
        SELECT e.id, e.name, t.depth + 1
        FROM employees e
        JOIN tmp_org t ON e.manager_id = t.id
        WHERE NOT EXISTS (SELECT 1 FROM tmp_org x WHERE x.id = e.id);
    UNTIL ROW_COUNT() = 0 END REPEAT;

    SELECT * FROM tmp_org ORDER BY depth, name;
    DROP TEMPORARY TABLE tmp_org;
END$$
DELIMITER ;
```

**Explanation:** Before MySQL 8.0, breadth expansion was hand-rolled: insert a level, keep looping until no new rows. The `NOT EXISTS` guard is the manual cycle prevention.

---

## Q97: Building a closure table (all ancestor-descendant pairs)

**Schema:** `categories(id, parent_id)`

**Query:**
```sql
WITH RECURSIVE closure(ancestor, descendant) AS (
    SELECT id, id
    FROM categories

    UNION ALL

    SELECT c.ancestor, e.id
    FROM categories e
    JOIN closure c ON c.descendant = e.parent_id
)
SELECT * FROM closure
ORDER BY ancestor, descendant;
```

**Explanation:** Self-pairs seed the anchor; each recursive round extends a (ancestor, descendant) edge one level down. A closure table pre-answers "is X under Y?" in O(1).

**Alt1:**
```sql
WITH RECURSIVE desc2 AS (
    SELECT id, id AS ancestor
    FROM categories
    WHERE id = 3

    UNION ALL

    SELECT e.id, d.ancestor
    FROM categories e
    JOIN desc2 d ON e.parent_id = d.id
)
SELECT ancestor, id AS descendant FROM desc2;
```
**Explanation:** Instead of the full closure table, enumerate one node's descendants — the pair-set idea, scoped to a single category.

---

## Q98: Window functions over the recursive result — per-level averages

**Schema:** `employees(id, name, manager_id, salary)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, salary, manager_id, 1 AS depth
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.salary, e.manager_id, o.depth + 1
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT depth,
       COUNT(*)  AS level_size,
       AVG(salary) AS avg_salary,
       AVG(AVG(salary)) OVER (ORDER BY depth) AS cumulative_avg
FROM org
GROUP BY depth
ORDER BY depth;
```

**Explanation:** Windows are forbidden inside the recursive term but fully available on its output. Nesting `AVG(AVG(...))` OVER layers an aggregate window on the grouped level statistics.

---

## Q99: Sibling discovery through the materialized path

**Schema:** `categories(id, name, parent_id)`

**Query:**
```sql
WITH RECURSIVE cat AS (
    SELECT id, name, parent_id
    FROM categories
    WHERE parent_id = 10

    UNION ALL

    SELECT c.id, c.name, c.parent_id
    FROM categories c
    JOIN cat t ON c.parent_id = t.id
)
SELECT a.name AS sibling_a, b.name AS sibling_b
FROM cat a
JOIN cat b
  ON b.parent_id = a.parent_id
 AND b.name <> a.name
WHERE a.parent_id <> 10
ORDER BY sibling_a;
```

**Explanation:** Filter the materialized subtree to a single sibling group — equality on `parent_id`. With a materialized path you would instead match the shared prefix up to the last slash.

---

## Q100: Grand finale — full-cycle-safe org chart with per-branch rollups

**Schema:** `employees(id, name, manager_id, salary)`

**Query:**
```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id, salary,
           1 AS depth,
           CAST(name AS VARCHAR(2000)) AS path,
           ARRAY[id] AS visited
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, e.salary,
           o.depth + 1,
           o.path || ' → ' || e.name,
           o.visited || e.id
    FROM employees e
    JOIN org o ON e.manager_id = o.id
    WHERE e.id <> ALL(o.visited)
)
SELECT REPEAT('  ', depth - 1) || name AS org_chart,
       depth,
       path,
       1 + (SELECT COUNT(*) FROM org d
            WHERE d.path LIKE o.path || ' → %')       AS subtree_size,
       o.salary + COALESCE((SELECT SUM(d.salary) FROM org d
                            WHERE d.path LIKE o.path || ' → %'), 0)
                                                      AS subtree_salary
FROM org o
ORDER BY path;
```

**Explanation:** The definitive end-to-end example: cycle-safe recursion with depth, indentation and DFS ordering, plus subtree size and salary rollups computed from prefix matches on the materialized set.

---

