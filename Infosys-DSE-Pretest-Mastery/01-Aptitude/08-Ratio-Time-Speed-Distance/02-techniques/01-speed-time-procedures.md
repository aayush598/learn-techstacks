# Speed, Time and Work — Solving Procedures

> Section 1 · Aptitude · Ratio, Time, Speed & Distance · _Estimated reading time: 8 min_
> **Prerequisite:** [Ratio, time, speed & distance rules](../01-concepts/01-ratio-speed-distance-rules.md)

## In one sentence

A fixed sequence of moves — **convert units once, name the situation, apply one formula, sanity
check** — that keeps every speed and work question inside 90 seconds.

## Why the pre-test tests this

- Speed–distance is the highest-frequency topic in the section. Two or three questions is normal.
- The formulas are few. The failure mode is *misreading the situation* — pole vs platform, equal
  times vs equal distances, rates vs times.
- Naming the situation before computing removes almost every error.

## Core concept

### The four-move procedure

| Move | Action | Time |
|---|---|---|
| 1 | **Convert units once** — pick m/s (for trains, boats) or km/h (for cars) and stay there | 15 s |
| 2 | **Name the situation** — pole, platform, opposite, same direction, downstream, upstream, together, one leaves early | 10 s |
| 3 | **Apply the one formula** for that situation | 40 s |
| 4 | **Sanity check** — is the answer in a sensible range, and are the units right? | 15 s |

### The unit-conversion drill (do this once, keep it)

```
km/h → m/s   :  × 5/18        (72 → 20, 54 → 15, 36 → 10)
m/s → km/h   :  × 18/5        (20 → 72, 15 → 54, 10 → 36)
```

Say it as a pair. `5/18` and `18/5` are the only two numbers in this topic worth memorising.

### Situation → formula table

| The stem says | Use |
|---|---|
| "crosses a pole" | `t = L/v` |
| "crosses a platform of P m" | `t = (L + P)/v` |
| "crosses a bridge of B m" | `t = (L + B)/v` |
| "two trains cross each other, opposite directions" | `t = (L1 + L2)/(v1 + v2)` |
| "a train overtakes a man" | `t = L/(v_train − v_man)` |
| "a train overtakes another train, same direction" | `t = (L1 + L2)/(v1 − v2)` |
| "downstream" | `v = b + s` |
| "upstream" | `v = b − s` |
| "travels to B and returns" (equal distances) | `avg = 2xy/(x + y)` |
| "A can do it in a days, B in b days, together" | `T = ab/(a+b)` |
| "A works x days, then B finishes" | Work done by A = `x/a`; rest by B at `1/b` per day |

### Time-and-work: the LCM work-units method

Take the total work as `LCM(a, b)` units. Whole numbers beat fractions.

| Case | A in 12 days, B in 18 days | LCM = 36 units |
|---|---|---|
| A's 1-day work | `36/12` | 3 units |
| B's 1-day work | `36/18` | 2 units |
| Together per day | `3 + 2` | 5 units |
| Time together | `36/5` | **7.2 days** |

For three workers, LCM of all three times.

### Time-and-work variants, pre-computed

| Situation | Formula | Example result |
|---|---|---|
| A in `a`, B in `b`, together | `ab/(a+b)` | 12 & 18 → 7.2 days |
| A in `a`, B in `b`; A works `x` days, B finishes | `x + b(1 − x/a)` | 12 & 18, A works 4 → 16 days |
| A in `a`, B in `b`; A leaves after `x` days, B finishes alone | `x + b(1 − x/a)` | same formula |
| A works every second day | Rate = `(1/a)/2` | — |
| A is `k` times as efficient as B, together in `T` days | A alone = `kT/(k+1)`, B alone = `T/(k+1)` | k = 2, T = 12 → A 8, B 4 |
| Work and wages: A : B efficiency = `b : a` | Divide the wage by efficiency | — |

### The "same work, different days" shortcut

If A does in 6 days what B does in 10 days, then in one day A does `10/6` of B's output, so
`A : B = 10 : 6 = 5 : 3`. **Efficiency ratio = inverse of time ratio.** This one line answers most
"in how many days" follow-ups.

### Train and boat card

| Situation | Formula |
|---|---|
| Train crosses a pole | `t = L/v` |
| Train crosses a platform | `t = (L + P)/v` |
| Two trains, opposite | `t = (L1 + L2)/(v1 + v2)` |
| Train overtakes a man | `t = L/(v_train − v_man)` |
| Boat downstream | `D = b + s` |
| Boat upstream | `U = b − s` |
| Boat in still water | `b = (D + U)/2` |
| Stream speed | `s = (D − U)/2` |

### Pipe card

| Situation | Rate |
|---|---|
| Fill in `m` min and fill in `n` min, both open | `1/m + 1/n` |
| Fill in `m` min, drain in `n` min, both open | `1/m − 1/n` |

### The chase formula

```
gap closed = (v_faster − v_slower) × time
```

For a man on a bike being chased by a car, the gap is the **distance the car must cover to reach
the man's current position**, which grows while the man rides. Use relative speed × time = initial gap
only when the man is stationary or the gap is defined at the start.

## Worked example

**Q. Two trains, 150 m and 100 m long, move in opposite directions at 54 km/h and 36 km/h. How long
do they take to cross each other?**

A. 6 seconds
B. 10 seconds
C. 16.7 seconds
D. 50 seconds

**Solution**

| Step | Working |
|---|---|
| Convert | `54 × 5/18` = 15 m/s; `36 × 5/18` = 10 m/s |
| Relative speed (opposite → add) | `15 + 10` = 25 m/s |
| Distance to cover | `150 + 100` = 250 m |
| Time | `250 ÷ 25` = **10 seconds** |

**Answer: B (10 seconds).**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| 6 seconds | Counted only the longer train's length: `150 ÷ 25` — you forgot the second train's length |
| 16.7 seconds | Used only the faster train's speed: `250 ÷ 15` |
| 50 seconds | Subtracted the speeds (the same-direction formula): `250 ÷ 5` |

**Note:** even if you skipped the conversion, `54 + 36 = 90 km/h = 25 m/s` gives the same relative
speed — the conversion was not even needed here. It is needed the moment a single speed appears.

**Second example (average speed).**

**Q. A car travels from A to B at 40 km/h and returns along the same road at 60 km/h. What is the
average speed for the whole trip?**

```
Equal distances → harmonic mean:
avg = 2 × 40 × 60 / (40 + 60) = 4800 / 100 = 48 km/h
```

**Answer: 48 km/h** (options: 45, 48, 50, 52.5). Option 50 is the arithmetic mean — the classic
trap — and it is only correct when the speeds are used for equal **times**.

**Third example (time and work variant).**

**Q. A and B can build a wall in 12 and 18 days respectively. A works for the first 4 days alone and
then B works alone until it is finished. How many days in total?**

| Step | Working |
|---|---|
| Work in 36 units | A = 3/day, B = 2/day |
| A's 4 days | `4 × 3` = 12 units |
| Remaining | `36 − 12` = 24 units |
| B's time for 24 units | `24 ÷ 2` = 12 days |
| **Total** | `4 + 12` = **16 days** |

**Answer: 16 days** (options: 14, 15, 16, 18).

## Quick rules

- Convert units once, then stay in them.
- Name the situation before computing.
- Crossing a pole → `L`; platform or bridge → `L + P`.
- Opposite → add speeds; same direction → subtract.
- Downstream `b + s`, upstream `b − s`.
- Average speed = total distance ÷ total time.
- Time and work: add rates. Together `T = ab/(a+b)`.
- LCM work units keep everything whole.
- Efficiency ratio = inverse of time ratio.
- 90 seconds.

## Common traps

| Trap | Wrong answer | Right answer |
|---|---|---|
| Arithmetic mean of speeds | 50 km/h | 48 km/h |
| `× 18/5` used for km/h → m/s | 259 m/s | `× 5/18` |
| Pole treated as platform | 10 s | 25 s |
| Same-direction formula used | 8 s | 10 s |
| Times added instead of rates | 7.5 days | 7.2 days |
| Efficiency ratio inverted | A and B swapped | Inverse of time |
| km/h used as m/s | 5 s | Convert first |

## Checklist

- [ ] I converted the speed to m/s or km/h once, and used it everywhere.
- [ ] I identified pole / platform / bridge / overtaking.
- [ ] I used add or subtract speeds according to direction.
- [ ] I used the harmonic mean for equal-distance average speed.
- [ ] I added rates for combined work.
- [ ] I checked the units on the final answer.
- [ ] I finished inside 90 seconds.

## Related

- [Ratio, time, speed & distance rules](../01-concepts/01-ratio-speed-distance-rules.md)
- [Solved speed and time set](../03-worked-examples/01-solved-speed-time-set.md)
- [Speed and time traps](../04-pitfalls/01-speed-time-traps.md)
- [Speed and time one-pager](../05-reference/01-speed-time-one-pager.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
