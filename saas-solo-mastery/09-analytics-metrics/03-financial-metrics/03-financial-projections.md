# Building Financial Projections for SaaS

A comprehensive guide to creating financial projections for your SaaS business — revenue modeling, expense forecasting, scenario planning, and building a spreadsheet model that grows with you. Essential for fundraising, planning, and staying alive as a solo founder.

---

## Part 1: Why Financial Projections Matter

### The Solo Founder's Financial Reality

```
A financial projection is not a prediction of the future.
It's a planning tool for TODAY'S decisions.
```

Without projections:
- You don't know if you'll run out of cash in 6 months
- You can't evaluate whether spending $500 on ads is worth it
- You have no benchmark to measure actual performance against
- You can't answer "how much do I need to raise?" with confidence

### What Projections Enable

1. **Cash management** — Know when you'll need more money
2. **Decision support** — Run scenarios before committing resources
3. **Fundraising** — Show investors you understand your business
4. **Goal setting** — Create concrete targets to work toward
5. **Early warning** — Detect when reality diverges from plan

### The Three Horizon Framework

```
Horizon 1: Tactical (Next 90 Days)
  - Weekly cash flow forecast
  - Monthly revenue by segment
  - Expense tracking against budget
  - Accuracy target: ±10%

Horizon 2: Strategic (Next 12 Months)
  - Monthly P&L projections
  - Headcount planning
  - Capital requirements
  - Accuracy target: ±20%

Horizon 3: Vision (Next 3-5 Years)
  - Annual revenue model
  - Fundraising timing
  - Exit scenarios
  - Accuracy target: ±50% (directionally correct)
```

---

## Part 2: Revenue Modeling

### The Revenue Build-Up

A proper SaaS revenue model is a "bottom-up" build, not a single growth rate applied to last month's MRR.

```
MRRThis Month = MRRLast Month + New MRR + Expansion MRR - Churn MRR - Contraction MRR
```

### Component: New MRR Forecast

**Method 1: Top-down (simple but less accurate)**
```
New MRR = (Target New Customers) × (Average ARPU)
```

**Example:**
```
January: 20 new customers × $50 ARPU = $1,000 new MRR
February: 22 new customers × $50 ARPU = $1,100 new MRR
March: 24 new customers × $52 ARPU = $1,248 new MRR (price increase)
```

**Method 2: Bottom-up (more accurate, channel-based)**
```
New MRR = Sum of (Channel Leads × Conversion Rate × ARPU) for each channel
```

**Example:**
```
Channel      | Leads | Conv Rate | Customers | ARPU  | New MRR
Organic      | 200   | 3%        | 6         | $49   | $294
Google Ads   | 150   | 4%        | 6         | $49   | $294
Content      | 80    | 5%        | 4         | $49   | $196
Referrals    | 40    | 20%       | 8         | $49   | $392
Total        | 470   | 5.1%      | 24        | $49   | $1,176
```

**Method 3: Historical Trend (when you have 6+ months of data)**
```
New MRR = Average of last 3 months' New MRR × Growth Factor
Growth Factor = (New MRR Last Month / New MRR 3 Months Ago) ^ (1/3)
```

### Component: Expansion MRR

Expansion comes from:
1. Plan upgrades (basic → pro, monthly → annual)
2. Usage-based overage fees
3. Additional seats/team members
4. Add-on purchases

**Simple expansion model:**
```
Expansion MRR = (Starting Customers × Upgrade Rate × Additional ARPU) + 
                (Starting Customers × Seat Expansion Rate × Per-Seat Price)
```

**Example:**
```
1,000 starting customers
5% upgrade per month → 50 upgrades
Upgrade delta: $49 → $99 = $50 additional ARPU
Expansion MRR = 50 × $50 = $2,500
```

### Component: Churn MRR

**Simple churn model:**
```
Churn MRR = Starting MRR × Monthly Revenue Churn Rate
```

**Better churn model (by segment):**
```
Churn MRR = (Self-serve MRR × 6% churn) + (Pro MRR × 4% churn) + (Enterprise MRR × 1.5% churn)
```

**Cohort-based churn (most accurate):**
```
For each historical cohort:
  Churn MRR this month = Cohort MRR × Cohort-specific churn rate
Total Churn MRR = Sum of all cohort churn
```

### Complete Revenue Model in Spreadsheet

```yaml
MONTHLY REVENUE MODEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INPUTS:
  Starting MRR: $10,000 (January)
  Starting Customers: 200

GROWTH ASSUMPTIONS:
  New Customers (monthly growth): 5% MoM
  ARPU: $50 (fixed)
  Monthly Churn: 5%
  Upgrade Rate: 2% of existing customers per month
  Upgrade Delta: $40 (basic → pro price difference)
  Annual Conversion Rate: 10% of new customers (pay annual)

PROJECTIONS:

Month  | Starting MRR | New MRR | Expansion | Churn | Ending MRR | Growth%
-------|-------------|---------|-----------|-------|------------|--------
Jan    | $10,000      | $1,000  | $400      | $500  | $10,900    | 9.0%
Feb    | $10,900      | $1,050  | $436      | $545  | $11,841    | 8.6%
Mar    | $11,841      | $1,103  | $474      | $592  | $12,826    | 8.3%
Apr    | $12,826      | $1,158  | $513      | $641  | $13,856    | 8.0%
May    | $13,856      | $1,216  | $554      | $693  | $14,933    | 7.8%
Jun    | $14,933      | $1,277  | $597      | $747  | $16,060    | 7.5%
Jul    | $16,060      | $1,340  | $642      | $803  | $17,239    | 7.3%
Aug    | $17,239      | $1,407  | $690      | $862  | $18,474    | 7.2%
Sep    | $18,474      | $1,478  | $739      | $924  | $19,767    | 7.0%
Oct    | $19,767      | $1,552  | $791      | $988  | $21,122    | 6.9%
Nov    | $21,122      | $1,629  | $845      | $1,056 | $22,540   | 6.7%
Dec    | $22,540      | $1,711  | $902      | $1,127 | $24,026   | 6.6%

Year End ARR: $288,312
Year over Year Growth: 140%
```

**Spreadsheet formulas:**
```
Cell "Starting MRR" = Previous month's "Ending MRR"
Cell "New MRR" = New_Customers × ARPU  (or channel model)
Cell "Expansion" = Starting Customers × Upgrade_Rate × Upgrade_Delta
Cell "Churn" = Starting MRR × Churn_Rate
Cell "Ending MRR" = Starting_MRR + New_MRR + Expansion_MRR - Churn_MRR
Cell "Growth%" = (Ending_MRR - Starting_MRR) / Starting_MRR
```

### Annual Revenue Forecasting

For investor presentations, show annual projections:

```yaml
Year 1    | Year 2    | Year 3    | Year 4    | Year 5
$200K ARR | $500K ARR | $1.2M ARR | $2.5M ARR | $5M ARR
```

**Rule of thumb for early-stage SaaS:**
- Year 1: $50K - $200K ARR (solo founder range)
- Year 2: 2-3x Year 1 ($100K - $600K)
- Year 3: 2-2.5x Year 2 ($200K - $1.5M)
- Year 4: 1.5-2x Year 3
- Year 5: 1.5-2x Year 4

### Revenue Model Sensitivity Table

Create a sensitivity table showing ARR under different assumptions:

```yaml
ARR at Year 3
              | New Customers (Monthly Growth)
Churn Rate    | 2%     | 5%     | 8%     | 12%
--------------|--------|--------|--------|--------
3%            | $450K  | $720K  | $1.1M  | $1.8M
5%            | $320K  | $510K  | $780K  | $1.3M
7%            | $230K  | $370K  | $560K  | $920K
10%           | $150K  | $240K  | $370K  | $600K
```

**Formula for each cell (simplified):**
```
= Starting_MRR × (1 + Monthly_Growth_Rate - Churn_Rate) ^ 36
```

This shows the enormous impact of churn on your final ARR. At 12% growth and 10% churn, you still grow (net 2% per month). At 5% growth and 7% churn, you shrink!

---

## Part 3: Expense Forecasting

### The SaaS Cost Structure

```
Revenue
  - COGS (Infrastructure, APIs, Payment Processing, Support)
  = Gross Profit
  - R&D (Development Tools, Engineering Salaries if any)
  - Sales & Marketing (Ads, Content, Tools)
  - G&A (Legal, Accounting, Insurance, Software)
  = Operating Income (EBITDA)
```

### Fixed vs. Variable Costs

| Cost Type | Examples | Behavior |
|-----------|----------|----------|
| Fixed | Accounting, legal, insurance, tools | Stay constant regardless of revenue |
| Semi-fixed | Infrastructure base tier, support tools | Step up at certain thresholds |
| Variable | Cloud hosting usage, APIs, payment fees | Scale with revenue/usage |
| Growth-variable | Ad spend, content production | Scales with growth plans |

### Expense Categories for Solo Founders

#### COGS (5-20% of revenue)

```yaml
Category            | % of Revenue | Example Costs
Infrastructure      | 5-15%        | Cloud hosting, CDN, database
Third-party APIs    | 2-8%         | AI APIs, data providers, email
Payment Processing  | 3-5%         | Stripe fees (2.9% + $0.30)
Customer Support    | 2-5%         | Intercom/Crisp, help desk
Total COGS          | 12-33%       | Target: < 20% of revenue
```

**Forecasting COGS:**
```
Infrastructure Cost = Base_Cost + (Variable_Cost_per_Customer × Customers)
Payment Processing = Revenue × 0.029 + (Transactions × 0.30)
API Costs = Usage_Volume × Per_Unit_Cost
```

#### R&D (20-40% of revenue)

```yaml
Category              | Monthly Cost | Notes
Development Tools     | $50-200      | GitHub Copilot, IDE, testing
Design Tools          | $20-50       | Figma, Canva
Domain & DNS          | $10-20       | Namecheap, Cloudflare
Your Time (as cost)   | $0           | Don't assign salary to R&D
Total (solo)          | $80-270      |
```

#### Sales & Marketing (10-50% of revenue)

```yaml
Category              | Monthly Cost | Notes
Advertising           | $0-5,000     | Google Ads, LinkedIn, Twitter
Content Production    | $0-1,000     | Freelancers, tools
Email Marketing       | $30-100      | ConvertKit, Mailchimp
CRM                   | $0-30        | Pipedrive, HubSpot free
SEO Tools             | $0-100       | Ahrefs, Semrush (free tiers)
Total (solo)          | $30-6,230    |
```

#### G&A (5-15% of revenue)

```yaml
Category              | Monthly Cost | Notes
Accounting            | $50-300      | QuickBooks, Wave, Bench
Legal                 | $0-500       | Retainers, contract review
Insurance             | $50-200      | E&O, general liability
Banking Fees          | $10-30       | Mercury, Brex
Your Tools            | $50-200      | Notion, Slack, Google Workspace
Total (solo)          | $160-1,230   |
```

### Complete Expense Model

```yaml
MONTHLY EXPENSE MODEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Month  | COGS  | R&D    | S&M    | G&A    | Total  | % of Revenue
-------|-------|--------|--------|--------|--------|------------
Jan    | $800  | $200   | $1,500 | $500   | $3,000 | 27.5%
Feb    | $850  | $200   | $1,500 | $500   | $3,050 | 25.7%
Mar    | $900  | $200   | $1,800 | $500   | $3,400 | 26.5%
Apr    | $950  | $200   | $1,800 | $500   | $3,450 | 24.9%
May    | $1,000| $200   | $2,000 | $500   | $3,700 | 24.8%
Jun    | $1,050| $200   | $2,000 | $500   | $3,750 | 23.4%
Jul    | $1,150| $300   | $2,500 | $700   | $4,650 | 27.0% (hire contractor)
Aug    | $1,200| $300   | $2,500 | $700   | $4,700 | 25.4%
Sep    | $1,300| $300   | $3,000 | $700   | $5,300 | 26.8%
Oct    | $1,400| $300   | $3,000 | $700   | $5,400 | 25.6%
Nov    | $1,500| $300   | $3,500 | $700   | $6,000 | 26.6%
Dec    | $1,600| $300   | $3,500 | $700   | $6,100 | 25.4%
```

**Spreadsheet formulas:**
```
COGS = Revenue × Target_COGS_Percentage
R&D = Fixed cost (update when you add tools/hire)
S&M = Base spend + (Growth_Spend based on plan)
G&A = Fixed cost + step changes for new services
Total = SUM of all categories
% of Revenue = Total / Revenue
```

---

## Part 4: The Full P&L Projection

### Combined P&L Model

```yaml
PROJECTED MONTHLY P&L (Year 1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                      | Jan    | Feb    | Mar    | Q1     | ...
REVENUE               |        |        |        |        |
  Subscription        | $10,900| $11,841| $12,826| $35,567|
  Other               | $0     | $0     | $0     | $0     |
  Total Revenue       | $10,900| $11,841| $12,826| $35,567|

COGS                  |        |        |        |        |
  Infrastructure      | $545   | $592   | $641   | $1,778 |
  Payment Processing  | $316   | $343   | $372   | $1,031 |
  Support Tools       | $30    | $30    | $30    | $90    |
  Total COGS          | $891   | $965   | $1,043 | $2,899 |

GROSS PROFIT          | $10,009| $10,876| $11,783| $32,668|
GROSS MARGIN          | 91.8%  | 91.8%  | 91.9%  | 91.8%  |

OPEX                  |        |        |        |        |
  R&D                 | $200   | $200   | $200   | $600   |
  Sales & Marketing   | $1,500 | $1,500 | $1,800 | $4,800 |
  G&A                 | $500   | $500   | $500   | $1,500 |
  Total OpEx          | $2,200 | $2,200 | $2,500 | $6,900 |

EBITDA                | $7,809 | $8,676 | $9,283 | $25,768|
EBITDA MARGIN         | 71.6%  | 73.3%  | 72.4%  | 72.4%  |

CASH FLOW ITEMS       |        |        |        |        |
  Annual Prepayments  | +$2,000| +$2,500| +$3,000| +$7,500|
  Deferred Revenue Δ  | +$1,800| +$2,300| +$2,700| +$6,800|
  Capital Expenditure | $0     | $0     | $0     | $0     |

NET CASH FLOW         | +$9,609| +$10,976|+$12,283|+$32,868|
```

### Key Formulas in the P&L

```
Gross Margin = Gross Profit / Total Revenue × 100
Operating Margin (EBITDA %) = EBITDA / Total Revenue × 100
Net Cash Flow = EBITDA + Non-cash adjustments + Working capital changes
```

---

## Part 5: Cash Flow Projection

### The Critical Model

For solo founders, cash flow is more important than the P&L. You can be profitable on paper and still go bankrupt (because customers pay annually but you need cash NOW).

### Cash Flow Model Structure

```yaml
CASH FLOW PROJECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Month | Starting Cash | Inflows | Outflows | Ending Cash
------|---------------|---------|----------|------------
Jan   | $50,000       | $12,900 | $3,091   | $59,809
Feb   | $59,809       | $14,341 | $3,165   | $70,985
Mar   | $70,985       | $15,826 | $3,543   | $83,268
Apr   | $83,268       | $16,856 | $3,595   | $96,529
May   | $96,529       | $17,933 | $3,845   | $110,617
Jun   | $110,617      | $18,060 | $3,895   | $124,782
...
Dec   | $200,000      | $25,000 | $6,500   | $218,500
```

**Cash inflows include:**
- Monthly subscription payments (collected this month)
- Annual prepayments (collected upfront)
- Interest income

**Cash outflows include:**
- All expenses (when paid, which may differ from when incurred)
- Tax payments (quarterly estimated taxes)
- Capital expenditures (equipment, computers)
- Founder draws/salary

### Cash Flow vs. P&L Reconciliation

The difference between cash flow and P&L is driven by:

```yaml
Difference = Cash Basis Profit - Accrual Basis Profit

Sources of difference:
  + Annual prepayments collected (cash in, not revenue yet)
  - Deferred revenue earned (revenue, not cash this month)
  + Prepaid expenses paid (cash out, not expense yet)
  - Expenses accrued (expense, not cash yet)
  + Accounts receivable paid (cash for previous revenue)
  - Capital expenditures (cash out, not expense — capitalized)
```

### Minimum Cash Reserve

**Rule of thumb for solo founders:**
```
Minimum Cash = 6 months of expenses + 1 month of revenue (paid in advance)
```

**Why:**
- You need 6 months to find new customers if growth stops
- You need to cover refunds if something goes wrong
- You need to cover your own living expenses for at least 6 months
- You need buffer for unexpected expenses (legal, compliance, downtime)

### Cash Flow Warning Levels

```yaml
Cash Balance / Monthly Burn     | Status      | Action Required
12+ months                      | Safe        | Grow aggressively
8-12 months                     | Comfortable | Maintain growth rate
6-8 months                      | Caution     | Cut costs, boost revenue
4-6 months                      | Warning     | Urgent action needed
2-4 months                      | Critical    | Survival mode
< 2 months                      | Emergency   | Sell, merge, or shut down
```

---

## Part 6: Scenario Planning

### The Three-Scenario Model

Every projection should have three versions:

#### 1. Base Case (Realistic)

```
Based on your current trajectory with conservative improvement.
You believe you can achieve this if nothing major changes.
```

**Assumptions:**
```
5% MoM customer growth
5% monthly churn (improving to 4% over 12 months)
$50 ARPU
3% expansion MRR per month
$3,000/month S&M spend
```

**Outcome:** $24K MRR at end of year, cash positive from month 3.

#### 2. Upside Case (Optimistic)

```
Based on your best possible execution.
You need things to go right, but it's achievable.
```

**Assumptions:**
```
8% MoM customer growth
4% monthly churn (improving to 3%)
$55 ARPU (price increase in month 6)
4% expansion MRR
$5,000/month S&M spend (increased investment)
```

**Outcome:** $35K MRR at end of year, cash positive from month 1 (due to growth justifying S&M).

#### 3. Downside Case (Pessimistic)

```
Based on what happens if things go wrong.
This is your "survive" scenario.
```

**Assumptions:**
```
3% MoM customer growth
6% monthly churn (worsening due to competition)
$45 ARPU (discounting to retain customers)
1% expansion MRR
$1,500/month S&M spend (cut back)
```

**Outcome:** $15K MRR at end of year, need additional capital by month 8.

### Scenario Decision Framework

```yaml
Scenario         | If This Happens      | I Will Do This
─────────────────|──────────────────────|────────────────
Upside           | Exceeding growth     | Invest more in S&M, hire earlier
Base             | On track             | Execute the plan, optimize
Downside         | Missing targets      | Cut S&M by 50%, extend runway
Catastrophe      | Product failure      | Pivot, consult, or go part-time
```

### Scenario Planning in Spreadsheets

Create a "Scenario Manager" sheet:

```yaml
SCENARIO INPUTS
              | Base | Upside | Downside
MoM Growth    | 5%   | 8%     | 3%
Churn Rate    | 5%   | 4%     | 6%
ARPU          | $50  | $55    | $45
Expansion     | 3%   | 4%     | 1%
S&M Spend     | $3K  | $5K    | $1.5K

SCENARIO OUTPUTS (Month 12)
              | Base    | Upside   | Downside
MRR           | $24,026 | $35,210  | $15,440
ARR           | $288K   | $423K    | $185K
Cash Balance  | $218K   | $285K    | $85K
Profitability | Profitable| Profitable| Marginal
Need Raise?   | No      | No       | Yes, by Month 8
```

**How to build:**
1. Create input cells for each assumption
2. Reference input cells in all projection formulas
3. Use a dropdown or button to switch scenarios
4. All formulas update automatically

### Stress Testing

Ask "what if" questions and model the impact:

```
What if our largest customer (5% of MRR) churns?
  → MRR drops by 5% immediately
  → Impact: Lose 2 months of growth
  → Action: Diversify customer base

What if Stripe increases fees to 3.5% + $0.50?
  → COGS increases by 0.6% of revenue
  → Gross margin drops from 80% to 79.4%
  → Impact: Small but cumulative
  → Action: Consider alternative processor or negotiate

What if Google changes algorithm and organic traffic drops 50%?
  → New signups from organic drop from 20 to 10 per month
  → New MRR drops by $500/month
  → Impact: Growth slows from 8% to 5% MoM
  → Action: Diversify acquisition channels NOW
```

---

## Part 7: Building the Projection Model

### The Structure

Create a spreadsheet with these sheets:

```
Sheet 1: Dashboard
  - Summary of key outputs
  - MRR chart, cash balance chart
  - Scenario comparison
  
Sheet 2: Assumptions
  - All input variables
  - Growth rates, churn, ARPU, expenses
  - Scenario selector
  
Sheet 3: Revenue Model
  - Monthly MRR build-up
  - New customers by channel
  - Churn and expansion detail
  
Sheet 4: P&L Projection
  - Monthly income statement
  - Gross margin, operating margin
  
Sheet 5: Cash Flow
  - Monthly cash statement
  - Runway calculation
  - Capital needs

Sheet 6: Unit Economics
  - LTV, CAC, payback over time
  - Channel economics
  
Sheet 7: Scenarios
  - Base, Upside, Downside comparison
```

### Key Excel/Sheets Formulas

```excel
'Revenue Model Sheet'

Cell B5 (Starting MRR this month): 
  =H5 (Ending MRR from previous month)

Cell C5 (New Customers): 
  =Previous_Customers * Assumptions!$B$3 (growth rate)

Cell D5 (New MRR): 
  =C5 * Assumptions!$B$5 (ARPU)

Cell E5 (Expansion MRR): 
  =(B5 / Assumptions!$B$5) * Assumptions!$B$7 (expansion rate * upgrade delta)

Cell F5 (Churn MRR): 
  =B5 * Assumptions!$B$4 (churn rate)

Cell G5 (Contraction MRR): 
  =B5 * Assumptions!$B$8 (downgrade rate)

Cell H5 (Ending MRR): 
  =B5 + D5 + E5 - F5 - G5
```

### Projection Automation

For technical founders, automate data flow:

```python
# Python script to pull actual data and update projections
import stripe
import gspread
from datetime import datetime, timedelta

# Connect to Stripe
stripe.api_key = "sk_live_..."

# Connect to Google Sheets
gc = gspread.service_account(filename='credentials.json')
sh = gc.open('SaaS Projections')
worksheet = sh.worksheet('Actuals')

# Pull actual MRR for last month
def get_actual_mrr():
    # Get all active subscriptions
    subscriptions = stripe.Subscription.list(status='active')
    total_mrr = 0
    
    for sub in subscriptions.auto_paging_iter():
        if sub.status == 'active':
            # Calculate MRR (normalized to monthly)
            if sub.items.data[0].price.recurring.interval == 'month':
                total_mrr += sub.items.data[0].price.unit_amount / 100
            elif sub.items.data[0].price.recurring.interval == 'year':
                total_mrr += (sub.items.data[0].price.unit_amount / 100) / 12
    
    return round(total_mrr, 2)

# Update sheet with actuals
actual_mrr = get_actual_mrr()
last_month = (datetime.now() - timedelta(days=30)).strftime('%b')
worksheet.update(f'B{last_month}', actual_mrr)

# Update forecast based on actuals
current_forecast = worksheet.acell('Forecast_MRR').value
if abs(actual_mrr - float(current_forecast)) / float(current_forecast) > 0.2:
    # Deviation > 20% — flag for review
    worksheet.update('Alert', 'Deviation > 20% — review assumptions')
```

---

## Part 8: Investor-Grade Projections

### What Investors Look For

When reviewing your projections, investors check:

1. **Is the model internally consistent?**
   - New customers × ARPU = New MRR
   - MRR × 12 = ARR
   - Churn and growth assumptions are reasonable

2. **Are the assumptions defensible?**
   - 5% weekly growth for 3 years = 140,000% growth — that's not happening
   - Your churn assumptions match industry benchmarks for your segment

3. **Does the founder understand the business?**
   - Can they explain the key drivers?
   - Do they know what would break the model?
   - Are there logical expense step-changes at revenue milestones?

4. **Is there a clear path to profitability?**
   - When does EBITDA turn positive?
   - How much capital is needed to get there?
   - What's the payback period on that capital?

### Fundraising Projection Template

```yaml
INVESTOR PROJECTION MODEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5-Year Revenue Model:
             | Year 0 | Year 1 | Year 2 | Year 3 | Year 4 | Year 5
Customers    | 200    | 500    | 1,500  | 4,000  | 10,000 | 22,000
ARPU         | $50    | $55    | $60    | $65    | $70    | $75
MRR          | $10K   | $27.5K | $90K   | $260K  | $700K  | $1.65M
ARR          | $120K  | $330K  | $1.08M | $3.12M | $8.4M  | $19.8M
YoY Growth   | ---    | 175%   | 227%   | 189%   | 169%   | 136%

Key Metrics:
  Gross Margin      | 75%    | 78%    | 80%    | 82%    | 83%    | 85%
  S&M % of Revenue  | 60%    | 50%    | 40%    | 35%    | 30%    | 25%
  R&D % of Revenue  | 40%    | 30%    | 25%    | 20%    | 18%    | 15%
  G&A % of Revenue  | 20%    | 15%    | 12%    | 10%    | 8%     | 7%
  EBITDA Margin      | -45%   | -17%   | 3%     | 17%    | 27%    | 38%

Capital Requirements:
  Seed Round: $500K (Year 0)
  Series A: $3M (Year 2 — at $1M+ ARR)
  Break-even: Year 2, Month 8
```

### The "Hockey Stick" Trap

Don't project unrealistic growth. Investors have seen thousands of models and know what's reasonable.

**Red flags:**
- 20%+ MoM growth for 3 years straight (impossible — base effects)
- Zero churn assumption (nobody has zero churn)
- Linear customer acquisition growth (it compounds or it doesn't)
- ARPU that doubles every year (without explaining HOW)

**Realistic growth curves:**
```
Good: 10% MoM for 12 months → 5% MoM for 12 months → 3% MoM thereafter
Great: 15% MoM for 6 months → 10% MoM for 12 months → 5% thereafter  
Unicorn: 20% MoM for 12 months → 15% MoM for 12 months → 8% thereafter
```

---

## Part 9: Review Cadence

### Weekly: 15 Minutes

```yaml
Friday afternoon:

1. Check actual MRR vs projected MRR (is it close?)
2. Check cash balance (any surprise charges?)
3. Check burn rate (are we spending more than planned?)
4. Note any deviation > 10% for investigation next week
```

### Monthly: 1 Hour

```yaml
First week of the month:

1. Update all actuals (revenue, expenses, customers)
2. Compare actuals to projections (variance analysis)
3. Update assumptions for the next 3 months based on actuals
4. Check runway — has it changed?
5. Run 3 scenarios with actual data
6. Identify top risk to the plan
7. Update action items to address risk
```

### Quarterly: 2 Hours

```yaml
End of quarter:

1. Full review of all assumptions
2. Rebuild projections for next 4 quarters
3. Review and update expense budget
4. Update fundraising plan (if applicable)
5. Run sensitivity analysis on top 5 risks
6. Create "lessons learned" from last quarter
7. Set specific financial goals for next quarter
```

### Annual: 4 Hours

```yaml
End of fiscal year:

1. Complete annual review of all projections vs. actuals
2. Build new 12-month projection (bottom-up)
3. Build 3-year strategic projection
4. Update fundraising strategy
5. Review pricing model
6. Review expense efficiency
7. Set company OKRs tied to financial model
8. Share updated model with advisors/board
```

---

## Part 10: Common Mistakes

### Mistake 1: Only Modeling the Upside

**Problem:** You project 20% MoM growth for 2 years straight because "we'll figure it out."

**Reality:** You hit 8% in month 1, 5% in month 3, and 2% in month 6. You're out of cash by month 8.

**Fix:** Always model the downside case. Plan to survive that.

### Mistake 2: Forgetting Non-Recurring Expenses

**Problem:** You model $3K/month in expenses forever.

**Reality:** You need a new computer ($2K), legal fees for entity setup ($2K), trademark filing ($1K), first hire interview costs...

**Fix:** Add 15% buffer to your expense forecast for "unexpected but inevitable" costs.

### Mistake 3: Linear Customer Growth

**Problem:** You add 50 customers every month, every month.

**Reality:** Customer acquisition compounds (or saturates). New channels have startup time. Organic SEO takes 6-12 months.

**Fix:** Model channel growth with realistic ramp times.

### Mistake 4: Static ARPU

**Problem:** You keep ARPU flat for 3 years.

**Reality:** You'll raise prices, introduce tiers, and add features. ARPU should increase 10-20% per year for a healthy SaaS.

**Fix:** Model ARPU growth tied to product milestones.

### Mistake 5: Ignoring Deferred Revenue

**Problem:** You treat all cash received as revenue.

**Reality:** Annual prepayments are liabilities. If you spend them, you're in trouble.

**Fix:** Show both cash basis and accrual basis projections.

### Mistake 6: Building It Once and Never Updating

**Problem:** You built a beautiful model in January. It's June and you haven't looked at it since.

**Reality:** The model is now completely useless — actuals diverged from projections months ago.

**Fix:** Update actuals monthly and revisit assumptions quarterly.

---

## The Complete Financial Model Template

Download this structure for your own model:

```yaml
Sheet: Dashboard
  Cells:
    B2: Current MRR (actual)
    B3: Month-over-Month Growth
    B4: Current ARR
    B5: Cash Balance
    B6: Monthly Burn Rate
    B7: Runway (months)
    B8-12: Key Metrics (from Unit Economics sheet)
    B14-25: Current Month vs Projected (variance)
  
  Chart 1: MRR — Actual vs Projected (line chart)
  Chart 2: Cash Balance Projection (area chart)
  Chart 3: Monthly Growth Rate (bar chart)

Sheet: Assumptions (Input everything here)

Sheet: Revenue Model (12-36 months)

Sheet: P&L (12-36 months)

Sheet: Cash Flow (12-36 months)

Sheet: Unit Economics (monthly over forecast period)

Sheet: Funding Needs (if applicable)

Sheet: Scenarios (Base, Upside, Downside side-by-side)
```

### Final Advice

> **Your financial model is never right. But that's not the point.**
> The point is that you have a framework for thinking about the future,
> a way to measure your performance, and a tool for making decisions.

Build the model. Review it weekly. Update it monthly. Challenge it quarterly. And when reality diverges from the model (it will), learn why and adjust.