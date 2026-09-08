# Power Semiconductor Devices - Practice Questions

## Multiple Choice Questions

### Q1. In a power diode, forward recovery is caused by:
(a) Junction capacitance charging
(b) Conductivity modulation lag
(c) Reverse minority carrier storage
(d) Avalanche breakdown

**Answer: (b)**
Forward recovery occurs when the diode is rapidly switched from OFF to ON. The lightly doped drift region takes time to modulate its conductivity, causing initial voltage overshoot.

---

### Q2. A fast recovery diode has trr = 50 ns and peak reverse current IRR = 10 A. The softness factor S = 1.5. Find tB.
(a) 30 ns
(b) 20 ns
(c) 33.3 ns
(d) 16.7 ns

**Answer: (a)**
S = tB/tA = 1.5
trr = tA + tB = 50 ns
tA + 1.5 × tA = 50 → 2.5 × tA = 50 → tA = 20 ns
tB = 1.5 × 20 = 30 ns

---

### Q3. For a power MOSFET, RDS(on) increases with voltage rating approximately as:
(a) BV²
(b) BV^2.5
(c) BV³
(d) BV^1.5

**Answer: (b)**
RDS(on) ∝ BV^2.5 due to the drift region resistance increasing faster than voltage rating. This is why MOSFETs are less efficient at high voltages compared to IGBTs.

---

### Q4. Which device has a positive temperature coefficient of on-state resistance, making it easy to parallel?
(a) BJT
(b) IGBT
(c) Power MOSFET
(d) SCR

**Answer: (c)**
MOSFET's RDS(on) increases with temperature (positive temp coefficient), which naturally balances current sharing when paralleled. BJTs have negative temp coefficient → thermal runaway risk.

---

### Q5. The tail current in an IGBT during turn-off is due to:
(a) Gate capacitance discharge
(b) Stored charge in the N- drift region
(c) Reverse recovery of the body diode
(d) Snubber capacitor discharge

**Answer: (b)**
The P+ substrate injects holes into the N- drift region during conduction. During turn-off, these minority carriers must recombine, causing a decaying "tail current" that increases switching losses.

---

### Q6. A Schottky diode is preferred over a PN junction diode in which application?
(a) High voltage rectification (>500V)
(b) Low voltage, high frequency switching
(c) High current, low frequency
(d) AC voltage regulation

**Answer: (b)**
Schottky diodes have low forward voltage (0.2-0.4V), negligible reverse recovery (majority carrier device), but limited voltage rating (<200V). Ideal for low-voltage SMPS.

---

### Q7. The safe operating area (SOA) of a MOSFET is bounded by all EXCEPT:
(a) Maximum drain current
(b) Maximum drain-source voltage
(c) Maximum power dissipation
(d) Maximum gate voltage

**Answer: (d)**
SOA is defined by: RDS(on) line, ID(max), VDS(max), power dissipation hyperbola, and second breakdown (for BJTs). Gate voltage affects RDS(on) but is not an SOA boundary.

---

### Q8. An IGBT is preferred over a MOSFET for:
(a) 12V, 100 kHz converter
(b) 600V, 20 kHz motor drive
(c) 48V, 500 kHz DC-DC converter
(d) 5V, 1 MHz logic circuit

**Answer: (b)**
At high voltages (600V), IGBT's low VCE(sat) gives lower conduction losses. At moderate switching frequencies (20 kHz), switching losses are acceptable. MOSFET would have excessive RDS(on) at 600V.

---

### Q9. The reverse recovery charge Qrr of a diode with trr = 100 ns and IRR = 8 A (triangular approximation) is:
(a) 400 nC
(b) 800 nC
(c) 200 nC
(d) 1600 nC

**Answer: (a)**
Qrr ≈ 0.5 × IRR × trr = 0.5 × 8 × 100 × 10⁻⁹ = 400 × 10⁻⁹ = 400 nC

---

### Q10. For an IGBT with VCE(sat) = 2V, IC(AV) = 50A, fsw = 20 kHz, EON = 5 mJ, EOFF = 3 mJ, find total power loss.
(a) 100 W
(b) 160 W
(c) 260 W
(d) 80 W

**Answer: (b)**
Pcond = VCE(sat) × IC(AV) = 2 × 50 = 100 W
Psw = (EON + EOFF) × fsw = (5 + 3) × 10⁻³ × 20 × 10³ = 160 W
Ptotal = 100 + 160 = 260 W

---

### Q11. Which statement about power diodes is FALSE?
(a) Fast recovery diodes have gold doping to reduce minority carrier lifetime
(b) Schottky diodes have higher reverse leakage than PN diodes
(c) PiN diodes are used for high voltage applications
(d) Power diodes have the same reverse recovery characteristics as signal diodes

**Answer: (d)**
Power diodes have significantly longer reverse recovery times due to their larger junction area and wider drift region designed for high voltage/current ratings.

---

### Q12. The Miller effect in MOSFETs causes:
(a) Increased RDS(on)
(b) Slower turn-on due to Cgd charging
(c) Increased body diode forward voltage
(d) Thermal runaway

**Answer: (b)**
During turn-on, Cgd (Miller capacitance) must be charged as VDS falls. This creates a plateau in gate voltage waveform, slowing the switching transition and increasing switching losses.

---

### Q13. A power diode has VRRM = 600V. What is the recommended maximum operating voltage?
(a) 600V
(b) 540V
(c) 480V
(d) 420V

**Answer: (c)**
Standard derating is 80% of rated voltage for reliability: 0.8 × 600 = 480V. For space applications, even more conservative derating (70-75%) may be used.

---

### Q14. In which region does a power MOSFET have the lowest conduction losses?
(a) Saturation region
(b) Linear (triode) region
(c) Cutoff region
(d) All regions are equal

**Answer: (b)**
In the linear region, VDS is small and ID = μnCox(W/L)[(VGS-Vth)VDS - VDS²/2], giving low VDS drop. Saturation has higher VDS and thus higher conduction losses.

---

### Q15. The maximum junction temperature of a silicon power device is typically:
(a) 100°C
(b) 125°C
(c) 150°C
(d) 200°C

**Answer: (c)**
Silicon power devices typically have Tj(max) = 150°C, with automotive grade reaching 175°C. Wide bandgap devices (SiC, GaN) can operate up to 200°C+.

---

### Q16. An IGBT's latching current is:
(a) Maximum current during turn-on
(b) Minimum current to maintain conduction after gate pulse
(c) Maximum repetitive peak current
(d) Current at which device enters saturation

**Answer: (b)**
Latching current is the minimum anode current required to maintain the SCR-like regenerative action in the IGBT's parasitic thyristor structure. Exceeding it during turn-on is normal operation.

---

### Q17. Which parameter determines the switching speed of a power MOSFET?
(a) RDS(on)
(b) Gate charge Qg
(c) Body diode forward voltage
(d) Thermal resistance

**Answer: (b)**
Gate charge determines how quickly the gate capacitance can be charged/discharged. Higher Qg requires more gate drive current for same switching speed: IG = Qg × fsw.

---

### Q18. The thermal resistance Rth(j-c) for a TO-220 packaged IGBT is typically:
(a) 0.1°C/W
(b) 1°C/W
(c) 5°C/W
(d) 50°C/W

**Answer: (b)**
TO-220 packages have Rth(j-c) ≈ 0.5-2°C/W. TO-247 packages: 0.4-0.8°C/W. TO-263 (D2PAK): 1-3°C/W. Module packages: 0.05-0.2°C/W.

---

### Q19. Power MOSFETs suffer from which parasitic element that can cause problems?
(a) Parasitic BJT
(b) Parasitic thyristor
(c) Parasitic JFET
(d) Parasitic SCR

**Answer: (a)**
Power MOSFETs have a parasitic NPN BJT formed by N+ source, P-body, and N- drain. If the P-body resistance is too high, this BJT can turn on, causing loss of gate control and potential destruction.

---

### Q20. For a SiC MOSFET compared to Si MOSFET at the same voltage rating:
(a) RDS(on) is higher
(b) Switching losses are higher
(c) RDS(on) is lower and switching losses are lower
(d) Thermal performance is worse

**Answer: (c)**
SiC has ~10x higher critical field strength, allowing thinner drift region → lower RDS(on). Lower capacitances → faster switching. Higher Tj(max) → better thermal performance.

---

## Numerical Problems

### N1. A power MOSFET has RDS(on) = 0.1Ω, ID(AV) = 30A. Calculate conduction loss.
**Solution:**
Pcond = ID(AV)² × RDS(on) = 30² × 0.1 = 900 × 0.1 = 90 W

---

### N2. An IGBT has VCE(sat) = 1.8V at IC = 100A. Find the on-state power dissipation.
**Solution:**
Pcond = VCE(sat) × IC = 1.8 × 100 = 180 W

---

### N3. A MOSFET has Qg = 150 nC, operates at 50 kHz with VGS = 12V. Find gate drive power.
**Solution:**
Pgate = Qg × VGS × fsw = 150 × 10⁻⁹ × 12 × 50 × 10³ = 90 mW

---

### N4. Two identical IGBTs (Rth(j-c) = 0.5°C/W each) are mounted on a heatsink (Rth(s-a) = 1°C/W). Each dissipates 100W. Find junction temperature if Ta = 40°C.
**Solution:**
Parallel devices share heatsink:
Total P = 200 W
Rth(j-c) per device = 0.5°C/W (thermal circuit is parallel for devices, series for path)
Tj = Ta + Ptotal × Rth(s-a) + Pdevice × Rth(j-c)
Tj = 40 + 200 × 1 + 100 × 0.5 = 40 + 200 + 50 = 290°C ← exceeds Tj(max)!

Need larger heatsink or forced cooling.

---

### N5. A diode has trr = 80 ns and IRR = 12A. Find Qrr (triangular approximation).
**Solution:**
Qrr ≈ 0.5 × IRR × trr = 0.5 × 12 × 80 × 10⁻⁹ = 480 nC

---

## Assertion-Reason Type

### AR1. Assertion: MOSFETs are preferred over IGBTs at switching frequencies above 100 kHz.
### Reason: MOSFET switching losses are proportional to frequency, while IGBT switching losses are independent of frequency.

**Answer: Assertion is true, Reason is false.**
Both MOSFET and IGBT switching losses are proportional to frequency (Psw = Esw × f). However, MOSFET has lower switching energy per cycle due to faster transitions, making it preferred at high frequencies.

---

### AR2. Assertion: Power diodes with soft recovery characteristics are preferred in converter circuits.
### Reason: Soft recovery diodes have higher reverse recovery losses.

**Answer: Assertion is true, Reason is false.**
Soft recovery diodes (S > 1) are preferred because they produce less voltage spikes (L di/dt) and EMI. They don't necessarily have higher losses; the key benefit is reduced transient voltages.

---

## True/False

1. **T/F: IGBT can be easily paralleled like MOSFETs.**
**Answer: False.** IGBTs have negative temperature coefficient of VCE(sat), making current balancing difficult without external ballast resistors.

2. **T/F: Schottky diodes are available with voltage ratings up to 5kV.**
**Answer: False.** Schottky diodes typically max out at 200-300V due to increased leakage current at higher voltages.

3. **T/F: MOSFET body diode can be used as a freewheeling diode in all applications.**
**Answer: False.** Body diode has poor reverse recovery characteristics, making it unsuitable for applications requiring fast freewheeling action.

---

## Fill in the Blanks

1. The __________ current in an IGBT causes additional switching losses during turn-off.
**Answer: tail**

2. __________ diodes have negligible reverse recovery time as they are majority carrier devices.
**Answer: Schottky**

3. The __________ effect in MOSFETs causes the Miller plateau during switching.
**Answer: Miller (gate-drain capacitance Cgd)**

4. IGBT combines the advantages of __________ (high input impedance) and __________ (low on-state losses).
**Answer: MOSFET, BJT**

5. The __________ of a MOSFET must be kept below the specified limit to prevent spurious turn-on.
**Answer: dv/dt**
