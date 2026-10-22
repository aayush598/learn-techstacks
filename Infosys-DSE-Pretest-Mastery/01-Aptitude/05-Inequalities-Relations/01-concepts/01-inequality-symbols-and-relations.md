# Inequalities and Relations — Reading Symbols

> Section 1 · Aptitude · Inequalities & Relations · _Estimated reading time: 8 min_
> **Prerequisite:** [Ranking and Ordering](../../04-Ranking-Ordering/README.md)

## In one sentence

An inequality question gives you a **chain of symbols** and asks which relation is forced — and every
relation is decided by reading the chain, never by guessing.

## Why the pre-test tests this

- The DSE pre-test's aptitude section often carries **1 inequality/relation question**, usually a
  chain like `a > b < n ≥ i < p` with four options, one of which is definitely true.
- It looks hard and takes 20 seconds. It is the best value-per-second archetype in the paper.
- The failures are always the same: transitivity applied across a direction change, or `>` confused
  with `≥`.

## Core concept

### The symbol vocabulary

| Symbol | Meaning | Transitivity |
|---|---|---|
| `>` | strictly greater than | `a > b` and `b > c` ⇒ `a > c` |
| `<` | strictly less than | `a < b` and `b < c` ⇒ `a < c` |
| `≥` | greater than or equal to | `a ≥ b` and `b ≥ c` ⇒ `a ≥ c` |
| `≤` | less than or equal to | `a ≤ b` and `b ≤ c` ⇒ `a ≤ c` |
| `=` | equal to | `a = b` and `b = c` ⇒ `a = c` |

**Mixed chains weaken the conclusion:** `a ≥ b` and `b > c` ⇒ `a > c` (still strict, because one link
is strict). But `a > b` and `b ≥ c` ⇒ `a > c` as well. Only when **both** links are non-strict
(`≥`, `≥`) is the result non-strict (`≥`).

### Decoding `a > b < n ≥ i < p`

Read the chain left to right and split it into pairs:

```
a > b < n ≥ i < p
```

| Pair | Gives | Plain English |
|---|---|---|
| `a > b` | a > b | a is bigger than b |
| `b < n` | n > b | n is bigger than b |
| `n ≥ i` | n ≥ i | n is at least as big as i |
| `i < p` | p > i | p is bigger than i |

**The "point points to the smaller" rule.** In a chain the signs point at the smaller value: in
`a > b < n`, both `>` and `<` point at `b`, so **b is smaller than both a and n**. Likewise in
`n ≥ i < p`, both signs point at `i`, so **i is at most n and strictly smaller than p**.

So the chain tells you:

- `b` is the minimum of `{a, b, n}`.
- `i` is at most `n` and strictly less than `p`.
- `p > i` and `n ≥ i` — but nothing links `p` and `n`, and nothing links `a` and `n`.

### What is "definitely true"?

| Kind | Example from the chain | Why |
|---|---|---|
| Directly given | `a > b`, `n ≥ i`, `p > i` | Stated in the question |
| Implied by transitivity | `b ≤ n`? no — but `i ≤ n` is given | One direction, one pass |
| Minimum identification | `b` is smaller than both `a` and `n` | Both signs point at `b` |
| Maximum identification | Not available here — no element is pointed at by two signs from both sides | — |

**Rule for maxima:** an element is the maximum only if it is greater than **every** other element
mentioned. In `a > b < n ≥ i < p`, nothing qualifies — `a` is only known to beat `b`, and `p` is only
known to beat `i`.

### Coded relations

Sometimes the symbols are defined for you:

> "In the following, `p # q` means p is greater than q, and `p @ q` means p is at most q."

Decode first, then solve as a normal inequality chain. A coding layer never changes the logic; it only
adds 15 seconds of reading.

### Two other standard formats

**Format A — "Which of the following statements is/are true?"**

```
Statement I: <a claim>
Statement II: <another claim>
A. Only I    B. Only II    C. Both    D. Neither
```

Test each statement against every possible assignment of the variables.

**Format B — "Always true" vs "sometimes true"**

| Label | Meaning | Test |
|---|---|---|
| Always true | Holds for every valid assignment | Try to find a counterexample; if none exists → always true |
| Sometimes true | Holds for at least one assignment | Construct one example |
| Never true | Contradicts the given relations | — |

To disprove an "always true" claim you need **one** counterexample. To prove it, you need the
relation to follow structurally from the chain.

## Worked example

**Q. If `a > b < n ≥ i < p`, which of the following is definitely true?**

A. `a > n`
B. `b < i`
C. `p > i`
D. `n > p`

**Solution**

Split the chain: `a > b`, `b < n`, `n ≥ i`, `i < p`.

| Option | Verdict | Reason |
|---|---|---|
| A. `a > n` | Not definite | Nothing links `a` and `n`. Example: a=5, b=1, n=9, i=2, p=7 → a < n |
| B. `b < i` | Not definite | Example: a=5, b=4, n=6, i=3, p=9 → b > i |
| C. `p > i` | **Definite** | Stated directly by `i < p` |
| D. `n > p` | Not definite | Example: a=5, b=1, n=6, i=2, p=9 → n < p |

**Answer: C (`p > i`).**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| A | The chain has a direction change at `b`; nothing relates `a` and `n` |
| B | `b` is only known to be below `a` and `n`; `i` floats |
| D | `n ≥ i` and `p > i` leave `n` and `p` unrelated |

**Time: 25 seconds.** Split the chain, read off the pairs, and test each option against the pairs.

## Quick rules

- Split the chain into pairs at every symbol; work from the pairs, not from the whole line.
- **The sign points at the smaller value.** Two signs pointing at one element ⇒ that element is the
  minimum of its neighbours.
- Transitivity runs in **one direction only**. Never chain across a direction change.
- `>` combined with `≥` still gives a strict `>`; `≥` with `≥` gives `≥`.
- An element is the **maximum** only if it dominates every other element mentioned.
- To disprove an "always true" claim, produce **one** counterexample.
- To disprove a "sometimes true" claim, show it can never hold.
- 30 seconds per inequality question. If you are drawing value tables, you are overthinking it.

## Common traps

| Trap | Symptom | Fix |
|---|---|---|
| Chaining across `>` then `<` | You conclude `a > n` | Direction change breaks transitivity |
| Treating `≥` as `>` | You conclude a strict relation from a non-strict one | Keep the strictness |
| Assuming `b` is the smallest overall | You pick `b` as the global minimum | `b` is smallest only among a, b, n |
| Forgetting `i ≤ n` | You miss a definitely-true option | Read every pair |
| Testing "always true" with one example | You accept a claim that only holds in your sample | One example proves "sometimes", not "always" |
| Decoding the code incorrectly | Everything downstream is wrong | Decode first, then solve |

## Checklist

- [ ] I split the chain into pairs before answering anything.
- [ ] I identified which element each pair points at.
- [ ] I checked each option against the pairs, one at a time.
- [ ] I never applied transitivity across a direction change.
- [ ] I kept strict and non-strict relations distinct.
- [ ] I produced a counterexample for every "definitely true" claim I rejected.
- [ ] I finished inside 30–45 seconds.

## Related

- [Inequality solving procedures](../02-techniques/01-inequality-solving-procedures.md)
- [Solved inequality and relations set](../03-worked-examples/01-solved-inequality-set.md)
- [Inequality traps](../04-pitfalls/01-inequality-traps.md)
- [Inequality one-pager](../05-reference/01-inequality-one-pager.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
