# Normal Forms Defined — 1NF, 2NF, 3NF and BCNF

> Section 3 · DBMS & SQL · Normalization · _Estimated reading time: 10 min_
> **Prerequisite:** [DBMS theory: schema, keys and indexes](../07-DBMS-Theory-Keys-Indexes-Views/01-concepts/01-schema-keys-and-indexes.md)

## In one sentence

**1NF = atomic values, 2NF = no partial dependency, 3NF = no transitive dependency, BCNF = every
determinant is a key** — four definitions, and the whole archetype is worth 1–2 questions.

## Why the pre-test tests this

- Normalization is 1–2 of the 10 DBMS questions and is the **cheapest** archetype in the section:
  definitions, no computation.
- The exam almost always asks one of three things: "which normal form is this table in?", "what is a
  partial dependency?", or "what does 3NF remove?".
- Ananya can get these right with 20 minutes of reading. She does not because she skips them.

## Core concept

### 1. The vocabulary you must be able to use

| Term | Definition | Example |
|---|---|---|
| **Functional dependency** `X → Y` | If two rows agree on `X`, they must agree on `Y` | `Emp_Id → Emp_Name` |
| **Trivial dependency** `X → Y` where `Y ⊆ X` | Always true, no constraint | `Emp_Id → Emp_Id` |
| **Non-trivial dependency** | `Y ⊄ X` | `Emp_Id → Emp_Name` |
| **Superkey** | A set of attributes that determines **all** attributes of the relation | `{Emp_Id, Proj_Id}` |
| **Candidate key** | A **minimal** superkey | `{Emp_Id, Proj_Id}` |
| **Primary key** | The candidate key you chose | `Emp_Id` |
| **Prime attribute** | Appears in **some** candidate key | `Emp_Id`, `Proj_Id` |
| **Non-prime attribute** | Appears in **no** candidate key | `Emp_Name`, `Hours_Worked` |
| **Partial dependency** | A non-prime attribute depends on **part** of a composite candidate key | `Emp_Name ← Emp_Id` in key `(Emp_Id, Proj_Id)` |
| **Transitive dependency** | `A → B` and `B → C` where `C` is non-prime and `B` is not a superkey | `Emp_Id → Dept_Id → Dept_Name` |

**How to read `X → Y`:** "X functionally determines Y." If you know `X`, you know `Y` without
looking at the rest of the row.

### 2. 1NF — First Normal Form

**Requirements**

1. Every attribute holds a **single atomic (indivisible) value**.
2. **No repeating groups** — no cell containing a list, no set of columns like `Subject1`,
   `Subject2`, `Subject3`.
3. **Each row is unique** — the relation has a key.
4. (Commonly added) Each column holds values of **one data type**.

**What 1NF removes:** repeating groups and multi-valued cells.

| Not 1NF | 1NF |
|---|---|
| `Emp_Name = 'Ananya', Projects = 'P1, P2, P3'` | Three separate rows, one per project |
| `Emp_Id, Skill1, Skill2` (a fixed number of skill columns) | `EMP_SKILL(Emp_Id, Skill)` |
| `Phone = '98765, 91234'` | `EMP_PHONE(Emp_Id, Phone)` |

**What 1NF does NOT remove:** repeated data across rows. Two rows both saying `Sales` for a
department is still fine in 1NF — that redundancy is what 2NF and 3NF attack.

### 3. 2NF — Second Normal Form

**Requirement:** 1NF **+** no non-prime attribute is **partially dependent** on any candidate key.

- Only relevant when a candidate key is **composite** (two or more attributes).
- With a single-attribute key, 2NF adds nothing — every dependency is on the whole key.

**Partial dependency** = a non-prime attribute depends on only **part** of the composite key.

Table `EMP_PROJECT(Emp_Id, Proj_Id, Emp_Name, Hours_Worked)`, key `(Emp_Id, Proj_Id)`:

- `Emp_Name` depends on `Emp_Id` only → **partial dependency** → 2NF violated.
- `Hours_Worked` depends on the **whole** key → fine.

**Fix:** move the partially dependent attributes into a table keyed by that part.

- `EMP(Emp_Id PK, Emp_Name, ...)`
- `EMP_PROJECT(Emp_Id, Proj_Id, Hours_Worked)`, PK `(Emp_Id, Proj_Id)`

**Memory hook:** *2NF = "the whole key, or nothing but the key."*

### 4. 3NF — Third Normal Form

**Requirement:** 2NF **+** no non-prime attribute is **transitively dependent** on any candidate key.

**Transitive dependency:** `A → B` and `B → C`, where `C` is non-prime and `B` is not a superkey.

Table `EMP(Emp_Id PK, Emp_Name, Dept_Id, Dept_Name)`:

- `Emp_Id → Dept_Id` (each employee is in one department)
- `Dept_Id → Dept_Name` (each department has one name)
- Therefore `Emp_Id → Dept_Name` **transitively**, through `Dept_Id`.
- `Dept_Name` is non-prime → 3NF violated.

**Fix:** move `Dept_Name` (and everything that depends only on `Dept_Id`) into its own table.

- `DEPT(Dept_Id PK, Dept_Name, Dept_Location)`
- `EMP(Emp_Id PK, Emp_Name, Dept_Id FK)`

**Memory hook:** *3NF = "the key, the whole key, and nothing but the key" (Codd).*

**Formal version of 3NF:** for every non-trivial FD `X → A`, either `X` is a superkey **or** `A` is
prime.

### 5. BCNF — Boyce-Codd Normal Form

**Requirement:** 3NF **+** every **determinant** (the left-hand side of any non-trivial FD) is a
**superkey**.

The difference between 3NF and BCNF: 3NF allows a dependency `X → A` where `A` is **prime**; BCNF
does not.

**Worked BCNF example:**

`EMP_PROJECT(Emp_Id, Proj_Id, Hours_Worked, Proj_Name)` where project names are unique.

- FDs: `(Emp_Id, Proj_Id) → Hours_Worked`; `Proj_Id → Proj_Name`; `Proj_Name → Proj_Id`
- Candidate keys: `(Emp_Id, Proj_Id)` and `(Emp_Id, Proj_Name)`. Prime attributes: `Emp_Id`,
  `Proj_Id`, `Proj_Name`. Non-prime: `Hours_Worked`.
- **3NF?** Every non-trivial FD `X → A` has `X` a superkey or `A` prime. `Proj_Id → Proj_Name`:
  `Proj_Name` is prime ✅. `Proj_Name → Proj_Id`: `Proj_Id` is prime ✅. → **in 3NF**.
- **BCNF?** `Proj_Name → Proj_Id` has determinant `Proj_Name`, which is **not** a superkey (it
  determines neither `Emp_Id` nor `Hours_Worked`). → **BCNF violated**.

**Fix:** put the project attributes in their own table.

- `PROJECT(Proj_Id PK, Proj_Name UNIQUE)`
- `EMP_PROJECT(Emp_Id, Proj_Id, Hours_Worked)`

**Memory hook:** *BCNF = "every determinant is a key."*

### 6. The normal-form ladder — one table

| Form | Adds | Breaks when | Fix |
|---|---|---|---|
| **UNF** | — | — | — |
| **1NF** | Atomic values, no repeating groups | A cell holds a list | Split the list out |
| **2NF** | No partial dependency | A non-key attribute depends on part of a composite key | Split by that part |
| **3NF** | No transitive dependency | A non-key attribute depends on another non-key attribute | Split that attribute out |
| **BCNF** | Every determinant is a key | A determinant is not a superkey (but the attribute it determines is prime) | Split on the determinant |

### 7. Lossless join and dependency preservation

A decomposition is only a *good* decomposition if it is **lossless** and **dependency
preserving**.

**Lossless join** — the decomposed tables, joined back, reproduce the original relation exactly
(no extra rows, no missing rows).

*Sufficient condition for a binary decomposition `R → R1, R2`:* the shared attributes `R1 ∩ R2` must
be a **key of at least one** of `R1` or `R2`.

| Decomposition | Shared attributes | Key of one side? | Lossless? |
|---|---|---|---|
| `EMP` ∩ `EMP_PROJECT` | `Emp_Id` | Key of `EMP` ✅ | **Yes** |
| `EMP` ∩ `DEPT` | `Dept_Id` | Key of `DEPT` ✅ | **Yes** |

**Dependency preservation** — every FD of the original relation can be enforced by a constraint on
**one** decomposed table, without joining.

| Original FD | Enforced in |
|---|---|
| `Emp_Id → Emp_Name, Emp_Salary` | `EMP` |
| `Dept_Id → Dept_Name, Dept_Location` | `DEPT` |
| `(Emp_Id, Proj_Id) → Hours_Worked` | `EMP_PROJECT` |

All preserved ✅.

### 8. Denormalisation — when repeating data is correct

Normalization is not a religion. Controlled redundancy is correct when:

| Situation | Why denormalisation wins |
|---|---|
| Read-heavy reporting | Joins are expensive; a wide flat table is fast |
| Data warehouse / star schema | Fact and dimension tables deliberately repeat dimension attributes |
| Materialised view / summary table | Pre-computed for a fixed query pattern |
| Derived value stored for convenience | Avoids recomputation on every read |
| Distributed systems | Avoids cross-node joins (replication instead) |

**The rules for denormalisation:** (1) the redundancy is **controlled**, (2) there is a single
"owner" of each fact, (3) the duplication is updated by a trigger or the application, (4) you accept
the anomaly risk knowingly.

### 9. The redundancy trade-off — what each form fixes

| Anomaly | Meaning | Fixed by |
|---|---|---|
| **Insertion anomaly** | You cannot add one fact without adding an unrelated one | 1NF/2NF/3NF decomposition |
| **Deletion anomaly** | Deleting one fact destroys another | 3NF decomposition |
| **Update anomaly** | The same fact lives in many rows and must be updated in all of them | 3NF decomposition |

Concrete: with `EMP(Emp_Id, Emp_Name, Dept_Id, Dept_Name)`, a department cannot be recorded until it
has an employee (insertion anomaly), deleting the last employee of a department deletes the
department (deletion anomaly), and renaming a department means updating every employee row (update
anomaly).

## Worked example

**Q. Consider
`EMP(Emp_Id PK, Emp_Name, Emp_Salary, Dept_Id, Dept_Name, Dept_Location)`.
Which normal form is this relation in?**

- A. 1NF
- B. 2NF
- C. 3NF
- D. BCNF

**Solution**

| Step | Check | Result |
|---|---|---|
| 1NF | All attributes atomic, no repeating groups, key present | ✅ Passes 1NF |
| 2NF | The key `Emp_Id` is a **single** attribute → no composite key → no partial dependency possible | ✅ Passes 2NF |
| 3NF | `Emp_Id → Dept_Id` and `Dept_Id → Dept_Name` / `Dept_Location`, and `Dept_Id` is **not** a superkey, and `Dept_Name`/`Dept_Location` are **non-prime** → **transitive dependency exists** | ❌ Fails 3NF |

**Answer: B (2NF).** The relation satisfies 1NF and 2NF but has a transitive dependency, so it is
**in 2NF but not in 3NF**.

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| A | It satisfies more than 1NF. The key is single-attribute, so 2NF is automatic |
| C | `Dept_Name` is transitively dependent on `Emp_Id` through `Dept_Id`. This is exactly what 3NF forbids |
| D | BCNF requires every determinant to be a superkey. `Dept_Id` is a determinant and it is not a superkey |

**The 3NF fix**

```
DEPT(Dept_Id PK, Dept_Name, Dept_Location)
EMP(Emp_Id PK, Emp_Name, Emp_Salary, Dept_Id FK → DEPT.Dept_Id)
```

## Quick rules

- **1NF:** atomic values, no repeating groups, unique rows.
- **2NF:** no partial dependency (only matters for composite keys).
- **3NF:** no transitive dependency.
- **BCNF:** every determinant is a superkey.
- 3NF allows a prime-attribute dependency; BCNF does not.
- A single-attribute key means 2NF is automatic.
- Good decompositions are **lossless** and **dependency preserving**.
- Denormalisation is correct when reads dominate and the redundancy is controlled.

## Common traps

| Trap | What you get | What you should get |
|---|---|---|
| Confusing 2NF and 3NF | "partial dependency" for a transitive one | Partial = part of the key; transitive = through another attribute |
| Calling a table "not in 1NF" because data repeats | 1NF | Repeating data across rows is 2NF/3NF territory |
| Thinking BCNF = "no transitive dependencies" | BCNF | BCNF is stricter than 3NF |
| Ignoring the composite-key condition | 2NF violation claimed | With a single key, 2NF always holds |
| Calling the primary key the only candidate key | — | Candidate keys can be several; pick one as primary |
| Forgetting lossless join | — | A decomposition that loses rows is not a good decomposition |

## Checklist

- [ ] I can state all four normal forms in one line each.
- [ ] I can identify partial vs transitive dependency from a given table.
- [ ] I know that 2NF only bites with composite keys.
- [ ] I know the difference between 3NF and BCNF (prime attributes).
- [ ] I can check losslessness using the shared-attribute rule.
- [ ] I know the three anomalies and which form fixes them.

## Related

- [Normalization decision procedure](../02-techniques/01-normalization-decision-procedure.md)
- [Solved normalization set](../03-worked-examples/01-solved-normalization-set.md)
- [Normalization traps](../04-pitfalls/01-normalization-traps.md)
- [Normalization quick check](../05-reference/01-normalization-quick-check.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
