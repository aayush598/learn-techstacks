# Calculus - Formulas

## 1. Limits Formulas

### Standard Limits
```
lim(x→0) sin(x)/x = 1
lim(x→0) tan(x)/x = 1
lim(x→0) (1-cos(x))/x = 0
lim(x→0) (e^x - 1)/x = 1
lim(x→0) (1+x)^(1/x) = e
lim(x→∞) (1 + 1/x)^x = e
lim(x→0) ln(1+x)/x = 1
lim(x→0) (a^x - 1)/x = ln(a)
```

### Limit Laws
```
lim[f ± g] = lim f ± lim g
lim[f · g] = lim f · lim g
lim[f/g] = lim f / lim g  [if lim g ≠ 0]
lim[f^n] = (lim f)^n
lim[c·f] = c · lim f
```

---

## 2. Derivative Formulas

### Power Rule
```
d/dx [x^n] = nx^(n-1)
d/dx [x] = 1
d/dx [1/x] = -1/x²
d/dx [√x] = 1/(2√x)
```

### Exponential & Logarithmic
```
d/dx [e^x] = e^x
d/dx [a^x] = a^x ln(a)
d/dx [ln(x)] = 1/x
d/dx [log_a(x)] = 1/(x ln a)
```

### Trigonometric
```
d/dx [sin(x)] = cos(x)
d/dx [cos(x)] = -sin(x)
d/dx [tan(x)] = sec²(x)
d/dx [sec(x)] = sec(x)tan(x)
d/dx [csc(x)] = -csc(x)cot(x)
d/dx [cot(x)] = -csc²(x)
```

### Inverse Trigonometric
```
d/dx [arcsin(x)] = 1/√(1-x²)
d/dx [arccos(x)] = -1/√(1-x²)
d/dx [arctan(x)] = 1/(1+x²)
d/dx [arccot(x)] = -1/(1+x²)
d/dx [arcsec(x)] = 1/(|x|√(x²-1))
d/dx [arccsc(x)] = -1/(|x|√(x²-1))
```

### Chain Rule
```
d/dx [f(g(x))] = f'(g(x)) · g'(x)

Examples:
d/dx [sin(x²)] = cos(x²) · 2x
d/dx [e^(3x)] = 3e^(3x)
d/dx [ln(cos(x))] = -tan(x)
d/dx [arctan(e^x)] = e^x/(1+e^(2x))
```

### Product & Quotient
```
(fg)' = f'g + fg'
(f/g)' = (f'g - fg')/g²
```

### Implicit Differentiation
```
If F(x,y) = 0:
dy/dx = -F_x/F_y = -(∂F/∂x)/(∂F/∂y)
```

### Logarithmic Differentiation
```
d/dx [f(x)^g(x)] = f(x)^g(x) [g'(x)ln(f(x)) + g(x)f'(x)/f(x)]
```

---

## 3. Higher Order Derivatives

```
d²/dx² [x^n] = n(n-1)x^(n-2)
d²/dx² [e^x] = e^x
d²/dx² [sin(x)] = -sin(x)
d²/dx² [cos(x)] = -cos(x)
d²/dx² [ln(x)] = -1/x²
```

### Leibnitz Rule (nth derivative of product)
```
(fg)^(n) = Σ[k=0 to n] C(n,k) f^(k) g^(n-k)

where C(n,k) = n!/(k!(n-k)!)
```

---

## 4. Integration Formulas

### Power Rule
```
∫ x^n dx = x^(n+1)/(n+1) + C  [n ≠ -1]
∫ 1/x dx = ln|x| + C
∫ 1/x² dx = -1/x + C
∫ 1/√x dx = 2√x + C
```

### Exponential & Logarithmic
```
∫ e^x dx = e^x + C
∫ a^x dx = a^x/ln(a) + C
∫ ln(x) dx = x·ln(x) - x + C
```

### Trigonometric
```
∫ sin(x) dx = -cos(x) + C
∫ cos(x) dx = sin(x) + C
∫ tan(x) dx = -ln|cos(x)| + C = ln|sec(x)| + C
∫ cot(x) dx = ln|sin(x)| + C
∫ sec(x) dx = ln|sec(x) + tan(x)| + C
∫ csc(x) dx = -ln|csc(x) + cot(x)| + C
∫ sin²(x) dx = x/2 - sin(2x)/4 + C
∫ cos²(x) dx = x/2 + sin(2x)/4 + C
∫ sec²(x) dx = tan(x) + C
∫ csc²(x) dx = -cot(x) + C
∫ sec(x)tan(x) dx = sec(x) + C
∫ csc(x)cot(x) dx = -csc(x) + C
```

### Inverse Trigonometric
```
∫ 1/√(1-x²) dx = arcsin(x) + C
∫ -1/√(1-x²) dx = arccos(x) + C
∫ 1/(1+x²) dx = arctan(x) + C
∫ -1/(1+x²) dx = arccot(x) + C
```

### Special Forms
```
∫ 1/(x²+a²) dx = (1/a)arctan(x/a) + C
∫ 1/√(a²-x²) dx = arcsin(x/a) + C
∫ 1/(x√(x²-a²)) dx = (1/a)arcsec(|x|/a) + C
∫ √(a²-x²) dx = (x/2)√(a²-x²) + (a²/2)arcsin(x/a) + C
∫ √(x²+a²) dx = (x/2)√(x²+a²) + (a²/2)ln|x+√(x²+a²)| + C
∫ √(x²-a²) dx = (x/2)√(x²-a²) - (a²/2)ln|x+√(x²-a²)| + C
```

---

## 5. Integration Techniques

### Substitution
```
∫ f(g(x))·g'(x) dx = ∫ f(u) du  where u = g(x)
```

### Integration by Parts
```
∫ u dv = uv - ∫ v du

LIATE Rule (priority for u):
Logarithmic → Inverse trig → Algebraic → Trigonometric → Exponential
```

### Partial Fractions
```
∫ (px+q)/[(x-a)(x-b)] dx = ∫ [A/(x-a) + B/(x-b)] dx
∫ (px+q)/(x-a)² dx = ∫ [A/(x-a) + B/(x-a)²] dx
∫ (px+q)/(ax²+bx+c) dx = complete square + arctan or ln
```

### Trigonometric Substitutions
```
∫ √(a²-x²) dx → x = a sin(θ)
∫ √(a²+x²) dx → x = a tan(θ)
∫ √(x²-a²) dx → x = a sec(θ)
```

### Walli's Formula (for ∫ sin^n or cos^n)
```
∫[0,π/2] sin^n(x) dx = ∫[0,π/2] cos^n(x) dx

n even: (n-1)/n · (n-3)/(n-2) · ... · 1/2 · π/2
n odd: (n-1)/n · (n-3)/(n-2) · ... · 2/3 · 1
```

---

## 6. Definite Integration Properties

```
∫[a,b] f(x) dx = ∫[a,b] f(a+b-x) dx
∫[0,a] f(x) dx = ∫[0,a] f(a-x) dx
∫[0,π/2] sin^n(x) dx = ∫[0,π/2] cos^n(x) dx
∫[0,π] x·f(sin(x)) dx = π/2 ∫[0,π] f(sin(x)) dx
∫[0,2π] sin^n(x) dx = 0 for odd n
∫[0,2π] cos^n(x) dx = 0 for odd n
```

### King's Property
```
∫[a,b] f(x) dx = ∫[a,b] f(a+b-x) dx
```

---

## 7. Taylor Series Formulas

### General Taylor Series (about x = a)
```
f(x) = Σ[n=0 to ∞] f^(n)(a)/n! · (x-a)^n
```

### Common Series
```
e^x = Σ x^n/n! = 1 + x + x²/2! + x³/3! + ...     [all x]
sin(x) = Σ (-1)^n x^(2n+1)/(2n+1)! = x - x³/3! + x⁵/5! - ...  [all x]
cos(x) = Σ (-1)^n x^(2n)/(2n)! = 1 - x²/2! + x⁴/4! - ...     [all x]
1/(1-x) = Σ x^n = 1 + x + x² + x³ + ...             [|x| < 1]
1/(1+x) = Σ (-1)^n x^n = 1 - x + x² - x³ + ...     [|x| < 1]
ln(1+x) = Σ (-1)^(n+1) x^n/n = x - x²/2 + x³/3 - ...  [-1 < x ≤ 1]
arctan(x) = Σ (-1)^n x^(2n+1)/(2n+1) = x - x³/3 + x⁵/5 - ...  [|x| ≤ 1]
```

---

## 8. Mean Value Theorem Formulas

```
Rolle's: f'(c) = 0 for some c ∈ (a,b)
         if f(a) = f(b), f continuous on [a,b], diff on (a,b)

Lagrange MVT: f'(c) = [f(b)-f(a)]/(b-a)
              for some c ∈ (a,b)

Cauchy MVT: f'(c)/g'(c) = [f(b)-f(a)]/[g(b)-g(a)]
            for some c ∈ (a,b)
```

---

## 9. L'Hopital's Rule Formula

```
If lim f(x)/g(x) = 0/0 or ∞/∞:

lim f(x)/g(x) = lim f'(x)/g'(x)

Keep applying until determinate form is reached.
```

---

## 10. Area and Volume Formulas

### Area Between Curves
```
A = ∫[a,b] |f(x) - g(x)| dx
A = ∫[c,d] |h(y) - k(y)| dy  [horizontal]
```

### Volume of Revolution
```
Disk: V = π ∫[a,b] [f(x)]² dx
Washer: V = π ∫[a,b] ([R(x)]² - [r(x)]²) dx
Shell: V = 2π ∫[a,b] x·f(x) dx  [about y-axis]
Shell: V = 2π ∫[c,d] y·h(y) dy  [about x-axis]
```

---

## 11. Partial Derivative Formulas

```
∂/∂x [x^n y^m] = nx^(n-1) y^m
∂/∂y [x^n y^m] = mx^n y^(m-1)
∂/∂x [f(x,y)] = f_x
∂/∂y [f(x,y)] = f_y

Chain Rule: dz/dt = ∂z/∂x · dx/dt + ∂z/∂y · dy/dt

Gradient: ∇f = (∂f/∂x, ∂f/∂y, ∂f/∂z)
Directional derivative: D_u f = ∇f · u
```
