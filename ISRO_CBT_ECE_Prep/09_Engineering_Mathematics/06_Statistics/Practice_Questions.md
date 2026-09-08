# Statistics - Practice Questions

## Easy Level

### Q1. Mean Calculation
Find mean of: 3, 7, 5, 9, 1.

**Solution**:
- x̄ = (3+7+5+9+1)/5 = 25/5 = **5**

---

### Q2. Median
Find median of: 2, 5, 8, 3, 7.

**Solution**:
- Ordered: 2, 3, 5, 7, 8
- Median = **5**

---

### Q3. Variance
Find variance of: 2, 4, 6, 8.

**Solution**:
- x̄ = 5
- Σ(xᵢ-x̄)² = 9+1+1+9 = 20
- σ² = 20/4 = **5**

---

### Q4. Poisson Quick
X ~ Poisson(λ=2). Find P(X=0).

**Solution**:
- P(X=0) = e^(-2) × 2⁰ / 0! = e^(-2) = **0.1353**

---

### Q5. Uniform Mean
X ~ Unif(0, 10). Find E[X].

**Solution**:
- E[X] = (0+10)/2 = **5**

---

## Medium Level

### Q6. Normal Probability
X ~ N(50, 25). Find P(X > 55).

**Solution**:
- Z = (55-50)/5 = 1
- P(Z > 1) = 1 - 0.8413 = **0.1587**

---

### Q7. Binomial Distribution
X ~ Bin(20, 0.5). Find P(X = 10).

**Solution**:
- P(X=10) = C(20,10) × 0.5²⁰ = 184756 × 9.5367e-7 = **0.1762**

---

### Q8. Standard Deviation
Find σ for: 1, 3, 5, 7, 9.

**Solution**:
- x̄ = 5
- Σ(xᵢ-x̄)² = 16+4+0+4+16 = 40
- σ² = 40/5 = 8
- σ = **2√2 ≈ 2.828**

---

### Q9. Poisson Approximation
n = 500, p = 0.01. Find P(X ≤ 2) using Poisson.

**Solution**:
- λ = np = 5
- P(X ≤ 2) = e^(-5)(1 + 5 + 25/2) = e^(-5)(18.5) = **0.1247**

---

### Q10. Normal Approximation to Binomial
X ~ Bin(100, 0.4). Find P(X ≤ 45) approximately.

**Solution**:
- μ = 40, σ² = 24, σ = 4.899
- P(X ≤ 45) ≈ P(Z ≤ (45.5-40)/4.899) = P(Z ≤ 1.12) = **0.8686**

---

### Q11. Mode
Find mode of: 1, 2, 2, 3, 3, 3, 4, 4, 5.

**Solution**:
- Mode = **3** (appears most frequently)

---

### Q12. Coefficient of Variation
CV of two datasets: A (σ=5, μ=50) and B (σ=8, μ=100).

**Solution**:
- CV_A = (5/50) × 100% = **10%**
- CV_B = (8/100) × 100% = **8%**
- Dataset B is less variable relative to mean

---

### Q13. IQR
Find IQR of: 1, 3, 5, 7, 9, 11, 13.

**Solution**:
- Q₁ = 3, Q₃ = 11
- IQR = 11 - 3 = **8**

---

### Q14. Exponential Distribution
X ~ Exp(λ=2). Find P(X > 1).

**Solution**:
- P(X > 1) = e^(-2) = **0.1353**

---

### Q15. Standard Normal
Find z such that P(Z > z) = 0.05.

**Solution**:
- P(Z > z) = 0.05 → P(Z ≤ z) = 0.95
- z = **1.645**

---

## Hard Level

### Q16. CLT Application
Sample of 64 from population with μ=100, σ=16. Find P(x̄ > 104).

**Solution**:
- SE = 16/√64 = 2
- P(x̄ > 104) = P(Z > (104-100)/2) = P(Z > 2) = **0.0228**

---

### Q17. Confidence Interval
x̄ = 50, s = 10, n = 25. Find 95% CI for μ (unknown σ).

**Solution**:
- t_{0.025, 24} = 2.064
- CI = 50 ± 2.064 × (10/5) = 50 ± 4.128
- **CI = (45.872, 54.128)**

---

### Q18. Proportion
Sample: 200 people, 60 favor policy. Find 95% CI for proportion.

**Solution**:
- p̂ = 0.3
- SE = √(0.3×0.7/200) = 0.0324
- CI = 0.3 ± 1.96 × 0.0324
- **CI = (0.2365, 0.3635)**

---

### Q19. Skewness
Data: 1, 2, 2, 3, 3, 3, 4, 4, 5, 10.

**Solution**:
- Mean = 3.7, Median = 3, Mode = 3
- Mean > Median > Mode
- **Right skewed (positively skewed)**

---

### Q20. Regression Line
x: 1, 2, 3, 4, 5
y: 2, 4, 5, 4, 5

Find regression line y = a + bx.

**Solution**:
- x̄ = 3, ȳ = 4
- Σ(xᵢ-x̄)(yᵢ-ȳ) = (-2)(-2)+(-1)(0)+(0)(1)+(1)(0)+(2)(1) = 6
- Σ(xᵢ-x̄)² = 4+1+0+1+4 = 10
- b = 6/10 = 0.6
- a = 4 - 0.6(3) = 2.2
- **y = 2.2 + 0.6x**

---

### Q21. Chi-Squared
If X₁, X₂, X₃ ~ N(0,1), find P(X₁² + X₂² + X₃² > 7.815).

**Solution**:
- X₁² + X₂² + X₃² ~ χ²(3)
- P(χ²(3) > 7.815) = **0.05** (from chi-squared table)

---

### Q22. Conditional Probability (Statistics)
A: X > 5, B: X is even. X ~ Poisson(λ=3). Find P(A|B).

**Solution**:
- P(B) = P(X=0)+P(X=2)+P(X=4)+... = e^(-3)(1 + 4.5 + 3.375 + ...)
- P(A∩B) = P(X=6)+P(X=8)+... (even and >5)
- Calculate numerically

---

### Q23. Moment Generating Function
X ~ Exponential(λ=2). Find E[X²] using MGF.

**Solution**:
- M(t) = 2/(2-t)
- M'(t) = 2/(2-t)²
- M''(t) = 4/(2-t)³
- M''(0) = 4/8 = 0.5
- **E[X²] = 0.5**

---

### Q24. Bayes in Statistics
Prior: P(disease) = 0.01. Test: sensitivity = 0.99, specificity = 0.95. Find P(disease|+).

**Solution**:
- P(+) = 0.99(0.01) + 0.05(0.99) = 0.0099 + 0.0495 = 0.0594
- P(D|+) = 0.0099/0.0594 = **0.1667**

---

### Q25. Kurtosis
Distribution has excess kurtosis = 2. What does this mean?

**Solution**:
- Excess kurtosis = γ₂ = 2 > 0
- **Leptokurtic**: heavier tails and more peaked than normal

---

## ISRO-Focused Questions

### Q26. Poisson Rate
If average is 3 events per hour, what is P(exactly 5 in 2 hours)?

**Solution**:
- λ = 3 × 2 = 6
- P(X=5) = e^(-6) × 6⁵ / 5! = e^(-6) × 7776 / 120 = **0.1606**

---

### Q27. Uniform Probability
X ~ Unif(0, 20). Find P(5 < X < 15).

**Solution**:
- P = (15-5)/20 = 10/20 = **0.5**

---

### Q28. Normal Quick
X ~ N(100, 100). Find P(90 < X < 110).

**Solution**:
- Z₁ = (90-100)/10 = -1, Z₂ = (110-100)/10 = 1
- P(-1 < Z < 1) = **0.6827**

---

### Q29. CLT Quick
n = 100, μ = 50, σ = 10. What is the distribution of x̄?

**Solution**:
- x̄ ~ N(50, 100/100) = N(50, 1)
- **x̄ ~ N(50, 1)**

---

### Q30. Standard Deviation Quick
X takes values 0, 1, 2 with probabilities 0.25, 0.5, 0.25. Find σ.

**Solution**:
- E[X] = 0 + 0.5 + 0.5 = 1
- E[X²] = 0 + 0.5 + 1 = 1.5
- Var(X) = 1.5 - 1 = 0.5
- σ = **√0.5 ≈ 0.707**
