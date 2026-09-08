# Bode Plots - Practice Questions

## Section A: Conceptual

**Q1.** What two plots make up a Bode plot?
**A1.** Magnitude (in dB vs log ω) and phase (in degrees vs log ω).

**Q2.** What is the slope of a single real pole after its corner frequency?
**A2.** −20 dB/decade.

**Q3.** Define gain crossover frequency.
**A3.** The frequency where |G(jω)| = 1 (0 dB).

**Q4.** Define phase crossover frequency.
**A4.** The frequency where ∠G(jω) = −180°.

## Section B: Slope & Corner Determination

**Q5.** G(s) = 10(1+0.1s)/(s(1+s)). Identify corners and type.
**A5.** Type 1 (one integrator) → starting slope −20 dB/dec. Zeros: corner at ω=1/0.1=10. Poles: corner at ω=1. Phase: −90° base.

**Q6.** For G(s)=1/[s(1+s/2)(1+s/100)], find corner frequencies.
**A6.** Integrator (type 1). Pole corner at ω=2 (T=0.5), another pole corner at ω=100 (T=0.01).

**Q7.** What is the slope after each of the two corners in Q6?
**A7.** After ω=2: −40 dB/dec. After ω=100: −60 dB/dec.

**Q8.** Determine the initial slope of G(s)=100s/(s+10).
**A8.** G(s)=100s/(10(1+s/10)) = 10s/(1+s/10). Has differentiator (s) → +20 dB/dec start. Pole corner at ω=10 (−20). Net after 10: 0 dB/dec.

## Section C: Gain/Phase Margin from Bode

**Q9.** On a Bode plot, |G(jω)| = 0 dB at ω=5 rad/s where phase = −150°. Find PM.
**A9.** PM = 180° + (−150°) = 30°.

**Q10.** At phase crossover, |G| = −12 dB. Find gain margin.
**A10.** GM = −(−12) = +12 dB. (Positive, stable.)

**Q11.** If at phase crossover |G| = +6 dB, what is the gain margin and is it stable?
**A11.** GM = −6 dB. Negative → unstable (needs gain reduction of 6 dB).

**Q12.** Gain crossover at ω=10 where phase=−135°. PM?
**A12.** PM = 180−135 = 45°.

## Section D: Transfer Function Identification

**Q13.** A Bode magnitude plot starts at −20 dB/dec, then flattens to 0 dB after ω=2, then −20 dB/dec after ω=20. Identify G(s) (type & corners).
**A13.** Starts −20 → type 1 (one integrator). Flattens at ω=2 → one real pole corner at 2. Slopes −20 again at ω=20 (pole at 20). So G(s)=K/[s(1+s/2)(1+s/20)].

**Q14.** The plot in Q13 has magnitude 0 dB at ω=1 before flattening. Estimate K.
**A14.** 20log|K|=20log(K)... At ω=1, |G|=1. Actually magnitude at ω=1: K/(1·(approx1)) — estimate K≈1. (Consistent with 0dB at ω=1.)

**Q15.** A plot shows -40 dB/dec from low frequency with no prior flat segment. What type?
**A15.** Type 2 (two integrators).

**Q16.** Magnitude plot: flat 20 dB until ω=10, then −20 dB/dec. Identify transfer function.
**A16.** DC gain: 20dB → 20log10(K0)=20 → K0=10. Pole at ω=10. G(s)=10/(1+s/10)=100/(s+10).

## Section E: Second-Order/Complex Poles

**Q17.** A complex pole pair with ζ=0.2, ω_n=10. Find the resonant peak magnitude in dB.
**A17.** M_r ≈ 1/(2ζ√(1−ζ²)) = 1/(0.4·0.98) ≈ 1/0.392 ≈ 2.55. In dB: 20log(2.55) ≈ 8.1 dB.

**Q18.** For the above, find frequency of resonance ω_r.
**A18.** ω_r = ω_n√(1−2ζ²) = 10√(1−0.08) = 10√0.92 ≈ 9.59 rad/s.

**Q19.** After a complex pole pair corner, the slope changes by how much?
**A19.** −40 dB/decade.

## Section F: Designing K for Desired PM

**Q20.** G(s)=K/[s(s+2)]. Find K for PM=45°.
**A20.** |G(jω)|=K/(ω√(ω²+4)). Phase = −90° − atan(ω/2). For PM=45: phase must be −135° → atan(ω/2)=45° → ω/2=1 → ω=2. At ω=2, |G|=K/(2√8)=K/(2·2.83)=K/5.66. Set =1 → K=5.66.

**Q21.** Verify Q20 gives PM=45°.
**A21.** At ω=2: phase = −90−45=−135. |G|=1. PM=180−135=45. ✓

## Section G: ISRO-Style

**Q22.** A Bode magnitude plot has low-frequency slope −20 dB/dec and passes through 0 dB at ω=4 rad/s, flattening at ω=8. Find an approximate transfer function.
**A22.** Type 1. Integrator gives |K/ω|=1 at ω=4 → K=4. Pole corner at ω=8 (T=0.125). G(s)=4/[s(1+s/8)].

**Q23.** Identify the system that has Bode magnitude: starts 0 dB flat, corner at ω=2 (−20 dB/dec), corner at ω=50 (−40 db/dec), no zeros.
**A23.** DC gain K0: 0dB→K0=1. Poles at ω=2 and ω=50. G(s)=1/[(1+s/2)(1+s/50)].

**Q24.** For G(s)=5/[s(1+s)(1+0.1s)], what is the starting phase and slope?
**A24.** Type 1. Starting slope −20 dB/dec, starting phase −90°.

**Q25.** A system has GM=+∞ and PM=60°. Why is GM infinite?
**A25.** No phase crossover (phase never reaches −180°, e.g., pure first/second order) → gain can be increased indefinitely without reaching −180° → infinite gain margin.

**Q26.** Given phase crossover at ω_pc where |G(jω_pc)|=0.5, find GM in dB and state stability of a stable system.
**A26.** GM=20log10(1/0.5)=20log10(2)=6.02 dB. Positive → stable.

**Q27.** The phase at gain crossover is −170°. PM = ?
**A27.** PM = 180 − 170 = 10° (small margin, near instability).

**Q28.** A Bode plot for G(s) shows slope starting at −40 dB/dec. Likely type number?
**A28.** Type 2 (two integrators).

## Common Mistakes
1. Confusing gain & phase crossover frequencies.
2. GM sign: positive dB = stable.
3. Reading corner frequencies off incorrectly (should be 1/T).
4. Using dB values without converting to linear for GM/PM.
5. Forgetting delay adds phase lag without magnitude change.
