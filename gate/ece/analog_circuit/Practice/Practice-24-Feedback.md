# Feedback in Amplifiers — Practice (Learn by Solving)

> **The idea in one line:** feeding **a fraction `β` of the output back to the
> input in phase** multiplies the usable gain by `(1 + Aβ)` and divides the
> error by exactly the same factor. Everything in this file is
> `A_f = A/(1 + Aβ)` rearranged four different ways.
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve
> the next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `24-Feedback.md` or `32-Single-File-Cheatsheet.md` only when you want the
> underlying theory.

## Concept box (what you must internalise)

- Closed-loop gain: `A_f = A/(1 + Aβ)`, where `A` is **open-loop** gain and `β` the feedback fraction.
- **Deep negative feedback** (`Aβ ≫ 1`): `A_f → `**`1/β`**, set by *resistors only* — not by the op-amp. The op-amp's job is now to supply current, not accuracy.
- Sensitivity to the amplifier: `dA_f/A_f = (dA/A)/(1 + Aβ)`. Feedback makes the gain depend on the *network*, not the device.
- **Bandwidth grows by the same factor**: `BW_cl = (1 + Aβ)·BW_ol`, and `A_f·BW_cl = A·BW_ol` is invariant (= GBW).
- Error, distortion and output-referred noise are all divided by `(1 + Aβ)`.
- **Negative** feedback ⇒ the four `D`s (distortion, drift, noise, offset) fall. **Positive** feedback ⇒ they rise and the circuit oscillates or latches.
- `Aβ` is the **loop gain**; everything above is a consequence of it. Work in `Aβ`, not in `A`.

---

## Questions

### Q1. (Easy) An amplifier has `A = 1×10⁵` and negative feedback with `β = 0.01`. Find `A_f` and the loop gain.
**Answer:** `Aβ = 1e5 × 0.01 = `**1000**. `A_f = 1e5/(1 + 1000) = `**99.9 ≈ 100 = 1/β**.
**Method:** Two steps, always in that order: multiply to get the loop gain, then divide. `1 + Aβ = 1001`, not 1000 — that 0.1 % is the entire difference between `99.9` and the ideal `100`. Since `Aβ = 1000 ≫ 1`, the deep-feedback approximation `A_f ≈ 1/β = 100` is justified to within 0.1 %.

### Q2. (Easy) State the closed-loop gain for deep negative feedback, and the two topologies that realise voltage gain.
**Answer:** `A_f → `**`1/β`**. The **voltage-series** (non-inverting) amplifier gives `A_f = 1 + R_f/R1`; the **voltage-shunt** (inverting) amplifier gives `A_f = −R_f/R1`. Both are set purely by two resistors.
**Method:** `1/β` is the *transconductance-free* answer — derive it from the virtual short and it drops out. For voltage-series, `β = R1/(R1+R_f)` so `1/β = 1 + R_f/R1`; for voltage-shunt, `β = R1/(R1+R_f)` in magnitude, so `1/β = (R1+R_f)/R1`, and the inverting sign supplies the minus. The whole family of amplifier types in this chapter is just "which of the four `1/β` quantities do you want".

### Q3. (Easy) A negative-feedback amplifier has `A = 2×10⁵`, `β = 0.02`. Find `A_f` exactly and by the approximation.
**Answer:** `Aβ = 4000`, `A_f = 2e5/4001 = `**49.9875**. Approximation `1/β = `**50**. Error `= (50 − 49.9875)/50 = `**0.025 %**.
**Method:** `2e5/4001 = 49.9875`. The general approximation error is exactly `1/(1 + Aβ) = 1/4001 = 0.025 %` — always the same formula, whatever the numbers. If `Aβ > 100`, quoting `1/β` loses less than 1 %; if `Aβ > 10⁴` you can forget `A` entirely.

### Q4. (Moderate) An inverting amplifier must give `|A_f| = 11` with `β = 0.09`. What open-loop gain is required for the gain to be within 1 % of the ideal `1/β`?
**Answer:** `A = A_f/(1 − A_f β) = 11/(1 − 11×0.09) = 11/(1 − 0.99) = 11/0.01 = `**`1100`**. Then `Aβ = 99` and `A_f = 1100/100 = `**11.0 exactly**, i.e. within 1 % of the ideal `1/β = 11.11`. Work in **magnitudes** throughout — the inverting sign lives in the circuit topology, not in the `β` you plug into the formula.
**Method:** Rearrange `A_f = A/(1 + Aβ)` for `A`: `A = A_f/(1 − A_f β)`. Two checks. (i) Substitute back: `Aβ = 1100×0.09 = 99`, `A_f = 1100/100 = 11` ✓. (ii) Sanity-check the error: `1/(1 + Aβ) = 1/100 = `**1 %** ✓, which is what the question asked for. The "accuracy to ε needs `Aβ ≈ 1/ε`" rule (Q26) is the same statement: here `ε = 1 %` ⇒ `Aβ = 100`. **Trap:** writing `A = A_f/(1 + A_f β)` — the denominator must *subtract*, because you are solving for the gain that makes the `+Aβ` in the original equation come out right.

### Q5. (GATE-level) Can negative feedback ever make the closed-loop gain *exceed* `1/β`? Show it numerically.
**Answer:** **No — never, for any finite `A`.** `A_f = A/(1 + Aβ) = (1/β)·(Aβ/(1 + Aβ))`, and the bracketed factor is always `< 1` for finite `Aβ`, approaching 1 only as `A → ∞`. Example: `β = 0.02` gives `1/β = 50`; asking for `A_f = 51` requires `A = 51/(1 − 51×0.02) = 51/(−0.02) = `**negative** — a contradiction, i.e. **impossible**. Similarly `A_f = 9.9` with `β = 0.1` (`1/β = 10`) needs `A = 9.9/(1 − 0.99) = `**990**; `A_f = 11` with `β = 0.09` (`1/β = 11.11`) needs `A = 11/(1 − 0.99) = `**1100**. Only `A_f` *below* `1/β` is reachable.
**Method:** Write `A_f = (1/β)·Aβ/(1 + Aβ)` and note `x/(1+x) < 1` for all `x ≥ 0`. This is why "gain accuracy" questions always come with a target **below** `1/β`; the examination never asks for more than the network can give. If a question does, the correct answer is "not possible with negative feedback".

### Q6. (Easy) `A = 1×10⁴`, `β = 0.1`. By what factor are output distortion and output-referred noise reduced?
**Answer:** Loop gain `Aβ = `**1000**. Distortion and output noise are both divided by `1001` ⇒ reduced by a factor of **`1001×`**, i.e. `20log₁₀(1001) = `**60 dB**. In deep feedback, quote the factor as `≈ 1/(Aβ)`.
**Method:** A non-linearity produces a fraction `D` of extra output; negative feedback opposes that extra output with a correction of `D·Aβ` times itself, leaving `D/(1 + Aβ)`. Identical algebra for output-referred noise. The `+1` again: it is `1/(1 + Aβ)`, never exactly `1/(Aβ)`. This is the basis of the phrase "feedback reduces distortion by the loop gain".

### Q7. (Moderate) The open-loop gain of an amplifier drops 10 % with temperature. With `A = 1×10⁵`, `β = 0.01`, by what percentage does the closed-loop gain change?
**Answer:** Relative sensitivity `= 1/(1 + Aβ) = 1/1001 = `**0.0999 %** of the change. A 10 % drift in `A` therefore becomes a `10/1001 = `**0.0100 %** change in `A_f` (≈ 1 part in 10 000). For comparison, an open-loop amp would move a full 10 % ≈ 0.83 dB.
**Method:** Differentiate `A_f = A/(1 + Aβ)` with `β` fixed: `dA_f/dA = 1/(1 + Aβ)²`, so `dA_f/A_f = (dA/A)/(1 + Aβ)`. Divide the drift by the loop gain — that is the whole point of negative feedback: **it trades gain accuracy for stability of accuracy.** The dB figure is `20log₁₀(1.1) = 0.83 dB` of open-loop change, shrinking to 0.00083 dB.

### Q8. (Easy) What is the *only* property of the amplifier that feedback cannot improve? Name two that it does improve.
**Answer:** **Speed / bandwidth** — feedback *uses* bandwidth to buy gain, so `BW` never improves; it multiplies by `(1 + Aβ)` (Q9). It improves: **gain accuracy** (depends on `1/β`, not `A`), **linearity** (distortion down by `1 + Aβ`), **output impedance** (`R_out/(1 + Aβ)`), and it makes `A` **temperature- and supply-insensitive**.
**Method:** Feedback always costs something and the cost is always the same currency: **bandwidth and stability margin**. Everything on the "improves" list follows from dividing the error by `(1 + Aβ)`; the one thing that cannot be divided is the device's own `f_t`. If a question offers "feedback improves bandwidth", it is wrong unless it also raises the gain.

### Q9. (Moderate) An amplifier has `A = 1000`, `β = 0.01`, and you want a closed-loop gain of 100. What is the percentage error?
**Answer:** `Aβ = 10`, `A_f = 1000/11 = `**90.909**. Error `= (100 − 90.909)/100 = `**9.09 %**. The gain is nearly 10 % low because `Aβ` is only 10, barely into feedback.
**Method:** `A_f = A/(1 + Aβ)`. The fractional shortfall from `1/β` is exactly `1/(1 + Aβ) = 1/11 = 9.09 %`. Rule of thumb: **to get `A_f` accurate to 1 % you need `Aβ > 99`, i.e. about 40 dB of loop gain** — that is the "how much loop gain do I need for 1 % gain accuracy" question you will see, and the answer is always `1/ε`.

### Q10. (Moderate) An inverting amplifier uses `R1 = 10 kΩ`, `R_f = 90 kΩ`, and the op-amp's differential input resistance is `1 MΩ`. What is the closed-loop input resistance, and what is `1/β`?
**Answer:** `A_f = −R_f/R1 = −9`; `1/β = 1 + R_f/R1 = `**10**. Input resistance with feedback `= R1 + (R1 ∥ R_f) = 1e4 + (1e4×9e4/1e5) = 1e4 + 9e3 = `**19 kΩ** — the input sees `R1` in series with the parallel combination, not `R1` alone.
**Method:** `1/β` is read straight off the resistor ratio (`1 + R_f/R1`); the input resistance is a *separate* calculation where feedback makes the op-amp's own `1 MΩ` irrelevant, because the virtual short forces `R_f`'s current to be supplied through `R1`. The classic trap is quoting `R_in = R1 = 10 kΩ` — the true value is larger, which is why inverting amps are not chosen for high input impedance.

### Q11. (Moderate) A non-inverting amplifier has `R1 = 100 kΩ`, `R_f = 900 kΩ` from the inverting input to ground. What are the signal gain and the **noise gain**?
**Answer:** Signal gain `A_f = 1 + R_f/R1 = `**10**. Noise gain (gain seen by a differential input) `= 1 + R_f/R1 = `**10** as well — for the non-inverting topology they are equal, which is precisely why that topology is preferred for low-noise work. Total `R1 ∥ R_f = 1e5×9e5/1e6 = `**90 kΩ** sets the noise bandwidth.
**Method:** In the non-inverting amp the input source is connected to `v+`, so signal and differential noise see the *same* closed-loop gain. Contrast the inverting amp (`24-Feedback.md` §24.6): its signal gain is `−R_f/R1 = −9` but its noise gain is `1 + R_f/R1 = 10` — noise gets amplified **10×** while the signal gets 9×, so the inverting SNR is worse by `10/9`, i.e. `10log₁₀(10/9) = `**0.46 dB**. Always ask "which gain does the noise see?"

### Q12. (GATE-level) An op-amp has `A₀ = 1×10⁵` (DC) and `f_t = 1 MHz`. With `β = 0.01`, find the open-loop bandwidth, the closed-loop gain, and the closed-loop bandwidth.
**Answer:** `Aβ = 1000`, `A_f = 99.9`. `BW_ol = f_t/A₀ = 1e6/1e5 = `**10 Hz**. `BW_cl = f_t/A_f = 1e6/99.9 = `**10.01 kHz**. Increase `= 10.01k/10 = `**1001 = 1 + Aβ** ✓.
**Method:** For a single-pole op-amp, `A·f = f_t` at all frequencies, so the closed-loop bandwidth is `f_t/A_f` — bandwidth is whatever the gain does not use. Check the invariant: `A_f × BW_cl = 99.9 × 10.01k = 1e6 = A₀ × BW_ol` ✓. **Gain–bandwidth product is conserved by feedback**; that conservation is why a 100× gain amplifier has 1/100th the bandwidth.

### Q13. (Easy) Feedback reduces sensitivity to amplifier variations by a factor of `(1 + Aβ)`. With `Aβ = 10⁴`, by how much is the closed-loop gain less sensitive to temperature, supply drift and component ageing?
**Answer:** By a factor of **`10001×`** — a 1 % change in `A` produces a `1/10001 = `**`0.0001 %** change in `A_f`.
**Method:** `1/(1 + Aβ) = 1/10001 ≈ 1e-4`. In dB terms, 40 dB of loop gain buys 40 dB (a factor of 100) of *extra* desensitivity beyond the raw ratio — but the honest statement is the plain ratio. The practical reading: with 40 dB of loop gain, a 1 % drift in the op-amp's gain becomes a 0.01 % drift in the amplifier, which is below the drift of the feedback resistors themselves — the circuit is now resistor-limited, and the design is finished.

### Q14. (Moderate) A voltage amplifier has `R_out = 1 kΩ` open loop, `A = 1×10⁵`, `β = 0.01`. What is `R_out` with feedback, and why does this matter?
**Answer:** `R_out,cl = R_out/(1 + Aβ) = 1e3/1001 = `**1.0 Ω**. This matters because the output can now drive a low-resistance load without the gain collapsing: the amplifier looks like a near-ideal voltage source.
**Method:** Feedback makes the output *stiff*. If `v_out` sags, `v_out/β` moves the inverting input, the op-amp corrects the sag, and the correction is amplified by `A` — so the *sag itself* is suppressed by `(1 + Aβ)`. Same mechanism as Q7, applied to output impedance. `1 Ω` is close to the classic `0.1 Ω` op-amp figure; the residual comes from the finite open-loop gain.

### Q15. (Moderate) In a non-inverting amplifier, `R1 = 9 kΩ` (to ground) and `R_f = 1 kΩ` (output to `−` input). What is `1/β`, and what is `Q` if this is a 2nd-order Sallen-Key low-pass with the same gain?
**Answer:** `1/β = 1 + R_f/R1 = 1 + 1/9 = `**1.111**, so `A_f = 1.111`. As a Sallen-Key gain `k = 1.111`, `Q = 1/(3 − k) = 1/(3 − 1.111) = 1/1.889 = `**0.529**, safely below 0.707, so the response is monotonic with a soft knee.
**Method:** The two gain conventions are the same circuit read two ways: as an amplifier `A_f = 1 + R_f/R1`; inside a Sallen-Key `Q = 1/(3 − k)` where `k` is that same ratio. Note that `k` slightly *above* 1 already gives `Q < 0.707`, so a unity-gain Sallen-Key is deliberately under-damped (`Q = 1/3`) — you need `k ≈ 1.586` for a flat 2nd-order Butterworth (see `Practice-22-Active-Filters.md` Q33). The `1 + …` is the term students forget most often.

### Q16. (Easy) Complete the table: fractional closed-loop gain error `1/(1 + Aβ)` for `Aβ = 0.1, 1, 10, 100, 1000`.
**Answer:** `0.1 → `**90.9 %**`, `1 → `**50 %****, `10 → `**9.09 %**`, `100 → `**0.990 %**`, `1000 → `**0.0999 %**`.
**Method:** Each decade of loop gain buys one decade of accuracy: 10× loop gain ⇒ 10× better. Memorise the ladder `10 % → 1 % → 0.1 %` at `Aβ = 10, 100, 1000`. The two anchor points worth remembering cold are `Aβ = 1` (error 50 %, i.e. gain is halved — feedback is doing something but not much) and `Aβ = 10` (error ~9 %, the usual threshold for calling an amplifier "precise").

### Q17. (Easy) An op-amp has input offset voltage `V_os = 5 µV`. Compare the output offset error at `β = 0.001` and at `β = 0.01`.
**Answer:** Output offset `= V_os/β`: at `β = 0.001` ⇒ `5e-6/1e-3 = `**5 mV**; at `β = 0.01` ⇒ `5e-6/1e-2 = `**0.5 mV**. Ten times more feedback ⇒ ten times less offset error.
**Method:** `V_os` appears at the input just as a real input signal would, and is amplified by the *closed-loop* gain `1/β`, so `V_out,offset = V_os/β = V_os × A_f`. **Feedback does not reduce the output offset in absolute terms — it reduces it only by allowing a larger closed-loop gain for the same `1/β`-limited accuracy.** This is the one place where "feedback cancels offset" is a misconception: deep feedback makes offset *proportional to gain*, and if you raise the gain you raise the offset too.

### Q18. (Moderate) An amplifier has loop gain `Aβ = 1000`. Express it in dB, and state the phase margin of a single-pole (dominant-pole) design.
**Answer:** `20log₁₀(1000) = `**60 dB**. A dominant-pole design has a phase margin of approximately `90°` at the unity-gain crossover and **infinite gain margin** (the open-loop phase never approaches 180°). Practical targets are 45–60°, achieved by adding a compensating pole.
**Method:** Loop gain in dB is `20log₁₀(Aβ)`, and 3 dB corresponds to a factor of 1.41, so 6 dB ≈ 2×: 60 dB = 1000× ✓. The trade is explicit: `Aβ` sets how much desensitivity you buy, and the phase margin sets how far you are from oscillation. A dominant pole gives ~90° of margin but only modest `Aβ` at the crossover; pushing `Aβ` higher brings the crossover closer to the next pole, eats phase margin, and eventually oscillates (Q19).

### Q19. (GATE-level) Compare the stability of feedback amplifiers with `Q = 0.5`, `0.707`, `1.0`, `2.0` in a 2nd-order loop. Which is closest to oscillation?
**Answer:** `Q = 0.5` heavily damped, `Q = 0.707` Butterworth (maximally flat, −3 dB at `f_c`), `Q = 1.0` has a `0 dB` peak at `f_c` with a −3 dB point, and `Q = 2.0` has a **+6.02 dB peak** (`20log₁₀(2) = 6.02`) plus heavy ringing. **`Q = 2.0` is closest to oscillation**; ringing peaks grow as `Q` passes 1 and diverge as `Q → ∞`.
**Method:** `Q` in a feedback loop plays exactly the role it plays in a filter (see `Practice-22-Active-Filters.md` Q19): the closed-loop transfer function `A/(1 + Aβ(s))` has a pair of complex poles whose damping is set by `Q`. The loop oscillates at `Q → ∞`, i.e. when the phase lag reaches 180° at a frequency where `|Aβ| ≥ 1` — the Nyquist/Barkhausen statement of the same fact. **Peaking in the closed-loop magnitude is the audible/visible symptom of too little phase margin.**

### Q20. (GATE-level) Two cascaded stages each have `A = 100` with `β = 0.01` per stage. Compare the overall gain with one stage of `A = 10⁴`, `β = 0.01`.
**Answer:** Per stage `Aβ = 1`, `A_f = 100/2 = `**50**; two stages give `50 × 50 = `**2500**. Single stage: `Aβ = 100`, `A_f = 1e4/101 = `**99.0**. So **the two cascaded stages deliver 25× more closed-loop gain while having 34 dB *less* total loop gain** (total `(1+Aβ) = 2×2 = 4` = 12 dB, versus `101` = 40 dB) — and each stage is individually half as accurate as its own `1/β = 100` ideal (50 vs 100, a 3.01 dB shortfall per stage).
**Method:** The two architectures differ in where the loop closes. Cascading two *weak* loops multiplies the **gain** (`A_f₁·A_f₂ = 2500`) but multiplies the **inaccuracy**, the noise, and the offset of both independent stages — the second stage amplifies the first stage's errors as well as its signal. One strong loop around a single high-gain stage multiplies the **loop gain** instead (`(1+Aβ) = 101`), which suppresses every error source at once. That is the architectural argument of `24-Feedback.md` §24.4: **gain cascades, error does not.**

### Q21. (Easy) A **voltage-series** (non-inverting) amplifier has `R1 = 1 kΩ`, `R_f = 9 kΩ`. Find `β` and `1/β`, and confirm which of the four amplifier types it is.
**Answer:** `β = R1/(R1 + R_f) = 1/10 = `**0.1**, `1/β = `**10**, `A_f = 10`. It is **voltage-series** (series-series): it senses output **voltage** and returns it in **series** (voltage) at the input. Ideal `R_in = ∞`, `R_out = 0`.
**Method:** `β` is the fraction of output that reaches the *op-amp's* input, so the divider is `R1` (to ground) over `R1 + R_f`. The four types and their ideal `1/β`: **voltage-series** `1 + R_f/R1` (voltage gain, `R_in→∞`, `R_out→0`); **voltage-shunt** `R_f/R1` (inverting voltage gain); **current-series** `1/R_s` (transconductance, `R_in→0`); **shunt-shunt** `R_f` (transresistance, `R_out→∞`). Naming which one you have is half of every topology question.

### Q22. (Moderate) A **current-series** (transconductance) feedback amplifier uses a sense resistor `R_s = 2 kΩ` in the output lead. What is the ideal input-output relation, and what is `β`?
**Answer:** `1/β = 1/R_s = 1/2e3 = `**0.5 mA/V** (500 µA/V): `i_out = v_in/R_s`. `β = R_s = `**2 kΩ** (β is dimensionless only after normalisation, which is why the four topologies have incommensurable `1/β` units).
**Method:** For current-series feedback, the output current is sensed by developing a voltage `i_out·R_s` and returning a *fraction of that voltage* in series with the input; deep feedback then forces that fraction to equal the input ⇒ `i_out = v_in/R_s`. High `R_s` means more output impedance. The unit mismatch is the giveaway: a transconductance amplifier's `1/β` is in **A/V**, not a pure number — you cannot compare it numerically with the voltage-gain cases.

### Q23. (Moderate) A **shunt-shunt** (transresistance) feedback amplifier has `R_f = 100 kΩ`. What is the ideal `1/β`, in what units, and what happens as `R_f → ∞`?
**Answer:** `1/β = R_f = `**1×10⁵ V/A** (100 kV/A). As `R_f → ∞`, `1/β → ∞`, so the ideal gain diverges — a photodiode TIA with a huge feedback resistor is the standard realisation, and the limit is the photodiode's own leakage and the op-amp's bias currents.
**Method:** The output current flows through `R_f` to develop `v_out = −i_in·R_f`; deep feedback forces the summing node to stay at virtual ground so *all* the input current flows through `R_f`. Sensitivity to `R_f` is `(1 + Aβ)`-fold improved, which is why TIA gain accuracy depends on resistor *matching and stability*, not on the op-amp. The units (V/A) tell you immediately it is a transresistance stage.

### Q24. (GATE-level) A non-inverting amplifier has `R1 = 10 kΩ`, `R_f = 100 kΩ` (gain 11), and the input signal is `100 mV`. Compare its input-referred noise to the open-loop amplifier's.
**Answer:** Input-referred noise at the amplifier's input is **unchanged** — feedback does not create noise, and the noise gain equals the signal gain (11), so the input SNR is identical to open loop. What feedback buys is a **10.4 dB better SNR at the output** than the same op-amp used open-loop at the same signal level, because the useful signal grew 11× while the output noise grew only 11× from the same sources. `10log₁₀(11) = `**10.41 dB**.
**Method:** Distinguish two claims that are routinely confused. (i) *Input-referred* noise is a property of the device and the noise-gain network — feedback cannot reduce it. (ii) *Output-referred* noise is reduced by `1/(1 + Aβ)`, so as you close the loop the **signal-to-noise ratio at the output is preserved relative to the ideal gain**. For the inverting topology the mismatch between noise gain and signal gain makes the loss explicit: `10/9`, i.e. 0.46 dB (Q11).

### Q25. (Easy) Summarise in one line each what negative feedback does to the four classic imperfections, and what it costs.
**Answer:** **Divides by `(1 + Aβ)`:** distortion, output-referred noise, output offset drift, sensitivity to `A`, `R_out` (and `R_in` toward its ideal). **Costs:** bandwidth (multiplied by `1 + Aβ`, with `A_f·BW = GBW` invariant), phase margin and hence stability, and transient overshoot/ringing as `Q` rises. Positive feedback does the exact opposite of the first list and is the mechanism of every oscillator and latch.
**Method:** Learn it as the **"four D's down, bandwidth down, margin down"** trade of `24-Feedback.md` §24.7. The two questions that test it directly are "how much does feedback reduce distortion?" (`1/(1+Aβ)`, Q6) and "what does feedback not improve?" (bandwidth, Q8). If you can state the trade in one line, every numerical follows.

### Q26. (Moderate) How much loop gain is needed for the closed-loop gain to be accurate to 0.1 %? To 0.01 %?
**Answer:** Error `= 1/(1 + Aβ) ≤ ε` ⇒ `Aβ ≥ 1/ε − 1`. For `0.1 %` (`ε = 1e-3`): `Aβ ≥ `**999**. For `0.01 %` (`ε = 1e-4`): `Aβ ≥ `**9999**. In dB that is ~60 dB and ~80 dB of loop gain.
**Method:** `A_f = (1/β)(1 − 1/(1+Aβ))`, so the fractional error is exactly `1/(1+Aβ)`. Solve for `Aβ` and quote `≈ 1/ε` — a beautifully simple result: **the loop gain you need is the reciprocal of the accuracy you want**, 40 dB per decade. (This is why `β` resistors are usually 0.1 % parts: their own tolerance is then the dominant error term, and the op-amp's `A` is irrelevant.)

### Q27. (GATE-level) An op-amp has `f_t = 1 MHz` and the design needs `A_f = 50`. What loop gain, closed-loop bandwidth, and open-loop bandwidth do you get, and is the op-amp adequate?
**Answer:** `A_f = 50` ⇒ `β = 1/50 = `**0.02**. `BW_cl = f_t/A_f = 1e6/50 = `**20 kHz**. Taking a 741-class `A₀ = 2×10⁵`, `Aβ = 2e5 × 0.02 = `**4000**, so `BW_ol = BW_cl/(1+Aβ) = 20000/4001 = `**5.0 Hz**. Adequate: yes — 20 kHz of closed-loop bandwidth is a factor of 50 of headroom against the 1 MHz part.
**Method:** The number to memorise is `BW_cl = f_t/A_f`: **bandwidth is simply GBW divided by whatever gain you close the loop at.** Feedback does not create bandwidth, it only reallocates it. Then invert Q12 to get the open-loop corner, `BW_ol = BW_cl/(1+Aβ)`, and check the invariant `A₀·BW_ol = 2e5 × 5.0 = 1e6 = f_t` ✓. If `f_t/A_f` lands below the signal bandwidth you need, no choice of `β` rescues it — you need a faster op-amp, which is the practical meaning of Q8.

### Q28. (GATE-level) Compare the input offset error of a non-inverting gain-11 amp (`β = 0.09`, `V_os = 2 µV`) with a gain-1 buffer (`β = 0.5`, `V_os = 2 µV`).
**Answer:** Gain 11: `β = 1/11 = 0.0909`, so `V_out,os = V_os/β = 2e-6 × 11 = `**22.0 µV**. Gain 1 (buffer): `β = 0.5`, `V_out,os = 2e-6/0.5 = `**4.0 µV**. The gain-11 amplifier therefore has **5.5× more output offset** — 11× the gain buys 11× the offset, because offset scales with gain.
**Method:** `V_out,offset = V_os/β = V_os × A_f`, so the two numbers are just `A_f` scaled: gain 11 ⇒ 11×, gain 1 ⇒ 1×, ratio 11/2 ≈ 5.5 ✓. Note that **the loop gain `Aβ` does not appear at all** — `A` cancels. This is the classic trade: high gain improves *input-referred* accuracy but worsens *absolute output* offset, and only auto-zeroing, nulling or chopper stabilisation fixes the latter. Referred back to the input the two are identical (`V_os = 2 µV` either way), which is why datasheets always quote input-referred figures.

### Q29. (Moderate) Johnson noise of `1 kΩ`, `10 kΩ` and `100 kΩ` at 300 K, per √Hz. Which resistor dominates the noise of a `1 MΩ` input impedance amplifier?
**Answer:** `v_n = √(4kTR)`: `1 kΩ → `**4.1 nV/√Hz**; `10 kΩ → `**12.9 nV/√Hz**; `100 kΩ → `**40.7 nV/√Hz**. A `1 MΩ` source resistance alone contributes `√(4kTR) = `**129 nV/√Hz** — larger than all three feedback resistors combined. The `100 kΩ` feedback resistor dominates the *feedback-network* noise.
**Method:** `v_n = √(4kTR)` with `k = 1.38×10⁻²³ J/K`. Noise voltage grows as `√R`, so a decade of resistance is only `√10 = 3.16×` more noise. Two design lessons: (i) high-impedance sources are noise-dominated regardless of the feedback network, and (ii) feedback resistors should be kept *low* in value, which is why `10 kΩ` rather than `1 MΩ` is the usual choice — and why inverting amplifiers with `R_f = 1 MΩ` are so noisy (Q10, Q11).

### Q30. (GATE-level) An op-amp has `SR = 0.5 V/µs` and `f_t = 1 MHz`, and must produce a **10 V peak** sine. Compare the slew-rate limit with the small-signal limit for a gain of 11.
**Answer:** Slew-rate limit: `f_max = SR/(2π·V_pk) = 0.5e6/(2π × 10) = `**7.96 kHz**. Small-signal limit: `f_max = f_t/A_f = 1e6/11 = `**90.9 kHz**. So the **slew rate binds first**, by a factor of 11.4 — the amplifier is full-power-bandwidth limited long before it is small-signal limited, and the output would be a triangle wave, not a sine.
**Method:** Two independent ceilings: the GBW ceiling `f_t/A_f` (amplitude-independent) and the full-power bandwidth `SR/(2π V_pk)` (shrinks as you ask for more output). The minimum of the two is the real limit. The lesson matches Q8 exactly: **the dynamic performance of the closed loop is the *open-loop* part's dynamic performance divided by the loop gain** — feedback improves static accuracy and never rescues a part that cannot slew.

### Q31. (GATE-level) `A = 1×10⁵`, `β = 0.01`. What is `A_f` with **positive** feedback, and what happens?
**Answer:** `A_f = A/(1 − Aβ) = 1e5/(1 − 1000) = 1e5/(−999) = `**−100.1** — the magnitude is ~100 but the **sign is inverted**, i.e. the circuit is `1/β` with 180° of phase shift added, which is exactly the condition for oscillation. In practice the output slams to a rail or the circuit rings; the linear formula is only valid for `Aβ < 1` (gain *increases*: `A_f = A/(1 − Aβ) > A`).
**Method:** Flip the sign in the denominator: `A_f = A/(1 − Aβ)`. For `Aβ < 1` the gain is *enhanced* above `A` (this is how a positive-feedback RF amplifier and a regenerative detector work); for `Aβ ≥ 1` the formula diverges — the loop gain has reached unity, the Barkhausen condition is met, and the circuit oscillates. **Every oscillator and Schmitt trigger in `23-Schmitt-Trigger-Comparators.md` is this formula run to its limit.**

### Q32. (Moderate) State the phase-margin budget for a 2-pole amplifier and the resulting closed-loop `Q`.
**Answer:** Two poles contribute `-180°` at high frequency; the closed-loop denominator `1 + Aβ(s)` is 2nd order, so `Q` for the standard loop is set by the phase lag at the crossover. With a **dominant pole plus one nondominant pole**, the non-dominant pole is placed `≥ 10×` above crossover, giving a phase margin of roughly **60°** and a closed-loop `Q` of about **0.7** (Butterworth-like, no peaking). Place it `2×` above and the margin falls to ~30°, `Q` rises above 1 and the closed loop rings.
**Method:** The two numbers are the same statement: **phase margin and closed-loop `Q` are two views of the same denominator polynomial.** 90° ⇒ `Q = 0.5`, 60° ⇒ `Q ≈ 0.7`, 45° ⇒ `Q ≈ 1` (0 dB peak), below ~30° ⇒ `Q > 1.3` and visible overshoot. This is the bridge between this chapter and `22-Active-Filters.md`: the feedback amplifier is literally a filter, with `1/β` as its passband gain and the loop dynamics as its roll-off.

### Q33. (GATE-level) A designer claims: *"I used `A = 10⁶` and `β = 0.01` to get a rock-solid gain of 100."* Evaluate the claim and give the two numbers that actually bound the accuracy.
**Answer:** `Aβ = 1e4`, so `A_f = 1e6/10001 = `**99.99** — the claim is right, and the error is `1/10001 = `**0.01 %**. The two bounding numbers are: (1) **the loop gain `Aβ = 10⁴` (40 dB)**, which sets the error at `1/(1+Aβ) = 0.01 %`; and (2) **the tolerance of `R1` and `R_f`**, which is now the *only* thing that matters — a 0.1 % resistor pair gives up to 0.2 % of gain error, which is **20× worse** than the amplifier's contribution. Spending more on a higher-gain op-amp buys nothing; the design is `β`-limited, exactly as `29-Formula-Sheet.md` §29.10 states.
**Method:** Three moves. (1) Compute `Aβ`. (2) The residual gain error is `1/(1+Aβ)`. (3) Compare it with the resistor tolerance `Δ(1/β)/(1/β) ≈ ΔR1/R1 + ΔR_f/R_f`. When the loop-gain error is far below the resistor error — here 0.01 % vs 0.2 % — the amplifier is irrelevant and **only the feedback network matters**. This is the single most important design conclusion in the chapter, and it is the reason `A` is omitted from the answer to most "design a precision amplifier" questions.

---

## Trap box (exam-day killers)

- **Dropping the `+1`.** It is `1/(1 + Aβ)`, not `1/(Aβ)`. At `Aβ = 1000` that is 0.0999 %, not 0.1 % — small, but the 0.1 % is what separates a right answer from a nearly-right one.
- **Inverting `β` gives the wrong `A`.** `A = A_f/(1 − A_f β)` — the denominator **subtracts**. Writing `1 + A_f β` is the single most common algebra slip in this chapter.
- **Asking for `A_f > 1/β`.** **Impossible** at any open-loop gain; the formula returns a negative `A` (Q5). The achievable range is `0 < |A_f| < 1/β`, always.
- **"Feedback improves bandwidth."** It does the opposite: `BW_cl = (1 + Aβ)·BW_ol`, and `A_f·BW_cl = GBW` is *conserved*. The one thing feedback never improves is speed.
- **Forgetting the `+1` on the non-inverting gain.** `1 + R_f/R1`, not `R_f/R1`. This also means a non-inverting stage cannot have gain below 1 — the classic "how do I get 0.5 from a non-inverting amp?" answer is: you cannot.
- **Confusing noise gain with signal gain.** Inverting: signal `R_f/R1 = 9`, noise `1 + R_f/R1 = 10` (Q11). Non-inverting: both equal.
- **Claiming feedback reduces input offset.** It does not — `V_out,offset = V_os/β = V_os·A_f`, so offset *grows* with gain (Q28). Only the **input-referred** figure is unchanged.
- **Slew rate is not improved by feedback.** The full-power bandwidth `SR/(2π V_pk)` is an open-loop property; feedback makes it bind *sooner*, by `A_f` (Q30).
- **Confusing phase margin with closed-loop `Q`.** They are two views of one polynomial: 90° ⇒ `Q = 0.5`, 60° ⇒ `Q ≈ 0.7`, 45° ⇒ `Q ≈ 1` (Q32).
- **Mixing the four topologies' `1/β`.** Voltage-series `1 + R_f/R1`, voltage-shunt `R_f/R1`, current-series `1/R_s` (A/V), shunt-shunt `R_f` (V/A). Transconductance and transresistance are **not** dimensionless — the unit is the tell.
- **Sign of the inverting gain.** Do the arithmetic in magnitudes; the minus belongs to the topology, not to `β`.
- **Using `A₀` where `A` is meant.** `A` must be the *open-loop gain at the frequency in question*. At 10 kHz a 1 MHz-GBW op-amp's `A` is 100, not 10⁵, and `Aβ` collapses (Q27).

## Final recall drill (do in 60 seconds)

1. `A_f = A/(1 + Aβ)`. Deep negative feedback: `A_f → 1/β`.
2. Loop gain `Aβ`; gain error `= 1/(1+Aβ)`; bandwidth gain `= (1+Aβ)`.
3. `A = 1×10⁵`, `β = 0.01` ⇒ `Aβ = 1000`, `A_f = 99.9`, error 0.1 %.
4. `Aβ = 10` ⇒ 9.09 % error. `Aβ = 100` ⇒ 0.99 %. `Aβ = 1000` ⇒ 0.0999 %.
5. Loop gain in dB: `20log₁₀(Aβ)`. `Aβ = 1000` ⇒ 60 dB.
6. Accuracy to `ε` needs `Aβ ≈ 1/ε` — 0.1 % needs 60 dB of loop gain.
7. `A_f` can never exceed `1/β`. Full stop.
8. `A = A_f/(1 − A_f β)`.
9. `BW_cl = f_t/A_f`, and `A_f·BW_cl = GBW` is invariant.
10. Non-inverting gain `= 1 + R_f/R1`; cannot be < 1. Inverting `= −R_f/R1`.
11. Output offset `= V_os/β`; `R_out,cl = R_out/(1+Aβ)`; `R_in,cl = R1 + (R1∥R_f)`.
12. Distortion and output noise are both divided by `1 + Aβ`.
13. `Aβ = 1000` with `ΔA/A = 10 %` ⇒ `ΔA_f/A_f = 0.01 %`.
14. Positive feedback: `A_f = A/(1 − Aβ)`; `Aβ ≥ 1` ⇒ oscillation.
15. Four topologies' `1/β`: `1+R_f/R1`, `R_f/R1`, `1/R_s`, `R_f`.

---
