# ISRO CBT ECE - Power Electronics Shortcuts

## 1. DC-DC Converter Quick Reference

### Buck (Step-Down)
```
Vo = D × Vin
Vo < Vin always
D = Vo/Vin
```

### Boost (Step-Up)
```
Vo = Vin/(1-D)
Vo > Vin always
D = 1 - Vin/Vo
```

### Buck-Boost
```
Vo/Vin = D/(1-D)
Vo can be >, <, or = Vin
Polarity inverted
```

### Flyback (Isolated Buck-Boost)
```
Vo = Vin × (N2/N1) × D/(1-D)
```

### Memory Trick: "Buck Down, Boost Up, Buck-Boost Both"
- Buck: Vo = D × Vin (multiply by D < 1)
- Boost: Vo = Vin/(1-D) (divide by 1-D < 1)
- Buck-Boost: D/(1-D) ratio

## 2. Rectifier Quick Formulas

### Single-Phase
```
Half-wave:     Vdc = Vm/π,        FF = 1.57, RF = 1.21
Full-wave:     Vdc = 2Vm/π,       FF = 1.11, RF = 0.482
Bridge:        Vdc = 2Vm/π,       FF = 1.11, RF = 0.482
```

### Three-Phase
```
Half-wave:     Vdc = 3√3Vm/(2π)
Full bridge:   Vdc = 3Vml/π       FF ≈ 1.0,  RF = 0.04
```

### Memory Trick: "1-2-3" for Rectifier Vdc
- Half-wave: Vm × (1/π) = 0.318Vm
- Full-wave: Vm × (2/π) = 0.636Vm
- Three-phase: Vm × (3/π) = 0.955Vm (full bridge)

## 3. SCR Formulas

### Controlled Rectifier Output
```
Half-wave:     Vdc = Vm/(2π) × (1 + cos α)
Full-wave:     Vdc = Vm/π × (1 + cos α)
Three-phase:   Vdc = 3Vml/π × cos α (for α ≤ 60°)
```

### Key Relationships
```
IL (latching) > IH (holding) always
IL ≈ 2-3 × IH
SCR turns off when: IA < IH
```

### Memory Trick: "Latching needs more than Holding"
- IL > IH
- IL needed to start, IH to maintain

## 4. Inverter Output Formulas

### Single-Phase
```
Half-bridge:   V1(peak) = 2Vm/π = 0.637Vm
Full-bridge:   V1(peak) = 4Vm/π = 1.27Vm
```

### Three-Phase (180° conduction)
```
VLL1(peak) = 2√3Vm/π = 1.1Vm (line-to-line)
Vph1(peak) = Vm/π = 0.318Vm (phase)
```

### THD Values
```
Square wave (single):     48.3%
6-step three-phase:       31.1%
SPWM:                     3-5%
SVM:                      2-4%
```

## 5. Chopper Formulas

### Type A (Buck): Vo = D × Vin
### Type B (Boost): Vo = Vin/(1-D)
### Step-Up: M = 1/(1-D)

```
D = 0.5 → M = 2 (boost)
D = 0.8 → M = 5 (boost)
D = 0.9 → M = 10 (boost)
```

### Memory Trick: "D=0.8 gives 5× boost"
- 1/(1-0.8) = 5
- Common exam value

## 6. Induction Motor Quick Calcs

### Synchronous Speed
```
ns = 120f/p
50 Hz: 4-pole → 1500 RPM
50 Hz: 2-pole → 3000 RPM
60 Hz: 4-pole → 1800 RPM
```

### Slip
```
s = (ns - n)/ns
n = ns(1-s)
```

### Common Slip Values
```
Rated slip: 2-5%
At 1440 RPM (4-pole, 50Hz): s = 4%
At 2850 RPM (2-pole, 50Hz): s = 5%
```

## 7. Commutation Classes Quick Reference

```
Class A: Load commutation (series RLC, underdamped)
Class B: Resonant pulse (parallel LC tank)
Class C: Complementary (two SCRs)
Class D: Auxiliary voltage (capacitor reverse bias)
Class E: Auxiliary current (SCR diverts current)
Class F: External pulse (GTO gate turn-off)
```

### Memory Trick: "ABCD-EF"
- A: Auto (load has RLC)
- B: Bounce (LC resonant pulse)
- C: Complement (two SCRs)
- D: Dump (capacitor dumps voltage)
- E: Extract (current extracted)
- F: Force (gate forced turn-off)

## 8. PWM Techniques Quick Comparison

```
SPWM:     ma = Vref/Vcarrier, Vo1 = ma × Vin
SVM:      15% higher DC utilization than SPWM
SHE:      N angles eliminate N-1 harmonics
Unipolar: First harmonics at 2fsw
Bipolar:  First harmonics at fsw
```

### Memory Trick: "Unipolar is uni-formly better"
- Unipolar: 2fsw (better harmonics)
- Bipolar: fsw (worse harmonics)

## 9. Efficiency Quick Reference

```
Half-wave rectifier:    40.6%
Full-wave rectifier:    81.2%
Three-phase bridge:     99.9%
Linear regulator:       Vo/Vin (e.g., 5/12 = 42%)
SMPS:                   85-95%
```

### Memory Trick: "40-80-100" for rectifier efficiency
- Half: 40%
- Full: 80%
- Three-phase: 100% (approximately)

## 10. Critical Design Values

### For CCM/DCM Boundary
```
Buck:     LC = (1-D)R/(2fsw)
Boost:    LC = D(1-D)²R/(2fsw)
```

### For Snubber Design
```
Cs = Vpeak/(dv/dt)max
Rs = √(Ls/Cs) for critical damping
```

### For Filter Design (Full-Wave Rectifier)
```
C = Iload/(2f × ΔV)
Example: 1A, 50Hz, 1V ripple → C = 10,000 μF
```

## 11. ISRO-Specific Values

### Derating Factors
```
Voltage: 80% of rated (20% margin)
Current: 75-80% of rated
Temperature: Tj(max) - 25°C margin
```

### Common Exam Values
```
Vm = √2 × Vrms (for 230V AC: Vm = 325V)
For 415V 3-phase: Vml = √2 × 415 = 587V
VT = 26 mV at 300K
```

### Quick Conversions
```
1 HP = 746 W
1 kVA = 1000 VA
Power factor = cos φ (for resistive load: PF = 1)
```

## 12. Most Likely ISRO Questions

### Top 10 Formulas to Memorize
1. Buck: Vo = D × Vin
2. Boost: Vo = Vin/(1-D)
3. Full-wave rectifier: Vdc = 2Vm/π
4. Three-phase full bridge: Vdc = 3Vml/π
5. SCR controlled: Vdc = (2Vm/π) cos α (full bridge)
6. Induction motor: ns = 120f/p
7. Slip: s = (ns-n)/ns
8. V/f control: V = Vrated × (f/frated)
9. THD = √(Vrms² - V1²)/V1
10. T = kΦIa (DC motor torque)

### Top 5 Concepts to Understand
1. SCR two-transistor analogy and latching condition
2. Commutation classes (especially A-F)
3. CCM vs DCM in DC-DC converters
4. PWM comparison (SPWM vs SVM vs SHE)
5. Four-quadrant chopper operation
