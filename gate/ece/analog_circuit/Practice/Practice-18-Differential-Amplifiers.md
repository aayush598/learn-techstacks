# Differential Amplifiers — Practice (Learn by Solving)

> **The idea in one line:** a differential pair must be solved as *two
> half-current amplifiers* plus a *stiff tail*: half current in each `gm`,
> `−gm·R_C` for a differential tap but `−gm·R_C/2` for a single-ended tap, and
> a common-mode gain of `−R_C/(2R_tail)` that decides the CMRR.
>
> **How to use:** solve each question fully before reading the answer. Cover the
> **Answer**/**Method** with paper, do it, then reveal. If you miss one, solve
> the next 3 in the file to lock the pattern. No need to read the chapter notes
> first — every concept is taught through the drill itself. Open
> `18-Differential-Amplifiers.md` or `32-Single-File-Cheatsheet.md` only when
> you want the underlying theory.

## Concept box (what you must internalise)

- `v_id = v1 − v2` (wanted), `v_icm = (v1 + v2)/2` (rejected). Write both
  before you touch a transistor.
- Each branch carries **`I_tail/2`** ⇒ `gm = (I_tail/2)/V_T` for BJT,
  `√(2k·I_tail/2)` for MOS. Using full `I_tail` in `gm` is the #1 error.
- `Ad(diff output) = −gm·R_C` (BJT); `Ad(single-ended) = −gm·R_C/2` — exactly
  half. MOS: `−gm·(R_D ∥ ro)`.
- `Ac ≈ −R_C/(2·R_tail)`; `CMRR = Ad/Ac`; `CMRR_dB = 20·log10(CMRR)`.
  Single-ended CMRR = `gm·R_tail`; differential-output CMRR = `2·gm·R_tail`.
- Differential mode: tail node is a **virtual ground**. Common mode: the tail
  fights back, so the output barely moves. Mixing these two pictures ruins
  every number.
- `R_in(BJT) = 2rπ`, `rπ = β/gm`. `R_in(MOS) = ∞`, and its gate current is
  **zero** — never write `I_G` in a MOS solution.
- Trap: a *perfect* tail gives `Ac → 0` and CMRR `→ ∞`; a plain resistor tail
  gives a terrible CMRR. That is the whole argument for mirrors (Chapter 17).

---

## Questions

### Q1. (Easy) The two inputs are `v1 = 1.5 V` and `v2 = 0.5 V`. Find
`v_id` and `v_icm`.
**Answer:** `v_id = v1 − v2 = 1.0 V`; `v_icm = (v1 + v2)/2 = 1.0 V`.
**Method:** Two formulas, no transistor work: `v_id = v1 − v2`,
`v_icm = (v1+v2)/2`. The check is that `v1 = v_icm + v_id/2 = 1 + 0.5 = 1.5` ✓.
(`18-Differential-Amplifiers.md` §18.1.)

### Q2. (Easy) `v1 = +0.1 V`, `v2 = −0.1 V`. Differential and common-mode
components?
**Answer:** `v_id = 0.2 V`; `v_icm = 0`. This is a **pure differential** input.
**Method:** Opposite signs ⇒ difference doubles, average vanishes. Contrast with
`v1 = v2 = 0.1 V` which is pure common mode. GATE loves "pure differential"
inputs for cancellation questions.

### Q3. (Easy) A differential pair has a tail current source of `2 mA`. What
current does each transistor carry at zero differential input?
**Answer:** `1 mA` each.
**Method:** Matched pair ⇒ equal split. The tail sets the *total*: `I_C1 +
I_C2 = I_tail`, so `I_C = I_tail/2` at `v_id = 0`. Everything downstream (`gm`,
`rπ`, `V_C`) uses this half value. (`18-Differential-Amplifiers.md` §18.7.)

### Q4. (Easy) Compare the differential input resistance of a BJT pair and a
MOS pair.
**Answer:** BJT: `R_in = 2rπ` (finite, e.g. `5 kΩ` for `β = 100`, `I_C = 1 mA`).
MOS: `R_in = ∞` (gate draws no current).
**Method:** In differential mode the two `rπ`s appear in **series** between the
inputs (`v_id` is applied across both), so `2rπ` — double, not half. A MOS
input stage therefore suits high-impedance sensors (thermocouples, strain
gages) because it draws no bias current at all.

### Q5. (Easy) A `100 mV` hum appears equally on both inputs of a
differential amplifier. Does the output see it?
**Answer:** Ideally no — it is pure common mode, and `Ac → 0` with an ideal
tail, so the output disturbance is zero.
**Method:** Ask first "is this `v_id` or `v_icm`?" Equal values ⇒ common mode
⇒ rejected in proportion to `1/CMRR`. Real rejection is
`v_icm/CMRR`, never exactly zero. (`18-Differential-Amplifiers.md` §18.4.)

### Q6. (Moderate) BJT pair, `I_tail = 2 mA`, `V_T = 25 mV`. Find `gm` of each
transistor, and state the `gm` you must **not** use.
**Answer:** `gm = (1 mA)/(25 mV) = 40 mS`. Do **not** use `I_tail/V_T = 80 mS`.
**Method:** `gm = I_C/V_T` with `I_C = I_tail/2 = 1 mA`; equivalently the handy
rule `gm = 40·I_C[mA]` mA/V. Direction check: doubling the tail current
*should* double `gm`, so 2 mA of tail ⇒ 80 mS only if all of it were in one
transistor — which it is not.

### Q7. (Moderate) In Q6 with `β = 100`, find `rπ` and the differential input
resistance.
**Answer:** `rπ = β/gm = 100/0.040 = 2.5 kΩ`; `R_in(diff) = 2rπ = 5 kΩ`.
**Method:** `rπ = β/gm = β·V_T/I_C` (also `rπ = (β+1)·re` with
`re = 25 mV/1 mA = 25 Ω`: `101 × 25 = 2.525 kΩ` ✓ consistent). Then double it,
because the two base–emitter paths are in series across `v_id`.

### Q8. (Moderate) BJT pair, `I_tail = 2 mA` (`gm = 40 mS`), `R_C = 10 kΩ`
per side, `V_CC = 12 V`. Find the **differential-output** gain
`v_o1 − v_o2` for `v_id`.
**Answer:** `Ad = −gm·R_C = −(40 mS)(10 kΩ) = −400`.
**Method:** Symmetry: the tail node is a virtual AC ground in differential
mode, so each half is a plain CE stage with `+v_id/2`; the outputs are
`−gm·R_C·(v_id/2)` and `+gm·R_C·(v_id/2)`, and the **difference** is
`−gm·R_C·v_id`. The `1/2` from the input and the `×2` from subtracting the two
outputs cancel. (`18-Differential-Amplifiers.md` §18.3.)

### Q9. (Moderate) Same circuit, but the output is taken from **one**
collector only. Find the gain from `v_id`.
**Answer:** `Ad(se) = −gm·R_C/2 = −200`.
**Method:** One collector sees only its own half of the drive:
`v_o1 = −gm·R_C·(v_id/2) = −200·v_id`. So a single-ended tap gives **exactly
half** the differential gain. Always ask "how many outputs does this circuit
have?" before quoting a gain. Trap: the chapter's `Ad(se)` is *not* the same
number as `Ad(diff)` — and CMRR must be computed with matching conventions
(`Ad(se)/Ac(se)` or `Ad(diff)/Ac(diff)`).

### Q10. (Moderate) Same pair, but the tail is a current source with
`R_tail = 500 kΩ`. Find the common-mode gain `Ac` (single-ended).
**Answer:** `Ac ≈ −R_C/(2R_tail) = −10 k/(2 × 500 k) = −0.01`.
**Method:** `Ac = −R_C/(2·R_tail)`. Reason: in common mode both halves swing
together, so each half sees `2·R_tail` of degeneration, and each contributes
half the differential gain of an ordinary CE stage. Sanity: `R_tail ≫ R_C`
⇒ `Ac ≪ 1`, i.e. the output barely moves. (`18-Differential-Amplifiers.md`
§18.4.)

### Q11. (Moderate) Using Q8–Q10, find the CMRR for the differential output and
in dB; then for the single-ended output and in dB.
**Answer:** Differential: `400/0.01 = 40,000` ⇒ `20 log10 4×10⁴ = 92.0 dB`.
Single-ended: `200/0.01 = 20,000` ⇒ `86.0 dB`.
**Method:** `CMRR = Ad/Ac`, `20 log10` for voltage ratios.
`log10(4×10⁴) = 4.602` ⇒ 92.04 dB; `log10(2×10⁴) = 4.301` ⇒ 86.02 dB. The
6 dB gap is exactly the factor 2 lost by throwing away one output — always use
matched conventions or the CMRR looks inconsistent.

### Q12. (Moderate) Q8's pair, quiescent: find the collector voltage and the
emitter-node voltage (inputs at 0 V, emitters to the tail).
**Answer:** `V_C = V_CC − (I_tail/2)·R_C = 12 − (1 mA)(10 kΩ) = 2.0 V`;
`V_E ≈ −V_BE = −0.7 V`.
**Method:** DC uses the **half current** again. Then check the region:
`V_C = 2 V > V_B = 0 > V_E = −0.7 V` ✓ forward active. If that check fails,
your `R_C` is too big or `I_tail` too small. (`18-Differential-Amplifiers.md`
§18.7.)

### Q13. (Moderate) MOS pair, `I_tail = 1 mA` (`I_D = 0.5 mA` per side),
`gm = 2 mA/V`, `R_D = 5 kΩ`, `ro = 100 kΩ`. Find the differential gain.
**Answer:** `R_D ∥ ro = (5 k × 100 k)/105 k = 4.762 kΩ`;
`Ad = −gm(R_D ∥ ro) = −(2 mA/V)(4.762 kΩ) = −9.52`.
**Method:** MOS version: `Ad = −gm(R_D ∥ ro)`. `ro` only *reduces* the gain
here (4.762 kΩ instead of 5 kΩ, −4.8 %) — it is the price of finite output
resistance. (`18-Differential-Amplifiers.md` §18.3, §18.6.)

### Q14. (Moderate) Same MOS pair with a mirror tail (`R_tail = ro`).
Estimate the CMRR and in dB.
**Answer:** `CMRR ≈ gm·R_tail = gm·ro = (2 mA/V)(100 kΩ) = 200` ⇒
`20 log10 200 = 46.0 dB`.
**Method:** `CMRR ≈ gm·R_tail` — the tail impedance directly scales the common
mode rejection. Note the number: 46 dB is *modest*, because MOS `gm` per mA is
small compared with BJT. That is the real reason BJT input stages are chosen
for high CMRR. (`18-Differential-Amplifiers.md` §18.5.)

### Q15. (Moderate) Q8–Q10's BJT pair, but `R_tail` is increased from `500 kΩ`
to `2 MΩ`. Recompute `Ac` and both CMRRs.
**Answer:** `Ac = −10 k/(2 × 2 M) = −0.0025`; differential CMRR
`= 400/0.0025 = 160,000` ⇒ `104.1 dB`; single-ended `= 200/0.0025 = 80,000` ⇒
`98.1 dB`.
**Method:** `Ac ∝ 1/R_tail`, so quadrupling `R_tail` divides `Ac` by 4 and
multiplies CMRR by 4 (`+12 dB`, since `20 log10 4 = 12.04`). Quick dB ladder:
×2 = +6 dB, ×4 = +12 dB, ×10 = +20 dB. Learn it — it turns every CMRR question
into one line of arithmetic.

### Q16. (Moderate) Q8–Q10's pair, but `I_tail` is raised from `2 mA` to
`4 mA` (same `R_C`, same `R_tail`). What changes?
**Answer:** `I_C = 2 mA` per side ⇒ `gm = 80 mS`; `Ad(diff) = −800`;
`Ad(se) = −400`; `Ac` **unchanged** at `−0.01`; differential CMRR
`= 80,000` ⇒ `98.1 dB`; single-ended `= 40,000` ⇒ `92.0 dB`.
**Method:** `Ad ∝ gm ∝ I_tail` but `Ac` depends only on `R_C` and `R_tail` —
so CMRR improves linearly with tail current (`CMRR = 2·gm·R_tail`). The single
big lesson: **more tail current buys gain and CMRR, and costs compliance
voltage and quiescent power.**

### Q17. (Moderate) A load `R_L = 10 kΩ` is connected from one collector to
ground. Find the single-ended gain now.
**Answer:** `R_C ∥ R_L = 5 kΩ`; `Ad(se) = −gm(R_C ∥ R_L)/2 = −(40 mS)(5 kΩ)/2 =
−100`, i.e. **half** the unloaded single-ended gain of `−200` in Q9.
**Method:** Load the collector resistance first, *then* divide by 2 for the
single-ended tap: `0.04 × 5000 = 200`, and `200/2 = 100`. If you instead
divided by 2 and then paralleled, you would wrongly get `R_C ∥ (R_L/2)`, which
is a different circuit. Order matters: modify the node, then apply the
single-ended factor.

### Q18. (Moderate) A sensor with `10 MΩ` output resistance drives a MOS
differential pair. Does the sensor see a loading error? Now substitute a BJT
pair with `rπ = 2.5 kΩ`.
**Answer:** MOS: no loading at all (`R_in = ∞`); the full sensor signal appears.
BJT: `R_in = 2rπ = 5 kΩ ≪ 10 MΩ` ⇒ voltage division gives
`5 k/(10 M + 5 k) ≈ 0.0005` ⇒ **0.05 %** of the signal gets through.
**Method:** Compare `R_in` with the source resistance: `R_in ≫ R_s` means no
loading. BJT input stages therefore need low-impedance sources (or a buffer);
MOS input stages happily accept megohm sources. (`18-Differential-Amplifiers.md`
§18.6.)

### Q19. (Easy) At the same tail current (`1 mA`), which input stage has the
larger `gm`: BJT or MOS? By roughly how much?
**Answer:** BJT. At `I_C = 0.5 mA`: `gm(BJT) = 0.5 mA/25 mV = 20 mS`. A typical
MOS device with `V_ov = 0.2 V` gives `gm = 2I_D/V_ov = 1 mA/0.2 V = 5 mS` —
about **4× smaller**.
**Method:** BJT `gm = I/V_T` grows linearly with current; MOS `gm = 2I/V_ov`
grows linearly too but needs a 0.2 V overdrive, so per mA BJT wins. Higher
`gm` at the same current ⇒ higher gain and higher CMRR for the same
microamps — the classic BJT-versus-MOS argument (`15-BJT-vs-MOSFET.md`).

### Q20. (Easy) Replace the tail current source with an **ideal** current
source (`R_tail = ∞`). What happens to `Ac` and the CMRR?
**Answer:** `Ac → 0` and `CMRR → ∞` (theoretically). The differential gain `Ad`
is unchanged (`−gm·R_C`).
**Method:** `Ac = −R_C/(2R_tail)`, so `R_tail → ∞` kills `Ac` while `Ad` (which
does not contain `R_tail`) is untouched. This is the idealised limit behind the
phrase "a stiff tail rejects common mode." Real circuits approach it with a
mirror (`17-Current-Mirrors.md`).

### Q21. (Moderate) Q8–Q10's pair, but the tail is a plain resistor
`R_E = 1 kΩ`. Find `Ac`, CMRR (single-ended) and CMRR in dB.
**Answer:** `Ac = −10 k/(2 × 1 k) = −5`;
`CMRR(se) = 200/5 = 40` ⇒ `20 log10 40 = 32.0 dB`.
**Method:** Same formula — the "tail resistance" is just `R_E` now. Compare
with 86 dB using a mirror: a resistor tail is a **54 dB** disaster. That single
comparison is the justification for every current-source tail in existence.

### Q22. (Easy) The tail mirror's output resistance halves (device change).
By how many dB does the single-ended CMRR drop?
**Answer:** `R_tail → R_tail/2` ⇒ `Ac` doubles ⇒ CMRR halves ⇒ drop of
`20 log10 2 = 6.02 dB`.
**Method:** CMRR is *linear* in `R_tail`, and dB is logarithmic, so halving
anything costs exactly `−3 dB` in amplitude terms but `−6 dB` for a voltage
ratio (which is what CMRR is — a voltage ratio, so `20 log10`). This is the
cleanest place GATE tests `20 log10` vs `10 log10`.

### Q23. (GATE-level) Full 2-mark problem. BJT pair: `V_CC = 15 V`,
`R_C = 5 kΩ` per side, `I_tail = 1 mA` (mirror tail, `V_A = 200 V`),
`β = 100`, `V_T = 25 mV`. Find `I_C`, `gm`, `rπ`, `R_in(diff)`, `Ad` (diff out),
`Ad` (single-ended), `Ac`, CMRR in dB, and the quiescent `V_C`.
**Answer:** `I_C = 0.5 mA`; `gm = 0.5 m/25 m = 20 mS`; `rπ = 100/0.02 = 5 kΩ`;
`R_in = 10 kΩ`; `Ad(diff) = −20 mS × 5 kΩ = −100`; `Ad(se) = −50`;
`R_tail = 200 V/1 mA = 200 kΩ`; `Ac = −5 k/(2 × 200 k) = −0.0125`;
`CMRR(diff) = 100/0.0125 = 8000` ⇒ `78.1 dB`;
`CMRR(se) = 50/0.0125 = 4000` ⇒ `72.0 dB`; `V_C = 15 − (0.5 m)(5 k) = 12.5 V`.
**Method:** Fixed pipeline: `I_tail → I_tail/2 → gm → rπ → R_in → Ad → R_tail →
Ac → CMRR → V_C`. Write the numbers in that order on the sheet; the only place
students hesitate is the `I_tail/2`. `log10 8000 = 3.903` ⇒ 78.06 dB;
`log10 4000 = 3.602` ⇒ 72.04 dB. Region check: `V_C = 12.5 V > V_B = 0` ✓.

### Q24. (GATE-level) MOS pair: `I_tail = 1 mA`, `V_ov = 0.2 V` for each
device, `λ = 0.01 V⁻¹`, `R_D = 10 kΩ`, `V_DD = 15 V`. Find `I_D`, `gm`, `ro`,
the differential gain, CMRR and dB, and `V_D`.
**Answer:** `I_D = 0.5 mA`; `gm = 2I_D/V_ov = 1 mA/0.2 V = 5 mS`;
`ro = 1/(λI_D) = 1/(0.01 × 0.5 mA) = 200 kΩ`;
`R_D ∥ ro = 10 k × 200 k/210 k = 9.524 kΩ`;
`Ad = −(5 mS)(9.524 kΩ) = −47.6`;
`CMRR ≈ gm·ro = (5 mS)(200 kΩ) = 1000` ⇒ `60.0 dB`;
`V_D = 15 − (0.5 mA)(10 kΩ) = 10.0 V`.
**Method:** MOS `gm = 2I_D/V_ov` (equivalently `√(2kI_D)`), `ro = 1/(λI_D)`.
Note `ro = 200 kΩ` was computed at the **half** current `0.5 mA` — but for the
*tail* device in Q23 the full `1 mA` was used. Same rule, different transistor.
`20 log10 1000 = 60 dB` exactly. (`18-Differential-Amplifiers.md` §18.6.)

### Q25. (GATE-level) A BJT pair and a MOS pair both run at `I_tail = 1 mA`,
and both have `V_A = 200 V` (`λ = 0.005 V⁻¹`). Compare their CMRR.
**Answer:** BJT: `gm = 0.5 m/25 m = 20 mS`, `R_tail = 200 V/1 mA = 200 kΩ`
⇒ `CMRR = gm·R_tail = 4000` ⇒ `72.0 dB`.
MOS (`V_ov = 0.2 V`): `gm = 5 mS`, `R_tail = 1/(0.005 × 1 mA) = 200 kΩ`
⇒ `CMRR = 5 m × 200 k = 1000` ⇒ `60.0 dB`.
BJT wins by 12 dB.
**Method:** `R_tail` is identical (same current, same Early resistance) — the
**only** difference is `gm`. So CMRR differences between BJT and MOS are a
*pure* `gm` effect. This is a favourite comparison question: identical
resistances, different `gm` ⇒ 12 dB. (`15-BJT-vs-MOSFET.md`.)

### Q26. (GATE-level) How large can `v_id` get before the BJT pair "steers"
(all the current into one branch)? Derive the value for a ratio of 100:1
between the branches.
**Answer:** `v_id = V_T·ln(I_C1/I_C2) = 25 mV × ln 100 = 25 m × 4.605 =
115 mV`.
**Method:** From `I_C = I_S·e^(V_BE/V_T)`, the two branch currents differ by
`I_C1/I_C2 = e^(v_id/V_T)`, so `v_id = V_T·ln(ratio)`. (MOS version:
`V_id,max ≈ √2·V_ov`, e.g. `√2 × 0.2 = 0.283 V` for `V_ov = 0.2 V`.) Beyond
this the pair behaves as a **switch**, which is how it is used as a comparator
or a multiplexer. (`18-Differential-Amplifiers.md` §18.8.)

### Q27. (GATE-level) Using Q23's pair, find the input common-mode range.
`V_CC = 15 V`, `R_C = 5 kΩ`, `I_tail = 1 mA`, and the tail goes to `−V_EE`.
**Answer:** Upper limit `V_icm,max = V_C = 12.5 V` (at the limit
`V_C = V_B`, the collector-base junction is at zero bias). Lower limit is set by
the tail: `V_icm,min ≈ −V_EE + V_CE(sat) + 0.7 V`; e.g. with `−V_EE = −5 V`,
`V_icm,min = −5 + 0.2 + 0.7 = −4.1 V`.
**Method:** Two constraints, always checked in this order: (1) `V_C > V_B`
(top end, uses the *quiescent* `V_C` you already computed in Q23);
(2) tail headroom (bottom end). Get `V_C` from the DC sweep first —
`V_C = V_CC − I_C·R_C`. (`18-Differential-Amplifiers.md` §18.8.)

### Q28. (GATE-level) Mismatched transistors give an input-referred offset of
`10 mV`. For Q23's pair, what DC output offset appears on the differential
output and on the single-ended output? How much of the supply does that shift
represent if the usable swing is `±12 V`?
**Answer:** Differential: `|Δv_o| = |Ad|·V_os = 100 × 10 mV = 1.0 V`
(12.5 V → 13.5 V or 11.5 V). Single-ended: `50 × 10 mV = 0.5 V`.
`1.0 V` of a 24 V span = **4.2 %**.
**Method:** Offset voltage is always multiplied by the *same* gain as the
signal: `Δv_o = V_os·|A|`. Do **not** use the closed-loop `1 + R_f/R_1` form
here — that is for op-amp input stages (see `Practice-19`). The percentage of
supply matters: it is the offset that eats your headroom.

### Q29. (GATE-level) In Q23's BJT pair, each base is driven by a source with
some finite impedance. Quantify the error from the input bias current
`I_B = 0.5 mA/100 = 5 µA` per base.
**Answer:** Each `5 µA` base current develops `I_B·rπ = 5 µA × 5 kΩ = 25 mV` of
input-referred offset; a **matched** pair's two currents cancel in `v_id`
(leaving only common mode, which the tail rejects), so the net differential
error is `I_os·2rπ` where `I_os = |I_B1 − I_B2|`. If `I_os = 0.5 µA`, the
residual is `0.5 µ × 10 k = 5 mV` ⇒ output `5 mV × 100 = 0.5 V`.
**Method:** Always split input-current problems into a **common** part
(cancels in a differential pair, rejected by CMRR) and an **offset-current**
part `I_os` (does not cancel; this is the real error). MOS inputs have both
`I_B = 0` and `I_os ≈ 0`. (`18-Differential-Amplifiers.md` §18.6.)

### Q30. (GATE-level) Output resistances of the two output options in Q23.
**Answer:** Differential output: `R_out = 2R_C = 10 kΩ`. Single-ended
(`R_C ∥ ro`): `R_out = 5 kΩ ∥ (200 V/0.5 mA = 400 kΩ) = 4.94 kΩ`.
**Method:** Two independent collectors in series-looking combination give
`2R_C`; one collector gives `R_C ∥ ro`. Include `ro` whenever you want a precise
number — the high CMRR story (`ro` of the tail is *large*) is different from the
`R_out` story (the collectors' `ro` only trims a few per cent).

### Q31. (GATE-level) "Why must a differential pair's tail be a current
source?" Answer quantitatively using Q23's numbers: what resistor tail would
be needed to match its CMRR, and is it buildable?
**Answer:** `CMRR(se) = gm·R_tail` ⇒ to get 4000 with `gm = 20 mS` we need
`R_E = 4000/0.020 = 200 kΩ` (equivalently `2·gm·R_tail = 8000` for the
differential tap ⇒ same `R_tail = 200 kΩ`). At `I_tail = 1 mA` that resistor
must drop `1 mA × 200 kΩ = 200 V`. Impossible on a 15 V supply.
**Method:** Two lines: `CMRR = gm·R_tail` → solve for `R_tail` → multiply by
`I_tail` to get the required drop, and compare with `V_EE`. The moment the
answer exceeds the supply, the mirror is not optional — it is *required*.
(`17-Current-Mirrors.md`, `18-Differential-Amplifiers.md` §18.4.)

### Q32. (GATE-level) A differential pair is used as a **switch**: the two
collectors feed a pair of resistors, and the pair steers the whole `1 mA` into
whichever input is high. Sketch the output behaviour for a square-wave `v_id`
of `±115 mV` and state the peak output voltage for Q23's `R_C = 5 kΩ`.
**Answer:** The `1 mA` current switches fully between branches, so the
low-side output is essentially `0 V` and the high-side output swings
`0 → I_tail·R_C = 1 mA × 5 kΩ = 5.0 V` (i.e. `v_o1 + v_o2` is a constant
5 V, and the outputs are complementary: one at 5 V, the other near 0). The
square wave at the input becomes a complementary pair of levels, with the
transitions limited by speed, not by the exponential "steering" curve.
**Method:** For a steering switch use `v_id ≥ V_T·ln(ratio)` (Q26) so the
residual current in the "off" branch is small (100:1 ⇒ 10 µA ⇒ 50 mV of
cross-talk on `R_C = 5 kΩ`). The sum of the two output voltages is nearly
constant — that invariance is a quick sanity check on any steered-pair answer.

### Q33. (GATE-level) Q23's pair, but `R_C1 ≠ R_C2` (`6 kΩ` and `4 kΩ`).
What is the common-mode gain now, and what does the mismatch do to CMRR?
**Answer:** `Ac = −(R_C1 + R_C2)/(4·R_tail)·1 = −(10 k)/(4 × 200 k) = −0.0125`.
Interesting: with `R_C1 + R_C2` fixed at 10 kΩ the average is unchanged, so
`Ac` is **unchanged** and so is the CMRR; what the mismatch destroys is the
*symmetry*, hence the **differential** gain cancellation: `Ad` becomes
`(gm/2)·|R_C1 − R_C2| = (0.020/2)(2 k) = 20` instead of `−50` single-ended
— the gain drops 2.5× while the input `v_id` still steers fully.
**Method:** Matched halves let the outputs cancel the common part; unequal
`R_C` make the common-mode movement *unequal*, so it survives. The useful
exam sentence: **resistor matching is what makes the differential
cancellation happen — and the same sentence appears for the 4-resistor
difference amplifier in `20-Op-Amp-Amplifiers-Summers.md`.**

### Q34. (GATE-level) A MOS differential pair uses the **body effect**
(`g_mb = 0.2·gm`, body tied to ground, sources at a negative voltage). How much
of the common-mode gain is due to the body effect rather than the tail, and
what would eliminate it?
**Answer:** The body effect makes each source current depend on its `V_S`, i.e.
it **adds** a common-mode path of its own; the tail term is
`−R_D/(2R_tail)` while the body term is
`−g_mb·R_D·(something of order 1)`. Order of magnitude: `g_mb/gm = 0.2`, so the
body-induced common-mode gain is of order `0.2·R_D`-ish, i.e. **the same order
as the differential gain itself** — a severe CMRR hit. Eliminating it requires
a **cascode / common-source tail** arrangement (folded cascode input stage) so
the sources stay at a near-constant voltage, or tying the body to the source.
**Method:** Rule: anything that makes the transconductance depend on a
common-mode voltage destroys CMRR. Two real culprits are (1) finite
`R_tail`, (2) body effect (`g_mb`). Body-cascode or a low-impedance source
node fixes it. (`18-Differential-Amplifiers.md` §18.6, `17-Current-Mirrors.md`
§17.5.)

---

## Trap box (exam-day killers)

- **Using `I_tail` instead of `I_tail/2` in `gm`.** Every gain, `rπ`, and `V_C`
  then comes out √2× too big.
- **Mixing `Ad` and `Ac` conventions.** `Ad(diff)/Ac(diff)` and
  `Ad(se)/Ac(se)` differ by 6 dB. Use the same output node in both.
- **Double `rπ` forgotten.** Differential input resistance is `2rπ` (the two
  paths in series across `v_id`), not `rπ`.
- **Writing a gate current in a MOS solution.** `I_G = 0`, always.
- **Using `R_C` alone for a MOS `Ad`.** It is `R_D ∥ ro`.
- **`ro` at the wrong current.** Collector `ro` uses `I_tail/2`; the tail
  device's `ro` uses `I_tail`.
- **Assuming a resistor tail is "fine".** A resistor tail is tens of dB worse
  than a mirror; Q21 and Q31 quantify the disaster.
- **Forgetting the output load before halving.** Load the node, *then* apply
  the single-ended `1/2`.
- **Region check skipped.** `V_C > V_B > V_E` for BJT, `V_DS ≥ V_GS − V_th` for
  MOS — the whole answer is wrong if the pair is in triode.
- **Sign of `v_id` output.** The differential tap `v_o1 − v_o2` **inverts**;
  flipping the tap flips the sign. GATE usually wants the magnitude.

## Final recall drill (do in 60 seconds)

1. `I_tail = 2 mA`: branch current? → *1 mA; `gm = 40 mS`.*
2. `Ad` for a differential output? → *`−gm·R_C`; single-ended? → *`−gm·R_C/2`.*
3. `Ac` with `R_C = 10 kΩ`, `R_tail = 500 kΩ`? → *`−0.01`.*
4. CMRR 40,000 in dB? → *92 dB.*
5. MOS pair `R_in`? → *∞ (zero gate current).*
6. BJT pair `R_in`? → *`2rπ`.*
7. Bigger `R_tail` → CMRR? → *increases linearly (= `2·gm·R_tail`).*
8. Max `v_id` to steer (BJT, 100:1)? → *`V_T ln 100` = 115 mV.*
9. MOS pair at `I_tail = 1 mA`, `V_ov = 0.2 V`: `gm`? → *5 mS (`2I/V_ov`).*
10. Tail as a resistor instead of a mirror? → *CMRR collapses (32 dB vs 86 dB).*

---

