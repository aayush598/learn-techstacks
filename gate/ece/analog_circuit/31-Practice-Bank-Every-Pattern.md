# Chapter 31 — GATE Practice Bank: Every Pattern, Variation, Technique (Q&A)

> **The idea in one line:** stop reading, start solving. This is a
> question-by-question, sequence-by-sequence drill that forces you to apply
> every concept from Chapters 00–30. Solve each question on paper *before*
> reading the answer. The questions are ordered so that each one builds the
> technique the next one needs.

---

## How to use this file (read this once)

1. Work strictly top to bottom. Later questions reuse the methods of earlier ones.
2. Cover the answer (everything after **A:**) with a paper/phone; write your
   solution, then reveal and compare *method*, not just the number.
3. If you miss a question, go back to the chapter named in **Ref:** and re-read
   only the relevant section, then attempt 3 more from that block.
4. Every block ends with a **"Method to memorise"** line that condenses the
   technique into one sentence — this is the exam-day recall hook.

---

# PART A — Diode Circuitry (variations GATE really asks)

## A1. Basic model selection

**Q1. A silicon diode with `Vγ = 0.7 V` carries a DC current set by a series**
**resistor. The diode current is `2 mA`. Dynamic resistance is?**
**Method:** `r_d = nV_T/I_D`; take `n = 1`, `V_T = 25 mV` unless stated.
**A:** `r_d = 25 mV/2 mA = 12.5 Ω.`

**Q2. Two silicon diodes in parallel, both with the same `Vγ`, driven by a**
**current source of 6 mA. Current in each?**
**Method:** identical drop → identical current, halves equally.
**A:** 3 mA each (matched). If `Vγ` differed, the lower-trip one hogs — GATE
rarely goes there, read the question.

**Q3. Three silicon diodes in series with a 3 kΩ resistor and a 9 V battery.**
**Current?**
**Method:** series drops add: `3×0.7 = 2.1 V`. KVL.
**A:** `(9 − 2.1)/3k = 2.3 mA`.

**Ref:** Ch 02. **Method to memorise:** series diodes add drops; use
`(V − ΣVγ)/ΣR`.

---

## A2. Series clipper patterns

**Q4. Positive series clipper, ideal, input `v = 10sin(ωt)`, load to ground.**
**Output waveform?**
**Method:** series diode conducts the positive half; negative blocked.
**A:** output = `+10 sin(ωt)` positive half, clamped to 0 in the negative half.

**Q5. Same circuit but silicon (`0.7 V`). Peak output?**
**A:** `10 − 0.7 = 9.3 V` during conduction. Negative half = 0.

**Q6. Positive series clipper with battery `+5 V` (ideal). Input ±12 V sine.**
**At what angle does the diode start conducting?**
**Method:** conducts when `v_in > 5`. `sin(θ) = 5/12`; conduction from θ to π−θ.
**A:** `θ = sin⁻¹(5/12) ≈ 24.6°`; conduction interval `24.6°–155.4°`.

**Ref:** Ch 03. **Method:** series clipper: diode passes the half-matched;
with bias: `v_in` must beat `bias(Vγ)`, conduction symmetric about π/2.

---

## A3. Shunt clipper patterns

**Q7. Positive shunt clipper (diode anode→output, cathode to gnd), ideal.**
**Input ±10 V. Output?**
**A:** positive half → diode ON → output ≈ 0; negative half → diode OFF →
output = input. Output is the negative half-wave.

**Q8. Biased shunt clipper: diode + 3 V battery to ground, ideal, input 5 V.**
**Output?**
**A:** 5 V > 3 V → diode ON → output = 3 V (clamped).
**Q9. Same circuit, input −5 V. Output?**
**A:** −5 V < 3 V → diode OFF → output = −5 V.

**Ref:** Ch 03. **Method:** shunt clipper shorts output during conduction —
output = clamp level when diode ON, follows input otherwise.

---

## A4. Two-level clippers

**Q10. Ideal two-level clipper: top clamp +4 V, bottom clamp −2 V. Input ±8 V**
**sine. Output in the middle (between clamps)?**
**A:** follows input (no diod conduction) when −2 < v < +4. Flat +4 above, flat
−2 below.

**Q11. Two Zener clipper: back-to-back, both `Vz = 5 V`, silicon 0.7. Positive**
**clamp level?**
**Method:** one Zener in breakdown + one forward → `Vz + 0.7`.
**A:** `5 + 0.7 = 5.7 V` positive; `−5.7 V` negative (symmetric here).

**Ref:** Ch 03. **Method:** Zener pair clamp level = `Vz + 0.7` per side.

---

## A5. Clamping patterns

**Q12. Positive clamper, ideal, sine ±6 V. Output range?**
**Method:** shift up so the bottom touches 0: offset = +6 V.
**A:** `0 to +12 V`.

**Q13. Negative clamper, silicon (0.7), sine ±6 V. Top value?**
**A:** bottom triggers? No — negative clamper: top clamped to `−0.7 V`;
range shift so top = −0.7 → output `−12.7 to −0.7 V`.

**Q14. Positive biased clamper with +2 V, ideal, sine ±4 V. Output range?**
**A:** bottom to +2 → range `+2 to +10 V`.

**Q15. A clamper's output amplitude equals the input amplitude. True or false?**
**A:** True — clampers shift DC level; shape/amplitude preserved.

**Q16. `R_L C` is small in a clamper. Between diode pulses the capacitor?**
**A:** discharges through R_L (droop) — output sags toward the reference.

**Ref:** Ch 04. **Method:** clamper = shift so one extreme hits the reference
`(Vγ or V_ref)`; amplitude unchanged.

---

## A6. Rectifier patterns (the numerical workhorses)

**Q17. HWR, ideal, peak 100 V, load 1 kΩ. V_dc? I_dc?**
**Method:** `V_dc = Vm/π`, `I_dc = V_dc/R`.
**A:** `31.8 V`, `31.8 mA`.

**Q18. Full-wave (bridge), ideal, peak 100 V. V_dc, V_rms, ripple factor?**
**A:** `63.7 V`, `70.7 V`, `γ = 0.48`.

**Q19. HWR mains 230 V rms → ideal. PIV?**
**Method:** rms → peak: `Vm = 230√2`.
**A:** `325.3 V` (PIV = Vm for HWR).

**Q20. Centre-tap FWR: each half `Vm = 40 V`. PIV per diode?**
**A:** `2·40 = 80 V`.

**Q21. Bridge rectifier (silicon), `Vm = 20 V`, load 1 kΩ. V_dc?**
**Method:** two diode drops: `(20 − 1.4)·2/π`.
**A:** `18.6·0.637 = 11.85 V`.

**Q22. Full-wave rectifier + C filter, load draws 10 mA, C = 50 µF, mains**
**50 Hz. Ripple voltage?**
**Method:** `V_r = I_dc/(f_r·C)`, `f_r = 2f = 100 Hz`.
**A:** `10m/(100·50µ) = 2 V`.

**Q23. To halve the ripple of an FWR-C filter by changing C alone: new C?**
**A:** double it — `V_r ∝ 1/C`.

**Q24. Rectification efficiency of full-wave ideal? Half-wave ideal?**
**A:** `81.2%`, `40.6%`.

**Q25. Which rectifier has ripple frequency = input frequency?**
**A:** Half-wave (FWR doubles it).

**Ref:** Ch 05. **Method:** waveform → average (`Vm/π` or `2Vm/π`, remember
half vs full), RMS (`Vm/2` or `Vm/√2`), ripple `V_r ≈ I_dc/(f_r·C)`, PIV = Vm
(HWR & bridge) or 2Vm (centre-tap).

---

# PART B — BJT (every biasing + small-signal pattern)

## B1. Biasing patterns

**Q26. Fixed bias: V_CC = 10 V, R_B = 400 kΩ, R_C = 2 kΩ, β = 100, V_BE = 0.7 V.**
**Q-point?**
**Method:** `I_B=(V_CC−V_BE)/R_B`, `I_C = βI_B`, `V_CE = V_CC − I_C·R_C`.
**A:** `I_B = 9.3/400k = 23.25 µA`; `I_C = 2.325 mA`; `V_CE = 10 − 4.65 = 5.35 V`; active ✓

**Q27. Fixed-bias stability factor S?**
**A:** `S = 1 + β` (e.g., 101 for β 100).

**Q28. Collector-to-base bias: V_CC=12, R_C=3k, R_B=150k, β=80, V_BE=0.7. I_C?**
**Method:** `I_B = (V_CC−V_BE)/(R_B + β·R_C)`.
**A:** `I_B = 11.3/(150k + 80·3k) = 11.3/390k = 28.97 µA`; `I_C = 2.32 mA`.

**Q29. Voltage-divider bias: V_CC=15, R1=100k, R2=50k, R_E=1k, R_C=4k, β=100.**
**Approximate I_C?** (Check: β·R_E = 100k ≥ 10·R2=500k ✓ approximate ok)
**Method:** `V_B = 15·50/150 = 5 V`, `V_E = 4.3 V`, `I_E = 4.3/1k`.
**A:** `I_C ≈ 4.3 mA`. `V_CE = 15 − 4.3−...`: V_CE = 15 − 4.3·(4k+1k) =
15 − 21.5 = −6.5 V → **saturated!** Q-point invalid; reduce R_C. *Lesson:* always
verify the Q-point half-line.

**Q30. What makes divider bias stable against β change?**
**A:** `V_B` is a divider constant; `I_C ≈ (V_B−V_BE)/R_E` — independent of β.
Large `R_E` → `S ≈ 1`.

**Ref:** Ch 07. **Method:** always (1) find I_C with the right bias formula,
(2) compute V_CE, (3) VERIFY active region — the exam's favourite trap.

---

## B2. Small-signal parameter patterns

**Q31. `I_C = 2 mA`, β = 200, V_T = 25 mV. gm, rπ, re?**
**A:** `gm = 2m/25m = 80 mA/V`; `rπ = 200/0.08 = 2.5 kΩ`; `re = 25m/2m = 12.5 Ω`.

**Q32. `I_C = 0.5 mA`, V_A = 50 V. ro?**
**A:** `ro = 50/0.5m = 100 kΩ`.

**Q33. Relationship `rπ`/`re`?**
**A:** `rπ = (β+1)·re ≈ β·re`.

**Ref:** Ch 08. **Method:** gm = I_C/V_T; rπ = β/gm; re = V_T/I_E; ro = V_A/I_C.

---

## B3. CE amplifier patterns

**Q34. CE with R_C = R_L = 4 kΩ, I_C = 1 mA. Gain?**
**Method:** `A_v = −gm·(R_C∥R_L) = −(1/25m·2k) = −80`.
**A:** `−80`.

**Q35. Same, but emitter degeneration R_E = 1 kΩ (unbypassed), I_C=1 mA, gm=40m.**
**A:** `A_v = −gm·R_C/(1+gm·R_E) = −(40m·4k)/(1+40) ≈ −3.9`.

**Q36. What happens to R_in when R_E is unbypassed?**
**A:** rises to `R_B∥(β+1)(re+R_E)` ≈ `R_B∥(β+1)·R_E` — much larger than `∥rπ`.

**Q37. CE with R1=100k, R2=25k, rπ=2k. R_in?**
**A:** `100k∥25k = 20k`; `∥2k ≈ 1.8 kΩ`.

**Q38. A CE stage is fed from a source R_s = 1 kΩ, R_in = 1.8 kΩ, and the**
**unloaded gain `A_v = −100`. Source-to-output gain?**
**Method:** `A_vs = A_v·R_in/(R_in + R_s)`.
**A:** `−100·1.8/2.8 ≈ −64.3`.

**Q39. Two identical CE stages each `A_v = −20` (properly loaded). Total gain?**
**A:** `(−20)·(−20) = +400` (two inversions → same phase as input).

**Ref:** Ch 09. **Method:** CE summary: `A_v = −gm·(R_C∥R_L)` (or −R_C/R_E
degenerated), R_in = R1∥R2∥rπ (or ∥(β+1)(re+R_E)), R_out = R_C.

---

## B4. CB and CC patterns

**Q40. CB amplifier, gm = 40 mA/V, R_C ∥ R_L = 2 kΩ. Gain, phase, R_in?**
**A:** `+gm·R = +80` (non-inverting), R_in ≈ re = 25 Ω.

**Q41. CC (emitter follower), R_E ∥ R_L = 4 kΩ, re = 25 Ω. Gain?**
**A:** `4k/(4k+25) ≈ 0.994` — just under 1.

**Q42. Emitter follower R_in (into base) with β=100, R_E∥R_L=4k?**
**A:** `(β+1)·(re + 4k) ≈ 100·4k = 400 kΩ` (plus bias R's in parallel).

**Q43. Identify: gain ≈ 1, very high R_in, very low R_out. Which stage?**
**A:** Common-collector (emitter follower) — the buffer.

**Ref:** Ch 09. **Method:** CB: +gm·R, R_in≈re. CC: gain≈1, R_in≈(β+1)R_E,
R_out ≈ re.

---

## B5. AC coupling / low-frequency patterns

**Q44. `C_E = 10 µF`, effective emitter resistance `re + R_B/(β+1) = 150 Ω`.**
**Bypass pole frequency?**
**Method:** `f = 1/(2π·C·R_eq)`.
**A:** `1/(2π·10µ·150) ≈ 106 Hz`.

**Q45. Removing the emitter bypass cap does what (three things)?**
**A:** midband gain drops, R_in rises, bandwidth widens.

**Q46. Which capacitors set the low cutoff of an amplifier?**
**A:** coupling caps (C1, C2) and the emitter/source bypass cap.

**Ref:** Ch 10. **Method:** each coupling/bypass cap → a high-pass pole at
`1/(2πCR_eq)`; bypass R_eq ≈ (re + R_B/(β+1)), not R_E.

---

# PART C — MOSFET (every biasing + small-signal pattern)

## C1. Region & parameter patterns

**Q47. NMOS: k=1 mA/V², V_th=1 V, V_GS=3 V, V_DS=5 V. Region? I_D?**
**Method:** `V_GS−V_th = 2`; `V_DS=5 > 2` → saturation; `I_D = ½k(2)² = 2 mA`.
**A:** Saturation, 2 mA.

**Q48. Same device, V_DS = 1 V. Region? I_D?**
**A:** Triode (`1 < 2`): `I_D = k[(2)(1) − 0.5] = 1.5 mA`.

**Q49. NMOS saturation, I_D = 0.5 mA, V_GS−V_th = 1 V. gm?**
**A:** `2·0.5m/1 = 1 mA/V`.

**Q50. `λ = 0.02`, I_D = 2 mA. ro?**
**A:** `1/(0.02·2m) = 25 kΩ`.

**Q51. Doubling I_D (square law) scales gm by?**
**A:** `√2`.

**Ref:** Ch 11, 13. **Method:** decide region first; params:
gm = k(V_GS−V_th) = 2I_D/(V_GS−V_th) = √(2kI_D); ro = 1/(λI_D).

---

## C2. MOSFET biasing patterns

**Q52. Divider bias NMOS: V_DD=10, R1=60k, R2=20k, R_D=2k, R_S=1k, k=1**
**mA/V², V_th=1 V. V_G?**
**A:** `V_G = 10·20/80 = 2.5 V`. (No gate current → divider exact.)

**Q53. Same circuit: approximate I_D by assuming V_GS ≈ 1.5 V?** (not given —
skip) Use exact: `I_D = ½k(V_G − I_D·R_S − V_th)²`, solve quadratically.
State the set-up: `I_D = 0.5k?(2.5 − I_D·1k − 1)²`.

**A:** Let x = I_D (mA): `x = 0.5(1.5 − x)²` → `x = 0.5(2.25 − 3x + x²)` →
`x² − 8x + 4.5 = 0` → `x = (8 ± √(64−18))/2 = (8±6.78)/2 = 7.39 or 0.61`.
Physical (V_GS>V_th) → `I_D ≈ 0.61 mA`.
Verify: `V_GS = 2.5 − 0.61 = 1.89 V > V_th` ✓; `V_DS = 10−0.61·3 = 8.17 V`,
`V_GS − V_th = 0.89` → saturation ✓.

**Q54. Drain-feedback NMOS: R_G from gate to drain, R_D=2k, k=1, V_th=1,**
**V_DD=8, I_D=1.5 mA. V_GS and V_D?**
**Method:** `V_D = V_DD − I_D·R_D = 8 − 3 = 5 V`; since `V_G = V_D`, V_GS = 5 V.
Check: `I_D = ½k(5−1)² = 8 mA ≠ 1.5` — inconsistency → the R_G feedback
stabilises at a different Q-point. Proper: solve `½k(V_DD − I_D·R_D − V_th)² = I_D`.

**Ref:** Ch 12. **Method:** gate voltage = divider (no current); V_GS = V_G −
I_D·R_S; solve quadratic; verify saturation.

---

## C3. MOSFET amplifier patterns

**Q55. CS: R_D=4k, R_L=4k, gm=2 mA/V. Gain?**
**A:** `−2m·2k = −4`.

**Q56. CS with unbypassed R_S=1k, gm=2m, R_D=4k. Gain?**
**A:** `−2m·4k/(1+2) ≈ −2.67` (≈ −R_D/R_S = −4 when gm·R_S ≫ 1 — verify scale).

**Q57. CG amplifier, gm=2m, R_D∥R_L=2k. Gain, R_in?**
**A:** `+4`, `1/gm = 500 Ω`.

**Q58. Source follower, R_S=1k, gm=2m. Gain, R_out?**
**A:** `1k/(1k+0.5k) = 0.67`, `R_out ≈ 1/gm = 500 Ω`.

**Q59. Which config has no Miller effect?**
**A:** CG (and CD/CC); CE/CS suffer it.

**Ref:** Ch 14–16. **Method:** same CJB formulas with R_E→R_S, rπ→∞,
re→1/gm. CS inverts; CG +; CD ≈1.

---

# PART D — Current Mirrors & Differential Pair

## D1. Mirror patterns

**Q60. BJT mirror, I_ref = 2 mA, β = 99. I_out?**
**A:** `I_ref·β/(β+2) = 2·99/101 ≈ 1.96 mA`.

**Q61. MOS mirror: (W/L)1=2, (W/L)2=8, I_ref=1 mA, λ=0. I_out?**
**A:** `1·(8/2) = 4 mA`.

**Q62. MOS mirror with λ: why does I_out ≠ I_ref even with matched W/L?**
**A:** `V_DS2 ≠ V_DS1` → `1+λV_DS` factors differ.

**Q63. Output resistance of a BJT current mirror (≈)?**
**A:** `ro = V_A/I_C` (e.g., 100 kΩ).

**Q64. Widlar mirror is used when?**
**A:** need a much smaller current than the reference; `I_out ≈ V_T/R_E ·
ln(I_ref/I_out)`.

**Q65. Minimum output voltage for a BJT mirror to stay active?**
**A:** ~`V_CE(sat) ≈ 0.2 V` — its compliance advantage.

**Ref:** Ch 17. **Method:** matched V_BE/V_GS → mirrored current; corrections:
BJT `β/(β+2)`, MOS `(W/L)` ratio and `λ(V_DS)` mismatch.

---

## D2. Differential pair patterns

**Q66. Tail current = 2 mA split between matched halves. Each collector's Q**
**current?**
**A:** `1 mA`.

**Q67. BJT diff pair, I_tail=2mA (1mA/half), R_C=10k, differential output. Ad?**
**A:** `−gm·R_C = −(1m/25m)·10k = −400`.

**Q68. Same pair, single-ended output (one collector). Ad?**
**A:** `−gm·R_C/2 = −200`.

**Q69. Finite tail R = 200 kΩ, R_C=10k. Ac? CMRR?**
**Method:** `Ac ≈ −R_C/(2·R_tail) = −10k/400k = −0.025`.
`CMRR = Ad/Ac = 400/0.025 = 16,000` → `20log10 ≈ 84 dB`.
**A:** Ac ≈ −0.025, CMRR ≈ 16000 (84 dB).

**Q70. Why does a current-source tail beat a resistor tail for the diff pair?**
**A:** current source has essentially infinite `R_tail` → Ac→0 → huge CMRR.

**Q71. MOS diff pair: input bias current? R_in?**
**A:** ≈ 0, ∞ (data-dependent tiny leakage in real life).

**Ref:** Ch 18. **Method:** half current in each branch; Ad = −gm·R_C (±/2 for
single-ended); Ac ≈ −R_C/(2R_tail); CMRR = Ad/Ac.

---

# PART E — Op-Amp Circuitry (the marks magnet)

## E1. Gain patterns

**Q72. Inverting: R1=2k, R_f=10k, v_in=−0.3 V. v_o?**
**A:** `−(−0.3)·(10/2) = +1.5 V`.

**Q73. Non-inverting: R1=1k, R_f=4k, v_in=0.2 V. v_o?**
**A:** `0.2·(1+4) = 1 V`.

**Q74. Which has higher input resistance: inverting or non-inverting amplifier?**
**A:** Non-inverting (≈ op-amp input R); inverting sees R1.

**Q75. Voltage follower output when v_in = 3 V, rails ±12?**
**A:** `+3 V` (unity buffer).

**Q76. Inverting amplifier with R1 = 0 (input resistor == 0)? Output?**
**A:** Gain `−R_f/0 → −∞` — every op-amp saturates; the real use: current-input
(transimpedance) amp. GATE gives v_in via a resistor; R1→0 breaks it.

## E2. Summer patterns

**Q77. Inverting summer: R1=R2=2k, R_f=4k, v1=1, v2=2. v_o?**
**A:** `−4k(1/2k + 2/2k) = −4(0.5+1) = −6 V`.

**Q78. Weighted summer: R1=1k, R2=2k, R_f=2k, v1=2, v2=1. v_o?**
**A:** `−2k(2/1k + 1/2k) = −2(2 + 0.5) = −5 V`.

**Ref:** Ch 20. **Method:** inverting = each input current summed at virtual
ground × R_f.

## E3. Integrator / differentiator patterns

**Q79. Integrator R=100k, C=1 µF. Input +1 V DC. Slop of output?**
**A:** `−1/(RC) = −10 V/s` (runs to rail).

**Q80. Integrator input square ±1 V, RC = 0.1 s. Output waveform?**
**A:** triangle, slope ±10 V/s.

**Q81. Differentiator C=1 µF, R=100k. Input square 0→+1 V. Output at edge?**
**A:** spike; ideal magnitude off-scale (−RC·dV/dt), practical limited by
slew rate.

**Q82. Why does the practical integrator need `R_f` across C?**
**A:** DC gain otherwise infinite → saturation & input offset drift blows out.

**Q83. Differentiator noise problem and fix?**
**A:** gain ↑ at high f (20 dB/dec); fix: series Rs with C input.

**Ref:** Ch 21. **Method:** integrator: `−(1/RC)∫`; differentiator: `−RC·d/dt`;
both practical forms add a resistor (R_f for int, Rs for diff).

---

## E4. Filter patterns

**Q84. 1st-order LPF from 1st-order integrator: R1=1k, R2=10k, C=1 nF. DC gain,**
**corner?**
**A:** `−10`; `f_c = 1/(2π·10k·1n) ≈ 15.9 kHz`.

**Q85. Order-1 roll-off? Order-2?**
**A:** 20 and 40 dB/dec respectively.

**Q86. Butterworth 2nd-order filter Q?**
**A:** `1/√2 ≈ 0.707`.

**Q87. Sallen-Key equal-C equal-R, unity gain. Q?**
**A:** `1/3`.

**Q88. Sallen-Key with unity components and an op-amp gain of exactly 3?**
**A:** Q→∞ → oscillation (Barkhausen) — the k→3 limit.

**Q89. Band-pass: centre 1 kHz, BW 100 Hz. Q?**
**A:** `1000/100 = 10`.

**Ref:** Ch 22. **Method:** LPF corner = 1/(2πRC); Butterworth Q=0.707;
Sallen-Key equal-RC unity Q=1/3; BPF Q = f_o/BW.

---

## E5. Schmitt & comparator patterns

**Q90. Comparator R_in? max gain? output states?**
**A:** likes open loop; output only ±V_sat; virtual short absent.

**Q91. Non-inv Schmitt: R1=2k, R_f=8k, V_sat=±10, V_ref=0. UT, LT, hysteresis?**
**A:** `Vth = ±10·(2k/10k) = ±2 V`; UT=+2, LT=−2, ΔV=4 V.

**Q92. Same but V_ref = +1 V. UT, LT?**
**A:** UT = 1+2 = 3 V; LT = 1−2 = −1 V; hysteresis still 4 V.

**Q93. Why does a Schmitt trigger reject noise at a threshold?**
**A:** once switched by UT, noise below UT can't un-trip it; it needs the LT
crossing — the dead band ends chatter.

**Ref:** Ch 23. **Method:** thresholds split by feedback: `V_ref ± V_sat·R1/R_f`.

---

# PART F — Feedback & Oscillators

## F1. Feedback patterns

**Q94. A=1000, β=0.1. A_f?**
**A:** `1000/(1+100) ≈ 9.9` (≈ 1/β = 10).

**Q95. Negative feedback effect on BW if A_f drops 10×?**
**A:** BW ×10 (gain-bandwidth constant conserved).

**Q96. Series-shunt (voltage-series) feedback: R_in, R_out?**
**A:** R_in ↑, R_out ↓.

**Q97. Which topology does the emitter/source-degenerated CE/CS use?**
**A:** current-series (series mixing at input) → R_in ↑, R_out ↑.

**Ref:** Ch 24. **Method:** A_f = A/(1+Aβ); series-mix ↑R_in, shunt ↓;
voltage-sample ↓R_out, current ↑.

## F2. Oscillator patterns

**Q98. Barkhausen conditions?**
**A:** `|Aβ| = 1` and `∠Aβ = 0°` at f_o.

**Q99. Phase-shift oscillator: R=10k, C=10 nF, R = 10 kΩ. f_o? Min gain?**
**A:** `f_o = 1/(2π·10k·10n·√6) ≈ 651 Hz`; min |A| = 29.

**Q100. Wien bridge equal R,C: f_o and gain requirement?**
**A:** `f_o = 1/(2πRC)`, gain = 3.

**Q101. Colpitts L=1m, C1=2n, C2=2n. f_o?**
**Method:** `C_eff = C1C2/(C1+C2) = 1n`.
**A:** `f_o = 1/(2π√(1m·1n)) ≈ 159 kHz`.

**Q102. Hartley L1=1m, L2=3m, C=1µ. f_o?**
**A:** `L_eff = 4m`; `f_o = 1/(2π√(4m·1µ)) ≈ 7.96 kHz` → ≈ 8 kHz.

**Q103. Relaxation osc: R=10k, C=10n, R1=10k, R2=10k. T, thresholds?**
**A:** `T = 2RC·ln(1+2·R1/R2) = 200µ·ln(3) ≈ 220 µs`; thresholds `±V_sat/2`.

**Ref:** Ch 25. **Method:** Barkhausen; phase-shift `1/(2πRC√6)`/29;
Wien `1/(2πRC)`/3; Colpitts series C, Hartley series L; relaxation
`2RC·ln(1+2R1/R2)`.

---

# PART G — Graphs, switch, and method drills

**Q104. BJT output char: family spacing ΔI_C for ΔI_B = 10 µA is 1.5 mA. β?**
**A:** `1.5m/10µ = 150`.

**Q105. Bode plot: gain falls 40 dB/dec beyond 10 kHz. Number of poles?**
**A:** 2.

**Q106. DC load line intercepts: (0, V_CC) and (V_CC/R, 0). What is the AC load**
**line relation to the DC line?**
**A:** steeper (R_AC = R_C∥R_L) and passes through the same Q-point.

**Q107. MOSFET switch "ON" region?**
**A:** triode (low R_ds), whereas amplifier uses saturation.

**Q108. BJT saturated: V_CE ≈? Test to confirm saturation?**
**A:** ≈ 0.2 V; confirm `I_B > I_C(sat)/β`.

**Q109. Storage time at BJT turn-off, why?**
**A:** minority charge in the base must be removed — slows turn-off vs MOSFET.

**Q110. Order of the master method for any transistor amplifier?**
**A:** DC Q-point → small-signal params → AC equivalent → solve gain/input/output.

**Ref:** Ch 26–28. **Method:** curves read slopes as gm/ro/β; saturation:
0.2 V + drive check; the 4-step method is always the plan.

---

# PART H — Integrated combos (the final exam style)

**Q111. A CE stage feeds a CC buffer. Stage 1 gain −50 with R_C=5k; buffer**
**R_in = 200k. What is R_C∥R_in effectively? Is loading significant?**
**A:** 5k∥200k ≈ 4.88k — very slight; buffer shields stage 1 (that's its job).
True loaded gain ≈ −gm·4.88k.

**Q112. Differential pair with active load (current mirror) — why is CMRR huge?**
**A:** active load ≈ ∞-internal-R current source → Ac→0; mirror balances the
load.

**Q113. A CS stage with source bypass removed: what three things change vs
bypassed?**
**A:** gain down (→ −R_D/R_S), R_in unchanged (R_G), bandwidth wider, linearity
better.

**Q114. Where does the Miller effect hit hardest: CE or CC? Why?**
**A:** CE/CS (inverting, feedback cap between input/output amplified by
`(1+|A|)`); CC/CD have no collector↔base gain path of the same sign.

**Q115. Why does the op-amp input stage need a differential pair?**
**A:** rejects common-mode (power-supply noise, DC offset), provides high CMRR
and matched-V_BE performance — the core of the op-amp.

**Q116. Cascade of a CS (gain −10) into a CG (gain +5) — cascode. Purpose?**
**A:** keeps the gain (−50) while killing Miller on the first stage → wider
bandwidth.

**Q117. Rectifier + filter → output has 120 Hz hum (full-wave from 60 Hz**
**mains). Where does hum come from?**
**A:** ripple at 2f isn't fully filtered; add more C or a regulator.

**Q118. What tests tell you a transistor is in saturation vs active (both
families)?**
**A:** BJT: V_CE ≈ 0.2 ↔ V_C > V_B; MOS: V_DS < ~V_GS−V_th ↔ ≥.

**Q119. Given a circuit, how do you decide it's CE/CB/CC in one glance?**
**A:** find the terminal tied to AC ground (cap to gnd / supply): that's the
"common" one.

**Q120. What does increasing the tail current do to a BJT diff pair's gm and Ad?**
**A:** raises gm (∝ I_C) and hence |Ad| — then CMRR (≈gm·R_tail) also rises.

---

## Final words for the practice bank

Done! If you solved all 120 in order you now carry **every pattern** the paper
can throw: the fixed set of formulas, the region checks, the Miller trick, the
hysteresis loop, the oscillator frequencies, the op-amp virtual short, and the
universal 4-step amplifier method. Tomorrow and two days before the
exam, re-do only the **Method to memorise** lines and the 5-question checks in
each chapter.

Next: **`32-Single-File-Cheatsheet.md`** — the entire subject on one page for
final-hour revision.