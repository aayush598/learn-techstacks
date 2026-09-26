# Master GATE-Level Question Bank + PYQs — Analog Circuits (ECE)

> **The idea in one line:** the single *main* file that combines full GATE-format
> questions (1-mark, 2-mark, MSQ, NAT — numerical answer type) with classic
> previous-year questions (PYQ) patterns, all solved with the exact GATE method.
>
> **How to use:** sit once a week, pick a paper-section (see index), time
> yourself like the real exam (1-mark ≈ 2 min, 2-mark ≈ 4 min), then verify.
> For more per-topic volume, drill the matching file in `Practice/`. Theory /
> formula recall lives in `32-Single-File-Cheatsheet.md`.

---

## Index (jump by paper section)

- **Section A — GATE 1-mark MCQs** (Q1–Q25): quick concept checks
- **Section B — GATE 2-mark MCQs** (Q26–Q45): single concept, heavier math
- **Section C — MSQ (multi-select)** (Q46–Q55): catch the "all that apply"
- **Section D — NAT numerical** (Q56–Q75): exact-number answers
- **Section E — Classic PYQ patterns** (Q76–Q90): year-wise, reworked figures
- **Section F — 15-minute full-paper drill** (Q91–Q100): mixed-all

---

# Section A — GATE 1-mark MCQs

### Q1. A silicon diode (`Vγ = 0.7 V`) in series with `R = 4.7 kΩ` and `V = 10 V`. The current is approximately:
- (A) 1.48 mA  (B) 1.98 mA  (C) 2.13 mA  (D) 2.5 mA
**Answer:** (B) 1.98 mA.
**Method:** `I = (10 − 0.7)/4.7k = 9.3/4.7 = 1.98 mA`.

### Q2. Full-wave rectifier: `Vm = 100 V`. `Vdc` (ideal) is:
- (A) 31.8 V  (B) 63.7 V  (C) 70.7 V  (D) 50 V
**Answer:** (B) 63.7 V.
**Method:** `Vdc = 2Vm/π`.

### Q3. In a voltage-source clamped positive clamper fed by `±6 V`, the output range is:
- (A) −6 to +6  (B) 0 to +12  (C) −12 to 0  (D) −6 to +12
**Answer:** (B) 0 to +12 V.
**Method:** positive clamper shifts the waveform so its bottom touches zero; amplitude 12 preserved.

### Q4. The op-amp ideal assumption that is INVALID when the op-amp saturates:
- (A) `v+ = v−`  (B) infinite gain  (C) infinite input R  (D) zero output R
**Answer:** (A) `v+ = v−`.
**Method:** the virtual short holds only in linear (negative-feedback, unsaturated) operation.

### Q5. `gm` of a BJT with `IC = 2 mA` (VT = 25 mV) is:
- (A) 40 mA/V  (B) 80 mA/V  (C) 20 mA/V  (D) 2 mA/V
**Answer:** (B) 80 mA/V.
**Method:** `gm = IC/VT = 2m/25m = 80 mA/V`.

### Q6. The Miller effect is exclusive to which amplifier configurations?
- (A) CB and CC  (B) CG and CD  (C) CE and CS  (D) all configurations
**Answer:** (C) CE and CS.
**Method:** Miller needs an inverting amplifier (180° phase shift across C).

### Q7. A current mirror copies a reference `1 mA` with `β = 99`. The output current is approximately:
- (A) 1 mA  (B) 0.98 mA  (C) 1.02 mA  (D) 0.5 mA
**Answer:** (B) 0.98 mA.
**Method:** `I_out = I_ref·β/(β+2) = 1·99/101 = 0.98 mA`.

### Q8. The bandwidth of an amplifier whose feedback factor `β` is decreased:
- (A) increases  (B) decreases  (C) unchanged  (D) doubles always
**Answer:** (B) decreases.
**Method:** less feedback (smaller β) ⇒ less gain reduction ⇒ less bandwidth extension (GBW ≈ const).

### Q9. Non-inverting amplifier `R1 = 2 kΩ`, `Rf = 18 kΩ`. Closed-loop gain:
- (A) −9  (B) 9  (C) 10  (D) −10
**Answer:** (C) 10.
**Method:** `1 + Rf/R1 = 1 + 9 = 10`.

### Q10. Wien bridge oscillator with equal R and C: the required op-amp gain is:
- (A) 29  (B) 3  (C) 1  (D) 2
**Answer:** (B) 3.
**Method:** attenuation = 1/3 at resonance ⇒ gain 3 to satisfy Barkhausen.

### Q11. Which oscillator uses the RC network (not LC)?
- (A) Colpitts  (B) Hartley  (C) Phase-shift  (D) Crystal
**Answer:** (C) Phase-shift.
**Method:** phase-shift and Wien are RC; Colpitts/Hartley are LC.

### Q12. The dominant pole sets the ... of the amplifier?
- (A) gain  (B) bandwidth  (C) input R  (D) output R
**Answer:** (B) bandwidth.
**Method:** the highest (lowest for low-frequency) pole sets −3 dB, i.e. bandwidth.

### Q13. CS amplifier with `RD = 5 kΩ`, `gm = 2 mA/V`, no load. Gain:
- (A) +10  (B) −10  (C) +2.5  (D) −2.5
**Answer:** (B) −10.
**Method:** `A_v = −gm·RD = −2m·5k = −10`.

### Q14. A MOSFET in triode with `k(V_GS−V_th) = 4 mA/V`: `rds(on)`?
- (A) 250 Ω  (B) 400 Ω  (C) 4 Ω  (D) 40 Ω
**Answer:** (A) 250 Ω.
**Method:** `rds(on) = 1/(k·Vov) = 1/4m = 250 Ω`.

### Q15. Source follower output resistance (gm = 5 mA/V, rLoad = 1 kΩ):
- (A) 200 Ω  (B) 1 kΩ  (C) 5 Ω  (D) ~5.2 kΩ
**Answer:** (A) 200 Ω.
**Method:** `Rout ≈ 1/gm = 1/5m = 200 Ω` (parallel with load for total).

### Q16. The DC input bias current of a BJT differential pair comes from:
- (A) gate  (B) base  (C) collector  (D) source
**Answer:** (B) base.
**Method:** `I_B = IC/β` on each side; MOS pairs have ~0.

### Q17. Which of these raises the input resistance of a CE amplifier?
- (A) removing the emitter bypass cap  (B) bypassing the emitter cap  (C) lowering RB  (D) removing RB
**Answer:** (A) removing the emitter bypass cap.
**Method:** unbypassed RE gives `Rin ∝ (β+1)(re+RE)` — much larger.

### Q18. An ideal op-amp integrator with `R=100 kΩ, C=1 µF`, input constant `+1 V`. Output slope:
- (A) +10 V/s  (B) −10 V/s  (C) +1 V/s  (D) −100 V/s
**Answer:** (B) −10 V/s.
**Method:** `dv_o/dt = −v_in/(RC) = −1/0.1 = −10 V/s`.

### Q19. Which of the following is NOT a reason for coupling capacitors in a BJT amplifier?
- (A) block DC  (B) isolate Q-points  (C) set low cutoff  (D) block AC
**Answer:** (D) block AC.
**Method:** coupling caps pass AC (chosen large so they "short" at signal frequencies) and block DC.

### Q20. A Schmitt trigger delivers hysteresis by using:
- (A) open loop  (B) positive feedback  (C) negative feedback  (D) large C
**Answer:** (B) positive feedback.
**Method:** the resistor divider from output to `+` input sets UT/LT and hysteresis.

### Q21. For 50% duty cycle triangle from a Schmitt+integrator, the threshold should be:
- (A) Vsat/2  (B) Vs  (C) 0  (D) Vsat
**Answer:** (C) 0 (zero threshold).
**Method:** zero-crossing threshold → symmetric triangle → 50% duty.

### Q22. Which topology is used in the input stage of a general op-amp?
- (A) CS  (B) CE  (C) differential amplifier  (D) cascode only
**Answer:** (C) differential amplifier.
**Method:** diff pair gives CMRR, matched V_BE and offset rejection.

### Q23. `A = 1000`, `β = 0.01`. The loop gain `A·β` is:
- (A) 1000  (B) 10  (C) 100  (D) 1
**Answer:** (B) 10.
**Method:** `Aβ = 1000×0.01 = 10`.

### Q24. The saturation of a BJT is signaled best by:
- (A) VCE ≈ VCC  (B) VCE ≈ 0.2 V  (C) collector current small  (D) base open
**Answer:** (B) VCE ≈ 0.2 V.
**Method:** in saturation both junctions forward; VCE(sat) ≈ 0.2 V.

### Q25. The minimum supply needed to bias a source follower of threshold 1 V to produce 2 V across RS (I_D·RS = 2):
- (A) 1 V  (B) 2 V  (C) 3 V  (D) 4 V
**Answer:** (C) 3 V.
**Method:** `V_DD − V_S ≥ |V_OV| + ... simple: VDD ≥ VGS + I_D·RS = Vth + Vov + V_out = 1 + 0 + 2 = 3 V`. (No overdrive needed headroom when gate= supply; minimum ≈ Vth + 2 = 3 V.)

---

# Section B — GATE 2-mark MCQs

### Q26. Voltage-divider biased CE amplifier: `V_CC=15, R1=100k, R2=50k, RE=1k, RC=4k, β=100, VBE=0.7`. The operating point IC and VCE:
- (A) 4.3 mA, 21.5 V  (B) 4.3 mA, −6.5 V  (C) 3 mA, 3 V  (D) 5 mA, −10 V
**Answer:** (B) 4.3 mA, −6.5 V (⇒ NOT a valid active point — the real conclusion is the transistor saturates).
**Method:** `VB = 15·50/150 = 5 V`, `VE = 4.3 V`, `IC ≈ 4.3 mA`, `VCE = 15 − 4.3·(4k+1k) = −6.5 V`. Since negative VCE is impossible, the assumed region fails — saturation traps you. GATE loves it.

### Q27. CE amplifier, `IC = 1 mA`, β = 100, VT = 25 mV: `gm`, `rπ`, and `re`.
- (A) 40, 2.5k, 25 Ω  (B) 40, 25, 25 Ω  (C) 2.5k, 40, 25k  (D) 25 m, 4k, 25 Ω
**Answer:** (A) 40 mA/V, 2.5 kΩ, 25 Ω.
**Method:** `gm=40 mA/V`, `rπ=β/gm=2.5k`, `re=VT/IE≈VT/IC=25 Ω`.

### Q28. Source follower drives `R_L=1 kΩ`; `gm = 2 mA/V`, `RS' = 1 kΩ`, λ = 0. Its gain:
- (A) 2  (B) 1  (C) 0.67  (D) −0.67
**Answer:** (C) 0.67.
**Method:** `Av = (RS∥RL)/(RS∥RL + 1/gm) = 500/(500+500) = 0.5` — recompute: `RS' = RS∥RL = 500 Ω`; `Av = 500/(500+500)=0.5`. Correct **answer (C) is 0.5** — the 0.67 number is the unloaded-with-RS-alone figure. GATE trap: load reduces it.

### Q29. BJT differential pair, tail current 2 mA, RC = 10 kΩ. Single-ended differential gain:
- (A) −200  (B) −400  (C) −100  (D) −800
**Answer:** (A) −200.
**Method:** half current = 1 mA → gm = 40 mA/V; single-ended `Ad = −gm·RC/2 = −40m·10k/2 = −200`.

### Q30. MOS current mirror: `(W/L)_2/(W/L)_1 = 5`, `I_ref = 0.5 mA`, λ=0. I_out:
- (A) 0.5 mA  (B) 2.5 mA  (C) 0.1 mA  (D) 5 mA
**Answer:** (B) 2.5 mA.
**Method:** `I_out = I_ref·(W/L)2/(W/L)1 = 0.5·5 = 2.5 mA`.

### Q31. Phase-shift oscillator with `R = 5 kΩ`, `C = 10 nF`. Frequency:
- (A) 3.18 kHz  (B) 1.3 kHz  (C) 650 Hz  (D) 9.55 kHz
**Answer:** (B) 1.3 kHz.
**Method:** `f = 1/(2πRC√6) = 1/(2π·50µ·2.45) ≈ 1.30 kHz`.

### Q32. Op-amp difference amplifier rejects common-mode perfectly if the resistor ratios are:
- (A) exactly matched  (B) roughly matched  (C) fixed 1:1  (D) none
**Answer:** (A) exactly matched, i.e. `R4/R3 = R2/R1`.
**Method:** CMRR → ∞ when the ratios match; mismatch is a GATE trap.

### Q33. Colpitts oscillator: `C1 = C2 = 1 nF`, `L = 1 mH`. Frequency:
- (A) 159 kHz  (B) 225 kHz  (C) 112 kHz  (D) 7.96 kHz
**Answer:** (A) 159 kHz.
**Method:** `C_eff = C1C2/(C1+C2) = 0.5n`; `f = 1/(2π√(1m·0.5n)) ≈ 225 kHz`. **The correct answer is (B) 225 kHz** — remember C_eff, not a single C.

### Q34. Feedback amplifier: `A = 100`, loop gain `Aβ = 9`. Closed-loop gain:
- (A) 9.9  (B) 10  (C) 11.1  (D) 100
**Answer:** (B) 10.
**Method:** `A/(1+Aβ) = 100/10 = 10`.

### Q35. A CE amplifier has `R_L = 4 kΩ`, `R_C = 4 kΩ`, `IC = 0.5 mA`. Its loaded gain (VT=25mV):
- (A) −80  (B) −40  (C) −160  (D) +40
**Answer:** (B) −40.
**Method:** `gm = 0.5m/25m = 20 mA/V`, `Av = −gm(R_C∥R_L) = −20m·2k = −40`.

### Q36. Two identical CS stages each gain −20 are cascaded. Overall gain:
- (A) −20  (B) +400  (C) −400  (D) +20
**Answer:** (B) +400.
**Method:** `(−20)·(−20) = +400` — sign flips twice.

### Q37. The unity-gain bandwidth of an op-amp = 1 MHz and midband gain 40 dB. The −3 dB bandwidth:
- (A) 10 kHz  (B) 100 kHz  (C) 1 MHz  (D) 40 kHz
**Answer:** (A) 10 kHz.
**Method:** 40 dB = 100×; `BW = f_T/A = 1M/100 = 10 kHz`.

### Q38. Non-inverting Schmitt trigger, `Vsat = ±10 V`, R1 = 2 kΩ, Rf = 8 kΩ. UT, LT, hysteresis:
- (A) +2, −2, 4 V  (B) +4, −4, 8 V  (C) +2, 0, 2 V  (D) +8, −8, 16 V
**Answer:** (A) +2, −2, 4 V.
**Method:** `Vth = ±Vsat·R1/(R1+Rf) = ±10·2/10 = ±2 V`, hysteresis 4 V.

### Q39. The transconductance of the diff pair: with tail current I_tail, BJT, each half gm =
- (A) `I_tail/2VT`  (B) `I_tail/VT`  (C) `2I_tail/VT`  (D) `I_tail/4VT`
**Answer:** (A) `I_tail/2VT`.
**Method:** IC per side = I_tail/2; gm = IC/VT.

### Q40. Which load in a CS amplifier delivers the highest voltage gain (all 4-Ω R_D equal to r_o)?
- (A) resistor RD  (B) current source (active load)  (C) diode-connected MOS  (D) resistor RL 0.5 things
**Answer:** (B) active (current source) load: gain ≈ gm·ro, beats gm·R_D.
**Method:** active load output impedance ≈ ro ⇒ max gain.

### Q41. For an inverting Schmitt trigger, as the input crosses UT going up, the output:
- (A) stays +  (B) goes to +Vsat  (C) goes to −Vsat  (D) floats
**Answer:** (B) goes to −Vsat in the inverting Schmitt (input at `−` pin). If the question uses "inverting Schmitt" the output at UT is −Vsat.
**Method:** confirm which pin the input is on. Inverting Schmitt: UT → output −Vsat.

### Q42. `C_M` of a CS with `Cgd = 3 pF`, `|Av| = 20`: input Miller capacitance:
- (A) 3 pF  (B) 63 pF  (C) 60 pF  (D) 66 pF
**Answer:** (B) 63 pF.
**Method:** `C_M = Cgd(1+|Av|) = 3·21 = 63 pF`.

### Q43. Relaxation oscillator: R1 = R2 = 10 kΩ, RC = 10 kΩ, C = 10 nF, Vsat = ±10 V. T:
- (A) 220 µs  (B) 200 µs  (C) 693 µs  (D) 110 µs
**Answer:** (A) 220 µs.
**Method:** `T = 2RC·ln(1 + 2R1/R2) = 2·(10k·10n)·ln(3) = 200µ·1.0986 = 219.7 µs`.

### Q44. Which of the following is an RC oscillator?
- (A) Colpitts  (B) Wein bridge  (C) Hartley  (D) Crystal-controlled
**Answer:** (B) Wein (Wien) bridge.
**Method:** Wien and phase-shift are RC; others LC/crystal.

### Q45. Maximum peak-to-peak uniform gain of a class-A CE with VCEQ = 8 V, VCE(sat) = 0.2 V, RAC = RDC:
- (A) 7.8 V  (B) 16 V  (C) 15.6 V  (D) 8 V
**Answer:** (C) 15.6 V.
**Method:** swing limited by `2·min(VCEQ−VCEsat, V_CC−VCEQ)`; for midpoint, `2·(8−0.2) = 15.6 V`.

---

# Section C — MSQ (all that apply)

### Q46. Which changes raise the input resistance of a CE amp? (select all)
- (A) larger R1∥R2 bias  (B) unbypassed RE  (C) no RE  (D) higher β
**Answer:** (A), (B), (D).
**Method:** `Rin = R1∥R2∥(β+1)(re+RE)`.

### Q47. The Miller effect applies to which (select all)?
- (A) CE  (B) CC  (C) CS  (D) CB
**Answer:** (A), (C).
**Method:** inverting amplifiers only.

### Q48. Which of these give a NON-inverted small-signal gain? (select all)
- (A) CG  (B) CS  (C) CC  (D) CB
**Answer:** (A), (C), (D).
**Method:** CG, CB, CC (follower) are non-inverting; CS and CE invert.

### Q49. A clamper's capacitor voltage changes if (select all)?
- (A) RC decreases a lot  (B) it never discharges  (C) input freq decreases  (D) diode is ideal
**Answer:** (A), (C).
**Method:** droop appears when RC isn't much larger than a period.

### Q50. Which are full-wave rectifiers? (select all)
- (A) half-wave  (B) center-tap  (C) bridge  (D) clamper
**Answer:** (B), (C).
**Method:** both produce 2f ripple and 2Vm/π.

### Q51. Which OSCILLATORS require gain ≥ 29 or other specific gain to start? (select all with Barkhausen)
- (A) Phase-shift (≥29)  (B) Wien (≥3)  (C) Colpitts  (D) Hartley
**Answer:** (A), (B) are the classical gain-criterion cases; (C), (D) also need Aβ ≥1 to start.
**Answer per exam expectation: (A), (B).**

### Q52. Which configurations have LOW (≈re or 1/gm) input resistance? (select all)
- (A) CB  (B) CG  (C) CC  (D) CS
**Answer:** (A), (B).
**Method:** CB/CG: looking into emitter/source ≈ re or 1/gm.

### Q53. Which change reduces the upper −3 dB (f_H) of a CE? (select all)
- (A) larger C_M (bigger C_cb)  (B) higher source resistance  (C) smaller gain  (D) larger f_T
**Answer:** (A), (B).
**Method:** Miller C and source R both multiply τ; smaller gain reduces f_H penalty? actually lowers it, so (C) is wrong.

### Q54. Which statement about an ideal op-amp are true? (select all)
- (A) v+ = v− in linear  (B) input R infinite  (C) output R zero  (D) infinite BW
**Answer:** (A), (B), (C), (D) — all ideal assumptions.

### Q55. Which circuits depend on positive feedback? (select all)
- (A) Schmitt trigger  (B) linear op-amp amplifier  (C) relaxation oscillator  (D) Wien bridge (with amplitude limiting)
**Answer:** (A), (C), (D).
**Method:** Schmitt: +ve fb; relaxation: comparator + feedback; Wien oscillator: feedback used for oscillation.

---

# Section D — NAT numerical

### Q56. Half-wave rectifier, `Vm = 80 V`, silicon diode (0.7 V): Vdc?
**Answer:** `(80 − 0.7)/π = 25.2 V`.
**Method:** `Vdc = (Vm − Vγ)/π`.

### Q57. Bridge rectifier, `Vm = 20 V`, silicon: Vdc?
**Answer:** `(20 − 1.4)·2/π = 11.85 V`.
**Method:** two diode drops.

### Q58. Emitter follower: `RE = R_L = 4 kΩ`, `re = 25 Ω`. Gain?
**Answer:** 0.994.
**Method:** `4k/(4k+25)`.

### Q59. CS stage: `gm = 1 mA/V`, `R_D = 10 kΩ`, `r_o = 100 kΩ`. Gain?
**Answer:** −9.09.
**Method:** `−gm·(RD∥ro) = −1m·9.09k`.

### Q60. Current mirror, `I_ref = 2 mA`, β = 49: I_out?
**Answer:** 1.92 mA.
**Method:** `2·49/51 = 1.92 mA`.

### Q61. Op-amp integrator, RC = 0.2 s, input +2 V, initial 0: v_o at 1 s?
**Answer:** −10 V.
**Method:** `vo = −(1/0.2)·2·1 = −10 V`.

### Q62. Source follower: gm = 8 mA/V: Rout?
**Answer:** 125 Ω.
**Method:** `1/gm = 1/8m = 125 Ω`.

### Q63. Wien bridge: R = 15.9 kΩ, C = 0.1 µF. Frequency (approx)?
**Answer:** 100 Hz.
**Method:** `1/(2π·15.9k·0.1µ) = 1/(2π·1.59m) ≈ 100 Hz`.

### Q64. Colpitts: `L=1 mH, C1=1 nF, C2=1 nF`. C_eff and f?
**Answer:** C_eff = 0.5 nF; `f = 1/(2π√(1m·0.5n)) = 225 kHz`.
**Method:** series combination.

### Q65. BJT mirror with `V_A = 50 V`, IC = 1 mA: output resistance?
**Answer:** 50 kΩ.
**Method:** `ro = V_A/IC`.

### Q66. Differential pair (BJT): tail 4 mA, RC = 10 kΩ, differential output Ad?
**Answer:** −400.
**Method:** gm per side 2mA/25m = 80 mA/V; `Ad = −80m·10k = −800`... recompute. `IC=2m, gm=2m/25m=80 mA/V`, `Ad = −gm·RC = −800`. **Answer −800.**
**Method:** careful — full tail splits; single-ended −400.

### Q67. Feedback: A = 300, β = 0.02: closed-loop gain?
**Answer:** `300/(1+6) = 42.86`.
**Method:** `A/(1+Aβ)`.

### Q68. Relaxation oscillator: RC = 100 µs, R1/R2 = 1: T?
**Answer:** 219.7 µs.
**Method:** `2RC·ln(3) = 200µ·1.0986`.

### Q69. Miller: C_cb 2 pF, gain 50, R_s 1 kΩ: f_H?
**Answer:** 1.56 MHz.
**Method:** `C_in = 2p·51 = 102 pF`, `f_H = 1/(2π·1k·102p)`.

### Q70. Schmitt trigger: Vsat = ±12 V, R1=1 kΩ, Rf=3 kΩ: hysteresis?
**Answer:** 6 V.
**Method:** `2·Vsat·R1/(R1+Rf) = 2·12·1/4 = 6 V`.

### Q71. Two identical stages, each gain −10; total gain?
**Answer:** +100.
**Method:** `(−10)²`.

### Q72. CE: IC = 0.5 mA, VT=25 mV, RC = RL = 2 kΩ: loaded gain?
**Answer:** −40.
**Method:** `gm=20m`, `Av=−20m·(2k∥2k)=−40`.

### Q73. BJT divider-bias: V_CC=12, R1=80k, R2=40k, RE=1k, β=100, VBE=0.7. Approx IC (valid approx)?
**Answer:** 3.3 mA.
**Method:** `VB=12·40/120=4 V`, `IE≈(4−0.7)/1k = 3.3 mA`. Approx valid since βRE=100k ≥ 10×R2=400k? no; it fails — exact answer slightly lower (Thevenin). GATE wants you to say "approximation not valid"; for approximate: 3.3 mA.

### Q74. HWR with cap filter: IL=20 mA, f=50 Hz, desired Vr=1 V. C?
**Answer:** `C = IL/(f·Vr)` use f_r=f for HWR: `20m/(50·1) = 400 µF`.
**Method:** `Vr ≈ IL/(f_r·C)`.

### Q75. Wien bridge with R = 10 kΩ, C = 15.9 nF: f_o?
**Answer:** 1 kHz.
**Method:** `1/(2π·10k·15.9n) = 1/(2π·159µ) ≈ 1001 Hz`.

---

# Section E — Classic PYQ Patterns (GATE EC, figures reworked)

> These follow the *exact pattern* of previous GATE EC papers (2009–2024 for
> Analog). Figures are recreated so you can re-solve without leaks; the number
> discipline is what matters.

### Q76. [GATE EC 2019 pattern] The op-amp inverting amplifier: R1 = 1 kΩ, Rf = 9 kΩ, vi = +1 V. v_o?
**Answer:** −9 V.
**Method:** `−(Rf/R1)·vi = −9·1 = −9 V`.

### Q77. [GATE EC 2017] A BJT has β = 100 and is in saturation with VCE = 0.2 V. If IC = 4 mA and RB such that IB = 0.1 mA — what is forced β?
**Answer:** 40.
**Method:** forced `β_f = IC/IB = 4m/0.1m = 40` — the point: it is *not* 100 in saturation.

### Q78. [GATE EC 2016] CS with active load (mirror) has `gm = 1 mA/V`, `r_o1 = r_o2 = 100 kΩ`. Gain?
**Answer:** −50.
**Method:** `Av = −gm·(ro1∥ro2) = −1m·50k = −50`.

### Q79. [GATE EC 2013] Two silicon diodes in series, `V = 10 V`, `R = 2.87 kΩ`. Current?
**Answer:** 3 mA.
**Method:** `(10 − 1.4)/2.87k = 8.6/2.87 = 3 mA`.

### Q80. [GATE EC 2015] Inverting Schmitt has nothing between inverting and output except Rf (to +), R1 (from + to GND). Vsat ±10, R1=1k, Rf=9k. UT?
**Answer:** +1 V.
**Method:** `V± = ±Vsat·R1/(R1+Rf) = ±10·1/10 = ±1 V`; UT = +1 when the input (on −) pushes the + node → for non-inv: UT=+1.

### Q81. [GATE EC 2020] A Wien bridge oscillator with R = C = 10 kΩ / 10 nF has frequency:
**Answer:** 1.59 kHz.
**Method:** `1/(2πRC) = 1/(2π·100µ) = 1592 Hz`.

### Q82. [GATE EC 2018] The input impedance of a common-base amplifier:
**Answer:** `re` (~25 Ω at 1 mA).
**Method:** CB input = emitter port.

### Q83. [GATE EC 2014] Two cascaded CE stages: first gain −40, second −5, less-than-you-think because of loading — the total (ideal, no loading): 
**Answer:** +200.
**Method:** sign flips twice, magnitudes multiply.

### Q84. [GATE EC 2021] An emitter-follower drives R_L = 1 kΩ, has (β+1)(re + RE∥RL) input — polarity check. Its voltage gain is:
**Answer:** slightly less than 1.
**Method:** `RE∥RL / (re + RE∥RL)`.

### Q85. [GATE EC 2012] PIV of a bridge rectifier with Vm=100 V:
**Answer:** 100 V.
**Method:** bridge PIV = Vm (center-tap = 2Vm for the same).

### Q86. [GATE EC 2022] A current mirror (MOS) with ratio 4 wants Iout = 2 mA: I_ref:
**Answer:** 0.5 mA.
**Method:** `I_ref = I_out/(W/L ratio) = 2/4`.

### Q87. [GATE EC 2010] The fastest-switching BJT drive uses:
**Answer:** very large base overdrive current (to clear stored charge) but must be carefully removed to avoid storage time → the answer that marks marks: remove base current quickly (negative bias) to shorten storage time.
**Method:** use Schottky-clamped or push-pull base drive.

### Q88. [GATE EC 2023] Common-mode gain of a diff amp with tail resistance R_tail and R_C: `Ac =`
**Answer:** `−RC/(2·R_tail)`.
**Method:** the defining formula — that (with infinite tail) is why current-source tail wins.

### Q89. [GATE EC 2011] Highest output resistance among mirror configurations:
**Answer:** cascode (or Wilson) current mirrors.
**Method:** stacking multiplies ro.

### Q90. [GATE EC 2015 2M] The op-amp ideal differentiator fed with `v_in(t) = 2 sin(2π·1000t)`, RC = 1 µs. Output amplitude:
**Answer:** `vo = −RC·dv/dt = −1µ·2·2π·1000·cos(...) = −12.57·cos(...) V` ⇒ amplitude 12.57 V.
**Method:** amplitude scales with ω.

---

# Section F — 15-minute full-paper drill (mixed, like a real seat)

### Q91. (1M) In a non-inverting op-amp amplifier R1=4k, Rf=36k, vi = 0.5 V. v_o?
**Answer:** +5 V.
**Method:** `(1+36/4)·0.5 = 10·0.5 = 5 V`.

### Q92. (2M) CE amp: `IC = 1 mA, β = 100, R1=100k, R2=25k, R_s = 1k`, VT=25mV. Midband gain `v_o/v_s` (RC=4k, RL=4k)?
**Answer:** −64.3.
**Method:** `gm=40m`, `Av=−40m·2k = −80`, `Rin = 20k∥2.5k = 2.22k`, `Avs = −80·2.22k/(2.22k+1k) = −80·0.689 = −55.1` — verify. `Rin=R1∥R2∥rπ = 20k∥2.5k = 2.222k`; `Avs = −80·2.222/3.222 = −55.2`. **Answer −55.2.**

### Q93. (1M) The CMRR of a diff pair defined as?
**Answer:** `20·log10(Ad/Ac)` dB.
**Method:** dB ratio of differential-to-common-mode gains.

### Q94. (2M) Relaxation oscillator: R1=5k, R2=5k, R=10k, C=10n, Vsat=±10 V. Thresholds and T?
**Answer:** thresholds `±10·5/10 = ±5 V`; `T = 2RC ln(1+2) = 200µ·1.0986 ≈ 220µs`.
**Method:** thresholds = Vsat·R1/(R1+R2); T formula.

### Q95. (2M) MOSFET cascode: gm1=gm2=2mA/V, ro1=ro2=100k: R_out of the cascode, idealised:
**Answer:** ~20 MΩ (gm·ro²).
**Method:** `R_out ≈ gm2·ro1·ro2 = 2m·(100k)² = 20 MΩ`.

### Q96. (2M) The lower −3dB of a CE set by C1 coupling with R_s + R_in = 2.5 kΩ, C1 = 1 µF:
**Answer:** 63.7 Hz.
**Method:** `1/(2π·2.5k·1µ) = 63.7 Hz`.

### Q97. (1M) A class-A amplifier Q-point optimized for max swing gives VCEQ = 7.5 V, V_CC=15 V, VCE(sat)=0.2 V. Peak clipped output (max, before clip)?
**Answer:** 7.3 V (VCEQ − VCEsat).
**Method:** max negative swing = VCEQ−0.2; positive = V_CC−VCEQ; the smaller wins.

### Q98. (1M) An emitter follower gain with re=25, RE∥RL=250 Ω:
**Answer:** 0.909.
**Method:** `250/275`.

### Q99. (2M) Difference amplifier wants `v_o = 5(v2 − v1)` with R2/R1 = 5 and both inputs now have exact ratios — which condition guarantees it?
**Answer:** `R4/R3 = R2/R1 = 5`.
**Method:** matched ratios for common-mode rejection.

### Q100. (2M) A HWR with ideal diode, Vm = 20 V, measures `Vdc` and ripple factor. 
**Answer:** Vdc = 6.37 V, γ = 1.21.
**Method:** `Vm/π`; HWR γ 1.21.

---

## After the bank — what to do next

- **Got ≥80%?** Go sit the `Practice/` per-topic drills to push weak chapters.
- **Under 50%?** Re-read the four core chapters: `07-BJT-Biasing.md`,
  `09-BJT-Amplifiers.md`, `14-MOSFET-Amplifiers.md`, `19-Op-Amp-Fundamentals.md`,
  then retake this paper cold.
- Formula cold on exam-eve: **`32-Single-File-Cheatsheet.md`**.

Good luck — this bank is the closest "single-file" proxy to sitting six years of
GATE EC Analog Circuits.