# Differential Equations - Practice Questions

## Easy Level

### Q1. Variable Separable
Solve: dy/dx = xy

**Solution**:
- dy/y = x dx
- ln|y| = x²/2 + C
- **y = Ae^(x²/2)**

---

### Q2. Linear First Order
Solve: dy/dx + y = eˣ

**Solution**:
- P(x) = 1, IF = eˣ
- y·eˣ = ∫ eˣ·eˣ dx = e^(2x)/2 + C
- **y = eˣ/2 + Ce^(-x)**

---

### Q3. Complementary Function
Find CF of y'' - 3y' + 2y = 0.

**Solution**:
- Auxiliary: m² - 3m + 2 = 0 → (m-1)(m-2) = 0
- **CF = c₁eˣ + c₂e^(2x)**

---

### Q4. Particular Integral
Find PI of y'' + y = sin(x).

**Solution**:
- sin(x) corresponds to root ±i of auxiliary
- Assume PI = x(A cos(x) + B sin(x))
- Substituting: 2A cos(x) + 2B sin(x) = sin(x)
- A = 0, B = 1/2
- **PI = x sin(x)/2**

---

### Q5. Exact Equation
Solve: (2xy + 3)dx + (x² + 4y)dy = 0.

**Solution**:
- M = 2xy + 3, N = x² + 4y
- ∂M/∂y = 2x = ∂N/∂x → Exact
- ∫(2xy+3)dx = x²y + 3x + f(y)
- ∂/∂y(x²y + 3x) = x² + f'(y) = x² + 4y → f'(y) = 4y → f(y) = 2y²
- **x²y + 3x + 2y² = C**

---

## Medium Level

### Q6. Bernoulli's Equation
Solve: dy/dx + y/x = x²y².

**Solution**:
- Bernoulli with n = 2, P = 1/x, Q = x²
- Let v = y⁻¹, dv/dx = -y⁻²(dy/dx)
- -dv/dx + v/x = -x² → dv/dx - v/x = x²
- IF = e^(-∫1/x dx) = 1/x
- v/x = ∫ x²/x dx = x²/2 + C
- v = x³/2 + Cx
- **y = 1/(x³/2 + Cx)**

---

### Q7. Second Order Non-Homogeneous
Solve: y'' - 5y' + 6y = eˣ.

**Solution**:
- CF: m² - 5m + 6 = 0 → (m-2)(m-3) = 0 → CF = c₁e^(2x) + c₂e^(3x)
- PI: Assume Aeˣ (1 not root of auxiliary)
- A - 5A + 6A = 1 → 2A = 1 → A = 1/2
- **y = c₁e^(2x) + c₂e^(3x) + eˣ/2**

---

### Q8. Cauchy-Euler
Solve: x²y'' - 2xy' + 2y = 0.

**Solution**:
- Auxiliary: m(m-1) - 2m + 2 = 0 → m² - 3m + 2 = 0
- (m-1)(m-2) = 0 → m = 1, 2
- **y = c₁x + c₂x²**

---

### Q9. Laplace Transform
Solve: y'' + y = sin(t), y(0) = 0, y'(0) = 0.

**Solution**:
- L{y''} + L{y} = L{sin(t)}
- s²Y(s) - sy(0) - y'(0) + Y(s) = 1/(s²+1)
- Y(s)(s²+1) = 1/(s²+1)
- Y(s) = 1/(s²+1)²
- **y(t) = (sin(t) - t·cos(t))/2**

---

### Q10. Initial Value Problem
Solve: y' + 2y = 4, y(0) = 1.

**Solution**:
- IF = e^(2x)
- y·e^(2x) = ∫ 4e^(2x) dx = 2e^(2x) + C
- y = 2 + Ce^(-2x)
- y(0) = 1: 1 = 2 + C → C = -1
- **y = 2 - e^(-2x)**

---

### Q11. Variation of Parameters
Solve: y'' + y = sec(x).

**Solution**:
- CF = c₁cos(x) + c₂sin(x)
- W = cos²(x) + sin²(x) = 1
- PI = -cos(x)∫sin(x)sec(x)dx + sin(x)∫cos(x)sec(x)dx
- = -cos(x)∫tan(x)dx + sin(x)∫1 dx
- = -cos(x)·ln|sec(x)| + sin(x)·x
- **y = c₁cos(x) + c₂sin(x) - cos(x)ln|sec(x)| + x·sin(x)**

---

### Q12. Second Order with Repeated Root
Solve: y'' - 4y' + 4y = 0.

**Solution**:
- Auxiliary: m² - 4m + 4 = 0 → (m-2)² = 0
- m = 2 (repeated)
- **y = (c₁ + c₂x)e^(2x)**

---

### Q13. Complex Roots
Solve: y'' + 2y' + 5y = 0.

**Solution**:
- Auxiliary: m² + 2m + 5 = 0
- m = (-2 ± √(4-20))/2 = -1 ± 2i
- **y = e^(-x)(c₁cos(2x) + c₂sin(2x))**

---

### Q14. Homogeneous First Order
Solve: dy/dx = (x + y)/x.

**Solution**:
- dy/dx = 1 + y/x (homogeneous)
- Let y = vx → v + x(dv/dx) = 1 + v
- x(dv/dx) = 1 → dv = dx/x
- v = ln|x| + C
- **y = x(ln|x| + C)**

---

### Q15. System of ODEs
Solve: dx/dt = 2x + y, dy/dt = -x + 2y.

**Solution**:
- Eigenvalue problem: |2-λ  1| = 0 → (2-λ)² + 1 = 0
                      |-1  2-λ|
- λ = 2 ± i
- **x = e^(2t)(c₁cos(t) + c₂sin(t))**
- **y = e^(2t)(-c₁sin(t) + c₂cos(t))**

---

## Hard Level

### Q16. Non-Homogeneous with Resonance
Solve: y'' + 4y = sin(2x).

**Solution**:
- CF: m² + 4 = 0 → m = ±2i → CF = c₁cos(2x) + c₂sin(2x)
- PI: sin(2x) is part of CF → PI = x(A cos(2x) + B sin(2x))
- Substitute: 4B cos(2x) - 4A sin(2x) = sin(2x)
- A = -1/4, B = 0
- **y = c₁cos(2x) + c₂sin(2x) - x cos(2x)/4**

---

### Q17. Laplace Transform (Step Function)
Solve: y'' + y = u(t-π), y(0) = 0, y'(0) = 0.

**Solution**:
- L{y''} + L{y} = L{u(t-π)}
- s²Y + Y = e^(-πs)/s
- Y(s) = e^(-πs)/(s(s²+1))
- Partial fractions: 1/(s(s²+1)) = 1/s - s/(s²+1)
- **y(t) = u(t-π)(1 - cos(t-π)) = u(t-π)(1 + cos(t))**

---

### Q18. Legendre's Linear Equation
Solve: (x+1)²y'' + (x+1)y' - y = 0.

**Solution**:
- Let x+1 = e^t
- Auxiliary: m(m-1) + m - 1 = 0 → m² - 1 = 0
- m = ±1
- **y = c₁(x+1) + c₂/(x+1)**

---

### Q19. Riccati's Equation
Given y' = 1 - y², and y₁ = 1 is a particular solution, find general solution.

**Solution**:
- Let y = 1 + 1/v
- dy/dx = -v⁻²(dv/dx)
- -v⁻²(dv/dx) = 1 - (1 + 1/v)² = -2/v - 1/v²
- dv/dx = 2v + 1
- Linear: dv/dx - 2v = 1
- IF = e^(-2x)
- v·e^(-2x) = ∫ e^(-2x) dx = -e^(-2x)/2 + C
- v = -1/2 + Ce^(2x)
- **y = 1 + 1/(-1/2 + Ce^(2x))**

---

### Q20. Damped Oscillation
Solve: y'' + 2y' + 5y = 0, y(0) = 1, y'(0) = -1.

**Solution**:
- CF: m² + 2m + 5 = 0 → m = -1 ± 2i
- y = e^(-x)(c₁cos(2x) + c₂sin(2x))
- y(0) = 1 → c₁ = 1
- y'(0) = -1: -c₁ + 2c₂ = -1 → -1 + 2c₂ = -1 → c₂ = 0
- **y = e^(-x)cos(2x)**

---

### Q21. Wronskian Check
Are eˣ and e^(-x) linearly independent?

**Solution**:
- W(eˣ, e⁻ˣ) = |eˣ  e⁻ˣ| = eˣ(-e⁻ˣ) - e⁻ˣ(eˣ) = -1 - 1 = -2
                 |eˣ  -e⁻ˣ|
- **W ≠ 0, so linearly independent**

---

### Q22. Operator Method
Solve (D² + 4)y = sin(2x) using operator method.

**Solution**:
- PI = 1/(D²+4) · sin(2x)
- D² = -4 → denominator = 0 → resonance
- PI = x · 1/(2D) · sin(2x) = x/2 · (-cos(2x)/2) = -x cos(2x)/4

---

### Q23. Simultaneous Equations
Solve: dx/dt + dy/dt = x + y, dx/dt - dy/dt = x - y.

**Solution**:
- Adding: 2dx/dt = 2x → dx/dt = x → x = c₁e^t
- Subtracting: 2dy/dt = 2y → dy/dt = y → y = c₂e^t
- But need to check consistency: original equations must be satisfied
- Actually: dx/dt = x, dy/dt = y are independent
- **x = c₁e^t, y = c₂e^t**

---

### Q24. Euler-Cauchy with Complex Roots
Solve: x²y'' + xy' + y = 0.

**Solution**:
- Auxiliary: m(m-1) + m + 1 = 0 → m² + 1 = 0
- m = ±i
- **y = c₁cos(ln x) + c₂sin(ln x)**

---

### Q25. Higher Order
Solve: y''' - 6y'' + 11y' - 6y = 0.

**Solution**:
- Auxiliary: m³ - 6m² + 11m - 6 = 0
- m = 1 is root → (m-1)(m²-5m+6) = 0
- (m-1)(m-2)(m-3) = 0
- **y = c₁eˣ + c₂e^(2x) + c₃e^(3x)**

---

## ISRO-Focused Questions

### Q26. Quick Linear ODE
Solve: dy/dx + 2y = 0.

**Solution**:
- IF = e^(2x)
- y·e^(2x) = C → **y = Ce^(-2x)**

---

### Q27. Nature of Roots
What is the nature of roots of m² + 4m + 4 = 0?

**Solution**:
- D = 16 - 16 = 0
- **Real and repeated roots** (m = -2, -2)

---

### Q28. Quick PI
Find PI of y'' - y = eˣ.

**Solution**:
- m² - 1 = 0 → m = ±1
- eˣ corresponds to root m = 1 (simple root)
- PI = **xeˣ/2**

---

### Q29. Laplace of Derivative
If L{f(t)} = F(s) and f(0) = 2, what is L{f'(t)}?

**Solution**: **sF(s) - 2**

---

### Q30. Application (RC Circuit)
RC circuit: R(dq/dt) + q/C = V₀, q(0) = 0.

**Solution**:
- dq/dt + q/(RC) = V₀/R
- IF = e^(t/RC)
- q·e^(t/RC) = V₀C(1 - e^(t/RC))/R · R... 
- q(t) = **CV₀(1 - e^(-t/RC))**
