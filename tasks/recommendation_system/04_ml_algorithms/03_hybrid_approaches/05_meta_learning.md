# Meta-Learning for Hybrid Recommendations

## Overview

Meta-learning ("learning to learn") applies to recommendation hybridization by learning how to optimally combine multiple recommendation models based on context. Rather than using fixed combination rules, meta-learning approaches learn dynamic weighting, model selection, and combination strategies from data. This enables the system to adapt to different users, items, and contexts without manual rule engineering.

---

## Learning to Combine Models

### Meta-Learning Framework

The meta-learner takes as input:
- **Base model predictions**: Scores from CF, content-based, and other models.
- **Context features**: User features, item features, request context.
- **Meta-features**: Features that describe the current situation (cold-start flags, confidence scores, data availability).

And outputs:
- **Combination weights**: How much to trust each base model.
- **Final score**: The combined recommendation score.

### Combination Architectures

| Architecture | Description | Complexity |
|---|---|---|
| **Linear combination** | Weighted sum with learned weights | Low |
| **Gating network** | Neural network that outputs combination weights | Medium |
| **Attention-based** | Self-attention over model predictions | Medium-High |
| **Mixture of experts** | Each model is an expert, gating selects experts | High |
| **Stacking** | Train a meta-model on base model predictions | Medium |

### Gating Network

A gating network learns to weight base models based on context:

**final_score = Σ_i (g_i(context) × score_i)**

Where g_i is the output of a neural network conditioned on context features. The gating network learns, for example:
- To weight CF more heavily when user interaction history is rich.
- To weight content-based more heavily for new items.
- To weight the deep learning model more when contextual features are informative.

---

## Attention-Based Model Selection

### Cross-Model Attention

Apply attention mechanisms over the predictions of multiple models:

**Attention weights = softmax(Query × Key^T / √d)**

Where:
- **Query**: Context features (user, item, request).
- **Key**: Model predictions and confidence scores.
- **Value**: Model predictions.

The attention mechanism learns to focus on the most relevant model for each context.

### Multi-Head Attention for Model Combination

Use multiple attention heads to capture different aspects of model relevance:

- **Head 1**: Focuses on user interaction patterns → weights CF-based models.
- **Head 2**: Focuses on item content features → weights content-based models.
- **Head 3**: Focuses on contextual signals → weights context-aware models.

The final combination is the concatenation (or sum) of all attention heads' outputs.

### Self-Attention Across Models

Treat each model's prediction as a token in a sequence and apply self-attention:

- Models that agree reinforce each other.
- Models that disagree attend to each other's predictions for resolution.
- The attention weights reveal which models are most informative for each prediction.

---

## Context-Aware Hybridization

### Context Dimensions

| Context Dimension | Impact on Model Selection |
|---|---|
| **User cold-start level** | More cold start → more content-based weight |
| **Item popularity** | More popular → more CF weight |
| **Time of day** | Different user behavior patterns → different model effectiveness |
| **Device type** | Mobile users may have different preferences → context-specific models |
| **Session depth** | Early in session → more exploration; late → more exploitation |
| **User segment** | Different segments respond to different recommendation strategies |

### Context-Dependent Weighting

The meta-learner can produce context-dependent weights:

| Context | CF Weight | Content Weight | Popularity Weight |
|---|---|---|---|
| New user, popular item | 0.1 | 0.7 | 0.2 |
| New user, new item | 0.0 | 0.9 | 0.1 |
| Active user, popular item | 0.8 | 0.1 | 0.1 |
| Active user, niche item | 0.6 | 0.3 | 0.1 |
| Returning user | 0.5 | 0.4 | 0.1 |

---

## Dynamic Model Weighting

### Online Weight Adaptation

Weights can be adapted in real-time based on online feedback:

1. **Initial weights**: Set by the meta-learner based on context.
2. **Online feedback**: Observe user response (click, dwell time, purchase).
3. **Weight update**: Adjust weights based on which model's prediction was correct.
4. **Convergence**: Over a session, weights converge to the optimal combination for that user.

### Thompson Sampling for Model Selection

Treat each model as an arm in a multi-armed bandit:

- **Reward**: User engagement (click, purchase) when using that model's recommendation.
- **Prior**: Beta distribution for each model (successes, failures).
- **Selection**: Sample from each model's posterior and select the model with the highest sample.
- **Update**: Update the posterior with the observed reward.

### Exploitation vs. Exploration in Model Weighting

| Strategy | Description |
|---|---|
| **Greedy** | Always use the model with the highest historical reward |
| **ε-greedy** | Randomly explore with probability ε |
| **Thompson Sampling** | Bayesian exploration based on posterior uncertainty |
| **UCB** | Optimistically explore models with high uncertainty |

---

## Training Meta-Learners

### Training Approaches

| Approach | Description | Pros | Cons |
|---|---|---|---|
| **End-to-end** | Train meta-learner jointly with base models | Optimal joint optimization | Complex, requires large data |
| **Sequential** | Train base models first, then meta-learner | Simpler, modular | Sub-optimal combination |
| **Online** | Adapt meta-learner weights online | Adapts to distribution shift | Requires online learning infrastructure |

### Loss Functions for Meta-Learning

- **Pairwise loss**: Optimize the ranking of combined predictions (BPR, WARP).
- **Pointwise loss**: Optimize the accuracy of combined predictions (MSE, log loss).
- **Listwise loss**: Optimize the quality of the entire ranked list (ListMLE, LambdaRank).
- **Exploration bonus**: Add an exploration term to encourage trying less-used models.

### Meta-Learning Evaluation

- **Offline**: Compare meta-learned combinations against fixed-weight baselines using standard metrics (NDCG, MAP, RMSE).
- **Online**: A/B test meta-learned combinations against baselines, measuring engagement, conversion, and user satisfaction.
- **Ablation**: Remove individual models from the combination to measure each model's contribution.
- **Interpretability**: Analyze learned weights to verify they make intuitive sense (e.g., CF weight increases with interaction count).
