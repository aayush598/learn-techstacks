# DC Bridges - Formulas

## 1. Wheatstone Bridge Balance
```
R₁/R₂ = R₃/R₄
R₁ × R₄ = R₂ × R₃ (opposite arms product)
```

## 2. Unknown Resistance
```
R₄ = R₃ × (R₂/R₁)    (using ratio arms)
```

## 3. Thévenin Equivalent at Detector
```
V_th = V_s × [R₄/(R₃+R₄) - R₂/(R₁+R₂)]

R_th = (R₁‖R₂) + (R₃‖R₄)
     = R₁R₂/(R₁+R₂) + R₃R₄/(R₃+R₄)
```

## 4. Detector Current (Unbalanced Bridge)
```
I_g = V_th / (R_th + R_g)
```

## 5. Bridge Sensitivity
```
S_B = ΔI_g / (ΔR₄/R₄)    (A per fractional change)

For small ΔR₄:
I_g ≈ V_s × ΔR₄ / [4R × (R_th + R_g)]
where R = R₁ = R₂ = R₃ = R₄ at balance (equal arm bridge)
```

## 6. Optimal Sensitivity
```
Maximum when: R₁ = R₂ = R₃ = R₄ = R
Then: R_th = R/2
I_g = V_s × (ΔR₄/R) / [4(R/2 + R_g)]
```

## 7. Kelvin Double Bridge
```
R_x = R_s × (P/Q)    when  p/q = P/Q

where:
P, Q = main ratio arms
p, q = auxiliary ratio arms
R_s = standard low resistance
```

## 8. Kelvin Bridge Lead Elimination
```
If p/q ≠ P/Q, error term:
Error ≈ R_x × (P/Q) × (pQ - qP)/(q(R_s + p + q))
This is negligible when p/q ≈ P/Q
```

## 9. Sensitivity for Different Ratio Arms
```
For ratio arms R₁/R₂ = k:
Sensitivity ∝ 1/(k + 1/k + 2) × V_s

Maximum when k = 1 (equal arms)
```

## 10. Wheatstone Bridge Accuracy
```
Relative error in R₄:
δR₄/R₄ = δR₃/R₃ + δ(R₂/R₁)

For ratio arms:
δ(R₂/R₁) = √[(δR₂/R₂)² + (δR₁/R₁)²]
```

## 11. Power Dissipation
```
P_total = V_s² / (R₁+R₂) + V_s² / (R₃+R₄)   (approximate)
For equal arms: P ≈ V_s² / R
```

## 12. Deflection Method (Small Unbalance)
```
I_g ≈ (V_s / 4R) × (ΔR/R)    for equal arm bridge
Sensitivity: S = V_s / (4R(R_th + R_g))
```

## 13. Bridge Excitation
```
DC: Battery (1.5V to 100V depending on application)
Higher voltage → higher sensitivity
But limited by power dissipation and self-heating
```

## Key Formulas for ISRO MCQs
| Quantity | Formula |
|----------|---------|
| Balance | R₁R₄ = R₂R₃ |
| Unknown | R₄ = R₃(R₂/R₁) |
| Thévenin V | V_s[R₄/(R₃+R₄) - R₂/(R₁+R₂)] |
| Thévenin R | R₁‖R₂ + R₃‖R₄ |
| Kelvin | R_x = R_s(P/Q) when p/q = P/Q |
| Detector I | I_g = V_th/(R_th + R_g) |
| Bridge S | S_B = ΔI_g/(ΔR/R) |
