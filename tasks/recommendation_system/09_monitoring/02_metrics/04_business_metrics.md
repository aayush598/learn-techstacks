# Business Metrics for Recommendation Systems

## 1. Core Business Metrics

### 1.1 Click-Through Rate (CTR)
- **Definition**: Clicks / Impressions
- **Target**: Varies by surface (2-10% for home page, 15-30% for "similar items")
- **Segmentation**: By user segment, device, surface, content type
- **Trend**: Track daily/weekly CTR trends

### 1.2 Conversion Rate
- **Definition**: Purchases / Clicks or Purchases / Impressions
- **Target**: 1-5% depending on domain
- **Attribution**: First-click, last-click, linear, time-decay
- **Attribution Window**: 7-30 days after recommendation

### 1.3 Revenue Per User
- **Definition**: Total revenue attributable to recommendations / Active users
- **Includes**: Direct purchases from recommendations, influenced purchases
- **Excludes**: Organic purchases not influenced by recommendations
- **Target**: Increasing trend over time

### 1.4 User Engagement
- **Session Duration**: Average time spent per session
- **Items Per Session**: Average items viewed per session
- **Return Rate**: Percentage of users returning within 7/30 days
- **Feature Adoption**: Percentage of users engaging with recommendation features

---

## 2. Recommendation Quality Metrics

### 2.1 Coverage
- **Catalog Coverage**: Percentage of items recommended at least once
- **User Coverage**: Percentage of users receiving personalized recommendations
- **Long-Tail Coverage**: Percentage of long-tail items recommended
- **Target**: >80% catalog coverage monthly

### 2.2 Diversity
- **Intra-List Diversity**: Average dissimilarity between items in recommendation list
- **Inter-Session Diversity**: Diversity of recommendations across sessions
- **Category Coverage**: Number of categories represented in recommendations
- **Target**: Intra-list diversity >0.7

### 2.3 Novelty
- **Average Popularity**: Mean popularity of recommended items (lower = more novel)
- **Long-Tail Ratio**: Percentage of recommendations from long-tail items
- **Unexpectedness**: How different recommendations are from user's past behavior
- **Target**: Balance between familiarity and discovery

### 2.4 Freshness
- **New Content Ratio**: Percentage of recently added items recommended
- **Recommendation Age**: Average age of recommended items
- **Timeliness**: How current recommendations are relative to trends

---

## 3. User Satisfaction Metrics

### 3.1 Explicit Satisfaction
- **Post-Recommendation Survey**: "How relevant were these recommendations?"
- **Rating of Recommendations**: User rating of recommendation quality
- **NPS (Net Promoter Score)**: Likelihood to recommend the platform
- **Feature-Specific Satisfaction**: Satisfaction with specific recommendation types

### 3.2 Implicit Satisfaction
- **Positive Engagement**: Likes, shares, saves, bookmarks
- **Negative Engagement**: Skips, dismisses, "not interested" signals
- **Session Quality**: Longer sessions, more items viewed
- **Return Behavior**: Users coming back for more recommendations

---

## 4. OKR Tracking

### 4.1 Example OKRs for Recommendation Team
**Objective**: Improve recommendation quality to drive user engagement

**Key Results**:
- Increase home page CTR from 5% to 7%
- Increase conversion rate from 2% to 3%
- Achieve >80% catalog coverage
- Reduce recommendation latency P99 from 200ms to 150ms
- Run 10+ experiments per quarter

### 4.2 Metric Dashboards
- Weekly OKR progress tracking
- Monthly business review metrics
- Quarterly OKR scoring and retrospective
- Real-time metric alerts for OKR-critical metrics

---

## 5. Counter-Metrics (Guardrails)

### 5.1 What are Guardrails
Metrics that should NOT degrade while optimizing primary metrics.

### 5.2 Common Guardrails
- **Latency**: Should not increase while improving CTR
- **Error Rate**: Should not increase with new features
- **Diversity**: Should not decrease while improving relevance
- **Catalog Coverage**: Should not decrease while improving conversion
- **User Complaints**: Should not increase with recommendation changes
- **Privacy Metrics**: Should not increase data collection without consent
