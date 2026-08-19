# Domain Adaptation for Recommendation Systems

## Overview

Domain adaptation enables transferring knowledge from a data-rich source domain to a data-scarce target domain. For recommendation systems, this is critical when launching in new markets, new verticals, or serving new user populations where interaction data is limited. This covers transfer strategies, fine-tuning approaches, divergence measurement, and adversarial adaptation.

---

## Transfer from Public to Private Datasets

### Source and Target Domains

| Domain Type | Data Richness | Example |
|------------|--------------|---------|
| Source (public) | Millions of interactions | Public movie ratings, Amazon reviews |
| Target (private) | Thousands of interactions | Company's internal product catalog |

### Transfer Learning Pipeline

1. **Pre-train** on large source domain dataset
2. **Analyze** domain divergence between source and target
3. **Select** adaptation strategy based on divergence level
4. **Fine-tune** on target domain data
5. **Evaluate** transfer effectiveness (target-only vs. transfer vs. source-only)

### When Transfer Helps

- Target domain has < 10K interactions (cold start)
- Source and target share similar user behavior patterns
- Feature spaces overlap significantly (common item attributes)
- Target domain has similar interaction structure (implicit vs explicit feedback)

### When Transfer Hurts (Negative Transfer)

- Domains have fundamentally different user preferences
- Feature distributions are very different
- Target domain has sufficient data for independent training
- Source domain contains biases not present in target

---

## Fine-Tuning Strategies

### Freeze Layers Strategy

Freeze lower layers (shared representations) and fine-tune upper layers (domain-specific):

| Layer Type | Freeze Status | Rationale |
|-----------|--------------|-----------|
| Feature embeddings | Freeze (shared) | General feature representations |
| Lower interaction layers | Freeze | Generic pattern extraction |
| Upper interaction layers | Train (domain-specific) | Domain-specific combinations |
| Output tower | Train (domain-specific) | Domain-specific prediction |
| Batch norm layers | Freeze or update slowly | Prevent distribution shift damage |

### Gradual Unfreezing

1. Train output tower only for N epochs (other layers frozen)
2. Unfreeze top interaction layer, train for M epochs
3. Unfreeze next layer down, train for P epochs
4. Continue until all layers are unfrozen (or stop earlier if overfitting)

**Benefits**:
- Prevents catastrophic forgetting of source knowledge
- Allows learning rate to stabilize before unfreezing deeper layers
- More stable training dynamics than immediate full fine-tuning
- Particularly effective when target data is very limited

### Learning Rate策略

| Component | Learning Rate | Rationale |
|-----------|-------------|-----------|
| Frozen layers | 0 | No updates |
| Newly unfrozen layers | 0.1× original LR | Small changes to learned representations |
| Output tower | 1.0× original LR | Domain-specific, can change faster |
| Embeddings (if training) | 0.01-0.1× original LR | Preserve general embeddings |

### Data Mixing Strategies

- **Source only**: Pre-train on source, no target data mixing
- **Target only**: Fine-tune on target only (no mixing)
- **Mixed training**: Combine source and target data with weighting
- **Curriculum mixing**: Start with source, gradually increase target proportion
- **Temperature mixing**: Oversample target data to balance representation

---

## Domain Divergence Measurement

### Feature Distribution Divergence

**Kullback-Leibler Divergence**:
- Measures how one probability distribution differs from another
- Asymmetric: KL(P||Q) ≠ KL(Q||P)
- Use for comparing feature distributions across domains

**Maximum Mean Discrepancy (MMD)**:
- Measures distance between two distributions in reproducing kernel Hilbert space
- Symmetric and non-parametric
- Lower MMD = more similar domains
- Can be computed per feature to identify divergent features

**Wasserstein Distance**:
- Measures the "earth mover's distance" between distributions
- More robust to distribution support mismatches
- Better gradient signal for optimization-based adaptation

### Behavioral Divergence

| Metric | What It Measures | Application |
|--------|-----------------|-------------|
| Interaction density | Clicks per user per session | Engagement pattern similarity |
| Item popularity distribution | Long-tail vs. uniform | Catalog bias comparison |
| Temporal patterns | Session length, frequency | Usage behavior similarity |
| Rating distribution | Mean, variance, skew | Feedback intensity comparison |
| Feature overlap | Common features across domains | Feature space compatibility |

### Divergence-Guided Strategy Selection

| Divergence Level | Strategy | Expected Transfer Benefit |
|-----------------|----------|--------------------------|
| Low (MMD < 0.1) | Direct fine-tuning | High |
| Medium (0.1 < MMD < 0.5) | Gradual unfreezing with data mixing | Moderate |
| High (MMD > 0.5) | Adversarial adaptation or train from scratch | Low-Moderate |

---

## Adversarial Domain Adaptation

### Concept

Train a domain discriminator that tries to identify which domain (source or target) a sample comes from. The feature extractor learns domain-invariant representations by fooling the discriminator.

### Architecture

```
Input → Feature Extractor → Domain Discriminator → Domain Label (source/target)
                                     ↓
                              Task Classifier → Prediction
```

### Training Dynamics

1. Train task classifier on source domain (supervised)
2. Train domain discriminator to classify source vs target
3. Train feature extractor to maximize discriminator loss (fool discriminator)
4. Alternate between discriminator and feature extractor updates
5. At inference, use only feature extractor + task classifier

### Applications to Recommendation Systems

- **Cross-market adaptation**: Transfer from established market to new market
- **Cross-category adaptation**: Transfer from electronics to fashion recommendations
- **Cold-start mitigation**: Use well-represented user groups as source domain
- **Platform migration**: Transfer from web to mobile recommendation patterns

### Gradient Reversal

- Use Gradient Reversal Layer (GRL) to reverse discriminator gradients
- Feature extractor learns representations that are indistinguishable across domains
- Simple to implement, effective in practice
- Requires careful balancing of task loss and domain adaptation loss

---

## Practical Considerations

### Measuring Transfer Success

- Compare target domain metrics with/without transfer
- Track negative transfer: when transfer hurts target performance
- Monitor feature importance changes during adaptation
- A/B test adapted model vs. target-only model vs. source-only model

### Common Pitfalls

- Overfitting to small target dataset (use strong regularization)
- Catastrophic forgetting of source knowledge (gradual unfreezing)
- Negative transfer when domains are too dissimilar (measure divergence first)
- Label distribution shift between domains (adjust for class imbalance)

### Best Practices

1. Always establish baselines: source-only, target-only, and transfer
2. Validate on held-out target domain data (never use for training)
3. Start with simple fine-tuning before trying adversarial methods
4. Monitor for negative transfer during adaptation
5. Document domain divergence metrics for future reference
