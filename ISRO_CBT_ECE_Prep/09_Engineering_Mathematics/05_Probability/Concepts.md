# Probability - Concepts

## 1. Basic Definitions

### Sample Space (S)
- Set of all possible outcomes
- **Elementary event**: Single outcome
- **Compound event**: Combination of outcomes

### Event
- Subset of sample space
- **Mutually exclusive**: A ∩ B = ∅
- **Exhaustive**: A₁ ∪ A₂ ∪ ... ∪ Aₙ = S

---

## 2. Set Operations

### Basic Operations
```
A ∪ B: Union (A or B)
A ∩ B: Intersection (A and B)
A': Complement (not A)
A - B: Difference (A but not B)
A Δ B: Symmetric difference
```

### De Morgan's Laws
```
(A ∪ B)' = A' ∩ B'
(A ∩ B)' = A' ∪ B'
```

---

## 3. Axioms of Probability

### Kolmogorov Axioms
1. P(A) ≥ 0 for all events A
2. P(S) = 1
3. For mutually exclusive events: P(A₁ ∪ A₂ ∪ ...) = P(A₁) + P(A₂) + ...

### Properties Derived
```
P(∅) = 0
P(A') = 1 - P(A)
P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
P(A ∪ B ∪ C) = P(A) + P(B) + P(C) - P(A∩B) - P(A∩C) - P(B∩C) + P(A∩B∩C)
```

---

## 4. Conditional Probability

### Definition
```
P(A|B) = P(A ∩ B) / P(B)  [P(B) > 0]
```

### Properties
```
P(A|A) = 1
P(A|S) = P(A)
If A ⊂ B: P(A|B) = P(A)/P(B)
```

### Multiplication Rule
```
P(A ∩ B) = P(A) · P(B|A) = P(B) · P(A|B)
```

### Chain Rule
```
P(A₁ ∩ A₂ ∩ ... ∩ Aₙ) = P(A₁) · P(A₂|A₁) · P(A₃|A₁∩A₂) · ...
```

---

## 5. Independent Events

### Definition
```
A and B are independent iff P(A ∩ B) = P(A) · P(B)
```

### Equivalent Condition
```
A and B independent ⟺ P(A|B) = P(A)  [if P(B) > 0]
```

### Properties
```
If A and B independent:
- A' and B independent
- A and B' independent
- A' and B' independent
```

### Pairwise vs Mutual Independence
- **Pairwise**: P(A∩B) = P(A)P(B), P(A∩C) = P(A)P(C), P(B∩C) = P(B)P(C)
- **Mutual**: P(A∩B∩C) = P(A)P(B)P(C)
- Mutual implies pairwise, but pairwise does NOT imply mutual

---

## 6. Bayes' Theorem

### Formula
```
P(Aᵢ|B) = P(B|Aᵢ) · P(Aᵢ) / Σ[j] P(B|Aⱼ) · P(Aⱼ)
```

### Prior vs Posterior
- **Prior**: P(Aᵢ) - before observing B
- **Posterior**: P(Aᵢ|B) - after observing B
- **Likelihood**: P(B|Aᵢ)

### Law of Total Probability
```
P(B) = Σ[i] P(B|Aᵢ) · P(Aᵢ)

where {Aᵢ} is a partition of S
```

---

## 7. Random Variables

### Discrete Random Variable
- Takes countable values
- Described by PMF: P(X = xᵢ) = pᵢ

### Continuous Random Variable
- Takes uncountable values
- Described by PDF: f(x) ≥ 0, ∫ f(x) dx = 1

### Properties
```
PMF: Σ p(xᵢ) = 1, p(xᵢ) ≥ 0
PDF: ∫ f(x) dx = 1, f(x) ≥ 0
CDF: F(x) = P(X ≤ x) = Σ or ∫ up to x
```

---

## 8. Probability Density Function (PDF)

### Definition
```
f(x) = dF(x)/dx  [if F is differentiable]
P(a ≤ X ≤ b) = ∫[a,b] f(x) dx
```

### Properties
1. f(x) ≥ 0
2. ∫[-∞,∞] f(x) dx = 1
3. P(X = a) = 0 for continuous RV
4. P(a < X < b) = P(a ≤ X ≤ b)

---

## 9. Cumulative Distribution Function (CDF)

### Definition
```
F(x) = P(X ≤ x)
```

### Properties
1. F is non-decreasing
2. F(-∞) = 0, F(∞) = 1
3. F is right-continuous
4. P(a < X ≤ b) = F(b) - F(a)
5. P(X > x) = 1 - F(x) = F̄(x) (survival function)

---

## 10. Expected Value

### Discrete
```
E[X] = μ = Σ xᵢ · p(xᵢ)
```

### Continuous
```
E[X] = μ = ∫ x · f(x) dx
```

### Function of Random Variable
```
E[g(X)] = Σ g(xᵢ) · p(xᵢ)  [discrete]
E[g(X)] = ∫ g(x) · f(x) dx  [continuous]
```

### Properties
```
E[aX + b] = aE[X] + b
E[X + Y] = E[X] + E[Y] (always)
E[XY] = E[X]E[Y] (if independent)
```

---

## 11. Variance

### Definition
```
Var(X) = σ² = E[(X-μ)²] = E[X²] - (E[X])²
```

### Standard Deviation
```
σ = √(Var(X))
```

### Properties
```
Var(c) = 0
Var(aX + b) = a²Var(X)
Var(X + Y) = Var(X) + Var(Y) (if independent)
Var(X + Y) = Var(X) + Var(Y) + 2Cov(X,Y)
```

### Coefficient of Variation
```
CV = σ/μ (relative measure of spread)
```

---

## 12. Moment Generating Function (MGF)

### Definition
```
M_X(t) = E[e^(tX)]
```

### Properties
```
M_X(0) = 1
E[X^n] = M^(n)_X(0) (nth derivative at t=0)
If M_X(t) = M_Y(t), then X and Y have same distribution
```

### Sum of Independent RVs
```
M_{X+Y}(t) = M_X(t) · M_Y(t)  [if independent]
```

---

## 13. Covariance and Correlation

### Covariance
```
Cov(X,Y) = E[XY] - E[X]E[Y]
```

### Correlation Coefficient
```
ρ = Cov(X,Y) / (σ_X · σ_Y)

-1 ≤ ρ ≤ 1
ρ = 0: uncorrelated
|ρ| = 1: perfectly correlated
```

### Properties
```
Cov(X,X) = Var(X)
Cov(X,Y) = Cov(Y,X)
Cov(aX,bY) = ab·Cov(X,Y)
Cov(X+Y,Z) = Cov(X,Z) + Cov(Y,Z)
```

---

## 14. Important Inequalities

### Chebyshev's Inequality
```
P(|X - μ| ≥ kσ) ≤ 1/k²
```

### Markov's Inequality
```
P(X ≥ a) ≤ E[X]/a  [for X ≥ 0, a > 0]
```

### Cauchy-Schwarz Inequality
```
(E[XY])² ≤ E[X²] · E[Y²]
```

---

## 15. Law of Total Probability (Bayes Application)

```
If A₁, A₂, ..., Aₙ partition S:

P(B) = Σ P(B|Aᵢ)P(Aᵢ)

P(Aⱼ|B) = P(B|Aⱼ)P(Aⱼ) / Σ P(B|Aᵢ)P(Aᵢ)
```

### Applications
- Medical testing (sensitivity/specificity)
- Quality control
- Signal detection
