# International Banking for SaaS

A guide to banking for solo SaaS founders operating globally — choosing the right bank (Mercury, Wise, Brex, Relay), handling multi-currency revenue, managing international expenses, and optimizing your financial operations.

---

## Part 1: The Solo Founder Banking Reality

### Why Traditional Banks Don't Work

Traditional banks are designed for local businesses with local customers and local expenses. Solo SaaS founders need:

```yaml
What you need:
  - No monthly fees (every dollar counts early on)
  - Multi-currency accounts (EUR, GBP, USD, etc.)
  - International wire transfers (pay contractors worldwide)
  - API access (automate accounting)
  - Virtual cards (for online tools and subscriptions)
  - Easy online setup (no branch visits)
  - Integration with Stripe/Paddle
  - High-yield interest on cash balances

What traditional banks offer:
  - $15/month maintenance fee
  - $45 international wire fee
  - No multi-currency
  - No API
  - Need to visit branch in person
  - Low interest (0.01% APY)
```

### The Neobank Revolution

Fintech banks (neobanks) were built for companies like yours. They offer everything you need with none of the friction.

```yaml
Neobank advantage:
  - No minimum balance (or very low)
  - Free or low monthly fees
  - Multi-currency accounts standard
  - Cheap international transfers
  - API access for automation
  - Virtual and physical cards
  - Stripe/Paddle integration
  - Higher interest on cash (2-5% APY)
  - Mobile-first (no branches needed)
  - Fast account setup (days, not weeks)
```

---

## Part 2: Mercury — The Solo Founder Favorite

### Overview

```yaml
Best for: US-based solo founders with international revenue
Cost: FREE ($0/month, $0 minimum)
Banking license: Evolve Bank & Trust (FDIC insured up to $250K)
Remote setup: Yes (100% online)
Year founded: 2017 (by former Silicon Valley Bank employees)

Features:
  - USD checking and savings
  - Multi-currency accounts (EUR, GBP, CAD, etc.)
  - Free domestic and international wire transfers
  - Free ACH transfers
  - Virtual and physical debit cards
  - API and webhooks
  - QuickBooks, Xero integration
  - High-yield treasury accounts (4%+ APY)
  - Bill pay
  - No transaction limits
```

### Mercury In Depth

```yaml
ACCOUNT SETUP:
  - Apply online (10 minutes)
  - Need: Legal entity (LLC/C-Corp), EIN, personal ID
  - Decision: Usually 1-3 business days
  - Note: Must be US entity with US founder

MULTI-CURRENCY:
  - Hold, send, and receive in USD, EUR, GBP, CAD
  - Create local account numbers (US, UK, EU)
  - This means: Customers can pay you via local transfer (no SWIFT fees)
  - Exchange between currencies at competitive rates
  - Free to receive international payments

TRANSFERS:
  - Domestic ACH: Free (unlimited)
  - Domestic wire: Free (incoming and outgoing)
  - International wire: Free (outgoing)
  - International wire (incoming): Free
  - SWIFT transfers: Embedded in the platform

VIRTUAL CARDS:
  - Unlimited virtual cards
  - Set per-card limits
  - Per-merchant cards
  - Freeze/unfreeze instantly
  - Integrate with accounting
  - 1% cashback on some cards

INTEGRATIONS:
  - Stripe (sync transactions)
  - QuickBooks, Xero, FreshBooks
  - Zapier
  - API (REST + webhooks)
  - Slack notifications

INTEREST:
  - Mercury Treasury: 4%+ APY on USD (via FDIC sweep)
  - No minimum balance
  - Instant transfers between checking and treasury

PROS:
  - Completely free (no monthly fees ever)
  - Best multi-currency support for US banks
  - Free international wires (huge for SaaS founders)
  - Excellent API for automation
  - VC-linked (integrations with Carta, AngelList)

CONS:
  - US entities only (no international founders)
  - No joint accounts
  - Customer support can be slow (email only, no phone)
  - Limited lending options (no business loans/credit)
  - No physical branches (can't deposit cash)
  - Sometimes long verification delays
```

### Mercury Setup Guide

```yaml
Step 1: Prepare documents
  - Articles of Organization (LLC) or Incorporation (C-Corp)
  - EIN confirmation letter (from IRS)
  - Personal ID (driver's license or passport)
  - Business address proof (utility bill, lease)
  - Identify all beneficial owners (anyone owning 25%+)

Step 2: Apply
  - Go to mercury.com
  - Click "Open an Account"
  - Fill in: Business info, ownership, expected activity
  - Upload documents

Step 3: Verification
  - Mercury verifies your documents
  - May ask for additional information
  - May schedule a video call (unusual but possible)

Step 4: Fund your account
  - Transfer initial deposit
  - Or: Connect Stripe to receive payments

Step 5: Set up integrations
  - Connect Stripe (Settings → Integrations → Stripe)
  - Connect accounting software
  - Set up virtual cards for subscriptions
  - Set up treasury account for cash reserves
```

---

## Part 3: Wise (Formerly TransferWise)

### Overview

```yaml
Best for: International money transfers and multi-currency holding
Cost: Free account, small fees on transfers (0.3-1%)
Banking license: Various (Estonia, UK, US, Singapore — depends on region)
Multi-currency: 50+ currencies, local account details in 10 currencies

Key features:
  - Hold 50+ currencies in one account
  - Local bank details in USD, EUR, GBP, AUD, NZD, CAD, etc.
  - Send money to 70+ countries
  - Real exchange rate (no hidden markup)
  - Low, transparent fees
  - Business debit card
  - Integration with Xero, QuickBooks
  - Batch payments
  - API access
```

### Wise vs Mercury

```yaml
                 | Mercury         | Wise
─────────────────|─────────────────|────────────────────
Best for         | Primary bank    | Secondary (transfer tool)
Monthly fee      | $0              | $0
Account types    | USD + 3 multi   | 50+ currencies
Local details    | USD, EUR, GBP   | USD, EUR, GBP, AUD,...
Card             | Debit + Virtual | Debit (business)
International wires| Free          | Low fee (0.3-1%)
Interest         | 4%+ (Treasury)  | Minimal
API              | Yes             | Yes
US entity required| Yes            | No (international)
Stripe integration| Native         | Manual
Loan/credit      | No              | No

When to use Wise:
  - Receiving payments in currencies Mercury doesn't support
  - Sending small amounts to international contractors
  - Holding currency for future expenses
  - As a backup/secondary account

When to use Mercury:
  - Primary operating account
  - Receiving Stripe payouts
  - Paying bills
  - Building cash reserves (interest-bearing)
  - EUR/GBP transactions
```

### Wise Setup for SaaS

```yaml
Step 1: Create Wise Business account
  - Go to wise.com/business
  - Sign up with business email
  - Select: "I'm a business owner"

Step 2: Verify business
  - Upload business registration
  - Provide owner identification
  - Wait for verification (1-3 days)

Step 3: Open balances
  - Add USD, EUR, GBP balances
  - Get local bank details for each
  - These are REAL local bank accounts (sort code, account number, IBAN)

Step 4: Connect Stripe
  - In Stripe, add Wise as a payout account
  - Or: Manually transfer from Wise for lowest fees

Step 5: Set up auto-conversion
  - Auto-convert EUR revenue to USD
  - Set target rate alerts
  - Batch payments for contractors

Cost example:
  Receive €5,000 from EU customer:
    Wise: Convert at real rate (~1.08) = $5,400
    Fee: 0.5% = $27
    Net: $5,373
    
  Traditional bank:
    Rate: ~1.04 (bank markup)
    $5,200
    Wire fee: $15
    Correspondent bank fee: $20
    Net: $5,165
    
  Savings with Wise: ~$208 on €5K
```

---

## Part 4: Brex — The Growth-Stage Bank

### Overview

```yaml
Best for: Growth-stage SaaS ($50K+ MRR, has employees)
Cost: $0/month (if > $50K in account) or $5/month
Banking license: FDIC insured (through partners)
Key focus: Corporate cards and spend management

Features:
  - Business checking account
  - Corporate cards (15-20x higher limits than Mercury)
  - Travel and expense management
  - Bill pay
  - Integration with accounting tools
  - Rewards (points on spend)
  - No foreign transaction fees
  - Up to $5M FDIC insurance (sweep program)
```

### Brex for Solo Founders

```yaml
IS IT RIGHT FOR A SOLO FOUNDER?

Probably not until you're larger.

Why:
  - $5/month fee if below $50K balance
  - Focuses on corporate card (not banking)
  - Must connect to your bank (Brex isn't your primary bank)
  - Better for teams with employees

When to switch to Brex:
  - You have employees and need expense management
  - You travel frequently and want travel rewards
  - You have $50K+ in cash and want sweep insurance
  - You need high-limit corporate cards

Solo founder recommendation:
  - Mercury for banking
  - Wise for international
  - Brex only if/when you have employees
```

---

## Part 5: Relay — The Bookkeeping-First Bank

### Overview

```yaml
Best for: Solo founders who want built-in bookkeeping
Cost: FREE
Banking license: FDIC insured (through partners)
Target: Small businesses, contractors

Features:
  - Unlimited checking accounts (separate accounts for different purposes)
  - Envelopes (set aside money for taxes, expenses)
  - Built-in bookkeeping (categorize transactions)
  - QuickBooks and Xero integration
  - Bill pay
  - Virtual and physical cards
  - Joint accounts

### Relay for Solo Founders

```yaml
Why choose Relay:
  - Best "envelope" system (save for taxes automatically)
  - Separate accounts for different purposes (operating, taxes, payroll)
  - Built-in categorization (reduces bookkeeping work)
  - Free bill pay
  - Good for freelancers and simple businesses

Why NOT to choose Relay:
  - No multi-currency (USD only)
  - No international wire capability (domestic only)
  - Limited integration with SaaS tools
  - No API access (basic)
  - No interest on cash

When to use Relay:
  - US-only revenue
  - You want the envelope/tax savings feature
  - You don't need international banking
  - You want simpler bookkeeping

Solo founder recommendation:
  - Mercury + Wise for international SaaS
  - Relay for US-only, domestic SaaS
```

---

## Part 6: Comparison Matrix

```yaml
                 | Mercury     | Wise          | Brex         | Relay
─────────────────|─────────────|───────────────|──────────────|───────────
Monthly Fee      | $0          | $0            | $0-$5        | $0
Multi-Currency   | EUR, GBP, CAD| 50+ currencies| USD only     | USD only
Intl. Wires      | Free        | 0.3-1% fee    | $0           | N/A
Virtual Cards    | Unlimited   | Yes           | Yes          | Yes
Physical Cards   | Yes         | Yes           | Yes          | Yes
Interest         | 4%+ APY     | —             | —            | —
API              | Excellent   | Good          | Good         | Basic
Stripe Integrate | Native      | Manual        | Manual       | Manual
QuickBooks       | Yes         | Yes           | Yes          | Yes
US Entity Needed | Yes         | No            | Yes          | Yes
FDIC Insurance   | $250K       | N/A           | $5M sweep    | $250K
Customer Support | Email       | Chat + Email  | Phone + Email| Chat + Email
Best For         | Primary bank| Transfers     | Cards/Spend  | Bookkeeping
```

---

## Part 7: Multi-Currency Strategy

### The Three-Currency Setup

For a solo founder with international revenue:

```yaml
Account 1: Mercury (Primary Operating)
  Currencies: USD, EUR, GBP
  Purpose:
    - Receive Stripe payouts (USD and EUR)
    - Pay US contractors and expenses
    - Hold cash reserves in treasury (4% APY)
    - Pay US taxes quarterly
    
Account 2: Wise (Secondary / Transfers)
  Currencies: AUD, CAD, JPY, etc.
  Purpose:
    - Receive payments from countries Mercury doesn't support
    - Convert to USD at best rates
    - Pay international contractors
    - Hold small amounts for future expenses
    
Account 3: Local Bank (If needed)
  Currency: Local
  Purpose:
    - Physical branch access (if needed for specific services)
    - Backup if Mercury has issues
    - Business credit card for large purchases
```

### Currency Conversion Strategy

```yaml
Goal: Minimize conversion fees and FX risk.

Strategy 1: Keep and spend in local currency
  If you have EUR revenue and EUR expenses, keep them matched
  No conversion needed: Revenue in → Expenses out

Strategy 2: Batch conversions
  Convert large amounts weekly/monthly (lower % fee)
  Don't convert small amounts daily (fees add up)

Strategy 3: Use Wise for conversion
  Best rates (real mid-market rate + small fee)
  Much better than bank rates (which have hidden markup)

Strategy 4: Hold reserves
  Keep 1-2 months of expenses in each major currency
  Convert only what you need for USD expenses

Example:
  Monthly revenue: $5K USD + €3K EUR + £1K GBP
  Monthly expenses: $4K USD + $1K EUR (contractors)
  
  Strategy:
    - Keep €3K in EUR (pay €1K contractor, keep €2K for future)
    - Convert £1K to USD (when rate is favorable)
    - Hold $5K in USD treasury (earning 4% APY)
    
  Conversion: Only £1K/month = minimal fees
  No unnecessary USD/EUR conversion
```

### Hedging Against Currency Fluctuation

```yaml
Risk: EUR drops 10% against USD
  Your €3K revenue becomes worth $2,700 less
  Your expenses are in USD — you lose purchasing power

Simple hedging for solo founders:
  
  1. Keep expenses in same currency as revenue (if possible)
    If you have EUR revenue, find EUR expenses
  
  2. Maintain a "currency buffer" (3 months expenses in each currency)
    Smooths out short-term fluctuations
  
  3. Don't convert currency speculatively
    Convert when you need USD, not when "the rate looks good"
  
  4. Consider USD as base currency (if US-based)
    Most of your expenses are likely in USD
    Convert revenue to USD regularly
```

---

## Part 8: Banking Operations for Solo Founders

### Account Structure

```yaml
Recommended account setup:

Accounts (all in Mercury):
  1. Operating Account (USD)
    - Stripe payouts arrive here
    - Pay monthly expenses
    - Pay your salary/draw
  
  2. Tax Reserve Account (USD)
    - Automatic transfers: 25-30% of revenue
    - Use for quarterly estimated tax payments
    - "Out of sight, out of mind"
  
  3. Emergency Fund (USD) — Mercury Treasury
    - 6 months of business expenses
    - Earning 4%+ APY
  
  4. EUR Account (Mercury)
    - Receive EU Stripe payouts
    - Pay EU contractors
    - Convert to USD when needed

  5. GBP Account (Mercury or Wise)
    - Receive UK payments
    - Pay UK contractors
```

### Payment Flows

```yaml
Revenue flows:

  Stripe (US) → Mercury USD Account (instant)
  Stripe (EU) → Mercury EUR Account (next day)
  Direct invoice (EUR) → Wise EUR → Mercury EUR
  Direct invoice (other) → Wise Account → Convert → Mercury USD

Expense flows:

  US contractors → Mercury USD (ACH, free)
  EU contractors → Mercury EUR (SEPA, free)
  UK contractors → Mercury GBP (Faster Payments, free)  
  Asian contractors → Wise (low fee, good rates)
  
  SaaS tools → Mercury Virtual Cards (free, per-merchant)
  Hosting (AWS/GCP) → Mercury Virtual Cards
  Domain/SSL → Mercury Virtual Cards

Tax payments:

  Mercury USD → IRS (ACH, free)
  Mercury USD → State tax authority (ACH or check)
  
  Automatic transfer: 25% of each Stripe payout → Tax Reserve
```

### Cash Management

```yaml
Rule of thumb for solo founders:

1. Keep 1 month of expenses in checking ($0 interest, but liquid)
2. Keep 3 months in high-yield savings (Mercury Treasury, 4%+ APY)
3. Keep 6+ months in diversified: treasury + money market
4. Keep investment money separate (don't invest business cash reserves)

Cash allocation at different stages:

Pre-revenue ($30K savings):
  100% in Mercury checking (need liquidity)
  $0 interest (too small to matter)

$5K MRR ($40K cash):
  $10K checking (1 month)
  $20K Mercury Treasury (4% APY = $800/year)
  $10K buffer (growth investment fund)

$20K MRR ($100K cash):
  $20K checking (1 month)
  $50K Mercury Treasury (4% APY = $2,000/year)
  $30K growth fund (ads, hiring, experiments)
```

---

## Part 9: Banking by Business Stage

### Stage 1: Pre-Revenue

```yaml
Recommended setup:
  Primary: Mercury (free, no minimum)
  Secondary: None needed yet

What you need:
  - Business checking account (Mercury)
  - Virtual card for expenses
  - Separate from personal (tax purposes)
  - Stripe integration (for when you launch)

Monthly cost: $0
Setup time: 1-2 days

Checklist:
  ☐ Open Mercury account
  ☐ Get physical card (if needed)
  ☐ Set up virtual card for subscriptions
  ☐ Connect to Stripe (even before launch)
  ☐ Set up QuickBooks/Xero integration
```

### Stage 2: Early Revenue ($1K - $10K MRR)

```yaml
Recommended setup:
  Primary: Mercury
  Secondary: Wise (for international)

What you need:
  - Multi-currency (if you have international customers)
  - Tax reserve (set up automatic transfers)
  - Virtual cards for tools
  - Bill pay

Monthly cost: $0
Setup time: Already set up

Checklist:
  ☐ Set up tax reserve account (auto-transfer 25%)
  ☐ Open Wise account if international customers
  ☐ Create virtual cards for each tool subscription
  ☐ Set up recurring bill payments
  ☐ Review bank statements monthly for errors
```

### Stage 3: Growth ($10K - $50K MRR)

```yaml
Recommended setup:
  Primary: Mercury
  Secondary: Wise
  Cash reserves: Mercury Treasury

What you need:
  - Interest on cash (4% APY makes a difference at $50K+)
  - Multiple accounts (operating, tax, reserve)
  - Automated transfers
  - Integration with accounting

Monthly cost: $0
Cash management:
  - 25% tax reserve (auto-transfer)
  - 20% treasury (build emergency fund)
  - 55% operating (pay expenses + draw)

Checklist:
  ☐ Open Mercury Treasury (for emergency fund)
  ☐ Set up auto-transfers to tax reserve
  ☐ Schedule monthly cash review
  ☐ Automate contractor payments
  ☐ Review currency strategy (minimize conversion fees)
```

### Stage 4: Scaling ($50K+ MRR)

```yaml
Recommended setup:
  Primary: Mercury
  Secondary: Wise + possibly Brex
  Cash reserves: Mercury Treasury + business savings account
  Maybe: Silicon Valley Bank or similar (for lending relationships)

What you need:
  - Higher cash limits (FDIC sweep programs)
  - Lending access (credit lines, loans)
  - Expense management (if hiring)
  - Payroll integration

Monthly cost: $0 - $50
Cash management:
  - Keep 12+ months operating expenses
  - Invest excess in treasury/money market
  - Consider real estate or other diversification

Checklist:
  ☐ Review FDIC coverage ($250K per bank — use sweep for larger)
  ☐ Consider Brex if hiring (expense cards for team)
  ☐ Build banking relationship for future debt
  ☐ Set up automated financial reporting
  ☐ Consider international banking entity (if $100K+ EUR/GBP revenue)
```

---

## Quick Reference

```yaml
BANKING CHEAT SHEET

YOUR BANKING STACK:

Solo Founder (Standard):
  - Mercury: Primary bank, USD, EUR, GBP, free wires, 4% interest
  - Wise: Secondary for 50+ currency transfers
  - Cost: $0/month

Growth Stage (with team):
  - Mercury: Primary bank
  - Brex: Corporate cards, expense management
  - Wise: International transfers
  - Cost: $0-$50/month

MULTI-CURRENCY BEST PRACTICES:
  - Keep EUR to pay EUR expenses
  - Convert only what you need for USD spending
  - Use Wise for best conversion rates
  - Batch conversions (don't convert daily)

CASH MANAGEMENT:
  1 month expenses: Checking (Mercury)
  3 months expenses: Treasury (Mercury Treasury, 4%+ APY)
  6+ months expenses: Diversified (treasury + money market + maybe index funds)

MONTHLY BANKING REVIEW (15 minutes):
  ☐ Review all transactions for errors
  ☐ Check foreign exchange rates (convert if favorable)
  ☐ Update tax reserve (25-30% of revenue)
  ☐ Review cash balance vs 3-month target
  ☐ Check for new bank features/tools

SETUP ORDER:
  Day 1: Mercury (primary checking + Stripe connect)
  Week 1: Wise (international transfers)
  Month 1: Mercury Treasury (interest on cash)
  As needed: Additional accounts for specific needs
```

The right banking setup saves you money (free accounts, better FX rates, interest on cash) and time (automated transfers, integrations, virtual cards). Set it up once, and you'll never think about banking again.