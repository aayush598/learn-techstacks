# State Space - Formulas

## 1. State-Space Equations (Continuous LTI)
ẋ = Ax + Bu
y = Cx + Du

## 2. Matrix Dimensions
- A: n×n (state matrix)
- B: n×r (input matrix)
- C: m×n (output matrix)
- D: m×r (feedforward matrix)
- x: n×1, ẋ: n×1, u: r×1, y: m×1

## 3. Transfer Function from State Space
G(s) = C(sI − A)⁻¹B + D

For SISO with D=0: G(s) = C·adj(sI−A)·B / det(sI−A)

## 4. Characteristic Equation
det(sI − A) = 0
Eigenvalues of A = poles of system.

## 5. State Transition Matrix
Φ(t) = e^{At} = L⁻¹{(sI−A)⁻¹}

### Series expansion
e^{At} = I + At + (At)²/2! + (At)³/3! + ...

### Properties
- Φ(0) = I
- Φ⁻¹(t) = Φ(−t)
- Φ(t₁+t₂) = Φ(t₁)Φ(t₂)
- dΦ/dt = AΦ(t)
- Φ(t) satisfying: x(t) = Φ(t)x(0)

## 6. Solution to State Equation
x(t) = e^{A(t−t₀)}x(t₀) + ∫ₜ₀ᵗ e^{A(t−τ)}Bu(τ)dτ

For t₀=0: x(t) = e^{At}x(0) + ∫₀ᵗ e^{A(t−τ)}Bu(τ)dτ

## 7. Output Solution
y(t) = Cx(t) + Du(t)

## 8. Controllability Matrix
Q_c = [B  AB  A²B  ...  A^{n−1}B]   (n × n·r)

### Test
System controllable ⇔ rank(Q_c) = n.

For SISO (n×n matrix): det(Q_c) ≠ 0 → controllable.

## 9. Observability Matrix
Q_o = [C; CA; CA²; ...; CA^{n−1}]   (n·m × n)

### Test
System observable ⇔ rank(Q_o) = n.

For SISO (n×n): det(Q_o) ≠ 0 → observable.

## 10. Controllable Canonical Form (Phase Variable)
For G(s) = (b₀ + b₁s + ... + b_m s^m)/(s^n + a_{n−1}s^{n−1} + ... + a₀):

A = [ [0,1,0,...,0],
      [0,0,1,...,0],
      ...
      [−a₀,−a₁,−a₂,...,−a_{n−1}] ]

B = [0,0,...,0,1]ᵀ
C = [b₀−a₀b_n, b₁−a₁b_n, ..., b_{n−1}−a_{n−1}b_n]

(For strictly proper, b_n=0, D=0.)

## 11. Observable Canonical Form
A = [ [0,0,...,0,−a₀],
      [1,0,...,0,−a₁],
      [0,1,...,0,−a₂],
      ...
      [0,0,...,1,−a_{n−1}] ]

B = [b₀−a₀b_n, b₁−a₁b_n, ..., b_{n−1}−a_{n−1}b_n]ᵀ
C = [0,0,...,1]

## 12. Diagonal (Jordan) Form
If eigenvalues distinct:
A = diag(λ₁, λ₂, ..., λ_n)

## 13. Resolvent Matrix Formula
(sI − A)⁻¹ = adj(sI−A)/det(sI−A)

For A = [[0,1],[−a₀,−a₁]]:
(sI−A)⁻¹ = [1/(s²+a₁s+a₀)]·[[s+a₁, 1],[−a₀, s]]

## 14. e^{At} for 2×2 A
Compute via L⁻¹ of resolvent, or via diagonalization:
e^{At} = P·diag(e^{λ₁t}, ..., e^{λ_nt})·P⁻¹ (if diagonalizable).

## 15. State Feedback (Pole Placement)
u = −Kx
A_cl = A − BK
Places eigenvalues of A_cl → need controllability.

## 16. Observer Design
ẋ̂ = A x̂ + Bu + L(y − Cx̂)
A_obs = A − LC
Poles placed by choosing L → need observability.

## 17. Relationship: TF Pole-Zero Cancellation
- A pole canceled by a zero in G(s) = an uncontrollable or unobservable mode.
- Controllable & observable modes only appear in transfer function.

## Formula Cheatsheet (State Space)
| Quantity | Formula |
|---|---|
| State eq | ẋ = Ax + Bu |
| Output eq | y = Cx + Du |
| TF | C(sI−A)⁻¹B + D |
| Char eq | det(sI−A)=0 |
| STM | e^{At}=L⁻¹{(sI−A)⁻¹} |
| Controllability | rank[B AB ... A^{n-1}B]=n |
| Observability | rank[C;CA;...;CA^{n-1}]=n |
| State feedback | A−BK |
| Observer | A−LC |

## Important Derivations
- For 1st order A=[a]: e^{At}=e^{at}.
- For 2nd order with distinct real eigenvalues: form via P, P⁻¹.
- Resolvent leads directly to impulse response.
