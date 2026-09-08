# Partial Differential Equations - Formulas

## 1. Classification Formula

### For Second Order PDE
```
A u_xx + B u_xy + C u_yy + D u_x + E u_y + F u = G

Δ = B² - 4AC

Δ > 0: Hyperbolic (Wave equation)
Δ = 0: Parabolic (Heat equation)
Δ < 0: Elliptic (Laplace equation)
```

---

## 2. Heat Equation Formulas

### One Dimensional
```
∂u/∂t = k ∂²u/∂x²

Solution (Dirichlet BC: u(0,t) = u(L,t) = 0):

u(x,t) = Σ[n=1 to ∞] Bₙ sin(nπx/L) e^(-k(nπ/L)²t)

Bₙ = (2/L) ∫[0,L] f(x) sin(nπx/L) dx
```

### Neumann BC (Insulated Ends)
```
u_x(0,t) = u_x(L,t) = 0

u(x,t) = A₀/2 + Σ[n=1 to ∞] Aₙ cos(nπx/L) e^(-k(nπ/L)²t)

Aₙ = (2/L) ∫[0,L] f(x) cos(nπx/L) dx
```

### Semi-Infinite Rod
```
u(0,t) = u₀ (constant)

u(x,t) = u₀ erfc(x/(2√(kt)))

erfc(z) = (2/√π) ∫[z,∞] e^(-t²) dt = 1 - erf(z)
```

---

## 3. Wave Equation Formulas

### One Dimensional
```
∂²u/∂t² = c² ∂²u/∂x²

d'Alembert's Solution:
u(x,t) = [f(x+ct) + f(x-ct)]/2 + (1/2c)∫[x-ct, x+ct] g(s) ds

f(x) = u(x,0) = initial displacement
g(x) = u_t(x,0) = initial velocity
```

### Separation of Variables (Dirichlet BC)
```
u(x,t) = Σ[n=1 to ∞] sin(nπx/L)[Aₙ cos(nπct/L) + Bₙ sin(nπct/L)]

Aₙ = (2/L) ∫[0,L] f(x) sin(nπx/L) dx
Bₙ = (2/(nπc)) ∫[0,L] g(x) sin(nπx/L) dx
```

### Energy Identity
```
E = (1/2)∫[0,L] [c²(u_x)² + (u_t)²] dx = constant
```

---

## 4. Laplace Equation Formulas

### Two Dimensional (Rectangle)
```
u_xx + u_yy = 0

Case 1: u(0,y) = u(a,y) = 0, u(x,0) = 0, u(x,b) = f(x)

u(x,y) = Σ[n=1 to ∞] Bₙ sin(nπx/a) sinh(nπy/a)

Bₙ = (2/(a sinh(nπb/a))) ∫[0,a] f(x) sin(nπx/a) dx
```

### Two Dimensional (Polar Coordinates)
```
u_rr + (1/r)u_r + (1/r²)u_θθ = 0

u(r,θ) = a₀/2 + Σ[rⁿ/(aⁿ)](aₙcos(nθ) + bₙsin(nθ))

aₙ = (1/π) ∫[0,2π] f(θ)cos(nθ) dθ
bₙ = (1/π) ∫[0,2π] f(θ)sin(nθ) dθ
```

### Poisson Equation
```
u_xx + u_yy = f(x,y)

Solution: u = u_h + u_p
u_h = solution of Laplace equation
u_p = particular solution
```

---

## 5. Separation of Variables Formulas

### General Method
```
For PDE: Lu = 0

Assume: u(x₁,x₂,...,t) = X₁(x₁)X₂(x₂)...T(t)

Substitute into PDE → separate variables → ODEs
```

### Heat Equation Steps
```
Step 1: u(x,t) = X(x)T(t)
Step 2: XT' = kX''T → T'/(kT) = X''/X = -λ
Step 3: X'' + λX = 0, X(0) = 0, X(L) = 0
        → λₙ = (nπ/L)², Xₙ = sin(nπx/L)
Step 4: T' = -kλₙT → Tₙ = e^(-kλₙt)
Step 5: u(x,t) = Σ Bₙ sin(nπx/L) e^(-k(nπ/L)²t)
Step 6: Bₙ = (2/L) ∫[0,L] f(x) sin(nπx/L) dx
```

### Wave Equation Steps
```
Step 1: u(x,t) = X(x)T(t)
Step 2: XT'' = c²X''T → T''/(c²T) = X''/X = -λ
Step 3: X'' + λX = 0, X(0) = 0, X(L) = 0
        → λₙ = (nπ/L)², Xₙ = sin(nπx/L)
Step 4: T'' + c²λₙT = 0
        → Tₙ = Aₙ cos(nπct/L) + Bₙ sin(nπct/L)
Step 5: u(x,t) = Σ sin(nπx/L)[Aₙ cos(nπct/L) + Bₙ sin(nπct/L)]
```

---

## 6. Fourier Series Formulas

### Fourier Sine Series (Odd Extension)
```
f(x) = Σ[n=1 to ∞] bₙ sin(nπx/L)

bₙ = (2/L) ∫[0,L] f(x) sin(nπx/L) dx
```

### Fourier Cosine Series (Even Extension)
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

### Important Series
```
1 = 4/π Σ[n=odd] sin(nπx/L)/n
x = (2L/π) Σ[n=1 to ∞] (-1)^(n+1) sin(nπx/L)/n
x² = L²/3 + (4L²/π²) Σ[n=1 to ∞] (-1)ⁿ cos(nπx/L)/n²
```

---

## 7. Special Functions

### Error Function
```
erf(z) = (2/√π) ∫[0,z] e^(-t²) dt
erfc(z) = 1 - erf(z)
d/dz erf(z) = (2/√π) e^(-z²)
```

### Bessel Functions
```
Jₙ(x) = Σ[k=0 to ∞] (-1)^k (x/2)^(n+2k) / (k! Γ(n+k+1))

Recurrence: Jₙ₋₁(x) + Jₙ₊₁(x) = (2n/x) Jₙ(x)
            Jₙ₋₁(x) - Jₙ₊₁(x) = 2 Jₙ'(x)
```

### Legendre Polynomials
```
Pₙ(x) = (1/2ⁿ n!) dⁿ/dxⁿ (x²-1)ⁿ

P₀(x) = 1
P₁(x) = x
P₂(x) = (3x²-1)/2
P₃(x) = (5x³-3x)/2
```

---

## 8. Important Properties

### Maximum Principle (Laplace)
```
If u_xx + u_yy = 0 in domain D, and u is not constant:
- u attains maximum and minimum on boundary of D
- u cannot have local max/min in interior
```

### Mean Value Property
```
u(center) = (1/2π) ∫[0,2π] u(center + R·cos θ, center + R·sin θ) dθ
```

### Uniqueness
```
Dirichlet problem has at most one solution
Neumann problem has at most one solution (up to additive constant)
```

---

## 9. Charpit's Method (First Order Non-Linear)

```
f(x,y,u,p,q) = 0 where p = ∂u/∂x, q = ∂u/∂y

Auxiliary equations:
dp/(f_x + pf_u) = dq/(f_y + qf_u) = -p dx/(f_p) = -q dy/(f_q)

From these, find relations between p, q, x, y, u
Substitute back to get complete integral
```

---

## 10. Laplace Transform Method for PDEs

### Heat Equation
```
L{u_t} = sU(x,s) - u(x,0) = kU_xx(x,s)

Solve: U_xx - (s/k)U = -u(x,0)/k

Apply BCs, then inverse Laplace
```

### Wave Equation
```
L{u_tt} = s²U - su(x,0) - u_t(x,0) = c²U_xx

Solve: U_xx - (s²/c²)U = -(su(x,0) + u_t(x,0))/c²

Apply BCs, then inverse Laplace
```
