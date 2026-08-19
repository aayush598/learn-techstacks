# Selection Bias

## Overview

Selection bias in recommendation systems occurs when the data used for training, evaluation, or analysis is not representative of the true population of user preferences. Unlike position bias (which biases what users click), selection bias affects which items are shown to users in the first place, creating a fundamental disconnect between observed behavior and true preferences. This is one of the most challenging biases in recommendation systems because it corrupts the very data that models learn from.

## Exposure Bias

### Definition

Exposure bias (also called "missing not at random" or MNAR) occurs when items that are not shown to users cannot receive feedback, creating an systematic gap between observed and unobserved preferences.

### The Feedback Loop

```
Model trains on observed data → Model recommends similar items →
Unobserved items never get shown → No feedback on unobserved items →
Model continues to be biased toward observed items
```

### Types of Exposure Bias

| Type | Description | Example |
|------|-------------|---------|
| **Position-based exposure** | Items in lower positions get less exposure | New items buried at bottom |
| **Model-based exposure** | The model's own predictions determine what gets shown | Cold-start items never shown |
| **UI-based exposure** | Interface design limits what users see | Only 10 items shown per page |
| **Temporal exposure** | Items available at certain times get different exposure | Seasonal items shown only during holidays |
| **Geographic exposure** | Items available in certain regions get different exposure | Regional content not shown to other regions |

### Exposure Bias Quantification

```
Exposure_Bias = 1 - |{items with observed feedback}| / |{all items}|
```

For most production systems, exposure bias is extreme: only 1–5% of the catalog receives any user feedback.

### The Implications

1. **Inflated accuracy metrics**: Models appear more accurate on observed items because they are easier to predict
2. **Popularity reinforcement**: Already-popular items get more exposure, becoming even more popular
3. **Long-tail suppression**: Niche items never get enough feedback to be recommended
4. **Evaluation bias**: Offline metrics computed on observed data overestimate true performance

## Self-Selection Bias

### Definition

Self-selection bias occurs when the users who provide explicit feedback (ratings, reviews) are systematically different from the general user population.

### How Self-Selection Manifests

| Behavior | Who Does This | Bias Effect |
|----------|--------------|------------|
| **Rating items** | Engaged, opinionated users | Over-represents extreme preferences |
| **Writing reviews** | Very satisfied or very dissatisfied users | Bimodal feedback distribution |
| **Completing profiles** | Privacy-comfortable users | Over-represents certain demographics |
| **Using recommendations** | Tech-savvy users | Under-represents less engaged users |

### Quantifying Self-Selection Bias

Compare the distribution of rated items to all interacted items:

```
Rating_Bias = KL_distribution(rated_items || all_interacted_items)
```

If rated items are systematically different from all interacted items, the rating data is self-selected.

### Self-Selection in Different Feedback Types

| Feedback Type | Self-Selection Severity | Mitigation |
|--------------|------------------------|------------|
| Explicit ratings | High | Only ~1–5% of users rate items |
| Clicks | Moderate | Users click what they see (exposure confound) |
| Purchase | Low–Moderate | Purchases are less selective |
| Time spent | Low | Most users leave implicit time signals |
| Skip/dismiss | Low | Nearly universal behavior |

## Causal Inference Approaches

### The Fundamental Problem

We want to know: "What would user u have done if shown a different item?" This is the counterfactual question, and it is fundamentally unanswerable for a single user-item pair. Causal inference provides frameworks for estimating average treatment effects.

### Propensity Scores

#### Definition

The propensity score is the probability of an item being shown to a user, given the user's features and the item's features:

```
e(x) = P(treatment=1 | X=x) = P(item shown | user features, item features)
```

#### Estimation

Propensity scores can be estimated using:
1. **Logistic regression**: P(shown) = σ(θ^T × features)
2. **Gradient boosting**: More flexible, captures non-linear relationships
3. **Randomized data**: Use randomized traffic to estimate true propensities

#### Validation

Propensity score models should be validated by checking:
- **Positivity**: All items have non-zero propensity (propensity > 0 for all items)
- **Overlap**: Treatment and control groups have overlapping propensity distributions
- **Calibration**: Predicted propensities match observed exposure rates

### Inverse Propensity Weighting (IPW)

#### Concept

Weight each observed outcome by the inverse of the probability of that outcome being observed:

```
IPW_Estimate = (1/n) * Σ (outcome_i × weight_i / propensity_i)
```

#### Why It Works

Items with low propensity (rarely shown) but high engagement are weighted more heavily, compensating for the fact that they are underrepresented in the data.

#### Variance Problem

IPW can have very high variance when propensities are small:

```
Var(IPW) ∝ E[outcome² / propensity²]
```

When propensity → 0, variance → ∞. This is the "propensity score problem."

#### Stabilized IPW

Use the marginal probability of treatment instead of the conditional:

```
Stabilized_IPW = (1/n) * Σ (outcome_i × P(treatment) / propensity_i)
```

This reduces variance while maintaining unbiasedness.

### Doubly Robust Estimation

#### Concept

Doubly robust (DR) estimation combines outcome modeling with propensity weighting:

```
DR_Estimate = Outcome_Model prediction + IPW_weight × (observed_outcome - Outcome_Model prediction)
```

#### Why "Doubly Robust"

The estimate is consistent if EITHER the outcome model OR the propensity model is correctly specified (but not necessarily both). This provides a safety net: if one model is wrong, the other can compensate.

#### DR Estimator Formula

```
DR = μ̂_treated(x) + (y_treated / e(x)) × (1 - e(x)) - μ̂_control(x) × (1 - e(x))
```

Where:
- μ̂_treated(x) = predicted outcome under treatment
- μ̂_control(x) = predicted outcome under control
- e(x) = propensity score
- y_treated = observed outcome under treatment

### Other Causal Methods

| Method | Requirement | Pros | Cons |
|--------|------------|------|------|
| **Matching** | Propensity scores | Simple, intuitive | Losses data, limited to observed confounders |
| **Stratification** | Propensity scores | Reduces confounding | Arbitrary strata boundaries |
| **IV (Instrumental Variables)** | Valid instrument | Handles unmeasured confounders | Finding valid instruments is hard |
| **RDD (Regression Discontinuity)** | Sharp threshold | Clean identification | Only estimates effects near threshold |
| **DiD (Difference-in-Differences)** | Parallel trends | Controls for time effects | Parallel trends assumption may fail |

### Application to Recommendations

#### Unbiased Learning from Implicit Feedback

```
For each (user, item) pair with observed click:
    weight = 1 / P(item_shown_to_user)
    Train model with weighted_loss = weight × prediction_error
```

#### Counterfactual Evaluation

```
Value_of_new_policy = Σ (new_policy_score(x) / old_policy_score(x)) × observed_reward
```

This is called Importance Sampling and allows estimating the value of a new recommendation policy using only data from the old policy.

## Practical Considerations

### When Selection Bias Is Severe

| Indicator | Measurement |
|-----------|-------------|
| High catalog coverage gap | >95% of catalog has zero feedback |
| Strong popularity concentration | Top 10% of items receive >80% of interactions |
| Low randomization traffic | No randomized data available for propensity estimation |
| Demographic skew | Rating users differ significantly from the general population |

### Mitigation Strategies

1. **Collect randomized data**: Allocate 1–5% of traffic to random recommendations
2. **IPS reweighting**: Apply inverse propensity weights to training data
3. **Doubly robust estimation**: Combine outcome modeling with propensity weighting
4. **Exploration**: Thompson sampling or epsilon-greedy to expose users to diverse items
5. **Catalog stratification**: Ensure training data includes items from all popularity tiers
6. **Causal regularization**: Add debiasing terms to the model loss function

### Monitoring Selection Bias

| Metric | Formula | Healthy Range |
|--------|---------|---------------|
| Catalog coverage | Items with feedback / total items | > 20% |
| Propensity overlap | KS statistic of propensities | < 0.3 |
| Effective sample size | n_eff = (Σw_i)² / Σw_i² | > 50% of nominal sample size |
| IPS weight ratio | max(weight) / min(weight) | < 100 |
