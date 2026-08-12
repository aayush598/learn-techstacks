# Priority 4 — Advanced Database (Q549–Q568)

**Why these matter for micro1:** deep database questions separate seniors. Expect MVCC internals, locking, partitioning vs sharding, migrations at scale, and replication.

---

## Q549: What is MVCC? How does PostgreSQL implement it?

**MVCC (Multi-Version Concurrency Control):** readers never block writers and writers never block readers — each transaction sees a consistent **snapshot** of committed data.

**How Postgres does it:**
- Every row carries **`xmin`** (the transaction that inserted it) and **`xmax`** (the transaction that deleted/updated it).
- An **UPDATE** = new row version (new `xmin`); the old version is kept and marked dead via `xmax` (that's why updates are ~like insert+delete and create bloat, Q556).
- A transaction sees a row only if `xmin` is committed *before* its snapshot and `xmax` is not committed (visible) — decided by comparing against the **transaction snapshot** (`txid_current_snapshot()`, which knows which txids are in-flight).
- **Dead rows** (old versions no longer visible to anyone) are cleaned by **VACUUM** (Q556).

**Consequences:**
- Writers lock the *row version*, not the whole table → high concurrency.
- Long-running transactions block vacuum of old versions → bloat (Q556).
- There is **no read lock** in normal SELECTs — snapshot isolation for free.

---

## Q550: What isolation levels exist, and which does Postgres default to?

**ANSI levels (weakest → strongest):**
1. **Read Uncommitted** — see uncommitted data (dirty reads). Postgres doesn't really allow this; it's upgraded to Read Committed.
2. **Read Committed** — each statement sees a fresh snapshot (committed only). **Postgres default.**
3. **Repeatable Read** — one snapshot for the whole transaction (in Postgres; ANSI defines it as no non-repeatable reads).
4. **Serializable** — full serializability (SSI in Postgres: true serializable isolation via conflict detection).

**Anomalies:**
- **Dirty read** — reading uncommitted data (impossible in Postgres).
- **Non-repeatable read** — same row returns different values within a transaction (another commit changed it).
- **Phantom read** — a query returns different *sets* of rows (rows added by others).
- **Write skew** — two transactions read overlapping sets, each writes something that violates a constraint *if the other commits* (Serializable catches this).

**For the recruiter:** Read Committed is right for most flows; use Repeatable Read where a whole turn of business logic must see one consistent view (e.g., reading candidate + job + existing applications before creating one); Serializable only where true invariants matter (e.g., preventing double-booking the same interview slot).

---

## Q551: What is a lost update? How do you prevent it?

**Lost update:** two transactions read the same value, each computes a new value from it, both write — the second write overwrites the first's *unseen* change.

```sql
-- both read balance=100
UPDATE accounts SET balance = balance + 10 WHERE id=1;  -- A: 110
UPDATE accounts SET balance = balance + 10 WHERE id=1;  -- B: 110  (A's change lost)
```

**Prevention:**
1. **Atomic UPDATE** — `SET balance = balance + 10` (the read+write is atomic in the server; no read-then-write in app code).
2. **Optimistic locking** — include a `version` column; `UPDATE ... WHERE id=? AND version=?`; if `rowcount=0`, retry (Q553).
3. **Pessimistic locking** — `SELECT ... FOR UPDATE` (locks the row until commit).
4. **Serializable isolation** — SSI detects the write skew and aborts one.

**The core rule:** never do *read in app → compute → write* without a version check, row lock, or atomic statement.

---

## Q552: What is partitioning? When do you use it?

**Partitioning** splits one logical table into multiple physical storage chunks (`PARTITION BY RANGE (created_at)`) — same schema, separate storage (Q440).

```sql
CREATE TABLE messages (...) PARTITION BY RANGE (created_at);
CREATE TABLE messages_2026_01 PARTITION OF messages
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
```

**Benefits:**
- **Dropping old data is O(1)** — `DROP TABLE messages_2025_12` (vs DELETE of millions of rows).
- Queries that filter on the partition key hit only relevant partitions (**partition pruning**).
- Easier index rebuilds, backups by partition.

**Costs/limits:**
- **Partition key must be in WHERE clauses** or pruning fails (full scan of all partitions).
- Unique constraints must include the partition key.
- Cross-partition operations (FKs, some scans) get complex.
- Bloat management is per-partition.

**When:** time-series data (messages, audit_logs, notifications, events) past ~10–50M rows, or when retention deletes dominate.

---

## Q553: Optimistic vs pessimistic locking?

| | **Optimistic** | **Pessimistic** |
|---|---|---|
| Idea | Assume no conflict; check on write | Assume conflict; lock at read |
| Mechanism | `version`/`updated_at` column; `WHERE version=?` | `SELECT ... FOR UPDATE` |
| Blocking | None | Locks row until commit |
| Retry | On conflict, re-read + redo | None needed (wait on lock) |
| Best for | Read-heavy, low-contention, long transactions (don't hold DB locks across slow work) | High-contention short writes (e.g., decrementing stock) |

```python
# optimistic
async def shortlist(candidate_id, expected_version):
    row = await conn.fetch_one("""
        UPDATE candidates SET status='shortlisted', version=version+1
        WHERE id=$1 AND version=$2 RETURNING id""", candidate_id, expected_version)
    if row is None: raise ConflictError("state changed, retry")   # retry with fresh read
```

**Rule for your app:** hold no DB lock across an **LLM call** (seconds). Use optimistic versioning for status transitions (application → screening → shortlisted); pessimistic only for brief, hot mutations.

---

## Q554: What is a transaction? What are ACID properties?

**Transaction** = a unit of work that is all-or-nothing.

- **Atomicity** — all or nothing (rollback on failure). Postgres implements via WAL + transaction logs.
- **Consistency** — the DB moves between valid states (constraints, FKs, triggers hold).
- **Isolation** — concurrent transactions don't see each other's partial work (Q549–550).
- **Durability** — committed data survives a crash (WAL is fsynced before commit).

```python
async with conn.transaction():       # SQLAlchemy async
    app = await conn.execute(insert_application)
    await conn.execute(insert_interview, app_id=app.id)   # both-or-neither
```

**Careful:** transactions + external side effects (emails, LLM calls) — do DB work in the transaction, queue side effects *after* commit (Q433, Q443). Never hold a transaction open across a network call to the LLM.

---

## Q555: What is a deadlock? How do you avoid it?

**Deadlock:** two transactions each hold a lock the other needs → neither can proceed → Postgres detects it and **aborts one** (with `40P01` "deadlock detected").

```text
T1: UPDATE jobs SET ... WHERE id=1   -- holds job 1
    then: UPDATE candidates SET ... WHERE id=2   -- waits on cand 2
T2: UPDATE candidates ... WHERE id=2  -- holds cand 2
    then: UPDATE jobs ... WHERE id=1   -- waits on job 1  → deadlock
```

**Avoidance:**
1. **Acquire locks in a consistent global order** (always update by `id` ascending — sort your ids) — the #1 fix.
2. Keep transactions **short** (no LLM calls inside, Q554).
3. Use the **minimum lock scope** (row not table; shorter isolation when safe).
4. **Retry on deadlock** — catch `40P01` and retry the transaction (deadlocks are inherently racy; a bounded retry is the standard practice).

---

## Q556: What is bloat? What is VACUUM, and why is it needed?

**Bloat** = dead row versions that MVCC leaves behind (Q549) — they waste disk and slow scans (extra pages read).

- **VACUUM** removes dead tuples, reclaims space, updates visibility maps. It does **not** shrink table files back to the OS (that needs `VACUUM FULL`, which locks the table).
- **Autovacuum** runs automatically based on dead-tuple thresholds — tune thresholds/scheduling for write-heavy tables.
- **VACUUM FULL** — compacts + rebuilds indexes, but **takes a table lock** → only in maintenance windows.

**Why tables bloat in your app:** mass updates (resume re-parses rewrite the same rows), long-running transactions (they pin old versions), `UPDATE` on hot rows.

**Signs + fixes:** table size ≫ live row data, slowing seq scans → `pg_stat_user_tables` (n_dead_tup), tune autovacuum, avoid frequent UPDATEs on the same rows (denormalize/queue batch writes), drop-and-rebuild for bulk changes.

---

## Q557: What is replication? What are the types?

**Replication** = copying data to another node for availability, read scaling, or DR.

- **Physical/streaming replication (Postgres native):** the primary ships **WAL** to standbys which replay it — byte-identical copies. Standby is read-only. Used for **HA (Q436) + read replicas**.
- **Logical replication:** publishes logical changes (row inserts/updates) to subscribers — can be cross-version, cross-database, **selective (tables)** — great for CDC/event streams (feed a search index, analytics warehouse, cache).
- **Synchronous vs asynchronous:** sync standby confirms before commit (RPO=0, more latency); async is faster, may lag (replication lag = stale reads).

**Your architecture (Q440):** primary for writes; async replicas for read scaling; logical replication to feed the vector/search index or analytics; Multi-AZ sync standby for failover (RPO~0).

---

## Q558: How do you run schema migrations safely?

**Principles:**
1. **Forward-only, versioned migrations** (Alembic) — never edit an applied migration; add a new one.
2. **Backward compatible ordering** — each step works with the previous app version: **expand → migrate → contract**:
   - *Additive*: add column nullable / new table / new index (safe, both versions fine).
   - *Backfill*: populate data in batches (avoid giant locks).
   - *Contractive*: drop old column only after the new app version is fully deployed.
3. **Avoid lock-heavy DDL at peak:** `ADD COLUMN NOT NULL` without default locks the table (Q504); use a default + backfill, or batched `ALTER`.
4. **Test on a staging copy**, then run with `lock_timeout` so a stuck migration fails instead of blocking writes forever.
5. **Automated**: migrations run in CI/CD *before* the new app deploys; monitor for long locks (`pg_stat_activity`).

**Model answer:** "Alembic, forward-only; additive changes first (new column nullable), backfill in batches, drop later; run during low traffic with lock_timeout; never rewrite history."

---

## Q559: Index types in PostgreSQL beyond B-tree?

- **B-tree** — default; equality + range (`=`, `>`, `<`, `BETWEEN`, `ORDER BY`).
- **Hash** — equality only; rarely better than B-tree.
- **GIN (Generalized Inverted Index)** — for **array/JSONB containment** (`@>`), full-text search (`tsvector`), trigrams. The workhorse for `parsed_resume JSONB` and FTS.
- **GiST** — geometric/range types, nearest-neighbor; also the base for **tsvector** in some cases and for `EXCLUDE` constraints (interval overlap → preventing double-booked interview slots).
- **BRIN** — for *very large, sorted* tables (time-series): tiny index over ranges of blocks; huge space savings when the column correlates with physical order.
- **Partial indexes** — `WHERE status = 'open'` — index only the relevant subset (jobs that are open).
- **Expression indexes** — `LOWER(email)`, `(data->>'name')` for functional lookups.
- **Covering indexes** — `INCLUDE` columns → index-only scans (Q161).

**Match to questions:** JSONB containment → GIN; FTS → GIN/tsvector; range/interval conflicts → GiST EXCLUDE; big time-ordered tables → BRIN; hot subset → partial.

---

## Q560: What is a covering index? What is an index-only scan?

- **Covering index** = index that contains *all* columns a query needs — the query never touches the heap (table) at all.
```sql
CREATE INDEX idx_app_cand_status ON applications(candidate_id) INCLUDE (status, created_at);
-- SELECT status, created_at FROM applications WHERE candidate_id=?  → index-only scan
```
- **Index-only scan** — Postgres reads only the index pages (plus a visibility-map check to confirm rows are visible). Much faster than index + heap fetch.

**Keys:** `INCLUDE` for extra payload columns (keeps the searchable key small), visibility map must say "all visible" (vacuum keeps it updated, Q556).

**Use case:** your hottest queries — "list applications for a candidate with status" → covering index removes table fetches entirely.

---

## Q561: What is a dead-letter queue (DLQ) and how does it fit with Postgres?

**DLQ:** a queue (SQS/SQS-Redis) for messages that **failed permanently** after N retries — they're parked for manual inspection instead of retried forever or silently dropped (Q433).

```
queue → worker → retry(backoff) → after N failures → DLQ → alert → operator fixes → replay
```

**Common failure types:** poison messages (unparseable payload), schema drift, missing resource, transient-but-persistent external errors.

**Best practices:**
- **Idempotent replay** — when you fix the root cause, re-drive DLQ messages; handlers must tolerate duplicates (Q396).
- **Alert on DLQ depth** immediately — a growing DLQ is a real incident.
- Log the original message + error + retry count; provide a replay tool/script.
- **DLQ + DB of record:** the queue is for *work*, Postgres is the *source of truth* — if a job's final state lives in the DB, the DLQ only delays reconciliation.

---

## Q562: What is connection pooling? Why is it critical?

**Connection pool** = a cache of reusable DB connections. Opening a Postgres connection is expensive (TCP + auth + backend process ~ 20–50ms+); pools reuse them.

**Why critical:**
- Postgres handles each connection with a **backend process** (memory, ~5–10MB+). 10k clients → impossible; pool of ~100 connections is plenty.
- Under burst load, thousands of "connect per request" calls → connection storms, timeouts, OOM.

**For FastAPI/SQLAlchemy (Q118):**
- **SQLAlchemy pool** (in-process, `pool_size=10, max_overflow=20`).
- **PgBouncer** (external, shared across app instances) when you scale horizontally — **transaction pooling** mode for stateless apps.
- **Async:** use `asyncpg`'s pool or SQLAlchemy async pool.

**Symptoms of no pool:** spikes in connection counts, `sorry, too many clients already`, latency cliffs at load. Rule: one pool per app/service, sized to CPU not connections.

---

## Q563: How do you handle a hot row / hot partition?

**Hot row:** one row updated by many concurrent transactions → lock contention, all waiters serialize.

**Examples:** a global counter, an org's settings row, a "best match" row.

**Options:**
1. **Shard the logical state** — split the counter into N shards (`counter_0..counter_N`) and sum (`UPDATE counter_1 SET v=v+1` on random shard) — the classic trick (Q368).
2. **Buffer/write-behind** — batch increments in memory/Redis, flush to DB periodically (eventually consistent — fine for counts).
3. **Queue the writes** — serialize hot mutations through a single writer; throughput bounded by that writer.
4. **Reduce write frequency** — denormalize, only update on state change not on every read.

**Prevention:** profile `pg_stat_statements` for hot rows; avoid DB-side counters entirely (use Redis for volatile counts).

---

## Q564: How would you design the database for high write throughput?

1. **Batch writes** — multi-row inserts, `COPY` for bulk; batch queue flushes (100 rows/commit instead of 100 commits).
2. **Reduce per-row cost:** fewer indexes per write, no unnecessary triggers/constraints on the hot table, avoid `UPDATE`s (use append-only event tables + projection/materialized views).
3. **Unlogged/`UNLOGGED` tables** for ephemeral data (faster, no WAL durability) — only for disposable data.
4. **Partitioning** by time so writes touch small chunks (Q552).
5. **Separate concerns:** analytics writes to a different DB; the OLTP DB stays lean.
6. **Tune:** bigger `wal_buffers`, group commit, RAID/NVMe I/O, `synchronous_commit=off` where RPO loss is acceptable.
7. **Scale out:** read replicas won't help writes — consider sharding (Q566) only after the above are exhausted.

**Answer structure:** "eliminate wasteful work first (batches, fewer indexes, append-only), then tune WAL, then partition, then shard."

---

## Q565: What is CAP theorem? Where does Postgres/Redis fit?

**CAP:** a distributed system can guarantee only two of three under network partitions:
- **Consistency** — every read sees the latest write (or fails).
- **Availability** — every request gets a response (possibly stale).
- **Partition tolerance** — the system keeps working when nodes can't talk.

**In a partition, you choose C or A.** In practice: **P is non-negotiable** in a distributed system → you pick **CP** or **AP**.

**Examples:**
- **CP:** Postgres (primary/standby — the standby can't serve writes during a split brain), Zookeeper, etcd.
- **AP:** DynamoDB (default), Cassandra, Redis replication in many configs (the master accepts writes even if a replica can't be reached → may lose writes on failover).
- **Single-node** (a lone Postgres): technically CA (no partition), but real deployments are CP-ish.

**Interview answer:** "CAP says pick P always in the real world; Postgres is CP — I choose consistency and fail over; for volatile, loss-tolerant data (scores, counts) an AP store like Redis/DynamoDB fits. It's about matching the store to the tolerance, not a universal truth."

---

## Q566: What is sharding? When and how would you shard?

**Sharding** = splitting *rows* of one logical table across multiple physical databases by a **shard key** (`candidate_id % N` or hash → cluster).

**When you need it (only after: indexing, replicas, cache, partitioning are exhausted):**
- Single DB hits write-throughput or storage ceiling (can't scale writes with replicas).
- Data volume beyond one healthy Postgres (100s of GB–TB+).

**Costs (why it's last resort):**
- **Cross-shard queries** — joins, global aggregates, FTS across shards → app-level fan-out + merge.
- **Transactions** across shards — need distributed transactions or sagas (painful).
- **Rebalancing** — adding a shard means re-hashing data.
- Application becomes shard-aware (knows the routing rule).

**How:**
- **Consistent hashing** for even distribution + minimal moves on resize.
- Shard key must match your dominant access pattern (most queries filter by it).
- Hash-based (even) vs range-based (hot ranges).
- Each shard = its own Postgres (primary+replica); a router/middleware picks the shard.

**For the recruiter:** candidate-centric data shards cleanly by `candidate_id`; job/company data is smaller and can stay central. Only shard `messages`/`applications` if volume truly demands it.

---

## Q567: How do read replicas work? What are the pitfalls?

**Read replica** = an async (or sync) copy of the primary that serves **SELECT** traffic — offloads reads from the primary (Q440).

**How:** primary streams WAL → standby replays → mostly-read-only copy.

**Pitfalls:**
- **Replication lag** — a read may be stale. If a user's own write must be immediately visible (their application status), route those reads to the primary (or use `statement_timeout`-safe session-based routing: read-your-writes).
- **Not writable** — writes to a replica fail (or in some setups are proxied); app must route correctly.
- **Single primary = write bottleneck** — replicas don't help write scaling.
- **Failover** — promoting a replica during an outage: data written since the last synced WAL may be lost (unless sync standby, Q557).

**Pattern:** all writes + "read-your-own-write" reads → primary; profile/search/listing reads → replicas; tolerate seconds of staleness for scores/listings.

---

## Q568: What is WAL, and why is it important?

**WAL (Write-Ahead Log):** before changing a data page, Postgres writes the change to an append-only log. The page write happens lazily.

**Why:**
- **Durability:** at COMMIT, the WAL record is fsynced — if the DB crashes, replay the WAL to reconstruct committed state (no torn pages).
- **Performance:** WAL is sequential append (fast); random page writes happen later/batched.
- **Crash recovery:** startup replays WAL from the last checkpoint.
- **Replication:** standbys replay the same WAL (Q557).

**Key knobs:** `wal_level` (minimal/replica/logical), `synchronous_commit` (off/on/remote), `wal_buffers`, checkpoint tuning, `max_wal_size`. **Interviews like:** "WAL is the write-ahead log — durability first, replayable for recovery and replication."
