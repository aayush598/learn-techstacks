# Transfer Functions - Concepts

## 1. Definition and Standard Form
- The **transfer function** G(s) is the ratio of the Laplace transform of the output to the Laplace transform of the input, with all initial conditions set to zero.
- G(s) = C(s)/R(s) = N(s)/D(s), where N(s) = numerator, D(s) = denominator.
- It completely characterizes a linear, time-invariant (LTI) system.

## 2. Poles
- **Poles** are the roots of the denominator polynomial D(s) = 0.
- Also roots of the **characteristic equation** (approaches system dynamics).
- Poles determine:
  - Stability (real part < 0 for stability).
  - Nature of transient response (real poles → exponential, complex poles → oscillatory).
  - Natural frequency and damping of the response.
- Number of poles = order of the system.

### Physical Meaning of Pole Locations
| Pole Location | Response Type |
|---|---|
| Negative real | Exponentially decaying (stable) |
| Positive real | Exponentially growing (unstable) |
| Imaginary (on jω axis) | Sustained oscillation (marginally stable) |
| Complex with negative real part | Damped oscillation (stable) |
| Complex with positive real part | Growing oscillation (unstable) |
| At origin | Integrator behavior |

## 3. Zeros
- **Zeros** are the roots of the numerator polynomial N(s) = 0.
- Zeros determine the shape of the transient response and affect steady-state gain.
- Zeros near the jω axis create resonances or anti-resonances in frequency response.
- Zeros do NOT determine stability (only poles do), but they affect transient features.

### Effect of Zeros
- A zero in the right half plane (RHP zero, non-minimum phase) adds initial undershoot/overshoot in the response.
- Zeros increase the transient "liveliness" of the system.

## 4. Characteristic Equation
- The characteristic equation is D(s) = 0 (for closed-loop: 1 + G(s)H(s) = 0).
- Roots of the characteristic equation are the system poles.
- **Stability criterion**: ALL roots (poles) must lie in the left half of the s-plane.
- The characteristic equation determines the homogeneous solution (free response) of the system.

## 5. Order of a System
- **Order** = degree of denominator polynomial = number of poles = number of state variables.
- First-order: D(s) = s + a → one pole.
- Second-order: D(s) = s² + 2ζω_n + ω_n² → two poles.
- The order dictates the maximum number of independent initial conditions, energy storage elements, or state variables.

## 6. Proper / Improper Transfer Functions

### Proper
- degree(N) ≤ degree(D) → m ≤ n (proper), m < n (strictly proper).
- Physically realizable systems are proper.
- Frequency response is finite at high frequencies.

### Improper
- degree(N) > degree(D) → m > n.
- Physically realizable independent of differentiator circuits.
- Frequency response grows indefinitely at high frequencies (physically impossible for passive systems).
- e.g., G(s) = s² (pure differentiator) is improper unless approximated.

### Biproper
- m = n (same degree).
- Gain at high frequency = ratio of leading coefficients.

## 7. Pole-Zero Cancellation
- When a pole and zero coincide at the same location in the s-plane, they cancel.
- **Formal cancellation**: The transfer function can be algebraically reduced.
- **Closed loop vs open loop**: Cancellation in closed loop may mask unstable modes (internal dynamics).
- **Uncontrollable/unobservable modes**: A pole canceled by a zero in the transfer function loses observability/controllability from that input-output pair.
- **Hidden modes**: Poles canceled in TF but still present in state-space → hidden (unobservable or uncontrollable).
- Engineering caution: exact cancellation is impossible in practice due to parameter tolerance, leading to robustness issues.

### Why Cancellation Matters
- If a RHP zero is canceled by a RHP pole, the transfer function appears stable but the internal state is unstable → dangerous in practice.
- Pole-zero cancellation can remove a pole but the mode may reappear due to perturbations.

## 8. Pole-Zero Cancellation in Design
- Non-minimum phase zeros cannot be canceled for stability reasons.
- Canceling slow (dominant) poles is a common control design trick to improve response speed.
- Zero-pole cancellation must preserve internal stability (avoid canceling RHP poles).

## 9. Minimum vs Non-Minimum Phase
- **Minimum phase**: All zeros in LHP (or at origin).
- **Non-minimum phase**: At least one zero in RHP (right half plane) or a pure delay.
- Non-minimum phase systems have:
  - Initial response in opposite direction.
  - Reduced achievable phase margin.
  - Larger phase lag.

## 10. DC Gain
- DC gain = G(0) = value of transfer function at s=0.
- For steady-state response to a step input, final value = DC gain × step magnitude (if stable).
- G(0) relates directly to static error constants.

## 11. Transfer Function Identification from Frequency Response
- Magnitude at low frequency gives DC gain (or slope for type 1/2 systems).
- Bode plot slope indicates pole/zero order.
- Each real pole reduces slope by -20 dB/decade, each zero increases by +20 dB/decade.

## 12. Stability Roots Summary
| System | All poles in LHP? | Stable |
|---|---|---|
| G(s) = 1/(s+2) | Yes (pole at -2) | Stable |
| G(s) = 1/(s-2) | No (pole at +2) | Unstable |
| G(s) = 1/s | On axis | Marginally stable |
| s²+ω² | On axis | Marginally stable |

## Key ISRO Points
- Poles → stability, zeros → response shape.
- Order = pole count.
- Physically realizable → proper transfer function.
- Pole-zero cancellation hides dynamic modes.
- DC gain = G(0).
- Characteristic equation 1+G(s)H(s)=0 governs closed-loop stability.
