# Op-Amp Integrators and Differentiators — Practice (Learn by Solving)

> **The idea in one line:** put a **capacitor in the feedback** and the op-amp
> integrates; put it **in the input path** and the op-amp differentiates. This
> file drills both transfer functions, every waveform mapping, the saturation
> behaviour, and the one resistor that fixes each circuit.
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve
> the next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `21-Op-Amp-Integrators-Differentiators.md` or `32-Single-File-Cheatsheet.md`
> only when you want the underlying theory.

## Concept box (what you must internalise)

- Ideal inverting integrator: `v_o = −(1/RC)·∫v_in dt`, `H(jω) = −1/(jωRC)`, `|H| = 1/(ωRC)` — a −90° low-pass.
- Ideal differentiator: `v_o = −RC·dv_in/dt`, `H(jω) = −jωRC`, `|H| = ωRC` — a +90° high-pass.
- Ramp slope for a **DC/square** input: `dv_o/dt = −v_in/RC`. Negative input slope for positive input. **Method:** slope is always `V/RC`, never `V/R`.
- Triangle p-p from a square: `ΔV_o(pp) = (V_pk/RC)·(T/2) = V_pk/(2f·RC)`. **Method:** area under a square of height V and width τ is `V·τ`; divide by `RC`.
- Practical fixes: `R_f` **across** `C` (integrator → DC gain `−R_f/R1`, corner `1/(2πR_fC)`); `R_s` **in series with** `C` (differentiator → HF gain `−R/R_s`, corner `1/(2πR_sC)`).
- **Trap:** both formulas carry a **minus sign**. Drop it and every waveform polarity, every threshold, every saturation question is wrong.

---

## Questions

### Q1. (Easy) An ideal inverting integrator has `R = 10 kΩ` and `C = 0.1 µF`. What is the time constant `RC`, and what is `|H|` at `f = 1 kHz`?
**Answer:** `RC = 10 kΩ × 0.1 µF = 1 ms`. At 1 kHz, `ω = 2π×1000 = 6283 rad/s`, so `|H| = 1/(ωRC) = 1/6.283 = 0.159` — i.e. **−16 dB**, phase −90°.
**Method:** Two steps only. (1) `RC = 10e3 × 0.1e-6 = 1e-3 s`. (2) Ideal integrator magnitude is `1/(2πfRC)` — put `f = 1000`, `RC = 1e-3` → `1/6.283 = 0.159`. Sanity check: the gain equals 1 where `f = 1/(2πRC) = 159 Hz`; ten times that frequency must give one-tenth the gain, and 0.159 ≈ 1/6.3 is exactly right.

### Q2. (Easy) The same integrator (RC = 1 ms) is fed a **constant** `v_in = +2 V` DC. What is `dv_o/dt`?
**Answer:** `dv_o/dt = −v_in/RC = −2/1e-3 = **−2000 V/s**` (= −2 V/ms, = −2000 V/s = −20 V per 10 ms).
**Method:** Differentiate the transfer function in time once: `v_o = −(1/RC)∫v_in dt` ⇒ `dv_o/dt = −v_in/RC`. A positive DC input drives the output **negative** and linearly. Never write the slope as `V/R` — the capacitor current is `v_in/R`, and `i = C·dv_o/dt` puts the extra `C` in the denominator.

### Q3. (Easy) A square wave of **±1 V** is applied to an integrator with `RC = 0.1 s`. What is the output waveform and its slope on each half-cycle?
**Answer:** A **triangle wave**. Slope is `−(+1)/0.1 = −10 V/s` while `v_in = +1 V`, and `−(−1)/0.1 = +10 V/s` while `v_in = −1 V`. So the output ramps down at 10 V/s, then up at 10 V/s.
**Method:** `dv_o/dt = −v_in/RC`. Plug the two levels, note the sign flip. Triangle-wave "in" and "ramp out" is the single most-tested mapping in this chapter — see `21-Op-Amp-Integrators-Differentiators.md` §21.1.

### Q4. (Easy) An ideal differentiator has `R = 10 kΩ`, `C = 0.1 µF` (so `RC = 1 ms`). The input is a triangle of constant slope `+500 V/s`. What is `v_o`?
**Answer:** `v_o = −RC·(dv_in/dt) = −1e-3 × 500 = **−0.5 V**, constant.** So a triangle in gives a **negative square** out.
**Method:** Because `dv_in/dt` is constant on each ramp, the output is constant on each ramp — that is exactly "square out". Sign: a *rising* ramp gives a *negative* output (op-amp inverts). The magnitude is `RC × slope`; units check: `1e-3 s × 500 V/s = 0.5 V` ✓.

### Q5. (Easy) For the same differentiator (`RC = 1 ms`), at what frequency does `|H| = 1` (0 dB)?
**Answer:** `|H| = ωRC = 1` ⇒ `ω = 1/RC = 1000 rad/s` ⇒ `f = 1000/(2π) = **159.2 Hz**`.
**Method:** Set `|H| = 1` in `|H| = ωRC`. This is the mirror image of the integrator, where `|H| = 1` also at `f = 1/(2πRC) = 159.2 Hz` — the same "break frequency", one falling and one rising. Recognise `159 Hz` for a 1 ms time constant and you have memorised a table entry.

### Q6. (Easy) Match each input waveform to the ideal **integrator** output and to the ideal **differentiator** output: (a) square, (b) triangle, (c) sine, (d) DC.
**Answer:**
- (a) square → integrator: **triangle**; differentiator: **spikes/impulses at the edges**.
- (b) triangle → integrator: **parabola**; differentiator: **square**.
- (c) sine → integrator: **cosine, amplitude × 1/(ωRC), lagging 90°**; differentiator: **cosine, amplitude × ωRC, leading 90°**.
- (d) DC → integrator: **unbounded linear ramp (saturates)**; differentiator: **0 V output** (dv/dt = 0).
**Method:** Use the operator view. Integration = division by `jω`; differentiation = multiplication by `jω`. For a square, the derivative is impulsive; for a triangle, the derivative is piecewise constant. For DC the derivative is zero — that asymmetry (DC killed by the differentiator, DC amplified by the integrator) is worth 1 mark by itself.

---

### Q7. (Easy) An ideal differentiator has `RC = 1 ms` and is driven by a square wave that steps `0 → 5 V` in `5 µs`. What is the output spike at the rising edge, and at the falling edge?
**Answer:** `v_o = −RC·Δv/Δt = −1e-3 × (5/5e-6) = **−1000 V** at the rising edge**, and **+1000 V** at the falling edge. Physically the op-amp clips at its rails; the ideal number just proves the point.
**Method:** Differentiate a step: `Δv/Δt = 5 V/5 µs = 1e6 V/s`. Multiply by `RC = 1e-3` → 1000 V. Sign from the leading minus. A real op-amp with `SR = 0.5 V/µs` only moves `0.5 × 5 = 2.5 V` in that 5 µs (Q17) — which is *why* the practical differentiator exists.

### Q8. (Easy) A square wave of **±5 V at 1 kHz** drives an integrator with `RC = 1 ms`, starting from `v_o(0) = 0`. Find the slope and the triangle's peak-to-peak value.
**Answer:** Slope = `5/1e-3 = 5000 V/s` (down while `v_in = +5 V`, up while `−5 V`). Half period `T/2 = 0.5 ms`, so each ramp covers `5000 × 0.5e-3 = 2.5 V`. The triangle swings between `0 V` and `−2.5 V`, so **p-p = 2.5 V**.
**Method:** slope = `V/RC`; then multiply by the half-period. The convenient compact form is `ΔV_pp = V_pk/(2f·RC)`: `5/(2 × 1000 × 1e-3) = 2.5 V` ✓. Do not forget the −5 V half-cycle ramps *back up* — a symmetric square does **not** drift (Q26 is the asymmetric case).

### Q9. (Easy) Design the integrator: a **±2 V, 500 Hz** square must become a triangle of **4 V p-p**. Find `RC`. If `C = 10 nF`, what is `R`?
**Answer:** `f = 500 Hz` ⇒ `T/2 = 1 ms`. The ramp must climb 4 V in 1 ms ⇒ slope = 4000 V/s. `slope = V_pk/RC` ⇒ `RC = 2/4000 = **0.5 ms**`. With `C = 10 nF`: `R = 0.5e-3/1e-8 = **50 kΩ**`.
**Method:** Work backwards from the required slope, never from the gain — an integrator has no gain, it has a **slope**. Then split `RC` any way you like (this is the key freedom: `RC` alone is fixed, `R` and `C` individually are not). Check: `RC = 50e3 × 10e-9 = 5e-4` ✓.

### Q10. (Easy) A **practical** integrator has `R1 = 1 kΩ`, feedback `R_f ∥ C` with `R_f = 10 kΩ`, `C = 1 nF`. Find the low-frequency gain and the corner frequency.
**Answer:** Low-frequency (DC) gain = `−R_f/R1 = **−10**`. Corner `f_c = 1/(2π·R_f·C) = 1/(2π × 10e3 × 1e-9) = **15.9 kHz**`. Below `f_c` it is a gain-of-−10 amplifier; above it, an integrator rolling off at 20 dB/dec.
**Method:** Identify the two elements in the feedback branch and use them for two different jobs. `R_f` sets the **DC gain** (it is the feedback impedance at ω = 0); `R_f·C` sets the **corner frequency** — the corner uses `R_f`, not `R1`. Common slip: using `R1 C = 1e-3 × ...` — `R1C` here is `1 µs`, which would give 159 kHz and is wrong.

### Q11. (Moderate) For the practical integrator of Q10, what is `|H|` (i) exactly at `f_c` and (ii) at `10 f_c`?
**Answer:** `H = −(R_f/R1)/(1 + jωR_fC)`, so at `f_c` the magnitude is `10/√2 = **7.07**` (−3 dB). At `10 f_c`, `|H| = 10/√(1 + 100) = **0.995**` ≈ 1, i.e. `−20 dB` relative to the passband.
**Method:** A first-order response falls 3 dB at the corner, and 20 dB per decade above it. 20 dB/dec from a value of 10 ⇒ `10/10 = 1`. Cross-check with the ideal-integrator asymptote: `|H| ≈ 1/(ωR1C)`; at `f = 10f_c = 159 kHz`, `ω = 1e6`, `1/(1e6 × 1e3 × 1e-9) = 1` ✓.

### Q12. (Moderate) The ideal integrator has `RC = 1 ms`. Evaluate `|H|` at `f = 159 Hz`, `1.59 kHz`, `15.9 kHz`. What dB per decade is that?
**Answer:** `|H| = 1/(ωRC)`: at 159 Hz → `1.00`; at 1.59 kHz → `0.100`; at 15.9 kHz → `0.0100`. Each decade divides the gain by 10 = **20 dB/decade** (equivalently 6 dB/octave).
**Method:** The whole "integrator = 20 dB/dec" claim is just three substitutions. `1/(2π×159×1e-3) = 1.0`; `1/(2π×1590×1e-3) = 0.1`; `1/(2π×15900×1e-3) = 0.01`. If your three numbers are 1, 0.1, 0.01 you have the roll-off right; if they come out 1, 0.3, 0.1 you have accidentally used a 2nd-order filter.

### Q13. (Moderate) An ideal integrator has `R = 100 kΩ`, `C = 0.01 µF` and is fed `v_in = 0.1 V` DC, starting at `v_o = 0`. Rails are `±12 V`. How long until the output hits a rail?
**Answer:** `RC = 100e3 × 0.01e-6 = 1e-3 s = 1 ms`. Slope = `−0.1/1e-3 = −100 V/s`. Time to reach `−12 V` = `12/100 = **0.12 s**` (120 ms).
**Method:** Three numbers, in this order: `RC`, then slope `V/RC`, then `t = rail/slope`. Note how long 0.12 s is compared to `RC = 1 ms` — the ideal integrator's time constant is 100× too fast to hold any DC, which is the physical reason it always runs away.

### Q14. (Moderate) A **practical** differentiator uses input `R_s = 1 kΩ` in series with `C = 0.1 µF`, and feedback `R = 10 kΩ`. Find the high-frequency gain limit and the corner.
**Answer:** HF gain limit = `−R/R_s = **−10**`. Corner `f_c = 1/(2π·R_s·C) = 1/(2π × 1e3 × 0.1e-6) = **1.59 kHz**`. Below that corner `|H| ≈ ωRC` (still rising at 20 dB/dec); above it the gain is pinned at −10.
**Method:** Note the symmetry with the practical integrator: **the extra resistor sets the flat-gain region, and its product with C sets the corner**. Integrator: `R_f ∥ C`, gain `−R_f/R1`, corner `1/(2πR_fC)`. Differentiator: `R_s + C`, gain `−R/R_s`, corner `1/(2πR_sC)`. Both corners use the *added* resistor. The exact gain is `|H| = R/√(R_s² + 1/(ωC)²)`, and the corner sits 3 dB below the flat value.

### Q15. (Moderate) An ideal integrator has `RC = 0.1 s` and `v_o(0) = 2 V`. At `t = 0` the input becomes `−1 V` DC. Find `v_o` at `t = 1 s`.
**Answer:** `v_o(t) = v_o(0) − (1/RC)·v_in·t = 2 − (1/0.1)(−1)(1) = 2 + 10 = `**`+12 V`**.
**Method:** Never forget the initial-condition term: `v_o(t) = v_o(0) − (1/RC)∫v_in dt`, and substitute the input **with its sign**. A `−1 V` DC input makes the output **rise** at `1/RC = 10 V/s`, so after 1 s it has climbed 10 V from its 2 V starting point to 12 V. Sign discipline in one line: the contribution is `−(v_in/RC)·t = −(−1/0.1)(1) = +10 V` — a negative input gives a *positive* contribution, which is exactly the integrating action (the sign flip and the time integral). The trap answer is `−8 V`, which comes from dropping the minus sign on `v_in`.

### Q16. (Moderate) State the phase relationship of each circuit's output to its input, and what that implies for a square wave.
**Answer:** Integrator: output **lags** input by **90°** (`H = −1/(jωRC) = j/(ωRC)`, i.e. `+90°` of `−j`... write it as −90°, pure lag). Differentiator: output **leads** input by **90°** (`H = −jωRC`). For a **square** wave, whose fundamental sits at `f`, a 90° shift is a **quarter period**: the integrator's triangle therefore *starts* its fall at the square's positive-going transition, and the differentiator's spike *coincides* with the edge itself.
**Method:** `−1/j = +j` and `1/j = −j`; the integrator's phase is `−90°`, the differentiator's `+90°`. The 90°-shift interpretation is the fastest way to draw the output: shift the input by a quarter of a cycle and then integrate/differentiate the shape.

### Q17. (Moderate) Q7 revisited realistically: `RC = 1 ms`, a `0 → 5 V` edge in `5 µs`, but the op-amp has `SR = 0.5 V/µs`. What output amplitude is actually reached?
**Answer:** The op-amp can only change `0.5 V/µs × 5 µs = **2.5 V**` during the edge, so the "spike" is at most 2.5 V (and in practice a rounded 2.5 V ramp), not the ideal 1000 V.
**Method:** Slew rate is a **V/s** ceiling. Edge time × SR = maximum voltage change. Compare: ideal wants `RC·ΔV/Δt = 1000 V`, the slew rate permits 2.5 V — a factor of 400 short. Whenever an ideal differentiator asks for hundreds of volts, the exam is testing whether you remember `SR`; see `SR ≥ 2πf_max V_pk` in `32-Single-File-Cheatsheet.md` §8.

### Q18. (Moderate) Ideal integrator, `RC = 1 ms`. Evaluate `|H|` at `f = 100 Hz` and convert to dB.
**Answer:** `|H| = 1/(2π × 100 × 1e-3) = 1/0.6283 = **1.591**` = `20log₁₀(1.591) = ` **+4.04 dB**.
**Method:** Below the break frequency an integrator has **gain greater than 1** — that surprises people, and it is the whole motivation for the practical version (which caps the passband gain at `R_f/R1`). Compute dB with `20log₁₀`, always, for voltage.

### Q19. (Moderate) A practical integrator must have `f_c = 1 kHz` with `R_f = 10 kΩ` fixed. What value of `C` do you need?
**Answer:** `C = 1/(2π·R_f·f_c) = 1/(2π × 1e4 × 1e3) = **15.9 nF**`.
**Method:** Invert `f_c = 1/(2πR_fC)` → `C = 1/(2πR_f f_c)`. `2π × 1e4 × 1e3 = 6.283e7`; `1/6.283e7 = 1.59e-8 F = 15.9 nF` ✓. Practical pick: 15 nF or 18 nF E-series. Always use `R_f` in this corner formula, never `R1`.

### Q20. (Moderate) **Exact** answer for the practical integrator: `R1 = 10 kΩ`, `R_f = 100 kΩ`, `C = 10 nF`, driven by a **±0.5 V, 5 kHz** square. What is the true triangle p-p, given `τ = T/2 = 0.1 ms` and `τ_f = R_f C = 1 ms`?
**Answer:** The exact steady-state peak is `x = k·tanh(τ/2τ_f)` with `k = V·R_f/R1 = 0.5 × 10 = 5 V`. `τ/2τ_f = 0.1/2 = 0.05`, `tanh(0.05) = 0.02499`. So `x = 0.125 V` and **p-p = 0.250 V** — while the ideal integrator would have given `0.5 V`, and the `R_f`-limited ceiling is `2k = 10 V`.
**Method:** The practical integrator satisfies `dv_o/dt + v_o/(R_fC) = −v_in/(R1C)`, so each half-cycle is an exponential relaxing toward `−(R_f/R1)V_in`. Solving the half-cycle recursion for a symmetric input gives `ΔV_pp = 2(R_f/R1)V·tanh(T/(4R_fC))`. The three numbers to keep in your head: `τ ≫ 4R_fC` ⇒ ideal answer; `τ ≈ R_fC` ⇒ badly attenuated; `τ ≪ R_fC` ⇒ a plain gain of `−R_f/R1`.

---

### Q21. (Moderate) A relaxation oscillator uses a Schmitt trigger (`V_sat = ±10 V`, `R1 = 2 kΩ` to input, `R_f = 10 kΩ`) driving an integrator (`R = 10 kΩ`, `C = 10 nF`, `RC = 0.1 ms`). Find the threshold, the triangle p-p, and the oscillation frequency.
**Answer:** Threshold `V_th = V_sat·R1/R_f = 10 × 2/10 = **2 V**`, so `UT = +2 V`, `LT = −2 V`. The integrator ramp must cross `4 V`. Square amplitude ±10 V into `RC = 1e-4 s` gives slope `10/1e-4 = 1e5 V/s`, so `T/2 = 4/1e5 = 40 µs`, `T = 80 µs`, and **f = 1/80 µs = 12.5 kHz**.
**Method:** This is the classic 2-op-amp square→triangle generator (`21-...md` §21.5). Three steps: (1) Schmitt threshold from `29-Formula-Sheet.md` §29.10; (2) the ramp must travel `2V_th`; (3) time = distance/slope with `slope = V_sat/RC`. General form worth memorising: `T = 4·R1·R·C/R_f`, so `f = R_f/(4R1RC) = 1e4/(4 × 2e3 × 1e-3) = 1e4/8 = 1.25e4 Hz` ✓.

### Q22. (Moderate) A differentiator must turn a **±2 V, 1 kHz triangle** into a **5 V square**. Find `RC`; with `C = 10 nF`, what is `R`?
**Answer:** Triangle slope = `4f·V_pk = 4 × 1000 × 2 = **8000 V/s**`. `RC = v_o/slope = 5/8000 = **0.625 ms**`. With `C = 10 nF`: `R = 0.625e-3/1e-8 = **62.5 kΩ**`.
**Method:** The trick is converting "triangle" to "slope" first. A symmetric triangle of peak `V_pk` at frequency `f` climbs `2V_pk` in `T/2`, so slope `= 4fV_pk`. Then `|v_o| = RC × slope`. Sanity check with Q4's rule: a bigger `RC` gives a bigger output square; 0.625 ms × 8000 V/s = 5 V ✓.

### Q23. (Moderate) An ideal differentiator (`RC = 1 ms`) amplifies HF noise without limit. By what factor is the gain at **1 MHz** greater than at **1 kHz**?
**Answer:** A factor of `f` ratio = `1e6/1e3 = **1000**`. (Absolute: `|H(1 kHz)| = 2π×1e3×1e-3 = 6.28`; `|H(1 MHz)| = 6283`; ratio 1000.)
**Method:** `|H| = ωRC` is *linear* in frequency, i.e. **+20 dB/decade**. Every extra decade of HF junk gets the same extra 20 dB. This is the fundamental instability of the ideal differentiator and the reason `R_s` (Q14) must be added: without it, noise above the signal band wins, and with phase lag in the op-amp the "amplifier" oscillates.

### Q24. (GATE-level) Ideal differentiator, `RC = 1 ms`, input a **1 V peak** sine, rails `±10 V`. Above what frequency does the output clip?
**Answer:** `|v_o|max = ωRC·V_pk ≤ 10 V` ⇒ `ω ≤ 10/(1e-3 × 1) = 1e4 rad/s` ⇒ `f ≤ 1e4/(2π) = **1.59 kHz**`. Above 1.59 kHz the output is clipped.
**Method:** Differentiate a sine: `dv_in/dt` has peak `ωV_pk` (the factor `2π` is the classic slip — a sine's *maximum slope* is `2πf·V_pk`, not `f·V_pk`). Then multiply by `RC` and compare to the rail. Note this same expression appears as the slew-rate check `SR ≥ 2πf V_pk` in `32-Single-File-Cheatsheet.md` §8.

### Q25. (GATE-level) For what frequency does a square wave of peak `V` produce a triangle whose **p-p equals the square's own p-p** (`2V`)? Answer in terms of `R` and `C`.
**Answer:** `ΔV_pp = V/(2fRC) = 2V` ⇒ `f = 1/(4RC)`. With `R1 = 10 kΩ`, `C = 10 nF`: `f = 1/(4 × 1e3 × 1e-8) = **2.5 kHz**`.
**Method:** Equate the ramp excursion to the input excursion. General result: **above `1/(4RC)` the output triangle is smaller than the input square; below it the output is larger** (and eventually runs into the rails). This one relation tells you, for any `RC`, whether the circuit is "compressing" or "expanding" the waveform — a very common 2-mark comparison question.

### Q26. (GATE-level) A **+1 V / −1 V square of 40 % duty cycle** (`+1 V for 0.4 ms`, `−1 V for 0.6 ms`, `T = 1 ms`) drives an ideal integrator with `R1 = 10 kΩ`, `C = 10 nF`. What is the output after one full period, starting from `v_o = 0`? What if `R_f = 100 kΩ` is added?
**Answer:** `RC = 1e-4 s`. First half: slope `−1/1e-4 = −1e4 V/s` for 0.4 ms ⇒ `v_o = −4 V`. Second half: `+1e4 V/s` for 0.6 ms ⇒ `v_o = −4 + 6 = `**+2 V**. Net **+2 V of upward drift per period** — the output sawtooths away and hits the rails. With `R_f = 100 kΩ` added, the drift stops: the mean output settles at `−(R_f/R1)·mean(v_in) = −10 × (−0.2 V) = `**+2 V**`, and only the ripple rides on it.
**Method:** Ideal integrator net drift per period `= (V/RC)(t₂ − t₁) = 1e4 × 0.2e-3 = 2 V`. The mean of the input is `(1)(0.4) + (−1)(0.6) = −0.2 V` per ms. For the practical circuit, average `dv_o/dt = 0` over a steady state: `0 = −mean(v_in)/(R1C) − mean(v_o)/(R_fC)` ⇒ `mean(v_o) = −(R_f/R1)·mean(v_in)`. **A DC-balanced (50 %-duty) square never drifts; any duty-cycle offset is a DC input, and an integrator turns DC into a ramp.**

### Q27. (GATE-level) Practical integrator, `R1 = 1 kΩ`, `R_f = 10 kΩ`, `C = 1 nF`, `v_o(0) = 0`. A `+1 V` step is applied at `t = 0`. Give `v_o` at one time constant and at steady state.
**Answer:** `τ = R_f C = 10 µs`; `v_o(t) = −(R_f/R1)(1 − e^{−t/τ}) = −10(1 − e^{−t/10µs}) V`. At `t = 10 µs`: `−10(1 − 0.368) = `**−6.32 V**. At steady state: `−(R_f/R1) × 1 = `**−10 V** (not infinity, and not the ideal `−1/µs` ramp to −10 V in 10 µs — the two happen to arrive at −10 V at the same instant here, but by different routes).
**Method:** The practical integrator's step response is the standard charging exponential toward `−(R_f/R1)V_step`, with time constant `R_fC` (**not** `R1C`, and **not** `R1C‖...`). Write the answer as the full expression `v_o(t) = −(R_f/R1)(1 − e^{−t/R_fC})`; then any asked instant is a substitution, and `1/e = 0.368` at one `τ`, `0.99` at five.

### Q28. (GATE-level) Which statement about the two practical circuits is **correct**?
- (A) The practical integrator's corner frequency uses `R1`, not `R_f`.
- (B) The practical differentiator's high-frequency gain is `−R/R_s`, reached **above** `1/(2πR_sC)`.
- (C) Adding `R_s` to the differentiator lowers its gain at every frequency.
- (D) Adding `R_f` across the integrator's capacitor increases its bandwidth.
**Answer:** **(B).** (A) is false — the integrator's corner is `1/(2πR_fC)`. (C) is false — `R_s` changes nothing below the corner; it only *limits* the gain above it (that is the point). (D) is false — `R_f` **lowers** the corner frequency, narrowing the integrating region.
**Method:** For each option, name the formula it contradicts before deciding. The two "one resistor fixes it" facts to hold in your head: `R_f ∥ C` caps the integrator's *passband gain*; `R_s + C` caps the differentiator's *stopband gain*. Both caps cost you nothing below the corner.

### Q29. (GATE-level) Design a practical differentiator (`C` in series with `R_s`, then `R` in feedback) whose gain **rises at 20 dB/dec through 1 kHz, where `|H| = 1`**, and **flattens above 10 kHz at `|H| = 10`**. Use `C = 1 nF`.
**Answer:** `C = 1 nF`. Rising region: `|H| = ωRC = 1` at 1 kHz ⇒ `R = 1/(2π×1000×1e-9) = `**159.2 kΩ**. Flat gain: `R/R_s = 10` ⇒ `R_s = 15.92 kΩ`, whose corner is `1/(2πR_sC) = 1/(2π×15.92e3×1e-9) = `**10.0 kHz** ✓ (consistent by construction). Exact spot checks with `|H| = R/√(R_s² + 1/(ωC)²)`: at 1 kHz `|H| = 0.995`; at 3.16 kHz `|H| = 3.01`; at 10 kHz `|H| = 10/√2 = 7.07` (the corner is −3 dB below the flat gain).
**Method:** Two design equations, two independent parts. The "rise" is set by `R` (`|H| = ωRC`); the "flat" is set by `R_s` (`|H| → R/R_s`). `1/(2πRC) = 1.59 kHz` is the *unity-gain* point — below it the circuit attenuates rather than differentiates, which is why a practical differentiator is a **band-pass**, never a full high-pass. Use the exact form `|H| = R/|R_s + 1/(jωC)|` for any spot check; the shortcuts `ωRC` and `R/R_s` are its two limits.

### Q30. (GATE-level) Take the integrator `R = 10 kΩ, C = 10 nF` and the differentiator `R = 10 kΩ, C = 10 nF`. Compare their gains at `f = 1 kHz` and at `f = 10 kHz`, and say what swapping the resistor and capacitor does.
**Answer:** `RC = 1e-4 s`. Integrator: `|H| = 1/(2πfRC)` → at 1 kHz, `1.591`; at 10 kHz, `0.159`. Differentiator: `|H| = 2πfRC` → at 1 kHz, `0.628`; at 10 kHz, `6.28`. So they are exact reciprocals at every frequency, and the product of the two gains is 1. **Swapping R and C (a frequency-dependent impedance) interchanges integration and differentiation**; the break frequency `1/(2πRC) = 1.59 kHz` is unchanged, only the slope direction flips (20 dB/dec falling ↔ rising).
**Method:** `|H_int|·|H_diff| = [1/(ωRC)]·[ωRC] = 1` — a 30-second check that catches a sign or an inverted `RC`. Also note the "1" crossover: each circuit passes `|H| = 1` at exactly `f = 1/(2πRC) = 1.59 kHz`, one falling through it and one rising.

### Q31. (GATE-level) `R = 10 kΩ`, `C = 10 nF` ideal integrator, rails `±12 V`. A **±3 V, 1 kHz** square is applied from `v_o = 0`. Does the output clip? If not, what is the triangle's p-p and its mean?
**Answer:** Slope = `3/1e-4 = 3e4 V/s`; half period `0.5 ms` ⇒ `ΔV_pp = 3e4 × 0.5e-3 = `**15 V (ideal, unclipped)**, swinging between `0` and `−15 V`. But only `−12 V` exists, so **the output clips**: the actual triangle is truncated to **12 V p-p** (0 to −12 V, mean `−6 V`) and the top of the ramp is flat instead of linear.
**Method:** Compute the ideal p-p **first**, then compare with the available rail-to-rail span (24 V here). A 15 V p-p triangle centred at −7.5 V needs `−15 V`, which does not exist. GATE loves this: the "ideal answer" and the "rail-limited answer" are both needed, and you must say which one applies. Rule of thumb: an integrator's usable input is limited by (available swing)/2.

### Q32. (GATE-level) A practical integrator must accept `0.5 V` DC without ever leaving `±15 V` rails. `R1 = 1 kΩ`. What is the largest `R_f` you may use?
**Answer:** Steady-state gain must satisfy `(R_f/R1) × 0.5 ≤ 15` ⇒ `R_f/R1 ≤ 30` ⇒ **`R_f ≤ 30 kΩ`**. With `R_f = 100 kΩ` the ideal steady state would be `−50 V`, so the output rails and stays there.
**Method:** The DC gain of the practical integrator is `−R_f/R1`, so the design rule is `R_f/R1 ≤ (rail)/(V_DC,max)`. A secondary effect: larger `R_f` also raises the corner (`1/(2πR_fC)`), so a large `R_f` both overloads the DC path and slows the response. Keeping `R_f/R1` between 1 and 10 is the usual engineering habit.

### Q33. (GATE-level) Summarise, in one line each, what changes when you go from the **ideal** to the **practical** integrator and differentiator, and what each fix costs.
**Answer:** Integrator: add `R_f` **across** `C` → DC gain becomes `−R_f/R1` (finite), corner appears at `1/(2πR_fC)`; **cost:** the circuit is no longer a perfect integrator below that corner, and the integrating range starts at `1/(2πR_fC)`. Differentiator: add `R_s` **in series with** `C` → HF gain becomes `−R/R_s` (finite), corner at `1/(2πR_sC)`; **cost:** differentiation only works above `1/(2πR_sC)`, and below it you just have a gain of `−R/R_s`. **Both fixes are a gain/bandwidth trade: infinite gain at one end of the spectrum becomes a bounded gain, and the usable frequency range shrinks.**
**Method:** Know *where* each resistor goes (`R_f ∥ C` vs `R_s + C`) and *what each one sets* (passband gain vs corner). The unifying statement: an unbounded gain in either direction is unbuildable, so you clamp the gain and pay with a corner.

---

## Trap box (exam-day killers)

- **The minus sign.** `v_o = −(1/RC)∫v_in dt` and `v_o = −RC·dv_in/dt`. Drop it and every polarity, every threshold crossing and every saturation answer flips.
- **Slope is `V/RC`, not `V/R`.** Students write `dv_o/dt = v_in/R` and lose the `1/C` factor immediately.
- **Triangle p-p is `V_pk/(2fRC)`, not `V_pk/(fRC)`.** The ramp lasts only `T/2`.
- **Wrong corner resistor.** The practical integrator's corner is `1/(2π·R_f·C)` (uses `R_f`, not `R1`); the practical differentiator's is `1/(2π·R_s·C)` (uses `R_s`, not `R`).
- **Confusing the two corners of the practical differentiator.** `1/(2πRC)` is where `|H| = 1`; `1/(2πR_sC)` is where the gain *stops* rising at `R/R_s`. The circuit is a band-pass.
- **Forgetting `v_o(0)`** in `v_o = v_o(0) − (1/RC)∫v_in dt`. A "capacitor initially uncharged" clause means `v_o(0) = 0` — read for it.
- **Assuming saturation never happens.** Any DC content integrates to a rail; a 50 %-duty square does not drift but *any* duty-cycle error does (Q26).
- **Ignoring slew rate on differentiator spikes.** The ideal answer (hundreds of volts) is not the physical one; `SR × edge time` caps it.
- **`|H| = 1` for an integrator at `f = 1/(2πRC)`, same as the differentiator** — students think only the integrator has a "break frequency". Both do; the slope direction is what differs.

## Final recall drill (do in 60 seconds)

1. Ramp slope for `v_in = +3 V`, `RC = 0.1 s` → −30 V/s.
2. `|H|` of an integrator with `RC = 1 ms` at `1 kHz` → `1/(2π) = 0.159`.
3. `|H|` of a differentiator with `RC = 1 ms` at `1 kHz` → `6.28`.
4. Practical integrator's DC gain with `R1 = 2 kΩ`, `R_f = 20 kΩ` → `−10`.
5. Practical integrator's corner with `R_f = 10 kΩ`, `C = 10 nF` → `1.59 kHz`.
6. Practical differentiator's HF gain with `R = 47 kΩ`, `R_s = 4.7 kΩ` → `−10`.
7. Square ±5 V, `RC = 1 ms`, 1 kHz → triangle p-p = 2.5 V.
8. Frequency where an integrator with `RC = 1 ms` has `|H| = 1` → 159 Hz.
9. Add what to an ideal integrator? → `R_f` **across** `C`; add what to an ideal differentiator? → `R_s` **in series with** `C`.
10. Triangle in, integrator out → parabola; square in, differentiator out → spikes.
11. Differentiate a DC input → 0 V. Integrate a DC input → unlimited ramp.
12. Integrator phase / differentiator phase → −90° (lag) / +90° (lead).

---
