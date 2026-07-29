# Business Entity Setup for Solo SaaS Founders

A comprehensive comparison of LLC vs. S-Corp vs. C-Corp for solo SaaS founders — covering liability, taxation, fundraising, compliance, and the right choice at each stage of your journey.

---

## Part 1: The Entity Decision Framework

### What Each Entity Does

```yaml
Entity Type | Liability Protection | Taxation      | Complexity | Cost
────────────|──────────────────────|───────────────|────────────|───────
Sole Prop   | NONE                 | Personal only | Simplest   | $0
LLC         | YES                  | Personal/S-Corp | Simple   | $100-$800/yr
S-Corp      | YES                  | Pass-through  | Moderate   | $500-$2K/yr
C-Corp      | YES                  | Double taxation | Complex   | $1K-$5K/yr

For a solo SaaS founder:
  - Stage 1 (Pre-revenue): Sole proprietorship — don't form anything
  - Stage 2 ($1K - $10K MRR): LLC — liability protection, simple
  - Stage 3 ($10K - $50K MRR): S-Corp election — tax savings
  - Stage 4 (Fundraising): C-Corp — investor requirement
```

### The Liability Question

```yaml
As a SaaS founder, what are you liable for?

Risks with no entity:
  - Contract disputes: Customer sues you personally
  - IP infringement: Your code uses unlicensed library
  - Data breach: Customer data exposed, they sue
  - Partnership disputes: Co-founder disagreement
  - Employee issues: If you ever hire

Reality check for solo founders:
  Most SaaS businesses never face a lawsuit
  BUT: One lawsuit can bankrupt you personally
  LLC/C-Corp protects your personal assets (house, savings)
  Cost of formation ($100-$500) is cheap insurance

Exception: If you're doing nothing illegal, writing original code,
and have standard terms of service — the risk is low.
But don't bet your house on it.
```

---

## Part 2: LLC — The Solo Founder Default

### Why LLC Is Usually Right

```yaml
Best for: $0 - $10K MRR, no fundraising plans
Cost: $100 - $800 initial filing + annual state fees
Complexity: Low (10-15 minutes online in most states)

Pros:
  - Personal asset protection
  - Pass-through taxation (file on personal taxes)
  - Simple to set up and maintain
  - Flexible profit distribution (pay yourself whenever)
  - Less paperwork than S-Corp or C-Corp
  - Can elect S-Corp taxation later (best of both)

Cons:
  - Self-employment tax on ALL profit (15.3%)
  - Not suitable for VC funding (investors want C-Corp)
  - Varies by state (some states tax LLCs heavily)
  - Must maintain separate bank accounts and records
  - Some states require annual reports/fees
```

### LLC Formation Process

```yaml
Step 1: Choose your state
  - Your home state (simplest, cheapest)
  - Delaware (if fundraising — investors prefer Delaware)
  - Wyoming/Nevada (lower fees, more privacy)

  Solo founder recommendation: Your home state.
  Unless fundraising — then Delaware.

Step 2: Choose a name
  - Must not conflict with existing businesses in your state
  - Check your state's Secretary of State website
  - Include "LLC" or "Limited Liability Company" in name

Step 3: File Articles of Organization
  - Online through Secretary of State website
  - Cost: $50 - $500 (varies by state)
  - Information needed:
    - Business name and address
    - Registered agent (you or a service)
    - Purpose of business
    - Management structure (member-managed)

Step 4: Create an Operating Agreement
  - Not required in all states, but HIGHLY recommended
  - Defines ownership, management, profit distribution
  - Template available online (free)
  - For solo founder: Simple 5-page document is fine

Step 5: Get an EIN (Employer Identification Number)
  - Free from IRS (online, 10 minutes)
  - Required for business bank account
  - Required if you'll have employees or contractors

Step 6: Register for state taxes
  - Sales tax registration (if selling in your state)
  - State income tax registration
  - Local business licenses (if required)

Step 7: Open business bank account
  - Separate from personal accounts (REQUIRED for liability protection)
  - Compare: Mercury (free, fintech), Brex (free), local bank

Total time: 1-3 days
Total cost: $100 - $1,500 (varies by state and complexity)
```

### Annual LLC Maintenance

```yaml
Annual requirements:
  - Annual report: $0 - $800 (varies by state)
  - Registered agent: $0 - $300/year (if using service)
  - State franchise tax: $0 - $800 (California: $800 minimum!)
  - Business license renewal: $0 - $100
  - Tax return: $100 - $500 (DIY) or $500 - $1,500 (CPA)

States with high LLC costs:
  - California: $800 minimum franchise tax + $20 annual filing
  - New York: $9 filing fee + publication costs ($1K-$2K in NYC!)
  - Texas: $0 filing but franchise tax on revenue > $1.23M
  - Delaware: $300 annual franchise tax

States with low LLC costs:
  - Wyoming: $100 filing, $50 annual, no state income tax
  - Nevada: $425 filing, $350 annual, no state income tax
  - New Mexico: $50 filing, $0 annual
  - Colorado: $50 filing, $10 annual
```

---

## Part 3: S-Corp for Tax Savings

### What Is an S-Corp?

An S-Corp is NOT a business entity type — it's a TAX ELECTION. You first form an LLC or C-Corp, then file Form 2553 with the IRS to elect S-Corp taxation.

### The Tax Advantage

```yaml
The key: S-Corp allows you to split profit into:
  1. Salary (subject to payroll/SE tax) — must be "reasonable"
  2. Distributions (NOT subject to SE tax) — tax-free for self-employment

Example:
  Profit: $100,000
  
  As LLC:
    SE Tax: $100,000 × 15.3% = $15,300
    Income Tax (24% bracket): ~$20,000
    Total: ~$35,300

  As S-Corp (reasonable salary: $50K):
    SE Tax on salary: $50K × 15.3% = $7,650
    No SE tax on distributions: $0
    Payroll processing: $1,000/year
    Income tax: ~$20,000 (same)
    Total: ~$28,650
  
  SAVINGS: ~$6,650/year

Break-even analysis:
  S-Corp costs: $1,000 - $2,000/year extra
  Tax savings: ~$6,000 on $100K profit (varies)
  Break-even profit: ~$60K/year ($5K/month profit)
```

### When to Elect S-Corp

```yaml
Do NOT rush to S-Corp. Only worth it when:

FRANKENSTEIN METRICS CONSIDERATIONS:

1. Net profit > $60K/year
  Below $60K: The tax savings don't justify the complexity
  $60K-$100K: Marginal benefit, consider carefully
  $100K+: Clear benefit, usually worth it

2. You have steady, predictable profit
  S-Corp requires consistent salary payments
  If profit fluctuates wildly, LLC is simpler

3. You plan to stay in business 2+ years
  One-time setup costs (~$1K) amortized over multiple years

4. You understand payroll
  Must run payroll (even if it's just you)
  Must pay yourself "reasonable salary"
  Must file quarterly payroll taxes

5. You're willing to do more paperwork
  Quarterly payroll tax returns
  Annual S-Corp tax return (Form 1120-S)
  Separate tax return from personal (more expensive)
```

### The "Reasonable Salary" Rule

```yaml
IRS requires S-Corp owners to pay themselves "reasonable compensation"
You can't avoid ALL SE tax by taking only distributions

What's "reasonable"?
  - Industry standards for similar work
  - What you'd pay an employee to do your job
  - Your qualifications and experience
  - Time spent and responsibilities

Guidelines:
  - Minimum: 30-40% of net profit as salary
  - Maximum: 100% as salary (but that defeats S-Corp purpose)
  - Typical: 40-60% as salary for solo SaaS founders
  
  Example: $100K profit
    Too aggressive ($20K salary): IRS audit risk
    Conservative ($60K salary): Less savings but safer
    Balanced ($45K salary): Common for solo founders

What NOT to do:
  - $0 salary, 100% distributions (IRS will reclassify)
  - Salary dramatically below market rate
  - Salary that doesn't match your workload
```

### S-Corp Compliance Requirements

```yaml
Setup:
  - Form LLC first ($100-$500)
  - File Form 2553 with IRS (within 75 days of formation or by March 15)
  - Get EIN (free from IRS)
  - Set up payroll (Gusto, ADP, or DIY)

Ongoing:
  - Pay yourself every month (or at least quarterly)
  - Run payroll (withhold FICA, income tax)
  - File Form 941 quarterly (payroll tax)
  - File Form 940 annually (FUTA)
  - File Form 1120-S annually (S-Corp return, due March 15)
  - Issue W-2 to yourself by January 31
  - Issue Schedule K-1 to shareholders
  
  Annual payroll processing: $500 - $1,500 (Gusto, SimplyHired)
  Annual tax return: $500 - $1,500 (CPA)

Late S-Corp Election:
  Can file late with IRS Form 2553
  Must show "reasonable cause" for late filing
  Possible if you haven't filed your first corporate return yet
```

---

## Part 4: C-Corp — For Fundraising

### What Is a C-Corp?

A C-Corporation is a separate legal entity that pays its own taxes. It's the standard structure for venture-backed startups.

### Why Investors Want C-Corp

```yaml
1. Preferred stock
  C-Corps can issue different classes of stock
  Investors want preferred shares (liquidation preference, etc.)
  LLCs can't do this cleanly

2. Tax treatment
  C-Corp tax structure is better for growing companies
  Losses offset future profits
  No self-employment tax issues
  S-Corp has ownership restrictions (max 100 shareholders, US only)

3. Familiarity
  Every VC has done 100+ C-Corp deals
  Standard documents exist
  No education needed

4. Option pool
  Stock options for employees are standard
  C-Corp structure supports this cleanly
  LLC/S-Corp equity is more complex

5. Delaware
  VCs prefer Delaware C-Corps
  Delaware has well-established corporate law
  Predictable legal outcomes
```

### The Double Taxation Problem

```yaml
C-Corp tax:
  Level 1: Corporation pays tax on profit (21% federal)
  Level 2: You pay tax on dividends or salary (personal rates)

Example:
  Corp profit: $100,000
  Corp tax (21%): $21,000
  After-tax profit: $79,000
  Distributed to you as dividend:
  Dividend tax (15%): $11,850
  Your net: $67,150
  
  Effective tax rate: ~33%
  
  vs S-Corp: ~24%
  vs LLC: ~30%

HOWEVER:
  Most VC-backed startups don't pay dividends
  They reinvest everything into growth
  So double taxation only matters when profitable
  And most pre-profit companies prefer C-Corp losses (can offset future income)
```

### C-Corp vs S-Corp for Fundraising

```yaml
If you plan to raise VC:

S-Corp is NOT suitable because:
  - Max 100 shareholders
  - All shareholders must be US citizens/residents
  - Can only have ONE class of stock
  - VCs rarely invest in S-Corps (causes immediate tax issues)

C-Corp is REQUIRED for:
  - Venture capital investment
  - Multiple share classes
  - Foreign investors
  - Employees with stock options

If you're not raising money:
  S-Corp is better (no double taxation, lower compliance)
```

### C-Corp Setup Process

```yaml
Step 1: Incorporate in Delaware
  - Most VC-friendly state
  - Established corporate law
  - Many corporate lawyers familiar with Delaware law
  - Can incorporate online in 30 minutes

Step 2: Choose a Registered Agent
  - Required for Delaware corporations
  - Service: $100-$300/year
  - Options: CSC, CT Corp, Harvard Business Services

Step 3: File Certificate of Incorporation
  - Online through Delaware Division of Corporations
  - Cost: $89 filing fee
  - Provide: Company name, purpose, authorized shares

Step 4: Draft Bylaws
  - Internal rules for corporate governance
  - Standard template from your lawyer

Step 5: Issue Stock
  - 10M authorized shares typical
  - Issue shares to founder(s)
  - 83(b) election (file within 30 days of receiving restricted stock)

Step 6: Get EIN
  - Same as LLC — free from IRS

Step 7: File S-Corp election (optional)
  - If you want S-Corp tax treatment temporarily
  - File Form 2553
  - Revoke before VC round (investors need C-Corp)

Total cost: $500 - $4,000 (legal fees + filing fees)
```

### C-Corp Maintenance

```yaml
Annual requirements:
  - Delaware franchise tax: $175 - $200,000 (based on shares)
  - Delaware annual report: $50
  - Registered agent: $100-$300/year
  - Board meetings (at least annual, with minutes)
  - Corporate tax return (Form 1120): $1,000-$5,000 (CPA)
  - State tax return (if doing business in another state)

Estimated annual cost:
  - Delaware C-Corp (no business in DE): $225 - $500/year
  - Delaware C-Corp (business in CA): $800 minimum + $225 = $1,025+
  - Delaware C-Corp (business in NY): $2,000+ (publication costs)

For a pre-revenue startup:
  ~$1,000-$2,000/year in compliance costs
  This is why C-Corp is NOT for pre-revenue solo founders
```

---

## Part 5: State-by-State Comparison

### The Worst States for SaaS Entities

```yaml
CALIFORNIA:
  - LLC: $800 minimum franchise tax every year (even with $0 revenue!)
  - C-Corp: $800 minimum franchise tax
  - Also: State income tax (8.84% for C-Corp)
  - Gross receipts tax (not applicable to most SaaS)
  
  → Avoid forming in CA if possible
  → Form in Delaware or Wyoming instead
  → Must still register in CA if you live there

NEW YORK:
  - LLC: Publication requirement (publish in 2 newspapers for 6 weeks)
  - Cost: $1,000 - $2,500 (NYC) or $500 - $1,500 (rest of state)
  - Also: $25 annual filing fee + $300+ publication fee
  
  → Painful for early stage
  → Still register in DE if you live in NY

TEXAS:
  - No state income tax (good for you and business)
  - No franchise tax for revenue < $1.23M (most solo founders exempt)
  - LLC: $300 filing fee
  - Simple, low-cost
  
  → Good state if you live there
```

### The Best States for SaaS Entities

```yaml
WYOMING:
  - $100 filing fee
  - $50 annual report
  - No state income tax
  - No franchise tax
  - Privacy (anonymous LLCs allowed)
  - No publication requirement
  
  → Best for: Founders who don't live in WY but want low costs
  → Must still register in your home state (additional cost)

NEVADA:
  - $425 filing fee
  - $350 annual fee
  - No state income tax
  - No franchise tax
  - Privacy protections
  
  → Similar to Wyoming, more expensive

DELAWARE:
  - $89 filing fee
  - $175-$300 annual franchise tax (typical for startups)
  - No state income tax for DE-only businesses
  - Best legal system for corporations
  - Investor preference
  
  → Best for: Fundraising companies
  → Overkill for lifestyle businesses

COLORADO:
  - $50 filing fee
  - $10 annual report
  - Flat 4.4% state income tax
  - Simple, low-cost
  - Good for: Local Colorado founders
```

### The Foreign Qualification Requirement

```yaml
If you form in Delaware but live in California:
  You must "foreign qualify" in California
  This means: Register as a foreign entity doing business in CA
  Cost: $800 minimum franchise tax (yes, you pay it)

This applies to EVERY state you do business in:
  "Doing business" = having a physical presence (home office, employees)
  NOT = having customers there (that's sales tax, not entity registration)

Foreign qualification checklist:
  - File with Secretary of State in your home state
  - Pay registration fee ($50 - $500)
  - Appoint registered agent in that state
  - File annual reports
  - Pay state taxes and fees

Solo founder nightmare:
  Form LLC in Wyoming ($100) to save money
  But live in California
  Must foreign qualify in CA ($800/year)
  Total: $100 (WY) + $800 (CA) = $900/year vs $800 (CA LLC only)
  
  → Just form in your home state unless fundraising
```

---

## Part 6: The Solo Founder Entity Roadmap

### Stage-Based Recommendations

```yaml
Stage 1: Pre-Revenue — No Entity (Sole Proprietorship)
  Months: 0-6
  Structure: Nothing formal
  Bank account: Personal (or free business account)
  Liability: None (but risk is low pre-revenue)
  Taxes: Schedule C with personal return
  Cost: $0

Stage 2: Early Revenue ($0 - $3K MRR) — LLC
  Months: 6-18
  Structure: Single-member LLC in your home state
  Bank account: Mercury or Brex
  Liability: Asset protection
  Taxes: Schedule C (pass-through)
  Cost: $100-$800 + annual state fees
  ✅ Form LLC when you get your first paying customer
  ✅ Get EIN and business bank account immediately

Stage 3: Growing ($3K - $10K MRR) — LLC + S-Corp Election
  Months: 12-24
  Structure: S-Corp (elect on existing LLC)
  Bank account: Same
  Liability: Same
  Taxes: S-Corp (salary + distributions)
  Cost: $500-$2K/year extra (payroll + tax returns)
  ✅ Elect S-Corp when profit > $60K/year ($5K MRR at 50% margin)
  ✅ Set up payroll (Gusto)
  ✅ Pay reasonable salary

Stage 4: Fundraising — C-Corp
  Months: Any (when raising institutional capital)
  Structure: Delaware C-Corp
  Bank account: Same + maybe Silicon Valley Bank
  Liability: Same + board oversight
  Taxes: C-Corp (double taxation)
  Cost: $1K-$5K/year extra (legal + franchise tax)
  ✅ Form C-Corp when you have a term sheet
  ✅ Use a lawyer for conversion
  ✅ File 83(b) election for founder shares
```

### The "Do Nothing" Option

```yaml
Many solo founders never form an entity. They operate as sole proprietors.

This is fine IF:
  - Revenue < $50K/year
  - No employees or contractors
  - Minimal risk profile
  - Not raising funding
  - Comfortable with personal liability

This is DANGEROUS IF:
  - You have significant revenue
  - You process/store customer data
  - You have contracts with enterprise customers
  - You have employees
  - You face any lawsuit risk

The vast majority of solo SaaS founders should form an LLC.
It costs $100-$500 once and protects your personal assets forever.
```

---

## Part 7: Entity Conversion (Changing Later)

### Sole Prop → LLC

```yaml
Process:
  - Form LLC in your state
  - Get EIN for LLC (if different from your SSN filing)
  - Transfer business assets to LLC
  - Update contracts (change from your name to LLC name)
  - Update payment processor (Stripe)
  - Close sole prop bank account, open LLC account

Tax impact: None (disregarded entity for tax purposes)
Cost: $100-$500 (formation)
Complexity: Low

Timing: Do this immediately when you get your first paying customer
```

### LLC → S-Corp

```yaml
Process:
  - Ensure LLC is already formed
  - File Form 2553 with IRS (within 75 days of formation or by March 15)
  - Set up payroll system
  - Begin paying yourself salary

Tax impact: Significant (see earlier — 15.3% SE tax savings)
Cost: $500-$2K/year (payroll + tax returns)
Complexity: Medium

Timing: When net profit > $60K/year
```

### LLC/S-Corp → C-Corp

```yaml
Process:
  - Form new Delaware C-Corp
  - Transfer assets from old entity to new C-Corp
  - Old entity dissolves (or becomes subsidiary)
  - Issue new shares
  - File 83(b) election within 30 days

Tax impact: 
  - Can be tax-free (Section 351 exchange)
  - May trigger tax on appreciated assets
  - Need tax attorney to structure correctly

Cost: $5K-$15K in legal and accounting fees
Complexity: High — use a lawyer

Timing: When you have a term sheet in hand
```

---

## Part 8: Quick Decision Guide

### The Entity Decision Flowchart

```yaml
Are you raising VC money?
├── YES → Delaware C-Corp
└── NO → Are you profitable (> $5K/month net)?
    ├── YES → Is your profit > $60K/year?
    │   ├── YES → LLC with S-Corp election
    │   └── NO → LLC
    └── NO → Are you pre-revenue?
        ├── YES → Sole proprietorship (wait)
        └── NO → LLC (low revenue)
```

### Quick Reference Card

```yaml
ENTITY TYPE          | SOLE PROP   | LLC         | S-Corp        | C-Corp
─────────────────────|─────────────|─────────────|───────────────|─────────────
Liability Protection | ❌         | ✅           | ✅            | ✅
Pass-through Tax    | ✅          | ✅           | ✅            | ❌
SE Tax Savings       | ❌         | ❌           | ✅            | N/A
VC-Friendly          | ❌         | ❌           | ❌            | ✅
Formation Cost       | $0          | $100-$800    | $500-$2K      | $500-$4K
Annual Cost          | $0          | $0-$800      | $500-$2K      | $500-$5K
Complexity           | None        | Low          | Medium        | High
Paperwork            | Schedule C  | Schedule C   | 1120-S + Payroll | 1120 + Minutes
Can Convert To       | LLC, C-Corp | S-Corp, C-Corp | C-Corp      | Nothing (hard)
Best For             | Pre-revenue | $0-$10K MRR  | $10K-$50K MRR | Fundraising
```

### The Question to Ask Yourself

```
"What's the worst that happens if I don't form an entity?"

If the answer is "I lose my house in a lawsuit" -> Form an LLC.
If the answer is "I miss out on tax savings" -> Elect S-Corp later.
If the answer is "I can't raise VC" -> Form C-Corp when needed.
If the answer is "Nothing, really" -> Stay a sole proprietor.

Most solo founders should:
  1. Start as sole proprietor (pre-revenue)
  2. Form LLC when they get first paying customer
  3. Elect S-Corp when profit > $60K/year
  4. Convert to C-Corp only if raising VC

You can always change entities later.
The wrong entity costs money. The wrong NON-entity costs your house.
```

The most common mistake solo founders make is overcomplicating their entity structure. A simple LLC in your home state is right for 90% of solo SaaS businesses. Don't form a Delaware C-Corp unless you're raising venture capital — the complexity and cost aren't worth it for a lifestyle business.