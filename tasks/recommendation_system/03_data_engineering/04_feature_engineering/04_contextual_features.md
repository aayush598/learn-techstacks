# Contextual Features for Recommendation Systems

## 1. Temporal Context

### 1.1 Time of Day
- **Hour of Day**: 0–23, representing the hour of the request
  - Encoding: Cyclical via sin/cos transform
    - `sin_hour = sin(2π × hour / 24)`, `cos_hour = cos(2π × hour / 24)`
  - Why cyclical: Hour 23 and hour 0 are close in real time but far in linear encoding
- **Time Bucket**: Morning (6–12), Afternoon (12–17), Evening (17–22), Night (22–6)
  - Coarser but more interpretable than raw hour
  - Different user behaviors dominate at different buckets
- **Minutes Since Midnight**: Continuous value 0–1439 for finer granularity

### 1.2 Day of Week
- **Day Index**: 0 (Monday) through 6 (Sunday)
  - Encoding: Cyclical sin/cos or one-hot
- **Is Weekend**: Boolean — strong signal for entertainment vs productivity content
- **Day-Type**: Weekday, Saturday, Sunday, Holiday-eve
- **Payday Proximity**: Days until/after typical payday (1st and 15th of month)
  - Affects purchase intent and spending patterns

### 1.3 Seasonal and Calendar Features
- **Month**: 1–12 (cyclical encoding)
- **Season**: Spring, Summer, Fall, Winter (region-dependent date mapping)
- **Is Holiday**: Boolean — major holidays (varies by country/culture)
- **Holiday Name**: One-hot encoding of specific holidays
  - Christmas, Black Friday, Prime Day, Diwali, Singles Day
- **Days Until Holiday**: Continuous — captures pre-holiday shopping behavior
- **Post-Holiday Flag**: Returns, gift cards redemption patterns
- **Quarter**: Q1–Q4 — affects B2B recommendation patterns
- **School Calendar**: In-session vs vacation — affects content consumption

### 1.4 Event-Driven Temporal Features
- **Event Proximity**: Time relative to major events (sports, concerts, conferences)
- **New Release Window**: Days since item's release (for entertainment, news)
- **Trending Timeframe**: Is this a real-time trending topic?
- **Recency of Last User Activity**: Hours since user's last interaction
  - Longer gaps may indicate churn or changed context

---

## 2. Device Context

### 2.1 Device Type
- **Device Category**: Desktop, Mobile, Tablet, Smart TV, Wearable, Voice Assistant
  - Each device type has distinct interaction patterns and content preferences
  - Mobile: shorter sessions, more visual content, on-the-go consumption
  - Desktop: longer sessions, more complex content, work-related
  - Smart TV: lean-back viewing, video-heavy, family context
- **Screen Size Bucket**: Small (<5"), Medium (5–8"), Large (8–12"), XL (>12")
  - Affects how much information can be displayed
  - Influences whether to show image-heavy vs text-heavy recommendations
- **Screen Resolution**: Affects UI layout decisions in recommendation presentation
- **Has Touchscreen**: Boolean — affects interaction modality

### 2.2 Platform Features
- **Operating System**: iOS, Android, Windows, macOS, Linux, tvOS
- **Browser**: Chrome, Safari, Firefox, Edge (for web contexts)
- **App Version**: Native app version number — newer versions support richer features
- **Is Native App vs Mobile Web**: Native apps have richer feature set
- **SDK Version**: For mobile apps, affects available recommendation features

### 2.3 Device Capabilities
- **Camera Available**: Boolean — enables visual search recommendations
- **GPS Available**: Boolean — enables location-based recommendations
- **Push Notification Enabled**: Boolean — affects re-engagement strategy
- **Storage Available**: Low storage may limit offline recommendation caching
- **Battery Level**: Low battery may trigger shorter, more targeted recommendations

---

## 3. Location Context

### 3.1 Geographic Features
- **Country Code**: ISO 3166-1 alpha-2 (US, IN, JP, etc.)
  - Strongest location signal — affects content availability, language, pricing
- **Region/State**: Administrative region within country
- **City**: City name or city ID
  - Enables hyper-local recommendations (restaurants, events, stores)
- **Zip/Postal Code**: Granular location for delivery-based recommendations
- **GPS Coordinates**: Latitude/longitude for precise distance calculations
- **Geo-Hash**: Geohash string for spatial indexing and proximity queries

### 3.2 Location Classification
- **Urban/Rural**: Classification based on population density
  - Urban: More options, faster delivery, more diverse content
  - Rural: Fewer options, longer delivery, different content preferences
- **Population Density Tier**: Mega-city, large city, medium city, small city, rural
- **Timezone**: IANA timezone identifier or UTC offset
  - Critical for correct time-of-day feature computation
  - Ensures temporal features are in user's local time, not server time
- **Country Risk Level**: Fraud risk classification per region

### 3.3 Location-Based Derived Features
- **Distance to Nearest Store**: For hybrid (online + offline) recommendations
- **Delivery Zone**: Whether item is deliverable to user's location
- **Local Popularity**: Item popularity in user's geographic area
- **Regional Trends**: Trending items specific to user's region
- **Climate Zone**: Tropical, temperate, arid — affects product recommendations
- **Cost of Living Index**: Adjusts price sensitivity by location

---

## 4. Network Context

### 4.1 Connection Type
- **Network Type**: WiFi, 4G/LTE, 5G, 3G, Ethernet, Offline
  - WiFi/Ethernet: Can serve rich media (high-res images, video previews)
  - Cellular: Optimize for bandwidth — lower-res images, fewer pre-fetches
  - Offline: Serve only cached recommendations
- **Connection Speed Estimate**: Download bandwidth category (slow/medium/fast)
  - Determines whether to pre-fetch heavy content
  - Affects UI rendering strategy (progressive loading vs full render)
- **Data Saver Mode**: Boolean — user has enabled data-saving preferences

### 4.2 Bandwidth-Aware Recommendations
- **Media Quality Level**: Adapt image/video quality to connection
- **Pre-fetch Budget**: How much data to pre-cache for offline browsing
- **Content Format Preference**: Image-heavy vs text-heavy based on bandwidth
- **Lazy Loading Threshold**: When to defer loading below-fold recommendations

---

## 5. Session Context

### 5.1 Session-Level Features
- **Session Length**: Duration from first to last event in session
  - Short sessions (<2 min): Quick task — be precise
  - Long sessions (>10 min): Exploration mode — diversify
- **Session Position**: Current position within session (item #1, #2, ...)
  - Early: More exploratory; Late: More decisive
- **Pages Viewed**: Number of pages/screens viewed this session
- **Items Viewed**: Number of distinct items viewed
- **Time in Session**: Elapsed time since session start
- **Session Depth**: Number of interactions (clicks, views, additions to cart)

### 5.2 Referral and Entry Context
- **Referral Source**: Direct, search engine, social media, email, ad, push notification
  - Search referral: High intent — recommend closely matching items
  - Social referral: Discovery mode — recommend diverse content
  - Email referral: Often deal/promotion-driven — highlight deals
- **Landing Page**: Where the user entered the site/app
- **Campaign ID**: Which marketing campaign brought the user
- **UTM Parameters**: Source, medium, campaign, content, term
- **Entry Search Query**: What the user searched to arrive (if search-referred)

### 5.3 Session Behavior Patterns
- **Browsing vs Buying Mode**: Session-level purchase probability estimate
- **Category Focus**: Which categories is user exploring this session
- **Price Sensitivity This Session**: Average price of viewed items this session
- **Comparison Shopping Signal**: Viewing multiple similar items rapidly
- **Cart State**: Items currently in cart — complement or substitute recommendations
- **Session Intent Classification**: Browse, search, compare, purchase, return

---

## 6. Environmental Context

### 6.1 Weather Features
- **Weather Condition**: Clear, cloudy, rain, snow, extreme heat, extreme cold
  - Rain: Indoor activities, streaming, comfort food recommendations
  - Sunny: Outdoor activities, travel, summer products
  - Snow: Winter gear, indoor entertainment, warm food
- **Temperature**: Actual temperature in user's location (Celsius/Fahrenheit)
  - Bucketed: Freezing, Cold, Cool, Warm, Hot
- **Temperature Deviation**: How far from seasonal average
  - Unusual cold/heat triggers demand for unexpected products
- **Precipitation Probability**: Likelihood of rain/snow
- **Air Quality Index**: Affects outdoor activity recommendations
- **Seasonal Weather Pattern**: Monsoon, drought, heatwave flags

### 6.2 Weather-Product Affinity
- **Weather-Category Correlation**: Historical correlation between weather and category demand
- **Weather-Triggered Recommendations**: Pre-computed weather-to-category mapping
- **Temporal Lag**: Weather effects may have 1–3 day delay (e.g., order before cold front)

---

## 7. Social Context

### 7.1 Social Proof Features
- **Friend Activity**: Items liked/purchased by user's social connections
  - Strong social proof signal — "3 friends bought this"
  - Weight by social closeness (close friend > acquaintance)
- **Trending Among Peers**: Items trending within user's demographic/interest group
- **Social Influence Score**: Weight recommendations by social network centrality
- **Collaborative Trending**: Items popular among similar users (not necessarily connected)

### 7.2 Real-Time Social Signals
- **Current Event Relevance**: Items related to live events (sports, concerts, news)
- **Viral Content**: Items trending on social media platforms
- **Review Velocity**: Rate of new reviews for candidate items
- **Social Sharing Count**: How many times item was shared on social platforms
- **Hashtag Trending**: Items associated with trending hashtags

### 7.3 Community Context
- **Forum/Discussion Activity**: Items being discussed in relevant communities
- **Expert Endorsement**: Items recommended by domain experts/influencers
- **Community Rating**: Aggregated rating from specific community or group
- **User-Generated Content Volume**: Amount of UGC (reviews, photos, videos) for item

---

## 8. Context-Aware Recommendation Models

### 8.1 Contextual Bandits
- **LinUCB**: Linear model for context-dependent arm selection
  - Features: User features + context features as input
  - Reward: Click, purchase, or engagement metric
  - Exploration: Upper confidence bound for uncertainty
- **Neural Bandits**: Deep network for context-reward mapping
  - Better at capturing non-linear context interactions
- **Contextual Thompson Sampling**: Bayesian approach for context-dependent exploration

### 8.2 Factorization Machines
- **Feature Interactions**: Model pairwise interactions between all features
  - Context features interact with user and item features automatically
  - `ŷ = w₀ + Σwᵢxᵢ + ΣΣ⟨vᵢ, vⱼ⟩xᵢxⱼ`
- **Field-Aware FM (FFM)**: Different latent vectors per feature field
  - Better at distinguishing feature context (same feature means different things in different fields)

### 8.3 Attention-Based and Sequential Models
- **Self-Cross-Attention**: Model learns which context features matter per prediction
- **GRU4Rec / SASRec / BERT4Rec**: Sequential models with context injection
- **Contextual Position Encoding**: Inject time, device, location into position embeddings
- **MMoE / PLE**: Multi-task architectures with context-specific expert networks

---

## 9. Context Feature Best Practices

### 9.1 Feature Freshness
- **Real-time context**: Must be computed at request time (time, device, location)
- **Session context**: Updated per event within session
- **Environmental context**: Updated hourly (weather, trending topics)
- **Static context**: Updated daily (timezone rules, holiday calendar)

### 9.2 Missing Context Handling
- **Missing GPS**: Fall back to IP-based geolocation
- **Missing device info**: Use defaults or skip device-dependent features
- **Missing weather**: Use seasonal/climate defaults for location
- **Unknown referral**: Default to "direct" classification

### 9.3 Context Drift Monitoring
- Track distribution of context features over time
- Alert on sudden shifts (e.g., 50% increase in mobile users may indicate tracking issue)
- Validate temporal features against timezone rules during DST transitions
