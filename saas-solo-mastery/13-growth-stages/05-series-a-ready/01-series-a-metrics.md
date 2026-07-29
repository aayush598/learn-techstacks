# Metrics That Matter for Series A: Growth Rate, Retention, Unit Economics, Market Size

## Why Series A Metrics Matter for Solo Founders

Even if you're bootstrapped and never plan to raise venture capital, Series A metrics are the universal language of SaaS health. They tell you:

- Is your business actually growing sustainably?
- Are you building something people will pay for long-term?
- Is the unit economy viable, or are you losing money on every customer?
- Is there a large enough market to build a real company?

For founders who DO plan to raise:
- Series A is the first institutional round where VCs scrutinize your metrics deeply
- Seed rounds fund the search for product-market fit. Series A funds the SCALING of an already-fit product.
- The bar is higher than you think: most VCs reject 95%+ of Series A candidates

The metrics in this guide are what VCs evaluate. More importantly, they're what YOU should be evaluating to know if your business is ready to scale.

## The Series A Readiness Framework

```
Investors answer three questions:

1. Is this a big market? (Market size)
2. Can this company capture it? (Growth + traction)
3. Will the economics work? (Unit economics + retention)

You need to pass ALL three, not just one.
```

## Metric 1: Growth Rate (The #1 Most Important Metric)

### What VCs Look For

Growth rate is the single strongest signal of product-market fit and future success.

**Series A Growth Benchmarks:**

| Metric | Good | Great | Exceptional |
|--------|------|-------|-------------|
| Monthly revenue growth | 10-15% | 15-20% | 20%+ |
| Annual revenue growth (YoY) | 200-300% | 300-500% | 500%+ |
| Revenue at Series A | $10-30K MRR | $30-100K MRR | $100K+ MRR |
| Growth efficiency | < $1.50 to acquire $1 ARR | < $1.00 | < $0.50 |

**The Growth Persistence Rule:**
- Consistent growth over 12+ months = strong signal
- One spike month = weak signal (could be seasonal, one-time event)
- VCs look for: "Do they grow every month even when they do nothing special?"

### Calculating Growth Rate

```python
# Month-over-month growth rate
def mom_growth(this_month, last_month):
    return (this_month - last_month) / last_month * 100

# Compounded monthly growth rate (CAGR)
def cagr(starting_mrr, ending_mrr, months):
    return (ending_mrr / starting_mrr) ** (1 / months) - 1

# Rule of 40 (growth rate + profit margin should exceed 40%)
def rule_of_40(revenue_growth_rate, profit_margin):
    return revenue_growth_rate + profit_margin
    # SaaS companies at Series A often have negative margins
    # But growth rate should compensate
    # Target: > 40% combined
```

### Growth Rate by Stage

```
Seed stage:
- Focus: Finding PMF
- Growth rate: Highly variable, inconsistent
- Expectation: Monthly swings up to 50% (new launches, experiments)

Series A:
- Focus: Proving repeatable growth
- Growth rate: 15%+ MoM for 6+ months
- Expectation: Consistent, predictable, month after month

Series B:
- Focus: Accelerating growth
- Growth rate: 10%+ MoM with increasing absolute revenue
- Expectation: Economies of scale improving unit economics
```

### What If Your Growth Rate Is Below 10%?

Common reasons and fixes:

```
Low growth rate — diagnostic:

1. You've saturated your initial channel
   - Fix: Build a second acquisition channel
   - Example: If content drove your first 50 customers, try referrals or partnerships

2. Your pricing is too low
   - Fix: Raise prices by 25-50%
   - Higher prices = more room for acquisition spend = faster growth

3. Your churn is too high
   - Fix: Fix retention before scaling acquisition
   - If you're losing 10%/month, you need 10%+ growth just to stay flat

4. Your market is small
   - Fix: Expand to adjacent segments or geographies
   - Sometimes the math just doesn't work for VC-scale

5. Your sales process doesn't scale
   - Fix: Build self-serve or automated sales
   - Founder-led sales doesn't compound (you can't clone yourself)
```

## Metric 2: Retention (The Quality of Your Growth)

### Why Retention > Acquisition

Here's the math that keeps VCs up at night:

```
Scenario A: 10% monthly growth, 5% monthly churn
Net growth rate: 5% month-over-month
After 12 months: 1.05^12 = 1.80x growth

Scenario B: 20% monthly growth, 15% monthly churn
Net growth rate: 5% month-over-month (same!)  
After 12 months: same 1.80x growth

BUT: Scenario A's customers stay 3x longer (20 months vs 6.7 months)
Scenario A's LTV is 3x higher
Scenario A's compounding advantage shows after 24+ months
```

High growth with high churn = leaky bucket. You're acquiring users who leave immediately.

### Retention Metrics VCs Care About

| Metric | Weak | Moderate | Strong | World-Class |
|--------|------|----------|--------|-------------|
| Net Revenue Retention (NRR) | < 80% | 80-100% | 100-120% | 120%+ |
| Gross Revenue Retention (GRR) | < 70% | 70-85% | 85-95% | 95%+ |
| Logo retention (monthly) | < 95% | 95-97% | 97-99% | 99%+ |
| Logo retention (annual) | < 70% | 70-85% | 85-95% | 95%+ |

**Net Revenue Retention (NRR) = The Magic Number:**
NRR measures how much revenue you keep from existing customers, including expansions, upgrades, and contractions.

```
NRR = (Starting MRR + Expansion - Contraction - Churn) / Starting MRR

Example:
- Starting MRR from existing customers: $10,000
- Upgrades/expansion: $1,000
- Downgrades: $500
- Churned: $400
- NRR = ($10,000 + $1,000 - $500 - $400) / $10,000 = 101%

100%+ NRR means your existing customers are growing faster than you're losing them.
This is the holy grail for VCs.
```

**How to Improve NRR:**

```
1. Build for expansion
   - Usage-based pricing (grows with customer success)
   - Tiered plans with natural upgrade path
   - Add-ons and integrations as upsells
   - Annual contracts with built-in price increases

2. Reduce churn
   - Improve onboarding (first 30 days determine retention)
   - Customer health scoring (intervene before churn)
   - Excellent support (retention through service)
   - Product improvements (retention through value)

3. Price optimization
   - Raise prices for new customers (grandfather existing)
   - Introduce annual plans (reduces churn risk)
   - Bundle features into higher tiers
```

### Cohort Retention Table

Your cohort retention table is one of the most powerful exhibits in your pitch deck:

```
Month 1  2   3   4   5   6   7   8   9   10  11  12
─────────────────────────────────────────────────────
Jan 23: 100% 65% 52% 45% 40% 37% 35% 34% 33% 32% 31% 31%
Feb 23: 100% 62% 48% 42% 38% 35% 33% 32% 31% 30% 30%
Mar 23: 100% 68% 55% 48% 42% 39% 37% 35% 34% 33%
Apr 23: 100% 70% 58% 50% 45% 41% 39% 37% 35%
May 23: 100% 72% 60% 53% 47% 43% 41% 39%
Jun 23: 100% 75% 63% 55% 50% 45% 43%
Jul 23: 100% 78% 65% 58% 52% 48%
Aug 23: 100% 80% 68% 60% 55%
Sep 23: 100% 82% 70% 62%
Oct 23: 100% 85% 73%
Nov 23: 100% 87%
Dec 23: 100%
```

**What VCs look for in this table:**
- Are newer cohorts retaining better than older cohorts? → Product improvement signal
- Does retention plateau after month 3? → PMF signal
- Is retention declining steadily? → No PMF
- Is the curve flattening at a higher level over time? → Compounding improvement

## Metric 3: Unit Economics (The Math of Your Business)

### Customer Acquisition Cost (CAC)

CAC = Total sales and marketing cost / New customers acquired

```
CAC Calculation:

Blended CAC:
Total S&M spend (including your salary, tools, ads) / New customers

Paid CAC:
Total ad spend / New customers from ads

Organic CAC:
Total content/SEO spend / New customers from organic

Sales-assisted CAC:
Sales team costs / New customers from sales

Example:
- Monthly S&M spend: $10,000 (your time + tools + ads)
- New customers: 50
- Blended CAC: $200
```

**Series A CAC Benchmarks:**

| CAC Level | Assessment | Typical for |
|-----------|------------|-------------|
| < $50 | Very low | Self-serve, PLG, viral products |
| $50-200 | Low | Content-driven, inbound |
| $200-1,000 | Moderate | Sales-assisted, mid-market |
| $1,000-5,000 | High | Enterprise sales |
| $5,000+ | Very high | Complex enterprise |

### Lifetime Value (LTV)

LTV = ARPU / Churn rate

```
LTV Calculation (Simple):

ARPU = $50/month
Monthly churn = 5%
Average lifetime = 1 / 0.05 = 20 months
LTV = $50 × 20 = $1,000

LTV Calculation (With Expansion):
ARPU = $50
NRR = 110% (growing)
Monthly churn = 5%
More complex calculation, but LTV is HIGHER than simple formula
```

**Series A LTV Benchmarks:**

| LTV | Assessment |
|-----|------------|
| < $500 | Low — likely doesn't support paid acquisition |
| $500-2,000 | Moderate — supports some paid channels |
| $2,000-10,000 | Strong — supports multiple channels |
| $10,000+ | Excellent — enterprise-level |

### CAC Payback Period

How long to earn back what you spent to acquire a customer.

```
CAC Payback = CAC / (ARPU × Gross Margin)

Example:
- CAC: $500
- ARPU: $50/month
- Gross margin: 80%
- CAC Payback = $500 / ($50 × 0.80) = 12.5 months
```

**Benchmarks:**

| Payback Period | Assessment |
|----------------|------------|
| < 6 months | Excellent |
| 6-12 months | Good |
| 12-18 months | Okay (common for enterprise) |
| 18+ months | Concerning |

### LTV:CAC Ratio

The holy grail of unit economics.

```
LTV:CAC = LTV / CAC

Example:
- LTV: $1,000
- CAC: $200
- LTV:CAC = 5:1
```

**Benchmarks:**

| Ratio | Assessment |
|-------|------------|
| < 1:1 | Business destroys value — every customer costs more than they return |
| 1:1 - 3:1 | Okay, but limited room for growth spend |
| 3:1 - 5:1 | Good — healthy unit economics |
| 5:1+ | Excellent — can invest aggressively in growth |

**VC sweet spot:** 3:1 to 5:1. Below 3:1 and you can't spend on growth. Above 5:1 and you're not spending enough on growth.

### Gross Margin

Gross Margin = (Revenue - COGS) / Revenue

```
COGS for SaaS includes:
- Cloud infrastructure (hosting, database, CDN)
- Payment processing fees
- Customer support costs (direct)
- API costs (if applicable)

COGS does NOT include:
- R&D (engineering salaries)
- Sales and marketing
- G&A (admin, office, legal)
```

**SaaS Gross Margin Benchmarks:**

| Margin | Assessment |
|--------|------------|
| < 60% | Low — infrastructure-heavy or support-heavy |
| 60-75% | Below average for SaaS |
| 75-85% | Average for SaaS |
| 85%+ | Excellent |

**Series A expectation:** 75%+ gross margin, trending toward 80%+ as you scale.

## Metric 4: Market Size (The TAM, SAM, SOM Framework)

### Why Market Size Matters

VCs need to believe your company can be worth $1B+ for them to get a meaningful return. If your market is $100M total, you can't build a $1B company.

```
TAM (Total Addressable Market):
  "If everyone who could possibly use this product did, how much 
  revenue would that be?"

SAM (Serviceable Addressable Market):
  "Of the TAM, what portion can we realistically reach with our 
  current distribution model?"

SOM (Serviceable Obtainable Market):
  "Of the SAM, what portion can we realistically capture in the 
  next 3-5 years?"
```

### Calculating TAM for a SaaS

```
Top-down approach:
"Project management software market is $10B globally."
→ May be accurate but tells you nothing about your ability to compete

Bottom-up approach (more credible):
"There are 500,000 marketing agencies worldwide."
"Average agency has 10 employees."
"Our pricing is $50/user/month."
"TAM = 500,000 × 10 × $50 × 12 = $3B"
→ More credible because it's based on your actual pricing and audience

Third-party validation:
"Gartner predicts the [category] market will reach $X by 2028."
→ Useful for framing, but less credible alone
```

### Market Size Expectations for Series A

| Market Size | Assessment |
|-------------|------------|
| < $100M | Too small for most VCs |
| $100M - $1B | Small — need dominant market share |
| $1B - $10B | Good — can build a meaningful company |
| $10B+ | Excellent — lots of room for growth |

**Important nuance:** "No market" is a common reason VCs pass. But "huge market" without traction is also a red flag. You need both.

### Market Expansion Narrative

Even if your current SAM is small, show how you'll expand:

```
Current: "We serve freelance designers in the US." (SAM: $200M)

Year 1: "Expand to all freelance creatives" (SAM: $800M)
Year 2: "Expand to small agencies" (SAM: $2B)
Year 3: "Expand to UK and EU markets" (SAM: $4B)
Year 4: "Platform for all creative businesses" (SAM: $10B)
```

VCs want to see a path from a beachhead to a large market.

## Metric 5: Capital Efficiency (The Solo Founder Advantage)

### What Capital Efficiency Means

Capital Efficiency = How much growth you generate per dollar of investment

```
Capital Efficiency = ARR Generated / Total Capital Raised

Example:
- You raised $500K seed
- Current ARR: $500K
- Capital Efficiency: 1.0 (generated $1 ARR for every $1 raised)

VC benchmark:
- Efficient: > 1.0 (generated more ARR than raised)
- Average: 0.5-1.0
- Inefficient: < 0.5
```

### The Solo Founder's Advantage

As a bootstrapped or capital-efficient solo founder, you have an advantage:

```
Your story: "We reached $100K ARR with $0 in outside funding."
VC perception: "This founder knows how to build value. If we give them 
capital, they'll use it well."

vs.

Funding-heavy story: "We reached $100K ARR after raising $2M."
VC perception: "This team burns cash. Can they ever be efficient?"
```

**Capital efficiency signals:**
- Bootstrapped to meaningful revenue
- Low burn rate relative to revenue
- High gross margins
- Organic growth (viral, word-of-mouth, content)
- Lean team (solo or small team achieving big numbers)

## Metric 6: The SaaS Triangle

VCs look at three metrics together:

```
Growth (month-over-month)
    | \
    |  \
    |   \
    |    \
    |     \
  Retention ←── Efficiency
(NRR > 100%)  (LTV:CAC > 3:1)

You need all three. Two out of three is not enough.
```

### Diagnostic: Where Are You Weak?

```
Scenario A: High growth, low retention, okay efficiency
→ You're growing fast but customers leave
→ Fix: Focus on product and onboarding, not acquisition

Scenario B: Great retention, low growth, okay efficiency
→ Customers love you but nobody knows you exist
→ Fix: Invest in marketing and distribution

Scenario C: High growth, great retention, low efficiency
→ You could grow faster if you had more capital
→ Fix: Optimize pricing, reduce costs, or raise money

Scenario D: All three strong
→ Series A ready approach investors
```

## The Series A Metrics Package

When approaching investors, have these numbers ready:

### Executive Summary (1 page)

```
Company Metrics Summary

Revenue:
  Current MRR: $XX,XXX
  MRR growth rate (3-month avg): XX% MoM
  ARR: $XX,XXX
  ARR growth (YoY): XXX%

Retention:
  Net Revenue Retention: XXX%
  Gross Revenue Retention: XXX%
  Logo retention (annual): XX%
  Cohort retention (month 6): XX%

Unit Economics:
  Blended CAC: $XXX
  ARPU: $XX/month
  LTV: $X,XXX
  LTV:CAC: X.X:1
  CAC Payback: XX months
  Gross margin: XX%

Market:
  TAM: $XB
  SAM: $XM
  Current market share: X%

Team:
  Team size: X
  Founder: Solo / Multi
  Key hires planned with Series A: X

Traction milestones:
  Month we hit $10K MRR: Month X
  Month we hit $50K MRR: Month X
  Current growth trajectory: $X MRR in 12 months
```

### Supporting Exhibits

For investor data room:

```
Financial:
  P&L statement (last 12 months)
  Revenue by month (since inception)
  Cohort retention table
  Unit economics breakdown

Customer:
  Top 10 customers by revenue
  Customer concentration (% from top 5)
  Logo churn analysis
  NPS survey results
  Testimonial quotes

Product:
  Product roadmap (12 months)
  Feature adoption rates
  Usage data (DAU/MAU, core actions)

Market:
  TAM/SAM/SOM analysis
  Competitive landscape
  Market trends and tailwinds
  Customer interview quotes about the problem
```

## The Solo Founder's Series A Timeline

### 12-18 Months Before Series A

```
Focus: Building the business foundations
- Reach $5-10K MRR with consistent growth
- Establish product-market fit (Sean Ellis 40%+)
- Get first 100 paying customers
- Document your unit economics
- Start tracking ALL metrics weekly
```

### 6-12 Months Before Series A

```
Focus: Building the Fundraising Foundations
- Reach $20-50K MRR
- Build relationships with VCs (don't pitch, just connect)
- Attend industry events (meet investors organically)
- Build in public (gives VCs visibility into your trajectory)
- Refine your narrative and story
- Start reaching out to warm intros
```

### 3-6 Months Before Series A

```
Focus: Fundraising Preparation
- Reach $50-100K MRR (or strong trajectory to get there)
- Prepare pitch deck (10-15 slides)
- Prepare data room
- Build investor target list (50+ VCs)
- Start warm intro process
- Practice pitch with advisors/fellow founders
```

### 1-3 Months Before Series A

```
Focus: Fundraising Execution
- Send warm intros to 10-15 target investors per week
- Nurture relationships with interested investors
- Run the fundraising process (4-8 weeks typically)
- Data room ready for due diligence
- Have answers ready for all common questions
```

## Common Series A Pitfalls

### Pitfall 1: Too Early
"You have $10K MRR and 20% MoM growth. Come back at $50K."
- Growth at small numbers is easier. $10K → $20K is easier than $50K → $100K.
- Wait until you have proven growth at a meaningful scale.

### Pitfall 2: Wrong Metric Mix
"Your NRR is 80%. We need to see 100%+ before we can invest in growth."
- High churn means you're adding customers who'll leave.
- Fix retention before raising.

### Pitfall 3: Small Market
"Your product is great, but it's a feature, not a company."
- If your TAM is under $500M, most VCs will pass.
- Show how you'll expand to adjacent markets.

### Pitfall 4: Founder Dependency
"Your business depends entirely on you. What happens if you get hit by a bus?"
- Build systems, processes, and (ideally) a small team.
- Show that the business can run without you.

### Pitfall 5: Unit Economics Not Improving
"Your LTV:CAC hasn't improved in 12 months."
- Unit economics should improve as you scale (efficiencies of scale).
- If they're not improving, there's a fundamental issue.

### Pitfall 6: No Competitive Moat
"What prevents a well-funded competitor from doing what you do?"
- Network effects, data network effects, brand, regulatory, proprietary tech
- You need at least one credible moat

## Metrics Optimization Action Plan

### Week 1-2: Measure Everything
- [ ] Set up metrics dashboard (Baremetrics, ChartMogul, or custom)
- [ ] Calculate current MRR, growth rate, churn, ARPU
- [ ] Build cohort retention table
- [ ] Calculate CAC, LTV, LTV:CAC, payback period
- [ ] Document TAM/SAM/SOM

### Week 3-4: Analyze Gaps
- [ ] Compare each metric to Series A benchmarks
- [ ] Identify your weakest metrics (below benchmark)
- [ ] Root cause analysis: WHY is this metric weak?
- [ ] Prioritize improvements (biggest impact, least effort)

### Month 2-3: Improve
- [ ] Growth rate below 15%? → Fix acquisition channels
- [ ] NRR below 100%? → Build expansion revenue engine
- [ ] LTV:CAC below 3:1? → Reduce CAC or increase pricing
- [ ] Churn above 5%? → Improve onboarding and product
- [ ] Gross margin below 75%? → Optimize infrastructure costs

### Month 4-6: Prove
- [ ] Maintain improved metrics for 3+ months
- [ ] Show consistent MoM improvement
- [ ] Build narrative around your metric trajectory
- [ ] Test your pitch with warm investor intros

### Month 6-12: Fundraise
- [ ] Metrics consistently at or above benchmarks
- [ ] Clear narrative: big market, strong retention, improving efficiency
- [ ] Warm introductions to 50+ investors
- [ ] Complete data room ready for due diligence
- [ ] Run efficient fundraising process (4-8 weeks)

## Final Thoughts

- **Metrics are not the goal. A great business is the goal.** Metrics are how you know you're building one.
- **Different VCs prioritize different metrics.** Some care most about growth. Others about retention. Know your audience.
- **The best time to start tracking metrics was when you started. The second best time is now.** Even if you're early, start measuring.
- **Investors invest in narratives supported by numbers.** Your story matters as much as your spreadsheet.
- **Your solo founder status is an asset, not a liability.** Capital efficiency, resourcefulness, and deep customer knowledge are hard to replicate.

If your metrics are strong enough for Series A, you've built something real. The funding is just fuel for the engine you've already built.
