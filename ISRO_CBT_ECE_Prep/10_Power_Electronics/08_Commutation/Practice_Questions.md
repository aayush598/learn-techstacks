# Commutation - Practice Questions

## Multiple Choice Questions

### Q1. Natural commutation occurs in:
(a) DC circuits
(b) AC circuits at current zero-crossing
(c) Only resonant circuits
(d) Only inverter circuits

**Answer: (b)**
Natural commutation uses AC line current zero-crossing to turn off SCR. Simple and reliable for AC applications.

---

### Q2. Class B commutation is also called:
(a) Load commutation
(b) Resonant pulse commutation
(c) Complementary commutation
(d) External pulse commutation

**Answer: (b)**
Class B uses resonant LC tank to generate current pulse opposing load current.

---

### Q3. For load commutation, the series RLC circuit must be:
(a) Overdamped
(b) Critically damped
(c) Underdamped
(d) Resonant

**Answer: (c)**
Underdamped (ζ < 1) ensures current oscillates to zero, allowing SCR turn-off.

---

### Q4. The minimum capacitor value for Class D commutation is:
(a) C = IL × tq / Vc
(b) C = Vc / (IL × tq)
(c) C = IL / (Vc × tq)
(d) C = Vc × tq / IL

**Answer: (a)**
C ≥ IL × tq / Vc ensures capacitor can supply load current during turn-off time.

---

### Q5. In complementary commutation, current transfer occurs when:
(a) Load current reaches zero
(b) Capacitor voltage reverses bias across conducting SCR
(c) Auxiliary SCR fires
(d) Line voltage crosses zero

**Answer: (b)**
Firing the complementary SCR applies reverse capacitor voltage, turning off the conducting SCR.

---

### Q6. GTO turn-off requires:
(a) Zero gate voltage
(b) Large negative gate current
(c) Series capacitor
(d) Auxiliary SCR

**Answer: (b)**
GTO turns off via large negative gate pulse that extracts stored charge from P2 base.

---

### Q7. The resonant frequency of Class B commutation circuit determines:
(a) Output voltage
(b) Commutation time
(c) Input current
(d) Load power

**Answer: (b)**
tc = 1/(2fres). Higher resonant frequency → shorter commutation time.

---

### Q8. Commutation failure occurs when:
(a) tc > tq
(b) Vc > VRRM
(c) tc < tq
(d) IL < IH

**Answer: (c)**
If commutation time is less than SCR turn-off time, SCR cannot recover blocking capability.

---

### Q9. A snubber capacitor value is determined by:
(a) Load current
(b) Desired dv/dt limiting
(c) Input voltage only
(d) Switching frequency

**Answer: (b)**
Cs = Vpeak/(dv/dt)max. Larger Cs gives better dv/dt protection.

---

### Q10. In Class E commutation, the auxiliary SCR:
(a) Charges the capacitor
(b) Diverts current from main SCR
(c) Provides gate pulse
(d) Protects against overvoltage

**Answer: (b)**
Auxiliary SCR diverts load current away from main SCR, allowing it to turn off.

---

### Q11. The damped resonant frequency ωd is:
(a) ωd = 1/√(LC)
(b) ωd = √(ω₀² - α²)
(c) ωd = R/(2L)
(d) ωd = 2πf

**Answer: (b)**
ωd = √(ω₀² - α²) where ω₀ = 1/√(LC) and α = R/(2L). Damping reduces frequency.

---

### Q12. For successful Class B commutation:
(a) IL must exceed resonant current
(b) Resonant current must exceed IL
(c) Resonant current equals IL
(d) Load current must be zero

**Answer: (b)**
Ires(peak) > IL ensures net SCR current goes to zero.

---

### Q13. The commutation margin angle should be:
(a) 0°
(b) Negative
(c) Positive and typically 20-30% of tq
(d) Equal to firing angle

**Answer: (c)**
Safety margin ensures reliable commutation under varying conditions.

---

### Q14. Series inductor in turn-on snubber limits:
(a) dv/dt
(b) di/dt
(c) Output voltage
(d) Input current

**Answer: (b)**
Ls limits di/dt = V/Ls during SCR turn-on, preventing current crowding.

---

### Q15. Which commutation class is simplest and most reliable?
(a) Class A
(b) Class D
(c) Natural commutation
(d) Class F

**Answer: (c)**
Natural commutation requires no external circuit, using AC zero-crossing.

---

### Q16. The snubber resistor power rating depends on:
(a) Load current
(b) Snubber capacitance and switching frequency
(c) Input voltage only
(d) Output power

**Answer: (b)**
Ps = 0.5 × Cs × V² × fsw. Higher Cs or fsw increases snubber loss.

---

### Q17. Complementary commutation is used in:
(a) Half-wave rectifiers
(b) McMurray-Bedford inverter
(c) Single-phase bridge rectifier
(d) Three-phase controlled rectifier

**Answer: (b)**
McMurray-Bedford inverter uses complementary commutation with two SCRs.

---

### Q18. The stored time (ts) in GTO turn-off represents:
(a) Time for current to reach zero
(b) Time to extract charge before current starts falling
(c) Total turn-off time
(d) Time to recharge capacitor

**Answer: (b)**
ts is the initial phase where gate pulse is applied but anode current hasn't started falling.

---

### Q19. Load commutation requires the load to be:
(a) Purely resistive
(b) Inductive
(c) Series RLC with ζ < 1
(d) Capacitive only

**Answer: (c)**
Underdamped RLC ensures current oscillates to zero, providing natural commutation.

---

### Q20. The maximum switching frequency for a Class D commutated chopper is limited by:
(a) Load resistance
(b) Capacitor charging time
(c) Output voltage
(d) Input voltage

**Answer: (b)**
Capacitor must recharge between commutations, limiting maximum frequency.

---

## Numerical Problems

### N1. A Class B commutation circuit has L = 10 μH, C = 0.1 μF. Find resonant frequency and commutation time.
**Solution:**
fres = 1/(2π√(LC)) = 1/(2π√(10×10⁻⁶ × 0.1×10⁻⁶))
= 1/(2π × 10⁻⁶) = 1/(6.283 × 10⁻⁶) = 159 kHz
tc = 1/(2fres) = 1/(2 × 159×10³) = 3.14 μs

---

### N2. Class D commutation: IL = 50A, tq = 50 μs, Vc = 200V. Find minimum C.
**Solution:**
C = IL × tq / Vc = 50 × 50×10⁻⁶ / 200 = 2500×10⁻⁶/200 = 12.5 μF

---

### N3. Series RLC load commutation: R = 10Ω, L = 1mH, C = 10μF. Find ζ and ωd.
**Solution:**
ζ = R/(2√(L/C)) = 10/(2√(10⁻³/10⁻⁵)) = 10/(2√100) = 10/20 = 0.5
ω₀ = 1/√(LC) = 1/√(10⁻³ × 10⁻⁵) = 1/10⁻⁴ = 10000 rad/s
ωd = √(ω₀² - α²) = √(10⁸ - (R/(2L))²) = √(10⁸ - (10/0.002)²)
= √(10⁸ - (5000)²) = √(10⁸ - 2.5×10⁷) = √(7.5×10⁷) = 8660 rad/s

---

### N4. GTO with βoff = 4 needs to turn off 400A. Find required negative gate current.
**Solution:**
IG(off) = IA/βoff = 400/4 = 100A

---

### N5. Snubber design: Vpeak = 600V, (dv/dt)max = 200 V/μs. Find Cs and Ps at 20 kHz.
**Solution:**
Cs = Vpeak/(dv/dt)max = 600/(200×10⁶) = 3 μF
Ps = 0.5 × Cs × V² × fsw = 0.5 × 3×10⁻⁶ × 600² × 20×10³
= 0.5 × 3×10⁻⁶ × 360000 × 20000 = 10.8W

---

## Assertion-Reason Type

### AR1. Assertion: Natural commutation is limited to AC circuits.
### Reason: Natural commutation relies on current zero-crossing which only occurs in AC.

**Answer: Both true, R is correct explanation.**
DC circuits have no current zero-crossing, requiring forced commutation.

---

### AR2. Assertion: Larger snubber capacitor provides better dv/dt protection.
### Reason: Larger capacitor requires smaller resistance for same damping.

**Answer: First true, R not necessarily true.**
Cs limits dv/dt but R is chosen for damping, not directly related to Cs size in that way.

---

## True/False

1. **T/F: Class B commutation uses series LC with load.**
**Answer: False.** Class B uses parallel LC tank across SCR, not series with load.

2. **T/F: GTO requires auxiliary commutation circuit.**
**Answer: False.** GTO turns off via gate pulse (Class F), no external commutation needed.

3. **T/F: Snubber resistor protects against di/dt.**
**Answer: False.** Snubber capacitor protects against dv/dt. Series inductor protects against di/dt.

---

## Fill in the Blanks

1. The process of turning off a conducting SCR is called __________.
**Answer: commutation**

2. __________ commutation uses AC line current zero-crossing.
**Answer: Natural (or line)**

3. Class B commutation uses __________ circuit to generate turn-off current pulse.
**Answer: resonant LC tank**

4. The minimum time for SCR to regain forward blocking is called __________ time.
**Answer: turn-off (tq)**

5. A __________ circuit limits dv/dt across SCR.
**Answer: snubber (RC)**
