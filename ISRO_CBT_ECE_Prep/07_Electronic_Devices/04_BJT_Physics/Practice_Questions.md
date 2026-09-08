# BJT Physics - Practice Questions (ISRO Style)

## Q1. Alpha-Beta Conversion
**A BJT has α = 0.98. The value of β is:**

(a) 49
(b) 50
(c) 98
(d) 100

**Answer: (a)**
**Explanation:** β = α/(1-α) = 0.98/(1-0.98) = 0.98/0.02 = 49

---

## Q2. Transconductance
**A BJT operates at IC = 2 mA at 300K. Its transconductance gm is approximately:**

(a) 2 mS
(b) 20 mS
(c) 77 mS
(d) 154 mS

**Answer: (c)**
**Explanation:** gm = IC/VT = 2 mA/26 mV = 76.9 mS ≈ 77 mS

---

## Q3. Input Resistance
**A BJT with β = 100 and gm = 40 mS has input resistance rπ of:**

(a) 2.5 Ω
(b) 25 Ω
(c) 250 Ω
(d) 2500 Ω

**Answer: (d)**
**Explanation:** rπ = β/gm = 100/0.04 = 2500 Ω = 2.5 kΩ

---

## Q4. Early Effect
**The Early effect in BJT causes:**

(a) Increase in IC with VCE
(b) Decrease in IC with VCE
(c) No change in IC
(d) Decrease in β

**Answer: (a)**
**Explanation:** Early effect (base width modulation) causes IC to increase slightly with VCE. VA is typically 50-200V.

---

## Q5. Emitter Current
**A BJT has IC = 10 mA and IB = 50 μA. The emitter current is:**

(a) 9.95 mA
(b) 10 mA
(c) 10.05 mA
(d) 10.5 mA

**Answer: (c)**
**Explanation:** IE = IC + IB = 10 mA + 0.05 mA = 10.05 mA

---

## Q6. Output Resistance
**The output resistance of a BJT with VA = 100V and IC = 1 mA is:**

(a) 100 Ω
(b) 1 kΩ
(c) 10 kΩ
(d) 100 kΩ

**Answer: (d)**
**Explanation:** ro = VA/IC = 100V/1 mA = 100 kΩ

---

## Q7. Beta Temperature Coefficient
**The β of a BJT at 25°C is 100. At 75°C, β approximately becomes:**

(a) 100
(b) 115
(c) 125
(d) 150

**Answer: (c)**
**Explanation:** dβ/dT ≈ +0.5%/°C. Δβ = 100 × 0.005 × 50 = 25. β(75°C) = 100 + 25 = 125

---

## Q8. Current Components
**In a BJT in active mode, the collector current is primarily due to:**

(a) Hole diffusion
(b) Electron diffusion
(c) Drift current
(d) Recombination

**Answer: (b)**
**Explanation:** In NPN active mode, IC is due to electron diffusion from emitter to collector through thin base.

---

## Q9. Cutoff Frequency
**A BJT has fT = 500 MHz and β = 100. The β-cutoff frequency fβ is:**

(a) 5 MHz
(b) 50 MHz
(c) 500 MHz
(d) 5 GHz

**Answer: (a)**
**Explanation:** fβ = fT/β = 500 MHz/100 = 5 MHz

---

## Q10. VBE Temperature Coefficient
**The base-emitter voltage of a BJT at 25°C is 0.7V. At 50°C, VBE approximately becomes:**

(a) 0.65 V
(b) 0.7 V
(c) 0.75 V
(d) 0.8 V

**Answer: (a)**
**Explanation:** dVBE/dT ≈ -2 mV/°C. ΔVBE = -2 mV/°C × 25°C = -50 mV. VBE(50°C) = 0.7 - 0.05 = 0.65 V

---

## Q11. Ebers-Moll Model
**The Ebers-Moll model is valid in:**

(a) Active mode only
(b) Saturation mode only
(c) All operating modes
(d) Cutoff mode only

**Answer: (c)**
**Explanation:** Ebers-Moll model is a large-signal model valid in all operating regions (active, saturation, cutoff, reverse active).

---

## Q12. Injection Efficiency
**To improve emitter injection efficiency, one should:**

(a) Increase base doping
(b) Decrease emitter doping
(c) Increase emitter doping
(d) Decrease base width

**Answer: (c)**
**Explanation:** γ = 1/(1 + NDBW/NBLE). Increasing emitter doping (NE) improves injection efficiency.

---

## Q13. Base Transport Factor
**The base transport factor αT approaches unity when:**

(a) Base width is large
(b) Base width is small compared to diffusion length
(c) Collector doping is high
(d) Emitter doping is low

**Answer: (b)**
**Explanation:** αT = 1/(1 + WB²/2Ln²). When WB << Ln, αT ≈ 1.

---

## Q14. Saturation Voltage
**The collector-emitter saturation voltage VCE(sat) is typically:**

(a) 0V
(b) 0.2V
(c) 0.7V
(d) 1V

**Answer: (b)**
**Explanation:** VCE(sat) ≈ 0.2V for silicon BJTs. This is the voltage drop across collector-emitter when saturated.

---

## Q15. Small-Signal Model
**In the hybrid-π model, the capacitance Cπ represents:**

(a) Collector-base capacitance
(b) Base-emitter diffusion capacitance
(c) Stray capacitance
(d) Output capacitance

**Answer: (b)**
**Explanation:** Cπ = Cje + Cd, where Cje is junction capacitance and Cd is diffusion capacitance of base-emitter junction.

---

## Q16. Current Gain Bandwidth Product
**The current gain bandwidth product fT of a BJT is defined as:**

(a) Frequency where β = 1
(b) Frequency where α = 0.707
(c) Frequency where gain-bandwidth product is constant
(d) Maximum operating frequency

**Answer: (a)**
**Explanation:** fT is frequency where |β| = 1. It's also approximately the frequency where gain-bandwidth product becomes constant.

---

## Q17. Miller Effect
**The Miller effect in BJT amplifier:**

(a) Increases input capacitance
(b) Decreases input capacitance
(c) Increases output capacitance
(d) Has no effect on capacitance

**Answer: (a)**
**Explanation:** Miller effect multiplies Cμ by (1 + gmRL) at input, significantly increasing effective input capacitance.

---

## Q18. Thermal Runaway
**Thermal runaway in BJT occurs when:**

(a) Power dissipation increases temperature
(b) Current increases power dissipation
(c) Both (a) and (b) form positive feedback
(d) Voltage decreases

**Answer: (c)**
**Explanation:** IC↑ → PD↑ → T↑ → β↑ → IC↑ → ... This positive feedback can destroy the transistor.

---

## Q19. Diffusion Capacitance
**The diffusion capacitance of a BJT:**

(a) Increases with collector current
(b) Decreases with collector current
(c) Is independent of current
(d) Depends only on frequency

**Answer: (a)**
**Explanation:** Cd = τF·IC/VT = τF·gm. Diffusion capacitance is proportional to IC.

---

## Q20. Gummel Number
**The Gummel number GB in BJT:**

(a) Is inversely proportional to IC
(b) Is proportional to IC
(c) Is independent of doping
(d) Depends on collector voltage

**Answer: (a)**
**Explanation:** IC ∝ 1/GB. GB = ∫(NB/Dn)dx. Higher GB (more base doping/width) → lower IC.

---

## Q21. Base Width
**The base width of a modern BJT is typically:**

(a) 1-10 μm
(b) 0.1-1 μm
(c) 10-100 μm
(d) 100-1000 nm

**Answer: (b)**
**Explanation:** Modern BJTs have very thin bases (~0.1-1 μm) for high speed and high β.

---

## Q22. Noise Figure
**The minimum noise figure of a BJT occurs at:**

(a) Very low frequencies
(b) Optimum source resistance
(c) Maximum current
(d) Zero temperature

**Answer: (b)**
**Explanation:** Minimum NF occurs at optimum source resistance Ropt = √(RS² + rπ²/β) where RS is source resistance.

---

## Q23. Power Dissipation
**A BJT with VCE = 10V and IC = 100 mA dissipates:**

(a) 1 W
(b) 10 W
(c) 100 W
(d) 1000 W

**Answer: (a)**
**Explanation:** PD = VCE × IC = 10V × 0.1A = 1W

---

## Q24. Injection Efficiency Formula
**The emitter injection efficiency γ is given by:**

(a) γ = 1/(1 + NDBW/NBLE)
(b) γ = NDBW/NBLE
(c) γ = 1/(1 + NBLE/NDBW)
(d) γ = NBLE/NDBW

**Answer: (a)**
**Explanation:** γ = 1/(1 + NDBW/NBLE). To maximize γ: increase NE, decrease NB, decrease BW.

---

## Q25. Transit Time
**The base transit time τB of a BJT is proportional to:**

(a) WB
(b) WB²
(c) 1/WB
(d) 1/WB²

**Answer: (b)**
**Explanation:** τB = WB²/(2Dn). Transit time is proportional to square of base width.
