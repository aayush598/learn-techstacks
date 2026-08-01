# Chapter: Advanced SQL & Practice

## What you'll learn
- **Query tuning & best practices**: reading `EXPLAIN` plans, index-aware query design, avoiding N+1 and full scans, `LIMIT`/keyset pagination, and the 10 rules that separate fast SQL from slow SQL.
- **Practical SQL interview problems with solutions**: the canonical pattern library — top-N per group, dedupe, running totals, gaps, sessionization, conditional aggregation — solved end-to-end on sample data.

## Prerequisites (linked)
- [Chapter 02 (SQL)](../chapter-02-sql/README.md) — all six sections (SELECT order, joins, aggregation, subqueries, windows) are the raw material this chapter tunes and drills.
- [Part 04 (Indexing)](../../part-04-indexing-and-file-organization/README.md) will explain *why* the index advice here works (B+ trees, covering indexes).

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — SQL Query Tuning and Best Practices](section-01-sql-query-tuning-and-best-practices.md) | EXPLAIN literacy; index-fit; N+1; pagination; the tuning checklist |
| [Section 02 — Practical SQL Interview Problems with Solutions](section-02-practical-sql-interview-problems-with-solutions.md) | 15 solved problems: top-N, dedupe, gaps, sessions, percentiles, running totals |

## One-paragraph narrative connecting all sections
Correct SQL (Chapter 02) is only half of production readiness — the other half is *speed and robustness*, which Section 01 attacks with `EXPLAIN` literacy, index-aware predicates, batching, and pagination. Everything in Section 01 is then exercised in Section 02's solved problems: each of the 15 problems is written, explained, and then given a performance note (which index, which plan). The two sections together turn "I can write SQL" into "I can write production-grade SQL and defend it in an interview."

## Common interview trap in this chapter
Candidates stop at "it returns the right rows." Interviewers (and production) demand: **can you read the plan, name the index, and predict the cost?** The second trap is answering every problem with the first query that works — Section 02 problems have *two* canonical answers (subquery vs window vs CTE), and you should pick the one whose plan is cheapest, then say why. Third: N+1 — answering with a loop when a single JOIN/GROUP BY exists. Always say "one query, not N queries."

## Checklist before moving on
- [ ] I can read a Postgres `EXPLAIN` output and name each node (SeqScan/IndexScan/HashJoin/Sort).
- [ ] I can explain why `WHERE year(created_at)=2024` defeats an index, and the rewrite.
- [ ] I can write the 5 canonical patterns from memory: top-N per group, dedup, running total, gap finder, sessionizer.
- [ ] I can explain keyset pagination and why OFFSET is slow.
- [ ] I can detect and fix an N+1 in SQL (single query instead of a loop).
- [ ] I can solve any of Section 02's 15 problems in under 3 minutes.
