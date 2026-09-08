# GTO, TRIAC, DIAC - Practice Questions

## Multiple Choice Questions

### Q1. The turn-off gain of a typical GTO is:
(a) 10-20
(b) 3-5
(c) 50-100
(d) 100-200

**Answer: (b)**
GTO turn-off gain βoff = IA/|IG(off)| is typically 3-5. This means to turn off 500A, approximately 100-170A of negative gate current is required. This is a major limitation of GTOs.

---

### Q2. In a TRIAC, which quadrant has the lowest sensitivity (requires highest gate current)?
(a) Quadrant I (MT2+, Gate+)
(b) Quadrant II (MT2+, Gate-)
(c) Quadrant III (MT2-, Gate-)
(d) Quadrant IV (MT2-, Gate+)

**Answer: (d)**
Quadrant IV is the least sensitive, requiring 2-3× more gate current than other quadrants. In practice, TRIAC circuits are designed to avoid triggering in Quadrant IV.

---

### Q3. A DIAC has a breakover voltage of 32V. It will switch when voltage exceeds:
(a) 16V
(b) 32V
(c) 48V
(d) 64V

**Answer: (b)**
DIAC switches when |V| > VBO = 32V. The switching is symmetric in both polarities.

---

### Q4. GTO turn-off is achieved by:
(a) Reducing anode current below holding current
(b) Applying a large negative gate pulse
(c) Reverse biasing the anode-cathode
(d) Increasing gate current

**Answer: (b)**
GTO turns off via negative gate pulse that extracts stored charge from the P2 base layer. This is the key advantage over SCR - controlled turn-off capability.

---

### Q5. In a DIAC-TRIAC light dimmer circuit, the DIAC is used to:
(a) Limit current through the TRIAC
(b) Provide symmetric triggering pulses
(c) Protect against overvoltage
(d) Control the firing angle

**Answer: (b)**
DIAC provides symmetric breakover voltage in both half-cycles, ensuring equal triggering for positive and negative half-cycles. This eliminates DC component in the output.

---

### Q6. The stored time (ts) in a GTO turn-off refers to:
(a) Time for anode current to reach zero
(b) Time for gate to extract stored charge before current falls
(c) Time for forward blocking to be established
(d) Time between gate pulse and anode current rise

**Answer: (b)**
ts is the time during which the negative gate pulse is applied but anode current hasn't started to fall. During ts, stored charge is being extracted from the P2 base.

---

### Q7. A TRIAC is rated at 400V, 25A. What is the maximum AC voltage it can directly switch?
(a) 400V RMS
(b) 283V RMS
(c) 200V RMS
(d) 566V RMS

**Answer: (b)**
VDRM = 400V is the peak rating. For AC: Vpeak = √2 × Vrms
Vrms = VDRM/√2 = 400/1.414 = 283V (with derating, safer to use 230V)

---

### Q8. The tail current in a GTO during turn-off is due to:
(a) Gate capacitance discharge
(b) Stored charge in the drift region that cannot be extracted
(c) Snubber capacitor discharge
(d) Inductive load energy

**Answer: (b)**
After the fall time, remaining stored charge in the N- drift region recombines slowly, creating tail current. This contributes significantly to turn-off losses.

---

### Q9. Which device is most suitable for AC phase control at 10 kW?
(a) SCR (single)
(b) TRIAC
(c) Two anti-parallel SCRs
(d) GTO

**Answer: (c)**
At 10 kW, current exceeds TRIAC's practical limit (~40A). Two SCRs provide higher current/voltage ratings, independent control, and better thermal management.

---

### Q10. The breakover voltage of a DIAC has a __________ temperature coefficient:
(a) Positive
(b) Negative
(c) Zero
(d) Variable

**Answer: (b)**
DIAC VBO decreases with temperature (negative temperature coefficient, approximately -0.05%/°C), similar to SCR.

---

### Q11. GTO is being replaced by IGBTs in many applications because:
(a) GTO has higher voltage rating
(b) IGBT has simpler gate drive requirements
(c) GTO has higher switching frequency
(d) IGBT has higher current rating

**Answer: (b)**
IGBT requires simple voltage-controlled gate drive, while GTO needs complex high-current gate circuits for turn-off. IGBT also has higher switching frequency capability.

---

### Q12. In a TRIAC circuit, the minimum firing angle is limited by:
(a) Load inductance
(b) Gate trigger current
(c) Holding current
(d) Breakover voltage

**Answer: (d)**
The firing angle cannot be less than the angle at which capacitor voltage reaches VBO(DIAC). This sets the minimum conduction angle and maximum power delivery.

---

### Q13. A GTO with βoff = 4 needs to turn off 800A. The required negative gate current is:
(a) 20A
(b) 100A
(c) 200A
(d) 3200A

**Answer: (c)**
|IG(off)| = IA/βoff = 800/4 = 200A. This requires a powerful gate drive circuit with low inductance.

---

### Q14. The negative resistance region of a DIAC V-I characteristic means:
(a) Current decreases as voltage increases
(b) Voltage decreases as current increases
(c) Both increase proportionally
(d) Resistance remains constant

**Answer: (b)**
After breakover, voltage drops (from VBO to ~1-2V) while current increases rapidly. This negative resistance provides the sharp triggering action.

---

### Q15. TRIAC is essentially two SCRs connected in:
(a) Series
(b) Anti-parallel (back-to-back)
(c) Parallel
(d) H-bridge configuration

**Answer: (b)**
TRIAC monolithically integrates two SCRs in anti-parallel, allowing bidirectional current flow controlled by a single gate terminal.

---

### Q16. The maximum on-state current of a TRIAC is typically limited by:
(a) Gate power dissipation
(b) Junction temperature rise
(c) dv/dt capability
(d) Breakover voltage

**Answer: (b)**
Current rating is determined by maximum junction temperature. Exceeding rated current causes overheating and eventual failure.

---

### Q17. GTO snubber circuit is essential because:
(a) GTO cannot block forward voltage
(b) High dv/dt at turn-off can cause false triggering
(c) GTO needs help to turn on
(d) Gate drive is insufficient

**Answer: (b)**
GTO's high switching speeds create large dv/dt transients. Snubber circuits limit dv/dt and provide energy absorption during turn-off.

---

### Q18. For a DIAC with VBO = 32V, what capacitor voltage is needed to trigger a TRIAC?
(a) 16V
(b) 32V
(c) 48V
(d) 64V

**Answer: (b)**
Capacitor must charge to VBO = 32V before DIAC fires and triggers the TRIAC.

---

### Q19. TRIAC firing in Quadrant I uses which mechanism?
(a) Main SCR1 conduction
(b) Remote gate triggering
(c) Breakover triggering
(d) dv/dt triggering

**Answer: (a)**
Quadrant I (MT2+, Gate+) triggers the main SCR1 directly through the gate. This is the most sensitive mode.

---

### Q20. The main disadvantage of GTO compared to IGBT is:
(a) Lower voltage rating
(b) Complex and high-power gate drive requirement
(c) Lower current rating
(d) Higher switching frequency

**Answer: (b)**
GTO requires hundreds of amps of negative gate current for turn-off, demanding complex, expensive gate drive circuits. IGBT needs only simple voltage-controlled gate signals.

---

## Numerical Problems

### N1. A TRIAC controls a 230V, 500W resistive heater. Find the firing angle for 250W output.
**Solution:**
PL = PL(max) × (1 - α/π + sin(2α)/(2π))
PL(max) = V²/R = 500W at α = 0°
250 = 500 × (1 - α/π + sin(2α)/(2π))
0.5 = (1 - α/π + sin(2α)/(2π))

At α = 90°:
(1 - 90/180 + sin(180)/(2π)) = (1 - 0.5 + 0) = 0.5 ✓

α = 90° for half power

---

### N2. A GTO has IA = 500A, βoff = 5. Find the negative gate current required and gate power if turn-off pulse is 10 μs wide at 200 Hz.
**Solution:**
|IG(off)| = IA/βoff = 500/5 = 100A
PG(off) = |VG(off)| × |IG(off)| × tw × f
Assuming VG(off) = 20V:
PG(off) = 20 × 100 × 10×10⁻⁶ × 200 = 4W

---

### N3. A DIAC-TRIAC circuit has R = 10kΩ, C = 0.1μF, Vpeak = 325V (230V AC), VBO(DIAC) = 32V. Estimate the firing angle.
**Solution:**
α = arccos(1 - VBO/Vpeak) = arccos(1 - 32/325)
α = arccos(0.9015) = 25.6°

More accurately:
α = arctan(ωRC/1) when VBO << Vpeak
α = arctan(2π × 50 × 10×10³ × 0.1×10⁻⁶)
α = arctan(3.14 × 10⁻³) ≈ very small

The simplified formula gives α ≈ 26°.

---

### N4. Two SCRs are connected in anti-parallel for AC control. Each has VTM = 1.5V. If IRMS = 30A, find total conduction loss.
**Solution:**
Each SCR conducts for half cycle:
Pcond(1 SCR) = VTM × IAV = 1.5 × (30√2/π) = 1.5 × 13.5 = 20.3W
Total = 2 × 20.3 = 40.6W

Alternatively:
Ptotal = VTM × IRMS = 1.5 × 30 = 45W (approximate)

---

### N5. A TRIAC has IT(RMS) = 25A, VDRM = 600V. What is the maximum average load current it can handle in full AC operation?
**Solution:**
For full AC (both half-cycles):
IAV = 0 (symmetric)

For single half-cycle conduction:
IAV = IT(RMS) / FF = 25/1.57 = 15.9A per half-cycle

Maximum power (resistive):
Pmax = Vrms × IT(RMS) = 230 × 25 = 5750W (at 230V)

---

## Assertion-Reason Type

### AR1. Assertion: GTO requires a complex gate drive circuit compared to SCR.
### Reason: GTO needs both positive and negative gate pulses with high current capability.

**Answer: Both true, R is correct explanation.**
GTO needs large negative gate current (1/βoff × IA) for turn-off, requiring special gate drive circuits with energy storage and low inductance paths.

---

### AR2. Assertion: TRIAC should not be operated in Quadrant IV for reliable triggering.
### Reason: Quadrant IV has the lowest sensitivity, requiring highest gate current.

**Answer: Both true, R is correct explanation.**
Quadrant IV sensitivity is 0.3-0.5 of Quadrant I, making triggering unreliable. AC circuits naturally alternate between I+ and III- modes, avoiding IV.

---

## True/False

1. **T/F: GTO can be turned off by reducing anode current to zero.**
**Answer: True.** Like SCR, GTO can turn off when IA < IH (natural commutation). But GTO additionally has controlled turn-off via gate.

2. **T/F: DIAC is a two-terminal device that triggers in only one polarity.**
**Answer: False.** DIAC triggers symmetrically in both polarities when |V| > VBO.

3. **T/F: TRIAC has equal sensitivity in all four quadrants.**
**Answer: False.** Quadrant IV is significantly less sensitive (2-3× higher IGT required).

---

## Fill in the Blanks

1. The __________ of a GTO determines the negative gate current required for turn-off.
**Answer: turn-off gain (βoff)**

2. A __________ provides symmetric triggering pulses for a TRIAC in both half-cycles.
**Answer: DIAC**

3. The __________ current in a GTO contributes to turn-off losses and limits maximum switching frequency.
**Answer: tail**

4. TRIAC stands for __________ for Alternating Current.
**Answer: Triode**

5. The __________ region of a DIAC provides the sharp switching action needed for triggering.
**Answer: negative resistance**
