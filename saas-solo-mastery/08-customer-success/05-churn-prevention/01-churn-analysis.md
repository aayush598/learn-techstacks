# Churn Analysis

## Understanding Churn

Churn is the rate at which customers stop paying for your product. It's the single most important metric for SaaS businesses because it directly determines whether you grow or shrink.

**The churn math:**
- If you acquire 10 customers/month and lose 10 customers/month → Zero growth
- If you acquire 10 and lose 5 → Net +5/month (growing)
- If you acquire 10 and lose 15 → Net -5/month (shrinking)

**For solo founders,** churn is especially painful because:
- Every lost customer represents hours of acquisition effort wasted
- You have limited capacity to replace lost customers
- Churn signals product-market fit issues

### Types of Churn

**Voluntary churn:** Customer actively cancels. They decided to leave.
**Involuntary churn:** Payment fails, account expires, technical issue.
**Passive churn:** Customer stops using but doesn't cancel (lapsed).

**Logo churn:** % of customers who cancel (count-based).
**Revenue churn:** % of MRR lost (revenue-based). More important.

## Cohort Analysis

### What Is Cohort Analysis?

Tracking groups of customers who signed up in the same time period. This shows how behavior changes over time and whether newer cohorts are better or worse than older ones.

### Building a Weekly Retention Cohort

**Step 1: Group signups by week**
```
Week 1 (Jan 1-7): 50 signups
Week 2 (Jan 8-14): 45 signups
Week 3 (Jan 15-21): 60 signups
```

**Step 2: Track each cohort's activity over time**
For each cohort, count how many are still active in each subsequent week.

**Step 3: Calculate retention rates**
```
Cohort    Wk1    Wk2    Wk3    Wk4    Wk5
Week 1    100%   70%    60%    55%    50%
Week 2    100%   72%    62%    56%    -
Week 3    100%    68%    58%    -      -
```

**Step 4: Read the cohort table**

Reading left to right: How does retention decline over time?
- Most churn happens in week 1 (30% drop) — focus retention there
- After week 4, retention stabilizes (50%) — these are your core users

Reading top to bottom: Is retention improving?
- Week 2 cohort retains slightly better than Week 1 (72% vs 70%) — positive trend
- Week 3 cohort is worse (68%) — investigate why

### Monthly Revenue Cohort

Even more important than activity cohorts:

```
Cohort    Month1  Month2  Month3  Month4  Month5  Month6
Jan       $1,000  $700    $600    $550    $500    $450
Feb       $900    $630    $540    $495    $450    -
Mar       $1,200  $840    $720    $660    -       -
```

Each cohort is total revenue from that signup cohort in each month.

**Analysis:**
- Month 1-2: 30% revenue drop (activation and early churn)
- Month 2-6: ~10% drop per month (natural churn)
- Revenue per cohort is increasing (Feb > Jan, Mar > Feb) — good sign

### Tools for Cohort Analysis

**Free:**
- Google Sheets (manual but effective)
- PostHog (free, open-source, built-in cohorts)
- ChartMogul (free trial, revenue-focused)

**Paid:**
- ProfitWell (free for basic metrics)
- Baremetrics ($79/mo, revenue analytics)
- Mixpanel/Amplitude (product + revenue cohorts)

## Identifying Churn Reasons

### The Churn Survey

When a customer cancels, ask them why. Immediately.

**Cancellation survey:**
"Why are you leaving [Product]?" (single choice or multi-select)
- Too expensive
- Missing features
- Found a better solution
- No longer need this type of product
- Too difficult to use
- Poor support
- Other (please specify)

**Follow-up (open):**
"What could we have done differently?"

**Send within 1 hour of cancellation.** Response rates are highest immediately.

### Churn Interview

For your highest-value churned customers, schedule a 15-minute exit interview:

"Hi [Name],

I'm sorry to see you go. I'd love to understand your decision so I can improve [Product]. Would you be open to a 15-minute call?

As a thank-you, I'd be happy to provide a prorated refund or extend your access for data export.

Best,
[Your Name]"

**Interview questions:**
1. "What prompted you to cancel?"
2. "What was the main reason you signed up originally?"
3. "What changed?"
4. "What did we do well?"
5. "What could we have done better?"
6. "What solution are you using instead?"
7. "What would it take for you to come back?"

### Churn Reason Categories

After collecting data, categorize churn reasons:

**Price-related (30-40% of churn):**
- Too expensive for current needs
- Found a cheaper alternative
- Budget cuts

**Product-related (25-35% of churn):**
- Missing critical feature
- Product too buggy or slow
- Poor user experience
- Doesn't solve the problem effectively

**Fit-related (15-20% of churn):**
- No longer need the product
- Changed jobs or roles
- Company went out of business
- Seasonal usage (churn and return)

**Experience-related (10-15% of churn):**
- Poor onboarding experience
- Poor customer support
- Felt neglected or ignored

**Competitor-related (5-10% of churn):**
- Found a competitor with better features/price
- Was using us and a competitor, consolidated on competitor

### Analyzing Churn Reasons

| Category | % of Churn | Preventable? | Action |
|----------|-----------|--------------|--------|
| Price | 35% | Maybe | Review pricing, offer downgrade |
| Missing features | 30% | Yes | Roadmap prioritization |
| No longer need | 15% | No | Accept it) |
| Poor onboarding | 10% | Yes | Improve onboarding |
| Competition | 5% | Maybe | Competitive analysis |
| Support | 5% | Yes | Improve support |

**Focus on preventable churn.** Not all churn is bad — some customers genuinely don't need your product anymore.

## Churn Segmentation

### Segment by Customer Type

| Segment | Churn Rate | Revenue Impact | Action |
|---------|-----------|----------------|--------|
| Enterprise | 2%/mo | High | Personal retention |
| Mid-market | 4%/mo | Medium | Health monitoring |
| Small team | 6%/mo | Medium | Automated retention |
| Freelancer | 10%/mo | Low | Self-serve retention |

**Prioritize retention efforts on segments with highest revenue impact.**

### Segment by Tenure

| Tenure | Churn Rate | Implication |
|--------|-----------|-------------|
| 0-30 days | 20-40% | Onboarding/activation issues |
| 1-3 months | 10-15% | Value not yet realized |
| 3-6 months | 5-8% | Not fully integrated |
| 6-12 months | 3-5% | Core users, but still at risk |
| 12+ months | 1-3% | Most loyal customers |

**Action by tenure:**
- 0-30 days: Improve onboarding and activation
- 1-3 months: Value reinforcement and feature discovery
- 3-6 months: Check-in calls, expansion opportunities
- 6+ months: Loyalty programs, advocacy requests

### Segment by Behavior

**Usage-based segments:**
- Power users (daily active): Lowest churn
- Regular users (weekly): Low churn
- Occasional users (monthly): Moderate churn
- Lapsed users (inactive 30+ days): Highest churn

**Train lapsed users first.** Before they can become churned, they become lapsed. Detect lapsed and re-engage.

## Win-Back Campaigns

### Re-engaging Churned Customers

30-40% of churned customers can be won back with the right approach.

**Timing:**
- 7 days after churn: "We miss you" email
- 30 days after churn: "What's changed?" email + offer
- 90 days after churn: Final re-engagement attempt
- 6 months after churn: "We've improved" campaign

### Win-Back Email Sequence

**Email 1 (Day 7): Acknowledgment**
Subject: We're sorry to see you go
"We noticed you canceled your [Product] subscription. We'd love to understand why and see if there's anything we can do to win you back. Reply to this email — I personally read every response."

**Email 2 (Day 30): What's New**
Subject: A lot has changed since you left
"Since you left, we've shipped [major features] and improved [key area]. Here's a quick summary: [bullet points]. We'd love to have you back for a second look. Here's 30 days free: [link]"

**Email 3 (Day 90): Value Reminder**
Subject: Still thinking about [Product]
"Hi [Name], just checking in. If your needs have changed, we'd love to welcome you back. Here's a quick look at what's new: [link]. No pressure — just wanted to keep the door open."

**Email 4 (Day 180): Final Attempt**
Subject: Coming back to [Product]?
"It's been 6 months. If you're ever looking for a solution to [problem], we're here. Your account is still available. Here's a special offer to come back: [offer]."

### Win-Back Offers

- 30-day free trial (no commitment)
- 25-50% off first 3 months
- Free onboarding or migration assistance
- Access to new features they missed
- Extended trial of premium features

### Win-Back Metrics

| Metric | Target |
|--------|--------|
| Win-back rate | 10-30% of churned customers |
| Time to win-back | 30-90 days |
| Cost per win-back | $50-200 |
| Re-churn rate of won-back | Higher than new customers (3-6 months) |
| Revenue recovered | 10-20% of churned MRR |

## Preventing Churn Before It Happens

### Early Warning Signs

**Usage decline:**
- Logins dropped 50%+ week over week
- Core actions stopped (reports, projects, etc.)
- Team members stopped being active
- Feature usage narrowing

**Support signals:**
- Multiple support tickets in short period
- Escalated or angry tickets
- Feature requests with urgency ("we need this or we'll leave")
- Billing questions

**Account signals:**
- Team size decreasing (members removed)
- Payment method expiring
- Failed payment attempts
- Downgrade in plan

### Intervention Playbook

**Signal: Usage dropped 50%+ in 2 weeks**
Action: Personal outreach from you
"Hi [Name], I noticed you've been less active lately. Is everything okay? I'm here if you need help."

**Signal: Multiple support tickets about the same issue**
Action: Prioritize fix + personal apology
"We're aware of the issue and fixing it. Here's a timeline and a credit for the inconvenience."

**Signal: Customer requested features that don't exist**
Action: Honest conversation about roadmap
"I understand you need [feature]. It's not on our near-term roadmap. Here's what I'd recommend: [workaround or alternative]."

**Signal: Failed payment**
Action: Proactive reach-out
"Your payment failed. Let me help you update your billing info so you don't lose access. Here's a direct link: [update billing]."

## Churn Metrics Dashboard

### Essential Churn Metrics

| Metric | Formula | Action if Bad |
|--------|---------|---------------|
| Monthly logo churn | Churned customers / total customers | Improve onboarding |
| Monthly revenue churn | Churned MRR / total MRR | Focus on high-value accounts |
| Net revenue retention | (Starting MRR - Churn + Expansion) / Starting MRR | Increase expansion |
| Churn by segment | Segmented churn rate | Fix worst segment |
| Churn reason distribution | % per reason | Address top reasons |
| Win-back rate | Won-back / churned | Improve win-back campaigns |

### Churn Dashboard Example

```
Churn Dashboard — July 2026

Total customers: 450
New customers: 25
Churned customers: 18 (4% logo churn)
Churned MRR: $1,450 (3.2% revenue churn)
Expansion MRR: $800
Net MRR change: -$650

Churn by segment:
- Enterprise (50): 0 churned (0%)
- Mid-market (150): 3 churned (2%)
- Small team (200): 10 churned (5%)
- Freelancer (50): 5 churned (10%)

Top churn reasons:
1. Too expensive (35%)
2. Missing features (25%)
3. No longer need (20%)

Churn trend (monthly):
- Apr: 5.2%
- May: 4.8%
- Jun: 4.0%
- Jul: 4.0% (stable, improving)
```

### Weekly Churn Review (30 min)

1. Review churn rate vs target
2. Review churned customers list (who churned, why?)
3. Identify any patterns (same segment, same reason, same week)
4. Check if any churn could have been prevented
5. Plan retention actions based on findings

## Common Churn Analysis Mistakes

### Mistake 1: Not Tracking Churn Reasons
Knowing the number of churns without knowing the reasons.
Fix: Always survey or interview churned customers.

### Mistake 2: Averaging Churn Across Segments
Hiding high churn in one segment by averaging with low churn in another.
Fix: Always segment churn analysis.

### Mistake 3: Ignoring Early Churn
First 30 days has highest churn but often gets lumped in with overall.
Fix: Track churn by tenure. Focus on early churn first.

### Mistake 4: Not Distinguishing Voluntary vs Involuntary churn
Payment failures and intentional cancellations need different responses.
Fix: Separate involuntary churn (payment issues) from voluntary.

### Mistake 5: Reacting Instead of Preventing
Only addressing churn after it happens.
Fix: Build early warning systems and intervene before cancellation.

## Conclusion

Churn analysis is not about assigning blame. It's about understanding why customers leave so you can build a business they stay with.

Build your churn analysis system:
1. Track cohort retention (weekly/monthly)
2. Survey every churned customer (within 1 hour)
3. Segment churn by customer type and reason
4. Identify early warning signs
5. Intervene before cancellation
6. Win back those who've left

The best churn rate is the one you don't see because you prevented it. Invest in understanding your churn, and invest in stopping it. Every customer you retain is revenue you don't need to replace.
