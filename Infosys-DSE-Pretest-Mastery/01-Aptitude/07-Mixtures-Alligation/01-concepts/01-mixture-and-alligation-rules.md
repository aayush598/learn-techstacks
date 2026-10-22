# Mixtures and Alligation — The Rules

> Section 1 · Aptitude · Mixtures & Alligation · _Estimated reading time: 8 min_
> **Prerequisite:** [Percentages, Profit/Loss & Discount](../../02-Percentages-Profit-Loss-Discount/README.md)

## In one sentence

Mixture questions are all one idea — **the concentration of a mix is the weighted average of the
concentrations** — and alligation is the shortcut that finds the weights without algebra.

## Why the pre-test tests this

- The DSE pre-test's aptitude section often carries **1 mixture/alligation question**, usually a
  milk–water or acid–water problem with a ratio or a "how much to add" answer.
- The topics look like five different chapters. They are one: track the **amount of solute** and the
  **total volume**, and every variant follows.
- Candidates who learn only the alligation rule still fail the "how much water must be added"
  questions. Those need the solute-tracking method.

## Core concept

### The two quantities that matter

| Quantity | Symbol | Rule |
|---|---|---|
| **Amount of solute** (milk, acid, salt) | S | Only changes when solute is added or removed |
| **Total volume** | V | Changes when liquid is added, removed or replaced |

```
Concentration % = (S / V) × 100
```

| Operation | S | V |
|---|---|---|
| Add pure solvent (water) | unchanged | increases |
| Add pure solute (milk, acid) | increases | increases |
| Add another mixture | adds proportionally | adds proportionally |
| Remove pure solvent | unchanged | decreases |
| Remove some of the mixture | decreases proportionally | decreases proportionally |
| Replace r litres with pure solute | increases by r | unchanged |

**The single most useful fact in this topic:** removing some of the mixture leaves the concentration
**unchanged**, because S and V shrink by the same factor. Only removing *pure solvent* (or pure
solute) changes the concentration.

### Alligation rule (alligation alternate)

Two mixtures of concentrations `C1` (cheaper) and `C2` (dearer) are mixed to give a mean `C`:

```
Q1 : Q2  =  (C2 − C) : (C − C1)
```

- `Q1` = quantity of the **cheaper** mixture
- `Q2` = quantity of the **dearer** mixture

**Why it works (3 lines).** Write `Q1C1 + Q2C2 = C(Q1 + Q2)`. Rearranged:
`Q1(C1 − C) = Q2(C − C2)`, so `Q1/Q2 = (C − C2)/(C1 − C) = (C2 − C)/(C − C1)`. The differences are
always **non-negative**, so the ratio is positive.

**Worked mini-example.** Mix a 20% solution with a 50% solution to get 30%.
`Q(20%) : Q(50%) = (50 − 30) : (30 − 20) = 20 : 10 = 2 : 1`.

### Alligation medial (the reverse direction)

Given the quantities and the concentrations, find the mean:

```
C = (Q1C1 + Q2C2) / (Q1 + Q2)
```

30 kg at ₹120/kg + 20 kg at ₹90/kg → `(3600 + 1800)/50 = ₹108/kg`.

### The three "how much" variants

**Variant 1 — add pure solvent.** Solute amount is constant, so:

```
new concentration % = (S / V_new) × 100   →   V_new = S / (new %)
```

**Variant 2 — remove pure solvent.** Solute amount is constant, `V` shrinks:

```
new concentration % = (S / (V − r)) × 100
```

**Variant 3 — remove part of the mixture and refill with pure solute.** Both S and V change:

```
S_new = S − (r × S/V) + r = S + r(1 − S/V)
V_new = V
```

### Alligation with ratios instead of percentages

Convert each mixture's ratio to a fraction first:

| Milk : water | Milk % |
|---|---|
| 1 : 1 | 50% |
| 1 : 2 | 33⅓% |
| 1 : 3 | 25% |
| 1 : 4 | 20% |
| 2 : 3 | 40% |
| 3 : 2 | 60% |
| 3 : 1 | 75% |
| 4 : 1 | 80% |

Then apply alligation on the percentages. **Never** apply alligation directly on ratios — the rule
needs a scale, and percentages provide it.

### Ratio of two mixtures

When two mixtures are combined in a ratio to reach a target concentration, alligation gives the ratio
directly (using fractions to avoid rounding):

```
Mix A = 1/5 milk, Mix B = 2/5 milk, target = 1/3 milk
A : B = (2/5 − 1/3) : (1/3 − 1/5) = (1/15) : (2/15) = 1 : 2
```

### The three-part (alligation alternate) case

Mixing three mixtures in a known ratio to find the resulting concentration is a weighted average:

```
C = (Q1C1 + Q2C2 + Q3C3) / (Q1 + Q2 + Q3)
```

## Worked example

**Q. A vessel contains 40 litres of milk and water in the ratio 3 : 2. How much water must be added
so that the ratio of milk to water becomes 3 : 4?**

A. 8 litres
B. 16 litres
C. 20 litres
D. 24 litres

**Solution — track the milk**

| Step | Working |
|---|---|
| Milk in 40 litres at 3 : 2 | `40 × 3/5 = 24 litres` |
| Water in 40 litres | `40 × 2/5 = 16 litres` |
| New ratio 3 : 4 with 24 litres of milk | 3 parts = 24 → 1 part = 8 → water = 4 × 8 = **32 litres** |
| Water to add | `32 − 16 = 16 litres` |

**Answer: B (16 litres).**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| 8 litres | Added half the current water (16 ÷ 2) instead of computing the target |
| 20 litres | Mistook the target water (32) for the amount to add |
| 24 litres | The milk amount — you added milk instead of water |

**Alternative route.** Note the ratio 3 : 4 means milk is 3/7 of the mixture. Milk stays 24 litres, so
total becomes `24 ÷ 3/7 = 56` litres; add `56 − 40 = 16` litres of water. Same answer, one line.

## Quick rules

- Track **solute amount** and **total volume** separately. Everything else follows.
- Alligation: `Q_cheap : Q_dear = (C_dear − C_mean) : (C_mean − C_cheap)`.
- Never run alligation on ratios — convert to percentages first.
- Adding pure solvent: solute constant, volume up. Removing pure solvent: solute constant, volume down.
- Removing **part of the mixture**: concentration unchanged.
- Replacing r litres with pure solute: `S_new = S + r(1 − S/V)`, `V` unchanged.
- Alligation medial for the mean: `(Q1C1 + Q2C2)/(Q1 + Q2)`.
- Use fractions to avoid decimal drift: `1/5`, `2/5`, `1/3`.
- Cap at 70 seconds. These questions are usually one substitution away from the answer.

## Common traps

| Trap | Symptom | Fix |
|---|---|---|
| Alligation ratio reversed | Answer is the mirror ratio | "Cheaper quantity comes first" |
| Alligation applied to ratios | Nonsense answer | Convert to % first |
| Removing mixture thought to change concentration | Wrong % | Both S and V shrink together |
| Removing pure solvent assumed to remove solute | Wrong % | Solute amount stays |
| Adding water treated as adding mixture | Wrong total | Solute constant |
| Replaced volume not restored | Total volume shrinks | Refill to the original volume |
| Mixing up milk and water ratios | Ratio inverted | Track the milk |
| Decimal rounding in alligation | Off by a fraction | Use fractions |

## Checklist

- [ ] I identified the solute (milk / acid / salt) and the total volume.
- [ ] I converted any ratio to a percentage before using alligation.
- [ ] I checked which quantity the question asks for (ratio, amount, or percentage).
- [ ] I used the constant-solute shortcut for "add water" and "remove water".
- [ ] I remembered that removing part of the mixture keeps the concentration.
- [ ] I finished inside 70 seconds.

## Related

- [Alligation shortcuts](../02-techniques/01-alligation-shortcuts.md)
- [Solved mixture and alligation set](../03-worked-examples/01-solved-mixture-set.md)
- [Mixture traps](../04-pitfalls/01-mixture-traps.md)
- [Alligation formula sheet](../05-reference/01-alligation-formula-sheet.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
