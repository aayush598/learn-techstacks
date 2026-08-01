# Chapter: Transactions

## What you'll learn
- What a *transaction* is, why a single SQL statement isn't the unit of work, and what the **ACID** acronym really commits the database to.
- The lifecycle of a transaction: the five states (active → partially committed → committed / failed → aborted) and how failure forces the DBMS to choose between undo and redo.
- Why concurrent transactions can produce wrong results even though each one is individually correct, and how **serializability** — conflict and view — is the formal yardstick for "as good as running one at a time."
- The four ANSI/SQL isolation levels (READ UNCOMMITTED → SERIALIZABLE), the anomalies each one permits (dirty read, non-repeatable read, phantom), and how the DBMS trades safety for throughput.

## Prerequisites (linked)
- [Part 05 README](../README.md) — the roadmap and study order.
- [Part 04](../part-04-indexing-and-file-organization/README.md) — you need to know that data lives in *pages* and that indexes are *B-trees* before locking semantics make sense.
- Part 01/02: relations, tuples, and basic SQL (`SELECT`, `UPDATE`, `INSERT`) — the data a transaction reads and writes.

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Transaction Concept and ACID Properties](section-01-transaction-concept-and-acid-properties.md) | What is a transaction, and what four promises does ACID make? |
| 02 | [Transaction States and Schedules](section-02-transaction-states-and-schedules.md) | What are the states a transaction passes through, and what happens when we interleave them? |
| 03 | [Serializability: Conflict and View](section-03-serializability-conflict-and-view.md) | When is an interleaved execution "as good as" a serial one — formally? |
| 04 | [Isolation Levels in Depth](section-04-isolation-levels-in-depth.md) | What does the SQL standard (and Postgres/MySQL) actually let you trade away? |

## One-paragraph narrative connecting all sections
A transaction bundles several database operations into one atomic unit, and ACID (Section 01) is the contract that makes that bundle trustworthy — including the requirement that two bundles running simultaneously must not corrupt each other. To reason about "simultaneously," Section 02 models each transaction as a sequence of read/write steps and then studies the *schedules* (interleavings) those steps can produce, introducing the states (committed/aborted) that recovery (Part 06) must respect. Section 03 then defines the correctness target: a schedule is good if it is equivalent, in a precise conflict- or view-based sense, to some serial schedule — this is serializability, the theoretical foundation for every protocol in Chapter 02. Finally, Section 04 acknowledges that fully serializable execution is expensive, so the SQL standard defines four isolation levels, each allowing a known, documented anomaly in exchange for concurrency; knowing which anomaly each level permits is the most common interview question in the entire DBMS subject.

## Common interview trap in this chapter
**Trap:** Confusing *consistency* (the C in ACID) with the *isolation* guarantee. Consistency is a property of the *database's application-level invariants* (e.g., "balance ≥ 0") — the DBMS can only check declarative constraints, not your business rules. Isolation is the DBMS's own guarantee that concurrent transactions behave as if serial. Interviewers also love the trap of saying "SERIALIZABLE prevents all anomalies" — true, but only if the DBMS actually *enforces* it (Postgres's SERIALIZABLE does via SSI; MySQL InnoDB's REPEATABLE READ is even *stronger* than the standard in some ways but still has the gap-lock write-skew limits). Also: "committed" is not the same as "durable" — a transaction can be committed in memory and lost in a crash (that's Part 06's job).

## Checklist before moving on
- [ ] I can define a transaction and give a real example of why one SQL statement is not enough.
- [ ] I can state all four ACID properties and give one counter-example that violates each.
- [ ] I can draw the transaction state diagram and explain when a transaction needs undo vs redo.
- [ ] I can classify a schedule as serial, serializable, or not, by hand, using conflict and view equivalence.
- [ ] I can name the four isolation levels, the anomaly each permits, and the default of Postgres and MySQL.
