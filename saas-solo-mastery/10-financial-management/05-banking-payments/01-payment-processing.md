# Payment Processing for SaaS

A comprehensive guide to choosing and managing payment processing for your SaaS — Stripe vs. Paddle vs. LemonSqueezy, subscription management, dunning strategies, and maximizing your revenue per transaction.

---

## Part 1: The Payment Processing Landscape

### What a Payment Processor Does

```yaml
Core functions:
  1. Charge the customer's card
  2. Handle subscription billing (recurring charges)
  3. Manage failed payments (dunning)
  4. Calculate and remit sales tax/VAT
  5. Handle refunds and disputes
  6. Provide customer portal for billing management

For SaaS, you also need:
  - Subscription management (plans, tiers, upgrades, downgrades)
  - Proration (mid-cycle changes)
  - Coupons and discounts
  - Trial management
  - Invoice generation
  - Revenue reporting
```

### The Three Options

```yaml
Option 1: Direct Processor (Stripe)
  - You are the "Merchant of Record"
  - You handle tax compliance
  - You receive gross payments, pay fees
  - Best for: US-only, B2B, willing to handle tax

Option 2: Merchant of Record (Paddle, LemonSqueezy)
  - They are the "Merchant of Record"
  - They handle ALL tax compliance
  - They pay you net of fees and taxes
  - Best for: International sales, B2C, hate tax compliance

Option 3: All-in-One (Chargebee, Recurly, Stripe Billing)
  - Subscription management layer on top of payment processor
  - Handles recurring billing, invoices, customer portal
  - Integrates with Stripe, PayPal, etc.
  - Best for: Complex billing needs, multiple payment methods
```

---

## Part 2: Stripe — The Standard

### Why Stripe Dominates SaaS

```yaml
Market share: ~70% of SaaS companies use Stripe
Integration: Best developer experience
Features: Everything a SaaS needs built in
Pricing: Transparent, no hidden fees

Key features for SaaS:
  - Subscriptions API (plans, tiers, trials)
  - Customer portal (self-serve billing management)
  - Invoicing (automated or manual)
  - Tax (calculation and remittance)
  - Connect (marketplace payouts)
  - Sigma (SQL-based reporting)
  - Radar (fraud prevention)
  - Billing (usage-based, metered)
```

### Stripe Pricing

```yaml
Standard pricing:
  2.9% + $0.30 per successful card charge
  +1.5% for international cards
  +1% if currency conversion needed

Subscription-specific:
  Same per-transaction pricing
  No monthly fee (pay as you go)

Additional costs:
  - Stripe Tax: 0.5% of transaction volume
  - Stripe Sigma: Free (limited) or custom (pricing)
  - Stripe Connect: 0.25% + $0.25 (platform fee)
  - Chargebacks: $15 (refundable if you win)

International:
  - Country-specific rates
  - EU: 1.4% + €0.25 (intra-EU)
  - UK: 1.4% + £0.20
  - Australia: 1.4% + $0.30 AUD

Example costs at different volumes:
  $1K MRR (20 customers × $50):
    20 × (2.9% × $50 + $0.30) = 20 × ($1.45 + $0.30) = $35
    Effective rate: 3.5%
    
  $10K MRR (200 customers × $50):
    200 × ($1.45 + $0.30) = $350
    Effective rate: 3.5%
    
  $50K MRR (1,000 customers × $50):
    1,000 × ($1.45 + $0.30) = $1,750
    Effective rate: 3.5%
    
  Volume discounts available at $1M+/month
```

### Stripe Setup for SaaS

```yaml
1. Create Stripe account
  - Sign up at stripe.com
  - Verify identity (need SSN, ID)
  - Link bank account

2. Set up products and prices
  - Each plan = a "Product"
  - Each tier = a "Price" (recurring or one-time)
  - Example:
    Product: "SaaS Pro"
    Price 1: "Monthly" — $49/month
    Price 2: "Annual" — $490/year ($40.83/month)

3. Create a customer portal (built-in)
  - Customers can:
    - View current plan
    - Upgrade/downgrade
    - Update payment method
    - View invoices
    - Cancel subscription
  - Setup: 
    - Go to Settings → Customer Portal
    - Configure features
    - Add link to your app

4. Webhook handling
  - Listen for events:
    - customer.subscription.created
    - customer.subscription.updated  
    - customer.subscription.deleted
    - invoice.paid
    - invoice.payment_failed
    - charge.dispute.created

5. Integrate with your app
  - Stripe.js + Stripe Elements (frontend)
  - Stripe SDK (backend)
  - Checkout (hosted payment page — easiest)
```

### Stripe Implementation Example

```javascript
// Create a subscription (Node.js)
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

async function createSubscription(customerId, priceId) {
  const subscription = await stripe.subscriptions.create({
    customer: customerId,
    items: [{ price: priceId }],
    payment_behavior: 'default_incomplete',
    expand: ['latest_invoice.payment_intent'],
    metadata: {
      source: 'web',
      signup_date: new Date().toISOString()
    }
  });
  
  return subscription;
}

// Handle proration on upgrade
async function upgradePlan(subscriptionId, newPriceId) {
  const subscription = await stripe.subscriptions.retrieve(subscriptionId);
  
  const updated = await stripe.subscriptions.update(subscriptionId, {
    items: [{
      id: subscription.items.data[0].id,
      price: newPriceId,
    }],
    proration_behavior: 'create_prorations',
    proration_date: Math.floor(Date.now() / 1000),
  });
  
  return updated;
}

// Handle failed payment (webhook)
async function handleFailedPayment(invoice) {
  // Log the failure
  console.log(`Payment failed for invoice: ${invoice.id}`);
  
  // Add custom metadata
  await stripe.invoices.update(invoice.id, {
    metadata: {
      dunning_attempt: (
        parseInt(invoice.metadata.dunning_attempt || '0') + 1
      ).toString()
    }
  });
  
  // Notify customer
  await sendPaymentFailedEmail(
    invoice.customer_email,
    invoice.amount_due / 100,
    invoice.id
  );
}
```

---

## Part 3: Paddle — The Merchant of Record

### Why Choose Paddle

```yaml
The key advantage: Paddle is the Merchant of Record.

This means Paddle:
  - Handles ALL sales tax/VAT globally
  - Handles ALL payment disputes
  - Handles ALL compliance (GDPR, PCI, etc.)
  - Takes the liability for tax mistakes
  - You receive net payments (tax already deducted)

This eliminates:
  - Sales tax registration (50 states)
  - VAT registration (170+ countries)
  - Quarterly sales tax filings
  - VAT return filings
  - Audit risk for tax errors
  - PCI compliance burden

Best for: Solo founders selling internationally, especially B2C.
```

### Paddle Pricing

```yaml
Paddle Classic:
  5% + $0.50 per transaction
  Includes: Payment processing, tax handling, merchant of record

Paddle Billing (new):
  Pay volume pricing (custom quote)
  Similar rates, more flexible

Example costs at different volumes:
  $1K MRR (20 × $50):
    20 × (5% × $50 + $0.50) = 20 × ($2.50 + $0.50) = $60
    Effective rate: 6.0%
    vs Stripe: $35 (Stripe is cheaper by $25)
    
  $10K MRR (200 × $50):
    200 × ($2.50 + $0.50) = $600
    Effective rate: 6.0%
    vs Stripe: $350 (Stripe is cheaper by $250)
    
  $50K MRR (1,000 × $50):
    1,000 × ($2.50 + $0.50) = $3,000
    Effective rate: 6.0%
    vs Stripe: $1,750 (Stripe is cheaper by $1,250)

BUT: With Paddle, you save on:
  - Sales tax compliance software ($1K-$3K/year + 0.5% per transaction)
  - VAT compliance (thousands/year)
  - Tax registration costs ($500/state)
  - Accounting costs (tax handling)
  - Audit risk (priceless)

Break-even analysis:
  At $5K MRR with sales in 5 states and 3 countries:
    Stripe fees: ~$175/month
    Tax compliance: ~$200/month (TaxJar/Stripe Tax)
    VAT compliance: ~$100/month (if EU sales)
    Total: ~$475/month
    
    Paddle fees: ~$350/month
    
    Paddle is CHEAPER at $5K MRR with international sales!
  
  At $5K MRR with US-only sales:
    Stripe + TaxJar: ~$300/month
    Paddle: ~$350/month
    Stripe is CHEAPER for US-only
```

### Paddle Setup

```yaml
1. Create Paddle account
  - Sign up at paddle.com
  - Provide business details (they do KYC)
  - Link bank account for payouts

2. Set up products
  - Products = what you sell
  - Each product has prices (monthly, annual)
  - Paddle handles localization

3. Integration
  - Paddle.js (frontend checkout)
  - Paddle API (backend)
  - Webhooks (subscription events)

4. Subscription management
  - Paddle handles proration
  - Built-in customer portal
  - Dunning emails (automated)
  - Tax handling (automatic)

5. Payouts
  - Weekly, bi-weekly, or monthly
  - Net of fees, taxes, and refunds
  - To your bank account
```

### Paddle Gotchas

```yaml
1. Higher fees (5% + $0.50 vs 2.9% + $0.30)
  - Makes a big difference at volume
  - Switch to Stripe when > $50K MRR and US-only

2. Less control over customer
  - Paddle "owns" the customer relationship
  - Direct email communication may be limited
  - Customer sees "Paddle" on their statement

3. Migration is hard
  - Moving from Paddle to Stripe mid-stream is painful
  - Customers need to re-enter payment info
  - Choose carefully from the start

4. Not all countries supported
  - Paddle supports 200+ countries for PAYING
  - But you must have a legal entity in supported countries (US, UK, EU)
  - Some restricted countries can't be sellers

5. Payout timing
  - Weekly payouts (vs daily with Stripe)
  - 7-day rolling reserve for disputes
```

---

## Part 4: LemonSqueezy — The Indie Alternative

### Why Choose LemonSqueezy

```yaml
LemonSqueezy is similar to Paddle:
  - Merchant of Record
  - Handles tax compliance
  - No sales tax/VAT paperwork

Key differences:
  - Lower fees than Paddle (tiered pricing)
  - More indie-friendly vibe
  - Built for digital products (more than SaaS)
  - Better developer experience
  - Actually profitable and independent (not VC-funded)
```

### LemonSqueezy Pricing

```yaml
Standard: 5% + $0.50 per transaction
Micro: 2.9% + $0.30 (but you handle tax — defeats the purpose)

Same effective rate as Paddle for standard pricing.

Volume discounts:
  $10K+/month: Negotiable
  $50K+/month: Lower rates

No monthly fees.
No setup fees.
```

### LemonSqueezy Pros and Cons

```yaml
Pros:
  - Merchant of Record (no tax hassle)
  - Lower volume pricing available
  - Clean, modern interface
  - Good API and docs
  - Built by indie founders for indie founders
  - Supports: subscriptions, payment links, checkout
  - Has customer portal

Cons:
  - Newer than Paddle (less battle-tested)
  - Fewer integrations
  - Smaller company (risk of going under?)
  - Less enterprise-ready
  - No direct Stripe migration path

Best for: Indie solo founders, especially pre-$20K MRR
```

---

## Part 5: Comparison Matrix

```yaml
                 | Stripe       | Paddle       | LemonSqueezy
─────────────────|──────────────|──────────────|──────────────
Fees             | 2.9%+$0.30  | 5%+$0.50     | 5%+$0.50
Merchant of Record| NO          | YES           | YES
Tax Handling     | Add-on (0.5%)| Included      | Included
Global Payments  | 135+ countries| 200+ countries| 180+ countries
Developer Exp.   | Excellent    | Good          | Great
Customer Portal  | Built-in     | Built-in      | Built-in
Dunning          | Manual/smart | Automatic     | Automatic
Subscriptions    | Excellent    | Good          | Good
Invoicing        | Built-in     | Built-in      | Built-in
Reporting        | Excellent    | Good          | Good
Solo Founder Fit | US-only: YES | Global: YES   | Global: YES
Enterprise       | YES          | OK            | No
Volume Discounts | At $1M+/mo   | At $10K+/mo   | At $10K+/mo

When Stripe is better:
  - US-only customers
  - B2B (tax is easier — reverse charge/VAT exempt)
  - You're comfortable with tax compliance
  - > $10K MRR (lower fees make a difference)

When Paddle/LemonSqueezy is better:
  - International customers
  - B2C (higher tax compliance burden)
  - You HATE tax paperwork
  - < $20K MRR (fee difference is manageable)
```

---

## Part 6: Subscription Management

### Essential Billing Features

```yaml
PRORATION:
  What happens when a customer upgrades mid-cycle?
  
  Stripe default: Credit for unused time on old plan + charge for new plan
  Formula: (Days remaining / Total days) × (New price - Old price)
  
  Example: Upgrade from $49 to $99 on day 15 of 30-day cycle
    Credit: 15/30 × $49 = $24.50 (unused)
    Charge: 15/30 × $99 = $49.50
    Net charge: $49.50 - $24.50 = $25.00

TRIALS:
  Free period before charging
  
  Best practices:
    - 7-30 day trials common for SaaS
    - Require payment method (higher conversion to paid)
    - Send reminder before trial ends (3 days, 1 day)
    - Offer extended trial if user engages but doesn't convert

COUPONS/DISCOUNTS:
  First month free: 100% off first invoice
  Lifetime discount: 20% off forever
  Annual discount: 2 months free (16.7% off)
  
  Best practices:
    - Time-limited (creates urgency)
    - Track coupon code usage
    - Don't stack discounts (customer gets best one)

METERED/USAGE BILLING:
  Charge based on usage
  
  Examples:
    - API calls per month
    - Storage used
    - Active users
    - Documents processed
  
  Implemented via Stripe's usage records API
```

### The Customer Portal

```yaml
Every SaaS needs a customer portal where users can:

1. View current plan and pricing
2. Upgrade/downgrade
3. Update payment method
4. View invoices and receipts
5. Download billing history
6. Cancel subscription

Stripe's Customer Portal (free, built-in):
  - No code needed beyond a link
  - Fully customizable (branding, features)
  - Supports self-serve upgrades, downgrades, cancellations
  - Handles proration automatically

Setup:
  https://dashboard.stripe.com/test/settings/billing/portal
  Configure: Features, branding, business details
  Add link: <a href="/portal">Manage Billing</a>
```

### Invoicing

```yaml
When to send invoices:
  - After successful payment (automatic)
  - For annual contracts (single invoice)
  - For enterprise customers (net-30 terms)
  - For customers who request them

Best practices:
  - Send invoice immediately after charge
  - Include: Company name, date, items, amount, tax, total
  - Invoice number format: INV-YYYY-XXXX
  - Store PDF copies (for accounting)
  - Make downloadable from customer portal

Stripe Invoicing:
  - Automatic invoice generation
  - Email delivery
  - PDF download
  - Cross-border compliant
```

---

## Part 7: Dunning — The Art of Getting Paid

### What Is Dunning?

Dunning is the process of recovering failed payments. It's critical because:

```yaml
- 3-7% of recurring payments fail each month
- Failed payments are a leading indicator of churn
- Good dunning recovers 50-70% of failed payments
- Bad dunning loses customers you could have kept

Common reasons for payment failure:
  Expired card: 35%
  Insufficient funds: 25%
  Card declined (bank risk): 20%
  Card lost/stolen: 10%
  Incorrect card details: 10%
```

### The Dunning Sequence

```yaml
Stripe's smart dunning (automated, no code):

1st attempt: Day of charge
  - Automatic retry
  - No email yet (may succeed on retry)

2nd attempt: 3 days after
  - Retry charge
  - Send email: "Payment failed — update your card"

3rd attempt: 5 days later (8 days total)
  - Retry charge
  - Send email: "Your account will be suspended in 7 days"

4th attempt: 7 days later (15 days total)
  - Final retry
  - Send email: "Final notice — update payment or account is suspended"

After 4 attempts (usually 15-21 days):
  - Mark subscription as past_due
  - Cancel if unpaid after 30 days
  - OR downgrade to free tier

Custom dunning schedule (recommended for solo founders):

Day  0: Initial charge fails
   → Send: Friendly email — "Hey, your card didn't go through"
   → Include: Direct link to update payment (1 click)
   → Personal touch: "Reply if you need help"

Day  3: Retry charge
   → Send: "Quick reminder — update your payment info"
   → Include: What happens if unpaid (service interruption)

Day  7: Retry charge
   → Send: More urgent — "Your account will be suspended"
   → Include: Alternative payment method offer (PayPal, bank transfer)

Day 14: Final retry
   → Send: "Last chance — service ending soon"
   → Offer: Discount, payment plan, callback

Day 21: Cancel subscription
   → Send: "Your subscription has ended"
   → Include: How to reactivate (data retained for 30-90 days)
   → Offer: Export their data
```

### Dunning Email Templates

```yaml
Email 1 (Day 0 — Friendly):

Subject: Payment issue with your [Product] subscription

Hi [Name],

We tried to process your monthly payment of $49, but it didn't go through.

This might be because your card expired or was replaced.

Please update your payment info here: [link]
It takes 30 seconds and you won't miss any service.

Reply to this email if you need help.

– [Your Name]

Email 2 (Day 3 — Reminder):

Subject: Reminder: Update your payment method

Hi [Name],

Your payment of $49 is still outstanding. We'll try again in a few days, 
but please update your payment info to avoid any interruption.

Update here: [link]

Thanks,
[Your Name]

Email 3 (Day 7 — Urgent):

Subject: Your [Product] subscription will be suspended

Hi [Name],

We haven't been able to process your payment. 
Your account will be suspended in 7 days if we don't receive payment.

Don't lose access to [key feature they use]. 
Update your payment method here: [link]

Prefer to pay via bank transfer? Reply to this email.

– [Your Name]

Email 4 (Day 14 — Final):

Subject: Final notice: [Product] subscription canceled tomorrow

Hi [Name],

This is your final notice. Your subscription will be canceled tomorrow.

When it's canceled:
- Your team will lose access to [Product]
- Your data will be retained for 30 days
- After 30 days, data will be deleted

Don't lose everything you've built. Update here: [link]

Questions? Reply to this email.

– [Your Name]
```

### Dunning Performance Metrics

```yaml
Track these metrics:

Recovery Rate: Recovered / Total failures × 100
  Good: > 60%
  Great: > 75%
  Poor: < 40%

Time to Recovery: Average days from first failure to recovery
  Good: < 5 days
  Great: < 3 days

Recovery by Attempt:
  1st retry: 35% recovery
  2nd retry: 20% recovery
  3rd retry: 10% recovery
  4th retry: 5% recovery
  Total: ~70% recovery with 4 attempts

Revenue Saved: Recovered payments × average payment amount
  Monthly: [Recovery rate] × [Failed payment volume] × [Avg payment]
```

---

## Part 8: Advanced Payment Strategies

### Strategy 1: Annual Pricing

```yaml
Offer annual billing at a discount:

Pricing:
  Monthly: $49/month
  Annual: $490/year (effectively $40.83/month — 16.7% discount)

Benefits:
  - Improves cash flow (get 12 months upfront)
  - Reduces churn (annual customers churn 40-60% less)
  - Reduces payment failures (1 transaction/year vs 12)
  - Increases LTV (locked in for 12 months)

Conversion rate:
  ~15-30% of customers choose annual when offered
  Higher for B2B, lower for B2C

Implementation:
  Create two prices in Stripe/Paddle:
    - Monthly: $49
    - Annual: $490
  Show both on pricing page
  Highlight savings
  Offer 60-day money-back guarantee (reduces hesitation)
```

### Strategy 2: Usage-Based Pricing

```yaml
Popular for: API tools, hosting, data processing

Structure:
  Flat fee: $29/month (base)
  Usage fee: $0.01 per API call over 1,000
  
  Example: 5,000 API calls
    Total: $29 + (4,000 × $0.01) = $29 + $40 = $69

Pros:
  - Aligns price with value (pay for what you use)
  - Low barrier to entry (low base fee)
  - Natural expansion revenue (usage grows, price grows)

Cons:
  - Revenue is less predictable
  - Customers may churn if usage spikes (bill shock)
  - More complex implementation
  - Need usage metering infrastructure

Implementation:
  Stripe Usage Records API
  Metered billing in subscription
  Set usage limits and overage rates
```

### Strategy 3: Multiple Payment Methods

```yaml
Offer options beyond credit cards:

1. ACH/Direct Debit (US)
  - Fees: ~0.8% (much lower than cards)
  - Best for: Enterprise customers
  - Provider: Stripe ACH, Plaid, Dwolla
  - Churn: Lower (can't expire)

2. PayPal
  - Fees: 2.9% + $0.30 (similar to Stripe)
  - Best for: Customers who don't trust sharing card info
  - Provider: PayPal Braintree, PayPal Checkout
  - Note: Can use alongside Stripe

3. Wire Transfer / Bank Transfer
  - Fees: $0 (you pay nothing)
  - Best for: $10K+ annual contracts
  - Process: Manual invoicing
  - Note: Requires manual reconciliation

4. Digital Wallets (Apple Pay, Google Pay)
  - Fees: Same as cards
  - Best for: Mobile users
  - Setup: Stripe Elements handles these automatically
```

### Strategy 4: Multi-Currency Pricing

```yaml
Show prices in customer's local currency:

Stripe:
  - Create prices in multiple currencies
  - Set FX conversion rules (Stripe handles)
  - Customer sees price in their currency

Paddle:
  - Automatic localization (shows local currency)
  - Handles FX conversion
  - Customer pays in local currency

Benefits:
  - Higher conversion (local currency = more trust)
  - Avoids FX confusion (customers know what they're paying)
  - Reduces support questions

Pricing strategy by country:
  US: $49
  EU: €49 (slightly higher to account for VAT)
  UK: £42
  Canada: C$65
  Australia: A$75
```

---

## Quick Reference

```yaml
PAYMENT PROCESSING CHEAT SHEET

CHOOSE STRIPE WHEN:
  - US-only customers
  - B2B (simple tax handling)
  - > $10K MRR (lower fees matter)
  - You need advanced billing features
  - You're comfortable with tax compliance

CHOOSE PADDLE/LEMONSQUEEZY WHEN:
  - International customers
  - B2C (complex tax handling)
  - < $20K MRR (fee difference is small)
  - You want to ignore tax compliance
  - You're a solo founder who hates paperwork

DUNNING BEST PRACTICES:
  - 4 attempts over 21 days
  - First email: Friendly, direct link
  - Final email: Urgent, offer help
  - Keep data for 30-90 days after cancellation
  - Track recovery rate (target > 60%)

FEE OPTIMIZATION:
  - Annual billing reduces fees (1 transaction vs 12)
  - ACH is cheaper than cards (0.8% vs 2.9%)
  - Negotiate volume discounts at $1M+/month
  - Use Merchant of Record for international (net cost may be lower)

NEVER FORGET:
  - Failed payments are recoverable (don't just cancel!)
  - Good dunning emails are personalized and helpful
  - Annual discounts hurt cash flow short-term but improve retention long-term
  - The cheapest processor isn't always the best value (consider hidden costs)
```

Your payment processing setup is the financial backbone of your SaaS. Get it right early, and you'll never think about it again. Get it wrong, and you'll be dealing with $0 days, angry emails about mysterious charges, and churn from payment failures you could have prevented.