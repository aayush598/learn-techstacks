# Payment Gateways: Getting Paid Fast, Cheap, and Reliably

## Why Payment Infrastructure Is a Revenue Multiplier

How you get paid directly affects your cash flow, your effective hourly rate, and your client relationships. The wrong payment method costs you 3-5% in fees, delays payments by 5-30 days, and creates friction with clients. The right setup gets you paid instantly, costs near zero, and makes you look professional.

This guide breaks down every payment method available to freelancers, their true costs, and how to design a payment system that maximizes your effective income.

---

## Part 1: The Payment Method Landscape

### Methods Ranked by What You Keep

| Method | You Receive (on $10k) | You Lose | Speed | Client Preference |
|---|---|---|---|---|
| ACH (US Only) | $10,000 | $0 | 1-3 days | High (free for them) |
| Wire Transfer | $10,000 | $0-$50 | 1-24 hours | Medium (some banks charge) |
| Wise | $9,975+ | ~$25 | 1-2 days | Medium (need Wise account or details) |
| Stripe (card) | $9,710 | $290 (2.9% + $0.30) | 2-3 days | High (credit card) |
| PayPal | $9,510 | $490 (4.9% + fixed fee) | Instant-3 days | Very High (everyone has PayPal) |
| Venmo/Zelle | $10,000 | $0 | Instant | High (US only, informal) |
| Crypto (USDC) | $9,990 | ~$10 (gas fees) | 1-30 min | Low (early adopters only) |
| Check | $10,000 | $0 | 5-21 days | Low (obsolete, slow) |

**The cost of convenience:** If you accept only PayPal and process $100k/year, you pay $4,900 in fees. Switching to ACH/Wise saves you $4,900. That is a 5% raise without working more.

---

## Part 2: Deep Dive on Each Method

### ACH Transfer (Best for US Clients)

| Detail | Info |
|---|---|
| Cost to you | $0 |
| Cost to client | $0 |
| How it works | Client adds you as a payee in their bank or accounting system |
| Speed | 1-3 business days |
| Limits | Varies by bank ($10k-250k per transaction typical) |
| Best for | US clients, recurring invoices, large payments |
| Setup | Provide routing number and account number from your bank |

**ACH Pros:**
- Free for both parties
- Secure and traceable
- Can be automated through invoicing tools
- No chargebacks (unlike credit cards)

**ACH Cons:**
- US only (requires US bank account)
- Slower than wire or card
- Can be reversed if client disputes (within 5 days)
- Client needs to set up in their banking portal

**How to get ACH details without a US bank account:**
- Wise Borderless account provides US ACH routing and account numbers
- Payoneer provides US payment service details

### Wire Transfer (Best for Large International Payments)

| Detail | Info |
|---|---|
| Cost to you | $0-50 (incoming) |
| Cost to client | $15-50 (outgoing) |
| Speed | 1-24 hours (same day if before cutoff) |
| Limits | No practical limit |
| Best for | Payments over $5,000, international, urgent |

**Wire Transfer Pros:**
- Fast (often same day)
- Secure (bank-to-bank)
- No practical amount limits
- Final (cannot be reversed)

**Wire Transfer Cons:**
- Fees on both sides ($15-50 each)
- Client needs your complete bank details
- Mistakes in wiring instructions cause delays
- Not ideal for small payments (fees eat into amount)

**Information required for US wire:**
- Bank name and address
- Routing number (ABA/ACH)
- Account number
- SWIFT/BIC code (for international)
- Beneficiary name and address
- Reference/Invoice number

### Wise (Best All-Around for International)

| Detail | Info |
|---|---|
| Cost to you | ~$5 to receive, 0.41-1% to convert |
| Cost to client | $0 (if they pay local) |
| Speed | 1-2 business days |
| Limits | None (higher limits with verification) |
| Best for | International payments, multi-currency |

**Wise Pros:**
- Clients pay as local transfer (no wire fees)
- You get mid-market exchange rate
- Hold 40+ currencies
- Borderless account with local bank details

**Wise Cons:**
- Client must set up Wise payment (not as universal as PayPal)
- Conversion fees still apply
- Not ideal for same-day urgency

**How clients pay you via Wise:**
- You provide local bank details (US ACH, EUR IBAN, GBP sort code)
- Client sends a domestic transfer from their bank
- Wise converts and deposits to your account

### Stripe (Best for Credit Card Payments)

| Detail | Info |
|---|---|
| Cost to you | 2.9% + $0.30 per transaction |
| Cost to client | $0 |
| Speed | 2-3 business days to bank |
| Limits | None |
| Best for | One-off payments, low-ticket items, retainer automation |

**Stripe Pros:**
- Clients can pay with any credit card
- Recurring billing and subscription management
- Professional checkout page
- Excellent API and integrations
- Stripe Invoicing (free professional invoices)

**Stripe Cons:**
- 2.9% + $0.30 is expensive for large payments
- Chargeback risk (client can dispute and reverse)
- Account holds for high-risk businesses
- 2-3 day payout delay

**Stripe fee math:**

| Invoice Amount | Stripe Fee | You Keep |
|---|---|---|
| $100 | $3.20 (3.2%) | $96.80 |
| $1,000 | $29.30 (2.93%) | $970.70 |
| $5,000 | $145.30 (2.91%) | $4,854.70 |
| $10,000 | $290.30 (2.9%) | $9,709.70 |
| $50,000 | $1,450.30 (2.9%) | $48,549.70 |

**When to use Stripe:** For payments under $1,000 where convenience matters more than fees. For large payments, steer clients to ACH or wire.

### PayPal (Most Universal, Most Expensive)

| Detail | Info |
|---|---|
| Cost to you | 2.99% + $0.49 (domestic), 4.99% + fixed (international) |
| Cost to client | $0 |
| Speed | Instant (to PayPal balance), 1-3 days to bank |
| Limits | Unverified accounts limited |
| Best for | Emergency payments, clients who refuse other methods |

**PayPal Pros:**
- Everyone has it
- Fast and familiar
- Buyer protection (for clients)
- Invoicing built in

**PayPal Cons:**
- Highest fees of any major payment processor
- Frequent account freezes for freelancers
- Currency conversion markup (3-4% on top of transaction fee)
- Chargeback-heavy policies
- Holds funds for 21 days for new accounts

**PayPal fee math:**

| Invoice Amount | PayPal Fee | You Keep | Effective Rate |
|---|---|---|---|
| $100 | $3.48 | $96.52 | 3.48% |
| $1,000 | $30.39 | $969.61 | 3.04% |
| $5,000 | $149.99 | $4,850.01 | 3.0% |
| $10,000 | $299.49 | $9,700.51 | 3.0% |
| $10,000 (intl) | $499.49 | $9,500.51 | 5.0% |

**Avoid PayPal for payments over $500.** The fees are simply too high. Use it only as a last resort.

### Zelle / Venmo (Free but Informal)

| Detail | Info |
|---|---|
| Cost to you | $0 |
| Cost to client | $0 |
| Speed | Instant |
| Limits | $500-5,000/day (varies by bank) |
| Best for | Small payments, trusted clients, US only |

**Zelle Pros:**
- Free and instant
- Integrated with most US bank apps
- No account freeze risk (bank-to-bank)

**Zelle Cons:**
- US only
- Low limits
- No buyer/seller protection
- Not professional (looks informal)
- Hard to track for accounting

**Venmo Pros:**
- Free with bank transfer
- Social features
- Widely used in US

**Venmo Cons:**
- US only
- No business protection
- Can be reversed in some cases
- Not for professional invoicing

### Crypto / Stablecoins (Emerging Option)

| Detail | Info |
|---|---|
| Cost to you | ~$1-50 (gas fees, varies by network) |
| Cost to client | ~$1-50 |
| Speed | 1-30 minutes |
| Limits | No practical limit |
| Best for | International, large payments, privacy-conscious clients |

**Crypto Pros:**
- Borderless and permissionless
- Fast settlement (minutes)
- No chargebacks (irreversible)
- No bank holidays or delays
- Growing adoption by tech-savvy clients

**Crypto Cons:**
- Volatility (if not using stablecoins)
- Tax complexity (each transaction is a taxable event)
- Client must have crypto knowledge
- Gas fees on Ethereum can be high
- Limited adoption compared to traditional methods

**Recommended setup:**
- Accept USDC or USDT (stablecoins pegged to USD)
- Use Coinbase, Kraken, or Nexo for merchant accounts
- Convert to fiat immediately if you want to avoid volatility
- Track every transaction for tax reporting

---

## Part 3: The Ideal Payment Flow by Scenario

### Scenario 1: US Freelancer, US Clients

```
Preferred: ACH (Direct bank transfer) — $0 fee
             ↓
     Alternative: Stripe (credit card) — 2.9% fee
             ↓
     Last Resort: PayPal — 3%+ fee
```

**Implementation:**
- Put ACH details on every invoice
- Set up Stripe as a payment link on your invoice
- Only mention PayPal if client asks

### Scenario 2: US Freelancer, International Clients

```
Preferred: Wise (multi-currency) — ~$5 per transfer
             ↓
     Alternative: Wire Transfer — $0-50 per transfer
             ↓
     Last Resort: PayPal — 4-5% fee
```

**Implementation:**
- Provide Wise local bank details in client's currency
- Include wire instructions on invoice
- Add a note: "Preferred: Wise or Wire — lower fees for both of us"

### Scenario 3: Non-US Freelancer, US Clients

```
Preferred: Wise (US ACH details) — ~$5 per transfer
             ↓
     Alternative: Payoneer — 1-2% fee
             ↓
     Last Resort: PayPal — 4-5% fee
```

**Implementation:**
- Get Wise US bank details (ACH routing + account number)
- Present as US bank details on invoice
- Set up automatic conversion to local currency when rate is favorable

### Scenario 4: High-Volume / Low-Ticket (Many small payments)

```
Preferred: Stripe (subscription) — 2.9% per transaction
             ↓
     Alternative: ACH via Stripe — 0.8% per transaction
             ↓
     Batch invoices monthly to reduce total fee impact
```

---

## Part 4: Invoicing Tools and Integration

### Top Invoicing Platforms Compared

| Platform | Cost | Payment Methods | Recurring | Best For |
|---|---|---|---|---|
| Stripe Invoicing | Free (2.9% per payment) | Cards, ACH, Wire | Yes | Tech-savvy freelancers |
| FreshBooks | $19-50/month | Cards, ACH, PayPal | Yes | Accounting + invoicing |
| Wave | Free (2.9% per payment) | Cards, ACH (US only) | No | Budget-conscious freelancers |
| QuickBooks Online | $30-60/month | Cards, ACH, PayPal | Yes | Full accounting suite |
| Xero | $13-45/month | Cards, ACH via Stripe | Yes | Accounting integration |
| Bonsai | $25-39/month | Cards, ACH, Wire | Yes | Freelancer-specific features |
| HoneyBook | $39-79/month | Cards, ACH | Yes | Creative freelancers |
| Invoice Ninja | Free-$12/month | Cards, ACH, PayPal | Yes | Self-hosted option |

**Our recommendation:**
- Start free: Stripe Invoicing + Wave (free accounting)
- Scale up: FreshBooks or Bonsai (best UX for freelancers)
- Full setup: QuickBooks Online + Stripe (most professional)

### Invoice Design Principles

1. **Make it easy to pay.** Put payment methods prominently at the top, not buried at the bottom.
2. **Offer the cheapest method first.** "Preferred: ACH Transfer — details below."
3. **Use payment links.** Stripe payment links or FreshBooks client portal.
4. **Automate reminders.** Late payment reminders at 7, 14, and 30 days.
5. **Include late fees.** 1.5% per month (or 18% APR) on overdue invoices.

---

## Part 5: Payment Terms Strategy

### Standard vs. Accelerated Payment Terms

| Term | Description | Best For |
|---|---|---|
| Net 30 | Payment due 30 days after invoice | Standard for enterprise clients |
| Net 15 | Payment due 15 days after invoice | Small to mid-size businesses |
| Net 7 | Payment due 7 days after invoice | Trusted clients |
| Due on Receipt | Payment due immediately | New clients, small projects |
| 50% Upfront + 50% on Delivery | Split payment | Large projects ($5k+) |
| Monthly Retainer | Same amount each month | Ongoing clients |
| Milestone Payments | Paid at project milestones | Long projects ($10k+) |

### Discount for Early Payment

Offer 2% discount if paid within 5 days (2/5 Net 30). This accelerates cash flow and many clients will take it.

### Late Payment Penalties

| Policy | Implementation |
|---|---|
| Late fee | 1.5% per month (18% APR) |
| Grace period | 3-5 days after due date |
| Warning | Email reminder at day 1 overdue |
| Final notice | Email + letter at day 15 |
| Collection | Third-party at day 30+ |
| Stop work | At day 15-30 for ongoing projects |

**Always include late payment terms in your contract.** Without a written agreement, late fees may not be enforceable.

---

## Part 6: Payment Gateway Setup Guide

### Stripe Setup (30 minutes)

1. Go to stripe.com and create account
2. Provide business details (EIN/SSN, bank account, address)
3. Enable payment methods: Cards, ACH, Wire
4. Create Products (if using subscriptions)
5. Set up Stripe Invoicing
6. Integrate with your website or invoicing tool
7. Test with a $1 payment

**Stripe optimization tips:**
- Enable ACH direct debit (0.8% fee cap $5)
- Set up payment links for quick invoices
- Use Stripe Tax for automatic sales tax calculation
- Enable card account updater (reduces failed recurring payments)

### Wise Setup for Receiving (20 minutes)

1. Create Wise account (if you don't have one)
2. Open Borderless account
3. Activate balance in currencies you want to receive (USD, EUR, GBP minimum)
4. Note your local bank details for each currency
5. Add to your invoice templates

### ACH Setup for US Freelancers

**Method 1: Via Bank (Simplest)**
- Provide client with your bank's routing number and account number
- Client initiates payment through their bank's bill pay system

**Method 2: Via Invoicing Platform**
- Stripe ACH: Enable in Stripe settings (0.8% fee)
- FreshBooks: Enable ACH in payment settings

**Method 3: Via Wise**
- Get your US ACH routing and account number from Wise
- Provide to client like a regular US bank account

---

## Part 7: Payment Processing Fees — True Cost Analysis

### Annual Fee Impact by Payment Mix

| Scenario | Payment Mix | Annual Fees on $100k |
|---|---|---|
| Worst case | 100% PayPal | $4,900 |
| Bad | 50% PayPal, 50% Stripe | $3,950 |
| Average | 20% PayPal, 50% Stripe, 30% ACH | $2,030 |
| Good | 10% Stripe, 90% ACH/Wire | $290 |
| Best | 100% ACH/Wire | $0 |

**The difference between worst and best case is $4,900/year.** That is a free vacation, a new laptop, or months of a software subscription.

### How to Shift Your Clients to Lower-Fee Methods

**Script for email signature:**
"Want to save 3% on my services? Pay by ACH or wire transfer instead of credit card or PayPal. I'll pass the savings to you."

**On invoices, list payment methods in this order:**
1. ACH Transfer (Preferred — free for both)
2. Wire Transfer (Fast — $25 fee)
3. Wise (International — mid-market rate)
4. Stripe (Credit Card — 2.9% fee)
5. PayPal (Most expensive — 4-5% fee)

**For existing clients, send a one-time message:**
"Hi [Client], I'm optimizing my payment systems to reduce fees. Starting next month, my preferred payment method is [ACH/Wire/Wise]. If you pay by credit card, there will be a 3% processing fee added to invoices. Please let me know if you need help setting up the new payment method."

---

## Part 8: Recurring Payments and Retainers

### Setting Up Retainers

Retainers are the holy grail of freelance income. They provide predictable cash flow and reduce payment friction.

**Setting up retainer payments:**
1. Use Stripe Subscriptions (best for credit card)
2. Use GoCardless (best for ACH/direct debit)
3. Use Wise recurring transfers (international)
4. Use FreshBooks recurring invoices (simple)

**Retainer fee processing comparison:**

| Method | Fee on $5k/month | Annual Fee |
|---|---|---|
| Stripe (card) | $145 | $1,740 |
| Stripe (ACH) | $25 | $300 |
| GoCardless | $30 | $360 |
| FreshBooks (ACH) | $25 | $300 |
| Manual ACH | $0 | $0 |

### Automating Payment Collection

| Tool | Recurring Feature | Best For |
|---|---|---|
| Stripe | Subscriptions, Invoicing | Full automation |
| Chargebee | Subscription management | Scaling businesses |
| Recurly | Enterprise subscriptions | High-volume |
| Paddle | SaaS billing | Digital products |
| Memberful | Membership sites | Content creators |

---

## Part 9: International Payment Optimization

### Multi-Currency Invoicing

Always invoice in your client's preferred currency when possible.

**Invoice in USD for US clients, EUR for EU clients, GBP for UK clients.**
This makes the payment easier for them and avoids their FX fees.

**How to receive in multiple currencies:**
- Wise: Bank details in USD, EUR, GBP, AUD, CAD, and more
- Revolut: Multi-currency accounts
- Mercury: USD only (but can receive international wires)
- Payoneer: Multiple currency balances

### Avoiding Double Currency Conversion

**Bad flow:**
Client pays in EUR → EUR converted to USD at client's bank → Sent as USD wire → USD converted to your local currency

**Good flow:**
Client pays in EUR directly to your EUR account → You hold EUR → Convert to local currency on your terms

### Currency Conversion Timing Strategy

1. Receive payments in original currency (USD, EUR, GBP)
2. Hold in that currency (don't convert immediately)
3. Convert only when you need to spend
4. Use limit orders to convert at favorable rates

---

## Part 10: Payment Security and Fraud Prevention

### Chargeback Protection

| Method | Chargeback Risk | Protection |
|---|---|---|
| ACH | Low | Can dispute but hard to reverse after 5 days |
| Wire | None | Cannot be reversed |
| Wise | Low | Limited dispute options |
| Stripe | Medium | Stripe Radar, 3D Secure |
| PayPal | High | PayPal sides with buyers |
| Crypto | None | Irreversible |
| Check | Medium | Can bounce |

### Fraud Prevention Checklist

- [ ] Verify client identity before starting work (LinkedIn, website, phone call)
- [ ] Get 50% upfront for new clients
- [ ] Use contracts with clear payment terms
- [ ] Enable 3D Secure on Stripe
- [ ] Set Stripe Radar rules to block high-risk transactions
- [ ] Never accept overpayment scams ("pay extra and wire the difference")
- [ ] Watch for rushed clients ("need this done TODAY")
- [ ] Verify large payments before releasing work

### Red Flag Payment Patterns

| Pattern | Risk |
|---|---|
| Client overpays by 2x and asks for refund | Classic scam — payment will bounce |
| Client insists on PayPal only | Could be chargeback fraud |
| Client from high-risk country with brand new email | Verify thoroughly |
| Client refuses a phone/video call | Legitimate clients will talk |
| Payment from different name than client | Verify source |

---

## Part 11: Payment Gateway Comparison Table

### Comprehensive Comparison

| Feature | ACH | Wire | Wise | Stripe | PayPal | Crypto |
|---|---|---|---|---|---|---|
| Setup Time | 1 day | 1 day | 1 hour | 1 hour | 10 min | 1 hour |
| Cost to Receive | $0 | $0-50 | $5 | 2.9%+$0.30 | 3-5% | $1-50 |
| Cost to Client | $0 | $15-50 | $0 | $0 | $0 | $1-50 |
| Speed | 1-3 days | 1-24 hours | 1-2 days | 2-3 days | Instant-3d | 1-30 min |
| Recurring | Yes | No | Yes | Yes | Yes | No |
| Chargeback Risk | Low | None | Low | Medium | High | None |
| US Only? | Yes | No | No | No | No | No |
| Max Amount | $250k+ | None | $1M+ | None | $10k-100k | None |
| Documentation | Bank details | Bank details | Invoice | API/Site | Email | Wallet address |
| Professionalism | High | High | High | High | Medium | Low-Medium |
| Client Trust | High | High | Medium | High | Very High | Low |

---

## Part 12: Your Payment Infrastructure Setup

### Minimum Viable Setup (Today)

1. **Open a Wise account** — receive USD, EUR, GBP at mid-market rates
2. **Set up Stripe** — accept credit cards for small/one-off payments
3. **Update your invoice template** — list payment methods from cheapest to most expensive
4. **Add late payment terms** — 1.5% monthly on overdue invoices

### Intermediate Setup (Week 2)

5. **Enable Stripe ACH** — 0.8% fee vs 2.9% for cards
6. **Set up recurring invoices** — automate retainer payments
7. **Create payment links** — for quick client checkout
8. **Add automatic payment reminders** — day 0, 7, 14, 30

### Advanced Setup (Month 1)

9. **Integrate invoicing with accounting** — Stripe + QuickBooks or FreshBooks
10. **Set up multi-currency payment pages** — different currencies for different regions
11. **Implement dunning** — automatic retry of failed payments
12. **Create a client portal** — clients can view invoices, make payments, download receipts

---

## Immediate Action Items

1. **Calculate your current payment fees.** Look at last year's Stripe/PayPal statements. Total all fees. You will be shocked.

2. **Change your default invoice payment method to ACH or Wise.** Update your invoice template today.

3. **Send an email to current clients** about your preferred payment method and the fee change for credit cards.

4. **Set up Stripe if you don't have it.** It takes 30 minutes and is free.

5. **Enable ACH in Stripe.** 0.8% is better than 2.9% for any payment over $100.

6. **Open a Wise Borderless account** if you work with international clients.

7. **Add payment links to your invoices.** Make it one-click to pay.

8. **Remove PayPal as your primary payment method.** If clients insist, add a 3% surcharge.

9. **Review your payment terms.** Net 30 is standard but try Net 15 or Net 7 for new clients.

10. **Set up recurring payments** for retainer clients. Automate everything.
