# Normalization — 8 Solved Questions

> Section 3 · DBMS & SQL · Normalization · _Estimated reading time: 11 min_
> **Prerequisite:** [Normalization decision procedure](../02-techniques/01-normalization-decision-procedure.md)

## In one sentence

Eight normalization questions — normal-form identification, partial vs transitive, anomalies,
lossless decomposition — each solved by the same 60-second procedure.

## Why the pre-test tests this

- Normalization is 1–2 of the 10 DBMS questions and is the **cheapest** archetype in the section.
- The questions are definitions and classification, not computation. Ten minutes of reading is worth
  2 marks.
- The distractors are built from the classic mix-ups: partial vs transitive, 3NF vs BCNF, and
  "repeating data" vs "repeating groups".

## Core concept

### The procedure, in four questions

```
1. What is the key?               (single → 2NF is automatic)
2. Is any cell non-atomic?        (yes → not 1NF)
3. Does a non-key attribute depend on PART of a composite key?   (yes → 1NF)
4. Does a non-key attribute depend on another non-key attribute? (yes → 2NF)
5. Is every determinant a superkey? (no → 3NF)
```

Stop at the first failure. The answer is the last form passed.

## Worked example

### Q1 — Answer **B** (transitive dependency → 2NF)

**Consider `EMP(Emp_Id, Emp_Name, Emp_Salary, Dept_Id, Dept_Name, Dept_Location)` with FDs
`Emp_Id → Emp_Name, Emp_Salary, Dept_Id` and `Dept_Id → Dept_Name, Dept_Location`.
What is the highest normal form?**

- A. 1NF
- B. 2NF
- C. 3NF
- D. BCNF

**Solution**

| Step | Check | Result |
|---|---|---|
| 1NF | All atomic, no repeating groups | ✅ |
| 2NF | Key `Emp_Id` is single-attribute → no composite key → automatic | ✅ |
| 3NF | `Emp_Id → Dept_Id → Dept_Name`: `Dept_Name` is non-prime and transitively dependent | ❌ |
| BCNF | `Dept_Id` is a determinant and is not a superkey | ❌ |

**Answer: B (2NF).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | It satisfies more than 1NF. The key is single-attribute, so 2NF adds nothing |
| C | `Dept_Name` is transitively dependent on `Emp_Id` through `Dept_Id`. This is precisely what 3NF forbids |
| D | BCNF requires every determinant to be a superkey; `Dept_Id` is not one |

---

### Q2 — Answer **A** (partial dependency → 1NF)

**Consider `STUDENT_COURSE(Student_Id, Course_Id, Student_Name, Course_Name, Grade)` with FDs
`Student_Id → Student_Name`, `Course_Id → Course_Name`, `(Student_Id, Course_Id) → Grade`.
Highest normal form?**

- A. 1NF
- B. 2NF
- C. 3NF
- D. BCNF

**Solution**

| Step | Check | Result |
|---|---|---|
| 1NF | Atomic values | ✅ |
| 2NF | Key is composite `(Student_Id, Course_Id)`. `Student_Name` depends on `Student_Id` only → **partial dependency** | ❌ |

Stop. **Answer: A (1NF).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | 2NF forbids partial dependencies. There are two of them |
| C | 3NF requires 2NF first |
| D | BCNF requires 3NF first |

---

### Q3 — Answer **C** (not 1NF — repeating group)

**Consider `EMP_SKILLS(Emp_Id, Emp_Name, Skill1, Skill2, Skill3)`. What is its normal form?**

- A. 3NF
- B. 2NF
- C. 1NF
- D. Not in 1NF

**Solution**

`Skill1`, `Skill2`, `Skill3` are a **repeating group** — a fixed number of columns standing in for
an unknown number of skills. Atomicity is broken at the table level, not just the cell level.

**Answer: D (not in 1NF).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Every column holds one value, which is what makes it *look* like 1NF. The repeating **group of columns** is what disqualifies it |
| B | Same reason — the form is not even reached |
| C | A repeating group of columns violates 1NF. If the exam means "no repeating group allowed", 1NF is not satisfied |

**The fix:** `EMP_SKILL(Emp_Id, Skill)` with PK `(Emp_Id, Skill)`.

---

### Q4 — Answer **A** (3NF but not BCNF)

**Consider `EMP_PROJECT(Emp_Id, Proj_Id, Hours_Worked, Proj_Name)` where project names are unique.
FDs: `(Emp_Id, Proj_Id) → Hours_Worked`, `(Emp_Id, Proj_Name) → Hours_Worked`,
`Proj_Id → Proj_Name`, `Proj_Name → Proj_Id`.
Highest normal form?**

- A. 3NF
- B. BCNF
- C. 2NF
- D. 1NF

**Solution**

The candidate keys are `(Emp_Id, Proj_Id)` and `(Emp_Id, Proj_Name)`. Prime attributes:
`Emp_Id`, `Proj_Id`, `Proj_Name`. Non-prime: `Hours_Worked`.

| Step | Check | Result |
|---|---|---|
| 1NF | Atomic | ✅ |
| 2NF | `Hours_Worked` depends on the whole key; `Proj_Name` depends on `Proj_Id` (prime, part of key) | ✅ |
| 3NF | `Proj_Id → Proj_Name`: `Proj_Name` is prime → allowed. `Proj_Name → Proj_Id`: `Proj_Id` is prime → allowed | ✅ |
| BCNF | `Proj_Name → Proj_Id`: determinant `Proj_Name` is **not** a superkey (it determines neither `Emp_Id` nor `Hours_Worked`) | ❌ |

**Answer: A (3NF).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | BCNF forbids the dependency `Proj_Name → Proj_Id` because `Proj_Name` is not a superkey |
| C | 2NF is satisfied — no non-prime attribute depends on part of a key |
| D | It satisfies far more than 1NF |

---

### Q5 — Answer **C** (the anomaly)

**In `EMP(Emp_Id, Emp_Name, Dept_Id, Dept_Name)`, what problem occurs when a new department with no
employees is created?**

- A. Update anomaly
- B. Deletion anomaly
- C. Insertion anomaly
- D. No anomaly — the relation is fully normalized

**Solution**

The department's name lives in the **employee** table. To record a department that has no
employees, you must insert an employee row — because `Dept_Name` cannot exist without an
`Emp_Id`. You cannot record the department on its own.

**Answer: C (Insertion anomaly).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | An update anomaly would be renaming a department and having to update every employee row |
| B | A deletion anomaly would be deleting the last employee of a department and thereby losing the department |
| D | The relation is in 3NF? No — it is in 2NF with a transitive dependency, which is exactly what causes the anomaly |

---

### Q6 — Answer **B** (the 3NF decomposition)

**Which decomposition removes the transitive dependency in
`EMP(Emp_Id, Emp_Name, Emp_Salary, Dept_Id, Dept_Name, Dept_Location)` and is lossless?**

- A. `EMP(Emp_Id, Emp_Name)` and `EMP_SAL(Emp_Id, Emp_Salary, Dept_Id, Dept_Name, Dept_Location)`
- B. `DEPT(Dept_Id, Dept_Name, Dept_Location)` and `EMP(Emp_Id, Emp_Name, Emp_Salary, Dept_Id)`
- C. `EMP_NAME(Emp_Id, Emp_Name)` and `EMP_DEPT(Emp_Id, Dept_Id, Dept_Name, Dept_Location)`
- D. `EMP(Emp_Id, Emp_Name, Emp_Salary)` and `DEPT_ALL(Emp_Id, Dept_Id, Dept_Name, Dept_Location)`

**Solution**

The transitive chain is `Emp_Id → Dept_Id → Dept_Name, Dept_Location`. The determinant of the
second link is `Dept_Id`, so `Dept_Name` and `Dept_Location` must move into a table keyed by
`Dept_Id`.

**Losslessness check:** `EMP ∩ DEPT = {Dept_Id}`, and `Dept_Id` is a **key of `DEPT`** → the
decomposition is lossless.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | `Dept_Name` still depends on `Dept_Id` inside `EMP_SAL`, and `Emp_Id` appears there as a non-key attribute → partial dependency and transitive dependency remain |
| C | `Dept_Name` and `Dept_Location` stay with `Emp_Id`, so `Dept_Id → Dept_Name` is still transitive. Also `EMP_DEPT` is keyed by `Emp_Id` alone and the shared attribute `Emp_Id` is not a key of `EMP_NAME`… it is, but the anomaly is still there |
| D | `EMP_ALL` still contains the transitive dependency `Dept_Id → Dept_Name`. Splitting on `Emp_Id` does not address it |

---

### Q7 — Answer **A** (lossless join)

**For a decomposition `R → R1, R2` to be lossless, which condition is sufficient?**

- A. The common attributes `R1 ∩ R2` form a key of at least one of `R1` or `R2`
- B. Every FD of `R` is preserved in `R1` and `R2`
- C. `R1` and `R2` are both in 3NF
- D. `R1` and `R2` have the same number of attributes

**Solution**

Lossless means the join of `R1` and `R2` reproduces `R` exactly. The standard sufficient condition
is that the intersection is a **key of at least one** side — then each tuple in `R` maps to exactly
one tuple in the join.

**Answer: A.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | That is the definition of **dependency preservation**, a different property |
| C | Normal form of the pieces says nothing about whether rows are lost or duplicated on the join |
| D | Irrelevant — the sizes of the pieces are unrelated to losslessness |

---

### Q8 — Answer **C** (denormalisation)

**Which scenario is the strongest justification for denormalisation?**

- A. A banking ledger where every balance must be exactly consistent at all times
- B. A students table where each student's row stores their city, and 500 students share 8 cities
- C. A data warehouse with a fact table that repeats the customer name and region on every row to
  avoid expensive joins at query time
- D. An inventory table where stock levels must never be inconsistent between the shelf and the
  website

**Solution**

Denormalisation is correct when **reads dominate**, the redundancy is **controlled**, and the
cost of joining exceeds the cost of the duplication. A star-schema fact table is the textbook
case.

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | A ledger needs strict consistency — denormalising a balance is how you get drift |
| B | That is exactly the redundancy 3NF removes. Repeating the city 500 times is an update anomaly waiting to happen |
| D | Consistency is the priority — normalise and enforce the invariant in one place |

## Quick rules

- Key first. Single-attribute key → 2NF is automatic.
- 1NF → 2NF → 3NF → BCNF, stop at the first failure.
- Partial = part of the key. Transitive = through another attribute.
- 3NF permits prime-attribute dependencies; BCNF does not.
- Lossless ⟺ the shared attributes form a key of at least one side.
- Dependency preservation ⟺ every FD is enforceable inside one table.
- Say "in 2NF but not in 3NF".

## Common traps

| Trap | Wrong answer | Right answer |
|---|---|---|
| Confusing partial and transitive | B in Q1 | Partial = part of key, transitive = through attribute |
| Calling repeating columns 1NF | C in Q3 | Not in 1NF |
| Calling a prime-attribute dependency a 3NF violation | — | It is a BCNF violation |
| Confusing losslessness with dependency preservation | B in Q7 | Lossless = shared attributes are a key |
| Believing denormalisation fixes everything | D in Q8 | Only for read-heavy, controlled redundancy |

## Checklist

- [ ] I can find the key in 30 seconds.
- [ ] I check the forms in order and stop at the first failure.
- [ ] I can name the anomaly behind each decomposed table.
- [ ] I can check losslessness with the shared-attribute rule.
- [ ] I know the difference between 3NF and BCNF.
- [ ] I can give one legitimate denormalisation example.

## Related

- [Normal forms defined](../01-concepts/01-normal-forms-defined.md)
- [Normalization decision procedure](../02-techniques/01-normalization-decision-procedure.md)
- [Normalization traps](../04-pitfalls/01-normalization-traps.md)
- [Normalization quick check](../05-reference/01-normalization-quick-check.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
