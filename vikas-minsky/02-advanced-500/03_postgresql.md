## 22. PostgreSQL Advanced (581–620)

581. Explain PostgreSQL query planner internals.

   **Answer:** The planner uses cost-based optimization, evaluating sequential scans, index scans, bitmap scans, and join strategies via `EXPLAIN`. It considers table statistics (row count, distribution) and `pg_class`/`pg_statistic` to estimate cheapest paths.

582. How does autovacuum work?

   **Answer:** Autovacuum reclaims storage from dead tuples by running `VACUUM` automatically based on thresholds (`autovacuum_vacuum_scale_factor`, `autovacuum_vacuum_threshold`). It prevents transaction ID wraparound and index bloat.

583. Explain heap storage.

   **Answer:** The heap is the main data structure for table rows, organized into pages (8KB each). Rows are stored as tuples with header metadata, and updates create dead tuples until vacuum reclaims space.

584. What are WAL logs?

   **Answer:** Write-Ahead Logs (WAL) record every change before applying it to data files. They enable crash recovery, point-in-time restoration, and streaming replication by replaying committed transactions.

585. Explain checkpointing.

   **Answer:** Checkpoints flush dirty buffers from shared_buffers to disk, advancing the WAL's redo point. They reduce crash recovery time by ensuring data is synced at regular intervals (`checkpoint_timeout`/`max_wal_size`).

586. How do partial indexes work?

   **Answer:** Partial indexes index only rows matching a `WHERE` clause. They reduce index size and write overhead, ideal for querying a subset of data (e.g., `WHERE status = 'active'`).

587. Explain covering indexes.

   **Answer:** Covering indexes include extra columns via the `INCLUDE` clause that are stored in the index but not used for indexing. They enable index-only scans by satisfying queries entirely from the index.

588. What are BRIN indexes?

   **Answer:** Block Range Indexes (BRIN) summarize data ranges per contiguous block group. They are efficient for large, naturally ordered tables (e.g., time-series data) with much smaller storage than B-tree indexes.

589. Explain GIN indexes.

   **Answer:** Generalized Inverted Indexes (GIN) index composite values like arrays, JSONB, and full-text search tokens. They map each component to all rows containing it, enabling fast `@>` and `@@` operators.

590. How do GiST indexes work?

   **Answer:** Generalized Search Trees (GiST) support custom data types like geometric shapes, ranges, and full-text search. They use balanced tree structures with user-defined consistency functions for complex queries.

591. Explain bitmap scans.

   **Answer:** Bitmap scans combine multiple index scans by building bitmaps of matching page locations. They merge these bitmaps via AND/OR operations before fetching rows, reducing random I/O compared to fetching each row individually.

592. What are sequential scans?

   **Answer:** Sequential scans read every page in a table sequentially. The planner chooses them when the table is small, a high percentage of rows is returned, or no suitable index exists.

593. Explain index-only scans.

   **Answer:** Index-only scans return data directly from the index without accessing the heap, using visibility maps to skip dead tuples. They are the fastest scan type when all needed columns are in the index.

594. How do correlated subqueries impact performance?

   **Answer:** Correlated subqueries execute once per outer row, causing N+1 performance problems. Rewriting as JOINs, lateral joins, or window functions typically eliminates repeated execution.

595. Explain lateral joins.

   **Answer:** `LATERAL` joins allow subqueries in the FROM clause to reference columns from preceding tables. They enable row-by-row computation, useful for top-N-per-group queries and complex data transformations.

596. What are recursive CTEs?

   **Answer:** Recursive CTEs use `WITH RECURSIVE` to iterate through hierarchical data (trees, graphs). They have an anchor member (non-recursive) and a recursive member that references the CTE itself, terminating when no more rows are produced.

597. Explain JSON path queries.

   **Answer:** JSON path queries use the `jsonpath` type and `@@`/`@?` operators to extract or test JSON data with expressions like `$.store.book[0].title`. They offer more powerful querying than simple `->>/#>>`

598. How does row-level security work?

   **Answer:** RLS restricts table access per row using policies defined with `CREATE POLICY`. Policies execute SQL expressions checked on every query, enforcing tenant isolation without application-level filtering.

599. Explain PostgreSQL extensions.

   **Answer:** Extensions (e.g., `pg_stat_statements`, `postgis`, `uuid-ossp`) package SQL objects and libraries. `CREATE EXTENSION` installs them, adding functions, data types, operators, and index methods to the database.

600. What is TimescaleDB?

   **Answer:** TimescaleDB is a PostgreSQL extension for time-series data. It uses hypertables (auto-partitioned by time) with continuous aggregates, compression policies, and retention policies for efficient time-series management.

601. Explain partition pruning.

   **Answer:** Partition pruning eliminates irrelevant partitions at query planning time based on the `WHERE` clause. Queries against range or list partitioned tables only scan matching partitions, reducing I/O significantly.

602. How do hot updates work?

   **Answer:** Hot updates occur when a row update fits on the same page. PostgreSQL stores a pointer (`ctid`) from old tuple to new tuple, allowing concurrent readers to follow the chain for MVCC.

603. Explain fillfactor.

   **Answer:** Fillfactor (default 100) reserves space on each page for future updates. A lower value (e.g., 70) leaves room for HOT updates, reducing index bloat on tables with frequent updates.

604. What are TOAST tables?

   **Answer:** The Oversized-Attribute Storage Technique (TOAST) moves large column values (e.g., text, JSONB > 2KB) into separate TOAST tables, keeping row size small and improving scan performance.

605. Explain replication lag.

   **Answer:** Replication lag measures the delay between primary writes and replica application. It's caused by network latency, slow replica I/O, or long-running transactions and can lead to stale reads if not monitored.

606. How do failovers work?

   **Answer:** Failovers promote a standby to primary when the primary fails. Streaming replication sends WAL to standbys continuously; on failure, a pg_ctl promote (or Patroni/HA tool) makes the standby writable.

607. Explain point-in-time recovery.

   **Answer:** PITR restores a database to a specific moment using base backups + WAL archives. You set recovery target time/XID, and PostgreSQL replays WAL up to that point before stopping.

608. What are foreign data wrappers?

   **Answer:** Foreign Data Wrappers (FDW) let PostgreSQL query external data sources (other databases, files, APIs) as local tables using `CREATE FOREIGN TABLE` and the `postgres_fdw` or `mysql_fdw` extensions.

609. Explain database connection storms.

   **Answer:** Connection storms occur when many clients connect simultaneously, overwhelming `max_connections`. Symptoms include high memory usage and query queuing. PgBouncer's transaction pooling mitigates this by reusing connections.

610. How does PgBouncer work?

   **Answer:** PgBouncer is a lightweight connection pooler that maintains a pool of backend connections. Client connections are multiplexed via session, transaction, or statement pooling modes, reducing the number of active PostgreSQL connections.

611. Explain prepared statements.

   **Answer:** Prepared statements parse, plan, and cache SQL query execution plans. Repeated executions skip parsing overhead. PostgreSQL's `PREPARE`/`EXECUTE` persist cached plans for a session.

612. What are advisory locks?

   **Answer:** Advisory locks are application-defined locks using `pg_advisory_lock()`/`pg_try_advisory_lock()`. They don't lock tables or rows, enabling custom coordination without database schema impact.

613. Explain query parameter sniffing.

   **Answer:** Parameter sniffing happens when cached plans optimized for initial parameter values perform poorly with different values. Using generic plans or `plan_cache_mode` adjusts PostgreSQL's behavior.

614. What are generated columns?

   **Answer:** Generated columns compute values from other columns using `GENERATED ALWAYS AS (expression) STORED`. They don't allow direct writes, ensuring consistency for computed fields like full names or JSON extracts.

615. Explain database auditing.

   **Answer:** Auditing tracks data changes using triggers (audit tables), PostgreSQL's `pgaudit` extension for session/object logging, or WAL-level logical decoding for full change data capture.

616. How do you migrate large databases safely?

   **Answer:** Safely migrate large databases using logical replication (pglogical) to keep standby in sync, running schemas changes incrementally, performing cutovers in maintenance windows, and testing rollback scripts.

617. Explain online schema changes.

   **Answer:** Online schema changes avoid locking by adding columns as nullable, creating indexes concurrently (`CONCURRENTLY`), using `pt-online-schema-change` or `pgroll` to migrate without downtime.

618. What causes index bloat?

   **Answer:** Index bloat results from dead index entries left by updates/deletes that autovacuum hasn't reclaimed. It wastes storage and degrades performance. Periodic `REINDEX` or `autovacuum` tuning mitigates it.

619. Explain write amplification.

   **Answer:** Write amplification in PostgreSQL occurs when a single logical write causes multiple physical writes (WAL, data file, index, TOAST). It increases I/O and reduces SSD lifespan; mitigation includes tuning `checkpoint_completion_target` and `wal_compression`.

620. How do you scale PostgreSQL to millions of users?

   **Answer:** Scale with read replicas for read offloading, connection pooling (PgBouncer), partitioning large tables, caching frequently accessed data in Redis, sharding via Citus, and optimizing queries with proper indexing.
