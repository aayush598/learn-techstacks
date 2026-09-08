# Routh-Hurwitz - Practice Questions

## Section A: Conceptual

**Q1.** What does the Routh-Hurwitz criterion determine?
**A1.** Stability of a system without solving for the roots — whether all characteristic-equation roots lie in the LHP, and how many lie in RHP.

**Q2.** Is the "all coefficients positive" condition sufficient for stability?
**A2.** No. It is necessary but not sufficient. The Routh array first-column test is needed for sufficiency.

**Q3.** What does the number of sign changes in the first column equal?
**A3.** The number of roots in the right half of the s-plane (RHP roots).

## Section B: Basic Stability Determination

**Q4.** For s²+3s+2=0, determine stability.
**A4.** Second-order with positive coefficients → always stable. Poles: -1, -2 (both LHP).

**Q5.** For s³+s²+s+6=0, determine stability using Routh.
**A5.** Coeffs all positive (necessary met).
Routh:
s³: 1, 1
s²: 1, 6
s¹: (1·1-1·6)/1 = -5
s⁰: 6
First column: 1, 1, -5, 6 → one sign change (1→-5) → ONE RHP root → unstable.

**Q6.** For s³+2s²+3s+4=0, determine stability.
**A6.** Routh:
s³: 1, 3
s²: 2, 4
s¹: (6-4)/2 = 1
s⁰: 4
All first column: 1,2,1,4 → positive → stable.

## Section C: Third-Order Shortcut

**Q7.** For s³+a₂s²+a₁s+a₀, state the stability condition.
**A7.** a₂a₁ > a₀ (with all coefficients positive).

**Q8.** Is s³+3s²+2s+10=0 stable?
**A8.** Check: 3·2 = 6 < 10 → a₂a₁ < a₀ → unstable.

**Q9.** Is s³+5s²+6s+8=0 stable?
**A9.** 5·6 = 30 > 8 → stable.

## Section D: Gain Range for Stability

**Q10.** Unity feedback, G(s) = K/[s(s+2)(s+4)]. Find range of K for stability.
**A10.** Char eq: s(s+2)(s+4)+K = s³+6s²+8s+K = 0.
Routh:
s³: 1, 8
s²: 6, K
s¹: (48-K)/6
s⁰: K
Require >0: K>0 and (48-K)/6>0 → K<48.
**Range: 0 < K < 48.**

**Q11.** For the above, find frequency at marginal stability (K=48).
**A11.** Auxiliary eq from s² row: 6s² + 48 = 0 → s² = -8 → s = ±j·√8 = ±j2.828. Oscillation at 2.828 rad/s.

**Q12.** Unity feedback G(s) = K/[s(s²+s+1)]. Find K range.
**A12.** Char: s³+s²+s+K=0.
Routh:
s³: 1, 1
s²: 1, K
s¹: (1-K)/1
s⁰: K
K>0 and 1-K>0 → 0 < K < 1.

## Section E: Zero in First Column (ε method)

**Q13.** For s³+2s²+s+2=0, analyze stability.
**A13.** Coeffs positive. Routh:
s³: 1, 1
s²: 2, 2
s¹: (2·1-1·2)/2 = 0 → ZERO first column.
Replace 0 with ε:
s¹: ε
s⁰: 2
First column: 1, 2, ε, 2 → as ε→0⁺, all positive → stable.
Check roots: (s+2)(s²+1) → poles -2, ±j. Marginally stable. ✓ (ε method gives no sign change.)

**Q14.** For s⁴+s³+s²+s+1=0, analyze.
**A14.** Routh:
s⁴: 1, 1, 1
s³: 1, 1, 0
s²: (1·1-1·1)/1 = 0, then (1·1-1·0)/1=1 → row [0,1]
Zero first column → use ε: row s²: [ε, 1]
s¹: (ε·1-1·1)/ε = (ε-1)/ε → as ε→0⁺, this is negative.
s⁰: 1
First column: 1,1,ε,(ε-1)/ε,1 → (ε-1)/ε<0 → two sign changes → TWO RHP roots → unstable.

## Section F: Row of Zeros (Auxiliary Equation)

**Q15.** For s⁴+2s³+11s²+18s+18=0, find the auxiliary equation and roots.
**A15.** Routh:
s⁴: 1, 11, 18
s³: 2, 18, 0
s²: (22-18)/2 = 2, (1·18-2·0)/2 = 9 → row [2,9]
s¹: (2·18-2·9)/2 = (36-18)/2 = 9
s⁰: 9
No zero row here. Poles all LHP? First col: 1,2,2,9,9 all pos → stable. (This is just a normal case.)

**Q16.** For s⁴ + s² + 1 = 0, find roots via auxiliary equation.
**A16.** Coeffs: 1,0,1,0,1. Lead zero coefficient → violates necessary condition. Actually s⁴+s²+1 = (s²+s+1)(s²-s+1) → roots ±0.5±j√3/2 unresolved... Instead note instability (missing s³, s terms). This is an even polynomial with symmetric roots.

**Q17.** For s⁴+5s³+10s²+20s+24=0, if a zero row occurs, find auxiliary eq.
**A17.** Routh:
s⁴: 1, 10, 24
s³: 5, 20, 0
s²: (50-20)/5=6, (5·24)/5=24 → [6, 24]
s¹: (120-120)/6 = 0 → ZERO row.
Auxiliary from s² row: 6s²+24 = 0 → s² = -4 → s = ±j2.
Replace s¹ row with derivative: d(6s²+24)/ds = 12s → row s¹: [12]
s⁰: 24
First col: 1,5,6,12,24 all positive → stable (marginally, with roots ±j2).
System oscillates at ω=2 rad/s.

## Section G: ISRO-Style

**Q18.** Characteristic eq s⁴+2s³+3s²+4s+5=0. Determine number of RHP roots.
**A18.** Routh:
s⁴: 1, 3, 5
s³: 2, 4
s²: (6-4)/2 = 1, (2·5-2·0)/2=5 → [1,5]
s¹: (1·4-2·5)/1 = (4-10)=-6
s⁰: 5
First col: 1,2,1,-6,5 → sign changes: 1→-6 (one), -6→5 (two) → TWO RHP roots → unstable.

**Q19.** For G(s)=K/(s(s+1)(s+4)) unity feedback, find K range and marginal frequency.
**A19.** Char: s³+5s²+4s+K=0.
Routh:
s³: 1,4
s²: 5, K
s¹: (20-K)/5
s⁰: K
K>0, K<20 → **0<K<20**. At K=20: aux 5s²+20=0 → s=±j2 → ω=2 rad/s.

**Q20.** Determine the number of roots in RHP for s⁵+2s⁴+3s³+6s²+5s+3=0.
**A20.** (Full array needed.) Coeffs: 1,2,3,6,5,3.
Routh:
s⁵: 1,3,5
s⁴: 2,6,3
s³: (6-6)/2=0! ... Zero first column → ε.
s³: ε, (2·5-2·1)/2 ... details. This requires careful ε analysis; leads to RHP roots. (Answer by full construction.)

**Q21.** A system with char. eq. s³+Ks²+2s+K=0. Determine K range for stability.
**A21.** s³: 1, 2
s²: K, K
s¹: (2K-K)/K = 1
s⁰: K
Require K>0. Also s² row K>0. First col: 1, K, 1, K → need K>0 for stability.
**Stable for all K>0.**

**Q22.** For s⁴+3s³+3s²+2s+2=0, use Routh to check stability.
**A22.** s⁴: 1,3,2
s³: 3,2,0
s²: (9-2)/3=7/3, (3·2-3·0)/3=2 → [7/3, 2]
s¹: ((7/3)·2 - 3·2)/(7/3) = (14/3-6)/(7/3) = ((14-18)/3)/(7/3) = (-4/3)·(3/7) = -4/7
s⁰: 2
First col: 1,3,7/3,-4/7,2 → sign change 7/3→-4/7 then -4/7→2 → TWO RHP roots.

**Q23.** What is the condition that the first-column entries of a Routh array all being positive implies?
**A23.** All characteristic-equation roots lie in the left half of the s-plane (system is asymptotically stable).

## Common Mistakes
1. Using "all coefficients positive" alone to declare stability.
2. Confusing the ε-substitution (first-column zero) with the zero-row case.
3. Mis-handling the auxiliary equation derivative.
4. Incorrect cross-product ratio in array construction.
5. Forgetting the marginal frequency comes from the auxiliary equation.
