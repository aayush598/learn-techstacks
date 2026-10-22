# Number Series — Pattern Catalogue

> Section 1 · Aptitude · Number Series · _Estimated reading time: 4 min_
> **Prerequisite:** [Number series pattern families](../01-concepts/01-series-pattern-types.md)

## In one sentence

A catalogue of every pattern family that appears in the pre-test, with its formula, its first terms
and the clue that identifies it on sight.

## Why the pre-test tests this

- You do not need new patterns. You need the old ones to arrive at in under 20 seconds.
- This is the page to revise the night before — it is a lookup table, not theory.

## Core concept

### Pattern catalogue

| Family | Rule | First terms | Identifying clue |
|---|---|---|---|
| Arithmetic | `+ d` | 3, 7, 11, 15, 19 | Constant first difference |
| Arithmetic (decreasing) | `− d` | 50, 44, 38, 32, 26 | Constant negative difference |
| Geometric | `× r` | 3, 6, 12, 24, 48 | Constant ratio |
| Geometric (decreasing) | `÷ r` | 243, 81, 27, 9, 3 | Constant ratio < 1 |
| Difference of difference | add 3, 5, 7, 9 … | 2, 5, 10, 17, 26 | Constant 2nd difference |
| Squares | `n²` | 1, 4, 9, 16, 25 | Differences are odd numbers 3,5,7,9 |
| Cubes | `n³` | 1, 8, 27, 64, 125 | Differences 7, 19, 37, 61 |
| n(n+1) pronic | `n² + n` | 2, 6, 12, 20, 30 | Differences 4, 6, 8, 10 |
| n(n−1) | `n² − n` | 2, 6, 12, 20, 30 | Same differences, shifted start |
| Powers of 2 | `2ⁿ` | 2, 4, 8, 16, 32 | Doubling from 2 |
| Powers of 3 | `3ⁿ` | 3, 9, 27, 81, 243 | Tripling from 3 |
| Fibonacci | `a(n−1) + a(n−2)` | 1, 1, 2, 3, 5, 8 | Each term = sum of two before |
| Lucas | `a(n−1) + a(n−2)` | 2, 1, 3, 4, 7, 11 | Fibonacci with a different start |
| Alternating operations | `×a, −b` | 5, 20, 19, 76, 75 | Differences alternate sign/size |
| Alternating two series | two rules by position | 1, 10, 3, 100, 5, 1000 | Odd and even positions differ |
| Primes | next prime | 2, 3, 5, 7, 11, 13 | Gaps 1, 2, 2, 4, 2 |
| Squares of primes | `p²` | 4, 9, 25, 49, 121 | Roots are 2, 3, 5, 7, 11 |
| Cubes of natural numbers + offset | `n³ + c` | 9, 28, 65, 126 | Offset constant |
| Digit increment | `+ k` | 19, 28, 37, 46 | Digit sum stays constant |
| Digit reversal | alternate reversed | 12, 21, 13, 31 | Digits swap |
| Mixed `+a, ×b` | two operations | 2, 6, 18, 20, 60 | +4, ×3 alternating |
| Sum + product | `a + b×c` | 3, 8, 15, 24 | n² + 2 form |

### Squares, cubes and pronics you must recognise instantly

| n | n² | n³ | n(n+1) |
|---|---|---|---|
| 1 | 1 | 1 | 2 |
| 2 | 4 | 8 | 6 |
| 3 | 9 | 27 | 12 |
| 4 | 16 | 64 | 20 |
| 5 | 25 | 125 | 30 |
| 6 | 36 | 216 | 42 |
| 7 | 49 | 343 | 56 |
| 8 | 64 | 512 | 72 |
| 9 | 81 | 729 | 90 |
| 10 | 100 | 1000 | 110 |

### Primes to 100

```
2  3  5  7  11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97
```

### Fibonacci sequence

```
1  1  2  3  5  8  13  21  34  55  89  144  233  377  610
```

### Difference-table reference

| Series | 1st differences | 2nd differences | Family |
|---|---|---|---|
| 2, 5, 10, 17, 26 | 3, 5, 7, 9 | 2, 2, 2 | Difference of difference |
| 1, 4, 9, 16, 25 | 3, 5, 7, 9 | 2, 2, 2 | Squares |
| 3, 6, 12, 24, 48 | (ratios 2) | — | Geometric |
| 1, 8, 27, 64, 125 | 7, 19, 37, 61 | 12, 18, 24 | Cubes (3rd difference 6) |
| 5, 20, 19, 76, 75 | 15, −1, 57, −1 | — | Alternating operations |

### Fast recognition heuristics

| You notice | Think |
|---|---|
| Differences are odd numbers 3, 5, 7, 9 | Squares |
| Differences are 4, 6, 8, 10 | n(n+1) |
| Every term is ×2 or ÷2 | Powers of 2 |
| Every term is ×3 | Powers of 3 |
| Terms sum in pairs | Fibonacci |
| One digit constant, one changing | Digit-based |
| Digit sums all equal | Digit-based |
| Roots are 2, 3, 5, 7, 11 | Squares of primes |

## Worked example

**Q. What comes next: 4, 9, 16, 25, ?**

Differences: 5, 7, 9 → next difference 11 → 25 + 11 = **36**. (Squares, 6².)

**Answer: 36.** Recognise "differences are consecutive odd numbers" ⇒ squares.

**Second check.** 4, 9, 16, 25, 36 are 2², 3², 4², 5², 6² ✅

## Quick rules

- Difference row, then ratio row.
- Extend one step only.
- Constant differences ⇒ arithmetic; constant ratios ⇒ geometric.
- Constant 2nd differences ⇒ difference-of-difference.
- Squares ⇒ odd-step differences; n(n+1) ⇒ even-step differences.
- Interleaved ⇒ split by position.
- Wrong term ⇒ recompute the rule.
- 70-second cap.

## Common traps

| Trap | Fix |
|---|---|
| Extending to reach an option | One step only |
| Odd-looking term | The rule decides |
| Squares vs cubes | Check two terms |
| Wrong Fibonacci pair | n−1 + n−2 |
| Continuing the last difference | Read the whole row |
| Missing interleaved series | Split by position |
| Time sink | 70 seconds |

## Checklist

- [ ] I can list the catalogue from memory without looking.
- [ ] I know the squares/cubes/pronic table to 10.
- [ ] I know the primes to 100 and the Fibonacci list.
- [ ] I write differences before guessing.
- [ ] I finish a 10-question series drill in under 13 minutes.

## Related

- [Number series pattern families](../01-concepts/01-series-pattern-types.md)
- [Series solving techniques](../02-techniques/01-series-solving-techniques.md)
- [Solved number-series set](../03-worked-examples/01-solved-series-set.md)
- [Series traps](../04-pitfalls/01-series-traps.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
