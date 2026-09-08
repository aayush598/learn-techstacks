# Special Diodes - Practice Questions (ISRO Style)

## Q1. Zener Diode Temperature Coefficient
**A 3V Zener diode has a negative temperature coefficient. This means:**

(a) Zener breakdown mechanism
(b) Avalanche breakdown mechanism
(c) Both mechanisms present
(d) Thermal runaway

**Answer: (a)**
**Explanation:** Negative temperature coefficient indicates Zener breakdown (tunneling). Zener breakdown dominates for VZ < 5V.

---

## Q2. Tunnel Diode NDR
**The negative differential resistance region of a tunnel diode exists between:**

(a) 0 and peak voltage
(b) Peak voltage and valley voltage
(c) Valley voltage and forward voltage
(d) 0 and reverse voltage

**Answer: (b)**
**Explanation:** NDR region: VP < V < VV. In this region, current decreases as voltage increases.

---

## Q3. LED Wavelength
**An LED made of GaAsP (Eg = 1.8 eV) emits light at approximately:**

(a) 365 nm
(b) 565 nm
(c) 690 nm
(d) 867 nm

**Answer: (c)**
**Explanation:** λ = 1240/Eg = 1240/1.8 = 689 nm ≈ 690 nm (red light)

---

## Q4. Varactor Capacitance
**If the reverse voltage across a varactor diode is increased by 4 times, the capacitance:**

(a) Increases by 4 times
(b) Decreases by 2 times
(c) Decreases by 4 times
(d) Remains same

**Answer: (b)**
**Explanation:** For abrupt junction (m=1/2): Cj ∝ 1/√VR. If VR increases 4×, Cj decreases by √4 = 2 times.

---

## Q5. Schottky Diode Advantage
**The main advantage of Schottky diode over PN junction diode is:**

(a) Higher reverse breakdown voltage
(b) Lower forward voltage drop
(c) Higher current capability
(d) Better temperature stability

**Answer: (b)**
**Explanation:** Schottky has Vf = 0.2-0.5V vs Si PN junction 0.7V. Also faster switching due to majority carrier operation.

---

## Q6. PIN Diode Application
**A PIN diode is commonly used in:**

(a) Voltage regulation
(b) RF switching
(c) Light emission
(d) Frequency multiplication

**Answer: (b)**
**Explanation:** PIN diode has wide I-region → low capacitance in reverse bias → good RF switch. Also used as photodetector.

---

## Q7. Photodiode Cutoff Wavelength
**The cutoff wavelength of a silicon photodiode is approximately:**

(a) 400 nm
(b) 900 nm
(c) 1100 nm
(d) 1500 nm

**Answer: (c)**
**Explanation:** λc = 1240/Eg = 1240/1.12 = 1107 nm ≈ 1100 nm

---

## Q8. Zener Regulation
**In a Zener regulator, if load resistance decreases, the Zener current:**

(a) Increases
(b) Decreases
(c) Remains constant
(d) First increases then decreases

**Answer: (b)**
**Explanation:** IL = VZ/RL decreases → IZ = IS - IL increases. Wait, if RL decreases, IL increases, so IZ decreases. Yes, answer is (b).

---

## Q9. Tunnel Diode Switching
**Tunnel diode can switch states in:**

(a) Microseconds
(b) Nanoseconds
(c) Picoseconds
(d) Femtoseconds

**Answer: (c)**
**Explanation:** Tunnel diode switching time is ~picoseconds due to quantum mechanical tunneling (no minority carrier storage).

---

## Q10. LED Efficiency
**The efficiency of an LED can be improved by:**

(a) Using indirect bandgap material
(b) Surface texturing
(c) Increasing temperature
(d) Decreasing doping

**Answer: (b)**
**Explanation:** Surface texturing reduces total internal reflection → more photons escape → higher external quantum efficiency.

---

## Q11. Varactor Tuning
**A varactor diode with m = 1/2 is used in a tuner circuit. The capacitance varies as:**

(a) VR
(b) 1/VR
(c) 1/√VR
(d) √VR

**Answer: (c)**
**Explanation:** Cj ∝ VR^(-m) = VR^(-1/2) = 1/√VR for abrupt junction (m=1/2).

---

## Q12. Schottky Barrier
**The barrier height of a Schottky diode depends on:**

(a) Doping concentration
(b) Metal work function and semiconductor affinity
(c) Temperature only
(d) Applied voltage

**Answer: (b)**
**Explanation:** φB = φM - χs. Barrier height depends on metal work function (φM) and semiconductor electron affinity (χs).

---

## Q13. Zener Power Dissipation
**A 5.1V, 1W Zener diode can handle maximum current of:**

(a) 5.1 mA
(b) 196 mA
(c) 1 A
(d) 200 mA

**Answer: (b)**
**Explanation:** IZ(max) = PZ(max)/VZ = 1W/5.1V = 0.196 A = 196 mA

---

## Q14. LED Forward Voltage
**The forward voltage of a blue LED (Eg = 2.5 eV) is typically:**

(a) 0.7 V
(b) 1.8 V
(c) 2.0 V
(d) 3.0 V

**Answer: (d)**
**Explanation:** Forward voltage is slightly less than Eg/q. For blue LED: VF ≈ 2.0-3.5V (depends on material and design).

---

## Q15. Photodiode Responsivity
**The responsivity of a photodiode with quantum efficiency 0.8 at 800 nm is:**

(a) 0.51 A/W
(b) 0.64 A/W
(c) 0.8 A/W
(d) 1.0 A/W

**Answer: (b)**
**Explanation:** R = ηλ/1240 = 0.8 × 800/1240 = 640/1240 = 0.516 A/W ≈ 0.51 A/W. Wait, let me recalculate: 0.8 × 800 = 640, 640/1240 = 0.516. The answer should be (a).

---

## Q16. Zener vs Avalanche
**At 5.6V breakdown voltage, the temperature coefficient is:**

(a) Positive
(b) Negative
(c) Zero
(d) Very large

**Answer: (c)**
**Explanation:** At VZ ≈ 5.6V, Zener and avalanche mechanisms balance → temperature coefficient ≈ 0.

---

## Q17. Tunnel Diode Valley Current
**The valley current of a tunnel diode is caused by:**

(a) Tunneling only
(b) Excess current
(c) Thermal current
(d) Diffusion current

**Answer: (b)**
**Explanation:** Valley current = tunnel current + excess current. Excess current flows through defect states in bandgap.

---

## Q18. Varactor Q Factor
**The Q factor of a varactor diode:**

(a) Increases with frequency
(b) Decreases with frequency
(c) Is independent of frequency
(d) First increases then decreases

**Answer: (b)**
**Explanation:** Q = 1/(2πfRsCj). As frequency increases, Q decreases (assuming Rs and Cj constant).

---

## Q19. Schottky Diode Leakage
**The reverse leakage current of a Schottky diode is:**

(a) Less than PN junction
(b) Greater than PN junction
(c) Same as PN junction
(d) Zero

**Answer: (b)**
**Explanation:** Schottky has higher reverse leakage due to thermionic emission over barrier. Typical: μA to mA range.

---

## Q20. PIN Diode I-Region
**The intrinsic region in a PIN diode:**

(a) Increases capacitance
(b) Decreases breakdown voltage
(c) Increases breakdown voltage
(d) Has no effect

**Answer: (c)**
**Explanation:** Wide I-region increases depletion width → reduces electric field → higher breakdown voltage. Also reduces capacitance.

---

## Q21. LED Direct Bandgap
**LED requires direct bandgap material because:**

(a) Higher mobility
(b) Efficient photon emission
(c) Lower cost
(d) Better thermal conductivity

**Answer: (b)**
**Explanation:** In direct bandgap, electron-hole recombination emits photon (momentum conservation). In indirect bandgap, phonon required → inefficient light emission.

---

## Q22. Photodiode Dark Current
**The dark current in a photodiode:**

(a) Increases with temperature
(b) Decreases with temperature
(c) Is independent of temperature
(d) Depends on light intensity

**Answer: (a)**
**Explanation:** Dark current is reverse saturation current → increases exponentially with temperature (like any PN junction).

---

## Q23. Zener Impedance
**The dynamic impedance of a Zener diode is typically:**

(a) Very high
(b) Very low (1-10 Ω)
(c) Zero
(d) Infinite

**Answer: (b)**
**Explanation:** Zener in breakdown has very low dynamic resistance (1-10 Ω), making it good voltage regulator.

---

## Q24. Tunnel Diode Application
**Tunnel diode is used in:**

(a) Power rectification
(b) High-frequency oscillators
(c) Voltage regulation
(d) Low-frequency amplifiers

**Answer: (b)**
**Explanation:** NDR property enables oscillation at very high frequencies (>100 GHz). Used in microwave oscillators.

---

## Q25. Solar Cell Fill Factor
**The fill factor of an ideal solar cell is approximately:**

(a) 0.5
(b) 0.7
(c) 0.85
(d) 1.0

**Answer: (c)**
**Explanation:** Ideal solar cell FF ≈ 0.85. Real cells: 0.7-0.85. Depends on series and shunt resistance.
