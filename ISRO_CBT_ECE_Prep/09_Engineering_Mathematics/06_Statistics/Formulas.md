# Statistics - Formulas

## 1. Central Tendency Formulas

### Mean
```
Population: μ = (Σ xᵢ) / N
Sample: x̄ = (Σ xᵢ) / n
Weighted: x̄_w = Σ(wᵢxᵢ) / Σwᵢ
```

### Median
```
Odd n: x_((n+1)/2)
Even n: (x_(n/2) + x_(n/2+1)) / 2
```

### Mode
```
Mode = most frequent value
For grouped data: Mode = L + (f₁-f₀)/(2f₁-f₀-f₂) × h
```

---

## 2. Dispersion Formulas

### Range
```
Range = x_max - x_min
```

### Variance
```
Population: σ² = Σ(xᵢ-μ)²/N
Sample: s² = Σ(xᵢ-x̄)²/(n-1) = [Σxᵢ² - (Σxᵢ)²/n]/(n-1)
```

### Standard Deviation
```
σ = √σ²
s = √s²
```

### Coefficient of Variation
```
CV = (σ/μ) × 100%
```

### Mean Absolute Deviation
```
MAD = Σ|xᵢ - x̄| / n
```

### Quartiles
```
Q₁ = value at position (n+1)/4
Q₂ = median = value at position (n+1)/2
Q₃ = value at position 3(n+1)/4
IQR = Q₃ - Q₁
```

---

## 3. Poisson Distribution Formulas

```
P(X = k) = e^(-λ) λ^k / k!  for k = 0, 1, 2, ...

E[X] = λ
Var(X) = λ
σ = √λ
Mode = floor(λ)

MGF: M(t) = e^(λ(e^t - 1))
PGF: G(s) = e^(λ(s-1))

P(X ≤ k) = Σ[i=0 to k] e^(-λ) λ^i / i!

Poisson Approximation to Binomial:
If n large, p small, λ = np:
P(X = k) ≈ e^(-λ) λ^k / k!
```

### Recursive Formula
```
P(X = k) = (λ/k) × P(X = k-1)
```

---

## 4. Uniform Distribution Formulas

### Continuous Uniform (a, b)
```
f(x) = 1/(b-a) for a ≤ x ≤ b

F(x) = (x-a)/(b-a)

E[X] = (a+b)/2

Var(X) = (b-a)²/12

P(c < X < d) = (d-c)/(b-a) for [c,d] ⊂ [a,b]
```

### Discrete Uniform {1, 2, ..., n}
```
P(X = k) = 1/n for k = 1, 2, ..., n

E[X] = (n+1)/2

Var(X) = (n²-1)/12
```

---

## 5. Normal Distribution Formulas

### General Normal N(μ, σ²)
```
f(x) = (1/(σ√(2π))) e^(-(x-μ)²/(2σ²))

F(x) = Φ((x-μ)/σ)

P(a < X < b) = Φ((b-μ)/σ) - Φ((a-μ)/σ)

P(X > a) = 1 - Φ((a-μ)/σ)

P(X < a) = Φ((a-μ)/σ)
```

### Standard Normal N(0,1)
```
φ(z) = (1/√(2π)) e^(-z²/2)

Φ(z) = ∫[-∞,z] φ(t) dt

Φ(-z) = 1 - Φ(z)

|z| Values:
P(|Z| ≤ 1) = 0.6827
P(|Z| ≤ 1.645) = 0.90
P(|Z| ≤ 1.96) = 0.95
P(|Z| ≤ 2) = 0.9545
P(|Z| ≤ 2.576) = 0.99
P(|Z| ≤ 3) = 0.9973
```

### Linear Transformation
```
X ~ N(μ, σ²) → Y = aX + b ~ N(aμ+b, a²σ²)

X₁ ~ N(μ₁, σ₁²), X₂ ~ N(μ₂, σ₂²):
X₁ + X₂ ~ N(μ₁+μ₂, σ₁²+σ₂²) [independent]
X₁ - X₂ ~ N(μ₁-μ₂, σ₁²+σ₂²) [independent]
```

### Standardization
```
Z = (X - μ)/σ

X = μ + σZ
```

---

## 6. Binomial Distribution Formulas

```
P(X = k) = C(n,k) p^k q^(n-k)  [q = 1-p]

E[X] = np

Var(X) = npq

σ = √(npq)

Skewness = (q-p)/√(npq)

Kurtosis = (1-6pq)/(npq)

P(X ≤ k) = Σ[i=0 to k] C(n,i) p^i q^(n-i)
```

### Important Relations
```
P(X = k+1)/P(X = k) = (n-k)p/((k+1)q)

Mode = floor((n+1)p) or floor((n+1)p) - 1

P(X = 0) = q^n
P(X = n) = p^n
```

### Normal Approximation
```
If n large: X ~ N(np, npq)

With continuity correction:
P(a ≤ X ≤ b) ≈ Φ((b+0.5-np)/√(npq)) - Φ((a-0.5-np)/√(npq))
```

---

## 7. Central Limit Theorem Formulas

```
If X₁, X₂, ..., Xₙ ~ iid(μ, σ²):

x̄ ~ N(μ, σ²/n) approximately for large n

z = (x̄ - μ)/(σ/√n) ~ N(0,1)

For proportions:
p̂ ~ N(p, p(1-p)/n) approximately

z = (p̂ - p)/√(p(1-p)/n) ~ N(0,1)
```

### Sample Size Requirements
```
For mean: n ≥ 30 (regardless of distribution)
For proportion: np ≥ 5 and n(1-p) ≥ 5
```

---

## 8. Exponential Distribution Formulas

```
f(x) = λe^(-λx) for x ≥ 0

F(x) = 1 - e^(-λx)

E[X] = 1/λ

Var(X) = 1/λ²

σ = 1/λ

Median = ln(2)/λ

P(X > x) = e^(-λx)

Memoryless: P(X > s+t | X > s) = P(X > t) = e^(-λt)

MGF: M(t) = λ/(λ-t) for t < λ
```

---

## 9. Chi-Squared Distribution Formulas

```
If Z₁, Z₂, ..., Zₖ ~ iid N(0,1):
χ² = Z₁² + Z₂² + ... + Zₖ² ~ χ²(k)

E[χ²] = k

Var[χ²] = 2k

Mode = max(k-2, 0)

If X ~ N(μ, σ²):
(n-1)S²/σ² ~ χ²(n-1)

χ²(a) + χ²(b) ~ χ²(a+b) [independent]
```

---

## 10. t-Distribution Formulas

```
If Z ~ N(0,1), V ~ χ²(k):
t = Z/√(V/k) ~ t(k)

E[t] = 0 for k > 1

Var(t) = k/(k-2) for k > 2

As k → ∞: t → N(0,1)

For confidence intervals:
x̄ ± t_{α/2, n-1} × s/√n
```

---

## 11. F-Distribution Formulas

```
If V₁ ~ χ²(k₁), V₂ ~ χ²(k₂):
F = (V₁/k₁)/(V₂/k₂) ~ F(k₁, k₂)

E[F] = k₂/(k₂-2) for k₂ > 2

Var(F) = 2k₂²(k₁+k₂-2)/(k₁(k₂-2)²(k₂-4)) for k₂ > 4

F_{α}(k₁, k₂) = 1/F_{1-α}(k₂, k₁)

Used in ANOVA: F = MS_between/MS_within
```

---

## 12. Correlation Formulas

### Pearson Correlation
```
r = Σ(xᵢ-x̄)(yᵢ-ȳ) / √[Σ(xᵢ-x̄)² × Σ(yᵢ-ȳ)²]
  = [nΣxy - (Σx)(Σy)] / √{[nΣx²-(Σx)²][nΣy²-(Σy)²]}

-1 ≤ r ≤ 1
r = 0: no linear correlation
|r| close to 1: strong linear correlation
```

### Spearman Rank Correlation
```
rₛ = 1 - (6Σdᵢ²)/(n(n²-1))

where dᵢ = rank(xᵢ) - rank(yᵢ)
```

### Coefficient of Determination
```
R² = r² = proportion of variance explained
```

---

## 13. Linear Regression Formulas

```
y = a + bx (simple linear regression)

b = Σ(xᵢ-x̄)(yᵢ-ȳ) / Σ(xᵢ-x̄)² = [nΣxy - (Σx)(Σy)] / [nΣx² - (Σx)²]

a = ȳ - bx̄

SST = Σ(yᵢ-ȳ)² (total sum of squares)
SSR = Σ(ŷᵢ-ȳ)² (regression sum of squares)
SSE = Σ(yᵢ-ŷᵢ)² (error sum of squares)

SST = SSR + SSE

R² = SSR/SST = 1 - SSE/SST
```

---

## 14. Hypothesis Testing Formulas

### z-test (known σ)
```
z = (x̄ - μ₀)/(σ/√n)

Reject H₀ if |z| > z_{α/2}
```

### t-test (unknown σ)
```
t = (x̄ - μ₀)/(s/√n)

Reject H₀ if |t| > t_{α/2, n-1}
```

### Confidence Intervals
```
Mean (σ known): x̄ ± z_{α/2} × σ/√n
Mean (σ unknown): x̄ ± t_{α/2, n-1} × s/√n
Proportion: p̂ ± z_{α/2} × √(p̂(1-p̂)/n)
```

### Sample Size
```
n = (z_{α/2} × σ/E)²  for estimating mean
n = (z_{α/2}/E)² × p(1-p)  for estimating proportion
```
