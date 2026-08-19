# Cold Start Problem in Recommendations

## Overview

The cold start problem occurs when a recommendation system cannot provide personalized recommendations because insufficient data is available about a new user, new item, or entirely new system. It is one of the most fundamental challenges in recommendation systems, affecting user acquisition (new users see irrelevant recommendations), item launch (new items get no exposure), and system bootstrap (new deployments have no interaction history).

---

## Types of Cold Start

### User Cold Start

A new user has no interaction history, so the system cannot infer their preferences. Collaborative filtering methods fail entirely—there is no user vector to factorize, no neighbors to match.

**Business impact:**
- New users receive generic (popularity-based) recommendations.
- Poor first impressions increase churn risk.
- User acquisition cost is wasted if users don't find relevant content.

### Item Cold Start

A new item has no interaction history, so the system cannot determine which users would like it. Even if user preferences are well-modeled, the item has no collaborative signal.

**Business impact:**
- New items receive no recommendations, reducing their exposure.
- Content creators and sellers are disadvantaged.
- The system biases toward established items, creating a popularity feedback loop.

### System Cold Start

A completely new recommendation system has no interaction data at all. No user-item matrix exists for collaborative filtering.

**Business impact:**
- The system must launch with non-personalized recommendations.
- Bootstrap data must be collected before collaborative methods become useful.
- The transition from non-personalized to personalized must be managed carefully.

---

## Content-Based Fallback

### Using Item Features for New Items

When a new item has no interaction history, use its content features to determine similarity to existing items:

| Feature Type | Examples | Similarity Method |
|---|---|---|
| Text | Title, description, tags | TF-IDF cosine similarity |
| Visual | Images, thumbnails | CNN embeddings, perceptual hashing |
| Audio | Music tracks, podcasts | Mel-frequency cepstral coefficients |
| Metadata | Category, brand, price, genre | Categorical/numerical similarity |
| Structural | Page layout, product attributes | Graph-based similarity |

### Content-Based User Modeling for New Users

When a new user has no interaction history, use explicitly provided information:

- **Demographics**: Age, gender, location (if provided during signup).
- **Stated preferences**: Onboarding quiz results ("What genres do you like?").
- **Context**: Device type, time of day, referral source.
- **Social signals**: Friends' preferences (if social login is used).

### Limitations of Content-Based Fallback

- **Feature quality**: Content features may not capture the aspects that drive user preferences.
- **Serendipity**: Content-based recommendations tend to be too similar (filter bubble).
- **No collaborative signal**: Cannot leverage the wisdom of the crowd.
- **Feature engineering cost**: Requires significant effort to extract meaningful content features.

---

## Onboarding Surveys

### Survey Design

Onboarding surveys collect user preferences explicitly during the first interaction:

| Survey Type | Questions | Time | Information Gained |
|---|---|---|---|
| **Category selection** | "Select categories you're interested in" | 10 seconds | Interest vectors |
| **Item rating** | "Rate these 10 items" | 30 seconds | Initial preference model |
| **Example-based** | "Which of these do you prefer?" | 15 seconds | Pairwise preferences |
| **Demographic** | "Age range, location" | 5 seconds | Demographic features |
| **Skip option** | "Skip for now" | 0 seconds | No information |

### Survey Optimization

- **Minimize friction**: Keep surveys short (< 30 seconds). Each additional question increases abandonment.
- **Visual choices**: Use images instead of text for faster, more intuitive responses.
- **Adaptive questions**: Show follow-up questions based on previous answers to efficiently explore the preference space.
- **Progressive profiling**: Collect a few preferences at onboarding, then learn more over subsequent sessions.
- **Incentivize completion**: Offer a small reward (e.g., better initial recommendations) for completing the survey.

### Survey-to-Model Pipeline

1. **Collect responses**: Store survey answers with user ID.
2. **Map to features**: Convert survey responses to feature vectors (category preferences, item ratings).
3. **Initialize model**: Use survey-derived features to initialize the user's latent factors.
4. **Update incrementally**: As the user interacts, update the model with the new signal, gradually replacing survey-derived features.

---

## Transfer Learning

### Cross-Domain Recommendations

Transfer learning leverages knowledge from a data-rich domain to improve recommendations in a data-sparse domain:

| Source Domain | Target Domain | Transfer Method |
|---|---|---|
| Movie ratings | Book recommendations | Shared user factors across domains |
| E-commerce purchases | Travel bookings | Transfer user preference embeddings |
| English content | Local language content | Cross-lingual embeddings |
| Desktop behavior | Mobile behavior | Cross-device user modeling |

### Pre-Training Strategies

- **Pre-train on auxiliary data**: Train a model on a related task with abundant data (e.g., predict item categories), then fine-tune on the sparse target task.
- **Shared embeddings**: Use pre-trained language or image models to generate item embeddings, bypassing the need for collaborative signals.
- **Meta-learning**: Learn a model that can quickly adapt to new users/items with few examples (MAML, Prototypical Networks).

### Transfer Learning for New Items

1. **Extract content features**: Use pre-trained models (BERT for text, ResNet for images) to generate item embeddings.
2. **Map to collaborative space**: Learn a mapping from content embeddings to the collaborative factor space.
3. **Hybrid representation**: Combine the mapped content embedding with any available collaborative signal.

---

## Exploration Strategies

### The Exploration-Exploitation Tradeoff

When a new user or item enters the system, the system must balance:

- **Exploitation**: Recommend items the system is confident the user will like (based on existing models).
- **Exploration**: Recommend items the system is uncertain about to gather information and improve future recommendations.

### Multi-Armed Bandits

Bandit algorithms provide a principled framework for the exploration-exploitation tradeoff:

| Algorithm | Strategy | Exploration Style |
|---|---|---|
| **ε-greedy** | Explore with probability ε, exploit otherwise | Random exploration |
| **UCB** | Select arm with highest upper confidence bound | Optimistic exploration |
| **Thompson Sampling** | Sample from posterior distribution of rewards | Bayesian exploration |
| **LinUCB** | UCB with contextual features | Contextual exploration |
| **Neural bandits** | Neural network reward model | Deep exploration |

### Bandit Application to Cold Start

**For new users:**
- Maintain a portfolio of recommendation strategies (popularity, content-based, diverse, niche).
- Use Thompson Sampling to allocate traffic across strategies, learning which works best for each new user.
- As interaction data accumulates, shift traffic toward the best-performing strategy.

**For new items:**
- Allocate a fraction of recommendation slots to new items (exploration budget).
- Track new item performance (CTR, conversion) during the exploration period.
- Promote items that perform well; demote items that don't.

### Exploration Budget

| Strategy | Budget | Risk | Learning Rate |
|---|---|---|---|
| Fixed exploration rate | 10% of traffic | Low (bounded exploration) | Moderate |
| Decaying exploration | Start high, decay over time | Low (exploration decreases) | Fast initially |
| Adaptive exploration | Increase exploration for uncertain users/items | Higher (more exploration) | Variable |
| A/B testing | Separate exploration and control groups | None (statistical rigor) | Slow (requires test duration) |

---

## Ensemble of Cold Start Strategies

### Strategy Cascade

The most effective approach combines multiple cold start strategies in a cascade:

1. **Level 0 (No data)**: Use content-based recommendations and popularity-based fallback.
2. **Level 1 (1–5 interactions)**: Incorporate onboarding survey results with content features.
3. **Level 2 (5–20 interactions)**: Transition to hybrid model (content + collaborative).
4. **Level 3 (20+ interactions)**: Full collaborative filtering model.

### Weighted Combination

Rather than hard switching, combine strategies with learned weights:

**score(item) = w_content × score_content + w_cf × score_cf + w_popularity × score_popularity**

Where weights are functions of the amount of data available:
- w_content decreases as collaborative signal accumulates.
- w_cf increases as the user interaction history grows.
- w_popularity decreases monotonically.

### Monitoring Cold Start Transition

- **Cold start percentage**: Track the fraction of users/items in each cold start level.
- **Transition velocity**: How quickly users move from level 0 to level 3.
- **Cold start quality**: Recommendation quality (CTR, engagement) for users at each cold start level.
- **Cold start impact**: Overall system quality impact of the cold start population.
