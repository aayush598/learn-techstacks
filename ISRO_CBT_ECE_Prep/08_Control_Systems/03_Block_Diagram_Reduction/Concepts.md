# Block Diagram Reduction - Concepts

## 1. Purpose of Block Diagram Reduction
- Simplify complex system representations into a single transfer function.
- Used to determine overall input-output relationship.
- Applies only to linear, time-invariant systems.

## 2. Basic Block Diagram Elements
- **Blocks**: Rectangles containing transfer functions G(s). Represent subsystems.
- **Summing Point**: ⊕ Circle with +/- signs. Algebraic sum of incoming signals.
- **Pickoff Point**: Branch point where a signal is tapped and sent to multiple locations.
- **Arrows**: Show signal flow direction.
- **Closed Loop**: Path from summing point through blocks and feedback back to summing point.
- **Open Loop**: Path from input through forward blocks, no feedback.

## 3. Fundamental Connections

### Series (Cascade) Connection
- Two blocks G₁ and G₂ in series, no loading between them.
- Combined TF = G₁ · G₂.
- Order of multiplication matters only if non-commutative (matrices), but for scalar TFs it's commutative.
- **Loading effect**: If there is impedance loading between stages, the simple product is invalid.

### Parallel Connection
- Two blocks G₁ and G₂ receiving same input, outputs added.
- Combined TF = G₁ + G₂ (or G₁ - G₂ for subtractive summing).

### Feedback Connection
- Forward path G(s), feedback path H(s).
- Negative feedback: T(s) = G/(1+GH).
- Positive feedback: T(s) = G/(1-GH).
- **Unity feedback**: H(s) = 1.

## 4. Reduction Rules (Move Blocks)

### Moving a Pickoff Point
- **Pickoff point before a block** moved AFTER the block: insert block with inverse function G⁻¹ in the new branch.
- **Pickoff point after a block** moved BEFORE the block: insert block G in the branch.

### Moving a Summing Point
- **Summing point before a block** moved AFTER the block: insert block G in the branch that was summed.
- **Summing point after a block** moved BEFORE the block: insert block G⁻¹ in the summed branch.

### Rules Summary (tabulated)
| Operation | Rule |
|---|---|
| Moving pickoff after block (ahead of block) | Add 1/G in tapped branch |
| Moving pickoff before block (behind) | Add G in tapped branch |
| Moving summing after block | Add G in branch |
| Moving summing before block | Add 1/G in branch |
| Interchange adjacent summing points | Allowed (no change) |
| Interchange summing & pickoff | Not directly; must use shifting rules |
| Eliminate series blocks | Multiply |
| Eliminate parallel | Add/subtract |
| Eliminate feedback loop | G/(1±GH) |

## 5. Standard Reduction Procedure (Step-by-step)
1. **Identify inner loops** (feedback loops not touching others) and reduce them first.
2. Move pickoff points and summing points to enable combining blocks in series/parallel.
3. Reduce series/parallel combinations.
4. Reduce feedback loops using closed-loop formula.
5. Repeat until a single block remains.
6. Document each step to avoid algebra errors.

## 6. Multiple Inputs / Multiple Outputs
- When a system has multiple inputs (disturbances), apply **superposition**.
- Reduce the diagram for each input separately, with other inputs set to zero.
- Total output = sum of outputs from each input.
- Disturbance rejection: sensitivity to disturbance D(s) analyzed separately from input.

## 7. Sensitivity Considerations
- Closed-loop transfer function reduces sensitivity to forward-path gain variations.
- Sensitivity of T to G: S = (∂lnT/∂lnG) = 1/(1+GH) for negative feedback.
- High loop gain → low sensitivity.

## 8. Internal vs Overall Transfer Functions
- Overall TF relates desired input to output.
- Internal TFs (e.g., output to disturbance) may be different.
- Ensure feedforward paths and feedback paths are correctly mapped.

## 9. Non-Unity Feedback Reduction
Given forward G and feedback H:
- T(s) = G/(1+GH).
- To use standard error analysis with error constants, sometimes converted to unity-feedback form:
  - Equivalent forward: G_eq = G·H, feedback = 1, with output scaled by 1/H.
  - Or compute error constants from G(s)H(s).

## 10. Common Errors in Reduction
1. Wrong sign in feedback formula.
2. Treating interconnection with loading as simple series (invalid when blocks load each other).
3. Moving pickoff/summing points without adding inverse-transfer compensating blocks.
4. Reducing loops that touch (sharing summing/pickoff points) as non-touching.
5. Forgetting superposition for multiple inputs.

## 11. Rules for Non-Touching Loops
- Two loops are non-touching if they do not share any block, summing point, or pickoff point.
- Non-touching loops appear in Mason's gain formula for signal flow graphs.
- In block diagram reduction, loops that touch must not be reduced independently in ways that violate structural relationships.

## 12. Worked Strategy for ISRO
- ISRO frequently tests single-loop and two-loop single-input reductions.
- Master feedback formula and series/parallel simplification.
- Practice moving summing and pickoff points systematically.
- Verify final result by substituting a numeric value for s.

## Key Vocabulary
- Forward path, feedback path, summing point, pickoff point.
- Loop gain = product of transfer functions around a loop.
- Number of loops, non-touching loops (for Mason's).
- Closed-loop TF vs open-loop TF.
