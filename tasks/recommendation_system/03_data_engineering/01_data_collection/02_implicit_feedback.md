# Implicit Feedback Collection for Recommendation Systems

## 1. Types of Implicit Feedback

### 1.1 Click/View Data
- **Impressions**: Item was shown to user (not interacted)
- **Clicks**: User clicked on item
- **Dwell Time**: Duration user spent on item page/content
- **Bounce**: User left immediately (short dwell time)
- **Pros**: Abundant (every user generates implicit signals); no user effort
- **Cons**: Noisy (clicks don't always mean preference); position bias

### 1.2 Purchase/Transaction Data
- **Purchases**: User bought item
- **Add to Cart**: User added item to shopping cart
- **Wishlist**: User added item to wishlist
- **Returns**: User returned purchased item
- **Pros**: Strong intent signal; directly tied to business value
- **Cons**: Sparse relative to views; delayed feedback

### 1.3 Engagement Data
- **Scroll Depth**: How far user scrolled through content
- **Video Completion**: Whether user watched full video
- **Audio Play Duration**: How long user listened to song
- **Content Sharing**: User shared item with others
- **Save/Bookmark**: User saved item for later
- **Pros**: Granular engagement signals; mid-funnel indicators
- **Cons**: Engagement ≠ satisfaction; completion doesn't guarantee preference

### 1.4 Search and Navigation Data
- **Search Queries**: What user searched for
- **Category Navigation**: Browsing paths through categories
- **Filter Usage**: What filters user applied
- **Sort Preferences**: How user sorted results
- **Pros**: Reveals user intent; informs recommendation context
- **Cons**: Noisy; may reflect exploration not preference

### 1.5 Social Signals
- **Follows**: User follows creator/brand
- **Likes on Social**: User liked shared content
- **Comments**: User commented on recommended content
- **Referrals**: User referred item to friends
- **Pros**: Strong social proof signal
- **Cons**: Privacy concerns; noisy; sparse

---

## 2. Implicit Feedback Processing

### 2.1 Confidence Score Computation
Not all implicit signals are equally strong:
```
confidence = f(action_type, dwell_time, position, context)

Example:
click_confidence = 1 + alpha * log(1 + dwell_time_seconds)
view_confidence = 0.1  # Low confidence for just viewing
purchase_confidence = 5.0  # High confidence for purchase
```

### 2.2 Negative Feedback Inference
- **Impression without click**: Weak negative (item shown but not clicked)
- **Skip/Swipe left**: Stronger negative (explicit rejection)
- **Item abandoned in cart**: Context-dependent (price issue vs preference)
- **Long time between category views**: Weak negative for category

### 2.3 Position Bias Correction
- Items at top of list get more clicks regardless of relevance
- Position bias correction: weight clicks by inverse position probability
- Randomized positions during training data collection
- Position-aware models that separate position effect from relevance

---

## 3. Implicit Feedback Data Pipeline

### 3.1 Event Collection
```
Client SDK → Event Collector → Kafka → Stream Processing
```
- Client SDK captures user events (clicks, views, scrolls)
- Events sent to collector endpoint
- Events published to Kafka topic
- Stream processor validates and enriches events

### 3.2 Event Schema
```json
{
  "event_id": "uuid",
  "user_id": "user_123",
  "item_id": "item_456",
  "event_type": "click",
  "timestamp": "2024-01-15T10:30:00Z",
  "context": {
    "session_id": "sess_789",
    "page": "home",
    "position": 3,
    "device": "mobile"
  },
  "metadata": {
    "dwell_time_ms": 45000,
    "scroll_depth": 0.8,
    "referrer": "search"
  }
}
```

### 3.3 Aggregation Pipelines
- **Real-time Aggregation**: Flink/Kafka Streams for live metrics
- **Micro-batch Aggregation**: 5-minute windows for near-real-time dashboards
- **Batch Aggregation**: Daily/hourly aggregation for model training data
- **Session Aggregation**: Group events into sessions for session-based features

---

## 4. Handling Implicit Feedback Challenges

### 4.1 Missing Not at Random (MNAR)
- Missing feedback is not random; users only interact with items they see
- Items not shown cannot have feedback (censoring)
- Solution: Propensity modeling, counterfactual learning, exploration

### 4.2 Exposure Bias
- Users can only click on items they're exposed to
- Items never shown to user have no feedback
- Solution: Exploration strategies, randomization in serving, unbiased learning

### 4.3 Dwell Time Interpretation
- Long dwell time could mean: engaged with content OR confused/lost
- Short dwell time could mean: quickly found what needed OR didn't like
- Solution: Combine with other signals; category-specific thresholds

### 4.4 Feedback Delay
- Some actions (purchase) happen long after recommendation
- Attribution window determines which recommendation gets credit
- Solution: Configurable attribution windows; delayed feedback models
