# SaaS Subscription Models: Choosing How You Charge

## Why Pricing Model Matters More Than Price

The subscription model you choose determines your revenue trajectory, customer acquisition strategy, and even which features you build. It's not just about how much you charge — it's about HOW you charge.

As a solo founder, your pricing model should:
- Align with the value you deliver
- Be simple enough to explain in one sentence
- Scale with customer success (not punish it)
- Minimize churn (or make it painful to leave)
- Avoid complexity that creates support overhead

## The Major Subscription Models

### 1. Flat-Rate Pricing

One product, one price. Everyone pays the same.

**Examples:** Basecamp ($99/mo), Carrd ($9/yr), ConvertKit started as flat-rate

**How it works:**
```
Plan: Pro — $49/month
Includes: All features, unlimited everything
Usage limit: Fair use policy
```

**Pros:**
- Simplest to understand and communicate
- Easy to bill (one SKU)
- No feature gate complexity
- Customers feel they get full value
- Low support overhead

**Cons:**
- Hard to capture value from different segments
- Either overpays small customers or underpays large ones
- No growth path for customers (no upgrade)
- Limits revenue per customer

**Best for:** Products where usage doesn't vary much between customers, simple tools, or when you want maximum simplicity.

**Solo founder suitability:** 8/10 — Dead simple to implement and manage

**Pricing strategy:**
```
Price = (Cost to serve average customer × 3) + Desired margin

Example:
- Infrastructure cost per customer: $2/month
- Support time per customer: 15 min/month ($10 labor)
- Total cost: $12/month
- Price: $36-49/month (3-4x cost)
```

### 2. Tiered Pricing (The Standard SaaS Model)

Multiple plans at different prices with different feature sets.

**Examples:** Most SaaS products (Slack, GitHub, Mailchimp, Notion)

**How it works:**
```
Free: $0 — Limited features, up to 10 projects
Starter: $29/mo — Core features, 50 projects
Professional: $79/mo — Advanced features, 200 projects
Enterprise: $199/mo — All features, unlimited projects
```

**Pros:**
- Captures value across segments
- Clear upgrade path (more features → more value → more revenue)
- Free/professional tiers act as acquisition funnel
- Can serve both SMB and mid-market with one product

**Cons:**
- Feature gating creates complexity
- More SKUs = more support questions
- Customers can get "plan confusion" (which plan do I need?)
- Higher development overhead (maintaining multiple feature sets)

**Best for:** Most B2B SaaS products with different customer segments.

**Solo founder suitability:** 6/10 — Worth the complexity if segments are clear

**The 3-tier structure (standard):**
```
Plan 1: Entry/Starter (40% of price)
- For individuals or small teams
- Limited features
- Price: $X/month

Plan 2: Professional/Most Popular (100% of price)
- For growing teams
- Full feature set
- Price: $2.5X/month

Plan 3: Enterprise/Business (150-200% of price)
- For larger organizations
- Premium features, support, compliance
- Price: $4-5X/month
```

**Pricing tier psychology:**
- **Decoy effect:** The Enterprise tier exists to make Professional look reasonable
- **Anchoring:** The highest price anchors the value of all tiers
- **Most Popular badge:** Drives 60-70% of customers to the middle tier

### 3. Per-Seat / Per-User Pricing

Charge per user per month. Revenue scales with customer team size.

**Examples:** Slack, Linear, Notion, Asana, GitHub

**How it works:**
```
User cost: $12/user/month, billed monthly

Team of 5: $60/month
Team of 50: $600/month
Team of 100: $1,200/month
```

**Pros:**
- Revenue scales naturally with customer growth
- Fair — pay for what you use
- Easy to understand
- Low barrier to entry (start with 1-2 users)
- Strong expansion revenue (add users → add revenue)

**Cons:**
- Customers may limit users to control costs
- Can create friction for collaboration (invite? costs money?)
- No per-user discount paradox (small teams overpay per user, large teams get discounts)
- Churn risk: reduce seats instead of canceling

**Best for:** Collaboration tools, communication platforms, project management.

**Solo founder suitability:** 8/10 — Simple model, predictable revenue

**Pricing strategies for per-seat:**

```
Flat per-user pricing:
$12/user/month for everyone

Volume discounts:
$12/user/month (1-10 users)
$10/user/month (11-50 users)
$8/user/month (51+ users)

Hybrid (base + per-user):
$50 base/month (includes 5 users)
+ $8/user/month for additional users
```

### 4. Usage-Based Pricing

Charge based on consumption (API calls, storage, compute, data processed).

**Examples:** AWS, Stripe, Twilio, SendGrid, OpenAI

**How it works:**
```
API calls: $0.01 per 1,000 calls
Storage: $0.10 per GB/month
Bandwidth: $0.05 per GB
Or: tiered usage levels
```

**Pros:**
- Perfect alignment with value (pay for what you use)
- No barriers to adoption (start small, grow)
- Can capture huge value from power users
- No feature gating complexity

**Cons:**
- Unpredictable bills for customers (bill shock risk)
- Harder to forecast revenue
- May discourage usage (customer caps their own usage)
- Billing infrastructure is complex
- Needs metering and usage tracking

**Best for:** API products, infrastructure, data processing, communication APIs.

**Solo founder suitability:** 4/10 — Complex to implement and manage

**Mitigating bill shock:**
```
Usage caps:
"Set your monthly budget and we'll alert you at 80%."

Plan-based:
Starter: 10K API calls included, $0.01/additional
Pro: 100K API calls included, $0.005/additional
Enterprise: Custom pricing

Capped plans:
$49/month for up to 10K API calls
Hard cap (stop serving at limit)
```

### 5. Hybrid Model (Most Common in Modern SaaS)

Combine two or more models for better alignment.

**Examples:** Most successful SaaS companies

**Common hybrids:**

```
1. Per-seat + Tiers:
   Free: 5 users, limited features
   Pro: $12/user/month, full features, $50 minimum
   Enterprise: $12/user/month, premium features, SSO

2. Usage + Tiers:
   Starter: $29/month, 1,000 API calls
   Pro: $99/month, 10,000 API calls
   Enterprise: $299/month, 100,000 API calls

3. Flat + Per-seat:
   Base fee: $79/month (includes 10 users)
   + $5/user/month for additional users

4. Tiered + Add-ons:
   Professional: $79/month
   + API access: $29/month
   + Custom branding: $49/month
   + Dedicated support: $199/month
```

**Best for:** Most SaaS products.

**Solo founder suitability:** 7/10 — Flexible but can get complex

### 6. Outcome-Based Pricing

Charge based on the value delivered (commission model).

**Examples:** Stripe (per-transaction), Shopify (transaction fee), referral fees

**How it works:**
```
5% of revenue processed through the platform
OR
$0.50 per transaction
OR
10% of cost savings achieved
```

**Pros:**
- Perfect value alignment (you win when customer wins)
- No upfront cost for customer (easy to sell)
- Can charge much more than subscription (if you deliver value)

**Cons:**
- Revenue is unpredictable
- Revenue tied to customer success (if they fail, you fail)
- Hard to forecast
- May cap customer upside if they think you're "taking too much"

**Best for:** Payment processing, marketplaces, affiliate platforms, specific value-delivery products.

**Solo founder suitability:** 3/10 — Revenue uncertainty is hard for solo founders

### 7. Freemium

Free tier + paid upgrade. Covered in detail in the freemium vs. free trial document.

## Choosing Your Model: The Decision Framework

### Factor 1: Value Alignment

```
How does your product deliver value?

Per-use value: Each usage delivers independent value
  → Usage-based pricing
  → Example: Each email delivered, each API call

Ongoing value: Value accumulates over time
  → Subscription pricing
  → Example: Having all your projects in one place

Team value: Value increases with more users
  → Per-seat pricing
  → Example: Team communication tool

Outcome value: Value = specific result achieved
  → Outcome-based pricing
  → Example: Payment processed successfully
```

### Factor 2: Customer Segmentation

```
Do your customers have very different needs?

Yes → Tiered pricing (different plans for different segments)
No → Flat-rate pricing (one plan for everyone)

Do customers grow with you?

Yes → Per-seat or usage-based (revenue grows with them)
No → Flat-rate (revenue per customer is stable)

Is there a clear "power user" segment?

Yes → Tiered or usage-based (capture higher value)
No → Flat-rate or simple per-seat
```

### Factor 3: Market Norms

```
What are customers accustomed to paying for?

In your category, what pricing models are standard?
- Project management: Per-seat + tiers
- Email marketing: Contacts + sends (hybrid usage)
- Infrastructure: Usage-based
- Vertical SaaS: Tiers (flat for specific industry)

Breaking category norms can be differentiation:
- Basecamp broke per-seat with flat pricing
- But breaking norms requires education
```

### Factor 4: Operational Complexity

```
As a solo founder, you need to consider:

Billing complexity:
- Flat-rate: Stripe subscription, 5 minutes to set up
- Tiers: Stripe subscription with plan IDs, 1 hour
- Per-seat: Need seat management UI, 1-2 days
- Usage-based: Need metering, billing integration, 1-2 weeks

Support complexity:
- Flat-rate: "What does this plan include?" — never asked
- Tiers: "Which plan is right for me?" — frequent question
- Usage-based: "Why was I billed $X?" — common support issue
```

### Factor 5: Solo Founder Suitability

| Model | Complexity | Revenue Predictability | Support Load | Solo Score |
|-------|-----------|----------------------|--------------|------------|
| Flat-rate | Very Low | High | Very Low | 9/10 |
| Per-seat | Low | High | Low | 8/10 |
| Tiers | Medium | High | Medium | 6/10 |
| Hybrid | Medium-High | High | Medium | 6/10 |
| Usage-based | High | Low | High | 4/10 |
| Outcome-based | High | Very Low | Medium | 3/10 |
| Freemium | Medium | Low | High | 4/10 |

## Pricing Model Playbooks

### Playbook 1: The Simple Starter

**Best for:** First-time solo founder, pre-PMF, simple product

```
Model: Flat-rate or 2-tier

Option A: Flat-rate at $29/month
Option B: $19/month (Basic) + $49/month (Pro)

Implementation:
1. Stripe subscription (5 min)
2. One pricing page
3. Feature gating code (if tiers)

Pros: Dead simple, easy to change later
Cons: Leaving money on the table with larger customers
```

**When to upgrade:** When you have 20+ customers and can see segments forming.

### Playbook 2: The Team Grower

**Best for:** Collaboration/team products

```
Model: Per-seat with 3 tiers

Free: 3 users, limited features
Team: $8/user/month, full features  
Business: $12/user/month + premium features

Implementation:
1. Seat management UI in product
2. Billing per seat on Stripe
3. Usage limits per plan

Pros: Scales with customer growth
Cons: Need to build seat management
```

**When to upgrade:** When you start losing deals because of missing collaboration.

### Playbook 3: The API Provider

**Best for:** API/developer tools

```
Model: Usage-based with tiered plans

Free: 1,000 API calls/month
Growth: $29/month (10K calls included, $0.01/additional)
Pro: $99/month (100K calls, $0.005/additional)
Enterprise: Custom

Implementation:
1. Usage metering system
2. Billing integration (Stripe Metered Billing)
3. Usage dashboard for customers

Pros: Captures value from heavy users
Cons: Complex implementation
```

**When to upgrade:** When you have stable product and need to maximize revenue.

## Billing Frequency

### Monthly vs. Annual

| Factor | Monthly | Annual |
|--------|---------|--------|
| Customer commitment | Low | High |
| Cash flow timing | Slow but steady | Fast (big upfront) |
| Churn risk | Higher | Lower (locked in) |
| ARR calculation | Same | Same |
| Revenue per customer | Lower per-touch | Higher per-touch |
| Discount offered | None typical | 10-30% for annual |

**Best practice:** Offer both with a discount for annual.

```
Standard: $49/month
Annual: $49 × 12 = $588 → $490/year (save $98, 17% discount)

Or simpler:
Monthly: $49/month
Annual: $39/month, billed annually ($468/year)
```

### Solo founder recommendation:

Start with monthly only. Add annual after product-market fit. Annual discounts improve retention but complicate accounting.

## Pricing Model Pitfalls

### Pitfall 1: Overcomplicating from Day 1

```
Bad: 5 tiers, usage-based with hybrid per-seat, add-ons, and contracts
Good: 2-3 tiers, simple, easy to understand

You can always add complexity later.
You CAN'T remove complexity without angering customers.
```

### Pitfall 2: Charging by Users When It's Not a Team Product

If one person gets all the value, per-seat pricing creates friction.

**Better:** Flat-rate or usage-based.

### Pitfall 3: Usage-Based Without Caps

Customers hate surprise bills. Always offer:
- Usage budgets
- Alerts at 50%, 80%, 100%
- Hard caps or automatic plan upgrades

### Pitfall 4: Free Tier That's Too Generous

You want free users to FEEL the limitations so they upgrade. If free has everything they need, they'll never pay.

### Pitfall 5: Changing Your Model Too Often

Every pricing change creates friction. Customers have to re-evaluate your value. Keep your model stable for at least 12 months.

## The Solo Founder's Pricing Model Decision Tree

```
START HERE:

Does the product deliver value per-use or continuously?
├── Per-use → Consider usage-based pricing
│   └── Is billing complexity manageable for one person?
│       ├── Yes → Usage-based (with tiered plans for predictability)
│       └── No → Tiered pricing with usage limits included
│
└── Continuous → Subscription model

Is the product used by teams or individuals?
├── Teams → Consider per-seat pricing
│   └── Do teams need different feature sets?
│       ├── Yes → Per-seat with tiers
│       └── No → Per-seat flat rate
│
└── Individuals → Flat-rate or simple tiers

Do customers have very different needs/budgets?
├── Yes → Tiered pricing (2-3 tiers)
├── No → Flat-rate pricing
└── Both → Hybrid (tiers + usage or tiers + per-seat)

Are you a solo founder?
├── Yes → Minimize complexity
│   ├── 2 tiers maximum to start
│   ├── Flat-rate or simple per-seat
│   ├── Monthly billing only
│   └── Can add complexity later
│
└── No → More options available
```

## Pricing Model Examples by SaaS Category

### Project Management
- **Asana:** Per-seat + tiers (Free, Premium $10.99/seat, Business $24.99/seat)
- **Basecamp:** Flat-rate ($99/month, everything included)
- **Trello:** Per-seat + tiers (Free, Standard $5, Premium $10, Enterprise)
- **Linear:** Per-seat + tiers (Free, Team $8/seat/month)

### Email Marketing
- **Mailchimp:** Contacts + sends (hybrid usage/tier)
- **ConvertKit:** Subscriber count (usage-based tiered)
- **Buttondown:** Flat-rate ($9/month, unlimited everything)

### Developer Tools
- **GitHub:** Per-seat + tiers (Free, Team $4/seat, Enterprise $21/seat)
- **Vercel:** Usage-based + tiers
- **Sentry:** Usage-based (events) + tiers

### Vertical SaaS
- **Toast (restaurants)::** Flat-rate + transaction fees (hybrid)
- **Procore (construction)::** Per-user + project fees
- **Vetcove (vet)::** Flat-rate subscription

## Final Recommendations for Solo Founders

### If You Have No Customers Yet
- Start with 2-tier flat-rate pricing
- $19/month (Basic) + $49/month (Pro)
- Monthly billing only
- No free tier (offer demo/trial instead)
- Be ready to change pricing as you learn

### If You Have 10-50 Customers
- Consider adding per-seat if appropriate
- Add annual billing with 20% discount
- Analyze usage patterns — which customers use what?
- Consider a third tier if you see a clear segment

### If You Have 50+ Customers
- Analyze pricing elasticity (could you raise prices?)
- Consider introducing usage-based elements
- Analyze churn by tier — is the lowest tier too cheap?
- Consider grandfathering (see pricing optimization doc)

### The Golden Rule

Your pricing model should reflect the VALUE you deliver, not the COST to deliver it. A customer who gets $1,000/month of value should pay more than someone who gets $100/month of value, even if your costs are the same.

The model that best captures this value while remaining simple enough for a solo founder to manage is the sweet spot.

**Start simple. Add complexity only when the data proves you're leaving money on the table.**
