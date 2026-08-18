# Deep Learning for Recommendation Systems

## 1. Autoencoders for Recommendations

### 1.1 Collaborative Filtering Autoencoder (Autorec)
- **Architecture**: Input (user-item vector) → Encoder → Bottleneck → Decoder → Reconstructed vector
- **Training**: Minimize reconstruction error on observed entries
- **Inference**: Use reconstructed vector to predict missing ratings
- **Advantage**: Non-linear collaborative filtering; captures complex patterns

### 1.2 Denoising Autoencoders
- **Architecture**: Add noise to input; train to reconstruct clean input
- **Benefit**: More robust representations; handles missing data better
- **Variants**: Masking noise (zero out random entries), Gaussian noise

### 1.3 Variational Autoencoders (VAE)
- **Architecture**: Encoder → mean and variance → sampling → decoder
- **Training**: ELBO loss (reconstruction + KL divergence)
- **Benefit**: Probabilistic model; can generate diverse recommendations
- **Use Case**: Multi-modal recommendations; uncertainty estimation

---

## 2. Neural Collaborative Filtering

### 2.1 Architecture
- **Generalized Matrix Factorization (GMF)**: Element-wise product of user and item embeddings
- **Multi-Layer Perceptron (MLP)**: Concatenate embeddings; feed through deep network
- **Neural MF**: Combine GMF and MLP outputs for final prediction
- **Training**: Binary cross-entropy for implicit feedback; MSE for explicit ratings

### 2.2 DeepFM
- **Factorization Machine Component**: Captures feature interactions (like FM)
- **Deep Component**: Captures high-order feature interactions
- **Benefit**: No manual feature engineering for feature crosses
- **Architecture**: Embedding layer → FM component + Deep component → Combination layer → Output

### 2.3 Wide & Deep Learning
- **Wide Component**: Linear model for memorization (direct feature crosses)
- **Deep Component**: DNN for generalization (learned feature interactions)
- **Joint Training**: Both components trained together
- **Benefit**: Balances memorization and generalization
- **Used By**: Google Play Store recommendations

---

## 3. Sequence-Aware Deep Learning

### 3.1 Recurrent Neural Networks (RNN)
- **GRU4Rec**: GRU-based model for session-based recommendations
- **Architecture**: Embedding → GRU layers → Output layer
- **Loss**: BPR loss or TOP1 loss for ranking
- **Benefit**: Captures sequential patterns in user behavior

### 3.2 Long Short-Term Memory (LSTM)
- **Architecture**: LSTM cells for long-term dependency modeling
- **Attention-Enhanced**: Add attention mechanism for important historical items
- **Bidirectional**: Process sequence forward and backward for richer representations

### 3.3 Transformer-Based Models

**SASRec (Self-Attentive Sequential Recommendation)**:
- Self-attention mechanism over user interaction history
- Position encoding for sequence order
- Point-wise feed-forward network
- Multiple attention heads for different patterns

**BERT4Rec**:
- Bidirectional attention (like BERT) for recommendations
- Cloze-style training: mask random item; predict masked item
- Benefits from bidirectional context
- Better than SASRec on some benchmarks

**Transformers4Rec (NVIDIA)**:
- Multi-head self-attention with causal masking
- Supports multiple input features (categorical, numerical, text)
- Session-based and long-term sequence modeling
- Integration with NVTabular for feature engineering

---

## 4. Attention Mechanisms

### 4.1 Self-Attention for Recommendations
- Compute attention weights between all items in user history
- Weighted sum of item embeddings based on relevance to target item
- Captures which historical items are most relevant for each prediction

### 4.2 DIN (Deep Interest Network)
- **Architecture**: User profile embedding + Target item embedding + Attention over history
- **Key Idea**: User interest is diverse; different items activate different interests
- **Attention**: Compute relevance between target item and each historical item
- **Benefit**: Personalized attention; captures multi-faceted user interests

### 4.3 DIEN (Deep Interest Evolution Network)
- **Architecture**: GRU + Attention + AUGRU (Attention-based GRU)
- **Key Idea**: User interest evolves over time; capture interest evolution
- **AUGRU**: Gate mechanism influenced by attention (relevant history gets higher gates)
- **Benefit**: Models how user preferences change over time

### 4.4 Multi-Head Attention
- Multiple attention heads capture different types of relationships
- Head 1: Category-based attention
- Head 2: Price-based attention
- Head 3: Temporal attention
- Concatenate or average head outputs

---

## 5. Graph Neural Networks for Recommendations

### 5.1 PinSage (Pinterest)
- Graph convolutional network on user-pin-board graph
- Produces pin embeddings from graph structure
- Handles billion-scale graphs through random walk sampling
- Combines graph features with content features

### 5.2 LightGCN
- Simplified GCN for collaborative filtering
- Only neighborhood aggregation (no feature transformation)
- learns embeddings from user-item bipartite interaction graph
- State-of-the-art on multiple benchmarks

### 5.3 NGCF (Neural Graph Collaborative Filtering)
- Embedding propagation on user-item bipartite graph
- Message passing between users and items
- Captures high-order connectivity (user → item → user → item patterns)

---

## 6. Multi-Task Learning

### 6.1 Shared-Bottom Architecture
- Shared bottom layers for feature extraction
- Task-specific tower for each prediction task
- Tasks: CTR, conversion, dwell time, rating

### 6.2 MMoE (Multi-gate Mixture-of-Experts)
- Multiple expert networks for different feature interactions
- Task-specific gating networks to weight expert outputs
- More flexible than shared-bottom; captures task-specific patterns
- Used by Google for YouTube recommendations

### 6.3 PLE (Progressive Layered Extraction)
- Explicitly separates shared and task-specific experts
- Progressive extraction of features for each task
- Reduces negative transfer between unrelated tasks

---

## 7. Model Serving Optimization

### 7.1 ONNX Conversion
- Convert PyTorch/TensorFlow models to ONNX format
- ONNX Runtime for optimized inference
- Quantization support (FP32 → FP16 → INT8)
- Cross-platform deployment

### 7.2 TensorRT Optimization
- NVIDIA TensorRT for GPU-optimized inference
- Layer fusion, kernel auto-tuning
- FP16 and INT8 quantization
- 2-5x speedup over standard PyTorch inference

### 7.3 Model Distillation
- Train large teacher model
- Distill knowledge into smaller student model
- Student model has 2-10x fewer parameters
- Maintains 95-99% of teacher accuracy
- Faster inference with smaller memory footprint
