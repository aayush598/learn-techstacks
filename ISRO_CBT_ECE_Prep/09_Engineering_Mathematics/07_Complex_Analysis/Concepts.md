# Complex Analysis - Concepts

## 1. Complex Numbers Basics

### Definition
```
z = x + iy, where i² = -1
x = Re(z), y = Im(z)
|z| = √(x² + y²) = modulus
arg(z) = arctan(y/x) = argument
```

### Polar Form
```
z = r(cos θ + i sin θ) = re^(iθ)
r = |z|, θ = arg(z)
```

### De Moivre's Theorem
```
[cos θ + i sin θ]^n = cos(nθ) + i sin(nθ)
z^n = r^n e^(inθ)
```

### nth Roots
```
z^(1/n) = r^(1/n) e^(i(θ + 2kπ)/n) for k = 0, 1, ..., n-1
```

---

## 2. Analytic Functions

### Definition
- f(z) is **analytic** at z₀ if f'(z₀) exists in some neighborhood
- **Entire**: analytic everywhere in ℂ
- **Singular**: not analytic at some point

### Cauchy-Riemann Equations
```
f(z) = u(x,y) + iv(x,y)

Analytic ⟺ CR equations hold:
∂u/∂x = ∂v/∂y
∂u/∂y = -∂v/∂x

f'(z) = ∂u/∂x + i∂v/∂x = ∂v/∂y - i∂u/∂y
```

### Harmonic Functions
- If f(z) is analytic, then u and v are harmonic
- u_xx + u_yy = 0 (Laplace equation)
- v_xx + v_yy = 0

### Conjugate Harmonic Functions
- u and v satisfy CR equations
- v is conjugate harmonic of u
- Given u, find v using CR equations

---

## 3. Conformal Mapping

### Definition
- Mapping preserves angles between curves
- Analytic function with f'(z₀) ≠ 0 is conformal at z₀

### Important Mappings
```
w = z + c: Translation
w = cz: Rotation and scaling
w = z²: Doubles angles at origin
w = 1/z: Inversion (circle to circle)
w = e^z: Maps strips to sectors
w = sin(z): Maps strips to half-planes
w = (z-a)/(z-b): Möbius transformation
```

### Möbius Transformations
```
w = (az + b)/(cz + d), ad - bc ≠ 0

Maps circles/lines to circles/lines
Three points determine the transformation
```

### Linear Fractional Transformations
```
w = (az + b)/(cz + d)

Fixed points: solve w = z
Conjugate points map to conjugate points
```

---

## 4. Complex Integration

### Line Integral
```
∫_C f(z) dz = ∫_a^b f(z(t)) z'(t) dt

where z = z(t), a ≤ t ≤ b
```

### Cauchy's Integral Theorem
```
If f(z) is analytic inside and on simple closed curve C:
∮_C f(z) dz = 0
```

### Cauchy's Integral Formula
```
f(z₀) = (1/(2πi)) ∮_C f(z)/(z - z₀) dz

where C is simple closed curve, z₀ inside C
```

### Generalized Cauchy Formula
```
f^(n)(z₀) = (n!/(2πi)) ∮_C f(z)/(z - z₀)^(n+1) dz
```

---

## 5. Residues

### Definition
- Residue of f(z) at isolated singularity z₀ is coefficient of (z-z₀)^(-1) in Laurent series
- Res(f, z₀) = a₋₁

### Residue at Simple Pole
```
Res(f, z₀) = lim(z→z₀) (z - z₀)f(z)
```

### Residue at Pole of Order m
```
Res(f, z₀) = (1/(m-1)!) lim(z→z₀) d^(m-1)/dz^(m-1) [(z - z₀)^m f(z)]
```

### Residue Theorem
```
∮_C f(z) dz = 2πi × Σ Res(f, zₖ)

where zₖ are all singularities inside C
```

---

## 6. Laurent Series

### Definition
```
f(z) = Σ[n=-∞ to ∞] aₙ(z - z₀)^n

= ... + a₋₂/(z-z₀)² + a₋₁/(z-z₀) + a₀ + a₁(z-z₀) + ...
```

### Coefficients
```
aₙ = (1/(2πi)) ∮_C f(z)/(z - z₀)^(n+1) dz
```

### Types of Singularities
```
Removable: No negative powers in Laurent series
Pole of order m: a₋ₘ ≠ 0, aₙ = 0 for n < -m
Essential: Infinitely many negative powers
```

---

## 7. Important Theorems

### Maximum Modulus Principle
```
If f is analytic and non-constant in domain D:
|f| has no maximum in interior of D
Maximum occurs on boundary
```

### Minimum Modulus Principle
```
If f is analytic and non-zero in D:
|f| has no minimum in interior of D
```

### Liouville's Theorem
```
Bounded entire function is constant
```

### Fundamental Theorem of Algebra
```
Every polynomial of degree n has exactly n roots (counting multiplicity)
```

### Argument Principle
```
(1/(2πi)) ∮_C f'(z)/f(z) dz = N - P

N = number of zeros, P = number of poles inside C
```

### Rouché's Theorem
```
If |f(z)| > |g(z)| on C, then f and f+g have same number of zeros inside C
```

---

## 8. Applications

### Evaluating Real Integrals
```
∫[0,2π] R(cos θ, sin θ) dθ: Let z = e^(iθ)
∫[-∞,∞] f(x)/(x²+1) dx: Use residue theorem
∫[-∞,∞] e^(ix)/(x²+1) dx: Jordan's lemma
```

### Cauchy Principal Value
```
P.V. ∫[-∞,∞] f(x) dx = lim(R→∞] ∫[-R,R] f(x) dx
```

### Sum of Series
```
Σ f(n) = -Σ Res(f(z)·cot(πz), zₖ)

where zₖ are poles of f(z)
```

---

## 9. Important Functions

### Exponential
```
e^z = e^(x+iy) = e^x(cos y + i sin y)
|e^z| = e^x
arg(e^z) = y
```

### Trigonometric
```
cos z = (e^(iz) + e^(-iz))/2
sin z = (e^(iz) - e^(-iz))/(2i)
cos(iz) = cosh z
sin(iz) = i sinh z
```

### Hyperbolic
```
cosh z = (e^z + e^(-z))/2
sinh z = (e^z - e^(-z))/2
cosh(iz) = cos z
sinh(iz) = i sin z
```

### Logarithm
```
Log(z) = ln|z| + i arg(z) (principal value)
log(z) = ln|z| + i(arg(z) + 2kπ) (multi-valued)
```

### Powers
```
z^a = e^(a log z)
z^n (integer): single-valued
z^(1/n): n values
z^c (complex): multi-valued
```

---

## 10. Singularities Classification

### Removable Singularity
```
Laurent series has no negative powers
lim(z→z₀) (z-z₀)^(m+1) f(z) = 0 for some m ≥ 0
```

### Pole of Order m
```
Laurent series: a₋ₘ ≠ 0, aₙ = 0 for n < -m
lim(z→z₀) (z-z₀)^m f(z) = a₋ₘ ≠ 0
```

### Essential Singularity
```
Laurent series has infinitely many negative powers
Cassorati-Weierstrass: f(z) comes arbitrarily close to every value
```

---

## 11. Argument Principle Application

### Number of Zeros
```
N = (1/(2πi)) ∮_C f'(z)/f(z) dz

Count zeros (with multiplicity) inside C
```

### Number of Poles
```
P = (1/(2πi)) ∮_C f'(z)/f(z) dz

Count poles (with multiplicity) inside C
```

### Difference
```
N - P = (1/(2πi)) ∮_C f'(z)/f(z) dz
```
