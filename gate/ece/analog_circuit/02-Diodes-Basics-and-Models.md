# Chapter 02 — Diodes: Basics and Models

> **The idea in one line:** A diode is a one-way valve for current. For GATE, you
> mostly decide *is the diode ON or OFF?* and then replace it with a simple
> model (0.7 V drop, a battery, or a resistor) and solve resistors with KVL.

---

## 2.1 The PN junction diode

### Symbol and polarity
- Symbol: triangle pointing to a bar. The **bar** is the **cathode (n side)**,
  the **triangle** is the **anode (p side)**.
- Conventional current flows **from anode to cathode** (i.e., from P to N).
- The arrow in the symbol points in the direction of *conventional* current.

### Forward bias
- Anode more positive than cathode (p-side connected to +). Barrier lowered.
- Above the **cut-in / knee voltage**, significant current flows.
- Cut-in: silicon ≈ **0.7 V**, germanium ≈ **0.3 V**.

### Reverse bias
- Anode negative w.r.t. cathode. Barrier raised. Only a tiny **reverse
  saturation current** `I_S` flows (µA to nA).
- If reverse voltage exceeds **breakdown voltage**, current rises sharply
  (Zener/avalanche). In signal diodes this *destroys* the diode; in Zeners it is
  the operating region.

### I–V characteristic (the curve you must be able to sketch)

```
   forward │    ____
   current │   /
       I   │  /
           │ /__ cutoff-in (≈0.7V)  → V
           │/_
   --------+--------------
     -Vz |        |  (tiny -I_S reverse current)
```

- First quadrant: exponential rise starting at `V_γ` (cut-in).
- Third quadrant: flat tiny reverse current until `−V_z` (breakdown).

### Key electric quantities
- Reverse saturation current `I_S`: small, strongly temperature dependent
  (doubles ~every 10 °C).
- Cut-in voltage `V_γ`: Si 0.7 V, Ge 0.3 V (may be given ~0.6–0.75 in exams).
- Static (DC) resistance: `R_static = V/I` at the operating point.
- Dynamic (small-signal) resistance: `r_d = dV/dI` at the operating point.

---

## 2.2 Important equations

### Shockley (diode) equation
```
i_D = I_S · ( e^(v_D/(n·V_T)) − 1 )
```
- `I_S` = reverse saturation current (A, typically 10^-14 to 10^-9 A)
- `n` = ideality factor (≈ 1 for perfect; silicon ≈ 1–2)
- `V_T = k·T/q ≈ 25.85 mV @ 300 K` (use **25 mV** as the standard GATE value)

For forward bias strongly ON, `e^(...) >> 1`, so `i_D ≈ I_S·e^(v_D/(nV_T))`.

### Small-signal (dynamic) resistance
```
r_d = n·V_T / I_D          (at the DC current I_D)
```
Standard room-temperature value **`r_d ≈ 25 mV / I_D`** with `n = 1`.
- At `I_D = 1 mA`: `r_d = 25 Ω`. At 5 mA: 5 Ω. At 0.1 mA: 250 Ω.
- It *decreases* as current increases. **GATE loves this inverse relation.**

Derivation (intuition): slope of the *linearized* I–V around the operating point.
Voltage change per current change `= dV/dI` and the Shockley relation gives
`dV = (nV_T/I)·dI`.

### Operating point / Q-point
The DC point `(I_D, V_D)` where the signal `v_d = V_m·sin(ωt)` rides.
Set by the DC circuit around the diode (the "load line"). GATE asks:
- Given circuit and diode model → find `I_D` and `V_D`.
- For AC signal → `v_d(t) = i_d(t)·r_d` using the *dynamic* resistance.

### DC load line
For a diode in series with resistor `R` and source `V`:
`I = (V − V_D)/R`.
- Plot on the I–V curve: a straight line from `(V, 0)` to `(0, V/R)`.
- Q-point = intersection of load line with diode curve.
- With ideal diode: `V_D = 0` → `I_Q = V/R`.
- With CVD model: `V_D = 0.7` → `I_Q = (V − 0.7)/R`.

### AC load line
If an AC source replaces part of the circuit in the signal model, the *slope* of
the AC load path differs. For small signals, always use the **dynamic
resistance** on the AC path, not the DC resistance.

---

## 2.3 The four diode models (GATE essentials)

| Model | Description | When to use |
|-------|-------------|-------------|
| **Ideal** | ON = short, OFF = open, no voltage drop | Qualitative clipping/clamping, fast checks |
| **Constant-voltage-drop (CVD)** | ON = 0.7 V source, OFF = open | Most numericals; silicon default |
| **Piecewise-linear** | ON = Vγ + r_d (a battery + series R) | When diagram gives `Vγ` and `r_d` or "knee resistance" |
| **Small-signal** | ON point replaced by `r_d = nV_T/I_D` (plus Vγ) | AC signal problems on top of a DC bias |

For OFF (reverse biased): all models say **open circuit**, current ≈ 0.

### Piecewise-linear model detail
Forward region: `v_D = Vγ + i_D·r_d`. So a diode with `Vγ = 0.7`, `r_d = 10 Ω`
carrying 5 mA drops `0.7 + 5m·10 = 0.75 V`.

### Choosing the model in the exam
- No model given, silicon → **CVD 0.7 V**. Germanium → 0.3 V.
- Problem says *"diode has cut-in voltage Vγ and forward resistance r_f"* →
  **piecewise-linear**.
- Problem asks for an **AC small-signal** change → use `r_d = nV_T/I_D`, and keep
  `Vγ` in the DC part.

---

## 2.4 Systematic method: is the diode ON or OFF?

For a diode in a resistor network the GATE method is:

1. **Temporarily remove the diode** (replace with open).
2. Find the voltage that *would* appear across its terminals (`V_anode − V_cathode`).
3. If anode > cathode: diode **ON** → replace with chosen model (0.7 V battery in
   CVD), re-solve.
4. If anode < cathode: **OFF** → leave open, done.

This "test for conduction first" method makes every clipper/rectifier solvable.

---

## Worked example (classic GATE)

**Problem:** Silicon diode (`Vγ = 0.7 V`), series `R = 2 kΩ`, supply `V = 5 V`.
Find DC current.

**Solution:**
1. Remove diode, V across terminals = +5 V (anode positive) → ON.
2. Replace with 0.7 V source. KVL: `5 = 0.7 + 2k·I`.
3. `I = (5 − 0.7)/2k = 4.3/2000 = 2.15 mA`.

**Follow-up (AC small-signal):** a ±0.1 V, 1 kHz sinusoid adds to the 5 V.
Find the AC current amplitude.
- `r_d = 25 mV/2.15 mA ≈ 11.6 Ω`.
- `i_ac = v_ac/(R + r_d) = 0.1/(2000 + 11.6) ≈ 50 µA`. (Notice R dominates.)

---

## GATE traps (diodes)

1. **Direction!** Conventional current flows P→N = anode→cathode. A flipped
   diode converts a positive clipper into a negative clipper instantly.
2. `r_d = 25 mV/I_D` — **at the DC current**. Do not use the AC current.
3. Reverse saturation current `I_S` is in the *nano/µA* range; never confuse it
   with forward currents (mA).
4. When two diodes are in series: drops **add**. Parallel with equal drops:
   currents split, but a mismatch in `Vγ` makes the *lower-Vγ* diode hog current.
5. "Germanium" problems mean `Vγ ≈ 0.3 V`, not 0.7.
6. For the ideal diode model, a forward-biased diode is a **wire**, not a 0.7 V
   battery — students blend models.
7. Reverse breakdown: read the question carefully — if it says **Zener**, it is
   *designed* to operate at breakdown; if it says ordinary silicon diode and
   asks about the I-V, breakdown means damage.

---

## 5-question self-check

1. `I_S = 10^-14 A`, `V_D = 0.7 V`, `n = 1`, `V_T = 25 mV`. Approx forward current?
   → *e^(0.7/0.025) = e^28, so I ≈ 10^-14·e^28 ≈ 1.4 mA.*
2. Diode at 2 mA. Dynamic resistance? → *25 mV/2 mA = 12.5 Ω.*
3. Diode drops 0.7 V, carries 0 (reverse). Call current? → *≈ I_S (µA–nA),* model OFF.
4. Three silicon diodes in series, bias 3 kΩ, source 9 V. Which current?
   → *Drop 2.1 V, I = (9 − 2.1)/3k = 2.3 mA.*
5. An ideal diode is ON. Its model is? → *A short.*

Next chapter: **`03-Clipping-Circuits.md`**