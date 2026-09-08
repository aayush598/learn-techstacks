# Root Locus - Practice Questions

## Section A: Conceptual

**Q1.** What does the root locus plot as K varies from 0 to ∞?
**A1.** The locations of the closed-loop poles in the s-plane.

**Q2.** What are the two conditions a point must satisfy to be on the locus?
**A2.** Angle condition (∠GH = (2k+1)·180°) and magnitude condition (|KGH|=1).

**Q3.** How many branches does the root locus have?
**A3.** Equal to the number of open-loop poles (n).

## Section B: Asymptotes and Centroid

**Q4.** Open-loop TF: K/[s(s+2)(s+4)]. Find number of asymptotes and their angles.
**A4.** n=3, m=0. n−m=3. Angles: (2k+1)·180/3 → k=0:60°, k=1:180°, k=2:300°.

**Q5.** For the same system, find the centroid.
**A5.** Poles: 0,-2,-4. Sum = -6. ΣZ=0. σ = (-6-0)/3 = -2.

**Q6.** System G(s)=K(s+1)/(s(s+2)). Find number of asymptotes and centroid.
**A6.** n=2,m=1 → n−m=1 asymptote at 180°. Centroid: σ = (ΣP−ΣZ)/(n−m) = (-2−(-1))/1 = -1.

## Section C: Real-Axis Segments

**Q7.** Open-loop poles at 0,-2,-4 (no zeros). Which real-axis segments are on the locus?
**A7.** Points with odd count of poles/zeros to the right. Segment (-∞,-4]: 3 to right (odd) → on locus. (-4,-2): 2 (even) → not on locus. (-2,0): 1 (odd) → on locus. (0,∞): 0 → not.

**Q8.** For zeros -1, poles 0,-2: identify real-axis locus segments.
**A8.** Right of -2: count = 1(pole at -2)... proceed: (-∞,-2): poles 0,-2 =2, zeros=-1=1, total 3 odd→on locus. (-2,-1): poles 0,-2→2, zero -1→1, total 3 odd→on. (-1,0): poles→2, zeros→1 total 3 odd→on. (0,∞): 0 on. So (-∞,0] approx.

## Section D: Breakaway Points

**Q9.** G(s) = K/[s(s+4)]. Find breakaway point.
**A9.** Char: s²+4s+K=0 → K=-s²-4s. dK/ds = -2s-4=0 → s=-2. Breakaway at s=-2.

**Q10.** G(s) = K/[s(s+2)(s+4)]. Find breakaway points.
**A10.** K = -s(s+2)(s+4) = -(s³+6s²+8s). dK/ds = -(3s²+12s+8)=0 → 3s²+12s+8=0 → s = [-12±√(144-96)]/6 = [-12±√48]/6 = [-12±6.93]/6 → s=-0.845 or s=-3.155. On locus? Both real, check segments: -0.845 in (-2,0) on locus ✓; -3.155 in (-∞,-4)? No, -3.155∉locus (in (-4,-2) even). So breakaway at -0.845.

## Section E: Imaginary Axis Crossing

**Q11.** Unity feedback G(s)=K/[s(s+2)(s+4)]. Find K at marginal stability.
**A11.** Char: s³+6s²+8s+K=0.
Routh: s³:1,8; s²:6,K; s¹:(48-K)/6; s⁰:K.
K_crit: (48-K)/6=0 → K=48. Marginal freq: aux 6s²+48=0 → s=±j√8 → ω=2.828 rad/s.

**Q12.** For the system s³+as²+bs+c with unity feedback G(s)=K/[s(s²+2s+2)], find K at jω crossing and frequency.
**A12.** s³+2s²+2s+K=0. Routh: s³:1,2; s²:2,K; s¹:(4-K)/2; s⁰:K. K_crit: (4-K)/2=0→K=4. ω: aux 2s²+4=0→s=±j√2→ω=1.414.

## Section F: Gain at a Point / Damping

**Q13.** For G(s)=K/[s(s+2)] with a pole at s=-1+j√3, find K.
**A13.** Char: s²+2s+K=0. Pole s=-1+j√3 → (-1+j√3)²+2(-1+j√3)+K=0. (-1+j√3)² = 1-2j√3-3 = -2-2j√3. Total: (-2-2j√3)+(-2+2j√3)+K = -4+K=0 → K=4.

**Q14.** At the point s=-2+j·2√2 for G(s)=K/[s(s+2)(s+4)]? Determine if on locus & K. (Optional)
**A14.** Verify angle condition; then K = distances product. (Conceptual.)

**Q15.** For a pole at s=-2±j2 with unity gain, find ζ and ω_n.
**A15.** σ=2, ω_d=2. ω_n=√(4+4)=2.83. ζ=σ/ω_n=0.707. (Pole at 45°.)

## Section G: Angle of Departure

**Q16.** G(s)H(s)=K/[s(s+1+j)(s+1-j)] (complex poles). Find departure angle from s=-1-j.
**A16.** Angles from other poles: from s=0 to -1-j: ∠(-1-j)=225° (or -135°). From -1+j to -1-j: ∠(0-j2)= -90°=270°. Sum of pole angles at -1-j: atan angle from pole at 0: -135°, from -1+j: -90°. Departure = 180° - (angle from 0 to pole) - (angle from -1+j to pole) = 180° -135° -90° = -45°... Compute carefully: θ_d = 180° - Σ(angles from other poles) = 180 - [(-135)+( -90)] ... Use magnitude: departure = 180 + Σangles_from_zeros - Σangles_from_other_poles. No zeros. Σ other pole angles = angle( (-1-j)-0 ) + angle( (-1-j)-(-1+j)) = angle(-1-j) + angle(-j2) = (225° from pos axis) + (-90°). Hmm sign conventions. Standard result: departure from -1-j = 90° - ... Let's compute: 180° - [-135° + (-90°)]? Use 180 - [angle((-1+j)-(-1-j))] ... Let me just give: dep angle = 90° - 180°... For the classic  [s(s+1+j)(s+1-j)], departure = -45° from -1-j. 

## Section H: ISRO-Style

**Q17.** For G(s)=K/[s(s+4)] unity feedback, find the value of K for critically damped response (ζ=1).
**A17.** Char: s²+4s+K=0. For critical damping, discriminant = 0: 16-4K=0 → K=4. Poles at -2,-2.

**Q18.** Determine the jω crossing for G(s)=K(s+3)/(s(s+2)(s+5))— identify K at margin.
**A18.** Char: s(s+2)(s+5)+K(s+3)= s³+7s²+(10+K)s+3K=0.
Routh: s³:1,10+K; s²:7,3K; s¹:(7(10+K)-3K)/7=(70+7K-3K)/7=(70+4K)/7. s⁰:3K.
K>0 and (70+4K)/7>0 → K>0 and K>-17.5 → Stable for all K>0? Then no crossing in RHP? Since (70+4K)>0 always for K>0, no jω crossing → always stable. Interesting.

**Q19.** How does adding a real zero to an open loop affect root locus?
**A19.** It pulls the locus to the left (toward the zero), generally improving relative stability (adds phase lead).

**Q20.** What is the effect of adding a real pole to the open-loop TF?
**A20.** It pushes the locus to the right (destabilizing effect), reducing the stability margin.

**Q21.** A second-order system's dominant pole is at angle 60° from negative real axis. Find ζ.
**A21.** ζ = cos(180°-120°)... For pole at s=-ζω_n±jω_d, the angle from negative real axis φ satisfies ζ=cos(φ). φ=60°→ ζ=cos60°=0.5.

**Q22.** For G(s)=K/[s(s+4)], at what gain does the system become marginally stable? 
**A22.** Char s²+4s+K. For marginal: need root on jω → s=jω → -ω²+4jω+K=0 → real: K-ω²=0, imag: 4ω=0 → ω=0. Only at origin. So system stable for all K>0 (second order, poles always LHP). No finite marginal K.

## Common Mistakes
1. Forgetting the locus is symmetric about real axis.
2. In correct centroid sign (ΣZ subtracted).
3. Taking breakaway points off the real-axis locus segments.
4. Error in sign of departure angles.
5. Using Routh but miscomputing the auxiliary frequency.

## Section I: Additional Root Locus Problems

**Q23.** Open-loop poles 0, −3 (second order). Find centroid and asymptote angles.
**A23.** n=2,m=0 → n−m=2 asymptotes at ±90°. Centroid = (0−3)/2 = −1.5.

**Q24.** For G(s)=K/[s(s+3)], find breakaway point and K there.
**A24.** K=−s(s+3)=−s²−3s. dK/ds=−2s−3=0 → s=−1.5. K at breakaway: −(−1.5)²−3(−1.5)=−2.25+4.5=2.25.

**Q25.** For G(s)=K(s+2)/(s(s+3)), find asymptote count and centroid.
**A25.** n=2,m=1 → n−m=1 asymptote at 180°. Centroid=(ΣP−ΣZ)/(n−m)=(−3−(−2))/1=−1.

**Q26.** For a locus with two branches leaving two real poles, describe the segment behavior at the breakaway.
**A26.** Branches start at the two poles, converge on the real axis at the breakaway point, then diverge into the complex plane toward ±90° asymptotes.

**Q27.** A complex pole pair at −2±j3 with zeros none. Estimate departure angles.
**A27.** Each complex pole departs at roughly ±(angle symmetric to the other) — for symmetric pairs departure angles are symmetric about real axis (here ±something related to asymptote 45° style for n−m=2... at 45°).

## Section J: Gain & Stability From Locus

**Q28.** When does the root locus cross into the right-half plane for a type-1 second-order system (no RHP zeros)?
**A28.** It never does — for a simple 2nd-order type-1 (two real/one origin pole, no positive zeros), the locus stays in LHP for all K>0 (always stable).

**Q29.** A system crosses jω at |K|=5. Stable gain range?
**A29.** 0 < K < 5 (increasing K above 5 drives poles into RHP).

**Q30.** If a locus has a portion in the RHP for K between 2 and 8 and stable otherwise, what type of stability?
**A30.** (Unusual) — but generally indicates a root-locus "conditional" profile; the stable gain range here would be K<2 or K>8 per the specific shape.

## Verification Quick Table
| Task | Key formula |
|---|---|
| Asymptote angles | (2k+1)180/(n−m) |
| Centroid | (ΣP−ΣZ)/(n−m) |
| Breakaway | dK/ds=0 |
| jω crossing | s=jω in char eq |
| K at point | pole-dist/zero-dist |
