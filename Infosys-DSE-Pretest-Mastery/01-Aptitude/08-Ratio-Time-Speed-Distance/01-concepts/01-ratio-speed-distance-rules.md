# Ratio, Time, Speed & Distance — The Rules

> Section 1 · Aptitude · Ratio, Time, Speed & Distance · _Estimated reading time: 10 min_
> **Prerequisite:** [Percentages, Profit/Loss & Discount](../../02-Percentages-Profit-Loss-Discount/README.md)

## In one sentence

Every question in this topic is one of three ideas — **ratio is a fraction, speed is distance over
time, and work is rate multiplied by time** — plus the unit conversions that trip people up.

## Why the pre-test tests this

- Speed–distance is the most common aptitude topic in the Infosys DSE pre-test. Expect **2–3
  questions**: one unit conversion, one average speed, one train or boat.
- Time and work appears less often but uses the same rate logic.
- The arithmetic is easy. The losses come from **unit slips** (m/s vs km/h) and from the two classic
  average-speed and combined-work traps.

## Core concept

### 1. Ratio and proportion

A ratio `a : b` means `a/b`. Two rules cover almost everything:

**Rule A — divide by the GCD.** `18 : 24` → `3 : 4`.

**Rule B — a ratio is a fraction of the whole.** If the total is `T`, then each part is `T/(a+b)`
and the two shares are `a·T/(a+b)` and `b·T/(a+b)`.

| What is asked | Method |
|---|---|
| Value of one part | `T / (a + b)` |
| Value of one share | `a × T/(a+b)` |
| New ratio after adding `x` to one share | Recompute both shares, reduce |
| Ratio of two ratios | Divide term by term |
| Ratio of A's share to B's share | `a/b` directly |

**Shortcut for ratio changes.** If `x` units are added to the first share, the new ratio is
`(a + x·k) : (b·k)` where `k = T/(a+b)` is one part. Work in parts, not in the raw numbers.

### 2. Speed, time and distance

```
Distance = Speed × Time        Speed = Distance / Time        Time = Distance / Speed
```

Keep the three consistent. Most errors are unit errors, not formula errors.

### 3. Unit conversion — the one you must be automatic at

| From | To | Multiply / divide by |
|---|---|---|
| km/h | m/s | `× 5/18` |
| m/s | km/h | `× 18/5` |
| km/h | km/min | `÷ 60` |
| km/min | km/h | `× 60` |
| m/s | km/min | `× 3/60` = `÷ 20` |
| minutes | seconds | `× 60` |
| hours | minutes | `× 60` |
| hours | seconds | `× 3600` |
| days | hours | `× 24` |

**Why `5/18`.** `1 km/h = 1000 m / 3600 s = 5/18 m/s`. Memorise the pair, not the arithmetic.

**Common speeds worth knowing instantly**

| Speed | m/s |
|---|---|
| 18 km/h | 5 |
| 36 km/h | 10 |
| 54 km/h | 15 |
| 72 km/h | 20 |
| 90 km/h | 25 |
| 108 km/h | 30 |

### 4. Average speed

```
Average speed = Total distance / Total time
```

**Never average the two speeds.** That is only correct when the two speeds are used for **equal
times**, not equal distances.

| Situation | Average speed |
|---|---|
| Equal distances, speeds `x` and `y` | `2xy/(x + y)` (harmonic mean) |
| Equal times, speeds `x` and `y` | `(x + y)/2` |
| Equal distances at 40 and 60 km/h | `48 km/h` |
| Equal times at 40 and 60 km/h | `50 km/h` |

### 5. Trains, platforms and crossings

| Situation | Distance to cover | Time |
|---|---|---|
| Train crosses a **pole** | Train's own length `L` | `L / v` |
| Train crosses a **platform** | `L + P` | `(L + P) / v` |
| Train crosses a **bridge** | `L + B` | `(L + B) / v` |
| Two trains cross in **opposite directions** | `L1 + L2` | `(L1 + L2)/(v1 + v2)` |
| Two trains cross in the **same direction** | `L1 + L2` | `(L1 + L2)/(v1 − v2)` |
| A train **overtakes a man** | Train's length `L` | `L/(v_train − v_man)` |

### 6. Boats and streams

| Quantity | Formula |
|---|---|
| Downstream speed | `b + s` |
| Upstream speed | `b − s` |
| Speed of the boat in still water | `b = (D + U)/2` |
| Speed of the stream | `s = (D − U)/2` |

`b` = boat in still water, `s` = stream speed, `D` = downstream, `U` = upstream.

### 7. Relative speed

| Situation | Relative speed |
|---|---|
| Moving in **opposite** directions | `v1 + v2` |
| Moving in the **same** direction | `v1 − v2` (the faster minus the slower) |

Distance travelled to close a gap = `relative speed × time`.

### 8. Time and work

```
Work = Rate × Time
```

If A alone finishes in `a` days, A's rate is `1/a` of the work per day.

| Situation | Formula |
|---|---|
| A and B together, in `a` and `b` days | `T = ab/(a+b)` days |
| A and B together, work `W` units | `W/(1/a + 1/b)` |
| A works `x` days, then B finishes alone | `x/a + (b·T_remaining)/b` |
| A does in 6 days what B does in 10 days | Efficiency A : B = `10 : 6` = `5 : 3` |
| A is twice as efficient as B, together in 12 days | A does 24 days' work, B 36 days' work |

**The "work units" method.** Take the total work as `LCM(a, b)` units. Then A's one-day output is
`LCM/a` units and B's is `LCM/b`. This keeps everything whole-number and is faster than fractions.

### 9. Pipes and cisterns

Pipes are time-and-work with a twist: a drain pipe has a **negative** rate.

| Situation | Formula |
|---|---|
| Fill in 20 min and fill in 30 min, both open | `1/20 + 1/30 = 1/12` → 12 min |
| Fill in 20 min, drain in 30 min, both open | `1/20 − 1/30 = 1/60` → 60 min |

## Worked example

**Q. A train 200 m long runs at 72 km/h. How long does it take to cross a platform 300 m long?**

A. 10 seconds
B. 15 seconds
C. 20 seconds
D. 25 seconds

**Solution**

| Step | Working |
|---|---|
| Convert the speed | `72 × 5/18` = **20 m/s** |
| Distance to cover | train length + platform = `200 + 300` = 500 m |
| Time | `500 ÷ 20` = **25 seconds** |

**Answer: D (25 seconds).**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| 10 seconds | Crossing a **pole** (200 m ÷ 20 m/s) — you forgot the platform |
| 15 seconds | 300 m ÷ 20 m/s — you counted only the platform |
| 20 seconds | 400 m ÷ 20 m/s — you added the lengths wrongly |

**Note the trap structure:** option A is exactly the "crossing a pole" answer, and option B is the
"platform only" answer. Both are wrong because the train must cover its own length **plus** the
platform.

**Second example (time and work).**

**Q. A can complete a piece of work in 12 days and B in 18 days. How long will they take together?**

```
A's 1-day work = 1/12
B's 1-day work = 1/18
Together      = 1/12 + 1/18 = (3 + 2)/36 = 5/36
Time          = 36/5 = 7.2 days
```

**Answer: 7.2 days** (options: 6, 7.2, 7.5, 30). The trap is 6 days — the answer if you average
12 and 18 incorrectly, or if you assume each does half the work in half the time.

## Quick rules

- Ratio: divide by the GCD; a ratio is a fraction of the whole.
- `km/h → m/s` is `× 5/18`; `m/s → km/h` is `× 18/5`.
- Average speed = total distance ÷ total time. Equal distances → harmonic mean `2xy/(x+y)`.
- Crossing a pole → train length. Crossing a platform → length + platform.
- Opposite directions → add speeds. Same direction → subtract.
- Downstream `b + s`, upstream `b − s`, so `b = (D + U)/2`.
- Time and work: add **rates**, not times. Together `T = ab/(a+b)`.
- Drain pipes subtract.
- Use LCM work units to stay in whole numbers.
- 90 seconds for a speed question.

## Common traps

| Trap | Symptom | Fix |
|---|---|---|
| Average of two speeds for equal distances | 50 instead of 48 | Use `2xy/(x+y)` |
| Wrong conversion multiplier | 20 km/h for 72 km/h | `× 5/18` |
| Crossing a pole counted as a platform | 10 s instead of 25 s | Length + platform |
| Same-direction relative speed added | Too small a time | Subtract |
| Times added instead of rates | 7.5 days instead of 7.2 | `ab/(a+b)` |
| Rate ratio inverted | A and B swapped | Efficiency ratio is inverse of time |
| Distance ratio = speed ratio | Wrong chase answer | Only when times are equal |
| Seconds and minutes mixed | Off by 60× | Convert once, early |

## Checklist

- [ ] I converted the speed to one consistent unit before computing.
- [ ] I used total distance ÷ total time for average speed.
- [ ] I added the train length to the platform or bridge length.
- [ ] I subtracted speeds for same-direction overtaking.
- [ ] I added rates (not times) for time and work.
- [ ] I checked the answer against the input range.
- [ ] I finished inside 90 seconds.

## Related

- [Speed, time and work procedures](../02-techniques/01-speed-time-procedures.md)
- [Solved speed and time set](../03-worked-examples/01-solved-speed-time-set.md)
- [Speed and time traps](../04-pitfalls/01-speed-time-traps.md)
- [Speed and time one-pager](../05-reference/01-speed-time-one-pager.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
