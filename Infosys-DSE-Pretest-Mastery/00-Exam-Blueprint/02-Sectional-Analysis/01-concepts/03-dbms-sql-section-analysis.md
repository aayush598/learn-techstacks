# DBMS / SQL Section Analysis (10 Q)

> Section 00 · Exam Blueprint · Sectional Analysis · _Estimated reading time: 16 min_
> **Prerequisite:** [../README.md](../README.md)

## In one sentence
**DBMS/SQL is the most predictable 10 marks on the paper** — learn JOINs, ACID, normalization, and simple query output, and 7-8 correct becomes routine.

## Why the pre-test tests this
- **Predictable scope:** the reported scope is "SQL up to JOINs", not advanced tuning, windowing, or query optimisation.
- **Ground-truth topics:** normalization, ACID, DBMS theory, and two-table queries recur.
- **High ROI for Data Engineering aspirants:** this section maps most directly to the Data Engineering and Data Science & Agentic AI streams.
- **Supports Meera:** DBMS-strong candidates use this section to bank near-guaranteed marks and build a buffer above 39.

## Core concept

### The sub-topics and their cost
| Topic | Typical share | Cost per mark | Notes |
|-------|---------------|---------------|-------|
| SQL up to JOINs | ~2-3 Q | Medium | Inner and left joins |
| Write a query for two tables | ~1-2 Q | Medium-high | Careful SELECT/JOIN/WHERE |
| Identify output of a given SQL | ~2 Q | Medium | Trace step by step |
| Normalization | ~1-2 Q | Low | 1NF/2NF/3NF definitions |
| ACID | ~1 Q | Low | Definitions |
| DBMS theory (keys, indexes, views) | ~1-2 Q | Low | Definitions |

### Difficulty distribution
| Band | Share | Notes |
|------|-------|-------|
| Easy | ~5-6 Q | ACID, normalization, theory |
| Medium | ~3-4 Q | Joins, output tracing |
| Hard | ~1-2 Q | Multi-condition query writing |

### Where the marks are cheapest
1. **ACID:** four definitions, no computation.
2. **Normalization levels:** 1NF atomic, 2NF no partial dependency, 3NF no transitive dependency.
3. **DBMS theory:** keys (primary, candidate, foreign), indexes, views.
4. **Basic JOIN output:** trace two small tables.

### Normalization quick table
| Form | Requirement | Broken by |
|------|-------------|-----------|
| 1NF | All attributes atomic (no repeating groups) | A cell with multiple values |
| 2NF | 1NF + no partial dependency on a composite key | Non-key attribute depending on part of the key |
| 3NF | 2NF + no transitive dependency | Non-key attribute depending on another non-key attribute |

### ACID quick table
| Property | Meaning |
|----------|---------|
| Atomicity | A transaction is all-or-nothing |
| Consistency | A transaction moves the database from one valid state to another |
| Isolation | Concurrent transactions do not interfere |
| Durability | Committed changes survive a crash |

### How the weight maps to score
10 questions = 16.7% of the paper. Target **7-8 correct**. For Data Engineering aspirants this section is the anchor that makes 39 comfortable.

## Worked example
**Output question:**
```sql
SELECT COUNT(*)
FROM orders o
JOIN customers c ON o.cid = c.id
WHERE c.city = 'Pune';
```

**Scenario:** 3 customers are in Pune. There are 5 orders total, 4 of which belong to Pune customers.

Trace:
1. The join keeps only orders whose customer is in Pune → 4 rows.
2. `COUNT(*)` counts rows after the join → **4**.

**Distractors:**
- "3" counts customers, not orders.
- "5" forgets the WHERE filter.
- "0" would be the answer if no customer were in Pune.

**Answer: 4.**

### Two-table query pattern
When asked to write a query for two tables:
```sql
SELECT c.name, o.amount
FROM customers c
JOIN orders o ON o.cid = c.id
WHERE c.city = 'Pune';
```
Fix the join key first, then the filter, then the selected columns.

## Quick rules
- **Trace joins row by row for small tables.**
- **`COUNT(*)` after a JOIN is not the count of the left table.**
- **LEFT JOIN keeps unmatched left rows (NULLs on the right).**
- **1NF atomic, 2NF no partial dependency, 3NF no transitive dependency.**
- **ACID = Atomicity, Consistency, Isolation, Durability.**
- **WHERE filters rows; HAVING filters groups.**

## Common traps
- **Confusing WHERE and HAVING.** WHERE runs before grouping; HAVING after.
- **Miscounting rows after a JOIN** by forgetting the join multiplicity.
- **Mixing up 2NF and 3NF conditions** — partial vs transitive dependency.
- **Forgetting NULL semantics:** `NULL = NULL` is not true; comparisons with NULL yield unknown.

## Checklist
- [ ] You know all six DBMS sub-topics and their approximate shares.
- [ ] You can classify 1NF/2NF/3NF on sight.
- [ ] You can recite ACID.
- [ ] You trace joins before answering an output question.
- [ ] You know WHERE vs HAVING.
- [ ] Your DBMS target is 7-8 correct.

## Related
- [02-english-ld-section-analysis.md](02-english-ld-section-analysis.md)
- [04-java-section-analysis.md](04-java-section-analysis.md)
- [05-score-model-building-39.md](05-score-model-building-39.md)
- [../02-techniques/01-cheapest-marks-first.md](../02-techniques/01-cheapest-marks-first.md)
