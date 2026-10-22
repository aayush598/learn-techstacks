# Alligation Shortcuts — Solve It in Four Lines

> Section 1 · Aptitude · Mixtures & Alligation · _Estimated reading time: 7 min_
> **Prerequisite:** [Mixture and alligation rules](../01-concepts/01-mixture-and-alligation-rules.md)

## In one sentence

Every mixture question can be answered in four lines if you use the **difference method** for ratios
and the **constant-solute method** for "how much to add".

## Why the pre-test tests this

- Mixture questions look like they need long algebra. They do not — they need one insight.
- The difference method (alligation) covers ratio questions in about 25 seconds.
- The constant-solute method covers "add/remove" questions in about 40 seconds.
- Between them, they cover 95% of what the pre-test asks.

## Core concept

### The four-line difference method (alligation)

```
Step 1: Write the three concentrations in a row, cheapest → mean → dearest.
Step 2: Take the difference between the dearest and the mean, and between the
        mean and the cheapest.
Step 3: The quantity of the cheapest : quantity of the dearest = those two
        differences, in that order.
Step 4: Convert the ratio to the quantity the question asks for.
```

**Example.** 20% and 50% solutions mixed to give 30%:

```
50 − 30 = 20  →  quantity of the 20% solution
30 − 20 = 10  →  quantity of the 50% solution
Ratio = 20 : 10 = 2 : 1
```

**Speed variant — the "difference table" layout:**

```
            20        30        50
              \_______/ \_______/
              10                20
```

The lower difference goes with the **left** mixture (the cheaper one), the upper difference with the
right. The rule is symmetric, so if you remember only one thing, remember: **the bigger difference
pairs with the weaker mixture**.

### The constant-solute method

For any "how much do I add / remove" question:

| Question | Method |
|---|---|
| Add water (or any pure solvent) | Solute is constant → `new total = solute ÷ new fraction` |
| Remove water (pure solvent) | Solute is constant → `new total = V − r`, `new % = S/(V−r)` |
| Remove part of the mixture | Concentration is constant → answer = `r × S/V` removed solute |
| Replace r litres with pure solute | `S_new = S − r(S/V) + r`, `V` unchanged |
| Replace r litres with pure solvent | `S_new = S − r(S/V)`, `V` unchanged |
| Mix with another mixture | Weighted average, or alligation for the ratio |

### The "parts" trick

Work in **parts**, not litres. If the question gives a ratio, convert it to parts and keep the parts
count.

| Question | Parts method |
|---|---|
| 40 litres at 3 : 2 → new ratio 3 : 4 | Milk = 3 parts = 24 litres → 1 part = 8 → new water = 32 → add 32 − 16 = 16 |
| Ratio in the answer | Use alligation, then scale to the given total |

### Reverse alligation (finding the mean)

When you have quantities and concentrations and want the mixture's concentration:

```
C = (Q1C1 + Q2C2) / (Q1 + Q2)
```

Speed trick: if the quantities are equal, `C` is simply the **average** of the two concentrations.
If they differ, use the weighted average — there is no shortcut, but it is one line.

### Three pre-test shapes and the method for each

| Shape | Stem pattern | Method | Time |
|---|---|---|---|
| Ratio of two mixtures | "In what ratio must X and Y be mixed…?" | Alligation | 25 s |
| Add or remove a liquid | "How much water must be added…?" | Constant solute | 40 s |
| Replace part of the mixture | "If 12 litres is drawn out and refilled with…" | Remove-then-add, in two steps | 60 s |

### The two-step replacement procedure

Never try to do replacement in one step. Do it in two:

```
Step 1: Remove r litres of mixture.
        Solute removed  = r × S/V
        Solute left    = S − r(S/V)
        Volume left    = V − r
Step 2: Add r litres of the new liquid.
        Solute added   = r × (its own concentration)
        Volume         = V
```

Then read off the new ratio or percentage.

## Worked example

**Q. A vessel contains 60 litres of a mixture of milk and water in the ratio 3 : 2. 12 litres of the
mixture is drawn out and the vessel is filled with milk. What is the ratio of milk and water in the
vessel now?**

A. 3 : 2
B. 17 : 8
C. 4 : 1
D. 5 : 2

**Step 1 — split the original mixture**

| Component | Working | Amount |
|---|---|---|
| Milk | `60 × 3/5` | 36 litres |
| Water | `60 × 2/5` | 24 litres |

**Step 2 — remove 12 litres of mixture.** The removed part has the same ratio 3 : 2:

| Removed | Working | Amount |
|---|---|---|
| Milk | `12 × 3/5` | 7.2 litres |
| Water | `12 × 2/5` | 4.8 litres |

**Step 3 — what is left, and what was added**

| Component | Left in vessel | Added | New total |
|---|---|---|---|
| Milk | 36 − 7.2 = 28.8 | 12 | **40.8** |
| Water | 24 − 4.8 = 19.2 | 0 | **19.2** |

Total volume = 40.8 + 19.2 = 60 litres ✅ (the vessel is full again).

**Step 4 — the ratio**

```
40.8 : 19.2  →  multiply both by 2.4  →  102 : 48  →  divide by 6  →  17 : 8
```

**Answer: B (17 : 8).**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| 3 : 2 | The original ratio — you forgot the replacement changed it |
| 4 : 1 | Removed the milk and added all 12 without the 7.2 that was taken out (36 + 12 = 48, water 24 − 12 = 12 → 48:12 = 4:1) — the classic "forgot that some milk was drawn out with the mixture" error |
| 5 : 2 | Wrong arithmetic |

**Time: 55 seconds.** The two-step method (remove, then add) is what makes this safe. One-step
arithmetic is where the 4 : 1 distractor comes from.

**Second example — alligation in 25 seconds.**

**Q. In what ratio must 20% and 50% salt solutions be mixed to obtain a 30% solution?**

```
50 − 30 = 20   →  quantity of the 20% solution
30 − 20 = 10   →  quantity of the 50% solution
Ratio = 20 : 10 = 2 : 1
```

**Answer: 2 : 1.** (Options: 1 : 2, 2 : 1, 3 : 1, 1 : 3 → 2 : 1.)

## Quick rules

- Alligation: `Q_cheap : Q_dear = (C_dear − C_mean) : (C_mean − C_cheap)`.
- The bigger difference pairs with the weaker mixture.
- Never run alligation on ratios — convert to percentages.
- Add/remove questions: hold the **solute** constant and recompute the total.
- Removing part of the mixture keeps the concentration unchanged.
- Replacement is always two steps: remove, then add.
- Verify the total volume after a replacement.
- Use fractions (1/5, 2/3) instead of decimals.
- 70 seconds.

## Common traps

| Trap | Effect | Fix |
|---|---|---|
| Alligation ratio reversed | Mirror answer | Cheaper quantity first |
| Alligation on raw ratios | Nonsense | Convert to % |
| Solute assumed to change when water is added | Wrong % | Solute constant |
| One-step replacement | Wrong ratio | Remove, then add |
| Total volume not restored | Wrong totals | Refill to the original volume |
| Forgetting that drawn-out mixture carries both components | 4:1 instead of 17:8 | Remove 3/5 and 2/5 of r |
| Decimal rounding | Off by 1–2 | Use fractions |

## Checklist

- [ ] I used alligation only after converting ratios to percentages.
- [ ] I held the solute constant for every "add/remove" question.
- [ ] I did replacement in two steps.
- [ ] I checked that the total volume is unchanged after a replacement.
- [ ] I identified which quantity the question asks for.
- [ ] I finished inside 70 seconds.

## Related

- [Mixture and alligation rules](../01-concepts/01-mixture-and-alligation-rules.md)
- [Solved mixture and alligation set](../03-worked-examples/01-solved-mixture-set.md)
- [Mixture traps](../04-pitfalls/01-mixture-traps.md)
- [Alligation formula sheet](../05-reference/01-alligation-formula-sheet.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
