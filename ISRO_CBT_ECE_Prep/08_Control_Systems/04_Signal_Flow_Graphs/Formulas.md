# Signal Flow Graphs - Formulas

## 1. Mason's Gain Formula

**T = (1/Δ) · Σ_{k=1}^{N} P_k·Δ_k**

- N = number of forward paths.
- P_k = gain of k-th forward path.
- Δ = graph determinant.
- Δ_k = cofactor of k-th forward path.

## 2. Graph Determinant Δ

**Δ = 1 - ΣLᵢ + ΣLᵢLⱼ - ΣLᵢLⱼLₖ + ...**

Where:
- ΣLᵢ = sum of all individual loop gains.
- ΣLᵢLⱼ = sum of products of gains of ALL combinations of 2 NON-TOUCHING loops.
- ΣLᵢLⱼLₖ = sum of products of gains of ALL combinations of 3 NON-TOUCHING loops.
- Continue for higher combinations; stop when no more non-touching combos exist.

## 3. Cofactor Δ_k
Δ_k = Δ t, but with all loops that touch the k-th forward path set to zero (removed).

## 4. Loop Gain Computation
For a loop traversing branches with transmittances T₁, T₂, ..., T_m:
L = T₁·T₂·...·T_m (product of all branch transmittances).

## 5. Forward Path Gain
For forward path through branches with transmittances G₁, G₂, ..., G_p:
P = G₁·G₂·...·G_p.

## 6. Series Reduction
Two branches in series with gains a and b between three nodes:
Equivalent single branch gain = a·b.

## 7. Parallel Reduction
Two branches between the same pair of nodes with gains a and b:
Equivalent gain = a + b (or a - b for subtractive).

## 8. Self-Loop Elimination
Node with self-loop L and incoming branches: eliminates self-loop by dividing incoming-transmittance contributions by (1 - L) when producing that node as output.

## 9. Feedback Loop Formula (Standard)
For forward gain G and feedback H:
T = G/(1 + GH)   [negative feedback]
T = G/(1 - GH)   [positive feedback]

Illustrated as: a loop node where loop gain includes H with appropriate sign.

## 10. Conversion Block Diagram → SFG
- Each block (TF) → a branch.
- Each summing point → a node.
- Each pickoff point → a node.
- Signal direction = arrow direction.
- Maintain same transfer relationships.

## 11. Example Template - Standard Closed Loop
Forward: R →(G)→ C.
Feedback: C →(H)→ summing node at R.
Mason: P₁ = G, L₁ = -GH (negative feedback → loop gain -GH).
Δ = 1 - L₁ = 1 - (-GH) = 1 + GH.
Δ₁ = 1 (only loop touches forward path → removed).
T = G/(1+GH). ✓

## 12. Two-Loop Example Template
Forward path: P₁ = G₁G₂G₃.
Loops: L₁ = G₂H₂, L₂ = G₁G₂H₁ (if non-touching to each path etc.).
Δ = 1 - (L₁+L₂) + L₁L₂ (if L₁,L₂ non-touching).
For each path compute Δ_k by zeroing touching loops.

## 13. Number of Non-Touching Loop Combinations
For m non-touching loops considered pairwise: C(m,2). For triples: C(m,3).

## Key Formula Summary Table

| Quantity | Symbol | Computation |
|---|---|---|
| Loop gain | L | Product of branch gains in loop |
| Forward path gain | P_k | Product of branch gains in forward path |
| Graph determinant | Δ | 1 - ΣL + ΣLᵢLⱼ - ... |
| Cofactor | Δ_k | Δ with touching loops removed |
| Transfer function | T | (ΣP_kΔ_k)/Δ |

## Sign Convention
- Negative feedback contributes NEGATIVE loop gain in Mason's formula.
- Positive feedback contributes POSITIVE loop gain.
- Handle signs directly: e.g., a feedback branch H with subtractive summing node → loop gain = -G·H.

## Validation Tip
For simple single-loop systems, Mason's formula must reduce to the standard feedback formula. Use this to verify your loop identification.

## 14. Worked Micro-example (two loops, one forward path)
System with forward P₁=G₁G₂G₃; loops L₁=−G₂H₂ (inner), L₂=−G₁G₂H₁ (outer), which share G₂.
- ΣL = L₁+L₂ = −(G₂H₂+G₁G₂H₁).
- No non-touching pair (they share G₂).
- Δ = 1 + G₂H₂ + G₁G₂H₁.
- Δ₁ = 1 (only one forward path, loops touch it).
- T = G₁G₂G₃ / (1 + G₂H₂ + G₁G₂H₁).

## 15. Non-touching example with three loops
Loops L₁, L₂, L₃ where L₁,L₃ are non-touching but L₂ touches both:
Δ = 1 − (L₁+L₂+L₃) + (L₁·L₃).

## 16. Cofactor quick rule
For forward path k, Δ_k = Δ with all loops that share ANY node with path k removed (set to 0). Loops that do NOT touch path k remain.

## 17. Sign Handling Quick Guide
- Each feedback transmittance at a subtractive summing node contributes a NEGATIVE loop gain.
- So a "negative feedback loop" with path gain L_pos appears as −L_pos in ΣL.
- Multiple negative signs → positive product for even count.

## 18. Mason's Formula Equivalence Checks
- One forward path + one negative loop → reduces to G/(1+GH). ✓
- Two parallel forward paths, no loop → sum of paths. ✓
- Always verify a trivial case to catch identification errors.

## 19. Rapid Loop Identification Method
1. List every closed directed cycle that returns to its start node without repeating nodes.
2. Record its branch-gain product.
3. Mark which loops share nodes (touching) vs disjoint (non-touching).
4. Build Δ incrementally.

## 20. Common SFG→TF Pitfalls
- Forward paths must not revisit nodes (they are simple paths).
- Self-loops count as individual loops.
- A node that is both mid-path and loop node still counts for touching.
