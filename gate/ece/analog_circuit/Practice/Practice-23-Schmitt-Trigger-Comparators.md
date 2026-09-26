# Schmitt Triggers and Comparators — Practice (Learn by Solving)

> **The idea in one line:** a comparator answers "which input is bigger?" with a
> railed output; a **Schmitt trigger** is a comparator with **positive feedback**
> and therefore **two** trip points, so noise between them cannot make it
> chatter. Every question in this file is really one formula — `V_th = V_sat·R1/R_f`
> — plus knowing *which* threshold you are standing on.
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve
> the next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `23-Schmitt-Trigger-Comparators.md` or `32-Single-File-Cheatsheet.md` only
> when you want the underlying theory.

## Concept box (what you must internalise)

- Comparator: **open loop**, no virtual short, `v_o = ±V_sat` — never anything in between.
- Non-inverting Schmitt (signal on `v+`, `v− = V_ref`, `R1` from input, `R_f` from output): `UT = V_ref + V_sat·R1/R_f`, `LT = V_ref − V_sat·R1/R_f`.
- Hysteresis (dead band) `= UT − LT = `**`2·V_sat·R1/R_f`** — *twice* the one-sided trip. **Trap:** both thresholds are **not** at `V_ref` unless `V_sat·R1/R_f = 0`.
- Which threshold applies: **rising input trips at `UT`** (output was low); **falling input trips at `LT`** (output was high). **Method:** always ask "what is the output doing *right now*?" before choosing a threshold.
- Hysteresis must exceed the noise amplitude, or the whole circuit is pointless. `Q = 0.707`-style shortcuts do not exist here — it is one ratio: `R1/R_f`.
- Positive feedback goes to **`v+`**. Send it to `v−` and you have built a linear amplifier, not a Schmitt trigger.

---

## Questions

### Q1. (Easy) A non-inverting Schmitt trigger has `V_sat = ±10 V`, `R1 = 1 kΩ` (from input), `R_f = 10 kΩ` (from output), `V_ref = 0`. Find `UT`, `LT` and the hysteresis.
**Answer:** `V_th = V_sat·R1/R_f = 10 × 1/10 = `**1 V**. `UT = +1 V`, `LT = −1 V`, hysteresis `= 1 − (−1) = `**2 V** (`= 2·10·(1/10)`).
**Method:** One ratio, `R1/R_f = 0.1`, times `V_sat = 10 V` gives the one-sided trip; double it for the band. Everything else is a sign. Write `R1/R_f` explicitly before multiplying — the fraction (not its reciprocal) decides whether the band is narrow or wide.

### Q2. (Easy) A comparator (open loop) has `v+ = +0.5 mV` and `v− = +0.2 mV`, rails `±12 V`. What is the output?
**Answer:** `v+ > v−` ⇒ `v_o = `**+12 V** (the positive rail).
**Method:** An open-loop op-amp is a comparator: it amplifies the **difference** by a factor of ~10⁶, so a 0.3 mV difference becomes thousands of volts — i.e. the rail. There is **no virtual short** in a comparator; never write `v+ = v−` here. The rule is literally: `v+ > v− ⇒ +V_sat`, `v+ < v− ⇒ −V_sat`.

### Q3. (Easy) A Schmitt trigger has `V_sat = ±9 V`, `R1 = 2 kΩ`, `R_f = 9 kΩ`, `V_ref = 0`. Find `UT`, `LT` and the hysteresis.
**Answer:** `V_th = 9 × 2/9 = `**2 V**. `UT = +2 V`, `LT = −2 V`, hysteresis `= 4 V` (`2 × 9 × 2/9`).
**Method:** `2/9 × 9 = 2` — note the `R_f` value cancels the `9` numerically; that is a coincidence of the numbers, not a rule. Then double for the band. Students who quote "3 V" here have used `V_sat` as a number somewhere in the wrong place.

### Q4. (Easy) Same circuit as Q1 but `V_ref = 2 V`. Find `UT` and `LT`.
**Answer:** `UT = 2 + 1 = `**3 V**, `LT = 2 − 1 = `**1 V`**. Hysteresis is still 2 V, but the band is **centred at 2 V** instead of 0 V.
**Method:** `V_ref` slides the whole band up or down; it does **not** change its width (`R1/R_f` alone sets the width). Sketch it as a window from 1 V to 3 V — this is a "level window detector" in one line, and it is how you answer any "detect when `v_in` is between X and Y" question.

### Q5. (Easy) Can the output of a Schmitt trigger ever sit at a value **between** the two rails? Under what circumstance?
**Answer:** **No — never.** Once the input has crossed the appropriate threshold the output snaps to a rail (in microseconds, limited only by slew rate). The output is always at `+V_sat`, `−V_sat`, or in the middle of a *transition*. A measured mid-rail value means either saturation has not yet been reached or the op-amp is oscillating.
**Method:** Positive feedback is *regenerative*: it pushes the output away from the midpoint, not towards it. Contrast with an op-amp used as a linear amplifier, where the output legitimately sits between the rails — the difference is negative vs positive feedback, not the device.

---

### Q6. (Easy) A Schmitt trigger with `V_th = 2 V` is driven by a `±1 V` sine. What does the output do?
**Answer:** **Nothing at all.** The input never reaches `±2 V`, so neither threshold is crossed and the output stays at whatever state it was in when the input was connected. Starting low, it stays at `−V_sat` forever.
**Method:** Compare `V_pk` with `V_th` *before* drawing any waveform. `V_pk < V_th` ⇒ no switching. This is the "Schmitt trigger as a noise-rejecting dead-zone / logic gate" property: the circuit is a **comparator with memory**, so it only reports "the input has definitely exceeded `V_th`". If a question asks what the output does, the answer is often "it never leaves its initial state" — a legitimate and frequently-tested result.

### Q7. (Easy) A Schmitt trigger has `V_sat = ±12 V`, `R1 = 1 kΩ`, `R_f = 9 kΩ`, `V_ref = 0`. Find `UT`, `LT`, hysteresis, and state the output polarity for a `+5 V` square input.
**Answer:** `V_th = 12 × 1/9 = `**1.333 V**; `UT = +1.333 V`, `LT = −1.333 V`, hysteresis `= `**2.667 V**. A `+5 V` square (`0 ↔ 5 V`) rises past `UT` ⇒ output goes **+12 V**; falling to 0 V is still above `LT` ⇒ it **stays** at +12 V. So the output is stuck high (a level shifter, not a square wave).
**Method:** `12/9 = 1.3333`; twice that is `2.6667`. Then trace the *actual* input range against the band: `0 V` never goes below `LT = −1.33 V`, so there is no falling transition. This "stuck at one rail" outcome is a classic 2-mark trap when the question gives an unipolar input.

### Q8. (Easy) You need a hysteresis of **6 V** with `V_sat = ±12 V` and `R1 = 1 kΩ`. Find `R_f`.
**Answer:** `2·V_sat·R1/R_f = 6` ⇒ `2 × 12 × 1e3/R_f = 6` ⇒ `R_f = 24000/6 = `**4 kΩ**.
**Method:** Solve the hysteresis formula for the resistor: `R_f = 2·V_sat·R1/(hysteresis) = 2 × 12 × 1000/6 = 4000 Ω`. Check: `2 × 12 × (1/4) = 6` ✓, and the thresholds land at `±3 V`. **To widen the band, increase `R1` or decrease `R_f`** — the ratio is what matters, so scaling both resistors together changes nothing.

### Q9. (Easy) A `+5 V`, `1 kHz` square drives a Schmitt trigger with `V_th = 1 V`, `V_ref = 0`, `V_sat = ±10 V`. Describe the output.
**Answer:** A clean **`+10 V / −10 V` square, 20 V p-p, 1 kHz, in phase with the input** (non-inverting): 0→5 V crossing trips high, 5→0 V falling stops above `LT = −1 V` so it stays high. It is high for the whole positive half and low for the whole negative half.
**Method:** A symmetric square that swings `±5 V` comfortably beyond `±1 V` trips twice per period, so the output is a **square at the same frequency and same phase** (non-inverting configuration). Amplitude = `2V_sat = 20 V`, independent of the input amplitude — a Schmitt trigger restores the rail-to-rail swing, which is why it is the standard "square-wave shaper / limiter".

### Q10. (Easy) A triangle of `±3 V` at `1 kHz` drives the same Schmitt trigger (`V_th = 1 V`, `V_sat = ±10 V). What is the output, and what is the **duty cycle** of the high state?
**Answer:** Output = `±10 V` square at **1 kHz**, in phase. High for the fraction of the period during which `v_in > +1 V`. For a symmetric triangle of peak `3 V` and threshold `V_th = 1 V`, the input is above `+1 V` for `(T/2)(1 − V_th/3) = (T/2)(2/3) = T/3`, so the **duty cycle is exactly 1/3 (33.3 %)**.
**Method:** For a triangle, `v_in` rises linearly, so "the time above a level" is a *linear* interpolation, not an angular one. On the rising ramp the input spans `−V_pk` to `+V_pk`, so the fraction of that half period spent above `V_th` is `(V_pk − V_th)/(2V_pk) = (3−1)/6 = `**1/3**. The falling ramp contributes the same, so total high time `= 2 × (T/2)(1/3) = T/3` ⇒ duty `= 1/3` ✓. Compact rule: **`duty = (1/2)(1 − V_th/V_pk)`** — note the leading `1/2`; it is what makes the duty exactly 50 % when `V_th = 0`. This linear-ramp reasoning is the same mechanism behind the 555 astable's non-50 % duty (Q32).

### Q11. (Moderate) A Schmitt trigger with `V_sat = ±10 V`, `R1 = 1 kΩ`, `R_f = 10 kΩ` drives an integrator with `R = 10 kΩ`, `C = 1 µF`. Find the frequency of the resulting relaxation oscillation and the triangle's p-p.
**Answer:** `V_th = 1 V`, so `UT = +1 V`, `LT = −1 V` and the ramp travels `2 V`. Square amplitude ±10 V into `RC = 10e3 × 1e-6 = `**10 ms** gives slope `10/0.01 = 1000 V/s`. `T/2 = 2/1000 = 2 ms`, `T = 4 ms`, so **f = 250 Hz**; triangle p-p = **2 V**.
**Method:** The 2-op-amp square/triangle generator of `21-Op-Amp-Integrators-Differentiators.md` §21.5, in three lines: Schmitt threshold `V_th = V_sat·R1/R_f`; ramp distance `2V_th`; slope `V_sat/RC` ⇒ `T/2 = 2·V_th·RC/V_sat`. So `T = 4·V_th·RC/V_sat = 4·(V_sat·R1/R_f)·RC/V_sat = `**`4·R1·RC/R_f`**. Check with the numbers: `4 × 1e3 × 1e-2/1e4 = 4e-3 s` ⇒ `f = 250 Hz` ✓. The `V_sat` cancels exactly: bigger rails give a proportionally steeper ramp that compensates for the proportionally longer distance.

### Q12. (Moderate) Repeat Q11 with `V_sat = ±12 V`, `V_th = 3 V` (`R1 = 2.5 kΩ`, `R_f = 10 kΩ`), and `C = 0.5 µF` with `R = 10 kΩ`. Find `f`.
**Answer:** `RC = 10e3 × 0.5e-6 = `**5 ms**. Slope = `12/0.005 = 2400 V/s`. Ramp distance = `2 × 3 = 6 V`. `T/2 = 6/2400 = 2.5 ms`, `T = 5 ms`, so **f = 200 Hz**.
**Method:** `f = V_sat/(4·V_th·RC) = 12/(4 × 3 × 0.005) = 12/0.06 = `**200 Hz** ✓. The single formula to remember: **`f = V_sat/(4 V_th R C)`**, i.e. bigger `RC` ⇒ slower, bigger thresholds ⇒ slower, bigger rails ⇒ faster. Note the triangle p-p (`2V_th = 6 V`) is set by the Schmitt alone, not by the integrator — the integrator only sets the *time* to traverse it.

### Q13. (Moderate) Compare a **comparator** and a **Schmitt trigger** when the input is `1 V` sine plus noise of `±0.8 V` peak, thresholding at 0 V. What happens in each case?
**Answer:** Comparator: the noise repeatedly pushes the input across 0 V, so the output **chatters violently** — a burst of full-swing transitions at up to the noise frequency, and the average power dissipation is high. Schmitt (`V_th = 2 V`): the total input swings only `±1.8 V`, which never reaches `+2 V`, so the output **never switches at all** — a stable, quiet state. There is an intermediate case (`V_th = 1 V`): the output switches once per cycle, cleanly, with no chatter.
**Method:** The rule is `hysteresis width must exceed the total input excursion that noise can produce`. Quantify: `V_pk(signal) + V_pk(noise)` versus `V_th`. Chatter is the default failure mode of a bare comparator and the whole reason positive feedback exists — this is the "why does a Schmitt trigger make a noisy zero-crossing detector clean?" question from `23-Schmitt-Trigger-Comparators.md` §23.4.

### Q14. (Moderate) An **inverting** Schmitt trigger: signal on `v−`; `v+` is a divider between `V_ref` (through `R1`) and `v_o` (through `R_f`), with `R1 = R_f = 10 kΩ` and `V_ref = 0`. Find the two thresholds, the hysteresis, and the output state for `v_in = +3 V`.
**Answer:** `v+ = (V_ref·R_f + v_o·R1)/(R1+R_f) = v_o/2`. Trip when `v_in = v+`. So the trip levels are `v_in = +V_sat/2` (output was high ⇒ goes **low**) and `v_in = −V_sat/2` (output was low ⇒ goes **high**). With `V_sat = ±10 V`: thresholds **±5 V**, hysteresis **10 V** (`2·V_sat·R1/(R1+R_f) = 2×10×0.5`). For `v_in = +3 V`: below `+5 V`, so the output is **+10 V (high)**.
**Method:** Write KCL at the `+` node: `(V_ref − v+)/R1 + (v_o − v+)/R_f = 0` ⇒ `v+ = (V_ref R_f + v_o R1)/(R1+R_f)`, then set `v+ = v_in` for the trip. The **general** inverting-Schmitt hysteresis is `2·V_sat·R1/(R1+R_f)` — with equal resistors it is only `V_sat`, half of the `2V_sat` that a *non-inverting* Schmitt with the same ratio gives, because the equal-resistor divider attenuates the feedback. Watch the polarity: **inverting Schmitt = output high when the input is low** (positive-going input forces the output down), the opposite of Q1.

### Q15. (Moderate) In the inverting Schmitt of Q14, what is the hysteresis if `R1 = 2 R_f`? And if `R1 = 9 R_f`?
**Answer:** `2·V_sat·R1/(R1+R_f)`: `R1 = 2R_f ⇒ 2·V_sat·2/3 = `**1.333·V_sat`** (13.33 V for `V_sat = 10`); `R1 = 9R_f ⇒ 2·V_sat·9/10 = `**1.8·V_sat`** (18 V). Thresholds are `±hysteresis/2`, so `±6.67 V` and `±9 V` respectively.
**Method:** `hysteresis = 2V_sat·R1/(R1+R_f)` — the denominator is the *sum*, which is the difference from the non-inverting form's `2V_sat·R1/R_f`. Bounded by `2V_sat` as `R1/R_f → ∞`. Bigger ratio ⇒ wider band ⇒ more noise immunity but the trigger needs a bigger input swing.

### Q16. (Moderate) A Schmitt trigger's supplies are changed from `±10 V` to `±15 V` with all resistors unchanged. What happens to `UT`, `LT` and the hysteresis?
**Answer:** All three scale linearly by `15/10 = 1.5`: `V_th` goes `1 V → 1.5 V`, hysteresis `2 V → `**3 V**, thresholds `±1.5 V`. The *shape* of the transfer characteristic is unchanged; only the scale moves.
**Method:** Every threshold formula contains `V_sat` **linearly and only** — no squaring, no `log`. So supply scaling scales the band exactly. Practical consequence: a ±15 V-supply Schmitt on a ±1 V signal is useless (it would need 1.5 V to trip); you would re-scale `R_f`.

### Q17. (Moderate) You need the output to switch exactly once per cycle of a `±5 V` sine that carries `±2 V` of noise. Minimum `V_th`? With `V_sat = ±12 V`, what `R1/R_f` do you pick, and how much margin do you have?
**Answer:** The input's total excursion is `±7 V`, so you need `V_th > 7 V`. Pick `V_th = 8 V` for margin. Then `R1/R_f = V_th/V_sat = 8/12 = `**0.667** (e.g. `R1 = 6.7 kΩ`, `R_f = 10 kΩ`), giving a hysteresis of `16 V`.
**Method:** `V_th` must exceed `V_pk(signal) + V_pk(noise)`, with margin — the signal peak and the noise peak **add**, they do not cancel. Then `R1/R_f = V_th/V_sat`. The margin is what makes the circuit immune to *slow* drift and to a slightly-underestimated noise figure; use 1.2–1.5× the calculated `V_th`.

### Q18. (Moderate) What is the transfer characteristic of an **inverting** Schmitt trigger? Describe the loop direction.
**Answer:** Output **high** while `v_in < LT`, then it drops to **low** when `v_in` rises above `UT`, and rises back to **high** when `v_in` falls below `LT`. The loop is traversed **clockwise** when `v_in` is the horizontal axis and `v_o` the vertical one (the non-inverting Schmitt of Q1 is counter-clockwise). With `V_ref = 0` and symmetric rails, the two horizontal segments sit at `±V_sat` and the vertical transitions occur at `v_in = ±V_sat/2` (equal-resistor case).
**Method:** Draw the axes first, then the two horizontal output levels, then the two vertical drops, then join them with the slanted regenerative transitions. The traversal direction is the only thing that differs from the non-inverting case — the *thresholds* and their widths are the same arithmetic. Sketching the loop is the fastest way to answer "is it inverting or non-inverting?" from a circuit picture.

### Q19. (Moderate) A Schmitt trigger is built with `R1 → 0` (input tied straight to `v+`) and `R_f = 10 kΩ`. What circuit have you built?
**Answer:** `R1/R_f → 0` ⇒ `V_th → 0` ⇒ `UT = LT = V_ref` and hysteresis `→ 0`. The circuit degenerates into an ordinary **comparator** with threshold `V_ref`. Positive feedback still exists but is too weak to hold any state against noise.
**Method:** The Schmitt trigger is a comparator plus a *finite* dead band; take the band to zero and you have removed the memory. This is the cleanest proof that hysteresis and chatter-immunity are the same thing, and it is a natural 1-mark conceptual question.

### Q20. (Moderate) Why must the positive-feedback resistor go to `v+`, and what happens if it goes to `v−`?
**Answer:** Sent to `v+`: when the output rises, `v+` rises, which drives the output **higher** — regeneration to the positive rail. Sent to `v−`: when the output rises, `v−` rises, which drives the output **lower** — that is **negative** feedback, so the op-amp becomes a linear amplifier with gain `1 + R_f/R1`, and it can never latch. A comparator with the feedback on `v−` has no hysteresis at all.
**Method:** Ask which input the feedback reinforces. The rule of thumb: **positive feedback must be connected so the output's own move pushes it further in the same direction** — through the *non-inverting* input. If `v+ = v−` can be satisfied with a finite output, you built an amplifier, not a latch.

### Q21. (Moderate) A relaxation oscillator: Schmitt (`V_sat = ±10 V`, `R1 = 2 kΩ`, `R_f = 10 kΩ`) → integrator (`R = 10 kΩ`, `C = 10 nF`). Find `UT`, `LT`, the triangle p-p, the square p-p, and `f`.
**Answer:** `V_th = 10 × 2/10 = `**2 V**, so `UT = +2 V`, `LT = −2 V`. Triangle p-p = `2V_th = `**4 V** (swings `−2 V` to `+2 V`). Square p-p = `2V_sat = `**20 V**. `RC = 1e-4 s`; slope = `10/1e-4 = 1e5 V/s`; `T/2 = 4/1e5 = 40 µs`; `T = 80 µs`; **f = 12.5 kHz**.
**Method:** `f = V_sat/(4·V_th·RC) = 10/(4 × 2 × 1e-4) = 10/8e-4 = `**12.5 kHz** ✓. All five sub-answers fall out of two numbers (`V_th`, `RC`) — draw the loop: the square's amplitude is set by the rails, the triangle's by the divider, and the *ratio* `V_sat/V_th = 5` is exactly the overdrive that makes the switching fast. If that ratio approaches 1, switching gets slow and the triangle gets distorted (slew-rate limit).

### Q22. (Moderate) A triangle wave of `±4 V` at `500 Hz` drives a Schmitt trigger with `V_th = 1.5 V`, `V_sat = ±12 V`. What are the output frequency, amplitude, and the time the output stays HIGH per period?
**Answer:** Output = `±12 V` square (**24 V p-p**) at **500 Hz**, in phase. High while `v_in > 1.5 V`. For a symmetric triangle of peak `4 V`, the time above `1.5 V` is `(T/2)(1 − 1.5/4) = (T/2)(0.625) = 0.3125 T`. With `T = 2 ms`: **t_HIGH = 0.625 ms**, duty cycle **31.25 %**.
**Method:** Derive it. Rising ramp over `[0, T/2]`: `v_in(t) = −4 + 16t/T`, so `v_in = +1.5` at `t = 5.5T/16 = `**`0.34375 T`**. Falling ramp: `v_in(t) = 4 − 16(t − T/2)/T`, so `v_in = +1.5` at `t = `**`0.65625 T`**. Width `= 0.65625 − 0.34375 = 0.3125 T` ✓, so with `T = 2 ms` the output is high for `0.625 ms`. Compact rule: **`duty = (1/2)(1 − V_th/V_pk)`** — here `(1/2)(1 − 1.5/4) = 0.3125`. The leading `1/2` is essential: it is what makes the duty exactly 50 % when `V_th = 0`, as it must be for a symmetric triangle. A positive threshold always shortens the high state.

### Q23. (Moderate) A Schmitt trigger has `V_ref = 1.5 V`, `V_sat = ±10 V`, `R1 = 2 kΩ`, `R_f = 10 kΩ`. Find the thresholds and state, for a slowly rising input from 0 V, the exact output state as a function of `v_in`.
**Answer:** `V_th = 10 × 2/10 = `**2 V**. `UT = 1.5 + 2 = `**3.5 V**; `LT = 1.5 − 2 = `**−0.5 V**; hysteresis `= 4 V`. Starting from output low: for `v_in < 3.5 V` the output stays **−10 V**; the instant `v_in` crosses `+3.5 V` it snaps to **+10 V**; it then stays high until `v_in` falls back below `−0.5 V`.
**Method:** `UT = V_ref + V_th`, `LT = V_ref − V_th` — `V_ref` offsets the *centre* of the band, not its width. This produces an **asymmetric** dead band (`−0.5` to `+3.5 V`) even though the resistors and rails are symmetric, which is how you build a level detector for a signal riding on a DC bias. The trap is writing both thresholds as `V_ref`.

### Q24. (GATE-level) The input to a Schmitt trigger carries `±0.5 V` of noise and you want the dead band to be at least `1.5×` that. `V_sat = ±10 V`. Design the divider and give `UT`, `LT`.
**Answer:** Required hysteresis `≥ 1.5 × 1.0 V = 1.5 V`. Pick `hysteresis = 2 V` ⇒ `V_th = 1 V` ⇒ `R1/R_f = 1/10 = `**0.1**, e.g. `R1 = 1 kΩ`, `R_f = 10 kΩ`. Then `UT = +1 V`, `LT = −1 V`.
**Method:** The noise peak-to-peak is `2 × 0.5 = 1 V`; multiply by the safety factor; that is the hysteresis. Then `V_th = hysteresis/2` and `R1/R_f = V_th/V_sat`. Two easy-to-swap steps: use the **peak-to-peak** noise, and halve to get `V_th`. And remember the noise the op-amp itself generates is *not* in your budget — that is the residual jitter the dead band cannot remove.

### Q25. (GATE-level) Using the relaxation-oscillator relation `T = 2RC·ln(1 + 2R1/R2)` from `29-Formula-Sheet.md` §29.12, with `R1 = R2`, `R = 10 kΩ`, `C = 10 nF`: find `T`, `f` and the two thresholds for `V_sat = ±10 V`.
**Answer:** `ln(1+2) = ln 3 = 1.0986`. `T = 2 × 1e-4 × 1.0986 = 2.197e-4 s` ⇒ **T = 219.7 µs**, **f = 4551 Hz ≈ 4.55 kHz**. Thresholds `= ±V_sat·R1/(R1+R2) = ±10 × 0.5 = `**±5 V**.
**Method:** Straight substitution: `RC = 10e3 × 10e-9 = 1e-4 s`; `T = 2 × 1e-4 × 1.0986 = 2.1972e-4`; `1/T = 4551 Hz`. The `ln` appears here (unlike the op-amp relaxation oscillator of Q21) because the capacitor charges **exponentially** toward the supply through a resistor rather than at a constant slope — a constant-current device gives the linear ramp of Q21, a resistor-plus-supply gives the `ln`. If `R1 = 3R2`: `T = 2RC·ln7 = 3.892RC = 389 µs`, `f = 2.57 kHz`, thresholds `±7.5 V`.

### Q26. (GATE-level) A Schmitt trigger's output must change state in `1 µs`, but the op-amp's slew rate is `0.5 V/µs` and the swing is `±12 V`. Can it keep up? What is the fastest possible transition?
**Answer:** No. The fastest possible transition is `24 V / (0.5 V/µs) = `**48 µs**. Positive feedback makes the op-amp switch *regeneratively* — it goes flat-out to the rail — but it cannot exceed the device slew rate. So a 1 µs requirement is impossible with this part.
**Method:** Slew rate is a hard `V/s` ceiling: `t_min = ΔV/SR = 2V_sat/SR`. The value of positive feedback is that the op-amp spends the whole time slewing *at full rate* toward the correct rail (no rounding, no slow linear approach), which makes the output *sharp* — but "sharp" is still bounded by `SR`. Choosing a faster-slew part (or a comparator IC, which is not slew-limited in the same way) is the real fix.

### Q27. (GATE-level) A square wave of `±5 V` at `10 kHz` feeds a Schmitt trigger with `V_sat = ±12 V`, `V_th = 1 V`, `R1 = 1 kΩ`, `R_f = 10 kΩ`. Sketch the output, and say how many times the output transitions per second.
**Answer:** Input rises `−5 → +5` (crosses `UT = +1`) ⇒ output `−12 → +12`; input falls `+5 → −5` (crosses `LT = −1`) ⇒ output `+12 → −12`. So the output is a **24 V p-p, 10 kHz square, in phase with the input**, with two transitions per input period ⇒ **20 000 transitions per second**.
**Method:** Trace the two crossings; two transitions per period of a symmetric square is automatic. `transitions/s = 2f = 20 kHz` — a Schmitt trigger never produces a toggle at a frequency other than the input's (unlike an astable, which has none). Non-inverting ⇒ output in phase with the input. If the answer had come out antiphase, the circuit would be the inverting form of Q14.

### Q28. (GATE-level) Explain why a Schmitt trigger is described as **regenerative**, and where that shows up in a GATE numerical.
**Answer:** "Regenerative" means the positive feedback **reinforces** its own decision: once `v+` crosses `v−`, the output moves toward a rail, which moves `v+` further in the same direction, which speeds the output up — the switching is effectively instantaneous compared with the linear time constant. Numerically it shows up as (a) the **hysteresis band itself** (without regeneration there is only one threshold), and (b) a very short transition time limited only by `SR`, not by any RC time constant.
**Method:** Two symptoms, one cause. (a) explains every `UT`/`LT`/hysteresis question; (b) explains the "clean square from a slow sine" question and the `2V_sat/SR` limit of Q26. If a problem says "the transition is abrupt although the input is changing slowly", the answer is regeneration, and the number to quote is `t = 2V_sat/SR`.

### Q29. (GATE-level) A level detector must flag when `v_in` is between `1 V` and `3 V`. Design it from two Schmitt triggers and one gate, and check the numbers against a single Schmitt.
**Answer:** Use two Schmitt triggers with `V_th = 0.5 V` each (`R1/R_f = 0.5/10 = 0.05`, e.g. `R1 = 500 Ω`, `R_f = 10 kΩ`): **T1**: `V_ref = 0.5 V` ⇒ `UT = 1.0 V`, `LT = 0.0 V`, output HIGH while `v_in > 1 V`. **T2**: `V_ref = 3.5 V` ⇒ `UT = 4.0 V`, `LT = 3.0 V`, output **LOW** while `v_in < 3 V`. Invert T2 and AND it with T1 ⇒ the flag is HIGH for exactly `1 V < v_in < 3 V`, with `1 V` of noise dead band on each edge. A **single** Schmitt with `V_ref = 2 V`, `V_th = 1 V` does have the same two trip levels (`LT = 1 V`, `UT = 3 V`), but it reports the *complement*: HIGH **outside** the band, LOW inside. So one Schmitt is a valid window detector only if an inverted output is acceptable.
**Method:** Each Schmitt supplies exactly two trip levels symmetric about `V_ref` at `V_ref ± V_th`, so two independent `V_ref` values give two independent edges. Rule of thumb: **one comparator = one threshold, one Schmitt = two thresholds about a common `V_ref`, two Schmitts + a gate = a window with dead band on both edges.** Note the economics: the two-Schmitt version tolerates `1 V` of noise at each edge, the single-Schmitt version tolerates nothing at all — its two thresholds are the *same* measurement, so noise on the edge just makes the flag flicker (cf. Q13).

### Q30. (GATE-level) A `0.5 V` pk, `1 kHz` square drives a Schmitt trigger (`V_th = 2 V`, `V_sat = ±10 V). Is anything wrong? Give the output and the best single fix.
**Answer:** The output **never switches** — it stays at `±10 V` in whatever state it started in (Q6). The cleanest fix is to **amplify the input** before the trigger (a non-inverting preamp of gain ≥ 4) so the 2 V threshold is reached; scaling `R1/R_f` down cannot help, because a *smaller* `V_th` also narrows the noise margin, and the input is too small to be a reliable `2 V` swing in the first place. Alternatively lower `V_th` below `0.5 V` — but then the dead band is under 1 V and the trigger becomes noise-sensitive, defeating the purpose.
**Method:** Always check `V_pk(input)` against `V_th` **first**. If `V_pk < V_th`, the answer is "no output" and the design is at fault, not the numbers. The general design rule is `V_th ≤ V_pk(signal)` (so switching happens) **and** `V_th > 2·V_pk(noise)` (so noise cannot) — both must hold, and if they cannot both hold, gain is required.

### Q31. (GATE-level) Which of the following statements is **correct**?
- (A) A comparator has no virtual short because it has no feedback.
- (B) A Schmitt trigger's hysteresis is `V_sat·R1/R_f`.
- (C) Both thresholds of a non-inverting Schmitt are equal to `V_ref`.
- (D) An inverting Schmitt trigger produces a larger hysteresis than a non-inverting one with the same resistor ratio.
**Answer:** **(A).** (B) is false — hysteresis is `2·V_sat·R1/R_f`, twice the one-sided trip. (C) is false — the thresholds are `V_ref ± V_sat·R1/R_f`, and coincide with `V_ref` only if the ratio is 0 (Q19). (D) is false — the inverting form gives `2·V_sat·R1/(R1+R_f) ≤ 2·V_sat·R1/R_f`, so it is always **equal or smaller** (Q14, Q15).
**Method:** For each option, name the formula it contradicts. Statement (A) is the load-bearing one: **open loop ⇒ no virtual short ⇒ the output is always at a rail.** If you remember only that, (B), (C) and (D) become arithmetic rather than judgement.

### Q32. (GATE-level) A 555 astable has `R_A = R_B = 10 kΩ`, `C = 1 nF`. Find `T`, `f`, and the duty cycle. Then explain the duty in terms of the 555's internal thresholds.
**Answer:** Charge through `R_A+R_B` from `Vcc/3` to `2Vcc/3` (time `0.693·(R_A+R_B)·C`), then discharge through `R_B` to `Vcc/3` (time `0.693·R_B·C`). Total `T = 0.693·(R_A + 2R_B)·C = 0.693 × 30e3 × 1e-9 = `**20.79 µs**, so **f = 48.1 kHz**. Duty `= (R_A+R_B)/(R_A+2R_B) = 20/30 = `**66.7 %**.
**Method:** Each half-cycle is one `ln2` of an RC exponential (`0.693·τ`), and the two half-cycles have *different* time constants: `τ_charge = (R_A+R_B)C` and `τ_discharge = R_B C`, hence `T = 0.693·(R_A + 2R_B)·C`. Connect it to Q1: the 555's internal comparators trip at `Vcc/3` and `2Vcc/3`, i.e. a threshold **pair symmetric about `Vcc/2` with `V_th = Vcc/6 = V_sat/3`** — exactly a Schmitt with `R1/R_f = 1/3`, as in Q1 with a 3:1 divider. The only structural difference from the op-amp relaxation oscillator of Q21 is that the capacitor charges **exponentially through a resistor toward the supply** rather than at a constant slope, which is where the `ln 3` of Q25 comes from. Duty exceeds 50 % whenever `R_A > 0`, because charging through two resistors is always slower than discharging through one.

### Q33. (GATE-level) Summarise in one line each: what a Schmitt trigger gives you that a plain comparator does not, and what it costs you.
**Answer:** **Gives you:** two thresholds instead of one, hence a **dead band** — noise inside it cannot switch the output, so the output never chatters; a clean, rail-to-rail square from a small or noisy input; and a **latching/memory** action (the output remembers which way it went). **Costs you:** a wider **input swing is required** (the input must exceed `V_th`, not just cross a reference), **slower and larger** switching in the small-signal sense, one extra resistor ratio to design, and a *non-monotonic* (hysteretic) transfer characteristic that cannot be used for linear amplification.
**Method:** Frame every Schmitt-trigger question as a trade: *noise immunity* (up) against *input amplitude required* (up), with *linearity of the transfer curve* (down). That framing survives any MCQ, including the "why not just use a comparator?" and "why is a Schmitt trigger not used as an amplifier?" variants.

---

## Trap box (exam-day killers)

- **Hysteresis is `2·V_sat·R1/R_f`, not `V_sat·R1/R_f`.** The one-sided trip and the band width are different numbers; the band is **twice** the trip.
- **Neither threshold is `V_ref`.** They are `V_ref ± V_sat·R1/R_f`. They land on `V_ref` only in the degenerate `R1 → 0` comparator (Q19).
- **Picking the wrong threshold.** Rising input trips at `UT`, falling at `LT`. Decide "what is the output doing *now*?" *before* you compute.
- **`R1/R_f` vs `R_f/R1`.** Ratio > 0.1 gives a narrow band; swapping the resistors gives a band up to `2V_sat` wide and will change the answer by 100×.
- **Writing the virtual short in a comparator.** Open loop ⇒ no feedback ⇒ `v+ ≠ v−` is fine and the output is at a rail.
- **Feedback to `v−`.** That is *negative* feedback; you built a linear amplifier, and it will never latch (Q20).
- **Assuming the output can sit mid-rail.** It cannot — positive feedback is regenerative, not a settling curve.
- **Forgetting to compare `V_pk` with `V_th` first.** `V_pk < V_th` means "output never switches", a legitimate and frequently-asked answer (Q6, Q30).
- **Noise budget uses peak-to-peak.** Need `V_th > 2·V_pk(noise)`, not `> V_pk(noise)`, and add margin (Q17, Q24).
- **Non-inverting = in phase, inverting = antiphase.** But inverting hysteresis is `2V_sat·R1/(R1+R_f)`, i.e. **≤** the non-inverting value (Q14, Q15).
- **Slew rate still applies.** "Instantaneous" means `2V_sat/SR`, not zero (Q26).
- **Op-amp vs comparator IC.** An op-amp's output is slew-limited and its propagation delay drifts with temperature; a dedicated comparator gives you a defined delay and a logic-level output.

## Final recall drill (do in 60 seconds)

1. Non-inverting Schmitt: `UT = V_ref + V_sat·R1/R_f`, `LT = V_ref − V_sat·R1/R_f`.
2. Hysteresis `= 2·V_sat·R1/R_f`. Inverting form: `2·V_sat·R1/(R1+R_f)`.
3. `V_sat = ±10 V`, `R1 = 1 kΩ`, `R_f = 10 kΩ` ⇒ trip ±1 V, hysteresis 2 V.
4. Positive feedback goes to **`v+`**; the transition loop of a non-inverting Schmitt is traversed **counter-clockwise**.
5. Comparator: `v+ > v− ⇒ +V_sat`. No virtual short.
6. `R1 → 0` ⇒ hysteresis → 0 ⇒ a plain comparator.
7. Relaxation oscillator: `f = V_sat/(4·V_th·RC)`, triangle p-p `= 2V_th`, square p-p `= 2V_sat`.
8. `V_sat = ±10 V`, `V_th = 2 V`, `RC = 1 ms` ⇒ `f = 1.25 kHz`, triangle 4 V p-p.
9. Triangle-driven duty `= (1/2)(1 − V_th/V_pk)`. Zero threshold ⇒ 50 %. `V_pk = 3 V`, `V_th = 1 V` ⇒ 1/3.
10. 555 astable: `T = 0.693(R_A + 2R_B)C`; duty `= (R_A+R_B)/(R_A+2R_B) > 50 %`.
11. Fastest output transition `= 2V_sat/SR`.
12. Design rule: `V_pk(signal) > V_th > 2·V_pk(noise)`; if no `V_th` satisfies both, add gain.

---
