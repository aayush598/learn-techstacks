# PWM Techniques - Formulas

## 1. Sinusoidal PWM (SPWM) Formulas

### Fundamental Output Voltage
```
Half-bridge: Vo1(peak) = ma × Vin/2
Full-bridge: Vo1(peak) = ma × Vin

ma = Vref(peak)/Vcarrier(peak)
```

### RMS Output Voltage
```
Half-bridge: Vo1(rms) = ma × Vin/(2√2)
Full-bridge: Vo1(rms) = ma × Vin/√2
```

### Harmonic Distribution
```
Harmonics at: n×fsw ± k×f1

n = 1,2,3... (carrier multiples)
k = 0,1,2,3... (sidebands)

Dominant harmonics near fsw with sidebands
```

### Modulation Index Range
```
0 ≤ ma ≤ 1: linear region
ma = 1: maximum linear output
ma > 1: overmodulation
```

### THD Calculation
```
THD = √(Vo(rms)² - Vo1(rms)²) / Vo1(rms) × 100%

For SPWM with ma = 0.8, fsw = 20f1:
THD ≈ 3-5%
```

## 2. Unipolar Switching Formulas

### Output Voltage
```
Vo = Va - Vb

Va: PWM output of leg A
Vb: PWM output of leg B (inverted reference)

Fundamental: Vo1(peak) = ma × Vin
```

### Harmonic Spectrum
```
First harmonics at: 2fsw ± k×f1
Effective switching frequency = 2fsw

Lower THD than bipolar for same fsw
```

### Switching States per Cycle
```
Bipolar: 2 switchings per carrier cycle per leg
Unipolar: 1 switching per carrier cycle per leg
But: 4 switches total vs 2 in bipolar
```

## 3. Bipolar Switching Formulas

### Output Voltage
```
Vo = +Vin or -Vin (alternating)

Fundamental: Vo1(peak) = ma × Vin

Harmonics at: fsw, 2fsw, 3fsw...
```

### THD
```
THD(bipolar) > THD(unipolar) for same fsw

Approximate: THD_bipolar ≈ 1.5 × THD_unipolar
```

## 4. Selective Harmonic Elimination (SHE) Formulas

### Switching Angles
```
For quarter-wave symmetry with N angles:
α1, α2, α3... αN

Constraint equations:
(1/π) × ∫[0 to π] f(α) dα = M/2   [fundamental]
(1/π) × ∫[0 to π] f(α) × sin(nθ) dα = 0   [harmonics]
```

### Fundamental Component
```
V1(peak) = (4/π) × Vin × Σ[(-1)^(k+1) × cos(αk)]   [for half-bridge]

Simplified:
V1(peak) = (2/π) × Vin × (1 - 2×Σ[cos(αk)])
```

### Harmonic Elimination
```
For N angles:
Eliminates harmonics: 5th, 7th, 11th... up to (2N-1)th

Example:
N=3: eliminates 5th, 7th
N=5: eliminates 5th, 7th, 11th, 13th
N=7: eliminates 5th, 7th, 11th, 13th, 17th, 19th
```

### THD with SHE
```
THD ≈ 1-3% (depending on N)
Lower than SPWM (3-5%) at same fundamental voltage
```

### Switching Frequency
```
fsw(SHE) ≈ N × f1   [much lower than SPWM]
SPWM: fsw = mf × f1 (mf = 15-25)
SHE: fsw = N × f1 (N = 3-7 typically)
```

## 5. Space Vector Modulation (SVM) Formulas

### Reference Vector
```
Vref = Vα + jVβ
|Vref| = √(Vα² + Vβ²)
θ = arctan(Vβ/Vα)
Sector = floor(θ/60°) + 1
```

### Switching Times (Sector 1: 0° to 60°)
```
T1 = (√3 × Ts × |Vref|/Vin) × sin(60° - θ)
T2 = (√3 × Ts × |Vref|/Vin) × sin(θ)
T0 = Ts - T1 - T2

Ts = 1/fsw = switching period
```

### Maximum Output Voltage
```
Vo1(max) = Vin/√3 = 0.577 Vin (per phase peak)
Vo1(rms) = Vin/√6 = 0.408 Vin (per phase RMS)

DC bus utilization: 100% (vs SPWM's 78.5%)
```

### Overmodulation
```
|Vref| > Vin/√3: overmodulation region
Output approaches six-step waveform
Vo1(max) → 2Vin/π = 0.637 Vin (per phase peak)
```

### THD
```
THD(SVM) ≈ 2-4% (at ma = 0.8, fsw = 20f1)
Better than SPWM by 10-20%
```

## 6. Overmodulation Formulas

### Linear to Square Wave Transition
```
ma = 1: Vo1 = Vin (linear limit)
ma = 1.15: Vo1 = 1.15Vin (SVM limit)
ma → ∞: Vo1 → 4Vin/π = 1.27Vin (square wave, full-bridge)

For half-bridge:
ma → ∞: Vo1 → 2Vin/π = 0.637Vin
```

### Harmonic Increase
```
At ma = 1: THD ≈ 3-5%
At ma = 1.5: THD ≈ 15-20%
At ma = 2 (near square wave): THD ≈ 48%
```

## 7. THD Comparison Formulas

### Theoretical THD Values
```
Square wave: THD = 48.3% (single-phase)
6-step three-phase: THD = 31.1% (line voltage)
SPWM (ma=0.8): THD ≈ 3-5%
Unipolar (ma=0.8): THD ≈ 2-4%
SVM (ma=0.8): THD ≈ 2-4%
SHE (N=5): THD ≈ 1-2%
```

### THD vs Switching Frequency Trade-off
```
Higher fsw → lower THD (more harmonic pushing)
But: higher switching losses

Optimal: fsw where THD meets requirement with minimum losses
```

## 8. Switching Loss Formulas

### Per-Switch Loss
```
Psw = 0.5 × V × I × (tON + tOFF) × fsw
```

### Total Inverter Loss
```
Ploss = 6 × Psw(per switch) + Pcond(total)
Ploss = 6 × [0.5 × Vin × I × (tON + tOFF) × fsw] + Pcond
```

### THD vs Loss Trade-off
```
For same THD:
SPWM requires higher fsw → higher losses
SVM provides same THD at lower fsw → lower losses
SHE provides lowest THD at lowest fsw → lowest losses
```

## 9. Useful Relationships

### Modulation Index Conversions
```
SPWM: ma = Vref/Vcarrier
SVM: ma = |Vref|/(Vin/√3)

To convert SVM ma to SPWM ma:
ma(SVM) = ma(SPWM) × (2/√3) = 1.155 × ma(SPWM)
```

### Frequency Relationships
```
SPWM: fsw = mf × f1 (mf = 15-25)
SVM: fsw = N × f1 (N = 10-20)
SHE: fsw = N × f1 (N = 3-7)

For same f1, SHE has lowest fsw
```

### Output Voltage Range
```
SPWM: 0 to Vin (full-bridge)
SVM: 0 to Vin/√3 × √3 = Vin (per phase, line-to-line)
SHE: 0 to Vin (linear region)
```
