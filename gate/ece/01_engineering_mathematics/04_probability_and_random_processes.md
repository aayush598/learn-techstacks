# Engineering Mathematics — Part 4: Probability & Random Processes

> Part 4 of 5 in the Engineering Mathematics question bank · 234 questions · Q1–Q234
> Read this file top to bottom, in order. It continues from `02_linear_algebra_and_multivariable.md`
> and is the last file of the subject.
>
> **Covers:** axiomatic probability, random variables and their distributions, every standard
> discrete and continuous distribution used in engineering, multivariate statistics and
> transformations, linear systems driven by random inputs, discrete and continuous random
> processes, wide-sense and strict-sense stationarity, ergodicity, power spectral density, and
> the mean-square behaviour of LTI systems under noise.
> **Assumes:** elementary set theory, single- and double-variable calculus (including
> convolution integrals), and complex exponentials. No prior probability background is needed —
> every definition used here is introduced in the question that needs it.

**Question count: 234** · Difficulty mix ≈ 15% recall, 20% quick application, 25% medium
problems, 20% GATE 1-mark MCQ, 20% GATE 2-mark MCQ/NAT/MSQ. Section 3 (standard distributions)
carries the heaviest weight, matching its share of real GATE papers.

---

## Section 1. Probability: axioms, conditional probability, Bayes and reliability (Q1–Q22)

### Q1. State the three axioms of probability and explain what each one is really saying.

> **Type:** Theory
> **Answer:** (i) Non-negativity, 0 ≤ P(A) ≤ 1 for every event A. (ii) Normalisation, P(S) = 1 for the whole sample space S. (iii) Countable additivity, if A₁, A₂, … are pairwise mutually exclusive (disjoint) then P(∪Aᵢ) = Σ P(Aᵢ). Also implied: P(∅) = 0 and P(Aᶜ) = 1 − P(A).
> **Solution:** These are the Kolmogorov axioms; together with the requirement that P is a set function on a σ-algebra they are the accepted definition of probability. Non-negativity makes P a real weight, normalisation fixes the scale so that the certain event has weight 1, and countable additivity is what makes probability behave like an area. P(∅)=0 follows from (iii) with one empty set, and P(Aᶜ)=1−P(A) follows from additivity applied to the disjoint pair {A, Aᶜ} plus normalisation.
> **Key point:** P(Aᶜ) = 1 − P(A) is a direct consequence of additivity + normalisation, not an extra axiom.

### Q2. A fair die is rolled twice. Write the sample space, and compute the probability that the sum of the two rolls equals 7 and that the first roll is 6.

> **Type:** Numerical
> **Answer:** S = {(i,j) : i,j ∈ {1,…,6}}, 36 equally likely outcomes. P(sum = 7) = 6/36 = 1/6 ≈ 0.1667. P(first roll = 6 and sum = 7) = 1/36 ≈ 0.02778.
> **Solution:** The outcomes summing to 7 are (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) — six of the 36, so 1/6. Given the first roll is 6, the second must be 1, a single outcome, so 1/36. Note the second is exactly 1/6 of the first, which is the conditional probability P(sum=7 | first=6) = 1/6.
> **Key point:** With equally likely outcomes, probability = (favourable count)/(total count).

### Q3. Give the subtraction rule and the product rule, and show the subtraction rule follows from the addition rule.

> **Type:** Theory
> **Answer:** P(A ∪ B) = P(A) + P(B) − P(A ∩ B) and P(A ∩ B) = P(A)·P(B|A). Subtraction: since A ∪ B = A ∪ (B ∩ Aᶜ) with A and (B ∩ Aᶜ) disjoint, P(A∪B) = P(A) + P(B∩Aᶜ) = P(A) + P(B) − P(A∩B).
> **Solution:** The two pieces A and (B ∩ Aᶜ) are disjoint, so additivity gives the first step; P(B ∩ Aᶜ) = P(B) − P(A∩B) because B = (A∩B) ∪ (Aᶜ∩B) is a disjoint union. The product rule is simply the definition of conditional probability rearranged: P(A|B) = P(A∩B)/P(B), valid for P(B) > 0.
> **Key point:** P(A∪B) = P(A) + P(B) − P(A∩B); you only omit the last term if A and B are mutually exclusive.

### Q4. Explain why the "classical" (equally likely outcomes) definition of probability cannot be used to assign a probability to "a real number chosen at random from [0,1] is exactly 0.4".

> **Type:** Conceptual
> **Answer:** The classical definition needs a finite number of equally likely outcomes, but [0,1] is continuous and its singletons have measure zero, so the requested event contains zero elements of "equal share". P({0.4}) = 0, yet P(X = 0.4) = 0 does not mean the event is impossible in the everyday sense — it means a single exact value has zero probability. What is well defined is P(X ≤ 0.4) = 0.4.
> **Solution:** Splitting [0,1] into n equal pieces and asking that 0.4 fall in one of them, the natural limit gives 0. The event is a single point; under Lebesgue measure every point has measure zero and the total measure of the interval is 1, so no finite counting argument can ever settle it. This failure of the combinatorial definition for continuous sample spaces is exactly why Kolmogorov's measure-theoretic definition replaced it.
> **Key point:** A single exact value of a continuous RV has probability 0; only intervals and points-in-intervals have nonzero probability.

### Q5. Two events A and B in a sample space satisfy P(A) = 0.5, P(B) = 0.5 and P(A ∪ B) = 0.8. What can you conclude?

> **Type:** MCQ (GATE-1)
> **Answer:** P(A ∩ B) = 0.2 and the events are **not** independent. (Option c)
>
> (a) A and B are independent
> (b) A and B are mutually exclusive
> (c) P(A ∩ B) = 0.2, so they are not independent
> (d) P(A ∩ B) = 0.25
> **Solution:** By the subtraction rule, P(A∩B) = 0.5 + 0.5 − 0.8 = 0.2. Independence would require P(A∩B) = P(A)P(B) = 0.25, which is not 0.2, so (a) fails. Mutual exclusion would require P(A∩B) = 0, which it is not, so (b) fails and (c) is the only consistent choice.
> **Key point:** Trap: students often set P(A∩B) = P(A)P(B) reflexively; that equality is the *test* for independence, not a law.

### Q6. Two dice are rolled. A = "the sum is even", B = "the first die shows 4". Are A and B independent? Justify numerically.

> **Type:** Conceptual
> **Answer:** The two events **are** independent: P(A) = 18/36 = 0.5, P(B) = 6/36 = 1/6 ≈ 0.1667, P(A∩B) = 3/36 = 1/12 ≈ 0.08333, and P(A)P(B) = 0.5 × 1/6 = 1/12 = 0.08333.
> **Solution:** The first die is even in half of the 36 outcomes, so P(A) = 0.5. Fixing the first die to 4 leaves six outcomes, so P(B) = 6/36 = 1/6. For the intersection, the first die is 4 (even) and the sum is even only when the second die is even, giving three outcomes and P(A∩B) = 3/36 = 1/12. Since 0.08333 equals P(A)P(B) exactly, the events are independent even though the parity structure looks as if it should couple them.
> **Key point:** Parity intuition misleads: "first die is 4" fixes the parity of the sum, yet the counts still satisfy P(A∩B) = P(A)P(B) = 1/12.

### Q7. Define conditional probability and extend it to three events using the chain rule.

> **Type:** Theory
> **Answer:** P(A|B) = P(A∩B)/P(B) for P(B) > 0. Chain rule: P(A∩B∩C) = P(A)·P(B|A)·P(C|A∩B), and in general P(∩_{i=1}^{n} Aᵢ) = P(A₁)∏_{i=2}^{n} P(Aᵢ | A₁∩…∩A_{i−1}).
> **Solution:** Conditional probability is the fraction of B's probability mass that also lies in A, so it renormalises the counting to the reduced sample space. The chain rule simply collapses two conditional probabilities at a time, and is the only correct way to multiply three probabilities — P(A)P(B)P(C) is valid only when all three are mutually independent.
> **Key point:** P(A∩B∩C) = P(A)P(B|A)P(C|A∩B); dropping the conditionals requires mutual independence.

### Q8. A system contains three sensors that fail independently with probabilities 0.1, 0.2 and 0.05. What is the probability that all three operate, and what is the probability that at least two operate?

> **Type:** Numerical
> **Answer:** P(all three work) = 0.9 × 0.8 × 0.95 = 0.684; P(at least two work) = 0.967.
> **Solution:** The all-work probability is the product of the survival probabilities: 0.9 × 0.8 = 0.72, then 0.72 × 0.95 = 0.684. For "at least two", the three mutually exclusive exactly-two cases are: sensors 1,2 work and 3 fails, 0.9 × 0.8 × 0.05 = 0.036; sensors 1,3 work and 2 fails, 0.9 × 0.2 × 0.95 = 0.171; sensors 2,3 work and 1 fails, 0.1 × 0.8 × 0.95 = 0.076. Their sum is 0.036 + 0.171 + 0.076 = 0.283, and adding the all-three case gives 0.684 + 0.283 = 0.967.
> **Key point:** "At least two" = all-three + the three exactly-two cases = 0.684 + 0.283 = 0.967.

### Q9. State Bayes' theorem and say what each symbol means, then give the "inversion" form used for engineering diagnosis.

> **Type:** Theory
> **Answer:** P(A|B) = P(B|A)·P(A) / P(B), where P(A) is the prior, P(B|A) the likelihood, P(B) the evidence (marginal) and P(A|B) the posterior. In diagnosis: P(fault|reading) = P(reading|fault)·P(fault) / P(reading), with the evidence expanded as P(reading) = P(reading|fault)P(fault) + P(reading|no fault)P(no fault).
> **Solution:** Bayes' theorem is the product rule with the conditioning reversed, plus the total-probability formula to eliminate P(B). Inverting a joint distribution this way is the only way to move from a known sensor characteristic to a fault probability, and the denominator normalisation is what stops the answer exceeding 1.
> **Key point:** Bayes needs the marginal P(B), which is the usual source of error — the two-term expansion is mandatory.

### Q10. A disease affects 0.4% of a population. A test has sensitivity 0.99 (detects the disease when present) and specificity 0.95 (correctly clears a healthy person). A person tests positive. What is the probability that they actually have the disease?

> **Type:** Numerical
> **Answer:** ≈ 0.0737 (7.37%).
> **Solution:** Prior P(D) = 0.004, so P(Dᶜ) = 0.996. P(+|D) = 0.99 and P(+|Dᶜ) = 0.05. By Bayes, P(D|+) = 0.99 × 0.004 / (0.99 × 0.004 + 0.05 × 0.996) = 0.00396 / (0.00396 + 0.0498) = 0.00396 / 0.05376 ≈ 0.07366. So even a 99%-sensitive test leaves roughly a 93% chance of being wrong for a positive, because the base rate is so low.
> **Key point:** With a rare fault, the false positives swamp the true positives; precision ≈ sensitivity × prevalence only when the test is very specific.

### Q11. In a factory of 10 000 components, 1% are defective. A test flags an item as defective with probability 0.95 if it is defective and 0.05 if it is sound. Of every 10 000 tested items, how many are flagged defective, and what fraction of those flagged are truly defective?

> **Type:** Numerical
> **Answer:** 590 items are flagged; 95 of them (≈ 16.1%) are truly defective.
> **Solution:** True defectives = 0.01 × 10 000 = 100; of these 0.95 × 100 = 95 are flagged. Sound items = 9900; of these 0.05 × 9900 = 495 are wrongly flagged. Total flagged = 95 + 495 = 590. The precision is 95/590 ≈ 0.1610. The same number follows from Bayes: 0.95 × 0.01 / (0.95 × 0.01 + 0.05 × 0.99) = 0.0095/0.059 = 0.1610.
> **Key point:** 100 defective items generate 495 false alarms — improving the test's sensitivity helps far less than raising the base rate.

### Q12. For what value of P(A) are the events A and B (with P(B) = 0.6) mutually exclusive **and** independent simultaneously?

> **Type:** Numerical
> **Answer:** P(A) = 0.
> **Solution:** Mutual exclusion gives P(A∩B) = 0. Independence demands P(A∩B) = P(A)P(B) = 0.6 P(A). Setting 0.6 P(A) = 0 forces P(A) = 0. So the only way to be both mutually exclusive and independent (for a genuinely random B with P(B) ≠ 0,1) is for one of them to be the impossible event. This is the standard "independent and exclusive ⟹ trivial" result.
> **Key point:** Independent and mutually exclusive simultaneously ⟹ P(A)P(B) = 0 ⟹ at least one event is impossible.

### Q13. Two components with reliabilities R₁ = 0.9 and R₂ = 0.8 are connected in **series**. What is the system reliability, and what reliability would the third identical-to-R₂ component in parallel with R₂ give?

> **Type:** Numerical
> **Answer:** Series reliability = 0.9 × 0.8 = 0.72. With the third component (R = 0.8) placed in parallel with R₂: R₂∥₃ = 1 − (1−0.8)² = 1 − 0.04 = 0.96, so the system becomes 0.9 × 0.96 = 0.864.
> **Solution:** A series system works only if every element works, and with independent elements that is the product of the reliabilities. A parallel (redundant) pair works if at least one works, which is the complement of "both fail": 1 − (0.2)(0.2) = 0.96. Redundancy lifted the R₂ stage from 0.8 to 0.96, a 20% relative gain on that stage and 0.72 → 0.864 overall.
> **Key point:** Series reliability = product; parallel reliability = 1 − product of failure probabilities.

### Q14. A single unit has an exponential lifetime with failure rate λ = 0.02 per hour. Two such units are (a) in series and (b) fully active parallel. Compute the reliability functions and the mean time to failure of each configuration.

> **Type:** Numerical
> **Answer:** Series: R_s(t) = e^{−2λt} = e^{−0.04t}, MTTF = 1/(2λ) = 25 h. Parallel: R_p(t) = 1 − (1 − e^{−λt})² = 2e^{−λt} − e^{−2λt}, MTTF = 2/λ − 1/(2λ) = 1.5/λ = 75 h.
> **Solution:** A unit survives to t with e^{−λt} = e^{−0.02t}. In series both must survive, giving e^{−0.04t} and MTTF = ∫₀^∞ R dt = 1/0.04 = 25 h. In parallel at least one survives: 1 − (1−e^{−0.02t})², whose integral is 2/0.02 − 1/0.04 = 100 − 25 = 75 h. Note MTTF is the area under the reliability curve, and redundancy has tripled it relative to one unit's 50 h.
> **Key point:** MTTF = ∫₀^∞ R(t) dt; redundant exponential pair gives 1.5/λ versus 1/(2λ) in series.

### Q15. A "standby" (cold-redundant) system has one working unit of reliability R₁ = 0.95 and a standby unit of the same reliability R₂ = 0.95 that only operates after the first fails. The switch itself must work, with probability q = 0.98. Find the system reliability and compare it with fully active parallel operation of the same two units.

> **Type:** Comparison
> **Answer:** Cold standby: R = R₁ + (1 − R₁)·q·R₂ = 0.95 + 0.05 × 0.98 × 0.95 = 0.99655 ≈ 0.9966. Active parallel: R = 1 − (1 − 0.95)² = 0.9975. Cold standby is worse only because the switch is less than perfect; with a perfect switch both give 0.9975.
> **Solution:** The system works either because unit 1 never failed (probability R₁) or because unit 1 failed **and** the switch worked **and** unit 2 then functioned: (1 − R₁)qR₂. The two cases are mutually exclusive, so they add. Active parallel works if at least one of two always-running units survives, 1 − 0.05² = 0.9975, which is marginally better here. The usual engineering claim that standby beats active parallel relies on the standby unit not ageing, and is exactly reversed once switch failure is priced in.
> **Key point:** Cold-standby and active-parallel formulas coincide only for a perfect switch; with q < 1, active parallel wins.

### Q16. Twenty independent experiments are performed, each with probability p = 0.25 of "success". Find the probability of **no** success and the probability of **at least one** success.

> **Type:** Numerical
> **Answer:** P(no success) = 0.75²⁰ ≈ 0.003171; P(at least one) ≈ 0.9968.
> **Solution:** Each trial fails with probability 0.75, and by independence the product over 20 trials is 0.75²⁰. Computing: 0.75² = 0.5625, 0.75⁴ = 0.31641, 0.75⁸ = 0.100113, 0.75¹⁶ = 0.0100226, so 0.75²⁰ = 0.0100226 × 0.31641 = 0.0031712. The complement is 1 − 0.0031712 = 0.9968288 ≈ 0.9968.
> **Key point:** "At least one" is almost always easier via the complement: 1 − (1−p)ⁿ.

### Q17. A fair coin is tossed until the first head appears. What is the probability that the first head occurs on the 3rd toss? Write it as a series of two products.

> **Type:** Numerical
> **Answer:** (1/2)·(1/2)·(1/2) = 1/8 = 0.125.
> **Solution:** "First head on toss 3" means toss 1 = tail, toss 2 = tail, toss 3 = head, and the first two are independent of the third, so the probability is (1/2)(1/2)(1/2). The general rule for "first success on trial n" with success probability p is (1−p)^{n−1}p, which is the geometric PMF.
> **Key point:** P(first success on trial n) = (1−p)^{n−1} p — the geometric PMF.

### Q18. If A and B are independent events with P(A) = 0.3 and P(B) = 0.4, what is P(A ∪ B)?

> **Type:** MCQ (GATE-1)
> **Answer:** 0.58 (Option b)
>
> (a) 0.12
> (b) 0.58
> (c) 0.70
> (d) 0.88
> **Solution:** Independence gives P(A∩B) = 0.3 × 0.4 = 0.12, so by the subtraction rule P(A∪B) = 0.3 + 0.4 − 0.12 = 0.58. Option (a) is the intersection, and (c) is the sum, which would only be right if the events were mutually exclusive — the classic confusion between "independent" and "exclusive".
> **Key point:** P(A∪B) = P(A) + P(B) − P(A)P(B) for independent events, not P(A) + P(B).

### Q19. A component fails within one year with probability 0.1. Assuming failures are independent across years, what is the probability that the component survives at least 6 years, and what is the survival function if failures follow a constant hazard λ = 0.1 per year?

> **Type:** Numerical
> **Answer:** Memoryless: S(6) = (0.9)⁶ ≈ 0.5314; with a constant hazard λ = 0.1, S(t) = e^{−λt}, so S(6) = e^{−0.6} ≈ 0.5488.
> **Solution:** Under the memoryless assumption the annual failure probability stays 0.1 each year, so the six-year survival is 0.9⁶ = 0.531441. A constant hazard instead gives an exponential survival e^{−λt} = e^{−0.6} = 0.5488. The two answers are close but not equal — memorylessness is a property of the exponential, not a general property of "constant annual failure probability".
> **Key point:** Constant hazard λ ⟹ S(t) = e^{−λt}; (1−p)^{n} is the discrete-year approximation to it.

### Q20. Events A and B satisfy P(A) = 0.4 and P(B) = 0.5. You are told nothing about their relationship. What additional single quantity is enough to determine P(A ∪ B)?

> **Type:** Conceptual (missing-data)
> **Answer:** P(A ∩ B). With P(A∪B) = P(A) + P(B) − P(A∩B) = 0.9 − P(A∩B), the intersection probability is the only missing quantity. Useful anchors: P(A∩B) = 0 (mutually exclusive) gives 0.9; P(A∩B) = 0.2 (independent) gives 0.7.
> **Solution:** The subtraction rule isolates the union as 0.9 − P(A∩B), so the single intersection probability closes the problem. Notice that independence and mutual exclusion are the two extreme cases giving 0.7 and 0.9 respectively, and every value in between is achievable since 0 ≤ P(A∩B) ≤ 0.4.
> **Key point:** Given P(A) and P(B) only, P(A∪B) ranges over [max(P(A),P(B)), P(A)+P(B)] and is fixed once P(A∩B) is known.

### Q21. In a group of n people, each birthday is independently one of 365 days, equally likely. For n = 23, what is the probability that at least two people share a birthday?

> **Type:** Numerical
> **Answer:** P(collision) = 1 − ∏_{k=0}^{22} (365−k)/365 ≈ 0.5073 (i.e. just over one half).
> **Solution:** The complement is "all birthdays distinct", so P(all distinct) = ∏_{k=0}^{22}(1 − k/365) = 1 × (364/365)(363/365)…(343/365). Taking logs, Σ_{k=0}^{22} ln(1 − k/365) ≈ −Σk/365 − Σk²/(2·365²) − Σk³/(3·365³) = −(253/365) − (3795/266450) − (64009/145881375) = −0.693151 − 0.014245 − 0.000439 = −0.707835, so P(all distinct) = e^{−0.707835} ≈ 0.4926, and direct evaluation of the finite product gives 0.4927. Hence P(at least one shared birthday) = 1 − 0.4927 ≈ 0.5073 — the famous "23 people" result.
> **Key point:** The birthday result: P(all distinct among 23) ≈ 0.4927, so P(collision) ≈ 0.5073 — just over one half.

### Q22. A, B and C are three events. Give a condition, expressed in terms of their probabilities, under which all three are mutually independent, and state what the probability of their joint occurrence would be.

> **Type:** Conceptual
> **Answer:** Mutual independence requires P(A∩B) = P(A)P(B), P(A∩C) = P(A)P(C), P(B∩C) = P(B)P(C) **and** P(A∩B∩C) = P(A)P(B)P(C). Then P(A∩B∩C) = P(A)P(B)P(C).
> **Solution:** The pairwise conditions alone are not sufficient: the classical counterexample is A, B, C being the three events "sum of two dice ≤ 7", "first die odd", "second die odd" style constructions where every pair is independent but the triple is not. The full definition demands the equality for every one of the seven non-empty subsets. This is exactly the condition that lets you multiply probabilities of independent events directly.
> **Key point:** Pairwise independence does **not** imply mutual independence; the triple product identity must also hold.

---

## Section 2. Random variables, distributions, CDF, survival, hazard, moments and MGF (Q23–Q47)

### Q23. Define a random variable as a measurable function, and explain what "discrete" versus "continuous" means in terms of the size of pre-images.

> **Type:** Theory
> **Answer:** A random variable X is a (measurable) real-valued function X : S → ℝ. It is discrete if the set of values it can take, {x : P(X = x) > 0}, is countable; it is continuous if every single point has probability zero, P(X = x) = 0 for all x.
> **Solution:** Random variables are the numerical surrogates for events: an event A becomes the set {x : X(ω) ∈ A}, and probabilities of events become probabilities of value-sets. The countable-image condition is what lets you write a probability mass function summing to 1, whereas a continuous variable needs a density. Note that "continuous" does not mean the variable takes every real value, only that no single value carries mass.
> **Key point:** Discrete ⟺ some values carry nonzero mass; continuous ⟺ every single value has mass zero.

### Q24. Distinguish a probability mass function from a probability density function on the three counts that must be correct.

> **Type:** Theory
> **Answer:** A PMF p(x) satisfies p(x) ≥ 0 and Σ_x p(x) = 1 (a countable sum). A PDF f(x) satisfies f(x) ≥ 0 and ∫_{−∞}^{∞} f(x) dx = 1 (a continuous integral). The third count is a consequence: both must be non-increasing as a function of any super-set, so P(X ≤ a) ≤ P(X ≤ b) for a ≤ b, and probabilities of disjoint value sets add.
> **Solution:** The normalisation forms differ because discrete values carry mass and continuous values do not. The additivity/monotonicity requirement is shared: for disjoint sets S₁, S₂ the probabilities add, and that is what forces both forms to be non-negative and normalised. A useful corollary is that for continuous X, P(a < X < b) = ∫_a^b f(x) dx, and an interval of zero width has zero probability.
> **Key point:** PMF sums to 1, PDF integrates to 1; both must give additive probabilities on disjoint sets.

### Q25. A continuous RV X has PDF f(x) = k·x for 0 ≤ x ≤ 2 and 0 elsewhere. Find k and verify your answer.

> **Type:** Numerical
> **Answer:** k = 1/2, so f(x) = x/2 on [0, 2].
> **Solution:** Normalisation requires ∫₀² kx dx = k[x²/2]₀² = 2k = 1, hence k = 1/2. Verification: f(x) = x/2 is non-negative on [0,2], its integral is 1, and P(X = 1) = 0 while P(0 ≤ X ≤ 2) = 1 as required. The corresponding CDF is F(x) = x²/4 on [0,2].
> **Key point:** Always normalise first: ∫f = 1 determines the unknown constant, and non-negativity then bounds the support.

### Q26. State the relationship between the CDF F(x), the PDF f(x) and the survival function S(x), and say which object is discontinuous for a discrete variable.

> **Type:** Theory
> **Answer:** F(x) = P(X ≤ x) = ∫_{−∞}^{x} f(t) dt, so f(x) = dF/dx where the derivative exists; S(x) = P(X > x) = 1 − F(x). For a discrete variable F is a right-continuous step function with jumps of size p(x) at each point of support, and there is no PDF; for a continuous variable F is continuous and absolutely continuous.
> **Solution:** The three functions carry identical information: knowing any one of them determines the other two, and the density exists precisely when F is absolutely continuous. The identity S(x) = 1 − F(x) is the discrete complement rule in function form. It also explains why discrete variables need PMFs — the jump size of F at x is exactly P(X = x), which is how you read a PMF off a CDF.
> **Key point:** F(x) = P(X ≤ x), S(x) = 1 − F(x), f = F′; for discrete X the jump of F at x equals p(x).

### Q27. Given the CDF of a continuous RV X is F(x) = 1 − e^{−λx} for x ≥ 0 and 0 for x < 0, identify the distribution, the PDF, and the mean and variance.

> **Type:** Numerical
> **Answer:** X is exponential with rate λ. f(x) = λe^{−λx} for x ≥ 0. Mean = 1/λ, variance = 1/λ², standard deviation = 1/λ.
> **Solution:** Differentiating gives f(x) = λe^{−λx}, which is the exponential density with rate parameter λ (scale θ = 1/λ). The mean is E[X] = ∫₀^∞ xλe^{−λx}dx = 1/λ and E[X²] = 2/λ², giving Var = 2/λ² − 1/λ² = 1/λ². Note both the mean and the standard deviation equal 1/λ — a hallmark of the exponential.
> **Key point:** Exponential(rate λ): f = λe^{−λx}, mean = 1/λ, var = 1/λ²; the **scale** convention writes mean θ, var θ² with θ = 1/λ.

### Q28. The PDF of X is f(x) = 2(1 − x) for 0 ≤ x ≤ 1. Compute E[X], E[X²] and Var(X).

> **Type:** Numerical
> **Answer:** E[X] = 1/3 ≈ 0.3333, E[X²] = 1/6 ≈ 0.1667, Var(X) = 1/6 − 1/9 = 1/18 ≈ 0.0556.
> **Solution:** E[X] = ∫₀¹ x·2(1−x)dx = 2∫₀¹(x − x²)dx = 2[x²/2 − x³/3]₀¹ = 2(1/2 − 1/3) = 2(1/6) = 1/3. Then E[X²] = ∫₀¹ 2x²(1−x)dx = 2[x³/3 − x⁴/4]₀¹ = 2(1/3 − 1/4) = 2(1/12) = 1/6. Hence Var = 1/6 − (1/3)² = 1/6 − 1/9 = 1/18 ≈ 0.0556. The mean is well below 0.5 because the density is skewed toward 1.
> **Key point:** Var(X) = 1/18 ≈ 0.0556 and E[X] = 1/3; compute E[X] and E[X²] separately rather than inferring one from the other.

### Q29. Define the hazard (failure-rate) function and prove the product-limit (reliability) identity from it.

> **Type:** Theory
> **Answer:** h(t) = lim_{Δt→0} P(t < T ≤ t + Δt | T > t) = f(t)/S(t) = −d ln S(t)/dt. Integrating, ln S(t) = −∫₀^t h(u)du, so S(t) = exp(−∫₀^t h(u)du).
> **Solution:** Conditional on surviving to t, the chance of failing in the next infinitesimal interval is f(t)dt / S(t), which is the definition of the hazard. Since S'(t) = −f(t), we get S'(t)/S(t) = −h(t), i.e. the log-survival has derivative −h(t); integrating from 0 to t with S(0) = 1 gives the product-limit formula. Constant hazard h(t) = λ therefore reproduces the exponential, which is the memoryless law.
> **Key point:** S(t) = exp(−∫₀^t h(u)du); constant hazard ⟹ exponential survival, i.e. the memoryless property.

### Q30. Two components have independent exponential lifetimes with rates λ₁ and λ₂. Find the survival function of the system when they are in series, and identify the resulting distribution.

> **Type:** Numerical
> **Answer:** S(t) = e^{−λ₁t}·e^{−λ₂t} = e^{−(λ₁+λ₂)t}, so the system lifetime is exponential with rate λ₁ + λ₂.
> **Solution:** A series system lives only while both live, and independence multiplies the survivals. The sum of independent exponentials is exponential, with rate equal to the sum of the rates. With λ₁ = λ₂ = λ this gives 2λ and a mean of 1/(2λ), exactly the MTTF found in Q14 by integrating the series reliability.
> **Key point:** Sum of independent exponentials is exponential with rate = sum of rates (not the sum of mean lifetimes).

### Q31. State the definition of the moment-generating function and state the existence criterion that makes it uniquely determine the distribution.

> **Type:** Theory
> **Answer:** M_X(s) = E[e^{sX}] for a real s. If M_X(s) exists and is finite in some open interval containing s = 0, then the distribution of X is uniquely determined by M_X.
> **Solution:** Differentiating under the expectation sign, M_X′(0) = E[X] and M_X″(0) = E[X²], so the MGF generates all moments: E[Xⁿ] = M_X^{(n)}(0). The existence of the MGF in a neighbourhood of zero also guarantees all moments exist, and the uniqueness theorem says no two distributions share the same MGF. The characteristic function Φ_X(ω) = E[e^{jωX}] always exists, and is the MGF evaluated on the imaginary axis, s = jω.
> **Key point:** M_X^{(n)}(0) = E[Xⁿ]; an MGF finite near 0 exists ⟹ distribution is unique and all moments are finite.

### Q32. The MGF of X is M_X(s) = 1/(1 − 3s). Identify the distribution and its mean and variance.

> **Type:** Numerical
> **Answer:** X is exponential with **scale** 3 (rate λ = 1/3 ≈ 0.3333 per unit). Mean = 3, variance = 9.
> **Solution:** The exponential MGF is M(s) = λ/(λ − s). Writing 1/(1 − 3s) in that form gives 1/(1 − s/3), so the denominator is 1 − s/λ with λ = 1/3, equivalently λ = 1/3 per unit. Differentiating to confirm: M′(s) = 3(1−3s)^{−2} gives M′(0) = 3, and M″(s) = 18(1−3s)^{−3} gives M″(0) = 18, so Var = 18 − 3² = 9. Both match E[X] = 1/λ = 3 and Var = 1/λ² = 9 exactly.
> **Key point:** M(s) = 1/(1 − s/θ) means scale θ; M(s) = 1/(1 − 3s) is exponential with mean 3 and var 9, not mean 1/3 and var 1/9.

### Q33. Show that if X ~ N(μ, σ²) then E[X] and Var(X) can be recovered from the MGF, and write the MGF explicitly.

> **Type:** Numerical
> **Answer:** M_X(s) = e^{μs + σ²s²/2}; M′(0) = μ and M″(0) = μ² + σ², so E[X] = μ and Var = σ².
> **Solution:** Completing the square, e^{−(x−μ)²/(2σ²)} = e^{−x²/(2σ²) + μx/σ² − μ²/(2σ²)} splits the Gaussian integral into a constant, a factor e^{μs/σ²} and a standard Gaussian integral √(2πσ²)e^{σ²s²/2}. Normalising by 1/√(2πσ²) leaves M_X(s) = e^{μs + σ²s²/2}. Differentiating, M′(s) = (μ + σ²s)M_X(s) so M′(0) = μ, and M″(s) = (σ² + (μ+σ²s)²)M_X(s) giving M″(0) = σ² + μ², hence Var = M″(0) − M′(0)² = σ².
> **Key point:** MGF of N(μ,σ²) is e^{μs + σ²s²/2}; the variance enters as σ² (not σ) in the exponent.

### Q34. If X and Y are independent with MGFs M_X(s) and M_Y(s), what is the MGF of S = X + Y? Prove the result in one line.

> **Type:** Theory
> **Answer:** M_S(s) = M_X(s)·M_Y(s).
> **Solution:** M_S(s) = E[e^{s(X+Y)}] = E[e^{sX}e^{sY}], and by independence of X and Y the expectation of the product of the two functions factorises into the product of the expectations, E[e^{sX}]E[e^{sY}]. This gives the useful corollary that the MGF of the sum of n iid variables with MGF M is M(s)ⁿ, and the sum of independent normals is normal with summed means and summed variances.
> **Key point:** MGFs multiply for independent sums: M_{X+Y}(s) = M_X(s)M_Y(s).

### Q35. Prove that Var(aX + b) = a² Var(X) for any real constants a, b.

> **Type:** Theory
> **Answer:** E[aX+b] = aE[X]+b, and E[(aX+b)²] = a²E[X²] + 2abE[X] + b², so Var = a²E[X²] + 2abE[X] + b² − (aE[X]+b)² = a²(E[X²] − E[X]²) = a² Var(X).
> **Solution:** Every term involving b cancels between the second moment and the squared mean, which is the algebraic reason shifts are irrelevant. The scaling is by a², not |a|, because squaring removes the sign — a reflection (a < 0) leaves the variance unchanged. This is the base rule behind normalisation: Z = (X − μ)/σ has variance 1.
> **Key point:** Var(aX + b) = a² Var(X); the shift b never affects variance and the scaling is a² regardless of sign.

### Q36. A random variable X has E[X] = 5 and E[X²] = 37. Find Var(X), σ, and the coefficient of variation.

> **Type:** Numerical
> **Answer:** Var(X) = 37 − 25 = 12, σ = √12 ≈ 3.464, coefficient of variation = 3.464/5 ≈ 0.6928.
> **Solution:** Var = E[X²] − (E[X])² = 37 − 5² = 12. The standard deviation is √12 = 2√3 ≈ 3.464. The coefficient of variation normalises the spread by the mean, so CV = σ/μ = 3.464/5 = 0.6928, i.e. 69.3%. CV is only meaningful for a positive mean and is a scale-free measure of relative dispersion.
> **Key point:** Var = E[X²] − μ²; CV = σ/μ, useful for comparing relative spread across different units.

### Q37. Given the random variable X takes values −1 and +2 with probabilities 0.4 and 0.6, find E[X], E[X²], Var(X) and the standard deviation.

> **Type:** Numerical
> **Answer:** E[X] = 0.8, E[X²] = 2.8, Var(X) = 2.8 − 0.64 = 2.16, σ = √2.16 ≈ 1.470.
> **Solution:** E[X] = (−1)(0.4) + (2)(0.6) = −0.4 + 1.2 = 0.8. E[X²] = (1)(0.4) + (4)(0.6) = 0.4 + 2.4 = 2.8. Var = 2.8 − 0.8² = 2.8 − 0.64 = 2.16, and σ = √2.16 ≈ 1.4697. Cross-check with the two-point identity Var = pq(x₂ − x₁)² with p = 0.6 on x₂ = 2 and q = 0.4 on x₁ = −1: 0.6 × 0.4 × 3² = 0.24 × 9 = 2.16, which matches.
> **Key point:** Var = E[X²] − (E[X])² = 2.8 − 0.64 = 2.16; the two-point shortcut Var = pq(x₂−x₁)² confirms it.

### Q38. The MGF of a discrete random variable is M(s) = 0.2 + 0.3e^{2s} + 0.5e^{3s}. Identify the distribution, its mean, and its variance.

> **Type:** Numerical
> **Answer:** X takes 0, 2, 3 with probabilities 0.2, 0.3, 0.5. Mean = 0(0.2) + 2(0.3) + 3(0.5) = 2.1. Var = 0 + 0.3(4) + 0.5(9) − 2.1² = 1.2 + 4.5 − 4.41 = 1.29.
> **Solution:** The MGF of a discrete variable is the sum of the masses weighted by e^{sx}, so reading off the coefficients at s = 0 gives the PMF: p(0) = 0.2, p(2) = 0.3, p(3) = 0.5, which sums to 1. The mean is the first moment, 2.1, and the second moment is 0.3(4) + 0.5(9) = 5.7, so Var = 5.7 − 4.41 = 1.29 and σ ≈ 1.136. The MGF always exists here because X is bounded, and it uniquely identifies the law.
> **Key point:** For a bounded discrete X the MGF is a finite sum ∑p(x)e^{sx}; coefficients at s = 0 are the PMF values.

### Q39. Compute the probability P(X > a) for a continuous random variable in terms of the CDF, and state the two inequalities you can never violate.

> **Type:** Conceptual
> **Answer:** P(X > a) = 1 − F(a) where F(a) = P(X ≤ a). The two invariants are 0 ≤ P(X ≤ a) ≤ 1 for all a, and F non-decreasing in a, which forces S(a) to be non-increasing.
> **Solution:** The events {X > a} and {X ≤ a} are complementary and exhaustive, so their probabilities sum to 1; for a continuous variable the strict/non-strict distinction is irrelevant since a single point has zero mass. The monotonicity of F follows because {X ≤ a} ⊆ {X ≤ b} whenever a ≤ b. These are exactly the axioms that let you reconstruct the whole distribution from a scatter of tail probabilities, and they are the sanity check on any tabulated CDF.
> **Key point:** S(a) = 1 − F(a); F must be non-decreasing and stay within [0, 1].

### Q40. A component's lifetime T is exponential with rate λ = 0.1 per hour. What is the probability it lasts between 2 and 5 hours, and what is the conditional probability it lasts more than 5 hours given it lasted at least 2 hours?

> **Type:** Numerical
> **Answer:** P(2 < T < 5) = e^{−0.2} − e^{−0.5} = 0.8187 − 0.6065 = 0.2122. P(T > 5 | T ≥ 2) = 0.6065/0.8187 ≈ 0.7408.
> **Solution:** The survival is S(t) = e^{−λt} with λ = 0.1, so S(2) = e^{−0.2} = 0.81873 and S(5) = e^{−0.5} = 0.60653. The interval probability is S(2) − S(5) = 0.21220. For the conditional part, P(T > 5 | T ≥ 2) = S(5)/S(2) = 0.60653/0.81873 = 0.74082, which is exactly e^{−0.1(5−2)} = e^{−0.3} — the memoryless property in action, since the elapsed 2 hours contribute nothing.
> **Key point:** P(T > t₂ | T > t₁) = e^{−λ(t₂−t₁)}; with t₁ = 2, t₂ = 5, λ = 0.1 this is e^{−0.3} ≈ 0.7408.

### Q41. Show that for any random variable, Var(X) ≥ 0 with equality only when X is constant almost surely, and state the exact inequality involved.

> **Type:** Theory
> **Answer:** Var(X) = E[(X − μ)²] ≥ 0 since the integrand is a square. Equality holds iff (X − μ)² = 0 a.s., i.e. X = μ almost surely. Equivalently E[X²] ≥ (E[X])², which is the Cauchy–Schwarz inequality with X and the constant 1.
> **Solution:** The variance is the expected value of a non-negative quantity, so it cannot be negative. This is a special case of Cauchy–Schwarz: E[X·1]² ≤ E[X²]·E[1²] = E[X²]. The "almost surely" qualifier matters — X may differ from μ on a set of measure zero without changing the distribution, so "constant except on a null set" is enough.
> **Key point:** Var(X) = E[(X−μ)²] ≥ 0, and Var = 0 ⟺ X is constant almost surely.

### Q42. X is uniform on [a, b]. Derive its mean, variance, PDF and CDF from the definition of a uniform distribution.

> **Type:** Numerical
> **Answer:** f(x) = 1/(b−a) on [a,b]; F(x) = 0 (x < a), (x−a)/(b−a) (a ≤ x ≤ b), 1 (x > b). Mean = (a+b)/2, Var = (b−a)²/12.
> **Solution:** Uniformity means equal probability per unit length, so normalisation fixes f = 1/(b−a). The CDF is just the fraction of the interval filled, giving the piecewise form. E[X] = ∫_a^b x/(b−a) dx = (b² − a²)/(2(b−a)) = (a+b)/2, symmetric about the midpoint. E[X²] = (b³ − a³)/(3(b−a)) = (a²+ab+b²)/3, and Var = (a²+ab+b²)/3 − (a+b)²/4 = (b−a)²/12. For [0,1] this is mean 1/2 and variance 1/12.
> **Key point:** Uniform(a,b): mean (a+b)/2, var (b−a)²/12; CDF is piecewise linear, so a uniform variable has infinite fourth moment.

### Q43. X is uniform on [0, 1]. Compute E[X²] and the fourth moment, and comment on whether the variance is finite.

> **Type:** Numerical
> **Answer:** E[X²] = 1/3 ≈ 0.3333, E[X⁴] = 1/5 = 0.2, Var(X) = 1/12 ≈ 0.0833. Every moment E[Xⁿ] = 1/(n+1) is finite, and because the support is bounded the MGF exists for **all** real s: M(s) = (e^s − 1)/s, with M(0) = 1.
> **Solution:** E[X^n] = ∫₀¹ x^n dx = 1/(n+1) for any n > −1, so E[X²] = 1/3 and E[X⁴] = 1/5. Var = 1/3 − (1/2)² = 1/3 − 1/4 = 1/12. The MGF is M(s) = ∫₀¹ e^{sx}dx = (e^s − 1)/s with the value at s = 0 given by continuity. The integrand is bounded by e^{|s|} on a finite interval for every finite s, so the integral converges for all s; the MGF is in fact entire. The contrast to note is with the Cauchy variable (Q80), whose MGF fails to exist for any s ≠ 0 despite being a perfectly valid distribution: moments existing is the condition for the MGF only in one direction, and the MGF is the stronger object.
> **Key point:** Uniform(0,1): E[X^n] = 1/(n+1), Var = 1/12; the MGF (e^s−1)/s exists for all real s, since bounded support guarantees it.

### Q44. Explain why the variance is a poor measure of spread for a heavy-tailed distribution, and show the effect on a concrete example.

> **Type:** Conceptual
> **Answer:** The variance uses squared deviations, so a single large outlier dominates it, whereas the mean absolute deviation is linear in the deviation. For the two-point law used in Q37-like settings this matters: if 99% of items deviate by 1 and 1% deviate by 100, the variance is dominated by the tail (0.99×1 + 0.01×10000 = 100.99) while the mean absolute deviation is only 0.99×1 + 0.01×100 = 1.99.
> **Solution:** Because x² grows much faster than |x|, any quantity built from squares over-weights rare extremes; this is the whole motivation behind the mean absolute deviation, the interquartile range, and robust estimators. Engineering examples are lightning surges on transmission lines, cosmic-ray-induced bit flips in memory, and impulsive interference on communication channels — all cases where the "RMS" answer is driven by a 1-in-10⁴ event.
> **Key point:** Squared deviations make variance outlier-dominated; for impulsive noise use mean-absolute-deviation or a percentile-based measure.

### Q45. Derive the general relation between the k-th raw moment, the mean and the k-th central moment.

> **Type:** Theory
> **Answer:** E[(X − μ)^k] = Σ_{j=0}^{k} C(k,j)(−μ)^{k−j}E[X^j] = Σ_{j=0}^{k} C(k,j)(−1)^{k−j}μ^{k−j}m_j, where m_j = E[X^j]. For k = 2: Var(X) = E[X²] − μ². For k = 3: μ₃ = E[X³] − 3μE[X²] + 2μ³.
> **Solution:** Expand (X − μ)^k by the binomial theorem and take expectations; linearity of expectation means each term is a constant times a raw moment. The case k = 2 gives the familiar Var = E[X²] − μ², and k = 3 gives the third central moment used to define skewness γ₁ = μ₃/σ³, which is 0 for every symmetric distribution and for the normal.
> **Key point:** Binomial expansion of (X−μ)^k converts raw to central moments; the normal is symmetric so all its odd central moments vanish.

### Q46. The skewness coefficient of a distribution is 0. What does that tell you, and what does it not tell you?

> **Type:** Conceptual
> **Answer:** γ₁ = E[(X−μ)³]/σ³ = 0, so the distribution is **symmetric about its mean**. It does not imply normality — uniform, triangular, symmetric beta, Laplace and many error-function-like distributions are all symmetric with zero skewness but far from Gaussian.
> **Solution:** Zero third central moment is the standard indicator of symmetry, since a symmetric distribution has paired deviations ±d with cancelling odd contributions. Normality needs much more: a Gaussian is the unique distribution with equal values of the higher cumulants too, and by the central limit theorem it is what you get from *many* small independent contributions rather than what symmetry alone guarantees. Exam traps regularly offer "zero skewness ⟹ normal", which is false.
> **Key point:** Zero skewness ⟹ symmetric about the mean, **not** ⟹ normal.

### Q47. Find E[X] and Var(X) for the triangular density f(x) = x for 0 ≤ x ≤ 1, f(x) = 2 − x for 1 < x ≤ 2, zero elsewhere. Verify your normalisation first.

> **Type:** Numerical
> **Answer:** Normalisation: ∫₀¹x dx + ∫₁²(2−x)dx = 0.5 + 0.5 = 1 ✓. E[X] = 1, E[X²] = 19/12 ≈ 1.5833, Var = 7/12 ≈ 0.5833, σ ≈ 0.7638.
> **Solution:** The two pieces each integrate to 1/2, so f is a legitimate density. E[X] = ∫₀¹x²dx + ∫₁²x(2−x)dx = 1/3 + [x² − x³/3]₁² = 1/3 + (4 − 8/3) − (1 − 1/3) = 1/3 + 4/3 − 2/3 = 1. E[X²] = ∫₀¹x³dx + ∫₁²x²(2−x)dx = 1/4 + [2x³/3 − x⁴/4]₁² = 1/4 + (16/3 − 4) − (2/3 − 1/4) = 1/4 + 4/3 − 7/12 = 3/12 + 16/12 − 7/12 = 19/12. Hence Var = 19/12 − 1² = 7/12 ≈ 0.5833 and σ = √(7/12) ≈ 0.7638.
> **Key point:** Triangular on [0,2]: mean 1, var 7/12 ≈ 0.5833; the shape is symmetric about x = 1, so zero skewness, yet it is not normal.

---

## Section 3. Standard discrete and continuous distributions (Q48–Q84)

### Q48. State the Bernoulli distribution with its PMF, mean, variance and MGF, and give the engineering interpretation.

> **Type:** Theory
> **Answer:** P(X = 1) = p, P(X = 0) = 1 − p, else 0. Mean = p, Var = p(1 − p), MGF M_X(s) = (1 − p) + pe^s, which exists for all s. A single trial: a switch closing, a bit being 1, a component surviving one stress step.
> **Solution:** E[X] = p and E[X²] = p, so Var = p − p² = p(1 − p), which peaks at p = 1/2 with value 0.25 — the maximum variance a single binary trial can produce, since the outcome carries at most one bit. The MGF is just the two-term weighted sum. The Bernoulli is the atom from which the binomial is built by adding independent trials.
> **Key point:** Bernoulli(p): mean p, var p(1−p), MGF = (1−p) + pe^s; its variance is capped at 0.25.

### Q49. Derive the binomial distribution as the distribution of the number of successes in n independent Bernoulli trials, and give its mean, variance and MGF.

> **Type:** Theory
> **Answer:** P(X = k) = C(n,k)p^k(1−p)^{n−k}, k = 0,…,n. Mean = np, Var = np(1−p), MGF = (1 − p + pe^s)^n.
> **Solution:** Count arrangements: there are C(n,k) ways to place the k successes and p^k(1−p)^{n−k} probability for any one arrangement, and the arrangements are disjoint so they add. Independence also means X = X₁ + … + Xₙ is a sum of independent Bernoulli variables, so E[X] = Σp = np and Var = Σp(1−p) = np(1−p) by additivity of mean and variance for independent terms. The MGF factorises into the n-th power of the Bernoulli MGF, and (1−p+pe^s)^n is a generating function whose n-th derivative at s = 0 recovers the first two moments.
> **Key point:** Binomial(n,p): mean np, var np(1−p), MGF = (1−p+pe^s)^n; it is the sum of n independent Bernoulli(p).

### Q50. A production line yields 10 items, each defective with probability 0.4 independently. Find P(exactly 3 defective) and P(at least 7 defective).

> **Type:** Numerical
> **Answer:** P(X = 3) ≈ 0.215. P(X ≥ 7) ≈ 0.0548.
> **Solution:** X ~ Binomial(10, 0.4). P(X=3) = C(10,3)(0.4)³(0.6)⁷ = 120 × 0.064 × 0.0279936 = 120 × 0.0017916 ≈ 0.21499. For the tail, compute term by term: P(7) = 120(0.4)⁷(0.6)³ = 120 × 0.0016384 × 0.216 ≈ 0.042467, P(8) = 45(0.4)⁸(0.6)² = 45 × 0.00065536 × 0.36 ≈ 0.0106168, P(9) = 10(0.4)⁹(0.6) ≈ 0.0015729, P(10) = 0.4¹⁰ ≈ 0.00010486. Sum ≈ 0.042467 + 0.010617 + 0.001573 + 0.000105 ≈ 0.054762. The mean is np = 4 and the variance 2.4, so a tail probability this small at 7 is expected.
> **Key point:** Binomial tail probabilities must be summed term by term; P(X ≥ 7) ≈ 0.0548 for n = 10, p = 0.4.

### Q51. Prove that a Binomial(n, p) variable converges to a Poisson variable with mean λ = np as n → ∞ with p = λ/n, and state the limiting PMF.

> **Type:** Theory
> **Answer:** With p = λ/n and n → ∞, Binomial(n, λ/n) → Poisson(λ), whose PMF is P(X = k) = e^{−λ}λ^k/k!.
> **Solution:** The binomial mass is C(n,k)(λ/n)^k(1 − λ/n)^{n−k} = [n(n−1)…(n−k+1)/k!]·(λ/n)^k·(1−λ/n)^{n−k}. The bracketed prefactor tends to λ^k/k! since (n−i)/n → 1 for fixed i, and (1 − λ/n)^{n−k} = [(1−λ/n)^n]·(1−λ/n)^{−k} → e^{−λ}·1. Multiplying gives e^{−λ}λ^k/k!. The practical rule is "rare independent events, each with small probability, many opportunities" — e.g. breakdown counts in an interval, phone calls per minute, or cosmic-ray-induced bit flips in a memory array.
> **Key point:** Binomial(n, λ/n) → Poisson(λ) = e^{−λ}λ^k/k!; the Poisson limit is "rare, small-probability, many-trial" counting.

### Q52. State the Poisson distribution, its mean, variance and MGF, and compute P(X = 0) and the most probable value.

> **Type:** Theory
> **Answer:** P(X = k) = e^{−λ}λ^k/k!, k = 0,1,2,…. Mean = λ, Var = λ, MGF = exp(λ(e^s − 1)). P(X = 0) = e^{−λ}; the mode is the integer nearest to λ (λ itself when λ is an integer).
> **Solution:** Differentiating the MGF, M′(s) = λe^s·M(s) so M′(0) = λ, and M″(0) = λ² + λ, giving Var = λ² + λ − λ² = λ — mean and variance are equal, the "index of dispersion is 1" property. The mass function e^{−λ}λ^k/k! is maximised where λ^{k+1}/(k+1)! ≤ λ^k/k!, i.e. k+1 ≤ λ, so the peak is at ⌊λ⌋ with a tie at λ when λ is integral.
> **Key point:** Poisson(λ): mean = var = λ, MGF = exp(λ(e^s−1)), P(0) = e^{−λ}; the variance equals the mean.

### Q53. A Poisson process has rate λ = 4 events per second. Find the probability of exactly 2 events in one second and the probability of 4 or more events in one second.

> **Type:** Numerical
> **Answer:** P(X = 2) = 8e^{−4} ≈ 0.1465. P(X ≥ 4) = 1 − e^{−4}(1 + 4 + 8 + 32/3) ≈ 0.5665.
> **Solution:** With λ = 4, P(X=2) = e^{−4}4²/2! = 8e^{−4} = 8 × 0.0183156 ≈ 0.146525. For the tail, accumulate the first four terms: P(0) = e^{−4} = 0.0183156, P(1) = 4e^{−4} = 0.0732624, P(2) = 8e^{−4} = 0.1465248, P(3) = (64/6)e^{−4} = 10.6667 × 0.0183156 = 0.195367. Their sum is 0.0183156 + 0.0732624 + 0.1465248 + 0.1953668 = 0.4334696, so P(X ≥ 4) = 1 − 0.4334696 ≈ 0.5665. Since the mean is 4, a probability above one half of getting 4 or more is sensible.
> **Key point:** Poisson tail = 1 − Σ of the lower terms; with λ = 4, P(X ≥ 4) ≈ 0.5665, not 0.4335.

### Q54. List the defining properties of a Poisson counting process N(t) with rate λ.

> **Type:** Theory
> **Answer:** (i) N(0) = 0. (ii) Independent increments: N(t₂) − N(t₁) depends only on t₂ − t₁, not on t₁. (iii) Poisson increments: N(t) − N(s) ~ Poisson(λ(t − s)) for t > s. Equivalently, interarrival times are iid exponential with rate λ, and the k-th arrival time T_k ~ Gamma(k, λ) with mean k/λ.
> **Solution:** These three axioms are exactly what makes the counting process memoryless: the number of arrivals in any interval depends only on the interval's length, and the count in it is Poisson. The interarrival equivalence follows because P(T₁ > t) = P(N(t) = 0) = e^{−λt}, which is the exponential survival. A consequence used in queueing and reliability is P(T_{n+1} − T_n ≤ τ) = 1 − e^{−λτ}, independent of n.
> **Key point:** Poisson process ⟺ iid exponential interarrivals of rate λ and the k-th arrival is Gamma(k, λ) with mean k/λ.

### Q55. Give the mean and variance of the k-th arrival time of a Poisson process of rate λ, and the probability that at least n events occur in time t.

> **Type:** Numerical
> **Answer:** T_k ~ Erlang/Gamma(k, λ): mean = k/λ, variance = k/λ². P(N(t) ≥ n) = 1 − Σ_{j=0}^{n−1} e^{−λt}(λt)^j/j!.
> **Solution:** The waiting time to the k-th event is the sum of k iid exponential(λ) variables, so the gamma moments apply: E[T_k] = k/λ and Var = k/λ². For λ = 2 per second and k = 4, the mean time to four events is 4/2 = 2 s with variance 4/4 = 1 s². The count tail is the complement of the Poisson CDF up to n−1, since P(N(t) ≥ n) = 1 − P(N(t) ≤ n−1).
> **Key point:** k-th arrival of a rate-λ Poisson process: mean k/λ, variance k/λ² — a gamma, not a normal, law.

### Q56. Two independent Poisson processes of rates λ₁ and λ₂ act on the same line. Give the distribution of the superposition and of the thinned processes, and say what determines the labels.

> **Type:** Theory
> **Answer:** Superposition: N(t) = N₁(t) + N₂(t) is Poisson with rate λ₁ + λ₂. Random thinning: if each N₁ event is independently kept with probability p, the kept process is Poisson with rate pλ₁ and the discarded one with rate (1 − p)λ₁.
> **Solution:** For the superposition, P(N₁(t₁)+N₂(t₁) = n) is the binomial-weighted sum Σ C(n,j)e^{−λ₁t}(λ₁t)^j/j! · e^{−λ₂t}(λ₂t)^{n−j}/(n−j)!, and the binomial theorem collapses it to e^{−(λ₁+λ₂)t}((λ₁+λ₂)t)^n/n!. For thinning, the count of kept events is a Binomial(N₁(t), p) mixture, and Σ_k C(m,k)p^k(1−p)^{m−k}(λ₁t)^m e^{−λ₁t}/m! = e^{−pλ₁t}(pλ₁t)^k/k!. The marking of which stream an arrival belongs to is a binomial split of the total count with success probability λ₁/(λ₁+λ₂).
> **Key point:** Independent Poissons add in rate; thinning scales the rate by the keep-probability; the label split is Binomial(n, λ₁/(λ₁+λ₂)).

### Q57. State the geometric distribution on the support {1, 2, 3, …} with its mean, variance and MGF, and justify the memoryless property.

> **Type:** Theory
> **Answer:** P(X = k) = (1−p)^{k−1}p, k = 1,2,…. Mean = 1/p, Var = (1−p)/p², MGF = pe^s/(1 − (1−p)e^s). It is memoryless: P(X > m + n | X > m) = P(X > n).
> **Solution:** The memorylessness follows directly from the survival function S(k) = (1−p)^k, since S(m+n)/S(m) = (1−p)^{m+n}/(1−p)^m = (1−p)^n = S(n), with no reference to m. The moments come from differentiating M(s) = pe^s/(1−qe^s) with q = 1−p: M′(0) = p/q · [p/q + 1] = 1/p, and M″(0) − M′(0)² = q/p². Note the alternative convention on support {0,1,2,…}, P(X = k) = (1−p)^k p, which has the same mean and variance; always state the support.
> **Key point:** Geometric(p) on {1,2,…}: mean 1/p, var (1−p)/p²; memoryless because S(m+n)/S(m) = S(n).

### Q58. State the negative binomial distribution (as the number of trials needed to obtain r successes) and give its mean, variance and MGF.

> **Type:** Theory
> **Answer:** P(X = k) = C(k−1, r−1)p^r(1−p)^{k−r}, k = r, r+1, …. Mean = r/p, Var = r(1−p)/p², MGF = [pe^s/(1 − (1−p)e^s)]^r.
> **Solution:** The last trial must be a success, and the preceding k−1 trials must contain exactly r−1 successes in any order, giving C(k−1, r−1)p^r(1−p)^{k−r}. Since X is the sum of r iid geometric(p) variables, the mean is r/p, the variance r(1−p)/p², and the MGF is the r-th power of the geometric MGF. Equivalently, the number of failures before the r-th success is a negative binomial on {0,1,…} with the same mean r(1−p)/p and variance r(1−p)/p².
> **Key point:** NegBin(r,p) on {r,r+1,…}: mean r/p, var r(1−p)/p² — the sum of r iid geometric(p).

### Q59. A wafer contains independent defects with probability p = 0.4 per site. How many sites must be scanned, on average, to find the third defect, and what is the variance of that number?

> **Type:** Numerical
> **Answer:** Mean = 3/0.4 = 7.5 sites; variance = 3(0.6)/(0.4)² = 1.8/0.16 = 11.25, so σ ≈ 3.354.
> **Solution:** The number of sites examined is the trial count needed for three successes, i.e. a negative binomial with r = 3, p = 0.4. Its mean is r/p = 7.5 and its variance r(1−p)/p² = 3 × 0.6 / 0.16 = 11.25, giving σ = √11.25 ≈ 3.354. The standard deviation exceeding the mean is normal for a count of "waiting time" type; note the coefficient of variation √((1−p)/p) = √1.5 ≈ 1.22 is independent of r.
> **Key point:** NegBin(3, 0.4): mean 7.5, var 11.25; the CV = √((1−p)/p) ≈ 1.22 does not depend on r.

### Q60. A technician picks two different random times in a one-hour window: T₁ uniform on [0,1] and T₂ exponential with rate 1. Which is more likely to be small, and what distinguishes their tails?

> **Type:** Comparison
> **Answer:** P(T₁ < t) = t on [0,1] while P(T₂ < t) = 1 − e^{−t}. The two are **stochastically incomparable**: the exponential's CDF is below the uniform's on (0, 1) but exceeds it beyond 1. T₁ is the more likely to be *large* (mean 0.5 vs 1 is not the point) — rather, the distinguishing feature is the **unbounded, heavier tail**: P(T₂ > t) = e^{−t} for all t ≥ 0, whereas P(T₁ > t) = 0 for t ≥ 1. Variances are 1/12 ≈ 0.0833 and 1.
> **Solution:** At small t the two CDFs agree to first order, since both densities equal 1 at the origin, but for 0 < t < 1 we have 1 − e^{−t} < t, so the exponential puts relatively more mass in the upper part of the unit interval; for t > 1 the uniform is exhausted while e^{−t} > 0. Because no single ordering of the two CDFs holds on all of ℝ⁺, neither variable dominates the other — the classic demonstration that crossing CDFs mean incomparability. What does distinguish them unconditionally is the support: the uniform is bounded with variance 1/12, the exponential is unbounded with variance 1, so for any threshold t large the exponential is far more likely to exceed it. The trap is to read "larger mean" as "larger in the stochastic order".
> **Key point:** Uniform[0,1] and Exp(1) have crossing CDFs, so neither stochastically dominates; the exponential's unbounded support gives P(X > 1) = e^{−1} ≈ 0.3679 against 0 for the uniform.

### Q61. Prove the memoryless property of the exponential distribution from its PDF.

> **Type:** Theory
> **Answer:** P(X > s + t | X > s) = e^{−λ(s+t)}/e^{−λs} = e^{−λt} = P(X > t) for all s, t ≥ 0.
> **Solution:** The survival is S(x) = ∫_x^∞ λe^{−λu}du = e^{−λx}. Conditioning on X > s restricts to the renormalised tail, and the ratio S(s+t)/S(s) cancels the dependence on s entirely. This means an exponential component that has already survived 100 hours has the same expected additional life as a brand-new one, so maintenance does not reset its age — the property that makes exponential lifetimes the default model for electronic component failure.
> **Key point:** S(s+t)/S(s) = e^{−λt}, independent of s — memorylessness, the reason exponential is the default electronic-failure lifetime.

### Q62. State the Erlang (Gamma) distribution with shape k and rate λ, giving its PDF, mean, variance and MGF, and interpret k physically.

> **Type:** Theory
> **Answer:** f(x) = λ^k x^{k−1}e^{−λx}/(k−1)! for x > 0, k a positive integer. Mean = k/λ, Var = k/λ², MGF = (λ/(λ−s))^k. The Erlang form is the time to the k-th event of a Poisson process of rate λ; k is the "number of stages".
> **Solution:** Since the interarrival times are iid exponential(λ), their k-fold sum is a convolution of k exponential densities, which evaluates to the given f. The moments follow either from the MGF or from additivity: mean k/λ, variance k/λ². The CDF is the incomplete gamma function, and for integer k it is the finite sum P(X ≤ x) = 1 − e^{−λx}Σ_{j=0}^{k−1}(λx)^j/j!, which is the practical way to evaluate Erlang probabilities.
> **Key point:** Erlang(k, λ): mean k/λ, var k/λ², MGF = (λ/(λ−s))^k; equivalently the k-th arrival time of a rate-λ Poisson process.

### Q63. The time to complete a three-stage process, each stage an independent exponential(2 per second) operation, is T. Find E[T], Var(T) and P(T < 2).

> **Type:** Numerical
> **Answer:** E[T] = 3/2 = 1.5 s, Var(T) = 3/4 = 0.75 s² (σ ≈ 0.866 s), P(T < 2) ≈ 0.7619.
> **Solution:** The three stages sum to an Erlang(3, 2) variable, so E[T] = 3/2 = 1.5 s and Var = 3/2² = 3/4 = 0.75 s². For the CDF use the integer-shape formula with λx = 2 × 2 = 4: P(T < 2) = 1 − e^{−4}(1 + 4 + 4²/2!) = 1 − e^{−4}(1 + 4 + 8) = 1 − 13e^{−4} = 1 − 13 × 0.0183156 = 1 − 0.238103 ≈ 0.761897. So there is about a 76% chance the three stages finish within 2 s even though the mean is 1.5 s — a reminder that the distribution is right-skewed.
> **Key point:** Erlang(3,2): P(T<2) = 1 − 13e^{−4} ≈ 0.7619; mean 1.5 s but the distribution is right-skewed so the median is lower.

### Q64. State the chi-square distribution in terms of the Gamma distribution, give its mean and variance in terms of degrees of freedom, and evaluate a tail probability you will actually meet in the exam.

> **Type:** Numerical
> **Answer:** χ²(k) = Gamma(k/2, rate 1/2). Mean = k, Var = 2k. For k = 10, P(χ² > 18.307) = 0.05 (equivalently P(χ² < 3.940) = 0.05).
> **Solution:** The chi-square with k degrees of freedom is the sum of the squares of k independent standard normals, and it coincides with the gamma of shape k/2 and rate 1/2, giving mean (k/2)/(1/2) = k and variance (k/2)/(1/2)² = 2k. With k = 10 these are 10 and 20. The table entry 18.307 is the 95th percentile of χ²(10), so the upper-tail probability is 0.05; the corresponding 5th percentile is 3.940, giving a two-sided rejection region outside [3.940, 18.307] at the 5% level.
> **Key point:** χ²(k) = Gamma(k/2, 1/2): mean k, var 2k; for k = 10, P(χ² > 18.307) = 0.05.

### Q65. State the normal distribution, its mean and variance, and prove the standardisation step.

> **Type:** Theory
> **Answer:** f(x) = e^{−(x−μ)²/(2σ²)}/(σ√(2π)) with mean μ and variance σ². If X ~ N(μ, σ²) then Z = (X − μ)/σ ~ N(0,1), and Φ(z) = (1/√(2π))∫_{−∞}^{z}e^{−u²/2}du.
> **Solution:** Substituting u = (x−μ)/σ turns the integral for the CDF of X into Φ((x−μ)/σ), because dx = σdu cancels the 1/σ in the density. E[Z] = (E[X] − μ)/σ = 0 and Var(Z) = Var(X)/σ² = 1 by the affine-variance rule. Symmetry gives Φ(−z) = 1 − Φ(z), and Φ(0) = 0.5, which is what makes all normal table lookups work.
> **Key point:** Z = (X−μ)/σ ~ N(0,1); Φ(−z) = 1 − Φ(z) and Φ(0) = 0.5, the two symmetry facts behind every table lookup.

### Q66. A random test score X is normal with mean 100 and standard deviation 15. Find P(85 < X < 115) and P(X > 130).

> **Type:** Numerical
> **Answer:** P(85 < X < 115) = Φ(1) − Φ(−1) = 0.6827. P(X > 130) = 1 − Φ(2) = 1 − 0.9772 = 0.0228.
> **Solution:** Standardise: Z = (X − 100)/15. Then 85 ↔ z = −1 and 115 ↔ z = +1, so P(−1 < Z < 1) = Φ(1) − Φ(−1) = 0.8413 − 0.1587 = 0.6826 ≈ 0.6827. For the second, 130 ↔ z = (130 − 100)/15 = 2, so P(X > 130) = 1 − Φ(2) = 1 − 0.9772 = 0.0228. Both results are the classic "68–95–99.7" values: within one sigma is 68.27%, beyond two sigma is 2.28%.
> **Key point:** 68–95–99.7 rule: P(|Z| < 1) = 0.6827 and P(Z > 2) = 0.0228; always standardise before using the table.

### Q67. A random variable is normal with unknown mean μ and standard deviation σ. Find the interval ±a that contains the random variable with probability 0.95, and the probability that a normal variable falls outside ±2σ.

> **Type:** Numerical
> **Answer:** a = 1.96σ. P(|X − μ| > 2σ) = 2(1 − Φ(2)) = 2(1 − 0.9772) = 0.0456.
> **Solution:** P(|X−μ| ≤ a) = 2Φ(a/σ) − 1 = 0.95 gives Φ(a/σ) = 0.975, and Φ⁻¹(0.975) = 1.95996 ≈ 1.96. For the second, P(|Z| > 2) = 1 − P(−2 < Z < 2) = 1 − (0.9772 − 0.0228) = 1 − 0.9544 = 0.0456. So roughly 4.56% of a population lies outside two sigma — the "2σ quality level" that corresponds to about 45 defective parts per thousand, which is why 6-sigma programmes target ±6σ (P ≈ 2 × 10⁻⁹).
> **Key point:** Central 95% is ±1.96σ; P(|Z| > 2σ) = 0.0456, the classic "two-sigma quality level".

### Q68. If X ~ N(μ₁, σ₁²) and Y ~ N(μ₂, σ₂²) are independent, give the distribution of aX + bY + c without deriving it from the density.

> **Type:** Theory
> **Answer:** aX + bY + c ~ N(aμ₁ + bμ₂ + c, a²σ₁² + b²σ₂²).
> **Solution:** By the scaling/shifting rule, aX + bY + c has mean aμ₁ + bμ₂ + c and variance a²σ₁² + b²σ₂². Since X and Y are independent, the joint MGF factorises, M_{aX+bY+c}(s) = e^{cs}M_X(as)M_Y(bs) = e^{cs}·e^{aμ₁s + a²σ₁²s²/2}·e^{bμ₂s + b²σ₂²s²/2}, which is exactly the MGF of a normal with the stated mean and variance. This is the reason normality survives linear processing, and it is the only step needed for filter and amplifier noise analysis.
> **Key point:** A weighted sum of independent normals is normal with **summed variances** a²σ₁² + b²σ₂², not the square root of the sum.

### Q69. State the central limit theorem precisely, including its hypotheses and the standardisation it performs.

> **Type:** Theory
> **Answer:** Let X₁, X₂, … be iid with mean μ and finite variance σ² > 0. Then for the sum S_n = ΣXᵢ, (S_n − nμ)/(σ√n) → N(0,1) in distribution as n → ∞; equivalently S_n ≈ N(nμ, nσ²). Equivalently the sample mean X̄_n ≈ N(μ, σ²/n).
> **Solution:** The theorem needs only iid and a **finite** variance — no normality, and no restriction on the shape of the individual distribution. Note the √n shrinkage of the standard deviation: averaging n samples reduces the spread by √n, which is why averaging 16 samples halves the noise. The convergence is in distribution, not in value: the approximation gets better as n grows but is not an identity for finite n.
> **Key point:** CLT: S_n ≈ N(nμ, nσ²) needs only iid + finite variance; the spread falls as σ√n, i.e. σ/√n for the mean.

### Q70. Four independent exponential(1) lifetimes are connected in series. Using the central limit theorem, approximate P(S > 7) where S is the total lifetime, and comment on the accuracy.

> **Type:** Numerical
> **Answer:** S ≈ N(4, 4), so P(S > 7) ≈ P(Z > 1.5) = 1 − 0.9332 = 0.0668. The exact Erlang value is ≈ 0.0818, so the CLT underestimates by about 0.015.
> **Solution:** Each exponential(1) has mean 1 and variance 1, so S has mean 4 and variance 4, giving σ_S = 2. Standardising: z = (7 − 4)/2 = 1.5, and P(Z > 1.5) = 1 − Φ(1.5) = 1 − 0.9332 = 0.0668. The exact answer uses the Erlang(4,1) tail, e^{−7}(1 + 7 + 7²/2 + 7³/6) = 0.000911882 × 89.6667 ≈ 0.0818. With only four summands the sample is far too small for the normal approximation, and the right-skewed true tail is underestimated — the standard caution that the CLT needs n in the tens before it is trustworthy.
> **Key point:** CLT with n = 4 underestimates the right tail: 0.0668 vs the exact Erlang 0.0818; the CLT needs n in the tens before it is reliable.

### Q71. Derive the Rayleigh distribution as the envelope of two orthogonal zero-mean Gaussian components and obtain its mean, variance and MGF.

> **Type:** Theory
> **Answer:** X = √(V₁² + V₂²) with V₁, V₂ iid N(0, σ²) gives f(x) = (x/σ²)e^{−x²/(2σ²)} for x ≥ 0, where σ is the standard deviation of each component. Mean = σ√(π/2) ≈ 1.2533σ, Var = (2 − π/2)σ² ≈ 0.4292σ², and M_X(s) = 1 + σs√(π/2)e^{σ²s²/2}[1 + erf(σs/√2)], which is finite for every real s.
> **Solution:** Working in polar coordinates, f_{V₁,V₂}(v₁,v₂) = e^{−(v₁²+v₂²)/(2σ²)}/(2πσ²) and the annulus element is x dx dθ, so f_X(x) = ∫₀^{2π} x dx e^{−x²/(2σ²)}/(2πσ²) = (x/σ²)e^{−x²/(2σ²)}. The moments use ∫₀^∞x³e^{−x²/(2σ²)}dx = 2σ⁴ and ∫₀^∞x⁵e^{−x²/(2σ²)}dx = 8σ⁶, giving E[X] = σ√(π/2), E[X²] = 2σ² and Var = 2σ² − πσ²/2. For the MGF, ∫₀^∞xe^{−ax²}e^{sx}dx = (1/2a) + (s/(2a))·(√π/√a)e^{s²/(4a)}, which with a = 1/(2σ²) gives 1 + σs√(π/2)e^{σ²s²/2}, and the region below the origin contributes erf(σs/√2)·that term, producing the form quoted. It is finite for all real s because the Gaussian in the density dominates the linear exponential, so the Rayleigh distribution is sub-exponential; numerical evaluation at sσ = 1 gives 4.477, matching the closed form.
> **Key point:** Rayleigh(scale σ): mean σ√(π/2) ≈ 1.2533σ, var (2 − π/2)σ² ≈ 0.4292σ², MGF 1 + σs√(π/2)e^{σ²s²/2}[1 + erf(σs/√2)], finite for all real s since the tail is Gaussian, not exponential.

### Q72. A Rayleigh-distributed envelope has component standard deviation σ = 2 V. Find P(X < 3), E[X] and Var(X).

> **Type:** Numerical
> **Answer:** P(X < 3) = 1 − e^{−9/8} ≈ 0.6753. E[X] = 2√(π/2) ≈ 2.507 V. Var = (2 − π/2)(4) ≈ 1.717 V².
> **Solution:** The CDF is F(x) = 1 − e^{−x²/(2σ²)}, so P(X < 3) = 1 − e^{−9/8} = 1 − e^{−1.125} = 1 − 0.324652 ≈ 0.67535. E[X] = σ√(π/2) = 2 × 1.253314 = 2.50663 V. Var = (2 − π/2)σ² = (2 − 1.570796) × 4 = 0.429204 × 4 = 1.716816 ≈ 1.717 V², giving σ_X = √1.716816 ≈ 1.3103 V. The mean exceeds σ because the Rayleigh mean scales with σ itself, not with √2 σ.
> **Key point:** Rayleigh CDF = 1 − e^{−x²/(2σ²)}; with σ = 2, P(X<3) ≈ 0.6753 and Var ≈ 1.717 V².

### Q73. Why does the Rayleigh distribution dominate receiver front-end noise, and by what factor does its mean exceed the component RMS?

> **Type:** Conceptual
> **Answer:** Complex noise is I + jQ with I and Q independent Gaussians of standard deviation σ, so its envelope is Rayleigh. Its mean is σ√(π/2) ≈ 1.2533σ, which is only 25% above the component RMS σ, and its standard deviation is ≈ 0.6551σ — so the envelope is a tightly concentrated random quantity, and the Rayleigh is well approximated by a constant at σ.
> **Solution:** Two degrees of freedom produce the two-dimensional Gaussian; the magnitude of a 2-D isotropic Gaussian is Rayleigh by construction, which is why it appears in every communication and radar front end. The ratio Var/E[X²] = 0.4292/2 = 0.2146 means the envelope is concentrated: its variance is only about 21% of its second moment, and the coefficient of variation is 0.6551/1.2533 = 0.5226. Envelope detectors exploit this by squaring and averaging rather than tracking the instantaneous envelope.
> **Key point:** Rayleigh is the envelope of complex Gaussian noise; CV = 0.523, so the envelope concentrates and is often well approximated by σ.

### Q74. State the Rice distribution arising from a quadrature receiver with a deterministic signal, giving its PDF, second moment, and the closed-form mean.

> **Type:** Theory
> **Answer:** With V₁ ~ N(ν cos θ, σ²), V₂ ~ N(ν sin θ, σ²) independent and X = √(V₁² + V₂²): f(x) = (x/σ²)e^{−(x²+ν²)/(2σ²)}I₀(xν/σ²) for x ≥ 0, where I₀ is the modified Bessel function of the first kind (order zero) and ν is the deterministic signal amplitude. E[X²] = 2σ² + ν², and E[X] = σ√(π/2)·e^{−a}[(1+2a)I₀(a) + 2aI₁(a)] with a = ν²/(4σ²); Var = 2σ² + ν² − E[X]².
> **Solution:** The two Gaussian components have offset means whose squares sum to ν²(cos²θ + sin²θ) = ν², so the total second moment is (σ² + ν²cos²θ) + (σ² + ν²sin²θ) = 2σ² + ν². Completing the square on the joint density and integrating the resulting e^{(ν/σ²)xv₁} factor produces the I₀ Bessel kernel, since I₀(z) = (1/2π)∫₀^{2π} e^{z cos φ}dφ. The Rice density has no simple MGF, so moments are evaluated from this closed form rather than from a generating function.
> **Key point:** Rice(ν, σ): E[X²] = 2σ² + ν², so Var = 2σ² + ν² − E[X]²; the PDF carries a Bessel I₀ kernel.

### Q75. For a Rice envelope with σ = 1 and ν = 2, compute E[X] and Var(X).

> **Type:** Numerical
> **Answer:** E[X] ≈ 2.272, Var(X) ≈ 0.838 (so σ_X ≈ 0.915).
> **Solution:** Set a = ν²/(4σ²) = 4/4 = 1. Using I₀(1) = 1.266066 and I₁(1) = 0.565159, the bracket is (1+2)(1.266066) + (2)(0.565159) = 3.798198 + 1.130318 = 4.928516, and multiplying by e^{−1} = 0.367879 gives 1.812923. Hence E[X] = 1.253314 × 1.812923 ≈ 2.27207. The second moment is E[X²] = 2σ² + ν² = 2 + 4 = 6, so Var = 6 − (2.27207)² = 6 − 5.16230 ≈ 0.83770 ≈ 0.838, and σ_X = √0.838 ≈ 0.9154.
> **Key point:** Rice(ν=2, σ=1): E[X] ≈ 2.272 and Var ≈ 0.838 from E[X²] = 6; the Bessel closed form is required since no MGF exists.

### Q76. Taking the limit ν → 0 in the Rice distribution recovers which distribution, and what happens to the mean and variance? What is the limit as ν → ∞?

> **Type:** Boundary case
> **Answer:** ν → 0 gives the **Rayleigh** distribution: E[X] → σ√(π/2) and Var → (2 − π/2)σ². As ν → ∞, E[X] ≈ ν + σ²/(2ν) and Var → σ², so the envelope becomes nearly deterministic at the signal amplitude.
> **Solution:** With ν = 0 the two component means vanish, the Bessel term I₀(0) = 1 collapses the Rice PDF to (x/σ²)e^{−x²/(2σ²)} and I₁(0) = 0 removes the second bracket term, giving exactly the Rayleigh mean. For large ν, E[X²] = ν² + 2σ² and the mean is √(E[X²])(1 − σ²/(2ν²) + …) ≈ ν + σ²/(2ν), so Var = 2σ² + ν² − E[X]² → σ². The two limits correspond to "noise only" and "signal far above noise", the two ends of the Rician SNR sweep.
> **Key point:** Rice collapses to Rayleigh at ν = 0 and to a near-deterministic amplitude with Var → σ² as ν → ∞.

### Q77. State the general Gamma distribution with shape α and rate λ, and evaluate E[X] and E[X²] for α = 2.5, λ = 2.

> **Type:** Numerical
> **Answer:** f(x) = λ^α x^{α−1}e^{−λx}/Γ(α), x > 0; mean = α/λ, Var = α/λ², MGF = (λ/(λ−s))^α. For α = 2.5, λ = 2: E[X] = 1.25, E[X²] = 2.1875, Var = 0.625.
> **Solution:** The moment formula is E[Xⁿ] = Γ(α+n)/(Γ(α)·λⁿ), which follows by substituting t = λx. For α = 2.5 and λ = 2, E[X] = 2.5/2 = 1.25. For the second moment, Γ(4.5)/Γ(2.5) = 3.5 × 2.5 = 8.75, since the Gamma recursion Γ(z+1) = zΓ(z) applied twice more gives Γ(4.5) = 3.5 × 2.5 × Γ(2.5). Hence E[X²] = 8.75/2² = 8.75/4 = 2.1875. Then Var = 2.1875 − 1.5625 = 0.625, which matches α/λ² = 2.5/4 = 0.625. Equivalently E[X²] = Var + mean² = α(α+1)/λ² = 2.5 × 3.5/4 = 2.1875, which is the quickest route. The non-integer shape is the "generalised Erlang" that models the sum of many small, non-identical stage times.
> **Key point:** Gamma(α, λ): E[X^n] = Γ(α+n)/(Γ(α)λⁿ), mean α/λ, var α/λ²; integer α is Erlang.

### Q78. State the Weibull distribution using the shape–scale parameterisation and give its mean, variance and hazard.

> **Type:** Theory
> **Answer:** f(x) = (k/λ)(x/λ)^{k−1}e^{−(x/λ)^k} for x ≥ 0, with k the shape (dimensionless) and λ the scale (metres). Mean = λΓ(1 + 1/k), Var = λ²[Γ(1 + 2/k) − Γ²(1 + 1/k)], survival S(x) = e^{−(x/λ)^k}, hazard h(x) = (k/λ)(x/λ)^{k−1}. There is no elementary MGF in general.
> **Solution:** Substituting t = (x/λ)^k in the moment integral gives E[Xⁿ] = λⁿΓ(1 + n/k), so n = 1 and n = 2 give the mean and second moment, and Var follows by subtraction. The hazard is increasing for k > 1, constant for k = 1, and decreasing for k < 1, which is the "wear-out versus random-failure" discrimination: k < 1 gives a high early failure rate (infant mortality), k > 1 gives a wear-out law. In reliability testing this is the standard model used to extrapolate a life test.
> **Key point:** Weibull(shape k, scale λ): mean λΓ(1+1/k), var λ²[Γ(1+2/k) − Γ²(1+1/k)], hazard (k/λ)(x/λ)^{k−1}.

### Q79. A Weibull lifetime has shape k = 2 and scale λ = 3. Find its mean, variance, and the probability that it exceeds 6.

> **Type:** Numerical
> **Answer:** E[X] = 3Γ(1.5) = 3 × 0.886227 ≈ 2.659. Var = 9[Γ(2) − Γ²(1.5)] = 9[1 − 0.785398] ≈ 1.931 (σ ≈ 1.390). P(X > 6) = e^{−(6/3)²} = e^{−4} ≈ 0.01832.
> **Solution:** Γ(1.5) = Γ(3/2) = ½√π = 0.8862269, so E[X] = 3 × 0.8862269 = 2.6586807. Γ(2) = 1 and Γ(1.5)² = 0.7853982, so Var = 9(1 − 0.7853982) = 9 × 0.2146018 = 1.9314162, giving σ = 1.3897546. The survival is e^{−(x/3)²}, so P(X > 6) = e^{−4} = 0.0183156. As a cross-check this same law is Rayleigh with component σ_R = λ/√2 = 2.12132, whose mean is 2.12132 × 1.253314 = 2.6587 ✓.
> **Key point:** Weibull(k=2, λ=3) = Rayleigh with σ = λ/√2; mean ≈ 2.659, var ≈ 1.931, P(X>6) = e^{−4}.

### Q80. Two Weibull distributions have the same median. Does that force the same mean, and what distinguishes k = 1, k = 2 and k → ∞?

> **Type:** Comparison
> **Answer:** No — the same median does not force the same mean, because the shape parameter controls the tail. k = 1 is the exponential (mean = λ, var = λ², mean/median = 1/ln 2 ≈ 1.4427); k = 2 is Rayleigh with scale λ/√2, so mean = 0.8862λ and median = 0.8326λ, giving mean/median ≈ 1.0644; as k → ∞ the distribution collapses onto λ (a degenerate distribution at the scale), with zero variance and mean/median → 1.
> **Solution:** The median solves S(m) = 1/2, i.e. (m/λ)^k = ln 2, so m = λ(ln 2)^{1/k} — for a fixed m you can pick any k and solve for λ, so equal medians impose no constraint on the mean. The mean-to-median ratio is R(k) = Γ(1+1/k)/(ln 2)^{1/k}: at k = 1, R = 1/0.693147 = 1.4427; at k = 2, R = Γ(1.5)/√(ln 2) = 0.886227/0.832555 = 1.0644; and R(k) → 1 as k → ∞, since Γ(1+1/k) → 1 and (ln 2)^{1/k} → 1. R(k) is monotonically decreasing, so a small mean-to-median ratio signals a tight, wear-out-like life distribution, which is exactly what accelerated life testing looks for, while k = 1 is the random-failure (constant-hazard) regime.
> **Key point:** Weibull median = λ(ln 2)^{1/k}; mean/median ratio falls from 1.443 (exponential) to 1 as k → ∞ (degenerate at λ).

### Q81. State the Cauchy distribution and explain why its mean, variance and MGF do not exist.

> **Type:** Theory
> **Answer:** f(x) = γ/[π((x − x₀)² + γ²)]. The mean does not exist because ∫x f(x)dx diverges logarithmically; the variance is undefined/infinite; the MGF does not exist for any s ≠ 0 because e^{sx} outgrows the 1/x² tail. The standard Cauchy is the ratio X = Z₁/Z₂ of two iid standard normals.
> **Solution:** As |x| → ∞ the density behaves like γ/(πx²), which is integrable, but x·f(x) ~ γ/(πx) is not, so the first moment diverges in the improper sense. Since a mean does not exist, neither does the variance. The generating function representation shows E[e^{sX}] = e^{sx₀}e^{−γ|s|} would require a density ∝ e^{sx} − γ|x|, and no single value of the normalisation constant can work for both tails, so the MGF is undefined. The Cauchy is the canonical example of a distribution with no mean and no variance.
> **Key point:** Cauchy: no mean, no variance, no MGF — the density tail ~ 1/x² is not integrable when multiplied by x.

### Q82. For a standard Cauchy random variable, compute P(|X| < 1) and P(0 < X < 1). What does this say about the "average" of a Cauchy sample?

> **Type:** Numerical
> **Answer:** P(|X| < 1) = 0.5, and P(0 < X < 1) = 0.25. The sample mean has no tendency to converge to any value — it is itself Cauchy distributed, so the law of large numbers fails without a finite mean.
> **Solution:** P(|X| < 1) = (1/π)∫_{−1}^{1}dx/(1+x²) = (1/π)[arctan x]_{−1}^{1} = (1/π)(π/4 + π/4) = 0.5. By symmetry, P(0 < X < 1) = 0.25. The sample mean of n iid Cauchy variables is again Cauchy with the same scale γ, since the Cauchy is closed under the ratio of normals. Hence the strong law of large numbers, which requires a finite mean, does not apply: the sample mean wanders and any single outlier can drag it far.
> **Key point:** Standard Cauchy: P(|X|<1) = 0.5; the sample mean is again Cauchy, so the law of large numbers fails.

### Q83. A counting process has a rate that varies with time: λ(t) = 2t, t ≥ 0. Give the distribution of N(t) and the mean number of events in [1, 3].

> **Type:** Numerical
> **Answer:** N(t) is Poisson with mean Λ(t) = ∫₀^t λ(u)du = t², so P(N(t) = n) = e^{−t²}(t²)ⁿ/n!. E[N(3) − N(1)] = 3² − 1² = 8, with variance also 8.
> **Solution:** A non-homogeneous Poisson process has increments that are Poisson with the integrated intensity, not with λ(t) itself. The mean number of events on [1, 3] is ∫₁³ 2u du = [u²]₁³ = 9 − 1 = 8, and for a Poisson count the variance equals the mean. The trap is to use λ(3) = 6, which is the instantaneous rate at one instant rather than the accumulated count; the model is used for flashover in insulation, where the hazard accelerates with accumulated damage.
> **Key point:** Non-homogeneous Poisson: N(t) ~ Poisson(∫₀^tλ), so E[events on [1,3]] = ∫₁³2t dt = 8, not λ(3) = 6.

### Q84. A random variable has PMF P(X = k) = e^{−λ}λ^k/k! for k = 0, 1, 2, …. What are its mean and variance?

> **Type:** MCQ (GATE-2)
> **Answer:** Mean = λ and variance = λ. (Option a)
>
> (a) λ, λ
> (b) λ, λ²
> (c) λ/2, λ
> (d) 2λ, λ
> **Solution:** This is the Poisson PMF, and a Poisson variable is a sum of unit exponential random variables in a limit, with MGF M(s) = exp(λ(e^s − 1)). Differentiating, M′(0) = λ and M″(0) = λ² + λ, so Var = λ² + λ − λ² = λ. The equality of mean and variance is the signature of the Poisson and distinguishes it from every binomial (whose variance np(1−p) is always less than its mean np, since p(1−p) < 1 for any non-degenerate p). The Poisson's own mode reinforces the pattern: the most probable values are ⌊λ⌋ and, when λ is an integer, λ − 1 as well, so the mode also sits at the mean up to a one-unit ambiguity.
> **Key point:** Poisson: E = Var = λ; unlike the binomial, whose variance np(1−p) is strictly less than its mean.

## Section 4. Multivariate random variables: joint, marginal, conditional, independence, covariance (Q85–Q107)

### Q85. Define the joint CDF, joint PDF and joint PMF of two random variables, and state the two conditions that make a joint PDF valid.

> **Type:** Theory
> **Answer:** Joint CDF F(x,y) = P(X ≤ x, Y ≤ y); joint PDF f(x,y) with F(x,y) = ∫_{−∞}^x∫_{−∞}^y f(u,v)dv du; joint PMF p(x,y) built from a double sum. A joint PDF is valid iff (i) f(x,y) ≥ 0 and (ii) ∬f(x,y)dxdy = 1, with the mixed derivative F_xy = f existing pointwise.
> **Solution:** The joint law assigns probability to rectangles, and the marginal is obtained by integrating out the discarded dimension. For discrete variables the same structure holds with sums replacing integrals, and p must be non-negative with ΣΣp = 1. The cumulative form is the more fundamental object, because it is monotone in each argument even when no density exists — a discrete joint law has a step-function CDF with no derivative.
> **Key point:** Joint PDF valid ⟺ f ≥ 0 and ∬f = 1; marginals come from integrating out the other variable.

### Q86. Derive the marginal distribution of X from the joint density, and show that every marginal integrates to 1.

> **Type:** Theory
> **Answer:** f_X(x) = ∫_{−∞}^∞ f(x,y)dy. Then ∫f_X(x)dx = ∬f(x,y)dxdy = 1, by normalisation of the joint density.
> **Solution:** Marginalisation is the total-probability formula: specifying X = x says nothing about Y, so the mass at x is the accumulation along the whole y-line. Fubini's theorem justifies interchanging the integrals, and the double integral equals 1 because the joint density was normalised. In cumulative form the same statement is F_X(x) = lim_{y→∞}F(x,y), the joint CDF collapsed onto its first argument.
> **Key point:** f_X(x) = ∫f(x,y)dy; then ∫f_X dx = 1 automatically, and F_X(x) = lim_{y→∞}F(x,y).

### Q87. A pair (X, Y) has joint density f(x,y) = cxy on the unit square 0 ≤ x ≤ 1, 0 ≤ y ≤ 1, zero elsewhere. Find c, the marginals, and P(X > Y).

> **Type:** Numerical
> **Answer:** c = 4; f_X(x) = 2x and f_Y(y) = 2y on [0,1]; P(X > Y) = 0.5.
> **Solution:** Normalisation gives c∫₀¹∫₀¹ xy dy dx = c(1/2)(1/2) = c/4 = 1, so c = 4. The marginals are f_X(x) = ∫₀¹4xy dy = 4x(1/2) = 2x and f_Y(y) = 2y, each integrating to 1. For P(X > Y), integrate over the upper triangle: ∫₀¹∫₀^x 4xy dy dx = ∫₀¹4x(x²/2)dx = 2∫₀¹x³dx = 2(1/4) = 0.5. The quick route is symmetry: f(x,y) is symmetric under swapping x and y, so the diagonal x = y splits the unit mass into two equal halves.
> **Key point:** c = 4 for f = cxy on the unit square; marginals are 2x and 2y, and P(X>Y) = 1/2 by symmetry about the diagonal.

### Q88. State the formulas for the conditional density and conditional CDF, and explain the "conditioning strip" interpretation.

> **Type:** Theory
> **Answer:** f_{X|Y}(x|y) = f(x,y)/f_Y(y) for f_Y(y) > 0, i.e. P(X ∈ dx | Y = y) = f_{X|Y}(x|y)dx. The conditional CDF is F_{X|Y}(x|y) = P(X ≤ x, Y = y)/P(Y = y) in the discrete case and (1/f_Y(y))∫_{−∞}^x f(u,y)du in the continuous case.
> **Solution:** Conditioning is renormalisation: restrict the joint law to the strip y = constant and divide by that strip's total mass f_Y(y), which is why the conditional density integrates to 1 in x. For a continuous Y the event {Y = y} has probability zero, so the conditional law is properly defined as the limit of conditional probabilities over shrinking intervals around y — the substitution itself is a notational convenience, not a division by zero.
> **Key point:** f_{X|Y}(x|y) = f(x,y)/f_Y(y); conditioning is the joint law renormalised on the strip y = const.

### Q89. A pair has joint density f(x,y) = c·x on the triangle 0 ≤ x ≤ y ≤ 1, zero elsewhere. Find c, the marginal of Y, the conditional density of X given Y = y, and P(X < 0.5 | Y = 0.5).

> **Type:** Numerical
> **Answer:** c = 6; f_Y(y) = 3y²; f_{X|Y}(x|y) = 2x/y² on 0 ≤ x ≤ y; P(X < 0.5 | Y = 0.5) = 1.
> **Solution:** Normalising first, ∫₀¹∫₀^y c·x dx dy = ∫₀¹c(y²/2)dy = c/6 = 1, so c = 6 and the density is 6x. Then f_Y(y) = ∫₀^y 6x dx = 3y², which integrates to 1 as required. The conditional density is f_{X|Y}(x|y) = 6x/(3y²) = 2x/y² on 0 ≤ x ≤ y, which integrates to ∫₀^y2x/y²dx = 1 ✓. At y = 0.5 the support forces X ≤ 0.5, so P(X < 0.5 | Y = 0.5) = 1, confirmed by ∫₀^{0.5} 2x/0.25 dx = ∫₀^{0.5}8x dx = 8(0.125) = 1.
> **Key point:** Normalise the joint first: f = 6x, so f_Y(y) = 3y² and f_{X|Y}(x|y) = 2x/y²; the constraint X ≤ Y forces the conditional probability equal to 1.

### Q90. X and Y are jointly normal with E[X] = 0, E[Y] = 1, Var(X) = 4, Var(Y) = 9 and correlation 0.6. Compute Cov(X,Y) and Var(Y + 2X).

> **Type:** Numerical
> **Answer:** Cov(X,Y) = ρσ_Xσ_Y = 0.6 × 2 × 3 = 3.6. Var(Y + 2X) = 9 + 4(4) + 2(2)(1)(3.6) = 9 + 16 + 14.4 = 39.4, so σ ≈ 6.277.
> **Solution:** Cov(X,Y) = ρ·σ_X·σ_Y = 0.6 × 2 × 3 = 3.6 by the definition of the correlation coefficient. For the linear combination, Var(aX + bY) = a²Var(X) + b²Var(Y) + 2ab Cov(X,Y); with a = 2, b = 1 this is 4(4) + 1(9) + 2(2)(1)(3.6) = 16 + 9 + 14.4 = 39.4. The cross term 2ab Cov is exactly what candidates drop — omitting it would give 25 instead of 39.4.
> **Key point:** Var(aX + bY) = a²Var(X) + b²Var(Y) + 2ab Cov(X,Y); here 16 + 9 + 14.4 = 39.4, and dropping the cross term wrongly gives 25.

### Q91. Show that for jointly normal X and Y, Cov(X,Y) = 0 implies independence, and state the exact condition that makes this implication valid.

> **Type:** Theory
> **Answer:** For jointly normal X, Y, Cov(X,Y) = 0 ⟹ X and Y are independent. The condition is the **joint** normality of the pair — not normality of the marginals alone, and not mere existence of a joint density.
> **Solution:** The joint normal density is exp(−½qᵀΣ⁻¹q)/(2π√|Σ|). When the off-diagonal entries of Σ vanish, Σ is diagonal, so Σ⁻¹ is diagonal, the exponent splits into two independent pieces and the density factorises into the product of the marginals. This is exceptional behaviour: for general distributions uncorrelated does not imply independent, and the failure is structural rather than an artefact of choice, as the next question shows.
> **Key point:** Jointly normal + Cov = 0 ⟹ independent; for non-normal laws uncorrelated ≠ independent.

### Q92. Construct an explicit counterexample showing that zero covariance does not imply independence for a general distribution.

> **Type:** Conceptual
> **Answer:** Let X take −1, 0, +1 with probabilities 1/4, 1/2, 1/4, and set Y = X². Then E[X] = 0, E[Y] = 1/2, E[XY] = E[X³] = 0, so Cov(X,Y) = 0, yet P(Y = 1 | X = 0) = 0 whereas P(Y = 1) = 1/2, so X and Y are dependent.
> **Solution:** Odd moments of a symmetric variable vanish, so any even function of a symmetric X is uncorrelated with it while being completely determined by it. The general principle is that covariance measures only the strength of the *linear* relationship: Y = f(X) for a nonlinear symmetric f is invisible to Cov but glaring to any measure of full dependence. This is also why a linear detector loses to a nonlinear energy or correlation detector when such structure is present.
> **Key point:** Cov measures only linear dependence: Y = X² with symmetric X gives Cov = 0 while X and Y are fully dependent.

### Q93. State the Cauchy–Schwarz bound on the correlation coefficient and prove that |ρ| = 1 occurs exactly when one variable is an affine function of the other.

> **Type:** Theory
> **Answer:** |ρ| = |Cov(X,Y)|/(σ_Xσ_Y) ≤ 1, with equality iff Y − E[Y] = a(X − E[X]) almost surely for some a ≠ 0. The sign of a fixes the sign: ρ = +1 for a > 0, ρ = −1 for a < 0.
> **Solution:** Cauchy–Schwarz gives E[|XY|] ≤ √(E[X²]E[Y²]); centring both variables and applying the same inequality to X − μ_X and Y − μ_Y yields |Cov(X,Y)| ≤ σ_Xσ_Y. Equality in Cauchy–Schwarz holds precisely when the two centred random variables are linearly dependent almost surely, which is the affine condition. The bound is therefore an algebraic fact about the inner product, not a statistical regularity, and it is attained only by perfect affine relations.
> **Key point:** |ρ| ≤ 1 with equality iff Y = aX + b a.s.; ρ = ±1 means a perfect linear relation, not merely a strong one.

### Q94. State the total expectation and total variance formulas, and explain the interpretation of the variance decomposition.

> **Type:** Theory
> **Answer:** E[X] = E_Y[E[X|Y]] = Σ_y E[X|Y = y]P(Y = y). Var(X) = E[Var(X|Y)] + Var(E[X|Y]).
> **Solution:** Conditioning on Y partitions the sample space into disjoint layers, and averaging the layer means weighted by the layer masses returns the overall mean. The variance identity splits X − μ into (X − E[X|Y]) + (E[X|Y] − μ); averaging the squared first part gives E[Var(X|Y)] and the second gives Var(E[X|Y]). It is the same structure as the ANOVA decomposition and quantifies exactly how much of the spread is between-stratum rather than within-stratum.
> **Key point:** E[X] = E[E[X|Y]] and Var(X) = E[Var(X|Y)] + Var(E[X|Y]) — within-stratum plus between-stratum variance.

### Q95. X has mean 2 and variance 6. Given Y, the conditional mean is E[X|Y] = 2 + 0.5(Y − 1) and the conditional variance is 3. Find Var(Y) and the fraction of Var(X) explained by Y.

> **Type:** Numerical
> **Answer:** Var(Y) = 12, Var(E[X|Y]) = 3, and the fraction of variance explained is 3/6 = 0.5.
> **Solution:** Since the conditional mean is affine in Y, Var(E[X|Y]) = 0.5²Var(Y) = 0.25Var(Y). Substituting into the total-variance identity, 6 = 3 + 0.25Var(Y), so Var(Y) = 12 and Var(E[X|Y]) = 0.25 × 12 = 3. The ratio Var(E[X|Y])/Var(X) = 3/6 = 0.5 is the fraction of total variance accounted for by conditioning on Y — the multiple-R² idea, with the other half of the spread irreducible noise.
> **Key point:** Var(Y) = 12 and Var(E[X|Y]) = 3, so conditioning on Y explains exactly 50% of Var(X).

### Q96. For jointly normal X, Y with means μ₁, μ₂, variances σ₁², σ₂² and correlation ρ, state the conditional normal density of X given Y = y.

> **Type:** Theory
> **Answer:** f_{X|Y}(x|y) = (1/(σ₁√(2π)))exp(−(x − μ₁ − (ρσ₁/σ₂)(y − μ₂))²/(2σ₁²(1−ρ²))). Equivalently X|Y = y ~ N(μ₁ + (ρσ₁/σ₂)(y − μ₂), σ₁²(1−ρ²)).
> **Solution:** The result comes from completing the square in the joint density, which factorises into the marginal of y times this conditional. The conditional mean is the best linear predictor of X from Y — the regression line — and the conditional variance shrinks by (1 − ρ²), reaching σ₁² when ρ = 0 and collapsing to zero as |ρ| → 1. This conditional-normal structure is the entire basis of the Kalman filter update step and of matched-filter performance analysis.
> **Key point:** X|Y=y ~ N(μ₁ + ρ(σ₁/σ₂)(y−μ₂), σ₁²(1−ρ²)); conditional variance shrinks by the factor (1−ρ²).

### Q97. Let X and Y be independent exponential(λ) variables. Find the conditional distribution of X given X + Y = s, and explain why this decomposition is useful.

> **Type:** Numerical
> **Answer:** f_{X|S}(x|s) = 1/s on 0 ≤ x ≤ s, i.e. X | S = s ~ Uniform(0, s). Consequently X/S is Uniform(0,1) and is independent of S.
> **Solution:** The joint density is λ²e^{−λ(x+y)} = λ²e^{−λs} on the line x + y = s, which is constant along that line, so after renormalising to length s the conditional density is uniform. Since the joint density is λ²e^{−λs} times a constant in the fractional coordinate, the fraction x/s and the total s are statistically independent. This is the classical gamma/dirichlet and Poisson/binomial decomposition, and it is exactly why the Erlang CDF factorises as a finite exponential sum and why the ratio of two iid gammas with equal shape is beta-distributed.
> **Key point:** Given X + Y = s with iid exponential parts, X ~ Uniform(0, s): the fraction and the total are independent — a standard beta/gamma decomposition.

### Q98. Define the covariance matrix of a random vector and state the three structural properties it must have.

> **Type:** Theory
> **Answer:** For X = [X₁, …, Xₙ]ᵀ, Σ = E[(X − μ)(X − μ)ᵀ] with entries Σᵢⱼ = Cov(Xᵢ, Xⱼ). It is (i) symmetric, Σᵢⱼ = Σⱼᵢ, (ii) positive semi-definite, vᵀΣv = Var(vᵀX) ≥ 0 for all real v, and (iii) unit-diagonal when it is a correlation matrix.
> **Solution:** Symmetry follows because Cov(Xᵢ,Xⱼ) = E[(Xᵢ−μᵢ)(Xⱼ−μⱼ)] − μᵢμⱼ is symmetric in the indices. Positive semi-definiteness is precisely the statement that a linear combination's variance, being a squared deviation, can never be negative. This structure is what a joint normal density needs: since the density requires Σ⁻¹, one needs positive *definiteness*, all eigenvalues strictly positive, and the equality cases are the degenerate distributions supported on a subspace.
> **Key point:** Σ is symmetric, positive semi-definite (vᵀΣv = Var(vᵀX) ≥ 0), and has unit diagonal when it is a correlation matrix.

### Q99. Two random variables X and Y are uncorrelated with equal variances. Show that X + Y and X − Y are uncorrelated, and state the extra condition under which they are also independent.

> **Type:** Theory
> **Answer:** Cov(X+Y, X−Y) = Cov(X,X) − Cov(X,Y) + Cov(Y,X) − Cov(Y,Y) = Var(X) − Var(Y) = 0 when the variances are equal. They are additionally **independent** iff X and Y are jointly normal.
> **Solution:** Expanding with the bilinearity of covariance gives Var(X) − Var(Y), because Cov is symmetric and vanishes. Independence of the sum and difference is strictly stronger: a 45° rotation of a jointly Gaussian vector is again jointly Gaussian, and its two new coordinates are uncorrelated, hence independent by the normal special property. In a receiver this rotation is the standard decorrelating step, with X + Y carrying signal and X − Y carrying only noise — the algebraic basis of quadrature error analysis.
> **Key point:** Cov(X+Y, X−Y) = Var(X) − Var(Y) = 0; the two are independent iff X, Y are jointly normal.

### Q100. Show that for Y = aX + b the correlation coefficient is sign(a), independent of both the slope magnitude and the offset.

> **Type:** Numerical
> **Answer:** ρ = +1 for a > 0 and ρ = −1 for a < 0, regardless of |a| and b. For Y = 3X + 4, ρ = 1.
> **Solution:** Cov(X,Y) = a Var(X) and Var(Y) = a²Var(X), so σ_Y = |a|σ_X and ρ = a Var(X)/(σ_X·|a|σ_X) = a/|a|. The constant 4 never appears and the magnitude 3 cancels completely. This invariance is what makes correlation a scale-free orientation measure: the sign of the slope is read off from the tilt of a scatter plot, while the residual scatter about the line carries the value of ρ.
> **Key point:** For Y = aX + b, ρ = a/|a| = ±1; correlation is invariant to shift and scale on either variable.

### Q101. Show that E[XY] = Cov(X,Y) + E[X]E[Y], and compute E[XY] for independent variables with means 3 and 2.

> **Type:** Numerical
> **Answer:** E[XY] = Cov(X,Y) + E[X]E[Y]. For independent X, Y, Cov = 0, so E[XY] = 3 × 2 = 6.
> **Solution:** Expanding the definition, Cov(X,Y) = E[(X−μ_X)(Y−μ_Y)] = E[XY] − μ_XE[Y] − μ_YE[X] + μ_Xμ_Y = E[XY] − E[X]E[Y], and inverting gives the identity. Independence implies E[XY] = E[X]E[Y] and hence Cov = 0, which is precisely why the cross term vanishes in Var(X+Y) for independent summands. If instead the pair were correlated with covariance 0.5, the answer would be 6 + 0.5 = 6.5.
> **Key point:** E[XY] = E[X]E[Y] + Cov(X,Y); independence makes E[XY] factorise, killing the cross term in Var(X+Y).

### Q102. A bivariate normal pair has correlation ρ = 0.8. What fraction of the prior variance of X remains after the best linear estimate from Y, and what does the estimate reduce it by?

> **Type:** Numerical
> **Answer:** Var(X|Y) = Var(X)(1 − 0.8²) = 0.36 Var(X). The residual is 36% of the prior and the reduction is 64%, so ρ² = 0.64 of the variance is explained.
> **Solution:** For jointly normal variables the conditional variance equals the linear-prediction error variance, Var(X|Y) = σ_X²(1−ρ²). With ρ = 0.8, 1 − 0.64 = 0.36, so the best linear estimate leaves 0.36σ_X². The mean-squared estimation error is exactly this quantity, and it vanishes as ρ → 1 because the estimate becomes exact. Note the asymmetry: the explained fraction is ρ² but the remaining fraction is 1 − ρ², a distinction that matters whenever ρ is close to 1.
> **Key point:** The best linear estimate leaves Var(X)(1−ρ²) = 0.36 Var(X) at ρ = 0.8; the fraction explained is ρ² = 0.64.

### Q103. Give the joint PDF of a bivariate normal in matrix form and state the condition for it to be a valid density.

> **Type:** Theory
> **Answer:** f(x) = (2π)^{−n/2}|Σ|^{−1/2}exp(−½(x−μ)ᵀΣ⁻¹(x−μ)) for an n-vector x. It is a valid density exactly when Σ is symmetric and positive **definite**, i.e. all eigenvalues strictly positive, equivalently |Σ| > 0.
> **Solution:** The density arises from the change of variables y = Σ^{−1/2}(x − μ) applied to a spherical Gaussian, which contributes the Jacobian factor |Σ|^{−1/2}. The requirement of strict positive definiteness, rather than mere semi-definiteness, is what makes Σ⁻¹ exist at all. A singular Σ collapses the distribution onto a lower-dimensional subspace, which happens when ρ = ±1 and the two variables are perfectly linearly related — a real law, but not a joint density.
> **Key point:** Bivariate normal is a valid density only for symmetric positive **definite** Σ; ρ = ±1 gives a singular Σ and a degenerate line-supported law.

### Q104. Let X and Y be independent N(0,1). Find P(X² + Y² ≤ 1) and identify the distribution of the sum.

> **Type:** Numerical
> **Answer:** X² + Y² ~ χ²(2) = Gamma(shape 1, rate 1/2), which is exponential with rate 1/2. P(X² + Y² ≤ 1) = 1 − e^{−1/2} ≈ 0.3935.
> **Solution:** The sum of the squares of k independent standard normals is chi-square with k degrees of freedom, so X² + Y² ~ χ²(2) = Gamma(1, 1/2). A chi-square with 2 degrees of freedom has CDF 1 − e^{−x/2}, so at x = 1 the probability is 1 − e^{−0.5} = 1 − 0.606531 ≈ 0.39347. A direct geometric check agrees: the joint density is rotationally symmetric with total mass 1 on ℝ², and the unit disc is the set x² + y² ≤ 1 whose enclosed mass this value gives.
> **Key point:** X² + Y² ~ χ²(2) = exponential(rate 1/2), so P(X² + Y² ≤ 1) = 1 − e^{−1/2} ≈ 0.3935.

### Q105. Which of the following statements about jointly Gaussian variables are true?

> **Type:** MSQ (GATE-2)
> **Answer:** Statements (a), (c) and (d) are true; (b) is false. (Options a, c, d)
>
> (a) Every linear combination of jointly Gaussian variables is Gaussian.
> (b) Uncorrelated variables of any distribution are independent.
> (c) Every linear combination of uncorrelated jointly Gaussian variables is Gaussian.
> (d) The joint density factorises if and only if the covariance matrix is diagonal.
> **Solution:** (a) is true by the definition of joint normality — the MGF factorises into a product of Gaussian MGFs. (b) is false, with the counterexample Y = X² for symmetric X, which is perfectly dependent yet uncorrelated. (c) is true: with a diagonal Σ the MGF of a linear combination reduces to a single Gaussian exponential in s, so the combination is Gaussian, and no correlation term appears. (d) is true provided the covariance matrix is positive definite: a diagonal Σ makes the quadratic form split and the density factorise, and factorisation forces a diagonal Σ, since the factorised density has a log-density that is a sum of separate functions and so must have no cross term. The qualification matters — a singular Σ admits factorised representations that are not diagonal in the given basis, which is the standard form's excluded degenerate case. Statements (a), (c) and (d) hold.
> **Key point:** Statements (a), (c) and (d) are true; (b) fails for non-Gaussian laws, where uncorrelated ≠ independent.

### Q106. X and Y are jointly normal with correlation ρ and equal variances. Show that (X+Y, X−Y) is jointly normal and find its correlation.

> **Type:** Numerical
> **Answer:** The transformed pair is jointly normal by the closure property, and its correlation is 0, so the two are independent. For unequal variances the general value is ρ' = (σ_X² − σ_Y²)/(σ_X² + σ_Y²).
> **Solution:** A linear transformation of a jointly normal vector is jointly normal, so no derivation is needed. Computing Cov(X+Y, X−Y) = Var(X) − Var(Y) = 0 for equal variances, and Var(X±Y) = σ_X² + σ_Y² for both, the correlation is 0. Together with joint normality this makes the sum and difference independent. This 45° rotation is the decorrelating transform for a quadrature receiver pair, where the sum carries signal and the difference carries only noise — the algebraic core of quadrature error analysis.
> **Key point:** The 45° rotation (X+Y, X−Y) is a joint-Gaussian decorrelating transform giving ρ' = (σ_X²−σ_Y²)/(σ_X²+σ_Y²), which is 0 for equal variances.

---

### Q107. A random variable X is the magnitude of a zero-mean complex Gaussian whose in-phase and quadrature components each have standard deviation σ. What are E[X] and E[X²]?

> **Type:** MCQ (GATE-2)
> **Answer:** E[X] = σ√(π/2) ≈ 1.2533σ and E[X²] = 2σ². (Option d)
>
> (a) E[X] = σ, E[X²] = σ²
> (b) E[X] = σ√(π/2), E[X²] = σ²
> (c) E[X] = σ√2, E[X²] = 2σ²
> (d) E[X] = σ√(π/2), E[X²] = 2σ²
> **Solution:** Two orthogonal zero-mean Gaussians give the Rayleigh envelope X = √(V₁² + V₂²). The second moment is immediate: E[V₁² + V₂²] = σ² + σ² = 2σ², so E[X²] = 2σ². The mean requires the Rayleigh integral: E[X] = ∫₀^∞ x·(x/σ²)e^{−x²/(2σ²)}dx = σ∫₀^∞ u e^{−u²/2}du = σ√(π/2), using u = x/σ. So Var = 2σ² − πσ²/2 = (2 − π/2)σ². Option (b) is the most common wrong answer, from assuming the envelope's second moment equals the component variance.
> **Key point:** Rayleigh: E[X²] = 2σ² (just the sum of component variances) but E[X] = σ√(π/2) ≈ 1.2533σ; Var = (2 − π/2)σ².

---
## Section 5. Transformations of random variables: functions, sums and convolution (Q108–Q126)

### Q108. Derive the PDF of Y = g(X) for a monotone increasing g from the CDF of X.

> **Type:** Theory
> **Answer:** F_Y(y) = P(g(X) ≤ y) = P(X ≤ g⁻¹(y)) = F_X(g⁻¹(y)), so f_Y(y) = f_X(g⁻¹(y))·|d g⁻¹(y)/dy| for y in the range of g. For a monotone **decreasing** g, the inequality reverses and the same formula holds with the absolute value of the derivative.
> **Solution:** The derivation works for a monotone g because the pre-image of the interval (−∞, y] under g is a single interval, either (−∞, g⁻¹(y)] or [g⁻¹(y), ∞), and the probability of that set is F_X(g⁻¹(y)) or 1 − F_X(g⁻¹(y)) respectively. Differentiating with respect to y gives the density. The absolute value is needed because a density is a non-negative rate of change, and for a decreasing g the CDF decreases with y. Non-monotone g generally produces a multi-valued inverse and the density becomes a **sum** over all pre-images.
> **Key point:** f_Y(y) = f_X(g⁻¹(y))·|d g⁻¹/dy| for monotone g; for non-monotone g, sum over all branches of the inverse.

### Q109. X is exponential with rate λ and Y = 2X. Find the distribution of Y, its mean, and its PDF.

> **Type:** Numerical
> **Answer:** Y is exponential with rate λ/2 (scale 2/λ). Mean = 2/λ, Var = 4/λ², and f_Y(y) = (λ/2)e^{−λy/2} for y ≥ 0.
> **Solution:** With g(x) = 2x, the inverse is g⁻¹(y) = y/2 and |dg⁻¹/dy| = 1/2, so f_Y(y) = f_X(y/2)·(1/2) = λe^{−λy/2}·(1/2) = (λ/2)e^{−λy/2}. The mean is 2/λ and the variance is 2²/λ² = 4/λ² by the scaling rule. Multiplying an exponential by a constant scales the **rate** down by that constant, not up — a common source of error when the transformation is written as Y = X/2.
> **Key point:** Y = 2X: rate drops to λ/2, so mean 2/λ and var 4/λ²; f_Y = (λ/2)e^{−λy/2}. Scaling X by k scales the rate by 1/k.

### Q110. X ~ N(μ, σ²) and Y = aX + b with a > 0. Give the distribution of Y and justify it from the density transformation.

> **Type:** Theory
> **Answer:** Y ~ N(aμ + b, a²σ²), with f_Y(y) = (1/(aσ√(2π)))exp(−(y − aμ − b)²/(2a²σ²)).
> **Solution:** The inverse transformation is x = (y − b)/a with dx/dy = 1/a, so f_Y(y) = f_X((y−b)/a)·(1/a). Substituting f_X and expanding the exponent gives exactly the Gaussian form with mean aμ + b and variance a²σ², since the prefactor 1/a combines with the 1/σ in f_X. The mean and variance also follow from the affine rules E[aX+b] = aμ + b and Var(aX+b) = a²σ², and the two derivations must agree — a useful check.
> **Key point:** Affine image of a normal: aX + b ~ N(aμ + b, a²σ²); the density picks up a factor 1/|a|.

### Q111. X is uniform on [0, 1] and Y = X². Find the PDF and CDF of Y and its mean.

> **Type:** Numerical
> **Answer:** f_Y(y) = 1/(2√y) on 0 < y < 1, F_Y(y) = y, and E[Y] = 1/3.
> **Solution:** g(x) = x² is monotone increasing on [0,1] with inverse g⁻¹(y) = √y and dg⁻¹/dy = 1/(2√y), so f_Y(y) = f_X(√y)·(1/(2√y)) = 1/(2√y). Integrating, F_Y(y) = ∫₀^y 1/(2√t)dt = √y, which is also immediate from P(X² ≤ y) = P(X ≤ √y) = √y. The density diverges at y = 0 as 1/(2√y) yet is integrable, illustrating that an infinite density at a point is perfectly legal. The mean is E[X²] = ∫₀¹x²dx = 1/3, or directly ∫₀¹y·(1/(2√y))dy = 1/2∫₀¹√y dy = 1/3.
> **Key point:** Y = X² on X~U(0,1): f_Y(y) = 1/(2√y), F_Y(y) = √y, E[Y] = 1/3; an infinite density at 0 is integrable and legal.

### Q112. X ~ N(0, 1) and Y = X². Find the distribution of Y and use it to show that the sample correlation of two independent normals is close to 0.

> **Type:** Numerical
> **Answer:** Y = X² ~ χ²(1) = Gamma(1/2, rate 1/2) with f_Y(y) = e^{−y/2}/√(2πy) for y > 0 and mean 1. For two independent N(0,1) samples of size n ≥ 2, the sample correlation r has E[r] = 0 by symmetry and E[r²] = 1/(n−1), so the rms spread is 1/√(n−1) and r concentrates near 0.
> **Solution:** Squaring folds the two tails of the standard normal onto y > 0, giving the chi-square density (1/√(2πy))e^{−y/2} with mean E[X²] = 1. For the correlation, write r = Σᵢxᵢyᵢ/√((Σxᵢ²)(Σyᵢ²)) with x, y independent standard-normal vectors of length n. Swapping x and y sends r to −r and leaves the joint law unchanged, so E[r] = 0 exactly. The ratio has a heavy tail, so its mean square rather than its variance is the convenient quantity: by rotational symmetry, conditioning on the direction of x in Rⁿ, E[r² | x] = (Σᵢxᵢyᵢ)²/((Σxᵢ²)(Σyᵢ²)) averaged over y gives (Σxᵢ²)/((Σxᵢ²)(Σyᵢ²)) = 1/Σyᵢ², and E[1/Σyᵢ²] = 1/(n−1) because Σyᵢ² is chi-square with n degrees of freedom. Hence the rms spread is 1/√(n−1), and the statistically important point is that two unrelated noise waveforms become uncorrelated in the large-sample limit.
> **Key point:** X² ~ χ²(1) = Gamma(1/2, 1/2) with mean 1; the sample correlation of two independent normal samples of size n has E[r] = 0 by symmetry and rms 1/√(n−1), so it vanishes as n grows.

### Q113. What is the general form of the density of Y = |X| when X has a symmetric density f_X?

> **Type:** Theory
> **Answer:** f_Y(y) = f_X(y) + f_X(−y) for y > 0, and 0 for y < 0; for a symmetric f_X this collapses to f_Y(y) = 2f_X(y) for y > 0. There is no atom at y = 0 when X is continuous, since P(Y = 0) = P(X = 0) = 0.
> **Solution:** The event {Y = y} for y > 0 is the disjoint union {X = y} and {X = −y}, so the probabilities add and the density is the sum of the two branches of the inverse, exactly as the non-monotone rule requires. For a symmetric f_X the two contributions are equal, doubling the density on the positive axis, and the total mass is ∫₀^∞2f_X(y)dy = 1 because the two halves of a symmetric density each carry 1/2. The doubling is not a change of distribution but a change of support: all the probability that used to sit on the negative axis is folded onto the positive one. This is exactly how a half-normal is obtained from a normal, and its mean is σ√(2/π) ≈ 0.7979σ.
> **Key point:** For Y = |X| with symmetric f_X: f_Y(y) = 2f_X(y) for y > 0, 0 for y < 0, no atom at 0; this is the half-normal when X is Gaussian.

### Q114. Two independent variables X ~ U(0,1) and Y ~ U(0,1) are added. Find the density of S = X + Y and verify it is a triangle.

> **Type:** Numerical
> **Answer:** f_S(s) = s for 0 ≤ s ≤ 1 and 2 − s for 1 < s ≤ 2, zero elsewhere. Mean = 1, Var = 1/6, and f_S(s) = 1 − |s − 1|.
> **Solution:** The convolution f_S(s) = ∫f_X(t)f_Y(s − t)dt counts the length of the overlap of the unit interval with its shift, which is s for s ∈ [0,1] and 2 − s for s ∈ [1,2]. Normalising: ∫₀¹s ds + ∫₁²(2−s) ds = 0.5 + 0.5 = 1 ✓. The mean is 0.5 + 0.5 = 1 by additivity, and the variance is 1/12 + 1/12 = 1/6, matching the triangular density centred at 1.
> **Key point:** The sum of two U(0,1) is triangular: f_S(s) = 1 − |s−1|, mean 1, var 1/6. The convolution integral counts interval overlap.

### Q115. State the convolution theorem for sums of independent continuous random variables, in both PDF and CDF form.

> **Type:** Theory
> **Answer:** PDF form: f_{X+Y}(z) = (f_X * f_Y)(z) = ∫_{−∞}^{∞} f_X(x)f_Y(z − x)dx. CDF form: F_{X+Y}(z) = ∫_{−∞}^{∞} F_X(z − y)f_Y(y)dy. Both require independence.
> **Solution:** The PDF form is just the total-probability formula for the event "X + Y lands in dz", written with the indicator 1{x + y ∈ dz} = 1{x ∈ [z − y, z − y + dy]}, which forces X ∈ dz and Y ∈ z − X. The CDF form is the inner integral of the PDF form by Fubini, and it is more robust numerically because the CDF of a sum is a one-dimensional integral even when the PDF would require a two-dimensional region. Both collapse to the MGF statement M_{X+Y}(s) = M_X(s)M_Y(s).
> **Key point:** f_{X+Y} = f_X * f_Y and F_{X+Y}(z) = ∫F_X(z−y)f_Y(y)dy; independence is required for both.

### Q116. Derive the density of the sum of n independent exponential(λ) variables, and give its mean, variance and MGF.

> **Type:** Numerical
> **Answer:** f_S(s) = λⁿs^{n−1}e^{−λs}/(n−1)! for s > 0 — an Erlang(Γ) distribution. Mean = n/λ, Var = n/λ², MGF = (λ/(λ−s))^n.
> **Solution:** The convolution of two exponentials gives λ²se^{−λs}, and folding in another factor of λe^{−λs} by convolution builds up the pattern λⁿs^{n−1}/(n−1)!, which can be verified by induction or by the MGF: since each summand has MGF λ/(λ−s), independence gives the n-th power, and expanding a negative binomial series identifies the Erlang density. The moments follow from additivity: n summands each with mean 1/λ and variance 1/λ² give n/λ and n/λ².
> **Key point:** Sum of n iid Exponential(λ) = Erlang(n, λ): mean n/λ, var n/λ², MGF (λ/(λ−s))^n, density λⁿs^{n−1}e^{−λs}/(n−1)!.

### Q117. Derive the density of the sum of two independent Rayleigh variables with scale σ, and explain why the closed form is piecewise.

> **Type:** Numerical
> **Answer:** For s > 0, f_S(s) = (√π/(2σ³))erf(s/(2σ))(s²/2 − σ²)e^{−s²/(4σ²)} + (s/(2σ²))e^{−s²/(2σ²)}, a single expression built from the error function. E[S] = 2σ√(π/2) = σ√(2π) ≈ 2.5066σ and Var = 2(2 − π/2)σ² = (4 − π)σ² ≈ 0.8584σ².
> **Solution:** S = X₁ + X₂ is the sum of the radii of two independent isotropic 2-D Gaussian pairs, so the direct route is the ordinary convolution f_S(s) = ∫₀^s (x/σ²)e^{−x²/(2σ²)}·((s−x)/σ²)e^{−(s−x)²/(2σ²)}dx. The support is s ≥ 0 with no internal breakpoint, so the answer is a single expression rather than a piecewise one; piecewise formulas of this shape arise when summing radii whose joint density is computed over a region of overlap. Evaluating the integral: put u = x − s/2 so x(s−x) = s²/4 − u² and x² + (s−x)² = 2u² + s²/2, giving f_S(s) = (e^{−s²/(4σ²)}/σ⁴)[(s²/4)∫_{−s/2}^{s/2}e^{−u²/σ²}du − ∫_{−s/2}^{s/2}u²e^{−u²/σ²}du]. Using ∫e^{−u²/σ²}du = σ√π erf(u/σ) and ∫u²e^{−u²/σ²}du = (σ²/2)[(σ√π/2)erf(u/σ) − u e^{−u²/σ²}] yields the closed form above, valid for every s > 0. The moments are additive: two Rayleighs each with mean σ√(π/2) and variance (2 − π/2)σ² give E[S] = σ√(2π) and Var = (4 − π)σ².
> **Key point:** Sum of two Rayleighs: f_S(s) = (√π/(2σ³))erf(s/2σ)(s²/2 − σ²)e^{−s²/(4σ²)} + (s/(2σ²))e^{−s²/(2σ²)}, one expression for all s > 0, no piecewise split; mean σ√(2π) ≈ 2.5066σ, var (4−π)σ² ≈ 0.8584σ².

### Q118. Find the distribution of the sum of n independent Bernoulli(p) variables and express the Poisson limit again from this angle.

> **Type:** Theory
> **Answer:** S ~ Binomial(n, p) with P(S = k) = C(n,k)p^k(1−p)^{n−k}. As n → ∞ with p = λ/n the sum tends to Poisson(λ) = e^{−λ}λ^k/k!.
> **Solution:** The sum of independent Bernoulli counts the number of successes in n trials, and the binomial coefficient enumerates which trials succeed. Viewing the same result as a limit, the fixed-k term p^k picks up the factor λ^k and the "no more successes" factor (1 − λ/n)^{n−k} → e^{−λ}, so the mass converges to e^{−λ}λ^k/k! with total mass 1. The physical reading is superposition: rare independent failure events accumulate into a Poisson count, which is why Poisson dominates the mathematics of shot noise, cosmic-ray upsets and queue arrivals.
> **Key point:** Sum of n Bernoulli(p) is Binomial(n,p); the Poisson limit is the superposition of many rare, small-probability events.

### Q119. Given the PDF of a single exponential(λ), derive the PDF of the maximum of n independent samples, and find its expected value for n = 10.

> **Type:** Numerical
> **Answer:** F_M(m) = (1 − e^{−λm})ⁿ, f_M(m) = nλe^{−λm}(1 − e^{−λm})^{n−1}. For n = 10 and λ = 1, E[M] = H₁₀ = 1 + 1/2 + … + 1/10 ≈ 2.9290.
> **Solution:** The maximum is below m exactly when all n samples are below m, and independence turns that into the n-th power of the single-sample CDF. Differentiating gives the density, which is the CDF of an order statistic. For the mean, the general result for the maximum of n iid exponentials with rate λ is H_n/λ, where H_n is the n-th harmonic number; H₁₀ = 1 + 0.5 + 0.3333 + 0.25 + 0.2 + 0.1667 + 0.1429 + 0.125 + 0.1111 + 0.1 = 2.92897. Note this exceeds the single-sample mean of 1 by nearly a factor of 3, since the maximum is an extreme order statistic.
> **Key point:** F_M(m) = (1 − e^{−λm})ⁿ; the mean of the max of n exponential(λ) is H_n/λ, so H₁₀ ≈ 2.929 for λ = 1.

### Q120. X and Y are iid N(μ, σ²). Give the joint normal distribution of the average and the difference, and state what the ratio of a difference to a sum looks like when μ = 0 and when μ ≠ 0.

> **Type:** Numerical
> **Answer:** (X+Y)/2 ~ N(μ, σ²/2) and X − Y ~ N(0, 2σ²), and the two are independent. For μ = 0, (X−Y)/(X+Y) is standard Cauchy (location 0, scale 1). For μ ≠ 0 the sum is no longer zero-mean and the ratio is **not** Cauchy.
> **Solution:** By the linear-combination rule, the average has mean μ and variance (1/4 + 1/4)σ² = σ²/2, so averaging two samples halves the variance. The difference has mean μ − μ = 0 and variance σ² + σ² = 2σ². Also Cov(X−Y, X+Y) = Var(X) − Var(Y) = 0, and the pair is jointly normal, so the two are independent. The ratio-of-independent-normals result requires *both* to be zero-mean: with μ = 0 we may write X−Y = √2σ·N₁ and X+Y = √2σ·N₂ for independent standard N₁, N₂, and N₁/N₂ is standard Cauchy. With μ ≠ 0 the denominator has mean 2μ, so the ratio is a ratio of normals with a nonzero-mean denominator, whose density is the heavier, non-Cauchy convolution form — a standard trap in communications problems about incoherent detection.
> **Key point:** Averaging n iid samples gives var σ²/n; a difference of iid normals is N(0, 2σ²) and is independent of the sum; N₁/N₂ is standard Cauchy **only** when both normals are zero-mean.

### Q121. Explain why the density of a sum of many variables is close to normal, using the Poisson and exponential examples, and state the one caveat about the shape of the summands.

> **Type:** Conceptual
> **Answer:** By the central limit theorem the density of the sum of many independent variables with finite variance approaches a Gaussian with the summed mean and variance. For the exponential, the sum of 20 exponentials(λ) has mean 20/λ and variance 20/λ², whose relative spread σ/μ = 1/√20 = 0.224 is what drives normality. The caveat: the theorem needs a **finite** variance, so a heavy-tailed summand such as the Cauchy (no mean, no variance) never becomes normal.
> **Solution:** The mechanism is that the central limit theorem is a statement about the aggregate of many small contributions, independent of the individual shapes. A useful diagnostic is the coefficient of variation of the sum: for iid summands it is σ/√n, so it falls as 1/√n and by n ≈ 20 to 40 the sum is usually acceptably normal. The Cauchy is the boundary case where no finite variance exists and the sum of any number of Cauchys is again Cauchy, so normality is never reached.
> **Key point:** The CLT guarantees normality from finite variance alone: CV of the sum = σ/√n → 0; Cauchy (no finite variance) never becomes normal.

### Q122. Find the density of the sum S = X + Y when X ~ Exp(1) and Y ~ Exp(2), independent.

> **Type:** Numerical
> **Answer:** f_S(s) = 2(e^{−s} − e^{−2s}) for s > 0, a difference of exponentials; mean = 1.5, var = 1.25. (Here λ₁ = 1, λ₂ = 2, and the general form is f_S(s) = λ₁λ₂(e^{−λ₁s} − e^{−λ₂s})/(λ₂ − λ₁).)
> **Solution:** Convolving f_X(x) = e^{−x} and f_Y(s−x) = 2e^{−2(s−x)} over 0 ≤ x ≤ s: f_S(s) = ∫₀^s 2e^{−x}e^{−2s+2x}dx = 2e^{−2s}∫₀^s e^x dx = 2e^{−2s}(e^s − 1) = 2(e^{−s} − e^{−2s}). The mean is 1 + 1/2 = 1.5 and the variance is 1/λ₁² + 1/λ₂² = 1 + 0.25 = 1.25. Normalising checks: ∫₀^∞2(e^{−s} − e^{−2s})ds = 2(1 − 0.5) = 1 ✓.
> **Key point:** Two exponentials with unequal rates convolve to the difference-of-exponentials form; here mean 1.5, var 1.25.

### Q123. Give the density of the sum of two independent Rayleigh variables of scale σ in a form usable for computation, and state its mean.

> **Type:** Numerical
> **Answer:** f_S(s) = (√π/(2σ³))erf(s/(2σ))(s²/2 − σ²)e^{−s²/(4σ²)} + (s/(2σ²))e^{−s²/(2σ²)} for s > 0, and 0 otherwise; E[S] = 2σ√(π/2) = σ√(2π) ≈ 2.5066σ, Var = 2(2 − π/2)σ² = (4 − π)σ² ≈ 0.8584σ².
> **Solution:** Evaluate f_S(s) = ∫₀^s (x/σ²)e^{−x²/(2σ²)}·((s−x)/σ²)e^{−(s−x)²/(2σ²)}dx by the substitution u = x − s/2, which turns the quartic exponent into a clean Gaussian and the polynomial x(s−x) into s²/4 − u²; the two resulting integrals are the standard erf and the erf-minus-gaussian primitive, giving the expression above. The point worth making is that this density is **not** piecewise: the sum of two Rayleighs is an ordinary convolution over 0 < x < s, with no geometry changing character at any value of s. It needs the error function rather than elementary exponentials because the summand densities are polynomially weighted. The moments are nevertheless trivially additive, since mean and variance add for independent variables: E[S] = 2σ√(π/2) and Var = 2(2 − π/2)σ². Numerically integrating the density gives total mass 1 and mean 2.506628σ, confirming the closed form.
> **Key point:** Sum of two Rayleighs, erf form valid for all s > 0 — not Bessel and not piecewise; mean σ√(2π) ≈ 2.5066σ, var (4 − π)σ² ≈ 0.8584σ².

---

### Q124. Compare the densities of the sum of 2 and the sum of 20 iid U(0,1) variables at the centre, and explain the shape trend.

> **Type:** Comparison
> **Answer:** For n = 2 the density at the centre s = 1 is f(1) = 1, the maximum. For n = 20 the density at the centre s = 10 is f(10) ≈ 1/√(2πn) = 1/√(125.66) ≈ 0.0892, a factor of about 11 lower.
> **Solution:** The sum of n U(0,1) variables is an Irwin–Hall distribution whose density is exactly the convolution of n unit rectangles, converging to N(n/2, n/12). Its central density therefore tends to 1/√(2πn) = 1/√(2π × 20) = 1/√125.66 ≈ 0.0892. The trend is a peak that gets lower and wider, like a Gaussian, while the n = 2 triangular density has a sharp corner at the centre. This is the visual signature of the CLT: repeated convolution rounds off the corners.
> **Key point:** Central density of the sum of n U(0,1) tends to 1/√(2πn); n = 2 gives a peak of 1, n = 20 gives ≈ 0.0892.

### Q125. The sum of n independent variables, each uniform on {0, 1}, is a Binomial. Generalise this: what is the sum of n independent variables, each uniform on {0, 1, …, M−1}?

> **Type:** Theory
> **Answer:** It is a discrete **Irwin–Hall** / "M-ary dice sum" distribution with P(S = k) = M^{−n} Σ_{j=0}^{⌊k/M⌋}(−1)^j C(n,j)C(k − jM + n − 1, n − 1) by inclusion–exclusion; for M = 2 it reduces to Binomial(n, 1/2).
> **Solution:** Each variable is uniform over M values, so there are Mⁿ equiprobable n-tuples, and the count of tuples summing to k is a stars-and-bars count with the upper-bound constraints handled by inclusion–exclusion. The formula is the discrete analogue of the continuous Irwin–Hall density. When M = 2 the sum is Binomial(n, 1/2) since each variable is a fair Bernoulli, and for large n the sum approaches a Gaussian with mean n(M−1)/2 and variance n(M²−1)/12.
> **Key point:** A sum of n uniform-on-{0..M−1} variables is the discrete Irwin–Hall law, reducing to Binomial(n, 1/2) at M = 2 and approaching N(n(M−1)/2, n(M²−1)/12).

### Q126. Which of the following is the correct expression for the density of the sum of two independent exponential random variables of rates λ₁ and λ₂, with λ₁ ≠ λ₂?

> **Type:** MCQ (GATE-2)
> **Answer:** f_S(s) = (λ₁λ₂/(λ₂ − λ₁))(e^{−λ₁s} − e^{−λ₂s}) for s > 0. (Option b)
>
> (a) f_S(s) = (λ₁ + λ₂)e^{−(λ₁+λ₂)s}
> (b) f_S(s) = (λ₁λ₂/(λ₂ − λ₁))(e^{−λ₁s} − e^{−λ₂s}), s > 0
> (c) f_S(s) = λ₁λ₂ s e^{−(λ₁+λ₂)s}
> (d) f_S(s) = (λ₁ − λ₂)/(e^{−λ₁s} − e^{−λ₂s})
> **Solution:** Convolution gives ∫₀^s λ₁e^{−λ₁x}λ₂e^{−λ₂(s−x)}dx = λ₁λ₂e^{−λ₂s}∫₀^s e^{(λ₂−λ₁)x}dx = λ₁λ₂e^{−λ₂s}(e^{(λ₂−λ₁)s} − 1)/(λ₂−λ₁) = (λ₁λ₂/(λ₂−λ₁))(e^{−λ₁s} − e^{−λ₂s}), which is option (b). Option (a) is the answer for **equal** rates, where the expression's limit gives the Erlang(2, λ) density λ²se^{−λs} — the classic trap of forgetting the equal-rate special case. Option (c) resembles the Erlang form but with the wrong rate, and (d) is dimensionally meaningless as a density.
> **Key point:** Unequal rates give the difference-of-exponentials form; equal rates give the Erlang density λ²s e^{−λs}, obtained only by taking the limit λ₂ → λ₁.

---

## Section 6. Linear systems driven by random input: mean, mean square, output correlation (Q127–Q146)

### Q127. A discrete-time LTI system has impulse response h[k]. Let its input be a zero-mean stationary sequence x[k] with autocorrelation R_x[m] = σ_x²δ[m]. Derive the output autocorrelation.

> **Type:** Theory
> **Answer:** R_y[m] = σ_x² Σ_n h[n]h[n+m], so R_y[m] = σ_x²·(h ⋆ h^{⊖})(m). For h[k] = a^k u[k] this is R_y[m] = σ_x²·a^{|m|}/(1 − a²), which decays geometrically — the output is **coloured**, not white. Only a single-tap system (h = δ) leaves the output white.
> **Solution:** Substituting y[k] = Σ_n h[n]x[k−n] into R_y[m] = E[y[k]y[k−m]] and using the sifting property of δ gives σ_x²Σ_{k,n}h[n]h[n−m], which with an index change is the autocorrelation of h itself. For h[k] = a^k u[k], Σ_{k=0}^∞ a^k a^{k+m} = a^m/(1−a²) for m ≥ 0, and symmetry gives a^{|m|}/(1−a²). The key point is that white **input** does not imply white **output**; only the variance σ_x²Σ_k h[k]² depends on the system at m = 0. This corrects the common but wrong slogan that filtering white noise just scales it.
> **Key point:** White input gives R_y[m] = σ_x²(h ⋆ h^⊖)(m), a *coloured* autocorrelation — white-in/white-out holds only for a single-tap system.

### Q128. Express the output mean of an LTI system in terms of the input mean, and state the value of the output DC component.

> **Type:** Theory
> **Answer:** E[y] = H(0)·E[x] for a system with a defined DC gain H(0) = Σ_n h[n] (discrete) or ∫h(t)dt (continuous). The output DC component is exactly E[y], the mean.
> **Solution:** Taking expectations through the convolution, E[y[k]] = Σ_n h[n]E[x[k−n]] = (Σ_n h[n])E[x] using mean stationarity. In the frequency domain this is the value of the output spectrum at f = 0, i.e. the zero-frequency component. A system with zero DC gain, such as a high-pass or band-pass filter, therefore passes zero mean regardless of the input mean, which is why AC coupling is used to remove a DC offset.
> **Key point:** E[y] = H(0)E[x]; a filter with H(0) = 0 blocks the mean (DC) component entirely.

### Q129. An RC low-pass filter has transfer function H(f) = 1/(1 + j2πfRC) and is driven by white noise of PSD S₀ = 2 V²/Hz. Find the output noise power.

> **Type:** Numerical
> **Answer:** σ_y² = ∫_{−∞}^{∞}S₀|H(f)|²df = S₀/(2RC). With S₀ = 2 V²/Hz and RC = 1 ms: σ_y² = 2/(2 × 10⁻³) = 1000 V², so σ_y = 31.6 V.
> **Solution:** The output PSD is S_y(f) = S₀|H(f)|² = 2/(1 + (2πfRC)²), and the total power is its integral over all frequencies. Substituting u = 2πfRC so df = du/(2πRC), the integral becomes (2/(2πRC))∫_{−∞}^{∞}du/(1+u²) = (1/(πRC))·π = 1/(RC). With RC = 10⁻³ s this is 1000 V², giving σ_y = √1000 ≈ 31.6 V. The general rule is that the noise power depends only on the area under |H|², which for a one-pole low-pass of unit DC gain is 1/(2RC) — equivalently the ENBW, as derived in Q138. So the result is linear in S₀ and inversely proportional to RC, and no choice of the corner frequency alone fixes it.
> **Key point:** Noise power through an RC low-pass = S₀·ENBW = S₀/(2RC) = 1000 V² for S₀ = 2 V²/Hz and RC = 1 ms, so σ_y = 31.6 V.

### Q130. A discrete-time system y[n] = 0.5y[n−1] + x[n] is driven by white noise of variance σ_x². Find the output variance.

> **Type:** Numerical
> **Answer:** σ_y² = σ_x²/(1 − 0.25) = 4σ_x²/3 ≈ 1.333σ_x².
> **Solution:** This is a first-order recursive filter, so the impulse response is h[k] = (0.5)^ku[k] and Σ_k h[k]² = Σ_{k=0}^∞(0.25)^k = 1/(1 − 0.25) = 4/3 ≈ 1.3333. Since the input is white, the output variance is σ_x²Σh² = (4/3)σ_x². The mechanism is energy accumulation: the pole at 0.5 stores and re-emits old samples, so the output power exceeds the input power even though the system is nominally a low-pass. Contrast this with a pure FIR average of 2 taps, which gives Σh² = 1/2 and halves the power.
> **Key point:** A pole inside the unit circle amplifies white-noise power: 0.5 pole gives Σh² = 1/(1−0.25) = 1.333, so σ_y² = 1.333σ_x².

### Q131. State the two ways a system output's mean square is computed, and show they agree.

> **Type:** Theory
> **Answer:** In the time domain, E[y²] = ∬ h(u)h(v)R_x(u − v)du dv. In the frequency domain, E[y²] = ∫ S_x(f)|H(f)|²df. They agree by the definition of the PSD as the Fourier transform of the autocorrelation.
> **Solution:** The time-domain form comes from substituting the convolution into E[y(t)y(t)] and writing it as a double integral over the autocorrelation; the frequency-domain form is the Parseval statement that the mean square of a process is the integral of its PSD. Equating them requires R_x(τ) = ∫S_x(f)e^{j2πfτ}df substituted into the double integral, which is exactly the inverse Wiener–Khinchin relation. This equivalence is the basis of every noise-budget calculation in receiver and amplifier design.
> **Key point:** E[y²] = ∬h(u)h(v)R_x(u−v)dudv = ∫S_x(f)|H(f)|²df — the time and frequency noise-power formulas are the same statement.

### Q132. Give the output autocorrelation in terms of the impulse response and the input autocorrelation, and state the form for white input.

> **Type:** Theory
> **Answer:** R_y(τ) = ∬ h(u)h(v)R_x(u − v)du dv, i.e. the **triple convolution** R_y = h ⋆ h^{⊖} ⋆ R_x. For white input R_x(τ) = σ_x²δ(τ), this reduces to R_y(τ) = σ_x²[h ⋆ h^{⊖}](τ), which is not generally a delta — only when h is itself a delta does white input give white output.
> **Solution:** The derivation substitutes y(t) = ∫h(u)x(t−u)du and y(t+τ) = ∫h(v)x(t+τ−v)dv into R_y(τ) = E[y(t)y(t+τ)], then applies the stationarity of R_x. The key subtlety is that R_x(u − v) appears under a double integral, so white input does **not** generally produce white output: the factor h ⋆ h^{⊖} survives. Only a single-tap system h = δ(t) gives R_y = σ_x²δ back. This is the correction to the shorthand "filtering white noise gives white noise", which is true only in that degenerate case; for a recursive filter such as the one-pole system of Q129 the output is coloured, with R_y(m) = σ_x²a^{|m|}/(1 − a²) for a stable pole a.
> **Key point:** R_y = h ⋆ h^⊖ ⋆ R_x. White input gives R_y = σ_x²(h ⋆ h^⊖)(τ), a triangular-like function, **not** white — except for a single-tap system.

### Q133. Define the cross-correlation between two processes and give its property under time reversal, contrasting it with autocorrelation.

> **Type:** Theory
> **Answer:** R_xy(τ) = E[x(t)y(t+τ)] is the cross-correlation. It is generally **not** even: R_xy(−τ) = R_yx(τ), a different quantity. The autocorrelation is always even for real processes, R_x(−τ) = R_x(τ), since it is the correlation of a process with itself.
> **Solution:** Substituting the definition, R_xy(−τ) = E[x(t)y(t−τ)] = E[y(t+τ)x(t)] = R_yx(τ) by commutativity of the product and a shift of the time origin. So time reversal swaps the two processes rather than reproducing the same function. Evenness of the autocorrelation is the same statement with x = y, giving R_x(−τ) = R_x(τ). This asymmetry is why the PSD of a real process is real and even, while a cross-spectral density S_xy(f) need not be.
> **Key point:** R_xy(−τ) = R_yx(τ) — cross-correlation is not even; autocorrelation always is, which is why S_x(f) is real and even but S_xy(f) need not be.

### Q134. A system is driven by input X and output Y. Show that the mean square value of the output equals the mean square of the input plus a term involving the correlation, and identify the system where the extra term vanishes.

> **Type:** Theory
> **Answer:** For an LTI system with input X and output Y, E[Y²] = ∬h(u)h(v)R_x(u−v)dudv; when the input is white, R_x = σ_x²δ, so E[Y²] = σ_x²∫|H(f)|²df. The "extra" dependence on the input spectrum beyond its power appears through R_x; for white input only the flat power level σ_x² matters, and the system shape enters through ∫|H|²df.
> **Solution:** Substituting R_x = ∫S_x(f)e^{j2πf(u−v)}df into the double integral collapses it to ∫S_x(f)|H(f)|²df by Fubini. The striking consequence is that for white input the output power depends only on the total "area" of |H|² and not on how that area is distributed in frequency, which is exactly why two different filters with equal equivalent noise bandwidth deliver equal noise. The case of the term vanishing entirely is H(f) = 0.
> **Key point:** For white input, E[Y²] = σ_x²∫|H|²df — output power depends only on the total area of |H|², the equivalent noise bandwidth.

### Q135. Two one-pole sections with impulse responses aᵏu[k] and bᵏu[k] are cascaded. Find the combined impulse response and evaluate its noise gain Σh[k]² for a = 0.5 and b = 0.2.

> **Type:** Numerical
> **Answer:** h[k] = (a^{k+1} − b^{k+1})u[k]/(a − b), and Σh[k]² = [a²/(1−a²) + b²/(1−b²) − 2ab/(1−ab)]/(a−b)². For a = 0.5, b = 0.2 this is 1.6975, which is 22.2% above the 1.3889 obtained by multiplying the two individual noise gains 1/(1−a²) = 1.3333 and 1/(1−b²) = 1.0417.
> **Solution:** Cascading convolves the two impulse responses: Σ_{j=0}^k a^j b^{k−j} = (a^{k+1} − b^{k+1})/(a − b) by the finite geometric series. Squaring and summing three such series, all of which converge for |a|, |b| < 1, gives the stated expression: Σa^{2k} = a²/(1−a²), Σb^{2k} = b²/(1−b²), and Σa^k b^k = ab/(1−ab). Numerically, a²/(1−a²) = 0.33333, b²/(1−b²) = 0.041667, 2ab/(1−ab) = 0.22222, and dividing the sum 0.152778 by (a−b)² = 0.09 gives 1.697531. The 1.3889 figure is what a purely all-pole model of the same two poles would predict by multiplying their individual gains, 1.333333 × 1.041667; the 1.6975 value is the exact gain of the cascade, and the 22.2% difference is the discrepancy that the naive product misses. The excess comes from the fact that the two sections' noise contributions are correlated through the cascade, which is exactly why cascade order and pole spreading change a biquad's noise while leaving its signal response unchanged.
> **Key point:** Cascading aᵏu[k] with bᵏu[k] gives h[k] = (a^{k+1}−b^{k+1})u[k]/(a−b) and Σh² = [a²/(1−a²) + b²/(1−b²) − 2ab/(1−ab)]/(a−b)² = 1.6975 for a = 0.5, b = 0.2, 22.2% above the product of the individual gains 1.3889.

### Q136. An amplifier has a transfer function with |H(f)|² = 1 for |f| ≤ B and 0 otherwise, scaled by gain G. Driven by white noise of PSD S₀, find the output noise power.

> **Type:** Numerical
> **Answer:** σ_y² = G²S₀·(2B) = 2BG²S₀. With S₀ = 10⁻¹⁸ V²/Hz, B = 1 kHz, G = 100: σ_y² = 2(10³)(10⁴)(10⁻¹⁸) = 2 × 10⁻¹¹ V², so σ_y ≈ 4.47 × 10⁻⁶ V.
> **Solution:** The ideal bandpass passes the flat PSD over the total width 2B, so the output power is G²S₀ times 2B. Substituting, 2B = 2000 Hz, G² = 10⁴, S₀ = 10⁻¹⁸: 2 × 10³ × 10⁴ × 10⁻¹⁸ = 2 × 10⁻¹¹ V², and √(2 × 10⁻¹¹) = √2 × 10⁻⁵·⁵ ≈ 1.414 × 3.162 × 10⁻⁶ ≈ 4.47 × 10⁻⁶ V. The result is the same as saying the output noise density is G²S₀ = 10⁻¹⁴ V²/Hz across a 2 kHz bandwidth.
> **Key point:** An ideal bandpass of total width 2B gives σ_y² = 2B·G²·S₀; here 2 × 10⁻¹¹ V², so σ_y ≈ 4.47 µV.

### Q137. Show that if the input to an LTI system is white, the output PSD is S_y(f) = S_x|H(f)|², and give the corresponding time-domain form.

> **Type:** Theory
> **Answer:** S_y(f) = S_x(f)|H(f)|², and in the time domain R_y(τ) = σ_x²(h ⋆ h^{⊖})(τ) for white input, equivalently R_y = h ⋆ h^{⊖} ⋆ R_x in general.
> **Solution:** Both statements are the same theorem — the input-output spectral relation — reached two ways. In the frequency domain the derivation is short: E[Y(f)Y*(f)] = |H(f)|²E[X(f)X*(f)] because the deterministic multiplier H acts on the input spectrum, and the cross terms between different frequencies vanish by the orthogonality of exponentials. The time-domain form is the triple convolution. The two must be consistent, and they are because S_y is by definition the Fourier transform of R_y.
> **Key point:** S_y(f) = S_x(f)|H(f)|² — the LTI spectral relation, equivalent to the triple-convolution R_y = h ⋆ h^⊖ ⋆ R_x in time.

### Q138. Find the output mean square of y[n] = 0.9y[n−1] + x[n] when x is white with variance σ_x², and contrast with a 2-tap moving average y[n] = (x[n] + x[n−1])/2.

> **Type:** Comparison
> **Answer:** Recursive: h[k] = 0.9^k, so Σh² = 1/(1 − 0.81) = 5.263σ_x². Moving average: h = {1/2, 1/2}, Σh² = 0.5, so 0.5σ_x². The recursive filter delivers 10.5 times more noise power.
> **Solution:** The first-order recursion accumulates: Σ_{k≥0}0.9^{2k} = 1/(1 − 0.81) = 5.2632. The two-tap average has Σh² = (1/2)² + (1/2)² = 0.5. The comparison isolates the cost of recursion: a pole at 0.9 re-injects old samples 9-fold, so it acts as an accumulator, whereas a symmetric FIR average rejects noise. The 10.5× ratio is the standard argument for preferring symmetric FIR sections for precision and low-noise stages.
> **Key point:** Recursion with pole 0.9 gives 5.26σ_x²; a 2-tap average gives 0.5σ_x² — a 10.5× penalty, the standard argument for symmetric FIR in low-noise stages.

### Q139. Define the equivalent noise bandwidth of a filter and give the ENBW of a first-order RC low-pass.

> **Type:** Theory
> **Answer:** ENBW = ∫_{−∞}^{∞}|H(f)|²df / |H(0)|², the width of the ideal brickwall that passes the same power. For a one-pole RC low-pass, |H(0)| = 1 and ∫|H|²df = 1/(2RC), so ENBW = 1/(2RC) Hz and the output noise power is S₀/(2RC). Expressed per one-sided (positive-frequency) integration, the equivalent width is 1/(4RC) Hz and the power is 2·S₀·ENBW_one-sided — the same result, and the 2 is the two-sided/one-sided convention, not a physical factor.
> **Solution:** The definition is normalised by the peak gain so that a flat-top filter of unit gain has ENBW equal to its physical width. With H(f) = 1/(1 + j2πfRC) we have |H|² = 1/(1 + (2πfRC)²) and, substituting u = 2πfRC, ∫_{−∞}^{∞}|H|²df = (1/(2πRC))∫_{−∞}^{∞}du/(1+u²) = (1/(2πRC))·π = 1/(2RC). Hence ENBW = 1/(2RC) and σ_y² = S₀/(2RC), which is the result quoted in Q128. Only the positive-frequency half of the integral is needed if the noise PSD is specified one-sided, so the one-sided ENBW is 1/(4RC) Hz and σ_y² = 2S₀/(4RC) — identical. The engineering point is that ENBW (1/(2RC) = 500 Hz for RC = 1 ms) is 57.1% larger than the 3-dB bandwidth measured between the ±3-dB points, 2f₃ = 1/(πRC) = 318.3 Hz, so a one-pole filter passes far more noise than a brickwall of the same 3-dB width.
> **Key point:** ENBW = ∫|H|²df/|H(0)|² = 1/(2RC) Hz for a one-pole RC low-pass, so σ_y² = S₀/(2RC); this is 1.571× the ±3-dB bandwidth 1/(πRC), which is why the 3-dB bandwidth alone understates receiver noise.

### Q140. A system has h[k] = a^k u[k] and white input of variance 1. Find the output variance, the output PSD, and the −3 dB frequency.

> **Type:** Numerical
> **Answer:** σ_y² = 1/(1 − a²). S_y(f) = 1/(1 + a² − 2a cos(2πf)). The −3 dB frequency satisfies cos(2πf₃) = (a² − 1)/(2a). For a = 0.5: σ_y² = 1.333 and cos(2πf₃) = −0.75, so f₃ = cos⁻¹(−0.75)/(2π) = 2.4189/6.2832 ≈ 0.3850 cycles/sample.
> **Solution:** The impulse response gives Σa^{2k} = 1/(1 − a²), and the PSD of the geometric sequence is the Poisson-kernel form S_y(f) = 1/(1 + a² − 2a cos 2πf), obtained by summing the geometric series Σ_{k=0}^∞ a^{2k}e^{−j2πfk}. Setting |H|² = 1/2 with |H|² = 1/(1 + a² − 2a cos 2πf) gives 1 + a² − 2a cos 2πf = 2, hence cos 2πf₃ = (a² − 1)/(2a). For a = 0.5 this is (0.25 − 1)/1 = −0.75, and arccos(−0.75) = 2.41886 rad, so f₃ = 2.41886/(2π) = 0.38500 cycles per sample. The symmetry cos 2πf₃ = cos(1 − f₃) gives a second solution at f = 0.6150.
> **Key point:** For h = a^ku[k]: σ_y² = 1/(1−a²), S_y(f) = 1/(1+a²−2a cos 2πf), cos 2πf₃ = (a²−1)/(2a); for a = 0.5, f₃ = 0.385 cycles/sample.

### Q141. Give the general formula for the output variance of an nth-order recursive filter driven by white noise, and explain the design implication.

> **Type:** Theory
> **Answer:** For y[k] = −Σ_{i=1}^{n}aᵢy[k−i] + x[k] with all poles strictly inside the unit circle, σ_y² = (1/(2π))∫_{−π}^{π}dω/|1 + Σaᵢe^{−jωi}|², which is finite. It diverges as any pole approaches the unit circle.
> **Solution:** The integral is the mean-square response to unit white noise, obtained from σ_y² = ∫|H(f)|²df with S_x = 1. The integrand has poles in ω wherever the denominator vanishes, and stability requires all roots of 1 + Σaᵢz^{−i} to lie inside the unit circle. As a pole approaches the unit circle the denominator gets small at one frequency and the integral blows up. The design implication is that noise gain is governed by how close the poles sit to the unit circle, so a marginally stable filter is a noise disaster even if it is nominally "stable".
> **Key point:** σ_y² = (1/2π)∫dω/|1 + Σaᵢe^{−jωi}|², finite only with all poles strictly inside the unit circle, and it diverges as a pole approaches it.

### Q142. A first-order high-pass filter H(f) = j2πfRC/(1 + j2πfRC) is driven by white noise of PSD S₀. Express the output PSD in terms of the input and find the total output power.

> **Type:** Numerical
> **Answer:** S_y(f) = S₀(2πfRC)²/(1 + (2πfRC)²). The total output power is **infinite**, because |H(f)|² → 1 as f → ∞ and ideal white noise has infinite total power. The finite statement is the complementary-pair identity |H_hp|² + |H_lp|² = 1, valid at every frequency.
> **Solution:** Taking |H|² = (2πfRC)²/(1 + (2πfRC)²) and multiplying by S₀ gives the output PSD. Integrating, ∫S₀u²/(1+u²)df with u = 2πfRC becomes S₀∫_{−∞}^{∞}(u²/(1+u²))du/(2πRC), and since u²/(1+u²) → 1 the integrand does not decay, so the integral diverges. The physically meaningful statement is the pointwise complement |H_hp(f)|² + |H_lp(f)|² = 1, which says each of an HP/LP pair passes half the input power **at every frequency**; a finite total for the high-pass only exists when the input PSD itself decays.
> **Key point:** High-pass noise power from ideal white noise diverges (|H|²→1); the valid statement is the pointwise complement |H_hp|² + |H_lp|² = 1.

### Q143. Establish that for a real wide-sense stationary process the autocorrelation satisfies R(τ) = R*(−τ) and R(0) = E[X²], and state the consequence for the PSD.

> **Type:** Theory
> **Answer:** For a real WSS process R(τ) = E[X(t)X(t+τ)] is real, so R(τ) = R*(τ) and by the symmetry of the product R(τ) = R(−τ): it is real and **even**. Also R(0) = E[X²(t)] = m² + σ², the total mean-square value. The consequence is that S(f) = ∫R(τ)e^{−j2πfτ}dτ is real and even, and S(0) = R(0) = the DC power including the mean.
> **Solution:** The evenness follows because R(−τ) = E[X(t)X(t−τ)] = E[X(t+τ)X(t)] = R(τ) by commutativity of multiplication and WSS invariance under time shift. For complex processes one instead gets R(τ) = R*(−τ), the Hermitian symmetry that makes S(f) real but not necessarily even. The second identity is immediate from substituting τ = 0, and it is why the "power at DC" includes a squared mean term.
> **Key point:** Real WSS ⟹ R(τ) real and even, R(0) = m² + σ²; complex WSS ⟹ R(τ) = R*(−τ) and S(f) real but not even.

### Q144. For an LTI system, derive the output mean-square value in the time domain starting from y(t) = ∫h(u)x(t−u)du, showing the full double integral.

> **Type:** Theory
> **Answer:** E[y²(t)] = ∬h(u)h(v)R_x(u − v)du dv = ∫∫∫h(u)h(v)S_x(f)e^{j2πf(u−v)}du dv df = ∫S_x(f)|H(f)|²df.
> **Solution:** Substituting the convolution twice gives E[y(t)y(t)] = ∫∫h(u)h(v)E[x(t−u)x(t−v)]du dv, and WSS turns the last factor into R_x(u − v) since the time separation is (t−u) − (t−v) = v − u and R_x is even. Expanding R_x as its Fourier transform and interchanging the integrals makes the u and v integrals independent, each producing H(f) or H*(f), so the double integral collapses to |H(f)|². Every step relies on WSS.
> **Key point:** E[y²] = ∬h(u)h(v)R_x(u−v)dudv, and writing R_x as an inverse Fourier transform collapses it to ∫S_x|H|²df.

### Q145. A system's output variance is to be reduced. Compare the effect of (a) halving the bandwidth and (b) doubling the input white-noise PSD.

> **Type:** Comparison
> **Answer:** Halving the bandwidth halves the output variance (output power ∝ bandwidth), while doubling the input PSD doubles it. The two are exactly proportional and opposite in effect: halving B is equivalent to doubling S₀.
> **Solution:** For an ideal bandpass, σ_y² = 2B·G²·S₀, which is linear in B and linear in S₀. This proportionality is what makes the classic receiver trade-off: sensitivity improves by narrowing B (less noise admitted) but degrades by the wider signal bandwidth required, and no filter can beat it because the noise and the signal occupy the same spectrum. The proportionality also means a 3-dB bandwidth reduction buys exactly 3 dB of noise reduction, a rule of thumb valid for any band-limited filter with a flat passband.
> **Key point:** σ_y² = 2B·G²·S₀ is linear in both bandwidth and input PSD: halving B ≡ doubling S₀, and each 3-dB of bandwidth reduction is 3 dB of noise reduction.

### Q146. An amplifier with voltage gain 100 and input-referred noise of 2 nV/√Hz is connected to a source with 10 kHz bandwidth. Compute the total input- and output-referred noise.

> **Type:** Numerical
> **Answer:** Input-referred total noise = 2 nV/√Hz × √(10⁴ Hz) = 2 × 10⁻⁹ × 100 = 2 × 10⁻⁷ V = 200 nV rms. Output-referred = 100 × 200 nV = 2 × 10⁻⁵ V = 20 µV rms.
> **Solution:** Noise voltage over a bandwidth B is the density times √B, because independent spectral increments add in power: √(10⁴) = 100 √Hz, so 2 nV/√Hz × 100 √Hz = 200 nV rms. For a real two-sided spectrum the √B uses the total two-sided bandwidth, which is what the "nV/√Hz" convention of a one-sided density assumes after the usual factor of √2 bookkeeping. The amplifier then scales this by the voltage gain 100 to give 2 × 10⁻⁵ V = 20 µV at the output. The √B scaling is the whole reason a wideband amplifier is so much noisier than a narrowband one for the same input signal.
> **Key point:** Total noise = density × √B: 2 nV/√Hz over 10 kHz gives 200 nV rms input-referred, 20 µV after a gain of 100.

## Section 7. Discrete random processes: PMFs, joint and k-th order distributions (Q147–Q161)

### Q147. Define a random process and state how a discrete-time random process differs from a discrete random variable.

> **Type:** Theory
> **Answer:** A random process {X(t), t ∈ T} is an indexed family of random variables. A **discrete-time** process has t ∈ {…, −1, 0, 1, …} or ℕ, so it is an infinite sequence of random variables; a discrete random variable is a single one of them, and the term "discrete" in each case refers to the *time* index, not to the values X(t) may take.
> **Solution:** The process is the natural object for signals, since a physical waveform is a time-indexed family of random quantities. The distinction matters because a discrete-time process can be continuous-valued (a sampled analogue waveform) while a discrete random variable is just one number. The analysis then asks how the individual X(t) are jointly distributed across time — which is exactly what stationarity and the correlation function describe.
> **Key point:** A random process is an indexed family {X(t)}; "discrete-time" refers to the index set, and each X(t) may still be continuous-valued.

### Q148. A discrete-time process has the PMF P(X[n] = k) = (1−p)p^k for k = 0, 1, 2, …. Identify the process, its mean, and its correlation function if the samples are independent.

> **Type:** Numerical
> **Answer:** Each X[n] is Geometric(p) on {0,1,2,…} with mean (1−p)/p and variance (1−p)/p². With independent samples, R_X[m] = μ² for m ≠ 0 and σ² + μ² for m = 0, i.e. R_X[m] = σ²δ[m] + μ².
> **Solution:** The mass (1−p)p^k is the geometric law on the support starting at zero, with mean (1−p)/p. Independence makes the process WSS: the mean is constant at μ and, for m ≠ 0, E[X[n]X[n−m]] = E[X[n]]E[X[n−m]] = μ². At m = 0 the product is X[n]², giving E[X²] = σ² + μ². So the autocorrelation is a constant μ² plus an impulse of weight σ² — the autocorrelation of any independent-sample WSS process. The μ² floor is the DC power of the mean and is present in the PSD as a line at f = 0.
> **Key point:** Independent samples give R_X[m] = σ²δ[m] + μ²; the μ² floor is the DC power of the mean, showing up as a spectral line at f = 0.

### Q149. State the definition of the k-th order joint distribution of a discrete random process, and give the k-th order PMF for k = 2.

> **Type:** Theory
> **Answer:** The k-th order joint distribution is F_{X(t₁),…,X(t_k)}(x₁,…,x_k) = P(X(t₁) ≤ x₁, …, X(t_k) ≤ x_k). For discrete time and discrete values, the corresponding PMF is p_{X^(k)}(x₁,…,x_k) = P(X[n₁] = x₁, …, X[n_k] = x_k), with n₁ < n₂ < … < n_k. For k = 2 it is the joint PMF p(x₁,x₂) over a pair of time indices.
> **Solution:** The full hierarchy {k-th order distributions, k = 1,2,…} determines the whole process, because consistency conditions link consecutive orders and the marginalisation F_k(x₁,…,x_{k−1}) = Σ_{x_k}F_{k+1}(…,x_k) tie them together. The k = 2 case is the joint distribution of two samples, and knowing only the k = 1 marginals throws away all information about how the process evolves — which is the practical reason higher-order statistics matter for non-Gaussian sources and for nonlinear signal processing.
> **Key point:** The k-th order distribution is the joint law of k samples at distinct time indices; the whole hierarchy of orders determines the process, and k = 1 marginals discard all temporal structure.

### Q150. A process is defined by X[n] = Wⁿ where W ~ U(0,1). Is it wide-sense stationary? Justify.

> **Type:** Conceptual
> **Answer:** No. E[X[n]] = E[Wⁿ] = 1/(n+1), which depends on n, so the mean is not constant and the process fails wide-sense stationarity.
> **Solution:** WSS requires a time-independent mean. Here the n-th sample has mean 1/(n+1), decreasing with n, because taking high powers of a uniform variable concentrates it near zero. So the process is not mean-stationary and hence not WSS, regardless of what its autocorrelation looks like. The example is a useful reminder that stationarity is a property of the *statistics* over time, not of the shape of individual samples, and that checking the mean is the fastest necessary test.
> **Key point:** WSS needs a constant mean; here E[X[n]] = 1/(n+1) varies with n, so the process is not WSS. Check the mean first.

### Q151. Consider X[n] = ξ where ξ ~ N(0, 1) is a single random constant. Is the process white, WSS, and ergodic in the mean? Give its autocorrelation and PSD.

> **Type:** Conceptual
> **Answer:** It is WSS but **not** white: R_X[m] = 1 for every m (a constant, not an impulse), so S_X(f) = δ(f) and all the power is at DC. It is **not** mean-ergodic in any of the usual senses, and **not** correlation-ergodic.
> **Solution:** Since the same ξ appears in every sample, E[X[n]] = 0 and E[X[n]X[n−m]] = E[ξ²] = 1 for every m, so the autocorrelation is the constant 1 — flat in time, which is exactly WSS. Its Fourier transform is a Dirac impulse, S_X(f) = δ(f), so all the power sits at DC. The time average is (1/N)Σ_{n=1}^N X[n] = ξ for every N, a constant random variable: it equals the target value 0 with probability 0, since a continuous variable takes a specific value with probability zero, and P(|ξ| > ε) is the same positive number for all N rather than tending to 0. So convergence in probability fails, and mean-square ergodicity fails as well because E[(ξ − 0)²] = 1 for all N. Correlation ergodicity fails for the same reason: the time correlation is 1 at every lag, while the ensemble value for m ≠ 0 is also 1, so that part agrees — but the estimator never converges in the required sense because the whole realisation is one sample of a non-ergodic process. Contrast with Q152, where iid samples average down as 1/N.
> **Key point:** X[n] = ξ is WSS with R_X[m] = 1 and S_X(f) = δ(f) — DC power, not white noise. Its time average is the constant ξ, so it is not ergodic in probability, in mean square, or in correlation.

### Q152. Define an iid (independent and identically distributed) discrete-time process and state three consequences of iid-ness.

> **Type:** Theory
> **Answer:** An iid process has each X[n] with the same marginal law and all distinct samples mutually independent. Consequences: (i) the mean is constant, so mean-stationarity holds automatically; (ii) the autocorrelation is R_X[m] = μ² + σ²δ[m], i.e. white; (iii) the PSD is S_X(f) = σ² + μ²δ(f), a flat continuum plus a DC line.
> **Solution:** Independence gives E[X[n]X[n−m]] = E[X[n]]E[X[n−m]] = μ² for m ≠ 0, and at m = 0 it is E[X²] = σ² + μ², so the autocorrelation is flat with a spike — the definition of white for a discrete-time process. Fourier transforming, the constant μ² gives a Dirac at DC and the impulse σ²δ[m] transforms to the constant σ². Identical distribution gives the constant mean, so any iid process is WSS without further assumption. This is the default model for thermal noise samples and for the input of many DSP blocks.
> **Key point:** An iid discrete process is automatically WSS and white: R_X[m] = μ² + σ²δ[m], S_X(f) = σ² + μ²δ(f).

### Q153. Give the PMF and correlation of a process where X[n] = Z + W[n], with Z and W[n] independent, Z ~ N(0, τ²) and W[n] iid N(0, σ²). Is it ergodic?

> **Type:** Numerical
> **Answer:** E[X[n]] = 0, R_X[m] = τ² + σ²δ[m], S_X(f) = τ²δ(f) + σ². It is **not** correlation-ergodic: the time average is Z + mean(W) = Z, so the time correlation is τ² + 0 = τ² rather than the ensemble value τ² + σ².
> **Solution:** Splitting the product, E[(Z + W[n])(Z + W[n−m])] = E[Z²] + E[Z]E[W] + E[W[n]]E[W[n−m]] + E[W[n]W[n−m]], where the Z² term is τ² for every m, the cross terms vanish because E[Z] = 0, and the white part contributes E[W[n]W[n−m]] = σ²δ[m]. So R_X[m] = τ² + σ²δ[m], and the PSD is the constant σ² plus a DC line of weight τ² (the discrete-time line train of Q153). The time average of N samples is (1/N)ΣW[n] + Z, and the first term → 0 by the law of large numbers, so the empirical autocorrelation converges to τ², missing the σ² white component entirely. That gap is the non-ergodicity: a per-realisation DC offset that a single long run cannot average away.
> **Key point:** X[n] = Z + W[n] is WSS with R_X[m] = τ² + σ²δ[m] but is not correlation-ergodic: the time correlation gives τ², not τ² + σ².

### Q154. Show that a discrete-time WSS process with mean μ has PSD S_X(f) = μ²Σ_m δ(f − m) + S_{X−μ}(f), and interpret the two terms.

> **Type:** Theory
> **Answer:** R_X[m] = μ² + R_{X−μ}[m], and the discrete-time PSD of the constant sequence μ² is the unit-period impulse train μ²Σ_{k=−∞}^{∞}δ(f − k), so S_X(f) = μ²Σ_k δ(f − k) + S_{X−μ}(f). Over the fundamental interval −1/2 ≤ f < 1/2 the first term is simply μ²δ(f) modulated by the periodic extension, a DC line of total weight μ²; the second term is the PSD of the zero-mean fluctuation.
> **Solution:** Decompose R_X[m] = E[(μ + Z[n])(μ + Z[n−m])] with Z = X − μ: expanding gives μ² + μE[Z] + μE[Z] + E[Z[n]Z[n−m]] = μ² + R_{X−μ}[m], since E[Z] = 0. Under the convention S(f) = Σ_m R[m]e^{−j2πfm}, a constant sequence transforms to μ²Σ_m e^{−j2πfm}, which is the periodic Dirac train μ²Σ_k δ(f − k) — not a single δ, because the discrete-time transform of a non-summable constant is a line spectrum, unlike the continuous-time case where a constant τ-transform gives 2πm²δ(f). Within the analysis band the impulse appears at f = 0. The engineering reading is unchanged: a nonzero mean is pure DC power that no filter with H(0) = 0 can pass, which is why mean removal precedes spectral estimation.
> **Key point:** A discrete-time mean μ contributes a DC line of weight μ², so S_X(f) = μ²Σ_k δ(f−k) + S_{X−μ}(f); the 2πδ form belongs to the continuous-time transform, not this one.

### Q155. Give the k-th order joint PMF for a process that emits, at each time n, a 1 with probability p and 0 with probability 1−p independently. State the process's entropy rate.

> **Type:** Numerical
> **Answer:** p_{X^(k)}(x₁,…,x_k) = ∏_{i=1}^{k}p^{x_i}(1−p)^{1−x_i} = p^{Σx_i}(1−p)^{k−Σx_i}. The entropy rate is H(X[n]) = −p log p − (1−p) log(1−p) bits per sample, its maximum at p = 1/2 where it equals 1 bit.
> **Solution:** Independence across the k sampled times factorises the joint PMF into a product of marginals, which is the definition of mutual independence of those k samples. The entropy rate of an iid process equals the single-symbol entropy, since −log P(X₁…X_k) = Σ log P(X_i) and the per-sample limit is the marginal entropy. For p = 0.5 each of the 2^k patterns is equally likely, giving exactly k bits per k samples. This is the capacity-achieving binary source, the reason noiseless coding of fair binary data cannot beat 1 bit per symbol.
> **Key point:** An iid binary source has k-th order PMF = p^{Σx}(1−p)^{k−Σx}, and entropy rate −p log p − (1−p) log(1−p), max 1 bit at p = 1/2.

### Q156. Define strict-sense stationarity and state its two relationships to wide-sense stationarity.

> **Type:** Theory
> **Answer:** SSS means the k-th order distribution is invariant under a shift of all time indices by any τ: F_{X^(k)}(x₁,…,x_k; t₁+τ,…,t_k+τ) = F_{X^(k)}(x₁,…,x_k; t₁,…,t_k) for all k. The relationships: (i) SSS ⟹ WSS, and (ii) WSS ⟹ SSS **only** if the process is Gaussian (a WSS Gaussian process is strictly stationary, and is called a wide-sense stationary Gaussian process).
> **Solution:** SSS is the full distributional requirement, so the k = 1 case gives a constant mean and the k = 2 case gives a lag-only autocorrelation, which is exactly WSS. The converse fails because WSS constrains only the first two moments, and many non-Gaussian processes have the same mean and autocorrelation while differing in higher-order structure — the classic example is a process that is symmetric about its mean but has a triangular rather than Gaussian shape. For Gaussian processes the second moment determines the whole law, so WSS collapses to SSS.
> **Key point:** SSS ⟹ WSS always, and WSS ⟹ SSS for Gaussian processes only; for general processes the higher-order structure is free.

### Q157. Consider the process X[n] = A cos(2πf₀n + Θ) + W[n] with A, f₀ fixed, Θ ~ U(0, 2π) and W[n] iid N(0, σ²). State whether it is WSS and whether it is Gaussian.

> **Type:** Theory
> **Answer:** It is WSS: E[X[n]] = 0 and R_X[m] = (A²/2)cos(2πf₀m) + σ²δ[m]. It is **not** Gaussian, because a deterministic-amplitude sinusoid with random phase is a continuous (arcsine-distributed) mixture, and adding noise makes it a continuous mixture of translates of a Gaussian — a Gaussian mixture, not a single Gaussian.
> **Solution:** E[cos(2πf₀n + Θ)] = 0 by integrating over a full period of the uniform phase. For m, the product of two cosines expands into (1/2)[cos(phase difference) + cos(phase sum)], and the second term averages to zero over Θ, leaving (A²/2)cos(2πf₀m). The white noise contributes σ²δ[m]. Stationarity holds because the uniform phase makes the marginal law shift-invariant. The lack of Gaussianity is immediate from the fact that the phase is continuous: a Gaussian shifted by every phase and then averaged gives a non-Gaussian mixture.
> **Key point:** X[n] = A cos(2πf₀n+Θ) + W[n] is WSS with R_X[m] = (A²/2)cos 2πf₀m + σ²δ[m], but it is a Gaussian *mixture*, not Gaussian — so it is WSS without being SSS.

### Q158. State the definition of a Gaussian random process and give the reason Gaussian processes are so widely used in linear systems analysis.

> **Type:** Theory
> **Answer:** A Gaussian process has a multivariate normal k-th order distribution for every k. They are used because (i) WSS completely determines the process for them, so first and second moments suffice, and (ii) linear filtering and closure results hold exactly, making output statistics computable in closed form.
> **Solution:** Since a multivariate normal is fully specified by its mean vector and covariance matrix, the first two moments fix the whole law, so WSS is enough to pin down a Gaussian process and its filtered versions. Additionally, a linear combination of Gaussian processes is Gaussian, which is what allows output mean, variance and PSD to be computed by linear algebra rather than by solving integral equations. The cost of the assumption is that it is often false in practice for nonlinear devices, where the output must be handled by describing functions or by measurement.
> **Key point:** A Gaussian process's whole law is fixed by its mean and covariance, so WSS ⟹ SSS for it, and linear filtering stays exactly solvable in closed form.

### Q159. A process X[n] satisfies R_X[m] = 2e^{−|m|}. Verify it is a valid autocorrelation, and identify the corresponding spectral shape.

> **Type:** Numerical
> **Answer:** It is valid: it is even, R_X[0] = 2 > 0, and its Fourier transform is the Lorentzian S_X(f) = 2a/(a² + (2πf)²) with a = 1, i.e. S_X(f) = 2/(1 + 4π²f²), which is everywhere positive. So the process is WSS with a Lorentzian spectrum, mean 0.
> **Solution:** Any non-negative-definite even function of lag is a valid autocorrelation, and the definitive test is that its Fourier transform is non-negative everywhere. Computing: ∫_{−∞}^{∞}e^{−|m|}e^{−j2πfm}dm = 2∫₀^∞e^{−m}cos(2πfm)dm = 2·(1/(1 + 4π²f²)), using ∫₀^∞e^{−m}cos(bm)dm = 1/(1+b²). The result 2/(1 + 4π²f²) is strictly positive, confirming validity. Lorentzian spectra of this form arise from Ornstein–Uhlenbeck-type processes and are the standard model for thermal noise in resistive networks.
> **Key point:** R_X[m] = 2e^{−|m|} has S_X(f) = 2/(1 + 4π²f²), a Lorentzian; a valid autocorrelation is exactly one whose FT is non-negative everywhere.

### Q160. Two discrete-time processes X and Y have cross-correlation R_XY[m] that is zero for all m. What can you conclude, and what can you not conclude?

> **Type:** Conceptual
> **Answer:** You can conclude the processes are uncorrelated at all lags, hence their cross-spectral density S_XY(f) ≡ 0. You cannot conclude independence — uncorrelatedness is only a second-moment statement. If the processes are jointly Gaussian, then zero cross-correlation at all lags does imply independence of the two entire sequences.
> **Solution:** Zero cross-correlation is a statement about E[X[n]Y[n−m]] only, and it is entirely compatible with a strong nonlinear relationship such as Y[n] = X[n]². What it does guarantee is that the coherent part of the transfer between them is absent, so no linear system can exploit one to predict the other in the mean-square sense, and the cross-spectrum vanishes. The Gaussian exception holds because a jointly Gaussian pair is determined by its covariance, and zero covariance between the two vectors then forces the block covariance matrix to be diagonal.
> **Key point:** Zero cross-correlation ⟹ S_XY(f) = 0 and no linear predictability, but not independence — except for jointly Gaussian processes, where it does imply independence.

### Q161. A discrete-time binary process takes values ±1 with equal probability and independently at each sample. Find its PSD and the autocorrelation, and identify the process by name.

> **Type:** Numerical
> **Answer:** E[X[n]] = 0, R_X[m] = δ[m], S_X(f) = 1 for all f. It is **discrete white noise** of unit variance, the reference model for an iid unit-variance input. For general amplitude ±A equiprobable, R_X[m] = A²δ[m] and S_X(f) = A².
> **Solution:** E[X[n]] = (1)(1/2) + (−1)(1/2) = 0. For m ≠ 0, E[X[n]X[n−m]] = E[X[n]]E[X[n−m]] = 0 by independence. For m = 0, E[X²] = 1. So R_X[m] = δ[m], and the flat unit PSD is its Fourier transform. This is the reference process against which filter noise gains are quoted: a filter's output variance is Σh² precisely because the input PSD is 1.
> **Key point:** iid equiprobable ±A binary noise: R_X[m] = A²δ[m], S_X(f) = A² — a flat spectrum, the reference for all noise-gain calculations.

---

## Section 8. Stationarity, ergodicity and correlation functions (Q162–Q185)

### Q162. Define wide-sense stationarity with its two conditions, and state the minimum information about the autocorrelation that WSS guarantees.

> **Type:** Theory
> **Answer:** WSS requires (i) constant mean, E[X(t)] = m for all t, and (ii) an autocorrelation depending only on the time difference, R_X(t₁,t₂) = R_X(t₂ − t₁) = R(τ). It guarantees nothing about the order of R beyond evenness, R(τ) = R(−τ) for real processes, and that R(0) = E[X²] = m² + σ² ≥ 0.
> **Solution:** WSS is a second-moment condition only, so it constrains the first two moments and leaves the higher-order statistics completely free. The lag-only dependence is the essence of translation invariance at the level of means. The evenness follows from the commutativity of the product, R(τ) = E[X(t)X(t+τ)] = E[X(t+τ)X(t)] = R(−τ). Nothing forces R(τ) to be a decaying function, to be integrable, or to be positive — the constant function R(τ) = 1 is a perfectly valid autocorrelation, as Q150 showed.
> **Key point:** WSS = constant mean + autocorrelation depending only on lag. For real processes R is even and R(0) = m² + σ², but higher-order structure is entirely unconstrained.

### Q163. State the covariance function of a WSS process and prove that it is a valid covariance in the sense of the positive-semi-definite requirement.

> **Type:** Theory
> **Answer:** C_X(τ) = R_X(τ) − m², so C_X(0) = σ² and C_X(τ) → 0 as |τ| → ∞ for a "mixing" process. Validity: for any weights a_i and times t_i, Σᵢⱼ aᵢaⱼC_X(t_i − t_j) = Var(ΣᵢaᵢX(t_i)) ≥ 0.
> **Solution:** Expanding the variance, Var(ΣaᵢX(tᵢ)) = E[(ΣaᵢX(tᵢ))²] − m²(Σaᵢ)² = Σᵢⱼaᵢaⱼ(E[X(tᵢ)X(t_j)] − m²) = ΣᵢⱼaᵢaⱼC_X(tᵢ − t_j), using bilinearity of expectation and the WSS substitution. The result is a squared real quantity, so it cannot be negative — exactly the positive-semi-definiteness condition on the covariance function. This is the property that its Fourier transform, the PSD, must inherit as a non-negative function.
> **Key point:** C_X(τ) = R_X(τ) − m², and ΣᵢⱼaᵢaⱼC(tᵢ−t_j) = Var(ΣaᵢX(tᵢ)) ≥ 0, which is why S_X(f) ≥ 0.

### Q164. State the conditions a function S_X(f) must satisfy to be a valid power spectral density, and show that white noise has a flat spectrum.

> **Type:** Theory
> **Answer:** A valid S_X(f) must be (i) real and non-negative, (ii) even for a real process, and (iii) integrable over the whole frequency axis, with ∫S_X(f)df = R_X(0) = E[X²] equal to the process power. A DC line of weight m² appears whenever the mean m is nonzero. White noise has R_X(τ) = σ²δ(τ), whose Fourier transform is the constant S_X(f) = σ².
> **Solution:** Non-negativity is forced by the quadratic form E[|∫X(f)e^{j2πft}df|²] ≥ 0, which integrates to ∫S_X(f)|W(f)|²df for any weight W and is impossible if S_X took a negative value. Evenness follows because R_X(τ) is real and even, so its transform is too. Integrability is what ties the spectrum to a finite process power and is the statement R_X(0) = ∫S_X(f)df. Non-negativity also rules out R_X(∞) = 0 as a universal requirement: a process with nonzero mean has R_X(τ) → m², which is a Dirac impulse at f = 0, a legitimate part of a non-negative spectrum. For white noise, transforming R_X(τ) = σ²δ(τ) under S(f) = ∫R(τ)e^{−j2πfτ}dτ gives the constant σ², the defining flat spectrum.
> **Key point:** A valid PSD is real, non-negative and even, with ∫S df = R(0) = E[X²]. White noise R = σ²δ ⟺ S(f) = σ², a constant; a nonzero mean shows up as a DC line, not a violation.

### Q165. Define ergodicity in the mean and correlation-ergodicity, and state the implication chain between them.

> **Type:** Theory
> **Answer:** Mean ergodicity: the time average (1/2T)∫_{−T}^T X(t)dt converges in mean square to the ensemble mean m. Correlation ergodicity: the time average (1/2T)∫X(t)X(t+τ)dt converges in mean square to R(τ). Correlation ergodicity ⟹ mean ergodicity, and both require WSS; ergodicity is strictly stronger than stationarity.
> **Solution:** The definitions differ only in the integrand, so if the correlation averages converge then averaging both factors at τ = 0 gives the mean average, and the Cauchy–Schwarz inequality carries the τ = 0 case to the general τ case. That is the direction correlation ⟹ mean. Stationarity only says the statistics are time-invariant in an ensemble sense; ergodicity says a single realisation can be used to estimate them, which is the actual bridge from theory to measurement. Ergodicity is a property of a process, not of a signal, and it can fail spectacularly for non-Gaussian or strongly correlated processes.
> **Key point:** Correlation ergodicity ⟹ mean ergodicity ⟹ WSS. Ergodic means a single long realisation can estimate the statistics, which stationarity alone does not give.

### Q166. Derive the variance of the sample mean of a WSS process and give the conditions under which it converges to the ensemble mean.

> **Type:** Theory
> **Answer:** Var(X̄_N) = (1/N²)ΣᵢΣⱼR(i−j) = (σ²/N) + (1/N)Σ_{k≠0}(1 − |k|/N)R(k), so Var → 0 as N → ∞ whenever the autocorrelation is absolutely summable, i.e. Σ_k|R(k)| < ∞. The N-independent samples give the ideal Var = σ²/N, but stationarity alone is not enough.
> **Solution:** Expanding Var((1/N)ΣX[n]) gives (1/N²)ΣᵢΣⱼR(i−j); counting the N diagonal terms and grouping the remainder by lag k, of which there are N − |k|, yields the stated expression. The first term is the ideal σ²/N, and the rest vanish if Σ_k|R(k)| < ∞ because the factor (1 − |k|/N) is bounded by 1. Without that summability the variance can stay bounded away from zero, so mean-ergodicity fails. The practical reading is that a process with a slowly decaying correlation has an effective sample size far below N, which is why averaging alone cannot rescue a strongly correlated process.
> **Key point:** Var(X̄_N) = σ²/N + (1/N)Σ_{k≠0}(1−|k|/N)R(k) → 0 only when Σ_k|R(k)| < ∞; stationarity by itself does not guarantee ergodicity.

### Q167. Show that the deterministic periodic process X[n] = A(−1)ⁿ is WSS, and that its time averages do converge to the ensemble values even though it is periodic.

> **Type:** Conceptual
> **Answer:** E[X[n]] = 0 and R_X[m] = A²(−1)^m, both independent of n, so the process is WSS. Its sample mean is A/N for odd N and 0 for even N, which tends to 0 = E[X], and the correlation average also converges to R_X[m]. It is mean- and correlation-ergodic despite being periodic.
> **Solution:** WSS in the ensemble sense requires only that the statistics do not depend on the time origin, and for a deterministic periodic signal those statistics are fixed constants, so stationarity holds trivially. The empirical mean of N samples is the partial sum A(1 − 1 + 1 − 1 + ⋯), which is A for odd N and 0 for even N; divided by N both cases tend to 0, so the sample mean converges in mean square to the ensemble mean because its variance is A²/N → 0. The correlation average converges too, since X[n]X[n+m] is periodic with period 2 and its partial sums grow only linearly. The contrast with the constant random process of an earlier question is the point: periodicity does not prevent ergodicity, but a random constant that is constant in time does.
> **Key point:** A deterministic periodic process is WSS and both mean- and correlation-ergodic — partial sums grow at most linearly, so dividing by N converges. Periodicity does not block ergodicity; a time-invariant random constant does.

### Q168. Let X(t) be a WSS process with R_X(τ) = 5e^{−|τ|}. Compute the PSD and the process power.

> **Type:** Numerical
> **Answer:** S_X(f) = 10/(1 + 4π²f²). Total power = R_X(0) = 5.
> **Solution:** Fourier transforming, ∫_{−∞}^{∞}e^{−|τ|}e^{−j2πfτ}dτ = 2∫₀^∞e^{−τ}cos(2πfτ)dτ = 2·1/(1 + 4π²f²), so multiplying by 5 gives S_X(f) = 10/(1 + 4π²f²). Checking the total power, ∫S_X(f)df = 10∫df/(1+4π²f²) = 10·(1/2π)∫du/(1+u²) = (10/2π)(π) = 5, agreeing with R_X(0) = 5 ✓. The spectrum is a Lorentzian, the standard shape for thermal (Johnson–Nyquist) noise in a resistive network, where the exponential decay in time comes from an RC time constant.
> **Key point:** R_X(τ) = 5e^{−|τ|} gives the Lorentzian S_X(f) = 10/(1 + 4π²f²), and total power = R(0) = 5, verified by integrating the Lorentzian.

### Q169. A zero-mean WSS process has autocorrelation R_X(τ) = A² cos(2πf₀τ). Interpret this process, and give its spectrum and its average power.

> **Type:** Numerical
> **Answer:** It is a sinusoidal random process — equivalently a random-phase sinusoid of amplitude A√2 at frequency f₀, whose autocorrelation happens to be A²cos(2πf₀τ). S_X(f) = (A²/2)[δ(f − f₀) + δ(f + f₀)], and the average power is R_X(0) = A².
> **Solution:** A random-phase sinusoid A cos(2πf₀t + Θ) with Θ uniform has autocorrelation (A²/2)cos(2πf₀τ), since averaging the product of two cosines over a full period of Θ kills the fast term and leaves half the amplitude squared. So the given R corresponds to amplitude A√2. A cosine in τ Fourier transforms into a pair of Dirac impulses, each of weight A²/2, so all the power sits in the two lines at ±f₀. The total power is the sum of the line weights, A²/2 + A²/2 = A², which matches R_X(0) = A²cos 0 = A² exactly.
"> **Key point:** R_X(τ) = A²cos 2πf₀τ ⟹ S_X(f) = (A²/2)[δ(f−f₀)+δ(f+f₀)]; total power = sum of line weights = R(0) = A². The DC line appears only if the process has a nonzero mean.



---
### Q170. Show that for a WSS process with a continuous spectrum, the average power equals the area under the PSD, and state the two distinct average powers.

> **Type:** Theory
> **Answer:** The average power is the limit of E[|X(t)|²] as t → ∞, equal to ∫_{−∞}^{∞}S_X(f)df by the Wiener–Khinchin theorem evaluated at τ = 0. Two averages must be distinguished: the **time average** (1/2T)∫_{−T}^T|X(t)|²dt and the **ensemble average** E[|X(t)|²]; they are equal for ergodic processes and unequal in general.
> **Solution:** Setting τ = 0 in the inverse transform R(τ) = ∫S(f)e^{j2πfτ}df gives R(0) = ∫S(f)df, and R(0) = E[X²] is the mean-square value. The time average is a single-realisation quantity and converges to R(0) only under ergodicity, so the two can differ by an arbitrary amount — for X(t) = Z with Z a random constant, the time average is Z² while the ensemble average is E[Z²]. The distinction is exactly what time-average spectrograms are trying to estimate, and why a non-ergodic process gives a spectrum that depends on the realisation.
> **Key point:** Average power = ∫S_X(f)df = R(0) = E[X²]; time and ensemble averages coincide only for ergodic processes.

### Q171. Give the mean and variance of the time average of a WSS process, and use them to design a sample size for a target accuracy.

> **Type:** Numerical
> **Answer:** For the N-sample average, Var(X̄) = (1/N²)[Nσ² + Σ_{k≠0}(N−|k|)R(k)]. For independent samples this is σ²/N, so reaching a relative standard deviation of 0.01 needs N ≥ 10⁴; for a first-order exponentially correlated process with correlation length τ_c it becomes ≈ (2τ_c/Δt)·σ²/N.
> **Solution:** Writing R(k) = σ²ρ(k) with |ρ(k)| ≤ 1 gives the bound Var(X̄) ≤ σ²(N + 2Σ_{k=1}^{N−1}(N−k)|ρ(k)|)/N². For independent samples this collapses to σ²/N, and demanding σ/√N ≤ 0.01σ gives N ≥ 10⁴. For a correlated process the effective sample size is reduced by the ratio of the correlation time to the sampling interval, which is why oversampling a correlated signal buys little. The same formula with the fourth moment gives the sample-variance estimator's accuracy.
> **Key point:** Var(X̄) = σ²/N only for independent samples; correlated data needs N ≫ τ_c/Δt, so oversampling a correlated signal buys little.

### Q172. A WSS process has R_X(τ) = σ²e^{−2|τ|}. Find the half-power frequency and the 3-dB bandwidth of the spectrum.

> **Type:** Numerical
> **Answer:** S_X(f) = σ²/(1 + π²f²). The −3 dB point satisfies 1 + π²f₃² = 2, giving f₃ = 1/(π√2) ≈ 0.2251 Hz. The total two-sided −3 dB width is 2f₃ ≈ 0.4502 Hz, while the one-sided half-width is f₃.
> **Solution:** Using ∫_{−∞}^{∞}e^{−a|τ|}e^{−j2πfτ}dτ = 2a/(a² + 4π²f²) with a = 2: the transform is 2(2)/(4 + 4π²f²) = 4/(4 + 4π²f²) = 1/(1 + π²f²). Multiplying by σ² gives S_X(f) = σ²/(1 + π²f²), whose peak value is S_X(0) = σ². The half-power condition S_X(f₃) = σ²/2 reads 1/(1 + π²f₃²) = 1/2, so π²f₃² = 1 and f₃ = 1/(π√2) ≈ 0.22508 Hz. Since the spectrum is a two-sided Lorentzian, the −3 dB bandwidth spans from −f₃ to +f₃, of total width 2f₃ ≈ 0.4502 Hz. The general form R(τ) = σ²e^{−|τ|/τ_c} gives f₃ = 1/(2πτ_c√2), and here τ_c = 0.5 s. Because f₃ is a half-width, the total −3 dB bandwidth of this two-sided Lorentzian is 2f₃, so the convention must always be stated.
> **Key point:** R(τ) = σ²e^{−2|τ|} ⟹ S_X(f) = σ²/(1 + π²f²), f₃ = 1/(π√2) ≈ 0.2251 Hz; for a two-sided spectrum the total −3 dB width is 2f₃ ≈ 0.4502 Hz.

### Q173. State the three properties of the autocorrelation of a WSS real process that constrain its Fourier transform, and show why the PSD cannot be negative.

> **Type:** Theory
> **Answer:** (i) R(τ) is real, (ii) R(τ) is even, (iii) R(0) = E[X²] is finite. Consequently S(f) is real, S(f) is even, and S(f) ≥ 0 for all f. The non-negativity follows from the requirement that R be positive semi-definite, which forces its transform to be non-negative.
> **Solution:** Realness and evenness of R give a real, even transform, so S(f) = ∫R(τ)cos(2πfτ)dτ with no imaginary part. Non-negativity is not automatic from these two properties — an oscillatory R(τ) = cos(ω₀τ) has a real even transform, but that transform is a pair of Dirac impulses, which is non-negative only because deltas are positive. The general proof: for any interval I, ∫_I S(f)df = R(0)⁻¹∫_I∫R(τ)e^{−j2πfτ}dτdf is a quadratic form in R, hence ≥ 0 by the positive-semi-definiteness of a valid autocorrelation. A negative PSD would mean some band carries negative power, which is physically impossible.
> **Key point:** Valid autocorrelation ⟹ S(f) real, even and **non-negative**; non-negativity is a consequence of positive semi-definiteness, not of realness or evenness alone.

### Q174. Give the autocorrelation of a process that is a sum of two independent sinusoids of different frequencies, and count the spectral lines.

> **Type:** Numerical
> **Answer:** For X(t) = A₁cos(2πf₁t + Θ₁) + A₂cos(2πf₂t + Θ₂) with independent uniform phases, R_X(τ) = (A₁²/2)cos(2πf₁τ) + (A₂²/2)cos(2πf₂τ), giving four spectral lines at ±f₁ and ±f₂ with weights A₁²/2 and A₂²/2.
> **Solution:** Expanding the product, terms like cos(2πf₁t + Θ₁)cos(2πf₂t + Θ₂) average to zero over the independent uniform phases because no matching frequency appears. The surviving self-terms each give half the squared amplitude times the cosine of the lag. The total power is R_X(0) = (A₁² + A₂²)/2, which is the sum of the four line weights as required. This is the model behind narrowband noise analysis, where a bandlimited noise process is decomposed into sinusoids with random phases.
> **Key point:** A sum of independent random-phase sinusoids gives one line pair per component; total power = (ΣAᵢ²)/2, and cross terms vanish by phase independence.

### Q175. Does WSS imply that the process is time-reversible? Give the precise statement and the counterexample direction.

> **Type:** Conceptual
> **Answer:** No — WSS does not imply time-reversibility. A process is time-reversible if (X(t₁), …, X(t_n)) has the same joint law as (X(−t₁), …, X(−t_n)). Every WSS **Gaussian** process is time-reversible, since a Gaussian law is fixed by its mean vector and covariance, and covariance is even in lag. The converse fails: a WSS non-Gaussian process can be non-reversible, so a non-zero higher-order time-asymmetric statistic such as the three-time correlation E[X(t)X(t+τ)X(t+2τ)] can distinguish forward from reversed time.
> **Solution:** Time-reversibility is a property of the full joint law under a reflection of the time axis, while WSS constrains only first and second moments. For Gaussian processes both forward and reversed vectors have the same mean and the same covariance matrix (because R is even), so by uniqueness of the multivariate normal the two laws coincide. For non-Gaussian processes the higher-order statistics need not be symmetric, and a non-zero three-time correlation is the simplest witness. Phase-noise processes built from nonlinear oscillators are the practical non-reversible case.
> **Key point:** WSS Gaussian ⟹ time-reversible (mean + even covariance fix the law); WSS alone does not, since higher-order time-asymmetric statistics may survive.

### Q176. Show that a process with a nonzero mean and a periodic autocorrelation has a spectral density containing a DC line, and quantify the line weight.

> **Type:** Theory
> **Answer:** Decompose X(t) = m + Z(t) with Z zero-mean. Then S_X(f) = 2πm²δ(f) + S_Z(f), so the DC line carries total weight m². The continuous part carries R_Z(0) = R_X(0) − m².
> **Solution:** The autocorrelation splits as R_X(τ) = m² + C_Z(τ) using the decomposition in Q153. Fourier transforming, the constant m² becomes 2πm²δ(f) and C_Z(τ) transforms into the continuous PSD of the fluctuation. The line weight is read off as the total power at DC, m², which is why removing the mean is a mandatory preprocessing step before estimating a spectrum: otherwise the DC line dominates the estimate and can swamp a weak nearby tone.
> **Key point:** Nonzero mean ⟹ a DC spectral line of weight m² in S_X(f) = 2πm²δ(f) + S_Z(f); subtract the mean before estimating spectra.

### Q177. A discrete-time process is white with PSD S_X(e^{jω}) = S₀ over −π ≤ ω ≤ π. What is the total power, and what happens as S₀ → 0?

> **Type:** Numerical
> **Answer:** Total power = (1/2π)∫_{−π}^{π}S₀dω = S₀, so σ² = S₀. As S₀ → 0, the power and the variance both vanish, the autocorrelation σ²δ[m] becomes the zero function, and the process converges to the identically-zero process. The *shape* of the spectrum never changes: it stays flat for all S₀.
> **Solution:** With the discrete-time PSD convention S_X(e^{jω}) = Σ_m R_X[m]e^{−jωm}, Parseval gives R_X[0] = (1/2π)∫_{−π}^{π}S_X dω = S₀. The limiting behaviour is worth noting because whiteness is defined by the *shape* of the spectrum, not its level: any flat spectrum is white, and scaling S₀ moves the process along a continuum without changing its correlation structure beyond a constant factor. This is what makes the noise-gain calculation Σh² valid for any white level.
> **Key point:** Discrete white noise with flat PSD S₀ has total power exactly S₀; whiteness is a statement about spectral *shape*, so S₀ → 0 shrinks the process to zero without changing its flat shape.

### Q178. A process has PSD S_X(f) = A/(f² + f₀²). Obtain its autocorrelation and total power, and identify a system that would produce it.

> **Type:** Numerical
> **Answer:** R_X(τ) = (Aπ/f₀)e^{−2πf₀|τ|}, and the total power is R_X(0) = Aπ/f₀, which matches the spectral integral ∫_{−∞}^{∞}A/(f² + f₀²)df = Aπ/f₀. The process is produced by driving the one-pole H(f) = f₀/(f₀ + jf) with white noise of PSD S₀ = A/f₀².
> **Solution:** Apply the transform pair ∫_{−∞}^{∞}e^{−a|τ|}e^{−j2πfτ}dτ = 2a/(a² + 4π²f²) with a = 2πf₀. That gives the transform of e^{−2πf₀|τ|} as 4πf₀/(4π²f₀² + 4π²f²) = f₀/(π(f₀² + f²)), so the prefactor that produces A/(f² + f₀²) is Aπ/f₀. Hence R_X(τ) = (Aπ/f₀)e^{−2πf₀|τ|}, and consistency demands R_X(0) = ∫S_X(f)df = A·(π/f₀), which is what the formula gives — the standard check that a transform pair is correctly scaled. For the system interpretation, a one-pole low-pass with corner f₀ in hertz has |H(f)|² = f₀²/(f₀² + f²), so driving it with white noise of PSD S₀ gives S_Y(f) = S₀f₀²/(f₀² + f²). Matching the target A/(f₀² + f²) fixes S₀f₀² = A, i.e. S₀ = A/f₀². The output power is S₀ × ENBW with ENBW = πf₀, giving (A/f₀²)(πf₀) = Aπ/f₀, exactly R_X(0) and consistent with the spectral integral.
> **Key point:** S_X(f) = A/(f² + f₀²) is a Lorentzian: R_X(τ) = (Aπ/f₀)e^{−2πf₀|τ|}, total power Aπ/f₀ = ∫S_X df; it is the output of H(f) = f₀/(f₀ + jf) fed with white noise of PSD A/f₀², whose ENBW is πf₀.

### Q179. A first-order autoregressive process satisfies R_X[m] = σ²a^{|m|}/(1 − a²) for |a| < 1. Give its PSD and verify it integrates to the total power.

> **Type:** Numerical
> **Answer:** S_X(f) = σ²/(1 + a² − 2a cos 2πf), the Poisson-kernel form, and ∫_{−1/2}^{1/2}S_X(f)df = σ²/(1 − a²) = R_X[0], as required.
> **Solution:** Summing the two geometric tails of the autocorrelation, R̂(f) = Σ_{m=−∞}^{∞}(σ²/(1−a²))a^{|m|}e^{−j2πfm} = (σ²/(1−a²))[1 + Σ_{m≥1}a^m(e^{−j2πfm} + e^{j2πfm})] = (σ²/(1−a²))·(1 − a²)/(1 + a² − 2a cos 2πf), using the standard identity Σ_{m≥1}a^m cos(mθ) = (a cos θ − a²)/(1 − 2a cos θ + a²). The denominator 1 + a² − 2a cos 2πf = (1 − a)² + 2a(1 − cos 2πf) is strictly positive for |a| < 1, so the spectrum is positive and integrable, and the integral reproduces R_X[0] = σ²/(1 − a²). This is the first-order AR(1) spectrum; larger a concentrates the power in narrower lobes near f = 0.
> **Key point:** AR(1) with R[m] = σ²a^{|m|}/(1−a²) has S_X(f) = σ²/(1 + a² − 2a cos 2πf) = (σ²/(1−a²))·(1−a²)/|1 − ae^{−j2πf}|², and ∫S df = σ²/(1−a²).

### Q180. Give the autocorrelation of the derivative of a WSS process in terms of the spectral density, and state when the derivative exists in the mean-square sense.

> **Type:** Theory
> **Answer:** If ẋ(t) = dx/dt exists in the mean-square sense, then R_ẋẋ(τ) = −R_X″(τ) and S_ẋ(f) = (2πf)²S_X(f). The mean-square derivative exists exactly when the second moment of X at two times is twice differentiable, equivalently when ∫(2πf)²S_X(f)df is finite.
> **Solution:** Differentiating R_X(t₁, t₂) with respect to the lag relies on the mean-square differentiability of the process, which is precisely the assumption; the result is R_ẋẋ(τ) = −d²R_X(τ)/dτ². In frequency, differentiation multiplies by j2πf, so the PSD is scaled by (2πf)². Ideal white noise has the flat spectrum S_X = σ², for which ∫(2πf)²σ²df diverges, so the mean-square derivative does not exist. This is different from the random constant process X[n] = Z, whose discrete-time spectrum is a periodic impulse train and whose samples are not uncorrelated.
> **Key point:** Differentiation multiplies the spectrum by (2πf)²: S_ẋ(f) = (2πf)²S_X(f) and R_ẋẋ(τ) = −R_X″(τ); it requires ∫(2πf)²S_X df < ∞, which fails for ideal white noise because its spectrum is flat rather than impulsive.

### Q181. Show that a discrete-time system with impulse response h[n] driven by a stationary input has output variance given by the sum Σ h[n]²R_x[0] when the input is white, and give the general form for a coloured input.

> **Type:** Theory
> **Answer:** For white input R_x[m] = σ_x²δ[m], R_y[k] = σ_x²Σ_n h[n]h[n+k] = σ_x²(h ⋆ h^⊖)[k], and R_y[0] = σ_x²Σ_n h[n]². For a coloured input, R_y[0] = Σ_n Σ_m h[n]h[m]R_x[n−m], which is a quadratic form in the impulse response.
> **Solution:** Substituting y[k] = Σ_n h[n]x[k−n] into R_y[0] = E[y²] and using stationarity gives the double sum; the white case collapses it because R_x[n−m] is a Kronecker delta that kills every term with n ≠ m, leaving the sum of squares. Physically, a flat input spectrum means every frequency is stimulated equally, so the output power measures the filter's total gain summed over frequency, Parseval's theorem in disguise.
> **Key point:** White input ⟹ output variance = σ_x²Σh[n]²; a coloured input gives the quadratic form Σ_m Σ_n h[m]h[n]R_x[m−n] instead.

### Q182. A narrowband process around a carrier f_c with bandwidth W is written X(t) = √2I(t)cos(2πf_ct + Θ) − √2Q(t)sin(2πf_ct + Θ). State the conditions on I, Q and the relation between their PSDs for this to be a valid representation.

> **Type:** Theory
> **Answer:** I(t) and Q(t) must be jointly WSS, uncorrelated at all nonzero lags (circular, or quadrature, symmetry: E[I(t)Q(t+τ)] = 0 for τ ≠ 0), and have equal PSDs S_I(f) = S_Q(f) with support confined to |f| ≤ W where W ≪ f_c. Under these conditions the PSD of X is S_X(f) = S_I(f + f_c) + S_I(f − f_c), a pair of symmetric copies of the baseband spectrum.
> **Solution:** Substituting the quadrature representation and averaging over the fast carrier, the products of I and Q with the carrier harmonics collapse to terms involving only the baseband spectrum, and the cross terms vanish by the quadrature symmetry condition, leaving the two shifted copies. The double-sideband structure is the reason a narrowband process carries its information in two sidebands symmetric about f_c, and why a narrowband receiver can process the baseband signal I and Q directly in digital form. The condition W ≪ f_c is what keeps the two shifted spectra from overlapping, and it is the assumption that lets the approximation be written as an equality.
> **Key point:** A narrowband process has quadrature components I, Q that are uncorrelated at nonzero lags with equal low-pass PSDs; its spectrum is S_X(f) = S_I(f+f_c) + S_I(f−f_c), two symmetric copies confined near the carrier.

### Q183. Give the PSD of a first-order moving-average process x[n] = w[n] − a w[n−1] with white w of variance σ_w², and find its variance.

> **Type:** Numerical
> **Answer:** S_X(f) = σ_w²(1 − a² + 2a cos 2πf) = σ_w²|1 − ae^{−j2πf}|², and R_X[0] = 2σ_w²(1 − a) for 0 < a < 1, which is 0.2σ_w² for a = 0.9. The spectrum has a zero at f = 1/2 and peaks at DC.
> **Solution:** The impulse response h = δ[n] − aδ[n−1] gives |H(f)|² = |1 − ae^{−j2πf}|² = 1 + a² − 2a cos 2πf, so filtering white noise multiplies the flat spectrum by this factor. The variance is the integral of the spectrum, equivalently the sum of squared coefficients: 1² + a² = 1 + a² for the general case. For 0 < a < 1 the standard differencing form x[n] = w[n] − a w[n−1] is a high-pass filter: |H(0)|² = (1−a)² < 1 while |H(1/2)|² = (1+a)² > 1, so the DC content is suppressed by (1−a)². Averaging over the unit circle, ∫_{-1/2}^{1/2}(1 + a² − 2a cos 2πf)df = 1 + a², giving variance σ_w²(1 + a²) = 1.81σ_w² for a = 0.9. This is the classic first-difference pre-emphasis used to suppress low-frequency content in speech and in error-diffusion quantisers, and it is MA(1), the dual of the AR(1) spectrum in an earlier question.
> **Key point:** The MA(1) spectrum is S_X(f) = σ_w²(1 + a² − 2a cos 2πf) with variance σ_w²(1 + a²) = 1.81σ_w² at a = 0.9; the zero at f = 1/2 makes it a high-pass, the spectral dual of AR(1).

### Q184. State the Wiener–Khinchin relations in both directions and explain why the PSD of a WSS process is uniquely determined by its autocorrelation.

> **Type:** Theory
> **Answer:** S_X(f) = ∫_{−∞}^{∞}R_X(τ)e^{−j2πfτ}dτ and R_X(τ) = ∫_{−∞}^{∞}S_X(f)e^{j2πfτ}df. The pair is a Fourier transform, so it is one-to-one: two processes with the same autocorrelation have the same spectrum and vice versa, whenever the integrals exist.
> **Solution:** Both directions are the same computation, so the mapping is injective on the class of functions for which the transform exists — typically the absolutely integrable autocorrelations, which is guaranteed for processes with a second moment under mild conditions. The practical consequence is that a measurement of the autocorrelation determines the spectrum exactly, which is what makes the FFT-based power spectral estimator a direct estimate of the true spectrum. The limitation is that a truncated finite-length record yields a biased estimate, since the empirical autocorrelation of a finite sample is not the true autocorrelation.
> **Key point:** Wiener–Khinchin gives S_X(f) = FT{R_X(τ)} and R_X(τ) = FT{S_X(f)}; because the transform is one-to-one, the autocorrelation and the spectrum determine each other completely.

### Q185. An amplifier has |H(f)|² = G² for |f| ≤ B and 0 elsewhere, and its input-referred noise density is S₀ = 4 nV²/Hz. With B = 20 kHz, find the total output-referred noise.

> **Type:** Numerical
> **Answer:** σ_out² = G²S₀·2B. With G = 50, S₀ = 4 nV²/Hz, 2B = 40 kHz: σ_out² = 2500 × 4 × 10⁻¹⁸ × 4 × 10⁴ = 4 × 10⁻¹⁰ V², so σ_out = 2 × 10⁻⁵ V = 20 µV. The input-referred total is √(4 × 10⁻¹⁸ × 4 × 10⁴) = 4 × 10⁻⁷ V = 0.4 µV, which is √400 = 20 times smaller.
> **Solution:** The output PSD is G²S₀ across the full width 2B, so the total output power is G²S₀·2B = 2500 × 4 × 10⁻¹⁸ × 4 × 10⁴ = 4 × 10⁻¹⁰ V², and its square root is 2 × 10⁻⁵ V = 20 µV. Input-referred means dividing by the gain, so √(4 × 10⁻¹⁰)/50 = 2 × 10⁻⁵/50 = 4 × 10⁻⁷ V = 0.4 µV, exactly the value obtained by integrating the flat input density over the bandwidth. The factor of two in 2B is the two-sided width of the passband; had the density been given as a one-sided figure, the bandwidth 20 kHz would be used instead.
> **Key point:** An ideal bandpass amplifier of total width 2B gives σ_out² = 2B·G²·S₀; here 4 × 10⁻¹⁰ V², so 20 µV output-referred, or 0.4 µV input-referred — the √400 = 20× difference being the gain.

---

## Section 9. Power spectral density: definition, Wiener–Khinchin, properties, common spectra (Q186–Q214)

### Q186. Define the power spectral density of a WSS process and state its two defining properties as a function.

> **Type:** Theory
> **Answer:** S_X(f) is the Fourier transform of the autocorrelation, S_X(f) = ∫R_X(τ)e^{−j2πfτ}dτ. It is **real** and **non-negative** for a real process, and ∫S_X(f)df = R_X(0) = E[X²] when the power is finite.
> **Solution:** Realness and evenness of R_X(τ) for a real process force the transform to be real, and positive semi-definiteness of a valid autocorrelation forces its transform to be non-negative. The integral identity is the Wiener–Khinchin relation evaluated at zero lag, where the exponential becomes unity. Together these three properties are what make S_X(f) readable as a power density: it cannot go negative, and its total area is the total power.
> **Key point:** S_X(f) = FT{R_X(τ)} is real, even and ≥ 0, with total area ∫S_X df = R_X(0) = E[X²].

### Q187. State the three requirements for a function to be a valid power spectral density, and prove the equivalence of the time- and frequency-domain characterisations of white noise.

> **Type:** Theory
> **Answer:** A valid S_X(f) must satisfy (i) S_X(f) ≥ 0 for all f, (ii) R_X(τ) = ∫S_X(f)e^{j2πfτ}df must tend to zero as |τ| → ∞, and (iii) R_X(0) must be finite, i.e. S_X must be integrable. White noise is characterised by R_X(τ) = σ²δ(τ) and its Fourier transform gives S_X(f) = σ² exactly.
> **Solution:** Requirement (i) is non-negativity, forced by positive semi-definiteness of the autocorrelation. Requirement (ii) is the integrability condition tying the spectral line at zero frequency to the long-lag limit of the correlation. Requirement (iii) is finiteness of total power, which follows from R_X(0) = E[X²] being finite for any random variable. For white noise the autocorrelation is a Dirac impulse, whose transform under the f-in-Hz convention is a constant, the defining flat spectrum.
> **Key point:** A valid S_X needs S_X ≥ 0, integrable with ∫S df = R(0), and R(∞) = 0. White noise R = σ²δ ⟺ S(f) = σ², a constant.

### Q188. A process has spectrum S_X(f) = 20/(1 + (f/300)²) with f in Hz. Find its autocorrelation, total power and correlation time.

> **Type:** Numerical
> **Answer:** R_X(τ) = 6000π·e^{−600π|τ|} ≈ 1.885 × 10⁴·e^{−1.885 × 10³|τ|}, so the total power is R_X(0) = 6000π ≈ 1.885 × 10⁴. The correlation time, defined as ∫R(τ)/R(0)dτ over τ from −∞ to ∞, is 2/(600π) ≈ 1.061 × 10⁻³ s.
> **Solution:** Reshape the spectrum: 20/(1 + (f/300)²) = 20 · 300²/(f² + 300²) = 1.8 × 10⁶/(f² + 300²), so it is of the Lorentzian form C/(f² + a²) with C = 1.8 × 10⁶ and a = 300 Hz. The transform pair for that form is R_X(τ) = (Cπ/a)e^{−2πa|τ|}, obtained by matching the pair ∫e^{−2πa|τ|}e^{−j2πfτ}dτ = 2(2πa)/((2πa)² + (2πf)²) = a/(π(a² + f²)). Hence R_X(τ) = (1.8 × 10⁶ · π/300)e^{−600π|τ|} = 6000π e^{−600π|τ|}. The consistency check R_X(0) = ∫S_X(f)df = 20 · 300 · π = 6000π ≈ 1.885 × 10⁴ confirms the scaling. The normalised autocorrelation is e^{−600π|τ|}, so its integral is 2/(600π) ≈ 1.061 × 10⁻³ s, twice the decay constant 1/(600π) ≈ 5.31 × 10⁻⁴ s — a fact worth remembering, since the correlation time of an exponential correlation is 2τ.
> **Key point:** S_X(f) = 20/(1 + (f/300)²) gives R_X(τ) = 6000π·e^{−600π|τ|} and total power 6000π ≈ 1.885 × 10⁴; the correlation time of an exponential decay e^{−t/τ} is 2τ, here 1.061 × 10⁻³ s.

### Q189. Find the 3-dB bandwidth of a process with autocorrelation R_X(τ) = σ²e^{−|τ|/τ_c} in terms of τ_c, and give the spectrum.

> **Type:** Numerical
> **Answer:** S_X(f) = 2σ²τ_c/(1 + 4π²f²τ_c²), a Lorentzian of half-width at half-maximum f_H = 1/(2πτ_c). The −3 dB point is where the denominator is 2, giving f₃ = 1/(2πτ_c√2), and the one-sided 3-dB bandwidth is 2f₃ = 1/(πτ_c√2).
> **Solution:** Substituting a = 1/τ_c into ∫e^{−a|τ|}e^{−j2πfτ}dτ = 2a/(a² + 4π²f²) gives S_X(f) = 2σ²τ_c/(1 + 4π²f²τ_c²), whose peak value is 2σ²τ_c. Setting S_X(f₃) = σ²τ_c (half the peak) reads 1 + 4π²f₃²τ_c² = 2, so f₃ = 1/(2πτ_c√2). With τ_c = 0.5 s this gives f₃ ≈ 0.2251 Hz and one-sided 3-dB bandwidth ≈ 0.4502 Hz. The two-sided width between ±f₃ is 1/(πτ_c√2), and ENBW over all frequencies is 1/(2τ_c), which exceeds the 3-dB width by a factor of √2 — the standard result for a one-pole response.
> **Key point:** R_X(τ) = σ²e^{−|τ|/τ_c} gives the Lorentzian S_X(f) = 2σ²τ_c/(1 + 4π²f²τ_c²); f₃ = 1/(2πτ_c√2), ENBW = 1/(2τ_c) = √2 × the 3-dB bandwidth.

### Q190. Which of the following statements about the power spectral density are true?

> **Type:** MSQ (GATE-2)
> **Answer:** Statements (a), (b) and (d) are true; (c) and (e) are false. (Options a, b, d)
>
> (a) The PSD of a real WSS process is real and even.
> (b) The PSD of a WSS process is non-negative.
> (c) The PSD of a process with a nonzero mean is continuous everywhere.
> (d) The area under the PSD equals the mean-square value of the process.
> (e) A process with a flat PSD necessarily has zero variance.
> **Solution:** (a) holds because R_X(τ) is real and even for a real process, and the Fourier transform of an even real function is real and even. (b) holds because a valid autocorrelation is positive semi-definite, and its transform must be non-negative. (c) is false: a nonzero mean contributes a Dirac impulse at DC, so the spectrum is not continuous. (d) is the Wiener–Khinchin relation at zero lag. (e) is false: a flat PSD of height S₀ has variance S₀, not zero — flatness is about shape, not level.
> **Key point:** (a), (b) and (d) are true. A nonzero mean makes the spectrum contain a DC impulse, and a flat PSD of height S₀ gives variance S₀, so flatness never implies zero power.

### Q191. Show that the sum of two independent WSS processes with spectra S_1(f) and S_2(f) has spectrum S_1(f) + S_2(f), and state what changes if they are not independent.

> **Type:** Theory
> **Answer:** Independence gives Cov(X(t), Y(t+τ)) = 0 for all τ, so R_{X+Y}(τ) = R_X(τ) + R_Y(τ) and S_{X+Y}(f) = S_X(f) + S_Y(f). Without independence, an extra cross term appears: S_{X+Y}(f) = S_X(f) + S_Y(f) + 2Re{S_{XY}(f)}, where S_{XY} is the cross-spectral density.
> **Solution:** Expanding E[(X(t)+Y(t))(X(t+τ)+Y(t+τ))] and taking expectations, the cross terms E[X(t)Y(t+τ)] and E[Y(t)X(t+τ)] survive unless the processes are uncorrelated at every lag. Independence implies uncorrelatedness at all lags, so they vanish. The remaining sum of autocorrelations transforms to the sum of spectra. The general case is the standard decomposition of a two-channel signal into uncorrelated plus coherent parts, and it is why the sum of correlated noises can be much quieter or much louder than the sum of the individual powers.
> **Key point:** Uncorrelated processes add in power: S_{X+Y} = S_X + S_Y. Correlated ones add a cross term 2Re{S_{XY}(f)}, which can be negative and cancel power.

### Q192. Give the PSD of the sum of two independent white noise processes of variances σ₁² and σ₂², and state the effective noise figure of the combination.

> **Type:** Numerical
> **Answer:** S(f) = (σ₁² + σ₂²) is still white, with total variance σ₁² + σ₂². The combination is equivalent to a single source of variance σ₁² + σ₂², so the equivalent input-referred noise of the pair, referred to the σ₁² port, is σ²/σ₁² = 1 + σ₂²/σ₁².
> **Solution:** Sums of flat spectra are flat, so the sum of two white noises is white with the summed variance — the only new thing is the level. Referring the combined input noise to the first port divides by σ₁², giving 1 + σ₂²/σ₁², which is the familiar form of a noise figure: the ratio of total input-referred noise to the noise of the source alone. This holds regardless of how the two variances are apportioned between the sources, only their sum matters for the downstream signal-to-noise ratio.
> **Key point:** Sums of independent white noises stay white with variance σ₁² + σ₂²; referred to the σ₁² port the equivalent input noise is 1 + σ₂²/σ₁², the standard noise-figure form.

### Q193. Show that filtering white noise of PSD S₀ through a filter with impulse response h gives output PSD S₀Σ|h[n]|²/…, i.e. a constant times the squared-magnitude response.

> **Type:** Theory
> **Answer:** S_Y(f) = S₀|H(f)|², and by Parseval S₀|H(f)|² integrates to S₀Σ_n|h[n]|², so the output variance is S₀Σ_n|h[n]|². The output is not white unless H is constant in magnitude.
> **Solution:** The output PSD is S_X(f)|H(f)|², which for flat S_X(f) = S₀ is simply S₀|H(f)|². The variance is the integral of that, which by Parseval equals the time-domain sum Σh[n]². The engineering consequence is that white noise through a filter stays white only if the filter is all-pass; every real filter shapes the noise the same way it shapes the signal.
> **Key point:** White input gives S_Y(f) = S₀|H(f)|² and σ_Y² = S₀Σ_n|h[n]|²; the output is coloured unless |H(f)| is constant.

### Q194. Define white noise and give its autocorrelation and PSD, in both continuous and discrete time.

> **Type:** Theory
> **Answer:** White noise has a flat PSD: S_X(f) = N₀/2 (one-sided convention) or σ² over the full band. Continuous time: R_X(τ) = (N₀/2)δ(τ). Discrete time: R_X[m] = σ²δ[m] and S_X(f) = σ².
> **Solution:** Whiteness means the second-order statistics are uncorrelated at all nonzero separations, R_X(τ) = 0 for τ ≠ 0, which is a delta in continuous time and a Kronecker delta in discrete time. The Fourier transform of a delta is a constant, so the PSD is flat. The two-sided density N₀/2 corresponds to a one-sided density N₀ over positive frequencies, the usual thermal-noise convention. Ideal white noise is not a physically realisable process over all frequencies — it is a model valid up to some cutoff, and the derived quantities are finite as long as the filter response limits the band.
> **Key point:** White noise: flat PSD N₀/2 (two-sided), R_X(τ) = (N₀/2)δ(τ) continuous or σ²δ[m] discrete; uncorrelated at every nonzero lag.

### Q195. What is the relationship between the bandwidth of a signal and the spectral extent of its autocorrelation?

> **Type:** Theory
> **Answer:** They are Fourier duals: the spectral width of S_X(f) is inversely proportional to the correlation length of R_X(τ). A signal confined to bandwidth B has an autocorrelation that decays over a time of order 1/B, and a process with correlation time τ_c has a spectrum of width of order 1/τ_c.
> **Solution:** Multiplication by a rectangular window of half-width B in frequency is convolution with a sinc in time, so a hard bandwidth limit produces an oscillating, slowly decaying autocorrelation R(τ) = S₀ sin(2πBτ)/(πτ), whose first zero is at 1/(2B). The uncertainty-type relation is the reason a narrowband signal has a long correlation time: you cannot have both a small frequency spread and a small time spread. This duality underlies time-bandwidth product limits in communications and the fact that a spread-spectrum signal has a low PSD despite high total power.
> **Key point:** Bandwidth and correlation length are Fourier duals: a signal of bandwidth B decorrelates over a time ≈ 1/B, with the ideal low-pass correlation sin(2πBτ)/(πτ) first vanishing at 1/(2B), and a process of correlation time τ_c occupies ≈ 1/τ_c of spectrum.

### Q196. Compute the PSD of a process that is white with PSD S₀ passed through an ideal low-pass filter of cutoff B, and give the output variance.

> **Type:** Numerical
> **Answer:** S_Y(f) = S₀ for |f| ≤ B and 0 otherwise, so the output is band-limited white with variance S₀·2B.
> **Solution:** Multiplying the flat input spectrum by the filter's unit gain over the passband and zero outside gives the rectangular output spectrum. The variance is the area, S₀ times the total width 2B. The output is white in the only sense that matters within its band: it has no spectral shaping, so all information about it must come from the band limit rather than the shape. This is the model of band-limited thermal noise, and it is the reason a receiver's noise figure is specified over a band.
> **Key point:** Band-limited white noise has S_Y(f) = S₀ on |f| ≤ B and variance 2B·S₀; the shape carries no information, only the band limit does.

### Q197. Define the spectral density at a frequency and relate it to the power in a small band around it.

> **Type:** Theory
> **Answer:** S_X(f) is the power per unit bandwidth at frequency f, defined so that the power in a band [f₁, f₂] is ∫_{f₁}^{f₂}S_X(f)df ≈ S_X(f₀)(f₂ − f₁) for a narrow band about f₀. It is a density, not a pointwise power.
> **Solution:** Because the spectrum is a continuous function, power accumulates over an interval, and S_X(f)df is the power in the differential band [f, f + df]. The definition is the continuous-time analogue of a probability density, inheriting the same caveat: a single point has zero power, so a "power at frequency f" is only meaningful as a limiting density. For a process with a line spectrum, the density is a sum of Dirac impulses whose weights are the individual line powers.
> **Key point:** S_X(f)df is the power in the band [f, f+df]; S_X is a density per Hz, so power is always an integral, and line spectra appear as Dirac impulses.

### Q198. Show that the autocorrelation of a WSS process with a nonzero mean contains a constant term μ², and give the corresponding term in the spectrum.

> **Type:** Theory
> **Answer:** R_X(τ) = μ² + C_X(τ), and the constant μ² transforms to a Dirac impulse at DC of total weight μ². The rest of the spectrum is the spectrum of the zero-mean fluctuation.
> **Solution:** Decompose X = μ + Z with E[Z] = 0. Then E[X(t)X(t+τ)] = μ² + E[Z(t)Z(t+τ)], because the cross terms contain E[Z] and vanish. In frequency, the constant μ² becomes a delta at f = 0, whose total weight is μ². The engineering reading is that a nonzero mean is pure DC power that no filter with H(0) = 0 can pass, which is why mean removal precedes spectral estimation.
> **Key point:** R_X(τ) = μ² + C_X(τ): a nonzero mean contributes a DC line of weight μ², removable by subtracting the mean before spectral analysis.

### Q199. Give the spectrum of a deterministic periodic signal and relate its line weights to its average power.

> **Type:** Theory
> **Answer:** A periodic signal of period T has the line spectrum S_X(f) = (1/T)Σ_k C_k δ(f − k/T), with C_k the complex Fourier-series coefficients, and the average power is Σ_k|C_k|². For x(t) = Acos(2πf₀t) this is (A²/4)[δ(f−f₀) + δ(f+f₀)], giving power A²/2, with no line at DC.
> **Solution:** Writing the periodic signal as x(t) = Σ_k C_ke^{j2πkt/T} and transforming term by term gives X(f) = Σ_k C_kδ(f − k/T), and since the squared magnitude of each exponential is 1 the power spectrum has the same 1/T weights. A cosine of amplitude A at frequency f₀ has C₁ = C_{−1} = A/2 and all other C_k = 0, so the two lines each carry A²/4 and the total is A²/2, which is the known mean-square value of a unit-amplitude cosine. There is no DC term because the coefficients at k = 0 vanish; a DC line appears only when a genuine constant offset is present, and its weight is that offset squared. This is the deterministic analogue of the random-phase sinusoid considered next.
> **Key point:** A periodic signal of period T has S_X(f) = (1/T)Σ_k C_kδ(f − k/T) with power Σ_k|C_k|²; a cosine of amplitude A gives two lines of weight A²/4 and power A²/2, with no DC line.

### Q200. Find the PSD of the process X(t) = cos(2πf₀t + Θ) with Θ uniform, and its average power.

> **Type:** Numerical
> **Answer:** S_X(f) = ¼[δ(f − f₀) + δ(f + f₀)], and the average power is R_X(0) = ½. There is no DC component, since the random phase makes E[X(t)] = 0.
> **Solution:** Averaging the product of two cosines over a full period of the uniform phase Θ kills the term containing 2Θ and leaves E[cos(2πf₀t + Θ)cos(2πf₀(t+τ) + Θ)] = ½cos(2πf₀τ), so R_X(τ) = ½cos(2πf₀τ). Since cos(2πf₀τ) transforms to ½[δ(f−f₀) + δ(f+f₀)], the spectrum is ¼[δ(f−f₀) + δ(f+f₀)]. The power is the sum of the line weights, ¼ + ¼ = ½, matching R_X(0) = ½, and the absence of a DC line reflects E[X] = 0. This is the narrowband-noise model: a random-phase sinusoid is the basic building block from which a general bandlimited noise process is assembled.
> **Key point:** A unit-amplitude random-phase sinusoid has S_X(f) = ¼[δ(f−f₀) + δ(f+f₀)], power ½, and no DC line because E[X] = 0.

### Q201. State the properties of the cross-spectral density S_XY(f) and the constraint on the cross-correlation.

> **Type:** Theory
> **Answer:** S_XY(f) is the Fourier transform of the cross-correlation R_XY(τ). It is generally complex, and it satisfies the Hermitian symmetry S_XY*(f) = S_YX(−f). The magnitude satisfies the Cauchy–Schwarz bound |S_XY(f)|² ≤ S_X(f)S_Y(f), and this bound is saturated exactly when the two processes are proportional at that frequency.
> **Solution:** Cross-correlation is a two-variable function, so the transform need not be real, and the relation R_XY(−τ) = R_YX(τ) becomes the conjugate-reversal symmetry above. The Cauchy–Schwarz inequality applied to the joint distribution of the two spectral components gives the magnitude bound, which is the frequency-domain form of the fact that correlation cannot exceed the geometric mean of the two variances. Coherence is defined as the normalised quantity |S_XY|²/(S_XS_Y), and it is exactly the fraction of Y's power at each frequency that is linearly predictable from X.
> **Key point:** S_XY(f) = FT{R_XY(τ)} is generally complex, satisfies S_XY*(f) = S_YX(−f), and obeys |S_XY|² ≤ S_XS_Y; the normalised bound is the coherence function, equal to 1 where X and Y are proportional.

### Q202. Given S_X(f), S_Y(f) and S_XY(f), show that the LTI system's transfer function can be recovered as H(f) = S_YX(f)/S_XX(f), and state the condition for its validity.

> **Type:** Theory
> **Answer:** For the model Y(t) = ∫h(u)X(t−u)du, S_XY(f) = H(f)S_X(f), so H(f) = S_XY(f)/S_X(f) wherever S_X(f) > 0. The recovery is valid wherever the input spectrum is nonzero, and is ill-posed where S_X vanishes.
> **Solution:** The output is the input filtered, so the output spectrum is the input spectrum times the transfer function, and the cross-spectrum with the input is H times the input's own spectrum. Dividing recovers H at every frequency where the input actually excites the system. This is the basis of system identification by spectral estimation and of adaptive noise cancellation, where a single tap-filling filter is estimated as the ratio of cross- to auto-spectra. The condition S_X > 0 is essential: at frequencies with no input energy the ratio is 0/0 and H is undetermined.
> **Key point:** H(f) = S_XY(f)/S_X(f) recovers the transfer function wherever S_X(f) > 0, the basis of spectral-ratio system identification; it is undefined where the input has no power.

### Q203. Compute the PSD of a first-order autoregressive process in terms of its correlation coefficient, and identify the −3 dB frequency.

> **Type:** Numerical
> **Answer:** S_X(f) = σ²(1−a²)/(1 + a² − 2a cos 2πf) for a process with R[m] = σ²a^{|m|}; the −3 dB point satisfies 1 + a² − 2a cos 2πf₃ = 2(1−a²), giving cos 2πf₃ = (3a² − 1)/(2a).
> **Solution:** The autocorrelation is the two-sided geometric sequence, whose Fourier transform is the Poisson kernel. The 3-dB condition halves the peak value σ²(1−a²)/(1−a)², so the denominator must double: 1 + a² − 2a cos 2πf₃ = 2(1 − a²), hence cos 2πf₃ = (3a² − 1)/(2a). This has a solution in [0, 0.5] only when a exceeds 1/√3, since otherwise the process is so strongly correlated that the spectrum never falls to half its peak within the band. For a = 0.5, cos 2πf₃ = −0.25, so f₃ = arccos(−0.25)/(2π) ≈ 0.2098 cycles per sample.
> **Key point:** S_X(f) = σ²(1−a²)/(1 + a² − 2a cos 2πf) for an AR(1) with correlation a; the −3 dB frequency is arccos((3a²−1)/(2a))/(2π) when a > 1/√3, and there is no in-band −3 dB point below that.

### Q204. Show that a process with a rational PSD has an autoregressive representation, and give the form of the all-pole filter.

> **Type:** Theory
> **Answer:** A rational PSD S_X(z) = S_A(z)/S_B(z) with z = e^{j2πf} and no common factors admits a finite-order linear time-invariant model driven by white noise: X[n] + Σ_{k=1}^{p}b_kX[n−k] = W[n] + Σ_{k=1}^{q}a_kW[n−k]. It is ARMA(p, q) in general, and purely AR (all-pole) only when the numerator S_A is a constant, i.e. the spectrum has no zeros.
> **Solution:** Rationality means the spectrum is a finite-degree function of z, so the process satisfies a linear difference equation with constant coefficients whose input is the innovation. Factoring S_B into roots inside and outside the unit circle and reflecting the outside ones by z → 1/z̄ produces a causal, stable denominator; the numerator S_A contributes a moving-average part. The all-pole special case occurs when S_A is constant, which is precisely the AR case; an arbitrary rational spectrum with a non-constant numerator, such as the MA(1) spectrum σ_w²|1 − ae^{−j2πf}|², is not all-pole. This correspondence underlies AR and ARMA spectral estimation, Yule–Walker, and the Levinson recursion.
> **Key point:** A rational PSD corresponds to an ARMA(p, q) model driven by white noise; it reduces to a pure all-pole AR model only if the numerator is constant, i.e. the spectrum has no zeros.

### Q205. Define the spectral density of a real process and show it must be real and even.

> **Type:** Theory
> **Answer:** S_X(f) = ∫R_X(τ)e^{−j2πfτ}dτ. Since R_X(τ) is real, the sine part integrates to zero by oddness, so S_X(f) = ∫R_X(τ)cos(2πfτ)dτ is real. Since R_X(τ) = R_X(−τ) is even, the cosine is even in f, so S_X(f) = S_X(−f).
> **Solution:** Writing the exponential in sine-cosine form, the imaginary part is −∫R_X(τ)sin(2πfτ)dτ. R_X is real, and the sine is odd in τ, so the integrand is odd and its integral over the symmetric whole line vanishes. Similarly, R_X even means the integral depends only on |f|, giving evenness. Neither property survives for complex processes: a complex exponential is a genuine one-sided spectrum, and a complex process can have a non-real, non-even PSD.
> **Key point:** A real WSS process has R_X(τ) real and even, so S_X(f) = ∫R_X(τ)cos 2πfτ dτ is real and even; the sine part vanishes by oddness. Complex processes lose both properties.

### Q206. Give the spectrum of white noise passed through a differentiator, and state the result for ideal white noise.

> **Type:** Theory
> **Answer:** Differentiation multiplies the spectrum by (2πf)², so S_Y(f) = (2πf)²S_X(f). For ideal white noise with S_X = N₀/2 the output spectrum is (2πf)²N₀/2, which grows without bound as f increases, so the output variance ∫S_Y(f)df diverges and the derivative does not exist in the mean square.
> **Solution:** The derivative operator has transfer function H(f) = j2πf, and S_Y = |H|²S_X = (2πf)²S_X. For white noise the spectrum is flat, so the output spectrum grows as f², which is unbounded — the output variance would be infinite, so the derivative of ideal white noise does not exist as an ordinary random process. Real filters band-limit the input, making the integral of (2πf)²S_X finite and the derivative well-defined. This is the precise sense in which differentiation amplifies high-frequency noise.
> **Key point:** Differentiation gives S_Y(f) = (2πf)²S_X(f); ideal white noise has infinite derivative variance, so it is not mean-square differentiable, though any band-limited noise is.

### Q207. State the definition of a Gaussian random process and give the reason Gaussian processes are so widely used in linear systems analysis.

> **Type:** Theory
> **Answer:** A Gaussian process is one every finite collection of which is jointly Gaussian. It is widely used because a linear functional of a Gaussian process is again Gaussian, so output statistics are determined entirely by the mean and autocorrelation, and the mean-square closure of linear systems is exact rather than approximate.
> **Solution:** Joint Gaussianity means the characteristic function of any finite vector factorises, and by the Cramér–Wold device that makes every linear combination Gaussian. Linearity then takes a Gaussian process to a Gaussian process, and the output covariance is determined by the input covariance through the deterministic relation R_y = h ⋆ h^⊖ ⋆ R_x. Nothing needs to be assumed about higher-order statistics, which is exactly what fails for non-Gaussian inputs and motivates the Volterra and Wiener series treatments. This closure under linear operations is the reason Gaussian noise dominates the analysis of linear electronic systems.
> **Key point:** Every finite collection of a Gaussian process is jointly Gaussian, so linear systems map it to a Gaussian process and the mean-square analysis closes exactly on first- and second-order statistics alone.

### Q208. Give the spectrum of a rectangular pulse of duration T and amplitude A, and relate it to the pulse's energy.

> **Type:** Numerical
> **Answer:** S(f) = A²T²sinc²(Tf) with sinc(Tf) = sin(πTf)/(πTf), so the spectrum is a squared sinc of total area A²T, the pulse's energy. The half-power points are at f = ±0.443/T.
> **Solution:** The pulse x(t) = A for 0 ≤ t < T and zero elsewhere has transform X(f) = A∫₀^T e^{−j2πft}dt = AT e^{−jπfT}sin(πfT)/(πf), whose magnitude squared is A²T²sinc²(fT). Integrating, ∫_{−∞}^{∞}|X(f)|²df = A²T by Parseval, since the time-domain energy is ∫|x|²dt = A²T. The half-power point sin(πfT) = πfT/√2 solves at fT ≈ 0.443, the familiar time-bandwidth product of a rectangular pulse.
> **Key point:** A rectangular pulse of duration T has |X(f)|² = A²T²sinc²(fT), total energy A²T, and half-power bandwidth 0.886/T; energy and bandwidth trade inversely as the time-bandwidth product.

### Q209. Show that the mean-square stability of a linear system with impulse response h is equivalent to Σ|h[n]|² being finite, and give the criterion for a rational transfer function.

> **Type:** Theory
> **Answer:** The system is mean-square stable for every bounded input iff Σ_n|h[n]|² < ∞, which by Parseval is equivalent to ∫|H(f)|²df < ∞. For a rational H(z) this holds iff every pole lies strictly inside the unit circle; the margin 1 − max|pole| controls how close to instability the system is.
> **Solution:** Output variance is Var(y) = ∫S_x(f)|H(f)|²df, which is finite for every bounded input spectrum only if |H|² is integrable, i.e. the impulse response is square-summable. This is the BIBO-stable condition and, for an LTI system, it is also mean-square stable. For rational systems Parseval's theorem turns the condition into a statement about poles: an unstable or marginally stable pole makes the impulse response grow or fail to decay, so the sum of squares diverges. A pole exactly on the unit circle gives a non-decaying oscillation and is also excluded.
> **Key point:** Mean-square stability ⟺ Σ|h[n]|² < ∞ ⟺ ∫|H|²df < ∞; for rational H(z) this is exactly "all poles strictly inside the unit circle".

### Q210. Compute the output noise power of an LTI system with white input of PSD S₀ and transfer function H, expressing it in terms of the impulse response.

> **Type:** Numerical
> **Answer:** σ_y² = ∫S₀|H(f)|²df = S₀Σ_n|h[n]|². For h[n] = a^nu[n] this is S₀/(1 − a²); for the two-tap average h[n] = (δ[n] + δ[n−1])/2 it is S₀/2.
> **Solution:** With S_X(f) = S₀, the output PSD is S₀|H(f)|² and the total power is its integral, which by Parseval equals S₀ times the sum of squared impulse-response samples. For h[n] = a^nu[n] the sum is the geometric series Σa^{2n} = 1/(1−a²), so a = 0.5 gives 1.333S₀. For h = (1/2, 1/2) the sum of squares is 1/4 + 1/4 = 1/2, and the two-tap average halves white noise power, which is the simplest illustration of averaging as noise reduction.
> **Key point:** σ_y² = S₀Σ_n h[n]²; for a one-pole with a = 0.5 that is 1.333S₀, and for a two-tap (1/2, 1/2) average it is S₀/2.

### Q211. Give the spectrum of the output of a system with transfer function H(f) driven by a process with spectrum S_X(f), and state the three properties of the output spectrum.

> **Type:** Theory
> **Answer:** S_Y(f) = |H(f)|²S_X(f). The output spectrum is non-negative, real, and even (for a real process and a real-coefficient system); its integral is the output power; and it is bounded above by max|H|² times the input spectrum.
> **Solution:** Filtering is a linear operation, so the output spectrum is the input spectrum weighted by the power gain of the system. The three properties follow from the corresponding properties of the input and of |H|². The bound S_Y ≤ max|H|²S_X shows the system cannot create spectral components where the input has none, and equality S_Y = S_X requires |H(f)| = 1 on the support of S_X, i.e. the system must be all-pass over the occupied band. This is the spectral statement of the fact that a filter reshapes but does not invent frequency content.
> **Key point:** S_Y = |H|²S_X, so the output spectrum is real, non-negative and even, cannot exceed max|H|²·S_X, and equals the input only where |H| = 1.

### Q212. Show that the spectrum of the derivative of a differentiable WSS process is (2πf)² times the original spectrum, and give the mean-square differentiability condition.

> **Type:** Theory
> **Answer:** S_Ẋ(f) = (2πf)²S_X(f) and R_ẊẊ(τ) = −R_X″(τ). The mean-square derivative exists exactly when R_X(τ) is twice differentiable, equivalently when ∫(2πf)²S_X(f)df is finite.
> **Solution:** Differentiation multiplies the transform by j2πf, and since the autocorrelation is the inverse transform, the same operation in time gives R_ẊẊ(τ) = −R_X″(τ). The existence condition follows from the mean-square derivative being a random variable with finite second moment, which by Parseval is the stated integral. For ideal white noise S_X = σ² is flat, so ∫(2πf)²σ²df diverges and no mean-square derivative exists; band-limiting the source is what restores differentiability.
> **Key point:** S_Ẋ(f) = (2πf)²S_X(f), R_ẊẊ(τ) = −R_X″(τ); the derivative exists in the mean square iff ∫(2πf)²S_X df < ∞, which fails for ideal white noise since its flat spectrum makes the integral diverge.

### Q213. A process is the output of a first-order recursion y[n] = ay[n−1] + x[n] driven by white noise of variance σ_x². Show that its spectrum has its maximum at f = 0 and find the −3 dB point for a = 0.9.

> **Type:** Numerical
> **Answer:** S_Y(f) = σ_x²/(1 + a² − 2a cos 2πf), maximised at f = 0 where it equals σ_x²/(1−a)². The −3 dB point satisfies 1 + a² − 2a cos 2πf₃ = 2(1−a)², so cos 2πf₃ = (3a² − 2a − 1)/(2a); for a = 0.9 this is (2.43 − 1.8 − 1)/1.8 = −0.2056, giving f₃ = arccos(−0.2056)/(2π) ≈ 0.2830 cycles per sample.
> **Solution:** The denominator 1 + a² − 2a cos 2πf = (1−a)² + 2a(1 − cos 2πf) is smallest when cos 2πf = 1, that is at f = 0, so the spectrum peaks at DC and decays monotonically to f = 0.5. Setting the spectrum to half its peak value σ_x²/(1−a)² gives the stated cosine condition, and with a = 0.9, arccos(−0.2056) = 1.7779 rad, so f₃ = 1.7779/6.2832 = 0.28297 cycles per sample. The output variance is σ_x²/(1 − a²) = 5.263σ_x², much larger than the peak spectral density because the spectrum is spread over a band of order (1−a).
> **Key point:** S_Y(f) = σ_x²/(1 + a² − 2a cos 2πf) peaks at DC with value σ_x²/(1−a)²; for a = 0.9 the −3 dB point is f₃ ≈ 0.283 cycles/sample and the total output power is 5.263σ_x².

### Q214. Which of the following statements about power spectral densities are true?

> **Type:** MSQ (GATE-2)
> **Answer:** Statements (a), (b), (c) and (e) are true; (d) is false. (Options a, b, c, e)
>
> (a) The PSD of a real WSS process is a real, non-negative function.
> (b) The PSD of a process with a nonzero mean contains an impulse at zero frequency.
> (c) White noise has a constant PSD.
> (d) A process with a flat PSD has zero variance.
> (e) The area under the PSD equals the mean-square value of the process.
> **Solution:** (a) holds by the realness and evenness of R_X combined with positive semi-definiteness. (b) holds because R_X(τ) = μ² + C_X(τ) and the constant μ² transforms to a Dirac impulse at DC of weight μ². (c) is the definition of white noise. (d) is false: a flat PSD of height S₀ gives variance S₀ by the area rule, so flatness is about shape, not level. (e) is the Wiener–Khinchin relation at zero lag, and it is the practical check that a computed spectrum is correctly normalised.
> **Key point:** (a), (b), (c) and (e) are true. A flat PSD of height S₀ has variance S₀, not zero — the area, not the shape, carries the power.

---

## Section 10. Mean-square stability, white-noise filtering and output noise power (Q215–Q234)

### Q215. State the condition for an LTI system to be mean-square stable, and distinguish it from asymptotic mean-square stability.

> **Type:** Theory
> **Answer:** Mean-square stability means E|y(t)|² stays bounded for every input with bounded second moments, which holds iff Σ|h[n]|² < ∞ (equivalently ∫|H(f)|²df < ∞). Asymptotic mean-square stability additionally requires the transient to vanish, i.e. the impulse response to tend to zero as n → ∞.
> **Solution:** The variance of the output is Var(y) = ∫S_x(f)|H(f)|²df, so boundedness for every bounded input spectrum requires |H|² to be integrable, which is exactly the square-summability of h. The two notions coincide for stable rational systems but differ in general: an input-output stable system can have a persistent response to certain inputs, while asymptotic stability demands the memory fade away. The distinction matters in control, where a marginally stable integrator is input-output stable for bounded inputs yet does not settle.
> **Key point:** Mean-square stability ⟺ Σ|h|² < ∞; asymptotic stability additionally needs h[n] → 0. The two coincide for rational systems with all poles strictly inside the unit circle.

### Q216. Show that a first-order recursion y[n] = ay[n−1] + x[n] is mean-square stable iff |a| < 1, and compute the steady-state output variance for white input.

> **Type:** Numerical
> **Answer:** Stable iff |a| < 1, since h[n] = a^nu[n] and Σ|h|² = 1/(1−a²). The steady-state variance is σ_x²/(1−a²), so for a = 0.5 it is 1.3333σ_x².
> **Solution:** The recursion has impulse response h[n] = a^nu[n], whose squares sum to the geometric series Σa^{2n}, convergent exactly when |a| < 1. The output variance follows from the white-input formula σ_y² = σ_x²Σh² = σ_x²/(1−a²). Directly, the recursion y[n] = ay[n−1] + x[n] gives σ_y² = a²σ_y² + σ_x² by independence of x[n] and y[n−1], so σ_y²(1−a²) = σ_x² and the same result follows. For a = 0.5, 1/(1−0.25) = 1.3333.
> **Key point:** A one-pole recursion is mean-square stable iff |a| < 1, and the white-input output variance is σ_x²/(1−a²) — 1.3333σ_x² for a = 0.5.

### Q217. Derive the noise gain of a second-order section y[n] = a₁y[n−1] − a₂y[n−2] + x[n] driven by white noise of variance σ_x², and evaluate it for a₁ = 0.8, a₂ = 0.15.

> **Type:** Numerical
> **Answer:** With the impulse response h[0] = 1, h[1] = a₁, h[n] = a₁h[n−1] − a₂h[n−2], the noise gain is Σ_n h[n]² = (1 + a₂)/((1 − a₂)((1 + a₂)² − a₁²)). For a₁ = 0.8, a₂ = 0.15 this is 1.15/(0.85 × 0.6825) = 1.982, so σ_y² = 1.982σ_x².
> **Solution:** A one-step recursion expands as the convolution of geometric sequences, so with p, q the two poles of 1/(1 − a₁z⁻¹ + a₂z⁻²) the impulse response is h[n] = (p^{n+1} − q^{n+1})/(p − q). Summing its square gives Σh² = [(1−p²)(1−q²)]/((1−pq)²(p−q)²), which on substituting p + q = a₁ and pq = a₂ reduces to (1 + a₂)/((1 − a₂)((1 + a₂)² − a₁²)). Checking the arithmetic for a₁ = 0.8, a₂ = 0.15: (1 + a₂)² − a₁² = 1.3225 − 0.64 = 0.6825, and 1.15/(0.85 × 0.6825) = 1.15/0.580125 = 1.9823. Direct summation of the recursion confirms it: h = 1, 0.8, 0.49, 0.272, 0.1441, …, whose squares sum to 1.9823. The denominator vanishes when a pole reaches the unit circle, which is where the gain diverges.
> **Key point:** The biquad noise gain is Σh² = (1 + a₂)/((1 − a₂)((1 + a₂)² − a₁²)), which is 1.982 for a₁ = 0.8, a₂ = 0.15 and blows up as either pole approaches the unit circle.

### Q218. A two-pole filter has a repeated pole at 0.5. Find its noise gain and compare it with a filter whose poles are at 0.5 and 0.3, which has the same 3-dB response.

> **Type:** Numerical
> **Answer:** Repeated pole at 0.5 gives h[n] = (n + 1)(0.5)ⁿ, so Σh² = 2.963. Poles at 0.5 and 0.3 give Σh² = 1.982. The repeated-pole filter therefore passes 49.5% more noise for the same signal response.
> **Solution:** For a repeated pole p the impulse response of 1/(1 − pz⁻¹)² is h[n] = (n + 1)pⁿ, and the noise gain is the weighted sum Σ(n + 1)²(p²)ⁿ = (1 + p²)/(1 − p²)³. With p = 0.5 this is 1.25/0.421875 = 2.9630. For the two distinct poles 0.5 and 0.3 the recursion coefficients are a₁ = 0.8, a₂ = 0.15, so the closed form of the previous question gives 1.15/(0.85 × 0.6825) = 1.9823, confirmed by summing h = 1, 0.8, 0.49, 0.272, 0.1441, … . The ratio 2.9630/1.9823 = 1.495, so spreading the poles apart cuts the noise gain by 33.1% while leaving the resonant gain and the 3-dB frequency essentially unchanged, since the signal response depends on the pole locations as a set whereas the noise depends on the weights of the individual decay terms.
> **Key point:** A double pole at 0.5 gives Σh² = 2.963 against 1.982 for poles at 0.5 and 0.3 — 49.5% more noise for the same signal response, which is the basis of pole spreading in biquad design.

### Q219. Give the noise gain of a first-order recursive filter and express it in terms of the pole, then state the design implication as the pole approaches the unit circle.

> **Type:** Numerical
> **Answer:** Noise gain = 1/(1−a²) for a pole at a, so a = 0.9 gives 5.263, a = 0.99 gives 50.25, and a = 0.999 gives 500.25. The gain grows without bound as a → 1, diverging like 1/(2(1−a)).
> **Solution:** The impulse response is h[n] = a^nu[n] and the noise gain is Σh² = Σa^{2n} = 1/(1−a²) = 1/((1−a)(1+a)). Near a = 1 the factor 1+a ≈ 2, so the gain ≈ 1/(2(1−a)); at a = 0.9, 1/(2 × 0.1) = 5, close to the exact 5.263. The design implication is severe: a 10% increase in pole radius from 0.9 to 0.99 multiplies the noise gain by 9.5, so stability margin is expensive in noise, and quantisation of the coefficient near unity translates directly into a large gain error. This is why high-Q biquads are implemented with pole spreading rather than a single near-unit-circle pole.
> **Key point:** A one-pole filter's noise gain is 1/(1−a²) ≈ 1/(2(1−a)) near a = 1; moving the pole from 0.9 to 0.99 multiplies it by 9.5, so stability margin costs noise.

### Q220. Show that a filter's output noise power for white input depends only on the integral of |H(f)|², so two filters with the same integral deliver the same noise.

> **Type:** Theory
> **Answer:** σ_y² = S₀∫|H(f)|²df, a statement about the area under the power-gain curve, not its shape. Hence the noise depends only on the equivalent noise bandwidth, ENBW = ∫|H|²df/|H(0)|², and two filters with equal ENBW pass equal noise regardless of their differing responses.
> **Solution:** Because a white input has no spectral structure, every frequency carries the same power density, so the output power is the constant S₀ times the total area of the power gain. A brickwall of width B and a two-pole filter with ENBW = B give identical output noise despite completely different |H|² shapes, though they differ in how they distort the signal. The engineering consequence is that a filter's noise performance is a single number, and only its signal response requires the full curve.
> **Key point:** For white input, σ_y² = S₀·ENBW, so noise depends only on the area under |H|², not its shape — filters with equal ENBW are equally noisy.

### Q221. A two-pole low-pass has |H(f)|² = 1/(1 + (f/f_c)⁴) with f_c = 2 kHz. Find its ENBW and output noise power for white input of PSD S₀.

> **Type:** Numerical
> **Answer:** ENBW = (π/√2)f_c = 2.221f_c = 4.443 kHz, so the output noise power is 4.443 × 10³ S₀. A one-pole low-pass at the same corner gives (π/2)f_c = 3.142 kHz, so the two-pole filter admits 1.414 times the noise.
> **Solution:** Substituting u = f/f_c turns the ENBW integral into f_c∫_{−∞}^{∞}du/(1 + u⁴), and the standard contour result is ∫_{−∞}^{∞}du/(1 + u⁴) = π/√2, giving ENBW = 2.2214f_c. With f_c = 2 kHz this is 4.4429 kHz and the output variance is 4.4429 × 10³ S₀, since for a DC-normalised filter σ_y² = S₀·ENBW. The one-pole comparison follows from ∫du/(1 + u²) = π, giving (π/2)f_c = 1.5708f_c = 3.1416 kHz, and the ratio 2.2214/1.5708 = 1.414. The extra noise buys the faster roll-off: beyond f_c the two-pole response falls as f⁻⁴ instead of f⁻², so the skirts that carry the noise are thinner in one sense but the area under them is larger.
> **Key point:** ENBW of 1/(1 + (f/f_c)⁴) is (π/√2)f_c = 2.221f_c, against 1.571f_c for a one-pole at the same corner — 1.414 times the noise for a 12 dB/octave roll-off.

### Q222. Derive the output autocorrelation of a system with impulse response h driven by a process with autocorrelation R_x, and state the white-input special case.

> **Type:** Theory
> **Answer:** R_y(τ) = ∫∫h(u)h(v)R_x(u − v)dudv, the triple convolution R_y = h ⋆ h^{⊖} ⋆ R_x. For white input R_x(τ) = σ_x²δ(τ), this reduces to R_y(τ) = σ_x²(h ⋆ h^{⊖})(τ).
> **Solution:** Substitute the convolution for y(t) and y(t+τ) into the definition of R_y, then apply the stationarity of R_x to identify the double integral. The white-input case collapses the integral to a delta and leaves the autocorrelation of the filter, so the output spectrum is |H|²S₀. The result is the frequency-domain statement in disguise, since the triple convolution transforms to S_y = |H|²S_x.
> **Key point:** R_y(τ) = ∫∫h(u)h(v)R_x(u−v)dudv, a triple convolution in time and a product S_y = |H|²S_x in frequency; white input leaves R_y = σ_x²(h ⋆ h^{⊖}).

### Q223. State the mean-square stability condition in terms of the poles of a rational transfer function, and show that marginal stability is insufficient.

> **Type:** Theory
> **Answer:** A rational system is mean-square stable iff all poles lie strictly inside the unit circle. A pole on the unit circle is marginally stable: the impulse response does not decay, Σ|h|² diverges, and the output variance is unbounded for a white input.
> **Solution:** Each pole of modulus r contributes a term rⁿ to the impulse response, so its squares contribute r^{2n}, whose sum converges iff r < 1. A pole at r = 1 gives a non-decaying oscillation (or a step, for a double pole at the origin or a pole at 1), so the sum of squares diverges and the noise gain is infinite. The classic example is the ideal integrator H(z) = 1/(1 − z⁻¹): its impulse response is the unit step, and white noise through it has unbounded output variance. In practice a pole at 0.99 is used instead, trading a large but finite gain of 50.25 for a bounded output.
> **Key point:** Mean-square stability requires all poles strictly inside the unit circle; a unit-circle pole gives an infinite noise gain, so marginal stability is useless for noise purposes.

### Q224. A first-order high-pass filter H(f) = j2πf/(j2πf + 1/RC) is driven by white noise of PSD S₀. Find the total output power and comment on its divergence.

> **Type:** Numerical
> **Answer:** σ_y² = ∫S₀(2πfRC)²/(1 + (2πfRC)²)df, which diverges, because the integrand tends to S₀ as |f| → ∞. Ideal white noise through an ideal differentiator has infinite output power; any practical roll-off of the high-pass restores finiteness.
> **Solution:** The power gain is 1 − 1/(1 + (2πfRC)²), so σ_y² = S₀[∫df − ∫df/(1 + (2πfRC)²)] — and the first integral over the infinite frequency axis is divergent. The high-pass passes the full white-noise floor at high frequency, so without a roll-off there is no upper band limit to stop the integral. Physically this reflects that ideal white noise has unbounded bandwidth and power at every frequency, and an ideal differentiator amplifies without bound as frequency grows. Real filters are band-limited, and a practical one-pole high-pass combined with the source's own band limit gives finite noise.
> **Key point:** An ideal high-pass on ideal white noise gives infinite output power, since |H| → 1 at high frequency and the white spectrum never ends; real systems need both a roll-off and a source band limit.

### Q225. Find the ENBW of a cascade of two one-pole low-passes with corner frequencies f₁ and f₂, and evaluate it for f₁ = 1 kHz, f₂ = 2 kHz.

> **Type:** Numerical
> **Answer:** ENBW = πf₁f₂/(f₁ + f₂), which is 2.094 kHz for f₁ = 1 kHz and f₂ = 2 kHz, so the output noise power is 2.094 × 10³ S₀. Two poles at the same corner f₀ give πf₀/2, half the single-pole value πf₀.
> **Solution:** With |H(f)|² = 1/((1 + (f/f₁)²)(1 + (f/f₂)²)), partial fractions give f₁²f₂²/((f₁² + f²)(f₂² + f²)) = f₁²f₂²/(f₂² − f₁²) · [1/(f₁² + f²) − 1/(f₂² + f²)], and since ∫_{−∞}^{∞}df/(f² + a²) = π/a the two terms combine to πf₁f₂(f₂ − f₁)/((f₂ − f₁)(f₁ + f₂)) = πf₁f₂/(f₁ + f₂). Substituting f₁ = 1 kHz and f₂ = 2 kHz gives π × 2/3 kHz = 2.0944 kHz, and numerical quadrature of the same integrand confirms it. The equal-corner case is the limit f₁ = f₂ = f₀, giving πf₀/2 = 1.571f₀, exactly half of the single-pole ENBW πf₀ — so a second pole at the same corner halves the noise. Note that the ±3-dB bandwidth behaves differently: it narrows by only about 0.6, falling from 1.571f₀ to 1.287f₀ for equal corners, which is a good illustration that the ENBW and the 3-dB bandwidth are not proportional.
> **Key point:** The ENBW of two cascaded one-pole low-passes is πf₁f₂/(f₁ + f₂), so equal corners at f₀ give 1.571f₀, half the single-pole value — while the 3-dB bandwidth falls by only a factor of 1.22.

### Q226. Show that for a stable LTI system the output variance is bounded by σ_x²·sup_f|H(f)|², and state when the bound is tight.

> **Type:** Theory
> **Answer:** Var(y) = ∫S_x(f)|H(f)|²df ≤ sup_f|H(f)|²∫S_x(f)df = σ_x²·sup|H|². The bound is tight when S_x is concentrated where |H| attains its maximum, which for white input never happens unless |H| is flat, in which case equality holds exactly.
> **Solution:** Since |H(f)|² ≤ sup|H|² pointwise, integrating against the non-negative S_x gives the bound. For a general coloured input the supremum need not be attained anywhere the input has power, so the bound can be loose; for a filter matched to a narrowband input, the output noise can be far below it. The engineering use is as a worst-case figure of merit that needs no knowledge of the input spectrum.
> **Key point:** Var(y) ≤ σ_x²·max_f|H(f)|² always, with equality only if the input spectrum lies entirely where |H| is at its peak — impossible for white input unless |H| is flat.

### Q227. Give the noise gain of a moving-average filter of length N, h[n] = 1/N for n = 0, …, N−1, driven by white noise of variance σ_x².

> **Type:** Numerical
> **Answer:** Σh² = N(1/N)² = 1/N, so σ_y² = σ_x²/N. The output spectrum is S₀(1/N)²|D_N(e^{jω})|² with |D_N|² = [sin(Nω/2)/sin(ω/2)]², a Dirichlet kernel.
> **Solution:** The sum of squared coefficients of a flat-weight average is N × (1/N²) = 1/N, so averaging N independent samples reduces white noise power by exactly a factor of N, matching the sample-mean result. In frequency, H(e^{jω}) = (1/N)(1 − e^{−jNω})/(1 − e^{−jω}), whose magnitude squared is the Dirichlet kernel divided by N²: it peaks at N/N = 1 (unit DC gain, as required for a DC-preserving averager) and has sidelobes of relative height about 13%, which is the leakage that distinguishes this simple filter from a windowed one.
> **Key point:** An N-point moving average gives σ_y² = σ_x²/N and frequency response (1/N)·D_N(ω); its gain peaks at 1 for preserving DC and falls as sinc², with sidelobes near −17.3 dB.

### Q228. Show that a matched filter maximises the output SNR for a signal in white noise, and state the resulting SNR.

> **Type:** Theory
> **Answer:** For a signal s(t) observed in white noise of PSD N₀/2, the filter h(t) = s(T − t) matched to the signal maximises SNR, giving SNR_out = E_s/N₀ = ∫s²(t)dt/(N₀/2) = 2E_s/N₀ for the two-sided convention, where E_s is the signal energy.
> **Solution:** Maximising the output signal-to-noise ratio E[|∫h s|²]/(∫S_n|H|²df) by varying h is a variational problem whose solution is h(t) ∝ s(T−t), the time-reversed and delayed signal. The result is the matched-filter theorem: the optimum is the convolution of the received waveform with a time-reversed replica of the known signal, which is also the operation that whitens the effective channel. The price is that the output is a sinc-like pulse, so a matched filter maximises SNR at the cost of an unresolved pulse shape, which is why practical detectors also impose a bandwidth constraint.
> **Key point:** A matched filter h(t) = s(T−t) maximises output SNR for a known signal in white noise, giving SNR = 2E_s/N₀; it whitens the effective channel at the cost of sinc-shaped output resolution.

### Q229. Show that a one-pole low-pass with corner f_c = 1/(2πRC) has ENBW = (π/2)f_c, and interpret the effect of reducing RC.

> **Type:** Numerical
> **Answer:** ENBW = ∫|H(f)|²df = 1/(4RC) = (π/2)f_c, so for f_c = 1 kHz the ENBW is 1.571 kHz and the output noise power is 1.571 × 10³ S₀. Halving RC halves the noise linearly, while the DC gain stays at 1.
> **Solution:** With H(f) = 1/(1 + jf/f_c), the power gain is |H|² = 1/(1 + (f/f_c)²) and substituting u = f/f_c gives ENBW = f_c∫_{−∞}^{∞}du/(1 + u²) = πf_c/2 = 1.5708f_c, which is also 1/(4RC) since f_c = 1/(2πRC). For f_c = 1 kHz that is 1.5708 kHz, and since the filter has |H(0)| = 1 the ENBW in hertz equals the output noise power per unit input density. The interpretation of shrinking RC is the apparent paradox that must be understood carefully: the DC gain is fixed at 1, so nothing "amplifies" the noise, yet the output power falls with RC simply because the filter admits a narrower band. The floor is the noise of the ideal white input itself, which has infinite power at any nonzero bandwidth, so the output variance being finite for every finite f_c is a statement about the filter, not about the source.
> **Key point:** A one-pole low-pass has ENBW = (π/2)f_c = 1/(4RC) = 1.571f_c; halving RC halves the output noise because the admitted band narrows, not because the gain falls.

### Q230. Derive the condition for the output of a linear system driven by white noise to be free of a DC component, and relate it to the high-pass case.

> **Type:** Theory
> **Answer:** The output DC component is E[y] = H(0)E[x], so a DC-free output requires either E[x] = 0 or H(0) = 0. Since white noise has zero mean, the output DC is zero for any system, but the output power at DC is governed by |H(0)|², and a high-pass filter with H(0) = 0 suppresses the DC bin entirely.
> **Solution:** Linearity gives E[y(t)] = ∫h(u)E[x(t−u)]du = m_x∫h = m_xH(0). For a zero-mean input this is zero regardless of the system, which is why white noise produces no DC output. The frequency-domain statement is that the output PSD at f = 0 is |H(0)|²S_x(0), so a system with a zero at DC removes any DC content in the input — the defining property of a high-pass or a differentiator, and the reason AC coupling exists in signal chains.
> **Key point:** E[y] = H(0)E[x]; for a zero-mean input the output mean is zero regardless of H, and |H(0)| = 0 (a high-pass) additionally removes any DC spectral content of the input.

### Q231. State the definition of the noise figure of a two-port and express it in terms of the source and total output noise.

> **Type:** Theory
> **Answer:** F = (S_out/(G·S_src)) = 1 + S_e/G, where S_e is the amplifier's own input-referred noise and S_src the available source noise density. F is a power ratio, always ≥ 1, and equals the input-referred SNR degradation: SNR_out = SNR_in/F.
> **Solution:** Referring the amplifier's internally added noise to the input gives the total input-referred density S_e + S_src, and dividing by the available source density gives the degradation factor F = (S_e + S_src)/S_src. This makes F interpretable as the extra noise the amplifier contributes relative to the ideal noiseless case, and the cascade rule F_total = F₁ + (F₂ − 1)/G₁ shows why the first stage's gain dominates a cascade's noise figure. Friis's formula is why a low-noise preamplifier ahead of a noisy power amplifier improves the system figure even though the total gain is unchanged.
> **Key point:** F = 1 + S_e/S_src is a power ratio ≥ 1 giving SNR degradation; in cascade, F_total = F₁ + (F₂−1)/G₁, so the first stage's noise figure and gain dominate.

### Q232. A two-stage amplifier has F₁ = 1.5, G₁ = 100, F₂ = 10. Compute the cascade noise figure and the equivalent input noise referred to stage 1.

> **Type:** Numerical
> **Answer:** F_total = 1.5 + (10 − 1)/100 = 1.5 + 0.09 = 1.59. With a source density S_src, the total input-referred noise is F_total·S_src = 1.59 S_src, and stage 2's own contribution referred to stage 1 is only 0.09 S_src despite F₂ = 10.
> **Solution:** Friis's formula gives F_total = F₁ + (F₂ − 1)/G₁ = 1.5 + 9/100 = 1.59. The dominant term is stage 1's own noise, 0.5 S_src; stage 2's noise of 9 S_src referred to its own input is divided by stage 1's gain of 100 to become 0.09 S_src at the system input. The result shows that a 10× noisy second stage contributes only 6% of the total input-referred noise because it is preceded by 20 dB of gain, which is the practical justification for putting the low-noise stage first.
> **Key point:** F_total = 1.5 + 9/100 = 1.59: stage 2's F = 10 contributes just 0.09 because of stage 1's gain of 100, so the first stage dominates the cascade noise figure.

### Q233. State the definition of the equivalent noise bandwidth and explain why it is used in place of the 3-dB bandwidth.

> **Type:** Theory
> **Answer:** ENBW = ∫|H(f)|²df/|H(0)|² is the width of the ideal brickwall filter that passes the same total noise power. It, not the 3-dB bandwidth, determines the output noise, because the noise depends on the whole area under |H|², not on a single frequency at which the response has fallen 3 dB.
> **Solution:** The definition is normalised by the peak gain so a flat-top filter has ENBW equal to its physical width. For a one-pole low-pass, ENBW = 1/(2RC) while the ±3-dB bandwidth is 1/(πRC), so ENBW is π/2 ≈ 1.571 times larger — a one-pole filter passes 57.1% more noise than a brickwall of the same 3-dB width. Two filters with quite different shapes can share an ENBW, and then they are equally noisy, which is exactly the comparison the number is designed to support.
> **Key point:** ENBW = ∫|H|²df/|H(0)|²; for a one-pole it is 1/(2RC), which is 1.571× the ±3-dB bandwidth 1/(πRC) — the reason noise specifications quote ENBW rather than 3-dB bandwidth.

### Q234. An amplifier has gain G = 10, input noise density 1 nV²/Hz, and is fed a source of density 2 nV²/Hz. With a total two-sided bandwidth of 10⁵ Hz, find the input- and output-referred total noise and the noise figure.

> **Type:** Numerical
> **Answer:** Total input-referred density = 2 + 1 = 3 nV²/Hz, so over 10⁵ Hz the input-referred noise is √(3 × 10⁻¹⁸ × 10⁵) = 5.477 × 10⁻⁷ V = 0.5477 µV rms. Output-referred is 10× that, 5.477 µV rms. The noise figure is F = 3/2 = 1.5, or 1.76 dB.
> **Solution:** The amplifier's own 1 nV²/Hz adds to the source's 2, giving 3 nV²/Hz referred to the input, so the noise figure is the ratio of total to source, 3/2 = 1.5; in decibels 10log₁₀(1.5) = 1.76 dB. Multiplying the density by the total two-sided bandwidth 2B = 10⁵ Hz gives 3 × 10⁻¹⁸ × 10⁵ = 3 × 10⁻¹³ V², whose square root is 5.477 × 10⁻⁷ V. The gain of 10 then gives 5.477 µV at the output. The bandwidth cancels out of the noise figure, so a 1 nV²/Hz amplifier on a 2 nV²/Hz source costs 1.76 dB of SNR whatever the bandwidth — which is why noise figure, unlike absolute noise voltage, is a bandwidth-independent specification.
> **Key point:** Input-referred total = (S_src + S_amp)·2B = 0.5477 µV rms, output-referred = G× that = 5.477 µV rms, and F = 1.5 = 1.76 dB; the 1 nV²/Hz amplifier costs 1.76 dB of SNR on a 2 nV²/Hz source.

---

## Quick revision — Probability & Random Processes

- Independence adds: P(A∩B) = P(A)P(B); for n mutually exclusive exhaustive events ΣP(Aᵢ) = 1, and Bayes inverts to P(A|B) = P(B|A)P(A)/P(B).
- Conditional expectation obeys the tower property E[X|Y] then E[·] recovers E[X]; law of total variance Var(X) = E[Var(X|Y)] + Var(E[X|Y]).
- Reliability: series P = Πpᵢ, parallel P = 1 − Π(1−pᵢ), and a redundant pair with a 2-out-of-3 voter gives p²(3−2p).
- CDF relations: F(x) = P(X ≤ x), survival S(x) = 1 − F(x), density f = F′; the hazard is h(x) = f(x)/S(x) with ∫₀^∞h dx = 1.
- Moments come from derivatives of the MGF: E[X] = M′(0), E[X²] = M″(0), Var = M″(0) − M′(0)²; the MGF need not exist even when the mean does.
- Bernoulli(p): mean p, var p(1−p), MGF (1−p) + pe^s.
- Binomial(n,p): mean np, var np(1−p); n independent Bernoulli trials, and n→∞ with p→0 at fixed np gives Poisson.
- Geometric(p) on {1,2,…}: mean 1/p, var (1−p)/p², memoryless with P(X>k) = (1−p)^k.
- Negative binomial counting trials to r successes: mean r/p, var r(1−p)/p².
- Poisson(λ): mean λ, var λ — the equality is the defining property; the mode is ⌊λ⌋ (λ−1 also when λ is an integer).
- Uniform(a,b): mean (a+b)/2, var (b−a)²/12, f = 1/(b−a).
- Normal(μ,σ²): MGF e^{μs+σ²s²/2}, mean μ, var σ²; the variance enters as σ², not σ.
- Half-normal from |N(0,σ²)|: mean σ√(2/π) ≈ 0.7979σ, var σ²(1−2/π) ≈ 0.3634σ².
- Exponential(λ): mean 1/λ, var 1/λ², f = λe^{−λx}, memoryless with S(x) = e^{−λx}.
- Gamma(k, rate λ): mean k/λ, var k/λ²; n exponentials sum to Gamma(n, λ), and the chi-square is Gamma(k/2, rate 1/2).
- Weibull(k, λ): mean λΓ(1 + 1/k), var λ²[Γ(1+2/k) − Γ²(1+1/k)]; exponential is the k = 1 case.
- Rayleigh(σ): mean σ√(π/2) ≈ 1.2533σ, var (2−π/2)σ² ≈ 0.4292σ²; envelope of two N(0,σ²) components.
- Cauchy: mean and variance both undefined, and the MGF does not exist for any s ≠ 0 — the standard trap.
- Laplace(a,b): mean a, var 2b², obtained as a difference of independent exponentials.
- Two independent Rayleighs sum: mean σ√(2π) ≈ 2.5066σ, var (4−π)σ² ≈ 0.8584σ², with a single error-function density.
- Joint density: f_{X,Y} = f_{X|Y}f_Y, marginals by integration, and independence iff f_{X,Y} = f_Xf_Y (or F_{X,Y} = F_XF_Y).
- Cov(X,Y) = E[XY] − E[X]E[Y]; zero covariance means uncorrelated, not independent, and independence ⇒ zero covariance is one-way.
- A bivariate Gaussian has independent components iff the cross-covariance is zero, since the joint density then factorises — unlike the general case.
- Transformations: for Y = g(X) monotone, f_Y(y) = f_X(g⁻¹(y))|d g⁻¹/dy|; with several pre-images, sum over all of them.
- Sums: independent variables convolve, f_{X+Y} = f_X ∗ f_Y; the characteristic function multiplies, and CLT makes the sum near-normal for large n.
- Linear systems: E[y] = ∫h E[x], and for input mean m and variance σ² the output variance is the double sum ΣΣh[n]h[m]R_x[n−m].
- White input R_x = σ²δ gives Var(y) = σ²Σh[n]², so the noise gain is the sum of squared impulse-response samples.
- Stationarity: WSS needs constant mean and R_x(t₁,t₂) depending only on t₂−t₁; strict-sense needs the full joint law, which for a Gaussian process follows from WSS.
- A random constant X[n] = Z is WSS but not ergodic, since the time average is always Z while the ensemble mean is E[Z] — the canonical non-ergodic case.
- A deterministic periodic process is WSS and both mean- and correlation-ergodic; periodicity does not prevent ergodicity.
- Var(X̄_N) = σ²/N + (1/N)Σ_{k≠0}(1−|k|/N)R(k) → 0 only when Σ_k|R(k)| < ∞.
- PSD = Fourier transform of the autocorrelation; it is real, even and non-negative, and ∫S df = R(0) = E[X²] is the total power.
- A nonzero mean contributes a DC impulse of weight m²; R(∞) = 0 is not a universal requirement, so the random-constant case is legitimate.
- Filtering: S_Y = |H|²S_X, so a filter reshapes but never invents spectral content, and S_Y = S_X needs |H| = 1 over the occupied band.
- White noise S = σ² is flat, so its mean-square derivative fails: ∫(2πf)²σ²df diverges, and S_Ẋ = (2πf)²S_X.
- AR(1): R[m] = σ²a^{|m|}/(1−a²) with S(f) = σ²/(1 + a² − 2a cos 2πf), the Poisson kernel peaking at DC; MA(1) is its dual with a zero at f = 1/2.
- A rational spectrum corresponds to an ARMA model, not generally an all-pole AR model; a pure AR spectrum has no zeros.
- Random-phase sinusoid: S = ¼[δ(f−f₀)+δ(f+f₀)], power ½, and no DC line because E[X] = 0.
- ENBW = ∫|H|²df/|H(0)|² is the brickwall width passing the same noise; a one-pole low-pass gives ENBW = (π/2)f_c = 1.571f_c against a −3 dB width of 1/(πf_c).
- Two cascaded one-pole low-passes have ENBW = πf₁f₂/(f₁+f₂); equal corners halve the single-pole value.
- Mean-square stability ⟺ Σ|h[n]|² < ∞, which for rational H(z) means all poles strictly inside the unit circle; a unit-circle pole gives infinite noise gain.
- Pole spreading: a double pole at 0.5 gives Σh² = 2.963 against 1.982 for poles at 0.5 and 0.3, 49.5% more noise for the same signal response.
- Biquad noise gain: Σh² = (1+a₂)/((1−a₂)((1+a₂)²−a₁²)) for y[n] = a₁y[n−1] − a₂y[n−2] + x[n]; one-pole case 1/(1−a²) = 5.263 at a = 0.9.
- Noise figure F = (S_src + S_amp)/S_src ≥ 1 is a bandwidth-independent SNR degradation, and in cascade Friis gives F_total = F₁ + (F₂−1)/G₁.
- Matched filter h(t) = s(T−t) maximises output SNR for a known signal in white noise, giving SNR = 2E_s/N₀ at the cost of sinc-shaped resolution.
