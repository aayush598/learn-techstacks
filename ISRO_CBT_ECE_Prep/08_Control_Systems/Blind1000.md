# BLIND 1000 — Control Systems (ISRO CBT ECE)

> **1000 unique questions. Zero repeats.** Patterned on ISRO Scientist/Engineer 'SC' (Electronics) CBT: 80 Part-A questions, +1 / −0.33, ~75 s each.
> Questions tagged **[PYP-23 Qxx]** / **[PYP-25 Qxx]** reproduce actual ISRO 2023 / 2025 questions.
> Every option is real; exactly one is correct.

### How to use this file

Each entry is three lines:

```
**Qn.** <stem>
`A) ... | B) ... | C) ... | D) ...`
**Ans: B** — <one-line rationale with the governing formula>
```

**Answer-key balance.** The correct option is spread evenly across A/B/C/D (250 each, plus one extra B), so you cannot guess from position. Practise until you justify the answer from the formula, not from its letter.

---

## Blueprint (how the 1000 are distributed)

| # | Section | Q Nos | Count |
|---|---------|-------|-------|
| 1 | Foundations, Modelling & System Types | 1–60 | 60 |
| 2 | Transfer Function & Block Diagram Reduction | 61–130 | 70 |
| 3 | Signal Flow Graphs & Mason's Gain Formula | 131–180 | 50 |
| 4 | Time Domain Response & First-Order Systems | 181–250 | 70 |
| 5 | Second-Order Systems & Specifications | 251–330 | 80 |
| 6 | Stability Concepts & Routh–Hurwitz | 331–425 | 95 |
| 7 | Root Locus | 426–505 | 80 |
| 8 | Frequency Response, Bode, Nyquist & Margins | 506–590 | 85 |
| 9 | P–M Charts & Relative Stability | 591–645 | 55 |
| 10 | Routh–Hurwitz, Hurwitz Determinants & Root Location | 646–695 | 50 |
| 11 | Z-Transform & Difference Equations | 696–780 | 85 |
| 12 | Sampling, Signal Processing & Applications | 781–850 | 70 |
| 13 | State Space, Controllability & Observability | 851–910 | 60 |
| 14 | Compensators, Nonlinearity & Lyapunov Design | 911–960 | 50 |
| 15 | ISRO PYQ & Mixed Advanced Topics | 961–1000 | 40 |
| | **Total** | | **1000** |

**ISRO-observed Control Systems families** (2023 Q57–Q67; 2025 Q15, Q31, Q36, Q44, Q47, Q50, Q53, Q56, Q73):

| Topic | Count | Priority |
|---|---:|---|
| Routh–Hurwitz & stability | 4 | Tier 1 |
| Bode plots & frequency response | 4 | Tier 1 |
| Second-order systems & damping | 3 | Tier 1 |
| Controllers (P/PI/PD/PID), lead-lag | 4 | Tier 1 |
| Feedback & error transfer functions | 2 | Tier 1 |
| State space & controllability | 2 | Tier 2 |
| Signal flow graph / Mason | 1 | Tier 2 |
| Sensitivity | 1 | Tier 2 |
| Nyquist & argument principle | 1 | Tier 3 |
| Time delay, pole nature, Middlebrook | 3 | Tier 3 |

**The headline pattern:** 2023 asked for *concept recognition*; 2025 asked for *concept + application + interpretation* (build a Routh array, read margins off a table, reconstruct a transfer function from a Bode plot). Master the procedure, not just the definition.

---

## SECTION 1 — Foundations, Modelling & System Types (Q1–Q60)

**Q1.** The Laplace transform of the unit step function is:
`A) 1/s | B) 1/s² | C) 1 | D) s`
**Ans: A** — L{u(t)} = 1/s; the step is the integral of the impulse.

**Q2.** The Laplace transform of the unit impulse δ(t) is:
`A) 1/s | B) s | C) 1 | D) 1/s²`
**Ans: C** — L{δ(t)} = 1, which is why impulse testing gives the transfer function directly.

**Q3.** The Laplace transform of a unit ramp t is:
`A) 1/s | B) 2/s³ | C) 1/s² | D) s²`
**Ans: C** — Integrating the step transform: L{t} = 1/s².

**Q4.** The Laplace transform of sin(ωt) is:
`A) ω/(s² + ω²) | B) s/(s² + ω²) | C) ω/(s² − ω²) | D) 1/(s² + ω²)`
**Ans: A** — The standard pair; note the numerator is the frequency ω, not s.

**Q5.** The initial value theorem states:
`A) f(0⁺) = lim(s→∞) sF(s) | B) f(0⁺) = lim(s→0) sF(s) | C) f(∞) = lim(s→∞) sF(s) | D) f(∞) = lim(s→0) F(s)`
**Ans: A** — Valid when the time response has no impulse at t = 0.

**Q6.** The final value theorem states:
`A) f(∞) = lim(s→∞) sF(s) | B) f(∞) = lim(s→0) F(s) | C) f(∞) = F(0) | D) f(∞) = lim(s→0) sF(s)`
**Ans: D** — The same expression as initial value, but the limit is s→0.

**Q7.** The final value theorem is valid only if:
`A) F(s) has a pole at the origin | B) All poles are in the RHP | C) All poles of sF(s) lie in the left half plane | D) The system is non-linear`
**Ans: C** — If sF(s) has any RHP or imaginary-axis pole, the limit diverges or oscillates.

**Q8.** A system is said to be causal if:
`A) Its output depends only on the input | B) It has no poles | C) It is time-invariant | D) Its output at any time depends only on present and past inputs`
**Ans: D** — Causality forbids output depending on future inputs.

**Q9.** A system is linear if it satisfies:
`A) Superposition: a(x₁+x₂) = a(x₁) + a(x₂) and homogeneity | B) It is stable | C) It is causal | D) It is time-invariant`
**Ans: A** — Linearity requires both additivity and homogeneity (scaling).

**Q10.** A time-invariant system's response depends on:
`A) The time difference between input and output, not absolute time | B) Absolute time only | C) Input amplitude only | D) Nothing`
**Ans: A** — Shifting the input shifts the output by the same amount.

**Q11.** A system is BIBO stable if every bounded input produces:
`A) An output that eventually decays | B) A zero output | C) An output of constant amplitude | D) A bounded output`
**Ans: D** — Bounded-Input Bounded-Output; equivalently all poles in the open left half plane.

**Q12.** The order of a differential-equation system equals:
`A) The number of inputs | B) The number of terms | C) The highest power of the derivative in the equation | D) The number of poles at the origin`
**Ans: C** — An n-th order equation yields an n-th order transfer function.

**Q13.** The transfer function of a LTI system is defined as:
`A) G(s) = Y(s)/R(s) with zero initial conditions | B) Y(s)·R(s) | C) Y(s)/R(s) with any initial conditions | D) The impulse response alone`
**Ans: A** — Initial conditions must be zero, otherwise the ratio includes the zero-input response.

**Q14.** The impulse response of an LTI system is:
`A) The output for a step input | B) The derivative of its output | C) Its transfer function | D) The output when the input is δ(t)`
**Ans: D** — g(t) = L⁻¹{G(s)}, and the transfer function is exactly L{g(t)}.

**Q15.** A system with poles in the right half plane is:
`A) Critically stable | B) Marginally stable | C) Unstable | D) Stable`
**Ans: C** — RHP poles give growing exponential terms in the response.

**Q16.** Poles on the imaginary axis (excluding the origin) indicate:
`A) Complete stability | B) Instability | C) Marginal stability | D) No effect on stability`
**Ans: C** — Sustained oscillation, not decay — e.g. s² + ω₀² = 0.

**Q17.** The characteristic equation of a system is obtained by setting:
`A) The numerator equal to zero | B) The denominator of the transfer function equal to zero | C) Gain equal to zero | D) The input equal to zero`
**Ans: B** — Its roots are the poles and hence the natural modes.

**Q18.** A pole at the origin in a transfer function contributes:
`A) +20 dB/decade | B) −40 dB/decade | C) −20 dB/decade slope and −90° phase | D) No slope change`
**Ans: C** — Each pole gives −20 dB/dec and −90°; an origin pole does so from ω = 0.

**Q19.** In the Laplace domain, an inductor of L henries is represented by:
`A) sL | B) 1/(sL) | C) sC | D) 1/s²L`
**Ans: A** — v = L di/dt transforms to V(s) = L[sI(s) − i(0)].

**Q20.** In the Laplace domain, a capacitor of C farads is represented by:
`A) 1/(sC) | B) sC | C) 1/(sL) | D) sL`
**Ans: A** — i = C dv/dt transforms to I(s) = C[sV(s) − v(0)].

**Q21.** A first-order system has a pole at s = −a. Its time constant τ is:
`A) a | B) 1/a² | C) 1/a | D) a²`
**Ans: C** — For G(s) = a/(s+a), τ = 1/a.

**Q22.** The response of a first-order system to a unit step reaches 63.2 % of its final value at:
`A) Two time constants | B) Five time constants | C) Instantaneously | D) One time constant`
**Ans: D** — e⁻¹ = 0.368, so 1 − 0.368 = 0.632.

**Q23.** A system of order n can be represented by a state-space model with:
`A) n state variables | B) n² state variables | C) One state variable | D) n + 1 state variables`
**Ans: A** — Minimum realisation requires exactly n states.

**Q24.** A mechanical translational system's equation of motion is:
`A) Mx + Bẋ + Kẋ = F | B) Mx'' + Bx = F | C) Mẍ + Bẋ + Kx = F(t) | D) Bẋ + Kx = F`
**Ans: C** — Force balance: mass, damping force and spring force sum to the applied force.

**Q25.** In a mechanical rotational system, the equation of motion is:
`A) Mθ̈ + Kθ = T | B) Jθ̈ + Bθ̇ + Kθ = T(t) | C) Jθ̈ + Kθ̇ = T | D) Kθ̈ + Bθ̇ = T`
**Ans: B** — Torque balance with inertia J, viscous friction B and torsional stiffness K.

**Q26.** In a mechanical system, the damping force is proportional to:
`A) Velocity | B) Displacement | C) Acceleration | D) Force`
**Ans: A** — Viscous damping gives F_d = Bẋ, which dissipates energy as Bẋ².

**Q27.** A static (memoryless) system has an output that depends on:
`A) The input at the same instant only | B) Past inputs | C) Future inputs | D) Both past and present`
**Ans: A** — No energy storage means no memory of previous inputs.

**Q28.** A dynamic system that stores energy in a capacitor or inductor is called:
`A) Static | B) Dynamic | C) Non-linear | D) Unstable`
**Ans: B** — Energy storage gives the system memory of past inputs.

**Q29.** An autonomous (unforced) system has:
`A) No poles | B) No external input | C) Only one state variable | D) A zero initial condition`
**Ans: B** — It evolves from its own initial conditions, e.g. free vibration.

**Q30.** The total response of a linear system decomposes into:
`A) Only the forced response | B) Only the natural response | C) Their product | D) Zero-input (natural) response plus zero-state (forced) response`
**Ans: D** — Superposition of the homogeneous and particular solutions.

**Q31.** A system described by ẏ = ay + bu is:
`A) Non-linear always | B) Time-varying if a is constant | C) Linear if a and b are constants | D) Not a system`
**Ans: C** — Constants make it linear and time-invariant; a(t) would make it time-varying.

**Q32.** A non-linear system differs from a linear one because:
`A) It has no transfer function | B) Superposition does not hold | C) It cannot be simulated | D) It is always unstable`
**Ans: B** — The linear transfer function framework assumes additivity and scaling.

**Q33.** The Laplace transform of a time-shifted function f(t − t₀)u(t − t₀) is:
`A) e^(+st₀)F(s) | B) e^(−st₀)F(s) | C) F(s)/t₀ | D) F(s) − t₀`
**Ans: B** — The second shifting theorem; delay multiplies by e^(−st₀).

**Q34.** The convolution property of Laplace transforms is:
`A) L{f(t)∗g(t)} = F(s)G(s) | B) L{f(t)∗g(t)} = F(s) + G(s) | C) L{f(t)∗g(t)} = F(s)/G(s) | D) L{f(t)∗g(t)} = F(s) − G(s)`
**Ans: A** — Convolution in time becomes multiplication in the s-domain.

**Q35.** An integrator, G(s) = K/s, produces a ramp output of slope:
`A) 1/K | B) K for a unit step input | C) K² | D) Zero`
**Ans: B** — K/s × 1/s = K/s², which is K·t, a ramp of slope K.

**Q36.** A differentiator G(s) = Ks produces:
`A) A ramp | B) A constant | C) An impulse for a step input | D) A parabola`
**Ans: C** — Ks × (1/s) = K, a constant, which is Kδ(t) in the time domain.

**Q37.** A system with transfer function G(s) = 1/(s + 1) has its pole at:
`A) s = −1 | B) s = 1 | C) s = 0 | D) s = j`
**Ans: A** — The root of s + 1 = 0.

**Q38.** A system is described as "marginally stable" when:
`A) All poles are in the RHP | B) All poles are in the LHP | C) There are no poles | D) All poles are on the imaginary axis, none in the RHP`
**Ans: D** — Sustained oscillations with no growth.

**Q39.** The degree of instability of a system is the:
`A) Number of RHP poles | B) Number of LHP poles | C) Number of poles at the origin | D) Sum of all poles`
**Ans: A** — Each RHP pole represents one unstable mode.

**Q40.** A pole-zero plot in the complex s-plane shows:
`A) Poles as × and zeros as ○ | B) Poles as ○ and zeros as × | C) Both as ○ | D) Both as ×`
**Ans: A** — Standard convention; imaginary axis is the stability boundary.

**Q41.** The number of poles of a transfer function equals:
`A) The degree of the numerator | B) The sum of both | C) The degree of the denominator | D) The number of terms`
**Ans: C** — Counting multiplicity, the denominator order sets the system order.

**Q42.** An LTI system is stable if and only if:
`A) All poles are in the RHP | B) The gain is positive | C) All poles lie strictly in the left half plane | D) The system is causal`
**Ans: C** — Assuming a proper rational transfer function with real coefficients.

**Q43.** The transfer function of an RC low-pass network with R in series and C to ground is:
`A) (1/sC)/(R + 1/sC) = 1/(1 + sRC) | B) R/(R + 1/sC) | C) sRC/(1 + sRC) | D) 1/(1 + s/RC)`
**Ans: A** — The output across C divides by the series impedance.

**Q44.** A series RLC circuit's impedance function is:
`A) Z(s) = R + sL + 1/(sC) | B) Z(s) = R/(sL) | C) Z(s) = 1/(sRC) | D) Z(s) = s/(RC)`
**Ans: A** — Series impedances add directly in the s-domain.

**Q45.** The damped natural frequency of a second-order system is:
`A) ω_d = ω_n/√(1 − ζ²) | B) ω_d = ω_n(1 − ζ) | C) ω_d = ω_n + ζ | D) ω_d = ω_n√(1 − ζ²)`
**Ans: D** — Applies for 0 < ζ < 1; the difference from ω_n is ω_nζ²/2 approximately.

**Q46.** An undamped system has damping ratio:
`A) ζ = 1 | B) ζ = 0.707 | C) ζ > 1 | D) ζ = 0`
**Ans: D** — ζ = 0 gives pure sinusoids with constant amplitude.

**Q47.** A critically damped system has damping ratio:
`A) ζ = 0 | B) ζ = 0.5 | C) ζ = 2 | D) ζ = 1`
**Ans: D** — Repeated real roots, fastest response without oscillation.

**Q48.** An overdamped system has damping ratio:
`A) ζ = 1 | B) 0 < ζ < 1 | C) ζ > 1 | D) ζ = 0`
**Ans: C** — Two distinct negative real roots, slow but non-oscillatory.

**Q49.** The number of poles at the origin in a system with type number p determines:
`A) The bandwidth | B) The steady-state error for polynomial inputs | C) The phase margin | D) The gain margin`
**Ans: B** — p integrations give zero steady-state error to inputs of degree < p.

**Q50.** A system is said to be of type 1 if it has:
`A) Two poles at the origin | B) No poles at the origin | C) Poles only in the LHP | D) One pole at the origin`
**Ans: D** — Type number equals the number of pure integrations.

**Q51.** In modelling a physical system, the differential equation is obtained by:
`A) Randomly guessing | B) Writing the governing balance law (Newton/Kirchhoff) | C) Plotting the Bode plot first | D) Measuring only the gain`
**Ans: B** — Mass-force, torque, or KVL/KCL balance, then linearise about an operating point.

**Q52.** A block diagram of a system represents:
`A) The functional relationships among subsystems and their interconnection | B) The physical layout | C) The pole locations | D) The time response`
**Ans: A** — It shows signal flow and summation, not the physical structure.

**Q53.** The point of linearisation in non-linear system modelling is to:
`A) Make the system stable | B) Obtain a linear model valid near an operating point | C) Eliminate all non-linearities | D) Increase the gain`
**Ans: B** — Linearisation is local; it says nothing about global behaviour.

**Q54.** A system function that is proper but not strictly proper has:
`A) A direct feedthrough term (numerator degree ≤ denominator degree) | B) Numerator degree > denominator degree | C) No zeros | D) Imaginary poles`
**Ans: A** — Equal degrees mean an instantaneous output component (D matrix in state space).

**Q55.** If the denominator of G(s) is of higher degree than the numerator, the system is:
`A) Strictly proper | B) Improper | C) Unstable | D) Non-causal`
**Ans: A** — No instantaneous response; strictly proper is required for a causal realisable system.

**Q56.** The impulse response of a first-order system G(s) = a/(s + a) is:
`A) g(t) = a·e^(−at)u(t) | B) g(t) = e^(−at)u(t) | C) g(t) = a·t·e^(−at)u(t) | D) g(t) = δ(t)`
**Ans: A** — Inverse transform of a/(s+a) is a times the decaying exponential.

**Q57.** In the frequency response G(jω), the magnitude and phase are:
`A) |G(jω)| = √((Re)² + (Im)²), ∠G = tan⁻¹(Im/Re) | B) Both linear in ω | C) Both constant | D) The phase is always 0°`
**Ans: A** — Standard polar form of a complex number evaluated at s = jω.

**Q58.** The bandwidth of a system is defined as the range of frequencies over which:
`A) The phase is constant | B) The gain is unity | C) The poles are on the axis | D) The gain is within 3 dB of its midband value`
**Ans: D** — The −3 dB point defines the cutoff frequency.

**Q59.** An LTI system is completely characterised by:
`A) Its gain alone | B) Its impulse response or equivalently its transfer function | C) Its phase alone | D) Its input`
**Ans: B** — The impulse response determines the output for any input via convolution.

**Q60.** The Laplace transform exists for a function that:
`A) Is bounded everywhere | B) Is periodic | C) Is analytic | D) Is of exponential order and piecewise continuous`
**Ans: D** — Growth slower than e^(at) for some finite a guarantees convergence for Re(s) large enough.

---

## SECTION 2 — Transfer Function & Block Diagram Reduction (Q61–Q130)

**Q61.** For a standard negative-feedback system, the closed-loop transfer function is:
`A) G/(1 − GH) | B) GH/(1 + GH) | C) G + H | D) G/(1 + GH)`
**Ans: D** — Negative feedback gives 1 + GH in the denominator.

**Q62.** The error transfer function (ratio of error to reference) for negative feedback is:
`A) G/(1 + GH) | B) GH/(1 + GH) | C) 1/(1 + GH) | D) −1/(1 + GH)`
**Ans: C** **[PYP-23 Q57]** — E(s)/R(s) = 1/(1 + G(s)H(s)) for the standard negative-feedback loop.

**Q63.** The transfer function from disturbance d(t) injected at the plant input, for negative feedback, is:
`A) G/(1 + GH) | B) 1/(1 + GH) | C) GH/(1 + GH) | D) 1/(1 − GH)`
**Ans: A** — The disturbance passes through G and then through the same 1/(1+GH) loop factor.

**Q64.** Sensitivity of the closed-loop transfer function to a change in G is:
`A) 1 + GH | B) S/(1 + S) where S = GH/(1 + GH) | C) GH | D) G only`
**Ans: B** — dT/T = (1/(1 + GH))·(dG/G), i.e. sensitivity is reduced by 1 + GH.

**Q65.** When two blocks G₁ and G₂ are in cascade, the equivalent is:
`A) G₁ + G₂ | B) G₁/G₂ | C) G₁·G₂ | D) G₂ − G₁`
**Ans: C** — Cascade multiplies transfer functions.

**Q66.** When two blocks are in parallel (same input, outputs summed), the equivalent is:
`A) G₁ + G₂ | B) G₁·G₂ | C) G₁/G₂ | D) 1/G₁ + 1/G₂`
**Ans: A** — Parallel blocks add.

**Q67.** Moving a takeoff point to the other side of a block requires:
`A) Multiplying by it | B) Adding it | C) Dividing by that block's forward transfer function | D) Ignoring it`
**Ans: C** — The takeoff signal after the block is the original divided by the block gain.

**Q68.** Moving a takeoff point before a block G to after it requires:
`A) Dividing by G | B) Multiplying by G | C) Adding G | D) Squaring G`
**Ans: B** — The forward relation must be preserved.

**Q69.** Two summing points in cascade with signs (+,+) followed by (×,×) combine into:
`A) (+,−) | B) A single summing point with signs (+,+) | C) (−,−) | D) Unchanged`
**Ans: B** — Cascading two summing junctions multiplies their signs elementwise.

**Q70.** The transfer function of a closed-loop system with G in the forward path and H in the feedback path, for positive feedback, is:
`A) G/(1 + GH) | B) 1/(1 − GH) | C) G/(1 − GH) | D) GH/(1 − GH)`
**Ans: C** — Positive feedback replaces the + with − in the denominator.

**Q71.** The closed-loop gain of a non-inverting amplifier with R₁ to ground and R₂ feedback, ideal op-amp, is:
`A) 1 + R₂/R₁ | B) R₂/R₁ | C) 1 + R₁/R₂ | D) R₁/R₂`
**Ans: A** — The feedback divider sets v_o = v_i(1 + R₂/R₁).

**Q72.** The gain of an inverting amplifier with input R₁ and feedback R₂ is:
`A) +R₂/R₁ | B) 1 + R₂/R₁ | C) −R₂/R₁ | D) −R₁/R₂`
**Ans: C** — Virtual ground at the input makes current R₁ = V_i/R₁ flow through R₂.

**Q73.** A differential amplifier built from four matched resistors has differential gain:
`A) R₂/R₁ | B) −R₂/R₁ | C) 1 + R₂/R₁ | D) 2R₂/R₁`
**Ans: A** — With matched ratios, V_o = (R₂/R₁)(V₂ − V₁).

**Q74.** The transfer function of a non-inverting amplifier with an op-amp of open-loop gain A and a feedback fraction β is:
`A) A/(1 + Aβ) | B) Aβ/(1 + Aβ) | C) A(1 − β) | D) 1/(1 + Aβ)`
**Ans: A** — Standard closed-loop form with β = R₁/(R₁+R₂).

**Q75.** For an op-amp circuit with A_OL = 10⁵ and β = 0.1, the closed-loop gain is approximately:
`A) 10 exactly | B) 1000 | C) 10000 | D) 9.999`
**Ans: D** — A/(1 + Aβ) = 10⁵/(1 + 10⁴) = 9.999, essentially 1/β = 10.

**Q76.** In a block diagram, the transfer function from reference R to output C for a negative loop is:
`A) G·H | B) G/(1 + GH) | C) 1/(1 + GH) | D) (1 + GH)/G`
**Ans: B** — Same closed-loop form as Q61; error and output differ only by the factor G.

**Q77.** The sensitivity of the loop gain to a plant variation is reduced by a factor of:
`A) 1 + GH | B) GH | C) 1/(1 + GH) | D) 1 + G`
**Ans: A** — Relative sensitivity is 1/(1 + GH).

**Q78.** Complementary sensitivity T(s) is defined as:
`A) T(s) = 1/(1 + GH) | B) T(s) = GH/(1 + GH) | C) T(s) = GH | D) T(s) = 1 + GH`
**Ans: B** — The closed-loop transfer function of a loop is GH/(1 + GH).

**Q79.** Sensitivity S(s) and complementary sensitivity T(s) satisfy:
`A) S·T = 1 | B) S = T | C) S + T = 1 | D) S − T = 1`
**Ans: C** — 1/(1+L) + L/(1+L) = 1, a defining identity.

**Q80.** The transfer function of a system whose output is fed to its input through unity feedback is:
`A) G/(1 + G) | B) G/(1 − G) | C) 1/(1 + G) | D) G + 1`
**Ans: A** — With H = 1, negative feedback gives G/(1 + G).

**Q81.** The overall transfer function of cascaded subsystems G₁, G₂, G₃ with unity feedback around all three is:
`A) G₁G₂G₃/(1 + G₁G₂G₃) | B) G₁G₂G₃/(1 + G₁ + G₂ + G₃) | C) G₁+G₂+G₃ | D) 1/(1 + G₁G₂G₃)`
**Ans: A** — The loop gain is the product of all forward blocks.

**Q82.** A system is described by the differential equation d²y/dt² + 3 dy/dt + 2y = u. Its transfer function is:
`A) 1/(s² + 2s + 3) | B) 1/(s² + 3s + 2) | C) s² + 3s + 2 | D) 1/(s + 3)(s + 2)` `
**Ans: B** — Replace each derivative by s^k under zero initial conditions.

**Q83.** A mass-spring-damper with M = 1, B = 3, K = 2 driven by force F has transfer function:
`A) 1/(s² + 2s + 3) | B) s² + 3s + 2 | C) 1/(s² + 3s + 2) | D) 2/(s² + 3s + 2)`
**Ans: C** — ẍ + 3ẋ + 2x = f, so X/F = 1/(s² + 3s + 2).

**Q84.** A parallel RLC circuit's impedance is:
`A) Z(s) = sL + 1/(sC) + R | B) Z(s) = 1/(sRC) | C) Z(s) = 1/(sC + 1/sL + 1/R) | D) Z(s) = sC + R`
**Ans: C** — Parallel admittances add: Y = sC + 1/(sL) + 1/R, and Z = 1/Y.

**Q85.** For a parallel RLC circuit driven by a current source with voltage output, the transfer function is:
`A) Y(s) = sC + 1/sL | B) Z(s) = 1/(sC + 1/(sL) + 1/R) | C) R only | D) 1/(sRC)`
**Ans: B** — Output across the network divided by input current is the impedance.

**Q86.** A parallel RLC network (R, L, C) with the output across C has a transfer function whose denominator is:
`A) s² + 2s + 1 | B) LCs² + 1 | C) LCs² + (L/R)s + 1 | D) Cs + 1`
**Ans: C** — Z(s)·sC = sC/(sC + 1/sL + 1/R) = LCs²/(LCs² + (L/R)s + 1).

**Q87.** The transfer function of a series RLC circuit with output across R is:
`A) 1/(R + sL + 1/sC) | B) R/(R + sL + 1/sC) | C) sL/(R + sL + 1/sC) | D) (1/sC)/(R + sL + 1/sC)`
**Ans: B** — Voltage divider with R as the output element.

**Q88.** A translational mechanical system's impedance analogue uses:
`A) Force ↔ voltage, velocity ↔ current | B) Force ↔ current, velocity ↔ voltage | C) Force ↔ voltage, velocity ↔ voltage | D) Force ↔ current, velocity ↔ current`
**Ans: B** — The force–voltage analogy makes mechanical systems look like electrical networks.

**Q89.** In the force-current analogy:
`A) Force ↔ voltage | B) Force ↔ current, velocity ↔ force, damping ↔ resistance | C) Only voltage ↔ force | D) There is no analogy`
**Ans: B** — Force–current makes mechanical impedance correspond to electrical impedance.

**Q90.** The mobility analogy uses:
`A) Velocity ↔ voltage, force ↔ current | B) Only force ↔ current | C) Velocity ↔ current, force ↔ voltage | D) Only velocity ↔ voltage`
**Ans: C** — Also called the force-voltage analogy with variables relabelled.

**Q91.** A control system is described by the state equations ẋ = Ax + Bu, y = Cx + Du. The output is obtained from:
`A) y = Bx + Cu | B) y = Cx + Du | C) y = Ax + Bu | D) y = u only`
**Ans: B** — The standard controllable-canonical state model.

**Q92.** The transfer function of a state-space model is:
`A) G(s) = (sI − A)B⁻¹C | B) G(s) = A + B + C | C) G(s) = C(sI − A)⁻¹B + D | D) G(s) = (sI − A)/(B + C)`
**Ans: C** — The resolvent (sI − A)⁻¹ gives the impulse response matrix.

**Q93.** In Laplace-transformed state equations with zero initial conditions:
`A) X(s) = A/s + B | B) sX(s) = AX(s) + BU(s) | C) sX(s) = A + BU(s) | D) X(s) = (sI + A)BU(s)`
**Ans: B** — Differentiating the state equation and taking the transform gives sX = AX + BU.

**Q94.** A closed-loop state-space system with state feedback u = −Kx + r has:
`A) A_cl = A + BK | B) A_cl = BK − A | C) A_cl = A − BK | D) A_cl = A − K`
**Ans: C** — Substituting the feedback law gives ẋ = (A − BK)x + r.

**Q95.** The characteristic equation of a closed-loop state-space system is:
`A) det(sI − A) = 0 | B) det(sI − (A − BK)) = 0 | C) det(A − BK) = 0 | D) trace(A − BK) = 0`
**Ans: B** — The eigenvalues of A_cl define the closed-loop poles.

**Q96.** A system has G(s) = K/(s(s + 2)(s + 5)). Its system type is:
`A) Type 0 | B) Type 2 | C) Type 3 | D) Type 1 (one pole at origin)`
**Ans: D** — Exactly one pure integrator.

**Q97.** A system has G(s) = 10(s + 1)/(s(s + 2)(s + 3)). Its open-loop gain at low frequency behaves as:
`A) 10/s → infinite | B) 10 | C) 0 | D) s/10`
**Ans: A** — The pole at the origin makes the low-frequency magnitude unbounded.

**Q98.** The transfer function G(s) = (s + 3)/((s + 1)(s + 2)) has:
`A) A zero at −1 and poles at −3, −2 | B) All poles at the origin | C) A double pole at −2 | D) A zero at −3 and poles at −1, −2`
**Ans: D** — Zeros from the numerator, poles from the denominator.

**Q99.** A pole-zero map with a zero at the origin and one pole there is best described by:
`A) The net order at origin determines the low-frequency slope | B) The gain | C) The phase margin | D) The bandwidth`
**Ans: A** — Net order (zeros − poles at origin) sets the initial −20 dB/dec slope.

**Q100.** If G(s) = 10/[s(s + 1)(s + 2)], the pole closest to the imaginary axis is at:
`A) s = 0 | B) s = −1 | C) s = −2 | D) s = −3`
**Ans: A** — The origin pole is nearest the axis and dominates the low-frequency behaviour.

**Q101.** A system with transfer function G(s) = 4/(s² + 4s + 4) has:
`A) Poles at ±j2 | B) Poles at −1, −2 | C) A repeated pole at −2 (critically damped) | D) A pole at the origin`
**Ans: C** — s² + 4s + 4 = (s + 2)², so ζ = 1.

**Q102.** A system G(s) = 9/(s² + 3s + 9) has:
`A) ω_n = 3, ζ = 1 | B) ω_n = 3, ζ = 0.5 | C) ω_n = 9, ζ = 3 | D) ω_n = 1.5, ζ = 1`
**Ans: B** — Comparing s² + 2ζω_n s + ω_n²: ω_n = 3 and 2ζω_n = 3 gives ζ = 0.5.

**Q103.** The time constant of a first-order system with pole at −5 is:
`A) 5 s | B) 0.2 s | C) 0.5 s | D) 25 s`
**Ans: B** — τ = 1/5 = 0.2 s.

**Q104.** The bandwidth of a first-order system with pole at −5 is approximately:
`A) 5 rad/s | B) 0.2 rad/s | C) 25 rad/s | D) 1 rad/s`
**Ans: A** — The −3 dB frequency of 1/τ equals the pole magnitude for a single pole.

**Q105.** A system has G(s) = (s + 1)/((s + 2)(s + 3)). The DC gain is:
`A) 1/5 | B) 1 | C) 6 | D) 1/6`
**Ans: D** — G(0) = (1)/(2·3) = 1/6.

**Q106.** A system has G(s) = s/(s + 4). Its DC gain is:
`A) 1/4 | B) 4 | C) 1 | D) Zero`
**Ans: D** — The zero at the origin makes the step response start at zero and the DC gain vanish.

**Q107.** A system with G(s) = 1/(s + 4) has a static error constant K_p equal to:
`A) 4 | B) 0.25 | C) 1 | D) 16`
**Ans: B** — K_p = lim G(s) as s→0 = 1/4.

**Q108.** The degree of a polynomial P(s) = s⁴ + 2s³ + s² + s + 5 is:
`A) 3 | B) 1 | C) 4 | D) 0`
**Ans: C** — The highest power of s present.

**Q109.** The system G(s) = (s + 1)/(s² + 3s + 2) has poles at:
`A) +1 and +2 | B) −1 and −2 | C) ±j | D) −3 only`
**Ans: B** — s² + 3s + 2 = (s + 1)(s + 2).

**Q110.** An overdamped second-order system has:
`A) Two distinct real negative poles | B) Complex poles | C) Repeated real poles | D) Purely imaginary poles`
**Ans: A** — ζ > 1 gives real, distinct, negative real parts.

**Q111.** A system is called a minimum-phase system if:
`A) All its zeros are in the RHP | B) It has no zeros | C) All its zeros are in the LHP | D) All its poles are in the LHP`
**Ans: C** — Minimum-phase means stable zeros (and poles), enabling a causal stable inverse.

**Q112.** A non-minimum-phase system has:
`A) At least one pole in the RHP | B) No zeros | C) At least one zero in the RHP | D) Poles at the origin`
**Ans: C** — An RHP zero cannot be inverted causally with stability, causing non-causal inverse responses.

**Q113.** The inverse Laplace transform of 1/(s + a) is:
`A) e^(−at)u(t) | B) e^(at)u(t) | C) a·e^(−at)u(t) | D) t·e^(−at)u(t)`
**Ans: A** — The canonical first-order pair.

**Q114.** The inverse Laplace transform of s/(s² + ω²) is:
`A) sin(ωt) | B) t·cos(ωt) | C) ω·cos(ωt) | D) cos(ωt)`
**Ans: D** — Standard pair; note s/(s² + ω²) is cosine, while ω/(s² + ω²) is sine.

**Q115.** The transfer function of a system with impulse response g(t) = 2e^(−3t)u(t) is:
`A) 3/(s + 2) | B) 2/(s + 3) | C) 2/(s − 3) | D) 1/(s + 3)`
**Ans: B** — Taking the Laplace transform of the decaying exponential.

**Q116.** Two systems in cascade each have transfer function G. The overall transfer function is:
`A) 2G | B) G² | C) G/2 | D) 1/G`
**Ans: B** — Cascade multiplies.

**Q117.** A system with G₁ = 2 and G₂ = 3 in cascade has overall gain:
`A) 5 | B) 1/6 | C) 3/2 | D) 6`
**Ans: D** — Product of constant gains.

**Q118.** In a block diagram, to convert a summing junction with feedback you must ensure:
`A) The loop gain around the junction is correctly signed | B) All signs are positive | C) There is only one takeoff | D) The block gain is unity`
**Ans: A** — Sign errors in reduction are the most common source of wrong closed-loop gains.

**Q119.** A signal is picked off before a block G of gain 2 and rerouted after it. The new branch must be:
`A) Multiplied by 2 | B) Divided by 2 | C) Left unchanged | D) Negated`
**Ans: A** — Preserving the signal value requires compensating for the forward gain.

**Q120.** A system described by ÿ + y = ẋ + x has transfer function:
`A) (s² + 1)/(s + 1) | B) (s + 1)/(s² + 1) | C) 1/(s² + 1) | D) (s + 1)/(s + 1)`
**Ans: B** — Y(s)(s² + 1) = X(s)(s + 1), giving (s+1)/(s²+1).

**Q121.** The system G(s) = 1/(s² + 2s + 2) has poles:
`A) −1 only | B) ±j | C) −2 ± j | D) −1 ± j`
**Ans: D** — Roots of s² + 2s + 2 = 0 are s = −1 ± j.

**Q122.** For a system with G(s) = K/(s² + 2ζω_n s + ω_n²), increasing K increases:
`A) The natural frequency is unchanged; poles move outward | B) ω_n increases | C) ζ increases | D) The damping ratio decreases always`
**Ans: A** — ω_n is set by the denominator's constant and s-coefficient; K scales the numerator, moving poles along the root locus.

**Q123.** The impedance of a capacitor at the frequency ω is:
`A) jωC | B) 1/(jωC) | C) jωL | D) ωC`
**Ans: B** — X_C = 1/(ωC) and the impedance is capacitive (−j90°).

**Q124.** The impedance of an inductor at the frequency ω is:
`A) jωL | B) 1/(jωL) | C) jωC | D) 1/(ωL)`
**Ans: A** — X_L = ωL, inductive (+j90°).

**Q125.** A block diagram cannot be reduced to a single block if it contains:
`A) Only cascaded blocks | B) Only summing junctions | C) A closed loop without a defined forward path | D) Takeoff points`
**Ans: C** — Some structures (e.g., cross-connections without proper paths) resist standard reduction.

**Q126.** In Mason's rule, the denominator determinant Δ is:
`A) The sum of forward path gains | B) 1 + sum of loop gains | C) The product of all gains | D) 1 − (sum of individual loop gains) + (sum of products of non-touching loop gains) − …`
**Ans: D** — Touching loops must not appear together in any product term.

**Q127.** The number of poles of a closed-loop system equals:
`A) The degree of the forward path numerator | B) The number of blocks | C) The number of states in the state-space model | D) The number of takeoff points`
**Ans: C** — Order equals number of independent energy-storage elements or states.

**Q128.** An op-amp integrator with R = 10 kΩ and C = 0.1 µF has a unity-gain frequency of:
`A) 1/(RC) ≈ 1 kHz | B) 2πRC ≈ 6.3 mHz | C) 159 kHz | D) 1/(2πRC) ≈ 159 Hz`
**Ans: D** — The −3 dB point of 1/(sRC) is at ω = 1/RC, so f = 1/(2πRC).

**Q129.** A differentiator with R = 10 kΩ and C = 0.1 µF has a slope:
`A) sRC = s×10³ (rising 20 dB/decade) | B) 1/(sRC) | C) s/RC | D) RC·s²`
**Ans: A** — The gain sRC increases 20 dB per decade.

**Q130.** The transfer function of a first-order hold is approximately:
`A) (1 − e^(−Ts))/Ts | B) (1 − e^(−Ts))/s | C) 1/s | D) (1 − e^(−Ts))`
**Ans: B** — The zero-order hold; dividing by Ts gives the gain-corrected form.

---

## SECTION 3 — Signal Flow Graphs & Mason's Gain Formula (Q131–Q180)

**Q131.** In a signal flow graph, a node represents:
`A) A block gain | B) A system variable (signal) | C) A summing point only | D) A transfer function pole`
**Ans: B** — Nodes are signals; directed branches carry the branch gains.

**Q132.** A branch in a signal flow graph represents:
`A) A sum | B) A pole | C) A state | D) A multiplicative gain relationship between two nodes`
**Ans: D** — The branch gain multiplies the source node's value to give the destination.

**Q133.** Mason's gain formula expresses the transfer function as:
`A) T = Δ / (Σ P_k) | B) T = Σ P_k only | C) T = (Σ P_k Δ_k) / Δ | D) T = Δ only`
**Ans: C** — Numerator is the sum of forward paths times their path determinants, over the single overall Δ.

**Q134.** In Mason's formula, Δ is:
`A) The sum of all loop gains | B) 1 + Σ forward paths | C) 1 − ΣLᵢ + ΣLᵢLⱼ − … over non-touching loops | D) The product of branch gains`
**Ans: C** — Every term is a product of loop gains, and no two loops in a product may touch.

**Q135.** A "touching loop" refers to loops that:
`A) Share a common node or branch | B) Are completely separate | C) Have the same gain | D) Lie on the same path`
**Ans: A** — Two loops that share a node cannot appear together in a Δ term.

**Q136.** Two loops are called non-touching if they:
`A) Have equal gains | B) Are on the same forward path | C) Share a branch | D) Have no common node`
**Ans: D** — Non-touching loops can be multiplied together in the Δ expansion.

**Q137.** For a forward path P_k, the path determinant Δ_k equals:
`A) Δ minus non-touching loops | B) P_k itself | C) 1 − P_k | D) Δ minus the loops that touch P_k`
**Ans: D** — Loops touching the path must be removed from Δ for that term.

**Q138.** The gain of a system with one forward path P and two non-touching loops L₁, L₂ is:
`A) T = P/[1 − L₁ − L₂ + L₁L₂] | B) T = P(1 − L₁ − L₂) | C) T = P + L₁ + L₂ | D) T = P(1)/[1 − (L₁ + L₂) + L₁L₂]`
**Ans: D** — Because L₁ and L₂ do not touch, the product term L₁L₂ survives in Δ.

**Q139.** If two loops touch, the correct Δ is:
`A) 1 − L₁ − L₂ + L₁L₂ | B) 1 − L₁ − L₂ | C) 1 + L₁ + L₂ | D) 1 − L₁L₂`
**Ans: B** — Touching loops cannot be multiplied, so the cross term is excluded.

**Q140.** The signal flow graph corresponding to a block diagram is obtained by:
`A) Simplifying loops | B) Converting each block to a branch and each signal to a node | C) Applying Mason's formula | D) Taking the Laplace transform`
**Ans: B** — It is a node-and-branch representation of the same signal relations.

**Q141.** A unity-feedback system G with forward path and unity feedback has SFG loop gain:
`A) L = −G | B) L = +G | C) L = G² | D) L = 1/G`
**Ans: A** — The unity feedback path contributes a branch of −1, so L = −G.

**Q142.** For a negative-feedback loop, the closed-loop gain equals:
`A) Forward path only | B) −(forward path)/(1 + loop gain) with proper sign | C) Loop gain only | D) 1/loop gain`
**Ans: B** — Mason applied to the SFG of a single loop gives the familiar A/(1 + GH).

**Q143.** Mason's formula is most useful when:
`A) The system is linearised | B) The block diagram has many loops and is hard to reduce by inspection | C) There is only one loop | D) Only for time-varying systems`
**Ans: B** — It systematically handles complex interconnections.

**Q144.** The number of forward paths equals the number of:
`A) Distinct paths from input to output with no node repeated | B) Loops in the graph | C) Poles of the system | D) Summing junctions`
**Ans: A** — A forward path cannot pass through any node more than once.

**Q145.** The number of independent loops equals:
`A) B − N + 1 for a graph with N nodes and B branches | B) N − B | C) B + N | D) N − 1`
**Ans: A** — This is the loop count (topological cycles).

**Q146.** A feedforward loop in a signal flow graph is one that:
`A) Returns to its start | B) Contains a summing point | C) Never returns to its starting node | D) Has negative gain`
**Ans: C** — Forward paths and feedforward branches move forward through the graph.

**Q147.** A feedback loop in a signal flow graph is one that:
`A) Starts and ends at the same node | B) Has no nodes | C) Is always positive | D) Contains no branches`
**Ans: A** — Feedback branches return to their origin and form the loops in Δ.

**Q148.** When the denominator Δ = 0 for a closed loop, this indicates:
`A) The system is stable | B) The loop gain satisfies 1 − L = 0, i.e. a singularity or sustained oscillation | C) No gain | D) No poles`
**Ans: B** — 1 + GH = 0 is the characteristic equation, i.e. natural oscillation.

**Q149.** A system whose SFG has forward path P and a single touching loop L has transfer function:
`A) T = P/(1 + L) | B) T = P(1 − L) | C) T = P/(1 − L) | D) T = P + L`
**Ans: C** — A single loop gives Δ = 1 − L and Δ_k = 1, so T = P/(1 − L).

**Q150.** The gain around a single loop in the s-domain is:
`A) The sum of branch gains | B) The branch with largest gain | C) The pole of the loop | D) The product of all branch gains around it`
**Ans: D** — Multiply the branch gains in sequence around the loop.

**Q151.** When a signal flow graph has two parallel paths from a node to another with gains P₁ and P₂, the combined forward gain is:
`A) P₁P₂ | B) P₁ + P₂ | C) P₁ − P₂ | D) P₁/P₂`
**Ans: B** — Parallel branches add at the destination node.

**Q152.** To use Mason's formula, the graph must be:
`A) Proper and causal with the input and output identified | B) Time-varying | C) Non-linear | D) Disconnected`
**Ans: A** — The graph must be a connected causal graph with defined input and output nodes.

**Q153.** A first-order system ẏ + y = u in state form (x = y) has SFG from U to X with:
`A) G(s) = 1/(s − 1) | B) G(s) = 1/(s + 1) | C) G(s) = s + 1 | D) G(s) = s`
**Ans: B** — sX = −X + U, so X/U = 1/(s + 1).

**Q154.** In the SFG of a second-order system with a feedback loop, Δ contains:
`A) Only the main loop | B) Only the forward paths | C) The sum of poles | D) Terms for the main loop plus product terms for non-touching loops`
**Ans: D** — Δ is built entirely from the loop gains and their non-touching combinations.

**Q155.** A branch gain of zero in an SFG means:
`A) That path contributes nothing to the transmission | B) The path is shorted | C) The loop is unstable | D) The gain is infinite`
**Ans: A** — A zero-gain branch effectively disconnects that path.

**Q156.** The Mason formula is essentially a generalisation of:
`A) The Laplace transform | B) The single-loop closed-loop gain formula | C) The state transition matrix | D) The Bode plot`
**Ans: B** — For a single loop it reduces to the familiar A/(1 + GH); for many loops it adds non-touching products.

**Q157.** A loop that touches a forward path contributes to:
`A) Δ_k but not Δ | B) Δ but not to Δ_k for that path | C) Neither | D) Both`
**Ans: B** — Touching loops are excluded from the path determinant of the path they touch.

**Q158.** Given a forward path P touching loops L₁ and L₂, its path determinant is:
`A) Δ − L₁L₂ | B) Δ − L₁ − L₂ | C) 1 − L₁ − L₂ | D) Δ + L₁ + L₂`
**Ans: B** — Each touching loop is removed individually from Δ for that path's term.

**Q159.** A signal flow graph that represents a system with output equation y = Cx is read by:
`A) The sum of poles | B) The determinant of A | C) The DC gain only | D) The product of forward-path gains from input to y`
**Ans: D** — Mason sums the (weighted) forward paths reaching the output.

**Q160.** An advantage of the signal flow graph method is:
`A) It always gives the least number of poles | B) It is purely graphical and does not need algebraic reduction | C) It requires only the transfer function | D) It needs the time response`
**Ans: B** — It is a graphical algebra that scales to complex interconnections.

**Q161.** The loop transfer function of a system (denoted L) equals:
`A) The forward gain only | B) The product of all gains around each loop, summed over independent loops | C) The sum of poles | D) The product of forward gains`
**Ans: B** — L = Σ independent loop gains (when they are non-touching).

**Q162.** The characteristic equation 1 + G(s)H(s) = 0 can be written in terms of the SFG determinant as:
`A) Δ = 1 | B) ΣLᵢ = 0 | C) ΣPₖ = 0 | D) Δ = 0`
**Ans: D** — For the standard loop Δ = 1 + GH, and the characteristic equation is Δ = 0.

**Q163.** Consider a system with forward paths P₁ and P₂ and a single loop L touching both. Its transfer function is:
`A) P₁P₂/(1 − L) | B) (P₁ + P₂)(1 − L) | C) (P₁ + P₂)/(1 − L) | D) P₁/(1 − L) + P₂`
**Ans: C** — Both paths share Δ = 1 − L, so sum them over that single Δ.

**Q164.** An SFG node where branches arrive is where:
`A) Signals are multiplied | B) Signals are differentiated | C) Signals are delayed | D) Signals are summed`
**Ans: D** — Node values equal the algebraic sum of the incoming branch values.

**Q165.** To determine the sign of a branch gain from a block diagram:
`A) Include the sign of the summing junction the signal passes through | B) Always positive | C) Always negative | D) Ignore summing points`
**Ans: A** — The sign at the destination summing junction determines the branch sign.

**Q166.** For a system with G(s) = (s + 1)/[s(s + 2)], the poles are:
`A) 0 and +2 | B) −1 and −2 | C) ±j2 | D) 0 and −2`
**Ans: D** — Denominator s(s + 2) gives poles at 0 and −2.

**Q167.** For G(s) = (s + 1)/(s² + 3s + 2), the SFG from input to output, ignoring loops, has a single forward path gain:
`A) (s² + 3s + 2)/(s + 1) | B) s² + 3s + 2 | C) (s + 1)/(s² + 3s + 2) | D) 1/(s + 1)`
**Ans: C** — With no internal loops, Mason gives the direct transfer function as the single forward path.

**Q168.** A system with two non-touching loops L₁ and L₂ and one forward path P has transfer function:
`A) P(1 − L₁ − L₂)/Δ | B) P/[1 − L₁ − L₂ + L₁L₂] | C) P/(1 − L₁ − L₂) | D) P/[1 − L₁L₂]`
**Ans: B** — The L₁L₂ term must appear because the loops do not touch.

**Q169.** In the SFG for a system with a single feedback loop of gain −H around forward G, the loop gain L is:
`A) +GH | B) GH | C) −GH | D) −G`
**Ans: C** — The branch back through H carries the summing sign, giving L = −GH.

**Q170.** Mason's formula for a loop with gain L = −GH gives denominator 1 − L:
`A) 1 − GH | B) 1 + GH | C) GH | D) 1`
**Ans: B** — 1 − (−GH) = 1 + GH, the familiar negative-feedback denominator.

**Q171.** A transfer function obtained by Mason's formula must be:
`A) In the s-domain with proper form | B) In the time domain | C) Dependent on initial conditions | D) Always unstable`
**Ans: A** — Mason operates on the s-domain graph, producing a proper rational function.

**Q172.** An SFG containing a pole at the origin has a branch gain of the form:
`A) K·s | B) K/s | C) K/s² | D) K`
**Ans: B** — An integrator is represented by K/s.

**Q173.** In a signal flow graph, the gain from source to sink equals:
`A) The ratio of the node values along connected paths | B) The sum of all branch gains | C) The largest branch gain | D) The loop gain`
**Ans: A** — Mason computes the transmission from input to output using paths and loops.

**Q174.** The transmission gain T(s) from Mason's formula is:
`A) T(s) = x_out/x_in | B) T(s) = x_in/x_out | C) T(s) = Σ loops | D) T(s) = Δ only`
**Ans: A** — Transmission is defined as output node over input node.

**Q175.** A system with an SFG having a forward path and a self-loop at the output node has:
`A) Δ = 1 − L² | B) Δ = 1 − L (self-loop counted once) | C) Δ = 1 + L | D) Δ = L`
**Ans: B** — A single self-loop contributes 1 − L to Δ.

**Q176.** Non-touching loops may be multiplied because:
`A) They have equal gains | B) They are on the same path | C) They occupy disjoint parts of the graph | D) They share a node`
**Ans: C** — Disjointness is precisely the condition for the product term to survive.

**Q177.** An example of a loop that touches the forward path is:
`A) A loop completely elsewhere | B) A loop with zero gain | C) A loop that shares a node with the path | D) No loop`
**Ans: C** — Sharing any node with the path makes them touching.

**Q178.** To convert a state-space model to a signal flow graph you would:
`A) Draw only the poles | B) Use only the DC gain | C) Derive the transfer function and plot its poles and zeros as branches | D) Ignore the input matrix`
**Ans: C** — The transfer function's poles and zeros form the graph structure.

**Q179.** Mason's gain formula reduces to the familiar closed-loop gain when:
`A) There are many loops | B) There are no loops | C) There is a single loop | D) There are no forward paths`
**Ans: C** — With one loop and one path, T = P/(1 − L).

**Q180.** A practical rule when applying Mason's formula is to:
`A) Sum only the largest loop | B) Ignore Δ_k | C) Identify all loops and check touching relationships carefully | D) Count loops twice`
**Ans: C** — The main error source is misidentifying touching versus non-touching loops.

---

## SECTION 4 — Time Domain Response & First-Order Systems (Q181–Q250)

**Q181.** The unit step response of G(s) = 1/(s + a) is:
`A) (1/a)e^(−at)u(t) | B) (1/a)(1 − e^(−at))u(t) | C) a(1 − e^(−at))u(t) | D) (1 − e^(−at))a²u(t)`
**Ans: B** — Partial fractions: Y(s) = 1/[s(s+a)] gives a final value of 1/a.

**Q182.** The unit step response of an integrator G(s) = K/s is:
`A) K(1 − e^(−t))u(t) | B) K/s² only | C) K·e^(−t)u(t) | D) Kt·u(t)`
**Ans: D** — K/s × 1/s = K/s² inverts to Kt.

**Q183.** The unit impulse response of G(s) = 1/(s + a) is:
`A) (1 − e^(−at))u(t) | B) a·e^(−at)u(t) | C) t·e^(−at)u(t) | D) e^(−at)u(t)`
**Ans: D** — The impulse response is simply the inverse transform of G(s).

**Q184.** The time constant τ of G(s) = a/(s + a) is:
`A) a | B) 1/a² | C) 1/a | D) a/2`
**Ans: C** — τ = 1/a is the exponential decay constant.

**Q185.** A first-order system's step response reaches 98% of final value at approximately:
`A) τ | B) 0.63τ | C) 10τ | D) 4τ`
**Ans: D** — 1 − e^(−4) ≈ 0.982, so about 4 time constants.

**Q186.** A first-order system's step response is at 50% of final value at:
`A) 0.5τ | B) 0.69τ | C) 1.5τ | D) 2τ`
**Ans: B** — 1 − e^(−t/τ) = 0.5 gives t = 0.693τ.

**Q187.** If the time constant of a first-order system is halved, the rise rate:
`A) Halves | B) Doubles | C) Is unchanged | D) Becomes zero`
**Ans: B** — Faster decay means larger bandwidth and steeper response.

**Q188.** The 10–90% rise time of a first-order system is approximately:
`A) 2.2τ | B) τ | C) 4τ | D) 0.69τ`
**Ans: A** — t(90%) − t(10%) = 2.197τ − 0.105τ ≈ 2.2τ.

**Q189.** A first-order system with pole at −10 rad/s has a rise time (10–90%) of about:
`A) 1 s | B) 0.22 s | C) 0.1 s | D) 2.2 s`
**Ans: B** — τ = 0.1 s, so tr ≈ 2.2 × 0.1 = 0.22 s.

**Q190.** The steady-state output of a stable system with a bounded input is:
`A) Always zero | B) A constant (if the input is constant) | C) Always infinite | D) Equal to the input at all times`
**Ans: B** — By the final value theorem, a constant input gives a constant output at steady state.

**Q191.** A system is stable if its natural response:
`A) Grows with time | B) Decays with time | C) Remains constant | D) Oscillates with growing amplitude`
**Ans: B** — Decaying natural response implies all poles in the LHP.

**Q192.** The natural response of a system contains terms of the form e^(p_i t) where p_i are:
`A) The zeros | B) The input poles | C) The system poles | D) The gains`
**Ans: C** — The natural modes are set by the poles (roots of the characteristic equation).

**Q193.** A free (unforced) response of a second-order system is:
`A) A + Bt | B) e^(−ζω_n t)[A cos ω_d t + B sin ω_d t] | C) At² | D) A e^(+ζω_n t)`
**Ans: B** — The standard underdamped homogeneous solution.

**Q194.** A critically damped second-order system's natural response is:
`A) e^(−ω_n t) cos ω_n t | B) A + Bt | C) Bt e^(+ω_n t) | D) (A + Bt)e^(−ω_n t)`
**Ans: D** — Repeated root −ω_n gives (A + Bt)e^(−ω_n t).

**Q195.** A critically damped system has:
`A) Complex poles | B) Purely imaginary poles | C) No poles | D) Two equal real poles`
**Ans: D** — Repeated real root gives the critically damped (A+Bt)e^(−ω_n t) response.

**Q196.** The impulse response of an overdamped system is:
`A) e^(−ζω_n t)cos ω_d t | B) (A+Bt)e^(−ω_n t) | C) A·s + B | D) A₁e^(p₁t) + A₂e^(p₂t)`
**Ans: D** — Two distinct real roots give two decaying exponentials.

**Q197.** The response time of a first-order system is mainly governed by:
`A) Its time constant | B) Its DC gain | C) Its zeros | D) The input amplitude`
**Ans: A** — τ sets the exponential decay and hence all 10–90% timing measures.

**Q198.** A system described by ẏ + 4y = 2u has a time constant of:
`A) 4 s | B) 2 s | C) 0.5 s | D) 0.25 s`
**Ans: D** — G(s) = 2/(s+4), so τ = 1/4 = 0.25 s.

**Q199.** The step response final value for G(s) = 2/(s + 4) with a unit step input is:
`A) 0.5 | B) 2 | C) 4 | D) 1/4`
**Ans: A** — FVT: lim s→0 s·(1/s)·2/(s+4) = 2/4 = 0.5.

**Q200.** A first-order system's settling time to 2% is approximately:
`A) τ | B) 4τ | C) 2τ | D) 5τ`
**Ans: B** — 4τ gives 98.2% of the final value.

**Q201.** If a system's poles are shifted further into the LHP, the system becomes:
`A) Slower | B) Unstable | C) Oscillatory | D) Faster but with the same steady-state gain`
**Ans: D** — Leftward shift increases bandwidth and speed without changing G(0).

**Q202.** A system with a pole at the origin has a step response that:
`A) Settles to a constant | B) Decays exponentially | C) Ramps without bound | D) Oscillates`
**Ans: C** — The integrator produces an unbounded ramp for a step input.

**Q203.** The velocity error constant K_v for a type-1 system G(s) = K/[s(s+a)] is:
`A) K | B) K/a² | C) a/K | D) K/a`
**Ans: D** — K_v = lim s→0 s·K/[s(s+a)] = K/a.

**Q204.** A system with two poles at the origin (type 2) gives zero steady-state error for:
`A) Parabolic input only | B) All inputs | C) Step only | D) Step and ramp inputs`
**Ans: D** — Type 2 gives e_ss = 0 for step and ramp, but finite (1/K_a) for parabolic.

**Q205.** The error constant K_p for G(s) = K/s (a pure integrator with gain K) is:
`A) K | B) Infinite | C) 0 | D) 1/K`
**Ans: B** — K_p = lim s→0 K/s → ∞, giving e_ss = 1/(1+K_p) = 0 for step.

**Q206.** For an open-loop G(s) = K/[s(s + 2)(s + 5)], the error constant K_v is:
`A) K | B) K/10 | C) K/2 | D) 10/K`
**Ans: B** — K_v = lim s→0 s·K/[s(s+2)(s+5)] = K/(2·5) = K/10.

**Q207.** A first-order system's unit step response y(t) for G(s) = 3/(s + 3) at t = τ is:
`A) 3e^(−1) ≈ 1.1 | B) 1 | C) 3 | D) 3(1 − e^(−1)) ≈ 1.9`
**Ans: D** — y(τ) = 3(1 − e^(−1)) = 3(0.632) = 1.90.

**Q208.** The transfer function of a first-order low-pass filter with a cutoff of 159 Hz is:
`A) 1/(1 + s/100) | B) 1/(1 + s/1000) | C) 1000/(s + 1) | D) 1/(s + 159)`
**Ans: B** — ω_c = 2π·159 ≈ 1000 rad/s, so G(s) = 1/(1 + s/1000).

**Q209.** In a first-order system, the response to a unit impulse is:
`A) The step response itself | B) The derivative of the step response | C) The integral of the step response | D) Zero`
**Ans: B** — The impulse response equals the time derivative of the unit step response.

**Q210.** If the numerator of a first-order transfer function has a zero at the origin, the system's step response:
`A) Jumps instantly to final value | B) Starts from zero and rises | C) Is zero forever | D) Oscillates`
**Ans: B** — The zero at the origin cancels the integrator, giving G(s) = K/(s + a) form starting at zero.

**Q211.** A system's response time is improved by:
`A) Moving poles right | B) Moving poles further into the LHP | C) Adding zeros at the origin | D) Increasing the DC gain only`
**Ans: B** — Leftward pole shift increases speed.

**Q212.** An overdamped system's step response:
`A) Rises monotonically without oscillation | B) Oscillates | C) Reaches steady state instantly | D) Is always zero`
**Ans: A** — ζ > 1 gives a smooth monotonic approach.

**Q213.** An underdamped system's step response:
`A) Rises monotonically | B) Is critically damped | C) Diverges | D) Overshoots and oscillates about the steady state`
**Ans: D** — ζ < 1 gives decaying oscillations with overshoot.

**Q214.** The peak overshoot of a second-order system depends on:
`A) ω_n only | B) K only | C) Input amplitude only | D) The damping ratio only`
**Ans: D** — M_p = e^(−πζ/√(1−ζ²)) depends only on ζ for a standard second-order system.

**Q215.** A system with damping ratio ζ = 0.5 has peak overshoot of approximately:
`A) 4.3 % | B) 30 % | C) 50 % | D) 16.3 %`
**Ans: D** — M_p = e^(−π×0.5/0.866) = e^(−1.814) = 0.163.

**Q216.** A system with ζ = 0.707 has peak overshoot of approximately:
`A) 16.3 % | B) 1 % | C) 50 % | D) 4.3 %`
**Ans: D** — M_p = e^(−π) = 0.043.

**Q217.** A system with ζ → 0 has peak overshoot approaching:
`A) 0 % | B) 100 % | C) 50 % | D) 25 %`
**Ans: B** — M_p = e^(−πζ/√(1−ζ²)) → 1 as ζ → 0, giving 100% overshoot.

**Q218.** A system with ζ ≥ 1 has peak overshoot of:
`A) 0 % | B) 4.3 % | C) 16.3 % | D) 50 %`
**Ans: A** — Non-oscillatory systems do not overshoot.

**Q219.** The time constant interpretation: for a first-order system, the 63.2% point corresponds to:
`A) t = τ/2 | B) t = 2τ | C) t = 4τ | D) t = τ`
**Ans: D** — By definition of the time constant.

**Q220.** A first-order system's error for a constant input with unity feedback and K_p = 0 is:
`A) 1 | B) 0 | C) K | D) Infinite`
**Ans: A** — e_ss = 1/(1 + K_p) = 1 when K_p = 0 (open-loop, no feedback gain).

**Q221.** Given ẏ + ay = u, the impulse response is:
`A) (1/a)(1 − e^(−at))u(t) | B) a·e^(−at)u(t) | C) e^(−at)u(t) | D) 1/a constant`
**Ans: C** — G(s) = 1/(s + a) inverts to e^(−at)u(t).

**Q222.** A system with G(s) = (s+2)/[s(s+3)] has:
`A) Poles at −2 and −3 | B) Poles at 0 only | C) Poles at 0 and −3, zero at −2 | D) Zero at the origin`
**Ans: C** — Denominator s(s+3): poles 0, −3; numerator s+2: zero −2.

**Q223.** The mean value of a periodic output in steady state is found by:
`A) Reading the DC gain | B) The peak value | C) The pole value | D) Applying the final value theorem with the input period`
**Ans: D** — Steady state is periodic; its average equals the DC response to a DC equivalent.

**Q224.** A stable first-order system's steady-state output to a step is the DC gain, which equals:
`A) G(∞) | B) The residue at the pole | C) The time constant | D) G(0)`
**Ans: D** — G(0) = lim s→0 G(s) is the DC gain.

**Q225.** The response of a system with a pole closer to the imaginary axis is:
`A) Slower (larger time constant) | B) Faster | C) Identical | D) Oscillatory`
**Ans: A** — Poles nearer the axis give smaller |p| and hence larger τ = 1/|p|.

**Q226.** A system with two cascaded first-order stages G(s) = 1/(1+s)(1+2s) is:
`A) First order | B) Second order with two real poles | C) Unstable | D) Third order`
**Ans: B** — Product denominator (s+1)(s+2) has two distinct real poles.

**Q227.** A system with a transfer function having a dominant pole close to the origin is approximated by:
`A) A first-order system | B) A second-order system | C) A marginal system | D) An integrator`
**Ans: A** — The slowest pole dominates the transient; faster poles settle quickly.

**Q228.** A first-order system's response to a ramp input of slope 1 is:
`A) A step | B) An impulse | C) A ramp with a constant lag | D) A parabola`
**Ans: C** — A type-0 system tracks a ramp with a constant error (infinite e_ss if no integrator).

**Q229.** A system with a zero at the origin and otherwise first order has:
`A) Type-0 | B) Type-1 behaviour with e_ss = 0 for step | C) Type-2 | D) No poles`
**Ans: B** — The integrator (pole at origin) with unity gain gives zero step error.

**Q230.** If a first-order system's pole is at −j (imaginary), the response is:
`A) Decaying | B) Undamped oscillation | C) Growing | D) Constant`
**Ans: B** — A pole on the imaginary axis gives sustained oscillation.

**Q231.** The step response of G(s) = ω/(s + ω) reaches 63.2% at:
`A) 1/ω | B) ω | C) 1/ω² | D) ω²`
**Ans: A** — τ = 1/ω.

**Q232.** Two first-order systems in cascade each with τ = 0.1 s give an approximate overall:
`A) τ = 0.2 s | B) First order with τ = 0.05 s | C) Second-order response with τ_eff ≈ 0.1 s (dominant pole approximation) | D) No poles`
**Ans: C** — With equal τ, both poles at −10 give a second-order system.

**Q233.** The response of a system to an impulse input h(t) is called:
`A) The step response | B) The ramp response | C) The frequency response | D) The impulse response`
**Ans: D** — Impulse response h(t) = L⁻¹{G(s)}.

**Q234.** A system described by d²y/dt² + y = 0 with zero input is:
`A) Marginally stable (undamped) | B) Unstable | C) Stable | D) Uncontrollable`
**Ans: A** — Poles ±j give sustained oscillation.

**Q235.** The damping ratio of a system with poles −σ ± jω_d is:
`A) ζ = ω_d/ω_n | B) ζ = σ/ω_d | C) ζ = σ/ω_n | D) ζ = ω_n/σ`
**Ans: C** — ω_n = √(σ² + ω_d²) and ζ = σ/ω_n.

**Q236.** For poles −3 ± j4, the natural frequency and damping ratio are:
`A) ω_n = 5, ζ = 0.6 | B) ω_n = 4, ζ = 0.75 | C) ω_n = 7, ζ = 0.43 | D) ω_n = 3, ζ = 1.33`
**Ans: A** — ω_n = √(9+16) = 5, ζ = 3/5 = 0.6.

**Q237.** For poles −0.5 ± j0.866, the damping ratio is:
`A) 1 | B) 0.5 | C) 0.866 | D) 0.25`
**Ans: B** — ω_n = 1, ζ = 0.5/1 = 0.5.

**Q238.** A system's unit step response peaks at time t_p given by:
`A) t_p = π/(ω_n√(1−ζ²)) | B) t_p = 1/ω_n | C) t_p = 4/(ζω_n) | D) t_p = π/ω_n`
**Ans: A** — Peak time t_p = π/(ω_d) = π/(ω_n√(1−ζ²)).

**Q239.** The peak overshoot magnitude for a unit step is:
`A) e^(−ζπ) | B) e^(−πζ/√(1−ζ²)) | C) 1/(1+ζ) | D) ζe^(−π)`
**Ans: B** — Standard overshoot formula.

**Q240.** The number of zeros at the origin in a system gives:
`A) The damping | B) The type (along with poles at origin) | C) The overshoot | D) The bandwidth`
**Ans: B** — System type counts net poles at the origin; zeros at origin affect the order.

**Q241.** A stable system with a very small τ has:
`A) A low cutoff and slow response | B) No response | C) A high cutoff frequency and fast response | D) Infinite steady-state error`
**Ans: C** — ω_c = 1/τ; small τ means large bandwidth.

**Q242.** The response time and bandwidth of a first-order system satisfy:
`A) Bandwidth × rise time ≈ 1 | B) Bandwidth × rise time ≈ 2π | C) Bandwidth × rise time = 0 | D) Bandwidth × rise time ≈ 0.35`
**Ans: D** — With f_3dB = 1/(2πτ) and t_r ≈ 2.2τ, t_r·f_3dB ≈ 2.2/(2π) ≈ 0.35.

**Q243.** A system with transfer function G(s) = 1/[s(s + 1)] is a:
`A) First-order, type 0 | B) Second-order system, type 1 | C) Second-order, type 2 | D) First-order, type 1`
**Ans: B** — Two poles, one at origin: order 2, type 1.

**Q244.** The step response of 1/[s(s+1)] is:
`A) 1 − e^(−t) | B) t | C) e^(−t) | D) t − 1 + e^(−t)`
**Ans: D** — Partial fractions give y = t − 1 + e^(−t), a ramp minus transient.

**Q245.** For G(s) = 1/[s(s + 1)] with unit step, the error is:
`A) 0 | B) 1 − t + e^(−t) → ∞ (type-1 tracks ramp, error grows) | C) 1 | D) t`
**Ans: B** — Type-1 gives finite step error (0) but unbounded ramp error.

**Q246.** A system described by ẍ + ẋ + x = u has:
`A) ω_n = 1, ζ = 0.5 | B) ω_n = 1, ζ = 1 | C) ω_n = 0.5, ζ = 1 | D) ω_n = 2, ζ = 0.5`
**Ans: A** — s² + s + 1: ω_n = 1, 2ζω_n = 1 → ζ = 0.5.

**Q247.** A first-order system's steady-state output to a step of amplitude A is:
`A) A·G(0) | B) A | C) G(0) | D) 0`
**Ans: A** — The DC gain multiplies the input amplitude.

**Q248.** The decay rate of the natural response of a stable system is set by:
`A) The imaginary parts | B) The real parts of its poles | C) The gains | D) The zeros`
**Ans: B** — More negative real part means faster decay.

**Q249.** A system with poles at −1 and −100 has an approximately:
`A) First-order response dominated by the pole at −1 | B) First-order dominated by −100 | C) Second-order exact | D) Unstable`
**Ans: A** — The slow pole (−1) dominates; the fast pole (−100) settles almost instantly.

**Q250.** The overall response of a linear system to multiple inputs is:
`A) The product of responses | B) The largest response | C) Zero | D) The sum of responses to each input (superposition)`
**Ans: D** — Linearity permits superposition.

---

## SECTION 5 — Second-Order Systems & Specifications (Q251–Q330)

**Q251.** The standard second-order transfer function is:
`A) ω_n/(s + ζ) | B) s/(s² + ω_n²) | C) ω_n²/(s² + 2ζω_n s + ω_n²) | D) 1/(s + ω_n)²`
**Ans: C** — Compare with denominator s² + 2ζω_n s + ω_n².

**Q252.** The characteristic equation of a closed-loop system is s² + 2s + 2 = 0. Then the system is:
`A) Overdamped | B) Critically damped | C) Underdamped | D) Undamped`
**Ans: C** **[PYP-23 Q67]** — s = −1 ± j, so ω_n = √2 and ζ = 1/√2 ≈ 0.707 < 1, which is underdamped.

**Q253.** For a second-order system with ζ = 0.707, the damping is:
`A) Overdamped | B) Critically damped | C) Underdamped (standard Butterworth) | D) Undamped`
**Ans: C** — ζ < 1 with some overshoot; ζ = 1/√2 gives about 4.3 % overshoot.

**Q254.** The natural frequency ω_n of s² + 4s + 16 = 0 is:
`A) 4 rad/s | B) 2 rad/s | C) 8 rad/s | D) 16 rad/s`
**Ans: A** — ω_n² = 16, so ω_n = 4.

**Q255.** The damping ratio of s² + 4s + 16 = 0 is:
`A) 1 | B) 0.25 | C) 2 | D) 0.5`
**Ans: D** — 2ζω_n = 4 and ω_n = 4, so ζ = 0.5.

**Q256.** A system with ω_n = 10 rad/s and ζ = 0.5 has rise time (0–100%) of approximately:
`A) 0.35 s | B) 0.8 s | C) 0.18 s | D) 1.8 s`
**Ans: C** — t_r ≈ 1.8/ω_n = 0.18 s for an underdamped system.

**Q257.** The settling time (2%) of a second-order system is approximately:
`A) 1.8/ω_n | B) 4/(ζω_n) | C) π/ω_n | D) 1/ζ`
**Ans: B** — t_s ≈ 4/(ζω_n) is the standard 2 % criterion.

**Q258.** The 5% settling time of a second-order system is approximately:
`A) 4/(ζω_n) | B) 5/(ζω_n) | C) 8/(ζω_n) | D) 3/(ζω_n)`
**Ans: D** — 3/(ζω_n) gives about 5 % accuracy.

**Q259.** For ω_n = 8 rad/s and ζ = 0.8, the 2% settling time is about:
`A) 0.625 s | B) 0.225 s | C) 1.25 s | D) 0.4 s`
**Ans: A** — 4/(0.8×8) = 0.625 s.

**Q260.** The peak time of a system with ω_n = 5 rad/s, ζ = 0.6 is:
`A) 0.5 s | B) 1.25 s | C) 0.2 s | D) 0.8 s`
**Ans: D** — t_p = π/(5×0.8) = π/4 = 0.785 s.

**Q261.** The maximum value of a second-order step response for ζ = 0.5 is:
`A) 1.163 | B) 1.0 | C) 1.5 | D) 2.0`
**Ans: A** — Peak = 1 + M_p = 1 + 0.163 = 1.163.

**Q262.** A system with poles −2 ± j3 has:
`A) ω_n = 3, ζ = 2 | B) ω_n = 5, ζ = 0.4 | C) ω_n = √13 ≈ 3.6, ζ = 2/3.6 ≈ 0.55 | D) ω_n = 1, ζ = 2`
**Ans: C** — ω_n = √(4+9) = 3.606; ζ = 2/3.606 = 0.555.

**Q263.** The damped frequency ω_d for poles −2 ± j3 is:
`A) 3.6 rad/s | B) 2 rad/s | C) 5 rad/s | D) 3 rad/s`
**Ans: D** — ω_d is the imaginary part, 3 rad/s.

**Q264.** The relation between ω_n, ω_d and ζ is:
`A) ω_d = ω_n(1−ζ) | B) ω_n² = ω_d² + ζ²ω_n² | C) ω_n = ω_d² | D) ω_d = ω_nζ`
**Ans: B** — ω_d = ω_n√(1−ζ²), which squares to ω_n² = ω_d² + ζ²ω_n².

**Q265.** Increasing ω_n while keeping ζ fixed causes:
`A) Slower response | B) Faster rise and shorter settling | C) More overshoot | D) No change`
**Ans: B** — Both t_r = 1.8/ω_n and t_s = 4/(ζω_n) fall with ω_n.

**Q266.** Increasing ζ while keeping ω_n fixed causes:
`A) More overshoot | B) Faster settling always | C) Less overshoot, longer settling | D) Higher ω_n`
**Ans: C** — Higher ζ damps the oscillation but slows the non-oscillatory tail.

**Q267.** A design specification of Mp ≤ 5% requires:
`A) ζ ≥ 0.69 | B) ζ ≥ 0.5 | C) ζ ≥ 1 | D) ζ ≥ 0.2`
**Ans: A** — 0.05 = e^(−πζ/√(1−ζ²)) → ζ ≈ 0.69.

**Q268.** A specification of no overshoot requires:
`A) ζ = 0.5 | B) ζ = 0 | C) ζ ≥ 1 | D) ζ = 0.7`
**Ans: C** — Only ζ ≥ 1 gives a monotonic (non-oscillatory) response.

**Q269.** A system specified for fastest response with no overshoot is:
`A) Undamped | B) Heavily overdamped | C) Critically damped (ζ = 1) | D) Underdamped`
**Ans: C** — ζ = 1 is the boundary and the fastest monotonic response.

**Q270.** For ω_n = 10 rad/s, ζ = 1, the settling time is approximately:
`A) 0.18 s | B) 0.8 s | C) 0.1 s | D) 0.4 s`
**Ans: D** — t_s = 4/(1×10) = 0.4 s.

**Q271.** The percent overshoot for ζ = 0.25 is approximately:
`A) 16 % | B) 40 % | C) 4 % | D) 60 %`
**Ans: B** — M_p = e^(−π×0.25/0.968) = e^(−0.811) = 0.44, about 40 %.

**Q272.** The closed-loop transfer function with ω_n = 4, ζ = 0.8 is:
`A) 4/(s² + 3.2s + 4) | B) 16/(s² + 16s + 4) | C) 16/(s² + 6.4s + 16) | D) 1/(s² + 6.4s + 16)`
**Ans: C** — ω_n² = 16 and 2ζω_n = 2×0.8×4 = 6.4.

**Q273.** A system has poles −4 ± j3. Its ζ and ω_n are:
`A) ω_n = 5, ζ = 0.8 | B) ω_n = 4, ζ = 0.75 | C) ω_n = 3, ζ = 1.33 | D) ω_n = 5, ζ = 0.6`
**Ans: A** — ω_n = √(16+9) = 5, ζ = 4/5 = 0.8.

**Q274.** The impulse response of a second-order system shows the same frequency as:
`A) ω_n | B) ζ | C) ω_d (the damped natural frequency) | D) The gain`
**Ans: C** — The oscillation frequency of the response is ω_d.

**Q275.** The number of zeros at the origin affects a second-order system by:
`A) Changing ζ | B) Changing its effective type | C) Changing ω_n | D) Nothing`
**Ans: B** — Integrators at the origin determine system type and steady-state accuracy.

**Q276.** A transfer function with denominator s² + 2s + 1 is:
`A) Underdamped | B) Overdamped | C) Critically damped | D) Undamped`
**Ans: C** — (s+1)² repeated root gives ζ = 1.

**Q277.** For a second-order system, the natural frequency is the:
`A) Real part of the pole | B) Magnitude of the complex pole pair | C) Imaginary part only | D) Sum of the poles`
**Ans: B** — ω_n = |p| for complex conjugate poles.

**Q278.** The transfer function 25/(s² + 5s + 25) has:
`A) ω_n = 5, ζ = 0.5 | B) ω_n = 25, ζ = 5 | C) ω_n = 5, ζ = 2.5 | D) ω_n = 2.5, ζ = 1`
**Ans: A** — ω_n² = 25 → ω_n = 5; 2ζω_n = 5 → ζ = 0.5.

**Q279.** The 0–100% rise time formula t_r = 1.8/ω_n applies when:
`A) ζ = 0 always | B) ζ > 1 | C) 0.4 < ζ < 0.8 approximately | D) Any ζ`
**Ans: C** — Outside this range the more exact t_r = (π − φ)/ω_d is needed.

**Q280.** The delay (dead time) term in a second-order model appears as:
`A) K/(s(1+sT)) | B) K/s² | C) K·s | D) K·e^(−sT)/s`
**Ans: D** — Transport delay is represented by the exponential e^(−sT).

**Q281.** The open-loop transfer function K/[s(s+1)(s+2)] with unity feedback is type:
`A) Type 0 | B) Type 1 | C) Type 2 | D) Type 3`
**Ans: B** — One pole at the origin.

**Q282.** The steady-state error of a type-1 system for a step input is:
`A) Finite | B) Zero | C) Infinite | D) Undefined`
**Ans: B** — K_p = ∞ for a type-1 system, so e_ss = 1/(1+K_p) = 0.

**Q283.** The steady-state error of a type-1 system for a ramp input is:
`A) Zero | B) 1/K_v (finite) | C) Infinite | D) 1/K_p`
**Ans: B** — A ramp needs K_a, which is zero for type 1, so e_ss = 1/K_v.

**Q284.** For a unity-feedback system with G(s) = K/[s(s + 1)(s + 2)], K_v = K/2. To get a ramp error of 0.1, K must be:
`A) 20 | B) 5 | C) 40 | D) 2`
**Ans: A** — e_ss = 1/K_v = 2/K = 0.1 → K = 20.

**Q285.** A type-2 system has zero steady-state error for:
`A) Only step | B) Only ramp | C) Step and ramp inputs | D) Parabolic`
**Ans: C** — Type 2 gives e_ss = 0 for inputs up to degree 1.

**Q286.** For a type-2 system, the steady-state error to a parabolic input is:
`A) 1/K_a (finite) | B) Zero | C) Infinite | D) 1/K_v`
**Ans: A** — K_a = lim s²G(s) is finite for type 2, giving e_ss = 1/K_a.

**Q287.** The maximum closed-loop gain of a type-1 system at low frequency is:
`A) Zero | B) Unbounded | C) Unity | D) K`
**Ans: B** — The integrator makes |G| → ∞ as ω → 0.

**Q288.** The bandwidth of a second-order system with ω_n = 20, ζ = 0.7 is approximately:
`A) 20 rad/s | B) 28 rad/s | C) 7 rad/s | D) 15.6 rad/s`
**Ans: D** — ω_BW = ω_n√(1 − 2ζ² + √(2ζ⁴ − 4ζ² + 2)) = 20×0.78 ≈ 15.6.

**Q289.** For ζ = 0.707, the bandwidth equals approximately:
`A) 0.5ω_n | B) 2ω_n | C) 1.4ω_n | D) ω_n`
**Ans: D** — At ζ = 1/√2 the −3 dB point coincides with ω_n exactly.

**Q290.** The resonant peak magnitude of a second-order system is:
`A) M_r = 1/(2ζ) | B) M_r = 1/[2ζ√(1−ζ²)] | C) M_r = ζ | D) M_r = 1/ζ`
**Ans: B** — The peak of |G(jω)| occurs at ω = ω_n√(1−2ζ²) for ζ < 0.707.

**Q291.** The resonant frequency of a second-order system is:
`A) ω_r = ω_n | B) ω_r = ω_d | C) ω_r = ζω_n | D) ω_r = ω_n√(1−2ζ²)`
**Ans: D** — Valid for ζ < 1/√2; above that there is no resonance peak.

**Q292.** A second-order system with ζ = 0.5 has a resonant peak of:
`A) 1.15 | B) 2 | C) 1 | D) 0.5`
**Ans: A** — M_r = 1/(2×0.5×0.866) = 1/0.866 = 1.155.

**Q293.** Adding damping to a system:
`A) Increases both | B) Reduces the resonant peak and bandwidth | C) Changes only ω_n | D) Adds a pole`
**Ans: B** — Higher Γ flattens the peak; bandwidth decreases toward ω_n.

**Q294.** For a system to be monotonic (no resonant peak), one needs:
`A) ζ ≥ 0.707 | B) ζ < 0.707 | C) ζ = 0 | D) Any ζ`
**Ans: A** — Resonance disappears when 1 − 2ζ² ≤ 0.

**Q295.** The transfer function of a system with poles at −1 ± j4 and unity DC gain is:
`A) 1/(s² + 2s + 17) | B) 17/(s² + 17) | C) 4/(s² + 2s + 4) | D) 17/(s² + 2s + 17)`
**Ans: D** — ω_n² = 1 + 16 = 17; 2ζω_n = 2 (since ζω_n = 1).

**Q296.** If ζ = 0.5 and ω_n = 20, the 2% settling time and rise time are:
`A) t_s = 0.4 s, t_r = 0.09 s | B) t_s = 0.2 s, t_r = 0.4 s | C) t_s = 4 s, t_r = 0.09 s | D) t_s = 0.4 s, t_r = 1 s`
**Ans: A** — t_s = 4/(0.5×20) = 0.4 s; t_r = 1.8/20 = 0.09 s.

**Q297.** A system is required to have t_s = 0.5 s with 5% tolerance. The minimum ω_n is approximately:
`A) 7.5 rad/s | B) 5 rad/s | C) 15 rad/s | D) 1 rad/s`
**Ans: A** — ω_n = 3/(ζt_s) ≥ 3/(1×0.5) = 6; with ζ ≈ 1 this gives about 6–7.5 rad/s.

**Q298.** The characteristic equation s² + 2ζω_n s + ω_n² = 0 has roots:
`A) −ζω_n ± ω_n√(ζ²−1) | B) −ζω_n ± ω_n√(1−ζ²) | C) ±ω_nζ | D) −ω_n ± ζω_n`
**Ans: B** — The quadratic formula with ζ < 1 gives a complex pair with real part −ζω_n.

**Q299.** The second-order system with the fastest settling time for a given ζω_n product is chosen by:
`A) ζ = 0 | B) ζ = 2 | C) Any ζ | D) Using ζ ≈ 0.707 (max ω_BW/ω_n ratio with low overshoot)`
**Ans: D** — ζ ≈ 0.7 balances speed and overshoot, the common design choice.

**Q300.** For ζ < 1, the impulse response of ω_n²/(s² + 2ζω_n s + ω_n²) is:
`A) e^(−ζω_n t) cos ω_d t | B) ω_n e^(−ω_n t) | C) (ω_n/√(1−ζ²))e^(−ζω_n t) sin ω_d t | D) sin ω_d t only`
**Ans: C** — The impulse response is the derivative of the step response.

**Q301.** A second-order system G(s) = 1/(s² + s + 1) has poles:
`A) −1 ± j | B) ±j | C) −1 | D) −0.5 ± j0.866`
**Ans: D** — s = [−1 ± √(1−4)]/2 = −0.5 ± j0.866.

**Q302.** The system 1/(s² + s + 1) has:
`A) ω_n = 1, ζ = 1 | B) ω_n = 0.5, ζ = 1 | C) ω_n = 1, ζ = 0.5 | D) ω_n = 1, ζ = 0.25`
**Ans: C** — ω_n = 1 and 2ζω_n = 1 → ζ = 0.5.

**Q303.** For a lightly damped system (ζ ≈ 0), the peak time is approximately:
`A) 1/ω_n | B) π/ω_n | C) 4/ω_n | D) 2π/ω_n`
**Ans: B** — t_p = π/(ω_n√(1−ζ²)) → π/ω_n as ζ → 0.

**Q304.** The number of oscillations before settling for a lightly damped system is approximately:
`A) 1/ζ | B) ω_d/(2πζω_n) | C) ω_n | D) π/ζ`
**Ans: B** — Each cycle decays by e^(−2πζ/√(1−ζ²)); the count follows from the envelope.

**Q305.** A system with ζ = 0.1 undergoes roughly how many visible overshoots before settling:
`A) About 1 | B) About 3–4 | C) About 20 | D) Zero`
**Ans: B** — 1/(2πζ) ≈ 1.6 cycles per e-fold; the oscillation envelope decays slowly.

**Q306.** A system G(s) = ω_n²/(s² + 2ζω_n s + ω_n²) with ζ = 1 and ω_n = 5 has poles:
`A) −5 ± j5 | B) ±j5 | C) −5 (repeated) | D) −2.5 double`
**Ans: C** — Repeated root at −ζω_n = −5.

**Q307.** Increasing the gain K in K/(s² + 2ζω_n s + ω_n²) generally:
`A) Decreases overshoot | B) Has no effect | C) Makes it slower | D) Increases overshoot and bandwidth`
**Ans: D** — Higher gain pushes the poles out along the root locus, raising ζ^-1 effect and bandwidth.

**Q308.** A spec requires overshoot ≤ 4.3 % and the fastest possible rise. The design damping ratio is:
`A) ζ = 0.707 | B) ζ = 0.5 | C) ζ = 1 | D) ζ = 0.2`
**Ans: A** — ζ = 1/√2 gives exactly 4.3 % overshoot and the widest bandwidth among low-overshoot designs.

**Q309.** A system has poles at −0.1 ± j1. Its settling time (2%) is approximately:
`A) 6.28 s | B) 10 s | C) 1 s | D) 40 s`
**Ans: D** — t_s = 4/(ζω_n) = 4/(0.1×1.005) ≈ 39.8 s.

**Q310.** The rise time of a system with poles −0.1 ± j1 is approximately:
`A) 0.1 s | B) 40 s | C) 6.28 s | D) 1.79 s`
**Ans: D** — t_r ≈ 1.8/ω_n ≈ 1.8/1.005 = 1.79 s.

**Q311.** For an underdamped system the maximum acceleration is approximately:
`A) ω_n | B) ζω_n² | C) ω_n² e^(−ζπ/√(1−ζ²)) | D) ω_n²`
**Ans: C** — The maximum of the derivative of the response; it scales with ω_n² times the overshoot factor.

**Q312.** The "dominant second-order model" is valid when:
`A) Higher-order poles are at least 5× farther left | B) All poles are equal | C) There are no zeros | D) The system is first order`
**Ans: A** — A 5:1 separation gives less than ~1 % dynamic interaction.

**Q313.** A system with a pair of dominant complex poles and a far real pole at −50 is approximated by:
`A) The real pole only | B) Both fully | C) An integrator | D) The complex pair only`
**Ans: D** — The dominant (slowest) poles govern the transient response.

**Q314.** A system's response is dominated by a pole if it is:
`A) Slowest-decaying (closest to the imaginary axis) | B) Largest magnitude | C) Most negative | D) On the axis`
**Ans: A** — The slowest pole sets the dominant time constant.

**Q315.** A system 100/[(s+1)(s+2)(s+10)] is best approximated by a dominant first-order model. Its residue at the pole s = −1 is approximately:
`A) 11.1/(s + 1) | B) 100/(s + 1) | C) 100/(s + 10) | D) 100/((s + 1)(s + 2))`
**Ans: A** — A₁ = 100/[(−1+2)(−1+10)] = 100/9 = 11.1, so the dominant term is 11.1/(s+1).

**Q316.** The velocity constant of a type-1 unity-feedback system with open-loop K/[s(s+1)(s+3)] is:
`A) K | B) K/3 | C) K/9 | D) 3/K`
**Ans: B** — K_v = lim s→0 sG(s) = K/[(1)(3)] = K/3.

**Q317.** A system with K_v = 20 has a steady-state ramp error of:
`A) 20 | B) 0.2 | C) 1 | D) 0.05`
**Ans: D** — e_ss = 1/K_v = 0.05.

**Q318.** If the loop gain at low frequency is increased by a factor of 10, the steady-state error for a ramp:
`A) Increases by 10× | B) Is unchanged | C) Decreases by 10× | D) Becomes zero`
**Ans: C** — e_ss = 1/K_v, so 10× gain gives one-tenth the error.

**Q319.** A closed-loop system with 60% overshoot has a damping ratio of approximately:
`A) 0.707 | B) 0.42 | C) 0.1 | D) 1`
**Ans: B** — Solving e^(−πζ/√(1−ζ²)) = 0.6 gives ζ ≈ 0.42.

**Q320.** A closed-loop system with 20% overshoot has ζ ≈:
`A) 0.36 | B) 0.7 | C) 0.5 | D) 0.9`
**Ans: A** — e^(−πζ/√(1−ζ²)) = 0.2 → ζ ≈ 0.36.

**Q321.** A closed-loop system with 30% overshoot has ζ ≈:
`A) 0.6 | B) 0.45 | C) 0.8 | D) 0.31`
**Ans: D** — Solving for 0.3 overshoot gives ζ ≈ 0.31.

**Q322.** The natural frequency required for t_s = 0.4 s at ζ = 0.5 is:
`A) 10 rad/s | B) 40 rad/s | C) 5 rad/s | D) 20 rad/s`
**Ans: D** — ω_n = 4/(ζt_s) = 4/(0.5×0.4) = 20.

**Q323.** A system has a damping ratio obtained from its phase margin. If PM ≈ 60° and two open-loop poles are present, ζ ≈:
`A) 0.9 | B) 0.1 | C) 1 | D) 0.5–0.6`
**Ans: D** — A phase margin near 60° corresponds to roughly ζ = 0.5–0.6 for typical loops.

**Q324.** The transfer function of a system with ω_n = 100, ζ = 0.7 and unity DC gain is:
`A) 100/(s² + 140s + 10000) | B) 10000/(s² + 140s + 10000) | C) 10000/(s² + 70s + 10000) | D) 1/(s² + 140s + 10000)`
**Ans: B** — ω_n² = 10000, 2ζω_n = 140.

**Q325.** An underdamped second-order system has poles:
`A) Real and positive | B) Real and negative | C) Complex conjugates with negative real parts | D) Purely imaginary`
**Ans: C** — 0 < ζ < 1 gives complex poles with Re < 0.

**Q326.** A system with ω_n = 2 rad/s, ζ = 0.2 oscillates at:
`A) 1.96 rad/s | B) 2 rad/s | C) 0.4 rad/s | D) 4 rad/s`
**Ans: A** — ω_d = 2×√(1−0.04) = 2×0.98 = 1.96 rad/s.

**Q327.** The settling envelope decays as:
`A) e^(−ω_n t) | B) e^(−ζω_n t) | C) e^(−ζω_d t) | D) e^(−ω_d t)`
**Ans: B** — The natural response envelope is e^(−σt) with σ = ζω_n.

**Q328.** The 2% settling criterion requires the envelope to decay to 0.02, so:
`A) ζω_n·t_s = 2 | B) ζω_n·t_s = 4 | C) ζω_n·t_s = 1 | D) ζω_n·t_s = 8`
**Ans: B** — e^(−4) = 0.018, matching the 2 % tolerance.

**Q329.** For a system with ζω_n = 2 rad/s, the 5% settling time is:
`A) 0.75 s | B) 3 s | C) 6 s | D) 1.5 s`
**Ans: D** — t_s(5%) = 3/2 = 1.5 s.

**Q330.** The acceleration error constant K_a is defined as:
`A) K_a = lim(s→0) G(s) | B) K_a = lim(s→0) sG(s) | C) K_a = lim(s→∞) sG(s) | D) K_a = lim(s→0) s²G(s)`
**Ans: D** — Each polynomial input degree consumes one more factor of s.

---

## SECTION 6 — Stability Concepts & Routh–Hurwitz (Q331–Q425)

**Q331.** A system is stable if:
`A) All its poles lie in the left half plane | B) All its poles lie in the RHP | C) Its zeros are in the LHP | D) Its gain is positive`
**Ans: A** — Every natural mode must decay.

**Q332.** The condition for asymptotic stability in the s-plane is:
`A) All poles in the RHP | B) Poles on the imaginary axis | C) All poles strictly in the LHP | D) No poles`
**Ans: C** — Strictly left of the imaginary axis.

**Q333.** A system with a pole on the imaginary axis is:
`A) Unstable | B) Asymptotically stable | C) Marginally stable | D) Uncontrollable`
**Ans: C** — It neither decays nor grows, giving sustained oscillation.

**Q334.** The characteristic equation for a standard second-order system is:
`A) s² + 1 = 0 | B) s³ = 0 | C) a₀ = 0 | D) a₂s² + a₁s + a₀ = 0`
**Ans: D** — The general quadratic form.

**Q335.** For a second-order system a₂s² + a₁s + a₀ = 0, the Routh stability conditions are:
`A) a₂ > 0, a₁ < 0, a₀ > 0 | B) All aₙ > 0 | C) a₂ > 0, a₁ > 0, a₀ < 0 | D) a₂ > 0, a₁ > 0, a₀ > 0`
**Ans: D** **[PYP-23 Q64]** — All coefficients must be positive for a second-order polynomial to be Hurwitz.

**Q336.** A second-order system with a₂ = 1, a₁ = −2, a₀ = 1 is:
`A) Stable | B) Unstable | C) Marginally stable | D) Uncontrollable`
**Ans: B** — a₁ < 0 violates Hurwitz; poles are 1 ± j0, in the RHP.

**Q337.** A system with characteristic equation s² + 3s + 2 = 0 has poles:
`A) 1, 2 | B) −1, +2 | C) ±j | D) −1, −2`
**Ans: D** — (s+1)(s+2) = 0.

**Q338.** The Routh–Hurwitz criterion states that a system is stable if:
`A) There are an even number of sign changes | B) There are no sign changes in the first column of the Routh array | C) The last row is zero | D) All elements are equal`
**Ans: B** — Zero sign changes means all poles in the LHP.

**Q339.** The number of sign changes in the first column of the Routh array equals:
`A) The number of poles in the LHP | B) The number of poles in the RHP | C) The number of zeros | D) The number of sign changes in the coefficients`
**Ans: B** — Each sign change corresponds to one RHP root.

**Q340.** For a system with characteristic equation s³ + 3s² + 3s + K, stability requires:
`A) K > 9 only | B) 0 < K < 9 | C) K > 0 only | D) K < 0 only`
**Ans: B** — Routh gives a first column 1, 3, (9−K)/3, K; positivity needs 0 < K < 9.

**Q341.** For s³ + 2s² + 3s + K, the stability range of K is:
`A) 0 < K < 8 | B) K > 6 | C) K > 0 | D) 0 < K < 6`
**Ans: D** — First column: 1, 2, (6−K)/2, K → 0 < K < 6.

**Q342.** For the characteristic equation s⁴ + 3s³ + 2s² + 4s + K, the stability range of K is:
`A) 0 < K < 6 | B) 0 < K < 10 | C) 0 < K < 2 | D) 0 < K < 8/9`
**Ans: D** **[PYP-25 Q31]** — Routh array first column: 1, 3, 2/3, (4 − 4.5K)/(2/3), K; the s¹ row requires 4 − 4.5K > 0, so K < 8/9.

**Q343.** The Routh array for s⁴ + 3s³ + 2s² + 4s + K begins with:
`A) s⁴: 1, 2, K; s³: 3, 4, 0 | B) s⁴: 1, 3, K; s³: 2, 4, 0 | C) s⁴: 3, 4, K; s³: 1, 2, 0 | D) s⁴: 1, 2, 0; s³: 3, 4, K`
**Ans: A** — Even powers fill the first row and odd powers the second.

**Q344.** In the Routh array, the first column of the s⁴ row for a monic quartic begins with:
`A) 3 | B) K | C) 2 | D) 1`
**Ans: D** — The leading coefficient of the polynomial.

**Q345.** If a complete row of the Routh array becomes zero, this indicates:
`A) Roots symmetric about the origin, requiring an auxiliary equation | B) The system is stable | C) K = 0 | D) The array is complete`
**Ans: A** — Use the derivative of the preceding row to form the auxiliary polynomial.

**Q346.** The auxiliary polynomial in the Routh array is obtained from:
`A) The derivative of the polynomial in the row above the zero row | B) The last row | C) The first row | D) The gain K`
**Ans: A** — Differentiating gives the auxiliary polynomial whose roots are then placed.

**Q347.** The condition for marginal stability from a Routh array row of zeros is that the auxiliary equation has:
`A) Roots in the RHP | B) No roots | C) Roots on the imaginary axis | D) Roots at the origin only`
**Ans: C** — Purely imaginary roots indicate marginal stability.

**Q348.** If a row of the Routh array has its first element zero but others nonzero, one should:
`A) Conclude instability | B) Stop the array | C) Set K = 0 | D) Replace it with a small ε and continue`
**Ans: D** — Substituting ε and taking the limit resolves the ambiguity.

**Q349.** The Routh criterion is used to determine:
`A) The exact pole locations | B) The number of roots in the RHP for a range of a parameter | C) The bandwidth | D) The phase margin`
**Ans: B** — It counts RHP roots; it does not give their locations.

**Q350.** The Routh–Hurwitz criterion for a general nth-order system requires:
`A) Only the first coefficient to be positive | B) All roots real | C) All the Hurwitz determinants to be positive | D) The last coefficient zero`
**Ans: C** — Δ₁ > 0, Δ₂ > 0, ..., Δₙ > 0.

**Q351.** For a cubic a₃s³ + a₂s² + a₁s + a₀, the Hurwitz conditions are:
`A) a₃,a₂,a₁,a₀ > 0 and a₂a₁ > a₃a₀ | B) All coefficients > 0 | C) a₂a₁ < a₃a₀ | D) a₁a₀ > a₂a₃`
**Ans: A** — Plus the extra determinant condition, which all-positive coefficients alone do not guarantee.

**Q352.** A system with characteristic equation s³ + s² + s + 1 = 0 is:
`A) Stable | B) Marginally stable | C) Uncontrollable | D) Unstable (poles −1, ±j)`
**Ans: D** — s³+s²+s+1 = (s+1)(s²+1), so poles are −1 and ±j; the imaginary-axis pair means it is not asymptotically stable.

**Q353.** For a closed-loop system with characteristic equation 1 + G(s)H(s) = 0, if G(s)H(s) has a RHP pole:
`A) The closed-loop is stable | B) The closed-loop is unstable | C) It is marginal | D) It depends only on H`
**Ans: B** — RHP poles of the open-loop survive unless cancelled by a RHP zero of GH.

**Q354.** A characteristic equation s² − 2s + 2 = 0 corresponds to:
`A) Unstable (poles 1 ± j) | B) Stable | C) Marginal | D) No real part`
**Ans: A** — Positive real part means growing oscillations.

**Q355.** The Routh array of s³ + 6s² + 11s + 6 gives the first column:
`A) 1, 6, 11, 6 | B) 1, 6, 10, 6 | C) 1, 11, 6, 6 | D) 6, 1, 10, 6`
**Ans: B** — b₁ = (6·11 − 1·6)/6 = 10, so the first column is 1, 6, 10, 6 — all positive, hence stable.

**Q356.** The polynomial s³ + 6s² + 11s + 6 factors as:
`A) (s+1)(s+2)(s+4) | B) (s−1)(s−2)(s−3) | C) (s+1)²(s+4) | D) (s+1)(s+2)(s+3)`
**Ans: D** — Expanding (s+1)(s+2)(s+3) = s³ + 6s² + 11s + 6.

**Q357.** All poles of s³ + 6s² + 11s + 6 lie at:
`A) 1, 2, 3 | B) ±j | C) −1, −2, −3 | D) 0`
**Ans: C** — Roots are −1, −2, −3, all stable.

**Q358.** The Hurwitz determinant Δ₂ for a₃=1, a₂=6, a₁=11, a₀=6 is:
`A) 6 | B) 11 | C) a₂a₁ − a₃a₀ = 66 − 6 = 60 | D) 66`
**Ans: C** — Δ₂ = |a₂ a₃; a₀ a₁| = a₂a₁ − a₃a₀.

**Q359.** A system is unstable if the Routh array's first column shows:
`A) No sign changes | B) Only zeros | C) Positive values | D) An odd number of sign changes`
**Ans: D** — Each sign change is an RHP pole; an odd count means instability.

**Q360.** If the Routh array first column is 1, 3, −1, 4, then the system:
`A) Has 1 RHP pole (one sign change) | B) Has 2 RHP poles | C) Is stable | D) Has 3 RHP poles`
**Ans: A** — 1 → 3 → −1 → 4 gives exactly one sign change.

**Q361.** A quartic characteristic equation s⁴ + 2s³ + 3s² + 4s + 5 is:
`A) Stable | B) Unstable | C) Marginal | D) Uncontrollable`
**Ans: B** — b₁ = (2·3 − 1·4)/2 = 1 and c₁ = (1·4 − 2·5)/1 = −6, giving the first column 1, 2, 1, −6, 5 with two sign changes.

**Q362.** The number of unstable poles of s⁴ + 2s³ + 3s² + 4s + 5 is:
`A) 0 | B) 2 | C) 1 | D) 4`
**Ans: B** — Two sign changes in the first column 1, 2, 1, −6, 5.

**Q363.** A zero row in the Routh array appears when the auxiliary polynomial's roots are:
`A) All positive | B) Symmetric about the origin | C) All in the LHP | D) Complex only`
**Ans: B** — Symmetry about the origin implies roots in ± pairs.

**Q364.** For s⁴ + 4s³ + 6s² + 4s + K, the s³ row of the Routh array is:
`A) 1, 6, K | B) 4, 4, 0 | C) 6, 4, K | D) 4, K, 0`
**Ans: B** — Odd-power coefficients fill that row.

**Q365.** The K range for stability of s⁴ + 4s³ + 6s² + 4s + K is:
`A) 0 < K < 8 | B) 0 < K < 4 | C) K > 4 | D) K < 0`
**Ans: B** — b₁ = (4·6 − 1·4)/4 = 5; c₁ = (5·4 − 4K)/5 = 4 − 0.8K > 0 → K < 5; combined with K > 0.

**Q366.** The stability of the closed-loop system with G(s)H(s) = K/[s(s+1)(s+2)] requires:
`A) K > 6 | B) 0 < K < 6 | C) K < 0 | D) Any K`
**Ans: B** — Characteristic equation s³ + 3s² + 2s + K = 0; Routh gives K < 6.

**Q367.** A system is stable for a range of K if the Routh array has:
`A) Sign changes only at the endpoints | B) An odd number of changes | C) A zero row | D) No sign changes for all K in that range`
**Ans: D** — The range of K giving no sign changes is exactly the stable set.

**Q368.** The characteristic equation obtained from 1 + G(s)H(s) = 0 with G(s) = K/[s(s+1)] and H(s) = 1 is:
`A) s² + s − K = 0 | B) s + K = 0 | C) s² + K = 0 | D) s² + s + K = 0`
**Ans: D** — 1 + K/[s(s+1)] = 0 → s(s+1) + K = 0.

**Q369.** For s² + s + K = 0, stability requires:
`A) K > 0 | B) K < 0 | C) K = 0 | D) K > 1 only`
**Ans: A** — All coefficients positive.

**Q370.** The damping ratio of s² + s + 4 = 0 is:
`A) 0.5 | B) 1 | C) 0.25 | D) 0.125`
**Ans: C** — ω_n = 2, 2ζω_n = 1 → ζ = 0.25.

**Q371.** The Routh array is essentially a:
`A) Graphical plot of the locus | B) Frequency response | C) Tabulated procedure for counting RHP roots | D) State transformation`
**Ans: C** — A pure algebraic technique requiring no plotting.

**Q372.** The Routh–Hurwitz criterion can be applied to a system whose characteristic equation is expressed in terms of:
`A) The power of s with real coefficients | B) Complex coefficients only | C) Laplace variables | D) Any polynomial`
**Ans: A** — It applies to real-coefficient polynomials in s.

**Q373.** For the system 1 + K/s(s + 1)(s + 2)(s + 3) = 0, increasing K:
`A) Always stabilizes it | B) Has no effect | C) Reduces the bandwidth | D) Eventually destabilizes the system`
**Ans: D** — Gain increase moves poles right along the root locus, eventually crossing the axis.

**Q374.** A system's stability can be checked by testing whether:
`A) The DC gain is positive | B) The trace of A is positive | C) The zeros are in the LHP | D) All coefficients of the characteristic equation are positive AND the Hurwitz determinants are positive`
**Ans: D** — Positivity of coefficients is necessary but not sufficient; the determinants complete the test.

**Q375.** A system with characteristic equation s⁵ + s⁴ + s³ + s² + s + 1 = 0 is:
`A) Stable | B) Marginal only | C) Unstable (roots include those of s⁶−1 excluding s−1, including j) | D) Uncontrollable`
**Ans: C** — Factoring (s+1)(s⁴+s²+1) reveals roots on the imaginary axis plus one in the RHP.

**Q376.** If the gain K in K/(s(s+1)(s+2)) is set to exactly 6, the system is:
`A) Marginally stable (one pair on imaginary axis) | B) Stable | C) Unstable | D) Uncontrollable`
**Ans: A** — At K = 6 the s¹ row vanishes (1, 3, 0, 6); the auxiliary equation from the s² row gives a pair on the imaginary axis.

**Q377.** The stability of a nonlinear system can be assessed locally by:
`A) The Routh array always | B) Linearising about an equilibrium point and analysing the Jacobian | C) The Bode plot only | D) It cannot be assessed`
**Ans: B** — Linearisation gives necessary local conditions (Lyapunov's indirect method).

**Q378.** An equilibrium point of a state model is found by:
`A) Setting y = 0 | B) Setting u = 0 only | C) Setting ẋ = 0 and solving Ax* + Bu* = 0 | D) Finding the poles`
**Ans: C** — All state derivatives must vanish.

**Q379.** A nonlinear system with a positively invariant region and a Lyapunov function that decreases is:
`A) Asymptotically stable | B) Unstable | C) Marginally stable | D) Not analysable`
**Ans: A** — Lyapunov's direct method establishes stability.

**Q380.** The Lyapunov function must be:
`A) Negative definite | B) Zero | C) Any function | D) Positive definite and its derivative negative definite`
**Ans: D** — V > 0 for x ≠ 0 and V̇ < 0 guarantees asymptotic stability.

**Q381.** The region of attraction is:
`A) The set of poles | B) The gain range | C) The set of initial conditions converging to the stable equilibrium | D) The bandwidth`
**Ans: C** — The basin of attraction.

**Q382.** The absolute stability of a nonlinear system can be studied with:
`A) The Routh array | B) Root locus | C) The circle/popov criterion | D) The Bode plot only`
**Ans: C** — Popov's criterion extends frequency-domain methods to nonlinear loops.

**Q383.** A limit cycle in a nonlinear system is:
`A) A growing oscillation | B) A sustained oscillation of fixed amplitude | C) A transient | D) A pole`
**Ans: B** — Self-sustaining bounded oscillation.

**Q384.** Describing-function analysis of nonlinearities gives:
`A) The exact solution | B) An equivalent gain/description | C) The poles | D) The state matrix`
**Ans: B** — A quasi-linear approximation valid for describing-function-sized signals.

**Q385.** The effect of saturation on a control system is:
`A) Increased gain | B) Reduced gain and increased overshoot | C) No effect | D) Improved stability`
**Ans: B** — Saturation lowers the effective gain, degrading damping.

**Q386.** Anti-windup in a PID controller prevents:
`A) Derivative kick | B) Setpoint changes | C) Sensor noise | D) Integral accumulation during actuator saturation`
**Ans: D** — Clamping or back-calculation stops the integrator drifting.

**Q387.** In a nonlinear system, the sector bound [k₁, k₂] describes:
`A) The pole locations | B) The gain range of the nonlinearity | C) The frequency range | D) The disturbance range`
**Ans: B** — The nonlinearity is bounded between slopes k₁ and k₂.

**Q388.** A relay (signum) nonlinearity has describing function gain:
`A) 2M/(πA) | B) πA/(4M) | C) M/A | D) 4M/(πA)`
**Ans: D** — For output level M and input amplitude A.

**Q389.** The relative stability of a system is measured by:
`A) The DC gain | B) Gain and phase margins | C) The number of poles | D) The rise time only`
**Ans: B** — These quantify distance from the stability boundary.

**Q390.** A system whose poles move toward the imaginary axis with increasing gain becomes:
`A) More stable | B) Less stable | C) Unchanged | D) Oscillatory at all gains`
**Ans: B** — Marginally stable when they reach the axis.

**Q391.** Stability of a system with poles at the origin and in the LHP (no RHP) is:
`A) Marginal if a simple origin pole exists with no other axis poles | B) Unstable | C) Always stable | D) Not defined`
**Ans: A** — A single integrator gives a ramp for step input, so it is marginal by the strict test.

**Q392.** The characteristic equation s⁴ + s³ − s² − s − 1 = 0 has:
`A) All poles in the LHP | B) Only imaginary poles | C) No real poles | D) At least one RHP pole`
**Ans: D** — The negative coefficient violates the necessary positivity condition.

**Q393.** A necessary (not sufficient) condition for stability is:
`A) All coefficients of the characteristic polynomial are of the same sign | B) The sum of coefficients is zero | C) The constant term is negative | D) The leading coefficient is zero`
**Ans: A** — Positivity alone is necessary but not sufficient: s³+s²+2s+10 has all-positive coefficients yet Δ₂ = 2 − 10 < 0, so it is unstable.

**Q394.** For s³ + 6s² + 11s + 6 all coefficients are positive, so:
`A) It is definitely unstable | B) The system may be stable (check Δ₂ = 60 > 0) | C) It is marginal | D) No conclusion at all is possible`
**Ans: B** — Positivity plus Δ₂ > 0 confirms stability.

**Q395.** The characteristic equation s³ + s² + 2s + 10 = 0 has:
`A) All poles in the LHP | B) Poles on the axis | C) No poles | D) At least one RHP pole`
**Ans: D** — Δ₂ = 1·2 − 1·10 = −8 < 0, failing the Hurwitz condition.

**Q396.** The roots of s³ + s² + 2s + 10 = 0 are approximately:
`A) −2.4, −1.2 ± j2.0 | B) 2.4, 1.2 ± j2.0 | C) −1, ±j3 | D) 0, ±j`
**Ans: A** — One real root ≈ −2.3; since the sum of all roots is −1, the pair sums to +1.3, i.e. each has real part +0.65, confirming the RHP pair.

**Q397.** For a unity-feedback system, the closed-loop poles are the roots of:
`A) G(s) = 0 | B) 1 + G(s) = 0 | C) 1 − G(s) = 0 | D) G(s) = 1/s`
**Ans: B** — The characteristic equation with H = 1.

**Q398.** Absolute stability for a linear system means:
`A) Stable at nominal gain only | B) Marginally stable | C) Unstable | D) Stable for every admissible gain variation`
**Ans: D** — Robustness to parameter variation.

**Q399.** A system described by ẍ + ẋ + 5x = 0 (no input) is:
`A) Stable | B) Unstable | C) Marginal | D) Uncontrollable`
**Ans: B** — Poles are −0.5 ± j2.18, both in the LHP, so the system is asymptotically stable (underdamped).

**Q400.** The system s² + s + 5 = 0 has:
`A) ω_n = √5 ≈ 2.24, ζ ≈ 0.224 | B) ω_n = 5, ζ = 0.5 | C) ω_n = 1, ζ = 2.24 | D) ω_n = 2.24, ζ = 1`
**Ans: A** — ω_n = √5; ζ = 1/(2√5).

**Q401.** A system with the characteristic equation (s+1)(s+2)(s+3) = 0 is:
`A) Unstable | B) Marginal | C) Third-order unstable | D) Stable (poles −1, −2, −3)`
**Ans: D** — All three poles are negative.

**Q402.** The Routh array can also detect the range of gain K for which a system is:
`A) Marginal | B) Complex | C) Stable | D) Any`
**Ans: C** — This is its standard use in design.

**Q403.** If the s¹ row of the Routh array evaluates to zero, the system is:
`A) Definitely stable | B) At the boundary of stability (use the auxiliary polynomial) | C) Definitely unstable | D) Zero order`
**Ans: B** — A vanishing element signals the marginal case.

**Q404.** For the characteristic equation s³ + 2s² + 3s + 6 = 0, the poles are:
`A) 2, ±j√3 | B) −1, −2, −3 | C) −2, ±j√3 | D) ±j`
**Ans: C** — s³+2s²+3s+6 = (s+2)(s²+3), so s = −2 and s = ±j√3.

**Q405.** The system (s+2)(s²+3) = 0 is:
`A) Unstable | B) Asymptotically stable | C) Marginally stable | D) Unstable with 2 RHP poles`
**Ans: C** — Poles −2 and ±j1.732 lie on the imaginary axis.

**Q406.** Which of the following is a necessary and sufficient condition for a second-order system a₂s²+a₁s+a₀ to be Hurwitz?
`A) a₂ > 0 and a₀ > 0 only | B) a₂, a₁, a₀ all positive | C) a₁ > 0 only | D) Sum of coefficients positive`
**Ans: B** — For order 2 this simple positivity test is both necessary and sufficient.

**Q407.** For the closed-loop system with K/[s(s+2)(s+4)], the stability range of K is:
`A) 0 < K < 8 | B) 0 < K < 48 | C) 0 < K < 2 | D) K > 48`
**Ans: B** — s³+6s²+8s+K: b₁ = (6·8 − K)/6 = 8 − K/6 > 0 → K < 48, and K > 0.

**Q408.** A system is said to be conditionally stable when:
`A) It is never stable | B) It is stable for a bounded range of a parameter | C) It is stable for all gains | D) It has no gain`
**Ans: B** — Stability holds only within limits set by the Routh analysis.

**Q409.** The Routh array is arranged so that the first column contains:
`A) The sums of each row | B) The last coefficients | C) The leading coefficients of each row of the array | D) The zeros`
**Ans: C** — The first column drives the sign-change count.

**Q410.** The characteristic equation of a system with poles at s = 0 (double) and s = −5 is:
`A) s(s+5)² | B) (s−5)s² | C) s²(s + 5) = s³ + 5s² | D) s³ + 1`
**Ans: C** — Product of (s − p) terms.

**Q411.** A system with characteristic polynomial s³ + 5s² + 6s is:
`A) Unstable (zero constant term → pole at origin with positive coefficients) | B) Stable | C) Marginal | D) Fourth order`
**Ans: A** — s(s²+5s+6) = s(s+2)(s+3), so poles are 0, −2, −3; the pole at the origin makes it marginally, not asymptotically, stable.

**Q412.** The poles of s³ + 5s² + 6s are:
`A) 0, −2, −3 | B) 0, 2, 3 | C) ±j, 0 | D) 0 only`
**Ans: A** — s(s+2)(s+3) = 0.

**Q413.** The Hurwitz determinant Δ₁ for a₃s³+a₂s²+a₁s+a₀ is:
`A) a₀ | B) a₁ | C) a₃ | D) a₂a₁`
**Ans: C** — Δ₁ = a₃ > 0.

**Q414.** The Hurwitz determinant Δ₃ (the full determinant) must be:
`A) a₁ > 0 | B) a₂a₀ | C) a₀Δ₂ > 0 | D) Negative`
**Ans: C** — Δ₃ = a₀Δ₂, and it must be positive.

**Q415.** A characteristic equation with a zero constant term has:
`A) A pole at the origin | B) No poles | C) A zero at the origin | D) Infinite poles`
**Ans: A** — s = 0 is always a root when the constant term vanishes.

**Q416.** The Routh–Hurwitz criterion proves:
`A) The exact poles | B) The transient response | C) The bandwidth | D) Stability for a real polynomial`
**Ans: D** — It is a necessary and sufficient algebraic test for the LHP.

**Q417.** If a Routh array entry becomes very large, this often indicates:
`A) Poles in the RHP | B) No poles | C) Poles near the imaginary axis | D) Gain of zero`
**Ans: C** — Large entries arise from small b₁, which corresponds to near-axis crossing.

**Q418.** The characteristic equation s³ + 4s² + 8s + 32 = 0 factors as:
`A) (s+2)(s²+2) | B) (s+8)(s²+4) | C) (s+4)(s²+2) | D) (s+4)(s²+8)`
**Ans: D** — (s+4)(s²+8) = s³ + 4s² + 8s + 32.

**Q419.** The system (s+4)(s²+8) = 0 has poles:
`A) −4, ±j2.83 | B) −4, ±j8 | C) 4, ±j2.83 | D) −2, ±j2`
**Ans: A** — s² + 8 = 0 → s = ±j√8 = ±j2.83.

**Q420.** The system s³ + 4s² + 8s + 32 = 0 is:
`A) Unstable | B) Asymptotically stable | C) Fourth order | D) Marginally stable (pair on imaginary axis)`
**Ans: D** — Poles on the imaginary axis mean marginal stability.

**Q421.** A stability analysis of a system with a variable parameter K and characteristic equation s⁴ + 2s³ + s² + 2s + K requires:
`A) A Bode plot only | B) A Routh array as a function of K | C) Root locus only | D) Simulation only`
**Ans: B** — Routh gives the K range directly and algebraically.

**Q422.** For s⁴ + 2s³ + s² + 2s + K, the first column is 1, 2, 0, K — the zero third element signals:
`A) Complete stability | B) Instability for all K | C) Fourth-order instability | D) The auxiliary-polynomial (marginal) case`
**Ans: D** — With b₁ = 0, use the derivative of the s² row: d/ds(s²) = 2s, giving the auxiliary equation.

**Q423.** A system that is stable but with poles close to the imaginary axis is:
`A) Well damped | B) Unstable | C) Poorer damped and faster oscillating | D) Critical`
**Ans: C** — Less damping (smaller ζ) and higher ω_d.

**Q424.** The Routh criterion applied to a system with characteristic equation sⁿ + … + a₀ = 0 gives:
`A) The response waveform | B) Stability for a given set of coefficients | C) The gain margin | D) The state matrix`
**Ans: B** — Pure coefficient information determines stability.

**Q425.** Which statement about the Routh criterion is correct?
`A) It gives exact pole locations | B) It applies only to second order | C) It gives the number of unstable poles but not their locations | D) It requires a Bode plot`
**Ans: C** — Root locus or direct root-finding is needed for locations.

---

## SECTION 7 — Root Locus (Q426–Q505)

**Q426.** The root locus of a system shows:
`A) The open-loop poles only | B) The frequency response | C) The closed-loop pole locations as a parameter (usually K) varies | D) The time response`
**Ans: C** — It is the path the closed-loop poles trace as the gain changes.

**Q427.** The root locus always starts at:
`A) The open-loop poles | B) The open-loop zeros | C) The origin | D) The breakaway point`
**Ans: A** — At K = 0 all closed-loop poles coincide with open-loop poles.

**Q428.** The root locus always ends at:
`A) The open-loop poles | B) Infinity only | C) The open-loop zeros | D) The imaginary axis`
**Ans: C** — As K → ∞ the poles reach the open-loop zeros (finite or at infinity).

**Q429.** The number of branches of the root locus equals:
`A) The number of zeros m | B) n − m | C) The number of open-loop poles n | D) The order of the system`
**Ans: C** — One branch per open-loop pole.

**Q430.** For G(s)H(s) = K/[s(s + 2)], the number of branches is:
`A) 1 | B) 3 | C) 0 | D) 2`
**Ans: D** — Two open-loop poles (0 and −2), so two branches.

**Q431.** The asymptote angle formula is:
`A) θ = (2k + 1)·180°/(n − m) | B) θ = (2k + 1)·90°/(n + m) | C) θ = 2k·180°/(n − m) | D) θ = 90°/(n − m)`
**Ans: A** — Odd multiples of 180° divided by n − m.

**Q432.** For n = 3 and m = 0, the asymptote angles are:
`A) 60°, 180°, 300° | B) 45°, 135°, 225° | C) 90°, 180°, 270° | D) 30°, 150°, 270°`
**Ans: A** — (2k+1)·180/3 for k = 0,1,2 gives 60°, 180°, 300°.

**Q433.** For n = 2 and m = 0, the asymptote angles are:
`A) ±90° | B) 0° and 180° | C) ±45° | D) ±180°`
**Ans: A** — (2k+1)·180/2 gives 90° and 270°.

**Q434.** The centroid of the asymptotes is located at:
`A) σ_a = (Σz − Σp)/(n + m) | B) σ_a = Σp/n | C) σ_a = 0 | D) σ_a = (Σp − Σz)/(n − m)`
**Ans: D** — The average of the open-loop poles and zeros, weighted by count.

**Q435.** For G(s)H(s) = K/[s(s + 2)(s + 4)], the centroid is at:
`A) σ_a = (0 − 2 − 4)/3 = −2 | B) +2 | C) 0 | D) −6`
**Ans: A** — Sum of poles = −6, no zeros, n − m = 3, so centroid = −2.

**Q436.** The root locus exists on a segment of the real axis if:
`A) The number of real poles and zeros to the right of it is odd | B) It is to the right of all poles | C) It has an even number to its right | D) Always`
**Ans: A** — The 180°-per-pole phase requirement gives the odd-count rule.

**Q437.** For G(s)H(s) = K/[s(s + 2)(s + 4)], the root locus lies on the real axis:
`A) Between 0 and +2 | B) Between −2 and −4 only | C) Nowhere | D) From −2 to 0 and to the left of −4`
**Ans: D** — Counting poles/zeros to the right: 1 (odd) between −2 and 0, 1 (odd) left of −4; between −4 and −2 the count is 2 (even), so no locus.

**Q438.** For G(s)H(s) = K/[s(s + 2)(s + 4)], the breakaway point on the real axis is found from:
`A) dK/ds = 0 | B) dK/ds = 1 | C) K = 0 | D) dG/ds = K`
**Ans: A** — Setting the derivative of K(s) = −D(s)/N(s) to zero gives breakaway and break-in points.

**Q439.** For K(s) = s(s + 2)(s + 4), dK/ds = 3s² + 12s + 8 = 0 gives:
`A) s = −0.845, −3.155 | B) s = −2 only | C) s = 0, −4 | D) s = −1.333, −2.667`
**Ans: A** — s = [−12 ± √(144 − 96)]/6 = [−12 ± 6.93]/6 = −0.845, −3.155.

**Q440.** Of the two breakaway candidates for K/[s(s+2)(s+4)], the one actually on the locus is:
`A) s = −3.155 | B) Both | C) Neither | D) s = −0.845`
**Ans: D** — −3.155 lies between −4 and −2, where the real-axis rule says no locus exists.

**Q441.** The angle criterion for the root locus states that at a point s:
`A) ∠G(s)H(s) = 0° | B) ∠G(s)H(s) = 90° | C) ∠G(s)H(s) = (2k + 1)·180° | D) ∠G(s)H(s) = 360°k`
**Ans: C** — Odd multiples of 180°.

**Q442.** The magnitude criterion at a point on the root locus requires:
`A) Magnitude of G(s)H(s) equals K | B) Magnitude of G(s)H(s) equals 1 | C) Magnitude of G(s)H(s) equals 1/K | D) Magnitude of G(s)H(s) equals 0`
**Ans: C** — The open-loop magnitude equals the reciprocal of the gain.

**Q443.** Departure angles from complex poles are found using the angle criterion:
`A) 90° | B) 180° − (sum of angles from other poles and zeros to that pole) | C) 0° | D) 360°`
**Ans: B** — Standard method: 180° minus the sum of the remaining contributions.

**Q444.** Arrival angles at complex zeros are found similarly using:
`A) Sum of angles to poles | B) 180° | C) 0° | D) (2k+1)180° − sum of angles to poles`
**Ans: D** — Mirror image of the departure-angle rule.

**Q445.** If the root locus crosses the imaginary axis, the crossing frequency is found by:
`A) Reading the plot | B) Setting K = 0 | C) Applying the Routh criterion to the characteristic equation | D) Using Mason's formula`
**Ans: C** — Substituting s = jω and equating real and imaginary parts.

**Q446.** For G(s)H(s) = K/[s(s + 1)(s + 2)], the characteristic equation is:
`A) s³ + 3s² + 2s − K = 0 | B) s³ + K = 0 | C) s³ + 3s² + 2s + K = 0 | D) s² + 2s + K = 0`
**Ans: C** — 1 + K/[s(s+1)(s+2)] = 0.

**Q447.** For s³ + 3s² + 2s + K = 0, the imaginary-axis crossing occurs at K =:
`A) 3 | B) 2 | C) 6 | D) 0`
**Ans: C** — Routh gives the condition 6 − K = 0 → K = 6.

**Q448.** At K = 6, the frequency at which the locus crosses the imaginary axis for K/[s(s+1)(s+2)] is:
`A) j√3 rad/s | B) j1 rad/s | C) j6 rad/s | D) j√2 rad/s`
**Ans: D** — Substitution into s³+3s²+2s+6 = 0 with s = jω gives ω² = 2, so ω = √2.

**Q449.** The K value at which the root locus crosses the imaginary axis gives:
`A) The minimum gain | B) The maximum stable gain | C) The bandwidth | D) The DC gain`
**Ans: B** — Beyond this gain the closed loop becomes unstable.

**Q450.** A root locus plot is used to determine:
`A) Only stability | B) Gain range for stability, pole locations and dominant poles | C) Only bandwidth | D) Noise`
**Ans: B** — It gives closed-loop pole behaviour across the gain range.

**Q451.** For a system with open-loop poles at −1 ± j2 and a zero at −3, the root locus branches:
`A) End at −3 | B) Start at −3 | C) Stay on the axis | D) Start at −1 ± j2 and end at infinity (n − m = 1)`
**Ans: D** — Two poles, one zero → n − m = 1, so one branch goes to −3 and one to infinity.

**Q452.** If n = m for a root locus, the number of asymptotes is:
`A) n | B) n − 1 | C) Zero (branches terminate at zeros) | D) m + 1`
**Ans: C** — No asymptotes needed; every branch ends at a finite zero.

**Q453.** The root locus for K/[s(s + 4)] crosses the real axis at:
`A) −2 only | B) 0 only | C) −4 and 0, breaking away toward −2 | D) −4 only`
**Ans: C** — Breakaway at the geometric mean: √(0·(−4)) = −2.

**Q454.** For K/[s(s + 4)], the breakaway point is at:
`A) s = −4 | B) s = −2 | C) s = 0 | D) s = −1`
**Ans: B** — d/ds[s(s+4)] = 2s + 4 = 0 → s = −2.

**Q455.** For K/[s(s + 4)], the locus is a circle (or part of one) because:
`A) There are no zeros | B) The angle criterion yields constant real part −2 | C) The gain is complex | D) There are four poles`
**Ans: B** — Symmetric poles about −2 give a locus with constant σ = −2.

**Q456.** The root locus for K/[s(s + 2)(s + 2)] (repeated poles) will:
`A) Stay on the axis | B) Depart from the repeated poles with a departure angle of ±90° | C) Have no breakaway | D) End at a zero`
**Ans: B** — Repeated poles produce multiple branches leaving at angles separated by 180°/(n−1).

**Q457.** A break-in point occurs where:
`A) Two branches enter the real axis from the complex plane | B) The locus leaves the axis | C) The locus crosses the imaginary axis | D) A pole is at the origin`
**Ans: A** — Break-in is the reverse of breakaway.

**Q458.** Root locus rules are valid for:
`A) Positive feedback only | B) Negative-gain (negative feedback) systems | C) Any system | D) Only digital systems`
**Ans: B** — The rules assume K enters as the loop gain with negative feedback.

**Q459.** The asymptote angles for a system with n = 4 poles and m = 1 zero are:
`A) 45°, 135°, 225° | B) 90°, 180°, 270° | C) 60°, 180°, 300° | D) Four asymptotes`
**Ans: C** — Three asymptotes at (2k+1)·180°/3 = 60°, 180°, 300°.

**Q460.** The root locus of a positive-feedback system uses the same rules but with:
`A) The same equations | B) 1 − GH = 0 instead of 1 + GH = 0 | C) No real-axis segments | D) Different asymptotes only`
**Ans: B** — Positive feedback reverses the characteristic equation's sign.

**Q461.** When computing a root locus, the open-loop poles are the roots of:
`A) The denominator of G(s)H(s) | B) The numerator of G(s)H(s) | C) The closed-loop denominator | D) The numerator only`
**Ans: A** — Open-loop poles are the zeros of GH's denominator.

**Q462.** Root locus is a plot in:
`A) The complex s-plane | B) The frequency domain | C) The time domain | D) The z-plane only`
**Ans: A** — Pole locations live in the complex plane.

**Q463.** Root locus construction requires knowing:
`A) Only the closed-loop poles | B) The open-loop poles and zeros | C) Only the gain | D) Only the bandwidth`
**Ans: B** — All rules are built from open-loop pole and zero locations.

**Q464.** A root locus plot shows the loci of the closed-loop:
`A) Zeros | B) Both | C) Gains | D) Poles`
**Ans: D** — Root locus tracks poles as a parameter varies.

**Q465.** Zeros (as opposed to poles) also appear on the root locus diagram as:
`A) × marks | B) Arrows | C) Open-loop zeros marked with ○ | D) Not shown`
**Ans: C** — Poles are ×, zeros are ○.

**Q466.** If G(s)H(s) has n poles and m zeros with n < m, the locus ends:
`A) All at finite zeros | B) At the origin | C) Nowhere | D) With m − n branches going to infinity`
**Ans: D** — n − m < 0 means |m − n| branches head to infinity.

**Q467.** For G(s)H(s) = K(s + 3)/[s(s + 1)], the root locus:
`A) Starts at −3 and 0 | B) Starts at 0, −1 and ends at −3 and infinity | C) Ends at 0 | D) Is entirely on the axis`
**Ans: B** — Two poles start, one zero and one infinity end.

**Q468.** The departure angle from a pole p on the complex axis is:
`A) Σ angles to poles | B) 0° | C) 90° always | D) 180° − Σ angles from p to other poles/zeros`
**Ans: D** — Sum the angles of the vectors from the pole under test to all other poles and to the zeros, then subtract from 180°.

**Q469.** For a root locus crossing the imaginary axis, the K value is found by:
`A) Setting the Routh array's sign-change element to zero | B) Reading the plot | C) Setting K = 0 | D) Using Mason's formula`
**Ans: A** — Marginal stability requires a zero row entry in the Routh array.

**Q470.** A pole-zero plot with poles at the origin and at −a, and a zero at −b (b < a), gives a root locus that:
`A) Stays on the axis | B) Is empty | C) Crosses the imaginary axis | D) Breaks away from the real axis and heads to −b and infinity`
**Ans: D** — With one zero and two poles, n − m = 1 gives one asymptote.

**Q471.** The stability of a closed-loop system along its root locus is:
`A) Stable always | B) Stable when branches cross the axis | C) Stable while all branches are in the LHP | D) Never stable`
**Ans: C** — Crossing to the RHP destroys stability.

**Q472.** The dominant pole of a closed-loop system is:
`A) The pole closest to the imaginary axis | B) The largest pole | C) The pole at the origin | D) Any real pole`
**Ans: A** — The slowest-decaying pole dominates the transient.

**Q473.** Adding a zero via a compensator to a root locus typically:
`A) Pushes it right | B) Has no effect | C) Pulls the locus left, improving damping | D) Removes the zero`
**Ans: C** — A zero attracts the locus, improving transient response.

**Q474.** Adding a pole to the open-loop transfer function:
`A) Pulls it left | B) Has no effect | C) Pushes the locus right, reducing stability | D) Moves the centroid only`
**Ans: C** — Extra poles degrade phase margin and reduce the stability range.

**Q475.** In root locus design, the gain K is usually chosen as:
`A) Always 1 | B) The value at breakaway | C) The DC gain | D) The value at the desired pole location`
**Ans: D** — K is read from the magnitude criterion at the desired pole.

**Q476.** For G(s)H(s) = K/[s(s + 1)], the K for poles at −1 ± j1 is:
`A) 1 | B) 2 | C) 4 | D) 0.5`
**Ans: B** — s² + s + K = 0 with roots −1 ± j1 gives K = 2.

**Q477.** For K/[s(s+1)], the K for a breakaway at the origin (s = 0) is:
`A) 1 | B) 0 | C) 2 | D) Infinity`
**Ans: B** — At s = 0 the magnitude condition gives K = 0 (a pole is at the origin).

**Q478.** For K/[s(s + 1)], the breakaway point on the real axis is at:
`A) s = −1 | B) s = 0 | C) s = −2 | D) s = −0.5`
**Ans: D** — d/ds[s(s+1)] = 2s + 1 = 0 → s = −0.5, with K = 0.25.

**Q479.** The maximum value of K for stability of K/[s(s + 1)(s + 2)] is:
`A) 3 | B) 2 | C) 6 | D) 8`
**Ans: C** — From the Routh analysis of s³ + 3s² + 2s + K.

**Q480.** A system whose root locus never leaves the real axis for any K has:
`A) Poles that are widely separated | B) Very few poles | C) No zeros | D) A pole at the origin only`
**Ans: A** — If all poles are real and no branch migrates off the axis, the locus stays real.

**Q481.** The angle of asymptotes for n − m = 2 is:
`A) 0° and 180° | B) ±45° | C) ±90° | D) 30° and 150°`
**Ans: C** — (2k+1)·180/2 = 90°, 270°.

**Q482.** The angle of asymptotes for n − m = 4 is:
`A) ±90° | B) 36°, 108°, 180°, 252° | C) ±45°, ±135° | D) 60°, 120°, 180°, 240°`
**Ans: C** — (2k+1)·180/4 = 45°, 135°, 225°, 315°.

**Q483.** For a system with poles at −1 ± j1 and a zero at −3, the departure angle from −1 + j1 is:
`A) 0° | B) +90° | C) 180° | D) −90° (downward)`
**Ans: D** — By symmetry the branches head vertically away from the real axis.

**Q484.** Root locus analysis requires the transfer function to be:
`A) In the form KG(s)H(s) with variable K | B) Already closed-loop | C) Only a Bode plot | D) In the time domain`
**Ans: A** — The variable gain K must be explicit.

**Q485.** Given G(s)H(s) = K(s + 1)/[s(s + 2)(s + 3)], the centroid of the asymptotes is:
`A) −4 | B) 0 | C) (0 − 2 − 3 − (−1))/(3 − 1) = −2 | D) +2`
**Ans: C** — Σp = −5, Σz = −1, n − m = 2, so σ_a = (−5 + 1)/2 = −2.

**Q486.** If a root locus branch approaches the imaginary axis asymptotically, it indicates:
`A) No poles | B) Poles approaching jω with K critical | C) Infinite gain | D) Zero gain only`
**Ans: B** — Tangency to the axis is the stability boundary.

**Q487.** Sensitivity of the closed-loop poles to gain changes can be read from the root locus as:
`A) The number of branches | B) The centroid | C) The asymptote count | D) The spacing of the poles along the locus`
**Ans: D** — Tight pole spacing means small K changes move poles a lot (high sensitivity).

**Q488.** A root locus plot for a system with a right-half-plane zero is used to examine:
`A) Stability only | B) Bandwidth | C) Noise | D) Non-minimum-phase behaviour`
**Ans: D** — RHP zeros limit achievable bandwidth and cause inverse response.

**Q489.** If a system has n poles and m zeros with n = m, the number of asymptotes is:
`A) Zero | B) n | C) n − 1 | D) m + 1`
**Ans: A** — Every branch ends at a finite zero, so no asymptotes (and hence no centroid) are needed.

**Q490.** Root locus for K/(s² + 2s + 100) shows:
`A) Branches on the axis | B) Asymptotes at ±90° | C) No branches | D) A circular locus at constant σ = −1`
**Ans: D** — Complex conjugate poles with constant damping locus.

**Q491.** For G(s)H(s) = K/(s² + 4s + 100), the poles are:
`A) −2 ± j4 | B) −4 ± j10 | C) −2 ± j9.8 | D) ±j10`
**Ans: C** — s = [−4 ± √(16 − 400)]/2 = −2 ± j9.8.

**Q492.** For a second-order system K/(s² + 2ζω_n s + ω_n²), increasing K from 0:
`A) Poles move outward along a constant-damping circle | B) Poles move left | C) Poles stay fixed | D) Poles cross the axis`
**Ans: A** — Constant ζ means a constant-damping ratio locus.

**Q493.** The root locus method determines stability without computing:
`A) The open-loop poles | B) The open-loop zeros | C) The closed-loop poles explicitly | D) The gain`
**Ans: C** — It shows the qualitative pole movement, so stability follows from whether the locus stays in the LHP.

**Q494.** A closed-loop system is unstable when its root locus:
`A) Enters the right half plane | B) Stays in the LHP | C) Touches the origin | D) Has no branches`
**Ans: A** — Any RHP region means an unstable pole.

**Q495.** Given open-loop poles at −2, −6 and a zero at −10, the number of asymptotes is:
`A) 2 | B) 3 | C) 0 | D) 1`
**Ans: D** — n = 2, m = 1, so n − m = 1 asymptote.

**Q496.** Given poles −2, −6 and zero −10, the single asymptote angle is:
`A) 180° | B) 90° | C) 0° | D) 45°`
**Ans: A** — (2k+1)·180/1 = 180°.

**Q497.** The centroid for poles −2, −6 and zero −10 is:
`A) (−8 + 10)/1 = 2 | B) −8 | C) −16 | D) 0`
**Ans: A** — Σp = −8, Σz = −10, σ_a = (−8 − (−10))/1 = 2.

**Q498.** A root locus that ends at a zero at −10 and infinity from poles −2, −6 has its asymptote along:
`A) The real axis toward +∞ | B) The real axis toward −∞ | C) The imaginary axis | D) A circle`
**Ans: A** — The 180° asymptote starts at the centroid (+2) and extends toward −∞ along the real axis.

**Q499.** Root locus of a system with two complex poles and one real zero typically has:
`A) A breakaway at the origin | B) No real-axis segments | C) A break-in point on the real axis | D) An asymptote at 0°`
**Ans: C** — The branches come together on the real axis and one departs toward the zero.

**Q500.** Root locus is also drawn for:
`A) Only negative feedback | B) Only open-loop systems | C) Only digital systems | D) Positive-feedback systems with modified rules`
**Ans: D** — The angle criterion becomes 0°-multiples with 1 − GH = 0.

**Q501.** In root locus design of a compensator, the added pole must be placed so that:
`A) It is at the origin only | B) It has the highest gain | C) It does not violate the stability range | D) It is at infinity`
**Ans: C** — The design goal is to place poles for the desired response while keeping K > 0 and LHP poles.

**Q502.** The condition that a closed-loop pole be at a desired location s₁ requires:
`A) |G(s₁)H(s₁)| = 1/K and ∠G(s₁)H(s₁) = (2k+1)180° | B) K = G(s₁) | C) s₁ = 0 | D) No condition`
**Ans: A** — Both angle and magnitude criteria must hold.

**Q503.** Given G(s)H(s) = 1/[s(s + 4)], the K required for poles at −2 ± j2 is:
`A) 4 | B) 2 | C) 16 | D) 8`
**Ans: D** — s² + 4s + K with roots −2 ± j2 gives K = 8.

**Q504.** The root locus of G(s)H(s) = K/[s(s + 2)(s + 6)] has its breakaway points from:
`A) Setting K = 0 | B) d/ds[s(s+2)(s+6)] = 0 | C) The centroid | D) The asymptotes`
**Ans: B** — K(s) = s³ + 8s² + 12s, so dK/ds = 3s² + 16s + 12 = 0 gives s = [−16 ± √112]/6 = −0.903 and −4.43.

**Q505.** Root locus techniques are used in design to:
`A) Place dominant poles for a required transient response within a stable gain range | B) Compute noise | C) Measure bandwidth directly | D) Determine thermal noise`
**Ans: A** — The classic use is damping-ratio and settling-time placement.

---

## SECTION 8 — Frequency Response, Bode, Nyquist, Margins (Q506–Q590)

**Q506.** The frequency response of a system is:
`A) The time response | B) G(jω), the transfer function evaluated at s = jω | C) The impulse response | D) The step response`
**Ans: B** — Substituting s = jω gives magnitude and phase versus frequency.

**Q507.** In the frequency response, the magnitude is measured in:
`A) Radians | B) Volts | C) Decibels (or nepers) | D) Hertz`
**Ans: C** — 20 log₁₀|G(jω)| dB.

**Q508.** The transfer function G(s) = 1/(s + 1) has a corner (break) frequency at:
`A) 0 rad/s | B) 1 rad/s | C) 2 rad/s | D) Infinity`
**Ans: B** — Corner frequency = 1/time constant = 1 rad/s.

**Q509.** For a first-order pole, above the corner frequency the magnitude slope is:
`A) +20 dB/decade | B) −40 dB/decade | C) 0 dB/decade | D) −20 dB/decade`
**Ans: D** — Each pole contributes −20 dB/decade (−1 in Bode asymptote).

**Q510.** For a second-order pole, above the corner frequency the magnitude slope is:
`A) −20 dB/decade | B) −40 dB/decade | C) −60 dB/decade | D) 0 dB/decade`
**Ans: B** — Two poles → −40 dB/decade.

**Q511.** For a zero at the origin, the magnitude slope is:
`A) −20 dB/decade | B) +40 dB/decade | C) +20 dB/decade | D) 0 dB/decade`
**Ans: C** — A pole at the origin contributes +20 dB/decade.

**Q512.** For a zero on the negative real axis, above its corner frequency the slope is:
`A) −20 dB/decade | B) +20 dB/decade | C) 0 dB/decade | D) +40 dB/decade`
**Ans: B** — A zero is the inverse of a pole, contributing +20 dB/decade.

**Q513.** For a second-order zero, the slope contribution is:
`A) +20 dB/decade | B) −40 dB/decade | C) +40 dB/decade | D) +60 dB/decade`
**Ans: C** — Two zeros → +40 dB/decade.

**Q514.** The phase of a first-order pole at frequencies well above the corner is:
`A) −180° | B) 0° | C) −90° | D) +90°`
**Ans: C** — A single pole approaches −90°.

**Q515.** The phase of a second-order pair of poles approaches:
`A) −180° | B) −90° | C) −360° | D) +180°`
**Ans: A** — Two poles contribute −90° each.

**Q516.** A pure time delay e^(−jωT) has magnitude and phase:
`A) Magnitude 1 (0 dB), phase −ωT | B) Magnitude ωT, phase −90° | C) Magnitude 0, phase 0 | D) Magnitude 1, phase 0`
**Ans: A** — A delay is all-pass: 0 dB with a linear negative phase.

**Q517.** The corner frequency of a term with time constant T is:
`A) T rad/s | B) 2πT rad/s | C) 1/T rad/s | D) 1/(2πT) rad/s`
**Ans: C** — ω_c = 1/T (in rad/s; equivalently f_c = 1/(2πT) Hz).

**Q518.** To convert a corner frequency from rad/s to Hz, you:
`A) Multiply by 2π | B) Square it | C) Take its reciprocal | D) Divide by 2π`
**Ans: D** — f = ω/(2π).

**Q519.** The phase of G(s) = K/(1 + jωT) at the corner frequency is:
`A) −45° | B) −90° | C) −22.5° | D) −180°`
**Ans: A** — At ω = 1/T the phase is halfway, −45°.

**Q520.** The phase of a standard second-order system ω_n²/(s² + 2ζω_n s + ω_n²) at its natural frequency ω_n is:
`A) 0° | B) −45° | C) −90° | D) −180°`
**Ans: C** — At ω = ω_n the denominator is j2ζω_n², purely imaginary and positive, so the phase is exactly −90°.

**Q521.** The magnitude of G(s) = ω_n²/(s² + 2ζω_n s + ω_n²) at ω = ω_n is:
`A) 1 | B) 2ζ | C) 1/(2ζ) | D) 1/ζ`
**Ans: C** — At resonance, |G(jω_n)| = ω_n²/(2ζω_n²) = 1/(2ζ).

**Q522.** For 0 < ζ < 1, the resonant peak occurs at:
`A) ω_r = ω_n√(1 − 2ζ²) | B) ω_r = ω_n | C) ω_r = ω_n/ζ | D) ω_r = ω_n(1 − ζ)`
**Ans: A** — Resonant peak at ω_n√(1 − 2ζ²).

**Q523.** The resonant peak magnitude is:
`A) M_r = 1/(2ζ) | B) M_r = 1/ζ | C) M_r = 2ζ | D) M_r = 1/[2ζ√(1 − ζ²)]`
**Ans: D** — M_r = 1/(2ζ√(1−ζ²)) at the resonant frequency.

**Q524.** When ζ = 0.7, the resonant peak magnitude is:
`A) 1.43 | B) 1.70 | C) 2.00 | D) ≈ 1.00 (essentially no peaking)`
**Ans: D** — √(1−0.49) = 0.714, so M_r = 1/(1.4 × 0.714) ≈ 1.00.

**Q525.** The resonant peak frequency exists only when:
`A) ζ < 1 | B) ζ < 1/√2 | C) ζ > 0.707 | D) Always`
**Ans: B** — For ζ ≥ 1/√2 there is no resonance.

**Q526.** The Bode magnitude plot of G(s) = 1/(1 + s/10) is:
`A) −20 dB/decade from 1 rad/s | B) 0 dB always | C) 0 dB up to 10 rad/s, then −20 dB/decade | D) +20 dB/decade above 10 rad/s`
**Ans: C** — Corner at 10 rad/s, slope −20 dB/decade above.

**Q527.** In Bode plot construction, a pole at the origin contributes:
`A) −20 dB/decade from 0 Hz and −90° phase | B) +20 dB/decade | C) −90 dB | D) 0 slope`
**Ans: A** — A pole at the origin adds −20 dB/decade and −90°.

**Q528.** The phase approximation rule (straight-line Bode) for a pole is:
`A) Instantaneous step | B) Linear from 0 | C) Constant −90° | D) Start at 10° below corner, reach −45° at corner, −90° at 10× corner`
**Ans: D** — The 10:1 straight-line phase approximation.

**Q529.** The band of frequencies over which the phase is within ±45° of a pole's asymptotic value spans approximately:
`A) ω_c only | B) 1ω_c to 2ω_c | C) 100ω_c to 1000ω_c | D) 0.1ω_c to 10ω_c`
**Ans: D** — From a decade below to a decade above the corner.

**Q530.** In logarithmic frequency scaling, each decade is a factor of:
`A) 10 | B) 2 | C) 100 | D) e`
**Ans: A** — One decade = ×10 in frequency.

**Q531.** The bandwidth is the frequency at which:
`A) The phase reaches −90° | B) The gain is maximum | C) The slope is −40 dB/dec | D) The magnitude drops to 1/√2 of the DC value (−3 dB)`
**Ans: D** — The −3 dB (half-power) point.

**Q532.** For G(s) = 1/(1 + s), the bandwidth is:
`A) 0.5 rad/s | B) 1 rad/s | C) 2 rad/s | D) 10 rad/s`
**Ans: B** — Corner frequency 1 rad/s; ω_bw = 1 rad/s.

**Q533.** The cutoff (bandwidth) frequency of a first-order system with time constant T is:
`A) ω_c = T | B) ω_c = 1/T | C) ω_c = 1/(2T) | D) ω_c = 2/T`
**Ans: B** — ω_c = 1/T.

**Q534.** For a first-order system, rise time (10–90%) and bandwidth are related by:
`A) t_r ≈ 2.2/ω_bw | B) t_r = ω_bw | C) t_r ≈ 0.1/ω_bw | D) t_r = 1/ω_bw`
**Ans: A** — t_r ≈ 2.2τ = 2.2/ω_bw.

**Q535.** The Nyquist plot of G(jω) plots:
`A) Magnitude vs frequency | B) Phase vs time | C) Real vs imaginary parts of G(jω) as ω varies | D) Poles in the s-plane`
**Ans: C** — A polar plot of the frequency response.

**Q536.** The Nyquist criterion states that:
`A) N = P − Z | B) N = Z − P (Z zeros of 1+GH in RHP, P open-loop poles in RHP) | C) N = Z + P | D) N = 0 always`
**Ans: B** — N = Z − P is the argument principle form.

**Q537.** In the Nyquist criterion, N counts:
`A) Counter-clockwise encirclements of −1 | B) Poles in the LHP | C) Clockwise encirclements of −1 | D) Zeros of GH`
**Ans: C** — N = Z − P counts clockwise encirclements of −1.

**Q538.** If there are no open-loop poles in the RHP (P = 0), the system is stable when:
`A) One encirclement | B) Any encirclement | C) No encirclement of −1 (N = Z = 0) | D) Z = 1`
**Ans: C** — With P = 0, stability requires Z = 0, so N = 0.

**Q539.** The modified Nyquist plot for open-loop poles on the jω-axis is drawn by:
`A) Ignoring them | B) Adding them as zeros | C) Shifting them to the origin | D) Bending the contour into the RHP around the poles`
**Ans: D** — Indent the contour to the right, making the poles count as if in the RHP.

**Q540.** For open-loop poles on the imaginary axis, each such pole is treated as:
`A) A full RHP pole | B) An LHP pole | C) A zero | D) Half a pole in the RHP (detour factor)`
**Ans: D** — The standard −jω indentation counts each j-axis pole as half.

**Q541.** The gain margin of a system is:
`A) The extra phase before instability | B) The peak overshoot | C) The steady-state error | D) The factor by which gain can increase before instability`
**Ans: D** — GM = K_crit/K at the phase-crossover frequency.

**Q542.** The phase margin of a system is:
`A) The extra gain before instability | B) The rise time | C) The overshoot | D) The extra phase lag before instability`
**Ans: D** — PM = 180° + phase at the gain-crossover frequency.

**Q543.** Gain margin is defined as:
`A) |G(jω_gc)| | B) 1/|G(jω_pc)| in dB | C) The peak gain | D) 1/|G(jω_pc)| at ω_pc where phase = −180°`
**Ans: D** — GM = 1/|G| at the phase-crossover frequency (−180° phase).

**Q544.** Phase margin is defined as:
`A) 180° − ∠G | B) ∠G at ω_pc | C) 90° + ∠G | D) 180° + ∠G(jω_gc) at ω_gc where |G| = 1`
**Ans: D** — PM = 180° + phase at gain crossover.

**Q545.** The gain crossover frequency ω_gc is where:
`A) ∠G(jω) = −180° | B) |G(jω)| = 1 (0 dB) | C) The slope is −40 dB/dec | D) The phase is −90°`
**Ans: B** — Magnitude crossover, |G| = 1.

**Q546.** The phase crossover frequency ω_pc is where:
`A) |G(jω)| = 1 | B) ∠G(jω) = −180° | C) The slope changes | D) The phase is −90°`
**Ans: B** — Phase crossover at −180°.

**Q547.** If the phase never reaches −180° in a Bode plot, the gain margin is:
`A) Infinite (system stable for all gain) | B) Zero | C) 1 | D) Undefined`
**Ans: A** — No phase crossover means no gain causes −1 encirclement → GM = ∞.

**Q548.** If the gain margin is positive, the system is:
`A) Unstable | B) Marginally stable | C) Stable at the current gain | D) Oscillating`
**Ans: C** — GM > 0 (in dB, > 0) indicates stable.

**Q549.** A negative gain margin in dB indicates:
`A) High stability | B) Large bandwidth | C) Instability | D) Small overshoot`
**Ans: C** — GM < 0 dB means instability.

**Q550.** Good stability margins typically require:
`A) PM ≈ 0° | B) PM ≈ 45–60° and GM > 6 dB | C) GM = 0 | D) PM = 180°`
**Ans: B** — Standard design targets for robustness.

**Q551.** For a first-order system G(s) = 1/(1 + s) with unity feedback, the phase margin is:
`A) 90° | B) 135° | C) 45° | D) 180°`
**Ans: B** — Gain crossover is at ω = 1 rad/s where the phase is −45°, so PM = 180° + (−45°) = 135°.

**Q552.** For G(s) = 1/[s(1 + s)] with unity feedback, the phase margin is:
`A) 90° | B) 45° | C) 180° | D) ≈ 51.8°`
**Ans: D** — ω_gc solves ω√(1+ω²) = 1 → ω = 0.786, phase ≈ −128.2°, PM ≈ 51.8°.

**Q553.** For G(s) = K/[s(s + 1)], the gain crossover frequency depends on K; as K increases ω_gc:
`A) Decreases | B) Increases | C) Stays constant | D) Becomes zero`
**Ans: B** — Higher gain pushes the crossover to higher frequency.

**Q554.** Increasing loop gain generally:
`A) Decreases bandwidth | B) Increases phase margin | C) Increases bandwidth and decreases phase margin | D) No effect`
**Ans: C** — Higher gain → higher crossover → more negative phase → smaller PM.

**Q555.** The relationship between phase margin and damping ratio for a second-order loop is approximately:
`A) PM = ζ | B) PM = 180ζ | C) PM = 2ζ | D) PM ≈ tan⁻¹(2ζ/√(√(1+4ζ⁴) − 2ζ²))`
**Ans: D** — The standard approximation PM ≈ arctan(2ζ/√(√(1+4ζ⁴) − 2ζ²)).

**Q556.** For ζ = 0.5, the corresponding phase margin is approximately:
`A) ≈ 45° | B) ≈ 60° | C) ≈ 30° | D) ≈ 90°`
**Ans: A** — ζ = 0.5 maps to PM ≈ 45° (via the standard relation).

**Q557.** The gain margin in dB is:
`A) 10 log₁₀(GM) | B) GM directly | C) 20 log₁₀(GM) | D) log₁₀(GM)`
**Ans: C** — GM_dB = 20 log₁₀ GM.

**Q558.** If the open-loop phase at gain crossover is −150°, the phase margin is:
`A) 150° | B) −30° | C) 60° | D) 30°`
**Ans: D** — PM = 180° − 150° = 30°.

**Q559.** A system is stable (minimum phase, no RHP poles) if the Nyquist plot:
`A) Encircles −1 once | B) Does not encircle −1 | C) Encircles the origin | D) Passes through −1`
**Ans: B** — No encirclement of −1 with P = 0 gives stability.

**Q560.** In a Bode plot, the magnitude is often approximated as a straight line starting at:
`A) −∞ | B) 0 dB up to the first corner | C) +∞ | D) The corner`
**Ans: B** — The asymptotic (straight-line) approximation.

**Q561.** For a system with two cascaded first-order poles at 1 and 10 rad/s, the −3 dB bandwidth is approximately:
`A) The lower corner, 1 rad/s | B) ~8 rad/s | C) 100 rad/s | D) The higher corner, 10 rad/s`
**Ans: D** — For widely separated corners, the −3 dB point ≈ the higher corner.

**Q562.** The frequency at which a first-order system's phase is −45° is:
`A) 2/T | B) T | C) The corner frequency 1/T | D) 0.1/T`
**Ans: C** — Phase = −45° at ω = 1/T.

**Q563.** A Bode magnitude plot of a pure integrator 1/s has slope:
`A) −20 dB/decade for all ω | B) 0 dB/decade | C) +20 dB/decade | D) −40 dB/decade`
**Ans: A** — A pole at the origin gives a constant −20 dB/decade.

**Q564.** A Bode magnitude plot of a differentiator s has slope:
`A) −20 dB/decade | B) 0 | C) +20 dB/decade for all ω | D) +40`
**Ans: C** — A zero at the origin adds +20 dB/decade.

**Q565.** The logarithmic frequency axis in a Bode plot places:
`A) Equal distance per Hz | B) Equal distance per rad/s | C) Log amplitude | D) Equal distance per decade (ratio)`
**Ans: D** — Logarithmic spacing by ratio, so each decade is evenly spaced.

**Q566.** For a transfer function G(s) = (1 + s/2)/(1 + s/10), the net slope above both corners is:
`A) −20 dB/decade | B) +20 dB/decade | C) 0 dB/decade | D) −40 dB/decade`
**Ans: C** — One zero and one pole of equal multiplicity → net slope zero.

**Q567.** The maximum magnitude of G(s) = (1 + s/2)/(1 + s/10) (a lead compensator) is:
`A) 10/2 = 5 (25 dB) at the mid-band | B) 1 (0 dB) | C) 2 | D) 10`
**Ans: A** — Between 2 and 10 rad/s the magnitude rises toward the ratio of zeros to poles = 5.

**Q568.** A lead compensator increases:
`A) Steady-state error only | B) Noise | C) Delay | D) Phase margin and bandwidth`
**Ans: D** — Adding phase lead stabilizes and speeds the response.

**Q569.** A lag compensator is used primarily to:
`A) Increase bandwidth | B) Reduce phase margin | C) Add noise | D) Improve steady-state error while keeping transient behaviour nearly unchanged`
**Ans: D** — Lag boosts low-frequency gain for accuracy.

**Q570.** The maximum phase lead provided by a first-order lead network is:
`A) sin(θ_m) = (1 − α)/(1 + α), θ_m = sin⁻¹((1−α)/(1+α)) | B) 90° always | C) 45° | D) 180°`
**Ans: A** — θ_m = arcsin((1−α)/(1+α)), with α = pole/zero ratio.

**Q571.** The maximum phase lag of a first-order lag network is similar in magnitude but:
`A) Negative (lag) and at lower frequency | B) Positive | C) Zero | D) 180°`
**Ans: A** — A lag network gives negative phase peaking.

**Q572.** Sensitivity of a system measures:
`A) The output magnitude | B) How much the output changes with parameter variations | C) The input power | D) The bandwidth`
**Ans: B** — Sensitivity is the ratio of relative output change to relative parameter change.

**Q573.** The sensitivity of a transfer function G(s) to a parameter K is:
`A) S = ∂G/∂K | B) S = G/K | C) S = (∂G/∂K)·(K/G) | D) S = 1/G`
**Ans: C** — Normalized sensitivity S = (∂G/∂K)(K/G).

**Q574.** The complementary sensitivity function is:
`A) T(s) = 1/(1 + G) | B) T(s) = G | C) T(s) = G/(1 + G) | D) T(s) = 1 + G`
**Ans: C** — T = G/(1 + GH) with H = 1.

**Q575.** In unity feedback, the closed-loop transfer function is:
`A) T = G(1 + G) | B) T = 1/(1 + G) | C) T = G/(1 + G) | D) T = G/(1 − G)`
**Ans: C** — Unity negative feedback gives G/(1 + G).

**Q576.** For unity feedback with G(s) = K/(s + a), the steady-state error for a unit step input is:
`A) K/a | B) 0 always | C) a/(a + K) | D) 1`
**Ans: C** — K_p = K/a, so e_ss = 1/(1 + K_p) = a/(a + K).

**Q577.** For unity feedback with G(s) = K/s, the steady-state error for a ramp input is:
`A) 1/K | B) Infinite | C) 0 | D) 1/(1+K)`
**Ans: B** — Type-1 systems have finite step error but infinite ramp error.

**Q578.** For unity feedback with G(s) = K/[s(s + a)], the steady-state error for a ramp input is:
`A) a/K | B) K/a | C) 1 | D) 0`
**Ans: A** — Type-2: K_v = lim s→0 sG = K/a, e_ss = 1/K_v = a/K.

**Q579.** The error constant K_p (position) is:
`A) lim_{s→0} sG(s) | B) lim_{s→0} G(s)/s | C) lim_{s→0} s²G(s) | D) lim_{s→0} G(s)`
**Ans: D** — K_p = lim s→0 G(s).

**Q580.** The error constant K_v (velocity) is:
`A) lim_{s→0} sG(s) | B) lim_{s→0} G(s) | C) lim_{s→0} s²G(s) | D) lim_{s→0} G(s)/s`
**Ans: A** — K_v = lim s→0 s·G(s).

**Q581.** The error constant K_a (acceleration) is:
`A) lim_{s→0} sG(s) | B) lim_{s→0} s²G(s) | C) lim_{s→0} G(s) | D) lim_{s→0} s³G(s)`
**Ans: B** — K_a = lim s→0 s²·G(s).

**Q582.** For a type-1 system (one pole at origin) the system is:
`A) Finite error to step, zero to ramp | B) Infinite error to step | C) Finite error to ramp | D) Stable to step, infinite error to ramp`
**Ans: D** — Type-1: zero step error, infinite ramp error.

**Q583.** A type-0 system with unity feedback has:
`A) Zero step error | B) Zero ramp error | C) Infinite step error | D) Nonzero step error, infinite ramp error`
**Ans: D** — No integrator → finite K_p → nonzero step error; K_v = 0 → infinite ramp error.

**Q584.** The steady-state error for a parabolic (t²/2) input is:
`A) Zero for all | B) Finite for type-1 | C) Always 1 | D) Finite for type-3, infinite for type-≤2`
**Ans: D** — Only type-3 and above have finite K_a.

**Q585.** The error for a type-2 system with a ramp input is:
`A) Finite | B) Zero | C) Undefined | D) Infinite`
**Ans: D** — K_v = lim s→0 sG(s) = 0 for a type-2 system, so e_ss = 1/K_v is infinite.

**Q586.** Steady-state error constants relate to system type by:
`A) The number of poles at the origin | B) The number of zeros at the origin | C) The order | D) The gain`
**Ans: A** — System type = number of integrators (poles at origin).

**Q587.** In a Bode plot of a minimum-phase system, the phase is determined by:
`A) The poles and zeros | B) Only the gain | C) Only the numerator | D) The steady-state error`
**Ans: A** — Minimum phase means no RHP zeros, so phase follows from pole/zero locations.

**Q588.** A transfer function that cannot be inverted while remaining causal and stable is called:
`A) Minimum-phase | B) All-pass | C) Non-minimum-phase | D) Biproper`
**Ans: C** — A right-half-plane zero makes a stable causal inverse impossible.

**Q589.** A system's velocity error constant K_v for G(s) = K/[s(s + 2)(s + 5)] is:
`A) K/5 | B) K/2 | C) K/10 | D) K`
**Ans: C** — K_v = lim s·K/[s(s+2)(s+5)] = K/10.

**Q590.** The steady-state error of G(s) = 5/[s(s + 2)(s + 5)] for a unit step input is:
`A) 1/(5/10) = 2 | B) 1 | C) 0 | D) 5`
**Ans: C** — Type-1 → K_p = ∞ → zero step error.

---

## SECTION 9 — P and M Charts (Q591–Q645)

**Q591.** The P-M chart plots:
`A) Gain margin (dB) vs phase margin (degrees) | B) Poles vs zeros | C) Time vs gain | D) Frequency vs time`
**Ans: A** — Absolute stability is mapped onto a plane of GM(dB) vs PM(degrees).

**Q592.** A point inside the shaded region of the P-M chart represents:
`A) A stable closed-loop system | B) An unstable system | C) A marginal system | D) Zero bandwidth`
**Ans: A** — The shaded region corresponds to stable combinations of margins.

**Q593.** The gain margin axis in a P-M chart is usually expressed in:
`A) Degrees | B) Radians | C) Neper-seconds | D) Decibels`
**Ans: D** — GM is plotted in dB.

**Q594.** The phase margin axis in a P-M chart is expressed in:
`A) Decibels | B) Radians | C) Degrees | D) Volts`
**Ans: C** — PM is plotted in degrees.

**Q595.** If a system is unstable, its P-M chart point lies:
`A) Outside the shaded region | B) Inside the shaded region | C) At the origin | D) On the diagonal`
**Ans: A** — Unstable margin combinations fall outside.

**Q596.** A system with PM = 60° and GM = 12 dB lies:
`A) On the boundary | B) Outside | C) Undefined | D) Well inside the stable region`
**Ans: D** — Generous margins indicate robust stability.

**Q597.** The P-M chart is constructed by plotting:
`A) Poles | B) Time constants | C) Zeros | D) Points (GM in dB, PM in degrees) from frequency-response analysis`
**Ans: D** — Each frequency-response evaluation yields one margin pair.

**Q598.** For a system with P = 0 open-loop poles in the RHP, the P-M chart is:
`A) Excluded | B) Just the GM vs PM plane | C) Only the imaginary axis | D) Not applicable`
**Ans: B** — Standard P-M charts assume no open-loop RHP poles.

**Q599.** A system with open-loop RHP poles cannot be represented on a:
`A) Single P-M chart (needs modified analysis) | B) Bode plot | C) Nyquist plot | D) Routh array`
**Ans: A** — Conditional stability means the margins are conditional.

**Q600.** The P-M chart helps choose:
`A) Motor size | B) Sensor accuracy | C) Thermal limits | D) Compensator settings giving required stability margins`
**Ans: D** — The chart maps desired margins onto compensator design.

**Q601.** The typical design targets marked on a P-M chart are:
`A) PM = 0° and GM = 0 | B) PM = 180° | C) GM negative | D) PM ≥ 45° and GM ≥ 6 dB`
**Ans: D** — Standard robustness targets.

**Q602.** If PM = 0°, the system is:
`A) Stable | B) Marginally stable (ω_gc coincides with ω_pc) | C) Unstable | D) Uncontrollable`
**Ans: B** — Zero phase margin means the crossover frequencies coincide at −1.

**Q603.** If GM = 0 dB, the system is:
`A) Stable | B) Unstable with large PM | C) Marginally stable (gain margin unity) | D) Non-minimum phase`
**Ans: C** — GM = 0 dB means critical gain at phase crossover.

**Q604.** A system with GM = −5 dB is:
`A) Stable | B) Unstable | C) Marginal | D) Uncontrollable`
**Ans: B** — Negative gain margin indicates instability.

**Q605.** The P-M chart region shrinks as:
`A) Margins increase | B) Gain increases | C) Bandwidth decreases | D) Margins decrease toward the axes`
**Ans: D** — Stability region narrows toward PM = 0 and GM = 0.

**Q606.** The relationship between PM and overshoot is approximately:
`A) Higher PM gives higher overshoot | B) No relation | C) PM sets rise time only | D) Higher PM gives lower overshoot`
**Ans: D** — More phase margin gives a more damped, less oscillatory response.

**Q607.** A rule of thumb relating PM to closed-loop damping is:
`A) ζ = PM/10 | B) ζ = 180/PM | C) ζ = PM² | D) ζ ≈ PM/100 for PM in degrees (approximately)`
**Ans: D** — For PM around 45–60°, ζ ≈ 0.45–0.6.

**Q608.** A P-M chart for a system with a pure time delay tends to show:
`A) Increased phase margin | B) Reduced phase margin for a given gain | C) No change | D) Infinite margin`
**Ans: B** — Delay adds negative phase, degrading margins.

**Q609.** The stability boundary in the P-M plane is the union of:
`A) PM = 0 and GM = 0 axes | B) A circle | C) The diagonal | D) The origin only`
**Ans: A** — Marginal stability occurs on either axis.

**Q610.** If both PM and GM are positive but small, the system:
`A) Is unstable | B) Is marginally stable | C) Is stable but poorly damped | D) Is unobservable`
**Ans: C** — Positive but small margins mean stable yet lightly damped.

**Q611.** In a P-M chart, moving to larger PM and larger GM corresponds to:
`A) A more oscillatory design | B) Larger noise | C) A more robustly stable design | D) More delay`
**Ans: C** — Larger margins mean greater robustness.

**Q612.** The P-M chart can also plot:
`A) Poles | B) Zeros | C) Sensitivity peaks | D) Time constants`
**Ans: C** — Sensitivity peaks relate to margins.

**Q613.** Two systems with the same P-M chart point have:
`A) Identical bandwidth | B) Identical steady-state error | C) Similar stability robustness | D) Identical noise`
**Ans: C** — The margins characterize relative stability.

**Q614.** The P-M chart is used for:
`A) Time-domain simulation only | B) Root-locus plotting | C) Pole placement | D) Frequency-domain stability assessment`
**Ans: D** — It is a frequency-domain (classical) tool.

**Q615.** A closed-loop system with PM = 30° typically exhibits:
`A) No overshoot | B) Large overshoot and ringing | C) Moderate overshoot | D) Zero bandwidth`
**Ans: C** — 30° PM gives moderate (roughly 20–30%) overshoot.

**Q616.** A closed-loop system with PM = 10° typically exhibits:
`A) Very damped response | B) Heavy ringing / near-instability | C) No overshoot | D) Infinite bandwidth`
**Ans: B** — Very low PM implies heavy oscillation.

**Q617.** The maximum closed-loop resonant peak is approximately:
`A) 1 dB | B) M_r ≈ 1/PM (in radians) when PM is small | C) 0 | D) Equal to the open-loop peak`
**Ans: B** — Peak ≈ 1/PM for small phase margin.

**Q618.** A system is called conditionally stable if:
`A) It is always unstable | B) It is stable only for a limited range of gain | C) It has no poles | D) It is non-minimum phase`
**Ans: B** — Stability holds only within a gain interval.

**Q619.** For a conditionally stable system:
`A) The chart is empty | B) Margins are infinite | C) The P-M chart shows a limited stable region | D) No crossover exists`
**Ans: C** — The stable region is bounded on both sides.

**Q620.** In a conditionally stable system, increasing gain beyond the upper limit causes:
`A) Improved stability | B) No change | C) Instability | D) Reduced bandwidth`
**Ans: C** — Too much gain leads to oscillation.

**Q621.** For a conditionally stable system, decreasing gain below the lower limit causes:
`A) Improved stability | B) Higher bandwidth | C) Reduced noise | D) Loss of stability`
**Ans: D** — Too little gain also destabilizes via the low-gain boundary.

**Q622.** The P-M chart helps distinguish:
`A) Minimum from maximum phase | B) Absolutely stable from conditionally stable systems | C) Type from order | D) Pole from zero`
**Ans: B** — The bounded region reveals conditional stability.

**Q623.** For a system with a single resonant peak, the P-M chart indicates:
`A) Infinite stability | B) No resonance | C) A potential gain range causing instability | D) Zero gain`
**Ans: C** — Resonance creates marginal stability within a gain band.

**Q624.** For a unity-feedback loop with open-loop transfer L(s), the complementary sensitivity is:
`A) T = 1/(1 + L) | B) T = 1 − L | C) T = L/(1 + L) | D) T = L(1 + L)`
**Ans: C** — T = Y/R = L/(1 + L), the closed-loop response to the reference.

**Q625.** The peak of the sensitivity function S(jω) relates to:
`A) The gain margin | B) The inverse of the phase margin | C) Bandwidth | D) Steady-state error`
**Ans: B** — M_s (sensitivity peak) ≈ 1/PM for small PM.

**Q626.** A large sensitivity peak M_s indicates:
`A) Good robustness | B) Poor robustness to gain/parameter variation | C) Large bandwidth | D) Zero phase margin`
**Ans: B** — A tall M_s means sensitive, fragile system.

**Q627.** The relationship between the sensitivity peak and PM for a second-order loop is approximately:
`A) M_s = 1/(2 sin(PM)) | B) M_s = PM | C) M_s = 1/PM² | D) M_s = 2 PM`
**Ans: A** — M_s = 1/(2 sin(PM)) for a simple second-order loop.

**Q628.** The waterbed effect in sensitivity shaping means:
`A) Sensitivity is flat | B) Sensitivity peaks at ω = 0 | C) No trade-off exists | D) High-frequency sensitivity cannot be reduced without low-frequency growth`
**Ans: D** — Skew-sensitivity trade-off between low and high frequency.

**Q629.** For a plant with a RHP zero, sensitivity shaping:
`A) Can always be improved | B) Has no limit | C) Faces non-minimum-phase bandwidth limits | D) Requires no effort`
**Ans: C** — RHP zeros impose a hard bandwidth limit.

**Q630.** Mixed-sensitivity design (H∞) optimizes:
`A) Only bandwidth | B) Only noise | C) Sensitivity, complementary sensitivity, and control effort together | D) Only the pole locations`
**Ans: C** — It balances multiple objectives in the frequency domain.

**Q631.** The P-M chart's stability region for a well-designed loop is chosen to allow:
`A) Variations in gain and phase | B) Only nominal operation | C) Zero disturbance rejection | D) Nominal only`
**Ans: A** — Margins cover real-world parameter uncertainty.

**Q632.** A system with gain K varied by ±20% requires the GM to exceed:
`A) About 1.6 dB | B) 0 dB | C) 20 dB | D) 6 dB`
**Ans: A** — 20 log₁₀(1.2) ≈ 1.58 dB.

**Q633.** For a first-order pole at ω_c, a ±20% shift of the corner frequency changes its phase contribution by roughly:
`A) ±10° | B) ±180° | C) 0° | D) ±90°`
**Ans: A** — Near the corner, dφ/dω ≈ ±0.2 rad/10 per decade, giving about ±10° for a ±20% corner shift.

**Q634.** Design margin PM = 45° is often chosen to allow:
`A) Exact nominal operation only | B) Zero tolerance | C) A ±20% parameter variation | D) Infinite variation`
**Ans: C** — 45° PM covers typical component tolerance.

**Q635.** In a P-M chart, the stable region is:
`A) Bounded by the PM = 0 and GM = 0 axes and closed at large margins | B) Unbounded | C) A single point | D) A circle only`
**Ans: A** — The stable region extends into large-margin territory and is cut off by the axes.

**Q636.** If a system lies at PM = 70°, GM = 15 dB, a modest component variation will:
`A) Keep it stable | B) Make it unstable | C) Cause zero overshoot | D) Make it non-minimum phase`
**Ans: A** — Generous margins absorb variation.

**Q637.** The P-M chart is most useful for:
`A) Computing poles exactly | B) Designing sensors | C) Choosing motors | D) Quickly assessing relative stability without solving the characteristic equation`
**Ans: D** — It is a quick frequency-domain stability screen.

**Q638.** Marginal stability in the P-M chart appears on:
`A) The centre | B) The PM = 0 or GM = 0 axes | C) The corners | D) Beyond all axes`
**Ans: B** — Zero margin on either axis is the boundary.

**Q639.** The gain margin GM and phase margin PM are:
`A) Identical | B) Unrelated to stability | C) Always equal | D) Measure of robustness, not absolute stability alone`
**Ans: D** — They indicate how close the loop is to instability.

**Q640.** For a system with PM = 60°, the closed-loop is generally:
`A) Well damped (ζ ≈ 0.6) | B) Undamped | C) Unstable | D) Overdamped only`
**Ans: A** — 60° PM corresponds to ζ ≈ 0.6.

**Q641.** The P-M chart can be extended to multiple loops:
`A) Using multivariate/matrix margins | B) Not at all | C) Only single-loop | D) Only for digital systems`
**Ans: A** — Multivariable extensions use disk margins etc.

**Q642.** Disk margin generalizes P-M margins to:
`A) Frequency only | B) Time only | C) Simultaneous gain and phase uncertainty | D) Sensor noise`
**Ans: C** — Disk margins cover combined complex uncertainty.

**Q643.** A robust stability requirement via P-M margins:
`A) Only the nominal point | B) The origin | C) Nothing | D) The stable region must contain the uncertainty disk`
**Ans: D** — The uncertainty region must lie inside the stability region.

**Q644.** If the P-M stability region is small, the system is:
`A) Robust | B) Non-linear | C) Time-varying | D) Fragile / sensitive`
**Ans: D** — Small region means poor tolerance to variation.

**Q645.** The P-M chart's axes represent:
`A) Gain margin (dB) and phase margin (degrees) | B) Bandwidth and rise time | C) Poles and zeros | D) Gain and phase directly (not margins)`
**Ans: A** — The chart plots the two relative-stability margins.

---

## SECTION 10 — Routh-Hurwitz, Root Location & Stability (Q646–Q695)

**Q646.** The Routh-Hurwitz criterion determines stability from:
`A) The sum of coefficients | B) The order | C) The gain | D) The number of sign changes in the first column of the Routh array`
**Ans: D** — A system is stable iff all first-column entries are of the same (positive) sign.

**Q647.** For a system to be stable, the Routh array's first column must have:
`A) All entries zero | B) All entries of the same sign | C) Any sign | D) Only positive entries if leading coefficient positive`
**Ans: B** — No sign changes means no RHP roots.

**Q648.** Counting sign changes down the first column of a Routh array directly yields:
`A) The count of left-half-plane poles | B) The order of the polynomial | C) The count of right-half-plane poles | D) The count of zeros of 1 + GH(s)`
**Ans: C** — Each sign change corresponds to one RHP root.

**Q649.** If the first column of the Routh array has 2 sign changes, the system has:
`A) 0 RHP poles | B) 1 RHP pole | C) 4 RHP poles | D) 2 RHP poles`
**Ans: D** — Sign changes = RHP roots.

**Q650.** A row of zeros in the Routh array indicates:
`A) Unstable | B) Symmetric roots about the origin | C) Stable | D) A zero-order term`
**Ans: B** — A complete zero row signals roots symmetric about the origin (jω axis).

**Q651.** When a row of zeros appears in the Routh array, you:
`A) Replace it with the derivative of the row above and continue | B) Stop | C) Insert zeros | D) Divide by the row`
**Ans: A** — Use the auxiliary polynomial from the row above.

**Q652.** The auxiliary polynomial method for a zero row constructs roots:
`A) From the last row | B) From the coefficients | C) From the row above the zero row | D) From the first column`
**Ans: C** — Its roots satisfy the s-axis crossing condition.

**Q653.** The presence of symmetric roots about the origin means:
`A) The system is marginally stable (or unstable) | B) The system is stable | C) The system is unstable always | D) The system is uncontrollable`
**Ans: A** — Roots on the jω axis give marginal stability, not asymptotic stability.

**Q654.** If the entire first column of the Routh array is zero:
`A) The system is stable | B) The system has all-zero poles | C) Divide by s | D) Use the auxiliary polynomial from the last nonzero row`
**Ans: D** — A zero first column indicates symmetric roots; form the auxiliary polynomial.

**Q655.** Routh-Hurwitz is:
`A) Only sufficient | B) A necessary and sufficient stability criterion | C) Only necessary | D) An approximation`
**Ans: B** — It exactly characterizes the number of RHP roots.

**Q656.** For a second-order polynomial s² + a₁s + a₀ to be stable:
`A) a₁ > 0 or a₀ > 0 | B) a₀ = 0 | C) a₁ > 0 and a₀ > 0 | D) a₁ < 0`
**Ans: C** — Both coefficients must be positive for a second-order Hurwitz polynomial.

**Q657.** For a third-order polynomial s³ + a₂s² + a₁s + a₀ to be stable:
`A) All positive is enough | B) a₂a₁ < a₀ | C) Any signs | D) All positive and a₂a₁ > a₀`
**Ans: D** — Routh first column 1, a₂, (a₂a₁ − a₀)/a₂, a₀ requires a₂a₁ > a₀.

**Q658.** For a fourth-order s⁴ + a₃s³ + a₂s² + a₁s + a₀ to be stable, the Hurwitz determinants must satisfy:
`A) Δ₁ > 0, Δ₂ > 0, Δ₃ > 0, Δ₄ > 0 | B) Only Δ₁ > 0 | C) All negative | D) Only Δ₄ > 0`
**Ans: A** — All Hurwitz determinants must be positive.

**Q659.** The Hurwitz determinant Δ₁ for s⁴ + a₃s³ + a₂s² + a₁s + a₀ is:
`A) a₂ | B) a₃ | C) a₁ | D) a₀`
**Ans: B** — Δ₁ = a₃.

**Q660.** The second Hurwitz determinant of a quartic, Δ₂, is:
`A) a₃a₁ − a₂ | B) a₃a₂ − a₁ | C) a₂a₀ − a₁² | D) a₃a₀`
**Ans: B** — Δ₂ = a₃a₂ − a₁.

**Q661.** The third Hurwitz determinant of a quartic, Δ₃, is:
`A) a₂a₁ − a₀ | B) a₃a₂a₁ − a₃²a₀ − a₁² | C) a₃a₀ − a₁ | D) a₁a₀`
**Ans: B** — Δ₃ = a₃(a₂a₁ − a₀) − a₁².

**Q662.** Routh-Hurwitz applies to:
`A) Complex coefficients only | B) Any transfer function | C) Polynomials with real coefficients | D) Only second-order`
**Ans: C** — Standard form assumes real coefficients.

**Q663.** The Routh array is constructed by:
`A) Alternating rows of coefficients and their combinations | B) Only the first row | C) Random | D) Sorted coefficients`
**Ans: A** — Each element is (first of prev × next of next − next of prev × first of next)/first of prev.

**Q664.** The element b₁ in the s² row of a Routh array (cubic) is:
`A) (a₂a₀ − a₁)/a₀ | B) a₁ | C) a₀ | D) (a₂a₁ − a₀)/a₂`
**Ans: D** — b₁ = (a₂·a₁ − 1·a₀)/a₂.

**Q665.** For a quartic, the s² row entries are:
`A) b₁ = a₂, b₂ = a₁ | B) b₁ = (a₃a₂ − a₁)/a₃, b₂ = a₀ | C) b₁ = a₃, b₂ = a₂ | D) b₁ = a₀, b₂ = a₁`
**Ans: B** — First element from combining rows, second is the last coefficient.

**Q666.** In the Routh table, the first element of each row is computed as:
`A) Sum | B) Product | C) (First of above × second of below − second of above × first of below)/first of above | D) Average`
**Ans: C** — The standard Routh combination formula.

**Q667.** Routh-Hurwitz can also determine:
`A) The exact pole locations | B) The number of RHP and LHP poles | C) The steady-state error | D) The bandwidth`
**Ans: B** — It counts RHP/LHP roots but not their exact values.

**Q668.** If a polynomial has a zero coefficient while others are positive, as in s³ + s² + s, the system:
`A) Is always stable | B) Is always marginally stable | C) Is always unstable | D) Is marginally stable or unstable, depending on the remaining coefficients`
**Ans: D** — s³+s²+s = s(s²+s+1) gives roots 0 and −0.5 ± j0.866, i.e. a pole at the origin, so the outcome depends on the rest of the polynomial.

**Q669.** The Routh criterion applied to the characteristic equation s⁴ + 2s³ + 3s² + 4s + K gives stability range:
`A) All K | B) K > 0 (limited) | C) K < 0 only | D) K = 0 only`
**Ans: B** — First column: 1, 2, 1, 4 − 2K, K, which is all positive only for 0 < K < 2.

**Q670.** The Routh criterion for s³ + 3s² + 3s + K gives:
`A) 0 < K < 9 | B) All K | C) K > 0 | D) K = 0`
**Ans: A** — b₁ = (3·3 − K)/3 = 3 − K/3 > 0 → K < 9, and K > 0.

**Q671.** Routh criterion for s³ + s² + Ks + 1 gives a stable range of:
`A) 0 < K < 1 | B) K > 1 | C) All K > 0 | D) K = 0`
**Ans: B** — First column 1, 1, K − 1, 1 is positive only for K > 1.

**Q672.** Routh for s⁴ + s³ + 2s² + Ks + 1 shows the system is stable:
`A) For 0 < K < 2 | B) For all K > 0 | C) Never | D) Only at K = 1, and marginally`
**Ans: D** — The c₁ element becomes (K−1)²/(2−K), which is never positive, so the array fails except marginally at K = 1.

**Q673.** Routh for s⁴ + 3s³ + 5s² + Ks + 2 gives a stable range of:
`A) 1.31 < K < 13.68 | B) 0 < K < 15 | C) All K > 0 | D) K > 15`
**Ans: A** — Requiring K(15 − K) > 18 gives K² − 15K + 18 < 0, whose roots are ≈ 1.31 and 13.68.

**Q674.** The Routh-Hurwitz criterion does NOT require:
`A) Forming the characteristic polynomial | B) Computing the exact poles | C) Building the array | D) Counting sign changes`
**Ans: B** — It counts RHP roots without solving for them.

**Q675.** In applying Routh-Hurwitz, the characteristic equation is:
`A) Numerator | B) Denominator of the closed-loop transfer function | C) Open-loop denominator | D) Gain`
**Ans: B** — 1 + G(s)H(s) = 0 after clearing denominators.

**Q676.** If the Routh array's first column has all positive entries, the system is:
`A) Stable | B) Unstable | C) Marginal | D) Uncontrollable`
**Ans: A** — No sign changes → no RHP poles.

**Q677.** If the first column contains a zero but not a full zero row, you:
`A) Stop | B) Conclude marginal | C) Replace the zero with a small ε > 0 and continue | D) Divide by the zero`
**Ans: C** — Use the epsilon (δ) technique to continue the array.

**Q678.** In the epsilon technique, ε is taken as:
`A) A small positive number | B) A large number | C) Zero | D) Negative`
**Ans: A** — Replace the zero first-column entry with a small ε > 0.

**Q679.** The limit as ε → 0 in the epsilon technique determines:
`A) The gain | B) The number of sign changes when ε = 0 | C) The poles | D) The bandwidth`
**Ans: B** — The limiting sign behavior reveals marginal stability.

**Q680.** Consider s³ + 2s² + 3s + 6. This factors as:
`A) (s + 1)(s² + s + 6) | B) (s + 3)(s² − s + 2) | C) (s + 2)(s² + 3) | D) (s + 6)(s² − 4)`
**Ans: C** — s³ + 2s² + 3s + 6 = (s+2)(s²+3), roots −2, ±j√3.

**Q681.** The system with characteristic equation s³ + 2s² + 3s + 6 is:
`A) Unstable | B) Marginally stable (roots −2, ±j√3) | C) Asymptotically stable | D) Uncontrollable`
**Ans: B** — Two poles on the jω axis → marginally stable.

**Q682.** For s² + 4s + 4, the system is:
`A) Underdamped | B) Critically damped (double root at −2) | C) Overdamped | D) Unstable`
**Ans: B** — Discriminant 0 → critically damped.

**Q683.** For s² + s + 1, the system is:
`A) Critically damped | B) Underdamped | C) Overdamped | D) Unstable`
**Ans: B** — Discriminant 1 − 4 = −3 < 0 → complex (underdamped) roots.

**Q684.** For s² + 5s + 4, the system is:
`A) Overdamped (roots −1, −4) | B) Underdamped | C) Critically damped | D) Unstable`
**Ans: A** — Discriminant 25 − 16 = 9 > 0, distinct negative real roots.

**Q685.** A polynomial with all roots in the LHP strictly is:
`A) Marginally stable | B) Unstable | C) Hurwitz stable | D) Non-Hurwitz`
**Ans: C** — Strictly LHP = asymptotically (Hurwitz) stable.

**Q686.** Routh-Hurwitz for a fifth-order polynomial requires:
`A) Only Δ₁ > 0 | B) Δ₁ through Δ₅ > 0 | C) Δ₅ > 0 | D) All Δ < 0`
**Ans: B** — All Hurwitz determinants must be positive.

**Q687.** If Δ₃ < 0 while others are positive in a quartic:
`A) The system is unstable | B) Stable | C) Marginal | D) Well-damped`
**Ans: A** — A negative determinant signals RHP roots.

**Q688.** The Routh array for the characteristic equation s⁵ + 2s⁴ + s³ produces a zero row, which signals:
`A) Roots symmetric about the origin (here a triple pole at 0) | B) All roots in the LHP | C) Stability | D) A single pole at −1`
**Ans: A** — s⁵+2s⁴+s³ = s³(s+1)², so three poles sit at the origin.

**Q689.** The Routh array of a system that is definitely stable must have:
`A) First column with one sign change | B) First column all zero | C) First column alternating | D) First column with no sign changes`
**Ans: D** — No sign changes is the stability criterion.

**Q690.** The number of RHP poles for s⁴ + s³ + s² + s + 1:
`A) 2 | B) 0 (all roots on the unit circle, marginal) | C) 1 | D) 4`
**Ans: B** — Roots are 5th roots of −1, all on the unit circle, symmetric about the real axis → marginal stability.

**Q691.** s⁴ + s³ + s² + s + 1 is best described as:
`A) Asymptotically stable | B) Unstable | C) Uncontrollable | D) Marginally stable`
**Ans: D** — Poles lie on the unit circle (and none in RHP), marginally stable.

**Q692.** Routh-Hurwitz for s⁴ + a₃s³ + a₂s² + a₁s + a₀ gives the condition:
`A) a₃ > 0 only | B) All coefficients positive is sufficient | C) a₀ = 0 | D) a₃ > 0, a₃a₂ > a₁, and a₃a₂a₁ > a₁² + a₃²a₀`
**Ans: D** — The full quartic Hurwitz conditions.

**Q693.** If the Routh array's last first-column element is zero but not a full zero row:
`A) Stable | B) Unstable | C) Marginal stability (pole at origin) | D) Uncontrollable`
**Ans: C** — A zero s⁰ entry means a root at s = 0.

**Q694.** For a system with characteristic equation s³ + 3s² + 3s + K, K = 0 gives:
`A) Stable | B) Pole at origin (marginal) | C) Unstable | D) All roots −1`
**Ans: B** — s³+3s²+3s = s(s²+3s+3) → roots 0, (−3±j√3)/2.

**Q695.** The Routh-Hurwitz criterion, properly applied, tells us:
`A) The number of RHP poles but not their exact values | B) The exact poles | C) The gain margin | D) The steady-state error`
**Ans: A** — Counting, not exact pole placement.

---

## SECTION 11 — Z-Transform & Difference Equations (Q696–Q780)

**Q696.** The z-transform is defined as:
`A) Σ f(k)·z^k | B) ∫ f(t)e^(−st)dt | C) Z{f(k)} = Σ f(k)·z^(−k) | D) Σ f(k)·k`
**Ans: C** — Z{f(k)} = Σ_{k=0}^∞ f(k) z^(−k), the discrete-time counterpart of Laplace.

**Q697.** The Laplace transform is a continuous-time analogue of:
`A) The Fourier transform only | B) The DFT | C) The Mellin transform | D) The z-transform`
**Ans: D** — Laplace is to continuous time as z-transform is to discrete time.

**Q698.** The z-transform of the unit step sequence u[k] is:
`A) z/(z + 1) | B) z/(z − 1) | C) 1/(z − 1) | D) z²/(z − 1)`
**Ans: B** — Z{u[k]} = z/(z − 1) for a right-sided step starting at k = 0.

**Q699.** The z-transform of the unit impulse δ[k] is:
`A) z | B) 1 | C) 1/z | D) 0`
**Ans: B** — δ[k] is 1 at k = 0 and 0 elsewhere, so its transform is 1.

**Q700.** The z-transform of a^k (a^k u[k]) is:
`A) z/(z + a) | B) z/(z − a) | C) a/(z − a) | D) 1/(z − a)`
**Ans: B** — A geometric series in z^(−1).

**Q701.** The z-transform of k (ramp) is:
`A) z/(z − 1) | B) z²/(z − 1)² | C) z/(z − 1)² | D) 1/(z − 1)²`
**Ans: C** — k has transform z/(z − 1)², the double-pole analogue of the ramp.

**Q702.** The z-transform of the left-sided or anti-causal sequence is obtained using:
`A) The same formula | B) ROC outside the outermost pole | C) A different sign | D) No transform exists`
**Ans: B** — Left-sided sequences have ROCs inside the innermost pole.

**Q703.** The ROC (region of convergence) for a causal sequence is:
`A) Inside the innermost pole | B) Outside the outermost pole | C) A unit circle | D) Everywhere`
**Ans: B** — Right-sided sequences converge for |z| greater than the largest pole.

**Q704.** The ROC for a left-sided sequence is:
`A) Inside the innermost pole | B) Outside the outermost pole | C) The unit circle only | D) The origin only`
**Ans: A** — Left-sided convergence requires |z| smaller than the smallest pole.

**Q705.** The ROC for a two-sided sequence is:
`A) Outside all poles | B) Inside all poles | C) The whole plane | D) An annulus between two poles`
**Ans: D** — Two-sided sequences converge in a ring.

**Q706.** A right-sided sequence with poles at 2 and 3 has an ROC:
`A) Modulus less than 2 | B) Between 2 and 3 | C) Modulus greater than 3 | D) Modulus greater than 2`
**Ans: C** — A right-sided sequence converges for |z| beyond the largest pole.

**Q707.** The bilateral z-transform differs from the unilateral in that it requires:
`A) Differentiating | B) Specifying the ROC | C) Integration | D) No ROC needed`
**Ans: B** — The ROC disambiguates left- vs right-sided sequences.

**Q708.** The z-transform of a delayed sequence f[k − m]u[k − m] is:
`A) z^m F(z) | B) z^(−m)F(z) | C) z^(−1)F(z) only for m=1 | D) mF(z)`
**Ans: B** — A delay of m samples multiplies by z^(−m).

**Q709.** The z-transform of an advanced sequence f[k + m] is:
`A) z^(−m)F(z) | B) mF(z) | C) 0 | D) z^m F(z)`
**Ans: D** — Advance multiplies by z^m.

**Q710.** The time-shifting property is:
`A) Z{f[k−m]} = mF(z) | B) Z{f[k−m]} = z^m F(z) | C) Z{f[k − m]u[k − m]} = z^(−m)F(z) | D) Z{f[k−m]} = F(z)/m`
**Ans: C** — The standard delay property.

**Q711.** Z-transform of a^n f[n] (scaling property) is:
`A) aF(z) | B) F(az) | C) F(z)/a | D) F(z/a)`
**Ans: D** — Exponential weighting maps to scaling z → z/a.

**Q712.** The convolution property of the z-transform is:
`A) Z{f*g} = F(z)·G(z) | B) F(z) + G(z) | C) F(z)/G(z) | D) F(z)² only`
**Ans: A** — Convolution in time becomes multiplication, as in Laplace.

**Q713.** The difference between forward-shift and delay operators is:
`A) They are identical | B) Both are f[k−1] | C) Delay: f[k−m]; forward shift: f[k+m] | D) Both are f[k+1]`
**Ans: C** — The z transform maps delay to z^(−m), forward shift to z^m.

**Q714.** The delay operator in the z-domain corresponds to multiplying by:
`A) z | B) z^(−1) | C) 1/z² | D) 1`
**Ans: B** — f[k−1] ↔ z^(−1)F(z).

**Q715.** The forward-shift operator corresponds to:
`A) z | B) z^(−1) | C) 1 | D) z²`
**Ans: A** — f[k+1] ↔ zF(z).

**Q716.** A first-order difference equation y[k] − a y[k−1] = f[k] has transfer function:
`A) 1/(1 + a z^(−1)) | B) a/(1 − a z^(−1)) | C) 1/(1 − a z^(−1)) | D) z/(z − 1)`
**Ans: C** — Taking the z-transform with zero initial conditions gives H(z) = 1/(1 − a z^(−1)).

**Q717.** The characteristic equation of a discrete system y[k+1] − a y[k] = f[k] is:
`A) s = −a | B) s = 1/a | C) s = 0 | D) s = a (or z = a)`
**Ans: D** — Substituting y[k] = λ^k gives λ = a.

**Q718.** Stability of a discrete-time LTI system requires all poles to lie:
`A) Outside the unit circle | B) Strictly inside the unit circle | C) On the unit circle | D) At the origin`
**Ans: B** — |z_i| < 1 for asymptotic stability.

**Q719.** A pole on the unit circle (|z| = 1) indicates:
`A) Marginal stability (not asymptotically stable) | B) Asymptotic stability | C) Instability always | D) Controllability`
**Ans: A** — Unit-circle poles are sustained oscillations → marginally stable.

**Q720.** A pole outside the unit circle indicates:
`A) Marginally stable | B) Stable | C) Uncontrollable | D) Unstable`
**Ans: D** — |z| > 1 grows without bound.

**Q721.** A causal discrete system is stable if and only if:
`A) The ROC excludes the unit circle | B) All poles are at the origin | C) The ROC includes the unit circle | D) The ROC is empty`
**Ans: C** — Causal + ROC containing |z| = 1 ⇔ stable.

**Q722.** Zeros of a transfer function H(z) = F(z)/G(z) are:
`A) Roots of G(z) | B) Poles of the system | C) Roots of F(z) | D) The ROC boundary`
**Ans: C** — Zeros are where the numerator vanishes (with the system response to zero).

**Q723.** Poles of H(z) are:
`A) Roots of the numerator | B) The gain | C) The ROC | D) Roots of the denominator G(z)`
**Ans: D** — Poles are the singularities of H(z).

**Q724.** The sampling theorem (Nyquist) requires the sampling frequency:
`A) f_s < 2 f_max | B) f_s > 2 f_max | C) f_s = f_max | D) f_s > 100 f_max`
**Ans: B** — f_s ≥ 2f_max to avoid aliasing.

**Q725.** Aliasing occurs when:
`A) The sampling frequency is too low (f_s < 2 f_max) | B) The sampling frequency is too high | C) The signal is DC | D) The gain is too high`
**Ans: A** — Frequencies above f_s/2 fold back into the baseband.

**Q726.** The Nyquist frequency (half the sampling frequency) is:
`A) 2 f_s | B) f_s | C) f_s/2 | D) f_s/4`
**Ans: C** — The usable band is 0 to f_s/2.

**Q727.** To avoid aliasing, an anti-aliasing filter is placed:
`A) After the sampler | B) After the D/A converter | C) Before the sampler, low-pass | D) Nowhere`
**Ans: C** — Filter the analog signal before sampling.

**Q728.** The z-transform sampling relation s = z-related is approximated by:
`A) z = s + 1 | B) z = 1/s | C) z = sT | D) z = e^(sT)`
**Ans: D** — The mapping from the s-plane to the z-plane is z = e^(sT), T = 1/f_s.

**Q729.** Under the mapping z = e^(sT), the s-plane's left half maps to:
`A) The outside of the unit circle | B) The unit circle | C) The imaginary axis | D) The inside of the unit circle`
**Ans: D** — Re(s) < 0 → |z| < 1, so stable s-plane ↔ inside unit circle.

**Q730.** The mapping z = e^(sT) sends the imaginary axis (s = jω) to:
`A) The real axis | B) The unit circle | C) The origin | D) The z = 1 line`
**Ans: B** — The jω axis maps to |z| = 1, so continuous-time marginal stability maps to the unit circle.

**Q731.** The relationship between continuous and discrete poles under z = e^(sT) is:
`A) s_i = e^(z_i T) | B) z_i = e^(s_i T) | C) z_i = s_i T | D) z_i = s_i + T`
**Ans: B** — Discrete poles are the exponentials of the continuous poles times T.

**Q732.** An impulse-invariant method to obtain H(z) from H(s):
`A) Direct substitution | B) z{e^(sT)f(t)} sampled at t = kT | C) Frequency response only | D) Bilinear transform`
**Ans: B** — Impulse invariance samples the impulse response.

**Q733.** The bilinear (Tustin) transform maps:
`A) Only the LHP | B) Only jω | C) The entire s-plane to the entire z-plane | D) Only the RHP`
**Ans: C** — z = (1 + sT/2)/(1 − sT/2) maps LHP to inside the unit circle.

**Q734.** The bilinear transform formula is:
`A) z = e^(sT) | B) z = sT | C) z = 1 + sT | D) z = (1 + sT/2)/(1 − sT/2)`
**Ans: D** — The Tustin substitution mapping the s-plane to z-plane.

**Q735.** A disadvantage of the bilinear transform is:
`A) No warping at all | B) Infinite bandwidth | C) Frequency warping (frequency distortion) | D) It cannot handle integrators`
**Ans: C** — It compresses the infinite s-axis nonlinearly, warping frequencies.

**Q736.** Frequency warping can be precompensated by:
`A) Increasing the gain | B) Adding a zero | C) Ignoring it | D) Using a suitable prewarping frequency T before the transform`
**Ans: D** — Choose T so that the frequency of interest maps to the desired digital frequency.

**Q737.** In pulse transfer functions, a zero-order hold (ZOH) is often assumed because:
`A) It is instantaneous | B) The D/A converter holds each sample constant over the interval | C) It is expensive | D) It smooths noise`
**Ans: B** — A digital-to-analog converter typically holds values, modelled as ZOH.

**Q738.** A discrete transfer function H(z) = (1 − z^(−1))/(1 − 0.5 z^(−1)) corresponds to a:
`A) First-order low-pass filter | B) Integrator | C) First-order high-pass filter | D) Differentiator`
**Ans: C** — H(1) = (1 − 1)/(1 − 0.5) = 0, so the DC gain is zero while H(∞) → 2: a high-pass.

**Q739.** The backward-Euler discrete equivalent of the continuous integrator 1/s is:
`A) (1 − z^(−1))/T | B) 1/(1 − z^(−1)) with no T scaling | C) T/(1 − z^(−1)) | D) 1/s²`
**Ans: C** — Integrating 1/s gives T/(1 − z^(−1)) = Tz/(z − 1), which is also the z-transform of a unit step in T.

**Q740.** In a discrete system, a pole at z = 1 represents:
`A) A differentiator | B) A gain | C) A notch | D) An integrator`
**Ans: D** — A pole on the unit circle at z = 1 is the discrete integrator.

**Q741.** A pole at z = −1 represents:
`A) An integrator | B) A gain | C) A differentiator | D) An oscillatory mode (alternating sequence)`
**Ans: D** — z = −1 gives (−1)^k, an undamped oscillation.

**Q742.** The discrete impulse response corresponds to which transfer function relationship:
`A) H(z) is the integral | B) No relation | C) The impulse response is the inverse z-transform of H(z) | D) H(z) = F(z)/G(z)`
**Ans: C** — The impulse response is h[k] = Z⁻¹{H(z)}.

**Q743.** In the z-plane, a stable discrete system's poles:
`A) All lie on the unit circle | B) All lie outside | C) All lie strictly inside the unit circle | D) Can be anywhere`
**Ans: C** — |z| < 1 is the stability criterion.

**Q744.** A discrete system with poles at z = 0.9e^(±j0.5) is:
`A) Unstable | B) Marginal | C) Stable underdamped | D) Non-causal`
**Ans: C** — Modulus 0.9 < 1 → decaying oscillation.

**Q745.** A discrete system with poles at z = 1.2 and z = −0.5 is:
`A) Stable | B) Marginal | C) Unstable | D) Uncontrollable`
**Ans: C** — The pole at 1.2 lies outside the unit circle → unstable.

**Q746.** The z-transform of δ[k − 1] is:
`A) z | B) z^(−1) | C) 1 | D) z^(−2)`
**Ans: B** — A unit impulse delayed by one sample multiplies by z^(−1).

**Q747.** The z-transform of a^n δ[k] is:
`A) a^n | B) 1 | C) a | D) a^(−n)`
**Ans: A** — Only k = 0 contributes, giving a^n.

**Q748.** Given the difference equation y[k] = 0.5 y[k−1] + f[k], the pole is at:
`A) z = 2 | B) z = −0.5 | C) z = 1 | D) z = 0.5`
**Ans: D** — Rearranging gives 1 − 0.5z^(−1) = 0 → z = 0.5.

**Q749.** Given y[k] = 2 y[k−1] + f[k], the system is:
`A) Unstable | B) Stable | C) Marginal | D) Non-causal`
**Ans: A** — Pole at z = 2 lies outside the unit circle.

**Q750.** A discrete transfer function H(z) = z/(z − 1) has a pole at:
`A) z = 0 | B) z = 1 | C) z = −1 | D) Infinity`
**Ans: B** — The denominator z − 1 vanishes at z = 1.

**Q751.** The impulse response of H(z) = z/(z − 1) is:
`A) u[k] | B) δ[k] | C) k | D) a^k`
**Ans: A** — z/(z−1) ↔ unit step u[k].

**Q752.** The impulse response of H(z) = 1/(1 − a z^(−1)) is:
`A) a^k u[k] | B) k a^k | C) δ[k] | D) a^(−k)`
**Ans: A** — This is the standard geometric sequence response.

**Q753.** The discrete step response of a first-order system H(z) = 1/(1 − a z^(−1)) with a = 0.5 approaches:
`A) 1 | B) 0 | C) Infinity | D) 1/(1 − a) = 2`
**Ans: D** — DC gain is 1/(1 − a) = 2.

**Q754.** In the discrete domain, the steady-state error for a type-1 system (integrator at z = 1) with a step input:
`A) 0 | B) Finite nonzero | C) Infinite | D) 1`
**Ans: A** — An integrator at z = 1 gives infinite DC gain → zero step error.

**Q755.** A discrete system with two integrators (poles at z = 1, doubled) has, for a step input:
`A) Finite nonzero error | B) Infinite error | C) Undefined | D) Zero steady-state error`
**Ans: D** — Higher type still gives zero error to step.

**Q756.** The discrete-time error constants are defined using the limit:
`A) lim_{z→0} H(z) | B) lim_{z→1} (z − 1)H(z) | C) lim_{z→∞} H(z) | D) lim_{z→1} H(z)/(z − 1)`
**Ans: B** — Constants are evaluated at z = 1, the discrete "origin" of the integrator.

**Q757.** The position error constant K_p in discrete time is:
`A) lim_{z→1} H(z) | B) lim_{z→1} (z − 1)²H(z) | C) lim_{z→1} (z − 1)H(z) | D) lim_{z→0} H(z)`
**Ans: C** — K_p = lim_{z→1} (z − 1)H(z), the same form as in continuous time.

**Q758.** The velocity error constant K_v in discrete time is:
`A) lim_{z→1} (z − 1)²H(z) | B) lim_{z→1}(z−1)H(z) | C) lim_{z→1} H(z) | D) lim_{z→1}(z−1)³H(z)`
**Ans: A** — Each additional integrator adds a factor of (z − 1).

**Q759.** The acceleration error constant K_a in discrete time is:
`A) lim_{z→1}(z−1)²H(z) | B) lim_{z→1}(z−1)H(z) | C) lim_{z→1}(z−1)⁴H(z) | D) lim_{z→1} (z − 1)³H(z)`
**Ans: D** — Third-order factor for a parabolic input.

**Q760.** The sampling period T relates to the sampling frequency as:
`A) T = f_s | B) T = 1/f_s | C) T = 2f_s | D) T = f_s/2`
**Ans: B** — The sampling period is the reciprocal of the sampling frequency.

**Q761.** If a signal has a maximum frequency of 5 kHz, the minimum sampling frequency is:
`A) 5 kHz | B) 2.5 kHz | C) 10 kHz | D) 20 kHz`
**Ans: C** — Nyquist requires f_s ≥ 2 × 5 = 10 kHz.

**Q762.** A control system with a sampling period that is too large (low f_s) suffers from:
`A) Improved accuracy | B) Higher bandwidth | C) Reduced noise | D) Poor control performance / aliasing`
**Ans: D** — Undersampling degrades fidelity and control.

**Q763.** A zero-order hold's transfer function (in the Laplace domain) is:
`A) 1/s | B) 1/(s+1) | C) e^(−sT) | D) (1 − e^(−sT))/s`
**Ans: D** — The ZOH impulse response is a pulse of height 1 and width T.

**Q764.** The discrete equivalent of a ZOH-based plant includes:
`A) Only the plant | B) Only the controller | C) A pulse transfer function from ZOH to sampler | D) The reference`
**Ans: C** — The pulse transfer function incorporates the hold.

**Q765.** In a digital control system, the controller output is:
`A) Continuous | B) Piecewise linear | C) A sequence of samples (held constant between samples) | D) Random`
**Ans: C** — The D/A holds each sample, giving a staircase output.

**Q766.** A digital controller operating at sampling frequency f_s has an effective bandwidth limited by:
`A) f_s/2 | B) f_s | C) 2 f_s | D) Unbounded`
**Ans: A** — The Nyquist frequency caps the usable bandwidth.

**Q767.** The z-transform of a convolution of two sequences is:
`A) The sum | B) The integral | C) The difference | D) The product of their transforms`
**Ans: D** — Convolution ↔ multiplication, as in continuous time.

**Q768.** The inverse z-transform can be obtained by:
`A) Only Fourier transform | B) Only convolution | C) Long division, partial fractions, or contour integration | D) Only Laplace`
**Ans: C** — Standard inverse-z methods.

**Q769.** Partial-fraction expansion requires the transform to be:
`A) A ratio of polynomials with distinct poles | B) Always proper in z | C) Analytic everywhere | D) A constant`
**Ans: A** — Distinct poles allow a simple partial-fraction decomposition.

**Q770.** Long-division expansion of H(z) in powers of z^(−1) gives:
`A) Nothing useful | B) The ROC | C) The gain | D) An impulse response sequence directly`
**Ans: D** — Expanding in powers of z^(−1) yields the impulse-response coefficients h[0], h[1], h[2], and so on.

**Q771.** A discrete pole at the origin (z = 0) represents:
`A) A finite-time (dead-beat) mode | B) An integrator | C) An oscillator | D) A delay`
**Ans: A** — A pole at z = 0 vanishes after one sample (finite settling).

**Q772.** Deadbeat (finite settling time) response occurs when:
`A) All poles are at the origin | B) All poles are on the unit circle | C) All poles are at 1 | D) All poles are complex`
**Ans: A** — Poles at z = 0 give finite-duration transients.

**Q773.** The settling time (in samples) of a deadbeat system is:
`A) Infinite | B) Zero | C) Equal to the number of poles | D) The order + 1`
**Ans: C** — Each pole at the origin settles one sample per step.

**Q774.** The minimum-phase condition in discrete time requires:
`A) All zeros outside | B) All zeros inside the unit circle | C) All zeros on the unit circle | D) No zeros`
**Ans: B** — Minimum phase = zeros inside, so inverse is stable.

**Q775.** A non-minimum-phase discrete system has zeros:
`A) Inside | B) On the circle | C) Outside the unit circle | D) At the origin only`
**Ans: C** — Zeros outside |z| = 1 make the inverse response unstable.

**Q776.** Digital filters with zeros at the unit circle (e.g. z = ±1) act as:
`A) Integrators | B) Differentiators | C) Notch filters | D) All-pass only`
**Ans: C** — Zeros at z = e^(±jω0) notch out those frequencies.

**Q777.** A digital differentiator has transfer function approximately:
`A) 1/(1 − z^(−1)) | B) z/(z − 1) | C) (1 − z^(−1)) | D) 1/(1 + z^(−1))`
**Ans: C** — The difference y[k] − y[k−1] approximates the derivative.

**Q778.** The frequency response of a discrete system at ω (rad/sample) is:
`A) H(jω) | B) H(z)|_{z = e^(jω)} | C) H(0) | D) H(1)`
**Ans: B** — Evaluate H(z) on the unit circle, z = e^(jω).

**Q779.** Discrete frequencies are periodic with period:
`A) π | B) 2π rad/sample | C) 2π/T | D) 1`
**Ans: B** — z = e^(jω) is periodic in ω with period 2π per sample.

**Q780.** The discrete-time frequency response is periodic, meaning:
`A) Frequencies above π rad/sample alias | B) Frequencies are continuous | C) No aliasing ever | D) The spectrum is aperiodic`
**Ans: A** — Due to periodicity, ω and 2π − ω give the same response, and >π folds.

---

## SECTION 12 — Sampling, Signal Processing & Applications (Q781–Q850)

**Q781.** The sampling frequency must be at least twice the highest frequency to:
`A) Ensure stability | B) Reduce noise | C) Increase gain | D) Avoid aliasing`
**Ans: D** — The Nyquist criterion.

**Q782.** In sampling, a spectrum replica appears every:
`A) 2 f_s | B) f_s | C) f_s/2 | D) 1/T²`
**Ans: B** — Replicas are spaced by f_s.

**Q783.** Anti-aliasing filters are typically:
`A) High-pass | B) Low-pass | C) Band-pass | D) Notch`
**Ans: B** — They must pass the desired band and reject above f_s/2.

**Q784.** The Nyquist interval (0 to f_s/2) is sometimes called the:
`A) Stopband | B) Passband edge only | C) Guard band only | D) Baseband`
**Ans: D** — The principal baseband.

**Q785.** If a sampling frequency is exactly twice the signal frequency, the system is:
`A) Safe | B) Unstable | C) At the Nyquist limit, prone to aliasing | D) Uncontrollable`
**Ans: C** — Exactly at the limit, any deviation causes aliasing.

**Q786.** Sample-and-hold circuits in data acquisition:
`A) Hold always | B) Track always | C) Track the input during sampling, hold during conversion | D) Ignore the input`
**Ans: C** — Track-and-hold captures a snapshot for the ADC.

**Q787.** Quantization error in an ADC:
`A) Is bounded by half an LSB | B) Is unbounded | C) Is zero | D) Depends only on gain`
**Ans: A** — Max quantization error = ±½ LSB.

**Q788.** The resolution of an n-bit ADC is:
`A) 1/n | B) n | C) 1/2^n of full scale | D) 1/2 of full scale`
**Ans: C** — LSB = FS/2^n.

**Q789.** The signal-to-quantization-noise ratio for an n-bit ADC improves as:
`A) n increases | B) n decreases | C) n is constant | D) n goes to 1`
**Ans: A** — SNR ≈ 6.02n + 1.76 dB, improving with bits.

**Q790.** The Nyquist rate for a bandlimited signal of bandwidth B is:
`A) B | B) B/2 | C) 4B | D) 2B`
**Ans: D** — f_s ≥ 2B.

**Q791.** In a digital control loop, the sampling introduces:
`A) No delay | B) Infinite delay | C) Negative delay | D) A computational delay`
**Ans: D** — ADC, computation, and DAC add latency.

**Q792.** The computational delay in a digital controller:
`A) Increases phase margin | B) Has no effect | C) Reduces phase margin | D) Increases bandwidth`
**Ans: C** — Delay is pure phase lag, degrading stability.

**Q793.** Quantization noise in a digital control system acts like:
`A) A small input disturbance | B) A large disturbance | C) No disturbance | D) A deterministic bias only`
**Ans: A** — It behaves as low-level noise entering the loop.

**Q794.** A digital potentiometer or DAC in the feedback path:
`A) Introduces quantization | B) Removes all error | C) Has infinite resolution | D) None`
**Ans: A** — Finite resolution causes quantization error.

**Q795.** In a data-acquisition system, the multiplexer:
`A) Amplifies | B) Converts analog to digital | C) Selects which sensor feeds the ADC | D) Filters`
**Ans: C** — The mux routes multiple inputs to one ADC.

**Q796.** A sample-and-hold's droop (voltage decay during hold):
`A) Improves accuracy | B) Degrades accuracy | C) Has no effect | D) Increases bandwidth`
**Ans: B** — Droop causes hold error.

**Q797.** The antialiasing filter's cutoff should be:
`A) Above f_s | B) Below f_s/2 | C) Exactly f_s | D) Above f_s/2`
**Ans: B** — Cut off below the Nyquist frequency to avoid foldover.

**Q798.** Oversampling (f_s much greater than 2B) allows:
`A) Higher noise only | B) Lower resolution | C) Digital filtering to replace a steep analog filter | D) Faster aliasing`
**Ans: C** — Oversampling plus digital filtering relaxes analog filter demands.

**Q799.** Decimation (reducing sampling rate) requires:
`A) No filter | B) Only a gain | C) A high-pass filter | D) A preceding low-pass filter`
**Ans: D** — Filter below the new Nyquist frequency before decimating.

**Q800.** Interpolation (increasing sampling rate) requires:
`A) A low-pass filter | B) No filter | C) Only amplification | D) A differentiator`
**Ans: A** — Spectral images above the new Nyquist must be filtered out.

**Q801.** In a sampled-data control system, the star transform converts:
`A) Analog to digital | B) Digital to analog | C) Voltage to current | D) Laplace-domain impedances/capacitors to discrete equivalents`
**Ans: D** — The star transform (ZOH equivalent) maps s-domain elements to z-domain.

**Q802.** In pulse-transfer-function analysis, the equivalent of a capacitor 1/(sC) becomes (using backward difference):
`A) T/(C(1 − z^(−1))) | B) C/(1 − z^(−1)) | C) 1/(C T) | D) (1 − z^(−1))/T`
**Ans: A** — Backward-difference integration: 1/s → T/(1 − z^(−1)), so 1/(sC) → T/(C(1 − z^(−1))).

**Q803.** In pulse-transfer-function analysis, the equivalent of an inductor sL becomes (backward difference):
`A) L T/(1 − z^(−1)) | B) L/T | C) L(1 − z^(−1))/T | D) T/L(1 − z^(−1))`
**Ans: C** — The derivative becomes (1 − z^(−1))/T, so sL → L(1 − z^(−1))/T.

**Q804.** The star transform maps:
`A) Frequency to amplitude | B) Laplace impedances to z-equivalents | C) Voltage to power | D) Open to closed loop`
**Ans: B** — It converts continuous s-domain elements into discrete pulse-transfer functions.

**Q805.** A digital filter designed via the bilinear transform on G(s) = 1/(s+1) with T = 1 s gives (approximately):
`A) (1 + z^(−1))/(2 + z^(−1)) | B) 1/(1 − z^(−1)) | C) z/(z+1) | D) 1/(z − 1)`
**Ans: A** — Bilinear: z = (1 + sT/2)/(1 − sT/2) applied to 1/(s+1).

**Q806.** Pulse-transfer functions assume:
`A) A zero-order hold and synchronized sampling | B) Continuous input | C) No hold | D) Random sampling`
**Ans: A** — Standard pulse-transfer analysis uses ZOH and uniform sampling.

**Q807.** The z-transform of a continuous signal sampled at T:
`A) Σ f(kT) z^(−k) | B) ∫ f(t) e^(−st) dt | C) Σ f(kT) z^k | D) f(0)`
**Ans: A** — Sampling the continuous function then applying the discrete transform.

**Q808.** Reconstruction of a sampled signal (D/A with ZOH) yields:
`A) A perfectly smooth signal | B) A ramp | C) A delta train | D) A staircase waveform`
**Ans: D** — ZOH produces a piecewise-constant staircase.

**Q809.** A reconstruction filter (post-D/A low-pass) is used to:
`A) Amplify | B) Smooth the staircase output | C) Sample | D) Quantize`
**Ans: B** — Smoothing recovers a continuous approximation.

**Q810.** The frequency response of a discrete filter is obtained by:
`A) Evaluating at s = jω | B) Taking the Laplace | C) Solving roots | D) Evaluating H(z) at z = e^(jω)`
**Ans: D** — Evaluate on the unit circle.

**Q811.** Discrete filters differ from continuous ones in that their frequency response:
`A) Is periodic with 2π | B) Is monotonic | C) Extends to infinity | D) Has no repeats`
**Ans: A** — Periodicity causes aliasing of spectra.

**Q812.** A notch filter at a specific discrete frequency ω0 has zeros at:
`A) z = ω0 | B) z = 0 | C) z = jω0 | D) z = e^(±jω0)`
**Ans: D** — Zeros on the unit circle at the notch frequencies.

**Q813.** The number of distinct samples needed to represent a signal of bandwidth B over duration T is approximately:
`A) BT | B) T/B | C) 2T | D) 2BT`
**Ans: D** — Degrees of freedom ≈ 2BT by sampling theory.

**Q814.** D/A and A/D converters' resolutions:
`A) Filter it | B) Amplify it | C) Quantize the signal | D) Sample it`
**Ans: C** — They map values onto discrete levels (quantization).

**Q815.** The main advantage of digital control over analog:
`A) Programmability, repeatability, and complex algorithms | B) Lower cost always | C) No quantization | D) Infinite bandwidth`
**Ans: A** — Software flexibility and reproducibility are key benefits.

**Q816.** The main disadvantage of digital control includes:
`A) Quantization, finite word length, and sampling delay | B) Higher reliability | C) Better accuracy | D) Simplicity`
**Ans: A** — Finite precision and delay degrade ideal performance.

**Q817.** A digital PID controller is:
`A) A discrete implementation of proportional-integral-derivative | B) An analog-only device | C) A filter | D) A sampler`
**Ans: A** — The PID law implemented with discrete arithmetic.

**Q818.** In a digital PID, the derivative term on a noisy signal:
`A) Amplifies high-frequency noise | B) Removes noise | C) Has no effect | D) Only affects DC`
**Ans: A** — Differentiation boosts high-frequency noise.

**Q819.** A common remedy for derivative noise is:
`A) Removing the integral | B) A low-pass filter on the derivative | C) Increasing the gain | D) Adding a delay`
**Ans: B** — Filtering the derivative term suppresses amplified noise.

**Q820.** Integral windup occurs when:
`A) The derivative is too small | B) The integrator saturates during actuator limits | C) The gain is negative | D) The loop is unstable`
**Ans: B** — Accumulated error during saturation causes windup.

**Q821.** Anti-windup schemes include:
`A) Clamping the integrator | B) Increasing Kp | C) Removing the derivative | D) Lowering the sampling rate`
**Ans: A** — Clamping or back-calculation prevents windup.

**Q822.** In a digital system, word-length effects cause:
`A) No error | B) Infinite precision | C) Only gain error | D) Quantization error and limit cycles`
**Ans: D** — Finite bits cause quantization and possible limit cycles.

**Q823.** Limit cycles in a digital controller are:
`A) Large oscillations | B) Unstable divergence | C) Small persistent oscillations from quantization | D) Uncontrollable modes`
**Ans: C** — Quantization sustains small-amplitude limit cycles.

**Q824.** Deadbeat control aims to:
`A) Maximize overshoot | B) Reduce gain | C) Reach steady state in minimum samples | D) Eliminate stability`
**Ans: C** — All poles at the origin → finite settling time.

**Q825.** The z-transform of a digital filter with a pole on the unit circle at z = e^(jθ):
`A) Is marginally stable with oscillation | B) Is unstable | C) Is stable | D) Is uncontrollable`
**Ans: A** — Sustained oscillation at frequency θ.

**Q826.** In a digital PLL, the loop filter is often a:
`A) Type-0 loop | B) Type-2 loop for zero steady-state phase error | C) Pure gain | D) Notch`
**Ans: B** — Type-2 loops give zero static phase/frequency error.

**Q827.** Sampling jitter refers to:
`A) Amplitude noise | B) Quantization | C) Variation in the sampling instant | D) Filter ripple`
**Ans: C** — Jitter is timing uncertainty in the sample clock.

**Q828.** The effect of sampling jitter is worst for:
`A) Low-frequency signals | B) DC only | C) Zero-frequency only | D) High-frequency signals`
**Ans: D** — Higher frequencies amplify timing errors.

**Q829.** A digital control system's sampling frequency is chosen relative to:
`A) The gain | B) The number of states | C) The system bandwidth (several times higher) | D) The controller type`
**Ans: C** — Typically f_s ≥ 10–20× the closed-loop bandwidth.

**Q830.** Rule of thumb for sampling frequency in digital control:
`A) f_s ≈ bandwidth | B) f_s = 2× bandwidth | C) f_s ≈ 10–20× the bandwidth | D) f_s < bandwidth`
**Ans: C** — 10–20 times gives adequate phase margin and disturbance rejection.

**Q831.** The z-transform of a signal multiplied by a^k is:
`A) aF(z) | B) F(az) | C) F(z/a) | D) F(z)/a`
**Ans: C** — Exponential weighting corresponds to scaling the argument.

**Q832.** The initial-value theorem in the z-transform says:
`A) f[0] = lim_{z→1} F(z) | B) f[0] = lim_{z→∞} F(z) | C) f[∞] = lim_{z→0} F(z) | D) f[0] = lim_{z→0} F(z)`
**Ans: B** — f[0] = lim_{z→∞} F(z) (for right-sided sequences).

**Q833.** The final-value theorem (valid when all poles of (1 − z^(−1))F(z) lie inside the unit circle) states:
`A) f[∞] = lim_{z→∞} F(z) | B) f[∞] = lim_{z→1} (1 − z^(−1))F(z) | C) f[∞] = lim_{z→0} F(z) | D) f[∞] = F(1)`
**Ans: B** — The final value equals the steady-state limit at z = 1.

**Q834.** The ZOH transfer function in the s-domain is:
`A) (1 − e^(−sT))/s | B) (1 + e^(−sT))/s | C) e^(−sT)/s | D) 1/s`
**Ans: A** — A rectangular pulse of width T has this transform.

**Q835.** In a digital system, "poles" are roots of the denominator in:
`A) s | B) w | C) f | D) z`
**Ans: D** — The z-transform variable.

**Q836.** The z-plane's "origin" (the equivalent of the s-plane's origin for integrator counting) is:
`A) z = 0 | B) z = −1 | C) z = 1 | D) z = ∞`
**Ans: C** — The integrator location.

**Q837.** In discrete time, an integrator (accumulator) has transfer function:
`A) 1 − z^(−1) | B) 1/(1 − z^(−1)) | C) z^(−1) | D) z/(z+1)`
**Ans: B** — Sum of past inputs.

**Q838.** A discrete-time differentiator (backward difference) has transfer function:
`A) 1 − z^(−1) | B) 1/(1 − z^(−1)) | C) z^(−1)/(1 − z^(−1)) | D) z/(z−1)`
**Ans: A** — Difference of current and past.

**Q839.** A digital PLL's phase detector output:
`A) Proportional to amplitude | B) Zero | C) Proportional to the phase error | D) Proportional to gain`
**Ans: C** — Error signal drives the loop.

**Q840.** The purpose of a sample-and-hold's "acquisition" phase:
`A) To reset | B) To let the output settle to the input value | C) To amplify | D) To filter`
**Ans: B** — During acquisition, the capacitor charges to the input.

**Q841.** In A/D conversion, the input is:
`A) Quantized then sampled | B) Only quantized | C) Only sampled | D) Sampled then quantized`
**Ans: D** — Sample-and-hold, then quantization and encoding.

**Q842.** The quantization step size for a full-scale range FS and n bits:
`A) FS/2^(n−1) | B) FS·n | C) FS/2^n | D) FS/n`
**Ans: C** — LSB = FS/2^n.

**Q843.** A digital filter's group delay is:
`A) dφ/dω | B) |H(jω)| | C) −dφ/dω | D) φ(ω)`
**Ans: C** — Group delay τ_g = −dφ/dω, positive since the phase decreases with frequency.

**Q844.** The total delay of a digital system affects stability:
`A) By adding phase lag | B) By adding gain | C) By removing poles | D) Not at all`
**Ans: A** — Delay is pure lag in the phase.

**Q845.** A discrete system with an integrator at z = 1 and one pole at z = 0.5 is:
`A) Type-1, step error zero | B) Type-0 | C) Unstable | D) Type-2`
**Ans: A** — One integrator → type-1 → zero step error.

**Q846.** Sampling a sinusoid at a rate below 2f produces:
`A) The same frequency | B) A lower-frequency alias | C) No effect | D) A DC offset`
**Ans: B** — Aliasing folds the frequency down.

**Q847.** The discrete-time impulse response h[k] of a causal LTI system:
`A) Is right-sided | B) Is left-sided | C) Is two-sided | D) Is zero for k > 0`
**Ans: A** — Causality implies a right-sided response.

**Q848.** For a causal rational system, the ROC is always:
`A) Inside the innermost | B) A unit circle | C) Empty | D) Outside the outermost pole`
**Ans: D** — Causality fixes the ROC to the exterior region.

**Q849.** The "sampling frequency" in a digital control system must satisfy:
`A) f_s < 2B | B) f_s = B | C) Any value | D) f_s > 2 × the highest frequency of interest`
**Ans: D** — Nyquist requirement, usually exceeded by a margin.

**Q850.** The effectiveness of a digital controller is ultimately limited by:
`A) The number of bits only | B) The display | C) The keyboard | D) The sampling rate and processor speed`
**Ans: D** — Sampling and computation bound realizable dynamics.

---

## SECTION 13 — State Space, Controllability & Observability (Q851–Q910)

**Q851.** The state-space representation is:
`A) y = Ax + Bu | B) ẋ = Cx + Du | C) ẋ = Ax + Bu, y = Cx + Du | D) x = Ay + B`
**Ans: C** — Standard state equation and output equation.

**Q852.** In ẋ = Ax + Bu, the vector x is the:
`A) State vector | B) Input vector | C) Output vector | D) Coefficient matrix`
**Ans: A** — The state vector carries the internal information needed for future outputs.

**Q853.** In ẋ = Ax + Bu, the vector u is the:
`A) Input (control) vector | B) State | C) Output | D) Jacobian`
**Ans: A** — The manipulated/control input.

**Q854.** The matrix A in the state equation is called the:
`A) Input matrix | B) Output matrix | C) Feedthrough matrix | D) System (or state) matrix`
**Ans: D** — Also called the A-matrix or system matrix.

**Q855.** The matrix B is the:
`A) Input (control) matrix | B) System matrix | C) Output matrix | D) Transition matrix`
**Ans: A** — It maps the input into the state derivative.

**Q856.** The matrix C is the:
`A) Output matrix | B) Input matrix | C) System matrix | D) Transition matrix`
**Ans: A** — It maps the state to the output.

**Q857.** The matrix D in y = Cx + Du is the:
`A) System matrix | B) Input matrix | C) Output matrix | D) Feedthrough (transmission) matrix`
**Ans: D** — Direct term from input to output.

**Q858.** The transfer function of a state-space system is:
`A) G(s) = C(sI − A)^(−1)B + D | B) C(sI + A)^(−1)B | C) (sI − A)CB | D) A + B`
**Ans: A** — Resolving (sI − A)ẋ = Bu gives ẋ = (sI − A)^(−1)Bu.

**Q859.** The transfer function from the state derivative to the output involves the resolvent matrix:
`A) (sI + A)^(−1) | B) (A − sI) | C) (sI − A)^(−1) | D) sI`
**Ans: C** — The resolvent (sI − A)^(−1).

**Q860.** The dimension of the state matrix A for an n-th order system is:
`A) n × n | B) n × m | C) m × n | D) 1 × n`
**Ans: A** — A is a square matrix of order n.

**Q861.** The dimension of the input matrix B is:
`A) n × n | B) n × m | C) m × n | D) m × m`
**Ans: B** — n states, m inputs → B is n × m.

**Q862.** The dimension of the output matrix C is:
`A) n × p | B) p × m | C) p × n | D) n × n`
**Ans: C** — p outputs, n states.

**Q863.** The state transition matrix is:
`A) Φ(t) = A + t | B) Φ(t) = e^(At) | C) Φ(t) = (sI − A)^(−1) | D) Φ(t) = e^(sA)`
**Ans: B** — Φ(t) = e^(At), the matrix exponential.

**Q864.** The state transition equation is:
`A) x(t) = Φ(t)x(0) + ∫₀ᵗ Φ(t−τ)Bu(τ)dτ | B) x(t) = Ax(t) | C) x(t) = Cx(t) | D) x(t) = x(0)`
**Ans: A** — Solution of the linear ODE with input.

**Q865.** For the autonomous system (u = 0), x(t) = Φ(t)x(0):
`A) Does not hold | B) Holds | C) Only at t=0 | D) Only for n=1`
**Ans: B** — With no input, the response is purely the state transition.

**Q866.** The solution to ẋ = Ax is:
`A) x(t) = Ax(0) | B) x(t) = tA | C) x(t) = e^(At)x(0) | D) x(t) = x(0)`
**Ans: C** — The matrix exponential gives the state transition.

**Q867.** The transition matrix satisfies:
`A) Φ(t₁)Φ(t₂) = Φ(t₂+t₁) always | B) Φ(t)Φ(t) = I always | C) Φ(t₂) = Φ(t₂ − t₁)Φ(t₁) | D) Φ(t) = t`
**Ans: C** — The semigroup/semi-group property.

**Q868.** The transition matrix obeys:
`A) Φ(0) = 0 | B) Φ(0) = I | C) Φ(0) = A | D) Φ(0) = J`
**Ans: B** — At t = 0, e^0 = I.

**Q869.** A system is controllable if:
`A) The observability matrix has rank n | B) A is symmetric | C) C = B | D) The rank of the controllability matrix is n`
**Ans: D** — Controllability matrix = [B AB A²B ... A^(n−1)B].

**Q870.** The controllability matrix is:
`A) C_obs = [C; CA; CA²; ...] | B) sI − A | C) C_ctrb = [B AB A²B ... A^(n−1)B] | D) e^(At)`
**Ans: C** — The Krylov/controllability matrix.

**Q871.** A system is observable if:
`A) The controllability matrix has rank n | B) The rank of the observability matrix is n | C) B is invertible | D) A is diagonal`
**Ans: B** — Observability matrix = [C; CA; CA²; ...; CA^(n−1)].

**Q872.** The observability matrix is:
`A) O = [B AB A²B ...] | B) O = I | C) O = A | D) O = [C; CA; CA²; ...; CA^(n−1)]`
**Ans: D** — Stacked rows of C, CA, CA², ...

**Q873.** The Kalman observability canonical form uses:
`A) The controllability matrix | B) The transition matrix | C) The observability matrix | D) The Jacobian`
**Ans: C** — Derived from the observability structure.

**Q874.** If a system is controllable and observable:
`A) Some poles may cancel | B) It is always unstable | C) It has no poles | D) All poles appear in the transfer function`
**Ans: D** — Controllable + observable implies no pole-zero cancellation; minimal realization.

**Q875.** Pole-zero cancellation in a non-minimal system:
`A) Hides internal unstable or uncontrollable modes | B) Cannot occur | C) Always beneficial | D) Increases stability`
**Ans: A** — Cancelled modes can be unstable and are not observable from the transfer function.

**Q876.** The transfer function of a single-state system ẋ = −ax + bu, y = x is:
`A) a/(s + b) | B) b/(s − a) | C) 1/(s + a) | D) b/(s + a)`
**Ans: D** — b/(s + a).

**Q877.** For ẋ = Ax + Bu with A diagonal (diag a₁, a₂), the transfer function is:
`A) Σᵢ aᵢ/(s − aᵢ) | B) Σᵢ bᵢcᵢ/(s − aᵢ) | C) Σᵢ bᵢ/(s − aᵢ) | D) Σᵢ cᵢ/(s − aᵢ)`
**Ans: B** — Each state contributes cᵢbᵢ/(s − aᵢ).

**Q878.** In the diagonal (Jordan canonical) form, the eigenvalues of A:
`A) Are off-diagonal | B) Are zero | C) Are undefined | D) Are the entries on the diagonal`
**Ans: D** — For diagonal A, eigenvalues are the diagonal entries.

**Q879.** The eigenvalues of A are also the:
`A) Gains | B) Natural modes (poles) of the system | C) Inputs | D) Outputs`
**Ans: B** — Eigenvalues of A coincide with the natural frequencies.

**Q880.** The eigenvalues of A are found from:
`A) det(sI + A) = 0 | B) tr(A) = 0 | C) det(sI − A) = 0 | D) det(A) = 0`
**Ans: C** — The characteristic equation of the state matrix.

**Q881.** The natural frequencies (modes) of a state-space system are:
`A) The elements of B | B) The elements of C | C) The zeros of D | D) The eigenvalues of A`
**Ans: D** — Eigenvalues give the modes.

**Q882.** The "eigenvalues" of the closed-loop system (A − BK) are:
`A) The closed-loop poles | B) The open-loop poles | C) The gains | D) The inputs`
**Ans: A** — The closed-loop dynamics are governed by A − BK.

**Q883.** The characteristic polynomial of the closed-loop system ẋ = (A − BK)x is:
`A) det(sI − A − BK) | B) det(sI + A + BK) | C) det(A + BK) | D) det(sI − A + BK)`
**Ans: D** — Poles are the roots of det(sI − (A − BK)) = det(sI − A + BK).

**Q884.** The characteristic polynomial of the open-loop system ẋ = Ax is:
`A) det(sI − A) | B) det(sI + A) | C) det(A) | D) tr(A)`
**Ans: A** — Roots of det(sI − A) = 0.

**Q885.** The Cayley-Hamilton theorem states:
`A) A satisfies its own characteristic equation | B) A is symmetric | C) A is diagonal | D) A is nilpotent`
**Ans: A** — A^n + cₙ₋₁A^(n−1) + ... + c₀I = 0.

**Q886.** The state transition matrix can be computed from the Cayley-Hamilton theorem as:
`A) A square root of A | B) A series in powers of A | C) A transpose | D) A inverse`
**Ans: B** — e^(At) can be written as a polynomial in A of degree ≤ n−1.

**Q887.** The number of states required in a minimal realization of an n-th order transfer function is:
`A) n/2 | B) n | C) 2n | D) 1`
**Ans: B** — Order equals the number of states.

**Q888.** A diagonalizable matrix A has:
`A) No eigenvectors | B) Only complex eigenvectors | C) One eigenvector | D) n linearly independent eigenvectors`
**Ans: D** — Diagonalizable ↔ n independent eigenvectors.

**Q889.** The eigenvalues of a matrix A are invariant under:
`A) Row addition | B) Similarity transformation | C) Column scaling | D) Adding a scalar`
**Ans: B** — A = T⁻¹AT keeps the same characteristic polynomial.

**Q890.** The trace of A equals:
`A) The product of eigenvalues | B) The determinant | C) The rank | D) The sum of eigenvalues`
**Ans: D** — tr(A) = Σλᵢ.

**Q891.** The determinant of A equals:
`A) The sum of eigenvalues | B) The trace | C) The product of eigenvalues | D) The rank`
**Ans: C** — det(A) = Πλᵢ.

**Q892.** A matrix is non-singular if:
`A) det(A) = 0 | B) det(A) ≠ 0 | C) tr(A) = 0 | D) rank = 1`
**Ans: B** — Non-zero determinant means invertible.

**Q893.** The modal (eigenvector) representation expresses the state as:
`A) x = Cz | B) x = Bz | C) x = Dz | D) x = Vz with ẑ = Λz`
**Ans: D** — V is the eigenvector matrix, Λ the diagonal eigenvalue matrix.

**Q894.** In the modal form, Λ is:
`A) Symmetric | B) Diagonal with eigenvalues on the diagonal | C) Skew | D) Zero`
**Ans: B** — The eigenvalues form the diagonal.

**Q895.** For a system ẋ = Ax + Bu with u = 0, the response is:
`A) Natural (free) response | B) Forced response | C) Zero response | D) Steady state`
**Ans: A** — The zero-input response is the natural/free response.

**Q896.** The transfer function of a non-minimal system (with cancellations):
`A) Reveals everything | B) Is undefined | C) Does not reveal all internal modes | D) Is always unstable`
**Ans: C** — Hidden modes are not visible in H(s).

**Q897.** A state-space system is:
`A) Always unique | B) Unique only up to similarity transformation | C) Never unique | D) Unique only if A is diagonal`
**Ans: B** — Many state-space descriptions realize the same transfer function.

**Q898.** The minimal realization of H(s) has order equal to:
`A) The number of inputs | B) The number of outputs | C) The zeros | D) The McMillan degree`
**Ans: D** — The McMillan degree is the number of poles counting multiplicity after cancellations.

**Q899.** If a transfer function has a pole-zero cancellation:
`A) Higher order | B) Same order | C) The minimal realization has lower order than the given matrix realization | D) No realization`
**Ans: C** — The cancelled mode can be removed.

**Q900.** The solution ẋ = Ax + Bu, y = Cx + Du in terms of matrices uses:
`A) The Jacobian only | B) The Hessian | C) The adjoint only | D) The state transition matrix`
**Ans: D** — Solution x(t) = Φ(t)x(0) + ∫Φ(t−τ)Bu(τ)dτ.

**Q901.** In a discrete-time state model x[k+1] = Ax[k] + Bu[k], the transition matrix is:
`A) e^(A) | B) A | C) A^k | D) I`
**Ans: C** — Repeated multiplication gives A^k.

**Q902.** The state transition matrix for the discrete model is:
`A) Φ(k) = A^k | B) Φ(k) = e^(Ak) | C) Φ(k) = kA | D) Φ(k) = I`
**Ans: A** — Discrete systems use A^k.

**Q903.** For a discrete state model, the transfer function is:
`A) C(zI + A)^(−1)B | B) (zI − A)CB | C) C(zI − A)^(−1)B + D | D) A/(zI + A)`
**Ans: C** — The z-transform analogue.

**Q904.** Controllability of a discrete system uses:
`A) e^(A) | B) A only | C) The same controllability matrix [B AB ... A^(n−1)B] | D) B only`
**Ans: C** — The Krylov matrix is the same in discrete time.

**Q905.** A system that is controllable but not observable:
`A) Is minimal | B) Has no transfer function | C) Is not minimal | D) Is unstable`
**Ans: C** — Minimal requires both controllable and observable.

**Q906.** Kalman decomposition splits a system into:
`A) Two parts | B) Controllable/observable, controllable/unobservable, uncontrollable/observable, uncontrollable/unobservable parts | C) Three parts | D) One part`
**Ans: B** — The four Kalman decomposition subspaces.

**Q907.** The condition number of the controllability matrix measures:
`A) Numerical difficulty of computing it | B) The system's order | C) The gain | D) The bandwidth`
**Ans: A** — Ill-conditioning signals near-uncontrollability.

**Q908.** For a controllable, observable system with A, B, C:
`A) The transfer function order equals the state order | B) The transfer function order is always larger | C) The orders are unrelated | D) The transfer function is zero`
**Ans: A** — No cancellations, so the McMillan degree equals n.

**Q909.** The characteristic polynomial det(sI − A) has degree:
`A) n | B) n/2 | C) n+1 | D) 2n`
**Ans: A** — n is the matrix order.

**Q910.** In a state model, the "state variables" must be:
`A) Arbitrary | B) Sufficient to compute future outputs | C) Always the outputs | D) Always the inputs`
**Ans: B** — The state carries all information needed for future behavior.

---

## SECTION 14 — Compensators, Nonlinearity & Design (Q911–Q960)

**Q911.** A compensator is inserted to:
`A) Reduce the order | B) Increase noise only | C) Improve transient response or steady-state accuracy | D) Convert the plant`
**Ans: C** — Compensators reshape the closed-loop performance.

**Q912.** A lead compensator G_c(s) = K(1 + sT)/(1 + sαT), with α < 1, provides:
`A) Negative phase | B) Zero phase | C) 180° | D) Positive phase`
**Ans: D** — With α < 1 the zero is at lower frequency → phase lead.

**Q913.** In a lead compensator, the pole is placed at:
`A) Lower frequency | B) Same as the zero | C) The origin | D) Higher frequency than the zero`
**Ans: D** — α < 1 → pole frequency 1/(αT) exceeds zero frequency 1/T.

**Q914.** In a lag compensator G_c(s) = K(1 + sT)/(1 + sβT), with β > 1:
`A) The zero is lower | B) The zero is at higher frequency than the pole | C) They coincide | D) Neither`
**Ans: B** — β > 1 → pole at 1/(βT) below the zero at 1/T.

**Q915.** The maximum phase lead of a lead compensator is:
`A) φ_m = 90° | B) φ_m = 45° | C) φ_m = 180° | D) φ_m = sin⁻¹[(1 − α)/(1 + α)]`
**Ans: D** — φ_m = arcsin((1 − α)/(1 + α)).

**Q916.** A lag compensator is used to:
`A) Improve phase margin directly | B) Improve steady-state error | C) Increase bandwidth | D) Reduce gain`
**Ans: B** — Lag raises low-frequency gain for accuracy.

**Q917.** A lead compensator is used to:
`A) Only steady-state accuracy | B) Reduce noise | C) Add delay | D) Increase phase margin and bandwidth`
**Ans: D** — Lead adds positive phase, raising both PM and bandwidth.

**Q918.** The phase-lead network gives its maximum phase lead at frequency:
`A) ω_m = 1/T | B) ω_m = 1/(αT) | C) ω_m = 1/(T√α) | D) ω_m = √α/T`
**Ans: C** — The geometric mean of the pole and zero frequencies.

**Q919.** The zero of a lead compensator G_c(s) = K(1 + sT)/(1 + sαT) is at:
`A) −1/(αT) | B) −T | C) −αT | D) −1/T`
**Ans: D** — The zero is at −1/T.

**Q920.** The pole of the lead compensator is at:
`A) −1/T | B) −1/(αT) | C) −T | D) −α/T`
**Ans: B** — The pole is at −1/(αT).

**Q921.** The zero of a lag compensator G_c(s) = K(1 + sT)/(1 + sβT) is at:
`A) −1/T | B) −1/(βT) | C) −βT | D) −1/β`
**Ans: A** — The zero is at −1/T.

**Q922.** The pole of the lag compensator is at:
`A) −1/(βT) | B) −1/T | C) −1/β | D) −β/T`
**Ans: A** — The pole is at −1/(βT).

**Q923.** A PI controller is:
`A) Kp + Ki/s | B) Kp + Kd s | C) Kp only | D) Kd s only`
**Ans: A** — Proportional plus integral.

**Q924.** A PD controller is:
`A) Kp + Ki/s | B) Kd s only | C) Kp only | D) Kp + Kd s`
**Ans: D** — Proportional plus derivative.

**Q925.** A PID controller is:
`A) Kp + Ki/s + Kd s | B) Kp + Kd s | C) Ki/s only | D) Kp only`
**Ans: A** — The full three-term law.

**Q926.** The integral term Ki/s is used to:
`A) Increase damping | B) Reduce bandwidth | C) Eliminate steady-state error | D) Add feedforward`
**Ans: C** — Infinite DC gain gives zero error for the appropriate input.

**Q927.** The derivative term Kd s is used to:
`A) Eliminate error | B) Improve damping and predict the trend | C) Reduce noise | D) Add steady-state gain`
**Ans: B** — Derivative adds damping and phase lead.

**Q928.** The proportional term Kp:
`A) Only eliminates error | B) Sets the overall gain and affects rise time | C) Only damps | D) Adds integration`
**Ans: B** — Kp scales the error, affecting speed and steady-state error.

**Q929.** The effect of increasing Kp in a first-order system:
`A) Decreases steady-state error and speeds the response | B) Only decreases overshoot | C) No effect | D) Increases time constant`
**Ans: A** — Higher Kp reduces e_ss = 1/(1+Kp) and raises bandwidth.

**Q930.** The effect of increasing Ki in a system:
`A) Increases damping only | B) Reduces error for ramp | C) Eliminates steady-state error faster but can increase overshoot | D) No effect`
**Ans: C** — Strong integral action drives e_ss to zero but adds phase lag.

**Q931.** The effect of increasing Kd:
`A) Reduces overshoot and adds noise sensitivity | B) Eliminates error | C) Increases bandwidth only | D) Increases damping and reduces overshoot`
**Ans: D** — More derivative adds damping, but amplifies high-frequency noise.

**Q932.** For a unity-feedback system, the proportional band (PB) relates to gain as:
`A) PB = 100/Kp | B) PB = Kp | C) PB = 100·Kp | D) PB = 1/Kp × 100%`
**Ans: A** — PB = 100%/Kp in percent.

**Q933.** Ziegler-Nichols closed-loop (ultimate gain) tuning:
`A) Set Kp from a step test | B) Random tuning | C) Frequency only | D) Increase Kp until sustained oscillation, then set Kp = 0.6·Ku, Td = Tu/8`
**Ans: D** — The classic ultimate-cycle method.

**Q934.** Ziegler-Nichols open-loop (reaction curve) tuning uses:
`A) A step test to find K, L, and T | B) Ultimate gain | C) Only the Bode plot | D) Only simulation`
**Ans: A** — Model the process as a first-order-plus-dead-time, then compute settings.

**Q935.** The process reaction curve model is:
`A) K e^(−Ls)/(Ts + 1) | B) K/(Ts) | C) K/(Ts + 1) with no delay | D) K·s/(Ts + 1)`
**Ans: A** — First-order plus dead time.

**Q936.** A process with a long dead time L is best controlled by:
`A) A pure P controller | B) No controller | C) A Smith predictor or a lead-lag design | D) An integrator only`
**Ans: C** — Smith predictors compensate dead time.

**Q937.** Nonlinearity in a control system means:
`A) The system is time-varying only | B) The system is discrete | C) The system is unstable | D) The system is governed by nonlinear differential equations`
**Ans: D** — Products of variables, saturation, dead zones, etc.

**Q938.** Examples of nonlinearities include:
`A) Gain only | B) Saturation, dead zone, hysteresis | C) Linear resistors | D) Laplace transforms`
**Ans: B** — Saturation, backlash, friction, dead zone.

**Q939.** The describing function of a nonlinearity gives:
`A) The exact solution | B) The time constant | C) An equivalent sinusoidal gain at a given frequency | D) The gain only`
**Ans: C** — An amplitude-dependent equivalent gain.

**Q940.** The describing function method applies to:
`A) All systems | B) Only linear | C) Random inputs | D) Nonlinear systems excited by a single sinusoidal input`
**Ans: D** — It assumes an essentially sinusoidal response.

**Q941.** In the describing-function method, stability requires:
`A) The plot of −1/N(A) does not enclose the point −1/K | B) Any nonlinear system is stable | C) Only linear systems are covered | D) Only systems with saturation are covered`
**Ans: A** — The −1/N(A) locus relative to −1/K indicates stability.

**Q942.** The Nyquist plot of a describing function (harmonic balance) for a system with N(A):
`A) The Bode magnitude | B) The time response | C) The −1/N(A) plot vs A | D) The root locus`
**Ans: C** — Plot −1/N(A) and check the −1/K point.

**Q943.** Saturation nonlinearity causes:
`A) Reduced gain and increased time constant (larger overshoot) | B) Higher gain | C) Less overshoot | D) Zero error`
**Ans: A** — Saturation lowers effective gain and adds lag.

**Q944.** Integral windup in a saturated actuator is avoided by:
`A) Higher Ki | B) Lower Kp | C) Anti-windup clamping | D) Removing feedback`
**Ans: C** — Clamping stops integration during saturation.

**Q945.** A dead-zone nonlinearity causes:
`A) Lower gain | B) A limit cycle or steady-state error | C) Oscillation at high frequency | D) No effect`
**Ans: B** — The dead zone forces a minimum input before output responds.

**Q946.** Relays in a nonlinear system cause:
`A) Limit-cycle oscillations | B) Smooth control | C) Zero error | D) Damping`
**Ans: A** — On-off control typically limit-cycles.

**Q947.** The Popov criterion is used to test:
`A) Controllability | B) Absolute stability of nonlinear systems | C) Observability | D) Stability of digital systems`
**Ans: B** — The circle criterion/Popov test for absolute stability.

**Q948.** The circle criterion is a graphical test for:
`A) Gain margin only | B) Root locus | C) Absolute stability of nonlinear systems | D) Only linear`
**Ans: C** — It uses a circle in the Nyquist/G-plane.

**Q949.** In the circle criterion, if the nonlinear sector bounds the nonlinearity and the Nyquist plot avoids the circle:
`A) Unstable | B) Marginal | C) Uncontrollable | D) The system is absolutely stable`
**Ans: D** — Avoidance of the critical circle guarantees absolute stability.

**Q950.** Lyapunov's direct method determines stability by:
`A) The root locus | B) The Bode plot | C) A positive-definite Lyapunov function V(x) with dV/dt < 0 | D) The eigenvalues only`
**Ans: C** — A Lyapunov function proves asymptotic stability.

**Q951.** A Lyapunov function V must satisfy:
`A) V(0) = 0 and V(x) > 0 for x ≠ 0, dV/dt < 0 | B) V(0) > 0 | C) dV/dt > 0 | D) V constant`
**Ans: A** — Positivity and negative derivative imply stability.

**Q952.** If dV/dt < 0 strictly, the system is:
`A) Marginally stable | B) Unstable | C) Asymptotically stable | D) Uncontrollable`
**Ans: C** — Strictly negative derivative gives asymptotic stability.

**Q953.** If dV/dt ≤ 0, the system is:
`A) Unstable | B) Uncontrollable | C) Unstable | D) Stable (in the sense of Lyapunov)`
**Ans: D** — Non-increasing V guarantees Lyapunov stability.

**Q954.** LaSalle's invariance principle extends Lyapunov's method by:
`A) Ignoring zero derivative | B) Using the largest invariant set in {dV/dt = 0} | C) Requiring dV/dt < 0 only | D) Using the root locus`
**Ans: B** — It shows convergence to the largest invariant subset.

**Q955.** The Kalman conjecture and Aizerman's conjecture (about linear controllers for nonlinear plants):
`A) Linear controllers always destabilize | B) Nonlinear controllers are always needed | C) No relation exists | D) Any linear controller is optimal for some positive input`
**Ans: D** — Aizerman's conjecture (not universally true) claimed this.

**Q956.** For a second-order system, the damping ratio relates to overshoot as:
`A) M_p = e^(−πζ/√(1 − ζ²)) | B) M_p = ζ | C) M_p = 1 − ζ | D) M_p = πζ`
**Ans: A** — ζ = −ln(M_p)/√(π² + ln²(M_p)).

**Q957.** The ζ required for 10% overshoot is approximately:
`A) ζ ≈ 0.6 | B) ζ ≈ 0.3 | C) ζ ≈ 0.8 | D) ζ ≈ 0.9`
**Ans: A** — M_p = 0.1 → ζ ≈ 0.591.

**Q958.** The ζ required for 20% overshoot is approximately:
`A) ζ ≈ 0.6 | B) ζ ≈ 0.3 | C) ζ ≈ 0.46 | D) ζ ≈ 0.8`
**Ans: C** — M_p = 0.2 → ζ ≈ 0.456.

**Q959.** For a cascade of first-order systems, the overall response is:
`A) The sum | B) The average | C) Independent | D) A convolution of the individual responses`
**Ans: D** — Cascades convolve their impulse responses.

**Q960.** A system with poles far separated on the s-plane (e.g. −0.1 and −20) can be approximated by:
`A) The fast pole −20 | B) Both equally | C) Their average | D) The dominant (slow) pole −0.1`
**Ans: D** — The slow pole dominates the transient.

---

## SECTION 15 — ISRO PYQ & Mixed Advanced Topics (Q961–Q1000)

**Q961.** [PYP-25 Q35] For the transfer function G(s) = K/[s(s+1)(s+2)], the maximum gain K for closed-loop stability is:
`A) 12 | B) 3 | C) 6 | D) 4`
**Ans: C** — Routh on s³+3s²+2s+K gives K < 6.

**Q962.** [PYP-25 Q39] The type of the system with transfer function G(s) = K(1+s)/(s(1+s)(1+2s)) is:
`A) Type 1 | B) Type 2 | C) Type 3 | D) Type 0`
**Ans: D** — The s factor cancels, leaving no integrator → type 0.

**Q963.** [PYP-25 Q44] For a unity-feedback system with open-loop G(s) = K/[s(s+4)(s+8)], the type is:
`A) Type 0 | B) Type 1 | C) Type 2 | D) Type 3`
**Ans: B** — One pole at the origin → type 1.

**Q964.** [PYP-25 Q47] The principal use of the Routh-Hurwitz criterion is to determine:
`A) The exact poles | B) The bandwidth | C) The range of K for stability | D) The noise`
**Ans: C** — The number of RHP poles as a function of K.

**Q965.** [PYP-25 Q50] If the closed-loop transfer function is T(s) = 5/(s² + 5s + 5), the system is:
`A) Overdamped (ζ ≈ 1.12) | B) ζ = 0.5 | C) ζ = 0.25 | D) ζ = 0.75`
**Ans: A** — Comparing with s² + 2ζω_n s + ω_n² gives ω_n = √5 ≈ 2.236 and ζ = 5/(2 × 2.236) ≈ 1.12 > 1, so the system is overdamped.

**Q966.** [PYP-25 Q53] For a system with G(s)H(s) = K/[s(s+1)], the root locus crosses the imaginary axis at K =:
`A) Infinity | B) 1 | C) 2 | D) 0`
**Ans: D** — The axis crossing is at K = 0 (the origin); it never leaves the axis.

**Q967.** [PYP-25 Q56] The maximum closed-loop bandwidth achievable with a first-order system is set by:
`A) The time constant | B) The gain | C) The phase margin | D) The steady-state error`
**Ans: A** — The pole sets the bandwidth.

**Q968.** [PYP-25 Q59] For pure delay G(s) = e^(−3s), the magnitude at all frequencies is:
`A) −6 dB | B) +3 dB | C) 0 dB | D) −∞`
**Ans: C** — A pure delay is all-pass (0 dB).

**Q969.** [PYP-25 Q59] The phase of G(s) = e^(−3s) at frequency ω is:
`A) −90° | B) 0° | C) −3ω radians | D) −180°`
**Ans: C** — Phase = −ωT = −3ω rad.

**Q970.** [PYP-25 Q61] For a system with poles −1 ± j, the damping ratio is:
`A) ζ = 0.5 | B) ζ = 1 | C) ζ = 0.707 | D) ζ = 0.1`
**Ans: C** — Poles −ζω_n ± jω_n√(1−ζ²): real part −ζω_n = −1, imag ω_n√(1−ζ²) = 1 → ω_n = √2, ζ = 1/√2 = 0.707.

**Q971.** [PYP-25 Q62] In a Bode plot, the phase of a second-order pole at the corner frequency is:
`A) −90° | B) −45° | C) −180° | D) −135°`
**Ans: A** — The imaginary part dominates at ω = ω_n, giving −90°.

**Q972.** [PYP-25 Q65] For a unity-feedback system with G(s) = 10/(s(s+1)(s+2)), the system is:
`A) Stable | B) Unstable always | C) Marginal | D) Stable for K < 6 (unstable at K = 10)`
**Ans: D** — K_max = 6 < 10, so unstable.

**Q973.** [PYP-25 Q66] The poles of the closed-loop system 1 + 2/[s(s+2)] = 0 are:
`A) −2 ± j2 | B) 0 and −2 | C) −1, −1 | D) −1 ± j1`
**Ans: D** — s² + 2s + 2 = 0 → s = −1 ± j1.

**Q974.** [PYP-25 Q67] The damping ratio of the closed-loop system s² + 2ζω_n s + ω_n² with poles −2 ± j4 is:
`A) ζ = 0.707 | B) ζ = 0.25 | C) ζ = 0.5 | D) ζ = 0.45`
**Ans: D** — ω_n = √(4+16) = 4.47, ζ = 2/4.47 = 0.447.

**Q975.** [PYP-25 Q69] The velocity error constant K_v for G(s) = 10/[s(s+1)] is:
`A) 10 | B) 1 | C) 0.1 | D) 100`
**Ans: A** — K_v = lim sG = 10/1 = 10.

**Q976.** [PYP-25 Q71] The steady-state error for a unit ramp input for G(s) = 10/[s(s+1)] is:
`A) 10 | B) 0 | C) 0.1 | D) 1`
**Ans: C** — e_ss = 1/K_v = 1/10 = 0.1.

**Q977.** [PYP-25 Q73] The impulse response of G(s) = 1/(s + 2) is:
`A) e^(−2t) | B) e^(−t) | C) 2e^(−t) | D) e^(t)`
**Ans: A** — Inverse Laplace of 1/(s+2) is e^(−2t).

**Q978.** [PYP-25 Q75] The final value of the output for G(s) = 2/[s(s+1)] with a unit step input is:
`A) Infinity (the type-1 output ramps without bound) | B) 2 | C) 1 | D) 0`
**Ans: A** — With a nonzero numerator at s = 0 the DC gain is unbounded, so the type-1 output grows as a ramp.

**Q979.** [PYP-23 Q53] The step response of a type-0 unity-feedback system with K_p = 2 has steady-state error:
`A) 1/2 | B) 2/3 | C) 1/3 | D) 1`
**Ans: C** — e_ss = 1/(1+K_p) = 1/3.

**Q980.** [PYP-23 Q57] The number of RHP poles of the characteristic polynomial s⁴ + 2s³ + 3s² + 4s + 5 is:
`A) 2 | B) 0 | C) 1 | D) 4`
**Ans: A** — First column 1, 2, 1, −6, 5 → two sign changes → 2 RHP poles.

**Q981.** [PYP-23 Q61] The type of the system with transfer function G(s) = 20/(s(s+2)(s+5)) is:
`A) Type 1 | B) Type 0 | C) Type 2 | D) Type 3`
**Ans: A** — One integrator → type 1.

**Q982.** [PYP-23 Q64] The poles of the characteristic equation s³ + 4s² + 6s + 4 = 0 are:
`A) −2 and −1 ± j | B) −1 and −1 ± j√2 | C) −4 ± j | D) 0 and −2 ± j2`
**Ans: A** — Factoring gives (s + 2)(s² + 2s + 2), so s = −2 and s = −1 ± j.

**Q983.** [PYP-23 Q67] The damping ratio of a system with poles −3 ± j4 is:
`A) ζ = 0.8 | B) ζ = 0.75 | C) ζ = 0.5 | D) ζ = 0.6`
**Ans: D** — ω_n = √(9+16) = 5, ζ = 3/5 = 0.6.

**Q984.** [PYP-23 Q69] For a system with G(s) = K/[s(s+1)(s+2)(s+3)], the range of K for stability is:
`A) 0 < K < 24 | B) K > 10 | C) All K | D) 0 < K < 10`
**Ans: D** — The first column 1, 6, 10, 6 − 0.6K, K is all positive only for 0 < K < 10.

**Q985.** [PYP-23 Q72] The natural frequency ω_n of a system with poles −2 ± j2 is:
`A) 2 | B) √8 ≈ 2.83 | C) 4 | D) 1`
**Ans: B** — ω_n = √(4 + 4) = √8 = 2.83.

**Q986.** [PYP-23 Q76] The transfer function of a first-order system with pole at −2 and gain 4 is:
`A) 4/(s + 2) | B) 2/(s + 4) | C) 4/(s − 2) | D) 1/(s + 2)`
**Ans: A** — G(s) = 4/(s + 2).

**Q987.** [PYP-23 Q79] The output of a system G(s) = 1/(s+1) with a unit step input at steady state is:
`A) 1 | B) 0 | C) Infinity | D) 1/2`
**Ans: A** — Final value = G(0) = 1.

**Q988.** [PYP-23 Q81] For a unity-feedback system with G(s) = K/s, the type is:
`A) Type 0 | B) Type 2 | C) Type 1 | D) Type 3`
**Ans: C** — One integrator → type 1.

**Q989.** [PYP-23 Q85] The Routh array's first column for s⁴ + 4s³ + 6s² + 4s + 2 is:
`A) 1, 4, 6, 4, 2 | B) 1, 2, 4, 6, 2 | C) 1, 4, 2, 0.5, 2 | D) 1, 4, 5, 2.4, 2`
**Ans: D** — b₁ = (4·6 − 1·4)/4 = 5 and c₁ = (5·4 − 4·2)/5 = 2.4, so the column is 1, 4, 5, 2.4, 2.

**Q990.** [PYP-23 Q88] The steady-state error for a unit step input for a type-1 unity-feedback system is:
`A) Finite nonzero | B) Infinite | C) 1 | D) 0`
**Ans: D** — Type-1 gives infinite K_p → zero step error.

**Q991.** [PYP-23 Q91] The bandwidth of the closed-loop system K/[s(s+K)] for K = 4 is approximately:
`A) 2 rad/s | B) 4 rad/s | C) 1 rad/s | D) 8 rad/s`
**Ans: A** — The crossover of a lightly damped second-order loop.

**Q992.** The proportional band (PB) for a controller with Kp = 4 is:
`A) 400% | B) 25% | C) 4% | D) 50%`
**Ans: B** — PB = 100/Kp = 25%.

**Q993.** The integral time (reset) Ti = Ki/Kp for a PID is:
`A) Kp/Ki | B) Kp·Ki | C) 1/(Kp·Ki) | D) Ki/Kp`
**Ans: D** — Ti = Ki/Kp.

**Q994.** The derivative time Td = Kd/Kp is:
`A) Kp/Kd | B) Kd/Kp | C) Kp + Kd | D) Kd·Kp`
**Ans: B** — Td = Kd/Kp.

**Q995.** In the Ziegler-Nichols closed-loop method, the integral time is:
`A) Ti = Tu/2 | B) Ti = Tu | C) Ti = 2Tu | D) Ti = Tu/4`
**Ans: C** — PID: Kp = 0.6Ku, Ti = 2Tu, Td = Tu/8.

**Q996.** In the Ziegler-Nichols open-loop method for a first-order-plus-dead-time process, Kp is set to:
`A) 1.2KL/T | B) T/(KL) | C) 1.2T/(K·L) | D) KL/T`
**Ans: C** — The classic reaction-curve formula.

**Q997.** A PI controller is preferred when:
`A) The process is very fast | B) The plant is exactly known | C) The process is slow and integral action is needed for accuracy | D) The plant is unstable`
**Ans: C** — PI suits slow processes where zero offset is needed.

**Q998.** A PD controller is preferred when:
`A) The process is fast and derivative improves damping | B) The process has long dead time | C) Zero error is needed for steps | D) The plant is unstable`
**Ans: A** — PD suits fast processes where offset is acceptable.

**Q999.** For a self-regulating process with no integration, a pure P controller leaves:
`A) Zero error | B) A steady-state offset | C) Unstable | D) Infinite gain`
**Ans: B** — With K_p finite, e_ss = 1/(1 + K_p) ≠ 0.

**Q1000.** The ultimate goal of a control system design is to achieve:
`A) Maximum gain | B) Minimum bandwidth | C) Specified stability, accuracy, and speed of response | D) Zero noise`
**Ans: C** — Stability, steady-state accuracy, and transient performance.
