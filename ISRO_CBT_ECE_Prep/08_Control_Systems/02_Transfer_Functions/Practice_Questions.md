# Transfer Functions - Practice Questions

## Section A: Conceptual Questions

**Q1.** Define the transfer function and state its key assumption.
**A1.** Ratio of Laplace transforms of output to input with ALL initial conditions zero. It is a property of the system, not the input.

**Q2.** Where must all poles lie for a stable system?
**A2.** All poles must lie in the left half of the s-plane (negative real parts).

**Q3.** Do zeros affect the stability of a system?
**A3.** No. Zeros affect the transient response shape, but only poles determine stability (excluding cancellation effects).

**Q4.** What is the 'order' of a system?
**A4.** The degree of the denominator polynomial = number of poles = number of state variables.

## Section B: Pole-Zero Analysis

**Q5.** Find poles and zeros of G(s) = (s+3)/(s(s+2)(s+5)).
**A5.** Zeros: s = -3. Poles: s = 0, -2, -5. Third order system.

**Q6.** For G(s) = (s²+4)/(s²+2s+5), find the poles and zeros.
**A6.** Zeros: s²+4=0 → s = ±j2 (imaginary zeros). Poles: s²+2s+5=0 → s = -1±j2.

**Q7.** A system has characteristic equation s³+4s²+5s+2=0. What is the order?
**A7.** Third order (highest power of s is 3).

**Q8.** Find poles and determining stability: G(s) = 4/(s²-4).
**A8.** Poles at s = ±2. One pole at +2 (RHP) → unstable system.

## Section C: Proper/Improper

**Q9.** Classify G(s) = (s+1)/(s²+2s+3). Proper or improper?
**A9.** Proper (m=1 ≤ n=2). Strictly proper.

**Q10.** Classify G(s) = (s²+s)/(s+1).
**A10.** Improper (m=2 > n=1). Note: s+1 divides evenly, giving G(s)=s, still improper/high-pass.

**Q11.** Which of these is REALIZABLE: (a) G(s)=s, (b) G(s)=1/s, (c) G(s)=s+2?
**A11.** (b) 1/s is realizable (integrator). (a) s and (c) s+2 are differentiators → not physically realizable as passive circuits.

**Q12.** For G(s) = (s+1)/(s+2), what is the high-frequency gain?
**A12.** Biproper (m=n=1). High-frequency gain = 1 (ratio of leading coefficients).

## Section D: Gain and Parameters

**Q13.** Find the DC gain of G(s) = 5(s+3)/((s+1)(s+4)).
**A13.** G(0) = 5(3)/(1·4) = 15/4 = 3.75.

**Q14.** A second-order system has denominator s²+2s+10. Find ω_n and ζ.
**A14.** ω_n = √10 ≈ 3.162. ζ = 2/(2√10) = 1/√10 ≈ 0.316.

**Q15.** Find poles of s²+4s+13=0 and identify system type (under/over/critically damped).
**A15.** Poles: s = -2±j3 (complex). ζ = 4/(2√13) = 2/3.61 = 0.554 → underdamped.

**Q16.** For G(s) = 10/(s(s+5)) with unity feedback, find the closed-loop characteristic equation.
**A16.** 1 + 10/(s(s+5)) = 0 → s²+5s+10 = 0.

## Section E: System Type & Error Constants

**Q17.** Determine the type of G(s) = 8/(s²(s+2)).
**A17.** Two poles at origin → Type 2 system.

**Q18.** For a type 0 system with K_p = 10, find steady-state error to a step input.
**A18.** e_ss = 1/(1+K_p) = 1/11 ≈ 0.0909.

**Q19.** A unity feedback type 1 system has K_v = 25. Find error to a unit ramp.
**A19.** e_ss = 1/K_v = 1/25 = 0.04.

**Q20.** For G(s) = 5/(s(s+3)) unity feedback, find K_v and ramp error.
**A20.** K_v = lim(s→0) s·G(s) = lim(s→0) 5/(s+3) = 5/3 ≈ 1.667. e_ss = 1/K_v = 3/5 = 0.6.

## Section F: Pole-Zero Cancellation

**Q21.** G(s) = [(s+2)]/[(s+2)(s+5)]. What happens?
**A21.** The zero at s=-2 cancels the pole at s=-2. Reduced TF: G(s) = 1/(s+5). The mode corresponds to -2 becomes hidden.

**Q22.** Why is canceling a RHP pole with a zero dangerous?
**A22.** The RHP pole mode is removed from the TF but remains internally present; any perturbation or parameter mismatch re-excites it → instability.

**Q23.** After cancellation in G(s) = (s-1)/((s-1)(s+3)), analyze the true stability.
**A23.** Formally G(s) = 1/(s+3) is stable, but the canceled RHP pole at +1 is a hidden unstable mode → system is NOT internally stable.

## Section G: ISRO-Style Questions

**Q24.** A system's transfer function is G(s) = 1/(0.5s+1). Identify time constant, pole, and DC gain.
**A24.** Time constant τ = 0.5 s. Pole at s = -2. DC gain = 1.

**Q25.** G(s) = 4/(s²+4s+16). Find ω_n, ζ, and nature of response.
**A25.** ω_n = 4, ζ = 4/(2·4) = 0.5. Underdamped, oscillatory.

**Q26.** Does the system G(s) = (s²+2s)/(s³+4s) have any pole at origin? Determine type.
**A26.** s³+4s = s(s²+4). One pole at origin → type 1 system.

**Q27.** Given G(s) = K(s+5)/(s(s+2)(s+10)). How many asymptotes point toward infinity in the root locus (poles=3, zeros=1)?
**A27.** n-m = 3-1 = 2 asymptotes.

**Q28.** Identify which transfer function represents a second-order underdamped system: (a) 1/(s+2), (b) 1/(s²+4s+16), (c) 1/(s²+8s+16).
**A28.** (b) 1/(s²+4s+16): ζ = 4/(2·4) = 0.5 underdamped. (c) is critically damped (ζ=1). (a) is first order.

## Common Mistakes to Avoid
1. Applying final value theorem without checking stability.
2. Confusing 'order' and 'type'.
3. Saying zeros affect stability (they don't directly).
4. Thinking improper TF is realizable.
5. Ignoring hidden modes in pole-zero cancellation.
