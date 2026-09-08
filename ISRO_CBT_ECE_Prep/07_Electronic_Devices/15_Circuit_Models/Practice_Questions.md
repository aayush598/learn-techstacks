# Circuit Models - Practice Questions (ISRO Style)

## Q1. h-parameter Definition
**The h-parameter hfe (forward current gain) is defined as:**

(a) V1/I1 with V2 = 0
(b) I2/I1 with V2 = 0
(c) V1/I1 with I1 = 0
(d) I2/I1 with V2 = 0

**Answer: (b)**
**Explanation:** h21 = I2/I1 with V2=0 (short-circuit output). For BJT: hfe = β.

---

## Q2. hie Value
**The h-parameter hie of a CE BJT amplifier typically is:**

(a) 10-100 Ω
(b) 1-10 kΩ
(c) 100 kΩ
(d) 1 MΩ

**Answer: (b)**
**Explanation:** hie = input impedance = rπ ≈ βVT/IC. Typically 1-10 kΩ.

---

## Q3. DC Equivalent
**In DC analysis of an amplifier, capacitors are treated as:**

(a) Short circuit
(b) Open circuit
(c) 1 Ω resistors
(d) Voltage sources

**Answer: (b)**
**Explanation:** At DC, capacitor impedance → ∞ (open circuit). Inductors → short.

---

## Q4. AC Equivalent
**In AC small-signal analysis, DC voltage sources are:**

(a) Kept as is
(b) Replaced by short circuit to ground
(c) Replaced by open circuit
(d) Multiplied by gain

**Answer: (b)**
**Explanation:** DC sources grounded (AC voltage 0). Capacitors shorted.

---

## Q5. DC Model BJT
**In the DC model of a forward-active BJT:**

(a) VBE = 0.7V, IC unknown
(b) VBE = 0.7V, IC = βIB
(c) VBE = 0.2V
(d) VCE = 0.7V

**Answer: (b)**
**Explanation:** Active mode: VBE ≈ 0.7V (Si), IC = βIB. VCE(sat) = 0.2V is saturation.

---

## Q6. z-parameters
**z-parameters are measured with:**

(a) Input/output short-circuited
(b) Input/output open-circuited
(c) Load connected
(d) Source connected

**Answer: (b)**
**Explanation:** z-parameters (open-circuit impedance): measured with I1=0 or I2=0 (open circuits).

---

## Q7. y-parameters
**y-parameters are measured with:**

(a) Open circuits
(b) Short circuits
(c) Matched loads
(d) No source

**Answer: (b)**
**Explanation:** y-parameters (short-circuit admittance): measured with V1=0 or V2=0 (short circuits).

---

## Q8. CE Voltage Gain
**The voltage gain of CE amplifier with β = 100, RL = 2 kΩ, rπ = 2 kΩ is:**

(a) +100
(b) -100
(c) +200
(d) -50

**Answer: (b)**
**Explanation:** Av = -βRL/rπ = -100×2000/2000 = -100

---

## Q9. CB Input Impedance
**The input impedance of a common base amplifier is:**

(a) rπ
(b) re (very low)
(c) ro
(d) βre

**Answer: (b)**
**Explanation:** CB input impedance = re = VT/IE. Very low (tens of ohms).

---

## Q10. Emitter Follower
**The emitter follower (CC) has:**

(a) High input, low output impedance
(b) Low input, high output impedance
(c) High gain
(d) Inverting output

**Answer: (a)**
**Explanation:** CC: high input (rπ + (1+β)RE), low output (re). Gain ≈ 1. Non-inverting.

---

## Q11. h to gm
**The relation between hfe and gm for BJT is:**

(a) gm = hfe/rπ
(b) gm = rπ/hfe
(c) gm = hfe × rπ
(d) gm = 1/(hfe·rπ)

**Answer: (a)**
**Explanation:** hfe = β = gm×rπ, so gm = hfe/rπ.

---

## Q12. MOSFET DC Model
**In the saturation region, the MOSFET DC drain current is:**

(a) ID = kn(W/L)VDS
(b) ID = (1/2)kn(W/L)(VGS-VT)²
(c) ID = kn(W/L)VGS
(d) ID = VT×VGS

**Answer: (b)**
**Explanation:** ID = (1/2)kn'(W/L)(VGS-VT)² in saturation.

---

## Q13. ABCD Parameters
**ABCD (transmission) parameters relate:**

(a) V1,I1 to V2,I2
(b) V1,I1 to V2,-I2
(c) V1,V2 to I1,I2
(d) I1,I2 to V1,V2

**Answer: (b)**
**Explanation:** |V1; I1| = |A B; C D| × |V2; -I2|. Used for cascaded networks.

---

## Q14. Hybrid Model Usage
**h-parameters are preferred for BJT because:**

(a) Easy to measure
(b) Good for low-frequency
(c) Datasheets provide them
(d) All of the above

**Answer: (d)**
**Explanation:** h-parameters are easy to measure, practical at low frequency, provided by datasheets.

---

## Q15. Output Impedance CE
**The output impedance of CE amplifier with RC = 5 kΩ and ro = 100 kΩ is:**

(a) 5 kΩ
(b) 4.76 kΩ
(c) 100 kΩ
(d) 105 kΩ

**Answer: (b)**
**Explanation:** Rout = RC||ro = 5k||100k = (5×100)/(105) = 4.76 kΩ

---

## Q16. Current Gain CC
**The current gain of common collector amplifier hfc is:**

(a) -1
(b) -(1+β)
(c) α
(d) β

**Answer: (b)**
**Explanation:** For CC: hfc = -(1+β). Emitter current is (1+β) times base current.

---

## Q17. Cascaded Amplifier
**The total voltage gain of two identical CE stages each with gain -50 is:**

(a) -100
(b) 2500
(c) -2500
(d) 100

**Answer: (b)**
**Explanation:** Av = Av1 × Av2 = (-50)×(-50) = +2500. Note positive (double inversion).

---

## Q18. DC to AC Transition
**For AC analysis, an ideal capacitor at signal frequency is:**

(a) Open circuit
(b) Short circuit
(c) 1 Ω
(d) Infinite

**Answer: (b)**
**Explanation:** At signal frequency, large coupling capacitors have low impedance → short circuit.

---

## Q19. Two-Port Ports
**In two-port network, IF and |A| for ABCD matrix are:**

(a) |A| = 1
(b) |A| = AD - BC = 1
(c) |A| = 0
(d) |A| = 2

**Answer: (b)**
**Explanation:** For reciprocal passive networks: AD - BC = 1 (determinant condition).

---

## Q20. Voltage Gain with Ohms Law h-model
**Using h-model, CE Av with RL and hre=hoe=0 is:**

(a) -hfe·RL/hie
(b) hfe·RL/hie
(c) -hie/(hfe·RL)
(d) hie·RL/hfe

**Answer: (a)**
**Explanation:** Av = -hfeRL/hie (ignoring hre, hoe). Standard CE approximation.

---

## Q21. DC MOSFET
**In DC analysis of a MOSFET, the gate current is:**

(a) βIB
(b) 0 (ideal)
(c) VG/RS
(d) ID/2

**Answer: (b)**
**Explanation:** MOSFET gate is insulated → gate DC current = 0 (ideal).

---

## Q22. Saturation Voltage
**VCE(sat) for a silicon BJT is:**

(a) 0.7V
(b) 0.2V
(c) 1.2V
(d) 0.1V

**Answer: (b)**
**Explanation:** VCE(sat) ≈ 0.2V for Si BJT in saturation.

---

## Q23. Input Impedance
**The input impedance of CC amplifier is:**

(a) Low
(b) High
(c) Zero
(d) Infinite

**Answer: (b)**
**Explanation:** Rin = RB||(rπ + (1+β)RE). High input impedance makes CC a good buffer.

---

## Q24. Model Frequency Limit
**h-parameter model is most accurate at:**

(a) Very high frequencies
(b) Low frequencies
(c) All frequencies
(d) DC only

**Answer: (b)**
**Explanation:** h-parameters ignore capacitances → accurate at low frequency only. Hybrid-π for high freq.

---

## Q25. Output Resistance CB
**The output resistance of a common base amplifier equals:**

(a) rπ
(b) re
(c) RC || ro
(d) βre

**Answer: (c)**
**Explanation:** Rout = RC || ro (like CE). CB has high output impedance.
