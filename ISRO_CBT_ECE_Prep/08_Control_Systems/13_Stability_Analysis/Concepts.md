# Stability Analysis - Concepts

## 1. Overview of Stability
Stability means a system's response to a bounded input remains bounded and settles appropriately. Multiple mathematical definitions exist.

## 2. BIBO Stability (Bounded Input, Bounded Output)
- A system is **BIBO stable** if every bounded input produces a bounded output.
- **Criterion**: For LTI systems, BIBO stability ⇔ all poles of the transfer function lie strictly in the left half plane (LHP).
- Also: impulse response h(t) is absolutely integrable: ∫₀^∞|h(t)|dt < ∞.
- Equivalent: all poles have negative real parts.

### BIBO for Input-Output perspective
- Concerned only with external (input-output) behavior.
- Does not see internal modes (may hide unstable internal states via pole-zero cancellation).

## 3. Asymptotic Stability
- A system is **asymptotically stable** if, starting near equilibrium, the state returns to equilibrium as t→∞.
- **Criterion**: All eigenvalues of A (for state-space) have strictly negative real parts.
- Equivalent to all closed-loop poles in LHP.
- Stronger than BIBO in the sense it considers internal behavior.

### Distinction
- BIBO: external stability (input-output).
- Asymptotic (Lyapunov/internal): internal stability (state).
- A system can be BIBO stable but NOT asymptotically stable if it has an uncontrollable/unobservable unstable mode (hidden).

## 4. Lyapunov Stability Methods
- Provide rigorous definition & tests for stability, especially for nonlinear systems.

### Conceptual definitions
- **Lyapunov stable (stable in sense of Lyapunov)**: For any small perturbation, the trajectory stays within a bounded region for all time.
- **Asymptotically stable**: Lyapunov stable AND trajectory converges to equilibrium as t→∞.
- **Exponentially stable**: convergence at exponential rate.
- **Marginally stable**: stable but not asymptotically (pure imaginary poles).

### Lyapunov's Direct (Second) Method
- Find a Lyapunov function V(x) ≥ 0, with V(x)=0 only at equilibrium.
- If V̇(x) < 0 (negative definite) for x≠0 → asymptotically stable.
- Applies to LTI and nonlinear systems.
- No closed-form solution needed.

### Lyapunov Equation (for LTI)
Given system ẋ = Ax, choose Q>0 (symmetric positive definite).
**AᵀP + PA = −Q**
- If solution P (symmetric) is positive definite → system asymptotically stable.
- Equivalent to all eigenvalues of A in LHP.

### Lyapunov Stability (first method / indirect)
- For LTI, eigenvalues determine stability — Lyapunov criterion reduces to checking eigenvalues.

## 5. Stability Criteria (Methods) Summary

### Routh-Hurwitz (algebraic)
- Uses characteristic equation coefficients.
- Determines if any roots in RHP without solving.

### Root Locus (graphical)
- Shows closed-loop pole movement as K varies.
- Stability region = portions in LHP; crossing jω = marginal.

### Nyquist Criterion (frequency, open-loop)
- Counts encirclements of −1 by open-loop frequency response.
- Handles delay and non-minimum phase.

### Bode (frequency, margins)
- Gain/phase margins indicate closeness to instability.

## 6. Comparison of Methods

| Method | Type | Input | Handles delay/RHP zeros | Result |
|---|---|---|---|---|
| Routh | Algebraic | char. eq. coeffs | no (needs polynomial) | stability & K range |
| Root locus | Graphical | open-loop TF | yes | pole trajectories |
| Nyquist | Frequency | open-loop freq response | yes | stability, margins |
| Bode | Frequency | open-loop | yes (with care) | margins |
| Lyapunov | Theoretic | state eq / nonlinear | yes | stability proof |

## 7. Relating Stability to Pole Locations

| Pole location | Stability type |
|---|---|
| All negative real parts (LHP) | Asymptotically stable |
| At least one positive real part | Unstable |
| Pure imaginary (nonrepeated) | Marginally stable (oscillation) |
| Repeated imaginary | Unstable (growth) |
| At origin (single) | Marginally stable (integrator) |

## 8. Internal vs External Stability
- **External (BIBO)**: defined by input-output TF.
- **Internal (Lyapunov/asymptotic)**: defined by state-space A, considering all modes.
- Cancellation of RHP pole-zero → externally stable but internally unstable.

## 9. Lyapunov for Nonlinear Systems
- Linearization (Jacobian) at equilibrium gives local stability.
- Direct method gives global results if a suitable V exists.
- Common V choices: quadratic V = xᵀPx.

## 10. Marginal Stability
- Distinct imaginary poles ±jω → oscillation at ω.
- For these, bounded but non-decaying responses (e.g., undamped oscillation, integrator).
- Steady-state oscillation persists.

## 11. Practical Stability Checks in ISRO
- Given characteristic equation → Routh.
- Given transfer function → determine poles.
- Given state matrix → eigenvalues.
- Given frequency response → Nyquist/Bode margins.

## 12. Relation to the Other Chapters
- This is the synthesis chapter — stability touched by Routh, root locus, Nyquist, margins.
- Deep understanding of each method strengthens overall exam performance.

## 13. Common Pitfalls
- Confusing BIBO and asymptotic stability.
- Believing "all positive coefficients" always means stable (it's necessary, not sufficient).
- Assuming positive Bode margins always mean stable for non-minimum phase systems.
- Forgetting marginal stability ≠ stable in a strict sense.
