# Linear Algebra - Concepts

## 1. Matrix Basics

### Matrix Types
| Type | Definition |
|------|-----------|
| Square Matrix | m = n, same rows and columns |
| Diagonal | a_ij = 0 for i ≠ j |
| Identity (I_n) | Diagonal with all 1s |
| Scalar | kI_n, all diagonal = k |
| Symmetric | A^T = A |
| Skew-Symmetric | A^T = -A |
| Triangular | Upper (a_ij = 0, i > j) or Lower (a_ij = 0, i < j) |
| Orthogonal | A^T A = AA^T = I |
| Idempotent | A² = A |
| Nilpotent | A^k = 0 for some k |
| Involutory | A² = I |

### Singular vs Non-Singular
- **Non-singular**: det(A) ≠ 0, inverse exists
- **Singular**: det(A) = 0, no inverse
- ISRO Focus: Quickly identify singular matrices from properties

---

## 2. Determinant

### Properties
1. det(AB) = det(A) · det(B)
2. det(A^T) = det(A)
3. det(kA) = k^n · det(A) for n×n matrix
4. det(A⁻¹) = 1/det(A)
5. det(adj(A)) = [det(A)]^(n-1)
6. Swapping two rows negates the determinant
7. det(A) = 0 if two rows/columns are identical

### Expansion Methods
- **Cofactor expansion** along any row or column
- **Sarrus rule** for 3×3 only
- **Row reduction** to triangular form → product of diagonal

---

## 3. Matrix Operations

### Addition & Subtraction
- Same dimensions required
- Element-wise operation

### Multiplication
- A(m×n) × B(n×p) = C(m×p)
- Not commutative: AB ≠ BA in general
- (AB)^T = B^T A^T
- (AB)^-1 = B^-1 A^-1

### Scalar Multiplication
- kA: multiply every element by k

---

## 4. Inverse of a Matrix

### Methods
1. **Adjoint method**: A⁻¹ = adj(A)/det(A)
2. **Row reduction**: [A | I] → [I | A⁻¹]
3. **2×2 shortcut**: A⁻¹ = (1/det) [d -b; -c a]

### Properties
- (A⁻¹)⁻¹ = A
- (AB)⁻¹ = B⁻¹A⁻¹
- (A^T)⁻¹ = (A⁻¹)^T
- (kA)⁻¹ = (1/k)A⁻¹

---

## 5. Rank of a Matrix

### Definition
- Largest number of linearly independent rows or columns
- Equals number of non-zero rows in row echelon form

### Key Properties
- rank(A) = rank(A^T)
- rank(AB) ≤ min(rank(A), rank(B))
- rank(A) + rank(B) ≤ rank(A + B) + rank(AB)
- rank(kA) = rank(A) for k ≠ 0

### Relation to Solutions
- For Ax = b: solution exists if rank(A) = rank([A|b])
- Unique solution if rank(A) = n (number of unknowns)
- Infinitely many if rank(A) < n
- No solution if rank(A) < rank([A|b])

---

## 6. Eigenvalues and Eigenvectors

### Definition
- Av = λv where v ≠ 0
- λ is eigenvalue, v is eigenvector
- Found from det(A - λI) = 0 (characteristic equation)

### Properties
- Sum of eigenvalues = trace(A)
- Product of eigenvalues = det(A)
- Eigenvalues of A⁻¹ are 1/λ_i
- Eigenvalues of A^k are λ_i^k
- Eigenvalues of A + kI are λ_i + k
- Similar matrices have same eigenvalues

### Singular Matrix Connection
- A is singular ↔ 0 is an eigenvalue

---

## 7. Diagonalization

### Process
1. Find all eigenvalues of A
2. Find eigenvectors for each eigenvalue
3. If n linearly independent eigenvectors exist, A is diagonalizable
4. A = PDP⁻¹ where D = diagonal matrix of eigenvalues

### Conditions
- Matrix must have n linearly independent eigenvectors
- Sufficient condition: n distinct eigenvalues

---

## 8. Cayley-Hamilton Theorem

- Every square matrix satisfies its own characteristic equation
- If p(λ) = det(A - λI) = 0, then p(A) = 0
- Used to find A⁻¹: express A⁻¹ in terms of powers of A

---

## 9. System of Linear Equations

### Ax = b
- **Consistent**: solution exists
- **Inconsistent**: no solution
- **Homogeneous** (b = 0): always has trivial solution x = 0
- Non-trivial solution exists iff det(A) = 0

### Cramer's Rule
- x_i = det(A_i)/det(A)
- Only for square systems with det(A) ≠ 0

### Gaussian Elimination
- Forward elimination to upper triangular
- Back substitution

---

## 10. Vector Spaces (Brief)

### Subspace Requirements
1. Zero vector present
2. Closed under addition
3. Closed under scalar multiplication

### Basis & Dimension
- Basis: minimal spanning set, linearly independent
- Dimension: number of vectors in basis
- dim(R^n) = n

---

## 11. Important Theorems

### Rank-Nullity Theorem
- rank(A) + nullity(A) = n

### Sylvester's Law
- rank(A) + rank(B) - n ≤ rank(AB)

### Similarity
- A ~ B if B = P⁻¹AP for some invertible P
- Same eigenvalues, same determinant, same trace

### Quadratic Forms
- Positive definite: all eigenvalues > 0
- Positive semi-definite: all eigenvalues ≥ 0
- Negative definite: all eigenvalues < 0

---

## 12. Important Properties for Quick Reference

| Property | Result |
|----------|--------|
| det(A) = 0 | Singular, non-invertible, 0 eigenvalue |
| rank(A) = n | Full rank, non-singular, invertible |
| AB = I | B = A⁻¹ |
| A^T = A⁻¹ | Orthogonal matrix |
| A² = A | Idempotent |
| Trace = sum of eigenvalues | Quick check |
| Det = product of eigenvalues | Quick check |
