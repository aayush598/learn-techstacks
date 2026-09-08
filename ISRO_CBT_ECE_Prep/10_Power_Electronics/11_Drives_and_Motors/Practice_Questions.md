# Drives and Motors - Practice Questions

## Multiple Choice Questions

### Q1. DC motor speed is directly proportional to:
(a) Armature current
(b) Field flux
(c) Armature voltage
(d) Armature resistance

**Answer: (c)**
n = (Va - IaRa)/(kΦ). Speed is proportional to armature voltage (numerator).

---

### Q2. In V/f control of induction motor, keeping V/f constant maintains:
(a) Constant speed
(b) Constant power
(c) Constant flux
(d) Constant slip

**Answer: (c)**
V/f = constant → Φ = constant (flux remains at rated value).

---

### Q3. A 4-pole induction motor at 50 Hz has synchronous speed of:
(a) 3000 RPM
(b) 1500 RPM
(c) 1000 RPM
(d) 750 RPM

**Answer: (b)**
ns = 120f/p = 120 × 50/4 = 1500 RPM

---

### Q4. Regenerative braking in DC motor drives requires:
(a) Type A chopper
(b) Type B chopper
(c) Type D chopper
(d) Type E chopper

**Answer: (b)**
Type B (second quadrant) chopper allows power flow from motor back to source.

---

### Q5. The starting current of an induction motor with direct-on-line starting is:
(a) Equal to rated current
(b) 2-3× rated current
(c) 5-7× rated current
(d) 10-15× rated current

**Answer: (c)**
DOL starting draws 5-7× rated current due to low impedance at standstill.

---

### Q6. In field weakening region of DC motor:
(a) Torque is constant
(b) Power is constant
(c) Speed is constant
(d) Current is constant

**Answer: (b)**
Above base speed: flux reduced, voltage constant → power = T × ω ≈ constant.

---

### Q7. Slip of induction motor at synchronous speed is:
(a) 1
(b) 0.5
(c) 0
(d) -1

**Answer: (c)**
s = (ns - n)/ns. At n = ns: s = 0.

---

### Q8. V/f control is preferred for induction motors because:
(a) It gives highest efficiency
(b) It maintains constant flux
(c) It's the simplest method
(d) It gives highest starting torque

**Answer: (b)**
Constant V/f maintains constant flux, giving constant torque below base speed.

---

### Q9. Star-delta starting reduces starting current by:
(a) 1/2
(b) 1/3
(c) 1/√3
(d) √3 times

**Answer: (b)**
Istar = Idelta/√3 = Istart(DOL)/3. Reduces to 1/3 of DOL current.

---

### Q10. Maximum torque of induction motor is:
(a) At starting (s=1)
(b) At slip = R2/X2
(c) At synchronous speed (s=0)
(d) Independent of slip

**Answer: (b)**
Breakdown torque occurs at slip sm = R2/X2 (approximately).

---

### Q11. The power saving with V/f control for fan load at 80% speed is approximately:
(a) 20%
(b) 49%
(c) 80%
(d) 10%

**Answer: (b)**
Fan load: P ∝ n³. At 80% speed: P = 0.8³ = 0.512 → saving = 49%.

---

### Q12. Soft starter uses __________ for voltage control:
(a) Diodes
(b) Thyristors
(c) MOSFETs
(d) Relays

**Answer: (b)**
Soft starters use anti-parallel thyristors to control firing angle and output voltage.

---

### Q13. The efficiency of a DC motor is highest at:
(a) No-load
(b) Half-load
(c) Full-load
(d) Starting

**Answer: (c)**
DC motor efficiency increases with load, reaching maximum near full-load.

---

### Q14. Vector control provides speed range of:
(a) 1:10
(b) 1:100
(c) 1:1000
(d) 1:2

**Answer: (b)**
Vector control provides 100:1 speed range with good dynamic response.

---

### Q15. The torque of induction motor is proportional to:
(a) V²
(b) V
(c) 1/V
(d) V³

**Answer: (a)**
T ∝ V²/s (approximately). Doubling voltage quadruples torque.

---

### Q16. In a chopper-fed DC drive, the armature current ripple depends on:
(a) Only inductance
(b) Only switching frequency
(c) Both L and fsw
(d) Neither L nor fsw

**Answer: (c)**
ΔIL = Vin × D × (1-D)/(Lfsw). Both L and fsw affect ripple.

---

### Q17. Dynamic braking of DC motor dissipates energy in:
(a) Source battery
(b) Braking resistor
(c) Motor armature
(d) External capacitor

**Answer: (b)**
Dynamic braking connects motor to resistor, converting kinetic energy to heat.

---

### Q18. The base speed of a DC motor occurs at:
(a) Zero voltage
(b) Rated voltage and rated flux
(c) Half rated voltage
(d) Double rated flux

**Answer: (b)**
Base speed: maximum speed at rated voltage and rated flux (field not weakened).

---

### Q19. At very low frequencies, V/f control requires voltage boost because:
(a) Motor saturates
(b) Stator resistance drop becomes significant
(c) Slip increases
(d) Efficiency decreases

**Answer: (b)**
At low frequency, I×R drop in stator becomes significant fraction of applied voltage, reducing flux.

---

### Q20. The most efficient method of induction motor speed control is:
(a) Rotor resistance control
(b) Pole changing
(c) V/f control with inverter
(d) Slip power recovery

**Answer: (c)**
V/f control with inverter provides wide speed range with high efficiency (minimal losses).

---

## Numerical Problems

### N1. A DC motor has Ra = 0.5Ω, kΦ = 0.1 V/RPM. At Va = 200V, find no-load speed.
**Solution:**
At no-load: Ia ≈ 0
n = Va/(kΦ) = 200/0.1 = 2000 RPM

---

### N2. A 4-pole induction motor runs at 1440 RPM at 50 Hz. Find slip and frequency of rotor current.
**Solution:**
ns = 120 × 50/4 = 1500 RPM
s = (1500-1440)/1500 = 0.04 (4%)
fr = s × f = 0.04 × 50 = 2 Hz

---

### N3. A chopper-fed DC motor has Vin = 200V, D = 0.7, kΦ = 0.08 V/RPM, Ra = 0.3Ω, Ia = 20A. Find speed.
**Solution:**
Va = D × Vin = 0.7 × 200 = 140V
n = (Va - IaRa)/(kΦ) = (140 - 20 × 0.3)/0.08 = (140-6)/0.08 = 134/0.08 = 1675 RPM

---

### N4. V/f control: rated 400V, 50Hz motor operates at 30Hz. Find applied voltage.
**Solution:**
V = Vrated × (f/frated) = 400 × (30/50) = 400 × 0.6 = 240V

---

### N5. DC motor: Va = 220V, Ia = 30A, Ra = 0.4Ω, n = 1500 RPM. Find torque and efficiency.
**Solution:**
E = Va - IaRa = 220 - 30 × 0.4 = 208V
Pmech = E × Ia = 208 × 30 = 6240W
ω = 2π × 1500/60 = 157.08 rad/s
T = Pmech/ω = 6240/157.08 = 39.7 Nm
η = Pmech/(Va × Ia) = 6240/(220 × 30) = 6240/6600 = 94.5%

---

## Assertion-Reason Type

### AR1. Assertion: V/f control maintains constant torque below base speed.
### Reason: Constant V/f maintains constant flux, and torque ∝ flux × current.

**Answer: Both true, R is correct explanation.**
With constant flux, torque is proportional to current. Current limited by drive rating, giving constant torque capability.

---

### AR2. Assertion: Field weakening reduces maximum torque.
### Reason: Torque ∝ flux × current, and flux is reduced in field weakening.

**Answer: Both true, R is correct explanation.**
Reduced flux at constant current gives lower torque (but higher speed, maintaining constant power).

---

## True/False

1. **T/F: DC motor speed is directly proportional to armature current.**
**Answer: False.** Speed is inversely proportional to flux and proportional to (Va - IaRa), not directly to Ia.

2. **T/F: V/f control can achieve speeds below rated speed.**
**Answer: True.** By reducing both V and f proportionally.

3. **T/F: Star-delta starting provides full starting torque.**
**Answer: False.** Starting torque is 1/3 of DOL torque.

---

## Fill in the Blanks

1. The __________ of an induction motor is the difference between synchronous speed and actual speed.
**Answer: slip**

2. __________ speed is the speed of rotating magnetic field in induction motor.
**Answer: synchronous**

3. Above base speed, DC motor operates in __________ region.
**Answer: field weakening (or constant power)**

4. The most efficient method for induction motor speed control is __________.
**Answer: V/f control (or inverter-fed)**

5. __________ starting reduces both starting current and torque to 1/3 of DOL values.
**Answer: Star-delta**
