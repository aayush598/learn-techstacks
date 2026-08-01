# Locking Protocols and Two-Phase Locking

> **TL;DR**: Locking protocols make serializability a *mechanical* guarantee — every transaction must acquire locks before touching data — and Two-Phase Locking (grow: acquire, shrink: release) is the canonical rule that provably produces only conflict-serializable schedules.

## 1. Why Does This Exist?
Serializability (Section 03, Chapter 01) defines *what* correct concurrency is, but it's not something you can test on every schedule at runtime (view-serializability is NP-complete, and even conflict-testing requires knowing the future). Locking protocols exist to *generate* only safe schedules by construction: if every transaction obeys a small, local rule (get a lock before each access, release it when done), then any interleaving the scheduler produces is provably serializable. That turns an undecidable-looking global property into a per-transaction rule a lock manager can enforce with an O(1) check per operation. Every production DBMS is a locking system at heart (with MVCC layered on top for readers).

## 2. How Does It Work?
Two lock modes: **shared (S)** — for reads, multiple readers allowed; **exclusive (X)** — for writes, one holder only. A lock manager maintains a table of held locks; a transaction requesting an incompatible lock blocks (queues) until it's granted. **Two-phase locking (2PL)**: the transaction executes in two phases — a **growing phase** during which it may *only acquire* locks, and a **shrinking phase** during which it may *only release* locks (and never acquire new ones). If all transactions obey 2PL, any produced schedule is conflict serializable. Variants: **strict 2PL** — hold all locks until commit/abort (no release in the middle; used by real engines) — and **rigorous 2PL** — all locks released at the very end (used in distributed settings).

## 3. When Is It Used?
- As the *write path* in essentially every relational DBMS (Postgres, MySQL InnoDB, Oracle, SQL Server all acquire X-locks on rows being updated).
- For `SELECT ... FOR UPDATE` / `LOCK IN SHARE MODE` — explicit 2PL on demand by the application.
- In distributed transaction coordinators (2PL generalizes; Spanner acquires locks via Paxos groups).
- In interviews: "prove 2PL gives conflict serializability", "what's the difference between growing and shrinking phases", "strict 2PL vs rigorous 2PL", "why do we hold locks until commit".

## 4. Why Wasn't Another Approach Chosen?
- *No locking (validate at the end, optimistic)*: works but risks long transactions being aborted repeatedly under contention — locking "wins" by preventing conflicts up front.
- *Timestamp ordering*: eliminates waiting (no lock queue) but aborts transactions that arrive out of order — high abort rate under contention; locking's blocking is gentler.
- *Full serial execution (one global lock)*: safe but zero concurrency — that's the extreme point; 2PL is the minimal locking that still allows concurrency.
- *Acquiring all locks up front (conservative/static 2PL)*: avoids deadlocks by predeclaring the lock set, but you rarely know in advance what you'll touch, and holding everything forever kills concurrency — rejected for dynamic workloads.
- *Single lock mode (only exclusive)*: simplest, but every read blocks every write and every read — shared locks exist precisely to let concurrent readers coexist.
- *Non-strict 2PL (release early)*: more concurrency (shorter shrinking overlaps) but creates non-recoverable schedules — a committed transaction might have read data from a later-aborted one. Strict 2PL is the production compromise.

## 5. Intuition
2PL is the **"no new requests once you start returning things"** rule at a library counter. During the growing phase, you can only *take* books (acquire locks); during the shrinking phase, you can only *return* them. You may never take a book after you've returned one. Why does this guarantee safety? Because once you release (return) a lock, another transaction can read/write that data and you can no longer be ordered "before" it on that item — but if you then grab a *different* item, the orderings become inconsistent. The two-phase rule forces all your "before/after" claims to line up in one direction — no cycles, hence serializable.

## 6. Real-World Analogy
A **hotel key-card system**: to enter room A you must "acquire" its key; you hold keys for all rooms you're working in. The rule: once you return a single key, you're never allowed to take another. If every maid follows this, no two maids ever reorder each other's room visits in contradictory ways — the sequence of visits becomes as safe as "one maid at a time." If a maid *did* take a key after returning one, two maids could each "happen before" the other in a circle — the maid-equivalent of a non-serializable schedule.

## 7. Formal Definition
Let T be a transaction, L(T) the set of locks (S or X on data items). **Two-phase locking protocol**: (1) before reading item Q, T must hold a shared or exclusive lock on Q; before writing Q, T must hold an exclusive lock on Q; (2) after T releases any lock, it may never acquire another lock. The schedule is split into a **growing phase** (only acquire) and **shrinking phase** (only release). **Theorem**: if every transaction in a schedule obeys the 2PL protocol, then the schedule is conflict serializable. **Strict 2PL**: a transaction holds all its exclusive locks until it commits or aborts (releases S-locks early only if done). **Rigorous 2PL**: holds *all* locks (S and X) until commit/abort. Strict 2PL additionally guarantees the schedule is recoverable (a transaction only reads committed data — no cascading aborts).

## 8. Example
T1: `read(A) write(A) read(B) write(B)`; T2: `read(A) read(B) write(B)`.
Under 2PL:
- T1 acquires X(A), T2 requests S(A) → **blocks** (X conflicts with S).
- T1 completes on A, acquires X(B), T2 still blocked.
- T1 commits → releases X(A), X(B) → T2 acquires S(A), reads, requests S(B)/X(B) → granted.
- T2 completes, releases.
Schedule produced is serial (T1 then T2) — conflict serializable trivially. If T2 had run first on B, ordering would enforce T2-before-T1 on B and T1-before-T2 on A → a cycle → 2PL *prevents* that by blocking the later requester. The lock manager is what converts the potential cycle into a block-and-wait.

## 9. Internal Working
1. Each operation arrives at the scheduler: `read(Q)` requires S or X; `write(Q)` requires X.
2. The **lock manager** checks a hash table keyed by data item: does the request conflict (compatibility matrix: S/S ✓, S/X ✗, X/S ✗, X/X ✗)?
3. No conflict → grant, record (transaction, item, mode), return immediately.
4. Conflict → insert the request into the item's wait queue; the transaction's status becomes "blocked"; when the holder commits/aborts, the manager wakes waiting transactions in FIFO (or priority) order and grants.
5. On commit/abort (strict 2PL): release **all** locks held by the transaction; wake waiters; the released versions are then visible to others (in MVCC engines the visibility is version-based, but the *lock release* is the same trigger).
6. The lock manager also tracks ownership for deadlock detection (Chapter 05) and can deny/upgrade requests (e.g., lock upgrade S→X must wait).

## 10. Time Complexity
- Lock grant/check: O(1) expected with a hash map keyed by (item → lock list).
- Lock release: O(#locks held) at commit/abort.
- Blocking wait: unbounded in the worst case (that's the concurrency cost), bounded by transaction duration.
- The serializability guarantee is O(1) per operation — 2PL's beauty is the local rule has constant cost while guaranteeing a global property.

## 11. Advantages
- **Provable correctness**: 2PL ⇒ conflict serializable (the classic theorem).
- **Low abort rate** compared to optimistic/timestamp approaches under contention: conflicts are handled by waiting, not killing work.
- **Simple, robust**: no clocks, no global version bookkeeping; the lock table is the only shared state.
- **Strict 2PL gives recoverability for free**, which is what recovery (Part 06) requires.

## 12. Disadvantages
- **Deadlock possible** (2PL does NOT prevent it — two transactions can each hold a lock the other wants).
- **Lock contention / convoying**: hot rows serialize; a slow transaction holds locks and starves others (a single "counter" row becomes a bottleneck).
- **Blocking readers**: plain 2PL makes readers wait for writers (the reason MVCC was invented).
- **Overhead**: lock table bookkeeping, queue management; fine-grained locking needs many lock entries.
- **Lock upgrade deadlocks** (T1 upgrades S→X while T2 does the same) require care.

## 13. Interview Questions
1. **Q: What is two-phase locking?** A: A concurrency control protocol where each transaction acquires all locks it needs before releasing any — split into a growing phase (only acquire) and a shrinking phase (only release). It guarantees conflict serializability.
2. **Q: Why does 2PL guarantee serializability?** A: If every pair of conflicting operations is ordered by the lock acquisition order, and 2PL forces each transaction's "acquire-before-release" to be monotonic, the conflicting orderings can't form a cycle — so the precedence graph is acyclic. The formal proof: assume a cycle exists → some transaction T releases a lock before another acquires it, but the cycle requires acquiring a lock after releasing — contradiction with the two-phase rule.
3. **Q: What's the difference between growing and shrinking phases?** A: Growing = only acquire locks (before first release); shrinking = only release locks (after first release). The point of no return is the *first unlock* — after that, no new locks.
4. **Q: What is strict 2PL?** A: A transaction holds all its exclusive (write) locks until it commits or aborts — it doesn't release mid-transaction. It makes the schedule recoverable (no reading aborted data) and is what real DBMSes implement.
5. **Q: What is the difference between strict and rigorous 2PL?** A: Strict = hold X-locks until commit/abort (S-locks can be released early). Rigorous = hold *all* locks (S and X) until commit/abort. Rigorous is used where stronger guarantees are needed (e.g., distributed commit).
6. **Q: TRICKY: Does 2PL prevent deadlock?** A: No. 2PL prevents non-serializable schedules, not deadlocks. Two transactions can each hold a lock the other wants while waiting for a lock the other holds — circular wait. Deadlock is handled separately (Chapter 05).
7. **Q: What is a lock compatibility matrix?** A: A table showing which lock modes can be held together on the same item: S/S compatible, S/X incompatible, X/S incompatible, X/X incompatible. Writes need X; multiple reads can share S.
8. **Q: Why do we need shared locks at all?** A: So multiple readers can access data concurrently. Without S-locks (only X), every read would block every other read — serializing reads unnecessarily. S-locks preserve read concurrency while still excluding writers.
9. **Q: PRACTICAL: How does `SELECT ... FOR UPDATE` relate to 2PL?** A: It makes a `SELECT` acquire an exclusive lock (rather than MVCC's lock-free read), letting the application get the *write lock in the read phase*. The read-modify-write cycle then holds the X-lock the whole time — strict 2PL from the application's perspective.
10. **Q: What happens when a transaction's lock request is denied?** A: It blocks (waits) in the item's queue; when the holder releases, the waiter is granted. If it never gets granted (deadlock or starvation), the DBMS may abort it — a blocked transaction is a scheduling state, not an error.
11. **Q: TRICKY: Why is non-strict 2PL dangerous?** A: Releasing locks before commit lets another transaction read your uncommitted data (non-recoverable schedule) — if you abort, that reader's committed result is invalid (it read aborted data). Strict 2PL (release at commit) avoids cascading aborts and recoverability violations.
12. **Q: What is lock upgrading and its hazard?** A: A transaction holding S(A) requests X(A) — an upgrade. Two transactions both holding S(A) both requesting upgrade can deadlock (each waits for the other to release S). Deadlock detection handles it, or the DBMS grants upgrades only when no other S-holders exist.
13. **Q: PRODUCTION: Why does a "hot row" (e.g., a global counter) cause serialization under 2PL?** A: Every increment takes X-lock on the same row; only one transaction holds it at a time, so increments serialize — throughput collapses at high concurrency. Fixes: atomic counters (Redis INCR), sharding the counter, or batched increments — this is a classic production bottleneck discussion.
14. **Q: How does 2PL interact with MVCC?** A: MVCC engines (Postgres, InnoDB) let *readers* skip locking entirely (they read old versions), but *writers* still use X-locks — write-write conflicts are 2PL-like (first writer wins, second blocks or aborts). So modern engines = MVCC for reads + 2PL for writes.
15. **Q: What is the difference between 2PL and serializability?** A: Serializability is the *property* (a schedule is serializable); 2PL is a *protocol* (a rule transactions follow) that guarantees the property. 2PL ⇒ conflict serializable, but not all serializable schedules are producible under 2PL — 2PL is a sufficient, not necessary, condition.
16. **Q: TRICKY: Can 2PL produce a schedule that is serializable but NOT in the transaction's intended order?** A: Yes — 2PL guarantees *some* serial order exists (the acyclic graph's topo order), not a specific one. Applications needing a particular order (e.g., "T1 must see T2's result") must use explicit synchronization, not just 2PL.

## 14. Follow-Up Questions
1. **Q: How is a lock table implemented in a real DBMS?** A: A hash table mapping (database_id, table_id, page_id/row_id) → lock struct with mode, owner list, and wait queue. Postgres stores locks in shared memory (`LOCKTAG`); InnoDB has a lock system with per-record locks.
2. **Q: What is lock convoying?** A: A pattern where many transactions queue on the same lock and process serially, so even after the original holder leaves, the queue drains one-by-one — throughput collapses. It's a starvation/perf hazard of fine-grained locking.
3. **Q: What's the difference between an S-lock on read and a snapshot read?** A: An S-lock *blocks* writers during the read; a snapshot read never blocks — it reads a historical version. That's precisely why MVCC reads are preferred for OLTP.

## 15. Coding Example
```python
# Minimal 2PL lock manager simulation
import threading
from collections import defaultdict

class LockManager:
    def __init__(self):
        self.mutex = threading.Lock()
        self.held = defaultdict(dict)   # item -> {txid: mode}
        self.cond = defaultdict(threading.Condition)

    def _compatible(self, mode1, mode2):
        return not (mode1 == 'X' or mode2 == 'X')  # S/S ok; X conflicts with all

    def acquire(self, txid, item, mode):
        with self.cond[item]:
            while True:
                holders = self.held[item]
                if all(self._compatible(m, mode) for m in holders.values()):
                    holders[txid] = mode          # grant (growing phase)
                    return True
                self.cond[item].wait()            # block — this is the wait queue

    def release_all(self, txid):
        for item, holders in self.held.items():
            if txid in holders:
                del holders[txid]
                with self.cond[item]:
                    self.cond[item].notify_all()  # wake waiters (shrinking phase)
```
```sql
-- Real strict-2PL write pattern
BEGIN;
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;   -- acquire X-lock (growing)
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;                                                 -- release all locks here (strict)
```

## 16. Industry Usage
- **PostgreSQL**: locks per tuple via a shared-memory lock manager; `SELECT FOR UPDATE` uses `LOCKTAG`. Readers don't lock (MVCC); writers serialize via 2PL-style row X-locks.
- **MySQL InnoDB**: record locks + gap locks + next-key locks implement 2PL over index records; upgrade and compatibility tables documented in the InnoDB docs.
- **SQL Server**: classic lock manager with S/X locks, lock escalation (row→page→table), and `WITH (UPDLOCK, HOLDLOCK)` hints exposing 2PL to apps.
- **Oracle**: undo-based MVCC + DML locks; `SELECT ... FOR UPDATE` obtains X locks.
- **Spanner**: distributed 2PL — read-write transactions acquire locks on Paxos groups; "TrueTime" timestamps order commits. Shows 2PL scales to geo-distributed when combined with a commit protocol.

## 17. References
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 16.1–16.2 (lock-based protocols, 2PL, strict/rigorous variants).
- Elmasri & Navathe, *Fundamentals of Database Systems*, Ch. 21.
- PostgreSQL docs, "Locking": https://www.postgresql.org/docs/current/locking-indexes.html and https://www.postgresql.org/docs/current/explicit-locking.html
- MySQL 8.0 InnoDB locking: https://dev.mysql.com/doc/refman/8.0/en/innodb-locking.html
- Gray, Lorie, Putzolu, Traiger, "Granularity of Locks and Degrees of Consistency in a Shared Data Base" (1975) — foundational locking paper.
- Bernstein, Hadzilacos, Goodman, *Concurrency Control and Recovery in Database Systems* (1987).

## 18. Cheat Sheet
- Locks: S (share, reads), X (exclusive, writes); S/S compatible, X conflicts with all.
- 2PL: growing phase (acquire only) → first release → shrinking phase (release only). First unlock = point of no return.
- Theorem: 2PL ⇒ conflict serializable.
- Strict 2PL: hold X-locks to commit → recoverable + no cascading aborts. This is production reality.
- Rigorous 2PL: hold all locks to commit.
- 2PL does NOT prevent deadlock; deadlock is handled by detection/prevention (Ch. 05).
- `SELECT FOR UPDATE` = app-level strict 2PL on the read.
- MVCC = lock-free reads + 2PL-style writes.

## 19. Quiz
1. Which phase allows only acquiring locks? a) shrinking b) growing c) both d) neither → **b**
2. Under strict 2PL, when are X-locks released? a) when no longer needed b) at commit/abort c) at first unlock d) never → **b**
3. Lock compatibility: S and S on same item → a) compatible b) conflict c) block d) upgrade → **a**
4. 2PL guarantees: a) no deadlocks b) conflict serializability c) view serializability d) no starvation → **b**
5. A transaction that releases a lock then requests another violates: a) ACID b) 2PL c) WAL d) nothing → **b**
6. Releasing locks before commit risks: a) lost updates b) non-recoverable schedules/cascading aborts c) phantoms d) all → **b**
7. `SELECT ... FOR UPDATE` acquires: a) S-lock b) X-lock c) no lock d) gap lock → **b**
8. Which is NOT a 2PL variant? a) strict b) rigorous c) conservative d) optimistic → **d** (optimistic is validation, Chapter 02 S4)

## 20. Flashcards
- **Q: What are the two lock modes?** → **A:** Shared (S, reads) and Exclusive (X, writes); S/S compatible, X conflicts with all.
- **Q: What is 2PL?** → **A:** Acquire all locks in a growing phase, then only release in a shrinking phase; never acquire after first release.
- **Q: What does 2PL guarantee?** → **A:** Conflict serializability (a sufficient, not necessary, condition).
- **Q: Strict vs rigorous 2PL.** → **A:** Strict holds X-locks till commit; rigorous holds all locks till commit.
- **Q: Does 2PL prevent deadlock?** → **A:** No — that's a separate mechanism (Ch. 05).
- **Q: Why do MVCC engines use locks on writes?** → **A:** To serialize write-write conflicts (first writer wins); readers skip locking via versions.
- **Q: What is the point of no return in 2PL?** → **A:** The first unlock — no new acquisitions after it.

## 21. Revision
2PL: every read/write needs S/X lock; growing phase (acquire) → first release → shrinking phase (release only). Guarantees conflict serializable (acyclic precedence graph). Strict 2PL (release X at commit) gives recoverability — what engines run. 2PL ≠ deadlock-free; hot rows serialize; readers blocked in pure 2PL (hence MVCC). Interview answers: "2PL is the protocol that turns serializability from a property into a mechanism", "strict variant = production standard", "no, it doesn't stop deadlocks", "S/S ok, X fights everyone".

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Explain two-phase locking." | 2, 7 |
| "Why does 2PL give serializability?" | 5, 7, 13 |
| "Strict vs rigorous 2PL?" | 7, 13 |
| "Does 2PL prevent deadlocks?" | 13, 18 |
| "What is a lock compatibility matrix?" | 7, 13 |
| "What does `SELECT FOR UPDATE` do?" | 13, 15 |
| "Why is non-strict 2PL unsafe?" | 13, 14 |
| "Hot-row bottleneck under 2PL?" | 13, 16 |
