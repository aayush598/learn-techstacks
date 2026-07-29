# SaaS Metrics Glossary

A comprehensive reference for every SaaS metric a solo founder needs to track, understand, and act upon. This glossary covers definitions, formulas, benchmarks, and common pitfalls for each metric.

---

## 1. Monthly Recurring Revenue (MRR)

### Definition
MRR is the normalized, predictable revenue your SaaS generates each month from subscriptions. It excludes one-time fees, setup fees, and non-recurring revenue streams.

### Formula

```
MRR = Total Number of Paying Customers × Average Revenue Per Account (ARPA)
```

More precisely:
```
MRR = Sum of all monthly subscription fees across all customers
```

For annual plans, divide the total contract value by 12 to get the monthly equivalent.

### Calculation Methods

**Simple MRR (flat-rate pricing):**
- If every customer pays $29/month: MRR = Number of Customers × $29

**Tiered MRR (multiple plan tiers):**
- MRR = (Customers on Basic × $19) + (Customers on Pro × $49) + (Customers on Enterprise × $99)

**Per-seat MRR (usage-based):**
- MRR = Sum of (Seats × Per-seat Price) for each account

### Components of MRR

| Component | Definition | Impact |
|-----------|------------|--------|
| New MRR | Revenue from newly acquired customers | Growth |
| Expansion MRR | Revenue from upsells, cross-sells, upgrades | Growth |
| Churn MRR | Revenue lost from cancellations | Attrition |
| Contraction MRR | Revenue lost from downgrades | Attrition |
| Reactivation MRR | Revenue from returning customers | Recovery |
| Net New MRR | New MRR + Expansion MRR - Churn MRR - Contraction MRR | Overall |

### Benchmarks for Solo Founders

- **Seed stage (< $5K MRR):** Focus on getting to $1K MRR as first milestone
- **Early stage ($5K - $20K MRR):** Aim for 15-20% MoM growth
- **Growth stage ($20K - $100K MRR):** 10-15% MoM growth is healthy
- **Scale stage ($100K+ MRR):** 5-10% MoM growth is solid
- **Warning sign:** Growth below 5% MoM at any stage requires investigation

### Excel/Sheets Formula

```
=SUMIFS(Revenue_Data!D:D, Revenue_Data!B:B, ">=2024-01-01", Revenue_Data!B:B, "<2024-02-01", Revenue_Data!C:C, "Monthly")
```

### Common Pitfalls

- **Counting annual prepayments as lump sum:** Always normalize to monthly
- **Including non-recurring revenue:** Exclude setup fees, professional services
- **Double-counting multi-month subscriptions:** Ensure each subscription is counted once per month
- **Ignoring discounts and coupons:** Track at net revenue, not gross

### Action Items for Solo Founder

1. Set up automated MRR tracking in your payment processor
2. Build a spreadsheet that breaks MRR into its five components
3. Review MRR weekly during the first year, monthly after $10K MRR
4. Set up alerts for MRR drops exceeding 5% in a single day

---

## 2. Annual Recurring Revenue (ARR)

### Definition
ARR is the annualized version of MRR, representing the predictable revenue your SaaS generates in a year. It is the standard metric for B2B SaaS companies.

### Formula

```
ARR = MRR × 12
```

Alternatively:
```
ARR = Sum of all Annual Contract Values (ACV)
```

### When to Use ARR vs. MRR

- **Use ARR when:** Your ACV > $1,000, primarily annual billing, B2B enterprise focused
- **Use MRR when:** Your ACV < $1,000, primarily monthly billing, B2C or SMB focused
- **Solo founder heuristic:** Track both. ARR impresses investors; MRR tells you if you'll survive the month

### Benchmarks for Solo Founders

- **$1K MRR = $12K ARR:** Survival mode
- **$10K MRR = $120K ARR:** Ramen profitable (solo in US)
- **$25K MRR = $300K ARR:** Sustainable solo income
- **$50K MRR = $600K ARR:** Can hire first employee
- **$100K MRR = $1.2M ARR:** Attractively fundable

### Converting Multi-Year Contracts to ARR

```
ARR = Total Contract Value / Contract Duration (years)
```

Example: A $60,000 3-year contract = $20,000 ARR (not $60,000 ARR)

### Pitfall: The "ARR Inflation" Trap
Some founders inflate ARR by including professional services, one-time fees, or non-recurring elements. Investors will strip these out. Be conservative and transparent.

---

## 3. Average Revenue Per User (ARPU)

### Definition
ARPU measures the average revenue generated per user or per account over a specific period. It helps you understand your pricing efficiency and customer value.

### Formula

```
ARPU = MRR / Total Number of Customers
```

### Variations

| Variation | Formula | Use Case |
|-----------|---------|----------|
| ARPU (per user) | MRR / Total Active Users | Multi-seat, per-user pricing |
| ARPA (per account) | MRR / Total Accounts | Account-level billing |
| Blended ARPU | (Total Revenue) / (Total Users) | Companies with mixed pricing |

### Benchmarks

- **Low ARPU (< $10/mo):** Consumer SaaS, high volume needed
- **Mid ARPU ($10 - $100/mo):** SMB SaaS, standard range
- **High ARPU ($100 - $1,000/mo):** Professional SaaS, requires strong sales
- **Premium ARPU ($1,000+/mo):** Enterprise SaaS, long sales cycles

### Excel/Sheets Formula

```
=SUM(Revenue_Data!D:D) / COUNTA(Customer_Data!A:A)
```

### Action Items for Solo Founder

1. Track ARPU by plan tier to see upgrade patterns
2. Monitor ARPU trends monthly — declining ARPU means you're acquiring lower-value customers
3. Experiment with pricing tiers to increase ARPU by 20-30%
4. Segment ARPU by acquisition channel to understand which channels bring higher-value customers

---

## 4. Customer Lifetime Value (LTV or CLV)

### Definition
LTV predicts the total revenue a customer will generate throughout their entire relationship with your SaaS. It is one of the two pillars of unit economics (alongside CAC).

### Formula

```
LTV = ARPU × Gross Margin × Average Customer Lifetime (months)
```

Or more simply:
```
LTV = ARPU / Monthly Churn Rate
```

### Detailed Calculation

```
LTV = ARPU × (1 / Monthly Churn Rate) × Gross Margin Percentage
```

### Example

If ARPU = $50/month, Monthly Churn = 5%, Gross Margin = 80%:
```
LTV = $50 × (1 / 0.05) × 0.80 = $50 × 20 × 0.80 = $800
```

### LTV by Churn Rate

| Monthly Churn | Annual Churn | Avg Lifetime | LTV at $50 ARPU, 80% GM |
|---------------|--------------|--------------|------------------------|
| 1% | 11.4% | 100 months | $4,000 |
| 2% | 21.5% | 50 months | $2,000 |
| 3% | 30.6% | 33 months | $1,320 |
| 5% | 46.0% | 20 months | $800 |
| 8% | 63.2% | 12.5 months | $500 |
| 10% | 71.8% | 10 months | $400 |

### LTV Benchmarks

- **Minimum healthy:** LTV > 3x CAC
- **Target for solo founder:** LTV > 5x CAC (you can't afford mistakes)
- **Excellent:** LTV > 10x CAC
- **Warning zone:** LTV < 2x CAC (you're losing money on every customer)

### Cohort-Based LTV (More Accurate)

Don't calculate LTV from aggregate data. Use cohort analysis:

```
Cohort LTV = Sum of (Monthly Revenue from Cohort / Number of Customers in Cohort) for months 1 to N
```

This accounts for the fact that churn rates change over time (typically improving for older cohorts).

### Excel/Sheets Formula for Cohort LTV

```
=AVERAGEIFS(Revenue_Data!E:E, Revenue_Data!A:A, Cohort_Month, Revenue_Data!B:B, Month_Number)
```

### Action Items

1. Calculate LTV by acquisition channel (organic vs paid vs referral)
2. Set up cohort-based LTV tracking from month 1 of your business
3. Aim to improve LTV by reducing churn before increasing prices
4. Use LTV to determine your maximum allowable CAC

---

## 5. Customer Acquisition Cost (CAC)

### Definition
CAC is the total cost of acquiring a new customer, including all marketing, sales, and related expenses.

### Formula

```
CAC = Total Sales & Marketing Expenses / Number of New Customers Acquired
```

### Detailed Breakdown

```
CAC = (Marketing Spend + Sales Salaries + Sales Tools + Content Creation + Advertising + Commissions) / New Customers
```

### CAC Components

| Category | Examples | Solo Founder Consideration |
|----------|----------|---------------------------|
| Paid Acquisition | Google Ads, Facebook Ads, LinkedIn Ads | Track CAC by channel |
| Content Marketing | Blog posts, SEO, videos | Amortize over content lifespan (6-12 months) |
| Sales Costs | CRM, demo tools, outreach | Often minimal for solo founders |
| Referral Costs | Referral program fees, affiliate commissions | Often lower CAC than paid |
| Time Cost | Your founder time spent on sales | Assign an hourly rate |

### CAC Benchmarks

- **Self-serve ($0 sales cost):** $0 - $50 CAC (ideal for solo founders)
- **Low-touch ($100 - $1,000 ACV):** $50 - $500 CAC
- **Mid-touch ($1K - $10K ACV):** $500 - $5,000 CAC
- **High-touch ($10K+ ACV):** $5,000 - $50,000+ CAC

### CAC Payback Period

```
CAC Payback Period (months) = CAC / (ARPU × Gross Margin)
```

**Benchmarks:**
- < 6 months: Excellent
- 6-12 months: Good for SMB SaaS
- 12-18 months: Acceptable for enterprise
- > 18 months: Problematic — you need to reduce CAC or raise prices

### Blended vs. Blended CAC

| Type | Formula | Purpose |
|------|---------|---------|
| Blended CAC | Total S&M / All new customers | Overall efficiency |
| Paid CAC | Total paid ad spend / Customers from paid | Channel ROI |
| Organic CAC | Content costs / Customers from organic | Content ROI |
| Fully Loaded CAC | All S&M costs (incl. salaries, tools) | True cost |

### Excel/Sheets Formula

```
=SUMIFS(Expenses!C:C, Expenses!A:A, "Sales & Marketing", Expenses!B:B, ">="&Start_Date, Expenses!B:B, "<="&End_Date) / COUNTIFS(Customers!C:C, ">="&Start_Date, Customers!C:C, "<="&End_Date)
```

### Action Items for Solo Founder

1. Know your CAC within two decimal places for each channel
2. If CAC > 3 months of ARPU, your unit economics are broken
3. Focus on organic/referral channels first — they have the lowest CAC
4. Setup a CAC dashboard that automatically pulls from Stripe and ad platforms

---

## 6. Churn Rate

### Definition
Churn rate measures the percentage of customers who stop paying for your SaaS over a given period. It is the single most important metric for SaaS survival.

### Formula

```
Monthly Customer Churn = Customers Lost in Month / Customers at Start of Month
```

```
Monthly Revenue Churn = MRR Lost to Churn / MRR at Start of Month
```

### Types of Churn

| Type | What It Measures | Why It Matters |
|------|-----------------|----------------|
| Customer Churn | % of customers who leave | Volume impact on growth |
| Revenue Churn | % of MRR lost | Financial impact (not all customers pay the same) |
| Voluntary Churn | Customers who actively cancel | Product/market fit signal |
| Involuntary Churn | Payment failures, expired cards | Operational issue |

### The Churn Math Reality

Here's why churn is so critical for solo founders:

```
To grow, you need: Net New MRR = New MRR + Expansion MRR - Churn MRR > 0
```

If your monthly churn is 5% and you're not growing your customer base:
- After 1 year: You'll have 54% of original customers
- After 2 years: You'll have 29%
- After 3 years: You'll have 16%

### Zero Churn Is Not the Goal

A 0% churn rate is actually a warning sign — it usually means:
- You're not charging enough
- You're not attracting enough customers (too selective)
- Your definition of churn is wrong (including free users?)

### Benchmarks

| SaaS Type | Good Monthly Churn | Good Annual Churn |
|-----------|-------------------|-------------------|
| Consumer/SMB self-serve | < 5% monthly | < 46% annual |
| SMB with touch | < 3% monthly | < 31% annual |
| Mid-market | < 2% monthly | < 22% annual |
| Enterprise | < 1% monthly | < 11% annual |
| **Solo founder target** | **< 3% monthly** | **< 31% annual** |

### Churn Rate by Company Stage

| Stage | Median Monthly Churn | What to Focus On |
|-------|---------------------|------------------|
| Pre-PMF (< $5K MRR) | 8-15% | Finding PMF — some churn is expected |
| Early PMF ($5K - $20K MRR) | 5-8% | Reduce churn through onboarding |
| Growth ($20K - $100K MRR) | 3-5% | Systematic retention programs |
| Scale ($100K+ MRR) | 1-3% | Enterprise retention strategies |

### Excel/Sheets Formula

```
=COUNTIFS(Churn_Log!A:A, ">="&Month_Start, Churn_Log!A:A, "<="&Month_End) / COUNTA(Customers!A:A) * 100
```

### Reducing Churn: Prioritized Actions for Solo Founders

1. **Fix onboarding (highest impact):** Most churn happens in the first 30 days
2. **Improve first value time:** Reduce the time from signup to "aha moment"
3. **Identify at-risk customers:** Track usage decline, support tickets, feature adoption
4. **Implement win-back campaigns:** Lost customers are your best source of learning
5. **Analyze cancellation reasons:** Use a cancellation survey (exit interview)
6. **Reduce involuntary churn:** Implement smart dunning (retry logic, email reminders)

### Spreadsheet Template: Churn Tracking

```
Month    | Start Customers | New | Lost | End Customers | Churn %
---------|----------------|-----|------|---------------|--------
Jan 2024 | 100            | 20  | 8    | 112           | 8.0%
Feb 2024 | 112            | 22  | 7    | 127           | 6.3%
Mar 2024 | 127            | 25  | 6    | 146           | 4.7%
```

---

## 7. Net Revenue Retention (NRR)

### Definition
NRR measures the revenue retained from existing customers, accounting for upgrades, downgrades, and churn. It is the most important growth metric for SaaS companies because it shows whether your existing customer base is growing or shrinking.

### Formula

```
NRR = (Beginning MRR - Churn MRR - Contraction MRR + Expansion MRR) / Beginning MRR
```

### Simplified

```
NRR = 1 - (Revenue Churn Rate) + (Expansion Revenue Rate)
```

### What NRR Tells You

| NRR Value | Meaning | Implication |
|-----------|---------|-------------|
| > 120% | World-class | Your existing customers grow 20%+ annually on their own |
| 110% - 120% | Excellent | Strong upsell/expansion motion |
| 100% - 110% | Good | Net zero or slight growth from existing base |
| 90% - 100% | Warning | Customer base is shrinking month over month |
| < 90% | Critical | Revenue loss is accelerating |

### The Solo Founder Advantage

Enterprise SaaS companies with $10M+ ARR often target 120%+ NRR. As a solo founder, you can achieve this by:

1. **Personal relationships:** You know customers by name, making upsells natural
2. **Direct feedback loop:** You ship features customers literally ask for
3. **Low overhead:** You can afford to have "unprofitable" accounts if they grow later

### Gross Revenue Retention (GRR)

```
GRR = (Beginning MRR - Churn MRR - Contraction MRR) / Beginning MRR
```

GRR excludes expansion revenue. It shows how much revenue you retain without any upsells. This is your "floor" metric.

**Benchmarks:**
- Good GRR: > 90%
- Great GRR: > 95%
- World-class GRR: > 98%

### Excel/Sheets Formula

```
=((B2 - C2 - D2 + E2) / B2) * 100
```

Where:
- B2 = Starting MRR
- C2 = Churned MRR
- D2 = Contraction MRR
- E2 = Expansion MRR

### Action Items

1. Calculate NRR and GRR every month from month one
2. If NRR < 100%, you need aggressive new customer acquisition just to stay flat
3. If NRR > 120%, you can slow down acquisition and still grow
4. Focus on expansion revenue: usage-based pricing, tier upgrades, add-on features

---

## 8. SaaS Magic Number

### Definition
The Magic Number measures the efficiency of your sales and marketing spend — specifically, how much incremental ARR you generate per dollar spent. It's a leading indicator of growth efficiency.

### Formula

```
Magic Number = (Current Quarter's New ARR - Previous Quarter's New ARR) / Previous Quarter's S&M Expense
```

### Simplified for Solo Founders

Since quarterly data may be noisy, use:
```
Magic Number = Net New MRR This Month / Last Month's S&M Spend
```

### Benchmarks

| Magic Number | Assessment |
|-------------|------------|
| > 1.0 | Outstanding — every dollar generates a dollar of ARR |
| 0.7 - 1.0 | Excellent — highly efficient growth |
| 0.5 - 0.7 | Good — standard SaaS efficiency |
| 0.3 - 0.5 | Needs improvement — review S&M efficiency |
| < 0.3 | Poor — either S&M is misallocated or product isn't converting |

### Example

- Q1 S&M Spend: $10,000
- Q2 New ARR: $15,000
- Q3 New ARR: $25,000
- Magic Number = ($25,000 - $15,000) / $10,000 = 1.0

### Limitations

1. **Lagging by one quarter:** Takes 90 days to measure
2. **Noisy for small numbers:** At $1K MRR, a single customer swings the metric
3. **Doesn't account for product-led growth:** Organic growth has no S&M spend
4. **Not useful pre-PMF:** Don't bother until you have consistent acquisition

### Alternative: Payback Period (Better for Solo Founders)

```
CAC Payback Period (months) = CAC / (Monthly ARPU × Gross Margin)
```

---

## 9. Quick Ratio

### Definition
The Quick Ratio measures your company's ability to grow through the combination of new business and expansion versus losses from churn and contraction.

### Formula

```
Quick Ratio = (New MRR + Expansion MRR) / (Churned MRR + Contraction MRR)
```

### Benchmarks

| Quick Ratio | Assessment |
|-------------|------------|
| > 4 | World-class growth |
| 2 - 4 | Healthy growth |
| 1 - 2 | Growing, but losing ground |
| < 1 | Shrinking |

### Excel/Sheets Formula

```
=(New_MRR + Expansion_MRR) / (Churned_MRR + Contraction_MRR)
```

---

## 10. Burn Multiple

### Definition
The Burn Multiple measures how much cash you're burning relative to the net ARR you're adding. Popularized by Alejandro Cremades and used by many VCs.

### Formula

```
Burn Multiple = Net Cash Burn / Net New ARR
```

### Benchmarks

| Burn Multiple | Assessment |
|-------------|------------|
| < 1 | Capital efficient — burning less than you're growing |
| 1 - 2 | Standard burn for growth-stage |
| 2 - 3 | High burn — needs justification |
| > 3 | Danger zone |

---

## 11. Months of Runway

### Definition
The amount of time your company can operate before running out of cash at the current burn rate.

### Formula

```
Runway (months) = Current Cash Balance / Monthly Burn Rate
```

Where:
```
Monthly Burn Rate = Monthly Expenses - Monthly Revenue
```

### Benchmarks for Solo Founders

| Runway | Risk Level | Recommended Action |
|--------|------------|-------------------|
| > 18 months | Safe | Continue executing, but start fundraising prep |
| 12 - 18 months | Comfortable | Build relationships with investors |
| 6 - 12 months | Caution | Cut expenses, accelerate revenue |
| 3 - 6 months | At risk | Drastic action needed — revenue push or reduce burn |
| < 3 months | Critical | Survival mode — side income, contract work, bridge funding |

### Excel/Sheets Formula

```
=Current_Cash / SUM(Monthly_Expenses) - SUM(Monthly_Revenue)
```

---

## 12. Gross Margin

### Definition
Gross Margin measures the percentage of revenue retained after paying for the direct costs of delivering your service (COGS).

### Formula

```
Gross Margin (%) = (Revenue - COGS) / Revenue × 100
```

### COGS for SaaS

| Category | Examples |
|----------|----------|
| Infrastructure | Cloud hosting (AWS, GCP, Cloudflare), CDN, database |
| Third-Party Services | API costs, email service (SendGrid, Resend), analytics |
| Payment Processing | Stripe/Paddle fees (typically 2.9% + $0.30) |
| Customer Support | Support tool subscriptions |
| Staff (if any) | Support engineers, SRE time |

### Benchmarks

| Gross Margin | Assessment |
|-------------|------------|
| > 85% | World-class (big tech) |
| 75% - 85% | Good SaaS |
| 60% - 75% | Needs improvement |
| < 60% | Problematic — your costs are too high |

### Action Items

1. Track gross margin monthly with a breakdown by category
2. Optimize infrastructure costs (use reserved instances, spot instances)
3. Negotiate volume pricing with third-party services
4. If gross margin < 70%, this is a red flag to fix immediately

---

## 13. Monthly Active Users (MAU) / Daily Active Users (DAU)

### Definition
Measures user engagement with your product.

### Benchmarks

| Metric | Consumer SaaS | B2B SaaS |
|--------|--------------|----------|
| DAU/MAU Ratio | < 20% is low, > 50% is excellent | > 30% is excellent |
| DAU per Paying Customer | N/A | 3-5+ daily active users per account |

### Excel/Sheets Tracking Template

```
Month | Total MAU | Paying MAU | Free MAU | DAU/MAU | MAU per Customer
------|-----------|------------|----------|---------|-----------------
Jan   | 5,000     | 1,200      | 3,800    | 25%     | 8.2
Feb   | 6,200     | 1,500      | 4,700    | 27%     | 7.8
```

---

## 14. Activation Rate

### Definition
The percentage of signups that reach the "aha moment" — the point where a user experiences your core value.

### Formula

```
Activation Rate = Users Who Reached Activation Event / Total Signups × 100
```

### Benchmarks

| Activation Rate | Assessment |
|----------------|------------|
| > 60% | Excellent — onboarding is working |
| 40% - 60% | Good — room for improvement |
| 20% - 40% | Needs work — optimize onboarding |
| < 20% | Critical — users aren't getting value |

### Action Items

1. Identify your "aha moment" (e.g., first report generated, first API call, first export)
2. Track time to activation — measure how many days it takes
3. Optimize onboarding to reduce time to activation
4. For solo founders: personally onboard first 100 customers to identify activation patterns

---

## 15. Viral Coefficient / K-Factor

### Definition
Measures how many new users each existing user brings in through referrals, sharing, or word-of-mouth.

### Formula

```
K = Invitations Sent per User × Conversion Rate per Invitation
```

### Benchmarks

| K-Factor | Assessment |
|----------|------------|
| > 1.0 | Viral growth — each user brings >1 new user |
| 0.5 - 1.0 | Viral assist — significant organic growth |
| 0.1 - 0.5 | Low virality — typical for B2B |
| < 0.1 | No viral growth |

### Solo Founder Reality

Most B2B SaaS products never achieve K > 1.0. Don't build your entire growth strategy around virality. Instead:
1. Build referral programs with incentives (discounts, credits)
2. Make sharing easy (public profiles, shareable reports)
3. Focus on product quality — word-of-mouth is the best growth driver

---

## 16. Customer Health Score

### Definition
A composite metric that predicts likelihood of churn or expansion. Not a single formula — it's a weighted combination of signals.

### Components

| Factor | Weight | Measurement |
|--------|--------|-------------|
| Product Usage | 40% | Logins, feature usage, time in product |
| Support Activity | 20% | Ticket volume, sentiment, response time |
| Payment History | 20% | On-time payments, failed payments |
| Account Profile | 10% | Company size, industry, plan tier |
| Engagement | 10% | Email opens, NPS response, feedback |

### Simple Health Score Formula

```
Health Score = (Usage Score × 0.4) + (Support Score × 0.2) + (Payment Score × 0.2) + (Profile Score × 0.1) + (Engagement Score × 0.1)
```

Each component is normalized to 0-100.

### Scoring Template

```
Customer | Usage | Support | Payment | Profile | Engagement | Health Score
---------|-------|---------|---------|---------|------------|-------------
Acme Inc | 85    | 90      | 100     | 80      | 75         | 86.5
Beta LLC | 30    | 20      | 50      | 80      | 25         | 36.0
```

### Action Items

1. Score customers weekly or monthly
2. Green (80+): Nurture — ask for referrals, case studies
3. Yellow (50-79): Monitor — reach out personally
4. Red (< 50): At risk — intensive intervention needed

---

## 17. Revenue Per Employee

### Definition
Measures how efficiently you generate revenue relative to headcount. As a solo founder, this is especially relevant because you are employee #1.

### Formula

```
Revenue Per Employee = Total Revenue / Total Headcount
```

### Benchmarks

| Headcount | Revenue Per Employee |
|-----------|---------------------|
| Solo founder (you) | Your ARR = 100% |
| 2 employees | $100K - $200K per person |
| 10 employees | $150K - $300K per person |
| 50 employees | $200K - $400K per person |

### Solo Founder Benchmark

As a solo founder:
- **$120K ARR:** You've replaced a decent salary
- **$200K ARR:** You're doing better than most salaried roles
- **$300K ARR:** Time to hire (you're bottlenecked)
- **$500K ARR:** You need at least one employee

---

## 18. Net Promoter Score (NPS)

### Definition
Measures customer satisfaction and willingness to recommend your product.

### Formula

```
NPS = % Promoters (score 9-10) - % Detractors (score 0-6)
```

### Benchmarks

| NPS | Assessment |
|-----|------------|
| > 50 | Excellent |
| 30 - 50 | Good |
| 0 - 30 | Needs improvement |
| < 0 | Poor |

### Tracking Template

```
Quarter | Surveyed | Promoters | Passives | Detractors | NPS | Response Rate
--------|----------|-----------|----------|------------|-----|--------------
Q1 2024 | 200      | 80        | 70       | 50         | 15  | 45%
Q2 2024 | 220      | 100       | 80       | 40         | 27  | 50%
Q3 2024 | 250      | 130       | 80       | 40         | 36  | 52%
```

---

## Quick Reference: The Solo Founder Scorecard

Print this and put it on your wall:

```
Metric              | Target         | Frequency | Priority
--------------------|----------------|-----------|---------
MRR                 | Growing MoM    | Weekly    | ★★★★★
MRR Growth Rate     | > 10% MoM      | Weekly    | ★★★★★
Churn Rate          | < 5% monthly   | Monthly   | ★★★★★
LTV/CAC             | > 3x           | Monthly   | ★★★★☆
CAC Payback Period  | < 12 months    | Monthly   | ★★★★☆
Gross Margin        | > 75%          | Monthly   | ★★★★☆
NRR                 | > 100%         | Monthly   | ★★★☆☆
Activation Rate     | > 40%          | Monthly   | ★★★☆☆
Runway              | > 12 months    | Weekly    | ★★★★★
Net Promoter Score  | > 30           | Quarterly | ★★☆☆☆
```

---

## Spreadsheet Formulas Master Reference

| Metric | Google Sheets Formula |
|--------|----------------------|
| MRR | `=SUMPRODUCT((Revenue!A:A>=DATE(2024,1,1))*(Revenue!A:A...` |
| MRR Growth % | `=(Current_MRR - Previous_MRR) / Previous_MRR * 100` |
| ARR | `=MRR * 12` |
| ARPU | `=MRR / Active_Customers` |
| LTV (simple) | `=ARPU / Monthly_Churn_Rate` |
| LTV (with GM) | `=ARPU / Monthly_Churn_Rate * Gross_Margin` |
| CAC | `=Total_S&M_Spend / New_Customers` |
| LTV/CAC Ratio | `=LTV / CAC` |
| CAC Payback | `=CAC / (Monthly_ARPU * Gross_Margin)` |
| Monthly Churn | `=Churned_Customers / Starting_Customers` |
| Revenue Churn | `=Churned_MRR / Starting_MRR` |
| NRR | `=(Start_MRR - Churn_MRR - Contraction_MRR + Expansion_MRR) / Start_MRR` |
| GRR | `=(Start_MRR - Churn_MRR - Contraction_MRR) / Start_MRR` |
| Quick Ratio | `=(New_MRR + Expansion_MRR) / (Churn_MRR + Contraction_MRR)` |
| Magic Number | `=(Q_New_ARR - Prev_Q_New_ARR) / Prev_Q_S&M` |
| Burn Multiple | `=Net_Cash_Burn / Net_New_ARR` |
| Gross Margin | `=(Revenue - COGS) / Revenue * 100` |
| Runway | `=Cash_Balance / Monthly_Burn_Rate` |

---

## Glossary of Terms

| Term | Definition |
|------|------------|
| ACV | Annual Contract Value — total value of a single customer contract per year |
| TCV | Total Contract Value — total value of a multi-year contract |
| ARR | Annual Recurring Revenue |
| ARPU | Average Revenue Per User |
| ARPA | Average Revenue Per Account |
| CAC | Customer Acquisition Cost |
| COGS | Cost of Goods Sold — direct costs of delivering your service |
| CRM | Customer Relationship Management |
| DAU | Daily Active Users |
| GM | Gross Margin |
| GRR | Gross Revenue Retention |
| LTV/CLV | Customer Lifetime Value |
| MAU | Monthly Active Users |
| MoM | Month over Month |
| MRR | Monthly Recurring Revenue |
| NPS | Net Promoter Score |
| NRR | Net Revenue Retention |
| PMF | Product-Market Fit |
| QoQ | Quarter over Quarter |
| S&M | Sales and Marketing |
| YoY | Year over Year |

---

## Final Advice for Solo Founders

**Start with three metrics:** MRR, Churn, and CAC. Everything else derives from these. Don't build a 50-metric dashboard until you've mastered tracking these three.

**Your first analytics setup should cost $0.** Use Stripe's built-in analytics + a Google Sheet. Upgrade to ChartMogul or Baremetrics only after $5K MRR.

**Investor-ready metrics:** When you talk to investors, have these ready:
1. MRR growth over 12-24 months
2. Cohort retention chart
3. LTV/CAC ratio with payback period
4. NRR
5. Gross margin

**The one metric that matters most:** For a solo founder pre-$100K ARR, it's MRR growth rate. As long as you're growing 15-20% MoM, most other problems are survivable.