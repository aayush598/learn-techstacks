# Stability Analysis - Practice Questions

## Section A: Conceptual

**Q1.** Define BIBO stability.
**A1.** Every bounded input produces a bounded output. For LTI = all TF poles in LHP / impulse response absolutely integrable.

**Q2.** Define asymptotic stability.
**A2.** Trajectories starting near equilibrium converge to equilibrium as t→∞. For LTI = all eigenvalues of A in LHP.

**Q3.** Can a system be BIBO stable but not asymptotically stable?
**A3.** Yes — if an unstable mode is hidden (uncontrollable/unobservable) via pole-zero cancellation.

**Q4.** State Lyapunov's direct method briefly.
**A4.** Find V(x)≥0 (equilibrium at 0); if V̇(x)<0 for x≠0 → asymptotically stable.

## Section B: BIBO / Pole Analysis

**Q5.** Is G(s)=1/(s−2) BIBO stable?
**A5.** No. Pole at +2 (RHP) → unstable.

**Q6.** Is G(s)=1/(s²+4) BIBO stable?
**A6.** Poles at ±j2 (imaginary axis) → NOT BIBO stable (impulse not absolutely integrable; oscillates).

**Q7.** Check G(s)=5/((s+1)(s+3)).
**A7.** Poles −1,−3 (both LHP) → BIBO stable.

## Section C: Asymptotic / Eigenvalue Analysis

**Q8.** A system with A eigenvalues −1±j2. Stability?
**A8.** Real parts negative → asymptotically stable.

**Q9.** A=[[0,1],[-4,0]]. Eigenvalues?
**A9.** det[[s,-1],[4,s]]=s²+4=0 → s=±j2 → pure imaginary → marginally stable.

**Q10.** A=[[1,2],[0,3]]. Eigenvalues & stability?
**A10.** Upper triangular → eigenvalues 1,3 (both positive) → unstable.

## Section D: Lyapunov

**Q11.** For ẋ=−2x, apply Lyapunov. Stable?
**A11.** V=x². V̇=2x·ẋ=2x(−2x)=−4x²<0 → asymptotically stable. (Eigenvalue −2.)

**Q12.** Choose Q=I, A=−2. Solve AᵀP+PA=−Q.
**A12.** P scalar: (−2)P+P(−2)=−1 → −4P=−1 → P=1/4>0 → stable.

**Q13.** A=0. Lyapunov analysis?
**A13.** AᵀP+PA=0 → any P; V̇=0 not <0 → stable in the sense of Lyapunov but NOT asymptotically stable (marginal).

## Section E: Method Comparison

**Q14.** Which method is best for a system with transport delay?
**A14.** Nyquist (handles delay in open-loop frequency response). Routh needs polynomial form.

**Q15.** Which method gives the range of gain K for stability directly?
**A15.** Routh-Hurwitz (algebraic inequalities).

**Q16.** Which method shows how poles move with gain?
**A16.** Root locus.

**Q17.** Which method computes stability margins from frequency response?
**A17.** Bode (GM/PM) or Nyquist.

## Section F: Hidden Modes / Internal Stability

**Q18.** G(s)=(s−1)/((s−1)(s+2)). BIBO stable?
**A18.** TF reduces to 1/(s+2) → BIBO stable. But internal mode at +1 is unstable & hidden → NOT asymptotically stable internally.

**Q19.** Why does cancellation hide instability?
**A19.** The RHP pole is removed from the TF but remains in state space; it's uncontrollable/unobservable externally.

**Q20.** A system is externally stable but has a hidden unstable pole—what type of stability is violated?
**A20.** Asymptotic (internal/Lyapunov) stability.

## Section G: ISRO-Style

**Q21.** Given char. eq. s³+2s²+5s+6=0, is the system stable?
**A21.** Routh: s³:1,5; s²:2,6; s¹:(10−6)/2=2; s⁰:6. First col: 1,2,2,6 all positive → stable.

**Q22.** A system with all poles in LHP — classify.
**A22.** BIBO stable and asymptotically stable (if controllable & observable).

**Q23.** Marginal stability corresponds to what poles?
**A23.** Distinct poles on imaginary axis (non-decaying oscillation or integrator).

**Q24.** Nyquist gives Z=N+P. For a stable closed loop, Z=?
**A24.** Z=0.

**Q25.** Which stability check is a "necessary but not sufficient" condition?
**A25.** All coefficients positive in the characteristic equation (Routh necessary condition).

**Q26.** A matrix A has both eigenvalues at −5. Stability?
**A26.** Both real parts −5 → asymptotically stable (and exponentially stable).

**Q27.** If a Lyapunov function yields V̇=0 (not strictly negative), what's concluded?
**A27.** Marginally stable (stable in the sense of Lyapunov) — cannot conclude asymptotic stability.

**Q28.** The impulse response of a stable system must satisfy what?
**A28.** ∫₀^∞|h(t)|dt < ∞ (absolutely integrable).

## Common Mistakes
1. Confusing BIBO and asymptotic stability.
2. Calling marginal stability "stable" without qualification.
3. Using eigenvalue test on the TF poles vs state matrix.
4. Forgetting Routh first-column all-positive requirement.
5. Overlooking hidden unstable modes in internal stability.
