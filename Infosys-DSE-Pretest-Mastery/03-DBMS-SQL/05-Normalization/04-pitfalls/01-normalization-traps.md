# Normalization Traps — Where Candidates Lose the Mark

> Section 3 · DBMS & SQL · Normalization · _Estimated reading time: 5 min_
> **Prerequisite:** [Normal forms defined](../01-concepts/01-normal-forms-defined.md)

## In one sentence

Ten traps, each one a specific confusion between partial and transitive, 3NF and BCNF, and
normalization and denormalization.

## Why the pre-test tests this

- Normalization distractors are **designed** around these ten confusions. They are not random.
- Every trap below is worth losing 1 mark — and normalization is only 1–2 marks to begin with.

## Core concept

### Trap 1 — "It repeats data, so it is not 1NF"

**The claim:** the same value appearing in many rows breaks 1NF.

**The truth:** 1NF is about a **single cell** and a **repeating group of columns**. The same value
in different rows is normal data, not a 1NF violation. The `Sales` string appearing in three
employee rows does not make the table un-normalized in 1NF terms.

**The exam tell:** the option says "not in 1NF because data is repeated". The table is in 1NF and
probably in 2NF or 3NF.

### Trap 2 — Partial vs transitive swapped

| Dependency | Type | Phrase |
|---|---|---|
| `Emp_Id → Emp_Name` in key `(Emp_Id, Proj_Id)` | **Partial** | Depends on **part of the key** |
| `Emp_Id → Dept_Id → Dept_Name` | **Transitive** | Depends **through another attribute** |

Both are "a non-key attribute depends on something other than the whole key", which is why they get
swapped. Fix it by asking: **is the thing it depends on part of the candidate key?**
Yes → partial. No → transitive.

### Trap 3 — 2NF claimed for a composite key

2NF only has content when the candidate key is composite. A table with key `Emp_Id` that has a
transitive dependency is **in 2NF** — not "not in 2NF". Many candidates say "it violates 2NF" when
the real failure is 3NF.

### Trap 4 — 3NF vs BCNF

- **3NF:** for every non-trivial FD `X → A`, `X` is a superkey **or** `A` is prime.
- **BCNF:** for every non-trivial FD `X → A`, `X` is a superkey. Always.

So if a dependency's right-hand side is a **prime attribute**, the table passes 3NF and fails BCNF.
The only gap between the two forms is exactly this case.

### Trap 5 — "The primary key is the only candidate key"

A relation can have several candidate keys. `EMP_PROJECT` with unique project names has two:
`(Emp_Id, Proj_Id)` and `(Emp_Id, Proj_Name)`. Attributes in **any** candidate key are **prime** —
and primality is what separates 3NF from BCNF.

### Trap 6 — Treating "prime attribute" as "primary key attribute"

Primary key is the one you **chose**. Prime is **all** attributes that appear in some candidate
key. They are often different sets.

### Trap 7 — Confusing lossless join with dependency preservation

| Property | Question it answers | Test |
|---|---|---|
| **Lossless** | Do I get the original rows back? | Shared attributes are a key of at least one side |
| **Dependency preserving** | Can I still enforce the rules? | Every FD lives inside one table |

They are independent. A decomposition can be lossless but lose dependency preservation, and the
reverse.

### Trap 8 — Denormalisation as a cure for bad design

Denormalisation is a **performance** decision made **after** the schema is correct. It is not a
substitute for normalisation and it does not remove the anomalies by magic — it converts them into
application-level or trigger-level responsibilities.

### Trap 9 — Denormalisation for a write-heavy system

The justification for denormalisation is **read-heavy, join-expensive** workloads: reporting,
dashboards, data warehouses. A transaction-processing ledger or a stock-count system needs
normalisation and single-source-of-truth, because the cost of inconsistency is higher than the cost
of the join.

### Trap 10 — Assuming decomposition always reduces the table count productively

Decomposing into tiny tables is not the goal. A good decomposition is **lossless**, **dependency
preserving**, and **no more granular than needed**. Splitting `EMP` into `EMP_NAME` and
`EMP_SAL` creates two extra joins to save nothing — the anomalies were already fixed by the
`DEPT` split.

### Bonus trap — "3NF is the highest form"

BCNF exists. A table can be in 3NF and not in BCNF, and the exam will offer "BCNF" as an option
precisely to test whether you know the difference.

## Worked example

**Q. `EMP(Emp_Id, Emp_Name, Dept_Id, Dept_Name)` with `Emp_Id → Dept_Id` and `Dept_Id → Dept_Name`.
Which statement is TRUE?**

- A. It violates 2NF because `Dept_Name` depends on only part of the key
- B. It violates 3NF because `Dept_Name` is transitively dependent on `Emp_Id`
- C. It is in 1NF only, because the key is composite
- D. It is in BCNF because every determinant determines the primary key

**Solution**

The key is `Emp_Id` — **single attribute**. So there is no composite key, so there is no partial
dependency, so 2NF holds. The chain `Emp_Id → Dept_Id → Dept_Name` with `Dept_Name` non-prime is a
transitive dependency, which is exactly what 3NF forbids.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | There is no composite key, so partial dependency is impossible. The dependency is transitive, not partial |
| C | The key `Emp_Id` is single-attribute, not composite. And the table satisfies 2NF |
| D | `Dept_Id` is a determinant that does **not** determine `Emp_Id`. BCNF requires every determinant to be a superkey |

## Quick rules

- 1NF is about **one cell**, not about repeating values across rows.
- Partial = part of the key. Transitive = through another attribute.
- A single-attribute key makes 2NF automatic.
- 3NF allows prime-attribute dependencies; BCNF does not.
- Prime ≠ primary.
- Lossless and dependency preserving are two different properties.
- Denormalise for read-heavy, join-expensive workloads only.

## Common traps

| Trap | The tell in the option |
|---|---|
| Calling repeating data "not 1NF" | The option justifies 1NF failure by "repetition" |
| Swapping partial and transitive | The option names the wrong dependency type |
| 3NF vs BCNF | The option says "prime attribute" |
| Lossless vs dependency preserving | The option talks about FDs for a lossless question |
| Denormalisation as a cure | The scenario is write-heavy or consistency-critical |

## Checklist

- [ ] I can tell partial from transitive without hesitating.
- [ ] I know a single-attribute key makes 2NF automatic.
- [ ] I know the exact gap between 3NF and BCNF.
- [ ] I know prime ≠ primary.
- [ ] I can give a legitimate and an illegitimate denormalisation example.
- [ ] I never decompose further than the anomalies require.

## Related

- [Normal forms defined](../01-concepts/01-normal-forms-defined.md)
- [Normalization decision procedure](../02-techniques/01-normalization-decision-procedure.md)
- [Solved normalization set](../03-worked-examples/01-solved-normalization-set.md)
- [Normalization quick check](../05-reference/01-normalization-quick-check.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
