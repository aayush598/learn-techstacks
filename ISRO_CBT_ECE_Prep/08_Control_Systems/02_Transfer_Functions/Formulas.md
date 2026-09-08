# Transfer Functions - Formulas

## 1. General Form
G(s) = (b_m s^m + b_{m-1} s^{m-1} + ... + b_0) / (a_n s^n + a_{n-1} s^{n-1} + ... + a_0)

- Standardize: m ≤ n for proper.
- Coefficient a_n (leading coefficient of denominator) often normalized to 1.

## 2. Pole-Zero Form
G(s) = K · Π(s - z_i) / Π(s - p_j)
- z_i = zeros, p_j = poles.
- K = gain constant.
- K = b_m / a_n (for monic factor polynomials): DC gain = K·(Π(-z_i))/Π(-p_j).

## 3. Time-Constant Form
G(s) = K' · Π(τ_i s + 1) / Π(T_j s + 1)
- τ_i = zero time constants, T_j = pole time constants.
- Useful for Bode plot construction: corner frequencies = 1/τ_i, 1/T_j.
- DC gain = K'.

## 4. Characteristic Equation
- Open loop: D(s) = 0.
- Closed loop (unity feedback): 1 + G(s) = 0 → s^n + a_{n-1}s^{n-1} + ... + a_0 = 0.
- General closed loop: 1 + G(s)H(s) = 0.

## 5. First-Order System
- Transfer function: G(s) = K/(τs + 1) or G(s) = a/(s + a).
- Time constant: τ = 1/a.
- Pole: s = -a = -1/τ.
- Step response: y(t) = K(1 - e^{-t/τ}).
- Time to reach 63.2% of final: τ.

## 6. Second-Order System (Standard Form)
G(s) = ω_n² / (s² + 2ζω_n s + ω_n²)

- ω_n = undamped natural frequency (rad/s).
- ζ = damping ratio.
- Poles: s = -ζω_n ± jω_n·√(1-ζ²).

#### Critical damping: ζ = 1, poles equal real.
#### Overdamped: ζ > 1, poles real distinct.
#### Underdamped: 0 < ζ < 1, complex conjugate.

- Damped natural frequency: ω_d = ω_n·√(1-ζ²).
- Peak time: t_p = π/ω_d.
- Settling time: t_s ≈ 4/(ζω_n) (2% criterion), 3/(ζω_n) (5%).
- Rise time (10-90%): t_r ≈ 1.8/ω_n (approx for ζ≈0.5).
- Percent overshoot: %OS = 100·e^{-ζπ/√(1-ζ²)}.

## 7. Relationship Formulas

### From ζ to overshoot
ζ = -ln(OS) / √(π² + ln²(OS)), OS = overshoot fraction.

### From poles to parameters
- σ = ζω_n (real part magnitude).
- ω_d = ω_n√(1-ζ²) (imaginary part).
- ζ = σ/ω_n = σ/√(σ² + ω_d²).

## 8. DC Gain and Static Constants

### DC gain
G(0) = b_0/a_0 (constant term ratio).

### Static Error Constants (for unity feedback with input u(t))
- Position constant: K_p = lim(s→0) G(s)  [type 0: K_p = const; type ≥1: infinite]
- Velocity constant: K_v = lim(s→0) s·G(s)  [type 1: finite]
- Acceleration constant: K_a = lim(s→0) s²·G(s)  [type 2: finite]

### Steady-State Errors
- e_ss (step) = 1/(1+K_p)
- e_ss (ramp) = 1/K_v
- e_ss (parabolic) = 1/K_a

## 9. Type Number
- **Type number** = number of poles at s=0 in open-loop transfer function G(s)H(s).
- Type 0: no integrator → finite error to step.
- Type 1: one integrator → zero error to step, finite to ramp.
- Type 2: two integrators → zero error to step & ramp.
- Type n: drives n-th order polynomial inputs to zero error.

## 10. Properness / Improperness Formulas
- Proper: m ≤ n.
- Strictly proper: m < n → |G(jω)|→0 as ω→∞.
- Biproper: m = n → |G(jω)|→ K (constant) as ω→∞.
- Improper: m > n → |G(jω)|→ ∞ as ω→∞ (not realizable with passive elements).

## 11. Frequency Response Formulas
- Magnitude: |G(jω)| = K·Π|jω-z_i| / Π|jω-p_j|.
- Phase: ∠G(jω) = Σ∠(jω-z_i) - Σ∠(jω-p_j).
- Return |G(jω)| in dB: 20·log₁₀|G(jω)|.

### Corner Frequencies
- Real pole (T): corner at ω = 1/T, slope changes -20 dB/dec.
- Real zero (τ): corner at ω = 1/τ, slope +20 dB/dec.
- Complex pole at ω_n: -40 dB/dec with resonance peak.

## 12. From State Space to TF
G(s) = C(sI - A)⁻¹B + D

## 13. Pole-Zero Cancellation
- Cancellation occurs if a zero of G and pole share the same value (s = p = z).
- In cascade G₁G₂, a pole of G₃ cancelled by zero of G₂.
- After cancellation, reduced-order TF.
- In state-space, cancelled mode becomes either uncontrollable or unobservable.

## Cheat Sheet Table

| Feature | Value | Location/Meaning |
|---|---|---|
| Order | # of poles, degree of D(s) | n |
| System type | # of poles at origin | affects error constants |
| DC gain | G(0) | limit at s→0 |
| Damping ratio ζ | -ln(OS)/√(π²+ln²OS) | 0 to 1 underdamped |
| Natural freq ω_n | √(constant term of D(s)) | |
| ζω_n | real part of pole | decay rate |
| ω_d | imaginary of pole | oscillation freq |

## Numerical Example Cheats
- For G(s)=K/(s+a): pole = -a, DC gain = K/a, time constant = 1/a.
- For second order D(s)=s²+2s+5: ω_n=√5≈2.236, ζ=2/(2√5)=0.447.
- Closed loop poles from 1+G(s)=0.
