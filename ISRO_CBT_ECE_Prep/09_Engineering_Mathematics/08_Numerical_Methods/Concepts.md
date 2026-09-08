# Numerical Methods - Concepts

## 1. Root Finding Methods

### Bisection Method
- **Idea**: Binary search on interval [a,b] where f(a)f(b) < 0
- **Convergence**: Linear, guaranteed if f continuous
- **Rate**: Halves interval each iteration
- **Pros**: Always converges, simple
- **Cons**: Slow, needs initial bracket

### Newton-Raphson Method
- **Idea**: Use tangent line to approximate root
- **Formula**: x_{n+1} = x_n - f(x_n)/f'(x_n)
- **Convergence**: Quadratic (very fast)
- **Rate**: Number of correct digits roughly doubles
- **Pros**: Fast convergence
- **Cons**: Needs f'(x), may diverge, fails if f'(x) = 0

### Secant Method
- **Idea**: Uses two previous points (no derivative needed)
- **Formula**: x_{n+1} = x_n - f(x_n)(x_n - x_{n-1})/(f(x_n) - f(x_{n-1}))
- **Convergence**: Superlinear (order ≈ 1.618)
- **Pros**: No derivative needed
- **Cons**: Needs two initial points

### Fixed Point Iteration
- **Idea**: Rewrite f(x) = 0 as x = g(x)
- **Formula**: x_{n+1} = g(x_n)
- **Convergence**: If |g'(x*)| < 1 at fixed point x*
- **Pros**: Simple
- **Cons**: May not converge, depends on g choice

### Regula Falsi (False Position)
- **Idea**: Like secant but maintains bracket
- **Formula**: Same as secant but with bracket
- **Convergence**: Linear
- **Pros**: Always maintains bracket
- **Cons**: Can be slow

---

## 2. Interpolation

### Lagrange Interpolation
- **Formula**: P(x) = Σ yᵢ × Lᵢ(x)
- **Lᵢ(x)** = Π(j≠i) (x-xⱼ)/(xᵢ-xⱼ)
- **Pros**: No need to solve system
- **Cons**: Adding point requires recalculation

### Newton's Divided Difference
- **Formula**: P(x) = f[x₀] + f[x₀,x₁](x-x₀) + f[x₀,x₁,x₂](x-x₀)(x-x₁) + ...
- **Pros**: Easy to add points
- **Cons**: Requires divided difference table

### Newton's Forward Difference
- **For equally spaced points**
- **Formula**: P(x₀ + sh) = f(x₀) + sΔf(x₀) + s(s-1)/2! Δ²f(x₀) + ...
- **Where s = (x-x₀)/h, h = spacing**

### Newton's Backward Difference
- **For points near end of table**
- **Formula**: P(xₙ + sh) = f(xₙ) + s∇f(xₙ) + s(s+1)/2! ∇²f(xₙ) + ...
- **Where s = (x-xₙ)/h**

### Spline Interpolation
- **Linear spline**: Piecewise linear
- **Cubic spline**: Piecewise cubic, C² continuous
- **Pros**: Smooth, avoids Runge's phenomenon

---

## 3. Numerical Differentiation

### Forward Difference
```
f'(x) ≈ [f(x+h) - f(x)]/h
Error: O(h)
```

### Backward Difference
```
f'(x) ≈ [f(x) - f(x-h)]/h
Error: O(h)
```

### Central Difference
```
f'(x) ≈ [f(x+h) - f(x-h)]/(2h)
Error: O(h²)
```

### Second Derivative
```
f''(x) ≈ [f(x+h) - 2f(x) + f(x-h)]/h²
Error: O(h²)
```

---

## 4. Numerical Integration

### Trapezoidal Rule
```
∫[a,b] f(x) dx ≈ h/2 [f(a) + 2Σf(xᵢ) + f(b)]

where h = (b-a)/n, xᵢ = a + ih

Error: O(h²) (proportional to f'')
```

### Simpson's 1/3 Rule
```
∫[a,b] f(x) dx ≈ h/3 [f(a) + 4Σf(x_odd) + 2Σf(x_even) + f(b)]

Error: O(h⁴) (proportional to f⁴⁾)

Requires even number of intervals (odd number of points)
```

### Simpson's 3/8 Rule
```
∫[a,b] f(x) dx ≈ 3h/8 [f(a) + 3f(x₁) + 3f(x₂) + 2f(x₃) + 3f(x₄) + ... + f(b)]

Error: O(h⁵)

Requires number of intervals multiple of 3
```

### Boole's Rule
```
∫[a,b] f(x) dx ≈ 2h/45 [7f(a) + 32f(x₁) + 12f(x₂) + 32f(x₃) + 7f(x₄)]

Error: O(h⁶)
```

### Gaussian Quadrature
```
∫[-1,1] f(x) dx ≈ Σ wᵢ f(xᵢ)

where xᵢ are roots of Legendre polynomial
wᵢ are weights

Higher accuracy for same number of function evaluations
```

---

## 5. Ordinary Differential Equations

### Euler's Method
```
y_{n+1} = y_n + h·f(x_n, y_n)

Error: O(h) (first order)
Simple but inaccurate for large h
```

### Improved Euler (Heun)
```
Predictor: y*_{n+1} = y_n + h·f(x_n, y_n)
Corrector: y_{n+1} = y_n + h/2 [f(x_n, y_n) + f(x_{n+1}, y*_{n+1})]

Error: O(h²) (second order)
```

### Runge-Kutta (RK4)
```
k₁ = h·f(x_n, y_n)
k₂ = h·f(x_n + h/2, y_n + k₁/2)
k₃ = h·f(x_n + h/2, y_n + k₂/2)
k₄ = h·f(x_n + h, y_n + k₃)

y_{n+1} = y_n + (k₁ + 2k₂ + 2k₃ + k₄)/6

Error: O(h⁴) (fourth order)
Best balance of accuracy and complexity
```

### Taylor Series Method
```
y_{n+1} = y_n + hy' + h²y''/2! + h³y'''/3! + ...

Requires derivatives of f
Error: O(h^n) for nth order method
```

---

## 6. Systems of Linear Equations

### Direct Methods

#### Gaussian Elimination
```
Forward elimination to upper triangular
Back substitution
Complexity: O(n³)
```

#### LU Decomposition
```
A = LU (Lower × Upper)
Solve Ly = b, then Ux = y
Efficient for multiple right-hand sides
```

#### Gauss-Jordan Elimination
```
Reduce to reduced row echelon form
Gives inverse directly
```

### Iterative Methods

#### Jacobi Method
```
x_i^(k+1) = (b_i - Σ(j≠i) a_ij x_j^(k)) / a_ii

Converges if matrix is diagonally dominant
```

#### Gauss-Seidel Method
```
x_i^(k+1) = (b_i - Σ(j<i) a_ij x_j^(k+1) - Σ(j>i) a_ij x_j^(k)) / a_ii

Uses most recent values
Faster convergence than Jacobi
```

---

## 7. Numerical Solutions of PDEs

### Finite Difference Method
```
Replace derivatives with differences:

∂u/∂t ≈ (u^{n+1}_i - u^n_i)/Δt
∂²u/∂x² ≈ (u^n_{i+1} - 2u^n_i + u^n_{i-1})/Δx²
```

### Explicit Scheme (Heat Equation)
```
u^{n+1}_i = u^n_i + r(u^n_{i+1} - 2u^n_i + u^n_{i-1})

where r = kΔt/Δx²

Stable if r ≤ 1/2
```

### Implicit Scheme (Heat Equation)
```
-r·u^{n+1}_{i-1} + (1+2r)u^{n+1}_i - r·u^{n+1}_{i+1} = u^n_i

Unconditionally stable
Requires solving tridiagonal system
```

### Crank-Nicolson
```
Average of explicit and implicit
Second order in both time and space
Unconditionally stable
```

---

## 8. Error Analysis

### Types of Error
```
Round-off error: Finite precision arithmetic
Truncation error: Approximating infinite process
Discretization error: Approximating continuous with discrete
```

### Error Propagation
```
If y = f(x₁, x₂, ..., xₙ):
Δy ≈ Σ |∂f/∂xᵢ| Δxᵢ
```

### Condition Number
```
κ(A) = ||A|| · ||A⁻¹||

Large κ: problem is ill-conditioned
Small κ: problem is well-conditioned
```

---

## 9. Convergence Concepts

### Order of Convergence
```
If lim |e_{n+1}|/|e_n|^p = C:
p = order of convergence
C = asymptotic error constant

p = 1: linear
p = 2: quadratic
p = 1.618: superlinear (secant)
```

### Stability
- A method is stable if errors don't grow
- **A-stable**: Stable for all eigenvalues in left half-plane
- **L-stable**: A-stable and → 0 as h → ∞

---

## 10. Summary Table

| Method | Order | Derivative Needed | Notes |
|--------|-------|------------------|-------|
| Bisection | 1 | No | Always converges |
| Newton-Raphson | 2 | Yes | Fast but may diverge |
| Secant | 1.618 | No | Good compromise |
| Euler | 1 | No | Simple, inaccurate |
| Heun | 2 | No | Better than Euler |
| RK4 | 4 | No | Best general method |
| Trapezoidal | 2 | No | Simple integration |
| Simpson's 1/3 | 4 | No | Good accuracy |
| Simpson's 3/8 | 5 | No | Better than 1/3 |
