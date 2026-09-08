# Routh-Hurwitz Criterion - Formulas

## 1. Characteristic Equation
A(s) = a_n s^n + a_{n-1} s^{n-1} + ... + a_1 s + a_0 = 0

Normalize so that a_n > 0 (multiply by -1 if needed).

## 2. Necessary Conditions (quick checks)
1. All coefficients a_i ≠ 0 (no missing terms).
2. All a_i > 0 (same sign).
If violated → unstable or roots on jω axis.

## 3. Routh Array Generation

### Rows 0-1 (from coefficients)
For a 5th order: a₅s⁵+a₄s⁴+a₃s³+a₂s²+a₁s+a₀
- Row s⁵:  a₅, a₃, a₁
- Row s⁴:  a₄, a₂, a₀

### Row s³
b₁ = (a₄·a₃ - a₅·a₂)/a₄
b₂ = (a₄·a₁ - a₅·a₀)/a₄
b₃ = 0

### Row s²
c₁ = (b₁·a₂ - a₄·b₂)/b₁
c₂ = (b₁·a₀ - a₄·0)/b₁ = a₀

### Row s¹
d₁ = (c₁·b₂ - b₁·c₂)/c₁

### Row s⁰
e₁ = c₂

### General Rule (any row entry)
element = (cross product of first-column element above and column element, minus another cross product) / first-column element of the row one above.

## 4. Stability Criterion
- **Stable** ⇔ ALL first-column entries > 0.
- **Number of RHP roots** = number of sign changes in the first column.

## 5. Special Case 1: Zero in First Column
Replace 0 with **ε** (small positive). Continue the array. Determine sign changes as ε→0⁺.

Example: If array row becomes [ε, a, b], signs depend on whether ε terms flip.

## 6. Special Case 2: Row of Zeros
- Locate row sᵏ that is all zeros.
- The row directly above (sᵏ⁺¹) defines the **auxiliary equation** A(s).

### Auxiliary Equation
A(s) = a_{k+1}s^{k+1} + a_{k-1}s^{k-1} + ...... (even powers only)

### Replace zero row with derivative coefficients
A'(s) = dA(s)/ds
Use the derivative coefficients as the new row sᵏ.

### Roots from auxiliary equation
Solve A(s) = 0 → the symmetric roots (e.g., ±jω, ±a±jb).
These are roots on the imaginary axis (marginal) or symmetric pairs.

## 7. Marginal Stability Frequency
If A(s) = s² + ω² with roots ±jω, the system oscillates at ω (rad/s).
Frequency in Hz: f = ω/(2π).

## 8. Gain (K) Range for Stability

### Unity feedback: char. eq. = 1 + G(s) = 0
1 + K(s+z).../(s^n+...) = 0 → bring to polynomial form, treat K symbolically.

### Procedure
1. Form characteristic equation as polynomial in s with K.
2. Build Routh array; first column entries are functions of K.
3. Require all > 0 → solve inequalities for K.
4. Intersection gives K_min < K < K_max.
5. At K = K_max (or K_min), the system is marginally stable.
6. Frequency at margin = |Imaginary root| from auxiliary equation.

## 9. Key Third-Order Condition
For s³ + a₂s² + a₁s + a₀ = 0:
**Stable iff: a₂a₁ > a₀** (and all coefficients positive).

## 10. Useful Second-Order Condition
For s² + a₁s + a₀ = 0: Always stable (if a₁, a₀ > 0). No Routh needed.

## 11. Routh Array for nth Order (compact)
Row s^n:   a_n   a_{n-2}  a_{n-4} ...
Row s^{n-1}: a_{n-1} a_{n-3} a_{n-5} ...
Row s^{n-2}: b₁ b₂ b₃ ...
  b₁ = (a_{n-1}·a_{n-2} - a_n·a_{n-3})/a_{n-1}
  b₂ = (a_{n-1}·a_{n-4} - a_n·a_{n-5})/a_{n-1}
  ...
Row continues similarly downward.

## 12. Relating to Marginal/Unstable Roots Count
- Zero row → auxiliary roots on jω axis or symmetric.
- After replacing, continue; sign changes in first column = number of RHP roots.
- Roots on jω axis do NOT change first-column signs but indicate non-strict stability (marginal).

## Formula Cheatsheet
| Quantity | Formula |
|---|---|
| Stability | all first column > 0 |
| RHP roots | # sign changes in first column |
| Auxiliary A(s) | even poly from row above zero row |
| New zero-row | A'(s) coefficients |
| Marginal freq | root of A(s)=0 (imag part) |
| 3rd order stable | a₂a₁ > a₀ |
| 2nd order stable | always if coeffs > 0 |
