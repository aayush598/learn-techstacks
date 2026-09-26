# Chapter 01 — Prerequisites (Circuit Fundamentals, AC Basics, Math)

> **The idea in one line:** Analog circuits are just KCL/KVL applied to resistors,
> capacitors, inductors, and active devices. If you can find Thevenin equivalents
> and write phasor impedances, you can solve every circuit in this syllabus.

---

## 1.1 Circuit fundamentals

### Ohm's law
`V = I·R`, `I = V/R`, `R = V/I`. Always ask: *voltage across the resistor?* The
current through a resistor is always `(voltage across it) / (its resistance)`.
This single habit solves most diode/transistor numericals.

### KCL (Kirchhoff's Current Law)
Sum of currents **entering** a node = sum of currents **leaving** it.
Also written: `Σ i = 0` with entering currents positive.
*Analogy:* water flowing into a pipe junction must equal water flowing out.

### KVL (Kirchhoff's Voltage Law)
Sum of voltage **rises** = sum of voltage **drops** around any closed loop.
Equivalently `Σ V = 0` around a loop (one direction positive).
*Analogy:* going up a staircase and coming back down — net height change is zero.

### Voltage division
Two resistors `R1`, `R2` in series across a voltage `V`:
`V1 = V·R1/(R1+R2)`, `V2 = V·R2/(R1+R2)`.
**GATE habit:** never compute current first — divide directly.

### Current division
Two resistors `R1`, `R2` in parallel fed by current `I`:
`I1 (through R1) = I·R2/(R1+R2)`.
The current divides **inversely** with resistance. Larger resistor → less current.

### Series and parallel
Series: `R = R1 + R2`, same current through all. Parallel: `R = R1·R2/(R1+R2)`
or `1/R = 1/R1 + 1/R2`, same voltage across all.
- Capacitors: series `C = C1·C2/(C1+C2)`, parallel `C = C1 + C2` (opposite of resistors).
- Inductors: same rule as resistors.

### Thevenin's theorem
Any linear one-port network can be replaced by:
- **`V_th`**: open-circuit voltage at the terminals, and
- **`R_th`**: equivalent resistance with all independent sources killed
  (voltage sources shorted, current sources opened).
This is *the* most-used theorem in analog. Example: finding the base voltage and
input resistance of a voltage-divider bias network.

### Norton's theorem
Any linear one-port = **`I_N`** (short-circuit current) in parallel with **`R_N`**.
`I_N = V_th/R_th` and `R_N = R_th`.

### Source transformation
A voltage source `V` in series with `R` ⇔ current source `V/R` in parallel with `R`.
Useful: converts messy circuits into single-loop or single-node circuits.

### Superposition
In a linear circuit with multiple independent sources, take each source one at a
time (others killed), sum the contributions. **Only for linear circuits** —
never for power (`P = I²R` is nonlinear).

### Maximum power transfer
To maximum power from source `V_th, R_th` into load `R_L`:
`R_L = R_th`. Max power `= V_th²/(4·R_th)`.

### Mesh analysis
Write KVL around each mesh; unknown loop currents. Good when few loops.
Mesh current shared by two meshes = algebraic difference.

### Nodal analysis
Write KCL at each node; unknown node voltages. Good when few nodes.
This is what you'll use for op-amp and small-signal circuits.

---

## 1.2 AC circuit basics

### Sinusoidal signals
`v(t) = V_m·sin(ωt + φ)`. 
- `V_m` = peak amplitude
- `ω = 2πf` = angular frequency (rad/s)
- `φ` = phase (radians or degrees)
- `T = 1/f` = period

### Phasors
A sine is represented as a complex number: `V = V_m ∠φ` (polar)
or `V = V_m·e^{jφ}` (exponential). All circuit math becomes algebra.
Multiplication of two sines is hard; addition of phasors is vector addition.

### Complex impedance
`Z = V/I` in phasor form:
- Resistor: `Z_R = R` (real, no phase shift)
- Capacitor: `Z_C = 1/(jωC) = -j/(ωC)`. Current **leads** voltage by 90°.
- Inductor: `Z_L = jωL`. Current **lags** voltage by 90°.

**Memory aid for capacitive phase:** C → "Current leads" (both start with C).

### Complex admittance
`Y = 1/Z` = conductance + susceptance: `Y = G + jB`.
- Capacitor admittance `Y_C = jωC`
- Inductor admittance `Y_L = 1/(jωL) = -j/(ωL)`
Parallel combinations: add admittances (like conductances).

### Magnitude and phase
For `Z = R + jX`: `|Z| = √(R² + X²)`, `∠Z = tan⁻¹(X/R)`.
For a series `RC`: `|Z| = √(R² + 1/(ωC)²)`.

### RMS values
RMS (effective) value of a sinusoidal waveform `= V_m/√2`.
RMS value = *DC value* that would deliver the same average power to a resistor.
- DC: RMS = DC value.
- Full-wave rectified sine: `V_m/√2` (same as sine).
- Half-wave rectified sine: `V_m/2` (average `V_m/π`; RMS `V_m/2`). **Memorize.**

### Frequency-response basics
Gain `= V_out/V_in` is itself a function of frequency:
`A(f) = A_mid · (1/(1 + j f/f_c))` type factors.
- Low-pass: capacitor across output / in feedback.
- High-pass: capacitor in series (coupling).
- `f_c = 1/(2πRC)` = corner / cutoff / 3-dB frequency.

---

## 1.3 Mathematics toolbox

### Complex numbers
- `a + jb` rectangular, `r∠θ` polar. `r = √(a²+b²)`, `θ = tan⁻¹(b/a)`.
- Multiplication: multiply magnitudes, add angles.
- Division: divide magnitudes, subtract angles.
- `j = √-1`, `1/j = -j`.

### Logarithms and decibels
- `dB = 20·log10(V2/V1)` for voltages (or currents).
- `dB = 10·log10(P2/P1)` for powers.
- **Note:** 3 dB (voltage) = factor √2 ≈ 1.414; a "10× voltage" = 20 dB.
- Doubling power = +3 dB (= +3.01 dB exactly).
- `log(a·b) = log a + log b`; `log(a/b) = log a − log b` — used to multiply
  cascade stage gains in dB.

Table of common voltage ratios:

| Ratio | dB |
|-------|-----|
| 1     | 0   |
| √2    | 3   |
| 2     | 6   |
| 10    | 20  |
| 100   | 40  |
| 1000  | 60  |
| 0.1   | −20 |
| 0.707 (1/√2) | −3 |

### Differentiation quick list
- `d/dx x^n = n·x^(n-1)`
- `d/dx sin x = cos x`, `d/dx cos x = −sin x`
- `d/dx e^x = e^x`, `d/dx ln x = 1/x`
- `d/dx sin(ax) = a·cos(ax)`

### Integration quick list
- `∫ x^n dx = x^(n+1)/(n+1)`
- `∫ sin(ax) dx = −cos(ax)/a`
- `∫ cos(ax) dx = sin(ax)/a`
- `∫ e^{ax} dx = e^{ax}/a`

### First-order differential equations (RC/RL transients)
`τ = RC` (or `L/R`).
- Charging: `v_C(t) = V_final + (V_0 − V_final)·e^{-t/τ}`
- Universal form: `value(t) = final + (initial − final)·e^{-t/τ}`.
- In **one time constant** (t = τ): 63% of the way from initial to final.
- After **5τ**: steady state (99.3%).

### Approximation techniques
- `e^{-x} ≈ 1 − x` for small x. Used for small-signal diode resistance.
- `1/(1+x) ≈ 1 − x` for small x.
- `√(1+x) ≈ 1 + x/2` for small x.
- In parallel resistors, if `R2 >> R1`, then `R1||R2 ≈ R1`.

---

## GATE traps (prerequisites)

1. **Do not** compute the current when a voltage divider answer can be read
   directly — you lose time.
2. When you "kill a source," a **current source is opened**, a **voltage source
   is shorted** — swapping these is the #1 Thevenin error.
3. Series capacitor rule is `C1C2/(C1+C2)` — students habitually add. Check.
4. `20·log10` for voltages, `10·log10` for powers. Same 3 dB means *"half power"*
   but for *voltage* 3 dB ≈ √2 (not 2×).
5. Half-wave RMS is `Vm/2`, NOT `Vm/(2√2)` and not `Vm/π`. The average (`Vm/π`)
   and RMS (`Vm/2`) are different numbers — know both.
6. `1/j = −j` is the single most-fumbled algebra step in AC analysis.

---

## 5-question self-check

1. Find the Thevenin voltage of: 12 V source in series with 6 kΩ, load taken
   across a 6 kΩ shunt. → *V = 6 V (divider).*
2. `v(t) = 10 sin(1000t)`. Impedance of a 1 µF cap at this frequency?
   → *Z = 1/(1000·10^-6) = 1 kΩ → Z = −j1 kΩ.*
3. RMS of a 311 V peak sine? → *220 V.*
4. What is 0.1 in dB? → *−20 dB.*
5. An RC circuit with R = 10 kΩ, C = 1 µF. Time constant? → *10 ms.*

Next chapter: **`02-Diodes-Basics-and-Models.md`**