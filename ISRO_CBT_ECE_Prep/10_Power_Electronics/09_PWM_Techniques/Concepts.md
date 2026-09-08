# PWM Techniques - Concepts

## 1. Sinusoidal PWM (SPWM)

### Basic Principle
- Carrier signal (high-frequency triangle) compared with reference (sine wave)
- When reference > carrier: switch ON
- When reference < carrier: switch OFF
- Output voltage fundamental follows reference sine wave

### Modulation Index
```
ma = Vref(peak)/Vcarrier(peak)

ma < 1: linear modulation
ma = 1: maximum linear output
ma > 1: overmodulation (increased harmonics)
```

### Frequency Modulation Ratio
```
mf = fcarrier/fref = fsw/f1

Typical: mf = 15-25 for motor drives
Higher mf → better harmonics but higher switching losses
```

### Types of SPWM
1. **Bipolar switching**: Two switches per leg, complementary operation
2. **Unipolar switching**: Four switches, independent leg control
3. **Hybrid PWM**: Combines bipolar and unipolar

### Harmonic Content
- Harmonics appear at: n×fsw ± k×f1
- Bipolar: harmonics at fsw, 2fsw, 3fsw...
- Unipolar: first harmonics at 2fsw (better)
- Low-order harmonics (3rd, 5th, 7th) significantly reduced

## 2. Unipolar Switching

### Principle
- Each leg controlled independently
- Leg A: reference compared with carrier
- Leg B: inverted reference compared with carrier
- Output voltage = Va - Vb

### Advantages
- First harmonics at 2fsw (effective frequency doubling)
- Lower THD than bipolar
- Smaller output filter needed
- Reduced switching losses per device

### Switching Sequence
```
Positive half-cycle: Q1 PWM, Q4 always ON
Negative half-cycle: Q3 PWM, Q2 always ON
Result: unipolar voltage waveform
```

## 3. Bipolar Switching

### Principle
- Diagonal switches operate together
- Q1/Q4 ON → +Vin
- Q2/Q3 ON → -Vin
- No zero states

### Output Voltage
- Switches between +Vin and -Vin
- Fundamental: V1 = ma × Vin
- Simple control but higher harmonics

### Comparison with Unipolar
| Aspect | Bipolar | Unipolar |
|--------|---------|----------|
| Switching states | 2 (+Vin, -Vin) | 3 (+Vin, 0, -Vin) |
| First harmonics | fsw | 2fsw |
| THD | Higher | Lower |
| Control | Simpler | More complex |
| Device stress | Same | Same |

## 4. Selective Harmonic Elimination (SHE)

### Principle
- Pre-calculated switching angles
- Eliminates specific low-order harmonics
- Solves non-linear equations for angles
- Lower switching frequency than SPWM

### Quarter-Wave Symmetry
- Angles: α1, α2, α3...
- Symmetric about 90° and quarter-wave symmetric
- Reduces number of equations

### Constraint Equations
```
For N angles:
(1/N) × Σ[cos(nαk)] = M/2    [fundamental, n=1]
(1/N) × Σ[cos(nαk)] = 0       [harmonics n=5,7,11...]

Where M = modulation index (0 to 1)
```

### Harmonics Eliminated
- N angles eliminate N-1 harmonics
- Example: 3 angles eliminate 5th and 7th
- 5 angles eliminate 5th, 7th, 11th, 13th

### Advantages
- Very low THD (<1% achievable)
- Lower switching losses (fewer switchings)
- Good for high-power applications
- Computationally intensive (offline)

## 5. Space Vector Modulation (SVM)

### Principle
- Represents three-phase voltages as space vector in α-β plane
- 8 switching states (6 active + 2 zero)
- Reference vector rotated at fundamental frequency
- Adjacent active states used to synthesize reference

### Switching States
```
State 0: Q2,Q4,Q6 ON → zero vector
State 1: Q1 ON → active vector at 0°
State 2: Q1,Q3 ON → active vector at 60°
State 3: Q3 ON → active vector at 120°
State 4: Q3,Q5 ON → active vector at 180°
State 5: Q5 ON → active vector at 240°
State 6: Q5,Q6 ON → active vector at 300°
State 7: Q1,Q3,Q5 ON → zero vector
```

### Reference Vector
```
Vref = Vα + jVβ
|Vref| = √(Vα² + Vβ²)
θ = arctan(Vβ/Vα)
```

### Switching Times Calculation
```
For sector 1 (0° to 60°):
T1 = (√3 × Ts × |Vref|/Vin) × sin(60° - θ)
T2 = (√3 × Ts × |Vref|/Vin) × sin(θ)
T0 = Ts - T1 - T2

Where Ts = switching period
```

### DC Bus Utilization
```
Vo1(max) = Vin/√3 = 0.577 Vin (per phase)
Ratio to SPWM: (Vin/√3)/(Vin/2) = 2/√3 = 1.155 (15.5% improvement)
```

### Advantages
- 15% higher DC bus utilization than SPWM
- Lower THD for same switching frequency
- Better dynamic response
- Easy to implement digitally

## 6. Comparison of PWM Techniques

| Parameter | SPWM | Unipolar | Bipolar | SHE | SVM |
|-----------|------|----------|---------|-----|-----|
| THD | 3-5% | 2-4% | 5-8% | <1% | 2-4% |
| DC utilization | 78.5% | 78.5% | 78.5% | 78.5% | 100% |
| Switching freq | High | High | High | Low | High |
| Complexity | Low | Medium | Low | High | Medium |
| Digital impl. | Easy | Easy | Easy | Hard | Easy |
| Dynamic response | Good | Good | Good | Slow | Excellent |

## 7. Overmodulation

### When ma > 1
- Reference exceeds carrier peaks
- Output approaches square wave
- Fundamental increases but harmonics increase
- Transition from PWM to six-step operation

### Overmodulation Region
```
ma = 1: Vo1 = Vin (linear limit)
ma = 1.15: Vo1 = 1.15Vin (SVM limit)
ma → ∞: Vo1 → 4Vin/π = 1.27Vin (square wave)
```

## 8. ISRO-Specific Focus

- PWM technique selection for motor drives
- THD requirements for power quality
- Switching frequency trade-offs (losses vs harmonics)
- Digital implementation on DSP/FPGA
- Radiation effects on PWM control circuits
- EMI considerations for spacecraft
