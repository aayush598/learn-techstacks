# SCR Thyristors - Practice Questions

## Multiple Choice Questions

### Q1. In the two-transistor analogy of SCR, the SCR latches when:
(a) α1 × α2 = 1
(b) α1 + α2 = 1
(c) α1 = α2
(d) α1 + α2 = 0

**Answer: (b)**
In the two-transistor model, α1 + α2 = 1 gives infinite anode current (IA → ∞), indicating latching. This is the self-sustaining condition where gate current is no longer needed.

---

### Q2. Holding current (IH) is always:
(a) Greater than latching current (IL)
(b) Equal to latching current
(c) Less than latching current
(d) Independent of latching current

**Answer: (c)**
IL > IH always. Latching current is the minimum to maintain turn-on (2-3× IH). Holding current is the minimum to maintain conduction (lower value). Once fully on, less current is needed to keep conducting.

---

### Q3. The dv/dt rating of an SCR can be improved by:
(a) Increasing gate current
(b) Using a snubber circuit across the SCR
(c) Increasing anode voltage
(d) Decreasing temperature

**Answer: (b)**
A snubber circuit (R-C) limits dv/dt by absorbing capacitive displacement current. The capacitor limits voltage rise rate, and the resistor limits discharge current through the SCR at turn-on.

---

### Q4. For a single-phase half-wave rectifier with SCR, maximum output voltage occurs at:
(a) α = 0°
(b) α = 90°
(c) α = 180°
(d) α = 45°

**Answer: (a)**
Vdc = Vm/(2π) × (1 + cos α). Maximum at α = 0°: Vdc = Vm/π. At α = 180°: Vdc = 0.

---

### Q5. The gate trigger circuit of an SCR provides:
(a) A continuous DC voltage to maintain conduction
(b) A pulse to initiate turn-on
(c) AC voltage to control firing angle
(d) Reverse bias to turn off

**Answer: (b)**
The gate pulse initiates turn-on. Once latched, the gate has no further effect. In AC circuits, natural commutation turns off the SCR at current zero-crossing.

---

### Q6. SCR can be turned off by all EXCEPT:
(a) Reducing anode current below IH
(b) Reverse voltage across anode-cathode
(c) Applying negative gate pulse (limited effect)
(d) Increasing gate current

**Answer: (d)**
Increasing gate current cannot turn off an SCR. Once latched, gate loses control. Turn-off requires: current below IH (natural commutation), reverse voltage, or forced commutation circuit.

---

### Q7. In a resistance firing circuit, the firing angle range is approximately:
(a) 0° to 180°
(b) 30° to 150°
(c) 0° to 90°
(d) 90° to 180°

**Answer: (b)**
Resistance firing has limited range due to the circuit's inability to provide sufficient gate voltage at extremes. Full range requires RC or UJT triggering.

---

### Q8. The snubber resistor in an SCR protection circuit is used to:
(a) Limit dv/dt
(b) Limit discharge current of snubber capacitor
(c) Increase switching losses
(d) Increase dv/dt

**Answer: (b)**
The snubber capacitor limits dv/dt, but when SCR turns on, the capacitor discharges through the SCR. The series resistor limits this discharge current to prevent di/dt damage.

---

### Q9. For an SCR with VTM = 1.5V carrying 50A average current, the conduction loss is:
(a) 75 W
(b) 50 W
(c) 25 W
(d) 100 W

**Answer: (a)**
Pcond = VTM × IT(AV) = 1.5 × 50 = 75 W

---

### Q10. Latching current is typically:
(a) 1/3 of holding current
(b) 2-3 times holding current
(c) Equal to holding current
(d) 10 times holding current

**Answer: (b)**
IL ≈ 2-3 × IH. This accounts for the additional current needed to establish full conduction area across the SCR junction during turn-on.

---

### Q11. The forward breakover voltage VBO of an SCR decreases with:
(a) Decreasing temperature
(b) Increasing temperature
(c) Decreasing gate current
(d) Increasing anode current

**Answer: (b)**
VBO has a negative temperature coefficient (-0.1%/°C approximately). Higher temperature increases leakage current, reducing the voltage needed for breakover. This is why thermal management is critical.

---

### Q12. A UJT firing circuit is preferred over resistance firing because:
(a) It provides better dv/dt immunity
(b) It gives a wider firing angle range (0° to 180°)
(c) It has lower cost
(d) It provides continuous gate current

**Answer: (b)**
UJT triggering provides 0° to 180° range with good linearity, unlike resistance firing which is limited to ~30°-150°. UJT also provides sharp, reliable pulses.

---

### Q13. An SCR with IT(RMS) = 100A is used in a half-wave rectifier. What is the maximum average load current?
(a) 100A
(b) 63.7A
(c) 50A
(d) 31.8A

**Answer: (b)**
For half-wave: IT(AV) = IT(RMS) / √(2π/π) = 100 / √2 ≈ 70.7A
But with conduction losses and derating, practical value is lower.
The form factor relationship: FF = IT(RMS)/IT(AV) = π/2 = 1.57 for full conduction.
IT(AV) = IT(RMS)/FF = 100/1.57 ≈ 63.7A

---

### Q14. Which firing method provides the best galvanic isolation?
(a) Resistance firing
(b) RC firing
(c) Optical (light-triggered) firing
(d) UJT firing

**Answer: (c)**
Light-triggered SCRs use fiber optic cables, providing complete electrical isolation between control and power circuits. Essential for high-voltage applications like HVDC converters.

---

### Q15. The di/dt rating of an SCR is exceeded when:
(a) Forward voltage rises too fast
(b) On-state current rises too fast
(c) Reverse voltage rises too fast
(d) Gate current is too high

**Answer: (b)**
di/dt is the rate of rise of anode current during turn-on. Excessive di/dt causes current crowding near the gate, creating hot spots that can destroy the SCR. Series inductors limit di/dt.

---

### Q16. In a single-phase full-wave center tap rectifier with SCR, Vdc at α = 60° (Vm = 200V) is:
(a) 95.5V
(b) 63.7V
(c) 47.7V
(d) 127.3V

**Answer: (a)**
Vdc = (Vm/π)(1 + cos α) = (200/π)(1 + cos 60°) = (200/π)(1.5) = 95.5V

---

### Q17. The minimum gate pulse width required for an SCR is related to:
(a) Holding current
(b) Latching current
(c) Breakover voltage
(d) On-state voltage

**Answer: (b)**
Gate pulse must be wide enough for anode current to reach IL before gate is removed. For inductive loads: tw ≥ IL × L / (V - VAK).

---

### Q18. A crowbar circuit uses an SCR to:
(a) Regulate output voltage
(b) Protect load from overvoltage by shorting supply
(c) Convert DC to AC
(d) Control motor speed

**Answer: (b)**
SCR crowbar fires when overvoltage detected, shorting the supply through a fuse or current-limiting device. The fuse blows, disconnecting the load. Used in power supply protection.

---

### Q19. The gate current of a typical SCR is of the order of:
(a) 1-10 μA
(b) 10-100 mA
(c) 1-10 A
(d) 10-100 A

**Answer: (b)**
Gate trigger current ranges from 10-500 mA for most SCRs. Power SCRs may require higher gate currents. This is much lower than the anode current, providing current gain.

---

### Q20. SCR is most suitable for which application?
(a) High-frequency inverters (>100 kHz)
(b) Phase-controlled AC voltage regulation
(c) Low-power DC-DC converters
(d) Audio amplifiers

**Answer: (b)**
SCRs excel at phase control in AC circuits due to natural commutation at current zero. They are limited to low frequency (<1 kHz) due to slow turn-off, making them ideal for 50/60 Hz power control.

---

## Numerical Problems

### N1. A single-phase half-wave SCR rectifier has Vm = 311V (230V AC). Find Vdc at α = 45°.
**Solution:**
Vdc = (Vm/2π)(1 + cos α) = (311/2π)(1 + cos 45°)
Vdc = (311/6.283)(1 + 0.707) = 49.5 × 1.707 = 84.5V

---

### N2. An SCR has Rth(j-c) = 0.3°C/W and maximum Tj = 150°C. If ambient is 40°C and heatsink has Rth(s-a) = 0.5°C/W, find maximum allowable power dissipation.
**Solution:**
Tj = Ta + P × (Rth(j-c) + Rth(s-a))
150 = 40 + P × (0.3 + 0.5)
P = 110/0.8 = 137.5 W

---

### N3. An SCR snubber has Cs = 0.1 μF. If the maximum allowable dv/dt is 200 V/μs and supply peak is 400V, find the required snubber resistance.
**Solution:**
dv/dt = V/Cs → Cs ≥ V/(dv/dt) = 400/(200×10⁶) = 2 μF
Minimum Cs = 2 μF (given Cs = 0.1 μF is insufficient!)
Rs = V/(di/dt)limit, typically 10-100Ω for discharge limiting.

---

### N4. A three-phase full-wave bridge rectifier with SCR has Vline(rms) = 415V. Find Vdc at α = 30°.
**Solution:**
Vdc = (3Vml/π) cos α = (3 × √2 × 415/π) cos 30°
Vdc = (3 × 1.414 × 415/3.1416) × 0.866
Vdc = (1764/3.1416) × 0.866 = 561.5 × 0.866 = 486.3V

---

### N5. An SCR carries a half-sine current pulse of 200A peak for 10 ms. Find the I²t rating required.
**Solution:**
I²t = (Im²/2) × t = (200²/2) × 10×10⁻³
I²t = (40000/2) × 0.01 = 200 A²s

---

## Assertion-Reason Type

### AR1. Assertion: SCR turn-off in AC circuits is simpler than in DC circuits.
### Reason: AC circuits naturally provide current zero-crossing for natural commutation.

**Answer: Both true, R is correct explanation.**
AC circuits provide natural current zero-crossing (natural commutation) at every half-cycle. DC circuits require forced commutation circuits, adding complexity.

---

### AR2. Assertion: Snubber capacitor value should be maximized for best dv/dt protection.
### Reason: Larger capacitor provides better dv/dt limiting but increases discharge current through SCR.

**Answer: Assertion false, Reason true.**
While larger Cs gives better dv/dt protection, it also increases discharge energy at turn-on (E = ½CV²), potentially exceeding di/dt rating. Optimal Cs balances both constraints.

---

## True/False

1. **T/F: SCR gate can turn off the device in DC circuits.**
**Answer: False.** Gate only initiates turn-on; it cannot turn off an SCR. Turn-off requires current below IH or forced commutation.

2. **T/F: SCR can block both forward and reverse voltages.**
**Answer: True.** Forward blocking: VDRM. Reverse blocking: VRRM. Both are rated parameters.

3. **T/F: Latching current is always greater than holding current.**
**Answer: True.** IL > IH by factor of 2-3 typically.

---

## Fill in the Blanks

1. The minimum anode current to maintain SCR conduction is called __________ current.
**Answer: holding**

2. __________ firing provides the widest firing angle range (0° to 180°).
**Answer: UJT or RC**

3. The __________ current flows during SCR turn-off and must be limited by snubber resistor.
**Answer: snubber capacitor discharge**

4. For inductive loads, the gate pulse width must be increased because current rises __________ than voltage.
**Answer: slower**

5. The __________ circuit protects the SCR from false triggering due to voltage transients.
**Answer: snubber**
