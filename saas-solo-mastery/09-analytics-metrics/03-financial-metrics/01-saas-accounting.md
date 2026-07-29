# SaaS Accounting Basics

A practical guide to SaaS accounting for solo founders — covering revenue recognition, deferred revenue, accrual vs. cash basis, and everything else you need to keep your books clean and survive a tax audit.

---

## Part 1: Why SaaS Accounting Is Different

### The Core Problem

SaaS businesses have a fundamental accounting challenge that traditional businesses don't:

**You collect money upfront, but earn it over time.**

When a customer pays $1,200 for an annual subscription in January, you don't actually "own" all $1,200 in January. You earn $100 each month as you deliver the service.

This creates four accounting challenges unique to SaaS:

1. **Revenue recognition** — When do you count revenue?
2. **Deferred revenue** — Where does the unearned money go?
3. **Accrual accounting** — How do you match expenses to revenue periods?
4. **Subscription metrics** — How do you track performance beyond cash?

### Why This Matters for Solo Founders

| Scenario | Cash Accounting Says | Accrual Accounting Says | Reality |
|----------|---------------------|------------------------|---------|
| You close a $12K annual deal in January | Revenue: $12K in January | Revenue: $1K/mo for 12 months | You can't spend $12K in January — you need to spread it |
| You pay $6K for annual hosting in January | Expense: $6K in January | Expense: $500/mo for 12 months | That $6K is an investment in the year, not a single expense |
| A customer cancels in month 3 | No impact (already counted) | Revenue write-down of $9K | You need to track refund exposure |

Getting this wrong means:
- You think you're profitable when you're not
- You spend money you don't actually have
- You pay taxes on revenue you might have to refund
- Investors can't understand your business

---

## Part 2: Cash vs. Accrual Accounting

### Cash Basis Accounting

**What it is:** Revenue is recorded when cash is received. Expenses are recorded when cash is paid.

**Example:**
```
January 15: Customer pays $1,200 for annual plan
  → Revenue recorded: $1,200 (January)
  → Net income: $1,200 - January expenses

March 1: You pay $6,000 for annual hosting
  → Expense recorded: $6,000 (March)
  → Net income: $1,200 - $6,000 = -$4,800 loss in March
```

**Pros:**
- Simple — no accounting knowledge needed
- Matches your bank account
- Easy to understand
- Good for very early stage (pre-revenue / < $10K revenue)

**Cons:**
- Doesn't match revenue with the period it was earned
- Creates misleading profit/loss statements
- Annual deals make your financials look lumpy
- Not GAAP-compliant (investors and banks will want accrual)
- Misses future obligations (refunds for canceled subscriptions)

**Who should use cash basis:**
- Pre-revenue or very early stage (< $10K total revenue)
- No investors, no loans, no board
- Simple business (monthly subscriptions only)
- Filing taxes as sole proprietor (check with your accountant)

### Accrual Basis Accounting

**What it is:** Revenue is recorded when it's earned (service delivered). Expenses are recorded when they're incurred (not when paid).

**Example:**
```
January 15: Customer pays $1,200 for annual plan
  → Cash: +$1,200
  → Deferred Revenue (liability): +$1,200
  → Revenue recognized: $100 (January's portion)

March 1: You pay $6,000 for annual hosting
  → Prepaid Expense (asset): +$6,000
  → Expense recognized: $500 (March's portion)
  → Cash: -$6,000
```

**Monthly P&L (Accrual):**
```
January: Revenue $100, Hosting Expense $500 → -$400
February: Revenue $100, Hosting Expense $500 → -$400
... (same every month for 12 months)
```

This is a much more accurate picture of your business.

**Pros:**
- GAAP-compliant
- Matches revenue and expenses to the correct period
- Provides accurate monthly P&L
- Required for investors, banks, and significant loans
- Reveals the true economics of your business

**Cons:**
- More complex
- Requires tracking deferred revenue and prepaid expenses
- Your P&L won't match your bank account
- May need an accountant (or accounting software)

**Who should use accrual basis:**
- Any SaaS with > $10K annual revenue
- Planning to raise funding
- Has annual subscriptions
- Wants accurate business metrics
- Filing as S-Corp or C-Corp

### The Solo Founder Decision

| Your Situation | Recommended Basis | Why |
|---------------|-------------------|-----|
| < $10K MRR, all monthly plans | Cash | Simple, and the difference is minimal |
| < $10K MRR, has annual plans | Accrual | Annual plans make cash basis misleading |
| > $10K MRR, any mix | Accrual | Required for proper management |
| Planning to raise money | Accrual | Investors require GAAP-compliant statements |
| Tax filing only | Cash (if IRS allows) | Simpler tax filing, but check with CPA |

**Note:** The IRS allows certain small businesses to use cash basis. Over $25M in gross receipts, you must use accrual. Consult your CPA.

---

## Part 3: Revenue Recognition (ASC 606)

### What is ASC 606?

ASC 606 is the revenue recognition standard (also known as IFRS 15) that all SaaS companies must follow for GAAP-compliant financials. It requires:

1. Identify the contract with the customer
2. Identify the performance obligations (what you're delivering)
3. Determine the transaction price (what they're paying)
4. Allocate the price to performance obligations
5. Recognize revenue when (or as) obligations are satisfied

### For SaaS, This Means

**Simple case (one subscription, one plan):**
```
Customer pays $120/month for Basic plan
→ One performance obligation: Provide Basic service for the month
→ Revenue recognized: $120 each month as service is delivered
```

**Annual plan:**
```
Customer pays $1,200/year for Pro plan
→ One performance obligation: Provide Pro service for 12 months
→ Revenue recognized: $100/month as service is delivered
```

**Multi-element arrangement (complex):**
```
Customer pays $24,000/year for:
  - Pro software subscription ($18,000 standalone value)
  - Implementation services ($6,000 standalone value)
  - 24/7 phone support ($12,000 standalone value)

Total standalone value: $36,000
Allocation:
  - Software: $18,000/$36,000 × $24,000 = $12,000/year
  - Implementation: $6,000/$36,000 × $24,000 = $4,000 (recognized at completion)
  - Support: $12,000/$36,000 × $24,000 = $8,000/year
```

### Revenue Recognition Rules for Common Scenarios

| Scenario | When to Recognize Revenue |
|----------|---------------------------|
| Monthly subscription | Each month as service is provided |
| Annual subscription paid upfront | Pro-rata over 12 months |
| Setup/onboarding fee | Over the expected customer lifetime (if not distinct) or at point of delivery (if distinct) |
| Usage-based billing (overage) | When usage occurs |
| Professional services | When services are performed (percentage of completion) |
| Multi-year contract | Over the contract term |
| Free trial | No revenue until trial converts to paid |
| Refund | Reduction of revenue in the period the refund is issued |
| Credit (downgrade) | Reduction of future revenue |

### Revenue Recognition Journal Entry

```yaml
When customer pays $1,200 for annual plan:
  
  Debit: Cash                       $1,200
    Credit: Deferred Revenue                 $1,200
  (Record receipt of cash, create liability)

Each month for 12 months:
  
  Debit: Deferred Revenue           $100
    Credit: Subscription Revenue              $100
  (Recognize revenue as service is delivered)
```

### Spreadsheet for Revenue Recognition

Create this sheet to track revenue recognition:

```
Customer  | Plan   | Amount | Start    | End      | Monthly | Jan  | Feb  | Mar  | Apr  | ...
----------|--------|--------|----------|----------|---------|------|------|------|------|
Acme Inc  | Pro    | $1,200 | 01/15/24 | 01/14/25 | $100    | $100  | $100  | $100  | $100  |
Beta LLC  | Basic  | $240   | 02/01/24 | 01/31/25 | $20     | $0    | $20   | $20   | $20   |
CharlieCo | Annual | $600   | 03/01/24 | 02/28/25 | $50     | $0    | $0    | $50   | $50   |
----------|--------|--------|----------|----------|---------|------|------|------|------|
TOTAL     |        |        |          |          |         | $100  | $120  | $170  | $170  |
```

**Formulas:**
```
Monthly = Amount / DATEDIF(Start, End, "M")
Monthly Revenue = SUM of Monthly for customers active that month
Deferred Revenue = SUM of remaining Monthly amounts for all active customers
```

---

## Part 4: Deferred Revenue (The Most Important SaaS Liability)

### What is Deferred Revenue?

Deferred revenue (also called unearned revenue) is money you've collected but haven't earned yet. It's a **liability** on your balance sheet — you owe the customer service for the prepaid period.

### Why Deferred Revenue Matters

For a SaaS business, deferred revenue can be enormous:

```
Company collects $1M in annual prepayments
→ Cash: $1M (looks great!)
→ Deferred Revenue: $1M (liability!)
→ Actual earned revenue this month: ~$83K
→ Actual earned revenue per month: $83K for 12 months
```

A founder who doesn't understand deferred revenue thinks: "I have $1M! I can hire 5 people!"

A founder who understands deferred revenue thinks: "I have $1M in cash, but I owe $917K in future service. I can only spend what I've earned: $83K this month."

**This is the #1 financial mistake solo SaaS founders make.**

### Deferred Revenue Calculation

```
Total Deferred Revenue = Sum of unearned portions of all active subscriptions

For each customer:
  Deferred = (Remaining days in subscription period / Total days) × Total payment
```

### Example Calculation

```
Customer: Acme Inc
Plan: Pro Annual ($1,200/year)
Paid: January 1, 2024
Subscription Period: January 1, 2024 — December 31, 2024

On January 15 (15 days in):
  Earned: $1,200 × (15/365) = $49.32
  Deferred: $1,200 × (350/365) = $1,150.68

On July 1 (182 days in):
  Earned: $1,200 × (182/365) = $598.36
  Deferred: $1,200 × (183/365) = $601.64
```

### Deferred Revenue Tracking Template

```yaml
Customer    | Contract Value | Start Date | End Date   | Deferred at Month Start | Recognized This Month | Deferred at Month End
Acme Inc    | $1,200         | 01/01/2024 | 12/31/2024 | $1,100                  | $100                  | $1,000
Beta LLC    | $600           | 03/01/2024 | 02/28/2025 | $550                    | $50                   | $500
CharlieCo   | $360           | 06/01/2024 | 05/31/2025 | $330                    | $30                   | $300
TOTAL       | $2,160         |            |            | $1,980                  | $180                  | $1,800
```

### Deferred Revenue and Cash Runway

```
Correct Runway Calculation:
  Available Cash = Cash + (Future Receivables) - (Deferred Revenue)
  Monthly Burn = All expenses (not just cash expenses)
  Real Runway = Available Cash / Monthly Burn

Correct Interpretation:
  "I have $100K in the bank, but I owe $60K in future service.
   My real available capital is $40K."
```

---

## Part 5: SaaS-Specific Accounting Entries

### Journal Entry: New Subscription (Monthly)

```yaml
When customer signs up for $49/month:

On signup (no entry, subscription starts):
  No accounting entry yet

On payment (Stripe settlement):
  Dr: Cash (Bank)                     $49
    Cr: Subscription Revenue                   $49
  (Revenue recognized immediately for monthly)

On Stripe fee:
  Dr: Processing Fee                  $1.42
    Cr: Cash (Bank)                             $1.42
  (2.9% + $0.30 on $49 = $1.72, actual depends on your Stripe rate)
```

### Journal Entry: New Subscription (Annual Paid Upfront)

```yaml
On payment ($600 received for annual):

  Dr: Cash (Bank)                   $600
    Cr: Deferred Revenue                      $600
  (Record prepayment as liability)

Each month for 12 months:
  Dr: Deferred Revenue               $50
    Cr: Subscription Revenue                    $50
  (Recognize 1/12 of annual payment)

On Stripe fee ($600 × 2.9% + $0.30 = $17.70):
  Dr: Processing Fee                $17.70
    Cr: Cash (Bank)                             $17.70
```

### Journal Entry: Upgrade (Mid-Cycle)

```yaml
Customer upgrades from Basic ($49/mo) to Pro ($99/mo) on day 15 of monthly cycle:

  Pro-rate: 
    Basic used: 15 days × $49/30 = $24.50 recognized
    Pro for remaining: 15 days × $99/30 = $49.50

  Dr: Cash (Bank)                    $50 ($99 - $49 already paid)
    Cr: Subscription Revenue                     $24.50 (prorated credit for unused Basic)
    Cr: Deferred Revenue                         $25.50 (unearned portion of Pro)
    
  End of month:
  Dr: Deferred Revenue               $25.50
    Cr: Subscription Revenue                     $25.50
```

### Journal Entry: Downgrade

```yaml
Customer downgrades from Pro ($99/mo) to Basic ($49/mo) on day 10 of monthly cycle:

  Option A: Pro-rate and credit
    Pro used: 10 days × $99/30 = $33 recognized
    Remaining unused: $66 credit
    New Basic for rest of month: 20 days × $49/30 = $32.67
    Credit applied: $66 - $32.67 = $33.33 remaining credit

  Dr: Deferred Revenue (or Revenue Contra)    $33.33
    Cr: Customer Credit (Liability)                       $33.33
  (Credit applied to future invoices)
```

### Journal Entry: Churn/Cancellation

```yaml
Customer cancels annual subscription ($600 paid, 4 months used):

  Revenue earned (4 months): $600 × 4/12 = $200
  Deferred remaining: $600 × 8/12 = $400
  
  If no refund (monthly billing, cancel at end of period):
    Dr: Deferred Revenue              $400
      Cr: Subscription Revenue                    $0 (no change — revenue was never recognized)
      Cr: [Deferred Revenue relieved]              $400
  (Remove deferred revenue liability; no refund given)
  
  If refund given:
    Dr: Deferred Revenue              $400
    Dr: Refund Expense                ($400 refund - $400 deferred removal = $0)
      Cr: Cash (Bank)                             $400
  (Return the unearned portion)
  
  In practice, many SaaS companies have a no-refund policy:
    Dr: Deferred Revenue              $400
      Cr: Revenue (or Other Income)               $400
  (Recognize remaining deferred as revenue if no refund — check your contract terms)
```

### Journal Entry: Failed Payment (Dunning)

```yaml
Monthly subscription $49 fails:

  No accounting entry yet — payment didn't happen.
  
  During dunning period (3-15 days):
  - Monitor accounts receivable (if accrual basis)
  - No revenue recognized for uncollected period
  
  If payment eventually succeeds:
    Dr: Cash (Bank)                    $49
      Cr: Subscription Revenue                    $49
  
  If customer cancels due to failed payment:
    - Remove from active subscribers
    - Any previously recognized revenue stays (revenue was earned)
```

---

## Part 6: SaaS Chart of Accounts

A minimal chart of accounts for a solo-founded SaaS company:

### Balance Sheet Accounts

```
ASSETS
1000 - Cash and Cash Equivalents
  1010 - Checking Account
  1020 - Savings Account
  1030 - Money Market / High-Yield

1100 - Accounts Receivable
  1110 - Trade Receivables (unpaid invoices)
  1120 - Allowance for Doubtful Accounts

1200 - Prepaid Expenses
  1210 - Prepaid Hosting/Infrastructure
  1220 - Prepaid Software Subscriptions
  1230 - Prepaid Insurance

1300 - Fixed Assets
  1310 - Computer Equipment
  1320 - Furniture
  1330 - Accumulated Depreciation

LIABILITIES
2000 - Accounts Payable
  2010 - Trade Payables

2100 - Deferred Revenue
  2110 - Deferred Subscription Revenue
  2120 - Deferred Professional Services Revenue

2200 - Accrued Liabilities
  2210 - Accrued Payroll
  2220 - Accrued Taxes Payable
  2230 - Accrued Interest

2300 - Current Portion of Debt
  2400 - Long-Term Debt

EQUITY
3000 - Common Stock / Owner's Equity
3100 - Retained Earnings
3200 - Additional Paid-In Capital
3300 - Current Year Earnings
```

### Income Statement Accounts

```
REVENUE
4000 - Subscription Revenue
  4010 - Monthly Subscription Revenue
  4020 - Annual Subscription Revenue

4100 - Other Revenue
  4110 - Professional Services Revenue
  4120 - Setup/Onboarding Fees
  4130 - Training Revenue
  4140 - Interest Income

COST OF GOODS SOLD
5000 - Infrastructure & Hosting
  5010 - Cloud Hosting (AWS/GCP/Cloudflare)
  5020 - Third-Party API Costs
  5030 - CDN Costs
  5040 - Database Costs

5100 - Payment Processing
  5110 - Stripe/Paddle Fees

5200 - Customer Support
  5210 - Support Tool Subscriptions
  5220 - Support Staff (if any)

OPERATING EXPENSES
6000 - Research & Development
  6010 - Software Development Tools
  6020 - Developer Licenses & Subscriptions
  6030 - Domain Names & DNS

6100 - Sales & Marketing
  6110 - Advertising (Google, LinkedIn, Twitter)
  6120 - Content Creation & SEO
  6130 - Email Marketing Tools
  6140 - CRM Costs
  6150 - Referral Program Costs

6200 - General & Administrative
  6210 - Accounting & Legal
  6220 - Insurance
  6230 - Bank Fees
  6240 - Office Supplies
  6250 - Software Subscriptions

6300 - Payroll (when you hire)
  6310 - Salaries & Wages
  6320 - Payroll Taxes
  6330 - Benefits
  6340 - Contractor Payments

6400 - Travel & Entertainment
  6410 - Conferences & Events
  6420 - Customer Meetings
  
6500 - Depreciation & Amortization
```

---

## Part 7: SaaS Financial Statement Analysis

### Income Statement (P&L) for a SaaS

```yaml
Monthly P&L (Accrual Basis)
──────────────────────────────────────
REVENUE
  Subscription Revenue          $12,000
  Other Revenue                 $500
Total Revenue                   $12,500

COST OF GOODS SOLD
  Infrastructure & Hosting      $2,000
  Payment Processing            $400
  Customer Support              $300
Total COGS                      $2,700

GROSS PROFIT                    $9,800
GROSS MARGIN                    78.4%

OPERATING EXPENSES
  Research & Development        $4,000
  Sales & Marketing             $2,500
  General & Administrative      $1,200
Total OpEx                      $7,700

OPERATING INCOME (EBITDA)       $2,100
OPERATING MARGIN                16.8%

OTHER INCOME/EXPENSE
  Interest Income               $50
  Interest Expense              $0

NET INCOME                      $2,150
NET MARGIN                      17.2%
──────────────────────────────────────
```

### Balance Sheet for a SaaS

```yaml
Monthly Balance Sheet
──────────────────────────────────────
ASSETS
  Current Assets
    Cash & Equivalents           $85,000
    Accounts Receivable          $2,000
    Prepaid Expenses             $6,000
  Total Current Assets           $93,000
  
  Fixed Assets (net)             $5,000
  
TOTAL ASSETS                     $98,000

LIABILITIES
  Current Liabilities
    Accounts Payable             $1,200
    Deferred Revenue             $18,000
    Accrued Expenses             $2,000
  Total Current Liabilities      $21,200
  
  Long-Term Debt                 $0

TOTAL LIABILITIES                $21,200

EQUITY
  Owner's Equity                 $50,000
  Retained Earnings              $26,800

TOTAL LIABILITIES + EQUITY       $98,000
──────────────────────────────────────
```

### Key Financial Ratios from Accounting Data

| Ratio | Formula | Healthy Range |
|-------|---------|---------------|
| Current Ratio | Current Assets / Current Liabilities | > 1.5 |
| Quick Ratio | (Cash + Receivables) / Current Liabilities | > 1.0 |
| Debt-to-Equity | Total Liabilities / Total Equity | < 1.0 (for bootstrapped) |
| Deferred Revenue Ratio | Deferred Revenue / Total Revenue (monthly) | Indicates prepayment mix |
| Gross Margin | Gross Profit / Total Revenue | > 75% |
| Operating Margin | Operating Income / Total Revenue | > 15% (early), > 30% (mature) |

---

## Part 8: Accounting Tools for Solo Founders

### Free/Low-Cost Options

#### Wave Apps (Free)

**Best for:** Pre-revenue to $10K MRR
**Cost:** Free (invoicing, accounting); payment processing fees apply
**Features:**
- Income/expense tracking
- Invoicing
- Receipt scanning
- Basic reporting (P&L, Balance Sheet)
- No deferred revenue tracking

**Limitations:**
- No deferred revenue management
- No subscription-specific features
- Manual entry for subscriptions

#### Xero (Paid)

**Best for:** $5K - $50K MRR
**Cost:** $13-$70/month
**Features:**
- Full double-entry accounting
- Bank reconciliation
- Deferred revenue (via add-on apps)
- P&L, Balance Sheet, Cash Flow
- Multi-currency

**Add-ons for SaaS:**
- ChartMogul subscription data sync
- Revenue recognition automation

#### QuickBooks Online (Paid)

**Best for:** $10K+ MRR
**Cost:** $30-$100/month (not including payroll)
**Features:**
- Full accounting suite
- Deferred revenue tracking
- Project profitability
- Time tracking (if billing hourly)
- Extensive third-party app marketplace

**SaaS-specific apps:**
- QuickBooks + Stripe integration
- QuickBooks + Chargebee (subscription billing sync)

#### Bench (Bookkeeping Service)

**Best for:** Founders who don't want to do their own books
**Cost:** $299-$599/month
**Features:**
- Dedicated bookkeeper
- Monthly financial statements
- Tax coordination
- Receipt management
- Software integration (Stripe, bank, etc.)

**Pros for solo founders:**
- Frees up your time completely
- Catch errors and ensure compliance
- Great for tax preparation
- Scales with your business

### Revenue Recognition Software

| Tool | Cost | Best For |
|------|------|----------|
| ChartMogul | $119/mo | Combined analytics + basic rev rec |
| Chargebee | $599/mo (Growth plan) | Subscription management + rev rec |
| Stax Bill | Custom | Full billing + rev rec |
| QuickBooks + Excel | $30-$100/mo | Manual but cheap |
| RevPro (Workday) | $$$$ | Enterprise only — ignore |

---

## Part 9: Tax Implications of Revenue Recognition

### The Tax Problem

This is where many solo founders get into trouble:

```
Scenario:
  You close $120K in annual deals in December
  Cash received: $120K
  Cash basis tax: You pay tax on $120K in revenue this year
  Accrual basis tax: You pay tax on $10K in revenue this year
  
  If you use cash basis for tax (and many small businesses do):
    → You pay income tax on $120K, even though you'll earn it over 12 months
    → You might not have enough cash left for taxes + operating expenses
  
  If you use accrual basis for tax:
    → You pay tax on the earned portion ($10K that month)
    → Much more manageable
```

### IRS Rules for SaaS Tax Accounting

- Businesses with < $25M in average annual gross receipts can use cash basis for tax
- Businesses with > $25M must use accrual
- Once you exceed $25M, you must switch to accrual (permanent)
- You can choose cash or accrual initially — but changing methods requires IRS approval

### Sales Tax on Revenue Recognition

**The complexity:**
- You collect sales tax on the full payment (when customer pays)
- But you recognize revenue over time
- Sales tax is due when collected, not when earned

**Impact on cash flow:**
```
$1,200 annual deal, 8% sales tax:
  Collect: $1,296 ($1,200 + $96 tax)
  Sales tax due: $96 (typically next month — regardless of rev rec)
  Cash available for operations: $1,200 (but $1,100 is deferred)
  Tax remittance: $96 (MUST be paid even though most revenue is unearned)
```

### Recommendations for Solo Founders

1. **Use accrual accounting for internal management** (so you understand your business)
2. **Use cash basis for tax filing** if eligible (simpler, consult CPA)
3. **Set aside 30% of all revenue** for taxes (both income and sales tax)
4. **File sales tax returns on time** — states are aggressive about SaaS tax collection
5. **Hire a CPA** when you cross $50K ARR — the complexity is worth the cost

---

## Part 10: Building Your Accounting System

### Month 1-3: Setup

```yaml
Week 1:
  - Open business bank account (separate from personal!)
  - Choose accounting software (Wave or Xero recommended)
  - Connect Stripe to accounting software

Week 2:
  - Set up chart of accounts (use the template above)
  - Import historical transactions
  - Categorize all expenses

Week 3:
  - Set up deferred revenue tracking (spreadsheet is fine for < $50K)
  - Create revenue recognition schedule
  - Verify MRR numbers match between Stripe and books

Week 4:
  - Create monthly close process
  - Set up recurring expense categories
  - Review first month's P&L with accrual accounting
```

### Monthly Close Process

```
Week 1 of every month:

Day 1: Bank reconciliation
  - Match all bank transactions to accounting entries
  - Identify and categorize uncategorized transactions
  - Resolve discrepancies

Day 2: Revenue reconciliation
  - Pull Stripe revenue report
  - Verify deferred revenue schedule
  - Confirm revenue recognition entries
  - Match revenue between Stripe and books

Day 3: Expense review
  - Review all expenses for the month
  - Categorize any miscategorized items
  - Prepaid expenses amortization
  - Accrue any unpaid expenses (credit card charges, etc.)

Day 4: Financial statements
  - Generate P&L (accrual basis)
  - Generate Balance Sheet
  - Calculate SaaS metrics from accounting data
  - Review against budget/forecast

Day 5: Review and file
  - Review with CPA (quarterly)
  - Pay estimated taxes (if applicable)
  - File sales tax returns (if applicable)
  - Update financial projections with actuals
```

### Annual Tasks

```yaml
January:
  - Year-end close
  - Review all accounts
  - Reconcile deferred revenue for entire year
  - Generate annual financial statements
  
February:
  - Tax preparation (W-2, 1099, corporate tax return)
  - CPA review of annual books
  - File annual reports (state filing)
  
March:
  - Budget for new fiscal year
  - Update chart of accounts if needed
  - Review accounting software (still the right tool?)
  
Quarterly:
  - Estimated tax payments (April 15, June 15, Sept 15, Jan 15)
  - Sales tax filings (frequency depends on state)
  - CPA check-in on financial health
```

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│              SAAS ACCOUNTING CHEAT SHEET                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  REVENUE RECOGNITION                                        │
│  ───────────────────                                        │
│  Monthly subs: Record as earned immediately                 │
│  Annual subs:  Defer, recognize 1/12 each month            │
│  Multi-year:   Defer, recognize over contract term          │
│  Setup fees:   Recognize over avg customer lifetime         │
│  Usage/Overage: Recognize when usage occurs                 │
│                                                             │
│  DEFERRED REVENUE                                           │
│  ────────────────                                           │
│  It's NOT revenue — it's a liability                        │
│  It's NOT your money to spend                               │
│  Deferred Revenue = Unearned portion of prepayments         │
│  Calculate: Remaining days / Total days × Amount paid       │
│                                                             │
│  ACCRUAL VS CASH                                            │
│  ────────────────                                           │
│  Use accrual for: Internal management, investors           │
│  Use cash for:    Tax filing (if < $25M receipts)          │
│  Difference:      Deferred Revenue + Prepaid Expenses      │
│                                                             │
│  KEY FORMULAS                                               │
│  ─────────────                                              │
│  Recognized Revenue = Total Payment / Subscription Months   │
│  Deferred Revenue = Remaining Months × Monthly Revenue     │
│  Gross Margin = (Revenue - COGS) / Revenue                 │
│  Real Runway = (Cash - Deferred Revenue) / Monthly Burn    │
│                                                             │
│  MONTHLY CLOSE CHECKLIST                                    │
│  ──────────────────────                                     │
│  ☐ Bank accounts reconciled                                 │
│  ☐ Revenue reconciled to Stripe                             │
│  ☐ Deferred revenue schedule updated                       │
│  ☐ All expenses categorized                                 │
│  ☐ P&L generated (accrual basis)                            │
│  ☐ Balance sheet reviewed                                   │
│  ☐ SaaS metrics calculated from books                       │
│  ☐ Projections updated with actuals                         │
│  ☐ Sales tax filed (if due)                                 │
│  ☐ Estimated taxes paid (if due)                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Final Advice for Solo Founders

1. **Separate your bank accounts immediately.** Mixing personal and business is the #1 accounting mistake.

2. **Don't spend deferred revenue.** Just because you collected $50K in annual deals doesn't mean you can hire someone. You've only earned ~$4K this month.

3. **Use accrual accounting from month 1.** The extra effort is small, and the understanding you gain is invaluable.

4. **Automate what you can.** Connect Stripe to your accounting software. Use a spreadsheet for deferred revenue if you can't afford dedicated software.

5. **Get a CPA before you need one.** At $50K MRR ($600K ARR), the complexity justifies professional help.

6. **Set aside 30% of all revenue for taxes.** This covers federal, state, self-employment, and sales tax. If you save nothing else, save this.

7. **Revenue recognition is not optional.** The IRS and GAAP have clear rules. Follow them. The penalties for getting it wrong are severe.

8. **Your P&L will be wrong on cash basis.** If your P&L says you're profitable but you're stressed about money, switch to accrual.