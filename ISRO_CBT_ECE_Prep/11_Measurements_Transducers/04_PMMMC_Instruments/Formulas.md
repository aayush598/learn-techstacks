# PMMC Instruments - Formulas

## 1. Deflecting Torque
```
T_d = NBIA sin(θ)
For radial field: T_d = NBIA  (constant, independent of θ)
N = number of turns
B = magnetic flux density (Wb/m²)
I = current through coil (A)
A = area of coil (m²)
```

## 2. Controlling Torque (Spring)
```
T_c = kθ
k = torsional stiffness of spring (N·m/rad)
θ = angular deflection (rad)
```

## 3. Damping Torque (Eddy Current)
```
T_m ∝ (velocity of coil) × B² × (conductivity of former)
Eddy current power: P_eddy ∝ B² × A² × ω² / R_eddy
```

## 4. Steady-State Deflection
```
T_d = T_c
NBIA = kθ
θ = (NBA/k) × I

Full-scale deflection: θ_max = NBAI_m/k
```

## 5. Shunt Resistance (Ammeter)
```
R_sh = (R_m × I_m) / (I - I_m)

or equivalently:
R_sh = R_m / (n - 1)  where n = I/I_m (multiplying power)
```

## 6. Multiplier Resistance (Voltmeter)
```
R_s = (V / I_m) - R_m

or: R_s = R_m(V/V_m - 1)

where V_m = I_m × R_m (full-scale voltage of movement)
```

## 7. Voltmeter Sensitivity
```
S_v = R_v / V_range  (Ω/V)
S_v = 1 / I_m  (since R_v = V/I_m for ideal)

For R_m = 100Ω, I_m = 50μA:
S_v = 1/50μA = 20 kΩ/V
```

## 8. Ayrton (Universal) Shunt
```
For multi-range ammeter with shunt resistance R_sh:
I_range = I_m × (R_sh_total / R_sh_active)

For n ranges:
R₁ + R₂ + ... + Rₙ = R_sh_total
Each range uses partial shunt
```

## 9. Current Multiplying Factor
```
m = I/I_m = (R_sh + R_m) / R_sh = 1 + R_m/R_sh

Required shunt: R_sh = R_m / (m - 1)
```

## 10. Voltage Multiplying Factor
```
M = V/V_m = (R_s + R_m) / R_m = 1 + R_s/R_m

Required series: R_s = R_m(M - 1)
```

## 11. Temperature Compensation
```
Temperature affects both B and k:
B = B₀(1 + α_B × ΔT)    (α_B < 0 for most magnets)
k = k₀(1 + α_k × ΔT)    (α_k > 0 for springs)

Net effect: errors partially cancel
Best compensation when α_B ≈ -α_k
```

## 12. Power Consumption
```
P = I²R = I_m² × R_m (at full scale)
For voltmeter: P = V²/R_v
Higher sensitivity → lower power consumption
```

## 13. Torque-to-Weight Ratio
```
T/W = (NBIA) / (mg × r)
Higher T/W → better performance (less friction error)
Typical: T/W = 10-15 for good PMMC
```

## 14. Damping Factor
```
Damping ratio: ζ = c / (2√(Jk))
c = damping coefficient
J = moment of inertia
For critical damping: ζ = 1
For PMMC: typically ζ = 0.5-0.8 (slightly underdamped)
```

## Key Formulas for ISRO MCQs
| Quantity | Formula |
|----------|---------|
| Deflection | θ = NBAI/k |
| Shunt | R_sh = R_m/(n-1), n = I/I_m |
| Multiplier | R_s = R_m(V/V_m - 1) |
| Sensitivity | S = 1/I_m (Ω/V) |
| Full scale | θ_max = NBAI_m/k |
| Power | P = V²/R_v = I_m²R_m |
