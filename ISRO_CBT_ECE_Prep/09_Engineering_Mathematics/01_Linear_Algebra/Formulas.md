# Linear Algebra - Formulas

## 1. Determinant Formulas

### 2×2 Matrix
```
|a  b| = ad - bc
|c  d|
```

### 3×3 Matrix (Sarrus Rule)
```
|a b c| = a(ei-fh) - b(di-fg) + c(dh-eg)
|d e f|
|g h i|
```

### General Properties
```
det(AB) = det(A) · det(B)
det(A^n) = [det(A)]^n
det(kA) = k^n · det(A)  [n×n matrix]
det(A⁻¹) = 1/det(A)
det(A*) = [det(A)]^(n-1  [A* = adjugate]
det(diag(a₁,a₂,...,aₙ)) = a₁ · a₂ · ... · aₙ
det(triangular) = product of diagonal elements
```

---

## 2. Inverse Formulas

### 2×2 Matrix
```
A = |a b|  →  A⁻¹ = 1/(ad-bc) | d -b|
    |c d|                      |-c  a|
```

### Adjoint Method (n×n)
```
A⁻¹ = (1/det(A)) · adj(A)

adj(A) = C^T  [Cofactor matrix transposed]

Cofactor: C_ij = (-1)^(i+j) · M_ij
Minor M_ij = determinant of submatrix after removing row i, column j
```

### Row Reduction
```
[A | I] → row operations → [I | A⁻¹]
```

---

## 3. Eigenvalue Formulas

### Characteristic Equation
```
det(A - λI) = 0

For 2×2: λ² - trace(A)·λ + det(A) = 0
For 3×3: λ³ - trace(A)·λ² + (sum of cofactors)·λ - det(A) = 0
```

### Trace & Determinant Relations
```
λ₁ + λ₂ + ... + λₙ = trace(A) = Σ a_ii
λ₁ · λ₂ · ... · λₙ = det(A)
```

### Eigenvalue Transformations
```
A eigenvalues: λ₁, λ₂, ...
A⁻¹ eigenvalues: 1/λ₁, 1/λ₂, ...
A^k eigenvalues: λ₁^k, λ₂^k, ...
A + cI eigenvalues: λ₁+c, λ₂+c, ...
A + B (if same eigenvectors): λ_i(A) + λ_i(B)
```

---

## 4. Rank Formulas

### Row Echelon Form
```
rank = number of non-zero rows in REF
     = number of pivot positions
     = size of largest non-zero minor
```

### Important Relations
```
rank(A) = rank(A^T) = rank(A^T A) = rank(A A^T)
rank(A) ≤ min(m, n)
rank(kA) = rank(A) for k ≠ 0
rank(AB) ≤ min(rank(A), rank(B))
rank(A + B) ≥ |rank(A) - rank(B)|
rank([A B]) ≤ rank(A) + rank(B)
```

---

## 5. Cramer's Rule

```
For Ax = b where det(A) ≠ 0:

x_i = det(A_i) / det(A)

A_i = matrix with column i replaced by b
```

---

## 6. Cayley-Hamilton

```
Characteristic polynomial: p(λ) = det(λI - A) = 0
Then: p(A) = 0

To find A⁻¹:
Multiply p(A) = 0 by A⁻¹ and rearrange
```

---

## 7. Diagonalization

```
A = PDP⁻¹

D = diagonal matrix of eigenvalues
P = matrix of eigenvectors (as columns)

A^k = PD^k P⁻¹

D^k = diag(λ₁^k, λ₂^k, ..., λₙ^k)
```

---

## 8. Matrix Power Formulas

### Diagonalization Method
```
A^k = PD^k P⁻¹
```

### 2×2 Repeated Eigenvalue (Defective)
```
A^k = λ^k I + kλ^(k-1)(A - λI)   [when A not diagonalizable]
```

### Special Cases
```
Idempotent: A² = A → A^k = A for all k ≥ 1
Involutory: A² = I → A^k = A if k odd, I if k even
Nilpotent: A^m = 0 → A^k = 0 for k ≥ m
```

---

## 9. Orthogonal Matrix

```
A^T A = AA^T = I
A⁻¹ = A^T
|det(A)| = 1
Eigenvalues have |λ| = 1
Rows/columns form orthonormal set
```

---

## 10. Quadratic Form

```
Q(x) = x^T A x  [A symmetric]

Positive definite:    all λ_i > 0
Positive semi-definite: all λ_i ≥ 0
Negative definite:    all λ_i < 0
Negative semi-definite: all λ_i ≤ 0
Indefinite:           mixed signs of λ_i
```

---

## 11. Systems of Equations

### Homogeneous (Ax = 0)
```
Non-trivial solution exists ↔ det(A) = 0
Dimension of solution space = nullity(A) = n - rank(A)
```

### Non-Homogeneous (Ax = b)
```
Solution: x = x_p + x_h
x_p = particular solution
x_h = solution of Ax = 0

Unique: rank(A) = rank([A|b]) = n
Infinite: rank(A) = rank([A|b]) < n
None: rank(A) < rank([A|b])
```

---

## 12. Adjacency Matrix (Graph Theory Connection)

```
(A^k)_ij = number of walks of length k from vertex i to j

det(I - A) = number of spanning trees (for Laplacian)
```
