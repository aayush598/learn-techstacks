# SQLite Interview Questions and Answers

## Q1: What is SQLite?
**A:** SQLite is a self-contained, serverless, zero-configuration, transactional SQL database engine. It is embedded into applications as a library rather than running as a separate process, storing the entire database as a single cross-platform file on disk.

## Q2: How does SQLite differ from client-server databases like PostgreSQL or MySQL?
**A:** SQLite is serverless (embedded directly into the application), requires no configuration or administration, stores data in a single file, and is designed for low-memory environments. Client-server databases run as separate processes, support concurrent write connections from multiple clients, and offer more advanced features like replication and user management.

## Q3: What are the data types in SQLite?
**A:** SQLite uses dynamic typing with five storage classes: NULL, INTEGER, REAL (floating-point), TEXT (strings), and BLOB (binary data). SQLite does not have dedicated BOOLEAN or DATE/TIME types; booleans are stored as integers (0/1) and dates as TEXT, REAL, or INTEGER.

## Q4: What is type affinity in SQLite?
**A:** Type affinity is the recommended type for a column, but SQLite does not enforce it strictly. Affinities include: TEXT, NUMERIC, INTEGER, REAL, and BLOB. For example, a column with INTEGER affinity can still store text if the application inserts a string value.

## Q5: What is AUTOINCREMENT in SQLite?
**A:** AUTOINCREMENT is a keyword that ensures the `ROWID` assigned to new rows is monotonically increasing and never reuses a previously deleted ROWID. Without AUTOINCREMENT, SQLite may reuse ROWIDs from deleted rows. It is only allowed on columns declared as `INTEGER PRIMARY KEY`.

## Q6: What is the maximum size of a SQLite database?
**A:** The maximum size of a SQLite database file is about 140 TB (2^48 bytes, 256 TB theoretically, but practically 140 TB due to page size limits). The maximum number of pages is 2^32 - 2, and the default page size is 4096 bytes.

## Q7: What is WAL mode in SQLite?
**A:** Write-Ahead Logging (WAL) mode improves concurrent read performance by allowing readers to access the database while a writer is active. Instead of writing directly to the database file, changes are appended to a separate WAL file. WAL mode is significantly faster than the traditional rollback journal for most workloads.

## Q8: What are the different journal modes in SQLite?
**A:** SQLite supports DELETE (default, rollback journal is deleted on commit), TRUNCATE (journal is truncated), PERSIST (journal is overwritten), MEMORY (journal stored in memory), WAL (write-ahead logging), and OFF (no journal, no atomic commit). WAL is recommended for most concurrent read workloads.

## Q9: What is a transaction in SQLite?
**A:** A transaction is a sequence of SQL operations that are executed atomically — either all changes are committed or none are applied. SQLite supports three transaction types: DEFERRED (waits for first read/write to acquire lock), IMMEDIATE (acquires reserved lock immediately), and EXCLUSIVE (acquires exclusive lock immediately).

## Q10: How does SQLite handle concurrent writes?
**A:** SQLite uses file-level locking. Only one writer can hold an exclusive lock at a time. Multiple readers can read concurrently, but any write will block other writers and readers (in exclusive mode). WAL mode allows concurrent reads during writes but still serializes writes.

## Q11: What is the difference between `PRAGMA journal_mode=WAL` and `PRAGMA journal_mode=DELETE`?
**A:** In WAL mode, writes append to a WAL file and readers can still read the main database file concurrently. In DELETE mode, each write creates a rollback journal, and readers are blocked during writes. WAL provides better concurrent read performance.

## Q12: What is `VACUUM` in SQLite?
**A:** `VACUUM` rebuilds the database file, reclaiming unused space and defragmenting pages. It creates a new database file, copies all content, and replaces the original. It is necessary because SQLite does not automatically return freed pages to the operating system.

## Q13: What is `PRAGMA` in SQLite?
**A:** `PRAGMA` statements modify SQLite's behavior or return metadata about the database. Examples: `PRAGMA journal_mode=WAL`, `PRAGMA page_size=4096`, `PRAGMA synchronous=NORMAL`, `PRAGMA foreign_keys=ON`.

## Q14: How do you enable foreign key constraints in SQLite?
**A:** Foreign key constraints are not enabled by default. They must be enabled per connection using `PRAGMA foreign_keys = ON`. This cannot be set at the database level — it must be set after each connection is opened.

## Q15: What are common table expressions (CTEs) in SQLite?
**A:** CTEs are temporary named result sets within a single SQL statement, defined using the `WITH` clause. SQLite supports recursive CTEs, which are powerful for traversing hierarchical or tree-structured data.

## Q16: What is a recursive CTE, and how is it used in SQLite?
**A:** A recursive CTE references itself in its definition. It consists of a non-recursive term (base case) and a recursive term joined by `UNION ALL`. It is commonly used for organizational charts, bill of materials, or any hierarchical tree traversal.

## Q17: What indexes does SQLite support?
**A:** SQLite supports B-tree indexes (default), UNIQUE indexes, partial indexes (with `WHERE` clause), covering indexes, descending indexes, and expression-based indexes (since version 3.9.0). It does not support hash indexes, spatial indexes natively, or clustered indexes other than the implicit ROWID index.

## Q18: What is a partial index in SQLite?
**A:** A partial index indexes only rows that satisfy a `WHERE` clause. It saves space and improves performance for queries that target a subset of data. For example: `CREATE INDEX idx_active ON users(created_at) WHERE active = 1;`

## Q19: What is an expression-based index in SQLite?
**A:** An expression-based index indexes the result of an expression rather than a column. For example: `CREATE INDEX idx_lower_name ON users(LOWER(name));` enables fast searches using `WHERE LOWER(name) = 'john'`.

## Q20: How does SQLite handle full-text search?
**A:** SQLite provides the FTS5 (Full-Text Search) extension, which creates virtual tables for text indexing. FTS5 supports tokenization, stemming, prefix queries, phrase queries, and ranking. It is ideal for implementing search within applications.

## Q21: What is the FTS5 virtual table?
**A:** FTS5 is a virtual table module for full-text indexing and search in SQLite. It creates an inverted index over text content and supports the `MATCH` operator for searching. It can be customized with tokenizers, content tables, and ranking functions.

## Q22: What is the difference between `FTS3`, `FTS4`, and `FTS5`?
**A:** FTS5 is the latest version (recommended), offering better tokenizers, column-specific searches, and ranking. FTS4 adds performance improvements over FTS3 and supports `matchinfo`. FTS3 is the legacy module. FTS5 is not backward-compatible with FTS3/4 syntax.

## Q23: What is a virtual table in SQLite?
**A:** A virtual table is a table-like interface that provides custom data access logic without storing data in the traditional database file. Examples: FTS tables for full-text search, `dbstat` for database statistics, `pragma_table_info`, and `generate_series`.

## Q24: What is the `LIKE` operator behavior in SQLite?
**A:** `LIKE` performs pattern matching with `%` (any sequence) and `_` (single character) wildcards. By default, `LIKE` in SQLite is case-insensitive for ASCII characters but case-sensitive for Unicode. This behavior can be changed with `PRAGMA case_sensitive_like=ON`.

## Q25: What is the `GLOB` operator in SQLite?
**A:** `GLOB` is similar to `LIKE` but uses Unix-style globbing: `*` matches any sequence (like `%` in LIKE), `?` matches any single character (like `_`), and `[...]` matches character ranges. `GLOB` is always case-sensitive.

## Q26: What is the `IN` operator in SQLite?
**A:** The `IN` operator checks whether a value matches any value in a list or subquery. For example: `SELECT * FROM users WHERE id IN (1, 2, 3)`. SQLite optimizes `IN` with a list of values by sorting them and using binary search.

## Q27: How does SQLite handle NULL values?
**A:** NULL in SQLite represents a missing or unknown value. NULL comparisons use IS NULL / IS NOT NULL (not `= NULL`). In sorting, NULLs are considered smaller than any non-NULL value by default. In UNIQUE constraints, each NULL is considered distinct (multiple NULLs are allowed).

## Q28: What is the difference between `UNION` and `UNION ALL` in SQLite?
**A:** `UNION` combines result sets and removes duplicate rows (requiring sorting). `UNION ALL` combines result sets without deduplication. `UNION ALL` is faster because it avoids the sorting overhead.

## Q29: What are triggers in SQLite?
**A:** Triggers are SQL statements that automatically execute in response to INSERT, UPDATE, DELETE, or INSTEAD OF events on a table or view. SQLite supports BEFORE, AFTER, and INSTEAD OF triggers, both row-level (FOR EACH ROW) and statement-level triggers.

## Q30: What is the maximum number of rows in a SQLite table?
**A:** There is no practical limit on the number of rows. The theoretical maximum is 2^64 (about 1.8e19) rows. Practical limits depend on disk space, memory, and performance. The maximum number of tables is limited to about 2 billion (2^31 - 1).

## Q31: What is the maximum number of columns in a SQLite table?
**A:** The maximum number of columns is 32767 (2^15 - 1), but the practical limit is lower (around 2000) due to the maximum record size (about 1 billion bytes) and decoding overhead.

## Q32: How does SQLite implement `ALTER TABLE`?
**A:** SQLite supports a limited subset of `ALTER TABLE`: `ALTER TABLE ... RENAME TO`, `ALTER TABLE ... ADD COLUMN`, and `ALTER TABLE ... DROP COLUMN` (since 3.35.0). To rename a column or modify constraints, you must recreate the table using `CREATE TABLE` + `INSERT INTO ... SELECT` + `DROP TABLE`.

## Q33: What is the `sqlite_master` table?
**A:** The `sqlite_master` table is a system catalog that stores the schema of the database, including table definitions, index definitions, view definitions, and trigger definitions. You can query it directly: `SELECT * FROM sqlite_master WHERE type='table';`

## Q34: What is `sqlite3` command-line tool?
**A:** `sqlite3` is the official command-line interface for SQLite. It allows executing SQL queries, importing/exporting data, configuring pragmas, and performing database administration tasks. Common commands: `.tables`, `.schema`, `.dump`, `.import`, `.output`.

## Q35: How do you import a CSV file into SQLite?
**A:** Using the `.import` command in the sqlite3 CLI: `.mode csv` then `.import /path/to/file.csv table_name`. Or programmatically: iterate through CSV rows and use INSERT statements, or use third-party tools.

## Q36: How do you export data from SQLite?
**A:** Methods include: (1) `.dump` command exports the entire database as SQL statements, (2) `.output` + SQL query exports query results, (3) `.mode csv` + `.output file.csv` exports CSV, (4) `.backup` creates a binary copy, (5) `.clone` clones the database.

## Q37: What is the `.dump` command in sqlite3?
**A:** The `.dump` command outputs SQL statements that can recreate the entire database, including schema and data. This is the standard way to create portable backups. The output can be piped back into sqlite3 to restore the database.

## Q38: What is the difference between `INTEGER PRIMARY KEY` and `INT PRIMARY KEY` in SQLite?
**A:** `INTEGER PRIMARY KEY` (with the exact word INTEGER) creates an alias for the rowid column, making it the true primary key with automatic auto-increment behavior. `INT PRIMARY KEY` (INT without the ER suffix) creates a regular column with a unique index but does not alias rowid.

## Q39: What is the rowid in SQLite?
**A:** Every row in SQLite (except in `WITHOUT ROWID` tables) has a unique 64-bit signed integer rowid. It is accessible as `rowid`, `_rowid_`, or `oid`. Tables with `INTEGER PRIMARY KEY` auto-increment use rowid as the primary key.

## Q40: What are WITHOUT ROWID tables?
**A:** `WITHOUT ROWID` tables use a B-tree keyed on the primary key directly rather than a separate rowid. They are useful when the primary key is not an integer or when you want to cluster data by the primary key. They require an explicit PRIMARY KEY.

## Q41: What is `PRAGMA synchronous` in SQLite?
**A:** `PRAGMA synchronous` controls how aggressively SQLite flushes data to disk. Modes: `0` or `OFF` (no synchronization, fastest but risk of corruption on crash), `1` or `NORMAL` (synchronizes at critical moments, balanced), `2` or `FULL` (full synchronization, safest but slower), `3` or `EXTRA` (extra synchronization in WAL mode).

## Q42: What is the `EXPLAIN QUERY PLAN` command?
**A:** `EXPLAIN QUERY PLAN` shows how SQLite executes a query — which indexes are used, the order of table scans, and join strategies. It is the primary tool for query optimization and debugging slow queries.

## Q43: How does SQLite handle JOINs?
**A:** SQLite supports INNER, LEFT OUTER, CROSS, and NATURAL JOINs. It does not support RIGHT OUTER or FULL OUTER JOIN natively (these can be simulated with LEFT JOINs and UNION). SQLite uses a loop-join algorithm and may reorder tables for optimization.

## Q44: What is a subquery in SQLite?
**A:** A subquery is a query nested within another query. SQLite supports subqueries in SELECT (scalar), FROM (derived tables), WHERE (semi-join/anti-join), and EXISTS/IN clauses. Correlated subqueries reference columns from the outer query.

## Q45: What is the `EXISTS` operator?
**A:** `EXISTS` returns true if a subquery returns at least one row. It is often used with correlated subqueries for efficient existence checks. `NOT EXISTS` is sometimes more efficient than `NOT IN` because it short-circuits on the first match.

## Q46: What is the difference between `IN` and `EXISTS` in SQLite?
**A:** `IN` with a subquery evaluates the entire subquery to build a list, while `EXISTS` can short-circuit on the first match. `EXISTS` is typically more efficient with correlated subqueries. `IN` is simpler for static value lists.

## Q47: What is the `DEFAULT` keyword in SQLite?
**A:** `DEFAULT` specifies a default value for a column when no value is provided during INSERT. It can be a literal value, an expression, or one of the special keywords: `CURRENT_TIME`, `CURRENT_DATE`, `CURRENT_TIMESTAMP`, or `NULL`.

## Q48: What is a `CHECK` constraint?
**A:** A `CHECK` constraint ensures that all values in a column satisfy a boolean expression. For example: `CHECK (age >= 0)`. CHECK constraints are enforced on INSERT and UPDATE but not on existing data unless explicitly validated.

## Q49: What is the difference between `PRIMARY KEY` and `UNIQUE` constraints?
**A:** A table can have only one PRIMARY KEY (which implies NOT NULL and UNIQUE) but multiple UNIQUE constraints. PRIMARY KEY typically creates an index and may be used as the rowid alias. UNIQUE allows NULL values (multiple NULLs are allowed in SQLite).

## Q50: How do you create a composite primary key in SQLite?
**A:** Using the table-level constraint syntax: `CREATE TABLE orders (user_id INT, product_id INT, quantity INT, PRIMARY KEY (user_id, product_id))`. In a composite key, rowid is still generated unless WITHOUT ROWID is specified.

## Q51: What is the `REPLACE` conflict resolution?
**A:** `REPLACE` (or `INSERT OR REPLACE`) works by attempting an INSERT; if it violates a UNIQUE or PRIMARY KEY constraint, it DELETEs the conflicting row and then INSERTs the new row. This can change the rowid and trigger DELETE triggers.

## Q52: What is `INSERT OR IGNORE`?
**A:** `INSERT OR IGNORE` attempts an insert, and if any constraint violation occurs, it silently ignores the error and proceeds. When used with `INSERT ... SELECT`, rows that cause conflicts are skipped while others are inserted.

## Q53: What is `INSERT OR ROLLBACK`?
**A:** If a constraint violation occurs, the entire transaction is rolled back. This is the most strict conflict resolution. Other options include `ABORT` (default, rolls back current statement but not the transaction) and `FAIL` (aborts current statement).

## Q54: How does SQLite handle concurrent connections?
**A:** SQLite supports multiple concurrent read connections (shared cache mode). Write connections are serialized — only one writer at a time. WAL mode improves this by allowing concurrent reads during writes. For high-concurrency write workloads, client-server databases are more appropriate.

## Q55: What is shared cache mode in SQLite?
**A:** Shared cache mode allows multiple connections to the same database to share a single data cache. It enables table-level locking instead of database-level locking, allowing multiple readers and a single writer to coexist (with some restrictions).

## Q56: What is `SQLITE_BUSY` error?
**A:** The `SQLITE_BUSY` error occurs when a connection cannot acquire a lock because another connection holds it. It is common in concurrent environments. Solutions: use `sqlite3_busy_timeout()` to retry, use WAL mode, or reduce lock contention.

## Q57: What is the `sqlite3_busy_timeout()` function?
**A:** It sets a timeout (in milliseconds) for SQLite to wait before returning `SQLITE_BUSY`. When a lock is unavailable, SQLite will retry until the timeout expires. A reasonable timeout (e.g., 5000ms) can prevent busy errors in concurrent applications.

## Q58: How do you handle database migration in SQLite?
**A:** Migrations involve: (1) creating new tables with the desired schema, (2) copying data from old tables, (3) dropping old tables, (4) renaming new tables. Tools like Alembic (Python) or custom migration scripts handle this process, often wrapped in transactions.

## Q59: What is the `ATTACH DATABASE` command?
**A:** `ATTACH DATABASE` allows accessing multiple SQLite database files within a single connection. For example: `ATTACH DATABASE '/path/to/other.db' AS other;` enables cross-database queries like `SELECT * FROM main.table UNION SELECT * FROM other.table;`.

## Q60: What is the `DETACH DATABASE` command?
**A:** `DETACH DATABASE` detaches a previously attached database. It is used to close the connection to an attached database file. The main database is always named `main` and the temp database is `temp`.

## Q61: How do you encrypt a SQLite database?
**A:** SQLite does not natively support encryption. Encryption extensions include: SQLite Encryption Extension (SEE, commercial), SQLCipher (open-source, uses 256-bit AES), and wxSQLite3. These extensions encrypt the entire database file page-by-page.

## Q62: What is SQLCipher?
**A:** SQLCipher is an open-source extension that encrypts SQLite database files with AES-256 encryption. It uses a passphrase combined with PBKDF2 key derivation. It is transparent to the application — queries work normally with the encryption handled at the page level.

## Q63: What is the `json1` extension in SQLite?
**A:** The json1 extension provides JSON functions for storing, querying, and manipulating JSON data within SQLite. Functions include `json_extract()`, `json_set()`, `json_array()`, `json_object()`, `json_each()`, `json_insert()`, `json_replace()`, and `json_remove()`.

## Q64: Can SQLite handle JSON data efficiently?
**A:** Yes, with the json1 extension. Since 3.38.0, SQLite also supports the JSONB binary format for more efficient storage and manipulation. `json_extract()` with path expressions enables querying into JSON structures, and virtual generated columns can index JSON fields.

## Q65: What is `json_extract()` in SQLite?
**A:** `json_extract()` extracts a value from a JSON string using a path expression. For example: `json_extract('{"name":"John"}', '$.name')` returns `"John"`. It supports the `->` (returns JSON) and `->>` (returns SQL) operators.

## Q66: What is `json_each()` in SQLite?
**A:** `json_each()` is a table-valued function that expands a JSON array or object into rows. Each row represents an element with columns for `key`, `value`, `type`, `id`, `parent`, and `path`. It is useful for unnesting JSON arrays into relational form.

## Q67: How do you optimize SQLite for read-heavy workloads?
**A:** (1) Use appropriate indexes, (2) Enable WAL mode for concurrent reads, (3) Increase cache size (`PRAGMA cache_size`), (4) Use `VACUUM` to defragment, (5) Consider `PRAGMA mmap_size` for memory-mapped I/O, (6) Use covering indexes to avoid table lookups.

## Q68: How do you optimize SQLite for write-heavy workloads?
**A:** (1) Use WAL mode, (2) Batch writes into transactions, (3) Set `PRAGMA synchronous=OFF` or `=NORMAL` (with risk), (4) Use prepared statements, (5) Increase page size if writing large BLOBs, (6) Use `INSERT OR REPLACE` carefully.

## Q69: What is the significance of page size in SQLite?
**A:** Page size (default 4096 bytes) affects disk I/O, cache efficiency, and maximum database size. Smaller pages (1024) waste less space for small rows but cause more I/O for large rows. Larger pages (65536) are better for large BLOBs and sequential scans.

## Q70: What is the `mmap_size` pragma?
**A:** `PRAGMA mmap_size` controls the amount of memory used for memory-mapped I/O. When set, SQLite maps the database file into the process's address space, potentially improving read performance by avoiding system calls. It is particularly effective for read-heavy workloads.

## Q71: What is the `cache_size` pragma?
**A:** `PRAGMA cache_size` sets the maximum number of pages SQLite will keep in memory cache. Default is -2000 (2000 KB). Increasing cache size improves read performance for frequently accessed data but consumes more memory.

## Q72: What is the `temp_store` pragma?
**A:** `PRAGMA temp_store` controls where temporary tables and indexes are stored: `0` (default, uses compiled-in location), `1` (file-based), `2` (memory-based). Memory-based temporary storage is faster but may cause issues with very large temporary datasets.

## Q73: How do you back up a SQLite database programmatically?
**A:** Using the backup API (`sqlite3_backup_init`, `sqlite3_backup_step`, `sqlite3_backup_finish`). This creates a consistent snapshot of a live database without needing to stop writes. The `.backup` command in the CLI also uses this API.

## Q74: What is the difference between `.backup` and `.dump`?
**A:** `.backup` creates a binary copy of the database file (faster, preserves all features). `.dump` creates SQL text output (portable, readable, but slower to restore). `.backup` is preferred for creating exact replicas; `.dump` is preferred for portability across SQLite versions.

## Q75: What are common SQLite performance pitfalls?
**A:** (1) Not using transactions around bulk inserts (each INSERT is an implicit transaction), (2) Missing indexes on frequently queried columns, (3) Overusing `LIKE '%...'` (cannot use indexes), (4) Using excessive triggers, (5) Not using WAL mode for concurrent access, (6) Running `VACUUM` too frequently.

## Q76: What is the `GROUP_CONCAT` function?
**A:** `GROUP_CONCAT` is an aggregate function that concatenates values from a group into a string. For example: `SELECT GROUP_CONCAT(name, ', ') FROM users;` returns all user names separated by commas. The separator defaults to `,` and can be customized.

## Q77: What is the `WINDOW` function support in SQLite?
**A:** SQLite supports window functions (since 3.25.0), including `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `NTILE()`, `LAG()`, `LEAD()`, `FIRST_VALUE()`, `LAST_VALUE()`, and aggregate functions with `OVER` clauses for partitioning and ordering.

## Q78: What is `ROW_NUMBER()` in SQLite?
**A:** `ROW_NUMBER()` is a window function that assigns a unique sequential integer to each row within a partition. For example: `SELECT ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rank FROM employees;`

## Q79: What is the `LAG()` and `LEAD()` function?
**A:** `LAG()` accesses data from the previous row within the same result set partition. `LEAD()` accesses data from the next row. They are used for comparing values across consecutive rows, computing differences, or calculating running totals.

## Q80: How do you implement pagination in SQLite?
**A:** Using `LIMIT` and `OFFSET`: `SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 20;` (returns 10 rows starting from row 21). For large datasets, keyset pagination (cursor-based) using `WHERE id > ? ORDER BY id LIMIT 10` is more efficient.

## Q81: What is the difference between `LIMIT` and `TOP`?
**A:** SQLite uses `LIMIT` with optional `OFFSET` (standard SQL). `TOP` is SQL Server syntax. There is no `TOP` in SQLite. The equivalent is `LIMIT n`.

## Q82: What is the `PRINTF()` function in SQLite?
**A:** `PRINTF()` formats strings using printf-style format specifiers. For example: `SELECT PRINTF('Hello, %s!', name) FROM users;`. It is useful for constructing formatted output within queries.

## Q83: What are virtual generated columns in SQLite?
**A:** Virtual generated columns (since 3.31.0) are computed from expressions involving other columns but do not occupy storage. They are recalculated on every read. They can be indexed for faster queries on derived values.

## Q84: What are stored generated columns in SQLite?
**A:** Stored generated columns (since 3.31.0) are computed from expressions and physically stored in the database. They take up disk space but avoid recomputation on every read. They cannot be written to directly.

## Q85: What is the `UPSERT` syntax in SQLite?
**A:** `UPSERT` (INSERT ... ON CONFLICT DO UPDATE) inserts a row, and if a conflict occurs, it updates the conflicting row instead. Syntax: `INSERT INTO t(id, val) VALUES (1, 'x') ON CONFLICT(id) DO UPDATE SET val=excluded.val;`

## Q86: What is the difference between `UPDATE ... FROM` and correlated subqueries?
**A:** `UPDATE ... FROM` (since 3.33.0) allows joining other tables in an UPDATE statement for more readable multi-table updates. Correlated subqueries achieve the same but can be harder to read and optimize.

## Q87: How does SQLite handle Unicode and internationalization?
**A:** SQLite's `LIKE`, `UPPER`, and `LOWER` functions only handle ASCII characters by default (7-bit). For Unicode case-insensitive comparisons, you must use a custom collation (`CREATE COLLATION`) or ICU extension. The ICU extension provides full Unicode support.

## Q88: What is the ICU extension in SQLite?
**A:** The ICU (International Components for Unicode) extension provides Unicode-aware string comparison, case folding, and collation for SQLite. It enables proper handling of international text with `LIKE`, `ORDER BY`, and comparison operators.

## Q89: What are SQLite limits on string and BLOB length?
**A:** The maximum length of a string or BLOB is determined by the SQLITE_MAX_LENGTH compile-time option (default 1 billion bytes, 10^9). Individual TEXT and BLOB values cannot exceed this limit, and the total row size cannot exceed about 1 billion bytes.

## Q90: What is the `SQLITE_MAX_VARIABLE_NUMBER`?
**A:** This is a compile-time limit on the number of parameters in a prepared statement (default 999 for SQLite 3.32+). If you need more parameters, you can batch your INSERTs or use the `json_each()` approach to pass arrays.

## Q91: What is the `sqlite3_exec()` function?
**A:** `sqlite3_exec()` is a convenience function that compiles and executes zero or more SQL statements. It is simple to use but less flexible than the prepare/step/finalize API. It returns a callback for each result row.

## Q92: What is the prepared statement API in SQLite?
**A:** The prepared statement API (`sqlite3_prepare_v2()`, `sqlite3_bind_*()`, `sqlite3_step()`, `sqlite3_finalize()`) provides the most efficient way to execute SQL. Prepared statements are compiled once and can be executed multiple times with different bindings.

## Q93: What is SQL injection, and how does SQLite help prevent it?
**A:** SQL injection occurs when user input is concatenated into SQL statements. SQLite's prepared statement API with parameter binding (using `?` or `?NNN` or `:AAA` placeholders) automatically escapes input values, preventing injection. Always use parameterized queries.

## Q94: What is `sqlite3_changes()` and `sqlite3_total_changes()`?
**A:** `sqlite3_changes()` returns the number of rows changed by the most recent INSERT, UPDATE, or DELETE statement. `sqlite3_total_changes()` returns the cumulative count of changes since the database connection was opened.

## Q95: What is the `last_insert_rowid()` function?
**A:** `last_insert_rowid()` returns the ROWID of the last successful INSERT on the current database connection. It is useful for retrieving auto-generated IDs after inserting a new row. It is connection-specific.

## Q96: How do you check the SQLite version?
**A:** Use `SELECT sqlite_version();` or run `sqlite3 --version` in the command line. The version follows semantic versioning (major.minor.patch). Compile-time options can be checked with `PRAGMA compile_options;`.

## Q97: What are the differences between SQLite and other embedded databases?
**A:** Compared to DuckDB (analytical, columnar), SQLite is transactional (OLTP). Compared to LevelDB/RocksDB (LSM-tree, key-value), SQLite is a full SQL relational database. Compared to H2 (Java-based), SQLite is C-based with zero dependencies.

## Q98: What is `PRAGMA integrity_check`?
**A:** `PRAGMA integrity_check` performs a thorough check of the database for structural corruption. It verifies b-tree page integrity, cell ordering, and pointer consistency. If it returns "ok", the database is internally consistent.

## Q99: What is `PRAGMA quick_check`?
**A:** `PRAGMA quick_check` is a faster but less thorough version of `integrity_check`. It checks page structure and some links but skips certain detailed validations. It is suitable for routine health checks where performance matters.

## Q100: How does SQLite handle power failure or system crash?
**A:** SQLite uses a rollback journal (or WAL file) for atomic commits and crash recovery. If a crash occurs during a transaction, the journal is used to roll back uncommitted changes (in rollback mode) or to replay committed changes (in WAL mode). The `synchronous=OFF` setting increases performance but risks corruption in such scenarios.
