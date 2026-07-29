# Market Sizing: TAM, SAM, SOM for Solo SaaS Founders

## Why Market Sizing Matters for Solo Founders

As a solo founder, your most precious resource is time. You cannot afford to build a product for a market that's too small to sustain you or too large to compete in. Market sizing helps you answer the critical question: **Is this opportunity worth my time?**

The goal isn't precision to the dollar — it's directional accuracy. You need to know if the market is $10M or $10B, not whether it's exactly $847M or $852M. This distinction determines your strategy, pricing, and whether you should pursue the idea at all.

## The TAM/SAM/SOM Framework

### TAM (Total Addressable Market)
The total revenue opportunity if you achieved 100% market share. This is the "whole pie."

### SAM (Serviceable Addressable Market)
The segment of TAM you can actually reach with your product and distribution channels. This is the "pie you can technically reach."

### SOM (Serviceable Obtainable Market)
The portion of SAM you can realistically capture in the near term (3-5 years). This is the "pie you can actually eat."

### Real-World Example

**Product:** Project management software for remote design teams

| Metric | Value | How Calculated |
|--------|-------|----------------|
| TAM | $10.5B | Global project management software spend |
| SAM | $1.2B | Project management for design teams (design firms + in-house design teams) |
| SOM | $12M | Realistic capture: 1% of SAM within 5 years |

## Method 1: Top-Down Market Sizing (The Analyst Approach)

### When to Use
- Getting initial industry numbers for your pitch deck or personal conviction
- Understanding the overall market landscape
- Quick sanity checks on market potential

### How to Do It

**Step 1: Find Industry Reports**
```
Sources (free):
- Gartner (free summaries, paid full reports)
- Forrester (same model)
- Statista (many free charts)
- IBISWorld (industry reports, some free)
- Grand View Research (summary data free)
- Verified Market Research (summary data free)
- ReportLinker (aggregates many reports)

Sources (paid, but worth it):
- Gartner subscription ($500-5K/year)
- Forrester subscription ($1-10K/year)
- IDC reports ($2-5K each)
```

**Step 2: Extract Base Numbers**
Example for "API Management Market":
- Gartner says: "API management market to reach $5.1B by 2026"
- Growth rate: 22% CAGR
- Current market: ~$2.5B

**Step 3: Narrow to Your Segment**
If you're building API documentation hosting:
- API management is too broad
- API documentation is a sub-segment: maybe 3-5% of total API management spend
- Estimated: $75-125M SAM for API documentation

**Step 4: Apply Reality Factors**
```
Reality Check Questions:
- What percentage of this market uses paid tools vs free? (Usually 20-40%)
- What percentage is accessible to a new entrant? (Not locked by contracts)
- What percentage is outside enterprise (your target)? (Often 10-30%)
- Are there geographic restrictions? (Can you serve them?)
```

### Top-Down Formula
```
TAM = Industry Report Number

SAM = TAM × Segment Percentage × Accessibility Factor × Geography Factor

SOM = SAM × Realistic Capture Rate (0.5-2% for new entrant)
```

### Top-Down Example: CRM for Real Estate Agents

```
Global CRM Market (Gartner): $80B
Real Estate CRM share (~3%): $2.4B
US Real Estate Agents (150K active): $800M
Entry-level CRM price ($50/mo × 12 months): $600/user/year
CRM software market accessible to startups (50%): $400M
Realistic 5-year capture (3%): $12M
= SOM of $12M/year
```

### Limitations of Top-Down
1. **Too optimistic:** "If we capture 1% of a $1B market" sounds easy but isn't
2. **Garbage in, garbage out:** Industry reports may not reflect your specific niche
3. **Ignores competition:** Doesn't account for existing players
4. **No customer validation:** Based on aggregate data, not real buyer behavior

## Method 2: Bottom-Up Market Sizing (The Founder Approach)

### When to Use
- Building a business case for YOUR specific product
- Convincing yourself (or investors) the opportunity is real
- Creating sales targets and growth projections

### Why Bottom-Up is Better for Solo Founders
Bottom-up uses REAL data — number of potential customers, real prices, and real conversion rates. It forces you to understand your customer acquisition mechanics.

### How to Do It

**Step 1: Define Your Customer Unit**
```
Unit = One customer (could be an individual, company, or account)

Examples:
- A law firm (for legal software)
- A single lawyer (for lawyer-specific tools)
- A company's engineering team (for devtools)
- An e-commerce store (for Shopify apps)
```

**Step 2: Count Potential Customers**
```
Methods to count customers:

Method A: Industry Data
- "There are 350,000 churches in the US" (per IRS data)
- "There are 500,000 construction companies" (per Census Bureau)

Method B: Platform Data
- "There are 2M+ Shopify stores" (Shopify reports)
- "There are 100K+ companies on Stripe" (public filings)

Method C: Bureau of Labor Statistics
- "150,000 physical therapists in the US" (BLS data)
- Can sort by industry, role, geography

Method D: LinkedIn / Job Boards
- Search for titles: "200K+ Project Manager" profiles in US
- Search for company titles: "5,000+ Director of Engineering"

Method E: Trade Association Data
- "3,000 members in the American Society of Interior Designers"
- Usually have industry sizing data
```

**Step 3: Determine Your Addressable Segment**
Not everyone in the total count can use your product:
```
Total Potential Customers: 100,000
× In our target geography: -20% → 80,000
× Have the budget for our price point: -30% → 56,000
× Match our ICP (size, industry, etc.): -40% → 33,600
× Use related tools (integration requirement): -10% → 30,240
= Realistic SAM: 30,000 potential customers
```

**Step 4: Calculate Revenue per Customer**
```
Monthly subscription: $99
Annual revenue per customer: $1,188

BUT: Not all customers stay forever
Average customer lifespan: 24 months
Customer Lifetime Value (LTV): $99 × 24 = $2,376

Revenue per customer per year: $1,188
Revenue per customer (lifetime): $2,376
```

**Step 5: Calculate SOM (What You Can Actually Capture)**
```
Realistic Capture Rates for Solo Founders:
- Year 1: 0.05-0.1% of SAM (very early, learning)
- Year 2: 0.2-0.5% of SAM (product-market fit starting)
- Year 3: 0.5-1% of SAM (growing)
- Year 5: 1-3% of SAM (established player)

Example with 30,000 SAM:
Year 1: 15-30 customers ($18K-$36K ARR)
Year 2: 60-150 customers ($71K-$178K ARR)
Year 3: 150-300 customers ($178K-$356K ARR)
Year 5: 300-900 customers ($356K-$1M+ ARR)
```

### Bottom-Up Formula

```
TAM = Total Possible Customers × Maximum Price

SAM = Addressable Customers × Realistic Price

SOM = SAM × Realistic Capture Rate by Year
```

### Bottom-Up Example: Appointment Scheduling for Boutique Salons

```
Step 1: Count Potential Customers
Boutique hair salons in the US (1-5 stylists): 80,000 (per IBISWorld)
In major metro areas (target first): 30%
= 24,000 in target geographies

Step 2: Addressable Segment
Use technology for booking: 60%
= 14,400
Have budget for software: 50%
= 7,200
Not locked in contract with competitor: 70%
= 5,040

SAM: 5,040 potential customers

Step 3: Revenue Per Customer
Monthly plan: $79
Annual: $948

Step 4: SOM
Year 1: 25 customers ($23,700 ARR)
Year 2: 100 customers ($94,800 ARR)
Year 3: 250 customers ($237,000 ARR)
Year 5: 500 customers ($474,000 ARR)
```

### Bottom-Up Tools and Resources

**Customer Count Research:**
- US Census Bureau Economic Census (census.gov)
- Bureau of Labor Statistics (bls.gov)
- IBISWorld industry reports
- Statista market data
- Trade association membership directories
- Chamber of Commerce directories
- LinkedIn Sales Navigator (filter by company size, industry, role)
- Apollo.io (similar to LinkedIn Sales Nav)
- Crunchbase (for funded companies)

**Price Research:**
- Competitor pricing pages
- G2/Capterra pricing reviews
- Reddit discussions about pricing
- Indie Hackers revenue reports
- SaaS pricing surveys (ProfitWell, ChartMogul publish these)

## Method 3: The Value-Based Approach

### When to Use
- You're selling to businesses (B2B)
- Your product saves or makes money for customers
- The value is quantifiable

### How to Do It

Instead of counting customers, calculate the economic value your product delivers:

**Step 1: Quantify Value Delivered**
```
Product: Automated invoice processing
- Replaces 0.5 FTE (full-time employee) for AP clerk
- Average AP clerk salary: $45,000
- Value: $22,500/year per customer

Product: Lead enrichment tool
- Increases lead conversion by 15%
- Average customer gets 100 leads/month at $50 value each
- Value: 100 × 15% × $50 × 12 = $9,000/year per customer
```

**Step 2: Determine Willingness to Pay**
```
Rule of thumb: Customers will pay 10-20% of value delivered
If you save them $22,500/year:
- They'll pay $2,250-4,500/year
- Monthly: $187-375

If your product costs less, they'll feel like they're stealing
```

**Step 3: Size the Market on Value**
```
Value per customer: $2,500/year (conservative)
Number of target customers: 5,000
Total value available: $12,500,000

Your share (at 30% of value): $3,750,000 potential revenue
Your actual capture (10% market share): $375,000 ARR potential
```

## Market Sizing by Stage

### Pre-Product (Idea Stage)
```
Method: Quick top-down + competitor analysis
Goal: Is the market big enough to pursue?
Time investment: 2-4 hours

Simple test:
1. Google "market size for [your category]"
2. Find 1-2 industry reports
3. Multiply by your segment percentage
4. If TAM > $100M, proceed to validate
```

### Pre-Build (Validation Stage)
```
Method: Detailed bottom-up
Goal: Can this support my target income?
Time investment: 4-8 hours

Key question: How many customers do I need at what price?
If answer is > 1,000 customers at $50/mo, validate further
If answer is < 100 customers at $500/mo, you might have a viable niche
```

### Pre-Launch (Building Stage)
```
Method: Bottom-up with channel analysis
Goal: Can I reach enough customers to grow?
Time investment: 8-16 hours

Channel-Specific SOM:
- Content marketing: 100 visitors/day × 2% conversion = 2 customers/day
- Cold email: 1000 emails × 0.5% conversion = 5 customers
- Partnerships: 10 partners × 5 referrals/month = 50 customers/month
- Paid ads: $1000 spend × $50 CAC = 20 customers
```

### Growth Stage (After Launch)
```
Method: Bottom-up with actual metrics
Goal: What's my realistic growth trajectory?
Data source: Your actual conversion metrics

Example:
- 1000 website visitors/month
- 3% sign up for trial = 30 trials
- 20% convert to paid = 6 customers/month
- $100 MRR per customer average
- = $600 MRR/month new revenue
- + 5% monthly churn on existing revenue
```

## Market Size Minimums for Solo Founders

### The $10K MRR Goal
Minimum viable lifestyle business.

```
At $50/mo: 200 customers
At $100/mo: 100 customers
At $200/mo: 50 customers
At $500/mo: 20 customers
At $1000/mo: 10 customers
```

**Your SAM needs to be at least 3-5x these numbers** to account for conversion rates, churn, and competition.

### The $50K MRR Goal
Solid income + ability to hire.

```
At $50/mo: 1,000 customers
At $100/mo: 500 customers
At $200/mo: 250 customers
At $500/mo: 100 customers
At $1000/mo: 50 customers
```

**Your SAM needs to be at least 1,000-5,000 potential customers.**

### The $100K+ MRR Goal
A serious business (possible acquisition target).

```
At $50/mo: 2,000+ customers
At $100/mo: 1,000+ customers
At $200/mo: 500+ customers
At $500/mo: 200+ customers
```

**Your TAM should be $500M+, SAM should be 10,000+ potential customers.**

## Market Size Red Flags

### Red Flag 1: TAM < $10M
This market is too small. Even at 100% capture, the business won't be meaningful. Unless this is a very high-margin niche with 90%+ profit margins, skip it.

### Red Flag 2: Market is shrinking
SaaS businesses need growing markets. Check:
- Is the industry in decline? (print media, travel agencies)
- Is the problem being solved by technology shifts? (SMS marketing being replaced by messaging apps)
- Are there regulatory threats? (crypto software in uncertain regulatory environments)

### Red Flag 3: Competitors have > 80% market share
If one or two players dominate, breaking in will require massive differentiation or distribution advantage.

### Red Flag 4: You can't find any data
If you can't find any industry data, it might mean the market is too small or too undefined. Proceed with caution.

### Red Flag 5: Your SOM requires 5%+ market share from day one
A new entrant capturing 5%+ of a market in Year 1 is extremely unlikely (outside of truly novel products).

## Market Sizing Spreadsheet Template

Create a spreadsheet with these columns:

| Category | Item | Source | Data |
|----------|------|--------|------|
| TAM | Total market value | Industry report | $500M |
| | | | |
| SAM | Total potential customers | Census/BLS/LinkedIn | 100,000 |
| | Addressable % | Your filters | 30% |
| | Addressable customers | Calculation | 30,000 |
| | Average expected price | Competitor analysis | $99/mo |
| | SAM revenue | Calculation | $35.6M/yr |
| | | | |
| SOM | Year 1 customers | Conservative estimate | 30 |
| | Year 1 ARR | Calculation | $35,640 |
| | Year 3 customers | Growth estimate | 200 |
| | Year 3 ARR | Calculation | $237,600 |
| | Year 5 customers | Stretch estimate | 500 |
| | Year 5 ARR | Calculation | $594,000 |

## Market Sizing by Customer Type

### B2B (Selling to Businesses)

**Advantages for solo founders:**
- Higher willingness to pay ($50-500+/month)
- Fewer customers needed for meaningful revenue
- More rational buying decisions
- Annual contracts available

**Disadvantages:**
- Longer sales cycles
- Multiple decision-makers
- Harder to reach decision-makers
- Higher churn if product doesn't deliver

**Sizing B2B markets:**
```
Number of target companies: 10,000
× Percentage with budget: 40% = 4,000
× Percentage in our geography: 100% (global) = 4,000
× Decision-maker access: 60% = 2,400
= Realistic SAM: 2,400
```

### B2C (Selling to Consumers)

**Advantages for solo founders:**
- Large potential markets
- Short sales cycles
- Viral distribution possible
- Low customer acquisition cost possible (SEO, organic)

**Disadvantages:**
- Very low willingness to pay ($5-15/month typical)
- Need massive scale for meaningful revenue
- High churn
- Compete with free alternatives

**Sizing B2C markets:**
```
Number of target consumers: 5,000,000
× Percentage with the problem: 5% = 250,000
× Percentage willing to pay: 10% = 25,000
= Realistic SAM: 25,000
```

**B2C reality check:**
$5/mo × 25,000 users = $125,000/mo MRR — but you need 25,000 paying users
This requires significant marketing investment or exceptional organic growth

## Geographic Market Sizing

### US-Only vs Global

**US-Only Benefits:**
- Homogeneous market (same language, currency, legal system)
- Higher willingness to pay
- Easier payment processing
- Familiarity

**Global Benefits:**
- Larger TAM
- Less competition in some regions
- 24/7 support coverage opportunity

**When US-Only is sufficient:**
- Niche B2B with 1,000+ US customers
- Revenue target under $2M ARR
- Product requires US-specific compliance (HIPAA, SOC 2)

**When Global is necessary:**
- Consumer product
- Developer tools (global audience)
- Revenue target over $5M ARR
- Small domestic market

## The Solo Founder's Market Sizing Cheat Sheet

### If You Have 30 Minutes
```
1. Google "market size [industry]"
2. Find one industry report number
3. Apply quick segment filter (% of industry)
4. If TAM > $100M → proceed
5. If TAM < $100M → niche too small (unless high-ticket)
```

### If You Have 2 Hours
```
1. Find 3 industry reports (Gartner, Statista, IBISWorld)
2. Build bottom-up customer count (LinkedIn + BLS data)
3. Price your product based on competitor analysis
4. Calculate SAM
5. Build 3-year SOM projection
6. Ensure SOM supports your revenue goals
```

### If You Have 8 Hours (Recommended Before Building)
```
1. Complete top-down analysis (industry reports)
2. Complete bottom-up analysis (customer counts)
3. Value-based analysis (what do you save/make customers?)
4. Channel-specific analysis (how will you reach them?)
5. Competitor revenue estimates (how big are they?)
6. Build 5-year financial projection
7. Sensitivity analysis (what if assumptions are wrong?)
8. Validate with 10+ customer interviews
```

## Market Sizing Pitfalls for Solo Founders

### Pitfall 1: Counting All "Users" as Customers
"Everyone has this problem" is not a market. "5,000 dental practices in California need this" is a market.

### Pitfall 2: Ignoring Free Alternatives
Microsoft Excel, Google Sheets, and manual processes are often your biggest competitor. They are "free" (in terms of software cost).

### Pitfall 3: Overestimating Conversion Rates
A 1% conversion from visitor to paying customer is EXCELLENT in SaaS. Don't plan on 5% or 10%.

### Pitfall 4: Underestimating Churn
20-30% annual churn is normal for small business SaaS. Plan for it.

### Pitfall 5: Ignoring the Competition's Market Share
If Salesforce has 20% of the CRM market, you need to account for their dominance.

### Pitfall 6: Using TAM When You Mean SAM
Your TAM is NOT your market. Your SAM is your market. Use SAM for decision-making.

### Pitfall 7: Not Segmenting by Company Size
A product for "dentists" is different from a product for "dental practices with 5+ dentists." The market size is very different.

## Market Sizing Case Studies

### Case Study 1: ConvertKit (Email Marketing for Creators)

**Top-down analysis:**
- Email marketing market: $10B+
- "Creator" segment: ~2% = $200M
- Accessible (not enterprise): 40% = $80M

**Bottom-up analysis:**
- Professional bloggers/creators: 5M+
- Use email marketing: 30% = 1.5M
- Unsatisfied with current solution: 20% = 300K
- Willing to pay $50/mo: 15% = 45K
- SAM: 45K customers at $50/mo = $27M

**Result:** ConvertKit grew to 30K+ customers, $30M+ ARR. The bottom-up was more accurate.

### Case Study 2: Baremetrics (SaaS Analytics)

**Top-down analysis:**
- Business analytics market: $50B+
- SaaS-specific analytics: 1% = $500M
- Stripe-specific: 10% of SaaS = $50M

**Bottom-up analysis:**
- Companies on Stripe: 200K+
- Need subscription analytics: 30% = 60K
- Use competitor (ChartMogul, etc.): 40% = 24K available
- Willing to pay $100/mo: 20% = 4,800
- SAM: 4,800 customers at $100/mo = $5.76M

**Result:** Baremetrics grew to 3,000+ customers, $3M+ ARR. The bottom-up was more accurate.

### Case Study 3: Carrd (Simple Landing Pages)

**Top-down analysis:**
- Website builder market: $8B+
- "Simple one-page sites": 5% = $400M

**Bottom-up analysis:**
- People who want a single-page site: 50M+
- Willing to pay: 5% = 2.5M
- Pay $19/year average: $47.5M SAM

**Result:** Carrd grew to 200K+ paying users, ~$2M ARR. Note: The bottom-up was too optimistic because Carrd chose a very low price point ($9/year pro). At $9/year, you need 100K+ customers for $1M ARR. But the low price also drove massive adoption.

## Market Sizing Action Plan

### Week 1: Initial Research (2-4 hours)
```
Day 1: Google market size data (3 industry reports)
Day 2: Competitor revenue estimates (Crunchbase, press releases)
Day 3: Build top-down TAM estimate
Day 4: Check if market is growing (Google Trends, CAGR data)
```

### Week 2: Deep Research (4-8 hours)
```
Day 1: Count potential customers (LinkedIn, Census, BLS)
Day 2: Estimate price point (competitor analysis, value calculation)
Day 3: Build bottom-up SAM/SOM
Day 4: Validate with customer interviews (test pricing)
```

### Week 3: Channel Analysis (2-4 hours)
```
Day 1: Estimate reachability (how to contact your market)
Day 2: CAC by channel (content, ads, cold outreach)
Day 3: Growth rate feasibility (can you actually hit your SOM?)
Day 4: Finalize market sizing document
```

## Market Sizing Template

### One-Page Market Sizing Summary

```
Product: [Name]
Target Customer: [Description]

TAM: $[X]M
- Source: [industry report]
- Date: [report date]

SAM: $[X]M
- Calculation: [bottom-up breakdown]
- Number of customers: [count]

SOM (5-year): $[X]M
- Year 1: $[X] ([#] customers)
- Year 2: $[X] ([#] customers)
- Year 3: $[X] ([#] customers)
- Year 4: $[X] ([#] customers)
- Year 5: $[X] ([#] customers)

Key assumptions:
1. [Assumption about market growth]
2. [Assumption about adoption rate]
3. [Assumption about pricing]
4. [Assumption about churn]

Risks:
1. [Risk: market may be smaller than estimated]
2. [Risk: competitors may dominate]
3. [Risk: reachability may be harder than expected]

Verdict: [Proceed / Caution / Skip]
```

## Final Thoughts

Market sizing is not about getting the "right" number. It's about building conviction that there's enough opportunity to justify your time investment. For solo founders, the bar should be higher — your time is too valuable to spend on markets that can't support you.

**The solo founder's market sizing mantra:**

If a market can't support $50K MRR for a capable solo founder, it's not worth pursuing. If it can't support $200K MRR, it might not be worth building defensibly.

But most importantly: market sizing tells you if it's possible. Customer interviews tell you if it's real. Don't skip either step.

**Quick reference — minimum market sizes for solo founders:**

| Goal | Minimum SAM (customers) | Minimum SAM ($) | Minimum Price |
|------|------------------------|-----------------|---------------|
| Side income ($1K MRR) | 200 | $240K/yr | $10/mo |
| Full-time income ($10K MRR) | 500 | $600K/yr | $50/mo |
| Agency-level ($50K MRR) | 2,000 | $2.4M/yr | $99/mo |
| Acquisition target ($100K MRR) | 5,000 | $6M/yr | $99/mo |
| VC-scale ($500K MRR) | 20,000 | $24M/yr | $99/mo |

Size your market. Validate your customers. Build your business.
