# Building Your Solo Founder Analytics Dashboard

A practical guide to setting up a SaaS analytics dashboard that gives you the insights you need without drowning you in data. Focus on what matters, skip the vanity metrics, and build systems that scale with you.

---

## Part 1: The Solo Founder Analytics Philosophy

### Why Most Dashboards Fail

The typical solo founder builds a dashboard that:
1. Has 47 metrics they never look at
2. Tracks things they can't influence
3. Takes 4 hours to set up and 2 hours per week to maintain
4. Gets abandoned after two weeks

This guide takes a different approach: **Minimum Viable Dashboard (MVD).** Track only what you can act on. Add metrics only when you have a specific decision to make.

### The Three-Layer Dashboard Strategy

```
Layer 1: Health Check (Daily, 30 seconds)
- MRR
- New Customers
- Cash Balance

Layer 2: Operations (Weekly, 15 minutes)
- MRR Breakdown (New, Expansion, Churn)
- Trial Conversions
- Usage Metrics (DAU/MAU)
- Support Tickets

Layer 3: Strategy (Monthly, 1 hour)
- Cohort Analysis
- Unit Economics (LTV, CAC, Payback)
- Channel Performance
- Feature Adoption
```

### Dashboard Principles for Solo Founders

1. **One source of truth** — don't have Stripe saying $10K MRR and your sheet saying $9.5K
2. **Push notifications, not pull** — set alerts for anomalies; don't check dashboards obsessively
3. **Actionable > Interesting** — if you can't change it, don't track it
4. **Cohort thinking** — aggregate metrics lie; cohorts tell the truth
5. **Trends over snapshots** — a single month of churn doesn't matter; 3-month trend does

---

## Part 2: The Essential Metrics to Track

### Tier 1: Survival Metrics (Check Daily)

These metrics tell you if your business is alive tomorrow:

| Metric | Why | Alert Threshold |
|--------|-----|-----------------|
| Cash Balance | You need to know if payroll clears | < 3 months runway |
| MRR (today) | Real-time revenue pulse | Drop > 5% in one day |
| Failed Payments | Customers about to churn involuntarily | > 3% of transactions failing |
| New Signups | Demand signal | 0 signups in 48 hours |

### Tier 2: Growth Metrics (Check Weekly)

These tell you if you're moving in the right direction:

| Metric | Formula | Actionable Insight |
|--------|---------|-------------------|
| Net New MRR | New + Expansion - Churn - Contraction | Are we growing or shrinking? |
| MRR Growth Rate | (Net New MRR / Previous MRR) × 100 | Is growth accelerating or decelerating? |
| Trial → Paid Conversion | Trials converted / Total trials × 100 | Is our onboarding working? |
| Churn Rate | Customers lost / Starting customers | Are customers sticking? |
| Revenue per Customer | MRR / Active customers | Is pricing working? |

### Tier 3: Strategic Metrics (Review Monthly)

These tell you if your business model is sustainable:

| Metric | Why It Matters | Good/Bad |
|--------|----------------|----------|
| LTV/CAC Ratio | Are you profitable on each customer? | > 3x is healthy |
| CAC Payback Period | How long to recoup acquisition costs? | < 12 months target |
| Gross Margin | How efficient is delivery? | > 75% target |
| NRR | Are existing customers growing? | > 100% target |
| Cohort Retention Curve | Do later cohorts behave like earlier ones? | Should be stable or improving |

### Metrics to Ignore (Vanity)

| Metric | Why It's Dangerous |
|--------|-------------------|
| Total Registered Users | Includes people who never paid — makes you feel good, not rich |
| Website Traffic | Doesn't convert? Doesn't matter |
| Social Media Followers | Zero correlation with revenue for B2B SaaS |
| Total Downloads | App store downloads ≠ active users |
| Gross Revenue (without normalization) | $50K revenue looks good, but $40K is refunded? Problem. |

---

## Part 3: Tool Comparison

### Paid Analytics Tools

#### ChartMogul

**Best for:** B2B SaaS with subscriptions
**Pricing:** Starts at $119/month (Essential plan)
**MRR threshold:** You should wait until $5K+ MRR to justify

**Key Features:**
- Automated MRR, ARR, LTV, churn calculations
- Cohort analysis built in
- Revenue recognition reports
- CSV import for non-Stripe revenue
- API for custom integrations
- Investor-ready reports

**Pros for Solo Founders:**
- "Set and forget" — connects to Stripe, automatically tracks everything
- Beautiful investor reports with one click
- Cohort analysis that actually makes sense
- Good customer support for questions

**Cons for Solo Founders:**
- Expensive early on ($119/mo = 3-4 customers worth of MRR)
- Overkill before $5K MRR
- Some features locked behind higher tiers
- Learning curve for advanced features

**Setup Process:**
```
1. Sign up for ChartMogul (14-day free trial)
2. Connect Stripe account (OAuth)
3. Import historical data (CSV or API)
4. Configure plan tiers and segmentation rules
5. Set up dashboard widgets for daily review
6. Invite investor access link (if fundraising)
7. Set up email reports (weekly digest)
```

#### Baremetrics

**Best for:** Subs-only SaaS with Stripe (pull-based, action focus)

**Pricing:** Starts at $79/month (Launch plan + 0.39% of revenue capped at $1.8M)
**MRR threshold:** $3K+ MRR

**Key Features:**
- MRR, ARR, LTV, churn tracking
- Customer segmentation
- Recovery (dunning) tool
- Forecast (predictive future MRR)
- Metric benchmarking against other SaaS

**Pros for Solo Founders:**
- Lower starting price than ChartMogul
- Recovery tool reduces churn
- Forecast feature helps with planning
- Benchmarks show you how you compare

**Cons for Solo Founders:**
- Revenue-based pricing can get expensive as you grow
- Less sophisticated cohort analysis
- Fewer integration options
- Reporting less polished for investors

**Setup Process:**
```
1. Sign up at baremetrics.com
2. Connect Stripe (primary) or other payment gateways
3. Set up segmentation (by plan, channel, geography)
4. Configure recovery (dunning) emails
5. Set MRR alert thresholds
6. Review Forecast weekly
```

#### ProfitWell (by Paddle)

**Best for:** Free, comprehensive metrics
**Pricing:** Free (acquired by Paddle, basic tier free)
**MRR threshold:** Any stage

**Key Features:**
- Free MRR, churn, LTV tracking
- Price intelligently (pricing optimization tool)
- Benchmark reports (sourced from 25K+ SaaS companies)
- Subscription retention insights

**Pros for Solo Founders:**
- FREE — can't beat the price
- Good benchmark data for comparisons
- Decent reporting for early-stage
- No commitment required

**Cons for Solo Founders:**
- Acquired by Paddle (potential upsell pressure)
- Less feature-rich than paid alternatives
- Limited customer segmentation
- Data lives on ProfitWell's servers
- Not as actively developed as before acquisition

**Setup Process:**
```
1. Go to profitwell.com (now profitwell.paddle.com)
2. Create account (free)
3. Connect payment processor (Stripe, Braintree, Recurly)
4. Review metrics dashboard
5. Download benchmark reports
6. Set up monthly email report
```

### Free/Build-Your-Own Tools

#### Stripe Analytics (Built-in)

**Best for:** Pre-$5K MRR (free, always available)

**What You Get:**
- Basic MRR graph
- Monthly revenue breakdown
- Customer count
- Payment failure rate
- Subscription lifecycle events

**Limitations:**
- No cohort analysis
- No LTV calculations
- No expansion vs. contraction breakdown
- Can't segment by acquisition channel
- No forecasting

**Setup:**
```
Already built in. Go to Stripe Dashboard → Reports → Subscriptions
```

#### Google Sheets Dashboard

**Best for:** $0-$3K MRR (completely custom, free)

**Template Structure:**

```
Sheet 1: Raw Data (imported from Stripe exports)
Sheet 2: MRR Calculation (pivot tables)
Sheet 3: Cohort Retention (monthly cohorts)
Sheet 4: Unit Economics (LTV, CAC, payback)
Sheet 5: Executive Dashboard (summary)
```

**Pros:**
- Completely free
- Fully customizable
- You understand every formula
- Can import data from Stripe, Google Analytics, email tools

**Cons:**
- Manual data imports (or requires API scripting)
- No real-time updates
- Easy to make formula errors
- Doesn't scale well past 100 customers

**Spreadsheet Template Download:**
```
Available at: [your-saas-resources]/templates/saas-dashboard-template.xlsx
```

#### Building with Google Sheets + Stripe API (Advanced)

For the technical solo founder, you can:
1. Use Google Apps Script to pull Stripe data hourly
2. Automate dashboard refresh
3. Send yourself Slack alerts

```javascript
// Google Apps Script to pull MRR from Stripe
function getStripeMRR() {
  var apiKey = 'sk_live_YOUR_KEY';
  var url = 'https://api.stripe.com/v1/charges?created[gte]=30_days_ago';
  
  var options = {
    'headers': {
      'Authorization': 'Bearer ' + apiKey
    },
    'method': 'GET'
  };
  
  var response = UrlFetchApp.fetch(url, options);
  var data = JSON.parse(response);
  
  // Calculate and write MRR to sheet
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Dashboard');
  sheet.getRange('B2').setValue(calculateMRR(data));
}
```

### Open Source / Self-Hosted

#### PostHog (self-hosted)

**Best for:** Product analytics (not financial metrics)
**Pricing:** Free self-hosted / $0.0003/event cloud
**Use it for:** User behavior, feature adoption, funnel analysis

#### Plausible Analytics

**Best for:** Web analytics (not subscription metrics)
**Pricing:** €9/month
**Use it for:** Traffic analysis, marketing attribution

#### Metabase

**Best for:** Custom dashboards on your own database
**Pricing:** Free (self-hosted) / $85/month (cloud)
**Use it for:** Querying your app database for custom metrics

---

## Part 4: Building Your First Dashboard (Google Sheets)

### Step 1: Set Up Data Sources

Create these sheets in a single workbook:

**Sheet: Stripe_Export**
```
| Date       | Customer ID | Customer Name | Plan     | Amount | Status    | Charge ID       |
|------------|-------------|---------------|----------|--------|-----------|-----------------|
| 2024-01-01 | cus_001     | Acme Inc      | Pro      | $49    | succeeded | ch_001          |
| 2024-01-01 | cus_002     | Beta LLC      | Basic    | $19    | succeeded | ch_002          |
```

Export weekly from Stripe Dashboard → Reports → All transactions → CSV

**Sheet: Customers**
```
| Customer ID | Name       | Plan     | Status     | First Signup | Channel   |
|-------------|------------|----------|------------|--------------|-----------|
| cus_001     | Acme Inc   | Pro      | Active     | 2024-01-01   | Organic   |
| cus_002     | Beta LLC   | Basic    | Canceled   | 2024-01-15   | Google Ad |
```

### Step 2: Build MRR Calculation

**Sheet: MRR_Calc**

```
Cell A1: Month
Cell B1: Basic MRR
Cell C1: Pro MRR
Cell D1: Enterprise MRR
Cell E1: Total MRR
Cell F1: MoM Growth

Row 2: =TEXT(DATE(2024,1,1), "MMM YYYY")  [formula for months]
Row 2, B2: =SUMPRODUCT(...)  [sum of basic plan charges for month]
```

**Formula for monthly total MRR:**
```
=SUMPRODUCT(
  (Stripe_Export!A:A >= DATE(2024, 1, 1)) *
  (Stripe_Export!A:A < DATE(2024, 2, 1)) *
  (Stripe_Export!F:F = "succeeded")
)
```

### Step 3: Build Cohort Retention Table

**Sheet: Cohort_Retention**

```
Cohort Month | Month 0 | Month 1 | Month 2 | Month 3 | Month 4 | Month 5 | Month 6
-------------|---------|---------|---------|---------|---------|---------|--------
Jan 2024     | 100     | 85      | 72      | 65      | 60      | 58      | 55
Feb 2024     | 90      | 78      | 70      | 63      | 59      | 56      |
Mar 2024     | 110     | 92      | 82      | 74      | 68      |         |
```

Each cell = Percentage of customers from that cohort still active in that month.
Month 0 = 100% (signup month).
Month 1 = Customers still active after 1 month.

**Formula for retention percentage:**
```
= COUNTIFS( cohort_start_date_range, cohort_month, active_flag_range, TRUE ) / COUNTIF( cohort_start_date_range, cohort_month )
```

### Step 4: Build Unit Economics Sheet

**Sheet: Unit_Economics**

```
Cell A1: Metric
Cell B1: Value
Cell C1: Formula

Row 2: ARPU        = MRR / Active_Customers
Row 3: Monthly Churn = Churned_Customers / Starting_Customers
Row 4: LTV         = ARPU / Monthly_Churn_Rate
Row 5: CAC         = Total_S&M_Spend / New_Customers
Row 6: LTV/CAC     = LTV / CAC
Row 7: Gross Margin = (Revenue - COGS) / Revenue
Row 8: Payback     = CAC / (ARPU * Gross_Margin)
```

### Step 5: Build the Executive Dashboard

**Sheet: Dashboard**

```
Section 1: Health (Top Row)
| MRR          | ARR           | Cash Balance | Runway     |
| $12,450      | $149,400      | $85,000      | 8.2 months |

Section 2: Growth (Second Row)
| MoM Growth  | New Customers | Churn Rate | NRR        |
| 12.3%       | 18            | 4.1%       | 102%       |

Section 3: Unit Economics (Third Row)
| ARPU   | LTV    | CAC   | LTV/CAC | Payback | Gross Margin |
| $58    | $1,160 | $290  | 4.0x    | 6.2 mo  | 82%          |

Section 4: Trend Chart (Sparklines or embedded chart)
MRR over last 12 months: ▁▃▅▆▇██▇█▇▇█

Section 5: Alerts
| Condition                                 | Current    | Status  |
|-------------------------------------------|------------|---------|
| Cash > 12 months runway                   | 8.2 months | ⚠️      |
| MRR growth > 10% MoM                      | 12.3%      | ✅      |
| Churn < 5% monthly                        | 4.1%       | ✅      |
| LTV/CAC > 3x                              | 4.0x       | ✅      |
| Gross Margin > 75%                        | 82%        | ✅      |
```

---

## Part 5: Dashboard Templates

### Template 1: The Solo Survival Dashboard (Pre-$5K MRR)

**Frequency:** Weekly review, 10 minutes

```
┌────────────────────────────────────────────────────────┐
│                    SOLO SURVIVAL DASHBOARD              │
├────────────────────────────────────────────────────────┤
│                                                        │
│  CASH BALANCE: $12,400    RUNWAY: 14 months            │
│  MRR: $2,850              GROWTH: +18% MoM             │
│  CUSTOMERS: 52            CHURN: 7.2%                  │
│                                                        │
│  ─── ALERTS ───                                        │
│  ✅ Cash runway > 12 months                            │
│  ✅ MRR growing > 15% MoM                              │
│  ⚠️ Churn above 5% threshold                           │
│  ✅ New customers this week: 4                         │
│                                                        │
│  ─── THIS WEEK'S FOCUS ───                             │
│  □ Improve onboarding flow                             │
│  □ Reach out to 3 churned customers                    │
│  □ Write 1 blog post for SEO                           │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Template 2: The Growth Dashboard ($5K-$50K MRR)

**Frequency:** Weekly review, 30 minutes

```
┌──────────────────────────────────────────────────────────────┐
│                    GROWTH DASHBOARD                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  MRR: $18,420        GROWTH: +15% MoM    RUNWAY: 11 months  │
│  ARR: $221,040       CHURN: 4.1%         NRR: 105%          │
│                                                              │
│  MRR BREAKDOWN:                                              │
│  ┌──────────────┬────────┬────────┬────────┬──────────┐     │
│  │              │  New   │Expansion│ Churn  │Contraction│     │
│  ├──────────────┼────────┼────────┼────────┼──────────┤     │
│  │ This Month   │ +$3,200│ +$1,100 │ -$760  │ -$380    │     │
│  │ Last Month   │ +$2,800│ +$900   │ -$620  │ -$310    │     │
│  │ Trend        │   ▲     │   ▲     │   ▲    │   ▲      │     │
│  └──────────────┴────────┴────────┴────────┴──────────┘     │
│                                                              │
│  COHORT RETENTION (focused on last 3 months):               │
│  Feb: Month 0: 100% → Month 1: 82% → Month 2: 74%          │
│  Mar: Month 0: 100% → Month 1: 85% → Month 2: 78%          │
│  Apr: Month 0: 100% → Month 1: 88% ✔️ improving             │
│                                                              │
│  UNIT ECONOMICS:                                            │
│  ARPU: $58/mo   LTV: $1,160   CAC: $290   LTV/CAC: 4.0x    │
│  CAC Payback: 6.2 months   Gross Margin: 82%               │
│                                                              │
│  CHANNEL PERFORMANCE:                                       │
│  Organic: 12 customers, CAC: $45    ← DOUBLE DOWN           │
│  Google Ads: 8 customers, CAC: $185 → OPTIMIZE              │
│  Referrals: 4 customers, CAC: $12   ← INVEST MORE           │
│  Twitter/X: 2 customers, CAC: $92   → MAINTAIN              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Template 3: The Investor Dashboard (Fundraising)

**Frequency:** Generated monthly for investor updates

```
┌──────────────────────────────────────────────────────────────┐
│                    INVESTOR DASHBOARD                         │
│                    Prepared For: [Investor Name]              │
│                    Date: [Month] 2024                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  COMPANY AT A GLANCE                                         │
│  ──────────────────                                           │
│  Founded: Jan 2024    Stage: Seed    Team: Solo              │
│  MRR: $24,500        ARR: $294,000                           │
│  Total Customers: 385     YoY Growth: 340%                   │
│                                                              │
│  REVENUE GROWTH (12 months):                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │    │
│  │  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░███      │    │
│  │  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░███████████       │    │
│  │  ░░░░░░░░░░░░░░░░░░░░███████████████████████       │    │
│  │  ░░░░░░░░███████████████████████████████████       │    │
│  │  ░████████████████████████████████████████████      │    │
│  │  ████████████████████████████████████████████████   │    │
│  │  ───────────────────────────────────────────────    │    │
│  │  J F M A M J J A S O N D                          │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  KEY METRICS:                                                │
│  MRR Growth: 15% MoM (12% median for seed stage)            │
│  Churn: 3.8% monthly (5.8% median)                          │
│  LTV/CAC: 4.5x (3.0x median)                                 │
│  NRR: 108% (100% median)                                     │
│  Gross Margin: 84% (75% median)                              │
│  CAC Payback: 5.5 months (12 months median)                  │
│                                                              │
│  NOTABLE:                                                    │
│  - [Month] set record for new MRR ($5,200)                   │
│  - Enterprise launch planned for next quarter                │
│  - Current runway: 10 months                                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Part 6: Automation and Alerts

### Setting up Free Alerts

#### Stripe Webhook → Slack

Create a Slack webhook and Stripe webhook to alert you on:

```javascript
// Stripe webhook endpoint (Vercel Edge Function)
export async function POST(req) {
  const event = await req.json();
  
  if (event.type === 'charge.failed') {
    await fetch(process.env.SLACK_WEBHOOK_URL, {
      method: 'POST',
      body: JSON.stringify({
        text: `⚠️ Payment Failed: ${event.data.object.billing_details.name} - $${event.data.object.amount / 100}`,
        channel: '#alerts'
      })
    });
  }
  
  if (event.type === 'customer.subscription.deleted') {
    await fetch(process.env.SLACK_WEBHOOK_URL, {
      method: 'POST',
      body: JSON.stringify({
        text: `❌ Churn Alert: ${event.data.object.customer} canceled ${event.data.object.items.data[0].price.nickname}`,
        channel: '#alerts'
      })
    });
  }
  
  if (event.type === 'invoice.paid' && event.data.object.amount_due > 50000) {
    // Alert on large invoices (enterprise expansion)
    await fetch(process.env.SLACK_WEBHOOK_URL, {
      method: 'POST',
      body: JSON.stringify({
        text: `💰 Large Invoice Paid: $${event.data.object.amount_due / 100}`,
        channel: '#wins'
      })
    });
  }
}
```

#### Google Sheets → Email

Use Apps Script to send a weekly email:
```javascript
function sendWeeklyDashboard() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Dashboard');
  var mrr = sheet.getRange('B2').getValue();
  var churn = sheet.getRange('B5').getValue();
  
  var subject = `Weekly Dashboard: MRR $${mrr} | Churn ${churn}%`;
  var body = `MRR: $${mrr}\nChurn: ${churn}%\n... (add more)`;
  
  MailApp.sendEmail('you@example.com', subject, body);
}
```

#### Zapier / Make.com (No-Code Automation)

Set up Zaps:
1. New Stripe customer → Slack #wins
2. Failed payment → Slack #alerts
3. Weekly MRR summary → Email
4. Churn event → Add to CRM follow-up list

---

## Part 7: Dashboard Maintenance Cadence

### Weekly Routine (15 minutes every Monday)

```
1. Update Stripe export (if manual sheet) — 2 min
2. Refresh MRR calculation — 1 min
3. Record churn events from last week — 3 min
4. Check for anomalies (churn spike, payment failures) — 3 min
5. Update "This Week's Focus" section — 3 min
6. Set 3 priorities based on data — 3 min
```

### Monthly Routine (1 hour first week of month)

```
1. Run cohort retention analysis — 10 min
2. Calculate full unit economics (LTV, CAC, payback) — 10 min
3. Review channel performance — 10 min
4. Update financial projections — 10 min
5. Review feature adoption — 10 min
6. Plan next month's experiments — 10 min
```

### Quarterly Routine (2 hours)

```
1. Full strategic review — 30 min
2. NPS survey and analysis — 20 min
3. Product roadmap alignment with metrics — 30 min
4. Budget reforecasting — 20 min
5. Fundraising readiness assessment — 20 min
```

---

## Part 8: Common Mistakes and Fixes

### Mistake 1: Measuring Everything

**The problem:** You have 47 metrics and no idea which to act on.

**The fix:** Your dashboard should have exactly ONE metric you're optimizing this month. Everything else is context.

### Mistake 2: Vanity Metrics

**The problem:** You celebrate 1,000 signups when only 3 converted to paid.

**The fix:** Each metric on your dashboard must tie to revenue. If it doesn't, remove it.

### Mistake 3: Lagging Only

**The problem:** You only track revenue (lagging) and never track usage (leading).

**The fix:** For every lagging metric, identify at least one leading metric:
- Lagging: Churn → Leading: Usage decline
- Lagging: MRR growth → Leading: Trial starts
- Lagging: LTV → Leading: Activation rate

### Mistake 4: Ignoring Cohort Effects

**The problem:** Overall churn looks fine (5%), but early customers have 3% churn and new ones have 9%.

**The fix:** Always segment by cohort. Always.

### Mistake 5: Over-Automation

**The problem:** You spend 10 hours building an automated dashboard that saves you 5 minutes per week.

**The fix:** Use manual processes until they hurt. At $3K MRR, a Google Sheet is fine. At $30K MRR, upgrade to ChartMogul.

---

## Part 9: The Solo Founder's First 90 Days of Analytics

### Week 1-2: Baseline Setup
```
Day 1: Export Stripe data to Google Sheets
Day 3: Build MRR tracking (with breakdowns)
Day 5: Set up customer list with cohorts
Day 7: Build basic dashboard (Health + Growth sections)
Day 10: Set up one alert (payment failures)
Day 14: Share dashboard with one advisor for feedback
```

### Week 3-4: Add Actionability
```
Day 15: Add churn tracking with cancellation reasons
Day 18: Set up trial conversion tracking
Day 21: Build unit economics (LTV, CAC)
Day 25: Add leading indicators (activation, usage)
Day 28: First full monthly review
```

### Week 5-8: Automate
```
Week 5: Set up weekly email report
Week 6: Add Slack alerts (churn, large payments)
Week 7: Automate data import (Apps Script or Zapier)
Week 8: Build cohort analysis table
```

### Week 9-12: Strategic
```
Week 9: Run first full cohort analysis
Week 10: Build investor dashboard (even if not fundraising)
Week 11: Set up NPS survey
Week 12: First quarterly strategic review
```

---

## Part 10: Recommended Tool Progression

### Stage 1: Pre-Revenue to $3K MRR

**Tools:** Stripe Dashboard + Google Sheets + Plausible (free)

**Cost:** $0/month
**Time investment:** 15 min/week

### Stage 2: $3K to $10K MRR

**Tools:** ProfitWell (free) + Google Sheets + PostHog (self-hosted)

**Cost:** $0-10/month
**Time investment:** 30 min/week

### Stage 3: $10K to $50K MRR

**Tools:** ChartMogul ($119/mo) + PostHog (cloud) + Google Sheets (supplemental)

**Cost:** ~$150/month
**Time investment:** 1 hour/week

### Stage 4: $50K+ MRR

**Tools:** ChartMogul + Amplitude/Mixpanel + Metabase + Financial modeling tool

**Cost:** $500+/month
**Time investment:** 2 hours/week (you can hire for this now)

---

## Quick Start: What to Do Today

1. **Log into Stripe** and export your transaction history
2. **Create a new Google Sheet** with tabs: Dashboard, MRR, Cohorts, Unit Economics
3. **Copy MRR formula** from this guide into your sheet
4. **Set a 30-minute calendar reminder** every Monday for dashboard review
5. **Set up one alert** — payment failures notification to your phone
6. **Share your dashboard** with one fellow founder or mentor for accountability

Your dashboard doesn't need to be perfect. It needs to exist, be reviewed consistently, and drive one action per week.