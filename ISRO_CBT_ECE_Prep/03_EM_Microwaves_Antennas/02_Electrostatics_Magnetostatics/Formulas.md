# Electrostatics & Magnetostatics - Formulas

## Fundamental Constants
| Constant | Symbol | Value |
|----------|--------|-------|
| Permittivity of free space | ε₀ | 8.854 × 10⁻¹² F/m |
| Permeability of free space | μ₀ | 4π × 10⁻⁷ H/m |
| Elementary charge | e | 1.602 × 10⁻¹⁹ C |
| Speed of light | c | 3 × 10⁸ m/s |

---

## Electrostatics Formulas

### Coulomb's Law
```
F = (1/4πε₀) × (q₁q₂/r²) × âᵣ
F = (q₁q₂)/(4πε₀εᵣr²) × âᵣ  (in dielectric)
```

### Electric Field (E) - Point Charge
```
E = Q/(4πε₀r²) âᵣ
E = -∇V (gradient relationship)
```

### Electric Field - Charge Distributions
```
Line charge:    E = ρₗ/(2πε₀ρ) âᵨ
Surface charge: E = ρₛ/(2ε₀) âₙ
Volume charge:  E = ρᵥr/(3ε₀) âᵣ  (sphere)
```

### Electric Flux
```
ψ = ∮ E·dA = Q_enclosed/ε₀  (Gauss's Law)
D = ε₀E + P = εE
ψ = ∮ D·dA = Q_enclosed
```

### Electric Potential
```
V = -∫ E·dl
V = Q/(4πε₀r)  (point charge)
V = (1/4πε₀)∫(ρᵥ/r)dV
```

### Energy Storage
```
W_e = ½CV² = ½QV = ½Q²/C
Energy density: w_e = ½ε|E|² = ½D·E
```

### Capacitance
```
C = Q/V
Parallel plate:     C = εA/d
Coaxial cable:      C = 2πεL/ln(b/a)
Sphere:             C = 4πε(ab)/(b-a)
Parallel: C_eq = C₁ + C₂ + ...
Series:  1/C_eq = 1/C₁ + 1/C₂ + ...
```

### Boundary Conditions (Dielectrics)
```
E₁ₜ = E₂ₜ  (tangential E continuous)
D₁ₙ - D₂ₙ = ρₛ  (normal D discontinuity)
ε₁E₁ₙ - ε₂E₂ₙ = ρₛ
```

---

## Magnetostatics Formulas

### Biot-Savart Law
```
dB = (μ₀/4π) × (I dl × âᵣ)/r²
B = (μ₀/4π)∫(I dl × âᵣ)/r²
```

### Magnetic Field Distributions
```
Infinite wire:   B = μ₀I/(2πρ) â𝜙
Solenoid:        B = μ₀nI (inside, n = N/l)
Toroid:          B = μ₀NI/(2πρ) (inside)
Circular loop:   B = μ₀IR²/(2(R²+z²)^(3/2)) âₖ
```

### Ampere's Circuital Law
```
∮ H·dl = I_enclosed
∇ × H = J  (differential form)
H = B/μ
```

### Magnetic Flux
```
Φ = ∫ B·dA
Φ = LI/N  (for inductance)
```

### Inductance
```
L = λ/I = NΦ/I
Solenoid:    L = μ₀N²A/l
Coaxial:     L = (μ₀l/2π)ln(b/a)
Parallel: 1/L_eq = 1/L₁ + 1/L₂ + ...
Series:    L_eq = L₁ + L₂ + ...
```

### Magnetic Energy
```
W_m = ½LI² = ½Φ²/L
Energy density: w_m = ½B·H = ½μ|H|²
```

### Boundary Conditions (Magnetic)
```
B₁ₙ = B₂ₙ  (normal B continuous)
H₁ₜ - H₂ₜ = K  (tangential H discontinuity)
μ₁H₁ₙ = μ₂H₂ₙ
```

---

## Force Formulas
```
Lorentz force:    F = q(v × B)
Force on wire:    F = I∫(dl × B)
Torque:           τ = m × B,  m = NIA âₙ
Hall voltage:     V_H = BI/(nqb)
```

---

## Key Unit Conversions
| Quantity | SI Unit | Gaussian Equivalent |
|----------|---------|---------------------|
| E field | V/m | statV/cm |
| B field | Tesla | Gauss (1T = 10⁴ G) |
| D field | C/m² | esu/cm² |
| H field | A/m | Oersted |
| Permittivity | F/m | (dimensionless in Gaussian) |

---

## Quick Numerical Values
```
ε₀ = 8.854 × 10⁻¹² F/m ≈ 1/(36π × 10⁹) F/m
μ₀ = 4π × 10⁻⁷ H/m = 1.257 × 10⁻⁶ H/m
1/(4πε₀) = 9 × 10⁹ N·m²/C²
μ₀/(4π) = 10⁻⁷ H/m
```

---

## Inductance of Common Geometries
```
Straight wire:     L = (μ₀l/2π)[ln(2l/r) - 1]  (l >> r)
Rectangular loop:  L ≈ 2μ₀a/π [ln(2a/b) - 0.77]
Circular loop:     L = μ₀R[ln(8R/r) - 2]
```
