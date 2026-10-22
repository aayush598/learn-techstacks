# DBMS Theory, Keys, Indexes & Views — Topic Guide

> Section 3 · DBMS & SQL · DBMS Theory, Keys, Indexes & Views · _Estimated reading time: 38 min for the full topic_

## What the pre-test asks in this topic

**DBMS theory is the broadest archetype in Section 3 — 1–2 of the 10 questions, and the content
ranges across six unrelated bodies of knowledge:**

- The **ANSI/SPARC three-level schema** and the two kinds of **data independence**.
- The **data languages** — DDL, DML, DQL, DCL, TCL.
- **Keys** — superkey, candidate, primary, alternate, composite, partial, foreign, natural,
  surrogate.
- **Referential integrity** and the `ON DELETE` actions.
- **ER model** — cardinality, participation, entity and attribute types.
- **Indexes** — B-tree vs hash, clustered vs non-clustered, dense vs sparse, selectivity.
- **Views** — virtual vs materialized, updatability.
- **Architecture** — 1/2/3-tier, DBMS vs flat files, the DBA's role.

The exam asks these as recall, not computation. **Read the list once and you own the archetype.**

## Learning objectives

After this topic you should be able to:

- Name the three schema levels and say exactly what each one contains.
- State **logical** and **physical** data independence correctly, and say which level changes in each.
- Sort every common SQL command into **DDL, DML, DQL, DCL, TCL** instantly.
- Define all **ten key types**, and explain why **prime ≠ primary**.
- Place a **foreign key** on the correct side of a relationship, and pick the right `ON DELETE`
  action.
- Read **cardinality** (1:1, 1:N, M:N) and **participation** (total, partial) off a scenario, and know
  when a junction table is needed.
- Choose between a **B-tree** and a **hash** index for a stated query, and apply the **leftmost
  prefix rule**.
- List the rules for an **updatable view**, and say why a virtual view cannot be indexed.
- Tell a **procedure**, a **function** and a **trigger** apart in one line each.
- Count **tiers** in an architecture description.

## File index

| File | Lines | What it gives you |
|---|---|---|
| [01-concepts/01-schema-keys-and-indexes.md](01-concepts/01-schema-keys-and-indexes.md) | ~470 | Every definition in the archetype, with fixture examples for each |
| [02-techniques/01-dbms-concept-procedures.md](02-techniques/01-dbms-concept-procedures.md) | ~280 | The 20-second classifier, ten concept tables, the definition-wording rule, the "which is NOT" trap |
| [03-worked-examples/01-solved-dbms-theory-set.md](03-worked-examples/01-solved-dbms-theory-set.md) | ~380 | 9 solved questions with full reasoning and distractors explained |
| [04-pitfalls/01-dbms-theory-traps.md](04-pitfalls/01-dbms-theory-traps.md) | ~190 | 9 traps + 2 bonus, each with the tell in the option |
| [05-reference/01-dbms-theory-quick-check.md](05-reference/01-dbms-theory-quick-check.md) | ~200 | The one-page version of every table above |

## Quick procedure

1. **Classify the stem in 20 seconds** — which of the ten concept families is this?
2. **Read the options as definitions**, not as assertions. Two will be near-identical sentences.
3. **Find the tell word** — *minimal*, *physical*, *automatically*, *any*, *every*, *never*.
4. **Check the direction** of relationships and which side holds the FK.
5. **If the stem says "NOT", verify every option** instead of hunting for the best one.

## Key takeaways

- ✅ **External = view, Conceptual = logical, Internal = physical.**
- ✅ **Logical independence** = conceptual changes, external unaffected. **Physical** = internal
  changes, conceptual unaffected.
- ✅ **Superkey** = any determinant. **Candidate key** = minimal superkey. **Primary** = the one you
  chose. **Prime** = in *some* candidate key.
- ✅ **FK on the many side.** M:N needs a junction table; 1:N does not.
- ✅ **B-tree** for ranges and sorts, **hash** for equality, **clustered** stores the rows.
- ✅ **Leftmost prefix rule** for composite indexes; **covering index** avoids the table lookup.
- ✅ **Virtual views**: not stored, not indexed, recomputed — often slower. **Materialized** views:
  stored, indexable, can be stale.
- ✅ **Only simple single-table views are updatable.**
- ✅ **Trigger fires automatically**; a procedure must be called.
- ⚠️ **Rahul's note:** the definitions are hard to read cold in English. Read them twice — the second
  pass is where they stick.

## Related

- [DBMS & SQL section index](../README.md)
- [SQL Basics: DDL & DML](../01-SQL-Basics-DDL-DML/README.md) — the commands behind DDL and DML
- [Joins](../02-Joins/README.md) — the FK relationships this topic describes
- [Functions, Aggregates & CASE](../08-Functions-Aggregates-Case/README.md) — `COUNT`, `SUM`, `CASE`
  in depth
- [Master README](../../README.md)
