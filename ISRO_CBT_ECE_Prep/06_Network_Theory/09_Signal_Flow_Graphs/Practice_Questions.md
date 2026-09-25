# Signal Flow Graphs and Mason's Gain Formula - Practice Questions

## Instructions
Each question has one correct option. Loops with negative signs are already included in the listed loop gains.

## Questions

### Q1. Loop definition [Easy]
In a signal-flow graph, a loop is:

A. Any path from source to sink  
B. A closed directed path that returns to its starting node without repeating another node  
C. Any branch directed toward the sink  
D. A product of forward-path gains

**Answer:** B  
**Explanation:** A loop starts and ends at the same node while not repeating any other node.

### Q2. Non-touching loops [Easy]
Two loops are non-touching when:

A. Their arrows point in opposite directions  
B. They share no common node  
C. They touch the same source node  
D. They contain equal numbers of branches

**Answer:** B  
**Explanation:** Non-touching loops have no node in common; only products of such loops appear in `Δ`.

### Q3. Mason's formula structure [Easy]
Mason's gain formula is:

A. `T=(ΣP_kΔ_k)/(1−ΣL_1+ΣL_2−⋯)`  
B. `T=(ΣP_k)/(1−ΣL_1)` only  
C. `T=Δ/(ΣP_k)`  
D. `T=1+ΣL_k`

**Answer:** A  
**Explanation:** `T=ΣP_kΔ_k/Δ`; `Δ` contains alternating sums of products of non-touching loops.

### Q4. Two touching loops [Medium]
A graph has two individual loop gains `L₁=−2` and `L₂=−3`. They touch each other. Two forward paths have gains 10 and 5, and each touches both loops. Mason's gain is:

A. `15/2`  
B. `5/2`  
C. `15/6`  
D. `5/6`

**Answer:** C  
**Explanation:** `Δ=1−(−2)−(−3)=6`; both `Δ_k=1`; therefore `T=(10+5)/6=15/6=2.5`.

### Q5. Paths touching different loops [Medium]
For `L₁=−2` and `L₂=−3`, path `P₁=4` touches only `L₁`, and path `P₂=6` touches only `L₂`. Find `T`.

A. `10/6`  
B. `34/6`  
C. `10/5`  
D. `34/4`

**Answer:** B  
**Explanation:** `Δ=6`, `Δ₁=1−L₂=4`, and `Δ₂=1−L₁=3`; `T=(4×4+6×3)/6=34/6`.

### Q6. Negative-feedback transfer [Easy]
For unity negative feedback with forward gain `G=4` and feedback gain `H=0.1`, the closed-loop gain is:

A. 2.5  
B. 2.857  
C. 3.5  
D. 4.4

**Answer:** B  
**Explanation:** `G_cl=G/(1+GH)=4/(1+0.4)=20/7≈2.857`.

### Q7. Positive-feedback transfer [Easy]
For unity positive feedback with `G=4` and `H=0.1`, the closed-loop gain is:

A. `20/3`  
B. `20/7`  
C. `10/3`  
D. `0.36`

**Answer:** A  
**Explanation:** `G_cl=G/(1−GH)=4/0.6=20/3`.

### Q8. Cascade reduction [Easy]
Two blocks in cascade have transfer functions `G₁=2` and `G₂=3`. Their equivalent gain is:

A. `1/6`  
B. `5`  
C. `6`  
D. `1`

**Answer:** C  
**Explanation:** Cascades multiply: `G_eq=G₁G₂=6`.

### Q9. Loop gain [Easy]
A negative-feedback loop contains forward block `G=12` and feedback block `H=0.05`. The loop gain is:

A. 0.05  
B. 0.6  
C. 12  
D. 13

**Answer:** B  
**Explanation:** The loop gain is `GH=12×0.05=0.6`.

### Q10. Graph without loops [Easy]
If a graph has one forward path and no closed loops, Mason's determinant is:

A. `0`  
B. `1`  
C. Equal to the forward-path gain  
D. Infinite

**Answer:** B  
**Explanation:** All loop sums are zero, so `Δ=1` and the transfer equals the forward-path gain.

## Answer Key
1. B  
2. B  
3. A  
4. C  
5. B  
6. B  
7. A  
8. C  
9. B  
10. B
