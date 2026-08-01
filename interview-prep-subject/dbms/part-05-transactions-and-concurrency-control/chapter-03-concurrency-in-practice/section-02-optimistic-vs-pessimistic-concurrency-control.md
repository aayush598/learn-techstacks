# Optimistic vs Pessimistic Concurrency Control

> **TL;DR**: Pessimistic concurrency (locks) assumes conflicts are frequent and pays to prevent them up front; optimistic concurrency (validation/versioning) assumes conflicts are rare and pays only when they happen — the right choice is decided by your conflict rate and the cost of a retry.

## 1. Why Does This Exist?
The DBMS must reconcile two facts: (1) concurrent transactions need to overlap for throughput, and (2) overlapping must never corrupt data. The pessimistic school says "resolve the conflict *before* it can happen — acquire a lock, wait, serialize." The optimistic school says "resolve the conflict *after* it happens — let everyone run, then detect and undo the loser." Both exist because neither strategy is universally best: under high contention, pessimistic locking prevents wasted work by blocking; under low contention, optimistic execution avoids the overhead of locking (lock manager, wait queues, deadlock detection) entirely and only pays when a real conflict materializes. Knowing *when to apply which* is a core system-design skill.

## 2. How Does It Work?
**Pessimistic**: acquire S/X locks before access (2PL, `SELECT ... FOR UPDATE`); conflicting transactions block (wait) on the lock manager; deadlocks detected/avoided; a transaction holding a lock is "guaranteed" no conflict with its peers. Reads under plain 2PL also take S-locks (readers block writers); MVCC-pessimistic hybrids let readers skip locks but still lock writes.
**Optimistic (Validation/OCC)**: run the transaction's reads/writes against live data with *no locks*; at commit, **validate** — check whether the read set and write set conflict with concurrently committed transactions (or, in version-based OCC, compare a version/update-timestamp column); if valid → write & commit; if invalid → **abort + retry**. App-level optimistic locking: `UPDATE ... SET v=v+1 WHERE id=? AND v=<read version>`; `ROW_COUNT()=0` means conflict → retry.
**MVCC as a third path**: snapshot reads (optimistic for readers — never block) + write-write locking (pessimistic for writers) — a hybrid that dominates OLTP.

## 3. When Is It Used?
- **Pessimistic**: money/inventory/booking where a conflict is *likely* or an abort is *unacceptable* (you already "sold" the seat); DDL; any read-modify-write where the read and write must be atomically linked; `SELECT FOR UPDATE` in transaction systems; distributed systems that want serializable semantics cheaply at low conflict (Spanner uses locks + commit-wait).
- **Optimistic**: read-mostly workloads with rare writes (a wiki page read a thousand times, edited once); app-level version-column concurrency (REST APIs, ORMs: Rails `optimistic: true`, JPA `@Version`, Django `F()`); in-memory/main-memory DBMS (validation is nearly free); distributed key-value stores (Redis `WATCH`).
- **MVCC**: nearly every OLTP engine's default — optimistic for readers, pessimistic for writers.

## 4. Why Wasn't Another Approach Chosen?
- *Pessimistic-only*: readers block writers and writers block readers (without MVCC), killing read-heavy workloads; deadlock/contention costs; a lock held during a long user interaction (network call inside transaction) is a guaranteed outage. Not the default for modern OLTP.
- *Optimistic-only*: under write contention, abort rates explode (a transaction re-executes after being killed), work is wasted, and long transactions lose repeatedly (starvation). Not viable for hot-row workloads.
- *MVCC for everything*: MVCC's snapshot is not serializable (write skew) and write-write conflicts still abort; pure MVCC can't fix phantom/write-skew without extra machinery (SSI/next-key locks). So engines combine mechanisms — the "one true approach" doesn't exist.
- *Timestamp ordering*: another abort-based (optimistic-leaning) alternative, but with the added complexity of timestamps and restart loops; less common as a primary mechanism.
- The industry conclusion: **hybrid** — pessimistic locks where blocking is cheap and correctness critical, optimistic validation/versioning where conflicts are rare, MVCC as the read path. That's why the answer to "optimistic or pessimistic?" is always "it depends — here's the conflict rate."

## 5. Intuition
**Optimistic** is like booking a **restaurant table by just showing up**: if there's no conflict (rare), you waltz in with zero friction; but if two groups show up for the same table, one gets sent away and has to come back (retry). **Pessimistic** is like **calling ahead and reserving**: you hold the table the whole evening (lock), others wait (block) — safe but everyone else is delayed even if you never use the table. Choose: if the restaurant is nearly empty (low conflict), showing up is better; if it's always packed (high conflict), reservations win. MVCC is the **"everyone gets their own copy of the menu"** trick: readers never compete, only people wanting to *change* the menu do.

## 6. Real-World Analogy
**Git collaboration**: pessimistic = a file lock — "I'm editing foo.py, everyone else waits." Safe but serial. Optimistic = everyone edits their own branch in parallel and merges (validate) at the end; if two people changed the same lines, one merge fails and must redo (retry). Git's model is optimistic, and it's why large teams can work in parallel — but merges conflict *sometimes*. A company that needs "nobody ever redoes work" (regulated financial edits) prefers locks; a company that wants maximum parallelism accepts occasional rebases.

## 7. Formal Definition
**Pessimistic concurrency control**: a transaction obtains locks (or otherwise secures access) *before* each operation, such that any conflicting operation by another transaction is prevented from interleaving (waits) — the conflict is resolved at access time. Examples: strict 2PL, `SELECT ... FOR UPDATE`, table/page/row locks.
**Optimistic concurrency control (validation-based)**: a transaction executes its read phase without locks; in the validation phase, the system verifies that for every item in the transaction's read set and write set, no transaction that committed *after* the transaction started (and overlaps it) has written items in the transaction's read set or write set; if the check fails, the transaction aborts and is restarted. (Kung & Robinson, 1981.)
**Version-based optimistic locking**: the row carries a version number (or updated-at timestamp); an update succeeds only if `WHERE version = <read value>`; a failed match (0 rows) signals a concurrent modification and the application retries.

## 8. Example
Inventory: `stock(id=1, qty=10, version=0)`. Two checkout transactions T1 and T2 each `SELECT qty, version WHERE id=1` → both read (10, v0).

**Optimistic (version column)**:
- T1: `UPDATE stock SET qty=8, version=1 WHERE id=1 AND version=0` → rowcount=1 ✓ commit.
- T2: `UPDATE stock SET qty=8, version=1 WHERE id=1 AND version=0` → rowcount=0 ✗ conflict → T2 must re-read (qty=8, v1) and retry (qty=6, v2). **Lost update prevented by validation.**

**Pessimistic (`SELECT FOR UPDATE`)**:
- T1: `SELECT qty WHERE id=1 FOR UPDATE` → X-lock on row 1.
- T2: same query → **blocks** (waits for T1's lock).
- T1 updates to 8, commits, releases lock → T2 proceeds, reads 8, updates to 6. Both succeed, serialized. No retry needed.

**MVCC snapshot (neither, for readers)**: a report transaction reading stock reads a snapshot; T1/T2's writes don't disturb it. Writers use pessimistic write locks.

## 9. Internal Working
**Pessimistic**:
1. `SELECT ... FOR UPDATE` / DML → lock manager grants X-lock (queue if held).
2. Operation proceeds; other transactions block; deadlock detection monitors the wait-for graph.
3. Commit/abort → release locks, wake waiters.
Cost: lock manager + waits + deadlock machinery; benefit: no aborts due to read/write conflict (only genuine deadlocks).

**Optimistic (validation)**:
1. Read phase: read data, track read-set and write-set (no locks).
2. Validate: at commit, compare against committed/overlapping transactions — per the OCC rule.
3. Write phase: apply writes (usually in a critical section or with a final lock on write-set).
4. On invalid → abort, release, retry (maybe exponential backoff).

**Optimistic (version column)**:
1. App reads `(data, version)`.
2. App computes new data; issues conditional UPDATE (`WHERE version = ?`).
3. rowcount 1 → success; rowcount 0 → conflict: re-read, recompute, retry (bounded attempts).
4. Under a DB engine, the conditional UPDATE still takes the row's write lock (pessimistic part) — the "optimism" is about *not holding locks during the read/compute*.

## 10. Time Complexity
- Pessimistic: per-access lock grant O(1); blocking time = hold time of others (the real cost, variable); deadlock detection amortized.
- Optimistic validation: O(reads+writes) per commit to check overlaps (with efficient in-memory conflict sets, near O(1) per commit in main-memory systems).
- Version-column OCC: O(1) per UPDATE (conditional WHERE uses the PK index).
- Retry cost: full transaction re-execution — O(work) × attempts. This is the dominant term under contention.
- Overall: pessimistic wins on throughput when conflict rate × transaction cost is high; optimistic wins when conflict rate is low.

## 11. Advantages
- **Pessimistic**: no lost work from read/write conflicts (except deadlock victims); predictable latency (you wait, you don't redo); correct for money/inventory; deadlock retries are rare.
- **Optimistic**: zero locking overhead in the common (non-conflicting) case; readers and writers of different data never interfere; no lock manager/deadlock machinery; scales to main-memory and distributed settings where locking coordination is expensive; simple to implement at the app layer (version columns).
- **MVCC hybrid**: best of both — lock-free reads, guarded writes.

## 12. Disadvantages
- **Pessimistic**: lock contention (hot rows serialize), deadlock handling, convoying; long-held locks (network calls, user waits) block others — a production footgun; needs lock manager resources.
- **Optimistic**: aborts waste all completed work under contention; retry storms; long transactions can starve (always conflict at validation); apps must implement retry logic correctly; read-modify-write still has a gap between read and validate (a writer could slip in between).
- **Version-column OCC**: requires schema discipline (version column), apps must re-read on conflict, and it can't protect against *unversioned* writes.

## 13. Interview Questions
1. **Q: What is the difference between optimistic and pessimistic concurrency?** A: Pessimistic: prevent conflicts before they happen by locking (transactions wait). Optimistic: let transactions run free, then validate at commit and abort/retry on conflict. Pessimistic pays up-front for safety; optimistic pays only on actual conflict.
2. **Q: When would you choose pessimistic over optimistic?** A: When conflicts are *likely* (hot rows: inventory, counters, account balances) or when an abort is expensive/unacceptable (you've already "held" a resource). Pessimistic gives predictable behavior and no wasted work.
3. **Q: When would you choose optimistic?** A: When conflicts are *rare* (read-mostly data, e.g., a wiki article, user profiles) or the system is distributed/main-memory where locking coordination costs more than a rare retry. Optimistic scales better when the conflict rate is low.
4. **Q: How does app-level optimistic locking work?** A: Add a `version` column; read `(data, version)`; update with `SET version=version+1, ... WHERE id=? AND version=?`; if `ROW_COUNT()=0`, someone modified it — re-read and retry. This prevents lost updates without DB-level locks during the read.
5. **Q: TRICKY: Is `SELECT ... FOR UPDATE` optimistic or pessimistic?** A: Pessimistic — it acquires an exclusive lock *before* the operation and holds it until commit. It's the pessimistic primitive; "optimistic" means *no* locks held during the transaction's read/compute phase.
6. **Q: What is the validation phase in OCC?** A: At commit, check whether the transaction's read set and write set overlap (read/write or write/write) with any transaction that committed after it started (and is concurrent). If a conflict exists → abort; else → write and commit. (Kung–Robinson.)
7. **Q: Why is MVCC sometimes called "optimistic"?** A: For *readers* it's optimistic — they take no locks and read a snapshot, never blocking. But writers are pessimistic (write-write conflicts lock/abort). So MVCC is a hybrid: optimistic reads + pessimistic writes.
8. **Q: PRODUCTION: Design an inventory decrement — optimistic or pessimistic?** A: Use `UPDATE inventory SET qty = qty - 1 WHERE id=? AND qty >= 1` (atomic conditional update) or `SELECT ... FOR UPDATE`. Both are pessimistic in the critical section; the first is atomic and lock-light. Optimistic read-then-write risks overselling if the gap isn't protected — a classic bug.
9. **Q: What are the failure modes of optimistic locking?** A: High abort/retry rates under contention; retry storms (all losers retry simultaneously and re-conflict); starvation of long transactions; and the read-modify-write gap (two readers both pass validation before either writes — mitigated by locking the write or by the conditional UPDATE being atomic).
10. **Q: TRICKY: Does optimistic locking require transactions?** A: No — version-column OCC works per-row even in autocommit mode (each conditional UPDATE is atomic on its own). But cross-row invariants still need a transaction; OCC-at-app-layer protects one row at a time.
11. **Q: What is a "retry storm"?** A: When many optimistic transactions fail at once (e.g., a write burst) and all retry immediately, colliding again — cascading retries that can collapse throughput. Mitigations: exponential backoff, jitter, and choosing pessimistic control when the storm probability is high.
12. **Q: How does Redis `WATCH` implement optimistic concurrency?** A: `WATCH key` marks keys; `MULTI`/`EXEC` runs commands; if any watched key changed between WATCH and EXEC, EXEC aborts (returns null) — the app retries. It's app-level OCC: no locks, detect-at-execute, retry on conflict.
13. **Q: PRODUCTION: Which would you use for a "seats booking" service?** A: Pessimistic (or atomic conditional update) — because the conflict is almost guaranteed (many users racing for the same seats) and an abort means losing a customer. Lock the seat briefly (`FOR UPDATE`) and keep the transaction tiny. Optimistic would cause endless retries.
14. **Q: How do ORMs expose optimistic locking?** A: Rails `optimistic: true` (adds `lock_version`); JPA `@Version`; Django `F()` expressions; Prisma `@@unique`+version patterns. The ORM issues the conditional UPDATE and raises a conflict exception the app catches → retry.
15. **Q: TRICKY: Can optimistic concurrency be used for a "counter" with 1M increments/sec?** A: No — a single counter row is the *highest* conflict workload possible; optimistic retries would thrash. Use atomic DB increments (`UPDATE ... SET n=n+1` — pessimistic but lock-light), a Redis INCR, or shard the counter. This is the canonical "pessimistic wins at the extreme" answer.
16. **Q: What does "deadlock-free by construction" mean for optimistic systems?** A: Since no transaction *waits* on another (no locks), circular wait can't form — OCC never deadlocks. Its failure mode is abort-and-retry instead. That's a real advantage for distributed systems where deadlock detection across nodes is hard.

## 14. Follow-Up Questions
1. **Q: How do you measure conflict rate to choose a strategy?** A: Instrument the fraction of writes that touch rows also touched by other in-flight writes (or count optimistic-retry rate in staging); if retries > a few %, pessimistic is cheaper. Also consider abort *cost* (work since start) — big transactions favor pessimism.
2. **Q: Can you combine both?** A: Yes — "pessimistic for hot rows, optimistic for cold rows" (or per-transaction: the hot leg uses `FOR UPDATE`, the long tail uses version checks). Engines do this: InnoDB locks writes (pessimistic) while serving snapshot reads (optimistic).
3. **Q: What is the relationship to isolation levels?** A: Optimistic systems naturally implement READ COMMITTED (validate against commits) and can implement SERIALIZABLE via SSI (validate serialization order); pessimistic systems implement SERIALIZABLE via 2PL. The level is a contract; the strategy is a mechanism.

## 15. Coding Example
```python
# App-level optimistic locking (version column) with retry
def withdraw(conn, account_id, amount, max_retries=5):
    for attempt in range(max_retries):
        row = conn.execute(
            "SELECT balance, version FROM accounts WHERE id=%s", (account_id,)).fetchone()
        if row is None: raise NotFound()
        balance, version = row
        if balance < amount: raise InsufficientFunds()
        n = conn.execute(
            "UPDATE accounts SET balance=%s, version=version+1 "
            "WHERE id=%s AND version=%s",
            (balance - amount, account_id, version))
        if n.rowcount == 1:
            return
        # conflict → retry with backoff
        time.sleep(0.05 * attempt)
    raise ConcurrencyError("retry budget exhausted")
```
```sql
-- Pessimistic variant — one atomic conditional statement (pessimistic on write)
BEGIN;
UPDATE inventory
   SET qty = qty - 1
 WHERE sku = 'A100' AND qty >= 1;      -- atomic decrement, condition enforces invariant
SELECT ROW_COUNT();                    -- 0 rows → out of stock → ROLLBACK
COMMIT;
```
```python
# Redis WATCH — optimistic in a cache
import redis
r = redis.Redis()
while True:
    r.watch("stock:A100")                       # begin optimistic watch
    qty = int(r.get("stock:A100") or 0)
    if qty < 1:
        raise OutOfStock()
    pipe = r.pipeline(transaction=True)         # MULTI
    pipe.decr("stock:A100")
    try:
        pipe.execute()                          # EXEC — aborts if watched key changed
        break
    except redis.WatchError:
        continue                                # retry on conflict
```

## 16. Industry Usage
- **Postgres/MySQL**: MVCC = optimistic reads + pessimistic writes; `SELECT FOR UPDATE` exposes the pessimistic path to apps; version-column OCC is an app pattern on top.
- **Rails/JPA/Django** ORMs: optimistic locking built-in (version columns) — most web CRUD apps rely on it.
- **Spanner**: pessimistic locking (Paxos-group locks) + commit-wait timestamps — chooses pessimism because geo-distributed retries are catastrophic; achieves serializable with predictable behavior.
- **CockroachDB**: MVCC + serializable; uses optimistic-style retries at high contention with a "transaction retry error" the client must handle — a hybrid leaning optimistic for reads.
- **Redis**: `WATCH`/`MULTI`/`EXEC` = optimistic; `INCR`/`DECR` = atomic (lock-free) — a microcosm of the choice.
- **Main-memory DBMS** (VoltDB, Hekaton, foundational stores like FoundationDB): validation/optimistic and deterministic execution — where retries are cheap and locking coordination dominates.

## 17. References
- Kung & Robinson, "On Optimistic Methods for Concurrency Control", ACM TODS 1981 — the OCC paper.
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 16.5 (validation-based protocols).
- Elmasri & Navathe, Ch. 21.
- PostgreSQL docs, "Data Consistency": https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK
- MySQL docs, locking reads: https://dev.mysql.com/doc/refman/8.0/en/innodb-locking-reads.html
- Rails docs, optimistic locking: https://edgeapi.rubyonrails.org/classes/ActiveRecord/Locking/Optimistic.html
- Redis docs, transactions: https://redis.io/docs/latest/develop/interact/transactions/

## 18. Cheat Sheet
- Pessimistic = lock first (block/queue); Optimistic = run first, validate at commit (abort/retry).
- Choose pessimistic when conflicts likely or abort expensive; optimistic when conflicts rare.
- App-level OCC: version column + conditional UPDATE + rowcount check + retry loop.
- MVCC = optimistic readers + pessimistic writers (the hybrid default).
- `SELECT FOR UPDATE` is pessimistic; Redis `WATCH` is optimistic.
- OCC is deadlock-free but can starve/retry-storm.
- Hot counter (single row, 1M TPS) → pessimistic/atomic, never optimistic.
- Backoff+jitter on retries to avoid storms.

## 19. Quiz
1. Pessimistic concurrency resolves conflicts: a) at commit b) before access (locking) c) after abort d) never → **b**
2. Optimistic concurrency resolves conflicts: a) by locking b) at validation/commit c) by timestamp d) never → **b**
3. `SELECT ... FOR UPDATE` is: a) optimistic b) pessimistic c) neither d) version-based → **b**
4. OCC is best when: a) conflicts frequent b) conflicts rare c) always d) never → **b**
5. A version-column conflict is detected by: a) rowcount 0 b) deadlock c) timeout d) exception → **a**
6. MVCC readers are: a) pessimistic b) optimistic (snapshot, no lock) c) blocked d) versioned → **b**
7. OCC is deadlock-free because: a) it uses timestamps b) nobody waits c) single-threaded d) no writes → **b**
8. A retry storm is a risk of: a) pessimistic b) optimistic c) both d) MVCC only → **b**

## 20. Flashcards
- **Q: Pessimistic vs optimistic?** → **A:** Lock-before (block) vs validate-at-commit (abort+retry).
- **Q: When to choose pessimistic?** → **A:** High conflict rate or high abort cost (hot rows, money, seats).
- **Q: When to choose optimistic?** → **A:** Low conflict rate (read-mostly) or cheap retries (in-memory/distributed).
- **Q: How does app-level optimistic locking work?** → **A:** version column; conditional UPDATE with WHERE version=?; rowcount 0 → retry.
- **Q: Is SELECT FOR UPDATE optimistic?** → **A:** No — pessimistic; it takes an X-lock up front.
- **Q: MVCC = ?** → **A:** Optimistic reads (snapshots) + pessimistic writes (write-write locks).
- **Q: OCC advantage/disadvantage?** → **A:** No locking overhead / no deadlock, but aborts+retries and starvation risk.
- **Q: Counter at 1M TPS?** → **A:** Atomic/pessimistic (INCR or conditional UPDATE); optimistic would thrash.

## 21. Revision
Optimistic vs pessimistic: pessimistic locks up front (2PL, `FOR UPDATE`) — safe, predictable, but contention-prone and deadlock-prone; optimistic validates at commit (Kung–Robinson, version columns) — zero overhead when conflicts are rare, aborts+retries when not, deadlock-free but retry-storm-prone. Rule: conflict rate × abort cost decides; MVCC hybridizes (optimistic readers + pessimistic writers). Production patterns: atomic conditional UPDATE (`qty>=1`), version column with retry loop, Redis WATCH/MULTI. Interview: "which for a booking system?" → pessimistic (conflicts guaranteed); "for a profile editor?" → optimistic (conflicts rare).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Optimistic vs pessimistic concurrency?" | 1, 2, 13 |
| "When to choose each?" | 4, 13 |
| "How does app-level optimistic locking work?" | 2, 9, 13 |
| "Is SELECT FOR UPDATE optimistic?" | 13, 18 |
| "What is a retry storm?" | 13, 14 |
| "How does Redis WATCH implement OCC?" | 13, 15, 16 |
| "Design inventory decrement?" | 13, 15 |
| "Counter at 1M TPS — which?" | 13, 18 |
