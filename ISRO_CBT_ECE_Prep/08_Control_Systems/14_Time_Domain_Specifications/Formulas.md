# Time Domain Specifications - Formulas

## 1. Standard Second-Order System
G(s) = ω_n² / (s² + 2ζω_n s + ω_n²)

## 2. Poles
s = −ζω_n ± jω_n√(1−ζ²)

## 3. Frequency Parameters
- Damped natural freq: ω_d = ω_n·√(1−ζ²)
- Damping ratio: ζ = σ/√(σ²+ω_d²), where σ = |Re(pole)|
- Natural freq: ω_n = √(σ²+ω_d²)

## 4. Transient Specifications

### Percent Overshoot
%OS = 100·e^{−πζ/√(1−ζ²)}

### Inverse (ζ from %OS)
ζ = −ln(OS)/√(π² + ln²(OS)),  OS = %OS/100

### Peak Time
t_p = π/ω_d = π/(ω_n·√(1−ζ²))

### Settling Time
- 2%: t_s = 4/(ζω_n)
- 5%: t_s = 3/(ζω_n)

### Rise Time (10%→90%, underdamped)
t_r = (π − β)/ω_d,  where β = cos⁻¹(ζ)
= (π − cos⁻¹ζ)/(ω_n·√(1−ζ²))

### Delay Time
t_d ≈ (1 + 0.7ζ)/ω_n

## 5. Step Response Equation (0<ζ<1)
y(t) = 1 − [e^{−ζω_n t}/√(1−ζ²)]·sin(ω_d·t + cos⁻¹ζ)

## 6. Steady-State Error (unity feedback)

### Position (step), K_p = lim_{s→0} GH
e_ss = 1/(1 + K_p)

### Velocity (ramp), K_v = lim_{s→0} s·GH
e_ss = 1/K_v

### Acceleration (parabolic), K_a = lim_{s→0} s²·GH
e_ss = 1/K_a

## 7. Static Error Constants
K_p = lim_{s→0} G(s)H(s)
K_v = lim_{s→0} s·G(s)H(s)
K_a = lim_{s→0} s²·G(s)H(s)

## 8. Error Dependence on Type Number
| Input r(t) | Error formula | Type 0 | Type 1 | Type 2 |
|---|---|---|---|---|
| Step | 1/(1+K_p) | finite | 0 | 0 |
| Ramp | 1/K_v | ∞ | finite | 0 |
| Parabolic | 1/K_a | ∞ | ∞ | finite |
| In general t^n/n! | 1/K_n | — | type n ≥ order gives 0 | |

## 9. Type Number
Type number = number of open-loop poles at s=0 (integrators) in GH.

## 10. Final Value Theorem (steady-state)
e_ss = lim_{s→0} s·E(s)  [if sE(s) poles in LHP]

## 11. Dominant Poles & Higher Order
Approximate high-order by second order with:
- σ_dom = smallest real part magnitude.
- ω_dom = ω_d of dominant pair.

## Formula Cheatsheet (Time Domain)
| Spec | Formula |
|---|---|
| %OS | 100·e^{−πζ/√(1−ζ²)} |
| ζ from OS | −ln(OS)/√(π²+ln²OS) |
| t_p | π/ω_d |
| t_s (2%) | 4/(ζω_n) |
| t_s (5%) | 3/(ζω_n) |
| t_r | (π−cos⁻¹ζ)/ω_d |
| ω_d | ω_n√(1−ζ²) |
| e_ss step | 1/(1+K_p) |
| e_ss ramp | 1/K_v |
| e_ss parabola | 1/K_a |
| K_p | lim GH |
| K_v | lim s·GH |
| K_a | lim s²·GH |

## Useful Derivations
- 2% settling uses T=1/(ζω_n): time constant of envelope e^{−ζω_n t}; settling ≈ 4 time constants.
- %OS derived from peak value y(t_p).
- These formulas are valid only for underdamped (0<ζ<1) second-order.
