# SQLite Interview Questions and Answers - Part 2

## Q1: How does SQLite's OS-level file locking work across NFS, and what failure modes should you expect?
**A:** SQLite relies on POSIX advisory locks (fcntl()) for concurrency control. NFS (versions 2, 3, and 4) has inconsistent support for POSIX locking. NFSv2/v3's lockd may release locks on client crash without proper recovery, leading to database corruption. NFSv4 has better lease-based locking but still suffers from: (1) stale lock recovery delays, (2) byte-range lock conflicts with other processes, (3) network partitions causing lock loss. Always avoid storing SQLite databases on NFS unless using WAL mode and a single connection. For multi-client access, use a client-server database.

## Q2: What is the off_t size limit on 32-bit systems, and how does it constrain SQLite database size?
**A:** On 32-bit systems, off_t is typically 32 bits, limiting file size to 2GB (2^31 - 1). SQLite's -DSQLITE_ENABLE_64BIT_STAT enables 64-bit off_t if the OS supports open64()/lseek64(). Without this, attempting to create a database >2GB fails with SQLITE_IOERR. To support large databases on 32-bit: (1) Compile SQLite with -D_FILE_OFFSET_BITS=64, (2) Ensure the filesystem supports large files, (3) Use 64-bit system for databases expected to exceed 2GB. On 64-bit systems, the maximum is about 140TB.

## Q3: How does SQLite handle rollback in WAL mode when a checkpoint is interrupted by a crash?
**A:** In WAL mode, if a crash occurs during a checkpoint (which moves frames from the WAL to the main database), the checkpoint is atomic at the page level. On recovery: (1) SQLite reads the WAL file header to find the last valid commit, (2) Frames after the last valid commit are discarded, (3) Partially written checkpoint frames are identified by their checksum and ignored, (4) The database file is consistent as of the last completed checkpoint. The WAL index in shared memory is rebuilt from the WAL file.

## Q4: What is the difference between SQLITE_FCNTL_CHUNK_SIZE and PRAGMA mmap_size in controlling file I/O behavior?
**A:** SQLITE_FCNTL_CHUNK_SIZE (set via sqlite3_file_control()) hints to the OS to allocate file space in chunks of the specified size, reducing fragmentation for append-heavy workloads. mmap_size controls how much of the database file is memory-mapped. When mmap is active, SQLite reads pages via memory access instead of read() system calls. Chunk size affects write allocation strategy (helps with sequential growth). Mmap affects read path (helps with random reads).

## Q5: How do subquery flattening, co-routine, and automatic indexing optimizations work in the SQLite query planner?
**A:** SQLite's optimizer applies: (1) Subquery flattening: converts subqueries in FROM or IN into joins or semi-joins, eliminating subquery overhead, (2) Co-routine: for subqueries used multiple times in a query, SQLite may materialize them once and reuse, (3) Automatic indexing: for queries with no usable index, SQLite creates a transient, automatic index on the ephemeral table to speed up joins or subqueries. Automatic indexes are created per-connection and discarded after the query.

## Q6: What is SQLITE_DBCONFIG_ENABLE_TRIGGER and how does it help with bulk data loading?
**A:** SQLITE_DBCONFIG_ENABLE_TRIGGER allows temporarily disabling triggers for a database connection. During bulk data loading, disabling triggers avoids per-row trigger overhead. Pattern: sqlite3_db_config(db, SQLITE_DBCONFIG_ENABLE_TRIGGER, 0, &old) before bulk inserts, then re-enable. You must manually synchronize any logic the triggers would have performed (e.g., updating summary tables). Similarly, SQLITE_DBCONFIG_ENABLE_FKEY temporarily disables foreign key enforcement during load.

## Q7: How does SQLite's lookaside allocator work, and what are the performance implications of tuning it?
**A:** The lookaside allocator is a per-connection pool of fixed-size memory buffers (default: 1200 bytes each, 100 slots = 120KB total). SQLite uses these for short-lived allocations during query processing (e.g., B-tree cell parsing). Benefits: avoids malloc()/free() overhead for common small allocations, reduces memory fragmentation, improves cache locality. Tuning: SQLITE_CONFIG_LOOKASIDE changes slot size and count. If too small, SQLite falls back to heap allocation. If too large, per-connection memory waste. For embedded systems, setting lookaside to 0 saves memory at the cost of performance.

## Q8: How do you implement a custom SQLite VFS for storing databases in memory or on encrypted storage?
**A:** A custom VFS replaces SQLite's file I/O layer. Steps: (1) Define a sqlite3_io_methods struct implementing xClose, xRead, xWrite, xFileSize, xLock, xUnlock, xSync, xFileControl, etc., (2) Define a sqlite3_vfs struct with xOpen, xDelete, xAccess, xFullPathname, etc., (3) Register with sqlite3_vfs_register(), (4) Use sqlite3_vfs_find() to locate by name. Use cases: in-memory databases backed by malloc'd buffers, transparent encryption, cloud storage backends. The built-in unix-vfs or win32-vfs source files serve as templates.

## Q9: What are the implications of using PRAGMA synchronous=OFF with WAL mode regarding durability?
**A:** With WAL mode + synchronous=OFF, SQLite does not call fsync() when committing WAL frames. In a power loss: committed transactions may not have reached disk and are lost; the WAL header and frames may be partially written, leading to corruption. With synchronous=NORMAL (recommended for WAL mode), SQLite fsyncs at critical checkpoints. Never use synchronous=OFF for data you care about. It is only acceptable for temporary databases or test fixtures.

## Q10: How does the SQLITE_CONFIG_SERIALIZED threading mode work, and what are the real concurrency benefits?
**A:** SQLITE_CONFIG_SERIALIZED places SQLite in thread-safe mode where all public APIs are protected by a single mutex. Multiple threads can safely call SQLite APIs on the same or different connections, but only one thread executes inside SQLite at any time. Performance benefit comes from overlapping I/O wait with computation. For actual concurrent database access, use SQLITE_CONFIG_MULTITHREAD with separate connections per thread and let the OS/database locks handle concurrency.

## Q11: How do you handle SQLite database corruption and what recovery options exist?
**A:** Recovery strategies: (1) PRAGMA integrity_check first to assess damage, (2) Use .dump to export as much data as possible, (3) If .dump fails, use sqlite3_analyzer to locate corruption, (4) PRAGMA quick_check for faster but less thorough check, (5) Restore from backup (.backup file), (6) Use sqlite3 CLI's .recover command (3.33.0+) which reads the database page by page, (7) Commercial recovery tools for severe cases. Prevention: set PRAGMA synchronous=FULL, use WAL mode, schedule regular integrity_check + .backup.

## Q12: How does SQLite's cost-based query optimizer estimate cardinality, and what happens when estimates are wrong?
**A:** SQLite maintains no table statistics by default. It estimates cardinality based on row count from sqlite_stat1 (populated by ANALYZE), default assumptions (100 rows for unknown table), and constant propagation. Without ANALYZE, the optimizer assumes uniform distribution and independence between columns, leading to poor plans for: skewed data distributions, correlated columns, complex join orders. Run ANALYZE after significant data changes. Use sqlite_stat1 through sqlite_stat4 for histogram data.

## Q13: How do you configure SQLite for a read-only database on a read-only filesystem?
**A:** SQLite requires write access for journal files, sqlite_master updates, and lock files. For read-only databases on read-only filesystems: (1) Open with SQLITE_OPEN_READONLY flag, (2) Set PRAGMA query_only = 1, (3) Use PRAGMA temp_store = MEMORY to avoid temp file writes, (4) PRAGMA journal_mode = OFF or MEMORY to avoid journal files, (5) Use sqlite3_db_readonly() to check if the database is read-only. Without these, SQLite returns SQLITE_CANTOPEN or SQLITE_READONLY errors.

## Q14: What are the differences between SQLITE_DBCONFIG_ENABLE_LOAD_EXTENSION and sqlite3_enable_load_extension()?
**A:** sqlite3_enable_load_extension() is a C API that globally enables or disables loading of extensions. SQLITE_DBCONFIG_ENABLE_LOAD_EXTENSION is a per-connection setting that overrides the global setting for a specific handle. For security: disable extension loading globally in production, only load extensions from trusted signed binaries, use sqlite3_db_config() to prevent extension loading on untrusted connections.

## Q15: How does the ICU extension's collation compare with SQLite's built-in BINARY and NOCASE collations?
**A:** SQLite's built-in BINARY collation compares strings byte-by-byte. NOCASE only folds ASCII A-Z to a-z, not handling Unicode case folding (e.g., A vs a). The ICU extension provides: Unicode-aware case folding and accent stripping, locale-specific collation, configurable strength (primary, secondary, tertiary), and Unicode standard LIKE and UPPER/LOWER. Performance: ICU is significantly slower due to Unicode table lookups.

## Q16: How do you set up SQLite as a shared cache across multiple threads or processes?
**A:** SQLite's shared cache mode allows multiple connections (same process) to share a single data and schema cache. Setup: (1) Enable with SQLITE_OPEN_SHAREDCACHE flag, (2) Or set PRAGMA shared_cache = 1, (3) Use sqlite3_enable_shared_cache(1) globally. Benefits: table-level locking replaces database-level locking, multiple readers can coexist, more memory efficient. Limitations: only works within same process, cannot use PRAGMA mmap_size with shared cache, not supported on all platforms.

## Q17: How does SQLite's PRAGMA cache_spill work, and when would you tune it?
**A:** PRAGMA cache_spill controls whether the cache spills dirty pages to disk before the cache is full (default: true). When enabled: SQLite writes dirty pages during large read transactions to keep cache available for hot data, reducing peak memory usage but increasing write amplification. Tuning: PRAGMA cache_spill = 0 disables early spill for write-heavy transactions; set specific size to spill when uncommitted dirty pages exceed a threshold. Use with PRAGMA cache_size tuning.

## Q18: What causes the SQLITE_SCHEMA error, and how do you handle it in long-running applications?
**A:** SQLITE_SCHEMA (error code 17) occurs when the database schema changes (DDL) while a prepared statement is still active. SQLite detects this by incrementing a schema cookie. Handling: the application must re-prepare the statement and retry. Use sqlite3_prepare_v2() (not v1) which auto-reprepares on schema change for most queries. For bulk operations, prepare statements just before use. Avoid DDL during read-heavy periods.

## Q19: How does PRAGMA journal_mode=OFF affect durability, and is it safe for any use case?
**A:** PRAGMA journal_mode=OFF disables the rollback journal entirely. No atomic commit: a crash during a transaction may leave the database in an inconsistent state. Transactions still work in that ROLLBACK is a no-op. Safe use cases: read-only temporary databases, databases fully rebuilt on each startup (cache), embedded devices with read-only filesystem after deployment, test environments where data loss is acceptable. Never use for production data.

## Q20: How do you implement a SQLite virtual table that wraps an external API or data source?
**A:** SQLite virtual tables allow custom backends. Implementation via C: define xConnect/xDisconnect for module load/unload, xBestIndex for query planning, xOpen/xClose for cursor lifecycle, xFilter/xNext/xEof/xColumn/xRowid for row iteration. Example: wrapping a REST API where xBestIndex translates SQL WHERE clauses into API query parameters, xFilter makes the HTTP call, xColumn extracts fields from JSON responses. Popular virtual tables: csv, json, fts5, rtree, dbstat.

## Q21: How does SQLite handle ALTER TABLE ADD COLUMN with DEFAULT values for existing rows?
**A:** When adding a column with DEFAULT value, SQLite does not modify existing rows immediately. The new column is added to the schema, and existing rows return the DEFAULT value when read. This is possible because SQLite stores default values per-table in the schema. When reading a row, if the column is missing from the record, SQLite returns the DEFAULT value. This makes ALTER TABLE ADD COLUMN O(1) with no table rewrite. Writing to an existing row materializes the column.

## Q22: How do you configure SQLite's PRAGMA soft_heap_limit and PRAGMA hard_heap_limit?
**A:** PRAGMA soft_heap_limit (in bytes) sets a soft limit on SQLite's heap allocation. When exceeded, SQLite aggressively releases memory back to the system. It is a hint, not a hard limit. PRAGMA hard_heap_limit (3.45.0+) sets a hard limit. These are useful for embedded systems with fixed memory budgets. Without limits, SQLite grows its cache to cache_size * page_size regardless of system memory pressure.

## Q23: What is the sqlite3_stmt_scanstatus() API, and how does it help profile query performance?
**A:** sqlite3_stmt_scanstatus() (enabled with SQLITE_ENABLE_STMT_SCANSTATUS) returns per-table scan statistics for a prepared statement: nLoop (loop iterations), nVisit (rows visited), estimatedRows (optimizer's estimate), zName (table/index name). Compare nVisit vs nLoop: if nVisit >> nLoop, the inner loop is scanning too many rows, indicating a missing index.

## Q24: How does SQLite's VDBE profile output help with query optimization?
**A:** The VDBE profile (PRAGMA vdbe_profile=1) prints per-instruction timing and row counts. The output shows each VDBE opcode with cumulative time and execution count. Analysis: Next or Prev opcodes with high time indicate expensive index scans; Column with high time suggests expensive row reconstruction (covering index needed); OpenRead/OpenWrite with high count means many table/index opens (consider reusing prepared statements).

## Q25: How do you handle SQLite database migrations with zero-downtime in production?
**A:** Zero-downtime SQLite migrations: (1) Only additive changes: add columns with DEFAULT, add indexes with CONCURRENTLY (3.35.0+), add tables, (2) Use CREATE INDEX CONCURRENTLY which builds index without blocking writes, (3) Never use ALTER TABLE RENAME on active databases, (4) For destructive changes: create new table, migrate data incrementally, swap atomically, (5) Use WAL mode so reads continue during migration writes, (6) Run migrations in a separate connection, (7) Version your schema in a _migrations table.

## Q26: How does SQLite's B-tree balancing work during inserts, and when do page splits occur?
**A:** SQLite uses a balanced B-tree with pages (default 4096 bytes). When a page is full and a new entry must be inserted: a page split occurs with half the entries moving to a new page, a separator key is promoted to the parent, cascading up the tree if the parent is also full. Split frequency depends on fill factor (about 90%), insert order (random causes more splits), and page size (larger pages reduce splits but increase I/O per operation).

## Q27: How does PRAGMA secure_delete work at the file system level, and what are its performance implications?
**A:** PRAGMA secure_delete (default: OFF) overwrites deleted content with zeros before releasing pages. When ON: deleted data is zeroed in the database file, preventing recovery through file inspection. It does NOT affect WAL or journal files. Performance: about 20-30% overhead on DELETE/UPDATE, increases write amplification, can cause SSD wear. Use only for data sensitivity compliance (PCI-DSS).

## Q28: What is SQLITE_DBSTATUS_CACHE_USED and SQLITE_DBSTATUS_CACHE_HIT, and how do you use them for cache tuning?
**A:** These per-connection status counters track: CACHE_USED (cache pages in use), CACHE_HIT (cumulative cache hits), CACHE_MISS (cumulative cache misses). The cache hit ratio = CACHE_HIT / (CACHE_HIT + CACHE_MISS). A ratio below 90% suggests PRAGMA cache_size is too small. Track over time after adjustments to find the optimal size.

## Q29: How do you implement row-level security (RLS) in SQLite without native RLS support?
**A:** SQLite has no built-in RLS. Implementations: (1) Views + application context: create views that filter by current_user, then grant SELECT on views, (2) Trigger-based RLS: INSTEAD OF triggers on views enforce row-level restrictions, (3) Authorizer callback: sqlite3_set_authorizer() intercepts every table access and can deny access based on the calling user, (4) Encrypted columns: store sensitive data encrypted and decrypt only for authorized users.

## Q30: How does SQLite handle concurrent writes in WAL mode vs DELETE mode?
**A:** In DELETE mode: only one writer can hold the RESERVED lock at a time; concurrent write attempts get SQLITE_BUSY. In WAL mode: multiple readers can read while a writer appends to the WAL; only one writer at a time; if a writer is active, a second writer gets SQLITE_BUSY or waits for busy_timeout; WAL readers do not block writers; checkpoint may briefly block readers and writers. WAL mode dramatically improves concurrency for read-mostly workloads.

## Q31: How do you use the generate_series table-valued function in SQLite for analytical queries?
**A:** The generate_series virtual table (3.33.0+) generates a sequence of integers. Use cases: date dimension tables (SELECT date(...) FROM generate_series(0, 364)), pivot/data densification (LEFT JOIN generate_series(0, 23) AS hours), test data generation (SELECT random() FROM generate_series(1, 10000)), bucket ranges for histograms. Requires the generate_series extension (-DSQLITE_ENABLE_MATH_FUNCTIONS).

## Q32: How does PRAGMA temp_store = FILE interact with SQLITE_TEMP_STORE compile-time setting?
**A:** SQLITE_TEMP_STORE (0-3) determines compile-time default: 0=file, 1=file(default), 2=memory, 3=memory. PRAGMA temp_store (0-2) overrides per-connection: 0=default, 1=file, 2=memory. If SQLITE_TEMP_STORE=2, temp_store=FILE still uses memory (compile-time wins). temp_store=MEMORY is faster for small temp sets but may cause OOM for large sorts/aggregations. For embedded, use memory; for desktop, use file to avoid OOM.

## Q33: How does SQLite's ORDER BY optimization work with LIMIT when using an index?
**A:** SQLite can avoid sorting for ORDER BY + LIMIT queries when an index provides the required ordering. The planner scans the index in order, fetches rows from the table, and stops after LIMIT rows. If the ORDER BY matches an index prefix but the WHERE clause filters many rows, the planner may still sort. EXPLAIN QUERY PLAN shows whether USING INDEX with ORDER BY appears.

## Q34: How do you implement a SQLite-backed queue for producer-consumer workloads?
**A:** SQLite as a queue: CREATE TABLE queue (id INTEGER PRIMARY KEY AUTOINCREMENT, payload BLOB, status TEXT DEFAULT 'pending'). Enqueue: INSERT INTO queue(payload) VALUES(?). Dequeue: BEGIN IMMEDIATE; SELECT ... ORDER BY id LIMIT 1 FOR UPDATE; UPDATE SET status='processing' WHERE id=?; COMMIT. For non-blocking: UPDATE ... WHERE id = (SELECT id FROM ... LIMIT 1) RETURNING *. Set PRAGMA busy_timeout=5000. Suitable for moderate throughput (<10K items/sec).

## Q35: How does SQLite handle CHECK constraints with NULL values?
**A:** SQLite follows the SQL standard: a CHECK constraint is satisfied if the expression evaluates to TRUE OR NULL. CHECK (age > 0) allows age = NULL. To reject NULL, add AND age IS NOT NULL. CHECK (age IS NOT NULL AND age > 0) properly rejects both NULL and invalid values. For NOT NULL enforcement, prefer column constraint NOT NULL over CHECK.

## Q36: What are SQLITE_STATIC and SQLITE_TRANSIENT in the sqlite3_bind_* API?
**A:** SQLITE_STATIC tells SQLite that the pointer is valid for the duration of the current call. SQLite does not copy the data. Use when the source buffer is guaranteed to exist until sqlite3_step() returns. SQLITE_TRANSIENT tells SQLite to make a copy of the data immediately. Use when the buffer may be freed or reused before the next sqlite3_step(). SQLITE_TRANSIENT is safer and more common for strings and blobs.

## Q37: How do you use SQLITE_ENABLE_MATH_FUNCTIONS for analytical workloads?
**A:** Compiling with -DSQLITE_ENABLE_MATH_FUNCTIONS enables math functions: ACOS, ASIN, ATAN, ATAN2, CEIL, COS, COT, DEGREES, EXP, FLOOR, LN, LOG, LOG10, LOG2, PI, POWER, RADIANS, SIN, SQRT, TAN, TRUNC. Use cases: statistical calculations (AVG, STDDEV), GIS-like distance queries, financial calculations, log-space aggregations for geometric mean.

## Q38: How does PRAGMA journal_mode=WAL interact with PRAGMA synchronous values differently than DELETE mode?
**A:** In DELETE mode: synchronous=FULL ensures journal is fully flushed; synchronous=NORMAL flushes at critical moments. In WAL mode: synchronous=NORMAL (recommended) ensures WAL frames are flushed on checkpoint but not every commit; synchronous=FULL ensures flush on every commit; synchronous=OFF does not flush. NORMAL in WAL mode provides stronger durability than NORMAL in DELETE mode.

## Q39: What is the SQLITE_IOERR_ACCESS error, and how do you diagnose filesystem permission issues?
**A:** SQLITE_IOERR_ACCESS occurs when SQLite cannot access a file due to: filesystem permissions, SELinux or AppArmor restrictions, filesystem full, or file locking conflicts on network filesystems. Diagnosis: check file permissions for all associated files, verify process user can access the directory, check audit.log for SELinux denials, check disk space, use strace for system call traces.

## Q40: How do you implement a custom tokenizer for FTS5?
**A:** FTS5 supports custom tokenizers via C callbacks. Implement xCreate, xDelete, xTokenize functions, then register with sqlite3_fts5_tokenizer(). The xTokenize function receives input text and calls a callback for each token. Use cases: Unicode-aware CJK tokenizer, URL tokenizer, code-aware tokenizer (camelCase splitting), language-specific stemmer integration. Register: CREATE VIRTUAL TABLE t1 USING fts5(content, tokenize='my_tokenizer').

## Q41: How does SQLite handle aggregate functions with FILTER (WHERE ...) syntax?
**A:** SQLite 3.30.0+ supports FILTER (WHERE ...) for aggregate functions: SELECT COUNT(*) FILTER (WHERE status = 'active'), COUNT(*) FROM users. Equivalent to SUM(CASE WHEN ... THEN 1 ELSE 0 END) but more readable. Only one FILTER clause per aggregate. Applies to SUM, AVG, GROUP_CONCAT, and window functions. Internally, SQLite evaluates the filter expression for each row.

## Q42: How does the STRICT table type (SQLite 3.37.0+) differ from traditional SQLite tables?
**A:** STRICT tables enforce strict type checking: columns defined as INT can only hold integers, TEXT only text, BLOB only blobs, REAL only real. No type affinity, type is strictly enforced at insert. INTEGER PRIMARY KEY still works as rowid alias. Storage format is identical. REAL accepts floating point, INT accepts integers. Tables default to non-STRICT for backward compatibility. Use STRICT for new applications.

## Q43: How is SQLITE_LIMIT_LENGTH enforced for TEXT vs BLOB values?
**A:** SQLITE_LIMIT_LENGTH (default: about 1GB) is the maximum length of a string or BLOB. Both TEXT and BLOB count toward this single limit. The limit applies to stored column values, intermediate expressions, GROUP_CONCAT output, and SQL string literals. Exceeding it returns SQLITE_TOOBIG. For TEXT, characters are counted in bytes, not characters, as SQLite uses UTF-8.

## Q44: How does the xFileControl operation in the VFS enable integration with custom I/O features?
**A:** xFileControl is a VFS method using opcodes. Standard opcodes: SQLITE_FCNTL_LOCKSTATE (get lock state), SQLITE_FCNTL_SIZE_HINT (pre-allocation), SQLITE_FCNTL_CHUNK_SIZE (allocation chunk size), SQLITE_FCNTL_FILE_POINTER (underlying fd), SQLITE_FCNTL_PERSIST_WAL, SQLITE_FCNTL_OVERWRITE, SQLITE_FCNTL_VFSNAME. Custom VFS implementations can add opcodes for encryption key rotation, compression changes, backup triggers, etc.

## Q45: How do you use the rtree extension for spatial indexing in SQLite?
**A:** The R-tree extension provides spatial indexing: CREATE VIRTUAL TABLE spatial_index USING rtree(id, minX, maxX, minY, maxY). Query: SELECT * FROM spatial_index WHERE minX <= ? AND maxX >= ? AND minY <= ? AND maxY >= ?. Performance: O(log N) for searches. Limitations: only supports axis-aligned bounding boxes (2D or 3D), no arbitrary polygons, no spatial join optimization.

## Q46: What happens when SQLite encounters a page with a checksum error during a read?
**A:** SQLite 3.32.0+ supports page-level checksums (PRAGMA checksum or -DSQLITE_ENABLE_PAGE_CHECKSUM). Each page includes a CRC32 or SHA3-256 checksum. On checksum mismatch: sqlite3_step() returns SQLITE_CORRUPT. The specific page number is known. The application should restore from backup. Page checksums detect bit rot and silent data corruption earlier than structural checks.

## Q47: How does PRAGMA encoding affect TEXT storage and collation behavior?
**A:** SQLite supports UTF-8 (default), UTF-16le, and UTF-16be at the database level. LENGTH() and SUBSTR() operate on characters, not bytes. LIKE and GLOB are encoding-aware. sqlite3_column_text() converts UTF-16 to UTF-8 automatically. Collation operates on raw bytes of stored encoding. Always use UTF-8 unless interfacing with Windows COM or .NET.

## Q48: How do you handle SQLite database migrations across platforms with different endianness?
**A:** SQLite databases are portable across platforms: the file header encodes the native page size and endianness (1=big-endian, 2=little-endian). SQLite detects endianness on open and converts on the fly. Switching platforms causes byte-swapping on every page read (5-10% overhead). The WAL and SHM files are NOT portable across endianness. Create the database on the target platform for cross-platform deployment.

## Q49: What is the effect of PRAGMA page_size on vacuum behavior and database size after bulk deletes?
**A:** Page size affects VACUUM and space reclamation. VACUUM rewrites the entire database, packing remaining rows into contiguous pages. Larger page sizes (8192, 16384, 65536) may increase wasted space after deletes but mean fewer pages to manage. PRAGMA auto_vacuum = INCREMENTAL or FULL can reclaim space incrementally. auto_vacuum causes file fragmentation. For frequent bulk deletes, use INCREMENTAL with periodic incremental_vacuum calls.

## Q50: How does RETURNING clause work in SQLite 3.35.0+, and what are its performance characteristics?
**A:** RETURNING returns values from modified rows: INSERT INTO t VALUES(1) RETURNING rowid; UPDATE t SET x=1 WHERE y=2 RETURNING old.x, new.x; DELETE FROM t RETURNING *. It returns results as a result set. In INSERT, returns newly inserted data including generated columns and defaults. In UPDATE, both old.* and new.* are accessible. Minimal performance overhead as data is already in memory.

## Q51: How do you configure PRAGMA busy_timeout with a connection pool for multi-threaded applications?
**A:** PRAGMA busy_timeout sets a millisecond timeout for SQLite to wait when a table is locked before returning SQLITE_BUSY. In a connection pool: set busy_timeout to 5000-10000ms to avoid SQLITE_BUSY errors. The timeout uses a busy handler that sleeps and retries. Combine with PRAGMA journal_mode=WAL for best concurrency. If timeout is too high, a long write transaction blocks all other writes for the entire timeout.

## Q52: How does the MATCH operator work with FTS5, and what ranking functions are available?
**A:** MATCH performs full-text search: SELECT * FROM docs WHERE content MATCH 'search phrase'. Ranking functions: rank (default BM25), bm25(docs, weight1, weight2) for custom per-column weights, highlight(docs, col, open, close) for highlighted snippets, snippet() for text excerpts. FTS5 query syntax supports AND, OR, NOT, NEAR, * (prefix), phrase matching, and boost.

## Q53: How does SQLite's UPSERT conflict handling differ for UNIQUE index vs PRIMARY KEY?
**A:** UPSERT identifies the constraint causing the conflict. For PRIMARY KEY, use ON CONFLICT(rowid) or ON CONFLICT(col) where col is the PK. For UNIQUE index, use ON CONFLICT(col) where col is indexed. The conflict target must match exactly one constraint. Use ON CONFLICT DO NOTHING without a target to ignore any constraint violation.

## Q54: How do you tune SQLite for millions of rows per second insert throughput?
**A:** For maximum insert throughput: use BEGIN IMMEDIATE + COMMIT per batch (1000-10000 rows), prepared statements with sqlite3_prepare_v2() + bind + step, set synchronous=OFF, journal_mode=MEMORY or OFF, temp_store=MEMORY, cache_size=-100000, locking_mode=EXCLUSIVE, mmap_size=256MB, drop indexes before bulk insert. With these settings, SQLite can achieve about 1-5M inserts/second on modern hardware.

## Q55: How do you implement materialized views in SQLite using triggers?
**A:** SQLite has no native materialized views. Create a summary table, then create triggers on the base table (INSERT, UPDATE, DELETE) that update the summary. Example: CREATE TRIGGER order_insert AFTER INSERT ON orders BEGIN INSERT INTO order_summary(date, total) VALUES(new.date, new.amount) ON CONFLICT(date) DO UPDATE SET total = total + new.amount; END. Initial population: INSERT INTO order_summary SELECT date, SUM(amount) FROM orders GROUP BY date.

## Q56: What is PRAGMA cell_size_check and how does it affect performance?
**A:** PRAGMA cell_size_check (default: OFF) causes SQLite to verify the internal consistency of B-tree cells when reading pages. When ON, each cell's payload size is validated against page boundaries before use. Performance impact: about 5-10% overhead on read operations. Provides additional defense against database corruption. For critical data systems, enable it. For high-performance systems, leave OFF and rely on periodic integrity_check.

## Q57: How does SQLite handle floating-point rounding errors in aggregate functions like SUM?
**A:** SQLite uses IEEE 754 double-precision for REAL values. SUM() of many floats accumulates rounding errors. For financial calculations: store money as integers (cents), use ROUND(SUM(amount), 2), or store as TEXT with fixed-point arithmetic extensions. AVG() on integers uses integer division. SQLite does not have NUMERIC/DECIMAL types.

## Q58: How do you configure PRAGMA checkpoint_fullfsync and when is it needed?
**A:** PRAGMA checkpoint_fullfsync (default: OFF, macOS: ON) controls whether F_FULLFSYNC is called during WAL checkpoints on macOS. F_FULLFSYNC ensures data is written to physical media, not just drive cache. Without it on macOS, power failure can lose recently written data. Enable on macOS for data-critical applications. Performance impact on macOS is significant (up to 10x slower).

## Q59: How does SQLite's ORDER BY RANDOM() LIMIT 1 optimization work?
**A:** Instead of sorting the entire table, SQLite generates a random rowid in the range [1, max(rowid)] and checks if it exists. For densely populated rowid space, this is O(1). For sparse rowid (many deletes), it may degrade to full sort. Does not apply to WITHOUT ROWID tables. For those, consider adding a random integer column with index.

## Q60: How do you use PRAGMA schema_version and PRAGMA user_version for schema migration tracking?
**A:** user_version (32-bit integer, default 0) persists across connections. Use for migration tracking: on connection open, read PRAGMA user_version, apply migration scripts for versions between stored and current, after each step update PRAGMA user_version = N. schema_version is managed by SQLite for internal DDL tracking; do not modify it directly. Some ORMs use user_version for migration tracking.

## Q61: How does SQLite handle WAL file cleanup after a crash?
**A:** After a crash in WAL mode: SQLite checks for existing -wal and -shm files, reads the WAL header for the last valid commit frame, replays committed frames into the database, truncates the WAL file after replay. If -shm file is corrupt, SQLite rebuilds the wal-index from the WAL file. The -wal file is only removed after a successful checkpoint moves all frames to the database. The -shm file is cleared after checkpoint completion.

## Q62: How does PRAGMA auto_vacuum work, and what are the trade-offs?
**A:** PRAGMA auto_vacuum has three modes: 0 (NONE, default, pages are never reclaimed), 1 (FULL, pages are reclaimed on commit), 2 (INCREMENTAL, pages are marked as free but not reorganized). FULL mode causes file fragmentation and may slow down write-heavy workloads. INCREMENTAL mode requires periodic PRAGMA incremental_vacuum(N) to actually free N pages. For databases that grow and shrink frequently, INCREMENTAL offers a good balance.

## Q63: How does SQLite handle the SQLITE_LIMIT_VARIABLE_NUMBER limit?
**A:** SQLITE_LIMIT_VARIABLE_NUMBER (default: 999 for 3.32.0+) limits the number of parameters in a prepared statement. If you need more, batch your inserts or use the json_each() approach to pass arrays. Example: INSERT INTO t VALUES (SELECT value FROM json_each(?)) where ? is a JSON array. This bypasses the variable number limit.

## Q64: How do you implement a SQLite-based cache with TTL expiration?
**A:** Create a cache table: CREATE TABLE cache (key TEXT PRIMARY KEY, value BLOB, expires_at INTEGER). Query: SELECT value FROM cache WHERE key = ? AND (expires_at IS NULL OR expires_at > strftime('%s', 'now')). Cleanup: DELETE FROM cache WHERE expires_at < strftime('%s', 'now'). Run cleanup periodically via application scheduler or after each read/write. Index on expires_at for cleanup query performance.

## Q65: What is the difference between sqlite3_backup_init() and the .backup command?
**A:** sqlite3_backup_init() is the C API for live database backup, allowing programmatic backup with progress monitoring. The .backup CLI command uses the same API internally. The C API allows: (1) backing up to or from :memory: databases, (2) incremental backup with sqlite3_backup_step() controlling page count per iteration, (3) progress callbacks, (4) concurrent writes during backup (pages are copied page-by-page with conflict resolution).

## Q66: How does SQLite's xFileControl with SQLITE_FCNTL_PERSIST_WAL work?
**A:** SQLITE_FCNTL_PERSIST_WAL controls whether the WAL file persists after checkpoint when no readers are active. Normally, the WAL file is truncated after checkpoint. With PERSIST_WAL enabled, the WAL file is kept (with size 0). This reduces file creation overhead for workloads that frequently checkpoint. The WAL file is then reused rather than recreated, saving the metadata writes needed for file creation.

## Q67: How do you use sqlite3_trace_v2() for query logging?
**A:** sqlite3_trace_v2() sets a callback for tracing SQL statement execution. Callback receives events: SQLITE_TRACE_STMT (prepared/finalized), SQLITE_TRACE_PROFILE (execution time), SQLITE_TRACE_ROW (each row), SQLITE_TRACE_CLOSE (connection close). Use for: slow query logging, query frequency analysis, connection leak detection. Unlike PRAGMA vdbe_trace, this works at the application level without modifying SQLite compilation flags.

## Q68: How does SQLite handle subqueries in the FROM clause (derived tables)?
**A:** SQLite processes FROM subqueries by materializing them into temporary tables (unless flattened). If the subquery is simple (no aggregates, no ORDER BY, no LIMIT), SQLite may flatten it into the outer query for better optimization. Otherwise, it creates an ephemeral table. Performance: flattened subqueries can use indexes on the underlying tables; materialized subqueries cannot. Use explain query plan to check for flattening.

## Q69: What is the difference between PRAGMA journal_mode=WAL and PRAGMA journal_mode=TRUNCATE?
**A:** TRUNCATE mode uses a rollback journal but truncates it to zero on commit (instead of deleting). This is faster than DELETE mode (no file deletion/creation overhead) but slower than WAL for concurrent access. WAL supports concurrent reads during writes; TRUNCATE does not. TRUNCATE is a middle ground between DELETE (slowest) and WAL (best concurrency).

## Q70: How do you use JSON functions with generated columns for indexing JSON fields?
**A:** SQLite 3.38.0+ supports generated columns that can extract JSON values for indexing: CREATE TABLE t (data TEXT, name TEXT GENERATED ALWAYS AS (json_extract(data, '$.name')) VIRTUAL, CREATE INDEX idx_name ON t(name)). This allows fast queries on JSON fields: SELECT * FROM t WHERE name = 'John'. Use VIRTUAL (computed on read) or STORED (computed on write) generated columns.

## Q71: How does SQLite's lookup in B-tree indexes handle NULL values?
**A:** In SQLite, NULLs in an index are treated as distinct and smaller than all non-NULL values. A UNIQUE index allows multiple NULL values (unlike some databases where NULL = NULL is considered duplicate). In ORDER BY, NULLs sort before all other values. Query: col IS NULL uses the index efficiently; col = NULL does not (use IS NULL instead).

## Q72: What are the implications of using WITHOUT ROWID tables on write performance?
**A:** WITHOUT ROWID tables are stored as a B-tree keyed on the PRIMARY KEY directly. They eliminate the rowid column, saving space. Write performance: (1) Slightly slower for sequential inserts because the PK B-tree is clustered and may require more page splits, (2) Faster for lookups by PK (one fewer indirection), (3) No AUTOINCREMENT support, (4) Cannot use rowid-based optimizations like ORDER BY RANDOM() LIMIT 1. Best for tables with composite primary keys.

## Q73: How does SQLite handle ALTER TABLE DROP COLUMN (3.35.0+)?
**A:** ALTER TABLE DROP COLUMN (3.35.0+) marks the column as removed in the schema but does not immediately rewrite the database. On subsequent writes to each row, the dropped column's data is actually removed. The column is invisible to queries. The database file shrinks only after VACUUM. Restrictions: cannot drop PRIMARY KEY columns, columns with UNIQUE constraint, or columns referenced by triggers/views.

## Q74: How do you configure the memory-mapped I/O size for best performance?
**A:** PRAGMA mmap_size sets the maximum bytes SQLite will memory-map. For read-heavy workloads on SSDs, set to 2GB-256GB. For write-heavy workloads, keep lower or disable (0) to avoid mapping overhead. Memory-mapped I/O reduces read() system calls but increases page fault overhead on first access. Monitor with vmstat and iostat. On 32-bit systems, mmap size is limited by address space.

## Q75: How does SQLite handle the SQLITE_LIMIT_ATTACHED limit?
**A:** SQLITE_LIMIT_ATTACHED (default: 10) limits how many databases can be attached via ATTACH DATABASE. Each attached database consumes file descriptors and cache memory. For connections that need many attached databases (e.g., sharding), increase this limit: sqlite3_limit(db, SQLITE_LIMIT_ATTACHED, 50). Performance decreases with more attachments due to cache competition and namespace resolution overhead.

## Q76: How do you implement a full outer join in SQLite?
**A:** SQLite does not support FULL OUTER JOIN natively. Simulate with UNION of LEFT JOIN and RIGHT JOIN (using reversed tables): SELECT * FROM t1 LEFT JOIN t2 ON t1.id = t2.id UNION SELECT * FROM t1 RIGHT JOIN t2 ON t1.id = t2.id (requires SQLite 3.39.0+ for RIGHT JOIN). Without RIGHT JOIN support, use SELECT * FROM t1 LEFT JOIN t2 ON ... UNION SELECT * FROM t2 LEFT JOIN t1 ON ... WHERE t1.id IS NULL.

## Q77: How does PRAGMA recursive_triggers affect trigger behavior?
**A:** PRAGMA recursive_triggers (default: OFF) controls whether triggers can fire recursively. When OFF, a trigger that modifies a table does not fire triggers on that table again. When ON, recursive trigger chains are allowed. Recursive triggers can cause infinite loops if not carefully designed. A trigger call depth limit (SQLITE_LIMIT_TRIGGER_DEPTH, default 1000) prevents runaway recursion.

## Q78: How does SQLite handle database-level CHECK constraints vs column-level CHECK constraints?
**A:** Table-level CHECK constraints can reference multiple columns: CHECK (end_date > start_date). Column-level CHECK constraints reference only the column being defined. Table-level constraints are evaluated after all column values are known; column-level constraints are evaluated as each column is populated. Both follow the same NULL behavior (pass if expression is TRUE or NULL).

## Q79: What is the sqlite3_compileoption_get() API used for?
**A:** sqlite3_compileoption_get() returns compile-time options one by one (used with sqlite3_compileoption_used() to check specific options). Useful for: (1) Verifying which features are available at runtime (threadsafe, enable_fts5, etc.), (2) Debugging deployment issues where SQLite was compiled with different options, (3) Feature detection in libraries that use SQLite. PRAGMA compile_options returns the same info as text.

## Q80: How do you handle SQLite in a microservices architecture where each service has its own database?
**A:** Each microservice owns its SQLite database file. Challenges: (1) No shared data access between services (use APIs), (2) File system coordination (use Kubernetes persistent volumes or dedicated storage), (3) Backup per service independently, (4) Schema migrations per service, (5) No global transactions across services (use saga pattern). Advantages: simplicity, no central database bottleneck, independent scaling. Not suitable for services that need ACID across service boundaries.

## Q81: How does SQLite handle correlated subqueries in terms of optimization?
**A:** SQLite may flatten correlated subqueries into joins when possible. If flattening is not possible (e.g., aggregate subquery, LIMIT in subquery), the subquery is executed once per outer row, potentially O(N*M). To optimize: (1) Add indexes on subquery WHERE columns, (2) Rewrite as JOIN if possible, (3) Use window functions instead of correlated subqueries in some cases. EXPLAIN QUERY PLAN shows whether the subquery is correlated.

## Q82: What is the role of the sqlite3_int64 and sqlite3_uint64 types?
**A:** sqlite3_int64 and sqlite3_uint64 are 64-bit integer types used by SQLite's API. sqlite3_int64 is signed (-2^63 to 2^63-1) and used for rowid and most count/offset APIs. sqlite3_uint64 is unsigned (0 to 2^64-1). On platforms without native 64-bit support, SQLite implements software 64-bit arithmetic. PRAGMA MAX_PAGE_COUNT uses these for the maximum page limit.

## Q83: How do you use SQLite as a message broker for pub-sub patterns?
**A:** SQLite as pub-sub: Create a subscriptions table and an events table. Producers insert events. Consumers poll for new events using a high-watermark (last_event_id). Use WAL mode and shared cache for multiple consumer processes. Limitations: polling not push-based, writer serialization limits throughput, no native topic routing. For >10K messages/sec, consider dedicated message brokers (RabbitMQ, Redis, NATS).

## Q84: What is the effect of PRAGMA application_id?
**A:** PRAGMA application_id sets a 32-bit identifier stored at offset 68 of the database header. It is used by applications to identify file types (e.g., Apple uses 0x4141504C for .app files, Firefox uses 0x48696768). SQLite itself does not use this value. The .dump command reads it. Useful for: file type detection, custom database formats, application-specific metadata in the header.

## Q85: How does SQLite handle the RAISE() function in triggers?
**A:** RAISE() in triggers aborts the trigger and can specify an error: RAISE(ABORT, 'error message'), RAISE(ROLLBACK, 'msg'), RAISE(FAIL, 'msg'), RAISE(IGNORE). IGNORE skips the current operation without error (useful for conditional insert suppression). ROLLBACK rolls back the entire transaction. ABORT rolls back only the current statement. These correspond to the conflict resolution modes.

## Q86: How do you use savepoints in SQLite for nested transactions?
**A:** SQLite supports savepoints for nested transaction control: SAVEPOINT sp1; ...; SAVEPOINT sp2; ...; RELEASE sp2; ...; ROLLBACK TO sp1; RELEASE sp1. Savepoints allow partial rollback without aborting the entire transaction. Useful for: (1) Batch processing where some items can fail, (2) Complex operations with multiple stages, (3) Error recovery in long-running transactions. Nested depth default is 1000 (SQLITE_LIMIT_TRIGGER_DEPTH).

## Q87: What is the SQLITE_MISUSE error, and how do you avoid it?
**A:** SQLITE_MISUSE occurs when SQLite APIs are called in the wrong sequence or from the wrong thread (without SQLITE_CONFIG_MULTITHREAD/SERIALIZED). Common causes: (1) Calling sqlite3_step() after sqlite3_finalize(), (2) Using a prepared statement on a different connection, (3) Thread safety violations. Avoid by: (1) Always checking return codes, (2) Using proper thread safety configuration, (3) Following the prepare -> bind -> step -> finalize lifecycle.

## Q88: How does PRAGMA legacy_file_format affect compatibility?
**A:** PRAGMA legacy_file_format (deprecated) controlled whether new databases used the legacy (3.x) or current file format. Modern SQLite versions use file format 4. The format affects: (1) Index storage (descending indexes in format 4), (2) VARCHAR and CHAR column types (no difference in storage), (3) Large file support. New databases should use the current format. The legacy format is only needed for compatibility with SQLite 3.0.x.

## Q89: How do you implement a SQLite-based full-text search with custom ranking?
**A:** FTS5 with custom ranking: Create a virtual table with FTS5, then define a custom ranking function: CREATE FUNCTION custom_rank RETURNS REAL; int custom_rank(sqlite3_context *ctx, int argc, sqlite3_value **argv). Register with sqlite3_create_function(). The function receives FTS5 metadata (match info) and can implement TF-IDF, BM25F, or domain-specific ranking. Use in queries: ORDER BY custom_rank(docs, 'my query', 0.5).

## Q90: How does SQLite's xBestIndex in virtual tables optimize query plans?
**A:** xBestIndex receives a list of WHERE clause constraints (column, operator, value binding) and ORDER BY information. It returns a cost estimate and an output plan with usage flags. The optimizer calls xBestIndex multiple times with different constraint combinations to find the cheapest plan. A virtual table should: (1) Estimate cost based on constraint selectivity, (2) Indicate which constraints it can handle efficiently, (3) Mark constraints as usable or not. Lower cost = better plan.

## Q91: What is the interaction between PRAGMA page_size and PRAGMA cipher_page_size (SQLCipher)?
**A:** In SQLCipher, cipher_page_size is independent of SQLite's page_size. The cipher page size covers the encrypted page including HMAC and IV overhead. When SQLite's page_size is 4096, the on-disk cipher_page_size might be 4112 (4096 + 16 IV + 32 HMAC). This means what SQLite sees as a 4096-byte page occupies more space on disk. Changing page_size after encryption requires migrating the entire database.

## Q92: How do you handle concurrent readers with IMMEDIATE transactions in WAL mode?
**A:** IMMEDIATE transactions in WAL mode start a write transaction immediately. While an IMMEDIATE transaction is active: (1) Other readers can still read from the database file (old snapshot), (2) Other writers are blocked (SQLITE_BUSY), (3) The active writer appends to the WAL, (4) Readers that open new transactions after the write started may or may not see the uncommitted data (controlled by read_uncommitted pragma). IMMEDIATE is preferred over EXCLUSIVE for most write workloads.

## Q93: How does SQLite's sqlite3_db_cacheflush() work?
**A:** sqlite3_db_cacheflush() (SQLITE_ENABLE_DBSTAT_VTAB) forces SQLite to write all dirty cache pages to disk. This is useful for: (1) Ensuring data durability without closing the database, (2) Reducing checkpoint size in WAL mode, (3) Testing crash recovery scenarios. It does not guarantee fsync (combine with PRAGMA synchronous for durability). This is a debugging/utility function, not typically needed in production.

## Q94: What are the limitations of SQLite for high-concurrency write workloads compared to PostgreSQL?
**A:** Key limitations: (1) Single writer - only one transaction can write at a time, (2) File-level locking - at the OS level, not row-level, (3) Coarse-grained concurrency control - WAL mode helps reads but writes still serialize, (4) No replication for read scaling, (5) No connection pooling at the database level, (6) Write throughput capped at about 50-100MB/s on typical SSDs. PostgreSQL WAL + MVCC handles thousands of concurrent writes. SQLite is designed for embedded/single-server use, not OLTP with hundreds of concurrent users.

## Q95: How do you use PRAGMA threads for parallel query execution?
**A:** PRAGMA threads (default: 0, uses number of CPU cores) sets the number of worker threads SQLite can use for (1) parallel index creation, (2) parallel sort operations, (3) parallel VACUUM. As of SQLite 3.39.0+, only index creation benefits from parallelism. Example: PRAGMA threads=4 speeds up CREATE INDEX on large tables. Query execution remains single-threaded. Set to 1 to disable parallel operations.

## Q96: How does the SQLite error log callback work?
**A:** sqlite3_config(SQLITE_CONFIG_LOG, callback, data) registers a global error log callback that receives all SQLite internal errors and warnings (not per-connection errors, which are retrieved via sqlite3_errmsg()). Useful for: (1) Monitoring silent failures like I/O retries, (2) Debugging corruption detection, (3) Auditing authorization denials. The callback receives error code, message, and user data.

## Q97: How do you implement a SQLite database health check that monitors for corruption?
**A:** Health check routine: (1) Run PRAGMA integrity_check on a schedule, (2) Verify the database file size is within expected bounds, (3) Check for -wal and -shm file existence (should exist only if WAL mode is active), (4) Verify last backup timestamp, (5) Check PRAGMA page_count vs actual file size, (6) Verify PRAGMA schema_version changes only during migrations, (7) Monitor error logs for SQLITE_CORRUPT or SQLITE_IOERR.

## Q98: How does SQLite handle the = and IS operators differently for NULL?
**A:** In SQLite, col = NULL always returns NULL (false in WHERE clauses) because NULL comparisons use three-valued logic. col IS NULL returns true if the value is NULL. Similarly, col != NULL is always NULL (use IS NOT NULL). This follows the SQL standard. The behavior is consistent for all data types including TEXT, INTEGER, and BLOB.

## Q99: What is the difference between immediate and deferred index creation?
**A:** SQLite's PRAGMA defer_foreign_keys controls when foreign key constraints are checked. For indexes: (1) CREATE INDEX (immediate) builds the index synchronously and can use significant I/O, (2) There is no deferred index build, (3) CREATE INDEX CONCURRENTLY (3.35.0+) builds the index while allowing concurrent writes. The new index becomes available only when the build completes. Concurrent builds use more disk space temporarily.

## Q100: How do you use SQLite with WebAssembly (WA-SQLite) for browser-based applications?
**A:** WA-SQLite compiles SQLite to WebAssembly for in-browser database use. Features: (1) Full SQLite in the browser with persistent storage via OPFS (Origin Private File System) or IndexedDB, (2) WAL mode for concurrent access within the same origin, (3) Support for FTS5, JSON1 extensions, (4) Performance: millions of rows/second for in-memory, thousands for persistent storage. Limitations: no direct file system access, limited persistence across browser sessions, single-origin sandbox. Used for offline-first apps, PWA data caching, and client-side analytics.
