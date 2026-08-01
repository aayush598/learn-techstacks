# Data Dictionary and Metadata

> **TL;DR**: The data dictionary (system catalog) is the database's "data about data" — a set of system tables describing tables, columns, types, constraints, indexes, users, and privileges — and it's what makes the DBMS self-describing, since the DBMS reads its own catalog to plan queries and enforce rules.

## 1. Why Does This Exist?
A DBMS cannot validate a query, enforce constraints, plan an index lookup, or grant privileges unless it *knows* what tables, columns, types, keys, and users exist. The data dictionary exists to hold that knowledge *inside the database itself*, so the DBMS is **self-describing**: the same engine that serves user queries reads its own metadata to decide how to serve them. It exists because hardcoding schema knowledge in the engine (or in each app) would break data independence, make DDL meaningless, and make the optimizer blind. It is the DBMS's *memory of its own structure*.

## 2. How Does It Work?
At startup and DDL time, the DBMS reads and writes catalog tables (relations) exactly like user tables, but protected. Flow: `CREATE TABLE students(...)` → DDL processor updates catalog rows (adds table row, column rows, constraint rows) → on every subsequent query the parser *reads* the catalog to resolve names/types → the optimizer reads catalog *statistics* (row count, distinct values) to estimate costs → the authorization manager reads catalog *privilege* rows to allow/deny access. The catalog is stored in ordinary pages, is cached, and is itself covered by WAL/transactions (catalog changes are transactional). Postgres calls it `pg_catalog` (plus `pg_*` system schemas); the SQL standard mandates `information_schema` as a portable, read-only view over it.

## 3. When Is It Used?
- **Every query**: name/type resolution, privilege checks, statistics for planning.
- **Every DDL**: `CREATE/ALTER/DROP` modify catalog rows (and are transactional).
- **Every constraint check**: FK enforcement reads catalog to find the referenced table and its unique index.
- **Tooling**: `information_schema`, `pg_catalog`, `SHOW TABLES`, `DESCRIBE`, `\d` in psql, DBMS metadata APIs — all read the dictionary.
- **Migration/orchestration**: Flyway, Liquibase, ORM schema introspection read the catalog to diff models against reality.
- **Privileges**: `GRANT`/`REVOKE` store per-user-per-object grants in catalog tables; the authorization manager consults them on every statement.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: schema knowledge hardcoded in each application.** Rejected: violates data independence (app changes when schema changes), no single source of truth, impossible to audit, no central constraint enforcement.
- **Alternative: separate configuration file (e.g., a `schema.json` read by the engine).** Rejected: needs external synchronization (can drift from actual DB), isn't transactional, isn't queryable, and can't store statistics/privileges that the engine itself maintains. Keeping metadata as *data in the DB* makes it consistent, transactional, and queryable for free.
- **Alternative: keep metadata only in memory.** Rejected: must be rebuilt on restart and shared across processes; persisted catalog is durable and concurrency-safe.
- **Why `information_schema` as a layer?** A portable, standard, read-only view so tools (and humans) can introspect any SQL DBMS without vendor-specific knowledge; the vendor keeps its private physical catalog underneath.

## 5. Intuition
A library keeps a **catalogue** of all its books: title, author, shelf, availability. The catalogue is itself a set of cards — it lives *in* the library, not in the librarian's head or in a document at home. Every time someone asks "do you have X?" the librarian checks the catalogue; when a book is added or moved, the librarian *updates* the catalogue. The catalogue is "data about books" — metadata. The DBMS's data dictionary is exactly this: the catalogue that describes the shelves (tables), the cards' fields (columns), the cross-references (indexes/keys), and the borrowing rules (constraints and privileges). And critically — *it can be queried with the same search language as the books themselves.*

## 6. Real-World Analogy
A **hospital's master patient index and charge master**. The charge master is a registry of every test, medication, and procedure: its code, name, price, and insurance rules. Every billing transaction looks it up; adding a new procedure updates the registry; auditing is done *against* the registry. The registry is data about the business (metadata), and the business literally runs on it. If two departments kept their own copies, prices would diverge — exactly why the catalog is centralized inside the DBMS rather than duplicated in apps. The catalog is the DBMS's charge master.

## 7. Formal Definition
The **data dictionary / system catalog** is a set of tables stored within the database that describe the database itself: relation names, attribute names and types, constraints (PK/FK/UNIQUE/CHECK), indexes, views, stored procedures, user accounts and privileges, plus optimizer statistics. It makes the DBMS **self-describing**. The SQL standard defines `INFORMATION_SCHEMA` as a set of standardized, read-only views over vendor catalogs; PostgreSQL exposes `pg_catalog` and the `information_schema`; MySQL exposes `information_schema` and `mysql.*` privilege tables. Catalog contents are metadata (data about data), distinguished from the user data they describe. (Elmasri & Navathe Ch. 2; Silberschatz Ch. 1.4, 27.)

## 8. Example
You run `CREATE TABLE students (id INT PRIMARY KEY, name TEXT, gpa NUMERIC(3,2));`. Behind the scenes the catalog now contains rows roughly like:
```
pg_class:      (relname='students', relkind='r', reltuples=0, ...)
pg_attribute:  (attname='id', atttypid=int4, attnotnull=true, ...)
               (attname='name', atttypid=text, ...)
               (attname='gpa', atttypid=numeric, ...)
pg_constraint: (conname='students_pkey', contype='p', conkey={1}, ...)
pg_index:      (indexrelid=..., indkey={1}, indisunique=true, ...)
```
Now `SELECT name FROM students WHERE gpa > 3.5`: the parser looks up `students`, `name`, `gpa` in `pg_attribute`/`pg_class` (validates types), the optimizer reads statistics, the privilege manager checks the user's grants, and execution proceeds. `SELECT * FROM information_schema.columns WHERE table_name='students'` returns the same info in a portable, readable form.

## 9. Internal Working
1. **DDL**: `CREATE TABLE` → DDL executor validates the statement → inserts catalog rows inside a transaction (so an aborted DDL leaves no partial catalog state) → builds/rebuilds dependent objects (indexes for PK/UNIQUE).
2. **Startup**: the DBMS opens its catalog, verifies integrity, and loads base catalogs into shared memory.
3. **Query path**: parser → catalog lookup (name resolution, type checking) → authorization (catalog grants) → optimizer (catalog statistics: `reltuples`, `n_distinct`, histograms) → executor.
4. **Constraint enforcement**: FK check on insert/update → catalog lookup finds the referenced table's unique index → lookup executed; the catalog is read on the hot path (which is why catalog rows are cached).
5. **Statistics maintenance**: `ANALYZE`/auto-vacuum recompute `pg_statistic` rows; optimizer cost estimates depend on their freshness.
6. **Introspection**: `information_schema` views join vendor catalogs to present standard columns; tools (psql `\d`, JDBC `DatabaseMetaData`) query them.

## 10. Time Complexity
- **Catalog lookup per query**: O(1)–O(log n) via catalog indexes + cache (catalog rows are small and hot) — effectively negligible per query.
- **DDL**: O(size of objects created) — creating an index is O(n log n) on the table; catalog inserts are O(1) per row.
- **Statistics refresh (ANALYZE)**: O(sample size) per table (sampling, not full scan).
- **Privilege check**: O(number of grants) worst, but cached per role → effectively O(1).
- **Introspection query**: O(catalog size) scan on the relevant catalog relation — small.

## 11. Advantages
- **Self-describing database**: the DBMS and tools can discover schema programmatically — this is what makes ORMs, migration tools, and generic drivers work.
- **Single source of truth**: schema lives in exactly one place; no drift between "documentation" and reality.
- **Transactional DDL**: catalog changes roll back with the transaction — a failed migration leaves no ghost schema.
- **Centralized authorization**: one place for grants; enforcement on every statement.
- **Optimizer intelligence**: statistics in the catalog enable cost-based planning (this is why `ANALYZE` exists).
- **Portability**: `information_schema` gives a vendor-neutral introspection layer.

## 12. Disadvantages
- **Catalog bloat**: stale statistics, many temp tables, and dropped-but-not-vacuumed objects inflate the catalog; needs maintenance (`VACUUM`, `ANALYZE`, `pg_catalog` pruning).
- **Introspection cost on hot paths**: very frequent `information_schema` queries (some ORMs) can add load; caching mitigates.
- **Overhead of transactional DDL**: heavy DDL inside big transactions can lock catalog rows and block concurrent DDL.
- **Security surface**: anyone with catalog read access sees structure metadata; permissions must guard it.
- **Catalog/code coupling**: upgrades of DBMS versions change catalog layout; tools must keep up.

## 13. Interview Questions
1. **Q: What is a data dictionary (system catalog)?** A: A set of system tables that describe the database itself: tables, columns, types, constraints, indexes, views, users, privileges, and statistics. It's the metadata store that makes the DBMS self-describing.
2. **Q: What is metadata? Give examples.** A: Data about data: table names, column names/types, constraint definitions, index definitions, user privileges, and optimizer statistics. Distinguish from user data (the actual rows).
3. **Q: What does "self-describing" mean?** A: The database contains its own description — the catalog is stored in the database and the DBMS reads it to validate queries, plan execution, and enforce constraints. No external schema file is required.
4. **Q: Where is the catalog stored?** A: In ordinary database pages, as system relations (e.g., `pg_class`, `pg_attribute` in Postgres), cached in shared memory, and covered by WAL/transactions like any user table.
5. **Q (tricky): Is the catalog user data?** A: No — it's metadata. It describes the schema; user data is the rows in user tables. (The catalog is *technically* stored like user tables, but semantically it's metadata.)
6. **Q: What is `information_schema` vs `pg_catalog`?** A: `information_schema` is the standard, portable, read-only SQL view layer over metadata; `pg_catalog` is Postgres's private physical catalog (with all its system tables). Tools use `information_schema` for portability; internals use `pg_catalog`.
7. **Q: What happens inside the DBMS when you run `CREATE TABLE`?** A: DDL executes transactionally: catalog rows are inserted (table in `pg_class`, columns in `pg_attribute`, constraints in `pg_constraint`, indexes for PK/UNIQUE), then the storage layer allocates files. On rollback, all those catalog changes revert.
8. **Q (production): Why do ORMs sometimes run slow `SHOW COLUMNS`/metadata queries on startup?** A: Many ORMs introspect the catalog to build mapping caches (Hibernate, EF Core). On large catalogs or frequent reconnects, these `information_schema` queries add load. Mitigation: cache introspection results, reuse connections.
9. **Q: How does the optimizer use the catalog?** A: It reads statistics — row estimates (`reltuples`), distinct values (`n_distinct`), histograms — to estimate selectivity and choose indexes/join orders. Stale statistics → bad plans → slow queries. That's why `ANALYZE`/auto-vacuum matters.
10. **Q: How does the catalog enforce foreign keys?** A: On INSERT/UPDATE, the FK check reads the catalog to find the referenced table's unique constraint/index, then looks up the referenced value there. The catalog defines *what* to check; the executor does the lookup.
11. **Q: How is authorization stored?** A: Privilege grants (per user/role per object: SELECT/INSERT/UPDATE/DELETE) live in catalog tables (`pg_authid`, `pg_class.relacl`). The authorization manager checks them on every statement, and `GRANT`/`REVOKE` just update catalog rows.
12. **Q (tricky): Are DDL and DML both transactional?** A: In Postgres/Oracle/SQL Server, yes — DDL is transactional (schema changes roll back). In MySQL, DDL is mostly *implicitly committed* (non-transactional), a real behavioral difference interviewers like to test.
13. **Q: What is in `pg_statistic`?** A: Optimizer statistics computed by `ANALYZE`: per-column distinct counts, null fractions, most-common-values, and histogram bounds. These drive selectivity estimates for `WHERE` clauses.
14. **Q (scenario): A query plan shows a seq scan on a 10M-row table with a great index. How can the catalog be involved?** A: Stale statistics — the optimizer estimated the index as not selective (e.g., old `reltuples`, outdated histograms) and chose a scan. Fix: `ANALYZE` the table (and re-check the planner's estimates in `EXPLAIN`).
15. **Q: How do migration tools use the catalog?** A: They introspect the actual schema (via `information_schema`/`pg_catalog`) and diff it against the target model to generate `ALTER` statements — the catalog is the "ground truth" the migration validates against.
16. **Q: What is a catalog cache?** A: The DBMS caches catalog rows in shared memory (e.g., Postgres `syscache`) so the per-statement catalog lookups are O(1) memory hits instead of disk reads. This is why the catalog can be "read on the hot path" cheaply.
17. **Q (production): What does `VACUUM ANALYZE` do in Postgres?** A: `VACUUM` reclaims dead tuples/space (including catalog bloat), `ANALYZE` refreshes optimizer statistics in the catalog. Running it keeps plans good and catalog size bounded.
18. **Q: What does `DESCRIBE` / `SHOW TABLES` actually do?** A: They query the catalog (MySQL `SHOW` = `information_schema` lookups; Oracle `DESCRIBE` = `USER_TAB_COLUMNS`). They're user-friendly windows into the data dictionary.
19. **Q (hard): Can you write to the catalog directly?** A: Not safely — vendor catalogs are private and non-contractual; direct writes corrupt the DB. Use `information_schema` for reading and DDL for changing. Writing via DDL is the *only* supported mutation path.
20. **Q: How does the catalog relate to the three-schema architecture?** A: The catalog stores the descriptions of all three levels (external views, conceptual tables, internal indexes) and the mappings — it's the metadata repository that makes the three-schema architecture self-describing and implementable.

## 14. Follow-Up Questions
1. **Q: Does the catalog itself have an index?** A: Yes — system catalogs have their own indexes (e.g., `pg_class_oid_index`); catalog lookups are indexed like any table. That's why per-query overhead stays tiny.
2. **Q: What happens to the catalog during a migration that fails halfway?** A: In transactional DDL engines, everything rolls back — no partial catalog state. In MySQL, the already-applied DDL may remain (implicit commit), which is why migrations there are riskier.
3. **Q: Why is `ANALYZE`/statistics the #1 cause of plan regressions?** A: The optimizer's cost model is only as good as its estimates; histograms and row counts that are stale or skew-heavy lead to wrong joins/index choices. Refreshing + checking `EXPLAIN` is the standard fix.
4. **Q: Is the catalog the same as a "system database"?** A: Closely related — Postgres keeps the catalog inside each database's `pg_catalog` schema plus cluster-wide tables (`pg_database`, `pg_authid`); MySQL has a real `mysql` system database. Conceptually: system tables = the catalog.
5. **Q: Why do some NoSQL stores lack a catalog?** A: Because schema is implicit in documents; there's no central table-description to enforce. But even they keep internal catalogs (collection metadata, indexes, shard maps) — e.g., MongoDB's `admin.system.*` — just less exposed.

## 15. Coding Example
```sql
-- Standard, portable introspection (works on Postgres/MySQL/Oracle via information_schema)
SELECT table_name, column_name, data_type, is_nullable
FROM   information_schema.columns
WHERE  table_schema = 'public'
ORDER  BY table_name, ordinal_position;

-- See constraints via the standard views
SELECT tc.table_name, tc.constraint_type, kcu.column_name
FROM   information_schema.table_constraints tc
JOIN   information_schema.key_column_usage kcu
  ON   tc.constraint_name = kcu.constraint_name
WHERE  tc.table_name = 'students';
```
```sql
-- Postgres-specific catalog access
SELECT c.relname, a.attname, format_type(a.atttypid, a.atttypmod) AS type
FROM   pg_class c
JOIN   pg_attribute a ON a.attrelid = c.oid
WHERE  c.relname = 'students' AND a.attnum > 0
ORDER  BY a.attnum;
-- \d students  (psql) is just a prettier version of the same catalog query
```

## 16. Industry Usage
- **Every tool in the data ecosystem introspects the catalog**: psql `\d`, MySQL `SHOW`, JDBC/ODBC `DatabaseMetaData`, DBeaver/pgAdmin, dbt (which reads `information_schema` to model dependencies), and every migration framework.
- **dbt**, the analytics-engineering standard, runs catalog-driven `ref()`/lineage resolution — its whole model graph comes from metadata.
- **ORMs** (Hibernate, Prisma, Django) build SQL from catalog-derived mappings; schema introspection is how they stay in sync with the DB.
- **Postgres** ships `pg_catalog` + `information_schema`; **MySQL** ships `information_schema` + `mysql` system DB; **Oracle** uses `DBA_/ALL_/USER_` data dictionary views — all evidence the catalog is a universal, standardized component.
- **Automated plan tuning** (PgHero, pg_stat_statements) reads catalog statistics to recommend indexes — proving the catalog is the nervous system the whole performance stack reads.

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 2 (Data Dictionary / Catalog discussion).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 1.4 & Ch. 27 (Metadata; Data Dictionary).
- PostgreSQL Documentation, System Catalogs: https://www.postgresql.org/docs/current/catalogs.html
- PostgreSQL Documentation, The Information Schema: https://www.postgresql.org/docs/current/information-schema.html
- MySQL Reference Manual, `information_schema`: https://dev.mysql.com/doc/refman/8.0/en/information-schema.html
- ISO/IEC 9075-11:2016 (Information and Definition Schemas) — the `information_schema` standard.

## 18. Cheat Sheet
- Catalog = data dictionary = metadata about tables/columns/constraints/indexes/users/privileges/stats.
- Self-describing: the DB's description lives inside the DB; the engine reads it to plan/enforce.
- `pg_catalog` (Postgres) / `information_schema` (standard portable view) / `mysql.*` (MySQL).
- DDL writes the catalog; every query reads it (name resolution, privileges, stats).
- Optimizer stats: `reltuples`, `n_distinct`, histograms → bad stats = bad plans → `ANALYZE`.
- FK enforcement = catalog-driven lookup of the referenced unique index.
- Transactional DDL: Postgres/Oracle/SQL Server yes; MySQL mostly no (implicit commit).
- Catalog is not user data; don't write to it directly — use DDL.

## 19. Quiz
1. The data dictionary stores: a) user rows b) metadata c) WAL d) indexes only → **b**
2. "Self-describing" means: a) the DB documents itself b) the DB's description is stored in the DB c) the DB writes logs d) no schema needed → **b**
3. Which is the portable standard introspection view? a) pg_class b) information_schema c) mysql.db d) sys.objects → **b**
4. `CREATE TABLE` primarily updates: a) user tables b) catalog tables c) WAL only d) nothing → **b**
5. Optimizer statistics live in: a) pg_statistic b) WAL c) temp files d) client cache → **a**
6. Stale statistics can cause: a) data loss b) bad query plans c) deadlocks d) catalog corruption → **b**
7. In MySQL, DDL is: a) transactional b) implicitly committed c) disallowed d) in-memory → **b**
8. Foreign key enforcement reads: a) the WAL b) the catalog c) application config d) OS files → **b**
9. `\d students` in psql shows: a) query plans b) catalog info c) logs d) grants only → **b**
10. Writing to the catalog directly is: a) recommended b) supported but slow c) unsafe/unsupported d) required for tuning → **c**

## 20. Flashcards
- **Q: What is the data dictionary?** → **A:** System tables describing the DB itself: tables, columns, constraints, indexes, users, stats.
- **Q: What does self-describing mean?** → **A:** The database's own description is stored in the database (the catalog).
- **Q: pg_catalog vs information_schema?** → **A:** Private physical catalog vs standard portable read-only views.
- **Q: How does DDL use the catalog?** → **A:** DDL writes catalog rows transactionally (Postgres/Oracle).
- **Q: Why ANALYZE?** → **A:** Refreshes optimizer statistics in the catalog → good plans.
- **Q: How are FK checks catalog-driven?** → **A:** Catalog names the referenced table + unique index to check.
- **Q: Is DDL transactional in MySQL?** → **A:** Mostly no — implicit commit.
- **Q: Why not write to catalog directly?** → **A:** Private, non-contractual; corruption risk; use DDL.

## 21. Revision
The data dictionary is the DB's metadata store — tables, columns, types, constraints, indexes, users, privileges, statistics — and it lives *inside* the database, making the DBMS self-describing. Every query reads it (name resolution, privilege check, optimizer stats); every DDL writes it transactionally (except MySQL's implicit commit). `pg_catalog` is Postgres's physical catalog; `information_schema` is the portable read-only view; ORMs/migrations/dbt all introspect it. Interview moves: define metadata with examples; tie the catalog to three-schema (it stores all three levels); explain "stale stats → bad plan → ANALYZE"; and warn never to write the catalog directly. Mention `pg_statistic` (reltuples, histograms) to show depth.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a data dictionary / catalog?" | 7 / 13 Q1 |
| "What is metadata? examples?" | 13 Q2 |
| "What does self-describing mean?" | 7 / 13 Q3 |
| "How does the optimizer use the catalog?" | 13 Q9 |
| "Why are statistics important?" | 13 Q14 / 9 |
| "What is information_schema vs pg_catalog?" | 13 Q6 |
| "Is DDL transactional in MySQL?" | 13 Q12 |
| "How do ORMs use the catalog?" | 13 Q8 |
