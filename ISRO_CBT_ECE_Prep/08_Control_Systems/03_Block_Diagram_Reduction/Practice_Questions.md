# Block Diagram Reduction - Practice Questions

## Section A: Series & Parallel

**Q1.** G₁ = 2/(s+1), G₂ = 3s. Series connection. Find total TF.
**A1.** G = G₁·G₂ = (2/(s+1))·3s = 6s/(s+1).

**Q2.** G₁ = 1/s, G₂ = 1/(s+2) in parallel with additive summing. Total?
**A2.** G = 1/s + 1/(s+2) = (s+2+s)/(s(s+2)) = (2s+2)/(s(s+2)) = 2(s+1)/(s(s+2)).

**Q3.** Three blocks 2, 3, 4 (constants) in series. Total?
**A3.** G = 2·3·4 = 24.

**Q4.** Parallel: G₁ = 3, G₂ = -2 (negative terminal). Total?
**A4.** G = 3 + (-2) = 1. (Or 3-2=1.)

## Section B: Feedback Loops

**Q5.** Unity negative feedback, G(s) = 10/(s+5). Find T(s).
**A5.** T = G/(1+G) = [10/(s+5)]/[1+10/(s+5)] = 10/(s+15).

**Q6.** G(s) = 4/s, H(s) = 1, negative feedback. T(s)?
**A6.** T = (4/s)/(1+4/s) = 4/(s+4).

**Q7.** Positive feedback: G = 10, H = 0.4. Find T and the characteristic equation stability check.
**A7.** T = G/(1-GH) = 10/(1-4) = 10/(-3) = -10/3. Since GH=4 with positive feedback, 1-GH = -3 ≠ 0 → the loop gain 4 > 1 causes instability tendency. Char. eq. 1-GH=0 → 1-4 ≠ 0, stable? Check: positive feedback with GH=4 gives pole where 1-GH=0 in denominator → no RHP pole from this constant, but the system amplifies. (Positive feedback unstable.)

**Q8.** G = K/(s(s+4)), H = 1. Characteristic equation.
**A8.** 1 + K/(s(s+4)) = 0 → s²+4s+K = 0.

**Q9.** A feedback system has T = G/(1+GH). If G = 100, H = 0.1, find T.
**A9.** T = 100/(1+100·0.1) = 100/(1+10) = 100/11 ≈ 9.09.

## Section C: Moving Blocks

**Q10.** A pickoff point lies AFTER block G=2 and before it there is a branch tapped. What must be inserted to shift the pickoff point before block G?
**A10.** Insert G (=2) in the tapped branch.

**Q11.** A summing point sums signal then feeds block G = 5. To move the summing point after block G, what compensates?
**A11.** Insert G = 5 in the branch that was summed (to preserve relationship).

**Q12.** If a pickoff point is moved from before block G to after it, which function is inserted in the tapped branch?
**A12.** 1/G (inverse).

## Section D: Multi-Loop Reduction

**Q13.** Inner loop: G₂ = 10/(s+3), H₂ = 0.5 (negative). Reduce inner loop.
**A13.** T_inner = G₂/(1+G₂H₂) = [10/(s+3)]/[1+(10/(s+3))(0.5)] = 10/(s+3+5) = 10/(s+8).

**Q14.** Given G₁ = 2 (series before inner loop of Q13), find total forward and overall (unity outer feedback).
**A14.** Forward = G₁·T_inner = 2·10/(s+8) = 20/(s+8). Overall unity feedback: T = [20/(s+8)]/[1+20/(s+8)] = 20/(s+28).

**Q15.** A system has an outer loop G = 8/(s(s+2)), H = 1, and an inner feedforward of 3. After reducing inner to forward=3·8/(s(s+2)), find overall.
**A15.** Forward G' = 24/(s(s+2)). Unity feedback: T = 24/(s(s+2)+24) = 24/(s²+2s+24).

## Section E: Multiple Inputs (Superposition)

**Q16.** A plant P(s) = 5/(s+1), controller C(s) = 2, unity feedback. Find output C(s) for reference R and disturbance D entering after the plant input.
**A16.** For R: T_R = CP/(1+CP) = [2·5/(s+1)]/[1+10/(s+1)] = 10/(s+11). For D at plant input: T_D = P/(1+CP) = [5/(s+1)]/[1+10/(s+1)] = 5/(s+11). C(s) = (10/(s+11))R(s) + (5/(s+11))D(s).

**Q17.** Why is superposition valid in the above?
**A17.** Because the system is linear; we can analyze each input separately with others zeroed.

## Section F: ISRO-Style

**Q18.** Reduce the block diagram: forward path has G₁=2, G₂=1/(s+1) in series, feedback H=1 negative. Overall TF?
**A18.** Forward = 2/(s+1). Overall = [2/(s+1)]/[1+2/(s+1)] = 2/(s+3).

**Q19.** For the block reduction result T = 2/(s+3), what is the closed-loop pole?
**A19.** Pole at s = -3 (from 1+T... characteristic eq s+3=0).

**Q20.** A unity feedback system has T(s) = 10/(s+10). Find G(s) (forward path).
**A20.** T = G/(1+G) → solve: G = T/(1-T) = [10/(s+10)]/[1-10/(s+10)] = [10/(s+10)]/[s/(s+10)] = 10/s.

**Q21.** Verify Q20: with G=10/s, what is T?
**A21.** T = (10/s)/(1+10/s) = 10/(s+10). ✓.

**Q22.** Reduce: two inner loops - Loop1: G=2,H=0.5; Loop2: G=3,H=1. If they are in series (loop1 feeding loop2), overall forward and then unity feedback.
**A22.** Loop1: T1 = 2/(1+2·0.5) = 2/2 = 1. Loop2: T2 = 3/(1+3·1) = 3/4 = 0.75. Series forward = 1·0.75 = 0.75. Unity feedback: T = 0.75/1.75 = 3/7.

## Section G: Conceptual Verification

**Q23.** When is a simple series product G₁·G₂ invalid due to loading?
**A23.** When the output of G₁ is loaded by the input impedance of G₂ (e.g., non-ideal stages in actual circuits). Standard block diagram assumes ideal (unloaded) interconnection.

**Q24.** Two summing points that don't touch other elements — can they be interchanged?
**A24.** Yes, adjacent summing points can be interchanged without changing the overall relationship.

**Q25.** In a negative feedback system, what is the closed loop TF if G=∞ (very large)?
**A25.** T = G/(1+GH) → as G→∞ with H constant, T → 1/H. (Output ≈ reference/H.)

## Common Mistakes
1. Using product formula when there is loading.
2. Wrong sign for positive vs negative feedback.
3. Moving summing/pickoff points without inserting compensating blocks (G or 1/G).
4. Forgetting to apply superposition for multiple inputs.
5. Reducing non-touching loops incorrectly.

## Section H: Worked Block Reduction (Multi-step)

**Q26.** Reduce: G₁=2 → [summing with feedback H=1] → G₂=3/(s+1). Unity negative feedback loop. Overall TF.
**A26.** First reduce inner loop around G₂ with H=1:
T_inner = G₂/(1+G₂) = [3/(s+1)]/[1+3/(s+1)] = 3/(s+4).
Then outer: forward = G₁·T_inner = 2·3/(s+4) = 6/(s+4). Overall unity feedback: T = [6/(s+4)]/[1+6/(s+4)] = 6/(s+10).

**Q27.** A block diagram has forward path G=K/[s(s+3)] and feedback H=0.5. Find closed-loop TF and characteristic equation.
**A27.** T = G/(1+GH) = [K/(s(s+3))]/[1+ (K/(s(s+3)))(0.5)] = K/(s²+3s+0.5K). Char. eq: s²+3s+0.5K=0.

**Q28.** For the system in Q27, apply the Routh third-order-style check isn't needed (2nd order). When is it stable?
**A28.** Always stable if 0.5K>0 → K>0 (2nd order with positive coefficients).

## Section I: Feedback with Pickoff Movement

**Q29.** A pickoff after block G=4 is to be moved to before the block, feeding a separate branch. What's inserted in that branch?
**A29.** G=4 (forward the block into the tapped branch).

**Q30.** A summing point is before block G=(s+1)/s. Moving it after the block requires inserting what in the summed branch?
**A30.** G=(s+1)/s.

## Section J: Disturbance Analysis

**Q31.** Plant P=2/(s+3), controller C=5, unity feedback. A disturbance D enters after P. Find output due to D only, and due to R only.
**A31.** For D: T_D = P/(1+CP) = [2/(s+3)]/[1+10/(s+3)] = 2/(s+13).
For R: T_R = CP/(1+CP) = 10/(s+13).
C(s)= (10/(s+13))R(s) + (2/(s+13))D(s).

**Q32.** If we want to reduce the effect of disturbance D, what should increase?
**A32.** The controller gain C (reduces the disturbance sensitivity transfer function).

## Quick Reference Verification Table
| Reduction | Result to double-check |
|---|---|
| Series G₁,G₂ | G₁G₂ |
| Parallel + | G₁+G₂ |
| Feedback − | G/(1+GH) |
| Feedback + | G/(1−GH) |
| Pickoff shift | add G or 1/G |
| Summing shift | add G or 1/G |
| Superposition | separate inputs |
