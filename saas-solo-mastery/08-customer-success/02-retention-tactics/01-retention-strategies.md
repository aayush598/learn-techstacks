# Retention Strategies

## Why Retention Matters More Than Acquisition

Acquiring a customer costs 5-7x more than retaining one. For a solo founder, this ratio is even more extreme because your acquisition channels are limited while your ability to deliver personal attention is high.

**The retention math:**
- If you have 100 customers at $100/mo and 5% monthly churn, you lose 5 customers ($500 MRR) per month
- Reducing churn to 3% saves $200 MRR per month — equivalent to acquiring 2 new customers
- Over 12 months, that 2% improvement saves $2,400 in lost revenue

**The compounding effect:**
- 5% monthly churn: After 12 months, you retain 54% of customers
- 3% monthly churn: After 12 months, you retain 69% of customers
- 1% monthly churn: After 12 months, you retain 89% of customers

Investing in retention has a higher ROI than almost any other growth investment.

## The Retention Framework

### The Three Pillars of Retention

**1. Product stickiness:** The product becomes essential to their workflow
**2. Customer success:** They achieve their desired outcomes
**3. Relationship:** They feel valued and connected to you

### The Retention Flywheel

```
Customer achieves success → They use product more → Product becomes essential → They renew → They expand → They refer → Customer achieves more success
```

### Retention vs Engagement

Don't confuse the two. A user can be engaged (logging in daily) but not retained (they cancel because they don't see ROI). Retention is about value realization, not usage frequency.

## Engagement Scoring

### What Is Engagement Scoring?

A numerical score that measures how actively and deeply a customer uses your product. Higher scores predict higher retention.

### Building an Engagement Score

**Step 1: Identify key actions**
Which product actions correlate with retention?

Common examples:
- Logging in (frequency and recency)
- Creating content/projects
- Inviting team members
- Using integrations
- Completing core workflow
- Exporting data

**Step 2: Weight each action**
Some actions are stronger retention predictors than others.

Example weights:
- Login in last 7 days: 5 points
- Created a project in last 30 days: 10 points
- Invited a team member: 15 points
- Completed core workflow: 20 points
- Connected integration: 10 points
- Exported data: 5 points
- Submitted support ticket: -5 points (negative engagement)

**Step 3: Set thresholds**
- 0-20: Low engagement (at risk)
- 21-50: Medium engagement (needs attention)
- 51-80: High engagement (good)
- 81+: Power user (excellent)

### Engagement Score Examples

**SaaS analytics tool:**
- Created dashboard: 15 pts
- Invited team: 20 pts
- Set up integration: 15 pts
- Viewed reports weekly: 10 pts
- Shared report: 10 pts
- Exported data: 5 pts

**Thresholds:** 0-25 = At risk, 26-55 = Engaged, 56-75 = High, 76+ = Power

### Tracking Engagement

**Tools:**
- PostHog (free, open-source)
- Mixpanel/Amplitude (paid)
- Your own database (custom query)

**Dashboard:**
```
Engagement Distribution:
- Power users (81+): 25 customers
- High (51-80): 40 customers
- Medium (21-50): 30 customers
- Low (0-20): 15 customers

Engagement Trend (over 90 days):
- Power users: +5%
- High: Flat
- Medium: -3%
- Low: +2% (ALERT — at-risk segment growing)
```

## Health Monitoring

### What Is Customer Health?

A composite metric that predicts the likelihood of retention or churn. Combines engagement, support interactions, usage trends, and relationship signals.

### Health Score Components

**Usage health (40% weight):**
- Days since last login
- Session frequency trend (increasing/decreasing)
- Feature adoption breadth
- Core workflow completion rate

**Support health (25% weight):**
- Open support tickets
- CSAT score trend
- Time since last ticket
- Ticket sentiment (positive/negative language)

**Business health (20% weight):**
- Payment status
- Contract remaining time
- Account changes (team size, plan changes)
- Billing history

**Relationship health (15% weight):**
- NPS score
- Referral activity
- Community participation
- Email engagement (opens, replies)

### Health Score Calculation

Simple formula to start:
```
Health = (Usage × 0.4) + (Support × 0.25) + (Business × 0.2) + (Relationship × 0.15)
```

Each component normalized to 0-100.

**Segments:**
- Green (80-100): Healthy — minimal intervention needed
- Yellow (50-79): Warning — needs attention
- Red (0-49): At risk — immediate intervention required

### Monitoring At-Risk Customers

**Weekly review (15 min):**
1. Sort customers by health score (ascending)
2. Review bottom 10%
3. Identify patterns — are they all showing the same behavior?
4. Reach out to 3-5 at-risk customers personally

**Triggered alerts:**
- Login frequency dropped 50%+ (weekly → monthly)
- No login in 14 days
- Open support ticket older than 5 days
- Negative CSAT score
- Payment declined
- Team size decreased

## Proactive Outreach

### The Outreach Cadence

**High-value customers ($1,000+/year):**
- Monthly check-in email
- Quarterly business review call
- Personal note from you on milestones

**Mid-value customers ($200-$1,000/year):**
- Quarterly check-in email
- Semi-annual call
- Automated health-based triggers

**Low-value customers (< $200/year):**
- Automated engagement emails
- In-app messages based on behavior
- Self-serve resources

### Outreach Templates

**Re-engagement (inactive 7+ days):**
"Hi [Name], I noticed you haven't been on [Product] in a bit. Is everything okay? I'm here if you need help with anything. Here's something new since you last visited: [feature update]."

**Post-positive-interaction (after good support):**
"Thanks for the kind words! I'm really glad we could help. By the way, I wanted to share [feature/tip] that might help you get even more out of [Product]."

**Milestone celebration:**
"Congrats on [milestone]! That's [X] reports/projects/tasks with [Product]. You're in the top [Y]% of our users. Here's a pro tip for the next level: [tip]."

**Health-triggered outreach (at-risk):**
"Hi [Name], I noticed things have been quiet with [Product] lately. I wanted to check in and see if there's anything I can help with. Sometimes a fresh workflow or a new feature can make all the difference. Want to hop on a 10-minute call?"

### The Personal Touch (Your Superpower)

As a solo founder, you can send personal outreach that no automated system can match.

**Personal outreach ideas:**
- Send a birthday card (physical or digital)
- Congratulate them on company milestones
- Comment on their LinkedIn posts
- Remember details from previous conversations
- Send a handwritten thank-you note for renewals

These cost minutes but build loyalty that lasts years.

## Value Reinforcement

### Continuous Value Demonstration

Don't assume customers remember why they signed up. Remind them.

**Techniques:**

**Weekly/monthly digest:**
"Your [Product] weekly recap: You saved 3 hours, completed 12 tasks, and your team sent 8 messages. [Link to dashboard]"

**ROI reminders:**
"Since joining [Product], your team has [action] [X] times. If each takes [Y] minutes, you've saved [Z] hours total."

**Feature discovery:**
"Did you know you can [feature]? Our power users love it for [use case]. Try it out: [link]"

**Success stories:**
"Here's how [Customer] used [Product] to achieve [result]. Could this work for you?"

### The Value Resurvey

Quarterly, ask customers:
1. What outcome are you trying to achieve with [Product]?
2. On a scale of 1-10, how close are you to achieving it?
3. What's blocking you?

Then help them close the gap.

## Annual Planning and Renewals

### The Renewal Timeline

**90 days before renewal:**
- Start measuring engagement more closely
- Begin value reinforcement sequence
- Identify any issues that need resolution

**60 days before renewal:**
- Send renewal reminder with value summary
- Offer to review usage and provide recommendations
- Check in on any open support issues

**30 days before renewal:**
- Send proposal with renewal terms
- Offer annual discount
- Address any concerns

**7 days before renewal:**
- Final reminder
- Ensure billing info is current
- Send direct message from you

**Renewal day:**
- Process payment
- Send thank-you note
- Celebrate the milestone

### Handling Non-Renewals

If they don't renew:
1. Thank them for their time
2. Ask for honest feedback
3. Offer to help with data export
4. Leave the door open for return
5. Add to re-engagement sequence (90-day follow-up)

## Building Retention into the Product

### Default Paths to Retention

**Default engagement:**
"Your team was mentioned in a project — [view update]"

**Default sharing:**
"Your weekly report is ready — [view and share]"

**Default check-in:**
"Don't forget to check your dashboard for this week's insights"

**Default renewal:**
"Your subscription is up for renewal — here's what you've accomplished"

### Retention Features

- **Scheduled reports:** Regular email with key metrics
- **Team activity feed:** Shows what others are doing
- **Goal tracking:** Set and track progress toward goals
- **Usage insights:** "You're in the top X% of users"
- **Achievement badges:** Gamify milestone completion
- **Data export:** Make leaving easy (reduces fear of lock-in)

## Retention Metrics

### Key Retention Metrics

**Logo retention (account-level):**
- Gross retention: % of customers retained (excluding expansion)
- Net retention: Revenue retained including expansion ( > 100% is ideal)

**Revenue retention:**
- Gross MRR churn: MRR lost to churn / beginning MRR
- Net MRR churn: (MRR lost - MRR from expansion) / beginning MRR

**Cohort retention:**
- Retention rate by signup cohort (weekly/monthly)
- Shows if newer customers retain better

**Milestone retention:**
- % of customers who reach day 30, 90, 180, 365

### Benchmarks (B2B SaaS)

| Metric | Median | Top Quartile |
|--------|--------|--------------|
| Monthly logo churn | 5-7% | < 3% |
| Annual logo churn | 30-50% | < 20% |
| Net MRR retention | 80-100% | 120%+ |
| 12-month retention | 50-70% | 80%+ |

## The Retention Stack

### Tools for Solo Founders

**Engagement tracking:**
- PostHog (free, open-source)
- Amplitude/Mixpanel (paid, powerful)

**Health monitoring:**
- Custify (retention-focused)
- Churned (churn analysis)
- Baremetrics (revenue + churn analytics)

**Outreach:**
- Intercom (in-app + email)
- Customer.io (behavioral email)
- HubSpot (CRM + email)

**Survey/feedback:**
- Delighted (NPS + CSAT)
- Typeform (feedback forms)

### Building Your Own Health System

Simple Google Sheets approach:
1. Export user activity weekly
2. Calculate engagement score
3. Highlight red/yellow/green
4. Plan outreach

You don't need expensive tools to start. A spreadsheet and 30 minutes per week can prevent most churn.

## Conclusion

Customer retention is the highest-leverage growth activity for solo founders. Every customer you keep is revenue you don't need to replace.

Build your retention system around:
1. **Monitor:** Track engagement and health scores
2. **Engage:** Proactive outreach based on signals
3. **Reinforce:** Continuously demonstrate value
4. **Improve:** Use churn data to make your product stickier

Invest 30 minutes per week in retention activities. It will pay back more than any other use of that time.
