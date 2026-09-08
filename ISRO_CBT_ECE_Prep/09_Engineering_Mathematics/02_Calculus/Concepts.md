# Calculus - Concepts

## 1. Limits

### Definition
- lim(x→a) f(x) = L means f(x) approaches L as x approaches a
- Left-hand limit: lim(x→a⁻) f(x)
- Right-hand limit: lim(x→a⁺) f(x)
- Limit exists iff LHL = RHL

### Standard Limits
```
lim(x→0) sin(x)/x = 1
lim(x→0) (1-cos(x))/x = 0
lim(x→0) (e^x - 1)/x = 1
lim(x→0) (1+x)^(1/x) = e
lim(x→∞) (1 + 1/x)^x = e
lim(x→0) tan(x)/x = 1
lim(x→0) ln(1+x)/x = 1
```

### Limit Laws
```
lim[f(x) + g(x)] = lim f(x) + lim g(x)
lim[f(x) · g(x)] = lim f(x) · lim g(x)
lim[f(x)/g(x)] = lim f(x) / lim g(x)  [if denominator ≠ 0]
lim[f(x)]^n = [lim f(x)]^n
```

### Indeterminate Forms
- 0/0, ∞/∞, 0·∞, ∞-∞, 0⁰, 1^∞, ∞⁰

---

## 2. Continuity

### Definition
- f is continuous at x = a if:
  1. f(a) is defined
  2. lim(x→a) f(x) exists
  3. lim(x→a) f(x) = f(a)

### Types of Discontinuity
| Type | Description |
|------|-------------|
| Removable | Limit exists but ≠ f(a) or f(a) undefined |
| Jump | LHL ≠ RHL (finite) |
| Infinite | lim = ±∞ |

### Intermediate Value Theorem
- If f continuous on [a,b] and k between f(a) and f(b)
- Then ∃ c ∈ (a,b) such that f(c) = k

---

## 3. Differentiation

### First Principle
```
f'(x) = lim(h→0) [f(x+h) - f(x)] / h
```

### Basic Differentiation Rules
```
d/dx [c] = 0
d/dx [x^n] = nx^(n-1)
d/dx [e^x] = e^x
d/dx [a^x] = a^x ln(a)
d/dx [ln(x)] = 1/x
d/dx [sin(x)] = cos(x)
d/dx [cos(x)] = -sin(x)
d/dx [tan(x)] = sec²(x)
d/dx [sec(x)] = sec(x)tan(x)
d/dx [csc(x)] = -csc(x)cot(x)
d/dx [cot(x)] = -csc²(x)
```

### Chain Rule
```
d/dx [f(g(x))] = f'(g(x)) · g'(x)

Example: d/dx [sin(x²)] = cos(x²) · 2x
Example: d/dx [e^(3x)] = 3e^(3x)
```

### Implicit Differentiation
- Differentiate both sides with respect to x
- Treat y as function of x (use chain rule)
- Solve for dy/dx

### Product Rule
```
d/dx [f·g] = f'g + fg'
```

### Quotient Rule
```
d/dx [f/g] = (f'g - fg') / g²
```

---

## 4. Higher Order Derivatives
- f''(x) = d²f/dx² (second derivative)
- f'''(x) = d³f/dx³ (third derivative)
- Applications: maxima/minima, curvature, Taylor series

---

## 5. Maxima and Minima

### First Derivative Test
- f'(c) = 0 (critical point)
- Sign change of f' at c:
  - + to - → local maximum
  - - to + → local minimum
  - No change → neither

### Second Derivative Test
- f'(c) = 0 and f''(c) < 0 → local maximum
- f'(c) = 0 and f''(c) > 0 → local minimum
- f'(c) = 0 and f''(c) = 0 → inconclusive

### Global Extrema on [a,b]
- Check critical points and endpoints
- Compare f values

---

## 6. Mean Value Theorems

### Rolle's Theorem
- f continuous on [a,b], differentiable on (a,b)
- f(a) = f(b)
- Then ∃ c ∈ (a,b) such that f'(c) = 0

### Mean Value Theorem (Lagrange)
- f continuous on [a,b], differentiable on (a,b)
- Then ∃ c ∈ (a,b) such that f'(c) = [f(b)-f(a)]/(b-a)

### Cauchy's Mean Value Theorem
- f,g continuous on [a,b], differentiable on (a,b)
- g'(x) ≠ 0 on (a,b)
- Then ∃ c ∈ (a,b) such that [f(b)-f(a)]/[g(b)-g(a)] = f'(c)/g'(c)

---

## 7. L'Hopital's Rule

### Conditions
- lim f(x)/g(x) gives 0/0 or ∞/∞
- f and g differentiable near a (except possibly at a)
- g'(x) ≠ 0 near a

### Formula
```
lim f(x)/g(x) = lim f'(x)/g'(x)
```

### Indeterminate Forms and Handling
```
0/0 → Apply L'Hopital directly
∞/∞ → Apply L'Hopital directly
0·∞ → Convert to 0/(1/∞) or ∞/(1/0)
∞-∞ → Combine fractions or factor
0⁰ → Take ln, get 0·∞
1^∞ → Take ln, get ∞·0
∞⁰ → Take ln, get 0·∞
```

---

## 8. Integration

### Indefinite Integration
```
∫ x^n dx = x^(n+1)/(n+1) + C  [n ≠ -1]
∫ 1/x dx = ln|x| + C
∫ e^x dx = e^x + C
∫ sin(x) dx = -cos(x) + C
∫ cos(x) dx = sin(x) + C
∫ sec²(x) dx = tan(x) + C
∫ 1/(1+x²) dx = arctan(x) + C
∫ 1/√(1-x²) dx = arcsin(x) + C
```

### Integration Techniques
1. **Substitution**: ∫ f(g(x))g'(x) dx = ∫ f(u) du
2. **Integration by Parts**: ∫ u dv = uv - ∫ v du
3. **Partial Fractions**: Decompose rational functions
4. **Trigonometric Substitution**: For √(a²-x²), √(a²+x²), √(x²-a²)

### Definite Integration
```
∫[a,b] f(x) dx = F(b) - F(a)

Properties:
∫[a,a] f(x) dx = 0
∫[a,b] f(x) dx = -∫[b,a] f(x) dx
∫[a,b] f(x) dx = ∫[a,c] f(x) dx + ∫[c,b] f(x) dx
```

### Fundamental Theorem of Calculus
```
Part 1: d/dx ∫[a,x] f(t) dt = f(x)
Part 2: ∫[a,b] f(x) dx = F(b) - F(a) where F' = f
```

---

## 9. Taylor Series

### Definition
```
f(x) = Σ[n=0 to ∞] f^(n)(a)/n! · (x-a)^n

Maclaurin series (a=0):
f(x) = f(0) + f'(0)x + f''(0)x²/2! + f'''(0)x³/3! + ...
```

### Common Taylor Series
```
e^x = 1 + x + x²/2! + x³/3! + ...  [all x]
sin(x) = x - x³/3! + x⁵/5! - ...   [all x]
cos(x) = 1 - x²/2! + x⁴/4! - ...   [all x]
1/(1-x) = 1 + x + x² + x³ + ...    [|x| < 1]
ln(1+x) = x - x²/2 + x³/3 - ...    [-1 < x ≤ 1]
```

---

## 10. Applications of Integration

### Area Between Curves
```
A = ∫[a,b] |f(x) - g(x)| dx
```

### Volume of Revolution
```
Disk: V = π ∫[a,b] [f(x)]² dx
Washer: V = π ∫[a,b] ([R(x)]² - [r(x)]²) dx
Shell: V = 2π ∫[a,b] x·f(x) dx
```

---

## 11. Partial Derivatives

### Definition
```
∂f/∂x = lim(h→0) [f(x+h,y) - f(x,y)] / h
∂f/∂y = lim(h→0) [f(x,y+h) - f(x,y)] / h
```

### Chain Rule (Multivariable)
```
dz/dt = ∂z/∂x · dx/dt + ∂z/∂y · dy/dt
```

### Gradient
```
∇f = (∂f/∂x, ∂f/∂y, ∂f/∂z)
Direction of steepest ascent
```

---

## 12. Important Concepts for ISRO

### Quick Derivative Table
| Function | Derivative |
|----------|-----------|
| x^n | nx^(n-1) |
| e^x | e^x |
| ln(x) | 1/x |
| sin(x) | cos(x) |
| cos(x) | -sin(x) |
| tan(x) | sec²(x) |
| arcsin(x) | 1/√(1-x²) |
| arctan(x) | 1/(1+x²) |

### Quick Integral Table
| Function | Integral |
|----------|----------|
| x^n | x^(n+1)/(n+1) |
| e^x | e^x |
| 1/x | ln|x| |
| sin(x) | -cos(x) |
| cos(x) | sin(x) |
| 1/(1+x²) | arctan(x) |
| 1/√(1-x²) | arcsin(x) |
