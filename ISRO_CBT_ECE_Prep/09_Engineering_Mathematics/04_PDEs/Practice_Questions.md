# Partial Differential Equations - Practice Questions

## Easy Level

### Q1. Classify the PDE
Classify: u_xx + u_yy = 0.

**Solution**:
- A = 1, B = 0, C = 1
- B² - 4AC = 0 - 4 = -4 < 0
- **Elliptic** (Laplace equation)

---

### Q2. Separation of Variables (Setup)
Set up separation for u_t = u_xx.

**Solution**:
- Assume u(x,t) = X(x)T(t)
- XT' = X''T → T'/(T) = X''/X = -λ
- **X'' + λX = 0, T' + λT = 0**

---

### Q3. Fourier Sine Coefficient
Find b₁ for f(x) = x on [0,π].

**Solution**:
- b₁ = (2/π) ∫[0,π] x sin(x) dx
- = (2/π)[-x cos(x) + sin(x)]₀π
- = (2/π)(π + 0) = **2**

---

### Q4. Heat Equation Solution
Solve u_t = u_xx with u(0,t) = u(π,t) = 0 and u(x,0) = sin(x).

**Solution**:
- u(x,t) = Σ Bₙ sin(nx) e^(-n²t)
- B₁ = (2/π) ∫[0,π] sin(x)·sin(x) dx = 1
- Bₙ = 0 for n ≠ 1
- **u(x,t) = sin(x)e^(-t)**

---

### Q5. Wave Equation d'Alembert
Solve u_tt = u_xx with u(x,0) = sin(x) and u_t(x,0) = 0.

**Solution**:
- d'Alembert: u(x,t) = [sin(x+t) + sin(x-t)]/2
- = sin(x)cos(t)
- **u(x,t) = sin(x)cos(t)**

---

## Medium Level

### Q6. Heat Equation (Finite Rod)
Solve u_t = 4u_xx, u(0,t) = u(2,t) = 0, u(x,0) = x(2-x).

**Solution**:
- u(x,t) = Σ Bₙ sin(nπx/2) e^(-n²π²t)
- Bₙ = ∫[0,2] x(2-x) sin(nπx/2) dx
- B₁ = 32/(π³), B₂ = 0, B₃ = 32/(27π³)
- **u(x,t) = (32/π³)[sin(πx/2)e^(-π²t) + sin(3πx/2)e^(-9π²t)/27 + ...]**

---

### Q7. Laplace Equation (Rectangle)
Solve u_xx + u_yy = 0 with u(0,y) = u(π,y) = 0, u(x,0) = 0, u(x,1) = sin(x).

**Solution**:
- u(x,y) = Σ Bₙ sin(nx) sinh(ny)/sinh(n)
- Only n=1 survives: B₁ = 1
- **u(x,y) = sin(x)sinh(y)/sinh(1)**

---

### Q8. Classification
Classify: u_xx + 2u_xy + u_yy + u_x = 0.

**Solution**:
- A = 1, B = 2, C = 1
- B² - 4AC = 4 - 4 = 0
- **Parabolic**

---

### Q9. Wave Equation (Non-Zero Initial Velocity)
Solve u_tt = 4u_xx, u(0,t) = u(1,t) = 0, u(x,0) = 0, u_t(x,0) = x.

**Solution**:
- u(x,t) = Σ Bₙ sin(nπx) sin(2nπt)/(2nπ)
- Bₙ = 2∫[0,1] x sin(nπx) dx = 2(-1)^(n+1)/(nπ)
- **u(x,t) = Σ [2(-1)^(n+1)/(nπ)²] sin(nπx) sin(2nπt)**

---

### Q10. Fourier Series Expansion
Expand f(x) = x² as Fourier cosine series on [0,π].

**Solution**:
- a₀ = (2/π) ∫[0,π] x² dx = 2π²/3
- aₙ = (2/π) ∫[0,π] x² cos(nx) dx = 4(-1)ⁿ/n²
- **x² = π²/3 + 4 Σ[n=1 to ∞] (-1)ⁿ cos(nx)/n²**

---

### Q11. Non-Homogeneous Heat
Solve u_t = u_xx + e^(-t)sin(x), u(0,t) = u(π,t) = 0, u(x,0) = sin(x).

**Solution**:
- Assume u(x,t) = T(t)sin(x)
- T' = -T + e^(-t)
- Linear ODE: T' + T = e^(-t)
- IF = e^t: T·e^t = ∫ e^(-t)·e^t dt = t + C
- T = (t + C)e^(-t)
- T(0) = 1 → C = 1
- **u(x,t) = (t+1)e^(-t)sin(x)**

---

### Q12. Laplace Equation (Polar)
Solve ∇²u = 0 in circle of radius 1 with u(1,θ) = cos(2θ).

**Solution**:
- u(r,θ) = Σ rⁿ(aₙcos(nθ) + bₙsin(nθ))
- Only a₂ = 1, all others 0
- **u(r,θ) = r²cos(2θ)**

---

### Q13. Neumann BC Heat
Solve u_t = u_xx with u_x(0,t) = u_x(π,t) = 0, u(x,0) = π - x.

**Solution**:
- u(x,t) = a₀/2 + Σ aₙ cos(nx) e^(-n²t)
- a₀ = (2/π) ∫[0,π] (π-x) dx = π
- aₙ = (2/π) ∫[0,π] (π-x) cos(nx) dx = 0 for n ≥ 1
- **u(x,t) = π/2**

---

### Q14. Wave Equation (General)
Solve u_tt = 9u_xx, u(0,t) = u(π,t) = 0, u(x,0) = sin(x), u_t(x,0) = 0.

**Solution**:
- c = 3
- u(x,t) = sin(x)cos(3t)
- **u(x,t) = sin(x)cos(3t)**

---

### Q15. Separation of Variables (2D)
Solve u_xx + u_yy = 0 on square [0,π]×[0,π] with u = 0 on three sides and u(x,π) = sin(x).

**Solution**:
- u(x,y) = Σ Bₙ sin(nx) sinh(ny)/sinh(nπ)
- Only n=1 survives: B₁ = 1
- **u(x,y) = sin(x)sinh(y)/sinh(π)**

---

## Hard Level

### Q16. Non-Homogeneous Boundary
Solve u_t = u_xx, u(0,t) = 1, u(π,t) = 0, u(x,0) = 0.

**Solution**:
- Steady state: v(x) = 1 - x/π
- Let u = v + w, then w satisfies:
  w_t = w_xx, w(0,t) = 0, w(π,t) = 0, w(x,0) = -(1-x/π)
- w(x,t) = Σ Bₙ sin(nx) e^(-n²t)
- Bₙ = (2/π) ∫[0,π] (x/π-1) sin(nx) dx = -2/(nπ)
- **u(x,t) = 1 - x/π + Σ [-2/(nπ)] sin(nx) e^(-n²t)**

---

### Q17. D'Alembert (Semi-Infinite)
Solve u_tt = u_xx, x > 0, u(0,t) = 0, u(x,0) = f(x), u_t(x,0) = 0.

**Solution**:
- Extend f(x) as odd function: F(x) = -f(-x) for x < 0
- d'Alembert: u(x,t) = [F(x+t) + F(x-t)]/2
- For x > t: u(x,t) = [f(x+t) + f(x-t)]/2
- For 0 < x < t: u(x,t) = [f(x+t) - f(t-x)]/2

---

### Q18. Poisson Equation
Solve u_xx + u_yy = -2 on unit square with u = 0 on boundary.

**Solution**:
- This is Poisson's equation with homogeneous BCs
- Series solution involves eigenfunctions of Laplacian
- u(x,y) = Σ Σ Aₘₙ sin(mπx) sin(nπy)
- Aₘₙ = (4/(mπ)² + (nπ)²) × (coefficient of -2 in expansion)

---

### Q19. Heat Equation (Insulated End)
Solve u_t = u_xx, u_x(0,t) = 0, u(π,t) = 0, u(x,0) = 1.

**Solution**:
- Mixed BCs → eigenfunctions: cos((n+1/2)x)
- u(x,t) = Σ Bₙ cos((n+1/2)x) e^(-(n+1/2)²t)
- Bₙ = (2/π) ∫[0,π] cos((n+1/2)x) dx = 2sin((n+1/2)π)/((n+1/2)π)
- **u(x,t) = Σ [2(-1)ⁿ/((n+1/2)π)] cos((n+1/2)x) e^(-(n+1/2)²t)**

---

### Q20. Laplace (Upper Half Plane)
Solve u_xx + u_yy = 0 in upper half-plane, u(x,0) = e^(-|x|).

**Solution**:
- Use Fourier transform in x
- û(k,y) = e^(-|k|y)
- Inverse: u(x,y) = y/(π(x²+y²)) * convolution with e^(-|x|)
- **u(x,y) = (1/π)[arctan((x+1)/y) - arctan((x-1)/y)]**

---

### Q21. Wave Equation (Non-Zero Boundary)
Solve u_tt = u_xx, u(0,t) = t, u(1,t) = 0, u(x,0) = 0, u_t(x,0) = 0.

**Solution**:
- Steady state: v(x,t) = t(1-x)
- w = u - v satisfies homogeneous BCs
- w_tt = w_xx + 2(1-x) [source term from v_tt]
- Series solution with source term

---

### Q22. Fourier Series (Half Range)
Expand f(x) = 1 as Fourier sine series on [0,π].

**Solution**:
- bₙ = (2/π) ∫[0,π] sin(nx) dx = 2(1-cos(nπ))/(nπ)
- bₙ = 4/(nπ) for odd n, 0 for even n
- **f(x) = (4/π) Σ[n=odd] sin(nx)/n**

---

### Q23. Laplace Equation (Neumann Problem)
Solve u_xx + u_yy = 0 on [0,π]×[0,π] with u_y(x,0) = sin(x), u_y(x,π) = 0, u(0,y) = u(π,y) = 0.

**Solution**:
- u(x,y) = Σ Bₙ sin(nx) cosh(n(y-π))/sinh(nπ)
- B₁ = 1, Bₙ = 0 for n ≠ 1
- **u(x,y) = sin(x)cosh(y-π)/sinh(π)**

---

### Q24. Heat Equation (Source Term)
Solve u_t = u_xx + sin(x), u(0,t) = u(π,t) = 0, u(x,0) = 0.

**Solution**:
- Particular solution: v(x) = sin(x) (steady state with source)
- w = u - v: w_t = w_xx, w(0,t) = w(π,t) = 0, w(x,0) = -sin(x)
- w(x,t) = -sin(x)e^(-t)
- **u(x,t) = sin(x)(1 - e^(-t))**

---

### Q25. Uniqueness Proof
Show that if u₁ and u₂ both satisfy Laplace equation with same Dirichlet BCs, then u₁ = u₂.

**Solution**:
- Let w = u₁ - u₂
- ∇²w = 0 in D, w = 0 on ∂D
- By maximum principle: max(w) = min(w) = 0
- Therefore w ≡ 0, so u₁ = u₂ ✓

---

## ISRO-Focused Questions

### Q26. Quick Classification
Classify: u_xx - 2u_xy + u_yy = 0.

**Solution**:
- A = 1, B = -2, C = 1
- B² - 4AC = 4 - 4 = 0
- **Parabolic**

---

### Q27. Eigenvalue Identification
What are the eigenvalues for u_tt = 4u_xx with u(0,t) = u(π,t) = 0?

**Solution**:
- λₙ = (nπ/π)² = n²
- **λₙ = n² for n = 1, 2, 3, ...**

---

### Q28. Boundary Condition Type
u(x,0) = sin(x) is what type of condition?

**Solution**: **Initial condition** (specifies initial displacement/temperature)

---

### Q29. Heat Equation Steady State
What is the steady state solution of u_t = u_xx with u(0) = 1, u(1) = 0?

**Solution**:
- Steady state: u_xx = 0 → u = Ax + B
- u(0) = 1 → B = 1
- u(1) = 0 → A + 1 = 0 → A = -1
- **u(x) = 1 - x**

---

### Q30. d'Alembert Quick
For u_tt = c²u_xx with f(x) = sin(x), g(x) = 0, what is u(x,t)?

**Solution**:
- u(x,t) = [sin(x+ct) + sin(x-ct)]/2 = sin(x)cos(ct)
- **u(x,t) = sin(x)cos(ct)**
