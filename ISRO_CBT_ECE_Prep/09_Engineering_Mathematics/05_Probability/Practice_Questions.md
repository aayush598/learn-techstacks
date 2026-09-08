# Probability - Practice Questions

## Easy Level

### Q1. Basic Probability
A die is rolled. Find P(even number).

**Solution**:
- Even outcomes: {2, 4, 6} → 3 outcomes
- P(even) = 3/6 = **1/2**

---

### Q2. Addition Rule
P(A) = 0.5, P(B) = 0.3, P(A∩B) = 0.1. Find P(A∪B).

**Solution**:
- P(A∪B) = 0.5 + 0.3 - 0.1 = **0.7**

---

### Q3. Conditional Probability
P(A∩B) = 0.2, P(B) = 0.5. Find P(A|B).

**Solution**:
- P(A|B) = 0.2/0.5 = **0.4**

---

### Q4. Independence Check
P(A) = 0.6, P(B) = 0.4, P(A∩B) = 0.24. Are A and B independent?

**Solution**:
- P(A)·P(B) = 0.6 × 0.4 = 0.24 = P(A∩B)
- **Yes, independent**

---

### Q5. Complement
P(A) = 0.7. Find P(A').

**Solution**:
- P(A') = 1 - 0.7 = **0.3**

---

## Medium Level

### Q6. Bayes' Theorem
A factory has machines A (60%) and B (40%). A produces 2% defective, B produces 3% defective. A randomly selected item is defective. Find P(A|defective).

**Solution**:
- P(A) = 0.6, P(B) = 0.4
- P(D|A) = 0.02, P(D|B) = 0.03
- P(D) = 0.6(0.02) + 0.4(0.03) = 0.024
- P(A|D) = (0.02)(0.6)/0.024 = 0.012/0.024 = **0.5**

---

### Q7. Total Probability
Balls in urns: Urn1 (3 red, 7 blue), Urn2 (6 red, 4 blue). Choose urn with equal probability, then pick a ball. Find P(red).

**Solution**:
- P(R) = P(R|U1)P(U1) + P(R|U2)P(U2)
- = (0.3)(0.5) + (0.6)(0.5) = 0.15 + 0.3 = **0.45**

---

### Q8. Binomial Distribution
X ~ Bin(10, 0.3). Find P(X = 3).

**Solution**:
- P(X=3) = C(10,3)(0.3)³(0.7)⁷
- = 120 × 0.027 × 0.0824 = **0.2668**

---

### Q9. Poisson Distribution
Calls arrive at rate λ = 4/hour. Find P(exactly 2 calls in an hour).

**Solution**:
- P(X=2) = e^(-4) × 4² / 2! = e^(-4) × 16 / 2
- = 0.0183 × 8 = **0.1465**

---

### Q10. Expectation
E[X] = 5, E[Y] = 3. Find E[X + Y].

**Solution**:
- E[X + Y] = E[X] + E[Y] = 5 + 3 = **8**

---

### Q11. Variance
Var(X) = 4. Find Var(2X + 3).

**Solution**:
- Var(2X + 3) = 4 × Var(X) = 4 × 4 = **16**

---

### Q12. Normal Distribution
X ~ N(100, 25). Find P(X > 110).

**Solution**:
- Z = (110-100)/5 = 2
- P(X > 110) = P(Z > 2) = 1 - Φ(2) = 1 - 0.9772 = **0.0228**

---

### Q13. Uniform Distribution
X ~ Unif(2, 8). Find P(3 < X < 6).

**Solution**:
- f(x) = 1/(8-2) = 1/6
- P(3 < X < 6) = (6-3)/6 = 3/6 = **0.5**

---

### Q14. Conditional Probability
P(A) = 0.4, P(B|A) = 0.7, P(B|A') = 0.2. Find P(B).

**Solution**:
- P(B) = P(B|A)P(A) + P(B|A')P(A')
- = 0.7 × 0.4 + 0.2 × 0.6 = 0.28 + 0.12 = **0.4**

---

### Q15. Chain Rule
P(A₁) = 0.5, P(A₂|A₁) = 0.6, P(A₃|A₁∩A₂) = 0.8. Find P(A₁∩A₂∩A₃).

**Solution**:
- P(A₁∩A₂∩A₃) = 0.5 × 0.6 × 0.8 = **0.24**

---

## Hard Level

### Q16. Bayes' (Three Hospitals)
Hospitals A(20%), B(30%), C(50%) deliver babies. A: 5% premature, B: 6%, C: 8%. Find P(C|premature).

**Solution**:
- P(P) = 0.2(0.05) + 0.3(0.06) + 0.5(0.08) = 0.01 + 0.018 + 0.04 = 0.068
- P(C|P) = (0.08 × 0.5)/0.068 = 0.04/0.068 = **0.5882**

---

### Q17. Geometric Distribution
P(success) = 0.25. Find P(first success on 4th trial).

**Solution**:
- P(X=4) = (0.75)³ × 0.25 = 0.4219 × 0.25 = **0.1055**

---

### Q18. Variance of Sum
Var(X) = 3, Var(Y) = 4, Cov(X,Y) = 1. Find Var(X+Y).

**Solution**:
- Var(X+Y) = Var(X) + Var(Y) + 2Cov(X,Y)
- = 3 + 4 + 2(1) = **9**

---

### Q19. Normal (Standardization)
X ~ N(50, 16). Find P(46 < X < 54).

**Solution**:
- Z₁ = (46-50)/4 = -1, Z₂ = (54-50)/4 = 1
- P(-1 < Z < 1) = 2Φ(1) - 1 = 2(0.8413) - 1 = **0.6826**

---

### Q20. Exponential Distribution
X ~ Exp(λ = 0.5). Find P(X > 2).

**Solution**:
- P(X > 2) = e^(-0.5×2) = e^(-1) = **0.3679**

---

### Q21. Poisson Approximation to Binomial
n = 1000, p = 0.001. Find P(X = 0) using Poisson approximation.

**Solution**:
- λ = np = 1
- P(X = 0) = e^(-1) × 1⁰ / 0! = e^(-1) = **0.3679**

---

### Q22. Conditional Expectation
Joint distribution: f(x,y) = x+y for 0 < x,y < 1. Find E[X|Y = 0.5].

**Solution**:
- f_{X|Y}(x|0.5) = f(x,0.5)/f_Y(0.5)
- f_Y(y) = ∫[0,1] (x+y) dx = 1/2 + y → f_Y(0.5) = 1
- f_{X|Y}(x|0.5) = x + 0.5
- E[X|Y=0.5] = ∫[0,1] x(x+0.5) dx = ∫[0,1] (x²+0.5x) dx
- = [x³/3 + x²/4]₀¹ = 1/3 + 1/4 = **7/12**

---

### Q23. Moment Generating Function
X ~ Poisson(λ). Find E[X²] using MGF.

**Solution**:
- M(t) = e^(λ(e^t-1))
- M'(t) = λe^t · M(t)
- M''(t) = λe^t · M(t) + λ²e^(2t) · M(t)
- M''(0) = λ + λ²
- **E[X²] = λ + λ²**

---

### Q24. Law of Total Variance
X|Y ~ N(Y, 1), Y ~ N(0, 4). Find Var(X).

**Solution**:
- E[X|Y] = Y, Var(X|Y) = 1
- Var(X) = E[Var(X|Y)] + Var(E[X|Y])
- = E[1] + Var(Y) = 1 + 4 = **5**

---

### Q25. Correlation
X ~ N(0,1), Y = 2X + 3. Find ρ(X,Y).

**Solution**:
- Cov(X,Y) = Cov(X, 2X+3) = 2Var(X) = 2
- σ_X = 1, σ_Y = 2
- ρ = 2/(1×2) = **1** (perfect correlation)

---

## ISRO-Focused Questions

### Q26. Quick Bayes
P(Disease) = 0.01, P(+|Disease) = 0.95, P(+|No Disease) = 0.05. Find P(Disease|+).

**Solution**:
- P(+) = 0.95(0.01) + 0.05(0.99) = 0.0095 + 0.0495 = 0.059
- P(D|+) = 0.0095/0.059 = **0.161** (about 16%)

---

### Q27. Poisson Quick
λ = 3. Find P(X = 1).

**Solution**:
- P(X=1) = e^(-3) × 3¹ / 1! = 3e^(-3) = 3 × 0.0498 = **0.1494**

---

### Q28. Normal Quick
X ~ N(0,1). Find P(Z > 0).

**Solution**:
- Normal distribution is symmetric about mean
- P(Z > 0) = **0.5**

---

### Q29. Uniform Quick
X ~ Unif(0, 10). Find P(X > 7).

**Solution**:
- P(X > 7) = (10-7)/10 = 3/10 = **0.3**

---

### Q30. Independence Quick
A, B independent, P(A) = 0.4, P(B) = 0.5. Find P(A∪B).

**Solution**:
- P(A∪B) = P(A) + P(B) - P(A)P(B)
- = 0.4 + 0.5 - 0.2 = **0.7**
