# Chapter 05 — Rectifiers

> **The idea in one line:** A rectifier converts AC into pulsating DC. You must
> know, for each circuit: the average (DC) output, the RMS output, ripple
> factor, efficiency, and each diode's **PIV** (the reverse voltage it must
> survive). Learn to *derive* these, not just memorize.

---

## 5.1 The key concepts first

Definitions that make everything fall into place:

- **Average / DC value** of waveform `v`: `V_dc = (1/T) ∫₀ᵀ v dt`. For a
  half-wave sine it's `Vm/π`. For a full-wave rectified sine it's `2Vm/π`.
- **RMS value**: `V_rms = √((1/T)∫₀ᵀ v² dt)`. This is the value that produces
  the *same heating* in a resistor as a DC voltage.
  - Half-wave: `Vm/2`. Full-wave: `Vm/√2` (same as a pure sine).
- **Ripple**: the ripple component left after removing the DC. Its RMS value,
  `V_r`, measures how "not-DC" the output is.
- **Ripple factor `γ`**: `γ = V_r/R V_dc = √((V_rms/V_dc)² − 1)`.
  - Half-wave: `γ = 1.21`. Full-wave: `γ = 0.48`. **Memorize these two.**
- **Rectification efficiency `η`**: `η = P_dc/P_ac(in)` — the fraction of input
  AC power that comes out as DC power.
  - Half-wave ideal: `40.6%`. Full-wave ideal: `81.2%`.
- **PIV** = Peak Inverse Voltage = maximum reverse voltage a diode must block.

---

## 5.2 Half-wave rectifier (HWR)

Circuit: transformer (or source) → single diode → load `R_L`.
- Diode conducts the positive half, blocks the negative.
- Output = only positive half-sines.

Key results (ideal diode, load `R`):
```
V_dc      = Vm/π          ≈ 0.318·Vm
V_rms     = Vm/2          = 0.5·Vm
γ (ripple)= 1.21  (121%)
η         = 40.6%
f_ripple  = f_in          (one ripple pulse per input cycle)
PIV       = Vm            (the diode must block the full negative peak)
TUF       = 0.287         (transformer utilization — low, poor transformer use)
```
- Average current `I_dc = Vm/(πR)`.
- Ripple-frequency = input frequency (only one hump per cycle).

### GATE derived facts
- DC voltage of HWR ≈ `0.318 Vm` ≈ `0.45 × (RMS input)`.
- Because the diode drops 0.7 V, real `V_dc ≈ (Vm − 0.7)/π`.

---

## 5.3 Full-wave rectifier (FWR)

Two forms, identical output maths:

### Centre-tapped full-wave
- Two diodes + centre-tapped transformer.
- Each diode feeds one half-of-the-secondary (each AC secondary = `Vm/2`? no —
  secondary across half = `Vm` measured from centre-tap).
  Precisely: with secondary voltage `Vm` between each end and the centre tap,
  each diode conducts on alternate half-cycles.
- PIV of each diode = `2·Vm` (it must block the full secondary across BOTH ends).
- Diode drop `Vγ`: output loses `Vγ` each half.

### Bridge rectifier
- Four diodes, no centre tap. Transformer used more fully.
- On positive half: D1 & D3 conduct; negative: D2 & D4.
- PIV of each diode = `Vm` (not 2Vm!) — this is the advantage.
- Diode drop: two diodes in series each half → output loses `2·Vγ`.

Key results, both types (ideal):
```
V_dc      = 2Vm/π         ≈ 0.637·Vm
V_rms     = Vm/√2         = 0.707·Vm
γ         = 0.48  (48%)
η         = 81.2%
f_ripple  = 2·f_in         (two humps per input cycle)
PIV       = bridge: Vm ; centre-tap: 2Vm
TUF       = 0.812 (bridge), 0.693 (centre-tap)
```

### Comparison table (ideal diodes)

| Quantity | Half-wave | Full-wave (both types) |
|----------|-----------|------------------------|
| V_dc | Vm/π | 2Vm/π |
| V_rms | Vm/2 | Vm/√2 |
| γ | 1.21 | 0.48 |
| η | 40.6% | 81.2% |
| f_ripple | f | 2f |
| PIV | Vm | CT: 2Vm ; bridge: Vm |
| No. diodes | 1 | CT: 2 ; bridge: 4 |

**With practical diode drops (silicon):**
- HWR: `V_dc = (Vm − 0.7)/π`.
- CT-FWR: `V_dc = (Vm − 0.7)·2/π`.
- Bridge: `V_dc = (Vm − 1.4)·2/π`.
- The bridge loses **two** drops; remember the factor in a numerical.

---

## 5.4 Capacitor filter (the "smoothed" rectifier)

Add a capacitor `C` across the load. The capacitor charges to the peak when the
diode conducts and supplies the load between peaks.

```
 v_out ┐ ┌────────────────┐
       ┘ │     │          │      ripple voltage
         └────┘    └──────┘
               t (period T, ripple freq f_r)
```
Ripple with capacitor filter (approximately a straight-down-then-exponential):
```
V_r ≈ I_dc / (f_r · C)          = V_dc / (f_r · R_L · C)
```
where `f_r` = ripple frequency (`f` for HWR, `2f` for FWR).

Consequences:
- Bigger `C` → smaller ripple. Bigger load current (`I_dc`) → larger ripple.
- `V_dc` ≈ `Vm − V_r/2` (drops slightly below peak due to ripple).
- Ripple factor with filter ≈ `V_r / V_dc ≈ 1/(f_r·R_L·C)`.
- Peak diode current is large (capacitor charging spikes) — GATE sometimes
  asks why the diode current is pulsating.
- If `R_L` removed (no load), cap holds the peak forever → output = `Vm`.

### Ripple factor approximations to quote
- HWR + C filter: `γ ≈ 1/(√3 · f·R_L·C)` if we model the discharge ramp (book
  formula) — GATE commonly uses `γ = 1/(f_r R_L C)` or sleeps with the
  `I/(4√3 f C V)` form. **Use `V_r ≈ I_dc/(f_r·C)`** as the cleanest general one.

---

## 5.5 Worked GATE-style numericals

**Q1. HWR, ideal, 230 V (rms) input through an ideal transformer, load 1 kΩ.**
Find DC output, ripple factor, efficiency, PIV.

- Convert rms→peak: `Vm = 230·√2 ≈ 325.3 V`.
- `V_dc = Vm/π = 103.6 V`.
- `V_rms = Vm/2 = 162.6 V`.
- `γ = 1.21`, `η = 40.6%`, `PIV = Vm = 325.3 V`.

**Q2. Bridge rectifier, `Vm = 20 V`, silicon diodes, load 1 kΩ.**
- `V_dc = (20 − 1.4)·2/π ≈ 18.6·0.637 = 11.84 V`.
- RMS output `≈ (20 − 1.4)/√2 = 13.15 V`.
- Each diode PIV = 20 V.
- Ripple frequency = `2·f`.

**Q3. Full-wave rectifier with C filter. Load 10 mA, C = 100 µF, mains 50 Hz.**
Find ripple voltage.
- `f_r = 2·50 = 100 Hz`.
- `V_r = I_dc/(f_r·C) = 10m/(100·100µ) = 10m/0.01 = 1 V`.

**Q4. What does the transformer utilization factor measure?**
How well the transformer's *rated VA* is turned into output DC watts. HWR is
~0.287 (bad), FWR-bridge ~0.812 (best of the three).

---

## 5.6 GATE traps (rectifiers)

1. **Never use the average = RMS.** `Vm/π` vs `Vm/2` for HWR — two different
   things; students swap them.
2. PIV for the **centre-tapped** is `2Vm`, for **bridge** is `Vm`. This is a
   favourite one-line trap.
3. Ripple frequency: HWR = f, FWR = 2f. "Which rectifier has double ripple
   frequency?" → full-wave.
4. Bridge diode-count: 4; the 0.7 V penalty is `2·0.7 = 1.4 V` total.
5. With capacitor filter, increasing load *resistance* → smaller current →
   smaller ripple. Increasing *capacitance* → smaller ripple. (Inverses!)
6. Efficiency is a *ratio of powers* — the rectifier's `η` uses input AC power
   absorbed, so diode/transformer losses make it less than the ideal numbers.
7. Regulator vs rectifier: a capacitor filter smooths (lowers ripple) but does
   *not* hold a stiff DC voltage under load changes (a regulator does).

---

## 5-question self-check

1. HWR ideal, `Vm = 100 V`. V_dc? → *31.8 V.*
2. Bridge, ideal `Vm = 100 V`. V_dc? → *63.7 V.*
3. CT-FWR ideal `Vm = 40 V` (each half). PIV per diode? → *80 V = 2Vm.*
4. FWR ripple frequency for 60 Hz mains? → *120 Hz.*
5. To halve the ripple of a C-filtered FWR by changing only C, new C = ?
   → *double C* (ripple ∝ 1/C).

Next chapter: **`06-BJT-Fundamentals.md`**