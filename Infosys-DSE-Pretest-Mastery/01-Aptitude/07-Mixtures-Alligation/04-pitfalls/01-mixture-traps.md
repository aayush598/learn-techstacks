# Mixture Traps — Where the Marks Leak

> Section 1 · Aptitude · Mixtures & Alligation · _Estimated reading time: 6 min_
> **Prerequisite:** [Solved mixture and alligation set](../03-worked-examples/01-solved-mixture-set.md)

## In one sentence

The seven traps in this topic are all **misreadings of the verb** — add, remove, replace, mix — not
arithmetic errors.

## Why the pre-test tests this

- The arithmetic in mixture questions is trivial; the exam targets the reading.
- Options are built from the misreadings: 3 : 2 (no change), 4 : 1 (one-step replacement),
  1 : 2 (reversed alligation). If you can name the trap behind each wrong option, you will not pick
  it.
- Meera's time panic turns a 45-second question into a 2-minute one. The trap list below is the
  fastest fix.

## Core concept

### Trap 1 — alligation ratio reversed

**Symptom:** your answer is the mirror of the correct ratio.

| Mixture | Correct | Reversed |
|---|---|---|
| 20% & 50% → 30% | 2 : 1 (20% solution : 50% solution) | 1 : 2 |

**Fix:** the quantity of the **cheaper** mixture comes first. And the check: the answer must pull the
mean toward the mixture you use more of.

### Trap 2 — alligation run on ratios instead of percentages

**Symptom:** the differences make no sense (a ratio has no scale).

**Fix:** convert to percentages first.

| Ratio | % |
|---|---|
| 1 : 4 | 20% |
| 2 : 3 | 40% |
| 1 : 2 | 33⅓% |

### Trap 3 — removing part of the mixture thought to change the concentration

**Symptom:** you compute a new percentage after taking out 12 litres of a 3 : 2 mixture.

**Fix:** S and V both shrink by the same factor `r/V`, so `S/V` is unchanged. Removing mixture changes
**quantities**, never the concentration.

### Trap 4 — pure solvent removal treated as mixture removal

**Symptom:** after removing 10 litres of water from 50 litres at 20% acid, you answer 20% (trap 3's
logic) or 10% (you removed acid too).

**Fix:** removing **pure water** keeps the acid at 10 litres and cuts the total to 40 → 25%.

| What is removed | Solute | Total | Concentration |
|---|---|---|---|
| Pure water | unchanged | decreases | **increases** |
| Pure solute | increases by the amount removed | decreases | changes |
| Part of the mixture | decreases proportionally | decreases proportionally | **unchanged** |

### Trap 5 — adding water treated as adding a mixture

**Symptom:** you write "milk and water both increase" when water is added.

**Fix:** adding water does not add milk. Solute constant, total up.

### Trap 6 — replacement done in one step

**Symptom:** you add 12 litres of milk to 36 litres of milk and subtract 12 litres of water, ignoring
that the drawn-out mixture contained milk too.

| One-step (wrong) | Two-step (right) |
|---|---|
| Milk: 36 + 12 = 48 | Milk: 36 − 7.2 + 12 = 40.8 |
| Water: 24 − 12 = 12 | Water: 24 − 4.8 = 19.2 |
| Ratio 4 : 1 | Ratio **17 : 8** |

**Fix:** remove first (r × each part), then add. Then check the volume is back to 60.

### Trap 7 — the volume not restored

**Symptom:** after "12 litres is drawn out and the vessel is filled with milk", you leave the total at
48 litres.

**Fix:** the phrase "filled with" means the total returns to the original volume. Always check.

### Trap 8 — the answer does not lie between the inputs

A mixture's concentration must lie between the two concentrations you mixed. If your answer is 60%
when you mixed 20% and 50%, something is wrong.

| Input range | Answer must be inside |
|---|---|
| 20% and 50% | 20% – 50% |
| 10%, 20%, 40% | 10% – 40% |

### Trap 9 — decimal drift

`33⅓%` becomes `33.3%`, then `2/5 − 33.3 = 6.7`, and the ratio becomes 6.7 : 13.3 instead of 1 : 2.
**Use exact fractions** whenever the mean is not a whole number.

## Worked example

**Q. A vessel contains 50 litres of a mixture of acid and water containing 20% acid. 10 litres of water
is removed. What is the concentration of acid in the remaining mixture?**

A. 12.5%
B. 20%
C. 22%
D. 25%

**The trap inside the trap:** 25% and 12.5% are both "reasonable-looking" numbers, so candidates
pick one on instinct. 12.5% comes from halving 25% — the "I removed a quarter so the concentration
halved" instinct.

**The correct reading**

| Element | Value |
|---|---|
| What is removed? | **Pure water** (the stem says "10 litres of water", not "10 litres of the mixture") |
| Acid amount | `50 × 0.2` = 10 litres, unchanged |
| New total | `50 − 10` = 40 litres |
| New concentration | `10/40 × 100` = 25% |

**Answer: D (25%).**

**Distractor mapping**

| Option | The mistake behind it |
|---|---|
| 12.5% | Halved the concentration instead of recomputing from the constant acid |
| 20% | Applied trap 3 (removing any liquid keeps the concentration) |
| 22% | Wrong arithmetic |

**The general rule this question tests:** **read the verb and the noun**. "10 litres of water" and
"10 litres of the mixture" are different questions with different answers.

## Quick rules

- Alligation: `Q_cheap : Q_dear = (C_dear − C_mean) : (C_mean − C_cheap)`.
- Cheaper mixture first; the bigger difference pairs with the weaker mixture.
- Percentages only in alligation.
- Pure water removed → concentration up. Part of mixture removed → concentration unchanged.
- Adding water → solute constant.
- Replacement → remove, then add, then verify the volume.
- The answer lies between the inputs.
- Exact fractions over decimals.
- 70 seconds.

## Common traps

| Trap | Wrong answer | Right answer |
|---|---|---|
| Alligation reversed | 1 : 2 | 2 : 1 |
| Alligation on ratios | Nonsense | Convert to % |
| Removing mixture thought to change % | 20% | Concentration unchanged |
| Pure water removal mishandled | 20% | 25% |
| Water addition adds milk | Wrong total | Solute constant |
| One-step replacement | 4 : 1 | 17 : 8 |
| Volume not restored | 48 L | 60 L |
| Answer outside input range | — | Check the range |
| Decimal drift | 6.7 : 13.3 | 1 : 2 |

## Checklist

- [ ] I read the verb: add, remove, replace, mix.
- [ ] I read the noun: pure water, pure solute, or "of the mixture".
- [ ] I converted ratios to percentages before alligating.
- [ ] I checked the answer lies between the input concentrations.
- [ ] I did replacement in two steps and restored the volume.
- [ ] I used fractions instead of rounded decimals.
- [ ] I finished inside 70 seconds.

## Related

- [Mixture and alligation rules](../01-concepts/01-mixture-and-alligation-rules.md)
- [Alligation shortcuts](../02-techniques/01-alligation-shortcuts.md)
- [Solved mixture and alligation set](../03-worked-examples/01-solved-mixture-set.md)
- [Alligation formula sheet](../05-reference/01-alligation-formula-sheet.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
