# MySQL Interview Questions and Answers

## Q1: What is MySQL?
**A:** MySQL is an open-source relational database management system (RDBMS) that uses Structured Query Language (SQL). It is developed by Oracle Corporation and is known for its speed, reliability, and ease of use. It's widely used for web applications.

## Q2: What are the key features of MySQL?
**A:** Key features include: ACID compliance (with InnoDB), replication (asynchronous, semi-synchronous, group replication), partitioning, full-text search, stored procedures, triggers, views, multiple storage engines (InnoDB, MyISAM, Memory, CSV), and foreign key support.

## Q3: What is the default storage engine in MySQL?
**A:** InnoDB has been the default storage engine since MySQL 5.5. It provides ACID-compliant transactions, foreign key support, row-level locking, MVCC, and crash recovery capabilities.

## Q4: What is the difference between MyISAM and InnoDB?
**A:** InnoDB supports transactions, foreign keys, row-level locking, and MVCC. MyISAM supports only table-level locking, no transactions or foreign keys, but offers faster full-text searches and compressed indexes. InnoDB is preferred for most use cases.

## Q5: What is a transaction in MySQL?
**A:** A transaction is a sequence of SQL operations treated as a single unit of work. It follows ACID properties (Atomicity, Consistency, Isolation, Durability). Transactions are managed with `START TRANSACTION`, `COMMIT`, and `ROLLBACK`.

## Q6: What isolation levels does InnoDB support?
**A:** InnoDB supports: READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ (default), and SERIALIZABLE. REPEATABLE READ prevents dirty reads and non-repeatable reads. SERIALIZABLE prevents phantom reads by locking ranges.

## Q7: What is the difference between `CHAR` and `VARCHAR`?
**A:** `CHAR` is fixed-length (padded with spaces), faster for fixed-length data. `VARCHAR` is variable-length (1-2 byte overhead for length). `CHAR(10)` always uses 10 characters; `VARCHAR(10)` uses actual length plus overhead.

## Q8: What is the difference between `VARCHAR` and `TEXT`?
**A:** `VARCHAR(n)` can be indexed fully (up to the limit), stored inline, and has a maximum length of 65,535 bytes. `TEXT` is stored off-page (if large), has a max of 65,535 bytes, requires prefix indexing, and cannot have a default value.

## Q9: What are the numeric data types in MySQL?
**A:** Integer types: `TINYINT` (1 byte), `SMALLINT` (2), `MEDIUMINT` (3), `INT` (4), `BIGINT` (8). Fixed-point: `DECIMAL(p,s)`. Floating-point: `FLOAT` (4), `DOUBLE` (8). `BIT` for bit values.

## Q10: What are the date/time types in MySQL?
**A:** `DATE` (YYYY-MM-DD), `TIME` (HH:MM:SS), `DATETIME` (YYYY-MM-DD HH:MM:SS, range 1000-01-01 to 9999-12-31), `TIMESTAMP` (Unix epoch-based, range 1970-2038), `YEAR` (YYYY).

## Q11: What is the difference between `DATETIME` and `TIMESTAMP`?
**A:** `DATETIME` stores date and time as-is (no timezone conversion), range 1000-01-01 to 9999-12-31, 8 bytes. `TIMESTAMP` converts values from the current timezone to UTC for storage and back on retrieval, range 1970-01-01 to 2038-01-19, 4 bytes.

## Q12: What is an index in MySQL?
**A:** An index is a data structure (B-tree by default) that improves the speed of data retrieval operations on a table. It's created on columns used in WHERE, JOIN, and ORDER BY clauses. Types: PRIMARY KEY, UNIQUE, INDEX (regular), FULLTEXT, SPATIAL.

## Q13: What is the difference between clustered and non-clustered indexes?
**A:** In InnoDB, the PRIMARY KEY is a clustered index — data rows are stored in the index order (the table is the index). Secondary indexes (non-clustered) store the primary key value as a pointer to the row. MyISAM separates index and data regardless.

## Q14: What is a composite index?
**A:** A composite index is an index on multiple columns. `CREATE INDEX idx_name ON table (col1, col2)`. It follows the leftmost prefix rule — the order of columns matters. Queries must use the leftmost columns to benefit.

## Q15: What is the leftmost prefix rule?
**A:** For a composite index on columns (A, B, C), the index can be used for queries on A, A+B, A+B+C, but NOT B, C, or B+C individually. The query must reference the leftmost columns of the index.

## Q16: What is `EXPLAIN` in MySQL?
**A:** `EXPLAIN SELECT ...` shows the query execution plan. It reveals how MySQL executes a query — which indexes are used, join types, row estimates, and access methods. Essential for query optimization.

## Q17: What does `type` column in `EXPLAIN` output mean?
**A:** The `type` column indicates join type/access method: `system` (single row), `const` (primary key lookup), `eq_ref` (one row per join), `ref` (non-unique index), `range` (index range scan), `index` (full index scan), `ALL` (full table scan — worst).

## Q18: What is the difference between `WHERE` and `HAVING`?
**A:** `WHERE` filters rows before aggregation (GROUP BY). `HAVING` filters groups after aggregation. `WHERE` cannot use aggregate functions; `HAVING` can. `WHERE` is applied per-row; `HAVING` is applied per-group.

## Q19: What is the difference between `INNER JOIN` and `LEFT JOIN`?
**A:** `INNER JOIN` returns only matching rows from both tables. `LEFT JOIN` returns all rows from the left table and matching rows from the right table (NULLs for non-matching). In MySQL, `LEFT JOIN` is the same as `LEFT OUTER JOIN`.

## Q20: What is a self-join?
**A:** A self-join joins a table with itself using aliases. `SELECT a.name, b.name AS manager FROM employees a JOIN employees b ON a.manager_id = b.id`. Used for hierarchical data (org charts, categories).

## Q21: What is a subquery in MySQL?
**A:** A subquery is a query nested inside another query. It can be used in SELECT, FROM, WHERE, or HAVING clauses. MySQL optimizes certain subqueries, but JOINs often perform better than correlated subqueries.

## Q22: What is a correlated subquery?
**A:** A correlated subquery references columns from the outer query and runs once for each row of the outer query. It's generally slower than a JOIN. Example: `SELECT * FROM employees e WHERE salary > (SELECT AVG(salary) FROM employees WHERE dept_id = e.dept_id)`.

## Q23: What is `GROUP_CONCAT` in MySQL?
**A:** `GROUP_CONCAT(column ORDER BY col SEPARATOR ',')` concatenates values from multiple rows into a single string. `SELECT dept_id, GROUP_CONCAT(name) FROM employees GROUP BY dept_id`. The default maximum length is 1024 bytes.

## Q24: What is `FIND_IN_SET` function?
**A:** `FIND_IN_SET('value', 'comma,separated,list')` returns the position (1-indexed) of a string in a comma-separated list, or 0 if not found. Used for searching in a string containing comma-separated values.

## Q25: What is the difference between `UNION` and `UNION ALL`?
**A:** Both combine results from multiple SELECT queries. `UNION` removes duplicate rows (requires sorting). `UNION ALL` includes all rows (faster, no deduplication). Use `UNION ALL` unless deduplication is needed.

## Q26: What is a stored procedure in MySQL?
**A:** A stored procedure is a set of SQL statements stored on the server. `CREATE PROCEDURE proc_name (IN param INT) BEGIN ... END`. It improves performance (pre-compiled), reduces network traffic, and encapsulates business logic.

## Q27: What is a trigger in MySQL?
**A:** A trigger is a stored program that automatically executes (`FOR EACH ROW`) when an event (INSERT, UPDATE, DELETE) occurs on a table. MySQL supports BEFORE and AFTER triggers. Limitations: one trigger per event per table per timing.

## Q28: What is a view in MySQL?
**A:** A view is a virtual table based on a SELECT query. `CREATE VIEW view_name AS SELECT ...`. Views simplify complex queries, provide security (column-level access), and can be updatable under certain conditions.

## Q29: What is the difference between `DELETE`, `TRUNCATE`, and `DROP`?
**A:** `DELETE` removes rows (can be rolled back, fires triggers, slower, resets auto-increment only for InnoDB). `TRUNCATE` removes all rows (cannot roll back in most cases, no triggers, resets auto-increment, faster). `DROP` removes the entire table structure.

## Q30: What is the `AUTO_INCREMENT` attribute?
**A:** `AUTO_INCREMENT` generates unique sequential integers for a column (usually primary key). Default starts at 1, increments by 1. Last inserted value: `LAST_INSERT_ID()`. InnoDB uses a counter stored in memory.

## Q31: How do you reset `AUTO_INCREMENT`?
**A:** `ALTER TABLE table_name AUTO_INCREMENT = 1;`. This works in InnoDB and MyISAM. For some storage engines, you may need to drop and recreate the table.

## Q32: What is a foreign key constraint in MySQL?
**A:** A foreign key enforces referential integrity. `FOREIGN KEY (col) REFERENCES parent(col) ON DELETE CASCADE`. Supports RESTRICT, CASCADE, SET NULL, NO ACTION. Only available with InnoDB. Requires an index on the foreign key column.

## Q33: What is the `ON DELETE CASCADE` option?
**A:** `ON DELETE CASCADE` automatically deletes child rows when the parent row is deleted. Useful for maintaining referential integrity (e.g., deleting an order automatically deletes its line items).

## Q34: What is `EXPLAIN FORMAT=JSON`?
**A:** `EXPLAIN FORMAT=JSON SELECT ...` provides the execution plan in JSON format with detailed cost estimates, index conditions, and filter information. More detailed than the default tabular output.

## Q35: What are MySQL configuration files?
**A:** The main config file is `my.cnf` (Linux) or `my.ini` (Windows). Located in `/etc/mysql/`, `/etc/my.cnf`, or the MySQL data directory. Sections: `[mysqld]` (server), `[client]` (client tools), `[mysql]` (mysql CLI).

## Q36: What is `innodb_buffer_pool_size`?
**A:** It's the most important InnoDB setting, defining the memory buffer for caching data and indexes. Recommended: 70-80% of available RAM for a dedicated MySQL server. Larger values reduce disk I/O.

## Q37: What is `query_cache_size` and why is it deprecated?
**A:** The query cache cached SELECT results. It was removed in MySQL 8.0 because it caused scalability issues (mutex contention on multi-core systems). Modern MySQL relies on application-level caching and InnoDB buffer pool.

## Q38: What is `max_connections`?
**A:** `max_connections` limits simultaneous client connections (default 151). Each connection consumes memory. High values need sufficient RAM. Use connection pooling to handle many concurrent users efficiently.

## Q39: What is `innodb_flush_log_at_trx_commit`?
**A:** Controls how InnoDB flushes log buffer to disk. 1 (default) — flush on each commit (ACID compliant, slower). 2 — flush once per second (faster, risk of losing 1 second of data on crash). 0 — no flush (fastest, risk of data loss).

## Q40: What is replication in MySQL?
**A:** Replication copies data from a source (master) to one or more replicas (slaves). Types: asynchronous (default), semi-synchronous, and group replication. Used for read scaling, high availability, and disaster recovery.

## Q41: What is the difference between asynchronous and semi-synchronous replication?
**A:** Asynchronous: source doesn't wait for replica acknowledgment (fast, potential data loss). Semi-synchronous: source waits for at least one replica to acknowledge receipt (slower, reduces data loss risk).

## Q42: What is Group Replication in MySQL?
**A:** Group Replication (MySQL 5.7+) implements a multi-primary or single-primary replication group with built-in conflict detection and resolution. Uses Paxos-like consensus for consistency. Foundation for InnoDB Cluster.

## Q43: What is InnoDB Cluster?
**A:** InnoDB Cluster provides a complete high-availability solution using Group Replication, MySQL Router (for automatic routing), and MySQL Shell (for administration). It offers automatic failover and read/write splitting.

## Q44: What is MySQL Router?
**A:** MySQL Router is a lightweight middleware that provides transparent routing between applications and MySQL servers. It automatically routes read/write to the primary and reads to replicas in InnoDB Cluster setups.

## Q45: What is `mysqldump`?
**A:** `mysqldump` is a command-line tool for logical database backups. It produces SQL statements to recreate databases, tables, and data. `mysqldump -u user -p database > backup.sql`. Options: `--single-transaction` (consistent InnoDB backup).

## Q46: What is `mysqlpump`?
**A:** `mysqlpump` is a newer backup tool (MySQL 5.7+) that supports parallel dumping of databases/tables, compression, and better performance than mysqldump. It uses multiple threads for faster backups.

## Q47: What is binary logging in MySQL?
**A:** The binary log (`binlog`) records all changes to the database (data modifications). Used for replication and point-in-time recovery. Enable with `log_bin = ON`. Format: STATEMENT, ROW (default), or MIXED.

## Q48: What is `ROW` vs `STATEMENT` binary log format?
**A:** `ROW` logs actual row changes (deterministic, larger, recommended). `STATEMENT` logs SQL statements (compact, but non-deterministic queries cause issues). `MIXED` uses STATEMENT by default and switches to ROW for unsafe statements.

## Q49: What is Point-in-Time Recovery (PITR) in MySQL?
**A:** PITR restores a database to a specific point in time using a full backup and the binary log. Process: restore the full backup, then apply binlog events up to the target time using `mysqlbinlog`.

## Q50: What is `mysqlbinlog`?
**A:** `mysqlbinlog` reads binary log files in human-readable or machine-readable format. Used for manual binlog inspection, PITR: `mysqlbinlog binlog.000001 | mysql -u user -p`. Supports timestamps, positions, and database filtering.

## Q51: What is partitioning in MySQL?
**A:** Partitioning divides a table into smaller physical segments while querying the same logical table. Types: RANGE, LIST, HASH, KEY, COLUMNS, and subpartitioning. Supported by InnoDB and NDB. Useful for archiving and large table management.

## Q52: What is `EXCHANGE PARTITION`?
**A:** `ALTER TABLE t EXCHANGE PARTITION p WITH TABLE t2` atomically swaps a partition with an empty table. Used for fast data archiving — move old data out of a partitioned table without locking the full table.

## Q53: What is the `information_schema` database?
**A:** `information_schema` is a system database providing metadata about all other databases, tables, columns, indexes, privileges, and processes. Example: `SELECT * FROM information_schema.tables WHERE table_schema = 'mydb'`.

## Q54: What is `performance_schema`?
**A:** `performance_schema` provides detailed runtime performance data — waits, stages, statements, transactions, and memory usage. Lower overhead than `INFORMATION_SCHEMA`. Essential for performance troubleshooting.

## Q55: What is the `sys` schema?
**A:** The `sys` schema (MySQL 5.7+) provides user-friendly views and stored procedures based on `performance_schema`. Simplifies performance monitoring with views like `sys.statements_with_full_table_scans`.

## Q56: What is a full-text index in MySQL?
**A:** A full-text index enables efficient full-text searches on `CHAR`, `VARCHAR`, or `TEXT` columns. Uses inverted indexing. `CREATE FULLTEXT INDEX idx ON table (column)`. Query with `MATCH(column) AGAINST('search text' IN BOOLEAN MODE)`.

## Q57: What are the full-text search modes in MySQL?
**A:** `IN NATURAL LANGUAGE MODE` (default, relevance-based), `IN BOOLEAN MODE` (operators: +, -, *, @), `WITH QUERY EXPANSION` (performs two searches, expanding results). Boolean mode is most flexible.

## Q58: What is the query optimizer in MySQL?
**A:** The optimizer determines the most efficient way to execute SQL queries. It considers indexes, statistics, join orders, and access methods. Access `optimizer_trace` for detailed optimization decisions.

## Q59: What is `optimizer_trace`?
**A:** `optimizer_trace` (set via `SET optimizer_trace='enabled=on'`) outputs the optimizer's decision-making process in JSON. Shows why the optimizer chose a particular plan — useful for understanding unexpected query behavior.

## Q60: What is `FORCE INDEX` and `USE INDEX`?
**A:** Index hints override the optimizer's index choice. `SELECT * FROM table FORCE INDEX (idx_name) WHERE ...` — forces MySQL to use the specified index. `USE INDEX` suggests but doesn't force. Use sparingly.

## Q61: What are the different types of table locks in MySQL?
**A:** InnoDB uses row-level locks (shared/exclusive). MyISAM uses table-level locks (READ/WRITE). InnoDB also supports intention locks (IS, IX), gap locks, next-key locks, and metadata locks.

## Q62: What is a deadlock in MySQL?
**A:** A deadlock occurs when two or more transactions hold locks that each other needs. InnoDB detects deadlocks (`SHOW ENGINE INNODB STATUS`) and rolls back one transaction. To reduce deadlocks: keep transactions short, access tables in consistent order.

## Q63: What is MVCC in InnoDB?
**A:** Multi-Version Concurrency Control (MVCC) maintains multiple versions of rows. Readers see a consistent snapshot without blocking writers. Implemented via undo logs in the rollback segment. Transaction isolation levels determine snapshot timing.

## Q64: What is a gap lock in InnoDB?
**A:** A gap lock locks a gap between index records to prevent phantom rows. InnoDB uses next-key locking (row lock + gap lock) at REPEATABLE READ level. Gap locks can cause deadlocks and contention; converting to READ COMMITTED disables them.

## Q65: What is `SHOW ENGINE INNODB STATUS`?
**A:** Displays extensive InnoDB status information: current transactions, locks, deadlock info (if any), buffer pool usage, I/O, and log. Essential for diagnosing lock contention and deadlocks.

## Q66: What is `SHOW PROCESSLIST`?
**A:** Shows active threads/connections — each row has Id, User, Host, db, Command, Time, State, and Info (current query). Use `KILL CONNECTION id` to terminate queries.

## Q67: What is the slow query log?
**A:** Logs queries that exceed `long_query_time` (default 10 seconds). Enable with `slow_query_log = 1` and `slow_query_log_file = /path/to/log`. Analyze with `mysqldumpslow` or `pt-query-digest`.

## Q68: What is `pt-query-digest`?
**A:** A tool from Percona Toolkit that analyzes MySQL query logs (slow query, general log, binary log) and produces a ranked report of the slowest and most frequent queries. Essential for query performance analysis.

## Q69: What is `pt-online-schema-change`?
**A:** Percona Toolkit's tool for altering large tables without locking them. It creates a shadow table, applies the schema change, and uses triggers to synchronize data incrementally, then swaps tables atomically.

## Q70: What is `gh-ost`?
**A:** GitHub's Online Schema Migration tool for MySQL. Like pt-online-schema-change but uses binary log streaming instead of triggers, reducing load and risks. Supports pause, resume, and testing in production scenarios.

## Q71: What is `mysqlslap`?
**A:** `mysqlslap` is a load emulation client that simulates concurrent query load. It's built-in and useful for benchmark testing. `mysqlslap --concurrency=50 --iterations=10 --query="SELECT * FROM table"`.

## Q72: What is `sysbench`?
**A:** `sysbench` is a popular benchmarking tool for MySQL. It tests CPU, memory, file I/O, and database performance. `sysbench oltp_read_write --tables=10 --table-size=1000000 run`.

## Q73: What is the difference between `utf8` and `utf8mb4` in MySQL?
**A:** `utf8` in MySQL is a 3-byte UTF-8 encoding that cannot store emoji or some CJK characters (supports BMP only, up to U+FFFF). `utf8mb4` is full 4-byte UTF-8 that supports all Unicode characters including emoji. Use `utf8mb4` in modern applications.

## Q74: What is charset and collation in MySQL?
**A:** Character set defines which characters can be stored (e.g., `utf8mb4`). Collation defines comparison rules (e.g., `utf8mb4_unicode_ci` is case-insensitive, `utf8mb4_bin` is binary/case-sensitive). Set at database, table, or column level.

## Q75: What is `utf8mb4_0900_ai_ci`?
**A:** The default collation in MySQL 8.0. `utf8mb4` (4-byte UTF-8), `0900` (Unicode 9.0 algorithm), `ai` (accent-insensitive), `ci` (case-insensitive). Updated sorting rules based on UCA 9.0.0.

## Q76: What are generated columns?
**A:** Generated columns compute values from other columns. `VIRTUAL` (computed on read, no storage) and `STORED` (computed on write, stored). `ALTER TABLE t ADD COLUMN full_name VARCHAR(200) GENERATED ALWAYS AS (CONCAT(first_name, ' ', last_name)) STORED`.

## Q77: What is the `JSON` data type in MySQL?
**A:** MySQL 5.7+ supports a native JSON data type that stores JSON documents in an optimized binary format. It provides automatic validation and functions like `JSON_EXTRACT()`, `JSON_SET()`, `JSON_CONTAINS()`, and `JSON_ARRAYAGG()`.

## Q78: What are common JSON functions in MySQL?
**A:** `JSON_EXTRACT(doc, '$.key')` (or `->` operator), `JSON_UNQUOTE(expr)` (or `->>` operator), `JSON_SET(doc, path, val)`, `JSON_REPLACE()`, `JSON_REMOVE()`, `JSON_CONTAINS(doc, val)`, `JSON_ARRAYAGG()`, `JSON_OBJECTAGG()`.

## Q79: What is a common table expression (CTE) in MySQL?
**A:** CTEs (MySQL 8.0+) are temporary result sets defined with `WITH`. `WITH cte AS (SELECT ...) SELECT * FROM cte`. Recursive CTEs use `WITH RECURSIVE` for hierarchical data traversal.

## Q80: What are window functions in MySQL?
**A:** Window functions (MySQL 8.0+) perform calculations across rows related to the current row. Functions: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LEAD()`, `LAG()`, `NTILE()`, `FIRST_VALUE()`, `SUM() OVER (PARTITION BY ...)`.

## Q81: What is the difference between `RANK()` and `DENSE_RANK()`?
**A:** `RANK()` leaves gaps after ties (1, 1, 3, 4). `DENSE_RANK()` does not leave gaps (1, 1, 2, 3). Both assign the same rank to equal values within a partition.

## Q82: What is `EXPLAIN ANALYZE` in MySQL 8.0?
**A:** `EXPLAIN ANALYZE` (MySQL 8.0.18+) executes the query and provides detailed timing and row count information for each plan step. It shows actual execution time and iterations, not just estimates.

## Q83: What is the `OPTIMIZE TABLE` command?
**A:** `OPTIMIZE TABLE table_name` reorganizes the table storage, reclaims unused space, and defragments the data file. For InnoDB, it runs as `ALTER TABLE ... ENGINE=INNODB` with online DDL.

## Q84: What is `ANALYZE TABLE`?
**A:** `ANALYZE TABLE table_name` updates table statistics (index cardinality, row counts). The query optimizer uses these statistics for execution plan decisions. Run after significant data changes to keep statistics fresh.

## Q85: What is the `CHECK TABLE` command?
**A:** `CHECK TABLE table_name` checks a table for corruption. Reports errors if the table is damaged. For InnoDB, it checks the clustered index. Run `REPAIR TABLE` to fix certain types of corruption (MyISAM specific).

## Q86: What is the difference between `MyISAM` and `InnoDB` full-text search performance?
**A:** MyISAM has traditionally faster full-text searches with built-in FULLTEXT indexes. InnoDB introduced FULLTEXT indexes in MySQL 5.6. For large text search workloads, consider dedicated search engines (Elasticsearch), though InnoDB full-text is sufficient for many use cases.

## Q87: What is `innodb_file_per_table`?
**A:** When enabled (default in MySQL 5.6+), each InnoDB table stores data and indexes in its own `.ibd` file. This makes space reclamation easier (OPTIMIZE TABLE or ALTER TABLE rebuilds the file) and simplifies backups.

## Q88: What is the `Doublewrite Buffer` in InnoDB?
**A:** The doublewrite buffer is a storage area where InnoDB writes pages before writing them to the data files. It prevents data corruption from partial page writes during crashes. Adds I/O overhead but ensures data integrity.

## Q89: What is the `Change Buffer` in InnoDB?
**A:** The change buffer caches changes to secondary index pages when they are not in the buffer pool. Merged later when pages are read. Optimizes for non-unique secondary index operations (INSERT, UPDATE, DELETE).

## Q90: What is `innodb_autoinc_lock_mode`?
**A:** Controls auto-increment locking. 0 (traditional — table-level lock for all INSERTs). 1 (consecutive — default, bulk inserts still lock). 2 (interleaved — no locks, fastest, but may produce gaps with statement-based replication).

## Q91: What is `read_only` mode in MySQL?
**A:** When `read_only = 1`, only users with SUPER privilege can write. Replicas are typically set to read-only. `super_read_only = 1` also prevents SUPER users from writing (except replication threads).

## Q92: What is `sql_mode` in MySQL?
**A:** `sql_mode` configures SQL syntax and validation behavior. Modes include: `ONLY_FULL_GROUP_BY`, `STRICT_TRANS_TABLES`, `NO_ZERO_IN_DATE`, `NO_ENGINE_SUBSTITUTION`, `ANSI_QUOTES`. Default in MySQL 8.0 is `ONLY_FULL_GROUP_BY, STRICT_TRANS_TABLES, NO_ZERO_IN_DATE, NO_ENGINE_SUBSTITUTION`.

## Q93: What is the difference between `NOW()` and `SYSDATE()`?
**A:** `NOW()` returns the time when the statement began execution (constant within a statement). `SYSDATE()` returns the current time at the moment of function execution (different values within the same statement).

## Q94: What are spatial data types in MySQL?
**A:** MySQL supports spatial/geometric data types: `GEOMETRY`, `POINT`, `LINESTRING`, `POLYGON`, `MULTIPOINT`, `MULTILINESTRING`, `MULTIPOLYGON`, `GEOMETRYCOLLECTION`. Uses with SPATIAL indexes (R-tree) for geographic queries.

## Q95: What is `ST_Distance_Sphere()` function?
**A:** Returns the minimum spherical distance (in meters) between two point geometries. `ST_Distance_Sphere(POINT(lon1, lat1), POINT(lon2, lat2))`. Useful for geolocation queries on a sphere (Earth).

## Q96: How do you handle time zones in MySQL?
**A:** Set the global timezone: `SET GLOBAL time_zone = '+00:00'`. Per-connection: `SET time_zone = 'America/New_York'`. Load timezone tables from the MySQL distribution for named timezones.

## Q97: What is connection pooling and why is it important?
**A:** Connection pooling reuses database connections to avoid the overhead of establishing new connections. Application-side pools (HikariCP, PHP PDO) or proxy-based (ProxySQL, MySQL Router) reduce latency and control connection count.

## Q98: What is ProxySQL?
**A:** ProxySQL is a high-performance MySQL proxy. Features: query routing (read/write splitting), connection pooling, query caching, query rewriting, firewall, and real-time configuration changes without restart.

## Q99: What is MySQL Shell?
**A:** MySQL Shell (mysqlsh) is a modern command-line client and administration tool. Supports JavaScript, Python, and SQL modes. Used for InnoDB Cluster administration, X DevAPI, document store operations, and migrations.

## Q100: How do you migrate from MySQL to another database or vice versa?
**A:** Tools: `mysqldump` for SQL exports (compatible with PostgreSQL with modifications), MySQL Workbench migration wizard, `pgloader` for MySQL-to-PostgreSQL, or ETL tools like Apache NiFi, AWS DMS, or Debezium for streaming migrations.
