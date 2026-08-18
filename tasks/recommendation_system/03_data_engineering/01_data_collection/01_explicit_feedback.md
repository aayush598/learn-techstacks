# Explicit Feedback Collection for Recommendation Systems

## 1. Types of Explicit Feedback

### 1.1 Ratings
- **Numeric Ratings**: 1-5 stars, 1-10 scale
- **Binary Ratings**: Like/Dislike, Thumbs up/down
- **Ordinal Ratings**: Poor/Fair/Good/Excellent
- **Pros**: Direct user preference signal; high quality labels
- **Cons**: Sparse (only 1-5% of users provide ratings); biased toward extremes

### 1.2 Reviews and Text Feedback
- **Free-form Text Reviews**: Detailed user opinions
- **Structured Reviews**: Rating + pros/cons + text
- **Pros**: Rich sentiment and preference signals
- **Cons**: Requires NLP processing; subjective; noisy

### 1.3 Preference Indicators
- **Favorite/Bookmark**: User saves item for later
- **Not Interested**: User explicitly rejects recommendation
- **Report**: User reports inappropriate content
- **Pros**: Binary signals are easy to collect; low user effort
- **Cons**: Less informative than ratings; ambiguous meaning

### 1.4 Explicit Preference Selections
- **Onboarding Preferences**: User selects preferred categories during signup
- **Interest Surveys**: Periodic preference surveys
- **Topic Following**: User follows specific topics/categories
- **Pros**: Rich preference data; no historical interaction needed
- **Cons**: User effort; preferences may change; cold-start for new preferences

---

## 2. Feedback Collection Design

### 2.1 UI/UX Patterns for Feedback Collection
- **Rating Prompts**: Ask for rating after sufficient interaction
- **Inline Feedback**: Like/dislike buttons on recommendation cards
- **Swipe UI**: Tinder-style swipe left/right for recommendations
- **Post-Experience Surveys**: Survey after consuming recommended content
- **Progressive Profiling**: Collect preferences gradually over time

### 2.2 When to Prompt for Feedback
- After user has spent sufficient time with item (threshold varies by domain)
- After purchase or completion (highest intent signal)
- Not too frequently (avoid survey fatigue)
- When user is in engaged state (not browsing casually)
- After positive interaction (user more likely to provide feedback)

### 2.3 Feedback Quality Control
- **Min/Max Validation**: Ensure ratings within valid range
- **Duplicate Prevention**: One rating per user per item
- **Spam Detection**: Detect and filter bot/fake ratings
- **Outlier Detection**: Identify and handle extreme ratings
- **Consistency Checks**: Compare explicit feedback with implicit signals

---

## 3. Feedback Storage Schema

### 3.1 Rating Storage
```sql
CREATE TABLE ratings (
    rating_id UUID PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    item_id VARCHAR NOT NULL,
    rating_value DECIMAL(3,2),  -- 0.00 to 5.00
    rating_type VARCHAR(20),    -- 'star', 'thumbs', 'binary'
    review_text TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    is_verified BOOLEAN,
    source VARCHAR(20),         -- 'web', 'mobile', 'email'
    UNIQUE(user_id, item_id)
);
```

### 3.2 Preference Storage
```sql
CREATE TABLE user_preferences (
    user_id VARCHAR NOT NULL,
    preference_type VARCHAR(50),  -- 'category', 'brand', 'topic'
    preference_value VARCHAR(100),
    strength DECIMAL(3,2),       -- 0.0 to 1.0 (confidence in preference)
    source VARCHAR(20),          -- 'explicit', 'inferred', 'survey'
    created_at TIMESTAMP,
    expires_at TIMESTAMP,
    PRIMARY KEY(user_id, preference_type, preference_value)
);
```

---

## 4. Explicit Feedback in ML Models

### 4.1 Direct Rating Prediction
- Train model to predict explicit rating value
- Loss function: MSE or MAE for numeric ratings
- Cross-entropy for ordinal ratings
- Output: Predicted rating for user-item pair

### 4.2 Classification from Explicit Feedback
- Convert ratings to binary labels (e.g., rating >= 4 → positive)
- Train classification model for relevance prediction
- Handle class imbalance (more positive than negative ratings)
- Output: Relevance probability for user-item pair

### 4.3 Label Generation from Explicit Feedback
- High rating (4-5 stars) → Positive label
- Low rating (1-2 stars) → Negative label
- Medium rating (3 stars) → Uncertain label (exclude or use as weak positive)
- Missing rating → Use implicit signals for label inference

---

## 5. Challenges with Explicit Feedback

### 5.1 Sparsity Problem
- Only 1-5% of users provide explicit feedback
- Most user-item pairs have no explicit feedback
- Solution: Combine with implicit feedback; use semi-supervised learning

### 5.2 Selection Bias
- Users who rate are not representative of all users
- Extreme opinions more likely to be expressed
- Solution: Propensity weighting; inverse propensity scoring

### 5.3 Temporal Dynamics
- User preferences change over time
- Old ratings may not reflect current preferences
- Solution: Time-decay weighting; sliding window of recent ratings

### 5.4 Rating Scale Interpretation
- Different users interpret rating scales differently
- Some users only give 4-5 stars; others use full range
- Solution: User-specific normalization; z-score normalization
