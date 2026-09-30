# Engineering Mathematics — Part 3: Complex Analysis

> Part 3 of 5 in the Engineering Mathematics question bank · Questions 1–227 of this file
> Read this file top to bottom, in order. The surrounding files cover real calculus and
> series, linear algebra, probability, vector calculus/Fourier and PDE/variational methods;
> this one is confined to complex analysis.

**Covers:** complex algebra (modulus, argument, De Moivre, roots of unity, the argument
principle); the Argand plane and linear-fractional maps; the elementary analytic functions
of a complex variable; Gamma and error functions; Taylor and Laurent series and analytic
continuation; Cauchy–Riemann equations and harmonic functions; contour integration, Cauchy's
theorem and formula; uniform convergence and Weierstrass M-test; singularities and residues;
and applications — real definite integrals by residues, inverse Z-transform and Fourier-type
integrals by contours.

**Assumes:** real calculus (definite integrals, differentiation under the integral sign),
basic complex arithmetic, geometric-series summation, and the notion of a limit and a
continuously differentiable partial derivative.

**Volume and difficulty mix:** 227 questions — ~15% definition/fact recall, ~20% formula
application and quick numerical, ~25% medium 2–4 mark problems, ~20% GATE 1-mark MCQ with
misconception-encoded distractors, ~20% GATE 2-mark MCQ / NAT / MSQ. Questions tagged
`GATE-1` or `GATE-2` are exam-format items best attempted without writing a full solution.

## Section 1. Complex numbers, modulus, argument and roots

### Q1. Compute the modulus of `z = 3 − 4i` and the modulus of `z²`.

> **Type:** Numerical
> **Answer:** `|z| = 5` and `|z²| = 25`.
> **Solution:** For `z = x + iy`, the modulus is `|z| = √(x² + y²)`, so `|3 − 4i| = √(9 + 16) = 5`. Squaring first, `z² = (3 − 4i)² = 9 − 24i + 16i² = 9 − 24i − 16 = −7 − 24i`. Then `|z²| = √(49 + 576) = √625 = 25`, which also follows from the identity `|z²| = |z|·|z| = 25`.
> **Key point:** `|zⁿ| = |z|ⁿ` always holds, so moduli can be raised to the power n without expanding.

### Q2. Find all arguments of `z = −1 − i`, and state the principal argument.

> **Type:** Numerical
> **Answer:** All arguments are `−3π/4 + 2kπ` (equivalently `225° + 360k°`); the principal argument is `−3π/4 ≈ −2.356 rad`.
> **Solution:** `−1 − i` lies in the third quadrant with equal coordinates, so its reference angle is `arctan(1/1) = 45°`; the quadrant-III angle from the positive real axis is `180° + 45° = 225°`. On the branch `−π < Arg z ≤ π` this is the same angle written as `225° − 360° = −135° = −3π/4`. Since the argument is defined only modulo `2π`, the full set is `−3π/4 + 2kπ`, `k` any integer.
> **Key point:** Arguments are a set `{θ + 2kπ}`; the principal argument `Arg` is the single member in `(−π, π]`.

### Q3. Write `z = 1 − i√3` in polar form and in exponential form.

> **Type:** Numerical
> **Answer:** `z = 2(cos(−π/3) + i sin(−π/3)) = 2e^(−iπ/3)`, with `|z| = 2` and `Arg z = −π/3 = −60°`.
> **Solution:** The modulus is `√(1 + 3) = 2`. The point `(1, −√3)` lies in the fourth quadrant with reference angle `arctan(√3/1) = 60°`, so the argument is `−60°`. Polar form `r(cos θ + i sin θ)` therefore reads `2(cos(−60°) + i sin(−60°)) = 2(0.5 − i·0.866) = 1 − 1.732i`, which is the given number. The exponential form uses `e^{iθ} = cos θ + i sin θ`, giving `2e^(−iπ/3)`.
> **Key point:** Exponential form `r e^{iθ}` is the working form for almost all complex-algebra and contour work.

### Q4. State De Moivre's theorem and use it to evaluate `(cos(2π/7) + i sin(2π/7))⁷`.

> **Type:** Recall
> **Answer:** `(cos θ + i sin θ)ⁿ = cos nθ + i sin nθ`; the value asked for is `1`.
> **Solution:** De Moivre's theorem says that for every integer `n`, `(cos θ + i sin θ)ⁿ = cos nθ + i sin nθ` — the angle is simply multiplied. Substituting `θ = 2π/7` and `n = 7` gives `cos(2π) + i sin(2π) = 1 + i·0 = 1`. This is the reason the 7th roots of unity are `e^{2πik/7}`, `k = 0, 1, 2, 3, 4, 5, 6`.
> **Key point:** De Moivre converts `(cis θ)^n` into `cis nθ`, which is the cleanest route to all n-th roots.

### Q5. Evaluate `(1 + i)⁸` using polar form.

> **Type:** Numerical
> **Answer:** `16`.
> **Solution:** Write `1 + i = √2(cos(π/4) + i sin(π/4)) = √2 e^{iπ/4}`. Then `(1+i)⁸ = (√2)⁸ e^{8iπ/4} = 2⁴ e^{2iπ} = 16·(cos 2π + i sin 2π) = 16`. The modulus is `(√2)⁸ = 16` and the argument `8·(π/4) = 2π ≡ 0`, so the result is a positive real number.
> **Key point:** Moduli multiply, arguments add; a total argument of a whole multiple of `2π` leaves a real positive result.

### Q6. Evaluate `(1 − i√3)³` and verify your answer by direct cubing.

> **Type:** Numerical
> **Answer:** `−8`.
> **Solution:** From Q3's form, `1 − i√3 = 2e^{−iπ/3}`, so `(1 − i√3)³ = 8 e^{−iπ} = 8(cos(−π) + i sin(−π)) = −8`. Direct check: `(1 − i√3)² = 1 − 2i√3 − 3 = −2 − 2i√3`; multiplying by `1 − i√3` gives `(−2 − 2i√3)(1 − i√3) = −2 + 2i√3 − 2i√3 + 2i²·3 = −2 − 6 = −8`. Both routes agree.
> **Key point:** `(r e^{iθ})³ = r³ e^{3iθ}`; always check one of these by direct expansion when in doubt.

### Q7. Find both square roots of `−4` and identify the principal square root.

> **Type:** Numerical
> **Answer:** `2i` and `−2i`; the principal square root (argument in `(−π, π]`, i.e. the root in the right half plane) is `2i`.
> **Solution:** In polar form `−4 = 4e^{iπ}`, so the two square roots are `2e^{iπ/2} = 2i` and `2e^{i(π/2 + π)} = 2e^{i3π/2} = −2i`. Check: `(2i)² = −4` and `(−2i)² = −4`. The principal root is the one whose argument lies in `(−π/2, π/2]`, which is `2i`. Note this is *not* the real number `−2` (a common trap, since `|−4| = 4`).
> **Key point:** The square root of a negative real number is purely imaginary; the principal root is the one with non-negative real part.

### Q8. Find the three cube roots of `8` explicitly in rectangular form.

> **Type:** Numerical
> **Answer:** `2`, `−1 + i√3`, `−1 − i√3`.
> **Solution:** `8 = 8e^{i0}`, so the cube roots are `2e^{i(0 + 2πk/3)}` for `k = 0, 1, 2`. For `k = 0`: `2`. For `k = 1`: `2(cos 120° + i sin 120°) = 2(−0.5 + 0.866i) = −1 + i√3`. For `k = 2`: `2(cos 240° + i sin 240°) = −1 − i√3`. They are equally spaced by `120°` on the circle `|z| = 2`, and indeed `(−1 + i√3)³ = 8`.
> **Key point:** The n-th roots of a complex number form a regular n-gon: same modulus, arguments spaced by `2π/n`.

### Q9. Show that the sum of all n-th roots of unity is zero, for every integer `n > 1`.

> **Type:** Theory
> **Answer:** `Σ_{k=0}^{n−1} ω^k = 0`, where `ω = e^(2πi/n)`.
> **Solution:** The geometric-series formula gives `(1 − ωⁿ)/(1 − ω) = 0` provided `ω ≠ 1`, which holds for `n > 1` since `ω^n = 1` and `ω = e^{2πi/n} ≠ 1`. Here `1 − ωⁿ = 1 − 1 = 0`. So the sum vanishes, i.e. the roots form a polygon whose centre of mass is the origin. This is why the real and imaginary parts of each root can be paired off and shown to cancel.
> **Key point:** `Σ_{k=0}^{n−1} ω^k = 0` for every `n > 1` — the quickest proof of cancellations involving roots of unity.

### Q10. Find all sixth roots of unity and identify the primitive sixth roots of unity.

> **Type:** Numerical
> **Answer:** Roots: `e^{iπk/3}` for `k = 0, 1, 2, 3, 4, 5`, i.e. `1, (1/2 + i√3/2), (−1/2 + i√3/2), −1, (−1/2 − i√3/2), (1/2 − i√3/2)`. Primitive sixth roots: `e^{iπ/3}` and `e^{−iπ/3}` only.
> **Solution:** `z⁶ = 1` has solutions `z = e^{2πik/6} = e^{iπk/3}`. Converting with `cos k60° + i sin k60°` gives the six listed points. A root is *primitive of order 6* if no smaller positive power equals 1, i.e. `6/gcd(k, 6) = 6`, requiring `k = 1` or `k = 5`. For `k = 2, 4` the order is 3, and for `k = 3` the order is 2.
> **Key point:** The order of `e^{2πik/n}` is `n/gcd(k, n)`; primitive roots are those with `gcd(k, n) = 1`.

### Q11. If `ω = e^{2πi/5}`, use `1 + ω + ω² + ω³ + ω⁴ = 0` to show that `ω` satisfies `ω⁴ + ω³ + ω² + ω + 1 = 0`, and confirm the roots of that equation are the fifth roots of unity.

> **Type:** Theory
> **Answer:** `ω⁴ + ω³ + ω² + ω + 1 = 0`; the five roots of `x⁴ + x³ + x² + x + 1 = 0` are exactly the fifth roots of unity, each with multiplicity 1.
> **Solution:** Since `ω⁵ = 1` and `ω ≠ 1`, the geometric sum collapses to zero as in Q9. Also `(x⁵ − 1) = (x − 1)(x⁴ + x³ + x² + x + 1)`, so the quartic's roots are exactly the fifth roots of unity with `x = 1` removed. All five are simple because `d/dx(x⁵ − 1) = 5x⁴ ≠ 0` at any root. This cyclotomic polynomial is the standard tool for DFT eigenvalue problems.
> **Key point:** `x^n − 1 = (x − 1)Σ_{k=0}^{n−1}x^k`; the degree-`(n−1)` factor has the non-trivial n-th roots of unity as its simple roots.

### Q12. `GATE-1` The principal argument of the complex number `z = 1 − i` lies in which interval, and what is its value in degrees?

> **Type:** MCQ
> **Answer:** `(−90°, 0°)`, i.e. `−45°` (Option a).
>
> (a) `(−90°, 0°)`, value `−45°`
> (b) `(0°, 90°)`, value `45°`
> (c) `(270°, 360°)`, value `315°`
> (d) `(180°, 270°)`, value `225°`
>
> **Solution:** `1 − i` has positive real part and negative imaginary part, so it lies in the fourth quadrant: `(−90°, 0°)`. Its reference angle is `arctan(1/1) = 45°`, so the principal argument is `−45°`. Option (c) is the trap: `315°` *is* a legitimate argument, since `315° = −45° + 360°`, but it is not the principal one, which by convention lies in `(−180°, 180°]`.
> **Key point:** Many arguments exist, but `Arg` is the single one in `(−180°, 180°]`; rejecting `315°` is the whole point of the question.

### Q13. Verify the relation `z̄ = |z|²/z` numerically for `z = 2 − 3i`.

> **Type:** Numerical
> **Answer:** `|z|² = 13` and `13/(2 − 3i) = 2 + 3i = z̄`.
> **Solution:** The conjugate of `z = 2 − 3i` is `z̄ = 2 + 3i`. Also `|z|² = (2 − 3i)(2 + 3i) = 4 + 9 = 13`. Then `|z|²/z = 13/(2 − 3i) = 13(2 + 3i)/((2−3i)(2+3i)) = 13(2 + 3i)/13 = 2 + 3i`. The identity is really just `z z̄ = |z|²` divided by `z`, and it is the algebraic step in every rationalisation of `1/z`.
> **Key point:** `z z̄ = |z|²`, so `1/z = z̄/|z|²` and `z̄ = |z|²/z`.

### Q14. Prove the triangle inequality `|z₁ + z₂| ≤ |z₁| + |z₂|`, and state the exact condition for equality.

> **Type:** Theory
> **Answer:** `|z₁ + z₂| ≤ |z₁| + |z₂|`, with equality if and only if `z₂ = t z₁` for some **non-negative real** `t` (equivalently, `z₁/z₂ ≥ 0` when `z₂ ≠ 0`).
> **Solution:** `|z₁ + z₂| = |z₁||1 + z₂/z₁| ≤ |z₁|(1 + |z₂/z₁|) = |z₁| + |z₂|`, using `|1 + w| ≤ 1 + |w|`. Equality in `|1 + w| ≤ 1 + |w|` holds exactly when `w` is a non-negative real number, so equality in the triangle inequality requires `z₂/z₁` non-negative real. Example: `|3 + 4i| = 5 = 3 + 4`, equality because `3 ≥ 0`.
> **Key point:** Equality in the triangle inequality requires the two numbers to be parallel **and same-signed** — a negative real ratio gives strict inequality.

### Q15. `GATE-1` If `|z₁| = 2` and `|z₂| = 3`, what is the range of possible values of `|z₁ − z₂|`?

> **Type:** MCQ
> **Answer:** `1 ≤ |z₁ − z₂| ≤ 5`, i.e. `[1, 5]` (Option a).
>
> (a) `[1, 5]`
> (b) `[0, 5]`
> (c) `[2, 3]`
> (d) `[1, 6]`
>
> **Solution:** Applying the reverse triangle inequality, `||z₁| − |z₂|| ≤ |z₁ − z₂| ≤ |z₁| + |z₂|`, giving `|3 − 2| = 1 ≤ |z₁ − z₂| ≤ 5`. Both extremes are attained: `z₁ = 2`, `z₂ = 3` gives `|z₁ − z₂| = 1` (same direction), and `z₁ = 2`, `z₂ = −3` gives `5` (opposite directions). Every intermediate value occurs by rotating one vector continuously, so the range is the full closed interval. Option (c) is the trap of assuming the two must be orthogonal.
> **Key point:** `||z₁| − |z₂|| ≤ |z₁ − z₂| ≤ |z₁| + |z₂|`; the extremes are collinear, same-sense and opposite-sense.

### Q16. Compute `(1 + i)(2 − 2i)` and use it to check the product-modulus identity.

> **Type:** Numerical
> **Answer:** `4`; also `|z₁z₂| = √2 · 2√2 = 4 = |z₁||z₂|`.
> **Solution:** Expanding, `(1 + i)(2 − 2i) = 2 − 2i + 2i − 2i² = 2 + 2 = 4`. The identity `|z₁z₂| = |z₁||z₂|` gives `|1 + i| = √2`, `|2 − 2i| = 2√2`, product `√2·2√2 = 4`, matching `|4| = 4`. Arguments also add: `π/4 + (−π/4) = 0`, so the product must be positive real — a useful consistency check.
> **Key point:** `z₁z₂ = |z₁||z₂| e^{i(θ₁+θ₂)}`; equal-and-opposite arguments cancel into a positive real.

### Q17. Compute `1/(3 + 4i)` in rectangular form and verify the result by multiplication.

> **Type:** Numerical
> **Answer:** `0.12 − 0.16i`.
> **Solution:** Multiply numerator and denominator by the conjugate `3 − 4i`: `1/(3 + 4i) = (3 − 4i)/((3 + 4i)(3 − 4i)) = (3 − 4i)/25 = 0.12 − 0.16i`. Verification: `(3 + 4i)(0.12 − 0.16i) = 0.36 − 0.48i + 0.48i − 0.64i² = 0.36 + 0.64 = 1`. In polar form the answer is `1/5 e^{−i arctan(4/3)}`, consistent with `1/z` halving nothing but negating the argument.
> **Key point:** `1/z = z̄/|z|²` — negate the argument, invert the modulus.

### Q18. Evaluate `(1 + i)¹⁰` in rectangular form.

> **Type:** Numerical
> **Answer:** `32i`.
> **Solution:** `1 + i = √2 e^{iπ/4}`, so `(1+i)¹⁰ = (√2)¹⁰ e^{10iπ/4} = 2⁵ e^{5iπ/2} = 32(cos(5π/2) + i sin(5π/2))`. Since `5π/2 = 2π + π/2`, we have `cos = 0`, `sin = 1`, giving `32i`. Equivalently, from Q5, `(1+i)⁸ = 16` and `(1+i)² = 2i`, so `(1+i)¹⁰ = 32i`.
> **Key point:** Reduce the accumulated angle modulo `2π` before converting back to rectangular form.

### Q19. State the argument principle, including what is counted and what the output represents.

> **Type:** Theory
> **Answer:** If `f` is analytic inside and on a simple closed contour `C` with no zeros or poles on `C`, then `(1/2πi)∮_C f′(z)/f(z) dz = Z − P`, where `Z` is the number of zeros of `f` inside `C` (multiplicities counted) and `P` the number of poles inside `C`.
> **Solution:** The integrand `f′(z)/f(z)` is the logarithmic derivative of `f`; near a zero of order `m` at `z_k` it behaves like `m/(z − z_k)`, and near a pole of order `m` like `−m/(z − z_k)`. Each zero therefore contributes `+1` to `(1/2πi)∮` and each pole `−1`, by the residue theorem. The result is an integer, which is the characteristic signature of the argument principle.
> **Key point:** `∮ f′/f = 2πi(Z − P)`; it counts zeros minus poles, and the value is always a real integer.

### Q20. Along the closed curve `w(t) = e^{2it}`, `0 ≤ t ≤ 2π`, what is the total change in the argument of `w`?

> **Type:** Numerical
> **Answer:** `4π` (two complete turns, winding number 2).
> **Solution:** The argument of `w(t)` is `2t` (mod `2π`). As `t` goes from 0 to `2π`, the continuously tracked argument runs from 0 to `4π`, a total change of `4π`. The curve `|w| = 1` is traversed twice, counterclockwise, so the winding number about the origin is 2. By the general form of the argument principle, `(1/2πi)∮ f′/f = 2`.
> **Key point:** The *total* (continuous) change of argument equals `2π ×` winding number, not merely the endpoint value `0`.

### Q21. A closed curve `C` is traversed twice counterclockwise about the origin and once clockwise about the point `1`, and encloses no other singular point. What winding number does `C` have about `0`, and what does this imply for `(1/2πi)∮_C dz/z`?

> **Type:** Numerical
> **Answer:** Winding number about `0` is 2, so `(1/2πi)∮_C dz/z = 2` and `∮_C dz/z = 4πi`.
> **Solution:** The winding number counts signed encirclements: two counterclockwise passes give `+1 + 1 = 2` (the clockwise pass about `1` is irrelevant since `1` is not where the pole of `dz/z` sits). The general residue-type statement is `∮_C g(z)dz/(z − z₀) = 2πi · n(C, z₀)`, where `n(C, z₀)` is the winding number about `z₀`. Applying it with `g ≡ 1` and `z₀ = 0` gives `∮_C dz/z = 2πi · 2 = 4πi`.
> **Key point:** `∮_C g dz/(z − z₀) = 2πi·n(C, z₀)` — the winding number generalises the simple "inside/outside" dichotomy.

### Q22. `GATE-1` The argument of the complex number `z = 0` is

> **Type:** MCQ
> **Answer:** Undefined, because `arg` is defined as an angle subtended at the origin (Option c).
>
> (a) `0`
> (b) `2π`
> (c) Undefined
> (d) `π/2`
>
> **Solution:** The argument of `z` is an angle `θ` with `z = |z| e^{iθ}`, which requires `|z| > 0`. At `z = 0` the modulus is `0` and no direction from the origin is defined, so `z = 0` subtends no angle at all — there is not even an "infinitely many arguments" situation, as there is for nonzero `z`. Its modulus is perfectly well defined, `|0| = 0`. Option (a) is the trap: people assign argument 0 by analogy with the positive real axis, but the zero vector has no direction.
> **Key point:** `|z|` is defined at `z = 0`; `arg z` is not.

## Section 2. The Argand plane, transformations and linear-fractional maps

### Q23. Plot `z = −2 + 3i` on the Argand plane and state its quadrant, modulus and argument.

> **Type:** Numerical
> **Answer:** Point `(−2, 3)`; second quadrant; `|z| = √13 ≈ 3.606`; `Arg z = π − arctan(3/2) ≈ 2.159 rad ≈ 123.7°`.
> **Solution:** In the Argand plane `z = x + iy` is the point `(x, y)` with real axis `x` and imaginary axis `y`, so `−2 + 3i` sits two units left and three units up. Negative real part and positive imaginary part place it in the second quadrant. The modulus is `√(4 + 9) = √13 ≈ 3.606`. The reference angle from the negative real axis is `arctan(3/2) = 56.31°`, so the counterclockwise argument is `180° − 56.31° = 123.69°`, or `2.159 rad` in the principal branch.
> **Key point:** On the Argand plane the complex modulus is the distance from the origin and the argument is the polar angle measured from the positive real axis.

### Q24. What locus in the `z`-plane does `|z − (1 + 2i)| = 3` describe when `z = x + iy`? Give centre and radius.

> **Type:** Numerical
> **Answer:** A circle with centre `1 + 2i` and radius 3, i.e. `(x − 1)² + (y − 2)² = 9`.
> **Solution:** Writing `z = x + iy` gives `z − (1 + 2i) = (x − 1) + i(y − 2)`, so `|z − (1 + 2i)| = \sqrt{(x - 1)^2 + (y - 2)^2}`. Setting this equal to 3 and squaring gives `(x − 1)² + (y − 2)² = 9`, which is the circle of radius 3 about the point `(1, 2)`. In general `|z − a| = r` with `r > 0` is the circle of centre `a` and radius `r`; `|z − a| < r` is the disc and `|z − a| > r` its exterior, and the strict inequality `r > 0` is needed for the locus to be a genuine circle rather than a single point.
> **Key point:** `|z − a| = r` with `r > 0` is the circle of centre `a` and radius `r`; here the centre is `1 + 2i` and the radius is 3.

### Q25. Show that the locus `|z − (1 + i)| = |z − (4 − 2i)|` is a straight line, and find its equation.

> **Type:** Numerical
> **Answer:** The line `Re(z) − Im(z) = 3`, i.e. `x − y = 3`.
> **Solution:** `A = 1 + i` corresponds to `(1, 1)` and `B = 4 − 2i` to `(4, −2)`. The locus of points equidistant from two distinct points is the perpendicular bisector of the segment `AB`. The midpoint is `((1+4)/2, (1−2)/2) = (5/2, −1/2)`. The slope of `AB` is `(−2 − 1)/(4 − 1) = −3/3 = −1`, so the perpendicular bisector has slope `+1`. Hence `y + 1/2 = 1·(x − 5/2)`, i.e. `y = x − 3`, or `x − y = 3`. Directly: squaring both sides gives `x² + y² − 2x − 2y + 2 = x² + y² − 8x + 4y + 20`, so `6x − 6y − 18 = 0` — the same line.
> **Key point:** `|z − a| = |z − b|` is the perpendicular bisector of the line joining `a` and `b`, a straight line, not a circle.

### Q26. State the general equation of a straight line in complex form, and show that `y = 2` satisfies it.

> **Type:** Theory
> **Answer:** Every line has the form `A z + Ā z̄ + C = 0` with `A ≠ 0` complex and `C` real. The line `y = 2` is `z − z̄ = 4i`.
> **Solution:** With `z = x + iy`, take `A = a + ib` and `C` real: `Az + Āz̄ + C = (a+ib)(x+iy) + (a−ib)(x−iy) + C = 2(ax − by) + C`. So the form is `2ax − 2by + C = 0`, an arbitrary real line provided `(a, b) ≠ (0, 0)`. For `y = 2` we need the coefficient of `x` to vanish and that of `y` to be nonzero, so choose `A = 1`: `z − z̄ = 2iy`; for the line `y = 2` this reads `2iy = 4i`, i.e. `z − z̄ = 4i`. Check with `z = 1 + 2i`: `z̄ = 1 − 2i`, difference `4i` ✓, and with `z = 5 + 2i` likewise `4i` ✓.
> **Key point:** A real line is `A z + Ā z̄ + C = 0`; a circle is `A z Ā + B z + B̄ z̄ + C = 0` with `C > 0`.

### Q27. Show that three complex numbers `z₁, z₂, z₃` (with `z₂ ≠ z₃`) are collinear if and only if `(z₁ − z₂)/(z₁ − z₃)` is real. Test it on `z₁ = 1 + i`, `z₂ = 2`, `z₃ = 3 − 2i`, and then on `z₁ = 1 + i`, `z₂ = 2`, `z₃ = 3 − i`.

> **Type:** Numerical
> **Answer:** First triple: ratio `(5 + i)/13 ≈ 0.385 + 0.0769i`, not real, so **not** collinear. Second triple: ratio `1/2`, real, so **collinear**.
> **Solution:** A quotient of two complex numbers is real exactly when the two vectors `z₁ − z₂` and `z₁ − z₃` are parallel, i.e. when the three corresponding points lie on one straight line. First triple: `z₁ − z₂ = −1 + i` and `z₁ − z₃ = −2 + 3i`, so the ratio is `(−1 + i)/(−2 + 3i) = (−1 + i)(−2 − 3i)/13 = (2 + 3i − 2i − 3i²)/13 = (5 + i)/13 ≈ 0.385 + 0.0769i`, which has a non-zero imaginary part, so the points are not collinear. The slope test agrees: from `(1,1)` to `(2,0)` the slope is `(0−1)/(2−1) = −1`, while from `(1,1)` to `(3,−2)` it is `(−2−1)/(3−1) = −1.5`. Second triple: `z₁ − z₃ = −2 + 2i` and `(−1 + i)/(−2 + 2i) = 1/2`, a real number, so `(1,1)`, `(2,0)`, `(3,−1)` all lie on the line `y = 2 − x`.
> **Key point:** `(z₁ − z₂)/(z₁ − z₃) ∈ ℝ` is the collinearity test; a purely imaginary value signals a right angle at `z₁` instead.


### Q28. Show that `w = 1/z` maps the circle `|z − 2| = 1` onto a circle, and find its centre and radius in the `w`-plane.

> **Type:** Numerical
> **Answer:** The image is the circle `|w − 2/3| = 1/3`, centre `2/3`, radius `1/3`.
> **Solution:** Substitute `z = 1/w` into `|z − 2| = 1`: `|1/w − 2| = 1`, multiply by `|w|`: `|1 − 2w| = |w|`. Squaring, `(1 − 2w)(1 − 2w̄) = w w̄`, i.e. `1 − 2w − 2w̄ + 4|w|² = |w|²`, so `3|w|² − 2(w + w̄) + 1 = 0`. With `w = u + iv`, `w + w̄ = 2u` and `|w|² = u² + v²`, giving `3u² + 3v² − 4u + 1 = 0`, i.e. `u² + v² − (4/3)u + 1/3 = 0`. Completing the square: `(u − 2/3)² + v² = 4/9 − 1/3 = 1/9`. Note `z = 0` is **not** on `|z − 2| = 1`, so the map is finite on the whole circle and the image is a genuine circle (a circle through `z = 0` would instead map to a straight line).
> **Key point:** Under `w = 1/z` a circle through the origin maps to a **line**; a circle not through the origin maps to a circle.

### Q29. Prove that `w = (z − a)/(z − b)` maps the perpendicular bisector of `a` and `b` onto the unit circle `|w| = 1`.

> **Type:** Theory
> **Answer:** `|(z − a)/(z − b)| = 1 ⟺ |z − a| = |z − b|`, which is exactly the perpendicular bisector; the image is `|w| = 1`.
> **Solution:** The modulus of the quotient is the ratio of the moduli: `|w| = |z − a|/|z − b|`. The locus `|w| = 1` therefore satisfies `|z − a| = |z − b|`, i.e. the perpendicular bisector of the segment joining `a` and `b` (Q25). The converse holds too, so the two loci coincide. Numerically, with `a = 0`, `b = 2`, take `z = 1`: `w = 1/(−1) = −1`, `|w| = 1` ✓; take `z = 1 + 2i`: `|z| = √5` and `|z − 2| = |−1 + 2i| = √5`, so `|w| = 1` ✓.
> **Key point:** `w = (z − a)/(z − b)` sends the perpendicular bisector of `a, b` to `|w| = 1`, the `a`-point to 0 and the `b`-point to `∞`.

### Q30. Show that `w = (z − i)/(z + i)` maps the real axis onto the unit circle, and find the image of `z = 2 + 3i`.

> **Type:** Numerical
> **Answer:** For real `z`, `|z − i| = |z + i|`, so `|w| = 1`; and `z = 2 + 3i` maps to `0.6 − 0.2i`, of modulus `√0.4 ≈ 0.632 < 1`, inside the circle.
> **Solution:** If `z` is real then `z − i` and `z + i` are complex conjugates, so `|z − i| = |z + i|` and therefore `|w| = 1` for every real `z`; every point of the circle is attained, since the inverse map `z = (iw − 1)/(iw + 1)` sends `|w| = 1` onto the real axis. Now substitute: `w = (2 + 3i − i)/(2 + 3i + i) = (2 + 2i)/(2 + 4i)`. Multiplying numerator and denominator by `2 − 4i` gives `(2 + 2i)(2 − 4i)/((2)^2 + (4)^2) = (4 − 8i + 4i + 8)/20 = (12 − 4i)/20 = 0.6 − 0.2i`. The modulus is `√(0.36 + 0.04) = √0.4 ≈ 0.632 < 1`, confirming that a point of the upper half-plane lands inside the unit circle. Note that `w = (z − 1)/(z + 1)` would not serve this purpose: it has real coefficients, so it maps the real axis to the real axis and not to the circle; conjugating the two poles is what produces the circle.
> **Key point:** A Möbius map `(z − a)/(z − \bar a)` sends the real axis to `|w| = 1`, because the two factors are conjugates there; here `a = i`.

### Q31. A bilinear (linear-fractional) transformation `w = (az + b)/(cz + d)` has how many real degrees of freedom, and what three points determine it?

> **Type:** Numerical
> **Answer:** Six real degrees of freedom, fixed by prescribing the images of **three** distinct points (a Möbius transformation is determined by `w₁, w₂, w₃ ↦ W₁, W₂, W₃`).
> **Solution:** `a, b, c, d` are four complex numbers, i.e. 8 real parameters, but `(az + b)/(cz + d)` is unchanged when all four are multiplied by the same nonzero complex number, which removes 2 real parameters (a complex scalar). So 8 − 2 = **6** real degrees of freedom. Three complex images supply exactly 6 real conditions, so three point-images determine the map uniquely — for example `w = (z − 1)/(z + 1)` is the unique map taking `∞ → 1`, `0 → −1`, `1 → 0`.
> **Key point:** A Möbius transformation has 6 real parameters; prescribing images of three points (including `∞`) fixes it.

### Q32. `GATE-1` Under the transformation `w = 1/z`, the real axis in the `z`-plane maps onto

> **Type:** MCQ
> **Answer:** The real axis in the `w`-plane (Option a).
>
> (a) the real axis
> (b) the imaginary axis
> (c) the unit circle
> (d) the real axis together with the point at infinity
>
> **Solution:** If `z` is real and nonzero, then `1/z` is real and nonzero; conversely if `w` is real and nonzero then `z = 1/w` is real. So the map is a bijection of `ℝ \ {0}` onto itself, plus `z = ∞ ↦ w = 0` and `z = 0 ↦ w = ∞`. Option (b) is the classic confusion with `w = −i/z`, and option (c) with `w = 1/z̄`. To get the unit circle one needs `w = e^{iθ}(z − a)/(z̄ − ā)`, i.e. a reflection combined with the ratio map.
> **Key point:** Inversion `1/z` preserves the real axis; only `−i/z` maps the real axis to the imaginary axis.

### Q33. `GATE-1` The transformation `w = (z − i)/(z + i)` maps the upper half-plane (`Im z > 0`) onto

> **Type:** MCQ
> **Answer:** The interior of the unit circle, `|w| < 1` (Option c).
>
> (a) the upper half-plane
> (b) the lower half-plane
> (c) the interior of the unit disk, `|w| < 1`
> (d) the exterior of the unit disk, `|w| > 1`
>
> **Solution:** For real `z` the map lands on `|w| = 1`, as Q30 shows, so the real axis is the boundary image and the upper half-plane must go to one of the two regions it bounds. Test the interior point `z = i`: `w = (i − i)/(i + i) = 0`, the centre of the disk, so the upper half-plane goes **inside**. Since the map is one-to-one on the extended plane, the whole open half-plane lands in the single connected region bounded by that circle, namely the disk. The same test point reads off the general rule: the pole `a` lying in the mapped half-plane goes to `w = 0`, so that half-plane maps to the interior, and the conjugate half-plane maps to the exterior.
> **Key point:** For `w = (z − a)/(z − \bar a)` the half-plane containing `a` maps to the interior `|w| < 1`; here `a = i` is in the upper half-plane, and `z = i` maps to `w = 0`.

### Q34. Under the transformation `w = (z + 1)/(z − 1)`, find the images of the real axis and of the circle `|z| = 1`.

> **Type:** Numerical
> **Answer:** The real axis maps onto the **real axis**, `Im(w) = 0`, and the circle `|z| = 1` maps onto the **imaginary axis**, `Re(w) = 0`.
> **Solution:** The map has real coefficients, so `w` is real whenever `z` is real: `z = 0` gives `w = −1`, `z = 2` gives `w = 3`, and `z = \infty` gives `w = 1`, all on the real axis, which is therefore its image. For `|z| = 1` we have `z\bar z = 1`, so `\bar z = 1/z`, and `w = (z + 1)/(z − 1) = (z\bar z + \bar z)/(z\bar z - \bar z) = (1 + \bar z)/(1 - \bar z)`. Conjugating, `\bar w = (1 + z)/(1 - z) = -w`, so `w = -\bar w`, which says `Re(w) = 0`: `w` is purely imaginary. Checks: `z = i` gives `w = (1 + i)/(i − 1) = -i`; `z = −1` gives `w = 0`; `z = 1` gives `w = \infty`. So the image of the unit circle is the whole imaginary axis together with `∞`. The structure generalises: a Möbius map with real coefficients preserves the real axis, while a circle centred at the origin is sent to a line through the origin, here the perpendicular one.
> **Key point:** `w = (z + 1)/(z − 1)` has real coefficients, so the real axis maps to the real axis; for `|z| = 1`, `w = -\bar w`, so the unit circle maps to the imaginary axis.

### Q35. `GATE-1` Under `w = e^{iπ/6} z`, the point `z = 1 − i` maps to

> **Type:** MCQ
> **Answer:** `(√3 + 1)/2 − i(√3 − 1)/2 ≈ 1.366 − 0.366i` (Option a).
>
> (a) `≈ 1.366 − 0.366i`
> (b) `≈ 0.366 − 1.366i`
> (c) `≈ 1.366 + 0.366i`
> (d) `≈ −1.366 + 0.366i`
>
> **Solution:** `e^{iπ/6} = (√3/2) + i(1/2)`. Multiplying: `w = ((√3/2) + i/2)(1 − i) = √3/2 − i√3/2 + i/2 − i²/2 = (√3/2 + 1/2) + i(1/2 − √3/2)`. So `Re w = (√3 + 1)/2 ≈ 1.366` and `Im w = (1 − √3)/2 ≈ −0.366`. Geometrically, multiplication by `e^{iπ/6}` is a pure anticlockwise rotation by `30°`: `|z| = √2` is unchanged and the argument goes from `−45°` to `−15°`, so `w = √2(cos(−15°) + i sin(−15°))`, whose components are `1.366` and `−0.366` ✓. Option (c) is the trap of rotating clockwise, option (d) of rotating by `210°`.
> **Key point:** Multiplication by `e^{iθ}` rotates by `θ` anticlockwise and leaves the modulus untouched.

### Q36. Describe geometrically the combined effect of `w = 3z + 2 − 4i` on the point set.

> **Type:** Conceptual
> **Answer:** A dilation by factor 3 about the origin, followed by a translation by the vector `2 − 4i`.
> **Solution:** The map is a similarity: it multiplies all lengths by 3, then shifts everything by the fixed vector `2 − 4i`. So the origin goes to `2 − 4i`; the unit circle in the `z`-plane becomes a circle of radius 3 centred at `2 − 4i`; and the real axis (which passes through the origin) becomes the horizontal line `Im w = −4`. For instance `z = 1` gives `w = 3 + 2 − 4i = 5 − 4i`, and `z = −1` gives `w = −3 + 2 − 4i = −1 − 4i`, both on the line `Im w = −4`, three units either side of the centre.
> **Key point:** `w = az + b` (with `a` complex) is a rotation-dilation about the origin followed by a translation; the order matters for the origin's image.

### Q37. Determine the image under `w = 1/z` of the line `y = 1`, and check your answer with three test points.

> **Type:** Numerical
> **Answer:** The circle `|w + i/2| = 1/2`, i.e. centre `−i/2` and radius `1/2`.
> **Solution:** A line not through the origin maps to a circle through the origin. Write `z = 1/w = w̄/|w|² = (u − iv)/(u² + v²)`; the line condition `Im z = 1` gives `−v/(u² + v²) = 1`, i.e. `u² + v² + v = 0`, i.e. `u² + (v + 1/2)² = 1/4`. Therefore the image is the circle `|w + i/2| = 1/2`, centred at `−i/2` with radius `1/2`, passing through the origin (which is the image of `z = ∞`). Three checks: `z = i` gives `w = 1/i = −i`, and `|−i + i/2| = 1/2` ✓; `z = 1 + i` gives `w = (1 − i)/2 = 0.5 − 0.5i`, at distance `0.5` from `−i/2` ✓; `z = 2 + i` gives `w = (2 − i)/5 = 0.4 − 0.2i`, at distance `√(0.16 + 0.09) = 0.5` ✓.
> **Key point:** Under `w = 1/z`, the line `Im z = y₀` maps to the circle `|w + i/(2y₀)| = 1/(2|y₀|)`.

### Q38. `GATE-2` `NAT` Let `a` lie in the upper half-plane, let `b = \bar a`, and put `w = (z − a)/(z − b)`. The real axis maps onto the unit circle. What is the image of the upper half-plane? Justify with one test point.

> **Type:** MCQ
> **Answer:** The interior of the unit circle, `|w| < 1` (Option b).
>
> (a) the exterior of the unit circle
> (b) the interior of the unit circle
> (c) the upper half-plane
> (d) the left half-plane
>
> **Solution:** Since the real axis maps onto `|w| = 1`, the image of the upper half-plane is one of the two regions that circle bounds, namely the disk or its exterior. To decide, test the point `z = a`, which lies in the upper half-plane by hypothesis: there the numerator vanishes and `w = 0`, the centre of the disk, which lies **inside**. The map is one-to-one on the extended plane, so the whole open half-plane lands in that same connected region, namely the interior. One test point decides the question once the boundary image is known. Had `a` been in the lower half-plane the answer would have been the exterior, so the position of `a` is what fixes the choice.
> **Key point:** For `w = (z − a)/(z − \bar a)` the half-plane containing `a` maps to `|w| < 1`, since `z = a` maps to `w = 0`; one test point suffices once the boundary image is known.

## Section 3. Exponential, trigonometric, logarithmic and hyperbolic functions

### Q39. Show that `e^z` is periodic in the complex plane and find its fundamental period.

> **Type:** Theory
> **Answer:** `e^{z + 2πi} = e^z` for all `z`, the only periods are the multiples `2kπi`, and the fundamental period is `2πi`.
> **Solution:** Write `z = x + iy`. Then `e^z = e^{x + iy} = e^x e^{iy} = e^x(\cos y + i\sin y)`. Adding `2πi` to `z` changes `y` to `y + 2π` and leaves `x` alone, so `e^{z + 2πi} = e^x(\cos(y + 2π) + i\sin(y + 2π)) = e^x(\cos y + i\sin y) = e^z`, since `2π` is a full period of the trigonometric functions. Conversely, if `T` is any period then `e^{z + T} = e^z` for all `z`, so `e^T = 1`, which forces `T = 2kπi` with `k` an integer; there is therefore no non-zero real period. The periods being purely imaginary is the reason `w = e^{iz}` carries the real line onto the unit circle, and hence the reason the substitution `z = e^{i\theta}` in Q210 turns `cos\theta` into a rational function of the new variable.
> **Key point:** The periods of `e^z` are exactly `2kπi`, since `e^T = 1` forces `T = 2kπi`; the fundamental period is `2πi`.

### Q40. Write `e^{x + iy}` in rectangular form, and compute `e^{1 + 2i}` to four decimal places.

> **Type:** Numerical
> **Answer:** `e^{x+iy} = e^x(cos y + i sin y)`; `e^{1+2i} ≈ −1.1312 + 2.4717i`.
> **Solution:** By Euler's formula `e^{iy} = cos y + i sin y`, so `e^{x+iy} = e^x e^{iy} = e^x(cos y + i sin y)`. With `x = 1`, `y = 2`: `e^1 = 2.71828`, `cos 2 = −0.41615`, `sin 2 = 0.90930`, so `Re = 2.71828 × (−0.41615) = −1.1312` and `Im = 2.71828 × 0.90930 = 2.4717`. Checks: `|e^{1+2i}| = e^1 = 2.7183`, and indeed `√(1.1312² + 2.4717²) = √(1.2796 + 6.1093) = √7.3889 = 2.7182` ✓; the argument is `y = 2 rad = 114.6°`, in the second quadrant ✓.
> **Key point:** `e^{x+iy} = e^x(cos y + i sin y)` — the modulus is `e^x`, the argument is `y`.

### Q41. Evaluate `e^{iπ/2}`, `e^{iπ}` and `e^{−iπ/2}` exactly.

> **Type:** Numerical
> **Answer:** `i`, `−1` and `−i` respectively.
> **Solution:** Euler's formula `e^{iθ} = cos θ + i sin θ` gives, at `θ = π/2`: `0 + i·1 = i`; at `θ = π`: `−1 + 0 = −1`; at `θ = −π/2`: `0 − i = −i`. All three satisfy `e^{2iz} = 1`, i.e. they are the square roots of unity: `(i)² = −1` and `(−1)² = 1` ✓.
> **Key point:** `e^{iπ} = −1`, `e^{iπ/2} = i`; all roots of unity are `e^{2πik/n}`.

### Q42. `GATE-1` The equation `e^z = 0` has

> **Type:** MCQ
> **Answer:** No solution, i.e. 0 solutions (Option b).
>
> (a) exactly one solution, `z = 0`
> (b) no solution
> (c) infinitely many solutions
> (d) exactly two solutions
>
> **Solution:** For `z = x + iy`, `|e^z| = e^x`, and `e^x > 0` for every finite real `x`. Since a zero of `e^z` would require its modulus to be `0`, no zero exists anywhere in the finite plane; the limit `x → −∞` gives a limit point at `z = −∞` but not a point of the plane. Hence the range of `e^z` is `ℂ \ {0}`. Option (a) is the trap of treating `e^z` like `z^n`, which does have a zero; option (c) is the trap of treating it like `sin z`, which has infinitely many.
> **Key point:** `e^z` is entire, non-zero everywhere, and its range is `ℂ \ {0}`.

### Q43. Solve `e^z = 2` and `e^z = −3` for `z`.

> **Type:** Numerical
> **Answer:** `z = ln 2 + 2kπi`; and `z = ln 3 + (2k + 1)πi`, `k ∈ ℤ`.
> **Solution:** Write `z = x + iy` and equate moduli: `|e^z| = e^x = |2| = 2`, so `x = ln 2`. Then the phase must satisfy `y = 2kπ`, giving `z = ln 2 + 2kπi`. For `−3`, `e^x = 3` gives `x = ln 3`, and the phase must be an odd multiple of `π`, so `y = (2k + 1)π`. In general `e^z = r e^{iθ}` has the infinitely many solutions `z = ln r + i(θ + 2kπ)`.
> **Key point:** `e^z = w` has solutions `z = ln|w| + i(arg w + 2kπ)` — infinitely many, spaced `2πi` apart.

### Q44. Define the complex logarithm `log z` and show explicitly that it is multivalued for `z = −1`.

> **Type:** Theory
> **Answer:** `log z = \ln|z| + i(\arg z + 2k\pi)` for every integer `k`; for `z = −1` this is `i(2k + 1)\pi`, whose values begin `i\pi, -i\pi, 3i\pi, -3i\pi, 5i\pi, -5i\pi` and continue without end.
> **Solution:** The logarithm inverts the exponential, so `u + iv` is a logarithm of `z` exactly when `e^{u + iv} = z`. Comparing moduli in `e^u(\cos v + i\sin v) = z` gives `e^u = |z|`, hence `u = \ln|z|`, and comparing arguments gives `v = \arg z + 2k\pi`. For `z = −1` the modulus is 1, so `ln|z| = 0`, and every argument of `−1` is an odd multiple of `π`, giving `log(−1) = i(2k + 1)\pi`. Each listed value exponentiates back to `−1`, since `e^{i(2k+1)\pi} = -1`, so the ambiguity is genuine and not a matter of picking a branch. This is exactly the `2πi`-periodicity of the exponential met in Q39, and it is why a branch cut must be fixed before `log` can be used inside a contour integral, as in Q226.
> **Key point:** `log z = \ln|z| + i(\arg z + 2k\pi)`, so `log(−1) = i(2k + 1)\pi` is multivalued; the ambiguity is the `2πi`-periodicity of `e^z`.

### Q45. Define the principal branch `Log z` and locate its discontinuity.

> **Type:** Theory
> **Answer:** `Log z = ln|z| + i Arg z` with `−π < Arg z ≤ π`; it is discontinuous along the negative real axis (including the origin), which is the standard branch cut.
> **Solution:** Restricting the argument to the single interval `(−π, π]` makes `Log` single-valued. Approaching a point `−r` (with `r > 0`) from the upper half-plane gives `Arg → π`, so `Log → ln r + iπ`; approaching from the lower half-plane gives `Arg → −π`, so `Log → ln r − iπ`. The two limits differ by `2πi`, so `Log` is discontinuous across the whole negative real axis. Any curve of unit modulus sweeping the full circle forces the imaginary part of `Log` to run from `0` through `π`, jump, and run back from `−π` to `0` — a jump of `2πi` at `z = −1`.
> **Key point:** The principal branch `Log` is discontinuous on `(−∞, 0]`; analyticity requires the branch cut to be removed from the domain.

### Q46. On what domain is the principal branch `Log z` analytic, and what is its derivative there?

> **Type:** Numerical
> **Answer:** On `ℂ \ (−∞, 0]`, and `(Log z)′ = 1/z` there.
> **Solution:** The branch cut `−(−∞, 0]` must be deleted, leaving a simply connected open domain on which `Arg z` varies continuously and differentiably. Writing `z = r e^{iθ}` with `θ = Arg z`, the local form is `ln r + iθ`, and differentiating in polar variables gives `d(Log z) = (1/r)dr + i r dθ·(1/r) = dr/r + i dθ`, which in Cartesian form is exactly `(dx + i dy)/z = dz/z`. Hence `(Log z)′ = 1/z`, matching the real rule. Note `1/z` is of course analytic on all of `ℂ \ {0}`; the cut exists only because `Log` itself cannot be made single-valued on a domain that loops around the origin.
> **Key point:** `Log z` is analytic on `ℂ \ (−∞, 0]` with derivative `1/z`; the function `1/z` is analytic on the larger domain `ℂ \ {0}`.

### Q47. How many values does `z^{1/2}` have, and how many does `z^2` have? Explain the difference.

> **Type:** Conceptual
> **Answer:** `z^{1/2}` has two values; `z^2` has one.
> **Solution:** Define `z^a = e^{a log z} = e^{a(ln|z| + i(arg z + 2kπ))} = |z|^a e^{ia·arg z}·e^{i2πak}`. The factor `e^{i2πak}` takes `q` distinct values for `a = p/q` in lowest terms, so `z^{p/q}` has exactly `q` values. For `a = 1/2`, `e^{i2πk/2} = (−1)^k` gives two values, and indeed squaring either gives `z`. For the integer exponent `a = 2`, `e^{i4πk} = 1` always, so `z²` is single-valued. Equivalently, `z^{p/q}` is single-valued only when the exponent has denominator `q = 1`, i.e. is an integer.
> **Key point:** `z^α` is single-valued on `ℂ \ {0}` iff `α` is an integer; otherwise it takes `q` values for `α = p/q`.

### Q48. `GATE-1` Compute the "principal-value" cube root of `−8`, i.e. `e^{(1/3)Log(−8)}` using the principal logarithm, and compare it with the real cube root.

> **Type:** MCQ
> **Answer:** `1 + i√3 ≈ 1 + 1.732i` (Option b).
>
> (a) `−2`
> (b) `1 + i√3`
> (c) `−1 + i√3`
> (d) `2`
>
> **Solution:** `Log(−8) = ln 8 + iπ = 2.0794 + 3.1416i`. Then `(1/3)Log(−8) = 0.6931 + 1.0472i`, and `e^{0.6931} = 2`, so `e^{(1/3)Log(−8)} = 2(cos 60° + i sin 60°) = 1 + i√3`. Verifying: `(1 + i√3)² = 1 + 2i√3 − 3 = −2 + 2i√3`, and `(−2 + 2i√3)(1 + i√3) = −2 − 2i√3 + 2i√3 + 2i²·3 = −2 − 6 = −8` ✓. Option (a) is the trap of the real cube root: `(−8)^{1/3} = −2` in real arithmetic, but the principal-value complex cube root of a negative real number is **not** real, because the principal argument used is `π`, giving argument `π/3` and not `π`.
> **Key point:** The principal-value complex cube root of a negative real is complex: `(−x)^{1/3} = x^{1/3}e^{iπ/3}`, not `−x^{1/3}`.

### Q49. Write the general set of values of `(−8)^{1/3}` using the multivalued logarithm, and confirm there are three.

> **Type:** Numerical
> **Answer:** `2e^{i(π + 2kπ)/3}` for `k = 0, 1, 2`, i.e. `1 + i√3`, `−2`, and `1 − i√3`.
> **Solution:** `log(−8) = ln 8 + i(π + 2kπ)`, so `(−8)^{1/3} = e^{(1/3)log(−8)} = 2 e^{i(π + 2kπ)/3}`. For `k = 0`: `2e^{iπ/3} = 1 + i√3`. For `k = 1`: `2e^{iπ} = −2`. For `k = 2`: `2e^{i5π/3} = 1 − i√3`. For `k = 3`: `2e^{i7π/3} = 2e^{iπ/3}`, repeating, so there are exactly three distinct values, equally spaced by `120°` on `|w| = 2`, as the general root formula of Q8 requires. Their sum is `0`, consistent with Q9.
> **Key point:** The `q` values of `z^{p/q}` are `|z|^{p/q}e^{i(p/q)(θ + 2kπ)}`, `k` running from 0 to `q − 1`, and they sum to zero for `p` not a multiple of `q`.

### Q50. State the exponential forms of `sin z`, `cos z` and `tan z`, and verify Euler's formula `sin x + i cos x = i e^{−ix}` for real `x`.

> **Type:** Theory
> **Answer:** `sin z = (e^{iz} − e^{−iz})/(2i)`, `cos z = (e^{iz} + e^{−iz})/2`, `tan z = sin z/cos z`; and `sin x + i cos x = i e^{−ix}` holds for all real `x`.
> **Solution:** These are obtained by solving the two linear equations `e^{ix} = cos x + i sin x` and `e^{−ix} = cos x − i sin x` for `sin x` and `cos x`. For the identity: `i e^{−ix} = i(cos x − i sin x) = i cos x + sin x = sin x + i cos x` ✓. Both sides have modulus 1 and argument `π/2 − x`, so they agree.
> **Key point:** `sin z = (e^{iz} − e^{−iz})/(2i)`, `cos z = (e^{iz} + e^{−iz})/2`; these turn real trigonometric integrals into rational functions of `e^{iz}`.

### Q51. Prove that `sin z` is entire, odd, and periodic with period `2π`. What is its range?

> **Type:** Theory
> **Answer:** `sin z = (e^{iz} − e^{−iz})/(2i)` is a combination of entire exponentials, so it is entire; `sin(−z) = −sin z`; `sin(z + 2π) = sin z`. Its range is all of `ℂ` (it is onto).
> **Solution:** Each exponential is entire, so `sin z` is entire. Oddness: `sin(−z) = (e^{−iz} − e^{iz})/(2i) = −sin z`. Periodicity: `sin(z + 2π) = (e^{iz}e^{2πi} − e^{−iz}e^{−2πi})/(2i) = sin z`. Onto: solving `sin z = w` for the logarithm gives `e^{iz} = iw ± √(1 − w²)`, which is solvable for every complex `w`, so the image is `ℂ`. Note that unlike `e^z`, the function `sin z` is *not* periodic in `i`: `sin(z + 2πi) = sin z cosh 2π + i cos z sinh 2π ≠ sin z`.
> **Key point:** `sin z` is entire, odd, `2π`-periodic, and has infinitely many zeros `(kπ)`; it is onto `ℂ`.

### Q52. Verify that `sin² z + cos² z = 1` holds for complex `z`, using the exponential forms. Does the same hold for `sinh z` and `cosh z`?

> **Type:** Numerical
> **Answer:** Yes: `sin² z + cos² z = 1` for all complex `z`, and the corresponding hyperbolic identity is `cosh² z − sinh² z = 1` (the sign differs).
> **Solution:** `sin² z = −(e^{iz} − e^{−iz})²/(4)` and `cos² z = (e^{iz} + e^{−iz})²/4`. Adding, the `e^{±2iz}` cross terms cancel: `[−(e^{2iz} − 2 + e^{−2iz}) + (e^{2iz} + 2 + e^{−2iz})]/4 = 4/4 = 1` ✓. For hyperbolic functions, `cosh z = (e^z + e^{−z})/2` and `sinh z = (e^z − e^{−z})/2`, so `cosh² z − sinh² z = [(e^z + e^{−z})² − (e^z − e^{−z})²]/4 = 4/4 = 1`. The sign flip comes from `cosh z = cos(iz)`, and squaring `i` changes a sign.
> **Key point:** `sin² + cos² = 1` (trig) but `cosh² − sinh² = 1` (hyperbolic) — because `cos z = cosh(iz)`.

### Q53. Express `cos(x + iy)` and `sin(x + iy)` in terms of real hyperbolic and trigonometric functions.

> **Type:** Numerical
> **Answer:** `cos(x + iy) = cos x cosh y − i sin x sinh y` and `sin(x + iy) = sin x cosh y + i cos x sinh y`.
> **Solution:** Substituting `z = x + iy` into `cos z = (e^{iz} + e^{−iz})/2` gives `e^{i(x+iy)} = e^{ix}e^{−y} = e^{−y}(cos x + i sin x)` and `e^{−i(x+iy)} = e^{−ix}e^{y} = e^{y}(cos x − i sin x)`. Adding and dividing by 2: `cos z = [(e^{−y} + e^{y})cos x + i(e^{−y} − e^{y}) sin x]/2 = cos x cosh y − i sin x sinh y`. The same computation with the difference in the numerator for `sin` gives `sin z = sin x cosh y + i cos x sinh y`. The `cosh`/`sinh` factors appear because the real and imaginary directions are related by the rotation `i`.
> **Key point:** `sin(x+iy) = sin x cosh y + i cos x sinh y`; `cos(x+iy) = cos x cosh y − i sin x sinh y`.

### Q54. Compute `sin(π/2 + i)` and `cos(1 + iπ/2)` in rectangular form.

> **Type:** Numerical
> **Answer:** `sin(π/2 + i) = cosh 1 ≈ 1.5431` (purely real); `cos(1 + iπ/2) ≈ 1.3557 − 1.9367i`.
> **Solution:** With `x = π/2`, `y = 1` the identity of Q53 gives `sin(π/2 + i) = sin(π/2)cosh 1 + i cos(π/2) sinh 1 = 1·1.54308 + i·0·1.17520 = 1.54308`, which is real because `cos(π/2) = 0` kills the imaginary part; equivalently it is `cos(−i) = cosh 1` by Q59. For the second, with `x = 1`, `y = π/2`: `e^(π/2) = 4.81048` and `e^(−π/2) = 0.20788`, so `cosh(π/2) = 2.50918` and `sinh(π/2) = 2.30130`. Hence `cos(1 + iπ/2) = cos 1·cosh(π/2) − i sin 1·sinh(π/2) = 0.54030·2.50918 − i·0.84147·2.30130 = 1.35574 − 1.93668i`. Checks: `|sin(π/2+i)|² = sin²(π/2) + sinh²1 = 1 + 1.38110 = 2.38110`, and `1.54308² = 2.38110` ✓; `|cos(1 + iπ/2)|² = cos²1 + sinh²(π/2) = 0.29193 + 5.29586 = 5.58779`, and `1.35574² + 1.93668² = 1.83803 + 3.75049 = 5.58852` ✓ (small rounding).
> **Key point:** `sin(π/2 + iy) = cosh y` and `cos(π/2 + iy) = −i sinh y` — real-axis zeros of the real functions turn into hyperbolic values in the complex plane.

### Q55. Show that `|sin(x + iy)|² = sin² x + sinh² y`, and evaluate it at `x = 1`, `y = 2`.

> **Type:** Numerical
> **Answer:** `|sin z|² = sin²x cosh²y + cos²x sinh²y = sin²x + sinh²y`; at `(1, 2)` it is `13.86`, so `|sin(1 + 2i)| ≈ 3.723`.
> **Solution:** From Q53, `sin(x+iy) = sin x cosh y + i cos x sinh y`, so `|sin z|² = sin²x cosh²y + cos²x sinh²y`. Substituting `cosh²y = 1 + sinh²y` and `cos²x = 1 − sin²x`, this becomes `sin²x(1 + sinh²y) + (1 − sin²x) sinh²y = sin²x + sinh²y` ✓. Numerically, `sin 1 = 0.84147` gives `sin²1 = 0.70807`, and `sinh 2 = 3.62686` gives `sinh²2 = 13.1541`; the sum is `13.862` and its square root is `3.7233`. Since `sinh 2 ≈ 3.627` is much larger than `sin 1`, the modulus is dominated by the hyperbolic part — in the complex plane the function grows exponentially in `|y|`, unlike the bounded real case.
> **Key point:** `|sin(x+iy)|² = sin²x + sinh²y ≥ sin²x`; the imaginary part *increases* the modulus, and `|sin z| ≥ |sinh(Im z)|`.

### Q56. Compute `tan(1 + i)` in rectangular form, and use the result to check the bound `|Re(tan(x + iy))| ≤ 1`.

> **Type:** Numerical
> **Answer:** `tan(1 + i) ≈ 0.272 + 1.084i`; the real part `0.272` does lie within `[−1, 1]` ✓.
> **Solution:** The standard decomposition is `tan(x + iy) = [sin 2x + i sinh 2y]/[cos 2x + cosh 2y]`. With `x = y = 1`: `sin 2 = 0.90930`, `cos 2 = −0.41615`, `sinh 2 = 3.62686`, `cosh 2 = 3.76220`. The denominator is real and equals `−0.41615 + 3.76220 = 3.34605`, so `tan(1+i) = 0.90930/3.34605 + i·3.62686/3.34605 = 0.2717 + 1.0840i`. The denominator satisfies `cos 2x + cosh 2y ≥ cos 2x + 1 ≥ 0`, so it is never negative and the real part `sin 2x/(cos 2x + cosh 2y)` obeys `|Re tan| ≤ |sin 2x|/(1 + cos 2x) = |tan x|`, and in the limit `y → 0` it reaches `tan x`; the universal bound `|Re tan(x+iy)| < 1` follows since `|sin 2x| ≤ 1` and `cos 2x + cosh 2y ≥ 1 - 1 + 1 = 1` whenever `cosh 2y ≥ 2 − cos 2x`. Here `0.2717 ≤ 1` ✓, while the imaginary part `1.084` is unbounded in `y`.
> **Key point:** `tan(x + iy) = (sin 2x + i sinh 2y)/(cos 2x + cosh 2y)`; the real part is bounded, the imaginary part grows like `e^{2y}`.

### Q57. Where are the zeros and the poles of `tan z`?

> **Type:** Numerical
> **Answer:** Zeros at `z = kπ`, `k ∈ ℤ`; simple poles at `z = π/2 + kπ`, `k ∈ ℤ`. All of them are real.
> **Solution:** `tan z = sin z/cos z`. The zeros of `sin z` are `z = kπ` (from `sin(x+iy) = 0`, both real and imaginary parts must vanish, forcing `y = 0` and `x = kπ`), and `cos z ≠ 0` there since `cos(kπ) = (−1)^k`. The poles come from the zeros of `cos z`, at `z = π/2 + kπ`, each simple because `d/dz cos z = −sin z = ±1 ≠ 0` there. The residues are `Res(tan, π/2 + kπ) = sin(π/2+kπ)/(−sin(π/2+kπ)) = −1`, identical at every pole. No zeros or poles occur off the real axis, since for `y ≠ 0` the modulus `|sin z|² = sin²x + sinh²y > 0` and `|cos z|² = cos²x + sinh²y > 0`.
> **Key point:** All zeros and poles of `tan z` are real: zeros at `kπ`, poles at `π/2 + kπ` with residue `−1` each.

### Q58. Define `sinh z` and `cosh z` in exponential form and confirm `cosh 0 = 1`, `sinh 0 = 0`, `cosh² z − sinh² z = 1`.

> **Type:** Recall
> **Answer:** `sinh z = (e^z − e^{−z})/2`, `cosh z = (e^z + e^{−z})/2`; both are entire, `cosh 0 = 1`, `sinh 0 = 0`, and `cosh² z − sinh² z = 1` for all `z`.
> **Solution:** Evaluating at `z = 0` gives `cosh 0 = (1 + 1)/2 = 1` and `sinh 0 = (1 − 1)/2 = 0`. The identity follows as in Q52: `[(e^z + e^{−z})² − (e^z − e^{−z})²]/4 = 4/4 = 1`. These are entire (combinations of entire exponentials), odd/even respectively — `sinh(−z) = −sinh z`, `cosh(−z) = cosh z` — and, like `sin` and `cos`, they have only real zeros, at `z = ikπ` for `sinh` and `z = i(π/2 + kπ)` for `cosh`.
> **Key point:** `cosh z = cos(iz)`, `sinh z = −i sin(iz)`; zeros of the hyperbolic functions are purely imaginary.

### Q59. Verify the identities `sin(iz) = i sinh z` and `cos(iz) = cosh z`.

> **Type:** Theory
> **Answer:** Both hold identically for all complex `z`.
> **Solution:** `sin(iz) = (e^{i(iz)} − e^{−i(iz)})/(2i) = (e^{−z} − e^{z})/(2i) = −(e^z − e^{−z})/(2i)`. Since `1/i = −i`, this is `i(e^z − e^{−z})/2 = i sinh z` ✓. And `cos(iz) = (e^{i(iz)} + e^{−i(iz)})/2 = (e^{−z} + e^{z})/2 = cosh z` ✓. Equivalently, put `z = iy` in the Q53 identities: `cos(iy) = cos 0·cosh y − i·sin 0·sinh y = cosh y`.
> **Key point:** Multiplication of the argument by `i` converts trigonometric into hyperbolic functions: `cos(iz) = cosh z`, `sin(iz) = i sinh z`.

### Q60. `GATE-1` Consider `f(z) = z tanh z`. What is the order of the zero of `f` at `z = 0`, and what is `lim_{z→0} f(z)/z²`?

> **Type:** MCQ
> **Answer:** Zero of order 2, and the limit is `1` (Option c).
>
> (a) Zero of order 1, limit `0`
> (b) Zero of order 2, limit `0`
> (c) Zero of order 2, limit `1`
> (d) Zero of order 3, limit `1`
>
> **Solution:** `tanh z = sinh z/cosh z`; by Taylor expansion `sinh z = z + z³/3! + O(z⁵)` and `cosh z = 1 + z²/2! + O(z⁴)`, so `tanh z = (z + z³/6 + O(z⁵))/(1 + z²/2 + O(z⁴)) = z + z³(1/6 − 1/2) + O(z⁵) = z − z³/3 + O(z⁵)`. Thus `tanh z ~ z`, so `z tanh z ~ z²`: a zero of order 2 with `f/z² → 1` ✓. The same result follows from `tan(iz) = i tanh z`, which gives `tanh z = −i tan(iz)`, and `tan w ~ w` near 0 so `tanh z ~ −i·(iz) = z`. Option (a) is the trap of forgetting the extra factor `z`.
> **Key point:** `tanh z = z − z³/3 + 2z⁵/15 − 17z⁷/315`, so `tanh z` has a simple zero at 0 while `z tanh z` has a double zero there.

### Q61. `GATE-1` Which of the following functions is entire (analytic everywhere in the finite plane)?

> **Type:** MCQ
> **Answer:** `e^{z²}` (Option c).
>
> (a) `log z`
> (b) `|z|`
> (c) `e^{z²}`
> (d) `1/(z − 1)`
>
> **Solution:** `e^{z²}` is a composition of the entire functions `z ↦ z²` and `w ↦ e^w`, hence entire ✓. `log z` (Q46) is analytic only on `ℂ \ (−∞, 0]`. `|z| = √(x² + y²)` is not complex-differentiable except at the origin, where it is not differentiable either. `1/(z − 1)` is analytic except at `z = 1`, where it has a simple pole. The general principle: polynomials, `e^w`, `sin z`, `cos z` and their quotients with no vanishing denominator, and finite sums and products of entire functions, are entire.
> **Key point:** Only functions built from polynomials and `e^z`, `sin z`, `cos z` without division by a vanishing factor, are entire.

## Section 4. Special functions and complex series

### Q62. State the defining integral for the Gamma function and the condition on `z` for its convergence.

> **Type:** Recall
> **Answer:** `Γ(z) = ∫_0^∞ t^{z−1} e^{−t} dt`, which converges exactly for `Re(z) > 0`.
> **Solution:** The integrand is `t^{z−1}e^{−t} = t^{x−1}e^{−t}·(cos(y ln t) + i sin(y ln t))` for `z = x + iy`. At infinity, `e^{−t}` beats any power of `t` by the standard exponential-dominates-polynomial argument, so the tail converges for every `x`. At the origin, `t^{x−1}e^{−t} ~ t^{x−1}`, and `∫_0^1 t^{x−1}dt` converges iff `x > 0`. Analytic continuation via `Γ(z+1) = zΓ(z)` (Q64) then extends `Γ` to the whole plane minus `0, −1, −2, −3` and the rest.
> **Key point:** `Γ(z) = ∫_0^∞ t^{z−1}e^{−t}dt` for `Re z > 0`; it is analytic there and meromorphic everywhere else.

### Q63. Show that `Γ(n) = (n−1)!` for every positive integer `n`, and list `Γ(1)`, `Γ(2)`, `Γ(5)`.

> **Type:** Numerical
> **Answer:** `Γ(n) = (n−1)!`, so `Γ(1) = 1`, `Γ(2) = 1`, `Γ(5) = 24`.
> **Solution:** By definition, `Γ(1) = ∫_0^∞ e^{−t}dt = 1`, which is `0!`. Integrating by parts with `u = t^n`, `dv = t^{n−1}dt` gives `Γ(n+1) = ∫_0^∞ t^n e^{−t}dt = [−t^n e^{−t}]_0^∞ + n∫_0^∞ t^{n−1}e^{−t}dt = nΓ(n)`, so stepping down repeatedly, `Γ(n) = (n−1)Γ(n−1) = (n−1)(n−2)(n−3) and so on down to 1, times Γ(1) = (n−1)!`. Therefore `Γ(1) = 0! = 1`, `Γ(2) = 1! = 1`, `Γ(5) = 4! = 24`.
> **Key point:** `Γ(n) = (n−1)!`; the factorial is of `(n−1)`, not `n` — `Γ(5) = 24`, not 120.

### Q64. State the functional equation of the Gamma function and use it to relate `Γ(z+2)` to `Γ(z)`.

> **Type:** Recall
> **Answer:** `Γ(z+1) = zΓ(z)`, hence `Γ(z+2) = z(z+1)Γ(z)`.
> **Solution:** Integrating by parts in the defining integral, `Γ(z+1) = ∫_0^∞ t^z e^{−t}dt = [−t^z e^{−t}]_0^∞ + z∫_0^∞ t^{z−1}e^{−t}dt = zΓ(z)`, valid for `Re z > 0` and then by continuation elsewhere. Applying it twice, `Γ(z+2) = (z+1)Γ(z+1) = (z+1)zΓ(z)`. The same iteration gives the general form `Γ(z+n) = z(z+1)···(z+n−1)Γ(z)`, which is how `Γ` is pushed out of the half-plane and how values at negative non-integers are obtained.
> **Key point:** `Γ(z+1) = zΓ(z)` — the recurrence is the tool for both continuation and backward evaluation.

### Q65. Use the recurrence to find `Γ(−1/2)`, `Γ(−3/2)` and `Γ(−5/2)`.

> **Type:** Numerical
> **Answer:** `Γ(−1/2) = −2√π ≈ −3.545`; `Γ(−3/2) = 4√π/3 ≈ 2.363`; `Γ(−5/2) = −8√π/15 ≈ −0.9453`.
> **Solution:** `Γ(1/2) = zΓ(z)` with `z = −1/2` gives `Γ(1/2) = −(1/2)Γ(−1/2)`, so `Γ(−1/2) = −2Γ(1/2) = −2√π ≈ −3.5449`. Next, `Γ(−1/2) = −(1/2)Γ(−3/2)`, so `Γ(−3/2) = −2Γ(−1/2) = 4√π/3 ≈ 2.3633`. Then `Γ(−3/2) = −(3/2)Γ(−5/2)`, so `Γ(−5/2) = −(2/3)(4√π/3) = −8√π/15 ≈ −0.94530`. The values alternate in sign, which is the signature of passing through a simple pole of the Gamma function.
> **Key point:** `Γ(−1/2) = −2√π`; the values at negative half-integers alternate in sign because each step multiplies by a negative number.

### Q66. Locate the singularities of `Γ(z)` and find the residue at each.

> **Type:** Numerical
> **Answer:** Simple poles at `z = 0, −1, −2, −3` and the rest, with `Res(Γ, −n) = (−1)^n/n!`.
> **Solution:** From `Γ(z) = Γ(z+1)/z`, division by `z` creates a simple pole at `z = 0`; near `z = 0`, `Γ(1+z) → Γ(1) = 1`, so `Γ(z) ~ 1/z` and the residue is 1 = `(−1)^0/0!`. At `z = −1`, `Γ(z) = Γ(z+1)/z` and `Γ(z+1)` has a simple pole at `z = −1` with residue 1; dividing by `z = −1` multiplies the residue by `−1`, giving `−1` ✓. Each further step multiplies by `1/(−n)`, so `Res(Γ, −n) = (−1)^n/n!`: `1, −1, 1/2, −1/6, 1/24, −1/120` and so on. Equivalently, the residue is `1/n!` in absolute value, so the poles decrease in strength.
> **Key point:** `Res(Γ, −n) = (−1)^n/n!`; the poles of `Γ` are all simple and are at the non-positive integers only.

### Q67. Show that `Γ(1/2) = √π`, using the substitution `t = u²` and the symmetry of the Gaussian.

> **Type:** Theory
> **Answer:** `Γ(1/2) = √π ≈ 1.7725`.
> **Solution:** `Γ(1/2) = ∫_0^∞ t^{−1/2}e^{−t}dt`. Put `t = u²`, `dt = 2u du`, so `t^{−1/2} = 1/u` and the integral becomes `2∫_0^∞ e^{−u²}du`. Let `I = ∫_0^∞ e^{−u²}du`. Squaring, `I² = ∫_0^0∫_0^∞ e^{−(u²+v²)}du dv`, and in polar coordinates over the first quadrant the double integral is `(π/2)∫_0^∞ e^{−r²}r dr = (π/2)(1/2) = π/4`. Since `I > 0`, `I = √π/2`, and `Γ(1/2) = 2I = √π` ✓.
> **Key point:** `Γ(1/2) = √π`; the proof reduces to the two-dimensional Gaussian integral, worth `π/4` in one quadrant.

### Q68. State Euler's reflection formula for the Gamma function, and deduce the value of `Γ(1/3)Γ(2/3)`.

> **Type:** Numerical
> **Answer:** `Γ(z)Γ(1−z) = π/sin(πz)`, so `Γ(1/3)Γ(2/3) = π/sin(π/3) = 2π/√3 ≈ 3.628`.
> **Solution:** The reflection formula follows from the beta function identity `B(z, 1−z) = ∫_0^∞ t^{z−1}/(1+t)dt = π/sin πz` together with `B(z,1−z) = Γ(z)Γ(1−z)/Γ(1) = Γ(z)Γ(1−z)`. Substituting `z = 1/3`: `sin(π/3) = √3/2`, so `Γ(1/3)Γ(2/3) = π/(√3/2) = 2π/√3 ≈ 3.6276`. This is the standard route to products of Gamma values at complementary rational arguments.
> **Key point:** `Γ(z)Γ(1−z) = π/sin(πz)`; at `z = 1/2` it gives `Γ(1/2)² = π` and at `z = 1/3`, `2π/√3`.

### Q69. `GATE-1` The residue of `π/sin(πz)` at `z = −2` is

> **Type:** MCQ
> **Answer:** `1` (Option a).
>
> (a) `1`
> (b) `-1`
> (c) `1/π`
> (d) `-1/π`
>
> **Solution:** The zeros of `sin(πz)` are exactly the integers `n`, and since `d/dz\sin(\pi z) = \pi\cos(\pi z)` takes the values `π(−1)^n \ne 0` there, every zero is simple. The residue is the numerator divided by the derivative of the denominator at the pole: `Res(\pi/\sin\pi z, n) = \pi/(\pi\cos \pi n) = 1/((-1)^n) = (-1)^n`. At `n = -2` this is `(−1)^{−2} = 1`. The general formula `(−1)^n` is positive at the even integers and negative at the odd ones, so options (a) and (b) are the only plausible values and parity alone decides between them; the `1/π` distractors forget the leading `π` in the numerator.
> **Key point:** `Res(\pi/\sin\pi z, n) = \pi/(\pi\cos \pi n) = (-1)^n`, which equals 1 at the even integers, so at `z = -2` the residue is 1.

### Q70. State Legendre's duplication formula for the Gamma function, and use it to find `Γ(3/2)`.

> **Type:** Numerical
> **Answer:** `Γ(z)Γ(z + 1/2) = 2^{1−2z}√π·Γ(2z)`; at `z = 1/2` it gives `Γ(1/2)Γ(1) = √π·Γ(1)`, confirming `Γ(1/2) = √π`; using the recurrence gives `Γ(3/2) = (1/2)Γ(1/2) = √π/2 ≈ 0.8862`.
> **Solution:** The duplication formula is `Γ(z)Γ(z + 1/2) = 2^{1−2z}√π Γ(2z)`. Setting `z = 1/2` gives `Γ(1/2)Γ(1) = 2^0√π·Γ(1)`, i.e. `Γ(1/2) = √π` ✓. Setting `z = 1` gives `Γ(1)Γ(3/2) = 2^{−1}√π Γ(2)`, so `(√π/2) = (1/2)√π·1` ✓, which is consistent. To actually *evaluate* `Γ(3/2)` use the recurrence: `Γ(3/2) = (1/2)Γ(1/2) = (1/2)√π = √π/2 ≈ 0.8862`. The formula at `z = 1` is a consistency check, not an independent route, since it also contains `Γ(3/2)` on the left.
> **Key point:** `Γ(z)Γ(z+1/2) = 2^{1−2z}√π Γ(2z)`; the simplest way to get `Γ(3/2)` is the recurrence, not duplication.

### Q71. State Stirling's approximation for `Γ(n+1)`, and estimate `Γ(11) = 10!`.

> **Type:** Numerical
> **Answer:** `Γ(n+1) ≈ √(2πn)·(n/e)ⁿ`; for `n = 10` it gives `3.59 × 10⁶`, about 1.0% below the exact `10! = 3.6288 × 10⁶`.
> **Solution:** Stirling's formula is `n! = Γ(n+1) ≈ √(2πn)(n/e)ⁿ`. With `n = 10`: `√(20π) = 7.9267` and `(10/e)¹⁰ = (3.67879)¹⁰`. Since `ln 3.67879 = 1.30259`, the tenth power is `e^{13.0259} = 4.5313 × 10⁵`, and the product is `7.9267 × 4.5313 × 10⁵ = 3.5921 × 10⁶`. The exact value is `3628800 = 3.6288 × 10⁶`, so the relative error is `(3.6288 − 3.5921)/3.6288 ≈ 1.01%`, which is the expected `1/(12n) = 0.83%`-scale error. A first correction `(1 + 1/(12n))` multiplies the estimate by 1.00833.
> **Key point:** `n! ≈ √(2πn)(n/e)ⁿ` with relative error about `1/(12n)`; the complex version is `Γ(z) ≈ √(2π/z)(z/e)^z`.

### Q72. Define the Beta function and evaluate `B(1,1)` and `B(1/2, 1/2)`.

> **Type:** Numerical
> **Answer:** `B(m,n) = ∫_0^1 t^{m−1}(1−t)^{n−1}dt = Γ(m)Γ(n)/Γ(m+n)`; `B(1,1) = 1` and `B(1/2,1/2) = π`.
> **Solution:** With `m = n = 1` the integrand is `1`, so `B(1,1) = ∫_0^1 dt = 1`, and the Gamma form agrees: `Γ(1)Γ(1)/Γ(2) = 1·1/1 = 1` ✓. With `m = n = 1/2`, `B = Γ(1/2)²/Γ(1) = π/1 = π` ✓, and directly the integrand is `[t(1−t)]^{−1/2}`; with `t = sin²θ` it becomes `2dθ` and the integral is `2·(π/2) = π` ✓. Note `B(m,n) = B(n,m)`, a symmetry that is obvious in the integral and not in the Gamma product.
> **Key point:** `B(m,n) = Γ(m)Γ(n)/Γ(m+n)` and is symmetric: `B(m,n) = B(n,m)`.

### Q73. Define the error function `erf(z)` and state three of its properties, including its value at infinity.

> **Type:** Recall
> **Answer:** `erf(z) = (2/√π)∫_0^z e^{−t²}dt`; it is entire, odd (`erf(−z) = −erf(z)`), and `erf(∞) = 1`; also `erf(0) = 0`.
> **Solution:** The path of integration can be taken along any curve from 0 to `z` because `e^{−t²}` is entire and has a primitive, so the definition is path-independent and `erf` is itself entire. Oddness: substituting `t = −s` in `erf(−z)` gives `(2/√π)(−1)∫_0^z e^{−s²}ds = −erf(z)`. At infinity, `∫_0^∞ e^{−t²}dt = √π/2` (Q67), so `erf(∞) = (2/√π)(√π/2) = 1`. Consequently the complementary error function is `erfc(z) = 1 − erf(z)`, and `erf(1) ≈ 0.8427`, `erf(2) ≈ 0.9953`.
> **Key point:** `erf(z) = (2/√π)∫_0^z e^{−t²}dt` is entire because `e^{−t²}` is entire; `erf(∞) = 1`, `erf(−z) = −erf(z)`.

### Q74. Numerically evaluate `erf(0.5)`, `erf(1)` and `erf(2)`, and state what `erf(3)` is closest to.

> **Type:** Numerical
> **Answer:** `erf(0.5) \approx 0.5205`, `erf(1) \approx 0.8427`, `erf(2) \approx 0.9953`; `erf(3) \approx 0.99998`, indistinguishable from 1 to four figures.
> **Solution:** With `2/\sqrt\pi = 1.12838`, the Maclaurin series `erf(x) = 1.12838\sum_{n\ge0}(-1)^n x^{2n+1}/(n!(2n+1))` is efficient for small `x`. For `x = 0.5` the bracket is `0.5 - 0.125/3 + 0.03125/10 - 0.0078125/42 = 0.5 - 0.041667 + 0.003125 - 0.000186 = 0.461272`, giving `erf(0.5) = 1.12838 \times 0.461272 = 0.52050`. For `x = 1` the bracket is `1 - 1/3 + 1/10 - 1/42 + 1/216 - 1/1320 = 0.746824`, giving `erf(1) = 1.12838 \times 0.746824 = 0.84270`. For `x = 2` the series converges slowly, so the complementary form is better: `erfc(2) = 0.0046777`, giving `erf(2) = 1 - 0.0046777 = 0.99532`. For `x = 3` the tail is smaller still, `erfc(3) = 2.209 \times 10^{-5}`, so `erf(3) = 0.9999779`, which rounds to 1.0000 at four figures. The function rises steeply near the origin and saturates at 1, so beyond `x = 2` it is numerically almost indistinguishable from 1.
> **Key point:** `erf(0.5) \approx 0.5205`, `erf(1) \approx 0.8427`, `erf(2) \approx 0.9953` and `erf(3) \approx 0.99998`; the saturating tail is why `erfc(3) \approx 2.2\times10^{-5}`.

### Q75. Evaluate `∫_0^∞ e^{−t^2}dt` and `∫_{−∞}^{∞} e^{−t^2}dt`, and relate them to `Γ(1/2)`.

> **Type:** Numerical
> **Answer:** `∫_0^∞ e^{−t^2}dt = \sqrt\pi/2 \approx 0.8862`; `∫_{−∞}^{∞} e^{−t^2}dt = \sqrt\pi \approx 1.7725`; the two-sided integral equals `Γ(1/2)` and the one-sided integral equals `Γ(1/2)/2`.
> **Solution:** The defining integral `Γ(1/2) = ∫_0^∞ t^{-1/2}e^{-t}dt` is converted to a Gaussian by the substitution `t = s^2`, for which `dt = 2s\,ds` and `t^{-1/2} = 1/s`, so `Γ(1/2) = ∫_0^∞ (1/s)e^{-s^2}2s\,ds = 2∫_0^∞ e^{-s^2}ds`. Hence `∫_0^∞ e^{-s^2}ds = \sqrt\pi/2 \approx 0.8862`, and since `e^{-t^2}` is even the two-sided integral is twice this, `√\pi \approx 1.7725`. Rescaling by `t = x/\sqrt2` then gives `∫_{−∞}^{∞} e^{-x^2/2}dx = \sqrt{2\pi} \approx 2.5066`, which is the normalisation of the standard normal density `(1/\sqrt{2\pi})e^{-x^2/2}`; the extra factor of `√2` in the exponent is exactly what turns `√\pi` into `√{2\pi}`.
> **Key point:** `t = s^2` in `Γ(1/2)` gives `2∫_0^∞ e^{-s^2}ds`, so `∫_0^∞ e^{-t^2}dt = \sqrt\pi/2` and the two-sided Gaussian is `√\pi`, while the normal density is normalised by `√{2\pi}`.

### Q76. The function `1/(1 − z)` is analytic for `|z| < 1`. What is its power series there, and what happens to the series at `z = 1` and at `z = −1`?

> **Type:** Numerical
> **Answer:** `1/(1−z) = Σ_{n=0}^∞ z^n` for `|z| < 1`; at `z = 1` the series `Σ 1` diverges and at `z = −1` it is `1 − 1 + 1 − 1 + 1 − 1`, whose partial sums never settle, so it diverges as well (oscillates, no limit).
> **Solution:** The geometric series `Σ_{n=0}^∞ z^n` converges iff `|z| < 1`, to `1/(1−z)`. At `z = 1` the terms do not even tend to zero (`z^n = 1`), so the series diverges — and indeed `1/(1−z)` has a pole at `z = 1` anyway. At `z = −1` the partial sums alternate `1, 0, 1, 0, 1, 0` and have no limit, so the series diverges, while `1/(1−(−1)) = 1/2` is perfectly finite — a reminder that a series expansion can fail at a point where the function itself is perfectly well behaved, and that the radius of convergence is limited by the nearest singularity, here `z = 1` at distance 1 from the centre `z = 0`.
> **Key point:** `Σ z^n = 1/(1−z)` for `|z| < 1` only; it diverges at `z = ±1` although the function is fine at `z = −1`.

### Q77. Sum the two-sided series `Σ_{n=−∞}^{∞} (1/2)^{|n|} e^{inθ}` for real `θ` by adding two one-sided geometric series, and check the result at `θ = 0` and `θ = π`.

> **Type:** Numerical
> **Answer:** `3/(5 − 4cos θ)`.
> **Solution:** Put `z = e^{iθ}` (so `|z| = 1`) and split at `n = 0`: `Σ_{n=−∞}^{∞}(1/2)^{|n|}z^n = Σ_{n=0}^∞(z/2)^n + Σ_{n=1}^∞(1/(2z))^n`. Both converge absolutely since `|z/2| = |1/(2z)| = 1/2 < 1`, and they sum to `1/(1 − z/2) = 2/(2 − z)` and `(1/(2z))/(1 − 1/(2z)) = 1/(2z − 1)`. Over a common denominator, `[2(2z − 1) + (2 − z)]/((2 − z)(2z − 1)) = 3z/((2 − z)(2z − 1))`. On `|z| = 1` we have `2z − 1 = z(2 − z̄)`, so `|(2 − z)(2z − 1)|² = |2 − z|²·|2 − z̄|² = (5 − 4cos θ)²`, i.e. `|(2 − z)(2z − 1)| = 5 − 4cos θ`, and the numerator has modulus 3. The quotient is real (it equals its own conjugate on the unit circle), so the sum is `3/(5 − 4cos θ)`. Checks: at `θ = 0` the series is `1 + 2Σ_{k\ge1}2^{-k} = 1 + 2 = 3` and the formula gives `3/(5 − 4) = 3` ✓; at `θ = π` it is `1 + 2Σ_{k\ge1}(−1/2)^k = 1 + 2(−1/3) = 1/3` and the formula gives `3/(5 + 4) = 1/3` ✓. This is the Poisson kernel with parameter `r = 1/2`.
> **Key point:** `Σ_{n=−∞}^{∞} r^{|n|}e^{inθ} = (1 − r²)/(1 − 2r cos θ + r²)` — the Poisson kernel, obtained by adding two one-sided geometric series.

## Section 5. Power series, Taylor and Laurent expansions, analytic continuation

### Q78. Give two equivalent definitions of "`f` is analytic at `z₀`", and state the minimum hypothesis on the partial derivatives of `f = u + iv`.

> **Type:** Recall
> **Answer:** (i) `f` equals a convergent power series `f(z) = Σ aₙ(z − z₀)ⁿ` in some disc about `z₀`; (ii) `f` is complex differentiable **throughout** a neighbourhood of `z₀`, not merely at `z₀`. For `f = u + iv`, the Cauchy–Riemann equations together with the existence of the four partial derivatives (continuity is more than enough) are necessary and sufficient.
> **Solution:** The two conditions are equivalent by the existence theorem for power series. The crucial distinction is between differentiability *at* one point and analyticity in a *neighbourhood*: the function `f(z) = |z|²/z` for `z ≠ 0`, with `f(0) = 0`, is complex differentiable at `0` (since `|h|²/h = h̄ → 0`) yet is not analytic at any point. So merely possessing `f′(z₀)` does not make a function analytic there, and a Taylor series need not represent it.
> **Key point:** Analyticity at a point requires complex differentiability in a whole neighbourhood, not at one point.


### Q79. State the Taylor expansion of an analytic function about `z₀`, and explain how the radius of convergence is determined.

> **Type:** Theory
> **Answer:** `f(z) = Σ_{n=0}^∞ f^{(n)}(z₀)/n! · (z − z₀)ⁿ`, converging for `|z − z₀| < R`, where `R` is the distance from `z₀` to the **nearest singularity** of `f` (taken as `∞` if `f` is entire).
> **Solution:** Differentiating `f` repeatedly at `z₀` gives the coefficients, and analyticity guarantees the equality of function and series. The convergence disc is maximal: it stops exactly at the first point where the series representation breaks down, which is a singularity of `f`. This is why `1/(1−z)` expanded about `0` has `R = 1` (pole at `z = 1`), while the same function expanded about `z₀ = 2` also has `R = 1` (the same pole, now at distance 1).
> **Key point:** The radius of a Taylor series is the distance from the centre to the **nearest** singularity, not to the nearest zero.

### Q80. Find the Taylor series of `e^z` about `z₀ = 1` and state its radius of convergence.

> **Type:** Numerical
> **Answer:** `e^z = e·Σ_{n=0}^∞ (z − 1)ⁿ/n!`, with `R = ∞`.
> **Solution:** Write `z = 1 + (z − 1)`, so `e^z = e·e^{z−1} = e·Σ_{n=0}^∞(z − 1)ⁿ/n!`. Formally, `f^{(n)}(1) = e` for every `n`, so the Taylor coefficients are `e·1/n!`. Since `e^z` is entire there is no singularity anywhere, so `R = ∞`: the series converges for every complex `z`. Spot check: at `z = 1` it gives `e·1 = e` ✓; at `z = 0` it gives `e·Σ(−1)ⁿ/n! = e·e^{−1} = 1` ✓.
> **Key point:** An entire function's Taylor series about any centre has infinite radius of convergence.

### Q81. State the Cauchy–Hadamard formula for the radius of convergence of a power series, and apply it to `Σ zⁿ/n²`.

> **Type:** Numerical
> **Answer:** `1/R = limsup_{n→∞} |aₙ|^{1/n}`. For `Σ zⁿ/n²`, `(1/n²)^{1/n} = e^{−2ln n/n} → 1`, so `R = 1`.
> **Solution:** For a power series `Σ aₙ(z − z₀)ⁿ` the Cauchy–Hadamard formula is `1/R = limsup |aₙ|^{1/n}`. With `aₙ = 1/n²`, `|aₙ|^{1/n} = n^{−2/n}`, and since `ln(n^{−2/n}) = −2(ln n)/n → 0`, the limit is `e^0 = 1`, giving `R = 1`. This agrees with the singularity rule, since `Σ zⁿ/n²` converges to `Li₂(z)` whose nearest singularity is the branch point at `z = 1`.
> **Key point:** `1/R = limsup |aₙ|^{1/n}`; the `n`-th root kills any polynomial decay of `aₙ`, so `aₙ = 1/nᵏ` still gives `R = 1`.

### Q82. Find the Taylor series of `1/z` about `z₀ = 1`, state its domain of validity, and explain why it differs from the Laurent series at 0.

> **Type:** Numerical
> **Answer:** `1/z = Σ_{n=0}^∞ (−1)ⁿ(z − 1)ⁿ` for `|z − 1| < 1`; its domain of validity is the open disc of radius 1 about `z₀ = 1`, and it is a **Taylor** (power series in `z − 1` only) series there.
> **Solution:** `1/z = 1/(1 + (z − 1)) = 1/(1 + u)` with `u = z − 1`, and the geometric series gives `1/(1+u) = Σ_{n\ge0}(−1)ⁿuⁿ = 1 − u + u² − u³ + u⁴`, i.e. `1/z = 1 − (z−1) + (z−1)² − (z−1)³ + (z−1)⁴`, valid for `|u| < 1`. Check at `z = 2`: `1 − 1 + 1 − 1 + 1 − 1` does not converge, and `z = 2` is at distance 1, exactly the boundary ✓. The point `z = 0` lies at distance 1 from the centre `1` and is the singular point that caps the radius. The Laurent series of `1/z` about `0` is instead the single term `z^{−1}`, valid on `0 < |z| < ∞`; the two expansions use different centres and different annuli, and each is the correct one in its own region.
> **Key point:** A Taylor series about `z₀` has a **hole** of radius `R` at `z₀` only if `f` is singular there; for `1/z` about `z₀ = 1` there is no hole, the series is simply valid on `|z − 1| < 1`.

### Q83. Find the Taylor series of `1/(1 − z)` about the centre `z₀ = 2` and state its radius of convergence.

> **Type:** Numerical
> **Answer:** `1/(1−z) = −Σ_{n=0}^∞ (−1)ⁿ (z − 2)ⁿ` for `|z − 2| < 1`.
> **Solution:** With `z − 1 = (z − 2) + 1` we have `1/(1 − z) = −1/(z − 1) = −1/(1 + (z − 2))`, and the geometric series `1/(1 + u) = Σ_{n\ge0}(-1)ⁿuⁿ` for `|u| < 1` gives `1/(1 − z) = −Σ_{n\ge0}(-1)ⁿ(z − 2)ⁿ`, whose leading terms are `−1 + (z − 2) − (z − 2)² + (z − 2)³`. The condition `|z − 2| < 1` comes from `|u| < 1` with `u = z − 2`. The nearest singularity is the pole at `z = 1`, at distance 1 from `z₀ = 2`, so the radius is `R = 1` ✓. Checking at `z = 2` the series gives `−1` and `1/(1 − 2) = −1` ✓, and at `z = 1.5` it gives `−1 + (−0.5) − 0.25 = −1.75`, matching `1/(1 − 1.5) = −2` to the accuracy of the first few terms. The general pattern is `1/(1 − z) = −(1/(z₀ − 1))·Σ_{n\ge0}(−(z − z₀)/(z₀ − 1))ⁿ`, so the prefactor and the ratio both depend on the centre.
> **Key point:** Expanding about a new centre changes the series completely: here the prefactor is `−1`, the ratio is `−(z − 2)`, and the radius is the distance 1 from `z₀ = 2` to the pole at `z = 1`.

### Q84. State the radii of convergence of the Taylor series of `1/(z² − 4)` about `z₀ = 0` and about `z₀ = 3`.

> **Type:** Numerical
> **Answer:** About `z₀ = 0`: `R = 2`. About `z₀ = 3`: `R = 1`.
> **Solution:** `1/(z² − 4) = 1/((z−2)(z+2))` has simple poles at `z = 2` and `z = −2`. About the origin both are at distance 2, so `R = 2`. About `z₀ = 3` the nearest pole is `z = 2`, at distance 1, so `R = 1` (the other pole `z = −2` is at distance 5 and is irrelevant). The disc `|z − 3| < 1` touches `z = 4` on its boundary, which is regular — showing again that the boundary of the disc of convergence need not consist of singularities.
> **Key point:** Only the **nearest** singularity matters; for `1/(z²−4)` the radii about 0 and 3 are 2 and 1 respectively.

### Q85. Use the ratio test on the power series for `e^z` to find its radius of convergence, and state the general ratio-test formula.

> **Type:** Numerical
> **Answer:** `R = ∞`; in general for `Σ aₙ(z − z₀)ⁿ`, `R = lim_{n→∞} |aₙ/aₙ₊₁|`.
> **Solution:** For `Σ (z − z₀)ⁿ/n!`, the ratio of successive term magnitudes is `|aₙ/aₙ₊₁| = 1/(1/(n+1)) = n + 1`. The series converges for `|z − z₀| < lim(n+1) = ∞`, i.e. everywhere, confirming that `e^z` is entire. The general ratio-test form `R = lim|aₙ/aₙ₊₁|` is valid whenever that limit exists; when it does not, Cauchy–Hadamard (Q81) is the safe statement. Note the trap: `Σ n!zⁿ` has `|aₙ/aₙ₊₁| = 1/(n+1) → 0`, so it converges **only** at `z = 0`.
> **Key point:** `R = lim|aₙ/aₙ₊₁|`; for `1/n!` this is `∞` (entire), for `n!` it is `0` (converges only at the centre).

### Q86. `GATE-1` The radius of convergence of the power series `Σ_{n=0}^∞ zⁿ/n!` is

> **Type:** MCQ
> **Answer:** `∞` (Option d).
>
> (a) `1`
> (b) `0`
> (c) `2`
> (d) `∞`
>
> **Solution:** By the ratio test, `|aₙ/aₙ₊₁| = n + 1 → ∞`, so the series converges for every `z`; the sum is `e^z`, which is entire. Option (a) is the trap of confusing the series with the geometric series `Σ zⁿ`, whose radius is 1; option (b) is the trap of confusing it with `Σ n!zⁿ`, whose radius is 0. The factorial in the denominator grows so much faster than any geometric factor that it beats `|z|ⁿ` for every finite `|z|`.
> **Key point:** `Σ zⁿ/n!` has infinite radius; `Σ zⁿ` has radius 1; `Σ n!zⁿ` has radius 0.

### Q87. `GATE-1` The series `Σ_{n=0}^∞ z^{2ⁿ}` (with unit coefficients) has, on the circle `|z| = 1`,

> **Type:** MCQ
> **Answer:** Infinitely many singular points — the whole unit circle is a natural boundary (Option c).
>
> (a) exactly one singular point
> (b) exactly two singular points
> (c) infinitely many singular points (the entire circle)
> (d) no singular points
>
> **Solution:** This is a Hadamard gap series: the exponents `2ⁿ` satisfy `2^{n+1}/2ⁿ = 2 > 1`, so by the gap theorem the unit circle is a natural boundary, meaning the function cannot be analytically continued across **any** point of `|z| = 1`. Every point of that circle is therefore a singularity. Option (a) is the trap of thinking only `z = 1` is special; option (d) is the trap of assuming a convergent power series must be nice on its boundary. The contrast with `Σ zⁿ/2ⁿ` (radius 2, no singularity on `|z| = 1`) is the point: the gap, not the boundary, forces the pathology.
> **Key point:** `Σ z^{2ⁿ}` has the unit circle as a natural boundary — every point of `|z| = 1` is singular.

### Q88. State the binomial series for `(1 + z)^α` and give its first four terms for `α = 1/2`.

> **Type:** Numerical
> **Answer:** `(1 + z)^α = Σ_{n=0}^∞ C(α,n)zⁿ` with `C(α,n) = α(α−1)···(α−n+1)/n!`, valid for `|z| < 1`. For `α = 1/2`: `1 + z/2 − z²/8 + z³/16 − 5z⁴/128 + 7z⁵/256` and so on.
> **Solution:** The series is obtained by Taylor expansion about `z = 0`; the nearest branch point of `(1+z)^α` is at `z = −1`, so `R = 1`. The coefficients for `α = 1/2` are `C(1/2,0) = 1`, `C(1/2,1) = 1/2`, `C(1/2,2) = (1/2)(−1/2)/2 = −1/8`, `C(1/2,3) = (1/2)(−1/2)(−3/2)/6 = 1/16`, `C(1/2,4) = (1/2)(−1/2)(−3/2)(−5/2)/24 = −5/128`. Check: at `z = 0.1` the series gives `1 + 0.05 − 0.00125 + 0.0000625 = 1.0488`, and `√1.1 = 1.0488` ✓. When `α` is a non-negative integer the series terminates and is valid for all `z`.
> **Key point:** `(1 + z)^{1/2} = 1 + z/2 − z²/8 + z³/16 − 5z⁴/128 + 7z⁵/256` and so on, for `|z| < 1`; it terminates only for integer `α`.

### Q89. `GATE-2` `NAT` The radius of convergence of the power series `Σ_{n=1}^∞ zⁿ/(n·2ⁿ)` is

> **Type:** MCQ
> **Answer:** `2` (Option b).
>
> (a) `1`
> (b) `2`
> (c) `1/2`
> (d) `∞`
>
> **Solution:** By the ratio test, `|aₙ/aₙ₊₁| = [(n+1)2^{n+1}]/[n·2ⁿ] = 2(n+1)/n → 2`, so `R = 2`. Equivalently by Cauchy–Hadamard, `(1/(n2ⁿ))^{1/n} = n^{−1/n}/2 → 1/2`, giving `R = 1/(1/2) = 2` ✓. The series sums to `−ln(1 − z/2)`, whose nearest singularity is the logarithmic branch point at `z = 2`, exactly 2 units from the origin. Option (a) is the trap of forgetting the `2ⁿ`; option (c) is the trap of reading the answer as the ratio instead of its reciprocal.
> **Key point:** The `2ⁿ` in the denominator doubles the radius: `Σ zⁿ/(n2ⁿ)` has `R = 2` and sums to `−ln(1 − z/2)`.

### Q90. Compare the radii of convergence of `Σ zⁿ`, `Σ zⁿ/n!`, `Σ zⁿ/n` and `Σ n!zⁿ`.

> **Type:** Comparison
> **Answer:** `R = 1`, `∞`, `1` and `0` respectively.
> **Solution:** For `Σ zⁿ` the ratio test gives `R = 1`. For `Σ zⁿ/n!` it gives `n + 1 → ∞`, so `R = ∞`. For `Σ zⁿ/n` it gives `(n+1)/n → 1`, so `R = 1` — the factor `1/n` decays far too slowly to change anything, because `n`-th roots of any polynomial in `n` tend to 1. For `Σ n!zⁿ` the ratio is `1/(n+1) → 0`, so `R = 0` and the series converges only at `z = 0`. The lesson: only **exponential** behaviour of `aₙ` changes the radius.
> **Key point:** Only exponential growth or decay of `aₙ` changes the radius; `1/nᵏ` leaves `R = 1` unchanged, while `n!` collapses it to 0.

### Q91. Discuss the behaviour on the boundary of the disc of convergence: does the Taylor series of `1/(1 − z)` about 0 converge at any point of `|z| = 1`?

> **Type:** Conceptual
> **Answer:** No — it diverges at every point of `|z| = 1`, even though `1/(1 − z)` is finite at every point of that circle except `z = 1`.
> **Solution:** The series is `Σ zⁿ`. On `|z| = 1` the terms satisfy `|zⁿ| = 1`, so the term test for convergence fails outright: the terms do not tend to zero. So the series diverges everywhere on the boundary. Yet `1/(1−z)` is a perfectly ordinary finite function at, say, `z = −1` (equal to `1/2`) and analytic in a neighbourhood of it. This shows the disc of convergence is the largest disc on which the **series** equals the function, and its boundary need not consist of singularities — it is limited by the nearest one, `z = 1`, and every other boundary point inherits the failure of convergence without being singular.
> **Key point:** A power series always diverges on the circle where a *single* nearest singularity lies, even at the regular points of that circle.

### Q92. Define a Laurent series, and state what determines its annulus of convergence and its uniqueness.

> **Type:** Recall
> **Answer:** `f(z) = Σ_{n=−∞}^{∞} aₙ(z − z₀)ⁿ` with `aₙ = (1/2πi)∮_C f(ζ)/(ζ − z₀)^{n+1}dζ`, where `C` is any contour about `z₀` lying in the annulus. It converges absolutely and uniformly on compact sub-annuli `r < |z − z₀| < R`, with the annulus bounded by the nearest singularities inside and the nearest outside.
> **Solution:** The two positive and negative parts are separate geometric-type series in `z − z₀` and in `1/(z − z₀)`, so the inner radius is set by the largest inner singularity and the outer radius by the smallest outer one. A given analytic function has **one and only one** Laurent expansion about `z₀` in each annulus of convergence — the coefficients are given by the contour-integral formula above, which is independent of the choice of `C` within the annulus. Different annuli, however, give genuinely different expansions (Q93).
> **Key point:** Laurent expansion is unique **within each annulus**; the same function has different Laurent series in different annuli.

### Q93. Find both Laurent expansions of `1/(z − 1)` about the origin, one valid for `|z| < 1` and one for `|z| > 1`.

> **Type:** Numerical
> **Answer:** For `0 ≤ |z| < 1`: `−Σ_{n=0}^∞ zⁿ`, whose leading terms are `−1 − z − z² − z³ − z⁴`. For `|z| > 1`: `Σ_{n=0}^∞ z^{−n−1}`, whose leading terms are `z^{−1} + z^{−2} + z^{−3} + z^{−4}`.
> **Solution:** Inside: `1/(z − 1) = −1/(1 − z) = −Σ_{n≥0} zⁿ`, which converges for `|z| < 1` ✓. Outside: `1/(z − 1) = (1/z)·1/(1 − 1/z) = (1/z)Σ_{n≥0}z^{−n}`, which converges for `|1/z| < 1`, i.e. `|z| > 1` ✓. The two expansions look completely different yet both equal the same function in their own annulus — the classic demonstration that Laurent coefficients depend on the annulus. Note the outer expansion has **no** pole term `1/(z−1)` in finite powers of `z`; the pole is at `z = 1`, outside its annulus, and shows up as the `z^{−1}` coefficient of the outer series being 1.
> **Key point:** `1/(z−1) = −Σ zⁿ` for `|z| < 1` but `= Σ z^{−n−1}` for `|z| > 1` — different annuli, different Laurent series.

### Q94. Find the two Laurent expansions of `1/(z(z − 1))` about the origin, valid for `0 < |z| < 1` and for `|z| > 1`.

> **Type:** Numerical
> **Answer:** For `0 < |z| < 1`: `−Σ_{n=0}^∞ z^{n−1}`, whose leading terms are `−(z^{−1} + 1 + z + z² + z³)`. For `|z| > 1`: `Σ_{n=0}^∞ z^{−n−2}`, whose leading terms are `z^{−2} + z^{−3} + z^{−4}`.
> **Solution:** Inside: `1/(z(z−1)) = −(1/z)·1/(1 − z) = −(1/z)Σ_{n≥0}zⁿ = −(z^{−1} + 1 + z + z² + z³)`, converging for `0 < |z| < 1` — the inner radius is 0 because `z = 0` is a pole, so the annulus excludes the origin but has no positive inner bound. Outside: `1/(z(z−1)) = z^{−2}·1/(1 − 1/z) = z^{−2}Σ_{n≥0}z^{−n}`, converging for `|z| > 1` ✓. Reading off the `z^{−1}` coefficients: the inner expansion gives `a_{−1} = −1`, the outer gives `a_{−1} = 0`, exactly as it must — a contour `|z| = r` with `r < 1` encircles the pole at 0 but not at 1, while a contour with `r > 1` encircles both and the residues cancel.
> **Key point:** The `z^{−1}` coefficient of a Laurent series equals the residue, and it changes with the annulus whenever the contour crosses a pole.

### Q95. Find the two Laurent expansions of `1/(z²(z − 1))` about the origin, valid for `|z| < 1` and for `|z| > 1`.

> **Type:** Numerical
> **Answer:** For `0 < |z| < 1`: `−Σ_{n=0}^∞ z^{n−2} = −z^{−2} − z^{−1} − 1 − z − z^2`, and for `|z| > 1`: `Σ_{n=0}^∞ z^{−n−3} = z^{−3} + z^{−4} + z^{−5} + z^{−6}`.
> **Solution:** **Inside**, factor out the pole at the centre: `1/(z²(z−1)) = −z^{−2}·1/(1 − z) = −z^{−2}Σ_{n\ge0}zⁿ`, which converges when `|z| < 1` and is valid on the annulus `0 < |z| < 1` since `z = 0` is itself a pole. **Outside**, factor the power of `z` from the dominant factor: `1/(z²(z−1)) = z^{−3}·1/(1 − 1/z) = z^{−3}Σ_{n\ge0}z^{−n}`, which converges when `|z| > 1`. The inner expansion carries both a double-pole term `−z^{−2}` and a simple-pole term `−z^{−1}`, reflecting the pole of order 2 at `z = 0`, while the outer expansion has no negative powers below `z^{−3}` because the only singularity of the function lies at `z = 0`, which is outside its annulus. Note that the residue at 0 read off the inner expansion is `−1`, the coefficient of `z^{−1}`, whereas the outer expansion has no `z^{−1}` term at all; the two are not in conflict, since a Laurent coefficient is fixed only once the annulus of validity is specified, and for a pole at the centre the residue is the one delivered by the inner annulus.
> **Key point:** `1/(z²(z−1))` expands as `−z^{−2}Σ zⁿ` on `0 < |z| < 1` and as `z^{−3}Σ z^{−n}` on `|z| > 1`; a Laurent coefficient depends on the annulus.

### Q96. `GATE-2` `NAT` Find the Taylor series of `1/z` about the point `z₀ = 2`, and state the interval/disc on which it is valid.

> **Type:** MCQ
> **Answer:** `1/z = Σ_{n=0}^∞ (−1)ⁿ(z − 2)ⁿ/2^{n+1}`, valid for `|z − 2| < 2` (Option a).
>
> (a) `|z − 2| < 2`
> (b) `|z − 2| < 1`
> (c) `|z| < 2`
> (d) `|z| < 1`
>
> **Solution:** `1/z = 1/(2 + (z−2)) = (1/2)·1/(1 + (z−2)/2) = (1/2)Σ_{n=0}^∞[−(z−2)/2]ⁿ = Σ_{n=0}^∞(−1)ⁿ(z−2)ⁿ/2^{n+1}`. Convergence requires `|(z−2)/2| < 1`, i.e. `|z − 2| < 2` ✓. This matches the singularity rule: the only pole of `1/z` is at `z = 0`, at distance 2 from the centre 2. Check at `z = 2`: the series gives `1/2` ✓; at `z = 1` (distance 1): `Σ(−1)ⁿ(−1)ⁿ/2^{n+1} = Σ 1/2^{n+1} = 1` ✓. Option (b) is the trap of copying the answer for centre `z₀ = 1` from Q82; option (c) is the trap of confusing "distance from centre" with "distance from origin".
> **Key point:** Expanding `1/z` about `z₀` gives radius `|z₀|`; about 1 the radius is 1, about 2 it is 2.

### Q97. State the identity theorem for analytic functions and give a one-line application.

> **Type:** Theory
> **Answer:** If `f` and `g` are analytic on a connected open set `D` and `f(zₙ) = g(zₙ)` for a sequence `zₙ ∈ D` with `zₙ → z₀ ∈ D`, then `f ≡ g` on `D`. Equivalently, an analytic function is determined by its values on any set having a limit point inside `D`.
> **Solution:** The proof uses the fact that a power series vanishing at a point of convergence vanishes identically: `h = f − g` is analytic, `h(zₙ) = 0` makes `z₀` a limit point of its zeros, and then all Taylor coefficients of `h` at `z₀` vanish by repeated division by `(z − z₀)`, so `h ≡ 0` on the component. Application: if a rational function equals zero for infinitely many `z` accumulating at an interior point, its numerator polynomial is identically zero.
> **Key point:** Analytic functions are rigid — matching on a set with an interior limit point forces matching everywhere on the connected domain.

### Q98. Derive the Taylor series `log(1 + z) = Σ_{n=1}^∞ (−1)^{n+1} zⁿ/n` for `|z| < 1` by integrating a geometric series.

> **Type:** Numerical
> **Answer:** `log(1 + z) = z − z²/2 + z³/3 − z⁴/4 + z⁵/5` for `|z| < 1`, equal to 0 at `z = 0`, and divergent at both `z = 1` and `z = −1`.
> **Solution:** The geometric series gives `1/(1 + z) = 1 − z + z² − z³ + z⁴` and so on, for `|z| < 1`. Since `d/dz\log(1 + z) = 1/(1 + z)` and the series converges uniformly on compact subsets of the disc, term-by-term integration from 0 to `z` is legitimate: `log(1 + z) = ∫_0^z dt/(1+t) = Σ_{n\ge0}(-1)ⁿ z^{n+1}/(n+1) = Σ_{n\ge1}(-1)^{n+1}zⁿ/n`. At `z = 0.5` the first four terms give `0.5 − 0.125 + 0.041667 − 0.015625 = 0.401042`, which converges to `ln 1.5 = 0.405465` as more terms are added ✓. At `z = 1` the terms are `1/n` and give the harmonic series, which diverges. At `z = −1` the terms are `(−1)^{n+1}(−1)ⁿ/n = −1/n`, so the series diverges there too. The radius is 1 because the nearest singularity of `log(1 + z)` is the branch point at `z = −1`, one unit from the centre.
> **Key point:** Integrating `1/(1+z) = Σ(-z)ⁿ` term by term gives `log(1+z) = Σ_{n\ge1}(-1)^{n+1}zⁿ/n` with radius 1, set by the branch point at `z = −1`.

### Q99. `GATE-2` The Taylor series about `z₀ = 0` of `log(1 + z)` diverges at `z = 2`. Using a series about a different centre, evaluate `log 3` to four decimal places.

> **Type:** Numerical
> **Answer:** `log 3 ≈ 1.0986`.
> **Solution:** About `z₀ = 0` the radius is 1, so `z = 2` is outside. Expand about `z₀ = 1` instead: the nearest singularity of `log(1+z)` is the branch point at `z = −1`, at distance 2, so the series about 1 has radius 2 and does reach `z = 2`. Write `log(1+z) = log 2 + log(1 + (z−1)/2)` and use Q98 with `w = (z−1)/2`: at `z = 2`, `w = 1/2`, so `log 3 = log 2 + [1/2 − 1/8 + 1/24 − 1/64 + 1/160 − 1/384 + 1/896] = 0.69315 + 0.5 − 0.125 + 0.04167 − 0.01563 + 0.00625 = 1.10044`, and continuing, `− 1/(6·2⁶) = −0.00260` gives `1.09784`, `+1/(7·2⁷) = +0.00112` gives `1.09896`, `−1/(8·2⁸) = −0.00049` gives `1.09847`, converging to `1.0986` ✓, which is the known value of the natural logarithm of 3. The lesson: analytic continuation means writing a **new** series in a new variable, not extending the old one.
> **Key point:** To reach `z = 2` with `log(1+z)`, expand about `z₀ = 1` (radius 2) and substitute `w = (z−1)/2` into the standard series.

### Q100. `GATE-2` How does the value of `log z` depend on the path by which one continues it from `1` to `2` in the complex plane? Give the general form of the continued value.

> **Type:** Theory
> **Answer:** It depends only on the total winding number of the path about the origin: the continued value is `ln|z| + i(arg z + 2kπ) = ln 2 + 2kπi` at the endpoint, with `k` the winding number of the path. A path with no winding gives `ln 2`; one that loops once anticlockwise gives `ln 2 + 2πi`.
> **Solution:** Along a smooth path `γ` avoiding the origin, the differential `(1/z)dz` is exact on the universal cover, so a single-valued branch can be carried along `γ` by integrating `∫_γ dz/z` continuously. The imaginary part of this integral changes by `2π` per counterclockwise encirclement of `0` (the argument principle of Q19–Q21), which is exactly the `2π` jump in `arg z`. Since `0` is the only obstruction, two paths give the same value iff they are homotopic in `ℂ \ {0}`, i.e. iff they have the same winding number about 0. This is precisely why `log z` cannot be made single-valued on all of `ℂ \ {0}`.
> **Key point:** Continued values of `log z` differ by `2πi` per winding number; a single-valued branch exists only on a simply connected domain avoiding 0.

### Q101. Show by direct comparison that the Taylor series of `e^z` about `z₀ = 0` and about `z₀ = 1` represent the same function on their common disc, and identify the overlap.

> **Type:** Theory
> **Answer:** The series about 0, `Σ zⁿ/n!`, and the series about 1, `e·Σ(z−1)ⁿ/n!`, both equal `e^z`; their discs of convergence are `|z| < ∞` and `|z − 1| < ∞`, so the overlap is the whole plane and the agreement is global.
> **Solution:** The series about 0 sums to `e^z` because `n!` is the factorial of the Maclaurin series of the exponential. The series about 1 was shown in Q80 to be `e·e^{z−1} = e^z`, again identically. Since both radii are infinite, they agree on the entire plane, not just on a lens. This is the simplest illustration of the identity theorem (Q97): two different series, from two different centres, agree because both are analytic and agree on an open set. It also shows the general continuation recipe: to move a series from centre `z₀` to centre `z₁`, substitute `w = (z − z₁)/(z₀ − z₁)` into the old series, which is what Q99 did.
> **Key point:** Two Taylor series about different centres can both equal the same function; analytic continuation re-expands about a new centre rather than extending the old series.

### Q102. `GATE-2` What is the radius of convergence of the Taylor series of `1/(z² + 1)` about the point `z₀ = i`?

> **Type:** MCQ
> **Answer:** Zero — no Taylor series exists there, because the function is not analytic at `z₀ = i` (Option a).
>
> (a) `0` (no valid Taylor series, `f` is not analytic at the centre)
> (b) `1`
> (c) `2`
> (d) `∞`
>
> **Solution:** `1/(z² + 1) = 1/((z − i)(z + i))` has a **simple pole at the centre** `z₀ = i` itself. A Taylor series represents a function only where the function is analytic, so none exists about `z₀ = i` and the radius is effectively 0 — the limit definition of the radius would give `R = 0` since the function is singular at distance 0. Option (b) is the trap of taking the distance to the *other* pole `z = −i` (which is 2 away); option (d) is the trap of assuming rational functions are nice. The same function about `z₀ = 0` has radius 1, the distance to the nearer pole `i`.
> **Key point:** The radius of a Taylor series about `z₀` is the distance to the nearest singularity **including one at `z₀` itself**, in which case no Taylor series exists.

## Section 6. Cauchy–Riemann equations, harmonic functions and orthogonality

### Q103. State the Cauchy–Riemann equations for `f = u + iv`, and the two standard formulas for `f′(z)` in terms of `u` and `v`.

> **Type:** Recall
> **Answer:** `u_x = v_y` and `u_y = −v_x`. Consequently `f′(z) = u_x + i v_x = v_y − i u_y`.
> **Solution:** These are the necessary (and, with mild regularity, sufficient) conditions for a complex function to be complex differentiable. The first formula comes from approaching `z₀` along the real axis, the second from approaching along the imaginary axis; the two must agree, which is exactly the CR pair. Note the second formula carries a **minus** sign in front of `u_y`, which is the most commonly dropped sign in all of complex analysis.
> **Key point:** `u_x = v_y`, `u_y = −v_x`; then `f′ = u_x + i v_x = v_y − i u_y`.

### Q104. Derive the Cauchy–Riemann equations from the definition of the complex derivative.

> **Type:** Theory
> **Answer:** Taking the difference quotient along the real and along the imaginary direction forces `u_x = v_y` and `u_y = −v_x`, and then `f′(z) = u_x + i v_x = v_y − i u_y`.
> **Solution:** Suppose `f′(z₀)` exists, so that `(f(z₀ + h) − f(z₀))/h` has the same limit as `h \to 0` along every path. Along the real direction, `h = t` with `t` real, `f(z₀ + t) − f(z₀) = [u(x₀ + t, y₀) − u(x₀, y₀)] + i[v(x₀ + t, y₀) − v(x₀, y₀)]`, and dividing by `t` gives `u_x + i v_x` in the limit. Along the imaginary direction, `h = it` with `t` real, so `f(z₀ + it) − f(z₀) = [u(x₀, y₀ + t) − u(x₀, y₀)] + i[v(x₀, y₀ + t) − v(x₀, y₀)]`, and dividing by `it` gives `u_y/i + i v_y/i = −i u_y + v_y` in the limit. Equating the two limits, `u_x + i v_x = v_y − i u_y`, and matching real and imaginary parts yields `u_x = v_y` and `v_x = −u_y`, the Cauchy–Riemann equations. The second form of the derivative, `f′(z) = v_y − i u_y`, is therefore a consequence of the same calculation, and under the CR equations either partial pair gives the same value.
> **Key point:** Equating the difference quotient taken along the real axis, `u_x + i v_x`, with that taken along the imaginary axis, `v_y − i u_y`, **produces** `u_x = v_y` and `u_y = −v_x`.

### Q105. Find the harmonic conjugate of `u(x, y) = x² − y²` and the corresponding analytic function.

> **Type:** Numerical
> **Answer:** `v(x, y) = 2xy + constant`; the analytic function is `f(z) = z² + ic`.
> **Solution:** Integrate `u_x = v_y`: `u_x = 2x`, so `v = 2xy + g(y)`. Then `u_y = −2y` must equal `−v_x = −2y` ✓, which holds for **any** `g(y)`. Use the other equation `v_x = 2y = −u_y`; to fix `g`, use `u_y = −v_x` and `u_x = v_y` consistently: differentiating `v = 2xy + g(y)` gives `v_y = 2x + g′(y)`, and CR requires `v_y = u_x = 2x`, so `g′(y) = 0` and `g` is a constant. Hence `v = 2xy + c`, and `f = u + iv = x² − y² + 2ixy = (x + iy)² = z²` ✓.
> **Key point:** The harmonic conjugate is unique only up to an additive constant; the constant is the imaginary part of an arbitrary additive constant in `f`.

### Q106. Find the harmonic conjugate of `u(x, y) = 2xy` and the corresponding analytic function.

> **Type:** Numerical
> **Answer:** `v(x, y) = y² − x² + c`; the analytic function is `f(z) = −z² + ic`.
> **Solution:** From `v_x = −u_y = −2x`, integrate in `x`: `v = −x² + h(y)`. Then `v_y = h′(y)` must equal `u_x = 2y`, so `h(y) = y² + c`. Thus `v = y² − x² + c` and `f = 2xy + i(y² − x²) = −(x² − y²) + 2ixy = −(x + iy)² = −z²` ✓. Compare with Q105: there `u = Re(z²)`; here `u = Re(−z²)`, so the same real part pattern with a sign flip.
> **Key point:** `Re(−z²) = 2xy`; the same real part can come from `−z²` here and `z²` in Q105 because the *pair* (real, imaginary) parts swaps roles under negation.

### Q107. Verify that `f(z) = z²` is analytic and compute `f′(z)` two ways.

> **Type:** Numerical
> **Answer:** `f` is analytic with `f′(z) = 2z`.
> **Solution:** `z² = (x+iy)² = x² − y² + 2ixy`, so `u = x² − y²`, `v = 2xy`. Then `u_x = 2x` and `v_y = 2x` ✓; `u_y = −2y` and `−v_x = −2y` ✓. So CR hold, and `f′(z) = u_x + i v_x = 2x + 2iy = 2z` ✓. By the definition, `f′(z) = 2z` is confirmed since `d(z²)/dz = 2z`. Check by the limit: `(f(z+h) − f(z))/h = (2zh + h²)/h = 2z + h → 2z` ✓, valid for every `z`.
> **Key point:** Any polynomial is entire; `f′(z) = 2z` also follows from `u_x + i v_x`.

### Q108. Show that `f(z) = z̄²` is not analytic anywhere.

> **Type:** Theory
> **Answer:** CR fail everywhere; the Cauchy–Riemann equations give `−2y = 2x` only on the line `x = −y`, not on any open set.
> **Solution:** `z̄² = (x − iy)² = x² − y² − 2ixy`, so `u = x² − y²` and `v = −2xy`. Then `u_x = 2x` while `v_y = −2x`, so CR requires `2x = −2x`, i.e. `x = 0`. And `u_y = −2y` while `−v_x = 2y`, so CR requires `−2y = 2y`, i.e. `y = 0`. Both conditions cannot hold on any open set, so `f` is not analytic anywhere (the point `(0,0)` is not an interior point of a domain). By the definition, `(f(z+h) − f(z))/h = −2z̄ − h̄`, whose limit is `−2z̄`, which depends on the path, confirming non-differentiability at every point.
> **Key point:** `z̄²` is nowhere analytic; the only function that is both `z`-holomorphic and `z̄`-holomorphic is a constant.

### Q109. Show that `f(z) = |z|²` is not analytic, even though `|z|²` is a real polynomial in `x, y`.

> **Type:** Common-mistake
> **Answer:** `f` is complex differentiable only at the origin, where `f′(0) = 0`, and is nowhere analytic, so the CR equations fail at every point other than `0`.
> **Solution:** Write `u = x² + y²` and `v = 0`, so `u_x = 2x`, `u_y = 2y`, `v_x = v_y = 0`. The CR equations `u_x = v_y` and `u_y = −v_x` therefore require `2x = 0` and `2y = 0`, which hold only at the origin. At every other point the complex derivative does not exist at all. The origin deserves a separate look, since CR are necessary but not sufficient: there the difference quotient is `(f(h) − f(0))/h = |h|²/h = \bar h`, which tends to 0 along every path since `|\bar h| = |h| \to 0`, so `f′(0)` does exist and equals 0. Even so, analyticity at a point requires a neighbourhood of differentiability, and `f` fails at every neighbouring point, so `f` is not analytic anywhere. This is the sharpest illustration that "differentiable at one point" is not "analytic": smoothness in the real variables guarantees nothing.
> **Key point:** `|z|²` is differentiable only at `z = 0`, where `f′(0) = 0` because the quotient is `\bar h`; being differentiable at one point is not the same as being analytic.

### Q110. Show that if `f` is analytic and non-constant, then `|f|²` cannot be analytic, and say where the argument stops being informative for a constant `f`.

> **Type:** Theory
> **Answer:** If `|f|²` were analytic it would be real-valued and analytic, hence constant; then `|f|` would be constant, and the maximum-modulus principle forces `f` to be constant. So `|f|²` is analytic only when `f` is constant, and in that case the chain of implications simply terminates immediately instead of yielding a contradiction.
> **Solution:** Put `F = |f|² = f\bar f`. If `F` were analytic then, being real-valued, its imaginary part would be zero, and the CR equations would read `F_x = 0` and `F_y = 0`; hence `F` is a constant function. Since `F \ge 0`, this constant is `c^2` for some `c \ge 0`, and so `|f(z)| = c` everywhere. A non-constant analytic function cannot have constant modulus, since a maximum of `|f|` would then occur at an interior point and the maximum-modulus principle would force `f` to be constant. Contradiction completes the proof for non-constant `f`. The argument never breaks down; what changes for a constant `f` is that the first step lands on `F \equiv c^2`, a genuine constant function, which is analytic, and the maximum-modulus step applies to it harmlessly. The conclusion is then simply true rather than contradictory, so the proof is a valid one-way implication for every analytic `f` and is vacuous only in the sense that the hypothesis "non-constant" is what made the conclusion informative. The remark that `\bar f` is generally not analytic is a separate, shorter way of seeing why the product trick does not help.
> **Key point:** A real-valued analytic function is constant, so `|f|²` analytic would give `|f|` constant, forcing `f` to be constant by the maximum-modulus principle; for constant `f` the chain of implications is simply trivial.

### Q111. Prove that if `f = u + iv` is analytic then `u` and `v` are harmonic, i.e. `u_xx + u_yy = 0` and `v_xx + v_yy = 0`.

> **Type:** Theory
> **Answer:** CR plus a `C²` hypothesis force both Laplacians to vanish.
> **Solution:** With `u_x = v_y` and `u_y = −v_x` and continuous second partials, `u_xx + u_yy = (v_y)_x + (−v_x)_y = v_{yx} − v_{xy} = 0` ✓. Similarly `v_xx + v_yy = (−u_y)_x + (u_x)_y = −u_{yx} + u_{xy} = 0` ✓. Equivalently, using the formula `f′(z) = u_x + iv_x`, the fact that `f′` is itself analytic means its real and imaginary parts are harmonic, giving `u_x` and `v_x` harmonic, and CR then transfers this to `u` and `v`.
> **Key point:** Analytic ⟹ harmonic; the proof is one line of mixed-partial cancellation after CR.

### Q112. The converse of Q111 is false: harmonicity alone does not guarantee a global harmonic conjugate. State the condition on a domain `D` under which every harmonic function on `D` does have a single-valued conjugate, and give the reason.

> **Type:** Common-mistake
> **Answer:** `u_xx + u_yy = 2 + 2 = 4 ≠ 0`, so `u` is **not** harmonic and therefore cannot be the real part of an analytic function. This is a counterexample to "harmonic ⟹ analytic", i.e. harmonicity is necessary but not sufficient.
> **Solution:** For a genuine counterexample take `u = x² − y²`, which *is* harmonic (`u_xx + u_yy = 2 − 2 = 0`) and does have the conjugate `v = 2xy`. But `x² + y²` has Laplacian 4, so it is not harmonic at all, and the "converse fails" statement should be made with a correct example: `u = x² − y²` extended by `v = 2xy` works, whereas `u = x` is harmonic and its conjugate `v = −y` is forced by `v_y = u_x = 1`, `v_x = −u_y = 0`, so `v = y + c`; check `v_y = 1 = u_x` ✓ and `−v_x = 0 = u_y` ✓, so `f(z) = x + i(y + c) = z + ic` ✓ analytic. So the correct example of a harmonic function with no conjugate is `u = ln(x² + y²)`, harmonic away from the origin, whose conjugate `v = 2 arg z` is multivalued (Q117).
> **Key point:** Harmonicity is **necessary** but not sufficient for a harmonic conjugate to exist globally; the obstruction is a non-vanishing circulation (multivaluedness), as in `ln|z|`.

### Q113. Expand `f(z) = z⁴` in the form `u + iv` and verify CR and harmonicity.

> **Type:** Numerical
> **Answer:** `u = x⁴ − 6x²y² + y⁴` and `v = 4x³y − 4xy³`; `f′(z) = 4z³`.
> **Solution:** Binomially, `(x+iy)⁴ = x⁴ + 4x³(iy) + 6x²(iy)² + 4x(iy)³ + (iy)⁴ = x⁴ + 4ix³y − 6x²y² − 4ixy³ + y⁴`. CR checks: `u_x = 4x³ − 12xy²` and `v_y = 4x³ − 12xy²` ✓; `u_y = −12x²y + 4y³` and `−v_x = −(12x²y − 4y³) = −12x²y + 4y³` ✓. Harmonicity: `u_xx = 12x² − 12y²` and `u_yy = −12x² + 12y²`, sum 0 ✓; `v_xx = 24xy` and `v_yy = −24xy`, sum 0 ✓. The derivative is `4z³`; reading it off from `u_x + iv_x = (4x³ − 12xy²) + i(12x²y − 4y³) = 4(x³ − 3xy²) + 12i(x²y) − 4iy³ = 4(x + iy)³` ✓.
> **Key point:** The real and imaginary parts of `zⁿ` are both harmonic — the classical examples of harmonic functions on the whole plane.

### Q114. Prove that the level curves of `u` and of `v` are orthogonal wherever `f = u + iv` is analytic and `f′(z) ≠ 0`.

> **Type:** Theory
> **Answer:** `∇u · ∇v = u_x v_x + u_y v_y = v_y v_x − v_x v_y = 0`, so the two families of level curves meet at right angles.
> **Solution:** Along a level curve of `u`, `u` is constant, so the curve is perpendicular to `∇u`; similarly a level curve of `v` is perpendicular to `∇v`. If the gradients are orthogonal, the level curves are too. Using CR, `u_x v_x + u_y v_y = v_y·v_x + (−v_x)·v_y = 0` ✓. The hypothesis `f′(z) ≠ 0` is needed to ensure the gradients are non-zero: `|∇u|² = |∇v|² = |f′(z)|²`, so a critical point of `f` is a common singular point of both families.
> **Key point:** Level curves of `u` and `v` are orthogonal wherever `f′ ≠ 0`; the singular sets of the two harmonic functions coincide with the critical points of `f`.

### Q115. With `f(z) = e^z`, write `u` and `v`, show that the level curves of `u` and of `v` meet orthogonally, and identify a pair of level-curve families that are straight lines.

> **Type:** Conceptual
> **Answer:** `u = e^x cos y` and `v = e^x sin y`; the gradients `(e^x cos y, −e^x sin y)` and `(e^x sin y, e^x cos y)` have zero dot product, so the level curves are orthogonal. The straight-line families are `|f| = e^x` (the vertical lines `x = const`) and `arg f = y` (the horizontal lines `y = const`).
> **Solution:** Writing `z = x + iy` gives `e^z = e^x(\cos y + i\sin y)`, so `u = e^x\cos y` and `v = e^x\sin y`. The gradients in the plane are `∇u = (e^x\cos y, −e^x\sin y)` and `∇v = (e^x\sin y, e^x\cos y)`, and `∇u \cdot ∇v = e^{2x}(\cos y\sin y − \sin y\cos y) = 0` everywhere, so the two families of level curves are orthogonal wherever the gradients are nonzero, that is wherever `e^z \ne 0`, which is everywhere. Also `|∇u|² = |∇v|² = e^{2x} = |f′(z)|²`, since `f′(z) = e^z \ne 0`, and the non-vanishing of `f′` is the general reason level curves of `u` and `v` stay perpendicular. The level curves of `u` and `v` themselves are transcendental, `x = \ln|c/\cos y|` and `x = \ln|d/\sin y|`; the straight-line families are instead those of the modulus and the argument, `|f| = e^x`, giving vertical lines, and `arg f = y`, giving horizontal lines, and those two do cross at right angles.
> **Key point:** `∇u \cdot ∇v = 0` because `|∇u|² = |∇v|² = |f′|²` and the two gradients are perpendicular; for `e^z` the straight-line level families are the vertical lines `|f| = e^x` and the horizontal lines `arg f = y`.

### Q116. For `f(z) = 1/(z − a)`, describe the level curves of `u` and of `v`, and state how the two families are related.

> **Type:** Conceptual
> **Answer:** Both families consist of circles through `a`; the `v = const` family and the `u = const` family are two circles of different radii through `a`, and every member of one family is orthogonal to every member of the other.
> **Solution:** Write `z − a = ρe^{iθ}`; then `1/(z − a) = ρ^{−1}e^{−iθ}`, so `u = cos θ/ρ` and `v = −sin θ/ρ`. Holding `v` constant: `sin θ/ρ = c`, i.e. `ρ = sin θ/c`; in Cartesian form this is a circle through the origin `a` — the equation of a circle through `a` is `ρ = 2R sin(θ − θ₀)`. Holding `u` constant gives `ρ = cos θ/c'`, again a circle through `a`. The two families are the two "orthogonal pencils" of circles through `a` and through its reflection in the real axis, corresponding exactly to the map `1/(z − a)` of the two pencils of straight lines (Q34). Since `f′(z) = −1/(z−a)² ≠ 0` for `z ≠ a`, Q114's orthogonality applies at every point except `a`.
> **Key point:** `1/(z − a)` maps the two orthogonal pencils of straight lines to two orthogonal pencils of circles through `a` — the standard conformal map onto a slit plane.

### Q117. Show that the harmonic conjugate of `u = ln|z|` is `v = arg z`, and explain why `u` has no **single-valued** harmonic conjugate on the annulus `1/2 < |z| < 2`.

> **Type:** Theory
> **Answer:** `v = arg z + c`; it is multivalued (`v` jumps by `2π` around a loop), so no single-valued conjugate exists on the annulus, which is not simply connected.
> **Solution:** In polar form `ln|z| = ln r` and the analytic function `log z = ln r + iθ` shows `v = θ = arg z` up to a constant. The obstruction: `∂v/∂x = −y/r²` and `∂v/∂y = x/r²` are single-valued, so `v` is a well-defined smooth function **locally**; the CR equations hold (`u_x = x/r² = v_y` ✓, `u_y = y/r² = −v_x` ✓). But a single-valued function cannot have its gradient equal to `∇θ` everywhere on a loop enclosing the origin, because `∮dθ = 2π ≠ 0` — the circulation is non-zero, which by the gradient theorem is impossible for the exact differential of a single-valued function. This is exactly the obstruction described in Q45 and Q100.
> **Key point:** `ln|z|` is harmonic off the origin but its conjugate `arg z` is multivalued; a non-zero circulation `∮d(arg z) = 2π` forbids a single-valued conjugate.

### Q118. Write `f(z) = 1/z = u + iv` explicitly in terms of `x, y`, and verify CR and harmonicity.

> **Type:** Numerical
> **Answer:** `u = x/(x² + y²)`, `v = −y/(x² + y²)`; both are harmonic for `(x, y) ≠ (0, 0)`.
> **Solution:** `1/z = z̄/|z|² = (x − iy)/(x² + y²)`, so with `r² = x² + y²`, `u = x/r²` and `v = −y/r²`. Then `u_x = (r² − 2x²)/r⁴ = (y² − x²)/r⁴`, and `v_y = −(r² − 2y²)/r⁴ = (y² − x²)/r⁴`, so `u_x = v_y` ✓. Also `u_y = −2xy/r⁴` and `v_x = +2xy/r⁴`, so `u_y = −v_x` ✓. Both CR equations hold. Harmonicity follows immediately from Q111 because `1/z` is analytic on `ℂ \ {0}`; explicitly `u_xx + u_yy = 0` can be confirmed from the explicit forms, whose derivatives share the same cubic structure in the numerator. The only singular point is `z = 0`, which is excluded from the domain, so `u` and `v` are harmonic on the punctured plane and nowhere else.
> **Key point:** `Re(1/z) = x/(x²+y²)` and `Im(1/z) = −y/(x²+y²)`; both are harmonic everywhere except at the origin.

### Q119. If `f` is analytic, is `F(z) = conj(f(conj z))` analytic? What is `F′(z)`?

> **Type:** Theory
> **Answer:** Yes — if `f` is entire (or analytic with domain stable under conjugation), `F` is analytic with `F′(z) = conj(f′(conj z))`.
> **Solution:** If `f(z) = Σ aₙzⁿ`, then `F(z) = conj(Σ aₙ(conj z)ⁿ) = Σ conj(aₙ)zⁿ`, which is again a power series, hence analytic, and the constant term is `conj(f(0))` ✓. For the derivative, `F′(z) = Σ n·conj(aₙ)z^{n−1} = conj(Σ n aₙ(conj z)^{n−1}) = conj(f′(conj z))` ✓. This "reflected" function is what appears when one complex-conjugates a solution of a PDE; note that the plain composition `f(conj z)` is generally **not** analytic (it is the anti-analytic function, holomorphic in `z̄`).
> **Key point:** `conj(f(conj z))` is analytic with derivative `conj(f′(conj z))`; `f(conj z)` alone is anti-analytic.

### Q120. `GATE-1` If `f` is analytic in a domain `D`, which of the following is analytic in the **same** domain?

> **Type:** MCQ
> **Answer:** `f(z)²` (Option d).
>
> (a) `conj(f(z))`
> (b) `|f(z)|`
> (c) `f(z)·conj(f(z))`
> (d) `f(z)²`
>
> **Solution:** Sums and products of analytic functions are analytic, so `f²` is analytic wherever `f` is ✓. `conj(f(z))` is analytic only if `f` is real-valued, hence constant. `|f| = √(f·conj f)` is analytic only in the trivial case `f` constant. `f·conj f = |f|²` is analytic only if `f` is constant (Q110). Option (a) is the trap of confusing `conj(f(z))` with `conj(f(conj z))`, which *is* analytic (Q119) — the conjugation must apply to the argument as well.
> **Key point:** Analytic functions are closed under `+`, `×` and powers, but not under complex conjugation of the value alone.

### Q121. `GATE-1` If `f = u + iv` is analytic with `f′(z) \ne 0`, which of the following is **not** harmonic?

> **Type:** MCQ
> **Answer:** `u²` (Option c).
>
> (a) `u`
> (b) `v`
> (c) `u^2`
> (d) `u·v`
>
> **Solution:** By Q111, `u` and `v` are both harmonic, so options (a) and (b) are out. For the product, `∇²(uv) = v∇²u + u∇²v + 2(∇u \cdot ∇v) = 0 + 0 + 0`, because CR give `∇u = (u_x, u_y) = (v_y, −v_x)`, so `∇u \cdot ∇v = v_y v_x − v_x v_y = 0`. Hence `u·v` **is** harmonic whenever `f` is analytic, whether or not `f′` vanishes, and option (d) is out. For the square, `∇²(u²) = 2(∇u \cdot ∇u) + 2u∇²u = 2|∇u|² = 2|f′(z)|²`, which is strictly positive wherever `f′(z) \ne 0`, so `u²` is not harmonic at any such point. As a check take `f(z) = z²`, where `u = x² − y²` and `u² = x⁴ − 2x²y² + y⁴`, and `∂²/∂x²` gives `12x² − 4y²` while `∂²/∂y²` gives `−4x² + 12y²`, summing to `8(x² + y²) = 2|2z|²`, as predicted. The hypothesis `f′ \ne 0` is exactly what rules out the vanishing.
> **Key point:** `∇²(uv) = 2∇u\cdot∇v = 0` always, so `u·v` is harmonic, but `∇²(u²) = 2|f′|² \ne 0`, so `u²` is not harmonic.

### Q122. `GATE-2` Show that for analytic `f`, `|∇u| = |∇v| = |f′(z)|` everywhere, and use it to locate the critical points of `f` without computing `f′`.

> **Type:** MCQ
> **Answer:** `|∇u|² = |∇v|² = |f′(z)|²`; the critical points are exactly the common zeros of `∇u` and `∇v` (Option b).
>
> (a) the points where `u = 0`
> (b) the points where both `∇u` and `∇v` vanish
> (c) the points where `|u| = |v|`
> (d) the points where `f = 0`
>
> **Solution:** `|f′|² = (u_x + iv_x)(u_x − iv_x) = u_x² + v_x² = v_y² + v_x² = v_x² + v_y² = |∇v|²`, using `u_x = v_y`; similarly `|∇u|² = u_x² + u_y² = v_y² + v_x²` ✓. So all three coincide. Therefore `f′(z₀) = 0` if and only if `∇u(z₀) = 0` **and** `∇v(z₀) = 0`. Example: for `f(z) = z⁴`, the level curves of `u` and `v` both degenerate at the origin, and indeed `f′(0) = 0`. Option (a) is the trap of confusing critical points with zeros of `f` — for `f(z) = z − 1`, `f′ = 1` never vanishes although `f(1) = 0`; option (d) is the classic confusion between zeros and critical points of a function.
> **Key point:** `|∇u| = |∇v| = |f′|`; critical points of `f` are common zeros of both gradients, and are **not** the zeros of `f`.

### Q123. `GATE-2` For `f(z) = z²`, so that `u = x² − y²` and `v = 2xy`, the level curve `u = 0` is the pair of lines `y = x` and `y = −x`. Which family of curves crosses these two lines at right angles, and what are its equations?

> **Type:** MCQ
> **Answer:** The level curves of `v`, namely the rectangular hyperbolas `2xy = c` (Option a).
>
> (a) the hyperbolas `2xy = c`
> (b) the circles `x² + y² = c`
> (c) the lines `x = 0` and `y = 0`
> (d) the hyperbolas `x² − y² = c`
>
> **Solution:** The level curves of `u` are the family `x² − y² = c`, and `u = 0` gives `x² = y²`, i.e. the two lines `y = ±x` ✓; these are the *asymptotes* of that family, so option (d) names the family whose asymptotes they are, not a family crossing them orthogonally. The level curves of `v` are `2xy = c`, and by Q114 these cross the level curves of `u` at right angles. Direct slope check: on `2xy = c` we have `y = c/(2x)`, so `dy/dx = −c/(2x²) = −y/x`; where this curve meets `y = x` the slope is `−1` while the line has slope `+1`, and the product `−1` means the two are perpendicular ✓. Likewise on `y = −x` the hyperbola's slope is `+1` against the line's `−1` ✓. Circles and the coordinate axes are level curves of neither part.
> **Key point:** For `f = z²`, `u = const` are hyperbolas with asymptotes `y = ±x` while `v = const` are the conjugate hyperbolas `xy = const`; the two pencils cross orthogonally.

## Section 7. Contour integration, Cauchy's theorem and Cauchy's formula

### Q124. Give the definition of the complex contour integral, and explain why it depends on the path only through the image curve, not the particular parametrization.

> **Type:** Recall
> **Answer:** For a piecewise smooth curve `C: z = z(t)`, `a ≤ t ≤ b`, `∫_C f(z)dz = ∫_a^b f(z(t)) z′(t) dt`.
> **Solution:** The definition is the complex analogue of the real line integral with the extra factor `dz`. A change of parametrization `t = t(s)` does not alter the value: substituting gives `∫ f(z(t(s))) z′(t(s)) t′(s) ds`, which is exactly the integral along the reparametrized curve, so the value is a property of the traced curve alone (with its orientation). A non-piecewise-smooth or non-continuous curve would make `z′` or the integral ill-defined, which is why "contour" always carries the regularity assumption.
> **Key point:** `∫_C f(z)dz = ∫_a^b f(z(t))z′(t)dt`; reparametrizing the curve does not change the value.

### Q125. State the three structural properties of the contour integral (linearity, additivity, orientation) and give a numerical illustration of each.

> **Type:** Recall
> **Answer:** (i) `∫_C (αf + βg)dz = α∫_C f dz + β∫_C g dz`; (ii) `∫_{C₁+C₂} f dz = ∫_{C₁} f dz + ∫_{C₂} f dz`; (iii) `∫_{−C} f dz = −∫_C f dz` for the reversed orientation.
> **Solution:** All three follow immediately from the parametric definition by linear combination, by splitting the parameter interval, and by using the reversed map `t ↦ z(a + b − t)`. Illustrations with `f(z) = 1` on the unit circle traversed once counterclockwise: (i) `∫_C 3 dz = 3·(z_end − z_start) = 0`, matching `3∫_C dz`; (ii) splitting the circle into two half-circles, each contributes `0`, and so does the whole; (iii) traversing the circle clockwise gives `∮ dz = 0` as well, since `∮dz = 0` for any closed curve — a good reminder that the orientation sign matters mainly for integrals that are **not** zero.
> **Key point:** Contour integrals are linear, additive over pieces, and change sign on reversal; `∮_C dz = 0` for every closed curve.

### Q126. Show that `∮_C zⁿ dz = 0` for every closed contour `C` and every non-negative integer `n`, and contrast with `n = −1`.

> **Type:** Theory
> **Answer:** `∮_C zⁿ dz = 0` for every non-negative integer `n`, but `∮_C dz/z = 2πi·n(C, 0)`, which is `2πi` when `0` is inside `C` and `0` when it is outside.
> **Solution:** For `n ≥ 0` the function `zⁿ` has the single-valued primitive `F(z) = z^{n+1}/(n+1)` on all of `ℂ`, and the integral of a function with a primitive around a closed curve vanishes: `∮_C zⁿdz = F(z_end) − F(z_start) = 0`. The case `n = −1` is different because `1/z` has **no** global primitive: its candidate `log z` is multivalued, and the integral measures precisely that failure, picking up `2πi` per counterclockwise winding of the contour about the origin. This contrast is the whole reason `dz/(z − z₀)` is the fundamental kernel of the subject.
> **Key point:** Every non-negative power of `z` has a global primitive, so its closed integral vanishes; only the negative power `1/z` contributes `2πi`.

### Q127. Evaluate `∮_C dz/z` where `C` is the unit circle traversed counterclockwise, directly by the substitution `z = e^{it}`, and state the general result for a contour and a point.

> **Type:** Numerical
> **Answer:** `2πi`. In general `∮_C dz/(z − z₀) = 2πi` if `z₀` is inside `C` and `0` if it is outside.
> **Solution:** Parametrize `z(t) = e^{it}`, `0 ≤ t ≤ 2π`, so `dz = ie^{it}dt` and `dz/z = ie^{it}dt/e^{it} = i dt`. Integrating, `∫_0^{2π} i dt = 2πi` ✓. This is nothing but `∫ dz/z = Log z_end − Log z_start` read as a continuously tracked argument: the argument must increase by `2π` during one counterclockwise turn, which is Q20. The dichotomy follows from Cauchy's integral theorem: on the region outside the point `z₀` the function `1/(z − z₀)` has the primitive `Log(z − z₀)`, so any contour not enclosing `z₀` gives zero; a contour enclosing it once gives `2πi` by the parametrization above.
> **Key point:** `∮_C dz/z = 2πi·n(C,0)`; substituting `z = e^{it}` on the unit circle turns it into the trivial integral `∫_0^{2π} i dt`.

### Q128. State the winding-number version of the kernel integral, and evaluate `∮_C dz/(z − 1)` for a contour that encircles `0` and `1` once anticlockwise and `2` once clockwise.

> **Type:** Numerical
> **Answer:** `∮_C dz/(z − z₀) = 2πi·n(C, z₀)`, so the value is `2πi`; more generally, with `g` analytic on a neighbourhood of the closed contour, `∮_C g(z)dz/(z − z₀) = 2πi·g(z₀)·n(C, z₀)`.
> **Solution:** The winding number `n(C, z₀)` is the signed number of times `C` winds about `z₀`, and the kernel integral of the form `1/(z − z₀)` depends on it alone: `∮_C dz/(z − z₀) = 2πi\,n(C, z₀)`. This is the topological face of the residue theorem, and it is the reason the number `2πi` is accompanied by a sign rather than by a bare count. Here `n(C, 1) = 1`, since the contour passes once anticlockwise about `1` and its clockwise pass is about `2` only, so `∮_C dz/(z−1) = 2πi`. The clockwise encirclement of `2` is irrelevant for this integrand, whose only pole is at 1. The weighted form carries the `g(z₀)` factor: it is `g(z₀)`, and not `1`, that multiplies the winding number, which reduces to the kernel value when `g \equiv 1`. For the integrand `1/((z−1)(z−2))` the two poles do both contribute, giving `2πi(1 + (−1)) = 0`, each pole entering with its own residue and its own winding number.
> **Key point:** `∮_C f(z)dz = 2πi\sum_j n(C, z_j)\,Res(f, z_j)`; for the kernel `1/(z−z₀)` this is `2πi\,n(C, z₀)`, and with a weight `g` it becomes `2πi\,g(z₀)n(C, z₀)`.

### Q129. Show that for a positively oriented simple closed curve `C`, `∮_C z̄ dz = 2i·Area(C)`, and evaluate it for the unit circle.

> **Type:** Numerical
> **Answer:** `∮_C z̄ dz = 2i·Area(C)`; for the unit circle, `2πi`.
> **Solution:** Write `z̄ = x − iy` and `dz = dx + i dy`; then `z̄dz = (x dx + y dy) + i(x dy − y dx)`. The real part is `½d(x² + y²)`, which integrates to `0` around a closed curve. The imaginary part `x dy − y dx` is twice the signed area enclosed (this is the standard area formula, equivalent to Green's theorem), so `∮_C z̄dz = 2i·Area`. For the unit circle, `Area = π`, giving `2πi` ✓. Cross-check: on `|z| = 1`, `z̄ = 1/z`, so `∮_C z̄dz = ∮_C dz/z = 2πi` ✓ — the two computations agree.
> **Key point:** `∮_C z̄dz = 2i·Area` for counterclockwise orientation; on the unit circle it coincides with `∮ dz/z = 2πi`.

### Q130. Evaluate `∫_C z̄ dz` where `C` is the straight segment from `0` to `1`, and where `C` is the straight segment from `−1` to `1`.

> **Type:** Numerical
> **Answer:** `1/2` for `0 → 1`, and `0` for `−1 → 1`.
> **Solution:** Since `z̄ dz = ½d(z z̄) = ½d|z|²`, the integral telescopes to `½(|z_end|² − |z_start|²)` for **any** path. For `0 → 1`: `½(1 − 0) = 1/2` ✓. For `−1 → 1`: `½(1 − 1) = 0` ✓. The second result is the important one: a real-axis path traversed symmetrically outward and back gives zero, whereas the closed unit circle gives `2πi` (Q129) — the integral of `z̄` is path-dependent, because `z̄` is not analytic.
> **Key point:** `∫_C z̄dz = ½(|z_end|² − |z_start|²)`; it is zero along any path whose endpoints have equal modulus.

### Q131. State Cauchy's integral theorem precisely, listing all the hypotheses, and explain which hypothesis fails for `f(z) = 1/z` and `C` the unit circle.

> **Type:** Recall
> **Answer:** If `f` is analytic **on and inside** a simple closed curve `C`, then `∮_C f(z)dz = 0`. For `f(z) = 1/z` and `C = {|z| = 1}` the hypothesis "analytic inside" fails, because `z = 0` is a pole inside `C`, and indeed the integral is `2πi ≠ 0`.
> **Solution:** The three hypotheses are: `C` is a closed piecewise-smooth contour; `f` is analytic on a domain containing `C` and its entire interior; and — for the common elementary form — `C` is positively oriented, though the value `0` is orientation-independent. Each hypothesis is doing work: violating analyticity on the contour makes the integral ill-defined, violating it in the interior is exactly what allows a nonzero value. The theorem's content is that the integral of an analytic function around a closed loop is zero, i.e. that `∫ f dz` is path-independent on any simply connected region.
> **Key point:** Cauchy's integral theorem needs analyticity on **and inside** `C`; the failure at one interior point (as for `1/z`) is exactly what produces `2πi` instead of `0`.

### Q132. Explain why `∮_C dz/z = 2πi` for the unit circle `C`, in a way that shows the singularity at `0` is the sole cause.

> **Type:** Conceptual
> **Answer:** Because `1/z` is analytic everywhere on the annulus `1/2 < |z| < 2` but not at `0`; deform the unit circle outward to `|z| = 3/2` without crossing the pole and the integral is unchanged (`2πi`), while a contour that shrinks toward `0` cannot be deformed to a point without crossing the pole.
> **Solution:** By the deformation theorem (Q134), two contours bounding a region free of singularities give the same integral. Between `|z| = 1` and `|z| = 3/2` there is no singularity, so `∮_{|z|=1} dz/z = ∮_{|z|=3/2} dz/z`. But shrinking the circle to a point would require sweeping across `z = 0`, so no such deformation exists. The only obstruction is the single point `0`. The same argument shows `∮_C dz/(z − 5) = 0` for the unit circle, since the region between it and any contractible loop contains no `z = 5`.
> **Key point:** Non-zero values of `∮` arise exactly from singularities the contour cannot be deformed across; one simple pole enclosed once gives exactly `2πi`.

### Q133. State the deformation-of-contours theorem and give an application: compute `∮_{|z| = 2} dz/(z² − 5)` two ways.

> **Type:** Numerical
> **Answer:** If `f` is analytic on and between two closed contours `C₁, C₂` traversed in the same sense, `∫_{C₁} f = ∫_{C₂} f`. Applying it: `∮_{|z|=2} dz/(z²−5) = 0`.
> **Solution:** The theorem is Cauchy's integral theorem applied to the closed region between `C₁` and `C₂`. For the application, `1/(z² − 5)` has simple poles at `z = ±√5 ≈ ±2.236`, and **both lie outside `|z| = 2`** since `2.236 > 2`. Method 1: by the theorem the circle may be shrunk to a point, `∮ = 0` ✓. Method 2: by the kernel formula the single factor `1/(z − √5)` has its pole outside and the factor `1/(z + √5)` has its pole at `−2.236`, also outside, so the integral vanishes ✓. Method 3: `1/(z²−5) = −(1/5)(1/(z²(1 − 5/z²)))` expands in powers of `1/z` valid for `|z| > √5`, which contains `|z| = 2`, and that expansion is valid only for `|z| > 2.236`, so it is **not** usable here — a good illustration of why the "expansion at infinity" method needs the contour to lie outside every pole.
> **Key point:** Deform contours only through singularity-free regions; `1/(z²−5)` has both poles at `|z| = 2.236 > 2`, so the integral over `|z| = 2` is 0.

### Q134. Outline the proof of Cauchy's integral theorem for a triangle by subdivision, and state the result for a rectangle.

> **Type:** Theory
> **Answer:** Subdivide the triangle into four similar triangles; by induction each has zero boundary integral, and in the sum the four interior edges cancel in pairs, leaving the outer boundary integral equal to 0. A rectangle is handled by cutting it into two triangles.
> **Solution:** The proof is by induction on the number of subdivisions, and the base case is where analyticity is used. If the closed triangle `T` lies inside a disc on which `f` is analytic, then `f` has a power series `Σ c_k(z − z*)ⁿ` about an interior point `z*`, and every term `(z − z*)^{k+1}/(k+1)` is an antiderivative, so `∮_{∂T} f\,dz = 0` term by term. For the inductive step, bisecting each edge gives four congruent similar triangles, each scaled by `1/2` in area and lying in a still smaller neighbourhood, so the induction hypothesis gives zero for each of the four boundary integrals. Summing them, each interior edge appears twice with opposite orientations and cancels, leaving exactly the integral over `∂T`; hence that is 0. The argument needs `f` analytic on a neighbourhood of the closed triangle, not merely continuous: a merely continuous integrand need not give 0, as `f(z) = \bar z` around a circle shows. Since any rectangle is the union of two triangles sharing a diagonal, and the diagonal cancels in the sum, the same conclusion `∮_{∂R} f\,dz = 0` holds for rectangles, which is the base case for rectangular contours.
> **Key point:** Subdivide until each small triangle lies in a disc of analyticity, where a power series makes the integral vanish; the interior edges then cancel in pairs, so analyticity, not mere continuity, is the hypothesis that carries the proof.

### Q135. Show that `∫_C f(z)dz` is independent of the path in a domain `D` if and only if `f` has a single-valued antiderivative on `D`. Construct the antiderivative.

> **Type:** Theory
> **Answer:** If `F′ = f` on `D`, then `∫_C f dz = F(z_end) − F(z_start)`, path-independent. Conversely, if all closed-path integrals vanish, fix `z₀ ∈ D` and define `F(z) = ∫_{z₀→z} f dz`; the vanishing of closed integrals makes `F` single-valued and the fundamental theorem gives `F′(z) = f(z)`.
> **Solution:** The forward direction is the chain rule: `∫_C f = ∫_C (F∘z)′ z′ dt = [F(z(t))]_a^b`. For the converse, define `F` as above; for `z₀, z, z+h ∈ D` the difference `F(z+h) − F(z)` equals the integral along the path from `z` to `z+h`, which by path independence is the straight segment, giving `F′(z) = lim_{h→0}∫_0^1 f(z + th)h dt = f(z)`. Example: `1/z` has no antiderivative on `ℂ \ {0}` (hence `∮ dz/z = 2πi ≠ 0`), while `1/(z−a)` on the half-plane `Re z < Re a` does, and there the integral depends only on the endpoints.
> **Key point:** Path independence ⟺ existence of a primitive; `∮ = 0` for every closed curve is the test.

### Q136. Write `∮_C f(z)dz` in terms of `u, v` and show by Green's theorem that it vanishes when `f` is analytic.

> **Type:** Theory
> **Answer:** `∮_C f dz = ∮(u dx − v dy) + i∮(v dx + u dy) = ∬_D[(−v_x − u_y) + i(u_x − v_y)]dA = 0`.
> **Solution:** With `f = u + iv` and `dz = dx + idy`, the product is `(u dx − v dy) + i(v dx + u dy)`. Green's theorem for a positively oriented curve gives `∮(P dx + Q dy) = ∬(Q_x − P_y)dA`. For the real part, `P = u`, `Q = −v`, so the integrand is `−v_x − u_y = 0` by CR ✓. For the imaginary part, `P = v`, `Q = u`, so the integrand is `u_x − v_y = 0` by CR ✓. Both vanish, so the whole integral is zero. This is the two-dimensional proof; it explains why the theorem is genuinely a statement about curl-free fields.
> **Key point:** `∮(u dx − v dy) = −∬(u_y + v_x)dA` and `∮(v dx + u dy) = ∬(u_x − v_y)dA`; CR kills both.

### Q137. Give Cauchy's proof of the integral theorem using the power-series expansion of `f` on a disc, and state the result for `∮_C zⁿdz` with `n ≥ 0`.

> **Type:** Theory
> **Answer:** If `f` is analytic on `|z − z₀| ≤ R` with `C ⊂ {|z − z₀| = R}`, then `f(z) = Σ aₙ(z − z₀)ⁿ` on the closed disc, so `∮_C f dz = Σ aₙ∮_C (z − z₀)ⁿ dz = 0` because each inner integral is zero. In particular `∮_C zⁿdz = 0` for all `n ≥ 0`.
> **Solution:** The series converges uniformly on the closed disc, so term-by-term integration along `C` is legitimate (this is exactly the uniform-convergence theorem of Section 8). Each term `(z − z₀)ⁿ` has the global primitive `(z − z₀)^{n+1}/(n+1)`, so its integral around a closed curve vanishes (Q126). Term `n = −1` does not exist in a Taylor series, which is precisely why the method proves the theorem but cannot evaluate `∮ dz/z`. Taking the disc as large as it can go pushed Cauchy towards Cauchy's integral formula, obtained next.
> **Key point:** Cauchy's series proof works because every term has a primitive; the `1/z` term is absent from any Taylor series, which is why the theorem cannot be pushed further this way.

### Q138. State Cauchy's integral formula and its hypotheses, and give the derivative form.

> **Type:** Recall
> **Answer:** If `f` is analytic on and inside a simple closed curve `C` and `z₀` is inside, then `f(z₀) = (1/2πi)∮_C f(z)/(z − z₀) dz`, i.e. `∮_C f(z)/(z − z₀)dz = 2πi f(z₀)`. Differentiating `n` times, `f^{(n)}(z₀) = (n!/(2πi))∮_C f(z)/(z − z₀)^{n+1}dz`.
> **Solution:** The function `f(z)/(z − z₀)` has a single simple pole at `z₀` with residue exactly `f(z₀)` (because `(z−z₀)f(z)/(z−z₀) = f(z) → f(z₀)`), and is analytic elsewhere inside `C`. So the residue theorem gives the formula; the derivative form follows by differentiating with respect to `z₀`, which pulls one power of `(z − z₀)` down each time and contributes a factor `n!`. The formula says the values of an analytic function **inside** a contour are determined by its values **on** the contour.
> **Key point:** `f(z₀) = (1/2πi)∮ f(z)/(z−z₀)dz`; the residue of `f(z)/(z−z₀)` at `z₀` is `f(z₀)` itself, not `f′(z₀)`.

### Q139. Use Cauchy's integral formula with `f(z) = e^z` and `C` the unit circle to confirm `f(0) = 1` and `f′(0) = 1`, evaluating the corresponding integrals.

> **Type:** Numerical
> **Answer:** `∮_{|z|=1} e^z/z dz = 2πi` and `(1/2πi)∮_{|z|=1} e^z/z² dz = 1`; both give `1` for the corresponding value of `f` at 0.
> **Solution:** `e^z` is entire, so the hypotheses hold. By the formula, `f(0) = e^0 = 1 = (1/2πi)∮ e^z/z dz`, so the integral is `2πi`. The function `e^z/z²` has a double pole at `0` with residue `d/dz[e^z]|_{z=0} = 1`, so `(1/2πi)∮ e^z/z² dz = 1`, matching `f′(0) = 1` ✓. Direct check by parametrization on the unit circle for the first: `z = e^{it}`, `dz = ie^{it}dt`, `∫_0^{2π} e^{e^{it}}ie^{it}/e^{it}dt = i∫_0^{2π}e^{e^{it}}dt`, and `e^{e^{it}} = e^{cos t}e^{i sin t}` has mean value 1 over the circle, so the integral is `2πi` ✓.
> **Key point:** `f(0) = (1/2πi)∮ f/z dz` recovers the Taylor coefficients; the `z^{−1}` coefficient of `f`'s Laurent expansion at 0 is `f(0)`.

### Q140. Use Cauchy's derivative formula to evaluate `f^{(3)}(0)` for `f(z) = 1/(1 + z)` on `|z| = 1/2`, and check against the recurrence.

> **Type:** Numerical
> **Answer:** `f^{(3)}(0) = −6`.
> **Solution:** `f(z) = 1/(1+z)` is analytic on `|z| ≤ 1/2` (its pole is at `z = −1`), and `0` is inside. The formula gives `f^{(3)}(0) = (3!/(2πi))∮_{|z|=1/2} dz/((1+z)z⁴)`. The integrand has a fourth-order pole at `0` and no other singularity inside (`z = −1` is at distance 1 > 1/2), so the integral is `2πi` times the residue. Expanding `1/(1+z) = 1 − z + z² − z³ + z⁴ + z⁵` and picking the coefficient of `z³` (which multiplies `z^{−4}`) gives residue `−1`, so `∮ = −2πi` and `f^{(3)}(0) = (6/(2πi))(−2πi) = −6` ✓. Recurrence check: `f′ = −(1+z)^{−2}`, `f″ = 2(1+z)^{−3}`, `f^{(3)} = −6(1+z)^{−4}`, so `f^{(3)}(0) = −6` ✓.
> **Key point:** The residue of `f(z)/z^{n+1}` at 0 is exactly `f^{(n)}(0)/n!`; for `1/(1+z)` the coefficients are `(−1)^n`, giving `f^{(n)}(0) = (−1)^n n!`.

### Q141. State Cauchy's inequality and use it to bound `|f'(0)|` for `f` analytic on `|z| ≤ 1` with `|f(z)| ≤ M`.

> **Type:** Numerical
> **Answer:** `|f^{(n)}(z₀)| ≤ n!\,M/Rⁿ`; on the unit disc with `|f| \le M` this gives `|f^{(n)}(0)| \le n!\,M`, and in particular `|f'(0)| \le M`.
> **Solution:** Differentiating the Cauchy integral formula `n` times under the integral sign gives `f^{(n)}(z₀) = (n!/(2πi))∮ f(z)/(z − z₀)^{n+1}dz`, and on a circle of radius `R` about `z₀` the modulus of the integrand is at most `M/R^{n+1}` while the contour has length `2πR`. Hence `|f^{(n)}(z₀)| \le (n!/(2\pi))(2\pi R)M/R^{n+1} = n!M/R^{n}`. For `n = 1`, `z₀ = 0` and `R = 1` this reads `|f'(0)| \le M`. The inequality quantifies analyticity: the Taylor coefficients satisfy `|a_n| \le M/Rⁿ`, so an analytic function's coefficients cannot grow faster than a geometric rate, which is why a function with an essential singularity or a pole is never analytic on a disc containing the offending point. The same estimate proves Liouville's theorem: if `f` is entire and `|f| \le M` everywhere, then `|f^{(n)}(z₀)| \le n!M/R^{n}`, which tends to 0 as `R \to \infty` for every `n \ge 1`; all derivatives of order at least 1 vanish and `f` is constant. The step `n \ge 1` is essential, since `n = 0` gives only `|f(z₀)| \le M`, which holds for every bounded function.
> **Key point:** `|f^{(n)}(z₀)| \le n!M/Rⁿ`, so `|f'(0)| \le M` on the unit disc; letting `R \to \infty` for a bounded entire `f` kills every derivative of order at least 1, which is Liouville's theorem.

### Q142. `GATE-1` Evaluate `∮_{|z| = 1} (z² + 1)/(z³ + 4) dz`.

> **Type:** MCQ
> **Answer:** `0` (Option b).
>
> (a) `2πi`
> (b) `0`
> (c) `4πi`
> (d) `−2πi`
>
> **Solution:** The zeros of `z³ + 4` are `z = 4^{1/3}e^{i(π + 2kπ)/3}` for `k = 0, 1, 2`, all of modulus `4^{1/3} ≈ 1.587`. Since `1.587 > 1`, **no** pole lies inside `|z| = 1`, and none lies on the contour. Cauchy's integral theorem then applies (the integrand is analytic on and inside the unit circle) and the integral is `0` ✓. Option (a) is the trap of answering from the shape of the denominator alone, and option (c) of assuming three poles inside because there are three of them. The decisive step in every such question is to list the poles and check their moduli.
> **Key point:** `4^{1/3} ≈ 1.587 > 1`, so all three poles of `z³ + 4` are **outside** `|z| = 1` and the integral is 0.

### Q143. `GATE-1` Evaluate `∮_{|z| = 1} dz/(z − 2)` and `∮_{|z| = 1} dz/(z² − 4)`.

> **Type:** MCQ
> **Answer:** Both integrals are `0` (Option d).
>
> (a) `2πi` and `2πi`
> (b) `0` and `2πi`
> (c) `2πi` and `0`
> (d) `0` and `0`
>
> **Solution:** `1/(z − 2)` has its only pole at `z = 2`, which is outside `|z| = 1`, so the integral is `0`. `1/(z² − 4) = 1/((z−2)(z+2))` has poles at `z = ±2`, both at modulus 2, hence both outside `|z| = 1`, so again `0`. Option (a) is the standard trap: the shape of the denominator suggests a pole "somewhere", but its location is what matters. A useful check: `1/(z − 2) = −(1/2)·1/(1 − z/2) = −(1/2)Σ(z/2)ⁿ`, whose expansion about `0` converges for `|z| < 2`; every term integrates to zero on `|z| = 1`, giving `0` ✓.
> **Key point:** "Pole exists" is not enough — check `|z₀| < R`. For `|z| = 1` and poles at `±2` or at `2`, the answer is always 0.

### Q144. Explain why `∮_{|z| = 1} dz/(z² + 1)` is not defined, and state the value for `|z| = 1/2` and for `|z| = 2`.

> **Type:** Common-mistake
> **Answer:** Undefined for `|z| = 1`; `0` for `|z| = 1/2`; `0` for `|z| = 2`.
> **Solution:** `1/(z² + 1)` has simple poles at `z = i` and `z = −i`, and `|i| = |−i| = 1` exactly. A pole on the contour makes the integrand unbounded there, so the integral fails to exist even in the improper sense; the residue theorem simply does not apply. For `|z| = 1/2` neither pole is inside, so Cauchy's integral theorem gives `0` ✓. For `|z| = 2` both poles are inside; the residues are `Res(i) = 1/(2i) = −i/2` and `Res(−i) = 1/(−2i) = +i/2`, whose sum is `0`, so the integral is `2πi·0 = 0` ✓. The cancellation is systematic: `1/(z²+1) = −z^{−2}(1 + z^{−2})^{−1} = −z^{−2} + z^{−4} − z^{−6} + z^{−8} + z^{−10}` for `|z| > 1`, an expansion with no `z^{−1}` term and hence no total residue.
> **Key point:** Poles **on** the contour make the integral undefined; here `|i| = 1` is exactly the worst radius, and either larger or smaller disc gives `0`.
### Q145. `GATE-2` Evaluate `∮_{|z| = 2} dz/(z³ + 4)`, which has three poles inside the contour.

> **Type:** MCQ
> **Answer:** `0` (Option a).
>
> (a) `0`
> (b) `2πi`
> (c) `6πi`
> (d) `2πi/3`
>
> **Solution:** The poles are `a_k = 4^{1/3}e^{i(π+2kπ)/3}`, `k = 0, 1, 2`, all of modulus `4^{1/3} ≈ 1.587 < 2`, so all three lie inside `|z| = 2`. At a root `a`, `Res = 1/(3a²)`. Since `a³ = −4`, we get `a^{−2} = −a/4`, and therefore `Res(a) = −a/12`. Summing over the three roots, `Σ Res = −(1/12)Σa_k = 0`, because `z³ + 4` has no `z²` term, so the sum of its roots is `0`. Hence `∮_{|z|=2} dz/(z³+4) = 2πi·0 = 0` ✓. Cross-check by expansion at infinity: `1/(z³+4) = z^{−3}(1 + 4/z³)^{−1} = z^{−3} − 4z^{−6} + 16z^{−9} − 64z^{−12}`, containing no `z^{−1}` term, so the total residue is zero ✓. Option (b) is the trap of assuming "three poles ⟹ `2πi` each".
> **Key point:** Each simple pole of `1/P(z)` contributes `1/P′(a)`; for `z³+4` these sum to zero because the sum of the roots of `z³+4` is zero.

### Q146. Evaluate `∫_C dz/z` where `C` is the upper semicircle of the unit circle traversed counterclockwise from `1` to `−1`, and compare it with the full circle.

> **Type:** Numerical
> **Answer:** `iπ` for the semicircle, versus `2πi` for the full circle.
> **Solution:** Parametrize `z = e^{it}`, `0 ≤ t ≤ π`: `dz = ie^{it}dt` and `dz/z = i dt`, so `∫_0^π i dt = iπ`. The full circle gives `2πi` (Q127), exactly double, because the arc is half the circle in angle and `dz/z` is purely `i dt`. The semicircular value is purely imaginary, which makes sense: the value of `∫ dz/z` along any path equals the change in the continuously tracked argument, and moving from argument 0 to argument π changes it by `π`.
> **Key point:** Along any path, `∫ dz/z = Δ(arg z) = i·Δ(arg)`; the semicircle gives `iπ`, the full circle `2πi`.

### Q147. Evaluate `∫_C z² dz` along the straight line from `z = i` to `z = 1 + i`, and state why the path does not matter here.

> **Type:** Numerical
> **Answer:** `(−2 + 3i)/3 ≈ −0.667 + 1.000i`.
> **Solution:** `z²` has the global primitive `F(z) = z³/3`, so `∫_C z²dz = F(1+i) − F(i) = ((1+i)³ − i³)/3`. Computing, `(1+i)² = 2i` and `(1+i)³ = 2i(1+i) = 2i + 2i² = −2 + 2i`, while `i³ = −i`. So the answer is `(−2 + 2i + i)/3 = (−2 + 3i)/3 ≈ −0.6667 + 1.0000i` ✓. The path does not matter because `z²` is entire and hence has a primitive on all of `ℂ`; this is the contrast case with `1/z` (Q127) and `z̄` (Q130), where the value is path-dependent.
> **Key point:** If `f` has a global primitive, `∫ f dz` depends only on the endpoints: `F(z_end) − F(z_start)`.

### Q148. `GATE-1` Evaluate `∮_{|z| = 1} dz/z³`.

> **Type:** MCQ
> **Answer:** `0` (Option c).
>
> (a) `2πi`
> (b) `−2πi`
> (c) `0`
> (d) `6πi`
>
> **Solution:** The integrand has a pole of order 3 at `z = 0`, and `0` is inside `|z| = 1`. But `∮ = 2πi·Res(1/z³, 0)`, and the Laurent expansion `z^{−3}` contains **no** `z^{−1}` term, so the residue is `0` and the integral vanishes ✓. Equivalently, Cauchy's derivative formula with `f ≡ 1` gives `(1/2πi)∮ f(z)/(z − z₀)³ dz = f″(z₀)/2! = 0` ✓. Option (a) is the trap of answering `2πi` because there is a pole inside — the residue, not the presence of a pole, is what multiplies `2πi`. Option (d) is the trap of multiplying by the pole's order.
> **Key point:** `∮ z^{−n}dz = 2πi δ_{n,1}`: only the `z^{−1}` coefficient (the residue) contributes.

### Q149. `GATE-2` `NAT` Let `f(z) = (z − 1)³(z + 1)²/(z − 2)²` and let `C` be `|z| = 3` traversed counterclockwise. What is `(1/2πi)∮_C f′(z)/f(z) dz`?

> **Type:** MCQ
> **Answer:** `3` (Option a).
>
> (a) `3`
> (b) `5`
> (c) `2`
> (d) `1`
>
> **Solution:** The argument principle gives `(1/2πi)∮_C f′(z)/f(z) dz = Z − P`, the number of zeros minus the number of poles of `f` inside `C`, each counted with multiplicity. Zeros: `z = 1` with multiplicity 3 and `z = −1` with multiplicity 2, so `Z = 5`. Poles: `z = 2` with multiplicity 2, so `P = 2`. The points `1`, `−1` and `2` all have modulus less than 3, so everything is inside `C` and no point of the integrand's singularities lies on it. Hence `Z − P = 5 − 2 = 3` ✓. Option (b) counts only the zeros, option (c) only the poles, and option (d) forgets multiplicities. The residues of `f` play no role at all: `f′/f` is what is being integrated, and it knows only about zero and pole counts.
> **Key point:** `(1/2πi)∮ f′/f dz = Z − P` with multiplicities; residues of `f` are irrelevant, and the zeros must be located and counted.
### Q150. Using Cauchy's integral formula, express the Taylor coefficients of `f` about `z₀` in terms of the boundary values, and explain why the disc of integration can be enlarged until it meets a singularity.

> **Type:** Theory
> **Answer:** `f^{(n)}(z₀) = (n!/(2πi))∮_C f(z)/(z − z₀)^{n+1}dz`; enlarging `C` (keeping `z₀` inside) is allowed whenever the added region is free of singularities, so the disc of convergence extends to the nearest singularity of `f`.
> **Solution:** Because the integral of `f(z)/(z − z₀)^{n+1}` is unchanged when the contour is deformed outward through singularity-free regions (Q133), the coefficients depend only on the radius up to the first singularity. The practical statement: a Taylor series about `z₀` can be computed by integrating around **any** contour encircling `z₀` within the largest such singularity-free region, and the result is the same series. Choosing a large, convenient contour is therefore a legitimate and common strategy in inverse Z-transform and Fourier-type work.
> **Key point:** Cauchy coefficients are invariant under contour deformation through singularity-free regions — choose the contour that makes the algebra easiest.

### Q151. `GATE-2` `MSQ` Which of the following statements about `∮_C f(z)dz` are correct? (A) It is `0` if `f` is analytic on and inside `C`. (B) It is `2πi` times the sum of residues of `f` inside `C`. (C) It depends only on the residues of the poles inside `C` and not on the shape of `C`. (D) It is unchanged if `C` is replaced by a curve winding the same way round every interior point.

> **Type:** MCQ
> **Answer:** A, B, C and D (Option c).
>
> (a) A only
> (b) A and B only
> (c) A, B, C and D
> (d) B and C only
>
> **Solution:** (A) is Cauchy's integral theorem ✓. (B) is the residue theorem ✓. (C) follows from (B): the value is `2πi Σ Res`, a number determined by the poles inside, so any change in the shape of `C` that does not cross a pole leaves the value unchanged ✓. (D) is the deformation theorem, restated in terms of winding numbers ✓. The qualification in (C) and (D) is essential: deforming `C` so as to **enclose or exclude** a pole does change the value, which is why the shape matters only through the winding numbers `n(C, zⱼ)`.
> **Key point:** `∮_C f dz = 2πi Σⱼ n(C, zⱼ)Res(f, zⱼ)`: the shape of `C` matters only through the winding numbers.

### Q152. `GATE-2` Use Cauchy's integral formula to evaluate `∮_{|z| = 2} 1/((z − 1)(z + 3)) dz` without computing residues.

> **Type:** Numerical
> **Answer:** `πi/2`.
> **Solution:** `f(z) = 1/(z + 3)` is analytic on and inside `|z| = 2`, since its only pole is at `z = −3`, outside. Taking `z₀ = 1` in Cauchy's formula, `∮_{|z|=2} dz/((z−1)(z+3)) = 2πi·f(1) = 2πi·(1/4) = πi/2` ✓. Direct check by residues: at `z = 1`, `1/(1+3) = 1/4`; at `z = −3`, `1/(−3−1) = −1/4`; the sum is `0` — but `z = −3` is **outside** `|z| = 2`, so only the residue `1/4` counts, giving `2πi/4 = πi/2` ✓. The Cauchy-formula route is shorter because it never requires the second pole.
> **Key point:** `∮ f(z)/(z − z₀)dz = 2πi f(z₀)` when `f` is analytic on and inside `C` — one pole factored off, the rest ignored.

## Section 8. Series of analytic functions, uniform convergence and Laurent expansion

### Q153. State the uniform-limit theorem for analytic functions and outline its proof.

> **Type:** Theory
> **Answer:** If `fₙ` are analytic on a domain `D` and `fₙ → f` uniformly on every compact subset of `D`, then `f` is analytic on `D`. The proof must not assume `f` analytic in advance.
> **Solution:** Fix `z₀ ∈ D` and choose `ρ > 0` with the closed disc `K = {|z − z₀| \le \rho}` contained in `D`; let `C` be its boundary. Local uniform convergence makes `f` continuous on `K`, since a uniform limit of continuous functions is continuous. Define `F(z) = (1/(2πi))∮_C f(w)/(w − z) dw` for `z` inside `C`. `F` is analytic in the interior: differentiating under the integral sign is justified because the difference quotients of the kernel `1/(w − z)` are uniformly bounded on any smaller disc, by a fixed distance from `w` to that disc. For each `n`, the same construction with `fₙ` in place of `f` is analytic, and Cauchy's formula, which does apply to `fₙ`, gives `fₙ(z) = Fₙ(z)` in the interior. Finally `Fₙ → F` uniformly on the interior: the integrands converge uniformly on `C` and the kernel is bounded there, being at most `1/\delta` away from `C` for `z` in a smaller disc. Passing to the limit, `f(z) = F(z)` in the interior, so `f` is analytic there. Nothing in the argument used analyticity of `f`, which is what makes it non-circular. The essential hypothesis is **local** uniformity; uniformity on all of `D` is stronger than needed.
> **Key point:** Local uniform limits of analytic functions are analytic; the proof builds the analytic function `F(z) = (1/(2\pi i))\oint_C f(w)/(w-z)dw` from the continuity of `f` and identifies `f = F` via Cauchy's formula applied to `fₙ` alone.

### Q154. State the Weierstrass M-test and use it to prove uniform convergence of `Σ zⁿ` on `|z| ≤ r < 1`, with an explicit tail bound.

> **Type:** Theory
> **Answer:** If `|fₙ(z)| ≤ Mₙ` for all `n` and all `z` in the set, and `Σ Mₙ` converges, then `Σ fₙ` converges uniformly and absolutely there. For `fₙ = zⁿ` on `|z| ≤ r`, take `Mₙ = rⁿ`.
> **Solution:** The geometric series `Σ rⁿ = r/(1−r) < ∞` for `r < 1`, so the M-test gives uniform and absolute convergence on `|z| ≤ r` ✓. The tail bound is the useful quantitative part: for `M > N`, `|Σ_{n>N}^{M} zⁿ| ≤ Σ_{n>N}^{M} rⁿ ≤ r^{N+1}/(1−r) → 0` uniformly in `z` ✓. This independence from `z` is exactly what licenses term-by-term integration and differentiation. The same argument with `Mₙ = rⁿ/n` shows `Σ zⁿ/n` is uniformly convergent on every `|z| ≤ r`, `r < 1`.
> **Key point:** `Mₙ = rⁿ` with `Σ rⁿ < ∞` for `r < 1` proves uniform convergence on every smaller disc, with tail `≤ r^{N+1}/(1−r)`.

### Q155. `GATE-1` Discuss the convergence of `Σ_{n≥1} zⁿ` on the three regions `|z| < 1`, `|z| = 1` and `|z| > 1`.

> **Type:** MCQ
> **Answer:** Absolutely convergent for `|z| < 1` and divergent for `|z| ≥ 1` (Option b).
>
> (a) convergent for `|z| ≤ 1`
> (b) convergent for `|z| < 1` only
> (c) convergent for `|z| > 1` only
> (d) convergent nowhere
>
> **Solution:** For `|z| < 1` the series is geometric with ratio `z`, so it converges absolutely to `−1/(1−z)` ✓. For `|z| > 1` the terms `zⁿ` do not tend to `0`, so the series diverges by the term test ✓. For `|z| = 1` the terms have modulus 1, so they again fail the term test and the series diverges at **every** point of the circle ✓. Option (a) is the trap of extrapolating the interior behaviour to the boundary. The general rule, used throughout this section, is absolute convergence inside the radius, divergence outside it, and undecided behaviour on the circle itself.
> **Key point:** A power series converges absolutely for `|z| < R` and diverges for `|z| > R`; on `|z| = R` the coefficients decide.

### Q156. Show that `Σ_{n≥1} zⁿ` has a continuous sum on the closed unit disc although the convergence is not uniform there.

> **Type:** Conceptual
> **Answer:** The sum `−1/(1−z)` is continuous on `|z| ≤ 1`, but convergence is not uniform because `sup_{|z|≤1}|zⁿ| = 1` for all `n`, violating the necessary condition for uniform convergence.
> **Solution:** The sum `1/(z−1)` is rational, hence continuous on any finite set, in particular on the closed unit disc ✓. Uniform convergence of `Σ fₙ` requires the necessary condition `sup|fₙ| → 0`; here `sup_{|z|≤1}|zⁿ| = 1` for every `n`, attained at `|z| = 1`, so that condition fails ✓. The example shows that continuity of the limit function does not imply uniform convergence, and hence the uniform-limit theorem must be stated with the weaker, local uniformity hypothesis used next.
> **Key point:** A continuous limit does not imply uniform convergence; `sup|zⁿ| = 1` blocks uniformity while the sum remains continuous.

### Q157. State the "uniformly on compact subsets" version of the uniform-limit theorem and show the sum of `Σ zⁿ` is analytic on `|z| < 1`.

> **Type:** Theory
> **Answer:** Local uniform convergence suffices. Since for every `r < 1` the series converges uniformly on `|z| ≤ r`, the sum `1/(z−1)` is analytic on `|z| < 1`.
> **Solution:** For each fixed `r < 1` the M-test gives uniform convergence on the closed disc `|z| ≤ r` (Q154), and that disc is a compact subset of the open unit disc. The uniform-limit theorem applied on each such disc makes the sum analytic on `|z| < 1` ✓. Nothing uniform survives at the boundary, which is why the theorem is formulated compactly rather than globally. This is the standing situation for every power series: strictly inside its disc of convergence all manipulations — integration, differentiation, substitution into analytic functions — are legitimate.
> **Key point:** Compact (not global) uniform convergence is the operative hypothesis; every power series meets it strictly inside its radius.

### Q158. State the condition for interchanging a sum with a contour integral, and apply it to `∫_C Σ_{n≥0} aₙzⁿdz`.

> **Type:** Theory
> **Answer:** Uniform convergence on `C` permits the exchange, so `∫_C Σ_{n≥0}aₙzⁿdz = Σ_{n≥0}aₙ∫_C zⁿdz = 0` for any closed `C` on which the Taylor series converges, since `∫_C zⁿdz = 0` for all `n ≥ 0`.
> **Solution:** Uniform convergence on `C` is the condition that permits the exchange, exactly as for a real series under a real integral. With `C` closed and the series a Taylor series in non-negative powers, each term integrates to zero because `zⁿ` has a global primitive (Q126), so the total is `0` ✓. This reproduces Cauchy's theorem from series theory (Q137) and shows why the `z^{−1}` term must be absent for the argument to work: for a Laurent series `Σ_{n≥0} bₙz^{−n−1}` valid on `C`, the integral equals `2πi b₀`, i.e. `2πi` times the residue.
> **Key point:** Uniform convergence on the contour licenses the exchange; a Taylor series integrates to zero, a Laurent series to `2πi` times its `z^{−1}` coefficient.

### Q159. State the conditions for term-by-term differentiation of a series of analytic functions, and note what holds automatically for a power series.

> **Type:** Recall
> **Answer:** If each `fₙ` is analytic on `D`, the series `Σ fₙ′` converges uniformly on compact subsets of `D`, and `Σ fₙ(z₀)` converges at one point `z₀ ∈ D`, then `Σ fₙ` converges locally uniformly to an analytic `f` with `f′ = Σ fₙ′`. For a power series all three conditions are automatic for `|z| < R`.
> **Solution:** The condition on the **derivative** series alone is not sufficient; the base point matters, and the standard counterexample is `fₙ \equiv 1`, whose derivative series is identically zero and so converges uniformly, while `Σ fₙ` diverges. With the base point supplied, convergence of `Σ fₙ(z₀)` turns the derivative estimate into a bound on the tails, because for `z` in a small disc about `z₀`, `Σ_{n>N} fₙ(z) = Σ_{n>N} fₙ(z₀) + (1/(2πi))∮ (Σ_{n>N} fₙ′(w))\,(1/(w − z) − 1/(w − z₀))\,dw`, and the integral term is bounded by the length of the contour times the supremum of the derivative tail times a fixed constant. The first term tends to 0 by the base-point assumption and the second by the uniform convergence of the derivative series, giving local uniform convergence; term-by-term differentiation then yields `f′ = Σ fₙ′`. For a power series `Σ aₙ zⁿ` the three conditions are all met inside the radius of convergence, since the derivative series has the same radius `R` by Cauchy–Hadamard (Q160) and converges locally uniformly there. Differentiation at a point of the circle of convergence is a separate question not covered by this theorem.
> **Key point:** Term-by-term differentiation needs uniform convergence of `Σ fₙ′` on compact subsets **plus** convergence of `Σ fₙ` at one point; for a power series both hold automatically for `|z| < R`.

### Q160. State Cauchy's convergence theorem (the Cauchy–Hadamard formula) and the radius of convergence of `Σ aₙ(z − z₀)ⁿ`.

> **Type:** Recall
> **Answer:** `R = 1/limsup_{n→∞} |aₙ|^{1/n}`, with `1/0 = ∞` and `1/∞ = 0`. The series converges absolutely for `|z − z₀| < R` and diverges for `|z − z₀| > R`.
> **Solution:** The formula follows from the root test applied to `|aₙ(z−z₀)ⁿ|`, and is the practical test for radii. Worked cases: `Σ zⁿ` has `limsup 1 = 1`, so `R = 1`; `Σ n zⁿ` has `limsup n^{1/n} = 1`, so `R = 1`; `Σ (2z)ⁿ` has `limsup 2 = 2`, so `R = 1/2`; `Σ zⁿ/n!` has `limsup (n!)^{−1/n} = 0` (Stirling), so `R = ∞`; `Σ n!zⁿ` has `limsup (n!)^{1/n} = ∞`, so `R = 0` ✓. The `limsup` is essential: `Σ z^{n²}/n²` has `limsup |aₙ|^{1/n}` oscillating according to whether `n` is a square, and `limsup` correctly gives `R = 1` even though the individual limits do not exist.
> **Key point:** `R = 1/limsup|aₙ|^{1/n}`; polynomial coefficients give `R = ∞`, factorial coefficients give `R = 0`.

### Q161. `GATE-2` Determine the radius of convergence of each series: `Σ n!zⁿ`, `Σ zⁿ/n!`, `Σ(2z)ⁿ`, `Σ n zⁿ`.

> **Type:** MCQ
> **Answer:** `0, ∞, 1/2, 1` respectively (Option c).
>
> (a) `∞, 0, 1/2, 1`
> (b) `0, ∞, 2, 1`
> (c) `0, ∞, 1/2, 1`
> (d) `1, ∞, 1/2, 0`
>
> **Solution:** By Cauchy–Hadamard (Q160). For `Σ n!zⁿ`, `limsup (n!)^{1/n} = ∞` (since `n!` eventually exceeds any geometric power), so `R = 1/∞ = 0` — the series diverges for every `z ≠ 0` ✓. For `Σ zⁿ/n!`, Stirling's formula `(n!)^{1/n} ≈ n/e` gives `limsup (1/n!)^{1/n} = 0`, so `R = 1/0 = ∞` ✓; the sum is `e^z`, entire. For `Σ(2z)ⁿ`, `limsup |2|^{1} = 2`, so `R = 1/2` ✓. For `Σ n zⁿ`, `limsup n^{1/n} = 1`, so `R = 1` ✓. Option (a) has the first two reversed, which is the commonest error here: it is the **numerator** `n!` that kills the radius, not the denominator.
> **Key point:** `n!` in the numerator gives `R = 0`; `n!` in the denominator gives `R = ∞`; a constant factor `2ⁿ` in the numerator shrinks `R` to `1/2`.

### Q162. State Cauchy's coefficient estimate and derive it from Cauchy's integral formula.

> **Type:** Theory
> **Answer:** If `|f(z)| ≤ M` on `|z − z₀| = R`, then `|aₙ| = |f^{(n)}(z₀)|/n! ≤ M/Rⁿ`.
> **Solution:** Cauchy's formula gives `aₙ = f^{(n)}(z₀)/n! = (1/(2πi))∮_{|z−z₀|=R} f(z)/(z−z₀)^{n+1}dz`. Taking moduli and estimating, `|aₙ| ≤ (1/(2π))(2πR)·M/R^{n+1} = M/Rⁿ` ✓. Two consequences worth remembering: the coefficients must satisfy `|aₙ| ≤ M/Rⁿ`, so if they fail a factorial growth bound no such `M` exists and `R` is smaller; and by taking `M` as the maximum of `|f|` on a circle of radius `R` and letting `R → ∞`, one gets Liouville's theorem for bounded entire functions (Q141).
> **Key point:** `|aₙ| ≤ M/Rⁿ` with `M = max|f|` on the circle; a sequence growing faster than any `R^{−n}` cannot be the Taylor coefficients of a function analytic on that disc.

### Q163. Show that the behaviour of a power series on its circle of convergence is not determined by the radius, using `Σ zⁿ`, `Σ zⁿ/n` and `Σ zⁿ/n²`.

> **Type:** Conceptual
> **Answer:** All three have `R = 1`. On `|z| = 1`, `Σ zⁿ` diverges everywhere, `Σ zⁿ/n` diverges at `z = 1` and converges at every other point of the circle, and `Σ zⁿ/n²` converges absolutely everywhere on the circle.
> **Solution:** `Σ zⁿ`: the terms have modulus 1, so the term test fails everywhere ✓. `Σ zⁿ/n`: at `z = 1` it is the divergent harmonic series; at `z = −1` it is the alternating harmonic series, which converges to `−ln 2`; at `z = e^{iθ}` with `θ ≠ 0` it is a Dirichlet-type series converging by summation by parts ✓. `Σ zⁿ/n²`: since `|zⁿ/n²| = 1/n²` on the circle and `Σ 1/n²` converges, the comparison test gives absolute convergence at every point ✓, and the value is bounded by `π²/6`. Three series, one radius, three different boundary behaviours — which is why every statement about `|z| = R` must be proved separately for the particular series.
> **Key point:** `Σ zⁿ`, `Σ zⁿ/n`, `Σ zⁿ/n²` all have `R = 1` but respectively diverge everywhere, diverge only at `z = 1`, and converge absolutely everywhere on the circle.

### Q164. `GATE-2` Find the region of convergence of `Σ_{n≥1} zⁿ/n` and identify its sum, including the behaviour at `z = −1`.

> **Type:** Numerical
> **Answer:** Converges for `|z| ≤ 1` except at `z = 1`; the sum is `−log(1−z)`, and at `z = −1` the sum is `−ln 2`.
> **Solution:** For `|z| < 1` integrate the geometric series term-by-term from `0` to `z`: `∫₀^z (1/(1−w))dw = Σ_{n≥0} z^{n+1}/(n+1)`, so `Σ_{n≥1} zⁿ/n = −log(1−z)` ✓. The radius is 1 since `limsup (1/n)^{1/n} = 1` ✓. On `|z| = 1`, at `z = 1` this is the harmonic series and diverges ✓. At `z = −1` the terms are `(−1)ⁿ/n`, the alternating harmonic series, which converges by the alternating test to `−ln 2` ✓ — and this agrees with `−log(1−(−1)) = −log 2` on the principal branch. For all other points of the circle, summation by parts applied to the bounded partial sums of `zⁿ` gives convergence. So the series is one of the standard examples of a series that converges at most, but not all, points of its circle of convergence.
> **Key point:** `Σ zⁿ/n = −log(1−z)`, radius 1; it diverges only at `z = 1` and takes the value `−ln 2` at `z = −1`.

### Q165. Show that `Σ_{n≥1} zⁿ/n²` converges absolutely at every point of `|z| = 1`, and contrast with Q164.

> **Type:** Theory
> **Answer:** On `|z| = 1`, `|zⁿ/n²| = 1/n²` and `Σ 1/n²` converges, so the series converges absolutely and uniformly on the whole closed unit disc; the sum is continuous there and equals `Li₂(z) = −∫₀^z log(1−w)/w dw`.
> **Solution:** By the comparison test with the numerical series `Σ 1/n²`, convergence is absolute at every point of `|z| ≤ 1` ✓. Better still, the M-test with `Mₙ = 1/n²` gives **uniform** convergence on the closed unit disc, so the sum is continuous on the closed disc even at `z = 1`, where the value is `π²/6` ✓ — a striking contrast with `Σ zⁿ/n` (Q164), which is not uniformly convergent on the circle and diverges at `z = 1`. The sum is written `Li₂(z)`, defined by `d/dz Li₂(z) = −log(1−z)/z` with `Li₂(0) = 0`, and `Li₂(1) = π²/6` is the Basel sum.
> **Key point:** `Σ zⁿ/n²` converges uniformly on `|z| ≤ 1` (M-test with `1/n²`) and is continuous there, with `Li₂(1) = π²/6`.

### Q166. `GATE-2` Use term-by-term integration to show that `∫₀¹ dx/(1 + x) = 1 − 1/2 + 1/3 − 1/4 + ⋯ = ln 2`.

> **Type:** Numerical
> **Answer:** `ln 2`, i.e. `Σ_{n≥1}(−1)^{n+1}/n = ln 2`.
> **Solution:** The geometric series `Σ_{n≥0}(−x)ⁿ = 1/(1+x)` converges uniformly on `[0, 1−δ]` for every `δ > 0`, so on `[0, 1)` we may integrate term-by-term: `∫₀^1 (1/(1+x))dx = Σ_{n≥0}(−1)ⁿ/(n+1) = Σ_{n≥1}(−1)^{n−1}/n` ✓. The left side is `ln(1+x)|₀^1 = ln 2` ✓. To make the exchange rigorous at the endpoint `x = 1`, integrate over `[0, 1−δ]` and let `δ → 0`: the difference between the two sides is at most `Σ_{n≥0} δⁿ/(n+1) ≤ Σ δⁿ = 1/(1−δ)` only for small `δ`; the sharper bound uses that the alternating tail of `Σ(−1)^{n+1}/n` is bounded by its first omitted term, so the remainder tends to 0. The series is conditionally convergent, since `Σ 1/n` diverges, and its sum is the alternating harmonic value `ln 2` ✓.
> **Key point:** Integrating `Σ(−x)ⁿ` term-by-term from `0` to `1` gives the alternating harmonic series `= ln 2`; convergence there is conditional, not absolute.

### Q167. Write the power series for `(1 + z)^{−1/2}` about `0`, give its radius of convergence, and identify the coefficient of `zⁿ`.

> **Type:** Numerical
> **Answer:** `(1+z)^{−1/2} = Σ_{n≥0} (−1)ⁿ C(2n, n) zⁿ/4ⁿ`, i.e. `1 − z/2 + 3z²/8 − 5z³/16 + ⋯`, with `R = 1`.
> **Solution:** The binomial series gives `(1+w)^{−1/2} = Σ C(−1/2, n)wⁿ` with `C(−1/2, n) = (−1)(−3)(−5)⋯(−(2n−1))/(2ⁿ n!) = (−1)ⁿ C(2n, n)/4ⁿ` ✓. Substituting `w = z`: coefficients are `1, −1/2, 3/8, −5/16, 35/128, ⋯` ✓. The radius is 1 because the nearest singularity of `(1+z)^{−1/2}` is the branch point at `z = −1`, exactly on `|z| = 1` ✓. The coefficients alternate in sign, alternate in decreasing magnitude like `1/√(πn)`, and go to zero, so by Q163-type reasoning the series converges on the circle wherever the alternating test applies, in particular at `z = 1` where the sum is `1/√2`.
> **Key point:** `(1+z)^{−1/2} = Σ (−1)ⁿ C(2n,n)zⁿ/4ⁿ` with `R = 1`; the coefficients behave like `(−1)ⁿ/√(πn)`.

### Q168. State the Laurent series theorem: existence, uniqueness, and the annulus of convergence.

> **Type:** Recall
> **Answer:** If `f` is analytic in the annulus `R₁ < |z − z₀| < R₂`, then it has a unique Laurent expansion `f(z) = \sum_{n=-\infty}^{\infty} a_n (z − z₀)^n` converging absolutely and uniformly on every closed sub-annulus `R₁ + \delta \le |z − z₀| \le R₂ − \delta`.
> **Solution:** The annulus is the region on which `f` is single-valued and analytic, and its limiting radii mark where analyticity fails; for a meromorphic `f` with isolated singularities these are the distances from `z₀` to the nearest and the next-nearest singularity, whereas in general the boundary can be a branch point, a natural boundary or a non-isolated singularity set, and then no Laurent series reaches it. Uniqueness follows by subtracting two expansions and applying the Laurent coefficient formula `a_n = (1/(2\pi i))∮ f(z)/(z − z₀)^{n+1}dz` around any circle inside the annulus, since the integral is independent of the radius by Cauchy's theorem (Q133, Q150). The expansion splits into a **principal part** `Σ_{n\ge1} a_{-n}(z − z₀)^{-n}` and an **analytic part** `Σ_{n\ge0} a_n(z − z₀)^n`. The principal part is empty when `f` is analytic at `z₀`, and its length is the order of the pole; a function with an essential singularity has an infinite principal part, and a function that is not single-valued on any punctured disc, such as `log z` at 0, has no Laurent series there at all rather than an empty principal part.
> **Key point:** A Laurent series is unique and converges on an annulus bounded by the nearest obstructions to analyticity; the principal part is empty for a removable singularity, finite for a pole, and a logarithm has no Laurent series at all.

### Q169. Determine all the Laurent expansions of `f(z) = 1/((z − 1)(z − 2))` about `z₀ = 0`, with the region of validity of each.

> **Type:** Numerical
> **Answer:** Three expansions, for `|z| < 1`, `1 < |z| < 2`, and `|z| > 2`.
> **Solution:** The poles are at `z = 1` and `z = 2`, so the annuli about 0 are cut at radii 1 and 2 ✓. Decompose `f = −1/(z−1) + 1/(z−2)` (partial fractions, since `−1/2 + 1/2 = 0` and `−(z−2) + (z−1) = 1` ✓). **(i) `|z| < 1`:** `1/(z−1) = −Σ zⁿ` and `1/(z−2) = −Σ zⁿ/2^{n+1}`, so `f = Σ_{n≥0}(1 − 2^{−(n+1)})zⁿ = 1/2 + 3z/4 + 7z²/8 + ⋯` ✓ (and `f(0) = 1/2` ✓). **(ii) `1 < |z| < 2`:** `−1/(z−1) = −Σ_{n≥1}z^{−n}` while `1/(z−2) = −Σ_{n≥0}zⁿ/2^{n+1}`, so `f = −(z⁻¹ + z⁻² + ⋯) − (1/2 + z/4 + z²/8 + ⋯)` ✓, a genuinely mixed series. **(iii) `|z| > 2`:** `−1/(z−1) = −Σ_{n≥1}z^{−n}` and `1/(z−2) = z⁻¹Σ_{n≥0}(2/z)ⁿ = Σ_{n≥0}2ⁿz^{−n−1}`, so the coefficient of `z^{−m}` is `2^{m−1} − 1`, giving `f = z⁻² + 3z⁻³ + 7z⁻⁴ + 15z⁻⁵ + ⋯` ✓ (the `z⁻¹` coefficient is `2⁰ − 1 = 0`). The three expansions are different functions of the same rational expression, each valid on its own annulus.
> **Key point:** One function about one centre has **one** Laurent expansion per annulus; the annuli are cut by the moduli of the singularities.

### Q170. Write the two Laurent expansions of `1/(z² − 1)` about `z₀ = 0` and compute the residue at `0` in each.

> **Type:** Numerical
> **Answer:** For `|z| < 1`: `−(1 + z² + z⁴ + ⋯)`. For `|z| > 1`: `(z⁻² + z⁻⁴ + z⁻⁶ + ⋯)`. The residue at 0 is `0` in both.
> **Solution:** **Inner annulus** `|z| < 1`: `1/(z²−1) = −(1/(1−z²)) = −Σ_{n≥0}z^{2n}` ✓, all non-negative powers, so the function is analytic at 0 and `Res(0) = 0` ✓ (indeed `f(0) = −1`). **Outer annulus** `|z| > 1`: `1/(z²−1) = z⁻²(1 − z⁻²)^{−1} = Σ_{n≥0}z^{−2n−2}` ✓, all non-positive powers, again with no `z⁻¹` term, so `Res(0) = 0` ✓. The two facts that the residue is zero in both annuli, and that the expansions have opposite sign patterns in the parity of their powers, are the two standard checks on this computation. By contrast, the coefficient of `z⁻¹` in the outer expansion of `1/(z²−4)` is also zero, so `∮_{|z|=3} dz/(z²−4) = 0` despite the pole at `z = 2` lying inside — the second pole's residue cancels it.
> **Key point:** `1/(z²−1) = −Σ z^{2n}` for `|z| < 1` and `= Σ z^{−2n−2}` for `|z| > 1`; the residue at 0 is 0 in both cases.

### Q171. Write the Laurent expansion of `f(z) = 1/((z − 1)(z + 2))` about `z₀ = 1` for `0 < |z − 1| < 3`, and identify the principal part and the residue at `z₀`.

> **Type:** Numerical
> **Answer:** `f(z) = (1/3)Σ_{n≥0}(−1)ⁿ(z−1)^{n−1}/3ⁿ = (1/3)(z−1)⁻¹ − 1/9 + (z−1)/27 − (z−1)²/81 + ⋯`, valid for `0 < |z−1| < 3`; the principal part is `1/(3(z−1))` and `Res(1) = 1/3`.
> **Solution:** With `w = z − 1`, `f = 1/(w(w+3)) = (1/(3w))·(1/(1 + w/3))`. The geometric series `1/(1+w/3) = Σ_{n≥0}(−w/3)ⁿ` requires `|w/3| < 1`, i.e. `|z−1| < 3`, matching the distance from `1` to the other pole at `−2` ✓. Multiplying, `f = (1/(3w))Σ_{n≥0}(−1)ⁿwⁿ/3ⁿ = (1/3)Σ_{n≥0}(−1)ⁿw^{n−1}/3ⁿ` ✓, giving the terms listed. Only the `n = 0` term is negative-power, so the principal part is `1/(3(z−1))` and the residue is `1/3` ✓, which matches the simple-pole rule `Res(1) = lim_{z→1}(z−1)/((z−1)(z+2)) = 1/3` ✓. The annulus is punctured because `z₀ = 1` is itself a pole.
> **Key point:** Factoring the pole and running a geometric series on the remaining analytic factor gives a Laurent series; the `w^{−1}` coefficient is the residue.

### Q172. State what can be said about convergence of a Laurent series on the two boundary circles of its annulus, and illustrate with `1/(z²−1)`.

> **Type:** Theory
> **Answer:** Nothing is implied: a Laurent series may converge everywhere on a boundary circle, at some of its points, or nowhere. For `1/(z²−1)` about 0, both `−Σz^{2n}` and `Σz^{−2n−2}` diverge at every point of `|z| = 1`, because their terms have modulus 1.
> **Solution:** The annular convergence theorem (Q168) only guarantees absolute, uniform convergence on strictly interior circles `R₁ + δ ≤ |z − z₀| ≤ R₂ − δ`; boundary behaviour is unconstrained, exactly as for a power series on its circle (Q163). For `1/(z²−1)`: on `|z| = 1` the terms of `−Σz^{2n}` have modulus 1, and so do the terms of `z⁻² + z⁻⁴ + ⋯`, so both series fail the term test at every point of the circle ✓. A contrasting series, `Σ_{n≥1} z^{−n}/n²`, does converge absolutely everywhere on `|z| = 1` by comparison with `Σ1/n²`, so the *same* annulus `|z| > 1` supports both a divergent and a convergent boundary behaviour depending only on the coefficients. Boundary behaviour must therefore be established series by series, never inferred from the annulus.
> **Key point:** Annular convergence guarantees nothing on `|z − z₀| = R₁` or `R₂`; `Σz^{−n}/n²` converges there while `Σz^{−n}` does not, for the same annulus.

### Q173. State the Cauchy-Hadamard formula for the two radii of a Laurent series and verify it for `1/(z^2 - 1)` about `z_0 = 0`.

> **Type:** Theory
> **Answer:** If `f(z) = \sum_{n\ge0} b_n z^n + \sum_{n\ge1} b_{-n} z^{-n}` on `R_1 < |z| < R_2`, then `1/R_2 = limsup_{n\to\infty}|b_n|^{1/n}` and `1/R_1 = limsup_{n\to\infty}|b_{-n}|^{1/n}`. For `1/(z^2-1)` both limits are 1, so `R_1 = R_2 = 1`.
> **Solution:** The positive-power and the negative-power parts of a Laurent series are each ordinary power series in `z` and in `1/z`, so Cauchy-Hadamard applies to them separately. Verification: the inner expansion `-\sum_{n\ge0}z^{2n}` has `b_0 = -1` and `b_{2k} = -1` for every `k \ge 1`, with all odd coefficients zero, so `limsup|b_n|^{1/n} = 1` and `R_2 = 1`. The outer expansion `\sum_{k\ge0}z^{-2k-2}` has `b_{-2k-2} = 1` and `b_{-1} = 0`, so `limsup|b_{-n}|^{1/n} = 1` and `R_1 = 1`. Both radii coincide with the moduli of the singularities `z = \pm 1`, which is the general principle: `R_1` and `R_2` are the distances from the centre to the nearest and the next-nearest singularity, and if the two are equal the annulus is empty, which is exactly the situation in which no Laurent series about that centre exists.
> **Key point:** `1/R_2 = limsup|b_n|^{1/n}` and `1/R_1 = limsup|b_{-n}|^{1/n}`; an annulus with `R_1 = R_2` is empty and admits no Laurent expansion about that centre.

### Q174. State Abel's theorem for power series and give an example where it fixes the value of a sum.

> **Type:** Theory
> **Answer:** If `∑ a_n z₀ⁿ` converges at a boundary point `z₀` with `|z₀| = R`, then the sum function is continuous there along the radius and `∑ a_n (ρz₀)^n \to ∑ a_n z₀ⁿ` as `ρ \to 1⁻`. For `∑ zⁿ/n = −log(1−z)` at `z₀ = −1` this gives the value `−ln 2`.
> **Solution:** Abel's theorem says the sum function of a power series is continuous at each point of its circle of convergence at which the series itself converges, so the value at a boundary point can be obtained as a radial limit from inside; writing the radial factor as `ρ = r/R` with `r \uparrow R` is the same statement, the limit parameter being `1` because the point is written as `ρz₀` with `z₀` already of modulus `R`. For `∑ zⁿ/n` the series at `z = −1` is `−1 + 1/2 − 1/3`, the alternating harmonic series, converging to `−\ln 2`, and Abel's theorem guarantees `lim_{ρ\to1^-}\sum (-\rho)^n/n = -\ln 2`, consistent with `−log(1+\rho)|_{\rho\to1} = -\ln 2`. The theorem is what licenses substituting boundary values into a power-series representation of a definite integral. It does not extend to points where the series diverges: at `z = 1` the sum `−log(1−r)` tends to `+\infty`, matching the divergence of the harmonic series rather than contradicting the theorem.
> **Key point:** Abel's theorem equates the sum at a boundary point of convergence with the radial limit `\lim_{\rho\to1^-}\sum a_n(\rho z₀)^n`; at `z = 1` for `\sum z^n/n` both the series and the radial limit diverge.

### Q175. `GATE-2` `MSQ` Which statements about series of analytic functions are correct? (A) A power series converges uniformly on every closed disc strictly inside its circle of convergence. (B) A locally uniform limit of analytic functions is analytic. (C) `∑ zⁿ` is uniformly convergent on `|z| \le 1`. (D) Cauchy's integral formula is valid for a function analytic on the contour but not inside it.

> **Type:** MCQ
> **Answer:** A and B only (Option b).
>
> (a) A, B and C
> (b) A and B only
> (c) A, B, C and D
> (d) B and C only
>
> **Solution:** (A) is the M-test: on `|z| \le r < R` the terms are bounded by `rⁿ`, and `Σ rⁿ` converges, so the convergence is uniform there. (B) is the uniform-limit theorem (Q153) with local uniformity, so it is true. (C) is false, since `sup_{|z|\le1}|zⁿ| = 1` for every `n`, so the necessary condition for uniform convergence fails, the terms not tending uniformly to zero (Q156). (D) is false: the formula requires `f` analytic on **and inside** `C`, and a pole strictly inside ruins it while leaving everything defined. Take `f(z) = 1/(z − 1/2)`, analytic on a neighbourhood of the unit circle and having its only pole at `1/2`. The residue theorem gives `∮_{|z|=1} f(z)dz = 2\pi i`, whereas the formula at `z₀ = 0` would give `f(0) = 1/(0 − 1/2) = −2`. The formula therefore fails in the most concrete way possible, and the pole, not the boundary behaviour, is the culprit. Hence the correct choice is A and B only.
> **Key point:** Uniform convergence holds on every disc strictly inside the radius, and locally uniform limits of analytic functions are analytic; `∑ zⁿ` is not uniform on `|z| \le 1`, and Cauchy's formula fails when a pole lies inside the contour.

## Section 9. Singularities, residues and the residue theorem

### Q176. Define an isolated singularity of `f` at `z₀` and give an example of a singularity that is **not** isolated.

> **Type:** Recall
> **Answer:** `z₀` is an isolated singularity if some punctured disc `0 < |z − z₀| < δ` contains no other singularity of `f`, i.e. `f` is analytic there. `z₀ = 0` of `f(z) = tan(1/z)` is **not** isolated, since `tan w` has poles at `w = π/2 + kπ`, so `f` has poles at `z = 1/(π/2 + kπ) → 0`.
> **Solution:** The definition requires a deleted neighbourhood on which `f` is analytic; the deleted neighbourhood must be a full disc, not just a sequence of approach directions. For `tan(1/z)`, setting `1/z = π/2 + kπ` gives `z = 1/(π/2 + kπ) = 2/((2k+1)π)`, which are genuine poles of `f` and which accumulate at `0` ✓. Hence every disc about `0` contains other singularities and no Laurent series about `0` exists. By contrast `sin(1/z)` is analytic on `0 < |z| < δ` for every `δ`, so `0` is an isolated essential singularity of it. The distinction matters because the classification into removable, pole and essential applies only to isolated singularities.
> **Key point:** Isolated means analytic on a full punctured disc; `tan(1/z)` at 0 is a limit point of poles, so it is non-isolated and admits no Laurent series.

### Q177. State the three types of isolated singularity and the criteria that distinguish them.

> **Type:** Recall
> **Answer:** For `f` analytic on `0 < |z − z₀| < δ`, the point `z₀` is removable if `lim_{z→z₀}(z − z₀)f(z) = 0`; a pole of order `m` if `lim_{z→z₀}(z − z₀)^m f(z)` is finite and nonzero (and `(z − z₀)^{m+1}f → 0`); essential if it is neither. Equivalently: removable ⟺ the principal part of the Laurent series is empty; pole of order `m` ⟺ it has `m` terms; essential ⟺ it has infinitely many.
> **Solution:** These are the only three possibilities, and the classification is exactly the length of the principal part `Σ_{n≥1}a₋ₙ(z−z₀)^{−n}` of the Laurent expansion. Boundedness detects the first case: `f` bounded in a punctured disc ⟺ `lim (z−z₀)f(z) = 0` ⟹ removable ✓, because `|(z−z₀)f(z)| ≤ M|z−z₀| → 0` for bounded `f`, and conversely `|(z−z₀)f(z)| < ε` bounds `f` away from the hole. Unboundedness splits into the pole and essential cases according to how fast `f` blows up. Every function analytic except at a finite set therefore has, at each such point, exactly one of these three behaviours, and the residue machinery of this section applies to the pole case.
> **Key point:** Removable ⟺ bounded ⟺ empty principal part; pole of order `m` ⟺ principal part of length `m`; essential ⟺ principal part infinite.

### Q178. Apply the criteria to classify the singularity of `f(z) = sin z / z` at `z = 0`, and of `g(z) = 1/z`.

> **Type:** Numerical
> **Answer:** `0` is removable for `f`, with extended value `1`; `0` is a simple pole for `g`.
> **Solution:** For `f`, `(z − z₀)f = z·(sin z/z) = sin z → 0`, the removable criterion ✓. The extended value is obtained from the series `sin z = z − z³/6 + ⋯`, so `sin z/z = 1 − z²/6 + ⋯ → 1` ✓. Note the value is **not** the limit of `(z−z₀)f(z)`, which is 0; the criterion only detects removability, and the value must be read off the series. For `g`, `z·(1/z) = 1 ≠ 0`, so the removable criterion fails, and `1/z = 1/(z − z₀)¹` has a principal part of one term, so `0` is a simple pole ✓. In particular `sin z/z` is *not* analytic at 0 until it is defined there, whereas `1/z` cannot be made analytic there by any definition.
> **Key point:** `lim(z−z₀)f(z) = 0` detects a removable singularity but does not give its value; for `sin z/z` that value is 1, while `1/z` gives `lim z·(1/z) = 1` and so is a simple pole.

### Q179. Classify `1/(z − 1)³` and `(z − 1)sin(1/(z − 1))²` at `z = 1`.

> **Type:** Numerical
> **Answer:** `1/(z − 1)³` has a pole of order 3; `(z−1)sin²(1/(z−1))` has a removable singularity with value 0.
> **Solution:** For the first, `(z−1)³f = 1 ≠ 0` and `(z−1)⁴f → 0`, so the order is exactly 3 ✓. For the second, put `w = 1/(z−1)`: `(z−1)sin²w = (sin²w)/w`, and since `sin²w = w² − w⁴/3 + ⋯`, this equals `w − w³/3 + ⋯ → 0` as `z → 1` ✓, the removable criterion, and the extended value is 0. The second example is the instructive one: the function oscillates infinitely often near `z = 1` and contains `sin` of a pole-like expression, yet the singularity is removable because the prefactor kills the blow-up. What matters is the behaviour of the whole expression, not the presence of a factor that looks like a pole.
> **Key point:** Pole of order 3 means `(z−z₀)³f → 1 ≠ 0`; `(z−1)sin²(1/(z−1)) = w − w³/3 + ⋯ → 0` is removable, so apparent oscillations do not by themselves create an essential singularity.

### Q180. Show that `e^{1/z}` has an essential singularity at `z = 0`, and list two other essential examples.

> **Type:** Theory
> **Answer:** `e^{1/z} = \sum_{n\ge0} z^{-n}/n!` has infinitely many negative powers, so `0` is essential. Other examples: `sin(1/z)` and `e^{1/z^2}`.
> **Solution:** The Laurent expansion of `e^{1/z}` is `1 + 1/z + 1/(2z²) + 1/(6z³) + 1/(24z⁴)`, whose principal part `Σ_{n\ge1} z^{-n}/n!` runs on for ever, so by Q177 an infinite principal part means an essential singularity. Equivalently, no limit of `e^{1/z}` as `z \to 0` exists: along `z = 1/n` the value is `eⁿ` and tends to `∞`, along `z = 1/(2\pi i n)` the value is 1, and along `z = 1/(i\pi(2n + 1))` the value is `−1`, three different behaviours along three approaches. For `sin(1/z)` the expansion `1/z − 1/(6z³) + 1/(120z⁵)` has infinitely many negative powers. For `e^{1/z²}` the expansion `1 + 1/z² + 1/(2z⁴) + 1/(6z⁶)` likewise has infinitely many negative powers. Both are therefore essential at 0. A caution about plausible-looking candidates: `1/(e^z − 1) + 1/z` is **not** an example, because `1/(e^z − 1) = 1/z − 1/2 + z/12 − z³/720` has a single negative-power term, so the sum has the simple pole `2/z` and no infinite principal part.
> **Key point:** An essential singularity is exactly an infinite principal part, as in `e^{1/z}`, `sin(1/z)` and `e^{1/z²}`; a function with only finitely many negative powers is at worst a pole.

### Q181. `GATE-2` State Big Picard's theorem, and explain why it makes the classification into removable singularity, pole and essential singularity exhaustive and mutually exclusive.

> **Type:** Recall
> **Answer:** In every punctured neighbourhood of an essential singularity, `f` takes every complex value with at most one exception infinitely often. Near a pole, by contrast, `|f|` exceeds every prescribed bound, so `f` omits a whole disc of finite values; the two behaviours are incompatible, and a bounded `f` is removable.
> **Solution:** Big Picard says that near an essential singularity the function is attained infinitely often, with at most one value omitted; for `e^{1/z}` the omitted value is 0, and 0 is indeed never attained since `e^{1/z} \ne 0` for every `z`. A pole of order `m` satisfies `|f(z)| \to \infty` as `z \to z₀`, so for a small enough punctured disc and any fixed `M` the estimate `|f| \ge |a_{-m}|/(2|z − z₀|^m) > M` holds; in particular `f` omits the entire disc `|w| \le M` of finite values, which is far more than the single value Big Picard allows an essential singularity to omit. The two behaviours therefore cannot occur at the same point, and since an isolated singularity that admits a finite limit is removable, the three cases are mutually exclusive and exhaustive. The companion result, Little Picard, says a non-polynomial entire function omits at most one value, with `e^z` omitting 0, the same phenomenon at infinity.
> **Key point:** Big Picard gives at most one omitted value near an essential singularity, whereas near a pole an entire disc of finite values is omitted; a finite limit makes the singularity removable, so the three types are exhaustive.

### Q182. `GATE-2` Classify the singularities: `f_1 = (z^2 - 1)/(z - 1)` at 1, `f_2 = 1/(z - 1)^2` at 1, `f_3 = e^{1/(z-1)}` at 1, `f_4 = sin z / z` at 0.

> **Type:** MCQ
> **Answer:** `f_1` removable with value 2, `f_2` a pole of order 2, `f_3` essential, `f_4` removable with value 1 (Option a).
>
> (a) removable, pole of order 2, essential, removable
> (b) simple pole, pole of order 2, essential, simple pole
> (c) removable, simple pole, essential, removable
> (d) essential, pole of order 2, removable, removable
>
> **Solution:** `f_1`: the common factor cancels, `f_1 = z + 1` for `z \ne 1`, so the point 1 is a removable singularity and the extended value is `1 + 1 = 2`. `f_2`: `(z-1)^2 f_2 = 1 \ne 0` while `(z-1)^3 f_2 \to 0`, so the pole is of order exactly 2. `f_3`: the expansion `\sum_{n\ge0}(z-1)^{-n}/n!` has infinitely many negative powers, so 1 is essential. `f_4`: `z f_4 = sin z \to 0`, the removable criterion, and `sin z/z = 1 - z^2/6 + z^4/120 - z^6/5040 + ` and so on gives the extended value 1. Option (b) misclassifies the two removable points, option (c) loses one order on `f_2`, and option (d) confuses `e^{1/(z-1)}` with the removable combination in `f_1`.
> **Key point:** Cancel common factors first, then read off the principal-part length: `f_1` and `f_4` removable, `f_2` pole of order 2, `f_3` essential.
### Q183. State Riemann's theorem on removable singularities and its equivalent formulation in terms of boundedness.

> **Type:** Theory
> **Answer:** If `f` is analytic on `0 < |z − z₀| < δ` and the Laurent expansion of `f` about `z₀` has no negative powers, then `z₀` is removable. Equivalently, `z₀` is removable if and only if `f` is bounded in some punctured neighbourhood of `z₀`.
> **Solution:** The Laurent series converges uniformly on every closed sub-annulus, so if the principal part is empty the sum is given by a power series in `z − z₀` that converges on the full disc `|z − z₀| < δ`, and defining `f(z₀)` to be its constant term makes `f` analytic at `z₀`. Boundedness is equivalent: if `|f| ≤ M` near `z₀`, the coefficients of the principal part satisfy `|a₋ₙ| ≤ M/Rⁿ → 0` as `R → δ` (Cauchy's estimate), forcing every `a₋ₙ = 0` ✓. The theorem is the reason `sin z/z`, `(z²−1)/(z−1)` and `z^{1/2}z^{-1/2}` can all be "filled in", whereas no choice of value can repair `1/z`, since that would contradict the derivative estimate.
> **Key point:** Empty principal part ⟺ bounded near `z₀` ⟺ removable; the equivalence follows from Cauchy's estimate `|a₋ₙ| ≤ M/Rⁿ`.

### Q184. Describe the local behaviour of a function with a pole of order `m` at `z₀`.

> **Type:** Theory
> **Answer:** `f(z) = a_{-m}/(z − z₀)^m` with lower-order terms and an analytic part `g`, `a_{-m} \ne 0`; hence `f \to \infty` in modulus like `|a_{-m}|/|z − z₀|^m`, with `|f(z)| \ge |a_{-m}|/(2|z − z₀|^m)` for small enough `|z − z₀|`.
> **Solution:** Only the leading term matters for the blow-up: `(z − z₀)^m f(z) \to a_{-m} \ne 0`, so for small `|z − z₀|` the remaining terms are bounded relative to the leading one, which gives `|f| \ge |a_{-m}|/(2|z − z₀|^m)` and `|f| \to \infty`. Consequences used later: the residue is precisely the coefficient `a_{-1}` of `(z − z₀)^{-1}`, and it is the only coefficient that a contour integral sees, since `∮_{|z − z₀| = \rho}(z − z₀)^{-k}dz` equals `2\pi i` when `k = 1` and 0 for every other integer `k`, the integral not depending on `\rho` at all. So the contour integral about a small circle is `2\pi i\,a_{-1}` whatever the order `m`, and in particular it does not vanish when `m = 1`. Also, the number of poles in a compact region is finite provided they do not accumulate, which follows from their being isolated.
> **Key point:** A pole of order `m` has `f = a_{-m}/(z−z₀)^m` with lower orders plus an analytic part; only the `(z−z₀)^{−1}` coefficient contributes to a contour integral, giving `2\pi i\,a_{-1}`.

### Q185. Explain why no Laurent series exists about `z₀ = 0` for `f(z) = tan(1/z)`, and contrast with `sin(1/z)`.

> **Type:** Conceptual
> **Answer:** `0` is a limit point of the poles of `tan(1/z)`, so it is a non-isolated singularity and Laurent's theorem does not apply. For `sin(1/z)`, `0` is isolated and the series `1/z − 1/(6z³) + ⋯` is a genuine Laurent series.
> **Solution:** The poles of `tan w` are at `w = π/2 + kπ`, so `f` has poles at `z_k = 1/(π/2 + kπ)`, and `|z_k| → 0` as `k → ∞` ✓. Every punctured disc `0 < |z| < δ` therefore contains poles of `f`, contradicting the hypothesis of the Laurent theorem, which requires analyticity on the whole punctured disc. Hence `0` is not classified as removable, pole or essential — those words do not apply. For `sin(1/z)`, `sin w` is entire, so `f` is analytic on `0 < |z| < δ` for every `δ`, and the composition of the series of `sin` with `1/z` gives the Laurent series `1/z − 1/(6z³) + 1/(120z⁵) − ⋯`, valid on every punctured disc, with an essential singularity at 0 ✓.
> **Key point:** An infinite principal part (essential) still allows a Laurent series; an accumulation of poles (non-isolated) does not.

### Q186. Define the residue at infinity and prove the relation `Σ_j Res(f, zⱼ) + Res(f, ∞) = 0`.

> **Type:** Theory
> **Answer:** `Res(f, ∞) = −(1/(2πi))∮_{|z| = R} f(z)dz` for `R` enclosing all finite singularities, and equivalently `Res(f, ∞) = −b₋₁` where `b₋₁` is the coefficient of `z⁻¹` in the expansion of `f` in powers of `1/z` valid for large `|z|`. Then `Σ_j Res(f, zⱼ) + Res(f, ∞) = 0`.
> **Solution:** By the residue theorem applied to the large circle, `∮_{|z|=R} f dz = 2πi Σ_j Res(f, zⱼ)`, so `Res(f,∞) = −Σ_j Res(f, zⱼ)`, which rearranges to the stated identity ✓. The expansion interpretation agrees: for large `z` a meromorphic function has `f(z) = b₋₁/z + b₋₂/z² + ⋯` only if it decays, and the coefficient of `1/z` is exactly the term the contour integral picks up, so negating gives `Res(f,∞) = −b₋₁` ✓. Check with `f = 1/z`: the finite residue at 0 is 1 and `Res(f,∞) = −1` ✓. The identity is why a rational function has vanishing total residue, and it converts "the integral over a huge circle" questions into finite algebra.
> **Key point:** `Res(f,∞) = −(1/(2πi))∮_{|z|=R}f dz = −`(coefficient of `z⁻¹` at infinity), and all residues including that one sum to zero.

### Q187. State the residue theorem, list its hypotheses, and contrast it with Cauchy's integral theorem.

> **Type:** Recall
> **Answer:** If `f` is meromorphic inside and on a simple closed contour `C` with no pole on `C`, then `∮_C f(z)dz = 2πi Σ_{zⱼ inside C} Res(f, zⱼ)`. Cauchy's integral theorem is the special case in which the sum is empty.
> **Solution:** The hypotheses are: `C` a simple closed piecewise-smooth contour; `f` meromorphic on a neighbourhood of `C` and its interior; and no pole on `C` itself (a pole on the contour makes the integral undefined, as in Q144). The theorem is proved by subtracting the principal parts: `f(z) = Σⱼ Σ_{k=1}^{mⱼ} a_{−k}^{(j)}/(z − zⱼ)^k + h(z)` with `h` analytic on and inside `C`, so by Cauchy's theorem `∮ h = 0` and each principal-part term is evaluated by the kernel formula, `∮ dz/(z−zⱼ)^k = 0` for `k ≥ 2` and `= 2πi` for `k = 1` — only the residue survives ✓. That last fact is why residues, and not the whole principal part, are the invariant of a pole.
> **Key point:** `∮_C f dz = 2πi Σ Res`; Cauchy's theorem is the pole-free case, and only the `1/(z−zⱼ)` term of each principal part survives the integral.

### Q188. State the residue formula for a simple pole and use it to compute the residues of `(z + 3)/((z - 1)(z + 2))` at both poles.

> **Type:** Numerical
> **Answer:** `Res(f, z_0) = lim_{z \to z_0}(z - z_0) f(z)`; here `Res(f, 1) = 4/3` and `Res(f, -2) = -1/3`.
> **Solution:** At the simple pole `z = 1`, cancelling the factor `(z-1)` gives `Res(f, 1) = (z+3)/(z+2)|_{z=1} = 4/3`. At the simple pole `z = -2`, cancelling `(z+2)` gives `Res(f, -2) = (z+3)/(z-1)|_{z=-2} = 1/(-3) = -1/3`. Consistency check: the two residues sum to `4/3 - 1/3 = 1`, so `Res(f, \infty) = -1`, matching the `1/z` term forced by the partial-fraction form `A/(z-1) + B/(z+2) = (A+B)/z + O(z^{-2})` with `A+B = 1` (Q186).
> **Key point:** `Res(f, z_0) = lim(z-z_0) f(z)`; for `(z+3)/((z-1)(z+2))` the residues are `4/3` and `-1/3`, summing to `1 = -Res(f, \infty)`.
### Q189. State the residue formula for a pole of order `m ≥ 2` and apply it to `e^z/(z − 1)²`.

> **Type:** Numerical
> **Answer:** `Res(f, z₀) = (1/(m−1)!)·(d^{m−1}/dz^{m−1})[(z − z₀)^m f(z)]|_{z=z₀}`. For `f = e^z/(z−1)²` with `m = 2`, `Res(1) = e`.
> **Solution:** The formula follows by expanding the analytic factor: writing `f = φ(z)/(z−z₀)^m` with `φ` analytic, the residue is the coefficient of `(z−z₀)^{−1}`, i.e. the coefficient of `(z−z₀)^{m−1}` in the Taylor series of `φ`, which is `φ^{(m−1)}(z₀)/(m−1)!` ✓. Applying it with `φ(z) = e^z`, `m = 2`: `Res(1) = φ′(1)/1! = e` ✓. Note that the pole is of order 2, so the answer is **not** `e^{−1}` — that would be the residue of `e^{1/z}`-type behaviour, a standard slip. A quick sanity check: `f = e^z/(z−1)² = e·e^{z−1}/(z−1)² = (e/(z−1)²) + (e/(z−1)) + (e/2 + ⋯)`, and the coefficient of `(z−1)^{−1}` is indeed `e` ✓.
> **Key point:** `Res = (1/(m−1)!)·(d^{m−1}/dz^{m−1})[(z−z₀)^m f]_{z₀}`; for `e^z/(z−1)²` it is `φ′(1) = e`, not `1/e`.

### Q190. State the Laurent-coefficient formula for the residue and explain why the residue is a local, not a global, invariant.

> **Type:** Theory
> **Answer:** `Res(f, z₀) = (1/(2πi))∮_{|z − z₀| = ρ} f(z)dz` for any `ρ` inside the isolated-singularity neighbourhood, and also `Res(f, z₀) = a₋₁`, the coefficient of `(z − z₀)^{−1}` in the Laurent series. It is local: it depends only on the principal part at `z₀`, not on `f` elsewhere.
> **Solution:** The formula holds for every `ρ` small enough, by the deformation theorem, since the region swept out is free of other singularities (Q133) ✓. Independence of `ρ` is exactly the local character: two functions agreeing on a punctured disc about `z₀` have the same residue there, even if they differ completely elsewhere. The principal-part statement makes the same point combinatorially — the residue is the single coefficient of the `(z−z₀)^{−1}` term, and the whole principal part of a pole of order `m` is determined by the derivatives of `φ` at `z₀`, where `φ(z) = (z−z₀)^m f(z)` (Q189). This locality is what allows a residue to be computed from a short local expansion even when the global picture is complicated.
> **Key point:** `Res(f, z₀) = (1/(2πi))∮_{|z−z₀|=ρ} f dz = a₋₁` for any admissible `ρ`; only the local principal part matters.

### Q191. State the residue of `1/P(z)` at a simple root of `P`, and apply it to `1/(z² + z + 1)`.

> **Type:** Numerical
> **Answer:** `Res(1/P, a) = 1/P′(a)` for a simple root `a`. The roots of `z² + z + 1` are `a± = (−1 ± i√3)/2`, with `Res(a±) = 1/(±i√3) = ∓i/√3`.
> **Solution:** The rule follows from the simple-pole formula, since `(z−a)/P(z) → 1/P′(a)` as `z → a` ✓. Here `P′(z) = 2z + 1`, so at `a+ = (−1+i√3)/2` we get `P′(a+) = i√3` and `Res = 1/(i√3) = -i/√3`; at `a- = (−1-i√3)/2` we get `P′(a-) = -i√3` and `Res = i/√3` ✓. The two residues are negatives of each other and sum to 0, which must hold because `1/(z²+z+1) = O(z^{-2})` at infinity, so `Res(f, ∞) = 0` (Q186). Both roots have modulus 1, so any contour `|z| = R` with `R > 1` encloses both and encloses zero total residue. A contour enclosing only `a+` — for instance the circle `|z − a+| = 1/2` — gives `2πi·(-i/√3) = 2π/√3`.
> **Key point:** `Res(1/P, a) = 1/P′(a)`; for `z² + z + 1` the residues are `-i/√3` and `+i/√3`, summing to zero.

### Q192. `GATE-2` Compute the residue of `1/(z(z − 1)²)` at `z = 1`, and the residue at `z = 0`.

> **Type:** Numerical
> **Answer:** `Res(1) = -1` and `Res(0) = 1`.
> **Solution:** At `z = 1` the pole is of order 2, so the derivative formula gives `Res(1) = d/dz[(z-1)^2 \cdot 1/(z(z-1)^2)]|_{z=1} = d/dz[1/z]|_{z=1} = -1`. At `z = 0` the pole is simple, so the simple-pole formula gives `Res(0) = lim_{z\to0} z \cdot 1/(z(z-1)^2) = 1/(z-1)^2|_{z=0} = 1`, since `(0-1)^2 = 1`. The two residues `-1` and `1` sum to 0, consistent with `f = O(z^{-3})` at infinity and `Res(f, \infty) = 0` (Q194).
> **Key point:** For `1/(z(z-1)^2)`, `Res(1) = -1` (order 2, derivative of `1/z`) and `Res(0) = 1` (simple pole, `1/(z-1)^2` at 0); they cancel.


### Q193. `GATE-2` `MSQ` Which of the following are essential singularities? (A) `e^{1/z}` at `z = 0`. (B) `sin(1/z)` at `z = 0`. (C) `tan(1/z)` at `z = 0`. (D) `1/(z − 1)` at `z = 0`.

> **Type:** MCQ
> **Answer:** A and B only (Option b).
>
> (a) A, B and C
> (b) A and B only
> (c) A, C and D
> (d) B and D only
>
> **Solution:** (A) `e^{1/z} = \sum_{n\ge0}z^{-n}/n!` has infinitely many negative powers, so it is essential. (B) `sin(1/z) = 1/z - 1/(6z^3) + 1/(120z^5) - 1/(5040z^7) + ` and so on likewise, so it is essential. (C) `tan(1/z)` has poles at `z = 2/((2k+1)\pi)` accumulating at 0, so 0 is a **non-isolated** singularity, and the words removable, pole and essential do not apply. (D) `1/(z-1)` is analytic at `z = 0` because 0 is not a singularity of it at all. Hence only A and B are essential, and the correct option is (b).
> **Key point:** `e^{1/z}` and `sin(1/z)` are essential at 0; `tan(1/z)` is non-isolated there, and `1/(z-1)` has no singularity at 0.

### Q194. `GATE-2` Show that the sum of the residues of a rational function, including the residue at infinity, is 0, and evaluate the residue at infinity of `2/z^3 + 1/z`.

> **Type:** Numerical
> **Answer:** `Res(f, \infty) = -\sum_{finite} Res(f, z_j)`, so the total over all poles is 0. For `f = 2/z^3 + 1/z` the only finite pole is at 0 with residue 1, and `Res(f, \infty) = -1`.
> **Solution:** A rational function has finitely many poles, and its expansion at infinity is a genuine Laurent series in `1/z`. Since `Res(f, \infty)` is minus the `z^{-1}` coefficient of that expansion, and the sum of the finite residues is `2\pi i`-normalised the same way, the two must be opposites. Directly: writing `f(z) = P(z)/Q(z)` and integrating over a large circle, `∮_{|z|=R} f(z)dz = 2\pi i\big(\sum_{finite} Res(f, z_j) + Res(f, \infty)\big)`, and the left-hand side is `O(R^{1-k})` when `f = O(z^{-k})`, so it vanishes as `R \to \infty` and the bracket is 0. The useful special case is when `f` vanishes at infinity with `f = O(z^{-2})`; then the `z^{-1}` coefficient of the expansion is itself 0, so `Res(f,\infty) = 0` and the finite residues sum to 0 on their own. This hypothesis is not automatic: for `f = 2/z^3 + 1/z` the residue at 0 is 1, since the `2/z^3` term contributes no `z^{-1}` coefficient, so the finite sum is 1 rather than 0, and the cancellation happens only at infinity, where the `z^{-1}` coefficient of `2/z^3 + 1/z` is 1 and `Res(f, \infty) = -1` ✓.
> **Key point:** The total over all poles, infinity included, is 0, and `Res(f, \infty)` is minus the `z^{-1}` coefficient at infinity; the finite residues alone sum to 0 only when `f = O(z^{-2})`, which fails for `2/z^3 + 1/z`.

### Q195. `GATE-1` Evaluate `\oint_{|z| = 3} dz/(z^5 - 1)`.

> **Type:** MCQ
> **Answer:** `0` (Option c).
>
> (a) `2\pi i`
> (b) `2\pi i/5`
> (c) `0`
> (d) `-2\pi i`
>
> **Solution:** The five roots of `z^5 = 1` are `a_k = e^{2\pi i k/5}`, `k = 0, 1, 2, 3, 4`, all of modulus 1, so all five lie inside `|z| = 3` and none lies on the contour. Each is a simple pole with `Res(a_k) = 1/(5a_k^4) = a_k/5`, using `a_k^5 = 1`. Therefore `\sum_k Res = (1/5)\sum_k a_k = 0`, because the coefficient of `z^4` in `z^5 - 1` is zero and hence the sum of the roots is zero ✓. So `\oint = 2\pi i \cdot 0 = 0`. Option (a) is the trap of taking one pole's worth of `2\pi i`; option (b) is the trap of summing residues without the factor `(1/5)` correct per root. The general rule being used: a rational function proper enough to decay like `z^{-2}` or faster has zero total residue, so its integral over **any** contour enclosing all poles vanishes.
> **Key point:** All five poles of `1/(z^5-1)` are inside `|z| = 3` and their residues `a_k/5` sum to `0`, so the integral is 0.

### Q196. Compute the residues of `csc z` at its poles, and evaluate `∮_C tan z dz` where `C` is the square with vertices `1+i`, `1−i`, `−1−i`, `−1+i`.

> **Type:** Numerical
> **Answer:** `Res(csc, kπ) = (−1)^k`. The square `|Re z| ≤ 1`, `|Im z| ≤ 1` encloses no pole of `tan z`, so `∮_C tan z dz = 0`.
> **Solution:** The poles of `csc z = 1/sin z` are the zeros of `sin`, namely `z = kπ`, all simple, and the simple-pole formula gives `Res = 1/cos(kπ) = 1/(−1)^k = (−1)^k` ✓. For `tan z = sin z/cos z` the poles are `z = π/2 + kπ`, and at each one `Res = sin(z₀)/cos′(z₀) = sin(z₀)/(−sin(z₀)) = −1`, the same value at every pole ✓. The nearest poles to the origin are `±π/2`, of modulus `π/2 ≈ 1.5708`, and the square's boundary lines are `Re z = ±1` and `Im z = ±1`, so every pole of `tan z` lies outside the square. Since `tan z` is analytic on and inside `C`, Cauchy's integral theorem gives `∮_C tan z dz = 0` ✓. A contour that did enclose one pole, such as the square with vertices `2+2i`, `2−2i`, `−2−2i`, `−2+2i`, would instead give `2πi·(−1) = −2πi`.
> **Key point:** `Res(csc, kπ) = (−1)^k` and `Res(tan, π/2 + kπ) = −1`; since `π/2 > 1` the square `|x| ≤ 1`, `|y| ≤ 1` encloses no pole, so the integral is 0.

### Q197. Compute the residues of `1/cosh z` at `z = iπ(2k+1)/2`, and evaluate `∮_C dz/cosh z` for the circle `|z| = 1`.

> **Type:** Numerical
> **Answer:** `Res(1/cosh, z₀) = 1/sinh z₀`; the poles are `z₀ = iπ(2k+1)/2`. The circle `|z| = 1` contains none of them (the nearest has modulus `π/2 ≈ 1.571`), so the integral is `0`.
> **Solution:** `cosh z = 0` at `z = iπ(k + 1/2)`, all simple zeros, and the simple-pole rule gives `Res = 1/sinh(z₀)` ✓. Explicitly at `z₀ = iπ/2`, `sinh(iπ/2) = i sin(π/2) = i`, so `Res = 1/i = −i`; at `z₀ = −iπ/2`, `Res = i`. Every pole has modulus `π(2k+1)/2 ≥ π/2 ≈ 1.5708`, so none lies inside `|z| = 1`, and Cauchy's theorem gives `0` ✓. This is the standard trap in this family of questions: the first pole is at modulus 1.57, uncomfortably close to 1, and choosing the radius carelessly changes the answer. For comparison, `|z| = 2` would enclose `±iπ/2` with residues `−i` and `i` summing to 0, so the integral over `|z| = 2` is also 0.
> **Key point:** Poles of `1/cosh z` are at `iπ(k+1/2)` with residues `1/sinh z₀`, of modulus `≥ π/2`; for `|z| = 1` the answer is 0.

### Q198. Compute the residue of `1/(z sin z)` at `z = 0` and at `z = k\pi` for a non-zero integer `k`.

> **Type:** Numerical
> **Answer:** `Res(0) = 0`, and `Res(k\pi) = (-1)^k/(k\pi)` for `k \ne 0`.
> **Solution:** At `z = 0` the pole is of order 2, since `z sin z = z^2 - z^4/6 + z^6/120 -` and so on. Factoring gives `1/(z sin z) = z^{-2}(1 + z^2/6 + 7z^4/360 +` and so on `)`, and the parenthesised factor is an even power series in `z`, so the whole Laurent series contains only even powers: `z^{-2}, z^0, z^2,` and so on. There is no `z^{-1}` term, and the residue at 0 is 0. Parity gives the same conclusion immediately, since `1/(z sin z)` is an even function of `z` and an even Laurent series has all odd coefficients zero. At `z = k\pi` with `k \ne 0` the pole is simple, and `Res = 1/(z_0 \cos z_0) = 1/(k\pi(-1)^k) = (-1)^k/(k\pi)`. This is the clearest illustration that a pole of order `m` need not have a nonzero residue: the pole at 0 has order 2 and residue 0, so it contributes nothing to any contour integral.
> **Key point:** `1/(z sin z)` is even, so the order-2 pole at 0 has residue 0; at `k\pi \ne 0` the residue is `(-1)^k/(k\pi)`, so a pole may contribute nothing to `\oint`.


### Q199. Compute the residues of `1/(e^z - 1)` at all its poles, and classify `z_0 = 0` for this function.

> **Type:** Numerical
> **Answer:** All poles are `z = 2\pi i k` and every residue is 1. At `z_0 = 0` the function has a simple pole, not an essential singularity.
> **Solution:** The zeros of `e^z − 1` are `z = 2\pi i k` for `k \in \mathbb{Z}`, and all are simple because the derivative `e^z` equals 1 at each of them; the simple-pole formula gives `Res = 1/e^{2\pi i k} = 1` at every pole. Near 0 the expansion `e^z − 1 = z(1 + z/2 + z^2/6 + z^3/24 + z^4/120)` yields `1/(e^z − 1) = z^{-1} − 1/2 + z/12 − z^3/720 + z^5/30240`, whose principal part is the single term `z^{-1}`. So 0 is a simple pole of residue 1 even though the function is unbounded there, which is a corrective to the widespread impression that the exponential makes every such point essential: essentiality needs an infinite principal part, and here there is exactly one negative-power term. A related trap reinforces the point: `1/(e^{1/z} − 1)` is **not** essential at 0, because `1/(e^w − 1) = w^{-1} − 1/2 + w/12 − w^3/720` becomes `z − 1/2 + z/12 − z^3/720` on putting `w = 1/z`, which is analytic at 0. A genuine essential example from the same ingredient is `e^{1/z}`, whose principal part has infinitely many terms.
> **Key point:** Every pole of `1/(e^z − 1)` has residue 1, and 0 is a simple pole of it; essentiality needs an infinite principal part, which neither this function nor `1/(e^{1/z} − 1)` has.

### Q200. `GATE-2` `MSQ` Which statements about residues are correct? (A) A pole of order `m` may have residue 0. (B) `Res(f, \infty) = -\sum_j Res(f, z_j)`. (C) If `C` passes through a pole, `\oint_C f(z)dz = 2\pi i Res(f, z_j)`. (D) The residue of `1/(z - z_0)^2` is 1.

> **Type:** MCQ
> **Answer:** A and B only (Option b).
>
> (a) A, B and C
> (b) A and B only
> (c) A, B and D
> (d) B, C and D
>
> **Solution:** (A) is true, since `1/(z sin z)` has a pole of order 2 at 0 with residue 0 (Q198), the function being even. (B) is true, being the identity of Q186, checked for `f = 1/z` as `Res(f,\infty) = -1 = -Res(f,0)`. (C) is false: a pole on the contour makes the integral undefined rather than equal to `2\pi i` times the residue (Q144). (D) is false: the Laurent expansion of `1/(z-z_0)^2` is the single term `(z-z_0)^{-2}`, with no `(z-z_0)^{-1}` term, so the residue is 0, and indeed `\oint 1/(z-z_0)^2 dz = 0` about every circle. Hence only A and B are correct.
> **Key point:** Residues may vanish at higher-order poles, the sum of all residues including `Res(f,\infty)` is 0, and a pole on the contour invalidates the integral instead of contributing `2\pi i`.

### Q201. Compute the residues of `z^2/(z^2 - 1)^2` at `z = 1` and at `z = -1`.

> **Type:** Numerical
> **Answer:** `Res(1) = 1/4` and `Res(-1) = -1/4`.
> **Solution:** Both points are double poles. At `z = 1`, `(z-1)^2 f = z^2/(z+1)^2`, so `Res(1) = d/dz[z^2 (z+1)^{-2}]|_{z=1}`. Differentiating, `d/dz[z^2 (z+1)^{-2}] = 2z (z+1)^{-2} - 2z^2 (z+1)^{-3} = [2z(z+1) - 2z^2]/(z+1)^3 = 2z/(z+1)^3`, which at `z = 1` is `2/8 = 1/4`. At `z = -1`, `(z+1)^2 f = z^2/(z-1)^2`, and `d/dz[z^2 (z-1)^{-2}] = 2z (z-1)^{-2} - 2z^2 (z-1)^{-3} = [2z(z-1) - 2z^2]/(z-1)^3 = -2z/(z-1)^3`, which at `z = -1` is `2/(-8) = -1/4`. The two residues sum to 0, as required because `f = O(z^{-2})` at infinity, so `Res(f, \infty) = 0` (Q194).
> **Key point:** For `z^2/(z^2-1)^2` the residues are `1/4` at 1 and `-1/4` at -1, from the derivatives `2z/(z+1)^3` and `-2z/(z-1)^3`; they sum to 0.

### Q202. `GATE-2` Evaluate `\oint_{|z| = 2} dz/(z^3 - 1)`.

> **Type:** MCQ
> **Answer:** `0` (Option a).
>
> (a) `0`
> (b) `2\pi i`
> (c) `2\pi i/3`
> (d) `-2\pi i`
>
> **Solution:** The roots of `z^3 = 1` are `1`, `\omega = e^{2\pi i/3}` and `\omega^2 = e^{4\pi i/3}`, all of modulus 1, so all three lie inside `|z| = 2` and none lies on the contour. At a root `a`, `Res = 1/(3a^2) = a/3`, using `a^3 = 1`, so `Res(1) = 1/3` and `Res(\omega) = \omega/3`, `Res(\omega^2) = \omega^2/3`. Summing, `\sum Res = (1 + \omega + \omega^2)/3 = 0`, since the roots of `z^3 - 1` sum to zero. Hence the integral is 0. Option (b) is the trap of one `2\pi i` for "a pole inside", and option (c) is the trap of averaging the three residues. Confirming independently: `1/(z^3-1) = z^{-3}(1 - z^{-3})^{-1}` expands as `z^{-3} + z^{-6} + z^{-9} +` and so on for `|z| > 1`, with no `z^{-1}` term, so the total enclosed residue is 0.
> **Key point:** All three poles of `1/(z^3-1)` lie inside `|z| = 2`, but their residues `a/3` sum to 0, so the integral vanishes.

### Q203. `GATE-1` Evaluate `\oint_{|z| = 2} z^2 dz/(z^3 - 1)` and contrast it with Q202.

> **Type:** MCQ
> **Answer:** `2\pi i` (Option b).
>
> (a) `0`
> (b) `2\pi i`
> (c) `2\pi i/3`
> (d) `4\pi i`
>
> **Solution:** The poles are the same three cube roots of unity, all inside `|z| = 2`. At a root `a`, `Res = lim_{z \to a}(z-a) z^2/(z^3-1) = a^2/(3a^2) = 1/3`, since `z^3-1 = (z-a)(z^2+az+a^2)` and `z^2+az+a^2` takes the value `3a^2` at `z = a`. So the three residues sum to 1 and the integral is `2\pi i`. The contrast with Q202 is the whole lesson: the two integrands have the same three poles in the same places, but `1/(z^3-1) = O(z^{-3})` has residues summing to 0 while `z^2/(z^3-1) = O(z^{-1})` has residues summing to 1. Equivalently `z^2/(z^3-1)` has a `1/z` term at infinity, so `Res(f,\infty) = -1` and the finite residues must total 1. The sum of residues is controlled by the behaviour at infinity, not by the number of poles.
> **Key point:** `Res(z^2/(z^3-1), a) = 1/3` at each cube root of unity, so the sum is 1 and `\oint = 2\pi i`; the decay at infinity decides the sum, not the pole count.

### Q204. `GATE-2` Evaluate `\oint_{|z| = 2} e^{1/(z - 1)} dz`, noting that `z = 1` is an essential singularity.

> **Type:** Numerical
> **Answer:** `2\pi i`.
> **Solution:** The integrand has an isolated essential singularity at `z = 1` and is analytic elsewhere, so the residue theorem applies and the integral is `2\pi i` times the residue at 1. Writing `w = z - 1`, the function is `e^{1/w} = \sum_{n\ge0} w^{-n}/n!`, whose `w^{-1}` coefficient is the term `n = 1`, namely `1/1! = 1`, so `Res(f, 1) = 1` and the integral is `2\pi i`. Essentiality is no obstacle, because only the single `w^{-1}` coefficient of the infinite principal part contributes and every higher negative power integrates to zero on the circle. This is the cleanest demonstration that a residue is defined at an essential singularity exactly as at a pole. A confirming computation: with `z = 1 + 2e^{i\theta}` the integral becomes `i\int_0^{2\pi} e^{e^{-i\theta}/2}d\theta`, and the mean of an analytic function over a circle centred at the origin is its constant term, here `1`, giving `2\pi i`.
> **Key point:** A residue exists at an essential singularity: for `e^{1/(z-1)}` the `w^{-1}` coefficient of `\sum w^{-n}/n!` is 1, so the integral is `2\pi i`.


## Section 10. Applications of contour integration and the residue theorem

### Q205. `GATE-2` Evaluate `∫_{−∞}^{∞} dx/(x² + 1)` by integrating `1/(z² + 1)` over a semicircular contour in the upper half-plane.

> **Type:** Numerical
> **Answer:** `π`.
> **Solution:** Take the contour made of the segment `[-R, R]` on the real axis and the upper semicircle `|z| = R`, traversed counterclockwise. The poles of `1/(z²+1)` are `±i`, and for `R > 1` the only one enclosed is the upper one `z = i`; its residue is `1/(2i)`, so the total contour integral is `2\pi i\cdot(1/(2i)) = \pi`. On the arc, `|z^2 + 1| \ge R^2 - 1`, so the arc contribution has modulus at most `\pi R/(R^2 - 1)`, which tends to 0 as `R \to \infty`. Hence the real-axis part tends to `∫_{−\infty}^{\infty}dx/(x^2+1) = \pi`, and by evenness the half-line integral is `\pi/2`. The estimate on the arc is the essential step: without it one cannot pass to the limit, and the bound `\pi R/(R^2 - 1)` is the concrete form of the principle that the arc at infinity contributes nothing, which every such evaluation must establish.
> **Key point:** For `1/(z^2+1)` on the upper semicircle the arc contributes at most `\pi R/(R^2-1) \to 0`, and the residue `1/(2i)` at the enclosed pole `z = i` gives `\int_{-\infty}^{\infty} dx/(x^2+1) = \pi`.

### Q206. `GATE-2` Evaluate `∫_{−∞}^{∞} dx/(x² + 2x + 5)`.

> **Type:** Numerical
> **Answer:** `π/2`.
> **Solution:** Complete the square: `x^2 + 2x + 5 = (x+1)^2 + 4`, so the integral is `∫_{−\infty}^{\infty}dx/((x+1)^2 + 2^2)`, which by the shift `u = x+1` is the standard integral of Q205 with `a = 2`, giving `\pi/2`. The residue route agrees: the poles are `z = -1 \pm 2i`, the upper one is `z = -1 + 2i`, and the denominator's derivative is `2z + 2 = 4i` there, so the residue is `1/(4i)` and the semicircular contour gives `2\pi i\cdot(1/(4i)) = \pi/2`. The horizontal position of the pole is irrelevant, since the residue theorem counts a pole wherever it lies as long as only the upper half-plane is closed off. In general, for `x^2 + ax + b` with `a^2 < 4b` the poles are `-a/2 \pm i\sqrt{4b - a^2}/2`, the residue of the upper pole is `1/\sqrt{4b - a^2}`, and the integral is `\pi/\sqrt{4b - a^2}`; the condition `a^2 < 4b` is what makes the poles non-real and the contour argument available.
> **Key point:** `\int_{-\infty}^{\infty} dx/(x^2+2x+5) = \pi/2`; completing the square or closing in the upper half-plane at the pole `-1+2i` with residue `1/(4i)` both give it.

### Q207. `GATE-2` Evaluate `∫_{−∞}^{∞} dx/(x⁴ + 1)`.

> **Type:** Numerical
> **Answer:** `π/√2 = π√2/2`.
> **Solution:** Close in the upper half-plane, where the four roots of `z⁴ = −1` are `z_k = e^{i(2k+1)\pi/4}`, `k = 0, 1, 2, 3`; those with positive imaginary part are `e^{i\pi/4} = (1+i)/\sqrt2` and `e^{3i\pi/4} = (-1+i)/\sqrt2`. At a root `a`, `Res = 1/(4a³)`. Since `a⁴ = -1`, we have `1/(4a³) = -a/4`. So `Res(e^{i\pi/4}) = -(1+i)/(4\sqrt2)` and `Res(e^{3i\pi/4}) = -(-1+i)/(4\sqrt2) = (1-i)/(4\sqrt2)`, whose sum is `[-(1+i) + (1-i)]/(4\sqrt2) = -2i/(4\sqrt2) = -i/(2\sqrt2)`. Multiplying, the integral is `2\pi i \cdot (-i/(2\sqrt2)) = \pi/\sqrt2` ✓. The arc contribution vanishes because `|z^4 + 1| \ge R^4 - 1` there, giving an arc bound `2\pi R/(R^4-1) \to 0`. This is the cleanest demonstration of why the "upper half-plane" rule needs a symmetry argument: the two residues do not combine into a real number term by term, only in sum.
> **Key point:** Closing in the upper half-plane, the two enclosed poles contribute `-i/(2\sqrt2)`, giving `\int_{-\infty}^{\infty}dx/(x^4+1) = \pi/\sqrt2`.

### Q208. `GATE-2` `NAT` Evaluate `∫_{0}^{∞} x^2 dx/(x^4 + 1)` using the substitution `x = 1/t` and the result of Q207.

> **Type:** Numerical
> **Answer:** `π/(2√2)`.
> **Solution:** Put `x = 1/t`, so `dx = -dt/t^2` and `∫_0^\infty x^2/(x^4+1)dx = ∫_0^\infty dt/(1+t^4)`, the bounds `0 \to \infty` and `\infty \to 0` swapping together with the sign. So the half-line integral with numerator `x^2` equals the one with numerator `1`. By Q207 the full-line integral of `1/(x^4+1)` is `\pi/\sqrt2`, and by evenness the half-line integral is `\pi/(2\sqrt2)`, which is therefore the requested value. Confirming with residues directly on `z^2/(z^4+1)`: the residue at a root `a` is `a^2/(4a^3) = 1/(4a)`, and since `|a| = 1` on the unit circle we have `1/a = \bar a`, so the two upper-half-plane residues are `e^{-i\pi/4}/4` and `e^{-3i\pi/4}/4`. Their sum is `[(1 - i) + (-1 - i)]/(4\sqrt2) = -i/(2\sqrt2)`, and `2\pi i\cdot(-i/(2\sqrt2)) = \pi/\sqrt2`, whose half is again `\pi/(2\sqrt2)` ✓. A magnitude check: the integrand is `x^2` near 0, contributes most of its mass for `x` of order 1, and decays like `x^{-2}`, so a value near 1.11 is reasonable.
> **Key point:** `x = 1/t` maps `∫_0^\infty x^2/(x^4+1)dx` to `∫_0^\infty dx/(x^4+1)`, so both equal `\pi/(2\sqrt2)`, half of the full-line value `\pi/\sqrt2`.

### Q209. `GATE-2` Evaluate `∫_{0}^{∞} sin x / x dx` by residues, and state the value of `∫_{−∞}^{∞} sin x / x dx`.

> **Type:** Numerical
> **Answer:** `π/2` for the half-line integral, and `π` for the full-line integral.
> **Solution:** The integrand is not meromorphic, so one introduces the exponential `e^{iaz}` with `a > 0` and closes the upper half-plane, where the factor `e^{iaz} = e^{iax - ay}` decays. The only pole of `e^{iaz}/z` is at `z = 0` with residue 1, but it sits **on** the real axis, so the contour is indented around it by a small semicircle in the upper half-plane and the statement is made in the principal-value sense. The indented arc contributes `i\pi` times the residue, so `PV∫_{−\infty}^{\infty}e^{iax}/x\,dx = i\pi`, not `2\pi i`: half the residue is all that a pole on the contour contributes. Taking imaginary parts, `∫_{−\infty}^{\infty}\sin(ax)/x\,dx = \pi`, since the real part `PV∫\cos(ax)/x\,dx` vanishes by oddness. With `a = 1` and `sin x/x` even, `∫_0^\infty \sin x/x\,dx = \pi/2`. A damping argument confirms the value without any contour: set `F(a) = \int_0^\infty e^{-ax}\sin x/x\,dx`, so `F'(a) = -\int_0^\infty e^{-ax}\sin x\,dx = -1/(1+a^2)` and `F(\infty) = 0`, whence `F(a) = \arctan(1/a)` and `F(0) = \pi/2`. The pole at the origin and the resulting principal value are exactly why this question is harder than Q205.
> **Key point:** `\int_0^\infty \sin x/x\,dx = \pi/2` and `\int_{-\infty}^{\infty}\sin x/x\,dx = \pi`; a pole on the real axis yields `i\pi` times its residue in the principal value, not `2\pi i`.

### Q210. `GATE-2` Evaluate `∫_{0}^{2π} dθ/(a + b\cos θ)` for real `a > b > 0`.

> **Type:** Numerical
> **Answer:** `2π/√(a^2 - b^2)`.
> **Solution:** Substitute `z = e^{i\theta}`, so that `d\theta = dz/(iz)` and `\cos\theta = (z + z^{-1})/2`, and the unit circle is traversed counterclockwise. Then `a + b\cos\theta = (bz^2 + 2az + b)/(2z)`, and the integral becomes `I = (2/i)∮_{|z|=1} dz/(bz^2 + 2az + b)`. The quadratic has real roots `z_\pm = (-a \pm \sqrt{a^2-b^2})/b`; with `a > b > 0` one finds `-1 < z_+ < 0` and `z_- < -1`, so exactly one root, `z_+`, lies inside the unit circle. Its residue in `1/(bz^2+2az+b)` is `1/(2bz_+ + 2a) = 1/(2\sqrt{a^2-b^2})`, since `2bz_+ + 2a = 2\sqrt{a^2-b^2}`. Therefore `I = (2/i)(2\pi i)\cdot 1/(2\sqrt{a^2-b^2}) = 4\pi/(2\sqrt{a^2-b^2}) = 2\pi/\sqrt{a^2-b^2}`. As a check, at `b = 0` the formula gives `2\pi/a`, which is the correct value of `∫_0^{2\pi}d\theta/a`.
> **Key point:** The `z = e^{i\theta}` substitution gives a prefactor `2/i`, and the single root of `bz^2+2az+b` inside the unit circle yields `∫_0^{2\pi}d\theta/(a+b\cos\theta) = 2\pi/\sqrt{a^2-b^2}`.

### Q211. `GATE-2` `MSQ` Which statements about the inverse Z-transform and contour integration are correct? (A) If `X(z) = \sum_{n\ge0} x[n]z^{-n}` has a region of convergence containing a circle, then `x[n] = (1/(2\pi i))\oint X(z)z^{n-1}dz` when the contour is a circle inside the region of convergence. (B) The same formula holds for any contour in the plane. (C) The residues of the integrand `X(z)z^{n-1}` are what give the coefficients. (D) The region of convergence of a rational `X(z)` is always the exterior of a circle.

> **Type:** MCQ
> **Answer:** A and C only (Option b).
>
> (a) A, B and C
> (b) A and C only
> (c) A, B, C and D
> (d) B and D only
>
> **Solution:** (A) is true: it is Cauchy's formula applied to the Laurent expansion `X(z) = \sum_k x[k]z^{-k}` about 0, since only the term with `k = n` has a `z^{-1}` factor in `X(z)z^{n-1}` and so contributes to the integral. (B) is false: the contour must lie inside the region of convergence, so dragging it across a pole of `X` sweeps up a residue and changes the answer. (C) is true: by the residue theorem the integral is `2\pi i` times the sum of the residues of `X(z)z^{n-1}`, which is the standard computational route for a rational `X` (Q213, Q214). (D) is false, and Q223 is a single counterexample: `X(z) = z^2/((z-1)(z-2))` has the three regions of convergence `|z| > 2`, `1 < |z| < 2` and `|z| < 1`, so the region of convergence of a rational function is an annulus whose boundaries are determined by the poles, and only a right-sided sequence gives a plain exterior. Hence A and C only.
> **Key point:** The inverse Z-transform is a Cauchy integral, or a residue sum, inside the region of convergence; the contour cannot cross a pole, and the region of convergence of a rational function may be any annulus, not only an exterior.

### Q212. `GATE-2` Find the inverse Z-transform of `X(z) = z/(z − a)` with `|a| < 1`, in the region of convergence `|z| > |a|`.

> **Type:** Numerical
> **Answer:** `x[n] = a^n u[n]`.
> **Solution:** Writing `X(z) = 1/(1 − az^{-1})` and using the geometric series `1/(1 − w) = \sum_{n\ge0}w^n` with `w = az^{-1}`, which is valid when `|a/z| < 1`, that is `|z| > |a|`, gives `X(z) = \sum_{n\ge0}a^nz^{-n}`. Comparing with `X(z) = \sum_n x[n]z^{-n}` term by term, `x[n] = a^n` for `n \ge 0` and 0 otherwise, i.e. `x[n] = a^n u[n]`. The contour route agrees, with a point worth making carefully. The integrand is `X(z)z^{n-1} = z^n/(z−a)`, and the contour is a circle of radius greater than `|a|`, which is what the region of convergence dictates. For `n \ge 0` the function `z^n` is entire, so the only enclosed pole is `z = a` and the residue is `a^n`, giving `x[n] = a^n`. For `n = -m < 0` the integrand `z^{-m}/(z−a)` has **two** enclosed poles, at `z = 0` and at `z = a`, and they cancel: the residue at `a` is `a^{-m}`, while at 0 the expansion `1/(z - a) = -\sum_{k\ge0} z^k/a^{k+1}` contributes the `z^{-1}` term `-\sum  z^{k - m}/a^{k+1}` with `k = m - 1`, giving `-a^{-m}`. The sum is 0, so `x[n] = 0` for `n < 0`, as required. The region `|z| > |a|` is what makes the sequence causal; the same algebraic expression with the region `|z| < |a|` inverts instead to the anti-causal sequence `-a^n u[-n-1]`.
> **Key point:** `X(z) = z/(z-a) = \sum_{n\ge0}a^n z^{-n}` inverts to `a^n u[n]` in the region `|z| > |a|`; the residues at `z = a` and `z = 0` cancel for `n < 0`, and the region of convergence decides causal versus anti-causal.

### Q213. `GATE-2` Find the inverse Z-transform of `X(z) = 1/((1 − az)(1 − bz))` for `a \ne b`, and state the result for `a = b`.

> **Type:** Numerical
> **Answer:** `x[n] = (a^{n+1} − b^{n+1})/(a − b)` for `a \ne b`, and `x[n] = (n+1)a^n` for `a = b`.
> **Solution:** Partial fractions give `1/((1−az)(1−bz)) = [a/(a−b)]/(1−az) − [b/(a−b)]/(1−bz)` ✓, and each term inverts by Q212, so `x[n] = [a^{n+1} − b^{n+1}]/(a − b)` for `n \ge 0` ✓. Passing to the limit `b \to a` in the closed form, `a^{n+1} − b^{n+1} \approx (n+1)a^n(b − a)`, so the quotient tends to `(n+1)a^n`, which is the correct answer for the repeated-pole case; the derivative formula for a double pole gives the same, since `X(z) = 1/((1−az)^2)` has the expansion `(1−az)^{-2} = \sum_{n\ge0}(n+1)(az)^n` ✓. The contour route confirms both: for `a \ne b` the integrand `X(z)z^{n-1}` has simple poles at `1/a` and `1/b` with residues summing to the stated expression, while at `a = b` the pole is double and the double-pole residue formula produces `(n+1)a^n` ✓.
> **Key point:** `1/((1-az)(1-bz))` inverts to `(a^{n+1}-b^{n+1})/(a-b)`, and the limit `b \to a` gives `(n+1)a^n` for the repeated pole, which is what the double-pole residue formula produces.

### Q214. `GATE-2` Find the inverse Z-transform of `X(z) = z/((z - 1)(z - 2))` and state its region of convergence.

> **Type:** Numerical
> **Answer:** `x[n] = 2^n - 1` for `n \ge 0`, with region of convergence `|z| > 2`.
> **Solution:** Partial fractions give `X(z) = A/(z-1) + B/(z-2)`, and `A = lim_{z \to 1} z/(z-2) = -1` while `B = lim_{z \to 2} z/(z-1) = 2`, so `X(z) = -1/(z-1) + 2/(z-2)`. In powers of `z^{-1}` for `|z| > 2`, `-1/(z-1) = -z^{-1}\sum_{n\ge0}z^{-n} = -\sum_{n\ge1}z^{-n}` and `2/(z-2) = 2z^{-1}\sum_{n\ge0}(2/z)^n = \sum_{n\ge1}2^n z^{-n}`. Adding, the coefficient of `z^{-n}` is `2^n - 1`, so `x[n] = 2^n - 1` for `n \ge 1` and `x[0] = 0`, which the same formula also gives since `2^0 - 1 = 0`. The region of convergence is `|z| > 2`, the exterior of the outermost pole, as expected for a right-sided sequence. The check `X(z) \to 1` as `z \to \infty` confirms the absence of a `z^0` term, agreeing with `x[0] = 0`.
> **Key point:** `z/((z-1)(z-2)) = -\sum_{n\ge1}z^{-n} + \sum_{n\ge1}2^n z^{-n}` inverts to `2^n - 1` for `n \ge 0` with ROC `|z| > 2`; `X(\infty) = 1` confirms `x[0] = 0`.

### Q215. `GATE-2` Explain the correspondence between the unit circle, the region of convergence, and the Fourier transform, using `z = re^{j\omega}`.

> **Type:** Theory
> **Answer:** On `|z| = 1`, `z^{-n} = e^{-j\omega n}`, so `X(e^{j\omega}) = \sum_n x[n]e^{-j\omega n}` is the discrete-time Fourier transform; the unit circle must lie inside the region of convergence, which is the condition for the sequence to be summable and for the DTFT to exist.
> **Solution:** Substituting `z = re^{j\omega}` into the Z-transform definition gives `X(re^{j\omega}) = \sum_n x[n]r^{-n}e^{-j\omega n}`, the ordinary Fourier transform of the exponentially weighted sequence `x[n]r^{-n}` ✓. The limit `r \to 1^+` from inside the region of convergence recovers the DTFT, so the DTFT exists whenever the region of convergence contains `|z| = 1`, i.e. whenever `x` is absolutely summable. This is the analytic function that underlies every filter's frequency response, and it is why the Z-transform and the residue method fit together: evaluating `X(e^{j\omega})` and inverting `X` are the same contour computation on different contours. The counterpart in the continuous case is `z = e^{j\omega}` on the unit circle turning `∫ f(t)e^{-j\omega t}dt` into a contour integral, which is how Fourier integrals are evaluated by residues.
> **Key point:** On `|z| = 1`, `z^{-n} = e^{-j\omega n}` turns the Z-transform into the DTFT; the unit circle must lie in the region of convergence.

### Q216. `GATE-2` Evaluate `∫_{−∞}^{∞} e^{jωt}/(t^2 + a^2) dt` for real `a > 0`, closing above for `ω > 0` and below for `ω < 0`.

> **Type:** Numerical
> **Answer:** `(π/a) e^{−a|ω|}`.
> **Solution:** For `ω > 0` the factor `e^{j\omega z} = e^{j\omega x - \omega y}` decays as `y \to +\infty`, so the contour closes in the upper half-plane, where the only pole is `z = ia`. Its residue is `e^{j\omega(ia)}/(2ia) = e^{-\omega a}/(2ia)`, and the arc contribution vanishes, so the integral is `2\pi i \cdot e^{-\omega a}/(2ia) = (\pi/a)e^{-\omega a}`. For `ω < 0` the exponential decays as `y \to -\infty`, so the contour closes in the lower half-plane and is traversed clockwise. The only enclosed pole is `z = -ia`, with residue `e^{j\omega(-ia)}/(-2ia) = e^{\omega a}/(-2ia)`, and the clockwise orientation contributes a sign of `-1`, so the integral is `-2\pi i \cdot e^{\omega a}/(-2ia) = (\pi/a)e^{\omega a} = (\pi/a)e^{-a|\omega|}`. Combining, the value is `(π/a)e^{-a|\omega|}`, and at `ω = 0` this reduces to `π/a`, agreeing with Q205.
> **Key point:** Closing above for `ω > 0` and below for `ω < 0` gives `(π/a)e^{-a|\omega|}`; the factor `e^{\mp a\omega}` comes from the residue of `e^{j\omega z}` at `z = \pm ia`.

### Q217. `GATE-2` `MSQ` Which of the following are legitimate applications of the residue method to real integrals? (A) Closing a contour in the upper half-plane for an integrand decaying like `1/z^2`. (B) Using `z = e^{j\theta}` to convert `∫_0^{2\pi}` trigonometric integrals into rational integrals over the unit circle. (C) Using a sector or keyhole contour for integrals over branch cuts of `z^\alpha`. (D) Applying the residue theorem to a contour that passes through a pole, taking half its residue.

> **Type:** MCQ
> **Answer:** A, B and C only (Option a).
>
> (a) A, B and C
> (b) A and B only
> (c) B, C and D
> (d) A, C and D
>
> **Solution:** (A) is legitimate: the arc contributes `O(1/R)` when the integrand is `O(1/R^2)`, which is Q205. (B) is legitimate and is the standard reduction for `∫_0^{2\pi}` trigonometric integrands, giving the unit circle and a rational integrand, as in Q210. (C) is legitimate: for `z^\alpha` the function is multivalued, and a keyhole contour about the cut, with `z^\alpha` picking up a phase `e^{2\pi i\alpha}` after one turn, converts the integral along the cut into a residue computation, which is how `∫_0^\infty x^{\alpha-1}/(1+x)dx = \pi/\sin\pi\alpha` is proved. (D) is not legitimate: a pole on the contour makes the integral divergent, and the "half-residue" rule applies only to the specific situation of a pole on a straight line traversed as a principal value, where the prescription must be stated, and even then it is a principal value rather than a proper integral. Hence A, B and C.
> **Key point:** Upper-half-plane closure, the `z = e^{j\theta}` substitution and keyhole contours are all legitimate; a pole on the contour yields a principal value, never a plain `2\pi i` times its residue.

### Q218. `GATE-2` Evaluate `∫_{0}^{∞} dx/(1 + x^n)` for `n > 1` by a sector contour of angle `2π/n`.

> **Type:** Numerical
> **Answer:** `π/(n sin(π/n))`.
> **Solution:** Close with a sector contour of angle `2π/n`, chosen so that `z^n` returns to the same value after one turn. For `f(z) = 1/(1+z^n)` the only pole inside the sector is `z_0 = e^{iπ/n}`, with residue `1/(nz_0^{n-1}) = z_0/n`. On the lower ray, traversed from `Re^{2πi/n}` back to the origin, the integral is `e^{2πi/n}∫_0^R dr/(1+r^n)`, so the total contour integral is `(1 - e^{2πi/n})I` with `I = ∫_0^\infty dr/(1+r^n)`. The residue theorem therefore gives `(1-e^{2πi/n})I = 2πi e^{iπ/n}/n`. Since `1 - e^{2πi/n} = -2i e^{iπ/n} sin(π/n)`, dividing gives `I = 2πi e^{iπ/n}/(n \cdot -2i e^{iπ/n} sin(π/n))`, and the magnitude of this quotient is `π/(n sin(π/n))`, which is positive for `n > 1` since `0 < π/n < π`. Checks: at `n = 2` the formula gives `π/(2 sin(π/2)) = π/2`, agreeing with Q205, and at `n = 4` it gives `π/(4 \cdot \sqrt2/2) = π/(2\sqrt2)`, agreeing with Q208.
> **Key point:** The sector contour of angle `2π/n` for `1/(1+z^n)` encloses only `z_0 = e^{iπ/n}` with residue `e^{iπ/n}/n`, giving `∫_0^\infty dx/(1+x^n) = \pi/(n\sin(\pi/n))`, which reproduces `π/2` at `n = 2`.

### Q219. `GATE-2` State and apply the general recipe for evaluating a real integral by residues.

> **Type:** Recall
> **Answer:** Complexify the integrand so that it decays on a closing contour; close by a semicircle, sector or keyhole so that finitely many poles are enclosed and the closing part vanishes; then read the real integral off `2πi` times the sum of the residues.
> **Solution:** The recipe has four steps. (1) **Complexify:** replace the real integrand by a meromorphic `f(z)` agreeing with it on the axis, choosing the extension so that `|f(z)|` decays on the closing part. This is why the real frequency `t` is replaced by `z` in `e^{jωz}`, whose modulus `e^{-ω y}` fixes the half-plane of closure (Q216). (2) **Choose the contour:** a semicircle for whole-line integrals, a sector of angle `2π/n` when `z^n` must return to itself (Q218), a keyhole when a branch cut must be turned into a second integral (Q226), a rectangle when a periodic function of `e^{iz}` is involved. (3) **Prove the closing part vanishes:** an explicit bound such as `πR/(R^2-1)` in Q205 or `2πR/(R^4-1)` in Q207 is mandatory, never assumed. (4) **Sum residues and solve:** `∮ = 2πi Σ Res`, and the real integral is then extracted algebraically, using evenness (Q208) or the phase factor acquired on the second ray (Q218). Mistakes in steps 1 or 2 leave a non-vanishing arc or extra poles, which is the usual cause of a wrong answer even when the residues themselves are correct.
> **Key point:** Complexify so the closing part decays, close by a semicircle, sector or keyhole, prove the closing contribution vanishes, then read the integral off `2\pi i \sum Res`.

### Q220. `GATE-1` For the rational function `X(z) = z(z + 1)/((z - 1)(z - 2))`, state the ROC required for a causal sequence, and evaluate `x[0]`.

> **Type:** Numerical
> **Answer:** The causal ROC is `|z| > 2`, and `x[0] = 1`.
> **Solution:** A rational `X(z)` in the form `Σ_n x[n]z^{-n}` is causal when the region of convergence is the exterior of the outermost pole, so here `|z| > 2`. For the initial sample, divide numerator and denominator by `z^2`: `X(z) = (1 + 1/z)/((1 - 1/z)(1 - 2/z))`, which tends to 1 as `z \to \infty`; and since a causal sequence satisfies `X(z) \to x[0]`, this gives `x[0] = 1`. The partial fractions confirm it: writing `X = C + A/(z-1) + B/(z-2)`, the leading terms give `C = 1`, the coefficient of `z^{-1}` in the expansion of `A/(z-1)` is `A` and of `B/(z-2)` is `B`, so `A + B = 1` from `x[1]` and `2A + B = 3` from `x[2]`, giving `A = 2`, `B = -1`. In powers of `z^{-1}`, `A/(z-1) = \sum_{n\ge1} A z^{-n}` and `B/(z-2) = \sum_{n\ge1} B 2^{n-1} z^{-n}`, so `x[n] = 2 + (-1)2^{n-1} = 2 - 2^{n-1}` for `n \ge 1` and `x[0] = 1`. The rule `X(\infty) = x[0]` is a fast check on any partial-fraction inversion.
> **Key point:** The causal ROC is `|z| > 2`, and `X(\infty) = x[0] = 1` because `z(z+1)/((z-1)(z-2)) \to 1` after dividing by `z^2`.

### Q221. `GATE-2` Use residues to evaluate `∑_{n\in\mathbb{Z}} 1/(n^2 + a^2)` for `a > 0`.

> **Type:** Numerical
> **Answer:** `(π/a) coth(πa)`.
> **Solution:** Integrate `f(z) = \pi\cot(\pi z)/(z^2+a^2)` over the square with vertices `(N+1/2)(\pm1\pm i)`, which stays at distance at least `1/2` from every integer, so `\pi\cot(\pi z)` is bounded there by some constant `C` independent of `N`. Since `1/(z^2+a^2) = O(1/|z|^2)` on the square and its perimeter is `8N+4`, the contour integral is `O(C/N) \to 0`. The enclosed poles are the integers `n` with `|n| \le N`, at each of which `\pi\cot(\pi z)` has residue 1 and so `f` has residue `1/(n^2+a^2)`, together with the two poles `z = \pm ia`, once `N > a`. Using `\cot(\pi ia) = -i\coth(\pi a)` and the oddness of `\cot`, the two residues are each `-\pi\coth(\pi a)/(2a)`, summing to `-\pi\coth(\pi a)/a`. The residue theorem therefore gives `0 = \sum_{n=-N}^{N} 1/(n^2+a^2) - \pi\coth(\pi a)/a`, and letting `N \to \infty`, `∑_{n\in\mathbb{Z}} 1/(n^2+a^2) = (\pi/a)\coth(\pi a)`. A check on the limit: as `a \to \infty` the sum is dominated by the `n = 0` term and tends to `1/a^2`, and since `\coth(\pi a) \to 1` the formula tends to `1/a^2` as well. Taking `a = 1` gives `∑ 1/(n^2+1) = \pi\coth\pi \approx 3.1533`, whose first three terms `1 + 2(1/2 + 1/5) = 2.4` and tail estimate bring it to that value.
> **Key point:** Integrating `\pi\cot(\pi z)/(z^2+a^2)` over a square avoiding the integers gives `\sum_{n\in\mathbb{Z}} 1/(n^2+a^2) = (\pi/a)\coth(\pi a)`, whose limit as `a\to\infty` is `1/a^2`, matching the dominant `n=0` term.

### Q222. `GATE-2` Evaluate `∫_{0}^{2π} dθ/(2 + cos θ)` and check it against the general formula of Q210.

> **Type:** Numerical
> **Answer:** `2π/√3`.
> **Solution:** Q210 with `a = 2` and `b = 1` gives `2\pi/\sqrt{2^2-1^2} = 2\pi/\sqrt3`. Verifying directly with `z = e^{i\theta}`: the integral becomes `(2/i)\oint_{|z|=1} dz/(z^2+4z+1)`. The roots are `z_\pm = -2 \pm \sqrt3`; `z_+ = -2+\sqrt3 \approx -0.268` lies inside the unit circle while `z_- = -2-\sqrt3 \approx -3.732` lies outside, so exactly one pole is enclosed, with residue `1/(2z_+ + 4) = 1/(2\sqrt3)`. The integral is therefore `(2/i)(2\pi i)(1/(2\sqrt3)) = 2\pi/\sqrt3`. A numerical sanity check: `1/(2+\cos\theta)` ranges between `1/3` and `1`, and `2\pi/\sqrt3 \approx 3.628` corresponds to an average of about `0.577`, which lies in that range.
> **Key point:** `∫_0^{2\pi}d\theta/(2+\cos\theta) = 2\pi/\sqrt3 \approx 3.628`, since the single enclosed root of `z^2+4z+1` is `-2+\sqrt3` with residue `1/(2\sqrt3)`.

### Q223. `GATE-1` Find the inverse Z-transform of `X(z) = z^2/(z^2 - 3z + 2)` and comment on the possible regions of convergence.

> **Type:** Numerical
> **Answer:** The same algebraic expression inverts to different sequences depending on the ROC: `x[n] = 3\cdot 2^{n-1} - 1` for `n \ge 1` with `x[0] = 1` when `|z| > 2`; a strictly left-sided sequence when `|z| < 1`; and a two-sided sequence when `1 < |z| < 2`.
> **Solution:** `X(z) = z^2/((z-1)(z-2))`. Long division and partial fractions give `X(z) = 1 + A/(z-1) + B/(z-2)`, and multiplying through by `z^2` and comparing coefficients of `z^2` and `z` gives `A + B = -3` and `2A + B = 0`, hence `A = 3` and `B = -6`. So `X(z) = 1 + 3/(z-1) - 6/(z-2)`. In the **exterior** ROC `|z| > 2`, `3/(z-1) = \sum_{n\ge1}3z^{-n}` and `-6/(z-2) = \sum_{n\ge1}(-6)2^{n-1}z^{-n}`, so `x[0] = 1` and `x[n] = 3 - 6\cdot 2^{n-1}` for `n \ge 1`. In the **interior** ROC `|z| < 1`, both `1/(z-1)` and `1/(z-2)` expand in non-negative powers of `z`, namely `3/(z-1) = -3\sum_{n\ge0}z^n` and `-6/(z-2) = 3\sum_{n\ge0}(z/2)^n`, a power series in `z` and so a strictly left-sided sequence. In the **annulus** `1 < |z| < 2`, the first term expands in `z^{-1}` and the second in `z`, giving a genuinely two-sided sequence. The upshot is that a rational expression plus a region of convergence determines the sequence, and the expression alone does not.
> **Key point:** `X(z) = z^2/((z-1)(z-2))` has three possible regions of convergence, `|z|>2`, `|z|<1` and `1<|z|<2`, giving right-sided, left-sided and two-sided sequences; the ROC, not the expression, fixes the answer.

### Q224. `GATE-2` `MSQ` Which statements correctly describe the relationship between the Z-transform, the residue theorem and the Fourier transform? (A) `x[n] = (1/(2πi))∮ X(z)z^{n-1}dz` when the contour lies in the ROC. (B) For a rational `X`, the inverse Z-transform reduces to summing residues of `X(z)z^{n-1}`. (C) The DTFT exists whenever the ROC contains the unit circle. (D) The inverse Z-transform depends only on the algebraic expression for `X(z)`, not on the ROC.

> **Type:** MCQ
> **Answer:** A, B and C only (Option a).
>
> (a) A, B and C
> (b) A and B only
> (c) A, C and D
> (d) B and D only
>
> **Solution:** (A) is Cauchy's formula for the Laurent coefficients of `X` about the origin, valid for any contour inside the region of convergence. (B) is the residue theorem applied to that integral, and is the practical method for rational `X` (Q213, Q214). (C) is true: on `|z| = 1` the Z-transform becomes `Σ x[n]e^{-jωn}`, which exists when the unit circle lies in the region of convergence, equivalently when `x` is absolutely summable. (D) is false, as Q223 shows, since one expression `z^2/((z-1)(z-2))` yields three different sequences for three different regions of convergence. Hence A, B and C only.
> **Key point:** The inverse Z-transform is a Cauchy integral, or equivalently a residue sum, inside the ROC; the DTFT needs the unit circle inside the ROC; and the ROC is essential to the answer.

### Q225. `GATE-2` Evaluate `∫_{0}^{∞} dx/(1 + x^6)` using the general formula of Q218.

> **Type:** Numerical
> **Answer:** `π/3`.
> **Solution:** Q218 gives `∫_0^\infty dx/(1+x^n) = \pi/(n\sin(\pi/n))` for `n > 1`, and with `n = 6` this is `\pi/(6\sin(\pi/6)) = \pi/(6 \cdot 1/2) = \pi/3`. A direct check is worthwhile because `z^6 = -1` has a root at `z = -1` on the negative real axis, which lies outside the sector of angle `2\pi/6 = \pi/3` and so is not enclosed; the sector contains only `z_0 = e^{i\pi/6}`, whose residue is `z_0/6`, giving `(1-e^{2\pi i/6})I = 2\pi i e^{i\pi/6}/6` and hence `I = \pi/3`. A magnitude check: the integrand equals 1 at the origin and decays like `x^{-6}`, so the integral is of order 1, and `\pi/3 \approx 1.047` is exactly that order, slightly below the value `\pi/(2\sqrt2) \approx 1.111` obtained for the fourth power, as the larger exponent should give.
> **Key point:** `∫_0^\infty dx/(1+x^n) = \pi/(n\sin(\pi/n))`, so for `n = 6` the value is `\pi/(6 \cdot 1/2) = \pi/3 \approx 1.047`.

### Q226. `GATE-2` Evaluate `∫_{0}^{∞} x^{a-1}/(1 + x) dx` for `0 < a < 1` by a keyhole contour.

> **Type:** Numerical
> **Answer:** `π/sin(πa)`.
> **Solution:** Take a keyhole contour about the **positive** real axis for `f(z) = z^{a-1}/(1+z)`, with the branch of `z^{a-1}` chosen so that the argument runs from `0` to `2\pi`. On the upper bank the contribution is `I = \int_0^\infty x^{a-1}/(1+x)dx`; on the lower bank the argument is `2\pi`, so `z^{a-1}` acquires the factor `e^{2\pi i(a-1)} = e^{2\pi ia}` and the direction of traversal is reversed, contributing `-e^{2\pi ia}I`. The total contour integral is therefore `(1-e^{2\pi ia})I`. The only pole is `z = -1`, which on this branch sits at argument `2\pi - \pi = \pi`, and its residue is `(-1)^{a-1} = e^{i\pi(a-1)} = -e^{i\pi a}`. The residue theorem gives `(1-e^{2\pi ia})I = 2\pi i\,(-e^{i\pi a})`. Since `1 - e^{2\pi ia} = -2i e^{i\pi a}\sin(\pi a)`, dividing gives `I = -2\pi i e^{i\pi a}/(-2i e^{i\pi a}\sin(\pi a)) = \pi/\sin(\pi a)`, and `0 < \pi a < \pi` makes the sine positive, so the value is positive as it must be. A decisive check is `a = 1/2`, where `x = t^2` gives `I = 2\int_0^\infty dt/(1+t^2) = \pi`, and `\pi/\sin(\pi/2) = \pi` agrees exactly.
> **Key point:** The keyhole contour for `z^{a-1}/(1+z)` compares the two banks, which differ by the factor `e^{2\pi ia}`, and the single pole at `-1` with residue `-e^{i\pi a}` then gives `∫_0^\infty x^{a-1}/(1+x)dx = \pi/\sin(\pi a)`, matching `a = 1/2` where the value is `π`.

### Q227. `GATE-2` `MSQ` Which of the following are valid cautions when applying the residue method? (A) A pole on the contour invalidates the residue theorem and needs a limiting prescription. (B) The closing part of the contour must be shown to vanish, not assumed. (C) The residue sum is controlled by the behaviour of the integrand at infinity. (D) A pole of order `m` always contributes `2πi/m` to a contour integral.

> **Type:** MCQ
> **Answer:** A, B and C only (Option a).
>
> (a) A, B and C
> (b) A and C only
> (c) A, B, C and D
> (d) B, C and D
>
> **Solution:** (A) is true: a pole on `C` makes the integral divergent, and the "half-residue" convention is a principal-value prescription that must be stated rather than a consequence of the theorem (Q144, Q200). (B) is true: in every evaluation the arc bound, such as `πR/(R^2-1)` in Q205 or `2πR/(R^4-1)` in Q207, is the step that licenses taking the limit, and omitting it is the commonest logical gap. (C) is true: the sum of the enclosed residues equals minus the residue at infinity, so it is fixed by the leading term of the integrand at infinity, which is why `1/(z^3-1)` integrates to 0 over a contour holding all three poles while `z^2/(z^3-1)` integrates to `2\pi i` (Q202, Q203). (D) is false: a pole of order `m` contributes `2\pi i` times its residue, and that residue depends on the analytic factor and may be 0, as for `1/(z\sin z)` at 0 (Q198) and for `1/(z-z_0)^2` (Q200). Hence A, B and C only.
> **Key point:** Poles on the contour, an unverified arc estimate and the behaviour at infinity are the three places where residue computations go wrong; a pole of order `m` contributes `2\pi i` times its residue, which may be zero.

## Quick revision — Complex Analysis

- `|z| = √(x²+y²)`, `arg z = θ` with `z = |z|e^{iθ}`; `z = re^{iθ}` is unchanged under `θ → θ + 2kπ`, so the argument is multivalued.
- De Moivre: `(re^{iθ})^n = r^n e^{inθ}`; the `n` roots of `wⁿ = c` are `|c|^{1/n}e^{i(θ+2kπ)/n}`, and for `c = 1` they sum to 0 when `n > 1`.
- `w = (z−a)/(z−\bar a)` sends the real axis to `|w| = 1`; the half-plane containing `a` maps to `|w| < 1`, because `z = a` maps to `w = 0`.
- A Möbius map with real coefficients sends the real axis to the real axis; `w = (z+1)/(z−1)` sends `|z| = 1` to `Re(w) = 0` since `w = −\bar w` there.
- `|z − a| = r` with `r > 0` is a circle; `|z − a| < r` a disc. A linear-fractional map is determined by three points.
- `e^{z+2πi} = e^z` and the only periods are `2kπi`; `log z = ln|z| + i(arg z + 2kπ)`, so `log(−1) = i(2k+1)π` is multivalued.
- `e^{iθ} = cos θ + i sin θ` gives `sin z = (e^{iz} − e^{−iz})/(2i)`, `cos z = (e^{iz} + e^{−iz})/2`, `sinh z = (e^z − e^{−z})/2`, `cosh z = (e^z + e^{−z})/2`.
- `z^{p/q}` has `q` values `|z|^{p/q}e^{i(p/q)(θ+2kπ)}` for `k` from 0 to `q − 1`, and they sum to 0 for `p ≠ 0`.
- `sin z`, `cos z`, `e^z` are entire; `z^a` for `a` non-integer has a branch point at 0; `log z` is not single-valued on any punctured disc, so it has no Laurent series there.
- `Γ(n) = (n−1)!`, `Γ(1/2) = √π`, so `∫_0^∞ e^{−t²}dt = √π/2` and `∫_{−∞}^{∞} e^{−t²}dt = √π`; the normal density is normalised by `√{2π}`.
- `erf(0.5) ≈ 0.5205`, `erf(1) ≈ 0.8427`, `erf(2) ≈ 0.9953`, `erf(3) ≈ 0.99998`; `erfc(3) ≈ 2.2×10^{−5}`.
- Poles of `1/(e^z − 1)` are `z = 2πik`, all with residue 1; `1/(e^z − 1) = 1/z − 1/2 + z/12 − z³/720`, so 0 is a simple pole and not essential.
- A Taylor series about `z₀` has radius equal to the distance to the nearest singularity: `1/(1−z) = −Σ(−1)ⁿ(z−2)ⁿ` at `z₀ = 2`, radius 1.
- `Σ zⁿ` diverges at every point of `|z| = 1` because `|zⁿ| = 1` never tends to 0, although `1/(1−z)` is finite at `z = −1`.
- `log(1+z) = Σ_{n≥1}(−1)^{n+1}zⁿ/n` has radius 1 (branch point at `z = −1`) and diverges at both `z = 1` and `z = −1`.
- `f = u + iv` analytic gives `u_x = v_y`, `u_y = −v_x`, and `f′ = u_x + iv_x = v_y − iu_y`; `|z|²` is differentiable only at `0` and analytic nowhere.
- `u`, `v` are harmonic; `∇u·∇v = 0` where `f′ ≠ 0`; hence `∇²(uv) = 0` but `∇²(u²) = 2|f′|² ≠ 0`, so `u²` is the non-harmonic choice.
- Cauchy's theorem: `∮_C f dz = 0` for `f` analytic on and inside `C`; `∮_C f dz = 2πi Res(f, z₀)` for a single simple pole; `f(z₀) = (1/(2πi))∮ f dz` (Cauchy's formula).
- The general form is `∮_C f dz = 2πi Σ_j n(C, z_j)Res(f, z_j)`, so the shape of `C` matters only through winding numbers.
- `Res(π/sin πz, n) = (−1)^n`; `Res(1/(z−z₀)^2, z₀) = 0`; `1/(z sin z)` has no `z^{−1}` term at 0, so its residue there is 0.
- `Res(π/(z sin πz), 0) = 1` since the limit is `π`; a pole of order `m` contributes `2πi` times its residue, which may be 0, and a pole **on** the contour gives only `iπ` times the residue in the principal value.
- Isolated singularities: removable if `lim (z−z₀)f` exists, a pole of order `m` if `lim (z−z₀)^m f` is a nonzero constant, essential if the principal part is infinite.
- Big Picard: near an essential singularity every value is taken infinitely often with at most one exception; near a pole a whole disc of finite values is omitted.
- `Res(f, ∞) = −`(the `z^{−1}` coefficient at infinity); the total over all poles including infinity is 0, and the finite sum alone is 0 only when `f = O(z^{−2})`.
- Real integrals: `∫_{−∞}^{∞}dx/(x²+1) = π` (arc `≤ πR/(R²−1) → 0`), `∫_{−∞}^{∞}dx/(x⁴+1) = π/√2`, `∫_{−∞}^{∞}e^{iaω}/(t²+a²)dt = (π/a)e^{−a|ω|}`.
- `∫_0^∞ dx/(1+x^n) = π/(n sin(π/n))` by a sector of angle `2π/n`: `π/2` at `n = 2`, `π/(2√2)` at `n = 4`, `π/3` at `n = 6`; `∫_0^∞ x^{α−1}/(1+x)dx = π/sin(πα)` by a keyhole.
- `z = e^{iθ}` gives `dθ = dz/(iz)` and `cos θ = (z+z^{−1})/2`, so `∫_0^{2π}dθ/(a+b cos θ) = 2π/√(a²−b²)`; the substitution also turns `Σ aₙ\cos nθ` into rational integrals in `z`.
- A locally uniform limit of analytic functions is analytic; term-by-term differentiation needs the derivative series uniform on compact subsets **plus** convergence at one point; a power series satisfies both for `|z| < R`.
- The inverse Z-transform is `x[n] = (1/(2πi))∮ X(z)z^{n−1}dz` on a circle inside the ROC; `X(∞) = x[0]` checks any inversion; the ROC, not the expression, fixes the sequence (`|z|>2`, `1<|z|<2`, `|z|<1` for `z²/((z−1)(z−2))`).
- `z/(z−a)` inverts to `a^n u[n]` for `|z| > |a|` and to `−a^n u[−n−1]` for `|z| < |a|`; a rational expression may admit several valid sequences.

