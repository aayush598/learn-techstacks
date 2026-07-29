# Cohort Analysis for SaaS

A comprehensive guide to cohort analysis — the single most powerful analytical tool for understanding your SaaS business. Retention cohorts, revenue cohorts, behavioral cohorts, and how to turn cohort insights into product decisions.

---

## Part 1: What is Cohort Analysis?

### The Core Concept

Cohort analysis groups users by a shared characteristic (typically signup date) and tracks their behavior and value over time. It answers the question: **"Do our newer customers behave like our older ones?"**

### Why Aggregate Metrics Lie

```
Aggregate Metric: "Average retention is 25% at 90 days"

This tells you NOTHING useful because:
- Early cohorts (with poor onboarding) might retain at 15%
- Recent cohorts (with improved onboarding) might retain at 35%
- Average: 25% — but it masks the improvement

Cohort Analysis reveals:
- January cohort: 15% at 90 days (problem)
- February cohort: 18% at 90 days (slight improvement)
- March cohort: 25% at 90 days (getting better)
- April cohort: 35% at 90 days (onboarding fix worked!)
```

### The Three Types of Cohorts

| Cohort Type | Groups By | Measures | Answers |
|-------------|-----------|----------|---------|
| Acquisition | Signup date | Retention, engagement | "Are newer users stickier?" |
| Behavioral | Action taken | Conversion, LTV | "Do users who integrate retain better?" |
| Revenue | First payment month | MRR, expansion, churn | "Are newer customers more valuable?" |

---

## Part 2: Retention Cohorts

### The Retention Table

This is the most important table in your analytics:

```yaml
RETENTION TABLE (% of Users Still Active)

Cohort   | Size | Wk 1 | Wk 2 | Wk 3 | Wk 4 | Mo 2 | Mo 3 | Mo 6 | Mo 12
---------|------|------|------|------|------|------|------|------|-------
Jan 2023 | 100  | 60%  | 48%  | 40%  | 35%  | 28%  | 22%  | 18%  | 15%
Feb 2023 | 110  | 62%  | 50%  | 42%  | 36%  | 29%  | 24%  | 19%  | 16%
Mar 2023 | 120  | 58%  | 45%  | 38%  | 33%  | 26%  | 21%  | 17%  | 14%
Apr 2023 | 105  | 65%  | 52%  | 44%  | 38%  | 31%  | 25%  | 20%  | 17%
May 2023 | 130  | 70%  | 58%  | 50%  | 42%  | 34%  | 28%  | 22%  | 18%
Jun 2023 | 140  | 68%  | 55%  | 47%  | 40%  | 33%  | 27%  | 21%  | —
Jul 2023 | 125  | 72%  | 60%  | 52%  | 45%  | 37%  | 30%  | 24%  | —
Aug 2023 | 135  | 75%  | 62%  | 54%  | 47%  | 39%  | 32%  | —    | —
Sep 2023 | 150  | 73%  | 61%  | 53%  | 46%  | 38%  | —    | —    | —
Oct 2023 | 155  | 78%  | 65%  | 56%  | 49%  | —    | —    | —    | —
Nov 2023 | 160  | 80%  | 68%  | 59%  | —    | —    | —    | —    | —
Dec 2023 | 170  | 82%  | 70%  | —    | —    | —    | —    | —    | —
```

### What to Look For

**Reading across a row (cohort over time):**
- How fast does this cohort decline?
- Does it flatten out (hooked users) or keep declining?
- Where's the "cliff" — the period of highest drop-off?

**Reading down a column (comparing cohorts at same age):**
- Are newer cohorts retaining better? (If yes, product improvements are working)
- Are newer cohorts retaining worse? (Something changed — investigate immediately)
- Is the trend stable, improving, or declining?

### The Three Retention Patterns

**Pattern 1: Improving (Good)**
```
Cohort  | Week 1 | Week 4 | Week 12
Jan     | 60%    | 35%    | 22%
Feb     | 62%    | 36%    | 24%
Mar     | 65%    | 38%    | 25%
```
→ Product is getting better, onboarding is improving
→ Keep doing what you're doing

**Pattern 2: Flat (Neutral)**
```
Cohort  | Week 1 | Week 4 | Week 12
Jan     | 60%    | 35%    | 22%
Feb     | 58%    | 33%    | 23%
Mar     | 61%    | 36%    | 21%
```
→ Product isn't meaningfully changing
→ Need to make deliberate improvements

**Pattern 3: Declining (Bad)**
```
Cohort  | Week 1 | Week 4 | Week 12
Jan     | 60%    | 35%    | 22%
Feb     | 55%    | 30%    | 18%
Mar     | 50%    | 28%    | 16%
```
→ Something is getting worse (more competition, worse traffic, product regression)
→ Investigate immediately — this is a business emergency

### Building Retention Cohorts in SQL

```sql
WITH first_activity AS (
  SELECT 
    user_id,
    MIN(event_time) AS first_action_date,
    DATE_TRUNC('month', MIN(event_time)) AS cohort_month
  FROM events
  WHERE event_name = 'User Signed Up'
  GROUP BY user_id
),
user_activity AS (
  SELECT 
    u.user_id,
    u.cohort_month,
    DATE_TRUNC('month', e.event_time) AS activity_month
  FROM first_activity u
  JOIN events e ON u.user_id = e.user_id
  WHERE e.event_name = 'Core Action'
  GROUP BY u.user_id, u.cohort_month, activity_month
),
cohort_sizes AS (
  SELECT 
    cohort_month,
    COUNT(DISTINCT user_id) AS cohort_size
  FROM first_activity
  GROUP BY cohort_month
),
retention_data AS (
  SELECT 
    u.cohort_month,
    u.activity_month,
    COUNT(DISTINCT u.user_id) AS active_users,
    c.cohort_size,
    -- Calculate month number (0 = signup month)
    EXTRACT('month' FROM u.activity_month) - 
    EXTRACT('month' FROM u.cohort_month) + 
    (EXTRACT('year' FROM u.activity_month) - EXTRACT('year' FROM u.cohort_month)) * 12 
    AS month_number
  FROM user_activity u
  JOIN cohort_sizes c ON u.cohort_month = c.cohort_month
  GROUP BY u.cohort_month, u.activity_month, c.cohort_size
)
SELECT 
  cohort_month,
  month_number,
  cohort_size,
  active_users,
  ROUND(active_users * 100.0 / cohort_size, 1) AS retention_pct
FROM retention_data
ORDER BY cohort_month, month_number;
```

### Building Retention Cohorts in Google Sheets

```yaml
Sheet Structure:

Column A: User ID
Column B: Signup Date
Column C: Is Active in Month 1? (TRUE/FALSE)
Column D: Is Active in Month 2? (TRUE/FALSE)
...
Column N: Is Active in Month 12? (TRUE/FALSE)

Pivot Table:
  Rows: Signup Month (extract from date)
  Values: Average of each Month column
  Format as percentages

Formulas:
  Signup Month: =TEXT(B2, "MMM YYYY")
  Month 1 Active: =IF(DATE(2024,1,1) <= B2, ...) -- requires proper date logic
```

---

## Part 3: Revenue Cohorts

### The Revenue Cohort Table

```yaml
REVENUE COHORTS ($ per Customer)

Cohort   | Size | Mo 1  | Mo 2  | Mo 3  | Mo 4  | Mo 5  | Mo 6  | Total LTV
---------|------|-------|-------|-------|-------|-------|-------|----------
Jan 2024 | 100  | $49   | $47   | $45   | $43   | $42   | $40   | $266
Feb 2024 | 110  | $49   | $48   | $46   | $44   | $43   | $42   | $272
Mar 2024 | 105  | $51   | $49   | $47   | $45   | $44   | —     | $236 (6 mo)
Apr 2024 | 120  | $53   | $51   | $49   | $47   | —     | —     | $200 (5 mo)
May 2024 | 130  | $55   | $53   | $51   | —     | —     | —     | $159 (4 mo)

Difference from Churn Table:
  - Revenue per customer declines SLOWER than customer count
  - Because churning customers are often lower-paying
  - Revenue cohorts show dollar impact, not just count impact
```

### What Revenue Cohorts Tell You

```
Reading across a row:
  - Mo 1 revenue is your ARPU (base pricing)
  - Decline from Mo 1 to Mo 2 shows impact of early churn
  - If revenue plateaus (stops declining), you have sticky high-value customers
  
Reading down a column:
  - Are newer cohorts generating more revenue per customer?
  - This could mean: pricing increases, better targeting, or more usage
```

### Revenue Cohort for Annual Plans

```yaml
ANNUAL REVENUE COHORTS

Cohort        | Q1   | Q2   | Q3   | Q4   | Yr 2 Q1 | Yr 2 Q2
--------------|------|------|------|------|---------|---------
Q1 2023 (100) | $100 | $100 | $100 | $100 | $95     | $90
Q2 2023 (120) | $100 | $100 | $100 | $100 | $92     | —
Q3 2023 (110) | $100 | $100 | $100 | $96  | —       | —
Q4 2023 (130) | $100 | $100 | $100 | —    | —       | —
```

With annual plans, revenue is constant for 12 months, then drops when renewal happens. The "Year 2" columns show renewal rates.

### Revenue Cohort Analysis in Python

```python
import pandas as pd
import numpy as np

def calculate_revenue_cohorts(subscription_data):
    """
    Calculate revenue per customer by cohort month.
    
    Args:
        subscription_data: DataFrame with columns:
            user_id, signup_date, month, revenue
    
    Returns:
        Pivot table of revenue per customer by cohort month
    """
    # Assign cohort month
    subscription_data['cohort'] = subscription_data['signup_date'].dt.to_period('M')
    
    # Calculate month number
    subscription_data['month_num'] = (
        (subscription_data['month'].dt.year - subscription_data['signup_date'].dt.year) * 12 +
        (subscription_data['month'].dt.month - subscription_data['signup_date'].dt.month)
    )
    
    # Group by cohort and month number
    cohort_data = subscription_data.groupby(['cohort', 'month_num']).agg(
        total_revenue=('revenue', 'sum'),
        user_count=('user_id', 'nunique')
    ).reset_index()
    
    # Revenue per user
    cohort_data['rev_per_user'] = (
        cohort_data['total_revenue'] / cohort_data['user_count']
    )
    
    # Pivot for display
    pivot = cohort_data.pivot_table(
        index='cohort',
        columns='month_num',
        values='rev_per_user',
        aggfunc='mean'
    ).round(2)
    
    return pivot
```

---

## Part 4: Behavioral Cohorts

### What Are Behavioral Cohorts?

Instead of grouping by signup date, group by what users DID:

| Cohort Type | Groups By | Example |
|-------------|-----------|---------|
| Activation | Completed onboarding vs. not | "Did they reach the aha moment?" |
| Integration | Connected X integration vs. not | "Did they connect Slack?" |
| Feature | Used Feature X vs. not | "Did they try reporting?" |
| Channel | Organic vs. paid | "How did they find us?" |
| Plan | Free vs. paid vs. enterprise | "What plan are they on?" |

### Behavioral Cohort Comparison

```yaml
COHORT: Integrated Slack in First Week

Metric           | Integrated | Did Not Integrate | Difference
-----------------|------------|-------------------|-----------
Week 1 Retention | 85%        | 55%               | +30pp
Week 4 Retention | 68%        | 32%               | +36pp
Month 3 Retention| 55%        | 22%               | +33pp
Month 6 Retention| 45%        | 15%               | +30pp
Average LTV      | $1,200     | $450              | +$750
Conversion to Paid| 65%       | 28%               | +37pp

INSIGHT: Getting users to connect Slack in week 1 is the strongest predictor of retention.
ACTION: Make Slack integration a required step in onboarding.
```

### Feature Adoption Cohorts

```yaml
COHORT: Used Reporting Feature in First Month

Metric           | Used Reports | Didn't Use Reports | Difference
-----------------|--------------|--------------------|-----------
Month 3 Retention| 62%          | 25%                | +37pp
Month 6 Retention| 48%          | 15%                | +33pp
Upgrade Rate     | 22%          | 8%                 | +14pp
NPS              | 45           | 12                 | +33 pts

INSIGHT: Reporting feature drives both retention AND expansion.
ACTION: Promote reporting feature more aggressively in onboarding.
```

### Creating Behavioral Cohorts in PostHog

```yaml
1. Go to "Cohorts" → "New Cohort"
2. Define criteria:
   "Users who did [event] at least [N] times in [time period]"
3. Example: "Users who did [Integration Connected] at least [1] time in [first 7 days]
4. Name: "Integrated in Week 1"
5. Save and use in retention analysis
6. Compare against "All Other Users" cohort
```

---

## Part 5: Comparing Cohorts to Find Product-Market Fit

### The PMF Cohort Framework

Superhuman founder Rahul Vohra popularized a cohort-based approach to measuring PMF:

**Ask users: "How would you feel if you could no longer use our product?"**
- Very disappointed
- Somewhat disappointed
- Not disappointed

**PMF threshold:** 40% say "Very disappointed"

### Cohort-Based PMF Tracking

```yaml
COHORT PMF SURVEY (% "Very Disappointed")

Cohort    | Month 0 | Month 1 | Month 2 | Month 3 | Month 6
----------|---------|---------|---------|---------|--------
Jan 2024  | 15%     | 25%     | 35%     | 38%     | 42%
Feb 2024  | 18%     | 28%     | 36%     | 40%     | —
Mar 2024  | 20%     | 30%     | 38%     | —       | —
Apr 2024  | 22%     | 32%     | —       | —       | —

INSIGHT:
  - PMF score improves over time for each cohort (as they use the product more)
  - PMF score is improving across cohorts (product improvements are working)
  - At month 6, the Jan cohort hit 42% — above PMF threshold!
```

---

## Part 6: Segmentation Within Cohorts

### The Cohort Analysis Tree

Don't just analyze cohorts at the aggregate level. Slice by:

```
Entire Cohort
├── By Plan Tier
│   ├── Free users
│   ├── Pro users  
│   └── Enterprise users
├── By Acquisition Channel
│   ├── Organic
│   ├── Paid (Google, LinkedIn)
│   ├── Referral
│   └── Social
├── By Company Size
│   ├── Solo / 1 person
│   ├── Small team (2-10)
│   └── Company (10+)
└── By Geography
    ├── North America
    ├── Europe
    └── Rest of World
```

### Segmentation Example

```yaml
COHORT: December 2024 — RETENTION BY PLAN TIER

Week  | Free | Pro  | Enterprise
------|------|------|-----------
1     | 55%  | 80%  | 95%
2     | 40%  | 72%  | 90%
4     | 25%  | 60%  | 85%
8     | 15%  | 48%  | 78%
12    | 10%  | 40%  | 72%

INSIGHT: 
  - Free users churn fast (only 10% at week 12)
  - Pro users are sticky (40% at week 12 — good for SMB SaaS)
  - Enterprise users are very sticky (72% at week 12)
  
ACTION:
  - Focus acquisition on Pro and Enterprise segments
  - Offer free users a limited-time discount to upgrade before they churn
```

---

## Part 7: Cohort Analysis in Action — Decision Making

### Decision 1: Is Our Onboarding Improvement Working?

```
Before: Onboarding was a 10-step process with high drop-off.
After: Simplified to 5 steps with progress bar.

Cohort Comparison:
  Cohort before change (Oct): Week 4 retention = 35%
  Cohort after change (Nov): Week 4 retention = 42%
  
  Improvement: +7pp (20% relative improvement)
  
  VERDICT: Onboarding improvement worked. Keep the new flow.
```

### Decision 2: Should We Invest in Channel X?

```
Channel A (Organic):
  Cohort: 100 users, Month 3 retention = 35%, ARPU = $50

Channel B (Google Ads):
  Cohort: 80 users, Month 3 retention = 22%, ARPU = $50

Channel C (Referrals):
  Cohort: 40 users, Month 3 retention = 48%, ARPU = $55
  
  INSIGHT: Referral users are highest quality (best retention, highest ARPU)
  ACTION: Invest in referral program. Reconsider Google Ads spend.
```

### Decision 3: Is Our Premium Tier Too Expensive?

```
Cohort: Enterprise tier users (before price increase)
  Month 3 retention: 75%
  
Cohort: Enterprise tier users (after price increase from $199 to $299)
  Month 3 retention: 68%
  
  INSIGHT: Price increase reduced retention by 7pp.
  
  Is the revenue gain worth the retention loss?
  Before: 100 customers × $199 × 75% retention = $14,925
  After: 100 customers × $299 × 68% retention = $20,332
  
  VERDICT: Higher absolute revenue despite retention loss. Keep the price.
  But monitor closely — if retention continues to decline, reconsider.
```

### Decision 4: Should We Kill Feature X?

```
Feature X users vs. non-users:
  Feature X users: Month 3 retention = 32%
  Non-Feature X users: Month 3 retention = 34%
  
  Difference: -2pp (Feature X users actually retain slightly WORSE)
  
  Feature X adoption: 8% of users
  Feature X support tickets: 15% of all tickets
  
  VERDICT: Feature X adds no retention value and generates disproportionate support.
  ACTION: Retire Feature X.
```

---

## Part 8: Advanced Cohort Techniques

### Waterfall Cohort View

Shows the flow of users through stages:

```yaml
COHORT: January 2024 (100 users)

Stage                   | Users | % of Cohort
------------------------|-------|------------
Signed Up               | 100   | 100%
Completed Onboarding    | 72    | 72%
Connected Integration   | 58    | 58%
Performed Core Action   | 45    | 45%
First Month Active      | 35    | 35%
First Payment           | 30    | 30%
Month 3 Active          | 22    | 22%
Month 6 Active          | 18    | 18%
```

### Lagged Cohort Analysis

Compare cohorts at the same "age" but different time periods:

```yaml
Cohort     | Month 0 | Month 1 | Month 2 | Month 3 | Month 6 | Month 12
Apr 2022   | 100%    | 45%     | 35%     | 28%     | 18%     | 12%
Apr 2023   | 100%    | 52%     | 42%     | 35%     | 25%     | —
Apr 2024   | 100%    | 58%     | 48%     | —       | —       | —
```

Year-over-year comparison shows if you're improving at the same rate.

### Cumulative LTV by Cohort

```yaml
Cohort     | Mo 1 | Mo 2 | Mo 3 | Mo 4 | Mo 5 | Mo 6 | Cum. LTV
Jan 2024   | $49  | $96  | $141 | $184 | $226 | $266 | $266
Feb 2024   | $49  | $97  | $143 | $187 | $230 | $272 | $272
Mar 2024   | $51  | $100 | $147 | $192 | $236 | —    | $236
```

Shows that newer cohorts are generating slightly more revenue — a good sign.

### Predictive Cohort Modeling

Use early cohort data to predict future retention:

```python
import numpy as np
from scipy.optimize import curve_fit

def retention_curve(t, a, b, c):
    """
    Fitzhugh curve model for retention prediction.
    a: initial retention drop
    b: decay rate
    c: floor retention (long-term steady state)
    """
    return c + (1 - c) * np.exp(-a * t) / (1 + b * t)

# Example: Fit model to 6 months of data
months = np.array([0, 1, 2, 3, 4, 5, 6])
retention = np.array([1.0, 0.45, 0.38, 0.33, 0.30, 0.28, 0.27])

# Fit curve
params, _ = curve_fit(retention_curve, months, retention, 
                       p0=[0.5, 0.1, 0.2])

# Predict months 7-12
future_months = np.array([7, 8, 9, 10, 11, 12])
predicted = retention_curve(future_months, *params)

print("Predicted retention:")
for m, r in zip(future_months, predicted):
    print(f"Month {m}: {r*100:.1f}%")
```

---

## Part 9: The Cohort Analysis Dashboard

### Weekly Cohort Review

```yaml
WEEKLY COHORT REVIEW (15 minutes)

1. Open retention table (90 seconds)
   - Do a quick visual scan
   - Check the most recent cohort column
   - Any obvious changes?

2. Compare latest cohort to 3 months ago (90 seconds)
   - Same time since signup?
   - Improving, declining, or flat?

3. Check one behavioral cohort (3 minutes)
   - This week: "Did users who connected integration retain better?"

4. Check revenue trend (3 minutes)
   - Are newer cohorts generating more per customer?

5. Document ONE insight (3 minutes)
   - What's the most important thing you learned?

6. Define ONE action (3 minutes)
   - What will you do differently based on this?
```

### Monthly Cohort Analysis Template

```yaml
MONTHLY COHORT ANALYSIS — [MONTH] [YEAR]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RETENTION TREND:
  Latest cohort (Dec 2024): [X]% at month 3
  3 months ago (Sep 2024): [Y]% at month 3
  6 months ago (Jun 2024): [Z]% at month 3
  Trend: [Improving | Flat | Declining]

REVENUE TREND:
  Latest cohort: $[X] revenue per customer (first month)
  Same period last year: $[Y]
  Change: [Z]%

BEHAVIORAL INSIGHT OF THE MONTH:
  [Behavior] cohort retains at [X]% versus [Y]% for non-[behavior]
  [Action item based on this]

SEGMENT INSIGHT:
  [Segment] has [X]% better retention than average
  [Action item based on this]

TOP CONCERN:
  [Concern identified from cohort data]
  [Mitigation plan]

TOP OPPORTUNITY:
  [Opportunity identified from cohort data]
  [Action to capture]
```

---

## Part 10: Common Cohort Analysis Mistakes

### Mistake 1: Too Few Cohorts

**Problem:** Only have 2-3 cohorts visible. Can't see trends.

**Fix:** Show at least 6-12 cohorts. This reveals trends, not just snapshots.

### Mistake 2: Comparing Unequal Time Periods

**Problem:** January cohort has 12 months of data, November cohort has 1 month. They look the same because both start at 100%.

**Fix:** Always compare cohorts at the same "age" (e.g., "all cohorts at month 3").

### Mistake 3: Ignoring Cohort Size

**Problem:** January cohort (10 users) has 50% retention at month 6. February cohort (100 users) has 25% retention. You think January is better.

**Reality:** 5 users vs. 25 users. February retained more users, just at a lower percentage.

**Fix:** Show BOTH percentages AND absolute numbers in your cohort table.

### Mistake 4: Not Segmenting

**Problem:** Aggregate retention looks flat. You think nothing is changing.

**Reality:** One segment improved (hiding another segment that declined).

**Fix:** Always segment cohorts by at least plan tier and acquisition channel.

### Mistake 5: Looking Only at the Latest Cohort

**Problem:** Latest cohort has great retention. You celebrate.

**Reality:** Latest cohort is only 2 weeks old — of course retention looks good.

**Fix:** Always evaluate cohorts at the same age (minimum 30 days data).

### Mistake 6: Mixing Cohorts with Different Characteristics

**Problem:** You launched a new pricing page and your cohorts look better.

**Reality:** You also started running ads on a new channel that attracts different users. Which change caused the improvement?

**Fix:** Isolate changes — don't run multiple experiments on the same cohort group.

### Mistake 7: Not Acting on Insights

**Problem:** You've known for 3 months that users who connect Slack retain better. You haven't changed the onboarding to make Slack connection easier.

**Fix:** Every cohort insight should produce an action item. If you're not acting, stop analyzing.

---

## The One-Page Cohort Cheat Sheet

```
┌────────────────────────────────────────────────────────────┐
│                   COHORT ANALYSIS CHEAT SHEET               │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  THREE TYPES OF COHORTS:                                   │
│  1. Acquisition (by signup date) — retention over time     │
│  2. Behavioral (by action) — compare behavior groups      │
│  3. Revenue (by first payment) — financial value over time │
│                                                            │
│  WHAT TO LOOK FOR:                                         │
│  ────────────────                                           │
│  • Across a row: How fast does the cohort decay?           │
│  • Down a column: Are newer cohorts better than old ones?  │
│  • Clusters: Do certain segments behave differently?       │
│  • Plateau: Does retention flatten (sticky users) or       │
│    continue declining (not sticky)?                        │
│                                                            │
│  KEY QUESTIONS:                                            │
│  • Is our product getting stickier over time?              │
│  • Which behaviors predict retention?                      │
│  • Which acquisition channels yield the best users?        │
│  • Are pricing changes affecting retention?                │
│  • Is our product-market fit improving?                    │
│                                                            │
│  COMMON MISTAKES:                                          │
│  • Comparing cohorts at different ages                     │
│  • Not segmenting (aggregate hides the truth)              │
│  • Ignoring cohort size (small cohorts are noisy)          │
│  • Analysis without action                                 │
│                                                            │
│  MONTHLY ACTION:                                           │
│  1. Update retention table with latest month               │
│  2. Check one behavioral cohort                            │
│  3. Identify one insight                                   │
│  4. Define one action                                      │
│  5. Schedule next month's review                           │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Final Advice

> **Cohort analysis is the closest thing to a crystal ball in SaaS.**
> Aggregate metrics tell you what happened.
> Cohort analysis tells you what's GOING to happen.

A cohort table that shows declining retention for newer cohorts is an early warning that your business will shrink. A cohort table that shows improving retention means you're building a more valuable product.

Check your cohorts monthly. Act on what they tell you. And always, always segment.