# Q-Learning for Recommendations

## Overview

Q-learning is a model-free reinforcement learning algorithm that learns the optimal action-value function (Q-function) to maximize cumulative reward. In recommendation systems, Q-learning frames the problem as a Markov Decision Process (MDP) where the system learns to select items that maximize long-term user engagement, rather than optimizing for immediate clicks or conversions.

---

## State/Action/Reward Design

### MDP Formulation

| Component | Definition | Example |
|---|---|---|
| **State (S)** | User's current context and history | User features + recent interactions + context |
| **Action (A)** | Item to recommend | Select from item catalog |
| **Reward (R)** | User feedback signal | Click (+1), purchase (+5), ignore (0), dislike (-1) |
| **Transition (P)** | State change after action | New interaction history after recommendation |
| **Discount factor (γ)** | Importance of future rewards | 0.9–0.99 (balance short vs. long term) |

### State Design

The state encodes all information needed to make the next decision:

| State Component | Description | Dimensionality |
|---|---|---|
| **User profile** | Demographics, preferences | Low (10–50 features) |
| **Interaction history** | Recent item interactions | Variable (sequence of embeddings) |
| **Session context** | Time, device, location | Low (5–10 features) |
| **Item features** | Properties of recently interacted items | Variable |
| **Aggregate statistics** | Session-level metrics | Low (5–10 features) |

### Reward Design

| Reward Signal | Value | Rationale |
|---|---|---|
| **Click** | +1 | User showed interest |
| **Long dwell time** | +2 | Strong engagement signal |
| **Add to cart** | +3 | High intent signal |
| **Purchase** | +5 | Strongest positive signal |
| **Skip/ignore** | 0 | No engagement |
| **Negative feedback** | -2 | Explicit disinterest |
| **Report** | -5 | Very negative signal |

### Reward Shaping

Poor reward design leads to suboptimal policies. Common reward shaping techniques:

- **Dense rewards**: Provide intermediate rewards for partial engagement (scroll depth, time spent) rather than only final outcomes (purchase).
- **Decay rewards**: Weight recent rewards more heavily to adapt to changing preferences.
- **Diversity bonus**: Add reward for recommending diverse items to avoid filter bubbles.
- **Serendipity bonus**: Reward unexpected but positively received recommendations.

---

## Deep Q-Networks (DQN)

### Why Deep Q-Learning?

The Q-table (mapping state-action pairs to Q-values) is intractable for large state spaces (continuous features, high-dimensional embeddings). DQN uses a neural network to approximate the Q-function:

**Q(s, a; θ) ≈ Q*(s, a)**

Where θ are the neural network parameters.

### DQN Architecture for Recommendations

| Layer | Input | Output | Purpose |
|---|---|---|---|
| **State encoder** | User features, context | State embedding | Compress state to fixed-dim vector |
| **Action embedding** | Item features | Action embedding | Represent candidate items |
| **Q-network** | State embedding × action embedding | Q-value | Score each action |

### DQN Training

1. **Experience replay**: Store (state, action, reward, next_state) transitions in a replay buffer.
2. **Mini-batch sampling**: Sample random mini-batches from the replay buffer.
3. **Target computation**: Compute target Q-values using the target network.
4. **Loss**: Minimize (Q(s,a; θ) - target)² where target = r + γ × max_a' Q(s', a'; θ_target).
5. **Update**: Backpropagate and update the Q-network.
6. **Periodic target update**: Copy Q-network parameters to the target network every N steps.

---

## Experience Replay

### Why Experience Replay?

- **Breaks correlation**: Consecutive experiences are correlated. Random sampling breaks this correlation.
- **Reuses data**: Each experience is used in multiple updates, improving sample efficiency.
- **Stabilizes training**: Reduces variance in updates by averaging over diverse experiences.

### Replay Buffer Design

| Parameter | Description | Typical Value |
|---|---|---|
| **Buffer size** | Maximum stored transitions | 100K–1M |
| **Sampling strategy** | How transitions are selected | Uniform, prioritized |
| **Minimum buffer size** | Transitions before training starts | 1K–10K |
| **Priority exponent** | Priority for prioritized replay | 0.6 |
| **Importance sampling** | Correct for priority bias | 0.4–1.0 |

### Prioritized Experience Replay

Not all experiences are equally important. Prioritized replay samples transitions with high TD-error more frequently:

**Priority(i) = |δ_i|^α + ε**

Where δ_i is the TD-error (how surprising the transition was) and α controls prioritization strength.

---

## Target Networks

### Stabilizing DQN Training

Without target networks, DQN training is unstable because the target values change with every parameter update:

- **Problem**: Moving target → oscillating/diverging training.
- **Solution**: Use a separate target network with frozen parameters for computing target Q-values.
- **Update frequency**: Copy Q-network parameters to target network every C steps (C = 1000–10000).

### Soft Target Updates

Instead of hard copy, use exponential moving average:

**θ_target ← τ × θ + (1-τ) × θ_target**

Where τ = 0.001–0.01 (small τ = slow, stable updates).

---

## Offline Q-Learning

### Why Offline RL for Recommendations?

Online RL requires live interaction with users, which is risky in production (exploration can degrade user experience). Offline RL learns from logged historical data:

- **No exploration risk**: Train on past data without affecting live users.
- **Data abundance**: Recommendation systems generate massive logged data.
- **Safety**: Avoid recommending items that might harm user experience.

### Offline RL Challenges

| Challenge | Description | Mitigation |
|---|---|---|
| **Distribution shift** | Policy trained on old data, deployed on new distribution | Conservative Q-learning, importance weighting |
| **Exploration** | Cannot explore new actions in offline setting | Conservative value estimation |
| **Data quality** | Logged data may have biases | Debiased logging, counterfactual evaluation |
| **Reward sparsity** | Many transitions have zero reward | Reward shaping, hierarchical RL |

### Conservative Q-Learning (CQL)

CQL adds a conservative penalty to prevent overestimation of Q-values for actions not seen in the training data:

**L_CQL = L_DQN + α × (E_a~π[a] [Q(s,a)] - E_a~D [Q(s,a)])**

This penalizes the policy for preferring actions with high Q-values that are not supported by the logged data.
