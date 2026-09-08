# Probability - Formulas

## 1. Basic Probability Formulas

### Addition Rule
```
P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
P(A ∪ B) = P(A) + P(B)  [if A, B mutually exclusive]
P(A ∪ B ∪ C) = P(A) + P(B) + P(C) - P(A∩B) - P(A∩C) - P(B∩C) + P(A∩B∩C)
```

### Complement
```
P(A') = 1 - P(A)
P(∅) = 0
P(S) = 1
```

### Difference
```
P(A - B) = P(A) - P(A ∩ B)
P(A - B) = P(A) - P(A ∩ B) = P(A ∩ B')
```

---

## 2. Conditional Probability

### Definition
```
P(A|B) = P(A ∩ B) / P(B)  [P(B) > 0]
```

### Multiplication Rule
```
P(A ∩ B) = P(A) · P(B|A)
P(A ∩ B) = P(B) · P(A|B)
```

### Chain Rule
```
P(A₁ ∩ A₂ ∩ ... ∩ Aₙ) = P(A₁) · P(A₂|A₁) · P(A₃|A₁∩A₂) · ... · P(Aₙ|A₁∩...∩Aₙ₋₁)
```

### Independence
```
A, B independent ⟺ P(A ∩ B) = P(A) · P(B)
A, B independent ⟺ P(A|B) = P(A)  [if P(B) > 0]
A, B independent ⟺ P(B|A) = P(B)  [if P(A) > 0]
```

---

## 3. Bayes' Theorem

### Formula
```
P(Aᵢ|B) = P(B|Aᵢ) · P(Aᵢ) / P(B)

where P(B) = Σ[j] P(B|Aⱼ) · P(Aⱼ)  (Total Probability)
```

### Notation
- P(Aᵢ) = Prior probability
- P(Aᵢ|B) = Posterior probability
- P(B|Aᵢ) = Likelihood
- P(B) = Evidence (normalizing constant)

---

## 4. Total Probability

### Law
```
If A₁, A₂, ..., Aₙ partition S (mutually exclusive, exhaustive):

P(B) = Σ[i=1 to n] P(B|Aᵢ) · P(Aᵢ)
```

### Extended Form
```
P(B) = P(B|A₁)P(A₁) + P(B|A₂)P(A₂) + ... + P(B|Aₙ)P(Aₙ)
```

---

## 5. Discrete Distribution Formulas

### Bernoulli (X ~ Bernoulli(p))
```
P(X=0) = 1-p, P(X=1) = p
E[X] = p
Var(X) = p(1-p)
```

### Binomial (X ~ Bin(n,p))
```
P(X=k) = C(n,k) p^k (1-p)^(n-k)
E[X] = np
Var(X) = np(1-p)
```

### Poisson (X ~ Poisson(λ))
```
P(X=k) = e^(-λ) λ^k / k!
E[X] = λ
Var(X) = λ
MGF: M(t) = e^(λ(e^t - 1))
```

### Geometric (X ~ Geom(p))
```
P(X=k) = (1-p)^(k-1) p  [k = 1,2,3,...]
E[X] = 1/p
Var(X) = (1-p)/p²
```

### Negative Binomial
```
P(X=k) = C(k-1, r-1) p^r (1-p)^(k-r)  [k = r, r+1, ...]
E[X] = r/p
Var(X) = r(1-p)/p²
```

### Hypergeometric
```
P(X=k) = C(K,k) C(N-K, n-k) / C(N,n)
E[X] = nK/N
Var(X) = n(K/N)(1-K/N)(N-n)/(N-1)
```

### Discrete Uniform (X ~ Unif{1,2,...,n})
```
P(X=k) = 1/n
E[X] = (n+1)/2
Var(X) = (n²-1)/12
```

---

## 6. Continuous Distribution Formulas

### Uniform (X ~ Unif(a,b))
```
f(x) = 1/(b-a) for a ≤ x ≤ b
F(x) = (x-a)/(b-a)
E[X] = (a+b)/2
Var(X) = (b-a)²/12
```

### Exponential (X ~ Exp(λ))
```
f(x) = λe^(-λx) for x ≥ 0
F(x) = 1 - e^(-λx)
E[X] = 1/λ
Var(X) = 1/λ²
Memoryless: P(X > s+t | X > s) = P(X > t)
```

### Normal (X ~ N(μ,σ²))
```
f(x) = (1/(σ√(2π))) e^(-(x-μ)²/(2σ²))
E[X] = μ
Var(X) = σ²
Standard: Z = (X-μ)/σ ~ N(0,1)
P(a < X < b) = Φ((b-μ)/σ) - Φ((a-μ)/σ)
```

### Standard Normal (Z ~ N(0,1))
```
φ(z) = (1/√(2π)) e^(-z²/2)
Φ(z) = ∫[-∞,z] φ(t) dt
Φ(-z) = 1 - Φ(z)
P(|Z| ≤ 1) ≈ 0.6827
P(|Z| ≤ 2) ≈ 0.9545
P(|Z| ≤ 3) ≈ 0.9973
```

### Gamma (X ~ Gamma(α,β))
```
f(x) = (1/(β^α Γ(α))) x^(α-1) e^(-x/β) for x > 0
E[X] = αβ
Var(X) = αβ²
Special case: Exp(λ) = Gamma(1, 1/λ)
Special case: Chi-squared(k) = Gamma(k/2, 2)
```

### Beta (X ~ Beta(α,β))
```
f(x) = (1/B(α,β)) x^(α-1) (1-x)^(β-1) for 0 < x < 1
E[X] = α/(α+β)
Var(X) = αβ/((α+β)²(α+β+1))
```

### Chi-Squared (X ~ χ²(k))
```
E[X] = k
Var(X) = 2k
Sum of k independent standard normals squared
```

---

## 7. Expectation Formulas

### Discrete
```
E[X] = Σ xᵢ P(X=xᵢ)
E[g(X)] = Σ g(xᵢ) P(X=xᵢ)
```

### Continuous
```
E[X] = ∫ x f(x) dx
E[g(X)] = ∫ g(x) f(x) dx
```

### Properties
```
E[c] = c
E[aX + b] = aE[X] + b
E[X + Y] = E[X] + E[Y]
E[XY] = E[X]E[Y]  [if X, Y independent]
```

### Moments
```
E[X^n] = nth raw moment about origin
E[(X-μ)^n] = nth central moment
```

---

## 8. Variance Formulas

### Definition
```
Var(X) = E[(X-μ)²] = E[X²] - (E[X])²
```

### Properties
```
Var(c) = 0
Var(aX + b) = a²Var(X)
Var(X ± Y) = Var(X) + Var(Y)  [if independent]
Var(X ± Y) = Var(X) + Var(Y) ± 2Cov(X,Y)
```

---

## 9. Covariance Formulas

### Definition
```
Cov(X,Y) = E[XY] - E[X]E[Y]
```

### Properties
```
Cov(X,X) = Var(X)
Cov(X,Y) = Cov(Y,X)
Cov(aX,bY) = ab Cov(X,Y)
Cov(X+Y,Z) = Cov(X,Z) + Cov(Y,Z)
```

### Correlation
```
ρ(X,Y) = Cov(X,Y) / (σ_X σ_Y)
-1 ≤ ρ ≤ 1
```

---

## 10. Moment Generating Function Formulas

### Definition
```
M_X(t) = E[e^(tX)]
```

### Derivatives
```
M_X'(0) = E[X]
M_X''(0) = E[X²]
M_X^(n)(0) = E[X^n]
```

### Important MGFs
```
Bernoulli: M(t) = 1-p + pe^t
Binomial: M(t) = (1-p + pe^t)^n
Poisson: M(t) = e^(λ(e^t-1))
Normal: M(t) = e^(μt + σ²t²/2)
Exponential: M(t) = λ/(λ-t) for t < λ
Uniform(a,b): M(t) = (e^(bt)-e^(at))/(t(b-a))
```

### Transformations
```
Y = aX + b: M_Y(t) = e^(bt) M_X(at)
X + Y (independent): M_{X+Y}(t) = M_X(t) · M_Y(t)
```

---

## 11. Conditional Expectation

```
E[X|Y=y] = Σ x P(X=x|Y=y)  [discrete]
E[X|Y=y] = ∫ x f_{X|Y}(x|y) dx  [continuous]
E[X] = E[E[X|Y]]  (Law of Total Expectation)
Var(X) = E[Var(X|Y)] + Var(E[X|Y])
```

---

## 12. Important Inequalities

```
Chebyshev: P(|X-μ| ≥ kσ) ≤ 1/k²
Markov: P(X ≥ a) ≤ E[X]/a  [X ≥ 0, a > 0]
Cauchy-Schwarz: (E[XY])² ≤ E[X²]E[Y²]
Jensen: φ(E[X]) ≤ E[φ(X)]  [φ convex]
```
