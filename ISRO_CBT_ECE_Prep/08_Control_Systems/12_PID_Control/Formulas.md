# PID Control - Formulas

## 1. Time-Domain PID
u(t) = K_p·e(t) + K_i·∫₀ᵗ e(τ)dτ + K_d·(de(t)/dt)

## 2. PID Transfer Function
G_c(s) = K_p + K_i/s + K_d·s
       = (K_d·s² + K_p·s + K_i)/s

## 3. Standard Parallel Form
G_c(s) = K_p·[1 + 1/(T_i·s) + T_d·s]

Where:
- T_i = K_p/K_i (integral time constant).
- T_d = K_d/K_p (derivative time constant).

## 4. Conversions
K_i = K_p/T_i
K_d = K_p·T_d

## 5. Ziegler-Nichols Closed-Loop (Ultimate Gain) Tuning

### Procedure
1. I, D disabled (P only).
2. Increase K_p → sustained oscillation.
3. Record K_u (ultimate gain), P_u (ultimate period).

### Table
| Controller | K_p | T_i | T_d | K_i=K_p/T_i | K_d=K_p·T_d |
|---|---|---|---|---|---|
| P | 0.5·K_u | ∞ | 0 | 0 | 0 |
| PI | 0.45·K_u | P_u/1.2 | 0 | 0.54·K_u/P_u | 0 |
| PID | 0.6·K_u | P_u/2 | P_u/8 | 1.2·K_u/P_u | 0.075·K_u·P_u |

## 6. Ziegler-Nichols Open-Loop (Reaction Curve)
Step plant, find: K (process gain), T (time constant), L (delay).

### Table
| Controller | K_p | T_i | T_d |
|---|---|---|---|
| P | T/(K·L) | ∞ | 0 |
| PI | 0.9·T/(K·L) | L/0.3 | 0 |
| PID | 1.2·T/(K·L) | 2L | 0.5L |

## 7. Tyreus-Luyben (alternative to reduce oscillation)
| Controller | K_p | T_i | T_d |
|---|---|---|---|
| PI | 0.31·K_u | 2.2·P_u | 0 |
| PID | 0.45·K_u | 2.2·P_u | P_u/6.3 |

## 8. Ultimate Period & Gain from Closed Loop
For open loop G(s):
K_u = value of K where closed loop becomes marginally stable (Routh).
P_u = 2π/ω, ω from auxiliary equation at margin.

## 9. Discrete PID (Digital Implementation)

### Positional (absolute) form
u[k] = K_p·e[k] + K_i·T_s·Σ_{j=0}^{k} e[j] + (K_d/T_s)·(e[k] − e[k−1])

### Velocity (incremental) form
Δu[k] = u[k] − u[k−1]
​      = K_p·(e[k] − e[k−1]) + K_i·T_s·e[k] + (K_d/T_s)·(e[k] − 2e[k−1] + e[k−2])

### Backward-difference derivative
de/dt ≈ (e[k] − e[k−1])/T_s

### Rectangular (forward) integral
∫e dt ≈ Σ e[j]·T_s

## 10. Transfer Function of Basic Controllers
| Type | G_c(s) |
|---|---|
| P | K_p |
| I | K_i/s |
| D | K_d·s |
| PI | K_p + K_i/s = K_p(1+1/(T_i s)) |
| PD | K_p + K_d·s = K_p(1+T_d s) |
| PID | K_p + K_i/s + K_d·s |

## 11. Closed-Loop with PID
Plant P(s), controller C(s):
T(s) = C(s)P(s)/[1 + C(s)P(s)]

## 12. Steady-State Error with Integral
With I action (pole at origin in controller), type of open loop increases by 1:
- Type 0 plant + PI → type 1 → zero step error.
- Type 1 plant + PI → type 2 → zero step AND zero ramp error.

## Formula Cheatsheet (PID)
| Item | Formula |
|---|---|
| u(t) | K_p e + K_i∫e + K_d ė |
| G_c(s) | K_p + K_i/s + K_d s |
| Parallel | K_p[1+1/(T_i s)+T_d s] |
| T_i | K_p/K_i |
| T_d | K_d/K_p |
| ZN PID (closed) | 0.6K_u, K_i=1.2K_u/P_u, K_d=0.075K_u P_u |
| P_u | 2π/ω_ult |
| Discrete D | (K_d/T_s)(e[k]−e[k−1]) |
