# Chapter 23 — Comparators and Schmitt Triggers

> **The idea in one line:** a comparator answers "which input is bigger?" with
> a railed output. A Schmitt trigger is a comparator with **positive feedback**
> and two separate thresholds — it refuses to chatter around a single crossing
> point. Hysteresis = switching immunity.

---

## 23.1 The comparator (open-loop op-amp)

No feedback: the op-amp acts as a comparator:
```
v_o = +V_sat   if v+ > v−      (positive rail)
v_o = −V_sat   if v+ < v−      (negative rail)
```
- **Zero-crossing detector:** v− = 0; v_o railed high when input > 0, low when
  < 0.
- **Inverting comparator:** signal at v− → output flips opposite.
- **Non-inverting comparator:** signal at v+ → output follows input polarity.
- Reference `V_ref` on one input; crossing that level flips the output.

### GATE facts
- Output is **at the rails**, never "in between."
- No virtual short (open loop).
- Temperature of reference drift etc. — only if stated.

---

## 23.2 The Schmitt trigger (regenerative comparator with feedback)

Positive feedback: a resistor from **output to the + input** (for
non-inverting).

```
               R2
  v_in ── R1 ──┼──────► v+ (op-amp)
               │
               └── R_f ──► v_o
  v− = V_ref (or 0)
```
Hysteresis comes from the fact that when output rails HIGH, the + input is
*pulled up*; when the output rails LOW, + is pulled down. So the switching
threshold differs depending on the current output state.

---

## 23.3 Thresholds — the two trip points

For a non-inverting Schmitt with v− = 0 (or V_ref), the + input is fed by:
`v+ = v_in·(R_f)/(R1+R_f) + v_o·(R1)/(R1+R_f)`

Switching occurs when `v+` crosses `v−`:

**Upper threshold (UT):** trips when v_o was LOW (−V_sat) and v_in rises until
v+ = 0:
```
UT = |V_sat|·R1/R_f
```
**Lower threshold (LT):** trips when v_o was HIGH (+V_sat) and v_in falls until
v+ = 0:
```
LT = −|V_sat|·R1/R_f
```
**Hysteresis width:**
```
ΔV = UT − LT = 2·|V_sat|·R1/R_f
```
For a symmetric rail (±V_sat), UT = +Vth and LT = −Vth, with
`Vth = V_sat·R1/R_f`.

**With a reference V_ref:**
```
UT = V_ref + V_sat·R1/R_f
LT = V_ref − V_sat·R1/R_f
```

### Transfer characteristic (the hysteresis loop)
```
 v_o
 +V_sat │ ─────────┐
        │          │    ← upper trip when v_in ↑ passes UT
        │          │
        └──────────┴──────► v_in
     −V_sat        └─── supply with downward → trips at LT
```
- Dual-threshold: output stays high until input beats UT, stays low until
  input drops below LT.
- **Symmetrical:** UT = −LT (equal magnitude around V_ref).
- **Asymmetrical:** different magnitude (use unequal feedback or a V_ref).

---

## 23.4 Why hysteresis matters

- **Noise immunity:** a noisy signal crossing near VT would otherwise make the
  output rattle. Hysteresis creates a dead zone the noise can't switch.
- **Square from sine:** feed sine → output is a clean square with edges at UT/LT.
- GATE favourite: "Why does a Schmitt trigger make a noisy zero-crossing
  detector clean?" → hysteresis band.

---

## 23.5 Inverting Schmitt trigger (alternative form)

Signal at v−, reference/feedback structure around v+:
```
v+ ─── R1 ─── v_ref
       └── R2 ─── v_o    (feedback, sign flips)
```
The + input is set by a divider between V_ref and v_o. Then:
- When output HIGH, threshold at + input pulled up; when LOW, pulled down —
  inverted relationship of thresholds. Output flips opposite to the non-inv case.

Both forms produce the loop; the direction of traversal (CW vs CCW) differs.
GATE typically just asks for the two thresholds — use KCL at the + terminal:
```
(v_ref − v+)/R1 + (v_o − v+)/R2 = 0  →  solve for v+; trip when v+ crosses v−.
```

---

## 23.6 Worked example

Non-inv Schmitt: `R1 = 1 kΩ`, `R_f = 10 kΩ`, `±V_sat = ±10 V`, `V_ref = 0`.
- `Vth = 10·(1k/10k) = 1 V`.
- UT = +1 V, LT = −1 V, hysteresis = 2 V.
- Input a 0.5 V sine: output stays HIGH because input never beats UT = ← but
  it's high while input < LT... simulate: start output LOW, signal rises through
  +1 → flips HIGH; falls through −1 → flips LOW. With ±0.5 signal: never trips
  → constant (no chatter). That's the point.

---

## 23.7 Worked example — with offset

Same but `V_ref = 2 V`:
- UT = 2 + 1 = 3 V. LT = 2 − 1 = 1 V. Output high when input > 3, low when
  < 1. Asymmetric band centered at 2 V.

---

## GATE traps (comparators / Schmitts)

1. Comparator = **open loop**, no virtual short. Schmitt = positive feedback.
2. Thresholds use **|V_sat|**, not the supply numeric if rails ±10 means V_sat
   = 10.
3. Hysteresis `= 2·V_sat·R1/R_f` — double the single-sided trip.
4. The two thresholds are NOT both at V_ref unless V_sat·R1/Rf = 0.
5. Inverting-vs-noninversion flips the traversal direction on the transfer
   loop. Sketch carefully.
6. "Regenerative" positive feedback can ring; hysteresis is what prevents
   multiple transitions on a single slow-slewing edge... actually the R-C
   (Schmitt+integrator) circuits, not here. Keep to thresholds.

---

## 5-question self-check

1. Schmitt output with noisy input? → *stable state per side, no chatter.*
2. UT with V_ref=0, V_sat=9, R1=2k, R_f=9k? → *2·9·(2k/9k)=? UT=2 V, LT=−2 V.*
3. Hysteresis width formula? → *2V_sat·R1/R_f.*
4. To widen hysteresis: increase R1 or R_f? → *increase R1 (raise ratio).*
5. Comparator output when in between thresholds? → *never — it's always at a rail.*

Next: **`24-Feedback.md`**