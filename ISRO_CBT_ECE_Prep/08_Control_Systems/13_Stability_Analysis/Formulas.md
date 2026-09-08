# Stability Analysis - Formulas

## 1. BIBO Stability
System BIBO stable ⇔ ∫₀^∞|h(t)|dt < ∞ (impulse response absolutely integrable).
For LTI: BIBO stable ⇔ all poles of TF strictly in LHP.

## 2. Asymptotic Stability (State-Space)
Asymptotically stable ⇔ all eigenvalues of A have Re(λ) < 0.
⇔ all roots of det(sI−A)=0 in LHP.

## 3. Lyapunov Equation
For ẋ = Ax:
**AᵀP + PA = −Q**
Where Q = Qᵀ > 0 (chosen), find P.
P = Pᵀ positive definite → asymptotically stable.

### Solution (when exists)
P = ∫₀^∞ e^{Aᵀt}Qe^{At} dt.

## 4. Lyapunov Function
V(x) = xᵀPx (quadratic candidate).
V̇(x) = xᵀ(AᵀP+PA)x = −xᵀQx.
V̇ < 0 for x≠0 → asymptotically stable.

## 5. Stability by Eigenvalues
- All Re(λ_A) < 0 → asymptotically stable.
- Any Re(λ_A) > 0 → unstable.
- Re(λ_A)=0 (pure imaginary, simple) → marginally stable.

## 6. Routh-Hurwitz Stability
Char. eq. a_n s^n + ... + a_0 = 0.
- Necessary: all a_i > 0 (nonzero).
- Sufficient: all first-column entries of Routh array > 0.
- # of RHP roots = # of sign changes in first column.
- Zero row → auxiliary equation; symmetric roots.

## 7. Root Locus Stability
Closed-loop poles from 1 + KG(s)H(s) = 0.
- LHP portion → stable.
- jω crossing → marginal, gain K_crit.
- RHP → unstable.

## 8. Nyquist Stability
Z = N + P.
- Z=0 → stable.
- Encirclements of −1 counted.

## 9. Bode Margins
GM = −20log₁₀|GH(jω_pc)|.
PM = 180° + ∠GH(jω_gc).
Positive GM & PM → stable (for P=0).

## 10. Exponential Stability
System exponentially stable if ∃ α,β>0:
‖x(t)‖ ≤ α·e^{−βt}·‖x(0)‖.
Equivalent to max[Re(λ)] < 0.

## 11. Pole Zero Cancellation & Internal Stability
G(s) = C(sI−A)⁻¹B.
- Cancelled RHP pole → external (BIBO) stable but internal (asymptotic) unstable.

## 12. Stability Classification Table

| Eigenvalues / Poles | Stability |
|---|---|
| All Re < 0 | Asymptotically stable |
| All Re < 0 (in TF) | BIBO stable |
| Some Re > 0 | Unstable |
| iω, distinct | Marginally stable |
| iω, repeated | Unstable |
| 0 (simple) | Marginally stable |

## 13. Lyapunov Stability Condition for LTI (Reduces to)
Positive definite solution P to AᵀP+PA=−Q exists ⇔ A is Hurwitz (all eigenvalues LHP).
Hurwitz matrix = eigenvalues all negative real parts.

## Formula Cheatsheet (Stability)
| Criterion | Condition |
|---|---|
| BIBO | ∫\|h(t)\|dt<∞, poles LHP |
| Asymptotic | all Re(λ_A)<0 |
| Lyapunov | AᵀP+PA=−Q, P>0 |
| Exponential | max Re(λ)<0 |
| Routh | first col all >0 |
| Nyquist | Z=N+P=0 |
| Margins | GM>0, PM>0 (P=0) |
| Marginal | iω poles (distinct) |

## Notes
- BIBO ⊆ weaker than asymptotic stability generally.
- Hurwitz stability for continuous LTI = all eigenvalues strictly LHP.
