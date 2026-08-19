# Feature Selection for Recommendation Systems

## 1. Why Feature Selection Matters

### 1.1 Impact on Recommendation Quality
- **Curse of Dimensionality**: Model performance degrades with too many features
  - Distance metrics become meaningless in high dimensions
  - Overfitting risk increases exponentially with feature count
- **Noise Amplification**: Irrelevant features add noise that drowns useful signal
  - A model with 50 good features often outperforms one with 500 mixed features
- **Feature Interaction Dilution**: Too many features weaken individual feature contributions
  - Trees split on most informative features first; noise features waste splits

### 1.2 Operational Benefits
- **Training Speed**: Fewer features = faster training (linear or better improvement)
- **Inference Latency**: Fewer features = faster feature retrieval and prediction
  - Critical for real-time recommendation serving (<50ms budget)
- **Pipeline Simplicity**: Fewer features = simpler computation, fewer dependencies
- **Model Interpretability**: Simpler models are easier to debug and explain
- **Storage Cost**: Fewer features = less feature store storage and memory

---

## 2. Filter Methods

### 2.1 Variance Threshold
- **Concept**: Remove features with near-zero variance (constant or near-constant)
- **Implementation**: `variance < threshold` → drop feature
  - For binary features: threshold at `p × (1-p)` where p is majority class proportion
  - For continuous: absolute variance threshold after normalization
- **Limitations**: Doesn't consider feature-target relationship

### 2.2 Correlation Analysis
- **Pearson Correlation**: Linear correlation between numeric feature pairs
  - Remove one of each pair with |r| > 0.95; keep the one more correlated to target
- **Spearman Correlation**: Rank-based; more robust to outliers than Pearson
- **Cramér's V**: Correlation between categorical features (chi-squared based, range [0,1])
- **Correlation Heatmap**: Visual inspection; identify feature clusters representing same signal

### 2.3 Mutual Information
- **MI with Target**: `MI(X; Y)` measures dependency — captures non-linear relationships
  - MI = 0: independent; higher MI: stronger predictive relationship
- **Implementation**: `sklearn.feature_selection.mutual_info_classif` or `mutual_info_regression`
- **Normalized MI**: `NMI(X;Y) = MI(X;Y) / sqrt(H(X) × H(Y))` — comparable across features
- **Estimation**: KNN-based (K=5) for continuous, histogram-based for discrete

### 2.4 Chi-Squared Test
- **Concept**: Test independence between categorical feature and target
  - `χ² = Σ (observed - expected)² / expected`; higher χ² = more predictive
- **Requirements**: Non-negative feature values (apply after encoding)
- **Limitations**: Only captures linear dependency between categorical variables
- **Implementation**: `sklearn.feature_selection.chi2`

### 2.5 ANOVA F-Test
- **Concept**: Test whether feature means differ across target classes
  - `F = between_class_variance / within_class_variance`
- **Requirements**: Numeric features, categorical target; assumes normality
- **Use Case**: Quick feature ranking for regression and classification targets

### 2.6 Variance Inflation Factor (VIF)
- **Concept**: Detect multicollinearity among features
  - `VIF(X) = 1 / (1 - R²_X)` where R²_X is from regressing X on all other features
  - VIF > 5–10 indicates problematic multicollinearity
- **Use Case**: Linear models where collinearity inflates coefficient variance

---

## 3. Wrapper Methods

### 3.1 Forward Selection
1. Start with empty feature set
2. Evaluate each candidate feature individually
3. Add feature that improves model performance most
4. Repeat until no improvement or budget reached
- **Cons**: O(n²) evaluations; greedy — may miss optimal combinations

### 3.2 Backward Elimination
1. Start with all features; evaluate model
2. Remove feature whose removal least impacts performance
3. Repeat until performance degrades or minimum features reached
- **Cons**: Expensive for high-dimensional feature sets

### 3.3 Recursive Feature Elimination (RFE)
1. Train model on all features
2. Rank features by importance (coefficient magnitude, tree importance)
3. Remove least important feature (or bottom p%); retrain and repeat
- **Variants**: RFE-CV and RFECV for cross-validated optimal feature count
- **Base Models**: Linear models (|coefficient|), trees (Gini/permutation importance), SVM (weight magnitude)
- **Pros**: More principled than forward/backward; captures feature interactions

### 3.4 Sequential Feature Selection (SFS)
- Similar to forward/backward but with different criteria (kNN accuracy, custom metric)
- **Bidirectional SFS**: Consider both adding and removing features at each step
- **Implementation**: `mlxtend.feature_selection.SequentialFeatureSelector`

---

## 4. Embedded Methods

### 4.1 L1 Regularization (Lasso)
- **Concept**: Add L1 penalty → drives some coefficients to exactly zero
  - `loss = original_loss + λ × Σ|wᵢ|`; higher λ → more features removed
- **Elastic Net**: Combine L1 + L2: `α × λ × Σ|wᵢ| + (1-α) × λ × Σwᵢ²`
  - L1 selects features; L2 handles correlated features
- **Limitation**: Assumes linear relationships

### 4.2 Tree-Based Feature Importance
- **Gini Importance (MDI)**: Mean decrease in impurity — biased toward high-cardinality features
- **Permutation Importance**: Shuffle feature → measure performance drop; more reliable
- **SHAP Values**: Game-theoretic importance via `shap.TreeExplainer`
  - Global: mean |SHAP|; Local: per-prediction contribution breakdown
- **Implementation**: `RandomForest.feature_importances_`, `sklearn.inspection.permutation_importance`

### 4.3 Regularized Tree Models
- **L1-Regularized XGBoost**: `alpha` parameter encourages sparse feature usage
- **Feature Subsampling**: Random feature subset per split (Random Forest style)
- **Max Features Parameter**: Prevents over-reliance on top features

---

## 5. Feature Importance Ranking

### 5.1 Global Importance Measures
- **Mean Absolute SHAP**: Average |SHAP value| — most reliable global measure
- **Permutation Importance Mean**: Average performance drop; model-agnostic
- **Feature Importance Entropy**: How evenly importance is distributed
  - Low entropy = model relies on few features (fragile); High = more robust

### 5.2 Stability Analysis
- **Bootstrap Stability**: Compute importance on multiple bootstrap samples
  - Stable rankings = reliable features; unstable = potentially spurious
- **Cross-Validation Stability**: Importance variance across CV folds
- **Temporal Stability**: Track importance over time; sudden changes indicate drift

### 5.3 Visualization
- **Bar Plot**: Top-K features by importance score
- **Beeswarm Plot**: SHAP value distribution per feature (direction + magnitude)
- **Dependence Plot**: Feature value vs SHAP value — reveals non-linear relationships
- **Waterfall Plot**: Per-prediction feature contribution breakdown

---

## 6. Dimensionality Reduction

### 6.1 Principal Component Analysis (PCA)
- Linear projection to orthogonal components maximizing variance
- Retain components explaining 95–99% of variance
- **When to Use**: High-dimensional dense features (embeddings, TF-IDF)
- **Implementation**: `sklearn.decomposition.PCA(n_components=0.95)`

### 6.2 t-SNE
- Non-linear dimensionality reduction for visualization (2D/3D)
- Preserves local neighborhood structure; O(n²) without approximation
- **Parameters**: Perplexity (30–50), learning rate (200–1000), iterations (1000+)

### 6.3 UMAP
- Faster, scalable t-SNE alternative; better preserves global structure
- Can be used for downstream tasks (not just visualization)
- **Parameters**: n_neighbors (15–50), min_dist (0.1–0.5), n_components (2 or 3)

### 6.4 Autoencoders
- Neural network: Encoder (high→low dim) → Decoder (low→high dim)
- **VAE**: Probabilistic latent space enables interpolation and generation
- **Advantage**: Captures non-linear relationships; task-specific compression

---

## 7. Feature Selection for Recommendations

### 7.1 Feature Tiers
- **Tier 1 (Critical)**: User-item interaction history, item popularity, user preferences
  - Drive 60–80% of recommendation quality; never remove without strong justification
- **Tier 2 (Important)**: Context features (time, device), content embeddings
  - Add 10–20% improvement; remove only if overfitting or latency issues
- **Tier 3 (Supplementary)**: Social features, weather, granular metadata
  - Add 2–5% improvement; include only if infrastructure supports it

### 7.2 Selection by Model Type
- **Collaborative Filtering**: Interaction features dominate; content features supplement
- **Content-Based**: Text/image embeddings primary; interaction features validate
- **Deep Learning**: Absorb high-dimensional features; rely on regularization
- **Linear Models**: Aggressive selection needed; interactions must be explicit
- **Tree-Based**: Handle mixed types well; less aggressive selection needed

### 7.3 Ablation Study Protocol
1. Start with full feature set as baseline
2. Remove one feature group at a time
3. Measure impact on offline metrics (NDCG, Recall, MRR)
4. A/B test top candidates online (engagement, revenue)
5. Document findings; establish minimum viable feature set

### 7.4 Selection Frequency
- **Initial**: Full ablation study when feature set is established
- **Monthly**: Review importance rankings for drift
- **Quarterly**: Full re-evaluation with new features
- **On model/data change**: Re-run selection for new architecture or major data shifts

---

## 8. Impact on Model Performance

### 8.1 Metrics to Track

| Metric | What It Measures | Expected Impact |
|---|---|---|
| NDCG@K | Ranking quality of top-K recommendations | Primary metric |
| Recall@K | Coverage of relevant items in top-K | Sensitivity to feature count |
| MRR | Mean reciprocal rank of first relevant item | Stability under changes |
| Training Time | Time to train model | Linear reduction with fewer features |
| Inference Latency | Time to generate recommendations | Proportional to feature count |
| Model Size | Memory footprint | Proportional to feature count |

### 8.2 Diminishing Returns
- **10–20 features**: Rapid performance gains
- **20–50 features**: Moderate gains; most important signals captured
- **50–100 features**: Marginal gains; diminishing returns
- **100+ features**: Near-zero or negative gains; overfitting risk
- **Rule of Thumb**: Optimal count is typically 30–80 for recommendation models

### 8.3 Selection Pitfalls
- **Data Leakage**: Features computed from future interactions
  - Always use point-in-time joins for feature computation
- **Selection Bias**: Optimizing for one metric may harm others
  - NDCG optimization may hurt diversity or novelty; evaluate multi-dimensionally
- **Distribution Shift**: Selected features may not remain important as data evolves
- **Interaction Blindness**: Filter methods miss jointly-predictive weak feature pairs
