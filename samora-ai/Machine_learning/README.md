# Machine Learning Interview Questions and Answers

## Q1: What is Machine Learning?
**A:** Machine Learning (ML) is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. ML algorithms build mathematical models from training data to make predictions or decisions. Types: supervised (labeled data), unsupervised (unlabeled data), semi-supervised, and reinforcement learning.

## Q2: What is the difference between supervised and unsupervised learning?
**A:** Supervised learning uses labeled data (input-output pairs) to learn a mapping function. Tasks: regression (predict continuous values) and classification (predict categories). Examples: Linear Regression, Random Forest, SVM. Unsupervised learning uses unlabeled data to find hidden patterns. Tasks: clustering (group similar data), dimensionality reduction, association. Examples: K-Means, PCA, Apriori.

## Q3: What is the difference between regression and classification?
**A:** Regression predicts continuous numerical values (e.g., house price, temperature). Output is a real number. Loss functions: MSE, MAE, Huber. Classification predicts discrete class labels (e.g., spam/not spam, digit 0-9). Output is a class/category. Loss functions: cross-entropy, hinge loss. Some algorithms can do both (e.g., decision trees, neural networks).

## Q4: What is overfitting and how do you prevent it?
**A:** Overfitting occurs when a model learns training data too well (including noise) but fails to generalize to unseen data. Signs: high training accuracy, low validation accuracy. Prevention: 1) Cross-validation, 2) Regularization (L1/L2), 3) More training data, 4) Data augmentation, 5) Early stopping, 6) Feature selection, 7) Simpler models, 8) Dropout (neural networks), 9) Pruning (decision trees).

## Q5: What is underfitting?
**A:** Underfitting occurs when a model is too simple to capture the underlying patterns in the data. Signs: high training error, high validation error (similar magnitude). Causes: overly simple model, insufficient features, too much regularization. Solutions: increase model complexity, add more features, reduce regularization, train longer, use more powerful algorithms.

## Q6: What is the bias-variance tradeoff?
**A:** Bias: error from overly simplistic assumptions (underfitting). Variance: error from sensitivity to training data fluctuations (overfitting). The tradeoff: increasing model complexity reduces bias but increases variance. Goal: find the sweet spot where total error (bias + variance + irreducible error) is minimized. Regularization and ensemble methods help manage this tradeoff.

## Q7: What is cross-validation?
**A:** Cross-validation evaluates model performance by splitting data into multiple train/validation sets. K-Fold: divide data into K folds, train on K-1, validate on 1, repeat K times. Stratified K-Fold: preserves class proportions in each fold. Leave-One-Out: K=N (one sample validation). Benefits: more reliable performance estimate, less dependent on single train/test split.

## Q8: What is the difference between training error and test error?
**A:** Training error is the error on the data used to train the model — typically decreases with more training. Test error is the error on unseen data — measures generalization. Large gap between low training error and high test error indicates overfitting. Both high indicates underfitting. Only test error matters for real-world performance.

## Q9: What are evaluation metrics for classification?
**A:** Accuracy: (TP+TN)/(TP+TN+FP+FN) — overall correctness. Precision: TP/(TP+FP) — how many selected items are relevant. Recall: TP/(TP+FN) — how many relevant items are selected. F1-Score: 2*P*R/(P+R) — harmonic mean of precision and recall. ROC-AUC: area under ROC curve — measures ranking quality. Log Loss: probabilistic classification error.

## Q10: What are evaluation metrics for regression?
**A:** MSE (Mean Squared Error): average squared differences — penalizes large errors. RMSE: sqrt(MSE) — in same units as target. MAE (Mean Absolute Error): average absolute differences — robust to outliers. R-squared (R2): proportion of variance explained — 1 is perfect, 0 is baseline. Adjusted R2: R2 penalized for number of features.

## Q11: What is the confusion matrix?
**A:** A confusion matrix is a table showing actual vs predicted classifications. For binary: rows = actual (positive/negative), columns = predicted (positive/negative). Cells: TP (true positive), TN (true negative), FP (false positive/Type I error), FN (false negative/Type II error). From it, derive: accuracy, precision, recall, F1, specificity.

## Q12: What is the ROC curve?
**A:** ROC (Receiver Operating Characteristic) curve plots True Positive Rate (recall) vs False Positive Rate (1-specificity) at various threshold settings. AUC (Area Under Curve) summarizes performance — 1.0 is perfect, 0.5 is random. AUC is threshold-independent and works well for imbalanced datasets. Higher AUC indicates better ranking quality.

## Q13: What is feature engineering?
**A:** Feature engineering is the process of creating new features from raw data to improve model performance. Techniques: 1) Domain-specific features (e.g., day of week from date), 2) Polynomial features (x2, x*y), 3) Interaction features, 4) Aggregations (mean, count per group), 5) Binning (age groups), 6) Text features (TF-IDF, word counts), 7) Encoding (one-hot, label, target encoding).

## Q14: What is feature selection?
**A:** Feature selection identifies the most relevant features to reduce dimensionality, improve performance, and reduce overfitting. Methods: 1) Filter (correlation, chi-square, mutual information), 2) Wrapper (forward/backward selection, RFE), 3) Embedded (Lasso, tree importance, regularization). Benefits: faster training, simpler models, better generalization.

## Q15: What is feature scaling and why is it important?
**A:** Feature scaling standardizes the range of features. Methods: Standardization (z-score: (x-mean)/std) — mean=0, std=1; Normalization/MinMax (x-min)/(max-min) — range [0,1]; Robust scaling (using median/IQR). Important for: distance-based algorithms (KNN, SVM, K-Means), gradient descent (faster convergence), regularization (fair penalty). Tree-based models don't require scaling.

## Q16: What is the difference between normalization and standardization?
**A:** Normalization (MinMax scaling) scales to [0,1] range: (x-min)/(max-min). Sensitive to outliers. Standardization (Z-score) centers to mean=0, std=1: (x-mean)/std. Less sensitive to outliers. Use normalization when data has bounded range. Use standardization when data has outliers or algorithm assumes normal distribution (SVM, linear models).

## Q17: What is PCA (Principal Component Analysis)?
**A:** PCA is an unsupervised dimensionality reduction technique that finds orthogonal directions (principal components) maximizing variance. Transforms original features into linearly uncorrelated components. Used for: reducing dimensionality, visualization, noise reduction, feature extraction. Steps: standardize data, compute covariance matrix, eigendecomposition, select top k components.

## Q18: What is the difference between PCA and t-SNE?
**A:** PCA: linear, deterministic, preserves global structure (variance), fast, good for preprocessing. t-SNE: non-linear, stochastic, preserves local structure (neighbor relationships), slower, good for visualization (2D/3D). PCA is suitable for dimensionality reduction before other algorithms; t-SNE is primarily for visualization of high-dimensional data.

## Q19: What is Linear Regression?
**A:** Linear Regression models the relationship between input features and continuous target as a linear function: y = w0 + w1*x1 + w2*x2 + ... + wn*xn + e. Parameters are estimated by minimizing MSE (Ordinary Least Squares). Assumptions: linearity, independence, homoscedasticity, normality of errors. Simple (1 feature) or multiple (many features).

## Q20: What is Logistic Regression?
**A:** Logistic Regression models binary classification probability using the sigmoid function: P(y=1) = 1/(1 + e^-(w·x + b)). Despite the name, it's a classification algorithm. Decision boundary is linear. Uses log-loss (binary cross-entropy). Can be extended to multi-class via softmax (multinomial logistic regression). Regularized versions: L1 (Lasso), L2 (Ridge), ElasticNet.

## Q21: What is the difference between Linear Regression and Logistic Regression?
**A:** Linear Regression predicts continuous values (output range: -inf to +inf), uses MSE loss, assumes normal error distribution. Logistic Regression predicts class probabilities (output range: 0 to 1), uses log-loss (cross-entropy), assumes binomial error distribution. Linear Regression is fit with OLS; Logistic Regression with maximum likelihood estimation (iterative).

## Q22: What is Regularization?
**A:** Regularization adds a penalty term to the loss function to prevent overfitting by constraining model weights. L1 (Lasso): adds absolute weight values (sum|w|) — encourages sparsity (feature selection). L2 (Ridge): adds squared weight values (sum w2) — keeps all features with small weights. ElasticNet: combines L1 and L2. Lambda controls regularization strength.

## Q23: What is the difference between L1 and L2 regularization?
**A:** L1 (Lasso): penalty = λ*Σ|wi| — can zero out features (feature selection), more robust to outliers, creates sparse models. L2 (Ridge): penalty = λ*Σ(wi2) — shrinks weights toward zero but never exactly zero, handles correlated features better. L1 is good for high-dimensional data; L2 is good when all features are relevant.

## Q24: What is Decision Tree?
**A:** A Decision Tree is a tree-structured algorithm that splits data based on feature values at each node. Internal nodes test features, branches represent outcomes, leaves represent predictions. Splitting criteria: Gini impurity (classification), entropy/information gain, MSE (regression). Advantages: interpretable, handles non-linear relationships, no scaling needed. Disadvantages: prone to overfitting.

## Q25: What is Gini Impurity?
**A:** Gini Impurity measures the probability of incorrect classification of a random sample: Gini = 1 - Σ(pi^2) where pi is the proportion of class i. Lower Gini = purer split. Perfect split: Gini=0. Worst: Gini=0.5 (binary). Used in CART (Classification and Regression Trees) for selecting split points.

## Q26: What is Entropy and Information Gain?
**A:** Entropy measures impurity/uncertainty: H = -Σ(pi*log2(pi)). Pure node: entropy=0. Max: log2(k) for k classes. Information Gain = parent_entropy - weighted_avg_child_entropy. Higher gain = better split. Used in ID3, C4.5 decision tree algorithms. Similar to Gini but computationally heavier (logarithms).

## Q27: How do you prevent overfitting in Decision Trees?
**A:** Pruning: remove branches that provide little predictive power. Pre-pruning (early stopping): max_depth, min_samples_split, min_samples_leaf, max_features, max_leaf_nodes. Post-pruning (prune after full growth): cost-complexity pruning (alpha parameter). Random Forest (ensemble of trees) inherently reduces overfitting.

## Q28: What is Random Forest?
**A:** Random Forest is an ensemble of decision trees trained with bagging and random feature selection. Each tree trained on a bootstrap sample (random sample with replacement). At each split, only a random subset of features is considered. Prediction: majority vote (classification) or average (regression). Reduces variance without increasing bias significantly.

## Q29: What is the difference between Bagging and Boosting?
**A:** Bagging (Random Forest): trains models in parallel on bootstrap samples, averages predictions. Reduces variance. Each model is independent. Boosting (XGBoost, AdaBoost): trains models sequentially, each correcting the previous model's errors. Reduces bias and variance. Boosting can overfit if too many iterations. Boosting generally achieves higher accuracy.

## Q30: What is Gradient Boosting?
**A:** Gradient Boosting builds an ensemble of weak learners (typically shallow trees) sequentially, where each new model fits the residuals (gradients) of the previous ensemble. The final prediction is the sum of all models. Key hyperparameters: learning_rate (shrinkage), n_estimators, max_depth, subsample. Popular implementations: XGBoost, LightGBM, CatBoost, scikit-learn GradientBoosting.

## Q31: What is XGBoost?
**A:** XGBoost (eXtreme Gradient Boosting) is an optimized gradient boosting library. Advantages: 1) Regularization (L1/L2) to prevent overfitting, 2) Parallel processing (uses all CPU cores), 3) Tree pruning with max_depth, 4) Handling missing values (learns best direction), 5) Built-in cross-validation, 6) Column block for cache-aware access, 7) GPU support.

## Q32: What is LightGBM?
**A:** LightGBM is a gradient boosting framework using histogram-based algorithms and GOSS (Gradient-based One-Side Sampling) for faster training. Key features: leaf-wise tree growth (instead of level-wise), categorical feature support, faster than XGBoost on large data, lower memory usage. Leaf-wise growth can overfit on small data (control with num_leaves, min_data_in_leaf).

## Q33: What is the difference between XGBoost and LightGBM?
**A:** XGBoost: level-wise tree growth, pre-sorted algorithm (exact greedy), handles small data better, more mature ecosystem. LightGBM: leaf-wise tree growth (can overfit), histogram-based algorithm (faster), GOSS for speed, native categorical support, better for very large datasets. Both are state-of-the-art for tabular data.

## Q34: What is SVM (Support Vector Machine)?
**A:** SVM finds the hyperplane that best separates classes with the maximum margin. Support vectors are the closest points to the hyperplane. Kernel trick: maps data to higher dimensions for non-linear separation. Kernels: linear, polynomial, RBF (Gaussian), sigmoid. Parameters: C (regularization), gamma (RBF spread). SVMs are effective in high-dimensional spaces.

## Q35: What is the kernel trick in SVM?
**A:** The kernel trick computes dot products in a transformed feature space without explicitly transforming the data. A kernel function K(xi, xj) computes similarity in the transformed space. RBF kernel: K(xi, xj) = exp(-γ||xi-xj||^2). This enables SVM to find non-linear decision boundaries while keeping optimization convex.

## Q36: What is K-Nearest Neighbors (KNN)?
**A:** KNN is a non-parametric, lazy learning algorithm that classifies based on majority vote of k nearest training samples (or averages for regression). Distance metrics: Euclidean, Manhattan, Minkowski, cosine. Key hyperparameter: k (number of neighbors). Pros: simple, no training phase, works for non-linear data. Cons: slow prediction, sensitive to scaling, curse of dimensionality.

## Q37: What is K-Means clustering?
**A:** K-Means partitions data into k clusters by minimizing within-cluster variance. Steps: 1) Initialize k centroids, 2) Assign each point to nearest centroid, 3) Recompute centroids as mean of assigned points, 4) Repeat 2-3 until convergence. Initialization: k-means++ (smart initialization). Limitations: assumes spherical clusters, sensitive to outliers, need to choose k.

## Q38: How do you choose the optimal K in K-Means?
**A:** Elbow method: plot within-cluster sum of squares (WCSS) vs k, look for elbow (diminishing returns). Silhouette score: measures cohesion vs separation (range -1 to 1, higher is better). Gap statistic: compares WCSS to null reference. Domain knowledge: business requirements for number of segments.

## Q39: What is Hierarchical Clustering?
**A:** Hierarchical clustering builds a tree of clusters (dendrogram). Agglomerative (bottom-up): each point starts as its own cluster, merges closest pairs. Divisive (top-down): start with one cluster, recursively split. Linkage criteria: single (min distance), complete (max distance), average, Ward (minimize variance increase). No need to specify k upfront.

## Q40: What is DBSCAN?
**A:** DBSCAN (Density-Based Spatial Clustering of Applications with Noise) groups points that are close together, marking outliers as noise. Parameters: eps (neighborhood radius), min_samples (minimum points for dense region). Advantages: finds arbitrary-shaped clusters, handles outliers, no need to specify k. Disadvantages: sensitive to eps parameter, struggles with varying densities.

## Q41: What is the difference between K-Means and DBSCAN?
**A:** K-Means: assumes spherical clusters, requires k, sensitive to initialization and outliers, assigns all points to clusters. DBSCAN: finds arbitrary shapes, no need for k, identifies outliers as noise, density-based. K-Means is faster and simpler; DBSCAN is more flexible for real-world data with noise and non-spherical clusters.

## Q42: What is dimensionality reduction?
**A:** Dimensionality reduction reduces the number of features while preserving essential information. Benefits: reduces overfitting, faster training, better visualization, removes multicollinearity. Methods: PCA (unsupervised, linear), t-SNE (unsupervised, non-linear, visualization), UMAP (fast, non-linear), LDA (supervised, linear), Autoencoders (neural network-based).

## Q43: What is the difference between PCA and LDA?
**A:** PCA is unsupervised — finds directions of maximum variance, ignores class labels. LDA is supervised — finds directions that maximize class separability (between-class variance / within-class variance). Both are linear. LDA is better for classification tasks with labeled data; PCA is better for general dimensionality reduction and unsupervised settings.

## Q44: What is Naive Bayes?
**A:** Naive Bayes is a probabilistic classifier based on Bayes' theorem with the naive assumption of conditional independence between features given the class. Despite this assumption, it performs well for text classification (spam detection, sentiment analysis). Variants: Gaussian (continuous), Multinomial (counts), Bernoulli (binary). Fast, scales well, works with high-dimensional data.

## Q45: What is the difference between Gaussian Naive Bayes and Multinomial Naive Bayes?
**A:** Gaussian NB assumes features follow a normal distribution — used for continuous data. Multinomial NB assumes features represent counts/frequencies — used for text classification with word counts or TF-IDF. Bernoulli NB assumes binary features (word present/absent). Choose based on feature distribution: Gaussian for real-valued, Multinomial for counts, Bernoulli for binary.

## Q46: What is Gradient Descent?
**A:** Gradient descent is an iterative optimization algorithm that minimizes a loss function by updating parameters in the opposite direction of the gradient. Types: Batch GD (full dataset per step), Stochastic GD (SGD, one sample at a time), Mini-batch GD (batches of samples). Learning rate controls step size. Variants: Momentum, Adam, RMSprop, Adagrad.

## Q47: What is the learning rate in gradient descent?
**A:** The learning rate determines step size during optimization. Too high: may overshoot minimum, diverge. Too low: slow convergence, may get stuck in local minima. Typical values: 0.001 to 0.1. Scheduling: reduce on plateau, step decay, cosine annealing. Adaptive methods (Adam) automatically adjust per-parameter learning rates.

## Q48: What is the difference between Batch Gradient Descent and SGD?
**A:** Batch GD computes gradient on full dataset — accurate but slow for large data, memory-intensive. SGD computes gradient on one sample — fast updates, noisy convergence, can escape local minima. Mini-batch GD (batch size 32-256) balances both: efficient on GPUs, stable convergence. SGD with momentum reduces noise.

## Q49: What is Ensemble Learning?
**A:** Ensemble learning combines multiple models to produce better predictions than any single model. Types: Voting (hard=majority class, soft=probability average), Bagging (train models on bootstrap samples, e.g., Random Forest), Boosting (sequential correction, e.g., XGBoost), Stacking (train meta-model on base model predictions). Ensembles reduce variance (bagging) or bias (boosting).

## Q50: What is Stacking?
**A:** Stacking (stacked generalization) trains a meta-model to combine predictions from multiple base models. Level 0: diverse base models (Random Forest, SVM, XGBoost). Level 1: meta-model (often Logistic Regression) trained on base model predictions. Usually uses out-of-fold predictions for training the meta-model to avoid overfitting.

## Q51: What is the curse of dimensionality?
**A:** As the number of features increases, the feature space becomes sparse, requiring exponentially more data to maintain statistical significance. Problems: distance metrics become less meaningful (all points appear equally far), overfitting increases, computation grows. Solutions: dimensionality reduction, feature selection, regularization.

## Q52: What are outliers and how do you handle them?
**A:** Outliers are data points significantly different from others. Detection: Z-score (>3), IQR method (outside Q1-1.5*IQR or Q3+1.5*IQR), Isolation Forest, LOF, DBSCAN. Handling: remove (if error), cap/winsorize (clip at percentiles), transform (log, Box-Cox), treat separately (as a class), use robust algorithms (tree-based, Huber loss).

## Q53: What is the difference between parametric and non-parametric models?
**A:** Parametric models assume a fixed functional form with a finite number of parameters (Linear Regression, Logistic Regression). Advantages: faster to train, require less data, more interpretable. Non-parametric models make no assumptions about data distribution (KNN, Decision Trees, SVM with RBF). Advantages: more flexible, better for complex patterns, more data needed.

## Q54: What is the bias in machine learning?
**A:** ML bias types: 1) Data bias — training data doesn't represent the population, 2) Algorithmic bias — algorithm favors certain groups, 3) Confirmation bias — results interpreted to confirm existing beliefs, 4) Measurement bias — features don't accurately capture the concept. Mitigation: diverse data, fairness metrics, bias audits, transparent modeling.

## Q55: What is imbalanced data and how do you handle it?
**A:** Imbalanced data has unequal class distribution (e.g., 99% negative, 1% positive). Handling: 1) Resampling — oversample minority (SMOTE, ADASYN), undersample majority, 2) Algorithm-level — class weights, cost-sensitive learning, 3) Ensemble — BalancedRandomForest, EasyEnsemble, 4) Anomaly detection approach for extreme imbalance, 5) Evaluation — use precision/recall/F1/AUC not accuracy.

## Q56: What is SMOTE?
**A:** SMOTE (Synthetic Minority Oversampling Technique) generates synthetic samples for the minority class. For a minority sample, finds k-nearest neighbors, creates new samples along the line connecting to random neighbors. More nuanced than simple duplication. Variants: Borderline-SMOTE, SMOTE-ENN (cleaning). Works best with continuous features; needs careful validation.

## Q57: What is the train-test split and why is it important?
**A:** Train-test split divides data into training (e.g., 80%) and testing (e.g., 20%) sets. The model learns from training data, and test data evaluates generalization on unseen data. Without proper split, you can't assess real-world performance. Stratified split preserves class proportions. Time-series: use temporal split (train on past, test on future).

## Q58: What is the difference between validation set and test set?
**A:** Validation set is used during model development for hyperparameter tuning and model selection. Test set is held out until final evaluation — used only once to estimate real-world performance. Using test set multiple times leaks information and overestimates performance. Use cross-validation on train+val for tuning; test set is sacred.

## Q59: What is hyperparameter tuning?
**A:** Hyperparameters are parameters set before training (not learned). Tuning searches for optimal values. Methods: Grid Search (exhaustive), Random Search (random combinations — more efficient), Bayesian Optimization (model-based search), Hyperband (adaptive resource allocation). Key hyperparameters vary by algorithm: learning_rate, max_depth, C, gamma, n_estimators.

## Q60: What is the difference between Grid Search and Random Search?
**A:** Grid Search exhaustively tries all combinations — guaranteed to find best in grid but expensive with many parameters. Random Search samples random combinations — more efficient, especially when some hyperparameters are more important than others. Random Search often finds equivalent or better results in fewer iterations.

## Q61: What is Bayesian Optimization?
**A:** Bayesian Optimization uses a probabilistic surrogate model (Gaussian Process) to model the objective function. It balances exploration (trying uncertain regions) and exploitation (trying promising regions) via acquisition function (Expected Improvement, UCB). More sample-efficient than grid/random search for expensive evaluations (e.g., deep learning).

## Q62: What is the F1 score?
**A:** F1-score is the harmonic mean of precision and recall: F1 = 2 * (precision * recall) / (precision + recall). Harmonic mean penalizes extreme values. F1 ranges [0,1], 1 is perfect, 0 is worst. Macro-F1: average F1 across classes (treats all classes equally). Weighted-F1: weighted by class support. Micro-F1: global metric (equals accuracy for multi-class).

## Q63: What is AUC-ROC?
**A:** AUC-ROC (Area Under the Receiver Operating Characteristic curve) measures the model's ability to distinguish between classes across all thresholds. AUC=1: perfect separation. AUC=0.5: no discrimination (random). AUC is threshold-independent and scale-invariant. AUC measures ranking quality: probability that a random positive is ranked higher than a random negative.

## Q64: What is the difference between AUC-ROC and AUC-PR?
**A:** AUC-ROC: plots TPR vs FPR — optimistic for imbalanced data (high AUC even with many false positives). AUC-PR: plots Precision vs Recall — more informative for imbalanced datasets. AUC-PR focuses on the positive class and reveals poor performance on minority class better than AUC-ROC.

## Q65: What is Multi-collinearity?
**A:** Multi-collinearity occurs when features are highly correlated. Problems: unstable coefficient estimates in linear models, difficult to interpret feature importance, increased variance. Detection: correlation matrix, Variance Inflation Factor (VIF > 5-10). Solutions: remove correlated features, PCA, ridge regression (L2 handles multi-collinearity), feature selection.

## Q66: What is One-Hot Encoding?
**A:** One-Hot Encoding converts categorical variables into binary columns — one column per category with 0/1 values. Avoids implying ordinal relationships. Problem: creates many columns for high-cardinality features (curse of dimensionality). Solutions: compress frequent categories, target encoding, hash encoding, embedding.

## Q67: What is Label Encoding vs One-Hot Encoding?
**A:** Label Encoding assigns integers to categories (0, 1, 2...) — implies ordinal relationship (2 > 1 > 0). Fine for ordinal data (small, medium, large). Bad for nominal data (red, blue, green) — model learns false order. One-Hot Encoding creates binary columns — no ordinal assumptions. Use One-Hot for nominal, Label for ordinal.

## Q68: What is Target Encoding?
**A:** Target Encoding replaces a categorical value with the mean of the target for that category (e.g., average price per city). Risk: target leakage (category-target relationship leaks into training). Mitigation: use cross-validation encoding (compute encoding within each fold), add smoothing (blend with global mean). Useful for high-cardinality categorical features.

## Q69: What is the difference between Parametric and Non-parametric models?
**A:** Parametric: fixed number of parameters, assumes data distribution (Linear Regression, Naive Bayes). Faster, requires less data. Non-parametric: parameters grow with data (KNN, Decision Trees, SVM). More flexible, needs more data. Non-parametric isn't parameter-free — the number of parameters depends on data size.

## Q70: What is the No Free Lunch Theorem in ML?
**A:** No single algorithm performs best for all problems. An algorithm's superior performance on one problem implies worse performance on another. This means: 1) Need to try multiple algorithms per problem, 2) Domain knowledge matters, 3) Ensemble methods work because they combine different biases, 4) No universal best ML algorithm.

## Q71: What is Transfer Learning in ML?
**A:** Transfer Learning applies knowledge from a pre-trained model to a new but related task. Instead of training from scratch, you start with weights learned on a large dataset and fine-tune on your smaller dataset. Common in deep learning (ImageNet pre-trained CNNs, BERT/GPT for NLP). Benefits: less data needed, faster training, better performance.

## Q72: What is Active Learning?
**A:** Active Learning is a strategy where the algorithm selects the most informative unlabeled data points to be labeled by an oracle (human). Reduces labeling cost. Query strategies: uncertainty sampling (least confident), margin sampling (smallest difference between top two), entropy, query-by-committee, diversity sampling. Used when labeling is expensive.

## Q73: What is Semi-Supervised Learning?
**A:** Semi-supervised learning uses a small amount of labeled data + large amount of unlabeled data. Methods: self-training (pseudo-labeling), co-training (two views), graph-based methods (label propagation), consistency regularization (mixMatch, FixMatch). Useful when labeling is expensive but unlabeled data is abundant.

## Q74: What is Reinforcement Learning?
**A:** Reinforcement Learning (RL) is about agents learning by interacting with an environment, receiving rewards/penalties. Key concepts: agent, environment, action, state, reward, policy, value function. Algorithms: Q-Learning, Deep Q-Networks (DQN), Policy Gradients, PPO, A3C, SAC. Used for: games, robotics, recommendation, autonomous driving.

## Q75: What is the difference between Q-Learning and Deep Q-Networks?
**A:** Q-Learning: tabular method — maintains Q-table of state-action values. Works for small, discrete state spaces. DQN: uses neural network to approximate Q-function — handles large/continuous state spaces. DQN additions: experience replay (breaks correlation), target network (stable target), exploration (epsilon-greedy).

## Q76: What is the exploration vs exploitation tradeoff?
**A:** Exploration: trying new actions to discover better rewards. Exploitation: using known actions that give high rewards. The tradeoff must balance learning (exploration) and performance (exploitation). Strategies: epsilon-greedy (random with probability e, decays over time), Upper Confidence Bound (UCB), Thompson Sampling, Boltzmann exploration.

## Q77: What is A/B testing in ML?
**A:** A/B testing compares two versions (control vs treatment) to determine which performs better. In ML: testing model A vs model B on live traffic. Steps: 1) Random split users, 2) Apply different models, 3) Measure metrics (conversion, revenue), 4) Statistical significance test. Challenges: network effects, carryover effects, multiple comparisons.

## Q78: What is MLOps?
**A:** MLOps (Machine Learning Operations) is the practice of deploying, monitoring, and maintaining ML models in production. Key components: 1) Version control (data, code, models), 2) CI/CD for ML pipelines, 3) Model registry, 4) Monitoring (data drift, model degradation), 5) Automated retraining, 6) Feature store, 7) Governance and compliance.

## Q79: What is data drift and model drift?
**A:** Data drift: the statistical properties of input data change over time (e.g., user behavior shifts, seasonality). Model drift: the relationship between features and target changes (concept drift). Detection: monitor prediction distribution, feature statistics, performance metrics. Mitigation: retrain periodically, online learning, adaptive models.

## Q80: What is SHAP in ML interpretability?
**A:** SHAP (SHapley Additive exPlanations) explains individual predictions using game theory. It computes feature contributions (Shapley values) — how much each feature changes the prediction from the baseline. Properties: local accuracy, consistency, missingness. Visualizations: summary plot, bar plot, dependence plot, force plot. Works with any model.

## Q81: What is LIME?
**A:** LIME (Local Interpretable Model-agnostic Explanations) explains individual predictions by approximating the model locally with a simple, interpretable model (linear model). It perturbs input data, gets predictions, and fits a local surrogate. LIME is faster but less stable than SHAP. Use LIME for quick explanations; use SHAP for consistent, theoretically grounded explanations.

## Q82: What is the difference between bagging and pasting?
**A:** Both train models on subsets of data. Bagging (Bootstrap Aggregating): samples with replacement (some data repeated, some omitted). Pasting: samples without replacement (each sample used at most once). Bagging introduces more diversity (≈63% of data used per model) and is more common. Random Forest uses bagging.

## Q83: What is Out-of-Bag (OOB) error?
**A:** For bagging (e.g., Random Forest), each tree is trained on ~63% of data. The remaining 37% (out-of-bag) can be used as a validation set without separate cross-validation. OOB error aggregates predictions for each sample using only trees where it was OOB. Provides unbiased estimate of generalization error.

## Q84: What is Feature Importance?
**A:** Feature importance measures how useful each feature is for predictions. Methods: 1) Built-in (tree-based: Gini importance, XGBoost: gain/cover/frequency), 2) Permutation importance (shuffle feature and measure performance drop), 3) Coefficient magnitude (linear models), 4) SHAP values (feature contribution magnitude). Helps with feature selection and interpretation.

## Q85: What is Permutation Feature Importance?
**A:** Permutation importance measures the increase in prediction error when a feature's values are randomly shuffled. This breaks the feature-target relationship. A large increase means the feature is important. Model-agnostic, can be computed on test set. More reliable than built-in impurity-based importance for tree models (which can be biased).

## Q86: What is Partial Dependence Plot (PDP)?
**A:** PDP shows the marginal effect of one or two features on the predicted outcome. It averages predictions across all other features at different values of the feature of interest. Helps understand: relationship direction (linear, monotonic, complex), interactions between two features, and feature impact on predictions.

## Q87: What is a learning curve?
**A:** A learning curve plots training/validation performance vs training set size. Helps diagnose: high bias (curves converge at high error), high variance (large gap between curves), and sufficiency of data. Also: performance vs training iterations (epoch curves) to check convergence and overfitting.

## Q88: What is the difference between a validation curve and a learning curve?
**A:** Validation curve plots training/validation scores vs a hyperparameter value (e.g., max_depth, regularization strength). Helps tune hyperparameters and detect overfitting. Learning curve plots scores vs training set size — helps diagnose bias/variance and determine if more data helps.

## Q89: What is Early Stopping?
**A:** Early stopping halts training when validation performance stops improving for a specified number of iterations (patience). Prevents overfitting by stopping before the model memorizes noise. Saves time and computation. Used in: neural networks, gradient boosting (XGBoost early_stopping_rounds), iterative algorithms.

## Q90: What is the difference between parametric and non-parametric density estimation?
**A:** Parametric: assumes a distribution (e.g., Gaussian Mixture Models). Non-parametric: data-driven (Kernel Density Estimation, histogram). Parametric is simpler but biased if assumption wrong. Non-parametric is flexible but needs more data and is computationally expensive. KDE estimates density as sum of kernel functions centered at data points.

## Q91: What is Gaussian Mixture Model (GMM)?
**A:** GMM models data as a mixture of multiple Gaussian distributions. Each component has: mean, covariance, weight. Estimated via Expectation-Maximization (EM) algorithm. Soft clustering (each point has probability of belonging to each cluster). More flexible than K-Means (captures ellipsoidal clusters of different sizes). Choose components via BIC/AIC.

## Q92: What is the Expectation-Maximization (EM) algorithm?
**A:** EM iteratively estimates parameters in models with latent variables. E-step: estimate missing/latent data given current parameters. M-step: maximize likelihood given the completed data. Used for: GMM, hidden Markov models, missing data imputation. Converges to local optimum (may need multiple random initializations).

## Q93: What is the difference between generative and discriminative models?
**A:** Generative models learn P(X, Y) — joint distribution of features and labels. Can generate new data. Examples: Naive Bayes, GMM, HMM, GANs, VAEs. Discriminative models learn P(Y|X) — conditional probability of label given features. Focus on decision boundary. Examples: Logistic Regression, SVM, neural networks. Discriminative generally performs better for classification.

## Q94: What is Anomaly Detection?
**A:** Anomaly detection identifies rare items/events that differ significantly from the majority. Types: point anomalies (single data point), contextual anomalies (anomalous in context), collective anomalies (group of related points). Methods: statistical (Z-score, IQR), proximity-based (KNN, LOF), clustering (DBSCAN), tree-based (Isolation Forest), neural (Autoencoders).

## Q95: What is Isolation Forest?
**A:** Isolation Forest detects anomalies by isolating observations. Anomalies are few and different — they are easier to isolate (require fewer random splits). Builds random trees, measures path length to isolate each point. Short path = anomaly. Advantages: linear time complexity, handles high dimensions, no need to define normal. Works well for high-dimensional data.

## Q96: What is Association Rule Mining?
**A:** Association rule mining finds relationships between variables in large datasets. Apriori algorithm: finds frequent itemsets, generates association rules. Metrics: Support (frequency of itemset), Confidence (conditional probability), Lift (how much more likely items occur together than independently). Used for market basket analysis, recommendation.

## Q97: What is the Apriori Principle?
**A:** If an itemset is frequent, then all its subsets are also frequent. Conversely, if an itemset is infrequent, all its supersets are infrequent. Used to prune the search space in association rule mining. Algorithm iteratively generates candidate itemsets and prunes those with infrequent subsets.

## Q98: What is the difference between correlation and causation?
**A:** Correlation: two variables move together (positive or negative). Causation: one variable directly causes a change in another. Correlation does not imply causation. Confounding variables (third factor causing both) can create spurious correlations. Establish causation: randomized controlled trials, natural experiments, instrumental variables, Granger causality (time series).

## Q99: What is the difference between parametric and non-parametric statistical tests?
**A:** Parametric tests (t-test, ANOVA, Pearson correlation): assume normal distribution, equal variances. More powerful when assumptions hold. Non-parametric tests (Mann-Whitney U, Kruskal-Wallis, Spearman): no distribution assumptions, work with ordinal data, less powerful but more robust. Use parametric for normally distributed data; non-parametric otherwise.

## Q100: What are the emerging trends in Machine Learning?
**A:** Trends: 1) AutoML (automated model selection, hyperparameter tuning, feature engineering), 2) Federated Learning (train on decentralized data without sharing), 3) TinyML (on-device ML for edge/IoT), 4) Causal ML (beyond correlation to causation), 5) Responsible AI (fairness, interpretability, privacy), 6) LLM-integrated ML pipelines, 7) ML on graphs (GNNs), 8) Self-supervised learning (no labels needed).
