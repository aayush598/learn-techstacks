# Software Licensing Models for Solo SaaS Founders

## Why Your Licensing Model Matters

Your licensing model is how you package, price, and sell access to your software. It defines:
- **Revenue model** — How you make money (per user, per usage, flat fee)
- **Customer fit** — What type of customer finds your pricing attractive
- **Market positioning** — Premium vs mass-market, enterprise vs SMB
- **Legal structure** — What customers can and cannot do with your software

The right licensing model aligns with your customers' willingness to pay, your competitive position, and your operational capabilities as a solo founder.

## Licensing Models Overview

### 1. Per-Seat Licensing (User-Based)

**How it works:** Customers pay for each user who accesses the software.

**Common structures:**
```
Per-user per month:  $29/user/month for 5 users = $145/month
Per-user per year:   $29/user/month × 12 × 20% discount = $278/user/year
Team pricing:        Flat rate for up to 10 users, then per user
Tiered by user count: Starter (1-5), Growth (6-20), Scale (21-100)
```

**Best for:**
- Collaboration tools (Slack, Notion, Asana)
- CRM and sales tools (Salesforce, HubSpot)
- Project management (Linear, Jira)
- Internal business tools

**Pros for solo founders:**
- Predictable, recurring revenue
- Scales with customer's team size (not your costs)
- Easy to understand and communicate
- Simple to implement (count users, charge)

**Cons for solo founders:**
- Caps revenue from each account (no upside from heavy usage)
- Customers may game the system (shared accounts, named user limits)
- Team sales have longer cycles
- Per-seat audits and enforcement are costly

**Implementation in Stripe:**

```javascript
// Create a per-seat subscription product
const product = await stripe.products.create({
  name: 'Pro Plan',
  metadata: { type: 'per_seat', billing: 'per_user_per_month' }
});

const price = await stripe.prices.create({
  product: product.id,
  unit_amount: 2900, // $29/user
  currency: 'usd',
  recurring: { interval: 'monthly', usage_type: 'licensed' }
});

// When user adds a team member, update subscription quantity
await stripe.subscriptions.update(subscriptionId, {
  quantity: numberOfUsers,
  proration_behavior: 'always_invoice'
});
```

**Per-seat best practices for solo founders:**
- Offer a free tier with limited seats (1-2 users)
- The first paid tier should cover 3-5 users (captures small teams)
- Annual billing should be 2 months free (discourages monthly churn)
- Invoice-based billing for 50+ seats (enterprise)
- Consider "unlimited" tier for large teams (price high enough)

### 2. Usage-Based Pricing (Metered)

**How it works:** Customers pay based on their consumption of your service.

**Common metrics:**
```
API calls:          $0.001 per API request
Storage:           $0.10 per GB/month
Compute time:      $0.01 per hour
Documents:         $0.05 per document processed
Active users:      $0.50 per monthly active user
Bandwidth:         $0.01 per GB transferred
Searches/queries:  $0.002 per search
```

**Best for:**
- API-first products (Stripe, Twilio, SendGrid)
- Infrastructure/platform (AWS, Vercel, DigitalOcean)
- Data processing tools (OCR, AI/ML, video transcoding)
- Communication platforms (SMS, video, email)

**Pros for solo founders:**
- Revenue scales DIRECTLY with customer value (no caps)
- Low barrier to entry (start small, pay as you grow)
- Attracts developers (they love usage-based pricing)
- No limits to customer expansion

**Cons for solo founders:**
- Revenue is less predictable (varies month to month)
- Top customers can have huge bills (credit risk)
- Harder to forecast and budget
- Requires metering infrastructure
- Customers may "shock" with large bills

**Implementation in Stripe:**

```javascript
// Create a usage-based product
const product = await stripe.products.create({
  name: 'API Credits',
  metadata: { type: 'usage_based' }
});

const price = await stripe.prices.create({
  product: product.id,
  unit_amount: 10, // $0.10 per unit
  currency: 'usd',
  recurring: {
    interval: 'monthly',
    usage_type: 'metered'  // metered (variable) or licensed
  }
});

// Report usage to Stripe
await stripe.subscriptionItems.createUsageRecord(
  subscriptionItemId,
  {
    quantity: 1500,  // 1500 API calls used
    timestamp: Math.floor(Date.now() / 1000),
    action: 'increment'
  }
);
```

**Usage-based best practices for solo founders:**
- Always include a base fee (minimum commit) for revenue stability
- Offer "included usage" with alerts at 80/90/100%
- Set hard caps to prevent bill shock
- Implement credit system ($10 = 1,000 API calls)
- Bill in arrears for usage above base
- Track customer usage and send monthly reports

### 3. Tiered Plans (Feature-Based)

**How it works:** Different plan tiers with different feature sets at different price points.

**Common structure:**
```
Free:     Basic features, 1 user, limited storage    $0
Starter:  Core features, 5 users, 10GB storage       $29/mo
Pro:      Advanced features, unlimited users, 100GB   $99/mo
Enterprise: Everything, custom limits, SLA, SSO       Custom
```

**Best for:**
- Feature-differentiated products
- Products serving different market segments
- SaaS with clear value progression

**Pros for solo founders:**
- Clear upgrade path for customers
- Monetizes different segments
- Free tier drives adoption
- Enterprise tier for high-value deals

**Cons for solo founders:**
- Feature decisions constrain pricing
- Goldilocks problem (customers choose middle tier)
- Feature gatekeeping can frustrate users
- Need to maintain multiple configurations

**Implementation:**
```javascript
// Define tiers in Stripe
const tiers = [
  { name: 'Starter', price: 'price_starter_id', features: [...] },
  { name: 'Pro', price: 'price_pro_id', features: [...] },
  { name: 'Enterprise', price: null, features: [...] }  // custom
];

// Subscription creates affect pricing
app.post('/api/create-subscription', async (req, res) => {
  const { priceId, customerId } = req.body;
  const subscription = await stripe.subscriptions.create({
    customer: customerId,
    items: [{ price: priceId }],
    payment_behavior: 'default_incomplete',
    expand: ['latest_invoice.payment_intent']
  });
  res.json({ subscriptionId: subscription.id });
});
```

### 4. Site Licenses (Unlimited Users)

**How it works:** A single flat fee for unlimited users within an organization.

**Common pricing:**
```
Small company (<50 employees):    $500/month
Medium company (50-200):          $1,500/month
Large company (200-1000):         $5,000/month
Enterprise (1000+):               $10,000+/month
```

**Best for:**
- Enterprise-focused products
- Developer tools used across teams
- Products where per-seat tracking is burdensome
- Education and non-profit sectors

**Pros for solo founders:**
- Simple sale (no user counting)
- High contract values
- Easy to get started (no complex setup)
- Customer doesn't need to manage users

**Cons for solo founders:**
- Lower per-user revenue (but easier to close)
- Hard to price fairly for different customer sizes
- Risk of overuse (customer may expect white-glove support)
- No growth from within customer (no upsell)

### 5. Usage Tier (Combined Model)

**How it works:** Base fee for included usage, then pay for overage.

**Common structure:**
```
Starter:  $29/month — 5,000 API calls included
Pro:      $99/month — 25,000 API calls included  
Business: $299/month — 100,000 API calls included
Add 1,000 extra calls: $2/thousand
```

**Best for:**
- Products with natural usage patterns
- SaaS that wants predictable base + growth upside
- Compromise between flat rate and pure usage

**Pros:**
- Predictable base revenue
- Upside from heavy users
- Customers can start small, grow into plan
- Clear upgrade triggers

**Cons:**
- More complex to implement
- Customers may overpay for unused included usage
- Need to balance included vs overage pricing

### 6. Freemium (Free Tier + Paid)

**How it works:** Free version with limited features/usage, paid version with full access.

**Common structures:**
```
Free forever:   Core features, 1 user, 100MB storage, community support
Pro:            All features, unlimited users, 10GB, priority support
Business:       All features, API access, custom integrations, phone support
```

**Best for:**
- Consumer/self-serve products
- Products with strong network effects
- "Try before you buy" for complex products
- Developer tools and platforms

**Pros:**
- Massive user acquisition
- Builds habit and dependency
- Creates word-of-mouth marketing
- Funnels users to paid

**Cons:**
- High infrastructure costs (free users consume resources)
- Low conversion rates (typically 2-5%)
- Free users generate support tickets
- Need to carefully limit free tier to prevent abuse

**Freemium metrics benchmark:**
```
Free → Paid conversion:        2-5% (good), 5-10% (great), 10%+ (exceptional)
Free user support cost:        ~$0.50-2/user/year
Free tier cost per user:       $0.10-1.00/month (infrastructure)
Paid plan recovery target:     Cover 50-70% of free tier costs
Upgrade trigger:               Free user hits limit or needs premium feature
```

### 7. Open Source + Commercial

**How it works:** Core product is open source (MIT/Apache), paid features are proprietary.

**Common model:**
```markdown
Open Source (Community Edition):
  → Core features
  → MIT/Apache license
  → Community support (GitHub Discussions)
  → Free forever

Commercial (Enterprise Edition):
  → Advanced features (SSO, audit logs, RBAC)
  → Commercial license
  → Priority support, SLA
  → Self-hosted or cloud
```

**Best for:**
- Developer tools and infrastructure
- Products where community adoption drives commercial sales
- Companies building credibility through transparency

**Examples:**
- GitLab (open source CE + paid EE)
- n8n (open source + cloud hosted)
- Sentry (open source + hosted)
- PostHog (open source + cloud)

**Pros:**
- Massive adoption through open source
- Community contributions
- Developer credibility
- Self-hosted free version for privacy-conscious companies

**Cons:**
- Competitors can use your code
- Open source version reduces urgency to buy
- Complex dual licensing
- Community management overhead

### 8. Marketplace/App Store Model

**How it works:** Your software is sold through a third-party marketplace.

**Common platforms:**
- **Salesforce AppExchange** — Access to Salesforce customers
- **Shopify App Store** — Shopify merchants
- **Atlassian Marketplace** — Jira/Confluence users
- **Slack App Directory** — Slack users
- **HubSpot App Marketplace** — HubSpot customers

**Revenue split:** Platform takes 15-30% commission

**Best for:**
- Products that enhance a larger platform
- Products with built-in distribution
- Products targeting specific platform users

**Pros:**
- Built-in customer base
- Simplified billing (platform handles it)
- Platform marketing and visibility
- Trust (platform endorsement)

**Cons:**
- Revenue share (15-30%)
- Dependency on platform
- Platform can change rules anytime
- Limited pricing flexibility
- Must comply with platform guidelines

### 9. White-Label / OEM Licensing

**How it works:** Your software is rebranded and resold by another company.

**Common structure:**
```
OEM License:
  → Reseller pays you wholesale (50-70% of retail)
  → Reseller brands as their own
  → They handle support and billing
  → You provide infrastructure and updates

White-Label:
  → Similar to OEM
  → No branding of your company visible
  → Often includes custom domain, colors, logo
```

**Best for:**
- Agencies that want to offer your product as part of their services
- Platform companies adding features to their ecosystem
- Geographic expansion (local resellers in foreign markets)

**Pros:**
- Revenue without marketing/sales effort
- Partner distribution
- Geographic expansion
- Recurring wholesale revenue

**Cons:**
- Lower margins (you sell at 50-70% of retail)
- Brand dilution
- Support complexity (tier 1 from reseller, tier 2 from you)
- Reseller lock-in with their customers

### 10. Usage-Based with Monthly Commit

**How it works:** Customer commits to minimum monthly spend, gets credits they can use.

```
Monthly commit: $500/month (1-year contract)
Billing: $500/month base (prepaid), $0.10 per additional unit above commit
If they use less: They still pay $500 (use it or lose it)
If they use more: They pay $500 + overage
```

**Best for:**
- Enterprise API products
- High-volume customers
- Revenue predictability

**Pros for solo founders:**
- Predictable revenue from commits
- Upside from overage
- Customer commitment (stickier)

**Cons for solo founders:**
- Customer may negotiate commit down
- Complex billing
- Use-it-or-lose-it credits can create customer friction

## Choosing Your Licensing Model

### Decision Framework

```
What type of value do you provide?

[Tool/Utility] ──────────────────┐
[Platform/Infrastructure] ───────┤
[Collaboration/Team] ────────────┤
[Developer Tool] ────────────────┤
[API/Integration] ───────────────┤
[Content/Analytics] ─────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
         Usage or Flat Fee?       Per-seat or Flat fee?
              │                       │
     ┌────────┴────────┐     ┌────────┴────────┐
     ▼                 ▼     ▼                 ▼
  Usage-based     Tiered    Per-seat       Site license
  (API, infra)    (SMB)     (collab)       (enterprise)
```

### Model Selection by Customer Profile

| Customer Type | Best Model | Rationale |
|--------------|-----------|-----------|
| **Individual / Freelancer** | Freemium or $10-29/mo flat | Low willingness to pay, simple needs |
| **SMB (2-50 employees)** | Per-seat or tiered | Predictable budget, simple buying |
| **Mid-market (50-500)** | Usage tier or per-seat + commit | Needs predictability, has budget |
| **Enterprise (500+)** | Site license or annual commit | Procurement wants one PO, not per-user |
| **Developers** | Usage-based or community edition | Want pay-as-you-grow, love free tier |
| **Platforms** | White-label or marketplace | Need to integrate and resell |

### Model Evolution Over Time

Your pricing model can (and should) evolve:

```
Stage 1 (MVP): Simple flat monthly fee
  → "Pay $29/month for everything"
  → Easy to understand, easy to sell

Stage 2 (Growth): Tiered plans
  → "Starter $29, Pro $99, Enterprise Custom"
  → Captures more customer segments

Stage 3 (Scale): Usage-based or hybrid
  → "$99/month + $0.10/unit above"
  → Revenue scales with customer success

Stage 4 (Maturity): Multi-model
  → Different models for different segments
  → Per-seat for SMB, usage for API, site license for enterprise
```

## Legal Considerations for Each Model

### Per-Seat Licensing Legal Language

```
License Grant: Subject to payment of fees, Company grants Customer
a non-exclusive, non-transferable license for [Number] Authorized Users
to access the Service.

Authorized Users: Named individuals within Customer's organization.
Authorized User licenses cannot be shared or reassigned more than once
in any 30-day period.

Over-use: If Customer exceeds the licensed number of Authorized Users,
additional licenses must be purchased within 30 days.

Audit Rights: Company may audit Customer's use of the Service with
reasonable notice. If audit reveals under-licensing, Customer shall
pay for additional licenses plus 10% interest.
```

### Usage-Based Licensing Legal Language

```
Usage Limits: The Service is subject to usage limits as specified in
the Order or Service Description. Usage is measured based on Company's
internal records.

Overage: Usage exceeding included amounts will be billed at the rates
specified in the Order. Company will provide usage notifications at
80%, 90%, and 100% of included usage.

Fair Use: Company reserves the right to implement reasonable usage
limits to prevent abuse of the Service.

Service Credits: If Company's metering is incorrect resulting in
overbilling, Company will credit Customer for the overcharged amount.
Company's records are the definitive source for usage calculations.
```

### Site License Legal Language

```
Site License: Company grants Customer a non-exclusive license to use
the Service by all employees, contractors, and affiliates of Customer
within Customer's organization.

No Sub-licensing: Customer may not sub-license, resell, or distribute
access to the Service to third parties outside Customer's organization.

Affiliates: Customer's affiliates may use the Service under this license
provided Customer remains responsible for compliance.
```

### Annual Commitment Legal Language

```
Annual Commitment: Customer commits to a [12/24/36] month subscription
term. Fees are invoiced annually in advance.

Early Termination: If Customer terminates before the end of the committed
term, Customer must pay [50/100]% of the remaining fees.

Auto-Renewal: The subscription will auto-renew for additional [1-year]
terms unless either party provides [30/60] days notice before renewal.
```

## Licensing Anti-Patterns

| Anti-Pattern | Why It's Bad | Better Approach |
|--------------|-------------|-----------------|
| **Too many plans (5+)** | Analysis paralysis, customer confusion | 3 plans max (Starter, Pro, Enterprise) |
| **Price anchoring** | "Our competitor charges $X" — leads to commoditization | Price based on value, not competitors |
| **Free tier too generous** | Costs outweigh conversion revenue | Limit free tier strictly |
| **Hiding pricing** | Customers don't trust "contact us" | Show pricing clearly |
| **No grandfathering** | Angering existing customers with price hikes | Grandfather for 6-12 months |
| **Per-feature pricing for B2B** | Nickel-and-diming frustrates customers | Tier by usage/users, not features |
| **Enterprise as "everything"** | No clear upgrade path | Specific enterprise features (SSO, audit, SLA) |

## Pricing Model Testing

Before committing to a model, test:

1. **Customer interviews:** "If we charged $X/user/month, would you buy?"
2. **Competitive analysis:** Compare models used by successful competitors
3. **Vanity metric:** What do customers actually care about? (users, usage, features?)
4. **Willingness to pay:** Van Westendorp price sensitivity meter
5. **A/B test pricing page:** Different models to different visitors

## Resources

- [Stripe Billing Guide](https://stripe.com/billing) — Subscription and usage-based billing
- [ProfitWell Pricing Page Examples](https://www.profitwell.com/pricing-page-examples) — Real SaaS pricing pages
- [Price Intelligently Blog](https://www.priceintelligently.com/blog) — SaaS pricing research
- [Chargify's Pricing Model Guide](https://www.chargify.com/blog/saas-pricing-models/) — Comprehensive overview
- [OpenView Pricing Study](https://openviewpartners.com/saas-pricing/) — SaaS pricing benchmarks
- [Recurly Pricing Page Examples](https://recurly.com/research/pricing-page-examples/)
