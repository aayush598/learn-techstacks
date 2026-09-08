# DC-DC Converters - Practice Questions

## Multiple Choice Questions

### Q1. In a buck converter, Vo = 5V, Vin = 12V. The duty cycle is:
(a) 0.583
(b) 0.417
(c) 0.294
(d) 0.706

**Answer: (b)**
D = Vo/Vin = 5/12 = 0.417

---

### Q2. A boost converter has Vin = 12V, D = 0.6. The output voltage is:
(a) 7.2V
(b) 20V
(c) 30V
(d) 19.2V

**Answer: (c)**
Vo = Vin/(1-D) = 12/(1-0.6) = 12/0.4 = 30V

---

### Q3. In CCM, the inductor current in a buck converter:
(a) Reaches zero each cycle
(b) Never reaches zero
(c) Is constant
(d) Varies linearly

**Answer: (b)**
CCM means continuous conduction - inductor current maintains a DC level with ripple, never falling to zero.

---

### Q4. A buck-boost converter with D = 0.75 gives Vo/Vin equal to:
(a) 0.33
(b) 1.0
(c) 3.0
(d) 4.0

**Answer: (c)**
Vo/Vin = D/(1-D) = 0.75/0.25 = 3.0

---

### Q5. The output ripple voltage of a boost converter can be reduced by:
(a) Increasing inductance
(b) Increasing output capacitance
(c) Increasing switching frequency
(d) All of the above

**Answer: (d)**
All three reduce ripple: higher L reduces ΔIL, higher C reduces ΔVo, higher fsw reduces both ΔIL and ΔVo.

---

### Q6. In a flyback converter, energy is transferred to the output:
(a) During switch ON time
(b) During switch OFF time
(c) During both ON and OFF
(d) At twice the switching frequency

**Answer: (b)**
Flyback stores energy in magnetizing inductance during ON, transfers to secondary during OFF.

---

### Q7. A buck converter operates at 100 kHz with Vin = 20V, D = 0.5, L = 100 μH. The peak-to-peak inductor current ripple is:
(a) 0.5A
(b) 1.0A
(c) 2.0A
(d) 4.0A

**Answer: (b)**
ΔIL = (Vin - Vo) × D/(Lfsw) = (20-10) × 0.5/(100×10⁻⁶ × 100×10³) = 5/(10) = 0.5A
Actually: ΔIL = Vin × D × (1-D)/(Lfsw) = 20 × 0.5 × 0.5/(10⁻⁴ × 10⁵) = 5/10 = 0.5A

Answer should be (a) 0.5A.

---

### Q8. The critical inductance for CCM/DCM boundary in a buck converter depends on:
(a) Only output capacitance
(b) Load resistance, duty cycle, and switching frequency
(c) Input voltage only
(d) Output voltage only

**Answer: (b)**
LC = (1-D) × R/(2fsw). It depends on D, RL (load), and fsw.

---

### Q9. In a boost converter at DCM, the output voltage:
(a) Is independent of load
(b) Increases with decreasing load
(c) Decreases with decreasing load
(d) Is always equal to Vin/(1-D)

**Answer: (b)**
In DCM, Vo = Vin × D²/(D² + 8Lfsw/R). As R increases (lighter load), Vo increases.

---

### Q10. The main advantage of Cuk converter over buck-boost is:
(a) Higher efficiency
(b) Continuous input and output currents
(c) Simpler circuit
(d) Higher voltage gain

**Answer: (b)**
Cuk has inductors at both input and output, providing continuous currents (lower EMI, lower ripple) unlike buck-boost's discontinuous currents.

---

### Q11. A buck converter with Vin = 48V needs Vo = 5V. The duty cycle is:
(a) 0.104
(b) 0.960
(c) 0.500
(d) 0.250

**Answer: (a)**
D = Vo/Vin = 5/48 = 0.104

---

### Q12. In CCM, Vo of a buck converter depends on:
(a) Load resistance
(b) Inductance
(c) Duty cycle only
(d) Capacitance

**Answer: (c)**
In CCM, Vo = D × Vin. Independent of load (ideal case).

---

### Q13. The output of a flyback converter is inverted when:
(a) N2/N1 = 1
(b) Diode is reversed
(c) Secondary winding has opposite polarity
(d) Never, flyback always gives positive output

**Answer: (c)**
Flyback polarity depends on dot convention of coupled inductor. Opposite polarity winding gives inverted output.

---

### Q14. A boost converter has Vin = 12V, Vo = 48V. If L = 200 μH, fsw = 50 kHz, and D = 0.75, the average inductor current at Io = 2A is:
(a) 2A
(b) 4A
(c) 8A
(d) 16A

**Answer: (c)**
IL(avg) = Io/(1-D) = 2/0.25 = 8A

---

### Q15. The ESR of the output capacitor contributes to voltage ripple because:
(a) It increases capacitance
(b) It creates I×R drop during current pulses
(c) It reduces inductance
(d) It increases switching frequency

**Answer: (b)**
ESR creates additional ripple: ΔVo(ESR) = ΔIL × ESR. This can dominate over capacitive ripple in electrolytic capacitors.

---

### Q16. Which converter has the highest switch voltage stress?
(a) Buck: Vpeak = Vin
(b) Boost: Vpeak = Vo
(c) Buck-Boost: Vpeak = Vin + Vo
(d) All have same stress

**Answer: (c)**
Buck-Boost switch sees Vin + Vo, which can be higher than either Vin or Vo alone. This is a disadvantage.

---

### Q17. At light load, a converter designed for CCM may enter:
(a) Voltage breakdown
(b) DCM
(c) Short circuit
(d) Overcurrent

**Answer: (b)**
When load current drops below Io(critical), inductor current reaches zero → DCM. This changes the Vo-D relationship.

---

### Q18. The primary advantage of using a coupled inductor in flyback over buck-boost is:
(a) Higher efficiency
(b) Electrical isolation
(c) Lower component count
(d) Higher switching frequency

**Answer: (b)**
Coupled inductor provides galvanic isolation between input and output, essential for safety and noise immunity.

---

### Q19. A buck converter has ΔIL = 2A at full load. At half load (Io halved), ΔIL:
(a) Doubles
(b) Halves
(c) Stays the same
(d) Becomes zero

**Answer: (c)**
ΔIL = Vin × D × (1-D)/(Lfsw), independent of load in CCM. Only DC level changes.

---

### Q20. The maximum duty cycle for a boost converter in CCM is limited by:
(a) Output voltage rating
(b) Inductor saturation
(c) Stability considerations
(d) All of the above

**Answer: (d)**
Practical limits: D < 0.9 (stability, efficiency), inductor saturation at high currents, output voltage rating.

---

## Numerical Problems

### N1. A buck converter has Vin = 24V, Vo = 5V, Pout = 25W, fsw = 200 kHz. Find D, Iin, and minimum L for ΔIL = 0.4A.
**Solution:**
D = Vo/Vin = 5/24 = 0.208
Io = Pout/Vo = 25/5 = 5A
Iin = D × Io = 0.208 × 5 = 1.04A (ideal)
Lmin = Vin × D × (1-D)/(fsw × ΔIL) = 24 × 0.208 × 0.792/(200×10³ × 0.4)
Lmin = 4.0/(80×10³) = 50 μH

---

### N2. A boost converter has Vin = 12V, Vo = 48V, Io = 1A, fsw = 100 kHz. Find D, IL(avg), and minimum L for CCM.
**Solution:**
D = 1 - Vin/Vo = 1 - 12/48 = 0.75
IL(avg) = Io/(1-D) = 1/0.25 = 4A
For CCM, ΔIL < 2 × IL(avg): Lmin = Vin × D/(fsw × ΔIL)
Let ΔIL = 0.8A (20% of IL): Lmin = 12 × 0.75/(100×10³ × 0.8) = 9/(8×10⁴) = 112.5 μH

---

### N3. A buck-boost converter has Vin = 24V, Vo = 36V (magnitude), Io = 2A. Find D and input current.
**Solution:**
Vo/Vin = D/(1-D) → 36/24 = D/(1-D)
1.5 = D/(1-D) → 1.5 - 1.5D = D → 1.5 = 2.5D → D = 0.6
Iin = Io × D/(1-D) = 2 × 0.6/0.4 = 3A

---

### N4. A flyback converter has Vin = 100V, N1/N2 = 5, Vo = 12V, D = 0.5. Verify the output voltage.
**Solution:**
Vo = Vin × (N2/N1) × D/(1-D) = 100 × (1/5) × 0.5/0.5 = 100 × 0.2 × 1 = 20V
But desired is 12V, so D needs adjustment:
12 = 100 × 0.2 × D/(1-D) → 0.6 = D/(1-D) → D = 0.375

---

### N5. A buck converter has Vo = 3.3V, Io = 10A, fsw = 500 kHz, ΔVo ≤ 30 mV. Find minimum C.
**Solution:**
ΔVo = ΔIL/(8fswC) → C = ΔIL/(8fsw × ΔVo)
ΔIL = Io × (1-D)/(Lfsw), but need L first.

Assume L = 1 μH, ΔIL = 1A (10% ripple):
C = 1/(8 × 500×10³ × 0.03) = 1/120000 = 8.33 μF

With ESR: ΔVo(ESR) = ΔIL × ESR, so need low-ESR capacitor.

---

## Assertion-Reason Type

### AR1. Assertion: Buck converter output voltage is always less than input voltage.
### Reason: Duty cycle D is always less than 1 in practical converters.

**Answer: Both true, R is correct explanation.**
Vo = D × Vin and 0 < D < 1, so Vo < Vin always.

---

### AR2. Assertion: DCM operation in DC-DC converters makes Vo depend on load.
### Reason: In DCM, the inductor current reaches zero, changing the energy transfer characteristics.

**Answer: Both true, R is correct explanation.**
DCM changes the voltage conversion ratio to include load resistance, making control more complex.

---

## True/False

1. **T/F: Boost converter can produce output voltage lower than input.**
**Answer: False.** Vo = Vin/(1-D) ≥ Vin for 0 ≤ D < 1.

2. **T/F: Cuk converter has continuous input current.**
**Answer: True.** Input inductor ensures continuous input current, reducing EMI.

3. **T/F: Flyback converter provides galvanic isolation.**
**Answer: True.** Coupled inductor separates primary and secondary circuits.

---

## Fill in the Blanks

1. In a buck converter, output voltage equals __________ times input voltage.
**Answer: duty cycle (D)**

2. A boost converter steps __________ the input voltage.
**Answer: up**

3. The boundary between CCM and DCM is called __________ conduction mode.
**Answer: critical (or boundary)**

4. The output ripple voltage of a DC-DC converter can be reduced by increasing __________ or __________.
**Answer: inductance (L), capacitance (C), or switching frequency (fsw)**

5. A __________ converter provides electrical isolation using a coupled inductor.
**Answer: flyback**
