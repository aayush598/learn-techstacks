# Feature Engineering for Recommendation Systems

## 1. User Features

### 1.1 Demographic Features
- **Age Group**: Bucketed age (18-24, 25-34, 35-44, 45-54, 55+)
- **Gender**: Male, Female, Non-binary, Unknown
- **Location**: Country, region, city, urban/rural
- **Language**: Primary language preference
- **Account Age**: Days since registration

### 1.2 Behavioral Features
- **Interaction Counts**: Total clicks, views, purchases (last 1h, 24h, 7d, 30d)
- **Engagement Rate**: Clicks / impressions
- **Purchase Frequency**: Purchases per week/month
- **Average Order Value**: Mean purchase amount
- **Category Distribution**: Percentage of interactions per category
- **Session Statistics**: Sessions per day, avg session duration, items per session
- **Recency Features**: Time since last click, last purchase, last session

### 1.3 Preference Features
- **Category Preferences**: Weighted category distribution (TF-IDF-like)
- **Brand Preferences**: Brand affinity scores
- **Price Sensitivity**: Price range preference, discount responsiveness
- **Quality Preferences**: Average rating of items user interacts with
- **Freshness Preferences**: Tendency to interact with new vs old items
- **Diversity Score**: Entropy of user's interaction distribution

### 1.4 Embedding Features
- **User Embedding**: Learned dense vector from collaborative filtering
- **Sequence Embedding**: RNN/Transformer encoding of interaction history
- **Social Embedding**: Graph-based embedding from social connections

---

## 2. Item Features

### 2.1 Metadata Features
- **Category Hierarchy**: Category level 1, 2, 3
- **Brand**: Brand name or ID
- **Price**: Raw price, price bucket, price relative to category
- **Creation Date**: Item age in days
- **Text Features**: Title length, description length, keyword extraction
- **Image Features**: Color histogram, quality score, NSFW score

### 2.2 Content Embeddings
- **Text Embedding**: Sentence-BERT embedding of title + description
- **Image Embedding**: ResNet/EfficientNet embedding of item image
- **Audio Embedding**: Audio feature extraction for music/podcast
- **Multimodal Embedding**: Combined text + image embedding

### 2.3 Statistical Features
- **Popularity**: Total views, clicks, purchases (all time, last 24h, last 7d)
- **Trending Score**: Rate of change in popularity
- **CTR**: Click-through rate (clicks / impressions)
- **Conversion Rate**: Purchases / clicks
- **Average Rating**: Mean user rating
- **Rating Count**: Number of ratings
- **Quality Score**: Composite quality metric

### 2.4 Interaction-Based Features
- **Co-occurrence**: How often item appears with other items
- **User Overlap**: How many users interact with this item
- **Diversity Contribution**: How much this item adds to recommendation diversity

---

## 3. Interaction Features

### 3.1 User-Item Affinity Features
- **Historical Affinity**: Strength of past interactions between user and item/category
- **Interaction Count**: Number of past interactions with similar items
- **Recency Weighted Affinity**: More recent interactions weighted higher
- **Implicit Rating**: Derived rating from behavioral signals

### 3.2 Cross Features
- **User × Category**: User's preference for item's category
- **User × Brand**: User's preference for item's brand
- **User × Price Range**: User's preference for item's price range
- **User × Time**: User's activity patterns at current time
- **Category × Time**: Category popularity at current time

### 3.3 Sequential Features
- **Previous Item**: Last item user interacted with
- **Session Position**: Position of item in current session
- **Time Gap**: Time between current and previous interaction
- **Category Transition**: Previous category → current category
- **Session Progression**: How user's interests evolve within session

---

## 4. Contextual Features

### 4.1 Time Features
- **Hour of Day**: 0-23 (cyclical encoding: sin/cos)
- **Day of Week**: 0-6 (cyclical encoding)
- **Month**: 1-12 (cyclical encoding)
- **Is Weekend**: Boolean
- **Is Holiday**: Boolean (based on user's country)
- **Season**: Spring, summer, fall, winter

### 4.2 Device Features
- **Device Type**: Desktop, mobile, tablet, smart TV
- **Platform**: iOS, Android, Web
- **Screen Size Bucket**: Small, medium, large, extra-large
- **Is App**: Native app vs mobile web

### 4.3 Location Features
- **Country**: Country code
- **Region**: State/province
- **City**: City name or ID
- **Urban/Rural**: Classification
- **Distance to Store**: For location-based recommendations

---

## 5. Feature Selection

### 5.1 Filter Methods
- **Correlation Analysis**: Remove highly correlated features (>0.95)
- **Mutual Information**: Rank features by MI with target variable
- **Variance Threshold**: Remove low-variance features
- **Statistical Tests**: Chi-squared, ANOVA for feature-target relationship

### 5.2 Wrapper Methods
- **Forward Selection**: Add features one at a time
- **Backward Elimination**: Remove features one at a time
- **Recursive Feature Elimination**: Iteratively remove least important features

### 5.3 Embedded Methods
- **L1 Regularization**: Automatic feature selection via sparsity
- **Feature Importance from Trees**: Random Forest / XGBoost feature importance
- **Attention Weights**: Transformer attention as feature importance

---

## 6. Feature Store Management

### 6.1 Feature Naming Convention
```
{domain}_{entity}_{feature_group}_{feature_name}_{window}
Examples:
  user_behavior_click_count_24h
  user_preference_category_distribution
  item_metadata_price_bucket
  item_statistic_ctr_7d
  interaction_user_item_affinity_score
```

### 6.2 Feature Versioning
- Version features when computation logic changes
- Maintain backward compatibility during version transitions
- A/B test new feature versions before full rollout
- Track which model uses which feature version

### 6.3 Feature Documentation
- Feature name, description, owner
- Data type, range, default value
- Computation logic and freshness SLA
- Dependencies and lineage
- Usage examples and known issues
