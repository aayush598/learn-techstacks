# Rectifiers - Practice Questions

## Multiple Choice Questions

### Q1. The form factor of a single-phase full-wave bridge rectifier is:
(a) 1.57
(b) 1.11
(c) 1.00
(d) 2.00

**Answer: (b)**
FF = Vrms/Vdc = (Vm/√2)/(2Vm/π) = π/(2√2) = 1.11

---

### Q2. A freewheeling diode in a controlled rectifier:
(a) Increases output voltage
(b) Prevents output voltage from going negative
(c) Decreases input power factor
(d) Increases harmonic content

**Answer: (b)**
FD provides path for inductive load current and clamps output voltage to zero (not negative) during freewheeling period, improving Vdc and power factor.

---

### Q3. The ripple factor of a three-phase full-wave rectifier is approximately:
(a) 48.2%
(b) 18.3%
(c) 4%
(d) 82.7%

**Answer: (c)**
Three-phase full-wave: RF = 4% (0.04). This is why three-phase rectifiers are preferred for high-quality DC supplies.

---

### Q4. For a half-wave rectifier with Vm = 311V, the average output voltage is:
(a) 99V
(b) 198V
(c) 220V
(d) 311V

**Answer: (a)**
Vdc = Vm/π = 311/3.1416 = 99V

---

### Q5. The PIV (Peak Inverse Voltage) of each diode in a full-wave center tap rectifier is:
(a) Vm
(b) 2Vm
(c) Vm/2
(d) √2 Vm

**Answer: (b)**
In center tap configuration, when one diode conducts, the other sees the full voltage across both ends = 2Vm.

---

### Q6. A capacitor filter for a full-wave rectifier operating at 50 Hz with Iload = 2A and desired ripple of 5V requires:
(a) 1000 μF
(b) 2000 μF
(c) 4000 μF
(d) 500 μF

**Answer: (b)**
C = Iload/(2f × ΔV) = 2/(2 × 50 × 5) = 2/500 = 4000 μF
Wait, let me recalculate: C = 2/(100 × 5) = 4000 μF → Answer (c)
Actually: C = Iload/(2fΔV) = 2/(2 × 50 × 5) = 2/500 = 0.004 F = 4000 μF

Answer should be (c) 4000 μF.

---

### Q7. The transformer utilization factor (TUF) is highest for:
(a) Half-wave rectifier
(b) Full-wave center tap
(c) Single-phase bridge
(d) Three-phase full bridge

**Answer: (d)**
TUF values: Half-wave = 0.287, Center tap = 0.693, Bridge = 0.812, Three-phase full = 0.955

---

### Q8. In a fully controlled bridge rectifier with resistive load, the output voltage becomes zero at:
(a) α = 0°
(b) α = 90°
(c) α = 180°
(d) α = 45°

**Answer: (b)**
Vdc = (2Vm/π) cos α. At α = 90°: cos 90° = 0, so Vdc = 0.

---

### Q9. The dominant harmonic in a single-phase full-wave rectifier output is:
(a) Fundamental (50 Hz)
(b) Second harmonic (100 Hz)
(c) Third harmonic (150 Hz)
(d) DC component

**Answer: (b)**
Output frequency = 2 × input frequency. Dominant ripple is at 100 Hz (for 50 Hz input).

---

### Q10. A freewheeling diode conducts for:
(a) Entire positive half-cycle
(b) Portion of negative half-cycle when SCR is off
(c) Entire cycle
(d) Only during commutation

**Answer: (b)**
FD conducts when main SCR turns off and inductive load current needs a path. This is during the portion when output voltage would otherwise go negative.

---

### Q11. The efficiency of a half-wave rectifier is:
(a) 81.2%
(b) 40.6%
(c) 100%
(d) 50%

**Answer: (b)**
η = (2/π)² = 0.406 = 40.6%. This is why half-wave rectifiers are rarely used in power supplies.

---

### Q12. In a three-phase half-wave rectifier, each diode conducts for:
(a) 60°
(b) 120°
(c) 180°
(d) 360°

**Answer: (b)**
Each phase conducts for 120° (one-third of the cycle) in a three-phase half-wave configuration.

---

### Q13. The output ripple frequency of a three-phase full bridge rectifier with 50 Hz input is:
(a) 50 Hz
(b) 100 Hz
(c) 150 Hz
(d) 300 Hz

**Answer: (d)**
Three-phase full bridge produces 6-pulse output: ripple = 6 × 50 = 300 Hz.

---

### Q14. An SCR in a fully controlled bridge operates in inversion mode when:
(a) 0° < α < 90°
(b) α = 90°
(c) 90° < α < 180°
(d) α = 0°

**Answer: (c)**
For α > 90° with continuous conduction, cos α is negative, meaning power flows from DC to AC side (inversion).

---

### Q15. The capacitor filter peak current is much higher than average current because:
(a) Capacitor charges in short pulses
(b) Diode has high forward resistance
(c) Load current is discontinuous
(d) Transformer has high leakage

**Answer: (a)**
Capacitor charges only near voltage peak in narrow pulses, resulting in high peak currents (3-5× average).

---

### Q16. A semi-converter bridge rectifier has:
(a) Four SCRs
(b) Two SCRs and two diodes
(c) Four diodes
(d) Six SCRs

**Answer: (b)**
Semi-converter uses two SCRs (for control) and two diodes (commutation), reducing cost and complexity.

---

### Q17. The form factor of a half-wave rectifier is:
(a) 1.11
(b) 1.57
(c) 2.00
(d) 0.637

**Answer: (b)**
FF = Vrms/Vdc = (Vm/2)/(Vm/π) = π/2 = 1.57

---

### Q18. Which rectifier configuration has the highest TUF?
(a) Half-wave
(b) Full-wave center tap
(c) Single-phase bridge
(d) Three-phase half-wave

**Answer: (c)**
Single-phase bridge TUF = 0.812 is highest among single-phase options. Three-phase full bridge (0.955) is highest overall.

---

### Q19. In a controlled rectifier with inductive load and no freewheeling diode, the average output voltage at α = 120° is:
(a) Positive
(b) Zero
(c) Negative
(d) Maximum

**Answer: (c)**
Vdc = (2Vm/π) cos 120° = (2Vm/π)(-0.5) = negative. The inductor forces conduction even when voltage reverses.

---

### Q20. The ripple voltage of a full-wave rectifier with C filter is:
(a) ΔV = I/(fC)
(b) ΔV = I/(2fC)
(c) ΔV = I/(4fC)
(d) ΔV = 2I/(fC)

**Answer: (b)**
For full-wave: ΔV = Iload/(2fC). For half-wave: ΔV = Iload/(fC).

---

## Numerical Problems

### N1. A single-phase bridge rectifier has Vrms = 230V, RL = 10Ω. Find Vdc, Idc, Pdc, and efficiency.
**Solution:**
Vm = √2 × 230 = 325.3V
Vdc = 2Vm/π = 2 × 325.3/π = 207V
Idc = Vdc/RL = 207/10 = 20.7A
Pdc = Vdc × Idc = 207 × 20.7 = 4285W
Pac = Vrms²/RL = 230²/10 = 5290W
η = Pdc/Pac = 4285/5290 = 81% (matches theoretical 81.2%)

---

### N2. A full-wave center tap rectifier has Vm = 100V (from center tap). Find Vrms output and PIV of each diode.
**Solution:**
Vrms = Vm/√2 = 100/1.414 = 70.7V
PIV = 2Vm = 200V

---

### N3. Design a capacitor filter for a full-wave rectifier: Vdc = 12V, Iload = 500mA, ripple ≤ 1V, f = 50 Hz.
**Solution:**
C = Iload/(2f × ΔV) = 0.5/(2 × 50 × 1) = 0.5/100 = 5000 μF

Check: τ = RL × C = (12/0.5) × 5000×10⁻⁶ = 24 × 0.005 = 0.12s
T = 1/(2f) = 0.01s
τ/T = 12 > 5 ✓ (good filtering)

---

### N4. A three-phase full bridge rectifier has VL(rms) = 415V. Find Vdc and PIV.
**Solution:**
Vml = √2 × 415 = 586.7V (line-to-line peak)
Vdc = 3Vml/π = 3 × 586.7/π = 561.1V
PIV = Vml = 586.7V

---

### N5. An SCR fully controlled bridge has Vm = 200V, RL = 10Ω, α = 60°. Find Vdc and Idc (resistive load).
**Solution:**
Vdc = (2Vm/π) cos α = (2 × 200/π) cos 60° = (400/π) × 0.5 = 63.7V
Idc = Vdc/RL = 63.7/10 = 6.37A

---

## Assertion-Reason Type

### AR1. Assertion: Three-phase rectifiers have lower ripple than single-phase rectifiers.
### Reason: Three-phase rectifiers have higher output frequency and more pulses per cycle.

**Answer: Both true, R is correct explanation.**
Three-phase full bridge produces 6 pulses per cycle (300 Hz for 50 Hz), while single-phase full-wave produces 2 pulses (100 Hz). Higher pulse count reduces ripple.

---

### AR2. Assertion: Capacitor input filters cause higher peak diode currents.
### Reason: Capacitor charges only during short intervals near voltage peaks.

**Answer: Both true, R is correct explanation.**
The capacitor must charge the full load energy in short pulses, resulting in high peak currents (3-5× average) concentrated near voltage peaks.

---

## True/False

1. **T/F: Half-wave rectifier has better TUF than full-wave bridge.**
**Answer: False.** Half-wave TUF = 0.287, Bridge TUF = 0.812. Bridge is much better.

2. **T/F: Three-phase rectifier output has no ripple.**
**Answer: False.** It has very low ripple (4%), not zero.

3. **T/F: Freewheeling diode improves input power factor.**
**Answer: True.** FD reduces input current distortion, improving PF.

---

## Fill in the Blanks

1. The ratio of RMS voltage to average voltage is called __________.
**Answer: form factor**

2. A __________ connected across the load in a controlled rectifier prevents negative output voltage.
**Answer: freewheeling diode**

3. The __________ of a rectifier determines the filtering requirements.
**Answer: ripple factor**

4. Three-phase full bridge produces __________ pulses per cycle.
**Answer: six (6)**

5. The peak inverse voltage of each diode in a single-phase bridge rectifier equals __________.
**Answer: Vm (peak input voltage)**
