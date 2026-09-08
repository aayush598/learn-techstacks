# ISRO CBT ECE - Engineering Mathematics Memory Tricks

## 1. Linear Algebra Memory Aids

### Singular Matrix Mnemonic
```
"Singular = Sad" (no inverse)
Check: det = 0 → sad, no inverse exists

Quick test: If rows add to zero vector → singular
If two rows identical → singular
```

### Eigenvalue Memory
```
"Sum = trace, Product = determinant"
λ₁ + λ₂ + λ₃ = trace(A) = a₁₁ + a₂₂ + a₃₃
λ₁ × λ₂ × λ₃ = det(A)

Eigenvalue of A⁻¹: "Inverse eigenvalue = 1/λ"
Eigenvalue of A^k: "Power eigenvalue = λ^k"
```

### Diagonalization Checklist
```
1. Find eigenvalues (characteristic equation)
2. Find eigenvectors (solve (A-λI)v = 0)
3. Check: n independent eigenvectors?
4. If yes: A = PDP⁻¹
5. If no: cannot diagonalize (defective)
```

### Cramer's Rule Quick
```
"x equals det-with-replaced-column over det"
x_i = det(A with column i replaced by b) / det(A)
Only works when det(A) ≠ 0
```

---

## 2. Calculus Memory Aids

### Derivative Ladder
```
"Bottom to Top":
x^n → nx^(n-1)
e^x → e^x (never changes!)
ln(x) → 1/x
sin → cos (positive)
cos → -sin (negative)
tan → sec² (positive)
```

### Integration Reverse Ladder
```
"Top to Bottom" (reverse of derivatives):
nx^(n-1) → x^n
e^x → e^x
1/x → ln|x|
cos → sin
-sin → cos
sec² → tan
```

### LIATE Rule for Integration by Parts
```
L - Logarithmic (ln x)
I - Inverse trig (arctan x)
A - Algebraic (x, x²)
T - Trigonometric (sin x)
E - Exponential (eˣ)

Choose u in this priority order
```

### L'Hopital's Rule Quick
```
"0/0 or ∞/∞ → differentiate top and bottom"
Keep going until you get a number
If stuck: try logarithmic form for 0⁰, 1^∞, ∞⁰
```

### Taylor Series Patterns
```
eˣ: All positive, factorial denominators
sin: Odd powers, alternating signs
cos: Even powers, alternating signs
1/(1-x): Geometric series, all positive
ln(1+x): Alternating, harmonic denominators
```

---

## 3. Differential Equations Memory Aids

### Second Order CF Quick Guide
```
"Aunt May Help" (AMH):

Distinct roots (m₁, m₂):
"Distinct → c₁e^(m₁x) + c₂e^(m₂x)"

Repeated root (m):
"Repeated → (c₁ + c₂x)e^(mx)"

Complex roots (α ± iβ):
"Complex → e^(αx)(c₁cos(βx) + c₂sin(βx))"
```

### PI Selection Rule
```
"Try same form as right side"

e^(ax) → Try Ae^(ax)
sin/cos → Try A sin + B cos
polynomial → Try same degree polynomial

"Hit by x" if part of CF:
Simple root → multiply by x
Double root → multiply by x²
```

### Laplace Transform Table
```
"1, t, e, sin, cos" (1-2-3-4-5)

1 → 1/s
t → 1/s²
e^(at) → 1/(s-a)
sin(bt) → b/(s²+b²)
cos(bt) → s/(s²+b²)
```

### Inverse Laplace Quick
```
"Flip the table"

1/s → 1
1/s² → t
1/(s-a) → e^(at)
b/(s²+b²) → sin(bt)
s/(s²+b²) → cos(bt)

Shift theorem: F(s-a) → e^(at)f(t)
```

---

## 4. PDE Memory Aids

### Classification Mnemonic
```
"Wave = Hyperbolic, Heat = Parabolic, Laplace = Elliptic"

Or: "WHL" → "Wave-Hyperbolic, Heat-Parabolic, Laplace-Elliptic"

Quick: B² - 4AC
Positive → Hyperbolic (Wave)
Zero → Parabolic (Heat)
Negative → Elliptic (Laplace)
```

### Separation of Variables Steps
```
"SPICE":
S - Separate variables: u = X(x)T(t)
P - Plug into PDE
I - Identify separation constant (-λ)
C - Create ODEs with boundary conditions
E - Expand using Fourier series
```

### Boundary Condition Types
```
"DNA":
D - Dirichlet: u = prescribed value
N - Neumann: ∂u/∂n = prescribed value
A - Robin: ∂u/∂n + hu = prescribed

Dirichlet = "Fixed value"
Neumann = "Fixed flux/derivative"
```

### Heat vs Wave Solution
```
Heat: "Decays with time"
u(x,t) = Σ Bₙ sin(nπx/L) e^(-k(nπ/L)²t)

Wave: "Oscillates with time"
u(x,t) = Σ sin(nπx/L)[Aₙ cos(nπct/L) + Bₙ sin(nπct/L)]

Heat has exponential decay, Wave has sine/cosine in time
```

---

## 5. Probability Memory Aids

### Bayes' Theorem Quick
```
"Posterior = Likelihood × Prior / Evidence"

P(A|B) = P(B|A) × P(A) / P(B)

"Backward = Forward × Prior / Total"
```

### Total Probability
```
"Mix of all paths"

P(B) = P(B|A₁)P(A₁) + P(B|A₂)P(A₂) + ...

"Like weighted average of conditional probabilities"
```

### Distribution Identification
```
"Count events → Poisson"
"Binary yes/no → Binomial"
"Continuous uniform → Uniform"
"Symmetric bell → Normal"
"Time until event → Exponential"
```

### Normal Distribution 68-95-97
```
"One sigma: 68%"
"Two sigma: 95%"
"Three sigma: 99.7%"

Or: "68-95-99.7 rule"
```

### Independence Check
```
"Independent: P(A∩B) = P(A)×P(B)"
"Dependent: P(A∩B) ≠ P(A)×P(B)"

Quick: If events affect each other → dependent
If truly separate → independent
```

---

## 6. Statistics Memory Aids

### Central Limit Theorem
```
"Sample mean is normal for large n"

x̄ ~ N(μ, σ²/n) for n ≥ 30

"Big sample, normal mean"
```

### Variance Formula
```
"Var = E[X²] - (E[X])²"
"Variance = second moment minus square of first moment"

Quick: Calculate E[X] and E[X²], then subtract
```

### Confidence Interval
```
"95%: 1.96 standard errors"
"99%: 2.576 standard errors"

CI = estimate ± z × standard error
```

### Hypothesis Testing Quick
```
"p-value < α → Reject H₀"
"p-value ≥ α → Fail to reject H₀"

"Small p = Strong evidence against null"
```

---

## 7. Complex Analysis Memory Aids

### Residue Quick
```
"Simple pole: (z-z₀) times function, then limit"
Res(f, z₀) = lim(z→z₀) (z-z₀)f(z)

"Quotient rule: p(z₀)/q'(z₀)"
If f = p/q and q has simple zero at z₀
```

### Cauchy-Riemann Quick
```
"u_x = v_y, u_y = -v_x"
"Partial x of real = Partial y of imaginary"
"Partial y of real = negative Partial x of imaginary"

f'(z) = u_x + iv_x
```

### Laurent Series Classification
```
"Removable: Clean, no negatives"
"Pole: Finite negatives, highest is (z-z₀)^(-m)"
"Essential: Infinitely many negatives"

Quick: Count negative powers in series
```

### Conformal Mapping Quick
```
"Möbius: (az+b)/(cz+d)"
"Maps circles to circles"
"Three points determine mapping"
```

---

## 8. Numerical Methods Memory Aids

### Newton-Raphson
```
"New x = Old x - f/f'"

x_{n+1} = x_n - f(x_n)/f'(x_n)

"Function over derivative, subtract from x"
```

### Simpson's Rule
```
"First, 4-odds, 2-evens, last, over 3"

∫ ≈ h/3 [f₀ + 4(f₁+f₃+...) + 2(f₂+f₄+...) + fₙ]

"Odd positions get 4, even get 2"
```

### RK4 Coefficients
```
"k₁k₂k₃k₄ pattern"

k₁ = hf(x, y)
k₂ = hf(x+h/2, y+k₁/2)
k₃ = hf(x+h/2, y+k₂/2)
k₄ = hf(x+h, y+k₃)

y_{new} = y + (k₁ + 2k₂ + 2k₃ + k₄)/6

"1-2-2-1 weights, divide by 6"
```

### Euler vs RK4
```
"Euler: Simple but crude (O(h))"
"RK4: Complex but accurate (O(h⁴))"

"Easy method, easy errors"
"Hard method, hard accuracy"
```

### Stability
```
"Heat explicit: r ≤ 0.5"
"Heat implicit: Any r"
"Wave: cr ≤ 1"

"Explicit = Conditional"
"Implicit = Unconditional"
```

---

## 9. ISRO-Specific Focus Areas

### High-Yield Topics
```
1. Singular matrix identification (quick check)
2. Eigenvalue problems (trace, determinant)
3. Poisson/uniform distributions
4. PDE boundary conditions
5. Bayes' theorem
6. Normal distribution (68-95-97)
7. Residue calculation
8. Simpson's rule
```

### Common Mistakes to Avoid
```
1. Forgetting det(kA) = k^n det(A)
2. Mixing up eigenvalue of A vs A⁻¹
3. Forgetting continuity correction in normal approximation
4. Using wrong integration by parts priority (LIATE)
5. Forgetting stable regions for PDE schemes
6. Mixing up heat vs wave equation solutions
```

### Quick Decision Tree
```
Matrix problem:
→ Check det = 0? → Singular
→ Find eigenvalues? → Characteristic equation
→ Diagonalizable? → n independent eigenvectors?

PDE problem:
→ Classify first (Δ = B² - 4AC)
→ Choose method based on type
→ Apply boundary conditions

Probability problem:
→ Identify distribution type
→ Apply appropriate formula
→ Check independence assumption
```

---

## 10. Last-Minute Review Checklist

### Must-Know Formulas
```
□ det(AB) = det(A)det(B)
□ (AB)⁻¹ = B⁻¹A⁻¹
□ Eigenvalue sum = trace
□ Pythagorean identity: sin²+cos²=1
□ d/dx eˣ = eˣ, ∫ eˣ dx = eˣ
□ L'Hopital: 0/0 or ∞/∞
□ Bayes: P(A|B) = P(B|A)P(A)/P(B)
□ Normal: 68-95-97 rule
□ Residue: 2πi × sum of residues
□ Simpson: h/3 × [first + 4odds + 2evens + last]
```

### Quick Checks
```
□ Singular matrix: det = 0
□ Analytic function: CR equations hold
□ Stable scheme: Check stability condition
□ Confidence interval: estimate ± z × SE
□ p-value < α: Reject null hypothesis
```
