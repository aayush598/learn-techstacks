# Partial Differential Equations - Concepts

## 1. Basic Definitions

### Order of PDE
- Highest order partial derivative present

### Linear vs Non-Linear
- **Linear**: u, u_x, u_xx, etc. appear to first power only
- **Quasi-linear**: Linear in highest order derivatives
- **Non-linear**: Products of highest order derivatives

### Solutions
- **General solution**: Contains arbitrary functions
- **Particular solution**: Specific solution satisfying conditions
- **Complete integral**: Contains n arbitrary constants for n independent variables
- **Singular solution**: Envelope of family of solutions

---

## 2. First Order PDEs

### Lagrange's Linear Equation
```
Pp + Qq = R

where p = ∂u/∂x, q = ∂u/ auxiliary: dxdydz
Auxiliary equations: dx/P = dy/Q = dz/R
```

### Non-Linear First Order
```
f(u, p, q) = 0 → Charpit's method
g(x, y, p, q) = 0 → Charpit's method
```

### Charpit's Auxiliary Equations
```
dp/(f_x + pf_u) = dq/(f_y + qf_u) = -p dx/(f_p) = -q dy/(f_q)
```

---

## 3. Second Order Linear PDEs

### General Form
```
A u_xx + B u_xy + C u_yy + D u_x + E u_y + F u = G(x,y)
```

### Classification (B² - 4AC)
| Condition | Type | Canonical Form |
|-----------|------|----------------|
| B² - 4AC > 0 | Hyperbolic | Wave equation |
| B² - 4AC = 0 | Parabolic | Heat equation |
| B² - 4AC < 0 | Elliptic | Laplace equation |

### Constant Coefficient Classification
```
Wave:      u_tt = c² u_xx     (hyperbolic)
Heat:      u_t = k u_xx       (parabolic)
Laplace:   u_xx + u_yy = 0    (elliptic)
Poisson:   u_xx + u_yy = f    (elliptic)
```

---

## 4. Heat Equation

### One Dimensional
```
∂u/∂t = k ∂²u/∂x²

k = thermal diffusivity = κ/(ρc)
κ = thermal conductivity
ρ = density
c = specific heat
```

### Solution Methods
- Separation of variables
- Fourier series
- Laplace transform

### Boundary Conditions
1. **Dirichlet**: u(0,t) = u(L,t) = 0 (fixed ends)
2. **Neumann**: u_x(0,t) = u_x(L,t) = 0 (insulated ends)
3. **Robin**: u_x + hu = 0 (mixed)

### Initial Condition
```
u(x,0) = f(x) for 0 < x < L
```

### Solution (Dirichlet BC)
```
u(x,t) = Σ[n=1 to ∞] Bₙ sin(nπx/L) e^(-k(nπ/L)²t)

Bₙ = (2/L) ∫[0,L] f(x) sin(nπx/L) dx
```

---

## 5. Wave Equation

### One Dimensional
```
∂²u/∂t² = c² ∂²u/∂x²

c = wave speed
```

### d'Alembert's Solution
```
u(x,t) = [f(x+ct) + f(x-ct)]/2 + (1/2c)∫[x-ct, x+ct] g(s) ds

where u(x,0) = f(x) (initial displacement)
      u_t(x,0) = g(x) (initial velocity)
```

### Separation of Variables
```
u(x,t) = X(x)T(t)

X'' + λX = 0
T'' + c²λT = 0
```

### Solution (Dirichlet BC)
```
u(x,t) = Σ[n=1 to ∞] sin(nπx/L)[Aₙ cos(nπct/L) + Bₙ sin(nπct/L)]

Aₙ = (2/L) ∫[0,L] f(x) sin(nπx/L) dx
Bₙ = (2/(nπc)) ∫[0,L] g(x) sin(nπx/L) dx
```

---

## 6. Laplace Equation (Dirichlet Problem)

### Two Dimensional
```
∂²u/∂x² + ∂²u/∂y² = 0 (Laplace)
∂²u/∂x² + ∂²u/∂y² = f (Poisson)
```

### Properties of Harmonic Functions
1. Mean value property
2. Maximum/minimum principle
3. Uniqueness of solution

### Solution in Rectangle
```
u(x,y) = Σ Bₙ sin(nπx/a) sinh(nπy/a)
or
u(x,y) = Σ Bₙ sin(nπy/b) sinh(nπx/b)
```

### Solution in Circle
```
u(r,θ) = a₀/2 + Σ[rⁿ/(aⁿ)](aₙcos(nθ) + bₙsin(nθ))

aₙ = (1/π) ∫[0,2π] f(θ)cos(nθ) dθ
bₙ = (1/π) ∫[0,2π] f(θ)sin(nθ) dθ
```

---

## 7. Separation of Variables

### General Method
1. Assume u(x,t) = X(x)T(t)
2. Substitute into PDE
3. Separate variables → ODEs
4. Solve ODEs with boundary conditions
5. Apply initial conditions using Fourier series

### Key Steps
```
For u_tt = c² u_xx:

Step 1: X(x)T''(t) = c² X''(x)T(t)
Step 2: T''/(c²T) = X''/X = -λ (separation constant)
Step 3: X'' + λX = 0 with BC
        T'' + c²λT = 0
Step 4: Find eigenvalues λₙ and eigenfunctions Xₙ
Step 5: General solution: u = Σ Xₙ(x)Tₙ(t)
```

---

## 8. Boundary and Initial Conditions

### Types of BCs
```
Dirichlet:   u = prescribed value on boundary
Neumann:     ∂u/∂n = prescribed value on boundary
Robin:       ∂u/∂n + hu = prescribed on boundary
```

### Initial Conditions
```
For u_t equation: u(x,0) = f(x) (initial temperature/displacement)
For u_tt equation: u(x,0) = f(x), u_t(x,0) = g(x) (initial displacement & velocity)
```

### Well-Posedness
- Solution exists
- Solution is unique
- Solution depends continuously on data

---

## 9. Fourier Series Solutions

### Fourier Sine Series
```
f(x) = Σ[n=1 to ∞] bₙ sin(nπx/L)

bₙ = (2/L) ∫[0,L] f(x) sin(nπx/L) dx
```

### Fourier Cosine Series
```
f(x) = a₀/2 + Σ[n=1 to ∞] aₙ cos(nπx/L)

aₙ = (2/L) ∫[0,L] f(x) cos(nπx/L) dx
```

### Full Fourier Series
```
f(x) = a₀/2 + Σ[aₙcos(nπx/L) + bₙsin(nπx/L)]

aₙ = (1/L) ∫[-L,L] f(x) cos(nπx/L) dx
bₙ = (1/L) ∫[-L,L] f(x) sin(nπx/L) dx
```

---

## 10. Important PDE Applications

### Heat Conduction
- Temperature distribution in rod/plate
- Boundary: fixed temperature or insulated
- Initial: initial temperature distribution

### Wave Propagation
- Vibrating string
- Boundary: fixed ends
- Initial: displacement and velocity

### Electrostatics
- Potential in charge-free region
- Laplace equation
- Boundary: conductor surface potential

### Fluid Flow
- Velocity potential satisfies Laplace equation
- Stream function for 2D incompressible flow

---

## 11. Classification Flowchart

```
Given: A u_xx + B u_xy + C u_yy + ... = 0

Compute: Δ = B² - 4AC

Δ > 0: Hyperbolic → Wave equation
       Canonical: u_ξη = ... (characteristic coordinates)

Δ = 0: Parabolic → Heat equation
       Canonical: u_ηη = ... (one repeated characteristic)

Δ < 0: Elliptic → Laplace equation
       Canonical: u_ξξ + u_ηη = ... (no real characteristics)
```

---

## 12. Quick Reference

| PDE | Type | Physical Meaning |
|-----|------|-----------------|
| u_tt = c² u_xx | Hyperbolic | Wave propagation |
| u_t = k u_xx | Parabolic | Heat diffusion |
| u_xx + u_yy = 0 | Elliptic | Steady-state |
| u_xx + u_yy = f | Elliptic | Poisson equation |
| u_t + u u_x = 0 | Non-linear | Burgers equation |
| u_t + c u_x = 0 | Hyperbolic | Transport equation |
