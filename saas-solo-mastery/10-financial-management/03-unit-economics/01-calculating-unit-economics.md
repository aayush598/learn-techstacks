# Calculating Unit Economics for SaaS

A step-by-step guide to calculating every unit economic metric for your SaaS business, with spreadsheet templates, formulas, and real examples. This is the math that determines whether your business works.

---

## Part 1: The Raw Data You Need

### Before You Calculate Anything

Collect these data points from your business:

```yaml
Monthly Data (export from Stripe/accounting):
  1. Total revenue (MRR)
  2. Number of paying customers (by plan)
  3. New customers this month (by channel)
  4. Churned customers this month
  5. Upgraded customers this month
  6. Downgraded customers this month
  7. Total sales & marketing spend
  8. Infrastructure costs
  9. Payment processing fees
  10. Customer support costs

One-Time Data:
  11. Customer creation dates (for cohort analysis)
  12. Customer cancellation dates
  13. Lifetime revenue per customer (longitudinal)
```

### The Data Template (Google Sheets)

Create this sheet:

```yaml
RAW DATA SHEET

Month    | MRR     | Customers | New     | Churned | Upgraded | S&M Spend | COGS
─────────|─────────|───────────|─────────|─────────|──────────|───────────|─────────
Jan 2024 | $10,000 | 200       | 20      | 10      | 5        | $3,000    | $2,000
Feb 2024 | $10,800 | 215       | 22      | 9       | 6        | $3,200    | $2,100
Mar 2024 | $11,800 | 232       | 24      | 8       | 7        | $3,400    | $2,300
Apr 2024 | $12,900 | 250       | 26      | 9       | 7        | $3,600    | $2,500
May 2024 | $14,100 | 270       | 28      | 10      | 8        | $3,800    | $2,700
Jun 2024 | $15,400 | 292       | 30      | 10      | 9        | $4,000    | $3,000
```

---

## Part 2: Revenue Metrics

### Calculation 1: MRR

```yaml
FORMULA:
  MRR = Sum of all monthly subscription fees

For monthly plans:
  MRR = SUM of all active subscriptions' monthly amounts

For annual plans:
  MRR = SUM of (Annual Contract Value / 12) for all active subscriptions

For usage-based:
  MRR = Average of last 3 months' usage revenue

EXCEL/SHEETS FORMULA:
  =SUMIFS(Subscriptions!E:E, Subscriptions!F:F, ">=Start_Date", Subscriptions!G:G, "active")
```

### Calculation 2: MRR Growth Rate

```yaml
FORMULA:
  MRR Growth Rate (%) = (Current Month MRR - Previous Month MRR) / Previous Month MRR × 100

EXAMPLE:
  June MRR: $15,400
  May MRR: $14,100
  Growth: ($15,400 - $14,100) / $14,100 × 100 = 9.2%

EXCEL/SHEETS:
  =(B7 - B6) / B6 * 100
```

### Calculation 3: MRR Breakdown

```yaml
New MRR = MRR from new customers this month
Expansion MRR = Additional MRR from upgrades (delta between old and new plan prices)
Churn MRR = MRR lost from customers who canceled
Contraction MRR = MRR lost from downgrades

Formula for each:
  New MRR = Number of new customers × Average new customer price
  Expansion MRR = SUM of (New Plan Price - Old Plan Price) for upgraded customers
  Churn MRR = SUM of churned customers' last MRR contribution
  Contraction MRR = SUM of (Old Plan Price - New Plan Price) for downgraded customers
  
Net New MRR = New MRR + Expansion MRR - Churn MRR - Contraction MRR

EXCEL:
  Net New MRR = New_MRR + Expansion_MRR - Churn_MRR - Contraction_MRR
  MRR Growth % = Net New MRR / Previous Month's MRR × 100
```

### Calculation 4: ARR

```yaml
FORMULA:
  ARR = MRR × 12

EXAMPLE:
  MRR: $15,400
  ARR: $15,400 × 12 = $184,800

EXCEL:
  =MRR * 12
```

### Calculation 5: ARPU (Average Revenue Per User)

```yaml
FORMULA:
  ARPU = MRR / Total Number of Paying Customers

EXAMPLE:
  MRR: $15,400
  Customers: 292
  ARPU: $15,400 / 292 = $52.74

EXCEL:
  =MRR / Total_Customers
```

### Calculation 6: ARPU by Plan

```yaml
FORMULA:
  ARPU per Plan = MRR from Plan / Number of Customers on Plan

EXAMPLE:
  Basic Plan: 200 customers × $29/month = $5,800 MRR → ARPU = $29
  Pro Plan: 80 customers × $79/month = $6,320 MRR → ARPU = $79
  Enterprise: 12 customers × $299/month = $3,588 MRR → ARPU = $299
  
  Blended ARPU: $15,708 / 292 = $53.79
  
EXCEL:
  =SUMIFS(MRR_Data, Plan_Column, "Pro") / COUNTIFS(Customer_Data, Plan_Column, "Pro")
```

---

## Part 3: Customer Metrics

### Calculation 7: New Customers

```yaml
FORMULA:
  New Customers = Count of customers who made their FIRST payment this month

EXCEL:
  =COUNTIFS(Customer_Data!A:A, ">="&Month_Start, Customer_Data!A:A, "<="&Month_End, Customer_Data!C:C, "First_Payment")
```

### Calculation 8: Churned Customers

```yaml
FORMULA:
  Churned Customers = Count of customers who canceled this month (excluding downgrades)

EXCEL:
  =COUNTIFS(Churn_Log!A:A, ">="&Month_Start, Churn_Log!A:A, "<="&Month_End)
```

### Calculation 9: Customer Churn Rate

```yaml
FORMULA:
  Monthly Customer Churn (%) = Churned Customers This Month / Total Customers at Start of Month × 100

EXAMPLE:
  Start of month: 292 customers
  Churned: 10
  Customer Churn: 10 / 292 × 100 = 3.42%

EXCEL:
  =Churned_Customers / Starting_Customers * 100
```

### Calculation 10: Revenue Churn Rate

```yaml
FORMULA:
  Revenue Churn (%) = Churned MRR This Month / Starting MRR × 100

EXAMPLE:
  Starting MRR: $15,400
  Churned MRR: $500
  Revenue Churn: $500 / $15,400 × 100 = 3.25%

EXCEL:
  =Churned_MRR / Starting_MRR * 100
```

### Calculation 11: Net Revenue Retention (NRR)

```yaml
FORMULA:
  NRR = (Starting MRR - Churn MRR - Contraction MRR + Expansion MRR) / Starting MRR × 100

EXAMPLE:
  Starting MRR: $15,400
  Churn MRR: $500
  Contraction MRR: $200
  Expansion MRR: $800
  NRR = ($15,400 - $500 - $200 + $800) / $15,400 × 100
  NRR = $15,500 / $15,400 × 100 = 100.65%

EXCEL:
  =(Starting_MRR - Churn_MRR - Contraction_MRR + Expansion_MRR) / Starting_MRR * 100
```

### Calculation 12: Gross Revenue Retention (GRR)

```yaml
FORMULA:
  GRR = (Starting MRR - Churn MRR - Contraction MRR) / Starting MRR × 100

EXAMPLE:
  GRR = ($15,400 - $500 - $200) / $15,400 × 100
  GRR = $14,700 / $15,400 × 100 = 95.45%

EXCEL:
  =(Starting_MRR - Churn_MRR - Contraction_MRR) / Starting_MRR * 100
```

---

## Part 4: Unit Economics

### Calculation 13: Customer Acquisition Cost (CAC)

```yaml
FORMULA:
  CAC = Total Sales & Marketing Spend / Number of New Customers

EXAMPLE:
  S&M Spend: $4,000
  New Customers: 30
  Blended CAC: $4,000 / 30 = $133.33

BY CHANNEL:
  Organic CAC: $0 / 12 = $0
  Google Ads CAC: $2,500 / 10 = $250
  Content CAC: $1,000 / 5 = $200
  Referral CAC: $500 / 3 = $166.67

EXCEL (blended):
  =Total_SM_Spend / New_Customers

EXCEL (by channel):
  =SUMIFS(Spend_Data!C:C, Spend_Data!B:B, "Google Ads") / COUNTIFS(Customer_Data!D:D, "Google_Ads", Customer_Data!A:A, ">="&Month_Start, Customer_Data!A:A, "<="&Month_End)
```

### Calculation 14: CAC Payback Period

```yaml
FORMULA:
  CAC Payback (months) = CAC / (ARPU × Gross Margin)

EXAMPLE:
  CAC: $133.33
  ARPU: $52.74
  Gross Margin: 80.5% (0.805)
  
  Monthly Gross Profit per Customer: $52.74 × 0.805 = $42.46
  Payback: $133.33 / $42.46 = 3.14 months

EXCEL:
  =CAC / (ARPU * Gross_Margin)
```

### Calculation 15: Customer Lifetime (Average)

```yaml
FORMULA:
  Average Customer Lifetime (months) = 1 / Monthly Churn Rate

EXAMPLE:
  Monthly Churn: 3.42%
  Average Lifetime: 1 / 0.0342 = 29.2 months

EXCEL:
  =1 / Monthly_Churn_Rate

NOTE: This formula assumes constant churn. In reality, churn decreases over time.
For a more accurate calculation, use cohort-based lifetime.
```

### Calculation 16: Lifetime Value (LTV)

```yaml
FORMULA (Simple):
  LTV = ARPU / Monthly Churn Rate

FORMULA (Gross Margin Adjusted):
  LTV = ARPU / Monthly Churn Rate × Gross Margin

EXAMPLE (GM Adjusted):
  ARPU: $52.74
  Monthly Churn: 3.42%
  Gross Margin: 80.5%
  LTV = $52.74 / 0.0342 × 0.805
  LTV = $1,542.11 × 0.805
  LTV = $1,241.40

EXCEL:
  =ARPU / Monthly_Churn_Rate * Gross_Margin
```

### Calculation 17: LTV/CAC Ratio

```yaml
FORMULA:
  LTV/CAC Ratio = LTV (GM Adjusted) / CAC

EXAMPLE:
  LTV: $1,241.40
  CAC: $133.33
  LTV/CAC: $1,241.40 / $133.33 = 9.31x

EXCEL:
  =LTV / CAC
```

### Calculation 18: Gross Margin

```yaml
FORMULA:
  Gross Margin (%) = (Revenue - COGS) / Revenue × 100

EXAMPLE:
  Revenue: $15,400
  COGS: $3,000
  Gross Margin: ($15,400 - $3,000) / $15,400 × 100 = 80.52%

COGS DETAIL:
  Infrastructure: $1,200
  Payment Processing: $450
  API Costs: $800
  Support Tools: $300
  Customer Support: $250
  Total COGS: $3,000

EXCEL:
  =(Revenue - COGS) / Revenue * 100
```

### Calculation 19: Quick Ratio

```yaml
FORMULA:
  Quick Ratio = (New MRR + Expansion MRR) / (Churn MRR + Contraction MRR)

EXAMPLE:
  New MRR: $1,200
  Expansion MRR: $800
  Churn MRR: $500
  Contraction MRR: $200
  
  Quick Ratio = ($1,200 + $800) / ($500 + $200) = $2,000 / $700 = 2.86

EXCEL:
  =(New_MRR + Expansion_MRR) / (Churn_MRR + Contraction_MRR)
```

---

## Part 5: Complete Unit Economics Model

### The Full Spreadsheet

```yaml
UNIT ECONOMICS MODEL

INPUTS (from raw data):
  MRR: $15,400
  Customers (start of month): 292
  New Customers: 30
  Churned Customers: 10
  Churned MRR: $500
  New MRR: $1,500
  Expansion MRR: $800
  Contraction MRR: $200
  S&M Spend: $4,000
  COGS: $3,000

CALCULATED METRICS:
  ARPU: $15,400 / 292 = $52.74
  Customer Churn: 10 / 292 = 3.42%
  Revenue Churn: $500 / $15,400 = 3.25%
  
  CAC: $4,000 / 30 = $133.33
  Gross Margin: ($15,400 - $3,000) / $15,400 = 80.52%
  Payback: $133.33 / ($52.74 × 0.8052) = 3.14 months
  
  Avg Lifetime: 1 / 0.0342 = 29.2 months
  LTV: $52.74 / 0.0342 × 0.8052 = $1,241.40
  LTV/CAC: $1,241.40 / $133.33 = 9.31x
  
  NRR: ($15,400 - $500 - $200 + $800) / $15,400 = 100.65%
  GRR: ($15,400 - $500 - $200) / $15,400 = 95.45%
  Quick Ratio: ($1,500 + $800) / ($500 + $200) = 3.29
```

### Monthly Unit Economics Dashboard

```yaml
MONTH: June 2024

Revenue:
  MRR: $15,400 (+9.2% MoM)
  ARR: $184,800
  ARPU: $52.74
  ARPU by Plan: Basic $29, Pro $79, Enterprise $299

Growth:
  New MRR: $1,500
  Expansion MRR: $800
  Churn MRR: -$500
  Contraction MRR: -$200
  Net New MRR: $1,600

Retention:
  Customer Churn: 3.42%
  Revenue Churn: 3.25%
  NRR: 100.65%
  GRR: 95.45%
  Quick Ratio: 3.29

Unit Economics:
  CAC (blended): $133.33
  CAC by Channel: Organic $0, Google Ads $250, Content $200, Referral $167
  Gross Margin: 80.52%
  Payback Period: 3.14 months
  LTV: $1,241.40
  LTV/CAC: 9.31x
```

### Putting It All Together: The Master Formula

The single most important formula for your SaaS:

```yaml
Sustainable Growth Capacity = 
  (New Customer MRR × Gross Margin × LTV/CAC) / (CAC Payback in Months)

This tells you how much you can spend on growth while staying cash-flow positive.

Example:
  New Customer MRR: $1,500
  Gross Margin: 80%
  LTV/CAC: 9.31x
  Payback: 3.14 months
  
  Growth Capacity = ($1,500 × 0.80 × 9.31) / 3.14 = $3,558/month
  
  This means you can spend up to $3,558/month on acquisition 
  and still be cash-flow positive within your payback period.
```

---

## Part 6: Sensitivity and Scenario Analysis

### What-If Scenarios

Create these in your spreadsheet to test assumptions:

```yaml
SCENARIO 1: What if churn increases to 5%?
  LTV falls from $1,241 to $52.74 / 0.05 × 0.805 = $849
  LTV/CAC falls from 9.31x to $849 / $133 = 6.38x
  Impact: Still healthy, but 31% less value per customer

SCENARIO 2: What if we double S&M spend to $8K?
  New customers: 50 (optimistic, not 60 — diminishing returns)
  CAC: $8,000 / 50 = $160 (worse)
  Payback: $160 / ($52.74 × 0.805) = 3.77 months (longer)
  LTV/CAC: $1,241 / $160 = 7.76x (worse, but still good)
  Decision: Worth trying if volume is the bottleneck

SCENARIO 3: What if we raise prices 20%?
  ARPU: $63.29 (up from $52.74)
  Churn: 4% (customers sensitive to price)
  LTV: $63.29 / 0.04 × 0.805 = $1,273 (slightly higher)
  LTV/CAC: $1,273 / $133 = 9.56x
  Revenue impact: +20% per customer, -12% volume → +5.6% net revenue
  Decision: Worth testing with a subset of customers
```

### Sensitivity Table

```yaml
LTV/CAC Sensitivity (at current CAC of $133)

                        | Monthly Churn Rate
                        | 2%     | 3%     | 4%     | 5%     | 6%
────────────────────────|────────|────────|────────|────────|────────
Current ARPU ($52.74)   | 15.9x  | 10.6x  | 8.0x   | 6.4x   | 5.3x
ARPU +10% ($58.01)      | 17.5x  | 11.7x  | 8.8x   | 7.0x   | 5.8x
ARPU +20% ($63.29)      | 19.1x  | 12.7x  | 9.6x   | 7.6x   | 6.4x
ARPU +30% ($68.56)      | 20.7x  | 13.8x  | 10.4x  | 8.3x   | 6.9x
ARPU +50% ($79.11)      | 23.9x  | 15.9x  | 11.9x  | 9.6x   | 8.0x
```

---

## Part 7: Cohort-Based Unit Economics

### Why Cohorts Matter

Aggregate metrics hide truth. Cohorts reveal it.

```yaml
AGGREGATE:
  LTV/CAC = 9.31x
  → "Great, our unit economics are amazing!"

COHORT ANALYSIS:
  Jan 2024 cohort: LTV/CAC = 15x (early adopters, perfect use case)
  Mar 2024 cohort: LTV/CAC = 8x (broader market, mixed fit)
  Jun 2024 cohort: LTV/CAC = 5x (mass market, weak fit)
  → "Oh no, our unit economics are DECLINING!"

The aggregate number was misleading because it included early cohorts.
```

### Cohort-Based LTV Calculation

```yaml
For each monthly cohort:

Cohort: January 2024 (100 customers)

Month  | Active | Revenue  | Rev/Customer
───────|────────|──────────|─────────────
1      | 100    | $4,900   | $49.00
2      | 85     | $4,165   | $49.00
3      | 72     | $3,528   | $49.00
4      | 65     | $3,185   | $49.00
5      | 60     | $2,940   | $49.00
6      | 58     | $2,842   | $49.00
7      | 55     | $2,695   | $49.00
8      | 53     | $2,597   | $49.00
9      | 50     | $2,450   | $49.00
10     | 48     | $2,352   | $49.00
11     | 47     | $2,303   | $49.00
12     | 45     | $2,205   | $49.00

Total Rev/User: $49 × (1 + 0.85 + 0.72 + 0.65 + ... + 0.45) = $49 × ~7.38 = $361.62
LTV (no GM adjustment): $361.62
LTV (80% GM): $361.62 × 0.80 = $289.30
```

### Cohort-Based Unit Economics Spreadsheet

```yaml
Create this sheet:

COHORT UNIT ECONOMICS
                      | Jan     | Feb     | Mar     | Apr     | May     | Jun
──────────────────────|─────────|─────────|─────────|─────────|─────────|─────────
Cohort Size           | 100     | 110     | 120     | 115     | 130     | 140
12-Month LTV (GM Adj) | $289    | $302    | $285    | $270    | —       | —
CAC                   | $150    | $140    | $155    | $165    | $170    | $175
LTV/CAC               | 1.93x   | 2.16x   | 1.84x   | 1.64x   | —       | —
Payback (months)      | 5.2     | 4.8     | 5.5     | 6.1     | 6.5     | 7.0

Note: LTV declining across cohorts — need to investigate.
```

---

## Part 8: The Complete Unit Economics Spreadsheet Template

### Structure

```yaml
Sheet 1: Raw Data
  Columns: Month, MRR, Customers, New, Churned, Upgraded, Downgraded, 
           S&M Spend, COGS Detail
  Rows: 24 months of historical data

Sheet 2: Metrics Calculation
  Calculates all metrics from raw data
  Columns: Each metric as a column
  Rows: One per month

Sheet 3: Channel Breakdown
  Columns: Channel, Spend, Customers, CAC, Conversion Rate
  Rows: Each channel

Sheet 4: Cohort Analysis
  Pivot table: Cohorts × Months
  Values: Customer count, revenue

Sheet 5: Sensitivity
  LTV/CAC sensitivity table (ARPU × Churn matrix)
  Payback sensitivity table (CAC × ARPU matrix)

Sheet 6: Dashboard
  Key metrics summary
  Trend charts
  Alerts
```

### Key Formulas Reference

```yaml
All formulas assume headers in Row 1, data starting Row 2.

A = Month
B = MRR
C = Customers
D = New Customers
E = Churned Customers
F = S&M Spend
G = COGS

Row 2 formulas:

ARPU: =B2/C2
Customer Churn: =E2/C2*100
Revenue Churn: =(E2*ARPU)/B2*100   [simplified]
CAC: =F2/D2
Gross Margin: =(B2-G2)/B2*100
Payback: =H2/(I2*(L2/100))   [CAC/(ARPU*GM)]
Lifetime: =1/(J2/100)        [1/(churn_rate)]
LTV: =I2*M2*(L2/100)         [ARPU*Lifetime*GM]
LTV/CAC: =N2/H2
NRR: =(B2-(E2*ARPU)+(upgrade_MRR))/B2*100   [simplified]
Quick Ratio: =(New_MRR+Exp_MRR)/(Churn_MRR+Cont_MRR)
```

---

## Part 9: Actionable Insights from Unit Economics

### What to Do With These Numbers

```yaml
If LTV/CAC < 3x (minimum):
  - Your business model is broken
  - Either reduce CAC, increase ARPU, reduce churn, or increase GM
  - Pick one and focus on it for 90 days

If LTV/CAC > 5x (good) but payback > 12 months:
  - You're profitable per customer but cash-flow negative
  - Need to improve payback: reduce CAC or increase ARPU
  - Consider annual prepayments to improve cash flow

If LTV/CAC > 10x (excellent):
  - You're under-spending on growth
  - Increase S&M budget aggressively
  - But test in small increments — don't bet the farm

If churn > 5% monthly:
  - Nothing else matters until this is fixed
  - Every dollar spent on acquisition is partially wasted
  - Focus ALL energy on retention

If NRR < 100%:
  - Your existing customer base is shrinking
  - You need aggressive new acquisition just to stay flat
  - Fix: improve expansion revenue or reduce contraction
```

### The Monthly Unit Economics Review

```yaml
90-DAY UNIT ECONOMICS SPRINT

Week 1: Setup
  ☐ Collect all raw data (last 12 months)
  ☐ Build the spreadsheet (use template)
  ☐ Calculate all metrics
  ☐ Identify the weakest metric

Week 2-4: Improve the weakest metric
  If churn > 5%: Improve onboarding
  If CAC > payback target: Find cheaper channel
  If ARPU < target: Test price increase
  If GM < 75%: Reduce infrastructure/API costs

Week 5-8: Measure and iterate
  ☐ Recalculate metrics
  ☐ Compare to baseline
  ☐ Adjust approach based on results
  ☐ Pick next weakest metric

Week 9-12: Full review
  ☐ Run full unit economics analysis
  ☐ Compare to benchmarks
  ☐ Set goals for next quarter
  ☐ Update dashboard
```

You now have a complete system for calculating and tracking your SaaS unit economics. Run this model monthly, act on the insights, and you'll build a business that's profitable by design, not by accident.