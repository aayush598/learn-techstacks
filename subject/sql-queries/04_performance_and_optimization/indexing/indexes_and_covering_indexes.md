# Indexes and Covering Indexes — 100 SQL Interview Q&A

## Q1: What is a database index and why do we create one?
**Query:**
```sql
CREATE INDEX idx_users_email ON users(email);
```
**Explanation:** An index is a sorted auxiliary structure (usually a B-tree) mapping keys to row locations; it answers `WHERE` on `email` in a handful of reads instead of scanning every row.
**Alt1:** Verify the effect: run `EXPLAIN SELECT * FROM users WHERE email='a@b.com';` before and after `CREATE INDEX`.

## Q2: What data structure backs the default index in most databases?
**Query:**
```sql
CREATE INDEX idx_users_name ON users(name);
```
**Explanation:** The B-tree (B+ tree); it balances O(log n) lookups with cheap insert/delete and yields keys in sorted order for range scans and `ORDER BY`.

## Q3: How does a B-tree actually find a row?
**Query:**
```sql
EXPLAIN SELECT * FROM users WHERE id = 42; -- MySQL / PostgreSQL
```
**Explanation:** The engine walks from the root to a leaf comparing the target key, then follows the row pointer (RID/clustered key) — only ~log(n) nodes touched.

## Q4: Clustered vs non-clustered index — what is the difference?
**Query:**
```sql
-- MySQL: InnoDB primary key IS the clustered index (row data lives in its leaves)
CREATE TABLE orders (id BIGINT PRIMARY KEY, user_id INT, total DECIMAL(10,2)) ENGINE=InnoDB;
-- PostgreSQL: no clustered store by default; every index is a separate non-clustered structure over a heap
CREATE INDEX idx_orders_user ON orders(user_id);
```
**Explanation:** Clustered = the table order itself is sorted by the key; non-clustered stores key + pointer to heap rows.
**Alt1:** SQL Server: `CREATE CLUSTERED INDEX ix_orders_id ON orders(id);` makes the row store sorted by `id`; secondary indexes then point at that clustered key.

## Q5: Does a primary key automatically create an index?
**Query:**
```sql
CREATE TABLE t (id INT PRIMARY KEY, v TEXT); -- MySQL / PostgreSQL
SELECT indexname FROM pg_indexes WHERE tablename='t'; -- PostgreSQL
```
**Explanation:** Yes — every PRIMARY KEY is enforced by a unique index; in InnoDB that index also becomes the clustered one holding the rows.

## Q6: UNIQUE index vs UNIQUE constraint — same thing?
**Query:**
```sql
ALTER TABLE users ADD CONSTRAINT uq_users_email UNIQUE (email);        -- constraint
CREATE UNIQUE INDEX uq2 ON users(email);                               -- raw index
```
**Explanation:** Both create the same underlying B-tree enforcing uniqueness; a constraint is declared metadata, a raw index is invisible to the constraint catalog.
**Alt1:** Check the difference: `SELECT conname FROM pg_constraint;` vs `SELECT indexname FROM pg_indexes;` in PostgreSQL.

## Q7: What physically happens when you run CREATE INDEX?
**Query:**
```sql
CREATE INDEX idx_users_name ON users(name);           -- builds the tree
ALTER TABLE users ALTER INDEX idx_users_name INVISIBLE; -- MySQL 8: hide it
ALTER TABLE users ALTER INDEX idx_users_name VISIBLE;    -- bring it back
```
**Explanation:** The engine scans the table and builds a sorted B-tree of key → row pointer (single-pass "sorted index build" in InnoDB/Postgres).

## Q8: How do you remove an index that is no longer needed?
**Query:**
```sql
DROP INDEX idx_users_email ON users;   -- MySQL
DROP INDEX idx_users_email;            -- PostgreSQL / SQL Server
DROP INDEX idx_users_email;            -- Oracle
```
**Explanation:** Dropping an index removes only the structure; table rows are untouched and reads continue (slower).
**Alt1:** PostgreSQL: `DROP INDEX IF EXISTS idx_users_email;` avoids an error on a missing index.

## Q9: What is a composite (multi-column) index?
**Query:**
```sql
CREATE INDEX idx_emp_dept_salary ON employees(dept_id, salary);
```
**Explanation:** One B-tree sorted by the first column, then the next — it serves filters on `dept_id` alone and on `dept_id` + `salary` in a single seek.

## Q10: What is the leftmost-prefix rule?
**Query:**
```sql
CREATE INDEX idx_a_b_c ON t(a, b, c);
SELECT * FROM t WHERE b = 5 AND c = 9; -- cannot be served by idx_a_b_c
```
**Explanation:** Only leading prefixes `(a)`, `(a,b)`, `(a,b,c)` are seekable; skipping `a` breaks the sort order of the tree.
**Alt1:** On MySQL 8.0.13+ an *index skip scan* can sometimes emulate the missing prefix, but it is a fallback, not a design.

## Q11: Should you put a low-cardinality column (e.g. a boolean) in front of a composite index?
**Query:**
```sql
CREATE INDEX idx_users_active_created ON users(is_active, created_at);
SELECT * FROM users WHERE is_active = 1 ORDER BY created_at;
```
**Explanation:** The first key narrows the search space only if it is selective; for a boolean the tree splits rows roughly in half, usually a losing trade-off.

## Q12: What is selectivity and why does it matter for indexing?
**Query:**
```sql
-- PostgreSQL: distinct values / total rows
SELECT COUNT(DISTINCT country) * 1.0 / COUNT(*) AS selectivity FROM users;
CREATE INDEX idx_users_country ON users(country);
```
**Explanation:** High selectivity (most values distinct) means each key matches few rows, making the index worth the extra read.

## Q13: Full table scan vs index — when does the engine scan anyway?
**Query:**
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE last_seen < '2024-01-01';
-- compare "Seq Scan" with/without: CREATE INDEX idx_users_seen ON users(last_seen);
```
**Explanation:** If the predicate matches a large fraction of rows (or stats are stale), a sequential scan beats index-seek-per-row and the planner says so.

## Q14: Index Seek vs Index Scan — what is the difference?
**Query:**
```sql
SELECT * FROM orders WHERE order_id = 123;    -- EXACT match -> seek
SELECT * FROM orders WHERE order_id < 1000;   -- wide range -> scan
CREATE INDEX idx_orders_id ON orders(order_id);
```
**Explanation:** A seek jumps straight down the tree to one key; a scan traverses a large contiguous run of leaf pages (range or non-selective predicate).

## Q15: What is a covering index?
**Query:**
```sql
CREATE INDEX idx_orders_user_amount ON orders(user_id, total);
SELECT user_id, total FROM orders WHERE user_id = 7; -- no table access needed
```
**Explanation:** When every column of the query sits inside the index (key or leaf), the planner never touches the heap — an *index-only* result.

## Q16: What does SQL Server's INCLUDE clause do?
**Query:**
```sql
CREATE INDEX ix_orders_user ON orders(user_id) INCLUDE (total, status);
SELECT user_id, total, status FROM orders WHERE user_id = 9;
```
**Explanation:** INCLUDE tucks extra columns into the leaf nodes only — they help cover queries without bloating the search key or its sort order.

## Q17: What is an index-only scan in PostgreSQL and why is it still possible with MVCC?
**Query:**
```sql
CREATE INDEX idx_users_name ON users(name);
EXPLAIN (ANALYZE) SELECT name FROM users WHERE name = 'Ada'; -- "Index Only Scan"
```
**Explanation:** Records carry a visibility map; if the page is fully visible the engine trusts the index alone and skips the heap.

## Q18: Why declare a column ASC or DESC inside an index?
**Query:**
```sql
CREATE INDEX idx_logs_ts ON logs(created_at DESC);  -- PostgreSQL / MySQL 8
CREATE NONCLUSTERED INDEX ix_logs_ts ON logs(created_at DESC); -- SQL Server
```
**Explanation:** Matching the btree direction to `ORDER BY ... DESC` lets the engine walk the index forwards instead of reversing or sorting.
**Alt1:** Older MySQL reversed a composite index to emulate DESC sorts; MySQL 8.0+ natively supports descending index parts.

## Q19: What is a functional (expression) index?
**Query:**
```sql
CREATE INDEX idx_users_lower_email ON users(lower(email));
SELECT * FROM users WHERE lower(email) = 'a@b.com';
```
**Explanation:** The index stores the *result* of an expression; it only fires when the query uses the exact same expression on the same column.
**Alt1:** In Oracle this is a *function-based index*: `CREATE INDEX idx_users_upper ON users(UPPER(last_name));`.

## Q20: MySQL can't index expressions directly — how do you work around it?
**Query:**
```sql
-- MySQL 8.0.13+ supports functional key parts:
CREATE INDEX idx_users_lower_email ON users((lower(email)));
-- Older MySQL: materialise the value in a generated column, then index it:
ALTER TABLE users ADD COLUMN email_lower VARCHAR(255)
  GENERATED ALWAYS AS (LOWER(email)) STORED,
  ADD INDEX ix_email_lower (email_lower);
```
**Explanation:** Write the expression inside parentheses on MySQL 8, or precompute into a generated column and index that.
**Alt1:** SQL Server: use a `PERSISTED` computed column (`ALTER TABLE users ADD email_lower AS LOWER(email) PERSISTED;`) and index it.

## Q21: What is a partial index?
**Query:**
```sql
CREATE INDEX idx_orders_open ON orders(status) WHERE status = 'open'; -- PostgreSQL
SELECT * FROM orders WHERE status = 'open' AND amount > 100;
```
**Explanation:** The btree only contains rows satisfying the predicate, so it is tiny and the planner restricts itself to matching queries.
**Alt1:** SQL Server has *filtered indexes* with an equivalent WHERE clause: `CREATE INDEX ix_orders_open ON orders(status) WHERE status='open';`.

## Q22: When is a hash index used and why is the B-tree usually preferred?
**Query:**
```sql
-- PostgreSQL (hash index)
CREATE INDEX idx_users_email_hash ON users USING hash(email);
-- MySQL: hash indexes are internal to the MEMORY/HEAP engine, not user-created
CREATE TABLE mem (id INT, v VARCHAR(50), UNIQUE KEY (v)) ENGINE=MEMORY;
```
**Explanation:** A hash gives O(1) equality lookups but no ordering and no range scans, so B-trees win for almost all real workloads.

## Q23: What is a GIN index good for?
**Query:**
```sql
CREATE INDEX idx_posts_tags ON posts USING gin(tags); -- jsonb column, PostgreSQL
SELECT * FROM posts WHERE tags @> '["sql"]';
```
**Explanation:** GIN (Generalized Inverted Index) maps each array/jsonb element (or tsvector lexeme) to the rows containing it — ideal for containment and full-text.

## Q24: When would you choose a BRIN index over a B-tree?
**Query:**
```sql
CREATE INDEX idx_sensor_reading ON sensor_data(reading_id) USING brin; -- PostgreSQL
SELECT * FROM sensor_data WHERE reading_id BETWEEN 100000 AND 200000;
```
**Explanation:** BRIN stores only min/max per page range, so it is tiny; on huge, physically-ordered time-series/log tables it beats an enormous B-tree.

## Q25: How do you index full-text search?
**Query:**
```sql
-- PostgreSQL: GIN over the tsvector of the text
CREATE INDEX idx_docs_fts ON docs USING gin(to_tsvector('english', body));
-- MySQL: FULLTEXT index
CREATE FULLTEXT INDEX ftx_docs_body ON docs(body);
SELECT * FROM docs WHERE MATCH(body) AGAINST('index' IN NATURAL LANGUAGE MODE);
```
**Explanation:** B-trees order whole strings; inverted indexes tokenize words → row ids, enabling term and phrase searches.
**Alt1:** Query the PostgreSQL one with `SELECT * FROM docs WHERE to_tsvector('english', body) @@ plainto_tsquery('english', 'index');`.

## Q26: Can `LIKE 'prefix%'` use an index?
**Query:**
```sql
CREATE INDEX idx_users_first ON users(first_name);
SELECT * FROM users WHERE first_name LIKE 'Ana%';
```
**Explanation:** A prefix match is a contiguous range in the B-tree's sorted order, so it becomes an index seek plus a small scan.
**Alt1:** Case-insensitive prefixes want a functional index: `CREATE INDEX idx_users_first_low ON users(lower(first_name) text_pattern_ops);`.

## Q27: Can `LIKE '%suffix'` use an index?
**Query:**
```sql
CREATE INDEX idx_users_last ON users(last_name);
SELECT * FROM users WHERE last_name LIKE '%son'; -- Seq Scan: leading wildcard
```
**Explanation:** A leading wildcard breaks the prefix, so the whole tree/table must be walked; index-reversing tricks (`reverse(last_name)`) or full-text are the fixes.
**Alt1:** PostgreSQL: `CREATE INDEX idx_users_last_rev ON users(reverse(last_name));` then query `WHERE reverse(last_name) LIKE 'nos%'`.

## Q28: How can an index remove an ORDER BY sort?
**Query:**
```sql
CREATE INDEX idx_users_email ON users(email);
SELECT * FROM users ORDER BY email LIMIT 10;
```
**Explanation:** Reading the B-tree already yields rows in key order, so the planner drops the Sort node and reads the first leaf page.

## Q29: What happens when ORDER BY mixes ASC and DESC?
**Query:**
```sql
CREATE INDEX idx_t_a_bd ON t(a ASC, b DESC);
SELECT * FROM t ORDER BY a ASC, b DESC; -- matches the index direction
```
**Explanation:** Fewer you can't com; the hybrid direction must be declared on the index columns, otherwise the engine adds a sort.
**Alt1:** A pure single-column index can be scanned in reverse for one direction; two directions on separate columns cannot both reverse.

## Q30: Can an index accelerate GROUP BY?
**Query:**
```sql
CREATE INDEX idx_orders_user ON orders(user_id);
EXPLAIN SELECT user_id, COUNT(*) FROM orders GROUP BY user_id;
```
**Explanation:** Equal keys are adjacent in the B-tree, letting the engine aggregate each group by streaming instead of a hash table.

## Q31: Why index the foreign-key column used in joins?
**Query:**
```sql
CREATE INDEX idx_orders_user ON orders(user_id);
EXPLAIN SELECT * FROM orders o JOIN users u ON u.id = o.user_id;
```
**Explanation:** A nested-loop join probes the inner table once per outer row; an index makes each probe a seek instead of a scan.

## Q32: What is an Oracle bitmap index and when is it right?
**Query:**
```sql
CREATE BITMAP INDEX bmp_orders_status ON orders(status);
SELECT * FROM orders WHERE status = 'shipped';
```
**Explanation:** Each distinct value owns a bitmap over row numbers; low-cardinality AND/OR predicates merge bitmaps fast, but row-locked writes make it unsuitable for OLTP.
**Alt1:** Bitmaps also shine in star schemas with several low-cardinality dimensions combined per query.

## Q33: When should you NOT create an index?
**Query:**
```sql
CREATE TABLE config (k VARCHAR(50) PRIMARY KEY, v TEXT); -- tiny lookup table
```
**Explanation:** Small tables fit one page, indexes add writes and page hops for no read gain; write-heavy and very low-selectivity columns are the classic anti-pattern.

## Q34: What is index bloat and how do you measure it?
**Query:**
```sql
-- PostgreSQL: size + usage per index
SELECT s.indexrelname, pg_size_pretty(pg_relation_size(s.indexrelid)) AS size,
       s.idx_scan, s.idx_tup_read
FROM pg_stat_user_indexes s WHERE s.relname = 'orders';
-- MySQL: InnoDB stats
SELECT * FROM information_schema.INNODB_METRICS WHERE NAME LIKE '%index%';
```
**Explanation:** Deletes/updates leave dead entries that inflate the tree (bloat), so it stores more pages and evicts more cache.

## Q35: What does FILLFACTOR do?
**Query:**
```sql
ALTER INDEX ix_orders_user ON orders REBUILD WITH (FILLFACTOR = 80);      -- SQL Server
ALTER TABLE orders SET (fillfactor = 70);                                  -- PostgreSQL (table-level)
ALTER TABLE orders ENGINE=InnoDB;                                          -- MySQL rebuild
```
**Explanation:** A factor below 100 leaves free space in each page so in-place updates don't force page splits; the cost is more pages and larger scans.
**Alt1:** Tune it up to 90–100 for read-only tables to keep scans tight.

## Q36: How do you rebuild or reindex a bloated index?
**Query:**
```sql
REINDEX INDEX idx_orders_user;                    -- PostgreSQL
ALTER INDEX ix_orders_user ON orders REBUILD;     -- SQL Server
OPTIMIZE TABLE orders;                            -- MySQL rebuilds the clustered tree
ALTER INDEX idx_orders_user REBUILD ONLINE;       -- Oracle
```
**Explanation:** Rebuilding rewrites the tree tight (right-filled leaves, no dead entries), restoring I/O and cache behavior.

## Q37: Why refresh statistics before trusting a plan?
**Query:**
```sql
ANALYZE TABLE orders;                            -- MySQL
ANALYZE orders;                                  -- PostgreSQL
UPDATE STATISTICS dbo.orders;                    -- SQL Server
DBMS_STATS.GATHER_TABLE_STATS(USER, 'ORDERS');   -- Oracle
```
**Explanation:** The planner picks paths from a histogram of values; stale stats make it misjudge selectivity and skip a perfectly good index.

## Q38: Why isn't my index used — function wrapping on the column?
**Query:**
```sql
-- Bad: the function hides the indexed column
SELECT * FROM orders WHERE EXTRACT(YEAR FROM created_at) = 2024;
-- Good: bare column with an equivalent range
CREATE INDEX idx_orders_created ON orders(created_at);
SELECT * FROM orders WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';
```
**Explanation:** `WHERE func(column) = x` defeats the B-tree unless a functional index matches; rewrite to a range over the column.
**Alt1:** Functional index on date parts: PostgreSQL `CREATE INDEX idx_o_y ON orders((EXTRACT(YEAR FROM created_at)));`.

## Q39: Do indexes handle NULL values?
**Query:**
```sql
CREATE INDEX idx_users_email ON users(email);
SELECT * FROM users WHERE email IS NULL;            -- seekable in MySQL/Postgres
```
**Explanation:** B-trees normally index NULLs; Oracle's B-tree stores all-NULL keys only when other columns exist or with `NULLS FIRST`.
**Alt1:** Partial index for a sparse column: `CREATE INDEX idx_users_email ON users(email) WHERE email IS NOT NULL;`.

## Q40: How do you spot redundant/duplicate indexes?
**Query:**
```sql
-- PostgreSQL: list every index and its definition
SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'users';
CREATE INDEX idx_users_name  ON users(name);
CREATE INDEX idx_users_name2 ON users(name); -- duplicate
```
**Explanation:** Two indexes covering the same key cost double the storage and writes with zero extra read benefit; drop the extra.

## Q41: Should a boolean column with a skewed distribution get an index?
**Query:**
```sql
-- PostgreSQL: only index the rare value
CREATE INDEX idx_users_deleted ON users(is_deleted) WHERE is_deleted;
SELECT * FROM users WHERE is_deleted;
```
**Explanation:** Indexing the common value helps nobody (seq scan wins); a partial index over just the rare rows is small and seekable.
**Alt1:** MySQL 8 filtered lookalike: put the stacking condition in a generated column or use `(is_deleted, created_at)` composite.

## Q42: How much space does an index take and why care?
**Query:**
```sql
-- PostgreSQL: on-disk size of the index
SELECT pg_size_pretty(pg_relation_size('idx_orders_user'));
-- MySQL: InnoDB index pages in the buffer pool
SELECT INDEX_NAME, INDEX_TYPE FROM information_schema.STATISTICS WHERE TABLE_NAME='orders';
```
**Explanation:** Indexes live on disk and race for the shared buffer pool; oversized/unused indexes evict hot pages and bloat backups.

## Q43: What is keyset (seek) pagination and how does the index support it?
**Query:**
```sql
CREATE INDEX idx_orders_id ON orders(id);
SELECT * FROM orders WHERE id > 1000 ORDER BY id LIMIT 50; -- next page: start at >1050
```
**Explanation:** Each page resumes from the last cursor with an index seek, so cost stays flat no matter how deep you go.
**Alt1:** With a composite cursor: `WHERE (id) > (last_id) ORDER BY id LIMIT 50` — keeps it fully index-based.

## Q44: Why is OFFSET pagination slow on huge tables?
**Query:**
```sql
SELECT * FROM orders ORDER BY id LIMIT 20 OFFSET 100000;
```
**Explanation:** The engine fetches and discards 100k index rows before returning 20 — cost grows linearly with the page number.

## Q45: Several single-column indexes vs one composite index?
**Query:**
```sql
CREATE INDEX ix_orders_user  ON orders(user_id);
CREATE INDEX ix_orders_total ON orders(total);
SELECT * FROM orders WHERE user_id = 5 AND total > 100;
```
**Explanation:** Each B-tree covers one predicate; an `(user_id, total)` composite serves the AND in one structure. MySQL 8 may "Index merge" the singles, often worse.
**Alt1:** For two equality predicates, the composite usually needs only one seek where index-merge logic spends more work.

## Q46: Do foreign-key columns get an index automatically?
**Query:**
```sql
CREATE TABLE order_items (
  id BIGINT PRIMARY KEY,
  order_id BIGINT,
  CONSTRAINT fk_oi FOREIGN KEY (order_id) REFERENCES orders(id)
);
CREATE INDEX idx_order_items_order ON order_items(order_id);
```
**Explanation:** PostgreSQL and SQL Server do *not* auto-index FK columns (InnoDB creates one if missing); always verify the child side to protect the join and parent `DELETE`.

## Q47: How do you verify an index is actually used from EXPLAIN?
**Query:**
```sql
EXPLAIN SELECT * FROM users WHERE email = 'a@b.com';
CREATE INDEX idx_users_email ON users(email);
EXPLAIN SELECT * FROM users WHERE email = 'a@b.com'; -- now "Index Seek" / "Index Only Scan"
```
**Explanation:** Compare before/after: watch for `Seq Scan`/`Full Scan` (not used) vs `Index Seek` + optional `Key/RID Lookup`.

## Q48: What is index fragmentation?
**Query:**
```sql
-- SQL Server: fragmentation per index
SELECT * FROM sys.dm_db_index_physical_stats(DB_ID(), OBJECT_ID('orders'), NULL, NULL, 'DETAILED');
ALTER INDEX ix_orders_user ON orders REORGANIZE; -- light; REBUILD for heavy
```
**Explanation:** When leaf-page order no longer matches key order (after churn), scans read scattered pages — extra I/O that a reorganize/rebuild fixes.

## Q49: In a composite index, which column comes first?
**Query:**
```sql
CREATE INDEX idx_orders_usr_dt ON orders(user_id, created_at);
EXPLAIN SELECT * FROM orders
WHERE user_id = 5 AND created_at > '2024-01-01'
ORDER BY created_at;
```
**Explanation:** Put the equality column first (narrow the tree), then the range/sort column; reversed, the leading range cancels the seek.

## Q50: What is the cost of a covering index (write amplification)?
**Query:**
```sql
CREATE INDEX idx_orders_cover ON orders(user_id, total) INCLUDE (status, shipped_at);
-- every INSERT/UPDATE now also writes this wide leaf + key
```
**Explanation:** Wider indexes mean every write touches more pages and every batch consumes more space — reserve them for genuinely hot read paths.
**Alt1:** Balance: keep INCLUDE columns to only what the report needs; adding columns "just in case" multiplies write cost.

## Q51: A slow query filters 3+ columns — what index do you add?
**Query:**
```sql
-- SQL Server / PostgreSQL 11+: equality + range in the key, the rest INCLUDE'd
CREATE INDEX idx_orders_usr_date ON orders(user_id, created_at) INCLUDE (total, status);
-- MySQL has no INCLUDE: fold them into the key (bigger index)
CREATE INDEX idx_orders_usr_date_all ON orders(user_id, created_at, total, status);
SELECT total FROM orders WHERE user_id = 5 AND created_at >= '2024-01-01' AND created_at < '2024-02-01';
```
**Explanation:** Equality first, then one range — remaining columns ride in the leaf so the answer is fully covered.

## Q52: Rewrite a function-heavy date filter so the index can fire.
**Query:**
```sql
CREATE INDEX idx_orders_created ON orders(created_at);
-- Before: DATE(created_at) prevents an index seek (MySQL)
SELECT * FROM orders WHERE DATE(created_at) = '2024-05-01';
-- After: bare column, half-open range
SELECT * FROM orders WHERE created_at >= '2024-05-01' AND created_at < '2024-05-02';
```
**Explanation:** Comparing a transformed column breaks the tree; a constant range keeps the raw key in the predicate.
**Alt1:** Same trick for SQL Server: `created_at >= '2024-05-01' AND created_at < '2024-05-02'` beats `CONVERT(date, created_at)` every time.

## Q53: Can a partial index and an expression index be combined (PostgreSQL)?
**Query:**
```sql
CREATE INDEX idx_users_la ON users(lower(email)) WHERE is_active;
SELECT * FROM users WHERE is_active AND lower(email) = 'a@b.com';
```
**Explanation:** Yes — the predicate bounds which rows live in the tree and the expression defines its keys; the planner matches both parts.

## Q54: How does collation affect whether an index is usable?
**Query:**
```sql
-- PostgreSQL: force a binary sort order for the index
CREATE INDEX idx_users_lastname ON users(last_name COLLATE "C");
SELECT * FROM users WHERE last_name > 'Baker';
```
**Explanation:** The B-tree order follows the collation; queries compared with a different collation may not match the same ordering.

## Q55: Random UUID primary key vs auto-increment in InnoDB?
**Query:**
```sql
CREATE TABLE uuid_events (id CHAR(36) PRIMARY KEY, payload JSON) ENGINE=InnoDB;
-- random inserts split pages constantly -> use monotonic PK + separate unique index:
CREATE TABLE events (id BIGINT AUTO_INCREMENT PRIMARY KEY, uid CHAR(36), UNIQUE KEY uk_uid (uid)) ENGINE=InnoDB;
```
**Explanation:** InnoDB rows are stored in primary-key order; random UUID writes cause page splits and index hurn — keep the UUID a unique secondary index.

## Q56: Why does the planner choose a full scan even though an index exists?
**Query:**
```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE status = 'new';
ANALYZE orders; -- refresh stats, re-explain
```
**Explanation:** If most rows match (or the histogram is stale), per-row seeks lose to a sequential scan; the planner trusts its cardinality estimate.

## Q57: Can the engine combine two indexes for an OR condition?
**Query:**
```sql
CREATE INDEX idx_orders_user   ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
SELECT * FROM orders WHERE user_id = 1 OR status = 'void';
-- PostgreSQL: BitmapOr of two bitmap scans; Oracle: bitmap convert
```
**Explanation:** OR means the engine cannot use one tree; it scans both indexes and merges the row-id sets before fetching the heap.

## Q58: Indexing jsonb paths with GIN (PostgreSQL).
**Query:**
```sql
CREATE INDEX idx_orders_meta ON orders USING gin (metadata jsonb_path_ops);
SELECT * FROM orders WHERE metadata @> '{"sku": "A-1"}';
```
**Explanation:** `jsonb_path_ops` builds a smaller, faster inverted index for `@>` containment on that property.

## Q59: MySQL 8 functional index directly over a JSON expression.
**Query:**
```sql
CREATE INDEX idx_orders_sku ON orders((JSON_UNQUOTE(JSON_EXTRACT(metadata, '$.sku'))));
SELECT * FROM orders WHERE JSON_UNQUOTE(JSON_EXTRACT(metadata, '$.sku')) = 'A-1';
```
**Explanation:** MySQL 8.0.13+ accepts expression key parts, so no generated column is needed for indexed JSON lookups.

## Q60: Indexing a JSON value in SQL Server.
**Query:**
```sql
ALTER TABLE orders ADD sku AS JSON_VALUE(metadata, '$.sku') PERSISTED;
CREATE INDEX ix_orders_sku ON orders(sku);
SELECT * FROM orders WHERE sku = 'A-1';
```
**Explanation:** SQL Server stores JSON as text; expose the property as a computed column and index that for seeks.

## Q61: GIN vs B-tree for the same jsonb column — when each wins.
**Query:**
```sql
CREATE INDEX idx_json_g ON orders USING gin(metadata);
CREATE INDEX idx_json_b ON orders USING btree(metadata);
SELECT * FROM orders WHERE metadata = '{"a": 1}'::jsonb;      -- exact: btree fine
SELECT * FROM orders WHERE metadata @> '{"b": 2}';            -- containment: gin
```
**Explanation:** Whole-document equality uses a B-tree seek; queries touching interior keys need the GIN inverted structure.

## Q62: Composite index order plus a LIKE on the second key.
**Query:**
```sql
CREATE INDEX idx_orders_usr_sku ON orders(user_id, sku);
SELECT * FROM orders WHERE user_id = 5 AND sku LIKE 'A%';
```
**Explanation:** The equality on `user_id` lands one subtree, then the prefix `LIKE 'A%'` walks a contiguous range of `sku` keys.

## Q63: Avoid a GROUP BY sort by streaming maxima over an index.
**Query:**
```sql
CREATE INDEX idx_orders_usr_ts ON orders(user_id, created_at);
EXPLAIN SELECT user_id, MAX(created_at) FROM orders GROUP BY user_id;
-- PostgreSQL: Group Aggregate streams groups in order, no Sort node
```
**Explanation:** Pre-sorted groups (equal `user_id` adjacent) let the engine aggregate while walking the leaves once.

## Q64: The "seek is slow" pattern — fix with a covering index.
**Query:**
```sql
-- Before: Index Seek + N Key Lookups (random I/O per row)
EXPLAIN SELECT email, total FROM orders WHERE user_id = 5;
-- After: everything requested is in the leaf
CREATE INDEX idx_orders_cover ON orders(user_id) INCLUDE (email, total);
EXPLAIN SELECT email, total FROM orders WHERE user_id = 5; -- Index Only/Seek only
```
**Explanation:** A key lookup is a random heap fetch per matched row; putting those columns in the index kills the lookup.

## Q65: Indexing equality + sort column for a LIMIT query.
**Query:**
```sql
CREATE INDEX idx_orders_usr_dt ON orders(user_id, created_at);
SELECT * FROM orders WHERE user_id = 4 ORDER BY created_at LIMIT 10;
```
**Explanation:** The leading key matches the where, the trailing key provides the order — the engine reads only the first few pages.

## Q66: Ascending vs descending index parts (MySQL 8 / PostgreSQL / SQL Server).
**Query:**
```sql
CREATE INDEX idx_orders_dt_desc ON orders(created_at DESC); -- MySQL 8+ / PostgreSQL
SELECT * FROM orders ORDER BY created_at DESC LIMIT 5;
```
**Explanation:** A true DESC part reads forward for descending order; old MySQL had to reverse-scan, which broke some two-column sorts.

## Q67: Composite index that matches a mixed-direction ORDER BY.
**Query:**
```sql
CREATE INDEX idx_orders_u_d ON orders(user_id ASC, created_at DESC);
SELECT * FROM orders WHERE user_id = 3 ORDER BY created_at DESC;
```
**Explanation:** Ties in `user_id` are then ordered by `created_at DESC` inside the tree, so no explicit sort node appears.

## Q68: NULLS FIRST / LAST ordering vs index direction (PostgreSQL).
**Query:**
```sql
CREATE INDEX idx_users_email ON users(email DESC NULLS LAST);
SELECT * FROM users ORDER BY email DESC NULLS LAST;
```
**Explanation:** PostgreSQL matches the declared column null-direction in the index; a different null placement forces a sort.

## Q69: Stats say one row, the table has a million — what to do?
**Query:**
```sql
UPDATE STATISTICS dbo.orders;                    -- SQL Server
DBMS_STATS.GATHER_TABLE_STATS(USER, 'ORDERS');   -- Oracle
ANALYZE orders;                                  -- PostgreSQL
EXPLAIN SELECT * FROM orders WHERE user_id = 987654; -- re-check the plan
```
**Explanation:** A stale histogram underestimates matching rows and sends the planner down the wrong access path; refresh stats and re-inspect.

## Q70: How to list index bloat in PostgreSQL.
**Query:**
```sql
SELECT s.indexrelname,
       pg_size_pretty(pg_relation_size(s.indexrelid)) AS size,
       s.idx_scan, s.idx_tup_read, s.idx_tup_fetch
FROM pg_stat_user_indexes s
ORDER BY pg_relation_size(s.indexrelid) DESC;
```
**Explanation:** Dead entries from updates/deletes inflate the tree; a bloated index degrades fan-out, cache, and scan speed.

## Q71: What does "UNUSABLE" mean on an Oracle index?
**Query:**
```sql
ALTER INDEX ix_orders_user UNUSABLE;  -- definition kept, not used/maintained
ALTER INDEX ix_orders_user REBUILD;   -- restore usability
SELECT index_name, status FROM user_indexes WHERE status = 'UNUSABLE';
```
**Explanation:** Oracle stops using and maintaining the tree but keeps the definition; rebuild online later to restore it.

## Q72: Rebuilding an index without blocking writers (ONLINE).
**Query:**
```sql
ALTER INDEX ix_orders_user REBUILD ONLINE;                    -- Oracle
ALTER INDEX ix_orders_user REBUILD WITH (ONLINE = ON);        -- SQL Server
ALTER TABLE orders ADD INDEX idx_orders_user (user_id) ALGORITHM=INPLACE, LOCK=NONE; -- MySQL 8
```
**Explanation:** Online rebuilds keep DML flowing during the operation — online DDL in MySQL 8 is the default for most index changes.

## Q73: Equality-then-range vs range-then-equality — which ordering wins?
**Query:**
```sql
CREATE INDEX idx_orders_gi ON orders(group_id, item_id);
SELECT * FROM orders WHERE group_id = 5 AND item_id BETWEEN 10 AND 20 ORDER BY item_id;
-- reversed (item_id BETWEEN... AND group_id=5) would waste the leading key
```
**Explanation:** Keep equality first; a leading range degenerates into scanning the whole btree and filtering the rest.

## Q74: The query uses the index but is still slow — what next?
**Query:**
```sql
EXPLAIN FORMAT=TREE SELECT * FROM orders WHERE user_id = 5001; -- MySQL
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = 5001; -- PostgreSQL
```
**Explanation:** Inspect rows examined and buffers; if a Key Lookup dominates, add the fetched columns as INCLUDE/leaf columns via a covering index.

## Q75: Should a low-cardinality status column get its own index for a GROUP BY?
**Query:**
```sql
CREATE INDEX idx_orders_status ON orders(status); -- 8 distinct values
EXPLAIN SELECT status, COUNT(*) FROM orders GROUP BY status;
-- likely a Seq Scan: one pass over the heap beats per-key index hops
```
**Explanation:** With very few groups, a single sequential scan wins; the index would loop between distinct values for no gain.

## Q76: Design indexes for a join-heavy report.
**Query:**
```sql
EXPLAIN ANALYZE
SELECT SUM(o.total) FROM orders o
JOIN users u ON u.id = o.user_id
WHERE u.country = 'DE';
-- 1) shrink the driving side first:
CREATE INDEX idx_users_country ON users(country);
-- 2) then make the probe cheap:
CREATE INDEX idx_orders_user ON orders(user_id);
```
**Explanation:** Restrict the outer table before joining so few probes happen; join-side FK indexes make each probe a seek.

## Q77: Two range predicates in one WHERE — one B-tree can't serve both.
**Query:**
```sql
CREATE INDEX idx_orders_dt_amt ON orders(created_at, amount);
SELECT * FROM orders
WHERE created_at BETWEEN '2024-01-01' AND '2024-02-01'
  AND amount > 100;
```
**Explanation:** The btree can seek on the first column, then `amount` is only a residual filter; choose which column should narrow the scan.
**Alt1:** Swap the order if `amount` is the rarer gate: `CREATE INDEX idx_orders_amt_dt ON orders(amount, created_at);`.

## Q78: Functional + partial + composite in one PostgreSQL index.
**Query:**
```sql
CREATE INDEX idx_users_la ON users(lower(email), is_active) WHERE is_active;
SELECT * FROM users WHERE is_active AND lower(email) LIKE 'a@%';
```
**Explanation:** The expression key is the seekable range and the WHERE clause prunes the rows stored — small tree, prefix-friendly.

## Q79: Covering index vs per-column indexes — which truly "covers"?
**Query:**
```sql
-- Covers filter + projection in ONE tree:
CREATE INDEX idx_orders_cov ON orders(user_id, total) INCLUDE (created_at);
-- ... vs separate trees that must be merged:
CREATE INDEX idx_orders_u ON orders(user_id);
CREATE INDEX idx_orders_t ON orders(total);
```
**Explanation:** A covering index answers entirely from its own leaf pages; separate indexes require merge/lookup logic that is never "covered".

## Q80: INCLUDE vs putting the column in the key — when either?
**Query:**
```sql
CREATE INDEX ix_orders_s ON orders(user_id, total) INCLUDE (status); -- cover only
-- vs keyed: can also sort/filter by status
CREATE INDEX ix_orders_all ON orders(user_id, total, status);
```
**Explanation:** Keyed columns steer seek/sort and stay order-sensitive; INCLUDE columns only tide over lookups and keep the key small.

## Q81: MAX() answered by a backward index scan.
**Query:**
```sql
CREATE INDEX idx_logs_ts ON logs(created_at);
EXPLAIN (ANALYZE) SELECT MAX(created_at) FROM logs; -- reads the last leaf page
```
**Explanation:** The leaf chain is sorted, so the engine grabs the final key instead of scanning the table.

## Q82: MAX() per group quickly using a composite prefix.
**Query:**
```sql
CREATE INDEX idx_orders_ugp ON orders(user_id, created_at);
EXPLAIN SELECT user_id, MAX(created_at) FROM orders GROUP BY user_id;
```
**Explanation:** Same trick per partition: groups are contiguous and their last key is the max, so no sort or hash aggregate is needed.

## Q83: Indexing arrays of tags with GIN + containment.
**Query:**
```sql
CREATE INDEX idx_posts_tags ON posts USING gin(tags); -- tags text[]
SELECT * FROM posts WHERE tags @> ARRAY['sql'];
```
**Explanation:** GIN flips "each element → rows," so `@>` element containment is one probe, not a full scan.

## Q84: Full-text queries must keep the index's exact expression.
**Query:**
```sql
CREATE INDEX idx_docs_fts ON docs USING gin(to_tsvector('english', body));
SELECT * FROM docs
WHERE to_tsvector('english', body) @@ plainto_tsquery('english', 'index AND interview');
```
**Explanation:** The predicate must spell out the same `to_tsvector(...)` expression as the index, or the planner loses the match.

## Q85: Indexing text for substring-heavy search with MySQL FULLTEXT + ngram.
**Query:**
```sql
CREATE FULLTEXT INDEX ftx_docs_body ON docs(body) WITH PARSER ngram;
SELECT id FROM docs WHERE MATCH(body) AGAINST('"covering index"' IN BOOLEAN MODE);
```
**Explanation:** The ngram parser tokenizes CJK and partial input; boolean mode adds phrase/wildcard operators over the inverted index.

## Q86: MySQL builds indexes while sorting — batch them.
**Query:**
```sql
-- One statement incurs a single sorted build pass:
ALTER TABLE orders ADD INDEX a (user_id), ADD INDEX b (created_at);
-- avoid adding indexes one-by-one in a loop
```
**Explanation:** Grouping index DDL reuses one table scan/sort and one page rewrite instead of rebuilding over and over.

## Q87: Decide whether to index for this slow reporting query.
**Query:**
```sql
SELECT total FROM orders
WHERE created_at >= '2024-01-01' AND created_at < '2024-02-01' AND status = 'paid';
-- Add: range key first, filter second, projection covered
CREATE INDEX ix_orders_rpt ON orders(created_at, status) INCLUDE (total); -- SQL Server
CREATE INDEX idx_orders_rpt ON orders(created_at, status, total);         -- PostgreSQL / MySQL
EXPLAIN SELECT total FROM orders WHERE ...; -- now Index Scan, no Key Lookup
```
**Explanation:** One seek over the date window, `status` filters inside the tree, and every needed column is in the leaf.

## Q88: Detect unused/redundant indexes with catalog queries.
**Query:**
```sql
-- MySQL 8: ready-made redundancy report
SELECT * FROM sys.schema_redundant_indexes;
-- PostgreSQL: find candidates by scan count
SELECT indexrelid::regclass, idx_scan FROM pg_stat_user_indexes ORDER BY idx_scan LIMIT 10;
```
**Explanation:** Indexes with near-zero `idx_scan` cost writes and cache for nothing; confirm no hidden use, then drop.

## Q89: Oracle function-based index for case-insensitive lookups.
**Query:**
```sql
CREATE INDEX idx_users_uname ON users(UPPER(username));
SELECT * FROM users WHERE UPPER(username) = 'JOHN';
```
**Explanation:** Oracle matches the expression literally; a stored transformed value turns the predicate into a seek.

## Q90: LIKE that stays fast under a non-deterministic collation (PostgreSQL).
**Query:**
```sql
CREATE INDEX idx_users_last ON users(last_name varchar_pattern_ops);
SELECT * FROM users WHERE last_name LIKE 'Ba%';
```
**Explanation:** The default text operator class sorts by locale rules where a prefix isn't a clean range; the `varchar_pattern_ops` class enables plain byte-order prefix seeks.

## Q91: FILLFACTOR + HOT updates keep the heap hot (PostgreSQL).
**Query:**
```sql
ALTER TABLE orders SET (fillfactor = 70);
UPDATE orders SET total = total * 1.1 WHERE user_id = 3; -- stays in page (HOT)
ANALYZE orders;
```
**Explanation:** Reserved free space allows in-place row updates (HOT), which leave index pointers valid and slash index writes and bloat.

## Q92: One covering index serving WHERE + GROUP BY + SELECT together.
**Query:**
```sql
CREATE INDEX idx_orders_report ON orders(user_id, created_at) INCLUDE (total); -- PG 11+ / SQL Server
EXPLAIN (ANALYZE)
SELECT user_id, SUM(total) FROM orders
WHERE created_at >= '2024-01-01' AND created_at < '2024-07-01'
GROUP BY user_id ORDER BY user_id;
```
**Explanation:** The date range is an index scan on the covered tree, groups stream in `user_id` order, and `total` is summed from leaves — one structure, no heap, no sort.

## Q93: Index skip scan for a DISTINCT over the second key (MySQL 8.0.13+).
**Query:**
```sql
CREATE INDEX idx_orders_uid_dt ON orders(user_id, created_at);
SELECT DISTINCT user_id FROM orders WHERE created_at > '2024-06-01';
```
**Explanation:** Instead of a full index scan, the engine probes each distinct leading value inside the searched range — the planner decides, and it only helps when few groups exist.

## Q94: Why the planner ignores an index on a tiny table.
**Query:**
```sql
CREATE TABLE small (id INT PRIMARY KEY, x INT);
CREATE INDEX idx_small_x ON small(x);
EXPLAIN (ANALYZE) SELECT * FROM small WHERE x = 7; -- still Seq Scan
```
**Explanation:** One page read beats the two-hop index path; cost modeling says the index only pays off past a size/selectivity crossing point.

## Q95: When to drop an index — evidence from usage stats (SQL Server).
**Query:**
```sql
SELECT * FROM sys.dm_db_index_usage_stats
WHERE object_id = OBJECT_ID('orders') ORDER BY user_seeks DESC;
-- high fragmentation candidates:
SELECT object_id, index_id, avg_fragmentation_in_percent
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED')
WHERE avg_fragmentation_in_percent > 30;
```
**Explanation:** Decisions rest on seeks/updates per index; zero-use indexes go, heavily fragmented ones get a rebuild.

## Q96: Indexing a time-zone conversion requires the same expression in the query.
**Query:**
```sql
CREATE INDEX idx_evt_local ON events((created_at AT TIME ZONE 'UTC'));
EXPLAIN SELECT * FROM events
WHERE (created_at AT TIME ZONE 'UTC') BETWEEN '2024-01-01' AND '2024-01-02';
```
**Explanation:** Expression indexes only fire when the query repeats the exact expression; wrap both sides identically.

## Q97: DESC + NULLS LAST matching a keyset pagination cursor.
**Query:**
```sql
CREATE INDEX idx_events_ts ON events(ts DESC NULLS LAST);
SELECT * FROM events
WHERE (ts, id) < ('2024-06-01 00:00', 999)
ORDER BY ts DESC, id DESC LIMIT 50;
```
**Explanation:** The row-comparison cursor plus matching direction makes each page resume with an index seek instead of OFFSET scanning.

## Q98: Aggregating a date range entirely inside a covering index.
**Query:**
```sql
CREATE INDEX idx_orders_rpt ON orders(created_at, status) INCLUDE (total, tax);
EXPLAIN ANALYZE
SELECT SUM(total + tax) FROM orders
WHERE created_at >= '2024-01-01' AND created_at < '2024-02-01' AND status = 'paid';
```
**Explanation:** Range-seek the first key, residual-filter `status`, then add the included numeric columns straight from the leaves.

## Q99: Which index to add first for an unknown slow query?
**Query:**
```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;   -- PostgreSQL: see the dominant node
EXPLAIN ANALYZE SELECT ...;              -- MySQL
SET STATISTICS IO ON; SELECT ...;        -- SQL Server
-- then create and re-explain:
CREATE INDEX idx_probe ON t(leading_equality_col, leading_range_col);
```
**Explanation:** Pick the index that removes the biggest plan node — a Seq Scan becomes a seek, a Sort vanishes, Key Lookups disappear.

## Q100: Anti-pattern: an index on every column — and the right fix.
**Query:**
```sql
-- DON'T: sprinkle indexes over every column
CREATE INDEX uxc1 ON users(col1); CREATE INDEX uxc2 ON users(col2); /* ... */
-- DO: one covering composite aimed at the real statement
CREATE INDEX idx_orders_cover2 ON orders(user_id, created_at) INCLUDE (total);
SELECT user_id, SUM(total) FROM orders
WHERE created_at >= '2024-01-01' AND created_at < '2024-04-01'
GROUP BY user_id;
```
**Explanation:** Every extra index slows every insert/update and eats cache; a single well-shaped covering index solves whole read patterns.
