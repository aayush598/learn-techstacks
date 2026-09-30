# Engineering Mathematics — Part 5: Vector Calculus, Fourier Series & GATE Drill Sets

> Part 5 of 5 of the GATE ECE Engineering Mathematics question bank · Questions 1–240 of this file
> Read this file top to bottom, in order; the earlier parts of this bank cover single-variable
> calculus and series, linear algebra, complex analysis, probability, and PDEs/variational calculus.

**Covers:** vector algebra and vector differentiation; line and surface integrals; Green's,
divergence and Stokes's theorems; cylindrical and spherical coordinates; Fourier series, their
properties, Parseval's identity and the Fourier integral; signal/Fourier-transform properties; and
six GATE-style drill sets built from all of it.

**Assumes:** partial derivatives, double and triple integrals, elementary line/surface integrals,
basic matrix algebra, and the elementary complex exponentials. No PDE theory is needed — the one
partial-differential equation solved here (the heat equation) is solved from
scratch by separation of variables.

**Volume:** 240 questions. Difficulty mix ≈ 15% recall, 20% quick application, 25% medium,
20% GATE 1-mark MCQ, 20% GATE 2-mark MCQ/NAT/MSQ.

---

## Section 1. Vector algebra: dot and cross products, triple products

### Q1. What does the dot product of two vectors measure?

> **Type:** Theory
> **Answer:** The scalar component of one vector along the other; equivalently the product of the two magnitudes times the cosine of the angle between them, **A**·**B** = |**A**||**B**|cos θ, so it is zero when they are perpendicular and has magnitude |**A**||**B**| only when they are parallel.
> **Solution:** Writing **A** = |**A**|**â** and **B** = |**B**|**b̂** with unit vectors **â**, **b̂**, the dot product is |**A**||**B**|(**â**·**b̂**) = |**A**||**B**|cos θ. If the components are A = (A₁, A₂, A₃) and B = (B₁, B₂, B₃), then **A**·**B** = A₁B₁ + A₂B₂ + A₃B₃. The result is a scalar, so a dot product can never be a vector.
> **Key point:** **A**·**B** = |**A**||**B**|cos θ is a scalar measuring projection length along **A**.

### Q2. Compute **A**·**B** for **A** = 2**i** − 3**j** + 4**k** and **B** = **i** + 5**j** − 2**k**, and find the angle between them.

> **Type:** Numerical
> **Answer:** **A**·**B** = −13, and the angle between them is θ = cos⁻¹(−13/√193) ≈ 158.8°.
> **Solution:** **A**·**B** = (2)(1) + (−3)(5) + (4)(−2) = 2 − 15 − 8 = −13. Magnitudes: |**A**| = √(4+9+16) = √29 ≈ 5.385, |**B**| = √(1+25+4) = √30 ≈ 5.477. Product = √870 ≈ 29.496. So cos θ = −13/29.496 = −0.4407, giving θ ≈ 158.8°. The negative dot product is the only thing that tells us the vectors point broadly opposite.
> **Key point:** A negative dot product means obtuse angle, not a sign error.

### Q3. State the geometric meaning of the cross product **A** × **B**.

> **Type:** Theory
> **Answer:** |**A** × **B**| = |**A**||**B**|sin θ is the area of the parallelogram with sides **A** and **B**, and the direction of **A** × **B** is the unit normal **n̂** = (**A** × **B**)/|**A** × **B**| found by the right-hand rule, perpendicular to both vectors.
> **Solution:** Since sin θ measures the component of **B** perpendicular to **A**, multiplying by |**A**| gives the height of the parallelogram over the base |**A**|, so the product is the base × height, i.e. the area. Direction follows from the right-hand rule: curl the fingers of the right hand from **A** toward **B** and the thumb gives **A** × **B**. Consequences: **A** × **B** is zero exactly when **A** ∥ **B**, and **A** × **B** = −(**B** × **A**).
> **Key point:** Cross product = area vector; it vanishes only for parallel vectors.

### Q4. Compute **A** × **B** for **A** = **i** − 2**j** + 3**k** and **B** = 4**i** + **j** − 2**k**.

> **Type:** Numerical
> **Answer:** **A** × **B** = **i** + 14**j** + 9**k**, with magnitude √278 ≈ 16.67.
> **Solution:** Expand the determinant: **A** × **B** = (A₂B₃ − A₃B₂)**i** + (A₃B₁ − A₁B₃)**j** + (A₁B₂ − A₂B₁)**k**. With A = (1, −2, 3) and B = (4, 1, −2): first component = (−2)(−2) − (3)(1) = 4 − 3 = 1; second = (3)(4) − (1)(−2) = 12 + 2 = 14; third = (1)(1) − (−2)(4) = 1 + 8 = 9. Magnitude = √(1 + 196 + 81) = √278 ≈ 16.67. Independent check: |A| = √14, |B| = √21, **A**·**B** = 4 − 2 − 6 = −4, so |A×B|² = 14·21 − 16 = 294 − 16 = 278 ✓.
> **Key point:** Verify cross products with |**A** × **B**|² = |**A**|²|**B**|² − (**A**·**B**)².

### Q5. Interpret the scalar triple product **A** · (**B** × **C**) geometrically.

> **Type:** Theory
> **Answer:** It is the signed scalar six times the volume of the parallelepiped with edges **A**, **B**, **C**; the magnitude of the parallelepiped is |**A** · (**B** × **C**)| and the signed tetrahedron volume is one sixth of it.
> **Solution:** **B** × **C** is the area vector of the parallelogram spanned by **B** and **C**, of magnitude |**B**||**C**|sin θ = the area of the base. Dotting with **A** multiplies that base area by the component of **A** along the normal, which is exactly the height, giving base × height = volume. In components **A**·(**B**×**C**) = |A₁ A₂ A₃; B₁ B₂ B₃; C₁ C₂ C₃|, the determinant. It is zero precisely when the three vectors are coplanar.
> **Key point:** Zero scalar triple product ⟺ the three vectors are coplanar.

### Q6. True or false: **A** · (**B** × **C**) = **B** · (**C** × **A**) = **C** · (**A** × **B**). What happens if the order of just two vectors is swapped?

> **Type:** Conceptual
> **Answer:** True; the three expressions are equal (cyclic permutations change nothing). Swapping any two vectors changes the sign, so **B** · (**A** × **C**) = −**A** · (**B** × **C**).
> **Solution:** Each expression is the same 3×3 determinant, just with rows cyclically permuted, and a 3-cycle is an even permutation so the determinant is unchanged. A single transposition (swapping any pair) is an odd permutation, so the determinant picks up a factor of −1. Geometrically the sign records the handedness of the ordered triple, so orientation matters even though the volume does not.
> **Key point:** Cyclic permutations keep the triple product; any transposition flips its sign.

### Q7. Evaluate **A** × (**B** × **C**) for **A** = **i** + 2**j** + 3**k**, **B** = 4**i** − **j**, **C** = 3**j** + 2**k**.

> **Type:** Numerical
> **Answer:** **A** × (**B** × **C**) = 48**i** − 18**j** − 4**k**.
> **Solution:** Use the "BAC − CAB" rule **A** × (**B** × **C**) = **B**(**A**·**C**) − **C**(**A**·**B**). Here **A**·**C** = 0 + 6 + 6 = 12 and **A**·**B** = 4 − 2 + 0 = 2. So the result = 12(4, −1, 0) − 2(0, 3, 2) = (48, −12, 0) − (0, 6, 4) = (48, −18, −4). Direct check: **B** × **C** = |**i** **j** **k**; 4 −1 0; 0 3 2| = (−2, −8, 12), and (1,2,3) × (−2,−8,12) = (24+24, −6−12, −8+4) = (48, −18, −4) ✓. The answer lies in the plane of **B** and **C**, as it must.
> **Key point:** **A** × (**B** × **C**) = **B**(**A**·**C**) − **C**(**A**·**B**), so the result is in the plane of **B**, **C**.

### Q8. Evaluate (**A** × **B**) × **C** for **A** = **i** + 2**j** + 3**k**, **B** = 4**i** − **j**, **C** = 3**j** + 2**k**, and check the answer against the rearrangement rule.

> **Type:** Numerical
> **Answer:** (**A** × **B**) × **C** = 51**i** − 6**j** + 9**k**.
> **Solution:** The rearrangement rule is (**A** × **B**) × **C** = **B**(**A**·**C**) − **A**(**B**·**C**), obtained by writing (A×B)×C = −C×(A×B) and applying the standard triple-product identity. Here **B**·**C** = (4)(0) + (−1)(3) + (0)(2) = −3 and **A**·**C** = (1)(0) + (2)(3) + (3)(2) = 12, so the result is 12(4, −1, 0) − (−3)(1, 2, 3) = (48, −12, 0) + (3, 6, 9) = (51, −6, 9) ✓. The direct determinant agrees: **A** × **B** = (3, 12, −9) and (3, 12, −9) × (0, 3, 2) = (24 + 27, −9 − 6, 9) = (51, −6, 9). The result lies in the plane of **A** and **B**, as it must.
> **Key point:** (**A** × **B**) × **C** = **B**(**A**·**C**) − **A**(**B**·**C**), and the result lies in the plane of **A** and **B**.

### Q9. [GATE-1] Which of the following expressions is a **scalar**?

> **Type:** MCQ
> **Answer:** **A** · (**B** × **C**) (Option b).
> **Solution:** (a) **A** × (**B** × **C**) is a cross product of two vectors, hence a vector. (b) the scalar triple product is a dot product, hence a scalar. (c) **A** × **B** is a vector, so (**A** × **B**) × **C** is a vector. (d) **A** + **B** is a vector. Only a dot product — and therefore a triple product ending in a dot — can return a scalar, since the cross product always rotates the plane spanned by its two arguments without changing their type.
> **Key point:** Only a dot product yields a scalar; any expression with a cross product at its outer level is a vector.

### Q10. [GATE-1] If **A** × **B** = **0** with both **A** ≠ **0** and **B** ≠ **0**, what must be true?

> **Type:** MCQ
> **Answer:** **A** and **B** are parallel (or antiparallel) (Option c).
> **Solution:** |**A** × **B**| = |**A**||**B**|sin θ = 0. Since neither magnitude vanishes, sin θ = 0, so θ = 0 or π: the vectors are collinear. Option (a) is the condition for a zero *dot* product, not a cross product. Option (b) is impossible: two nonzero vectors that are both parallel and perpendicular would have to be the zero vector. Option (d) is not implied — the direction of **A** × **B** is undefined when it is zero, not along **A**.
> **Key point:** **A** × **B** = 0 with **A**, **B** nonzero ⟺ **A** ∥ **B**.

### Q11. [GATE-2] If **A** = 2**i** + 3**j** + **k**, **B** = **i** − 2**j** + 3**k**, **C** = 3**i** + **j** − 2**k**, find **A** · (**B** × **C**).

> **Type:** NAT
> **Answer:** 42
> **Solution:** The scalar triple product is the determinant |2 3 1; 1 −2 3; 3 1 −2|. Expanding along the first row: 2[(−2)(−2) − (3)(1)] − 3[(1)(−2) − (3)(3)] + 1[(1)(1) − (−2)(3)] = 2(4 − 3) − 3(−2 − 9) + (1 + 6) = 2 + 33 + 7 = 42. So the parallelepiped volume is 42 and the corresponding tetrahedron (origin plus the three tips) has volume 42/6 = 7. The sign is positive, so the ordered triple (**A**, **B**, **C**) is right-handed.
> **Key point:** Expand a triple product as a 3×3 determinant along any row and the sign is automatic.

### Q12. Find the unit vector in the direction from the point (1, 2, 3) to the point (2, 4, 6).

> **Type:** Numerical
> **Answer:** (**i** + 2**j** + 3**k**)/√14 ≈ 0.267**i** + 0.535**j** + 0.802**k**.
> **Solution:** Direction vector = (2 − 1, 4 − 2, 6 − 3) = (1, 2, 3), whose magnitude is √(1 + 4 + 9) = √14 ≈ 3.742. Dividing gives the unit vector. A unit vector is defined by the requirement |**n̂**| = 1, and here √(0.0713 + 0.2857 + 0.6429) = √1 = 1 ✓. Direction is independent of any choice of length for the original vector, but it is reversed if the two points are swapped.
> **Key point:** Direction vector = Δposition, normalised to unit length.

### Q13. Find the scalar and vector projections of **A** = 2**i** + 3**j** + 6**k** onto **B** = **i** + 2**j** + 2**k**.

> **Type:** Numerical
> **Answer:** Scalar projection = 20/3 ≈ 6.667; vector projection = (20/9)(**i** + 2**j** + 2**k**) = 2.222**i** + 4.444**j** + 4.444**k**.
> **Solution:** |**B**| = √(1 + 4 + 4) = 3 and **A**·**B** = 2 + 6 + 12 = 20. The scalar (component) projection is **A**·**b̂** = 20/3. The vector projection is (**A**·**B**)/|**B**|² · **B** = 20/9 · **B**. Note the two differ by the factor |**B**| = 3: scalar projection is a length along the direction, vector projection is the actual projected vector. Both are negative-signed here only if **A**·**B** < 0; here the angle is acute.
> **Key point:** Scalar projection = **A**·**B̂**; vector projection = (**A**·**B**)/|**B**|² · **B**.

### Q14. [GATE-2] Two nonzero vectors **A** and **B** satisfy **A**·**B** = 0 and **A** × **B** = **0** simultaneously. Which statement is correct?

> **Type:** MCQ
> **Answer:** At least one of **A**, **B** must be the zero vector — so under the stated nonzero hypothesis no such pair exists (Option c).
> **Solution:** **A**·**B** = 0 says they are perpendicular; **A** × **B** = **0** says they are parallel. A nonzero vector can be both parallel and perpendicular to another only if the other is the zero vector, since two orthogonal directions cannot span one line. So option (a) (perpendicular) is only half the condition, option (b) (parallel) is only the other half, and option (d) contradicts itself. This is the classic trick: the two conditions are mutually exclusive for nonzero vectors.
> **Key point:** Dot zero ⟹ perpendicular, cross zero ⟹ parallel; both can hold only for a zero vector.

### Q15. Find the acute angle between the planes 2x − y + z = 3 and 3x + y − 2z = 5.

> **Type:** Numerical
> **Answer:** θ = cos⁻¹(3/√84) ≈ 70.89°.
> **Solution:** Normals are **n**₁ = (2, −1, 1) and **n**₂ = (3, 1, −2). **n**₁·**n**₂ = 6 − 1 − 2 = 3; |**n**₁| = √6 ≈ 2.449, |**n**₂| = √14 ≈ 3.742, product √84 ≈ 9.165. cos θ = 3/9.165 = 0.3273, so θ = 70.89°. If the dot product had come out negative the angle would be obtuse; the *acute* dihedral angle between the planes is 180° − 70.89° = 109.11° only if you insist on the supplementary convention — the standard GATE answer is the angle between the normals, here 70.89° up to the acute/supplementary choice.
> **Key point:** Angle between planes = angle between their normal vectors.

### Q16. [GATE-1] For **A** = 3**i** + 4**j** and **B** = **i** + 4**k**, which is larger: |**A** × **B**| or |**A**||**B** sin θ|?

> **Type:** Comparison
> **Answer:** They are exactly equal — both equal √416 ≈ 20.40.
> **Solution:** The identity |**A** × **B**| = |**A**||**B**|sin θ is a theorem, not an approximation, so a "comparison" question on these two is testing whether the student knows the identity rather than computing. Explicitly, **A** × **B** = (4·4 − 0·0, 0·1 − 3·4, 3·0 − 4·1) = (16, −12, −4), magnitude √(256 + 144 + 16) = √416 ≈ 20.40. Cross-check: |**A**| = 5, |**B**| = √17, **A**·**B** = 3, so |**A**|²|**B**|² − (**A**·**B**)² = 25·17 − 9 = 416 ✓.
> **Key point:** |**A** × **B**|² = |**A**|²|**B**|² − (**A**·**B**)² is the fastest way to get a cross-product magnitude.

### Q17. Show that the three vectors **A** = **i** + 2**j** + 3**k**, **B** = 3**i** − **j** + 2**k**, **C** = 7**i** + 0**j** + 7**k** are coplanar.

> **Type:** Numerical
> **Answer:** **A** · (**B** × **C**) = 0, so the three vectors are coplanar.
> **Solution:** The determinant is |1 2 3; 3 −1 2; 7 0 7| = 1[(−1)(7) − (2)(0)] − 2[(3)(7) − (2)(7)] + 3[(3)(0) − (−1)(7)] = −7 − 2(21 − 14) + 3(7) = −7 − 14 + 21 = 0. The scalar triple product vanishes, so the three vectors are linearly dependent and lie in a common plane. The reason is visible directly: **C** = **A** + 2**B** = (1 + 6, 2 − 2, 3 + 4) = (7, 0, 7), so **C** is a combination of **A** and **B** and cannot leave their plane.
> **Key point:** Three vectors are coplanar ⟺ their scalar triple product is zero.

### Q18. A constant force **F** = 3**i** − 4**j** + 12**k** N acts on a particle that moves in a straight line from (1, 2, 3) m to (4, 6, 3) m. What is the work done, and what does its sign tell you?

> **Type:** Numerical
> **Answer:** W = −7 J; the negative sign means the displacement has a component opposite to **F**, so the force does negative work overall.
> **Solution:** Work by a constant force along a straight path is **F**·**d** with **d** = (4 − 1, 6 − 2, 3 − 3) = (3, 4, 0) m, |**d**| = 5 m. W = (3)(3) + (−4)(4) + (12)(0) = 9 − 16 = −7 J. A negative value simply means the particle is, on net, moving somewhat against the force — here the displacement's 4 m **j**-component works against the −4 N **j**-component of the force. Work done *by* the force is negative, so work done *on* the particle by this agent is +7 J.
> **Key point:** Constant-force work = **F**·**d** in joules; sign reports direction relative to the force.

---

## Section 2. Vector differentiation: gradient, directional derivative, divergence, curl

### Q19. Define the gradient of a scalar field and state its geometric meaning.

> **Type:** Theory
> **Answer:** ∇f = (∂f/∂x)**i** + (∂f/∂y)**j** + (∂f/∂z)**k**; it is perpendicular to every level surface f = c through the point and points in the direction of steepest increase of f.
> **Solution:** Each component measures the rate of change of f per unit displacement along that axis, and the vector sum of these rates is the net rate along a general direction. Moving a distance ds in the direction **n̂** changes f by ∇f·**n̂** ds to first order, which is maximised when **n̂** = ∇f/|∇f|; hence ∇f is the steepest-ascent direction and |∇f| is the steepest rate. Since the level surface f = c is described by a constant, its tangent directions **t** satisfy ∇f·**t** = 0, i.e. ∇f is normal to it.
> **Key point:** ∇f is normal to level surfaces and points along steepest ascent; |∇f| is the maximum directional derivative.

### Q20. Compute ∇f for f = x²y + yz + x and evaluate it at the point (1, 1, 1).

> **Type:** Numerical
> **Answer:** ∇f = (2xy + 1, x² + z, y); at (1,1,1), ∇f = (3, 2, 1).
> **Solution:** ∂f/∂x = 2xy + 1, ∂f/∂y = x² + z, ∂f/∂z = y. Substituting (1,1,1) gives 2(1)(1) + 1 = 3, 1 + 1 = 2, 1. Note that the two partial derivatives with respect to y and z are genuinely different expressions; treating "y + yz" as a single y-dependent term is the usual source of error here.
> **Key point:** Differentiate each term with respect to each variable separately, holding the others constant.

### Q21. Define the directional derivative of f at a point along a unit vector **u**.

> **Type:** Theory
> **Answer:** D**u**f = ∇f · **u** = u₁ ∂f/∂x + u₂ ∂f/∂y + u₃ ∂f/∂z; it is the limit as ds → 0 of [f(**r** + s**u**) − f(**r**)]/s, the rate of change of f per unit distance measured along the ray in direction **u**.
> **Solution:** The limit is exactly the chain rule applied to f(**r**(s)) with **r**′(s) = **u**, giving d/ds f = ∇f·**r**′(s), and evaluating at s = 0 gives the definition. Two special cases matter: **u** = **i** gives ∂f/∂x, and since |**u**| = 1 the result has units of f per unit length. Because D**u**f is the projection of ∇f onto **u**, it lies between −|∇f| and +|∇f| and equals +|∇f| only for **u** = ∇f/|∇f|.
> **Key point:** D**u**f = ∇f·**u**; it equals |∇f| only along ∇f itself.

### Q22. [GATE-1] The directional derivative of f = x² + 2y² + 3z² at the point (1, 1, 1) in the direction of the vector **i** + **j** + **k** is:

> **Type:** MCQ
> **Answer:** 12/√3 = 4√3 ≈ 6.928 (Option d).
> **Solution:** ∇f = (2x, 4y, 6z) = (2, 4, 6) at the point. The direction must first be normalised: |**i**+**j**+**k**| = √3, so **u** = (**i**+**j**+**k**)/√3. Then D**u**f = (2 + 4 + 6)/√3 = 12/√3 = 4√3 ≈ 6.928. Option (a), 12, is the trap answer obtained by forgetting to normalise the direction — the directional derivative must be *per unit distance*, so an unnormalised direction vector gives the rate per √3 metres. |∇f| = √56 ≈ 7.483 bounds the answer, as it must.
> **Key point:** Always normalise the direction vector before computing a directional derivative.

### Q23. [GATE-1] In which direction does f = 2x² + 3y² − z² increase most rapidly at the point (1, −1, 1), and what is the maximum rate?

> **Type:** MCQ
> **Answer:** Direction (4, −6, −2)/√56 = (2, −3, −1)/√14, maximum rate |∇f| = √56 ≈ 7.483 (Option b).
> **Solution:** ∇f = (4x, 6y, −2z), and at (1,−1,1) this is (4, −6, −2). Since D**u**f = ∇f·**u** ≤ |∇f| by the Cauchy–Schwarz inequality, with equality only for **u** along ∇f, the direction of steepest increase is (2, −3, −1)/√14 and the rate is √(16 + 36 + 4) = √56 ≈ 7.483. Option (a) (using 2,6,2 in place of the correct partials) drops the minus signs; option (c) gives a direction of steepest *decrease*, which is −∇f/|∇f|; option (d) confuses the gradient with the Laplacian.
> **Key point:** Max rate of increase = |∇f|, direction = ∇f/|∇f|; steepest decrease is the negative of that.

### Q24. Evaluate the directional derivative of f = x³y + y²z at (1, 1, 1) in the direction of the unit vector **u** = (2**i** + 2**j** − **k**)/3.

> **Type:** Numerical
> **Answer:** D**u**f = (4 + 4 − 1)/3 = 7/3 ≈ 2.333.
> **Solution:** ∇f = (3x²y, x³ + 2yz, y²) = (3, 3, 1) at (1,1,1). The given direction is already a unit vector: |(2,2,−1)| = √9 = 3 ✓. So D**u**f = (3)(2/3) + (3)(2/3) + (1)(−1/3) = 2 + 2 − 1/3 = 7/3 ≈ 2.333. The result is well inside the bound |∇f| = √19 ≈ 4.359, as a directional derivative must be.
> **Key point:** Check your direction vector is a unit vector before dotting it with ∇f.

### Q25. [GATE-2] A surface is defined by g(x, y, z) = x² + 2y² + 3z² = 14. Find a unit normal to the surface at the point (1, 2, 2).

> **Type:** NAT
> **Answer:** (2, 8, 12)/√212 = (1, 4, 6)/√53 ≈ 0.137**i** + 0.550**j** + 0.824**k**.
> **Solution:** The surface is a level surface of g, so the normal is ∇g = (2x, 4y, 6z), which at (1,2,2) is (2, 8, 12), magnitude √(4 + 64 + 144) = √212 = 2√53 ≈ 14.56. Dividing gives the unit normal, equivalently (1, 4, 6)/√53. The point does lie on the surface: 1² + 2(2²) + 3(2²) = 1 + 8 + 12 = 21, so the level value must be 21. The normal direction depends only on the point, not on the constant c.
> **Key point:** The unit normal to a level surface f = c at a point is ∇f/|∇f|, independent of the value of c.

### Q26. Define the divergence of a vector field and state its physical meaning for a flow field.

> **Type:** Theory
> **Answer:** ∇·**F** = ∂F₁/∂x + ∂F₂/∂y + ∂F₃/∂z; for a velocity field it is the net volumetric source density (outflow minus inflow per unit volume), so ∇·**F** > 0 denotes a source and ∇·**F** < 0 a sink.
> **Solution:** Each partial measures the local stretching of the field's component along its own axis; adding them counts net outflow from an infinitesimal box of volume dV, which carries a net volume (∇·**F**)dV per unit time. A divergence-free field (**F** purely tangential, e.g. uniform rotation) transports fluid but creates none. The divergence theorem later integrates this local density over a volume to get the total flux through the bounding surface.
> **Key point:** Divergence is a scalar measuring local source strength; ∫∫∫ div **F** dV = total outward flux.

### Q27. Find the divergence of **F** = x²**i** + xy**j** + z**k**.

> **Type:** Numerical
> **Answer:** ∇·**F** = 3x + 1.
> **Solution:** ∇·**F** = ∂(x²)/∂x + ∂(xy)/∂y + ∂(z)/∂z = 2x + x + 1 = 3x + 1. Note the middle term: ∂(xy)/∂y = x, because x is held constant during that differentiation. A common wrong route keeps y and writes ∂(xy)/∂y = y, which would give 2x + y + 1.
> **Key point:** In ∇·**F**, each component is differentiated by its *own* coordinate.

### Q28. [GATE-1] The divergence of the field **F** = x**i** + y**j** + z**k** in three dimensions is:

> **Type:** MCQ
> **Answer:** 3 (Option c).
> **Solution:** ∇·**F** = ∂x/∂x + ∂y/∂y + ∂z/∂z = 1 + 1 + 1 = 3. This field is the position vector itself, so it is the "radial expansion" field and its divergence is the space dimension. Option (a) 0 is the divergence of a *unit* radial field **r̂** = **r**/r, which does vanish away from the origin; option (b) 1 counts only one term; option (d) is the value of the curl, which is zero for this irrotational field.
> **Key point:** div(**r**) = 3 in 3-D, while div(**r̂**) = 0 away from the origin.

### Q29. [GATE-1] Which of the following statements are always true for a sufficiently smooth vector field **F** and scalar field f? (MSQ)

> **Type:** MSQ
> **Answer:** (a), (b) and (d) are all correct.
> **Solution:** The options are (a) ∇·(∇ × **F**) = 0, (b) ∇ × (∇f) = **0**, (c) ∇(∇·**F**) = ∇·(∇ × **F**), (d) ∇ × (∇ × **F**) = ∇(∇·**F**) − ∇²**F**. Option (a) holds because the two terms of the divergence of a curl are the same mixed partial with opposite signs. Option (b) holds by the same Clairaut argument as (a). Option (c) is false: the right side is identically zero while the left side is generally nonzero, e.g. for **F** = (x², 0, 0) in one dimension of dependence, ∇(∇·**F**) = ∇(2x) = 2 but the divergence of any curl is 0. Option (d) is the standard vector identity obtained by expanding the double curl in indices. So (a), (b), (d) are correct.
> **Key point:** div(curl **F**) = 0 and curl(grad f) = 0 are the two mixed-partial-commutation identities.

### Q30. Compute the curl of **F** = 2xy**i** + 3yz**j** + 4zx**k** and its magnitude at (1, 1, 1).

> **Type:** Numerical
> **Answer:** ∇ × **F** = −3y**i** − 4z**j** − 2x**k**, with magnitude at (1,1,1) equal to √29 ≈ 5.385.
> **Solution:** ∇ × **F** = (∂F₃/∂y − ∂F₂/∂z, ∂F₁/∂z − ∂F₃/∂x, ∂F₂/∂x − ∂F₁/∂y) = (0 − 3y, 0 − 4z, 0 − 2x). At (1,1,1) the vector is (−3, −4, −2), magnitude √(9 + 16 + 4) = √29 ≈ 5.385. All three off-diagonal terms vanish because each component of **F** is missing one variable, so only the ∂F₂/∂z, ∂F₃/∂x, ∂F₁/∂y terms survive, each with a minus sign.
> **Key point:** curl components are (R_y − Q_z, P_z − R_x, Q_x − P_y) for **F** = P**i** + Q**j** + R**k**.

### Q31. [GATE-2] Is the field **F** = y**i** + z**j** + x**k** conservative?

> **Type:** MCQ
> **Answer:** No — ∇ × **F** = −(**i** + **j** + **k**) ≠ **0**, so it is not conservative (Option b).
> **Solution:** ∇ × **F** = (∂F₃/∂y − ∂F₂/∂z, ∂F₁/∂z − ∂F₃/∂x, ∂F₂/∂x − ∂F₁/∂y) = (0 − 1, 0 − 1, 0 − 1) = (−1, −1, −1), which is never zero. Since the domain is all of R³, simply connected, the necessary and sufficient test is the vanishing of the curl; it fails, so no potential function exists. Option (a) is the wrong test (divergence = 0 here, but that means solenoidal, not conservative); option (c) is right about the divergence but irrelevant to conservativeness; option (d) claims a constant curl, which is indeed true but does not restore a potential.
> **Key point:** On all of R³, conservative ⟺ curl is identically zero; divergence says nothing about it.

### Q32. Show that ∇ × (∇f) = **0** for a twice-differentiable scalar f, and state one assumption needed.

> **Type:** Theory
> **Answer:** Each component of the curl, e.g. (∇ × ∇f)ₓ = ∂²f/∂y∂z − ∂²f/∂z∂y = 0, and similarly for the other two; the assumption is that the mixed partial derivatives of f exist and are continuous (f ∈ C²).
> **Solution:** Expand: (∇ × ∇f) = (∂²f/∂y∂z − ∂²f/∂z∂y, ∂²f/∂z∂x − ∂²f/∂x∂z, ∂²f/∂x∂y − ∂²f/∂y∂x). Clairaut's theorem (equality of mixed partials for C² functions) makes each bracket zero. The continuity requirement matters: for a function with discontinuous mixed partials (a classic pathological example) the curl of the gradient can be nonzero.
> **Key point:** curl(grad f) = 0 follows from equality of mixed partials, valid for f ∈ C².

### Q33. Verify numerically that ∇·(∇ × **F**) = 0 for **F** = y**i** + 2z**j** + 3x**k**.

> **Type:** Numerical
> **Answer:** ∇ × **F** = (−2, −3, −1), whose divergence is −2·0 + (−3)·0 + (−1)·0 = 0 ✓.
> **Solution:** With P = y, Q = 2z, R = 3x: (∇ × **F**) = (∂R/∂y − ∂Q/∂z, ∂P/∂z − ∂R/∂x, ∂Q/∂x − ∂P/∂y) = (0 − 2, 0 − 3, 0 − 1) = (−2, −3, −1). Its divergence is ∂(−2)/∂x + ∂(−3)/∂y + ∂(−1)/∂z = 0 + 0 + 0 = 0. Notice each component of the curl is a constant, which is why the divergence vanishes here term by term; in general the cancellation is between mixed partials of different components of **F**.
> **Key point:** div(curl) = 0 always — an immediate check that each curl component's own-variable derivative cancels a mixed term.

### Q34. For **F** = 2xy**i** + 3yz**j** + 4zx**k**, verify the identity ∇ × (∇ × **F**) = ∇(∇·**F**) − ∇²**F**.

> **Type:** Numerical
> **Answer:** Both sides equal 4**i** + 2**j** + 3**k**.
> **Solution:** ∇·**F** = 2y + 3z + 4x, so ∇(∇·**F**) = (4, 2, 3). The vector Laplacian acts component-wise: ∇²(2xy) = ∇²(3yz) = ∇²(4zx) = 0 since each term is linear in two variables and has zero second derivatives. Hence ∇²**F** = **0** and the right side is (4, 2, 3). Independently, ∇ × **F** = (−3y, −4z, −2x), so ∇ × (∇ × **F**) = (∂(−2x)/∂y − ∂(−4z)/∂z, ∂(−3y)/∂z − ∂(−2x)/∂x, ∂(−4z)/∂x − ∂(−3y)/∂y) = (0 + 4, 0 + 2, 0 + 3) = (4, 2, 3) ✓. Note ∇(∇·**F**) takes the partial in each coordinate: ∂(2y+3z+4x)/∂x = 4, not 2.
> **Key point:** ∇ × (∇ × **F**) = ∇(∇·**F**) − ∇²**F**, with ∇² acting component-wise.

### Q35. Give the SI units of gradient, divergence and curl of a field, using **F** in m/s and f in m².

> **Type:** Conceptual
> **Answer:** grad f has units m (since [m²]/[m]); div **F** and curl **F** both have units s⁻¹ (since [m/s]/[m]).
> **Solution:** Gradient = change of field per unit distance, so units are [f]/length = m²/m = m. Divergence and curl both differentiate a vector field component with respect to a length, giving [m s⁻¹]/[m] = s⁻¹. That the two have identical dimensions is a useful check: the divergence theorem equates ∫∫∫(s⁻¹)(m³) = m³/s of flux against ∫∫∫ **F**·**n** dS = (m/s)(m²) = m³/s, consistent. Both also carry the same unit as a rate of rotation.
> **Key point:** [grad f] = [f]/length; [div F] = [curl F] = [F]/length.

### Q36. If **u** = cos θ **i** + sin θ **j** in the xy-plane, express the directional derivative of f along **u** in terms of f_x and f_y, and evaluate for f = x² + 3y² at (1, 1) with θ = 60°.

> **Type:** Numerical
> **Answer:** D**u**f = f_x cos θ + f_y sin θ; for the given data it is 2(0.5) + 6(0.8660) = 1 + 3√3 ≈ 6.196.
> **Solution:** ∇f = (2x, 6y) = (2, 6) at (1,1), and **u** = (cos 60°, sin 60°) = (0.5, 0.8660). Dot product = 2(0.5) + 6(0.8660) = 1 + 5.196 = 6.196 = 1 + 3√3. The check |∇f| = √40 ≈ 6.325 ≥ 6.196 confirms the direction is close to, but not exactly, the gradient direction (which is at θ = tan⁻¹(3) ≈ 71.57°).
> **Key point:** D**u**f = f_x cos θ + f_y sin θ; it peaks when tan θ = f_y/f_x.

### Q37. [GATE-1] For f = x² + y² + z², the direction of steepest ascent of f at any point is:

> **Type:** MCQ
> **Answer:** Radially outward, along the position vector (2x, 2y, 2z)/|∇f| (Option a).
> **Solution:** ∇f = 2(x, y, z) = 2**r**, so the gradient is parallel to the position vector everywhere except the origin, where it is zero. The steepest-ascent direction is therefore radially outward, and the steepest-ascent rate is 2r, which equals 2 times the distance from the origin. Option (b) (tangential) is the direction of steepest *descent* for the sphere, i.e. of the *decrease* of the surface distance; option (c) is the null direction; option (d) confuses the gradient with the radial unit vector itself, which omits the factor 2 and hence the correct rate.
> **Key point:** For a spherically symmetric f, ∇f is radial; max rate here is 2r.

### Q38. Verify that **F** = 2xy**i** + (x² + y²)**j** is the gradient of a scalar function, and find that function.

> **Type:** Numerical
> **Answer:** **F** = ∇f with f(x, y) = x²y + y³/3 + C.
> **Solution:** Seek f with f_x = 2xy, giving f = x²y + g(y). Then f_y = x² + g′(y), and matching F_y = x² + y² gives g′(y) = y², so g(y) = y³/3 + C. Check: ∂f/∂x = 2xy ✓ and ∂f/∂y = x² + y² ✓. Equivalently the curl is (∂F_y/∂x − ∂F_x/∂y) = 2x − 2x = 0, and on the whole plane that certifies conservativeness.
> **Key point:** Match F_y = ∂f/∂y = x² + g′(y) to find the leftover function of y.

### Q39. A particle moves along **r**(t) = (t, t², t³) m and f = 2xy + 3z m². Find df/dt at t = 1.

> **Type:** Numerical
> **Answer:** df/dt = 15 m²/s.
> **Solution:** Along a curve, df/dt = ∇f · d**r**/dt. With f = 2xy + 3z, ∇f = (2y, 2x, 3) = (2, 2, 3) at the point (1,1,1). The velocity is **r**′(t) = (1, 2t, 3t²) = (1, 2, 3) at t = 1, in m/s. Hence df/dt = 2(1) + 2(2) + 3(3) = 2 + 4 + 9 = 15 m²/s, since f is measured in m² and the velocity in m/s. The z-term 3z contributes 3·3 = 9, the largest share, because the curve's vertical speed is largest at t = 1.
> **Key point:** Total rate along a path = ∇f · **v**, the sum of ∂f/∂x v_x, ∂f/∂y v_y, ∂f/∂z v_z.

### Q40. [GATE-2] Compute the vector Laplacian ∇²**F** for **F** = 3x²**i** + 2y²**j** + 5z²**k**, and use it with the curl to show ∇ × (∇ × **F**) = **0**.

> **Type:** NAT
> **Answer:** ∇²**F** = 6**i** + 4**j** + 10**k**, ∇(∇·**F**) = 6**i** + 4**j** + 10**k**, and ∇ × (∇ × **F**) = **0**.
> **Solution:** The vector Laplacian differentiates each component with respect to all three variables: ∇²**F** = (∇²3x², ∇²2y², ∇²5z²) = (6, 4, 10). Also ∇·**F** = 6x + 4y + 10z, so ∇(∇·**F**) = (6, 4, 10). The identity then gives ∇ × (∇ × **F**) = (6,4,10) − (6,4,10) = **0**, which is right because ∇ × **F** = (0 − 0, 0 − 0, 0 − 0) = **0** directly, so ∇ × **0** = **0** ✓. The cancellation occurs because ∇·**F** is linear, so its gradient equals the componentwise Laplacian term for term.
> **Key point:** ∇²**F** is component-wise ∇²; for a field whose divergence is linear, ∇(∇·**F**) = ∇²**F**.

### Q41. State why the curl of a velocity field measures twice the local angular velocity of the fluid element.

> **Type:** Theory
> **Answer:** A rigid rotation with angular velocity **ω** produces a velocity field **F** = **ω** × **r**, and ∇ × (∐ **ω** × **r**) = 2**ω**, so curl = 2 × angular velocity.
> **Solution:** Writing out the components of **ω** × **r** and taking the curl, every term in which two different components of **ω** are mixed cancels, leaving 2(ω₁, ω₂, ω₃). Physically, the particle at **r** + δ**r** has velocity **F** + δ**F**, and the relative motion δ**F** = δ**r** × (∇ × **F**) is exactly a rigid rotation with angular velocity (1/2)∇ × **F**. The factor of two appears because a rotation by angle φ over a time Δt is a shear-like rate twice what either component alone would suggest.
> **Key point:** curl **F** = 2**ω** for rotational flow, so |curl|/2 is the local angular speed.

### Q42. [GATE-1] The flux of a constant vector **c** through a closed surface S is:

> **Type:** MCQ
> **Answer:** Zero, because the total outward flux of a constant field through any closed surface vanishes (Option c).
> **Solution:** ∇·**c** = 0, so the divergence theorem gives ∫∫∫ 0 dV = 0. Geometrically, whatever enters through one part of a closed surface leaves through another. Option (a) is the flux through a *plane* bounded by a curve, where the answer is **c**·**n̂** × area and is generally nonzero; option (b) confuses the flux with the divergence; option (d) would only hold for a surface of volume zero.
> **Key point:** Flux of a constant vector through any closed surface is zero.

---

## Section 3. Line integrals: work, evaluation, orientation

### Q43. Define the line integral of a vector field **F** along a curve C, and give its two most important interpretations.

> **Type:** Theory
> **Answer:** ∫_C **F**·d**r** = ∫ₐᵇ **F**(**r**(t))·**r**′(t) dt; it is the work done by **F** on a particle moving along C (units J when **F** is in N), and in the closed-loop case ∮C **F**·d**r** it is the circulation, which measures the local spinning tendency of the field around C.
> **Solution:** Parametrise C by **r**(t), a ≤ t ≤ b, and sum the tiny work increments **F**·(ds **t̂**) along the path; since ds **t̂** = **r**′(t) dt, this becomes the stated integral. Work is path dependent in general: it changes if the path changes, because the work also depends on how much of the displacement is along the force. For a closed loop the integral is independent of the starting point but changes sign if the traversal direction is reversed, and the circulation is large where the field curls around the enclosed region.
> **Key point:** ∫C **F**·d**r** = ∫ **F**·**r**′ dt is work in joules; reversing the path reverses its sign.

### Q44. Evaluate ∫_C (2x dx + 3y dy) along the parabola y = x² from (0, 0) to (1, 1).

> **Type:** Numerical
> **Answer:** 5/2 = 2.5.
> **Solution:** With y = x², dy = 2x dx, and x runs 0 → 1. The integral becomes ∫₀¹ (2x + 3x²·2x) dx = ∫₀¹ (2x + 6x³) dx = [x² + (3/2)x⁴]₀¹ = 1 + 1.5 = 2.5. The same field is conservative (curl-free), so this value is path independent — the closed-loop circulation of the same field is also 0.
> **Key point:** Parametrise the curve, express differentials in terms of one parameter, and integrate over its range.

### Q45. Evaluate ∫_C (2x dx + 3y dy) along the straight line from (0, 0) to (1, 1) and compare with Q44. What does the comparison prove?

> **Type:** Comparison
> **Answer:** Both give 5/2 = 2.5, so the line integral is path independent over this region and the field is conservative.
> **Solution:** Along the line, x = t, y = t with 0 ≤ t ≤ 1, so dx = dt, dy = dt, and ∫₀¹ (2t + 3t) dt = ∫₀¹ 5t dt = (5/2)t²|₀¹ = 2.5. Getting 2.5 on two different paths proves the integral depends only on the endpoints, which is the hallmark of a conservative field. The analytical reason is that the field is **F** = (2x, 3y) = ∇f with f = x² + (3/2)y², and ∫∇f·d**r** = f(end) − f(start) always.
> **Key point:** Two paths giving the same value proves path independence; equivalently curl **F** = 0.

### Q46. Compute the work done by **F** = 2x**i** + 3y**j** + 4z**k** N in moving a particle from (1, 1, 1) m to (2, 2, 2) m, and check against the potential-function method.

> **Type:** Numerical
> **Answer:** W = 13.5 J.
> **Solution:** The field is the gradient of φ = x² + (3/2)y² + 2z², so W = φ(2,2,2) − φ(1,1,1) = (4 + 6 + 8) − (1 + 1.5 + 2) = 18 − 4.5 = 13.5 J. Direct integration of the differential form: ∫(2x dx + 3y dy + 4z dz) from 1 to 2 in each variable = ∫₁²2x dx + ∫₁²3y dy + ∫₁²4z dz = (4 − 1) + (6 − 1.5) + (8 − 2) = 3 + 4.5 + 6 = 13.5. So the work is 13.5 J; the potential method and the direct method agree, and the result is positive because the field points outward from the origin throughout the path.
> **Key point:** Work by a conservative field = change in potential; here 13.5 J for the path along the diagonal.

### Q47. A force field is **F** = (3x²)**i** − 2xy**j** N. Find the work done in moving a particle from (1, 0) m to (2, 2) m along the path parametrised by **r**(t) = (t, t²), 0 ≤ t ≤ 2. Is the field conservative?

> **Type:** Numerical
> **Answer:** W = −17.6 J; the field is not conservative, since ∂(−2xy)/∂x = −2y ≠ 0 = ∂(3x²)/∂y.
> **Solution:** **r**(t) = (t, t²), **r**′(t) = (1, 2t). **F**(t) = (3t², −2t·t²) = (3t², −2t³). Dot product: 3t²·1 + (−2t³)(2t) = 3t² − 4t⁴. Integrate from 0 to 2: [t³ − (4/5)t⁵]₀² = 8 − (4/5)(32) = 8 − 25.6 = −17.6. The negative sign means the field opposes the motion over most of the path, which is possible because the work is path dependent for a non-conservative field. The planar curl is ∂Q/∂x − ∂P/∂y = −2y − 0 = −2y, nonzero except on the x-axis, so conservativeness is ruled out.
> **Key point:** Non-conservative fields give path-dependent work; here it came out negative (−17.6 J).

### Q48. Show that the line integral of a gradient field around any closed curve is zero.

> **Type:** Theory
> **Answer:** ∮C ∇f·d**r** = 0, because f returns to its starting value after a closed traversal.
> **Solution:** Break C into segments on which f is differentiable and apply the fundamental theorem on each: ∫C ∇f·d**r** = f(B) − f(A) for each segment, and the values telescope around the loop to f(A) − f(A) = 0. Formally, a continuous f with ∇f existing implies ∇f is conservative, so its closed-loop circulation vanishes regardless of shape. This is the statement that a conservative field has zero circulation, and it fails for non-conservative fields such as a rotational one with nonzero curl.
> **Key point:** ∮ ∇f·d**r** = 0 for every closed curve; the potential returns to its start.

### Q49. Evaluate ∮C (y dx − x dy) where C is the circle x² + y² = a² traversed counterclockwise.

> **Type:** Numerical
> **Answer:** −2πa².
> **Solution:** Parametrise x = a cos t, y = a sin t, 0 ≤ t ≤ 2π, so dx = −a sin t dt and dy = a cos t dt. The integrand is y dx − x dy = a sin t(−a sin t dt) − a cos t(a cos t dt) = −a²(sin²t + cos²t) dt = −a² dt. Integrating: −a²(2π) = −2πa². The sign reflects the counterclockwise orientation: reversing the traversal gives +2πa². Green's theorem confirms it: with P = y and Q = −x the planar curl is Q_x − P_y = (−1) − (1) = −2, so the integral is −2 × Area = −2πa² ✓. The factor of 2 is the tell that this integrand measures twice the signed area — the field (−x, y) has curl −2, not −1 — which is exactly why the standard area formula uses the field (−y, x) with curl +2.
> **Key point:** ∮(y dx − x dy) = −2πa² for CCW orientation; reversing direction flips the sign.

### Q50. [GATE-1] In Q49, if the circle is traversed clockwise instead, the line integral becomes:

> **Type:** MCQ
> **Answer:** +2πa² (Option c).
> **Solution:** The same curve, the same field, only the sense of traversal reversed. Since the integral is a sum of contributions proportional to ds along the curve, reversing the direction negates every increment, so the answer is the negative of the counterclockwise value: +2πa². Option (a) −2πa² is the counterclockwise result and the trap for those who ignore orientation; option (b) 0 would follow only if the field were conservative, which it is not; option (d) 2a² omits π, as if the loop subtended only one radian.
> **Key point:** Line integrals over a closed curve depend on orientation: reversing the sense negates the value.

### Q51. Find the length of the curve **r**(t) = (cos t, sin t, t), 0 ≤ t ≤ π.

> **Type:** Numerical
> **Answer:** π√2 ≈ 4.443.
> **Solution:** The arc length is ∫ₐᵇ|**r**′(t)| dt. Differentiating: **r**′(t) = (−sin t, cos t, 1), so |**r**′(t)| = √(sin²t + cos²t + 1) = √2. Hence length = ∫₀^π √2 dt = π√2 ≈ 4.443. Geometrically this is a half-turn of a helix with radius 1: the horizontal part has length π and each turn rises √2, giving the total π + π = 2π ≈ 6.283 over a full turn of 2π in t — consistent with the standard helix formula 2π√2 for t ∈ [0, 2π].
> **Key point:** Arc length = ∫|**r**′(t)| dt; for a helix of radius 1 the speed is constant √2.

### Q52. [GATE-1] The circulation ∮C **F**·d**r** of a field about C equals the flux of the curl of **F** through any surface S bounded by C, provided:

> **Type:** MCQ
> **Answer:** S is any surface (with matching orientation) whose boundary is C, and **F** is smooth on and inside S (Option b).
> **Solution:** That is precisely Stokes's theorem, and the word "any" carries the important content: the circulation does not depend on which spanning surface you choose. The orientation condition is that the direction of traversal of C is right-hand-rule consistent with the normal of S. Option (a) would only be true in a plane, where S is fixed up to the interior; option (c) imposes an unnecessary topological restriction — in R³ any closed curve bounds a surface; option (d) is the divergence theorem, which relates a volume integral to a closed-surface flux.
> **Key point:** Stokes: ∮C **F**·d**r** = ∬S (∇ × **F**)·d**S**, valid for any spanning S.

### Q53. Evaluate ∫_C (x²**i** + y²**j**)·d**r** along the curve x = t², y = t³, 0 ≤ t ≤ 1.

> **Type:** Numerical
> **Answer:** 2/3 ≈ 0.667.
> **Solution:** **r**(t) = (t², t³), **r**′(t) = (2t, 3t²). **F** = (t⁴, t⁶). The dot product is t⁴·2t + t⁶·3t² = 2t⁵ + 3t⁸. Integrating from 0 to 1: 2·(1/6) + 3·(1/9) = 1/3 + 1/3 = 2/3. Both terms are positive, consistent with the field components and the velocity components being positive throughout, so every contribution to the work adds up.
> **Key point:** Dot the field with **r**′(t) — components of like sign contribute, opposite signs subtract.

### Q54. Compare the value of ∮C (x dy − y dx) for a circle of radius a traversed once clockwise against the same integral for a circle of radius 2a traversed once clockwise.

> **Type:** Comparison
> **Answer:** The first is −2πa², the second is −8πa², so the larger-radius loop gives a value larger in magnitude by a factor of 4.
> **Solution:** Under the parametrisation x = R cos t, y = R sin t, the integrand x dy − y dx becomes R cos t (R cos t dt) − R sin t(−R sin t dt) = R²(cos²t + sin²t) dt = R² dt. Integrated counterclockwise (0 ≤ t ≤ 2π) this is +2πR², so clockwise it is −2πR². Hence radius a gives −2πa² and radius 2a gives −8πa². The magnitude scales as the enclosed area, i.e. as R², because both the arc length and the magnitude of the integrand grow with R.
> **Key point:** ∮(x dy − y dx) = −2πR² clockwise (+2πR² counterclockwise); magnitude scales as R².

---

## Section 4. Surface integrals and flux

### Q55. Define the flux of a vector field **F** through an oriented surface S, and explain the role of the orientation.

> **Type:** Theory
> **Answer:** Φ = ∫∫_S **F**·**n̂** dS, the total field passing through S per unit time in the direction of the unit normal; orienting S as "outward" (for a closed surface) or by the right-hand rule (for an open surface) fixes the sign.
> **Solution:** Write d**S** = **n̂** dS with **n̂** a unit normal, so Φ = ∫∫_S **F**·d**S**. Physically, if **F** is a velocity field, Φ is the volume of fluid crossing S per second; if **F** is force per unit area, Φ is the total force component along the normal. Because **F**·(**n̂**) is odd under reversal of **n̂**, the flux value is meaningless without an orientation — flipping the normal flips the sign. Parametrising, **n̂** dS = (**r**_u × **r**_v) du dv for the surface **r**(u, v).
> **Key point:** Flux = ∫∫ **F**·**n̂** dS, and its sign depends entirely on the chosen normal direction.

### Q56. Compute the flux of **F** = x**i** + y**j** + z**k** through the sphere x² + y² + z² = 4, normal outward.

> **Type:** Numerical
> **Answer:** 32π ≈ 100.5.
> **Solution:** **F** = **r**, so on the sphere of radius 2, **F**·**n̂** = |**r**| = 2 everywhere. The surface area is 4πR² = 4π(4) = 16π. Hence Φ = 2 · 16π = 32π ≈ 100.5. Check via the divergence theorem: ∇·**F** = 3, volume = (4/3)π(8) = 32π/3, product = 32π ✓.
> **Key point:** For **F** = **r** on a sphere of radius R, flux = R · 4πR² = 4πR³.

### Q57. [GATE-1] The flux of **F** = x**i** + y**j** + z**k** through the closed surface of the unit sphere is:

> **Type:** MCQ
> **Answer:** 4π ≈ 12.57 (Option b).
> **Solution:** On the unit sphere **F**·**n̂** = 1 everywhere, and the area is 4π(1)² = 4π. Equivalently, the divergence theorem gives ∭(3) dV = 3 · (4π/3) = 4π. Option (a) 1 is the value of the integrand **F**·**n̂**, forgetting to integrate over the surface; option (c) 3 is the divergence, not the flux; option (d) π corresponds to a hemisphere flux divided wrongly, or confusing the 2-D disk area π with the 3-D sphere's 4π.
> **Key point:** Flux = integrand × area; the integrand for **F** = **r** on radius R is R, not R².

### Q58. Find the total outward flux of the field **F** = (2x, 3y, 4z) through the closed spherical surface x² + y² + z² = 9, using the divergence theorem.

> **Type:** Numerical
> **Answer:** 324π ≈ 1018.
> **Solution:** ∇·**F** = 2 + 3 + 4 = 9, constant. The volume of the sphere of radius 3 is (4/3)π(27) = 36π. The divergence theorem gives Φ = ∫∫∫ 9 dV = 9 · 36π = 324π ≈ 1018. The key shortcut is that the divergence is a constant, so it can be pulled out of the volume integral and multiplied by the volume.
> **Key point:** If the divergence is a constant c, total flux = c × volume of the region.

### Q59. Compute the flux of **F** = (x², y², z²) through the sphere of radius 1, outward normal.

> **Type:** Numerical
> **Answer:** 0.
> **Solution:** ∇·**F** = 2x + 2y + 2z, so the divergence theorem gives Φ = 2∭(x + y + z) dV over the unit ball. Each of the three integrals vanishes by odd symmetry: x is antisymmetric under x → −x while the ball is invariant, so its integral is zero, and likewise for y and z. The direct surface check agrees: **n̂** = (x, y, z) on the unit sphere, so **F**·**n̂** = x³ + y³ + z³, and each cube integrates to zero over the sphere. The field is large on parts of the sphere but negative on others, and the cancellation is exact.
> **Key point:** Flux of (x², y², z²) through a sphere centred at the origin is 0 by odd symmetry.

### Q60. [GATE-2] Let S be the paraboloid z = 1 − x² − y² over the disk x² + y² ≤ 1, with upward normal. Find the flux of **F** = (x, y, z).

> **Type:** NAT
> **Answer:** 3π/2 ≈ 4.712
> **Solution:** Close the surface with the disk D at z = 0. On D the normal is −**k̂** and **F**·**n̂** = −z = 0, so the disk contributes no flux. Now ∇·**F** = 1 + 1 + 1 = 3, and the enclosed volume between the paraboloid and z = 0 is ∫∫_D (1 − x² − y²) dA = 2π∫₀¹(1 − r²) r dr = 2π(1/2 − 1/4) = π/2, so the total closed-surface flux is 3 · π/2 = 3π/2, all of it through S. Direct check: on the paraboloid **n̂** dS = (−z_x, −z_y, 1) dA = (2x, 2y, 1) dA, and with **F** = (x, y, z) and z = 1 − r² we get **F**·d**S** = 2x² + 2y² + z = 2r² + 1 − r² = 1 + r², so Φ = 2π∫₀¹(1 + r²) r dr = 2π(1/2 + 1/4) = 3π/2 ✓.
> **Key point:** To use the divergence theorem on an open surface, close it and subtract the flux through the added piece.

### Q61. Explain what happens to the sign of the surface integral if the orientation of the surface in Q60 is reversed, without recomputing.

> **Type:** Conceptual
> **Answer:** The sign flips: the flux becomes −3π/2 ≈ −4.712, because **n̂** → −**n̂** everywhere and the integrand **F**·**n̂** is odd in the normal.
> **Solution:** The integrand of the surface integral is **F**·(**n̂** dS); under a reversal of orientation, d**S** → −d**S** while **F** is unchanged, so the whole integral changes sign. The magnitude 3π/2 is invariant, so the two orientations give ±3π/2. This is why every theorem statement (Green, divergence, Stokes) is paired with an orientation convention; without it the answer is ambiguous up to sign.
> **Key point:** Reversing the orientation of a surface negates its flux — always state the orientation.

### Q62. Find the flux of the constant field **F** = 2**k̂** through the closed surface of a cube of side a centred at the origin.

> **Type:** Numerical
> **Answer:** 0.
> **Solution:** By the divergence theorem, Φ = ∭∇·**F** dV = 0, since a constant field has zero divergence. Geometrically, the flux out through the top face (2a²) exactly cancels the flux in through the bottom face (−2a²), and the four side faces each have a horizontal normal, so their flux is zero. The total is 0. Note the individual face fluxes are not zero — only the sum is — which is exactly why the closed surface formulation is the useful one.
> **Key point:** Constant field ⇒ zero total flux through any closed surface, though individual faces may differ.

### Q63. [GATE-1] If S is a sphere of radius R centred at the origin and **F** = (x, y, z) — i.e. **F** = **r** — the flux through S (outward) is:

> **Type:** MCQ
> **Answer:** 4πR³ (Option d).
> **Solution:** **F**·**n̂** = R everywhere on the sphere, and the area is 4πR², so the flux is R · 4πR² = 4πR³. Via the divergence theorem, ∇·**r** = 3 and the volume is (4/3)πR³, giving 3 · (4/3)πR³ = 4πR³ ✓. Option (a) 4πR² is the surface area, option (b) 3R² is a plausible "divergence × something" mix-up, and option (c) R³ forgets the 4π.
> **Key point:** Flux of **F** = **r** through radius-R sphere = 3 × volume = 4πR³.

### Q64. Compute the total flux of **F** = (x, y, 2z) through the closed surface of the unit sphere.

> **Type:** Numerical
> **Answer:** 16π/3 ≈ 16.76.
> **Solution:** ∇·**F** = ∂x/∂x + ∂y/∂y + ∂2z/∂z = 1 + 1 + 2 = 4, a constant, so by the divergence theorem Φ = 4 × volume of the unit ball = 4 · (4π/3) = 16π/3 ≈ 16.76. The anisotropy of the field (stronger in the z direction) shows up only in the value of the constant divergence; the geometric factor is always the volume of the enclosed region.
> **Key point:** For linear fields the divergence is a constant, so flux = (constant) × volume.

### Q65. For the field **F** = x**i** + y**j** + z**k** and the sphere of radius 1, give the SI units of the flux if **F** were instead interpreted as a mass flux density in kg/(m²·s). What would the flux mean physically?

> **Type:** Conceptual
> **Answer:** The flux would be 4π kg/s ≈ 12.57 kg/s, the total mass of material crossing the sphere per second.
> **Solution:** Units: [F][dS] = kg m⁻² s⁻¹ × m² = kg s⁻¹. The integrand on the unit sphere is 1 kg/(m²·s), and integrating over the 4π m² surface gives 4π kg/s. Physically, the divergence theorem applied to a density field states that the rate of mass leaving a volume equals the integral of the mass source density inside it, which is the conservation statement behind transport phenomena.
> **Key point:** Flux of a mass (or volume, or charge) density times area has units of that quantity per second.

### Q66. [GATE-2] Let S be the part of the sphere x² + y² + z² = 1 above the plane z = 1/2, with outward normal. Find the flux of **F** = (0, 0, z) through S.

> **Type:** MCQ
> **Answer:** 7π/12 ≈ 1.833 (Option a).
> **Solution:** Use the projection shortcut: for a field with only a vertical component, the flux through a graph z = g(x, y) is ∫∫ g dx dy over its projection. Here z = √(1 − r²) over the disk r ≤ √3/2, so Φ = 2π∫₀^{√3/2} √(1 − r²) r dr. Substituting u = 1 − r²: = 2π · (1/2)∫_{1/4}^{1} u^{1/2} du = π · (2/3)(1 − 1/8) = (2π/3)(7/8) = 7π/12 ≈ 1.833. Cross-check with the divergence theorem: close with the disk D at z = 1/2, where the flux is −(1/2)·π(3/4) = −3π/8; div **F** = 1 and the cap volume is πh²(1 − h/3) = π(1/4)(5/6) = 5π/24, so Φ_S = 5π/24 + 3π/8 = 5π/24 + 9π/24 = 7π/12 ✓.
> **Key point:** For a field with only a vertical component, flux through a graph surface is ∫∫ g(x,y) dx dy over the projection.

---

## Section 5. Green's theorem and planar divergence and curl

### Q67. State Green's theorem in circulation form, including the orientation condition.

> **Type:** Theory
> **Answer:** For a positively oriented (counterclockwise) simple closed curve C bounding a region R in the plane, ∮C (P dx + Q dy) = ∬R (∂Q/∂x − ∂P/∂y) dA, assuming P and Q have continuous first partial derivatives on R and its boundary.
> **Solution:** The left side is the circulation of the planar field **F** = (P, Q) around C; the right side is the flux of the scalar curl (2-D) through the region. "Positively oriented" means the interior stays on the left as you traverse C, which for a simple closed curve is counterclockwise. The regularity assumption is what allows the proof by breaking the region into small elements, each of which is a tiny square whose boundary circulation collapses to the flux of the curl through it. The theorem is the two-dimensional case of Stokes's theorem.
> **Key point:** Green's theorem: ∮(P dx + Q dy) = ∬(Q_x − P_y) dA for CCW-oriented C.

### Q68. [GATE-1] Green's theorem converts a line integral around a closed curve into:

> **Type:** MCQ
> **Answer:** A double integral of the planar curl (Q_x − P_y) over the enclosed region (Option c).
> **Solution:** The identity is ∮(P dx + Q dy) = ∬(Q_x − P_y) dA. Option (a), the divergence, is what the divergence theorem does in three dimensions over a closed surface, and the planar divergence P_x + Q_y is not the integrand here. Option (b) mixes the two theorems. Option (d) is a meaningless pairing: a line integral around C cannot become a line integral elsewhere. The sign flips if C is traversed clockwise, so the orientation must be stated.
> **Key point:** Green converts a closed line integral into a double integral of the planar curl, not the divergence.

### Q69. Use Green's theorem to evaluate ∮C (x³ dy) where C is the unit circle traversed counterclockwise.

> **Type:** Numerical
> **Answer:** 3π/4 ≈ 2.356.
> **Solution:** With P = 0 and Q = x³, the planar curl is Q_x − P_y = 3x², so the circulation is ∬_R 3x² dA over the unit disk. Using polar coordinates, x² = r²cos²θ, so ∬ 3r²cos²θ r dr dθ = 3[∫₀¹r³ dr][∫₀^2π cos²θ dθ] = 3(1/4)(π) = 3π/4. Direct check: x = cos t, y = sin t, dy = cos t dt, so ∫₀^2π cos³t cos t dt = ∫cos⁴t dt = 3π/4 ✓ (the standard full-period value ∫cos⁴ = 3π/4).
> **Key point:** ∮ x³ dy = ∬3x² dA; the disk's second moment ∫∫x² dA = π/4.

### Q70. Show that the line integral ∮C (y dx) around the unit circle counterclockwise equals −π, and verify with Green's theorem.

> **Type:** Numerical
> **Answer:** −π ≈ −3.142.
> **Solution:** Green's theorem: P = y, Q = 0, so Q_x − P_y = 0 − 1 = −1, and ∬(−1) dA over the unit disk = −1 · π = −π. Direct parametrisation: x = cos t, y = sin t, dx = −sin t dt, so ∫₀^2π sin t(−sin t) dt = −∫₀^2π sin²t dt = −π ✓. This is a clean illustration: the integrand is small in magnitude but nonzero everywhere along the circle, and the negative answer records that y is positive where the motion is leftward and negative where it is rightward.
> **Key point:** ∮ y dx = −(area) for CCW orientation, since the planar curl of (y, 0) is −1.

### Q71. Find the area enclosed by the curve x² + y² = a² using Green's theorem in flux form.

> **Type:** Numerical
> **Answer:** πa².
> **Solution:** Take the field (P, Q) = (0, x) in the circulation form: Q_x − P_y = 1 − 0 = 1, so ∮C (x dy) = ∬_R 1 dA = Area. Direct parametrisation of the circle: x = a cos t, y = a sin t, so dy = a cos t dt and ∫₀^2π (a cos t)(a cos t) dt = a² ∫cos²t dt = a²π ✓. So the area πa² is recovered purely as a line integral, which is the practical content of the area formula and underlies the shoelace formula.
> **Key point:** Area = ∮ x dy (CCW) = −∮ y dx; comes from Green with a unit integrand.

### Q72. [GATE-2] Evaluate ∮C (x² dy − 2xy dx) where C is the circle x² + y² = 1 traversed counterclockwise.

> **Type:** MCQ
> **Answer:** 0 (Option a).
> **Solution:** Identify P = −2xy (the coefficient of dx) and Q = x² (the coefficient of dy). The planar curl is Q_x − P_y = 2x − (−2x) = 4x, so the integral equals ∬_R 4x dA over the unit disk, which vanishes by odd symmetry in x. Splitting the disk into left and right halves makes this explicit: the x > 0 half contributes positively and the x < 0 half an equal and opposite amount. The nonzero options all come from sign or derivative slips, such as reading the curl as 2x − 2x = 0 times π instead of integrating a nonzero integrand.
> **Key point:** An integrand whose planar curl is odd about an axis integrates to zero over a symmetric region.

### Q73. Evaluate ∮C (x²y dx − xy² dy) around the triangle with vertices (0,0), (2,0), (0,2), counterclockwise, by direct line-by-line integration.

> **Type:** Numerical
> **Answer:** −8/3 ≈ −2.667.
> **Solution:** Traverse the three edges counterclockwise. Edge 1, (0,0) → (2,0): y = 0, so both terms vanish and the integral is 0. Edge 2, (2,0) → (0,2): x + y = 2, so y = 2 − x, x from 2 to 0; dy = −dx. Integrand: x²y dx − xy² dy = x²(2 − x) dx + x(2 − x)² dx = x(2 − x)[x + (2 − x)] dx = 2x(2 − x) dx. Integrating from 2 to 0: 2∫₂⁰(2x − x²) dx = 2[x² − x³/3]₂⁰ = 2(0 − (4 − 8/3)) = 2(−4/3) = −8/3. Edge 3, (0,2) → (0,0): x = 0, so again 0. Total = −8/3. Green's theorem confirms: Q_x − P_y = −y² − x², and ∬ over the triangle of −(x² + y²) = −2·(symmetric moment) = −8/3 for this triangle, since ∬x² dA = ∬y² dA = 4/3.
> **Key point:** For a polygon, split the boundary integral edge by edge; agreement with Green is the correctness check.

### Q74. Use Green's theorem to evaluate ∮C ((x² + y²) dy) around the unit circle counterclockwise, and identify the region property being used.

> **Type:** Numerical
> **Answer:** 0.
> **Solution:** With P = 0 and Q = x² + y², the planar curl is Q_x − P_y = 2x, so the circulation is ∬ 2x dA = 0 by odd symmetry in x over the unit disk. Parametrising directly: x² + y² = 1 on the circle, dy = cos t dt, so ∫₀^2π 1 · cos t dt = 0 ✓. The key property exploited is the left-right symmetry of the disk, which lets the x-odd integrand cancel in pairs. This is the standard "check the parity before integrating" shortcut for Green-type integrals.
> **Key point:** Before integrating Q_x − P_y over a symmetric region, check whether the integrand is odd in some variable — then the answer is 0.

### Q75. Green's theorem fails to apply directly to a region with a hole. What must be done, and what happens if the hole is ignored?

> **Type:** Conceptual
> **Answer:** Apply the theorem to the region between the boundaries with the inner boundary traversed clockwise; ignoring the hole and treating C as a single boundary gives the wrong answer, because the circulation around the inner boundary is an independent contribution that need not vanish.
> **Solution:** For an annulus-like region with outer curve C₁ and inner curve C₂, Green's theorem in its usable form is ∮C₁ **F**·d**r** + ∮C₂(reverse) **F**·d**r** = ∬R (Q_x − P_y) dA. Concretely, if the region is the annulus between radii 1 and 2, the theorem requires both boundary loops. Substituting a single contour that jumps across the gap, or omitting the inner loop, changes the enclosed region and hence the double integral, producing a wrong result. The same caveat appears for Green's theorem applied to non-simply-connected domains with non-zero curl.
> **Key point:** Regions with holes need both boundary components, the inner one traversed in the reverse sense.

### Q76. Compute the circulation of **F** = (x, y) around the unit circle counterclockwise using both the direct method and Green's theorem.

> **Type:** Numerical
> **Answer:** 0 by both methods.
> **Solution:** Green's theorem: the planar curl is Q_x − P_y = 1 − 1 = 0, so the circulation is 0. Direct: x = cos t, y = sin t, dx = −sin t dt, dy = cos t dt, so ∫₀^2π (cos t · (−sin t) + sin t · cos t) dt = 0. Both agree. The field is the gradient of (x² + y²)/2, so it is conservative and all closed-loop circulations vanish, which is the same statement.
> **Key point:** A field with identically zero planar curl has zero circulation around every closed loop.

### Q77. [GATE-2] The area of the region bounded by the astroid x^{2/3} + y^{2/3} = a^{2/3} is:

> **Type:** MCQ
> **Answer:** 3πa²/8 (Option c).
> **Solution:** Parametrise x = a cos³t, y = a sin³t, 0 ≤ t ≤ 2π, which traces the astroid once. Then Area = ∮ x dy = ∫₀^2π (a cos³t)(3a sin²t cos t) dt = 3a²∫cos⁴t sin²t dt. Over a full period, ∫₀^2π cos⁴t sin²t dt = 4∫₀^{π/2}cos⁴t sin²t dt = 4(π/32) = π/8, so Area = 3a²(π/8) = 3πa²/8. The value is 3πa²/8 ≈ 1.178a², less than the πa² ≈ 3.142a² of the circumscribed circle, as it must be.
> **Key point:** Area = ∮ x dy; for the astroid (parametrised by cos³t, sin³t) this gives 3πa²/8.

### Q78. State the flux form of Green's theorem and explain how it is obtained from the circulation form.

> **Type:** Theory
> **Answer:** ∮C (P dy − Q dx) = ∬R (P_x + Q_y) dA, where Q_y here plays the role of the "P" of the circulation form; equivalently the flux of **F** = (P, Q) across the positively oriented boundary equals the integral of the planar divergence.
> **Solution:** Start from the circulation form with the field (P, Q) replaced by (−Q, P): ∮(−Q dx + P dy) = ∬(∂P/∂x − ∂(−Q)/∂y) dA = ∬(P_x + Q_y) dA. The left side is ∫∫S **F**·**n̂** dS, the total outward flux of **F** across the boundary, and the right side is the integral of the planar divergence. The plus sign in P_x + Q_y versus the minus sign in Q_x − P_y of the circulation form is exactly what distinguishes the two forms.
> **Key point:** Flux form of Green: ∮(P dy − Q dx) = ∬(P_x + Q_y) dA — a plus, not a minus.

### Q79. [GATE-1] Green's theorem in flux form applied to **F** = (x, y) over the unit disk gives the flux through its boundary as:

> **Type:** MCQ
> **Answer:** 2π ≈ 6.283 (Option a).
> **Solution:** The planar divergence is P_x + Q_y = 1 + 1 = 2, so the flux is ∬ 2 dA = 2π. Direct check: the outward normal on the unit circle is **n̂** = (x, y), so **F**·**n̂** = x² + y² = 1 everywhere, and the flux equals the circumference 2π ✓. Note that the *circulation* of the same field around the unit circle is 0 while its flux is 2π: circulation involves the curl, flux involves the divergence, and for this field the curl is 0 while the divergence is 2.
> **Key point:** Flux = ∬(divergence); for **F** = (x, y) that is 2 × area = 2π over the unit disk.

### Q80. Show that Green's theorem implies the identity ∮C (y dx − x dy) = −2 × (area enclosed by C) for counterclockwise C.

> **Type:** Theory
> **Answer:** With P = y, Q = −x, the planar curl is Q_x − P_y = −1 − 1 = −2, so the circulation equals ∬(−2) dA = −2·Area.
> **Solution:** Substituting P = y and Q = −x into Green's theorem gives ∮(y dx − x dy) = ∬(−1 − 1) dA = −2 Area. The geometric reading is that y dx − x dy is the differential form whose closed-loop integral measures signed area; for the unit circle a direct computation gives −2π, which equals −2 × π as required. It is the basis of the shoelace formula and of Green's-theorem area computations such as the astroid area.
> **Key point:** ∮(y dx − x dy) = −2·Area for CCW orientation — a differential form that encodes area.

### Q81. Apply Green's theorem to compute ∮C (P dx + Q dy) with P = −y/(x² + y²) and Q = x/(x² + y²) around the unit circle. Why does Green's theorem fail here?

> **Type:** Numerical
> **Answer:** The circulation is 2π, and Green's theorem cannot be applied because the field is undefined at the origin, which lies inside C, violating the hypothesis of continuous partial derivatives on the region including the interior.
> **Solution:** Parametrise the unit circle: x = cos t, y = sin t, dx = −sin t dt, dy = cos t dt, and x² + y² = 1. Then P dx + Q dy = (−sin t)(−sin t) dt + (cos t)(cos t) dt = (sin²t + cos²t) dt = dt, so the integral is 2π. Green's theorem would need the planar curl, which on the punctured plane is (Q_x − P_y) = 0, incorrectly suggesting a value of 0. The failure is exactly the missing hypothesis: the origin is a singularity inside the contour, so the field is not continuous (indeed not defined) on the whole enclosed region. This is the standard counterexample showing the hypothesis is essential.
> **Key point:** Green's theorem needs P, Q continuous including the interior; a pole at the origin is the classic violation.

### Q82. [GATE-1] Green's theorem in flux form applied to the field **F** = (−y, x) over the unit disk gives the outward flux across the boundary as:

> **Type:** MCQ
> **Answer:** 0 (Option c).
> **Solution:** The planar divergence is P_x + Q_y = ∂(−y)/∂x + ∂(x)/∂y = 0 + 0 = 0, so the flux is ∬ 0 dA = 0. Direct check on the boundary: on the unit circle **n̂** = (x, y), so **F**·**n̂** = −xy + xy = 0 at every point, consistent. This is the counter-rotating "swirl" field, whose magnitudes are largest exactly where the normal is most nearly tangential, so inflow and outflow cancel pointwise. Its *circulation* around the same circle, by contrast, is 2π — curl and divergence answer different questions about the same field.
> **Key point:** For **F** = (−y, x) the divergence is 0 (no flux) but the curl is 2 (nonzero circulation).

---

## Section 6. Divergence theorem and Stokes's theorem

### Q83. State the divergence theorem in both surface and volume forms, with the orientation convention.

> **Type:** Theory
> **Answer:** For a closed surface S of outward unit normal **n̂** bounding a volume V, ∫∫S **F**·**n̂** dS = ∫∫∫V (∇·**F**) dV, where **F** is continuously differentiable on a neighbourhood of V; the outward orientation on the left is what makes the equality sign correct.
> **Solution:** The theorem says the total flux out of a closed surface equals the integral of the local source density inside it, so any volume with zero divergence throughout encloses no net source and has zero net flux. Reversing to inward normals on the left would give a minus sign. The hypotheses matter: the field must be defined and C¹ on all of V, not merely on S, which is why singular fields (a point charge's field at its own location, or a field with a 1/ρ singularity on an interior axis) are outside the domain of the theorem. The theorem is to surfaces and volumes what Green's theorem is to curves and planar regions.
> **Key point:** ∫∫_S **F**·**n̂** dS = ∫∫∫_V (∇·**F**) dV with outward normals; the field must be C¹ on the whole volume.

### Q84. Compute the total flux of **F** = (x, y, 2z) out of the sphere of radius 2 centred at the origin.

> **Type:** Numerical
> **Answer:** 128π/3 ≈ 134.0.
> **Solution:** The divergence is 1 + 1 + 2 = 4, a constant. The volume of the sphere of radius 2 is (4/3)π(8) = 32π/3, so the flux is 4 · 32π/3 = 128π/3 ≈ 134.0. Direct check on the surface: on the sphere of radius 2, **F** = (x, y, 2z) and **n̂** = (x, y, 2z)/2, so **F**·**n̂** = (x² + y² + 4z²)/2, which is not constant but integrates to the same total by the theorem.
> **Key point:** Constant divergence c ⇒ total flux = c × volume; here 4 × 32π/3 = 128π/3.

### Q85. [GATE-1] The total flux of **F** = (x, y, z) out of the cube of side 2 centred at the origin is:

> **Type:** MCQ
> **Answer:** 24 (Option b).
> **Solution:** ∇·**F** = 3, and the cube has volume 8, so the flux is 3 · 8 = 24. Face-by-face: on the face x = 1 the outward normal is **i** and **F**·**i** = 1 over an area of 4, giving 4; similarly each of the six faces contributes 4, and 6 × 4 = 24 ✓. For **F** = (x, y, z) the divergence is always 3, so the flux through *any* closed surface is 3 × volume — the shape is irrelevant.
> **Key point:** div(**r**) = 3, so flux through any closed surface = 3 × enclosed volume.

### Q86. Find the total flux of **F** = (x³, y³, z³) out of the unit sphere.

> **Type:** Numerical
> **Answer:** 12π/5 ≈ 7.540.
> **Solution:** ∇·**F** = 3x² + 3y² + 3z² = 3r², so the flux is ∫∫∫ 3r² dV = 3 ∫₀¹ r² (4πr² dr) = 12π ∫₀¹ r⁴ dr = 12π/5 ≈ 7.540. Here a parity argument would fail in a useful way: the divergence 3r² is even, so no cancellation occurs and the integral is purely radial. In spherical coordinates the volume element is r² sin θ dθ dφ, giving the extra r² that turns the integrand into r⁴.
> **Key point:** div(x³, y³, z³) = 3r², whose ball integral needs the r² volume factor: 12π/5 for the unit ball.

### Q87. [GATE-2] A vector field has divergence ∇·**F** = 6 inside a sphere of radius 3 and is divergence-free elsewhere. The total outward flux through the sphere is:

> **Type:** MCQ
> **Answer:** 216π ≈ 678.6 (Option c).
> **Solution:** By the divergence theorem, flux = ∫∫∫ (6) dV over the sphere, since the divergence vanishes outside and the sphere's interior is the relevant region. Volume = (4/3)π(27) = 36π, so the flux is 6 · 36π = 216π ≈ 678.6. The field's values on the surface are irrelevant — the theorem converts the surface problem into a volume one. Note that 6 · 36π = 216π, since 36 × 6 = 216.
> **Key point:** A constant divergence 6 through a sphere of radius 3 gives flux 6 × 36π = 216π.

### Q88. Compute the total flux of **F** = (xy, yz, zx) out of the sphere of radius 1.

> **Type:** Numerical
> **Answer:** 0.
> **Solution:** ∇·**F** = ∂(xy)/∂x + ∂(yz)/∂y + ∂(zx)/∂z = y + z + x, and each of x, y, z integrates to zero over the symmetric ball by oddness. Hence the total flux is 0 + 0 + 0 = 0. Unlike a field whose divergence is a sum of even powers, these are linear terms which are odd, so the cancellation is exact. This is a quick sanity test: any field whose divergence is odd about the origin integrates to zero over a sphere centred there.
> **Key point:** Flux of (xy, yz, zx) through a sphere at the origin is 0 because the divergence x + y + z is odd.

### Q89. State Stokes's theorem and identify the two ways its hypotheses can fail.

> **Type:** Theory
> **Answer:** ∮C **F**·d**r** = ∫∫S (∇ × **F**)·**n̂** dS, where C bounds S and the orientation of C is right-hand-rule consistent with the normal of S. It fails if **F** is not continuously differentiable on a neighbourhood of S, or if the field has singularities on, or inside, S.
> **Solution:** The statement is the surface generalisation of Green's theorem: the circulation around the boundary equals the flux of the curl through any spanning surface. The two failure modes are (i) a non-C¹ field, e.g. a velocity field with a vortex filament, and (ii) a singularity enclosed by C, where the surface integral depends on which S you pick because the field is undefined somewhere in between. The second mode is the three-dimensional analogue of the failure seen for a planar field with a hole in its domain. A further practical restriction: in this form S must be orientable, and for a surface with several boundary components the orientations must be consistent.
> **Key point:** Stokes: ∮C **F**·d**r** = ∫∫S curl **F**·d**S; fails for non-C¹ fields or for singularities on/inside S.

### Q90. [GATE-1] By Stokes's theorem, the line integral of a field around a closed curve equals:

> **Type:** MCQ
> **Answer:** The surface integral of the curl of the field over any surface bounded by the curve (Option b).
> **Solution:** Stokes's theorem is exactly ∮C **F**·d**r** = ∫∫S (∇ × **F**)·**n̂** dS. Option (a) is the divergence theorem. Option (c) is Green's theorem restricted to planar regions, which is the special case of Stokes when S lies in the xy-plane. Option (d) mixes the two. The "any surface" clause is the crucial content: the circulation is a property of the curve alone, not of the chosen surface, provided no singularity intervenes.
> **Key point:** Stokes equates a closed line integral to the flux of the curl over a spanning surface.

### Q91. Compute ∮C **F**·d**r** for **F** = (x, y, z) around the circle of radius a in the xy-plane, counterclockwise, using Stokes's theorem.

> **Type:** Numerical
> **Answer:** 0.
> **Solution:** ∇ × **F** = (∂z/∂y − ∂y/∂z, ∂x/∂z − ∂z/∂x, ∂y/∂x − ∂x/∂y) = 0 for every component, so the curl is **0** and hence the circulation is 0. Parametrising confirms it: **r**(t) = (a cos t, a sin t, 0), **r**′(t) = (−a sin t, a cos t, 0), **F** = (a cos t, a sin t, 0), and the dot product is −a²cos t sin t + a² sin t cos t = 0. The field is the gradient of (x² + y² + z²)/2, so its circulation around any loop vanishes.
> **Key point:** **F** = (x, y, z) has zero curl, so its circulation around every closed loop is 0.

### Q92. Compute ∮C **F**·d**r** for **F** = (0, 0, 2x) around the unit circle in the xy-plane, counterclockwise, using Stokes's theorem.

> **Type:** Numerical
> **Answer:** 2π ≈ 6.283.
> **Solution:** Choose S to be the unit disk in the z = 0 plane with normal **k̂**. The curl is (∂F_z/∂y − ∂F_y/∂z, ∂F_x/∂z − ∂F_z/∂x, ∂F_y/∂x − ∂F_x/∂y) = (0 − 0, 0 − 2, 0 − 0) = (0, −2, 0), whose **z**-component — the only one that survives the dot product with **k̂** — is zero. So the circulation is 0. Direct check: **F** = (0, 0, 2a cos t) while **r**′(t) = (−a sin t, a cos t, 0), and the dot product is 0 because the field has no in-plane component. So the circulation is 0, matching the curl computation. The trap here is expecting 2π: the x-dependence of F_z is irrelevant to an in-plane loop.
> **Key point:** For an in-plane loop only the z-component of the curl matters, and here it is 0.

### Q93. [GATE-2] Compute the flux of **F** = (3y, 0, 2x) out of the closed surface of the unit cube [0,1]³ using the divergence theorem.

> **Type:** NAT
> **Answer:** 5
> **Solution:** ∇·**F** = ∂(3y)/∂x + 0 + ∂(2x)/∂z = 0 + 0 + 0 = 0. So the total flux is 0. Face by face: on x = 0 the normal is −**i** and **F**·**n̂** = −3y, integrating over the unit square gives −3/2; on x = 1, +3y gives +3/2, and these cancel. On z = 0 and z = 1 the normals are ∓**k̂** and **F**·(∓**k̂**) = ∓2x, giving −1 and +1, which cancel. The y-faces and the remaining faces contribute zero. Total 0 ✓. The point of the question is that the field looks "active" on every face yet the net is zero, because each contribution has an opposite partner.
> **Key point:** Flux of (3y, 0, 2x) through a closed box is 0 since the divergence vanishes identically.

### Q94. Use the divergence theorem to find the total flux of **F** = (x + y, y + z, z + x) out of the sphere of radius 1.

> **Type:** Numerical
> **Answer:** 4π ≈ 12.57.
> **Solution:** ∇·**F** = 1 + 1 + 1 = 3, a constant, so the flux is 3 × volume of the unit ball = 3 · (4π/3) = 4π. The off-diagonal terms (x in the y-component, y in the z-component, z in the x-component) contribute nothing to the divergence because each depends only on coordinates other than its own. This is a common exam pattern: read off the diagonal coefficients 1, 1, 1, discard the off-diagonal terms.
> **Key point:** For **F** = (x+y, y+z, z+x) the divergence is 3; off-diagonal terms never contribute.

### Q95. Compare the flux of **F** = (x, y, z) through (i) a sphere of radius 1 and (ii) a cube of side 2, both centred at the origin.

> **Type:** Comparison
> **Answer:** The sphere gives 4π ≈ 12.57, the cube gives 24, so the cube's flux is larger by a factor of 24/(4π) = 6/π ≈ 1.910.
> **Solution:** The divergence of **F** is 3 everywhere, so the flux is 3 × volume. The sphere's volume is 4π/3, giving 4π ≈ 12.57; the cube's volume is 8, giving 24. The ratio is 8/(4π/3) = 6/π ≈ 1.910. The comparison is decided purely by volume because the divergence is uniform — a useful reminder that for uniform divergence the geometry of the surface never enters.
> **Key point:** For uniform divergence, flux ∝ enclosed volume: cube/sphere = 6/π ≈ 1.91.

### Q96. Find the total flux of the field **F** = (x², y², z²) out of the cube [−1, 1]³.

> **Type:** Numerical
> **Answer:** 24.
> **Solution:** ∇·**F** = 2(x + y + z), an odd function of each variable separately. Over the symmetric cube, ∫∫∫ x dV = ∫∫∫ y dV = ∫∫∫ z dV = 0, so the flux is 0. Face-by-face confirmation: on the face x = 1 the outward normal is **i** and **F**·**i** = 1 over an area of 4, giving 4; on x = −1 the normal is −**i** and **F**·(−**i**) = −1 · 4 = −4; the two cancel, and the same happens for the y and z pairs. Total = 0.
> **Key point:** div(x², y², z²) = 2(x+y+z) is odd, so flux through any region symmetric about all three planes is 0.

### Q97. [GATE-2] A sphere of radius 2 carries a uniform volume charge density ρ. Use Gauss's law (the divergence theorem for **F** = ρ/(4πε₀) **r̂**) to find the total charge enclosed.

> **Type:** NAT
> **Answer:** Q = 4π(2)³ρ/3 = 32πρ/3 C.
> **Solution:** Coulomb's law gives ∫∫S **E**·d**S** = Q_enclosed/ε₀, and **E** = ρ**r**/(3ε₀) inside a uniformly charged ball (obtainable by applying the divergence theorem to div **E** = ρ/ε₀ with **E** = Cr). The enclosed charge is simply ρ × volume = ρ · (4/3)π(2³) = 32πρ/3. Writing it via Gauss's law: ∫∫S **E**·d**S** = |**E**| · 4π(2²) with |**E**| = ρ(2)/(3ε₀) = 2ρ/(3ε₀), giving (2ρ/(3ε₀)) · 16π = 32πρ/(3ε₀) = Q/ε₀, so Q = 32πρ/3 ✓. This is the divergence theorem doing the work that direct integration of Coulomb's law would do much harder.
> **Key point:** Uniformly charged ball of radius R: Q = (4/3)πR³ρ, from ∫∫ **E**·d**S** = Q/ε₀.

### Q98. Compute ∮C **F**·d**r** for **F** = (−y, x, 0) around the unit circle in the xy-plane, counterclockwise, and compare with the same circulation around a circle of radius 2 in the same plane.

> **Type:** Numerical
> **Answer:** 2π ≈ 6.283 for the unit circle and 8π ≈ 25.13 for the radius-2 circle, so the larger loop's circulation is four times as large.
> **Solution:** Stokes's theorem with the planar disk: ∇ × **F** = (0 − 0, 0 − 0, 1 − (−1)) = (0, 0, 2), and the flux through a disk of radius R with normal **k̂** is 2 · πR². So the circulation is 2π for R = 1 and 2 · 4π = 8π for R = 2, a ratio of 4. The circulation grows as the *area* enclosed because the curl is constant and uniform. Direct parametrisation for R = 1 gives ∫(sin²t + cos²t) dt = 2π ✓.
> **Key point:** Constant curl z ⇒ circulation = 2πR², so doubling the radius quadruples the circulation.

### Q99. Explain why the total flux of any field through a closed surface is independent of the shape of the surface, provided the divergence is the same inside.

> **Type:** Theory
> **Answer:** Because the flux equals the volume integral of the divergence, and if the divergence is fixed then so is that volume integral; equivalently, two surfaces enclosing the same region can be joined by a closed surface on which the fluxes cancel.
> **Solution:** Take two surfaces S₁ and S₂ enclosing the same volume V. Glue them together (reversing one orientation) to form a closed surface S. Then ∫∫S₁ **F**·d**S − ∫∫S₂ **F**·d**S = ∫∫S **F**·d**S = ∫∫∫V div **F** dV, and the right side depends only on the field and the region, not on the surfaces chosen. So the difference of the two fluxes is zero and the fluxes are equal. This is the mathematical content of charge conservation and of "action equals reaction" for forces between enclosed bodies.
> **Key point:** Flux through a closed surface depends only on the enclosed field via ∫∫∫div **F** dV, not on the surface's shape.

### Q100. [GATE-1] Given ∇·**F** = 0 everywhere, the value of ∇×**F** at the centre of the unit ball is:

> **Type:** MCQ
> **Answer:** Cannot be determined from the given information (Option d).
> **Solution:** A zero divergence constrains only the net flux, never the rotation. Two smooth fields satisfy ∇·**F** = 0 everywhere in the ball: **F**₁ = **0**, whose curl is **0** at the centre, and **F**₂ = (−y, x, 0), whose divergence is ∂(−y)/∂y + ∂(x)/∂x + 0 = 0 + 0 + 0 = 0 and whose curl is (0, 0, ∂(x)/∂x − ∂(−y)/∂y) = (0, 0, 2), nonzero at the centre. Since both obey the hypothesis yet give different curls there, the curl at the centre is undetermined. What the hypothesis *does* fix is the flux: the divergence theorem forces the flux through any closed surface to be 0, which is a statement about net outflow, not about local rotation.
> **Key point:** div **F** = 0 constrains flux only; curl is an independent quantity (e.g. (−y, x, 0) is both solenoidal and rotational).

### Q101. Demonstrate surface independence in Stokes's theorem: compute the circulation of **F** = (−y, x, 0) around the unit circle in the xy-plane (counterclockwise) using (i) the flat disk and (ii) the upper hemispherical cap, and show both give the same value.

> **Type:** Numerical
> **Answer:** Both give 2π ≈ 6.283.
> **Solution:** The curl is (0, 0, 2). Over the flat unit disk with normal **k̂**, the flux is 2 · π(1)² = 2π. Over the upper hemispherical cap, the outward normal is radial, so **F**·**n̂** = 2cos θ and dS = sin θ dθ dφ, giving ∫₀^{2π}∫₀^{π/2} 2cos θ sin θ dθ dφ = 2π · 1 = 2π, since ∫₀^{π/2} 2cos θ sin θ dθ = 1. Combining the cap with the flat disk into a closed hemisphere confirms it: div(∇ × **F**) = 0, so the outward cap flux plus the inward disk flux is zero, and since the disk's inward flux is −2π, the cap's outward flux is 2π. Both spanning surfaces give 2π, so the circulation depends only on the curve.
> **Key point:** Stokes is surface independent: any spanning surface of the same curve gives the same circulation, and here both the disk and the hemisphere cap give 2π.

### Q102. Compute the total flux of **F** = (x, y, z) out of a hemisphere of radius 2 with the flat face in the xy-plane and outward normal, and relate it to the full sphere's flux.

> **Type:** Numerical
> **Answer:** 24π ≈ 75.40, exactly half of the full sphere's 32π.
> **Solution:** The divergence of **F** = (x, y, z) is 3, and the volume of a radius-2 hemisphere is (2/3)πR³ = (2/3)π(8) = 16π/3, so the flux is 3 · 16π/3 = 16π ≈ 50.27. Direct check: on the curved surface **F**·**n̂** = 2 everywhere and the curved area is 2πR² = 8π, giving 16π; on the flat disk at z = 0 the normal is −**k̂** and **F**·**n̂** = −z = 0, contributing nothing. The full radius-2 sphere has flux 3 · 32π/3 = 32π, and the hemisphere is exactly half of it because the field and the region are symmetric.
> **Key point:** Flux of **r** over a region = 3 × volume; a radius-2 hemisphere gives 16π, half the full sphere's 32π.

---

## Section 7. Orthogonal curvilinear coordinates: cylindrical and spherical

### Q103. Write the cylindrical coordinates (ρ, φ, z) in terms of x, y, z, and state the scale factors.

> **Type:** Theory
> **Answer:** ρ = √(x² + y²), φ = tan⁻¹(y/x), z = z; the scale factors are h_ρ = 1, h_φ = ρ, h_z = 1, so dV = ρ dρ dφ dz.
> **Solution:** Cylindrical coordinates wrap a right circular cylinder about the z-axis, with ρ the distance from the axis, φ the angle in the xy-plane measured from +x, and z the height. The scale factors h₁ = |∂**r**/∂ρ|, h₂ = |∂**r**/∂φ| = ρ, h₃ = |∂**r**/∂z| = 1 measure the metric: a small displacement is ds² = dρ² + ρ²dφ² + dz². The volume element is the product h₁h₂h₃ dρ dφ dz = ρ dρ dφ dz, because an arc of angle dφ at radius ρ has length ρ dφ, giving the extra factor ρ.
> **Key point:** Cylindrical scale factors (1, ρ, 1); the volume element is ρ dρ dφ dz.

### Q104. Compute the volume of the solid cylinder of radius a and height h using the cylindrical volume element.

> **Type:** Numerical
> **Answer:** πa²h.
> **Solution:** V = ∫₀^h ∫₀^{2π} ∫₀^a ρ dρ dφ dz = h · 2π · (a²/2) = πa²h. The factor ρ in the volume element is exactly what converts the double integral over the cross-sectional disk, πa², into the product of area and height. Omitting the ρ factor would give a²h, an error by the average radius 2a/3.
> **Key point:** V = ∫ρ dρ dφ dz; forgetting ρ underestimates by a factor 2/3 of the mean radius.

### Q105. Find the gradient of f = ρ²z in cylindrical coordinates.

> **Type:** Numerical
> **Answer:** ∇f = 2ρz **â**_ρ + ρ² **â**_z.
> **Solution:** The gradient in curvilinear coordinates is ∇f = **â**_ρ ∂f/∂ρ + **â**_φ (1/ρ) ∂f/∂φ + **â**_z ∂f/∂z. With f = ρ²z: ∂f/∂ρ = 2ρz and ∂f/∂z = ρ², while ∂f/∂φ = 0. So ∇f = 2ρz **â**_ρ + 0 + ρ² **â**_z. The same field in Cartesian form is (2xz, 2yz, x² + y²), because **â**_ρ = (x, y, 0)/ρ converts 2ρz**â**_ρ to (2xz, 2yz, 0) and ρ²**â**_z adds (0, 0, x² + y²) ✓.
> **Key point:** ∇f = Σ(1/hᵢ)∂f/∂uᵢ **â**_i; the 1/φ term carries the extra 1/ρ.

### Q106. Compute the divergence of **A** = ρ²**â**_ρ + ρz**â**_z in cylindrical coordinates.

> **Type:** Numerical
> **Answer:** 4ρ.
> **Solution:** The divergence formula is ∇·**A** = (1/ρ)∂(ρA_ρ)/∂ρ + (1/ρ)∂A_φ/∂φ + ∂A_z/∂z. Here A_ρ = ρ², A_φ = 0, A_z = ρz. First term: (1/ρ)∂(ρ³)/∂ρ = 3ρ. Second: 0. Third: ∂(ρz)/∂z = ρ. Total = 4ρ. Cartesian check: ρ²**â**_ρ = (ρx, ρy, 0) and ρz**â**_z = (0, 0, ρz), so ∂(ρx)/∂x = ρ + x²/ρ and ∂(ρy)/∂y = ρ + y²/ρ and ∂(ρz)/∂z = ρ; summing gives 3ρ + (x²+y²)/ρ = 3ρ + ρ = 4ρ ✓. The trap is writing ∂(ρx)/∂x as ρ, forgetting that ρ itself depends on x.
> **Key point:** div in cylindrical = (1/ρ)∂(ρA_ρ)/∂ρ + (1/ρ)∂A_φ/∂φ + ∂A_z/∂z; the outer ρ in (ρA_ρ) is essential.

### Q107. State the scale factors of the spherical coordinate system (r, θ, φ) with θ the polar angle from +z and φ the azimuth.

> **Type:** Theory
> **Answer:** h_r = 1, h_θ = r, h_φ = r sin θ, so dV = r² sin θ dr dθ dφ and ds² = dr² + r²dθ² + r²sin²θ dφ².
> **Solution:** A small radial displacement has length dr, a small polar displacement r dθ (an arc of a circle of radius r), and a small azimuthal displacement r sin θ dφ (an arc of a circle of radius r sin θ — the distance to the z-axis). The product h_r h_θ h_φ = r² sin θ is the volume element, generalising the polar case 2πρ dρ with the geometric factor. Note that sin θ collapses to zero at the poles, where the azimuthal scale factor degenerates because all points at φ are the same point.
> **Key point:** Spherical scale factors (1, r, r sin θ); dV = r² sin θ dr dθ dφ.

### Q108. Write the gradient of f = r³ cos θ in spherical coordinates.

> **Type:** Numerical
> **Answer:** ∇f = 3r² cos θ **â**_r − r² sin θ **â**_θ.
> **Solution:** ∇f = **â**_r ∂f/∂r + **â**_θ (1/r) ∂f/∂θ + **â**_φ (1/(r sin θ)) ∂f/∂φ. Here ∂f/∂r = 3r² cos θ, ∂f/∂θ = −r³ sin θ, ∂f/∂φ = 0. So ∇f = 3r² cos θ **â**_r − r² sin θ **â**_θ. Note the factor 1/r in the θ-component. Sanity check with Cartesian: cos θ = z/r, so f = r²z, and ∇(r²z) = (2xz, 2yz, x² + y²) = 2xz**x̂** + 2yz**ŷ** + r²**ẑ**; with **â**_r = sin θ cos φ, **x̂** + cos θ sin φ, **ŷ** + cos θ **ẑ** and **â**_θ = cos θ cos φ, cos θ sin φ, −sin θ, the spherical expression reproduces this ✓.
> **Key point:** Spherical ∇f = **â**_r f_r + **â**_θ (1/r)f_θ + **â**_φ (1/(r sin θ))f_φ.

### Q109. Compute the divergence of **A** = r³**â**_r + r sin θ**â**_θ in spherical coordinates.

> **Type:** Numerical
> **Answer:** 5r² + 2cos θ.
> **Solution:** ∇·**A** = (1/r²)∂(r²A_r)/∂r + (1/(r sin θ))∂(sin θ A_θ)/∂θ + (1/(r sin θ))∂A_φ/∂φ. With A_r = r³: (1/r²)∂(r⁵)/∂r = 5r². With A_θ = r sin θ: (1/(r sin θ))∂(r sin²θ)/∂θ = (1/(r sin θ))(2r sin θ cos θ) = 2 cos θ. Total = 5r² + 2 cos θ. The first term alone is where most errors happen: the factor r² belongs inside the derivative because the radial scale factors are 1 and r.
> **Key point:** div in spherical = (1/r²)(r²A_r)_r + (1/(r sin θ))(sin θ A_θ)_θ + (1/(r sin θ))A_φ,φ.

### Q110. Find the curl of **A** = (1/s) **â**_φ, where s = r sin θ is the distance from the z-axis, and interpret the result physically.

> **Type:** Numerical
> **Answer:** ∇ × **A** = **0** for s ≠ 0; the field is curl-free everywhere off the z-axis, with a singular line source on the axis itself.
> **Solution:** Convert to Cartesian: s**â**_φ = (−y, x, 0), so **A** = (−y, x, 0)/s² = (−y/s², x/s², 0). The curl's z-component is ∂(x/s²)/∂x + ∂(y/s²)/∂y = (s² − 2x²)/s⁴ + (s² − 2y²)/s⁴ = (2s² − 2(x²+y²))/s⁴ = 0, and the x- and y-components vanish because A_z = 0. This matches Ampère's law: a line current along the z-axis has curl zero at every point not on the axis, and the "missing" curl is concentrated on the axis as a delta function. It is also why Stokes's theorem cannot be applied to a loop that encircles the axis, since the field is not defined everywhere inside.
> **Key point:** **A** = (1/s)**â**_φ is curl-free off the z-axis; the singular source lies on the axis.

### Q111. [GATE-1] The volume element in spherical coordinates is:

> **Type:** MCQ
> **Answer:** r² sin θ dr dθ dφ (Option c).
> **Solution:** It is the product of the three scale factors h_r h_θ h_φ = 1 · r · r sin θ = r² sin θ. Option (a) r² alone omits the sin θ that comes from the shrinking azimuthal circles near the poles. Option (b) r sin θ is the two-dimensional area element of a spherical surface, missing one factor of r. Option (d) r³ is dimensionless in the wrong sense: comparing with the 2-D polar case, the extra factor comes from having three radial shells, not from an extra power of r.
> **Key point:** dV = r² sin θ dr dθ dφ = (product of scale factors) dq₁dq₂dq₃.

### Q112. [GATE-2] The Laplacian of f = 1/r in spherical coordinates (r ≠ 0) is:

> **Type:** MCQ
> **Answer:** 0 (Option b).
> **Solution:** The spherical Laplacian is ∇²f = (1/r²)(r²f_r)_r + (1/(r² sin θ))(sin θ f_θ)_θ + (1/(r² sin²θ))f_φ,φ. With f = 1/r: f_r = −1/r², so r²f_r = −1 and its radial derivative is 0; f is independent of θ and φ, so those terms vanish. Hence ∇²(1/r) = 0 for r ≠ 0 — the potential of a point charge is harmonic everywhere except at the source. In Cartesian terms this is the statement ∇²(1/√(x²+y²+z²)) = 0 away from the origin.
> **Key point:** ∇²(1/r) = 0 for r ≠ 0; the point charge is a singularity, not part of the harmonic region.

### Q113. Write the Laplacian of a scalar f in cylindrical coordinates.

> **Type:** Theory
> **Answer:** ∇²f = (1/ρ)∂/∂ρ(ρ f_ρ) + (1/ρ²) f_{φφ} + f_{zz}.
> **Solution:** The Laplacian is div(grad f), and applying the cylindrical gradient and then the cylindrical divergence component-wise gives the 1/ρ weight on the radial second derivative, the 1/ρ² weight on the azimuthal one, and no weight on ∂²/∂z². The structure is general: the coefficient on the i-th term is 1/(h₁h₂h₃) times ∂/∂qᵢ of ((h₁h₂h₃)/hᵢ² · ∂f/∂qᵢ). With h = (1, ρ, 1) the product h₁h₂h₃ = ρ, giving the 1/ρ and 1/ρ² weights.
> **Key point:** Cylindrical ∇²f = f_ρρ + (1/ρ)f_ρ + (1/ρ²)f_φφ + f_zz.

### Q114. Compute ∇²(r⁴) in spherical coordinates.

> **Type:** Numerical
> **Answer:** 20r².
> **Solution:** f = r⁴ depends only on r, so only the radial term survives: ∇²f = (1/r²)(r²f_r)_r = (1/r²)(4r³·r²)_r = (1/r²)(4r⁵)_r = 20r². In Cartesian terms, r⁴ = (x²+y²+z²)² and one can verify ∇²r⁴ = 20r² by direct expansion, which confirms the 20 = 4·5 coefficient pattern for rⁿ in 3-D: ∇²rⁿ = n(n+1)r^{n−2}.
> **Key point:** For a radial function in 3-D, ∇²rⁿ = n(n+1)r^{n−2}; here 4·5 = 20.

### Q115. [GATE-1] In cylindrical coordinates, the divergence of a purely azimuthal field **A** = A_φ(r) **â**_φ is:

> **Type:** MCQ
> **Answer:** 0 (Option a).
> **Solution:** The divergence's azimuthal term is (1/ρ)∂A_φ/∂φ, and since A_φ = A_φ(r) has no φ dependence this term is 0; the other two terms are absent because A_ρ = A_z = 0. The quantity (1/ρ)∂A_φ/∂ρ belongs to the *curl*, specifically its z-component, and it is what gives a nonzero circulation for the azimuthal field **A** = (1/ρ)**â**_φ. The option listing the radial derivative is the trap for those who swap the two roles.
> **Key point:** (1/ρ)A_φ,φ belongs to the divergence; (1/ρ)A_φ,ρ belongs to the curl's z-component.

### Q116. Compute the flux of the electrostatic field **E** = (kq/r²)**â**_r of a point charge at the origin through a sphere of radius R centred at the origin, using the spherical surface integral.

> **Type:** Numerical
> **Answer:** 4πkq ≈ 12.566kq.
> **Solution:** The outward normal is **â**_r and **E**·**n̂** = kq/r². With dS = r² sin θ dr dθ dφ, the integrand **E**·d**S** = kq sin θ dr dθ dφ, and ∫₀^R∫₀^π∫₀^{2π} kq sin θ dφ dθ dr = kq · R · 2 · 2π = 4πkq. The r² in the area element exactly cancels the 1/r² in the field, which is why the flux is independent of R. In SI units k = 1/(4πε₀), so this is q/ε₀, reproducing Gauss's law.
> **Key point:** dS = r² sin θ dθ dφ cancels the 1/r² of a point-charge field, giving radius-independent flux 4πkq.

### Q117. Compute the Laplacian of f = ρ³z in cylindrical coordinates.

> **Type:** Numerical
> **Answer:** 9ρz.
> **Solution:** The cylindrical Laplacian is ∇²f = f_ρρ + (1/ρ)f_ρ + (1/ρ²)f_φφ + f_zz. With f = ρ³z: f_ρ = 3ρ²z, f_ρρ = 6ρz, f_φφ = 0 and f_zz = 0 (since z appears only to the first power). Hence ∇²f = 6ρz + (3ρ²z)/ρ = 6ρz + 3ρz = 9ρz. In SI units this is m (the field is 9ρz in metres if ρ, z are lengths), consistent with [∇²] = m⁻¹ acting on a length.
> **Key point:** Cylindrical ∇²f = f_ρρ + (1/ρ)f_ρ + (1/ρ²)f_φφ + f_zz; here 6ρz + 3ρz = 9ρz.

### Q118. [GATE-2] In spherical coordinates, the curl's radial component of **A** = A_r **â**_r + A_θ **â**_θ + A_φ **â**_φ is:

> **Type:** MCQ
> **Answer:** (1/(r sin θ))[∂(sin θ A_φ)/∂θ − ∂A_θ/∂φ] (Option b).
> **Solution:** The three curl components in spherical coordinates are (∇ × **A**)_r = (1/(r sin θ))(∂(sin θ A_φ)/∂θ − ∂A_θ/∂φ), (∇ × **A**)_θ = (1/r)((1/sin θ)∂A_r/∂φ − ∂(rA_φ)/∂r), and (∇ × **A**)_φ = (1/r)(∂(rA_θ)/∂r − ∂A_r/∂θ). Note that the radial component carries the full 1/(r sin θ) weight, because the surface element perpendicular to **â**_r is r sin θ dθ dφ. Option (a) gives only the first term of the bracket; option (c) is the θ-component; option (d) swaps the roles of r and sin θ.
> **Key point:** (∇ × **A**)_r = (1/(r sin θ))[∂(sin θ A_φ)/∂θ − ∂A_θ/∂φ] — the weight is 1/(r sin θ).

### Q119. Give the SI units of the scale factors h_i in cylindrical and spherical coordinates, and why must they be dimensionless or have units of length?

> **Type:** Conceptual
> **Answer:** h_i has units of length, because h_i dq_i must be a displacement: for cylindrical, h = (1, ρ, 1) has units (1, m, 1); for spherical, h = (1, r, r sin θ) has units (1, m, m).
> **Solution:** The metric relation is ds² = Σ hᵢ² dqᵢ², and ds has units of length. Since dφ and dθ are pure angles (dimensionless), the corresponding scale factors must carry the units of length; this forces h_φ = ρ and h_θ = r, h_φ = r sin θ. The dimensionally consistent volume element dV = h₁h₂h₃ dq₁dq₂dq₃ = m³ confirms it. A common error is treating the Jacobian as a pure number, which is dimensionally impossible for a volume element.
> **Key point:** h_i must have units of length so that h_i dq_i is a displacement; dV = h₁h₂h₃ dq₁dq₂dq₃.

---

## Section 8. Fourier series: Dirichlet conditions, Euler's form, convergence

### Q120. Write the general Fourier series of a function f(x) defined on (−L, L).

> **Type:** Theory
> **Answer:** f(x) ~ a₀/2 + Σₙ₌₁^∞ [aₙ cos(nπx/L) + bₙ sin(nπx/L)], with aₙ = (1/L)∫₋ᴸᴸ f(x)cos(nπx/L) dx, bₙ = (1/L)∫₋ᴸᴸ f(x)sin(nπx/L) dx, and n₀ = π/L the fundamental angular frequency for a period 2L.
> **Solution:** The basis consists of cosines and sines of integer multiples of the fundamental frequency n₀ = π/L, chosen so the series is 2L-periodic. The constant term is written a₀/2 purely by convention, which matters when reading off a₀ from an integral. The series represents f(x) at points of continuity and the average of the left- and right-hand limits at jump discontinuities, so it is an equality only where the function is continuous. All coefficients decay to zero as n → ∞ (Riemann–Lebesgue), which is the practical content of convergence.
> **Key point:** Fourier basis on (−L, L) has n₀ = π/L and fundamental period 2L; the constant term is written a₀/2.

### Q121. State the Dirichlet conditions a function must satisfy for its Fourier series to converge pointwise.

> **Type:** Theory
> **Answer:** f must be periodic with period 2L, piecewise continuous on (−L, L) (only finitely many finite jumps), and piecewise smooth, so that ∫|f'| dx over (−L, L) is finite. Under these conditions the series converges to f(x) at points of continuity and to [f(x⁺) + f(x⁻)]/2 at jumps.
> **Solution:** The proof integrates the partial sum against a Dirichlet kernel and uses integration by parts once; the boundary terms vanish at every point where f is continuous because the "sawtooth" factor oscillates into a limit, and they survive as the average of the two one-sided values at a jump. Piecewise continuity rules out wild behaviour such as an infinite number of discontinuities, and the bounded variation implied by piecewise smoothness is what makes that average meaningful. The classical 50% overshoot near a jump (Gibbs phenomenon) persists no matter how many terms are summed, because the partial sums are continuous while f is not.
> **Key point:** Dirichlet conditions: periodic, piecewise continuous, piecewise smooth; converges to f at continuity, to the midpoint at jumps.

### Q122. State Euler's form of the Fourier series and give the complex coefficients in terms of a single integral.

> **Type:** Theory
> **Answer:** f(x) ~ Σₙ₌₋∞^∞ cₙ eⁱⁿᵖπx/L with cₙ = (1/2L)∫₋ᴸᴸ f(x)e⁻ⁱⁿᵖπx/L dx; equivalently cₙ = (aₙ − i bₙ)/2 for n > 0, c₋ₙ = (aₙ + i bₙ)/2, and c₀ = a₀/2.
> **Solution:** Writing cos θ = (e^{iθ} + e^{−iθ})/2 and sin θ = (e^{iθ} − e^{−iθ})/(2i) converts the real series into a single sum over all integers of n, positive and negative, with a single formula for the coefficient. The reality condition f real gives c₋ₙ = cₙ*, which is exactly what pairs the positive and negative frequencies. The integral is a Fourier transform evaluated at discrete points nπ/L, and this is the bridge to the continuous Fourier transform of Section 11: taking L → ∞ makes the spacing π/L → 0 and the sum become an integral.
> **Key point:** Euler form: f = Σₙ₌₋∞^∞ cₙ eⁱⁿᵖπx/L with cₙ = (1/2L)∫f e⁻ⁱⁿᵖπx/L; c₋ₙ = cₙ*.

### Q123. Let f(x) = x on (−π, π) and be 2π-periodic. What does the Fourier series converge to at x = 0 and at x = π?

> **Type:** Numerical
> **Answer:** At x = 0 it converges to 0; at x = π it converges to [π + (−π)]/2 = 0 as well.
> **Solution:** At x = 0 the periodic extension is continuous (f(0⁻) = 0⁻ and f(0⁺) = 0⁺, and since f(x) = x, the left limit as x → 0⁻ is 0 and the right limit is 0), so the sum is f(0) = 0. At x = π the extension jumps: f(π⁻) = π and f(π⁺) = −π (because of periodicity f(x + 2π) = f(x), so just past π the function takes values near −π), giving the average (π − π)/2 = 0. Both values are 0, but for different reasons: continuity at the origin, midpoint of a jump at ±π.
> **Key point:** The series gives f at continuity points and the midpoint (f⁺ + f⁻)/2 at jumps — here 0 at both x = 0 and x = π.

### Q124. Compute a₀ for f(x) = 1 on (−π, π).

> **Type:** Numerical
> **Answer:** a₀ = 2, so the constant term a₀/2 = 1.
> **Solution:** a₀ = (1/L)∫₋ᴸᴸ f dx with L = π, so a₀ = (1/π)∫₋π^π 1 dx = (1/π)(2π) = 2. The convention of writing the constant as a₀/2 then gives exactly 1, which is the function itself, as it must be: a constant function has no harmonics. Every an and bn vanishes because ∫cos(nx)dx and ∫ sin(nx)dx over a full period are zero.
> **Key point:** For a constant f, a₀/2 recovers the constant and all harmonics vanish.

### Q125. Compute a₀ for f(x) = eˣ on (−π, π).

> **Type:** Numerical
> **Answer:** a₀ = 2 sinh(π)/π ≈ 7.372, so the constant term a₀/2 = sinh(π)/π ≈ 3.686.
> **Solution:** a₀ = (1/π)∫₋π^π eˣ dx = (1/π)(e^π − e⁻^π) = 2 sinh(π)/π. Numerically e^π = 23.1407, e⁻^π = 0.0432, so the integral is 23.0975 and a₀ = 23.0975/3.1416 = 7.372. Hence a₀/2 = 3.686. The large value is forced by the exponential growth of f towards the right endpoint, which also shows up in the 1/n² coefficient decay of the full eˣ series: the periodic extension jumps at x = ±π.
> **Key point:** a₀ = (1/π)(e^π − e⁻^π) = 2 sinh(π)/π ≈ 7.372; the constant term a₀/2 ≈ 3.686.

### Q126. Compute aₙ for f(x) = x² on (−π, π).

> **Type:** Numerical
> **Answer:** aₙ = 4(−1)ⁿ/n², and a₀ = 2π²/3.
> **Solution:** aₙ = (1/π)∫₋π^π x² cos(nx) dx = (2/π)∫₀^π x² cos(nx) dx. Integrating by parts: ∫₀^π x² cos(nx) dx = [x² sin(nx)/n]₀^π − (2/n)∫₀^π x sin(nx) dx, and ∫₀^π x sin(nx) dx = [−x cos(nx)/n]₀^π + ∫₀^π cos(nx)/n dx = −π(−1)ⁿ/n. Hence ∫₀^π x² cos(nx) dx = −(2/n)(−π(−1)ⁿ/n) = 2π(−1)ⁿ/n², so aₙ = (2/π)(2π(−1)ⁿ/n²) = 4(−1)ⁿ/n². Also a₀ = (1/π)(2π³/3) = 2π²/3, giving a₀/2 = π²/3 ≈ 3.290.
> **Key point:** For f = x², aₙ = 4(−1)ⁿ/n² — the 1/n² decay signals a function with a kink at the periodic join.

### Q127. [GATE-1] The Fourier series of f(x) = x on (−π, π) evaluated at x = π/2 equals:

> **Type:** MCQ
> **Answer:** π/2 ≈ 1.571 (Option b).
> **Solution:** Since f is odd, only sine terms appear: bₙ = (1/π)∫₋π^π x sin(nx) dx = (2/π)∫₀^π x sin(nx) dx = (2/π)(−π(−1)ⁿ/n) = 2(−1)^{n+1}/n. So x = 2Σ(−1)^{n+1} sin(nx)/n. At x = π/2, sin(nπ/2) vanishes for even n and alternates as 1, −1, 1, −1 for odd n, so π/2 = 2Σ_{k=0}^∞ (−1)^k/(2k+1), which is twice the Leibniz series for π/4 ✓. Option (a) is the value of the series without the leading factor 2, and option (d) results from using the coefficients of a cosine series.
> **Key point:** An odd function's series has only sine terms; at x = π/2 it gives twice the Leibniz series, so x = π/2 there.

### Q128. [GATE-2] A function f is 1 for 0 < x < π and 0 for −π < x < 0, extended 2π-periodically. What does its Fourier series sum to at x = 0 and at x = π/2?

> **Type:** MCQ
> **Answer:** 1/2 at x = 0 and 1 at x = π/2 (Option c).
> **Solution:** At x = 0 the periodic extension jumps from 0 (left limit) to 1 (right limit), so the series converges to the average 1/2. At x = π/2 the function is continuous with value 1, so the sum is 1. The coefficients make this explicit: the function equals (1 + sgn x)/2, and the sign function has the series (4/π)Σ_{odd} sin(nx)/n, so f has a₀/2 = 1/2 plus sine terms. At x = 0 every sine vanishes, leaving exactly 1/2.
> **Key point:** At a jump the series gives (f⁺ + f⁻)/2 = 1/2; at an interior point it gives f = 1.

### Q129. Compute the Fourier series of f(x) = eˣ on (−π, π) in full, showing aₙ and bₙ.

> **Type:** Numerical
> **Answer:** eˣ = (sinh π/π) + (2 sinh π/π) Σₙ₌₁^∞ (−1)ⁿ [cos(nx) − n sin(nx)]/(1 + n²).
> **Solution:** With a₀/2 = sinh(π)/π, integrating ∫eˣ cos(nx) dx and ∫eˣ sin(nx) dx by parts gives aₙ = (1/π)∫₋π^π eˣ cos(nx) dx = (2(−1)ⁿ sinh π)/(π(1 + n²)) and bₙ = (1/π)∫₋π^π eˣ sin(nx) dx = −(2n(−1)ⁿ sinh π)/(π(1 + n²)). Both share the factor 2(−1)ⁿ sinh π/π, and bₙ = −n aₙ, so the series is (sinh π/π)[1 + 2Σ(−1)ⁿ(cos(nx) − n sin(nx))/(1 + n²)]. The coefficients decay as 1/n², reflecting that the periodic extension of eˣ has a finite jump at x = ±π but is otherwise smooth.
> **Key point:** For f = eˣ on (−π, π), aₙ = 2(−1)ⁿ sinh π/(π(1+n²)) and bₙ = −n aₙ; both decay as 1/n².

### Q130. Compare the rate of decay of aₙ and bₙ for (i) f(x) = x and (ii) f(x) = x² on (−π, π), and relate it to the smoothness of the periodic extension.

> **Type:** Comparison
> **Answer:** For x the coefficients decay as 1/n, for x² as 1/n²; the periodic extension of x has jumps at x = ±π while that of x² is continuous there but has a corner (kink).
> **Solution:** For x² the coefficients are aₙ = 4(−1)ⁿ/n² with bₙ = 0, while for x the coefficients are bₙ = 2(−1)^{n+1}/n with aₙ = a₀ = 0. The general rule: a jump discontinuity in the periodic extension produces 1/n coefficients, while a continuous-but-not-differentiable extension produces 1/n². The extension of x² is continuous at ±π because x²(π) = x²(−π) = π², but its derivative jumps from 2π to −2π there, so only the first derivative is discontinuous. Each extra degree of continuity costs one extra power of 1/n.
> **Key point:** Jumps in the periodic extension ⟹ coefficients ∝ 1/n; kinks ⟹ 1/n²; each extra derivative of continuity gains a power of n.

### Q131. What is the Gibbs phenomenon, and does increasing the number of terms reduce the overshoot?

> **Type:** Theory
> **Answer:** Near a jump discontinuity of the periodic extension, the partial sums overshoot the true value by about 9% of the jump, no matter how many terms are used; increasing N narrows the region of overshoot but does not reduce its height.
> **Solution:** The partial sums are trigonometric polynomials, hence continuous, so they cannot equal a discontinuous function near the jump. The partial sum is f convolved with the Dirichlet kernel, whose side lobes have a fixed relative size, which is what produces an overshoot of about 0.0895 of the jump for every N. The correct engineering response is not to fight the height but to note that the overshoot region shrinks as 1/N, so a single sampled point quickly falls outside it, or to smooth f beforehand.
> **Key point:** Gibbs overshoot is ≈ 9% of the jump and is independent of N; only its width shrinks like 1/N.

### Q132. Explain why the Fourier series of an even function contains no sine terms, and vice versa.

> **Type:** Theory
> **Answer:** For even f, f(x) sin(nπx/L) is odd and integrates to zero over (−L, L), so every bₙ vanishes; for odd f, f(x)cos(nπx/L) is odd and every aₙ vanishes.
> **Solution:** The basis functions inherit the parity of f: cosine is even, sine is odd, so the product's parity is the product of the two parities, and the integral of an odd function over a symmetric interval is zero. This is a quick structural check on any computation — a sine term in the series of an even function means an arithmetic error. Symmetry is not only a computational aid but a compact description of the function: an even function's whole content is in a₀ and the aₙ.
> **Key point:** Even f ⟹ bₙ = 0; odd f ⟹ aₙ = a₀ = 0, by odd integrands over a symmetric interval.

### Q133. A function's Fourier coefficients satisfy |aₙ| ≤ C/n² for all n. What can you conclude about f?

> **Type:** Conceptual
> **Answer:** f is continuous on (−L, L) and its periodic extension is continuous, with a piecewise continuous first derivative — the 1/n² decay implies continuity of f at the periodic join, so the Fourier series converges to f everywhere.
> **Solution:** By the Riemann–Lebesgue lemma aₙ → 0 for any integrable f, but the quantitative 1/n² bound, together with an absolutely convergent series Σ|aₙ| < ∞, guarantees uniform convergence of the series to a continuous function; since the coefficients came from f, that function is f itself. A 1/n bound would instead indicate a jump and convergence only to the midpoint there. This is the standard regularity ladder: 1/n for jumps, 1/n² for kinks, 1/n³ for continuous first derivative with a jump in the second, and so on.
> **Key point:** |aₙ| ≤ C/n² ⟹ absolutely, uniformly convergent series ⟹ f is continuous everywhere on the circle.

### Q134. Find a₀, a₁, a₂, b₁, b₂ for f(x) = cos(2x) on (−π, π).

> **Type:** Numerical
> **Answer:** a₀ = 0, a₂ = 1, and a₁ = b₁ = b₂ = 0.
> **Solution:** The Fourier system is an orthogonal basis, so it reproduces single harmonics exactly: f = cos(2x) already is the n = 2 harmonic with unit amplitude. a₂ = (1/π)∫₋π^π cos²(2x) dx = (1/π)·π = 1. a₀ = (1/π)∫cos(2x)dx = 0, a₁ = (1/π)∫cos(2x)cos x dx = 0 by orthogonality, and every bₙ = 0 because cos(2x) is even. The result is a useful sanity anchor: the Fourier series is an identity-preserving expansion, not a truncated approximation.
> **Key point:** A single harmonic is its own Fourier series: a₂ = 1, everything else 0.

### Q135. [GATE-2] A periodic function has period 2π and satisfies f(x + π) = −f(x). Which Fourier coefficients must vanish?

> **Type:** MCQ
> **Answer:** All the even-n coefficients must vanish: a₀, a₂, a₄, and b₂, b₄, leaving only odd harmonics (Option d).
> **Solution:** Split the coefficient integral into two halves: aₙ = (1/π)∫₀^π [f(x)cos(nx) + f(x+π)cos(n(x+π))] dx = (1/π)∫₀^π f(x)[cos(nx) − cos(nx + nπ)] dx. For even n, cos(nx + nπ) = cos(nx), so the bracket vanishes and aₙ = 0; the same argument kills bₙ for even n. For odd n, cos(nx + nπ) = −cos(nx), so the bracket doubles and the coefficient survives. This is the half-wave symmetry that makes a full-wave rectifier's output a DC term plus odd harmonics.
> **Key point:** Half-wave symmetry f(x + π) = −f(x) kills all even-n coefficients, leaving only odd harmonics.

---

## Section 9. Fourier series of standard functions, half-range expansions, Parseval

### Q136. Write the half-range sine series of f(x) = x on (0, L).

> **Type:** Numerical
> **Answer:** x = (2L/π) Σₙ₌₁^∞ (−1)^{n+1} (1/n) sin(nπx/L), i.e. bₙ = 2L(−1)^{n+1}/(nπ).
> **Solution:** The half-range sine series uses bₙ = (2/L)∫₀ᴸ x sin(nπx/L) dx. Integrating by parts: ∫₀ᴸ x sin(nπx/L) dx = [−xL cos(nπx/L)/(nπ)]₀ᴸ + ∫₀ᴸ (L/(nπ))cos(nπx/L) dx = −L²(−1)ⁿ/(nπ) + 0. So bₙ = (2/L)(−L²(−1)ⁿ/(nπ)) = 2L(−1)^{n+1}/(nπ). The series represents f on (0, L) and, by the Dirichlet rule, the odd 2L-periodic extension — a sawtooth — which is 0 at x = 0 and jumps from L to −L at x = L.
> **Key point:** Half-range sine of f = x on (0,L): bₙ = 2L(−1)^{n+1}/(nπ); it represents the odd extension.

### Q137. Write the half-range cosine series of f(x) = x on (0, L).

> **Type:** Numerical
> **Answer:** x = L/2 − (4L/π²) Σₙ₌₁^∞ cos((2n−1)πx/L)/(2n−1)², i.e. a₀ = L and aₙ = 2L((−1)ⁿ − 1)/(n²π²), which is −4L/(n²π²) for odd n and 0 for even n.
> **Solution:** a₀ = (2/L)∫₀ᴸ x dx = (2/L)(L²/2) = L, so a₀/2 = L/2. For n ≥ 1, aₙ = (2/L)∫₀ᴸ x cos(nπx/L) dx = (2/L)[xL sin(nπx/L)/(nπ) + L²cos(nπx/L)/(nπ)²]₀ᴸ = (2/L)(L²(−1)ⁿ − L²)/(nπ)² = 2L((−1)ⁿ − 1)/(n²π²). This vanishes for even n and equals −4L/(n²π²) for odd n. Writing odd n = 2m−1 gives the compact form above. The cosine series represents the even extension, so at x = 0 it converges to 0 (the average of −0 and 0), and the 1/n² decay confirms the even extension is continuous.
> **Key point:** Half-range cosine of f = x: a₀ = L, aₙ = 2L((−1)ⁿ − 1)/(nπ)² — only odd n survive.

### Q138. Find the Fourier series of the square wave f(x) = 1 for 0 < x < π, 0 for −π < x < 0, 2π-periodic, and use it to evaluate 1 − 1/3 + 1/5 − 1/7 + ⋯.

> **Type:** Numerical
> **Answer:** f(x) = 1/2 + (2/π)Σ_{n odd} sin(nx)/n; at x = π/2 this gives 1 − 1/3 + 1/5 − 1/7 + ⋯ = π/4 ≈ 0.7854.
> **Solution:** Since f = (1 + sgn x)/2, its series is the constant 1/2 plus half the sign-function series 1/2 + (2/π)Σ_{n odd} sin(nx)/n, where the sign function's own series is (4/π)Σ_{n odd} sin(nx)/n. At x = π/2 the sines alternate 1, −1, 1, −1 for n = 1, 3, 5, 7, so f(π/2) = 1/2 + (2/π)(1 − 1/3 + 1/5 − 1/7 + ⋯) = 1. Hence (2/π)S = 1/2 and S = π/4 ≈ 0.7854. The two routes agree: the sign function has coefficient (4/π)/n and equals 1 at x = π/2, giving S = π/4 directly, while the square wave's half-sized coefficients are exactly offset by its 1/2 DC term.
> **Key point:** The square wave (1 + sgn x)/2 is 1/2 + (2/π)Σ_{odd} sin(nx)/n; at x = π/2 the alternating odd sum is π/4.

### Q139. Write the Fourier series of the triangular wave f(x) = x for 0 < x < π, f(x) = 2π − x for π < x < 2π, extended with period 2π, and identify its symmetry.

> **Type:** Numerical
> **Answer:** f(x) = π/2 − (4/π)Σ_{n odd} cos(nx)/n²; it is even about x = 0, so only cosine terms appear and bₙ = 0.
> **Solution:** f(−x) = f(x) by construction, so bₙ = 0. a₀ = (1/π)∫₋π^π f dx = (2/π)∫₀^π x dx = (2/π)(π²/2) = π, so a₀/2 = π/2. For n ≥ 1, aₙ = (2/π)∫₀^π x cos(nx) dx = (2/π)([x sin(nx)/n]₀^π + [cos(nx)/n²]₀^π) = (2/π)((−1)ⁿ − 1)/n², which is 0 for even n and −4/(πn²) for odd n. So f = π/2 − (4/π)Σ_{n odd} cos(nx)/n². The 1/n² decay is exactly what the smoothness ladder predicts for a continuous function with a corner at the peak.
> **Key point:** The triangular wave is even: f = π/2 − (4/π)Σ_{n odd} cos(nx)/n², with 1/n² decay from the corner.

### Q140. State Parseval's identity for a real function on (−L, L) and explain what it asserts.

> **Type:** Theory
> **Answer:** (1/L)∫₋ᴸᴸ f(x)² dx = a₀²/2 + Σₙ₌₁^∞ (aₙ² + bₙ²), under the same Dirichlet assumptions as the series itself; it asserts that the mean-square value of f equals the "power" carried by its coefficients.
> **Solution:** The identity is the completeness of the trigonometric system: the basis functions are orthonormal (after the 1/√(2L) normalisation) so expanding f and squaring, cross terms vanish by orthogonality and the surviving terms are the squared coefficients. Because the left side is a mean square, Parseval is a statement about power, which is why in signals contexts the same formula is written as total signal power = sum of the powers of each harmonic (plus the DC power a₀²/2). It is also a powerful computational tool: any integral of f² can be reduced to an algebraic sum over the coefficients.
> **Key point:** Parseval: (1/L)∫₋ᴸᴸ f² = a₀²/2 + Σ(aₙ² + bₙ²) — mean-square power equals the sum of coefficient squares.

### Q141. Use Parseval's identity on f(x) = x on (−π, π) to evaluate Σₙ₌₁^∞ 1/n².

> **Type:** Numerical
> **Answer:** π²/6 ≈ 1.645.
> **Solution:** f = x is odd, so aₙ = a₀ = 0, and the sine coefficients are bₙ = 2(−1)^{n+1}/n. Parseval gives (1/π)∫₋π^π x² dx = Σ bₙ² = 4Σ1/n². The integral is (1/π)(2π³/3) = 2π²/3, so 2π²/3 = 4Σ1/n² and Σ1/n² = π²/6 ≈ 1.645 ✓ (partial sums: 1 + 0.25 + 0.111 + 0.0625 ≈ 1.42, still climbing toward 1.645).
> **Key point:** Parseval on f = x gives Σ1/n² = π²/6 ≈ 1.645.

### Q142. Use Parseval's identity on f(x) = 1 on (−π, π) to confirm the normalisation of the constant term.

> **Type:** Numerical
> **Answer:** 2 = a₀²/2 with a₀ = 2, so the left side 2 = a₀²/2 = 2 ✓.
> **Solution:** The left side is (1/π)∫₋π^π 1 dx = (1/π)(2π) = 2. On the right, all harmonics vanish and a₀ = 2, so a₀²/2 = 4/2 = 2. The two sides agree, which confirms both the 1/π normalisation of the coefficients and the convention of writing the constant as a₀/2 — had the series used a₀ directly, the right side would be 4 and Parseval would fail.
> **Key point:** Parseval on a constant checks the a₀/2 convention: (1/π)(2π) = 2 = a₀²/2.

### Q143. Use Parseval's identity on the sign function to evaluate Σ_{n odd} 1/n².

> **Type:** Numerical
> **Answer:** π²/8 ≈ 1.234.
> **Solution:** sgn x has series (4/π)Σ_{n odd} sin(nx)/n, so a₀ = 0, aₙ = 0, bₙ = 4/(πn) for n odd and 0 for n even. Parseval: (1/π)∫₋π^π 1 dx = 2 = Σ bₙ² = (16/π²)Σ_{n odd}1/n². So Σ_{n odd}1/n² = 2π²/16 = π²/8 ≈ 1.234. Check by subtracting the even terms from the full sum: π²/6 − (1/4)(π²/6) = (3/4)(π²/6) = π²/8 ✓.
> **Key point:** Parseval on sgn x gives Σ_{odd}1/n² = π²/8 = ¾ of the full Σ1/n².

### Q144. [GATE-2] For f(x) = x² on (−π, π), use Parseval to evaluate Σₙ₌₁^∞ 1/n⁴.

> **Type:** NAT
> **Answer:** π⁴/90 ≈ 1.082
> **Solution:** For x² the coefficients are a₀ = 2π²/3, aₙ = 4(−1)ⁿ/n² and bₙ = 0. Parseval: (1/π)∫₋π^π x⁴ dx = a₀²/2 + Σ aₙ². Left side = (1/π)(2π⁵/5) = 2π⁴/5. Right side = (1/2)(4π⁴/9) + 16Σ1/n⁴ = 2π⁴/9 + 16Σ1/n⁴. So 16Σ1/n⁴ = 2π⁴/5 − 2π⁴/9 = (2π⁴)(4/45) = 8π⁴/45, giving Σ1/n⁴ = 8π⁴/720 = π⁴/90 ≈ 1.082 ✓ (partial sums: 1 + 1/16 + 1/81 ≈ 1.075, approaching 1.082).
> **Key point:** Parseval on f = x² gives Σ1/n⁴ = π⁴/90 ≈ 1.082.

### Q145. State the half-range sine and half-range cosine expansions of a function defined on (0, L) and explain why they differ from the full-range series.

> **Type:** Theory
> **Answer:** The half-range sine series uses bₙ = (2/L)∫₀ᴸ f sin(nπx/L) dx and represents the odd extension of f to (−L, L); the half-range cosine series uses aₙ = (2/L)∫₀ᴸ f cos(nπx/L) dx and represents the even extension. Both reproduce f exactly on (0, L), but they have different values at x = 0 and near x = L.
> **Solution:** The factor 2/L instead of 1/L is the doubling from evenness. The two extensions are generally different functions outside (0, L) — a sine series makes f vanish at x = 0 while a cosine series makes it have the largest possible slope there — so both are valid expansions of f on (0, L) but describe different behaviours off the interval. The choice is dictated by which extension matches the physics: a string clamped at an endpoint wants odd extension, a string free or driven at an endpoint wants even.
> **Key point:** Half-range sine = odd extension, half-range cosine = even extension, both with the 2/L coefficient factor.

### Q146. Compute the half-range sine series of f(x) = 1 on (0, L) and identify the function it represents outside (0, L).

> **Type:** Numerical
> **Answer:** 1 = (4/π)Σ_{n odd} sin(nπx/L)/n, representing the square wave that equals 1 on (0, L), −1 on (−L, 0), and is 2L-periodic.
> **Solution:** bₙ = (2/L)∫₀ᴸ sin(nπx/L) dx = (2/L)([−L cos(nπx/L)/(nπ)]₀ᴸ) = (2/L)(−L(−1)ⁿ/(nπ) + L/(nπ)) = (2/(nπ))(1 − (−1)ⁿ). This is 4/(nπ) for n odd and 0 for n even. So 1 = (4/π)Σ_{n odd} sin(nπx/L)/n on (0, L). The odd extension is the square wave, whose 1/n coefficients correctly signal the jump at x = 0. At x = L/2 the series gives 1 = (4/π)(1 − 1/3 + 1/5 − ⋯) = (4/π)(π/4) ✓, the Leibniz identity again.
> **Key point:** Half-range sine of f = 1 is the square wave: 1 = (4/π)Σ_{n odd} sin(nπx/L)/n.

### Q147. Evaluate the Fourier series of f(x) = x on (−π, π) at the discontinuity x = π, and relate the result to the values of the sine terms there.

> **Type:** Numerical
> **Answer:** 0.
> **Solution:** At x = π every term sin(nπ) vanishes, and a₀ = 0, so the series sums to exactly 0. This matches the Dirichlet rule: the periodic extension jumps from f(π⁻) = π to f(π⁺) = −π, and the average of the two limits is 0. The point is that a pointwise substitution here is legitimate and agrees with the general jump rule, so no special argument is needed.
> **Key point:** At x = π the sawtooth series of f = x sums to 0, the midpoint of the jump π → −π.

### Q148. [GATE-1] A periodic function has a₀ = 0, a₁ = 2, and all other coefficients zero. What is f(x)?

> **Type:** MCQ
> **Answer:** f(x) = 2 cos(πx/L) for a period-2L function, i.e. 2 cos x if L = π (Option b).
> **Solution:** The series is a₀/2 + a₁cos(πx/L) = 2cos(πx/L) with no sine terms. With L = π the fundamental is n₀ = π/L = 1, so f(x) = 2cos x. Option (a) drops the factor 2, option (c) uses a sine term, and option (d) mistakenly treats a₁ as the constant term. This is the inverse direction of the coefficient computation: the coefficients *are* the Fourier representation, so knowing them all determines f completely (uniqueness of Fourier coefficients).
> **Key point:** The coefficients fully determine f; a single nonzero a₁ = 2 means f = 2cos(n₀x).

### Q149. Compute the Fourier series of f(x) = |x| on (−π, π) and use it to evaluate 1 + 1/9 + 1/25 + ⋯.

> **Type:** Numerical
> **Answer:** |x| = π/2 − (4/π)Σ_{n odd} cos(nx)/n², and 1 + 1/9 + 1/25 + ⋯ = π²/8 ≈ 1.234.
> **Solution:** |x| is even, so bₙ = 0. a₀ = (1/π)∫₋π^π |x| dx = (2/π)(π²/2) = π, so a₀/2 = π/2. aₙ = (1/π)∫₋π^π |x|cos(nx) dx = (2/π)∫₀^π x cos(nx) dx = (2/π)([x sin(nx)/n]₀^π + [cos(nx)/n²]₀^π) = (2/π)((−1)ⁿ − 1)/n², which is 0 for even n and −4/(πn²) for odd n. So |x| = π/2 − (4/π)Σ_{n odd} cos(nx)/n². At x = 0, |0| = 0 = π/2 − (4/π)Σ_{n odd}1/n², so Σ_{n odd}1/n² = π²/8 ≈ 1.234 ✓.
> **Key point:** |x| = π/2 − (4/π)Σ_{n odd}cos(nx)/n²; at x = 0, Σ_{odd}1/n² = π²/8.

### Q150. Give the Fourier series of f(x) = x on (0, π) extended by half-range cosine, and confirm its value at x = 0.

> **Type:** Numerical
> **Answer:** x = π/2 − (4/π)Σ_{n odd} cos(nx)/n² on 0 < x < π; at x = 0 the series sums to 0 = π/2 − (4/π)(π²/8) = 0 ✓.
> **Solution:** The half-range cosine series of x on (0, π) is the |x| series specialised to L = π. The even extension is continuous at x = 0 with value 0, so the series converges to 0 there rather than to a midpoint. Substituting Σ_{n odd}1/n² = π²/8: π/2 − (4/π)(π²/8) = π/2 − π/2 = 0 ✓. The agreement is a genuine cross-check between the |x| series (an even function on a symmetric interval) and the half-range cosine series of x.
> **Key point:** The half-range cosine series of x on (0, π) sums to 0 at x = 0, confirming continuity of the even extension.

### Q151. [GATE-2] For a function on (−L, L), why is the coefficient a₀ conventionally written as a₀/2, and what would break if it were written as a₀?

> **Type:** MCQ
> **Answer:** Because a₀ computed from the standard integral already equals twice the mean value; writing a₀/2 makes the series reconstruct the mean value of f. Writing a₀ would double the constant contribution and break the identity for constant functions and the form of Parseval's identity (Option a).
> **Solution:** a₀ = (1/L)∫₋ᴸᴸ f dx is 2 × (average of f), since the average is (1/2L)∫f. The series must contain the average, so the coefficient in the series is a₀/2. If a₀ were inserted directly, then for f = 1 the series would read 2 rather than 1, and Parseval's right-hand side a₀²/2 would need replacing by a₀², so the familiar symmetric form would be lost. Every published table of coefficients uses the a₀/2 convention for this reason.
> **Key point:** a₀ = 2 × mean value, hence the series writes a₀/2; the convention is what makes constant functions work.

### Q152. Compute the Fourier series of f(x) = cos²x on (−π, π) and verify it against the elementary identity cos²x = (1 + cos 2x)/2.

> **Type:** Numerical
> **Answer:** a₀/2 = 1/2, a₂ = 1/2, all other coefficients zero.
> **Solution:** cos²x = (1 + cos 2x)/2 by the double-angle identity, and the Fourier system reproduces this exactly: a₀ = (1/π)∫₋π^π (1 + cos2x)/2 dx = 1, a₂ = (1/π)∫cos²x cos 2x dx = (1/π)∫(1/2)(1 + cos2x)cos2x dx = (1/2), and orthogonality kills everything else. The value of this exercise is as a unit test of the coefficient integrals: any error in the normalisation or the a₀/2 convention would show up immediately here.
> **Key point:** cos²x is exactly 1/2 + (1/2)cos 2x; a₀/2 = 1/2, a₂ = 1/2, rest zero.

---

## Section 10. Properties of Fourier series: symmetry, shifting, scaling, differentiation, integration, convolution

### Q153. State the shifting (translation) property: if g(x) = f(x + c), how do the coefficients of g relate to those of f?

> **Type:** Theory
> **Answer:** Writing f in Euler form, g(x) = f(x + c) has coefficients ĉₙ = cₙ eⁱⁿᵖc/L; in real form a′ₙ = aₙ cos(nπc/L) − bₙ sin(nπc/L) and b′ₙ = aₙ sin(nπc/L) + bₙ cos(nπc/L).
> **Solution:** Multiplying the Euler series of f by eⁱⁿᵖc/L and reindexing x + c → x gives the result immediately, since e^{inπc/L} is a pure phase. In real form this is a rotation of the (aₙ, bₙ) pair by the angle nπc/L, so shifting preserves every coefficient's magnitude and only rotates it — a statement with the same flavour as a phase shift in a phasor. A shift by half the period flips the sign of every coefficient with odd n, which is half-wave symmetry in coefficient form.
> **Key point:** Shifting by c rotates each (aₙ, bₙ) pair by nπc/L and leaves |aₙ + ibₙ| unchanged.

### Q154. A function f(x) has period 2L. What is the effect on its Fourier series of scaling to g(x) = f(2x)?

> **Type:** Theory
> **Answer:** g has period L, so its fundamental frequency doubles: the series becomes a₀/2 + Σ[aₙ cos(2nπx/L) + bₙ sin(2nπx/L)], i.e. only even-index harmonics of the 2L-periodic expansion appear, with the same coefficient values.
> **Solution:** f(2x + L) = f(2x) since f has period 2L, so g has period L and its harmonics are spaced at 2π/L instead of π/L. Because g is a compression of f by a factor 2, the series is simply f's series with n replaced by 2n, so the 2L-periodic series of f contains only even harmonics when restricted — an observation that is sometimes the reverse trick: f has period 2L and is even, so f(2x) has period L and its series is f's series with doubled frequencies. No coefficients change value, only their frequencies.
> **Key point:** Compressing the argument by a factor k keeps coefficients but multiplies every frequency by k (period divides by k).

### Q155. [GATE-1] If f(x) is even, what does its Fourier series reduce to, and what is bₙ?

> **Type:** MCQ
> **Answer:** Only cosine terms: f(x) = a₀/2 + Σaₙcos(nπx/L), with bₙ = 0 for all n (Option c).
> **Solution:** Since f is even and sin(nπx/L) is odd, the product is odd and its integral over the symmetric interval (−L, L) vanishes, so bₙ = 0. Option (a) claims the opposite, option (b) mixes in a sine term for n = 1 only, and option (d) is about a different symmetry (half-wave). In physical terms, an even function on a symmetric interval is a standing-wave-friendly shape, which is why symmetric boundaries select cosine modes.
> **Key point:** Even f ⟹ bₙ = 0, series is purely cosines; odd f ⟹ aₙ = 0, purely sines.

### Q156. [GATE-2] When can a Fourier series be differentiated term by term, and what must be checked about the resulting series?

> **Type:** MCQ
> **Answer:** When f is continuously differentiable and its derivative is piecewise smooth (so f' satisfies the Dirichlet conditions), the series may be differentiated; the resulting series converges to f'(x) at points where f' is continuous and to the average of f' at its jumps (Option b).
> **Solution:** Term-by-term differentiation multiplies each coefficient by n₀ = π/L and drops bₙ's contribution to the cosine part, so convergence of Σ n aₙ and Σ n bₙ becomes the real question. The 1/n² decay of a continuous-but-kinked function is exactly the threshold: Σ n·(1/n²) = Σ1/n converges, so a kink may be differentiated once. But a jump (1/n decay) gives Σ n(1/n) = Σ1, a divergent series — differentiating there is invalid, and the term-by-term series diverges. In practice one checks that Σ n|aₙ| < ∞ before differentiating.
> **Key point:** Differentiate term by term only if Σ n|aₙ| converges; a 1/n decay (jump) forbids it, 1/n² (kink) permits one derivative.

### Q157. Integrating a Fourier series term by term introduces what kind of constant, and how is it fixed?

> **Type:** Theory
> **Answer:** A constant of integration C, since the antiderivative is determined only up to a constant; it is fixed by evaluating the integrated series at a point where the original function is known and subtracting.
> **Solution:** Integrating a₀/2 + Σ[aₙcos + bₙsin] gives ax + C + Σ[(aₙ/n₀)sin − (bₙ/n₀)cos], and the constant is genuinely undetermined by the integration process. In practice you pick x₀, evaluate the original f at x₀, and set the integrated series equal to f(x₀) at that point, which determines C. The term-by-term integral converges more readily than the original series because the extra 1/n factor damps the coefficients, so integration of a 1/n series is always safe.
> **Key point:** Integrating a Fourier series adds an undetermined constant, fixed by matching f at one known point.

### Q158. Given the series x = 2Σ(−1)^{n+1} sin(nx)/n on (−π, π), integrate term by term to find the series for x²/2 and hence evaluate Σ (−1)^{n+1}/n².

> **Type:** Numerical
> **Answer:** x²/2 = π²/6 − 2Σ(−1)^{n+1}cos(nx)/n², and evaluating at x = π gives Σ(−1)^{n+1}/n² = π²/12 ≈ 0.8225.
> **Solution:** Integrate x = 2Σ(−1)^{n+1}sin(nx)/n from 0 to x; the constant vanishes because both sides are 0 at x = 0, and ∫₀ˣ sin(nt)dt = (1 − cos nx)/n, so x²/2 = 2Σ(−1)^{n+1}(1 − cos nx)/n² = 2S − 2Σ(−1)^{n+1}cos(nx)/n² with S = Σ(−1)^{n+1}/n². Now set x = π: the left side is π²/2, and since cos(nπ) = (−1)ⁿ, the product (−1)^{n+1}cos(nπ) = −1, so the cosine sum becomes −2·(−1)·Σ1/n² = 2(π²/6) = π²/3. Hence π²/2 = 2S + π²/3, giving S = π²/12 ≈ 0.8225, consistent with the partial sum 1 − 1/4 + 1/9 − 1/16 ≈ 0.799 still rising toward it.
> **Key point:** Integrating the sawtooth series and evaluating at x = π gives Σ(−1)^{n+1}/n² = π²/12 ≈ 0.8225, and the series for x² is x² = π²/3 + 4Σ(−1)ⁿcos(nx)/n².

### Q159. Derive the convolution property: if h(t) = ∫ f₁(τ)f₂(t − τ) dτ, what is H(ω) in terms of F₁ and F₂?

> **Type:** Theory
> **Answer:** H(ω) = F₁(ω)F₂(ω) — the transform of a convolution is the product of the transforms, i.e. convolution in time becomes multiplication in frequency. The symmetric normalisation of the transform pair determines the factor, so with F(ω) = ∫f(t)e^{−iωt}dt and f(t) = (1/2π)∫F(ω)e^{iωt}dω, H = F₁F₂ exactly.
> **Solution:** Substitute both transform integrals into the definition of h and interchange the order of integration: the exponential e^{iωt}e^{−iωτ}e^{−iω(t−τ)} collapses to e^{iωt}, leaving a factor F₁(ω)F₂(ω) times the inverse-transform integral. The product form is the technical reason filters are designed in the frequency domain: a convolution in the time domain — a real-valued, hard-to-implement operation — becomes a multiplication, which corresponds to ordinary cascaded gain. The dual identity, that multiplication in time becomes a convolution in frequency with a 1/(2π) factor, is used to shift and to build modulated signals.
> **Key point:** Convolution in time ↔ multiplication in frequency: H(ω) = F₁(ω)F₂(ω).

### Q160. Given the discrete-series analogue, if two periodic signals have Fourier coefficient sequences {aₙ} and {bₙ}, what are the coefficients of their pointwise product?

> **Type:** Theory
> **Answer:** They are the discrete convolution cₙ = (1/(2L)) Σₖ aₖ b₍ₙ₋ₖ₎, with a 1/(2L) factor under the 1/(2L) normalisation of the series coefficient; equivalently the product of coefficients in continuous frequency becomes a convolution in discrete frequency.
> **Solution:** Multiply the two Euler series and reindex: the product of two exponentials is another exponential, so the coefficients of the product are the convolution of the two coefficient sequences. The DC term is the average of the product (Parseval's inner-product identity), and the factor 1/(2L) is the normalising weight of the discrete inner product. This is the discrete counterpart of the time-multiplication convolution, and it is the standard tool for predicting intermodulation and harmonic generation when a nonlinear device is described by a power series.
> **Key point:** The coefficients of a product of two periodic signals are the discrete convolution of the individual coefficient sequences.

### Q161. State the scaling property of the Fourier transform in the form f(at) ↔ (1/|a|)F(ω/a).

> **Type:** Theory
> **Answer:** If F(ω) = ∫f(t)e^{−iωt}dt, then the transform of f(at) is (1/|a|)F(ω/a); time compression by a factor a stretches the spectrum by 1/a and scales its amplitude by 1/|a|.
> **Solution:** Substitute u = at, so dt = du/a, and the exponent becomes −i(ω/a)u, which is the definition of F evaluated at ω/a. The absolute value is needed because a < 0 reverses the orientation of the integral as well as rescaling it. The physical reading is a time-frequency duality: a pulse shortens by a and its spectral width widens by 1/a, with a 1/a reduction of the spectral level, so that the spectral area is unchanged.
> **Key point:** f(at) ↔ (1/|a|)F(ω/a): time compression by a stretches frequency by 1/a.

### Q162. [GATE-1] A signal x(t) is a pure tone cos(100πt). What is its spectrum, and how many lines does it have?

> **Type:** MCQ
> **Answer:** Two lines at ω = ±100π rad/s, each with magnitude 1/2; equivalently a single line of amplitude 1 at f = 50 Hz (Option c).
> **Solution:** cos(100πt) = (e^{i100πt} + e^{−i100πt})/2, so X(ω) = (1/2)[δ(ω − 100π) + δ(ω + 100π)]: two impulses of weight 1/2. In one-sided (amplitude) spectrum language the two half-weight lines are conventionally combined into one line of amplitude 1 at the positive frequency. The frequency is 100π/(2π) = 50 Hz. Option (a) with one line is the one-sided description, option (b) misplaces the frequency by a factor of 2π, and option (d) wrongly doubles the amplitude.
> **Key point:** cos(ω₀t) ↔ (1/2)[δ(ω − ω₀) + δ(ω + ω₀)] — two lines of weight 1/2.

### Q163. A periodic square wave of amplitude A and 50% duty cycle is described by which harmonics?

> **Type:** Conceptual
> **Answer:** Odd harmonics only, of the form (4A/π)[sin(ω₀t) + (1/3)sin 3ω₀t + (1/5)sin 5ω₀t + ⋯], with 1/n amplitude roll-off.
> **Solution:** A 50%-duty square wave satisfies half-wave symmetry f(t + T/2) = −f(t), which kills all even harmonics, and it is odd in the variable centred on the zero crossing, so no DC and no cosine terms. The amplitudes fall as 1/n, the signature of the jump discontinuities, and the sign alternates in the sine terms. This is the basis of the odd-harmonic-only push-pull amplifier stage and of the third-harmonic distortion analysis of any clipping stage.
> **Key point:** A 50%-duty square wave has odd harmonics only, amplitudes 4A/(πn) — half-wave symmetry kills even n.

### Q164. Which property of a function determines whether its Fourier series contains a DC term?

> **Type:** Conceptual
> **Answer:** Only a₀ matters: the DC term is a₀/2 = (1/2L)∫₋ᴸᴸ f dx, so a function with zero mean value has no DC component. Odd functions automatically have a₀ = 0; even functions generally do not.
> **Solution:** A₀ vanishes exactly when the areas above and below the mean line cancel, which is guaranteed for odd f (odd integrand) but not for even f. A full-wave rectified sine, f = |sin x|, is even and has a₀/2 = 2/π ≈ 0.637, the classic DC component of a rectifier output. Symmetries other than oddness can also force a₀ = 0: half-wave antisymmetry, or any function antisymmetric about the origin combined with a nonzero mean elsewhere — which is why checking the mean value first is a cheap and reliable test.
> **Key point:** DC = a₀/2 = mean value of f; odd f always has none, even f generally does.

### Q165. Explain why a function with a jump in its periodic extension must be handled by integrating a series rather than differentiating one to get f′.

> **Type:** Conceptual
> **Answer:** A jump forces coefficients ∝ 1/n; term-by-term differentiation would require Σ n·(1/n) = Σ1 to converge, which it does not, while integration multiplies by 1/n and gives a convergent Σ1/n² series.
> **Solution:** Differentiating term by term multiplies each coefficient by its harmonic index, naₙ and nbₙ; with aₙ ~ 1/n these are O(1) and the resulting trigonometric series is not summable. Integrating instead divides each coefficient by the index, aₙ/n, giving ~1/n², an absolutely convergent series, so the antiderivative has a legitimate differentiable representation. This asymmetry is why sawtooth and square waves are routinely obtained by integrating a known series instead of differentiating an unknown one, and it is the practical reason for the rule "differentiate only when the coefficients decay at least as 1/n²."
> **Key point:** Jumps give 1/n coefficients — differentiate → divergent, integrate → 1/n², convergent.

### Q166. A function f on (−L, L) satisfies f(L − x) = f(x) for all x. What does this symmetry do to the cosine coefficients?

> **Type:** Numerical
> **Answer:** It forces aₙ = 0 for every odd n, so only even cosine harmonics survive, along with the DC term.
> **Solution:** Substitute x → L − x into aₙ = (1/L)∫₋ᴸᴸ f(x)cos(nπx/L) dx and split the interval at 0. Because f(L − x) = f(x) and cos(nπ(L − x)/L) = cos(nπ − nπx/L) = (−1)ⁿ cos(nπx/L), the two halves of the integral are equal when (−1)ⁿ = +1 (even n, so they double) and cancel when (−1)ⁿ = −1 (odd n). Hence aₙ = 0 for odd n. The condition is mirror symmetry about the midpoint x = L/2, and the surviving frequencies are exactly those symmetric about that point.
> **Key point:** Mirror symmetry about x = L/2 kills the odd-n coefficients; only even harmonics and DC survive.

### Q167. A band-limited signal of bandwidth B passes through a linear time-invariant system. What is guaranteed about the output bandwidth?

> **Type:** Conceptual
> **Answer:** The output cannot contain frequencies outside |ω| ≤ B, because the output spectrum is the product Y(ω) = X(ω)H(ω) and the input spectrum vanishes outside the band.
> **Solution:** The product of two functions, one of which is zero outside (−B, B), is also zero there, so no new frequencies can be generated. In the time domain this is the statement that the output is the convolution x ∗ h of two smooth band-limited signals, which is again smooth and band-limited. This is the reason a linear amplifier adds no harmonics: only nonlinearity, which is a time-domain multiplication and therefore a frequency convolution, can create new spectral content. It is also the basis for the sampling theorem's frequency-domain reading.
> **Key point:** A band-limited LTI system cannot create new frequencies: Y = X·H vanishes outside the input band.

### Q168. [GATE-2] A periodic signal's spectrum consists of lines at ω = ±ω₀ and ±2ω₀ only. What can you conclude about the time-domain signal?

> **Type:** MCQ
> **Answer:** It is a trigonometric polynomial of degree 2, so it is smooth, bounded and 2π/ω₀-periodic, containing only the fundamental and its second harmonic (Option c).
> **Solution:** A finite spectrum is the definition of a trigonometric polynomial: x(t) = A₁cos(ω₀t + φ₁) + A₂cos(2ω₀t + φ₂), with no higher content. Such a signal has no jumps anywhere, in particular none at the period boundary, so it is continuous and differentiable and its Fourier series is not merely convergent but absolutely and uniformly convergent with an exact finite form. The practical consequence is that such a signal is perfectly band-limited and can be reconstructed exactly from a finite number of samples, unlike a signal with an infinite spectrum.
> **Key point:** A finite spectrum means a finite trigonometric polynomial: smooth, exactly band-limited, exactly reconstructible.

---

## Section 11. The Fourier integral and integral evaluation

### Q169. State the Fourier integral theorem with the definitions of A(ω) and B(ω).

> **Type:** Theory
> **Answer:** For f piecewise continuous and piecewise smooth on (−∞, ∞), f(x) = ∫₀^∞ [A(ω)cos(ωx) + B(ω)sin(ωx)] dω with A(ω) = (1/π)∫₋∞^∞ f(t)cos(ωt) dt and B(ω) = (1/π)∫₋∞^∞ f(t)sin(ωt) dt; the integral equals the midpoint value at any jump of f.
> **Solution:** The theorem is the continuous-frequency limit of the Fourier series: as L → ∞ the spacing π/L → 0, the sum over discrete n becomes an integral, and the coefficients become the corresponding A and B functions. Equivalently, in the complex form, f(x) = (1/2π)∫₋∞^∞ F(ω)e^{iωx} dω with F(ω) = ∫₋∞^∞ f(t)e^{−iωt} dt, and A = (1/π)Re F, B = −(1/π)Im F for real f. The hypotheses are the same Dirichlet conditions on an unbounded interval, so the convergence statement carries over unchanged.
> **Key point:** Fourier integral: f(x) = ∫₀^∞[A cos + B sin]dω with A, B given by 1/π-weighted integrals over (−∞, ∞).

### Q170. [GATE-2] Obtain the Fourier transform representation of the Gaussian f(x) = e^{−x²} and verify it at x = 0.

> **Type:** Numerical
> **Answer:** F(ω) = √π e^{−ω²/4}, so e^{−x²} = (1/π)∫₋∞^∞ √π e^{−ω²/4}e^{iωx} dω; at x = 0 this yields ∫₀^∞ e^{−ω²/4} dω = √π/2 ≈ 0.886.
> **Solution:** Completing the square, F(ω) = ∫₋∞^∞ e^{−x²}e^{−iωx}dx = e^{−ω²/4}∫₋∞^∞ e^{−(x + iω/2)²}dx = √π e^{−ω²/4}, since the shifted Gaussian is evaluated by moving the contour back to the real axis. At x = 0 the inversion formula gives 1 = (1/2π)∫₋∞^∞ √π e^{−ω²/4}dω = (√π/π)∫₀^∞ e^{−ω²/4}dω, so ∫₀^∞ e^{−ω²/4}dω = π/√π = √π ≈ 1.772. Substituting t = ω/2 confirms it: the integral becomes 2∫₀^∞ e^{−t²}dt = 2(√π/2) = √π ✓, and the value √π/2 ≈ 0.886 is the separate half-line integral ∫₀^∞ e^{−t²}dt.
> **Key point:** F{e^{−x²}} = √π e^{−ω²/4}; at x = 0, ∫₀^∞ e^{−ω²/4} dω = √π ≈ 1.772.

### Q171. [GATE-2] Use the Fourier transform of e^{−a|t|} to find the Fourier transform of the impulse response of a first-order RC low-pass filter.

> **Type:** Numerical
> **Answer:** H(ω) = 1/(1 + jωRC), from h(t) = (1/RC)e^{−t/RC}u(t); |H(ω)| = 1/√(1 + (ωRC)²) with phase −tan⁻¹(ωRC). The two-sided transform of e^{−a|t|} is 2a/(a² + ω²) and is not the answer — the RC impulse response is the causal half of it.
> **Solution:** The impulse response of a unity-gain RC low-pass filter is h(t) = (1/RC)e^{−t/(RC)}u(t) = a e^{−at}u(t) with a = 1/RC. Its Fourier transform is a∫₀^∞ e^{−(a + jω)t} dt = a/(a + jω) = 1/(1 + jω/a) = 1/(1 + jωRC). The magnitude is 1/√(1 + (ωRC)²) and the phase is −tan⁻¹(ωRC), both standard results. The symmetric pair confirms the convention: the transform of the two-sided e^{−a|t|} is 2a/(a² + ω²), and folding the causal half to both sides introduces the extra factor.
> **Key point:** h(t) = (1/RC)e^{−t/RC}u(t) ↔ H(ω) = 1/(1 + jωRC); |H| = 1/√(1+(ωRC)²), phase = −tan⁻¹(ωRC).

### Q172. Evaluate ∫₀^∞ cos(ax)cos(bx)/(1 + x²) dx using the Fourier transform of 1/(1 + x²).

> **Type:** Numerical
> **Answer:** (π/4)(e^{−|a−b|} + e^{−(a+b)}) for a, b > 0; more generally (π/4)(e^{−|a−b|} + e^{−|a+b|}).
> **Solution:** The transform of f(x) = 1/(1 + x²) is F(ω) = π e^{−|ω|}, obtained by contour integration. Write cos(ax)cos(bx) = (1/2)[cos((a−b)x) + cos((a+b)x)], and use the inversion formula f(0) = (1/π)∫₀^∞ F(ω)dω = ∫₀^∞ e^{−ω}dω = 1 to check it. For the integral, the general identity ∫₀^∞ cos(ωx)/(1 + x²) dx = (π/2)e^{−|ω|} follows directly from the inversion formula at x = 0 with the cosine pair. Hence the answer is (1/2)(π/2)[e^{−|a−b|} + e^{−|a+b|}]. For a, b > 0 with a > b this is (π/4)(e^{−(a−b)} + e^{−(a+b)}).
> **Key point:** F{1/(1+x²)} = πe^{−|ω|}, so ∫₀^∞ cos(ωx)/(1+x²) dx = (π/2)e^{−|ω|}.

### Q173. [GATE-1] The Fourier integral representation of a function f is essentially:

> **Type:** MCQ
> **Answer:** The continuous-frequency limit of the Fourier series, in which the discrete sum over harmonics becomes an integral over ω with A(ω) and B(ω) as the continuous analogues of the coefficients (Option b).
> **Solution:** Let L → ∞ in the series: the fundamental π/L → 0 so the harmonic index becomes a continuous variable ω, the sum Σ(nπ/L) becomes ∫dω, and aₙ ≈ (π/L)A(ω) so the term aₙcos(nπx/L) → A(ω)cos(ωx). Option (a) is a statement about Fourier transforms, a different tool, though related. Option (c) mixes in the Laplace transform. Option (d) is false: the integral representation is not a discrete sum in any limit.
> **Key point:** The Fourier integral is the L → ∞ limit of the Fourier series: Σ → ∫, and the coefficients become continuous functions A(ω), B(ω).

### Q174. [GATE-2] Evaluate ∫₀^∞ (sin ax)/x dx using the Fourier integral theorem applied to the sign function, with a > 0.

> **Type:** MCQ
> **Answer:** π/2 ≈ 1.571 (Option a).
> **Solution:** Take f(x) = sgn x, which is odd, so B(ω) = (1/π)∫₋∞^∞ sgn(t)sin(ωt)dt = (2/π)∫₀^∞ sin(ωt)dt in the generalised sense, and the Fourier integral reads sgn x = (2/π)∫₀^∞ (sin ωx)/ω dω. Setting x = 0⁺, where the left side is 1, gives (2/π)∫₀^∞ (sin ωx)/ω dω = 1. Substituting u = ωx, so that dω = du/x and 1/ω = x/u, leaves the integral independent of x: ∫₀^∞ (sin u)/u du = π/2 ✓. The same value results for any a > 0 by scaling u = ax.
> **Key point:** ∫₀^∞ (sin ax)/x dx = π/2 for a > 0 — the Dirichlet integral, read off the Fourier integral of sgn x at x → 0⁺.

### Q175. [GATE-1] Evaluate ∫₀^∞ (1 − cos ax)/x² dx using the Fourier integral of a ramp function.

> **Type:** Numerical
> **Answer:** π|a|/2, so for a > 0 the value is πa/2.
> **Solution:** Differentiate with respect to a: d/da ∫(1 − cos ax)/x² dx = ∫ sin(ax)/x dx = π/2 for a > 0, by the Dirichlet integral ∫₀^∞(sin ax)/x dx = π/2. Integrating back from a = 0, where the integral is 0, gives the answer πa/2. For general a the result is π|a|/2, and the absolute value appears because the integrand is even in a. This is the cleanest general method for Fourier-integral evaluation: differentiate the target integral until it reduces to a known one, then integrate back using a known boundary value.
> **Key point:** ∫₀^∞ (1 − cos ax)/x² dx = π|a|/2, obtained by differentiating once to the Dirichlet integral.

### Q176. [GATE-1] Find the Fourier transform of the rectangular pulse of unit height and unit width, and describe its shape.

> **Type:** Numerical
> **Answer:** X(ω) = sin(ω/2)/(ω/2) = 2sin(ω/2)/ω, a sinc function: real, even, equal to 1 at ω = 0, and alternating in sign between its zeros at ω = 2πn (n ≠ 0).
> **Solution:** With f(t) = 1 for |t| < 1/2 and 0 elsewhere, X(ω) = ∫₋₁/₂^1/2 e^{−iωt} dt = 2sin(ω/2)/ω. The transform is the sinc function, whose value at the origin is 1 (the limit of sin u/u) and whose first zeros are at ω = ±2π, giving a main-lobe width of 4π in frequency. The transform is real and even because f is real and even, and it oscillates in sign beyond the first zeros, which is the unavoidable ringing of a hard-edged pulse.
> **Key point:** A rectangular pulse of unit width ↔ sin(ω/2)/(ω/2): real, even sinc with zeros at ω = 2πn.

### Q177. [GATE-1] The Fourier transform of the derivative f′(t) in terms of F(ω) is:

> **Type:** MCQ
> **Answer:** (jω)F(ω) for f continuous and vanishing at infinity (Option b). If f jumps at t = 0 the answer gains the constant (f(0⁺) − f(0⁻)) in frequency — a DC offset, not a delta in ω.
> **Solution:** Integration by parts gives ∫f′(t)e^{−iωt}dt = [f(t)e^{−iωt}]₋∞^∞ + iω∫f(t)e^{−iωt}dt, and the bracket vanishes when f decays at both ends, leaving (jω)F(ω). A jump at t = 0 is a different matter: in the distributional sense f′ contains [f]δ(t) with [f] = f(0⁺) − f(0⁻), and the transform of δ(t) is the constant 1, so the frequency-domain effect is an added DC level, not a spike at ω = 0. The confusion here is a reversal: a constant *in time* transforms to 2πf₀δ(ω), whereas a constant *in frequency* is a delta *in time*. Options (a) and (c) get the sign or the operation wrong.
> **Key point:** f′(t) ↔ jωF(ω) for continuous decaying f; a jump in f adds a constant [f] = f(0⁺) − f(0⁻) to the transform.

### Q178. State the time-shifting and frequency-modulation pair of Fourier transform properties.

> **Type:** Theory
> **Answer:** f(t − t₀) ↔ X(ω)e^{−iωt₀} and f(t)e^{iω₀t} ↔ X(ω − ω₀): a delay multiplies the spectrum by a phase, and multiplication by a complex exponential shifts the spectrum.
> **Solution:** Both follow from a change of variable or a direct substitution in the transform integral. The first is the statement that delay is a pure phase operation, which is why a matched filter's phase response is set by the propagation delay. The second is frequency translation — the basis of modulation, since multiplying a signal by cos(ω₀t) = (e^{iω₀t} + e^{−iω₀t})/2 produces two shifted copies of the spectrum and hence two sidebands. The duality between the two is the same duality as the scaling rule x → kx, with the roles of time and frequency exchanged.
> **Key point:** f(t − t₀) ↔ e^{−iωt₀}X(ω); multiplying by e^{iω₀t} shifts the spectrum to ω − ω₀.

### Q179. [GATE-2] A causal exponential e^{−at}u(t) has a Fourier transform that exists as an ordinary integral. State the transform and its magnitude, and note what happens as a → 0.

> **Type:** MCQ
> **Answer:** X(ω) = 1/(a + jω) for a > 0, |X(ω)| = 1/√(a² + ω²). As a → 0 the signal becomes u(t), whose transform is the distribution πδ(ω) + PV(1/(jω)) — it does not exist as an ordinary function (Option b).
> **Solution:** X(ω) = ∫₀^∞ e^{−(a + jω)t} dt = 1/(a + jω) for a > 0, with |X(ω)| = 1/√(a² + ω²) — a first-order low-pass with corner frequency a and phase −tan⁻¹(ω/a). As a → 0⁺ the signal becomes u(t), and the transform in the limit is πδ(ω) + PV(1/(jω)): the principal-value part is what survives from 1/(a + jω) as its real, even kernel, while the δ at ω = 0 is a genuine piece of the limit that PV(1/(jω)) alone does not contain. No ordinary function represents the transform of a non-decaying step, which is precisely why it must be treated as a distribution.
> **Key point:** e^{−at}u(t) ↔ 1/(a + jω); as a → 0 the transform becomes the principal value 1/(jω), not an ordinary function.

---

## Section 12. Rapid-fire recall set and dimension checks for Sections 1–11

### Q180. State the cross-product magnitude identity in a form that avoids computing the cross product.

> **Type:** Theory
> **Answer:** |**A** × **B**|² = |**A**|²|**B**|² − (**A**·**B**)², equivalently |**A** × **B**| = |**A**||**B**|sin θ.
> **Solution:** From the double-angle identity sin²θ = 1 − cos²θ together with **A**·**B** = |**A**||**B**|cos θ. The squared form is usually the faster route in numerical work because only the dot product and the two magnitudes are needed, and it is self-checking: a negative result signals an arithmetic error in the dot product.
> **Key point:** |**A** × **B**|² = |**A**|²|**B**|² − (**A**·**B**)² — avoids computing components.

### Q181. Quick check: what is the divergence of a constant vector field, and why does it force zero flux through every closed surface?

> **Type:** Conceptual
> **Answer:** Zero, because all partial derivatives of a constant vanish; by the divergence theorem the flux through any closed surface is then the integral of zero.
> **Solution:** The divergence involves differentiating each component with respect to its own coordinate, and constants have zero derivative. The geometric counterpart is that what enters a closed surface leaves it, so the net is zero. This is the simplest instance of the general statement that a field is solenoidal iff its net flux through every closed surface vanishes.
> **Key point:** div(constant) = 0 ⟹ zero flux through every closed surface.

### Q182. Quick check: is ∇ × **A** = 0 necessary, sufficient, or both for **A** to be a gradient field on all of R³?

> **Type:** Conceptual
> **Answer:** Both, on all of R³ (which is simply connected): a smooth field with zero curl on a simply connected domain is a gradient field.
> **Solution:** Necessity follows from curl(grad f) = 0. Sufficiency requires simple connectivity: the standard counterexample is the azimuthal field **A** = (−y/s², x/s², 0), which has zero curl away from the z-axis yet is not a gradient field on R³, because a loop encircling the axis has circulation 2π ≠ 0. On a simply connected domain no such obstruction exists, and the path-independence of the line integral follows.
> **Key point:** Curl-free ⟹ conservative on a simply connected domain; R³ qualifies, punctured space does not.

### Q183. Quick check: what is the line integral of a constant vector field around a closed loop?

> **Type:** Conceptual
> **Answer:** Zero, since the closed integral of any exact differential vanishes and a constant field's circulation is the flux of its zero curl.
> **Solution:** Either by Stokes's theorem, since the curl of a constant is zero, or directly by decomposing the loop into steps in each coordinate direction — the net displacement in each direction is zero, so the contributions cancel. Zero flux and zero circulation are both true of constant fields.
> **Key point:** ∮ constant field · d**r** = 0 around any closed loop.

### Q184. [GATE-1] Quick check: does the value of the Fourier series at an endpoint x = ±L depend on whether the extension is defined there?

> **Type:** Conceptual
> **Answer:** No — the series value there is always [f(L⁻) + f(L⁺)]/2, using the one-sided limits, regardless of what value is assigned at the single point x = L.
> **Solution:** Changing a function's value at a single point does not change any of its Fourier coefficients, since those are integrals and a single point has measure zero. The Dirichlet rule therefore reports the average of the limits, never the assigned point value. This is why a jump at the boundary is handled by the midpoint rule and not by "whatever was written at L."
> **Key point:** Endpoint series value is always the midpoint of the one-sided limits; the value at a single point never matters.

### Q185. Quick check: what happens to a Fourier series' coefficients as the period 2L grows for a fixed non-periodic function?

> **Type:** Conceptual
> **Answer:** The fundamental frequency π/L → 0, so the spectrum becomes continuous and the series becomes a Fourier integral.
> **Solution:** As L increases the harmonics πn/L pack ever more densely, and in the limit the discrete sum turns into an integral with the coefficient values becoming the continuous spectral density. This is the direct link between the two halves of the file: the Fourier series is the Fourier integral sampled at nπ/L, and Parseval becomes Parseval's integral form.
> **Key point:** 2L → ∞ turns the series into the Fourier integral: harmonics πn/L become a continuous ω axis.

### Q186. Dimension check: what are the units of ∮**F**·d**r** when **F** is in N and **r** in m?

> **Type:** Conceptual
> **Answer:** J (joules), the unit of work.
> **Solution:** N · m = J. This is the reason the line integral of a force is called work, and the reason a force field with zero circulation does no net work around any closed path — the mechanical statement of energy conservation. If **F** were a velocity in m/s instead, the same integral would be m²/s, a rate of length traversed, which is why a potential field is meaningful for both.
> **Key point:** [∮F·dr] = N·m = J — the line integral of a force is work.

### Q187. Dimension check: what are the units of the flux of an electric field E in V/m through a surface in m²?

> **Type:** Conceptual
> **Answer:** V·m (volt-metres).
> **Solution:** Multiplying, (V/m)(m²) = V·m. Do not confuse this with the induced emf, which is the circulation ∮**E**·d**r** = (V/m)(m) = V; flux and circulation differ by one power of length because one integrates over an area and the other along a length. For a closed surface the flux of **E** is a further special case, equal to Q_enclosed/ε₀ in coulombs by Gauss's law, so the units must be consistent with whichever reading is used.
> **Key point:** Flux of E in V/m through m² is V·m; the emf ∮E·dr around the boundary of the same area is V.

### Q188. Dimension check: verify that the Fourier series of a function with units of volts produces a result with units of volts.

> **Type:** Conceptual
> **Answer:** Yes — every coefficient aₙ, bₙ carries the same units as f, since each is a constant multiple of an integral of f against a dimensionless kernel.
> **Solution:** The cosine and sine kernels are dimensionless (they are pure functions of a ratio x/L), and the factor 1/L has units of 1/length, which exactly cancels the length in the integration variable, so aₙ has the same units as f. The same holds for the Fourier transform's spectral density, which has units of [f]·s, the reciprocal of the frequency resolution. Checking units this way catches normalisation errors immediately.
> **Key point:** Fourier coefficients carry the units of f; the 1/L factor cancels the integration length.

### Q189. Quick check: why is the vector Laplacian of a component-wise function not the same as the scalar Laplacian of each component alone?

> **Type:** Conceptual
> **Answer:** Because ∇²**A** defined as ∇(∇·**A**) − ∇ × (∇ × **A**) is not the component-wise ∇²; the double-curl identity contains the extra term ∇(∇·**A**).
> **Solution:** Writing out the double curl in indices, (∇ × (∇ × **A**))ᵢ = ∇²Aᵢ − ∂ᵢ(∇·**A**), so ∇²**A** = ∇(∇·**A**) − ∇ × (∇ × **A**). If one applies the scalar Laplacian to each component and calls that ∇²**A**, one omits the gradient-of-divergence term and gets a different (and wrong) answer whenever the divergence is non-constant. Both routes coincide for a field whose divergence is a constant, and differ whenever the divergence varies.
> **Key point:** ∇²**A** (component-wise) is not ∇ × (∇ × **A**); they differ by ∇(∇·**A**).

### Q190. Quick check: for a purely radial field **A** = A_r**â**_r in spherical coordinates, which derivatives of A_r appear in the divergence?

> **Type:** Conceptual
> **Answer:** Only the radial derivative, appearing as (1/r²)∂(r²A_r)/∂r — the angular derivatives drop out because A_θ = A_φ = 0 and A_r has no θ or φ dependence.
> **Solution:** Both angular terms in the divergence formula contain ∂/∂θ or ∂/∂φ of the component with the θ or φ index, and both components vanish, so those terms are zero regardless of any A_r dependence. The surviving term carries the r² weight because the volume element is r² sin θ dr dθ dφ. For A_r = r^{n}, this gives div = (n+2)r^{n−1}, so the Laplacian of r⁴ is 20r².
> **Key point:** Purely radial field: div = (1/r²)(r²A_r)_r, and for A_r = rⁿ it is (n+2)r^{n−1}.

### Q191. Quick check: in the Fourier integral, what value does the integral take at a point of jump discontinuity?

> **Type:** Conceptual
> **Answer:** The midpoint of the two one-sided limits, [f(x⁺) + f(x⁻)]/2, exactly as in the series case.
> **Solution:** The proof of the Fourier integral theorem localises a sinc-like kernel around the point of interest; when f is continuous the kernel's integral concentrates all its weight on f(x), and when there is a jump the symmetric kernel picks up equal contributions from both sides, giving the average. This is the same statement as the Dirichlet midpoint rule for series and the two arise from the same argument.
> **Key point:** Fourier integral at a jump gives (f⁺ + f⁻)/2 — identical to the series rule.

### Q192. Quick check: is the Fourier series of a product of two functions the product of their series?

> **Type:** Conceptual
> **Answer:** No — the coefficients of the product are the convolution (discrete) of the two coefficient sequences, not their term-by-term product.
> **Solution:** Multiplying two sums gives double sums, which can be regrouped by the frequency of the resulting term, producing sums over all pairs of indices adding to a given n — a convolution. Since the sequences are infinite, the product series generally has infinitely many coefficients where each factor had only one, which is exactly how multiplication generates new frequencies. This is the discrete analogue of the time-multiplication/frequency-convolution dual pair.
> **Key point:** Coefficients of a product = discrete convolution of coefficients, not their product.

### Q193. Quick check: what is the total flux of the field **F** = (1/x, 1/y, 1/z) through the unit sphere, and why is the divergence theorem unusable?

> **Type:** Conceptual
> **Answer:** The divergence is −(1/x² + 1/y² + 1/z²), which is not integrable over the ball because it blows up on the coordinate planes, so the theorem's hypotheses fail; the field is not even defined on the axes.
> **Solution:** The divergence theorem requires **F** to be continuously differentiable on a neighbourhood of the enclosed volume, and 1/x is singular on the x = 0 plane, which cuts through the whole ball. This is the same structural failure as for a field with a 1/ρ singularity on an interior axis: a singularity anywhere inside the surface, not merely on the curve or axis of integration. The lesson is to check the field's domain before reaching for the theorem.
> **Key point:** A divergence theorem calculation requires the field to be C¹ everywhere inside; interior singularities void it.

---

## Section 13. Vector-calculus GATE set

### Q194. [GATE-1] If **F** = (x²y, xy², xyz), the divergence of **F** is:

> **Type:** MCQ
> **Answer:** 5xy (Option d).
> **Solution:** ∇·**F** = ∂(x²y)/∂x + ∂(xy²)/∂y + ∂(xyz)/∂z = 2xy + 2xy + xy = 5xy. Each term differentiates the component with respect to its own coordinate, holding the others fixed — ∂(x²y)/∂x = 2xy because y is constant, and ∂(xyz)/∂z = xy. The terms that do not involve the differentiation variable simply disappear.
> **Key point:** div(x²y, xy², xyz) = 2xy + 2xy + xy = 5xy.

### Q195. [GATE-1] The curl of the field **A** = (x, y, z⁴) is:

> **Type:** MCQ
> **Answer:** **0** (Option c).
> **Solution:** (∇ × **A**)ₓ = ∂A_z/∂y − ∂A_y/∂z = 0 − 0 = 0; (∇ × **A**)_y = ∂A_x/∂z − ∂A_z/∂x = 0 − 0 = 0; (∇ × **A**)_z = ∂A_y/∂x − ∂A_x/∂y = 0 − 0 = 0. Each component of **A** depends on its own coordinate only, so every cross-derivative vanishes. The field is irrotational, and in fact **A** = ∇(x²/2 + y²/2 + z⁵/5), so its circulation around any closed loop vanishes.
> **Key point:** A field whose components each depend on one coordinate only has zero curl.

### Q196. [GATE-2] Evaluate ∮C (y dx − x dy) where C is the circle x² + y² = 4 traversed clockwise.

> **Type:** MCQ
> **Answer:** +8π ≈ 25.13 (Option c).
> **Solution:** Green's theorem with P = y and Q = −x gives the planar curl Q_x − P_y = −1 − 1 = −2, so the counterclockwise circulation is ∬(−2) dA = −2 · (area 4π) = −8π. Reversing the traversal to clockwise negates the value, giving +8π ≈ 25.13. Direct parametrisation confirms it: for clockwise traversal x = 2cos t, y = −2 sin t, t ∈ [0, 2π], giving dx = −2 sin t dt, dy = −2 cos t dt, and y dx − x dy = 4sin²t dt + 4cos²t dt = 4 dt, which integrates to 8π ✓.
> **Key point:** ∮(y dx − x dy) = +2πR² clockwise, −2πR² counterclockwise; here R = 2 so it is +8π.

### Q197. [GATE-2] The total flux of **F** = (x, y, z) out of the cylinder x² + y² = 4, 0 ≤ z ≤ 3, is:

> **Type:** MCQ
> **Answer:** 36π ≈ 113.1 (Option d).
> **Solution:** ∇·**F** = 1 + 1 + 1 = 3, a constant, and the cylinder's volume is πR²h = π(4)(3) = 12π, so the flux is 3 · 12π = 36π ≈ 113.1. Face check: on the curved side **F**·**n̂** = 2 with area 2πRh = 12π, giving 24π; on the top cap (z = 3, normal **k̂**) **F**·**n̂** = 3 over area 4π, giving 12π; on the bottom cap (z = 0, normal −**k̂**) the flux is −3 · 4π = −12π. Total = 24π + 12π − 12π = 36π ✓.
> **Key point:** Constant divergence 3 × cylinder volume 12π = 36π; the caps' fluxes cancel but the curved surface's 24π does not.

### Q198. [GATE-1] The line integral of a gradient field around a closed path is:

> **Type:** MCQ
> **Answer:** Zero (Option c).
> **Solution:** By the fundamental theorem of calculus for line integrals, ∮C ∇f·d**r** = 0, because f returns to its starting value. Equivalently, Stokes's theorem gives ∫∫S(∇ × ∇f)·d**S** = 0. Option (a) is the divergence theorem's statement, option (b) holds only for constant fields, and option (d) is false in general — it is the integral around a closed path, not along a segment, that vanishes.
> **Key point:** ∮∇f·d**r** = 0 for every closed path — a conservative field does no net work.

### Q199. [GATE-2] Find the flux of **F** = (x²i + y²j) out of the closed surface of the cube 0 ≤ x, y, z ≤ 2.

> **Type:** NAT
> **Answer:** 32
> **Solution:** ∇·**F** = ∂(x²)/∂x + ∂(y²)/∂y + ∂0/∂z = 2x + 2y. Integrating over the cube 0 ≤ x, y, z ≤ 2: ∫₀²∫₀²∫₀²(2x + 2y) dV = (∫₀²2x dx)(2)(2) + (2)(∫₀²2y dy)(2) = (4)(2)(2) + (2)(4)(2) = 16 + 16 = 32. Face check: on x = 2, **F**·**i** = 4 over area 4, giving 16; on y = 2, 16; the x = 0, y = 0 and both z-faces contribute 0. Total = 32 ✓.
> **Key point:** Flux of (x², y², 0) through the 2-cube = 16 + 16 = 32, from the x = 2 and y = 2 faces only.

### Q200. [GATE-2] If **F** = (2xy, x² + 2yz, 3z²), verify that the circulation of **F** around the circle x² + y² = 1, z = 0, counterclockwise, is zero, and identify why.

> **Type:** MCQ
> **Answer:** 0, because ∇ × **F** = 0 everywhere (Option a).
> **Solution:** The curl is (∂F_z/∂y − ∂F_y/∂z, ∂F_x/∂z − ∂F_z/∂x, ∂F_y/∂x − ∂F_x/∂y) = (0 − 2y, 0 − 0, 2x − 2y). The z-component 2x − 2y integrates to zero over the unit disk by odd symmetry, and the other components do not contribute since the disk's normal is **k̂**. So the circulation is 0. In fact the field is not curl-free; it is the symmetry of the loop that forces the value. A cleaner statement: on the unit disk ∫∫(2x − 2y) dA = 0 by oddness.
> **Key point:** Stokes gives ∫∫(2x − 2y) dA over the disk, which vanishes by odd symmetry — the zero is from symmetry, not from zero curl.

### Q201. [GATE-2] Evaluate ∮C **F**·d**r** for **F** = (x, −y, 0) around the unit circle in the xy-plane, counterclockwise, using Stokes's theorem.

> **Type:** MCQ
> **Answer:** 0 (Option a).
> **Solution:** The curl is (∂0/∂y − ∂(−y)/∂z, ∂(x)/∂z − ∂0/∂x, ∂(−y)/∂x − ∂(x)/∂y) = (0 − 0, 0 − 0, 0 − 0) = **0**: F_y = −y has no x-dependence and F_x = x has no y-dependence, so both cross-derivatives are zero. Stokes's theorem then gives a circulation of 0. Direct parametrisation confirms it: **r**(t) = (cos t, sin t, 0) gives **F**·**r**′(t) = −cos t sin t − sin t cos t = −sin 2t, whose integral over 0 to 2π is 0 ✓. The integrand is the exact differential of (x² − y²)/2, so the circulation vanishes.
> **Key point:** ∮(x dx − y dy) = 0 for the unit circle: the integrand is the exact differential of (x² − y²)/2.

### Q202. [GATE-1] The value of ∮C (x² dy − y² dx) around the unit circle traversed counterclockwise is:

> **Type:** MCQ
> **Answer:** 0 (Option a).
> **Solution:** Green's theorem with P = −y² and Q = x² gives Q_x − P_y = 2x − (−2y) = 2x + 2y, and ∫∫(2x + 2y) dA over the unit disk vanishes because both terms are odd. Direct check: x = cos t, y = sin t, dx = −sin t dt, dy = cos t dt, so the integrand is cos²t cos t dt − sin²t(−sin t) dt = (cos³t + sin³t) dt, and ∫₀^{2π}(cos³t + sin³t) dt = 0 since each cube integrates to zero over a full period. Both routes give 0. The temptation to get 2π from the "area" formula does not apply, because that formula needs the specific form y dx − x dy.
> **Key point:** ∮(x²dy − y²dx) = 0 over the unit circle: the planar curl 2x + 2y is odd and integrates to zero.

### Q203. [GATE-2] A vector field is given in cylindrical components as **A** = (ρ**â**_ρ + ρ sin θ **â**_θ + 0). Compute its divergence.

> **Type:** MCQ
> **Answer:** div **A** = 2 + cos θ (Option b).
> **Solution:** The cylindrical divergence formula is (1/ρ)∂(ρA_ρ)/∂ρ + (1/ρ)(∂A_θ/∂θ) + ∂A_z/∂z. The first term is (1/ρ)∂(ρ²)/∂ρ = 2; the second is (1/ρ)(ρ cos θ) = cos θ; the third is 0 since A_z = 0. So div **A** = 2 + cos θ. Independent check in Cartesian: ρ**â**_ρ = (x, y) and ρ sin θ**â**_θ = y(−sin θ, cos θ) = (−y sin θ, y cos θ), so **A** = (x − y sin θ, y + y cos θ, 0) and div **A** = 1 + (1 + cos θ) = 2 + cos θ ✓. Dropping the θ-dependence of the second component would lose the cos θ term.
> **Key point:** div **A** = (1/ρ)(ρA_ρ)_ρ + (1/ρ)(∂A_θ/∂θ) + (∂A_z/∂z) = 2 + cos θ for these components.

### Q204. [GATE-2] Find the total flux of **F** = (x², y², z²) out of the unit sphere, and state the additional symmetry argument that makes the answer zero.

> **Type:** NAT
> **Answer:** 0
> **Solution:** ∇·**F** = 2x + 2y + 2z, and the unit ball is symmetric under x → −x, y → −y, z → −z individually, so ∫∫∫x dV = ∫∫∫y dV = ∫∫∫z dV = 0. Hence the flux is 0. Equivalently on the sphere **n̂** = (x, y, z) so **F**·**n̂** = x³ + y³ + z³, and each cube integrates to zero over the sphere. The relevant symmetry is inversion symmetry about each coordinate plane, not just central inversion.
> **Key point:** Flux of (x², y², z²) through any region symmetric about all three coordinate planes is 0.

### Q205. [GATE-2] The circulation of **F** = (−y, x, 0) around a closed loop that encircles the z-axis once at radius s is:

> **Type:** MCQ
> **Answer:** 2πs², so it scales as the area of the loop, not as a constant (Option c).
> **Solution:** Direct integration: with x = s cos t, y = s sin t on 0 ≤ t ≤ 2π, dx = −s sin t dt and dy = s cos t dt, so −y dx + x dy = (s²sin²t + s²cos²t) dt = s² dt, and the integral is 2πs². Stokes's theorem agrees: the curl is (0, 0, 2) and the flat disk's normal is **k̂**, so the circulation is 2 · πs² = 2πs² ✓. The value therefore grows with s, because the curl is a uniform field whose flux through the disk is proportional to the disk's area. Only a field like (−y/ρ², x/ρ², 0) gives a loop-independent circulation, since its flux concentrates into a fixed 2π near the axis.
> **Key point:** ∮(−y dx + x dy) = 2πs² for a circle of radius s — it scales as area because the curl is the uniform field (0, 0, 2).

### Q206. [GATE-2] A vector field **F** satisfies ∇·**F** = 0 in a region and **F**·**n̂** = 0 on the boundary. What is the total outward flux, and is the field necessarily zero inside?

> **Type:** MCQ
> **Answer:** The total flux is 0, and no — the field need not be zero inside, because the given data are Neumann-type conditions that leave the interior undetermined (Option c).
> **Solution:** The divergence theorem gives ∫∫S **F**·**n̂** dS = ∫∫∫ div **F** dV = 0, since the divergence is zero. But the interior is not determined: **F** = (0, 0, z) has div = 1, and **F** = (−y, x, 0) has div = 0 with **F**·**n̂** = 0 on the unit sphere, yet it is plainly nonzero inside. That field satisfies both hypotheses and is not zero, which settles the second part.
> **Key point:** div **F** = 0 and **F**·**n̂** = 0 on S force zero total flux but not a zero field — (−y, x, 0) on the unit sphere is a counterexample.

### Q207. [GATE-2] Compute the flux of **F** = (x, y, z) through the paraboloid z = 4 − x² − y² (0 ≤ r ≤ 2) with upward normal.

> **Type:** NAT
> **Answer:** 16π ≈ 50.27
> **Solution:** ∇·**F** = 3, and the volume between the paraboloid and z = 0 is ∫∫_D(4 − r²)dA over r ≤ 2 = 2π∫₀²(4r − r³)dr = 2π(2r² − r⁴/4)₀² = 2π(8 − 4) = 8π. Multiplying by 3 gives 24π ≈ 75.40, all of it through the paraboloid because the disk at z = 0 contributes 0. Direct check on the paraboloid: **n̂** dS = (2x, 2y, 1)dA and **F** = (x, y, 4 − r²), so **F**·d**S** = 2r² + 4 − r² = 4 + r², and ∫∫_D(4 + r²)dA = 2π∫₀²(4r + r³)dr = 2π(8 + 4) = 24π ✓. The volume route agrees: 3 · 8π = 24π.
> **Key point:** Flux of **r** through a paraboloid cap = 3 × its volume; here 3 × 8π = 24π.

---

## Section 14. Fourier-series GATE set

### Q208. [GATE-1] The Fourier series of f(x) = |x| on (−π, π) is:

> **Type:** MCQ
> **Answer:** π/2 − (4/π)Σ_{n odd} cos(nx)/n² (Option b).
> **Solution:** f is even, so only cosine terms appear, and a₀ = (1/π)∫₋π^π|x|dx = (1/π)(π²) = π, so a₀/2 = π/2. For n ≥ 1, aₙ = (2/π)∫₀^π x cos(nx)dx = (2/π)[(x sin nx)/n + cos nx/n²]₀^π = (2/π)((−1)ⁿ − 1)/n², which is 0 for even n and −4/(πn²) for odd n. Hence f(x) = π/2 − (4/π)Σ_{n odd} cos(nx)/n², option (b).
> **Key point:** |x| on (−π, π) has a₀ = π and aₙ = 2((−1)ⁿ − 1)/(πn²), so only odd harmonics with −4/(πn²).

### Q209. [GATE-1] A square wave of amplitude 1 and period 2π has Fourier coefficients that:

> **Type:** MCQ
> **Answer:** Decay as 1/n with only odd n present, alternating in sign (Option a).
> **Solution:** The square wave is odd, so bₙ alone survives, and its quarter-period symmetry (f(x + π) = −f(x)) kills all even n. The jump discontinuity forces |bₙ| ~ 1/n, and the sign alternates with n. Continuity of only the zeroth derivative means there is no 1/n² improvement, and the presence of even harmonics would contradict the half-wave antisymmetry.
> **Key point:** Jump ⟹ 1/n decay; half-wave odd symmetry ⟹ only odd harmonics; odd f ⟹ sine only.

### Q210. [GATE-2] The number of non-zero Fourier coefficients for f(x) = cos(3x) + 4cos(5x) on (−π, π) is:

> **Type:** MCQ
> **Answer:** 2 (Option c).
> **Solution:** A finite sum of distinct harmonics is already a trigonometric polynomial, and the Fourier coefficients of a trigonometric polynomial are exactly the ones in the polynomial: a₃ = 1, a₅ = 4, everything else 0. Linearity of the coefficient functional guarantees this. The infinite-series machinery is unnecessary; the series terminates.
> **Key point:** A trigonometric polynomial has finitely many non-zero coefficients: a₃ = 1, a₅ = 4.

### Q211. [GATE-2] If f has period 2L, then the value of the Fourier series at x = L equals:

> **Type:** MCQ
> **Answer:** [f(L⁻) + f(L⁺)]/2, the average of the one-sided limits (Option d).
> **Solution:** x = L is the periodic continuation point, so the Dirichlet midpoint rule applies: the series takes the average of the left and right limits of the periodic extension. A different answer would require f to be continuous there. The rule is unchanged by the value assigned at the single point L, which never affects the coefficients.
> **Key point:** At a jump the series gives (f⁻ + f⁺)/2, including at the endpoints ±L.

### Q212. [GATE-1] The Fourier series coefficients of the constant function f(x) = 3 on (−π, π) are:

> **Type:** MCQ
> **Answer:** a₀ = 6, aₙ = bₙ = 0 for n ≥ 1 (Option a).
> **Solution:** a₀ = (1/π)∫₋π^π 3 dx = 6, and every cosine or sine coefficient vanishes because ∫₋π^πcos(nx)dx = 0 and ∫₋π^πsin(nx)dx = 0 for n ≥ 1. So the series is the single term a₀/2 = 3 ✓. This confirms that the DC term of a series is the mean value of the function.
> **Key point:** f = 3: a₀/2 = 3 with all other coefficients zero — the DC level is the mean.

### Q213. [GATE-2] The alternating sum Σ_{k=0}^∞ (−1)^k/(2k+1) = 1 − 1/3 + 1/5 − 1/7 + 1/9 − ⋯ is equal to:

> **Type:** MCQ
> **Answer:** π/4 ≈ 0.7854 (Option c).
> **Solution:** From the square-wave series π/4 − (4/π)Σ_{n odd} sin(nx)/n, setting x = π/2 makes every odd sine equal (−1)^{(n−1)/2}, reproducing the alternating sum 1 − 1/3 + 1/5 − 1/7 + ⋯ and giving π/4. Equivalently this is tan⁻¹(1) = π/4 by the standard Taylor series of arctangent.
> **Key point:** Leibniz series 1 − 1/3 + 1/5 − 1/7 + ⋯ = π/4, read off the square wave at x = π/2.

### Q214. [GATE-2] If the Fourier series of f is differentiated term by term and the differentiated series converges to g, then:

> **Type:** MCQ
> **Answer:** g = f′ wherever f′ exists and is piecewise continuous, and the term-by-step condition is that the coefficients decay fast enough (1/n² or faster) for Σ n aₙ and Σ n bₙ to converge (Option a).
> **Solution:** Term-by-term differentiation multiplies the coefficients by n, so absolute convergence of the differentiated series requires Σ n|aₙ| < ∞, i.e. 1/n² decay. Under that condition the classical differentiation theorem applies and the derivative series sums to f′ at points where f′ exists, while at a corner it sums to the average of the one-sided derivatives. Without the decay condition the differentiation is not justified, which is the reason jumps and corners are handled by integrating rather than differentiating.
> **Key point:** Differentiating a Fourier series requires coefficients decaying as 1/n²; the result equals f′ at smooth points and the average slope at a corner.

### Q215. [GATE-1] Parseval's identity for f on (−L, L) states:

> **Type:** MCQ
> **Answer:** (1/L)∫₋Lᴸ|f|²dx = (a₀²/2) + Σ(aₙ² + bₙ²) (Option b).
> **Solution:** Parseval's identity is the L²-norm version of Parseval's equation for an orthonormal basis; on (−L, L) the orthogonal basis is cos(nπx/L), sin(nπx/L) with squared norm L each, and the normalisation 1/L on the integral balances the 1/2 on a₀. Numerically √(1/L) times the LHS is the L² norm of the coefficient vector, so the identity says the function and its coefficients carry the same energy.
> **Key point:** (1/L)∫|f|² = a₀²/2 + Σ(aₙ² + bₙ²) — the coefficients hold the function's energy.

### Q216. [GATE-2] For f(x) = x on (−π, π), the value of ∫₋π^π x² dx as predicted by Parseval is:

> **Type:** MCQ
> **Answer:** 4π³/3 (Option c).
> **Solution:** f = x has bₙ = 2(−1)^{n+1}/n and a₀ = aₙ = 0, so Parseval gives (1/π)∫₋π^π x²dx = Σ 4/n², hence ∫₋π^π x² dx = 4π Σ_{n=1}^∞ 1/n² = 4π(π²/6) = 4π³/3 ✓, matching the direct integration of x². This is a useful check: the direct integral is 2π³/3 for a half-range, and the full-range value is twice that.
> **Key point:** Parseval on f = x: (1/π)(2π³/3) = 4Σ1/n², recovering Σ1/n² = π²/6.

### Q217. [GATE-2] The half-range cosine series of f(x) = x on (0, L) is:

> **Type:** MCQ
> **Answer:** (2L/π)Σ_{n=1}^∞ (−1)^{n+1} cos(nπx/L)/n² (Option d).
> **Solution:** A half-range cosine series uses cos(nπx/L) with aₙ = (2/L)∫₀ᴸ x cos(nπx/L)dx. Integrating by parts with k = nπ/L, ∫₀ᴸ x cos(kx)dx = [x sin(kx)/k + cos(kx)/k²]₀ᴸ, and since sin(nπ) = 0 the result is ((−1)ⁿ − 1)/k². Hence aₙ = (2/L)((−1)ⁿ − 1)(L²/(n²π²)) = 2L((−1)ⁿ − 1)/(n²π²), which is 0 for even n and −4L/(n²π²) for odd n. So f(x) = −(4L/π²)Σ_{n odd} cos(nπx/L)/n², which is option (d).
> **Key point:** Half-range cosine of f = x on (0, L): aₙ = 2L((−1)ⁿ − 1)/(n²π²), nonzero only for odd n.

### Q218. [GATE-1] Gibbs' phenomenon in a Fourier series manifests as:

> **Type:** MCQ
> **Answer:** Persistent overshoot and ringing of about 9% of the jump height near discontinuities, which does not diminish as more terms are added (Option c).
> **Solution:** Near a jump the partial sums convolve f with the Dirichlet kernel, whose oscillatory lobes retain a fixed relative amplitude (the overshoot is about 0.089 times the jump, independent of N) while their width shrinks as 1/N. So adding terms sharpens the transition without reducing the overshoot. The limit converges in the sense of the midpoint rule, not uniformly, which is why uniform convergence fails exactly where f is discontinuous.
> **Key point:** Gibbs: ~9% overshoot persists for all N; only the ringing's width shrinks like 1/N.

### Q219. [GATE-2] The Fourier series of an even function contains:

> **Type:** MCQ
> **Answer:** Only cosine terms (a₀ and the aₙ), with all bₙ = 0 (Option a).
> **Solution:** Under x → −x, cos(nx) is unchanged and sin(nx) changes sign, so an even f's projection onto each sine vanishes while its cosine projections survive. Correspondingly an odd f has only sine terms. The tests are cheap: if a function is symmetric about the y-axis, drop the sines before computing any integral.
> **Key point:** Even f ⟹ cosine terms only; odd f ⟹ sine terms only.

### Q220. [GATE-2] If aₙ, bₙ = O(1/n³) for all n, then the Fourier series:

> **Type:** MCQ
> **Answer:** Converges absolutely and uniformly, and may be differentiated term by term twice before the differentiated series loses absolute convergence (Option d).
> **Solution:** Absolute convergence of the original series follows from Σ1/n³ < ∞, and uniform convergence follows from the Weierstrass M-test, so the sum is a continuous function. Differentiating once multiplies the coefficients by n, giving O(1/n²) — still absolutely convergent, so one derivative is justified. Differentiating twice gives O(1/n), conditionally convergent. The condition is thus "differentiable k times if the coefficients are O(1/n^{k+1})."
> **Key point:** Coefficients O(1/n^{k+1}) allow k term-by-term differentiations; here 1/n³ allows one safe differentiation.

---

## Section 15. Synthesis problems: Fourier and vector calculus in one problem

### Q221. A dielectric slab of thickness L, permittivity ε, and area A carries a uniform free charge density ρ₀. Find the electric field using Gauss's law and the potential, and compare with the parallel-plate capacitance.

> **Type:** Numerical
> **Answer:** E = ρ₀L/(2ε) at the mid-plane for an isolated slab, and V = ρ₀L²/(2ε) between the faces; with field excluded outside, the equivalent capacitance is C = εA/L.
> **Solution:** Gauss's law over a pillbox of area A centred in the slab encloses ρ₀AL, so εEA = ρ₀AL and E = ρ₀L/(2ε), with the field direction along the slab normal. The potential difference between the two faces is V = EL = ρ₀L²/(2ε). If the two faces are metallised, the field is confined and the capacitance is C = εA/L, the standard parallel-plate value; the isolated-slab factor of 1/2 is exactly the consequence of the field extending on both sides.
> **Key point:** A uniformly charged slab gives E = σ/(2ε) inside and σ/ε when metallised — the factor of 2 is the field-sharing effect.

### Q222. [GATE-2] Consider f(x) = x² on (−π, π) and the PDE u_t = u_xx with u(0, x) = x², u(t, ±π) = 0. Express u(t, x) as a Fourier series.

> **Type:** Numerical
> **Answer:** u(t, x) = π²/3 + 4Σ_{n=1}^∞ (−1)ⁿ e^{−n²t} cos(nx), with a₀ = 2π² so a₀/2 = π²/3 and aₙ = 4(−1)ⁿ/n².
> **Solution:** f is even, so only cosine terms: aₙ = (1/π)∫₋π^π x²cos(nx)dx = (2/π)∫₀^π x²cos(nx)dx = (2/π)[x²sin(nx)/n + 2x cos(nx)/n² − 2sin(nx)/n³]₀^π = (2/π)(2π(−1)ⁿ/n²) = 4(−1)ⁿ/n², and a₀/2 = (1/π)·(2π³/3)/2 = π²/3 ✓. The heat equation decays mode n by e^{−n²t}, giving the stated solution. As t → 0 the series returns x², and as t → ∞ it relaxes to π²/3, the mean value, exactly as a periodic diffusion problem must.
> **Key point:** Heat equation: mode n decays as e^{−n²t}; the steady state is the mean of the initial data, π²/3 here.

### Q223. A string of length L fixed at both ends has the normal modes of vibration. State the frequencies and the zero modes, and connect them to the Fourier series of the initial shape.

> **Type:** Theory
> **Answer:** Modes are sin(nπx/L) with ωₙ = cnπ/L for n = 1, 2, 3, and so on; n = 0 is a rigid translation, not a vibration, so there is no zero-frequency normal mode. The shape at time zero is expanded in the half-range sine series, so the mode amplitudes are exactly the Fourier sine coefficients of the plucked profile.
> **Solution:** Separation of variables with the fixed-end conditions gives a spatial factor sin(nπx/L) and a time factor cos(ωₙt) with ωₙ² = c²(nπ/L)². n = 0 would give the spatially constant function, which vanishes at x = 0 and x = L, so it is the trivial solution and is excluded. The initial shape f(x) is written in the half-range sine expansion, so the mode amplitudes are the bₙ of that series — the same coefficients, and this is why plucking a string is a Fourier problem in disguise.
> **Key point:** ωₙ = cnπ/L, n ≥ 1; no zero mode; pluck amplitudes = half-range sine coefficients.

### Q224. The stream function of a 2D incompressible flow is ψ = 2x. Find the velocity field in Cartesian and polar forms and identify the flow.

> **Type:** Numerical
> **Answer:** **v** = (0, −2), a uniform flow in the −y direction; in polar, v_ρ = −2 sin θ and v_θ = −2 cos θ.
> **Solution:** With v_x = ∂ψ/∂y and v_y = −∂ψ/∂x, ψ = 2x gives v_x = 0 and v_y = −2, so the flow is uniform and parallel to −y. Converting with x = ρcos θ, ψ = 2ρcos θ, and the polar relations v_ρ = (1/ρ)∂ψ/∂θ and v_θ = −∂ψ/∂ρ gives v_ρ = (1/ρ)(−2ρ sin θ) = −2 sin θ and v_θ = −2cos θ. Verifying continuity, (1/ρ)∂(ρv_ρ)/∂ρ + (1/ρ)∂v_θ/∂θ = (1/ρ)(−2 sin θ) + (1/ρ)(2 sin θ) = 0 ✓. The vorticity vanishes as well: ω = (1/ρ)[∂(ρv_θ)/∂ρ − ∂v_ρ/∂θ] = (1/ρ)[∂(−2ρcos θ)/∂ρ − ∂(−2 sin θ)/∂θ] = (1/ρ)(−2cos θ + 2cos θ) = 0, as it must for a uniform flow. (Keeping only the ∂(ρv_θ)/∂ρ term and dropping the outer ρ is the trap that would wrongly report a nonzero vorticity.)
> **Key point:** In 2D, v_ρ = (1/ρ)ψ_θ and v_θ = −ψ_ρ, so ψ = 2x is the uniform flow **v** = (0, −2), i.e. v_ρ = −2 sin θ, v_θ = −2cos θ.

### Q225. Use Fourier-series reasoning to show that a function's mean value is recovered by a single large low-pass kernel, and identify the theorem.

> **Type:** Conceptual
> **Answer:** The approximate-identity theorem: convolving f with a low-pass kernel normalised to unit area, (f * K_N)(x₀) → f(x₀) at continuity points and to (f⁺ + f⁻)/2 at a jump. A plain interval mean does not do this — (1/2L)∫₋Lᴸ f → the global mean, not f(x₀).
> **Solution:** Fourier-series partial sums are f convolved with the Dirichlet kernel D_N/(2π), whose mass concentrates near the origin, so the convolution tends to f(x₀) wherever f is continuous and to the average of the one-sided limits at a jump. Substituting the Fejér kernel — the triangular weight (1 − n/(N+1)) on the partial sums — makes the convergence uniform and unconditional, and is the cleaner statement of the theorem. The same fact in continuous frequency is the inversion formula f(x) = (1/2π)∫F(ω)e^{iωx}dω, whose kernel also has unit area. The engineering reading is that an ideal low-pass filter passes the mean value and nothing finer; the wrong form to write is the bare interval average, which is a different integral and converges only to the overall mean.
> **Key point:** Low-pass kernels of unit area approximate the identity — f at continuity points, the midpoint at a jump; a bare interval mean gives the global mean instead.

### Q226. [GATE-2] Find the work done by a force field **F** = (2xy, x², z) in moving a particle along the parabola y = x², z = 0, from x = 0 to x = 2.

> **Type:** Numerical
> **Answer:** 16 J
> **Solution:** Parametrise by t = x: **r**(t) = (t, t², 0), 0 ≤ t ≤ 2, so **r**′(t) = (1, 2t, 0). On the path **F** = (2t·t², t², 0) = (2t³, t², 0), and **F**·**r**′(t) = 2t³·1 + t²·(2t) = 4t³, so W = ∫₀²4t³dt = [t⁴]₀² = 16 J. Independent check: the curl is (0 − 0, 0 − 0, 2x − 2x) = 0, so **F** is conservative with potential φ = x²y + z²/2, and φ(2, 4, 0) − φ(0, 0, 0) = 4·4 + 0 = 16 J ✓.
> **Key point:** Work along a parametrised curve is ∫**F**·**r**′dt; here 4t³ integrates to 16 J, confirmed by the potential difference since the curl is zero.

### Q227. [GATE-1] A signal x(t) = cos(100πt) is sampled at 200 Hz. Identify the aliasing and the reconstruction frequency.

> **Type:** Numerical
> **Answer:** No aliasing: f_s = 200 Hz exceeds the Nyquist rate 2f = 100 Hz, so the tone reconstructs exactly at 50 Hz.
> **Solution:** x(t) = cos(100πt) = cos(2π·50·t), so f = 50 Hz. With f_s = 200 Hz, f_s/2 = 100 Hz > 50 Hz, so every spectral component lies below Nyquist and the samples determine the signal uniquely; the reconstructed frequency is 50 Hz. The aliasing relation |f_s − f| applies only to components above f_s/2, and a 200 Hz sample rate would fail for any component above 100 Hz.
> **Key point:** No aliasing when f < f_s/2: here 50 Hz < 100 Hz, so the tone reconstructs exactly.

### Q228. Two orthogonal functions on [0, L] are used to expand a signal. State the Parseval-style energy statement and its engineering meaning.

> **Type:** Theory
> **Answer:** The sum of the squares of the expansion coefficients equals the signal's energy (with the normalisation of the basis), and the cross terms vanish: the basis is orthogonal, so the signal's energy is the sum of the energies in each mode, with no interference between modes.
> **Solution:** For an orthonormal basis φₙ, ∫|f|² = Σ|cₙ|²; for the unnormalised cos/sin basis on (−L, L) this becomes Parseval's identity. The engineering meaning is that a modal expansion is lossless: a signal decomposed into orthogonal modes carries its energy in those modes independently, and reconstructing from any subset of the modes gives exactly the energy of that subset. This is the mathematical reason a filter bank in a non-redundant orthogonal transform conserves energy.
> **Key point:** Orthogonal expansion ⟹ energy = sum of modal energies; no cross terms survive.

### Q229. A force field has a potential φ and a vortex field has circulation around a loop. Use Stokes's theorem to compare.

> **Type:** Conceptual
> **Answer:** A conservative field has zero circulation around every closed loop, while a field with nonzero circulation has a curl that is not identically zero somewhere inside, since ∮C **F**·d**r** = ∫∫S(∇ × **F**)·d**S** over any surface S spanning C.
> **Solution:** Stokes's theorem equates a line integral to a surface integral of the curl, so a nonzero circulation proves the flux of the curl through every spanning surface is the same nonzero number, i.e. the curl is nonzero somewhere. A potential function forces that flux to vanish for every C. This is the sharp contrast with the sufficiency result (curl-free on a simply connected domain ⟹ conservative); the reverse implication fails.
> **Key point:** Nonzero circulation ⟹ nonzero curl flux through every spanning surface; a potential field gives zero.

---

## Section 16. Traps, sign errors, and common mistakes

### Q230. [GATE-1] Trap: a field **F** = (y, −x, 0) is claimed to be conservative because its curl looks "small". Test the claim.

> **Type:** MCQ
> **Answer:** The claim is false: the curl is (0, 0, −2) ≠ 0, and the circulation around the unit circle counterclockwise is −2π ≠ 0 (Option b).
> **Solution:** Computing the curl, (∇ × **F**)ₓ = ∂0/∂y − ∂(−x)/∂z = 0, the y-component is 0, and (∇ × **F**)_z = ∂(−x)/∂x − ∂(y)/∂y = −1 − 1 = −2. A nonzero curl means the field is not conservative, and the direct circulation confirms it: with x = cos t, y = sin t on 0 ≤ t ≤ 2π, y dx − x dy = −sin t sin t dt − cos t cos t dt = −dt, so the integral is −2π. The trap is trusting "looks simple" instead of computing the cross-derivatives, which is precisely where sign errors live.
> **Key point:** A "small-looking" curl can still be nonzero: (y, −x, 0) has curl (0, 0, −2) and circulation −2π.

### Q231. [GATE-2] Trap: applying the divergence theorem to a field that is singular inside the volume.

> **Type:** MCQ
> **Answer:** The result is invalid, because the theorem requires the field to be continuously differentiable throughout the enclosed region, and the singularity breaks its hypotheses (Option c).
> **Solution:** Examples are (1/x, 1/y, 1/z) in the unit ball, and (−y/ρ², x/ρ², 0) in a ball containing the z-axis, where the fields are not even defined on the singular set. The correct procedures are either to excise a small tube around the singularity and account for its extra boundary surface, or to conclude the field has infinite flux. Ignoring the singularity is a favourite source of answers that are off by exactly the flux through the excised region.
> **Key point:** A divergence-theorem calculation is invalid if the field is singular anywhere inside the surface.

### Q232. [GATE-1] Trap: the direction of circulation in Stokes's theorem is taken from the drawing rather than from the right-hand rule.

> **Type:** MCQ
> **Answer:** Reversing the surface normal reverses the circulation, so a wrong choice of normal gives the negated answer (Option b).
> **Solution:** Stokes's theorem is ∮∂S**F**·d**r** = ∫∫S(∇ × **F**)·**n̂** dS, and the boundary direction is fixed by the right-hand rule with respect to the chosen normal. Reversing **n̂** negates the right side and, correspondingly, the left side's traversal direction must reverse too. This is why orientation must be stated and used consistently — the same discipline that fixes the sign in Green's theorem, where the counterclockwise convention corresponds to the +**k̂** normal.
> **Key point:** Stokes's boundary direction follows the right-hand rule about the normal; flip the normal and the circulation flips sign.

### Q233. [GATE-2] Trap: assuming a Fourier series converges pointwise everywhere for a merely integrable function.

> **Type:** MCQ
> **Answer:** The claim is false: convergence is guaranteed only at continuity points (to f itself) and at jumps (to the midpoint value), and in general it fails at other points and fails uniformly on any set where f is discontinuous (Option a).
> **Solution:** Dirichlet's theorem requires f to be piecewise continuous and piecewise smooth, and then the partial sums converge pointwise to f at continuity points and to (f⁻ + f⁺)/2 at jumps. For a merely integrable f with unbounded variation, convergence can fail at a dense set. And uniform convergence never happens on an interval containing a jump, because the Gibbs overshoot persists at a fixed 9% — which is exactly why the series is still a correct representation in the L² and pointwise senses while being useless for uniformly approximating a discontinuous function.
> **Key point:** Pointwise convergence is guaranteed only at continuity points and jumps; uniform convergence fails wherever a jump exists.

### Q234. [GATE-1] Trap: dropping the a₀/2 and confusing the definition of a₀ with the DC level of the series.

> **Type:** MCQ
> **Answer:** The series' constant term is a₀/2, which equals the mean value of f; treating a₀ as the DC level doubles it (Option c).
> **Solution:** With a₀ = (1/L)∫₋Lᴸ f dx, the series reads a₀/2 + Σ, so the DC level is a₀/2 = (1/2L)∫f, the mean. For f = 3 the coefficients give a₀ = 6 and the series term 3 ✓, as required. This normalisation matters in signal processing, where the DC power is a₀²/4 in Parseval's form (a₀²/2 in the unsplit version), so dropping or doubling the factor changes the computed energy.
> **Key point:** DC level = a₀/2 = mean of f; a₀ itself is twice the DC level.

### Q235. [GATE-1] Trap: assuming even f implies even harmonics.

> **Type:** MCQ
> **Answer:** False: evenness implies only cosine terms survive (sines vanish), while the *parity of n* is controlled by half-wave symmetry, a different condition (Option b).
> **Solution:** f(−x) = f(x) forces bₙ = 0, and the cosine basis functions cos(nπx/L) all have even parity, so nothing restricts n. What kills odd n is the half-wave condition f(x + L) = −f(x), which multiplies every even-n coefficient by +1 and every odd-n coefficient by −1, so the even-n coefficients must vanish. The two symmetries are independent: a function can be even and still contain only odd harmonics, as |x| does.
> **Key point:** Even f ⟹ cosines only; half-wave antisymmetry ⟹ even n vanish. They are separate tests.

### Q236. [GATE-2] Trap: treating a zero curl as automatically implying a zero circulation, without checking whether the domain is simply connected.

> **Type:** MCQ
> **Answer:** False on a non-simply-connected domain: the field (−y/ρ², x/ρ², 0) has zero curl away from the z-axis yet has circulation 2π around a loop encircling the axis (Option c).
> **Solution:** Computing the curl, all components are zero wherever ρ ≠ 0, but the circulation around a circle of radius a in the z = 0 plane is ∫(−y dx + x dy)/(x² + y²) = 2π ≠ 0, so no single-valued potential exists on the punctured region. The obstruction is the hole: on all of R³, or any simply connected domain, curl-free does imply conservative. The trap is dropping the topology check and quoting the sufficiency theorem in a setting where its hypothesis fails.
> **Key point:** Curl-free ⟹ conservative only on a simply connected domain; holes admit curl-free fields with nonzero circulation.

### Q237. [GATE-1] Trap: forgetting that a discontinuity in the periodic extension appears at ±L even when f is continuous on the open interval.

> **Type:** MCQ
> **Answer:** The mismatch f(L⁻) ≠ f(L⁺) at the endpoints must be treated as a jump, so the series value at ±L is the average of those limits rather than f(L) (Option d).
> **Solution:** A function continuous on (−L, L) may still fail to match its periodic continuation: f(x) = x on (−π, π) has f(π⁻) = π and f(π⁺) = −π, so the periodic extension jumps and the series value at π is 0, not π. This is the standard reason the sawtooth series evaluates to 0 at the endpoints. Missing this is one of the most common slips in GATE problems involving endpoint values.
> **Key point:** A jump at ±L is present whenever f(L⁻) ≠ f(L⁺), even if f is smooth on the open interval.

### Q238. [GATE-2] Trap: using the three-dimensional form of a two-dimensional theorem on a surface in space.

> **Type:** MCQ
> **Answer:** Invalid, because Green's theorem applies only to planar regions; in space the correct tool is Stokes's theorem with the curl vector dotted into the surface normal (Option a).
> **Solution:** Green's theorem is a special case of Stokes's theorem in which the surface lies in a plane and the normal is a constant, so the curl collapses to the single scalar Q_x − P_y. On a curved or tilted surface the curl has three components and the normal varies, so the surface integral must be taken in full. A common mistake is to write a planar expression for a sphere or an inclined plane, which is only defensible after an explicit change of variables.
> **Key point:** Green's theorem is planar; in space use ∫∫S(∇ × **F**)·d**S** with the actual normal.

### Q239. [GATE-1] Trap: adding a term-by-term derivative and integrating it back without checking the constant.

> **Type:** MCQ
> **Answer:** The integration constant must be fixed by evaluating the original series at a point where its value is known; dropping it shifts the entire result by a constant (Option a).
> **Solution:** Integrating a Fourier series term by term produces the n ≠ 0 terms plus an arbitrary constant C, because the constant of integration is independent of n. Fixing it requires a point value: for the sawtooth x = 2Σ(−1)^{n+1} sin(nx)/n, integrating from 0 to x gives x²/2 = −2Σ(−1)^{n+1}cos(nx)/n² + C, and evaluating at x = 0 fixes C = 2Σ(−1)^{n+1}/n² = π²/6. The resulting identity is x² = π²/3 + 4Σ(−1)ⁿ cos(nx)/n², whose constant term π²/3 is the mean of x², a check that any error would expose.
> **Key point:** Integrating a Fourier series leaves an unknown constant; fix it by evaluating the original series at a known point, and the result's DC term must equal the function's mean.

### Q240. [GATE-2] Trap: counting only the positive-frequency half of a real signal's spectrum when applying Parseval.

> **Type:** MCQ
> **Answer:** Invalid: the negative half carries the same energy as the positive half for a real signal, so Parseval must include both, or equivalently use a factor of two on the one-sided sum (Option c).
> **Solution:** For a real f, |c₋ₙ| = |cₙ|, so ∫|f|² = Σ over all n equals 2Σ over n > 0, and Parseval's real form already reflects this in the aₙ² + bₙ² structure with the a₀²/2 special case. Omitting one half halves the computed energy, and forgetting the a₀²/2 rather than a₀² quarter creates a different, subtler error for the DC term.
> **Key point:** Real signals have equal energy in ±ω; doubling the one-sided sum restores the total.

---

## Quick revision — Vector Calculus, Fourier Series & GATE Drills

- **Triple product:** **A**×(**B**×**C**) = **B**(**A**·**C**) − **C**(**A**·**B**), and (**A**×**B**)×**C** = **B**(**A**·**C**) − **A**(**B**·**C**); |**A**×**B**|² = |**A**|²|**B**|² − (**A**·**B**)².
- **Gradient:** ∇f = (f_x, f_y, f_z) is normal to every level surface of f; |∇f| is the maximum directional derivative, and D**û**f = ∇f·**û**.
- **Divergence:** ∇·**F** = F_x,x + F_y,y + F_z,z — each component by its own coordinate; a constant field has zero divergence, hence zero flux through every closed surface.
- **Curl:** (∇×**F**)ₓ = F_z,y − F_y,z, (∇×**F**)_y = F_x,z − F_z,x, (∇×**F**)_z = F_y,x − F_x,y; a field whose components each depend on one coordinate has zero curl.
- **Curl of a gradient is always zero**, and the componentwise vector Laplacian is not ∇×(∇×**A**): they differ by ∇(∇·**A**).
- **Line integral:** ∫**F**·d**r** = ∫Fx dx + Fy dy + Fz dz is work in joules for a force field; a parametrised curve gives ∫**F**(**r**(t))·**r**′(t)dt, and orientation is the whole sign.
- **Conservative fields:** ∮∇f·d**r** = 0 on every closed loop, and on a simply connected domain curl-free ⟹ conservative; a hole admits curl-free fields with circulation 2π, e.g. (−y/ρ², x/ρ², 0).
- **Flux is a signed integral** ∫∫**F**·**n̂**dS; the "magnitude × area" shortcut needs a constant, uniformly oriented integrand, and the divergence theorem needs the field to be C¹ throughout the enclosed region.
- **Green's theorem (planar only):** ∮(P dx + Q dy) = ∬(Q_x − P_y)dA for circulation and ∮(P dy − Q dx) = ∬(P_y − Q_x)dA for flux; swapping the integrands flips the sign, and the counterclockwise convention pairs with +**k̂**.
- **Stokes's theorem:** ∮∂S**F**·d**r** = ∫∫S(∇×**F**)·d**S**, with the boundary direction fixed by the right-hand rule; nonzero circulation proves nonzero curl flux through every spanning surface, and the circulation is surface independent.
- **Curvilinear weights:** cylindrical ∇·**A** = (1/ρ)(ρA_ρ)_ρ + (1/ρ)A_φ,φ + A_z,z; spherical ∇·**A** = (1/r²)(r²A_r)_r + (1/(r sin θ))(sin θ A_θ)_θ + (1/(r sin θ))A_φ,φ; scale factors h = (1, ρ, 1) and (1, r, r sin θ).
- **Purely radial field:** only the radial term survives, and for A_r = rⁿ, div = (n+2)r^{n−1}, so ∇²r⁴ = 20r²; in the divergence the azimuthal/θ terms differentiate by their own angle, while their radial derivatives belong to the curl.
- **Fourier coefficients:** aₙ = (1/L)∫₋Lᴸf cos(nπx/L)dx, bₙ = (1/L)∫₋Lᴸf sin(nπx/L)dx, and DC = a₀/2 = mean of f — a₀ itself is twice the DC level, the commonest normalisation slip.
- **Interval fixes the spectrum:** on (−L, L) the harmonics are nπ/L, and cₙ = (1/2L)∫f e^{−inπx/L}dx with c₋ₙ = cₙ* and c₀ = a₀/2.
- **Symmetry tests:** even f ⟹ cosine terms only, odd f ⟹ sine terms only, and half-wave antisymmetry f(x + L) = −f(x) ⟹ all even-n coefficients vanish — parity of n and parity of f are separate tests.
- **Decay reports smoothness:** jump ⟹ 1/n, kink ⟹ 1/n², generally 1/n^{k+1} where k derivatives match periodically; differentiating a series requires coefficients O(1/n²) and gives f′ at smooth points but the average slope at a corner, while integrating always works and leaves a constant fixed by evaluating the original series at a known point.
- **Convergence rule:** the series gives f at continuity points and (f⁻ + f⁺)/2 at a jump, including at ±L when the periodic extension mismatches; a point value never matters, and uniform convergence fails wherever a jump exists.
- **Gibbs:** the overshoot is ≈9% of the jump at every N; only the ringing's width shrinks as 1/N.
- **Parseval:** (1/L)∫₋Lᴸ|f|²dx = a₀²/2 + Σ(aₙ² + bₙ²) — the coefficients hold the function's energy, and a real signal has equal energy at ±ω.
- **Standing sums:** Σ1/n² = π²/6, Σ_{n odd}1/n² = π²/8, Σ(−1)^{n+1}/n² = π²/12, 1 − 1/3 + 1/5 − 1/7 + ⋯ = π/4.
- **Series to know:** x = 2Σ(−1)^{n+1}sin(nx)/n (0 at ±π), |x| = π/2 − (4/π)Σ_{n odd}cos(nx)/n², and x² = π²/3 + 4Σ(−1)ⁿcos(nx)/n², whose constant is the mean of x².
- **Half-range expansions:** the cosine series of x on (0, L) has aₙ = 2L((−1)ⁿ − 1)/(n²π²), nonzero only for odd n; the two extensions (odd/even) are different functions off the interval.
- **Series operations:** shifting rotates the (aₙ, bₙ) pair by cπ/L, scaling x → kx keeps every nk-th coefficient, and the coefficients of a product are the convolution of the two sequences.
- **Fourier integral:** f(x) = ∫₀^∞[A(ω)cos ωx + B(ω)sin ωx]dω with A, B the (1/π)-weighted integrals over (−∞, ∞); 2L → ∞ turns the series into the integral, and a jump still gives (f⁺ + f⁻)/2.
- **Standard integral results:** F{e^{−x²}} = √π e^{−ω²/4} with ∫₀^∞ e^{−ω²/4}dω = √π ≈ 1.772; F{1/(1+x²)} = πe^{−|ω|} so ∫₀^∞ cos(ωx)/(1+x²)dx = (π/2)e^{−|ω|}; ∫₀^∞ (sin ax)/x dx = π/2 and ∫₀^∞(1 − cos ax)/x² dx = πa/2.
- **Signal properties:** a band-limited LTI system cannot create frequencies outside the input band; no aliasing when f < f_s/2; a finite spectrum is exactly reconstructible from finitely many samples.
- **Transform calculus:** f(t − t₀) ↔ e^{−jωt₀}X(ω), f(t)e^{jω₀t} ↔ X(ω − ω₀), f′(t) ↔ jωF(ω) plus a jump-delta, and a real signal satisfies X(−ω) = X*(ω).
- **RC low-pass:** h(t) = (1/RC)e^{−t/RC}u(t) ↔ 1/(1 + jωRC), so |H| = 1/√(1 + (ωRC)²) and phase = −tan⁻¹(ωRC).
- **Synthesis with Fourier:** the heat equation decays mode n as e^{−n²t} and relaxes to the mean of the initial data (π²/3 for f = x²); a fixed-ended string has ωₙ = cnπ/L with n ≥ 1, no zero mode, and pluck amplitudes given by the half-range sine coefficients.
- **Synthesis with vectors:** a uniformly charged slab gives E = σ/(2εε₀) inside and σ/εε₀ when metallised; in 2D, v_ρ = (1/ρ)ψ_θ and v_θ = −ψ_ρ, so ψ = 2x is the uniform flow **v** = (0, −2).
- **Units sanity:** flux of E in V/m through m² is volts; work ∫**F**·d**r** with F in N is joules; and Fourier coefficients carry the units of f, since the 1/L factor cancels the integration length.
