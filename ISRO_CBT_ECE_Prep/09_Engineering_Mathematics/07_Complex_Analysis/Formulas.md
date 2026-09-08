# Complex Analysis - Formulas

## 1. Complex Number Formulas

### Basic Operations
```
z₁ + z₂ = (x₁+x₂) + i(y₁+y₂)
z₁ - z₂ = (x₁-x₂) + i(y₁-y₂)
z₁z₂ = (x₁x₂-y₁y₂) + i(x₁y₂+x₂y₁)
z₁/z₂ = (z₁z₂*)/|z₂|²
```

### Modulus and Argument
```
|z| = √(x² + y²)
arg(z) = arctan(y/x) [with quadrant adjustment]
|z₁z₂| = |z₁||z₂|
arg(z₁z₂) = arg(z₁) + arg(z₂)
```

### Polar Form
```
z = r(cos θ + i sin θ) = re^(iθ)
z* = r(cos θ - i sin θ) = re^(-iθ) = r^(-1)z̄
1/z = (1/r)(cos θ - i sin θ)
```

### De Moivre's Theorem
```
z^n = r^n(cos nθ + i sin nθ)
z^(1/n) = r^(1/n)(cos(θ+2kπ)/n + i sin(θ+2kπ)/n) for k = 0,...,n-1
```

---

## 2. Cauchy-Riemann Equations

### Condition for Analyticity
```
f(z) = u(x,y) + iv(x,y) is analytic ⟺

∂u/∂x = ∂v/∂y
∂u/∂y = -∂v/∂x

and partial derivatives are continuous
```

### Derivative Formula
```
f'(z) = ∂u/∂x + i∂v/∂x = ∂v/∂y - i∂u/∂y
```

### Finding Conjugate Harmonic
```
Given u(x,y), find v:
1. ∂v/∂y = ∂u/∂x → integrate w.r.t. y
2. ∂v/∂x = -∂u/∂y → differentiate and compare
3. Determine constant of integration
```

---

## 3. Conformal Mapping Formulas

### Elementary Mappings
```
Translation: w = z + c
Rotation: w = e^(iθ)z
Scaling: w = kz
Inversion: w = 1/z
Power: w = z^n
Exponential: w = e^z
Logarithmic: w = log z
```

### Möbius Transformation
```
w = (az + b)/(cz + d), ad - bc ≠ 0

Inverse: z = (dw - b)/(-cw + a)

Fixed points: solve w = z → cz² + (d-a)z - b = 0

Cross ratio: (z₁,z₂;z₃,z₄) = (z₁-z₃)(z₂-z₄)/((z₁-z₄)(z₂-z₃))
```

### Key Properties
```
Maps circles/lines to circles/lines
Preserves cross ratio
Three points determine transformation
Conformal everywhere except at pole z = -d/c
```

---

## 4. Complex Integration Formulas

### Line Integral
```
∫_C f(z) dz = ∫_a^b f(z(t)) z'(t) dt
```

### Cauchy's Integral Theorem
```
∮_C f(z) dz = 0

if f is analytic inside and on simple closed curve C
```

### Cauchy's Integral Formula
```
f(z₀) = (1/(2πi)) ∮_C f(z)/(z - z₀) dz
```

### Generalized Cauchy Formula
```
f^(n)(z₀) = (n!/(2πi)) ∮_C f(z)/(z - z₀)^(n+1) dz
```

### ML Inequality
```
|∫_C f(z) dz| ≤ M × L

M = max|f(z)| on C, L = length of C
```

---

## 5. Residue Formulas

### Definition
```
Res(f, z₀) = coefficient of (z-z₀)^(-1) in Laurent series
            = a₋₁
```

### Simple Pole
```
Res(f, z₀) = lim(z→z₀) (z - z₀)f(z)

If f(z) = p(z)/q(z), p(z₀) ≠ 0, q(z₀) = 0, q'(z₀) ≠ 0:
Res(f, z₀) = p(z₀)/q'(z₀)
```

### Pole of Order m
```
Res(f, z₀) = (1/(m-1)!) lim(z→z₀) d^(m-1)/dz^(m-1) [(z - z₀)^m f(z)]
```

### Essential Singularity
```
Res(f, z₀) = (1/(2πi)) ∮_C f(z) dz [contour around z₀]
```

### Residue Theorem
```
∮_C f(z) dz = 2πi × Σ Res(f, zₖ)

where zₖ are singularities inside C
```

---

## 6. Laurent Series Formulas

### Definition
```
f(z) = Σ[n=-∞ to ∞] aₙ(z - z₀)^n

aₙ = (1/(2πi)) ∮_C f(z)/(z - z₀)^(n+1) dz
```

### Important Series
```
1/(1-z) = Σ[n=0 to ∞] z^n for |z| < 1
1/(1+z) = Σ[n=0 to ∞] (-1)^n z^n for |z| < 1
e^z = Σ[n=0 to ∞] z^n/n! for all z
sin z = Σ[n=0 to ∞] (-1)^n z^(2n+1)/(2n+1)! for all z
cos z = Σ[n=0 to ∞] (-1)^n z^(2n)/(2n)! for all z
1/(z-a) = -(1/a) Σ[n=0 to ∞] (z/a)^n for |z| < |a|
1/(z-a) = (1/z) Σ[n=0 to ∞] (a/z)^n for |z| > |a|
```

### Singularities from Laurent Series
```
Removable: aₙ = 0 for all n < 0
Pole of order m: a₋ₘ ≠ 0, aₙ = 0 for n < -m
Essential: infinitely many aₙ ≠ 0 for n < 0
```

---

## 7. Important Theorems

### Maximum Modulus Principle
```
If f is analytic and non-constant in domain D:
max|f(z)| on closure(D) = max|f(z)| on boundary(D)
```

### Liouville's Theorem
```
If f is entire and |f(z)| ≤ M for all z:
f is constant
```

### Fundamental Theorem of Algebra
```
Every polynomial p(z) of degree n ≥ 1 has at least one root
Equivalently: p(z) has exactly n roots counting multiplicity
```

### Argument Principle
```
(1/(2πi)) ∮_C f'(z)/f(z) dz = N - P

N = zeros of f inside C (with multiplicity)
P = poles of f inside C (with multiplicity)
```

### Rouché's Theorem
```
If |f(z)| > |g(z)| on C:
f and f+g have same number of zeros inside C
```

### Open Mapping Theorem
```
Non-constant analytic function maps open sets to open sets
```

---

## 8. Real Integral Evaluation

### Type 1: Trigonometric Integrals
```
∫[0,2π] R(cos θ, sin θ) dθ

Let z = e^(iθ):
cos θ = (z + z⁻¹)/2
sin θ = (z - z⁻¹)/(2i)
dθ = dz/(iz)

= ∮|z|=1 R(...) dz/(iz)
```

### Type 2: Rational Functions
```
∫[-∞,∞] P(x)/Q(x) dx

where deg(Q) ≥ deg(P) + 2

= 2πi × Σ Res in upper half-plane
```

### Type 3: With Exponential
```
∫[-∞,∞] f(x)e^(ix) dx = 2πi × Σ Res(f(z)e^(iz)) in upper half-plane

Jordan's Lemma: ∫_C_R f(z)e^(iz) dz → 0 as R → ∞
if |f(z)| → 0 uniformly as |z| → ∞ in upper half-plane
```

### Cauchy Principal Value
```
P.V. ∫[-∞,∞] f(x) dx = lim(R→∞] ∫[-R,R] f(x) dx

For simple pole at x₀ on real axis:
P.V. ∫ f(x) dx = πi Res(f, x₀)
```

---

## 9. Special Functions in Complex Plane

### Exponential
```
e^z = e^x(cos y + i sin y)
|e^z| = e^x
arg(e^z) = y
e^(z+2πi) = e^z
```

### Trigonometric
```
cos z = (e^(iz) + e^(-iz))/2
sin z = (e^(iz) - e^(-iz))/(2i)
tan z = sin z/cos z
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
Log(z) = ln|z| + i Arg(z)  [-π < Arg(z) ≤ π]
log(z) = ln|z| + i(arg(z) + 2kπ)  [multi-valued]
Log(z₁z₂) ≠ Log(z₁) + Log(z₂) in general
```

### Powers
```
z^a = e^(a log z) = |z|^a e^(ia arg(z))
z^n (integer): single-valued
z^(1/n): n values
z^c (complex): multi-valued
```

---

## 10. Contour Integration Quick Reference

### Common Contours
```
|z| = R: Circle of radius R
Real axis: -R to R, semicircle in upper half-plane
Keyhole contour: Around branch cut
Rectangle: For integrals with periodicity
```

### Residue at Infinity
```
Res(f, ∞) = -Res(f(1/z)/z², 0)
```

### Sum of Residues
```
Σ(all residues including ∞) = 0
```
