# Routh-Hurwitz Criterion - Concepts

## 1. Purpose
- Determines whether a system (characteristic equation) is stable **without solving** for the roots.
- Provides necessary and sufficient conditions for all roots to lie in the left half of the s-plane.
- Also gives the **range of a parameter** (e.g., gain K) for which the system is stable.

## 2. Necessary Condition (first check)
For characteristic equation a_n s^n + a_{n-1} s^{n-1} + ... + a_0 = 0:
- **All coefficients must be present** (no missing terms except possibly s^0 being nonzero).
- **All coefficients must have the same sign** (all positive after normalization).
- If any coefficient is zero or sign is negative → system is UNSTABLE or has roots on the imaginary axis (no need to build the array).

### Note
- Satisfying the necessary condition does NOT guarantee stability.
- It is necessary but not sufficient.

## 3. Routh Array Construction
Arrange coefficients in the first two rows, then fill subsequent rows.

Row layout for 4th-order char. eq. a₄s⁴+a₃s³+a₂s²+a₁s+a₀:

| Row | s^4 | s^3 | s^2 | s^1 | s^0 |
|---|---|---|---|---|---|
| s⁴ | a₄ | a₂ | a₀ | | |
| s³ | a₃ | a₁ | | | |
| s² | b₁=(a₃a₂-a₄a₁)/a₃ | b₂=(a₃a₀-a₄·0)/a₃=a₀ | | | |
| s¹ | c₁=(b₁a₁-a₃b₂)/b₁ | | | | |
| s⁰ | d₁=b₂ (if proceeding) | | | | |

### General formulas
For row entries, compute from the two rows above using determinants of 2x2 matrices.

## 4. Stability from Routh Array
- The system is **stable if and only if all elements in the FIRST COLUMN of the Routh array have the same sign (all positive)**.
- The **number of sign changes** in the first column equals the **number of roots in the right half of the s-plane** (instability count).

## 5. Special Cases

### Case 1: Zero in the first column (but not entire row)
- Cannot divide by zero.
- Replace the zero by a small positive number **ε** (epsilon) and continue.
- Analyze signs as ε → 0⁺.
- If sign changes occur across ε, there are RHP roots.

### Case 2: Entire row of zeros
- Occurs when there is an **even polynomial** (roots symmetrically placed about origin, e.g., ±jω or pairs ±a±jb).
- This indicates roots on the imaginary axis (or symmetric about it) → marginal stability or instability.
- **Auxiliary equation**: formed from the row above the zero row, using its coefficients as an even polynomial.
- Differentiate the auxiliary polynomial with respect to s to get a new row (replace the zero row with its derivative coefficients).
- The roots of the auxiliary equation are the roots on (or symmetric about) the imaginary axis.

## 6. Auxiliary Equation Details
- Auxiliary polynomial A(s) = even polynomial from the row above the zero row.
- Its roots are exactly the symmetric roots (purely imaginary or symmetric about origin).
- Differentiate A(s), use its coefficients for the zero row.
- The auxiliary equation also helps find the frequency of sustained oscillation ω (imaginary roots) and the gain K at marginal stability.

## 7. Application: Range of K for Stability
- Build the Routh array treating K as a symbolic parameter.
- Set the first-column entries (especially in the highest rows) ≥ 0 and solve inequalities.
- Intersection of constraints gives the stable range of K.
- At the boundary (marginal), system oscillates at frequency from auxiliary equation.

## 8. Necessary and Sufficient Conditions Summary
- Necessary: all coefficients positive (present).
- Sufficient: all first-column entries of Routh array positive.
- Both together guarantee LHP poles.

## 9. Higher-Order Systems
- Fifth order and above: sign conditions on coefficients alone are insufficient, Routh array required.
- Third-order example: s³ + a₂s² + a₁s + a₀ with stability condition a₂a₁ > a₀.

## 10. Relationship to Other Stability Methods
- Routh: algebraic, gives stability & parameter ranges, no iteration.
- Root locus: graphical, shows pole movement with gain.
- Nyquist: for open-loop, handles delay and non-minimum phase.
- For ISRO, Routh is used heavily for stability limits and gain ranges.

## 11. Common Misconceptions
- "All coefficients positive" alone does NOT guarantee stability.
- A zero row does NOT immediately mean unstable — use auxiliary equation.
- The ε substitution is only for first-column zero, not row of zeros.

## 12. ISRO Common Questions
- Given characteristic equation, find range of K.
- Determine number of RHP roots from first-column sign changes.
- Identify marginal-stability frequency from auxiliary equation.
- Classify stability without solving for poles.

## 13. Routh Array Pitfalls & Tips
- Always write the characteristic equation in descending powers of s before building the array.
- If a coefficient is zero in the middle (e.g., missing s³ term), check necessary condition — usually unstable immediately.
- Multiply an entire row by a positive constant to simplify fractions without changing the sign pattern (allowed).
- Do NOT multiply by a negative constant (flips sign perception of first column).

## 14. Step-by-Step Routh Workflow
1. Write char. eq. with a_n > 0 (normalize if needed).
2. Quick check: all coefficients present & positive → else unstable/jω roots.
3. For 3rd order, apply a₂a₁ > a₀ shortcut.
4. Build array (only first-column matters for sign, but compute all entries for auxiliary eq).
5. Count sign changes → number of RHP roots.
6. Handle first-column zero with ε; handle full zero row with auxiliary eq.

## 15. Using Routh for Design (Gain & Parameter Ranges)
- Treat the unknown (K or other parameter) symbolically.
- Enforce positivity of key first-column entries.
- Usually the constraint comes from the s¹ (or s²) row: set (expr) > 0 → K range.
- Boundary value → marginal stability; frequency from auxiliary eq.

## 16. Relation to Number of Poles on Axis
- A zero row indicates an even polynomial factor (auxiliary) with roots symmetric about origin (i.e., on jω axis or ±a±jb).
- The number of jω-axis root pairs = (number of times you encounter zero rows processing downward) with care.

## 17. Common Confusions Resolved
- "Missing constant term" (a₀=0) → pole at origin → not asymptotically stable.
- "All coefficients positive" is quick but NOT sufficient — always need Routh for order ≥ 3.
- A zero first-column entry is treatable (ε); a fully zero row is a separate case.

## 18. Quick Memory
- First column : all positive = stable.
- Sign changes = RHP roots.
- Zero row → auxiliary → differentiate → continue.
- Third order: a₂a₁ > a₀.
