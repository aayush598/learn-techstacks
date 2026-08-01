# Chapter: Concurrency Control Protocols

## What you'll learn
- How **locking** turns the abstract "schedule must be serializable" requirement into a mechanical rule the DBMS can enforce, and exactly why **two-phase locking (2PL)** is the protocol that guarantees conflict serializability.
- The *fine print*: shared/exclusive locks, lock compatibility matrices, lock granularity (record → page → table), intention locks, and lock escalation — the machinery every production lock manager runs.
- The *alternatives to locking*: **timestamp-based protocols** (ordering by birth-time, not waiting), **validation** (optimistic, check-then-commit), and **MVCC** (never wait, read old versions) — and why each trades off differently.
- What happens when all of this goes wrong: **deadlock** (detection, prevention, avoidance, and why real DBMSes pick detection + victim rollback).

## Prerequisites (linked)
- [Chapter 01 README](chapter-01-transactions/README.md) — you must know what a transaction, schedule, and serializability are before studying protocols.
- [Part 05 README](../README.md) — roadmap.

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Locking Protocols and Two-Phase Locking](chapter-02-concurrency-control-protocols/section-01-locking-protocols-and-two-phase-locking.md) | How does a lock rule guarantee serializable schedules? |
| 02 | [Lock Granularity and Lock Types](chapter-02-concurrency-control-protocols/section-02-lock-granularity-and-lock-types.md) | What exactly does a transaction lock — a row, a page, a table? |
| 03 | [Timestamp-Based Protocols](chapter-02-concurrency-control-protocols/section-03-timestamp-based-protocols.md) | How do you get serializability by *ordering* instead of *waiting*? |
| 04 | [Validation and Multiversion Concurrency Control (MVCC)](chapter-02-concurrency-control-protocols/section-04-validation-and-multiversion-concurrency-control-mvcc.md) | What if you just let everyone run and fix conflicts at commit? |
| 05 | [Deadlock Handling in Databases](chapter-02-concurrency-control-protocols/section-05-deadlock-handling-in-databases.md) | Who detects the circular wait, and who gets rolled back? |

## One-paragraph narrative connecting all sections
Chapter 01 established *what* "correct concurrency" means (serializability) and *how much* safety each isolation level buys. Chapter 02 turns that into *mechanism*. Section 01 shows the cornerstone protocol: acquire locks, and split the transaction into a growing phase (acquire only) and a shrinking phase (release only) — 2PL — which provably yields only conflict-serializable schedules, and whose *strict* variant (release at commit) also gives the recoverable/strict schedules recovery needs. Section 02 answers the practical question 2PL leaves open — *what do you lock?* — with a hierarchy (records, pages, tables) plus intention locks so that fine-grained and coarse-grained locks coexist without exploding bookkeeping. Section 03 steps off the locking path entirely: instead of making transactions *wait*, timestamp ordering gives each transaction a birth time and aborts any conflict that violates time order — serializability without waiting, at the price of many aborts. Section 04 goes further with validation (optimistic: run, then check) and MVCC (the dominant production design: never block readers; serve old versions from a version chain, abort on write-write conflict). Section 05 handles the failure mode every protocol inherits — deadlock — covering detection via wait-for graphs, victim selection, and the timeout vs. graph trade-off. By the end you can explain why Postgres uses MVCC, why MySQL InnoDB uses MVCC + next-key locks, and why Spanner uses locks + timestamps: each protocol is a different point on the wait-vs-abort-vs-version spectrum.

## Common interview trap in this chapter
**Trap:** Saying "2PL prevents deadlocks" — it does **not**; 2PL guarantees serializability but can still deadlock (deadlock is a separate concern handled by detection/prevention). Also: saying "MVCC prevents all write conflicts" — it aborts on write-write conflicts but can *delay* reads? No — MVCC's whole point is readers never wait; the trap is thinking MVCC is serializable. Snapshot isolation (the MVCC default) is *not* serializable (write skew), which is why Postgres needed SSI. Also common: confusing *lock compatibility* (shared/shared compatible) with *lock types* (record/gap/next-key). And "READ COMMITTED uses shared locks on reads" is wrong in MVCC engines — reads take *no* locks (they read snapshots); locking engines (old SQL Server style) do use shared locks. Say the mechanism you mean.

## Checklist before moving on
- [ ] I can state 2PL's two phases and prove it gives conflict serializability; I know strict vs rigorous 2PL.
- [ ] I can fill in a lock-compatibility matrix and explain why shared/shared is allowed but exclusive with anything is not.
- [ ] I can explain intention locks and multi-granularity locking, and when lock escalation happens.
- [ ] I can run the Thomas write rule / basic timestamp protocol by hand and say when it aborts vs overwrites.
- [ ] I can describe MVCC's version chain, read/write-conflict rules, and why snapshot isolation is not serializable.
- [ ] I can draw a wait-for graph, find the cycle, and justify victim selection; I can contrast detection vs timeout vs wound-wait.
