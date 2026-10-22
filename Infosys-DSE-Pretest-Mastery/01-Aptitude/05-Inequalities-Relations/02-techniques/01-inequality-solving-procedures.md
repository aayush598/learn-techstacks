# Inequality Solving Procedures — Five Moves

> Section 1 · Aptitude · Inequalities & Relations · _Estimated reading time: 7 min_
> **Prerequisite:** [Inequality symbols and relations](../01-concepts/01-inequality-symbols-and-relations.md)

## In one sentence

Five moves in a fixed order — **split, point, chain, test, counterexample** — solve every inequality
question in the DSE pre-test.

## Why the pre-test tests this

- Inequality questions look symbolic and intimidate candidates who have not seen the format.
- The five moves below are mechanical. You do not need to be "good at logic"; you need to be
  disciplined about order.
- With a 30–45 second budget, this archetype should never cost you more than 1 mark of time.

## Core concept

### The five moves

| # | Move | Action | Time |
|---|---|---|---|
| 1 | **Split** | Break the chain into pairs at every symbol | 5 s |
| 2 | **Point** | Mark which element each sign points at | 5 s |
| 3 | **Chain** | Apply transitivity inside each direction only | 10 s |
| 4 | **Test** | Check each option against the pair list | 10 s |
| 5 | **Counterexample** | For any rejected "always true" claim, produce one counterexample | 10 s |

### Move 1–2 in detail: split and point

```
a > b < n ≥ i < p
```

| Pair | Direction | Pointed-at (smaller) element |
|---|---|---|
| `a > b` | a is above b | b |
| `b < n` | b is below n | b |
| `n ≥ i` | n is at least above i | i |
| `i < p` | i is below p | i |

Output: `b` is the minimum of `{a, b, n}`; `i` is the minimum of `{n, i, p}` (weakly against n).

### Move 3 in detail: chain inside one direction

You may chain `a > b` and `b < n` only if you restate them in the same direction: `a > b` and
`n > b` both say "**b** is below". The conclusion is "b is below both a and n" — **not** "a > n".

| Valid chain | Invalid chain |
|---|---|
| `a > b` and `b > c` ⇒ `a > c` | `a > b` and `b < c` ⇒ `a > c` ❌ |
| `a ≥ b` and `b > c` ⇒ `a > c` | `a > b` and `c < b` ⇒ `a > c` ❌ (direction change) |

### Move 4–5 in detail: test options and kill them

For each option, classify it:

| Class | Meaning | Action |
|---|---|---|
| Directly given | Appears in the chain | Correct answer |
| Structurally implied | Follows from a single-direction chain | Correct answer |
| Unknown | Not implied | Reject — but find a counterexample to be sure |
| Contradicted | Opposite of a given relation | Reject immediately |

**Counterexample recipe.** Build the smallest set of numbers that breaks the claim:

```
Claim: a > n
Counterexample: a=5, b=1, n=9, i=2, p=7   → a=5 < n=9  ✔ claim fails
```

Use small integers (1..9) and always satisfy the original chain while violating the claim. If you
cannot satisfy both, the claim is definitely true.

### The "Statements I and II" procedure

```
Statement I: <claim>
Statement II: <claim>
Options: A. Only I   B. Only II   C. Both   D. Neither
```

| Step | Action |
|---|---|
| 1 | Decode each statement into a relation |
| 2 | Test Statement I against every valid assignment (or prove it structurally) |
| 3 | Do the same for Statement II |
| 4 | Choose Only I / Only II / Both / Neither |

Most "Only II" answers come from a statement that holds **because of** a fact stated in the other
statement. Read the question's given facts before you test the statements.

### The "always vs sometimes" procedure

| Question type | How to answer |
|---|---|
| "Which is always true?" | The one that cannot be broken |
| "Which is sometimes true?" | The one you can satisfy with **one** example |
| "Which is never true?" | The one that contradicts the given facts |

For "always true", try to break each option with a counterexample. The one you cannot break is the
answer. Build the counterexample *before* you read the options' text carefully — the option you
expect is rarely the answer.

## Worked example

**Q. If `a > b ≥ c = d < e ≤ f`, which of the following is definitely true?**

A. `a > f`
B. `c < e`
C. `b > d`
D. `e > f`

**Solution**

| Pair | Relation | Pointed at |
|---|---|---|
| `a > b` | a > b | b |
| `b ≥ c` | b ≥ c | c |
| `c = d` | c = d | both |
| `d < e` | e > d | d |
| `e ≤ f` | f ≥ e | e |

**Test each option**

| Option | Verdict | Reason |
|---|---|---|
| A. `a > f` | Not definite | Example: a=5, b=4, c=3, d=3, e=9, f=9 → a=5 < f=9 |
| B. `c < e` | **Definite** | `c = d` and `d < e` ⇒ `c < e` — one direction, strict link |
| C. `b > d` | Not definite | We only know `b ≥ c = d`, so `b ≥ d`; b could equal d (b=3, c=3, d=3) |
| D. `e > f` | False | The chain says `e ≤ f` |

**Answer: B (`c < e`).**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| A | `a` and `f` are at opposite ends of the chain with no link between them |
| C | `≥` does not upgrade to `>` — equality is allowed |
| D | Directly contradicts `e ≤ f` |

**Second example — Statements I and II.**

**Q. Which of the following statements is/are true?**
I. If `x > y`, then `x + 1 > y`.
II. If `x > y`, then `x > y + 1`.

A. Only I
B. Only II
C. Both
D. Neither

**Solution**

- Statement I: adding 1 to the larger side keeps it larger. **Always true.**
- Statement II: `x > y` does not promise a gap of more than 1. Counterexample: x = 5.5, y = 5 →
  5.5 > 5 is true, but 5.5 > 6 is false. **Not always true.**

**Answer: A (Only I).**

## Quick rules

- Split into pairs; then point; then chain; then test; then counterexample.
- The sign points at the smaller element.
- Chain only within one direction.
- `≥` + `>` ⇒ `>`; `≥` + `≥` ⇒ `≥`; `>` + `>` ⇒ `>`.
- Equality breaks strict chains: `b ≥ c = d` gives `b ≥ d`, not `b > d`.
- To reject an "always true" option, produce a small counterexample that still satisfies the chain.
- Maxima require domination over *every* other element.
- 30–45 seconds.

## Common traps

| Trap | Effect | Fix |
|---|---|---|
| Chaining across a direction change | Concludes `a > n` | Split into pairs first |
| Upgrading `≥` to `>` | Claims `b > d` | Keep the weak link |
| Missing a definitely-true option | You pick a "probably true" one | Check every pair |
| Accepting an option without a counterexample | You never prove your rejection | Build one |
| Assuming the pointed-at element is the global min | Wrong when there are two peaks | It is the min of its neighbours only |
| Decoding the code symbol wrongly | Whole question lost | Decode first |

## Checklist

- [ ] I split the chain into pairs before judging options.
- [ ] I marked which element each sign points at.
- [ ] I applied transitivity only within one direction.
- [ ] I kept `≥` and `>` distinct.
- [ ] I produced a counterexample for every option I rejected.
- [ ] I finished inside 45 seconds.

## Related

- [Inequality symbols and relations](../01-concepts/01-inequality-symbols-and-relations.md)
- [Solved inequality and relations set](../03-worked-examples/01-solved-inequality-set.md)
- [Inequality traps](../04-pitfalls/01-inequality-traps.md)
- [Inequality one-pager](../05-reference/01-inequality-one-pager.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
