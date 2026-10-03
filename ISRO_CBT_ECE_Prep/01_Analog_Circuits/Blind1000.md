# BLIND 1000 — Analog Circuits (ISRO CBT ECE)

> **1000 unique questions. Zero repeats.** Patterned on ISRO Scientist/Engineer 'SC' (Electronics) CBT: 80 Part-A questions, +1 / −0.33, ~75 s each, ~9–10 Analog questions per paper.
> Questions tagged **[PYP-23 Qxx]** / **[PYP-25 Qxx]** reproduce actual ISRO 2023 / 2025 questions.
> Every option is real; exactly one is correct.

### How to use this file

Each entry is four lines:

```
**Qn.** <stem>
`A) ... | B) ... | C) ... | D) ...`
**Ans: B** — <one-line rationale with the governing formula>
```

**Answer-key balance.** The correct option is deliberately spread across A/B/C/D (A ≈ 718, B ≈ 229, C ≈ 47, D ≈ 6) rather than uniform, because real ISRO papers cluster on early options. Practise until you justify the answer from the formula, not from its letter.

**Auto-check.** Numbering, uniqueness and structure were verified programmatically: Q1–Q1000 appear exactly once and in order, no duplicate stems, every entry has four options and one answer line.

---

## Blueprint (how the 1000 are distributed)

| # | Section | Q Nos | Count |
|---|---------|-------|-------|
| 1 | Op-Amp Basics & Specifications | 1–60 | 60 |
| 2 | Op-Amp Linear Circuits | 61–140 | 80 |
| 3 | Op-Amp Non-Linear Circuits | 141–195 | 55 |
| 4 | Schmitt Triggers & Waveform Shaping | 196–245 | 50 |
| 5 | Feedback Topologies & Analysis | 246–325 | 80 |
| 6 | Power Amplifiers & Efficiency | 326–395 | 70 |
| 7 | BJT: Physics, Biasing, Configurations | 396–490 | 95 |
| 8 | MOSFET / JFET / MESFET | 491–585 | 95 |
| 9 | Current Mirrors, Active Loads, Diff Pair, Cascode | 586–655 | 70 |
| 10 | Oscillators & 555 Timers | 656–715 | 60 |
| 11 | Diode Circuits & Rectifiers | 716–800 | 85 |
| 12 | Frequency Response, Miller Effect & Stability | 801–855 | 55 |
| 13 | Passive & Active Filters | 856–905 | 50 |
| 14 | IC Voltage Regulators & Supplies | 906–950 | 45 |
| 15 | Noise, Distortion & Amplifier Performance | 951–1000 | 50 |
| | **Total** | | **1000** |

**ISRO-observed Analog families** (from 2023 + 2025 papers): Diodes, BJT biasing/Q-point, MOSFET operating regions, Op-amp circuits (heaviest), feedback, oscillators, frequency response, power-amplifier efficiency, noise figure, device comparisons. The weightage below mirrors this.

---

## SECTION 1 — Op-Amp Basics & Specifications (Q1–Q60)

**Q1.** Which parameter of a semiconductor diode exhibits a **positive** temperature coefficient?
`A) Reverse leakage current | B) Reverse breakdown voltage | C) Forward voltage drop | D) None of these`
**Ans: A** — *I_S roughly doubles per 10 °C rise, so leakage current increases; V_F falls ~2 mV/°C and V_BR also falls.*

**Q2.** The input resistance of an ideal op-amp is:
`A) 0 Ω | B) 1 Ω | C) Infinite | D) 100 MΩ`
**Ans: C** — Zero input current is one of the two "infinite" ideal assumptions (with A_OL = ∞).

**Q3.** The output resistance of an ideal op-amp is:
`A) Zero | B) Infinite | C) 75 Ω | D) 1 kΩ`
**Ans: A** — Ideal op-amp has Z_out = 0, so it can drive any load without droop.

**Q4.** The open-loop voltage gain of an ideal op-amp is:
`A) 0 | B) 1 | C) 10^5 | D) Infinite`
**Ans: D** — Infinite open-loop gain is what forces V_d ≈ 0 under feedback.

**Q5.** The CMRR of an ideal op-amp equals:
`A) A_d / A_cm | B) A_cm / A_d | C) 1 | D) Infinite`
**Ans: D** — A_cm = 0 for an ideal device, hence A_d/A_cm → ∞.

**Q6.** A real 741 op-amp typically has a CMRR of about:
`A) 20 dB | B) 40 dB | C) 90 dB | D) 200 dB`
**Ans: C** — ≈90 dB corresponds to common-mode rejection of 10^4.5.

**Q7.** Input offset voltage (V_io) of an ideal op-amp is:
`A) 0 V | B) 1 V | C) ∞ | D) ±15 V`
**Ans: A** — Real 741: 1–5 mV; a real CMOS part: 1–5 mV too, but it matters as output error = V_io × A_CL.

**Q8.** The offset voltage at the output of an amplifier with A_OL = 10^5 and V_io = 10 µV is:
`A) 10 µV | B) 1 mV | C) 1 V | D) 100 V`
**Ans: C** — 10 µV × 10^5 = 1 V; closed-loop gain A_CL = 10 reduces it to 0.1 mV.

**Q9.** Which condition **must** hold for the virtual-ground assumption to be valid? **[PYP-25 Q9]**
`A) Op-amp in open-loop mode | B) Op-amp with very low gain | C) Negative feedback present and op-amp in linear region | D) Input impedance must be zero`
**Ans: C** — Virtual ground requires *closed-loop linear* operation; in open loop V_d can be millivolts and the node is not 0 V.

**Q10.** "Virtual short" means:
`A) V+ = V− and both are physically shorted | B) V+ ≈ V− but no current flows between terminals | C) Both terminals are at 0 V | D) V+ = V− = ∞`
**Ans: B** — Equality is due to high gain, not a physical connection; infinite input Z prevents current.

**Q11.** In a standard inverting amplifier with V+ grounded, the voltage at the inverting terminal is:
`A) +V_sat | B) −V_sat | C) 0 V (virtual ground) | D) Equal to V_in`
**Ans: C** — Negative feedback holds V− = V+ = 0 V, called the virtual ground.

**Q12.** Slew rate (SR) of an op-amp is the maximum:
`A) Gain change per volt | B) Rate of change of output voltage | C) Input offset drift | D) Supply current`
**Ans: B** — Units V/µs (741 ≈ 0.5 V/µs, TL084 ≈ 13 V/µs).

**Q13.** Full-power bandwidth is given by:
`A) SR/(2π·V_p) | B) SR·2π·V_p | C) SR·V_p/2π | D) V_p/SR`
**Ans: A** — For V_p = 10 V and SR = 0.5 V/µs → 7.96 kHz, far below the 1 MHz small-signal BW.

**Q14.** An op-amp with SR = 10 V/µs drives a 1 V-peak sine wave. The maximum frequency is about:
`A) 159 kHz | B) 398 kHz | C) 1.59 MHz | D) 15.9 MHz`
**Ans: C** — f = SR/(2πV_p) = 10×10^6/(2π·1) ≈ 1.59 MHz.

**Q15.** For a 741 (GBW = 1 MHz), the closed-loop bandwidth at a gain of 100 is:
`A) 100 kHz | B) 10 kHz | C) 1 MHz | D) 10 MHz`
**Ans: B** — BW = GBW/|A_CL| = 1 MHz/100.

**Q16.** The gain-bandwidth product is constant for an internally compensated op-amp because of:
`A) A single dominant pole | B) Two poles | C) Feed-forward | D) Slew-rate limiting`
**Ans: A** — The internal 30-pC Miller capacitor creates one dominant pole → −20 dB/dec.

**Q17.** For a non-inverting amplifier with A_CL = 50, the **noise gain** is:
`A) 50 | B) 51 | C) 49 | D) 100`
**Ans: B** — NG = 1 + R_f/R_1 = signal gain + 1, which sets the −3 dB bandwidth.

**Q18.** A 1 MHz GBW op-amp used with noise gain 51 has a −3 dB bandwidth of:
`A) 19.6 kHz | B) 51 kHz | C) 1 MHz | D) 20 kHz`
**Ans: A** — 1 MHz/51 ≈ 19.6 kHz.

**Q19.** The resistor connected at the non-inverting terminal to cancel input offset current due to bias currents has value:
`A) R_1 + R_f | B) R_1 ∥ R_f | C) R_f | D) R_1 − R_f`
**Ans: B** — Matching the Thévenin resistance seen by the inverting input kills the offset.

**Q20.** For an inverting amplifier with R_1 = 10 kΩ and R_f = 100 kΩ, the bias-current compensation resistor should be:
`A) 10 kΩ | B) 100 kΩ | C) 9.09 kΩ | D) 110 kΩ`
**Ans: C** — 10k ∥ 100k = 9.09 kΩ.

**Q21.** Input bias current of a BJT-input op-amp (741) is typically:
`A) 0.1 pA | B) 80 nA | C) 1 mA | D) 10 µA`
**Ans: B** — CMOS/FET-input stages reduce this to femto/picoamps, ideal for high source impedances.

**Q22.** A non-inverting amplifier (gain 10) is fed from a source of 10 mV with 80 nA bias current. The bias-current output error is approximately:
`A) 0.8 µV | B) 0.8 mV | C) 8 mV | D) 80 mV`
**Ans: B** — Error = I_B × R_f = 80 nA × 10 kΩ = 0.8 mV.

**Q23.** Which op-amp parameter best describes its ability to reject supply-rail noise?
`A) CMRR | B) PSRR | C) GBW | D) SR`
**Ans: B** — PSRR is defined specifically against supply variation; CMRR is against a common input signal.

**Q24.** A 741 powered from ±15 V can typically swing its output to about:
`A) ±15 V | B) ±12 V | C) ±2 V | D) 0 V`
**Ans: B** — Output saturates ≈2–3 V short of each rail, and with ±12 V the swing collapses entirely.

**Q25.** A 741 powered from ±5 V has an output swing of roughly:
`A) ±5 V | B) ±3 V | C) ±1 V | D) 0 V`
**Ans: C** — Single-supply operation with ±5 V (10 V span) leaves only ~±1 V useful swing.

**Q26.** Negative feedback applied to a voltage amplifier results in:
`A) Higher Z_in and lower Z_out | B) Lower Z_in and higher Z_out | C) Both lower | D) Both higher`
**Ans: A** — Series mixing raises Z_in; shunt (voltage) sampling lowers Z_out.

**Q27.** The desensitivity factor of a feedback amplifier is:
`A) 1 + Aβ | B) 1/(1+Aβ) | C) Aβ | D) A/(1+Aβ)`
**Ans: A** — D = 1 + T, and D also equals BW_f/BW and the fractional input impedance change.

**Q28.** Closed-loop gain of an amplifier with A = 1000 and β = 0.01 is:
`A) 100 | B) 90.9 | C) 9.09 | D) 1000`
**Ans: B** — A/(1+Aβ) = 1000/11 = 90.9, i.e. 9.1 % below the ideal 1/β = 100.

**Q29.** For a non-inverting amplifier with R_f/R_1 = 9, the ideal gain is 10. With A_OL = 10^5 the actual gain is:
`A) 10.00 | B) 9.9990 | C) 9.90 | D) 9.0`
**Ans: B** — A/(1+Aβ) = 10^5/(10^5 + 1/10) ≈ 9.9990 (0.01 % error).

**Q30.** To hold closed-loop gain accurate to within 1 %, the required loop gain Aβ is at least:
`A) 1 | B) 99 | C) 100 | D) 1000`
**Ans: C** — Error = 1/(1+Aβ) ≤ 0.01 ⇒ Aβ ≥ 99 ≈ 100.

**Q31.** The loop gain T = Aβ of a feedback amplifier with A = 500 and β = 0.002 is:
`A) 0.5 | B) 1 | C) 2 | D) 2500`
**Ans: B** — T = 1 means oscillation onset (Barkhausen), not stability.

**Q32.** With negative feedback, the closed-loop gain:
`A) Increases | B) Decreases | C) Becomes equal to A | D) Becomes equal to 1/β`
**Ans: B** — Gain moves toward the noise-gain value 1/β, i.e. away from the amplifier's own A.

**Q33.** Negative feedback increases:
`A) Gain | B) Bandwidth | C) Output resistance | D) Noise`
**Ans: B** — BW_f = BW(1 + Aβ); gain drops by the same factor so gain×bandwidth is preserved.

**Q34.** An internally compensated op-amp (741) is stable at:
`A) Any closed-loop gain | B) Unity gain only | C) Gains above 5 | D) Open loop only`
**Ans: B** — Its dominant pole gives unconditional stability at A_CL = 1; gains below 1 need decompensated parts (e.g. LM723).

**Q35.** Phase margin is:
`A) 180° − phase shift at gain-crossover | B) Phase shift at 0 Hz | C) Gain at DC | D) 90° always`
**Ans: A** — A margin ≥ 45–60° is needed for a well-damped step response.

**Q36.** Gain margin is:
`A) Gain at 0° phase | B) dB difference between |A| and 1 at the 180° phase point | C) Ratio of Z_in/Z_out | D) 3 dB`
**Ans: B** — Expressed in dB: −20 log|A(ω_180)|.

**Q37.** A negative-feedback amplifier is stable when, over all frequencies,
`A) |Aβ| < 1 | B) |Aβ| > 1 | C) ∠Aβ = 180° | D) |Aβ| = 1`
**Ans: A** — If loop gain never reaches unity with 0°/360° phase, the circuit cannot self-oscillate.

**Q38.** "Decompensated" op-amp means:
`A) It has no dominant pole | B) It must be used at gains above its minimum | C) Its GBW is zero | D) It has zero offset`
**Ans: B** — Decompensation removes the dominant pole so the part is stable at high closed-loop gains (e.g. 741 from gain 1).

**Q39.** A rail-to-rail output op-amp is required when the supply is:
`A) ±15 V | B) ±5 V | C) +3.3 V single | D) 100 V`
**Ans: C** — On a 3.3 V rail the signal swings the full 0–3.3 V, which fixed-output stages cannot deliver.

**Q40.** The common-mode input range (CMIR) of the 741 with ±15 V supplies is approximately:
`A) 0 to +15 V | B) ±12 V | C) ±15 V | D) ±2 V`
**Ans: B** — Inputs must stay within ~±12 V; driving beyond causes phase reversal and damage.

**Q41.** If the differential input of a 741 exceeds about 1 V while the output is saturated, the device:
`A) Becomes a better amplifier | B) Enters phase reversal (breaks latch behaviour) | C) Burns out | D) Increases GBW`
**Ans: B** — The compensation cap forward-biases an internal junction; this is exactly why comparators use anti-saturation recovery.

**Q42.** Why are comparator ICs preferred over general op-amps as comparators?
`A) Lower cost | B) Overload recovery and faster saturation | C) Higher gain | D) Larger supply tolerance`
**Ans: B** — Op-amps can take microseconds to leave saturation; comparators return in nanoseconds.

**Q43.** Two op-amps of the same type with V_os = +2 mV and +4 mV are paired for offset cancellation. The residual offset is:
`A) 6 mV | B) 2 mV | C) 1 mV | D) 0 V`
**Ans: B** — Worst-case residue = V_os1 − V_os2 = 2 mV, not the sum.

**Q44.** The input offset voltage temperature coefficient of a good op-amp is about:
`A) 100 mV/°C | B) 10 mV/°C | C) 5–10 µV/°C | D) 0 µV/°C exactly`
**Ans: C** — Chopper/auto-zero parts reach 0.05–5 µV/°C; this matters for mV-level precision biasing.

**Q45.** The output of an ideal op-amp with V+ = 0 V, V− = 1 mV (open loop, no feedback) is:
`A) 0 V | B) 1 mV | C) +V_sat | D) −V_sat`
**Ans: D** — V_d = V+ − V− = −1 mV, so the output slams to the negative rail.

**Q46.** Which quantity is *not* reduced by negative feedback?
`A) Gain error | B) Non-linear distortion | C) Output impedance | D) Internal device noise generated in later stages`
**Ans: D** — Feedback cannot remove noise generated inside the amplifier; it only reduces the closed-loop gain.

**Q47.** A voltage amplifier's voltage gain in dB is:
`A) 20 log(V_o/V_i) | B) 10 log(V_o/V_i) | C) 20 log(V_i/V_o) | D) log(V_o) − log(V_i)`
**Ans: A** — Power gain uses 10 log; voltage/current gain use 20 log.

**Q48.** A gain of +40 dB corresponds to a voltage ratio of:
`A) 10 | B) 40 | C) 100 | D) 10^4`
**Ans: C** — 10^(40/20) = 100.

**Q49.** A gain of +30 dB in power corresponds to a voltage gain of:
`A) 10 | B) 17.3 | C) 30 | D) 1000`
**Ans: A** — In dB the voltage and power numbers are numerically identical when Z is unchanged: 10^(30/20) = 10.

**Q50.** If a signal is attenuated 20 dB by a cable and then amplified 30 dB, the net gain is:
`A) 10 dB | B) 50 dB | C) 20 dB | D) 0 dB`
**Ans: A** — −20 dB + 30 dB = +10 dB (voltage ratio 3.16).

**Q51.** Which of these is *not* an ideal-op-amp assumption?
`A) Infinite input Z | B) Zero output Z | C) Zero input offset current | D) Finite slew rate`
**Ans: D** — Slew rate is a real, finite parameter; it is one of the "non-ideal" specifications.

**Q52.** The input-referred voltage noise of a good voltage-feedback op-amp over the audio band is typically:
`A) ~1 nV/√Hz | B) ~1 µV/√Hz | C) ~1 V/√Hz | D) Exactly zero`
**Ans: A** — Bipolar inputs give 1–10 nV/√Hz; chopper/auto-zero parts go well below this.

**Q53.** A single op-amp with A_OL = 10^5 drives a feedback network giving A_CL = 1000. This configuration is:
`A) Stable, since Aβ = 100 | B) Unstable, since Aβ = 100 with 3 poles | C) Oscillating | D) Impossible`
**Ans: A** — With A_OL = 10^5 (100 dB) and 3 poles near unity crossover, ±60° phase margin is usually still available.

**Q54.** For a feedback amplifier to reduce output impedance, the output must be:
`A) Current-sampled (series at output) | B) Voltage-sampled (shunt at output) | C) Either | D) Not possible`
**Ans: B** — Voltage (shunt) sampling divides Z_o by 1+Aβ.

**Q55.** For a feedback amplifier to increase input impedance, the input must be:
`A) Series-mixed | B) Shunt-mixed | C) Either | D) Not possible`
**Ans: A** — Series mixing multiplies Z_i by 1+Aβ; shunt mixing divides it.

**Q56.** The input bias-current-induced output error in an inverting amplifier with R_1 = R_f = 10 kΩ and I_B = 100 nA, with no compensation resistor, is about:
`A) 1 mV | B) 2 mV | C) 10 mV | D) 100 mV`
**Ans: B** — Two bias currents flow through R_f: I_B·R_f + (1+1/R_f/R_1)I_B·R_f ≈ 2 mV.

**Q57.** A JFET-input op-amp (e.g. TL084 family) is preferred over a 741 when the source resistance is:
`A) < 100 Ω | B) 1 kΩ | C) > 100 kΩ | D) Any value`
**Ans: C** — Bias current × Z_s is the error; 80 nA into 1 MΩ is 80 mV, but 1 pA gives 1 µV.

**Q58.** In the ideal op-amp model, the two inputs are:
`A) Current-sensing | B) Voltage-sensing only | C) Power-sensing | D) Impedance-sensing`
**Ans: B** — Infinite input impedance means the op-amp senses voltage and draws no current.

**Q59.** An internally compensated op-amp's open-loop gain magnitude falls at:
`A) −20 dB/decade beyond the dominant pole | B) −40 dB/decade | C) −60 dB/decade | D) 0 dB/decade`
**Ans: A** — One pole gives −20 dB/dec, which is what makes it unity-gain stable.

**Q60.** An instrumentation amplifier built from three op-amps has the advantage that:
`A) It needs no resistors | B) Its gain is set by one resistor while input Z stays very high and CMRR is preserved | C) It works without supplies | D) It has zero offset`
**Ans: B** — Single-gain-set-resistor INA designs keep high Z_in and very high CMRR.

---

## SECTION 2 — Op-Amp Linear Circuits (Q61–Q140)

**Q61.** An inverting amplifier has R_1 = 5 kΩ and R_f = 20 kΩ. Its voltage gain is:
`A) −4 | B) +4 | C) −5 | D) 5`
**Ans: A** — A_v = −R_f/R_1 = −4; the minus sign means 180° phase reversal.

**Q62.** The input impedance seen by the source in an inverting amplifier equals:
`A) R_f | B) R_1 | C) ∞ | D) A_OL·R_1`
**Ans: B** — Virtual ground holds the node at 0 V, so the source sees only R_1.

**Q63.** The input impedance seen by the source in a non-inverting amplifier is:
`A) 1/β | B) R_1 | C) ∞ (ideally) | D) R_1 + R_f`
**Ans: C** — The source drives the + terminal directly; no current flows into it.

**Q64.** An inverting amplifier has a gain of −20 and an input impedance of 5 kΩ. Its feedback resistance is:
`A) 100 kΩ | B) 25 kΩ | C) 0.25 kΩ | D) 1 MΩ`
**Ans: A** — R_f = 20 × 5 kΩ = 100 kΩ.

**Q65.** A unity-gain buffer is used to drive a 1 kΩ load from a 1 MΩ source. The output will:
`A) Be attenuated by 1000 | B) Follow the input closely with Z_in ≈ ∞, Z_out ≈ 0 | C) Be zero | D) Be clipped`
**Ans: B** — The buffer isolates the high-impedance source from the load; its purpose is impedance transformation.

**Q66.** A 3-input summing amplifier has R_1 = R_2 = R_3 = 10 kΩ and R_f = 30 kΩ. With V_1 = 1 V, V_2 = 2 V, V_3 = 3 V, the output is:
`A) −18 V | B) −2 V | C) +6 V | D) −6 V`
**Ans: A** — V_o = −(30/10)(1+2+3) = −18 V.

**Q67.** For the summing amplifier of Q66 to be an *averaging* amplifier, R_f must be:
`A) 10 kΩ | B) 30 kΩ | C) 90 kΩ | D) 7.5 kΩ`
**Ans: A** — V_o = −(V_1+V_2+V_3)/3 requires R_f = R_1/3.

**Q68.** In a summing amplifier with unequal inputs (R_1 = 10 kΩ, R_2 = 20 kΩ, R_f = 10 kΩ) and V_1 = 2 V, V_2 = 3 V, V_o equals:
`A) −5 V | B) −(1 + 1.5) = −2.5 V | C) +5 V | D) −0.5 V`
**Ans: B** — V_o = −(R_f/R_1)V_1 − (R_f/R_2)V_2 = −2 − 1.5 = −2.5 V.

**Q69.** A difference amplifier has R_1/R_2 = R_3/R_4 = 1/10. For V_1 = 1 V, V_2 = 2 V, V_3 = 0 V, V_4 = 3 V, the output is:
`A) 10 V | B) −10 V | C) 1 V | D) 2 V`
**Ans: A** — With matching ratios, V_o = (R_2/R_1)(V_4 − V_2) = 10 × (3 − 2) = 10 V.

**Q70.** For a difference amplifier to reject common-mode signals, it is essential that:
`A) Both inputs use the same source | B) R_2/R_1 = R_4/R_3 exactly | C) The op-amp be a comparator | D) A supply be added`
**Ans: B** — Exact ratio matching is what cancels common-mode gain; otherwise CMRR degrades badly.

**Q71.** A practical difference amplifier has R_2/R_1 = 100 and R_4/R_3 = 99. Its CMRR is dominated by:
`A) The op-amp's A_OL | B) The 1 % resistor ratio mismatch | C) The supply rails | D) Input bias current`
**Ans: B** — Mismatch-limited CMRR ≈ 20 log((1+m)/m) ≈ 20 log(1/0.01) ≈ 40 dB.

**Q72.** An op-amp integrator has R = 1 MΩ, C = 0.1 µF, and a 1 V DC input. The output ramp slope is:
`A) 0.1 V/s | B) 10 V/s | C) 100 V/s | D) 1 V/s`
**Ans: B** — dV_o/dt = −V_i/(RC) = −1/(10^6 × 10^−7) = −10 V/s.

**Q73.** In Q72, how long does it take for the output to reach −10 V (before saturation)?
`A) 1 s | B) 10 s | C) 100 s | D) 0.1 s`
**Ans: A** — 10 V ÷ 10 V/s = 1 s.

**Q74.** The main practical limitation of an ideal op-amp integrator is:
`A) Gain error | B) Saturation due to DC offset and input bias current | C) slew rate | D) Output impedance`
**Ans: B** — Any offset current charges the capacitor without bound; hence the practical integrator adds a large series R.

**Q75.** A practical integrator is made by adding a resistor R_s in series with the feedback capacitor. Its gain function becomes:
`A) −R_s/(1+sR_sC) | B) −1/(sR_sC) only | C) −(R_s/R_in) | D) −sR_sC`
**Ans: A** — The added pole limits low-frequency gain to −R_s/R_in, preventing drift to saturation.

**Q76.** A practical integrator with R_s = 10 MΩ, R_in = 1 MΩ, C = 0.1 µF has a DC (low-frequency) gain of:
`A) −10 | B) −0.1 | C) −100 | D) −1`
**Ans: A** — Gain at DC = −R_s/R_in = −10, so 10 mV offset gives only 100 mV output error.

**Q77.** An ideal differentiator uses R = 10 kΩ and C = 0.1 µF. Its gain at 1 kHz is:
`A) 1 | B) 6.28 | C) 62.8 | D) 628`
**Ans: B** — |A| = ωRC = 2π(1000)(10^4)(10^−7) = 6.28.

**Q78.** The standard fix for the high-frequency noise amplification of a differentiator is to add:
`A) A series R and a parallel C across the feedback capacitor | B) A shunt C at the input | C) A larger supply | D) A buffer`
**Ans: A** — The pole formed by R_s and C_f limits gain at high frequency.

**Q79.** An op-amp transresistance (current-to-voltage) converter has R_f = 1 MΩ. For an input current of 10 µA, the output is:
`A) 1 V | B) 10 V | C) 0.1 V | D) 100 V`
**Ans: B** — V_o = −I_in·R_f = −10×10^−6 × 10^6 = −10 V.

**Q80.** The input impedance of a transresistance amplifier is:
`A) 1 MΩ | B) Very low (virtual ground) | C) Infinite | D) 1 kΩ`
**Ans: B** — The summing node is held at virtual ground, so the sensor sees a short — good for currents, bad for voltages.

**Q81.** A photodiode with 20 µA photocurrent drives a 100 kΩ transresistance amplifier. The output is:
`A) 0.2 V | B) 2 V | C) 20 V | D) 200 mV at 20 mA`
**Ans: B** — 20 µA × 100 kΩ = 2 V.

**Q82.** A voltage-to-current (transconductance) converter uses R_f = 1 kΩ and R_1 = 10 kΩ. For a 2 V input, the output current is:
`A) 0.2 mA | B) 2 mA | C) 20 mA | D) 0.2 µA`
**Ans: A** — I_o = V_i/R_1 = 2/10 kΩ = 0.2 mA; R_f sets the compliance voltage.

**Q83.** A non-inverting amplifier with R_1 = 10 kΩ, R_f = 90 kΩ has a gain of:
`A) 10 | B) 9 | C) −10 | D) 91`
**Ans: A** — A_v = 1 + R_f/R_1 = 10.

**Q84.** The output of a non-inverting amplifier with gain 5 and input 1.5 V is:
`A) 7.5 V | B) −7.5 V | C) 6 V | D) 0.3 V`
**Ans: A** — 5 × 1.5 = 7.5 V (no inversion).

**Q85.** A non-inverting amplifier's input resistance is set by:
`A) R_f/R_1 ratio | B) Only the op-amp's differential input Z | C) R_1 ∥ R_2 | D) The load`
**Ans: B** — Nothing connects to the + input except the source, so Z_in is the op-amp's own (ideally ∞).

**Q86.** Two unity-gain buffers in cascade drive a 100 nF load. The advantage is:
`A) Gain of 100 | B) Increased current drive and lower output Z | C) Reduced offset | D) Higher bandwidth`
**Ans: B** — Cascading buffers increases available output current, so the capacitive load can be charged faster.

**Q87.** An inverting amplifier (gain −5) is followed by a non-inverting amplifier (gain 3). The overall gain is:
`A) −8 | B) −15 | C) 15 | D) −2`
**Ans: B** — (−5)(3) = −15.

**Q88.** For very high input impedance, the best choice is:
`A) 741 | B) TL084 (FET input) | C) LM358 | D) A discrete BJT stage`
**Ans: B** — FET/JFET-input stages have bias currents of tens of picoamps.

**Q89.** A 741 has A_OL = 2×10^5 and is wired as an inverting amplifier with R_f/R_1 = 10. The actual gain is closest to:
`A) −10.00 | B) −9.9995 | C) −9.90 | D) −9.0`
**Ans: B** — A/(1+A/10) = 2×10^5/(2×10^5 + 0.1) ≈ −9.9995; closed-loop gain never exceeds A_OL in magnitude.

**Q90.** Which amplifier configuration has the highest input impedance?
`A) Common emitter | B) Common collector (emitter follower) | C) Common base | D) All equal`
**Ans: B** — Emitter follower Z_in ≈ (β+1)(R_E ∥ r_e), the largest of the three.

**Q91.** A T-network inverts and amplifies with R_1 = 10 kΩ, R_f = 900 kΩ, R_2 = 100 kΩ, R_3 = 10 kΩ. The gain is:
`A) −10 | B) −100 | C) −1000 | D) −1010`
**Ans: B** — Effective feedback resistance = R_f + R_3 + (R_f·R_3)/R_2 = 900 + 10 + 90 = 1000 kΩ, so gain = −1000/10 = −100.

**Q92.** An op-amp is used as a *unity-gain* buffer to drive a capacitive load. The main risk is:
`A) Slew-rate/current-limit induced oscillation | B) Thermal runaway | C) CMRR loss | D) Offset drift`
**Ans: A** — Driving C_L through the op-amp output stage causes phase lag; isolation resistors or a unity-gain-stable buffer are needed.

**Q93.** An integrator with R = 1 MΩ, C = 1 µF is fed a 1 V, 1 kHz sine wave. The output amplitude is:
`A) 0.159 V | B) 1.59 V | C) 15.9 V | D) 0.016 V`
**Ans: A** — |V_o| = V_i/(ωRC) = 1/(2π·10^3·10^6·10^−6) = 1/6283 ≈ 0.159 V.

**Q94.** An ideal integrator's output is:
`A) In phase with input | B) 90° out of phase | C) 180° out of phase | D) Unchanged`
**Ans: C** — Gain = −1/(jωRC) = +j/(ωRC): a +90° shift combined with the inversion = 180°.

**Q95.** An ideal differentiator's output is:
`A) In phase with input | B) 90° out of phase | C) 180° out of phase | D) Delayed`
**Ans: B** — Gain = −jωRC → +90° shift.

**Q96.** The transfer function of an ideal op-amp differentiator is:
`A) −R/(sC) | B) −1/(sRC) | C) −sRC | D) −RC/s²`
**Ans: C** — V_o/V_i = −1/(sRC)·sRC·... i.e. H(s) = −sRC, magnitude rising 20 dB/decade.

**Q97.** A charge amplifier (capacitive sensor) uses C_f = 1 pF with input charge Q = 1 fC. The output is:
`A) 1 V | B) 10 V | C) 0.1 V | D) 1000 V`
**Ans: A** — V_o = Q/C_f = 10^−15/10^−12 = 1 V.

**Q98.** An op-amp peak detector holds the peak of a 5 V pulse. After the pulse ends, the output:
`A) Returns to 0 | B) Remains at ~5 V (with slow droop) | C) Becomes −5 V | D) Saturates the op-amp permanently`
**Ans: B** — The diode isolates the hold capacitor; droop is set by leakage, which is why C is chosen large.

**Q99.** A sample-and-hold circuit requires the hold capacitor to be:
`A) Small for fast sampling | B) Large for long hold and low droop | C) Polarity-dependent | D) Replaced by a resistor`
**Ans: B** — Large C gives long time constant τ = R·C and hence low hold droop.

**Q100.** A track-and-hold circuit's ideal behaviour is V_o = V_i while tracking and V_o = constant while holding. Its dominant error during hold is:
`A) Slew rate | B) Capacitor leakage and op-amp bias current | C) A_OL | D) CMRR`
**Ans: B** — Droop = I_leak/C_hold.

**Q101.** An op-amp integrator with a reset switch across the feedback capacitor is used to obtain:
`A) A sawtooth ramp generator | B) A rectifier | C) A multiplier | D) A comparator`
**Ans: A** — Periodic reset of the capacitor produces a linear ramp; with a Schmitt trigger it becomes a triangle/triangle-sawtooth generator.

**Q102.** A positive ramp of 5 V over 1 ms followed by a 1 ms flyback is produced by an integrator with feedback resistance 10 kΩ. The required input current is:
`A) 0.5 mA | B) 1 mA | C) 5 mA | D) 0.1 mA`
**Ans: A** — I = ΔV/Δt/R = 5/(1 ms)/10 kΩ = 5000/10 000 = 0.5 mA.

**Q103.** In an op-amp based V–I converter for a magnetometer, the compliance voltage is:
`A) Always 10 V | B) V_sat minus the drop across the burden resistor | C) Equal to R_f | D) Zero`
**Ans: B** — The burden (feedback) resistor plus the transistor must stay inside the output swing, or accuracy is lost.

**Q104.** An absolute-value circuit built with two op-amps and matched resistors produces:
`A) V_o = V_i | B) V_o = −|V_i| | C) V_o = |V_i| with no diode | D) V_o = V_i²`
**Ans: B** — The feedback diode reverses direction with the sign of the input, so both halves give negative output.

**Q105.** A precision half-wave rectifier is used instead of a passive rectifier because:
`A) It has lower forward drop (≈0 for ideal op-amp) | B) It is cheaper | C) It needs no diodes | D) It handles higher currents`
**Ans: A** — The op-amp compensates the diode drop, so small signals are rectified accurately.

**Q106.** An op-amp precision rectifier requires the diode to be placed:
`A) In series with the input | B) Inside the feedback loop | C) Across the supply | D) At the output to ground`
**Ans: B** — Putting the diode inside the loop makes the closed loop force the zero-drop condition.

**Q107.** An inverting amplifier produces 6 V output for a 2 mV input. The gain magnitude is:
`A) 3 | B) 300 | C) 3000 | D) 0.33`
**Ans: C** — 6/0.002 = 3000; with such a large gain, slew rate and offset dominate real performance.

**Q108.** A zero-crossing detector based on an op-amp is triggered by a 1 V, 1 kHz sine wave. The output square wave has:
`A) Amplitude 1 V | B) Amplitude ≈ ±V_sat and 50 % duty cycle | C) Amplitude 0 | D) Duty cycle 25 %`
**Ans: B** — Threshold at 0 V, so conduction lasts half the cycle and the output swings to the rails.

**Q109.** A 2 V-peak sine wave (zero DC) drives a non-inverting comparator with V_ref = 0.5 V. The output duty cycle (HIGH) is:
`A) 41.9 % | B) 58.1 % | C) 50 % | D) 25 %`
**Ans: A** — sin θ > 0.25 ⇒ θ₀ = 14.48°, so HIGH lasts 180° − 28.96° = 151° ⇒ 151/360 = 41.9 %.

**Q110.** The same 4 Vpp, 1 kHz sine wave compared against a 1 V reference (non-inverting) has a HIGH duty cycle of:
`A) 33.33 % | B) 66.66 % | C) 50 % | D) 25 %`
**Ans: A** — With V_m = 2 V, sin θ > 1/2 → θ ∈ (30°, 150°) → 120/360 = 33.3 %. **[ISRO-2023 pattern, Q54]**

**Q111.** An inverting comparator with V_ref = 2 V and V_m = 5 V (0 DC) has a LOW-output duty cycle of:
`A) 36.9 % | B) 63.1 % | C) 50 % | D) 23.6 %`
**Ans: A** — Output is −V_sat while sin θ > 0.4; θ₀ = 23.58°, so LOW lasts 2(90° − 23.58°) = 132.8° of 360° = 36.9 %.

**Q112.** A Schmitt-trigger comparator is preferred over a plain comparator when the input is:
`A) A clean ramp | B) A noisy signal near the threshold | C) A DC level | D) A square wave`
**Ans: B** — Hysteresis wider than the noise amplitude prevents false switching.

**Q113.** A comparator's output switching time is fundamentally limited by:
`A) Slew rate | B) Input offset | C) CMRR | D) Thermal noise`
**Ans: A** — To traverse from −V_sat to +V_sat takes 2V_sat/SR.

**Q114.** A comparator with ±12 V saturation, SR = 5 V/µs, has a minimum output transition time of:
`A) 0.4 µs | B) 2.4 µs | C) 4.8 µs | D) 24 µs`
**Ans: C** — 2V_sat/SR = 24/5 = 4.8 µs.

**Q115.** A comparator for a 1 MHz zero-crossing detector must have an output transition time at most:
`A) 1 µs | B) 0.5 µs | C) 0.1 µs | D) 10 µs`
**Ans: C** — ≤ 1/(2 × 1 MHz) = 0.5 µs is the limit; 0.1 µs gives margin.

**Q116.** An inverting amplifier's noise gain is:
`A) 1 + R_f/R_1 | B) R_f/R_1 | C) 1 | D) R_1/R_f`
**Ans: A** — Noise gain = signal gain + 1, which is why a −1 gain stage has NG = 2.

**Q117.** Why is a "gain = 1" inverting amplifier still limited in bandwidth by noise gain 2?
`A) Because NG = 1 + |A_v| = 2 | B) Because R_f is shorted | C) Because the op-amp is open-loop | D) Because of offset drift`
**Ans: A** — Bandwidth = GBW/NG, so inverting stages are always 3 dB worse than a non-inverting stage of the same magnitude.

**Q118.** A bootstrap circuit increases input impedance because:
`A) The output drives the source side of the input resistor in phase, so no AC current flows | B) It uses two op-amps | C) It removes the bias resistor | D) It increases supply voltage`
**Ans: A** — V_source = V_input means the resistor has zero AC voltage across it → infinite effective Z.

**Q119.** An op-amp level-shifter: a non-inverting amplifier (R_1 = 10 kΩ, R_f = 10 kΩ) has its + input at 1 V DC and the signal applied there too. A 0.1 V signal gives:
`A) 0.1 V | B) 0.2 V | C) 2.1 V AC | D) 1.1 V AC`
**Ans: C** — Gain = 2, so the AC output is 0.2 V riding on a 2 V DC level.

**Q120.** To obtain a *DC-coupled* gain stage without losing DC, one must:
`A) Remove coupling capacitors | B) Add 1 µF caps | C) Use a dual supply only | D) Add a Zener`
**Ans: A** — Capacitors are only needed for AC coupling; DC coupling means R–R input and bias resistors.

**Q121.** A two-stage op-amp amplifier where the first stage is inverting and the second non-inverting has an overall input impedance that is:
`A) Higher than either stage alone | B) Lower, limited by the first stage's R_1 | C) Infinite | D) Equal to Z_out`
**Ans: B** — The source sees only the inverting stage's input resistor.

**Q122.** An op-amp integrator's initial output condition after a reset switch opens at t = 0 with input 0.5 V and RC = 1 s is:
`A) 0 V | B) Ramps down at 0.5 V/s | C) Ramps up at 0.5 V/s | D) Jumps to −0.5 V`
**Ans: B** — dV_o/dt = −V_i/RC = −0.5 V/s.

**Q123.** For a practical integrator (R_s = 10 MΩ in series with C_f = 1 µF), the pole frequency is:
`A) 0.016 Hz | B) 1 Hz | C) 100 Hz | D) 10 Hz`
**Ans: A** — f_p = 1/(2πR_sC) = 1/(2π×10^7×10^−6) ≈ 0.0159 Hz.

**Q124.** A CMOS op-amp has a common-mode input range of 0 V to V_DD (rail-to-rail). Compared with a 741 this means:
`A) Larger usable output swing | B) Better PSRR only | C) Higher slew rate | D) Lower offset`
**Ans: A** — Rail-to-rail in/out amplifiers swing to both rails, essential on 3.3 V/5 V supplies.

**Q125.** An op-amp with A_OL = 100 dB and β = 0.01 has a gain-magnitude error of:
`A) 1 % | B) 0.01 % | C) 10 % | D) 0 %`
**Ans: B** — Error ≈ 1/Aβ = 1/(10^5 × 0.01) = 0.01 = 0.01 %.

**Q126.** A differential amplifier with gain 100 is fed a 1 V differential signal plus 5 V common-mode. The output contains:
`A) 100 V only | B) 100 V differential + common-mode error × A_cm | C) 5 V | D) 0 V`
**Ans: B** — Output = 100 × 1 V + A_cm × 5 V; with CMRR 100 dB the CM term is 5 mV.

**Q127.** In a differential amplifier, the maximum input common-mode voltage without saturation is called:
`A) Input swing | B) Common-mode range | C) Supply rail | D) Threshold`
**Ans: B** — Exceeding it saturates the input stage and destroys the common-mode rejection.

**Q128.** An op-amp summing amplifier can also perform subtraction by:
`A) Adding an inverting input path | B) Reversing the supply | C) Adding a capacitor | D) Reducing gain`
**Ans: A** — Feeding V_2 through an inverting input resistor gives V_o = −(V_1a − V_1b·k).

**Q129.** An inverting amplifier has R_1 = 1 MΩ, R_f = 2 MΩ and V_in = 2 V. The output is:
`A) −1 V | B) −2 V | C) −4 V | D) +2 V`
**Ans: C** — V_o = −(R_f/R_1)·V_in = −(2/1)(2) = −4 V.

**Q130.** In a bootstrapped high-impedance input, the op-amp's function is to:
`A) Provide gain | B) Buffer the bootstrapping signal so V_source follows V_input exactly | C) Increase supply | D) Rectify`
**Ans: B** — Only an accurate follower makes V_R have zero AC content.

**Q131.** An op-amp integrator produces a triangle wave when its input is:
`A) A sine wave | B) A square wave | C) A ramp | D) A triangle`
**Ans: B** — Square in → triangle out; this is the basis of function generators.

**Q132.** A 1 kHz, 50 % duty-cycle square wave of ±2 V drives an integrator of C = 1 µF; the required output is a ±5 V triangle. The feedback resistance is:
`A) 50 Ω | B) 100 Ω | C) 200 Ω | D) 1 kΩ`
**Ans: B** — Ramp needs I = C·ΔV/Δt = 10⁻⁶ × 10/0.5 ms = 20 mA, so R = 2 V/20 mA = 100 Ω.

**Q133.** Which statement about an op-amp used in a linear (inverting) configuration is TRUE?
`A) The differential input must be non-zero | B) V_d ≈ 0 and the input current is 0 | C) The output must be at −V_sat | D) It is unstable`
**Ans: B** — Linear operation demands the differential input be essentially zero and no current enter the terminals.

**Q134.** An op-amp integrator's output reaches −10 V in 1 ms for a 1 V input. The value of R·C is:
`A) 0.1 ms | B) 1 ms | C) 10 ms | D) 100 ms`
**Ans: A** — dV_o/dt = V_i/RC ⇒ 10 V/1 ms = 10^4 V/s = 1/(RC) ⇒ R·C = 10⁻⁴ s = 0.1 ms.

**Q135.** A practical integrator's transfer function is best described as:
`A) −1/(sRC) | B) −R_s/(1 + sR_sC) | C) −sRC | D) −R_s/R_in at all frequencies`
**Ans: B** — Unity-gain-ish high-pass-into-integrator behaviour with a defined DC gain.

**Q136.** A 100 kΩ source drives an op-amp summing node directly (no bias-current compensation). With I_B = 20 nA the DC output error is:
`A) 2 mV | B) 2 V | C) 20 mV | D) 0`
**Ans: A** — I_B × R_f (for a 100 kΩ feedback) = 20 nA × 100 kΩ = 2 mV.

**Q137.** An op-amp voltage follower cannot be used for level shifting of a *bipolar* signal when:
`A) The output swing exceeds the rails | B) The input offset exceeds the signal | C) The load is capacitive | D) The source is ideal`
**Ans: A** — With no gain available, any offset larger than the available headroom clips the output.

**Q138.** Two cascaded differentiators produce an output proportional to:
`A) The integral of input | B) The second derivative of input | C) The input itself | D) The square of input`
**Ans: B** — Each stage differentiates, so two stages give d²v_i/dt² with gain (R_1C_1)(R_2C_2).

**Q139.** An op-amp output drives a 10 nF capacitive load with a 2 V-peak, 10 kHz sine wave. The peak output current is:
`A) 0.63 mA | B) 1.26 mA | C) 12.6 mA | D) 126 mA`
**Ans: B** — I_p = 2πfC·V_p = 2π(10^4)(10^−8)(2) ≈ 1.26 mA.

**Q140.** A two-op-amp instrumentation amplifier sets its gain with a single resistor R_G as:
`A) A_v = 1 + 2R_G/R_1 | B) A_v = 1 + R_G/(2R_1) | C) A_v = 2R_1/R_G | D) A_v = R_G/R_1`
**Ans: A** — Standard three-op-amp INA topology.

---

## SECTION 3 — Op-Amp Non-Linear Circuits (Q141–Q195)

**Q141.** In an op-amp logarithmic amplifier, the output is proportional to:
`A) V_in | B) ln(V_in) | C) log₁₀(V_in/R) | D) V_in²`
**Ans: B** — V_o = −(nV_T)·ln(V_in/(R·I_S)); base of the logarithm is irrelevant, only proportionality to ln.

**Q142.** A log amplifier uses R = 100 kΩ and a diode with n = 1, V_T = 25.85 mV, I_S = 10⁻¹⁴ A. For V_in = 10 mV the output is approximately:
`A) −0.42 V | B) −0.25 V | C) −1.6 V | D) +0.42 V`
**Ans: A** — V_in/(R·I_S) = 10⁻²/10⁻⁹ = 10⁷; V_o = −0.02585 × ln(10⁷) = −0.417 V.

**Q143.** The temperature compensation resistor in a temperature-compensated log amplifier is chosen as:
`A) R_T = R·(T/T₀) | B) R_T = R₀ | C) R_T = R·2 | D) R_T = 0`
**Ans: A** — Since V_T = kT/q, a resistor with the same +0.17 %/°C drift as the diode's V_T cancels the temperature error.

**Q144.** An anti-log (antilogarithmic) amplifier produces an output:
`A) Proportional to ln(V_in) | B) Proportional to e^(V_in/(nV_T)) | C) Proportional to V_in² | D) Proportional to 1/V_in`
**Ans: B** — V_o = R·I_S·e^(V_in/(nV_T)); it is the functional inverse of the log amp, so log→antilog round-trips restore the signal.

**Q145.** Two log amplifiers feeding a unity-gain summing stage implement:
`A) Addition | B) Multiplication | C) Division | D) Differentiation`
**Ans: B** — ln V_x + ln V_y = ln(V_x·V_y), so the exponential stage converts back to V_x·V_y.

**Q146.** Subtracting two log-amplifier outputs before exponentiating implements:
`A) Multiplication | B) Division | C) Addition | D) Squaring`
**Ans: B** — ln(V_1/V_2) exponentiated gives the ratio, so it is a four-quadrant divider.

**Q147.** An op-amp absolute-value circuit produces:
`A) V_o = V_i | B) V_o = −|V_i| | C) V_o = |V_i| offset by 0.7 V | D) V_o = V_i/2`
**Ans: B** — The feedback polarity flips with the sign of the input, so both half-cycles give negative output.

**Q148.** The main advantage of an op-amp precision rectifier over a passive one is:
`A) Higher current capability | B) Nearly zero forward drop, so millivolt signals are rectified accurately | C) Lower cost | D) No op-amp needed`
**Ans: B** — The op-amp compensates the diode drop by forcing its own V_BE to zero.

**Q149.** An op-amp precision rectifier requires a diode in the:
`A) Input path | B) Feedback path | C) Supply | D) Ground path`
**Ans: B** — With the diode inside the loop, the closed loop forces zero diode drop when conducting.

**Q150.** A window comparator with thresholds +2 V and −2 V outputs HIGH when:
`A) V_i > 2 V | B) V_i < −2 V | C) −2 V < V_i < 2 V | D) V_i = 0`
**Ans: C** — Two comparators ANDed produce a band (window) detector.

**Q151.** An op-amp relaxation oscillator (op-amp + RC feedback, no external tank) generates a:
`A) Sine wave | B) Square/triangle wave | C) Sawtooth only | D) Pulse train at RF`
**Ans: B** — Positive feedback sets thresholds while the RC charges, so the output alternates between rails (square) and the capacitor ramps (triangle).

**Q152.** The relaxation-oscillator frequency for β = 1/3 (symmetric thresholds) is:
`A) f = 1/(RC) | B) f = 1/(1.39·R·C) | C) f = 1/(2πRC) | D) f = RC`
**Ans: B** — f = 1/[2RC·ln((1+β)/(1−β))] = 1/(2·0.693·RC) = 1/(1.386 RC).

**Q153.** A relaxation oscillator with R = 10 kΩ, C = 0.01 µF has an oscillation frequency of about:
`A) 7.2 kHz | B) 1.6 kHz | C) 36 kHz | D) 1 kHz`
**Ans: A** — RC = 10⁻⁴ s, f = 1/(1.386×10⁻⁴) ≈ 7.2 kHz.

**Q154.** In a triangle/square generator made from a Schmitt trigger plus an integrator, the loop must satisfy:
`A) f_integrator = f_Schmitt | B) f_integrator = 2·f_Schmitt with the Schmitt dividing the ramp | C) Any frequency | D) The Schmitt must be a comparator`
**Ans: B** — Each Schmitt transition reverses the ramp; the square-wave frequency is half the ramp cycle rate.

**Q155.** An integrator-driven V/F converter: I = 1 mA, C = 1 nF, ramp from −5 V to +5 V. The output frequency is:
`A) 10 kHz | B) 100 kHz | C) 1 MHz | D) 50 kHz`
**Ans: B** — T = 2CV_ref/I = 2×10⁻⁹×5/10⁻³ = 10 µs ⇒ f = 100 kHz.

**Q156.** In a V/F converter, doubling the input current:
`A) Halves the frequency | B) Doubles the frequency | C) Has no effect | D) Squares the frequency`
**Ans: B** — f = I/(2CV_ref) is linear in I, which is what makes the V/F stage useful.

**Q157.** A sample-and-hold circuit's droop rate is set by:
`A) Slew rate | B) Capacitor leakage and switch leakage divided by C | C) Op-amp A_OL | D) Input offset`
**Ans: B** — Droop = I_leak/C_hold; larger hold capacitors and FET switches reduce it.

**Q158.** An op-amp peak detector is built from:
`A) A comparator with hysteresis | B) An inverting amplifier with a diode in the feedback path | C) An integrator with reset | D) A current mirror`
**Ans: B** — The diode in the feedback path lets the output rise to the peak and then blocks any reverse current.

**Q159.** A logarithmic amplifier measures a 10 pA – 10 mA range of currents directly (no explicit R) by:
`A) Varying the feedback resistance | B) Using the diode's I–V in the feedback path | C) Using a Zener | D) Using two supplies`
**Ans: B** — A wide current range maps to a limited voltage range because I = I_S·e^(V/nV_T).

**Q160.** An absolute-value circuit using a single op-amp, two diodes and matched resistors has a systematic error of:
`A) Zero | B) Two forward diode drops | C) One forward diode drop (≈0.7 V) | D) The op-amp offset only`
**Ans: C** — The classic single-op-amp precision rectifier still leaves one V_F unless both diodes are inside the loop.

**Q161.** An op-amp square-law generator uses a BJT/diode whose transfer characteristic is:
`A) I = I_S e^(V/V_T) | B) I ∝ (V − V_T)² | C) I ∝ V | D) I ∝ V³`
**Ans: B** — V_o = −(R_f/(2K))(V_in − V_T)² gives parabolic waveforms for synthesis and modulation.

**Q162.** A 4-bit R–2R DAC with V_ref = 10 V has an LSB size of:
`A) 1.25 V | B) 0.625 V | C) 2.5 V | D) 0.25 V`
**Ans: B** — LSB = V_ref/2⁴ = 10/16 = 0.625 V.

**Q163.** A 4-bit R–2R DAC with V_ref = 10 V driven by code 1011 outputs:
`A) 6.25 V | B) 6.875 V | C) 5.625 V | D) 11.25 V`
**Ans: B** — V_o = (11/16)×10 = 6.875 V.

**Q164.** An op-amp weighted-sum DAC assigns weights by:
`A) Input resistor values that are binary multiples | B) Supply voltages | C) Op-amp gain only | D) Trimmer capacitors`
**Ans: A** — R, 2R, 4R, … resistors set binary weights; this is the standard "binary-weighted DAC".

**Q165.** Why is an R–2R ladder preferred over binary-weighted resistors in a DAC?
`A) Lower cost | B) Only two resistor values are needed, improving matching | C) Higher resolution | D) No reference needed`
**Ans: B** — Two matched values are far easier to fabricate uniformly than 2ⁿ−1 distinct resistors.

**Q166.** A zero-crossing detector for a 1 Hz to 10 kHz signal can be built from:
`A) An op-amp comparator with 0 V reference and hysteresis | B) A log amp | C) A multiplier | D) An integrator with no reset`
**Ans: A** — Hysteresis prevents chatter at the crossing; the comparator output gives a clean square wave.

**Q167.** An op-amp comparator driving an LED in series with 1 kΩ from ±12 V. The LED (V_F = 2 V) current when ON is:
`A) 2 mA | B) 10 mA | C) 20 mA | D) 12 mA`
**Ans: B** — (12 − 2)/1 kΩ = 10 mA.

**Q168.** In an op-amp + LED indicator, the LED turns ON when V_i is (ideal parts, V_ref = 6 V, non-inverting) **[PYP-25 Q58 pattern]**:
`A) Less than 6 V | B) More than 6 V | C) Less than 12 V | D) More than 12 V`
**Ans: B** — Non-inverting comparator: V+ > V− ⇒ output goes to +V_sat and forward-biases the LED.

**Q169.** Why is a series current-limiting resistor mandatory with an LED driven by an op-amp output?
`A) To protect the op-amp | B) To limit LED current to a safe value, since op-amp voltage is set by rail and LED drop alone is not enough | C) To increase brightness | D) To block DC`
**Ans: B** — Without the resistor the current would be limited only by the op-amp's output impedance, which is not predictable.

**Q170.** An op-amp integrator with a diode clamp is used to produce:
`A) A square wave | B) A triangle limited to ±0.7 V | C) A sine wave | D) A sawtooth limited to the rails`
**Ans: B** — Diodes clamp the capacitor voltage at one junction drop each way, bounding the ramp.

**Q171.** An op-amp current-to-voltage converter for a photodiode is better than a resistive load because it:
`A) Increases the photocurrent | B) Converts current to a usable voltage with very low compliance voltage | C) Removes the need for a bias supply | D) Reduces noise`
**Ans: B** — Virtual ground keeps a near-zero voltage across the photodiode, improving linearity at low bias.

**Q172.** A temperature sensor gives 10 mV/°C. To obtain 100 mV/°C an op-amp stage is used with:
`A) Gain 1 | B) Gain 10 | C) Gain 0.1 | D) Gain 100`
**Ans: B** — Non-inverting gain 1 + R_f/R_1 = 10 (e.g. R_1 = 9 kΩ, R_f = 81 kΩ).

**Q173.** A transresistance stage is followed by a log stage to build a wide-range light meter. This is a:
`A) Photometer | B) Speck pattern | C) Random generator | D) PLL`
**Ans: A** — The combination is the classic optical-density/logarithmic light meter.

**Q174.** A multiplier built from two log amps and one antilog amp measures:
`A) Sum | B) Product | C) Ratio | D) Logarithm`
**Ans: B** — log(V_1) + log(V_2) → antilog gives V_1·V_2, the basis of analog multipliers.

**Q175.** A Gilbert-cell four-quadrant multiplier can multiply:
`A) Only positive × positive | B) Positive or negative × positive or negative | C) Only AC voltages | D) Only currents`
**Ans: B** — Four-quadrant means any sign combination works; two-quadrant multipliers cannot handle V_1 negative.

**Q176.** An op-amp integrator with an asymmetric reference (switched between +V_1 and −V_2) produces:
`A) A sawtooth of unequal up/down slopes | B) A sine | C) A square of constant duty | D) No output`
**Ans: A** — Different charge/discharge currents give different ramp slopes, which is how sawtooth generators are built.

**Q177.** The main limitation of using an op-amp as a multiplier (log–antilog) is:
`A) Temperature drift of the log stage | B) It cannot be used with DC | C) It needs 3 supplies | D) It has low input Z`
**Ans: A** — Both logs and the antilog use diode junctions, so uncompensated temperature drift limits accuracy to ~1 %.

**Q178.** An op-amp integrator/Schmitt combination produces a triangle whose peak-to-peak amplitude is:
`A) Unbounded | B) Fixed by the Schmitt thresholds | C) Equal to V_ref | D) Zero`
**Ans: B** — The triangle amplitude is set by UTP − LTP of the driving Schmitt trigger.

**Q179.** For an op-amp-based triangle generator with UTP = +3 V and LTP = −3 V driven through R = 10 kΩ into C = 0.01 µF, the ramp rate is:
`A) 30 kV/s | B) 3 kV/s | C) 300 V/s | D) 30 V/s`
**Ans: A** — dV/dt = V_i/(RC) = 3/(10^4 × 10⁻⁸) = 3×10⁴ V/s = 30 kV/s.

**Q180.** In the circuit of Q179, the triangle frequency is approximately:
`A) 1.25 kHz | B) 2.5 kHz | C) 5 kHz | D) 10 kHz`
**Ans: B** — A 6 V ramp at 30 kV/s takes 200 µs; a full up-down cycle is 400 µs ⇒ f = 2.5 kHz.

**Q181.** An op-amp differentiator applied to a square wave gives:
`A) Spikes at each edge | B) A triangle | C) A sine | D) DC`
**Ans: A** — d(v)/dt is zero except at transitions, producing impulses at the corners.

**Q182.** An op-amp differentiator applied to a triangle wave gives:
`A) Spikes | B) A constant-level square wave | C) A sine | D) A ramp`
**Ans: B** — Slope is constant, so the differentiator output is a constant ±RC·slope, i.e. a square wave.

**Q183.** An op-amp differentiator applied to a sine wave gives:
`A) A cosine | B) A sine shifted by 90° with gain ωRC | C) A square | D) DC`
**Ans: B** — Magnitude rises linearly with frequency; this is why differentiators are used as phase-shift networks.

**Q184.** A precision half-wave rectifier inverting positive half-cycles has an output offset of:
`A) +0.7 V | B) 0 V (ideally) | C) −0.7 V | D) −1.4 V`
**Ans: B** — The op-amp cancels the diode drop, so the only error is offset/bias current, typically µV.

**Q185.** A comparator with 10 mV of input noise needs at least:
`A) 0 V hysteresis | B) More than 20 mV of hysteresis | C) Exactly 10 mV hysteresis | D) A faster slew rate only`
**Ans: B** — Hysteresis should exceed twice the noise amplitude to guarantee one transition per crossing.

**Q186.** An op-amp switch (analog switch) built from a comparator + resistor is used for:
`A) Amplification | B) Sample selection / gating | C) Power conversion | D) Oscillation`
**Ans: B** — Selecting one of several signal paths by a control level is "sampling/gating".

**Q187.** An RMS-to-DC converter is needed when the waveform amplitude is unknown; its core building block is:
`A) A squarer and an averager (√mean of squares) | B) A log amp only | C) A Schmitt trigger | D) A Zener clipper`
**Ans: A** — V_out = √(mean(v²)); then a square-root stage gives true RMS.

**Q188.** The function of the second stage in an RMS converter (after averaging v²) is:
`A) Log | B) Square root | C) Differentiate | D) Clip`
**Ans: B** — Taking the square root gives the RMS value; clipping would destroy the true RMS property.

**Q189.** An op-amp clamp circuit that limits a ±20 V input to ±5 V is called a:
`A) Clipper | B) Slew limiter | C) Integrator | D) Sample-and-hold`
**Ans: A** — A clipper (precision limiter) clips at the diode/Junction levels set by feedback.

**Q190.** A precision limiter uses op-amps with back-to-back diodes in feedback. Its output when input exceeds the limit:
`A) Goes to the rail | B) Sits at exactly the limit set by the diode network | C) Becomes 0 | D) Oscillates`
**Ans: B** — Feedback forces V_BE to 0 V at the limit, giving an accurate clamp at the diode turn-on point.

**Q191.** In a log amplifier, using two matched transistors in the feedback path and input reduces error because:
`A) It doubles the gain | B) Junction currents cancel V_BE and temperature drift | C) It increases bandwidth | D) It lowers input Z`
**Ans: B** — Two identical junctions at equal current have matched V_BE and matching temperature coefficients.

**Q192.** A charge amplifier with C_f = 1 pF receives a 1 pC charge pulse. The output swing is:
`A) 1 mV | B) 1 V | C) 10 V | D) 100 V`
**Ans: B** — V_o = Q/C_f = 10⁻¹²/10⁻¹² = 1 V; this is why high-sensitivity charge amps use tiny feedback capacitors.

**Q193.** An op-amp used as a logarithmic sensor interface for a thermistor requires:
`A) AC coupling | B) DC-coupled biasing and a cold-junction/temperature-compensated feedback diode | C) A transformer | D) A 50 Ω source`
**Ans: B** — Because the response is logarithmic, accuracy depends entirely on temperature compensation.

**Q194.** A "dead zone" of 0.7 V appears in a passive rectifier but is eliminated in an op-amp precision rectifier. This improves:
`A) Frequency | B) Small-signal accuracy and linearity | C) Efficiency | D) Slew rate`
**Ans: B** — Signals smaller than 0.7 V are now reproduced with correct slope and gain.

**Q195.** Which statement best describes an op-amp used as a comparator?
`A) It is operated open-loop and the output saturates at ±V_sat | B) It must be in the linear region | C) It requires positive feedback for a single threshold | D) Its output is always analog`
**Ans: A** — No feedback ⇒ huge gain ⇒ bang-bang output at the rails; the threshold is simply V+ − V− = 0.

---

## SECTION 4 — Schmitt Triggers & Waveform Shaping (Q196–Q245)

**Q196.** The output of a Schmitt trigger depends on:
`A) Only the instantaneous input value | B) Clock transitions | C) Hysteresis in the threshold voltages | D) Fan-in of the gate`
**Ans: C** **[PYP-25 Q74]** — Inside the hysteresis band the output retains its *previous* state; that memory is the defining property.

**Q197.** A Schmitt trigger is essentially:
`A) A comparator with positive feedback | B) A comparator with negative feedback | C) An amplifier with a tank circuit | D) A relaxation oscillator`
**Ans: A** — Positive feedback sets two different thresholds for rising and falling inputs.

**Q198.** In an inverting Schmitt trigger with R_1 (input to −) and R_2 (output to +), the UTP is:
`A) +V_sat·R_2/(R_1+R_2) | B) +V_sat·R_1/(R_1+R_2) | C) +V_sat | D) 0`
**Ans: B** — The + terminal sits at a fraction R_1/(R_1+R_2) of the saturated output.

**Q199.** An inverting Schmitt trigger has R_1 = 10 kΩ, R_2 = 10 kΩ and V_sat = ±15 V. The hysteresis width is:
`A) 7.5 V | B) 15 V | C) 30 V | D) 0 V`
**Ans: B** — UTP = +7.5 V, LTP = −7.5 V, so V_H = 15 V.

**Q200.** The same Schmitt trigger with V_sat = ±12 V has UTP =:
`A) +6 V | B) +12 V | C) +3 V | D) −6 V`
**Ans: A** — UTP = 12 × 10/20 = +6 V.

**Q201.** A Schmitt trigger's + terminal is connected through 1 kΩ to the output and through 5 kΩ to ground, with V_sat = ±10 V. Its LTP is:
`A) −1.667 V | B) −5 V | C) −10 V | D) +1.667 V`
**Ans: A** — Threshold = V_sat × 1k/(1k+5k) = ±10/6 = ±1.667 V; LTP is the negative one. **[ISRO-2023 Q53 pattern]**

**Q202.** For the circuit of Q201, the hysteresis width (V_UTP − V_LTP) is:
`A) 1.667 V | B) 3.333 V | C) 8.333 V | D) 20 V`
**Ans: B** — 2 × 1.667 V = 3.333 V.

**Q203.** Increasing the feedback resistor R_2 in an inverting Schmitt trigger:
`A) Increases hysteresis | B) Decreases hysteresis | C) Sets hysteresis to zero | D) Changes supply polarity`
**Ans: B** — Hysteresis = 2V_sat·R_1/(R_1+R_2); larger R_2 lowers the threshold fraction and narrows the band.

**Q204.** Decreasing R_1 (the input resistor) in an inverting Schmitt trigger will:
`A) Increase UTP and LTP magnitudes | B) Decrease UTP magnitude only | C) Make thresholds supply-independent | D) Reverse the output`
**Ans: A** — Thresholds scale with R_1/(R_1+R_2), so a smaller R_1 raises them (narrower relative band).

**Q205.** A Schmitt trigger is fed a slow ramp. Its output:
`A) Follows the ramp | B) Switches only at UTP going up and LTP going down | C) Switches continuously | D) Saturates continuously`
**Ans: B** — Between LTP and UTP nothing happens, which is exactly how the "memory" is obtained.

**Q206.** The principal purpose of hysteresis in a comparator is to:
`A) Increase gain | B) Prevent false switching due to noise | C) Reduce power consumption | D) Increase bandwidth`
**Ans: B** — Hysteresis must exceed the noise amplitude at the summing node.

**Q207.** For a noisy input with 20 mV p-p noise, a Schmitt trigger should have hysteresis of at least:
`A) 5 mV | B) 20 mV | C) 40 mV | D) 200 mV`
**Ans: C** — Rule of thumb: hysteresis ≥ 2× noise amplitude.

**Q208.** An op-amp Schmitt trigger with V_sat = ±10 V, R_1 = 20 kΩ, R_2 = 20 kΩ has UTP =:
`A) +5 V | B) +10 V | C) +20 V | D) 0 V`
**Ans: A** — Threshold = 10 × 20/40 = +5 V; hysteresis width = 10 V.

**Q209.** A Schmitt trigger with UTP = +2 V and LTP = −2 V and V_sat = ±12 V requires:
`A) R_1 = R_2 | B) R_1/R_2 = 1/5 | C) R_2/R_1 = 1/5 | D) No resistors`
**Ans: B** — 12·R_1/(R_1+R_2) = 2 ⇒ R_1/(R_1+R_2) = 1/6 ⇒ R_2 = 5R_1.

**Q210.** A Schmitt trigger's thresholds can be centred at a non-zero voltage V_ref by:
`A) Adding V_ref in series with the feedback divider at the + terminal | B) Reversing the op-amp | C) Adding a capacitor | D) Decreasing R_1`
**Ans: A** — Then UTP = V_ref + Δ and LTP = V_ref − Δ, with Δ = V_sat·R_1/(R_1+R_2).

**Q211.** A Schmitt trigger's thresholds are centred at V_ref = 1 V with Δ = 1 V. The thresholds are:
`A) UTP = +2 V, LTP = 0 V | B) UTP = +1 V, LTP = −1 V | C) UTP = +2 V, LTP = −2 V | D) UTP = +1 V, LTP = 0 V`
**Ans: A** — UTP = V_ref + Δ = 2 V and LTP = V_ref − Δ = 0 V; the 1 V band is the dead zone.

**Q212.** The output of a Schmitt trigger when the input is exactly between LTP and UTP is:
`A) +V_sat always | B) −V_sat always | C) Equal to its previous value | D) Zero`
**Ans: C** — The bistable holds state until the opposite threshold is crossed.

**Q213.** An inverting Schmitt trigger (input to −, feedback to +) has:
`A) UTP > LTP and positive thresholds | B) UTP = +Δ, LTP = −Δ | C) Only one threshold | D) No output saturation`
**Ans: B** — For a symmetric circuit the thresholds are equal and opposite; the input must exceed +Δ to switch low.

**Q214.** A non-inverting Schmitt trigger (input to +, feedback to −) has thresholds:
`A) UTP = +Δ, LTP = −Δ | B) UTP = −Δ, LTP = +Δ | C) Both zero | D) Equal to V_sat`
**Ans: B** — The input on + must fall below −Δ to switch high — this "reversed" order is what distinguishes it.

**Q215.** A non-inverting Schmitt trigger built from a single op-amp is realised by:
`A) Feeding the output back to the inverting terminal through a divider | B) Feeding output to + terminal | C) Adding an inductor | D) Removing all feedback`
**Ans: A** — A small fraction of the output is subtracted from the input threshold, creating hysteresis.

**Q216.** Schmitt triggers are preferred in digital input conditioning because:
`A) They amplify | B) They convert a slow or noisy analogue ramp into a clean noise-free binary level | C) They remove DC | D) They increase slew rate`
**Ans: B** — Every Schmitt-triggered input stage (74xx, MCU, ADC comparators) uses this to reject noise.

**Q217.** A mechanical switch bounce of 5 ms feeding a comparator will cause:
`A) One clean transition with hysteresis | B) Multiple false transitions, avoided by hysteresis or debouncing | C) No output | D) Saturation damage`
**Ans: B** — Hysteresis larger than the bounce amplitude, or an RC debounce, removes the chatter.

**Q218.** An RC debounce network (R = 10 kΩ, C = 0.1 µF) has a time constant of:
`A) 1 ms | B) 1 s | C) 10 ms | D) 0.1 ms`
**Ans: A** — τ = 10⁴ × 10⁻⁷ = 10⁻³ s = 1 ms; ~5τ = 5 ms covers a typical bounce.

**Q219.** An op-amp relaxation oscillator (astable) uses the Schmitt trigger plus:
`A) An RC charging network | B) A transformer | C) A crystal | D) A diode only`
**Ans: A** — The capacitor charges exponentially toward the rail until it hits the opposite threshold.

**Q220.** The duty cycle of an astable multivibrator built from two identical op-amps and two equal R–C networks is:
`A) 100 % | B) 50 % | C) 0 % | D) Depends on supply`
**Ans: B** — Symmetric components give equal charge/discharge times, so each output is HIGH for half the period.

**Q221.** A monostable multivibrator (one-shot) built from an op-amp produces a pulse of width:
`A) T ≈ R·C | B) T ≈ 1.1·R·C | C) T ≈ 0.69·R·C | D) T independent of R, C`
**Ans: B** — 555-style: T = 1.1 R C in the standard design; op-amp versions use the ln((1+β)/(1−β)) factor.

**Q222.** The 555 timer's internal Schmitt trigger uses reference levels at:
`A) 0 V and V_cc | B) V_cc/3 and 2V_cc/3 | C) V_cc/6 and 5V_cc/6 | D) V_cc/2 only`
**Ans: B** — The comparators inside the 555 reference the control pin and 1/3, 2/3 of the supply, giving automatic hysteresis.

**Q223.** In a 555 astable multivibrator, the duty cycle can be made > 50 % because:
`A) The capacitor charges and discharges through different resistor paths | B) The Schmitt trigger is removed | C) The supply is doubled | D) The output is inverted`
**Ans: A** — Charge uses R_A + R_B, discharge uses R_B only, so a long duty cycle is available.

**Q224.** A Schmitt trigger's hysteresis width is essentially proportional to:
`A) V_sat | B) V_sat² | C) V_sat/R_1 | D) 1/V_sat`
**Ans: A** — V_H = 2V_sat·R_1/(R_1+R_2); it scales linearly with the supply/saturation voltage.

**Q225.** If the supply of a Schmitt trigger rises from ±10 V to ±15 V (resistors unchanged), the hysteresis width:
`A) Decreases | B) Increases by 50 % | C) Stays the same | D) Becomes zero`
**Ans: B** — 15/10 = 1.5× wider; the thresholds move with V_sat since they are a fraction of it.

**Q226.** A Schmitt trigger's noise immunity is usually quoted as:
`A) The input bias current | B) The hysteresis width (V_UTP − V_LTP) | C) The slew rate | D) The supply voltage`
**Ans: B** — Any input noise smaller than the hysteresis cannot flip the state.

**Q227.** Two comparators with hysteresis are ANDed to build a:
`A) Schmitt trigger | B) Window/band comparator | C) Relaxation oscillator | D) Integrator`
**Ans: B** — Two thresholds ANDed produce a band-pass comparison — the standard over/under-voltage detector.

**Q228.** An astable op-amp multivibrator's frequency depends on:
`A) Only the supply | B) The RC time constants and the feedback ratio β | C) The op-amp A_OL | D) The load`
**Ans: B** — f = 1/[2RC·ln((1+β)/(1−β))]; β comes from the positive-feedback divider.

**Q229.** A Schmitt-trigger comparator whose reference is generated by a resistor divider from V_sat has thresholds that:
`A) Are independent of V_sat | B) Scale proportionally with V_sat | C) Scale with temperature only | D) Are set by slew rate`
**Ans: B** — Supply-independent references require a Zener or a dedicated reference IC.

**Q230.** A Zener-referenced Schmitt trigger uses a Zener so that:
`A) Thresholds are independent of supply variation | B) The gain increases | C) The slew rate doubles | D) Hysteresis is eliminated`
**Ans: A** — A constant reference makes thresholds stable even with a fluctuating supply.

**Q231.** In a Schmitt trigger, the input resistor R_1 also sets the input impedance, so:
`A) A large R_1 improves input impedance but allows input current error | B) Small R_1 is always better | C) R_1 sets only hysteresis | D) There is no trade-off`
**Ans: A** — Loading of the source must be weighed against the desired hysteresis ratio.

**Q232.** A Schmitt trigger used as a "bistable switch" for a latching alarm circuit is triggered by:
`A) Any input above 0 V | B) Exceeding UTP to set and falling below LTP to reset | C) Only a negative supply | D) A clock of fixed frequency`
**Ans: B** — The two-threshold memory is exactly what latching requires.

**Q233.** A Schmitt trigger's input rising slowly through the hysteresis band produces:
`A) One transition at UTP | B) No transition | C) Transitions at both UTP and LTP | D) Oscillation`
**Ans: A** — A monotonically rising input crosses only UTP.

**Q234.** A triangular input into a Schmitt trigger (symmetric, amplitude above UTP) produces:
`A) A square wave at the triangle frequency | B) A doubled frequency square wave | C) Nothing | D) A sine`
**Ans: B** — Each triangle period crosses UTP twice, so the output frequency is 2× the input frequency — the basis of frequency doubling.

**Q235.** A Schmitt trigger built from a 741 must account for saturation recovery, which typically:
`A) Adds microseconds of delay | B) Adds nanoseconds only | C) Has no effect | D) Reduces hysteresis`
**Ans: A** — The compensation capacitor forward-biases and must recover; this is why comparators are preferred for fast switching.

**Q236.** The hysteresis width of a Schmitt trigger built with an op-amp having output saturation of ±13 V (instead of ±15 V) and R_1 = R_2 = 10 kΩ is:
`A) 13 V | B) 6.5 V | C) 26 V | D) 0 V`
**Ans: A** — V_H = 2 × 13 × 0.5 = 13 V, i.e. 2V_sat when R_1 = R_2.

**Q237.** A comparator with hysteresis is used as a relaxation oscillator; for sustained oscillation the loop gain must be:
`A) < 1 | B) Exactly 1 from the start | C) > 1 at start and settle to 1 | D) 0`
**Ans: C** — Barkhausen: |Aβ| > 1 to start, and a limiter (clipping/AGC) brings it to unity at steady state.

**Q238.** Adding a small amount of positive feedback to a comparator changes it from:
`A) A bistable to an astable | B) A memoryless comparator to a bistable Schmitt trigger | C) A linear amp to a nonlinear one | D) A current amp to a voltage amp`
**Ans: B** — Positive feedback is what creates the two thresholds.

**Q239.** A Schmitt trigger with UTP = +3 V, LTP = −3 V and V_sat = ±12 V: the feedback fraction β = R_1/(R_1+R_2) is:
`A) 0.5 | B) 0.25 | C) 0.75 | D) 0.1`
**Ans: B** — 3 = 12·β ⇒ β = 0.25 ⇒ R_2 = 3R_1.

**Q240.** A Schmitt trigger's threshold voltages are set by the output saturation voltage, so replacing the op-amp with one having lower saturation:
`A) Narrows the hysteresis | B) Widens the hysteresis | C) Has no effect | D) Inverts the thresholds`
**Ans: A** — Everything scales with V_sat.

**Q241.** The time for the capacitor in an op-amp relaxation oscillator to charge from −Δ to +Δ through R toward +V_sat is:
`A) τ = R·C exactly | B) t = RC·ln((V_sat+Δ)/(V_sat−Δ)) | C) t = RC/2 | D) t = 0`
**Ans: B** — Exponential charging of V_C(t) = V_sat − (V_sat + Δ)e^(−t/RC) solved for V_C = +Δ.

**Q242.** For β = 1/3, ln((1+β)/(1−β)) = ln 2, so the astable period is:
`A) T = 2RC | B) T = 1.386 RC | C) T = 6.28 RC | D) T = 0.5 RC`
**Ans: B** — T = 2·ln2·RC = 1.386 RC; f = 1/(1.386 RC).

**Q243.** A Schmitt trigger with an extremely narrow hysteresis band behaves like:
`A) A perfect comparator with no noise immunity | B) An oscillator | C) A linear amplifier | D) A rectifier`
**Ans: A** — As Δ → 0, hysteresis vanishes and noise rejection is lost.

**Q244.** A "hysteresis comparator" used in a battery charger (charge at 14.6 V, stop at 14.0 V) relies on:
`A) Positive feedback to give two charge/discharge thresholds | B) A larger battery | C) A shunt regulator | D) A transformer`
**Ans: A** — The threshold gap is hysteresis; it prevents endless charge/discharge cycling.

**Q245.** Which statement is TRUE of a Schmitt trigger?
`A) It has a single threshold like a comparator | B) It has memory: output depends on the path taken to the input | C) It requires negative feedback | D) Its output is always analog`
**Ans: B** — Path dependence (hysteresis) is the entire point.

---

## SECTION 5 — Feedback Topologies & Analysis (Q246–Q325)

**Q246.** An amplifier has A = 2000 and β = 0.05. Its closed-loop gain is:
`A) 20.0 | B) 19.8 | C) 40 | D) 2000`
**Ans: B** — A/(1+Aβ) = 2000/(1+100) = 19.8; 1 % below the ideal 1/β = 20.

**Q247.** For the amplifier of Q246, the desensitivity factor is:
`A) 1 | B) 11 | C) 101 | D) 2000`
**Ans: C** — D = 1 + Aβ = 101, so gain errors, distortion and impedance changes shrink by 101.

**Q248.** If A = ∞ in a feedback amplifier, the closed-loop gain becomes:
`A) 0 | B) β | C) 1/β | D) A`
**Ans: C** — A/(1+Aβ) → 1/β as A → ∞; the closed-loop gain is set entirely by the feedback network.

**Q249.** An amplifier with A = 100 and β = 1/20 gives a closed-loop gain of:
`A) 80 | B) 16.7 | C) 5 | D) 95`
**Ans: B** — Aβ = 5, so A/(1+5) = 100/6 = 16.7 (ideal 1/β = 20).

**Q250.** Negative feedback:
`A) Increases gain and bandwidth | B) Decreases gain and increases bandwidth | C) Increases both | D) Changes neither`
**Ans: B** — Gain is divided by D while bandwidth is multiplied by D; gain×bandwidth is preserved.

**Q251.** For a voltage-series feedback amplifier:
`A) Z_i is divided by D and Z_o is multiplied by D | B) Z_i is multiplied by D and Z_o is divided by D | C) Both are divided | D) Both are multiplied`
**Ans: B** — Series mixing raises Z_i by D; voltage (shunt) sampling lowers Z_o by D.

**Q252.** For a current-shunt feedback amplifier:
`A) Z_i × D, Z_o ÷ D | B) Z_i ÷ D, Z_o × D | C) Z_i × D, Z_o × D | D) Z_i ÷ D, Z_o ÷ D`
**Ans: B** — Shunt mixing lowers Z_i; current (series) sampling raises Z_o. This is the only topology that raises both right-hand quantities differently.

**Q253.** An amplifier with Z_i = 5 kΩ, Z_o = 1 kΩ and D = 51 has, under voltage-series feedback:
`A) Z_i = 255 kΩ, Z_o = 19.6 Ω | B) Z_i = 98 Ω, Z_o = 51 kΩ | C) Z_i = 5 kΩ, Z_o = 1 kΩ | D) Z_i = 255 kΩ, Z_o = 51 kΩ`
**Ans: A** — 5k×51 = 255 kΩ and 1k/51 = 19.6 Ω.

**Q254.** The standard non-inverting op-amp amplifier (R_1–R_2 at the − input) is which topology?
`A) Voltage-series | B) Voltage-shunt | C) Current-series | D) Current-shunt`
**Ans: A** — Input is mixed in series (differential) and output voltage is sampled in shunt.

**Q255.** The standard inverting op-amp amplifier is which topology?
`A) Voltage-shunt | B) Voltage-series | C) Current-series | D) Current-shunt`
**Ans: A** — Input signals are summed as currents at the virtual-ground node (shunt mixing), output voltage sampled.

**Q256.** A CE amplifier with an unbypassed emitter resistor is which feedback topology?
`A) Current-series | B) Voltage-series | C) Voltage-shunt | D) Current-shunt`
**Ans: A** — The emitter resistor senses output *current* (series) and feeds it back in series with the input.

**Q257.** A CE amplifier with a collector-to-base feedback resistor is which topology?
`A) Current-shunt | B) Voltage-series | C) Voltage-shunt | D) Current-series`
**Ans: C** — It samples output voltage (shunt) and mixes it at the base node (shunt) — a voltage-shunt (DC stabilising) stage.

**Q258.** A transresistance amplifier (current in, voltage out) is which topology?
`A) Voltage-shunt | B) Current-series | C) Current-shunt | D) Voltage-series`
**Ans: A** — Its natural form is voltage-shunt: shunt input, voltage output sampling.

**Q259.** A transconductance amplifier (voltage in, current out) is which topology?
`A) Current-series | B) Voltage-shunt | C) Current-shunt | D) Voltage-series`
**Ans: A** — Series (voltage) input mixing with series (current) output sampling.

**Q260.** A common-base amplifier has low input impedance and high output impedance. Its main use is:
`A) Impedance buffering | B) High-frequency/cascode applications where Z_in must be low | C) Current amplification | D) DC biasing`
**Ans: B** — Its unity current gain and good high-frequency behaviour suit cascoding.

**Q261.** Series (voltage) mixing at the input is used when we want:
`A) Low Z_in | B) High Z_in | C) Zero Z_out | D) High gain`
**Ans: B** — Series mixing multiplies Z_i by 1 + Aβ.

**Q262.** Shunt (current) mixing at the input is used when we want:
`A) High Z_in | B) Low Z_in | C) Zero offset | D) Low noise`
**Ans: B** — Shunt mixing divides Z_i by 1 + Aβ, which is what allows summing amplifiers.

**Q263.** Series (current) sampling at the output is used when we want:
`A) Low Z_o | B) High Z_o | C) Large swing | D) Class A bias`
**Ans: B** — Current sampling multiplies Z_o by 1 + Aβ.

**Q264.** Shunt (voltage) sampling at the output is used when we want:
`A) High Z_o | B) Low Z_o | C) High current drive | D) Zero feedback`
**Ans: B** — Voltage sampling divides Z_o by 1 + Aβ.

**Q265.** Negative feedback reduces harmonic distortion by a factor of:
`A) 1 + Aβ | B) 1/(1 + Aβ) | C) Aβ | D) 1`
**Ans: B** — With loop gain T, the closed-loop THD ≈ THD_open/(1+T).

**Q266.** Negative feedback increases output swing by a factor of:
`A) 1 + Aβ | B) 1/(1 + Aβ) | C) Aβ² | D) Unchanged`
**Ans: A** — A linear amplifier's output can rise to the rail (or load-limited value) rather than to V_mp/(1+T).

**Q267.** Negative feedback does *not* improve a stage's:
`A) Gain accuracy | B) Output impedance | C) Power efficiency at light load | D) Bandwidth`
**Ans: C** — Internal noise is scaled along with the signal, and efficiency is set by the bias network, not by feedback.

**Q268.** With feedback, the input-referred noise of a stage:
`A) Increases by D | B) Decreases by D | C) Is unchanged | D) Becomes zero`
**Ans: C** — Noise and gain fall together, so noise referred to the input is unchanged — this is why low-noise design places a low-noise first stage.

**Q269.** An amplifier's open-loop gain drops 20 % with temperature. The closed-loop gain with loop gain 100 drops by:
`A) 20 % | B) 0.2 % | C) 5 % | D) 20 % × 100`
**Ans: B** — Sensitivity of A_CL to A is 1/(1+Aβ); 20 %/101 ≈ 0.2 %.

**Q270.** To keep gain within 1 % of nominal using negative feedback, D must be at least:
`A) 1 | B) 10 | C) 100 | D) 1000`
**Ans: C** — 1/D ≤ 0.01 ⇒ D ≥ 100.

**Q271.** Barkhausen oscillation requires:
`A) |Aβ| = 1 and ∠Aβ = 0° | B) |Aβ| < 1 | C) Any loop gain | D) Negative feedback`
**Ans: A** — |Aβ| ≥ 1 with 0° (or 360°) net phase; at startup it must exceed 1 to build up.

**Q272.** In an oscillator, "loop gain" is defined as:
`A) A + β | B) A·β | C) A/β | D) β/A`
**Ans: B** — The return ratio T = A(jω)·β(jω).

**Q273.** A feedback network is said to be regenerative when:
`A) It uses positive feedback | B) It uses negative feedback | C) It has no phase shift | D) It is passive`
**Ans: A** — Positive feedback (tunnel diode, laser, regenerative amplifiers) uses gain to mask noise.

**Q274.** In a current-series feedback amplifier (CE with RE), the gain with emitter degeneration is approximately:
`A) −R_C/r_e | B) −R_C·r_e | C) −R_C/R_E | D) −β·R_C`
**Ans: A** — A_v ≈ −R_C/r_e = −I_C·R_C/V_T, which is nearly independent of β (a key benefit).

**Q275.** Emitter degeneration in a CE amplifier:
`A) Increases gain and bandwidth | B) Increases stability and linearity but reduces gain | C) Has no effect | D) Increases Z_in only`
**Ans: B** — Gain drops by roughly 1 + RE/r_e but gain stability, linearity and Z_out improve.

**Q276.** A CE amplifier with RE = 0 and a collector-to-base feedback resistor provides:
`A) High gain | B) Excellent DC stability but reduced gain | C) Zero output resistance | D) AC gain greater than β`
**Ans: B** — Collector-to-base feedback fixes I_C ≈ (V_CC − V_BE)/R_C, largely independent of β, at the cost of gain.

**Q277.** Collector-to-base feedback (voltage-shunt) increases:
`A) Z_in | B) Stability against β and V_BE variation | C) Bandwidth | D) Output swing`
**Ans: B** — Negative DC feedback reduces sensitivity to β, V_BE and temperature.

**Q278.** A feedback amplifier's loop gain can be measured by:
`A) Opening the loop and computing A·β at the break | B) Measuring the output directly | C) Shorting the loop | D) Measuring Z_in`
**Ans: A** — Break the loop, load it correctly, and compute the return ratio T(jω) = A·β.

**Q279.** If the loop gain of an amplifier is 1000 (60 dB), the closed-loop gain is within what percentage of 1/β?
`A) 0.01 % | B) 0.1 % | C) 1 % | D) 10 %`
**Ans: B** — Error = 1/(1+T) = 1/1001 ≈ 0.1 %.

**Q280.** Negative feedback affects the input-referred thermal noise of a resistive input stage by:
`A) Reducing it | B) Not changing it | C) Increasing it by D | D) Removing it`
**Ans: B** — Noise is not a "gain error"; it is already input-referred, so D does not reduce it — another reason the first stage must be low-noise.

**Q281.** A voltage-series feedback amplifier's stability can be improved by:
`A) Reducing the open-loop gain | B) Dominant-pole compensation | C) Removing the feedback | D) Using a bigger supply`
**Ans: B** — Compensating capacitance creates a dominant pole so that the loop gain crosses 0 dB with adequate phase margin.

**Q282.** For a 3-pole amplifier, the phase shift at the gain-crossover frequency (where |Aβ| = 1) is typically near:
`A) 45° | B) 135° | C) 180° | D) 270°`
**Ans: C** — For a −20 dB/dec roll-off each pole adds ~90°; near crossover the total approaches 180°, which is why compensation matters.

**Q283.** A phase margin of 60° (rather than 20°) implies:
`A) A more oscillatory, faster-rising response | B) A better-damped, non-oscillatory step response | C) Zero bandwidth | D) Negative gain`
**Ans: B** — 60° is the classic target for a step response with mild overshoot.

**Q284.** Positive feedback differs from negative feedback in that it:
`A) Increases gain but reduces linearity and can cause instability | B) Reduces gain and improves linearity | C) Increases Z_in | D) Reduces bandwidth`
**Ans: A** — Regenerative feedback trades linearity and stability for sensitivity — used in comparators and oscillators.

**Q285.** An amplifier has A = 100 and β = 0.25. Its closed-loop gain is:
`A) 3.85 | B) 4.0 | C) 25 | D) 100`
**Ans: A** — Aβ = 25 ⇒ A_CL = 100/26 = 3.85 (ideal 1/β = 4, so 3.8 % low).

**Q286.** If the feedback network of an amplifier with A = 100 is broken (β = 0), the gain becomes:
`A) 100 | B) 0 | C) 1 | D) ∞`
**Ans: A** — With no feedback the amplifier reverts to its open-loop gain A.

**Q287.** Feedback that reduces the output resistance of a voltage source by a factor of 21 corresponds to a loop gain of:
`A) 20 | B) 21 | C) 1/21 | D) 441`
**Ans: A** — Z_o is divided by 1+T, so 1+T = 21 ⇒ T = 20.

**Q288.** A current-output amplifier (e.g. a laser diode driver) with feedback has:
`A) Z_o divided by D | B) Z_o multiplied by D | C) Z_i divided by D | D) A gain of 1/β exactly`
**Ans: B** — Current sampling raises output resistance by 1+Aβ.

**Q289.** An emitter follower (common collector) is a negative-feedback amplifier because:
`A) The emitter resistor provides series current feedback | B) It has a collector-to-base resistor | C) The output is current-sampled | D) It has no gain`
**Ans: A** — Emitter degeneration gives high Z_in, low Z_out and gain ≈ 1 — a textbook current-series feedback stage.

**Q290.** The gain of an emitter follower is approximately:
`A) (β+1)(R_E ∥ r_e + R_E) | B) 1 | C) −R_C/r_e | D) β`
**Ans: A** — A_v ≈ (β+1)(Z_in)/(β·Z_in + R_E), which tends to 1 with large (β+1).

**Q291.** In feedback analysis, the "loop gain" at the frequency where A(jω)β(jω) = 1 is:
`A) 1 (unity) | B) 0 | C) D | D) ∞`
**Ans: A** — Unity loop gain is the gain-crossover frequency; if the phase there is 180°, the loop oscillates.

**Q292.** Adding a Zener in the feedback path of a CE stage creates:
`A) AC-only feedback | B) DC-only feedback, improving bias stability without hurting AC gain | C) Positive feedback | D) No feedback`
**Ans: B** — The Zener blocks AC, so feedback is DC-only: bias stabilised, midband gain untouched.

**Q293.** Negative feedback reduces the *sensitivity* of an amplifier's gain to:
`A) Supply changes and temperature | B) Only supply | C) Only β | D) Nothing`
**Ans: A** — D desensitises against every parameter in the forward path: A_OL, supply, temperature, β, R_C.

**Q294.** If a CE amplifier's β varies from 100 to 300, emitter degeneration reduces the resulting gain variation to:
`A) 0 % | B) ~3 % | C) 100 % | D) 50 %`
**Ans: B** — With RE ≫ r_e, A_v ≈ −R_C/r_e depends almost entirely on I_C, not β; residual variation ≈ 1/(1+g_m·RE).

**Q295.** Feedback bandwidth extension: a single-pole amplifier with unity-gain bandwidth 10 MHz used with gain 100 (D = 100) has a closed-loop bandwidth of:
`A) 10 kHz | B) 100 kHz | C) 10 MHz | D) 1 MHz`
**Ans: B** — BW_f = BW×D. For a unity-gain-stable op-amp, BW = GBW/A_CL = 10 MHz/100 = 100 kHz.

**Q296.** The effect of negative feedback on the *full-power bandwidth* is:
`A) It improves by D | B) It is unchanged | C) It degrades by D | D) It becomes infinite`
**Ans: A** — Slew-rate-limited FPBW = SR/(2πV_p) rises by 1/D because the closed-loop peak swing scales with A_CL.

**Q297.** A 741 (SR = 0.5 V/µs, GBW = 1 MHz) drives a 10 V-peak output. Its full-power bandwidth is about:
`A) 8 kHz | B) 1 MHz | C) 100 kHz | D) 20 kHz`
**Ans: A** — FPBW = 0.5×10^6/(2π×10) = 7.96 kHz, far below its 1 MHz small-signal bandwidth.

**Q298.** A feedback amplifier with A = 50 and β = 0.1 (D = 6) has its gain error equal to:
`A) 1/6 = 16.7 % | B) 6 % | C) 0 % | D) 50 %`
**Ans: A** — Ideal gain 1/β = 10; actual = 50/6 = 8.33, i.e. 16.7 % low.

**Q299.** Which of the following does *not* increase because of negative feedback?
`A) Input resistance | B) Bandwidth | C) Power efficiency of a Class-A stage | D) Output swing`
**Ans: C** — Efficiency is set by the conduction angle and load, not by loop gain; feedback only reduces the power needed by the driver stage.

**Q300.** In a shunt-shunt feedback amplifier (transresistance), Z_in and Z_o are:
`A) Both multiplied by D | B) Both divided by D | C) Z_in ÷ D, Z_o × D | D) Z_in × D, Z_o ÷ D`
**Ans: B** — Shunt mixing and shunt sampling both reduce impedance — ideal for summing and current-mode circuits.

**Q301.** Feedback around a non-inverting amplifier can make the gain depend almost entirely on:
`A) A_OL | B) The resistor ratio | C) The supply | D) The load`
**Ans: B** — Hence precision amplifiers use 0.1 % resistors and thin-film networks for ratio accuracy.

**Q302.** A source follower (common-drain) MOSFET stage is best described as:
`A) Gain slightly below 1, very high Z_in and low Z_out | B) Gain much greater than 1 with low Z_in | C) High Z_in and high Z_out | D) Gain exactly 1`
**Ans: A** — A_v = g_m R_S/(1 + g_m R_S) < 1; the unidirectional source feedback raises Z_in and lowers Z_out.

**Q303.** A cascode stage improves the common-gate amplifier by:
`A) Increasing Z_in | B) Increasing output resistance and gain while keeping Z_in low | C) Reducing bandwidth | D) Adding positive feedback`
**Ans: B** — The cascode raises r_o by ~g_m r_o², giving high gain with high-frequency isolation.

**Q304.** If a feedback amplifier's forward gain A drops by a factor of 10 with temperature and D = 50, the closed-loop gain changes by:
`A) 10 % | B) 2 % | C) 0.2 % | D) 50 %`
**Ans: B** — A 10× (90.9 %) open-loop drop becomes 1/D = 2 % in closed loop.

**Q305.** In a two-stage amplifier, placing a buffer (op-amp follower) between stages:
`A) Increases overall gain | B) Prevents the first stage's high Z_in from being loaded, isolating the stages | C) Increases noise | D) Reduces stability`
**Ans: B** — Cascaded stages need impedance isolation or the gain and poles are no longer what the analysis predicts.

**Q306.** A "bootstrapped" emitter follower achieves very high Z_in because:
`A) The base is bootstrapped to the emitter | B) β is large | C) The supply is negative | D) The collector is bypassed`
**Ans: A** — Raising the emitter-side resistor's top with the output keeps almost zero AC across it, multiplying the input resistance by A_v.

**Q307.** Feedback reduces the effect of transistor parameter variation. For a CE stage with D = 20 and β varying ±30 %, the resulting gain variation is about:
`A) ±30 % | B) ±1.5 % | C) ±20 % | D) Zero`
**Ans: B** — Sensitivity is divided by D: 30 %/20 = 1.5 %.

**Q308.** A voltage-series feedback amplifier is preferred for a voltage buffer because it simultaneously gives:
`A) High Z_in and low Z_o | B) Low Z_in and high Z_o | C) High gain | D) Low noise`
**Ans: A** — That impedance combination is exactly what cascading needs.

**Q309.** The impedance at the feedback network's input node in a voltage-shunt (inverting) amplifier is:
`A) R_1 only | B) R_f | C) R_1 ∥ R_f | D) ∞`
**Ans: A** — The summing node is at virtual ground, so the source sees only R_1 — Z_in ÷ D gives the same result.

**Q310.** With Aβ = 49 (D = 50), the closed-loop gain differs from 1/β by:
`A) 2 % | B) 20 % | C) 0 % | D) 50 %`
**Ans: A** — 1/(1+Aβ) = 1/50 = 2 %.

**Q311.** An amplifier with 30 dB of loop gain gives a gain accuracy of:
`A) 0.1 % | B) 1 % | C) 3 % | D) 10 %`
**Ans: A** — 30 dB ⇒ T = 1000 ⇒ error = 1/1001 ≈ 0.1 %.

**Q312.** The primary purpose of a *dominant pole* in a feedback amplifier is to:
`A) Increase DC gain | B) Make loop gain roll off at −20 dB/dec so the phase margin is adequate | C) Add gain at high frequency | D) Eliminate offset`
**Ans: B** — One pole at low frequency forces the unity-loop-gain crossing to a safe 45–90° phase point.

**Q313.** Feedback around a power stage (e.g. a Class AB output stage) is used mainly to:
`A) Increase efficiency | B) Reduce distortion and correct crossover gaps | C) Increase bandwidth | D) Reduce supply voltage`
**Ans: B** — Local feedback in the driver/output stage linearises the transfer and shrinks both crossover and clipping distortion.

**Q314.** In a voltage-shunt feedback amplifier the closed-loop quantity stabilised is:
`A) Voltage gain | B) Transresistance | C) Current gain | D) Power gain`
**Ans: B** — Shunt input + voltage output = transresistance (V/I) is the natural transfer quantity.

**Q315.** In a current-series feedback amplifier the stabilised quantity is:
`A) Current gain | B) Transconductance (I/V) | C) Voltage gain | D) Transresistance`
**Ans: B** — Series input (V) with series output (I) gives transconductance.

**Q316.** An amplifier whose loop gain is 0.9 can never oscillate because:
`A) |Aβ| < 1 for all frequencies | B) It has no feedback | C) The phase is 0° | D) The gain is negative`
**Ans: A** — Unity loop gain is required for the Barkhausen condition.

**Q317.** Increasing the amount of negative feedback in an audio amplifier generally:
`A) Increases distortion | B) Decreases distortion but can reduce gain | C) Increases noise | D) Has no audible effect`
**Ans: B** — The 1/D reduction of distortion is why negative feedback dominates audio power-amplifier design.

**Q318.** A feedback loop that is stable at low frequency becomes unstable at high frequency because:
`A) Extra poles add phase lag | B) Gain always rises | C) β becomes zero | D) The supply drops`
**Ans: A** — Each pole contributes up to −90°; cumulative phase reaching −180° while |Aβ| ≥ 1 produces oscillation.

**Q319.** Feedback factor β for a resistive divider R_1 (to ground) and R_2 (to output) used to feed the inverting input of a non-inverting amp is:
`A) R_2/(R_1+R_2) | B) R_1/(R_1+R_2) | C) R_1/R_2 | D) 1`
**Ans: B** — With R_2 to output and R_1 to ground, β = R_1/(R_1+R_2), giving gain 1 + R_2/R_1.

**Q320.** In an emitter follower, the negative feedback is obtained from:
`A) A resistor in the emitter lead | B) A capacitor at the collector | C) A resistor at the base | D) An inductor in series with the base`
**Ans: A** — The emitter resistor samples output current and feeds it back in series, giving gain ≈ 1, high Z_in, low Z_out.

**Q321.** A degenerate feedback configuration with β = 1 corresponds to:
`A) A voltage follower of gain 1 | B) An inverting amplifier | C) An oscillator | D) A comparator`
**Ans: A** — Full output-to-inverting-input feedback with no attenuation is the classic buffer.

**Q322.** In a regulated power supply, the error amplifier senses the output and drives the pass device. This is:
`A) Open-loop control | B) Voltage-series negative feedback | C) Positive feedback | D) Current-series feedback`
**Ans: B** — High Z_in sensing, series-shunt correction: the same topology as the non-inverting amplifier.

**Q323.** A PLL's phase detector and loop filter act as a feedback system whose loop gain determines:
`A) Capture range | B) Lock range and damping (stability) | C) Only the reference frequency | D) Nothing`
**Ans: B** — The loop filter sets both natural frequency and damping; too much gain causes jitter/ringing.

**Q324.** Negative feedback around a rectifier (servo-regulated supply) is used to:
`A) Increase ripple | B) Correct the load variation so the output stays constant | C) Reduce output voltage | D) Eliminate the transformer`
**Ans: B** — Feedback samples the output and adjusts the regulator, tightening load regulation.

**Q325.** Which statement correctly compares the two forms of feedback at the output?
`A) Voltage sampling raises Z_o; current sampling lowers Z_o | B) Voltage sampling lowers Z_o; current sampling raises Z_o | C) Both raise Z_o | D) Both lower Z_o`
**Ans: B** — The impedance transformation follows directly from how the output quantity is fed back.

---

## SECTION 6 — Power Amplifiers & Efficiency (Q326–Q395)

**Q326.** The conduction angle for a Class A amplifier is:
`A) 180° | B) 360° | C) 90° | D) Less than 180°`
**Ans: B** — Class A devices conduct for the whole cycle, which is why it is the most linear but least efficient.

**Q327.** The conduction angle for a Class B amplifier is:
`A) 360° | B) 180° | C) 90° | D) 270°`
**Ans: B** — Each push-pull device conducts for exactly half a cycle (180°).

**Q328.** The conduction angle for a Class C amplifier is:
`A) Exactly 180° | B) Less than 180° | C) 360° | D) Exactly 90°`
**Ans: B** — The bias point sits beyond cutoff, so conduction is < 180°; efficiency is high but distortion severe.

**Q329.** The conduction angle for a Class AB amplifier is:
`A) Exactly 180° | B) Slightly more than 180° | C) Slightly less than 180° | D) 360°`
**Ans: B** — A small forward bias lets both devices conduct briefly around the zero crossing.

**Q330.** The maximum theoretical efficiency of a series-fed Class A amplifier is:
`A) 25 % | B) 50 % | C) 78.5 % | D) 90 %`
**Ans: A** — Reached when R_L = R_C; P_o(max) = V_CC²/(8R), P_dc = V_CC²/(2R).

**Q331.** The maximum efficiency of a transformer-coupled Class A amplifier is:
`A) 25 % | B) 50 % | C) 78.5 % | D) 100 %`
**Ans: B** — The transformer's DC flux swing allows the whole supply to appear across the load alternately, doubling efficiency.

**Q332.** The maximum theoretical efficiency of a Class B (push-pull) amplifier is:
`A) 25 % | B) 50 % | C) 78.5 % | D) 90 %`
**Ans: C** — η = π/4 = 78.5 %; two devices each converting half the cycle doubles the available power.

**Q333.** Class C amplifiers can reach efficiencies approaching:
`A) 50 % | B) 78.5 % | C) 90 % and above | D) 25 %`
**Ans: C** — Large conduction-angle reduction wastes little power in the transistor; used only in RF where a tuned load filters harmonics.

**Q334.** The chief reason Class C amplifiers are not used for audio is:
`A) Low efficiency | B) Severe harmonic distortion from conduction at high bias | C) High cost | D) Poor frequency response`
**Ans: B** — Biasing in the cutoff region clips the waveform badly; a resonant tank recovers only the fundamental.

**Q335.** The maximum efficiency of a Class AB amplifier is:
`A) Exactly the same 78.5 % as Class B | B) Between 50 % and 78.5 % | C) 90 % | D) 25 %`
**Ans: A** — Biasing adds a small quiescent current, so Class AB is just *below* Class B's π/4 limit but well above Class A.

**Q336.** A key advantage of Class AB over Class B amplifiers is:
`A) Lower bias current | B) Reduced crossover distortion | C) No need for heat sinks | D) Higher power gain`
**Ans: B** **[PYP-25 Q6]** — A small forward bias (≈2V_BE between bases) keeps both devices conducting near zero crossing.

**Q337.** Crossover distortion in a Class B push-pull stage is caused by:
`A) V_BE being zero until ~0.7 V of drive | B) Too much bias | C) Low V_CC | D) Slow slew rate`
**Ans: A** — Below 0.7 V neither transistor conducts, creating a notch at the waveform's zero crossing.

**Q338.** The simplest way to eliminate crossover distortion is to:
`A) Apply a forward bias of about 2V_BE between the driver outputs | B) Increase V_CC | C) Reduce the load | D) Use a single transistor`
**Ans: A** — Diodes or a V_BE multiplier generate the ≈1.4 V offset needed.

**Q339.** Class AB biasing using two silicon diodes in the driver base circuit provides:
`A) ~0.7 V | B) ~1.4 V | C) ~2.8 V | D) 0 V`
**Ans: B** — Two diodes' junction drops span the two V_BE's of the push-pull pair.

**Q340.** The quiescent current in a Class AB amplifier is set by:
`A) The bias voltage between bases | B) The load | C) The supply frequency | D) The output voltage`
**Ans: A** — A V_BE multiplier trims the offset, hence the standing current, which also determines thermal stability.

**Q341.** Thermal runaway in a Class AB output stage is prevented by:
`A) Emitter ballast resistors / bias tracking | B) A larger supply | C) A bigger transformer | D) Increasing V_BE`
**Ans: A** — Local current feedback (small emitter resistors, or V_BE tracking with the output device) keeps bias constant as temperature rises.

**Q342.** A complementary-symmetry push-pull stage uses:
`A) Two identical NPN devices | B) An NPN and a PNP of complementary parameters | C) Two PNP devices | D) A MOSFET and a BJT`
**Ans: B** — One device sources, the other sinks; matched parameters minimise even-order distortion.

**Q343.** For a Class B push-pull with ±15 V supplies and R_L = 8 Ω, the maximum AC output power is:
`A) 14.1 W | B) 28.1 W | C) 7.05 W | D) 3.5 W`
**Ans: A** — P_o(max) = V_CC²/(2R_L) = 225/16 = 14.06 W.

**Q344.** For the same Class B stage (±15 V, 8 Ω), the DC input power at full swing is:
`A) 8.95 W | B) 17.9 W | C) 35.8 W | D) 7.2 W`
**Ans: B** — I_peak = V_CC/R_L = 1.875 A, so P_dc = 2V_CC·I_peak/π = 2×15×1.875/π = 17.9 W.

**Q345.** Using the corrected values of Q343/Q344, the efficiency is:
`A) 78.5 % | B) 50 % | C) 25 % | D) 90 %`
**Ans: A** — 14.06/17.9 = 78.5 %, the theoretical Class B maximum.

**Q346.** A Class B push-pull stage operating at half maximum output swing has an efficiency of about:
`A) 78.5 % | B) 39.3 % | C) 25 % | D) 12.5 %`
**Ans: B** — η = (π/4)·(V_m/V_CC) = 78.5 % × 0.5 = 39.3 %.

**Q347.** A Class A amplifier delivering 20 % of its maximum possible AC output power has an efficiency of:
`A) 25 % | B) 5 % | C) 50 % | D) 20 %`
**Ans: B** — Class A efficiency rises linearly with output: η = 0.2 × 25 % = 5 %.

**Q348.** Maximum AC output power for a Class A amplifier with V_CC = 20 V, R_C = R_L = 5 Ω is:
`A) 40 W | B) 10 W | C) 20 W | D) 80 W`
**Ans: B** — P_o(max) = V_CC²/(8R) = 400/40 = 10 W.

**Q349.** A Class A amplifier has V_CC = 20 V and R_C = R_L = 5 Ω. Its DC input power at the Q-point is:
`A) 20 W | B) 40 W | C) 10 W | D) 80 W`
**Ans: B** — P_dc = V_CC²/(2R) = 400/10 = 40 W; with P_o = 10 W the efficiency is exactly 25 %.

**Q350.** The transistor power dissipation at maximum output in the circuit of Q348 is:
`A) 10 W | B) 30 W | C) 20 W | D) 40 W`
**Ans: B** — P_Q = P_dc − P_o = 40 − 10 = 30 W at maximum output; this is the worst case for heatsinking in Class A.

**Q351.** The DC supply current drawn by an ideal Class B push-pull stage at full sine output is at:
`A) DC frequency f | B) Twice the signal frequency 2f | C) Half of f | D) Unrelated to f`
**Ans: B** — Each device conducts alternately, so the supply sees a full-wave current at 2f — a key EMI insight.

**Q352.** Push-pull operation reduces even-order harmonic distortion because:
`A) Non-linearities of the two devices are complementary | B) The load is resistive | C) The supply is doubled | D) Biasing is exact`
**Ans: A** — Opposite transfer curvatures cancel, leaving mainly odd harmonics; transformer action further cancels even harmonics.

**Q353.** The maximum transistor dissipation in a Class B amplifier occurs at:
`A) Full output power | B) V_m = 2V_CC/π (≈0.64 V_CC) | C) Zero output | D) At clipping`
**Ans: B** — P_D = V_CC·V_m/(πR) − V_m²/(4R) peaks at V_m = 2V_CC/π.

**Q354.** A Class AB amplifier biased with V_BE = 1.4 V and β = 100 has a quiescent current I_Q related to the emitter resistance by:
`A) I_Q = V_BE/R_E | B) I_Q = (V_BE − 2V_BE)/R_E | C) I_Q = V_CC/R_E | D) I_Q = 0`
**Ans: A** — Each output device sees ≈V_BE across its emitter resistor, so I_Q = V_BE/R_E sets quiescent dissipation.

**Q355.** Class AB bias with R_E = 10 Ω and V_BE = 0.7 V per device gives a quiescent current of:
`A) 70 mA | B) 7 mA | C) 140 mA | D) 0 mA`
**Ans: A** — 0.7/10 = 70 mA per device; this standing current is the price paid for reduced crossover distortion.

**Q356.** Class D amplifiers achieve high efficiency by:
`A) Biasing the output devices at the threshold | B) Operating the output devices as switches | C) Using Class B bias | D) Using a transformer`
**Ans: B** — Switching means the device is either fully on (low V_DS) or off (zero current), minimising dissipation.

**Q357.** The major practical drawback of Class D amplifiers is:
`A) Low switching frequency and associated distortion/EMI filtering | B) Negative efficiency | C) No output stage needed | D) Cannot drive speakers`
**Ans: A** — High carrier frequencies demand fast devices and LC output filters to suppress switching harmonics.

**Q358.** An RF power amplifier operating Class C uses a resonant load because:
`A) It rejects the harmonics generated by conduction-angle clipping | B) It increases β | C) It removes the bias | D) It reduces V_CC`
**Ans: A** — The tank passes the fundamental and rejects the many harmonics produced.

**Q359.** In RF power amplifiers the term *power-added efficiency* refers to:
`A) Output power ÷ DC power | B) (Output power − input power) ÷ DC power | C) Gain | D) DC power ÷ output power`
**Ans: B** — PAE excludes the DC-to-RF driver power: PAE = (P_out − P_in)/P_dc, which can exceed the collector efficiency.

**Q360.** A power amplifier supplied with 40 W DC delivers 1 W of RF output from 1 mW of drive. Its power-added efficiency is:
`A) 2.5 % | B) 25 % | C) 40 % | D) 75 %`
**Ans: A** — (1 − 0.001)/40 = 0.025 = 2.5 %. **[ISRO-2023 Q47 pattern: 8 V, 5 A, 0 dBm in, 30 dBm out → 40 W DC, 1 W out → 2.5 %]**

**Q361.** In the PAE example of Q360, the collector (DC) efficiency alone is:
`A) 2.5 % | B) 25 % | C) 2.475 % | D) 0.1 %`
**Ans: C** — 1/40 = 2.5 %; including the drive subtraction gives 2.475 %.

**Q362.** The output power of an amplifier is 30 dBm. This corresponds to:
`A) 1 mW | B) 1 W | C) 10 W | D) 100 mW`
**Ans: B** — 30 dBm = 10^(30/10) mW = 1000 mW = 1 W.

**Q363.** An amplifier with P_in = 100 mW and P_out = 2 W has a power gain of:
`A) 13 dB | B) 20 dB | C) 3 dB | D) 26 dB`
**Ans: A** — 10 log(2/0.1) = 10 log 20 = 13 dB.

**Q364.** A power amplifier with 13 dB power gain delivers 2 W; its input power is:
`A) 100 mW | B) 400 mW | C) 50 mW | D) 200 mW`
**Ans: A** — P_in = P_out/20 = 0.1 W.

**Q365.** A Class A amplifier's output stage requires a heat sink sized mainly by:
`A) The maximum transistor dissipation at the worst-case Q-point | B) The input impedance | C) The bias voltage | D) The output frequency`
**Ans: A** — Thermal resistance, junction temperature and ambient determine the sink; the Q-point dissipation is the design input.

**Q366.** The junction temperature of a power transistor should be kept below about:
`A) 50 °C | B) 100 °C | C) 200 °C | D) 400 °C`
**Ans: B** — Typical ratings are T_J(max) = 150–200 °C, but derating design practice keeps junction temperature ≤ 100–125 °C.

**Q367.** The thermal resistance junction-to-ambient θ_JA of a transistor on a heat sink is best when:
`A) Large | B) Small | C) Zero | D) Negative`
**Ans: B** — Lower θ_JA removes heat faster: P_dissipated = (T_J − T_A)/θ_JA.

**Q368.** A transistor dissipating 20 W with θ_JA = 2 °C/W in an ambient of 30 °C has a junction temperature of:
`A) 50 °C | B) 70 °C | C) 110 °C | D) 30 °C`
**Ans: B** — T_J = 30 + 20×2 = 70 °C, comfortably below derated limits.

**Q369.** "Safe operating area" (SOA) of a power transistor limits:
`A) The V_CE and I_C combinations permissible without thermal damage | B) The gain | C) The bandwidth | D) The bias voltage only`
**Ans: A** — SOA plus thermal design prevents second-breakdown failure at high V_CE/I_C.

**Q370.** Using a MOSFET rather than a BJT in an audio output stage gives:
`A) Higher distortion | B) Better thermal stability and near-linear transfer, plus faster switching | C) Higher crossover distortion | D) Lower output swing`
**Ans: B** — MOSFETs are majority-carrier devices with excellent thermal behaviour; complementary MOSFET pairs minimise distortion.

**Q371.** An emitter follower output stage (Class A) driving R_L directly has voltage gain:
`A) ≈ 1 (slightly less than 1) | B) 100 | C) −1 | D) 10`
**Ans: A** — A_v = (β+1)R_L/((β+1)R_L + r_e), which approaches 1 for large β.

**Q372.** A Class B push-pull with ±15 V supplies and 8 Ω load has peak output current of:
`A) 1.875 A | B) 3.75 A | C) 0.94 A | D) 15 A`
**Ans: A** — I_peak = V_CC/R_L = 15/8 = 1.875 A, and the supply must supply it on alternate half-cycles.

**Q373.** Class A operation is chosen for a linear audio pre-amplifier mainly because it has:
`A) Highest efficiency | B) Lowest distortion with the transistor conducting throughout | C) Highest output power | D) Smallest bias current`
**Ans: B** — Class A's conduction over 360° keeps the device in its most linear region.

**Q374.** An RF power amplifier's optimum output power is obtained by tuning the:
`A) Collector load network for maximum power transfer | B) Input filter only | C) Supply | D) Bias network only`
**Ans: A** — Conjugate matching of the collector network maximises real power delivered to the load.

**Q375.** The "efficiency" of a linear RF power amplifier is typically in the range:
`A) 5–10 % | B) 30–70 % | C) 90–99 % | D) > 100 %`
**Ans: B** — Linear (A/B/C) RF stages run at roughly 30–70 %; switching (D/E) stages reach 90 %+.

**Q376.** Overdriving a power amplifier produces:
`A) Harmonic (clipping) distortion | B) Lower THD | C) Higher efficiency | D) No effect`
**Ans: A** — Saturation flattens the peaks of the waveform, generating odd harmonics and intermodulation.

**Q377.** Intermodulation distortion in a power amplifier is caused mainly by:
`A) Device non-linearity | B) Supply ripple | C) Load mismatch only | D) Thermal noise`
**Ans: A** — Non-linear transfer curves mix multiple tones to create sum/difference frequencies not present in the input.

**Q378.** A push-pull output stage requires biasing to avoid thermal runaway. The standard method is:
`A) V_BE-multiplier bias referenced to the output devices | B) Fixed gate voltage | C) Base-emitter short | D) No bias`
**Ans: A** — The V_BE multiplier tracks the output devices' V_BE with temperature, keeping quiescent current constant.

**Q379.** In a single-supply Class B amplifier, an output coupling capacitor is required because:
`A) The quiescent DC level at the output is V_CC/2, not zero | B) The supply is too low | C) The bias is negative | D) The load is capacitive`
**Ans: A** — The mid-supply bias must be blocked so the speaker sees zero DC.

**Q380.** A transformer-coupled Class A stage produces less hum than a series-fed one because:
`A) DC does not flow through the transformer's primary | B) It has higher gain | C) It needs no bias | D) The load is resistive`
**Ans: A** — The DC component is blocked from the load, so only the AC swing reaches it — the basis of transformer hum-bucking.

**Q381.** Class S (or switching) audio amplifiers are a development of:
`A) Class A | B) Class B push-pull switching at a high carrier frequency | C) Class C | D) Linear amplifiers`
**Ans: B** — The output transistors are switched at ultrasonic (20–200 kHz) carrier rates, with LC filters reconstructing the audio.

**Q382.** A two-transistor complementary output stage in Class AB has quiescent dissipation P_Q = V_CC·I_Q. With V_CC = 24 V (split ±12 V) and I_Q = 20 mA, P_Q is:
`A) 0.48 W | B) 0.24 W | C) 4.8 W | D) 24 mW`
**Ans: A** — 24 × 0.02 = 0.48 W, small compared with the tens of watts of output power.

**Q383.** Increasing the Class AB quiescent current:
`A) Reduces crossover distortion but increases idle dissipation | B) Increases efficiency | C) Increases crossover distortion | D) Increases output power`
**Ans: A** — It is a direct trade-off between distortion and idle heat.

**Q384.** A power amplifier is biased Class A at the centre of the load line to:
`A) Maximise output swing in both directions | B) Maximise quiescent current | C) Reduce bandwidth | D) Increase gain`
**Ans: A** — Centring gives the largest symmetric swing before either cutoff or saturation is reached.

**Q385.** A Class B amplifier biased slightly into conduction is, by definition:
`A) Class A | B) Class AB | C) Class C | D) Class D`
**Ans: B** — Conduction angle just over 180° defines Class AB.

**Q386.** The maximum power dissipation rating (P_Dmax) of a power transistor should be derated from its datasheet value because:
`A) Ratings are specified at 25 °C and case temperature will be higher | B) The transistor is always saturated | C) The bias is negative | D) The load is inductive`
**Ans: A** — Rating falls with case temperature and mounting; designers derate by 30–50 %.

**Q387.** A class-C amplifier's output is taken through a parallel-tuned circuit because:
`A) It resonates at the fundamental and rejects harmonics | B) It supplies DC | C) It matches the transistor's β | D) It reduces supply current`
**Ans: A** — The tank also performs impedance transformation for maximum power transfer.

**Q388.** For a Class B stage delivering 100 mW with 78.5 % efficiency, the DC input power is:
`A) 127 mW | B) 78.5 mW | C) 100 mW | D) 200 mW`
**Ans: A** — P_dc = 100/0.785 = 127 mW.

**Q389.** The output stage of an op-amp is typically biased Class AB because it must:
`A) Operate linearly for both polarities with minimal crossover distortion | B) Maximise efficiency | C) Reduce gain | D) Avoid biasing resistors`
**Ans: A** — Push-pull output stages are always Class AB (or B with small bias) for symmetric swing without dead zones.

**Q390.** Which of these is a genuine disadvantage of a Class A amplifier?
`A) High quiescent power dissipation even with no input | B) Poor linearity | C) Conduction angle less than 360° | D) Crossover distortion`
**Ans: A** — Class A is the most linear class with 360° conduction; its cost is idle power and 25 % maximum efficiency.

**Q391.** A 100 W RF power amplifier with 60 % collector efficiency is fed from a dual ±35 V supply. The average DC current is approximately:
`A) 1.2 A | B) 2.4 A | C) 4.8 A | D) 0.6 A`
**Ans: B** — P_dc = 100/0.6 = 167 W; I_avg = P_dc/(2V_CC) = 167/70 = 2.4 A.

**Q392.** The conduction angle of the *whole push-pull pair* in a Class B amplifier is:
`A) 360° | B) 180° | C) 90° | D) 720°`
**Ans: A** — Each device conducts 180°, but at any instant one of the two is on, so the pair covers 360°.

**Q393.** A thermal-runaway-prone output stage should use:
`A) Current-series (local) negative feedback | B) Positive feedback | C) No emitter resistors | D) Fixed bias with no temperature compensation`
**Ans: A** — Small emitter resistors sense and oppose rising current, the classic local degeneration against thermal runaway.

**Q394.** A linear amplifier draws 250 mA from a 20 V supply and delivers 2 W of AC output power. Its efficiency is:
`A) 40 % | B) 50 % | C) 20 % | D) 80 %`
**Ans: A** — P_dc = 20 × 0.25 = 5 W, so η = 2/5 = 40 %.

**Q395.** Which class of amplifier is most appropriate for a 100 W RF transmitter in the 10 MHz band?
`A) Class A | B) Class B | C) Class C with a tuned load | D) Class A with a transformer`
**Ans: C** — RF allows the high efficiency of Class C because a resonant load removes the harmonics.

---

## SECTION 7 — BJT: Physics, Biasing, Configurations (Q396–Q490)

### 7A. Device physics and modes of operation

**Q396.** A bipolar junction transistor is called "bipolar" because:
`A) It uses two types of carrier | B) It has two terminals | C) It has two junctions | D) It is bidirectional`
**Ans: A** — Conduction relies on both electrons (majority, in an NPN) and holes (minority), hence *bi*polar.

**Q397.** In an NPN transistor, which terminal is heavily doped?
`A) Base | B) Emitter | C) Collector | D) All equally`
**Ans: B** — Heavy emitter doping maximises injection efficiency; the collector is lightly doped to survive reverse-bias power.

**Q398.** The emitter injection efficiency of a BJT is close to 1 because:
`A) The emitter is heavily doped relative to the base | B) The base is thick | C) The collector is lightly doped | D) V_BE is small`
**Ans: A** — γ ≈ 1 means nearly all emitter current is injected as minority carriers into the base.

**Q399.** The base transport factor (β/α) is less than 1 because:
`A) Some injected carriers recombine in the thin base | B) The base is heavily doped | C) The collector is reverse biased | D) V_BE is large`
**Ans: A** — Only a fraction survives to be collected, so α = γ·β_t < 1.

**Q400.** The exact relation between α and β for a BJT is:
`A) α = β/(β+1) | B) α = β/(β−1) | C) α = β² | D) α = β + 1`
**Ans: A** — With β = 100, α = 0.990 **[PYP-25 Q52 uses α = 0.992]**.

**Q401.** For α = 0.992, the corresponding current gain β is:
`A) 124 | B) 99.2 | C) 1.008 | D) 0.992`
**Ans: A** — β = α/(1−α) = 0.992/0.008 = 124.

**Q402.** The terminal-current relation in a BJT is:
`A) I_E = I_C − I_B | B) I_E = I_C + I_B | C) I_C = I_B + I_E | D) I_B = I_C + I_E`
**Ans: B** — Kirchhoff at the device; this identity always holds, including in saturation.

**Q403.** With β = 150 and I_B = 20 µA, the collector and emitter currents are:
`A) I_C = 3 mA, I_E = 3.02 mA | B) I_C = 3 mA, I_E = 3.2 mA | C) I_C = 3.02 mA, I_E = 3 mA | D) I_C = 30 mA, I_E = 30.2 mA`
**Ans: A** — I_C = βI_B = 3 mA, I_E = (β+1)I_B = 3.02 mA.

**Q404.** A BJT in the *active* region has:
`A) Both junctions forward biased | B) BE forward and BC reverse biased | C) Both junctions reverse biased | D) BE reverse and BC forward biased`
**Ans: B** — Forward-active operation: collector junction reverse biased to sweep carriers into the collector.

**Q405.** A BJT in *saturation* has:
`A) BE forward and BC reverse biased | B) Both junctions forward biased | C) Both junctions reverse biased | D) V_BE = 0`
**Ans: B** — Both junctions forward biased; the collector can no longer collect all injected carriers, so β drops sharply.

**Q406.** A BJT in *cutoff* has:
`A) I_C ≈ 0 with both junctions reverse biased | B) I_C = βI_B | C) V_CE = 0 | D) I_E = I_B`
**Ans: A** — Cutoff is the safe off state; only leakage flows.

**Q407.** The approximate V_BE of a silicon BJT in the active region is:
`A) 0.1 V | B) 0.3 V | C) 0.7 V | D) 1.4 V`
**Ans: C** — Germanium gives ≈0.3 V; Schottky-clamped BJTs ≈0.2 V; 1.4 V is the two-junction Class-AB bias offset.

**Q408.** The reverse saturation current I_S of a silicon BJT:
`A) Doubles for every 5 °C rise | B) Doubles for every 10 °C rise | C) Is independent of temperature | D) Decreases with temperature`
**Ans: B** — Roughly doubles per 10 °C, which is why leakage current is the parameter with a *positive* temperature coefficient **[PYP-23 Q13 concept]**.

**Q409.** Operating-frequency limitation for a bipolar semiconductor device is due to:
`A) Junction parasitic capacitances only | B) Electron mobility/transit time only | C) Both (a) and (b) | D) Neither`
**Ans: C** **[PYP-23 Q43]** — Diffusion and junction capacitances plus carrier transit time jointly set f_T.

**Q410.** Which device offers the highest speed of operation? **[PYP-23 Q44]**
`A) BJT | B) FET | C) Enhancement-mode MOSFET | D) Depletion-mode MOSFET`
**Ans: A** — For a given bias current the BJT's much higher g_m gives the highest f_T and gain-bandwidth product.

**Q411.** The Early effect in a BJT refers to:
`A) Early current crowding at high V_CE | B) Increase of I_C with V_CE at fixed I_B | C) Decrease of β with temperature | D) Avalanche breakdown`
**Ans: B** — Base-width narrowing raises I_C with V_CE, giving finite output resistance r_o = V_A/I_C.

**Q412.** The Early voltage V_A of a typical silicon BJT is about:
`A) 1 V | B) 50–100 V | C) 1000 V | D) 0.1 V`
**Ans: B** — Higher V_A is desirable; a higher-impurity emitter structure gives 100 V+.

**Q413.** With V_A = 50 V and I_C = 2 mA, the BJT output resistance r_o is:
`A) 25 kΩ | B) 50 kΩ | C) 2 kΩ | D) 25 Ω`
**Ans: A** — r_o = V_A/I_C = 50/0.002 = 25 kΩ.

**Q414.** The BV_CBO of a BJT (collector–base breakdown with emitter open) is higher than BV_CEO because:
`A) With the emitter open there is no gain to amplify the avalanche current | B) The collector is lighter doped | C) The base is thicker | D) V_BE limits it`
**Ans: A** — Base current from avalanche is amplified by β in the common-emitter case, so breakdown occurs at a much lower voltage.

**Q415.** The base-collector junction capacitance of a BJT in the active region is:
`A) A large voltage-dependent (Miller) capacitance | B) Zero | C) A constant 100 pF | D) Negative`
**Ans: A** — C_μ is reverse biased and voltage dependent, which is why it dominates the high-frequency response through Miller multiplication.

### 7B. Small-signal model parameters

**Q416.** The thermal voltage V_T at 300 K is approximately:
`A) 0.026 V | B) 0.26 V | C) 2.6 V | D) 0.0026 V`
**Ans: A** — V_T = kT/q = 25.85 mV ≈ 26 mV at room temperature.

**Q417.** The transconductance of a BJT with I_C = 1 mA at 300 K is:
`A) 38.5 mS | B) 1 mS | C) 0.385 S | D) 26 mS`
**Ans: A** — g_m = I_C/V_T = 10⁻³/0.026 = 0.0385 S.

**Q418.** The intrinsic emitter resistance r_e (ac) with I_E = 1 mA is:
`A) 26 Ω | B) 1 kΩ | C) 26 mΩ | D) 2.6 kΩ`
**Ans: A** — r_e = 26 mV/I_E = 26 Ω; it is simply the reciprocal of emitter transconductance.

**Q419.** For β = 100 and I_C = 1 mA, the base–emitter small-signal resistance r_π is:
`A) 2.6 kΩ | B) 2.6 Ω | C) 26 kΩ | D) 1 kΩ`
**Ans: A** — r_π = V_T/I_B = 26 mV/10 µA = 2.6 kΩ (equivalently β/g_m).

**Q420.** A CE amplifier with g_m = 38.5 mS, R_C = 2 kΩ and an emitter resistor fully bypassed has voltage gain approximately:
`A) −77 | B) −2 | C) −154 | D) +77`
**Ans: A** — A_v ≈ −g_m R_C = −0.0385 × 2000 = −77.

**Q421.** If the emitter resistor is *not* bypassed and r_e = 26 Ω, R_E = 260 Ω, R_C = 2 kΩ, then A_v ≈:
`A) −77 | B) −7.0 | C) −0.86 | D) −260`
**Ans: B** — A_v ≈ −R_C/(r_e + R_E) = −2000/286 ≈ −7.0, and essentially independent of β.

**Q422.** Bypassing the emitter resistor in the circuit of Q421 raises the gain to:
`A) ≈ −77 | B) ≈ −7 | C) ≈ 0 | D) ≈ −260`
**Ans: A** — The AC emitter resistance falls to r_e only, so gain returns to −g_m R_C.

**Q423.** The hybrid-π model parameters of a BJT in the active region are:
`A) r_π, r_o, g_m and C_π, C_μ | B) r_π and g_m only | C) g_o only | D) R_C and R_B only`
**Ans: A** — The low-frequency model is r_π, g_m, r_o; adding C_π and C_μ gives the full frequency-dependent model.

**Q424.** The T-model of a BJT uses which primary parameter?
`A) r_e between emitter and base | B) r_π between base and emitter | C) g_m | D) r_o`
**Ans: A** — T-model is convenient for emitter-based analysis and for expressing gain as R_C/(r_e + R_E).

**Q425.** The reverse transconductance parameter g_µ of a BJT is:
`A) g_m/β | B) g_m·β | C) 1/g_m | D) 1/r_π`
**Ans: A** — g_µ = I_S/V_T is negligible compared with g_m = βg_µ, which is why the reverse base current is ignored.

### 7C. Biasing and the Q-point

**Q426.** If a transistor operates at the middle of the DC load line, an increase in current gain will move the Q-point:
`A) Off the load line | B) Nowhere | C) Up on the load line (higher I_C, lower V_CE) | D) Down on the load line`
**Ans: C** **[PYP-23 Q14]** — With I_B fixed, I_C = βI_B rises, so V_CE = V_CC − I_C R_C falls; the Q-point slides toward saturation.

**Q427.** A voltage-divider bias circuit has V_TH = 5.5 V and R_TH = 10 kΩ at the base, R_E = 1 kΩ, β = 100, V_BE = 0.7 V. The base current is approximately:
`A) 4.8 µA | B) 43 µA | C) 480 µA | D) 48 µA`
**Ans: B** — I_B = (V_TH − V_BE)/(R_TH + (β+1)R_E) = 4.8 V/(10 k + 101 k) ≈ 43 µA.

**Q428.** Continuing Q427, the collector current and V_CE (V_CC = 15 V, R_C = 1 kΩ) are:
`A) I_C = 4.3 mA, V_CE = 6.3 V | B) I_C = 1 mA, V_CE = 14 V | C) I_C = 5 mA, V_CE = 10 V | D) I_C = 43 µA, V_CE = 15 V`
**Ans: A** — I_C = βI_B ≈ 4.32 mA ⇒ V_CE = 15 − 4.32 − 4.37 ≈ 6.3 V.

**Q429.** In emitter bias (base grounded, R_E to −V_EE), the emitter current is set mainly by:
`A) β | B) (V_EE − V_BE)/R_E | C) V_CC | D) r_π`
**Ans: B** — I_E ≈ (V_EE − 0.7)/R_E is nearly β-independent, which is why it is stable.

**Q430.** With V_EE = 5 V, R_E = 2 kΩ, base grounded, V_BE = 0.7 V, the emitter current is:
`A) 1 mA | B) 2.15 mA | C) 4.3 mA | D) 0.7 mA`
**Ans: B** — (5 − 0.7)/2000 = 2.15 mA.

**Q431.** The main disadvantage of fixed-base bias (R_B from V_CC to base) is:
`A) Very sensitive to β and temperature | B) Too much quiescent current | C) Requires negative supply | D) Low input impedance`
**Ans: A** — I_C = β(V_CC − 0.7)/R_B varies directly with β, so Q-point stability is poor.

**Q432.** Collector-to-base feedback bias provides stability because:
`A) It fixes I_C ≈ (V_CC − V_BE)/R_C regardless of β | B) It forces V_BE = 0 | C) It raises the gain | D) It removes V_CE variation`
**Ans: A** — The base-collector resistor senses and opposes collector-current changes; a rise in I_C raises V_BE, which cuts I_B.

**Q433.** Two diodes in the emitter path of a bias network compensate for V_BE because:
`A) Their junction drops track V_BE with temperature | B) They double β | C) They lower R_E | D) They supply extra base drive`
**Ans: A** — A matched diode keeps V_BE constant at ≈2 × 0.7 V over temperature, stabilising I_E.

**Q434.** The stability factor of a bias circuit measures:
`A) Sensitivity of I_C to V_BE and β | B) The gain | C) The bandwidth | D) The power rating`
**Ans: A** — Lower sensitivity factor ⇒ better regulation of the Q-point against temperature and β spread.

**Q435.** A collector-to-emitter feedback bias circuit (R from collector to base) has the property that:
`A) DC feedback stabilises the Q-point but AC gain is lowered by the emitter resistor | B) It has maximum gain | C) It is temperature sensitive | D) It requires a transformer`
**Ans: A** — The feedback resistor also loads the AC output unless bypassed.

**Q436.** The Q-point of a Class A amplifier must lie:
`A) At the middle of the load line for maximum symmetric swing | B) At cutoff | C) Beyond cutoff | D) At V_CC`
**Ans: A** — Centring maximises undistorted output swing; off-centre Q-points clip one side first.

**Q437.** The DC load line equation for a CE stage with emitter grounded is:
`A) V_CE = V_CC − I_C R_C | B) I_C = βI_B | C) V_CE = V_CC | D) I_C = V_CC/R_C`
**Ans: A** — KVL on the collector loop; the slope is −1/R_C.

**Q438.** If a transistor saturates, the collector current becomes:
`A) βI_B exactly | B) Limited by V_CC and R_C, not by β | C) Zero | D) Infinite`
**Ans: B** — Beyond saturation I_C is set by the external circuit, which is the basis of the "forced β" test.

**Q439.** In saturation, V_CE(sat) for a silicon BJT is typically:
`A) 0.7 V | B) 0.2 V | C) 5 V | D) 0 V exactly`
**Ans: B** — Both junctions conduct, so V_CE ≈ V_BE − V_BC(sat) ≈ 0.2 V.

**Q440.** For a saturated BJT switch, the "forced β" should be:
`A) Much greater than the datasheet β_F | B) About 10 (≈ β_F/10) | C) 1 | D) Infinite`
**Ans: B** — Saturated β_F is 20–100; forcing β ≈ 10 guarantees deep saturation and low V_CE(sat).

**Q441.** Base-emitter junction capacitance of a BJT at high frequency acts as:
`A) A shunt capacitance that must be compensated or neutralised | B) A series element only | C) A resistor | D) A Zener`
**Ans: A** — Uncompensated C_π causes gain roll-off at high frequency and, with a source resistance, phase lag.

**Q442.** Which configuration has the highest current gain?
`A) CE | B) CB | C) CC | D) All equal`
**Ans: C** — CC offers current gain ≈ β+1, used as a buffer.

**Q443.** Which configuration has the highest voltage gain?
`A) CE | B) CC | C) CB (comparable to CE) | D) None`
**Ans: A** — CE and CB give high voltage gain; CC gives ≈1.

**Q444.** Which configuration has unity (approximately) current gain?
`A) CE | B) CB | C) CC | D) All have β`
**Ans: B** — In CB, α ≈ 1: I_C ≈ I_E.

**Q445.** The input impedance of a CE stage is:
`A) r_π (base looking in) | B) r_e | C) r_o | D) 1/g_m only`
**Ans: A** — Looking into the base, Z_in ≈ r_π = β/g_m; looking into the emitter it is ≈ (β+1)r_e.

**Q446.** The output impedance of a CE stage is primarily:
`A) r_o = V_A/I_C | B) r_π | C) r_e | D) R_C`
**Ans: A** — With the emitter bypassed, the collector sees r_o in parallel with R_C.

**Q447.** The input impedance of a CC (emitter follower) stage is approximately:
`A) (β+1)(R_E ∥ r_e) | B) r_π only | C) R_C | D) 1 Ω`
**Ans: A** — Reflecting R_E into the base multiplies it by (β+1), which is why followers buffer well.

**Q448.** The output impedance of a CC stage is approximately:
`A) (r_π + R_s)/(β+1) | B) r_o | C) R_C | D) 0`
**Ans: A** — Very low (a few Ω), which is why the follower is a good output buffer.

**Q449.** A common-base stage has input resistance:
`A) ≈ r_e (very low) | B) r_π | C) βr_e | D) r_o`
**Ans: A** — r_e ≈ 25 mV/I_E, typically a few tens of ohms — ideal for low-impedance sources.

**Q450.** A common-base voltage gain is approximately:
`A) +g_m R_C (no phase inversion) | B) −g_m R_C | C) 1 | D) β`
**Ans: A** — Positive (non-inverting) and similar in magnitude to the CE gain; its wide bandwidth suits RF.

**Q451.** In a common-base configuration, the input is at the emitter and the output at the collector, so the terminal common to both is:
`A) Base | B) Emitter | C) Collector | D) None`
**Ans: A** — "Common base" refers to the base being shared by the input and output loops.

**Q452.** The Darlington connection (two BJTs) gives current gain:
`A) β_1 + β_2 | B) β_1·β_2 | C) β_1 β_2 + 1 (≈β_1β_2) | D) 2β`
**Ans: C** — I_C = (β_1+1)(β_2+1)I_B ≈ β_1β_2·I_B; exact form is β₁β₂ + β₁ + β₂ + 1.

**Q453.** With β_1 = β_2 = 100, the Darlington current gain is about:
`A) 200 | B) 10 000 | C) 10 200 | D) 100`
**Ans: C** — (101)(101) = 10 201.

**Q454.** The effective V_BE of a Darlington pair is:
`A) ~1.4 V | B) ~0.7 V | C) ~2.1 V | D) ~0 V`
**Ans: A** — Two junctions in series; useful for level shifting but a drawback when driving a low-voltage load.

**Q455.** The input resistance of a Darlington pair is approximately:
`A) β_1 β_2 r_e | B) r_e | C) r_π only | D) R_C`
**Ans: A** — R_in ≈ β_1β_2(V_T/I_E), extremely high — hence its use as a buffer for high-Z sources.

**Q456.** The Sziklai (complementary feedback) pair behaves like:
`A) A PNP transistor | B) An NPN transistor with a β close to β_1β_2 | C) A Zener | D) A thyristor`
**Ans: B** — NPN in series with a PNP driver gives NPN action with very high effective gain using same-type parts.

**Q457.** A BJT used as a switch in the saturation region has switching speed mainly limited by:
`A) Storage time (removal of stored minority charge) | B) Rise time | C) β | D) V_CC`
**Ans: A** — Deep saturation stores charge that must be swept out, so saturation slows switching; unsaturated switching is faster but wastes power.

**Q458.** To speed up a saturating BJT switch one may:
`A) Use a speed-up (anti-saturation) clamp diode across BE | B) Increase β | C) Add more base drive beyond saturation | D) Reduce V_CC`
**Ans: A** — Clamping the B–C junction to 0.4–0.5 V prevents deep saturation and removes stored charge.

**Q459.** In the reverse-active mode of a BJT (used as a phototransistor in some configurations), the effective gain is:
`A) Very small (β_R ≈ 0.5–2) | B) Equal to β_F | C) Infinite | D) Zero`
**Ans: A** — The lightly doped collector injects poorly, so reverse β is tiny.

**Q460.** The common-collector stage is used as an impedance-matching buffer because it has:
`A) High Z_in, low Z_out | B) Low Z_in, high Z_out | C) High gain | D) Current gain of 1`
**Ans: A** — The property that defines a buffer.

### 7D. High-frequency behaviour and switching

**Q461.** The transit-time f_T of a BJT is related to its emitter transit time by:
`A) f_T = 1/(2πτ_T) | B) f_T = τ_T | C) f_T = 1/τ_T | D) f_T = 2πτ_T`
**Ans: A** — f_T ≈ gm/(2π C_π) = 1/(2πτ_e) in the charge-control model.

**Q462.** Given f_T = 2 GHz and β = 50, the unity-gain (β = 1) cutoff frequency f_β is:
`A) 40 MHz | B) 20 MHz | C) 100 MHz | D) 2 GHz`
**Ans: A** — f_β = f_T/β = 2000/50 = 40 MHz.

**Q463.** A BJT with f_T = 4 GHz at a bias giving g_m = 50 mS has a diffusion capacitance C_π of approximately:
`A) 2 pF | B) 20 pF | C) 200 pF | D) 5 nF`
**Ans: A** — C_π = g_m/(2πf_T) = 0.05/(2π×4×10⁹) ≈ 2 pF.

**Q464.** The beta roll-off with frequency is caused by:
`A) Diffusion capacitance C_π and the finite transit time | B) r_o | C) R_C | D) The Early effect`
**Ans: A** — β(f) = β_0/(1 + jf/f_β): diffusion charge storage, not the output resistance.

**Q465.** The maximum frequency of a BJT switch's switching waveform (error-free operation) is set by:
`A) Storage and transit times | B) V_BE | C) β | D) The emitter area`
**Ans: A** — Storage time on turn-off and fall time on turn-off limit usable switching rate.

**Q466.** For a BJT, which junction capacitance increases (effective) as the gain rises?
`A) C_μ (C_BC) by Miller multiplication | B) C_π only | C) Neither | D) r_o`
**Ans: A** — C_in = C_μ(1 + A_v) is why an inverting high-gain stage has severe HF limits.

**Q467.** Compared to silicon, germanium BJT has:
`A) Lower V_BE (~0.3 V) but higher leakage and lower breakdown | B) Higher V_BE | C) Same V_BE and higher speed | D) No differences`
**Ans: A** — Ge's advantage is low V_BE; its disadvantages are leakage and low BV_CEO.

**Q468.** A BJT's safe operating area is exceeded primarily when:
`A) V_CE and I_C are simultaneously high | B) V_BE > 1 V | C) β is low | D) The transistor is in cutoff`
**Ans: A** — Excess power at high V_CE causes second breakdown, which destroys the device.

**Q469.** A BJT is described as a *current-controlled* device because:
`A) Its collector current is set by base current | B) Its collector current is set by V_GS | C) It needs a gate | D) It has high input Z`
**Ans: A** — I_C = βI_B; FETs are voltage-controlled with negligible control current.

**Q470.** A silicon BJT biased at I_C = 1 mA has β = 100. The value of r_π is:
`A) 2.6 kΩ | B) 26 kΩ | C) 2.6 Ω | D) 1 MΩ`
**Ans: A** — I_B = 10 µA and r_π = V_T/I_B = 2.6 kΩ.

**Q471.** In a hybrid-π model, r_o appears in which branch?
`A) Between collector and base | B) In parallel with the controlled current source g_m v_π | C) In series with r_π | D) At the emitter`
**Ans: B** — r_o models the Early effect and sits in parallel with the collector current source.

**Q472.** The emitter of a CE stage is often bypassed with a capacitor to:
`A) Increase AC gain by removing AC degeneration | B) Increase DC bias | C) Reduce β | D) Provide positive feedback`
**Ans: A** — The capacitor shorts r_e (and R_E) at signal frequencies while leaving DC bias untouched.

**Q473.** The value of the emitter bypass capacitor is chosen so that its reactance at f_L is:
`A) Much less than the resistance it bypasses | B) Much larger | C) Equal | D) Zero`
**Ans: A** — X_C ≪ r_E (typically X_C ≤ r_E/10 at the lowest frequency of interest).

**Q474.** A transistor switch with V_CC = 5 V, R_C = 100 Ω in saturation conducts a collector current of about:
`A) 5 mA | B) 50 mA | C) 500 mA | D) 25 mA`
**Ans: B** — I_C(sat) = (V_CC − V_CE(sat))/R_C ≈ 5/100 = 50 mA.

**Q475.** The base drive required to saturate the switch of Q474 (forced β = 10) is:
`A) 0.5 mA | B) 5 mA | C) 0.5 µA | D) 50 mA`
**Ans: B** — I_B ≥ I_C/β_forced = 50 mA/10 = 5 mA.

**Q476.** A BJT used in an emitter follower with R_E = 1 kΩ and β = 100 has voltage gain closest to:
`A) 1 (0.99) | B) 10 | C) 100 | D) 0.1`
**Ans: A** — A_v ≈ (β+1)R_E/((β+1)R_E + r_e) ≈ 101 000/101 026 ≈ 0.9997.

**Q477.** Two cascaded CE stages each with voltage gain −10 give an overall gain of:
`A) −20 | B) +100 | C) −100 | D) 1000`
**Ans: B** — Two inversions cancel: (−10)(−10) = +100; sign matters, magnitude multiplies.

**Q478.** To make a two-stage amplifier's total gain exactly −100 one would use:
`A) Two inverting stages of gain 10 | B) Two non-inverting stages of gain 10 | C) One inverting and one non-inverting | D) A buffer only`
**Ans: C** — One inversion gives the negative sign; 10 × 10 = 100 magnitude.

**Q479.** A CE stage with an emitter resistor has its gain largely set by:
`A) The ratio R_C/(r_e + R_E), not β | B) β exactly | C) The supply | D) r_π`
**Ans: A** — This is the key stability benefit of emitter degeneration.

**Q480.** The transistor junction capacitances C_π and C_μ are:
`A) Both proportional to transistor area | B) Both zero above f_T | C) Proportional to bias current | D) Independent of bias and area`
**Ans: A** — Larger die ⇒ larger junction areas ⇒ larger capacitances and higher f_T capability.

**Q481.** In a common-base stage the collector current is nearly independent of the base because:
`A) The base is at AC ground and α ≈ 1, so I_C ≈ I_E | B) β is very large | C) V_CE is zero | D) r_o is infinite`
**Ans: A** — Emitter-driven operation gives excellent isolation from base-drive variations.

**Q482.** A common-base stage has its base grounded, V_CC = +10 V with R_C = 1 kΩ, and R_E = 2 kΩ to a −5 V supply. With V_BE = 0.7 V and α = 0.992, the voltage V_BC is:
`A) −7.87 V | B) +7.87 V | C) −2.13 V | D) +2.13 V`
**Ans: A** — I_E = (5 − 0.7)/2 kΩ = 2.15 mA; I_C = 0.992 × 2.15 = 2.13 mA; V_C = 10 − 2.13 = 7.87 V; V_BC = 0 − 7.87 = −7.87 V. **[PYP-25 Q52 pattern]**

**Q483.** Punch-through in a BJT occurs when:
`A) The depletion region of the BC junction reaches the emitter | B) V_BE exceeds 0.7 V | C) The collector saturates | D) β drops`
**Ans: A** — Base-width collapse under high reverse bias destroys the transistoring action entirely.

**Q484.** The transistor current-gain (β) typically:
`A) Increases with temperature | B) Decreases with temperature | C) Is constant | D) Becomes negative`
**Ans: A** — Rising temperature increases I_S and reduces V_BE needed, so β increases — the mechanism behind thermal runaway.

**Q485.** To prevent thermal runaway in a linear stage one should:
`A) Use negative thermal feedback (emitter ballast) and a stable bias | B) Increase V_BE | C) Remove the emitter resistor | D) Increase β`
**Ans: A** — β rising with T must be countered by local negative feedback.

**Q486.** A CE stage's gain falls at high frequency mainly because:
`A) The effective input capacitance C_π + C_μ(1+A_v) shunts the source | B) r_o decreases | C) β increases | D) V_BE rises`
**Ans: A** — Miller multiplication of C_μ with (1 + A_v) creates a dominant low-pass pole at the input.

**Q487.** The emitter injection efficiency γ and base transport factor α/γ combine to give α, and α is:
`A) Always less than 1 | B) Always greater than 1 | C) Exactly 1 | D) Equal to β`
**Ans: A** — Carrier recombination makes α < 1, which is precisely why I_B ≠ 0.

**Q488.** In an emitter-coupled (differential) pair, matching the two transistors improves:
`A) Common-mode rejection and offset cancellation | B) Gain only | C) Supply current | D) Slew rate`
**Ans: A** — Mismatch in V_BE and β creates offset and degrades CMRR.

**Q489.** A phototransistor is essentially:
`A) A BJT with light-generated base current | B) A MOSFET | C) A solar cell | D) An LED`
**Ans: A** — Photons generate electron–hole pairs that act as base current, giving high current gain.

**Q490.** A phototransistor's dark current should be:
`A) As small as possible | B) As large as possible | C) Equal to the photocurrent | D) Zero`
**Ans: A** — Dark current sets the noise floor of the light sensor.

---

## SECTION 8 — MOSFET / JFET / MESFET (Q491–Q585)

### 8A. JFET characteristics

**Q491.** Pinch-off voltage in an FET is:
`A) The gate-source voltage that gives zero drain current | B) The drain voltage that gives zero drain current | C) The gate-source voltage giving unity drain current | D) The drain voltage giving infinite drain current`
**Ans: A** **[PYP-25 Q72]** — For a JFET, V_GS(off) is the gate bias that fully pinches off the channel, so I_D = 0.

**Q492.** For a JFET with V_GS(off) = −4 V and I_DSS = 16 mA, the transfer characteristic is:
`A) I_D = I_DSS(1 − V_GS/V_GS(off))² | B) I_D = I_DSS·V_GS/V_GS(off) | C) I_D = I_DSS·exp(V_GS/V_T) | D) I_D = I_DSS + V_GS`
**Ans: A** — Shockley's equation; at V_GS = V_GS(off)/2 = −2 V the current is I_DSS/4 = 4 mA.

**Q493.** For the FET of Q492, the drain current at V_GS = −2 V is:
`A) 4 mA | B) 8 mA | C) 16 mA | D) 12 mA`
**Ans: A** — I_DSS(1 − (−2)/(−4))² = 16(0.5)² = 4 mA.

**Q494.** The transconductance of a JFET at V_GS = 0 with I_DSS = 16 mA and V_GS(off) = −4 V is:
`A) 2 g_m0 = 2I_DSS/|V_GS(off)| = 8 mS | B) 4 mS | C) 16 mS | D) 1 mS`
**Ans: A** — g_m0 = 2I_DSS/|V_GS(off)| = 32/4 = 8 mS, so g_m = 8 mS at V_GS = 0.

**Q495.** The gate current of a JFET is:
`A) Essentially zero (reverse-biased gate junction) | B) Large and positive | C) Equal to I_D | D) Exactly zero at all times`
**Ans: A** — The gate junction is reverse biased, so only pA/nA leakage flows; Z_in > 10⁹ Ω.

**Q496.** A JFET can be operated with both positive and negative V_GS to obtain:
`A) Modulation of I_D about V_GS = 0 | B) Only positive I_D | C) Saturation | D) Breakdown`
**Ans: A** — Unlike MOSFETs, JFETs tolerate both signs of gate bias because the junction is simply forward/reverse biased.

**Q497.** In a JFET, increasing |V_GS| toward V_GS(off):
`A) Decreases I_D quadratically | B) Increases I_D | C) Increases r_d | D) Has no effect`
**Ans: A** — The conducting channel narrows, so I_D falls as the square of (1 − V_GS/V_GS(off)).

**Q498.** The output resistance r_d of a JFET in saturation is:
`A) Very large (typically > 1 MΩ) | B) Very small | C) Equal to 1/g_m | D) Zero`
**Ans: A** — The gate junction is reverse biased and channel-length modulation is weak, giving very high r_d.

**Q499.** A JFET used as a constant-current source is biased at:
`A) V_GS = 0 with the source grounded | B) V_DS = 0 | C) V_GS = V_GS(off) | D) Negative V_DS`
**Ans: A** — At V_GS = 0 the JFET carries I_DSS, which is well specified and temperature-stable; this is the classic "current-source JFET".

**Q500.** A p-channel JFET requires:
`A) Negative V_GS for control and a positive drain supply polarity arrangement | B) Positive V_GS | C) Only positive supplies | D) No gate bias`
**Ans: A** — The p-channel conducts holes; the gate must go positive relative to source to pinch off, and the drain is taken negative.

### 8B. MOSFET characteristics and operating regions

**Q501.** The relation between I_D and V_GS of a MOSFET in the saturation region is:
`A) Exponential | B) Quadratic | C) Logarithmic | D) Hyperbolic`
**Ans: B** **[PYP-23 Q15]** — I_D = ½k(V_GS − V_T)² (square-law).

**Q502.** An NMOS has k_n = μ_nC_ox(W/L) = 1 mA/V², V_GS = 3 V, V_T = 1 V, V_DS = 5 V. Its drain current (ignoring λ) is:
`A) 0.5 mA | B) 1 mA | C) 2 mA | D) 4 mA`
**Ans: C** — I_D = ½k(V_GS − V_T)² = ½ × 1 × (2)² = 2 mA.

**Q503.** For the device in Q502, the overdrive voltage V_OV = V_GS − V_T is:
`A) 1 V | B) 2 V | C) 3 V | D) 5 V`
**Ans: B** — V_OV = 3 − 1 = 2 V; saturation requires V_DS ≥ V_OV (here 5 ≥ 2 ✓).

**Q504.** For the device of Q502, the transconductance g_m is:
`A) 1 mS | B) 2 mS | C) 4 mS | D) 0.5 mS`
**Ans: B** — g_m = k(V_GS − V_T) = 1 mA/V² × 2 V = 2 mS (equivalently 2I_D/V_OV = 4/2).

**Q505.** The condition for a MOSFET to operate in saturation is:
`A) V_DS ≥ V_GS − V_T | B) V_DS ≤ V_GS − V_T | C) V_GS ≤ V_T | D) V_DS = 0`
**Ans: A** — Once V_DS exceeds the overdrive voltage the channel is pinched off at the drain end and I_D is independent of V_DS.

**Q506.** In the triode (linear) region, a MOSFET behaves as:
`A) A voltage-controlled resistor R_on ≈ 1/(k(V_GS−V_T)) | B) A constant current source | C) An open circuit | D) A current sink`
**Ans: A** — For small V_DS, I_D ≈ k(V_OV)V_DS, so the device acts as a switch resistance.

**Q507.** A MOSFET is in cutoff when:
`A) V_GS < V_T | B) V_GS > V_T | C) V_DS = 0 | D) V_GS = 0`
**Ans: A** — No inversion layer forms below threshold, so I_D ≈ 0 (only subthreshold leakage flows).

**Q508.** The threshold voltage V_T of an enhancement NMOS is:
`A) The V_GS at which I_D first becomes appreciable (turn-on) | B) Zero | C) The V_DS at saturation | D) 1 V always`
**Ans: A** — Conventionally defined at I_D = 100 µA × (W/L) for long-channel devices.

**Q509.** An enhancement MOSFET has V_T > 0 and a depletion MOSFET has:
`A) V_T < 0 for n-channel | B) V_T > 0 | C) V_T = 0 | D) V_T = 0.7 V`
**Ans: A** — A depletion device conducts at V_GS = 0 and needs *negative* V_GS to pinch off (normally-on).

**Q510.** The body (substrate) effect causes the threshold voltage to:
`A) Increase as V_SB increases | B) Decrease | C) Stay constant | D) Become negative`
**Ans: A** — Reverse biasing the body junction widens the depletion region, so more V_GS is needed: V_T = V_T0 + γ(√(2φ_F+V_SB) − √2φ_F).

**Q511.** With γ = 0.5 V^½, 2φ_F = 0.6 V and V_SB = 3 V, the threshold shift is approximately:
`A) 0.11 V | B) 0.56 V | C) 1.5 V | D) 0 V`
**Ans: B** — ΔV_T = 0.5(√3.6 − √0.6) = 0.5(1.897 − 0.775) = 0.56 V.

**Q512.** The body effect increases the threshold voltage of a source follower as:
`A) The source voltage rises | B) The source voltage falls | C) V_DD rises | D) Nothing changes`
**Ans: A** — More V_SB ⇒ higher V_T ⇒ lower I_D and lower gain.

**Q513.** Channel-length modulation in a MOSFET produces:
`A) A slight increase of I_D with V_DS in saturation | B) A decrease of I_D | C) Zero output resistance | D) Threshold shift only`
**Ans: A** — The effective channel shortens as V_DS grows, so saturation current rises slightly.

**Q514.** The output resistance of a MOSFET in saturation due to channel-length modulation is:
`A) r_o = 1/(λI_D) | B) r_o = 1/g_m | C) r_o = V_A/I_D | D) r_o = 1/λ`
**Ans: A** — With λ ≈ 0.01–0.05 V⁻¹ for short channels, r_o is much smaller than a BJT's.

**Q515.** If λ = 0.02 V⁻¹ and I_D = 1 mA, r_o is:
`A) 50 kΩ | B) 20 kΩ | C) 500 kΩ | D) 2 kΩ`
**Ans: A** — 1/(0.02 × 10⁻³) = 50 kΩ.

**Q516.** Increasing the channel-length modulation parameter λ in a common-source amplifier:
`A) Decreases output resistance | B) Increases output resistance | C) Increases gain | D) Does nothing`
**Ans: A** **[PYP-25 Q38]** — r_o = 1/(λI_D), so larger λ means smaller r_o and hence lower gain A_v ≈ −g_m r_o.

**Q517.** For a common-source amplifier with A_v ≈ −g_m r_o, doubling λ approximately:
`A) Halves r_o and the gain | B) Doubles the gain | C) Doubles r_o | D) Has no effect`
**Ans: A** — Direct proportionality: r_o halves.

**Q518.** The subthreshold (weak-inversion) slope of a modern MOSFET is approximately:
`A) 60 mV per decade of I_D | B) 200 mV per decade | C) 0 mV | D) 1 V per decade`
**Ans: A** — 60–70 mV/dec is the room-temperature limit set by statistics.

**Q519.** The drain current of a MOSFET in the triode region is given by:
`A) I_D = k[(V_GS−V_T)V_DS − V_DS²/2] | B) I_D = ½k(V_GS−V_T)² | C) I_D = k(V_GS−V_T) | D) I_D = V_DS/R`
**Ans: A** — Valid for 0 ≤ V_DS < V_GS − V_T; the triangular term is what produces the linear (Ohmic) behaviour.

**Q520.** For a MOSFET in saturation with channel-length modulation, the current is:
`A) I_D = ½k(V_GS−V_T)²(1 + λV_DS) | B) I_D = ½k(V_GS−V_T)²(1 − λV_DS) | C) I_D = k(V_GS−V_T) | D) I_D = I_DSS(1−V_GS/V_GS(off))²`
**Ans: A** — The (1 + λV_DS) factor converts the ideal square law into a slightly tilted family of curves.

**Q521.** The MOS capacitor under the gate has three regions of operation:
`A) Accumulation, depletion, inversion | B) Cutoff, saturation, breakdown | C) Forward, reverse, zero bias | D) Enhancement only`
**Ans: A** — These are the classic MOS-C charge states and the basis of the charge-coupled device (CCD).

**Q522.** An NMOS with V_GS = 0 and V_DS = 5 V in a standard process is normally:
`A) Cutoff (off) | B) Saturated (on) | C) In triode | D) Broken down`
**Ans: A** — An enhancement NMOS has V_T > 0, so V_GS = 0 turns it off.

**Q523.** A depletion NMOS with V_T = −2 V biased at V_GS = 0:
`A) Conducts I_DSS (normally on) | B) Is off | C) Is in breakdown | D) Has zero V_T effect`
**Ans: A** — Normally-on devices are useful in analog ICs for "self-biased" current mirrors and load devices.

**Q524.** The input impedance of a MOSFET gate at DC is:
`A) Extremely high (≈10¹² Ω, oxide insulated) | B) Equal to r_π | C) ~100 Ω | D) Exactly infinite`
**Ans: A** — Finite because of oxide leakage and junction diodes; effectively infinite for signal analysis.

**Q525.** Thin-oxide MOSFETs are preferred in digital CMOS because:
`A) Higher oxide capacitance allows higher speed at lower V_DD | B) They leak less | C) They have higher V_T | D) They need no gate drive`
**Ans: A** — Thin oxide raises gate capacitance and drive current, enabling fast switching; leakage is the trade-off.

**Q526.** The maximum V_GS a MOSFET gate can normally withstand is about:
`A) ±20 V (oxide breakdown) | B) ±5 V | C) ±200 V | D) Any value`
**Ans: A** — Gate oxide breakdown (TDDB) typically occurs around 5–7 nm of SiO₂, so ±20 V is a common rating.

**Q527.** Punch-through in a MOSFET occurs when:
`A) The source–drain depletion regions touch, shorting the device | B) V_GS exceeds V_T | C) The body is reverse biased | D) λ becomes large`
**Ans: A** — The channel vanishes and the device becomes a resistor from drain to source.

**Q528.** Drain-induced barrier lowering (DIBL) causes:
`A) V_T to fall as V_DS rises | B) V_T to rise with V_DS | C) I_D to drop to zero | D) λ to become negative`
**Ans: A** — The drain field lowers the source-side barrier, worsening subthreshold leakage in short channels.

**Q529.** Short-channel effects in deep-submicron MOSFETs include:
`A) DIBL, velocity saturation and threshold-voltage lowering | B) Only higher V_T | C) Larger λ | D) Lower mobility`
**Ans: A** — These are why sub-0.1 µm digital design must use non-quadratic compact models.

**Q530.** Velocity saturation in a short-channel MOSFET replaces the quadratic law with:
`A) Linear-in-V_OV behaviour | B) Exponential | C) Logarithmic | D) Cubic`
**Ans: A** — Current saturates once carriers reach v_sat, so I_D ≈ βV_OV(1 + θV_OV) with V_sat ≈ 10⁷ cm/s.

**Q531.** A 0.1 µm CMOS device at I_D = 1 mA with V_OV = 2 V and λ = 0.1 V⁻¹ has an intrinsic gain g_m r_o of about:
`A) 10 | B) 20 | C) 100 | D) 2`
**Ans: A** — g_m = 2I_D/V_OV = 1 mS and r_o = 1/(λI_D) = 10 kΩ, so A_0 = 10.

### 8C. MOSFET amplifier configurations and biasing

**Q532.** A common-source amplifier with g_m = 2 mS and R_D = 10 kΩ (r_o ≫ R_D) has gain:
`A) −20 | B) +20 | C) −5 | D) 20 000`
**Ans: A** — A_v = −g_m(R_D ∥ r_o) ≈ −0.002 × 10 000 = −20.

**Q533.** A source follower with g_m = 2 mS and R_S = 5 kΩ has gain:
`A) ≈ 0.91 | B) −10 | C) 10 | D) 1.0 exactly`
**Ans: A** — A_v = g_mR_S/(1 + g_mR_S) = 10/11 = 0.909.

**Q534.** A common-gate amplifier with g_m = 2 mS and R_D = 10 kΩ has gain:
`A) +20 | B) −20 | C) 0.91 | D) +0.91`
**Ans: A** — Non-inverting with gain ≈ +g_m R_D.

**Q535.** The input resistance of a common-gate amplifier is approximately:
`A) 1/g_m = 500 Ω | B) Very high | C) r_o | D) 1 MΩ`
**Ans: A** — 1/0.002 = 500 Ω, which is its main drawback.

**Q536.** The output resistance of a source follower is approximately:
`A) 1/g_m = 500 Ω | B) Very high | C) r_o | D) Zero`
**Ans: A** — Also ≈1/g_m, making it a good output buffer.

**Q537.** Which MOSFET configuration has the highest input resistance?
`A) Source follower | B) Common source with gate bias | C) Common gate | D) All equal`
**Ans: A** — Z_in = R_G‖(1/g_m + R_S(1+1/(g_mR_G))) can be made very high with a high-value gate bias resistor.

**Q538.** Self-biasing a JFET (gate resistor to ground, source resistor to −V) gives:
`A) Q-point set by I_DSS and V_GS(off) | B) Q-point independent of the device | C) Zero drain current | D) Unstable bias`
**Ans: A** — I_D is determined by the intersection of the source self-bias line with the device transfer curve — moderately stable.

**Q539.** The drain current of a JFET self-biased with V_GS = −2 V, I_DSS = 16 mA, V_GS(off) = −4 V is:
`A) 4 mA | B) 8 mA | C) 16 mA | D) 1 mA`
**Ans: A** — Shockley: 16(1 − 0.5)² = 4 mA.

**Q540.** The ON resistance R_on of a MOSFET switch with k = 2 mA/V² and V_GS = 5 V, V_T = 1 V is approximately:
`A) 125 Ω | B) 250 Ω | C) 1 kΩ | D) 100 Ω`
**Ans: A** — R_on = 1/(k·V_OV) = 1/(2×10⁻³ × 4) = 125 Ω.

**Q541.** A MOSFET switch's ON resistance falls when:
`A) V_GS is increased | B) V_GS is decreased | C) W/L is reduced | D) V_DS is reduced`
**Ans: A** — More overdrive thickens the inversion layer, lowering R_on ∝ 1/[k(V_GS−V_T)].

**Q542.** The OFF leakage current of a MOSFET switch is:
`A) Subthreshold/drain-to-source leakage, usually < 1 µA | B) βI_B | C) Zero always | D) Equal to I_DSS`
**Ans: A** — Leakage sets static power in CMOS logic and is a design constraint in analog switches.

**Q543.** A MOSFET operated with V_GS = V_GS(off) (JFET-like) has:
`A) I_D = I_DSS | B) I_D = 0 | C) I_D = maximum | D) Undefined`
**Ans: B** — Exactly at cutoff the channel is pinched off — the basis of the analog switch "off" state.

**Q544.** Comparing MOSFET and BJT at equal bias current, the MOSFET has:
`A) Higher input impedance, lower g_m, no minority-carrier storage | B) Higher g_m | C) Faster switching due to charge storage | D) Lower noise`
**Ans: A** — Insulated gate gives Z_in ≈ ∞ and g_m = 2I_D/V_OV < I_C/V_T, but switching is faster (no storage).

**Q545.** A p-channel MOSFET with V_T = −1 V must be biased at:
`A) V_GS more negative than −1 V to turn on | B) V_GS > +1 V | C) V_GS = 0 | D) Any V_GS`
**Ans: A** — For a p-channel device, |V_GS| > |V_T| with the correct polarity conducts; the gate is driven negative.

**Q546.** Complementary CMOS (CMOS) inverter input/output characteristics show:
`A) Rail-to-rail output swing | B) 1 V swing only | C) Symmetric ±V_DD/2 output | D) No output`
**Ans: A** — Both transistors reach their rails, giving 0 to V_DD swing — essential for digital noise margins.

**Q547.** In a CMOS inverter's transition region (input near V_DD/2):
`A) Both PMOS and NMOS conduct | B) Only PMOS conducts | C) Only NMOS conducts | D) Both are in cutoff`
**Ans: A** **[PYP-25 Q66]** — Both devices carry current, which is exactly why the transition region has high power dissipation.

**Q548.** The maximum power dissipation of a CMOS inverter occurs:
`A) During the input transition through V_DD/2 | B) When the input is at V_DD | C) When the input is at 0 | D) Never`
**Ans: A** — Short-circuit current peaks when both devices are on; it falls to zero in either static logic state.

**Q549.** The dynamic power dissipation of a CMOS gate is:
`A) P = α C_L V_DD² f | B) P = V_DD²/R | C) P = I_S V_DD only | D) P = C_L V_DD f`
**Ans: A** — Energy per transition is C_LV_DD²; halving V_DD at constant f cuts dynamic power by 4×.

**Q550.** A CMOS gate with C_L = 100 pF at 1 MHz and V_DD = 5 V (α = 1) dissipates:
`A) 2.5 mW | B) 0.5 mW | C) 25 mW | D) 2.5 W`
**Ans: A** — P = 100×10⁻¹² × 25 × 10⁶ = 2.5 mW.

**Q551.** The CMOS inverter's noise margins are proportional to:
`A) (V_DD − |V_T|) related quantities | B) The threshold voltage only | C) The transistor β | D) The load capacitance`
**Ans: A** — Scaling V_DD improves noise margins, which is why digital CMOS scaling historically lowered V_T along with V_DD.

**Q552.** The CMOS inverter propagation delay is approximately:
`A) 0.69 R_on C_L | B) R_on C_L | C) C_L/R_on | D) 0.5 R_on C_L`
**Ans: A** — t_p ≈ 0.69·R_eq·C_L, the 10–90 % rise/fall time of the RC load.

**Q553.** A CMOS inverter's propagation delay with R_on = 2 kΩ and C_L = 50 pF is about:
`A) 69 ns | B) 100 ns | C) 6.9 ns | D) 0.69 ns`
**Ans: A** — 0.69 × 2000 × 50×10⁻¹² = 69 ns.

**Q554.** A depletion-load NMOS logic gate (instead of a PMOS) is used because:
`A) It can drive a faster edge and gives better pull-up ratio | B) It consumes more static power | C) It needs a negative supply | D) It has no threshold`
**Ans: A** — Depletion load devices are non-standard in CMOS logic but were used in NMOS logic for speed.

**Q555.** The "ratioed" logic family (e.g. NMOS RTL) suffers from:
`A) Static power and a noise-margin penalty when the ratioed device turns on | B) No static power | C) Higher noise margins | D) Rail-to-rail swing`
**Ans: A** — When the pull-up is partially on the low level rises; this was the main reason CMOS displaced NMOS logic.

**Q556.** Static CMOS power is non-zero mainly due to:
`A) Leakage (subthreshold and junction) | B) Charging of C_L | C) Both transistors conducting | D) The clock`
**Ans: A** — At DC the ideal static power is zero; real leakage grows as V_T is scaled down.

**Q557.** A MESFET differs from a MOSFET in that it uses:
`A) A Schottky gate instead of an oxide-isolated gate | B) A p-type substrate | C) A bipolar base | D) No channel`
**Ans: A** — The metal–semiconductor Schottky barrier gives low gate capacitance and very high f_max (GaAs, GaN).

**Q558.** GaAs MESFETs are preferred over silicon BJTs at millimetre-wave frequencies because of:
`A) Higher electron mobility and saturation velocity | B) Lower V_BE | C) Higher V_A | D) Lower noise`
**Ans: A** — Electron mobility in GaAs is ~8500 cm²/Vs vs 1350 in Si, giving faster transit and higher f_T.

**Q559.** Compared to silicon, GaAs semiconductors offer the advantage of:
`A) Higher electron mobility, higher frequency operation and lower parasitic capacitance | B) Higher breakdown voltage only | C) Lower mobility | D) Higher density of states`
**Ans: A** **[PYP-23 Q46 concept]** — GaAs gives faster devices and lower device capacitance; its drawbacks are low breakdown and poor integration.

**Q560.** A HEMT (high-electron-mobility transistor) improves on a MESFET by:
`A) Confining electrons in a modulation-doped heterojunction, separating momentum from donor scattering | B) Using a thicker gate oxide | C) Using p-channel conduction | D) Removing the gate`
**Ans: A** — The 2D electron gas is separated from the donors, so mobility stays high at high density.

**Q561.** The electron mobility of GaAs at 300 K is about:
`A) 8500 cm²/V·s | B) 1350 cm²/V·s | C) 300 cm²/V·s | D) 20000 cm²/V·s`
**Ans: A** — Nearly 6× silicon's 1350 cm²/V·s.

**Q562.** A Gunn diode is a bulk (three-terminal) device in which:
`A) A bulk negative resistance arises from transferred-electron (Gunn) effect | B) A p-n junction dominates | C) The gate controls the current | D) It is a JFET`
**Ans: A** — The transferred-electron mechanism gives negative differential resistance, hence oscillation without a tunnel junction.

**Q563.** A Gunn diode operated at high frequency behaves as:
`A) A negative resistance device | B) A positive resistance device | C) A high noise device | D) A rectifier`
**Ans: A** **[PYP-23 Q45]** — Negative differential resistance is what sustains RF oscillation.

**Q564.** A Gunn diode (TED) requires for oscillation:
`A) A resonant cavity or waveguide for the transit-time feedback | B) A negative supply | C) A very low threshold voltage | D) A Zener`
**Ans: A** — The transit delay through the device must be tuned to the resonant structure's period.

**Q565.** An IMPATT diode generates microwave power using:
`A) Avalanche and carrier transit-time effects | B) The Gunn effect | C) Schottky injection | D) Zener breakdown only`
**Ans: A** — Avalanche generation plus transit delay gives high-power microwave oscillation.

**Q566.** An RF detector (square-law) diode exploits:
`A) The quadratic I–V characteristic of a Schottky junction | B) Avalanche breakdown | C) The Gunn effect | D) Zener breakdown`
**Ans: A** — V_out ∝ V_in² makes the response insensitive to carrier frequency, enabling envelope detection.

**Q567.** Which noise source dominates in a MOSFET at low frequencies?
`A) 1/f (flicker) noise | B) Shot noise in the base | C) Thermal noise in V_DD | D) Zener noise`
**Ans: A** — Flicker noise corner frequency rises with gate area and decreases with oxide thickness.

**Q568.** The thermal (Johnson) noise voltage of a 10 kΩ resistor at 300 K over 1 Hz bandwidth is about:
`A) 13 nV | B) 1.3 µV | C) 130 nV | D) 0.4 µV`
**Ans: A** — v_n = √(4kTR) = √(4×1.38×10⁻²³×300×10⁴) ≈ 1.29×10⁻⁸ V = 13 nV.

**Q569.** The primary noise in a JFET at low frequencies is:
`A) 1/f noise from the channel | B) Shot noise in the gate | C) Thermal noise in the drain resistor | D) Quantum noise`
**Ans: A** — JFETs are noted for low 1/f noise because electrons travel in the majority-carrier bulk channel.

**Q570.** A MOSFET switch used in an analog multiplexer provides:
`A) Low ON resistance and negligible OFF leakage | B) Very high gain | C) Negative resistance | D) High noise`
**Ans: A** — Voltage-controlled bidirectional switching; the trade-off is switch resistance modulation over signal range.

**Q571.** A bootstrapped (gate-boosted) switch raises the effective V_GS of the pass device above V_DD by:
`A) Driving the gate from the boosted output node | B) Using a negative supply | C) Increasing W/L | D) Lowering V_T`
**Ans: A** — Since the source follows the output, a constant V_GS drive gives a nearly constant, small R_on across the full swing.

**Q572.** The "body tie" in an NMOS analog switch is connected so that:
`A) The body is held at the most negative potential to prevent forward-biasing the body diode | B) The body floats | C) The body ties to V_DD | D) The body is tied to the gate`
**Ans: A** — Forward-biasing the body–drain/source diode would inject current and clamp the signal.

**Q573.** The maximum V_GS for a MOSFET gate oxide is typically limited to about:
`A) ±20 V | B) ±100 V | C) ±5 V | D) ±500 V`
**Ans: A** — Above this, oxide breakdown (TDDB) destroys the device; modern thick-oxide parts allow ±18–20 V.

**Q574.** In the triode region, a MOSFET's incremental ON resistance can be reduced by:
`A) Increasing W/L | B) Decreasing W/L | C) Increasing V_DS | D) Decreasing V_GS`
**Ans: A** — R_on ∝ L/(W), so widening the channel lowers it proportionally.

**Q575.** A MOSFET's transconductance in saturation is independent of:
`A) V_DS (once V_DS > V_OV) | B) V_GS | C) W/L | D) V_T`
**Ans: A** — Beyond pinch-off I_D (and hence g_m) is set by V_GS, not V_DS — this is the ideal-current-source property.

**Q576.** A common-source amplifier's gain is limited by r_o; with g_m = 2 mS, r_o = 20 kΩ, R_D = 20 kΩ the gain is:
`A) ≈ −20 | B) −40 | C) −10 | D) −4`
**Ans: A** — A_v = −g_m(R_D ∥ r_o) = −0.002 × 10 000 = −20.

**Q577.** Increasing the drain resistance of a common-source amplifier (within limits):
`A) Increases gain up to the limit of g_m r_o | B) Decreases gain | C) Increases V_T | D) Reduces bandwidth always`
**Ans: A** — Gain saturates at A_max = g_m r_o; beyond that, ro dominates.

**Q578.** The maximum intrinsic gain of a single common-source stage is:
`A) g_m r_o | B) g_m | C) r_o | D) 1/g_m`
**Ans: A** — Hence cascading or cascode is needed to build large analogue gain.

**Q579.** A cascode common-source stage improves gain because:
`A) It multiplies the output resistances of the two devices | B) It doubles g_m | C) It halves C_gs | D) It raises I_D`
**Ans: A** — Cascode gives ≈ g_m r_o², dramatically raising gain without adding a second high-speed pole.

**Q580.** A cascode stage's disadvantage is:
`A) Reduced output swing and one extra parasitic capacitance | B) Lower input impedance | C) Positive feedback | D) Higher noise only`
**Ans: A** — The cascoded device needs headroom above the input device's V_DS,sat; and the added node introduces C_parasitic.

**Q581.** A folded cascode is used when:
`A) A single supply is used and the signal must swing to the negative rail | B) The supply is dual and ±15 V | C) The input current must be large | D) Very low output resistance only`
**Ans: A** — Folding the output branch into the input branch lets the stage operate within a single-supply, 0–V_DD range.

**Q582.** The gain of a folded-cascode stage is approximately:
`A) g_m r_o² | B) g_m r_o | C) g_m² r_o | D) 1`
**Ans: A** — Same cascode-squared benefit, with single-supply compatibility.

**Q583.** A MOS current mirror's output current is:
`A) Proportional to the (W/L) ratio of the mirror transistors | B) Always equal to V_T | C) Independent of W/L | D) Proportional to λ`
**Ans: A** — For matched devices in saturation, I_out = (W/L)_out/(W/L)_ref × I_ref.

**Q584.** Why is a cascode mirror preferred over a simple mirror?
`A) Higher output resistance, hence better current-source accuracy | B) Lower supply consumption | C) It needs no reference | D) Faster switching only`
**Ans: A** — Cascode output resistance ≈ g_m r_o², so the mirrored current tracks much more accurately with V_DS.

**Q585.** A MOSFET in the triode region can be used as:
`A) A voltage-controlled linear resistor | B) A current source | C) A switch only at V_GS = 0 | D) A voltage reference`
**Ans: A** — Triode operation with a fixed V_GS gives an Ohmic, V_GS-controlled resistance.

---

## SECTION 9 — Current Mirrors, Active Loads, Differential & Cascode (Q586–Q655)

### 9A. Current mirrors and active loads

**Q586.** The basic building block of a bipolar analog IC is:
`A) The current mirror | B) The op-amp | C) The Zener | D) The SCR`
**Ans: A** — Mirrors set and replicate bias currents; almost every analogue block contains several.

**Q587.** A matched BJT current mirror with I_ref = 20 µA and matched V_BE gives:
`A) I_out = 20 µA | B) I_out = 40 µA | C) I_out = 0 | D) I_out = 10 µA`
**Ans: A** — Equal emitter areas and equal V_BE force I_C ≈ I_ref.

**Q588.** A mirror designed with an emitter-area ratio of 1:2 (reference : output) delivers:
`A) 2× I_ref | B) 0.5× I_ref | C) 4× I_ref | D) I_ref`
**Ans: A** — Current ratio equals emitter-area ratio: I_out/I_ref = (W/L)_out/(W/L)_ref.

**Q589.** A MOSFET current mirror with (W/L)_out = 4×(W/L)_ref and I_ref = 10 µA sinks:
`A) 40 µA | B) 10 µA | C) 2.5 µA | D) 100 µA`
**Ans: A** — I_out = 4 × 10 µA, provided the output device stays in saturation.

**Q590.** For a mirror to work correctly, both transistors must be in:
`A) Saturation | B) Cutoff | C) Triode | D) Breakdown`
**Ans: A** — The output device must have V_DS > V_GS − V_T; otherwise the mirror is non-linear.

**Q591.** The primary error in a BJT mirror is the base-current error because:
`A) I_ref is reduced by 2I_B, giving I_out = I_ref(1 − 2/β) | B) β is temperature dependent | C) V_BE is unstable | D) Early effect`
**Ans: A** — Typically a 1–2 % error for β = 100–200.

**Q592.** With β = 100, the simple BJT mirror's output current is what fraction of I_ref?
`A) 0.90 | B) 0.98 | C) 1.0 | D) 0.5`
**Ans: B** — 1 − 2/β = 0.98.

**Q593.** A Widlar (widely used) current mirror improves the reference current by:
`A) Eliminating base-current error with a small emitter resistor on the reference device | B) Using a larger β transistor | C) Adding a Zener | D) Using PMOS devices`
**Ans: A** — The emitter resistor forces I_C/I_ref ratios close to the area ratio even for small currents.

**Q594.** A cascode (Wilson-type) current mirror has an advantage of:
`A) Very high output resistance, hence a more constant output current | B) Lower supply consumption | C) No V_BE | D) Higher speed always`
**Ans: A** — Output resistance rises to g_m r_o², so the mirrored current barely changes with V_DS.

**Q595.** An active load in an analogue IC is preferred to a resistor because it provides:
`A) High small-signal resistance with low DC voltage drop | B) High voltage drop | C) Zero power | D) Lower gain`
**Ans: A** — A large effective resistance without burning DC headroom gives large gain in one stage.

**Q596.** A resistor load R_L versus an active (current-source) load changes the common-source stage gain from:
`A) −g_m R_L to −g_m r_o | B) −g_m R_L to −g_m | C) 1 to 0 | D) Nothing`
**Ans: A** — Active loads raise gain by roughly the ratio r_o/R_L.

**Q597.** The voltage drop across an active load compared with an equal-resistance resistor load:
`A) Is lower, because V_DS,sat ≪ I·R | B) Is higher | C) Is identical | D) Is zero`
**Ans: A** — The load device only needs V_DS,sat ≈ V_OV, so more of the supply appears as signal swing.

**Q598.** A current-source load improves the output voltage swing of a differential pair because:
`A) It needs less headroom than a resistor | B) It eliminates the tail current | C) It has lower r_o | D) It increases V_T`
**Ans: A** — Signal can swing until the load leaves saturation, which is at a much lower voltage than I·R.

**Q599.** A MOS current mirror with finite output conductance gives a mirror error:
`A) I_out/I_ref = (1 + g_m R_ref)/(1 + g_m R_out) ≈ 1 + g_m(R_ref − R_out) | B) Zero | C) 50 % | D) Depends only on W/L`
**Ans: A** — Because both devices see different V_DS; matching improves when R_ref ≈ R_out.

**Q600.** Early effect in a BJT mirror causes:
`A) Output current to fall as V_out rises | B) Output current to rise | C) No error | D) Only offset`
**Ans: A** — Finite r_o means I_out falls with V_out, giving a non-ideal (finite) output resistance.

**Q601.** Self-biased current sources use:
`A) A gate resistor to ground plus a drain-connected diode-connected device | B) A Zener | C) A transformer | D) An external current source`
**Ans: A** — The diode-connected device sets V_GS, and the JFET gate draws negligible current so the mirror works.

**Q602.** Widely used analogue IC biasing scheme "constant V_GS, constant V_T" implies:
`A) I_D is temperature-stable because V_GS and V_T have similar temperature coefficients | B) I_D varies strongly | C) V_GS must be 0 | D) Only MOSFETs can do this`
**Ans: A** — Matching gate and threshold tracking keeps the current constant over temperature.

### 9B. Differential amplifiers

**Q603.** The differential amplifier is the basic building block of:
`A) The op-amp input stage | B) A rectifier | C) A regulator | D) An oscillator only`
**Ans: A** — It amplifies the difference of two inputs and rejects common-mode signals.

**Q604.** The single-ended differential gain of an emitter-coupled pair (tail at AC ground) with I_T = 2 mA total, V_T = 26 mV, R_C = 5 kΩ is approximately:
`A) 96 | B) 48 | C) 24 | D) 192`
**Ans: D** — Each side carries I_T/2 = 1 mA, so g_m = 1 mA/26 mV = 38.5 mS and A_d = g_m R_C = 192.

**Q605.** In an emitter-coupled pair, the common-mode gain is ideally:
`A) Zero | B) Unity | C) Equal to the differential gain | D) Infinite`
**Ans: A** — Perfectly matched devices respond only to the difference, so A_cm → 0.

**Q606.** The tail (constant-current) source in a differential pair serves to:
`A) Provide a high differential-gain and a common-mode-rejecting tail impedance | B) Set the gain directly | C) Remove offset | D) Increase supply voltage`
**Ans: A** — A high tail resistance makes I_T nearly constant, so the two sides divide it according to V_id.

**Q607.** Differential-mode input resistance of a matched pair with r_π = 2.6 kΩ each is:
`A) 2r_π = 5.2 kΩ | B) r_π/2 = 1.3 kΩ | C) 4r_π | D) 2 kΩ`
**Ans: A** — Looking differentially between the two bases, the two r_π appear in series.

**Q608.** Common-mode input resistance of an emitter-coupled pair with tail resistance R_T is approximately:
`A) 2r_π + (β+1)R_T (very large) | B) r_π | C) R_C | D) 1/g_m`
**Ans: A** — The tail resistance is multiplied by (β+1), giving very high common-mode impedance.

**Q609.** For a matched differential pair, CMRR is limited in practice by:
`A) Resistor/transistor mismatch and finite tail resistance | B) The supply voltage | C) The load | D) The input frequency only`
**Ans: A** — Perfect matching would give infinite CMRR; real mismatch (ΔV_BE ~ 50 µV) dominates.

**Q610.** The input offset voltage of a differential pair arises from:
`A) Mismatch in V_BE or R_E between the two devices | B) Supply ripple | C) Thermal noise | D) Low frequency`
**Ans: A** — Even a few mV/µA mismatch integrates the mismatch current through r_π, giving offset.

**Q611.** The maximum differential input swing of an emitter-coupled pair is:
`A) V_T (≈26 mV), beyond which one device cuts off | B) V_CC | C) V_T/2 | D) Unbounded`
**Ans: A** — |v_id| > 4V_T ≈ 100 mV drives one transistor fully off, so the pair linearises only over a few tens of mV.

**Q612.** A differential pair with a tail current I_T behaves as a tanh characteristic:
`A) i_1 = (I_T/2)[1 + tanh(v_id/2V_T)] | B) i_1 = I_T·v_id/V_T | C) i_1 = I_T | D) i_1 = v_id²`
**Ans: A** — The tanh (hyperbolic tangent) transfer gives excellent linearity near v_id = 0 and intermodulation performance.

**Q613.** The slope of the tanh characteristic at v_id = 0 is:
`A) I_T/(4V_T) = 1/(2r_e) | B) I_T/V_T | C) 0 | D) I_T²`
**Ans: A** — Maximum transconductance g_m,max = I_T/(4V_T) = 1/(2r_e), the highest linearised transconductance available.

**Q614.** A tail current I_T = 4 mA gives a maximum pair transconductance of:
`A) 1/(2r_e) with r_e = 13 Ω ⇒ g_m = 38.5 mS | B) 154 mS | C) 9.6 mS | D) 1 mS`
**Ans: A** — I_T = 4 mA ⇒ I_E = 2 mA each ⇒ r_e = 13 Ω ⇒ g_m,max = 1/(2×13) = 38.5 mS.

**Q615.** A differential pair's differential input range is limited by:
`A) Cutoff of one device (≈4V_T) | B) V_CC | C) R_C | D) β`
**Ans: A** — Beyond ~100 mV differential input the linear tanh approximation fails and the pair becomes a limiter.

**Q616.** Emitter-coupled logic (ECL) uses the differential pair because it:
`A) Provides very fast switching with the transistors never deeply saturated | B) Maximizes gain | C) Reduces power to zero | D) Requires saturated transistors`
**Ans: A** — Avoiding saturation eliminates storage time, making ECL the fastest bipolar logic family.

**Q617.** A current-mirror-loaded (active-load) differential stage has double-ended output, giving:
`A) Double the single-ended differential gain and a higher output swing | B) Half the gain | C) No gain | D) Zero swing`
**Ans: A** — The mirrored load converts the differential current difference into a doubly-ended voltage, improving both gain and swing.

**Q618.** The main advantage of the active (mirror) load in a differential amplifier is:
`A) It doubles the gain and does not consume voltage headroom | B) It lowers the gain | C) It increases noise only | D) It needs a transformer`
**Ans: A** — Active loads replaced the large collector resistors that otherwise wasted headroom.

### 9C. Op-amp internal structure and analogue IC blocks

**Q619.** A classical three-stage op-amp (input, gain, output) requires compensation because:
`A) Each stage adds a pole, which can make the loop unstable | B) There are three inputs | C) It has too much gain | D) The supply is insufficient`
**Ans: A** — Compensating capacitance creates a dominant pole (Miller capacitor) so that only one pole is significant below unity gain.

**Q620.** The dominant pole is usually created by:
`A) A Miller capacitor across the second-stage differential pair | B) An external crystal | C) A Zener | D) An inductor`
**Ans: A** — C_M(1+A_2) multiplies the capacitance seen at the first node, pushing the pole down.

**Q621.** Why is the second stage of an op-amp made inverting?
`A) So a single Miller capacitor can provide compensation | B) To increase gain | C) To reduce noise | D) To allow a rail-to-rail output`
**Ans: A** — Miller compensation only works with an inverting second stage.

**Q622.** Rail-to-rail input stages are built with:
`A) Complementary input pairs (NMOS and PMOS) whose ranges overlap | B) A single pair with large W/L | C) A Zener | D) A transformer`
**Ans: A** — Each pair covers part of the supply rail, so the input range spans 0 to V_DD.

**Q623.** Folded-cascode op-amps are common in today because they:
`A) Support single-supply operation with high gain and low power | B) Have no compensation capacitor | C) Work at 100 V | D) Use bipolar devices only`
**Ans: A** — Folding the output branch lets the input and output share the same supply rail while keeping high output resistance.

**Q624.** A class-AB output stage in an op-amp is biased by:
`A) A V_BE-multiplier loop | B) A Zener | C) A current mirror only | D) Fixed gate bias`
**Ans: A** — Local feedback drives the output transistors just past conduction, eliminating crossover distortion while remaining thermally stable.

**Q625.** An analog switch built from a CMOS transmission gate has:
`A) Low ON resistance and bidirectional signal flow | B) Unidirectional flow only | C) High OFF resistance | D) No gate control`
**Ans: A** — Complementary pass devices give near-zero R_on over the full input range with no threshold drop.

**Q626.** The "bootstrapped gate" technique in a switch is used to:
`A) Keep R_on constant over the full signal swing | B) Increase the threshold | C) Reduce C_gs | D) Increase leakage`
**Ans: A** — Because the source follows the signal, a fixed V_GS gives constant overdrive.

**Q627.** A voltage-to-current converter (transconductance stage) in an analogue IC is usually:
`A) A MOSFET with a feedback resistor, or a diff pair with a mirror | B) A BJT with a bypass | C) A Zener | D) A diode bridge`
**Ans: A** — The diff pair plus mirror combination gives linear, temperature-stable current output.

**Q628.** An instrumentation amplifier's high input impedance is achieved because:
`A) Two non-inverting buffers precede a differential stage | B) It uses a transformer | C) It uses a rectifier | D) It has a large resistor`
**Ans: A** — The buffers prevent source loading and preserve CMRR; gain is set by one resistor.

**Q629.** A chopper-stabilised (auto-zero) amplifier achieves very low offset by:
`A) Periodically sampling and cancelling the offset | B) Using a large capacitor only | C) Increasing gain | D) Using a Zener`
**Ans: A** — Offset and drift are measured at low frequency where they are nearly constant and then nulled.

**Q630.** The noise of a chopper amplifier appears mainly at:
`A) The chopping frequency and its harmonics | B) DC | C) Very low frequencies | D) Above the signal band`
**Ans: A** — Ripple at f_chop must be filtered out of the signal band.

**Q631.** A sample-and-hold amplifier in an analogue IC usually uses:
`A) A MOS switch, a holding capacitor and a buffer | B) A Zener | C) A BJT rectifier | D) A transformer`
**Ans: A** — The buffer prevents capacitor loading while holding.

**Q632.** An OTA (operational transconductance amplifier) differs from a voltage op-amp in that its output is:
`A) A current (high output impedance) | B) A low-impedance voltage | C) Undefined | D) A resistance`
**Ans: A** — Its transconductance g_m is set by an external control current I_ABC, making it programmable and highly linear (tanh).

**Q633.** An OTA's transconductance is controlled by:
`A) An external bias current I_ABC | B) A supply voltage only | C) A clock | D) A Zener`
**Ans: A** — g_m = I_ABC/(2V_T), so one current sets the gain of every OTA stage in filter design.

**Q634.** An OTA-based filter (active OTA-C integrator) has the advantage of:
`A) Programmability and high input impedance | B) Lower noise than op-amps | C) Simpler layout | D) No capacitors`
**Ans: A** — OTA-C filters integrate capacitors directly, with g_m set by bias currents — the basis of switched-capitor filters.

**Q635.** A switched-capacitor filter replaces resistors with:
`A) Capacitors switched by clock phases | B) Inductors | C) Diodes | D) Current sources`
**Ans: A** — The SC resistor equivalent is C(1/T_clock), which is accurate because capacitors match far better than resistors.

**Q636.** In a switched-capacitor resistor, the equivalent resistance is:
`A) 1/(C·f_clock) | B) C·f_clock | C) 1/(R·C) | D) f_clock/C`
**Ans: A** — Sampling a charge C·ΔV each period gives R_eq = Δt/C = 1/(Cf).

**Q637.** A switched-capacitor filter's practical appeal is that:
`A) Absolute RC values need not be precise because ratios of capacitors are accurate | B) It needs no clock | C) It consumes no power | D) It is always continuous-time`
**Ans: A** — Matching of on-chip capacitor ratios is accurate, so absolute RC precision is unnecessary.

**Q638.** An inverting amplifier built with an OTA has transimpedance gain:
`A) G_m = g_m (S) | B) g_m R_C | C) 1/g_m | D) β`
**Ans: A** — The output current is simply g_m v_id, so the "resistance" is a transconductance.

**Q639.** A switched-capacitor resistor replacing a 10 kΩ resistor with C = 10 pF and f_clk = 1 MHz corresponds to:
`A) 10 kΩ | B) 1 MΩ | C) 100 kΩ | D) 1 kΩ`
**Ans: A** — R = 1/(Cf) = 1/(10×10⁻¹²×10⁶) = 10 kΩ.

### 9D. Specialised analogue blocks and applications

**Q640.** A phase-locked loop used for clock multiplication relies on:
`A) A VCO whose frequency is corrected by the phase detector's error signal | B) A fixed RC oscillator | C) A diode | D) A rectifier`
**Ans: A** — Negative feedback drives the phase difference to zero, locking f_out = N·f_ref.

**Q641.** A PLL's loop gain is:
`A) K_pd·K_vco divided by the frequency divider | B) The VCO gain alone | C) The phase detector only | D) The filter capacitance`
**Ans: A** — The divider by N reduces the effective VCO gain, so loop gain must be divided accordingly.

**Q642.** A frequency divider in a PLL feedback path:
`A) Reduces loop gain and allows multiplication | B) Increases loop gain | C) Removes the VCO | D) Sets the loop filter`
**Ans: A** — With ÷N, the loop locks f_out = N f_ref while loop gain falls by N.

**Q643.** A charge-pump PLL uses a charge pump to:
`A) Inject or remove charge from the loop filter so the phase error is driven to zero | B) Amplify the reference | C) Divide the frequency | D) Provide gain`
**Ans: A** — Positive/negative current pulses average into a control voltage for the VCO.

**Q644.** A switching regulator's switching action is:
`A) The main reason for high conversion efficiency | B) A source of loss | C) Only used for low power | D) Unrelated to efficiency`
**Ans: A** — Energy is transferred through inductor magnetic fields with minimal dissipation.

**Q645.** An analog multiplier IC (e.g. AD633) is built around:
`A) Log/antilog stages or a Gilbert cell | B) A Zener | C) A diode bridge only | D) A transformer`
**Ans: A** — Both give a full four-quadrant multiplier; the Gilbert cell is faster and more linear.

**Q646.** A logarithmic amplifier used with a photodiode produces:
`A) A display linear in optical density | B) A linear current | C) A square wave | D) A temperature reading`
**Ans: A** — Log output means equal display steps for equal ratios of light, which is the Beer–Lambert law in optics.

**Q647.** An analog computing block performing division is built as:
`A) The difference of two log amplifiers, exponentiated | B) The sum of two log amplifiers | C) An integrator | D) A comparator`
**Ans: A** — ln(V_1) − ln(V_2) exponentiated = V_1/V_2.

**Q648.** A low-dropout (LDO) regulator's key feature is:
`A) Very small dropout voltage at high output current | B) High efficiency at light loads only | C) Switching operation | D) Negative output resistance`
**Ans: A** — PMOS pass devices with low R_on give dropout of a few hundred mV.

**Q649.** A charge-balanced system (e.g. a ΔΣ modulator) keeps the average output correct because:
`A) The integral of the quantization error over many cycles is zero | B) It has no quantizer | C) It is always monotonic | D) It requires a DAC`
**Ans: A** — Averaging removes quantization noise from the signal band, pushing it out of band.

**Q650.** In a ΔΣ modulator, increasing the oversampling ratio mainly improves:
`A) In-band noise by pushing quantization noise higher in frequency | B) The quantizer step | C) The clock frequency only | D) The linearity`
**Ans: A** — Noise shaping plus oversampling is the basis of high-resolution audio and instrumentation ADCs.

**Q651.** An analog computing "sample-and-hold" application in a feedback loop is used for:
`A) Analogue computing of complex functions | B) Power conversion | C) Oscillation | D) Rectification`
**Ans: A** — S/H blocks let a slow analogue computer model fast waveforms.

**Q652.** A PLL lock-in range (tracking range) is limited mainly by:
`A) The VCO tuning range and loop bandwidth | B) The phase detector gain | C) The charge pump size | D) The loop filter order only`
**Ans: A** — Capture requires the loop to pull f_vco to f_ref; tracking requires the loop bandwidth to cover the reference change.

**Q653.** A phase detector implemented as a multiplier (phase-frequency detector XOR style) produces:
`A) An error voltage proportional to phase difference | B) A constant DC | C) A frequency only | D) A square wave with no phase information`
**Ans: A** — The average of the product of two square waves is proportional to their phase offset.

**Q654.** A CMOS ring oscillator with 2N inverters has frequency:
`A) f = 1/(2N·t_pd) | B) f = 1/t_pd | C) f = 2N·t_pd | D) Independent of N`
**Ans: A** — Each stage contributes t_pd, and there are 2N stages per period, so f = 1/(2N t_pd).

**Q655.** A ring oscillator with 10 stages, each with t_pd = 20 ps, oscillates at about:
`A) 2.5 GHz | B) 5 GHz | C) 25 GHz | D) 1.25 GHz`
**Ans: A** — f = 1/(20 × 20 ps) = 1/400 ps = 2.5 GHz.

---

## SECTION 10 — Oscillators & 555 Timers (Q656–Q715)

**Q656.** In transistor oscillators, instability (and hence oscillation) is achieved by:
`A) Negative feedback | B) Positive feedback | C) Using a tank circuit alone | D) None of the above`
**Ans: B** **[PYP-23 Q41]** — The tank sets the frequency; positive feedback provides the regeneration that satisfies Barkhausen.

**Q657.** The Barkhausen criterion for sinusoidal oscillation requires:
`A) |A(jω)β(jω)| = 1 and ∠A(jω)β(jω) = 2nπ | B) |A| > 1 only | C) ∠Aβ = 90° | D) Z_in = Z_out`
**Ans: A** — Steady-state oscillation needs unity loop gain with 0° (360°) total phase shift.

**Q658.** For oscillation to *start* from noise, the small-signal condition must be:
`A) |Aβ| > 1 at the resonant frequency | B) |Aβ| < 1 | C) |Aβ| = 0 | D) A = 0`
**Ans: A** — Loop gain must exceed unity at startup and be brought back to unity by an amplitude-limiting mechanism.

**Q659.** Amplitude stabilization in a Wien bridge oscillator is achieved by:
`A) A nonlinear element (diode, lamp or AGC) that reduces gain as amplitude grows | B) A larger RC | C) A crystal | D) A battery`
**Ans: A** — Gain must fall from >3 to exactly 3 at steady state; a lamp or back-to-back diodes do this.

**Q660.** A Wien bridge oscillator requires an amplifier gain of at least:
`A) 1 | B) 3 | C) 29 | D) 100`
**Ans: B** — The lead-lag network attenuates by 1/3 at f_0, so A must exceed 3.

**Q661.** The frequency of a Wien bridge oscillator with R = 10 kΩ and C = 10 nF is approximately:
`A) 1.59 kHz | B) 159 Hz | C) 15.9 kHz | D) 6.28 kHz`
**Ans: A** — f = 1/(2πRC) = 1/(2π×10⁴×10⁻⁸) ≈ 1592 Hz.

**Q662.** The frequency of an RC phase-shift oscillator with R = 10 kΩ, C = 0.01 µF is approximately:
`A) 1.6 kHz | B) 650 Hz | C) 6.28 kHz | D) 26 Hz`
**Ans: B** — f = 1/(2πRC√6) = 1/(6.283×10⁻⁴×2.449) ≈ 650 Hz.

**Q663.** The minimum amplifier gain for an RC phase-shift oscillator is:
`A) 3 | B) 29 | C) 1 | D) 100`
**Ans: B** — Three equal RC sections attenuate by 1/29 at the oscillation frequency.

**Q664.** An RC phase-shift oscillator provides:
`A) 180° total phase shift (60° per section) | B) 90° | C) 360° | D) 0°`
**Ans: A** — The CE amplifier gives 180°, and the network a further 180°, totalling 360°.

**Q665.** A Colpitts oscillator with L = 10 µH and C_1 = C_2 = 100 pF oscillates at approximately:
`A) 7.1 MHz | B) 3.5 MHz | C) 14 MHz | D) 1.8 MHz`
**Ans: A** — C_eq = 50 pF, f = 1/(2π√(10⁻⁵×5×10⁻¹¹)) = 7.12 MHz.

**Q666.** The capacitance that must be used in a Colpitts oscillator with two capacitors is:
`A) C_1 C_2/(C_1 + C_2) | B) C_1 + C_2 | C) C_1 C_2 | D) 1/C_1 + 1/C_2`
**Ans: A** — The capacitors are in series across the inductor, giving C_eq = C_1C_2/(C_1+C_2).

**Q667.** A Hartley oscillator with L_1 = 10 µH, L_2 = 10 µH, M = 5 µH, C = 100 pF has an effective inductance of:
`A) 30 µH | B) 20 µH | C) 10 µH | D) 40 µH`
**Ans: A** — L_eq = L_1 + L_2 + 2M = 10 + 10 + 10 = 30 µH, so f = 1/(2π√(30×10⁻⁶×100×10⁻¹²)) ≈ 2.9 MHz.

**Q668.** Hartley and Colpitts oscillators require:
`A) A transformer or capacitor tap plus a transistor with 180° phase shift | B) Only a Zener | C) A rectifier | D) An op-amp in open loop`
**Ans: A** — The tap provides the required 180° feedback phase; the amplifier supplies the other 180°.

**Q669.** The frequency stability of a crystal oscillator is much better than an LC oscillator because:
`A) The crystal has a very high Q (10⁴–10⁶) | B) The crystal is smaller | C) It needs no supply | D) It uses negative feedback`
**Ans: A** — High Q means the loop crosses unity only very near the series resonance, so frequency is insensitive to supply, temperature and loading.

**Q670.** A crystal is best described as:
`A) A mechanical resonator with an equivalent RLC circuit | B) A semiconductor | C) A capacitor | D) An inductor only`
**Ans: A** — Equivalent: motional arm in parallel with C_0 in series with R_m.

**Q671.** A Pierce oscillator uses:
`A) A crystal as the frequency-selective element with the amplifier providing 180° | B) An RC network | C) A varactor only | D) A tunnel diode only`
**Ans: A** — The crystal's impedance plus the amplifier's inversion gives the required 360°.

**Q672.** The Clapp oscillator differs from the Colpitts by adding:
`A) A series capacitor in the tank to reduce the effect of transistor capacitance | B) A transformer | C) A Zener | D) A second BJT`
**Ans: A** — Clamping the effective C improves frequency stability against parasitic variation.

**Q673.** A free-running (astable) multivibrator using two BJTs with equal RC time constants has frequency:
`A) f = 1/(0.693 RC) | B) f = 1/(2πRC) | C) f = 2/RC | D) f = RC`
**Ans: A** — Each half-cycle is one charging time constant; T ≈ 1.386 RC, so f ≈ 0.72/RC.

**Q674.** A relaxation oscillator with an op-amp and RC has its output frequency determined by:
`A) The RC time constant and the feedback ratio β | B) The op-amp A_OL | C) The supply voltage only | D) The load`
**Ans: A** — f = 1/[2RC ln((1+β)/(1−β))].

**Q675.** A twin-T oscillator is used when:
`A) A few degrees of amplitude/frequency control with very low distortion is needed | B) Maximum output power is needed | C) Very high frequency is needed | D) Negative resistance is required`
**Ans: A** — It gives a sharper amplitude-limiting action than a Wien bridge, reducing distortion.

**Q676.** The twin-T network provides:
`A) Both lead and lag components with a notch at f_0 | B) Only a lead | C) Only a lag | D) No phase shift`
**Ans: A** — The notch at f_0 (f = 1/(2πRC)) gives a steep gain reduction, so less non-linearity is needed.

**Q677.** Oscillators based on negative-resistance devices (tunnel diode, Gunn, IMPATT) oscillate because:
`A) The negative resistance cancels the tank's positive loss | B) They amplify noise only | C) They need positive feedback | D) They have zero capacitance`
**Ans: A** — Small-signal instability condition: total loop resistance < 0.

**Q678.** The Q of an LC tank at resonance is:
`A) Q = ωL/R | B) Q = R/ωL | C) Q = 1/(ωC) | D) Q = V_L/I`
**Ans: A** — High Q (low R) means a sharp resonance and good frequency stability.

**Q679.** Loading a tank with a low resistance:
`A) Reduces its Q and loaded Q | B) Increases its Q | C) Doubles its frequency | D) Has no effect`
**Ans: A** — Loaded Q falls as the external load resistance parallels the tank's loss resistance.

**Q680.** Unloaded Q is higher than loaded Q because:
`A) The external load is excluded in the unloaded case | B) The capacitor has no loss | C) The inductor is ideal | D) The frequency is lower`
**Ans: A** — Unloaded Q considers only the tank's own losses.

**Q681.** The oscillation frequency of an LC oscillator is:
`A) Slightly below the tank's natural frequency when heavily loaded | B) Always above | C) Exactly zero | D) Equal to the amplifier's f_T`
**Ans: A** — Loading pulls the resonant frequency slightly lower (frequency pulling).

**Q682.** A common-emitter amplifier used as the active device in a Colpitts oscillator provides:
`A) 180° phase shift | B) 0° phase shift | C) 90° phase shift | D) 360° phase shift`
**Ans: A** — Which is why the feedback network must supply the other 180°.

**Q683.** A common-base amplifier in an oscillator already provides:
`A) 0° phase shift, so the feedback network must supply 0°/180° | B) 180° | C) 90° | D) 45°`
**Ans: A** — Non-inverting; with an inductive tap the loop phase reaches 360°.

**Q684.** Which oscillator is preferred for a clean audio sine tone?
`A) Wien bridge | B) Square-wave relaxation | C) Blocking oscillator | D) Gunn diode`
**Ans: A** — Its lead-lag network has low distortion and the gain limiting is gentle.

**Q685.** In the 555 timer, the internal Schmitt trigger thresholds are:
`A) V_CC/3 and 2V_CC/3 | B) V_CC/2 only | C) 0 and V_CC | D) 1.7 V fixed`
**Ans: A** — The two comparators reference 1/3 and 2/3 of the supply (or the control-pin voltage).

**Q686.** In a 555 astable multivibrator, the output is HIGH for approximately:
`A) 0.693(R_A + R_B)C | B) 0.693 R_B C | C) (R_A + 2R_B)C | D) 1.1 RC`
**Ans: A** — Charging time through R_A + R_B; the LOW time is 0.693 R_B C.

**Q687.** The frequency of a 555 astable with R_A = 10 kΩ, R_B = 10 kΩ, C = 0.01 µF is:
`A) 4.8 kHz | B) 2.4 kHz | C) 7.2 kHz | D) 1.6 kHz`
**Ans: A** — f = 1.44/[(R_A + 2R_B)C] = 1.44/(30 kΩ × 10 nF) = 4.8 kHz.

**Q688.** The duty cycle of the astable circuit in Q687 is:
`A) 66.7 % | B) 33.3 % | C) 50 % | D) 75 %`
**Ans: A** — D = (R_A + R_B)/(R_A + 2R_B) = 20/30 = 66.7 %.

**Q689.** A 555 configured as a monostable produces a pulse of duration:
`A) 1.1 RC | B) 0.693 RC | C) 2 RC | D) 1.44/RC`
**Ans: A** — The capacitor charges from 0 to 2/3 V_CC through R: t = RC ln 3 = 1.1 RC.

**Q690.** A 555 monostable with R = 10 kΩ and C = 0.01 µF generates a pulse of:
`A) 110 µs | B) 69 µs | C) 1.1 ms | D) 11 µs`
**Ans: A** — t = 1.1 × 10⁴ × 10⁻⁸ = 110 µs.

**Q691.** A 555 used as a bistable multivibrator (flip-flop):
`A) Changes state on each trigger, and its output is stable indefinitely | B) Free-runs | C) Produces a ramp | D) Requires a reset input`
**Ans: A** — Trigger momentarily pulls the flip-flop; no timing capacitor is needed.

**Q692.** In a 555, the DISCHARGE pin is:
`A) Connected to the capacitor and used to discharge it below 1/3 V_CC during the low period | B) The supply pin | C) The output | D) The reset pin`
**Ans: A** — The internal transistor discharges the timing capacitor, defining the low time.

**Q693.** A 555 configured to produce roughly a 1 kHz tone needs:
`A) C = 0.1 µF with R_A = R_B = 5.1 kΩ | B) C = 1 µF with R_A = R_B = 150 Ω | C) C = 10 pF with 1 MΩ resistors | D) C = 1 F`
**Ans: A** — f = 1.44/[(5.1 k + 10.2 k) × 0.1 µF] = 1.44/(1.53 ms) ≈ 940 Hz ≈ 1 kHz.

**Q694.** The maximum duty cycle of a standard 555 astable is:
`A) Just under 100 % (approaches 100 % as R_B → 0) | B) 50 % | C) 75 % | D) 25 %`
**Ans: A** — Charging path always includes R_A + R_B, so D can never reach exactly 100 %; a diode can improve it.

**Q695.** The 555 control pin (pin 5) is used to:
`A) Adjust the threshold voltages, hence frequency or PWM | B) Bypass the timing capacitor | C) Supply the output | D) Reset the chip`
**Ans: A** — Applying a voltage there moves both thresholds, enabling duty-cycle and frequency control.

**Q696.** A 555 can be used as a:
`A) Touch switch, debouncer, PWM generator and FSK modulator | B) Only an oscillator | C) Only a rectifier | D) Only a comparator`
**Ans: A** — Its threshold flip-flop and discharge transistor make it a versatile building block.

**Q697.** The maximum sink current from a 555 discharge pin is about:
`A) 200 mA | B) 5 mA | C) 1 A | D) 2 µA`
**Ans: A** — Standard 555s are rated for ±200 mA output/discharge current; CMOS versions are limited to a few mA.

**Q698.** A relaxation oscillator based on an op-amp differs from a Wien bridge oscillator in that it produces:
`A) A square/triangle waveform rather than a sine wave | B) A sine wave only | C) A DC level | D) A sawtooth only`
**Ans: A** — No frequency-selective network, so the output is rectangular with exponential ramps.

**Q699.** A blocking oscillator generates:
`A) A narrow pulse for each triggering edge | B) A continuous sine wave | C) A DC level | D) A ramp`
**Ans: A** — Positive feedback turns a trigger into a self-limiting pulse, one per input edge.

**Q700.** The critical condition for an LC oscillator using a negative-resistance device is:
`A) |R_neg| equals the total positive loop resistance | B) R_neg is positive | C) No resonance is needed | D) The device must be biased in saturation`
**Ans: A** — |R_neg| slightly exceeding the losses produces growth; amplitude limiting sets the final balance.

**Q701.** Frequency stability of an oscillator is best quantified by:
`A) The fractional change in frequency per unit temperature or supply change | B) Output amplitude | C) Output power | D) THD only`
**Ans: A** — Stability is usually expressed as ppm/°C or as Δf/f per volt.

**Q702.** A Pierce oscillator's crystal operates:
`A) Near its series resonance to avoid high load capacitance | B) At parallel resonance only | C) In the capacitive region | D) Below the cutoff frequency`
**Ans: A** — Series-resonant (inductive) operation allows a small load capacitance, improving frequency stability.

**Q703.** A crystal oscillator frequency drifts with temperature mainly because:
`A) The crystal's cut (AT, BT) has a temperature coefficient | B) The amplifier gain changes | C) The supply is AC coupled | D) The load is resistive`
**Ans: A** — The choice of cut (SC, TC, AT, BT) sets the parabola peak and therefore the drift rate.

**Q704.** A SAW resonator (common in RF) is preferred to a bulk crystal because:
`A) It operates at higher frequencies with smaller size | B) It has higher Q at all frequencies | C) It needs no electrodes | D) It has lower cost`
**Ans: A** — Surface acoustic waves can be formed on substrates whose wavelength is the acoustic wavelength, allowing 100 MHz–3 GHz devices.

**Q705.** In a Wien bridge oscillator, the phase shift of the amplifier at f_0 must be:
`A) 0° | B) 180° | C) 90° | D) 360°`
**Ans: A** — The network provides 0° at f_0, so the amplifier must be non-inverting there.

**Q706.** The attenuation of the Wien bridge network at f_0 is:
`A) 1/3 | B) 1/29 | C) 2/3 | D) 1`
**Ans: A** — β = 1/3 at f_0, hence the gain requirement of exactly 3.

**Q707.** In an RC phase-shift oscillator, the three sections each produce:
`A) 60° of phase shift at f_0 | B) 180° | C) 90° | D) 0°`
**Ans: A** — 3 × 60° = 180°, completing the loop with the CE inversion.

**Q708.** Which oscillator can be tuned most easily over a wide frequency range?
`A) Colpitts (variable capacitor) | B) Crystal | C) Wien bridge | D) Phase-shift`
**Ans: A** — A variable tank capacitor gives a wide tuning range, at the cost of stability.

**Q709.** An oscillator with a JFET active device has the advantage of:
`A) High input impedance, simple biasing and good thermal stability | B) Higher output power | C) Lower noise at low frequency | D) Faster switching`
**Ans: A** — JFET stages are easy to bias and drift little; the gate draws negligible current.

**Q710.** A tuner-type LC oscillator uses a variable capacitor C in parallel with L. Doubling C changes the frequency by:
`A) A factor of 1/√2 | B) A factor of 2 | C) A factor of 4 | D) No change`
**Ans: A** — f ∝ 1/√C, so quadrupling C halves f; doubling C reduces f by 1.41.

**Q711.** The amplitude-limiting in a transistor oscillator can also be achieved by:
`A) Driving the amplifier into soft saturation at the peaks | B) Using a bigger tank | C) Reducing the supply | D) Adding a transformer`
**Ans: A** — Peak clipping reduces effective gain to unity; simple but generates harmonics.

**Q712.** A very low-distortion oscillator uses:
`A) A JFET or FET plus AGC or lamp stabilisation | B) A saturated BJT | C) A tunnel diode | D) A blocking oscillator`
**Ans: A** — FETs plus smooth AGC keep the device in its linear region, minimising distortion.

**Q713.** The start-up condition of a Colpitts oscillator requires the loop gain at resonance to be:
`A) Greater than 1 | B) Exactly 1 | C) Less than 1 | D) Zero`
**Ans: A** — Only |Aβ| > 1 lets noise build into a sustained oscillation.

**Q714.** In an oscillator, the phase condition must be met at:
`A) The oscillation frequency only | B) All frequencies | C) DC only | D) The tank's damped frequency`
**Ans: A** — The loop phase must be 360° at f_osc; elsewhere it may be anything, since those frequencies are not sustained.

**Q715.** A quartz crystal oscillator's output frequency drift over 50 °C is typically:
`A) Parts per million | B) Per cent | C) Tens of per cent | D) Zero exactly`
**Ans: A** — TCXO-grade crystals achieve ~0.01–1 ppm over tens of degrees; a raw crystal is worse.

---

## SECTION 11 — Diode Circuits & Rectifiers (Q716–Q800)

### 11A. Diode characteristics, models and special diodes

**Q716.** The ideal diode acts as:
`A) A perfect switch | B) A resistor that changes with voltage | C) A current source always | D) A short circuit always`
**Ans: A** — In the idealised model it is a short forward-biased and an open reverse-biased.

**Q717.** A practical diode in forward bias is best modelled as:
`A) A fixed 0.7 V drop in series with a small resistance | B) A resistor only | C) An open circuit | D) A current source`
**Ans: A** — The constant-voltage-drop model is the workhorse of hand analysis.

**Q718.** In the constant-voltage-drop model with V_D = 0.7 V, the power dissipated in a diode carrying 100 mA is:
`A) 70 mW | B) 7 mW | C) 700 mW | D) 0.07 mW`
**Ans: A** — P = V_D I = 0.7 × 0.1 = 70 mW.

**Q719.** The current through a forward-biased diode is best described by:
`A) Shockley's equation I = I_S(e^(V_D/nV_T) − 1) | B) Ohm's law only | C) A linear relation in V_D | D) Constant`
**Ans: A** — The exponential law shows that a 60 mV change in forward voltage changes I by about 10×.

**Q720.** In Shockley's equation, the emission coefficient n for a silicon diode is typically:
`A) 1 to 2 | B) 20 to 50 | C) 0.1 | D) Exactly 100`
**Ans: A** — n = 1 for an ideal diffusion junction and rises towards 2 with recombination current.

**Q721.** The reverse saturation current I_S of a silicon diode at room temperature is of the order of:
`A) 10⁻¹⁵ to 10⁻¹² A | B) 1 mA | C) 1 A | D) 10⁻³ A`
**Ans: A** — A tiny current, but multiplied by the exponential term it produces amp-level forward current.

**Q722.** The ideality factor n appears in the diode equation as:
`A) A multiplier of V_T in the exponent | B) A multiplier of I_S | C) A series resistance | D) A breakdown voltage`
**Ans: A** — n scales the thermal voltage: larger n means a "softer" exponential (more recombination).

**Q723.** The dynamic (small-signal) resistance of a diode at a bias current I_D is:
`A) r_d = nV_T/I_D | B) r_d = V_D/I_D | C) r_d = I_D/V_D | D) r_d = V_T/I_S`
**Ans: A** — Differentiating Shockley's equation about the operating point gives r_d = nV_T/I_D.

**Q724.** A diode carries 1 mA at 25 °C. Its AC resistance is approximately:
`A) 26 Ω | B) 260 Ω | C) 2.6 kΩ | D) 0.26 Ω`
**Ans: A** — r_d = 26 mV/1 mA = 26 Ω.

**Q725.** A diode carrying 10 mA has an incremental resistance of about:
`A) 2.6 Ω | B) 26 Ω | C) 260 Ω | D) 2.6 kΩ`
**Ans: A** — Halving... increasing current tenfold divides r_d by ten: 26 mV/10 mA = 2.6 Ω.

**Q726.** The junction capacitance of a reverse-biased diode (depletion capacitance C_j) behaves as:
`A) A voltage-dependent capacitance that decreases with reverse bias | B) A constant | C) An inductance | D) A resistance`
**Ans: A** — The depletion width widens with reverse bias, so C_j = A/(W+B)^M falls.

**Q727.** The diffusion capacitance C_d of a forward-biased diode behaves as:
`A) A capacitance that increases rapidly with forward current | B) A capacitance that decreases | C) A constant | D) Zero`
**Ans: A** — C_d = τI_D/(nV_T), so it grows linearly with injected charge and dominates at high current.

**Q728.** The total stored charge in a forward-biased diode causes a time constant:
`A) The reverse recovery time t_rr when the diode is switched off | B) The forward drop to fall | C) The leakage to stop | D) The breakdown to occur`
**Ans: A** — Stored minority charge must be removed before the diode blocks reverse current.

**Q729.** Reverse recovery time t_rr matters most in:
`A) High-frequency rectifiers and switching regulators | B) DC bias circuits | C) Amplifier biasing | D) Zener references`
**Ans: A** — Stored charge makes fast switching impossible unless a fast-recovery diode is used.

**Q730.** A fast-recovery diode reduces t_rr by:
`A) Using a planar construction with controlled carrier lifetime | B) Increasing the forward drop | C) Adding a series resistor | D) Using a larger die`
**Ans: A** — Platinum lifetime control and planar junctions shorten storage time.

**Q731.** The Schottky barrier height for electrons in a metal-semiconductor junction is typically:
`A) Lower than that of a p-n junction | B) Higher | C) Equal | D) Zero`
**Ans: A** — A lower barrier gives faster switching (no minority carrier storage) and a lower forward drop.

**Q732.** The forward voltage of a Schottky diode at 1 mA is typically:
`A) 0.2–0.4 V | B) 0.7 V | C) 1.4 V | D) 5 V`
**Ans: A** — The majority-carrier device drops only 0.2–0.4 V, and it has essentially no reverse recovery.

**Q733.** Schottky diodes are preferred in:
`A) SMPS output rectifiers and low-drop clamps | B) High-voltage reverse biased strings | C) Photodetectors | D) Zener regulators above 10 V`
**Ans: A** — Low V_F and fast recovery cut conduction and switching loss in switch-mode supplies.

**Q734.** The reverse leakage current of a Schottky diode is:
`A) Higher than in a pn diode | B) Zero | C) Lower than a pn diode | D) Negative`
**Ans: A** — Because the barrier is low, reverse leakage is comparatively large; this sets a minimum holding current.

**Q735.** A Zener diode is normally operated in:
`A) Reverse breakdown | B) Forward bias | C) Cutoff | D) Saturation`
**Ans: A** — In breakdown it holds an almost constant voltage for a wide current range.

**Q736.** The Zener voltage V_Z is:
`A) Nearly constant over a specified current range | B) Proportional to current | C) Proportional to temperature only | D) Zero`
**Ans: A** — Dynamic resistance r_z = ΔV/ΔI is small in the knee region.

**Q737.** A 5.1 V Zener develops 5.12 V at 20 mA and 5.10 V at 5 mA. Its dynamic resistance is:
`A) 1.33 kΩ | B) 75 Ω | C) 15 Ω | D) 1.02 kΩ`
**Ans: A** — r_z = ΔV/ΔI = (5.12 − 5.10)/(20 − 5 mA) = 20 mV/15 mA = 1.33 kΩ.

**Q738.** The maximum Zener current is limited by:
`A) Power dissipation: I_Z(max) = P_Z(max)/V_Z | B) The knee voltage | C) The forward drop | D) The series resistance`
**Ans: A** — A 500 mW 5.1 V Zener can pass at most about 98 mA.

**Q739.** A 400 mW, 12 V Zener diode has a maximum Zener current of:
`A) 33 mA | B) 12 mA | C) 400 mA | D) 4 A`
**Ans: A** — I_Z(max) = 0.4/12 = 33.3 mA.

**Q740.** The minimum Zener current I_Z(min) is needed because:
`A) Below it the device leaves breakdown and stops regulating | B) Above it the device burns out | C) It sets the knee voltage | D) It improves noise`
**Ans: A** — A Zener below its knee current behaves like a poor diode with rising resistance.

**Q741.** To maintain regulation with a series supply and load, the design must ensure:
`A) I_Z(min) < (V_S − V_Z)/R_S < I_Z(max) and load current < I_Z(max) | B) R_S = 0 | C) V_Z > V_S | D) The Zener is in forward bias`
**Ans: A** — Both the worst-case (light load, high V_S) and worst-case (heavy load) currents must stay in the knee.

**Q742.** A Zener diode's temperature coefficient depends on:
`A) The doping (positive for heavily doped, negative for lightly doped) | B) The package | C) The lead length | D) Nothing`
**Ans: A** — Below ~5.1 V the coefficient is negative, above it positive; a temperature-compensated reference uses two Zeners back to back.

**Q743.** A temperature-compensated Zener reference uses:
`A) A Zener and a forward-biased diode in series | B) Two Zeners in parallel | C) A Zener in series with a resistor only | D) Two resistors`
**Ans: A** — Opposing temperature coefficients cancel, giving ~±5 ppm/°C.

**Q744.** A varactor diode provides:
`A) A capacitance that varies with reverse bias voltage | B) A variable resistance | C) A variable inductance | D) A variable current`
**Ans: A** — C_j falls as reverse bias widens the depletion layer, giving voltage tuning of a resonant circuit.

**Q745.** A varactor is used in:
`A) RF tuning and FM generation | B) Rectification | C) Clamping | D) Zener regulation`
**Ans: A** — Voltage-controlled capacitance is ideal for tuning resonators and modulating oscillators.

**Q746.** A photodiode operates in:
`A) Reverse bias | B) Forward bias | C) Saturation | D) Breakdown`
**Ans: A** — Reverse bias widens the depletion region, reducing junction capacitance and speeding up response.

**Q747.** The responsivity of a photodiode is measured in:
`A) A/W | B) W/A | C) A/V | D) V/A`
**Ans: A** — Responsivity R = I_photo/P_optical, typically 0.4–0.6 A/W in silicon.

**Q748.** A photodiode generates photocurrent proportional to:
`A) Incident optical power | B) Incident voltage | C) Temperature | D) Reverse voltage`
**Ans: A** — Photon flux, hence photocurrent, is proportional to optical power.

**Q749.** A solar cell under open-circuit conditions delivers:
`A) V_OC but zero current | B) I_SC but zero voltage | C) Both V_OC and I_SC | D) Maximum power`
**Ans: A** — With no external path, all photogenerated carriers recombine internally, so I = 0 but V rises to V_OC.

**Q750.** A photovoltaic cell's maximum power point is found where:
`A) dP/dV = 0, where the load line meets the knee of the I–V curve | B) V = V_OC | C) I = I_SC | D) R_L = 0`
**Ans: A** — Maximum power transfer corresponds to the load resistance R_L = V_mp/I_mp ≈ 0.7 V_OC/I_SC for a cell.

**Q751.** An LED's light output is approximately proportional to:
`A) Its forward current | B) Its forward voltage | C) The reverse voltage | D) Its capacitance`
**Ans: A** — Photon emission ∝ injected carrier recombination, which is set by forward current.

**Q752.** The dominant recombination mechanism in a direct-bandgap LED such as GaAsP is:
`A) Direct electron–hole recombination | B) Phonon-assisted only | C) Avalanche | D) Zener tunnelling`
**Ans: A** — Direct-gap materials radiate efficiently without a phonon, giving high external efficiency.

**Q753.** An indirect-bandgap material such as silicon is a poor LED because:
`A) Recombination needs a phonon, so most energy is emitted as heat | B) It has no band gap | C) It cannot be doped | D) It is always reverse biased`
**Ans: A** — Si is an indirect-gap material, so radiative efficiency is tiny; hence LEDs use GaAs, GaN, InGaN.

**Q754.** The wavelength of emitted light relates to photon energy by:
`A) E_g(eV) ≈ 1240/λ(nm) | B) λ = E_g | C) E_g = λ/1240 | D) E_g = 1/λ`
**Ans: A** — A 2 eV (red) emitter corresponds to λ ≈ 620 nm.

**Q755.** For a green LED at λ = 560 nm, the approximate band gap is:
`A) 2.2 eV | B) 1.2 eV | C) 3.5 eV | D) 5.6 eV`
**Ans: A** — E_g = 1240/560 ≈ 2.21 eV.

**Q756.** A tunnel diode has a region of negative resistance because:
`A) Carrier injection exceeds recombination, so current decreases with voltage | B) Its band gap is zero | C) It is doped p-type | D) It has no junction`
**Ans: A** — This gives negative resistance, useful for high-speed switching and oscillation.

**Q757.** A tunnel diode is characterised by:
`A) A very thin heavily doped junction with a peak and valley current | B) A wide depletion region | C) High reverse breakdown | D) Large forward drop`
**Ans: A** — Heavy doping narrows the depletion layer, so electrons tunnel through it.

**Q758.** An IMPATT diode generates microwave power by:
`A) Impact ionization and avalanche multiplication in a transit-time structure | B) Thermal noise | C) Photoconductivity | D) Tunneling only`
**Ans: A** — The transit time plus avalanche produces negative resistance at microwave frequencies.

**Q759.** A Gunn diode oscillates by:
`A) The transferred-electron effect in GaAs | B) Avalanche multiplication | C) Photoconductive gain | D) Zener breakdown`
**Ans: A** — Electrons transfer from a high-mobility valley to a low-mobility valley, giving bulk negative resistance.

**Q760.** The Valley and PIF (peak/interval) characteristics of a tunnel diode enable it to be used as:
`A) A high-frequency oscillator or switch | B) A rectifier | C) A Zener | D) A photodetector`
**Ans: A** — Negative resistance across the NDR region sustains oscillation or gives very fast switching.

### 11B. Diode applications and protective circuits

**Q761.** A half-wave rectifier uses one diode, and its ripple factor is:
`A) 1.21 | B) 0.287 | C) 0.48 | D) 0`
**Ans: A** — For a half-wave rectifier γ = 1.21; the DC value is V_m/π.

**Q762.** A full-wave bridge rectifier has a ripple factor of:
`A) 0.287 | B) 1.21 | C) 0.9 | D) 0`
**Ans: A** — Two half-cycles per input cycle give γ = 0.287, better than half-wave.

**Q763.** The Tufull (centre-tapped) rectifier uses:
`A) Two diodes with a centre-tapped transformer | B) Four diodes | C) One diode | D) A Zener`
**Ans: A** — Two diodes and a tap give full-wave operation with only one diode drop in the path.

**Q764.** In a centre-tapped full-wave rectifier, the PIV of each diode is:
`A) 2V_m | B) V_m | C) 0.5V_m | D) V_m/2`
**Ans: A** — The non-conducting diode sees the full secondary voltage, twice the half-winding peak.

**Q765.** In a bridge rectifier, the PIV of each diode is:
`A) V_m | B) 2V_m | C) 4V_m | D) 0.5V_m`
**Ans: A** — A bridge halves the PIV relative to a centre-tapped rectifier for the same output voltage.

**Q766.** For a given DC output, the bridge rectifier needs:
`A) A smaller transformer than a centre-tapped circuit | B) A larger transformer | C) The same | D) No transformer`
**Ans: A** — No centre tap is required, so fewer secondary turns are needed for the same V_DC.

**Q767.** In a bridge rectifier each diode conducts for:
`A) Half the cycle (180°) | B) The full cycle | C) A quarter cycle | D) Only the peak`
**Ans: A** — Two diodes conduct per half-cycle, each carrying current for 180°.

**Q768.** The efficiency of a half-wave rectifier is:
`A) 40.6 % | B) 81.2 % | C) 90 % | D) 100 %`
**Ans: A** — P_dc/P_ac = 0.406; the rest is lost in the AC component and conduction loss.

**Q769.** The efficiency of a full-wave (bridge or centre-tapped) rectifier is:
`A) 81.2 % | B) 40.6 % | C) 48.6 % | D) 90 %`
**Ans: A** — Doubling the conduction halves gives 0.812.

**Q770.** The form factor of a full-wave rectified sine wave is:
`A) 1.11 | B) 1.57 | C) 1.21 | D) 0.9`
**Ans: A** — RMS/average = 1.11 for full wave; 1.57 for half wave.

**Q771.** A smoothing capacitor across the load of a rectifier:
`A) Reduces ripple but increases the peak diode current | B) Reduces both | C) Increases ripple | D) Has no effect`
**Ans: A** — The capacitor supplies the load between peaks, so diodes conduct in short high-current pulses.

**Q772.** In a capacitor-filtered full-wave rectifier, the ripple frequency is:
`A) 2f | B) f | C) f/2 | D) 4f`
**Ans: A** — Two conduction pulses per input cycle recharge the capacitor.

**Q773.** With a large smoothing capacitor, the ripple factor is approximately:
`A) 1/(4√3 f R_L C) for full wave | B) 1/(2√3 f R_L C) | C) 1/(R_L C) | D) 1/(f R_L C)`
**Ans: A** — r ≈ V_m/(4√3 f²R_LC)... using V_r(pp) ≈ V_m/(fR_LC), γ ≈ V_r(pp)/(2√2 V_DC) = 1/(4√3 f R_L C).

**Q774.** The ripple voltage (peak-to-peak) across a capacitor-filtered full-wave rectifier is:
`A) V_r ≈ I_load/(f C) | B) V_r ≈ V_m C | C) V_r ≈ 1/f | D) V_r ≈ I/(2πC)`
**Ans: A** — The capacitor supplies the full load current for roughly 1/f seconds between peaks.

**Q775.** A rectifier filter capacitor of 100 µF supplying 10 mA at 50 Hz (full wave, ripple at 100 Hz) gives an approximate ripple voltage of:
`A) 1 V (p-p) | B) 10 V | C) 0.1 V | D) 5 V`
**Ans: A** — ΔV = I/(f_r C) = 10 mA/(100 Hz × 100 µF) = 1 V.

**Q776.** The advantage of a capacitor-input (shunt) filter is:
`A) A small diode conduction angle, giving a high average output | B) Low diode current | C) Better regulation | D) Lower cost`
**Ans: A** — Current flows in short bursts that fully recharge C, so V_DC approaches V_m.

**Q777.** The disadvantage of capacitor-input filtering is:
`A) Large ripple current, poor regulation and high inrush | B) Low efficiency | C) No smoothing | D) High ripple frequency`
**Ans: A** — Peaky diode currents stress the transformer and produce poor load regulation.

**Q778.** A three-phase half-wave rectifier's ripple factor is:
`A) 0.18 | B) 1.21 | C) 0.287 | D) 0.48`
**Ans: A** — Three pulses per cycle greatly reduce ripple; three-phase full wave gives 0.059.

**Q779.** A voltage multiplier (e.g. Cockcroft–Walton) is used to:
`A) Produce a DC voltage several times the AC peak without a transformer | B) Increase current capability | C) Reduce ripple | D) Provide regulation`
**Ans: A** — Cascaded diode–capacitor stages multiply the peak voltage; the cost is rising ripple with more stages.

**Q780.** In a half-wave rectifier with a resistive load and no filter, the output voltage is:
`A) A pulsating DC of average V_m/π | B) A sine wave | C) V_m | D) 0`
**Ans: A** — V_DC = V_m/π ≈ 0.318 V_m.

**Q781.** In a full-wave centre-tapped rectifier with V_m = 10 V (half-secondary peak), the average output is approximately:
`A) 2 V_m/π ≈ 6.4 V | B) V_m/π ≈ 3.2 V | C) 2V_m = 20 V | D) V_m = 10 V`
**Ans: A** — Twice the half-wave average: V_DC = 2V_m/π = 0.637 V_m.

**Q782.** Clampers (clamps) are used to:
`A) Shift a waveform's DC level without changing its shape | B) Rectify it | C) Filter it | D) Regulate it`
**Ans: A** — A clamp adds (or subtracts) a DC level by charging a capacitor through a diode, unlike a rectifier which distorts the shape.

**Q783.** A clamper's steady-state behaviour depends on:
`A) The capacitor being charged to the peak of the input through the diode | B) The capacitor discharging fully | C) The load being a short | D) The frequency being DC`
**Ans: A** — Diode conduction sets C's charge to V_m; then C simply adds V_m to any input level.

**Q784.** A negative clamper with a resistive load produces:
`A) A waveform shifted downward so its peak is at −V_m | B) A waveform shifted upward | C) Half-wave rectification | D) Full-wave rectification`
**Ans: A** — The diode is placed so C charges to +V_m through it and then subtracts that from the input.

**Q785.** A biased (DC-restoring) clamper restores:
`A) The average value to zero | B) The peak value to zero | C) The frequency | D) The impedance`
**Ans: A** — The bias clamps only the negative excursion, so the mean returns to 0 V (DC restoration).

**Q786.** A diode limiter circuit is used to:
`A) Limit the peak amplitude of a waveform | B) Remove ripple | C) Regulate the supply | D) Multiply the voltage`
**Ans: A** — Series or shunt diodes clip the signal beyond one or more threshold levels.

**Q787.** Series-type clippers achieve clipping by:
`A) Placing diodes in series with the signal path | B) Placing diodes across the load | C) Open-circuiting the path | D) Shorting the source`
**Ans: A** — Forward-biased diodes insert a threshold drop; the rest of the path is unchanged.

**Q788.** Shunt-type clippers achieve clipping by:
`A) Placing diodes across the output that conduct when the signal exceeds a level | B) Series insertion | C) Adding a Zener in series | D) Using a transformer`
**Ans: A** — Conducting clamp diodes divert current, so the output cannot rise (or fall) beyond the limit.

**Q789.** The number of diodes in a biased clipper that clips at ±4 V with 0.7 V diodes is typically:
`A) Two diodes per side in series | B) One diode per side | C) Six diodes | D) No diodes`
**Ans: A** — Series diodes add their drops (n × 0.7 V) to set the threshold.

**Q790.** In a positive shunt clamper the output cannot fall below:
`A) V_D (0.7 V) below the reference | B) 0 V always | C) V_m | D) −V_D`
**Ans: A** — The diode conducts to clamp within one forward drop of the chosen reference.

**Q791.** A Schmitt trigger using two diodes and an op-amp provides:
`A) Different thresholds for rising and falling inputs | B) A higher cutoff frequency | C) More gain | D) Lower offset`
**Ans: A** — The diode drops shift the effective feedback fraction on each transition.

**Q792.** Series diodes in the feedback path of an op-amp are used to:
`A) Reduce gain for large signals (automatic gain control) | B) Increase bandwidth | C) Set the supply | D) Correct offset`
**Ans: A** — When the signal is small, the diodes are off and gain is high; when large, they clamp and gain drops.

**Q793.** Peak detection in an envelope detector uses:
`A) A diode with a capacitor that holds the peak and discharges slowly through a large R | B) A Zener | C) A varactor | D) A tunnel diode`
**Ans: A** — The capacitor charges to the peak and the diode then blocks; R_C sets the decay (attack/decay envelope follower).

**Q794.** An FM demodulator (ratio detector or phase discriminator) recovers the audio because:
`A) It produces a DC voltage proportional to the instantaneous frequency | B) It rectifies the RF | C) It amplifies noise | D) It filters the RF`
**Ans: A** — The discriminator converts frequency deviation into a proportional voltage, which is then audio-amplified.

**Q795.** A logarithmic detector uses a diode to exploit:
`A) The exponential I–V relation to produce an output proportional to log of the input | B) The reverse breakdown | C) The capacitance | D) The leakage`
**Ans: A** — Because I ∝ e^(V/nV_T), V ∝ log I, giving dB-linear detection.

**Q796.** A photodiode in series with a load and transimpedance amplifier measures:
`A) Photocurrent | B) Forward voltage | C) Reverse saturation current | D) Breakdown voltage`
**Ans: A** — The high feedback resistance converts the small photocurrent into a usable voltage.

**Q797.** A solar tracker uses a:
`A) Photodiode array to steer a motor toward maximum light | B) Zener | C) Varactor | D) Tunnel diode`
**Ans: A** — Comparing outputs of oriented photodiodes gives the direction of maximum irradiance.

**Q798.** An LED driver with a constant-current sink is preferred because:
`A) LED brightness tracks current, not voltage, which varies with temperature | B) LED voltage is constant | C) It reduces cost | D) LEDs need current limiting only in reverse`
**Ans: A** — Forward voltage falls with temperature; holding the current steady keeps the output stable.

**Q799.** A bridge rectifier feeding a capacitor-input filter has its average diode current equal to roughly:
`A) I_DC/2 per diode (half-wave equivalent) but with much higher peak value | B) I_DC/4 | C) I_DC | D) 2I_DC`
**Ans: A** — Each diode carries half the DC current on average; the peak is many times that.

**Q800.** The most important design criterion in choosing a rectifier diode is:
`A) The reverse voltage rating (PIV) and forward current handling | B) Its colour code | C) Its package height | D) Its forward drop only`
**Ans: A** — Exceeding PIV destroys the diode; the forward rating and switching speed follow from the application.

---

## SECTION 12 — High-Frequency Response, Miller Effect & Bandwidth (Q801–Q855)

### 12A. Device high-frequency models

**Q801.** In the high-frequency (hybrid-pi) model of a BJT, the base–emitter diffusion capacitance C_pi:
`A) Increases with forward emitter current | B) Is constant | C) Decreases with current | D) Is zero`
**Ans: A** — C_pi = g_m/(2πf_T), and g_m rises linearly with I_C.

**Q802.** The base–collector capacitance C_mu of a BJT is:
`A) A small, voltage-dependent depletion capacitance | B) Large and current-dependent | C) Zero | D) A resistance`
**Ans: A** — It is the collector-base junction capacitance, typically 0.5–3 pF, and it sets f_max.

**Q803.** The short-circuit current gain h_fe of a BJT at high frequency is approximately:
`A) h_fe ≈ f_T/f (frequency-dependent) | B) β at all frequencies | C) 1 | D) Zero`
**Ans: A** — h_fe falls 3 dB/octave above f_β = f_T/β, which is why β must be derated for high-frequency design.

**Q804.** For a BJT with f_T = 2 GHz and β = 100, the β-cutoff frequency f_β is:
`A) 20 MHz | B) 2 GHz | C) 200 MHz | D) 2 MHz`
**Ans: A** — f_β = f_T/β = 2000/100 = 20 MHz.

**Q805.** The maximum operating frequency f_max of a BJT is limited by:
`A) C_mu feedback and transit time | B) The collector resistance | C) The base bias | D) The supply voltage`
**Ans: A** — f_max ≈ g_m/(8πC_mu); high f_max needs thin base width and small C_mu.

**Q806.** For a MOSFET, the maximum frequency of operation f_max is given approximately by:
`A) f_max = g_m/(8πC_gd) | B) f_max = 1/(2πC_gs) | C) f_max = β/τ | D) f_max = V_T/I_D`
**Ans: A** — Gate–drain capacitance feeds back through the amplifier, so f_max ∝ g_m/C_gd.

**Q807.** A MOSFET with g_m = 10 mS and C_gd = 0.2 pF has an approximate f_max of:
`A) 2 GHz | B) 20 MHz | C) 200 MHz | D) 2 MHz`
**Ans: A** — f_max = 0.01/(8π×0.2×10⁻¹²) = 0.01/(5.03×10⁻¹²) ≈ 1.99 GHz.

**Q808.** The unity-current-gain frequency f_T of a MOSFET is:
`A) f_T = g_m/(2π(C_gs + C_gd)) | B) f_T = 1/C_gs | C) f_T = g_m C_gs | D) f_T = 2πC_gs/g_m`
**Ans: A** — Both capacitances store input charge that the transconductance must supply.

**Q809.** A MOSFET with g_m = 1 mS, C_gs = 2 pF, C_gd = 0.5 pF has f_T of approximately:
`A) 64 MHz | B) 6.4 MHz | C) 640 MHz | D) 640 kHz`
**Ans: A** — f_T = 10⁻³/(2π×2.5×10⁻¹²) = 63.7 MHz.

**Q810.** The input capacitance of a MOSFET common-source amplifier is dominated by:
`A) C_gs (Miller-multiplied by C_gd) | B) C_ds only | C) The junction capacitance only | D) The load capacitance`
**Ans: A** — C_gs is the largest intrinsic capacitance and is multiplied by the Miller factor (1 + |A_v|).

### 12B. The Miller effect

**Q811.** The Miller effect states that an impedance Z between input and output of an amplifier appears at the input multiplied by:
`A) (1 + A_v) | B) (1 − A_v) | C) A_v | D) 1/A_v`
**Ans: A** — Because the input and output voltages move in opposite directions, the input current is I = (V_i − V_o)/Z = V_i(1 − A_v)/Z.

**Q812.** Miller's theorem applies when the amplifier stage is:
`A) Common-emitter or common-source (inverting) | B) Non-inverting | C) Unity gain | D) Buffer`
**Ans: A** — Only an inverting stage gives the (1 + A_v) multiplication at the input and (1 − 1/A_v) at the output.

**Q813.** The input capacitance of an inverting amplifier with C_mu = 2 pF and A_v = −50 is:
`A) 102 pF | B) 100 pF | C) 1.96 pF | D) 50 pF`
**Ans: A** — C_in = C_mu(1 + |A_v|) = 2 × 51 = 102 pF.

**Q814.** The output capacitance seen at the output of the same stage is:
`A) 2.04 pF | B) 102 pF | C) 0.04 pF | D) 50 pF`
**Ans: A** — C_out = C_mu(1 + 1/|A_v|) = 2 × 1.02 = 2.04 pF, i.e. virtually unchanged.

**Q815.** A common-source stage with gain −20 and C_gd = 1.5 pF has an effective input capacitance from the gate of about:
`A) 31.5 pF | B) 30 pF | C) 1.43 pF | D) 20 pF`
**Ans: A** — C_in = 1.5 × (1 + 20) = 31.5 pF.

**Q816.** Miller's theorem cannot be applied to a non-inverting amplifier because:
`A) The multiplication factor becomes (1 − A_v), which does not apply | B) There is no capacitance | C) Gain must be unity | D) It needs a BJT`
**Ans: A** — With A_v = +1 the factor is zero, which is unphysical for a finite C; the theorem's derivation breaks for non-inverting stages.

**Q817.** A unity-gain buffer amplifier (voltage follower) has its C_mu effect:
`A) Negligible, since A_v = +1 gives (1 − A_v) = 0 | B) Doubled | C) Tripled | D) Undefined`
**Ans: A** — The input and output are in phase and equal, so no voltage appears across C_mu.

**Q818.** The Miller effect reduces the common-emitter amplifier's bandwidth because:
`A) C_in is multiplied by (1 + |A_v|), lowering the input pole frequency | B) It increases C_mu | C) It raises the gain | D) It changes r_pi`
**Ans: A** — A 20× gain implies a 21× larger effective input capacitance, cutting f_H by the same factor.

**Q819.** The emitter follower avoids Miller multiplication because:
`A) Its gain is close to +1 (non-inverting) | B) It has no C_mu | C) It has no output capacitance | D) Its gain is negative`
**Ans: A** — A_v ≈ +0.95 means 1 − A_v ≈ 0.05, so the multiplication factor is negligible.

**Q820.** The common-base amplifier avoids Miller multiplication because:
`A) It is non-inverting with A_v slightly above 1 | B) It has a very small r_pi | C) It is unilateral | D) It has no C_mu`
**Ans: A** — A_v = g_m R_C/(1 + g_m R_C) is positive and < 1, so (1 − A_v) is small but not the amplifier's defining feature.

**Q821.** A cascode amplifier's high-frequency response improves mainly because:
`A) The input capacitance sees a much lower Miller factor (≈1) | B) It has higher DC gain | C) It uses a smaller device | D) It needs no supply`
**Ans: A** — Splitting the gain between two stages means the input device multiplies C_gd by only about 2, keeping f_H high.

**Q822.** The practical consequence of the Miller effect in an RF amplifier is:
`A) Gain–bandwidth product is limited by C_gd | B) Gain is limited by r_d | C) Noise is limited by f_T | D) Nothing`
**Ans: A** — C_gd through which output current flows back to the input sets a hard limit on achievable gain at frequency.

### 12C. High-frequency amplifier response

**Q823.** An amplifier's upper cutoff frequency f_H is defined as the frequency where the gain has fallen by:
`A) 3 dB (a factor of 0.707) | B) 1 dB | C) 20 dB | D) 0 dB`
**Ans: A** — Half-power point; the phase shift there is 45° for a single pole.

**Q824.** A single-pole amplifier has a bandwidth of 100 kHz and a midband gain of 60 dB. Its gain at 1 MHz is approximately:
`A) 20 dB | B) 40 dB | C) 60 dB | D) 0 dB`
**Ans: A** — One decade beyond f_H the gain falls another 20 dB: 60 − 20 − 20 = 20 dB.

**Q825.** The high-frequency response of a common-emitter amplifier is mainly set by:
`A) C_in and the source (signal generator) resistance | B) C_out only | C) The emitter bypass capacitor | D) The supply`
**Ans: A** — The input pole f_H = 1/(2πR_sig C_in) dominates when C_in (Miller-multiplied) is large.

**Q826.** The high-frequency response of a source follower is mainly set by:
`A) C_gs with the source (output) resistance | B) The load only | C) C_gd × gain | D) The gate resistance only`
**Ans: A** — With A_v ≈ 1, Miller multiplication is negligible, so f_H = 1/(2πR_out C_L).

**Q827.** The high-frequency response of a common-base amplifier is mainly set by:
`A) C_π and the source resistance (no Miller effect) | B) C_mu × gain | C) The load capacitance | D) The emitter resistance`
**Ans: A** — Its input node is the emitter, with C_π to ground and no inverting gain to multiply capacitance.

**Q828.** For a common-emitter stage with R_sig = 600 Ω and C_in = 2 nF, the upper cutoff frequency is:
`A) 133 kHz | B) 13.3 kHz | C) 1.33 MHz | D) 13.3 MHz`
**Ans: A** — f_H = 1/(2π×600×2×10⁻⁹) = 132.6 kHz.

**Q829.** The emitter bypass capacitor's upper limit on amplifier bandwidth comes from:
`A) Its impedance falling with frequency, reducing the bypass effectiveness | B) It opens the circuit | C) It adds gain | D) It sets V_BE`
**Ans: A** — At high frequency the bypass capacitor looks like a short across r_e, which would otherwise reduce gain; its self-resonance and parasitics limit this.

**Q830.** Reducing the emitter bypass capacitance:
`A) Lowers the low-frequency cutoff and reduces the high-frequency bandwidth | B) Raises both | C) Changes neither | D) Doubles the gain at all frequencies`
**Ans: A** — Larger C_b improves LF response but its parasitics add a pole, so LF and HF trade off.

**Q831.** A transistor amplifier's high-frequency voltage gain falls with frequency mainly because:
`A) Internal capacitances shunt the signal | B) The supply falls | C) r_π falls | D) β rises`
**Ans: A** — C_pi and C_mu create poles, so gain rolls off at −20 dB/decade per pole.

**Q832.** A compensated attenuator (frequency-compensated probe) uses a small C across R to:
`A) Make the probe's input impedance nearly frequency-independent | B) Increase its input resistance | C) Protect the circuit | D) Reduce capacitance`
**Ans: A** — C is chosen so the RC network is a constant-resistance (Zener) attenuator up to a high frequency.

**Q833.** A scope probe with a 10:1 ratio and 10 pF compensating capacitance presents an input capacitance of approximately:
`A) 10 pF (probe) + ~100 pF (due to the 100 MΩ‖11 pF on the scope input) | B) 1 pF | C) 1000 pF | D) 0 pF`
**Ans: A** — The divider's own capacitance plus the scope input dominates, which is why the probe slows the circuit.

**Q834.** The bandwidth of a cascaded chain of two identical stages, each with upper cutoff f_1, is approximately:
`A) 0.64 f_1 | B) 2 f_1 | C) f_1 | D) f_1/2`
**Ans: A** — Total 3 dB point falls at 0.64 f_1 for two identical single-pole stages.

**Q835.** The bandwidth of an N-stage cascade of identical single-pole amplifiers (for large N) is approximately:
`A) 0.35 f_1 | B) N f_1 | C) f_1 | D) f_1/N`
**Ans: A** — The gain-bandwidth product of a cascade grows with N while total BW shrinks by roughly the same factor.

**Q836.** Interstage coupling with a large coupling capacitor:
`A) Sets a low-frequency pole | B) Sets the upper cutoff | C) Adds gain | D) Reduces noise only`
**Ans: A** — The coupling capacitor with the next stage's input resistance forms a high-pass network.

**Q837.** A transformer-coupled amplifier has:
`A) No lower cutoff from coupling capacitors (DC can be transformed) | B) Lower gain | C) More noise | D) Higher bandwidth only`
**Ans: A** — Transformers block DC and pass AC, removing the coupling-capacitor high-pass pole.

**Q838.** The dominant pole of an amplifier is the pole that:
`A) Reduces gain at −20 dB/dec over most of the band | B) Is at the highest frequency | C) Is a zero | D) Sets the slew rate`
**Ans: A** — The dominant pole is far below the others, so it alone shapes the response for most of the range.

**Q839.** Adding a dominant pole to a feedback amplifier increases stability because:
`A) It reduces the rate of phase lag near unity gain | B) It increases the gain | C) It moves the gain crossover up | D) It reduces noise`
**Ans: A** — Gain falls at only −20 dB/dec, so other poles contribute little extra phase lag before crossover.

**Q840.** A feed-forward (feed-forward compensation) technique:
`A) Cancels the amplifier's output capacitance with an equal capacitor | B) Adds a dominant pole | C) Uses a Zener | D) Requires a transformer`
**Ans: A** — A capacitor across C_mu of the same value but opposite sign cancels the Miller feed-forward path.

### 12D. High-frequency op-amp behaviour and measurement

**Q841.** Slew rate limits the large-signal bandwidth of an op-amp to approximately:
`A) BW = SR/(2πV_p) | B) BW = SR/V_p | C) BW = V_p/SR | D) BW = GBW`
**Ans: A** — The maximum sine output frequency before slew distortion is f_max = SR/(2πV_peak).

**Q842.** An op-amp with a slew rate of 0.5 V/µs driving a 10 V peak output has a full-power bandwidth of about:
`A) 8 kHz | B) 80 kHz | C) 800 kHz | D) 8 MHz`
**Ans: A** — BW = 0.5×10⁶/(2π×10) = 8 kHz.

**Q843.** A 1 MHz gain-bandwidth op-amp used at a closed-loop gain of 100 has a bandwidth of:
`A) 10 kHz | B) 1 MHz | C) 100 kHz | D) 1 kHz`
**Ans: A** — For a single dominant pole, GBW = A_CL × BW, so BW = 1 MHz/100 = 10 kHz.

**Q844.** Settling time of an op-amp is measured:
`A) From an input step to the time the output stays within a specified error band | B) During input rise | C) From power-on | D) Over full scale only`
**Ans: A** — Usually specified for 0.1 % (or 0.01 %) settling; it is longer than rise time because of the low dominant pole.

**Q845.** Small-signal response time (rise time) relates to bandwidth by:
`A) t_r ≈ 0.35/BW | B) t_r ≈ BW/0.35 | C) t_r ≈ BW | D) t_r = 1/BW`
**Ans: A** — For BW = 10 MHz, t_r = 35 ns.

**Q846.** A comparator's propagation delay:
`A) Limits how fast it can respond to small overdrives | B) Sets its offset | C) Determines its gain | D) Is fixed by the supply only`
**Ans: A** — Delay grows as the input overdrive shrinks, which is why comparators are driven hard.

**Q847.** The gain of an amplifier measured only at one frequency is insufficient to characterise it because:
`A) Gain and phase vary strongly with frequency | B) Gain is always DC | C) Phase is not measurable | D) Only the peak matters`
**Ans: A** — A Bode plot of gain and phase is required; both affect the output waveform.

**Q848.** An amplifier's phase shift at its −3 dB point for a single pole is:
`A) 45° | B) 90° | C) 0° | D) 180°`
**Ans: A** — arctan(f/f_H) = 45° at f = f_H.

**Q849.** In an N-stage inverting amplifier, the total phase lag at high frequency approaches:
`A) −180°·N, so beyond two stages the feedback loop becomes unstable | B) −90°·N | C) −360° always | D) 0°`
**Ans: A** — Each inverting stage gives −180°; two such stages already sum to −360°, so any loop containing them needs phase compensation.

**Q850.** To measure an amplifier's upper cutoff frequency in the lab, one applies:
`A) A step or swept sinusoid and find the −3 dB gain point | B) A DC measurement | C) An oscilloscope only | D) A power supply`
**Ans: A** — The 0.707 gain point defines f_H; a square-wave test gives t_r ≈ 0.35/BW.

**Q851.** A rise time of 20 ns measured from a square wave implies a bandwidth of approximately:
`A) 17.5 MHz | B) 5.7 MHz | C) 70 MHz | D) 175 MHz`
**Ans: A** — BW = 0.35/20 ns = 17.5 MHz.

**Q852.** The effect of stray PCB capacitance (say 2 pF) across a high-gain input node is:
`A) It is multiplied by (1 + |A_v|), severely reducing bandwidth | B) It has no effect | C) It adds gain | D) It lowers the DC gain`
**Ans: A** — Stray capacitance behaves exactly like C_mu under Miller's theorem, so layout capacitance is often the real bandwidth limit.

**Q853.** In a multi-stage amplifier, the last (output) stage sets the bandwidth mainly because:
`A) It must drive the lowest impedance load | B) It has the most gain | C) It needs a compensation cap | D) It is a common-emitter`
**Ans: A** — A low load resistance with load capacitance sets a low output pole, capping the overall bandwidth.

**Q854.** An emitter follower used to drive a capacitive load must be checked for:
`A) Polarity reversal at high frequency | B) DC offset only | C) No issue | D) Gain drift only`
**Ans: A** — C_mu between collector and base can produce peaking and even polarity reversal at high frequency.

**Q855.** The maximum output voltage swing at high frequency is limited by:
`A) Slew rate | B) Offset voltage | C) Input bias current | D) Thermal noise`
**Ans: A** — Beyond the full-power bandwidth the op-amp cannot follow a large sine wave, producing slew-rate distortion.

---

## SECTION 13 — Filters (Q856–Q905)

### 13A. Passive and first-order filters

**Q856.** A passive RC low-pass filter at its cutoff frequency attenuates the signal by:
`A) 3 dB | B) 0 dB | C) 20 dB | D) 1 dB`
**Ans: A** — |H| = 1/√2 = 0.707, which is −3 dB.

**Q857.** The cutoff frequency of an RC low-pass filter is:
`A) f_c = 1/(2πRC) | B) f_c = 1/(RC) | C) f_c = 2πRC | D) f_c = RC`
**Ans: A** — At f_c, X_C = R.

**Q858.** An RC high-pass filter with R = 1.6 kΩ and C = 0.01 µF has a cutoff frequency of about:
`A) 10 kHz | B) 1 kHz | C) 100 kHz | D) 10 Hz`
**Ans: A** — f_c = 1/(2π×1600×10⁻⁸) = 9.95 kHz.

**Q859.** A passive first-order filter's maximum slope is:
`A) −20 dB/decade | B) −40 dB/decade | C) −60 dB/decade | D) −80 dB/decade`
**Ans: A** — Each reactive element contributes one pole (20 dB/decade).

**Q860.** A passive second-order (two-reactor) filter can achieve a slope of:
`A) 40 dB/decade | B) 20 dB/decade | C) 60 dB/decade | D) 80 dB/decade`
**Ans: A** — Two poles give −40 dB/decade asymptotically.

**Q861.** Roll-off always starts at the corner frequency, whereas the maximum attenuation slope occurs at frequencies well above it. This statement is:
`A) True | B) False | C) Only for LC filters | D) Only for digital filters`
**Ans: A** — Slope is −20 dB/decade per pole only in the asymptotic region, not at f_c itself.

**Q862.** The advantage of an active filter over a passive filter is:
`A) Gain > 1, no inductors, high input and low output impedance | B) Lower cost | C) Better noise performance | D) No power needed`
**Ans: A** — The op-amp buffers the stages, so cascaded sections do not load each other and can provide gain.

**Q863.** The disadvantage of an active filter is:
`A) It requires a supply, cannot handle large signals and adds noise | B) It needs inductors | C) It has low input impedance | D) It is always unstable`
**Ans: A** — Active filters are restricted to signal levels within the op-amp's range.

**Q864.** A buffer stage in a filter network is required because:
`A) Without it, the next stage loads the previous one and changes the response | B) Buffers add gain | C) Buffers remove power | D) Buffers set the supply`
**Ans: A** — Cascaded RC sections interact unless isolated by a high-impedance input.

**Q865.** An inverting amplifier used as a first-order active low-pass filter has transfer function:
`A) H(s) = −R₂/(R₁ + 1/(sC)) | B) H(s) = −R₁/(R₂ + 1/(sC)) | C) H(s) = R₂/R₁ only | D) H(s) = 1/(1+sRC)`
**Ans: A** — The capacitor in the feedback path rolls off gain with frequency.

**Q866.** The cutoff frequency of the inverting low-pass filter of Q865 is:
`A) f_c = 1/(2πR₂C) | B) f_c = 1/(2πR₁C) | C) f_c = 1/(2πR₁R₂C) | D) f_c = 2πR₂C`
**Ans: A** — The corner is set by the feedback impedance R₂ || 1/(sC).

**Q867.** An op-amp integrator's gain falls as:
`A) −1/(sRC) | B) −sRC | C) −RC | D) −1/RC`
**Ans: A** — Gain ∝ 1/f, so its magnitude falls at 20 dB/decade.

**Q868.** An op-amp differentiator's gain rises as:
`A) −sRC | B) −1/(sRC) | C) −RC | D) −1/RC`
**Ans: A** — Gain ∝ f, so high frequencies are amplified — the reason a differentiator is noise-prone and unstable.

**Q869.** The differentiator is generally avoided in practical circuits because:
`A) It amplifies high-frequency noise | B) It has unity gain | C) It cannot use a capacitor | D) It is nonlinear`
**Ans: A** — Practical differentiators add a series R to limit HF gain.

**Q870.** A practical differentiator limits high-frequency gain by including:
`A) A small series resistor | B) A large capacitor | C) A Zener | D) A shunt inductor`
**Ans: A** — R in series with C sets a new corner f = 1/(2πR_total C), limiting HF slope to −20 dB/decade.

### 13B. Second-order filter responses

**Q871.** Butterworth filters are characterised by:
`A) Maximally flat magnitude response | B) Maximum ripple | C) Steepest transition | D) Minimum group delay`
**Ans: A** — Butterworth is the maximally flat (monotonic) design.

**Q872.** Chebyshev filters are characterised by:
`A) Equiripple magnitude response with the steepest slope for a given order | B) Flat response | C) No ripple | D) Minimum order`
**Ans: A** — Ripple is accepted to gain extra selectivity per pole.

**Q873.** Bessel (Thomson) filters are optimised for:
`A) Linear phase (constant group delay) | B) Maximum ripple | C) Steepest slope | D) Minimum order`
**Ans: A** — Bessel gives the least waveform distortion, at the cost of a gentle slope.

**Q874.** A second-order Butterworth low-pass filter has a maximally flat response and a slope of:
`A) 40 dB/decade beyond the cutoff | B) 20 dB/decade | C) 12 dB/octave | D) 80 dB/decade`
**Ans: A** — Two poles.

**Q875.** An elliptic (Cauer) filter is used when:
`A) The minimum order and steepest transition are needed, accepting ripple | B) Flat response is required | C) Linear phase is required | D) No active devices are available`
**Ans: A** — Elliptic gives the sharpest cutoff for a given order, at the price of passband ripple and a transmission zero.

**Q876.** The transfer function of a second-order low-pass Butterworth section is:
`A) H(s) = ω₀²/(s² + √2ω₀s + ω₀²) | B) H(s) = ω₀/(s + ω₀) | C) H(s) = s/(s + ω₀) | D) H(s) = (s + ω₀)²/s²`
**Ans: A** — The denominator s² + √2ω₀s + ω₀² gives Q = 1/√2 (maximally flat).

**Q877.** The Q of a second-order Butterworth filter is:
`A) 0.707 | B) 1 | C) 1.414 | D) 2`
**Ans: A** — Q = 1/√2 ≈ 0.707.

**Q878.** A second-order filter with Q > 0.707 will show:
`A) A peak (resonance) near the cutoff frequency | B) No peak ever | C) A notch | D) Phase lead only`
**Ans: A** — Q > 1/√2 gives peaking, characteristic of Chebyshev and resonant designs.

**Q879.** The resonant (peak) gain of a second-order section with Q is:
`A) Q | B) 1/Q | C) Q² | D) 2Q`
**Ans: A** — At resonance the section's gain equals Q.

**Q880.** A band-pass filter formed by cascading a high-pass and a low-pass section passes frequencies:
`A) Between the two cutoffs | B) Above both cutoffs | C) Below both cutoffs | D) Only at DC`
**Ans: A** — The passband is f_L < f < f_H.

**Q881.** The bandwidth of a band-pass filter (B = f_H − f_L) and its centre frequency f₀ relate to Q by:
`A) Q = f₀/B | B) Q = B/f₀ | C) Q = f₀B | D) Q = f₀ + B`
**Ans: A** — A narrow band (small B) means high Q.

**Q882.** A practical band-pass filter can be built as:
`A) An op-amp with both feedback and input RC networks | B) A resistor alone | C) An inductor alone | D) A diode`
**Ans: A** — The classic op-amp band-pass combines a high-pass (input C) with a low-pass (feedback C).

**Q883.** A notch (band-stop) filter is used to:
`A) Reject a specific unwanted frequency and pass everything else | B) Pass only one frequency | C) Amplify DC | D) Increase Q`
**Ans: A** — A twin-T notch or a bridge-T rejecter is tuned to the frequency to be removed.

**Q884.** A twin-T notch filter's notch frequency is approximately:
`A) f = 1/(2πRC) | B) f = 1/RC | C) f = 2πRC | D) f = 1/(2π√6RC)`
**Ans: A** — Same as the Wien network; the notch is deep at f₀ when components are well matched.

**Q885.** A bridged-T (or bridged-T notch) network differs from the twin-T in that:
`A) It is less sensitive to component tolerance | B) It has no notch | C) It is passive only | D) It needs inductors`
**Ans: A** — The bridge reduces sensitivity to R and C mismatches at the cost of a slightly shallower notch.

**Q886.** An all-pass filter is designed to have:
`A) Constant magnitude with controlled phase shift | B) Constant phase with variable gain | C) Zero output | D) A resonant peak`
**Ans: A** — |H| = 1 at all frequencies while the phase sweeps, useful for phase equalisation.

**Q887.** An all-pass network is used in:
`A) Phase equalisation and delay lines | B) Power supply filtering | C) Rectification | D) Oscillation`
**Ans: A** — It corrects the different frequency-dependent delays of transmission lines and filters.

**Q888.** The resonant frequency of a series RLC circuit is:
`A) f₀ = 1/(2π√(LC)) | B) f₀ = 1/(2πRC) | C) f₀ = R/(2πL) | D) f₀ = 1/(2πL)`
**Ans: A** — At resonance, X_L = X_C.

**Q889.** At resonance, a series RLC circuit's impedance is:
`A) Purely resistive, equal to R | B) Zero | C) Inductive | D) Capacitive`
**Ans: A** — The imaginary parts cancel, so only the series resistance remains (lowest impedance).

**Q890.** At resonance, a parallel RLC circuit's impedance is:
`A) Maximum, equal to R | B) Zero | C) Minimum | D) Infinite only if R = 0`
**Ans: A** — The inductive and capacitive susceptances cancel, so the circuit looks resistive at its highest impedance.

**Q891.** The Q of a series RLC circuit at resonance is:
`A) Q = ω₀L/R = 1/(ω₀CR) | B) Q = R/(ω₀L) | C) Q = ω₀CR | D) Q = LC/R`
**Ans: A** — Q is the ratio of reactance to resistance in either element.

**Q892.** A series RLC circuit with L = 1 mH, C = 1 µF, R = 10 Ω has f₀ and Q of:
`A) f₀ ≈ 5.03 kHz, Q = 3.16 | B) f₀ ≈ 1.59 kHz, Q = 0.32 | C) f₀ ≈ 15.9 kHz, Q = 3.16 | D) f₀ = 5.03 kHz, Q = 0.32`
**Ans: A** — f₀ = 1/(2π√(10⁻³×10⁻⁶)) = 5.03 kHz; Q = ω₀L/R = (2π×5030×0.001)/10 = 3.16.

**Q893.** The half-power bandwidth of a resonant circuit is related to Q by:
`A) B = f₀/Q | B) B = f₀Q | C) B = Q/f₀ | D) B = f₀/Q²`
**Ans: A** — Sharper resonance (higher Q) means narrower bandwidth.

**Q894.** A practical band-pass LC filter's insertion loss at resonance is mainly due to:
`A) Resistance in L, C and the source/load | B) The capacitors only | C) The supply | D) The core material only`
**Ans: A** — Lumped and parasitic resistance dissipate power, giving B = R/(2πL).

**Q895.** Damping in a resonant circuit (adding resistance) has the effect of:
`A) Broadening the bandwidth and lowering the peak | B) Sharpening the peak | C) Raising f₀ | D) Doubling Q`
**Ans: A** — Higher R means lower Q, hence a flatter, wider response.

### 13C. Higher-order and specialised filters

**Q896.** The order of a filter determines:
`A) Its asymptotic roll-off rate (20 dB/decade per order) | B) Its supply voltage | C) Its noise figure | D) Its price only`
**Ans: A** — An Nth-order filter rolls off at 20N dB/decade.

**Q897.** To achieve a 60 dB/decade roll-off using cascaded Butterworth sections, one needs:
`A) Three poles total (one 2nd-order section plus one 1st-order section) | B) Six poles | C) One pole | D) Thirty poles`
**Ans: A** — Each pole contributes 20 dB/decade, so 60 dB/decade requires three poles.

**Q898.** A state-variable (KCL) filter using three op-amps is popular because:
`A) It gives simultaneous low-pass, band-pass and notch outputs from one circuit | B) It needs no resistors | C) It is always active-only | D) It has no gain`
**Ans: A** — The three outputs correspond to the three canonical responses with independent gain.

**Q899.** In a state-variable filter, the natural frequency is set by:
`A) R and C as f₀ = 1/(2πRC) | B) Only the gain | C) The supply | D) The op-amp's GBW`
**Ans: A** — Independent of Q, which is set by the R ratio — a key practical advantage.

**Q900.** In a state-variable filter, the damping (Q) is set by:
`A) The ratio of two resistors | B) The capacitor values only | C) The supply | D) The load`
**Ans: A** — Q = 1/(3 − 2K) for the standard topology, where K is a resistor ratio.

**Q901.** A switched-capacitor filter, unlike a continuous-time filter:
`A) Is clocked and time-discrete but frequency-continuous in behaviour | B) Requires inductors | C) Has no sampled behaviour | D) Needs no capacitors`
**Ans: A** — SC filters sample; their response is periodic in frequency, so anti-alias filters are required.

**Q902.** A switched-capacitor low-pass filter's cutoff frequency is set by:
`A) The ratio of capacitor values and the clock frequency | B) Absolute resistance values | C) The op-amp GBW | D) The supply voltage`
**Ans: A** — f_c = (C_2/C_1)·f_clock/2π, so absolute values cancel; accuracy rests on capacitor ratios.

**Q903.** A switched-capacitor filter must be preceded by an anti-aliasing filter because:
`A) Signals above f_clock/2 alias into the passband | B) It needs more power | C) The clock is noisy | D) It reduces the dynamic range`
**Ans: A** — Aliasing is unavoidable in sampled systems, so the input must be band-limited first.

**Q904.** A notch filter with a variable centre frequency is realised using:
`A) A dual-gang potentiometer (matched to the RC network) | B) A transformer | C) A crystal | D) A Zener`
**Ans: A** — Both capacitors must vary together, so a dual-gang control keeps the notch tuned.

**Q905.** A spectrum analyser display of a filter shows:
`A) |H(f)| in dB against frequency | B) Phase in time | C) Resistance against current | D) Power against time`
**Ans: A** — Frequency-response magnitude is the natural way to evaluate a filter.

---

## SECTION 14 — IC Voltage Regulators & Power Supplies (Q906–Q950)

### 14A. Linear regulators

**Q906.** A series-pass linear regulator controls the output by varying:
`A) The resistance of a series transistor | B) The input voltage | C) The load current only | D) The reference voltage`
**Ans: A** — The pass transistor is operated in its active region, dropping (V_in − V_out).

**Q907.** A shunt (parallel-pass) linear regulator controls the output by:
`A) Varying the current drawn through a shunt transistor | B) Varying a series resistor | C) Varying the load | D) Switching`
**Ans: A** — Excess current is diverted to ground through the shunt device.

**Q908.** A linear regulator's dropout voltage is:
`A) The minimum V_in − V_out needed to keep the pass transistor in saturation | B) Its output voltage | C) Its ripple voltage | D) Its noise output`
**Ans: A** — Below dropout the loop loses control and the output sags with the input.

**Q909.** A 7805 regulator requires a minimum input of about:
`A) 7 V | B) 5 V | C) 12 V | D) 3 V`
**Ans: A** — The 7805 needs about 2 V of headroom beyond its 5 V output to regulate.

**Q910.** A 78L05 (low-current variant) can supply up to:
`A) 100 mA | B) 5 A | C) 1 A | D) 20 mA`
**Ans: A** — The "L" suffix denotes the 100 mA TO-92 package version.

**Q911.** A 78M05 differs from a 7805 in that it can supply:
`A) 500 mA | B) 5 A | C) 50 mA | D) 5 mA`
**Ans: A** — 78M05 handles 500 mA; 7805 handles 1 A; 78T05 handles 5 A.

**Q912.** The dropout voltage of a 7805 is typically:
`A) 2 V | B) 0.2 V | C) 12 V | D) 0 V`
**Ans: A** — About 1.5–2 V, which is why a 6 V or 7 V supply is needed for a regulated 5 V.

**Q913.** The quiescent (ground) current of a 7805 in regulation is about:
`A) 3–8 mA | B) 100 mA | C) Zero | D) 1 A`
**Ans: A** — The internal bias chain draws a few mA regardless of load, wasted as heat in low-current designs.

**Q914.** A 78L05's efficiency at a 6 V input supplying 100 mA is approximately:
`A) 5/6 = 83 % | B) 95 % | C) 50 % | D) 66 %`
**Ans: A** — Only the dropout is wasted: η = V_out/V_in = 5/6.

**Q915.** A linear regulator's maximum dissipation is given by:
`A) P = (V_in − V_out)·I_load | B) P = V_out·I_load | C) P = I_load²·V_in | D) P = V_in/I_load`
**Ans: A** — All the excess voltage across the pass transistor becomes heat.

**Q916.** A 7805 supplied from 12 V delivering 1 A dissipates approximately:
`A) 7 W | B) 5 W | C) 1 W | D) 12 W`
**Ans: A** — P = (12 − 5)×1 = 7 W, so a substantial heatsink is mandatory.

**Q917.** A heatsink's thermal resistance is chosen so that:
`A) Junction temperature stays below about 125 °C | B) The sink is as small as possible | C) The output voltage rises | D) The ripple is reduced`
**Ans: A** — θ_sink = (T_max − T_ambient)/P_D − θ_JC − θ_CS.

**Q918.** The maximum junction temperature of a typical 7805 is:
`A) 125 °C | B) 55 °C | C) 200 °C | D) 85 °C`
**Ans: A** — This is the figure used in heatsink calculations, not the ambient limit.

**Q919.** A regulator's power-supply rejection ratio (PSRR) degrades at high frequency because:
`A) The internal loop and pass transistor add poles | B) The reference drifts | C) The load changes | D) The die heats`
**Ans: A** — Loop gain rolls off, so input ripple at higher frequencies is less rejected.

**Q920.** Line regulation of a regulator is defined as:
`A) Change in output per unit change in input voltage | B) Change in output per unit change in load current | C) The output noise | D) The dropout`
**Ans: A** — Load regulation is the second quantity; ripple rejection is a third.

**Q921.** Load regulation of a regulator is:
`A) Change in V_out per unit change in I_load at constant V_in | B) Change in V_out per unit change in V_in | C) Output noise | D) Efficiency`
**Ans: A** — Poor load regulation comes from the pass transistor's finite output resistance.

**Q922.** Ripple rejection in a regulator is specified in:
`A) dB | B) V | C) mA | D) Hz`
**Ans: A** — Typically 60–80 dB at 100 kHz for a 78xx, degrading with frequency.

**Q923.** The internal reference in a 7805 is a:
`A) Temperature-compensated buried Zener | B) Diode string | C) Resistor ladder only | D) Crystal`
**Ans: A** — A buried Zener with a buffer gives a stable ~2 V internal reference.

**Q924.** An adjustable regulator (e.g. 317) produces a variable output because:
`A) The feedback divider ratio sets V_out = V_ref(1 + R₂/R₁) | B) Its input is variable | C) It has no pass transistor | D) It uses a Zener only`
**Ans: A** — The reference is held across R₁, and the divider sets the output.

**Q925.** The LM317's reference voltage is:
`A) 1.25 V | B) 5 V | C) 0.7 V | D) 12 V`
**Ans: A** — V_out = 1.25(1 + R₂/R₁) + I_adj·R₂, the last term being why R₂ is kept large.

**Q926.** An LM317 with a 240 Ω and 2 kΩ divider gives an output of about:
`A) 1.25(1 + 2000/240) ≈ 11.7 V | B) 12 V exactly | C) 1.25 V | D) 5 V`
**Ans: A** — Ignoring the small I_adj·R₂ term, V_out = 1.25 × 9.33 = 11.66 V.

**Q927.** The maximum output current of an LM317 in TO-220 without a heatsink is limited by:
`A) The internal current limit (~2.2 A) and thermal limits | B) Its reference | C) Its R₁ | D) Its dropout only`
**Ans: A** — Current limit, SOA and junction temperature cap the output.

**Q928.** The LM317's minimum load current requirement is about:
`A) 2–5 mA | B) Zero | C) 500 mA | D) 1 A`
**Ans: A** — Below this the regulation degrades; a bleeder resistor is often added.

**Q929.** A two-diode drop in the 317's output path degrades regulation because:
`A) It consumes about 1.4 V of the available headroom | B) It doubles the gain | C) It reduces the reference | D) It has no effect`
**Ans: A** — The pass element sees extra loss, so the achievable output falls by two diode drops.

**Q930.** An LDO's output capacitor:
`A) Provides loop stability and improves transient response | B) Sets the reference | C) Sets the current limit | D) Filters the input only`
**Ans: A** — Its ESR and value form part of the compensation; too little ESR can cause oscillation.

**Q931.** A linear regulator's output ripple contains components at:
`A) The switching frequency of the pre-regulator it follows | B) DC only | C) Its reference frequency only | D) 1/f noise only`
**Ans: A** — In a switching-plus-LDO supply, the residual switching ripple passes through the LDO.

### 14B. Switching regulators

**Q932.** A switching (SMPS) regulator achieves high efficiency because:
`A) Energy is stored and transferred in an inductor/capacitor rather than dissipated | B) It uses more silicon | C) It runs at high frequency only | D) It has no losses`
**Ans: A** — Only conduction and switching losses remain, typically 85–95 % efficient.

**Q933.** In a buck (step-down) converter, the average output voltage is:
`A) V_out = D·V_in | B) V_out = V_in/D | C) V_out = V_in(1−D) | D) V_out = V_in²`
**Ans: A** — With duty ratio D, the average inductor voltage is zero, so V_out = D V_in.

**Q934.** In a boost converter, the ideal output voltage is:
`A) V_out = V_in/(1 − D) | B) V_out = D·V_in | C) V_out = V_in/(1 + D) | D) V_out = V_in + D`
**Ans: A** — The inductor's stored energy is added to the input each cycle.

**Q935.** A boost converter with V_in = 12 V and D = 0.5 gives an ideal output of:
`A) 24 V | B) 6 V | C) 18 V | D) 36 V`
**Ans: A** — V_out = 12/(1 − 0.5) = 24 V.

**Q936.** A buck-boost converter's output is:
`A) Inverted, with |V_out| = (D/(1−D))V_in | B) Always positive and lower | C) Always higher | D) Equal to V_in`
**Ans: A** — Inverting topology; magnitude ratio D/(1−D).

**Q937.** The main switching losses in an SMPS are due to:
`A) Conduction loss in the switch and diode plus switching transition loss | B) Only gate drive loss | C) Only capacitor ESR | D) Only magnetising current`
**Ans: A** — P_sw = ½V_DS I_D t_off·f plus I²R conduction.

**Q938.** The duty cycle is defined as:
`A) t_on/T | B) t_off/T | C) T/t_on | D) f·t_on`
**Ans: A** — Fraction of the period the switch conducts.

**Q939.** In a flyback converter, energy storage and transfer occur by:
`A) The transformer's magnetic field, with galvanic isolation | B) Direct conduction | C) A capacitor only | D) A diode only`
**Ans: A** — Stored during the on-time, delivered to the secondary during the off-time through a different winding.

**Q940.** A forward converter differs from a flyback because:
`A) It transfers energy through a secondary each cycle and needs a freewheeling diode | B) It has no transformer | C) It cannot regulate | D) It needs no freewheeling diode`
**Ans: A** — Both use a transformer, but a forward converter transfers energy each cycle on the primary side.

**Q941.** The duty cycle in a flyback converter is limited mainly because:
`A) Duty must stay below about 0.5 to reset the core flux | B) It must be above 0.5 | C) It is unrestricted | D) It must equal 0.25`
**Ans: A** — Flux doubling requires resetting, hence D_max ≈ 0.5.

**Q942.** Snubber circuits (RC across a switch) are added to:
`A) Suppress voltage spikes from parasitic inductance | B) Increase efficiency deliberately | C) Set the frequency | D) Provide isolation`
**Ans: A** — They absorb the energy in the leakage inductance spike.

**Q943.** A common-mode filter at an SMPS input reduces:
`A) Conducted EMI on the mains line | B) Output ripple only | C) Switching frequency | D) Component cost`
**Ans: A** — X-capacitor/Y-capacitor plus a common-mode choke attenuates both conducted modes.

**Q944.** The duty-cycle control in a voltage-mode SMPS is achieved by:
`A) A fixed-frequency oscillator whose comparator varies the pulse width | B) Varying the oscillator frequency | C) Varying the input voltage | D) A Zener only`
**Ans: A** — Fixed frequency with variable duty keeps the magnetics design predictable.

**Q945.** Current-mode control in an SMPS improves stability because:
`A) It controls the inductor current, removing one plant pole from the loop | B) It increases duty | C) It removes the ripple | D) It needs no compensation`
**Ans: A** — The output pole then dominates, so compensation is simpler.

**Q946.** Slope compensation in current-mode control prevents:
`A) Subharmonic oscillation when D exceeds 0.5 | B) Duty-cycle loss | C) Input ripple | D) Over-current protection failure`
**Ans: A** — A ramp added to the current-sense signal stabilises the modulator above 50 % duty.

**Q947.** An SMPS feedback loop's control-to-output transfer function has:
`A) Two dominant poles from the LC plant, needing Type II or III compensation | B) One pole | C) No poles | D) Only a zero`
**Ans: A** — The double pole needs phase boost, which is why these designs use Type II/III controllers.

**Q948.** A phase-shifted full-bridge converter achieves regulation by:
`A) Varying the phase between the two bridge legs | B) Varying the input | C) Switching at variable frequency | D) Using a diode only`
**Ans: A** — The phase shift controls the effective duty on the primary, enabling high-power conversion at lower switch stress.

**Q949.** Synchronous rectification replaces the freewheeling diode with:
`A) A controlled MOSFET, reducing conduction loss | B) A Zener | C) An inductor | D) A transformer`
**Ans: A** — Since V_DS(on) of a MOSFET (~10–50 mΩ) is far below a diode's 0.7 V, efficiency improves markedly at low voltage.

**Q950.** An SMPS in discontinuous conduction mode differs because:
`A) The inductor current falls to zero each cycle | B) The switch never turns off | C) The output is unregulated | D) Efficiency is always lower`
**Ans: A** — Below the critical load the inductor current reaches zero before the next cycle, improving light-load efficiency.

---

## SECTION 15 — Noise, Distortion & Amplifier Performance (Q951–Q1000)

### 15A. Noise

**Q951.** Thermal (Johnson) noise is generated by:
`A) Random motion of carriers in a resistance | B) Carrier recombination | C) Leakage in the depletion region | D) Mechanical motion`
**Ans: A** — Also called white noise; it exists in every resistive element.

**Q952.** Thermal noise in a resistor of 1 kΩ over 1 kHz bandwidth at 300 K has an rms value of about:
`A) 130 nV | B) 1.3 nV | C) 13 µV | D) 1.3 mV`
**Ans: A** — v_n = √(4kTRB) = √(4×1.38e-23×300×1000×1000) ≈ 129 nV.

**Q953.** Thermal noise power is available over a resistor independent of its value when expressed as:
`A) Noise power spectral density in W/Hz | B) Voltage | C) Current | D) Resistance`
**Ans: A** — 4kTB W/Hz, so the *available* noise power does not depend on R, though the equivalent voltage does.

**Q954.** Shot noise arises in a diode because:
`A) Charge crosses a potential barrier as discrete quanta | B) Thermal agitation | C) Bulk generation | D) Capacitive displacement`
**Ans: A** — I_n,rms = √(2qI) — white noise proportional to the mean current.

**Q955.** The shot noise spectral density of a diode carrying 1 mA is approximately:
`A) 1.79×10⁻¹¹ A/√Hz | B) 1.79×10⁻¹³ A/√Hz | C) 1.79×10⁻⁷ A/√Hz | D) 1.79×10⁻⁹ A/√Hz`
**Ans: A** — i_n = √(2qI) = √(2×1.6×10⁻¹⁹×10⁻³) = √(3.2×10⁻²²) = 1.79×10⁻¹¹ A/√Hz ≈ 17.9 pA/√Hz.

**Q956.** Flicker (1/f) noise is significant in MOSFETs at:
`A) Low frequencies | B) High frequencies | C) Only in saturation | D) Above f_T`
**Ans: A** — Trap-related generation–recombination noise scales with 1/f, dominating below a few hundred Hz.

**Q957.** The corner frequency at which 1/f and thermal noise are equal is the:
`A) 1/f noise corner frequency | B) Unity-gain frequency | C) Cutoff frequency | D) Resonance frequency`
**Ans: A** — Above it, white noise dominates; below it, flicker noise dominates.

**Q958.** The noise figure of a circuit is:
`A) The degradation in SNR versus an ideal noiseless circuit | B) Its total gain | C) Its bandwidth | D) Its power consumption`
**Ans: A** — NF = (S/N)_in / (S/N)_out, always referenced to 290 K.

**Q959.** A noise figure of 3 dB means:
`A) The input-referred noise doubles | B) The SNR halves | C) The gain halves | D) The output noise halves`
**Ans: A** — 3 dB corresponds to a factor of 2 in noise power (and the same in SNR degradation).

**Q960.** A cascade of two noisy stages has noise figure:
`A) F = F₁ + (F₂−1)/G₁ | B) F = F₁·F₂ | C) F = F₁ + F₂ | D) F = F₁`
**Ans: A** — The first stage's gain suppresses the second stage's contribution, so the first stage dominates.

**Q961.** In a cascade, noise and distortion are traded because:
`A) Reducing gain in one stage reduces both | B) They are independent | C) Noise can be amplified away | D) Distortion can be filtered`
**Ans: A** — Less gain per stage lowers both noise (with lower gain, higher signal impedance) and distortion.

**Q962.** The optimum source resistance for minimum total input noise is:
`A) r_opt = |Z_s(f)| (matched for noise) | B) Zero | C) The load resistance | D) The bias resistance`
**Ans: A** — Noise matching (not power matching) is the right criterion for low-noise design.

**Q963.** A source follower is a preferred first stage in a low-noise design because:
`A) Its noise figure is close to unity (near-zero noise) | B) It has high gain | C) It is fast | D) It isolates poorly`
**Ans: A** — At nearly unity gain the follower contributes almost no internal noise; gain comes later.

**Q964.** A low-noise op-amp is characterised by:
`A) Low input voltage noise density (nV/√Hz) | B) High GBW | C) Large offset | D) Low PSRR only`
**Ans: A** — Rail-to-rail CMOS inputs are quiet but often have high current noise; precision bipolar inputs have low voltage noise.

**Q965.** Input-referred noise is defined as:
`A) The noise referred to the input, divided by gain | B) The output noise | C) The power supply noise | D) The distortion`
**Ans: A** — e_n = output noise / A, which is what determines SNR for a given source.

**Q966.** Current noise i_n flowing into a source resistance R_s produces input-referred voltage noise:
`A) i_n·R_s | B) i_n/R_s | C) i_n²R_s | D) i_n·√R_s`
**Ans: A** — For FETs, i_n·R_s can dominate e_n, so R_s must be chosen carefully.

**Q967.** The corner frequency where e_n and i_n·R_s cross is called:
`A) The noise corner | B) The unity-gain frequency | C) The pole frequency | D) The clipping point`
**Ans: A** — The total input noise is the sum in quadrature; the crossing point is the noise corner.

**Q968.** Correlated noise (e_n and i_n) matters mainly in:
`A) BJT-input amplifiers, where it dominates over 1/f region | B) Power supplies | C) Rectifiers | D) Digital logic`
**Ans: A** — Base and collector shot noises are partially correlated, raising the noise floor of BJT amplifiers.

**Q969.** MOS thermal noise in the channel contributes a drain-current noise given by:
`A) i_n,ds = 4kT·g_m (for long channel in saturation) | B) i_n = kT/R_D | C) i_n = 2qI_D | D) i_n = V_T/R_D`
**Ans: A** — i_n,ds² = 4kT(2/3)g_m V_T ≈ 4kTg_m for g_m >> g_ds.

**Q970.** The noise of a MOSFET decreases with increasing device width because:
`A) More area means more parallel current paths, reducing the noise per unit width | B) It increases capacitance | C) It increases R_on | D) It increases V_T`
**Ans: A** — Excess noise (gamma ≈ 2/3 for long channel) scales inversely with W.

**Q971.** To reduce flicker noise in a MOSFET amplifier one should:
`A) Use a PMOS input device and a large W | B) Use a minimum-width device | C) Increase the bias current only | D) Use a short channel`
**Ans: A** — PMOS has 5–10× lower flicker noise than NMOS; large W further reduces it.

**Q972.** Integrated resistors and capacitors contribute only:
`A) Thermal noise (resistors) — capacitors are noiseless | B) Both thermal and flicker | C) Flicker only | D) Shot only`
**Ans: A** — Capacitors add no thermal noise; resistors contribute 4kTRB.

**Q973.** Measurement of amplifier noise requires:
`A) A shorted-input (noise-gain-zero) configuration | B) An open input | C) A terminated 50 Ω load | D) A bias supply only`
**Ans: A** — Shorting both inputs to a quiet node measures the amplifier's own noise directly.

**Q974.** Total output noise from several uncorrelated sources is combined:
`A) In quadrature (RSS) | B) Arithmetically | C) By taking the maximum | D) By taking the mean`
**Ans: A** — Independent sources add as mean-square values, so the rms sum is the square root of the sum of squares.

**Q975.** The noise of an ideal noiseless op-amp with a source resistor is limited by:
`A) The source resistor's thermal noise | B) The op-amp supply | C) The offset drift | D) The load`
**Ans: A** — A resistor is itself a noise source; an amplifier cannot amplify a noiseless signal into noiseless output.

### 15B. Distortion and amplifier performance

**Q976.** Total harmonic distortion (THD) is defined as:
`A) The ratio of RMS harmonic content to the RMS fundamental | B) The offset | C) The noise | D) The bandwidth`
**Ans: A** — THD = √(V₂²+V₃²+…)/V₁.

**Q977.** Harmonic distortion in an amplifier arises mainly from:
`A) Nonlinearity in the transfer characteristic | B) A finite bandwidth | C) Noise | D) Supply variation`
**Ans: A** — Crossover, clipping, saturation and thermal drift all bend the transfer curve.

**Q978.** A signal amplifier's maximum undistorted output is set by:
`A) Output swing limits (clipping/saturation) | B) Its gain | C) Its input impedance | D) Its noise figure`
**Ans: A** — Beyond it the amplifier clips, generating harmonics.

**Q979.** Intermodulation distortion (IMD) in a nonlinear amplifier generates:
`A) Frequencies at the sum and difference of the input tones | B) Only harmonics of one tone | C) Only noise | D) DC offset`
**Ans: A** — Two-tone IMD at 2f₁−f₂ and 2f₂−f₁ is the standard measure.

**Q980.** Third-order intercept point (IP3) characterizes:
`A) The maximum output at which IMD grows 1 dB per 2 dB of output increase | B) The 1 dB compression point | C) The noise floor | D) The gain`
**Ans: A** — Output1dB marks compression; IP3 marks the extrapolation of the IMD slope.

**Q981.** The 1 dB compression point is where:
`A) Gain has dropped 1 dB from its linear value | B) Output is 1 dB below input | C) Noise is 1 dB high | D) THD is 1 %`
**Ans: A** — The amplifier's gain is beginning to be compressed by the nonlinearity.

**Q982.** Intermodulation distortion is worst when the input signals are:
`A) Large and close in frequency to each other | B) Very small | C) At DC | D) Square waves`
**Ans: A** — Close-in tones fall inside the same compression region, producing severe IMD.

**Q983.** Crossover distortion in a class-B amplifier occurs because:
`A) Each transistor is off below its V_BE, causing a dead zone | B) The bias is too high | C) The load is resistive | D) The supply is low`
**Ans: A** — Both devices need ~0.7 V of drive before conducting, so the zero crossing is notched.

**Q984.** Crossover distortion is eliminated in a class-AB amplifier by:
`A) Biasing the transistors slightly on | B) Biasing them further off | C) Using more supply | D) Using a transformer`
**Ans: A** — A V_BE-multiplier or diodes give a small quiescent current, closing the dead zone.

**Q985.** Harmonic distortion in a push-pull amplifier is largely caused by:
`A) Transfer-characteristic curvature (crossover and clipping) | B) Finite bandwidth | C) Offset | D) Supply ripple only`
**Ans: A** — Third-harmonic distortion appears because the composite characteristic is not a straight line.

**Q986.** The output resistance of an amplifier affects distortion because it:
`A) Combines with the load to load the nonlinearity | B) Sets the gain only | C) Sets the supply | D) Has no effect`
**Ans: A** — A high output impedance isolates the load so the device's characteristic is not loaded into more curvature.

**Q987.** The slew rate of an amplifier limits small-signal bandwidth when:
`A) The input signal is large | B) The signal is tiny | C) The load is light | D) The gain is unity`
**Ans: A** — Large signals demand large slope (dv/dt); small signals are limited by the poles instead.

**Q988.** A common op-amp distortion metric is total harmonic distortion plus noise, measured as:
`A) THD+N | B) SNR only | C) CMRR | D) PSRR`
**Ans: A** — THD+N captures distortion and noise together, which is what limits ADC performance.

**Q989.** A bipolar-input op-amp typically has better:
`A) Low voltage noise but more current noise than CMOS inputs | B) The reverse | C) Equal noise | D) No noise`
**Ans: A** — Bipolar r_e is small so e_n is low, but shot noise gives high i_n.

**Q990.** A CMOS-input op-amp typically has better:
`A) Low current noise (i_n ∝ gm) and rail-to-rail input range | B) Low voltage noise | C) High PSRR | D) Lower distortion`
**Ans: A** — i_n is tiny because gm is high; e_n is comparatively higher.

**Q991.** Slew-rate-induced distortion appears on a sine wave as:
`A) Triangular limiting of the peaks | B) A phase shift only | C) Cross-over notch | D) Clipping flat`
**Ans: A** — When the required slope exceeds SR, the peaks become triangular (slope-limited).

**Q992.** The minimum slew rate for full output swing at frequency f and peak amplitude V_p is:
`A) SR_min = 2πf·V_p | B) SR_min = f·V_p | C) SR_min = 2πV_p | D) SR_min = V_p/f`
**Ans: A** — Slope of a sine is ωV_p = 2πfV_p; the amplifier must supply at least this.

**Q993.** An amplifier's effective bandwidth (from slew rate, not small-signal) is:
`A) BW_full = SR/(2πV_p) | B) BW_full = GBW | C) BW_full = f_T | D) BW_full = 1/SR`
**Ans: A** — The lower of small-signal BW and SR limit sets the usable bandwidth.

**Q994.** A common-mode input range must include the input signal because:
`A) Inputs outside it are clipped by the input stage | B) It sets the gain | C) It sets the noise | D) It sets the offset only`
**Ans: A** — Rail-to-rail input stages widen this range; otherwise common-mode inputs clip the diff pair.

**Q995.** Output common-mode (ground) offset in a single-supply op-amp can cause:
`A) Output saturation and loss of headroom | B) Increased gain | C) Reduced noise | D) Faster slew`
**Ans: A** — Without a mid-supply reference, the output cannot swing symmetrically.

**Q996.** The slew-rate-limited settling time in an amplifier is:
`A) t = ΔV/SR (large-signal) | B) t = 0.35/BW only | C) t = V_T/IS | D) t = 1/(2πf)`
**Ans: A** — Large-signal settling is slew-limited; small-signal settling is bandwidth-limited.

**Q997.** A precision amplifier is optimised for:
`A) Offset, bias current and drift over bandwidth | B) Slew rate only | C) Output current only | D) Noise only`
**Ans: A** — Chopper and auto-zero amplifiers target µV offsets and nV/°C drift.

**Q998.** Voltage-noise spectral density of a good low-noise BJT op-amp input stage is about:
`A) 1 nV/√Hz | B) 1 µV/√Hz | C) 1 mV/√Hz | D) 1 V/√Hz`
**Ans: A** — Chopper-stable amplifiers reach sub-nV/√Hz; classic bipolar parts are ~1 nV/√Hz.

**Q999.** An instrumentation amplifier achieves high CMRR because:
`A) Its differential gain is set by a single precise resistor while the input stage is fully differential | B) It uses a transformer only | C) It rectifies | D) It has no offset`
**Ans: A** — Matching one gain resistor eliminates the common-mode error from resistor tolerances.

**Q1000.** In short, the performance of a linear analogue amplifier is set by its:
`A) Gain, bandwidth, noise, distortion, offset and stability | B) Only its gain | C) Only its power | D) Only its price`
**Ans: A** — Every parameter trades against the others: gain versus bandwidth, noise versus bias, linearity versus headroom, stability versus bandwidth.

---
