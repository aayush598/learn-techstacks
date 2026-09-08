# Numerical Methods - Formulas

## 1. Root Finding Formulas

### Bisection Method
```
c = (a + b)/2

if f(a)f(c) < 0: b = c
else: a = c

Interval halves each iteration
Error ≤ (b-a)/2^n after n iterations
```

### Newton-Raphson
```
x_{n+1} = x_n - f(x_n)/f'(x_n)

Convergence: x_{n+1} - x* ≈ C(x_n - x*)²
Error: O(h²) quadratic convergence
```

### Secant Method
```
x_{n+1} = x_n - f(x_n)(x_n - x_{n-1})/(f(x_n) - f(x_{n-1}))

Convergence: order ≈ 1.618 (golden ratio)
Error: O(h^φ) where φ ≈ 1.618
```

### Fixed Point Iteration
```
x_{n+1} = g(x_n)

Converges if |g'(x*)| < 1
Error: |x_{n+1} - x*| ≈ |g'(x*)| |x_n - x*|
```

### Regula Falsi
```
x_{n+1} = a_n - f(a_n)(b_n - a_n)/(f(b_n) - f(a_n))

Maintains bracket: f(a_n)f(b_n) < 0 always
```

---

## 2. Interpolation Formulas

### Lagrange Interpolation
```
P(x) = Σ[i=0 to n] yᵢ Lᵢ(x)

Lᵢ(x) = Π[j≠i] (x - xⱼ)/(xᵢ - xⱼ)

Degree ≤ n polynomial through n+1 points
```

### Newton's Divided Difference
```
f[x_i] = y_i
f[x_i, x_{i+1}] = (f[x_{i+1}] - f[x_i])/(x_{i+1} - x_i)
f[x_i, x_{i+1}, x_{i+2}] = (f[x_{i+1}, x_{i+2}] - f[x_i, x_{i+1}])/(x_{i+2} - x_i)

P(x) = f[x₀] + f[x₀,x₁](x-x₀) + f[x₀,x₁,x₂](x-x₀)(x-x₁) + ...
```

### Newton's Forward Difference (Equally Spaced)
```
x = x₀ + sh, s = (x - x₀)/h

P(x) = f(x₀) + sΔf(x₀) + s(s-1)/2! Δ²f(x₀) + s(s-1)(s-2)/3! Δ³f(x₀) + ...

Δf(x₀) = f(x₁) - f(x₀)
Δ²f(x₀) = Δf(x₁) - Δf(x₀)
```

### Newton's Backward Difference
```
x = xₙ + sh, s = (x - xₙ)/h

P(x) = f(xₙ) + s∇f(xₙ) + s(s+1)/2! ∇²f(xₙ) + ...

∇f(xₙ) = f(xₙ) - f(xₙ₋₁)
∇²f(xₙ) = ∇f(xₙ) - ∇f(xₙ₋₁)
```

### Stirling's Formula (Central Difference)
```
P(x) = f(x₀) + sδf(x₀) + s²/2! δ²f(x₀) + s(s²-1)/3! δ³f(x₀) + ...

δf(x₀) = f(x_{1/2}) - f(x_{-1/2}) [central difference]
```

---

## 3. Numerical Differentiation Formulas

### Forward Difference
```
f'(x) ≈ [f(x+h) - f(x)]/h

Error: -hf''(x)/2 - ... = O(h)
```

### Backward Difference
```
f'(x) ≈ [f(x) - f(x-h)]/h

Error: hf''(x)/2 - ... = O(h)
```

### Central Difference
```
f'(x) ≈ [f(x+h) - f(x-h)]/(2h)

Error: -h²f'''(x)/6 - ... = O(h²)
```

### Second Derivative
```
f''(x) ≈ [f(x+h) - 2f(x) + f(x-h)]/h²

Error: O(h²)
```

### Higher Order Central Difference
```
f'(x) ≈ [-f(x+2h) + 8f(x+h) - 8f(x-h) + f(x-2h)]/(12h)

Error: O(h⁴)
```

---

## 4. Numerical Integration Formulas

### Trapezoidal Rule
```
∫[a,b] f(x) dx ≈ h/2 [f(a) + 2f(x₁) + 2f(x₂) + ... + 2f(x_{n-1}) + f(b)]

where h = (b-a)/n

Error: -(b-a)³ f''(ξ)/(12n²) = O(h²)
```

### Simpson's 1/3 Rule
```
∫[a,b] f(x) dx ≈ h/3 [f(a) + 4f(x₁) + 2f(x₂) + 4f(x₃) + ... + 4f(x_{n-1}) + f(b)]

n must be even

Error: -(b-a)⁵ f⁴(ξ)/(180n⁴) = O(h⁴)
```

### Simpson's 3/8 Rule
```
∫[a,b] f(x) dx ≈ 3h/8 [f(a) + 3f(x₁) + 3f(x₂) + 2f(x₃) + 3f(x₄) + ... + f(b)]

n must be multiple of 3

Error: O(h⁵)
```

### Boole's Rule
```
∫[a,b] f(x) dx ≈ 2h/45 [7f(a) + 32f(x₁) + 12f(x₂) + 32f(x₃) + 7f(x₄)]

Error: O(h⁶)
```

### Gaussian Quadrature
```
∫[-1,1] f(x) dx ≈ Σ[i=1 to n] wᵢ f(xᵢ)

2-point: x₁ = -1/√3, x₂ = 1/√3, w₁ = w₂ = 1
3-point: x₁ = -√(3/5), x₂ = 0, x₃ = √(3/5)
         w₁ = 5/9, w₂ = 8/9, w₃ = 5/9
```

---

## 5. ODE Solver Formulas

### Euler's Method
```
y_{n+1} = y_n + h·f(x_n, y_n)

Global error: O(h)
Local error: O(h²)
```

### Improved Euler (Heun)
```
k₁ = f(x_n, y_n)
k₂ = f(x_n + h, y_n + h·k₁)
y_{n+1} = y_n + h/2 (k₁ + k₂)

Global error: O(h²)
```

### Runge-Kutta (RK4)
```
k₁ = f(x_n, y_n)
k₂ = f(x_n + h/2, y_n + h·k₁/2)
k₃ = f(x_n + h/2, y_n + h·k₂/2)
k₄ = f(x_n + h, y_n + h·k₃)

y_{n+1} = y_n + h/6 (k₁ + 2k₂ + 2k₃ + k₄)

Global error: O(h⁴)
```

### Taylor Series Method
```
y_{n+1} = y_n + hy' + h²y''/2! + h³y'''/3! + h⁴y⁴⁾/4! + ...

Requires computing derivatives of f
```

---

## 6. System of Linear Equations

### Gaussian Elimination
```
Forward elimination: O(n³)
Back substitution: O(n²)

Total: O(n³)
```

### LU Decomposition (Doolittle)
```
A = LU where L has 1s on diagonal

L_{ij} = (a_{ij} - Σ_{k=1}^{j-1} L_{ik}U_{kj})/U_{jj}
U_{ij} = a_{ij} - Σ_{k=1}^{i-1} L_{ik}U_{kj}
```

### Jacobi Iteration
```
x_i^(k+1) = (b_i - Σ_{j≠i} a_{ij} x_j^(k)) / a_{ii}

Converges if: |a_{ii}| > Σ_{j≠i} |a_{ij}| (diagonally dominant)
```

### Gauss-Seidel
```
x_i^(k+1) = (b_i - Σ_{j<i} a_{ij} x_j^(k+1) - Σ_{j>i} a_{ij} x_j^(k)) / a_{ii}

Uses updated values immediately
Faster convergence than Jacobi
```

---

## 7. PDE Finite Difference Formulas

### Heat Equation (Explicit)
```
u^{n+1}_i = u^n_i + r(u^n_{i+1} - 2u^n_i + u^n_{i-1})

r = kΔt/Δx²

Stable if r ≤ 1/2
```

### Heat Equation (Implicit)
```
-r·u^{n+1}_{i-1} + (1+2r)u^{n+1}_i - r·u^{n+1}_{i+1} = u^n_i

Unconditionally stable
Tridiagonal system
```

### Crank-Nicolson
```
-r/2·u^{n+1}_{i-1} + (1+r)u^{n+1}_i - r/2·u^{n+1}_{i+1} = 
r/2·u^n_{i-1} + (1-r)u^n_i + r/2·u^n_{i+1}

Second order in time and space
Unconditionally stable
```

### Wave Equation
```
u^{n+1}_i = 2u^n_i - u^{n-1}_i + c²r²(u^n_{i+1} - 2u^n_i + u^n_{i-1})

where r = Δt/Δx
Stable if cr ≤ 1
```

---

## 8. Error Formulas

### Local Truncation Error
```
LTE = y(x_{n+1}) - y_{n+1} (single step error)
```

### Global Truncation Error
```
GTE = y(x_n) - y_n (accumulated error)

For O(h^p) method: GTE = O(h^p)
```

### Condition Number
```
κ(A) = ||A|| · ||A⁻¹||

Well-conditioned: κ ≈ 1
Ill-conditioned: κ >> 1
```

---

## 9. Convergence Criteria

### Newton-Raphson
```
Converges if:
1. f'(x*) ≠ 0
2. Initial guess close to root
3. f''(x) bounded near root
```

### Fixed Point Iteration
```
Converges if:
1. g is continuous on [a,b]
2. g maps [a,b] to [a,b]
3. |g'(x)| < 1 for all x ∈ [a,b]
```

### Iterative Methods (Linear Systems)
```
Converges if:
1. Matrix is diagonally dominant
2. Or: Matrix is positive definite (for Gauss-Seidel)
3. Spectral radius of iteration matrix < 1
```

---

## 10. Quick Reference Table

| Method | Formula | Error | Notes |
|--------|---------|-------|-------|
| Bisection | c = (a+b)/2 | O((b-a)/2ⁿ) | Always converges |
| Newton | x - f/f' | O(h²) | Needs derivative |
| Secant | x - f(x)(x-xₚ)/(f-fₚ) | O(h^1.618) | No derivative |
| Euler | y + hf | O(h) | Simple |
| RK4 | y + h/6(k₁+2k₂+2k₃+k₄) | O(h⁴) | Best general |
| Trapezoidal | h/2(f₀+2f₁+...+fₙ) | O(h²) | Simple |
| Simpson's | h/3(f₀+4f₁+2f₂+...+fₙ) | O(h⁴) | Good accuracy |
