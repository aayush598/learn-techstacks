# AC Bridges - Concepts

## 1. AC Bridge General Principle
AC bridges extend DC bridge concepts to measure inductance, capacitance, and their quality factors.
At balance: Z₁Z₄ = Z₂Z₃ (complex impedance product of opposite arms equal)
This gives TWO equations: Real = 0 and Imaginary = 0.

## 2. General AC Bridge Notation
Standard arrangement:
- Arm 1: Z₁ (unknown)
- Arm 2: Z₂ (standard impedance)
- Arm 3: Z₃ (ratio arm, usually pure resistance)
- Arm 4: Z₄ (standard impedance, variable)

At balance: Z₁ = Z₂Z₃/Z₄

## 3. Maxwell Inductance Bridge

### 3.1 Purpose
Measures unknown inductance Lₓ and its resistance Rₓ using a standard capacitor.

### 3.2 Configuration
- Arm 1: Lₓ in series with Rₓ (unknown)
- Arm 2: R₂ (known resistance)
- Arm 3: R₃ (known resistance)
- Arm 4: C₄ in parallel with R₄

### 3.3 Balance Equations
```
Lₓ = R₂R₃C₄
Rₓ = R₂R₃/R₄
Quality factor: Q = ωLₓ/Rₓ = ωR₄C₄
```

### 3.4 Suitable For
Medium Q coils (Q > 10)

## 4. Hay Bridge

### 4.1 Purpose
Measures high-Q inductors (Q > 10).

### 4.2 Difference from Maxwell
In Hay bridge, C₄ is in SERIES with R₄ (not parallel).

### 4.3 Balance Equations
```
Lₓ = R₂R₃C₄/(1 + ω²R₄²C₄²)
Rₓ = R₂R₃R₄ω²C₄²/(1 + ω²R₄²C₄²)
```

### 4.4 Note
At balance, Lₓ and Rₓ depend on frequency ω → frequency must be known precisely.

## 5. Anderson Bridge

### 5.1 Purpose
More accurate than Maxwell for inductance measurement.

### 5.2 Configuration
Uses a standard capacitor C and additional resistance R₅ in series with it.

### 5.3 Balance Equations
```
Lₓ = C[R₂R₅R₃ + R₃R₄R₅]/R₄  (simplified)
```
Anderson bridge has 6 arms but better accuracy than Maxwell.

## 6. Wien Bridge

### 6.1 Purpose
Measures unknown capacitance and frequency.
Wien bridge oscillator uses it for frequency determination.

### 6.2 Configuration
- Arm 1: R₁ in series with C₁
- Arm 4: R₄ in parallel with C₄
- Arms 2, 3: Pure resistances R₂, R₃

### 6.3 Balance Equations
```
For capacitance measurement:
C₁ = R₄C₄ × (R₃/R₂)   (at specific frequency)

For frequency measurement (Wien oscillator):
f = 1/(2π√(R₁R₄C₁C₄))

When R₁ = R₄ = R and C₁ = C₄ = C:
f = 1/(2πRC)
```

### 6.4 Wien Bridge Oscillator
Uses Wien bridge in feedback path for sinusoidal oscillation.
Condition for oscillation: R₂/R₃ = 2 (or gain = 3)

## 7. Schering Bridge

### 7.1 Purpose
Measures capacitance and dissipation factor (loss tangent).

### 7.2 Configuration
- Arm 1: Unknown Cₓ with loss resistance
- Arm 2: Standard capacitor C₂ (loss-free)
- Arm 3: R₃ (pure resistance)
- Arm 4: C₄ in parallel with R₄

### 7.3 Balance Equations
```
Cₓ = C₂ × (R₄/R₃)
Dissipation factor: D = tan δ = ωC₄R₄
```

### 7.4 Suitable For
Precision capacitance measurement, cable capacitance, insulation testing.

## 8. Product/Arm Relationships
General principle: Opposite arms product = Adjacent arms product.
For ANY AC bridge: Z₁Z₄ = Z₂Z₃
Separate real and imaginary parts.

## 9. Bridge Sensitivity (AC)
```
S_AC = ΔI_d / (ΔZ/Z)
```
Depends on:
- Source frequency and amplitude
- Detector sensitivity
- Arm impedance values
- Frequency stability

## 10. Comparison Table of AC Bridges
| Bridge | Measures | Key Components | Best For |
|--------|----------|----------------|----------|
| Maxwell | L, R | C‖R | Medium Q coils |
| Hay | L, R | C series R | High Q coils |
| Anderson | L, R | C, extra R | High accuracy |
| Wien | C, f | RC series-parallel | Frequency measurement |
| Schering | C, D | C‖R | Loss measurement |

## 11. Shielding and Guarding
AC bridges are sensitive to stray capacitances.
Guard rings and shielding prevent errors from parasitic capacitances.
Schering bridge requires careful guarding for accurate D measurement.

## 12. ISRO Focus Areas
- Maxwell bridge balance equations (Lₓ = R₂R₃C₄)
- Wien bridge frequency formula
- Schering bridge dissipation factor
- Which bridge for which measurement
- Frequency dependence in Hay bridge
