# Chapter 03 — Clipping Circuits

> **The idea in one line:** A clipper *cuts off* part of a waveform. The diode
> conducts during intervals the input tries to drive the output past a limit;
> during conduction the output is "clamped" to that limit level. Clipping only
> changes the *shape* — it never changes the DC level of the reference.

---

## 3.1 What clipping does

Given `v_in`, the circuit produces `v_out` that follows the input except where a
diode conducts; at those intervals output is pinned at a threshold.
Result: peaks above (or below) a level are *cut off* — hence the name.

Key concept: **series vs shunt** refers to where the diode sits relative to
input and load.

---

## 3.2 Series clippers (diode in series with the load)

The diode is between input and the output node (with the load resistor to
ground).

### Positive series clipper (no bias)
```
 v_in —►▷— v_out
           │
          R_L
           │
          gnd
```
- During **positive** half-cycle: diode forwards, output = input (minus 0 V
  ideal; minus 0.7 V for silicon).
- During **negative** half-cycle: diode reverse, output = 0.
- Result: only positive half-waves appear. (For ideal diode: output = positive
  half; for silicon: `v_out = v_in − 0.7` in the positive cycle.)

### Negative series clipper
Diode flipped (`◁`). Negative half passes, positive half cut → output only the
negative half-wave.

### Biased series clipper
A DC battery (or resistor divider providing `V_ref`) sits in the diode branch.

**Positive biased clipper** (battery `V` with + toward the load, diode points
into output):
- Diode conducts when `v_in > V` (input must beat both the diode drop and the
  battery). Output = `V` during conduction.
- Output = input when `v_in < V`.
- Net effect: waveform is clamped flat at `V` on the high side.

**Negative biased clipper:** symmetric on the low side: output flat at `−V`.

### Series clipper: conduction rule
Series diode + load resistor to ground behaves as: output follows input until
the conducting condition, then holds at the clamp level.

---

## 3.3 Parallel / shunt clippers (diode across the output)

The diode sits **across** the output (in parallel with the load). Now the diode
*shorts the output* during conduction, forcing `v_out` to the diode's clamping
value.

### Positive shunt clipper (no bias)
Diode from output node to ground, anode at output:
- Positive half-cycle → diode ON → `v_out = 0` (ideal; or +0.7 V Si).
- Negative half-cycle → diode OFF → `v_out = v_in`.
- Result: positive peaks clipped to (approximately) ground. Output = negative
  half-wave plus flat infinite at top.

### Negative shunt clipper
Diode flipped. Negative peaks shut to ~0; output = positive half-wave with the
bottom clipped.

### Biased shunt clippers
Battery in series with the shunt diode. When the input exceeds the reference
plus the diode drop, the diode conducts and pins the output at the reference.
- Positive biased shunt clipper pins the *top* at `+V`.
- Negative biased shunt clipper pins the *bottom* at `−V`.

---

## 3.4 Two-level clippers (both halves)

Combining a positive clipper and a negative clipper clips **both** sides:
- Top clamped at `+V1`, bottom clamped at `−V2`.
- Common form: two diodes + two batteries, or two Zener diodes back-to-back.

Classic GATE circuit: **two Zeners in series, back-to-back**, across the output.
- Positive half: one Zener breaks down at `Vz`, the other is forward ≈ 0.7 V →
  clamp level `Vz + 0.7`.
- Negative half symmetric: clamp at `−(Vz + 0.7)`.

(Zener details: forward drop ~0.7 V, reverse breakdown = `Vz`. So a pair gives
a two-level clipper with both thresholds.)

---

## 3.5 The master method for ANY clipper

1. **Choose the model** (ideal / CVD given Vγ).
2. For each half of the waveform, **decide diode states** using the
   "remove diode, check terminal voltage" test (Chapter 02).
3. Replace ON diodes with their model, OFF with open.
4. Solve `v_out` as a function of `v_in` for each interval (voltage division /
   KVL — usually trivial).
5. **Sketch** the output waveform: flat regions when clamped, ramp/follow
   regions otherwise.
6. If asked, read off: peak values, DC (average) value, time when a diode turns
   on/off.

### Average (DC) value of a clipped waveform — GATE style
For symmetric clipped sine: the average is usually found by `(1/T)∫v_out dt`,
but for GATE use symmetry + area reasoning:
- Half-wave (series positive clipper): average `= Vm/π` for ideal.
- If the top 50% of a sine is cut to a flat `Vm`: average is a trapezoid/blend —
  integrate, don't guess.

*Shortcut:* The average of a flat region is that level; the average of a rectified
half-sine is `Vm/π`. Weighted sum of the areas / T.

### When does the diode turn ON?
Solve `v_in(t) = threshold`. E.g., a sine `Vm sin(ωt)` clipped at `+0.5 V` turns
the diode on between `ωt = sin⁻¹(0.5/Vm)` and `π − sin⁻¹(0.5/Vm)`. GATE asks
exactly this *conduction interval*.

---

## Worked example 1 — positive series clipper, biased

Given `v_in = 10 sin(ωt)`, ideal diode, battery `V = 5 V` with + toward output.
Input voltage divider: diode in series with the source. Output `v_out` = ?

**Solution:**
1. Ideal diode. Diode conducts when `v_in > 5 V`.
2. Conducting interval: `10 sin(ωt) > 5` → `sin(ωt) > 0.5` →
   `ωt ∈ [30°, 150°]`.
3. During conduction `v_out = 5 V` (battery holds it).
4. Else `v_out = v_in`.
5. Sketch: original otherwise; flat at +5 V on top between 30° and 150°.

---

## Worked example 2 — two-level (dual bias) clipper

Two diodes: top clipper at `+4 V` (ideal), bottom at `−2 V`. Input = `8 sin(ωt)`.

- When `v_in > +4`: top diode ON → `v_out = +4`.
- When `v_in < −2`: bottom diode ON → `v_out = −2`.
- Between: `v_out = v_in`.
Result: a sine with +4 top and −2 bottom flat clamps.

---

## Worked example 3 — Zener pair as two-level clipper

Back-to-back Zeners, `Vz1 = 5 V`, `Vz2 = 3 V`, silicon forward `0.7 V`.
Input ±12 V.

- Positive: upper Zener breaks at 5 V, lower forward at 0.7 → clamp `+5.7 V`.
- Negative: lower breaks at 3 V (reverse), upper forward 0.7 → clamp `−3.7 V`.

---

## GATE traps (clippers)

1. **Series vs shunt:** in series the diode *passes* the half that conducts; in
   shunt it *shorts* it. Mixing these inverts the answer.
2. Do not forget the **0.7 V** diode drop if it is a silicon diode — ideal vs
   CVD gives different clamp levels (`0 vs 0.7`).
3. Conduction angle: many students find the on-set time but forget the
   off-set is `π − sin⁻¹(...)`, not `π + sin⁻¹(...)` measured over one cycle.
4. For the DC value of a clipped sine, don't average the unclipped sine.
5. A diode conducting does *not* mean the output is the battery value in a
   **series** clipper — the input still drives through (check the loop).
6. Two-level clipper polarity: batteries facing "out" clip top; facing "in"
   clip bottom. Get the sign of the flat level right.

---

## 5-question self-check

1. Positive series clipper, ideal, `v_in = 20 sin ωt`, load 1 kΩ. Output peak +?
   → *Conducts above 0 → v_out clips the negative half → positive half passes at
   20 V, negative flat at 0.*
2. Same with silicon 0.7: positive peak output? → *19.3 V.*
3. Biased shunt clipper battery +3 V. Input 5 V. Output? → *+3 V (diode ON).*
4. Shunt positive clipper ideal, input −8 V. Output? → *−8 V (diode OFF).*
5. Two-level clipper, top +2, bottom −1, ideal, input +4 V. Output? → *+2 V.*

Next chapter: **`04-Clamping-Circuits.md`**