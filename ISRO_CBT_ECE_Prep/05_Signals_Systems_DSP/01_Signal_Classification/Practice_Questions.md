# Signal Classification - Practice Questions (ISRO CBT Style)

## Question 1
A signal x(t) = e^(-2|t|) is:
- (A) Periodic and energy signal
- (B) Aperiodic and energy signal
- (C) Periodic and power signal
- (D) Aperiodic and power signal

**Answer: (B)**
**Explanation:** Exponential decay e^(-2|t|) is aperiodic. Energy E = ∫e^(-4|t|)dt = 1/2 < ∞ → Energy signal.

---

## Question 2
For x[n] = cos(3πn/7), the fundamental period N is:
- (A) 7
- (B) 14
- (C) 21
- (D) 14/3

**Answer: (B)**
**Explanation:** Ω₀ = 3π/7. Ω₀/2π = 3/14. Since 3/14 is already rational, N = 14.

---

## Question 3
The energy of signal x(t) = rect(t/2) is:
- (A) 1
- (B) 2
- (C) 4
- (D) 1/2

**Answer: (B)**
**Explanation:** rect(t/2) = 1 for -1 < t < 1. E = ∫₋₁¹ 1² dt = 2.

---

## Question 4
A CT sinusoidal signal x(t) = cos(ω₀t) is always periodic with period:
- (A) 2π/ω₀
- (B) ω₀/2π
- (C) π/ω₀
- (D) 2ω₀

**Answer: (A)**
**Explanation:** CT sinusoids are always periodic with T = 2π/ω₀.

---

## Question 5
The even part of x(t) = e^(jθ) is:
- (A) cos θ
- (B) j sin θ
- (C) e^(jθ)
- (D) 1

**Answer: (A)**
**Explanation:** x_e = [x(t) + x(-t)]/2 = [e^(jθ) + e^(-jθ)]/2 = cos θ.

---

## Question 6
The power of x(t) = A cos(ω₀t + φ) is:
- (A) A²
- (B) A²/2
- (C) A²/4
- (D) 2A²

**Answer: (B)**
**Explanation:** P = (1/T)∫A²cos²(ωt+φ)dt = A²/2.

---

## Question 7
If x[n] is periodic with period N, then x[n] + x[n+N/2] (N even) is:
- (A) Periodic with period N
- (B) Periodic with period N/2
- (C) Aperiodic
- (D) Depends on x[n]

**Answer: (B)**
**Explanation:** If N is even, x[n+N/2] has period N/2, so the sum repeats every N/2.

---

## Question 8
The unit step u(t) can be expressed as:
- (A) ∫₋∞^t δ(τ)dτ
- (B) dδ(t)/dt
- (C) δ(t) + u(t-1)
- (D) δ(t) × u(t)

**Answer: (A)**
**Explanation:** u(t) = ∫₋∞^t δ(τ)dτ is the integral of the impulse function.

---

## Question 9
Signal x(t) = e^(-t²) is:
- (A) Power signal only
- (B) Energy signal only
- (C) Both energy and power signal
- (D) Neither

**Answer: (B)**
**Explanation:** Gaussian e^(-t²) has finite energy E = √(π/2) < ∞ and zero average power.

---

## Question 10
Which operation converts CT signal to DT signal?
- (A) Sampling
- (B) Quantization
- (C) Modulation
- (D) Integration

**Answer: (A)**
**Explanation:** Sampling converts CT to DT: x[n] = x(nT_s).

---

## Question 11
The fundamental period of x[n] = sin(πn/3) is:
- (A) 3
- (B) 6
- (C) 9
- (D) 12

**Answer: (B)**
**Explanation:** Ω = π/3, Ω/2π = 1/6 → N = 6.

---

## Question 12
For x(t) = u(t) - u(t-2), the energy is:
- (A) 1
- (B) 2
- (C) 4
- (D) ∞

**Answer: (B)**
**Explanation:** Rectangular pulse of width 2. E = ∫₀² 1² dt = 2.

---

## Question 13
The signal x(t) = e^(at) is periodic if a is:
- (A) Real
- (B) Pure imaginary
- (C) Complex with positive real part
- (D) Zero

**Answer: (B)**
**Explanation:** e^(jωt) is periodic. e^(σt) is not periodic for σ ≠ 0.

---

## Question 14
A signal having finite energy and zero power is called:
- (A) Periodic signal
- (B) Energy signal
- (C) Power signal
- (D) Random signal

**Answer: (B)**
**Explanation:** Energy signals: 0 < E < ∞, P = 0.

---

## Question 15
The time reversal of x(t) = u(1-t) gives:
- (A) u(t-1)
- (B) u(t+1)
- (C) u(1+t)
- (D) u(-t-1)

**Answer: (C)**
**Explanation:** x(-t) = u(1-(-t)) = u(1+t).

---

## Question 16
x[n] = e^(jπn/2) has period:
- (A) 2
- (B) 4
- (C) 8
- (D) π

**Answer: (B)**
**Explanation:** Ω = π/2, Ω/2π = 1/4 → N = 4.

---

## Question 17
The odd part of x[n] = u[n] is:
- (A) 0.5
- (B) 0.5sgn[n]
- (C) δ[n]/2
- (D) u[n] - 0.5

**Answer: (B)**
**Explanation:** x_o[n] = [u[n] - u[-n]]/2 = sgn[n]/2 (for n ≠ 0, x_o[0] = 0).

---

## Question 18
Which is NOT a property of impulse function δ(t)?
- (A) δ(t) = δ(-t)
- (B) ∫δ(t)dt = 1
- (C) x(t)δ(t) = x(0)δ(t)
- (D) δ(t) has finite energy

**Answer: (D)**
**Explanation:** δ(t) is not a true function; its energy is undefined/infinite.

---

## Question 19
Signal x(t) = cos(2πt) + sin(πt) is:
- (A) Periodic with T = 2
- (B) Periodic with T = 4
- (C) Aperiodic
- (D) Periodic with T = 1

**Answer: (C)**
**Explanation:** T₁ = 1, T₂ = 2. Ratio T₁/T₂ = 1/2 is rational. LCM = 2. Actually T = 2. Wait—let me recheck: cos(2πt) has T=1, sin(πt) has T=2. LCM(1,2) = 2. So it IS periodic with T = 2.

**Corrected Answer: (A)**
**Explanation:** cos(2πt): T₁ = 1, sin(πt): T₂ = 2. T₁/T₂ = 1/2 (rational). LCM(1,2) = 2.

---

## Question 20
The signal δ(t-3) × δ(t+2) equals:
- (A) δ(t-3)
- (B) δ(t+2)
- (C) 0
- (D) δ(t-1)

**Answer: (C)**
**Explanation:** δ(t-a)δ(t-b) = 0 if a ≠ b, since they are never simultaneously non-zero.
