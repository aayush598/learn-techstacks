# Inequality Traps — Wrong Turns and How to Catch Them

> Section 1 · Aptitude · Inequalities & Relations · _Estimated reading time: 6 min_
> **Prerequisite:** [Inequality solving procedures](../02-techniques/01-inequality-solving-procedures.md)

## In one sentence

Every inequality trap is a **direction mistake or a strength mistake** — you chained across a `>` that
turned into `<`, or you upgraded a `≥` into a `>`.

## Why the pre-test tests this

- Inequality questions are short and look technical, so candidates over-think them and lose time.
- The options are engineered around exactly two mistakes: wrong direction, wrong strength.
- Once you name the mistake, the option becomes obviously wrong — and the question takes 30 seconds.

## Core concept

### The eight traps

| # | Trap | Typical wrong conclusion | Fix |
|---|---|---|---|
| 1 | Chaining across a direction change | `a > c` from `a > b < c` | Split into pairs first |
| 2 | Upgrading `≥` to `>` | `b > d` from `b ≥ d` | Keep the weak link |
| 3 | Downgrading `>` to `≥` | "always true" claims that are strict | Strictness matters |
| 4 | Assuming a global minimum/maximum | "b is the smallest overall" | It is the smallest only of its neighbours |
| 5 | One example proving "always" | Accepting a claim that held in one case | One counterexample rejects |
| 6 | Confusing "always" and "sometimes" | Picking an option that is merely possible | Read the question stem twice |
| 7 | Mis-decoding the symbols | Whole question lost | Decode before reasoning |
| 8 | Missing a second true option | Answer key says B, you found C | Re-read `≥`/`>` and equality |

### The direction-change rule, drawn

```
a > b < c
```

| What you may conclude | What you may NOT |
|---|---|
| b < a | a > c ❌ |
| b < c | c > a ❌ |
| b is smaller than both a and c | b is the smallest overall ❌ (other variables may be smaller) |

```
a > b > c
```

| What you may conclude | What you may NOT |
|---|---|
| a > b, b > c | — |
| a > c ✅ (transitivity) | — |

### The strength rule, tabulated

| Link 1 | Link 2 | Conclusion |
|---|---|---|
| `>` | `>` | `>` |
| `>` | `≥` | `>` |
| `≥` | `>` | `>` |
| `≥` | `≥` | `≥` |
| anything | `=` | copy the `=` |
| `=` | anything | copy the other relation |

If **any** link in the chain is strict, the conclusion is strict.

## Worked example

**Q. If `a > b < n ≥ i < p`, which of the following is definitely true?**

A. `a > n`
B. `b < i`
C. `p > i`
D. `n > p`

**The trap in option A.** The chain looks like a sequence you can chain end to end: `a > b`, `b < n`,
`n ≥ i`, `i < p`. A candidate who reads it as "a is above b, b is below n, n is at least i, i is
below p" and then tries to build one descending run gets `a > n` — which is **not** a valid chain,
because the direction changes at `b` and at `i`.

**Proof that A is not definite:** take a = 5, b = 1, n = 9, i = 2, p = 7.
Chain check: 5 > 1 ✓, 1 < 9 ✓, 9 ≥ 2 ✓, 2 < 7 ✓. But a = 5 < n = 9 → `a > n` is false.

**The trap in option D.** `n ≥ i` and `p > i` put both n and p *above* i, but say nothing about n
versus p. Proof: n = 6, p = 9 (with a = 5, b = 1, i = 2) satisfies the chain and gives n < p.

**The correct reasoning**

| Option | Status |
|---|---|
| A. `a > n` | Direction change — no chain links a and n |
| B. `b < i` | Not definite: b = 4, i = 3, a = 5, n = 6, p = 9 satisfies the chain with b > i |
| C. `p > i` | **Given directly** by `i < p` |
| D. `n > p` | Not definite — see above |

**Answer: C (`p > i`).**

**Second example — the "always" trap.**

**Q. If `x + 3 > 10`, which is definitely true? A. `x > 10` B. `x = 7` C. `x < 7` D. `x > 7`**

You might reason: "x + 3 > 10, so x is definitely more than 10 − 3 = 7, but is it *more* than 7 or
could it equal 7?" The inequality is strict, so x > 7 exactly. **Answer: D.**

The trap is option B, `x = 7`: many candidates write `x ≥ 7` in their head, then see `x = 7` and
think it might also be allowed. It is not — the given inequality is strict.

## Quick rules

- Split into pairs. Never chain across a direction change.
- The sign points at the smaller value.
- One strict link makes the whole conclusion strict.
- Equality in the chain kills strictness.
- Reject an "always true" option by producing one counterexample that still satisfies the chain.
- A "sometimes true" option needs one valid example.
- Decode the symbols first.
- 30–45 seconds.

## Common traps

| Trap | Wrong answer | Right answer |
|---|---|---|
| Chaining `a > b < c` | `a > c` | Only `b < a` and `b < c` |
| `≥` upgraded | `b > d` | `b ≥ d` |
| `>` downgraded | "maybe" | `>` is strict — always strict |
| Global minimum assumed | "b is the smallest" | smallest of its neighbours only |
| One example proves always | accepting a claim | you need a counterexample to reject |
| Always vs sometimes mixed up | a merely-possible option | read the stem's exact wording |
| Code mis-decoded | everything | decode first |
| Second true option missed | wrong key | re-read the `≥`/`=` details |

## Checklist

- [ ] I split every chain into pairs before judging options.
- [ ] I never chained across a direction change.
- [ ] I kept track of strict vs non-strict relations.
- [ ] I produced a counterexample for every rejected "always true" option.
- [ ] I read the stem's exact wording ("always", "sometimes", "must", "can").
- [ ] I finished inside 45 seconds.

## Related

- [Inequality symbols and relations](../01-concepts/01-inequality-symbols-and-relations.md)
- [Inequality solving procedures](../02-techniques/01-inequality-solving-procedures.md)
- [Solved inequality and relations set](../03-worked-examples/01-solved-inequality-set.md)
- [Inequality one-pager](../05-reference/01-inequality-one-pager.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
