# Engineering Mathematics — Part 2: Linear Algebra & Multivariable Calculus

> Part 2 of 5 of the Engineering Mathematics question bank · Questions Q1–Q233 of this file
> Read this file top to bottom, in order. It continues from `01_real_calculus_and_series.md` and
> is followed by `03_complex_analysis_and_special_functions.md`.

**Covers / assumes.** This file is the working machinery of engineering mathematics: matrices
and their algebra, determinants, rank and Gaussian elimination, linear systems, vector-space
geometry (row / column / null spaces), eigenvalues and matrix decompositions, then multivariable
differentiation, optimisation and multiple integration. It assumes only single-variable
differentiation, basic integration and the meaning of a limit; nothing here needs series,
probability or complex-variable theory. Every matrix result is quoted in its worked form, so
the file is readable without any prior notes.

**Volume and difficulty.** 233 questions across 11 sections. Roughly 15% definition recall,
20% quick formula application, 25% medium 2–4 mark problems, 20% GATE 1-mark MCQ (tagged
`GATE-1`) and 20% GATE 2-mark MCQ / NAT / MSQ (tagged `GATE-2`).

---

## Section 1. Matrices: types, operations, transpose, trace, symmetric / skew-symmetric / Hermitian

### Q1. What is the order of a matrix, and which standard names apply to a matrix whose rows and columns are equal in number?

> **Type:** Theory
> **Answer:** The order of a matrix is the pair (m, n) meaning m rows and n columns. It is square when m = n, rectangular when m ≠ n; a 1 × n matrix is a row matrix and an m × 1 matrix is a column matrix.
> **Solution:** For A = (a_ij) with i = 1 … m and j = 1 … n, each entry a_ij is a scalar in the underlying field (real or complex here). The order is written A_{m×n}. A matrix is *diagonal* when all off-diagonal entries vanish, *scalar* when it is diagonal with all diagonal entries equal to the same k, the *identity* when the diagonal entries are all 1, and the *zero* (null) matrix when every entry is 0.
> **Key point:** Order (m, n) fixes the shape; square ⇔ row count = column count.

### Q2. Under what condition is A + B defined, and is scalar multiplication kA ever undefined?

> **Type:** Theory
> **Answer:** A + B is defined only when A and B have the same order m × n. Scalar multiplication kA is defined for every k for any A of any order.
> **Solution:** Addition is entrywise: (A + B)_ij = a_ij + b_ij, which needs a matching a_ij in both matrices. Multiplication by k is simply (kA)_ij = k a_ij, which never requires a second operand. This asymmetry is why matrix addition behaves like vector addition while matrix multiplication (Q3) does not behave like scalar multiplication.
> **Key point:** Addition needs equal orders; scalar multiplication never does.

### Q3. If A is of order m × n and B is of order n × p, is AB defined? What if A is m × n and B is q × n?

> **Type:** Theory
> **Answer:** AB is defined when the number of columns of A equals the number of rows of B (n = n here), giving a product of order m × p. It is **not** defined when A is m × n and B is q × n, because the inner dimensions n and n do match, so in fact that product *is* defined and gives order m × n — check the indexing carefully: A is m × n and B is q × n require n = q.
> **Solution:** (AB)_ij = Σ_{k=1}^{n} a_ik b_kj runs over k = 1 … n, so b_kj must exist for k up to n, i.e. B must have n rows. With B of order q × n the product needs n = q. So "A is m × n, B is q × n" is defined only when q = n, giving an m × n product. The rule is purely: inner dimensions must agree.
> **Key point:** AB needs (cols of A) = (rows of B); the result takes A's rows and B's columns.

### Q4. Two 2 × 2 matrices A = [[1,2],[3,4]] and B = [[0,1],[1,0]] are given. Compute AB and BA and comment.

> **Type:** Numerical
> **Answer:** AB = [[2,1],[4,3]] and BA = [[3,4],[1,2]], so AB ≠ BA — matrix multiplication is not commutative.
> **Solution:** AB = [[1·0+2·1, 1·1+2·0],[3·0+4·1, 3·1+4·0]] = [[2,1],[4,3]]. BA = [[0·1+1·3, 0·2+1·4],[1·1+0·3, 1·2+0·4]] = [[3,4],[1,2]]. Scalars commute (ab = ba) but matrices generally do not, so one cannot write AB = BA.
> **Key point:** AB ≠ BA in general — scalar-style cancellation and swapping is invalid.

### Q5. State which algebraic laws matrix multiplication obeys, and which law it does not.

> **Type:** Theory
> **Answer:** Matrix multiplication is **associative** ((AB)C = A(BC)) and **distributive** over addition (A(B + C) = AB + AC, (A + B)C = AC + BC). It is **not commutative**.
> **Solution:** Associativity follows because Σ_j Σ_k a_ik b_kj c_jl can be regrouped; commutativity fails as shown by the 2 × 2 counterexample. Note distributivity holds over *matrix addition* on both sides, which is why a scalar may always be moved in and out: k(AB) = (kA)B = A(kB).
> **Key point:** Associative yes, commutative no; scalars commute with everything.

### Q6. `GATE-1`. Let A and B be square matrices of the same order. Which statement is correct?

> (a) (AB)^T = A^T B^T
> (b) (AB)^T = B^T A^T
> (c) (AB)^T = (BA)^T
> (d) (AB)^T = A^H B^H where ^H is the conjugate transpose and A, B are real

> **Type:** MCQ `GATE-1`
> **Answer:** (AB)^T = B^T A^T (Option b).
> **Solution:** Entry (i, j) of (AB)^T equals entry (j, i) of AB, which is Σ_k a_jk b_ki. Entry (i, j) of B^T A^T is Σ_k b_ki a_jk — the same sum with the product written in the opposite order. Option (a) is the classic trap; option (c) is false since (AB)^T = (BA)^T would imply AB = BA; option (d) holds numerically for real A, B because the conjugate does nothing and (AB)^H = B^H A^H, which is again in the reversed order.
> **Key point:** The transpose reverses the order: (AB)^T = B^T A^T, never A^T B^T.

### Q7. Verify the transpose rules (A^T)^T = A, (kA)^T = kA^T and (A + B)^T = A^T + B^T.

> **Type:** Application
> **Answer:** All three hold for every A, B and scalar k: (A^T)^T = A, (kA)^T = kA^T = (kA^T), (A + B)^T = A^T + B^T.
> **Solution:** Each rule follows by transposing the defining index: ((A^T)^T)_ij = (A^T)_ji = a_ij. For (kA): (kA^T)_ij = k (A^T)_ij = k a_ji = (kA)^T_ij. For sums: (A+B)^T_ij = a_ji + b_ji. What is *not* true is that transpose distributes over matrix *multiplication* in the original order (Q6).
> **Key point:** Transpose is linear and involutive, but order-reversing on products.

### Q8. Recall the trace of a square matrix and the properties it satisfies.

> **Type:** Theory
> **Answer:** tr(A) = a_11 + a_22 + … + a_nn. Properties: tr(A + B) = tr(A) + tr(B), tr(kA) = k tr(A), tr(A^T) = tr(A), and tr(AB) = tr(BA) (whenever both products are defined).
> **Solution:** The trace sums the main diagonal entries, so each rule follows term by term except the last. For the last, tr(AB) = Σ_i Σ_k a_ik b_ki = Σ_k Σ_i b_ki a_ik = tr(BA) by interchanging the finite sums. Note tr(ABC) = tr(BCA) = tr(CAB) cyclically, but tr(ABC) ≠ tr(ACB) in general.
> **Key point:** tr(AB) = tr(BA) by cyclic invariance; transpose does not change the trace.

### Q9. A = [[1,2,0],[3,4,1],[0,1,2]] and B = [[2,0,1],[0,3,-1],[1,1,1]]. Find tr(AB) and tr(BA).

> **Type:** Numerical
> **Answer:** tr(AB) = tr(BA) = 16.
> **Solution:** AB = [[2,6,3],[7,11,6],[2,4,3]] and BA = [[3,6,7],[2,5,6],[3,8,10]]. Check by direct multiplication: AB row 1 = (1·2+2·0+0·1, 1·0+2·3+0·1, 1·1+2·(−1)+0·1) = (2, 6, 1) — recomputing the (1,3) entry gives 1·1 + 2·(−1) + 0·1 = −1, so AB = [[2,6,−1],[7,13,1],[2,5,1]] and tr(AB) = 2 + 13 + 1 = 16. By cyclic invariance tr(BA) = 16 as well.
> **Key point:** Whatever the entries, tr(AB) = tr(BA); here both equal 16.

### Q10. `GATE-1`. What is the trace of any skew-symmetric matrix of even order?

> (a) Zero
> (b) Equal to the sum of the squares of its entries
> (c) Equal to its determinant
> (d) Twice the sum of its entries above the main diagonal

> **Type:** MCQ `GATE-1`
> **Answer:** Zero (Option a).
> **Solution:** In a skew-symmetric matrix A^T = −A, which forces a_ii = −a_ii, hence a_ii = 0 on the whole diagonal. Since the trace is the sum of the (zero) diagonal entries, tr(A) = 0. Option (b) describes the trace of A^T A, not of A; option (d) describes twice the sum of the strictly-upper entries, which is tr(A^T) = −tr(A) = 0 again, so it equals 0 only coincidentally.
> **Key point:** Diagonal of a skew-symmetric matrix is zero, so its trace is zero.

### Q11. What does A^T = A guarantee? List three consequences.

> **Type:** Theory
> **Answer:** A is *symmetric*. Then (i) x^T A x is a scalar (real, for real A) equal to x^T A^T x for every x; (ii) all eigenvalues of A are real; (iii) every power A^k is symmetric.
> **Solution:** (i) x^T A x is a 1 × 1 matrix and satisfies (x^T A x)^T = x^T A^T x = x^T A x, so it equals its own transpose. (ii) follows from the eigenvalue–eigenvector equation transposed and combined: if Ax = λx then A^T x = λ̄ x̄, so for real A the eigenvalues come out real. (iii) follows from (A^k)^T = (A^T)^k = A^k. For complex matrices the corresponding condition is Hermitian, not symmetric.
> **Key point:** Symmetric ⇔ A^T = A; then quadratic forms are real, eigenvalues real, powers symmetric.

### Q12. A = [[1,2],[3,4]]. Compute tr(A^T A) and explain the significance of the result.

> **Type:** Numerical
> **Answer:** tr(A^T A) = 1 + 4 + 9 + 16 = 30, which is the square of the Frobenius (Hilbert–Schmidt) norm ‖A‖_F = √30 ≈ 5.477.
> **Solution:** (A^T A)_11 = 1² + 2² = 5 and (A^T A)_22 = 3² + 4² = 25, so the trace is 30. In general tr(A^T A) = Σ_i Σ_j a_ij², the sum of the squares of all entries. This is always ≥ 0, and it is zero **only** when A = 0, which proves the useful statement: A^T A = 0 implies A = 0 over the reals. The same trace equals the squared Frobenius norm used in least-squares fitting.
> **Key point:** tr(A^T A) = Σ a_ij² ≥ 0, so A^T A is positive semidefinite and vanishes only for A = 0.

### Q13. What must be true of a skew-symmetric matrix, and how do its rank and determinant behave?

> **Type:** Theory
> **Answer:** A^T = −A forces a_ii = 0 for every i and a_ij = −a_ji. Its rank is always even, and a skew-symmetric matrix of odd order has determinant 0.
> **Solution:** a_ii = −a_ii gives a_ii = 0 immediately; off-diagonal entries then come in equal-and-opposite pairs. The rank being even follows because the rank of a skew-symmetric matrix equals the number of conjugate pairs in its purely imaginary eigenvalues. If the order is odd, those pairs cannot fill the whole spectrum, so at least one eigenvalue is 0 and det A = 0.
> **Key point:** Odd-order skew-symmetric ⇒ singular; rank of a skew-symmetric matrix is even.

### Q14. K = [[0,2,−1],[−2,0,3],[1,−3,0]] is a real 3 × 3 matrix. Compute det K, rank K and the nature of its eigenvalues.

> **Type:** Numerical
> **Answer:** det K = 0, rank K = 2, and the eigenvalues are 0, +j√14 and −j√14 (≈ 0, ±j3.742) — purely imaginary, occurring in conjugate pairs.
> **Solution:** Expanding along the first row: det K = 0·M_11 − 2·M_12 + (−1)·M_13. M_12 = det[[−2,3],[1,0]] = −3, M_13 = det[[−2,0],[1,−3]] = 6, so det K = −2(−3) − 6 = 0. The 2 × 2 minor from rows 1, 2 and columns 1, 2 is det[[0,2],[−2,0]] = 4 ≠ 0, so rank ≥ 2; since det = 0 the rank is exactly 2. The characteristic equation det(K − λI) = −λ(λ² + 14) = 0 gives λ = 0, ±j√14, consistent with the even-rank and conjugate-pair rules.
> **Key point:** 3 × 3 skew-symmetric: det = 0, rank 2, spectrum {0, ±jω}.

### Q15. `GATE-2`. Let A be a real symmetric 4 × 4 matrix with tr(A) = 10 and det(A) = 2. Which of the following must be true?

> (a) All eigenvalues of A are positive
> (b) All eigenvalues of A are real
> (c) A is diagonalisable by a matrix P with P^T = P
> (d) tr(A^2) = 100

> **Type:** MSQ `GATE-2`
> **Answer:** (b) only.
> **Solution:** (b) is true: every eigenvalue of a real symmetric matrix is real. (a) is false — a positive determinant with even order gives an even number of negative eigenvalues, so two negatives and two positives is compatible with det = 2 > 0. (c) is false as written: P^T = P makes P symmetric, but a symmetric matrix with all eigenvalues equal to 1 (the identity) is orthogonal only in the trivial case; what is true is P^T P = I. (d) is false: tr(A^2) = Σ λ_i² which need not equal (Σ λ_i)² = 100.
> **Key point:** Symmetry guarantees real eigenvalues and orthogonal diagonalisation (Q^TAQ = Λ), nothing about signs.

### Q16. Define a Hermitian matrix and state how it differs from a symmetric one.

> **Type:** Theory
> **Answer:** A is Hermitian if A^H = A, where A^H = (A*)^T is the conjugate transpose (adjoint). For real A, A^H = A^T, so every real symmetric matrix is Hermitian; Hermitian is the correct notion over the complex field.
> **Solution:** Symmetric means A^T = A with no conjugation, and is only meaningful (as a self-adjointness condition) over the reals. Over the reals the two notions coincide exactly. A Hermitian matrix has real eigenvalues, real quadratic forms x^H A x, and is unitarily (orthogonally, if real) diagonalisable.
> **Key point:** Symmetric = transpose-self-adjoint (real); Hermitian = conjugate-transpose-self-adjoint (complex).

### Q17. H = [[1, 2j], [−2j, 3]] is a complex 2 × 2 matrix. Verify that H is Hermitian and report its trace, determinant and eigenvalues.

> **Type:** Numerical
> **Answer:** H is Hermitian, tr(H) = 4 (real), det(H) = −1, and its eigenvalues are 2 ± √5 ≈ 4.236 and −0.236, both real.
> **Solution:** H^H = conj(H)^T = [[1, −2j],[2j,3]]^T = [[1, 2j],[−2j,3]] = H, so H is Hermitian. tr(H) = 1 + 3 = 4, which is real as required for a Hermitian matrix. det(H) = 1·3 − (2j)(−2j) = 3 + 4j² = 3 − 4 = −1. The characteristic equation is λ² − 4λ − 1 = 0, giving λ = 2 ± √5.
> **Key point:** Hermitian ⇒ real trace and real eigenvalues, even when entries are complex.

### Q18. `GATE-1`. Let Z = [[1,1],[0,0]]. What is Z^2, and what category does Z belong to?

> (a) Z^2 = Z and Z is idempotent
> (b) Z^2 = 0 and Z is nilpotent
> (c) Z^2 = I and Z is an involution
> (d) Z^2 = −Z and Z is skew-symmetric

> **Type:** MCQ `GATE-1`
> **Answer:** (a) Z^2 = Z and Z is idempotent.
> **Solution:** Z^2 = [[1·1+1·0, 1·1+1·0],[0,0]] = [[1,1],[0,0]] = Z, so Z is **idempotent** (a projection). Its eigenvalues are 1 and 0, consistent with Z^2 = Z. It is not nilpotent (Z² ≠ 0), not an involution (Z² ≠ I), and not skew-symmetric since Z^T = [[1,0],[1,0]] ≠ −Z.
> **Key point:** Z^2 = Z is idempotent; its spectrum is contained in {0, 1}.

### Q19. A is a 3 × 3 matrix. As powers of A are formed, what can happen to the *order* of the product?

> **Type:** Conceptual
> **Answer:** A^k is 3 × 3 for every k ≥ 1 — the order never changes — unless a factor is the zero matrix, in which case the next product is the undefined 0 × 3 matrix rather than a 3 × 3 zero.
> **Solution:** Order composition says A·A is (3 × 3)(3 × 3) → 3 × 3 and inductively every power has order 3 × 3. A genuine zero matrix Z of order 3 × 3 times A would need Z to be 3 × 0 to be a legal 3 × 3 → 3 × 3 product with a 3 × 3 operand, so the product ZA is not defined — this is exactly the boundary case where "0 × A = 0" fails for matrices, unlike scalars.
> **Key point:** Powers preserve order 3 × 3; the scalar rule 0·A = 0 breaks down for matrices.

---

## Section 2. Determinants: properties, evaluation, minors and cofactors, expansions

### Q20. Define the determinant of a 2 × 2 matrix and state its notation.

> **Type:** Theory
> **Answer:** For A = [[a,b],[c,d]], det A = ad − bc. It is written |A|, det A or Δ(A), and equals the product ad minus bc.
> **Solution:** The determinant is a scalar function of the entries, defined recursively by cofactor expansion (Q29). Its geometric meaning for a 2 × 2 matrix is the signed area of the parallelogram spanned by the two row (or column) vectors, with orientation given by the sign of ad − bc. It is linear in each row separately and alternating (interchanging two rows flips the sign).
> **Key point:** det[[a,b],[c,d]] = ad − bc; sign encodes orientation.

### Q21. Evaluate det of M = [[2,1,0],[1,3,4],[5,−1,2]] by expanding along the first row.

> **Type:** Numerical
> **Answer:** det M = 38.
> **Solution:** The cofactors of row 1 are C_11 = det[[3,4],[−1,2]] = 6 + 4 = 10, C_12 = −det[[1,4],[5,2]] = −(2 − 20) = 18, C_13 = det[[1,3],[5,−1]] = −1 − 15 = −16. Hence det M = 2(10) + 1(18) + 0(−16) = 38. Row 1 was chosen because it contains a zero, which removes one term.
> **Key point:** Expand along the row or column with the most zeros; here 2·10 + 1·18 = 38.

### Q22. Define the minor and the cofactor of an entry.

> **Type:** Theory
> **Answer:** The minor M_ij of a_ij is the determinant of the (n − 1) × (n − 1) matrix obtained by deleting row i and column j. The cofactor is C_ij = (−1)^{i+j} M_ij.
> **Solution:** The sign factor alternates along the row, so the cofactors of any row read +, −, +, − … or −, +, −, + …. The Laplace expansion det A = Σ_{j=1}^{n} a_ij C_ij along row i then reconstructs the determinant from a single row. Confusing a minor with a cofactor (forgetting (−1)^{i+j}) is one of the most common computational errors.
> **Key point:** C_ij = (−1)^{i+j} M_ij; Laplace: det A = Σ_j a_ij C_ij along row i.

### Q23. For M = [[2,1,0],[1,3,4],[5,−1,2]], compute the three cofactors of the first row and use them to form the first row of adj(M).

> **Type:** Numerical
> **Answer:** C_11 = 10, C_12 = 18, C_13 = −16; the first row of adj(M) (which is the transpose of the cofactor matrix) is (10, 1, 4).
> **Solution:** From Q21, C_11 = 10, C_12 = 18, C_13 = −16. The adjugate is adj(M) = C^T, so the cofactors of the first row become the first *column* of adj(M); adj(M)'s first row is (C_11, C_21, C_31) = (10, 1, 4), using C_21 = −det[[1,0],[−1,2]] = −2 and C_31 = det[[1,0],[3,4]] = 4.
> **Key point:** adj(M) transposes the cofactors: adj(M)_ij = C_ji.

### Q24. State the product property of the determinant and give a numerical illustration.

> **Type:** Numerical
> **Answer:** det(AB) = det A · det B. For A = [[1,2],[3,4]] and B = [[0,1],[1,0]]: det A = −2, det B = −1, and AB = [[2,1],[4,3]] has det 6 − 4 = 2 = (−2)(−1).
> **Solution:** The identity det(AB) = det A det B means multiplicativity — the determinant is a homomorphism from the multiplicative monoid of matrices to the scalars. It immediately implies det(A^k) = (det A)^k and, for invertible A, det(A^{−1}) = 1/det A. It does **not** hold as det(A + B) = det A + det B (Q27).
> **Key point:** det(AB) = det A · det B, so det(A^k) = (det A)^k.

### Q25. State the effect of transpose and of scalar multiplication on the determinant.

> **Type:** Theory
> **Answer:** det(A^T) = det A, and for an n × n matrix, det(kA) = k^n det A.
> **Solution:** Transposition mirrors the matrix about the main diagonal; the determinant is unchanged because a cofactor expansion along row i of A equals the corresponding expansion along column i of A^T. Scalar multiplication scales every one of the n^2 entries, but the determinant is multilinear in n *rows*, not n^2 entries, so the determinant picks up exactly n factors of k. This is why det(−A) = (−1)^n det A, and hence det(−A) = −det A only for odd n.
> **Key point:** det(A^T) = det A; det(kA) = k^n det A (n rows, n powers of k).

### Q26. `GATE-1`. Which of the following matrices always has zero determinant?

> (a) A triangular matrix
> (b) A matrix with two identical rows
> (c) A matrix with all entries equal to 1
> (d) A symmetric matrix

> **Type:** MCQ `GATE-1`
> **Answer:** (b) A matrix with two identical rows (Option b).
> **Solution:** The determinant is *alternating*: interchanging two rows multiplies it by −1, so if two rows coincide the determinant equals its own negative and must be zero. Option (a) is false — a triangular matrix has determinant equal to the product of its diagonal entries, generally non-zero. Option (c) is false for n ≥ 2, where the all-ones matrix has rank 1 but a non-zero determinant for n = 1 only (for n = 2 it is [[1,1],[1,1]] with det 0, but [[1,1],[1,0]] is symmetric with det −1 ≠ 0, which kills option (d) and also shows "all entries 1" is not general).
> **Key point:** Repeated rows (or columns) ⇔ determinant 0 ⇔ matrix singular.

### Q27. `GATE-1`. Let A = [[1,2],[3,4]] and B = [[0,1],[1,0]]. Compare det(A + B) with det A + det B.

> (a) det(A + B) = det A + det B
> (b) det(A + B) = det A · det B
> (c) det(A + B) = det A + det B − 1
> (d) Neither quantity equals det(A + B); the relation is not additive

> **Type:** MCQ `GATE-1`
> **Answer:** (d) The determinant is not additive: det(A + B) = det[[1,3],[4,4]] = 4 − 12 = −8, while det A + det B = −2 + (−1) = −3.
> **Solution:** Numerically det(A + B) = −8 and det A + det B = −3, so (a), (b) and (c) are all false. The determinant is linear in each row *separately* when the other rows are held fixed, but cross terms appear when rows from two different matrices are mixed — for 2 × 2, det(A + B) = det A + det B + (a_11 b_22 + a_22 b_11 − a_12 b_21 − a_21 b_12), and here that cross term is −8 − (−3) = −5.
> **Key point:** Determinant is multiplicative (det AB = det A det B) but never additive.

### Q28. As the entry t of A(t) = [[t,1],[1,t]] varies, what happens to det A(t), and at which value is A(t) singular?

> **Type:** Boundary case
> **Answer:** det A(t) = t² − 1, which vanishes at t = ±1; A(t) is singular exactly at t = 1 and t = −1.
> **Solution:** det A(t) = t·t − 1·1 = t² − 1. At t = ±1 the determinant is zero, so no inverse exists and the associated homogeneous system has non-trivial solutions. At t = ±1 the matrix is [[±1, 1],[1, ±1]], whose rows become identical (t = 1) or opposite (t = −1) — both are the "repeated rows up to a sign" singularity mechanism. For |t| > 1 the matrix is positive definite; for |t| < 1 it is indefinite.
> **Key point:** det A(t) = t² − 1 → singular exactly at t = ±1.

### Q29. `GATE-2`. What is the determinant of A = [[1,2,3],[4,5,6],[7,8,9]]?

> (a) −3
> (b) 0
> (c) 3
> (d) 6

> **Type:** MCQ `GATE-2`
> **Answer:** 0 (Option b).
> **Solution:** Expanding along row 1: M_11 = det[[5,6],[8,9]] = 45 − 48 = −3, M_12 = det[[4,6],[7,9]] = 36 − 42 = −6, M_13 = det[[4,5],[7,8]] = 32 − 35 = −3. Hence det A = 1(−3) − 2(−6) + 3(−3) = −3 + 12 − 9 = 0. The structural reason is that the rows are in arithmetic progression: R2 − R1 = (3,3,3) and R3 − R2 = (3,3,3), so R1 − 2R2 + R3 = (1−8+7, 2−10+8, 3−12+9) = (0,0,0), i.e. the rows are linearly dependent and the determinant vanishes.
> **Key point:** Rows in arithmetic progression are dependent (R1 − 2R2 + R3 = 0), so det = 0 — answer (b).

### Q30. Explain why the determinant is best expanded along a row containing zeros, and compute det of the upper-triangular T = [[2,3,1],[0,−1,4],[0,0,5]].

> **Type:** Application
> **Answer:** Expanding along a row (or column) with zeros eliminates the corresponding terms, so only the nonzero entries contribute. det T = 2·(−1)·5 = −10, the product of the diagonal entries.
> **Solution:** A triangular matrix satisfies det T = product of diagonal entries, which itself follows from the same reasoning: expanding along the last row of an upper-triangular matrix leaves a smaller triangular matrix, and induction finishes. Here 2·(−1)·5 = −10, so T is non-singular.
> **Key point:** det of a triangular matrix = product of diagonal entries; expand where the zeros are.

### Q31. Compute det of the 2 × 2 matrix A(k) = [[2k, 3k],[k, 4k]] in terms of k, and find all k making it singular.

> **Type:** Numerical
> **Answer:** det A(k) = 8k² − 3k² = 5k², which vanishes only at k = 0.
> **Solution:** Applying the 2 × 2 rule: (2k)(4k) − (3k)(k) = 8k² − 3k² = 5k². Equivalently, by the scalar rule det(kM) = k² det M with M = [[2,3],[1,4]] and det M = 8 − 3 = 5. So k = 0 gives det = 0 (A becomes the zero matrix, the trivial singularity); any k ≠ 0 gives a non-zero determinant.
> **Key point:** det(kM) = k² det M for 2 × 2, so k = 0 is the only singular case.

### Q32. State the Vandermonde determinant formula and evaluate it for the nodes 1, 2, 3, 4.

> **Type:** Application
> **Answer:** For V = (x_j^{i−1}) with rows 1, x, x², x³, det V = ∏_{1≤i<j≤n} (x_j − x_i). For x = 1, 2, 3, 4 this equals (2−1)(3−1)(4−1)(3−2)(4−2)(4−3) = 1·2·3·1·2·1 = 12.
> **Solution:** The product runs over all pairs with the later node's value minus the earlier one's. Substituting: (2−1) = 1, (3−1) = 2, (4−1) = 3, (3−2) = 1, (4−2) = 2, (4−3) = 1, and 1·2·3·1·2·1 = 12. The Vandermonde form is what gives the interpolation formula and the barycentric weights used in least-squares fitting.
> **Key point:** det of the Vandermonde matrix = ∏_{i<j}(x_j − x_i); nodes 1,2,3,4 give 12.

### Q33. Give a column-operation trick for evaluating a determinant, and apply it to B = [[1,2],[1,3]].

> **Type:** Application
> **Answer:** Replacing a column by itself plus a multiple of another column leaves the determinant unchanged. Replacing C_1 of B by C_1 − C_2 gives [[−1,2],[−2,3]] with det = −3 + 4 = 1, which equals det B = 3 − 2 = 1.
> **Solution:** Adding k times column j to column i is a determinant-preserving operation (it corresponds to a unit-upper-triangular row-equivalent operation on the transposed matrix, whose determinant is 1). For B = [[1,2],[1,3]]: det = 1·3 − 2·1 = 1. After C_1 − C_2: [[−1,2],[−2,3]], det = (−1)(3) − (2)(−2) = −3 + 4 = 1. Confirmed. Useful operations that *do* change the determinant are scaling a row by k (multiply det by k) and swapping two rows (flip the sign).
> **Key point:** Row/column additions preserve the determinant; swaps negate it and scalings multiply it.

### Q34. `GATE-1`. A = [[1,1],[1,1]] and B = [[1,0],[0,1]]. Which relation is correct?

> (a) det(A + B) = det A + det B
> (b) det(A + B) = det A · det B
> (c) det(A − B) = det A − det B
> (d) det(A + B) = det A − det B

> **Type:** MCQ `GATE-1`
> **Answer:** (c) det(A − B) = det A − det B = −1 (Option c).
> **Solution:** det A = 1·1 − 1·1 = 0 and det B = 1. Then A + B = [[2,1],[1,2]] with det = 4 − 1 = 3, while det A + det B = 1 and det A · det B = 0 — so (a) and (b) are false, and 3 ≠ det A − det B = −1 kills (d). Finally A − B = [[0,1],[1,0]] with det = 0·0 − 1·1 = −1 = det A − det B = 0 − 1, so (c) holds. This agreement is a coincidence of this particular pair and is **not** a general law — for A = [[1,2],[3,4]] and B = [[0,1],[1,0]] the same two sides were −8 and −3.
> **Key point:** No general formula exists for det(A ± B); an accidental match is not a rule.

### Q35. `GATE-2`. A and B are 3 × 3 matrices with det A = 3 and det B = −2. Find det(A^T B^{-1}).

> (a) 1.5
> (b) −1.5
> (c) −6
> (d) −0.5

> **Type:** MCQ `GATE-2`
> **Answer:** −1.5 (Option b).
> **Solution:** det(A^T) = det A = 3, and multiplicativity gives det(B^{-1}) = 1/det B = 1/(−2) = −0.5. Hence det(A^T B^{-1}) = det(A^T)·det(B^{-1}) = 3 · (−0.5) = −1.5. Option (c) is the trap of forgetting to invert the factor 2 — or rather, of computing det A · det B instead of det A / det B; option (d) drops the factor det A.
> **Key point:** det(A^T B^{-1}) = det A / det B = 3 / (−2) = −1.5.

### Q36. Is det(A + B) computable from det A and det B alone? What extra information would be required?

> **Type:** Missing-data
> **Answer:** No. One needs the off-diagonal cross terms between rows of A and B — equivalently the entries themselves (or the eigenvalues of the pencil A + tB).
> **Solution:** Expanding det(A + B) with multilinearity in the rows gives det A + det B + Σ (one row from B, rest from A). Those mixed terms need individual entries, so two determinant values carry far less information than a full matrix. A sufficient data set is the full characteristic polynomial of A + tB in t; a minimal practical statement is that all entries of A and B are needed.
> **Key point:** det A and det B alone are insufficient for det(A + B) — cross terms matter.

---

## Section 3. Rank, row-reduced echelon form, Gaussian elimination, linear dependence

### Q37. Define the rank of a matrix and state the procedure for finding it.

> **Type:** Theory
> **Answer:** The rank of a matrix A is the largest number of linearly independent rows (equivalently columns) of A. It is found by row-reducing A to echelon form and counting the nonzero rows.
> **Solution:** "Largest number of linearly independent rows" and "largest number of linearly independent columns" always agree — both equal the dimension of the row space, which equals the dimension of the column space. The count of nonzero rows in *any* echelon form is the rank; row-reduced form is not required. For A with m rows and n columns, 0 ≤ rank A ≤ min(m, n).
> **Key point:** rank = number of nonzero rows in echelon form = dim row space = dim column space.

### Q38. State three rank facts that hold for any real matrix A.

> **Type:** Theory
> **Answer:** (i) rank A = rank A^T; (ii) rank A = rank(A^T A) = rank(AA^T); (iii) rank A ≤ min(m, n) for an m × n A, with equality iff A has a nonsingular square minor.
> **Solution:** (i) row space of A equals the column space of A^T as sets of vectors, and both have the same dimension. (ii) since x^T A^T A x = ‖Ax‖² ≥ 0 with equality only for Ax = 0, the null spaces of A and A^T A coincide, so the ranks match. (iii) follows from the independent-rows / independent-columns bounds; rank = n (full column rank) iff some n × n minor is non-zero.
> **Key point:** rank A = rank A^T = rank(A^T A); rank ≤ min(m, n).

### Q39. Find the rank of A = [[1,1,1],[1,1,2],[1,1,3]] by row reduction.

> **Type:** Numerical
> **Answer:** rank A = 2.
> **Solution:** Subtract row 1 from row 2 and from row 3: A → [[1,1,1],[0,0,1],[0,0,2]]. Then row 3 → row 3 − 2·row 2 gives [[1,1,1],[0,0,1],[0,0,0]], which has two nonzero rows. So rank A = 2. As a check, no 2 × 2 minor here is zero (e.g. the minor from rows 1,2 and columns 1,3 is 1·2 − 1·1 = 1 ≠ 0) while det A = 0, and indeed rows 1, 2 and 3 are related by R1 − 3R2 + 2R3 = 0.
> **Key point:** Count nonzero rows after row reduction; rows 1,2,3 satisfy R1 − 3R2 + 2R3 = 0.

### Q40. A = [[1,2,3],[4,5,6],[7,8,10]]. Determine its rank in two ways.

> **Type:** Numerical
> **Answer:** rank A = 3; equivalently det A = −3 ≠ 0, and row reduction gives three nonzero rows.
> **Solution:** Row reduction: R2 → R2 − 4R1 gives [0,−3,−6], R3 → R3 − 7R1 gives [0,−6,−11], then R3 → R3 − 2R2 gives [0,0,1]. Continuing to RREF yields the 3 × 3 identity, so three pivots and rank 3. The determinant route: det A = 1(50 − 48) − 2(40 − 42) + 3(32 − 35) = 2 + 4 − 9 = −3 ≠ 0, and a square matrix has full rank exactly when its determinant is non-zero.
> **Key point:** For a square matrix, rank = n ⟺ det ≠ 0; here rank 3, det = −3.

### Q41. `GATE-1`. What is the rank of the matrix A = [[1,2],[2,4]]?

> (a) 0
> (b) 1
> (c) 2
> (d) It cannot be determined without row reduction

> **Type:** MCQ `GATE-1`
> **Answer:** 1 (Option b).
> **Solution:** Row 2 equals 2 × row 1, so the rows are dependent and rank ≤ 1. Since row 1 = (1,2) ≠ 0, at least one row is independent, so rank ≥ 1. Hence rank = 1. Equivalently det A = 4 − 4 = 0 rules out rank 2, and a nonzero matrix cannot have rank 0. Option (d) is wrong because rank is unique and always computable; rank 0 is reserved for the zero matrix.
> **Key point:** Proportional rows ⇒ rank drops to 1; nonzero matrix ⇒ rank ≥ 1.

### Q42. `GATE-2`. The matrix A = [[1,2,1],[2,4,2],[3,6,3]] has what rank, and what does that imply about the linear system Ax = b?

> (a) rank 1, and Ax = b has either no solution or infinitely many for each b
> (b) rank 2, and Ax = b has a unique solution for every b
> (c) rank 3, and Ax = b has a unique solution for every b
> (d) rank 1, and Ax = b has a unique solution when b is in the column space

> **Type:** MCQ `GATE-2`
> **Answer:** (a) rank 1, and for a consistent system there are infinitely many solutions (never a unique one) (Option a).
> **Solution:** All rows are multiples of (1,2,1), and the columns are c1 = (1,2,3), c2 = 2c1, c3 = c1, so rank = 1 and det A = 0. Since the columns are dependent, the homogeneous system has non-trivial solutions, so any consistent non-homogeneous system has infinitely many, not a unique, solution — option (b) and (c) require a nonsingular matrix. Option (d) is a trap: consistency with b in the column space guarantees *infinitely* many solutions when rank < n.
> **Key point:** rank A < n ⇒ a consistent Ax = b has infinitely many solutions, never one.

### Q43. A(k) = [[1,2,3],[2,k,5],[1,0,1]]. How does rank A(k) depend on k?

> **Type:** Boundary case
> **Answer:** rank A(k) = 3 for k ≠ 3, and rank A(3) = 2.
> **Solution:** det A(k) = −2(k − 3), so the determinant is non-zero for all k ≠ 3 and the matrix has full rank 3. At k = 3 the determinant vanishes, so rank drops by at least one; the minor from rows 1, 2 and columns 1, 3 is 1·5 − 3·2 = −1 ≠ 0, so rank is still 2 at k = 3. The rank cannot fall further since a 2 × 2 minor survives.
> **Key point:** rank = n except where det = 0; here only k = 3 is exceptional, with rank 2.

### Q44. Distinguish an echelon form from a reduced row echelon (RREF) form.

> **Type:** Theory
> **Answer:** In an **echelon form** (i) all zero rows are at the bottom, (ii) the leading entry of each nonzero row is strictly to the right of the one above, (iii) entries below a leading entry are zero. A **reduced** echelon form additionally has every leading entry equal to 1 and zeros *above* and *below* each leading entry.
> **Solution:** Echelon form already determines the rank and the linear relations among rows, which is all Gaussian elimination needs. RREF is unique for a given matrix, while echelon form is not, and RREF additionally identifies pivot columns and hence a basis for the column space and the exact solution of a linear system. Echelon form is the work-horse for rank; RREF is the form in which you read off solutions.
> **Key point:** Echelon form counts pivots; RREF is unique and also gives solutions and pivot columns.

### Q45. Compute the RREF of A = [[1,2,3],[4,5,6],[7,8,9]] and identify the pivots.

> **Type:** Numerical
> **Answer:** RREF(A) = I_3, so there are three pivots (in columns 1, 2, 3) and rank 3.
> **Solution:** R2 → R2 − 4R1 = [0,−3,−6]; R3 → R3 − 7R1 = [0,−6,−12]. Then R3 → R3 − 2R2 = [0,0,0], R2 → R2/(-3) = [0,1,2], R2 → R2 − 2R3 has no effect, R1 → R1 − 3R3 no effect, R1 → R1 − 2R2 = [1,0,0]. The result is the identity, so every column is a pivot column. This is consistent with det A ≠ 0.
> **Key point:** RREF = I_3 here, so A is invertible and the columns form a basis of R^3.

### Q46. `GATE-1`. Row operations are used to reduce A to RREF. Which of the following do row operations preserve?

> (a) The column space of A
> (b) The row space of A
> (c) The column space of A^T
> (d) The null space of A

> **Type:** MCQ `GATE-1`
> **Answer:** (b) The row space of A (Option b).
> **Solution:** Row operations left-multiply by an invertible matrix E, and the row space of EA is E applied to the row space of A — a bijective change of basis within the same subspace, so the row space is unchanged. The column space does change: for A = [[1,2],[2,4]] the column space is span{(1,2)}, while after R2 → R2 − 2R1 the matrix is [[1,2],[0,0]], whose column space is span{(1,0)}. Hence the null space changes too (its dimension drops when rank drops), and (c) is the same statement as (a) with A^T's rows being A's columns.
> **Key point:** Row operations preserve the row space but **not** the column space or the null space.

### Q47. For A = [[1,2,3],[4,5,6],[7,8,9]], give one numerical reason (row reduction aside) for believing rank A = 3.

> **Type:** Application
> **Answer:** Any one non-zero 3 × 3 minor proves rank 3, and here the only 3 × 3 minor is det A = −3 ≠ 0; a single non-zero 2 × 2 minor such as det[[1,2],[4,5]] = −3 also shows rank ≥ 2.
> **Solution:** The rank of an m × n matrix is the order of the largest non-singular square submatrix. Here the 3 × 3 minor is det A = −3 ≠ 0, so rank A = 3. One does not need every minor: the single non-zero determinant settles it. In general, if the determinant happens to be zero one looks for the largest non-zero minor of order n − 1, then n − 2, and so on.
> **Key point:** rank = order of the largest non-singular minor; one non-zero n × n minor settles full rank.

### Q48. Perform two steps of Gaussian elimination on A = [[1,2,−1],[3,−1,2]] to obtain an upper-triangular form, and report the rank.

> **Type:** Numerical
> **Answer:** R2 → R2 − 3R1 gives [[1,2,−1],[0,−7,5]], which is upper triangular with two nonzero rows, so rank A = 2.
> **Solution:** The operation R2 ← R2 − 3R1 replaces row 2 by (3 − 3·1, −1 − 3·2, 2 − 3·(−1)) = (0, −7, 5). The result is upper triangular, so the number of nonzero rows gives rank 2. Check: the minor from rows 1,2 and columns 1,2 is 1·(−1) − 2·3 = −7 ≠ 0, so rank ≥ 2, and since only two rows exist rank ≤ 2.
> **Key point:** One elimination step gives an upper-triangular matrix with 2 nonzero rows ⇒ rank 2.

### Q49. `GATE-2`. For the system x + y + z = 3, x + y + 2z = 4, how many solutions are there, and what does the rank criterion say?

> (a) No solution, because rank A < rank [A|b]
> (b) Infinitely many solutions, because rank A = rank [A|b] = 2 < 3
> (c) A unique solution, because det A ≠ 0
> (d) Infinitely many solutions, because det A = 0

> **Type:** MCQ `GATE-2`
> **Answer:** (b) Infinitely many solutions, because rank A = rank [A|b] = 2 < 3 (Option b).
> **Solution:** A = [[1,1,1],[1,1,2]] and [A|b] = [[1,1,1,3],[1,1,2,4]]. Row-reducing: R2 ← R2 − R1 gives [[1,1,1,3],[0,0,1,1]], so both A and [A|b] have rank 2. Since rank A = rank [A|b], the system is consistent, and since rank A = 2 < n = 3 there is a free variable, hence infinitely many solutions. Option (d) is a trap: det A = 0 alone does not distinguish "no solution" from "infinitely many" — only the rank comparison does.
> **Key point:** Consistent ⇔ rank A = rank [A|b]; unique solution additionally needs rank A = n.

### Q50. `GATE-1`. The vectors v1 = (1,2,0)^T, v2 = (0,1,1)^T and v3 = (1,3,1)^T are given. What is their linear dependence status?

> (a) Linearly independent, because none of them is the zero vector
> (b) Linearly dependent, because v3 = v1 + v2
> (c) Linearly dependent, because v1 = v2 + v3
> (d) Linearly independent, because the determinant of the matrix formed is zero

> **Type:** MCQ `GATE-1`
> **Answer:** (b) Linearly dependent, because v3 = v1 + v2 (Option b).
> **Solution:** v1 + v2 = (1+0, 2+1, 0+1) = (1,3,1) = v3, so −v1 − v2 + v3 = 0 is a non-trivial relation. Equivalently the matrix with these as columns, V = [[1,0,1],[2,1,3],[0,1,1]], has det V = 0, which is the general test: vectors in R^n are dependent exactly when the matrix they form as columns (or rows) is singular. Option (a) is the classic error — non-zero individual vectors say nothing. Option (c) has the relation backwards: v2 + v3 = (1,4,2) ≠ v1.
> **Key point:** v's are dependent ⟺ det[v1 … vn] = 0 ⟺ some non-zero combination gives 0.

### Q51. Define linear dependence of a set of vectors and state how many linearly independent vectors R^n can contain.

> **Type:** Theory
> **Answer:** A set {v_1, …, v_k} is linearly dependent if scalars c_1, …, c_k, **not all zero**, exist with Σ c_i v_i = 0; otherwise it is independent. At most n vectors in R^n can be linearly independent, and any n independent vectors form a basis.
> **Solution:** The quantifier "not all zero" is essential: c_i = 0 for every i always works. Independence means the only solution of Σ c_i v_i = 0 is the trivial one, which for a square n × n matrix is exactly det ≠ 0. Consequently a set of more than n vectors in R^n is automatically dependent — this is called the *pigeonhole principle* for vector spaces and underlies the statement that a homogeneous system with more unknowns than independent equations has non-trivial solutions.
> **Key point:** > n vectors in R^n ⇒ automatically dependent; "not all c_i zero" is part of the definition.

### Q52. What is the maximum number of linearly independent vectors in R^5, and what does a set of 5 independent vectors form?

> **Type:** Conceptual
> **Answer:** At most 5; any set of 5 linearly independent vectors in R^5 forms a basis of R^5, and each vector in R^5 is a unique linear combination of them.
> **Solution:** R^5 has dimension 5, and a linearly independent set cannot have more elements than the dimension (proved by expressing each extra vector in a basis and finding a non-trivial relation). Independence of exactly 5 vectors in a 5-dimensional space means they span R^5, hence form a basis, giving both spanning and unique representation. In matrix terms this says a 5 × 5 matrix is invertible exactly when its columns are independent.
> **Key point:** dim R^n = n; n independent vectors form a basis (complete and minimal).

### Q53. `GATE-1`. The columns of A = [[1,1],[1,1]] are both nonzero. Does that make them linearly independent?

> (a) Yes — non-zero columns are always independent
> (b) No — c1 = (1,1)^T and c2 = (1,1)^T satisfy c1 − c2 = 0 with c1 − c2 ≠ 0
> (c) Yes — because det A = 0 only for even n
> (d) No — but only because both columns have equal magnitude

> **Type:** MCQ `GATE-1`
> **Answer:** (b) No — the two columns are equal, so c1 − c2 = 0 is a non-trivial relation (Option b).
> **Solution:** Both columns are (1,1)^T, so taking the coefficients (1, −1) gives 1·(1,1)^T + (−1)·(1,1)^T = 0 with coefficients not all zero. Hence the columns are dependent and rank A = 1. Option (a) is the fundamental misconception the question targets; option (c) is nonsense since det A = 0 happens at any order; option (d) gives the right conclusion for the wrong reason — dependence has nothing to do with magnitudes, only with the relation.
> **Key point:** Non-zero columns say nothing about independence; equal columns ⇒ dependent.

### Q54. State the rank inequalities for products and sums: what can you say about rank(AB), rank(A + B), rank(AB^T)?

> **Type:** Theory
> **Answer:** rank(AB) ≤ min(rank A, rank B); rank(A + B) ≤ rank A + rank B; rank(AB^T) = rank(AB^T) ≤ min(rank A, rank B), and for A m × n, B n × p one has rank(AB) ≤ min(m, p) as well.
> **Solution:** For AB, the columns of AB are combinations of columns of A, so they lie in the column space of A, giving rank(AB) ≤ rank A; applying the same argument to rows (or to A(AB) = (AB)B^T style reasoning) gives rank(AB) ≤ rank B. For the sum, expand A + B as A + (each column of B placed in its own column) and add the ranks. Equality in rank(AB) ≤ rank A requires A to have full column rank; equality in both simultaneously requires A and B both square and nonsingular.
> **Key point:** rank(AB) ≤ min(rank A, rank B); rank(A + B) ≤ rank A + rank B.

### Q55. A = [[1,2],[3,4]] (rank 2) and B = [[0,1],[0,0]] (rank 1). What is rank(AB)?

> **Type:** Numerical
> **Answer:** rank(AB) = 1, strictly less than rank A = 2.
> **Solution:** AB = [[1·0+2·0, 1·1+2·0],[3·0+4·0, 3·1+4·0]] = [[0,1],[0,3]], which has rank 1 (columns (0,0) and (1,3)). This attains the bound rank(AB) ≤ min(2, 1) = 1. It shows the inequality can be strict relative to rank A: even though A is invertible, the multiplication destroys one dimension because B itself has a null space.
> **Key point:** rank(AB) = 1 = rank B here; A invertible does not prevent rank loss caused by B's null space.

### Q56. Give an example where rank(A + B) is strictly smaller than both rank A and rank B.

> **Type:** Application
> **Answer:** Take A = [[1,0],[0,0]] and B = [[−1,0],[0,0]]. Then rank A = rank B = 1 but rank(A + B) = 0, strictly smaller than both.
> **Solution:** Each of A and B has exactly one nonzero row and one nonzero column, so both have rank 1. But A + B = [[0,0],[0,0]] = 0, the zero matrix, whose rank is 0. Rank is only subadditive in the upper direction (rank(A + B) ≤ rank A + rank B = 2); cancellation of entries can annihilate independent directions. In the contrasting pair A = [[1,0],[0,0]], B = [[0,0],[0,1]] the supports are disjoint and the ranks add to give rank(A + B) = 2.
> **Key point:** rank(A + B) can exceed, equal, or fall below both ranks — cancellation gives rank 0 from two rank-1 matrices.

### Q57. `GATE-2`. Given only that A is 3 × 3 and rank A = 2, what must be true?

> (a) A is invertible
> (b) det A = 0 and the homogeneous system Ax = 0 has a one-dimensional solution space
> (c) The columns of A form a basis of R^3
> (d) The homogeneous system Ax = 0 has only the trivial solution

> **Type:** MCQ `GATE-2`
> **Answer:** (b) det A = 0 and dim{n : An = 0} = 3 − 2 = 1 (Option b).
> **Solution:** rank A = 2 < 3 = n means A is singular, so det A = 0, which kills (a) and (d) (the null space is non-trivial). By rank–nullity, dim ker A = n − rank A = 1, so the null space is a line, not all of R^3. Option (c) is false because the three columns span a 2-dimensional subspace of R^3, so they are dependent and cannot form a basis.
> **Key point:** rank A = 2 for a 3 × 3 A ⇒ det A = 0 and null space dimension 1.

---

## Section 4. Systems of linear equations: consistency, rank criterion, Cramer's rule, homogeneous systems, eigenvector method

### Q58. State the rank criterion for consistency of a system of linear equations.

> **Type:** Theory
> **Answer:** For Ax = b with A of order m × n and b an m-vector, the system is consistent (has at least one solution) **if and only if** rank A = rank [A | b], where [A | b] is the m × (n + 1) augmented matrix.
> **Solution:** Write the rows of the augmented matrix; the system is consistent exactly when no row reduces to the form [0 0 … 0 | c] with c ≠ 0, i.e. no contradictory equation 0 = c. Such a row appears precisely when the augmented matrix has a row that is all zeros in the coefficient part but not in the last column — equivalently when the rank of the augmented matrix exceeds the rank of A. This is Rouché–Capelli's theorem.
> **Key point:** Consistent ⇔ rank A = rank [A|b]; a row [0…0 | c≠0] is the certificate of inconsistency.

### Q59. State the complete classification of a linear system by rank.

> **Type:** Theory
> **Answer:** If rank A = rank [A|b] = n, there is a unique solution. If rank A = rank [A|b] = r < n, there are infinitely many solutions (n − r free variables). If rank A < rank [A|b], there is no solution.
> **Solution:** The number of free variables is n − r, so a consistent system with n − r > 0 has a one-parameter, two-parameter, … family of solutions. Uniqueness requires r = n, which for a square n × n matrix is equivalent to det A ≠ 0. This trichotomy covers every case; note "no solution" and "infinitely many" are the two failure modes of a nonsingular-looking system.
> **Key point:** Unique ⇔ rank A = n; infinite ⇔ rank A = rank[A|b] < n; none ⇔ ranks differ.

### Q60. `GATE-1`. Consider the system x + y + z = 3, 2x + 2y + 2z = 6. How many solutions does it have?

> (a) None, because the two equations look proportional
> (b) Exactly one
> (c) Infinitely many, since the equations are dependent
> (d) Infinitely many only if x = y = z

> **Type:** MCQ `GATE-1`
> **Answer:** (c) Infinitely many, since the equations are dependent (Option c).
> **Solution:** A = [[1,1,1],[2,2,2]] has rank 1 and the augmented matrix [[1,1,1,3],[2,2,2,6]] also has rank 1 (the second equation is twice the first), so the ranks agree and the system is consistent. With rank 1 < n = 3 there are two free variables, so the solution set is the plane {(3 − s − t, s, t)}. Option (a) confuses dependent *consistent* equations with inconsistency; option (d) is a spurious restriction.
> **Key point:** Dependent equations that agree ⇒ infinitely many solutions, not inconsistency.

### Q61. `GATE-1`. Consider the system x + 2y + 3z = 2, x − 2y − z = 4, x + 2y + 3z = 2. Which is true?

> (a) No solution, because the first and third equations are identical
> (b) A unique solution
> (c) Infinitely many solutions
> (d) No solution, because two variables must be equal

> **Type:** MCQ `GATE-1`
> **Answer:** (c) Infinitely many solutions (Option c).
> **Solution:** The duplicated equation is redundant, not contradictory. A = [[1,2,3],[1,−2,−1],[1,2,3]] has rank 2, and the augmented matrix also has rank 2 because the duplicate carries the same right-hand side 2. Consistent with rank 2 < 3, so two-parameter family. Indeed, subtracting gives 4y + 4z = −2, i.e. y + z = −0.5, and the family is {(2 − 2y − 3z, y, z)} with y = −0.5 − z, giving {(−0.5 + z, −0.5 − z, z)}.
> **Key point:** A repeated identical equation is redundant; it leaves infinitely many solutions, not none.

### Q62. Find all solutions of the system x + 2y + 3z = 2, x − 2y − z = 4 by elimination, and describe the solution set.

> **Type:** Numerical
> **Answer:** y + z = −0.5 and x = −0.5 + z; the general solution is (x, y, z) = (−0.5 + t, −0.5 − t, t) for any real t — a one-parameter family.
> **Solution:** Subtract equation 1 from equation 2: (x − x) + (−4y) + (−4z) = 2 so −4y − 4z = −2, giving y + z = −0.5, i.e. y = −0.5 − z. Substitute into equation 1: x + 2(−0.5 − z) + 3z = 2 ⇒ x − 1 + z = 2 ⇒ x = 3 − z. Recomputing: 2(−0.5 − z) = −1 − 2z, so x − 1 − 2z + 3z = 2 ⇒ x = 3 − z. With z = t, the solution is (3 − t, −0.5 − t, t). Check with t = 1: (2, −1.5, 1): 2 − 3 + 3 = 2 ✓ and 2 + 3 − 1 = 4 ✓.
> **Key point:** Two independent equations in three unknowns ⇒ one free parameter; eliminate, then substitute.

### Q63. `GATE-2`. For the system x + 2y + 3z = 2, x − 2y − z = 4, x + 2y + 3z = 2, which of the following are true?

> (a) The system has exactly one solution
> (b) rank A = rank [A|b] = 2
> (c) There are two free variables
> (d) The system has no solution

> **Type:** MSQ `GATE-2`
> **Answer:** (b) only.
> **Solution:** The third equation repeats the first, so rank A = 2 and the augmented matrix also has rank 2 — (b) is true. With n = 3 and rank 2 the number of free variables is 3 − 2 = 1, so (c) is false. Since the ranks agree, the system is consistent with infinitely many solutions, so (a) and (d) are both false.
> **Key point:** rank A = rank[A|b] = 2 with n = 3 ⇒ consistent, infinite solutions, one free variable.

### Q64. State Cramer's rule for a system of n equations in n unknowns.

> **Type:** Theory
> **Answer:** If A is n × n with det A ≠ 0, the unique solution of Ax = b is x_i = D_i / D where D = det A and D_i is the determinant of A with its i-th column replaced by b.
> **Solution:** Cramer's rule follows from the adjugate formula x = A^{-1} b = adj(A) b / det A, since expanding each term gives exactly the determinant with one column replaced. Its cost is n + 1 determinants of order n, i.e. about (n + 1) n! operations, which grows factorially — this is why Gaussian elimination is used in practice even though Cramer's rule is algebraically exact. The rule simply does not apply when det A = 0, i.e. when the solution is not unique.
> **Key point:** x_i = D_i/D with D_i = A with column i replaced by b; requires det A ≠ 0.

### Q65. Solve 2x + y = 5, x + 3y = 2 by Cramer's rule.

> **Type:** Numerical
> **Answer:** x = 13/5 = 2.6, y = −1/5 = −0.2.
> **Solution:** A = [[2,1],[1,3]], D = 2·3 − 1·1 = 5. Replacing column 1 by b = (5,2): D_x = det[[5,1],[2,3]] = 15 − 2 = 13, so x = 13/5. Replacing column 2: D_y = det[[2,5],[1,2]] = 4 − 5 = −1, so y = −1/5. Verify: 2(2.6) + (−0.2) = 5.0 ✓ and 2.6 + 3(−0.2) = 2.0 ✓.
> **Key point:** D = 5, D_x = 13, D_y = −1 ⇒ (x, y) = (13/5, −1/5).

### Q66. Solve x − y + 2z = 4, 2x + y + z = 7, 3x − y − z = 1 by Cramer's rule.

> **Type:** Numerical
> **Answer:** x = 8/5 = 1.6, y = 26/15 ≈ 1.733, z = 31/15 ≈ 2.067.
> **Solution:** A = [[1,−1,2],[2,1,1],[3,−1,−1]] has D = det A = −15. Replacing column 1 by (4,7,1): D_x = det[[4,−1,2],[7,1,1],[1,−1,−1]] = 4(1·(−1) − 1·(−1)) − (−1)(7·(−1) − 1·1) + 2(7·(−1) − 1·1) = 4(0) + (−6) + 2(−8) = −22, so x = −22 / −15 = 22/15. Recomputing the whole solution directly to cross-check: from eq 1, y = x + 2z − 4. Substituting into eq 2: 2x + x + 2z − 4 + z = 7 ⇒ 3x + 3z = 11 ⇒ x + z = 11/3. From eq 3: 3x − x − 2z + 4 − z = 1 ⇒ 2x − 3z = −3. Using x = 11/3 − z: 2(11/3 − z) − 3z = −3 ⇒ 22/3 − 5z = −3 ⇒ 5z = 31/3 ⇒ z = 31/15, x = 11/3 − 31/15 = 55/15 − 31/15 = 24/15 = 8/5, y = 8/5 + 62/15 − 4 = 24/15 + 62/15 − 60/15 = 26/15. Hence (x, y, z) = (8/5, 26/15, 31/15) and D_x = 8/5 · (−15) = −24, D_y = (26/15)(−15) = −26, D_z = 31.
> **Key point:** D = −15 with D_x = −24, D_y = −26, D_z = 31 ⇒ (x,y,z) = (8/5, 26/15, 31/15).

### Q67. `GATE-2`. What is the solution of the system 2x + y = 5, x + 3y = 2?

> (a) x = 2.6, y = −0.2
> (b) x = −0.2, y = 2.6
> (c) x = 1, y = 3
> (d) x = 2.6, y = 0.2

> **Type:** MCQ `GATE-2`
> **Answer:** (a) x = 2.6, y = −0.2 (Option a).
> **Solution:** Eliminating y: multiply the first equation by 3 to get 6x + 3y = 15 and subtract the second: 5x = 13, so x = 13/5 = 2.6; then y = 5 − 2(2.6) = −0.2. Option (b) swaps the answers — a common slip. Option (c) fails: 2 + 3 = 5 ✓ but 1 + 9 = 10 ≠ 2. Option (d) fails the first equation: 5.2 + 0.2 = 5.4 ≠ 5.
> **Key point:** (x, y) = (13/5, −1/5) = (2.6, −0.2); sign of y is easy to get wrong.

### Q68. What can be said about a homogeneous system Ax = 0 when A is singular?

> **Type:** Theory
> **Answer:** The system always has the trivial solution x = 0 and, since det A = 0 means A is singular, it also has at least one non-trivial solution; the solution space is the null space of A and has dimension n − rank A ≥ 1.
> **Solution:** A homogeneous system can never be inconsistent, because x = 0 satisfies it always. Its solution set is a subspace (the null space), so if it contains any non-zero vector it contains infinitely many scalar multiples. Invertibility is exactly the condition for the null space to be trivial: det A ≠ 0 ⇔ rank A = n ⇔ only x = 0.
> **Key point:** Homogeneous systems are always consistent; det A = 0 ⇒ null space dimension n − rank A ≥ 1.

### Q69. Determine the solution set of the homogeneous system x + 2y + 3z = 0, 2x + 5y + 7z = 0, 3x + 6y + 10z = 0.

> **Type:** Numerical
> **Answer:** Only the trivial solution x = y = z = 0, since det A = 1 ≠ 0.
> **Solution:** det A = det[[1,2,3],[2,5,7],[3,6,10]] = 1(50 − 42) − 2(20 − 21) + 3(12 − 15) = 8 + 2 − 9 = 1 ≠ 0. Since the matrix is nonsingular, the only solution of Ax = 0 is x = 0. This illustrates that the number of equations matching the number of unknowns is not enough — the coefficient matrix must be nonsingular.
> **Key point:** det = 1 ≠ 0 ⇒ Ax = 0 has only the trivial solution, regardless of how the rows look.

### Q70. `GATE-1`. A is 3 × 3 with rank 2. How many free variables does Ax = 0 have?

> (a) None, because the system is homogeneous
> (b) One
> (c) Two
> (d) Three

> **Type:** MCQ `GATE-1`
> **Answer:** (c) Two (Option c).
> **Solution:** By rank–nullity, dim ker A = n − rank A = 3 − 2 = 1 dimension, i.e. one free parameter. The null space is a line in R^3 through the origin, so one variable is free and the other two are determined. Option (a) is wrong: homogeneity does not remove free variables, it only guarantees the zero solution. If the question had asked about a *non-homogeneous consistent* system with rank 2 and n = 3, the answer would again be one free variable.
> **Key point:** Free variables in Ax = 0 equal n − rank A; here 3 − 2 = 1, so the null space is a line.

### Q71. `GATE-2`. A homogeneous system of 4 equations in 3 unknowns has rank 2. What is the dimension of its solution space?

> (a) 0
> (b) 1
> (c) 2
> (d) 3

> **Type:** MCQ `GATE-2`
> **Answer:** (b) 1 (Option b).
> **Solution:** Rank–nullity: dim N(A) = n − rank A = 3 − 2 = 1, independent of the number of equations (4), which only limits rank to at most 3. So the solution space is a one-dimensional line through the origin. Note the trap: the four equations might suggest "four − two = two free variables", but only the *rank* and the *number of unknowns* matter.
> **Key point:** dim N(A) = n − rank A; the number of equations is irrelevant.

### Q72. Describe the eigenvector method for solving a consistent system of two linear equations.

> **Type:** Application
> **Answer:** Write the system Ax = b with A 2 × 2, find the eigenvalues λ₁, λ₂ of A by det(A − λI) = 0, get corresponding eigenvectors v₁, v₂, write x = c₁v₁ + c₂v₂, and then the two scalars c₁, c₂ satisfy a 2 × 2 system c₁λ₁ = (v₁^T b) and c₂λ₂ = (v₂^T b), provided v₁^T v₂ = 0 (eigenvectors are orthogonal when A is symmetric).
> **Solution:** If A is symmetric with orthogonal eigenvectors normalised to unit length, write x in that eigenbasis: x = Σ c_i v_i. Then b = Ax = Σ c_i λ_i v_i, and projecting on v_j gives v_j^T b = c_j λ_j. Hence c_j = (v_j^T b)/λ_j, which fails only if some λ_j = 0. For non-symmetric A one must instead use P^{-1} b with P = [v₁ v₂], i.e. c = P^{-1}b.
> **Key point:** In the eigenbasis, b's components are c_j λ_j, so c_j = (v_j^T b)/λ_j; needs λ ≠ 0.

### Q73. Solve x + 2y = 5, 2x + 4y = 10 — or is the eigenvector method applicable here?

> **Type:** Application
> **Answer:** The system has infinitely many solutions (rank 1 < 2): x = 5 − 2y for any y. The eigenvector method is not applicable because A = [[1,2],[2,4]] is singular (det A = 0), so one of its eigenvalues is 0 and the projection step divides by zero.
> **Solution:** Row 2 of A is twice row 1, so rank A = 1 and n = rank A gives one free variable. Det A = 4 − 4 = 0, so one eigenvalue vanishes; the eigenvector method needs all eigenvalues non-zero, hence it breaks down exactly in the degenerate case. The general rule is: eigenvector method ⇔ A invertible (distinct eigenvalues or a diagonalisable invertible A).
> **Key point:** Eigenvector method requires det A ≠ 0; at det A = 0 the system is singular with free variables.

### Q74. Solve 2x + y = 5, x + 2y = 8 using eigenvectors.

> **Type:** Numerical
> **Answer:** x = 2/3, y = 11/3.
> **Solution:** A = [[2,1],[1,2]] is symmetric, and det(A − λI) = (2 − λ)² − 1 = λ² − 4λ + 3 = (λ − 3)(λ − 1). So λ₁ = 3 with v₁ = (1,1)^T/√2 (since (A − 3I) = [[−1,1],[1,−1]] forces x = y) and λ₂ = 1 with v₂ = (1,−1)^T/√2. The eigenvectors are orthogonal since v₁·v₂ = (1 − 1)/2 = 0. With b = (5,8): v₁·b = 13/√2, so c₁ = (13/√2)/3 = 13/(3√2); v₂·b = (5 − 8)/√2 = −3/√2, so c₂ = −3/√2. Hence x = c₁(1/√2) + c₂(1/√2) = 13/6 − 3/2 = 4/6 = 2/3 and y = c₁(1/√2) − c₂(1/√2) = 13/6 + 3/2 = 22/6 = 11/3. Check: 2(2/3) + 11/3 = 15/3 = 5 ✓ and 2/3 + 2(11/3) = 24/3 = 8 ✓.
> **Key point:** Symmetric A ⇒ orthogonal eigenvectors ⇒ c_j = (v_j·b)/λ_j; here x = 2/3, y = 11/3.

### Q75. Solve x + 2y = 5, 2x + y = 2 by the eigenvector method.

> **Type:** Numerical
> **Answer:** x = −1/3, y = 8/3.
> **Solution:** A = [[1,2],[2,1]] is symmetric with det(A − λI) = (1 − λ)² − 4 = λ² − 2λ − 3 = (λ − 3)(λ + 1), so λ₁ = 3 with v₁ = (1,1)/√2 and λ₂ = −1 with v₂ = (1,−1)/√2. The eigenvectors are orthogonal (v₁·v₂ = 0). With b = (5,2): c₁ = (v₁·b)/λ₁ = (7/√2)/3 = 7/(3√2) and c₂ = (v₂·b)/λ₂ = (3/√2)/(−1) = −3/√2. Then x = c₁/√2 + c₂/√2 = 7/6 − 3/2 = 7/6 − 9/6 = −1/3 and y = c₁/√2 − c₂/√2 = 7/6 + 3/2 = 7/6 + 9/6 = 8/3. Check: −1/3 + 2(8/3) = −1/3 + 16/3 = 15/3 = 5 ✓ and 2(−1/3) + 8/3 = 6/3 = 2 ✓.
> **Key point:** Symmetric A ⇒ orthogonal eigenvectors ⇒ c_j = (v_j·b)/λ_j; here x = −1/3, y = 8/3.

### Q76. `GATE-2`. The system x + y = 1, 2x + 2y = 2 is attacked by the eigenvector method with A = [[1,1],[2,2]]. What goes wrong and why?

> (a) Nothing — the method gives a unique solution
> (b) One eigenvalue is 0, so the component of b along its eigenvector cannot be recovered by dividing by λ
> (c) The method fails because the two eigenvectors are not orthogonal
> (d) The method fails because b is not an eigenvector of A

> **Type:** MCQ `GATE-2`
> **Answer:** (b) One eigenvalue is 0, so the division step breaks down (Option b).
> **Solution:** det(A − λI) = (1 − λ)(2 − λ) − (1)(2) = 2 − 3λ + λ² − 2 = λ² − 3λ = λ(λ − 3), so the eigenvalues are 0 and 3. The projection formula c_j = (v_j·b)/λ_j divides by λ, so the λ = 0 eigenvector's coefficient is unrecoverable — which reflects the mathematics: rank A = 1 < 2, so the system has infinitely many solutions and there is no unique answer to recover. Option (c) is irrelevant because the method never needs orthogonality (it uses P^{-1}b in general). Option (d) is not a requirement at all.
> **Key point:** Eigenvalues 0 and 3; λ = 0 breaks the division step exactly because A is singular and the solution is non-unique.

---

## Section 5. Vector space, basis, dimension, row space vs column space vs null space, fundamental subspaces

### Q77. List the ten axioms that make a set V with operations + and scalar multiplication a vector space over ℝ.

> **Type:** Theory
> **Answer:** For all u, v, w ∈ V and scalars a, b: (1) u + v ∈ V, (2) u + v = v + u, (3) (u + v) + w = u + (v + w), (4) ∃ 0 ∈ V with u + 0 = u, (5) ∀u ∃(−u) with u + (−u) = 0, (6) au ∈ V, (7) a(u + v) = au + av, (8) (a + b)u = au + bu, (9) a(bu) = (ab)u, (10) 1·u = u.
> **Solution:** Axioms 1 and 6 are *closure*, the rest are algebraic structure. The zero vector and additive inverse must be *in* V — this is exactly why the set of all solutions of a homogeneous system (which contains 0) is a vector space while the solution set of a non-homogeneous system generally is not, because it fails closure under negation.
> **Key point:** Closure is part of the definition; the zero vector must belong to V.

### Q78. How do you test whether a subset W of a vector space V is itself a vector space?

> **Type:** Theory
> **Answer:** W is a subspace of V if and only if (i) the zero vector of V lies in W and (ii) W is closed under linear combination: for u, v ∈ W and scalars a, b, the combination au + bv is in W.
> **Solution:** It is enough to check only two things because the other axioms are inherited from V automatically. Equivalently: W contains 0 and is closed under addition and under scalar multiplication. The single test "au + bv ∈ W" bundles both, so a set closed under all linear combinations of its own elements is automatically a subspace.
> **Key point:** 0 ∈ W and au + bv ∈ W for all — that is the whole test.

### Q79. Which of the following sets are subspaces of R³? Justify each briefly.

> (a) all vectors with first coordinate 0
> (b) all vectors with x + y = 1
> (c) all vectors satisfying x − 2y + 3z = 0
> (d) all vectors of the form (t, 2t, 0)

> **Type:** MSQ
> **Answer:** (a), (c) and (d) are subspaces; (b) is not.
> **Solution:** (a) is the set {0} × R²: contains 0 and is closed under linear combinations. (c) is the kernel of the linear functional (1, −2, 3), hence a plane through the origin containing 0 and closed under combinations. (d) is span{(1,2,0)}, a line through the origin, and is closed. (b) is an *affine* plane not passing through the origin: it excludes 0 (since 0 + 0 = 0 ≠ 1) and it is not closed under scaling, because (1,0,0) ∈ set but 2·(1,0,0) = (2,0,0) fails x + y = 1.
> **Key point:** Kernels of linear maps and spans are subspaces; planes not through the origin are not.

### Q80. Define a basis and the dimension of a subspace W.

> **Type:** Theory
> **Answer:** A basis of W is a linearly independent set of vectors of W that spans W. The dimension dim W is the number of vectors in any basis of W; it is well defined because all bases of a space have the same cardinality.
> **Solution:** Basis = "complete and minimal". Completeness (spanning) makes every vector of W a combination of basis vectors; minimality (independence) makes that combination unique. In matrix terms a basis of the column space of A is exactly the set of pivot columns read off from the RREF of A.
> **Key point:** A basis is linearly independent **and** spanning; dim = its size.

### Q81. Find a basis for the null space of A = [[1,2,3],[4,5,6],[1,1,1]] and state its dimension.

> **Type:** Numerical
> **Answer:** The null space is spanned by the single vector (1, −2, 1)^T, so dim N(A) = 1.
> **Solution:** Row-reducing with R2 ← R2 − 4R1 and R3 ← R3 − R1 gives rows (1,2,3) and (0,−3,−6) and (0,−1,−2); scaling and subtracting yields the RREF [[1,0,−1],[0,1,2],[0,0,0]]. Reading off Ax = 0: x₁ − x₃ = 0 and x₂ + 2x₃ = 0, so with x₃ = t the solution is x = t(1, −2, 1)^T. Verification: row 1 gives 1 − 4 + 3 = 0 ✓, row 2 gives 4 − 10 + 6 = 0 ✓, row 3 gives 1 − 2 + 1 = 0 ✓. Since x₃ is the only free variable, dim N(A) = 3 − 2 = 1.
> **Key point:** Free variables of Ax = 0 give a basis of N(A); here x₃ is free and dim N(A) = 1.

### Q82. The four fundamental subspaces of a 3 × 4 matrix A are listed. Which dimension statement is correct?

> (a) dim(row space) = dim(column space) = rank A, and dim(null space) = 4 − rank A
> (b) dim(row space) = number of rows = 3
> (c) dim(column space) = number of columns = 4
> (d) dim(null space) = rank A

> **Type:** MCQ
> **Answer:** (a).
> **Solution:** The row space lives in R⁴ (it spans R⁴ via its rows) and the column space lives in R³, so option (b) — row space dimension = 3 — confuses the ambient dimension of the column space with the row space, and option (c) confuses it the other way. Rank–nullity gives dim N(A) = n − rank A = 4 − rank A, so (d) is wrong unless rank A = 2. The remaining fundamental subspace is the left null space N(A^T), of dimension 3 − rank A, living in R³.
> **Key point:** dim row = dim col = rank; dim N(A) = n − rank; dim N(A^T) = m − rank.

### Q83. For A = [[1,2,3],[4,5,6],[1,1,1]], give bases of the row space, column space, null space and left null space, with dimensions.

> **Type:** Numerical
> **Answer:** rank A = 2. Row space: {(1,2,3), (0,1,2)}, dim 2 in R³. Column space: {(1,4,1)^T, (2,5,1)^T}, dim 2 in R³. Null space: {(1,−2,1)^T}, dim 1. Left null space: {(−1,1,−3)^T}, dim 1.
> **Solution:** det A = 1(5 − 6) − 2(4 − 6) + 3(4 − 5) = −1 + 4 − 3 = 0, while the minor from rows 1, 2 and columns 1, 2 is 1·5 − 2·4 = −3 ≠ 0, so rank A = 2. Row reduction R2 ← R2 − 4R1, R3 ← R3 − R1 gives rows (1,2,3) and (0,−3,−6), i.e. a basis {(1,2,3), (0,1,2)} for the row space. The pivot columns are columns 1 and 2, and one must take the *original* columns (1,4,1)^T and (2,5,1)^T, not the reduced ones. Rank–nullity gives dim N(A) = 3 − 2 = 1, spanned by (1,−2,1)^T. For the left null space, A^T y = 0 reads y₁ + 4y₂ + y₃ = 0, 2y₁ + 5y₂ + y₃ = 0, 3y₁ + 6y₂ + y₃ = 0; subtracting the first from the second gives y₁ + y₂ = 0, and then the first gives 3y₂ + y₃ = 0, so y ∝ (−1, 1, −3), verified as −(1,4,1) + (2,5,1) − 3(3,6,1) = (0,0,0).
> **Key point:** Basis of column space = *original* pivot columns; basis of row space = nonzero rows of an echelon form.

### Q84. The three eigenvalues of A = [[1,2,3],[4,5,6],[1,1,1]] are found from det A = 0. What is rank A, and how do the four fundamental subspaces look?

> **Type:** Numerical
> **Answer:** rank A = 2, so the row and column spaces are 2-dimensional subspaces of R³, N(A) is the line spanned by (1,−2,1)^T, and N(A^T) is the line spanned by (−1,1,−3)^T.
> **Solution:** det A = −1 + 4 − 3 = 0 shows only that rank A < 3; the non-zero 2 × 2 minor 1·5 − 2·4 = −3 pins rank A = 2 exactly. Rank–nullity then fixes both null space dimensions at 3 − 2 = 1, and each is a single line through the origin, given by the generators computed in Q83. The row and column spaces are each 2-dimensional planes inside R³; they are not the same set of vectors because one contains row vectors of length 3 and the other column vectors of length 3.
> **Key point:** det A = 0 only says rank < 3; a surviving 2 × 2 minor then fixes rank = 2 and both null spaces at dimension 1.

### Q85. `GATE-1`. The row space of a matrix A is contained in R⁴ and the column space of A is contained in R³. What is A's order?

> (a) 4 × 3
> (b) 3 × 4
> (c) 4 × 4
> (d) 3 × 3

> **Type:** MCQ `GATE-1`
> **Answer:** (b) 3 × 4 (Option b).
> **Solution:** The row space is a subspace of R^n because each row has n entries, so n = 4. The column space is a subspace of R^m because each column has m entries, so m = 3. Hence A is 3 × 4: 3 rows (living in R⁴) and 4 columns (living in R³). Option (a) has the roles reversed — a 4 × 3 matrix has its row space in R³ and column space in R⁴.
> **Key point:** Row space ⊆ R^n, column space ⊆ R^m, so A is m × n.

### Q86. The null space of a matrix A is a subspace of which ambient space, and of what dimension?

> **Type:** Theory
> **Answer:** N(A) is a subspace of R^n (or C^n) for A of order m × n, and dim N(A) = n − rank A by rank–nullity.
> **Solution:** A vector x ∈ N(A) satisfies Ax = 0, and multiplying an m × n matrix by a vector gives an m-vector, so x must have n components. Rank–nullity, dim N(A) + rank A = n, is the dimension count; the left null space N(A^T) is the corresponding object of dimension m − rank A. The null space is invariant under row operations (Ax = 0 ⇔ (EA)x = 0), which is why it is read off from the RREF.
> **Key point:** N(A) ⊆ R^n with dim N(A) = n − rank A; N(A^T) ⊆ R^m with dim = m − rank A.

### Q87. `GATE-2`. For A = [[1,2,3],[4,5,6],[1,1,1]], which of the following are true?

> (a) rank A = 2
> (b) dim(row space) = dim(column space)
> (c) dim N(A) = 0
> (d) The columns of A are a basis of R³

> **Type:** MSQ `GATE-2`
> **Answer:** (a) and (b) are true; (c) and (d) are false.
> **Solution:** det A = 1(5 − 6) − 2(4 − 6) + 3(4 − 5) = −1 + 4 − 3 = 0, while the minor from rows 1, 2 and columns 1, 2 is 1·5 − 2·4 = −3 ≠ 0, so rank A = 2, making (a) true. Row and column spaces always have equal dimension (= rank), so (b) is true. Rank–nullity gives dim N(A) = 3 − 2 = 1, not 0, so (c) is false. Option (d) fails because three vectors in a 2-dimensional space cannot be a basis — at least two of the columns must be dependent.
> **Key point:** rank A = 2, so dim N(A) = 1 and three columns spanning a 2-dimensional space cannot be a basis.

### Q88. The vectors v₁ = (1,1,0), v₂ = (0,1,1) and v₃ = (1,2,1) are given. Are they a basis of R³?

> **Type:** Numerical
> **Answer:** No — they are linearly dependent, because v₁ + v₂ = (1,2,1) = v₃, so they do not form a basis.
> **Solution:** v₁ + v₂ = (1+0, 1+1, 0+1) = (1,2,1) = v₃, so −v₁ − v₂ + v₃ = 0 is a non-trivial relation and the set is dependent. Equivalently, the matrix with these as columns, V = [[1,0,1],[1,1,2],[0,1,1]], has det V = 1(1·1 − 2·1) − 0(1·1 − 2·0) + 1(1·1 − 1·0) = (1 − 2) + 0 + 1 = 0, confirming dependence. Three vectors in R³ form a basis exactly when they are linearly independent, which is not the case here; the pair {v₁, v₂} is already a basis of their 2-dimensional span.
> **Key point:** v₃ = v₁ + v₂ ⇒ dependent ⇒ not a basis; the determinant of the column matrix is 0.

### Q89. A vector set {v₁, v₂, v₃} in R³ has v₁, v₂ independent and v₃ = 2v₁ − v₂. What is the dimension of their span?

> **Type:** Application
> **Answer:** The span has dimension 2.
> **Solution:** Since v₃ is a linear combination of v₁ and v₂, adding it introduces no new direction; because v₁ and v₂ are independent the span of {v₁, v₂} already has dimension 2, and span{v₁,v₂,v₃} equals it. So dim = 2 and the set is a dependent set in a 2-dimensional subspace.
> **Key point:** Adding linear combinations never increases dimension; rank of a coefficient matrix counts independent directions.

### Q90. `GATE-1`. Is the null space of A the same subspace as the row space of A?

> (a) Yes, they are both computed from A
> (b) No — the row space is spanned by the rows and the null space by solutions of Ax = 0; for a square nonsingular matrix the null space is {0} while the row space is R^n
> (c) Yes, provided A is symmetric
> (c') Yes, provided rank A = n
> (d) They coincide only when A has one row

> **Type:** MCQ `GATE-1`
> **Answer:** (b).
> **Solution:** The row space is the span of A's rows (viewed as vectors in R^n) while N(A) = {x : Ax = 0} is a set of *coefficients* annihilating those rows. For A = [[1,2],[3,4]] the row space is R² but N(A) = {0}, so they cannot be equal. What is true is a duality: N(A) is the orthogonal complement (R(A^T))^⊥ of the row space, and its dimension is n − rank A rather than rank A. Options (c), (c′) and (d) are false.
> **Key point:** Row space = range of A^T; N(A) = (row space)^⊥, a different subspace of complementary dimension.

### Q91. `GATE-2`. Let A be 3 × 4 with rank 2. What are the dimensions of, in order, the row space, column space, null space and left null space?

> (a) 2, 2, 2, 1
> (b) 4, 3, 1, 1
> (c) 2, 2, 1, 2
> (d) 3, 4, 2, 1

> **Type:** MCQ `GATE-2`
> **Answer:** (a) 2, 2, 2, 1 (Option a).
> **Solution:** Row space and column space both have dimension rank A = 2. Rank–nullity gives dim N(A) = n − rank A = 4 − 2 = 2, and dim N(A^T) = m − rank A = 3 − 2 = 1. Option (b) confuses the ambient dimensions n = 4 and m = 3 with the rank; option (c) swaps the roles of n and m in the two null spaces, which is exactly the trap — the null space of A lives in R⁴ while the null space of A^T lives in R³.
> **Key point:** dim row = dim col = rank = 2; dim N(A) = n − rank = 2; dim N(A^T) = m − rank = 1.

### Q92. Give a basis of the row space and a basis of the column space of A = [[1,2],[2,4]].

> **Type:** Numerical
> **Answer:** Row space = span{(1,2)} (basis {(1,2)}, dim 1); column space = span{(1,2)^T} (basis {(1,2)^T}, dim 1).
> **Solution:** The second row equals twice the first, so the row space is generated by (1,2) alone. The columns are (1,2)^T and (2,4)^T = 2(1,2)^T, so the column space is the same line, generated by (1,2)^T. Note that for a non-square matrix the row space (in R^n) and column space (in R^m) are subsets of different ambient spaces and cannot be compared at all.
> **Key point:** Row and column spaces of a square matrix are parallel constructions but live in R^n vs R^m; here both are 1-dimensional lines.

### Q93. Missing data: given only that A is m × n with rank r, can you determine dim N(A)? What else would you need?

> **Type:** Missing-data
> **Answer:** Yes — dim N(A) = n − r, so the number of rows m is irrelevant.
> **Solution:** Rank–nullity gives dim N(A) + rank A = n, and n is known from the stated order, so dim N(A) = n − r is determined. Conversely, given dim N(A) = d and n, one gets rank A = n − d, again without m. What is *not* determined is dim N(A^T) = m − r, which needs m.
> **Key point:** dim N(A) = n − rank A needs only n; dim N(A^T) = m − rank A needs only m.

---

## Section 6. Eigenvalues and eigenvectors: characteristic equation, multiplicities, properties, diagonalisation, symmetric matrix theorems

### Q94. Define an eigenvalue and an eigenvector of a square matrix A.

> **Type:** Theory
> **Answer:** A scalar λ is an eigenvalue of A if there is a non-zero vector v with Av = λv. Such a non-zero v is an eigenvector of A for λ.
> **Solution:** The word "non-zero" is essential: v = 0 satisfies Av = λv for every λ and would make every λ an eigenvalue. Rearranging, Av − λv = 0 or (A − λI)v = 0; this homogeneous system has a non-trivial solution precisely when A − λI is singular, i.e. det(A − λI) = 0. Hence the eigenvalues are exactly the roots of the characteristic equation, and the eigenvectors for a given λ are the non-zero vectors of its null space (the eigenspace).
> **Key point:** λ is an eigenvalue ⟺ det(A − λI) = 0; eigenvectors form the null space of A − λI.

### Q95. How does one compute all eigenvalues of an n × n matrix, and how many are there?

> **Type:** Application
> **Answer:** Solve det(A − λI) = 0. Being a polynomial of degree n in λ, this equation has exactly n roots counted with multiplicity (over ℂ), so A has n eigenvalues over ℂ counted with algebraic multiplicity; real matrices may have fewer real roots, the rest being complex.
> **Solution:** det(A − λI) is the *characteristic polynomial* of A, and det(λI − A) = (−1)^n det(A − λI) differs only in overall sign. For a triangular matrix the characteristic polynomial factors immediately into (λ − a₁₁)…(λ − a_nn), so the eigenvalues are just the diagonal entries. Eigenvalues are roots of a polynomial, so they cannot generally be written in closed form beyond degree 4 — which is why numerical methods (QR, Jacobi) are used in practice (Section 8).
> **Key point:** n eigenvalues over ℂ counted with multiplicity; triangular ⇒ eigenvalues = diagonal entries.

### Q96. Find the eigenvalues and eigenvectors of A = [[4,1],[2,3]].

> **Type:** Numerical
> **Answer:** Eigenvalues 5 and 2. For λ = 5 the eigenvectors are all multiples of (1,1)^T; for λ = 2 all multiples of (1,−2)^T.
> **Solution:** det(A − λI) = (4 − λ)(3 − λ) − 2 = λ² − 7λ + 10 = (λ − 5)(λ − 2). For λ = 5: A − 5I = [[−1,1],[2,−2]], so −x + y = 0, giving v = c(1,1). For λ = 2: A − 2I = [[2,1],[2,1]], so 2x + y = 0, giving v = c(1,−2). Check: A(1,1) = (5,5) = 5(1,1) ✓ and A(1,−2) = (2,−4) = 2(1,−2) ✓.
> **Key point:** λ = 5 → (1,1); λ = 2 → (1,−2); eigenvectors come from null spaces of A − λI.

### Q97. `GATE-1`. Can a real matrix have non-real eigenvalues?

> (a) No — eigenvalues of a real matrix are always real
> (b) Yes — but then they occur in conjugate pairs, so a 2 × 2 real matrix can have them
> (c) Yes — any real matrix may have complex eigenvalues without restriction
> (d) No — only if the matrix is complex

> **Type:** MCQ `GATE-1`
> **Answer:** (b) Yes — but they occur in complex-conjugate pairs (Option b).
> **Solution:** det(A − λI) is a real polynomial, so non-real roots come in conjugate pairs. Example: A = [[0,−1],[1,0]] has characteristic polynomial λ² + 1, hence eigenvalues ±j. Option (a) is only true for symmetric (and skew-symmetric/Hermitian) matrices, not for all real ones. Option (c) ignores the pairing constraint and would wrongly allow a lone complex eigenvalue of a real matrix.
> **Key point:** Non-real eigenvalues of a real matrix occur in conjugate pairs; A = [[0,−1],[1,0]] has λ = ±j.

### Q98. `GATE-2`. The eigenvalues of a 3 × 3 real matrix A are 2, 2 and −1. Which of the following are necessarily true?

> (a) tr A = 3
> (b) det A = −4
> (c) rank A = 3
> (d) A is diagonalisable

> **Type:** MSQ `GATE-2`
> **Answer:** (a), (b) and (c) are true; (d) is false.
> **Solution:** tr A = sum of eigenvalues = 2 + 2 − 1 = 3, so (a) is true. det A = product = 2·2·(−1) = −4, so (b) is true. Since det A = −4 ≠ 0, A is nonsingular and rank A = 3, so (c) is true. Diagonalisability is not guaranteed: the eigenvalue 2 has algebraic multiplicity 2 and could have geometric multiplicity 1, as in the defective block [[2,1],[0,2]] together with the block [−1]. Hence (d) is false.
> **Key point:** Sum/product of eigenvalues always give tr and det, and det ≠ 0 gives full rank; a repeated eigenvalue does **not** guarantee diagonalisability.

### Q99. `GATE-1`. Which matrix is necessarily diagonalisable?

> (a) Any matrix with distinct eigenvalues
> (b) Any symmetric matrix
> (c) Any matrix with all positive eigenvalues
> (d) Any matrix

> **Type:** MCQ `GATE-1`
> **Answer:** Both (a) and (b) are correct — distinct eigenvalues always give n independent eigenvectors, and real symmetric matrices are orthogonally diagonalisable.
> **Solution:** (a) is the spectral theorem's easy direction: eigenvectors belonging to distinct eigenvalues are automatically linearly independent. (b) is the real spectral theorem: a real symmetric A has an orthonormal eigenbasis, so A = QΛQ^T. (c) fails: the defective matrix [[2,1],[0,2]] has both eigenvalues equal to 2 (positive) yet is not diagonalisable. (d) is false for the same counterexample.
> **Key point:** Distinct eigenvalues ⇒ diagonalisable; real symmetric ⇒ orthogonally diagonalisable. Positive eigenvalues alone do not suffice.

### Q100. State the two spectral identities linking eigenvalues to trace and determinant, and verify on A = [[4,1],[2,3]].

> **Type:** Numerical
> **Answer:** Σλᵢ = tr A and Πλᵢ = det A. For A = [[4,1],[2,3]]: eigenvalues 5 and 2, so 5 + 2 = 7 = tr A ✓ and 5·2 = 10 = det A ✓.
> **Solution:** The two statements are general (sum and product of eigenvalues, counted with algebraic multiplicity, equal trace and determinant). They hold for triangular matrices trivially and in general because the characteristic polynomial det(λI − A) = λ^n − (tr A)λ^(n−1) + … + (−1)^n det A, whose coefficients are the elementary symmetric functions of the eigenvalues. They are the practical way to recover tr A and det A from a spectrum.
> **Key point:** Σλᵢ = tr A, Πλᵢ = det A (multiplicities counted).

### Q101. Distinguish algebraic multiplicity from geometric multiplicity.

> **Type:** Theory
> **Answer:** The algebraic multiplicity (AM) of λ is its multiplicity as a root of the characteristic polynomial; the geometric multiplicity (GM) is dim N(A − λI), the number of linearly independent eigenvectors for λ. Always GM ≤ AM, and equality holds for every λ of every diagonalisable matrix.
> **Solution:** AM counts how many times det(A − λI) vanishes; GM counts the dimension of the solution space of (A − λI)v = 0, which by rank–nullity is n − rank(A − λI). A matrix is diagonalisable iff GM = AM for every eigenvalue, equivalently iff it has n linearly independent eigenvectors. For the Jordan block [[2,1],[0,2]] the root λ = 2 has AM = 2 (the characteristic polynomial is (λ − 2)²) and GM = 1, since the null space of [[0,1],[0,0]] is one-dimensional.
> **Key point:** AM ≥ GM always; diagonalisable ⟺ AM = GM for all λ. Jordan block: AM 2, GM 1.

### Q102. `GATE-2`. For A = [[2,1],[0,2]], what are the algebraic and geometric multiplicities of λ = 2, and is A diagonalisable?

> (a) AM = 1, GM = 1, diagonalisable
> (b) AM = 2, GM = 1, not diagonalisable
> (c) AM = 2, GM = 2, diagonalisable
> (d) AM = 1, GM = 2, not diagonalisable

> **Type:** MCQ `GATE-2`
> **Answer:** (b) AM = 2, GM = 1, not diagonalisable (Option b).
> **Solution:** det(A − λI) = (2 − λ)² so λ = 2 is a double root, AM = 2. The eigenvectors satisfy [[0,1],[0,0]](x,y) = (y, 0) = 0, so y = 0 and x is free: the eigenspace is one-dimensional, GM = 1. Since GM < AM, A has fewer than n = 2 independent eigenvectors and cannot be diagonalised. This is the standard defective (Jordan) block.
> **Key point:** [[2,1],[0,2]]: (λ−2)² ⇒ AM = 2; eigenspace {(x,0)} ⇒ GM = 1 ⇒ defective.

### Q103. State the diagonalisation condition and write the diagonalisation explicitly.

> **Type:** Theory
> **Answer:** A is diagonalisable iff it has n linearly independent eigenvectors. If v₁, …, v_n are those eigenvectors, then with P = [v₁ … v_n] and Λ = diag(λ₁, …, λ_n) one has P^{-1} A P = Λ, or A = PΛP^{-1}.
> **Solution:** The columns of P are eigenvectors, so A P = P Λ (column j of AP is Av_j = λ_j v_j); multiplying on the left by P^{-1} gives the diagonal form. Since P is invertible exactly when its columns are independent, diagonalisability is equivalent to the existence of such a basis. The formula A = PΛP^{-1} is what makes powers easy: A^k = PΛ^k P^{-1}, so eigenvalues of A^k are λ_i^k.
> **Key point:** A = PΛP^{-1} with P's columns = independent eigenvectors; then A^k = PΛ^k P^{-1}.

### Q104. Diagonalise A = [[4,1],[2,3]] and verify the result.

> **Type:** Numerical
> **Answer:** With P = [[1,1],[1,−2]] and Λ = diag(5,2), we get P^{-1}AP = Λ, since P^{-1} = [[2/3,1/3],[1/3,−1/3]].
> **Solution:** From Q96 the eigenvectors are v₁ = (1,1)^T for λ = 5 and v₂ = (1,−2)^T for λ = 2, so P = [[1,1],[1,−2]] with det P = −3 ≠ 0, and P^{-1} = (1/−3)[[−2,−1],[−1,1]] = [[2/3,1/3],[1/3,−1/3]]. Multiplying, AP = [[5,2],[5,−4]] and P^{-1}AP = [[2/3,1/3],[1/3,−1/3]]·[[5,2],[5,−4]] = [[5,0],[0,2]] ✓. The diagonal entries are the eigenvalues, in the order the eigenvectors were placed as columns.
> **Key point:** P^{-1}AP = diag(5,2) with P = [[1,1],[1,−2]]; check the diagonal is exactly the eigenvalue list.

### Q105. Compare the diagonalisability of a symmetric matrix and a skew-symmetric matrix.

> **Type:** Comparison
> **Answer:** A real symmetric matrix is orthogonally diagonalisable with **real** eigenvalues. A real skew-symmetric matrix is normal and diagonalisable over ℂ (by a unitary matrix) with **purely imaginary** eigenvalues 0, ±jω₁, ±jω₂, …, so an odd-order skew-symmetric matrix cannot be diagonalised over ℝ at all.
> **Solution:** Symmetry gives real eigenvalues and an orthonormal eigenbasis, hence P^{-1}AP = P^TAP = Λ over ℝ. For skew-symmetry, if Av = λv then (Av)^T = −v^T A = λ v^T, so v^T Av = λ‖v‖² while also = −(Av)^T v = −λ̄‖v‖², forcing λ = −λ̄, i.e. Re λ = 0. Since the eigenvalues of an odd-order real matrix include a real one, that one must be 0.
> **Key point:** Symmetric ⇒ real eigenvalues + orthogonal diagonalisation; skew ⇒ purely imaginary eigenvalues, so odd order forces a zero eigenvalue.

### Q106. `GATE-1`. What are the eigenvalues of a real skew-symmetric 3 × 3 matrix?

> (a) Three real numbers whose sum is zero
> (b) 0, +jω and −jω for some real ω
> (c) Three purely imaginary numbers
> (d) Only zero

> **Type:** MCQ `GATE-1`
> **Answer:** (b) 0, +jω, −jω (Option b).
> **Solution:** Skew-symmetry forces purely imaginary eigenvalues occurring in conjugate pairs (Q105), and an odd order forces at least one real eigenvalue, which must then be 0. Option (c) ignores the forced zero and violates the conjugate-pair structure for odd order. Option (a) contradicts the imaginary requirement. Option (d) is only the degenerate case ω = 0. Example: [[0,2,−1],[−2,0,3],[1,−3,0]] has eigenvalues 0, ±j√14.
> **Key point:** Odd-order real skew-symmetric spectrum = {0, ±jω₁, …}: always a forced zero eigenvalue.

### Q107. Compare the eigenvalues of AB and BA, and of A and A^T.

> **Type:** Comparison
> **Answer:** For square A and B of the same order, AB and BA have the **same** characteristic polynomial, hence the same eigenvalues with multiplicity. A and A^T also have the same eigenvalues.
> **Solution:** Sylvester's identity det(I + PQ) = det(I + QP) gives, with λ ≠ 0, det(AB − λI) = det(λ(I − AB/λ)) = λ^n det(I − AB/λ) = λ^n det(I − BA/λ) = det(BA − λI); since both sides are polynomials in λ, the equality extends to λ = 0 as well. For the transpose, det(A − λI) = det((A − λI)^T) = det(A^T − λI), because a matrix and its transpose have the same determinant. Note that eigenvectors differ even though the spectra agree: if Av = λv then A^T v need not be λv.
> **Key point:** spectra of AB, BA, A and A^T coincide; eigenvectors need not.

### Q108. `GATE-2`. Let A be 3 × 3 with eigenvalues 2, 2 and −1. What is the rank of A, and what can you say about tr(A^T A)?

> (a) rank A = 3 and tr(A^T A) = 9
> (b) rank A = 2 and tr(A^T A) ≥ 9
> (c) rank A = 3 and tr(A^T A) = 5
> (d) rank A ≤ 2 and tr(A^T A) = 9

> **Type:** MCQ `GATE-2`
> **Answer:** (a) rank A = 3 and tr(A^T A) = 9 (Option a).
> **Solution:** det A = 2·2·(−1) = −4 ≠ 0, so A is nonsingular and rank A = 3. Since A^T has the same eigenvalues, tr(A^T A) is the sum of the squares of the eigenvalues of A^T A, whose eigenvalues are λᵢ² = 4, 4, 1, giving 9. Equivalently tr(A^T A) = ΣΣ a_ij² ≥ Σλᵢ² = 9, with equality iff A is normal (diagonalisable unitarily).
> **Key point:** det A = −4 ≠ 0 ⇒ rank 3; tr(A^T A) = Σλᵢ² = 9 for normal A.

### Q109. `GATE-1`. What are the eigenvalues of A² if the eigenvalues of A are 1, −2 and 3?

> (a) 1, −2, 3
> (b) 1, 4, 9
> (c) 1, −4, 9
> (d) 2, −4, 6

> **Type:** MCQ `GATE-1`
> **Answer:** (b) 1, 4, 9 (Option b).
> **Solution:** If Av = λv then A²v = λ(Av) = λ²v, so the eigenvalues of A² are λᵢ² = 1, 4, 9. The trap in (c) is keeping the sign of −2, forgetting that squaring a negative eigenvalue gives a positive one; note also that if A is *not* diagonalisable, A² may have fewer distinct eigenvalues than the number of λᵢ² values, but the multiset of eigenvalues of A² is still {λᵢ²} counted with multiplicity.
> **Key point:** Eigenvalues of A^k are λᵢ^k — so sign errors vanish: (−2)² = 4.

### Q110. `GATE-2`. If A is an n × n matrix, relate the eigenvalues of A + 3I to those of A.

> (a) They are λᵢ + 3
> (b) They are 3λᵢ
> (c) They are λᵢ/3
> (d) They are λᵢ³

> **Type:** MCQ `GATE-2`
> **Answer:** (a) They are λᵢ + 3 (Option a).
> **Solution:** (A + 3I)v = Av + 3v = λv + 3v = (λ + 3)v, so each eigenvector is preserved and the eigenvalue shifts by 3. Equivalently det(A + 3I − λI) = det(A − (λ − 3)I), whose roots are λ = λᵢ + 3. This also shows tr(A + 3I) = tr A + 3n and det(A + 3I) = Π(λᵢ + 3) — the latter useful for checking.
> **Key point:** A + cI shifts every eigenvalue by c; eigenvectors unchanged.

### Q111. `GATE-2`. Let A = [[4,1],[2,3]] with eigenvalues 5 and 2. Which statements about A^{-1} are true?

> (a) A^{-1} has eigenvalues 1/5 and 1/2
> (b) A^{-1} has eigenvalues 5 and 2
> (c) A^{-1} is diagonalisable in the same eigenbasis as A
> (d) tr A^{-1} = 7

> **Type:** MSQ `GATE-2`
> **Answer:** (a) and (c).
> **Solution:** From Av = λv, multiply by A^{-1}: v = λ A^{-1}v, so A^{-1}v = (1/λ)v — giving (a), and the *same* eigenvectors diagonalise A^{-1}, giving (c). Option (b) is the trap of forgetting the inversion. Option (d): tr A^{-1} = 1/5 + 1/2 = 7/10 ≈ 0.7, not 7. Note the requirement λ ≠ 0 — A must be nonsingular for A^{-1} to exist.
> **Key point:** Eigenvalues of A^{-1} are 1/λᵢ, same eigenvectors, same eigenbasis.

### Q112. What does it mean for an eigenvalue to be repeated, and can you tell diagonalisability from the eigenvalue list alone?

> **Type:** Conceptual
> **Answer:** An eigenvalue repeated in the characteristic polynomial has algebraic multiplicity > 1. No — the list alone is insufficient: a repeated eigenvalue may or may not be defective. E.g. λ = 2 appears twice for both the diagonalisable I₂ and the defective [[2,1],[0,2]].
> **Solution:** I₂ has characteristic polynomial (λ − 2)² with AM = 2 and GM = 2, so it is diagonalisable; [[2,1],[0,2]] has the same characteristic polynomial but GM = 1, so it is not. The deciding information is the dimension of the eigenspace, which the eigenvalue list does not contain. That is why the count of *distinct* eigenvalues being less than n is not, by itself, proof of non-diagonalisability (e.g. I₂) — it is only proof when some AM exceeds GM.
> **Key point:** Same characteristic polynomial can give diagonalisable (I₂) or defective ([[2,1],[0,2]]) matrices.

### Q113. `GATE-2`. How many linearly independent eigenvectors does a matrix with n distinct eigenvalues have?

> (a) 1
> (b) At most n
> (c) Exactly n
> (d) Exactly 1 per distinct eigenvalue, so 1 in total

> **Type:** MCQ `GATE-2`
> **Answer:** (c) Exactly n (Option c).
> **Solution:** Eigenvectors belonging to **distinct** eigenvalues are linearly independent — this is proved by assuming Σ cᵢvᵢ = 0, applying A − λ₁I and using that all other terms survive with non-zero factors (λᵢ − λ₁), forcing c₂ = … = c_n = 0, then c₁ = 0. With n distinct eigenvalues in R^n this gives a full eigenbasis, hence diagonalisability (Q99). Note the qualification "distinct": repeated eigenvalues do not guarantee independence.
> **Key point:** Eigenvectors for distinct eigenvalues are automatically independent ⇒ n distinct eigenvalues ⇒ diagonalisable.

### Q114. `GATE-1`. A 2 × 2 real matrix has characteristic polynomial λ² + 1. What are its eigenvalues and can it be diagonalised over the reals?

> (a) λ = ±1, and it can be diagonalised over ℝ
> (b) λ = ±j, and it cannot be diagonalised over ℝ
> (c) λ = ±j, and it can be diagonalised over ℝ
> (d) λ = 0 with multiplicity 2

> **Type:** MCQ `GATE-1`
> **Answer:** (b) λ = ±j, and it cannot be diagonalised over ℝ (Option b).
> **Solution:** The roots of λ² + 1 = 0 are λ = ±j. Over ℝ a real diagonal matrix has only real diagonal entries, so no real P can satisfy P^{-1}AP = diag(j, −j); the best possible is the real block form (a rotation block). Example: A = [[0,−1],[1,0]] has exactly this characteristic polynomial. Over ℂ the same matrix is diagonalisable since the two eigenvalues are distinct.
> **Key point:** Complex eigenvalues ⇒ diagonalisable over ℂ only; real canonical form uses 2 × 2 rotation blocks.

### Q115. Show that A = [[1,2],[2,3]] has eigenvalues 2 ± √5 and comment on their signs.

> **Type:** Numerical
> **Answer:** The eigenvalues are 2 + √5 ≈ 4.236 and 2 − √5 ≈ −0.236; the matrix is symmetric but **indefinite** (one positive and one negative eigenvalue).
> **Solution:** det(A − λI) = (1 − λ)(3 − λ) − 4 = 3 − 4λ + λ² − 4 = λ² − 4λ − 1, whose roots are λ = (4 ± √(16 + 4))/2 = (4 ± √20)/2 = 2 ± √5. Check with the spectral identities: sum = 4 = tr A ✓, product = 4 − 5 = −1 = det A ✓. Symmetry guarantees real eigenvalues, not positivity; since det A = −1 < 0 the two eigenvalues have opposite signs.
> **Key point:** Symmetric ⇒ real eigenvalues; det < 0 ⇒ one positive, one negative (indefinite).

### Q116. `GATE-1`. If A is a real matrix with all eigenvalues real, must A be symmetric?

> (a) Yes — real eigenvalues imply symmetry
> (b) Yes — real eigenvalues imply normality and hence symmetry
> (c) No — the upper-triangular matrix [[1,1],[0,2]] has eigenvalues 1, 2 but is not symmetric
> (d) No — but only for matrices of order greater than 2

> **Type:** MCQ `GATE-1`
> **Answer:** (c) No — [[1,1],[0,2]] has real eigenvalues 1 and 2 but is not symmetric (Option c).
> **Solution:** A matrix is triangular ⇔ all its eigenvalues are real (the characteristic polynomial splits into linear factors), and triangular matrices need not be symmetric. Being symmetric is a *sufficient* condition for real eigenvalues, not a necessary one. Option (b) mixes up two different notions — normality (A^T A = AA^T, which gives a unitary diagonalisation) does not force symmetry.
> **Key point:** Real eigenvalues ⇏ symmetric. All real eigenvalues ⇔ triangularisable over ℝ.

### Q117. Give an eigenvalue/vector pair for the rotation matrix R = [[0,−1],[1,0]] and explain the geometric meaning.

> **Type:** Application
> **Answer:** λ = j with v = (1, j)^T and λ = −j with v = (1, −j)^T (up to scaling).
> **Solution:** Rv = λv reads −y = λx, x = λy. Substituting y = x/λ gives −x/λ = λx, so λ² = −1, λ = ±j. With λ = j, y = x/j = −jx, so v = (1, −j)^T. Geometrically, R is a rotation by 90° and j = e^{jπ/2}; the general rotation by angle θ has eigenvalues e^{±jθ}. A rotation is normal and unitary, so it is diagonalisable over ℂ but never over ℝ.
> **Key point:** Rotation by θ has eigenvalues e^{±jθ}; R(90°) gives λ = ±j.

### Q118. `GATE-2`. A real 4 × 4 matrix has eigenvalues 1, 1, 1, 1. What are its eigenvalues as a matrix, and is it necessarily I?

> (a) A has four real eigenvalues and must equal I
> (b) A has all eigenvalues equal to 1, so A = I + N for some nilpotent N, which need not be zero
> (c) A must be rank 4 or 0
> (d) A cannot be diagonalised

> **Type:** MCQ `GATE-2`
> **Answer:** (b).
> **Solution:** With all eigenvalues equal to 1, det(A − I) = 0 and every root of the characteristic polynomial is 1, so A − I is nilpotent (its characteristic polynomial is λ^n). The matrix need not be I: A = [[1,1,0],[0,1,0],[0,0,1]] has all eigenvalues 1 and is diagonalisable, while the Jordan form shows non-diagonalisable cases exist as well. So (a) is false, (c) is false (rank = 4 always, since det = 1 ≠ 0), and (d) is false in general.
> **Key point:** All eigenvalues equal to 1 ⇒ A = I + N with N nilpotent; A need not be I and may or may not be diagonalisable.

### Q119. `GATE-1`. What does det(A) ≠ 0 tell you about the eigenvalues of A?

> (a) All eigenvalues are non-zero
> (b) All eigenvalues are positive
> (c) At least one eigenvalue is non-zero
> (d) A is diagonalisable

> **Type:** MCQ `GATE-1`
> **Answer:** (a) All eigenvalues are non-zero (Option a).
> **Solution:** det A is the product of the eigenvalues, so a non-zero product forces every factor to be non-zero. Positivity is not implied (det can be negative, as for [[1,2],[2,3]] with eigenvalues 2 ± √5 of opposite signs). Diagonalisability is a separate matter — [[2,1],[0,2]] has eigenvalues 2, 2, both non-zero, yet is not diagonalisable.
> **Key point:** det A ≠ 0 ⇔ no zero eigenvalue ⇔ 0 is not in the spectrum.

### Q120. `GATE-2`. Which of these matrices can be diagonalised over ℝ? A = [[0,−1],[1,0]], B = [[1,1],[0,1]], C = [[2,0],[0,3]], D = [[1,2],[2,1]].

> (a) A only
> (b) B and C only
> (c) B, C and D only
> (d) A, B, C and D

> **Type:** MCQ `GATE-2`
> **Answer:** (c) B, C and D only (Option c).
> **Solution:** A = [[0,−1],[1,0]] has eigenvalues ±j, so it cannot be diagonalised over ℝ. B = [[1,1],[0,1]] has characteristic polynomial (λ − 1)² but only one independent eigenvector — the null space of B − I = [[0,1],[0,0]] is spanned by (1,0) — so B is defective and not diagonalisable. C = [[2,0],[0,3]] is already diagonal. D = [[1,2],[2,1]] is symmetric, since d₁₂ = d₂₁ = 2, with distinct eigenvalues 3 and −1, hence diagonalisable. So C and D succeed, A and B fail.
> **Key point:** A: complex eigenvalues (no over ℝ); B: defective; C: already diagonal; D: symmetric ⇒ yes.

### Q121. `GATE-2`. If A and B are n × n and share a common eigenvector v with Av = λv and Bv = μv (λ ≠ μ), what can you conclude?

> (a) A and B commute
> (b) v is an eigenvector of AB with eigenvalue λμ
> (c) λ = μ necessarily
> (d) A and B are simultaneously diagonalisable

> **Type:** MSQ `GATE-2`
> **Answer:** (b) only.
> **Solution:** (b) is immediate: ABv = A(μv) = μAv = μλv, so v is an eigenvector of AB with eigenvalue λμ. (a) does not follow: a single shared eigenvector imposes one scalar relation and cannot force AB = BA on the rest of the space. (d) requires a *full* common eigenbasis (or commutation plus normality/symmetry of both matrices), not one shared vector. (c) contradicts the hypothesis λ ≠ μ.
> **Key point:** A shared eigenvector gives an eigenvector of AB with eigenvalue λμ; commutation and simultaneous diagonalisation need a full common eigenbasis.

### Q122. What are the eigenvalues of a 2 × 2 matrix A = [[a,b],[c,d]] in terms of its entries, and what do they tell you about diagonalisability?

> **Type:** Application
> **Answer:** λ = (a + d)/2 ± sqrt(((a − d)/2)² + bc). If sqrt(((a−d)/2)² + bc) ≠ 0 the eigenvalues are distinct and A is diagonalisable over ℂ; if it is 0, there is a repeated eigenvalue λ = (a+d)/2 and diagonalisability must be checked from rank(A − λI).
> **Solution:** The characteristic polynomial is λ² − (a+d)λ + (ad − bc), solved by the quadratic formula. The discriminant (a − d)² + 4bc decides distinctness; writing it as 4[((a−d)/2)² + bc] gives the form above. For a real matrix, a negative quantity inside the sqrt gives complex conjugate eigenvalues; zero gives the repeated case where the geometric multiplicity may be 1 (e.g. [[2,1],[0,2]] has ((2−2)/2)² + 0 = 0).
> **Key point:** λ = (tr A)/2 ± sqrt((tr A)²/4 − det A); repeated root ⇒ check rank(A − λI).

---

## Section 7. Cayley–Hamilton and its applications, minimal polynomial, positive definite matrices, quadratic forms and Sylvester's criterion

### Q123. State the Cayley–Hamilton theorem and its main consequence.

> **Type:** Theory
> **Answer:** Every square matrix satisfies its own characteristic equation: p(A) = 0, where p(λ) = det(λI − A). Its main consequence is that A^n can always be reduced to a linear combination of I, A, …, A^(n−1), so no matrix power ever needs to be computed by brute force.
> **Solution:** Writing p(λ) = λ^n + c_(n−1)λ^(n−1) + … + c₁λ + c₀, substitution of λI for A gives A^n + c_(n−1)A^(n−1) + … + c₁A + c₀I = 0, so A^n = −(c_(n−1)A^(n−1) + … + c₁A + c₀I). The theorem is easy to believe because the characteristic polynomial's coefficients are the elementary symmetric functions of the eigenvalues: substituting each eigenvalue λᵢ into p gives p(λᵢ) = 0. The matrix version is subtler (the polynomial must vanish as a *matrix*, not just on the spectrum) but is nevertheless true.
> **Key point:** p(A) = 0 with p the characteristic polynomial; hence every power reduces to degree < n.

### Q124. `GATE-1`. Use Cayley–Hamilton to compute A² for A = [[2,1],[1,3]] without multiplying.

> (a) [[5,5],[5,10]]
> (b) [[5,4],[4,10]]
> (c) [[5,1],[1,3]]
> (d) [[4,2],[2,9]]

> **Type:** MCQ `GATE-1`
> **Answer:** (a) [[5,5],[5,10]] (Option a).
> **Solution:** p(λ) = det(λI − A) = (λ − 2)(λ − 3) − 1 = λ² − 5λ + 5, so Cayley–Hamilton gives A² − 5A + 5I = 0, i.e. A² = 5A − 5I = 5[[2,1],[1,3]] − 5[[1,0],[0,1]] = [[10,5],[5,15]] − [[5,0],[0,5]] = [[5,5],[5,10]]. Option (b) is the result of a mis-expansion of the constant term.
> **Key point:** A² − 5A + 5I = 0 ⇒ A² = 5A − 5I = [[5,5],[5,10]].

### Q125. Using A² = 5A − 5I, compute A³, A⁴ and A⁵ for A = [[2,1],[1,3]].

> **Type:** Numerical
> **Answer:** A³ = [[15,20],[20,35]], A⁴ = [[50,75],[75,125]], A⁵ = [[175,275],[275,450]].
> **Solution:** Multiply the reduction by A and collect: A³ = 5A² − 5A = 5(5A − 5I) − 5A = 20A − 25I = [[40,20],[20,60]] − [[25,0],[0,25]] = [[15,20],[20,35]]. Then A⁴ = 20A² − 25A = 20(5A − 5I) − 25A = 75A − 100I = [[50,75],[75,125]], and A⁵ = 75A² − 100A = 75(5A − 5I) − 100A = 275A − 375I = [[175,275],[275,450]]. Every step produced coefficients of I, A only — the whole tower of powers stays in the two-dimensional span of I and A.
> **Key point:** A^k = aₖA + bₖI with aₖ, bₖ following a scalar recurrence: aₖ = 5a_(k−1) + b_(k−1), bₖ = −5a_(k−1).

### Q126. `GATE-2`. Compute tr(A^n) recursively for A = [[2,1],[1,3]] starting from tr A = 5.

> (a) tₙ = 5tₙ₋₁ − 5tₙ₋₂
> (b) tₙ = 5tₙ₋₁ + 5tₙ₋₂
> (c) tₙ = tₙ₋₁ + tₙ₋₂
> (d) tₙ = 25tₙ₋₁

> **Type:** MCQ `GATE-2`
> **Answer:** (a) tₙ = 5tₙ₋₁ − 5tₙ₋₂ (Option a).
> **Solution:** From A^n = 5A^(n−1) − 5A^(n−2), taking traces and using linearity gives tₙ = 5tₙ₋₁ − 5tₙ₋₂, with seeds t₁ = 5 and t₀ = tr I = n = 2. This gives t₂ = 25 − 10 = 15, t₃ = 75 − 25 = 50, t₄ = 250 − 75 = 175, t₅ = 875 − 250 = 625 — all matching tr of the matrices in Q125 (5, 15, 50, 175, and 175 + 450 = 625).
> **Key point:** Cayley–Hamilton converts matrix powers into a scalar linear recurrence: tₙ = 5tₙ₋₁ − 5tₙ₋₂.

### Q127. `GATE-2`. Use Cayley–Hamilton to find A⁻¹ for A = [[2,1],[1,3]].

> (a) [[3/5,−1/5],[−1/5,2/5]]
> (b) [[2/5,1/5],[1/5,3/5]]
> (c) [[3,−1],[−1,2]]
> (d) [[1/2,1],[1,1/3]]

> **Type:** MCQ `GATE-2`
> **Answer:** (a) [[3/5,−1/5],[−1/5,2/5]] (Option a).
> **Solution:** p(λ) = λ² − 5λ + 5 gives A² − 5A + 5I = 0. Factor the scalar identity λ² − 5λ + 5 = λ(λ − 5) + 5: A(A − 5I) = −5I, so A · ((5I − A)/5) = I, hence A⁻¹ = (5I − A)/5 = (5I − [[2,1],[1,3]])/5 = [[3,−1],[−1,2]]/5. Option (c) is 5A⁻¹, a common slip from forgetting the division; option (d) is elementwise inversion.
> **Key point:** From p(A) = 0 with p(0) ≠ 0: A⁻¹ = −(c₁A + … + c_(n−1)A^(n−1))/c₀.

### Q128. State the general Cayley–Hamilton formula for A⁻¹.

> **Type:** Theory
> **Answer:** If p(λ) = λ^n + c_(n−1)λ^(n−1) + … + c₁λ + c₀ with p(0) = c₀ ≠ 0, then A⁻¹ = −(c₁A + c₂A² + … + c_(n−1)A^(n−1))/c₀ = (A^(n−1) + c_(n−1)A^(n−2) + … + c₁)/|c₀| in the det A = ±1 case.
> **Solution:** Rewrite p(A) = 0 as (A⁻¹A^(n) + c_(n−1)A⁻¹A^(n−1) + … + c₁A⁻¹A + c₀A⁻¹) = 0, i.e. A^(n−1) + c_(n−1)A^(n−2) + … + c₁I = −c₀A⁻¹, which is the stated formula after dividing. The requirement c₀ ≠ 0 is exactly det A ≠ 0 — if the constant term vanishes then 0 is an eigenvalue and no inverse exists. The formula is the theoretical route to the adjugate: since A⁻¹ = adj A/det A, comparing terms recovers adj A = c_(n−1)A^(n−2) + … + c₁I.
> **Key point:** p(0) ≠ 0 needed; adj A = c_(n−1)A^(n−2) + … + c₁I.

### Q129. Verify the Cayley–Hamilton identity for the diagonal matrix C = diag(1,2,3).

> **Type:** Numerical
> **Answer:** p(λ) = λ³ − 6λ² + 11λ − 6, and C³ − 6C² + 11C − 6I = 0 (the zero matrix).
> **Solution:** For a diagonal matrix the characteristic polynomial is the product of the diagonal factors: (λ − 1)(λ − 2)(λ − 3) = λ³ − 6λ² + 11λ − 6. Substituting C: C³ = diag(1, 8, 27), 6C² = diag(6, 24, 54), 11C = diag(11, 22, 33), 6I = diag(6, 6, 6). Then diag(1 − 6 + 11 − 6, 8 − 24 + 22 − 6, 27 − 54 + 33 − 6) = diag(0, 0, 0) = 0. This is exactly the "p vanishes at each eigenvalue" argument made rigorous for the diagonal case.
> **Key point:** For diagonal C, p(λ) = Π(λ − cᵢᵢ), and p(C) = 0 because each entry is p(cᵢᵢ) = 0.

### Q130. `GATE-1`. If A satisfies p(A) = 0 for the characteristic polynomial p, what is the significance of eigenvalues of A among the roots of p?

> (a) Every root of p is an eigenvalue and vice versa — they are the same set
> (b) Every root of p is an eigenvalue, but an eigenvalue may fail to be a root
> (c) Only real roots of p are eigenvalues
> (d) Eigenvalues are the roots of the minimal polynomial only, not of p

> **Type:** MCQ `GATE-1`
> **Answer:** (a) (Option a).
> **Solution:** p(λ) = det(λI − A) vanishes exactly when λI − A is singular, i.e. when (A − λI)v = 0 has a non-zero solution — precisely the definition of an eigenvalue. So over ℂ the roots of p and the eigenvalues coincide including multiplicity. Option (c) confuses eigenvalues with real eigenvalues; option (d) is false because the minimal polynomial and the characteristic polynomial have the **same roots** (the minimal polynomial is a divisor of p, Q132).
> **Key point:** Roots of the characteristic polynomial = eigenvalues of A (over ℂ, with multiplicity).

### Q131. Give a worked use of Cayley–Hamilton to find the eigenvalues of a 3 × 3 matrix.

> **Type:** Application
> **Answer:** For any 3 × 3 A, the eigenvalues are the roots of λ³ − (tr A)λ² + (sum of principal 2 × 2 minors)λ − det A = 0, obtained by reading the three coefficients from A.
> **Solution:** p(λ) = det(λI − A) = λ³ − c₂λ² + c₁λ − c₀ with c₂ = tr A, c₁ = sum of the principal minors of order 2, c₀ = det A. For A = [[1,2,3],[4,5,6],[7,8,10]]: tr = 16, det = −3, principal 2 × 2 minors are (1·5 − 2·4) = −3, (1·10 − 3·7) = −11, (5·10 − 6·8) = 2, summing to −12. So p(λ) = λ³ − 16λ² − 12λ + 3, and the eigenvalues are its three roots. Writing the determinant symbolically once is the practical way to avoid coefficient mistakes.
> **Key point:** For 3 × 3: p(λ) = λ³ − (tr A)λ² + (Σ principal 2 × 2 minors)λ − det A.

### Q132. `GATE-2`. How is the minimal polynomial of A related to the characteristic polynomial, and what determines it?

> (a) The minimal polynomial divides the characteristic polynomial and is the product of (λ − λᵢ) over the *distinct* eigenvalues if A is diagonalisable
> (b) The minimal polynomial is always equal to the characteristic polynomial
> (c) The minimal polynomial has degree n always
> (d) The minimal polynomial has no common roots with the characteristic polynomial

> **Type:** MCQ `GATE-2`
> **Answer:** (a) (Option a).
> **Solution:** The minimal polynomial m_A is the monic polynomial of least degree with m_A(A) = 0; since both p_A and m_A annihilate A and m_A has least degree, m_A divides p_A (Euclidean division of p_A by m_A leaves a remainder that also annihilates A, so the remainder is zero). Both have the **same roots** — the distinct eigenvalues — because a root of p_A is an eigenvalue and any annihilating polynomial must vanish on every eigenvalue. For a diagonalisable A, m_A = Π over distinct λ of (λ − λᵢ), each factor to the first power; for a defective matrix larger powers appear: m_A for [[2,1],[0,2]] is (λ − 2)², while p_A = (λ − 2)² as well, and for diag(1,2,3) one has m_A = (λ−1)(λ−2)(λ−3) = p_A.
> **Key point:** m_A | p_A, same roots; exponents in m_A = max Jordan block size for that λ.

### Q133. `GATE-2`. Compare the minimal polynomial of a diagonalisable matrix with one having a nontrivial Jordan block.

> (a) Both equal the characteristic polynomial
> (b) Diagonalisable ⇒ m_A = Π(λ − λᵢ) over distinct λ; defective ⇒ higher powers of (λ − λ) appear
> (c) Defective ⇒ m_A has smaller degree
> (d) Minimal polynomial does not exist for defective matrices

> **Type:** MCQ `GATE-2`
> **Answer:** (b) (Option b).
> **Solution:** In Jordan form, J = diag(J₁, …, J_k) with Jᵢ = λᵢI + Nᵢ; the minimal polynomial of Jᵢ is (λ − λᵢ)^(size of the block), since (Jᵢ − λᵢI) = Nᵢ ≠ 0 but Nᵢ^(size) = 0. So m_A = Π_i (λ − λᵢ)^(largest block size for λᵢ). Diagonalisable means all blocks have size 1, giving exponent 1 and degree = number of distinct eigenvalues. The defective 2 × 2 block [[2,1],[0,2]] has m_A = (λ − 2)². Option (d) is false — a minimal polynomial always exists (the characteristic polynomial itself is a candidate).
> **Key point:** Exponent of (λ − λᵢ) in m_A = size of the largest Jordan block at λᵢ.

### Q134. Define positive definite matrix and give the three equivalent criteria.

> **Type:** Theory
> **Answer:** A real symmetric A is positive definite (PD) iff (i) xᵀAx > 0 for all x ≠ 0, (ii) all eigenvalues are positive, (iii) all leading principal minors are positive (Sylvester's criterion).
> **Solution:** (i) ⇔ (ii): with an orthonormal eigenbasis, xᵀAx = Σλᵢxᵢ², positive for all x ≠ 0 exactly when all λᵢ > 0. (ii) ⇔ (iii): symmetric A admits an LDLᵀ factorisation, and the pivots in D are the ratios D_k/D_(k−1) of leading principal minors, so all D_k > 0 forces positive pivots, hence positive eigenvalues. Symmetry is essential for the equivalence: positive *semi*-definiteness of a general matrix is not testable by principal minors alone.
> **Key point:** PD ⟺ xᵀAx > 0 ∀x≠0 ⟺ λᵢ > 0 ⟺ all leading principal minors > 0 (symmetric A).

### Q135. `GATE-1`. Apply Sylvester's criterion to A = [[4,1],[1,3]].

> (a) Not PD since det = 11
> (b) PD since D₁ = 4 > 0 and D₂ = 11 > 0
> (c) PD only if 4 > 0 and 1 > 0
> (d) Cannot be decided without eigenvalues

> **Type:** MCQ `GATE-1`
> **Answer:** (b) PD since D₁ = 4 > 0 and D₂ = 11 > 0 (Option b).
> **Solution:** A is symmetric with leading principal minors D₁ = 4 and D₂ = det A = 4·3 − 1 = 11. Both positive, so A is positive definite by Sylvester's criterion. Option (c) is a misreading — the criterion needs the leading principal *minors* (determinants), not the off-diagonal entries. Option (a) misuses the determinant: a positive determinant is necessary but not sufficient (e.g. [[−1,0],[0,−1]] has det = 1 > 0 yet is negative definite).
> **Key point:** D₁ = 4, D₂ = 11 > 0 ⇒ A = [[4,1],[1,3]] is positive definite.

### Q136. `GATE-2`. Apply Sylvester's criterion to A = [[4,2,−2],[2,10,2],[−2,2,10]].

> (a) Not PD because a₁₃ < 0
> (b) PD because D₁ = 4, D₂ = 36, D₃ = 288 are all positive
> (c) Not PD because D₂ = 40
> (d) PD only if the matrix is also symmetric

> **Type:** MCQ `GATE-2`
> **Answer:** (b) (Option b).
> **Solution:** The matrix is symmetric (a₁₂ = a₂₁ = 2, a₁₃ = a₃₁ = −2, a₂₃ = a₃₂ = 2). Leading principal minors: D₁ = 4, D₂ = 4·10 − 2² = 36, D₃ = det A = 4(100 − 4) − 2(20 + 4) + (−2)(4 + 20) = 384 − 48 − 48 = 288. All three positive, so A is positive definite. Note that PD is about the quadratic form, so negative off-diagonal entries are perfectly fine; and symmetry is already satisfied here, so option (d) is vacuous.
> **Key point:** D₁ = 4, D₂ = 36, D₃ = 288 all > 0 ⇒ A = [[4,2,−2],[2,10,2],[−2,2,10]] is PD; sign of off-diagonals is irrelevant.

### Q137. `GATE-1`. What is the Cholesky factorisation of the PD matrix A = [[4,2,−2],[2,10,2],[−2,2,10]]?

> (a) L = [[2,0,0],[1,3,0],[−1,1,2√2]]
> (b) L = [[2,0,0],[1,√2,0],[−1,1,3]]
> (c) L = [[2,0,0],[1,2,0],[−1,0,3]]
> (d) L = [[4,0,0],[2,10,0],[−2,2,10]]

> **Type:** MCQ `GATE-1`
> **Answer:** (a) L = [[2,0,0],[1,3,0],[−1,1,2√2]] (Option a).
> **Solution:** Write L = [[l₁₁,0,0],[l₂₁,l₂₂,0],[l₃₁,l₃₂,l₃₃]] with A = LLᵀ. l₁₁ = √4 = 2. l₂₁ = a₂₁/l₁₁ = 2/2 = 1, l₂₂ = √(10 − 1) = 3. l₃₁ = a₃₁/l₁₁ = −2/2 = −1, l₃₂ = (a₃₂ − l₃₁l₂₁)/l₂₂ = (2 + 1)/3 = 1, l₃₃ = √(10 − 1 − 1) = √8 = 2√2. Check: LLᵀ = [[4,2,−2],[2,10,2],[−2,2,10]] ✓. Cholesky exists **iff** A is positive definite, so it doubles as a PD test.
> **Key point:** Cholesky: A = LLᵀ, l_jj = √(a_jj − Σ_{k<j} l_jk²); exists iff A is PD.

### Q138. `GATE-1`. Distinguish positive definite, positive semidefinite, negative definite and indefinite for the quadratic form q(x) = xᵀAx.

> (a) PD: q > 0 for all x ≠ 0; PSD: q ≥ 0 with equality for some x ≠ 0; ND: q < 0 for all x ≠ 0; indefinite: both signs occur
> (b) PD: q ≥ 0; PSD: q > 0
> (c) PD: all leading minors positive; indefinite: det < 0
> (d) All four describe the same property

> **Type:** MCQ `GATE-1`
> **Answer:** (a) (Option a).
> **Solution:** The classification rests on the signs of the eigenvalues of symmetric A. PSD differs from PD by having a zero eigenvalue (so q vanishes on a non-zero vector, e.g. x on the null space of [[1,1],[1,1]]); ND is the negative of PD; indefinite means at least one positive and one negative eigenvalue (e.g. [[1,2],[2,3]] with eigenvalues 2 ± √5). Option (b) swaps the strict and non-strict inequalities — the whole distinction between definite and semidefinite. Option (c) mixes a sufficient test with a symptom.
> **Key point:** PD ⟺ all λ > 0; PSD ⟺ all λ ≥ 0 (some 0); ND ⟺ all λ < 0; indefinite ⟺ mixed signs.

### Q139. `GATE-2`. A symmetric A is positive semidefinite but not positive definite. What must be true?

> (a) det A = 0
> (b) All leading principal minors are positive
> (c) A is singular and some x ≠ 0 has xᵀAx = 0
> (d) A has a negative eigenvalue

> **Type:** MSQ `GATE-2`
> **Answer:** (a) and (c).
> **Solution:** PSD but not PD means all eigenvalues ≥ 0 with at least one equal to 0, so det A = Πλᵢ = 0 — A is singular — and the zero eigenvalue has a non-zero eigenvector v with vᵀAv = 0. Option (b) is false: all leading principal minors positive is exactly the criterion for *positive definiteness* (Sylvester), which is excluded here. Option (d) is false: a negative eigenvalue would make A indefinite, not semidefinite. Note the converse of (a) is not enough: [[−1,0],[0,−1]] has det = 1 but [[1,0],[0,0]] has det = 0 and is PSD; one also needs the non-negativity of all eigenvalues (equivalently all principal minors ≥ 0).
> **Key point:** PSD not PD ⟺ singular with a zero eigenvalue ⟺ some x ≠ 0 has xᵀAx = 0.

### Q140. `GATE-2`. Can a positive semidefinite matrix be tested by Sylvester's criterion?

> (a) Yes — replace ">" by "≥" in the leading principal minors
> (b) Yes — all principal minors ≥ 0 is the criterion
> (c) No — Sylvester's criterion with ">" is for positive definiteness; the "≥" version needs **all** principal minors ≥ 0
> (d) No — PSD cannot be tested at all

> **Type:** MCQ `GATE-2`
> **Answer:** (c) (Option c).
> **Solution:** For positive definiteness, Sylvester needs the **leading** principal minors strictly positive. For semidefiniteness, the leading minors alone are insufficient (a PSD matrix may have a zero leading minor while still being PSD, e.g. diag(0,1) in that order has D₁ = 0, D₂ = 0 yet is PSD — and diag(0,1) does show the leading test fails to be equivalent). The correct criterion is that **all** principal minors (not just leading ones) are ≥ 0. Option (a) is the standard wrong answer: requiring leading D_k ≥ 0 admits indefinite matrices such as [[0,1],[1,0]] whose leading minors are 0, 0 ≥ 0 yet eigenvalues ±1.
> **Key point:** PD: leading minors > 0 (Sylvester). PSD: **all** principal minors ≥ 0 — leading minors alone are not enough.

### Q141. `GATE-1`. Reduce the quadratic form q = x² + 2y² + 3z² + 2xy + 4yz to a sum/difference of squares and classify it.

> (a) q = (x + y)² + y² + 4yz + 3z² — sign: 2 positive, 1 negative (indefinite)
> (b) q = (x + y)² + (y + z)² + z², so q is positive definite
> (c) q = (x + y + z)², so q is a perfect square
> (d) q = (x − y)² + 2(y + z)², so q is positive definite

> **Type:** MCQ `GATE-1`
> **Answer:** (a) q = (x + y)² + y² + 4yz + 3z² — the form is indefinite, with two positive and one negative eigenvalue (Option a).
> **Solution:** Complete the square in x: q = x² + 2xy + 2y² + 4yz + 3z² = (x + y)² + y² + 4yz + 3z². The matrix of the form is M = [[1,1,0],[1,2,2],[0,2,3]] with det M = 1(6 − 4) − 1(3 − 0) + 0 = 2 − 3 = −1 < 0. Since M is symmetric its eigenvalues are real, and their product is negative, so an odd number is negative; tr M = 6 > 0 rules out all three being negative, so exactly one is negative. Numerically the eigenvalues are ≈ 4.669, 1.476, −0.145 — signature (2, 1), so the form is indefinite and options (b) and (d), which claim positive definiteness, are wrong. Option (c) is wrong because (x+y+z)² = x²+y²+z²+2xy+2xz+2yz, which contains an xz term absent from q.
> **Key point:** q = x²+2y²+3z²+2xy+4yz has M = [[1,1,0],[1,2,2],[0,2,3]] with det M = −1 < 0 ⇒ signature (2, 1), indefinite.

### Q142. Reduce q = 3x² + 2y² + z² − 2xy − 2yz to a sum of squares, and identify the matrix of the form.

> **Type:** Application
> **Answer:** q = 2(y − (x + z)/2)² + (5/2)(x − z/5)² + (2/5)z², so q is positive definite. The matrix is M = [[3,−1,0],[−1,2,−1],[0,−1,1]] with det M = 2.
> **Solution:** Completing the square in y first: 2y² − 2xy − 2yz = 2[y² − y(x + z)] = 2(y − (x + z)/2)² − (x + z)²/2, so q = 3x² + z² − (x² + 2xz + z²)/2 = (5/2)x² − xz + (1/2)z². Now (5/2)x² − xz = (5/2)(x − z/5)² − (5/2)(z²/25) = (5/2)(x − z/5)² − z²/10, leaving q = 2(y − (x + z)/2)² + (5/2)(x − z/5)² + (2/5)z². All three coefficients are positive, so q ≥ 0 with equality only at the origin: q is positive definite. This is confirmed by Sylvester: D₁ = 3, D₂ = 3·2 − 1 = 5, D₃ = det M = 3(2·1 − 1) + 1((−1)(1) − 0) = 3 − 1 = 2, all positive.
> **Key point:** q = 3x²+2y²+z²−2xy−2yz = 2(y−(x+z)/2)² + (5/2)(x−z/5)² + (2/5)z²; D₁ = 3, D₂ = 5, D₃ = 2 > 0 ⇒ positive definite.

### Q143. `GATE-2`. What is the signature of the quadratic form with matrix M = [[1,−1,0],[−1,1,−1],[0,−1,1]]?

> (a) (3, 0) — positive definite
> (b) (2, 1) — indefinite
> (c) (1, 2)
> (d) (0, 3) — negative definite

> **Type:** MCQ `GATE-2`
> **Answer:** (b) (2, 1) — indefinite (Option b).
> **Solution:** M = [[1,−1,0],[−1,1,−1],[0,−1,1]] has det M = 1(1·1 − (−1)(−1)) − (−1)((−1)(1) − 0) + 0 = 0 + (−1) = −1. M is symmetric, so its eigenvalues are real; their product is −1 < 0, so an odd number of them is negative. Checking the eigenvalues 1, 1 ± √2 shows exactly one is negative (1 − √2 < 0), the other two being positive. So there are two positive and one negative eigenvalue — signature (2, 1) — and the form is indefinite. Option (a) would require a positive determinant, and the trace here is 3 > 0, ruling out all three eigenvalues being negative.
> **Key point:** M = [[1,−1,0],[−1,1,−1],[0,−1,1]] has eigenvalues 1, 1 ± √2 ⇒ two positive, one negative ⇒ indefinite, signature (2, 1).

### Q144. `GATE-1`. How does a symmetric matrix with orthonormal eigenbasis reduce a quadratic form, and what is the resulting canonical form?

> (a) q = λ₁x₁² + λ₂x₂² + … + λₙxₙ² after the orthogonal change of variables x = Py, where the columns of P are normalised eigenvectors
> (b) q = λ₁x₁² + … only if the matrix is positive definite
> (c) q becomes the identity form always
> (d) The canonical form is the Jordan form

> **Type:** MCQ `GATE-1`
> **Answer:** (a) (Option a).
> **Solution:** Let A = PΛPᵀ with P orthogonal. Then q = xᵀAx = (Py)ᵀPΛPᵀ(Py) = yᵀΛy = Σλᵢyᵢ², so the form loses all cross terms and is expressed purely in the squares of the transformed variables. This diagonal form (the canonical form by orthogonal reduction) keeps the signature and the inertia. Option (b) is false — the reduction works for any symmetric matrix, indefinite included. Option (c) confuses the reduction with normalisation: the diagonal entries are the eigenvalues, not 1. Option (d) confuses symmetric reduction with the Jordan form of a general matrix.
> **Key point:** Orthogonal change x = Py turns q into Σλᵢyᵢ²; the diagonal entries are the eigenvalues (the inertia is preserved).

### Q145. `GATE-2`. Given q = x² + y² + z² − 2xy − 2yz, what does the det of the associated matrix tell you directly?

> (a) q is positive definite
> (b) q is indefinite, since det M = −1 < 0 for a 3 × 3 M
> (c) q is negative definite
> (d) q is positive semidefinite

> **Type:** MCQ `GATE-2`
> **Answer:** (b) q is indefinite, since det M = −1 < 0 (Option b).
> **Solution:** M = [[1,−1,0],[−1,1,−1],[0,−1,1]] with det M = −1. M is symmetric, so its eigenvalues are real; their product is −1 < 0, so an odd number is negative. Direct evaluation of the form is the cleanest confirmation. At x = (1,1,1): q = 1 + 1 + 1 − 2 − 2 = −1 < 0. At x = (0,1,−1): q = 0 + 1 + 1 − 0 + 2 = 4 > 0. Both signs occur, so q is indefinite. Option (a) is false because PD requires all eigenvalues positive and hence a positive determinant; option (d) is false because the positive values exclude semidefiniteness.
> **Key point:** det M = −1 < 0 ⇒ odd number of negative eigenvalues; evaluate q at (1,1,1) = −1 and at (0,1,−1) = 4 to confirm both signs.

### Q146. `GATE-1`. Why does the positive definiteness of a matrix matter in optimisation problems?

> (a) It makes the gradient zero
> (b) It makes the Hessian constant, guaranteeing every critical point is a global minimum
> (c) It makes the gradient non-zero
> (d) It makes the function linear

> **Type:** MCQ `GATE-1`
> **Answer:** (b) (Option b).
> **Solution:** A quadratic form q = xᵀAx with A positive definite is a strictly convex function of x, so it has a unique minimiser (found by ∇q = 0 or the normal equations) and no other local minima, maxima or saddle points. The Hessian of a quadratic function is 2A, which is positive definite and **constant**, so the test "Hessian positive definite" reduces to a one-time check on A. In least-squares problems, A = XᵀX is automatically positive semidefinite and positive definite exactly when X has full column rank, which is why rank-deficiency causes non-uniqueness.
> **Key point:** A PD ⇒ q = xᵀAx strictly convex ⇒ unique global minimum; Hessian 2A is constant.

### Q147. `GATE-2`. For a PD matrix A, which statement about its inverse is true?

> (a) A⁻¹ is symmetric positive definite
> (b) A⁻¹ is symmetric but not positive definite
> (c) A⁻¹ is not guaranteed to be symmetric
> (d) A⁻¹ exists only if det A > 0

> **Type:** MCQ `GATE-2`
> **Answer:** (a) A⁻¹ is symmetric positive definite (Option a).
> **Solution:** (A⁻¹)ᵀ = (Aᵀ)⁻¹ = A⁻¹ since A is symmetric, so the inverse is symmetric. For positivity: if A = LLᵀ is its Cholesky factor, then A⁻¹ = L⁻ᵀL⁻¹ = (L⁻¹)ᵀ(L⁻¹), and for any x ≠ 0, xᵀA⁻¹x = ‖L⁻¹x‖² > 0. Eigenvalues of A⁻¹ are 1/λᵢ, so positive λᵢ give positive inverses. Option (d) misstates the condition: A⁻¹ exists whenever det A ≠ 0, which for PD A is automatic.
> **Key point:** A PD ⇒ A⁻¹ = (L⁻¹)ᵀL⁻¹ is symmetric PD, eigenvalues 1/λᵢ > 0.

### Q148. `GATE-1`. For A = [[4,1],[1,3]], compute A⁻¹ and check A⁻¹A = I.

> (a) A⁻¹ = (1/11)[[3,−1],[−1,4]], and A⁻¹A = I
> (b) A⁻¹ = (1/11)[[4,−1],[−1,3]], and A⁻¹A = I
> (c) A⁻¹ = (1/11)[[3,1],[1,4]], and A⁻¹A = I
> (d) A⁻¹ does not exist since det = 11

> **Type:** MCQ `GATE-1`
> **Answer:** (a) (Option a).
> **Solution:** det A = 4·3 − 1·1 = 11 ≠ 0, and for a 2 × 2 matrix the inverse is (1/det)[[d,−b],[−c,a]] = (1/11)[[3,−1],[−1,4]]. Check: A⁻¹A = (1/11)[[3,−1],[−1,4]]·[[4,1],[1,3]] = (1/11)[[12 − 1, 3 − 3],[−4 + 4, −1 + 12]] = (1/11)[[11,0],[0,11]] = I ✓. Note the adjugate swaps a and d and negates the off-diagonals — the most common error in 2 × 2 inverses.
> **Key point:** A⁻¹ = (1/11)[[3,−1],[−1,4]]; adjugate swaps the diagonal and negates the off-diagonal.

---

## Section 8. Matrix decompositions: LU, LDU, Cholesky, QR, SVD, and the practical role of each

### Q149. What is an LU decomposition, and when does it exist without row exchanges?

> **Type:** Theory
> **Answer:** A = LU with L lower triangular and U upper triangular. It exists with L unit lower triangular whenever A admits Gaussian elimination without row exchanges, i.e. all leading principal minors are non-zero; otherwise one needs PA = LU with a permutation matrix P.
> **Solution:** The decomposition exists because elimination is a sequence of row operations, each of which factors as L (subtracting a multiple of an earlier row) and U (normalising and zeroing). A pivot a_kk = 0 in step k forces a row exchange, which is why the general form is PA = LU. Since det A = det P · det L · det U and det L = 1, we get det A = ±∏u_ii, so the product of U's diagonal gives the determinant — one of the practical reasons LU is so widely used. With L unit lower triangular and U upper triangular, the factorisation is unique when A is nonsingular.
> **Key point:** A = LU (or PA = LU) factors elimination into two triangular pieces; det A = ±∏u_ii.

### Q150. Find the LU decomposition of A = [[2,1],[1,3]].

> **Type:** Numerical
> **Answer:** L = [[1,0],[1/2,1]] and U = [[2,1],[0,5/2]], with L unit lower triangular.
> **Solution:** The multiplier is m₂₁ = a₂₁/a₁₁ = 1/2, so subtract (1/2)·(row 1) from row 2: row 2 becomes (1 − 1, 3 − 1/2) = (0, 5/2). Reading off, U = [[2,1],[0,5/2]] and L collects the multipliers, L = [[1,0],[1/2,1]]. Check: LU = [[1,0],[1/2,1]]·[[2,1],[0,5/2]] = [[2,1],[1, 1/2 + 5/2]] = [[2,1],[1,3]] ✓. Also det A = u₁₁u₂₂ = 2·5/2 = 5 ✓, and solving Ax = b now costs two triangular sweeps instead of a full elimination.
> **Key point:** m₂₁ = 1/2, U = [[2,1],[0,5/2]], L = [[1,0],[1/2,1]]; det A = 2·5/2 = 5.

### Q151. `GATE-2`. Perform the LU decomposition with a row exchange for A = [[0,1,2],[1,0,3],[4,5,6]].

> (a) L = [[1,0,0],[0,1,0],[4,5,1]], U = [[1,0,3],[0,1,2],[0,0,−16]], P swapping rows 1 and 2
> (b) L = [[1,0,0],[1,1,0],[4,5,1]], U = [[0,1,2],[0,−1,1],[0,0,16]]
> (c) L = I, U = A
> (d) No LU decomposition exists because a₁₁ = 0

> **Type:** MCQ `GATE-2`
> **Answer:** (a) (Option a).
> **Solution:** a₁₁ = 0 forces the exchange R₁ ↔ R₂, giving PA = [[1,0,3],[0,1,2],[4,5,6]]. Now eliminate: m₃₁ = 4/1 = 4 and m₃₂ = 5/1 = 5, so row 3 becomes (0, 0, 6 − 4·3 − 5·2) = (0, 0, −16). Hence U = [[1,0,3],[0,1,2],[0,0,−16]] with L = [[1,0,0],[0,1,0],[4,5,1]], and PA = LU reproduces the permuted matrix. Check det A = det P · det U = (−1)(1·1·(−16)) = 16, matching a direct expansion. Option (d) is wrong because the row exchange fixes the zero pivot — that is exactly what P is for.
> **Key point:** Zero pivot ⇒ swap rows first: PA = [[1,0,3],[0,1,2],[4,5,6]] = LU with det A = 16.

### Q152. `GATE-1`. What happens to the LU decomposition when A is singular?

> (a) No LU decomposition exists at all
> (b) The decomposition exists, but U has a zero on its diagonal, signalling singularity
> (c) L becomes singular
> (d) The decomposition becomes non-unique

> **Type:** MCQ `GATE-1`
> **Answer:** (b) The decomposition exists, but U has a zero on its diagonal (Option b).
> **Solution:** Elimination never fails on a singular matrix — it produces a zero row. For A = [[1,2],[2,4]]: m₂₁ = 2, row 2 becomes (0, 0), so U = [[1,2],[0,0]] with L = [[1,0],[2,1]]. A zero on U's diagonal is the signal that A is singular, that A⁻¹ does not exist, and that the elimination-based solve is inconsistent or underdetermined. Option (a) is a common misconception; options (c) and (d) are false since L stays unit lower triangular and the factorisation remains valid.
> **Key point:** Singular A ⇒ LU still exists, but some u_kk = 0 — that zero is the diagnostic.

### Q153. `GATE-2`. What is the LDU decomposition, and what does it reveal about a symmetric matrix?

> (a) A = LDLᵀ with L unit lower triangular and D diagonal; for symmetric A, D's entries are ratios of consecutive leading principal minors
> (b) A = LDU with L unit lower triangular, D diagonal and U unit upper triangular, only for non-symmetric A
> (c) A = LDU exists only if A is invertible
> (d) LDU is another name for the QR decomposition

> **Type:** MCQ `GATE-2`
> **Answer:** (a) (Option a).
> **Solution:** LDU separates the three jobs elimination mixes: unit L holds the multipliers, D holds the pivots, U holds L-transposed. For a symmetric matrix the condition for symmetric LDLᵀ is the same no-pivot condition, and the pivots are d_k = D_k/D_(k−1) where D_k is the k-th leading principal minor — so the leading minors can be read off the decomposition. For A = [[2,1],[1,3]]: D₁ = 2, D₂ = 5, so d₁ = 2 and d₂ = 5/2, with L = [[1,0],[1/2,1]] and A = LDLᵀ. Option (c) is false: the decomposition exists for singular A too, with a zero in D. Option (b) misstates the structure: for symmetric A, LDU forces U = Lᵀ.
> **Key point:** A = LDLᵀ; pivots d_k = D_k/D_(k−1), so the LDLᵀ factors are exactly the Sylvester data.

### Q154. `GATE-1`. When does a Cholesky decomposition A = LLᵀ exist, and what is it used for?

> (a) For any A, and it is used to compute the determinant
> (b) For symmetric positive definite A, and it is used for fast, stable solves and to test positive definiteness
> (c) For triangular A only
> (d) For any square A with det A > 0

> **Type:** MCQ `GATE-1`
> **Answer:** (b) (Option b).
> **Solution:** A = LLᵀ with L lower triangular and positive diagonal exists **iff** A is symmetric positive definite, and the construction only needs the Schur complements of the leading blocks to stay positive. It costs half the arithmetic of LU and is numerically stable, which makes it the standard tool for least-squares and for the Newton/Newton-Raphson step in optimisation. Detecting breakdown (a non-positive pivot) is a certificate that A is not PD, so the same routine tests definiteness. Option (d) is false because det A > 0 does not imply PD — [[−1,0],[0,−1]] has det 1 but is negative definite. Option (a) is false since LU, not Cholesky, is the general-purpose factorisation.
> **Key point:** A = LLᵀ exists iff A is SPD; Cholesky = half the cost of LU, stable, and doubles as a PD test.

### Q155. Given the Cholesky factorisation, how do you solve Ax = b without forming A⁻¹?

> **Type:** Application
> **Answer:** Solve Ly = b by forward substitution, then Lᵀx = y by back substitution. The cost is n² operations, half of LU on A alone.
> **Solution:** With A = LLᵀ, Ax = b becomes LLᵀx = b; setting y = Lᵀx, one first solves Ly = b (forward substitution: y₁ = b₁/l₁₁, yᵢ = (bᵢ − Σ_{j<i} l_ij y_j)/l_ii) and then Lᵀx = y (back substitution). Factorising once and re-using L for many right-hand sides is the whole point of the decomposition — in a Newton iteration the matrix stays fixed while b changes at every step. Because the multipliers involve only sums and divisions by positive pivots, the error growth is benign, which is why Cholesky is preferred whenever A is known to be SPD.
> **Key point:** Solve Ly = b then Lᵀx = y — factorise once, reuse for every b.

### Q156. `GATE-2`. What is a QR decomposition, and what is it good for?

> (a) A = QR with Q orthogonal and R upper triangular; it always exists, and it is the natural factorisation for least squares
> (b) A = QR with Q upper triangular and R orthogonal
> (c) A = QR exists only for symmetric matrices
> (d) A = QR is the same as the LU decomposition

> **Type:** MCQ `GATE-2`
> **Answer:** (a) (Option a).
> **Solution:** A = QR with QᵀQ = I and R upper triangular exists for every A (Householder reflections give it; if A is invertible the sign of R's diagonal may be chosen positive). Least squares minimises ‖Ax − b‖₂; writing A = QR gives ‖Rx − Qᵀb‖₂² + ‖(I − QQᵀ)b‖₂², so the normal equations Qᵀ(AᵀA)x = QᵀAᵀb collapse to Rx = Qᵀb, a triangular solve. QR also gives an orthonormal basis for the column space (the columns of Q) and, for rank-deficient A, reveals the rank as the number of non-zero diagonal entries of R. Options (b)–(d) are all structural errors.
> **Key point:** A = QR always exists; least squares reduces to Rx = Qᵀb with no squaring of the condition number.

### Q157. Compute the QR decomposition of A = [[2,1],[1,3]] by Gram–Schmidt on its columns.

> **Type:** Numerical
> **Answer:** Q = (1/√5)[[2,1],[1,−2]] and R = [[√5,√5],[0,√5]].
> **Solution:** Columns are a₁ = (2,1) and a₂ = (1,3). ‖a₁‖ = √5, so q₁ = (2,1)/√5. Project: r₁₂ = q₁ᵀa₂ = (2 + 3)/√5 = √5. Then w₂ = a₂ − r₁₂q₁ = (1,3) − √5(2,1)/√5 = (1 − 2, 3 − 1) = (−1, 2), whose norm is √5, giving q₂ = (−1,2)/√5. So Q = (1/√5)[[2,−1],[1,2]] with the sign of q₂ absorbed into R, and r₂₂ = q₂ᵀa₂ = (−1 + 6)/√5 = √5. Thus R = [[√5,√5],[0,√5]] and QR = A. Check QᵀQ = I and det Q = (4 + 1)/5 = 1.
> **Key point:** Gram–Schmidt on (2,1),(1,3) gives Q = (1/√5)[[2,−1],[1,2]], R = [[√5,√5],[0,√5]].

### Q158. Compare QR with Gram–Schmidt applied directly.

> (a) They produce the same Q in exact arithmetic, but Gram–Schmidt loses orthogonality numerically while Householder QR does not
> (b) Gram–Schmidt is always more stable
> (c) QR gives an R that is not upper triangular
> (d) Gram–Schmidt cannot be applied to a matrix

> **Type:** Comparison
> **Answer:** (a).
> **Solution:** In exact arithmetic the classical Gram–Schmidt and Householder QR produce the same factorisation up to column signs. Numerically they differ greatly: Gram–Schmidt projects with already-computed (approximate) q-vectors, so orthogonality errors amplify — the loss is worst when the columns are nearly linearly dependent, exactly the case QR is used for. Householder QR applies a sequence of orthogonal reflections, each of which perturbs orthogonality only by machine epsilon, so Q stays orthogonal to working precision. Modified Gram–Schmidt reorthogonalises and is much better than classical, but Householder remains the default in numerical libraries.
> **Key point:** Same answer in exact arithmetic; Householder QR is numerically stable, classical Gram–Schmidt is not.

### Q159. State the singular value decomposition and its two main uses.

> **Type:** Theory
> **Answer:** A = UΣVᵀ with U and V orthogonal and Σ = diag(σ₁, …, σ_r, 0, …) with σ₁ ≥ … ≥ σ_r ≥ 0 the singular values, equal to the square roots of the eigenvalues of AᵀA. It gives the best rank-r approximation in the Frobenius and spectral norms, and it exposes the 2-norm condition number as σ₁/σ_r.
> **Solution:** The singular values are σᵢ = √λᵢ(AᵀA), so they can be computed by an eigenproblem on the smaller Gram matrix; the left singular vectors are uᵢ = Avᵢ/σᵢ. Truncating to the first r terms gives A_r = Σ_{i≤r} σᵢuᵢvᵢᵀ with the Eckart–Young guarantee ‖A − A_r‖₂ = σ_{r+1} and ‖A − A_r‖_F = √(Σ_{i>r}σᵢ²), i.e. the best possible approximation of that rank. The condition number κ₂(A) = σ₁/σ_r quantifies how much a small relative input error is amplified, which is why SVD is the standard tool for detecting rank deficiency and near-dependence.
> **Key point:** A = UΣVᵀ, σᵢ = √λᵢ(AᵀA); truncated SVD is optimal in rank r; κ₂ = σ₁/σ_r.

### Q160. `GATE-1`. Find the singular values of A = [[1,1],[1,−1]].

> (a) 1 and 1
> (b) √2 and √2
> (c) 2 and 0
> (d) √2 and 0

> **Type:** MCQ `GATE-1`
> **Answer:** (b) √2 and √2 (Option b).
> **Solution:** AᵀA = [[1,1],[1,1]]ᵀ·[[1,1],[1,−1]] = [[1,1],[1,1]]·[[1,1],[1,−1]] = [[2,0],[0,2]] = 2I. Its eigenvalues are 2, 2, so σ₁ = σ₂ = √2. The matrix is the 2-norm isometry √2·(reflection about x₁ = x₂), so it preserves length up to the factor √2 and κ₂ = 1 — perfectly conditioned. Option (d) would be right only if AᵀA were singular, which it is not since det A = −2 ≠ 0.
> **Key point:** AᵀA = 2I for A = [[1,1],[1,−1]] ⇒ σ₁ = σ₂ = √2, κ₂ = 1.

### Q161. `GATE-2`. Given the singular values of A = [[1,2],[3,4]], what is its 2-norm condition number?

> (a) 1
> (b) σ₁/σ₂ = 5.46499/0.365966 ≈ 14.93
> (c) σ₁ + σ₂ = 5.83
> (d) det A = −2

> **Type:** MCQ `GATE-2`
> **Answer:** (b) σ₁/σ₂ ≈ 14.93 (Option b).
> **Solution:** AᵀA = [[10,14],[14,20]]; its characteristic polynomial is λ² − 30λ + 4, giving λ = 15 ± √221, so σ₁ = √(15 + √221) ≈ 5.46499 and σ₂ = √(15 − √221) ≈ 0.365966. Therefore κ₂(A) = σ₁/σ₂ = √((15 + √221)/(15 − √221)) ≈ 14.93. Option (c) is meaningless as a conditioning measure — the ratio, not the sum, controls error amplification. Option (d) confuses conditioning with size: a determinant of −2 says nothing about κ.
> **Key point:** κ₂(A) = σ₁/σ₂; for A = [[1,2],[3,4]] it is √((15+√221)/(15−√221)) ≈ 14.93.

### Q162. `GATE-1`. How does the SVD detect that a matrix is rank deficient, and what does the best rank-1 approximation look like?

> (a) By a zero determinant in Σ; the approximation is σ₁u₁v₁ᵀ
> (b) By a vanishing smallest singular value; the best rank-1 approximation is A₁ = σ₁u₁v₁ᵀ, and the error is σ₂
> (c) By repeated entries in U; the approximation is u₁v₁ᵀ
> (d) By a zero row in U; the approximation is the first column of A

> **Type:** MCQ `GATE-1`
> **Answer:** (b) (Option b).
> **Solution:** rank A = number of non-zero singular values, so a vanishing σ_r is exactly the rank deficiency, detected far more reliably than an exact-zero determinant in floating point. The Eckart–Young theorem states that the best rank-1 approximation in the spectral norm is σ₁u₁v₁ᵀ with error σ₂, and in the Frobenius norm the same matrix is optimal with error √(Σ_{i≥2}σᵢ²). For A = [[1,2,3],[4,5,6],[1,1,1]] the singular values are approximately 9.65881, 0.841102, 0, so rank A = 2 — a fact that floating-point elimination might report as 3.
> **Key point:** rank A = #{σᵢ > 0}; best rank-r approximation is the truncated SVD, with ‖A − A_r‖₂ = σ_{r+1}.

### Q163. `GATE-2`. How is the 2-norm of a matrix defined, and how does it relate to the SVD?

> (a) ‖A‖₂ = largest singular value = max‖Ax‖₂ over unit x
> (b) ‖A‖₂ = largest absolute eigenvalue
> (c) ‖A‖₂ = sum of all singular values
> (d) ‖A‖₂ = |det A|

> **Type:** MCQ `GATE-2`
> **Answer:** (a) (Option a).
> **Solution:** The induced (spectral) 2-norm is ‖A‖₂ = max_{‖x‖₂=1}‖Ax‖₂ = σ₁. Writing x = Σcᵢvᵢ and expanding shows ‖Ax‖₂² = Σσᵢ²cᵢ², maximised by taking x = v₁. The other options are the Frobenius norm (c), the spectral radius (b) and the determinant (d) — all different quantities. For a symmetric matrix with positive eigenvalues σ₁ = λ_max, so the 2-norm coincides with the largest eigenvalue, but not in general.
> **Key point:** ‖A‖₂ = σ₁ = max‖Ax‖₂ over unit x; ‖A‖_F = √(Σσᵢ²); ‖A‖₁ = max column sum.

### Q164. `GATE-1`. Why is solving a system via LU generally preferred to forming A⁻¹ explicitly?

> (a) A⁻¹ rarely exists
> (b) LU costs about n³/3 operations, computes det A as a by-product, and avoids the extra error of an explicit inverse
> (c) A⁻¹ is only defined for symmetric matrices
> (d) LU gives the exact answer while A⁻¹ never does

> **Type:** MCQ `GATE-1`
> **Answer:** (b) (Option b).
> **Solution:** Factoring costs roughly n³/3 flops and each subsequent solve only n², so for k right-hand sides the total is n³/3 + kn² instead of n³ for an explicit inverse — a large saving. The factorisation also delivers det A = ±∏u_ii and reveals singularity through a zero pivot. Numerically, forming A⁻¹ squares the condition number of the problem: ‖δA⁻¹‖/‖A⁻¹‖ ≈ κ(A)·‖δA‖/‖A‖, so the computed inverse can be much worse than a solve would be. Option (d) is false in both directions — LU solves are also approximate.
> **Key point:** LU: n³/3 once, n² per solve, det free, and no squaring of κ.

### Q165. `GATE-2`. When is the LU decomposition preferred over the QR decomposition for solving Ax = b?

> (a) Always, since LU is more accurate
> (b) When A is square and nonsingular, LU is slightly cheaper; QR is preferred for least squares, overdetermined systems, and rank-deficient A
> (c) QR is only for symmetric matrices
> (d) LU cannot be used for square systems

> **Type:** MCQ `GATE-2`
> **Answer:** (b) (Option b).
> **Solution:** For a square nonsingular system both work, and LU's triangular structure gives a marginally smaller constant. QR is the better tool when the system is overdetermined (least squares) or rank-deficient, because it detects and exposes the rank through R's diagonal and does not require nonsingularity. QR is also more numerically stable when A is ill-conditioned, since it does not form AᵀA (whose squaring of the condition number is the source of the loss). Cholesky is preferred when A is known SPD, costing half of LU. Option (a) ignores that both are backward stable.
> **Key point:** LU for square nonsingular; QR for least squares / rank-deficient / ill-conditioned; Cholesky when A is SPD.

### Q166. `GATE-1`. What does a zero on the diagonal of R in a QR decomposition of A indicate?

> (a) That A is invertible
> (b) That the corresponding column of A is a linear combination of the preceding ones
> (c) That the matrix is symmetric
> (d) That A has complex eigenvalues

> **Type:** MCQ `GATE-1`
> **Answer:** (b) (Option b).
> **Solution:** A = QR with Q orthogonal preserves linear dependence: columns of A are dependent exactly when columns of R are, and since R is upper triangular, a_j lies in the span of a_1, …, a_(j−1) precisely when r_jj = 0 (equivalently when column j of R is zero from row j down). The first r non-zero diagonal entries therefore equal rank A. For A = [[1,2],[2,4]]: Q = (1/√5)[[1,2],[2,−1]], R = [[√5,2√5],[0,0]], so r₂₂ = 0 and rank A = 1. Option (a) is exactly backwards.
> **Key point:** Number of non-zero entries on R's diagonal = rank A; a zero at position j means a_j depends on a_1, …, a_(j−1).

### Q167. `GATE-2`. How is the Schur decomposition of a real matrix A written, and what does it say?

> (a) A = QTQ* with T upper triangular (or quasi-triangular with 2 × 2 blocks) and Q unitary; T has the same eigenvalues as A
> (b) A = QTQ* with T diagonal, so A is always diagonalisable
> (c) A = QT with T having the same singular values as A
> (d) A = QTQ⁻¹ with T = A

> **Type:** MCQ `GATE-2`
> **Answer:** (a) (Option a).
> **Solution:** The Schur form puts a matrix in upper-triangular form by unitary similarity, so it always exists (over ℝ it is quasi-triangular, with 1 × 1 real blocks and 2 × 2 blocks for conjugate pairs). For a normal matrix — real symmetric is the common case — the Schur form *is* diagonal. Schur's triangular form is what the QR algorithm produces and is the basis of every practical eigenvalue routine. Option (b) holds only for normal matrices; option (c) confuses Schur with SVD; option (d) is vacuous.
> **Key point:** Schur: A = QTQ* with T upper triangular, same eigenvalues, exists always; diagonal only if A is normal.

### Q168. `GATE-1`. What is the Jordan canonical form, and when is it available?

> (a) A = PJP⁻¹ with J block diagonal of Jordan blocks; it exists over every field but is most useful over ℂ
> (b) A = PJP⁻¹ with J diagonal, always
> (c) A = PJPᵀ with J upper triangular, only for symmetric A
> (d) A = PJP⁻¹ with J the RREF of A

> **Type:** MCQ `GATE-1`
> **Answer:** (a) (Option a).
> **Solution:** Over ℂ every matrix has a Jordan form: J is block diagonal with Jordan blocks J_k(λ) = λI + superdiagonal ones. Over ℝ the form exists only if the complex eigenvalues are allowed as 2 × 2 blocks, so a real matrix with a complex pair has no real Jordan form. The size of the largest block at an eigenvalue λ gives the exponent of (λ − λ) in the minimal polynomial (Q133) and the number of generalised eigenvectors needed. For A = [[2,1],[0,2]] the form is A itself. Option (b) describes a diagonal form, which exists only for diagonalisable matrices.
> **Key point:** Jordan form: A = PJP⁻¹, always over ℂ; block size at λ = largest Jordan block size at λ.

### Q169. `GATE-2`. Which decomposition would you use to compress a large matrix to rank r with the least error?

> (a) LU, keeping the first r pivots
> (b) The truncated SVD, since it minimises the error among all rank-r approximations
> (c) QR, keeping the first r columns of Q
> (d) The Cholesky factorisation truncated to rank r

> **Type:** MCQ `GATE-2`
> **Answer:** (b) The truncated SVD minimises the error among all rank-r approximations (Option b).
> **Solution:** Eckart–Young states that the best rank-r approximation to A in the spectral norm is the truncated SVD, with error exactly σ_{r+1}; in the Frobenius norm it is also optimal, with error √(Σ_{i>r}σᵢ²). Storing only U_r, Σ_r, V_r costs O(nr) instead of O(n²). The other options are not optimal: keeping r rows of L from an LU captures only the leading r pivot directions and ignores the rest of the spectrum, truncating Cholesky is meaningless for compression, and keeping r columns of Q gives an orthonormal basis of a subspace, not the best rank-r matrix.
> **Key point:** Truncated SVD is the optimal rank-r approximation (Eckart–Young); other factorisations are not.

---

## Section 9. Partial differentiation: partial and total derivatives, total differential, chain rule, implicit functions, Jacobians

### Q170. Define the first partial derivatives of f(x, y) and state how many are needed for a gradient.

> **Type:** Theory
> **Answer:** f_x = ∂f/∂x is the rate of change of f with y held fixed, and f_y = ∂f/∂y with x held fixed. For a function of two variables there are two first partials, and together they form the gradient ∇f = (f_x, f_y).
> **Solution:** Partial differentiation is ordinary one-variable differentiation with the other variable treated as a constant, so for f = x²y + 3xy² + sin(xy) we get f_x = 2xy + 3y² + y·cos(xy) and f_y = x² + 6xy + x·cos(xy). The gradient collects the partials into a vector field, and the geometric picture is that at any point ∇f is perpendicular to the level curve f = c through that point, with its magnitude equal to the maximum rate of increase per unit distance. Only the two first partials are needed to form ∇f; second partials come from differentiating those.
> **Key point:** f_x, f_y are rates with the other variable fixed; ∇f = (f_x, f_y) is perpendicular to level curves.

### Q171. `GATE-1`. For f = x²y + 3xy² + sin(xy), what are f_x and f_y?

> (a) f_x = 2xy + 3y² + y cos(xy); f_y = x² + 6xy + x cos(xy)
> (b) f_x = 2xy + 3y² + x cos(xy); f_y = x² + 6xy + y cos(xy)
> (c) f_x = 2xy + 3y² − y cos(xy); f_y = x² + 6xy − x cos(xy)
> (d) f_x = 2x + 3y + cos(xy); f_y = x² + 6x + cos(xy)

> **Type:** MCQ `GATE-1`
> **Answer:** (a) (Option a).
> **Solution:** Differentiating x²y + 3xy² with y fixed: 2xy + 3y²; differentiating sin(xy) with y fixed gives cos(xy)·y by the chain rule. So f_x = 2xy + 3y² + y cos(xy). Similarly with x fixed, the chain-rule factor is x: f_y = x² + 6xy + x cos(xy). Option (b) swaps the chain-rule factors x and y, which is the single most common error here — ∂/∂x of sin(xy) carries the factor y, not x.
> **Key point:** f_x = 2xy + 3y² + y cos(xy), f_y = x² + 6xy + x cos(xy); the chain-rule factor is the *other* variable.

### Q172. State the four second-order partial derivatives and Clairaut's theorem.

> **Type:** Theory
> **Answer:** f_xx, f_xy, f_yx, f_yy. Clairaut's theorem: if f_xy and f_yx both exist in a neighbourhood and are continuous there, then f_xy = f_yx — the mixed partials are equal.
> **Solution:** For f = x²y + 3xy² + sin(xy): f_xx = 2y − y² sin(xy), f_xy = 2x + 6y + cos(xy) − xy sin(xy), f_yx = the same expression, f_yy = 6x − x² sin(xy). The equality f_xy = f_yx is not automatic: it needs continuity of the mixed partials near the point. A classic counterexample is f(x,y) = xy(x² − y²)/(x² + y²) with f(0,0) = 0, which has f_xy(0,0) = 1 but f_yx(0,0) = −1. In applications the hypothesis holds almost everywhere, so the mixed partials are treated as equal.
> **Key point:** f_xx, f_xy, f_yx, f_yy; Clairaut gives f_xy = f_yx under continuity. For the example, f_xx = 2y − y² sin(xy) and f_yy = 6x − x² sin(xy).

### Q173. `GATE-2`. Distinguish the total differential from the differential of a partial derivative.

> (a) The total differential is df = f_x dx + f_y dy, the linear part of the change; d(f_x) is a different object involving second partials
> (b) The total differential is df = f_x dx + f_y dy, and d(f_x) = f_x dx + f_y dy
> (c) The total differential requires f to be linear
> (d) d(f_x) does not exist unless f_x is constant

> **Type:** MCQ `GATE-2`
> **Answer:** (a) (Option a).
> **Solution:** The total differential df = f_x dx + f_y dy is the first-order approximation to the actual change, f(x + dx, y + dy) − f(x, y) = df + (higher-order terms); for small increments the error is second order. By contrast d(f_x) = f_xx dx + f_xy dy is the differential of the partial-derivative *function*, and it involves second partials — so option (b), which reuses the same expression, is exactly the confusion the question targets. Option (c) is false: df is a linear approximation to a nonlinear function. Option (d) is false — d(f_x) is a perfectly well-defined linear map.
> **Key point:** df = f_x dx + f_y dy is the linear part of the change; d(f_x) = f_xx dx + f_xy dy involves second partials.

### Q174. Find the total differential of z = x²y at the point (2, 3) and use it to estimate the change for dx = 0.01, dy = −0.02.

> **Type:** Numerical
> **Answer:** dz = 2xy dx + x² dy = 12 dx + 4 dy; at (2,3) with dx = 0.01, dy = −0.02, dz = 0.12 − 0.08 = 0.04.
> **Solution:** z_x = 2xy and z_y = x², so dz = z_x dx + z_y dy = 2xy dx + x² dy. At (2,3): z_x = 12, z_y = 4, hence dz = 12(0.01) + 4(−0.02) = 0.12 − 0.08 = 0.04. The true change is 2.12²·2.98 − 2²·3 = 13.3432 − 12 = 1.3432... computing: 2.12² = 4.4944, times 2.98 = 13.3933, minus 12 gives 1.3933 — far larger than 0.04, because dx = 0.01 is not small *relative to x = 2*: a 0.5% change. This illustrates that the differential approximation is only trustworthy when the relative increments are small.
> **Key point:** dz = 2xy dx + x² dy = 12 dx + 4 dy = 0.04 at (2,3); the approximation needs small *relative* increments to be accurate.

### Q175. `GATE-1`. A surface is given by z = f(x, y). What does dz = f_x dx + f_y dy estimate?

> (a) The change in height of the surface over a small horizontal displacement (dx, dy)
> (b) The change in f_x only
> (c) The volume under the surface
> (d) The curvature of the surface

> **Type:** MCQ `GATE-1`
> **Answer:** (a) (Option a).
> **Solution:** Geometrically, the tangent plane to the graph at (x₀, y₀, f(x₀,y₀)) is z − f(x₀,y₀) = f_x dx + f_y dy, so dz is the rise of the tangent plane over the small horizontal displacement (dx, dy). The error between the actual surface and the plane is second order, so dz is a first-order (linear) approximation of the height change. This is the basis of linearising nonlinear models such as Newton–Raphson and of error propagation: δz ≈ f_x δx + f_y δy.
> **Key point:** dz = f_x dx + f_y dy is the rise of the tangent plane — a first-order approximation to Δz.

### Q176. State the multivariable chain rule for z = f(x, y) with x = x(s, t) and y = y(s, t).

> **Type:** Theory
> **Answer:** z_s = f_x x_s + f_y y_s and z_t = f_x x_t + f_y y_t; in matrix form ∇_z = Jᵀ∇_f where J = ∂(x,y)/∂(s,t) is the Jacobian.
> **Solution:** Each of x(s,t) and y(s,t) depends on both s and t, so by linearity z depends on s through both, giving z_s = f_x x_s + f_y y_s. Written in matrices with ∇_f = (f_x, f_y)ᵀ and J = [[x_s, x_t],[y_s, y_t]], the pair of equations is ∇_z = Jᵀ∇_f, so ∇_z = [[x_s, y_s],[x_t, y_t]]·(f_x, f_y)ᵀ. This is the same rule that makes the Jacobian transpose the differential of a composition, and it is what the chain rule becomes in differential geometry: dz = df ∘ (dx ⊕ dy).
> **Key point:** z_s = f_x x_s + f_y y_s, z_t = f_x x_t + f_y y_t; in matrix form ∇_z = Jᵀ∇_f.

### Q177. `GATE-2`. If u = f(x, y) and x = s² + t, y = s − t², what is u_s?

> (a) f_x(2s + 1) + f_y(1)
> (b) f_x(2s) + f_y(−2t)
> (c) f_x(2s + 1) + f_y(1 − 2t)
> (d) f_x(s² + t) + f_y(s − t²)

> **Type:** MCQ `GATE-2`
> **Answer:** (c) f_x(2s + 1) + f_y(1 − 2t) (Option c).
> **Solution:** x_s = 2s + 1 and y_s = 1, since y = s − t² has no s-dependence beyond the explicit s. So u_s = f_x·x_s + f_y·y_s = f_x(2s + 1) + f_y·1. Option (a) is this answer misread as u_t — for t we get x_t = 1, y_t = −2t, hence u_t = f_x(1) + f_y(−2t) = f_x − 2t f_y, and option (b) mixes the two partials of x together. Option (d) substitutes the outer function's arguments instead of applying the chain rule at all.
> **Key point:** u_s = f_x(2s + 1) + f_y(1) for x = s² + t, y = s − t²; x_s = 2s + 1, y_s = 1.

### Q178. Find the Jacobian determinant of the transformation u = x² + y², v = xy.

> **Type:** Numerical
> **Answer:** J = ∂(u,v)/∂(x,y) = [[2x, 2y],[y, x]], and the Jacobian determinant is 2x² − 2y².
> **Solution:** The Jacobian is the matrix of partials of the outputs with respect to the inputs, u_x = 2x, u_y = 2y, v_x = y, v_y = x, so J = [[2x, 2y],[y, x]] and det J = (2x)(x) − (2y)(y) = 2x² − 2y². Note the two rows are deliberately listed in the order (u,v): the determinant changes sign if the rows are swapped, which matters when the Jacobian is used in a change-of-variables integral. The map is invertible wherever det J ≠ 0.
> **Key point:** J = [[2x, 2y],[y, x]] with det J = 2x² − 2y²; the row order follows the output order.

### Q179. `GATE-1`. What does a non-zero Jacobian determinant guarantee for a change of variables?

> (a) That the map is one-to-one locally, so a local inverse exists and the area element transforms by the factor |det J|
> (b) That the map is one-to-one globally
> (c) That the map is linear
> (d) That the map preserves area

> **Type:** MCQ `GATE-1`
> **Answer:** (a) (Option a).
> **Solution:** The inverse function theorem says that if det J ≠ 0 at a point, then in a neighbourhood of that point the map is one-to-one and has a smooth local inverse — this is exactly the condition required for a change of variables in a double integral. The area element becomes dA_uv = |det J| dA_xy, the absolute value because orientation must not flip the sign of an area. Option (b) confuses local invertibility with global: for example (u,v) = (x², y) has det J = 2x ≠ 0 for x ≠ 0 yet is two-to-one in x. Option (d) is true only when |det J| = 1.
> **Key point:** det J ≠ 0 ⇒ local one-to-one with a smooth inverse, and dA transforms as |det J| dA.

### Q180. `GATE-2`. Differentiate x² + xy + y² = 1 implicitly to find dy/dx.

> (a) dy/dx = (2x + y)/(x + 2y)
> (b) dy/dx = −(2x + y)/(x + 2y)
> (c) dy/dx = (x + 2y)/(2x + y)
> (d) dy/dx = −(x + 2y)/(2x + y)

> **Type:** MCQ `GATE-2`
> **Answer:** (b) dy/dx = −(2x + y)/(x + 2y) (Option b).
> **Solution:** Let F(x, y) = x² + xy + y² − 1 = 0. Differentiating with the chain rule, F_x + F_y·y' = 0, so y' = −F_x/F_y = −(2x + y)/(x + 2y). Option (a) drops the minus sign, which is the standard slip: the rule is y' = −F_x/F_y. Option (c) is the reciprocal, and option (d) has both errors. The result is valid where F_y = x + 2y ≠ 0, i.e. away from the points where the level curve has a vertical tangent; dy/dx is the slope of the curve and is perpendicular to the gradient (2x + y, x + 2y).
> **Key point:** Implicit: dy/dx = −F_x/F_y = −(2x + y)/(x + 2y) — never drop the minus sign.

### Q181. Find the second derivative y'' of the curve x² + xy + y² = 1 in terms of x and y.

> **Type:** Application
> **Answer:** y'' = −2[(x + 2y)² − (2x + y)(x + 2y) + (2x + y)²]/(x + 2y)³ = −6(x² + xy + y²)/(x + 2y)³, so on the curve y'' = −6/(x + 2y)³.
> **Solution:** Write N = 2x + y and D = x + 2y, so y' = −N/D. The quotient rule gives y'' = −[(2 + y')D − N(1 + 2y')]/D², and substituting y' = −N/D turns the bracket into (2D² − 2ND + 2N²)/D, hence y'' = −2(D² − ND + N²)/D³. Expanding the bracket, D² − ND + N² = (x² + 4xy + 4y²) − (2x² + 5xy + 2y²) + (4x² + 4xy + y²) = 3x² + 3xy + 3y², so y'' = −6(x² + xy + y²)/(x + 2y)³. Since the curve has x² + xy + y² = 1, this is −6/(x + 2y)³. Check at (1, 0): the formula gives −6, and the alternative route y'' = −(F_xx + 2F_xy y' + F_yy y'²)/F_y = −(2 + 2(−2) + 2·4)/1 = −6 ✓.
> **Key point:** y'' = −(F_xx + 2F_xy y' + F_yy y'²)/F_y; for x²+xy+y²=1 this reduces to −6/(x+2y)³.

### Q182. `GATE-1`. What is the geometric meaning of the gradient at a point?

> (a) It is perpendicular to the level curve and its magnitude is the maximum rate of change of f per unit distance
> (b) It is parallel to the level curve
> (c) It is the curvature of the level curve
> (d) It points in the direction of least increase of f

> **Type:** MCQ `GATE-1`
> **Answer:** (a) (Option a).
> **Solution:** Moving along a level curve gives no change in f, so ∇f is orthogonal to any tangent vector t there: ∇f·t = 0. The maximum rate of increase per unit distance is |∇f|, attained in the direction of ∇f itself, and the direction of steepest *decrease* is −∇f. The directional derivative along a unit vector u is D_u f = ∇f·u, and by Cauchy–Schwarz this is largest when u = ∇f/|∇f|. Hence option (b) is exactly backwards, and option (d) names the wrong direction.
> **Key point:** ∇f ⊥ level curves; |∇f| is the max rate of change, attained along ∇f; steepest descent is −∇f.

### Q183. `GATE-2`. Compute the directional derivative of f = x² + y² at (3, 4) along the unit vector u = (3/5, 4/5).

> (a) 5
> (b) 6
> (c) 10
> (d) 2.5

> **Type:** MCQ `GATE-2`
> **Answer:** (c) 10 (Option c).
> **Solution:** ∇f = (2x, 2y), so at (3, 4) it is (6, 8). The directional derivative is D_u f = ∇f·u = 6(3/5) + 8(4/5) = 18/5 + 32/5 = 50/5 = 10. Since u = (3/5, 4/5) = ∇f/|∇f| at this point, u points along the gradient, so this is by construction the maximum rate of change and equals |∇f| = √(36 + 64) = 10. Option (a), 5, would be the rate per unit step along the *radial unit direction divided again*; option (b) is 2x = 6, the first component of the gradient alone.
> **Key point:** D_u f = ∇f·u = (6,8)·(3/5,4/5) = 10 = |∇f|, since u is parallel to ∇f at (3,4).

### Q184. `GATE-1`. How do the directional derivative and the Jacobian transpose differ in form?

> (a) They are the same: D_u f = ∇f·u = ∇_zᵀ Jᵀ u when z = f(x(s,t), y(s,t))
> (b) They are unrelated quantities
> (c) The directional derivative needs the determinant of the Jacobian
> (d) The Jacobian transpose is always symmetric

> **Type:** MCQ `GATE-1`
> **Answer:** (a) (Option a).
> **Solution:** The directional derivative is the Jacobian applied to a displacement: D_u f = ∇f·u for a unit u. If x and y themselves depend on (s,t) with Jacobian J, then the chain rule gives ∇_z = Jᵀ∇_f, so D_u f = ∇_f·(Jᵀu) = (Jᵀ∇_f)·u — the same scalar, obtained either way. Option (c) is wrong because directional derivatives are first-order and never involve a determinant; option (d) is wrong because a Jacobian transpose is generally not symmetric.
> **Key point:** D_u f = ∇f·u = (Jᵀ∇_f)·u — the Jacobian transpose propagates gradients under a change of variables.

### Q185. `GATE-2`. Verify Euler's homogeneous function theorem for h = x³y + 2xy³.

> (a) x h_x + y h_y = 3h holds because h is homogeneous of degree 4
> (b) x h_x + y h_y = h holds because h is homogeneous of degree 1
> (c) x h_x + y h_y = 0 for all homogeneous functions
> (d) x h_x + y h_y = 2h

> **Type:** MSQ `GATE-2`
> **Answer:** (a).
> **Solution:** h is homogeneous of degree 4, since every term is a product of four variables' powers (x³y and xy³ both have total degree 4). Euler's theorem states x h_x + y h_y = 4h. Directly: h_x = 3x²y + 2y³ and h_y = x³ + 6xy², so x h_x + y h_y = 3x³y + 2xy³ + x³y + 6xy³ = 4x³y + 8xy³ = 4h ✓. This is the multivariable generalisation of f(tv) = t^n f(v) and is the standard tool for computing homogeneous functions from their partials. Option (b) applies the degree-1 case wrongly.
> **Key point:** For homogeneous degree n, x·f_x + y·f_y = n·f; here n = 4 and the identity checks directly.

### Q186. State Euler's homogeneous function theorem and one use of it.

> **Type:** Theory
> **Answer:** If f is differentiable and homogeneous of degree n, then x·f_x + y·f_y + z·f_z = n·f. It lets you determine f from any one of its partials: if f_x is known, f = (x f_x)/n.
> **Solution:** Homogeneity of degree n means f(tx, ty, tz) = tⁿ f(x, y, z) for all t; differentiating with respect to t at t = 1 gives exactly x f_x + y f_y + z f_z = n f. In thermodynamics this identity is Gibbs'–Duhem relation (S dT + V dp = μ dN-type bookkeeping) and in elasticity it relates the strain-energy function to the stress. A practical use: given the partial f_x of a degree-2 homogeneous function, recover f = (x f_x)/2 by integrating in x and fixing the arbitrary function using homogeneity.
> **Key point:** Homogeneous degree n ⇒ x f_x + y f_y + z f_z = n f; use it to recover f from a single partial.

### Q187. `GATE-1`. What is the divergence of a vector field, and what is its physical meaning?

> (a) div P = P_x + P_y + P_z, the net outward flow per unit volume at a point
> (b) div P = P_x·P_y·P_z, the product of the components
> (c) The divergence is a vector
> (d) The divergence of a constant field is non-zero

> **Type:** MCQ `GATE-1`
> **Answer:** (a) (Option a).
> **Solution:** For P = (P, Q, R), div P = ∂P/∂x + ∂Q/∂y + ∂R/∂z — a scalar. Its value at a point is the limit of the net outward flux per unit volume around that point, by the divergence theorem: ∮_S P·n dS = ∭_V div P dV. Positive divergence means a local source, negative a local sink, zero means divergence-free. Option (b) is nonsense; option (c) is wrong since it is a scalar; option (d) is wrong because a constant field has divergence 0.
> **Key point:** div P = P_x + Q_y + R_z, a scalar equal to net outward flux density; ∮P·n dS = ∭ div P dV.

### Q188. `GATE-2`. Compute div F and curl F for F = (x² + 3yz, xy + z, sin x).

> (a) div F = 3x; curl F = (−1, 3y − cos x, y − 3z)
> (b) div F = 2x + y; curl F = 0
> (c) div F = 0; curl F = (−1, 3y − cos x, y − 3z)
> (d) div F = 3x; curl F = 0

> **Type:** MCQ `GATE-2`
> **Answer:** (a) (Option a).
> **Solution:** div F = ∂(x² + 3yz)/∂x + ∂(xy + z)/∂y + ∂(sin x)/∂z = 2x + x + 0 = 3x. Curl in the (curl) orientation (R_y − Q_z, P_z − R_x, Q_x − P_y) = (0 − 1, 0 − cos x, y − 3z) = (−1, 3y − cos x, y − 3z). Both are non-zero, so options (b) and (d) are wrong; option (c) drops the 2x term. Note that curl F is identically non-zero because the first component is −1, so this field is not conservative — consistent with the fact that the scalar potential ∂P/∂y = 3z does not equal ∂Q/∂x = y.
> **Key point:** For F = (x²+3yz, xy+z, sin x): div F = 3x, curl F = (−1, 3y − cos x, y − 3z).

### Q189. `GATE-1`. When is a vector field conservative, and how do you test it?

> (a) When the curl vanishes everywhere on a simply connected domain
> (b) When the divergence vanishes everywhere
> (c) When the field is irrotational at one point
> (d) When the field is linear in the coordinates

> **Type:** MCQ `GATE-1`
> **Answer:** (a) (Option a).
> **Solution:** A field F on a simply connected region is conservative — that is, F = ∇φ for some scalar potential φ — if and only if ∇ × F = 0 everywhere on the region. The "simply connected" hypothesis matters: F = (−y, x)/r² has zero curl away from the origin yet no global potential, because the region ℝ²∖{0} is not simply connected. Option (b) is a different property (incompressible flow), and option (c) is far too weak — the test must hold everywhere, not at one point.
> **Key point:** F conservative ⟺ curl F ≡ 0 on a simply connected domain; divergence is a different condition.

---

## Section 10. Unconstrained and constrained optimisation, Lagrange multipliers, second derivative test, boundary and global extrema

### Q190. State the necessary condition for an unconstrained local extremum of a differentiable f(x, y).

> **Type:** Theory
> **Answer:** Both first partials must vanish: f_x = 0 and f_y = 0, so the point is a critical point; equivalently ∇f = 0, which fails if ∇f is ever the zero vector-free direction.
> **Solution:** If f is differentiable and has a local extremum at an interior point, small displacements in the x and y directions are all admissible, so the one-variable necessary condition applies in each direction and gives f_x = f_y = 0. The proof: along the line x = x₀ + t, y = y₀, the function of t has a local extremum at t = 0, so the derivative vanishes. The condition is necessary but not sufficient — points satisfying it may be minima, maxima, or saddles. The direction of steepest ascent and descent at any point is ±∇f, and at a critical point that direction collapses, which is exactly why gradient-based searches stall there.
> **Key point:** Interior extremum ⇒ ∇f = 0; necessary, not sufficient (saddles also satisfy it).

### Q191. `GATE-2`. Apply the second derivative test to f = x² + y² − 2x − 4y + 1.

> (a) f has a local minimum of −4 at (1, 2)
> (b) f has a local maximum of −4 at (1, 2)
> (c) f has a saddle at (1, 2)
> (d) f has a local minimum of 5 at (2, 1)

> **Type:** MCQ `GATE-2`
> **Answer:** (a) f has a local minimum of −4 at (1, 2) (Option a).
> **Solution:** f_x = 2x − 2 = 0 and f_y = 2y − 4 = 0 give the critical point (1, 2). The second partials are f_xx = 2, f_yy = 2, f_xy = 0, so D = f_xx f_yy − f_xy² = 4 > 0 and f_xx = 2 > 0, which by the second derivative test makes it a local minimum. The value is 1 + 4 − 2 − 8 + 1 = −4. Completing the square confirms this globally: f = (x − 1)² + (y − 2)² − 4 ≥ −4, so (1,2) is in fact the absolute minimum. Option (c) misuses the test — D > 0 with f_xx > 0 means minimum, not saddle.
> **Key point:** ∇f = 0 at (1,2); D = 4 > 0 and f_xx = 2 > 0 ⇒ local (here absolute) minimum with value −4.

### Q192. `GATE-1`. What is the nature of the critical point of f = −x² − y² + 4x + 2y?

> (a) A local maximum at (2, 1) with value 5
> (b) A local minimum at (2, 1) with value 5
> (c) A saddle at (2, 1)
> (d) A local maximum at (4, 2) with value 5

> **Type:** MCQ `GATE-1`
> **Answer:** (a) A local maximum at (2, 1) with value 5 (Option a).
> **Solution:** f_x = −2x + 4 = 0 and f_y = −2y + 2 = 0 give (2, 1). Here f_xx = f_yy = −2 and f_xy = 0, so D = 4 > 0 with f_xx = −2 < 0, which by the second derivative test is a local maximum. The value is −4 − 1 + 8 + 2 = 5. Completing the square, f = −(x − 2)² − (y − 1)² + 5 ≤ 5, so (2,1) is the absolute maximum. Option (d) confuses the gradient components 4 and 2 with the location.
> **Key point:** f_xx = f_yy = −2, D = 4 > 0 with f_xx < 0 ⇒ max at (2,1), value 5; f = −(x−2)²−(y−1)²+5.

### Q193. `GATE-2`. Test f = x² − y² for the nature of its critical point.

> (a) Local minimum at (0,0), since f_xx = 2 > 0
> (b) Local maximum at (0,0), since f_yy = −2 < 0
> (c) Saddle point at (0, 0), since f_xx f_yy < 0
> (d) No critical point exists

> **Type:** MCQ `GATE-2`
> **Answer:** (c) Saddle point at (0, 0) (Option c).
> **Solution:** f_x = 2x = 0 and f_y = −2y = 0 give the origin as the only critical point. f_xx = 2, f_yy = −2, f_xy = 0, so D = −4 < 0 — the saddle case of the test. Directly, along y = 0, f = x² ≥ 0, while along x = 0, f = −y² ≤ 0, so the function rises along one direction and falls along the perpendicular one. Options (a) and (b) each look at only one second partial, which is not the test; option (d) is false since the gradient does vanish at the origin.
> **Key point:** D = f_xx f_yy − f_xy² = −4 < 0 ⇒ saddle; verify by walking along the two axes.

### Q194. `GATE-2`. Test f = x² + 2y² − 4xy + x − y + 1, whose critical point is (0, 1/4).

> (a) Local minimum with value 7/8
> (b) Local maximum with value 7/8
> (c) Saddle point, since D = 2·4 − (−4)² = −8 < 0
> (d) The critical point test is inconclusive because f_xx = 0

> **Type:** MCQ `GATE-2`
> **Answer:** (c) Saddle point (Option c).
> **Solution:** f_x = 2x − 4y + 1 = 0 and f_y = 4y − 4x − 1 = 0; solving gives x = 0, y = 1/4, and f(0, 1/4) = 0 + 2/16 + 0 + 0 − 1/4 + 1 = 7/8. The second partials are f_xx = 2, f_yy = 4, f_xy = −4, giving D = 2·4 − 16 = −8 < 0, so the point is a saddle — the function decreases along one direction from it and increases along another. Option (d) is false: f_xx = 2 ≠ 0. A nonzero D settles the question immediately, which is the point of the test.
> **Key point:** D = 2·4 − (−4)² = −8 < 0 ⇒ saddle at (0, 1/4), value 7/8.

### Q195. State the second derivative test in two variables, including the inconclusive case.

> **Type:** Theory
> **Answer:** At a critical point compute D = f_xx f_yy − f_xy². If D > 0 and f_xx > 0, a local minimum; if D > 0 and f_xx < 0, a local maximum; if D < 0, a saddle; if D = 0, the test is inconclusive and other methods are needed.
> **Solution:** The test is the two-variable analogue of the one-variable rule f'' > 0 (min) and f'' < 0 (max), with the mixed partial supplying the missing information. D is (up to a positive factor) the discriminant of the quadratic part of the Taylor expansion, so D > 0 means the quadratic form is definite (same sign in all directions) and D < 0 means it is indefinite — the local picture is decided by the quadratic terms and the cubic ones are negligible. The D = 0 case needs a different tool: completing the square, a Taylor expansion to higher order, or examining lines through the point, as with f = x² + y⁴ which has a minimum at the origin with D = 0.
> **Key point:** D > 0 → min (if f_xx > 0) or max (if f_xx < 0); D < 0 → saddle; D = 0 → test inconclusive.

### Q196. `GATE-2`. What does D = 0 leave unresolved, and what do you do then?

> (a) Nothing — D = 0 always means a saddle
> (b) The quadratic term is degenerate, so you must go to the Taylor expansion of higher order, complete the square, or examine lines through the point
> (c) D = 0 means there is no critical point
> (d) D = 0 implies the point is a maximum

> **Type:** MCQ `GATE-2`
> **Answer:** (b) (Option b).
> **Solution:** D = 0 means the quadratic part of the Taylor expansion has a zero eigenvalue, so the quadratic terms cannot decide the question. Example: f = x² + y⁴ has a strict local minimum at the origin although f_xx = 2, f_yy = 0 and D = 0, while f = x³ + y³ has neither a min nor a max there (it takes both signs along y = ±x). Both have D = 0, so the test cannot separate them. Option (a) is false, option (c) is nonsense — a critical point already exists — and option (d) is contradicted by the first example.
> **Key point:** D = 0 ⇒ inconclusive; x² + y⁴ is a min, x³ + y³ is a saddle — both have D = 0.

### Q197. `GATE-1`. Find the absolute extrema of f = x² − 3x + 1 on the closed interval [0, 2].

> (a) Absolute minimum −5/4 at x = 3/2, absolute maximum 1 at x = 0
> (b) Absolute minimum 1 at x = 0, absolute maximum −1 at x = 2
> (c) Absolute minimum −1 at x = 2, absolute maximum 1 at x = 0
> (d) No absolute extrema exist

> **Type:** MCQ `GATE-1`
> **Answer:** (a) (Option a).
> **Solution:** On a closed interval, absolute extrema occur at critical points or endpoints. f' = 2x − 3 = 0 gives the interior critical point x = 3/2, where f = 9/4 − 9/2 + 1 = −5/4. At the endpoints: f(0) = 1 and f(2) = 4 − 6 + 1 = −1. Comparing {−5/4, 1, −1}, the smallest is −5/4 and the largest is 1, so the absolute minimum is −5/4 at x = 3/2 and the absolute maximum is 1 at x = 0. The extreme value theorem guarantees both exist on a closed bounded interval, ruling out option (d).
> **Key point:** Compare critical points and endpoints: f(3/2) = −5/4 (min), f(0) = 1 (max), f(2) = −1.

### Q198. `GATE-2`. Find the absolute maximum and minimum of f(x, y) = x² + y² on the disk x² + y² ≤ 4.

> (a) Maximum 4 at (±2, 0) and (0, ±2); minimum 0 at (0, 0)
> (b) Maximum 0 at the origin; minimum 4 on the boundary
> (c) Maximum 4 at the origin
> (d) Maximum 16, minimum 0

> **Type:** MSQ `GATE-2`
> **Answer:** (a).
> **Solution:** The critical point is where f_x = 2x = 0 and f_y = 2y = 0, giving the origin, where f = 0. The boundary is the circle x² + y² = 4, and on it f is identically 4, so the maximum is 4, attained at all four boundary points (±2, 0) and (0, ±2). Since the region is closed and bounded, both absolute extrema exist; comparing interior and boundary values, min = 0 at the origin and max = 4 on the boundary. Option (d) confuses f with f² = (x²+y²)².
> **Key point:** On a compact region, compare interior critical points with the boundary: f = 0 at the origin (min), f = 4 on the circle (max).

### Q199. State the Lagrange multiplier condition for extremising f(x, y) subject to g(x, y) = c.

> **Type:** Theory
> **Answer:** At a constrained extremum where ∇g ≠ 0, there is a scalar λ with ∇f = λ∇g, i.e. f_x = λ g_x and f_y = λ g_y, together with the constraint.
> **Solution:** Along the constraint curve, the rate of change of f is ∇f·t for tangent t, and since t ⊥ ∇g, the constrained derivative is ∇f·t = 0 for all such t, forcing ∇f to be parallel to ∇g. The multiplier λ is then the rate of change of f per unit change in g, which is why it appears directly in sensitivity analysis. The regularity condition ∇g ≠ 0 is needed; at a singular point of the constraint (∇g = 0) the test does not apply and one must handle the point separately. In several variables the same condition is ∇f = Σλᵢ∇gᵢ.
> **Key point:** ∇f = λ∇g with ∇g ≠ 0; λ is the rate of f per unit of g along the normal direction.

### Q200. `GATE-1`. Use Lagrange multipliers to maximise xy subject to x² + y² = 1.

> (a) Maximum 1/2 at x = y = 1/√2
> (b) Maximum 1 at x = y = 1
> (c) Maximum 1/2 at x = −y
> (d) Maximum 0 everywhere on the circle

> **Type:** MCQ `GATE-1`
> **Answer:** (a) Maximum 1/2 at x = y = 1/√2 (Option a).
> **Solution:** Set f = xy − λ(x² + y² − 1). Then f_x = y − 2λx = 0 and f_y = x − 2λy = 0. If x, y ≠ 0, these give y = 2λx and x = 2λy, so 1 = 4λ², λ = ±1/2. For λ = 1/2: y = x, and the constraint gives 2x² = 1, so x = y = 1/√2 with xy = 1/2. For λ = −1/2: y = −x, x = ±1/√2, giving xy = −1/2, the minimum. The cases x = 0 or y = 0 give xy = 0, not extreme. So the maximum is 1/2 at x = y = 1/√2, matching the AM–GM bound (x + y)² ≤ 2 with xy ≤ 1/2.
> **Key point:** ∇(xy) = λ∇(x²+y²) gives λ = ±1/2; max xy = 1/2 at x = y = 1/√2, min = −1/2 at x = −y.

### Q201. `GATE-2`. Maximise x + y subject to x² + y² = 1.

> (a) Maximum √2 at x = y = 1/√2
> (b) Maximum 2 at x = y = 1
> (c) Maximum 1 at x = 1, y = 0
> (d) Maximum √2 at x = −y

> **Type:** MCQ `GATE-2`
> **Answer:** (a) Maximum √2 at x = y = 1/√2 (Option a).
> **Solution:** With f = x + y − λ(x² + y² − 1), the conditions are 1 = 2λx and 1 = 2λy, so x = y. The constraint then gives 2x² = 1, and taking the positive root maximises: x = y = 1/√2 with x + y = √2. The stationary value −√2 at x = y = −1/√2 is the minimum. This agrees with Cauchy–Schwarz, (x + y)² ≤ (1² + 1²)(x² + y²) = 2. Option (b) is infeasible since (1,1) does not satisfy the constraint; option (c) is a stationary point only in the sense of a non-maximal direction.
> **Key point:** ∇(x+y) = λ∇(x²+y²) ⇒ x = y; max x + y = √2 at x = y = 1/√2, min = −√2 at the negative point.

### Q202. `GATE-2`. Maximise x²y subject to x + y = 1 with x, y ≥ 0.

> (a) Maximum 4/27 at x = 2/3, y = 1/3
> (b) Maximum 1/8 at x = y = 1/2
> (c) Maximum 1/4 at x = 1/2, y = 1/2
> (d) Maximum 4/27 at x = 1/3, y = 2/3

> **Type:** MCQ `GATE-2`
> **Answer:** (a) Maximum 4/27 at x = 2/3, y = 1/3 (Option a).
> **Solution:** With f = x²y − λ(x + y − 1), the conditions are 2xy − λ = 0 and x² − λ = 0, so 2xy = x², and with y > 0 this gives x = 2y. Substituting into x + y = 1: 3y = 1, y = 1/3, x = 2/3, and f = (4/9)(1/3) = 4/27. The endpoints x = 0 or y = 0 give f = 0, so 4/27 is the maximum. Option (b) is the trap of using AM–GM on three equal quantities — the maximum of x·x·y with x + x + 2y = 2 gives x = 2/3, y = 1/3, which is the same point, so the value 4/27 is the right one and 1/8 is not.
> **Key point:** 2xy = x² ⇒ x = 2y; with x + y = 1, max x²y = 4/27 at (2/3, 1/3).

### Q203. `GATE-1`. Find the point on the line 3x + 4y = 25 closest to the origin.

> (a) (3, 4)
> (b) (5, 5/2)
> (c) (4, 13/4)
> (d) (3, 4) lies on the line but is not the closest point

> **Type:** MCQ `GATE-1`
> **Answer:** (a) (3, 4), at distance 5.
> **Solution:** Minimise f = x² + y² subject to 3x + 4y = 25. The multiplier conditions f_x = 2x = 3λ and f_y = 2y = 4λ give x = 3λ/2 and y = 2λ. Substituting into the constraint: 3(3λ/2) + 4(2λ) = 25, so (9/2 + 8)λ = (25/2)λ = 25, giving λ = 2, hence x = 3, y = 4. Verify 3·3 + 4·4 = 9 + 16 = 25 ✓, and the distance is √(9 + 16) = 5, which matches the standard formula 25/√(3² + 4²) = 25/5 = 5. Option (b) fails the constraint: 15 + 10 = 25 ✓ actually holds, but the distance is √(25 + 6.25) = 5.59 > 5, so it is not the closest; option (c) gives 12 + 13 = 25 ✓ with distance √(16 + 10.5625) = 5.15 > 5. Only (3, 4) attains the minimum, and since the objective is strictly convex on a line, the critical point is the unique global minimum.
> **Key point:** Closest point to 3x + 4y = 25 is (3, 4) at distance 5 = 25/√(3²+4²).

### Q204. `GATE-2`. Formulate the problem of maximising xyz subject to x + y + z = 3, x, y, z ≥ 0 and solve it.

> (a) Maximum 1 at x = y = z = 1
> (b) Maximum 27 at x = y = z = 3
> (c) Maximum 3 at x = y = z = 1
> (d) No maximum exists since the constraint set is unbounded

> **Type:** MCQ `GATE-2`
> **Answer:** (a) Maximum 1 at x = y = z = 1 (Option a).
> **Solution:** With f = xyz − λ(x + y + z − 3), the conditions yz = λ, xz = λ, xy = λ. If all variables are non-zero, dividing gives x = y = z, and the constraint gives x = y = z = 1 with f = 1. If exactly one variable is zero, f = 0, which is smaller; the boundary therefore does not improve on 1. The domain is not unbounded because x, y, z ≥ 0 with a fixed sum bounds each variable by 3, so option (d) is false. This is exactly the AM–GM inequality (x + y + z)/3 ≥ (xyz)^(1/3), which gives xyz ≤ 1.
> **Key point:** yz = xz = xy = λ ⇒ x = y = z = 1, max xyz = 1; this is AM–GM in Lagrange-multiplier form.

### Q205. `GATE-1`. What does the Lagrange multiplier λ represent geometrically in ∇f = λ∇g?

> (a) The rate of change of the maximum value of f per unit change in the constraint level c
> (b) The magnitude of ∇f
> (c) The distance from the extremum to the constraint curve
> (d) The number of constrained critical points

> **Type:** MCQ `GATE-1`
> **Answer:** (a) (Option a).
> **Solution:** For the family of level curves g = c, the extremal value f*(c) satisfies f*(c + dc) ≈ f*(c) + λ dc, so λ = df*/dc — the sensitivity of the optimal value to the constraint level. In economics λ is the marginal value of the resource; in stress–strain analysis it is a Lagrange multiplier playing the role of a shadow price. Option (b) is wrong because |∇f| = |λ||∇g|, not |λ|; option (c) has no meaning, and option (d) counts solutions rather than describing any of them.
> **Key point:** λ = df*/dc, the marginal rate of the optimal objective value with respect to the constraint level.

### Q206. `GATE-2`. Maximise f = x + y² subject to x² + y² = 1.

> (a) Maximum 5/4 at x = 1/2, y = ±√3/2
> (b) Maximum 3/2 at x = 1/2, y = 1
> (c) Maximum 1 at x = 1, y = 0
> (d) Maximum 5/4 at x = 1, y = 1/2

> **Type:** MCQ `GATE-2`
> **Answer:** (a) Maximum 5/4 at x = 1/2, y = ±√3/2 (Option a).
> **Solution:** Eliminate x instead: the constraint gives x = ±√(1 − y²) with |y| ≤ 1, so f = ±√(1 − y²) + y². Taking the positive sign of x (which always maximises) and setting t = y², f = √(1 − t) + t with derivative −1/(2√(1 − t)) + 1 = 0, giving √(1 − t) = 1/2, t = 3/4, so y² = 3/4, y = ±√3/2, x = 1/2. Then f = 1/2 + 3/4 = 5/4. The check with multipliers agrees: f_x = 1 = 2λx and f_y = 2y = 2λy, so λ = 1 when y ≠ 0 and then x = 1/2, y² = 3/4. The endpoints give f = 1.
> **Key point:** Max x + y² on the unit circle is 5/4 at x = 1/2, y = ±√3/2; multipliers give λ = 1 there.

### Q207. `GATE-2`. How do you maximise a continuous function over a closed and bounded region?

> (a) Find all interior critical points and check the entire boundary, then compare the values
> (b) Only the interior critical points need checking
> (c) Only the boundary needs checking
> (d) Differentiate the boundary parameterisation and take the largest value found

> **Type:** MCQ `GATE-2`
> **Answer:** (a) (Option b).
> **Solution:** The extreme value theorem guarantees that a continuous function on a closed bounded set attains both an absolute maximum and an absolute minimum, and the absolute maximum on such a region must occur either at an interior critical point or on the boundary (it cannot occur at an interior point that is not critical). Hence the method is: solve ∇f = 0 inside, parameterise each boundary piece and maximise there including its endpoints, then compare all candidate values. Option (b) would miss the common case where the maximum sits on the boundary; option (c) would miss interior maxima; option (d) is only the boundary half of the method.
> **Key point:** Compact region ⇒ both extrema exist; candidates = interior critical points + all boundary points.

### Q208. `GATE-1`. A function has a unique interior critical point and a negative-definite Hessian there. What can you conclude?

> (a) It is a strict local maximum
> (b) It is a strict local minimum, and it is the unique local minimum
> (c) It is a global minimum without further assumptions
> (d) Nothing can be concluded

> **Type:** MCQ `GATE-1`
> **Answer:** (b) (Option b).
> **Solution:** A negative-definite Hessian gives a strict local minimum by the second derivative test, and because the function is quadratic — the Hessian of a quadratic form is constant — a negative-definite Hessian everywhere means strict convexity, so this is the unique global minimum. Careful: the conclusion "unique local minimum" holds because the Hessian is negative definite at the only critical point, so no other critical point exists, and any local extremum must be critical. The stronger claim in (c) — global — needs the Hessian to be negative definite everywhere, not just at that point. For a general nonlinear f, a negative-definite Hessian at one point guarantees only local minimality.
> **Key point:** Negative-definite Hessian at the only critical point ⇒ unique local minimum; global needs it everywhere (automatic for a quadratic form).

### Q209. `GATE-2`. Minimise f = x² + y² + xy subject to x + y = 1.

> (a) Minimum 3/4 at x = y = 1/2
> (b) Minimum 1/2 at x = y = 1/2
> (c) Maximum 3/4 at x = y = 1/2
> (d) Minimum 1 at x = 0 or y = 0

> **Type:** MCQ `GATE-2`
> **Answer:** (a) Minimum 3/4 at x = y = 1/2 (Option a).
> **Solution:** With f = x² + y² + xy − λ(x + y − 1): f_x = 2x + y − λ = 0 and f_y = 2y + x − λ = 0. Subtracting gives x − y = 0, so x = y; the constraint then gives x = y = 1/2, λ = 3/2, and f = 1/4 + 1/4 + 1/4 = 3/4. Eliminating y confirms it independently: y = 1 − x gives f = x² + (1 − x)² + x(1 − x) = x² − x + 1 = (x − 1/2)² + 3/4 ≥ 3/4, with equality only at x = 1/2. The function is strictly convex (the matrix [[1,1/2],[1/2,1]] is positive definite), so this is the unique global minimum. Option (b) has the right point but the wrong value, and option (c) mislabels a minimum as a maximum.
> **Key point:** On y = 1 − x, f = (x − 1/2)² + 3/4, so the minimum is 3/4 at x = y = 1/2, with λ = 3/2.

### Q210. `GATE-2`. Which conditions must hold at a constrained extremum of f subject to g₁ = 0 and g₂ = 0?

> (a) ∇f = λ₁∇g₁ + λ₂∇g₂, with the multipliers unknown, plus both constraints
> (b) ∇f = 0
> (c) ∇f = λ∇g₁ with a single multiplier
> (d) ∇g₁ = ∇g₂

> **Type:** MSQ `GATE-2`
> **Answer:** (a).
> **Solution:** With two constraints in two variables the feasible set is generically a finite set of points, so the tangent space is zero-dimensional and every feasible point is a "critical point" in the multiplier sense: there must be scalars λ₁, λ₂ with ∇f = λ₁∇g₁ + λ₂∇g₂, which reads as a system of two equations in the two multipliers, solvable whenever ∇g₁ and ∇g₂ are linearly independent. Each solution point is then compared by direct evaluation, and regularity requires ∇g₁, ∇g₂ to be independent. Option (b) is the unconstrained condition and is far too strong; option (c) uses one multiplier where two are needed; option (d) is not required at all.
> **Key point:** Two constraints ⇒ ∇f = λ₁∇g₁ + λ₂∇g₂, a 2-equation system in λ₁, λ₂, valid when ∇g₁, ∇g₂ are independent.

---

## Section 11. Multiple integrals: double and triple integrals, order of integration, polar / cylindrical / spherical coordinates, change of variables, applications

### Q211. Write a double integral as an iterated integral over a rectangle, in both orders.

> **Type:** Application
> **Answer:** ∫₀²∫₀¹ f(x, y) dx dy = ∫₀¹∫₀² f(x, y) dy dx, both equal to the integral of f over [0,1] × [0,2].
> **Solution:** An iterated integral fixes one variable at a time: the inner integral with respect to x uses the limits x = 0 and x = 1 while y stays inside the outer integral, and conversely. The equality of the two forms is exactly Fubini's theorem, valid when f is continuous on the closed rectangle (or integrable in the product sense). The value for f = x² + y² over this rectangle is ∫₀²∫₀¹ (x² + y²) dx dy = ∫₀² (1/3 + y²) dy = 2/3 + 8/3 = 10/3.
> **Key point:** ∫₀²∫₀¹ = ∫₀¹∫₀² by Fubini; the limits belong to the variable being integrated.

### Q212. `GATE-1`. Evaluate ∫₀¹∫₀¹ (x² + y²) dy dx.

> (a) 2/3
> (b) 1
> (c) 4/3
> (d) 2

> **Type:** MCQ `GATE-1`
> **Answer:** (a) 2/3 (Option a).
> **Solution:** Integrate in y first: ∫₀¹ (x² + y²) dy = x² + 1/3. Then ∫₀¹ (x² + 1/3) dx = 1/3 + 1/3 = 2/3. Reversing the order gives the same value by Fubini: ∫₀¹ (1/3 + y²) dy = 1/3 + 1/3 = 2/3 ✓. Option (c), 4/3, is the value if you forget one of the two 1/3 contributions.
> **Key point:** ∫₀¹∫₀¹ (x² + y²) dy dx = 2/3; each variable contributes its own 1/3.

### Q213. `GATE-2`. What does Fubini's theorem state, and when does it apply?

> (a) For a continuous f on a closed rectangle, ∫∫f dA computed in either order agree
> (b) The integral of a non-negative function can be computed in either order, even if it is infinite
> (c) Fubini applies to any function, since integration always commutes
> (d) Fubini says the integral equals the product of the separate integrals

> **Type:** MSQ `GATE-2`
> **Answer:** (a) and (b).
> **Solution:** Fubini's theorem: if f is continuous on a closed rectangle (more generally, if f is integrable on the product), the two iterated integrals exist and are equal. Tonelli's theorem extends this to non-negative measurable f, where both orders are equal in [0, +∞] — that is what option (b) states, and it is the version that justifies rearranging divergent non-negative integrals without worry. Option (c) is false: for a general signed f the iterated integrals can fail to exist or differ. Option (d) is the separability property, valid only for f = g(x)h(y).
> **Key point:** Fubini: continuous (or integrable) f ⇒ both orders agree; Tonelli: same for non-negative f, allowing +∞.

### Q214. `GATE-1`. Evaluate ∫₀^∞∫₀^∞ e^(−(x²+y²)) dx dy using polar coordinates.

> (a) π
> (b) 2π
> (c) π/2
> (d) 1

> **Type:** MCQ `GATE-1`
> **Answer:** (a) π (Option a).
> **Solution:** The region is the whole plane, so in polar coordinates r ranges over [0, ∞) and θ over [0, 2π), and the area element is dA = r dr dθ, giving ∫₀^2π∫₀^∞ e^(−r²) r dr dθ. Substituting u = r², the inner integral is ∫₀^∞ e^(−u) du/2 = 1/2, and the answer is 2π · (1/2) = π. This is the two-dimensional Gaussian integral; squaring it gives the one-dimensional value √π, a classical proof of ∫₀^∞ e^(−x²) dx = √π. Option (c) drops the polar Jacobian factor r, which is the standard trap.
> **Key point:** ∫∫ e^(−r²) dA = ∫₀^2π dθ ∫₀^∞ e^(−r²) r dr = 2π·(1/2) = π; the r in dA is essential.

### Q215. State the polar substitution and the Jacobian, and the transformed limits for a disk of radius a.

> **Type:** Theory
> **Answer:** x = r cos θ, y = r sin θ with r ≥ 0, 0 ≤ θ < 2π, and the Jacobian is |∂(x,y)/∂(r,θ)| = r, so dA = r dr dθ. The disk x² + y² ≤ a² becomes 0 ≤ r ≤ a, 0 ≤ θ ≤ 2π.
> **Solution:** The Jacobian is the determinant [[cos θ, −r sin θ],[sin θ, r cos θ]] = r cos²θ + r sin²θ = r. Beyond the disk, the key limit pairs are: first quadrant 0 ≤ θ ≤ π/2, 0 ≤ r ≤ a; outside the circle but inside the square [0,a]×[0,a], 0 ≤ θ ≤ π/2 with sec θ ≤ r ≤ csc θ (from x ≤ a and y ≤ a); between the circles r₁ and r₂, r₁ ≤ r ≤ r₂. The factor r is what makes polar coordinates ideal for circular regions and is the thing to check most often in exams.
> **Key point:** dA = r dr dθ; disk radius a ⇒ 0 ≤ r ≤ a, 0 ≤ θ ≤ 2π; always keep the r.

### Q216. `GATE-2`. Evaluate ∫∫_D (x² + y²) dA over the unit disk D by polar coordinates.

> (a) π/2
> (b) π/4
> (c) π
> (d) 2π

> **Type:** MCQ `GATE-2`
> **Answer:** (a) π/2 (Option a).
> **Solution:** With x² + y² = r² and dA = r dr dθ over 0 ≤ r ≤ 1, 0 ≤ θ ≤ 2π, the integral is ∫₀^2π∫₀¹ r²·r dr dθ = ∫₀^2π [r⁴/4]₀¹ dθ = 2π/4 = π/2. Direct evaluation in Cartesian coordinates confirms it: ∫₋₁¹∫₋√(1−x²)^√(1−x²) (x² + y²) dy dx gives π/2 as well. Option (b) is what you get by forgetting the outer 2π; option (d) comes from using the wrong power of r.
> **Key point:** ∫∫_D r² dA = ∫₀^2π∫₀¹ r³ dr dθ = 2π(1/4) = π/2.

### Q217. `GATE-1`. Find the area of the ellipse x²/9 + y²/4 ≤ 1 by a change of variables.

> (a) 6π
> (b) 3π
> (c) 12π
> (d) π

> **Type:** MCQ `GATE-1`
> **Answer:** (a) 6π (Option a).
> **Solution:** Substitute x = 3u, y = 2v, which maps the unit disk u² + v² ≤ 1 onto the ellipse. The Jacobian is |∂(x,y)/∂(u,v)| = 3·2 = 6, so Area = ∫∫_disk 6 du dv = 6 · π. Equivalently in polar coordinates, x = 3r cos θ, y = 2r sin θ gives a Jacobian of 6r, and ∫₀^2π∫₀¹ 6r dr dθ = 6π. Sanity check: semi-axes 3 and 2 give π ab = 6π ✓.
> **Key point:** Semiaxes a, b ⇒ area πab; the scaling x = au, y = bv contributes the factor ab = 6 to the Jacobian.

### Q218. `GATE-2`. What is the Jacobian of the transformation u = x + y, v = x − y, and what does |∂(u,v)/∂(x,y)| = 2 imply?

> (a) The transformation is not invertible
> (b) Area elements satisfy du dv = 2 dx dy, so dx dy = (1/2) du dv
> (c) The transformation preserves area
> (d) The Jacobian is 1/2

> **Type:** MCQ `GATE-2`
> **Answer:** (b) du dv = 2 dx dy, so dx dy = (1/2) du dv (Option b).
> **Solution:** ∂(u,v)/∂(x,y) = [[1,1],[1,−1]] with determinant −2, so the absolute value is 2. Non-zero, so the map is locally invertible (x = (u+v)/2, y = (u − v)/2), and the area elements satisfy du dv = 2 dx dy. To integrate over a region in (u,v) you must therefore multiply the integrand by the **reciprocal** 1/2 — using 2 instead of 1/2 doubles the answer. Option (d) confuses the two directions of the transformation.
> **Key point:** |∂(u,v)/∂(x,y)| = 2 ⇒ dx dy = (1/2) du dv; use the reciprocal of the Jacobian you computed.

### Q219. Evaluate ∫∫_T xy dA over the triangle T = {(x, y) : x ≥ 0, y ≥ 0, x + y ≤ 1} in both Cartesian and (u, v) coordinates.

> **Type:** Numerical
> **Answer:** 1/24 in both cases. Cartesian: ∫₀¹∫₀^(1−x) xy dy dx = 1/24. In (u, v) = (x + y, x − y): 0 ≤ u ≤ 1, −u ≤ v ≤ u, integrand (u² − v²)/4 times the Jacobian 1/2, giving the same 1/24.
> **Solution:** Cartesian: the inner integral is x·(1−x)²/2, so the answer is ∫₀¹ x(1−x)²/2 dx = (1/2)(1/2 − 2/3 + 1/4) = (1/2)(1/12) = 1/24. Transformed: x = (u+v)/2, y = (u − v)/2 give xy = (u² − v²)/4; the triangle maps to the wedge 0 ≤ u ≤ 1, −u ≤ v ≤ u since u = x + y ∈ [0,1] and |v| = |x − y| ≤ x + y = u. With the factor 1/2, the integral is ∫₀¹∫₋ᵤ^u (u² − v²)/8 dv du = ∫₀¹ (2u³/8 + 2u³/24) du = ∫₀¹ u³(1/4 + 1/12) du = (1/3)·(1/3) = 1/24 ✓.
> **Key point:** ∫∫_T xy dA = 1/24; under u = x+y, v = x−y the triangle becomes 0 ≤ u ≤ 1, −u ≤ v ≤ u with factor 1/2.

### Q220. `GATE-1`. When is a change of variables u = u(x, y), v = v(x, y) valid for transforming an integral?

> (a) When the Jacobian ∂(u,v)/∂(x,y) is non-zero on the region, so a one-to-one local inverse exists
> (b) Always, for any differentiable change of variables
> (c) Only when the transformation is linear
> (d) Only when the new region is a rectangle

> **Type:** MCQ `GATE-1`
> **Answer:** (a) (Option a).
> **Solution:** The inverse function theorem requires det J ≠ 0 to give a smooth local inverse, which is what makes the change of variables legitimate; the integrand is then rewritten as f(x(u,v), y(u,v))/|J| and the region mapped correspondingly. If the map is many-to-one, one must split the region into pieces on which it is one-to-one and add the contributions. Option (b) is false since a zero Jacobian makes the inverse singular, and options (c) and (d) are irrelevant restrictions.
> **Key point:** Change of variables needs |J| ≠ 0 and one-to-one behaviour; the integrand picks up the factor 1/|J|.

### Q221. `GATE-2`. State the change-of-variables formula for a double integral.

> (a) ∫∫_R f(x, y) dx dy = ∫∫_{R'} f(x(u,v), y(u,v)) |∂(x,y)/∂(u,v)| du dv
> (b) ∫∫_R f dx dy = ∫∫_{R'} f(x(u,v), y(u,v)) |∂(u,v)/∂(x,y)| du dv
> (c) ∫∫_R f dx dy = ∫∫_{R'} f du dv, with no Jacobian
> (d) The formula holds only when the transformation is linear

> **Type:** MCQ `GATE-2`
> **Answer:** (a) (Option a).
> **Solution:** The area element transforms as dA_xy = |∂(x,y)/∂(u,v)| du dv, so the integral acquires the factor |∂(x,y)/∂(u,v)| = 1/|∂(u,v)/∂(x,y)|. Option (b) has the Jacobian the wrong way round — a very common error. In Q218, |∂(u,v)/∂(x,y)| = 2, so the correct multiplier when integrating over (u, v) is 1/2, exactly as (a) requires. Option (c) is right only for area-preserving maps.
> **Key point:** Multiply by |∂(x,y)/∂(u,v)| = 1/|∂(u,v)/∂(x,y)| — the reciprocal of the Jacobian you usually compute.

### Q222. `GATE-1`. Evaluate the volume under z = x² + y² over the unit disk, in polar coordinates.

> (a) π/2
> (b) π/4
> (c) π
> (d) 2π

> **Type:** MCQ `GATE-1`
> **Answer:** (a) π/2 (Option a).
> **Solution:** The volume is ∫∫_D (x² + y²) dA = ∫₀^2π∫₀¹ r²·r dr dθ = 2π ∫₀¹ r³ dr = 2π(1/4) = π/2 — the same integral as Q216, because volume under a graph is the integral of the height. Option (c) is the volume under z = 1, and option (b) the volume under z = r/2. This example shows the general principle: a volume integral is a double integral of the height function.
> **Key point:** Volume under z = f over D is ∫∫_D f dA = π/2 here; ∫₀^2π∫₀¹ r³ dr dθ = π/2.

### Q223. `GATE-2`. Find the area enclosed by the curve r = 2a cos θ in polar coordinates.

> (a) πa²
> (b) 2πa²
> (c) πa²/2
> (d) 4πa²

> **Type:** MCQ `GATE-2`
> **Answer:** (a) πa² (Option a).
> **Solution:** r = 2a cos θ is a circle: r² = 2ar cos θ, i.e. x² + y² = 2ax, i.e. (x − a)² + y² = a² — a circle of radius a centred at (a, 0), so its area is πa². Computing it in polar: r ≥ 0 requires cos θ ≥ 0, so −π/2 ≤ θ ≤ π/2, and A = (1/2)∫₋π/2^π/2 (2a cos θ)² dθ = 2a² ∫₋π/2^π/2 cos²θ dθ = 2a²(π/2) = πa² ✓. Equivalently 2πa² on [0, π/2] would double-count the region, since the curve is traced twice over the full 0 to 2π range.
> **Key point:** r = 2a cos θ is the circle (x−a)² + y² = a², area πa², from (1/2)∫₋π/2^π/2 4a²cos²θ dθ.

### Q224. `GATE-1`. State the cylindrical and spherical coordinate substitutions with their Jacobians.

> **Type:** Theory
> **Answer:** Cylindrical: x = r cos θ, y = r sin θ, z = z with dV = r dr dθ dz. Spherical: x = ρ sin φ cos θ, y = ρ sin φ sin θ, z = ρ cos φ with dV = ρ² sin φ dρ dφ dθ, where φ is the polar angle from the positive z-axis.
> **Solution:** Both keep the angular variables θ (azimuth) and differ in how the radial distance and the third coordinate are used. Cylindrical coordinates suit regions bounded by cylinders and planes parallel to z; spherical ones suit spheres, cones (φ constant) and radial surfaces (ρ constant). The angle convention matters: with φ measured from the z-axis, the Jacobian is ρ² sin φ and the limits are 0 ≤ φ ≤ π; with the angle measured from the horizontal plane the sine becomes a cosine. A quick check on the ball of radius R: the volume comes out (4/3)πR³, matching (1/2)·4πR²·R.
> **Key point:** Cylindrical dV = r dr dθ dz; spherical dV = ρ² sin φ dρ dφ dθ with φ from the z-axis.

### Q225. `GATE-2`. Evaluate the volume of the ball of radius 2 using spherical coordinates.

> (a) 32π/3
> (b) 16π
> (c) 32π
> (d) 64π/3

> **Type:** MCQ `GATE-2`
> **Answer:** (a) 32π/3 (Option a).
> **Solution:** The integrand for volume is 1, and the volume element is dV = ρ² sin φ dρ dφ dθ, so V = ∫₀^2π∫₀^π∫₀² ρ² sin φ dρ dφ dθ. Separating: ∫₀² ρ² dρ = 8/3, ∫₀^π sin φ dφ = [−cos φ]₀^π = 2, and ∫₀^2π dθ = 2π. So V = (8/3)(2)(2π) = 32π/3, which matches (4/3)πR³ with R = 2 ✓. The common trap is writing an extra factor of ρ, which would give ρ⁴ in the radial integral and the nonphysical value 128π/5.
> **Key point:** V_ball(R) = ∫₀^2π∫₀^π∫₀^R ρ² sin φ dρ dφ dθ = (8/3)(2)(2π) = 4πR³/3 = 32π/3; exactly one factor of the Jacobian.

### Q226. `GATE-2`. A lamina of constant density occupies the semicircle of radius 2 above the x-axis. Find its centroid's y-coordinate.

> (a) 8/(3π)
> (b) 4/(3π)
> (c) 2/π
> (d) 4/π

> **Type:** MCQ `GATE-2`
> **Answer:** (a) 8/(3π) (Option a).
> **Solution:** With constant density the mass M equals the area A = (1/2)π(2)² = 2π, and the first moment about the x-axis is M·ȳ = ∫∫ y dA. In polar coordinates y = r sin θ and dA = r dr dθ over 0 ≤ r ≤ 2, 0 ≤ θ ≤ π: M ȳ = ∫₀^π∫₀² (r sin θ) r dr dθ = (∫₀² r² dr)(∫₀^π sin θ dθ) = (8/3)(2) = 16/3. Hence ȳ = (16/3)/(2π) = 8/(3π) ≈ 0.849. Sanity check: a semicircle's centroid sits at 4R/(3π) from its diameter, so with R = 2 that is 8/(3π) ✓ — it must be less than R = 2 and greater than 2/3.
> **Key point:** Centroid of a semicircle of radius R is 4R/(3π) from the diameter; here ȳ = 8/(3π), and the Jacobian r is needed in the moment integral.

### Q227. `GATE-1`. State Green's theorem and give its area formula.

> (a) ∮_C (P dx + Q dy) = ∫∫_D (Q_x − P_y) dA; taking P = −y/2, Q = x/2 gives Area = (1/2)∮(x dy − y dx)
> (b) ∮_C (P dx + Q dy) = ∫∫_D (P_x + Q_y) dA
> (c) Area = ∮_C x dy
> (d) Green's theorem applies only to non-simply-connected regions

> **Type:** MCQ `GATE-1`
> **Answer:** (a) (Option a).
> **Solution:** Green's theorem converts a circulation around a simple closed curve C bounding a region D into a double integral of the curl: ∮(P dx + Q dy) = ∫∫(Q_x − P_y) dA, provided P, Q have continuous partials on D. Setting P = −y/2, Q = x/2 gives Q_x − P_y = 1/2 + 1/2 = 1, so Area = (1/2)∮(x dy − y dx). For the circle x = a cos θ, y = a sin θ, dx = −a sin θ dθ, dy = a cos θ dθ, the integrand x dy − y dx = a dθ, giving Area = (1/2)∫₀^2π a dθ = πa² ✓. Option (c) is the special case Q = 0, P = −x, which also works but is one of several valid forms. Option (d) is backwards — the theorem requires D to be simply connected with C its boundary.
> **Key point:** ∮(P dx + Q dy) = ∫∫(Q_x − P_y) dA; Area = (1/2)∮(x dy − y dx) = ∮x dy = ∮−y dx.

### Q228. `GATE-2`. State Stokes' theorem and the divergence theorem, and say what each converts.

> (a) Stokes: ∮_C F·dr = ∫∫_S curl F·n dS; divergence: ∫∫∫_V div F dV = ∮_{∂V} F·n dS
> (b) Stokes converts a double integral to a single integral; the divergence theorem converts a single integral to a double integral
> (c) Stokes: ∫∫ curl F dA = ∮ F·dr; divergence: ∫∫ F·n dS = ∫∫∫ div F dV
> (d) Both theorems require the region to be unbounded

> **Type:** MCQ `GATE-2`
> **Answer:** (a) (Option a).
> **Solution:** Stokes' theorem says the line integral of a vector field around a closed curve C equals the surface integral of its curl through any surface S spanning C: ∮_C F·dr = ∫∫_S (∇×F)·n dS. The divergence theorem says the flux out of a closed surface equals the integral of the divergence over the enclosed volume: ∫∫∫_V ∇·F dV = ∮_{∂V} F·n dS. Both convert an integral over a higher-dimensional boundary into one over the interior. Option (b) has the directions reversed, and option (d) is nonsense — both theorems are stated for bounded regions with piecewise smooth boundaries.
> **Key point:** Stokes: ∮C F·dr = ∫∫S curl F·n dS. Divergence: ∫∫∫V div F dV = ∮∂V F·n dS.

### Q229. `GATE-1`. Evaluate ∫∫∫_B (x² + y² + z²) dV over the unit ball B by symmetry or by spherical coordinates.

> (a) 4π/5
> (b) 4π/3
> (c) π
> (d) 8π/15

> **Type:** MCQ `GATE-1`
> **Answer:** (a) 4π/5 (Option a).
> **Solution:** By symmetry each coordinate contributes equally, so the integral is 3∫∫∫ z² dV. With z = ρ cos φ, dV = ρ² sin φ dρ dφ dθ: ∫∫∫ z² dV = ∫₀^2π dθ ∫₀^π cos²φ sin φ dφ ∫₀¹ ρ⁴ dρ = 2π · (2/3) · (1/5) = 4π/15, where ∫₀^π cos²φ sin φ dφ = [−cos³φ/3]₀^π = 2/3. Multiplying by 3 gives 4π/5. A cross-check: ∫∫∫ (x²+y²+z²) dV = ∫₀¹ ρ²·ρ²dρ · ∫₀^π sin φ dφ · ∫₀^2π dθ = (1/5)(2)(2π) = 4π/5 ✓.
> **Key point:** Spherically symmetric integrands are easy: ∫∫∫ ρ² dV = ∫₀¹ρ⁴dρ · 2 · 2π = 4π/5; use symmetry to split into three equal parts.

### Q230. `GATE-2`. Reverse the order of integration in ∫₀¹∫₀^(1−x) f(x, y) dy dx.

> (a) ∫₀¹∫₀^(1−y) f(x, y) dx dy
> (b) ∫₀¹∫_(1−y)¹ f(x, y) dx dy
> (c) ∫₀¹∫₀^(1−x) f(x, y) dx dy
> (d) ∫₀¹∫_(−y)¹ f(x, y) dx dy

> **Type:** MCQ `GATE-2`
> **Answer:** (a) ∫₀¹∫₀^(1−y) f(x, y) dx dy (Option a).
> **Solution:** The original region is the triangle x ≥ 0, y ≥ 0, x + y ≤ 1, bounded by the lines x = 0, y = 0 and x + y = 1. To reverse, describe the region with y outermost: y ranges over [0, 1], and for a fixed y the horizontal slice runs from the line x = 0 to the line x = 1 − y. So the reversed integral is ∫₀¹∫₀^(1−y) f(x, y) dx dy. The reliable method is to draw the region and label the horizontal slices; option (b) describes the region to the right of the line, which is outside the triangle, and option (c) has not changed the order at all.
> **Key point:** For the triangle x + y ≤ 1 in the first quadrant, swapping to x-innermost gives ∫₀¹∫₀^(1−y) f dx dy.

### Q231. `GATE-1`. Evaluate ∫₀¹∫₀^(1−x) 1 dy dx and confirm it equals the area of the triangle.

> (a) 1/2
> (b) 1
> (c) 1/3
> (d) 2

> **Type:** MCQ `GATE-1`
> **Answer:** (a) 1/2 (Option a).
> **Solution:** Integrate in y first: ∫₀^(1−x) 1 dy = 1 − x, so the integral is ∫₀¹(1 − x) dx = 1 − 1/2 = 1/2. The region is the right triangle with legs of length 1 along the axes and hypotenuse x + y = 1, so its area is (1/2)(1)(1) = 1/2 ✓. Reversing the order gives ∫₀¹∫₀^(1−y) 1 dx dy = ∫₀¹(1 − y) dy = 1/2, agreeing as Fubini requires. This is the standard way to convert a geometric area question into an integral.
> **Key point:** ∫₀¹∫₀^(1−x) dy dx = ∫₀¹(1−x) dx = 1/2, the area of the unit right triangle with hypotenuse x + y = 1.

### Q232. `GATE-2`. How does a triple integral over a solid region of uniform density give the mass and the centre of mass?

> (a) Mass = ∫∫∫ ρ dV; centre of mass = (1/M)∫∫∫ (x, y, z) ρ dV
> (b) Mass = ∫∫∫ ρ² dV; centre of mass = ∫∫∫ ρ (x,y,z) dV
> (c) Mass = ∫∫∫ ρ dV and the centre of mass equals the centroid of the bounding box
> (d) Mass = ∫∫∫ dV / ρ

> **Type:** MSQ `GATE-2`
> **Answer:** (a).
> **Solution:** Mass is the integral of the density over the region, M = ∫∫∫_V ρ(x,y,z) dV, and the moments about the coordinate planes are M x̄ = ∫∫∫ xρ dV, M ȳ = ∫∫∫ yρ dV, M z̄ = ∫∫∫ zρ dV, so the centre of mass is the vector (1/M)∫∫∫ (x,y,z)ρ dV — the density-weighted mean position. For constant density the density cancels and the centre of mass is the geometric centroid, computed as in Q226. Option (b) has a spurious square in the mass; option (c) is false unless the region is a symmetric box; option (d) inverts the density.
> **Key point:** M = ∫∫∫ρ dV and (x̄,ȳ,z̄) = (1/M)∫∫∫(x,y,z)ρ dV; constant density ⇒ centroid.

### Q233. `GATE-2`. A uniform lamina of density 1 occupies the disk of radius 2. Find its mass and its moment of inertia about the z-axis.

> (a) Mass 4π, moment 8π
> (b) Mass 4π, moment 4π
> (c) Mass 2π, moment 4π
> (d) Mass 4π, moment 16π

> **Type:** MCQ `GATE-2`
> **Answer:** (a) Mass 4π, moment of inertia 8π (Option a).
> **Solution:** With density 1 the mass is the area, M = π(2)² = 4π, which polar coordinates confirm: ∫₀^2π∫₀² r dr dθ = 2π·2 = 4π. The moment about the z-axis is I_z = ∫∫ (x² + y²) ρ dA = ∫₀^2π∫₀² r²·r dr dθ = 2π ∫₀² r³ dr = 2π·(16/4) = 8π. Check against the disc formula I_z = (1/2)MR² = (1/2)(4π)(4) = 8π ✓. Option (b) is the perimeter rather than the area-like slip of halving twice, and option (c) uses the semicircular area.
> **Key point:** Disc radius R, density 1: M = πR² = 4π, I_z = ½MR² = 8π; in polar, I_z = ∫₀^2π∫₀² r³ dr dθ.

---

## Quick revision

- Matrix order m × n means m rows, n columns; (AB)_ij = Σ_k a_ik b_kj, so AB needs matching inner dimensions, and the product is (rows of A) × (columns of B).
- Transpose swaps indices: (Aᵀ)_ij = a_ji; the trace tr A = Σa_ii is defined only for square matrices, and tr(AB) = tr(BA).
- (A + B)ᵀ = Aᵀ + Bᵀ, (AB)ᵀ = BᵀAᵀ (order reverses), and (Aᵀ)ᵀ = A.
- A real matrix is symmetric if A = Aᵀ, skew-symmetric if A = −Aᵀ (so all diagonal entries vanish), Hermitian if A = A* (its diagonal is real).
- det(A − λI) = 0 is the characteristic equation; n roots over ℂ counted with multiplicity. det(λI − A) = (−1)ⁿ det(A − λI).
- det(AB) = det A · det B, det Aᵀ = det A, det(kA) = kⁿ det A; det A⁻¹ = 1/det A, and det A = 0 ⟺ A is singular.
- det A = 0 if and only if two rows (or columns) of A are linearly dependent — a quick structural check before expanding.
- Row operations change the determinant: swap rows negates it, scaling a row by k multiplies it by k, adding a multiple of one row to another leaves it unchanged.
- Laplace expansion: det A = Σ_j a_ij C_ij along any row i, where C_ij = (−1)^(i+j) M_ij; the cofactor matrix is the transpose of the adjugate.
- adj A = Cᵀ, A adj A = det A · I, and A⁻¹ = adj A/det A.
- Triangular A: det A = product of diagonal entries; eigenvalues are the diagonal entries; inverse exists iff no diagonal entry is zero.
- Rank: maximum number of linearly independent rows or columns; rank A = rank Aᵀ, and rank A ≤ min(m, n).
- Rank = number of non-zero rows in RREF = number of pivots = number of non-zero singular values = number of non-zero diagonal entries of U in a QR factorisation.
- A row-reduced matrix is in echelon form when every leading entry is to the right of the one above and every pivot is 1; in RREF it is also the only entry in its column and pivots move left.
- A square matrix is invertible ⟺ rank n ⟺ RREF = I ⟺ det ≠ 0 ⟺ no zero pivot during elimination.
- An m × n matrix has rank r with n − r free variables in Ax = b; for m = n the rank is n − k where k is the number of free variables.
- Rouché–Capelli: Ax = b is consistent ⟺ rank A = rank[A|b]; inconsistency is certified by a row of the form [0 … 0 | c] with c ≠ 0.
- Homogeneous system Ax = 0: trivial solution only iff det A ≠ 0; otherwise the solution space has dimension n − rank A, a basis of which comes from the free variables.
- Ax = b has a unique solution iff A is square with det A ≠ 0; if singular it has either no solution or infinitely many.
- Cramer's rule: x_i = D_i/D with D = det A and D_i obtained by replacing column i by b; it applies only to square systems with D ≠ 0.
- Independent vectors: v₁, …, v_k are dependent iff scalars c_i, not all zero, satisfy Σ c_i v_i = 0; n vectors in Rⁿ form a basis iff det[v₁ … vₙ] ≠ 0.
- A basis spans the space and is linearly independent; any two bases of the same space have the same size, called the dimension.
- dim row space = dim col space = rank A; dim N(A) = n − rank A; dim N(Aᵀ) = m − rank A (rank–nullity, twice).
- Fundamental subspaces: row space ⊂ Rⁿ, column space ⊂ Rᵐ, N(A) ⊂ Rⁿ, N(Aᵀ) ⊂ Rᵐ; row space ⊥ N(A) and col space ⊥ N(Aᵀ).
- For a full-column-rank 3 × 4 matrix of rank 2: dim row = 2, dim col = 2, dim N(A) = 2, dim N(Aᵀ) = 1.
- λ is an eigenvalue with eigenvector v ≠ 0 if Av = λv; the eigenvectors for λ are exactly the non-zero vectors of N(A − λI).
- Algebraic multiplicity (root of the characteristic polynomial) is always ≥ geometric multiplicity (dim of the eigenspace).
- Σλᵢ = tr A and Πλᵢ = det A, both counted with algebraic multiplicity.
- Distinct eigenvalues ⇒ n independent eigenvectors ⇒ diagonalisable; real symmetric ⇒ orthogonally diagonalisable with real eigenvalues.
- Real skew-symmetric ⇒ purely imaginary eigenvalues in conjugate pairs, so odd order forces a zero eigenvalue.
- Eigenvalues of A², Aᵏ, A⁻¹, A + cI, cA are λᵢ², λᵢᵏ, 1/λᵢ, λᵢ + c, cλᵢ respectively; the eigenvectors of A are unchanged by A⁻¹ and by A + cI.
- A is diagonalisable ⟺ AM = GM for every λ ⟺ A = PΛP⁻¹ with P's columns an eigenbasis; then Aᵏ = PΛᵏP⁻¹.
- For a 2 × 2 matrix, λ = (a+d)/2 ± √[((a−d)/2)² + bc]; distinct roots mean immediate diagonalisability.
- Cayley–Hamilton: p(A) = 0 with p the characteristic polynomial, so every power reduces to a combination of I, A, …, A^(n−1).
- A⁻¹ = −(c₁A + c₂A² + … + c_(n−1)A^(n−1))/c₀ when p(λ) = λⁿ + … + c₀, and p(0) = c₀ = ±det A ≠ 0.
- For A = [[2,1],[1,3]]: A² − 5A + 5I = 0, so A² = 5A − 5I, A³ = 20A − 25I, and A⁻¹ = (5I − A)/5.
- The minimal polynomial m_A divides the characteristic polynomial, has the same roots, and its exponent of (λ − λᵢ) equals the size of the largest Jordan block at λᵢ.
- A real symmetric A is positive definite ⟺ xᵀAx > 0 for x ≠ 0 ⟺ all λᵢ > 0 ⟺ all leading principal minors > 0 (Sylvester's criterion).
- Positive semidefinite but not positive definite ⟺ A is singular with a zero eigenvalue ⟺ some x ≠ 0 gives xᵀAx = 0; test PSD with **all** principal minors ≥ 0, not just the leading ones.
- Signature is (number of positive, number of negative) eigenvalues; for symmetric A, det A < 0 in odd order means an odd number of negative eigenvalues.
- A = LDLᵀ exists iff A is SPD; pivots d_k = D_k/D_(k−1), so Cholesky doubles as a Sylvester-type test and costs half of LU.
- Cholesky: l_jj = √(a_jj − Σ_{k<j} l_jk²) with A = LLᵀ; solve Ax = b by forward then back substitution without forming A⁻¹.
- A = LU (or PA = LU) when a pivot is zero; L is unit lower triangular, U upper triangular, and det A = ±∏u_ii.
- A zero on U's diagonal signals a singular matrix, not a failed decomposition; elimination always produces a zero row for a singular matrix.
- A = QR always exists with Q orthogonal; least squares reduces to Rx = Qᵀb, and rank A = number of non-zero diagonal entries of R.
- Householder QR is numerically stable; classical Gram–Schmidt gives the same answer in exact arithmetic but loses orthogonality in floating point.
- A = UΣVᵀ with σᵢ = √λᵢ(AᵀA); σ₁ = ‖A‖₂, and κ₂(A) = σ₁/σ_r.
- The truncated SVD is the optimal rank-r approximation (Eckart–Young), with ‖A − A_r‖₂ = σ_(r+1) and ‖A − A_r‖_F = √(Σ_{i>r}σᵢ²).
- Schur: A = QTQ* with T upper triangular, always available; Jordan: A = PJP⁻¹ with block sizes giving the minimal polynomial exponents.
- f_x, f_y are partial rates with the other variable fixed; ∇f = (f_x, f_y) is perpendicular to level curves, and |∇f| is the maximum rate of increase.
- The chain rule: z_s = f_x x_s + f_y y_s, z_t = f_x x_t + f_y y_t, or in matrix form ∇_z = Jᵀ∇_f.
- The total differential df = f_x dx + f_y dy is the linear part of the change, while d(f_x) = f_xx dx + f_xy dy involves second partials.
- Clairaut: f_xy = f_yx when the mixed partials are continuous near the point; this is false without the hypothesis.
- Implicit differentiation: dy/dx = −F_x/F_y for F(x,y) = 0, and y'' = −(F_xx + 2F_xy y' + F_yy y'²)/F_y.
- Euler's theorem: for f homogeneous of degree n, x f_x + y f_y + z f_z = n f, so f = (x f_x)/n.
- The Jacobian J = ∂(u,v)/∂(x,y) must be non-zero for a change of variables; area transforms as dA_new = |J| dA_old, and dA_xy = (1/|J|) du dv.
- div F = P_x + Q_y + R_z is a scalar (net flux density) and curl F = (R_y − Q_z, P_z − R_x, Q_x − P_y) is a vector; F is conservative iff curl F ≡ 0 on a simply connected domain.
- An interior extremum requires ∇f = 0; the second derivative test uses D = f_xx f_yy − f_xy²: D > 0 with f_xx > 0 gives a minimum, D > 0 with f_xx < 0 a maximum, D < 0 a saddle, and D = 0 is inconclusive.
- On a closed bounded region, absolute extrema occur at interior critical points **or** on the boundary, and both are compared.
- Lagrange multipliers: ∇f = λ∇g with ∇g ≠ 0; with m constraints, ∇f = Σλᵢ∇gᵢ, and λ = df*/dc is the marginal rate of the optimal value.
- Max xy on x² + y² = 1 is 1/2 at x = y = 1/√2; max x²y on x + y = 1 is 4/27 at x = 2/3, y = 1/3; max xyz on x + y + z = 3 is 1 at (1,1,1).
- Fubini: the two iterated integrals agree for continuous (integrable) f; Tonelli extends this to non-negative f, allowing the value +∞.
- Polar: x = r cos θ, y = r sin θ, dA = r dr dθ, with the disk of radius a given by 0 ≤ r ≤ a, 0 ≤ θ ≤ 2π; the factor r is the most commonly omitted term.
- Cylindrical dV = r dr dθ dz; spherical dV = ρ² sin φ dρ dφ dθ with φ measured from the +z axis, giving V_ball(R) = 4πR³/3.
- Change of variables multiplies the integrand by |∂(x,y)/∂(u,v)|, the **reciprocal** of the Jacobian usually computed — the most frequent sign/factor error.
- Volume under z = f over D is ∫∫_D f dA; mass is ∫∫∫ρ dV and the centre of mass is (1/M)∫∫∫(x,y,z)ρ dV.
- Green's theorem: ∮(P dx + Q dy) = ∫∫(Q_x − P_y) dA, with Area = ½∮(x dy − y dx); reversing the order of integration requires describing the region with the new slicing.
- The centroid of a semicircle of radius R is 4R/(3π) from the diameter; a disc of radius R and density 1 has M = πR² and I_z = ½MR².
