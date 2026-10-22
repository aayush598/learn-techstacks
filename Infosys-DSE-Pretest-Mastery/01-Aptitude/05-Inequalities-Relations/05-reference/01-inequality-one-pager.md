# Inequalities & Relations — One-Page Revision Sheet

> Section 1 · Aptitude · Inequalities & Relations · _Estimated reading time: 4 min_
> **Prerequisite:** [Inequality symbols and relations](../01-concepts/01-inequality-symbols-and-relations.md)

## In one sentence

Print this page: the symbol table, the chain decoder, the transitivity rules and the counterexample
test — the whole archetype on one sheet.

## Why the pre-test tests this

- One inequality question per paper, worth a full mark if you read the chain correctly.
- Everything on this page is mechanical. Ten minutes of revision removes the archetype from your
  worry list.

## Core concept

### Symbol table

| Symbol | Means | In a chain it points at |
|---|---|---|
| `>` | strictly greater | the smaller element |
| `<` | strictly less | the smaller element |
| `≥` | at least as great | the smaller element |
| `≤` | at most as great | the smaller element |
| `=` | equal | both elements |

### Chain decoder — the canonical example

```
a > b < n ≥ i < p
```

| Pair | Relation | Pointed at |
|---|---|---|
| a > b | a is greater than b | b |
| b < n | n is greater than b | b |
| n ≥ i | n is at least i | i |
| i < p | p is greater than i | i |

| You may conclude | You may NOT conclude |
|---|---|
| a > b | a > n |
| n > b | n > p |
| n ≥ i | b < i |
| p > i | i is the smallest overall |
| b is the minimum of {a, b, n} | a is the maximum |

### Transitivity and strength

| Chain | Conclusion | Rule |
|---|---|---|
| `a > b > c` | `a > c` | strict + strict |
| `a ≥ b > c` | `a > c` | one strict link upgrades |
| `a > b ≥ c` | `a > c` | one strict link upgrades |
| `a ≥ b ≥ c` | `a ≥ c` | weak + weak stays weak |
| `a = b > c` | `a > c` | equality is transparent |

### Minimum and maximum test

| Claim | True when |
|---|---|
| X is the minimum of the group | Both neighbouring signs point at X |
| X is the maximum of the group | X is greater than **every** other element mentioned |
| X is definitely not the maximum | X is pointed at by a sign from a larger element |

### The three question formats

| Format | Options | Answer rule |
|---|---|---|
| "Which is definitely true?" | Relations | True in every assignment |
| "Which is always true?" | Statements | Cannot be broken by a counterexample |
| "Which is sometimes true?" | Statements | One valid example exists |
| "Statements I and II" | Only I / Only II / Both / Neither | Test each independently |

### Counterexample recipe

```
Claim:  a > n
Pick:   a=5, b=1, n=9, i=2, p=7
Check:  chain satisfied ✔, claim violated ✔  →  reject the claim
```

Use small integers 1–9. If you cannot satisfy the chain and break the claim, the claim is definitely
true.

## Worked example

**Q. If `a > b < n ≥ i < p`, which is definitely true?**

```
Split:  a>b | b<n | n≥i | i<p
Answer: p > i   (directly given)
```

**Answer: `p > i`.**

**Second check — is `n > p` maybe true?** No: n = 6, p = 9 works with the chain.

## Quick rules

- Split → point → chain → test → counterexample.
- The sign points at the smaller element.
- Chain only in one direction.
- Any strict link ⇒ strict conclusion.
- Equality kills strictness.
- One counterexample rejects an "always true" claim.
- A "maximum" must dominate every element.
- 30–45 seconds.

## Common traps

| Trap | Fix |
|---|---|
| Chaining across `>` then `<` | Split into pairs |
| `≥` treated as `>` | Keep the weak link |
| Assuming global min/max | Neighbours only |
| One example proving "always" | Need a counterexample |
| Always vs sometimes mixed up | Read the stem twice |
| Code mis-decoded | Decode first |

## Checklist

- [ ] I can decode `a > b < n ≥ i < p` from memory.
- [ ] I know the strength table.
- [ ] I can produce a counterexample in under 20 seconds.
- [ ] I always test each option against the pairs.
- [ ] I finished a 10-question inequality drill in under 11 minutes.

## Related

- [Inequality symbols and relations](../01-concepts/01-inequality-symbols-and-relations.md)
- [Inequality solving procedures](../02-techniques/01-inequality-solving-procedures.md)
- [Solved inequality and relations set](../03-worked-examples/01-solved-inequality-set.md)
- [Inequality traps](../04-pitfalls/01-inequality-traps.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
