# Complex Analysis - Practice Questions

## Easy Level

### Q1. Modulus and Argument
Find |z| and arg(z) for z = 3 + 4i.

**Solution**:
- |z| = √(9+16) = √25 = **5**
- arg(z) = arctan(4/3) = **53.13°**

---

### Q2. Polar Form
Convert z = -1 + i to polar form.

**Solution**:
- r = √(1+1) = √2
- θ = π - π/4 = 3π/4
- z = **√2 e^(i3π/4)**

---

### Q3. De Moivre's Theorem
Find (cos θ + i sin θ)⁵.

**Solution**:
- = cos(5θ) + i sin(5θ)

---

### Q4. nth Roots
Find all cube roots of 8.

**Solution**:
- 8 = 8e^(i0)
- Roots: 2e^(i2kπ/3) for k = 0,1,2
- z₁ = **2**, z₂ = **-1+i√3**, z₃ = **-1-i√3**

---

### Q5. Analytic Function Check
Is f(z) = z² analytic?

**Solution**:
- u = x²-y², v = 2xy
- ∂u/∂x = 2x = ∂v/∂y ✓
- ∂u/∂y = -2y = -∂v/∂x ✓
- **Yes, analytic everywhere**

---

## Medium Level

### Q6. Cauchy-Riemann
Find v if u = x²-y² + xy.

**Solution**:
- ∂u/∂x = 2x+y = ∂v/∂y → v = 2xy + y²/2 + g(x)
- ∂u/∂y = -2y+x = -∂v/∂x → -2y+x = -(2y + g'(x))
- g'(x) = x → g(x) = x²/2
- **v = 2xy + y²/2 + x²/2 + C**

---

### Q7. Simple Pole Residue
Find Res(1/(z²+1), i).

**Solution**:
- z²+1 = (z+i)(z-i)
- Simple pole at z = i
- Res = lim(z→i) (z-i)/(z+i)(z-i) = 1/(2i) = **-i/2**

---

### Q8. Residue Theorem
Evaluate ∮|z|=2 dz/(z²+1).

**Solution**:
- Poles at z = ±i inside |z| = 2
- Res(z=i) = 1/(2i), Res(z=-i) = -1/(2i)
- ∮ = 2πi(1/(2i) - 1/(2i)) = **0**

---

### Q9. Cauchy's Integral Formula
Evaluate ∮|z|=3 e^z/(z-1) dz.

**Solution**:
- z = 1 is inside |z| = 3
- By Cauchy's formula: = 2πi × e¹ = **2πie**

---

### Q10. Laurent Series
Find Laurent series of 1/(z(z-1)) about z = 0 for 0 < |z| < 1.

**Solution**:
- 1/(z(z-1)) = -1/z × 1/(1-z) = -(1/z)Σz^n = **-Σz^(n-1) for n = 0,1,2,...**
- = -1/z - 1 - z - z² - ...

---

### Q11. Essential Singularity
Classify singularity of e^(1/z) at z = 0.

**Solution**:
- Laurent series: e^(1/z) = Σ 1/(n!z^n) has infinitely many negative powers
- **Essential singularity**

---

### Q12. Real Integral
Evaluate ∫[-∞,∞] dx/(x²+1).

**Solution**:
- Poles at z = ±i, only z = i in upper half-plane
- Res(z=i) = 1/(2i)
- ∫ = 2πi × 1/(2i) = **π**

---

### Q13. Conformal Mapping
What does w = z² map the first quadrant to?

**Solution**:
- z = re^(iθ), 0 < θ < π/2
- w = r²e^(i2θ), 0 < 2θ < π
- **Upper half-plane**

---

### Q14. Möbius Transformation
Find Möbius transformation mapping 0→1, 1→i, i→0.

**Solution**:
- w = (az+b)/(cz+d)
- w(0) = 1 → b/d = 1
- w(i) = 0 → ai+b = 0 → b = -ai
- w(1) = i → (a+b)/(c+d) = i
- Solving: w = **(z-i)/(z+1)**

---

### Q15. Maximum Modulus
If f is analytic in |z| ≤ 1 and |f(z)| ≤ 5, what is |f(0)|?

**Solution**:
- By maximum modulus principle: |f(0)| ≤ max|f| on |z| = 1 ≤ 5
- **|f(0)| ≤ 5**

---

## Hard Level

### Q16. Residue at Double Pole
Find Res(z²/(z-1)², 1).

**Solution**:
- Double pole at z = 1
- Res = lim(z→1) d/dz [(z-1)² × z²/(z-1)²]
- = lim(z→1) d/dz [z²] = lim(z→1) 2z = **2**

---

### Q17. Evaluate Real Integral
Evaluate ∫[0,∞] dx/(x²+1)².

**Solution**:
- Use upper half-plane contour
- Double pole at z = i
- Res = lim(z→i) d/dz [(z-i)²/(z²+1)²]
- = lim(z→i) d/dz [1/(z+i)²] = lim -2/(z+i)³
- = -2/(2i)³ = -2/(-8i) = 1/(4i)
- ∫ = 2πi × 1/(4i) = π/2
- By symmetry: ∫[0,∞] = π/4

---

### Q18. Argument Principle
Find number of zeros of z⁴ + z³ + 1 in |z| < 2.

**Solution**:
- On |z| = 2: |z⁴| = 16 > |z³ + 1| ≤ 9
- By Rouché's theorem: same zeros as z⁴ = 0
- **4 zeros** inside |z| < 2

---

### Q19. Conformal Mapping
Map the upper half-plane to unit disk.

**Solution**:
- w = (z - i)/(z + i)
- Maps i → 0, real axis → unit circle
- **Möbius transformation**

---

### Q20. Branch Cut
Find branch points of f(z) = √(z²-1).

**Solution**:
- z²-1 = 0 → z = ±1
- **Branch points at z = 1 and z = -1**
- Branch cut: typically [-1, 1] or (-∞, -1] ∪ [1, ∞)

---

### Q21. Cauchy Principal Value
Find P.V. ∫[-∞,∞] dx/x.

**Solution**:
- P.V. = lim(R→∞] ∫[-R,R] dx/x = lim(R→∞] [ln|x|]₋ᴿᴿ = 0
- **P.V. = 0**

---

### Q22. Residue at Essential Singularity
Find residue of e^(1/z) at z = 0.

**Solution**:
- e^(1/z) = Σ 1/(n!z^n)
- Coefficient of 1/z: a₋₁ = 1/1! = **1**

---

### Q23. Evaluate Integral with cot
Evaluate ∫[0,2π] dθ/(2+cos θ).

**Solution**:
- Let z = e^(iθ), cos θ = (z+z⁻¹)/2
- dθ = dz/(iz)
- ∮|z|=1 2dz/(iz(z²+4z+1))
- Poles: z = -2±√3, only z = -2+√3 inside unit circle
- Res = 1/(iz) × 2/((z+2-√3)(z+2+√3)) at z = -2+√3
- = 2/(i(-2+√3)(2√3)) = 1/(i√3(-2+√3))
- ∫ = 2πi × Res = **2π/√3**

---

### Q24. Conformal Mapping (Strip)
Map strip 0 < Im(z) < π to unit disk.

**Solution**:
- First: w₁ = e^z maps strip to upper half-plane
- Then: w₂ = (w₁-i)/(w₁+i) maps to unit disk
- **w = (e^z - i)/(e^z + i)**

---

### Q25. Laurent Series (Annulus)
Find Laurent series of 1/((z-1)(z-2)) for 1 < |z| < 2.

**Solution**:
- 1/((z-1)(z-2)) = 1/(z-1) - 1/(z-2)
- For 1 < |z| < 2: 1/(z-1) = (1/z)Σ(z)^n = Σz^(n-1)
- 1/(z-2) = -(1/2)Σ(z/2)^n = -Σz^n/2^(n+1)
- Combine appropriate terms

---

## ISRO-Focused Questions

### Q26. Quick Residue
Find Res(1/(z-3), 3).

**Solution**:
- Simple pole at z = 3
- Res = lim(z→3) (z-3) × 1/(z-3) = **1**

---

### Q27. Cauchy Theorem Quick
∮|z|=1 cos(z) dz = ?

**Solution**:
- cos(z) is entire (analytic everywhere)
- By Cauchy's theorem: **∮ = 0**

---

### Q28. Modulus Quick
|e^(iπ)| = ?

**Solution**:
- |e^(iπ)| = |cos(π) + i sin(π)| = |-1| = **1**

---

### Q29. Argument Quick
arg(i) = ?

**Solution**:
- i = 0 + 1i
- arg(i) = **π/2** (or 90°)

---

### Q30. Analytic Check
Is f(z) = |z|² analytic?

**Solution**:
- u = x²+y², v = 0
- ∂u/∂x = 2x, ∂v/∂y = 0
- CR: 2x = 0 and 2y = 0 only at origin
- **Not analytic anywhere** (except trivially at z=0)
