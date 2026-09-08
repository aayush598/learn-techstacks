# ISRO CBT ECE - Engineering Mathematics Shortcuts

## 1. Linear Algebra Quick Tricks

### Singular Matrix Identification (5 seconds)
```
Matrix is singular if:
1. Two rows/columns are identical
2. One row/column is scalar multiple of another
3. Sum of rows = 0 vector
4. Trace = sum of eigenvalues, one is 0
5. Determinant = product of eigenvalues = 0

Quick check: If row1 + row2 = row3 → singular
```

### Eigenvalue Quick Formulas
```
For 2×2: λ² - trace·λ + det = 0

trace(A) = λ₁ + λ₂ + ...
det(A) = λ₁ × λ₂ × ...

Eigenvalue of A⁻¹ = 1/λ
Eigenvalue of A^k = λ^k
Eigenvalue of A + cI = λ + c
```

### Cayley-Hamilton Shortcut
```
To find A⁻¹ using Cayley-Hamilton:
1. Find characteristic equation: p(λ) = λⁿ + ... = 0
2. Replace λ with A: Aⁿ + ... = 0
3. Multiply by A⁻¹: Aⁿ⁻¹ + ... + I = 0
4. Solve for A⁻¹
```

### Rank Quick Check
```
rank(A) = number of non-zero rows in REF
rank(A) < n → det(A) = 0 → singular
rank(A) = n → full rank → invertible
```

---

## 2. Calculus Speed Techniques

### Limit Tricks
```
For 0/0: L'Hopital's rule (differentiate top and bottom)
For ∞/∞: L'Hopital's rule
For 0·∞: Convert to fraction
For 1^∞: Use lim(1+x)^(1/x) = e

Quick limit: lim(x→0) sin(ax)/(bx) = a/b
```

### Derivative Shortcuts
```
d/dx [e^(ax)] = ae^(ax)
d/dx [ln(ax)] = 1/x
d/dx [sin(ax)] = a·cos(ax)
d/dx [arctan(x)] = 1/(1+x²)
d/dx [arcsin(x)] = 1/√(1-x²)
```

### Integration by Parts LIATE
```
Priority for u: Logarithmic > Inverse trig > Algebraic > Trig > Exponential

Example: ∫ x·eˣ dx → u = x, dv = eˣ dx
Example: ∫ x·sin(x) dx → u = x, dv = sin(x) dx
Example: ∫ ln(x) dx → u = ln(x), dv = dx
```

### Definite Integral Symmetry
```
∫[0,a] f(x) dx = ∫[0,a] f(a-x) dx

If f(a-x) = f(x): ∫[0,a] = 2∫[0,a/2]
If f(a-x) = -f(x): ∫[0,a] = 0
```

### Taylor Series Quick Reference
```
eˣ = 1 + x + x²/2! + x³/3! + ...     [all x]
sin(x) = x - x³/3! + x⁵/5! - ...    [all x]
cos(x) = 1 - x²/2! + x⁴/4! - ...    [all x]
1/(1-x) = 1 + x + x² + x³ + ...     [|x| < 1]
ln(1+x) = x - x²/2 + x³/3 - ...     [-1 < x ≤ 1]
```

---

## 3. Differential Equations Shortcuts

### Second Order CF Quick
```
Auxiliary: am² + bm + c = 0

D > 0: CF = c₁e^(m₁x) + c₂e^(m₂x)
D = 0: CF = (c₁ + c₂x)e^(mx)
D < 0: CF = e^(αx)(c₁cos(βx) + c₂sin(βx))
```

### PI Quick Selection
```
R(x) = e^(ax): Try Ae^(ax)
R(x) = sin(bx): Try A sin(bx) + B cos(bx)
R(x) = polynomial: Try polynomial of same degree

If R(x) is part of CF: multiply by x (or x² if repeated)
```

### Laplace Transform Quick Table
```
L{1} = 1/s
L{t^n} = n!/s^(n+1)
L{e^(at)} = 1/(s-a)
L{sin(bt)} = b/(s²+b²)
L{cos(bt)} = s/(s²+b²)
L{f'(t)} = sF(s) - f(0)
L{f''(t)} = s²F(s) - sf(0) - f'(0)
```

### Inverse Laplace Quick
```
1/s → 1
1/s² → t
1/(s-a) → e^(at)
b/(s²+b²) → sin(bt)
s/(s²+b²) → cos(bt)
F(s-a) → e^(at)f(t)
e^(-as)F(s) → f(t-a)u(t-a)
```

---

## 4. PDE Shortcuts

### Classification Quick
```
A u_xx + B u_xy + C u_yy = ...
Δ = B² - 4AC

Δ > 0: Hyperbolic (Wave)
Δ = 0: Parabolic (Heat)
Δ < 0: Elliptic (Laplace)
```

### Heat Equation Solution
```
u_t = k u_xx, u(0,t) = u(L,t) = 0:

u(x,t) = Σ Bₙ sin(nπx/L) e^(-k(nπ/L)²t)

Bₙ = (2/L) ∫[0,L] f(x) sin(nπx/L) dx
```

### Wave Equation Solution
```
u_tt = c² u_xx, u(0,t) = u(L,t) = 0:

u(x,t) = Σ sin(nπx/L)[Aₙ cos(nπct/L) + Bₙ sin(nπct/L)]
```

### Laplace Equation Solution (Polar)
```
u(r,θ) = a₀/2 + Σ rⁿ(aₙcos(nθ) + bₙsin(nθ))

aₙ, bₙ from Fourier series of boundary condition
```

### Steady State Quick
```
Heat equation steady state: u_xx = 0 → u = Ax + B
Apply boundary conditions to find A, B
```

---

## 5. Probability Shortcuts

### Bayes' Theorem Quick
```
P(A|B) = P(B|A)P(A) / [P(B|A)P(A) + P(B|A')P(A')]

Medical testing:
P(Disease|+) = sensitivity × prevalence / [sensitivity × prevalence + (1-specificity) × (1-prevalence)]
```

### Total Probability Quick
```
P(B) = Σ P(B|Aᵢ)P(Aᵢ)

If two events: P(B) = P(B|A)P(A) + P(B|A')P(A')
```

### Distribution Quick Reference
```
Binomial: P(X=k) = C(n,k)p^k(1-p)^(n-k)
Poisson: P(X=k) = e^(-λ)λ^k/k!
Normal: Z = (X-μ)/σ
Exponential: P(X>x) = e^(-λx)
```

### Normal Distribution 68-95-97
```
P(μ-σ < X < μ+σ) ≈ 68%
P(μ-2σ < X < μ+2σ) ≈ 95%
P(μ-3σ < X < μ+3σ) ≈ 99.7%
```

---

## 6. Statistics Shortcuts

### Variance Quick
```
Var(X) = E[X²] - (E[X])²

If X ~ Bin(n,p): Var = npq
If X ~ Poisson(λ): Var = λ
If X ~ Unif(a,b): Var = (b-a)²/12
```

### Central Limit Theorem
```
x̄ ~ N(μ, σ²/n) for n ≥ 30

z = (x̄ - μ)/(σ/√n)
```

### Confidence Interval Quick
```
95% CI: x̄ ± 1.96σ/√n
99% CI: x̄ ± 2.576σ/√n
```

### Sample Size Quick
```
n = (z·σ/E)² for mean
n = (z/E)²·p(1-p) for proportion
```

---

## 7. Complex Analysis Shortcuts

### Residue Quick
```
Simple pole at z₀: Res = lim(z→z₀) (z-z₀)f(z)

If f(z) = p(z)/q(z): Res(z₀) = p(z₀)/q'(z₀)
```

### Residue Theorem
```
∮ f(z) dz = 2πi × Σ (residues inside contour)
```

### CR Equations Quick
```
f = u + iv analytic ⟺
u_x = v_y and u_y = -v_x

f'(z) = u_x + iv_x
```

### Laurent Series Quick
```
Removable: No negative powers
Pole of order m: highest negative power is (z-z₀)^(-m)
Essential: infinitely many negative powers
```

---

## 8. Numerical Methods Shortcuts

### Newton-Raphson
```
x_{n+1} = x_n - f(x_n)/f'(x_n)

For √a: x_{n+1} = (x_n + a/x_n)/2
For 1/a: x_{n+1} = x_n(2 - ax_n)
```

### Simpson's Rule Quick
```
∫ f dx ≈ h/3 [first + 4(odd sum) + 2(even sum) + last]

n must be even
```

### RK4 Quick
```
k₁ = hf(x_n, y_n)
k₂ = hf(x_n + h/2, y_n + k₁/2)
k₃ = hf(x_n + h/2, y_n + k₂/2)
k₄ = hf(x_n + h, y_n + k₃)
y_{n+1} = y_n + (k₁ + 2k₂ + 2k₃ + k₄)/6
```

### Euler's Method
```
y_{n+1} = y_n + hf(x_n, y_n)

Simple but O(h) error
```

---

## 9. Common Patterns in ISRO Questions

### Matrix Questions
```
1. Quick singular check: det = 0?
2. Eigenvalue sum = trace
3. Eigenvalue product = det
4. A singular ↔ 0 is eigenvalue
```

### Integration Questions
```
1. LIATE rule for integration by parts
2. Symmetry for definite integrals
3. Walli's formula for sin^n, cos^n
```

### PDE Questions
```
1. Classification first (Δ = B² - 4AC)
2. Separation of variables → ODEs
3. Fourier coefficients for boundary conditions
```

### Probability Questions
```
1. Bayes' theorem for conditional
2. Distribution identification (count = Poisson, etc.)
3. Normal approximation for large n
```

---

## 10. Time-Saving Formulas

### Determinant (2×2)
```
|a b| = ad - bc
|c d|
```

### Determinant (3×3) Sarrus
```
|a b c| = aei + bfg + cdh - ceg - bdi - afh
|d e f|
|g h i|
```

### Matrix Inverse (2×2)
```
A = |a b|  →  A⁻¹ = 1/(ad-bc) | d -b|
    |c d|                      |-c  a|
```

### Quadratic Formula
```
x = (-b ± √(b²-4ac))/(2a)
```

### Sum of Geometric Series
```
Σ[k=0 to n-1] ar^k = a(1-r^n)/(1-r)
```

### Sum of Arithmetic Series
```
Σ[k=1 to n] (a + (k-1)d) = n/2(2a + (n-1)d)
```
