# Alligation Formula Sheet — One Page

> Section 1 · Aptitude · Mixtures & Alligation · _Estimated reading time: 3 min_
> **Prerequisite:** [Mixture and alligation rules](../01-concepts/01-mixture-and-alligation-rules.md)

## In one sentence

Every formula you need for mixtures and alligation, on one page, with the direction of each ratio
written out so you never reverse it.

## Why the pre-test tests this

- This is the page to open for 60 seconds before the exam and after every practice drill.
- Mixture questions are one or two per paper. One missed rule costs 5% of the section.

## Core concept

### Master formula table

| # | Question type | Formula | Watch out |
|---|---|---|---|
| 1 | Mix two mixtures, find the ratio | `Q1 : Q2 = (C2 − C) : (C − C1)` | Q1 = cheaper mixture |
| 2 | Mix two mixtures, find the mean | `C = (Q1C1 + Q2C2)/(Q1 + Q2)` | Weighted, not simple, average |
| 3 | Add pure solvent | `V_new = S / (new% ÷ 100)` | Solute constant |
| 4 | Remove pure solvent | `new% = S/(V − r) × 100` | Solute constant |
| 5 | Remove r of the mixture | `S_new = S(1 − r/V)`, `new% = S/V` | **% unchanged** |
| 6 | Replace r with pure solute | `S_new = S(1 − r/V) + r`, `V_new = V` | Two-step logic |
| 7 | Replace r with pure solvent | `S_new = S(1 − r/V)`, `V_new = V` | Solute drops |
| 8 | Mix three in a known ratio | `C = Σ(QiCi)/ΣQi` | Ratio of quantities |
| 9 | Find the quantity of each | Alligation ratio, then scale to the total | Ratio → litres needs a total |

### Alligation table layout

```
        C1 (cheaper)     C (mean)      C2 (dearer)
             |____________|  |___________|
                  C − C1            C2 − C
                  ↓                 ↓
        quantity of C1      quantity of C2
```

`Q1 : Q2 = (C2 − C) : (C − C1)` — the **left** difference goes with the **left** mixture.

### Ratio ↔ concentration conversions

| Milk : water | Water : milk | Milk % | Water % |
|---|---|---|---|
| 1 : 1 | 1 : 1 | 50% | 50% |
| 1 : 2 | 2 : 1 | 33⅓% | 66⅔% |
| 1 : 3 | 3 : 1 | 25% | 75% |
| 1 : 4 | 4 : 1 | 20% | 80% |
| 1 : 5 | 5 : 1 | 16⅔% | 83⅓% |
| 2 : 3 | 3 : 2 | 40% | 60% |
| 2 : 5 | 5 : 2 | 28⅔% | 71⅓% |
| 3 : 2 | 2 : 3 | 60% | 40% |
| 3 : 1 | 1 : 3 | 75% | 25% |
| 4 : 1 | 1 : 4 | 80% | 20% |
| 5 : 1 | 1 : 5 | 83⅓% | 16⅔% |

### Operation recipe table

| Stem says | Solute (S) | Total (V) | Result |
|---|---|---|---|
| "X litres of water is added" | unchanged | increases | concentration falls |
| "X litres of the mixture is removed" | falls proportionally | falls | concentration unchanged |
| "X litres of water is removed" | unchanged | falls | concentration rises |
| "X litres of the mixture is replaced by X litres of milk" | recompute | unchanged | two steps |
| "X litres of the mixture is replaced by X litres of water" | recompute | unchanged | two steps |
| "X litres of milk is added" | increases by X | increases by X | recompute both |
| "Mixed in the ratio a : b" | weighted | weighted | alligation |

### Two-step replacement card

```
Remove r litres of mixture (fraction f = S/V of it):
    solute out   = r × S/V
    solute left  = S − r(S/V)
    volume left  = V − r
Add r litres of the new liquid:
    solute added = r × (its own concentration)
    volume       = V
```

### Alligation with exact fractions (avoid decimals)

| Target | Fraction | Use instead of |
|---|---|---|
| 1 : 2 | 1/3 | 33.33% |
| 2 : 5 | 2/7 | 28.57% |
| 3 : 7 | 3/10 | 30% |
| 1 : 6 | 1/7 | 14.29% |

### Numbers worth memorising

| Quantity | Value |
|---|---|
| 20% of 50 | 10 |
| 25% of 40 | 10 |
| 1/3 of 60 | 20 |
| 1/5 of 40 | 8 |
| 2/5 of 60 | 24 |
| 3/5 of 60 | 36 |
| ₹108/kg mix | 30 kg @ ₹120 + 20 kg @ ₹90 |
| 13 : 3 | 60 L at 3:1, replace 15 L with milk |
| 17 : 8 | 60 L at 3:2, draw 12 L, refill with milk |

### 70-second checklist

| Check | Done |
|---|---|
| Shape identified (ratio / add-remove / replace / weighted) | ☐ |
| Ratios converted to percentages before alligation | ☐ |
| Cheaper mixture written first in the alligation ratio | ☐ |
| Solute held constant for add/remove questions | ☐ |
| Volume restored after a replacement | ☐ |
| Answer lies between the input concentrations | ☐ |
| Fractions used instead of rounded decimals | ☐ |

## Worked example

**Q. In what ratio must a 20% salt solution and a 50% salt solution be mixed to obtain a 30%
solution?**

```
Q(20%) : Q(50%) = (50 − 30) : (30 − 20) = 20 : 10 = 2 : 1
```

**Answer: 2 : 1.** The 20% solution comes first because it is the cheaper mixture.

**Second check.** 2 parts of 20% + 1 part of 50% → `(2×20 + 1×50)/3 = 90/3 = 30%` ✅

## Quick rules

- `Q_cheap : Q_dear = (C_dear − C_mean) : (C_mean − C_cheap)`.
- Weighted mean for the reverse direction.
- Solute constant → volume changes.
- Removing mixture → concentration unchanged.
- Replacement → remove, then add, then verify the volume.
- Answer between the inputs.
- Fractions, not decimals.
- 70 seconds.

## Common traps

| Trap | Fix |
|---|---|
| Alligation reversed | Cheaper first |
| Alligation on ratios | Convert to % |
| Removing mixture changes % | It does not |
| Pure water removal | Solute constant, % rises |
| One-step replacement | Remove, then add |
| Volume not restored | Refill |
| Decimal drift | Fractions |

## Checklist

- [ ] I can write the alligation rule from memory with the correct direction.
- [ ] I know the common ratio ↔ percentage conversions.
- [ ] I know which operations keep the solute constant.
- [ ] I can do the two-step replacement without notes.
- [ ] I will use exact fractions when the mean is not whole.
- [ ] I will time-check at 70 seconds.

## Related

- [Mixture and alligation rules](../01-concepts/01-mixture-and-alligation-rules.md)
- [Alligation shortcuts](../02-techniques/01-alligation-shortcuts.md)
- [Solved mixture and alligation set](../03-worked-examples/01-solved-mixture-set.md)
- [Mixture traps](../04-pitfalls/01-mixture-traps.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
