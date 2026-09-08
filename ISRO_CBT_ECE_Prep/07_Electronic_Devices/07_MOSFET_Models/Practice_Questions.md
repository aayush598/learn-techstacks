# MOSFET Models - Practice Questions (ISRO Style)

## Q1. gm Calculation
**A MOSFET has ID = 1 mA and VGS - VT = 0.5V. The transconductance gm is:**

(a) 1 mS
(b) 2 mS
(c) 4 mS
(d) 10 mS

**Answer: (c)**
**Explanation:** gm = 2ID/Vov = 2 × 1 mA/0.5V = 4 mS

---

## Q2. Output Resistance
**A MOSFET with λ = 0.05 V⁻¹ and ID = 2 mA has output resistance ro of:**

(a) 10 kΩ
(b) 25 kΩ
(c) 50 kΩ
(d) 100 kΩ

**Answer: (a)**
**Explanation:** ro = 1/(λID) = 1/(0.05 × 2×10⁻³) = 1/(10⁻⁴) = 10 kΩ

---

## Q3. Intrinsic Gain
**The intrinsic gain gmro of a MOSFET with VA = 50V and Vov = 0.5V is:**

(a) 50
(b) 100
(c) 200
(d) 400

**Answer: (c)**
**Explanation:** gmro = 2VA/Vov = 2 × 50/0.5 = 200

---

## Q4. Hybrid-π Model
**In the hybrid-π model, the output resistance ro is connected between:**

(a) Gate and Source
(b) Gate and Drain
(c) Drain and Source
(d) Source and Body

**Answer: (c)**
**Explanation:** ro represents channel length modulation effect, connected between drain and source.

---

## Q5. Body Transconductance
**The body transconductance gmb is typically:**

(a) Equal to gm
(b) 0.1-0.3 times gm
(c) 10 times gm
(d) Zero

**Answer: (b)**
**Explanation:** gmb = ηgm where η ≈ 0.1-0.3. Body effect is usually smaller than gate effect.

---

## Q6. Cgs in Saturation
**In saturation, the gate-source capacitance Cgs is approximately:**

(a) WLCox
(b) (2/3)WLCox
(c) (1/2)WLCox
(d) (1/3)WLCox

**Answer: (b)**
**Explanation:** In saturation: Cgs = (2/3)WLCox, Cgd ≈ 0 (ideal).

---

## Q7. gm and ID Relationship
**If the drain current of a MOSFET is increased by 4 times, gm:**

(a) Increases by 2 times
(b) Increases by 4 times
(c) Increases by 16 times
(d) Doubles

**Answer: (a)**
**Explanation:** gm ∝ √ID. If ID increases 4×, gm increases √4 = 2 times.

---

## Q8. T-Model Usage
**The T-model is particularly useful for analyzing:**

(a) Common-source amplifiers
(b) Common-gate amplifiers
(c) Common-drain amplifiers
(d) Differential pairs

**Answer: (b)**
**Explanation:** T-model provides simpler analysis for common-gate configuration.

---

## Q9. fT Formula
**The unity current gain frequency fT of a MOSFET is given by:**

(a) gm/(2πCgs)
(b) gm/(2π(Cgs + Cgd))
(c) 1/(2πgmCgs)
(d) gm/(2πCgd)

**Answer: (b)**
**Explanation:** fT = gm/(2π(Cgs + Cgd)). This is where current gain drops to 1.

---

## Q10. Large Signal vs Small Signal
**The large-signal model is used for:**

(a) AC analysis only
(b) DC bias point calculation
(c) Noise analysis
(d) Frequency response

**Answer: (b)**
**Explanation:** Large-signal model represents DC and large AC behavior, used for bias point.

---

## Q11. gm/ID Ratio
**The gm/ID ratio of a MOSFET is:**

(a) Constant
(b) Inversely proportional to Vov
(c) Proportional to ID
(d) Proportional to W/L

**Answer: (b)**
**Explanation:** gm/ID = 2/Vov. As Vov increases, gm/ID decreases.

---

## Q12. Noise Model
**The thermal noise current of a MOSFET is proportional to:**

(a) ID
(b) √ID
(c) gm
(d) gm²

**Answer: (c)**
**Explanation:** i²nd = 4kTγgmB. Thermal noise proportional to gm.

---

## Q13. Cgd Miller Effect
**The Miller effect on Cgd:**

(a) Increases input capacitance
(b) Decreases input capacitance
(c) Increases output capacitance
(d) Has no effect

**Answer: (a)**
**Explanation:** Miller effect multiplies Cgd by (1 + |Av|) at input, increasing effective input capacitance.

---

## Q14. Channel Length Modulation
**Channel length modulation effect:**

(a) Increases output resistance
(b) Decreases output resistance
(c) No effect on output resistance
(d) Only affects gm

**Answer: (b)**
**Explanation:** Channel length modulation makes output resistance finite (decreases from infinity).

---

## Q15. gm and W/L
**If W/L ratio of a MOSFET is doubled, gm:**

(a) Doubles
(b) Quadruples
(c) Increases by √2 times
(d) No change

**Answer: (a)**
**Explanation:** gm = μnCox(W/L)(VGS-VT) ∝ (W/L). Doubling W/L doubles gm.

---

## Q16. Source Follower
**A source follower (common drain) has:**

(a) High input, high output impedance
(b) High input, low output impedance
(c) Low input, high output impedance
(d) Low input, low output impedance

**Answer: (b)**
**Explanation:** Source follower: high input impedance (gate), low output impedance (source).

---

## Q17. Frequency Response
**The gain of a MOSFET amplifier decreases with frequency due to:**

(a) gm decrease
(b) Capacitance effects
(c) ro increase
(d) Body effect

**Answer: (b)**
**Explanation:** Internal capacitances (Cgs, Cgd) cause gain to roll off at high frequencies.

---

## Q18. Voltage Gain
**The voltage gain of a common-source amplifier with load RD is:**

(a) gmRD
(b) -gmRD
(c) gm/(RD||ro)
(d) -gm(RD||ro)

**Answer: (d)**
**Explanation:** Av = -gm(RD||ro||RL). Negative sign indicates 180° phase shift.

---

## Q19. Input Impedance
**The input impedance of a MOSFET amplifier at low frequency is:**

(a) 1/gm
(b) ro
(c) Infinite (ideal)
(d) RD

**Answer: (c)**
**Explanation:** MOSFET gate is insulated → infinite input impedance at low frequency.

---

## Q20. Flicker Noise
**Flicker noise (1/f noise) in MOSFET:**

(a) Dominates at high frequencies
(b) Dominates at low frequencies
(c) Is constant with frequency
(d) Only affects PMOS

**Answer: (b)**
**Explanation:** Flicker noise power ∝ 1/f, dominates at low frequencies. Important in analog circuits.

---

## Q21. Output Impedance
**The output impedance of a common-source amplifier with current source load is:**

(a) 1/gm
(b) ro
(c) RD
(d) Infinite

**Answer: (b)**
**Explanation:** Current source load has high impedance → output impedance ≈ ro.

---

## Q22. gm and Temperature
**The transconductance gm of a MOSFET:**

(a) Increases with temperature
(b) Decreases with temperature
(c) Is independent of temperature
(d) First increases then decreases

**Answer: (b)**
**Explanation:** gm ∝ μn, and μn decreases with temperature (∝ T⁻³/²). So gm decreases.

---

## Q23. Current Gain
**The current gain of a MOSFET amplifier at low frequency is:**

(a) gm
(b) ro
(c) Infinite (ideal)
(d) W/L

**Answer: (c)**
**Explanation:** Gate current is zero → current gain = ID/IG = ∞ (ideal).

---

## Q24. Power Gain
**Power gain of a MOSFET amplifier is the product of:**

(a) Voltage gain and current gain
(b) Voltage gain squared
(c) Current gain squared
(d) gm and ro

**Answer: (a)**
**Explanation:** Power gain = |Av| × |Ai|. For MOSFET: Ai ≈ ∞, so power gain ≈ ∞ (ideal).

---

## Q25. Model Selection
**For analyzing a common-source amplifier, the preferred small-signal model is:**

(a) T-model
(b) Hybrid-π model
(c) Pi-model only
(d) Any model works

**Answer: (b)**
**Explanation:** Hybrid-π is most common for common-source analysis. T-model is better for common-gate.
