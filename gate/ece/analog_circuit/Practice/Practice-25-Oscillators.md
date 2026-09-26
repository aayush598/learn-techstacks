# Oscillators — Practice (Learn by Solving)

> **The idea in one line:** every oscillator question in GATE is one of two
> jobs — *find the frequency* (from an RC network, an LC tank, or a relaxation
> timing loop) or *check the gain/phase condition* (Barkhausen). This file drills
> both until the formulas come out without thinking.
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve
> the next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `25-Oscillators.md` or `32-Single-File-Cheatsheet.md` only when you want the
> underlying theory.

## Concept box (what you must internalise)

- **Barkhausen:** sustained oscillation needs `|Aβ| = 1` **and** `∠Aβ = 0°` at
  `f_o` — both conditions, together, at the same frequency.
- **Start-up:** `|Aβ| > 1` slightly (then a nonlinearity shrinks the *effective*
  gain back to 1). Saying "it must equal 1 to start" is a false statement.
- **Phase-shift oscillator:** `f_o = 1/(2π·R·C·√6)`, minimum gain **29**;
  3 RC sections give 180°, the inverting amplifier gives the other 180°.
- **Wien bridge:** `f_o = 1/(2π·R·C)`, gain **3** (i.e. `1 + Rf/R1 = 3` →
  `Rf = 2R1`).
- **Colpitts:** capacitors in **series** → `C_eff = C1C2/(C1+C2)`.
  **Hartley:** inductors in **series** → `L_eff = L1 + L2`. One swapped
  combination = wrong answer.
- **Relaxation:** `T = 2·R·C·ln(1 + 2R1/R2)`, thresholds `±V_sat·R1/(R1+R2)`;
  output is a **square** (Schmitt) and a **triangle** (integrator), never a sine.
- **Method:** convert *every* timing element to one number first (C_eff, L_eff,
  or RC), then `f = 1/(2π·√(L·C))` or `f = 1/(2π·R·C)`. Never mix a series
  combination where a parallel one belongs.
- **Trap:** Wien's gain is 3, phase-shift's is 29. Swapping the two numbers is
  the single most common oscillator mistake.

---

## Questions

### Q1. (Easy) State the two conditions a feedback loop must satisfy to sustain a sinusoidal oscillation, and say what each one controls.
**Answer:** `|Aβ| = 1` (the gain/magnitude condition — it fixes the amplitude) and `∠Aβ = 0°` or 360° (the phase condition — it fixes the frequency at which the loop adds in phase). Both must hold **at the same frequency**.
**Method:** Barkhausen is two equations, not one. Mark the question: if it says "loop gain must be 1" only, it is incomplete; if it says "at the frequency where the phase shift around the loop is 0°", it is complete. Source: `25-Oscillators.md` §25.1.

### Q2. (Easy) An RC phase-shift oscillator uses three identical RC sections and an inverting amplifier. What is the minimum magnitude of the amplifier gain for sustained oscillation?
**Answer:** `|A| ≥ 29` (at exactly 29 it sustains; to be safe, design for 30–40).
**Method:** The 3-section ladder supplies 180°; the inverting amplifier supplies the remaining 180°. The ladder's attenuation at that frequency is `β = 1/29`, so `Aβ = 1` needs `A = 29`. Memorise 29 for phase-shift; it is never 3. Source: `25-Oscillators.md` §25.3.

### Q3. (Easy) A Wien bridge oscillator uses equal R and C. Write its oscillation frequency and the amplifier gain it needs.
**Answer:** `f_o = 1/(2πRC)`, gain `= 3` (for the non-inverting op-amp: `1 + Rf/R1 = 3`).
**Method:** The Wien lead–lag network has zero phase shift at `f_o = 1/(2πRC)` and `β = 1/3`, so the amplifier must supply exactly 3 to make `Aβ = 1`. Source: `25-Oscillators.md` §25.3.

### Q4. (Easy) A Colpitts oscillator has `C1 = 2 nF` and `C2 = 2 nF` as the tapped capacitive divider. Write the effective capacitance that sets the frequency.
**Answer:** `C_eff = C1C2/(C1+C2) = 4/4 = 1 nF` (series combination).
**Method:** Colpitts taps *capacitors*, so the two caps are effectively in series across the coil. Always reduce the divider to one number first, then use `f_o = 1/(2π√(L·C_eff))`. Source: `25-Oscillators.md` §25.4.

### Q5. (Easy) A Hartley oscillator has `L1 = 1 mH`, `L2 = 3 mH` and `C = 1 µF`. What is the effective inductance and the oscillation frequency?
**Answer:** `L_eff = L1 + L2 = 4 mH`; `f_o = 1/(2π√(4m·1µ)) = 1/(2π·6.325e-5) = 2.52 kHz`.
**Method:** Hartley taps the *inductor*, so the two windings add in series: `L_eff = L1 + L2`. Then `√(L·C) = √(4×10⁻³ × 10⁻⁶) = 6.32×10⁻⁵`, `2π×6.32×10⁻⁵ = 3.97×10⁻⁴`, `f_o = 1/3.97×10⁻⁴ = 2.52 kHz`. (Do not use "7.96 kHz" — that slips into the wrong square root; recheck `√(4e-9) = 6.32e-5`, not `2e-4`.) Source: `25-Oscillators.md` §25.4.

### Q6. (Easy) What waveform does a relaxation oscillator built from an op-amp Schmitt trigger and an RC timing network produce, and where does the triangle come from?
**Answer:** A **square** wave at the Schmitt output (sitting exactly on `±V_sat`), and a **triangle** from a following integrator driven by that square. It is *not* sinusoidal.
**Method:** The Schmitt supplies the two rails, the RC supplies the timing slope. A relaxation oscillator never produces a clean sine; a phase-shift, Wien, Colpitts or Hartley oscillator does. Source: `25-Oscillators.md` §25.5.

### Q7. (Easy) True or false: for an oscillator to *start* oscillating, the loop gain magnitude must be exactly 1.
**Answer:** **False.** Start-up needs `|Aβ| > 1`; sustained steady state needs `|Aβ| = 1`. Amplitude limiting (device saturation or a lamp/diode limiter) then pulls the effective gain back to unity.
**Method:** If `|Aβ| < 1` at every frequency, the oscillation decays to zero (damped). If `|Aβ| > 1`, it grows until the amplifier saturates and the effective `A` falls to `1/β`. Source: `25-Oscillators.md` §25.1.

### Q8. (Easy) In a Wien bridge oscillator built around a non-inverting op-amp with gain `1 + Rf/R1`, what value of `Rf/R1` gives exactly the minimum gain for sustained oscillation?
**Answer:** `Rf/R1 = 2` (so `1 + 2 = 3`).
**Method:** The bridge attenuates by `β = 1/3` at `f_o`, so `Aβ = 1` needs `A = 3`. The `1 +` in the non-inverting gain formula is where the 3 comes from: `1 + Rf/R1 = 3`. Source: `25-Oscillators.md` §25.3.

### Q9. (Easy) A phase-shift oscillator has `R = 10 kΩ` in all three sections and `C = 10 nF`. Find the oscillation frequency, and the minimum gain.
**Answer:** `RC = 10k × 10n = 100 µs`; `f_o = 1/(2π·100µ·√6) = 1/(2π·100µ·2.449) = 1/(1.539×10⁻³) = 650 Hz`. Minimum gain = 29.
**Method:** Do the two steps separately: (1) `RC = 1×10⁻⁴ s`. (2) `2πRC√6 = 6.283×10⁻⁴ × 2.449 = 1.539×10⁻³`. (3) `f_o = 1/1.539e-3 ≈ 650 Hz`. Round the intermediate product, not the formula — keeping `2πRC√6` as one product avoids the classic 6.5 kHz / 650 Hz factor-of-10 slip. Source: `25-Oscillators.md` §25.6.

### Q10. (Easy) A Wien bridge oscillator has `R = 10 kΩ` and `C = 100 nF`. Find `f_o` and the required amplifier gain.
**Answer:** `RC = 10k × 100n = 1 ms`; `f_o = 1/(2π·10⁻³) = 159 Hz`. Gain = 3.
**Method:** Wien has **no √6 factor** — that factor belongs to the unbuffered 3-section phase-shift ladder only. `2πRC = 6.283×10⁻³`, `f_o = 1/6.283×10⁻³ = 159.2 Hz`. Source: `25-Oscillators.md` §25.3.

### Q11. (Easy) A Colpitts oscillator has `L = 1 mH`, `C1 = 2 nF`, `C2 = 2 nF`. Find `C_eff` and `f_o`.
**Answer:** `C_eff = 2·2/(2+2) = 1 nF`; `L·C = 10⁻³ × 10⁻⁹ = 10⁻¹²`; `√(LC) = 10⁻⁶`; `f_o = 1/(2π×10⁻⁶) = 159 kHz`.
**Method:** Reduce first (`C_eff = 1 nF`), then the arithmetic is a clean power of 10. If the numbers don't come out to a round power of 10, you probably forgot the series step. Source: `25-Oscillators.md` §25.6.

### Q12. (Moderate) A Hartley oscillator has `L1 = L2 = 1 mH` and `C = 1 µF`. Find `f_o`, and express it relative to a tank that used only a single 1 mH coil with the same C.
**Answer:** `L_eff = 2 mH`; `L·C = 2×10⁻³ × 10⁻⁶ = 2×10⁻⁹`; `√(LC) = 4.472×10⁻⁵`; `f_o = 1/(2π×4.472e-5) = 3.56 kHz`. Ratio to the single-1 mH case: `1/√2 = 0.707`, i.e. **44% lower** in frequency.
**Method:** Adding inductance always *lowers* `f_o` (`f ∝ 1/√L`). `1/√2 = 0.707` is the exact ratio for a doubling of L. Source: `25-Oscillators.md` §25.4.

### Q13. (Moderate) An op-amp relaxation oscillator has `R = 10 kΩ`, `C = 10 nF`, and the hysteresis divider `R1 = R2 = 10 kΩ`. Find the period, the frequency, and the two threshold voltages (symmetric rails).
**Answer:** `T = 2·R·C·ln(1 + 2R1/R2) = 2×10⁻⁴·ln(3) = 2×10⁻⁴×1.0986 = 220 µs`; `f = 1/220µ = 4.55 kHz`; thresholds `= ±V_sat·R1/(R1+R2) = ±V_sat/2`.
**Method:** `2RC = 2×10⁻⁴ s`, `1 + 2(10/10) = 3`, `ln 3 = 1.0986`, `T = 2.197×10⁻⁴ s`, `f = 4551 Hz`. The threshold is the *divider ratio* `R1/(R1+R2) = 0.5` times `V_sat` — same divider, different expression. Source: `29-Formula-Sheet.md` §29.12.

### Q14. (Moderate) A relaxation oscillator has `R1 = 10 kΩ`, `R2 = 20 kΩ`, `V_sat = ±10 V`. Compute the two switching thresholds, the hysteresis width, and the charge time per half cycle if `R = 10 kΩ, C = 10 nF`.
**Answer:** Thresholds `= ±10 × 10k/30k = ±3.33 V`; hysteresis = `6.67 V`; `T = 2×10⁻⁴·ln(1 + 2×10/20) = 2×10⁻⁴·ln 2 = 1.386×10⁻⁴ s = 138.6 µs`; `f = 7.21 kHz`. Half period = 69.3 µs.
**Method:** The `ln` term is the *same* divider ratio: `1 + 2R1/R2 = 1 + 1 = 2`. Always check that the two formulas use the *same* `R1` (the feedback resistor) and `R2` (the resistor to ground) — if the chapter's `ln` form and its threshold form ever disagree, you have mixed up R1 and R2. Source: `25-Oscillators.md` §25.5.

### Q15. (Moderate) A Wien bridge op-amp oscillator has `R1 = 10 kΩ` in the non-inverting arm. What `Rf` gives exactly gain 3, and what happens if you fit `Rf = 10 kΩ` instead?
**Answer:** `Rf = 2R1 = 20 kΩ`. With `Rf = 10 kΩ`, `A = 1 + 1 = 2`, so `Aβ = 2/3 = 0.67 < 1` → the circuit will not oscillate; any noise present dies away.
**Method:** The loop gain is `Aβ = A/3`. Below 3, no oscillation; exactly 3, marginal; above 3, it starts and the amplitude limiter brings the effective gain back to 3. Source: `25-Oscillators.md` §25.3.

### Q16. (Moderate) An RC phase-shift oscillator has `β = 1/29` at `f_o`. Give the loop gain and the verdict for amplifier gains of 28, 29 and 31.
**Answer:** `A = 28` → `Aβ = 0.966 < 1`: no oscillation (damped). `A = 29` → `Aβ = 1.00`: sustained (marginal). `A = 31` → `Aβ = 1.069 > 1`: starts, grows, then amplitude-limiting reduces the effective gain to 29.
**Method:** `Aβ = A/29`. The pass/fail test is one comparison; the *only* one that cannot start from noise is the first. Real designs pick ~30–40 for start-up margin. Source: `25-Oscillators.md` §25.1.

### Q17. (Moderate) A 32.768 kHz watch crystal has `Q = 10⁴`. What is its −3 dB bandwidth, and what does that number say about the oscillator's frequency stability?
**Answer:** `BW = f₀/Q = 32768/10⁴ = 3.28 Hz`. The oscillation frequency can only drift a couple of hertz around 32.768 kHz, i.e. about 1 part in 10⁴ — hence the crystal is the timing element of every watch.
**Method:** `Q = f₀/BW` → `BW = f₀/Q`. Bigger Q, narrower bandwidth, better frequency definition. A plain LC tank (Q ≈ 100) would drift by ~328 Hz. Source: `25-Oscillators.md` §25.4.

### Q18. (Moderate) The same R and C are used in a phase-shift oscillator and a Wien bridge oscillator. What is the ratio of their oscillation frequencies?
**Answer:** `f_phase-shift / f_Wien = 1/√6 = 0.408`, i.e. the phase-shift frequency is **2.45× lower**. Conversely `f_Wien/f_phase-shift = √6 = 2.449`.
**Method:** Both use `1/(2πRC)` as a base; only the phase-shift ladder carries the `√6`. If you ever forget the √6, your phase-shift answer comes out 2.45× too high — the classic detectable error. Source: `25-Oscillators.md` §25.3.

### Q19. (Moderate) A student solves a Colpitts problem with `C1 = C2 = 1 nF` by using `C_eff = C1 + C2 = 2 nF` instead of the series value. By what factor is the answer wrong, and in which direction?
**Answer:** `2 nF` instead of `0.5 nF` is 4× too large in `C`, so `f_o` is `1/√4 = 0.5` — exactly **half** the correct frequency.
**Method:** `f_o = 1/(2π√(L·C_eff))`, so the error in `C_eff` is halved in `f_o`. A 2:1 frequency error is a *recognisable* wrong answer, so GATE expects you to catch it. Correct: `C_eff = 1×1/2 = 0.5 nF`. Source: `25-Oscillators.md` §25.4.

### Q20. (Moderate) Match the oscillator to its band of use: phase-shift, Wien bridge, Colpitts, crystal. Which two are the audio/low-frequency ones and which is the precise reference one?
**Answer:** Phase-shift and Wien bridge are the **audio / low-frequency (RC)** types; Colpitts is the **RF (LC)** type; the **crystal** oscillator is the precise reference (Q up to 10⁵). Hartley is also RF.
**Method:** Decide by *what sets the frequency*: an RC time constant → low frequency; an LC tank → high frequency; a piezoelectric resonance → precision. Frequency-setting element ⇒ band. Source: `25-Oscillators.md` §25.2.

### Q21. (Moderate) A square wave of `±1 V` drives an op-amp integrator with `R_int = 10 kΩ`, `C_int = 10 nF`. What is the output ramp slope, and what shape is the output?
**Answer:** Slope `= V/(R·C) = 1/(10k × 10n) = 1/10⁻⁴ = 10⁴ V/s = 10 V/ms`, alternating sign → a **triangle**.
**Method:** The integrator's slope is `±V_in/(R·C)`, independent of the output voltage (that's what makes it an ideal integrator). Square in, triangle out; triangle in, square out through a Schmitt. Source: `21-Op-Amp-Integrators-Differentiators.md`, `25-Oscillators.md` §25.5.

### Q22. (Moderate) An amplifier has gain `A = −20` and the feedback network gives `β = +1/20`. Does the circuit oscillate? Justify with the two Barkhausen conditions.
**Answer:** No. `|Aβ| = 20 × 0.05 = 1` — the magnitude condition is met — but `∠Aβ = 180° ≠ 0°`, so the loop is in **negative** feedback and is stable. The closed-loop gain is `A/(1 − Aβ) = −20/(1+1) = −10`, finite.
**Method:** Test both conditions separately. `|Aβ| = 1` alone is *not* sufficient — a loop with 180° of phase returns the signal inverted and settles. This is exactly the trap that `25-Oscillators.md` §25.1 warns about. Source: `25-Oscillators.md` §25.1.

### Q23. (Moderate) A sine wave of amplitude 6 V is applied to a Schmitt trigger with `V_sat = ±12 V`, `R1 = 10 kΩ` (feedback arm), `R_f = 30 kΩ`. What does the output look like, and what are the two switching levels?
**Answer:** `V_th = 12 × 10k/40k = 3 V`, so the output is a **square wave that switches only at ±3 V** — flat at +12 V above +3 V and at −12 V below −3 V. Hysteresis width = 6 V.
**Method:** The Schmitt is a *hysteretic* switch: the output edges occur only when the input crosses `+V_th` (rising) or `−V_th` (falling), so a small input excursion produces no output change. Noise smaller than the 6 V dead band cannot re-trigger it. Source: `28-Graphical-Interpretation.md` §28.7, `23-Schmitt-Trigger-Comparators.md`.

### Q24. (Moderate) Does the frequency of an op-amp relaxation oscillator depend on the supply rail voltage `V_sat`?
**Answer:** **No** — and that is its great advantage. `T = 2RC·ln(1 + 2R1/R2)` contains only R, C and the divider ratio. The rail voltage only sets the *amplitude* (±V_sat square, triangle peak = `±V_th = ±V_sat·R1/(R1+R2)`).
**Method:** Read the formula and list what is in it. Frequency from R, C, divider ratio; amplitude from the rails. Supply-noise rejection falls out of this for free — a useful GATE one-liner. Source: `25-Oscillators.md` §25.5.

### Q25. (Moderate) A phase-shift oscillator uses `R = 4.7 kΩ`, `C = 22 nF` in every section. Find `f_o`. Then the *same* R and C are used in a Wien bridge. Find that `f_o` and the required gain of each.
**Answer:** Phase-shift: `RC = 1.034×10⁻⁴`, `f_o = 1/(2π×1.034e-4×2.449) = 628 Hz`, gain ≥ 29. Wien: `f_o = 1/(2π×1.034×10⁻⁴) = 1.54 kHz`, gain = 3.
**Method:** Identical R and C, two different answers — because the phase condition networks differ (3 loaded sections with `√6` vs a balanced bridge with no factor). `1/(2πRC) = 1539 Hz`; multiply the phase-shift result by `2.449` to get `1539` back. Source: `25-Oscillators.md` §25.3.

---

### Q26. (GATE-level) A phase-shift oscillator is redesigned so that each RC section is **buffered** (an amplifier isolates every section, so sections do not load each other). Derive the new `f_o` and the new minimum gain for `R = 10 kΩ`, `C = 10 nF`.
**Answer:** Each isolated high-pass section is `H = jωRC/(1 + jωRC)`, whose phase is `90° − arctan(ωRC)`. For 3 sections to give 180° each must give 60°, so `arctan(ωRC) = 30°` → `ωRC = 1/√3` → **`f_o = 1/(2πRC√3) = 919 Hz`**. At that point `|H| = (1/√3)/√(1+1/3) = 0.5` per section, so `β = 0.5³ = 1/8` and the minimum gain is **8** (`Aβ = 1`). Compare: unbuffered 650 Hz and gain 29.
**Method:** Derive, don't memorise. (1) Write the isolated-section transfer function and its phase. (2) `3 × 60° = 180°`. (3) Read the attenuation at that same frequency. (4) `A = 1/β`. The numbers change because buffering removes the loading that produced the `√6` and the extra attenuation of the 29. Both answers are right for their own circuit — state which one your circuit is. Source: `25-Oscillators.md` §25.3.

### Q27. (GATE-level) A Wien bridge is balanced at `f_o` with `β = 1/3 ∠0°`. The amplifier gain is exactly 3. Compute `|β|` and the phase of `β` at `2f_o`, and say whether the loop can oscillate there.
**Answer:** With `x = ωRC = 2` (`f = 2f_o`), `Z1 = R(1 − j/2)`, `Z2 = R/(1 + 2j) = R(0.2 − 0.4j)`, so `β = Z2/(Z1+Z2) = (0.2 − 0.4j)/(1.2 − 0.9j) = 0.2667 − 0.1333j` → `|β| = 0.298`, phase `= −26.6°`. Loop gain `= 3 × 0.298 = 0.894 ∠−26.6°`: magnitude **< 1** and phase ≠ 0, so the loop **cannot** sustain oscillation at `2f_o`. The bridge is strongly frequency-selective — that selectivity is why the Wien oscillator doesn't wander.
**Method:** Evaluate the network at the new frequency and check *both* Barkhausen conditions. The `−26.6°` is `arctan(0.5)`; note the network's phase is zero only at `f_o`, and its attenuation is worst exactly at the edges of the band, which is what pins `f_o`. Source: `25-Oscillators.md` §25.3, `01-Prerequisites.md` (complex divider).

### Q28. (GATE-level) A Schmitt trigger with symmetric `±12 V` rails and `R1 = R2` feeds an integrator with `R_int = 10 kΩ`, `C_int = 10 nF`. Derive the triangle-generator frequency in terms of `V_sat`, `R_int`, `C_int` and `V_th`, then evaluate it.
**Answer:** The integrator ramps between `−V_th` and `+V_th` at slope `±V_sat/(R_int·C_int)`, so the half period is `2V_th·R_int·C_int/V_sat` and `T = 4·V_th·R_int·C_int/V_sat`, i.e. **`f = V_sat/(4·V_th·R_int·C_int)`**. Here `V_th = 12/2 = 6 V`: `f = 12/(4×6×10⁻⁴) = 12/2.4×10⁻³ = 5.0 kHz`.
**Method:** Time = (distance travelled)/(slope) = `(2V_th)/(V_sat/(R_int C_int))`. Double it for the full period, invert. This is the only frequency formula an op-amp triangle generator ever needs — no `ln` term appears. Source: `25-Oscillators.md` §25.5.

### Q29. (GATE-level) A crystal oscillator has `Q = 10⁵`; a Colpitts LC tank has `Q = 10²`. Both nominally sit at 10 MHz. Compare their −3 dB bandwidths and the resulting frequency uncertainty.
**Answer:** Crystal: `BW = 10⁷/10⁵ = 100 Hz`. LC tank: `BW = 10⁷/10² = 100 kHz`. The crystal is **1000× more frequency-selective**, so it holds its frequency to ~1 part in 10⁵ while the LC oscillator wanders by ~1 part in 10².
**Method:** `BW = f₀/Q`. Everything else being equal, Q *is* the stability. This is the standard "why crystals?" one-mark answer: the oscillation frequency is set by a mechanical resonance whose Q is enormous, not by a lossy electrical tank. Source: `25-Oscillators.md` §25.4.

### Q30. (GATE-level) A Sallen–Key filter built with equal R, equal C and a non-inverting amplifier of gain `k` has `Q = 1/(3 − k)`. What happens as `k → 3`, and how does this connect to the Barkhausen criterion?
**Answer:** `Q → ∞`: the filter loses its damping and the poles move onto the imaginary axis, i.e. the circuit **oscillates**. This is Barkhausen in disguise: the loop gain has reached `Aβ = 1` with 0° of net phase, so the filter has become an oscillator. For `k > 3` the circuit is unstable and blows up to the rails.
**Method:** `Q = 1/(3−k)` is the same statement as "loop gain = 1". Stable filter ⇒ `Aβ < 1` ⇒ `k < 3`; `k = 3` ⇒ marginal/oscillating; `k > 3` ⇒ positive feedback runaway. A favourite GATE conceptual link between filters and oscillators. Source: `22-Active-Filters.md`, `25-Oscillators.md` §25.1.

### Q31. (GATE-level) Design a Wien bridge oscillator for `f_o = 1 kHz` using `C = 10 nF` in both arms. Give the R value, and the feedback resistor pair that gives the start-up margin.
**Answer:** `R = 1/(2π·f_o·C) = 1/(2π×10³×10⁻⁸) = 1/(6.283×10⁻⁵) = 15.9 kΩ` (nearest practical value 16 kΩ or 15 kΩ + trim). Gain: `1 + Rf/R1` must exceed 3 for start-up, so choose `Rf/R1` slightly above 2 — e.g. `R1 = 10 kΩ`, `Rf = 22 kΩ` gives `A = 3.2`, `Aβ = 1.067 > 1`. The amplitude limiter then brings the effective gain to 3.
**Method:** Invert Wien's frequency formula for the unknown (`R = 1/(2πfC)`), then design the gain arm last. Design for `A` a little *above* 3, never exactly 3 — exactly 3 is the marginal, noise-starved case. Source: `25-Oscillators.md` §25.3.

### Q32. (GATE-level) A phase-shift oscillator runs at 650 Hz with `R = 10 kΩ`, `C = 10 nF`. Someone replaces the capacitors with 22 nF parts. What is the new frequency, and what must the gain arm now supply?
**Answer:** `RC = 10k × 22n = 2.2×10⁻⁴ s`; `f_o = 1/(2π×2.2×10⁻⁴×2.449) = 1/3.386×10⁻³ = 295 Hz`. The gain requirement is **unchanged at 29** — the `√6` and the 29 come from the *network topology*, not from the component values.
**Method:** Frequency scales as `1/RC`: 22/10 = 2.2× larger C ⇒ `650/2.2 = 295 Hz`. The gain is a property of the three-section ladder's attenuation at its own phase-null frequency, which is dimensionless and value-independent. Source: `25-Oscillators.md` §25.3.

### Q33. (GATE-level) A relaxation oscillator is specified as "20 kHz, square and triangle outputs". With `R1 = R2 = 10 kΩ`, find `C` for `R = 20 kΩ`. Then state the triangle's peak amplitude for `V_sat = ±5 V`.
**Answer:** `f = V_sat/(4·V_th·R·C)` is the triangle-generator form, but for the plain square-wave relaxation generator use `T = 2RC·ln 3`. Set `f = 20 kHz` → `T = 50 µs`; `50×10⁻⁶ = 2·R·C·1.0986` → `R·C = 50e-6/2.1972 = 22.76 µs` → `C = 22.76 µs/20 kΩ = 1.14 nF` (practical: 1.2 nF with a trim). Triangle peak = `V_th = 5 × 10/20 = 2.5 V`, so 5 Vpp.
**Method:** Step 1 `T = 1/f`. Step 2 divide by `2 ln 3 = 2.1972` to get `RC`. Step 3 divide by `R` for `C`. Step 4 the triangle amplitude is set by the Schmitt threshold, not by the rails — 2.5 V peak, 5 Vpp. Source: `25-Oscillators.md` §25.5.

### Q34. (GATE-level) A relaxation oscillator uses a Schmitt divider with `R1 = 47 kΩ`, `R2 = 10 kΩ` and `R = 4.7 kΩ`, `C = 4.7 nF`. Find `f_o` and the thresholds for `V_sat = ±9 V`.
**Answer:** `1 + 2R1/R2 = 1 + 9.4 = 10.4`; `ln 10.4 = 2.342`; `2RC = 2×4.7e3×4.7e-9 = 44.18 µs`; `T = 44.18×10⁻⁶×2.342 = 103.5 µs`; `f_o = 9.66 kHz`. Thresholds `= ±9 × 47/57 = ±7.42 V`; hysteresis = 14.8 V.
**Method:** Compute the `ln` argument first (`1 + 2R1/R2` — note it is 2R1/R2, not R1/R2), then `ln`, then multiply by `2RC`. A wide divider ratio gives a *large* threshold (deep hysteresis, noise-proof) and a *slower* oscillation. Source: `25-Oscillators.md` §25.5.

### Q35. (GATE-level) A Colpitts oscillator has `L = 100 µH`, `C1 = 0.1 µF`, `C2 = 0.1 µF`. Find `f_o`. Then the designer replaces the pair with a single `50 nF` capacitor and keeps the same coil. Compare the two frequencies.
**Answer:** `C_eff = 0.1×0.1/0.2 = 0.05 µF = 50 nF`; `L·C = 10⁻⁴ × 5×10⁻⁸ = 5×10⁻¹²`; `√(LC) = 2.236×10⁻⁶`; `f_o = 1/(2π×2.236×10⁻⁶) = 71.2 kHz`. A single 50 nF gives the *identical* frequency — the tapped pair is only a way of obtaining 50 nF while also providing the feedback tap. A single 100 nF would give `f = 1/(2π√(10⁻⁴·10⁻⁷)) = 50.3 kHz`, i.e. `1/√2` lower.
**Method:** The Colpitts divider exists for the *feedback tap*, not to change the frequency. Question to ask: "what is the number the frequency formula needs?" — a series-combined capacitance. Source: `25-Oscillators.md` §25.4.

### Q36. (GATE-level) A student claims: "In a phase-shift oscillator the required amplifier gain is 29 *because* the RC sections are unloaded, so the answer is 8 for the same circuit." Is this claim right, and which number belongs to which circuit?
**Answer:** It is a *mislabel*, not a physics error. The unbuffered 3-section ladder (sections load each other) gives `f_o = 1/(2πRC√6)` with gain **29**. The buffered ladder (each section isolated by an amplifier) gives `f_o = 1/(2πRC√3)` with gain **8**. Both are correct for their own circuit; the √6 and the 29 are both consequences of the *loading*. Quote "29" whenever a diagram shows a plain resistive 3-section ladder with no buffers.
**Method:** When a frequency/gain pair is quoted, always name the circuit that produced it. GATE never gives an unlabelled number. The reliable self-check: gain 29 ↔ √6 ↔ no buffers; gain 8 ↔ √3 ↔ buffers. Source: `25-Oscillators.md` §25.3, and Q26 of this file.

---

## Trap box (exam-day killers)

- **29 vs 3.** Phase-shift needs gain 29; Wien needs 3. They are the two numbers most often swapped under exam pressure.
- **Series vs parallel combination.** Colpitts = caps in *series* (`C1C2/(C1+C2)`); Hartley = inductors in *series* (`L1+L2`). Getting this backwards shifts `f_o` by `√2` (equal components) or more.
- **Drop the √6 and your phase-shift answer is 2.45× too high.** Every other RC oscillator formula is plain `1/(2πRC)`.
- **Barkhausen needs both conditions.** `|Aβ| = 1` *and* `∠Aβ = 0°`, at the same frequency. `Aβ = −1` is stable negative feedback, not oscillation.
- **"Must equal 1 to start" is false.** Start-up needs `> 1`; the limiter brings the *effective* gain to 1. Exam statements are usually worded to catch this.
- **Relaxation is square + triangle, never sine.** Conversely, phase-shift/Wien/Colpitts/Hartley all produce a clean **sine** — do not credit "square" for them.
- **Relaxation frequency is rail-independent** but the thresholds are not; they scale with `V_sat`. R only, C only, divider ratio only.

## Final recall drill (do in 60 seconds)

1. Barkhausen's two conditions? → *`|Aβ| = 1` and `∠Aβ = 0°`.*
2. Phase-shift `f_o` and minimum gain? → *`1/(2πRC√6)`, gain 29.*
3. Wien `f_o` and gain? → *`1/(2πRC)`, gain 3 (`1 + Rf/R1 = 3` ⇒ `Rf = 2R1`).*
4. Colpitts effective capacitance? → *`C1C2/(C1+C2)` (series).*
5. Hartley effective inductance? → *`L1 + L2` (series).*
6. Relaxation period and thresholds? → *`T = 2RC·ln(1 + 2R1/R2)`, `±V_sat·R1/(R1+R2)`.*
7. Relaxation output waveform? → *square (Schmitt) + triangle (integrator).*
8. Best frequency stability and why? → *crystal, `Q = 10⁴–10⁵` ⇒ `BW = f₀/Q` is tiny.*
9. Start-up loop gain? → *`> 1`; sustained `= 1`.*
10. Buffered phase-shift gain and `f_o`? → *gain 8, `f_o = 1/(2πRC√3)`.*
