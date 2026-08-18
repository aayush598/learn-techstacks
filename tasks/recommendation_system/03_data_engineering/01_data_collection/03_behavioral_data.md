# Behavioral Data Collection for Recommendation Systems

## 1. Behavioral Data Types

### 1.1 Browsing Behavior
- **Page Views**: Which pages/content user visited
- **Navigation Paths**: Sequence of pages visited
- **Time on Page**: Duration spent on each page
- **Scroll Behavior**: Scroll depth, scroll speed, scroll direction
- **Tab Switching**: How often user switches between tabs
- **Back Navigation**: When user goes back to previous page

### 1.2 Interaction Behavior
- **Click Patterns**: What user clicks on, click frequency, click timing
- **Hover Behavior**: What user hovers over (mouse/touch)
- **Form Interactions**: How user fills forms, field completion rates
- **Search Behavior**: Search queries, reformulation, result selection
- **Filter/Sort Usage**: How user filters and sorts results

### 1.3 Purchase Behavior
- **Purchase History**: What user bought, when, how much
- **Cart Behavior**: Add to cart, remove from cart, cart abandonment
- **Payment Preferences**: Payment method, installments usage
- **Return Behavior**: What user returned and reasons
- **Price Sensitivity**: Response to discounts, price comparison behavior

### 1.4 Content Consumption Behavior
- **Viewing Duration**: How long user consumed content
- **Completion Rate**: Percentage of content consumed
- **Re-engagement**: Whether user returns to same content
- **Sharing**: Content shared and to whom
- **Saving**: Content saved for later consumption

---

## 2. Session Analysis

### 2.1 Session Definition
- **Session Start**: First user activity in a time window
- **Session End**: No activity for timeout period (typically 30 minutes)
- **Cross-Device Sessions**: Linking sessions across devices for same user
- **Session Types**: Discovery, search, purchase, casual browsing

### 2.2 Session Features
- **Session Length**: Total duration of session
- **Session Depth**: Number of items/pages viewed
- **Session Diversity**: Category diversity of items viewed
- **Session Outcome**: Purchase, no action, add to cart, exit
- **Session Sequence**: Order of categories/items viewed
- **Session Frequency**: How often user has sessions

### 2.3 Session-Based Recommendations
- Use current session behavior for immediate recommendations
- Sequential pattern mining within sessions
- Session-based neural models (GRU4Rec, STAMP, NARM)
- Cross-session patterns for longer-term recommendations

---

## 3. Behavioral Data Processing

### 3.1 Event Deduplication
- Client SDK may send duplicate events (network retries)
- Deduplicate by event_id within time window
- Use Kafka consumer deduplication or stream processor deduplication

### 3.2 Event Enrichment
- Add server-side context (geolocation, device detection)
- Join with user profile data
- Join with item metadata
- Add computed fields (time since last interaction, session position)

### 3.3 Event Validation
- Schema validation against registered schema
- Required field checks
- Data type validation
- Range validation (e.g., dwell_time > 0)
- Referential integrity (valid user_id, item_id)

### 3.4 Event Aggregation
- **User-level aggregation**: Daily/hourly metrics per user
- **Item-level aggregation**: Daily/hourly metrics per item
- **Session-level aggregation**: Session summary features
- **Category-level aggregation**: Category-level trends and patterns

---

## 4. Behavioral Data Storage

### 4.1 Storage Requirements
- **Write Path**: High-throughput event ingestion (100K+ events/second)
- **Read Path**: Low-latency feature serving + analytical queries
- **Retention**: Raw events 30-90 days; aggregated data longer
- **Partitioning**: By date and entity type

### 4.2 Storage Architecture
- **Kafka**: Real-time event streaming (7-30 day retention)
- **Data Lake**: Long-term raw event storage (Parquet on MinIO)
- **ClickHouse**: Real-time analytical queries on aggregated data
- **Redis**: Hot aggregated features for serving

### 4.3 Data Volume Estimation
```
Events per user per day: 50-200 (active user)
Events per day for 1M users: 50M-200M events
Event size (JSON): ~1KB
Daily raw data: 50GB-200GB
With compression (10:1): 5GB-20GB
Monthly data: 150GB-600GB compressed
```

---

## 5. Behavioral Data for Model Training

### 5.1 Training Label Generation
- **Click as Positive Label**: User clicked → interested
- **Purchase as Strong Positive**: User purchased → very interested
- **Dwell Time as Soft Label**: Longer dwell → stronger interest
- **No Click as Weak Negative**: Shown but not clicked → likely not interested (with position bias correction)

### 5.2 Feature Engineering from Behavior
- **Frequency Features**: How often user interacts with category/brand
- **Recency Features**: Time since last interaction with category/item
- **Sequence Features**: Order of items interacted with
- **Session Features**: Current session behavior
- **Aggregated Features**: Statistical summaries of behavior

### 5.3 Behavioral Patterns for Recommendations
- **Sequential Patterns**: What items users typically view in sequence
- **Association Rules**: Items frequently co-purchased or co-viewed
- **Transition Patterns**: How users move between categories
- **Time-of-Day Patterns**: When users are interested in different categories
