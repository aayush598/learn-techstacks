# Feature Adoption Metrics

How to track, measure, and improve feature adoption in your SaaS product. This guide covers feature adoption metrics, feature usage scoring frameworks, and data-driven feature retirement decisions for solo founders.

---

## Part 1: Why Feature Adoption Matters

### The Feature Paradox

As a solo founder, you build features because users ask for them or you believe they'll add value. But here's the reality:

- **30% of features** in the typical SaaS product are used by less than 10% of users
- **15% of features** account for 85% of usage
- **40% of features** have less than 5% weekly active usage

The cost of maintaining unused features is invisible but real:
- Code complexity increases → bugs take longer to fix
- UI becomes cluttered → new users get confused
- Support burden grows → you answer questions about irrelevant features
- Development velocity slows → every change requires updating unused code paths

Feature adoption metrics expose which features to double down on, which to improve, and which to kill.

### Feature Adoption vs. Feature Awareness

| Concept | Definition | Measurement |
|---------|------------|-------------|
| Feature Awareness | Users know the feature exists | Survey, in-app messaging opens |
| Feature Adoption | Users try the feature at least once | Event tracking |
| Feature Stickiness | Users use the feature regularly | Weekly/Daily active usage |
| Feature Mastery | Users use advanced capabilities | Power user metrics |

A feature can be widely known but poorly adopted, or secretly loved by a small group. Both are important signals.

---

## Part 2: Feature Adoption Metrics Framework

### The Four Levels of Feature Adoption

```
Level 1: Discovery (user sees the feature)
Level 2: Trial (user tries it once)
Level 3: Adoption (user uses it 3+ times)
Level 4: Habit (user uses it regularly)
```

### Core Feature Adoption Metrics

#### 1. Ever Used Rate

Percentage of users who have ever used a feature.

```
Ever Used Rate = Users who used feature at least once / Total Users × 100
```

**Benchmarks:**
- Core features: > 60% ever used
- Secondary features: 20-60% ever used
- Niche features: < 20% ever used

**When to check:** Monthly, for each feature

#### 2. Weekly Active Usage Rate

Percentage of weekly active users who use the feature each week.

```
Weekly Active Usage = Users who used feature in last 7 days / Total WAUs × 100
```

**Benchmarks:**
- Sticky features: > 30% weekly active
- Occasional features: 10-30% weekly active
- Rarely used features: < 10% weekly active

#### 3. Feature Stickiness (DAU/MAU for a Feature)

How often users come back to use a specific feature.

```
Feature Stickiness = DAU using feature / MAU using feature × 100
```

**Benchmarks:**
- Habit-forming features: > 40% stickiness
- Utility features: 20-40% stickiness
- Infrequent features: < 20% stickiness

#### 4. Time to First Use

How long after signup does a user try a feature for the first time.

```
Time to First Use = Date of first feature use - Date of signup (in days)
```

**Benchmarks:**
- Features found naturally: < 7 days
- Features needing discovery: 7-30 days
- Features hidden or complex: > 30 days

#### 5. Repeat Usage Rate

Percentage of users who try a feature and then use it again.

```
Repeat Usage Rate = Users who used feature 2+ times / Users who used it once × 100
```

**Benchmarks:**
- Habitual features: > 50% repeat rate
- Transactional features: 20-50% repeat rate
- One-time features: < 20% repeat rate

#### 6. Feature Depth

How deeply users explore a feature's capabilities.

```
Feature Depth = Average number of sub-actions within a feature per user
```

Example:
- Reports feature has: Create Report, Schedule Report, Export Report, Share Report
- Feature Depth = Average number of these actions per user

#### 7. Feature Contribution to Retention

Do users who adopt a feature retain better?

```
Retention Impact = (Retention of feature users - Retention of non-feature users) / Retention of non-feature users × 100
```

**Example:**
- Users who use Reporting: 90-day retention = 65%
- Users who don't use Reporting: 90-day retention = 40%
- Retention Impact = (65% - 40%) / 40% = 62.5% lift

---

## Part 3: Feature Usage Scoring

### The Feature Score Card

Score each feature on these dimensions to prioritize development and maintenance:

```yaml
Feature Scoring Matrix:

1. Adoption (30% weight)
   - Ever Used Rate (0-10 points)
   - Weekly Active Usage (0-10 points)
   - Repeat Usage Rate (0-10 points)

2. Business Impact (30% weight)
   - Correlation with conversion (0-10 points)
   - Correlation with retention (0-10 points)
   - Revenue attribution (0-10 points)

3. User Satisfaction (20% weight)
   - NPS of feature users (0-10 points)
   - Feature-specific feedback (0-10 points)
   - Support tickets (inverse, 0-10 points)

4. Strategic Value (20% weight)
   - Differentiation from competitors (0-10 points)
   - Roadmap alignment (0-10 points)
   - Future potential (0-10 points)
```

#### Scoring Formula

```
Feature Score = (Adoption Score × 0.30) + (Business Impact × 0.30) + (Satisfaction × 0.20) + (Strategic Value × 0.20)
```

#### Feature Score Interpretation

| Score | Classification | Action |
|-------|---------------|--------|
| 8-10 | Star | Invest more — this is your competitive advantage |
| 6-8 | Growth | Improve adoption — better onboarding, more features |
| 4-6 | Maintain | Keep as-is — serves a niche but don't over-invest |
| 2-4 | Legacy | Reduce investment — consider deprecating |
| 0-2 | Dead | Retire — actively remove or replace |

### Feature Scoring Spreadsheet Template

```
Feature Name | Ever Used | WAU% | Repeat Rate | Conv Impact | Ret Impact | NPS | Support | Strategy | Score
-------------|-----------|------|-------------|-------------|------------|-----|---------|----------|------
Task Create  | 92% (10)  | 68% (9) | 85% (10)  | High (9)   | High (9)   | 8.2 | Low (9) | Core (10)| 9.4
Reporting   | 45% (5)   | 22% (3) | 40% (4)    | Med (6)    | High (8)   | 7.5 | Med (6) | Diff (8) | 5.6
Calendar    | 30% (3)   | 8% (1)  | 20% (2)    | Low (3)    | Low (3)    | 6.0 | Low (8) | Low (4)  | 3.1
```

### Automated Feature Scoring

For the technical solo founder, automate scoring with a script:

```python
def calculate_feature_score(feature_data):
    # Normalize each metric to 0-10
    def normalize(value, min_val, max_val):
        return min(10, max(0, (value - min_val) / (max_val - min_val) * 10))
    
    # Adoption metrics (30%)
    ever_used_score = normalize(feature_data['ever_used_pct'], 0, 100)
    wau_score = normalize(feature_data['wau_pct'], 0, 50)
    repeat_score = normalize(feature_data['repeat_pct'], 0, 100)
    adoption = (ever_used_score + wau_score + repeat_score) / 3 * 0.30
    
    # Business impact (30%)
    conv_score = feature_data['conv_impact'] * 10  # 0.0 to 1.0
    ret_score = feature_data['ret_impact'] * 10
    rev_score = normalize(feature_data['revenue_attribution'], 0, 10000)
    impact = (conv_score + ret_score + rev_score) / 3 * 0.30
    
    # Satisfaction (20%)
    nps_score = normalize(feature_data['nps'], -100, 100)
    support_score = 10 - normalize(feature_data['support_tickets_pct'], 0, 20)
    satisfaction = (nps_score + support_score) / 2 * 0.20
    
    # Strategic value (20%)
    strategy = normalize(feature_data['strategic_value'], 0, 10) * 0.20
    
    total = adoption + impact + satisfaction + strategy
    return round(total, 1)
```

---

## Part 4: Feature Adoption Lifecycle

### The Feature Adoption Funnel

```
Awareness (100% of target users)
    ↓
    ↓ Discovery: 60% learn about it
    ↓
Trial (60% of aware users)
    ↓
    ↓ First Use: 80% try it once
    ↓
Adoption (48% of aware users)
    ↓
    ↓ Repeat Use: 60% use it again
    ↓
Habit (29% of aware users)
    ↓
    ↓ Regular Use: 70% use it weekly
    ↓
Mastery (20% of aware users)
```

### Improving Adoption at Each Stage

#### Stage 1: Awareness → Discovery

**Problem:** Users don't know the feature exists.

**Solutions:**
```
- In-app announcement (modal or banner on login)
- What's New / Changelog page
- Email announcement to relevant segment
- Tooltip on dashboard or feature entry point
- Documentation and blog post
- Social media (Twitter, LinkedIn) highlight
```

**Measurement:** Feature page views, announcement click-through rate.

**Target:** > 60% of target users aware within 14 days of launch.

#### Stage 2: Discovery → Trial

**Problem:** Users know about the feature but don't try it.

**Solutions:**
```
- Reduce friction (fewer clicks to start)
- Add context (why should they use it?)
- Show social proof ("85% of teams use this")
- Offer a template or preset to get started
- Provide a guided setup flow
- Lower commitment (sample output before full use)
```

**Measurement:** Click-through from awareness to first action.

**Target:** > 50% conversion from discovery to trial.

#### Stage 3: Trial → Repeat

**Problem:** Users try it once but don't come back.

**Solutions:**
```
- Improve the first experience (speed, reliability)
- Trigger follow-up (email: "Your report is ready")
- Surface the feature at relevant moments
- Add personalization ("here's what you created")
- Show progression ("you've used this 3 times, here's pro tip")
- Make it part of a workflow (can't complete task X without it)
```

**Measurement:** % of triers who use it again.

**Target:** > 40% repeat rate.

#### Stage 4: Repeat → Habit

**Problem:** Users use it sometimes but not regularly.

**Solutions:**
```
- Add notifications, reminders, or scheduled execution
- Integrate with daily workflow (dashboard widget, email digest)
- Add shareability/collaboration
- Create templates or presets
- Power user features (shortcuts, bulk actions, API)
- Gamification (streaks, achievements)
```

**Measurement:** Weekly/daily active usage rate.

**Target:** > 30% weekly active among users who've adopted.

### Feature Adoption Timeline

Track how adoption evolves over time:

```
Feature: Reporting

Week 1 Post-Launch:
  - Awareness: 20% (announcement just went out)
  - Trial: 5%
  - Repeat: 1%

Week 4 Post-Launch:
  - Awareness: 65% (in-app banner seen by most)
  - Trial: 40% (800 of 2000 users tried it)
  - Repeat: 25% (200 of 800 used it again)

Week 12 Post-Launch:
  - Awareness: 80%
  - Trial: 55%
  - Repeat: 40%
  - Habit: 22% (weekly usage)

Week 24 Post-Launch:
  - Awareness: 85%
  - Trial: 60%
  - Repeat: 45%
  - Habit: 28%
```

**The adoption curve:** Most features plateau around week 12-16. If adoption isn't at target by then, it likely won't improve without significant changes.

---

## Part 5: Measuring Feature Adoption in Practice

### Event Structure for Feature Tracking

```javascript
// Track feature-related events
analytics.track('Feature Viewed', {
  feature_name: 'reporting',
  source: 'sidebar',
  plan_tier: 'pro'
});

analytics.track('Feature First Used', {
  feature_name: 'reporting',
  feature_version: 'v2',
  trigger: 'onboarding_flow'
});

analytics.track('Feature Used', {
  feature_name: 'reporting',
  action: 'create_report',
  duration_seconds: 145,
  template_used: true
});

analytics.track('Feature Shared', {
  feature_name: 'reporting',
  share_method: 'email',
  recipient_role: 'team_member'
});
```

### Feature Adoption Dashboard

Create this dashboard in your analytics tool:

```
┌─────────────────────────────────────────────────────────────┐
│                  FEATURE ADOPTION DASHBOARD                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  OVERVIEW (Last 30 Days):                                   │
│  ┌──────────────┬──────────┬─────────┬─────────┬─────────┐ │
│  │ Feature      │ Ever Used│ WAU%    │ Stick.  │ Status  │ │
│  ├──────────────┼──────────┼─────────┼─────────┼─────────┤ │
│  │ Tasks        │ 92%      │ 68%     │ 45%     │ 🟢 Star │ │
│  │ Projects     │ 78%      │ 45%     │ 38%     │ 🟢 Star │ │
│  │ Reports      │ 55%      │ 22%     │ 28%     │ 🟡 Grow  │ │
│  │ Calendar     │ 30%      │ 8%      │ 18%     │ 🟡 Maint │ │
│  │ API          │ 18%      │ 12%     │ 55%     │ 🟡 Maint │ │
│  │ Templates    │ 12%      │ 5%      │ 35%     │ 🔴 Legacy│ │
│  │ Gamification │ 8%       │ 2%      │ 15%     │ 🔴 Dead  │ │
│  └──────────────┴──────────┴─────────┴─────────┴─────────┘ │
│                                                             │
│  TRENDS (WAU% Over Time):                                   │
│  Tasks:    ████████████████████ 68% (stable)                │
│  Reports:  ██████░░░░░░░░░░░░░░ 22% (growing +5% MoM)     │
│  Calendar: ███░░░░░░░░░░░░░░░░░ 8% (declining -2% MoM)     │
│                                                             │
│  NEW FEATURES (Last 60 Days):                               │
│  Feature A: 35% ever used, 15% WAU (on track)              │
│  Feature B: 12% ever used, 3% WAU (below target)           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Feature Adoption by User Segment

Break down adoption by:

```
Segment: Plan Tier

Feature  | Free Users | Pro Users | Enterprise
---------|------------|-----------|------------
Tasks    | 88%        | 94%       | 96%
Reports  | 35%        | 55%       | 78%
API      | 5%         | 18%       | 85%
Calendar | 25%        | 32%       | 28%

Segment: Account Age

Feature  | < 30 days | 30-90 days | 90+ days
---------|-----------|------------|----------
Tasks    | 75%       | 88%        | 95%
Reports  | 20%       | 45%        | 68%
API      | 8%        | 15%        | 25%
Calendar | 15%       | 28%        | 38%
```

**Insights:**
- Reports adoption grows significantly with account age → users discover it over time
- API usage is heavily plan-dependent → free users don't need it
- Calendar adoption plateaus → not a feature users grow into

---

## Part 6: Feature Retirement Decisions

### When to Retire a Feature

**The Cost of Keeping Unused Features:**

1. **Maintenance cost:** Every feature requires testing, documentation, and support
2. **Cognitive load:** New users navigate through clutter
3. **Technical debt:** Unused code paths increase bug surface area
4. **Opportunity cost:** Time spent maintaining could be spent building

**The Decision Framework:**

```
1. Adoption check: < 10% ever used AND < 5% weekly active
2. Revenue check: No revenue attribution (not driving upgrades)
3. Retention check: No correlation with retention (users don't leave without it)
4. Support check: Generates more support tickets than value
5. Feedback check: No customer complaints when discussed for removal
6. Strategic check: Not aligned with product direction
```

If ALL six conditions are met → Strong candidate for retirement.

### Feature Retirement Process

#### Phase 1: Announce (2 weeks)

```yaml
Week 1:
  - Add "Legacy" badge in UI (feature is deprecated)
  - Send email to users who have used feature in last 90 days
  - Post changelog entry about planned removal
  - Provide migration guide (if applicable)

Week 2:
  - In-app banner on feature pages
  - Reminder email to power users
  - Offer 1:1 call for users who need help migrating
```

#### Phase 2: Soft Remove (4 weeks)

```yaml
Weeks 3-4:
  - Remove feature from main navigation
  - Keep accessible via direct URL or settings toggle
  - Track how many users access it via the hidden path

Weeks 5-6:
  - Add interstitial page ("This feature has been replaced by X")
  - Redirect feature URL to alternative or explanation page
  - Continue monitoring for any users hitting the URL

Week 7:
  - Measure: How many users found the hidden feature?
  - If < 1% of active users → proceed to full removal
  - If > 1% → Extend soft removal period, improve migration
```

#### Phase 3: Remove (Permanent)

```yaml
Week 8:
  - Delete feature code from codebase
  - Remove database tables/columns (after backup)
  - Update documentation
  - Remove from UI everywhere
  - Add redirect to relevant alternative
  - Update onboarding to remove references
  
Week 9:
  - Monitor support tickets for "where did X go?"
  - Respond to each with migration path
  - Track: < 5 support tickets = successful removal
```

### Feature Retirement Decision Matrix

```
Feature | Ever Used | WAU | Stickiness | Retention Impact | Support % | Decision
--------|-----------|-----|------------|------------------|-----------|---------
Calendar| 30%       | 8%  | 18%        | 2% lift          | 5%        | Maintain (niche)
Templates| 12%      | 5%  | 35%        | 1% lift          | 8%        | Retire (low adoption)
Gamific. | 8%       | 2%  | 15%        | -1% (negative!)  | 12%       | Retire (negative impact)
API     | 18%       | 12% | 55%        | 15% lift         | 3%        | Keep (strategic, high retention)
```

### The "1% Rule"

If a feature is used by less than 1% of your active users in a given month, it's costing you more to maintain than it's worth, UNLESS:

1. It's a premium/enterprise-only feature driving upgrades
2. It's strategically important for a specific segment you're targeting
3. It generates significant positive word-of-mouth
4. It has high revenue per user among the small group that uses it

---

## Part 7: Feature Adoption Improvement Playbook

### Play 1: The Empty State Opportunity

**Strategy:** Use empty states to promote features.

```
BAD: Empty state shows "No reports yet" with nothing else
GOOD: Empty state shows "No reports yet. 
      Create your first report → [button] 
      or learn how reports help you track team productivity → [learn more]"
```

### Play 2: Contextual Promotion

**Strategy:** Suggest features at relevant moments.

```
If user creates 10+ tasks:
  → Surface: "You've created 10 tasks! Try organizing them into Projects."
  → Feature: Projects

If user has 5+ unfinished tasks:
  → Surface: "Looks busy! Schedule time for these tasks with Calendar view."
  → Feature: Calendar

If user invites 3+ team members:
  → Surface: "Your team is growing! Track their workload with Reports."
  → Feature: Reports
```

### Play 3: Progressive Disclosure

**Strategy:** Introduce features gradually as users advance.

```
Week 1: Core features only (tasks, projects)
Week 2: Collaboration features (comments, mentions)
Week 3: Organization features (labels, filters)
Week 4: Advanced features (automations, integrations)
Month 2: Power features (API, custom fields, reports)
```

### Play 4: Feature Templates

**Strategy:** Reduce the blank page problem.

```
Feature: Reports
Without template: User needs to create report from scratch (high friction)
With template: "Monthly Team Report" template pre-configured (low friction)

Conversion improvement: 3x more reports created with templates
```

### Play 5: Integration with Core Flow

**Strategy:** Make the feature part of a workflow users already do.

```
Before: "View Reports" is a separate tab (discoverable but optional)
After: After completing a project, automatically surface a project summary report

Conversion improvement: 5x more report views when integrated into workflow
```

### Play 6: Email and Push Notifications

**Strategy:** Drive users back to features they've started but not finished.

```
1. User starts creating a report but doesn't finish
2. 24 hours later: "Your report draft is waiting. 
   Finish it in 2 minutes → [link to draft]"
3. 72 hours later: "We saved your report draft. 
   Would you like us to complete it with default settings? → [auto-complete]
```

### Play 7: Social Proof and Case Studies

**Strategy:** Show how other users benefit from the feature.

```
In-app testimonial: 
  "Acme Corp reduced reporting time by 80% using automated reports. 
  Start your first report → [button]"
```

---

## Part 8: Feature Adoption by Product Stage

### Pre-PMF Stage (< $5K MRR)

**Focus:** Identify the ONE core feature that drives retention.

**Process:**
```
1. Track usage of every feature
2. Run correlation: Which features do retained users use?
3. Identify the "aha moment" feature
4. Remove everything else or hide it behind settings
5. Obsess over improving the core feature adoption
```

**Metric that matters:** Core feature stickiness (DAU/MAU of core action)

### Early PMF ($5K - $20K MRR)

**Focus:** Expand feature adoption to increase stickiness.

**Process:**
```
1. Identify top 3 features used by power users
2. Build onboarding paths for each feature
3. Track time-to-first-use for each feature
4. A/B test different promotion strategies
5. Measure: Does multi-feature adoption reduce churn?
```

**Metric that matters:** Average number of features adopted per user

### Growth Stage ($20K - $100K MRR)

**Focus:** Feature adoption as a growth lever.

**Process:**
```
1. Segment users by feature adoption profile
2. Create feature-specific power user programs
3. Build feature-based upsell paths
4. Measure NRR by number of features adopted
5. Retire features that have < 5% adoption
```

**Metric that matters:** NRR by feature adoption segment

### Scale Stage ($100K+ MRR)

**Focus:** Feature optimization, personalization, and enterprise needs.

**Process:**
1. Build personalized feature recommendations (ML-driven if possible)
2. Create role-based feature presets
3. Enterprise feature adoption programs
4. Feature gatekeeping for pricing tiers
5. Advanced feature analytics (time-in-feature, efficiency metrics)

---

## Part 9: Technical Implementation

### Feature Adoption Database Schema

```sql
-- Feature registry
CREATE TABLE features (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  key VARCHAR(100) NOT NULL UNIQUE,
  description TEXT,
  feature_group VARCHAR(100),
  launch_date DATE,
  owner VARCHAR(100),
  status VARCHAR(50) DEFAULT 'active',
  created_at TIMESTAMP DEFAULT NOW()
);

-- User feature events
CREATE TABLE feature_events (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  feature_key VARCHAR(100) NOT NULL,
  event_type VARCHAR(50) NOT NULL, -- 'view', 'first_use', 'use', 'share'
  metadata JSONB,
  session_id VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  
  FOREIGN KEY (user_id) REFERENCES users(id),
  INDEX idx_feature_key (feature_key),
  INDEX idx_user_feature (user_id, feature_key),
  INDEX idx_created_at (created_at)
);

-- User feature state
CREATE TABLE user_features (
  user_id UUID NOT NULL,
  feature_key VARCHAR(100) NOT NULL,
  first_used_at TIMESTAMP,
  last_used_at TIMESTAMP,
  usage_count INTEGER DEFAULT 0,
  weekly_use_count INTEGER DEFAULT 0,
  is_power_user BOOLEAN DEFAULT FALSE,
  
  PRIMARY KEY (user_id, feature_key),
  FOREIGN KEY (user_id) REFERENCES users(id),
  INDEX idx_last_used (last_used_at)
);
```

### Feature Adoption Queries

```sql
-- Ever Used Rate for each feature
SELECT 
  f.key,
  f.name,
  COUNT(DISTINCT uf.user_id) as ever_used,
  (SELECT COUNT(*) FROM users WHERE status = 'active') as total_users,
  ROUND(COUNT(DISTINCT uf.user_id) * 100.0 / 
    (SELECT COUNT(*) FROM users WHERE status = 'active'), 1) as ever_used_pct
FROM features f
LEFT JOIN user_features uf ON f.key = uf.feature_key
  AND uf.usage_count > 0
GROUP BY f.key, f.name
ORDER BY ever_used_pct DESC;

-- Weekly Active Usage
SELECT 
  f.key,
  f.name,
  COUNT(DISTINCT uf.user_id) as weekly_users,
  (SELECT COUNT(DISTINCT user_id) 
   FROM feature_events 
   WHERE created_at > NOW() - INTERVAL '7 days'
   AND event_type = 'use') as total_weekly_active,
  ROUND(COUNT(DISTINCT uf.user_id) * 100.0 / 
    (SELECT COUNT(DISTINCT user_id) 
     FROM feature_events 
     WHERE created_at > NOW() - INTERVAL '7 days'
     AND event_type = 'use'), 1) as wau_pct
FROM features f
JOIN user_features uf ON f.key = uf.feature_key
  AND uf.last_used_at > NOW() - INTERVAL '7 days'
GROUP BY f.key, f.name
ORDER BY wau_pct DESC;

-- Feature Stickiness (DAU/MAU)
SELECT 
  f.key,
  f.name,
  COUNT(DISTINCT CASE WHEN fe.created_at > NOW() - INTERVAL '1 day' 
    THEN fe.user_id END) as dau,
  COUNT(DISTINCT CASE WHEN fe.created_at > NOW() - INTERVAL '30 days' 
    THEN fe.user_id END) as mau,
  ROUND(
    COUNT(DISTINCT CASE WHEN fe.created_at > NOW() - INTERVAL '1 day' 
      THEN fe.user_id END) * 100.0 /
    NULLIF(COUNT(DISTINCT CASE WHEN fe.created_at > NOW() - INTERVAL '30 days' 
      THEN fe.user_id END), 0), 1
  ) as stickiness
FROM features f
JOIN feature_events fe ON f.key = fe.feature_key
WHERE fe.event_type = 'use'
GROUP BY f.key, f.name
ORDER BY stickiness DESC;

-- Feature Adoption by Cohort
WITH cohorts AS (
  SELECT 
    DATE_TRUNC('month', created_at) as cohort_month,
    user_id
  FROM users
),
feature_first_use AS (
  SELECT 
    user_id,
    feature_key,
    MIN(created_at) as first_use_date
  FROM feature_events
  WHERE event_type = 'first_use'
  GROUP BY user_id, feature_key
)
SELECT 
  c.cohort_month,
  f.key as feature_key,
  COUNT(DISTINCT c.user_id) as cohort_size,
  COUNT(DISTINCT ffu.user_id) as adopted,
  ROUND(COUNT(DISTINCT ffu.user_id) * 100.0 / 
    COUNT(DISTINCT c.user_id), 1) as adoption_pct
FROM cohorts c
LEFT JOIN feature_first_use ffu ON c.user_id = ffu.user_id
JOIN features f ON ffu.feature_key = f.key
GROUP BY c.cohort_month, f.key
ORDER BY c.cohort_month DESC, adoption_pct DESC;
```

### Feature Usage API Endpoints

```javascript
// API route for tracking feature usage
app.post('/api/track/feature', async (req, res) => {
  const { featureKey, action, metadata } = req.body;
  const userId = req.user.id;
  
  // Record event
  await db.query(
    `INSERT INTO feature_events (user_id, feature_key, event_type, metadata)
     VALUES ($1, $2, $3, $4)`,
    [userId, featureKey, action, JSON.stringify(metadata)]
  );
  
  // Update user feature state
  await db.query(
    `INSERT INTO user_features (user_id, feature_key, first_used_at, last_used_at, usage_count)
     VALUES ($1, $2, NOW(), NOW(), 1)
     ON CONFLICT (user_id, feature_key) 
     DO UPDATE SET 
       last_used_at = NOW(),
       usage_count = user_features.usage_count + 1,
       weekly_use_count = CASE 
         WHEN user_features.last_used_at > NOW() - INTERVAL '7 days' 
         THEN user_features.weekly_use_count + 1 
         ELSE 1 
       END`,
    [userId, featureKey]
  );
  
  res.json({ success: true });
});
```

---

## Part 10: The Solo Founder Feature Workflow

### Monthly Feature Review (1 hour)

```
Week 1: Feature Adoption Review
1. Run feature adoption report (5 min)
2. Identify top 3 features by adoption (5 min)
3. Identify bottom 3 features by adoption (5 min)
4. Check new feature adoption (< 3 months old) (5 min)
5. Run feature-retention correlation (10 min)
6. Decide: What to kill, what to improve (15 min)
7. Update feature scoring matrix (15 min)
```

### Feature Investment Decisions

Use this decision tree for every feature:

```
Is the feature used by > 10% of active users?
├── YES → Is it sticky (> 30% WAU)?
│   ├── YES → INVEST MORE: Improve, expand, promote
│   └── NO → IMPROVE ADOPTION: Better onboarding, triggers
└── NO → Does it drive retention or revenue?
    ├── YES → Does a small group LOVE it?
    │   ├── YES → MAINTAIN: Keep but don't grow
    │   └── NO → Is it strategic?
    │       ├── YES → Invest in adoption
    │       └── NO → CONSIDER RETIREMENT
    └── NO → Does it generate complaints when discussed for removal?
        ├── YES → INVESTIGATE: Who uses it? Why?
        └── NO → RETIRE: Remove the feature
```

### Feature Adoption Goals Template

```
Quarter: Q3 2024

Feature Adoption Goals:
1. Reporting: Increase WAU from 22% to 35%
   - Action: Add report scheduling, email delivery
   - Owner: Solo founder (you)
   - Timeline: Week 4

2. Calendar: Reduce without losing customers
   - Action: Hide from nav, track access
   - Owner: Solo founder (you)
   - Timeline: Week 6

3. API: Increase free-tier trial from 5% to 12%
   - Action: Add quickstart template for free tier
   - Owner: Solo founder (you)
   - Timeline: Week 8

Features to Watch:
- Templates (12% ever used) → Decline detected, plan for retirement in Q4
- Gamification (8% ever used) → Already in soft removal phase
```

---

## Quick Reference: Feature Adoption Metrics

```
METRIC                | FORMULA                                          | TARGET
──────────────────────┼──────────────────────────────────────────────────┼─────────
Ever Used Rate        | Users who ever used / Total users                | > 60% (core)
Weekly Active Usage   | Users who used this week / Total WAUs           | > 30% (sticky)
Feature Stickiness    | DAU of feature / MAU of feature × 100            | > 40%
Time to First Use     | Date of first use - Signup date (days)          | < 7 days
Repeat Usage Rate     | Users w/ 2+ uses / Users w/ 1+ use × 100        | > 50%
Feature Depth         | Avg sub-actions per user                         | > 3 (complex)
Retention Lift        | Ret(feature users) - Ret(non-users) / Ret(non)   | > 20%
Feature Score         | Weighted composite (see scoring matrix)          | > 6.0
────────────────────────────────────────────────────────────────────────────
DECISION THRESHOLDS
Invest: Score > 8, Ever Used > 60%, WAU > 30%
Improve: Score 6-8, adoption below target but potential
Maintain: Score 4-6, niche but valuable
Retire: Score < 4, Ever Used < 10%, WAU < 5%
```

The most important principle for solo founders: **Build fewer features, but make every one count.** Every feature you add is a feature you need to maintain, document, support, and track. Feature adoption metrics aren't just about measuring usage — they're about deciding what NOT to build next.