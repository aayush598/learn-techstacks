# Leading vs Lagging Indicators for SaaS

Understanding the difference between leading and lagging indicators is crucial for solo founders. Lagging indicators tell you what happened (too late to change it). Leading indicators tell you what's about to happen (giving you time to act). This guide covers both categories comprehensively, with emphasis on predictive metrics and early warning signals.

---

## Part 1: The Fundamental Framework

### The Problem with Lagging Metrics

Most founders spend 80% of their time looking at lagging indicators:
- MRR (last month's number)
- Churn rate (customers who already left)
- LTV (requires months of data to calculate)

These are useful for reporting but dangerous for decision-making. By the time you see a churn spike, those customers are already gone.

### The Leading Indicator Advantage

Leading indicators predict future outcomes. They give you:

| Leading Indicator | Predicts | Warning Time |
|-------------------|----------|--------------|
| Activation rate | 90-day retention | 30-90 days |
| DAU/MAU ratio | Churn risk | 30-60 days |
| Trial → Paid conversion | New MRR | 14-30 days |
| Support ticket volume | Churn risk | 7-30 days |
| Feature adoption | Expansion revenue | 30-90 days |
| Page load time | Conversion rate | Immediate |
| NPS score | Referral volume | 30-90 days |

### The Metrics Hierarchy

```
                      ┌──────────────────┐
                      │   Cash Balance   │  ← Ultimate lagging indicator
                      │   (Survival)     │     of all decisions
                      └────────┬─────────┘
                               │
                      ┌────────▼─────────┐
                      │    MRR / ARR      │  ← Lagging indicator
                      │   (Revenue)      │     of acquisition & retention
                      └────────┬─────────┘
                               │
                      ┌────────▼─────────┐
                      │    Churn Rate     │  ← Semi-lagging (happened)
                      │    LTV / CAC     │     but informs future
                      └────────┬─────────┘
                               │
                      ┌────────▼─────────┐
                      │   Trial Conv.    │  ← Leading (in progress)
                      │   Activation     │     but visible today
                      └────────┬─────────┘
                               │
                      ┌────────▼─────────┐
                      │   Page Views     │  ← Early leading
                      │   Signups        │     (hours/days ahead)
                      └──────────────────┘
```

---

## Part 2: The Complete Indicator Catalog

### Group 1: Revenue Indicators

#### Lagging: MRR (Monthly Recurring Revenue)

**What it is:** Revenue from subscriptions this month
**Time delay:** 30 days (you see it after the month ends)
**Can't change:** Yesterday's MRR is fixed

**Analogy:** Your bank account balance. It tells you where you are, but you can't unfire employees.

**When to use:** Reporting, investor updates, tax calculations

#### Leading: New Signup Trends

**What it is:** Number of new users starting free trials or signing up
**Predicts:** MRR in 14-90 days (depending on trial length + conversion time)
**Actionable:** Yes — you can increase or decrease ad spend today

**Formula:**
```
Predicted MRR (30 days out) = Signups × Trial Conversion Rate × ARPU
```

**Example:**
- 200 signups this week
- Historical trial conversion: 15%
- ARPU: $49
- Predicted MRR contribution in 30 days: 200 × 0.15 × $49 = $1,470

**Setting:**
```
Cell A1: This Week's Signups
Cell B1: =200
Cell C1: =B1 * 0.15 * 49
```

#### Leading: Trial Starts by Channel

**What it is:** Breakdown of trial starts by acquisition channel
**Predicts:** Which channels will drive future MRR
**Actionable:** Reallocate budget to highest-converting channels before spending more

**Example:**
```
Channel      | Trials | Conv Rate | Predicted MRR
Organic      | 100    | 18%       | $882
Google Ads   | 80     | 12%       | $470
Referrals    | 30     | 25%       | $368
Twitter/X    | 40     | 8%        | $157
```

#### Leading: Free → Paid Conversion Rate (Real-time)

**What it is:** Percentage of trials or freemium users converting to paid
**Predicts:** Revenue in the next billing cycle
**Actionable:** If conversion drops, fix onboarding immediately

**Leading indicator alert:** If conversion drops below historical baseline, you'll see MRR decline in 30-60 days.

### Group 2: Retention Indicators

#### Lagging: Churn Rate

**What it is:** Customers who already canceled
**Time delay:** At least 30 days (you see it after cancellations happen)
**Can't change:** Those customers are gone

**Problem with churn as a lagging indicator:**
- By the time you measure monthly churn of 5%, you've lost 5% of your revenue
- You can't re-acquire those customers at the same cost
- You can only reduce future churn, not undo past churn

#### Leading: Usage Decline

**What it is:** Decrease in daily/weekly active usage, feature adoption, or login frequency
**Predicts:** Churn in 30-60 days
**Signal strength:** Very strong — usage drop is the #1 predictor of churn

**Formula:**
```
Churn Risk Score = 1 - (Current DAU / Average DAU over last 30 days)
```

If a customer's usage drops by 50% for two weeks, they have a 70%+ probability of churning within 60 days.

**Implementation in your database:**
```sql
SELECT 
  customer_id,
  AVG(dau_30_days_ago) as avg_dau_30d,
  AVG(dau_last_7_days) as avg_dau_7d,
  (AVG(dau_last_7_days) / AVG(dau_30_days_ago)) as usage_ratio,
  CASE 
    WHEN (AVG(dau_last_7_days) / AVG(dau_30_days_ago)) < 0.5 THEN 'HIGH_CHURN_RISK'
    WHEN (AVG(dau_last_7_days) / AVG(dau_30_days_ago)) < 0.75 THEN 'MEDIUM_CHURN_RISK'
    ELSE 'LOW_CHURN_RISK'
  END as risk_level
FROM daily_usage
WHERE customer_id = ?
GROUP BY customer_id;
```

#### Leading: First Activation Time (Time to Value)

**What it is:** Time between signup and the user experiencing core value
**Predicts:** 30-day and 90-day retention
**Signal strength:** Very strong — faster activation = higher retention

**Benchmark per activation time:**
```
Activation Time | 90-Day Retention
< 5 minutes     | 80%+
5-30 minutes    | 65%
30-60 minutes   | 45%
> 60 minutes    | 25%
```

**Action:** If activation time is > 30 minutes, focus all product efforts on reducing it.

#### Leading: Feature Stickiness

**What it is:** The percentage of active users who use your core feature(s) each day/week
**Predicts:** Long-term retention and NRR expansion
**Formula:**
```
Feature Stickiness % = DAU using core feature / Total DAU
```

**Benchmark:**
- Core feature stickiness > 40%: Excellent
- Core feature stickiness 20-40%: Good
- Core feature stickiness < 20%: Your core feature isn't sticky enough

#### Leading: Onboarding Completion Rate

**What it is:** Percentage of new users who complete your defined onboarding steps
**Predicts:** 7-day activation and 30-day retention

**Steps to track:**
1. Account created (100%)
2. First integration connected (85%)
3. First import completed (70%)
4. First report generated (55%)
5. First export/sharing (45%) ← This is often the activation point

**Formula:**
```
Drop-off rate at Step N = 1 - (Users reaching Step N / Users reaching Step N-1)
```

#### Leading: Support Ticket Sentiment

**What it is:** Sentiment analysis of support tickets and customer interactions
**Predicts:** Churn (negative sentiment), expansion (positive sentiment)

**Simple implementation:**
```python
# Simple sentiment analysis for support tickets
from textblob import TextBlob

def analyze_ticket_sentiment(ticket_text):
    blob = TextBlob(ticket_text)
    sentiment = blob.sentiment.polarity  # -1 to 1
    
    if sentiment < -0.3:
        return "Negative"  # Churn risk
    elif sentiment > 0.3:
        return "Positive"  # Expansion opportunity
    else:
        return "Neutral"
```

### Group 3: Growth Indicators

#### Lagging: MRR Growth Rate

**What it is:** (Current MRR - Previous MRR) / Previous MRR
**Time delay:** 30 days
**Tells you:** Whether you grew last month

#### Leading: Net New Leads

**What it is:** New leads entering your funnel (email signups, demo requests, trial starts)
**Predicts:** MRR growth in 30-90 days

**Forecasting formula:**
```
Predicted MRR in 90 days = Current MRR + 
  (Leads × Lead-to-Trial% × Trial-to-Paid% × ARPU × 3 months) +
  (Current Customers × Expansion Rate × ARPU × 3 months) -
  (Current Customers × Monthly Churn × ARPU × 3 months)
```

#### Leading: Inbound Email Volume

**What it is:** Number of inbound emails from prospects and customers
**Predicts:** Sales pipeline and support load

**Correlation:** For B2B SaaS, a 20% increase in inbound emails typically precedes a 15% increase in qualified leads within 2 weeks.

#### Leading: Social Listening (Brand Mentions)

**What it is:** Number of organic mentions of your product on social media, forums, review sites
**Predicts:** Future organic signups (7-30 day lead)

**Tools:**
- Google Alerts (free)
- Mention (paid)
- Brand24 (paid)

**Track:**
- Positive mentions → Predicts signups
- Negative mentions → Predicts support tickets and churn
- Feature requests → Predicts expansion opportunity

### Group 4: Product Indicators

#### Lagging: Daily Active Users (DAU)

**What it is:** Number of users who use your product each day
**Time delay:** 24 hours minimum
**Problem:** Today's DAU already happened

#### Leading: Session Start Rate (Hourly)

**What it is:** Number of new sessions starting each hour
**Predicts:** Today's DAU within 4-6 hours
**Actionable:** Set up real-time alerts for session start drops

#### Leading: Page Load Time (Performance)

**What it is:** How fast your application loads
**Predicts:** Bounce rate, trial conversion, user satisfaction

**Benchmark data:**
```
Load Time | Bounce Rate Impact | Conversion Impact
< 1 sec   | Baseline           | Baseline
1-2 sec   | +32% bounce        | -15% conversion
2-3 sec   | +90% bounce        | -38% conversion
3-5 sec   | +123% bounce       | -50% conversion
> 5 sec   | +160% bounce       | -70% conversion
```

**Action:** If load time exceeds 2 seconds, stop feature work and fix performance.

#### Leading: Error Rate

**What it is:** Percentage of user actions that result in errors
**Predicts:** Churn, support tickets, negative reviews

**Thresholds:**
- < 0.1% error rate: Good
- 0.1% - 1%: Monitor
- > 1%: Immediate action required

**Implementation:**
```javascript
// Client-side error tracking
window.onerror = function(message, source, lineno, colno, error) {
  analytics.track('Error Occurred', {
    message: message,
    source: source,
    line: lineno,
    column: colno,
    stack: error?.stack
  });
};
```

#### Leading: NPS Responses (Real-time)

**What it is:** Net Promoter Score collected immediately after key events
**Predicts:** Referral volume, expansion, churn

**Best practice:** Survey after onboarding (predicts 30-day retention) and after support interaction (predicts churn).

### Group 5: Financial Indicators

#### Lagging: Cash Balance

**What it is:** Money in the bank
**Time delay:** Real-time (but reflects past decisions)
**Problem:** If you check and have 2 months runway, you needed to act 4 months ago

#### Leading: Runway Trend (Burn Rate Acceleration)

**What it is:** Rate at which your burn rate is changing
**Predicts:** When you'll hit zero cash

**Formula:**
```
Runway Trend = (This Month's Burn Rate / Last Month's Burn Rate) - 1
```

If burn rate is accelerating (trend > 0), your actual runway is shorter than your calculated runway.

**Example:**
```
Month 1: Burn $5K, Runway 12 months (calculated)
Month 2: Burn $6K (+20%), Trend > 0
Month 3: Burn $7.2K (+20% again)
Reality: Runway is closer to 8 months, not 12.
```

#### Leading: Accounts Receivable Aging

**What it is:** Unpaid invoices past due
**Predicts:** Cash flow issues in 30-60 days

**Track:**
```
0-30 days overdue: $X (normal)
31-60 days overdue: $Y (caution)
61-90 days overdue: $Z (risk)
90+ days overdue: $W (likely loss)
```

#### Leading: Failed Payment Rate

**What it is:** Percentage of recurring payments that fail (expired cards, insufficient funds)
**Predicts:** Involuntary churn in 7-14 days

**Benchmark:**
- Good: < 3% failure rate
- Normal: 3-7% failure rate
- Warning: > 7% failure rate — immediate dunning optimization needed

**Action:**
```javascript
// Stripe dunning logic (retry schedule)
const retrySchedule = [
  { delay: 3, days: 3 },     // Retry in 3 days
  { delay: 5, days: 8 },     // Retry in 5 more days
  { delay: 7, days: 15 },    // Retry in 7 more days
  { delay: 10, days: 25 },   // Retry in 10 more days
];
```

---

## Part 3: Early Warning Systems

### The Solo Founder Early Warning Dashboard

This should be the FIRST thing you check every morning (takes 30 seconds):

```
┌────────────────────────────────────────────────────────┐
│                  EARLY WARNING SYSTEM                   │
├────────────────────────────────────────────────────────┤
│                                                        │
│  🟢 GREEN - All Clear                                   │
│  ─────────────────                                      │
│  • Signups: 12 today (above avg of 8)                   │
│  • Trial Conv: 18% (at baseline)                        │
│  • Error Rate: 0.05% (below 1% threshold)              │
│  • Load Time: 1.2s (below 2s threshold)                │
│                                                        │
│  🟡 YELLOW - Monitor                                    │
│  ──────────────────                                     │
│  • DAU decline: -8% this week (trending down)           │
│  • 1st activation time: 45 min (above 30 min target)   │
│  • Support tickets: +15% (may need investigation)      │
│                                                        │
│  🔴 RED - Immediate Action                              │
│  ────────────────                                       │
│  • Failed payments: 12% (above 7% threshold)           │
│    → ACTION: Review dunning email sequence             │
│  • Churn risk customers: 8 (highest ever)               │
│    → ACTION: Personal outreach to top 3 at-risk        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Setting Up Your Early Warning System

#### Step 1: Define Thresholds

For each leading indicator, define three thresholds:

| Indicator | Green | Yellow | Red |
|-----------|-------|--------|-----|
| Trial → Paid | > 15% | 10-15% | < 10% |
| Activation Time | < 30 min | 30-60 min | > 60 min |
| DAU/MAU (weekly) | > 30% | 20-30% | < 20% |
| Failed Payments | < 3% | 3-7% | > 7% |
| Error Rate | < 0.1% | 0.1-1% | > 1% |
| Support Ticket Sentiment | Positive | Mixed | Negative |
| NPS | > 30 | 0-30 | < 0 |

#### Step 2: Automate Alerts

Set up these alerts in your stack:

**Slack alerts (critical, immediate):**
```yaml
# Alert configuration
alerts:
  - name: "Failed Payment Spike"
    condition: failed_payment_rate > 7%
    channel: "#alerts-critical"
    message: "🔴 Failed payments at {rate}% - check dunning"
    
  - name: "Error Rate Critical"
    condition: error_rate > 1%
    channel: "#alerts-critical"
    message: "🔴 Error rate at {rate}% - rollback or fix"
    
  - name: "Zero Signups 48h"
    condition: signups_48h == 0
    channel: "#alerts-critical"
    message: "🔴 Zero signups in 48 hours"

  - name: "Churn Risk Cluster"
    condition: high_risk_customers > 10
    channel: "#alerts-retention"
    message: "🔴 {count} customers at high churn risk"
```

**Email alerts (daily summary):**
```yaml
daily_summary:
  subject: "SaaS Daily Early Warning Summary {date}"
  sections:
    - title: "Green (Normal)"
      metrics: [trial_conversion, error_rate, load_time]
    - title: "Yellow (Monitor)"
      metrics: [dau_trend, activation_time, support_volume]
    - title: "Red (Act Now)"
      metrics: [failed_payments, churn_risk_count, revenue_anomaly]
```

**Phone alerts (emergency only):**
```yaml
phone_alerts:
  - condition: error_rate > 5%  # Site is down/broken
  - condition: payment_gateway_down
  - condition: cash_balance < 1_month_runway
```

#### Step 3: Weekly Review Protocol

Every Monday, spend 15 minutes on this leading indicator review:

```
1. Scan the Early Warning Dashboard (30 seconds)
2. Investigate any RED indicators (5 minutes)
3. Choose ONE leading indicator to improve this week (3 minutes)
4. Set a specific, measurable action (2 minutes)
5. Schedule next week's review (automatic)
```

**Example weekly action:**
```
WARNING: Activation time is 45 minutes (above 30 min target)
THIS WEEK'S ACTION: Add interactive onboarding walkthrough
SUCCESS METRIC: Reduce activation time to under 35 minutes
NEXT WEEK: Review activation time trend
```

---

## Part 4: Predictive Metrics Models

### Simple Predictive Model for MRR

```
30-Day Forward MRR = Current MRR + (Leads × Conv Rate × ARPU × Upsell Factor) - (Churn Risk × ARPU)
```

Where:
- Leads = projected signups based on current trajectory
- Conv Rate = historical trial-to-paid conversion
- ARPU = current average revenue per user
- Upsell Factor = historical expansion rate
- Churn Risk = weighted sum of at-risk customer accounts

### Implementation in Google Sheets:

```
Cell A1: Current MRR (=B2)
Cell A2: Average Daily Signups (last 14 days)
Cell A3: Signups per 30 days (=A2*30)
Cell A4: Trial Conversion Rate (= 0.15 if 15%)
Cell A5: New Customer MRR (=A3*A4*ARPU)
Cell A6: Expansion MRR (=Current Expansion Rate * Current MRR)
Cell A7: Projected Churn (=Churn Risk Customers * ARPU)
Cell A8: Predicted MRR in 30 days (=B2 + A5 + A6 - A7)
```

### Cohort-Based Prediction (More Accurate)

Predict future retention for each cohort:

```sql
WITH cohort_data AS (
  SELECT 
    DATE_TRUNC('month', first_signup_date) as cohort_month,
    COUNT(*) as customers_in_cohort,
    AVG(3_month_retention) as avg_retention
  FROM customers
  GROUP BY cohort_month
)
SELECT 
  cohort_month,
  customers_in_cohort,
  avg_retention,
  LAG(avg_retention, 1) OVER (ORDER BY cohort_month) as prev_cohort_retention,
  avg_retention - LAG(avg_retention, 1) OVER (ORDER BY cohort_month) as retention_trend
FROM cohort_data
ORDER BY cohort_month DESC;
```

If retention_trend is consistently negative, future MRR will decline even with constant acquisition.

### Churn Prediction Model (Logistic Regression)

For the technical solo founder, here's a simple churn prediction model:

```python
import pandas as pd
from sklearn.linear_model import LogisticRegression

# Features that predict churn
features = [
    'days_since_last_login',
    'support_tickets_30d',
    'feature_usage_count',
    'plan_tier',
    'months_as_customer',
    'payment_failures_90d',
    'nps_score'
]

# Train on historical data
X = historical_data[features]
y = historical_data['churned']

model = LogisticRegression()
model.fit(X, y)

# Predict churn risk for current customers
current_customers['churn_probability'] = model.predict_proba(
    current_customers[features]
)[:, 1]

# Flag high-risk customers
at_risk = current_customers[
    current_customers['churn_probability'] > 0.5
].sort_values('churn_probability', ascending=False)
```

### Points to Track for Prediction Model

| Feature | Why It Predicts Churn | How to Track |
|---------|----------------------|--------------|
| Days since last login | Disengagement | Product analytics |
| Logins per week (trend) | Declining engagement | Product analytics |
| Support tickets (30d) | Either frustration or high engagement | Help desk |
| Feature breadth (% of features used) | Low = low investment | Product analytics |
| Team member count | More members = stickier | Account data |
| Payment failures | Financial friction | Payment processor |
| NPS response timing | Late responses = disengaged | Survey tool |
| Account age | Newer = higher churn risk | Customer DB |

---

## Part 5: Leading Indicators by Business Stage

### Pre-PMF (< $5K MRR)

**Primary leading indicator:** Repeat usage (DAU/WAU)
**Why:** If users aren't coming back, you don't have product-market fit
**Daily focus:** "Are users returning?"

**Additional leading indicators:**
- % of trials that reach activation
- Time to first "aha moment"
- Organic signup ratio (word of mouth)
- Feature adoption of core feature

**Ignore for now:**
- MRR growth rate (too volatile)
- LTV/CAC (too few data points)
- NRR (premature)

### Early PMF ($5K - $20K MRR)

**Primary leading indicator:** Trial conversion rate
**Why:** Indicates whether your product-to-market communication is working
**Weekly focus:** "Are we converting users who try?"

**Additional leading indicators:**
- Days to first value (activation time)
- Feature adoption of paid features
- Early churn signals (< 30 day usage drop)
- Referral rate

### Growth ($20K - $100K MRR)

**Primary leading indicator:** Net revenue retention (NRR)
**Why:** Predicts whether your existing base is growing or shrinking
**Monthly focus:** "Are existing customers buying more?"

**Additional leading indicators:**
- Expansion MRR drivers (which features drive upgrades)
- Channel efficiency (CAC by channel)
- High-value account health scores
- NRR by segment

### Scale ($100K+ MRR)

**Primary leading indicator:** Magic number
**Why:** Measures sales and marketing efficiency
**Quarterly focus:** "Are we spending efficiently to grow?"

**Additional leading indicators:**
- Enterprise pipeline velocity
- Win rate by segment
- Time-to-close by deal size
- Competitive win/loss analysis

---

## Part 6: The Leading Indicator Playbook

### Play 1: Improving Trial Conversion (Leading Indicator)

**Signal:** Trial conversion rate declining
**Warning:** MRR decline in 14-30 days
**Actions:**

```
Week 1: Audit onboarding flow
  - Remove unnecessary steps
  - Add progress indicator
  - Reduce time to "aha moment"
  
Week 2: Add in-app guidance
  - Tooltips for key features
  - Email sequence for inactive trials
  - "Success checklist" in dashboard

Week 3: Personal outreach
  - Solo founder calls top 10 trials/week
  - Ask what's blocking conversion
  - Offer extended trial + help

Week 4: Measure and iterate
  - Check conversion rate improvement
  - Double down on what worked
  - Remove what didn't work
```

### Play 2: Responding to Usage Decline (Leading Indicator)

**Signal:** Customer usage drops 40%+ over 2 weeks
**Warning:** Churn in 30-60 days
**Actions:**

```
Immediate: 
  - Flag customer in CRM as at-risk
  - Send personalized check-in email from founder
  
Within 48 hours:
  - Call or video meeting (not text)
  - Ask open-ended questions: 
    "What changed in your workflow?"
    "What feature would bring you back?"
    "Is there a problem we haven't solved?"

Week 2:
  - Implement the #1 requested change
  - Send "we heard you" update
  - Offer discount or pause subscription

Week 3-4:
  - Monitor usage for recovery
  - If no recovery: offer graceful exit
  - Learn from the loss
```

### Play 3: Capitalizing on Positive Leading Indicators

**Signal:** NPS > 40, high usage, low support tickets
**Opportunity:** Expansion revenue in 30-90 days
**Actions:**

```
Immediate:
  - Add to "expansion list" CRM segment
  - Monitor for upgrade triggers:
    * Hitting usage limits
    * Requesting team features
    * Mentioning growth

Week 2:
  - Send case study interview request
  - Ask for referral (warm intro)
  - Share advanced feature tips

Week 4:
  - Propose upgrade with personalized ROI
  - Offer annual pricing discount
  - Ask for testimonial (social proof)

Week 8:
  - Follow up on upgrade proposal
  - Ask about team expansion
  - Introduce new features they'd benefit from
```

---

## Part 7: Building Your Leading Indicator System

### Step 1: Identify Your Core Leading Indicators

Choose 3-5 based on your stage:

| Stage | Leading Indicators |
|-------|-------------------|
| Pre-PMF | Signups, Activation rate, DAU/MAU, Time to value |
| Early | Trial conversion, Onboarding completion, Feature adoption |
| Growth | NRR, Channel CAC, Account health, Expansion triggers |
| Scale | Magic number, Pipeline velocity, Win rate |

### Step 2: Set Up Data Collection

Minimum viable tracking:
- **Stripe Export** → Revenue data (manual, weekly)
- **PostHog/Amplitude** → Product usage (free tier)
- **Google Analytics** → Traffic, signups (free)
- **Help desk** (Intercom, Crisp) → Support volume (free tier)

### Step 3: Build Leading Indicator Dashboard

Create a separate dashboard from your lagging metrics:

```
┌────────────────────────────────────────────────────────────┐
│                 LEADING INDICATOR DASHBOARD                 │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  TODAY'S SIGNALS (Hourly Update):                         │
│  ┌─────────────────────┬────────┬────────┬──────────┐     │
│  │ Indicator           │ Value   │ Status │ vs Avg   │     │
│  ├─────────────────────┼────────┼────────┼──────────┤     │
│  │ Signups             │ 14     │ 🟢     │ +40%     │     │
│  │ Activation (today)  │ 3      │ 🟡     │ -20%     │     │
│  │ Error Rate          │ 0.3%   │ 🟢     │ normal   │     │
│  │ Load Time           │ 1.4s   │ 🟢     │ normal   │     │
│  └─────────────────────┴────────┴────────┴──────────┘     │
│                                                            │
│  7-DAY TRENDS:                                             │
│  Signups:     ▁▃▄▆▇███ (+15% WoW)                        │
│  Activation:  ██▇▆▅▄▃ (-28% WoW) ← INVESTIGATE          │
│  DAU/MAU:     ▄▅▆▅▆▇█ (+3% WoW)                          │
│                                                            │
│  PREDICTED 30-DAY OUTCOME:                                 │
│  ┌─────────────────────┬─────────────────┬────────────┐   │
│  │ Metric              │ Predicted        │ Confidence │   │
│  ├─────────────────────┼─────────────────┼────────────┤   │
│  │ MRR (30 days)       │ $8,400 (+12%)   │ High       │   │
│  │ Churn Rate (30 days)│ 4.8%             │ Medium     │   │
│  │ Customers (30 days) │ 184 (+8%)        │ Medium     │   │
│  └─────────────────────┴─────────────────┴────────────┘   │
│                                                            │
│  ACTION REQUIRED (from activation decline):               │
│  → Review onboarding flow changes from last week          │
│  → Add in-app guidance for new users                      │
│  → A/B test simplified signup                             │
└────────────────────────────────────────────────────────────┘
```

### Step 4: Weekly Leading Indicator Review

Schedule: Every Monday, 9:00 AM, 15 minutes

```
Monday Morning Leading Indicator Review:

1. Open Leading Indicator Dashboard (30s)
2. Note any RED indicators (2 min)
3. Choose ONE indicator to improve this week (3 min)
4. Define specific action with success metric (5 min)
5. Add action to Monday task list (2 min)
6. Set next Monday's review (30s)

Template for weekly action:
  Indicator: [name]
  Current: [value]
  Target: [value]
  Action: [specific action]
  Success metric: [measurable outcome]
  Expected result in: [timeframe]
```

---

## Part 8: Common Leading Indicator Mistakes

### Mistake 1: Reacting to Noise, Not Signal

**Problem:** You see a one-day signup drop and panic, changing your pricing.

**Fix:** Use moving averages (7-day or 14-day) before reacting. One day is noise; a trend is signal.

```python
# Calculate 7-day moving average before deciding
def should_react(daily_data):
    ma_7 = daily_data.rolling(7).mean()
    ma_30 = daily_data.rolling(30).mean()
    
    # Only react if 7-day MA deviates 20% from 30-day MA
    deviation = (ma_7[-1] - ma_30[-1]) / ma_30[-1]
    return abs(deviation) > 0.20
```

### Mistake 2: Confusing Activity with Progress

**Problem:** High signup volume makes you feel good, but conversion is declining.

**Fix:** Always pair volume metrics with quality metrics:
- Signups + Trial Conversion Rate
- Traffic + Bounce Rate
- DAU + Feature Adoption

### Mistake 3: Analyzing Without Acting

**Problem:** You spend hours analyzing data but never change anything.

**Fix:** Before looking at any metric, ask: "What specific action will I take based on this?"

### Mistake 4: Too Many Leading Indicators

**Problem:** You track 20 leading indicators, overwhelm yourself, and track nothing effectively.

**Fix:** Maximum 5 leading indicators. One primary, four secondary.

### Mistake 5: Not Segmenting

**Problem:** Average activation time is 20 minutes (looks good), but enterprise users take 45 minutes (bad for that segment).

**Fix:** Always segment by:
- Acquisition channel
- Customer segment
- Plan tier
- Geography

---

## Quick Reference Card

Print this and put it on your wall:

```
METRIC            | TYPE      | PREDICTS              | LEAD TIME
──────────────────────────────────────────────────────────────
Signups           | Leading   | MRR                   | 14-90 days
Trial Conversion  | Leading   | MRR                   | 14-30 days
Activation Time   | Leading   | Retention             | 30-90 days
Usage (DAU/MAU)   | Leading   | Churn                 | 30-60 days
Feature Adoption  | Leading   | Expansion, NRR        | 30-90 days
Error Rate        | Leading   | Churn, Reviews        | Immediate
Support Sentiment | Leading   | Churn, Expansion      | 7-30 days
NPS               | Leading   | Referrals, Retention  | 30-90 days
Failed Payments   | Leading   | Involuntary Churn     | 7-14 days
Load Time         | Leading   | Conversion            | Immediate
──────────────────────────────────────────────────────────────
MRR               | LAGGING   | Financial Health      | 30 days
Churn Rate        | LAGGING   | Business Model        | 30 days
LTV/CAC           | LAGGING   | Unit Economics        | 90-180 days
Cash Balance      | LAGGING   | Survival              | Real-time
```

**The golden rule:** For every lagging metric you track, identify TWO leading indicators that predict it. Track the leading indicators weekly. Review the lagging metrics monthly.

**The solo founder principle:** You only have time to act on the top 3 leading indicators. Choose wisely, track consistently, and act immediately when they signal danger.