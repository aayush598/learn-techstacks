# Chapter 21 — Op-Amp Integrators and Differentiators

> **The idea in one line:** put a capacitor in the feedback (integrator) or in
> the input (differentiator), and the op-amp now performs calculus. Know the
> transfer functions, the waveforms, the saturation limits, and both circuit's
> practical fixes (the resistor that makes them stable).

---

## 21.1 Ideal inverting integrator

```
  v_in ── R ──┼─── C ──►────┐
             v−            │
                           + (op-amp) ──► v_o
              v+ = 0 ──────┴
```
Virtual ground at v−. Current `i = v_in/R` charges the capacitor:
```
i = C·dv_o/dt
v_in/R = −C·dv_o/dt
→ v_o(t) = −(1/RC)·∫ v_in dt + v_o(0)
```

### Frequency / phasor
```
H(jω) = v_o/v_in = −1/(jωRC)
|H| = 1/(ωRC)     (falls 20 dB/dec — low-pass with −90°)
```
- DC gain "infinite" (integrator), gain −∞ at DC.
- Corner: when `1/(ωRC) = 1` → ω = 1/(RC).

### GATE waveforms (memorize the classic set)
- **Square wave input:** output = linear ramp/sawtooth (integral of square).
  Slope = `−V_pk/(RC)`.
- **Sine input:** output = cosine scaled `−1/(ωRC)·V_pk` (90° lag).
- **DC input:** output ramps linearly forever (until rail).

### First-order differential property
A square in → triangle out; a triangle in → parabola. "Differentiation flips
these."

---

## 21.2 Practical integrator (the fix)

Problem: at DC the ideal integrator runs away (feedback open). Fix: parallel a
**resistor `R_f`** across the feedback capacitor.

```
          R_f          C
  v_in ──R1──┼────R_f────┐
            v−            │  C  ──►────┐
                         + (op-amp) ─►───── v_o
```
- Gain at DC: `−R_f/R1` (limited, stable).
- Corner frequency: `f = 1/(2π·R_f·C)` — below it behaves as gain −Rf/R1;
  above it, integrating (gain rolls off).
- The practical integrator is a **low-pass** with finite DC gain.

---

## 21.3 Ideal differentiator

```
  v_in ── C ──┼── R ──►────┐
             v−            │
                          + (op-amp) ──► v_o
              v+ = 0 ──────┴
```
C in input, R in feedback:
```
i = C·dv_in/dt
v_o = −i·R = −R·C·dv_in/dt
→ v_o(t) = −RC·(dv_in/dt)
```
### Short-cut waveforms
- **Square in:** output = spikes (impulses at edges).
- **Triangle in:** output = square wave.
- **Sine in:** output = cosine × −ω·RC (90° lead, high-frequency boost).

### Frequency / phasor
```
H = −jωRC      (rises 20 dB/dec — high-pass, +90°)
```
- Gain grows with frequency → **noise amplifier**, unstable → practical fix
  needed.

---

## 21.4 Practical differentiator

Fix: series a small **resistor `Rs`** with the input capacitor (and often a
small C_f across the feedback R).
- High-frequency gain limited to `−R/Rs` instead of blowing up.
- Corner `f = 1/(2π·Rs·C)` — after that, gain flattens.
- Noise does not explode.

---

## 21.5 Integrator in ramp/square/triangle waveform generators

- **Ramp generation:** constant current into a capacitor
  (`V_ramp = −t·I/C`, straight line).
- **Square → triangle:** feed the square into an integrator (this is how the
  triangular-wave oscillator works, Chapter 25).
- Integrator + Schmitt trigger = the astable waveform generator (square from
  trig, triangle from integrator). Classic 2-op-amp question.

---

## 21.6 Saturation / initial conditions / frequency limits

- **Saturation:** any DC component integrates to a rail over time. Practical
  integrator prevents this with R_f.
- **Initial conditions:** the formula needs `v_o(0)`. GATE gives "capacitor
  initially uncharged" → start at 0 V.
- **In practice (real op-amp):**
  - Finite slew rate distorts the sharp spikes of a differentiator.
  - Input offset/GBW limit how "perfect" the 90°/~180° phases are.

---

## Worked example — square to ramp

Integrator: R = 100 kΩ, C = 1 µF → RC = 0.1 s. Input square ±1 V at 2 kHz.
- Between edges, `dv/dt·(-1/(RC))`: `−1/0.1 = −10 V/s` per 1 V step; for input
  +1 → slope `−10 V/s`; for −1 → `+10 V/s`.
- Triangle amplitude after half-a-period increases by slope·(T/2);
  `T = 0.5 ms`; `slope·T/2 = 10·0.25m = 2.5 mV` per half-cycle — tiny. Ramp
  grows as square-wave-run.

## Worked example — differentiator spike

C = 0.1 µF, R = 10 kΩ → RC = 1 ms. Square 0→5 V (fast edges):
- Spike height `≈ RC·(dV/dt)`. Edge 5 V/10 µs → `1m·(5/10µ) = 500 V`
  (ideal; real op-amp limits by slew). The *sign*: rising edge → negative spike.

---

## GATE traps (integrators / differentiators)

1. Integrator inverts AND integrates: `−(1/RC)∫`. Differentiator: `−RC·d/dt`.
   Missing minus = wrong polarity on waveforms.
2. Practical integrator runs `R_f ∥ C` — not bare C.
3. Differentiator loves noise (rising HF gain). Practical fix = series R_s.
4. Waveform mapping: square→triangle (integrate); triangle→square (diff);
   square→spikes (diff); triangle→parabola (integrate).
5. Initial condition matters — a "0 V start" vs "charged cap" changes the ramp
   origin.
6. Pedestal/DC: an integrating circuit eventually rails unless R_f bounds it.

---

## 5-question self-check

1. Integrate a square → ? → *triangle.*
2. Differentiate a triangle → ? → *square.*
3. Practical integrator add? → *R_f across C.*
4. Differentiator HF gain? → *rises at 20 dB/dec (why noise).*
5. Ramp slope for square ±1 V, RC=0.1 s? → *±10 V/s.*

Next: **`22-Active-Filters.md`**