# Speed and Time Traps — Ten Ways to Lose the Mark

> Section 1 · Aptitude · Ratio, Time, Speed & Distance · _Estimated reading time: 7 min_
> **Prerequisite:** [Solved speed and time set](../03-worked-examples/01-solved-speed-time-set.md)

## In one sentence

Every trap in this topic is a **misread of the situation** — equal times vs equal distances, pole vs
platform, adding vs subtracting — and every wrong option in the question bank is one of them.

## Why the pre-test tests this

- The formulas are correct in almost every wrong answer. The *situation* is wrong.
- Learning the trap → wrong-option mapping means you can **eliminate** options on sight, which
  saves time even when you are unsure.
- Rahul's experience: "I knew the formula but chose the pole answer because I read fast." Reading
  is a skill, and this list is how you train it.

## Core concept

### Trap 1 — averaging the two speeds

**Symptom:** you write `(40 + 60)/2 = 50` for a round trip.

| Situation | Correct method | Answer |
|---|---|---|
| Equal **distances** | `2xy/(x + y)` | 48 km/h |
| Equal **times** | `(x + y)/2` | 50 km/h |

**Fix:** ask "was the car moving for the same time, or covering the same distance?" A round trip is
equal distances.

### Trap 2 — wrong conversion multiplier

| Direction | Multiplier | Check |
|---|---|---|
| km/h → m/s | `× 5/18` | Result is **smaller** (÷3.6) |
| m/s → km/h | `× 18/5` | Result is **larger** (×3.6) |

**Fix:** 1 km/h = 1000 m in 3600 s = 0.278 m/s, so the multiplier is less than 1. If your m/s answer
is bigger than the km/h number, you inverted it.

### Trap 3 — pole vs platform vs bridge

| Stem | Distance the train covers |
|---|---|
| "crosses a pole" | `L` |
| "crosses a platform of P m" | `L + P` |
| "crosses a bridge of B m" | `L + B` |

**Fix:** the train must cover its own length **plus** whatever it passes.

### Trap 4 — subtracting speeds for opposite directions

**Symptom:** you use `v1 − v2` when the trains move toward each other.

| Situation | Relative speed |
|---|---|
| Opposite directions | **Add** |
| Same direction | **Subtract** |

**Fix:** ask which way the gap closes — if the gap closes from both sides, add.

### Trap 5 — adding times instead of rates

**Symptom:** A in 12 days, B in 18 days, and you answer 30 days, or you average them to 15.

**Fix:** rates add: `1/12 + 1/18 = 5/36` → `36/5 = 7.2` days.

| Wrong | Right |
|---|---|
| 12 + 18 = 30 days | `ab/(a+b)` = 7.2 days |
| (12 + 18)/2 = 15 days | `ab/(a+b)` = 7.2 days |

### Trap 6 — the efficiency ratio inverted

**Symptom:** "A does in 6 days what B does in 10 days" → you write A : B = 6 : 10.

**Fix:** the **faster** worker has the **bigger** share. `A : B = 10 : 6 = 5 : 3`. Efficiency ratio is
the **inverse** of the time ratio.

### Trap 7 — assuming distance ratio = speed ratio

**Symptom:** "A is twice as fast as B, so A travels twice as far in the same time."

**Fix:** that is true only if the **times are equal**. If the times differ, you need the actual times.

| Statement | True only when |
|---|---|
| Distance ratio = Speed ratio | Times are equal |
| Distance ratio = Inverse of speed ratio | Distances are equal (which is not a distance ratio) |

### Trap 8 — minutes and seconds mixed

**Symptom:** "20 minutes" and "20 seconds" in the same calculation.

**Fix:** convert once, at the start. If the answer is in seconds, everything must be in metres and
seconds.

### Trap 9 — forgetting what the overtaking object contributes

**Symptom:** a train overtakes a man; you use `L + something` for the man.

**Fix:** a man is a point. The train covers **its own length** to fully pass him: `t = L/(v_train −
v_man)`. For a **train overtaking a train**, add both lengths.

### Trap 10 — the drain pipe treated as a fill pipe

**Symptom:** fill in 20 min, drain in 30 min, and you write `1/20 + 1/30` → 12 minutes.

**Fix:** a drain removes, so its rate is negative: `1/20 − 1/30 = 1/60` → 60 minutes. The answer must
be **longer** than the fill time alone, and that is your sanity check.

## Worked example

**Q. A car travels from A to B at 40 km/h and returns along the same road at 60 km/h. What is the
average speed for the whole trip?**

A. 45 km/h
B. 48 km/h
C. 50 km/h
D. 52.5 km/h

**The trap:** 50 km/h sits in the middle of the option list and *feels* right. It is the arithmetic
mean, and it is correct only for equal **times**.

**The reading that decides it**

| Question | Answer | Consequence |
|---|---|---|
| Did the car cover equal **distances**? | Yes — out and back | Use the harmonic mean |
| Did the car travel for equal **times**? | No — 3 h out, 2 h back | The simple average is invalid |

**Solution (harmonic mean)**

```
avg = 2xy/(x + y) = 2 × 40 × 60 / 100 = 48 km/h
```

**Solution (proof by construction)** — take each leg as 120 km:

| Leg | Speed | Distance | Time |
|---|---|---|---|
| Outward | 40 km/h | 120 km | 3 h |
| Return | 60 km/h | 120 km | 2 h |
| Total | — | 240 km | 5 h |

`240 ÷ 5 = 48 km/h` ✅

**Answer: B (48 km/h).**

**Distractor mapping**

| Option | The mistake behind it |
|---|---|
| 45 km/h | Subtraction, not averaging |
| 50 km/h | Arithmetic mean — the equal-times method applied to an equal-distances question |
| 52.5 km/h | Averages 45 and 60 for no reason |

**The general rule:** read the stem for **what is equal** — equal distances, equal times, or neither.
That single sentence decides the formula.

## Quick rules

- km/h → m/s `× 5/18`; m/s → km/h `× 18/5`.
- Average speed = total distance ÷ total time.
- Equal distances → `2xy/(x+y)`; equal times → `(x+y)/2`.
- Pole → `L`; platform or bridge → `L + P`.
- Opposite → add; same direction → subtract.
- Downstream `b + s`, upstream `b − s`, `b = (D+U)/2`.
- Time and work: add rates; `T = ab/(a+b)`.
- Efficiency ratio = inverse of time ratio.
- A man is a point; a train is a length.
- 90 seconds.

## Common traps

| Trap | Wrong answer | Right answer |
|---|---|---|
| Arithmetic mean of speeds | 50 km/h | 48 km/h |
| Inverted conversion | 259 m/s | `× 5/18` |
| Pole treated as platform | 10 s | 25 s |
| Subtracting for opposite directions | 50 s | 10 s |
| Times added | 30 or 15 days | 7.2 days |
| Efficiency ratio inverted | 6 : 10 | 10 : 6 |
| Drain treated as fill | 12 min | 60 min |
| Man's size added to the train | Over-long distance | Train length only |

## Checklist

- [ ] I read the stem for what is equal (distances or times).
- [ ] I converted units once, in the right direction.
- [ ] I identified pole / platform / bridge / overtaking.
- [ ] I added or subtracted speeds according to the direction of travel.
- [ ] I added rates for work and subtracted for drains.
- [ ] I checked the answer is in a sensible range.
- [ ] I finished inside 90 seconds.

## Related

- [Ratio, time, speed & distance rules](../01-concepts/01-ratio-speed-distance-rules.md)
- [Speed, time and work procedures](../02-techniques/01-speed-time-procedures.md)
- [Solved speed and time set](../03-worked-examples/01-solved-speed-time-set.md)
- [Speed and time one-pager](../05-reference/01-speed-time-one-pager.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
