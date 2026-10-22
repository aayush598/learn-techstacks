# Normalization Decision Procedure — Classify Any Table in 60 Seconds

> Section 3 · DBMS & SQL · Normalization · _Estimated reading time: 8 min_
> **Prerequisite:** [Normal forms defined](../01-concepts/01-normal-forms-defined.md)

## In one sentence

**Find the key, look for a part-of-key dependency, then look for a through-attribute dependency —
two checks and you can name the highest normal form of any table.**

## Why the pre-test tests this

- "Which normal form is this table in?" is the standard normalization question and it is worth 60
  seconds, not 3 minutes.
- The answer is always the **highest** form the table satisfies, so you must check 1NF → 2NF → 3NF
  in that order and stop at the first failure.
- Ananya's gap is not knowledge, it is that she never learned the **procedure**.

## Core concept

### Procedure 1 — classify a table in 60 seconds

1. **Find the candidate key.** Look for the attribute(s) that determine everything. If the table has
   a single-attribute primary key, write it down and remember: **2NF is automatic**.
2. **Check 1NF.** Is every cell atomic? Any cell with a comma-separated list, or columns like
   `Subject1`/`Subject2`? If yes → the answer is **not 1NF** (or "un-normalized" if there are
   repeating groups).
3. **Check 2NF (only if the key is composite).** For each non-key attribute, ask: does it depend on
   **only part** of the key? If yes → the answer is **1NF**.
4. **Check 3NF.** For each non-key attribute, ask: does it depend on another non-key attribute
   (a chain `A → B → C`)? If yes → the answer is **2NF**.
5. **Check BCNF.** For every non-trivial dependency, is the left-hand side a superkey? If some
   determinant is not a superkey → the answer is **3NF**.
6. **Otherwise** → **BCNF**.

**Stop at the first failure.** The answer is the last form passed.

### Procedure 2 — the key-finding checklist

| Question | If yes |
|---|---|
| Is there a single-attribute primary key declared? | Use it. 2NF is automatic |
| Do two attributes together determine everything? | The key is composite → 2NF matters |
| Does one attribute determine all the others? | Candidate key found |
| Are there two different attributes each of which determines everything? | Two candidate keys — pick one as primary; the others' attributes are **prime** |
| Does every non-key attribute depend on the whole row? | No key found — look harder; the "key" may be a combination |

### Procedure 3 — the dependency chain test

Draw the dependencies as arrows. A **chain** of length 2 or more where the last element is
non-prime is a transitive dependency.

```
Emp_Id ──→ Emp_Name            (direct, fine)
Emp_Id ──→ Dept_Id ──→ Dept_Name    (chain — TRANSITIVE dependency → fails 3NF)
```

| Chain | Verdict |
|---|---|
| `A → B` only | Direct dependency, fine |
| `A → B → C` where C is non-prime | **Transitive** → fails 3NF |
| `A → B → C` where C is prime | Allowed in 3NF, **fails BCNF** |

### Procedure 4 — decide "normal form" vs "highest normal form"

The exam's phrasing matters:

| Phrasing | Answer |
|---|---|
| "Which normal form is this relation in?" | The **highest** form it satisfies |
| "What is the highest normal form of this relation?" | Same |
| "Is this relation in 3NF?" | Yes or no, with the reason |
| "What violates 3NF here?" | Name the transitive dependency |
| "How many normal forms does this satisfy?" | Say "it satisfies 1NF and 2NF" — the count, not the highest |

**Always state both:** "It is in 2NF but not in 3NF" covers both readings.

### Procedure 5 — decompose a table

1. List the FDs you can see.
2. Identify the **partial dependencies** → make one table per key part.
3. Identify the **transitive dependencies** → make one table per determinant.
4. Check **losslessness**: is the shared attribute a key of at least one side?
5. Check **dependency preservation**: is every FD enforceable inside a single table?

### Procedure 6 — the six-question checklist for a decomposition

| # | Question | Good answer |
|---|---|---|
| 1 | Is every relation in 1NF? | Atomic values, no repeating groups |
| 2 | Are the FDs still enforced? | Dependency preservation |
| 3 | Does the join reproduce the original? | Lossless join |
| 4 | Was the redundancy removed? | No repeated facts across rows |
| 5 | Were the anomalies removed? | No insert/update/delete anomalies |
| 6 | Is the number of tables reasonable? | Not over-decomposed into 6 one-column tables |

### Procedure 7 — answer "which normal form" under time pressure

| You see | Answer |
|---|---|
| A cell with `a, b, c` in it | Not 1NF |
| `Subject1, Subject2, Subject3` columns | Not 1NF (repeating group) |
| Composite key + a non-key attribute that depends on half the key | 1NF (fails 2NF) |
| Single key + `Dept_Name` depending on `Dept_Id` depending on the key | 2NF (fails 3NF) |
| Everything depends on the key and nothing chains | 3NF |
| A prime attribute with a dependency on a non-superkey determinant | 3NF (fails BCNF) |

## Worked example

**Q. Given
`STUDENT_COURSE(Student_Id, Course_Id, Student_Name, Course_Name, Grade)`
with FDs: `Student_Id → Student_Name`, `Course_Id → Course_Name`, `(Student_Id, Course_Id) → Grade`.
Which normal form is it in?**

- A. 1NF
- B. 2NF
- C. 3NF
- D. BCNF

**Solution by Procedure 1**

1. **Key:** `(Student_Id, Course_Id)` — composite. 2NF **does** matter here.
2. **1NF:** all values atomic, no repeating groups → ✅ passes.
3. **2NF:** `Student_Name` depends on `Student_Id` **only**; `Course_Name` depends on `Course_Id`
   **only**. Both are **partial dependencies** → ❌ fails 2NF.
4. Stop. The answer is **1NF**.

**Answer: A (1NF).**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| B | 2NF would require no partial dependency. `Student_Name` depends on part of the composite key |
| C | 3NF requires 2NF first. It already fails 2NF |
| D | BCNF requires 3NF first |

**The 2NF fix**

```
STUDENT(Student_Id PK, Student_Name)
COURSE(Course_Id PK, Course_Name)
STUDENT_COURSE(Student_Id, Course_Id, Grade), PK (Student_Id, Course_Id)
```

**Second example — the 3NF test.**

**Q. `EMP(Emp_Id, Emp_Name, Dept_Id, Dept_Name, Dept_Location)` with `Emp_Id → Dept_Id` and
`Dept_Id → Dept_Name, Dept_Location`. Highest normal form?**

- A. 1NF
- B. 2NF
- C. 3NF
- D. BCNF

**Solution**

| Step | Check | Result |
|---|---|---|
| 1NF | Atomic, unique rows | ✅ |
| 2NF | Key `Emp_Id` is single-attribute → automatic | ✅ |
| 3NF | `Emp_Id → Dept_Id → Dept_Name` is a chain, `Dept_Name` is non-prime | ❌ |
| BCNF | `Dept_Id` is a determinant that is not a superkey | ❌ |

**Answer: B (2NF).**

## Quick rules

- Find the key first. Single-attribute key → 2NF is free.
- Check in order: 1NF → 2NF → 3NF → BCNF. Stop at the first failure.
- Partial = depends on **part of the key**. Transitive = depends **through another attribute**.
- A chain of length 2+ ending in a non-prime attribute = transitive.
- 3NF permits prime-attribute dependencies; BCNF does not.
- Say "in 2NF but not in 3NF" — it answers both exam phrasings.
- A good decomposition is lossless and dependency preserving.

## Common traps

| Trap | Fix |
|---|---|
| Calling a table "not 1NF" because values repeat across rows | That is 2NF/3NF territory |
| Checking 3NF before 2NF | Always in order |
| Forgetting 2NF only applies to composite keys | Single key → automatic |
| Calling a prime-attribute dependency a 3NF violation | It is a **BCNF** violation |
| Confusing partial and transitive | "Part of the key" vs "through an attribute" |
| Ignoring losslessness | Check the shared attribute is a key of one side |

## Checklist

- [ ] I can find the candidate key of any table in 30 seconds.
- [ ] I check 1NF → 2NF → 3NF → BCNF in that order.
- [ ] I distinguish partial from transitive dependency.
- [ ] I state the answer as "in X but not in Y" when the form is ambiguous.
- [ ] I check losslessness and dependency preservation for any decomposition.
- [ ] I can name the anomaly that each decomposition fixes.

## Related

- [Normal forms defined](../01-concepts/01-normal-forms-defined.md)
- [Solved normalization set](../03-worked-examples/01-solved-normalization-set.md)
- [Normalization traps](../04-pitfalls/01-normalization-traps.md)
- [Normalization quick check](../05-reference/01-normalization-quick-check.md)
- [Topic overview](../README.md)
- [DBMS & SQL section index](../../README.md)
