# Chapter: NoSQL Overview & Types

## What you'll learn
- **Why NoSQL exists**: the limits of a single relational node, horizontal scaling, and the write/read patterns relational engines weren't built for.
- **The taxonomy**: key-value, document, wide-column/columnar, and graph families — the data model, the killer use case, and the consistency model of each.
- **The trade-off vocabulary**: ACID vs BASE, CAP and PACELC, consistency models (strong, causal, eventual), and how each family picks its corner.
- **Hands-on shape of each family**: Redis/Memcached, MongoDB, Cassandra, and Neo4j — query languages, partitioning, and replication patterns.

## Prerequisites (linked)
- [Part 01](../part-01-dbms-fundamentals/README.md) — what a DBMS is, why ACID exists (the baseline NoSQL contrasts against).
- [Part 05](../part-05-transactions-and-concurrency-control/README.md) — isolation levels and consistency, the vocabulary NoSQL relaxes.
- [Part 06](../part-06-recovery-system/README.md) — durability/WAL, which NoSQL systems keep and which drop.

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [NoSQL Overview & Types](section-01-nosql-overview-and-types.md) | Why do NoSQL databases exist, and what are the big families? |
| 02 | [Key-Value & Document Stores](section-02-key-value-and-document-stores.md) | Redis, DynamoDB, MongoDB — what problems do they actually solve? |
| 03 | [Wide-Column & Columnar Stores](section-03-wide-column-and-columnar-stores.md) | Cassandra and ClickHouse — how do they differ, and from what? |
| 04 | [Graph Databases](section-04-graph-databases.md) | Neo4j — when do relationships *becomes* the data model? |
| 05 | [SQL vs NoSQL Decision Guide](section-05-sql-vs-nosql-decision-guide.md) | Which database should I pick for this problem? |

## One-paragraph narrative connecting all sections
Relational databases win on generality, integrity, and ad-hoc queries — but they scale *up* (one powerful node) by default, and joins/ACID get expensive as workloads grow. Section 01 sets the frame: NoSQL relaxes some of those guarantees in exchange for horizontal scale, simpler operations, or specialized query shapes — formalized as CAP/PACELC and the ACID-vs-BASE spectrum. Sections 02-04 walk the four families. Key-value stores (Section 02) trade almost everything for O(1) get/put at any scale (Redis cache, DynamoDB session tables). Document stores keep schemas flexible and objects self-contained (MongoDB content/activity feeds). Wide-column and columnar stores (Section 03) — Cassandra for write-heavy, always-available, time-series workloads; ClickHouse/columnar for big analytical scans. Graph databases (Section 04) make relationships first-class (Neo4j: social, fraud, knowledge graphs) where join trees would be unreadable. Section 05 ties it together as a decision guide — the "should this be SQL or NoSQL, and which flavor?" playbook interviewers actually ask, with a concrete framework, not vibes.

## Common interview trap in this chapter
**Trap:** Treating "NoSQL" as a single thing, or as "SQL but faster." It's four different data models with different trade-offs — there is no universal "NoSQL answer" to "which database." Also: quoting CAP as "consistency OR availability" as if it were a free choice — in practice the partition-tolerant choice is *which* consistency (strong vs eventual) and how, governed by PACELC's latency trade-off. And conflating a document store's "schema-less" with "no data modeling" — schema design still matters, it just lives at query time.

## Checklist before moving on
- [ ] I can name the four NoSQL families and one flagship system each.
- [ ] I can explain ACID vs BASE and CAP/PACELC with a concrete example.
- [ ] I can say when a key-value/document/wide-column/graph store is the right call.
- [ ] I can compare MongoDB vs Cassandra vs Redis vs Neo4j on data model, consistency, and partitioning.
- [ ] I can give a data-driven reason *not* to use NoSQL for a given problem.
