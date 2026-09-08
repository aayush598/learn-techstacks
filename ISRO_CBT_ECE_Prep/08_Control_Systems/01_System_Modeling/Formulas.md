# System Modeling - Formulas

## 1. Laplace Transform Pairs

| Time Domain f(t) | Laplace Domain F(s) | Region of Convergence |
|---|---|---|
| δ(t) | 1 | All s |
| u(t) | 1/s | Re(s) > 0 |
| t·u(t) | 1/s² | Re(s) > 0 |
| t^n·u(t) | n!/s^(n+1) | Re(s) > 0 |
| e^{-at}·u(t) | 1/(s+a) | Re(s) > -a |
| t·e^{-at}·u(t) | 1/(s+a)² | Re(s) > -a |
| sin(ωt)·u(t) | ω/(s²+ω²) | Re(s) > 0 |
| cos(ωt)·u(t) | s/(s²+ω²) | Re(s) > 0 |
| e^{-at}sin(ωt)·u(t) | ω/((s+a)²+ω²) | Re(s) > -a |
| e^{-at}cos(ωt)·u(t) | (s+a)/((s+a)²+ω²) | Re(s) > -a |

## 2. Key Laplace Properties

### Linearity
L{a·f₁(t) + b·f₂(t)} = a·F₁(s) + b·F₂(s)

### Differentiation
L{df/dt} = s·F(s) - f(0⁻)
L{d²f/dt²} = s²·F(s) - s·f(0⁻) - f'(0⁻)
L{dⁿf/dtⁿ} = sⁿ·F(s) - Σ s^(n-1-k) · f^(k)(0⁻)

### Integration
L{∫₀ᵗ f(τ)dτ} = F(s)/s

### Time Shifting
L{f(t-a)·u(t-a)} = e^{-as}·F(s)

### Frequency Shifting (s-domain shifting)
L{e^{-at}·f(t)} = F(s+a)

### Initial Value Theorem
f(0⁺) = lim(s→∞) s·F(s)  [if limit exists]

### Final Value Theorem
f(∞) = lim(s→0) s·F(s)  [valid only if all poles of sF(s) in LHP]

### Convolution
L{f₁(t) * f₂(t)} = F₁(s) · F₂(s)

## 3. Transfer Function Formulas

### Standard Form
G(s) = C(s)/R(s) = (b_m·s^m + b_{m-1}·s^{m-1} + ... + b_0) / (a_n·s^n + a_{n-1}·s^{n-1} + ... + a_0)

### Factored (Pole-Zero) Form
G(s) = K · [(s-z₁)(s-z₂)...(s-z_m)] / [(s-p₁)(s-p₂)...(s-p_n)]

### Time Constant Form
G(s) = K · [(τ₁s+1)(τ₂s+1)...] / [(T₁s+1)(T₂s+1)...]

## 4. RLC Circuit Transfer Functions

### Series RLC (output across C)
G(s) = (1/LC) / (s² + (R/L)s + 1/LC)

### Series RLC (output across R)
G(s) = (R/L)s / (s² + (R/L)s + 1/LC)

### Series RLC (output across L)
G(s) = s² / (s² + (R/L)s + 1/LC)

### Parallel RLC
G(s) = (1/LC) / (s² + (1/RC)s + 1/LC)

## 5. Mechanical System Transfer Functions

### Spring-Damper-Mass (output = displacement, input = force)
G(s) = X(s)/F(s) = 1 / (ms² + bs + k)

### Spring-Damper (no mass)
G(s) = X(s)/F(s) = 1 / (bs + k)

### Damper-Mass (no spring)
G(s) = X(s)/F(s) = 1 / (ms² + bs)

## 6. Transfer Function from State-Space

Given: ẋ = Ax + Bu, y = Cx + Du
G(s) = C(sI - A)⁻¹B + D

Where (sI - A)⁻¹ is the resolvent matrix.

## 7. Canonical Forms

### Controllable Canonical Form
A = [[0,1,0,...,0],[0,0,1,...,0],...,[−a₀,−a₁,...,−a_{n-1}]]
B = [[0],[0],...,[1]]
C = [b₀−a₀b_n, b₁−a₁b_n,..., b_{n-1}−a_{n-1}b_n]

### Observable Canonical Form
A = [[0,0,...,−a₀],[1,0,...,−a₁],...,[0,1,...,−a_{n-1}]]
B = [b₀−a₀b_n, b₁−a₁b_n,..., b_{n-1}−a_{n-1}b_n]ᵀ
C = [0,0,...,1]

## 8. Block Diagram Algebra

### Series (Cascade): G₁(s) → G₂(s)
G_total = G₁ · G₂

### Parallel
G_total = G₁ ± G₂

### Feedback Loop
T(s) = G(s) / [1 ± G(s)H(s)]
- Negative feedback: T = G/(1+GH)
- Positive feedback: T = G/(1−GH)

### Open-Loop Transfer Function
OLTF = G(s)·H(s)

### Closed-Loop Transfer Function
CLTF = G(s) / [1 + G(s)H(s)]

## 9. Characteristic Equation
1 + G(s)H(s) = 0
- Roots of characteristic equation = poles of closed-loop system.
- Determines stability and transient response.

## 10. Mason's Gain Formula (Preview)
T = (1/Δ) · Σ P_k · Δ_k
- P_k = k-th forward path gain
- Δ = 1 - Σ(loop gains) + Σ(products of non-touching loop gains) - ...
- Δ_k = Δ with loops touching k-th path removed

## Key Formulas for Quick Reference

| System | Transfer Function |
|---|---|
| First order: τ(dY/dt) + Y = K·X | G(s) = K/(τs+1) |
| Second order standard | ω_n²/(s²+2ζω_n·s+ω_n²) |
| Integrator | 1/s |
| Differentiator | s |
| Delay e^{-T_d s} | e^{-T_d s} |

## Units Check
- Electrical: [V/V], [A/A] (dimensionless for voltage transfer functions)
- Mechanical: [m/N], [rad/N·m]
- Always verify dimensional consistency of derived transfer functions.
