# AC Bridges - Formulas

## 1. General AC Bridge Balance
```
Z₁Z₄ = Z₂Z₃

Separate into real and imaginary:
Real part equation = 0
Imaginary part equation = 0
```

## 2. Maxwell Bridge
```
Lₓ = R₂R₃C₄
Rₓ = R₂R₃/R₄
Q = ωLₓ/Rₓ = ωR₄C₄
```

## 3. Hay Bridge
```
Lₓ = R₂R₃C₄ / (1 + ω²R₄²C₄²)
Rₓ = R₂R₃R₄ω²C₄² / (1 + ω²R₄²C₄²)

When Q >> 1: Lₓ ≈ R₂R₃C₄ (same as Maxwell)
```

## 4. Anderson Bridge
```
Lₓ = C₃[R₂R₅R₃ + R₃R₄R₅] / R₄

With standard values and R₅:
Lₓ ≈ C₃R₂R₃    (when R₅ >> R₄)
```

## 5. Wien Bridge
```
Capacitance balance:
C₁ = C₄R₄(R₃/R₂) × 1/(1 + ω²R₁²C₁²)

Frequency (simplified for R₁=R₄=R, C₁=C₄=C):
f = 1/(2πRC)

General frequency:
f = 1/(2π√(R₁R₄C₁C₄))
```

## 6. Wien Bridge Oscillation Condition
```
For oscillation: R₂/R₃ = 2 (when R₁=R₄, C₁=C₄)
Feedback fraction: β = 1/3
Required amplifier gain: A ≥ 3
```

## 7. Schering Bridge
```
Cₓ = C₂ × (R₄/R₃)
tan δ = ωC₄R₄    (dissipation factor)

For loss angle: δ = arctan(ωC₄R₄)
```

## 8. Product/Arms Relations (Summary)
| Bridge | Balance (Real) | Balance (Imaginary) |
|--------|----------------|---------------------|
| Maxwell | RₓR₄ = R₂R₃ | Lₓ = R₂R₃C₄ |
| Hay | Rₓ(1+ω²R₄²C₄²) = R₂R₃R₄ω²C₄² | Lₓ = R₂R₃C₄/(1+ω²R₄²C₄²) |
| Schering | R₃/R₄ = C₂/Cₓ | ωC₄R₄ = tan δ |
| Wien | R₁R₄C₁C₄ω² = 1 | R₁C₁ = R₄C₄ |

## 9. AC Bridge Sensitivity
```
S_AC = ΔI_detector / (ΔZ/Z)

For equal arm bridges:
S ∝ V_source / (Z_detector + Z_bridge)
```

## 10. Quality Factor Relations
```
Q = ωL/R = 1/(ωCR)    (for series L-R or parallel C-R)

Maxwell bridge: Q = ωR₄C₄
For Q > 10, Hay bridge preferred over Maxwell
```

## 11. Dissipation Factor
```
D = tan δ = 1/Q = ωCR    (for parallel RC)
Loss angle δ = arctan(D)
```

## 12. Frequency Error in Hay Bridge
```
If actual frequency differs from nominal:
ΔL/L = -2(Δω/ω) × Q²/(1+Q²)
```

## 13. Stray Capacitance Effect
```
Guard ring potential = tap point potential
Eliminates stray C from measurement
Essential for Schering bridge accuracy
```

## Key Formulas for ISRO MCQs
| Bridge | Primary Formula |
|--------|-----------------|
| Maxwell | Lₓ = R₂R₃C₄, Rₓ = R₂R₃/R₄ |
| Hay | Lₓ = R₂R₃C₄/(1+ω²R₄²C₄²) |
| Wien (freq) | f = 1/(2πRC) |
| Schering | Cₓ = C₂(R₄/R₃), D = ωC₄R₄ |
| Anderson | Lₓ = C₃(R₂R₃R₅+R₃R₄R₅)/R₄ |
| General | Z₁Z₄ = Z₂Z₃ |
