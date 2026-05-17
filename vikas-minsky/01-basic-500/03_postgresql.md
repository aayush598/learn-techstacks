## 3. PostgreSQL (81–120)

81. What are PostgreSQL advantages over MySQL?
    P**Answer:** PostgreSQL offers superior support for advanced features like JSONB, full-text search, window functions, CTEs, and custom data types. It has better standards compliance, supports concurrent read/write via MVCC, and handles complex queries and large datasets more efficiently.

82. Explain normalization.
    N**Answer:** Normalization organizes database tables to reduce redundancy and dependency by dividing large tables into smaller, related ones. It follows normal forms (1NF, 2NF, 3NF) — eliminating duplicate columns, ensuring partial and transitive dependency removal, and maintaining data integrity.

83. What are database indexes?
    I**Answer:** Indexes are data structures (usually B-trees) that speed up query execution by allowing rapid row lookup without full table scans. They are created on frequently queried columns but add overhead to write operations and consume disk space.

84. Difference between clustered and non-clustered indexes?
    C**Answer:** Clustered indexes determine the physical order of data on disk — each table can have only one. Non-clustered indexes store a separate structure with pointers to the actual rows, allowing multiple per table for different query patterns.

85. Explain B-tree indexes.
    B**Answer:** B-tree indexes are balanced tree structures that store sorted key-value pairs for efficient search, insert, and delete operations in O(log n) time. They support range queries, sorting, and pattern matching with leading wildcards.

86. What are composite indexes?
    C**Answer:** Composite indexes are indexes on multiple columns, where column order matters. They speed up queries filtering by all columns in the index or a prefix of them, following the leftmost prefix rule for optimal usage.

87. Explain transactions.
    T**Answer:** Transactions group multiple database operations into a single atomic unit. Either all operations commit successfully or all roll back on failure, ensuring data consistency. They are controlled with `BEGIN`, `COMMIT`, and `ROLLBACK` statements.

88. What are ACID properties?
    A**Answer:** ACID stands for Atomicity (all or nothing), Consistency (data remains valid), Isolation (concurrent transactions don't interfere), and Durability (committed data persists). PostgreSQL fully implements ACID compliance.

89. Explain MVCC in PostgreSQL.
    M**Answer:** MVCC (Multi-Version Concurrency Control) allows multiple transactions to see different versions of data simultaneously. Each transaction sees a snapshot of data at its start time, enabling non-blocking reads and writes without locks.

90. What is VACUUM?
    V**Answer:** VACUUM reclaims storage occupied by dead rows created by updates and deletes. It prevents transaction ID wraparound and optimizes table bloat. `VACUUM FULL` rewrites the table completely but locks it during operation.

91. Difference between DELETE, TRUNCATE, and DROP?
    D**Answer:** DELETE removes rows one by one (can be rolled back, fires triggers). TRUNCATE quickly removes all rows (cannot be rolled back in some cases, no triggers). DROP removes the entire table structure and data permanently.

92. Explain joins in SQL.
    J**Answer:** Joins combine rows from two or more tables based on related columns. Types include INNER JOIN (matching rows only), LEFT JOIN (all left table rows), RIGHT JOIN (all right table rows), FULL JOIN (all rows from both), and CROSS JOIN (cartesian product).

93. Difference between INNER JOIN and LEFT JOIN?
    I**Answer:** INNER JOIN returns only rows with matches in both tables. LEFT JOIN returns all rows from the left table and matching rows from the right, filling NULLs where no match exists. LEFT JOIN is used when left-side data must be preserved.

94. What are CTEs?
    C**Answer:** CTEs (Common Table Expressions) are temporary result sets defined with the `WITH` clause, improving query readability and allowing recursive queries. They can reference themselves (recursive CTEs) and be used multiple times in the same query.

95. Explain window functions.
    W**Answer:** Window functions perform calculations across a set of rows related to the current row without collapsing them. They use the `OVER` clause with `PARTITION BY` and `ORDER BY`, enabling running totals, rankings, and moving averages.

96. What are materialized views?
    M**Answer:** Materialized views store query results physically on disk, unlike regular views which execute the query each time. They improve read performance for expensive queries but require manual or scheduled refresh with `REFRESH MATERIALIZED VIEW`.

97. Explain query execution plans.
    Q**Answer:** Query execution plans show how PostgreSQL executes a query — the sequence of operations, join methods, index usage, and cost estimates. They are generated with `EXPLAIN ANALYZE` and help identify performance bottlenecks like sequential scans.

98. How do you optimize slow queries?
    O**Answer:** Optimize by analyzing execution plans with `EXPLAIN ANALYZE`, adding appropriate indexes, rewriting inefficient joins, using `EXPLAIN` to check index usage, partitioning large tables, and tuning PostgreSQL configuration like `work_mem` and `shared_buffers`.

99. What are constraints?
    C**Answer:** Constraints enforce data integrity rules at the database level. Types include `NOT NULL`, `UNIQUE`, `PRIMARY KEY`, `FOREIGN KEY`, `CHECK`, and `EXCLUSION` — preventing invalid data entry and maintaining relational consistency.

100. Explain foreign keys.
     F**Answer:** Foreign keys enforce referential integrity between tables. A column in one table references the primary key of another, ensuring that values exist in the referenced table. They prevent orphaned records and support cascading actions.

101. Difference between UUID and SERIAL IDs?
     S**Answer:** SERIAL generates auto-incrementing integers, which are efficient but predictable and can cause collisions in distributed systems. UUIDs are globally unique strings that enable safe merging across databases but are larger (16 bytes vs 4) and slower to index.

102. What are JSONB columns?
     J**Answer:** JSONB stores JSON data in a binary format that supports indexing via GIN indexes. Unlike plain JSON, JSONB removes whitespace and duplicates, and allows efficient querying of nested fields using operators like `->`, `->>`, and `@>`.

103. Explain full-text search.
     F**Answer:** Full-text search uses `tsvector` and `tsquery` types to tokenize and match natural language text. It supports stemming, ranking with `ts_rank`, language-specific dictionaries, and partial match handling, enabling search engine-like functionality.

104. What are triggers in PostgreSQL?
     T**Answer:** Triggers are functions that automatically execute before or after INSERT, UPDATE, DELETE, or TRUNCATE events on a table. They enforce business rules, audit changes, synchronize tables, or cascade operations at the database level.

105. Explain stored procedures.
     S**Answer:** Stored procedures are precompiled SQL code blocks stored in the database, created with `CREATE PROCEDURE` (PostgreSQL 11+). They can contain transaction control and are called with `CALL`, useful for complex business logic that should run close to the data.

106. What are locks in PostgreSQL?
     L**Answer:** Locks prevent concurrent transactions from interfering with each other. PostgreSQL uses table-level locks (ACCESS SHARE, ROW EXCLUSIVE, etc.) and row-level locks, with automatic lock management and deadlock detection.

107. Explain deadlocks.
     D**Answer:** Deadlocks occur when two transactions each hold locks the other needs, causing infinite waiting. PostgreSQL detects deadlocks using a timeout and resolves them by aborting one transaction, which must be retried by the application.

108. What is connection pooling?
     C**Answer:** Connection pooling reuses a fixed set of database connections across multiple client requests, avoiding the overhead of establishing new connections. Tools like PgBouncer or Pgpool-II manage pool size and distribute connections efficiently.

109. Explain replication.
     R**Answer:** Replication copies data from a primary server to standby servers for high availability, read scaling, or disaster recovery. PostgreSQL supports streaming replication, logical replication, and synchronous/asynchronous modes.

110. Difference between logical and physical replication?
     P**Answer:** Physical replication copies entire data blocks byte-for-byte, requiring identical PostgreSQL versions and architecture. Logical replication streams individual data changes (INSERT/UPDATE/DELETE), allowing selective table replication and cross-version compatibility.

111. What are partitions?
     P**Answer:** Partitioning splits large tables into smaller, manageable pieces based on a key like date or range. Each partition is a separate physical table, improving query performance through partition pruning and simplifying data archiving and deletion.

112. Explain sharding.
     S**Answer:** Sharding distributes data across multiple independent database servers based on a shard key. Unlike partitioning (which is within one instance), sharding scales horizontally across machines but adds application complexity for cross-shard queries and transactions.

113. What are migrations?
     M**Answer:** Migrations are version-controlled scripts that evolve the database schema over time. They handle creating, altering, and dropping tables, indexes, and columns while preserving existing data, and are managed by tools like Prisma, Drizzle, or node-pg-migrate.

114. Explain transactions isolation levels.
     I**Answer:** Isolation levels control how transactions see each other's changes. PostgreSQL supports Read Committed (default, sees committed data), Repeatable Read (snapshot at start), and Serializable (prevents all anomalies). Phantom reads are prevented at Repeatable Read level.

115. Difference between optimistic and pessimistic locking?
     O**Answer:** Optimistic locking assumes conflicts are rare — it checks at update time using version numbers and retries on failure. Pessimistic locking uses `SELECT ... FOR UPDATE` to lock rows immediately, preventing concurrent writes but reducing throughput.

116. Explain rollback mechanisms.
     R**Answer:** Rollback undoes changes made during an uncommitted transaction using the `ROLLBACK` command. PostgreSQL maintains undo data in WAL (Write-Ahead Log) and rollback restores the database to the state before `BEGIN` was issued.

117. What are sequences?
     S**Answer:** Sequences are database objects that generate unique numeric values, typically used for auto-incrementing primary keys. They are defined with `CREATE SEQUENCE` and accessed via `nextval()` and `currval()` functions.

118. Explain cascading deletes.
     C**Answer:** Cascading deletes automatically delete child rows when a parent row is deleted, defined with `ON DELETE CASCADE` on foreign key constraints. Other options include `SET NULL`, `RESTRICT`, and `NO ACTION` for different behaviors.

119. How do you secure PostgreSQL?
     S**Answer:** Secure by using strong passwords, SSL/TLS encryption, row-level security policies, network-level access restrictions (`pg_hba.conf`), least-privilege roles, regular security updates, and auditing via `pgAudit` extension.

120. How do you monitor PostgreSQL performance?
     M**Answer:** Monitor using `pg_stat_activity` for active queries, `pg_stat_user_tables` for table access patterns, `pg_stat_bgwriter` for write performance, `pg_stat_database` for overall metrics, and tools like pgAdmin, pg_stat_statements for slow queries, and Prometheus with exporters.
