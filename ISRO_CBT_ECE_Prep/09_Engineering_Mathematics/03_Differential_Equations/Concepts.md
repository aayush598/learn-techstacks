# Differential Equations - Concepts

## 1. Basic Definitions

### Order & Degree
- **Order**: Highest derivative present
- **Degree**: Power of highest derivative (after removing radicals from derivatives)

### General Solution
- Contains arbitrary constants equal to order
- **Particular solution**: Specific values for constants

### Linear vs Non-Linear
- **Linear**: y, y', y'', etc. appear to first power only
- **Non-linear**: y², yy', (y')², etc.

---

## 2. First Order Differential Equations

### Variable Separable
```
dy/dx = f(x)g(y)
∫ dy/g(y) = ∫ f(x)dx + C
```

### Linear First Order
```
dy/dx + P(x)y = Q(x)

Integrating factor: IF = e^(∫P(x)dx)
Solution: y · IF = ∫ Q(x) · IF dx + C
```

### Exact Differential Equation
```
M(x,y)dx + N(x,y)dy = 0

Exact if: ∂M/∂y = ∂N/∂x
Solution: ∫ M dx + ∫ (terms of N not involving x) dy = C
```

### Reducible to Exact
```
If (1/N)(∂M/∂y - ∂N/∂x) = f(x) only:
Integrating factor: e^(∫f(x)dx)

If (1/M)(∂N/∂x - ∂M/∂y) = g(y) only:
Integrating factor: e^(∫g(y)dy)
```

### Homogeneous Differential Equation
```
dy/dx = f(y/x)

Substitution: y = vx → dy/dx = v + x(dv/dx)
Separate and integrate
```

### Bernoulli's Equation
```
dy/dx + P(x)y = Q(x)y^n

Substitution: v = y^(1-n)
Reduces to linear equation
```

### Riccati's Equation
```
dy/dx = P(x) + Q(x)y + R(x)y²

If one particular solution y₁ is known:
Substitution y = y₁ + 1/v reduces to linear
```

---

## 3. Second Order Linear ODEs

### Standard Form
```
y'' + P(x)y' + Q(x)y = R(x)
```

### Homogeneous (R = 0)
```
y'' + P(x)y' + Q(x)y = 0
```

### Complementary Function (CF)
- **Constant coefficients**: y'' + ay' + by = 0
- Auxiliary equation: m² + am + b = 0

| Roots | CF Form |
|-------|---------|
| Real distinct m₁, m₂ | c₁e^(m₁x) + c₂e^(m₂x) |
| Real repeated m | (c₁ + c₂x)e^(mx) |
| Complex α ± iβ | e^(αx)(c₁cos(βx) + c₂sin(βx)) |

### Non-Homogeneous (R ≠ 0)
```
Solution: y = CF + PI
```

### Particular Integral (PI) Methods

#### Method of Undetermined Coefficients
```
For R(x) = polynomial:
- Assume PI = polynomial of same degree
- For R(x) = e^(ax): PI = Ae^(ax)
- For R(x) = sin(bx) or cos(bx): PI = A sin(bx) + B cos(bx)
- For R(x) = e^(ax)·sin(bx): PI = e^(ax)(A sin(bx) + B cos(bx))
- If R(x) is part of CF, multiply by x (or x² if repeated)
```

#### Method of Variation of Parameters
```
For y'' + P(x)y' + Q(x)y = R(x)

If CF = c₁y₁ + c₂y₂:
PI = -y₁∫(y₂R/W)dx + y₂∫(y₁R/W)dx

W = Wronskian = y₁y₂' - y₂y₁'
```

### Cauchy-Euler Equation
```
x²y'' + axy' + by = 0

Substitution: x = e^t → constant coefficient equation
Auxiliary: m(m-1) + am + b = 0
```

---

## 4. Important Special Equations

### Legendre's Linear Equation
```
(a + bx)^n y^(n) + ... = R(x)

Substitution: a + bx = e^t
```

### Bessel's Equation
```
x²y'' + xy' + (x² - n²)y = 0

Solution: y = c₁Jₙ(x) + c₂Yₙ(x)
```

### Legendre's Differential Equation
```
(1-x²)y'' - 2xy' + n(n+1)y = 0

Solution: y = c₁Pₙ(x) + c₂Qₙ(x)
```

---

## 5. Laplace Transform Method

### Definition
```
L{f(t)} = F(s) = ∫[0,∞] e^(-st)f(t) dt
```

### Important Transforms
```
L{1} = 1/s
L{t^n} = n!/s^(n+1)
L{e^(at)} = 1/(s-a)
L{sin(bt)} = b/(s²+b²)
L{cos(bt)} = s/(s²+b²)
L{sinh(bt)} = b/(s²-b²)
L{cosh(bt)} = s/(s²-b²)
L{e^(at)f(t)} = F(s-a)
L{t^n f(t)} = (-1)^n F^(n)(s)
L{f'(t)} = sF(s) - f(0)
L{f''(t)} = s²F(s) - sf(0) - f'(0)
```

### Inverse Laplace Transform
```
L⁻¹{1/s} = 1
L⁻¹{n!/s^(n+1)} = t^n
L⁻¹{1/(s-a)} = e^(at)
L⁻¹{b/(s²+b²)} = sin(bt)
L⁻¹{s/(s²+b²)} = cos(bt)
L⁻¹{F(s-a)} = e^(at)f(t)
```

### Convolution Theorem
```
L{f * g} = F(s) · G(s)
(f * g)(t) = ∫[0,t] f(τ)g(t-τ) dτ
```

---

## 6. Applications of ODEs

### Growth & Decay
```
dN/dt = kN → N = N₀e^(kt)
```

### Newton's Cooling Law
```
dT/dt = -k(T - Tₛ)
Solution: T(t) = Tₛ + (T₀ - Tₛ)e^(-kt)
```

### Simple Harmonic Motion
```
my'' + ky = 0
Solution: y = A cos(ωt + φ), ω = √(k/m)
```

### Damped Harmonic Motion
```
my'' + cy' + ky = 0
Characteristic: mλ² + cλ + k = 0
Underdamped: c² < 4mk
Overdamped: c² > 4mk
Critically damped: c² = 4mk
```

### RC/RL/RLC Circuits
```
RC: R(dq/dt) + q/C = E(t)
RL: L(di/dt) + Ri = E(t)
RLC: L(d²q/dt²) + R(dq/dt) + q/C = E(t)
```

---

## 7. Order Reduction

### Missing Dependent Variable
```
y'' = f(x, y')
Let p = y', then p' = f(x, p) → first order
```

### Missing Independent Variable
```
y'' = f(y, y')
Let p = y', then p(dp/dy) = f(y, p) → first order in p(y)
```

---

## 8. Important Properties

### Superposition Principle
- If y₁ and y₂ are solutions of homogeneous linear ODE
- Then c₁y₁ + c₂y₂ is also a solution

### Existence & Uniqueness
- For y' = f(x,y) with y(x₀) = y₀
- If f and ∂f/∂y are continuous near (x₀, y₀)
- Then solution exists and is unique

### Wronskian
```
W(y₁, y₂) = |y₁  y₂|
              |y₁' y₂'|

If W ≠ 0: y₁, y₂ are linearly independent
If W = 0: y₁, y₂ are linearly dependent
```

---

## 9. Quick Reference Table

| Equation Type | Method |
|--------------|--------|
| Separable | Separate variables |
| Linear 1st order | Integrating factor |
| Exact | Direct integration |
| Homogeneous 1st order | y = vx substitution |
| Bernoulli | v = y^(1-n) substitution |
| Constant coefficient 2nd order | Auxiliary equation |
| Cauchy-Euler | x = e^t substitution |
| Variation of parameters | Wronskian method |
| Laplace transform | Transform, solve, inverse |
