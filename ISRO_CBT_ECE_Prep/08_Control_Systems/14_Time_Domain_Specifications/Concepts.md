# Time Domain Specifications - Concepts

## 1. Purpose
- Describe the transient and steady-state behavior of a system's step response.
- Key to specifying and verifying control-system performance.
- For a standard second-order underdamped system, the step response has well-defined metrics.

## 2. The Standard Second-Order System
G(s) = ω_n² / (s² + 2ζω_n·s + ω_n²)

- ω_n = undamped natural frequency.
- ζ = damping ratio.
- Poles: s = −ζω_n ± jω_n√(1−ζ²).

## 3. Step Response of Underdamped Second-Order System

### Standard step response (0<ζ<1)
y(t) = 1 − [e^{−ζω_n t}/√(1−ζ²)]·sin(ω_d·t + φ)

Where:
- ω_d = ω_n√(1−ζ²) (damped natural frequency).
- φ = cos⁻¹(ζ) = phase angle.

## 4. Time-Domain Specifications Definitions

### Delay Time (t_d)
- Time to reach 50% of final value.
- t_d ≈ (1 + 0.7ζ)/ω_n (approximation).

### Rise Time (t_r)
- Time to go from 10% to 90% of final value.
- For underdamped: t_r ≈ (π − β)/ω_d, where β = cos⁻¹(ζ) measured... often t_r = (π − φ)/ω_d with φ = cos⁻¹(ζ).

### Peak Time (t_p)
- Time to reach first (maximum) overshoot.
- t_p = π/ω_d.

### Percent Overshoot (%OS or M_p)
- Maximum amount the response overshoots the final value.
- %OS = 100·e^{−πζ/√(1−ζ²)}.

### Settling Time (t_s)
- Time for response to enter and stay within specified band (2% or 5%) of final value.
- 2% criterion: t_s ≈ 4/(ζω_n).
- 5% criterion: t_s ≈ 3/(ζω_n).

## 5. Relationships Among Specifications

### From damping ratio ζ
- %OS depends only on ζ.
- Rise/peak/settling times depend on ζ and ω_n.

### From %OS to ζ
ζ = −ln(%OS/100) / √(π² + ln²(%OS/100))

### From pole location to parameters
Given pole at −σ ± jω_d:
- σ = ζω_n.
- ω_d = ω_n√(1−ζ²).
- ζ = σ/√(σ²+ω_d²).
- ω_n = √(σ²+ω_d²).

## 6. Steady-State Error
- The difference between final value and desired input.
- Depends on system type and input signal.

## 7. Type Number & Static Error Constants
- **Type number** = number of poles at origin in open-loop TF G(s)H(s).
- Determines which inputs produce zero steady-state error.

### Static Error Constants
- **Position constant**: K_p = lim(s→0) G(s)H(s).
- **Velocity constant**: K_v = lim(s→0) s·G(s)H(s).
- **Acceleration constant**: K_a = lim(s→0) s²·G(s)H(s).

### Steady-State Errors (unity feedback)
- Step (position): e_ss = 1/(1+K_p). [type 0 finite, type ≥1 zero]
- Ramp (velocity): e_ss = 1/K_v. [type 0 infinite, type 1 finite, type≥2 zero]
- Parabolic (accel): e_ss = 1/K_a. [type 0,1 infinite, type 2 finite, type≥3 zero]

### Error summary table
| Input | Type 0 | Type 1 | Type 2 |
|---|---|---|---|
| Step | 1/(1+K_p) | 0 | 0 |
| Ramp | ∞ | 1/K_v | 0 |
| Parabolic | ∞ | ∞ | 1/K_a |

## 8. Time-Domain Specs in Terms of Second-Order Parameters

### Standard formulas (underdamped, unity gain)
- %OS = 100·e^{−πζ/√(1−ζ²)}
- t_p = π/(ω_n√(1−ζ²)) = π/ω_d
- t_s(2%) = 4/(ζω_n)
- t_s(5%) = 3/(ζω_n)
- t_r ≈ (π − cos⁻¹ζ)/(ω_n√(1−ζ²))

## 9. Dominant Poles Concept
- Higher-order systems often dominated by slowest (closest to origin) real or complex-conjugate poles.
- The response resembles a second-order system governed by these dominant poles.
- Used to approximate high-order systems.

## 10. Performance–Parameter Trade-offs
- Increasing ω_n: faster rise/peak/settling (all scale by 1/ω_n).
- Higher ζ: less overshoot, but slower rise time.
- Trade: faster response (high ω_n or low ζ) vs stability (low overshoot).

## 11. ISRO Commonly Tests
- Compute %OS, t_p, t_s, t_r from ω_n, ζ.
- Given %OS → find ζ.
- Determine steady-state error from error constants/type.
- Identify type number and K_p, K_v, K_a.

## 12. Relationship Among the Different Entities
- Time-domain specs ↔ pole positions ↔ damping/natural frequency ↔ Bode margins.
- Consistent throughout the entire control syllabus.
