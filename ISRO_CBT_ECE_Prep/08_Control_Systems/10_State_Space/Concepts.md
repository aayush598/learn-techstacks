# State Space - Concepts

## 1. Introduction
- **State-space** representation describes a system using first-order differential equations (state equations).
- Powerful for MIMO systems, nonlinear, and time-varying systems.
- Provides internal description (states), not just input-output.
- The state at time t is the minimum information needed to predict future behavior given the input.

## 2. State, State Variables, State Vector
- **State variables** x₁, x₂, ..., x_n: minimum set of variables that completely describe the system.
- **State vector**: x = [x₁ x₂ ... x_n]ᵀ.
- Number of state variables = order of the system = number of energy storage elements.
- Choice of state variables is NOT unique.

## 3. State Equation & Output Equation

### Continuous-time LTI system
**ẋ = Ax + Bu**  (state equation)
**y = Cx + Du**  (output equation)

Where:
- x = state vector (n×1)
- ẋ = derivative of state
- u = input vector (r×1)
- y = output vector (m×1)
- A = system/state matrix (n×n)
- B = input matrix (n×r)
- C = output matrix (m×n)
- D = feedforward/direct transmission matrix (m×r)

### D matrix
- Direct transmission from input to output (bypassing states).
- Usually D=0 for most physical systems (no algebraic feedthrough).

## 4. Matrix Dimensions
| Matrix | Size |
|---|---|
| A | n × n |
| B | n × r |
| C | m × n |
| D | m × r |

Where n = #states, r = #inputs, m = #outputs.

## 5. Deriving State-Space from Transfer Function
### Direct (Controllable/Phase-variable) Form
For G(s) = (b_m s^m + ... + b_0)/(s^n + a_{n-1}s^{n-1}+...+a_0):
A = companion matrix (controllable canonical)
B = [0 ... 0 1]ᵀ
C = [b_0−a_0 b_n, ..., b_{n-1}−a_{n-1} b_n]

### Observable Canonical Form
A = transpose of controllable companion
B = column [first column of C cont. form]...

## 6. State Transition Matrix
- Solution of homogeneous state eq: x(t) = Φ(t)x(0).
- **Φ(t) = e^{At} = L⁻¹{(sI−A)⁻¹}**.
- e^{At} = I + At + (At)²/2! + (At)³/3! + ...
- Properties:
  - Φ(0) = I.
  - Φ⁻¹(t) = Φ(−t).
  - Φ(t₁+t₂) = Φ(t₁)·Φ(t₂).
  - d/dt Φ(t) = AΦ(t).

### Full Solution
x(t) = e^{A(t−t₀)}x(t₀) + ∫ₜ₀ᵗ e^{A(t−τ)}Bu(τ)dτ

## 7. Transfer Function from State Space
G(s) = C(sI − A)⁻¹B + D

Where (sI−A)⁻¹ is the resolvent matrix.

## 8. Controllability
- A system is **controllable** if any state can be driven to any other state in finite time using the input.
- **Controllability matrix**: Q_c = [B  AB  A²B  ...  A^{n-1}B].
- System controllable ⇔ rank(Q_c) = n.
- A system must be controllable for full state feedback pole placement.

### Kalman Controllability Test
rank[B | AB | A²B | ... | A^{n-1}B] = n → controllable.

## 9. Observability
- A system is **observable** if all states can be determined from the output over finite time.
- **Observability matrix**: Q_o = [C; CA; CA²; ...; CA^{n-1}] (n rows).
- System observable ⇔ rank(Q_o) = n.

### Kalman Observability Test
rank[C; CA; ...; CA^{n-1}] = n → observable.

## 10. Canonical Forms
1. **Controllable canonical form (Phase-variable)**: A is companion with last row = negative characteristic coefficients.
2. **Observable canonical form**: Transpose structure.
3. **Diagonal (Jordan) form**: A diagonal; states decoupled; used for analysis.
4. **Jordan form**: for repeated eigenvalues.

### Controllable Canonical
A = [[0,1,0,...],[0,0,1,...],...,[−a₀,−a₁,...,−a_{n-1}]]
B = [0,0,...,1]ᵀ

### Observable Canonical
A = [[0,0,...,−a₀],[1,0,...,−a₁],[0,1,...,−a₂],...]
B = [b₀, b₁, ..., b_{n-1}]ᵀ (adjusted)
C = [0,0,...,1]

## 11. Eigenvalues & Stability
- Eigenvalues of A = poles of the system = roots of characteristic equation det(sI−A)=0.
- System stable ⇔ all eigenvalues of A have negative real parts.
- Used to check internal stability.

## 12. State Feedback
- Control law u = −Kx.
- Closed-loop: A_cl = A − BK.
- Eigenvalues placed arbitrarily if controllable.
- Pole placement design.

## 13. Observable/Controllable Decomposition
- Uncontrollable/unobservable modes appear in transfer function only if controllable & observable simultaneously.
- Pole-zero cancellation in TF = loss of controllability or observability.

## 14. ISRO Commonly Tests
- Identify A, B, C, D matrices for a given system.
- State transition matrix computation (e^{At}).
- Controllability/observability using Kalman rank test.
- Transfer function from state space.
- Canonical forms identification.

## 15. Advantages of State Space
- Handles multiple inputs/outputs.
- Internal states visible.
- Nonlinear/time-varying extensions natural.
- Digital & sampled control compatibility.
