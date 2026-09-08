# Inverters - Formulas

## 1. Single-Phase Half-Bridge Inverter Formulas

### Output Voltage
```
Vo(peak) = Vin/2
Vo(rms) = Vin/2   [square wave]

Fundamental component:
V1(peak) = (2/π) × Vin/2 = Vin/π
V1(rms) = Vin/(π√2)
```

### THD
```
THD = √(Vrms² - V1²)/V1
THD = √((Vin/2)² - (Vin/(π√2))²) / (Vin/(π√2))
THD = √(π²/8 - 1) / (1/√2) = 0.483 (48.3%)
```

### Output Power
```
Po = Vo(rms)² / RL = (Vin/2)² / RL   [resistive load]

For fundamental:
P1 = V1(rms)² / RL = (Vin/(π√2))² / RL
```

## 2. Single-Phase Full-Bridge Inverter Formulas

### Square Wave Operation
```
Vo(peak) = Vin
Vo(rms) = Vin   [square wave]

Fundamental:
V1(peak) = 4Vin/π = 1.27Vin
V1(rms) = 4Vin/(π√2) = 0.9Vin
```

### THD (Square Wave)
```
THD = √(Vin² - (4Vin/(π√2))²) / (4Vin/(π√2))
THD = √(1 - 8/π²) / (4/(π√2)) = 0.483 (48.3%)
```

### Bipolar PWM
```
Vo(fundamental, peak) = ma × Vin   [ma = modulation index]
Vo(rms) = ma × Vin / √2

Harmonics at: n × fsw ± k × f1
Where n = 1,2,3,... and k = 1,3,5,...
```

### Unipolar PWM
```
Vo(fundamental, peak) = ma × Vin   [same as bipolar]
Harmonics at: 2n × fsw ± k × f1  [first harmonics at 2fsw]
Better harmonic performance than bipolar
```

## 3. Three-Phase VSI Formulas (180° Conduction)

### Line-to-Line Voltage
```
VLL(rms) = Vin × √(2/3) = 0.816 Vin   [6-step]
VLL(peak) = Vin

Fundamental:
VLL1(peak) = (2√3/π) × Vin = 1.1 Vin
VLL1(rms) = (2√3/(π√2)) × Vin = 0.78 Vin
```

### Phase Voltage (Star Load)
```
Vph(rms) = Vin/√3 × √(2/3) = Vin/3 × √2 = 0.471 Vin   [6-step]

Fundamental:
Vph1(peak) = Vin/π = 0.318 Vin
Vph1(rms) = Vin/(π√2) = 0.225 Vin
```

### THD (6-Step Line Voltage)
```
THD = √(VLL(rms)² - VLL1(rms)²) / VLL1(rms)
THD = √(0.816² - 0.78²) / 0.78 = 0.311 (31.1%)
```

### Output Power (Three-Phase)
```
P = 3 × Vph(rms) × IL(rms) × cos φ
P = √3 × VLL(rms) × IL(rms) × cos φ
```

## 4. SPWM Formulas

### Fundamental Output Voltage
```
Vo1(peak) = ma × Vin/2   [half-bridge]
Vo1(peak) = ma × Vin     [full-bridge]

ma = Vref(peak)/Vcarrier(peak)
0 ≤ ma ≤ 1: linear range
```

### RMS Output Voltage
```
Vo(rms) = ma × Vin / (2√2)   [half-bridge]
Vo(rms) = ma × Vin / √2       [full-bridge]
```

### Harmonic Distribution
```
Harmonics at:
fc = switching frequency (carrier)
Sidebands: fc ± 2f1, fc ± 4f1, ...
2fc ± f1, 2fc ± 3f1, ...

For bipolar PWM: harmonics at fc, 2fc, 3fc...
For unipolar PWM: harmonics at 2fc, 4fc... (first at 2fc)
```

### DC Bus Utilization
```
Maximum linear output (SPWM):
Vo1(max) = Vin/2   [half-bridge]
Vo1(max) = Vin     [full-bridge]

DC utilization = Vo1(max)/Vin = 100% (full-bridge)
```

## 5. Space Vector Modulation (SVM) Formulas

### Reference Vector
```
Vref = Vα + jVβ   [in α-β plane]

Magnitude: |Vref| = √(Vα² + Vβ²)
Angle: θ = arctan(Vβ/Vα)
```

### Maximum Output Voltage
```
Vo1(max) = Vin/√3 = 0.577 Vin   [per phase]
Vo1(max) = Vin                    [line-to-line peak]

DC bus utilization: 100% (better than SPWM's 78.5%)
Vo1(max) = Vin/√3 × 2/√3 = 2Vin/3   [6-step maximum]
```

### Switching Times
```
T1 = (√3 × Ts × Vo/Vin) × sin(60° - θ)   [active vector 1]
T2 = (√3 × Ts × Vo/Vin) × sin(θ)         [active vector 2]
T0 = Ts - T1 - T2                        [zero vector]

Where Ts = switching period, θ = angle within sector
```

### THD Comparison
```
SPWM:  THD ≈ 3-5% (at ma = 0.8, fsw = 20f1)
SVM:   THD ≈ 2-4% (same conditions)
SHE:   THD < 1% (with harmonic elimination)
```

## 6. Selective Harmonic Elimination (SHE) Formulas

### Switching Angles
```
For quarter-wave symmetry:
α1, α2, α3... (N angles)

Constraint equations:
(1/N) × Σ[cos(nαk)] = M/2   [for fundamental, n=1]
(1/N) × Σ[cos(nαk)] = 0     [for harmonics n=5,7,11,...]

Solve N equations for N angles
```

### Harmonic Elimination
```
N angles eliminate N-1 harmonics
Example: 3 angles eliminate 5th and 7th harmonics
THD with SHE: < 1% (theoretical)
```

## 7. Inverter Efficiency

### Efficiency Formula
```
η = Po / (Po + Ploss)
η = Po / (Po + Pcond + Psw + Pfilter)

Pcond = I² × Rds(on) × D   [conduction losses]
Psw = 0.5 × V × I × (tON + tOFF) × fsw   [switching losses]
```

### Typical Efficiencies
```
Square wave inverter: 95-98%
SPWM inverter: 92-96%
SVM inverter: 93-97%
```

### THD vs Efficiency Trade-off
```
Higher fsw → lower THD but higher switching losses
Optimal fsw depends on application requirements
Motor inductance helps filter harmonics
```

## 8. Useful Relationships

### Modulation Index Range
```
SPWM:   0 ≤ ma ≤ 1 (linear)
         ma > 1: overmodulation (increased harmonics)
SVM:     0 ≤ ma ≤ 1.15 (compared to SPWM)
         Better DC bus utilization
```

### Harmonic Amplitudes (Square Wave)
```
Vn/V1 = 1/n   [for odd harmonics]
V3/V1 = 1/3 = 33.3%
V5/V1 = 1/5 = 20%
V7/V1 = 1/7 = 14.3%
```

### Filter Design
```
LC filter cutoff: fc = 1/(2π√(LC))
fc should be: f1 << fc << fsw
Typically: fc ≈ 10 × f1 to fsw/5
```
