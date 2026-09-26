# Clamping Circuits — Practice (Learn by Solving)

> **The idea in one line:** this file teaches the whole of Chapter 04 through 36
> questions — a clamper *shifts* a whole waveform without touching its shape, and
> you learn it by computing shifts, not by reading about them.
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve
> the next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `04-Clamping-Circuits.md` or `32-Single-File-Cheatsheet.md` only when you want
> the underlying theory.

## Concept box (what you must internalise)

- **Clipper cuts shape; clamper shifts DC level.** A capacitor in the branch ⇒
  clamp. No capacitor ⇒ clip. That is the whole classification test.
- **Amplitude and shape are never changed.** A `±Vm` sine becomes a
  `0 … 2Vm` (or `−2Vm … 0`) wave — the p-p is still `2Vm`.
- Diode anode on the **input** side ⇒ **positive** clamp (shift up, bottom touches
  0). Cathode on the input side ⇒ **negative** clamp (shift down, top touches 0).
- General rule that solves every clamper: **shift the waveform until its most
  negative point sits at `V_ref` (positive clamp) or its most positive point sits
  at `V_ref` (negative clamp).** The shift is `−V_min` or `−V_max`.
- Silicon adds **0.7 V** to the reference: a positive silicon clamper's bottom sits
  at `+0.7 V`, not 0.
- Between diode pulses the capacitor **discharges through `R_L`** — droop is a
  discharge, never a charge. Droop fraction over the non-conducting half-period =
  `1 − e^(−(T/2)/(R_L·C))`.
- Design rule: `R_L·C ≫ T`; for under 1 % droop you need `R_L·C ≳ 50·T`.

---

## Questions

### Q1. (Easy) Positive clamper, **ideal** diode, `R_L·C ≫ T`, sine input
`±5 V`. Give the output range and the vertical shift.
**Answer:** Range **0 V to +10 V**; shift = **+5 V**.
**Method:** The diode conducts on the negative peak, charging `C` to `Vm = 5 V`; the
output is then `v_in + 5 V`. Write the output as an equation first —
`v_out = v_in − V_min = v_in − (−5) = v_in + 5` — and the range falls out
automatically. The signal that swung `±5` now swings `0 … +10`: **same 10 V p-p,
new DC level.**

---

### Q2. (Easy) **Negative** clamper, ideal, sine `±5 V`. Output range and shift?
**Answer:** Range **−10 V to 0 V**; shift = **−5 V** (`v_out = v_in − V_max = v_in − 5`).
**Method:** Diode flipped ⇒ it conducts on the *positive* peak, charging `C` to
`−5 V`. Sanity check: the two answers in Q1 and Q2 are exact mirror images, which
is the quickest way to catch a sign error.

---

### Q3. (Easy) In Q1 and Q2, what is the peak-to-peak value of the output compared
with the input? Does the clamper gain or lose amplitude?
**Answer:** Input p-p = 10 V; output p-p = 10 V in **both** cases. **Amplitude is
unchanged** — only the DC level moves.
**Method:** This is the #1 misconception in this chapter (students "clip" a
clamper by accident). A clamper is a **DC level shifter**: it is an AC coupling
network plus a diode that restores a chosen reference. If the p-p changes, you
have accidentally solved a clipper problem.

---

### Q4. (Easy) Positive clamper with a **silicon** diode (0.7 V), sine `±5 V`. What
is the bottom of the output, and the range?
**Answer:** Bottom = **+0.7 V**; range **+0.7 V to +10.7 V**; shift = **+5.7 V**.
**Method:** The conducting diode is a 0.7 V drop, so the output's lowest value is
`+0.7 V`, not 0. Equivalently: `C` charges to `Vm + 0.7 = 5.7 V`, so
`v_out = v_in + 5.7`. **Silicon always moves the clamp level 0.7 V away from the
reference, in the direction of the clamp.**

---

### Q5. (Easy) Negative clamper, **silicon**, sine `±5 V`. Range and shift?
**Answer:** Top = **−0.7 V**; range **−10.7 V to −0.7 V**; shift = **−5.7 V**.
**Method:** Mirror of Q4. `C` charges to `−(Vm + 0.7) = −5.7 V`, so
`v_out = v_in − 5.7` and the top lands at `−0.7`. The two silicon clampers differ
from the two ideal ones (Q1, Q2) by exactly **0.7 V in the shift** and nothing
else.

---

### Q6. (Easy) Positive clamper biased to a **+2 V** reference, ideal diode,
`v_in = 5 sin ωt`. Output range?
**Answer:** Bottom at **+2 V**, so range **+2 V to +12 V**; shift = **+7 V**
(= `2 + 5`).
**Method:** Biased positive clamper: slide the wave up until its *minimum* sits at
`V_ref = +2 V`. `v_out = v_in − V_min + 2 = v_in + 5 + 2 = v_in + 7`. Remember the
bias adds to the shift **once** — not twice (a classic trap: `5 + 2 + 2`).

---

### Q7. (Easy) Same as Q6 but the diode is **silicon**. Output range?
**Answer:** Bottom at `2 + 0.7 = ` **+2.7 V**; range **+2.7 V to +12.7 V**; shift **+7.7 V**.
**Method:** Q4's rule applied to a biased clamper: **reference + 0.7**. Both ends
move up by 0.7 V; the p-p is still 10 V.

---

### Q8. (Easy) Negative clamper with a **−4 V** reference, ideal,
`v_in = 10 sin ωt`. Output range?
**Answer:** Top at **−4 V**; range **−24 V to −4 V**; shift = **−14 V**
(= `−(10 + 4)`).
**Method:** Negative biased clamper: slide down until the *maximum* sits at
`V_ref = −4 V`. `v_out = v_in − V_max + V_ref = v_in − 10 − 4 = v_in − 14`. p-p is
still 20 V. Compare with the ideal negative clamper on the same input (shift −10 V):
the bias simply *adds* its magnitude to the downward shift.

---

### Q9. (Moderate) A symmetric triangle `−5 V ↔ +5 V` goes into a positive clamper
(ideal, `RC ≫ T`). Give the output range and describe the shape.
**Answer:** Range **0 V to +10 V**; still a **triangle** (identical shape, twice the
level).
**Method:** Clampers are shape-agnostic — nothing in the operation depends on the
waveform being a sine. Use `V_min = −5` ⇒ `v_out = v_in + 5`. The reason students
reach for `sin⁻¹` here is that they have imported a clipper habit; a clamper never
needs a conduction angle.

---

### Q10. (Moderate) A **0 ↔ +10 V** square wave goes into a positive clamper
(ideal, `RC ≫ T`). What is the output?
**Answer:** **Unchanged: 0 V to +10 V.** The shift is `−V_min = −0 = 0`.
**Method:** A great trap: the input is *already* entirely non-negative, so its
minimum is 0 and the positive clamp has nothing to do. `V_C = |V_min| = 0`.
The general test: *"a positive clamper shifts by `−V_min`; if `V_min ≥ 0` there is
no shift."* Similarly a negative clamper on a `0 ↔ −10 V` square also does nothing.

---

### Q11. (Moderate) A **−5 ↔ +5 V** square wave goes into a positive clamper (ideal).
Output range, and what happens to the shape?
**Answer:** Shift `−V_min = +5` ⇒ range **0 V to +10 V**. Still a square wave: it
became a **unipolar 0–10 V square** (the input was already bipolar about 0).
**Method:** Same as Q9 but with a square. Note the *input* average was 0 V and the
*output* average is +5 V — a clamper is exactly a DC restorer. This is the same
mechanism as a DC blocker in an AC-coupled amplifier, except the diode chooses a
specific reference.

---

### Q12. (Moderate) A **0 ↔ +10 V** square wave goes into a **negative** clamper
(ideal). Output range? Is the result a level shift or an inversion?
**Answer:** `V_C = V_max = 10` ⇒ range **−10 V to 0 V**; shift = **−10 V**. It is a
pure **level shift, not an inversion** — the +10 V level goes to 0 V and the 0 V
level goes to −10 V.
**Method:** The classic "inverting level shifter". The order of the levels swaps
because the *whole* wave is translated, so if you track labels instead of levels
it looks inverted; track *levels* and it is obviously just a shift. The chapter's
own worked example in `04-Clamping-Circuits.md` §4.5 shows exactly this problem
and warns against the "inversion" misreading.

---

### Q13. (Moderate) Find the **average (DC) value** and the **RMS** of the output of
a positive clamper (ideal) fed with `v_in = 10 sin ωt`.
**Answer:** `v_out = 10 + 10 sinωt`. Average = **+10 V**.
RMS = `10·sqrt(1 + 2·⟨sin⟩ + ⟨sin²⟩) = 10·sqrt(1 + 0 + 0.5) = 10·1.2247 = ` **12.25 V**.
**Method:** Expand the square: `(1 + sinθ)² = 1 + 2sinθ + sin²θ`; the averages of `sin`
and `sin²` are 0 and 0.5. So the factor is `sqrt(1.5) = 1.2247`. The DC of a
positively clamped sine equals the shift, `+Vm` — a 30-second check worth having.

---

### Q14. (Moderate) A negative clamper (ideal) on `10 sin ωt`: average and RMS?
**Answer:** Average = **−10 V**; RMS = **12.25 V** — the *same* RMS as Q13.
**Method:** The output is `−10(1 + sinθ)`, whose average is −10 V. RMS is
insensitive to the sign of the whole waveform, so it is unchanged. **General
point: a clamper changes the average and the peak values, but not the RMS (for
ideal clampers).** The RMS is the only "size" measure a clamper leaves alone.

---

### Q15. (Moderate) A clamper has `R_L = 1 kΩ`, `C = 1 µF`, and the input period is
`T = 1 ms`. What fraction of the stored voltage is lost by droop during the
non-conducting half-period?
**Answer:** `τ = R_L C = 1 ms`; the diode is off for `T/2 = 0.5 ms`;
droop `= 1 − e^(−0.5/1) = 1 − 0.6065 = ` **39.3 %**.
**Method:** Two numbers then one formula: `τ = R_L·C`, discharge interval
`Δt = T/2` (a clamper's diode is off for *half* the cycle), fraction
`1 − e^(−Δt/τ)`. Here `τ = T` exactly, which is a deliberately bad design — 39 %
sag is a visibly triangular, not flat, clamp. Sanity: droop always increases as
`τ` shrinks.

---

### Q16. (Moderate) Same clamper, but `C = 2 µF`. Droop fraction now?
**Answer:** `τ = 2 ms`; `1 − e^(−0.5/2) = 1 − e^(−0.25) = 1 − 0.7788 = ` **22.1 %**.
**Method:** Identical template with `τ = 2 ms`. Compare Q15: doubling `C` halved
the *exponent* (0.5 → 0.25), which cut the droop from 39.3 % to 22.1 % — droop is
**exponential** in `1/(RC)`, not linear, so "double C" gives less than half the
improvement once droop is already small. For small droop, `1 − e^(−x) ≈ x`, and
then doubling C *does* halve it.

---

### Q17. (Moderate) Same clamper, but `C = 10 µF`. Droop fraction? Is this a
"good" clamper?
**Answer:** `τ = 10 ms`; `1 − e^(−0.05) = 1 − 0.9512 = ` **4.88 %**. It is a *usable*
clamper, but 5 % sag of a 10 V peak is 0.5 V of tilt per cycle — visible on a
scope, acceptable for many signals.
**Method:** `1 − e^(−0.05) = 4.88 %`. The design judgement: for a clean clamp you
want droop under ~1 %, i.e. `R_L·C ≳ 50·T` (Q21). Rule of thumb from the three
data points: Q15 (τ = T) → 39 %, Q16 (τ = 2T) → 22 %, Q17 (τ = 10T) → 5 %.

---

### Q18. (Moderate) During the non-conducting interval, is the capacitor **charging**
or **discharging**, and through what path?
**Answer:** **Discharging**, through `R_L`. The diode is reverse biased (an open),
so the only closed path is `C → R_L → ground`.
**Method:** Follow the current path. During conduction the diode shorts and `C` is
*charged* in one quick pulse; between pulses the diode opens and the load bleeds
`C` away. GATE states this as a binary choice — the answer is always
**discharge**, and the droop is always *toward* the reference level, never past it.
This also explains why the clamper's reference is a *floor/ceiling* rather than
an exact value.

---

### Q19. (Moderate) In a clamper's **steady state**, what is the diode's average
current over one cycle? What is the average current into the capacitor?
**Answer:** Both are **zero**. The diode conducts in brief pulses that deliver
exactly the charge lost through `R_L` during the off interval.
**Method:** Steady state means the capacitor's voltage repeats every cycle, so
`ΔV_C = 0`, so `⟨i_C⟩ = 0`. Charge in = charge out. This is the cleanest proof
that the offset you computed is a genuine DC equilibrium and not a transient — and
it is why the first cycle or two looks different (Q31).

---

### Q20. (Moderate) What happens to the output of a clamper if `R_L → ∞` (open
load)?
**Answer:** No discharge path ⇒ **no droop whatsoever**; the offset is held
indefinitely. The diode then conducts only in an infinitesimal sliver at the very
peak, and the average diode current is exactly zero. This is the *ideal* clamper.
**Method:** `τ = R_L C → ∞` ⇒ `1 − e^(−(T/2)/τ) → 0`. The practical version of
"very large `R_L`" is a high-impedance next stage (a FET input or an op-amp input,
`R_in ≈ 10¹² Ω`), which is why MOSFET-input amplifiers follow clippers nicely.

---

### Q21. (Moderate) A clamper must keep droop below **1 %** on a 1 kHz signal.
What minimum `R_L·C` is required?
**Answer:** Droop `= 1 − e^(−x) < 0.01` ⇒ `x < −ln(0.99) = 0.01005` ⇒
`τ > (T/2)/0.01005 = (0.5 ms)/0.01005 = 49.75 ms ≈ ` **50·T**.
With `T = 1 ms`: `R_L·C ≳ ` **50 ms**.
**Method:** Invert the droop formula for the *small-droop* approximation:
`droop ≈ Δt/τ = (T/2)/τ`, so `τ ≥ (T/2)/droop`. 0.5 ms/0.01 = 50 ms. Since
`T = 1/f = 1 ms`, that is `R_L·C ≥ 50/f`. Handy design formula: for a 1 % ripple at
1 kHz you need a 50 ms time constant, e.g. `C = 0.05 µF` with `R_L = 1 MΩ`.

---

### Q22. (Moderate) What is the **reverse voltage** (PIV) the diode in a clamper must
block, for `v_in = ±10 V`?
**Answer:** **10 V.** When the diode is off it sees the full capacitor voltage,
which is `V_C = |V_min| = Vm = 10 V`.
**Method:** During the off interval the diode is in series with the charged
capacitor, so it blocks exactly `V_C` — never `2V_C`, and never the input
peak-to-peak by default.

Derive `V_C` from the clamp itself: the capacitor charges until the output's
extreme sits at the reference, so `V_C` is **the distance from the reference to the
input extreme on the other side** — i.e. exactly how far the output gets shifted.
For a sine `±Vm` with a 0 reference, `V_C = Vm = 10 V`.

⚠️ `V_C` equals the input **peak-to-peak** *only when the reference coincides with
one input extreme*:

| Input | Clamper | Reference | `V_C` = PIV |
|---|---|---|---|
| `±10 V` sine | positive | 0 V | **10 V** |
| `0 ↔ +10 V` | positive | 0 V | **0 V** (diode never conducts) |
| `−5 ↔ +5 V` | positive | 0 V | **5 V** (not the 10 V p-p!) |
| `0 ↔ +10 V` | negative | 0 V | **10 V** |

The `−5 ↔ +5 V` case is the trap: the output swings 0 → 10 V, but the capacitor
only ever holds 5 V, and the diode only ever blocks 5 V.

---

### Q23. (Moderate) A `0 ↔ +10 V` square wave drives a **negative** clamper (ideal).
Find the capacitor's steady-state voltage and the output range.
**Answer:** `V_C = V_max = ` **10 V**; output range **−10 V to 0 V**.
**Method:** Step 1: which extreme reaches the diode's conducting half-cycle? For a
negative clamper that is the **maximum**, so `V_C = V_max`. Step 2: subtract it:
`v_out = v_in − 10`, so 0 → −10 and 10 → 0. Always state `V_C` first — it is the
number the whole problem hangs on.

---

### Q24. (Moderate) Design: a positive clamper must place a `±6 V` sine entirely in
the range **0 to +12 V**. What capacitor voltage is required, and what must the
reference be?
**Answer:** `V_C = Vm = ` **6 V** (charged on the negative peak). Reference =
**0 V** (ideal diode) — so it is an ordinary ground-referenced positive clamper, no
bias needed.
**Method:** Design backwards: for a sine the required capacitor voltage is always
exactly `Vm`; then `V_ref = ` whatever you want the output's floor to be
(`0 V` ⇒ 0 ↔ 2Vm, `+2 V` ⇒ 2 ↔ 14 V). The two design questions are independent and
always asked in that order: *how much charge, and to what level.*

---

### Q25. (GATE-level) A **positive clamper is followed by a biased positive clipper
at +6 V** (both ideal). Input `v_in = 10 sin θ`. Describe `v_out` and find the
conduction window of the clipper's diode.
**Answer:** The clamper gives `10(1 + sinθ)`, range 0–20 V. The clipper then pins
anything above 6 V: output range **0 V to +6 V**. The clipper conducts when
`10(1 + sinθ) > 6` ⇒ `sin θ > −0.4` ⇒ `θ₁ = −23.58°`, i.e. conduction from
**−23.58° to 203.58°** (width 227.16°). Average `≈ ` **+4.56 V**.
**Method:** The cascade is a *clamp-then-slice*. Crucially, the clipper's
threshold is applied to the **clamped** signal, so `sin θ > −0.4`, not
`sin θ > 0.6`. This is the classic exam trap in cascaded non-linear stages:
**always write the intermediate waveform before touching the next stage.**
The negative `sin θ` value is the tell-tale that the DC shift matters.

---

### Q26. (GATE-level) Compute the average and RMS of the output of a positive clamper
with a **+2 V reference** fed with `v_in = 5 sin ωt` (ideal).
**Answer:** `v_out = 7 + 5 sinθ`. Average = **+7 V**.
RMS = `sqrt(7² + 5²/2) = sqrt(49 + 12.5) = sqrt(61.5) = ` **7.84 V**.
**Method:** For `v_out = A + B sinθ`, `⟨v⟩ = A` and
`V_rms = sqrt(A² + B²/2)` (the cross term averages to zero). Here `A = Vm + V_ref = 7`
and `B = Vm = 5`. Sanity: RMS must lie between the peak (12 V) and the
average (7 V) — 7.84 V ✔. Same formula gives Q13: `sqrt(100 + 50) = 12.25` ✔.

---

### Q27. (GATE-level) A **negative clamper, silicon**, `v_in = ±10 V`, `R_L·C ≫ T`.
Give the output range, the capacitor voltage, and the diode's PIV.
**Answer:** Range **−20.7 V to −0.7 V**; shift **−10.7 V**;
`V_C = −(Vm + 0.7) = −10.7 V`; **PIV = 10.7 V**.
**Method:** Three numbers from three different principles:
(1) range: reference **+ 0.7** ⇒ top = −0.7 V, p-p = 20 V ⇒ bottom = −20.7 V;
(2) `V_C` = the shift, since `v_out = v_in + V_C`;
(3) PIV = `|V_C|` (Q22). Notice the PIV **grows** when you add silicon — the
0.7 V lands on the reverse blocking requirement as well as the level. Design
implication: a silicon clamper needs a slightly higher PIV rating than an ideal one.

---

### Q28. (GATE-level) A composite video signal has sync tips at **−4 V** and a white
level at **+1 V** (total swing 5 V). A **positive clamper with a 0 V reference** and
a silicon diode feeds a monitor. What are the sync-tip and white levels at the
output, and what must the coupling capacitor's PIV be?
**Answer:** Sync tips land at **+0.7 V**; white level = 0.7 + 5 = **+5.7 V**.
PIV ≥ **4.7 V** (`V_C = 4 + 0.7`).
**Method:** This is a **DC restorer** — the most important real use of a clamper.
The positive clamper slides the whole composite signal so the sync tips (the most
negative excursion) rest at the reference `+0.7 V`. The picture information is
preserved exactly (5 V swing untouched), only the DC is reset — which is why a
clamper is the right stage here and a clipper would be catastrophic.
In a TV the reference is deliberately a bit *above* the wanted blanking level so
the sync tips sit slightly negative, but the principle is identical.

---

### Q29. (GATE-level) Give the general steady-state rule for an **arbitrary** periodic
input, then apply it to `v_in = 2 V DC + 4 sin ωt` through a positive clamper
(ideal). Output range and average?
**Answer:** Rule: positive clamper ⇒ `V_C = −V_min`, output `v_in − V_min`;
negative clamper ⇒ `V_C = V_max`, output `v_in − V_max`.
Here `V_min = 2 − 4 = −2 V` ⇒ `V_C = +2 V` ⇒ output `4 + 4 sinωt`, range
**0 V to 8 V**, average **+4 V**.
**Method:** The one formula that solves every clamper: **shift = −V_min (positive
clamp) or −V_max (negative clamp).** Note the DC component of the input is *not*
irrelevant — it moves `V_min`, so `2 V DC + 4 V sine` shifts by only 2 V, not 4 V.
Students who shift by `Vm = 4 V` get a 2–10 V answer that leaves the bottom at 2 V
and fails the defining property of a clamper (bottom must touch the reference).

---

### Q30. (GATE-level) A negative clamper has `R_L = 500 Ω`, `C = 0.1 µF`, and is fed
at 5 kHz. Compute the droop fraction, then state whether the circuit is a
satisfactory clamper and why.
**Answer:** `T = 200 µs`, `T/2 = 100 µs`, `τ = 500 × 0.1 µ = 50 µs`;
droop `= 1 − e^(−100/50) = 1 − e^(−2) = 1 − 0.1353 = ` **86.5 %**. Unsatisfactory —
the "clamped" peak falls to 13.5 % of its value before the next pulse, so the
output is a sawtooth, not a shifted sine. Fixes: raise `R_L`, raise `C`, or raise
the frequency is *not* an option (it makes it worse). Needed for 1 %: `τ ≳ 50T = 10 ms`.
**Method:** Compute `τ`, compare with `T/2`, apply `1 − e^(−(T/2)/τ)`. The order of
magnitude check is fastest: droop `≈ (T/2)/τ` for small values, so
`100 µs/50 µs = 2` ⇒ already > 100 % ⇒ the clamp has completely failed. **Always
sanity-check with the linear approximation first**; if it exceeds 1, the exponential
answer is somewhere between 63 % and 100 %.

---

### Q31. (GATE-level) Describe the first two cycles of a positive clamper whose
capacitor starts **completely uncharged**, and explain why GATE only ever asks for
the steady state.
**Answer:** Cycle 1: with `C` at 0 V the output simply follows the input, negative
excursion and all — the diode has not yet established an offset. At the first
negative peak the diode conducts and `C` charges to ≈ `Vm`. Cycle 2 onwards: the
output is `v_in + Vm` and repeats exactly. Because the answer depends on the
initial condition for the first cycle or two, every textbook/GATE clamper question
says *"in steady state"*.
**Method:** Start from `V_C = 0` and iterate the loop: the capacitor voltage is the
*state variable*, and it reaches its fixed point after a few time constants. The
practical lesson: a clamper's output is not valid on the first cycle — which is
exactly why DC restoration in a TV happens every frame and nobody notices.

---

### Q32. (GATE-level) A clamper feeds a **half-wave rectifier** stage (single ideal
diode into 1 kΩ). Input `v_in = 5 sin ωt` goes into a positive clamper first. What
is the final output range and its average?
**Answer:** After the clamper: `v_out = 5 + 5 sinθ`, range 0–10 V (never negative).
The half-wave rectifier then has nothing to block — the diode is forward biased
throughout. So the output is unchanged: range **0 V to +10 V**, average
`= 5 + 5/π = 5 + 1.5915 = ` **6.59 V**.
**Method:** The insight: **a positive clamper makes a positive half-wave rectifier
unnecessary** (and a negative clamper makes a negative one unnecessary), because
the signal never goes below the reference. This is the "clamp-then-rectify"
trick. Compute it as `A + B/π` with `A = 5` (the DC from the clamp) and
`B = 5` (the sine amplitude). If you had skipped the clamper, the plain half-wave
average would have been only `5/π = 1.59 V` — the clamp supplied the missing
4.41 V of DC.

---

### Q33. (GATE-level) A positive clamper (ideal, `V_ref = 0`) is followed by a
**negative** shunt clipper with reference `−2 V` (ideal). Input `10 sin θ`. Give the
final range and the clipper's conduction window.
**Answer:** After the clamper: `10 + 10 sinθ`, range 0–20 V — always ≥ 0, so a
`−2 V` bottom clipper can **never** turn on. Final range **0 V to +20 V**;
**no conduction at all**.
**Method:** Sanity-check the intermediate stage first: a bottom clip at −2 V can
only clip a signal that goes below −2 V, and a positively clamped sine never does.
A clamp that removes the very excursion a clipper needed is a real design
situation — and the fix is to use the *right* reference level, or to clip before
clamping. Always verify a clipper's threshold is actually reachable in the
clamped waveform.

---

### Q34. (GATE-level) A positive clamper (ideal) on `v_in = 5 sin ωt` has
`R_L C = 0.2·T`. (a) What does the textbook droop formula give for the charge lost
between conduction pulses? (b) What are the actual output peak and average, and is
the DC restoration still working?
**Answer:** (a) `1 − e^(−(T/2)/(0.2T)) = 1 − e^(−2.5) = 1 − 0.0821 = ` **91.8 %** lost.
(b) Integrating the drooping waveform cycle by cycle: the output still touches
**0 V** at the bottom (the diode always gets a short conduction window at the
negative peak) but the peak reaches only **4.36 V** instead of 10 V, and the
**average collapses to ≈ 1.60 V** instead of +5 V. The DC restoration has largely
**failed** — the output is a weak sawtooth on a small pedestal, not a shifted sine.
**Method:** (a) is the standard `1 − e^(−Δt/τ)` droop estimate with `Δt ≈ T/2`.
(b) is the important, less-quoted lesson: droop does **not** merely tilt the top of
the wave, it **destroys the DC level**, because the stored charge was what supplied
the offset in the first place. Always take the order-of-magnitude reading first:
`(T/2)/τ = 0.5/0.2 = 2.5 > 1`, so more than 100 % of the charge would be lost in a
half-cycle and the clamp has plainly failed — no precision needed.
**Design rule: keep droop under a few percent, i.e. `R_L C ≳ 20 T`; for 1 % droop,
`R_L C ≳ 50 T` (Q21).**

---

### Q35. (GATE-level) Give a one-line test to tell a clipper from a clamper, and
explain what happens to the p-p output amplitude in each.
**Answer:** Test: **is there a series capacitor?** Capacitor ⇒ clamper (shifts DC,
p-p preserved). No capacitor, diode in series or across the output ⇒ clipper (cuts
shape, p-p reduced).
**Method:** Clamper p-p in = clamper p-p out (`±Vm` → `2Vm` span).
Clipper p-p out < p-p in (e.g. `10 sinθ` series-clipped at 0 gives 0–10 V, p-p = 10 V
from an input p-p of 20 V). The p-p check is also a *self-test* on your solution: if
you drew a "clamper" whose p-p shrank, you have drawn a clipper.

---

### Q36. (GATE-level) A clamper's diode is reverse biased at `V_C`. For a sine input
of `Vm = 8 V` with a **+1.5 V** reference and a silicon diode, find `V_C`, the
reverse voltage, the output range, and the average.
**Answer:** Bottom target = `1.5 + 0.7 = 2.2 V`; the input's minimum is `−8 V`, so
the capacitor must make up `−8 → 2.2`, i.e. `V_C = ` **10.2 V**.
Reverse voltage on the diode = **10.2 V**. Output range **+2.2 V to +18.2 V**
(p-p 16 V ✔). Average `= 2.2 + 8 = ` **10.2 V** — which equals `V_C`, a useful
shortcut: **for a sine, the average of a positive clamper's output equals the
capacitor voltage.**
**Method:** Build it in one chain: (1) clamp level = `V_ref + 0.7`; (2) `V_C` = the
distance from `V_min = −Vm` up to the clamp level = `Vm + V_ref + 0.7`; (3) PIV =
`V_C`; (4) range = `[clamp, clamp + 2Vm]`; (5) average = clamp + `Vm` = `V_C`.
Every one of the five answers comes from step 2, so getting `V_C` right is worth
four marks. Cross-check: 2.2 + 16 = 18.2 ✔ and average 10.2 = `V_C` ✔.

---

## Trap box (exam-day killers)

- **A clamper never changes amplitude or shape.** If your p-p output is smaller
  than the p-p input, you have solved a clipper problem.
- **Silicon moves the clamp level by 0.7 V, and it moves it *away* from the
  reference**: positive silicon clamper bottoms at `+0.7 V`, negative at `−0.7 V`.
- **A clamp referenced to `0` on a signal that never goes negative does nothing.**
  Compute `−V_min` first; if it is zero, the answer is "no change".
- **Never count the bias twice.** A positive clamper with `V_ref = 2 V` on
  `Vm = 5 V` shifts by `2 + 5 = 7 V`, not 9 V.
- **Between pulses the capacitor DISCHARGES through `R_L`.** Droop is exponential
  `1 − e^(−(T/2)/τ)` with `τ = R_L C`; the diode is off for **half** the cycle,
  not the whole cycle.
- **Linear approximation trap:** droop `≈ (T/2)/τ` is only valid when `τ ≫ T`.
  If `(T/2)/τ > 1` the linear formula predicts more than 100 % loss, which means
  the clamper has failed completely — use the exponential.
- **PIV of a clamper's diode = `|V_C|`** — never `2V_C`, and *not* automatically the
  input peak-to-peak. `V_C` is the distance from the reference to the input extreme
  on the far side, i.e. how far the output actually shifts. So `±Vm` sine ⇒ `Vm`
  (not `2Vm`); `0 ↔ 10 V` with a **negative** clamper ⇒ `10 V`; but `−5 ↔ +5 V` with
  a positive clamper ⇒ only **5 V**, even though the p-p is 10 V (Q22).
- **The clamper shifts first.** In any clamper → clipper cascade, apply the
  threshold to the *clamped* waveform, so the `sin θ` condition can come out with a
  **negative** number (Q25). Writing the intermediate waveform first prevents this.

## Final recall drill (do in 60 seconds)

1. Positive clamper, ideal, `±Vm` → range **0 … 2Vm**, shift **+Vm**
2. Negative clamper, ideal, `±Vm` → range **−2Vm … 0**, shift **−Vm**
3. Positive clamper, silicon, `±Vm` → range **0.7 … (2Vm+0.7)**
4. Negative clamper, silicon, `±Vm` → range **−(2Vm+0.7) … −0.7**
5. Positive clamper, `V_ref = +2 V`, ideal, `±5 V` → range **+2 … +12**
6. Negative clamper, `V_ref = −4 V`, ideal, `±10 V` → range **−24 … −4**
7. General rule, positive clamp → shift = **−V_min**
8. General rule, negative clamp → shift = **−V_max**
9. Droop over the off half-cycle → **1 − e^(−(T/2)/(R_L C))**
10. Between pulses the capacitor is **discharging** through **`R_L`**
11. `R_L C = T`, droop → **39.3 %**
12. `R_L C` for under 1 % droop → **≳ 50·T**
13. Clamped sine average, positive, `Vm` → **+Vm**; RMS → **1.2247·Vm**
14. PIV of a clamper diode → **`|V_C|`** (= `Vm` for a sine; **not** the p-p unless
    the reference sits on an input extreme — `−5↔+5` gives 5 V, Q22)
15. Clamper vs clipper test → **is there a series capacitor?**
16. `0 ↔ 10 V` square into a **negative** clamper → **−10 … 0 V** (level shift, not inversion)

---

