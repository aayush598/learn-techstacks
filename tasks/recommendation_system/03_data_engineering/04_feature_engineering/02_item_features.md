# Item Features for Recommendation Systems

## 1. Metadata Features

### 1.1 Structural Metadata
- **Category Hierarchy**: Multi-level taxonomy (e.g., Electronics > Computers > Laptops)
  - Level 1: Broad category (fewer categories, higher abstraction)
  - Level 2: Sub-category (moderate specificity)
  - Level 3: Fine-grained category (most specific, sparse)
  - Encoding: Target encoding per level, or hierarchical embeddings
  - Cold-start: Fall back to parent category when leaf is sparse
- **Brand**: Brand name or normalized brand ID
  - High-cardinality categorical — use embeddings or frequency-based encoding
  - Brand affinity correlates strongly with user loyalty patterns
  - Handle brand aliases (e.g., "Samsung Electronics" → "Samsung")
- **Tags**: User-assigned or system-assigned descriptive labels
  - Multi-label feature — each item can have 0–N tags
  - Compute tag frequency and inverse frequency for weighted representation
  - Filter spam/low-quality tags using minimum co-occurrence thresholds
- **SKU Attributes**: Color, size, weight, material, dimensions
  - Size/material preferences are strong user signals
  - Normalize numeric attributes (z-score within category)

### 1.2 Pricing Features
- **Raw Price**: Original listed price in native currency
- **Normalized Price**: Converted to single currency for global systems
- **Price Bucket**: Discretized price ranges (e.g., $0–10, $10–50, $50–200, $200+)
  - Use logarithmic bucketing for heavy-tailed price distributions
- **Price Relative to Category**: `item_price / median_category_price`
  - Captures whether an item is cheap or expensive *within its category*
- **Discount Features**: Original price, sale price, discount percentage, is_on_sale
- **Price Percentile**: Rank of item price within its category (0.0–1.0)
- **Price History**: Min/max/avg price over last 30/90/365 days

### 1.3 Temporal Metadata
- **Creation Date**: When the item was added to the catalog
- **Item Age**: Days since creation — new items need exploration boosts
- **Last Updated**: Recency of last metadata or content change
- **Availability Window**: Start/end dates for seasonal or limited items
- **Listing Duration**: How long the item has been live — proxy for quality

### 1.4 Catalog Features
- **Description Length**: Number of words/tokens in description
- **Title Length**: Shorter titles often correlate with higher conversion
- **Has Image / Image Count**: Binary or count of available images
- **Has Video**: Presence of video content
- **Completeness Score**: Percentage of optional metadata fields populated
- **Seller/Retailer Quality**: Seller rating, return rate, response time

---

## 2. Content-Based Features

### 2.1 Text Embeddings
- **Sentence-BERT (SBERT)**: Encoding item titles and descriptions
  - Model: `all-mpnet-base-v2` (768-dim) or `all-MiniLM-L6-v2` (384-dim)
  - Input: Concatenation of title + description + tags
  - Output: Dense vector capturing semantic meaning
  - Truncation: Limit to 512 tokens; prioritize title over description
- **TF-IDF Features**: Sparse bag-of-words representation
  - Useful as baseline; dense embeddings generally outperform
  - Apply SVD to reduce dimensionality (e.g., 100–300 components)
- **Keyword Extraction**: Top-K keywords from title/description
  - Use RAKE, YAKE, or KeyBERT for extraction
  - Encode as multi-hot or weighted by relevance score
- **Named Entity Recognition**: Extract brand, product names, locations
  - Entities provide structured signals from unstructured text
- **Language Detection**: Primary language of item content
  - Critical for multilingual recommendation systems

### 2.2 Image Embeddings
- **CLIP (Contrastive Language-Image Pre-training)**: Joint image-text embeddings
  - Model: `ViT-B/32` or `ViT-L/14` from OpenAI
  - Advantages: Semantically aligned with text — enables cross-modal search
  - Output: 512-dim or 768-dim vector per image
  - Use primary image + up to 5 additional images (average or concatenate)
- **ResNet / EfficientNet**: Pure visual feature extraction
  - ResNet-50: 2048-dim features from penultimate layer
  - Better for visual similarity than semantic understanding
- **Color Features**: Dominant color palette, color histogram
  - 8–16 bin color histogram in HSV space
  - Important for fashion, home decor, visual content
- **Quality Features**: Blur detection, resolution, aesthetic score
  - Low-quality images correlate with lower engagement
  - Use NIMA (Neural Image Assessment) for aesthetic scoring
- **Object Detection**: Count and types of objects in image
  - Faster R-CNN or YOLO-based object labels
  - Useful for category validation and enrichment

### 2.3 Audio Embeddings
- **VGGish / YAMNet**: Audio feature extraction for music, podcasts, videos
  - 128-dim embeddings capturing timbre, rhythm, pitch
  - Use for music recommendation, podcast recommendation
- **Tempo / Energy / Valence**: Audio attribute features
  - Extracted via librosa or Essentia
  - Mood-based features for entertainment recommendations
- **Speech vs Music**: Content type classification
  - Affects downstream recommendation strategy

### 2.4 Multimodal Embeddings
- **CLIP Joint Space**: Align text and image in shared embedding space
- **Late Fusion**: Concatenate text embedding + image embedding + audio embedding
- **Attention-Based Fusion**: Learn weighted combination of modalities
  - Weight modality by availability (some items have no audio)
  - Missing modality: zero-vector with binary indicator flag
- **Multimodal Transformers**: ViLBERT, LXMERT for deeper fusion
  - Computationally expensive; reserved for high-value ranking stages

---

## 3. Statistical Features

### 3.1 Popularity Features
- **Total Views**: All-time view count (log-transformed to handle skew)
- **View Count by Window**: Views in last 1h, 24h, 7d, 30d, 90d
- **Click Count by Window**: Same windows for clicks
- **Purchase Count by Window**: Same windows for purchases
- **Unique User Count**: Distinct users who interacted (diversity of audience)
- **Impression Count**: How often the item was shown in recommendations

### 3.2 Engagement Rate Features
- **Click-Through Rate (CTR)**: `clicks / impressions`
  - Compute per time window (24h, 7d, 30d)
  - Apply Bayesian smoothing: `(clicks + α) / (impressions + α + β)` to handle low-impression items
  - Confidence interval matters more than point estimate for sparse items
- **Conversion Rate (CVR)**: `purchases / clicks`
  - Same smoothing applied
  - CVR is typically 10–100x lower than CTR
- **Add-to-Cart Rate**: `add_to_cart / views`
- **Save/Bookmark Rate**: `saves / views`
- **Completion Rate**: For videos/content — `completed / started`

### 3.3 Rating Features
- **Average Rating**: Mean of all user ratings (1–5 scale)
- **Rating Count**: Number of ratings — proxy for reliability
- **Rating Variance**: Standard deviation — high variance indicates polarizing item
- **Rating Trend**: Slope of rating over time (improving or declining quality)
- **Bayesian Average Rating**: `weighted_avg = (C × m + Σratings) / (C + n)` where C is confidence parameter, m is global mean
- **Rating Distribution**: Histogram of 1-star through 5-star counts

### 3.4 Composite Quality Features
- **Popularity Score**: Weighted combination of views, clicks, purchases
- **Quality Score**: Composite of rating, review length, return rate
- **Trending Score**: `current_rate / baseline_rate` — items gaining traction
- **Decay-Weighted Popularity**: Exponential decay weighting favoring recent activity

---

## 4. Cross-Item Features

### 4.1 Similarity Features
- **Embedding Cosine Similarity**: Pairwise similarity between item embeddings
  - Pre-compute top-K similar items for each item (K=50–200)
  - Store as sparse feature vectors
- **Category Co-occurrence**: Items frequently viewed/purchased together in same session
- **Content Overlap Score**: Jaccard similarity of tags/keywords between items
- **Visual Similarity**: CLIP-based image similarity for visual recommendations

### 4.2 Co-Purchase / Co-View Features
- **Frequently Bought Together**: Items purchased in same transaction
- **Also Viewed**: Items viewed in same session
- **Affinity Matrix**: `support(A,B) = P(A and B) / P(A) × P(B)` — lift metric
- **Association Rules**: Confidence and lift for item pairs
  - Pre-compute top association rules with minimum support threshold

### 4.3 Item Graph Features
- **PageRank Score**: Importance of item in item-item interaction graph
- **Node Degree**: Number of connections in co-occurrence graph
- **Community Detection**: Which cluster/item-group the item belongs to
- **Centrality Measures**: Betweenness, closeness centrality in item graph

---

## 5. Temporal Features

### 5.1 Recency Features
- **Time Since Last Interaction**: Hours since last click/view/purchase
- **Recency Bucket**: Very recent (<1h), recent (<24h), old (<7d), stale (>7d)
- **Freshness Score**: Exponential decay from last interaction timestamp

### 5.2 Seasonality Features
- **Day-of-Week Pattern**: Is this item more popular on weekends?
- **Hour-of-Day Pattern**: Does the item peak at specific hours?
- **Monthly Seasonality**: Seasonal demand patterns (e.g., winter coats in fall)
- **Holiday Affinity**: Items popular during specific holidays
  - Pre-compute holiday association scores from historical data
- **Seasonal Index**: `item_popularity_during_season / item_popularity_overall`

### 5.3 Trending Features
- **Trending Score**: `(views_last_1h / views_last_24h_avg_hourly)` — velocity
- **Momentum**: Rate of change of popularity (first derivative)
- **Acceleration**: Second derivative of popularity (accelerating trends)
- **Viral Score**: Anomaly detection on interaction rate vs historical baseline

---

## 6. Item Embedding Techniques

### 6.1 Collaborative Filtering Embeddings
- **Matrix Factorization**: SVD/ALS on user-item interaction matrix
  - Latent factors capture collaborative signals (128–256 dims)
  - Good for capturing user preferences without content understanding
- **Item2Vec**: Skip-gram model on item interaction sequences
  - Treats purchase sequences like word sentences
  - Captures sequential and co-occurrence patterns
- **Graph Embeddings**: Node2Vec / GraphSAGE on item interaction graph
  - Captures structural relationships beyond pairwise similarity

### 6.2 Content-Based Embeddings
- **Text**: Sentence-BERT for titles/descriptions (768 dims)
- **Image**: CLIP ViT for product images (512–768 dims)
- **Hybrid**: Concatenate collaborative + content embeddings
  - Weight modality by availability and information density

### 6.3 Learned Embedding Best Practices
- **Dimensionality**: 64–256 dims for most use cases
- **Training Data**: Minimum 10–50 interactions per item for stable embeddings
- **Cold Start**: Initialize new items with content-based embeddings
- **Periodic Retraining**: Refresh embeddings weekly or on significant catalog changes
- **Normalization**: L2-normalize embeddings before use in similarity computations
- **Dimensionality Reduction**: Apply PCA/UMAP for visualization and debugging

### 6.4 Embedding Evaluation
- **Intrinsic Evaluation**: Semantic similarity, clustering quality
- **Extrinsic Evaluation**: Impact on downstream recommendation metrics (NDCG, Recall)
- **A/B Testing**: Online metrics with embedding variants
- **Nearest Neighbor Quality**: Manual inspection of top-K similar items

---

## 7. Feature Engineering Best Practices

### 7.1 Handling Cold Start
- New items: Rely on content-based features (text, image, metadata)
- Bootstrap with category-level statistics when item-level data is sparse
- Use metadata completeness as a quality signal for new item onboarding

### 7.2 Feature Normalization
- Numeric features: Min-max scaling or z-score normalization
- Categorical features: Target encoding with smoothing to prevent overfitting
- Embedding features: L2 normalization for cosine similarity computations
- Log-transform skewed features (view counts, price)

### 7.3 Feature Validation
- Automated range checks for all features
- Monitor feature distribution drift daily
- Alert on sudden null rate increases (pipeline failures)
- Validate embedding quality via nearest neighbor inspection quarterly
