# Subject-Wise Test - Control Systems

## 20 Questions, 25 Minutes, +1/−0.33

## Questions

**Q1.** A causal continuous-time LTI system is BIBO stable when all poles are:

A. In the open left-half plane  
B. On the imaginary axis  
C. In the right-half plane  
D. At the origin only

**Q2.** The system `G(s)=1/(s+2)` with unity negative feedback is:

A. Stable  
B. Unstable  
C. Marginally stable  
D. Uncontrollable

**Q3.** A second-order system with damping ratio 0.5 is:

A. Overdamped  
B. Underdamped  
C. Critically damped  
D. Undamped

**Q4.** The characteristic polynomial `s²+6s+9` has:

A. Two distinct real roots  
B. One repeated root at −3  
C. A complex-conjugate pair  
D. A root at zero

**Q5.** For `s²+2ζω₀s+ω₀²`, the damping ratio is:

A. `ω₀/(2ζ)`  
B. `2ζω₀`  
C. `ζ`  
D. `ω₀²/2`

**Q6.** A unity-feedback type-1 system has zero steady-state error for:

A. Ramp input  
B. Parabolic input  
C. Step input  
D. Any input

**Q7.** A proportional-only controller usually:

A. Eliminates ramp steady-state error  
B. Reduces step steady-state error but leaves a ramp error  
C. Guarantees zero error for all inputs  
D. Integrates plant state

**Q8.** An integral controller is introduced mainly to:

A. Reduce steady-state error  
B. Increase natural frequency only  
C. Remove all noise  
D. Eliminate actuator limits

**Q9.** The number of right-half-plane poles equals the number of sign changes in:

A. The last column of the Routh array  
B. The first column of the Routh array  
C. The numerator coefficients only  
D. The gain margin

**Q10.** Gain margin at a phase-crossover frequency is:

A. `−180°−phase`  
B. `1/|T(jωpc)|`  
C. `|T(jωgc)|`  
D. The closed-loop pole count

**Q11.** Phase margin at gain-crossover frequency is:

A. `180°+∠T(jωgc)`  
B. `∠T(jωgc)` only  
C. `1/|T(jωgc)|`  
D. The delay in seconds

**Q12.** Nyquist stability analysis directly concerns:

A. Poles and zeros in the complex plane only  
B. Encirclement of `−1` by the open-loop frequency plot  
C. Time-domain settling time only  
D. State controllability

**Q13.** Increasing gain margin usually makes a feedback system:

A. Less robustly stable  
B. More robustly stable, all else equal  
C. Nonlinear regardless of margin  
D. Unobservable

**Q14.** An `n`-state state-space model has an `n×n` state matrix:

A. Only for MIMO systems  
B. Always  
C. Only if inputs equal states  
D. Only in discrete time

**Q15.** The characteristic polynomial is obtained from:

A. `sI−A`  
B. `B⁻¹C` only  
C. The controllability matrix  
D. The observability matrix

**Q16.** The controllability matrix is formed from:

A. `[B AB … Aⁿ⁻¹B]`  
B. `[C A Cᵀ …]` only  
C. The state-transition matrix  
D. The output matrix

**Q17.** The observability matrix is formed from:

A. `[C; CA; …; CAⁿ⁻¹]`  
B. `[B AB …]` only  
C. The identity matrix  
D. The feedforward matrix

**Q18.** If a state variable moves farther into the left-half plane, the system generally becomes:

A. More damped  
B. More unstable  
C. Noncausal  
D. Nonobservable

**Q19.** For unity feedback, the sensitivity function is:

A. `1/(1+T)`  
B. `1+T`  
C. `T/(1+T)`  
D. `1−T`

**Q20.** Negative feedback can improve stability and sensitivity, but it may also:

A. Reduce bandwidth and introduce delay-related margin limits  
B. Always eliminate every disturbance  
C. Make every system nonlinear  
D. Eliminate all poles

## Answer Key

| Question | Answer | Question | Answer |
|---:|:---:|---:|:---:|
| 1 | A | 11 | A |
| 2 | A | 12 | B |
| 3 | B | 13 | B |
| 4 | B | 14 | B |
| 5 | C | 15 | A |
| 6 | C | 16 | A |
| 7 | B | 17 | A |
| 8 | A | 18 | A |
| 9 | B | 19 | A |
| 10 | B | 20 | A |

## Quick Solutions

1. Every BIBO pole of a causal rational system must lie in the open left-half plane.  
10. `GM=1/|T(jωpc)|` with magnitude in dB written as `−20log10|T(jωpc)|`.  
11. `PM=180°+∠T(jωgc)`.  
19. `S=1/(1+T)` maps loop-gain variations to output sensitivity.
