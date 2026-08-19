# Variational Autoencoders for Recommendation Systems

## Overview

Variational Autoencoders (VAEs) extend standard autoencoders by learning a structured probabilistic latent space rather than a deterministic encoding. For recommendations, VAEs model uncertainty in user preferences, enable diverse recommendations, support latent space interpolation, and handle cold-start through smooth generalization. The Mult-VAE variant for implicit feedback achieved state-of-the-art results and remains a foundational deep learning recommendation architecture.

---

## VAE Architecture

### Generative Model

VAEs frame recommendation as: sample latent preference `z ~ N(0, I)`, then generate interaction vector `x ~ p_θ(x|z)`. The encoder approximates the intractable posterior with `q_φ(z|x)`.

### Components

| Component | Input | Output | Purpose |
|-----------|-------|--------|---------|
| Encoder | User-item vector `x ∈ R^{|I|}` | μ, log σ² | Parameterize posterior distribution |
| Reparameterization | μ, σ, ε ~ N(0,I) | z = μ + σ⊙ε | Differentiable sampling |
| Decoder | Latent z ∈ R^d | Reconstructed x̂ ∈ R^{|I|}` | Generate interaction prediction |

**Encoder**: Fully-connected layers → two output heads (mean, log-variance)
**Decoder**: Fully-connected layers → softmax over item vocabulary (Mult-VAE) or linear (standard)
**Reparameterization trick**: `z = μ + σ ⊙ ε` routes stochasticity through `ε`, making sampling differentiable

---

## VAE Loss Function

### Evidence Lower Bound (ELBO)

```
ELBO = E_{q_φ(z|x)} [log p_θ(x|z)] - KL(q_φ(z|x) || p(z))
     = Reconstruction Loss - KL Divergence
```

**Reconstruction loss**: Measures decoder's ability to recover original interactions
- Bernoulli likelihood (binary feedback): Binary cross-entropy
- Multinomial likelihood (counts): Cross-entropy with softmax (Mult-VAE)
- Gaussian likelihood (ratings): Mean squared error

**KL divergence**: `KL = -0.5 × Σⱼ (1 + log σⱼ² - μⱼ² - σⱼ²)` — closed-form for diagonal Gaussians

KL forces the latent space to be smooth, compact, and generalizable.

### Loss Balancing

| β Value | Effect |
|---------|--------|
| β < 1 | Under-regularized; better reconstruction, worse generalization |
| β = 1 | Standard VAE |
| β > 1 | Smoother latent space; may hurt reconstruction |
| β >> 1 | Posterior collapse; decoder ignores latent variable |

---

## Mult-VAE: Multinomial Likelihood for Implicit Feedback

### Motivation

Standard VAEs with Bernoulli likelihood treat items independently. Mult-VAE uses multinomial likelihood — a user's interaction distribution is inherently multinomial with finite total mass distributed across items.

### Architecture

```
Input: sparse interaction vector x
  ↓ Encoder: FC layers → μ, log σ²
  ↓ Sampling: z = μ + σ⊙ε
  ↓ Decoder: FC layers → logits h ∈ R^{|I|}
  ↓ Output: softmax(h) = exp(hᵢ) / Σⱼ exp(hⱼ)
```

**Multinomial log-likelihood**: `L = Σᵢ xᵢ log p(xᵢ|z) = Σᵢ xᵢ log (exp(hᵢ) / Σⱼ exp(hⱼ))`

Key advantages: normalized outputs create competition between items, better calibrated probabilities, naturally handles implicit feedback counts.

### Dropout as Approximate MAP

Input dropout during training is equivalent to approximate MAP estimation in VAEs (Liang et al., 2018) — provides additional regularization and faster convergence on sparse data.

---

## VAE vs Standard Autoencoders

| Aspect | Standard AE | VAE |
|--------|------------|-----|
| Latent space | Deterministic point | Probabilistic distribution |
| Structure | Irregular, may have holes | Smooth, continuous |
| Generation | Cannot generate new samples | Can sample and decode |
| Interpolation | Unreliable between points | Meaningful interpolation |
| Cold-start | Poor generalization | Better via prior |
| Regularization | None (or manual) | KL divergence (automatic) |

---

## Conditional VAE for Context-Aware Recommendations

CVAE augments the VAE with conditioning variables `c`: `q_φ(z|x,c)`, `p_θ(x|z,c)`.

| Context Type | Examples | Benefit |
|-------------|----------|---------|
| Temporal | Time of day, season | Time-aware preferences |
| Demographic | Age, location | Segment preferences |
| Device | Mobile, desktop | Platform-specific behavior |
| Session | Previous items in session | Short-term intent |

Condition concatenated with input at encoder and with latent vector at decoder. At inference, set `c` to target context for context-specific recommendations.

---

## β-VAE for Disentangled Representations

β-VAE uses `β > 1` to encourage disentangled latent dimensions where each captures an independent factor:

| Dimension | Captured Factor |
|-----------|-----------------|
| z₁ | Genre preference |
| z₂ | Price sensitivity |
| z₃ | Recency preference |
| z₄ | Content length preference |

Benefits: interpretability, controllable generation, transfer learning, fairness auditing. Trade-off: higher β hurts reconstruction quality.

---

## VAE Training Challenges

### Posterior Collapse

**Problem**: Decoder ignores latent variable `z`; KL drops to zero; recommendations become non-personalized.

**Diagnosis**: KL near zero, latent codes cluster at origin, reconstruction high but generic.

**Mitigations:**

| Strategy | Mechanism | Effectiveness |
|----------|-----------|---------------|
| KL annealing | Gradually increase β from 0 to 1 over 50–200 epochs | High |
| Free bits | Set minimum KL per dimension (e.g., 0.5 nats) | High |
| Cyclical annealing | Reset β periodically (Fu et al., 2019) | High |
| Warm-up epochs | Train only on reconstruction first | Moderate |

### Training Instability

- **Gradient variance**: Multiple samples or control variates
- **Mode collapse**: Popularity-weighted sampling
- **KL vanishing in high dimensions**: Free bits or per-dimension KL monitoring

### Hyperparameter Sensitivity

| Hyperparameter | Range | Impact |
|---------------|-------|--------|
| Latent dimension | 50–200 | Higher = more capacity, more KL |
| β | 0.5–2.0 | Higher = smoother latent space |
| Learning rate | 1e-4–5e-4 | VAEs sensitive to high LR |
| Annealing epochs | 50–200 | Longer = more stable |
| Input dropout | 0.3–0.5 | Critical for MAP approximation |

---

## Production Deployment Considerations

### Embedding Pre-computation

After training, item embeddings are pre-computed from decoder weights. Serving: encode user → latent vector → dot product with item embeddings → ANN search. Avoids running full decoder per candidate.

### Latent Space Indexing

Build ANN index (FAISS, ScaNN, HNSW) over decoder output embeddings. User encoding latency O(log N) instead of O(N). Memory: store item embeddings separately from model parameters.

### Cold-Start Handling

- **New user (few interactions)**: KL pulls latent toward prior → smoother recommendations
- **New item**: Initialize near prior mean → gravitates toward popular until interactions accumulate
- **Zero interactions**: Sample from N(0,I) → globally popular as safe default

### Model Size and Latency

| Component | Parameters (10K items, 200 latent) |
|-----------|-------------------------------------|
| Encoder | `|I| × h + h × 2d` ≈ 2M |
| Decoder | `d × h + h × |I|` ≈ 2M |
| Total | ~4M (lightweight) |
| Inference latency | 1–5 ms per user on CPU |

### Monitoring

- Track KL divergence over time (drift = distribution shift)
- Monitor reconstruction quality on held-out interactions
- Measure latent space utilization (dimension collapse)
- A/B test against non-probabilistic baselines
- Track recommendation diversity as latent space coverage proxy

---

## Summary

VAEs provide a probabilistic framework with smooth latent spaces, meaningful interpolation, uncertainty quantification, and better cold-start handling than deterministic alternatives. Mult-VAE addresses the multinomial nature of implicit feedback. Key challenges — posterior collapse and training instability — are addressable through KL annealing and free bits. Production benefits from pre-computing item embeddings and indexing the latent space for fast retrieval.
