# Numerical Methods - Practice Questions

## Easy Level

### Q1. Bisection (First Iteration)
Find first approximation of root of x³-x-1 = 0 in [1,2].

**Solution**:
- c = (1+2)/2 = 1.5
- f(1) = -1, f(1.5) = 0.875
- f(1)f(1.5) < 0 → root in [1, 1.5]
- **c₁ = 1.5**

---

### Q2. Newton-Raphson (First Iteration)
Find first approximation of √2 using x_{n+1} = (x_n + 2/x_n)/2, x₀ = 1.

**Solution**:
- x₁ = (1 + 2/1)/2 = 1.5
- **x₁ = 1.5**

---

### Q3. Lagrange (2 Points)
Find linear interpolation of f(2.5) given f(2) = 5, f(3) = 8.

**Solution**:
- L₀ = (2.5-3)/(2-3) = 0.5, L₁ = (2.5-2)/(3-2) = 0.5
- f(2.5) ≈ 5(0.5) + 8(0.5) = 2.5 + 4 = **6.5**

---

### Q4. Trapezoidal Rule
Evaluate ∫[0,1] x² dx using trapezoidal rule with h = 0.5.

**Solution**:
- x₀=0, x₁=0.5, x₂=1
- f(0)=0, f(0.5)=0.25, f(1)=1
- ≈ 0.5/2 [0 + 2(0.25) + 1] = 0.25[1.5] = **0.375**

---

### Q5. Euler's Method (First Step)
Solve y' = y, y(0) = 1, h = 0.1. Find y(0.1).

**Solution**:
- y₁ = y₀ + h·f(x₀,y₀) = 1 + 0.1(1) = **1.1**

---

## Medium Level

### Q6. Newton-Raphson (Second Iteration)
Find √5, x₀ = 2.

**Solution**:
- x₁ = (2 + 5/2)/2 = 2.25
- x₂ = (2.25 + 5/2.25)/2 = (2.25 + 2.222)/2 = **2.236**

---

### Q7. Lagrange (3 Points)
Find f(1.5) given f(1)=1, f(2)=4, f(3)=9.

**Solution**:
- L₀ = (1.5-2)(1.5-3)/((1-2)(1-3)) = (-0.5)(-1.5)/((-1)(-2)) = 0.75/2 = 0.375
- L₁ = (1.5-1)(1.5-3)/((2-1)(2-3)) = (0.5)(-1.5)/((1)(-1)) = 0.75
- L₂ = (1.5-1)(1.5-2)/((3-1)(3-2)) = (0.5)(-0.5)/((2)(1)) = -0.125
- f(1.5) ≈ 1(0.375) + 4(0.75) + 9(-0.125) = 0.375 + 3 - 1.125 = **2.25**

---

### Q8. Simpson's 1/3 Rule
Evaluate ∫[0,2] x³ dx using Simpson's rule with h = 0.5.

**Solution**:
- x: 0, 0.5, 1, 1.5, 2
- f: 0, 0.125, 1, 3.375, 8
- ≈ 0.5/3 [0 + 4(0.125) + 2(1) + 4(3.375) + 8]
- = 0.5/3 [0 + 0.5 + 2 + 13.5 + 8] = 0.5/3(24) = **4**

---

### Q9. Central Difference
Find f'(1) using central difference with h = 0.1 for f(x) = x².

**Solution**:
- f(1.1) = 1.21, f(0.9) = 0.81
- f'(1) ≈ (1.21 - 0.81)/(0.2) = 0.4/0.2 = **2** (exact)

---

### Q10. RK4 (First Step)
Solve y' = x + y, y(0) = 1, h = 0.1.

**Solution**:
- k₁ = 0.1(0 + 1) = 0.1
- k₂ = 0.1(0.05 + 1.05) = 0.11
- k₃ = 0.1(0.05 + 1.055) = 0.1105
- k₄ = 0.1(0.1 + 1.1105) = 0.12105
- y₁ = 1 + (0.1 + 0.22 + 0.221 + 0.12105)/6 = 1 + 0.11034 = **1.11034**

---

### Q11. Fixed Point Iteration
Find root of x = cos(x) using x_{n+1} = cos(x_n), x₀ = 0.

**Solution**:
- x₁ = cos(0) = 1
- x₂ = cos(1) = 0.5403
- x₃ = cos(0.5403) = 0.8576
- x₄ = cos(0.8576) = 0.6543
- Converges to **0.7391**

---

### Q12. Secant Method
Find root of x²-4 = 0 with x₀ = 1, x₁ = 3.

**Solution**:
- f(1) = -3, f(3) = 5
- x₂ = 3 - 5(3-1)/(5-(-3)) = 3 - 10/8 = 1.75
- f(1.75) = -0.9375
- x₃ = 1.75 - (-0.9375)(1.75-3)/(-0.9375-5) = 1.75 + 1.078/5.9375 = **1.933**

---

### Q13. Newton's Forward Difference
Given f(0)=1, f(1)=4, f(2)=9, f(3)=16. Find f(0.5).

**Solution**:
- Δf: 3, 5, 7
- Δ²f: 2, 2
- Δ³f: 0
- s = 0.5
- f(0.5) = 1 + 0.5(3) + 0.5(-0.5)/2(2) + ... = 1 + 1.5 - 0.25 = **2.25**

---

### Q14. Simpson's 3/8 Rule
Evaluate ∫[0,3] x² dx with h = 1.

**Solution**:
- x: 0, 1, 2, 3
- f: 0, 1, 4, 9
- ≈ 3(1)/8 [0 + 3(1) + 3(4) + 9] = 3/8(24) = **9**

---

### Q15. Gauss-Seidel (First Iteration)
Solve: 4x + y = 9, x + 3y = 11. Start (0,0).

**Solution**:
- x₁ = (9 - 0)/4 = 2.25
- y₁ = (11 - 2.25)/3 = 2.9167
- **(x₁, y₁) = (2.25, 2.9167)**

---

## Hard Level

### Q16. Newton-Raphson for System
Solve x² + y² = 4, x + y = 1 using Newton's method, (x₀,y₀) = (1,0).

**Solution**:
- F = x² + y² - 4, G = x + y - 1
- J = |2x  2y|
      |1   1|
- At (1,0): J = |2  0|, F = -3, G = 0
               |1  1|
- Solve J·Δ = -F: Δ = (1.5, -1.5)
- (x₁,y₁) = (1+1.5, 0-1.5) = **(2.5, -1.5)**

---

### Q17. Simpson's with Error
Evaluate ∫[0,1] eˣ dx using Simpson's 1/3 with n=4. Compare with exact.

**Solution**:
- h = 0.25
- f: 1, 1.284, 1.649, 2.117, 2.718
- Simpson: 0.25/3[1 + 4(1.284) + 2(1.649) + 4(2.117) + 2.718]
- = 0.0833[1 + 5.136 + 3.298 + 8.468 + 2.718] = 0.0833(20.62) = **1.718**
- Exact: e - 1 = 1.7183
- Error ≈ 0.0003

---

### Q18. RK4 (Two Steps)
Solve y' = -2xy, y(0) = 1, h = 0.5. Find y(1).

**Solution**:
- Step 1 (x=0 to 0.5):
  k₁ = 0.5(0) = 0
  k₂ = 0.5(-2(0.25)(1)) = -0.25
  k₃ = 0.5(-2(0.25)(0.875)) = -0.21875
  k₄ = 0.5(-2(0.5)(0.78125)) = -0.390625
  y₁ = 1 + (0 - 0.5 - 0.4375 - 0.390625)/6 = 1 - 0.22135 = 0.77865

- Step 2 (x=0.5 to 1):
  k₁ = 0.5(-2(0.5)(0.77865)) = -0.3864
  k₂ = 0.5(-2(0.75)(0.5853)) = -0.4390
  k₃ = 0.5(-2(0.75)(0.5591)) = -0.4193
  k₄ = 0.5(-2(1)(0.3593)) = -0.3593
  y₂ = 0.77865 + (-0.3864 - 0.878 - 0.8386 - 0.3593)/6
  = 0.77865 - 0.4107 = **0.3679**
- Exact: e^(-1) ≈ 0.3679 ✓

---

### Q19. Interpolation Error
What is the error bound for Lagrange interpolation of sin(x) on [0,π] with 5 points?

**Solution**:
- f⁴(x) = sin(x), max|f⁴| = 1
- h = π/4
- Error ≤ M·h⁴/4! = 1·(π/4)⁴/24 = π⁴/6144 ≈ **0.0158**

---

### Q20. Trapezoidal vs Simpson
Compare errors for ∫[0,1] x⁴ dx with n=10.

**Solution**:
- Exact: 1/5 = 0.2
- Trapezoidal error: O(h²), h = 0.1
- Simpson error: O(h⁴), much smaller
- Simpson is significantly more accurate

---

### Q21. Convergence Rate
Which converges faster: Newton (p=2) or Secant (p=1.618)?

**Solution**:
- Newton: x_{n+1} ≈ C·e_n²
- Secant: x_{n+1} ≈ C·e_n^1.618
- **Newton converges faster** (quadratic vs superlinear)

---

### Q22. Implicit Method
For heat equation with r = 1, which method is stable: explicit or implicit?

**Solution**:
- Explicit: stable if r ≤ 0.5 → r=1 is **unstable**
- Implicit: **unconditionally stable** for any r
- **Use implicit method**

---

### Q23. Divided Difference Table
Construct divided difference table for: f(0)=1, f(1)=3, f(3)=7.

**Solution**:
- f[0,1] = (3-1)/(1-0) = 2
- f[1,3] = (7-3)/(3-1) = 2
- f[0,1,3] = (2-2)/(3-0) = 0
- **Constant divided difference** → linear function

---

### Q24. Gaussian Quadrature
Evaluate ∫[-1,1] x² dx using 2-point Gaussian quadrature.

**Solution**:
- x₁ = -1/√3, x₂ = 1/√3, w₁ = w₂ = 1
- ∫ ≈ 1·(1/3) + 1·(1/3) = 2/3 ≈ **0.6667**
- Exact: 2/3 ✓

---

### Q25. Condition Number
A = |4  1|, find κ(A) using ∞-norm.
    |2  3|

**Solution**:
- ||A||∞ = max(5, 5) = 5
- A⁻¹ = (1/10)|3 -1|, ||A⁻¹||∞ = max(0.4, 0.5) = 0.5
           |-2  4|
- κ(A) = 5 × 0.5 = **2.5**

---

## ISRO-Focused Questions

### Q26. Quick Bisection
f(1) = -2, f(2) = 3. After 3 bisections, what is the interval?

**Solution**:
- [1,2] → [1,1.5] → [1.5,1.75] → [1.75,1.875]
- Interval = **[1.75, 1.875]**, length = 0.125

---

### Q27. Quick Newton-Raphson
f(x) = x²-9, f'(x) = 2x, x₀ = 5. Find x₁.

**Solution**:
- x₁ = 5 - (25-9)/10 = 5 - 1.6 = **3.4**

---

### Q28. Simpson's Quick
For Simpson's 1/3 rule, minimum number of points needed?

**Solution**:
- Requires even number of intervals
- **Minimum 3 points** (2 intervals)

---

### Q29. Euler vs RK4
Which is more accurate for same step size: Euler or RK4?

**Solution**:
- Euler: O(h), RK4: O(h⁴)
- **RK4 is much more accurate**

---

### Q30. Stability
For explicit heat equation scheme, what happens if r = 0.6?

**Solution**:
- Stability requires r ≤ 0.5
- r = 0.6 > 0.5
- **Solution is unstable**, will oscillate and diverge
