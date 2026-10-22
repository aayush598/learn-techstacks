# Number Series — Traps and the Time Sink

> Section 1 · Aptitude · Number Series · _Estimated reading time: 6 min_
> **Prerequisite:** [Series solving techniques](../02-techniques/01-series-solving-techniques.md)

## In one sentence

Series traps are **rule-forcing traps** — you stretch the pattern until it reaches an option — and the
real enemy is the clock, not the arithmetic.

## Why the pre-test tests this

- Any finite series can be fitted by an infinite number of rules. The exam exploits that: options are
  designed to reward the rule that "almost" works.
- The 10-question section has ~15 minutes. A 4-minute series costs you three other questions.
- The wrong-term format is the biggest trap: the "obviously odd" term is frequently not the wrong one.

## Core concept

### The eight traps

| # | Trap | What it looks like | The fix |
|---|---|---|---|
| 1 | **Extend until an option appears** | You try 3 rules and keep the one that lands on an option | Extend one step; if it misses, the family is wrong |
| 2 | **Missing interleaved patterns** | One rule fits the odd terms, another fits the even terms | Split the series by position |
| 3 | **Picking the odd-looking term** | The wrong term is the one that "looks strange" | The rule decides, not the look |
| 4 | **Squares vs cubes** | 27 treated as 3³ when the pattern is n² | Check two terms, not one |
| 5 | **Wrong Fibonacci pair** | You add the previous term to a term two back | term(n) = term(n−1) + term(n−2) |
| 6 | **Continuing the last difference** | The difference row changes and you keep adding | Look at the whole row |
| 7 | **Forcing third differences** | You invent a cubic to fit a quadratic | Test families in the standard order |
| 8 | **The 4-minute sink** | You are still writing numbers at the 3-minute mark | 70-second cap |

### Trap 3 in detail — the wrong-term trap

```
2, 6, 12, 20, 30, 44, 56
```

Candidates see `44` between two even-step numbers and pick it. That happened to be right here, but
consider:

```
3, 9, 27, 81, 243, 730, 729
```

Here `730` is the wrong term even though `729` *also* looks odd, and `729` is a correct term. The
"looks odd" heuristic cannot tell 730 from 729. Only the rule can: `× 3` ⇒ the 6th term must be 729.

### Trap 2 in detail — interleaved series

```
5, 20, 19, 76, 75, ?
```

Read as one sequence and nothing fits. Split by position:

| Position | Terms | Rule |
|---|---|---|
| Odd | 5, 19, 75 | ×4, −1 |
| Even | 20, 76, ? | ×4, −1 → 300 |

### Trap 1 in detail — rule-forcing

| You see | The trap | The discipline |
|---|---|---|
| Your rule gives a number that is not an option | You extend two more steps "to reach" an option | The rule is wrong. Go back to the difference row |
| Two rules both fit the visible terms | You pick the one matching an option | Both fit, so pick the one that fits **all** visible terms *and* produces an option |
| The last option fits "no pattern" | You avoid it | Some exam series do use the "no rule" option — check it last |

## Worked example

**Q. Find the wrong term: 4, 9, 16, 25, 38, 49**

A. 16
B. 25
C. 38
D. 49

**The trap**: candidates look for a term that "does not belong" by eye. 38 is not a perfect square, so
the eye picks it — but the eye is unreliable. In the earlier series `3, 9, 27, 81, 243, 730, 729`
**two** terms look wrong and only 730 is. Only the rule decides.

**The right procedure**

| Step | Action |
|---|---|
| 1 | Write the differences: 5, 7, 9, **13**, 11 — the odd steps should be 5, 7, 9, 11, 13 |
| 2 | The rule is `n²`: 2², 3², 4², 5², 6², 7² → 4, 9, 16, 25, 36, 49 |
| 3 | The term after 25 should be 36; the printed **38** breaks the pattern |

**Answer: C (38).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 16 | 4² — correct |
| 25 | 5² — correct |
| 49 | 7² — correct |

**The lesson:** the rule, not the look, selects the answer. Always recompute the rule and check what
the corrected series becomes.

## Quick rules

- Difference row, then ratio row. Always both.
- Extend one step; a miss means the family is wrong.
- Interleaved series: split by position before trying more families.
- Wrong-term: exclude the suspect, find the rule, recompute the correct value.
- Two terms looking wrong means your rule is wrong, not that two answers exist.
- Squares, cubes, n(n+1), primes and Fibonacci are memorised lists, not derived.
- Digit sums constant → digit-based rule.
- 70-second cap. Mark and move.

## Common traps

| Trap | Wrong answer | Right answer |
|---|---|---|
| Extending to reach an option | A number you forced | Go back to the difference row |
| Odd-looking term | 729 in the 730 question | 730 — the rule decides |
| Squares read as cubes | 144 for the cubes series | 216 |
| Wrong Fibonacci pair | 6 | 8 |
| Continuing the last difference | 39 instead of 37 | Extend the difference row first |
| Interleaved series missed | "no rule fits" | Split odd/even |
| Time sink | 3 minutes | 70 seconds, then guess and move |

## Checklist

- [ ] I wrote the difference row before guessing.
- [ ] I checked the ratio row too.
- [ ] I split by position when a single rule failed.
- [ ] For wrong-term questions, I recomputed the correct value.
- [ ] I did not force a rule to reach an option.
- [ ] I finished inside 70 seconds.

## Related

- [Number series pattern families](../01-concepts/01-series-pattern-types.md)
- [Series solving techniques](../02-techniques/01-series-solving-techniques.md)
- [Solved number-series set](../03-worked-examples/01-solved-series-set.md)
- [Pattern catalogue](../05-reference/01-series-pattern-catalogue.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
