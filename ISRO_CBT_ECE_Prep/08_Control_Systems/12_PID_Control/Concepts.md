# PID Control - Concepts

## 1. What is a PID Controller?
- A **Proportional-Integral-Derivative (PID)** controller computes an error value and applies a correction based on proportional, integral, and derivative terms.
- u(t) = K_p·e(t) + K_i·∫e(t)dt + K_d·de(t)/dt.
- The most widely used feedback controller in industry (over 90% of control loops).

## 2. Control Actions

### Proportional (P) Action
u_p = K_p·e(t)
- Output proportional to current error.
- Reduces error but leaves **steady-state error** (offset) for step inputs.
- Increasing K_p reduces offset but too much → instability/oscillation.

### Integral (I) Action
u_i = K_i·∫e(t)dt
- Output proportional to accumulated error.
- **Eliminates steady-state error** by increasing control action as long as error persists.
- Adds phase lag (reduces phase margin) → can cause oscillation if too strong (integral windup).
- Slows response.

### Derivative (D) Action
u_d = K_d·de(t)/dt
- Output proportional to rate of change of error.
- **Anticipates** error → improves damping, reduces overshoot.
- Adds phase lead.
- Sensitive to noise (amplifies high-frequency noise).
- Cannot be used alone (does nothing for constant error).

## 3. PID Transfer Function
G_c(s) = K_p + K_i/s + K_d·s
      = (K_d·s² + K_p·s + K_i)/s

### Alternate standard forms
G_c(s) = K_p·(1 + 1/(T_i·s) + T_d·s)

Where:
- T_i = integral time constant = K_p/K_i.
- T_d = derivative time constant = K_d/K_p.

## 4. Effect of Each Term Summary

| Term | Steady-state error | Overshoot | Settling time | Stability |
|---|---|---|---|---|
| P (↑K_p) | ↓ (but not zero) | ↑ | ↓ | ↓ |
| I (↑K_i) | → 0 | ↑ | ↑ | ↓ |
| D (↑K_d) | no effect | ↓ | ↓ | ↑ |

## 5. Common PID Variants
- **P only**: fastest, but offset.
- **PI**: eliminates offset, good for processes with small lags.
- **PD**: reduces overshoot, faster, but no offset removal.
- **PID**: combined, best performance within limits.
- Note: proper physical controllers may use filtered derivative to limit noise.

## 6. Ziegler-Nichols Tuning Methods

### Method 1: Open-Loop (Reaction Curve / Process Reaction Method)
- Apply a step input, record the S-shaped (Sigmoid) step response.
- Find parameters: delay L, time constant T, process gain K.
- Use table to set K_p, T_i, T_d (or K_i, K_d).

### Method 2: Closed-Loop (Ultimate Gain / Frequency Response Method)
1. Set I and D to zero (use P controller only).
2. Increase K_p until sustained oscillation (marginal stability). Record:
   - **Ultimate gain** K_u.
   - **Ultimate period** P_u (period of oscillation).
3. Use Ziegler-Nichols tables.

### Ziegler-Nichols Closed-Loop Tuning Table (based on K_u, P_u)
| Controller | K_p | T_i | T_d |
|---|---|---|---|
| P | 0.5·K_u | ∞ | 0 |
| PI | 0.45·K_u | P_u/1.2 | 0 |
| PID | 0.6·K_u | P_u/2 | P_u/8 |

### Equivalent K_i, K_d
K_i = K_p/T_i, K_d = K_p·T_d.

### Z-N Open-Loop (Reaction curve) Table (based on L, T, K)
| Controller | K_p | T_i | T_d |
|---|---|---|---|
| P | T/(K·L) | ∞ | 0 |
| PI | 0.9·T/(K·L) | L/0.3 | 0 |
| PID | 1.2·T/(K·L) | 2L | 0.5L |

## 7. Advantages & Disadvantages

### Proportional
- Adv: simple, fast.
- Disadv: steady-state offset.

### Integral
- Adv: removes offset.
- Disadv: instability risk, windup, slower, phase lag.

### Derivative
- Adv: damping, overshoot reduction, anticipates.
- Disadv: noise amplification, not standalone.

## 8. Integral Windup
- Occurs when actuator saturates: integrator keeps accumulating error → large overshoot when error changes sign.
- Mitigated by anti-windup (clamping integrator when saturated).

## 9. PID Implementation (Digital)
- Discrete approximation:
  - Derivative: (e[k] − e[k−1])/T_s (backward difference).
  - Integral: Σ e[k]·T_s (summation) or trapezoidal.
- **Positional PID**: computes full u each sample.
- **Velocity (incremental) PID**: computes change Δu — avoids reset windup, smoother.
- Sample rate must be fast enough (≥10× closed-loop bandwidth).

## 10. PID Tuning Rules of Thumb
- High K_p → fast but oscillatory.
- High K_i → zero offset but risk of oscillation/windup.
- High K_d → less overshoot but noise-sensitive.
- Start with P, add I, then D.

## 11. ISRO Exam Relevance
- Characteristics of P, I, D actions (effect on error, overshoot, stability).
- PID transfer function identification.
- Ziegler-Nichols table constants.
- Recognize formula for u(t) and G_c(s).

## 12. Pole-zero View of PID
G_c(s) = (K_d s² + K_p s + K_i)/s.
- Two zeros (from numerator quadratic) + one pole at origin (integrator).
- The integrator (pole at origin) ensures zero steady-state error.
- Zeros add phase lead and improve damping.
