# Differential Equations - Formulas

## 1. First Order ODE Formulas

### Variable Separable
```
dy/dx = f(x)g(y)
∫ dy/g(y) = ∫ f(x)dx + C
```

### Linear First Order
```
dy/dx + P(x)y = Q(x)

Integrating Factor: IF = e^(∫P(x)dx)

Solution: y · IF = ∫ Q(x) · IF dx + C
```

### Exact Equation
```
M dx + N dy = 0

Exact if: ∂M/∂y = ∂N/∂x

Solution: ∫ M dx (y constant) + ∫ (terms of N without x) dy = C
```

### Homogeneous (y = vx)
```
dy/dx = f(y/x)

Let y = vx → v + x(dv/dx) = f(v)
∫ dv/(f(v) - v) = ∫ dx/x + C
```

### Bernoulli (v = y^(1-n))
```
dy/dx + P(x)y = Q(x)y^n

Let v = y^(1-n) → dv/dx + (1-n)P(x)v = (1-n)Q(x)
Integrating factor: e^((1-n)∫P(x)dx)
```

---

## 2. Second Order Constant Coefficient

### Homogeneous: y'' + ay' + by = 0
```
Auxiliary: m² + am + b = 0

Roots m₁, m₂ (real distinct):
  CF = c₁e^(m₁x) + c₂e^(m₂x)

Roots m (real repeated):
  CF = (c₁ + c₂x)e^(mx)

Roots α ± iβ (complex):
  CF = e^(αx)(c₁cos(βx) + c₂sin(βx))
```

### Non-Homogeneous: y'' + ay' + by = R(x)
```
General Solution: y = CF + PI
```

---

## 3. Particular Integral Formulas

### Undetermined Coefficients
```
R(x) = polynomial of degree n:
  PI = Aₙxⁿ + Aₙ₋₁x^(n-1) + ... + A₀

R(x) = e^(ax):
  PI = Ae^(ax)  [if a not root of auxiliary]
  PI = Axe^(ax) [if a is simple root]
  PI = Ax²e^(ax) [if a is double root]

R(x) = sin(bx) or cos(bx):
  PI = A sin(bx) + B cos(bx)
  [if ib not root of auxiliary]

R(x) = e^(ax)sin(bx) or e^(ax)cos(bx):
  PI = e^(ax)(A sin(bx) + B cos(bx))

R(x) = x^n · e^(ax):
  PI = e^(ax)(Aₙxⁿ + ... + A₀)
```

### Variation of Parameters
```
PI = -y₁∫(y₂R/W)dx + y₂∫(y₁R/W)dx

Wronskian: W(y₁,y₂) = |y₁  y₂|  = y₁y₂' - y₂y₁'
                        |y₁' y₂'|
```

---

## 4. Cauchy-Euler Equation

```
x²y'' + axy' + by = 0

Substitution: x = e^t

Auxiliary: m(m-1) + am + b = 0
→ m² + (a-1)m + b = 0

Roots m₁, m₂:
  CF = c₁x^(m₁) + c₂x^(m₂)

Root m (repeated):
  CF = (c₁ + c₂ln(x))x^m

Roots α ± iβ:
  CF = x^α(c₁cos(β ln x) + c₂sin(β ln x))
```

---

## 5. Laplace Transform Table

```
f(t)              F(s) = L{f(t)}
─────────────────────────────────────────
1                 1/s
t^n               n!/s^(n+1)
e^(at)            1/(s-a)
sin(bt)           b/(s²+b²)
cos(bt)           s/(s²+b²)
sinh(bt)          b/(s²-b²)
cosh(bt)          s/(s²-b²)
t·e^(at)          1/(s-a)²
t·sin(bt)         2bs/(s²+b²)²
t·cos(bt)         (s²-b²)/(s²+b²)²
e^(at)sin(bt)     b/((s-a)²+b²)
e^(at)cos(bt)     (s-a)/((s-a)²+b²)
δ(t-a)            e^(-as)
u(t-a)            e^(-as)/s
```

### Properties
```
Linearity: L{af + bg} = aF(s) + bG(s)
First Shift: L{e^(at)f(t)} = F(s-a)
Second Shift: L{f(t-a)u(t-a)} = e^(-as)F(s)
Differentiation: L{f'(t)} = sF(s) - f(0)
L{f''(t)} = s²F(s) - sf(0) - f'(0)
Integration: L{∫[0,t] f(τ)dτ} = F(s)/s
Multiplication by t: L{t·f(t)} = -dF/ds
Division by t: L{f(t)/t} = ∫[s,∞] F(u)du
Convolution: L{f*g} = F(s)·G(s)
```

---

## 6. Inverse Laplace Transform

```
L⁻¹{1/s} = 1
L⁻¹{n!/s^(n+1)} = t^n
L⁻¹{1/(s-a)} = e^(at)
L⁻¹{b/(s²+b²)} = sin(bt)
L⁻¹{s/(s²+b²)} = cos(bt)
L⁻¹{b/((s-a)²+b²)} = e^(at)sin(bt)
L⁻¹{(s-a)/((s-a)²+b²)} = e^(at)cos(bt)
L⁻¹{F(s-a)} = e^(at)f(t)
L⁻¹{e^(-as)F(s)} = f(t-a)u(t-a)
L⁻¹{F(s)G(s)} = (f*g)(t) = ∫[0,t] f(τ)g(t-τ)dτ
```

### Partial Fractions
```
L⁻¹{(px+q)/[(x-a)(x-b)]} = L⁻¹{A/(x-a) + B/(x-b)}

L⁻¹{(px+q)/(x-a)²} = L⁻¹{A/(x-a) + B/(x-a)²}

L⁻¹{(px+q)/(ax²+bx+c)} = complete square method
```

---

## 7. Complementary Function Quick Reference

### Auxiliary Equation: am² + bm + c = 0
```
Discriminant D = b² - 4ac

D > 0 (real distinct roots m₁, m₂):
  CF = c₁e^(m₁x) + c₂e^(m₂x)

D = 0 (repeated root m = -b/2a):
  CF = (c₁ + c₂x)e^(mx)

D < 0 (complex roots α ± iβ):
  α = -b/2a, β = √(|D|)/2a
  CF = e^(αx)(c₁cos(βx) + c₂sin(βx))
```

---

## 8. Wronskian Formula

```
W(y₁, y₂, ..., yₙ) = |y₁   y₂   ... yₙ|
                       |y₁'  y₂'  ... yₙ'|
                       |y₁'' y₂'' ... yₙ''|
                       | ...                 |
                       |y₁^(n-1) ... yₙ^(n-1)|

For 2 functions: W = y₁y₂' - y₂y₁'

W ≠ 0: functions are linearly independent
W = 0: functions are linearly dependent
```

---

## 9. Important ODE Solutions

### d²y/dx² + ω²y = 0 (SHM)
```
y = c₁cos(ωx) + c₂sin(ωx)
y = A sin(ωx + φ)
```

### d²y/dx² - ω²y = 0
```
y = c₁e^(ωx) + c₂e^(-ωx)
y = c₁cosh(ωx) + c₂sinh(ωx)
```

### d²y/dx² + 2k dy/dx + (k² + ω²)y = 0 (Damped)
```
y = e^(-kx)(c₁cos(ωx) + c₂sin(ωx))
```

### Newton's Cooling
```
dT/dt = -k(T - Tₛ)
T(t) = Tₛ + (T₀ - Tₛ)e^(-kt)
```

### Growth/Decay
```
dN/dt = kN
N(t) = N₀e^(kt)
```

### Logistic Growth
```
dN/dt = kN(1 - N/K)
N(t) = K/(1 + ((K-N₀)/N₀)e^(-kt))
```

---

## 10. Series Solution (Brief)

### Ordinary Point x = x₀
```
y = Σ aₙ(x-x₀)^n

Substitute into ODE, equate coefficients of powers to zero
Recurrence relation for aₙ
```

### Regular Singular Point (Frobenius Method)
```
y = (x-x₀)^r Σ aₙ(x-x₀)^n

Indicial equation from lowest power
r = roots give independent solutions
```

---

## 11. Boundary Value Problems

### Dirichlet Problem
```
y'' + λy = 0, y(0) = 0, y(L) = 0
Eigenvalues: λₙ = (nπ/L)²
Eigenfunctions: yₙ = sin(nπx/L)
```

### Neumann Problem
```
y'' + λy = 0, y'(0) = 0, y'(L) = 0
Eigenvalues: λₙ = (nπ/L)²
Eigenfunctions: yₙ = cos(nπx/L)
```

### Mixed Boundary
```
y'' + λy = 0, y(0) = 0, y'(L) = 0
Eigenvalues: λₙ = ((2n-1)π/2L)²
Eigenfunctions: yₙ = sin((2n-1)πx/2L)
```
