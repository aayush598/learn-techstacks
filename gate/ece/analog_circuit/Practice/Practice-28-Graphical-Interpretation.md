# Graphical Interpretation — Practice (Learn by Solving)

> **The idea in one line:** a transistor is a **curve**, not a formula — so you
> draw the right straight line (DC load line, AC load line), put the Q-point
> where you want the swing to fit, and then *read off* gain, swing, clipping,
> power and efficiency by measuring distances on the picture.
>
> **How to use:** every question below is a *drawing* question. Get paper and
> actually draw the line and mark the Q before computing anything with the
> formulas — the formulas are the arithmetic you do *after* the picture
> confirms itself. Open `28-Graphical-Interpretation.md` or
> `32-Single-File-Cheatsheet.md` only when you want the underlying theory.

## Concept box (what you must internalise)

- **DC load line:** input signal set to zero, `R_L` disconnected. It runs from
  the **cutoff intercept** `(V_CE = V_CC, I_C = 0)` to the **saturation
  intercept** `(V_CE = 0, I_C = V_CC/R_C)`, with **slope `−1/R_C`**. Only the
  DC line uses `R_C`.
- **AC load line:** `V_CC → AC ground`, `R_L` connected. Slope **`−1/R_AC`**
  with **`R_AC = R_C ∥ R_L`** (for a transformer-coupled or current-source
  load, `R_AC → ∞` and the AC line is *horizontal*). It is drawn **through
  the Q-point**, because the signal is a *deviation* from the Q-point.
- **Safe operating region:** the transistor must stay inside the DC line **and**
  the AC line. Both pass through Q. Never draw the signal moving along a single
  "combined" line.
- **The diagonal line of slope `−1/R_DC`** (through Q, `R_DC = V_CC/I_CQ`) is
  a valid construction **only when `R_AC = R_DC`**. Outside that condition use
  the two-line method.
- **Max symmetric swing:** `V_peak = min(V_CEQ − V_CE(sat), I_CQ·R_AC)`,
  `V_pp = 2·V_peak`. The simplified form
  `V_pp = 2·min(V_CEQ − V_CE(sat), V_CC − V_CEQ)` is exact **only when
  `R_AC = R_C`** (no external load), because only then
  `I_CQ·R_AC = V_CC − V_CEQ`.
- **Slope of the transistor curve at Q is the transconductance:**
  `dI_C/dV_BE = gm = I_C/V_T`, so the "resistance" of the curve is
  `1/gm = re`. The gain is the *product* of the horizontal excursion and this
  slope: `|A_v| = gm·R_AC`.
- **Where the Q-point sits decides which peak clips:** too **high**
  (`V_CEQ` large, `I_CQ` small) → the **positive output peak** flattens
  (cutoff); too **low** → the **negative** peak flattens (saturation).

**Reference circuit used throughout:** CE stage, `V_CC = 12 V`,
`R_C = 2 kΩ`, `V_CE(sat) = 0.2 V`, `β = 100`, `V_T = 25 mV`. Q-point:
`I_CQ = 3 mA`, `V_CEQ = 6 V`. With an external load `R_L = 2 kΩ`:
`R_AC = 1 kΩ`.

---

## Questions

### Q1. (Easy) Draw the DC load line for `V_CC = 12 V`, `R_C = 2 kΩ`. Give both intercepts and the slope.
**Answer:** Cutoff intercept `(V_CE, I_C) = (12 V, 0)`; saturation intercept `(0, 12/2k) = (0, 6 mA)`. Slope `= ΔI_C/ΔV_CE = −1/R_C = −0.5 mA/V`.
**Method:** Two intercepts, then join them — and the slope is a free consistency check (`−1/R_C`). Everything else about the DC line follows. Source: `28-Graphical-Interpretation.md` §28.1.

### Q2. (Easy) What is the Q-point of the reference circuit, and is it on the mid-line?
**Answer:** `I_CQ = 3 mA` → `V_CEQ = 12 − 3m×2k = 6 V`. Mid-line means `V_CEQ = V_CC/2 = 6 V` ✓ and `I_CQ = I_C,sat/2 = 3 mA` ✓ — this Q-point is exactly centred.
**Method:** "Centred" is the design goal for maximum *symmetric* swing, and `V_CEQ = V_CC/2` is the graphical form of it. Always check centring numerically, not by eye. Source: `28-Graphical-Interpretation.md` §28.2.

### Q3. (Easy) What is the largest `V_peak` at the Q-point of Q2 with no external load, and what is `V_pp`?
**Answer:** `V_peak = min(V_CEQ − V_CE(sat), V_CC − V_CEQ) = min(6 − 0.2, 12 − 6) = min(5.8, 6) = 5.8 V`; `V_pp = 11.6 V`.
**Method:** The two numbers are the two *distances* from Q to the two ends of the DC line: down to saturation is `V_CEQ − 0.2 = 5.8 V`, up to cutoff is `V_CC − V_CEQ = 6 V`. The swing is limited by the *smaller* distance, and by `0.2 V`, not `0`. Source: `28-Graphical-Interpretation.md` §28.2.

### Q4. (Easy) Why do we use `V_CE(sat) ≈ 0.2 V` instead of `0 V` in the swing calculation?
**Answer:** Because the saturation **knee** is at ≈`0.2 V` for a silicon BJT; a real BJT does not reach `V_CE = 0`. Using `0` overstates the swing by 0.2 V at one end and is the reason textbook answers differ by that amount.
**Method:** `V_CE(sat)` is a *device parameter*, like `V_BE` or `V_th` — know it (`0.2 V` BJT, `0`–`0.5 V` MOS) and never treat the transistor as an ideal switch in the swing budget. Source: `26-Transistor-as-Switch.md`, `28-Graphical-Interpretation.md` §28.2.

### Q5. (Easy) The slope of the output characteristic at `I_CQ = 3 mA` is what, and what is its reciprocal?
**Answer:** `dI_C/dV_BE = gm = I_C/V_T = 3m/25m = 0.12 S = 120 mA/V`. Its reciprocal is `1/gm = 8.33 Ω` — which is exactly `re = V_T/I_C = 25m/3m = 8.33 Ω`.
**Method:** The transistor's "internal resistance" on the B-E input is the reciprocal of the curve's slope, and it is *exactly* `re`. This is the graphical origin of `re`, not an independent formula. Source: `08-BJT-Small-Signal-Models.md`, `28-Graphical-Interpretation.md` §28.3.

### Q6. (Easy) Give the AC load line for the reference circuit loaded with `R_L = 2 kΩ`: its slope and the two points at `i_c = ±1 mA`.
**Answer:** `R_AC = 2k∥2k = 1 kΩ`; slope `= −1/R_AC = −1 mA/V`. Through Q `(3 mA, 6 V)`: at `i_c = +1 mA`, `I_C = 4 mA`, `V_CE = 6 − 1m×1k = 5 V`; at `i_c = −1 mA`, `I_C = 2 mA`, `V_CE = 7 V`. Check the slope: `(2−4)/(7−5) = −1 mA/V` ✓.
**Method:** Build the AC line by moving *along* it from Q: a change of current `Δi_c` costs `Δv_ce = Δi_c·R_AC` of voltage. Two symmetric moves plus the slope check make the line impossible to get wrong. Source: `28-Graphical-Interpretation.md` §28.2.

### Q7. (Easy) With the AC load line of Q6, what is the largest sinusoidal `i_c` peak, and which limit binds?
**Answer:** `V_peak = min(V_CEQ − 0.2, I_CQ·R_AC) = min(5.8, 3m×1k = 3) = 3 V`, so `i_c,peak = 3 V/1 kΩ = 3 mA`. The binding limit is the **cutoff** side (`I_CQ·R_AC = 3 V`), not saturation.
**Method:** Adding a load *steepens* the AC line, so the current axis becomes the tight constraint long before the voltage axis does. This is the central practical consequence of loading a stage: the Q-point that was perfectly centred on the DC line is now badly off-centre on the AC line. Source: `28-Graphical-Interpretation.md` §28.2.

### Q8. (Easy) What does the output at the collector of a CE stage look like for a small sinusoidal input, and why?
**Answer:** A **sinusoid, inverted** (180° out of phase with the input). An increase in `v_BE` raises `i_C`, which raises the drop across `R_C`, which *lowers* `v_CE = V_CC − i_C R_C`.
**Method:** The sign is read straight off the load line: moving **up-left** along it (more current) is more output voltage *dropped* across `R_C`, so the collector voltage moves **down**. Source: `09-BJT-Amplifiers.md`, `28-Graphical-Interpretation.md` §28.4.

### Q9. (Easy) Why must the AC load line be drawn *through* the Q-point?
**Answer:** Because the AC line is the locus of `(V_CEQ + v_ce, I_CQ + i_c)`, the **deviation** from the Q-point. Q is by definition the point of zero deviation, so it lies on the line; the line's *slope* is fixed by `R_AC` and its *position* is fixed by Q. Two things, two pieces of information — that is the whole content of the AC line.
**Method:** DC line = slope from `R_C`, position from `V_CC`. AC line = slope from `R_AC`, position from **Q**. Source: `28-Graphical-Interpretation.md` §28.2.

### Q10. (Easy) List the two things a good Q-point must satisfy, and what fails if each is ignored.
**Answer:** (1) **Active region with margin** — `V_CEQ` well above `V_CE(sat)` and well below `V_CC`; ignore it and the device is in saturation/cutoff, where the small-signal model and `gm` are meaningless. (2) **Centred on the load line that matters** (the AC line if a load is present); ignore it and one peak clips long before the other.
**Method:** Q-point questions are always "which of these two constraints is binding?" — compute *both* distances from Q to the ends of the relevant line and compare. Source: `28-Graphical-Interpretation.md` §28.2.

### Q11. (Easy) At `f_H` (the −3 dB point) of a single-pole amplifier, what are the magnitude and the phase?
**Answer:** Magnitude `= 1/√2` of midband (`−3 dB`); phase `= −45°`. Two poles put the magnitude at `1/2` (`−6 dB`) and the phase at `−90°` at the geometric-mean corner.
**Method:** The Bode line is a straight approximation (`−20 dB/dec`, `−45°/pole`); the exact values at the corner are the standard exam checkpoints. Source: `16-Frequency-Response.md`, `28-Graphical-Interpretation.md` §28.5.

### Q12. (Moderate) The reference circuit is driven with `i_c` of 1 mA peak. Find `v_ce,peak` and the output voltage peak, and state the sign of each.
**Answer:** `v_ce,peak = i_c,peak·R_AC = 1m×1k = 1 V`; `v_o = −v_ce` (CE inverts), so `v_o,peak = 1 V`, occurring when `v_ce` is at its *minimum*. `V_CE` therefore swings between 5 V and 7 V.
**Method:** The two signs are independent and both matter: `v_ce` is *reduced* by a positive `i_c` (`v_ce = −i_c R_AC`), and the *output* is the negative of `v_ce`. Source: `09-BJT-Amplifiers.md`, `28-Graphical-Interpretation.md` §28.4.

### Q13. (Moderate) Construct the gain graphically: for a displacement of `i_c = 0.5 mA`, what `v_BE` is needed, and what is `A_v`?
**Answer:** Along the AC line, `Δi_c = 0.5 mA` corresponds to `Δv_ce = 0.5m×1k = 0.5 V`. The characteristic's slope at Q is `gm = 120 mA/V`, so `v_BE = 0.5m/0.12 = 4.17 mV`. `A_v = −0.5/4.17m = −120`.
**Method:** The graphical gain construction is exactly `|A_v| = Δv_ce/Δv_BE = R_AC·(Δi_c/Δv_BE) = R_AC·gm`. Measure the *vertical* displacement along the load line and the *horizontal* displacement along the characteristic, and divide. The method formula `A_v = −gm(R_C∥R_L)` is this measurement done algebraically. Source: `28-Graphical-Interpretation.md` §28.3.

### Q14. (Moderate) An emitter follower has a load-line slope of `−1/5 Ω` at its Q-point. What is `re` there, and what is `I_E`?
**Answer:** The emitter characteristic's slope is `dI_E/dV_BE = 1/re`, so `re = 5 Ω`; `I_E = V_T/re = 25m/5 = 5 mA`.
**Method:** The slope of the *emitter* characteristic is the reciprocal of `re` — remember which current each characteristic carries (`I_C` for the collector set, `I_E` for the emitter set) and the slope is `1/re` either way. Source: `08-BJT-Small-Signal-Models.md`.

### Q15. (Moderate) Compute the output power, DC input power and efficiency at the maximum swing of Q7.
**Answer:** `V_peak = 3 V` into `R_AC = 1 kΩ` → `P_out = V_peak²/(2R_AC) = 9/2000 = 4.5 mW`. `P_dc = V_CC·I_CQ = 12 × 3m = 36 mW`. `η = 4.5/36 = 12.5%`.
**Method:** For a sine, `P = V_peak²/(2R) = V_pp²/(8R)` — the factor of 2 from averaging `sin²`, and it is the single most common power error. `P_dc` is the supply power `V_CC·I_CQ`. Note 12.5% is *half* of the 25% ceiling (Q26) because the Q-point is no longer centred on the AC line. Source: `28-Graphical-Interpretation.md` §28.7.

### Q16. (Moderate) When is the "diagonal load line" of slope `−1/R_DC` through Q a legitimate construction? Give its numbers for the reference circuit.
**Answer:** It is legitimate **only when `R_AC = R_DC`**, i.e. a transformer-coupled collector or a current-source load, where the AC line is horizontal. Here `R_DC = V_CC/I_CQ = 12/3m = 4 kΩ`; the diagonal has slope `−0.25 mA/V` and joins `(V_CC = 12, 0)` to `(0, 3 mA)`, passing through Q `(3 mA, 6 V)` ✓. With `R_L = 2 kΩ` we instead have `R_AC = 1 kΩ ≠ 4 kΩ`, so the two-line (DC **and** AC) method is the correct one.
**Method:** The diagonal line is a *shortcut for the horizontal-AC-line case*. It is often quoted without its condition, and using it with a finite `R_L` is a real GATE trap. Always state which case you are in. Source: `28-Graphical-Interpretation.md` §28.2.

### Q17. (Moderate) The bias is misadjusted to `V_CEQ = 8 V` (`I_CQ = 2 mA`) with `R_L = 2 kΩ`. Which output peak clips first, and at what output level?
**Answer:** `R_AC = 1 kΩ`; cutoff side `I_CQ·R_AC = 2 V`; saturation side `V_CEQ − 0.2 = 7.8 V`. So the **positive output peak** clips, at `v_o,peak = 2 V`; the negative peak could reach 7.8 V.
**Method:** `I_CQ` too small ⇒ the transistor runs out of **current** before it runs out of **voltage**. Because the CE output inverts, running out of current shows up as a flattened **positive** output peak (flat top). Diagnose a clipped waveform by *which side* is flat. Source: `28-Graphical-Interpretation.md` §28.4.

### Q18. (Moderate) The opposite misadjustment: `V_CEQ = 4 V` (`I_CQ = 4 mA`), same `R_L`. Which peak clips, and at what level?
**Answer:** Cutoff side `4m×1k = 4 V`; saturation side `4 − 0.2 = 3.8 V`. The **negative output peak** clips, at `3.8 V`.
**Method:** Mirror image of Q17: `I_CQ` too large ⇒ the transistor hits **saturation** first, which is a flat **negative** output peak (flat bottom). Fix either case by re-centring the Q-point on the *AC* line (Q25). Source: `28-Graphical-Interpretation.md` §28.4.

### Q19. (Moderate) A diode detector rectifies a 5 V-peak 1 kHz sine through a `0.7 V` diode into `R = 10 kΩ`, `C = 1 µF`. Find the DC output, the ripple and the ripple percentage.
**Answer:** `V_out ≈ 5 − 0.7 = 4.3 V`. `f_c = 1/(2πRC) = 1/(2π×10k×1µ) = 15.9 Hz ≪ 1 kHz` ✓. Ripple `ΔV = I_load/(fC) = (4.3/10k)/(1k×1µ) = 0.43 mA/1 mC = 0.43 V`, i.e. **10%**.
**Method:** Two separate checks. (i) Smoothing: `f_c` must be ≪ the signal frequency. (ii) Ripple: the capacitor supplies the load current for the whole cycle, so `ΔV = I/(fC) = V_out/(fRC)`, and the ripple *percentage* is simply `1/(fRC)`. Here `fRC = 10`, hence 10%. Source: `05-Rectifiers.md`.

### Q20. (Moderate) The same detector is used at 100 Hz. Does the 10% ripple figure hold? Give the ripple percentage and the cutoff frequency.
**Answer:** Ripple % `= 1/(fRC) = 1/(100 × 10k × 1µ) = 1/1 = 100%` — the output is a full sawtooth, useless. `f_c = 15.9 Hz` is now only 6× below the signal, which is nowhere near "≪".
**Method:** Ripple % is set by the single number `fRC`, not by the components separately. Rule of thumb: keep `fRC ≥ 20` for 5% ripple. This is why envelope detectors are useless at audio frequencies and demodulators always add a few stages of RC filtering. Source: `05-Rectifiers.md`.

### Q21. (Moderate) Give the `rπ` and the input resistance seen at the base for the reference circuit.
**Answer:** `gm = 0.12 S`; `rπ = β/gm = 100/0.12 = 833 Ω`; the base also sees the bias network in parallel, so with `R_b = 20 kΩ`, `R_in = 20k∥833 = 801 Ω`.
**Method:** `rπ` is the reciprocal of the *base* characteristic's slope, not the output characteristic's: `dI_B/dV_BE = gm/β` ⇒ `rπ = β/gm`. Mixing up the two characteristic families is the standard graphical-analysis error. Source: `08-BJT-Small-Signal-Models.md`.

### Q22. (Moderate) Why is the gain of a CE stage *not* maximum at the extremes of the load line?
**Answer:** At the extremes the transistor leaves the active region: near cutoff `I_C → 0` so `gm = I_C/V_T → 0` (gain collapses); near saturation the output characteristic bends over (the Early effect and the knee) so the incremental `gm` no longer matches `I_C/V_T` and the linearity fails. The gain and the linearity are both best near the middle of the active region.
**Method:** `gm` is a *Q-point* quantity, so the gain you have is the gain *at the Q-point* only. Asking "what is the gain at cutoff?" is meaningless, and GATE uses that to separate students who memorised `A_v = −gm R_C` from those who understand it. Source: `08-BJT-Small-Signal-Models.md`, `28-Graphical-Interpretation.md` §28.3.

### Q23. (Moderate) Two CE stages in cascade, both with the Q-point of Q2. What is the total phase shift from the first base to the last collector, and is the overall gain positive or negative?
**Answer:** Each CE inverts by 180°; two give 360°, i.e. **in phase**, and the overall gain is **positive**: `(+)(+)(−)(−) = +`. With `R_AC = 1 kΩ` each, `A_total = (−120)(−120) = +14,400`.
**Method:** Phase adds arithmetically, sign multiplies. Count inversions, not stages: CE, CB, CG invert or not as a fixed property of the topology (only CE/CS invert among the four classic configurations). Source: `09-BJT-Amplifiers.md`, `28-Graphical-Interpretation.md` §28.4.

### Q24. (Moderate) Sketch the output waveform if a CE stage (Q-point of Q2, no external load) is driven with a 7 V-peak input sine, and say what appears in its spectrum that a sine does not have.
**Answer:** The stage's gain is `−gm·R_C = −0.12×2000 = −240`, so a 7 V-peak input *demands* `7 × 240 = 1680 V` at the collector — 290× more than the 5.8 V available. The output is therefore a hard-clipped, nearly square wave, flat at `+5.8 V` and `−5.8 V` (the two distances from Q on the DC line). Even a mildly overdriven stage's flat tops generate **harmonics** — and if only one peak clips (Q17/Q18) the waveform loses half-wave symmetry, so **even-order harmonics and a DC component** appear.
**Method:** Clipping is a *nonlinear* operation, and nonlinearities generate harmonics; symmetry determines *which* harmonics. Symmetric clipping → odd harmonics only. Asymmetric clipping (one peak only) → even harmonics plus a DC shift. This is the bridge from "graphical waveform" to "distortion". Source: `28-Graphical-Interpretation.md` §28.4, §28.6.

### Q25. (Moderate) Redesign the bias of the reference circuit (`R_C = 2 kΩ`, `V_CC = 12 V`, `V_CE(sat) = 0.2 V`, `R_L = 2 kΩ`) so the **AC** line is centred. Find `I_CQ`, `V_CEQ` and `V_peak`.
**Answer:** Centre the AC line: `I_CQ·R_AC = V_CEQ − 0.2` with `V_CEQ = 12 − 2k·I_CQ` and `R_AC = 1 kΩ` ⇒ `1k·I_CQ = 11.8 − 2k·I_CQ` ⇒ `3k·I_CQ = 11.8` ⇒ **`I_CQ = 3.93 mA`**, `V_CEQ = 4.13 V`, `V_peak = 3.93 V`, `V_pp = 7.87 V`.
**Method:** Centring is a *two-equation* condition (one for each direction), not "set `V_CEQ = V_CC/2`" — that is only correct when `R_AC = R_C`. Notice the centred design gives a *smaller* `V_pp` (7.87 V) than the naive `V_CC/2` choice (which is asymmetric and clips at 3 V per side anyway). Source: `28-Graphical-Interpretation.md` §28.2.

### Q26. (GATE-level) A CE stage has `V_CC = 12 V` and `R_C = 2 kΩ` with no external load. Show that the maximum possible efficiency is 25%, and state the Q-point that achieves it.
**Answer:** Max swing needs `V_CEQ − 0.2 = V_CC − V_CEQ` ⇒ `V_CEQ = 6.1 V`, `I_CQ = (12−6.1)/2k = 2.95 mA` (≈3 mA, the mid-line). `V_peak = 5.9 V`; `P_out = 5.9²/(2×2k) = 8.70 mW`; `P_dc = V_CC·I_CQ = 12 × 2.95m = 35.4 mW`; `η = 8.70/35.4 = 24.6%`. In the idealisation `V_CE(sat) → 0`: `V_CEQ = 6 V`, `I_CQ = 3 mA`, `P_out = 6²/4000 = 9 mW`, `P_dc = 36 mW`, so **`η_max = (V_CC²/8R_C) ÷ (V_CC²/2R_C) = 25%`**.
**Method:** The 25% ceiling is the price of class A with a resistive load: at best the transistor passes current for the whole cycle while the *voltage* across it swings the whole range, and the two waveforms are 180° out of phase, so the average product is half the peak product. The `V_CE(sat) = 0.2 V` correction always pushes you slightly *below* the ceiling. Getting above 25% requires class B or C, or an inductive/transformer load. Source: `28-Graphical-Interpretation.md` §28.7.

### Q27. (GATE-level) For the Q-point of Q2, split the 36 mW drawn from the `V_CC` supply between `R_C` and the transistor, and check the balance.
**Answer:** `P_RC = I_CQ²·R_C = (3m)²×2k = 18.0 mW`. In the transistor: `P = V_CEQ·I_CQ + V_BE·I_B = 6×3m + 0.7×30µ = 18.0 mW + 0.021 mW = 18.02 mW`. Total `= 18.0 + 18.02 = 36.02 mW ≈ V_CC·I_CQ = 36 mW` ✓ (the 0.02 mW is rounding).
**Method:** Power in the transistor is **the sum of both junctions** (`V_CEQ I_CQ` for the collector junction + `V_BE I_B` for the base junction) — a base-driven amplifier dissipates slightly *more* than `V_CC I_CQ` because the base supply adds power. If your two halves do not add up to the supply power, you have dropped a term. Source: `06-BJT-Fundamentals.md`, `28-Graphical-Interpretation.md` §28.7.

### Q28. (GATE-level) How much power does the *base* supply contribute in Q27, and why is the base usually treated as a voltage source?
**Answer:** `V_B = V_E + 0.7 = 0.7 V` here (the Q-point sits at `V_CE = 6 V` with no `R_E`); `I_B = 30 µA`; `P_base = 0.7 × 30µ = 21 µW`, against `36 mW` from the collector supply — a ratio of 1:1700.
**Method:** `P_base/P_total ≈ 1/β`. Because it is negligible, the base can be modelled as a stiff voltage source and the base current ignored in power budgets. The same approximation *fails* for the **DC bias point** if `R_b` is small (see `Practice-27`, Q9) — power small, `rπ` effect large. Source: `06-BJT-Fundamentals.md`, `28-Graphical-Interpretation.md` §28.7.

### Q29. (GATE-level) For the loaded reference circuit (Q7, `R_AC = 1 kΩ`), what input peak voltage produces the maximum undistorted output?
**Answer:** `v_BE,peak = V_peak,out/gm = 3/0.12 = 25 mV`.
**Method:** The ratio `V_peak,out/v_BE,peak = gm·R_AC = 120` is the gain; the *input* range of a CE stage is only of the order of tens of millivolts. Anything larger and you are no longer doing small-signal analysis — you are doing the clipping analysis of Q24. This number (`≤ 25 mV` typically) is the practical difference between a linear amplifier and a switch. Source: `28-Graphical-Interpretation.md` §28.4.

### Q30. (GATE-level) A sinusoidal input is applied to a biased CE stage. Sketch `v_BE` and `i_C` for a small input, and state the phase relationship.
**Answer:** `v_BE = v_sig` and `i_C = gm·v_BE` are **in phase** (the exponential is a power law: increasing `v_BE` increases `i_C`). The phase inversion appears only at the *collector*, because `v_ce = −i_C R_AC`.
**Method:** Three nodes, three phases: base and collector current in phase; collector voltage inverted. The inversion is a *circuit* effect (the `R_C` drop), not a device effect — the transistor never inverts anything. Source: `09-BJT-Amplifiers.md`, `28-Graphical-Interpretation.md` §28.4.

---

### Q31. (GATE-level) `V_CC = 12 V`, `R_C = 2 kΩ`, `V_CE(sat) = 0.2 V`, `R_L = 2 kΩ`. Find the maximum output power, the DC supply power and the efficiency, and explain why the answer differs from the 25% ceiling.
**Answer:** `R_AC = 1 kΩ`. `V_peak = min(6 − 0.2, 3m×1k) = 3 V` (cutoff side binds). `P_out = 3²/(2×1k) = 4.5 mW`. `P_dc = 12×3m = 36 mW`. `η = 12.5%`.
**Method:** Half the ceiling, for two independent reasons: (i) the external load steepens the AC line so the current axis binds long before the voltage axis, wasting 2.8 V of the 5.8 V available; (ii) the Q-point was centred on the **DC** line, not the **AC** line. Re-centre (Q25) and `η` rises to 16.4% — still short of 25% because the load steals voltage swing too. Efficiency is a *Q-point* result, never a device constant. Source: `28-Graphical-Interpretation.md` §28.7.

### Q32. (GATE-level) In Q31, re-centre the Q-point on the AC line and recompute `P_out`, `P_dc` and `η`.
**Answer:** From Q25, `I_CQ = 3.93 mA`, `V_CEQ = 4.13 V`, `V_peak = 3.93 V`. `P_out = 3.93²/(2×1k) = 7.73 mW`; `P_dc = 12×3.93m = 47.2 mW`; `η = 16.4%`.
**Method:** Compare with Q31: `P_out` rises 72% (3 → 3.93 V peak) but `P_dc` also rises 31%, so `η` improves only from 12.5% to 16.4%. The trade is unavoidable — the transistor now dissipates more on average, because a higher standing current is what buys the larger swing. Source: `28-Graphical-Interpretation.md` §28.7.

### Q33. (GATE-level) A CE stage is measured and its output shows a flattened **positive** peak. Give (a) which limit is hit, (b) the direction of the bias error, (c) the numerical test, and (d) the fix.
**Answer:** (a) **Cutoff** — the positive output peak corresponds to the *minimum* `V_CE`, i.e. the maximum current demand. (b) `I_CQ` is too **small** (`V_CEQ` too high). (c) Compare `I_CQ·R_AC` with `V_CEQ − V_CE(sat)`: here `2 V < 7.8 V`, so the current axis is the binding one. (d) Reduce `V_CEQ` (raise `I_CQ`) until the two are equal — Q25's condition `I_CQ·R_AC = V_CEQ − V_CE(sat)`.
**Method:** A clipped waveform is a Q-point diagnosis. Flat **top** ⇒ cutoff ⇒ too little current. Flat **bottom** ⇒ saturation ⇒ too much current. Then confirm numerically before changing anything. Source: `28-Graphical-Interpretation.md` §28.4.

### Q34. (GATE-level) The same stage is measured and its output shows a flattened **negative** peak. Repeat the diagnosis, and explain what happens to the average output level.
**Answer:** (a) **Saturation**; (b) `I_CQ` too **large** (`V_CEQ` too low) — here `3.8 V < 4 V`, saturation binds. (c) Reduce `I_CQ` until `I_CQ·R_AC = V_CEQ − 0.2`. (d) The average collector voltage **drops** below `V_CEQ` when the negative peaks are the ones flattened, because the waveform is truncated where it spends the least time. Asymmetric clipping therefore also shifts the DC output level — a real "rectifier-like" behaviour, and a useful diagnostic.
**Method:** Asymmetric clipping shifts the mean; symmetric clipping does not. If the measured DC output level has moved, the clipping is asymmetric — and that immediately tells you which peak is flat. Source: `28-Graphical-Interpretation.md` §28.4, §28.6.

### Q35. (GATE-level) Design a CE stage for maximum output power into `R_L = 10 kΩ` with `R_C = 1 kΩ`, `V_CC = 12 V`, `V_CE(sat) = 0.2 V`. Find `I_CQ`, `V_CEQ`, `V_peak`, `P_out` and `η`.
**Answer:** `R_AC = 1k∥10k = 909 Ω`. Centre: `I_CQ·909 = 12 − 1k·I_CQ − 0.2` ⇒ `1909·I_CQ = 11.8` ⇒ **`I_CQ = 6.18 mA`**, `V_CEQ = 5.82 V`, `V_peak = 5.62 V`. `P_out = 5.62²/(2×909) = 17.4 mW`; `P_dc = 12×6.18m = 74.2 mW`; `η = 23.4%`.
**Method:** A light load (`R_L ≫ R_C`) makes `R_AC ≈ R_C`, so the AC line is close to the DC line and the efficiency approaches the 25% ceiling (23.4% here). A heavy load (`R_L < R_C`, Q31) collapses it. The `R_AC = R_C∥R_L` in the centring equation is the whole story. Source: `28-Graphical-Interpretation.md` §28.2, §28.7.

### Q36. (GATE-level) A CE stage has an emitter resistor that is *not* bypassed. Sketch how the AC load line changes (slope and position) and derive the new slope from first principles.
**Answer:** The unbypassed `R_E` carries `(1 + 1/β)` of the signal current, so the *incremental* resistance seen by the AC signal is `R_AC,eff = R_C∥R_L + (β+1)R_E` (referred to the collector), and the AC line's slope becomes `−1/R_AC,eff` — a much shallower line than `−1/(R_C∥R_L)`. Since the emitter current is a factor `(β+1)` larger than the collector current, the emitter's contribution is multiplied by `(β+1)`: for `R_E = 500 Ω`, β = 100, `R_C∥R_L = 1 kΩ`, the effective load is `1k + 101×500 = 51.5 kΩ` and the slope is `−0.019 mA/V` instead of `−1 mA/V` — 52× flatter. The Q-point does not move; only the line's slope does.
**Method:** Unbypassed degeneration is a **series feedback** term, and series feedback in a load line always means *rotating the line about the Q-point* to a shallower slope by a factor `(1 + gm R_E·(β+1)/…)`. The practical reading: degeneration makes the gain insensitive to `β` and to `R_C` (it becomes `−(R_AC)/R_E`), and it costs gain — the same three effects as in `Practice-27` Q7, now visible as a *picture*. Source: `28-Graphical-Interpretation.md` §28.2, `29-Formula-Sheet.md` §29.3.

---

## Trap box (exam-day killers)

- **Centring `V_CEQ = V_CC/2` is only right when `R_AC = R_C`.** With an external load you must centre the **AC** line: `I_CQ·R_AC = V_CEQ − V_CE(sat)`.
- **Slopes:** DC line `−1/R_C`; AC line `−1/(R_C∥R_L)`; both through Q. Using `R_C` for the AC line, or `R_C∥R_L` for the DC line, is the #1 load-line error.
- **`V_pp = 2·min(V_CEQ − V_CE(sat), V_CC − V_CEQ)`** is exact only for `R_AC = R_C`. The general form is `2·min(V_CEQ − V_CE(sat), I_CQ·R_AC)`.
- **Which peak clips tells you the fault:** flat top ⇒ cutoff ⇒ `I_CQ` too small; flat bottom ⇒ saturation ⇒ `I_CQ` too large. Verify with the two numbers, not by eye.
- **The diagonal `−1/R_DC` line is valid only when `R_AC = R_DC`** (transformer / current-source load). It is not a general construction.
- **Power:** `P_out = V_peak²/(2R) = V_pp²/(8R)`; `P_dc = V_CC·I_CQ`; class-A resistive ceiling **25%**. Quoting `V_pp²/R` overstates `P_out` by 8×.
- **Transistor dissipation is `V_CEQ I_CQ + V_BE I_B`** — two junctions. It must add up to the supply power.
- **Gain is a Q-point property.** `A_v = −gm R_AC` and `gm = I_C/V_T`; ask for the gain at cutoff and the answer is zero, not a formula.
- **`rπ` comes from the base characteristic, `re` from the emitter characteristic, `gm` from the slope of the output characteristic.** Mixing the families gives factors of `β` wrong.

## Final recall drill (do in 60 seconds)

1. DC load-line intercepts? → *`(V_CC, 0)` and `(0, V_CC/R_C)`.*
2. DC load-line slope? → *`−1/R_C`.*
3. `R_AC`? → *`R_C∥R_L`; AC line slope `−1/R_AC`, drawn through Q.*
4. When is the AC line horizontal? → *transformer-coupled / current-source load (`R_AC → ∞`).*
5. `V_peak` (general)? → *`min(V_CEQ − V_CE(sat), I_CQ·R_AC)`; `V_pp = 2×` that.*
6. `V_CE(sat)`? → *≈`0.2 V` (silicon BJT).*
7. Slope of the output characteristic at Q? → *`gm = I_C/V_T`; its reciprocal is `re = V_T/I_E`.*
8. `rπ`? → *`β/gm`; reciprocal of the **base** characteristic's slope.*
9. `P_out` (sine)? → *`V_peak²/(2R_AC) = V_pp²/(8R_AC)`.*
10. `P_dc` and the class-A ceiling? → *`V_CC·I_CQ`; **25%** for a resistive load.*
11. Transistor dissipation? → *`V_CEQ I_CQ + V_BE I_B`.*
12. Flat top at the output? → *cutoff, `I_CQ` too small.* Flat bottom? → *saturation, `I_CQ` too large.*
13. Diagonal `−1/R_DC` line valid when? → *`R_AC = R_DC` only.*
14. CE output phase? → *180° inverted (the `R_C` drop, not the device).*
