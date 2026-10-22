# Normalization — Topic Guide

> Section 3 · DBMS & SQL · Normalization · _Estimated reading time: 35 min for the full topic_

## What the pre-test asks in this topic

**Normalization is 1–2 of the 10 DBMS questions** and it is the cheapest marks in the section — no
SQL, no fixture, no computation. The exam asks one of four things:

- "Which normal form is this table in?" → the answer is the **highest** form it satisfies.
- "What is a partial dependency / transitive dependency?" → pick the definition.
- "Which decomposition is lossless?" → check the shared attributes against the keys.
- "What anomaly does this design cause?" → insert, update or delete.

## Learning objectives

After this topic you should be able to:

- State 1NF, 2NF, 3NF and BCNF in one precise line each, and say **what each one removes**.
- Explain the difference between **partial** and **transitive** dependency using the words *part of
  the key* and *through another attribute*.
- Find the candidate key of a small table in under 30 seconds, and know that a **single-attribute key
  makes 2NF automatic**.
- Explain why 3NF and BCNF differ **only** in the case of a **prime-attribute** dependency.
- Distinguish **prime attributes** from the **primary key**.
- Check a binary decomposition for **lossless join** (shared attributes form a key of one side) and
  for **dependency preservation** (every FD enforceable in one table).
- Name the **insert, update and delete anomalies** and say which decomposition fixes them.
- Give one scenario where **denormalisation** is the right call and one where it is not.

## File index

| File | Lines | What it gives you |
|---|---|---|
| [01-concepts/01-normal-forms-defined.md](01-concepts/01-normal-forms-defined.md) | ~330 | Vocabulary, all four definitions with formal tests, lossless join, dependency preservation, denormalisation, the three anomalies |
| [02-techniques/01-normalization-decision-procedure.md](02-techniques/01-normalization-decision-procedure.md) | ~260 | The 6-step classification procedure, key-finding checklist, chain test, decomposition procedure, the 6-question decomposition checklist |
| [03-worked-examples/01-solved-normalization-set.md](03-worked-examples/01-solved-normalization-set.md) | ~380 | 8 solved questions with full reasoning and distractors explained |
| [04-pitfalls/01-normalization-traps.md](04-pitfalls/01-normalization-traps.md) | ~200 | 10 traps + 1 bonus, each with the tell in the option |
| [05-reference/01-normalization-quick-check.md](05-reference/01-normalization-quick-check.md) | ~170 | The one-page version: definitions, ladder, anomaly table, the UNF→3NF worked fixture |

## Quick 6-step procedure

1. **Find the key.** Single attribute → 2NF is automatic. Composite → keep going.
2. **Check 1NF.** Atomic cells? Any repeating group of columns? If no → **not 1NF**.
3. **Check 2NF.** Does a non-prime attribute depend on **part** of a composite key? If yes → **1NF**.
4. **Check 3NF.** Does a non-prime attribute depend on **another non-prime attribute**? If yes →
   **2NF**.
5. **Check BCNF.** Is every determinant a superkey? If no → **3NF**.
6. **Otherwise → BCNF.**

Stop at the first failure. The answer is the last form passed.

## Key takeaways

- ✅ **1NF = atomic values, no repeating groups.** Repeating data across *rows* is not a 1NF issue.
- ✅ **2NF = no partial dependency.** Only matters with composite keys.
- ✅ **3NF = no transitive dependency.** The chain is `A → B → C`.
- ✅ **BCNF = every determinant is a superkey.** The only gap from 3NF is prime-attribute
  dependencies.
- ✅ **Prime ≠ primary.** Prime means "in *some* candidate key".
- ✅ **Lossless** = shared attributes are a key of one side. **Dependency preserving** = every FD
  lives inside one table.
- ✅ **Denormalise only for read-heavy, join-expensive workloads** — warehouses, reporting,
  materialised views. Never for ledgers or balances.
- ⚠️ **Ananya's note:** she reads the definitions but never learns the *procedure*. The procedure is
  the mark.

## Related

- [DBMS & SQL section index](../README.md)
- [DBMS Theory, Keys, Indexes & Views](../07-DBMS-Theory-Keys-Indexes-Views/README.md) — keys, candidate keys and schema levels that normalization builds on
- [SQL Basics: DDL & DML](../01-SQL-Basics-DDL-DML/README.md) — `CREATE TABLE`, `ALTER TABLE`, constraints
- [Master README](../../README.md)
