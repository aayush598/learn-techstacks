# ISRO CBT ECE - Power Electronics Memory Tricks

## 1. DC-DC Converter Memory Tricks

### Buck Converter
```
"Buck goes DOWN like a deer"
Vo = D × Vin (D < 1, so Vo < Vin)
```

### Boost Converter
```
"Boost goes UP like a rocket"
Vo = Vin/(1-D) (denominator < 1, so Vo > Vin)
```

### Buck-Boost
```
"Buck-Boost goes BOTH ways but INVERTS"
Vo/Vin = D/(1-D), polarity reversed
```

### Flyback
```
"Flyback = Buck-Boost with wings (transformer)"
Vo = Vin × (N2/N1) × D/(1-D)
```

### Quick Duty Cycle Values
```
D = 0.5: Buck → Vo = 0.5Vin, Boost → Vo = 2Vin
D = 0.75: Buck → Vo = 0.75Vin, Boost → Vo = 4Vin
D = 0.8: Boost → Vo = 5Vin (common exam value!)
D = 0.9: Boost → Vo = 10Vin
```

## 2. Rectifier Memory Tricks

### Vdc Values (Single-Phase)
```
"Half = 1/π, Full = 2/π"
Half-wave: Vdc = Vm/π = 0.318Vm
Full-wave: Vdc = 2Vm/π = 0.636Vm
```

### Form Factor
```
"Full wave is 1.11 (one-one)"
FF = 1.11 for full-wave
FF = 1.57 for half-wave
```

### Ripple Factor
```
"Full wave ripple is almost half (0.482)"
RF = 0.482 for full-wave
RF = 1.21 for half-wave (more than 1 = bad!)
```

### PIV Ratings
```
"Center tap PIV = 2Vm (double trouble)"
"Bridge PIV = Vm (single)"
```

## 3. SCR Memory Tricks

### Two-Transistor Analogy
```
"Alpha 1 + Alpha 2 = 1 → LATCH!"
When α1 + α2 = 1, anode current → ∞ (latches ON)
```

### Latching vs Holding Current
```
"Latching > Holding always"
IL (start) > IH (maintain)
Think: "You need more effort to START a car than to KEEP it running"
```

### SCR Firing Angle Formulas
```
"Half = (1+cosα)/2, Full = (1+cosα)"
Half-wave: Vdc = Vm/(2π) × (1+cosα)
Full-wave: Vdc = Vm/π × (1+cosα)
Three-phase: Vdc = 3Vml/π × cosα (no "+1"!)
```

### Commutation Classes
```
"ABCDEF" = Load, Resonant, Complementary, Voltage, Current, Force
A = Auto (load resonance)
B = Bounce (LC pulse)
C = Complement (two SCRs)
D = Dump (capacitor reverse voltage)
E = Extract (current diversion)
F = Force (GTO gate)
```

## 4. Inverter Memory Tricks

### Fundamental Output
```
"Single Full = 4/π = 1.27"
"Three Phase = 2√3/π = 1.1"
```

### THD Hierarchy
```
"Worst to Best: Square > Six-step > SPWM > SVM > SHE"
48% > 31% > 4% > 3% < 1%
```

### Modulation Index
```
"ma < 1: Linear, ma = 1: Max linear, ma > 1: Overmodulation"
```

### SVM Advantage
```
"SVM = 15% more voltage than SPWM"
SVM Vo1(max) = Vin/√3 = 0.577Vin
SPWM Vo1(max) = Vin/2 = 0.5Vin
Ratio = 1.155 (15.5% improvement)
```

## 5. Chopper Memory Tricks

### Quadrant Operation
```
"Type A: Only DOWN (buck)"
"Type B: Only UP (boost/regen)"
"Type C: UP or DOWN (two quadrant)"
"Type D: FORWARD or REVERSE (voltage bidirectional)"
"Type E: EVERYTHING (four quadrant)"
```

### Step-Up Gain
```
"D=0.5 → Gain=2, D=0.8 → Gain=5, D=0.9 → Gain=10"
M = 1/(1-D)
```

### Jones Chopper
```
"Jones = Auto-transformer + Capacitor"
Auto-transformer provides voltage boost
Capacitor provides forced commutation
```

## 6. Induction Motor Memory Tricks

### Synchronous Speed
```
"120 × Frequency / Poles"
50 Hz, 4-pole: 120×50/4 = 1500 RPM
50 Hz, 2-pole: 120×50/2 = 3000 RPM
60 Hz, 4-pole: 120×60/4 = 1800 RPM
```

### Slip
```
"Slip = 1 at start, 0 at sync speed"
s = 1: standstill (n=0)
s = 0: synchronous speed (n=ns)
s = 0.04: rated operation (typical)
```

### V/f Control
```
"V over f = Constant = Flux"
V/f = constant → constant flux → constant torque
Above base speed: V constant, f increases → flux decreases → constant power
```

### Starting Current
```
"DOL start = 5-7× rated"
"Star-Delta = 1/3 of DOL"
"V/f start = controlled"
```

## 7. Power Formula Memory Tricks

### Power Triangle
```
"P = VI cosφ (single phase)"
"P = √3 VI cosφ (three phase)"
"Q = VI sinφ (reactive)"
"S = VI (apparent)"
```

### Efficiency
```
"Linear: η = Vo/Vin (simple ratio)"
"SMPS: η = 85-95% (high)"
"Rectifier: 40%, 80%, 100% (half, full, three-phase)"
```

### Power Loss
```
"Conduction: I²R (MOSFET) or Vce(sat)×I (IGBT)"
"Switching: 0.5×V×I×(tON+tOFF)×f"
"Gate: Qg×Vg×f"
```

## 8. Thermal Management Memory Tricks

### Junction Temperature
```
"Tj = Ta + P × Rth"
"Rth total = Rth(j-c) + Rth(c-s) + Rth(s-a)"
```

### Derating
```
"Derate by 20-25% for reliability"
"Vop ≤ 0.8 × Vrated"
"Iop ≤ 0.8 × Irated"
```

### Heatsink Selection
```
"Required Rth = (Tj(max) - Ta)/P - Rth(j-c)"
```

## 9. ISRO-Specific Memory Tricks

### Most Tested Topics
```
1. DC-DC converter output formulas (Vo = D/(1-D)×Vin)
2. SCR firing circuits and commutation classes
3. Rectifier average voltage formulas
4. Induction motor V/f control
5. Inverter PWM techniques and harmonics
```

### Common Exam Patterns
```
"Boost converter with D=0.75: Vo = 4Vin"
"Three-phase full bridge: Vdc = 3Vml/π"
"SCR full bridge: Vdc = (2Vm/π)cosα"
"Induction motor 4-pole 50Hz: ns = 1500 RPM"
"THD of six-step: 31.1%"
```

### Quick Numerical Tricks
```
Vm = √2 × Vrms ≈ 1.414 × Vrms
For 230V: Vm = 325V (memorize!)
For 415V 3-phase: Vml = 587V (memorize!)
π ≈ 3.14, √2 ≈ 1.414, √3 ≈ 1.732
```

### Comparison Tricks
```
"MOSFET vs IGBT: MOSFET for <200V, IGBT for >600V"
"SPWM vs SVM: SVM gives 15% more voltage"
"CCM vs DCM: CCM for high power, DCM for light load"
```

## 10. Formula Derivation Memory Tricks

### Deriving Boost Vo
```
"Energy balance: Pin = Pout"
Vin × IL = Vo × Io
IL = Io/(1-D) (from inductor volt-second balance)
Substitute: Vin × Io/(1-D) = Vo × Io
Therefore: Vo = Vin/(1-D)
```

### Deriving Buck Vo
```
"Inductor volt-second balance"
During ON: (Vin-Vo) × ton
During OFF: -Vo × toff
Balance: (Vin-Vo)×ton = Vo×toff
Solve: Vo = D × Vin
```

### Deriving Three-Phase Full Bridge Vdc
```
"6 pulses per cycle, each 60°"
Average of 6 segments of line voltage
Vdc = 3√3Vm/π = 3Vml/π
```

## 11. Quick Reference Cards

### Card 1: DC-DC Converters
```
Buck:     Vo = D×Vin           (D<1)
Boost:    Vo = Vin/(1-D)       (D<1)
Buck-Boo: Vo = D/(1-D)×Vin     (inverted)
Flyback:  Vo = (N2/N1)×D/(1-D)×Vin
```

### Card 2: Rectifiers
```
1φ Half:    Vm/π,   FF=1.57, RF=1.21
1φ Full:    2Vm/π,  FF=1.11, RF=0.482
3φ Half:    3√3Vm/(2π)
3φ Full:    3Vml/π, FF≈1.0,  RF=0.04
```

### Card 3: Inverters
```
1φ Full SW:  V1 = 4Vm/π
3φ Full SW:  VLL1 = 2√3Vm/π
SPWM:        V1 = ma×Vin
SVM:         V1 = Vin/√3 (max)
```

### Card 4: Motors
```
ns = 120f/p
s = (ns-n)/ns
n = ns(1-s)
V/f = constant (constant torque)
```

### Card 5: Protection
```
dv/dt: Cs = V/(dv/dt)max
di/dt: Ls = V/(di/dt)max
Snubber: Ps = 0.5×Cs×V²×fsw
```

## 12. Last-Minute Revision Checklist

### Must-Know Formulas
- [ ] Buck: Vo = D×Vin
- [ ] Boost: Vo = Vin/(1-D)
- [ ] Full-wave: Vdc = 2Vm/π
- [ ] Three-phase bridge: Vdc = 3Vml/π
- [ ] SCR bridge: Vdc = (2Vm/π)cosα
- [ ] ns = 120f/p
- [ ] s = (ns-n)/ns
- [ ] T = kΦIa (DC motor)
- [ ] V/f = constant (induction motor)
- [ ] THD = √(Vrms²-V1²)/V1

### Must-Know Concepts
- [ ] SCR latching condition (α1+α2=1)
- [ ] Commutation classes (A-F)
- [ ] CCM vs DCM boundary
- [ ] PWM comparison (SPWM vs SVM)
- [ ] Four-quadrant chopper operation
- [ ] V/f control principle
- [ ] Freewheeling diode purpose
- [ ] Snubber circuit design

### Common Mistakes to Avoid
- [ ] Forgetting √2 in Vm calculations
- [ ] Confusing buck and boost formulas
- [ ] Using wrong FF/RF formulas
- [ ] Mixing up latching and holding current
- [ ] Forgetting polarity in buck-boost
- [ ] Using phase voltage instead of line voltage
- [ ] Confusing 50Hz and 60Hz calculations
