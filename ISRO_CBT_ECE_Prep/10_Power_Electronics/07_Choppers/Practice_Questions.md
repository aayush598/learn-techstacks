# Choppers - Practice Questions

## Multiple Choice Questions

### Q1. A Type A chopper has Vin = 200V, D = 0.6. The output voltage is:
(a) 120V
(b) 333V
(c) 80V
(d) 200V

**Answer: (a)**
Vo = D × Vin = 0.6 × 200 = 120V

---

### Q2. In a Type B chopper, power flows from:
(a) Source to load
(b) Load to source
(c) Both directions equally
(d) Neither direction

**Answer: (b)**
Type B operates in second quadrant: load has back-EMF (motor), power regenerates to source.

---

### Q3. A four-quadrant chopper (Type E) uses:
(a) 2 switches and 2 diodes
(b) 4 switches and 4 diodes
(c) 1 switch and 1 diode
(d) 2 switches only

**Answer: (b)**
Type E (H-bridge) requires 4 switches and 4 diodes for full four-quadrant operation.

---

### Q4. In a step-up chopper with D = 0.8, the voltage gain is:
(a) 1.25
(b) 5
(c) 8
(d) 0.8

**Answer: (b)**
M = 1/(1-D) = 1/0.2 = 5

---

### Q5. A Jones chopper uses __________ for forced commutation:
(a) Load commutation
(b) Auto-transformer and capacitor
(c) Series inductor
(d) Line commutation

**Answer: (b)**
Jones chopper uses auto-transformer for energy transfer and capacitor for SCR commutation.

---

### Q6. The output voltage ripple of a buck chopper can be reduced by:
(a) Increasing switching frequency
(b) Increasing inductance
(c) Adding output capacitor
(d) All of the above

**Answer: (d)**
All three methods reduce output voltage ripple.

---

### Q7. Morgan chopper is also known as:
(a) Jones chopper
(b) Impulse-commutated chopper
(c) Step-up chopper
(d) Resonant chopper

**Answer: (b)**
Morgan chopper uses impulse commutation via capacitor discharge through auxiliary SCR.

---

### Q8. Type C chopper operates in:
(a) First quadrant only
(b) Second quadrant only
(c) First and second quadrants
(d) All four quadrants

**Answer: (c)**
Type C combines Type A and Type B for two-quadrant operation (positive voltage, bidirectional current).

---

### Q9. A buck chopper has Vin = 100V, L = 5mH, fsw = 1kHz, D = 0.5. The peak-to-peak current ripple is:
(a) 5A
(b) 10A
(c) 2.5A
(d) 20A

**Answer: (a)**
ΔIL = Vin × D × (1-D)/(Lfsw) = 100 × 0.5 × 0.5/(5×10⁻³ × 10³) = 25/5 = 5A

---

### Q10. In regenerative braking, the chopper operates as:
(a) Step-down converter
(b) Step-up converter
(c) Buck-boost converter
(d) Linear regulator

**Answer: (b)**
Regenerative braking requires stepping up the motor back-EMF to match or exceed source voltage.

---

### Q11. The average output voltage of a Type E chopper in quadrant III is:
(a) Positive
(b) Zero
(c) Negative
(d) Equal to Vin

**Answer: (c)**
Quadrant III: reverse motoring, Vo is negative (opposite polarity to quadrant I).

---

### Q12. A chopper feeds a DC motor. For smooth speed control, the minimum inductance should ensure:
(a) Discontinuous current
(b) Continuous current (CCM)
(c) Zero current
(d) Maximum current

**Answer: (b)**
Continuous current (CCM) provides smoother speed control and better dynamic response.

---

### Q13. The duty cycle of a step-up chopper to get Vo = 5Vin is:
(a) 0.2
(b) 0.5
(c) 0.8
(d) 0.9

**Answer: (c)**
D = 1 - Vin/Vo = 1 - 1/5 = 0.8

---

### Q14. In a Type D chopper:
(a) Voltage is bidirectional, current is unidirectional
(b) Voltage is unidirectional, current is bidirectional
(c) Both are bidirectional
(d) Both are unidirectional

**Answer: (a)**
Type D: Vo can be positive or negative, but Io flows in one direction only.

---

### Q15. The commutation capacitor in a Morgan chopper must store energy equal to:
(a) Output power
(b) Input power
(c) SCR turn-off energy requirement
(d) Inductor energy

**Answer: (c)**
Capacitor energy E = 0.5CV² must exceed SCR's turn-off energy requirement.

---

### Q16. Which chopper is most suitable for DC motor speed control in both directions?
(a) Type A
(b) Type B
(c) Type C
(d) Type E

**Answer: (d)**
Type E (four-quadrant) provides forward/reverse motoring and regeneration in both directions.

---

### Q17. The source current waveform in a buck chopper is:
(a) Continuous DC
(b) Rectangular pulses
(c) Triangular
(d) Sinusoidal

**Answer: (b)**
Source current flows only during switch ON time → rectangular pulses at switching frequency.

---

### Q18. A step-up chopper with D = 0.6 and Vin = 24V gives output voltage:
(a) 40V
(b) 60V
(c) 38.4V
(d) 14.4V

**Answer: (b)**
Vo = Vin/(1-D) = 24/0.4 = 60V

---

### Q19. Jones chopper provides:
(a) Only step-down operation
(b) Only step-up operation
(c) Both step-up and step-down
(d) AC output

**Answer: (c)**
Auto-transformer allows both modes depending on turns ratio and duty cycle.

---

### Q20. For a four-quadrant chopper, the switching sequence for quadrant I forward motoring is:
(a) Q1, Q3 PWM
(b) Q2, Q4 PWM
(c) Q1, Q4 PWM
(d) Q2, Q3 PWM

**Answer: (c)**
Q1 and Q4 conduct together for forward motoring (positive Vo, positive Io).

---

## Numerical Problems

### N1. A buck chopper feeds a DC motor with back-EMF = 80V, Ra = 0.5Ω, Vin = 150V. Find D for Io = 20A.
**Solution:**
Vo = E + Io × Ra = 80 + 20 × 0.5 = 90V
D = Vo/Vin = 90/150 = 0.6

---

### N2. A boost chopper has Vin = 48V, D = 0.75, Io = 10A. Find Vo and input current.
**Solution:**
Vo = Vin/(1-D) = 48/0.25 = 192V
Iin = Io/(1-D) = 10/0.25 = 40A (or Iin = Io × Vo/Vin = 10 × 4 = 40A)

---

### N3. A Type E chopper drives a motor at 100V, 20A in forward motoring. Find the power and efficiency if switching losses are 5%.
**Solution:**
Pout = Vo × Io = 100 × 20 = 2000W
Ploss = 0.05 × 2000 = 100W (approximate)
Pin = 2000 + 100 = 2100W
η = 2000/2100 = 95.2%

---

### N4. A buck chopper has ΔIL = 4A, Io = 16A. Find the minimum and maximum inductor current.
**Solution:**
IL(min) = Io - ΔIL/2 = 16 - 2 = 14A
IL(peak) = Io + ΔIL/2 = 16 + 2 = 18A

---

### N5. A Jones chopper has N2/N1 = 1.5, D = 0.4, Vin = 100V. Find Vo.
**Solution:**
Vo = Vin × (N2/N1) × D/(1-D) = 100 × 1.5 × 0.4/0.6 = 100 × 1.5 × 0.667 = 100V

---

## Assertion-Reason Type

### AR1. Assertion: Type B chopper requires an active load for operation.
### Reason: Type B operates in second quadrant where load must have back-EMF.

**Answer: Both true, R is correct explanation.**
Type B needs motor or other active source to push current back to supply. Passive loads cannot generate negative current.

---

### AR2. Assertion: Step-up chopper cannot operate at D = 1.
### Reason: At D = 1, theoretical output voltage is infinite.

**Answer: Both true, R is correct explanation.**
Vo = Vin/(1-D) → ∞ as D → 1. Practical limit is D < 0.9 due to component stresses and efficiency.

---

## True/False

1. **T/F: Type A chopper can regenerate power to source.**
**Answer: False.** Type A is unidirectional (source to load only). Regeneration requires Type B or C/E.

2. **T/F: Four-quadrant chopper requires only one switch.**
**Answer: False.** Requires four switches (H-bridge) for full four-quadrant operation.

3. **T/F: Morgan chopper uses load commutation.**
**Answer: False.** Morgan chopper uses forced commutation via capacitor and auxiliary SCR.

---

## Fill in the Blanks

1. A __________ chopper provides step-down operation (Vo < Vin).
**Answer: Type A (or buck)**

2. __________ operation allows power to flow from load back to source.
**Answer: Second quadrant (or regenerative)**

3. The __________ chopper uses an auto-transformer for voltage transformation.
**Answer: Jones**

4. Type E chopper provides __________ operation.
**Answer: four-quadrant**

5. The output voltage of a step-up chopper equals __________ when D = 0.8.
**Answer: 5 × Vin (or Vo = Vin/(1-0.8) = 5Vin)**
