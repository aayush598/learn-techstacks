# Timestamp-Based Protocols

> **TL;DR**: Timestamp-based concurrency control orders transactions by their "birth time" and resolves every conflict by aborting the younger transaction — achieving serializability by *ordering* instead of by *waiting* on locks.

## 1. Why Does This Exist?
2PL achieves serializability by making conflicting transactions *wait* — but waiting creates lock queues, contention, convoying, and deadlocks. Timestamp-based protocols offer a different mechanism: instead of blocking a transaction when it conflicts, the DBMS *decides immediately* who wins based on a fixed global ordering (the timestamps), and aborts the loser. This eliminates waiting entirely (a transaction either proceeds or is killed and restarted) — which makes it attractive for distributed and main-memory systems where blocking coordination is the bottleneck. It also produces deadlock-free execution *by construction*: since winners are decided by timestamps, no circular wait can form.

## 2. How Does It Work?
Each transaction gets a unique timestamp TS(T) (e.g., from a counter or system clock) — older transactions have smaller timestamps. Each data item Q tracks `W-timestamp(Q)` (last writer) and `R-timestamp(Q)` (last reader). **Basic Timestamp Ordering (TO)**:
- `read(Q)`: if `TS(T) < W-timestamp(Q)`, a *newer* transaction already wrote Q — the read would be "too old" (read a value that should have been seen earlier) → **abort T** (and restart with a new timestamp). Otherwise read, and set `R-timestamp(Q) = max(R-timestamp(Q), TS(T))`.
- `write(Q)`: if `TS(T) < R-timestamp(Q)`, a newer transaction already read Q → abort (its read must see a newer write). If `TS(T) < W-timestamp(Q)`, a newer write already happened → abort. Otherwise write and set `W-timestamp(Q) = TS(T)`.
**Thomas Write Rule**: *relax* the last case — if `TS(T) < W-timestamp(Q)`, ignore (reject) the write without aborting, because the newer write will be the one in the final state; this yields schedules that are view-serializable (not always conflict-serializable) and reduces aborts.

## 3. When Is It Used?
- In **distributed database** designs where a global lock manager is the bottleneck (timestamp ordering is decentralized — each node can decide locally given timestamps).
- In **main-memory / high-throughput** engines that avoid locking overhead (some in-memory systems use optimistic/timestamp schemes).
- In **specialized protocols** (e.g., distributed timestamp-based like HBase's model for ordering versions, or Spanner's commit-timestamp ordering).
- In interviews: "explain basic timestamp protocol", "Thomas write rule", "compare timestamp vs 2PL", "why is it deadlock-free".

## 4. Why Wasn't Another Approach Chosen?
- *2PL (waiting)*: contention-prone, deadlock-prone, needs a central lock manager — for distributed systems, coordinating locks across nodes is expensive. Timestamp ordering replaces "wait" with "abort" — no queue, no deadlock — at the cost of wasting completed work.
- *Optimistic validation (wait until commit, then check)*: also abort-heavy, but it lets transactions do their *work* before aborting — under high contention both abort a lot; timestamp ordering aborts *earlier* (at the conflicting operation) so less work is wasted *after* detection. Choose based on conflict rates and workload.
- *Fully serial (a single timestamp gate on everything)*: too coarse; TO orders only *conflicting* operations, letting independent transactions overlap.
- *Logical vs physical timestamps*: physical (wall-clock) can have ties and clock skew; logical (Lamport-style counter / commit counters) guarantee uniqueness and total order — modern systems (Spanner) actually use *physical + uncertainty* (TrueTime) to get both real-time ordering and uniqueness.

## 5. Intuition
Think of **priority by arrival ticket at a deli counter**. Everyone takes a numbered ticket when they arrive (timestamp). The rule: the oldest ticket wins every dispute. If you (older) want to read an ingredient that a newer customer just wrote, you lose the dispute — you were supposed to go before them — so you're told to start over (abort + new ticket). If you want to write something a newer customer already read, same thing: they expected to see your older write, so abort you. The deli never blocks anyone in line (no waiting); it just yanks the wrong-order customer out. Thomas Write Rule is a small mercy: if a newer customer already wrote the item, your write is just ignored — no need to throw you out, because your write is obsolete anyway.

## 6. Real-World Analogy
**Banking queue with numbered tickets**: customer #5 wants to deposit, customer #9 wants to check the balance. If #5's deposit happens "after" #9's check in ticket order (that is, #5 is actually processed after #9, violating the order), the balance check was wrong — so #5 is politely asked to re-queue (abort). The teller never makes anyone wait-in-place for another ticket-holder (no blocking); they just re-order by reissuing tickets. If #5's deposit is simply irrelevant (a #10 deposit already landed), the teller discards #5's deposit silently (Thomas Write Rule) — the account is already newer.

## 7. Formal Definition
Each transaction T is assigned a unique, monotonically increasing timestamp TS(T). Each data item Q maintains `W-timestamp(Q)` (the TS of the transaction that last wrote Q) and `R-timestamp(Q)` (the TS of the last transaction that read Q). **Basic TO protocol**:
- read(Q): if TS(T) < W-timestamp(Q), reject: abort T and restart with a new TS; else perform the read and set R-timestamp(Q) = max(R-timestamp(Q), TS(T)).
- write(Q): if TS(T) < R-timestamp(Q), abort T and restart; else if TS(T) < W-timestamp(Q), abort T and restart; else perform the write and set W-timestamp(Q) = TS(T).
**Thomas Write Rule (TWR)**: replace the second abort case (TS(T) < W-timestamp(Q)) with *ignore the write* (the write is obsolete — a newer value is already there). TWR produces schedules that are *view-serializable* (they may not be conflict-serializable because a conflict edge is effectively "removed" by dropping the older write) and it reduces aborts. Both TO and TWR are deadlock-free — a transaction never waits on another.

## 8. Example
Initial: `A=0`, W-ts(A)=R-ts(A)=0. Transactions T1(TS=10): `write(A,1); read(A)`; T2(TS=20): `read(A); write(A,2)`.
Schedule under Basic TO:
1. T1 writes A=1 → W-ts(A)=10.
2. T2 reads A → TS(T2)=20 ≥ W-ts(A)=10 → allowed; R-ts(A)=20.
3. T1 reads A → TS(10) ≥ W-ts(A)=10 → allowed (W-ts(A)=10 ≤ 10) → reads 1. R-ts(A) stays 20.
No aborts — conflict order (T1 before T2 on A) is consistent.

Now reverse: T2 first.
1. T2 reads A=0 → R-ts(A)=20.
2. T1 writes A=1 → check: TS(10) < R-ts(A)=20 → **abort T1**. (T2's read must see T1's older write — since T2 already read, the only way to honor order is to abort T1 and restart it with a *later* timestamp, e.g., 30.)
3. T2 writes A=2 → TS(20) ≥ R-ts(20), ≥ W-ts(0) → allowed; W-ts(A)=20.
Final A=2; T1 restarted. Without the abort, T2 would have read a value "written by a transaction ordered after it" — a serializability violation.

Thomas Write Rule example: T1(TS=10) `write(A,1)`, T2(TS=20) `write(A,2)`, T3(TS=30) `write(A,3)`, executed T1, T3, T2.
- T1: W-ts(A)=10.
- T3: TS(30) ≥ 10 → allowed, W-ts(A)=30.
- T2: TS(20) < W-ts(A)=30 → under Basic TO: abort. Under TWR: **ignore the write** — the final A=3, and the schedule is view-serializable to serial order T1,T3,T2 (T2's write lost, as it would be in that serial order since T3 writes last).

## 9. Internal Working
1. Transaction start → TS assigned from a global counter (or hybrid clock). In distributed systems TS must be globally unique and roughly time-ordered (Lamport counters; Spanner's TrueTime commits).
2. Each read/write consults the item's W-ts and R-ts (stored with the data item — in MVCC engines these become version metadata).
3. On violation → the DBMS aborts the transaction: rolls back its changes (undo log), releases resources, and the app (or an auto-restarter) retries with a **new, larger timestamp** so it won't be rejected by the same conflict (a *guarantee of eventual progress* under TWR / abort-on-conflict).
4. Restart is essential: if restarted with a smaller TS it would hit the same conflict forever (starvation); new TS must be > the current max.
5. System clock / counter synchronization: needed so "TS(T1) < TS(T2)" is a meaningful order; logical counters guarantee this locally; physical clocks need clock-sync (NTP) and uncertainty bounds.

## 10. Time Complexity
- Per operation: O(1) (compare two integers + maybe update one).
- No blocking → no queue management; but **aborts cost**: O(work done so far) wasted per abort, plus restart.
- Under contention, restart frequency rises; worst case can approach "no progress" for hot items (though newer-TS restart ensures eventual success unless starved by writes).
- Memory: O(2 ints) per item for R-ts/W-ts (or folded into MVCC version metadata).

## 11. Advantages
- **Deadlock-free by construction** (no waiting ⇒ no circular wait) — a huge win vs 2PL.
- **No lock manager, no queues, no lock table** — simple, decentralized, scales to distributed settings.
- **Deterministic conflict resolution**: each conflict has a clear winner (older TS) — easy to reason about and prove.
- **Reads never block writes and writes never block reads** (unlike strict 2PL where an X-holder blocks readers); conflicting operations just abort.
- **Thomas Write Rule** cuts abort frequency while staying view-serializable.

## 12. Disadvantages
- **High abort/restart rate under contention**: transactions that do a lot of work before conflicting are costly to kill — throughput can collapse.
- **Starvation risk**: a heavily-rewritten item can cause many restarts; TWR helps but the "restart with newer TS" loop isn't guaranteed to terminate promptly under constant conflict.
- **Restart rollback overhead**: undoing work (log replay) per abort.
- **Physical-timestamp pitfalls**: clock skew and ties require logical counters or clock-sync hardware; misuse produces wrong orderings.
- **Schedules can be view-serializable but not conflict-serializable** (TWR) — slightly weaker than 2PL's guarantee.

## 13. Interview Questions
1. **Q: What is the basic timestamp ordering protocol?** A: Assign each transaction a unique timestamp; for each data item track last-read and last-write timestamps. A read is rejected (abort) if a newer transaction already wrote the item; a write is rejected if a newer transaction read or wrote it. Older timestamp wins disputes.
2. **Q: Why is timestamp ordering deadlock-free?** A: Because no transaction ever *waits* on another — every conflict is resolved immediately by aborting the younger transaction. Deadlock requires circular waiting, which can't form if nobody waits.
3. **Q: What is the Thomas Write Rule?** A: If a write arrives with TS(T) < W-timestamp(Q), instead of aborting, *ignore the obsolete write*. The schedule stays view-serializable but may not be conflict-serializable; it reduces aborts.
4. **Q: Compare timestamp ordering to 2PL.** A: 2PL blocks (waits) and can deadlock; TO aborts and never deadlocks. 2PL needs a central lock manager; TO is decentralized (just timestamps). 2PL has lower abort rates under low-to-moderate contention; TO wastes completed work when conflicts happen. Both guarantee serializability (2PL conflict-serializable; basic TO conflict-serializable; TWR view-serializable).
5. **Q: What happens when a transaction is aborted by TO?** A: It's rolled back (undo log) and restarted with a *newer* timestamp — so it won't immediately violate the same conflict. The app may also receive the abort signal and retry.
6. **Q: TRICKY: Why must a restarted transaction get a *newer*, not the same or older, timestamp?** A: If it kept the old (small) TS it would fail the same conflict forever (it's "older" than whoever now owns the item). A newer TS makes it the winner of future disputes — guaranteeing progress.
7. **Q: What timestamps do items keep, and when are they updated?** A: R-timestamp = TS of the most recent reader; W-timestamp = TS of the most recent writer. Read updates R-ts (max); write updates W-ts (and R-ts is unchanged — only actual reads update it).
8. **Q: What is the "read too old" conflict?** A: read(Q) with TS(T) < W-ts(Q): a transaction ordered *before* the last writer tries to read *after* it — violating serial order. Abort T.
9. **Q: What is the "write too old" conflict?** A: write(Q) with TS(T) < R-ts(Q) (a transaction ordered before the last reader writes after it — the reader should have seen this write) or TS(T) < W-ts(Q) (a newer write already happened). Abort T (or TWR: ignore).
10. **Q: PRODUCTION: Where do real systems use timestamp ordering?** A: Distributed databases where a global lock manager doesn't scale (CockroachDB uses hybrid timestamps + MVCC; Spanner uses TrueTime to assign commit timestamps that define serial order). Main-memory/OLTP prototypes use it to avoid lock overhead. PostgreSQL uses transaction IDs (a form of logical timestamps) for MVCC visibility — not the TO *protocol* per se, but the same timestamp machinery.
11. **Q: TRICKY: Does timestamp ordering guarantee recoverability?** A: Basic TO *can* produce non-recoverable schedules unless constrained (a transaction must wait to commit until transactions it read from commit). Real implementations add commit-ordering rules (e.g., commit after all read-from transactions) — so "deadlock-free" doesn't automatically mean "recoverable."
12. **Q: How does TO interact with dirty reads?** A: TO prevents *incorrect* ordering, but a transaction can still read an uncommitted write unless the system forces the writer to be committed before reads of its data — typically engines add a "read committed data only" constraint (like cascadelessness) on top of TO.
13. **Q: What does "restart with new timestamp" guarantee about livelock?** A: Nothing hard — starvation is theoretically possible if a hot item is constantly being written by newer transactions. In practice TWR + infrequent conflicts make it rare. This is a known weakness to name honestly.
14. **Q: What happens to a long-running transaction under TO?** A: It becomes "old," so *newer* transactions that conflict with it get aborted instead — TO actually protects long transactions (unlike 2PL where long holders are the problem). But its many writes can force many aborts of others (and itself if a newcomer writes its data — rare but possible).

## 14. Follow-Up Questions
1. **Q: What is the difference between the timestamp used in TO and the transaction ID in Postgres MVCC?** A: TO uses TS for *conflict resolution* (ordering disputes); Postgres uses XID for *visibility* (which versions a snapshot sees). The XID is a logical timestamp; MVCC read/write conflicts are handled by locks/serialization, not by TO's abort-the-younger rule.
2. **Q: How does Spanner order timestamps across datacenters?** A: TrueTime gives each commit an interval [earliest, latest]; Spanner waits out the uncertainty (commit-wait) so commit timestamps reflect real-time order — external consistency. That's timestamp *assignment*, with 2PL handling conflicts.
3. **Q: Can timestamp ordering be combined with MVCC?** A: Yes — MVCC versions are tagged with write timestamps; TO's W-ts becomes the version tag, and reads pick the largest version ≤ their read timestamp. This is how many versioned stores (HBase, TiDB-style) implement "multiversion timestamp ordering."

## 15. Coding Example
```python
class TimestampProtocol:
    def __init__(self):
        self.clock = 0
        self.w_ts = {}   # item -> write timestamp
        self.r_ts = {}   # item -> read timestamp
        self.values = {}

    def next_ts(self):
        self.clock += 1
        return self.clock

    def read(self, tx_ts, item):
        if tx_ts < self.w_ts.get(item, 0):
            return "ABORT: read too old (newer write exists)"
        self.r_ts[item] = max(self.r_ts.get(item, 0), tx_ts)
        return self.values.get(item, None)

    def write(self, tx_ts, item, value):
        if tx_ts < self.r_ts.get(item, 0):
            return "ABORT: write too old (newer read exists)"
        if tx_ts < self.w_ts.get(item, 0):
            return "IGNORED (Thomas Write Rule): newer write exists"
        self.values[item] = value
        self.w_ts[item] = tx_ts
        return "OK"

tp = TimestampProtocol()
t1, t2 = tp.next_ts(), tp.next_ts()          # t1=1 (older), t2=2 (newer)
print(tp.read(t2, 'A'))                       # read A=0 (None) → r_ts[A]=2
print(tp.write(t1, 'A', 1))                   # ABORT: 1 < r_ts[A]=2
```

## 16. Industry Usage
- **Spanner**: commit timestamps from TrueTime define serial order (external consistency); conflicts handled by Paxos + locks; timestamp machinery is the *ordering* backbone.
- **CockroachDB**: hybrid logical clock timestamps + MVCC + "transaction timestamp" pinning for serializable behavior.
- **TiDB / HBase**: MVCC with timestamps/versions for reads; write conflicts via lock/transaction manager — a blend of TO-style versioning with locking.
- **Postgres/MySQL**: not pure TO, but *logical timestamps* (XIDs) drive MVCC visibility — interviews love the comparison "MVCC timestamps vs TO timestamps."
- **VoltDB / main-memory OLTP**: sometimes use partitioned timestamp ordering (a "single-threaded per partition" simplification of TO) to avoid locking entirely.

## 17. References
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 16.4 (timestamp-based protocols) & 16.5 (validation).
- Elmasri & Navathe, Ch. 21.
- Bernstein, Hadzilacos, Goodman, *Concurrency Control and Recovery in Database Systems* (1987) — authoritative treatment.
- Lamport, "Time, Clocks, and the Ordering of Events in a Distributed System" (1978) — logical clocks.
- Corbett et al., "Spanner: Google's Globally-Distributed Database" (OSDI 2012) — TrueTime + commit ordering.
- Taft et al., "CockroachDB: The Resilient Geo-Distributed SQL Database" (SIGMOD 2020).

## 18. Cheat Sheet
- Every transaction gets a unique increasing timestamp; items track R-ts and W-ts.
- read: abort if TS < W-ts; else read, bump R-ts.
- write: abort if TS < R-ts or TS < W-ts (Basic TO); TWR ignores the second case.
- TO is deadlock-free (no waiting), but abort/restart-heavy under contention.
- Restart must use a *newer* timestamp to guarantee progress.
- TWR yields view-serializable (not always conflict-serializable) schedules.
- TO ≠ MVCC visibility; MVCC uses timestamps for reads, TO for ordering disputes.
- Long transactions benefit (newcomers get aborted, not the elder).

## 19. Quiz
1. TO resolves a conflict between transactions by: a) waiting b) aborting the younger c) aborting the older d) random → **b**
2. read(Q) aborts when: a) TS < W-ts b) TS > R-ts c) TS == W-ts d) never → **a**
3. Thomas Write Rule applies when: a) TS < R-ts b) TS < W-ts c) TS > W-ts d) TS == R-ts → **b**
4. Timestamp ordering is deadlock-free because: a) it uses locks b) no transaction waits c) it aborts older txns d) single-threaded → **b**
5. TWR produces schedules that are: a) always conflict-serializable b) view-serializable c) never serializable d) serial → **b**
6. A restarted transaction should get: a) the same TS b) a newer TS c) an older TS d) any TS → **b**
7. Which does TO NOT require? a) timestamps b) a lock manager c) abort handling d) item R/W-ts → **b**
8. TO's main weakness is: a) deadlocks b) high aborts/restarts c) lock contention d) phantoms → **b**

## 20. Flashcards
- **Q: How does TO resolve conflicts?** → **A:** Abort the younger (larger-ts) transaction; older wins.
- **Q: When does a read abort?** → **A:** When TS(T) < W-ts(item) — a newer write already happened.
- **Q: When does a write abort?** → **A:** When TS(T) < R-ts(item) (newer read) or TS(T) < W-ts(item) (newer write).
- **Q: What does Thomas Write Rule do?** → **A:** Ignores an obsolete write (TS < W-ts) instead of aborting; view-serializable.
- **Q: Why is TO deadlock-free?** → **A:** Nobody waits — conflicts are decided by timestamps instantly.
- **Q: What TS must a restart get?** → **A:** A newer one, or it fails the same conflict forever.
- **Q: TO vs 2PL?** → **A:** 2PL blocks, can deadlock, central lock manager; TO aborts, never deadlocks, decentralized.
- **Q: TO's downside?** → **A:** Abort/restart overhead under contention; possible starvation.

## 21. Revision
Timestamp ordering: TS(T) unique increasing; each item has R-ts and W-ts. Read: abort if TS < W-ts. Write: abort if TS < R-ts; abort (or TWR-ignore) if TS < W-ts. Deadlock-free (no waiting). Restart with newer TS. TWR → view-serializable. Compare to 2PL (block vs abort), to MVCC (timestamps for visibility vs ordering). Used in distributed systems (Spanner TrueTime ordering). Interviews: trace a conflict, name the abort rule, contrast with 2PL, mention restart-with-newer-TS and starvation.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Explain basic timestamp ordering." | 2, 7 |
| "Why is TO deadlock-free?" | 1, 7, 13 |
| "Thomas Write Rule?" | 2, 7, 13 |
| "TO vs 2PL comparison." | 4, 13 |
| "Why restart with a newer timestamp?" | 13, 18 |
| "What are R-ts and W-ts?" | 7, 13 |
| "Where is TO used in production?" | 13, 16 |
| "TO guarantees recoverability?" | 13, 14 |
