# Deep Dive into Unit Economics

A comprehensive guide to understanding and optimizing SaaS unit economics — the fundamental math that determines whether your business survives and thrives. Includes formulas, benchmarks, spreadsheet templates, and actionable strategies for solo founders.

---

## Part 1: The Foundation — Why Unit Economics Matter

### The VC's Favorite Question

When an investor asks "What are your unit economics?" they're really asking: **"Do you make money on every customer, or are you masking losses with growth?"**

For a solo founder, the question is even more personal: **"Can you sustainably acquire customers without going broke?"**

### The Core Principle

```
If LTV > CAC, you have a viable business.
If LTV < CAC, every customer makes you poorer.

The ratio LTV/CAC tells you how efficient your business model is.
The payback period tells you how long until you see that profit.
```

### Why Unit Economics Hit Different as a Solo Founder

| Factor | Solo Founder | VC-Backed Startup |
|--------|--------------|-------------------|
| Cash buffer | Thin (3-12 months) | Thick (18-24 months) |
| Ability to raise more | Limited | Can raise Series A, B, C |
| Time to profitability | Must be fast | Can wait 5-7 years |
| Burn rate tolerance | Low | High |
| **LTV/CAC requirement** | **> 5x** | > 3x |
| **Payback period requirement** | **< 6 months** | < 18 months |

**The solo founder rule:** Your unit economics need to be TWICE as good as a VC-backed startup's because you don't have the cash cushion.

---

## Part 2: The Complete Unit Economics Model

### The Key Metrics

```
ARPU (Average Revenue Per User) = MRR / Total Customers

Gross Margin (GM) = (Revenue - COGS) / Revenue × 100

CAC (Customer Acquisition Cost) = Total S&M Spend / New Customers

CAC Payback Period = CAC / (ARPU × GM)

LTV (Customer Lifetime Value) = ARPU / Monthly Churn Rate × GM

LTV/CAC Ratio = LTV / CAC

Gross Margin Adjusted Payback = CAC / (ARPU × GM)
```

### The Spreadsheet Model

Build this in Google Sheets:

```
Row 1: INPUTS (your assumptions)
  ARPU: $50
  Monthly Churn: 5%
  Gross Margin: 80%
  Total S&M Spend: $3,000
  New Customers: 20
  Expected Customer Lifetime: 20 months (1/churn)

Row 2: CALCULATIONS
  CAC = $3,000 / 20 = $150
  Payback (gross) = $150 / $50 = 3 months
  Payback (GM adjusted) = $150 / ($50 × 0.80) = 3.75 months
  LTV (simple) = $50 / 0.05 = $1,000
  LTV (GM adjusted) = $50 / 0.05 × 0.80 = $800
  LTV/CAC Ratio = $800 / $150 = 5.3x
```

### The Interrelationship

Unit economics are not independent. Changing one affects others:

```
Increase Price (ARPU):
  → ARPU goes up ✓
  → Conversion may go down ✗ (higher CAC)
  → Churn may go up ✗ (price-sensitive customers leave)
  → LTV/CAC may stay the same or change unpredictably

Reduce Churn:
  → LTV goes up ✓
  → CAC stays the same (or may go down with referrals)
  → LTV/CAC improves ✓
  → Most impactful lever for solo founders

Reduce CAC:
  → LTV/CAC improves ✓
  → May reduce volume ✗ (if you cut effective channels)
  → Payback period improves ✓
```

---

## Part 3: CAC Payback Period — Deep Dive

### What It Measures

CAC payback period is the number of months it takes to earn back what you spent acquiring a customer (after accounting for the cost of delivering service).

### Why It Matters for Solo Founders

Your cash flow depends entirely on how fast customers pay back their acquisition cost.

```
Scenario A: Payback in 3 months
  Month 1: Spend $5K on ads, get 20 customers
  Month 4: Those 20 customers have paid back $5K
  Month 4+: All revenue is pure profit
  Cash flow: Cash-positive by Month 4

Scenario B: Payback in 15 months
  Month 1: Spend $5K on ads, get 20 customers
  Month 15: Those 20 customers finally pay back $5K
  Months 1-15: You must keep injecting cash to grow
  Cash flow: Deeply negative for over a year
```

**As a solo founder with 12 months of runway, Scenario A is survivable. Scenario B will kill you.**

### Payback Period Benchmarks

| Payback Period | Assessment | Solo Founder Viability |
|---------------|------------|----------------------|
| < 3 months | Excellent | Very safe — grow aggressively |
| 3-6 months | Good | Safe — grow at measured pace |
| 6-9 months | Fair | Caution — monitor cash closely |
| 9-12 months | Poor | Risky — need to fix before growing |
| > 12 months | Critical | Unsustainable — you'll run out of cash |

### Improving Payback Period

**Levers you can pull:**

| Lever | Impact | Time to Implement | Risk |
|-------|--------|-------------------|------|
| Reduce CAC | High | 1-3 months | Lower volume |
| Increase prices | Medium | Immediate | Higher churn |
| Reduce churn | Very High | 3-6 months | None |
| Increase gross margin | Medium | 1-2 months | Lower quality |
| Annual prepayments | Medium | Immediate | Less cash upfront (actually helps payback!) |

### Payback Period Calculator

```python
def calculate_payback(cac, arpu, gross_margin=0.75):
    """
    Calculate CAC payback period in months.
    
    Args:
        cac: Customer Acquisition Cost
        arpu: Average Revenue Per User (monthly)
        gross_margin: Gross Margin (0.0 to 1.0)
    
    Returns:
        payback_months: Number of months to recoup CAC
    """
    monthly_profit = arpu * gross_margin
    payback_months = cac / monthly_profit
    return round(payback_months, 1)

# Example
print(calculate_payback(200, 50, 0.75))
# Output: 5.3 months

print(calculate_payback(200, 50, 0.80))
# Output: 5.0 months

print(calculate_payback(150, 60, 0.80))
# Output: 3.1 months
```

---

## Part 4: LTV/CAC Ratio — Deep Dive

### What It Measures

The LTV/CAC ratio tells you how much lifetime value you generate for every dollar spent acquiring a customer.

```
LTV/CAC = 3x → Every $1 spent on acquisition generates $3 in lifetime profit
LTV/CAC = 5x → Every $1 generates $5 in lifetime profit
LTV/CAC = 1x → You break even on each customer (after their lifetime)
LTV/CAC < 1x → You lose money on every customer
```

### Why the Ratio Matters

| LTV/CAC | Interpretation | Solo Founder Action |
|---------|---------------|---------------------|
| > 10x | World-class efficiency | Invest more in growth — you're under-spending |
| 5x - 10x | Excellent | Keep doing what you're doing |
| 3x - 5x | Good — minimum healthy | Maintain, optimize slowly |
| 2x - 3x | Below average | Urgent improvements needed |
| 1x - 2x | Poor | Drastic changes required |
| < 1x | Unsustainable | Pivot or shut down |

### The Solo Founder Threshold

**Minimum healthy LTV/CAC for solo founders: 5x**

Why 5x instead of 3x?
1. You have less cash buffer to absorb mistakes
2. Your customers may churn faster (less brand recognition)
3. You can't raise a bridge round if things go wrong
4. Your G&A expenses are a higher percentage of revenue
5. You need to reinvest in the business (tools, infrastructure)

### LTV/CAC by Business Model

| Business Model | Typical LTV/CAC | Solo Founder Target |
|---------------|-----------------|---------------------|
| Self-serve SMB | 3-5x | > 4x |
| Sales-assisted SMB | 5-8x | > 5x |
| Mid-market | 5-10x | > 5x |
| Enterprise | 5-15x | > 5x |
| Consumer SaaS | 2-5x | > 4x |

### The LTV/CAC Spreadsheet Model

```yaml
LTV/CAC Model (Monthly)

ASSUMPTIONS:
  Starting Customers: 100
  New Customers per Month: 20
  ARPU: $50
  Monthly Churn: 5%
  Gross Margin: 80%
  S&M Spend per Month: $3,000

CALCULATIONS:
  Average Lifetime (months): 1 / 0.05 = 20 months
  LTV (simple): $50 × 20 = $1,000
  LTV (GM adjusted): $50 × 20 × 0.80 = $800
  CAC: $3,000 / 20 = $150
  LTV/CAC Ratio: $800 / $150 = 5.3x

SCENARIOS:
  Optimistic: Churn improves to 4%, LTV/CAC = 6.7x
  Pessimistic: Churn increases to 7%, LTV/CAC = 3.8x
  Worst Case: Churn at 10%, LTV/CAC = 2.7x
```

### LTV/CAC Sensitivity Analysis

Create a sensitivity table in your spreadsheet:

```
           | Monthly Churn Rate
           | 2%    | 3%    | 5%    | 7%    | 10%
-----------|-------|-------|-------|-------|-------
$50 ARPU   | 13.3x | 8.9x  | 5.3x  | 3.8x  | 2.7x
$75 ARPU   | 20.0x | 13.3x | 8.0x  | 5.7x  | 4.0x
$100 ARPU  | 26.7x | 17.8x | 10.7x | 7.6x  | 5.3x
```

**Formula for each cell:**
```
= (ARPU × Gross Margin × (1 / Monthly Churn)) / CAC
```

**Key insight:** At $50 ARPU and $150 CAC, churn above 6% puts you below 5x LTV/CAC. This tells you exactly how good your retention needs to be.

---

## Part 5: Gross Margin — The Overlooked Metric

### What It Measures

Gross margin shows how much revenue you keep after paying the direct costs of delivering your service. For SaaS, COGS includes:

| COGS Category | Typical % of Revenue | Examples |
|---------------|---------------------|----------|
| Infrastructure | 5-15% | Cloud hosting, CDN, database |
| Third-party APIs | 2-8% | AI APIs, data providers, email service |
| Payment processing | 3-5% | Stripe/Paddle fees |
| Customer support | 2-5% | Support tools, support staff |

### Gross Margin Benchmarks

| Gross Margin | Assessment | Notes |
|-------------|------------|-------|
| > 85% | World-class | Microsoft, Salesforce territory |
| 80-85% | Excellent | Most mature SaaS |
| 75-80% | Good | Target range for solo founders |
| 70-75% | Fair | Monitor closely, improve slowly |
| 60-70% | Poor | Need to reduce costs or raise prices |
| < 60% | Critical | Business model may not work |

### Improving Gross Margin

**1. Infrastructure optimization:**
- Use reserved instances (AWS) or committed use discounts (GCP) — saves 30-60%
- Right-size your infrastructure (don't over-provision)
- Use Cloudflare for caching and CDN (reduces origin server costs)
- Implement caching aggressively (reduce database queries)
- Consider moving to serverless (pay-per-use instead of flat costs)

**2. Payment processing optimization:**
- Negotiate with Stripe (volume discounts above $1M/month)
- Consider Paddle or LemonSqueezy (higher % but no sales tax handling)
- Use ACH/direct debit for enterprise customers (lower fees)
- Reduce failed payment costs (better dunning = fewer retries)

**3. Third-party costs:**
- Audit every API and third-party subscription
- Are you paying for unused capacity?
- Can you self-host any services?
- Negotiate volume pricing as you grow
- Batch API calls to reduce count

### Gross Margin Calculator

```python
def calculate_gross_margin(revenue, cogs_breakdown):
    """
    Calculate gross margin with breakdown.
    
    Args:
        revenue: Total monthly revenue
        cogs_breakdown: Dict of COGS categories and amounts
    
    Returns:
        gross_margin_pct, cogs_pct_by_category
    """
    total_cogs = sum(cogs_breakdown.values())
    
    gross_margin = ((revenue - total_cogs) / revenue) * 100
    cogs_pct = {}
    
    for category, amount in cogs_breakdown.items():
        cogs_pct[category] = (amount / revenue) * 100
    
    return round(gross_margin, 1), cogs_pct

# Example
revenue = 10000
cogs = {
    'infrastructure': 1200,
    'api_costs': 400,
    'payment_processing': 350,
    'support_tools': 200,
}

gm, breakdown = calculate_gross_margin(revenue, cogs)
print(f"Gross Margin: {gm}%")
for cat, pct in breakdown.items():
    print(f"  {cat}: {pct}%")

# Output:
# Gross Margin: 78.5%
#   infrastructure: 12.0%
#   api_costs: 4.0%
#   payment_processing: 3.5%
#   support_tools: 2.0%
```

---

## Part 6: Customer Acquisition Cost (CAC) — Full Breakdown

### The Hidden Costs

Most founders only track direct ad spend as CAC. But your true CAC includes:

| Cost Component | Example | Solo Founder Consideration |
|---------------|---------|---------------------------|
| Direct ad spend | Google Ads, Facebook Ads | Easy to track |
| Content marketing | Blog posts, videos, SEO | Amortize over 6-12 months |
| Sales tools | CRM, email outreach, LinkedIn | Often minimal for solo |
| Time cost | Your hours spent on sales | Assign $50-100/hr |
| Referral costs | Discounts, credits, commissions | Variable but trackable |
| Free trial costs | Infrastructure for free users | Significant at scale |
| Onboarding costs | Time spent onboarding new users | Often forgotten |

### CAC by Channel

| Channel | Typical CAC | Solo Founder Viability |
|---------|-------------|----------------------|
| Organic (SEO) | $0 - $50 | Excellent — invest heavily |
| Referrals | $0 - $25 | Excellent — incentivize |
| Content marketing | $20 - $100 | Excellent — solo founders can write |
| Social media (organic) | $10 - $50 | Good — time-intensive |
| Google Ads (search) | $50 - $500 | Good — if LTV supports it |
| LinkedIn Ads | $100 - $1,000 | Fair — expensive but targeted |
| Facebook Ads | $30 - $200 | Fair — declining for B2B |
| Affiliates | 20-30% of revenue | Good — performance-based |
| Partnerships | $50 - $500 | Good — scalable over time |
| Conferences/Events | $500 - $5,000 | Poor for solo — too expensive |

### CAC Tracking Template

```yaml
Channel         | Spend | New Customers | CAC   | Conversion Rate | Trend
Organic         | $0    | 15            | $0    | 3.2%            | Flat
Content         | $500  | 8             | $62.50 | 1.8%           | Growing
Google Ads      | $1,200| 6             | $200  | 4.5%            | Declining
Referrals       | $100  | 4             | $25   | 25%             | Growing
Twitter/X       | $0    | 2             | $0    | 0.5%            | Flat
Total           | $1,800| 35            | $51.43| ---             | ---
```

**Formulas:**
```
CAC = Channel Spend / Customers from Channel
Blended CAC = Total Spend / Total New Customers
```

### CAC Payback Period by Channel

Beyond just CAC, calculate payback for each channel:

```yaml
Channel    | CAC  | Monthly ARPU | Payback (months)
Organic    | $0   | $50          | 0.0
Content    | $63  | $50          | 1.6 (63 / 50 × 0.80 GM)
Google Ads | $200 | $50          | 5.0
Referrals  | $25  | $50          | 0.6
```

**Decision:** Google Ads takes 5 months to pay back. With a 12-month runway, you can afford this — but only if you have sufficient cash flow from organic/referral channels.

---

## Part 7: LTV Calculation — Methods and Precision

### Method 1: Simple LTV (Quick Estimate)

```
LTV = ARPU / Monthly Churn Rate
```

**Example:**
```
ARPU: $50
Monthly Churn: 5%
LTV = $50 / 0.05 = $1,000
```

**When to use:** Quick estimate, pre-revenue planning, early stage with little data.

**Limitations:** Assumes churn is constant over time (it's not — churn typically decreases for older cohorts).

### Method 2: Gross Margin Adjusted LTV

```
LTV = ARPU × Gross Margin / Monthly Churn Rate
```

**Example:**
```
ARPU: $50
GM: 80%
Monthly Churn: 5%
LTV = $50 × 0.80 / 0.05 = $800
```

**When to use:** More accurate, accounts for cost of delivery.

### Method 3: Cohort-Based LTV (Most Accurate)

Track revenue per cohort month by month:

```
Cohort: January 2024 (100 customers)
Month 1: Revenue = $5,000 → Per customer = $50
Month 2: Revenue = $4,500 → Per customer = $45 (some churned)
Month 3: Revenue = $4,200 → Per customer = $42
Month 4: Revenue = $4,000 → Per customer = $40
...
Month 12: Revenue = $3,000 → Per customer = $30

Cumulative LTV = $50 + $45 + $42 + $40 + ... + $30 = $450 (after 12 months)
Projected LTV = $450 + extrapolated future months
```

**When to use:** Any stage where you have 6+ months of data. Much more accurate.

### Method 4: Discounted LTV (Investor Grade)

Accounts for the time value of money:

```
LTV = Sum of (Monthly Profit / (1 + Discount Rate)^Month)

Where:
  Discount Rate = 5-10% annually for SaaS
  Monthly Profit = ARPU × Gross Margin for each month the customer remains
```

**Example (10% annual discount rate = 0.83% monthly):**
```
Month 1: $40 / (1.0083)^1 = $39.67
Month 2: $38 / (1.0083)^2 = $37.41
Month 3: $36 / (1.0083)^3 = $35.10
...
Total Discounted LTV = Sum of all discounted monthly profits
```

### LTV by Customer Segment

Most powerful LTV analysis — break down by segment:

```yaml
Segment         | ARPU  | Monthly Churn | LTV (GM Adj) | LTV/CAC
Self-serve      | $29   | 8%            | $261         | 3.5x
Sales-assisted  | $99   | 4%            | $1,782       | 5.1x
Enterprise      | $499  | 2%            | $17,964      | 8.5x
```

**Action:** Focus acquisition on segments with highest LTV/CAC ratio.

---

## Part 8: The Unit Economics Dashboard

### Full Dashboard Template

```yaml
UNIT ECONOMICS DASHBOARD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CURRENT MONTH:
  ARPU: $54         (last month: $52)         ↑ +3.8%
  Monthly Churn: 4.8%  (last month: 5.2%)     ↓ -0.4pp
  Gross Margin: 81%    (last month: 80%)      ↑ +1pp
  CAC: $185           (last month: $210)      ↓ -11.9%
  Payback: 4.3 months  (last month: 5.1 mo)   ↓ -0.8mo
  LTV: $900            (last month: $800)     ↑ +12.5%
  LTV/CAC: 4.9x        (last month: 3.8x)    ↑ +1.1x

COHORT COMPARISON:
  Latest Cohort (Apr): LTV/CAC = 5.2x
  Prior Cohort (Mar):  LTV/CAC = 4.8x
  3 Months Ago (Feb):  LTV/CAC = 4.1x
  → Improving ✓

CHANNEL BREAKDOWN:
  Organic: CAC=$0,    Payback=0mo,   LTV/CAC=∞
  Content: CAC=$85,   Payback=1.9mo, LTV/CAC=10.6x
  Google Ads: CAC=$250, Payback=5.7mo, LTV/CAC=3.6x
  Referral: CAC=$30,  Payback=0.7mo, LTV/CAC=30x
  Twitter: CAC=$110,  Payback=2.5mo, LTV/CAC=8.2x

TRENDS (3 Month Rolling):
  CAC: $195 → $190 → $185     Improving ↓
  ARPU: $50 → $52 → $54        Improving ↑
  Churn: 5.5% → 5.2% → 4.8%   Improving ↓
  LTV/CAC: 3.5x → 3.8x → 4.9x Improving ↑

WARNINGS:
  ⚠ Google Ads CAC > 5x ARPU ($250 vs $54*5=$270) — borderline
  ⚠ Churn still above 5x LTV/CAC threshold for target
```

---

## Part 9: The Solo Founder Unit Economics Playbook

### Phase 1: Pre-Revenue to $5K MRR

**Goal:** Find a channel with positive unit economics

**Actions:**
```
1. Focus on FREE channels only (organic, content, referrals)
2. Your CAC should be $0 (you're spending time, not money)
3. Track churn from day 1 — if it's > 10% monthly, find PMF first
4. Don't worry about LTV/CAC ratio yet — sample size is too small
5. Talk to every churned customer — understand why they left
6. If you must spend money, keep it under $100/month
```

**Target metrics:**
- Monthly churn: < 10% (ideally < 5%)
- Payback period: N/A (no paid acquisition)
- LTV/CAC: Not applicable yet

### Phase 2: $5K to $20K MRR

**Goal:** Prove unit economics work at small scale

**Actions:**
```
1. Start one paid channel (Google Ads is best for B2B)
2. Cap spend at $500/month — prove economics before scaling
3. Calculate CAC for every channel separately
4. Aim for LTV/CAC > 5x on every channel
5. Optimize gross margin — aim for > 75%
6. Reduce churn from onboarding improvements
7. Implement annual pricing to improve cash flow
```

**Target metrics:**
- Monthly churn: < 7%
- Payback period: < 6 months
- LTV/CAC: > 5x
- Gross margin: > 75%

### Phase 3: $20K to $100K MRR

**Goal:** Scale what works, kill what doesn't

**Actions:**
```
1. Triple down on channels with best unit economics
2. Kill channels with payback > 12 months
3. Segment unit economics by customer type
4. Build LTV/CAC sensitivity models
5. Implement pricing experiments to improve ARPU
6. Reduce churn through product improvements
7. Consider annual-only pricing for cash flow
```

**Target metrics:**
- Monthly churn: < 5%
- Payback period: < 6 months
- LTV/CAC: > 5x on all active channels
- Gross margin: > 80%

### Phase 4: $100K+ MRR

**Goal:** Optimize and systematize

**Actions:**
```
1. Automate unit economics tracking (ChartMogul or custom)
2. Build predictive models (churn prediction, LTV forecasting)
3. Full cohort-based LTV analysis
4. Run pricing optimization experiments
5. Hire for growth (first non-founder hire)
6. Build sales team if LTV supports it
7. Annual planning based on unit economics
```

**Target metrics:**
- Monthly churn: < 3%
- Payback period: < 9 months (can be longer with more cash)
- LTV/CAC: > 5x
- Gross margin: > 80%

---

## Part 10: Common Unit Economics Mistakes

### Mistake 1: Counting Annual Prepayments as MRR

**Problem:** You get $12K for an annual deal and think it's $1K/month MRR.

**Reality:** It's $1K/month MRR — but you have $12K deferred revenue, not $12K profit.

**Fix:** Always normalize to monthly. Track cash separately from revenue.

### Mistake 2: Not Including All COGS in Gross Margin

**Problem:** You think gross margin is 90% because you only count hosting costs.

**Reality:** You forgot payment processing (3%), API costs (4%), support tool (2%), and your own time spent onboarding (5%). Real GM is closer to 76%.

**Fix:** Create a comprehensive COGS list. Include EVERYTHING that scales with revenue.

### Mistake 3: Using Blended CAC Instead of Channel CAC

**Problem:** Blended CAC is $50, looks great. But organic is $0 and Google Ads is $300.

**Reality:** You're subsidizing Google Ads with organic. When you scale Google Ads, your blended CAC will skyrocket.

**Fix:** Always track CAC by channel. Scale channels independently.

### Mistake 4: Assuming Constant Churn

**Problem:** Average churn is 5%, so you calculate LTV = ARPU / 0.05.

**Reality:** First-month churn might be 8%, and month-12 churn might be 2%. Your LTV is higher than your simple calculation.

**Fix:** Use cohort-based LTV or account for the churn curve (churn rate decreasing over time).

### Mistake 5: Ignoring the Time Value of Money

**Problem:** LTV/CAC looks great at 8x, but payback period is 14 months.

**Reality:** You'll run out of cash waiting for customers to pay back. Especially dangerous for solo founders.

**Fix:** Always pair LTV/CAC with payback period. Both matter.

### Mistake 6: Optimizing the Wrong Lever

**Problem:** You spend months reducing CAC by $10 (from $200 to $190).

**Reality:** Reducing churn from 5% to 4% improves LTV by 25% ($1,000 → $1,250).

**Fix:** Prioritize improvements by impact: Churn > ARPU > Gross Margin > CAC.

### Mistake 7: Ignoring the "CAC Payback Cliff"

**Problem:** Your payback period is 8 months and you have 6 months of runway.

**Reality:** You'll run out of cash before customers pay back. You can't fund growth.

**Fix:** Payback period must be LESS than your available runway / 2. If runway is 12 months, payback must be under 6 months.

---

## Part 11: Take Action Today

### Your Unit Economics Checklist

```
□ Know your exact ARPU (from Stripe data)
□ Know your exact monthly churn (by cohort)
□ Know your exact gross margin (all COGS included)
□ Know your CAC by channel (not blended)
□ Know your payback period (GM adjusted)
□ Know your LTV/CAC ratio (GM adjusted)
□ Build sensitivity model (what happens if churn increases by 2%?)
□ Identify your BEST channel (lowest CAC, highest LTV)
□ Identify your WORST channel (highest CAC, lowest LTV)
□ Set unit economics improvement goal for this quarter
```

### The 30-Day Unit Economics Sprint

```
Week 1: Data Collection
  - Export Stripe data for last 6 months
  - Calculate actual ARPU, churn, gross margin
  - Track all S&M spend for last 3 months
  - Calculate CAC by channel

Week 2: Analysis
  - Build unit economics spreadsheet
  - Calculate payback period
  - Calculate LTV/CAC ratio
  - Build sensitivity scenarios
  - Identify biggest improvement lever

Week 3: Action Planning
  - If churn is biggest problem: Plan retention improvements
  - If CAC is biggest problem: Identify best channel to scale
  - If ARPU is low: Plan pricing experiment
  - If gross margin is low: Plan cost reduction

Week 4: Implementation
  - Implement one unit economics improvement
  - Set up automated tracking
  - Create weekly unit economics review
  - Share with mentor or advisor
```

### The Bottom Line

> **Unit economics tell you if your business works.**
> Growth rate tells you how fast it works.
> Cash balance tells you if you'll survive to see it work.

For solo founders: **Fix unit economics before scaling.** A growing business with bad unit economics is a faster path to bankruptcy.