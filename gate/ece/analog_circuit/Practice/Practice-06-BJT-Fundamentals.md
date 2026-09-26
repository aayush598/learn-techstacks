# BJT Fundamentals — Practice (Learn by Solving)

> **The idea in one line:** this file teaches the whole BJT first course through
> 34 questions only — that a BJT is a *current-controlled* device obeying
> `I_C = β·I_B`, that `α` and `β` are two views of the same current split, that
> the three operating regions are decided purely by comparing `V_C`, `V_B`,
> `V_E`, and that the DC load line is just `V_CE = V_CC − I_C·R_C` drawn on
> paper.
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve the
> next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `06-BJT-Fundamentals.md` or `32-Single-File-Cheatsheet.md` only when you want
> the underlying theory.

## Concept box (what you must internalise)

- `I_E = I_C + I_B` (KCL at the transistor — charge conservation, always true).
- `α = I_C/I_E`, `β = I_C/I_B`, and they are locked together: `β = α/(1−α)`,
  `α = β/(β+1)`. Pick one, convert instantly.
- `I_E = (β+1)·I_B`, **not** `β·I_B`. The `+1` is the base current.
- NPN regions: active iff `V_C > V_B > V_E` with `V_BE ≈ 0.7 V`; PNP is the
  mirror image `V_E > V_B > V_C` with `V_EB ≈ 0.7 V`.
- Method: to classify a region, list `V_C`, `V_B`, `V_E` and compare. Never
  guess from the picture.
- Method: to test saturation, compare `β·I_B` against `I_C(sat) = (V_CC−0.2)/R_C`.
- Trap: `I_C = β·I_B` is an **active-region-only** law. In saturation `β` is
  forced down to `I_C/I_B < β` (the "forced β").

---

## Questions

### Q1. (Easy) A transistor has `α = 0.98`. What is its `β`?
**Answer:** `β = 49`.
**Method:** `β = α/(1−α) = 0.98/0.02 = 49`. Never convert α→β by multiplying —
always divide by `(1−α)`, because that `(1−α)` is exactly the base-current
fraction. Sanity check: α=0.98 means 2% of emitter current is base current, and
`1/β = 2%` ⇒ `β = 50`. Consistent.

### Q2. (Easy) `β = 100` and `I_B = 20 µA`. Find `I_C` and `I_E`.
**Answer:** `I_C = 2 mA`, `I_E = 2.02 mA`.
**Method:** `I_C = β·I_B = 100 × 20 µA = 2 mA`. Then `I_E = I_C + I_B =
2 mA + 0.02 mA = 2.02 mA`, or directly `I_E = (β+1)I_B = 101 × 20 µA`. The
`+1` term is only 1% here — that is exactly why `I_C ≈ I_E` is a legal
approximation, but the moment a question says "find `I_E`", write the exact form.

### Q3. (Easy) How do you tell an NPN symbol from a PNP symbol in a circuit diagram?
**Answer:** By the **emitter arrow**: NPN's arrow points *away* from the base
(out of the transistor, "NPN = Not Pointing iN"), PNP's arrow points *toward*
the base.
**Method:** Memorise "NPN = arrow iN" (out). The mnemonic encodes the physics:
an NPN emitter is n-type and *emits* electrons out of the device; a PNP emitter
is p-type and injects holes inward. Everything else (which terminal is called
"emitter") follows from the arrow.

### Q4. (Easy) Write the active-region voltage condition for a **PNP** transistor.
**Answer:** `V_E > V_B > V_C` with `V_EB ≈ 0.7 V`.
**Method:** Take the NPN rule `V_C > V_B > V_E` and reverse every inequality plus
the sign of the junction drop. Physically: the emitter must be the most positive
terminal (it supplies the carriers), the collector the least positive, and the
base sits 0.7 V below the emitter. Never mix `V_EB` and `V_BE` signs on a PNP.

### Q5. (Easy) An NPN has `V_BE = 0.4 V` and `V_CE = 5 V`. Which region?
**Answer:** Cutoff.
**Method:** The E-B junction needs ≥ ~0.5–0.6 V to conduct meaningfully. At
0.4 V the diode current is essentially zero (exponential law from
`06-BJT-Fundamentals.md` §6.5), so `I_C ≈ 0` no matter how positive the
collector is. Two separate tests, two separate junctions — here the E-B test
already decides it.

### Q6. (Easy) `β = 49`. What is `α`?
**Answer:** `α = 0.98`.
**Method:** `α = β/(β+1) = 49/50 = 0.98`. This is the exact inverse of Q1. Always
use `(β+1)` in the denominator, never `β` — using `β` gives 1.00, which is
physically impossible for a real transistor (α must be < 1).

### Q7. (Easy) `I_C = 1 mA` and `β = 200`. Find `I_B` and `I_E`.
**Answer:** `I_B = 5 µA`, `I_E = 1.005 mA`.
**Method:** `I_B = I_C/β = 1 mA/200 = 5 µA`. `I_E = I_C + I_B = 1 mA + 5 µA =
1.005 mA`. This is the **inverse** of the usual direction of travel: in a bias
problem you often know `I_B` and want `I_C`; here you know `I_C`. Write
`I_E = I_C(1 + 1/β) = 1 mA × 1.005`.

### Q8. (Easy) What is the current gain `β = 100` in decibels?
**Answer:** 40 dB.
**Method:** Voltage *and* current ratios use `20·log10`; power ratios use
`10·log10`. `20·log10(100) = 20 × 2 = 40 dB`. Remember this because a
voltage-gain question in dB (`08`/`09` chapters) uses the same rule.

### Q9. (Easy) `α = 0.995`. Find `β`, and state the base-current fraction.
**Answer:** `β = 199`; base current is 0.5% of emitter current.
**Method:** `β = 0.995/0.005 = 199`. The `1−α` term is the base fraction: 0.005,
i.e. `I_B/I_E = 1/β = 1/199`. High-α devices (199) are the ones you want in a
current mirror or a CB stage, because almost all the emitter current reaches the
collector.

### Q10. (Easy) `I_E = 2 mA` and `α = 0.98`. Find `I_C` and `I_B`.
**Answer:** `I_C = 1.96 mA`, `I_B = 40 µA`.
**Method:** `I_C = α·I_E = 0.98 × 2 mA = 1.96 mA`. Then `I_B = I_E − I_C =
2 − 1.96 = 0.04 mA = 40 µA`. This is the direct KCL route and it is safer than
converting to β and back. Cross-check: `β = 49`, `I_B = 1.96 mA/49 = 40 µA` ✓.

### Q11. (Moderate) Draw the DC load line for `V_CC = 10 V`, `R_C = 2 kΩ` (emitter
at ground, no `R_E`). Give both intercepts and the slope.
**Answer:** `V_CE` intercept = 10 V, `I_C` intercept = 5 mA, slope = `−1/R_C` =
−0.5 mA/V.
**Method:** Two easy end points, then the slope.
- `I_C = 0` ⇒ no drop across `R_C` ⇒ `V_CE = V_CC = 10 V`.
- `V_CE = 0` (hard saturation) ⇒ the whole supply is across `R_C` ⇒
  `I_C = V_CC/R_C = 10/2k = 5 mA`.
- Slope `dI_C/dV_CE = −1/R_C = −1/2000 = −0.5 mA per volt`.
Check the two intercepts against the slope: from (10 V, 0) to (0, 5 mA) the
slope is `5 mA / −10 V = −0.5 mA/V` ✓.

### Q12. (Moderate) Now add `R_E = 1 kΩ` in series (`V_CC = 12 V`, `R_C = 4 kΩ`).
What changes on the load line?
**Answer:** `V_CE` intercept stays 12 V; `I_C` intercept becomes
`12/(4k+1k) = 2.4 mA`; slope becomes `−1/(R_C+R_E) = −0.2 mA/V`.
**Method:** The governing equation is `V_CE = V_CC − I_C(R_C + R_E)`. The
`V_CE` intercept can never change — it is always `V_CC`, because zero current
means zero drop anywhere. The `I_C` intercept always uses the *total* series
resistance. Students lose marks by computing `V_CC/R_C` and forgetting `R_E`
(see `07-BJT-Biasing.md`).

### Q13. (Moderate) `V_CC = 10 V`, `R_C = 2 kΩ`, base grounded, `I_B = 40 µA`,
`β = 100`. Is the transistor active or saturated? Find `V_CE` if active.
**Answer:** Active; `V_CE = 2 V`.
**Method:** Two-step test.
1. Maximum current the circuit can deliver: `I_C(sat) = V_CC/R_C = 10/2k = 5 mA`.
2. What `β` asks for: `β·I_B = 100 × 40 µA = 4 mA`.
Since `4 mA < 5 mA` the transistor can deliver the demanded current, so
`I_C = 4 mA` and `V_CE = 10 − (4 mA)(2 kΩ) = 2 V`. Confirm with the region test:
`V_C = 2 V > V_B = 0.7 V > V_E = 0` ✓.

### Q14. (Moderate) Same circuit, but `I_B = 100 µA`. Now what?
**Answer:** Saturated. `V_CE ≈ 0.2 V`, actual `I_C = (10−0.2)/2k = 4.9 mA`, and
the effective (forced) `β = 4.9 mA/100 µA = 49`.
**Method:** `β·I_B = 10 mA` now *exceeds* `I_C(sat) = 5 mA`, so the transistor
cannot deliver — both junctions go forward and it behaves like a closed switch.
**The key idea:** in saturation `I_C = β·I_B` is false. The real `I_C` is set by
the external circuit (`V_CC`, `R_C`), and the device's gain has been *forced
down* to 49 instead of 100. Always report this "forced β" — GATE asks for it
directly.

### Q15. (Moderate) An NPN is biased at `V_C = 5 V`, `V_B = 3 V`, `V_E = 0 V`.
Which region?
**Answer:** Forward-active.
**Method:** Apply `V_C > V_B > V_E`: `5 > 3 > 0` ✓. In words: E-B is forward
biased (`V_BE = 3 V` ≫ 0.7 V) and B-C is reverse biased (`V_CB = 2 V > 0`). No
arithmetic needed — this is a pure ordering question.

### Q16. (Moderate) Same transistor, but `V_C = 1.5 V`, `V_B = 2 V`, `V_E = 0 V`.
**Answer:** Saturation.
**Method:** `V_C < V_B`, so the collector is *below* the base: the B-C junction
is **forward** biased (`V_BC = 0.5 V`) while E-B is forward (`V_BE = 2 V`). Both
junctions forward = saturation. The transistor is acting as a closed switch with
`V_CE ≈ 0.2 V`.

### Q17. (Moderate) `V_C = 0 V`, `V_B = 0 V`, `V_E = 0 V`. Region?
**Answer:** Cutoff.
**Method:** Every junction sits at 0 V, so no junction is even close to
forward biased. `I_C ≈ 0`. The trap here is students seeing "collector connected
to ground" and assuming conduction; without ~0.7 V across E-B there is no
current at all.

### Q18. (Moderate) A fixed-bias circuit holds `I_B = 20 µA` constant. With
`V_CC = 12 V`, `R_C = 2 kΩ`, find `V_CE` for `β = 50`, `150`, `200`. Comment.
**Answer:** `β=50 → I_C = 1 mA, V_CE = 10 V`; `β=150 → 3 mA, V_CE = 6 V`;
`β=200 → 4 mA, V_CE = 4 V`.
**Method:** `I_C = β·I_B`, then `V_CE = V_CC − I_C·R_C`. All three are active
(`V_C` = 10, 6, 4 V, all above `V_B = 0.7 V`). The Q-point wanders by a factor of
4 in current for a 4× spread in β. That is precisely why fixed bias has
`S = 1+β` and why every practical design uses feedback
(`07-BJT-Biasing.md`).

### Q19. (Moderate) With no base drive at all (`I_B = 0`) but `I_CBO = 1 µA` and
`β = 100`, what collector current flows?
**Answer:** `I_C = (β+1)·I_CBO = 101 µA`.
**Method:** `I_C = β·I_B + (β+1)·I_CBO`. The leakage current `I_CBO` is
amplified by `β` *and* the base current it creates is itself amplified, giving
`β+1`. This is the mechanism behind thermal runaway: `I_CBO` roughly doubles
every 10 °C, so at `I_CBO = 1 µA, β = 100` you already have 101 µA flowing with
the base open — and that 101 µA heats the device further.

### Q20. (Moderate) An NPN is measured at `V_C = 0 V`, `V_B = 1 V`, `V_E = 2 V`.
Which region, and what current-gain applies?
**Answer:** Reverse-active. The applicable gain is `β_rev` (a few units, typically
2–10), not the 50–300 forward `β`.
**Method:** Compare against the two junctions individually. E-B: `V_B − V_E = −1 V`
⇒ **reverse** biased. B-C: `V_B − V_C = +1 V` ⇒ **forward** biased. E-B reverse
plus B-C forward is the fourth (rarely used) region, reverse-active. It happens
if you ever connect a transistor backwards with the base held positive — hence
`β_rev` being tiny.

### Q21. (Moderate) `I_B = 5 µA`, `β = 100`, `V_CC = 5 V`, `R_C = 1 kΩ`, emitter at
ground. Find `I_C`, `V_CE`, and state the current-gain role.
**Answer:** `I_C = 0.5 mA`, `V_CE = 4.5 V`, active. The device is a
**current-controlled current source** with gain 100 (40 dB).
**Method:** `I_C = β·I_B = 100 × 5 µA = 0.5 mA`; `V_CE = 5 − (0.5 mA)(1 kΩ) =
4.5 V`. The phrase "current amplifier" means: change `I_B` and `I_C` follows
multiplied by β. Contrast with a FET, which is *voltage*-controlled — this is
the headline distinction in `06-BJT-Fundamentals.md` §6.1.

### Q22. (Moderate) `V_CC = 10 V`, `R_C = 1 kΩ`, `I_B = 20 µA`, `β = 100`. Give the
Q-point and the largest *symmetric* output swing before clipping.
**Answer:** Q = (`I_C = 2 mA`, `V_CE = 8 V`). Peak swing = 2 V, i.e. `V_CE` from
6 V to 10 V.
**Method:** Q-point: `I_C = 2 mA`, `V_CE = 10 − 2 = 8 V`. Then clip in **both**
directions and take the smaller limit:
- Toward cutoff: `ΔI_C = I_C(Q) = 2 mA` ⇒ `ΔV = I_C(Q)·R_C = 2 mA × 1 kΩ = 2 V`.
- Toward saturation: `ΔV = V_CE(Q) − V_CE(sat) = 8 − 0.2 = 7.8 V`.
Minimum is 2 V. A symmetric swing must be limited by the *smaller* distance;
here the Q-point sits far too close to cutoff.

### Q23. (GATE-level) NPN with `V_BB = 2 V`, `R_B = 100 kΩ` to `V_BB`,
`R_C = 2 kΩ`, `V_CC = 10 V`, `β = 100`, `V_BE = 0.7 V`. Region, `I_C`, `V_CE`.
**Answer:** `I_B = 13 µA`, `I_C = 1.3 mA`, `V_CE = 7.4 V`, **active**.
**Method:** The base loop is separate from the collector loop here — that is the
point of two-supply fixed bias.
1. `I_B = (V_BB − V_BE)/R_B = (2 − 0.7)/100 kΩ = 1.3/100k = 13 µA`.
2. `I_C = β·I_B = 1.3 mA`.
3. `V_CE = V_CC − I_C·R_C = 10 − (1.3 mA)(2 kΩ) = 10 − 2.6 = 7.4 V`.
4. Region test: `V_C = 7.4 V > V_B = 2 V > V_E = 0` ✓ active. Always do step 4 —
`06-BJT-Fundamentals.md` calls it the GATE check.

### Q24. (GATE-level) Identical circuit but `V_BB = 5 V`. Re-do it.
**Answer:** `I_B = 43 µA`; the *hypothetical* `β·I_B = 4.3 mA` cannot happen —
the transistor is **saturated**, `V_CE ≈ 0.2 V`, `I_C = 4.9 mA`.
**Method:**
1. `I_B = (5 − 0.7)/100k = 43 µA`.
2. Assume active: `I_C = 4.3 mA`, then `V_C = 10 − (4.3 mA)(2 kΩ) = 10 − 8.6 = 1.4 V`.
3. **Contradiction:** `V_C = 1.4 V < V_B = 5 V`, so B-C would be forward biased —
   the assumption is invalid.
4. Therefore saturated: `V_CE ≈ 0.2 V` and the circuit sets the current:
   `I_C = (10 − 0.2)/2 kΩ = 4.9 mA`.
The method to internalise: *assume active, then check*. If the check fails, the
circuit, not the device, sets `I_C`.

### Q25. (GATE-level) PNP with `V_EE = 10 V`, emitter resistor `R_E = 2 kΩ` to
`V_EE`, base resistor `R_B = 10 kΩ` to ground, `R_C = 1 kΩ` to ground,
`β = 100`, `V_EB = 0.7 V`. Find `I_B`, `I_C`, `V_EC` and the region.
**Answer:** `I_B = 9.19 µA`, `I_C = 0.919 mA`, `I_E = 0.928 mA`, `V_E = 8.14 V`,
`V_C = 0.92 V`, `V_EC = 7.22 V` — **active**.
**Method:** Write the emitter loop for a PNP exactly as you would the base loop
for an NPN, with `V_EB`:
`(V_EE − V_EB) = I_E·R_E + I_B·R_B` with `I_E = (β+1)I_B`
⇒ `I_B = (10 − 0.7)/(2 kΩ + 101 × 10 kΩ) = 9.3/1.012 MΩ = 9.19 µA`.
Then `I_C = 100 × 9.19 µA = 0.919 mA`, `I_E = 0.928 mA`,
`V_E = 10 − (0.928 mA)(2 kΩ) = 8.14 V`, `V_C = (0.919 mA)(1 kΩ) = 0.92 V`.
Region: `V_E = 8.14 > V_B = 0 > V_C = 0.92` ✓ active. `V_EC = 8.14 − 0.92 =
7.22 V`.

### Q26. (GATE-level) Same PNP, but `R_C = 2 kΩ`. Re-do the region check.
**Answer:** **Saturated**, `V_EC ≈ 0.2 V`, `I_C ≈ I_E ≈ 2.45 mA`.
**Method:** The *same* `I_B = 9.19 µA` still gives `I_C = 0.919 mA`, so
`V_C = (0.919 mA)(2 kΩ) = 1.84 V`. Now the ordering test fails:
`V_E = 8.14 V` is fine, but `V_C = 1.84 V > V_B = 0 V` means the B-C junction is
forward biased ⇒ saturation. With `V_EC ≈ 0.2 V` the two series resistors
(2 kΩ + 2 kΩ) take the rest: `I_C ≈ I_E = (10 − 0.2)/(4 kΩ) = 2.45 mA`.
Lesson: raising `R_C` alone can silently drive a PNP into saturation.

### Q27. (GATE-level) A datasheet says `V_BE(on) = 0.75 V` and
`V_CE(sat) = 0.05 V`. Is this transistor amplifying or switching, and what does
`V_BE = 0.75 V` tell you?
**Answer:** It is specified as a **switch**. `V_BE(on) ≈ 0.75 V` (higher than the
0.7 V amplification figure) and `V_CE(sat) = 0.05 V` (much lower than 0.2 V) are
both saturation-region numbers.
**Method:** Learn the two "families" of datasheet numbers. Amplifier parts quote
`V_BE ≈ 0.65–0.7 V` at a stated `I_C`, and `V_CE(sat) ≈ 0.2 V`. Switch parts
quote `V_BE(on) = 0.7–0.9 V` at a large `I_B` and `V_CE(sat) = 0.05–0.2 V` at
`I_C = I_B`. A `V_BE` of 0.75 V means the base current is large enough to
overdrive the device into saturation.

### Q28. (GATE-level) `V_CC = 10 V`, `R_C = 5 kΩ`, emitter grounded, and the base
is *held* at `V_B = 2 V` (a stiff source). `I_B = 20 µA`. Find the largest `β`
that still keeps the transistor active, and the `V_CE` at that limit.
**Answer:** `I_C(max) = (10 − 2)/5k = 1.6 mA`, so `β_max = 1.6 mA/20 µA = 80`;
`V_CE = 2 V` at the limit. For `β > 80` the transistor saturates.
**Method:** The edge of saturation is exactly `V_C = V_B` (B-C just zero-biased).
So set `V_C = V_B = 2 V`, solve the collector loop for the current the circuit
allows, and that current divided by `I_B` is the largest `β` the circuit can
tolerate. This is the "overdrive factor" question in reverse — real logic design
wants `β·I_B ≥ I_C(sat)`, amplifier design wants the strict opposite.

### Q29. (Moderate) A transistor has `α = 0.97`. (a) Find `β`. (b) What `I_B` is
needed for `I_C = 1.6 mA`? (c) What is `I_E`?
**Answer:** (a) `β = 32.3`; (b) `I_B = 49.5 µA`; (c) `I_E = 1.65 mA`.
**Method:** (a) `β = 0.97/0.03 = 32.33` — note `1−α = 0.03` is a 3% base fraction,
which is a *low*-β device. (b) `I_B = I_C/β = 1.6 mA/32.33 = 49.5 µA`.
(c) `I_E = I_C/α = 1.6/0.97 = 1.649 mA`. Cross-check by KCL:
`I_B = 1.649 − 1.6 = 0.049 mA = 49 µA` ✓. Working with α is often cleaner when
α is the given number — convert once, then stay in α.

### Q30. (GATE-level) Switch design: `V_CC = 5 V`, `R_C = 1 kΩ`, `I_B = 0.2 mA`,
`β = 50`. Region, `V_CE`, and the forced `β`.
**Answer:** Saturated. `I_C(sat) = (5−0.2)/1 kΩ = 4.8 mA`; `β·I_B = 10 mA ≫
4.8 mA`; `V_CE ≈ 0.2 V`; forced `β = 4.8 mA/0.2 mA = 24`.
**Method:** The switch designer's test is `β·I_B ≥ I_C(sat)` — you deliberately
*overdrive* by 2×. Forced β = 24 vs the device's 50, i.e. the device is running
at half its rated gain because it is being used as a switch, not a device. Note
that using `V_CC/R_C` instead of `(V_CC−0.2)/R_C` gives 5 mA and forced β = 25;
the 0.2 V matters when `V_CC` is small, which is exactly why switch datasheets
use low `V_CE(sat)`.

### Q31. (GATE-level) Temperature rises 10 °C. By what factor does `I_C` change if
`V_BE` falls 2 mV per °C and the bias current is set by a fixed source?
**Answer:** `ΔV_BE = −20 mV`, so `I_C` multiplies by `e^(20 mV/25 mV) = e^0.8 ≈ 2.2`
— the familiar "`I_C` roughly doubles every 10 °C" rule.
**Method:** Use the transfer characteristic from `06-BJT-Fundamentals.md` §6.5:
`I_C ∝ e^(V_BE/V_T)`, so `I_C2/I_C1 = e^(ΔV_BE/V_T)`. With `V_T = 25 mV`,
20 mV gives `e^0.8 = 2.23`. If the bias came from a resistor alone (fixed bias,
`S = 1+β`) the *sensitivity multiplies* by β and the effect is catastrophic —
which is the entire motivation for emitter/divider feedback in
`07-BJT-Biasing.md`.

### Q32. (GATE-level) Two transistors from the same lot, `I_B = 10 µA` for both,
`V_CC = 5 V`, `R_C = 1.2 kΩ`. `β_1 = 50`, `β_2 = 300`. Find both Q-points and
say whether both are usable as amplifiers.
**Answer:** `β_1`: `I_C = 0.5 mA`, `V_CE = 4.4 V`. `β_2`: `I_C = 3 mA`,
`V_CE = 1.4 V`. Both technically active, but their Q-points are 6× apart in
current.
**Method:** `I_C(sat) = (5−0.2)/1.2k = 4 mA`, so both `β·I_B` values (0.5 mA and
3 mA) are below it ⇒ both active. `V_CE = 5 − I_C·1.2 kΩ`: `5 − 0.6 = 4.4 V` and
`5 − 3.6 = 1.4 V`. Both sit *very* close to an edge, and the β=300 part is one
transistor swap away from saturation. A circuit whose Q-point depends on β is
not manufacturable — that is the punchline of `07-BJT-Biasing.md`.

### Q33. (GATE-level) Design the base current for the **largest possible
symmetric** swing: `V_CC = 10 V`, `R_C = 2 kΩ`, `β = 100`. Give `I_C(Q)`,
`V_CE(Q)`, `I_B`, and the available peak swing.
**Answer:** `I_C(Q) = 2.5 mA`, `V_CE(Q) = 5 V`, `I_B = 25 µA`; peak swing 4.8 V,
so the **symmetric** swing covers `V_CE` from `0.2 V` to `9.8 V`.
**Method:** For maximum symmetry the Q-point must sit **midway between the two
load-line intercepts**. The `V_CE` intercept is 10 V, so `V_CE(Q) = 5 V`, and
`I_C(Q) = (10 − 5)/2k = 2.5 mA`. Then `I_B = I_C/β = 25 µA`. Check both swing
limits, and note the *directions*: toward cutoff `I_C` falls 2.5 mA, so `V_CE`
**rises** by `2.5 mA × 2 kΩ = 5 V` (up to 10 V); toward saturation `V_CE`
**falls** by `5 − 0.2 = 4.8 V` (down to 0.2 V). The smaller limit is 4.8 V — the
saturation floor is why designers aim the Q-point slightly *above* mid-line.

### Q34. (Moderate) Sketch (describe) the `I_C` vs `V_BE` transfer
characteristic. By what factor does `I_C` change for a 60 mV rise in `V_BE`? For a
100 mV rise?
**Answer:** A very steep exponential, flat (≈0) below ~0.5 V, then rising
exponentially. `+60 mV ⇒ ×10`; `+100 mV ⇒ ×10^(100/60) = ×46.4`.
**Method:** From `06-BJT-Fundamentals.md` §6.5, `I_C ∝ e^(V_BE/V_T)`, so the
ratio for a step `ΔV` is `e^(ΔV/25 mV)`. `e^(60/25) = e^2.4 = 11.0 ≈ 10`
(exactly 10 for `ΔV = V_T ln 10 = 25 mV × 2.303 = 57.6 mV` — memorise
"**60 mV per decade**"). For 100 mV: `10^(100/60) = 46.4`. Consequences: (i) the
transfer curve is a poor *linear* element — hence all linearisation is done by
resistors/`R_E`; (ii) β is strongly temperature-dependent, so no design may
rely on it.

---

## Trap box (exam-day killers)

- `I_E = (β+1)·I_B`, never `β·I_B`. The extra 1% is free points if you write it.
- `α = β/(β+1)` — using `β` in the denominator gives the impossible `α = 1`.
- `I_C = β·I_B` is an **active-region-only** law. In saturation the circuit sets
  `I_C` and you must report the forced `β = I_C/I_B`.
- Saturation test: `β·I_B ≥ (V_CC − 0.2)/R_C`. Using `V_CC/R_C` shifts the answer
  slightly whenever `V_CC` is small.
- Active-region test is an *ordering*: `V_C > V_B > V_E` (NPN),
  `V_E > V_B > V_C` (PNP). `V_C = V_B` is the boundary, not "active with margin".
- `V_CE` load-line intercept is always `V_CC`; the `I_C` intercept uses
  `R_C + R_E` when `R_E` is present.
- dB for voltage/current ratios is `20·log10`; only power uses `10·log10`.
- Symmetric swing is limited by `min(I_C(Q)·R_ac, V_CE(Q) − V_CE(sat))` — never
  assume the supply-limited value.

## Final recall drill (do in 60 seconds)

1. `α = 0.99` ⇒ `β`? → *99.*
2. `β = 99` ⇒ `α`? → *0.99.*
3. `I_B = 20 µA`, `β = 150` ⇒ `I_C`, `I_E`? → *3 mA, 3.02 mA.*
4. `I_C = β·I_B` is valid in which region? → *forward-active only.*
5. NPN active region requires what ordering? → *`V_C > V_B > V_E`.*
6. `V_CE(sat)` ≈ ? → *0.2 V.*
7. `V_CC = 10 V`, `R_C = 2 kΩ`: `I_C` load-line intercept? → *5 mA.*
8. `V_BE = 0.4 V` ⇒ region? → *cutoff.*
9. `I_C = 1 mA`, `β = 200` ⇒ `I_B`? → *5 µA.*
10. NPN in saturation with `I_C = 4.9 mA`, `I_B = 100 µA` ⇒ forced `β`? → *49.*

---

Theory behind every answer: `06-BJT-Fundamentals.md`, `29-Formula-Sheet.md`
§29.3, `32-Single-File-Cheatsheet.md` §4.
