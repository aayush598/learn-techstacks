# Calculus - Practice Questions

## Easy Level

### Q1. Basic Limit
Find lim(x→0) sin(3x)/x.

**Solution**: lim(x→0) sin(3x)/x = 3 · lim(x→0) sin(3x)/(3x) = 3 · 1 = **3**

---

### Q2. Derivative of Polynomial
Find d/dx [3x⁴ - 2x² + 5x - 7].

**Solution**: 12x³ - 4x + 5

---

### Q3. Chain Rule
Find d/dx [sin(3x²)].

**Solution**: cos(3x²) · 6x = **6x·cos(3x²)**

---

### Q4. Basic Integration
Find ∫ (2x³ + 3x² - x + 4) dx.

**Solution**: **x⁴/2 + x³ - x²/2 + 4x + C**

---

### Q5. Definite Integral
Evaluate ∫[0,1] x² dx.

**Solution**: [x³/3]₀¹ = 1/3 - 0 = **1/3**

---

## Medium Level

### Q6. L'Hopital's Rule
Find lim(x→0) (eˣ - 1 - x)/x².

**Solution**:
- Form 0/0, apply L'Hopital: lim (eˣ - 1)/(2x)
- Still 0/0, apply again: lim eˣ/2 = **1/2**

---

### Q7. Implicit Differentiation
Find dy/dx if x² + y² = 25.

**Solution**:
- 2x + 2y(dy/dx) = 0
- dy/dx = **-x/y**

---

### Q8. Product Rule
Find d/dx [x²·sin(x)].

**Solution**: 2x·sin(x) + x²·cos(x) = **x(2sin(x) + x·cos(x))**

---

### Q9. Integration by Substitution
Find ∫ x·cos(x²) dx.

**Solution**:
- Let u = x², du = 2x dx → x dx = du/2
- ∫ cos(u) du/2 = sin(u)/2 + C = **sin(x²)/2 + C**

---

### Q10. Integration by Parts
Find ∫ x·eˣ dx.

**Solution**:
- u = x, dv = eˣ dx → du = dx, v = eˣ
- ∫ x·eˣ dx = x·eˣ - ∫ eˣ dx = **x·eˣ - eˣ + C = eˣ(x-1) + C**

---

### Q11. Maxima/Minima
Find local extrema of f(x) = x³ - 3x + 2.

**Solution**:
- f'(x) = 3x² - 3 = 0 → x = ±1
- f''(x) = 6x
- f''(1) = 6 > 0 → local min at x=1, f(1) = 0
- f''(-1) = -6 < 0 → local max at x=-1, f(-1) = 4

---

### Q12. Taylor Series
Find Maclaurin series for eˣ up to x³ term.

**Solution**: **1 + x + x²/2 + x³/6**

---

### Q13. Mean Value Theorem
Verify MVT for f(x) = x² on [1,4].

**Solution**:
- f(4) - f(1) = 16 - 1 = 15
- (b-a) = 3
- f'(c) = 2c = 15/3 = 5 → c = **5/2** ∈ (1,4) ✓

---

### Q14. Quotient Rule
Find d/dx [(x²+1)/(x-1)].

**Solution**:
- f = x²+1, g = x-1, f' = 2x, g' = 1
- (2x(x-1) - (x²+1)(1))/(x-1)² = **(x²-2x-1)/(x-1)²**

---

### Q15. Second Derivative Test
Find the point of inflection of f(x) = x⁴ - 4x³.

**Solution**:
- f'(x) = 4x³ - 12x²
- f''(x) = 12x² - 24x = 12x(x-2)
- f''(x) = 0 at x = 0 and x = 2
- Sign changes at both → inflection points at **x = 0** and **x = 2**

---

## Hard Level

### Q16. Trigonometric Substitution
Evaluate ∫ √(4-x²) dx.

**Solution**:
- Let x = 2sin(θ), dx = 2cos(θ)dθ
- ∫ √(4-4sin²θ) · 2cosθ dθ = ∫ 2cosθ · 2cosθ dθ = 4∫cos²θ dθ
- = 4∫(1+cos2θ)/2 dθ = 2θ + sin2θ + C
- = 2θ + 2sinθcosθ + C
- = 2arcsin(x/2) + x√(4-x²)/2 + C

---

### Q17. Improper Integral
Evaluate ∫[1,∞] 1/x² dx.

**Solution**:
- = lim(t→∞] ∫[1,t] x⁻² dx = lim(t→∞] [-1/x]₁ᵗ
- = lim(t→∞] (-1/t + 1) = **1**

---

### Q18. Partial Fractions
Evaluate ∫ (3x+5)/((x-1)(x+2)) dx.

**Solution**:
- 3x+5 = A(x+2) + B(x-1)
- x=1: 8 = 3A → A = 8/3
- x=-2: -1 = -3B → B = 1/3
- ∫ [8/(3(x-1)) + 1/(3(x+2))] dx = **(8/3)ln|x-1| + (1/3)ln|x+2| + C**

---

### Q19. Higher Order Chain Rule
Find d²/dx² [sin(x²)].

**Solution**:
- First: d/dx [sin(x²)] = 2x·cos(x²)
- Second: d/dx [2x·cos(x²)] = 2cos(x²) - 4x²sin(x²)

---

### Q20. L'Hopital (Indeterminate Power)
Find lim(x→0⁺) xˣ.

**Solution**:
- Let y = xˣ, ln(y) = x·ln(x)
- lim(x→0⁺) x·ln(x) = lim(x→0⁺) ln(x)/(1/x) [∞/∞]
- = lim(x→0⁺) (1/x)/(-1/x²) = lim(x→0⁺) (-x) = 0
- So y = e⁰ = **1**

---

### Q21. Area Between Curves
Find area between y = x² and y = x.

**Solution**:
- x² = x → x = 0, 1
- A = ∫[0,1] (x - x²) dx = [x²/2 - x³/3]₀¹ = 1/2 - 1/3 = **1/6**

---

### Q22. Volume of Revolution
Find volume when y = √x (0 ≤ x ≤ 4) rotated about x-axis.

**Solution**:
- V = π ∫[0,4] (√x)² dx = π ∫[0,4] x dx = π[x²/2]₀⁴ = π(8) = **8π**

---

### Q23. Implicit Differentiation (Complex)
Find dy/dx if eʸ + xy = e.

**Solution**:
- eʸ(dy/dx) + y + x(dy/dx) = 0
- dy/dx(eʸ + x) = -y
- dy/dx = **-y/(eʸ + x)**

---

### Q24. Definite Integral Property
Evaluate ∫[0,π/2] sin⁴(x) dx.

**Solution**:
- Using Walli's formula (n=4 even):
- = (3/4)(1/2)(π/2) = **3π/16**

---

### Q25. Taylor Series Expansion
Expand f(x) = 1/(1-x) about x = 0 up to x⁴.

**Solution**: **1 + x + x² + x³ + x⁴**

---

## ISRO-Focused Questions

### Q26. Quick Limit
Find lim(x→∞) (x²+1)/(2x²-3).

**Solution**: Divide by x²: lim (1+1/x²)/(2-3/x²) = **1/2**

---

### Q27. Derivative at a Point
If f(x) = x³ - 2x + 1, find f'(2).

**Solution**: f'(x) = 3x² - 2, f'(2) = 12 - 2 = **10**

---

### Q28. Quick Integration
Find ∫[0,π] sin(x) dx.

**Solution**: [-cos(x)]₀π = -(-1) - (-1) = **2**

---

### Q29. L'Hopital Quick
Find lim(x→0) (sin(x) - x)/x³.

**Solution**:
- 0/0, L'Hopital: lim (cos(x) - 1)/(3x²)
- 0/0, L'Hopital: lim (-sin(x))/(6x)
- 0/0, L'Hopital: lim (-cos(x))/6 = **-1/6**

---

### Q30. Critical Point
Find critical points of f(x) = x³ - 6x² + 9x.

**Solution**:
- f'(x) = 3x² - 12x + 9 = 3(x-1)(x-3) = 0
- Critical points: **x = 1** and **x = 3**
