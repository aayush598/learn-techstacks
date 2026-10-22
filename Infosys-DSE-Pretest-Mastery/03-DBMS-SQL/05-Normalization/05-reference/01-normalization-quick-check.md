# Normalization Quick Check — One Page

> Section 3 · DBMS & SQL · Normalization · _Estimated reading time: 3 min_
> **Prerequisite:** [Normalization decision procedure](../02-techniques/01-normalization-decision-procedure.md)

## In one sentence

The four definitions, the decision ladder, the anomaly table and the decomposition rules — the whole
archetype on one page.

## Why the pre-test tests this

- One page = one revision session. Read it the morning of the exam and the archetype is closed.
- It is 1–2 marks, so a 3-minute review is the best marks-per-minute trade in Section 3.

## Core concept

### The four forms

| Form | Requirement | Removes |
|---|---|---|
| **1NF** | Atomic values, no repeating groups, unique rows | Repeating groups |
| **2NF** | 1NF + no **partial** dependency | Repeating non-key data across a composite key |
| **3NF** | 2NF + no **transitive** dependency | Repeating non-key data through another non-key attribute |
| **BCNF** | 3NF + every determinant is a superkey | Prime-attribute dependencies |

### Vocabulary card

| Term | One-line meaning |
|---|---|
| `X → Y` | X functionally determines Y |
| Superkey | Determines **all** attributes |
| Candidate key | **Minimal** superkey |
| Primary key | The candidate key you picked |
| Prime attribute | In **some** candidate key |
| Non-prime attribute | In **no** candidate key |
| Partial dependency | Non-prime attribute depends on **part** of a composite key |
| Transitive dependency | `A → B → C`, C non-prime, B not a superkey |
| Lossless join | Join reproduces the original exactly |
| Dependency preservation | Every FD enforceable inside one table |

### The decision ladder

```
1. Find the key.
   ├─ single attribute → 2NF is automatic
   └─ composite        → check partial deps
2. Any non-atomic cell or repeating group of columns?  → NOT 1NF
3. Non-prime attribute depends on part of a composite key? → 1NF
4. Non-prime attribute depends on another non-prime attr?  → 2NF
5. Some determinant is not a superkey?                   → 3NF
6. Otherwise                                            → BCNF
```

### Formal tests

| Form | Formal test for every non-trivial FD `X → A` |
|---|---|
| 3NF | `X` is a superkey **OR** `A` is prime |
| BCNF | `X` is a superkey |

### Anomaly table

| Anomaly | Trigger | Fixed by |
|---|---|---|
| Insertion | Cannot add one fact without an unrelated one | 3NF decomposition |
| Update | Same fact stored in many rows | 3NF decomposition |
| Deletion | Removing one fact destroys another | 3NF decomposition |

### Decomposition rules

| Rule | Test |
|---|---|
| Lossless | `R1 ∩ R2` is a key of at least one of `R1`, `R2` |
| Dependency preserving | Every FD of `R` is enforceable in one piece |
| Don't over-decompose | Stop when the anomalies are gone |

### Worked fixture for this topic

```
UNF   EMP_REC(Emp_Id, Emp_Name, Emp_Salary, Dept_Id, Dept_Name,
              Dept_Location, {Proj_Id, Hours_Worked} ×n)

1NF   EMP_PROJECT(Emp_Id, Proj_Id, Emp_Name, Emp_Salary, Dept_Id,
                  Dept_Name, Dept_Location, Hours_Worked)
      key (Emp_Id, Proj_Id)

2NF   EMP(Emp_Id PK, Emp_Name, Emp_Salary, Dept_Id)
      EMP_PROJECT(Emp_Id, Proj_Id, Hours_Worked)  PK (Emp_Id, Proj_Id)
      EMP ∩ EMP_PROJECT = {Emp_Id} = key of EMP → LOSSLESS

3NF   DEPT(Dept_Id PK, Dept_Name, Dept_Location)
      EMP(Emp_Id PK, Emp_Name, Emp_Salary, Dept_Id FK)
      EMP ∩ DEPT = {Dept_Id} = key of DEPT → LOSSLESS
```

### Denormalisation — when it is correct

| ✅ Justified | ❌ Not justified |
|---|---|
| Data warehouse / star schema | Transactional ledger |
| Read-heavy reporting tables | Stock / balance tables |
| Materialised views | Anything where consistency matters |
| Distributed replication | Small, well-normalised OLTP tables |

### Quick facts

- 2NF only matters with a **composite** key.
- 3NF and BCNF differ **only** on prime-attribute dependencies.
- "In 2NF but not in 3NF" answers both exam phrasings.
- Codd's phrase: *the key, the whole key, and nothing but the key*.

## Worked example

**Q. `EMP_PROJECT(Emp_Id, Proj_Id, Hours_Worked)` with key `(Emp_Id, Proj_Id)`. Highest normal
form?**

- A. 1NF
- B. 2NF
- C. 3NF
- D. BCNF

**Solution:** 1NF ✅. Key is composite, `Hours_Worked` depends on the **whole** key → no partial
dependency → 2NF ✅. No chain → 3NF ✅. Every determinant (`Emp_Id`, `Proj_Id` as a pair) is a
superkey → BCNF ✅.

**Answer: D (BCNF).**

## Quick rules

- Key first. Composite key → check partial. Single key → 2NF free.
- Stop at the first failure.
- Partial = part of the key. Transitive = through an attribute.
- 3NF allows prime-attribute dependencies; BCNF does not.
- Lossless ⟺ shared attributes are a key of one side.
- Denormalise only for read-heavy, join-expensive workloads.

## Common traps

| Trap | Fix |
|---|---|
| "Repeats data" → not 1NF | 1NF is per cell |
| Partial vs transitive | Part of key vs through attribute |
| Lossless vs dependency preservation | Rows back vs rules enforceable |
| Denormalise a ledger | No — single source of truth |

## Checklist

- [ ] I can recite all four definitions.
- [ ] I know the exact 3NF/BCNF gap.
- [ ] I can check losslessness in one step.
- [ ] I can name the three anomalies.
- [ ] I know when denormalisation is justified.

## Related

- [Normal forms defined](../01-concepts/01-normal-forms-defined.md)
- [Normalization decision procedure](../02-techniques/01-normalization-decision-procedure.md)
- [Solved normalization set](../03-worked-examples/01-solved-normalization-set.md)
- [Normalization traps](../04-pitfalls/01-normalization-traps.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
