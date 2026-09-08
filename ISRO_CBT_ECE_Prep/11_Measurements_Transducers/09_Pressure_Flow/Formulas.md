# Pressure and Flow Transducers - Formulas

## 1. Venturi Meter Discharge
```
Q = C_d × A_t × √[2(P₁-P₂)/ρ(1-β⁴)]

where:
C_d = coefficient of discharge (0.95-0.99)
A_t = throat area = πd²/4
β = d/D (throat to pipe diameter ratio)
ρ = fluid density
P₁-P₂ = differential pressure
```

## 2. Orifice Plate Discharge
```
Q = C_d × A_o × √[2(P₁-P₂)/ρ(1-β⁴)]

where:
A_o = orifice area = πd²/4
C_d = 0.60-0.65 (lower than Venturi)
β = d/D (typically 0.2-0.7)
```

## 3. Pitot Tube Velocity
```
v = √[2(P_stag - P_static)/ρ] = √[2ΔP/ρ]

v = √[2gh]  (when ΔP = ρgh)
```

## 4. Bernoulli's Equation
```
P₁ + ½ρv₁² + ρgh₁ = P₂ + ½ρv₂² + ρgh₂

For horizontal: P₁ + ½ρv₁² = P₂ + ½ρv₂²
```

## 5. Continuity Equation
```
A₁v₁ = A₂v₂ = Q
v₂ = v₁ × (A₁/A₂) = v₁ × (D/d)²
```

## 6. Throat Velocity (Venturi)
```
v₂ = v₁ / β²    (from continuity)
For β = 0.5: v₂ = 4v₁
```

## 7. Pressure Drop
```
Venturi: ΔP = ½ρ(v₂² - v₁²) = ½ρv₁²(1/β⁴ - 1)
Orifice: Similar but with different C_d
```

## 8. Reynolds Number
```
Re = ρvD/μ = vD/ν

where:
ν = kinematic viscosity (m²/s)
μ = dynamic viscosity (Pa·s)
D = pipe diameter (m)
```

## 9. Piezoelectric Transducer
```
Charge: q = d₃₃ × F = d₃₃ × P × A
Voltage: V = q/C = d₃₃ × P × A / C

where:
d₃₃ = piezoelectric coefficient (C/N)
P = pressure (Pa)
A = electrode area (m²)
C = capacitance (F)
```

## 10. Capacitive Pressure Sensor
```
C = εA/d

For small gap change Δd:
ΔC/C ≈ -Δd/d = Δd/(d₀)  (for small changes)

Or with diaphragm:
ΔC ∝ pressure × sensitivity
```

## 11. Discharge Coefficient
```
C_d = Q_actual / Q_ideal

Venturi: C_d = 0.95-0.99 (high efficiency)
Orifice: C_d = 0.60-0.65 (low, due to vena contracta)
Nozzle:  C_d = 0.96-0.99
```

## 12. Flow Velocity Profile
```
Turbulent: v_avg ≈ 0.82 × v_max
Laminar:   v_avg = 0.5 × v_max (parabolic)
```

## 13. Differential Pressure to Flow
```
Q = K × √(ΔP)

K = calibration constant
Square root relationship: doubling ΔP → √2 increase in Q
```

## 14. Rotameter
```
For vertical tapered tube:
Q ∝ h (float height)
Linear relationship (unlike Venturi)
```

## 15. Head Loss
```
Venturi: h_L ≈ 10-15% of ΔP (low loss)
Orifice: h_L ≈ 40-60% of ΔP (high loss)
```

## Key Formulas for ISRO MCQs
| Measurement | Formula |
|-------------|---------|
| Venturi Q | Q = C_d × A_t × √[2ΔP/ρ(1-β⁴)] |
| Orifice Q | Q = C_d × A_o × √[2ΔP/ρ(1-β⁴)] |
| Pitot v | v = √(2ΔP/ρ) |
| Bernoulli | P₁ + ½ρv₁² = P₂ + ½ρv₂² |
| Continuity | A₁v₁ = A₂v₂ |
| Piezo charge | q = d₃₃ × P × A |
