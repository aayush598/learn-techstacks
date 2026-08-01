# Part: Transactions and Concurrency Control

> **TL;DR**: Transactions give database users the "all-or-nothing" guarantee (ACID), and concurrency control is the machinery that lets thousands of transactions interleave safely without corrupting data — the single most-asked DBMS interview area at FAANG/MAANG.

## What this part covers
Part 05 answers the question "what happens when two or more database operations run at the *same time*, and one of them crashes midway?" It covers the transaction abstraction and ACID properties, the schedules that interleaving transactions produce, the three kinds of serializability, the four SQL isolation levels and their anomalies, and the concrete protocols databases use to enforce safety (2PL and its variants, timestamp ordering, validation, MVCC, and deadlock handling). It closes with how real engines (Postgres and MySQL InnoDB) implement these ideas and a curated interview question bank.

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| **Chapter 01: Transactions** | transaction concept & ACID; transaction states & schedules; serializability (conflict & view); isolation levels in depth | Define a transaction; explain every ACID property with a counter-example; classify schedule equivalence; derive conflict/view serializability; map isolation levels to anomalies |
| **Chapter 02: Concurrency Control Protocols** | locking & 2PL; lock granularity & types; timestamp-based protocols; validation & MVCC; deadlock handling | Design 2PL schedules; trace the growing/shrinking phases; apply lock escalation and intention locks; run timestamp/validation protocols; write deadlock detection and prevention strategies |
| **Chapter 03: Concurrency in Practice** | MVCC in Postgres & InnoDB; optimistic vs pessimistic | Explain real snapshot isolation, version chains, and `REPEATABLE READ` semantics in two production engines |
| **Chapter 04: Transaction Practice** | interview questions | Answer 25+ transaction/concurrency questions with production-grade answers |

## Study order
1. **Chapter 01** — build the vocabulary: transaction, ACID, schedule, serializability, isolation level. Everything else reuses these terms.
2. **Chapter 02** — learn the *protocols* that guarantee the guarantees (2PL is the crown jewel; it is the basis of most interview answers).
3. **Chapter 03** — see how the theory shows up in Postgres and MySQL (interviewers love "but how does Postgres actually do it?").
4. **Chapter 04** — apply it all to interview questions.

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ★★★★★ (5/5)** — a top-3 DBMS topic. Nearly every database round opens with "what are ACID properties?" or "what is serializability?"
- **Emphasized by**: all of them — Google (Spanner/F1, Bigtable consistency), Meta (TAO/MySQL at scale), Amazon (DynamoDB + Aurora), Apple, Microsoft (SQL Server isolation levels), Stripe, Databricks, and every Postgres-based startup. System-design rounds (designing a chat app, an inventory system, a payment ledger) all hinge on concurrency control.
- Typical asked: "ACID", "2PL vs MVCC", "isolation levels", "deadlock vs livelock", "phantom reads", "what does `SELECT ... FOR UPDATE` do", "design an inventory system with 100k TPS".

## How the parts connect (roadmap)
- **Part 04 (Indexing & File Organization)** is a prerequisite: concurrency control operates on pages and index structures (lock managers acquire locks on records/pages/B-tree nodes).
- **Part 05 Chapter 01-02** give the theory of correctness; **Chapter 03-04** ground it in real engines.
- **Part 06 (Recovery System)** is the direct sequel: concurrency control prevents *anomalies from interleaving*, recovery fixes *anomalies from crashes*. The two are inseparable — a concurrency protocol that isn't crash-safe (e.g., strict 2PL) is worthless.
- **Part 07 (Query Processing)** asks "how fast is a query?" — but `SELECT FOR UPDATE`, transactions, and locking from this part determine real throughput.
- **Part 08 (NoSQL + Question Bank)** compares ACID relational stores to BASE NoSQL stores — you need this part's vocabulary to answer "why would you give up ACID?"
