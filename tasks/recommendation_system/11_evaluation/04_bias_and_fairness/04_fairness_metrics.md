# Fairness Metrics

## Overview

Fairness in recommendation systems ensures that recommendations do not systematically disadvantage individuals or groups based on protected attributes such as race, gender, age, or socioeconomic status. Fairness is not a single concept—there are multiple, sometimes conflicting, definitions depending on who is being protected (users, providers, items) and what aspect of fairness is prioritized.

## Demographic Parity

### Definition

Demographic parity (also called statistical parity or disparate impact) requires that the recommendation outcomes be independent of the protected attribute:

```
P(recommended | group A) = P(recommended | group B)
```

### In Recommendation Context

```
P(item_i recommended to user | gender = male) = P(item_i recommended to user | gender = female)
```

### Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| **Demographic Parity Difference** | \|P(recommended \| A) - P(recommended \| B)\| | 0 |
| **Disparate Impact Ratio** | P(recommended \| A) / P(recommended \| B) | 1.0 (or 0.8–1.25 acceptable) |

### Limitations

- **Ignores qualifications**: Treats all group members as interchangeable
- **Ignores preferences**: May force recommendations that don't match genuine preferences
- **Zero-sum framing**: Improving fairness for one group may require reducing it for another
- **Doesn't address quality**: A system can satisfy demographic parity while providing low-quality recommendations to all groups

## Equalized Odds

### Definition

Equalized odds requires that the model's error rates are equal across protected groups:

```
P(positive prediction | group A, true_label) = P(positive prediction | group B, true_label)
```

This decomposes into:
- **Equal true positive rates** (equal opportunity): P(recommended | actually relevant, group A) = P(recommended | actually relevant, group B)
- **Equal false positive rates**: P(recommended | not relevant, group A) = P(recommended | not relevant, group B)

### Equal Opportunity

A relaxed version that only requires equal true positive rates:

```
P(predicted positive | actually positive, group A) = P(predicted positive | actually positive, group B)
```

This ensures that qualified individuals from all groups have equal probability of being recommended.

### Application to Recommendations

| Scenario | Equalized Odds Application |
|----------|---------------------------|
| Job recommendations | Ensure qualified candidates from all demographics have equal probability of being recommended |
| Content recommendations | Ensure engaging content from diverse creators receives equal exposure |
| Product recommendations | Ensure products from diverse sellers are recommended at equal rates given relevance |

## Calibration Across Groups

### Definition

A model is calibrated across groups if, for a given predicted score, the actual probability of the positive outcome is the same across groups:

```
P(positive | score = s, group A) = P(positive | score = s, group B) for all s
```

### Calibration Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| **Expected Calibration Error (ECE)** | Σ (bins) \|accuracy(bin) - confidence(bin)\| × (bin_size / n) | 0 |
| **Group-specific ECE** | ECE computed separately per group | Equal across groups |
| **Maximum Calibration Difference** | max_s \|P(pos\|s,A) - P(pos\|s,B)\| | 0 |

### Why Calibration Matters

- A model that assigns high scores to items for group A but low scores for group B, even when both groups have similar preferences, violates calibration
- Calibration ensures that score magnitudes have consistent meaning across groups

## Individual Fairness

### Definition

Individual fairness requires that similar individuals receive similar recommendations:

```
d(f(x₁), f(x₂)) ≤ L × d(x₁, x₂)
```

Where:
- f is the recommendation function
- d is a task-specific distance metric
- L is the Lipschitz constant

### Distance Metric Design

The distance metric must capture meaningful similarity:

| Distance Type | Use Case | Example |
|--------------|---------|---------|
| **User feature distance** | Similar users should get similar recs | Euclidean distance on preference vectors |
| **Item feature distance** | Similar items should have similar recommendation rates | Cosine distance on item embeddings |
| **Task-specific distance** | Distance relevant to the recommendation domain | Semantic similarity for content, price similarity for products |

### Challenges

- Defining the "right" distance metric is domain-specific and subjective
- Lipschitz constant L is hard to estimate in practice
- Satisfying individual fairness is computationally expensive for large item catalogs

## Counterfactual Fairness

### Definition

A recommendation is counterfactually fair if it would remain the same if the individual's protected attribute were different:

```
P(recommend | do(A = a), X = x) = P(recommend | do(A = a'), X = x)
```

Where A is the protected attribute and X are other features.

### Implementation Approach

1. **Train a causal model** that includes the protected attribute and its causal descendants
2. **Predict counterfactual outcomes** by intervening on the protected attribute
3. **Compare** outcomes across counterfactual worlds
4. **Enforce consistency**: Ensure recommendations don't change when the protected attribute changes

### Causal Graph Requirements

```
Protected Attribute (A) → User Features (X) → Recommendation (Y)
                    ↘                    ↗
              Mediator Variables (M)
```

Counterfactual fairness requires blocking all causal paths from A to Y that go through non-justified mediators.

## Fairness-Accuracy Tradeoffs

### The Fundamental Tension

| Fairness Constraint | Accuracy Impact | Typical Tradeoff |
|--------------------|-----------------|-----------------|
| Demographic parity | 1–5% accuracy loss | Moderate |
| Equalized odds | 2–8% accuracy loss | Significant |
| Calibration across groups | 0.5–3% accuracy loss | Mild |
| Individual fairness | 3–10% accuracy loss | Severe |
| Counterfactual fairness | 2–7% accuracy loss | Significant |

### Pareto Frontier

Plot accuracy vs. fairness to find the Pareto-optimal solutions:

```
For each model configuration:
    Compute accuracy (e.g., NDCG@10)
    Compute fairness metric (e.g., demographic parity difference)
    Identify Pareto-optimal points (no other model dominates both)
```

### Multi-Objective Optimization

```
Objective = α × Accuracy + (1-α) × Fairness
```

Where α controls the tradeoff. The optimal α depends on:
- Business requirements
- Regulatory constraints
- Stakeholder preferences
- Domain ethics

## Fairness in Recommendations (Group and Provider Fairness)

### Group Fairness for Users

Ensure that different user groups receive equal quality recommendations:

| Metric | Formula | Application |
|--------|---------|------------|
| **Equalized recommendation quality** | NDCG@K(group A) ≈ NDCG@K(group B) | All groups receive equally good recommendations |
| **Equalized exposure** | Exposure_i(group A) ≈ Exposure_i(group B) | All groups see similar item distributions |
| **Equalized satisfaction** | CSAT(group A) ≈ CSAT(group B) | All groups report equal satisfaction |

### Provider Fairness

Ensure that content creators, sellers, or suppliers receive fair treatment:

| Metric | Definition | Application |
|--------|-----------|------------|
| **Exposure fairness** | Each provider receives proportionate exposure | Marketplace platforms |
| **Popularity fairness** | New/niche providers get minimum exposure | Creator economies |
| **Revenue fairness** | Revenue share proportional to value created | Platform economics |
| **Review fairness** | Reviews reflect quality, not bias | Rating systems |

### Provider Fairness Metrics

```
Provider_Exposure_Share(provider_i) = Views(provider_i) / Total_Views
Provider_Revenue_Share(provider_i) = Revenue(provider_i) / Total_Revenue
```

#### The Moritz-Hardt Fairness Framework for Providers

```
E_i / E_total ≥ (1/|providers|) × min(1, |providers| × S_i / S_total)
```

Where E_i is the exposure of provider i and S_i is the provider's quality-weighted supply.

### Intersectional Fairness

Consider fairness across multiple protected attributes simultaneously:

```
Fairness(A = race, B = gender): Ensure fairness for each intersection
例如: Black women, Asian men, etc. (not just "Black" and "women" separately)
```

Intersectional fairness is harder to achieve because:
- Subgroups are smaller, making statistical measurement harder
- Different protected attributes may interact in complex ways
- Multiple fairness constraints may conflict

## Reporting Fairness Results

### Fairness Dashboard

| Metric | Group A | Group B | Group C | Difference | Threshold |
|--------|---------|---------|---------|-----------|-----------|
| Exposure rate | 0.32 | 0.29 | 0.31 | 0.03 | < 0.05 |
| NDCG@10 | 0.45 | 0.43 | 0.44 | 0.02 | < 0.05 |
| Satisfaction (CSAT) | 4.2 | 4.0 | 4.1 | 0.2 | < 0.3 |
| Diverse item % | 25% | 22% | 24% | 3% | < 5% |

### Fairness Audit Frequency

| Audit Type | Frequency | Scope |
|-----------|----------|-------|
| Automated fairness checks | Per model training cycle | Quantitative metrics |
| Comprehensive fairness audit | Quarterly | All fairness dimensions |
| External fairness review | Annually | Third-party assessment |
| Incident-driven audit | As needed | Specific fairness concerns |
