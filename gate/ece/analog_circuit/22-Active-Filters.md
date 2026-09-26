# Chapter 22 — Active Filters

> **The idea in one line:** passive R-C filters get a *boost* (and steep cutoffs)
> from an op-amp. Learn: what each filter does, how to compute corner
> frequencies, what **Q** and **order** mean, and the two famous 2nd-order
> topologies — **Sallen-Key** and **Butterworth**.

---

## 22.1 Filter vocabulary (usable in every problem)

- **Passband / stopband:** where the signal passes / is cut.
- **Cutoff `f_c`:** where gain falls to `1/√2` of max (−3 dB).
- **Roll-off:** rate of attenuation past cutoff — `20·order dB/decade`:
  1st = 20, 2nd = 40, 3rd = 60 dB/dec.
- **Q (quality):** sharpness at resonance/peaking.
  - Q = 0.707 (1/√2) = **maximally flat** (Butterworth).
  - Q > 0.707 → peaking near cutoff (Chebyshev-like).
  - Q < 0.707 → more gradual knee.
- **Order = number of poles** = number of effective reactive elements in the
  transfer; higher order → steeper skirts.
- **Bandwidth** (band-pass) `BW = f_H − f_L`; center `f_o = √(f_L·f_H)`;
  `Q = f_o/BW`.

---

## 22.2 The four basic filters

| Type | Passes | Transfer shape | Example |
|------|--------|----------------|---------|
| **Low-pass (LPF)** | below f_c | `H = 1/(1 + jf/f_c)` (1st) | smoothing, anti-alias |
| **High-pass (HPF)** | above f_c | `H = (jf/f_c)/(1 + jf/f_c)` | DC removal, AC coupling |
| **Band-pass (BPF)** | between f_L, f_H | two retro sides | radio selectivity |
| **Band-stop / notch** | rejects f_o | notch at center | hum (50 Hz) removal |

### First-order op-amp filters (built from Chapter 21 circuits)

**First-order LPF (integrator with R_f / inverting form):**
```
         R2 ──► v_o
  v_in──R1──┼── C ∥ R2
          v−
```
Gain low-freq `= −R2/R1`; corner `f_c = 1/(2π·R2·C)`; rolls at 20 dB/dec.

**First-order HPF (coupling form, non-inverting):**
```
  v_in ── C ──R1──► v+ (op-amp, non-inv gain 1+Rf/R1) 
              R1 → GND
```
`f_c = 1/(2π·R1·C)`.

**Rules of thumb for the exam:**
- LPF: capacitor **in parallel** with the feedback element(s).
- HPF: capacitor **in series** with the input path.
- BPF: cascade (or series) LPF+HPF; notch: sum of the two / twin-T.

---

## 22.3 Second-order LPF — the standard formulas

For a 2nd-order low-pass with corner `ω_o` and Q:
```
H(s) = ω_o² / (s² + (ω_o/Q)·s + ω_o²)
```
- Cutoff `f_o = ω_o/2π`.
- Q determines peaking and knee sharpness.
- Roll-off = 40 dB/dec.

---

## 22.4 Sallen-Key topology (unity-gain & gain variants)

**Unity-gain Sallen-Key LPF:**
```
 v_in ── R1 ──A── R2 ──► v_o (charges Q)
             │ C1    │ C2
            (C1 to gnd) (C2 from A to... )
Structure:
 v_in ─ R1 ─┬─ R2 ─┬──► v_o
            │      │
            C1     C2
            │      │
           GND    v+ (op-amp follower)
The follower output = v_o feeds back the right node.
```
Analysis (follow the follower: `v+ = v_o`):
```
ω_o² = 1/(R1·R2·C1·C2)
Q    = √(R1·R2·C1·C2) / (R1·C1 + R2·C1 + R1·C2·(1−gain_follower_0))
```
For the standard equal-component (`R1=R2=R, C1=C2=C`) version:
```
ω_o = 1/(RC)
Q   = 1/3    (for unity-gain follower Sallen-Key)
```
- **Q = 1/3 is the signature of equal-R, equal-C unity Sallen-Key.** GATE
  asks: adjust Q by changing one cap.

**Gain Sallen-Key (with gain k via 1+Rb/Ra on non-inv):**
```
Q = 1/(3 − k)      (single-pole formula when R,C all equal)
```
- As gain k → 3, Q → ∞ (poles go imaginary → oscillation). So Sallen-Key
  max *usable* gain = 3 (unity ok). GATE loves: "gain = 3 → oscillator!"

General Sallen-Key Q formula:
```
Q = √(C1·C2·R1·R2) / (R1·C1 + R2·C1 + R1·C2(1 − k))
```

---

## 22.5 Butterworth response

- **Maximally flat** magnitude in the passband: no ripple, flattest near DC.
- 2nd-order Butterworth has (by definition) **Q = 1/√2 ≈ 0.707** — damping
  where no peaking.
- Order N: attenuation `20N dB/dec`; magnitude squared `1/(1 + (f/f_c)^{2N})`.
- Butterworth poles lie on a circle (left half-plane).
- Realizing a 2nd-order Butterworth LPF:
  - Sallen-Key with `Q = 0.707` (e.g., equal-R with unequal C, or gain selection).
  - Example: `R1=R2=R`, `C1 = 2C`, `C2 = C/2` → Q ≈ 0.707 (standard pair).
- 1st-order Butterworth: just the `1/(1+jf/f_c)` (Q undefined conceptually).

### Cascade for higher order
- Butterworth of order 4 = two 2nd-order sections in series with chosen Q's, or
  1st + 2nd for odd orders.
- Each section's `f_c` equal; overall roll-off = sum of individual slopes.

---

## 22.6 Band-pass formulas (GATE-standard)

- Centre `f_o = 1/(2π√(R1·R2·C1·C2))` for a tuned LCR/op-amp filter.
- `BW = f_H − f_L`; `Q = f_o/BW`.
- Roll-offs: 20 dB/dec both sides (1st-order each side) → 40 dB/dec total.

### Notch (band-stop)
- Twin-T (passive) + op-amp buffer gives a sharp 50 Hz notch.
- Q adjustable; used to kill mains hum.

---

## 22.7 Worked examples

**Q1. 1st-order LPF via integrator:** R1 = 1 kΩ, R2 = 10 kΩ, C = 1 nF.
- DC gain = −10. `f_c = 1/(2π·10k·1n) = 15.9 kHz`. Roll 20 dB/dec.

**Q2. Sallen-Key equal RC unity:** R = 10 kΩ, C = 10 nF.
- `f_o = 1/(2π·10k·10n) ≈ 1.59 kHz`. Q = 1/3 (equal components). Slightly
  underdamped → no peaking, knee starts ~fo, slope 40 dB/dec above.

**Q3. Butterworth 2nd-order:** wanted Q = 0.707 from Sallen-Key. Using gain-free
design `R1=R2=R`, choose `C1 = 2C`, `C2 = C` (or C/2) whatever satisfies
`Q = √(C1C2)/(C1+C2·(…))`... convention: `C1 = 2C, C2 = C`:
- `ω_o = 1/(R√(2C·C)) = 1/(√2·RC)`; `Q ≈ 0.707`. Done.

---

## GATE traps (filters)

1. **Q = f_o/BW** only for band-pass. LPF/HPP "Q" is a sharpness quantity.
2. Butterworth means *Q = 0.707*, i.e., no peaking — not "any sharp filter."
3. Equal-component Sallen-Key unity = Q 1/3; gain-3 Sallen-Key → oscillation.
   The k→3 transition is a favourite MCQ.
4. Roll-off `= 20·order dB/dec`. 2nd-order is 40, not 20.
5. Corner: for `H=1/(1+jf/fc)`, gain at f_c = −3 dB (not −6).
6. Active filter cost: op-amp must supply the passband gain; beyond its GBW the
   "active" part vanishes → real filters droop.

---

## 5-question self-check

1. 2nd-order roll-off? → *40 dB/dec.*
2. Q for Butterworth? → *1/√2.*
3. Sallen-Key equal-C equal-R unity Q? → *1/3.*
4. Gain k of Sallen-Key → oscillation threshold? → *3.*
5. Notch/Band-stop kills? → *one narrow band (e.g., 50 Hz).*

Next: **`23-Schmitt-Trigger-Comparators.md`**