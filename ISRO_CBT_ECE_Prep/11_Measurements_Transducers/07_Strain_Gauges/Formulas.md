# Strain Gauges - Formulas

## 1. Gauge Factor
```
GF = (ΔR/R) / ε

ΔR/R = GF × ε
ε = (ΔR/R) / GF

Typical GF = 2.0 for metallic gauges
```

## 2. Strain
```
ε = ΔL/L = stress/E = σ/E

where:
E = Young's modulus (Pa)
σ = stress (Pa)
ε = dimensionless (mm/mm)

Microstrain: 1 με = 10⁻⁶ mm/mm
```

## 3. Quarter Bridge Output
```
V_out = (V_s/4) × (ΔR/R) = (V_s/4) × GF × ε

Sensitivity: S_q = V_s × GF / 4  (V per unit strain)
```

## 4. Half Bridge Output
```
V_out = (V_s/2) × (ΔR/R) = (V_s/2) × GF × ε

Two active gauges: one in tension (+ε), one in compression (-ε)
Total output: V_out = V_s/2 × GF × ε
```

## 5. Full Bridge Output
```
V_out = V_s × GF × ε

Four active gauges: two in tension, two in compression
Maximum sensitivity: S_f = V_s × GF
```

## 6. Temperature Compensation (Dummy Gauge)
```
Active gauge: ΔR_a/R = GF × ε + α × ΔT
Dummy gauge:  ΔR_d/R = α × ΔT (no mechanical strain)

In bridge: V_out ∝ (ΔR_a - ΔR_d) = GF × ε × R
Temperature effects cancel.
```

## 7. Lead Wire Compensation
```
For long lead wires with resistance R_L:
Effective bridge arm = R_gauge + 2R_L

Bridge output reduced by factor:
Correction = R_gauge / (R_gauge + 2R_L)

For R_gauge = 120Ω, R_L = 10Ω:
Correction = 120/140 = 0.857 (14.3% error)
```

## 8. Bridge Sensitivity
```
S = V_out / ε = (V_s/4) × GF  (quarter bridge)

For V_s = 5V, GF = 2:
S = 5/4 × 2 = 2.5 V/unit strain
S = 2.5 mV/με
```

## 9. Apparent Strain
```
ε_apparent = α_s × ΔT + (TCR/GF) × ΔT

where:
α_s = coefficient of thermal expansion of specimen
TCR = temperature coefficient of resistance of gauge
Match α_s to minimize apparent strain
```

## 10. Gauge Resistance Change
```
ΔR = R × GF × ε

For R = 350Ω, GF = 2, ε = 1000 με:
ΔR = 350 × 2 × 10⁻³ = 0.7Ω
```

## 11. Bridge Unbalance Voltage
```
V_unbalance = V_s × [R₁/(R₁+R₂) - R₃/(R₃+R₄)]

For quarter bridge with ΔR:
V_unbalance ≈ V_s × ΔR/(4R) for small ΔR
```

## 12. Power Dissipation
```
P = V_s² / R_total

For V_s = 5V, R = 350Ω:
P = 25/350 = 71.4 mW

Self-heating error: ΔT = P × θ_jc
θ_jc = thermal resistance (°C/mW)
```

## 13. Strain from Bridge Output
```
ε = (4 × V_out) / (V_s × GF)    (quarter bridge)
ε = (2 × V_out) / (V_s × GF)    (half bridge)
ε = V_out / (V_s × GF)           (full bridge)
```

## Key Formulas for ISRO MCQs
| Quantity | Formula |
|----------|---------|
| Gauge factor | GF = (ΔR/R)/ε |
| Quarter bridge | V_out = V_s/4 × GF × ε |
| Half bridge | V_out = V_s/2 × GF × ε |
| Full bridge | V_out = V_s × GF × ε |
| Strain | ε = ΔL/L = σ/E |
| ΔR | ΔR = R × GF × ε |
| Temp compensation | Dummy gauge in adjacent arm |
