# Small Signal Models - Practice Questions (ISRO Style)

## Q1. BJT Transconductance
**A BJT has IC = 5 mA at 300K. Its transconductance gm is:**

(a) 25 mS
(b) 40 mS
(c) 100 mS
(d) 200 mS

**Answer: (d)**
**Explanation:** gm = IC/VT = 5 mA/25.85 mV = 193 mS ≈ 200 mS

---

## Q2. r-pi Calculation
**A BJT with β = 100 and IC = 1 mA has input resistance rπ of:**

(a) 100 Ω
(b) 1 kΩ
(c) 2.6 kΩ
(d) 26 kΩ

**Answer: (c)**
**Explanation:** rπ = β/gm = 100/(1mA/26mV) = 100/0.0385 = 2600 Ω = 2.6 kΩ

---

## Q3. MOSFET Transconductance
**A MOSFET has ID = 1 mA and Vov = 0.5V. Its gm is:**

(a) 1 mS
(b) 2 mS
(c) 4 mS
(d) 10 mS

**Answer: (c)**
**Explanation:** gm = 2ID/Vov = 2 × 1mA/0.5V = 4 mS

---

## Q4. Common Emitter Gain
**The voltage gain of a CE amplifier with gm = 40 mS and Rc||ro = 2 kΩ is:**

(a) +80
(b) -80
(c) +20
(d) -20

**Answer: (b)**
**Explanation:** Av = -gm(RC||ro) = -40m × 2k = -80. Negative sign shows inversion.

---

## Q5. Miller Effect
**For a CE amplifier with gain -100 and Cμ = 5 pF, the Miller input capacitance is:**

(a) 5 pF
(b) 100 pF
(c) 500 pF
(d) 505 pF

**Answer: (d)**
**Explanation:** Cin = Cμ(1+|Av|) = 5(1+100) = 505 pF

---

## Q6. Output Resistance BJT
**A BJT with VA = 100V and IC = 2 mA has output resistance ro of:**

(a) 50 kΩ
(b) 100 kΩ
(c) 200 kΩ
(d) 500 kΩ

**Answer: (a)**
**Explanation:** ro = VA/IC = 100/2mA = 50 kΩ

---

## Q7. MOSFET Output Resistance
**A MOSFET with λ = 0.02 V⁻¹ and ID = 1 mA has ro of:**

(a) 20 kΩ
(b) 50 kΩ
(c) 100 kΩ
(d) 200 kΩ

**Answer: (b)**
**Explanation:** ro = 1/(λID) = 1/(0.02 × 1m) = 1/(2×10⁻⁵) = 50 kΩ

---

## Q8. h-parameters
**The relation between h-parameters and hybrid-π model: hie equals:**

(a) re
(b) rπ
(c) ro
(d) gm

**Answer: (b)**
**Explanation:** hie = rπ = input resistance. Also hfe = β, hoe = 1/ro.

---

## Q9. Emitter Follower Gain
**The voltage gain of an ideal emitter follower (common collector) is:**

(a) -gmRC
(b) gmRC
(c) 1
(d) 0

**Answer: (c)**
**Explanation:** CC amplifier has Av ≈ 1 (voltage follower). Output follows input.

---

## Q10. gm/ID Ratio
**The gm/ID ratio for a MOSFET with Vov = 0.2V is:**

(a) 5 V⁻¹
(b) 10 V⁻¹
(c) 20 V⁻¹
(d) 50 V⁻¹

**Answer: (b)**
**Explanation:** gm/ID = 2/Vov = 2/0.2 = 10 V⁻¹

---

## Q11. Body Transconductance
**If gm = 5 mS and η = 0.2, the body transconductance gmb is:**

(a) 0.5 mS
(b) 1 mS
(c) 2 mS
(d) 5 mS

**Answer: (b)**
**Explanation:** gmb = ηgm = 0.2 × 5 = 1 mS

---

## Q12. Common Base Input
**The input resistance of a common base amplifier is:**

(a) rπ
(b) re
(c) ro
(d) βre

**Answer: (b)**
**Explanation:** Rin = re = VT/IE. Typically very low (few ohms to tens of ohms).

---

## Q13. Source Follower Output
**The output resistance of a source follower (common drain) is:**

(a) ro
(b) 1/gm
(c) RD
(d) RG

**Answer: (b)**
**Explanation:** Rout = 1/gm || RS. For ideal: 1/gm (very low).

---

## Q14. fT of BJT
**A BJT with gm = 100 mS and Cπ + Cμ = 100 pF has fT of:**

(a) 100 MHz
(b) 159 MHz
(c) 200 MHz
(d) 1 GHz

**Answer: (b)**
**Explanation:** fT = gm/(2πC) = 0.1/(2π×100×10⁻¹²) = 0.1/6.28×10⁻¹⁰ = 1.59×10⁸ = 159 MHz

---

## Q15. Input Resistance CS
**The input resistance of a common source amplifier is:**

(a) 1/gm
(b) rπ
(c) RG (very high)
(d) RD

**Answer: (c)**
**Explanation:** MOSFET gate is insulated → RG very high (MΩ to GΩ).

---

## Q16. Transconductance-Amplifier Gain
**For a BJT with IC = 1 mA, gm is:**

(a) 26 mS
(b) 40 mS
(c) 1 mS
(d) 100 mS

**Answer: (b)**
**Explanation:** gm = 40 × IC (mA) = 40 × 1 = 40 mS (using VT = 25 mV approximation)

---

## Q17. Output Resistance Effect
**The gain of a CS amplifier with RD = 10 kΩ and ro = 100 kΩ is:**

(a) -gm×10k
(b) -gm×9.1k
(c) -gm×100k
(d) -gm×110k

**Answer: (b)**
**Explanation:** RD||ro = 10k||100k = (10×100)/(10+100) = 1000/110 = 9.09 kΩ ≈ 9.1k

---

## Q18. Load Resistance Gain
**The gain of CS amplifier decreases when RL is reduced because:**

(a) gm decreases
(b) RD||RL||ro decreases
(c) ro decreases
(d) Vov increases

**Answer: (b)**
**Explanation:** Av = -gm(RD||RL||ro). Lower RL → lower parallel combination → lower gain.

---

## Q19. re Relation
**The emitter resistance re relates to gm by:**

(a) re = βgm
(b) re = α/gm
(c) re = gm/α
(d) re = 1/(βgm)

**Answer: (b)**
**Explanation:** re = VT/IE = αVT/IC = α/gm

---

## Q20. Low Frequency Response
**The low-frequency cutoff of an amplifier is set by:**

(a) gm
(b) Coupling/bypass capacitors
(c) Internal capacitances
(d) Load resistance

**Answer: (b)**
**Explanation:** Coupling and bypass capacitors determine lower cutoff frequency. Internal caps set high-frequency.

---

## Q21. Current Gain
**The current gain (Ai) of a common base amplifier is:**

(a) β
(b) α ≈ 1
(c) 1+β
(d) β²

**Answer: (b)**
**Explanation:** Ai = α ≈ 1 for CB. Current essentially passes from emitter to collector.

---

## Q22. Av with Degeneration
**Adding emitter resistance RE to a CE amplifier:**

(a) Increases gain
(b) Decreases gain
(c) No effect
(d) Doubles gain

**Answer: (b)**
**Explanation:** Av = -RC/(re + RE). RE reduces gain but improves stability and linearity.

---

## Q23. High-Frequency Pole
**The dominant high-frequency pole of CS amplifier is determined by:**

(a) Cgs at input
(b) Cgd with Miller
(c) Cgb
(d) Cds

**Answer: (b)**
**Explanation:** Miller-multiplied Cgd at input dominates high-frequency pole.

---

## Q24. Small-Signal Limits
**Small-signal approximation for BJT is valid when:**

(a) vbe < VT
(b) vbe >> VT
(c) vbe = VT
(d) Always

**Answer: (a)**
**Explanation:** Small-signal valid when vbe << VT (26 mV). Then exponential can be linearized.

---

## Q25. Back-Gate Effect
**The back-gate transconductance gmb in MOSFET represents:**

(a) Effect of VDS on ID
(b) Effect of VSB on ID
(c) Effect of VGS on ID
(d) Effect of VDD on ID

**Answer: (b)**
**Explanation:** gmb = ∂ID/∂VSB. Represents body effect: source-body voltage influence on drain current.
