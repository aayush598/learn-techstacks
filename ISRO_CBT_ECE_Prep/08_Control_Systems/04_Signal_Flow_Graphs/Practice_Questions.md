# Signal Flow Graphs - Practice Questions

## Section A: Basic Identification

**Q1.** In a signal flow graph, what is a source node?
**A1.** A node with only outgoing branches (independent variable/input).

**Q2.** What is a forward path?
**A2.** A path from a source (input) node to a sink (output) node that does not pass through any node more than once.

**Q3.** Define loop gain.
**A3.** The product of the transmittances (gains) of all branches forming a closed loop.

**Q4.** Two loops are non-touching if...
**A4.** They share no nodes (and hence no branches) with each other.

## Section B: Simple Mason's Formula

**Q5.** A single forward path P₁ = G and one feedback loop H (negative feedback). Find T via Mason.
**A5.** L₁ = -GH. Δ = 1 + GH. Δ₁ = 1 (loop touches forward path → removed). T = G(1)/(1+GH) = G/(1+GH).

**Q6.** Same as Q5 but positive feedback. Find T.
**A6.** L₁ = +GH. Δ = 1 - GH. T = G/(1-GH).

**Q7.** Forward path P₁ = 10, single loop L₁ = -2. Find T.
**A7.** Δ = 1 - (-2) = 3. Δ₁ = 1. T = 10/3 ≈ 3.33.

## Section C: Multiple Forward Paths

**Q8.** Graph with two forward paths P₁ = G₁, P₂ = G₂ (parallel) and no loops. Find T.
**A8.** Δ = 1. Δ₁ = Δ₂ = 1. T = (G₁+G₂)/1 = G₁+G₂.

**Q9.** Parallel forward paths P₁ = 2, P₂ = 3 with a single non-touching-free loop L₁ = -4 that touches both paths. Find T.
**A9.** Δ = 1-(-4) = 5. Both Δ₁ = Δ₂ = 1 (loop removed for touching). T = (2·1 + 3·1)/5 = 5/5 = 1.

## Section D: Non-Touching Loops

**Q10.** Graph has loops L₁ = -a and L₂ = -b that are NON-touching. Compute Δ.
**A10.** Δ = 1 - (L₁+L₂) + L₁L₂ = 1 - (-a-b) + ab = 1 + a + b + ab.

**Q11.** Forward path P₁ = G₁, loops L₁ = -2, L₂ = -3 non-touching. Both loops touch forward path. Find T.
**A11.** ΣL = -5. Non-touching product = (-2)(-3) = 6. Δ = 1 - (-5) + 6 = 12. Δ₁ = 1 (both loops removed). T = G₁/12.

**Q12.** Re-do Q11 but assume only L₁ touches the forward path while L₂ does NOT touch it. Find T.
**A12.** Δ = 12 (same). For cofactor: L₂ does not touch path → keep it: Δ₁ = 1 - L₂ = 1 - (-3) = 4. T = G₁·4/12 = G₁/3.

## Section E: Standard Closed-Loop Systems via SFG

**Q13.** Forward G = 5/s, unity feedback negative. Using Mason, find T.
**A13.** P₁ = 5/s. L₁ = -5/s. Δ = 1 + 5/s. Δ₁ = 1. T = (5/s)/(1+5/s) = 5/(s+5).

**Q14.** Forward G = 20/(s(s+2)), H = 1 negative. Mason T?
**A14.** P₁ = 20/(s(s+2)). L₁ = -20/(s(s+2)). Δ = 1+20/(s(s+2)). T = 20/(s²+2s+20).

**Q15.** Forward G = 8/(s+1), feedback H = 0.5 negative. T?
**A15.** P₁ = 8/(s+1). L₁ = -8·0.5/(s+1) = -4/(s+1). Δ = 1+4/(s+1) = (s+5)/(s+1). T = [8/(s+1)]/[(s+5)/(s+1)] = 8/(s+5).

## Section F: Multi-Loop Systems

**Q16.** System with two cascaded feedback loops. Forward G₁G₂, inner loop H₂ around G₂ only. Identify loops.
**A16.** Loops: L₁ = -G₂H₂ (inner), L₂ = -G₁G₂H₁ (outer, unity outer). They touch (share G₂).

**Q17.** For the above with G₁=2, G₂=10/(s+3), H₂=0.5, H₁=1, compute T.
**A17.** L₁ = -10·0.5/(s+3) = -5/(s+3). L₂ = -2·10/(s+3) = -20/(s+3) (they touch). Δ = 1 - (L₁+L₂) = 1+5/(s+3)+20/(s+3) = 1+25/(s+3) = (s+28)/(s+3). P₁ = 20/(s+3). Δ₁ = 1. T = [20/(s+3)]/[(s+28)/(s+3)] = 20/(s+28). Matches block diagram reduction ✓.

## Section G: ISRO-Style Problems

**Q18.** A signal flow graph has forward path gain 6 and a single negative feedback loop of gain 2. Determine closed-loop transfer function.
**A18.** P₁ = 6, L₁ = -2. Δ = 3. T = 6/3 = 2.

**Q19.** In a Mason's formula computation, Δ = 1 - ΣL + Σ(non-touching pairs). If loops are L₁=-1, L₂=-2, L₃=-3 all mutually touching, find Δ.
**A19.** Only individual sums (they touch → no pair products). Δ = 1 - (-6) = 7.

**Q20.** For the graph with forward paths P₁ = 4, P₂ = 2 and loop L₁ = -5 touching both, find T.
**A20.** Δ = 1+5 = 6. Δ₁=Δ₂=1. T = (4+2)/6 = 1.

**Q21.** If a forward path of gain 8 does NOT touch loop L₁ = -0.5, and there are no other structures, find T (single forward path).
**A21.** Δ = 1-(-0.5) = 1.5. Δ₁ = 1 - L₁ = 1.5 (loop not touching → kept). T = 8·1.5/1.5 = 8. (The loop contributes equally, cancels.)

**Q22.** Graph: forward path G₁G₂, loop L₁ = -G₁G₂H₁, loop L₂ = -G₂H₂. L₁ and L₂ touch (share G₂). Find Δ.
**A22.** ΣL = -(G₁G₂H₁ + G₂H₂). No non-touching pair. Δ = 1 + G₁G₂H₁ + G₂H₂.

## Section H: Conceptual

**Q23.** Convert a unity-feedback block diagram (G forward) to SFG and verify Mason gives G/(1+G).
**A23.** Nodes: R, E (error), C. Branches: R→E (1), E→C (G), C→R (feedback -1). Loops: L = -G. P₁ = G. Δ = 1+G. T = G/(1+G). ✓

**Q24.** Why must a forward path not repeat a node?
**A24.** Because per definition, forward paths and loops are simple paths; repeating nodes would create sub-loops and miscompute.

**Q25.** What is a self-loop and how is its gain handled?
**A25.** A branch from a node to itself with gain L. It contributes to ΣL and its elimination uses (1-L) division.

## Common Mistakes
1. Wrongly treating touching loops as non-touching.
2. Omission of feedback sign (-) for negative feedback in loop gain.
3. Miscounting forward paths.
4. Incorrect cofactor Δ_k when a non-touching loop is retained.
5. Forgetting higher-order non-touching products when more loops present.

## Section I: Three-Loop Problems

**Q26.** Loops L₁=−2, L₂=−3 (touch each other), L₃=−4 (touches L₁ but not L₂). Compute all non-touching pairs.
**A26.** L₁ & L₂ touch. L₁ & L₃ touch. L₂ & L₃: check — L₃ not touching L₂ → NON-touching pair. Δ = 1 −(−9) + (L₂L₃ product)=1+9+((−3)(−4))=1+9+12=22.

**Q27.** If additionally a fourth loop L₄, and L₂, L₄ non-touching AND L₃, L₄ non-touching but L₁ touches L₄, list non-touching pairs.
**A27.** Pairs: (L₂,L₃),(L₂,L₄),(L₃,L₄). Not (L₁, anything) since L₁ touches all. Δ = 1 −ΣL + (sum of the three pair products) − (triple if all three non-touching). If L₂,L₃,L₄ all mutually non-touching, add −(L₂L₃L₄).

**Q28.** A forward path of gain 7 touches L₁ but NOT L₂. If Δ has been computed as 12 and Δ₁=5, find T.
**A28.** T = P₁Δ₁/Δ = 7·5/12 = 35/12 ≈ 2.92.

## Section J: ISRO Quick SFG Scenarios

**Q29.** Sketch context: two forward paths both touch the only loop. T = (P₁+P₂)/Δ with Δ₁=Δ₂=1.
**A29.** If loop L=−G: Δ=1+G. T=(P₁+P₂)/(1+G).

**Q30.** Forward paths P₁=3, P₂=5, single loop L=−2 (touches both). Find T.
**A30.** Δ=1−(−2)=3, Δ₁=Δ₂=1. T=(3+5)/3=8/3≈2.67.

**Q31.** For the standard unity-feedback G(s) diagram, list nodes used in the SFG and their transmittances.
**A31.** Nodes: R, E, C. Branches: R→E (1), E→C (G), C→R (−1 for negative feedback). Loop=−G, forward path=G. T=G/(1+G).

## Verification Table
| # forward paths | # loops | Non-touching? | Δ form |
|---|---|---|---|
| 1 | 1 | n/a | 1−L |
| 1 | 2 touching | no | 1−(L₁+L₂) |
| 1 | 2 non-touching | yes | 1−(L₁+L₂)+L₁L₂ |
| 2 | any | path-wise | (P₁Δ₁+P₂Δ₂)/Δ |
