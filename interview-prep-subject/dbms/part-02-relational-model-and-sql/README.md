# Part: Relational Model & SQL

## What this part covers
The **single most-tested topic in all of DBMS interviews**. It takes the relational model that Part 01 introduced and makes it operational: the precise definition of a relation (with why order doesn't matter), keys and how to find them, integrity constraints, and the relational algebra that gives SQL its semantics. Then it drills SQL itself — SELECT execution order, DDL/DML, joins, GROUP BY, subqueries/CTEs, and window functions — ending with query-tuning best practices and a bank of solved practical SQL problems. If you prepare only one part before an interview, it is this one.

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| ch-01 Relational Model | Relational model & schema, keys (super/candidate/primary/foreign), integrity constraints, relational algebra operations | Define a relation formally, identify candidate keys from FDs, enforce entity/referential/domain integrity, write queries in relational algebra notation |
| ch-02 SQL | SELECT in depth, DDL/DML/DCL & constraints, joins, aggregation & GROUP BY, subqueries & CTEs, window functions | Write correct, optimized SQL; know the logical execution order; classify every join type; know where the 8 JOIN semantics fail (NULLs); use ROW_NUMBER/RANK/LAG correctly |
| ch-03 Advanced SQL & Practice | Query tuning & best practices, practical SQL interview problems with solutions | Read an EXPLAIN plan, avoid N+1, write the classic data-prep queries (top-N per group, gaps, dedupe, running totals) from memory |

## Study order
1. **ch-01** first — relational algebra is the *semantics* of SQL; knowing it makes tricky SQL questions mechanical.
2. **ch-02** second — the meat: write thousands of queries across the 6 sections.
3. **ch-03** last — tuning + the pattern library; revisit before every interview to stay sharp.
Read every section in numbered order within a chapter; each section assumes the previous one.

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ⭐⭐⭐⭐⭐ (5/5)** — *the* most heavily weighted DBMS topic. SQL screens are common at **Amazon (SQL assessment for BI/data roles), Meta, Google, Stripe, Snowflake, Databricks, Airbnb, Uber, and every analytics/data-engineering interview**.
- **Emphasized by**: anyone who touches data — backend SWE, data engineers, analysts, ML pipelines. Expect 30-60% of a DBMS round to be SQL.
- Typical asked: "write a query for top 3 salaries per dept", "inner vs left join", "where can't you use window functions", "EXPLAIN your query".

## How the parts connect (roadmap)
- **Part 01** gave the relational model at the conceptual level; this part makes it concrete and testable in SQL.
- **Part 03 (Normalization)** reuses this part's keys, FDs and relation vocabulary to judge *design* quality.
- **Part 04 (Indexing & File Organization)** explains *why* certain SQL patterns (seeks vs scans, covering indexes) are fast — the query-tuning section previews that.
- Transaction/concurrency parts later explain isolation behaviors you'll notice when writing `UPDATE`s.
