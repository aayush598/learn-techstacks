# Priority 2 — PostgreSQL (Q325–Q340)

**Why these matter for micro1:** PostgreSQL is the required skill. Expect: JSONB, index types, MVCC, VACUUM, optimization, and schema design for the AI conversation system. Many answers extend the Priority 1 SQL chapter — link them.

---

## Q325: Why use PostgreSQL?

1. **Mature, standards-compliant relational DB** — full ACID, rich SQL (window functions, CTEs, full-text search, JSON).
2. **Extensible:** JSONB, arrays, `tsvector`, extensions (`pgvector`, `postgis`, `pg_trgm`, `citext`).
3. **MVCC concurrency** — readers never block writers (Q335).
4. **Reliability & features:** WAL, PITR, replication (streaming/logical), partitioning, materialized views, triggers.
5. **Strong ecosystem** — SQLAlchemy, asyncpg, Alembic; hosted options (RDS, Aurora).
6. **Performance at scale** with proper indexes, partitioning, tuning.
7. **Open source + permissive license**; massive community.
8. For the AI recruiter: relational core + JSONB for flexible AI data + `pgvector` for embeddings → one database covers almost everything.

---

## Q326: What are PostgreSQL's main advantages?

- **ACID + MVCC** (isolation without locking readers).
- **JSONB** — flexible schema-less data + GIN indexes.
- **Advanced indexing:** B-tree, GIN, GiST, BRIN, hash, partial, expression, covering.
- **Advanced SQL:** window functions, CTEs/recursive, `LATERAL`, `DISTINCT ON`, full-text search, `RETURNING`.
- **Extensibility:** `pgvector` (vector search!), PostGIS, triggers/functions in PL/pgSQL or Python.
- **Replication:** streaming (hot standby) + logical replication + `pg_upgrade`/zero-downtime upgrades.
- **Tooling:** `EXPLAIN ANALYZE`, `pg_stat_statements`, autovacuum, `pg_dump`/`pg_restore`, `pgbouncer`.
- **Cost:** open source; predictable performance; huge talent pool.

---

## Q327: What is JSONB?

A PostgreSQL **binary JSON type** — stores JSON documents in an internal binary format with efficient querying and indexing.

```sql
CREATE TABLE profiles (
  id BIGSERIAL PRIMARY KEY,
  data JSONB
);

INSERT INTO profiles (data) VALUES
  ('{"skills": ["python", "react"], "years": 3}');

-- querying
SELECT * FROM profiles WHERE data->>'years' = '3';
SELECT * FROM profiles WHERE data @> '{"skills": ["python"]}';   -- contains
```

- **Validates JSON** at insert; **normalizes keys** (duplicates removed); supports `->`, `->>`, `@>`, `?`, `#>` operators.
- Can be **indexed with GIN** (Q330) for `@>`/`?`/`->` lookups.
- For embeddings: `pgvector` stores vectors in a column alongside JSONB — one stack.

---

## Q328: JSON vs JSONB?

| | `json` | `jsonb` |
|---|---|---|
| Storage | Text — exact copy (whitespace/keys preserved) | Binary — normalized, no whitespace/dups |
| Speed | Slower reads (reparse) | **Faster** reads/querying |
| Indexing | None (expression indexes only) | **GIN index** support |
| Write speed | Faster (no processing) | Slower (parse + normalize) |
| Default? | — | **Preferred** in practice |

**Rule:** use `JSONB` almost always. `json` only when you need byte-exact preservation of input (rare) or pure storage of opaque payloads.

---

## Q329: When would you use JSONB?

1. **Flexible/semi-structured data** that varies per row: candidate profiles, job requirements, evaluation criteria, AI-generated metadata.
2. **Fast schema evolution** — add fields without migrations.
3. **Nested documents** queried with `@>`/GIN (e.g., "find all candidates with skill X").
4. **Caching/payloads** — store third-party API responses, webhook payloads.
5. **Storing embeddings alongside JSON** (pgvector extension).

**When NOT:** data you query/join by structured columns (use relational + indexes), data needing referential integrity, hot transactional fields, or where strict typing matters.

**Tradeoff answer:** "JSONB buys flexibility and speed of change at the cost of no relational integrity and weaker validation — I use it for the flexible 'extras', never for the core query paths."

---

## Q330: What are PostgreSQL indexes?

(Extended from Q160–165.) PostgreSQL provides multiple access methods:

- **B-tree** (default): equality + range (`=`, `<`, `>`, `BETWEEN`, `ORDER BY`). Best general-purpose.
- **GIN** (Generalized Inverted Index): for composite/array/JSONB/full-text — `@>`, `?`, `tsvector`.
- **GiST**: geometry, ranges, similarity (also enables `pg_trgm`).
- **BRIN**: block-range summaries — tiny indexes for huge, append-ordered tables (logs, time series).
- **Hash**: equality only (rarely better than B-tree).
- **Partial** (WHERE clause), **expression** (`lower(email)`), **covering** (`INCLUDE`).

```sql
CREATE INDEX idx_profiles_skills ON profiles USING GIN (data);
CREATE INDEX idx_users_email_lower ON users (lower(email));
CREATE INDEX idx_candidates_active ON candidates (status) WHERE status = 'active';
```

---

## Q331: What is a B-tree index?

The default index type — a **balanced search tree** with sorted keys, giving **O(log n)** lookup for equality, range, prefix, and sorted access.

- Each node holds multiple keys; leaves point to heap rows (or hold data in index-only scans).
- Supports `=`, `<`, `>`, `<=`, `>=`, `BETWEEN`, `IN`, and `ORDER BY`.
- Efficient for point lookups, range scans, and **sorted output without a sort step**.
- Why the default: covers the vast majority of query patterns.

---

## Q332: What is a partial index?

An index on a **subset of rows** — defined with a `WHERE` predicate.

```sql
CREATE INDEX idx_candidates_pending ON candidates (created_at) WHERE status = 'pending';
```

- Smaller, faster, cheaper to maintain than a full index.
- Perfect when queries always filter by a skewed value (e.g., 99% `done`, 1% `pending` — index only the 1%).
- Planner uses it when the query's `WHERE` implies the predicate.

---

## Q333: What is a composite index?

See Q163 — multi-column index with the **leftmost-prefix rule**; order columns equality-first, then range/sort.

```sql
CREATE INDEX idx_applications_job_status ON applications (job_id, status);
-- serves WHERE job_id=? AND status=?  (and WHERE job_id=?)
-- does NOT serve WHERE status=? alone
```

---

## Q334: What are PostgreSQL transactions?

(Extended from Q152–153.) Wrapped in `BEGIN`/`COMMIT` (or `ROLLBACK`), guaranteed **ACID**, using **MVCC** for isolation.

```sql
BEGIN;
INSERT INTO applications (candidate_id, job_id) VALUES (1, 10);
UPDATE jobs SET applicants = applicants + 1 WHERE id = 10;
COMMIT;   -- atomic: both or neither
```

- Isolation levels: READ COMMITTED (default), REPEATABLE READ, SERIALIZABLE (Q173).
- Use for multi-statement invariants; keep short; errors inside → `ROLLBACK`.

---

## Q335: What is MVCC?

**Multi-Version Concurrency Control** — PostgreSQL's concurrency model:

- Every transaction sees a **consistent snapshot** of committed data as of its start point.
- **Writers never block readers and readers never block writers.** A writer's uncommitted changes live in a new row version; other transactions keep reading the old version until commit.
- Implemented via: **xmin/xmax** system columns on each row version + a transaction ID (XID) visibility rule, plus the **WAL** for durability.
- Old versions accumulate → cleaned by **VACUUM** (Q336).
- Effect: high concurrency, no dirty reads (READ COMMITTED), snapshot isolation (REPEATABLE READ).

**Why it matters for micro1:** a busy recruiting platform does many concurrent reads/writes; MVCC keeps it responsive.

---

## Q336: What is VACUUM?

The process that **removes dead row versions** created by MVCC (updates/deletes) and recycles the space.

- **Autovacuum** runs automatically in the background (usually fine).
- `VACUUM` — reclaims space, refreshes visibility map, updates stats (can run concurrently with reads/writes).
- `VACUUM FULL` — compacts the table (takes a lock, rewrites; use during maintenance).
- `ANALYZE` — refreshes planner statistics (often run together: `VACUUM ANALYZE`).
- **Why care:** without VACUUM, tables **bloat** — slower scans, bigger storage, transaction ID wrap risk.

**Interview angle:** "bloat is why an old table gets slow despite indexes — monitor `pg_stat_user_tables` for dead tuples and bloat; rely on autovacuum tuned for aggressive updates."

---

## Q337: What is `ANALYZE`?

Refreshes the **statistics** (row counts, value distribution/histograms) the planner uses to estimate costs.

```sql
ANALYZE candidates;
```

- Stale stats → bad plans → suddenly-slow queries (est. rows far from actual).
- Runs automatically (autovacuum), but run manually after large bulk loads.
- In debugging: `ANALYZE` first, then re-`EXPLAIN` (Q169).

---

## Q338: How would you optimize a PostgreSQL database?

1. **Queries first:** `EXPLAIN (ANALYZE, BUFFERS)` + `pg_stat_statements` — find the expensive ones (Q169, Q245).
2. **Indexes:** add for hot filters/joins/orders; partial/composite/covering as needed; remove unused (Q330–333, Q162).
3. **`ANALYZE`/statistics** freshness (Q337).
4. **Schema:** normalization where it matters, denormalization/materialized views for aggregates (Q158–159, Q556).
5. **Config tuning:** `shared_buffers` (e.g., 25% of RAM), `work_mem` (sorts/hashes), `maintenance_work_mem`, `effective_cache_size`, `max_connections`, autovacuum settings.
6. **Concurrency:** connection pooling (PgBouncer), `statement_timeout`, avoid long transactions/locks.
7. **Storage/hardware:** fast disks (NVMe), enough RAM for the working set.
8. **Scale-out:** read replicas (Q566), partitioning big tables (Q558–560), sharding only when truly needed.
9. **Monitoring:** slow-query log, `pg_stat_statements`, dead-tuple/bloat checks, disk/latency (Q630).
10. **Maintenance:** routine `VACUUM ANALYZE`, `REINDEX` when bloaty (Q336).

---

## Q339: How would you handle millions of rows?

1. **Indexes tuned to the access patterns** — always query by indexed keys; avoid `SELECT *` scans (Q245).
2. **Pagination (cursor/keyset)** — never `OFFSET` deep into millions of rows (Q256–257).
3. **Partitioning** — range-partition append-only tables (conversations, messages, events) by date; queries prune partitions (Q558–560).

```sql
CREATE TABLE messages (...) PARTITION BY RANGE (created_at);
-- one partition per month; old ones dropped/archived cheaply
```

4. **Partial + covering indexes** to shrink index size (Q332, Q163).
5. **Materialized views** for heavy aggregates/reports (Q556).
6. **Batching** bulk loads; avoid long transactions.
7. **Aggregate in DB, not in app** — push computation down.
8. **Read replicas** for reporting load (Q566).
9. **Keep working set in RAM** (shared_buffers + OS cache).
10. **Archive/retention** — move cold data (older than N months) to cheap storage (S3) or partitioned-off tables.
11. **Monitor** — bloat, dead tuples, index sizes; keep autovacuum healthy (Q336).

---

## Q340: How would you design PostgreSQL tables for an AI conversation system?

**Walk through a schema:**

```sql
CREATE TABLE conversations (
  id BIGSERIAL PRIMARY KEY,
  candidate_id BIGINT REFERENCES candidates(id),
  interview_id BIGINT,              -- optional interview run
  title TEXT,
  status TEXT NOT NULL DEFAULT 'active',   -- active | completed | abandoned
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE messages (
  id BIGSERIAL PRIMARY KEY,
  conversation_id BIGINT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('system','user','assistant','tool')),
  content TEXT NOT NULL,
  tool_call_id TEXT,                 -- for tool messages
  model TEXT,                        -- model used
  prompt_tokens INT, completion_tokens INT,   -- cost/analytics
  latency_ms INT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_messages_conv ON messages (conversation_id, id);   -- cursor pagination
CREATE INDEX idx_messages_conv_time ON messages (conversation_id, created_at);
```

**Design choices to mention:**
1. **Append-only messages** — audit-friendly, replayable; paginate with **keyset** by `(conversation_id, id)`.
2. **JSONB** for flexible per-message metadata and context state (Q327–329).
3. **Partitioning** `messages` by month if it grows huge (Q558).
4. **Token/cost columns** per message → analytics (cost per interview, Q631).
5. **Concurrency:** each conversation append-only → low lock contention; `ON CONFLICT` for idempotent inserts (Q396–397).
6. **`pgvector`** column/table for embeddings (question embeddings, candidate semantic search) (Q657).
7. **Indexes:** FK columns, composite pagination keys, GIN on JSONB for flexible filters.
8. **Read replicas** for analytics; **materialized views** for dashboards (Q556).
9. **Retention policy** — archive/delete per compliance; partition drops make it cheap (Q558).
10. **Audit trail** — a separate append-only `ai_audit` table for agent actions (Q683).