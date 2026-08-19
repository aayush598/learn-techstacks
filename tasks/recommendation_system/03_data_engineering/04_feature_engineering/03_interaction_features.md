# Interaction Features for Recommendation Systems

## 1. Explicit Interaction Features

### 1.1 Rating Features
- **Raw Rating Value**: User's explicit rating (1–5, 1–10, thumbs up/down)
- **Rating Deviation**: `user_rating - item_average_rating`
  - Captures whether user rates this item above or below average
  - Useful for personalized quality adjustment
- **Rating Normalization**: User-mean-centered ratings
  - `z_rating = (rating - user_mean) / user_std`
  - Eliminates systematic bias from lenient/harsh raters
- **Rating Count**: Total ratings by user (high-count users are more reliable)
- **Rating Variance**: How much a user's ratings spread — high variance = discriminative rater
- **Rating History Trend**: Slope of user's ratings over time (getting stricter or lenient)

### 1.2 Like/Dislike Features
- **Binary Preference**: 1 for like, -1 for dislike, 0 for no signal
- **Like Ratio**: `likes / (likes + dislikes)` for items with both signals
- **Like Count by Window**: Likes in last 24h, 7d, 30d
- **Dislike-to-Like Ratio**: High ratio signals controversial content
- **Implicit Negation**: Items explicitly dismissed or marked "not interested"

### 1.3 Save and Bookmark Features
- **Save Count**: Number of users who saved/bookmarked this item
- **Save Rate**: `saves / impressions` — high save rate indicates high intent
- **Save-to-Purchase Conversion**: `purchases / saves` — measures follow-through
- **User Save Velocity**: Rate of new saves — trending signal
- **Save Duration**: How long item stays in saved list before action

---

## 2. Implicit Interaction Features

### 2.1 Click and View Features
- **Click Binary**: Whether user clicked on the item (1/0)
- **Click Count**: Total clicks by user on this item (multiple clicks = strong interest)
- **Click-Through Rate**: `clicks / impressions` for this user-item pair
- **Click Position Bias**: Click probability decreases with rank position
  - Corrected CTR: `click / propensity(position)` using position bias model
- **View Count**: Total views/impressions
- **View-through Rate**: Whether user viewed item detail page after click

### 2.2 Dwell Time Features
- **Raw Dwell Time**: Seconds spent viewing item detail page
- **Log Dwell Time**: `log(1 + dwell_seconds)` — handles heavy-tailed distribution
- **Dwell Time Bucket**: Skim (<5s), Normal (5–30s), Deep (30–120s), Very Deep (>120s)
- **Dwell Time Relative to Category**: `dwell / median_dwell_for_category`
  - Some categories naturally have longer dwell (furniture vs. snacks)
- **Reading Speed Normalized Dwell**: Adjust for content length
- **Bounce Detection**: Single-page view with <2s dwell — likely accidental click
- **Completion Dwell**: For articles/videos — percentage of content consumed

### 2.3 Scroll and Engagement Features
- **Scroll Depth**: Percentage of page scrolled (0–100%)
- **Scroll Speed**: Pixels per second — fast scroll = low interest
- **Image Interaction**: Number of product images viewed, zoom events
- **Video Watch Time**: Duration of video watched, completion percentage
- **Expand/Collapse**: Whether user expanded description, reviews, specifications
- **Share Events**: Share to social media, copy link, send to friend

### 2.4 Purchase and Transaction Features
- **Purchase Binary**: Whether user purchased the item
- **Purchase Count**: Repeat purchases of same item
- **Purchase Value**: Transaction amount (for items with variable pricing)
- **Cart Abandonment**: Added to cart but did not purchase
  - Strong negative signal for future recommendations
- **Return Rate**: Purchases followed by returns — negative quality signal
- **Purchase Channel**: In-app, web, in-store — context-dependent preferences
- **Time-to-Purchase**: Hours from first view to purchase (consideration length)

### 2.5 Search Interaction Features
- **Search-to-Click**: Item was clicked after search query
- **Search Query**: The query string used to find this item
- **Search Position**: Rank at which item appeared in search results
- **Filter Usage**: Which filters were applied before finding this item
- **Search Refinement Count**: How many searches before clicking — proxy for difficulty

---

## 3. Interaction History Encoding

### 3.1 Recency-Weighted Encoding
- **Exponential Decay Weighting**: `weight = e^(-λ × time_delta)`
  - λ controls decay rate: fast decay (λ=0.1) vs slow decay (λ=0.01)
  - Recent interactions dominate the signal
- **Time-Bucketed Aggregation**: Separate features for 1h, 24h, 7d, 30d, 90d windows
  - Multiple windows capture both short-term intent and long-term preference
- **Sliding Window Statistics**: Mean, count, variance within rolling windows
- **Recency Rank**: Rank of most recent interaction relative to history

### 3.2 Frequency-Weighted Encoding
- **Interaction Count by Type**: Separate counts for clicks, views, purchases, saves
- **TF-IDF Interaction Weighting**: `weight = count × log(N / item_frequency)`
  - Down-weights items everyone interacts with (popular items)
  - Up-weights niche items that indicate specific preference
- **Burst Detection**: Interaction frequency spike vs user's baseline
  - High burst = strong temporary interest (e.g., searching for a gift)
- **Category Interaction Frequency**: Aggregate interactions per category
- **Temporal Frequency Pattern**: Does user interact more on weekdays or weekends?

### 3.3 Sequence Encoding
- **RNN/LSTM Encoding**: Process interaction sequence through recurrent network
  - Captures order-dependent patterns (browse → compare → purchase)
- **Transformer Encoding**: Self-attention over interaction history
  - BERT4Rec style: masked item prediction in sequence
  - SASRec style: causal attention for next-item prediction
- **Sequence Window**: Last N interactions (N=50–200 typical)
- **Padding Strategy**: Zero-pad short sequences, truncate long ones
- **Positional Encoding**: Sinusoidal or learned position embeddings

### 3.4 Summary Statistics Encoding
- **Interaction Count Vector**: [clicks, views, purchases, saves] as feature vector
- **Time Span**: Duration from first to last interaction (engagement longevity)
- **Interaction Rate**: Interactions per session / per day
- **Unique Items Interacted**: Breadth of item exploration
- **Category Entropy**: `H = -Σ p(c) × log(p(c))` — high entropy = diverse interests
- **Session-Length Distribution**: Mean, median, std of items per session

---

## 4. Co-Occurrence Features

### 4.1 User-Level Co-Occurrence
- **Items Co-Interacted by User**: Items appearing in same user's history
  - Weight by interaction strength (purchase > save > click > view)
- **User Preference Overlap**: Jaccard similarity of two users' interaction sets
- **User Affinity to Item Cluster**: How many items from item's cluster did user interact with?

### 4.2 Item-Level Co-Occurrence
- **Co-View Count**: How often two items are viewed in same session
- **Co-Purchase Count**: How often two items are purchased together
- **Association Rules**: `confidence(A→B) = support(A,B) / support(A)`
  - Lift: `confidence(A→B) / support(B)` — above 1.0 means positive association
- **Jaccard Similarity**: `|users(A) ∩ users(B)| / |users(A) ∪ users(B)|`
- **Cosine Similarity**: On user-item interaction vectors

### 4.3 Session-Level Co-Occurrence
- **Same-Session Items**: Items appearing within a single session
- **Temporal Co-Occurrence**: Items interacted within T minutes of each other
- **Sequential Patterns**: Item A → Item B transition probability
  - Markov chain transition matrix for sequential recommendations
- **Session Similarity**: Cosine similarity between two sessions' item sets

---

## 5. Cross-Domain Interaction Features

### 5.1 Cross-Category Features
- **Category Transition Probability**: P(category_B | category_A) from user history
- **Cross-Category Affinity**: User's tendency to explore beyond primary category
- **Category Diversity**: Entropy of user's category interaction distribution
- **Exploration Score**: Ratio of novel categories to total categories in recent history

### 5.2 Cross-Platform Features
- **Platform-Specific Interactions**: Separate interaction counts per platform
- **Cross-Device Continuity**: Same user interacting across mobile and desktop
- **Platform Preference**: Which platform drives highest engagement
- **Cross-Platform Deduplication**: Unified interaction history across devices

### 5.3 Cross-User Features
- **Social Connections**: Interactions from followed/friended users
- **Collaborative Signal**: Similar users' interactions with candidate items
- **Social Proof Features**: "X friends liked this" — friend interaction counts
- **Influence Score**: How much this user's interactions predict others' behavior

---

## 6. Multi-Modal Interaction Features

### 6.1 Text + Behavior Fusion
- **Search Query Embedding + Click Pattern**: Combine what user searched with what they clicked
- **Review Text + Rating**: Sentiment from review text vs explicit rating alignment
- **Query Reformulation Pattern**: How search queries evolve across session

### 6.2 Image + Behavior Fusion
- **Visual Preference Embedding**: Average image embedding of items user interacts with
- **Style Consistency Score**: How visually similar are items in user's history
- **Visual vs Textual Click Pattern**: Do users click on visually similar or semantically similar items?

### 6.3 Multi-Modal Fusion Architecture
- **Early Fusion**: Concatenate all modality features before model input
- **Late Fusion**: Separate models per modality, combine predictions
- **Cross-Attention Fusion**: Let modalities attend to each other (most expressive)
- **Modality Dropout**: Randomly zero-out modalities during training for robustness

---

## 7. Interaction Feature Computation

### 7.1 Batch Computation
- **Daily Aggregates**: Recompute all interaction counts, rates, statistics nightly
- **Weekly Aggregates**: Longer-window statistics, trending scores
- **Monthly Aggregates**: User preference profiles, item quality scores
- **Backfill**: Recompute historical features when logic changes

### 7.2 Real-Time Computation
- **Streaming Aggregation**: Update counts and running statistics per event
  - Apache Flink / Kafka Streams for exactly-once aggregation
- **Sliding Window Counts**: Maintain counts over last 1h, 24h, 7d windows
- **Session State**: Track current session interactions for session-based features
- **Latency Requirement**: <100ms from event to feature availability

### 7.3 Near-Real-Time Computation
- **Micro-Batch**: Aggregate every 1–5 minutes
- **Feature Snapshot**: Periodic snapshots of interaction state
- **Change Data Capture**: Stream updates to feature store on interaction events
- **Trade-off**: Freshness vs computational cost

---

## 8. Sparse Interaction Handling

### 8.1 Cold-Start Interactions
- **Zero-Interaction Users**: Default to popularity-based recommendations
- **Few-Interaction Users** (<5): Increase exploration rate, rely on content features
- **Interaction Threshold**: Minimum interactions before switching to personalized model

### 8.2 Sparsity Mitigation
- **Implicit Feedback Matrix**: 99%+ sparse — use ALS or neural collaborative filtering
- **Negative Sampling**: Sample negative interactions (non-clicked items) for training
- **Data Augmentation**: Add session-based pseudo-interactions
- **Transfer Learning**: Use pre-trained embeddings from similar domains

### 8.3 Interaction Quality Filtering
- **Bot Detection**: Filter automated/bot interactions from feature computation
- **Accidental Click Filtering**: Remove clicks with <1s dwell time
- **Spam Filtering**: Detect and remove artificial interaction patterns
- **Duplicate Removal**: Deduplicate rapid repeated interactions from same session
