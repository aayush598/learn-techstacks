# Statistics - Concepts

## 1. Measures of Central Tendency

### Mean (Arithmetic)
```
Population: μ = (Σ xᵢ) / N
Sample: x̄ = (Σ xᵢ) / n
```

### Weighted Mean
```
x̄_w = Σ(wᵢxᵢ) / Σwᵢ
```

### Median
- Middle value when data is ordered
- For even n: average of n/2 and (n/2+1)th values
- Robust to outliers

### Mode
- Most frequently occurring value
- Can be multimodal

### Relationships
- **Symmetric**: Mean = Median = Mode
- **Right skewed**: Mean > Median > Mode
- **Left skewed**: Mean < Median < Mode

---

## 2. Measures of Dispersion

### Range
```
Range = Maximum - Minimum
```

### Variance
```
Population: σ² = Σ(xᵢ-μ)²/N
Sample: s² = Σ(xᵢ-x̄)²/(n-1)
```

### Standard Deviation
```
σ = √(variance)
```

### Coefficient of Variation
```
CV = (σ/μ) × 100%
```

### Mean Absolute Deviation
```
MAD = Σ|xᵢ - x̄| / n
```

---

## 3. Poisson Distribution

### Definition
```
P(X = k) = e^(-λ) λ^k / k!  for k = 0, 1, 2, ...
```

### Parameters
- λ > 0 (rate parameter)
- λ = mean = variance

### Properties
- Models rare events
- Memoryless property (for inter-arrival times)
- Sum of Poissons: X₁ ~ Poisson(λ₁), X₂ ~ Poisson(λ₂) → X₁+X₂ ~ Poisson(λ₁+λ₂)

### When to Use
- Number of events in fixed interval
- Events occur independently
- Average rate is constant
- No simultaneous events

---

## 4. Uniform Distribution

### Continuous Uniform
```
f(x) = 1/(b-a) for a ≤ x ≤ b
F(x) = (x-a)/(b-a)
```

### Properties
```
E[X] = (a+b)/2
Var(X) = (b-a)²/12
```

### Discrete Uniform
```
P(X = k) = 1/n for k = 1, 2, ..., n
E[X] = (n+1)/2
Var(X) = (n²-1)/12
```

---

## 5. Normal Distribution

### Definition
```
f(x) = (1/(σ√(2π))) e^(-(x-μ)²/(2σ²))
```

### Standard Normal
```
Z = (X - μ)/σ ~ N(0,1)
φ(z) = (1/√(2π)) e^(-z²/2)
Φ(z) = P(Z ≤ z)
```

### Properties
- Symmetric about μ
- Mean = Median = Mode = μ
- Empirical Rule:
  - P(μ-σ < X < μ+σ) ≈ 68.27%
  - P(μ-2σ < X < μ+2σ) ≈ 95.45%
  - P(μ-3σ < X < μ+3σ) ≈ 99.73%

### Linear Combination
```
X ~ N(μ,σ²) → aX + b ~ N(aμ+b, a²σ²)
X₁ ~ N(μ₁,σ₁²), X₂ ~ N(μ₂,σ₂²) → X₁+X₂ ~ N(μ₁+μ₂, σ₁²+σ₂²)
```

### Central Limit Theorem Application
```
x̄ ~ N(μ, σ²/n) for large n (n ≥ 30)
```

---

## 6. Binomial Distribution

### Definition
```
P(X = k) = C(n,k) p^k (1-p)^(n-k)  for k = 0, 1, ..., n
```

### Parameters
- n: number of trials
- p: probability of success
- q = 1-p: probability of failure

### Properties
```
E[X] = np
Var(X) = npq
Skewness = (q-p)/√(npq)
```

### Special Cases
- n = 1: Bernoulli distribution
- Large n, small p: Poisson approximation (λ = np)
- Large n: Normal approximation (μ = np, σ² = npq)

---

## 7. Central Limit Theorem (CLT)

### Statement
```
If X₁, X₂, ..., Xₙ are iid with mean μ and variance σ², then:

z = (x̄ - μ) / (σ/√n) → N(0,1) as n → ∞
```

### Practical Implications
- Sample mean x̄ is approximately normal for n ≥ 30
- Distribution of population doesn't matter
- Approximation improves with larger n

### Applications
- Confidence intervals for mean
- Hypothesis testing
- Quality control

---

## 8. Other Important Distributions

### Exponential
```
f(x) = λe^(-λx) for x ≥ 0
E[X] = 1/λ, Var(X) = 1/λ²
Memoryless: P(X > s+t | X > s) = P(X > t)
```

### Chi-Squared
```
If Z₁, Z₂, ..., Zₖ ~ iid N(0,1):
χ² = Z₁² + Z₂² + ... + Zₖ² ~ χ²(k)
E[χ²] = k, Var[χ²] = 2k
```

### t-Distribution
```
If Z ~ N(0,1), V ~ χ²(k):
t = Z/√(V/k) ~ t(k)
Heavy tails, approaches normal as k → ∞
```

### F-Distribution
```
If V₁ ~ χ²(k₁), V₂ ~ χ²(k₂):
F = (V₁/k₁)/(V₂/k₂) ~ F(k₁, k₂)
Used in ANOVA, regression analysis
```

---

## 9. Sampling Distributions

### Sampling Distribution of Mean
```
For population with mean μ, variance σ²:
x̄ has mean μ and variance σ²/n
If population normal or n ≥ 30: x̄ ~ N(μ, σ²/n)
```

### Standard Error
```
SE(x̄) = σ/√n  [known σ]
SE(x̄) = s/√n  [unknown σ]
```

### Finite Population Correction
```
If sampling without replacement from finite population:
SE = (σ/√n) × √((N-n)/(N-1))
```

---

## 10. Descriptive Statistics

### Five-Number Summary
```
Minimum, Q₁, Median (Q₂), Q₃, Maximum
```

### Interquartile Range
```
IQR = Q₃ - Q₁
Outliers: values outside [Q₁ - 1.5×IQR, Q₃ + 1.5×IQR]
```

### Skewness
```
γ₁ = E[(X-μ)³]/σ³

γ₁ > 0: right skewed
γ₁ < 0: left skewed
γ₁ = 0: symmetric
```

### Kurtosis
```
γ₂ = E[(X-μ)⁴]/σ⁴ - 3

γ₂ > 0: leptokurtic (heavy tails)
γ₂ < 0: platykurtic (light tails)
γ₂ = 0: mesokurtic (normal-like)
```

---

## 11. Correlation and Regression

### Pearson Correlation
```
r = Σ(xᵢ-x̄)(yᵢ-ȳ) / √[Σ(xᵢ-x̄)² × Σ(yᵢ-ȳ)²]
-1 ≤ r ≤ 1
```

### Spearman Rank Correlation
```
rₛ = 1 - (6Σdᵢ²)/(n(n²-1))
where dᵢ = rank difference
```

### Simple Linear Regression
```
y = a + bx

b = Σ(xᵢ-x̄)(yᵢ-ȳ) / Σ(xᵢ-x̄)²
a = ȳ - bx̄
```

---

## 12. Hypothesis Testing Basics

### Null and Alternative
```
H₀: null hypothesis (status quo)
H₁: alternative hypothesis (what we want to prove)
```

### Test Statistics
```
z = (x̄ - μ₀)/(σ/√n)  [known σ]
t = (x̄ - μ₀)/(s/√n)  [unknown σ]
```

### Type I and Type II Errors
```
Type I (α): Reject H₀ when H₀ is true
Type II (β): Fail to reject H₀ when H₁ is true
Power = 1 - β
```

### p-value
```
p-value = P(test statistic ≥ observed value | H₀ true)

If p-value < α: reject H₀
If p-value ≥ α: fail to reject H₀
```
