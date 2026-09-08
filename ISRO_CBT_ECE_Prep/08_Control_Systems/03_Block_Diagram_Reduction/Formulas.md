# Block Diagram Reduction - Formulas

## 1. Series (Cascade) Connection
G_total(s) = G₁(s) · G₂(s) · ... · G_n(s)

For n blocks in series, multiply all transfer functions. Product order for scalar TFs is commutative.

## 2. Parallel Connection
G_total(s) = G₁(s) + G₂(s)  (if outputs summed)
G_total(s) = G₁(s) - G₂(s)  (if subtractive)

## 3. Feedback Connection

### Negative Feedback
T(s) = G(s) / [1 + G(s)·H(s)]

### Positive Feedback
T(s) = G(s) / [1 - G(s)·H(s)]

### Unity Feedback (H=1)
T(s) = G(s) / [1 + G(s)]

### Open-Loop Transfer Function (in feedback loop)
L(s) = G(s)·H(s)

### Closed-Loop Denominator (Characteristic Equation)
1 + G(s)·H(s) = 0

## 4. Moving a Pickoff Point

### Pickoff point moved from BEFORE a block G to AFTER it:
Original branch that was tapped now needs:  G(s)⁻¹ = 1/G(s) inserted in the tapped-off branch.

### Pickoff point moved from AFTER a block G to BEFORE it:
Insert block G(s) in the tapped branch.

## 5. Moving a Summing Point

### Summing point from BEFORE block G to AFTER it:
Insert block G(s) in the summed branch.

### Summing point from AFTER block G to BEFORE it:
Insert block 1/G(s) in the summed branch.

## 6. Equivalent Transformations Table

| Rule | Original | Equivalent |
|---|---|---|
| Series | G₁ → G₂ | G₁G₂ |
| Parallel | G₁ with G₂ summed | G₁ ± G₂ |
| Feedback -ve | G/(1+GH) | single block |
| Feedback +ve | G/(1-GH) | single block |
| Pickoff shifted after G | pickoff (before) | G⁻¹ in tapped branch |
| Pickoff shifted before G | pickoff (after) | G in tapped branch |
| Summing shifted after G | summing (before) | G in branch |
| Summing shifted before G | summing (after) | G⁻¹ in branch |

## 7. Superposition (Multiple Inputs)
For inputs R(s) and D(s):
C(s) = T_R(s)·R(s) + T_D(s)·D(s)
Where T_R = transfer function from R, T_D = transfer function from D (D set to zero for T_R etc.).

## 8. Sensitivity
Sensitivity of closed-loop TF T to forward gain G:
S_G^T = (∂T/T)/(∂G/G) = 1/(1+G(s)H(s))  [for negative feedback]

Sensitivity to H:
S_H^T = -G(s)H(s)/(1+G(s)H(s))

## 9. Equivalent Unity Feedback Conversion
Given non-unity feedback forward G, feedback H:
- Move H into the forward path: G' = G·H (with output scaled).
- The closed loop TF: T = G/(1+GH) = (G·H)/(1+GH) · (1/H) = G'/(1+G') · (1/H).
This lets error constants be computed from L(s)=G(s)H(s).

## 10. Sequential Reduction Example Formulas

### Two nested loops (inner loop inside outer loop)
Given:
- Inner forward: G₂, inner feedback: H₂.
- Outer forward: G₁, outer feedback: H₁ (path includes G₂'s loop).
Reduced: first reduce inner loop → T_inner = G₂/(1+G₂H₂). Then result in series with G₁ etc.

## 11. Error Transfer Functions (with G forward, H feedback)
- Error signal E(s) = R(s) - H(s)·C(s).
- E(s)/R(s) = 1/[1+G(s)H(s)] (sensitivity to reference).
- C(s)/D(s) for disturbance = G_D(s)/[1+G(s)H(s)].

## 12. Signal Flow Conversion
Block diagrams can be converted to signal flow graphs:
- Each summing point → node.
- Each signal → branch.
- Transfer functions → transmittances.
Then apply Mason's gain formula.

## Quick Reference Cheatsheet
| Structure | Transfer Function |
|---|---|
| Series | Product |
| Parallel | Sum |
| Negative feedback | G/(1+GH) |
| Positive feedback | G/(1-GH) |
| Unity feedback | G/(1+G) |
| Characteristic equation | 1+GH=0 |

## Numerical Validation Tip
To verify a reduced result, plug s = a specific value (e.g., s=1) into the original and reduced expressions and compare numeric results. Ensure sign correctness in feedback loops.
