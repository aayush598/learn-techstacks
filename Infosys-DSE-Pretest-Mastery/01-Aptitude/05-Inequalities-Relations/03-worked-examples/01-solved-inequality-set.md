# Inequalities and Relations — 10 Solved Questions

> Section 1 · Aptitude · Inequalities & Relations · _Estimated reading time: 11 min_
> **Prerequisite:** [Inequality solving procedures](../02-techniques/01-inequality-solving-procedures.md)

## In one sentence

Ten questions built on symbol chains — each solved by splitting the chain, pointing at the smaller
element, and killing the wrong options with one counterexample.

## Why the pre-test tests this

- Inequality/relation questions are 1 of the 10 aptitude questions and are worth banking in under a
  minute.
- The set below covers every format you will meet: a plain chain, a "minimum/maximum" question, an
  "always vs sometimes" question, a coded relation, a Statements-I-and-II question, and an algebraic
  version.
- Correct answers are spread across all four option positions on purpose, so a guessing pattern
  cannot carry you.

## Core concept

The single habit that solves all ten:

> **Split the chain into pairs, mark the element each sign points at, and test each option against
> those pairs.**

## Worked example

### Q1 — Answer **B** (transitivity within one direction)

**If `x > y ≥ z < w ≤ v`, which of the following is definitely true?**

A. `x > v`
B. `x > z`
C. `y > z`
D. `w < v`

**Solution**

| Pair | Relation | Pointed at |
|---|---|---|
| `x > y` | x > y | y |
| `y ≥ z` | y ≥ z | z |
| `z < w` | w > z | z |
| `w ≤ v` | v ≥ w | w |

- **B**: `x > y` and `y ≥ z` → `x > z`. One direction, strict link → definitely true. ✅
- **A**: no link between x and v. Counterexample: x=5, y=4, z=3, w=6, v=7 → x=5 < v=7.
- **C**: `y ≥ z` allows y = z (y=3, z=3) → not definite.
- **D**: `w ≤ v` allows w = v → not definite.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | No chain links x and v |
| C | `≥` is not `>` |
| D | `≤` is not `<` |

---

### Q2 — Answer **C** (minimum identification)

**If `x > y` and `y < z`, which of the following is definitely true?**

A. x is the largest of the three.
B. z is the largest of the three.
C. y is smaller than both x and z.
D. x > z.

**Solution**: Both signs point at `y`, so y is below x and below z. The chain `x > y < z` gives no
information about x versus z.

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | x could be smaller than z |
| B | z could be smaller than x |
| D | Not determined — the chain changes direction at y |

---

### Q3 — Answer **D** (strict link upgrades a weak one)

**If `p ≥ q > r ≥ s`, which of the following is definitely true?**

A. `p > q`
B. `q = r`
C. `r > s`
D. `p > s`

**Solution**

- `p ≥ q` and `q > r` ⇒ `p > r` (one strict link upgrades the result).
- `p > r` and `r ≥ s` ⇒ `p > s`. ✅
- `p > q` is **not** definite: p = q = 5, q > r = 3, r ≥ s = 1 satisfies the chain.
- `q = r` contradicts `q > r`.
- `r > s` is not definite: r = s = 1 satisfies `r ≥ s`.

**Answer: D (`p > s`).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | `p ≥ q` allows p = q |
| B | Contradicts `q > r` |
| C | `r ≥ s` allows r = s |

---

### Q4 — Answer **C** (always true vs sometimes true)

**If `a > b`, which of the following is sometimes true but not always true?**

A. `a > b`
B. `a + 1 > b`
C. `a > b + 1`
D. `a − b > 0`

**Solution**

- A: restates the given → always true.
- B: `a > b` ⇒ `a + 1 > b + 1 > b` → always true.
- D: `a > b` ⇒ `a − b > 0` → always true.
- C: needs the gap to exceed 1. Sometimes true (a = 5, b = 3), not always (a = 5, b = 4.5). ✅

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Always true |
| B | Always true |
| D | Always true |

---

### Q5 — Answer **D** (coded relations)

**In the following, `x > y` means x scored more marks than y. Rahul > Ananya, Meera > Ananya and
Karthik > Ananya. Who scored the least?**

A. Karthik
B. Meera
C. Rahul
D. Ananya

**Solution**: All three signs point at Ananya, so Ananya is below everyone else.

**Answer: D (Ananya).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A, B, C | Each is above Ananya; nothing tells you the order among them |

---

### Q6 — Answer **A** (Statements I and II)

**Which of the following statements is/are true?**
I. If `a > b` and `b > c`, then `a > c`.
II. If `a > b` and `c > b`, then `a > c`.

A. Only I
B. Only II
C. Both
D. Neither

**Solution**

- **I**: transitivity → always true. ✅
- **II**: counterexample — a = 1, b = 0, c = 5. Both `a > b` and `c > b` hold, but `a > c` is false
  (1 > 5 is false). Not always true.

**Answer: A (Only I).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | II fails on the counterexample above |
| C | II is not always true |
| D | I is always true |

---

### Q7 — Answer **B** (chain with numbers)

**Meera scored 50 marks. Rahul scored 5 more than Meera. Ananya scored 8 more than Rahul. Karthik
scored 3 less than Meera. Divya scored 40 marks. How many marks did Ananya score?**

A. 58
B. 63
C. 68
D. 45

**Solution**

```
Meera   = 50
Rahul   = 50 + 5  = 55
Ananya  = 55 + 8  = 63
Karthik = 50 − 3  = 47
Divya   = 40
```

**Answer: B (63).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 58 | 50 + 8 — applied Ananya's lead to Meera instead of Rahul |
| 68 | 50 + 5 + 8 + 5 — added Rahul's lead twice |
| 45 | 50 − 5 — subtracted instead of adding |

---

### Q8 — Answer **C** (ordering with names)

**Ananya scored more than Rahul. Meera scored less than Ananya. Rahul scored less than Meera. Who
scored the least?**

A. Ananya
B. Meera
C. Rahul
D. Cannot be determined

**Solution**

```
Rahul < Meera < Ananya
```

**Answer: C (Rahul).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | The highest |
| B | In the middle |
| D | The chain is fully determined — the middle statement connects both ends |

---

### Q9 — Answer **A** (equality inside a chain)

**If `p = q` and `q > r > s`, which of the following is definitely true?**

A. `p > r`
B. `p > q`
C. `s > r`
D. `r > q`

**Solution**: `p = q` and `q > r` ⇒ `p > r`. ✅

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | `p = q` exactly |
| C | Contradicts `r > s` |
| D | Contradicts `q > r` |

---

### Q10 — Answer **D** (algebraic always-true)

**If `x + 3 > 10`, which of the following is definitely true?**

A. `x > 10`
B. `x = 7`
C. `x < 7`
D. `x > 7`

**Solution**: `x + 3 > 10` ⇒ `x > 10 − 3 = 7`. ✅

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | x could be 8 — that satisfies the given but not this claim |
| B | x = 7 fails the strict inequality `x + 3 > 10` (7 + 3 = 10 is not > 10) |
| C | The opposite of the truth |

## Quick rules

- Split into pairs; point at the smaller element; test each option.
- Chain only within one direction.
- A strict link upgrades a weak relation to strict: `≥` + `>` ⇒ `>`.
- Equality kills strictness: `b ≥ c = d` ⇒ `b ≥ d`, not `b > d`.
- One counterexample rejects an "always true" claim.
- One valid example proves a "sometimes true" claim.
- Decode coded symbols before you reason.
- 30–45 seconds.

## Common traps

| Trap | Seen in | Silently gives |
|---|---|---|
| Chaining across a direction change | Q1 | `x > v` |
| Reading `≥` as `>` | Q1, Q3 | `y > z`, `p > q` |
| Assuming a global minimum | Q2 | "x is the largest" |
| Accepting a "sometimes" option as always true | Q4 | option B |
| Assuming the order among elements that share a sign | Q5 | any of the three |
| Not testing a statement for a counterexample | Q6 | "Both" |
| Applying a gap to the wrong person | Q7 | 58 |
| Reading "cannot be determined" without trying | Q8 | option D |

## Checklist

- [ ] I split every chain into pairs before judging options.
- [ ] I built a counterexample for every "definitely true" option I rejected.
- [ ] I got Q3 and Q6 right — strictness and the Statements-I-and-II format are the two that cost marks.
- [ ] I finished all 10 in 11 minutes or less.

## Related

- [Inequality symbols and relations](../01-concepts/01-inequality-symbols-and-relations.md)
- [Inequality solving procedures](../02-techniques/01-inequality-solving-procedures.md)
- [Inequality traps](../04-pitfalls/01-inequality-traps.md)
- [Inequality one-pager](../05-reference/01-inequality-one-pager.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
