# Stacking Ensemble for Recommendations

## Overview

Stacking (stacked generalization) is an ensemble learning technique that combines multiple diverse base models through a meta-learner. In recommendation systems, stacking leverages the complementary strengths of different algorithms — collaborative filtering, content-based, deep learning, and graph-based methods — to produce superior predictions that no single model can achieve alone.

---

## Stacking Architecture

### Two-Level Architecture

```
Level 0 (Base Models):
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│  Model A  │ │  Model B  │ │  Model C  │ │  Model D  │ │  Model E  │
│  (CF-MF)  │ │  (CB-BERT)│ │ (DeepFM) │ │ (XGBoost) │ │ (Pop-based│
└─────┬────┘ └─────┬────┘ └─────┬────┘ └─────┬────┘ └─────┬────┘
      │            │            │            │            │
      ▼            ▼            ▼            ▼            ▼
   score_A     score_B     score_C     score_D     score_E
      │            │            │            │            │
      └────────────┴────────────┼────────────┴────────────┘
                                │
                                ▼
                    Level 1 (Meta-Learner):
                    ┌────────────────────┐
                    │   Meta-Model       │
                    │   Input: [s_A,     │
                    │   s_B, s_C, s_D,   │
                    │   s_E, context]    │
                    └─────────┬──────────┘
                              │
                              ▼
                       final_score
```

### Multi-Level Stacking

Production systems sometimes use three or more levels:

```
Level 0: Raw features → Simple models (MF, KNN, popularity)
Level 1: Level 0 outputs → Complex models (deep learning, gradient boosting)
Level 2: Level 1 outputs → Meta-learner (linear model, small neural net)
```

Each level adds capacity but increases complexity and overfitting risk.

---

## Meta-Learner Design

### Choice of Meta-Learner

| Meta-Learner | Parameters | Pros | Cons | Best When |
|-------------|-----------|------|------|-----------|
| Linear Regression | K+1 | Fast, interpretable, regularized | Assumes linearity | Base scores are well-calibrated |
| Logistic Regression | K+1 | Probabilistic output | Still linear | Binary classification |
| Ridge/Lasso | K+1 + α | Prevents overfitting | Still linear | Many base models |
| Random Forest | Many | Captures non-linear interactions | Risk of overfitting | Moderate data |
| Gradient Boosting | Many | High capacity | Overfitting risk | Large data |
| Neural Network | Many | Flexible, universal approximator | Most overfitting risk | Very large data |
| RankNet | Many | Optimizes ranking directly | Complex | Ranking-specific targets |

### Meta-Feature Design

Beyond base model scores, meta-features can include:

| Feature Category | Examples | Value |
|-----------------|----------|-------|
| Base model scores | score_CF, score_CB, score_DL | Primary signal |
| Score variance | Variance across base models | Confidence indicator |
| Score rank | Rank of each model's prediction | Robust to scale differences |
| User features | Activity level, demographics | Personalization |
| Item features | Popularity, category, age | Context |
| Context features | Time, device, session depth | Situational adaptation |

### Output Transformation

Base model scores may have different scales and distributions:

| Transformation | When to Use |
|---------------|-------------|
| Min-max normalization | Scores in different ranges |
| Z-score normalization | Scores with different means/variances |
| Rank transformation | Non-parametric, robust to outliers |
| Sigmoid / Platt scaling | Calibrate to probabilities |
| No transformation | Scores already comparable (e.g., all AUC-calibrated) |

---

## Cross-Validation for Stacking

### The Data Leakage Problem

A critical issue in stacking: base models must not train on the same data used to generate their predictions for the meta-learner. Otherwise, the meta-learner learns from overly optimistic (leaked) predictions.

### K-Fold Stacking Procedure

```
Split data into K folds (e.g., K=5):

For each fold k in 1..K:
  Train all base models on K-1 folds (training set)
  Generate predictions on fold k (out-of-fold predictions)

Combine: Out-of-fold predictions from all folds → Full prediction matrix
Train meta-learner on the full prediction matrix

For test data:
  Use base models trained on full training set
  Generate test predictions
  Feed to meta-learner for final prediction
```

### Fold Design Considerations

| Strategy | Description | Pros | Cons |
|----------|-------------|------|------|
| Random K-fold | Random split | Simple | May not respect temporal order |
| Temporal split | Train on past, validate on future | Realistic | May waste recent data |
| User-level split | All interactions of a user in one fold | Prevents user leakage | May create imbalanced folds |
| Stratified K-fold | Balanced distribution per fold | Consistent | Complex for implicit feedback |

### Out-of-Fold Prediction Generation

```
Original training data: [d₁, d₂, ..., dₙ]

Fold 1: Train on [d₆, ..., dₙ], predict on [d₁, ..., d₅]
Fold 2: Train on [d₁, d₅, ..., dₙ], predict on [d₆, ..., d₁₀]
...
Fold 5: Train on [d₁, ..., d₄₀], predict on [d₄₁, ..., dₙ]

Combined OOF predictions: [d₁_oof, d₂_oof, ..., dₙ_oof]
```

### Repeated Stacking

For higher quality, repeat the K-fold process R times with different random splits:

```
Repeat R times:
  Generate K-fold OOF predictions with different splits
Average: Final OOF = mean of R OOF prediction sets
```

R = 3–5 is typical; diminishing returns beyond that.

---

## Diverse Base Models

### Diversity Principles

The power of stacking comes from base model diversity. Models should make different types of errors.

#### Algorithm Diversity

| Model Type | Strength | Typical Weakness |
|-----------|----------|-----------------|
| Matrix Factorization | User-item patterns | Cold start, no content |
| Content-Based (BERT) | Semantic understanding | No behavioral signals |
| DeepFM | Feature interactions | Requires feature engineering |
| XGBoost | Non-linear features | Limited sequence modeling |
| Item-KNN | Local patterns | No global optimization |
| Popularity baseline | Simple, robust | No personalization |
| Graph-based (PinSage) | Structural relationships | Expensive, sparse graphs |

#### Data Diversity

- Train different base models on different subsets or views of the data
- Use different negative sampling strategies per model
- Apply different data augmentation techniques

#### Feature Diversity

- Model A: Only interaction features
- Model B: Only content features
- Model C: Interaction + content features
- Model D: Temporal features + interactions

### Measuring Diversity

| Metric | Description | Target |
|--------|-------------|--------|
| Prediction correlation | Pairwise correlation between base model outputs | Low (< 0.7) |
| Error diversity | Correlation between model errors | Low |
| Output variance | Variance of predictions across models | High |
| Disagreement rate | % of samples where models disagree on ranking | Moderate (30–60%) |

### Anti-Patterns to Avoid

- **Redundant models**: Two matrix factorization variants with same hyperparameters
- **Dominant model**: One model consistently outperforms others by large margin
- **Correlated errors**: All models fail on the same items
- **Overfitting base models**: Overly complex base models that overfit training data

---

## Preventing Overfitting in Stacking

### Sources of Overfitting

1. **Data leakage**: Base model predictions leak training information to meta-learner
2. **Meta-learner complexity**: Complex meta-learners memorize training patterns
3. **Small validation set**: Limited data for meta-learner training
4. **Feature engineering leakage**: OOF features accidentally use test information

### Prevention Strategies

#### Regularization

| Technique | Application | Typical Values |
|-----------|-------------|----------------|
| L1 regularization | Sparse meta-learner weights | α = 0.01–0.1 |
| L2 regularization | Prevent large meta-learner weights | α = 0.001–0.01 |
| Dropout | Neural meta-learner | 0.2–0.5 |
| Early stopping | Monitor validation loss | Patience = 5–10 epochs |

#### Meta-Learner Complexity Control

```
Progression (start simple, increase only if justified):
1. Linear regression with L2 (start here)
2. Ridge regression with feature selection
3. Small gradient boosted tree (max_depth = 3)
4. Shallow neural network (1 hidden layer)
5. Deeper models (only with large datasets)
```

#### Validation Strategy

- **Hold-out set**: Reserve 10–20% of training data for meta-learner validation
- **Nested cross-validation**: Outer loop for base model evaluation, inner loop for meta-learner
- **Temporal validation**: Train on past, validate on future (most realistic)

#### Feature Selection for Meta-Learner

- Remove base model features with low importance (tree-based importance or L1 coefficients)
- Monitor for feature redundancy (high correlation between base model outputs)
- Use permutation importance on the meta-learner validation set

---

## Blending vs Stacking

### Blending (Simplified Stacking)

```
Split data into Training (70%) and Hold-out (30%):

1. Train base models on Training set
2. Generate predictions on Hold-out set (not OOF)
3. Train meta-learner on Hold-out predictions
4. For test: base models predict → meta-learner combines
```

### Comparison

| Aspect | Blending | Stacking |
|--------|---------|----------|
| Implementation | Simple | More complex |
| Data usage | Less efficient (hold-out) | More efficient (K-fold OOF) |
| Prediction quality | Good | Better |
| Training time | Faster (no retraining) | Slower (K models × base models) |
| Leakage risk | Low (clean separation) | Higher (requires careful K-fold) |
| Meta-training data | Limited (hold-out only) | Full training set (OOF) |
| Overfitting risk | Lower | Higher (more complex) |
| Production usage | Quick prototyping | Production systems |

### When to Use Each

**Use Blending When:**
- Prototyping and rapid iteration
- Small datasets where K-fold is expensive
- Simple base model ensemble with linear meta-learner
- Need quick validation of ensemble approach

**Use Stacking When:**
- Production system requiring maximum quality
- Sufficient compute for K-fold retraining
- Many diverse base models to combine
- Large dataset where data efficiency matters

---

## Production Implementation

### Training Pipeline

```
Step 1: Define base models and their configurations
Step 2: Generate OOF predictions using K-fold cross-validation
Step 3: Train meta-learner on OOF predictions
Step 4: Retrain all base models on full training data
Step 5: Validate end-to-end pipeline on hold-out set
Step 6: Deploy all models to serving infrastructure
```

### Serving Pipeline

```
Request → 
  Parallel base model inference →
  Collect all scores →
  Construct meta-feature vector →
  Meta-learner prediction →
  Final ranking
```

### Latency Considerations

| Component | Typical Latency | Optimization |
|-----------|----------------|-------------|
| Base model inference | 5–50ms each | Pre-computation, caching |
| Feature extraction | 2–10ms | Feature store |
| Meta-learner | < 1ms | Linear model, very fast |
| Total | 10–100ms | Parallel base model execution |

### Model Versioning

- Version each base model independently
- Version the meta-learner separately
- Track which combination of base model versions produced each prediction
- Enable rollback of individual components

### Monitoring

- Track per-base-model score distributions over time
- Monitor meta-learner weight changes (drift detection)
- Alert on sudden changes in ensemble behavior
- Log disagreements between base models (potential data issues)

---

## Advanced Stacking Techniques

### Cascaded Stacking

```
Level 1: Simple, fast models → Initial ranking
Level 2: Complex models re-ranked on Level 1's top candidates
Level 3: Meta-learner combines Level 1 and Level 2 outputs
```

Reduces compute by only running expensive models on a filtered candidate set.

### Dynamic Stacking

- Select which base models to use per prediction based on context
- Different user segments may benefit from different model combinations
- Implemented via a gating network or rule-based selection

### Online Stacking

- Continuously update meta-learner weights based on incoming feedback
- Use online learning algorithms (e.g., online gradient descent)
- Adapt to distribution shifts without full retraining

### Multi-Task Stacking

- Train base models on different tasks (CTR, conversion, rating)
- Meta-learner combines predictions from different task models
- Particularly useful when optimizing multiple objectives simultaneously
