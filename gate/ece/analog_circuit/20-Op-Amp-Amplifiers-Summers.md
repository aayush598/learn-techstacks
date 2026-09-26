# Chapter 20 — Op-Amp Amplifiers and Summers

> **The idea in one line:** every op-amp amplifier is just *"inverting, put the
> input resistor charge into the feedback resistor"* or *"non-inverting, let the
> divider set the gain."* Summers are multiple input resistors into one
> virtual-ground summing junction.

---

## 20.1 Inverting amplifier — the master template

```
            R_f
  v_in ──R1──┼──►────┐
            v−       │
                     + (op-amp) ──► v_o
            v+ = 0 ──┴
```
Because `v− = 0` (virtual ground) and no current enters the op-amp:
```
i1 = v_in/R1   (through R1)
i_f = −v_o/R_f (through R_f)
i1 = −i_f        (KCL at v−)
→ v_o = −(R_f/R1)·v_in
```
- **Gain:** `−R_f/R1`. Inverting, purely resistor-defined.
- **Input resistance:** `R1` (seen from source; the junction is at 0 V).
- **Output resistance:** ~0 (voltage source).

With a load `R_L`, output unchanged (ideal); real op-amp sags a little.

### GATE specifics
- R_f = 0 → follower... no, that's non-inverting unity; here R_f shorted makes
  `v_o = 0` (buffer, gain −0).
- Adding a capacitor across R_f → low-pass (Chapter 22 filter territory).

---

## 20.2 Non-inverting amplifier

```
  v_in ────────► v+ (op-amp) ──► v_o
                v− ── R1 ── GND
                └── R_f ──────┘
```
Virtual short: `v− = v+ = v_in`. Divider at v−:
```
v− = v_o·R1/(R1+R_f) = v_in
→ v_o = v_in·(1 + R_f/R1)
```
- **Gain:** `1 + R_f/R1` (≥ 1, no inversion).
- **Input resistance:** huge (≈ op-amp input R, ~∞). Source barely loaded.
- **Output resistance:** ~0.

### Why "1+" and never 0
Because the feedback divides to `v_in`, the amplifier must *out-produce* the
division — hence `1 +`. Losing the 1 is the classic error.

---

## 20.3 Voltage follower (unity buffer)

```
  v_in ───► v+ (op-amp) ──► v_o
           v− ────────────┘ (direct feedback)
```
- `v+ = v−` → `v_o = v_in` → **gain = +1**.
- Infinite R_in, zero R_out — ideal buffer. Isolates a source from a load.

---

## 20.4 Inverting summing amplifier

```
   v1 ── R1 ──┐
   v2 ── R2 ──┼──► v− (virtual ground) ── R_f ──► v_o
   v3 ── R3 ──┘      │
                     +  
                    v+ = GND
```
Each input pushes current into the virtual-ground summing node:
```
i1 + i2 + i3 = −i_f
v1/R1 + v2/R2 + v3/R3 = −v_o/R_f
→ v_o = −( R_f·(v1/R1 + v2/R2 + v3/R3) )
```
**Weighted summer.** If all R equal: `v_o = −(v1+v2+v3)·(R_f/R1)`.

GATE facts:
- Superposition works here (linear!): hit each input one at a time, sum.
- Input of the *summing* cases: the resistors only "see" their own voltage; the
  virtual ground isolates inputs — no crosstalk. That isolation is the point.

---

## 20.5 Non-inverting summer (bonus, GATE rare)

Multiple resistors into the non-inverting input:
```
v_o = (1 + R_f/R1)·(weighted average of inputs)
```
The + input is a *node* (not virtual ground), so the output is `1+R_f/R1`
times the average-like combination based on the input divider. More often GATE
sticks to the inv-summer — master that.

---

## 20.6 Scaling / instrumentation flavour

- "Scaling" = inverting gain with R values tuned: `v_o = −a1·v1 − a2·v2...`
- Difference amplifier (op-amp subtraction): inputs to both terminals:
  ```
  v_o = (R2/R1)·(v2 − v1)    [if R2/R1 matched both sides]
  ```
  This uses 4 resistors; the balanced difference amp is the heart of
  instrumentation amps. GATE asks for the common-mode rejection: R_mismatch →
  finite CMR.

---

## Worked example — weighted summer

`R1 = 1 kΩ`, `R2 = 2 kΩ`, `R3 = 4 kΩ`, `R_f = 4 kΩ`, `v1 = 1 V, v2 = 2 V,
v3 = 1 V`.
- `v_o = −4k·(1/1k + 2/2k + 1/4k) = −4k·(1 + 1 + 0.25) = −4k·2.25 = −9 V`.

## Worked example — non-inverting with source resistance

Source with `R_s = 10 kΩ` into non-inv amp (R_f=90k, R1=10k) with R_s in
series with the input:
- The non-inverting input draws no current → R_s drops nothing → gain unaffected.
- (Contrast: the *inverting* input would load through R1... but with R1 between
  source and virtual ground the input R = R1.) 

---

## GATE traps (amplifiers + summers)

1. Inverting: R_in = R1. Non-inverting: R_in = ∞. R_s affects inverting gain
   via Rs+R1 but not the non-inverting (no current).
2. `1 + R_f/R1` — forget the 1 and you're off by a constant.
3. Summer polarity: inverting summers OUTPUT a NEGATIVE sum (with sign).
4. Virtual ground is at the summing node — that's why inputs don't affect each
   other.
5. Saturation again: a large weighted sum can rail the op-amp.
6. Difference amp requires matched resistors for CMR; a mismatch destroys CMRR.

---

## 5-question self-check

1. Inv amp R1=1k, R_f=5k, v_in=0.2: v_o? → *−1 V.*
2. Non-inv R_f=9k, R1=1k: gain? → *10.*
3. Follower gain/R_in? → *+1 / ∞.*
4. Summer R_all equal, three inputs equal 1 V, R_f=3k,R_i=1k → v_o? → *−9 V.*
5. Difference amp (R2/R1)=2, v2−v1=3 → v_o? → *6 V.*

Next: **`21-Op-Amp-Integrators-Differentiators.md`**