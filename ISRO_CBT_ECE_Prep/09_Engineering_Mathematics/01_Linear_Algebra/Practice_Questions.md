# Linear Algebra - Practice Questions

## Easy Level

### Q1. Determinant of a 2×2 Matrix
If A = |3 2|, find det(A).
       |1 4|

**Solution**: det(A) = (3)(4) - (2)(1) = 12 - 2 = **10**

---

### Q2. Singular Matrix
For what value of k is the matrix singular?
A = |1  k|
    |2  4|

**Solution**: det(A) = 0 → (1)(4) - (k)(2) = 0 → 4 - 2k = 0 → **k = 2**

---

### Q3. Inverse of 2×2 Matrix
Find A⁻¹ if A = |4 3|
                  |7 5|

**Solution**:
- det(A) = 20 - 21 = -1
- A⁻¹ = (1/-1)|5 -3| = |-5 3|
               |-7 4|   | 7 -4|

---

### Q4. Eigenvalues
Find eigenvalues of A = |2 0|
                         |0 3|

**Solution**: Diagonal matrix → eigenvalues are diagonal elements: **λ₁ = 2, λ₂ = 3**

---

### Q5. Matrix Multiplication
If A = |1 2| and B = |5 6|, find AB.
       |3 4|          |7 8|

**Solution**:
AB = |(1)(5)+(2)(7)  (1)(6)+(2)(8)| = |19 22|
     |(3)(5)+(4)(7)  (3)(6)+(4)(8)|   |43 50|

---

## Medium Level

### Q6. Rank of Matrix
Find the rank of A = |1 2 3|
                      |2 4 6|
                      |3 6 9|

**Solution**:
- R2 = 2R1, R3 = 3R1 (linearly dependent)
- Only 1 independent row
- **rank(A) = 1**

---

### Q7. Eigenvalues and Eigenvectors
Find eigenvalues and eigenvectors of A = |4 1|
                                          |2 3|

**Solution**:
- Characteristic eq: (4-λ)(3-λ) - 2 = 0 → λ² - 7λ + 10 = 0
- (λ-5)(λ-2) = 0 → **λ₁ = 5, λ₂ = 2**
- For λ₁ = 5: (A-5I)v = 0 → v₁ = |1|
                                    |1|
- For λ₂ = 2: (A-2I)v = 0 → v₂ = |1|
                                    |-2|

---

### Q8. Cayley-Hamilton Theorem
Verify Cayley-Hamilton for A = |2 1|
                                |1 2|

**Solution**:
- Characteristic eq: λ² - 4λ + 3 = 0
- A² - 4A + 3I = |5 4| - |8 4| + |3 0| = |0 0| = 0 ✓
                   |4 5|   |4 8|   |0 3|   |0 0|

---

### Q9. System of Linear Equations
Solve: x + y = 3, 2x + 2y = 6

**Solution**:
- Augmented matrix: [1 1 | 3; 2 2 | 6]
- R2 - 2R1: [1 1 | 3; 0 0 | 0]
- rank(A) = rank([A|b]) = 1 < 2 (unknowns)
- **Infinitely many solutions**: x = 3-t, y = t

---

### Q10. Diagonalization
Diagonalize A = |5 4|
                |1 2|

**Solution**:
- Eigenvalues: λ² - 7λ + 6 = 0 → λ₁ = 6, λ₂ = 1
- Eigenvectors: v₁ = |4|, v₂ = |1|
                      |1|        |-1|
- P = |4 1|, D = |6 0|, P⁻¹ = (1/-5)|-1 -1|
     |1 -1|      |0 1|               |-1  4|
- A = PDP⁻¹

---

## Hard Level

### Q11. Matrix Inverse Using Adjoint
Find A⁻¹ using adjoint method:
A = |2 3 1|
    |0 5 2|
    |1 1 1|

**Solution**:
- det(A) = 2(5-2) - 3(0-2) + 1(0-5) = 6 + 6 - 5 = 7
- Cofactors:
  - C₁₁ = +(5-2) = 3, C₁₂ = -(0-2) = 2, C₁₃ = +(0-5) = -5
  - C₂₁ = -(3-1) = -2, C₂₂ = +(2-1) = 1, C₂₃ = -(2-3) = 1
  - C₃₁ = +(6-5) = 1, C₃₂ = -(4-0) = -4, C₃₃ = +(10-0) = 10
- adj(A) = |3 -2  1|, A⁻¹ = (1/7) adj(A)
           |2  1 -4|
           |-5 1 10|

---

### Q12. Eigenvalue Problem
Find eigenvalues of A = |0 1 0|
                         |0 0 1|
                         |1 0 0|

**Solution**:
- det(A - λI) = |−λ  1   0|
                 | 0 −λ   1|
                 | 1  0  −λ|
- = -λ(λ²) - 1(-1) = -λ³ + 1 = 0
- λ³ = 1 → **λ = 1, ω, ω²** (cube roots of unity)

---

### Q13. Singular Matrix Properties
A is a 3×3 matrix with det(A) = 0. Which is FALSE?
(a) A⁻¹ exists
(b) rank(A) < 3
(c) 0 is an eigenvalue
(d) Columns are linearly dependent

**Solution**: **(a)** - If det(A) = 0, A⁻¹ does NOT exist

---

### Q14. System Consistency
For what value of k does the system have no solution?
x + y + z = 1
2x + y + 2z = 3
x + ky + z = 2

**Solution**:
- [A|b] = |1 1 1 |1|
           |2 1 2 |3|
           |1 k 1 |2|
- R2→R2-2R1, R3→R3-R1:
  |1 1 1 |1|
  |0 -1 0|1|
  |0 k-1 0|1|
- R3→R3+(k-1)R2:
  |1 1 1  |1|
  |0 -1 0 |1|
  |0  0 0 |k|
- No solution when k ≠ 0

---

### Q15. Orthogonal Matrix
Check if A = |1/√2  1/√2| is orthogonal.
             |1/√2 -1/√2|

**Solution**:
- A^T = |1/√2  1/√2|
        |1/√2 -1/√2| = A (symmetric)
- A·A^T = |1  0| = I ✓
          |0  1|
- **Yes, orthogonal**

---

### Q16. Diagonalization Check
Can A = |1 1| be diagonalized?
        |0 1|

**Solution**:
- Eigenvalue λ = 1 (repeated)
- (A - I)v = 0 → |0 1||v₁| = |0| → v₂ = 0
                  |0 0||v₂|   |0|
- Only 1 independent eigenvector: v = |1|
                                       |0|
- **No**, A cannot be diagonalized (defective matrix)

---

### Q17. Quadratic Form
Classify Q(x,y) = 3x² + 2xy + 3y²

**Solution**:
- A = |3 1|
      |1 3|
- Eigenvalues: (3-λ)² - 1 = 0 → λ = 2, 4
- Both positive → **Positive definite**

---

### Q18. Matrix Powers
Find A¹⁰⁰ if A = |1 1|
                    |0 1|

**Solution**:
- A² = |1 2|, A³ = |1 3|, ... A^n = |1 n|
       |0 1|        |0 1|             |0 1|
- **A¹⁰⁰ = |1 100|**
            |0   1|

---

### Q19. Trace and Determinant
Matrix A has eigenvalues 2, 3, 5. Find:
(a) trace(A)
(b) det(A)
(c) eigenvalues of A⁻¹

**Solution**:
(a) trace(A) = 2 + 3 + 5 = **10**
(b) det(A) = 2 × 3 × 5 = **30**
(c) A⁻¹ eigenvalues: **1/2, 1/3, 1/5**

---

### Q20. Rank-Nullity
A is a 5×3 matrix with rank(A) = 2. Find nullity(A).

**Solution**:
- rank(A) + nullity(A) = n = 3
- nullity(A) = 3 - 2 = **1**

---

## ISRO-Focused Questions

### Q21. Quick Singular Matrix
Which matrix is singular?
(a) |1 2|  (b) |2 1|  (c) |3 0|  (d) |1 1|
    |3 4|      |4 2|      |0 3|      |2 2|

**Solution**:
- (a) det = 4-6 = -2
- (b) det = 4-4 = **0** ← Singular
- (c) det = 9-0 = 9
- (d) det = 2-2 = **0** ← Singular
- **Both (b) and (d)**

---

### Q22. Eigenvalue Quick Check
If A is 3×3 with eigenvalues 1, 2, 3, what is det(2A)?

**Solution**:
- det(2A) = 2³ · det(A) = 8 · (1·2·3) = **48**

---

### Q23. System Solution Count
How many solutions does x₁ + 2x₂ = 5 have in R²?

**Solution**:
- Underdetermined (1 equation, 2 unknowns)
- **Infinitely many solutions** (line in R²)

---

### Q24. Orthogonal Matrix Property
If A is orthogonal with det(A) = 1, what is A⁻¹?

**Solution**:
- A⁻¹ = A^T (orthogonal property)
- Since det(A) = 1, A is a **rotation matrix**

---

### Q25. Idempotent Matrix
Find all idempotent 2×2 matrices.

**Solution**:
- A² = A → eigenvalues are 0 or 1
- Possible eigenvalue combinations: {0,0}, {0,1}, {1,1}
- For {0,1}: A is projection onto 1D subspace
- Infinite family parameterized by eigenvector directions
