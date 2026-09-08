# System Modeling - Concepts

## 1. Introduction to Control Systems
- A **control system** manages, commands, or regulates the behavior of other devices using control loops.
- **Open-loop system**: No feedback; output has no effect on input (e.g., toaster).
- **Closed-loop system**: Uses feedback; output influences input (e.g., AC temperature control).
- **Feedback** can be positive (regenerative) or negative (degenerative). Negative feedback is used for stability.

## 2. Differential Equations in Modeling
- Physical systems (electrical, mechanical, thermal) are modeled using differential equations.
- The relationship between input and output is described by an ODE with constant coefficients for LTI systems.

### Electrical Systems (RLC)
- **Kirchhoff's Voltage Law (KVL)**: Sum of voltages around a loop = 0.
- Series RLC: `L(d²q/dt²) + R(dq/dt) + q/C = v(t)` where q is charge.
- In terms of current i = dq/dt: `L(di/dt) + Ri + (1/C)∫i dt = v(t)`.
- Parallel RLC uses KCL (Kirchhoff's Current Law).

### Mechanical Systems
- **Newton's Second Law**: F = ma = m(d²x/dt²).
- Spring-damper-mass system: `m(d²x/dt²) + b(dx/dt) + kx = F(t)`.
- **Translational elements**: Mass (inertia), Spring (stiffness k), Dashpot (damping b).
- **Rotational elements**: Moment of inertia (J), Torsional spring (K), Rotational damper (B).

### Electrical-Mechanical Analogy
| Electrical | Translational | Rotational |
|------------|---------------|------------|
| Voltage (V) | Force (F) | Torque (T) |
| Current (i) | Velocity (v) | Angular velocity (ω) |
| Resistance (R) | Damping (b) | Rotational damping (B) |
| Inductance (L) | Mass (m) | Moment of inertia (J) |
| Capacitance (C) | Compliance (1/k) | Torsional compliance (1/K) |

## 3. Laplace Transform for Modeling
- Converts differential equations (time domain) to algebraic equations (s-domain).
- **Key Properties**:
  - Linearity: `L{af(t) + bg(t)} = aF(s) + bG(s)`
  - Differentiation: `L{df/dt} = sF(s) - f(0)` (with zero initial conditions: sF(s))
  - Second derivative: `L{d²f/dt²} = s²F(s) - sf(0) - f'(0)`
  - Integration: `L{∫f(τ)dτ} = F(s)/s`
  - Time shift: `L{f(t-a)u(t-a)} = e^{-as}F(s)`
  - Frequency shift: `L{e^{-at}f(t)} = F(s+a)`

### Important Laplace Transforms
| f(t) | F(s) |
|------|------|
| δ(t) (impulse) | 1 |
| u(t) (step) | 1/s |
| t (ramp) | 1/s² |
| e^{-at} | 1/(s+a) |
| sin(ωt) | ω/(s²+ω²) |
| cos(ωt) | s/(s²+ω²) |
| t^n | n!/s^{n+1} |

## 4. Transfer Function
- **Definition**: Ratio of Laplace transform of output to Laplace transform of input, assuming **all initial conditions are zero**.
- `G(s) = C(s)/R(s) = (b_m s^m + ... + b_0) / (a_n s^n + ... + a_0)`
- Transfer function is a property of the system, independent of the input.
- Poles of G(s) determine system stability and transient response.
- Zeros of G(s) affect the shape of the response.

## 5. Block Diagram Elements
- **Block**: Represents a system/component with a transfer function G(s).
- **Summing Point**: Adds or subtracts signals (represented by ⊕ or Σ).
- **Pickoff Point (Branch Point)**: Splits a signal to multiple paths.
- **Arrow**: Indicates direction of signal flow.
- **Input/Output**: Reference signal R(s) and controlled output C(s).

## 6. Impedance Approach
- In s-domain, replace components with impedances:
  - Resistor: Z_R = R
  - Inductor: Z_L = Ls (zero initial condition)
  - Capacitor: Z_C = 1/(Cs)
- Transfer function derived as ratio of impedances or voltage dividers.

## 7. State-Space Representation (Overview)
- State variables are minimum set of variables that completely describe system state.
- First-order vector differential equation: `ẋ = Ax + Bu`, `y = Cx + Du`.
- Advantage: Handles MIMO systems, nonlinear systems, and provides time-domain solution.
- State variables are not unique; different choices lead to different A, B, C, D matrices.

## 8. Analogous Systems
- Systems from different physical domains can have identical transfer functions.
- Force-voltage analogy: Mechanical translational ↔ Electrical series.
- Force-current analogy: Mechanical translational ↔ Electrical parallel.
- Same mathematical model → same dynamic behavior.

## 9. Linearization
- Most real systems are nonlinear; linearization about an operating point allows use of linear analysis.
- Taylor series expansion about equilibrium, keeping only first-order terms.
- Valid for small perturbations around the operating point.
- Jacobian matrix used for state-space linearization.

## 10. Signal Flow Conventions
- All signals are functions of s (Laplace domain).
- Arrow direction = positive signal flow direction.
- Feedback always creates a loop (closed-loop system).
- Negative feedback: subtracted at summing point; positive feedback: added.

## Key Points for ISRO Exam
- Transfer function assumes **zero initial conditions**.
- Order of a system = highest power of s in characteristic equation = number of state variables.
- A system is **proper** if degree of numerator ≤ degree of denominator.
- Block diagram reduction and signal flow graphs are equivalent tools for finding closed-loop transfer functions.
- Always check units and physical meaning when deriving transfer functions from first principles.
