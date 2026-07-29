# Building a Reseller Channel for Your SaaS

## Why a Reseller Channel?

A reseller channel lets other companies sell your software to their customers. For a solo founder, this can be a force multiplier — giving you a sales team without hiring anyone.

**Benefits for solo founders:**
- **Distribution without cost** — Resellers bring their customer relationships
- **Geographic expansion** — Resellers in foreign markets open new regions
- **Market credibility** — Being "on the channel" signals stability
- **Recurring revenue** — Wholesale pricing means recurring income
- **Focus on product** — Partners handle the sales process

**Challenges:**
- **Margins** — You give up 20-50% of revenue
- **Brand control** — Partner represents your brand (for better or worse)
- **Support complexity** — Who handles support? Tier 1 vs Tier 2?
- **Partner management** — Resellers need enablement, training, and support
- **Channel conflict** — Partners competing with your direct sales

## Types of Reseller Partnerships

### 1. Referral Partner (Simplest)

**How it works:** Partner refers leads to you. You close the deal and pay a commission.

```
Commission: 15-25% of first-year revenue OR 20-30% of first payment
Payment: One-time (or first 3-6 months of subscription)
Example: Partner refers customer → customer signs up for $100/month
         → You pay partner $30/month for 6 months ($180 total)
```

**Pros:**
- Simplest setup
- No legal complexity (no sub-licensing)
- You control pricing and relationship
- Easy to track (referral link/code)

**Cons:**
- Partner has less incentive (one-time payment)
- Partner doesn't "own" the customer relationship
- Lower partner engagement

**Best for:**
- Agencies, consultants, freelancers
- Bloggers and content creators
- Complementary SaaS products
- Early stage (testing channel)

### 2. Reseller / Value-Added Reseller (VAR)

**How it works:** Partner buys your software at wholesale and resells at retail. They invoice the customer and handle support.

```
Wholesale: 50% off retail (partner pays you $50 for $100 list price)
Retail price: Partner sets their own price (usually MSRP or higher)
Support: Partner handles tier 1, you handle tier 2/3
Billing: Partner bills customer; you bill partner monthly
Example: Partner buys license at $50/seat, sells to customer at $100/seat
         Partner keeps $50/seat, pays you $50/seat monthly
```

**Pros:**
- Partner has ownership of customer relationship
- Higher partner margins → more motivated
- Partner adds value (implementation, customization)
- Scales well with established partners

**Cons:**
- Complex billing (partner invoices you, you invoice partner)
- Support confusion (who handles what?)
- Partner branding may override yours
- Requires partner training

**Best for:**
- B2B products with implementation/setup needs
- Geographic expansion (partners in target markets)
- Products targeting specific industries (healthcare, legal)

### 3. White-Label Partner

**How it works:** Partner rebrands your software as their own. No indication it's your product.

```
Wholesale: 40-60% off retail
Branding: Partner's logo, domain, colors, terms of service
Support: Partner handles ALL support (tier 1, 2, 3)
Billing: Partner bills customer directly
You provide: Infrastructure, updates, backend
Example: Customer sees "Acme Analytics" by their MSP
         Behind the scenes, it's your software
```

**Pros:**
- Partner makes it their own (high motivation)
- No customer relationship for you (partner does it all)
- Potential for massive scale via large partners

**Cons:**
- No brand awareness for you
- You're invisible to the end customer
- Partner may switch to another provider
- Heavy support from you (back-end infrastructure)
- Lower margins (usually 40-60% to partner)

**Best for:**
- Agencies offering services to clients
- MSPs (Managed Service Providers)
- Established companies adding your feature to their platform
- Situations where you don't want to build a brand

### 4. Marketplace Partner

**How it works:** Your product is listed on an app marketplace (Shopify, Salesforce, Atlassian, HubSpot).

```
Revenue share: Platform takes 15-30%
Pricing: You set your own price; platform takes cut
Discovery: Customers find you through marketplace search
Billing: Platform handles billing and remits payment to you
```

**Pros:**
- Massive built-in distribution
- Platform handles billing (reduces churn)
- Trust (platform endorsement)
- Lower support burden (platform provides some)

**Cons:**
- Significant revenue share (15-30%)
- Platform dependency
- Must comply with platform rules
- May need to build integration first

**Best for:**
- Products that enhance an existing platform
- Products with strong platform affinity
- Growing a user base quickly

### 5. Technology Partnership (Integration)

**How it works:** Partner integrates with your API and they co-sell or resell to their customers.

```
Revenue: Varies (referral commission, co-sell, or reseller)
Type: Marketing partnership + potential reseller
Support: Each handles their own product
```

**Best for:**
- Complementary products
- "Works with [Product]" co-marketing
- API-first products

## Building Your Partner Program

### Step 1: Define Your Offer

```markdown
Partner Program Overview

Product: [Product Name]
Target partners: [Agencies / MSPs / SaaS companies / Consultants]

Partner Tiers:
  Bronze (Referral):
    → Commission: 20% of first 6 months revenue
    → Requirements: Submit qualified leads
    → Support: Email support

  Silver (Reseller):
    → Discount: 30% off retail
    → Requirements: $2,000/month minimum commitment
    → Support: Email + Slack channel
    → Training: Self-paced online

  Gold (White-Label):
    → Discount: 50% off retail
    → Requirements: $10,000/month minimum commitment
    → Support: Priority email + dedicated Slack channel
    → Training: Live onboarding + quarterly business reviews
    → Extras: Custom branding, dedicated infrastructure, API access
```

### Step 2: Create Partner Materials

```markdown
Partner Enablement Kit:

1. Product overview (pitch deck)
   → What it does, who it's for, key benefits
   → Competitive differentiators
   → Pricing and packaging

2. Demo script and recordings
   → 15-minute standard demo
   → 5-minute elevator pitch
   → Feature deep-dives

3. Sales materials
   → Case studies and testimonials
   → ROI calculator
   → Comparison matrix
   → FAQ for common objections

4. Technical materials
   → API documentation (if reseller builds integrations)
   → Integration guides
   → White-labeling instructions

5. Legal documents
   → Partner agreement template
   → Pricing and discount schedules
   → SLA terms
```

### Step 3: Set Up Partner Tracking

**Tools for partner management:**

| Tool | Cost | Best For |
|------|------|----------|
| **PartnerStack** | Free + revenue share | Referral and affiliate programs |
| **Impact** | Custom pricing | Enterprise partner management |
| **FirstPromoter** | $59-249/month | Affiliate and referral tracking |
| **ReferralCandy** | $49/month | Referral programs |
| **Tolt** | $29-99/month | Simple referral tracking |
| **Custom (Stripe + webhooks)** | Free (development time) | Simple tracking via your app |

**Minimum tracking setup:**
```markdown
1. Unique referral link for each partner (e.g., yourdomain.com/?ref=partner123)
2. Cookie tracking (30-90 day attribution window)
3. Commission tracking (per subscription, per payment)
4. Dashboard showing:
   → Leads referred
   → Conversion rate
   → Revenue generated
   - Commissions earned and paid
```

**Tracking implementation (simplified):**

```javascript
// When a user signs up with a referral code
app.post('/api/signup', async (req, res) => {
  const { email, referralCode } = req.body;
  
  // Create user
  const user = await User.create({ email });
  
  // Track referral
  if (referralCode) {
    const partner = await Partner.findOne({ code: referralCode });
    if (partner) {
      await Referral.create({
        partnerId: partner.id,
        userId: user.id,
        status: 'pending', // becomes 'active' on first payment
        commissionRate: partner.commissionRate
      });
    }
  }
  
  res.json({ user });
});

// When subscription payment succeeds, credit commission
stripeWebhooks.on('invoice.paid', async (invoice) => {
  const subscription = await stripe.subscriptions.retrieve(invoice.subscription);
  const user = await User.findOne({ stripeId: subscription.customer });
  const referral = await Referral.findOne({ userId: user.id });
  
  if (referral && referral.status === 'pending') {
    referral.status = 'active';
    await referral.save();
    
    // Create commission
    await Commission.create({
      partnerId: referral.partnerId,
      referralId: referral.id,
      amount: invoice.amount_paid * (referral.commissionRate / 100),
      status: 'earned' // becomes 'paid' when you send payment
    });
  }
});
```

### Step 4: Recruit Partners

**Where to find reseller partners:**

```
Existing customers:
  → Who loves your product and refers others?
  → Offer them your referral program

Industry consultants and agencies:
  → They already sell to your target market
  → Your product complements their services

Complementary SaaS products:
  → Products serving the same customers
  → Non-competing, complementary features

Freelancers in your space:
  → Implementation consultants
  → Configuration and setup specialists

Former colleagues and network:
  → People who know your industry
  - Trusted referrals

Competitor's customers who are looking:
  → May want to offer your product alongside
  → Approach carefully (anti-competitive?)
```

**Partner recruitment pitch:**

```
Subject: Partnership opportunity with [Your Product]

Hi [Name],

I've been following [Their Company] and I think there's a great
opportunity for us to work together.

[Product Name] helps [target customer] solve [problem]. It
complements what you do at [Their Company] by [specific value].

I'm looking for [agency/SaaS/consulting] partners who:

1. Work with [target customer type]
2. Want to offer [solution] to their clients
3. Are looking for recurring revenue stream

As a partner, you'd get:
- [X]% commission on every sale
- [Custom branding / Co-marketing / Priority support]
- Dedicated partner manager (me!)

Would you be open to a 15-minute call to explore this?

Best,
[Your Name]
[Your Title]
```

### Step 5: Partner Agreement

**Essential clauses in a reseller agreement:**

```markdown
Reseller Agreement

1. Appointment
   Company appoints Reseller as a non-exclusive reseller of the Product.

2. License
   Reseller may market, demonstrate, and sell the Product to end users.
   Reseller may not modify, reverse engineer, or create derivative works.

3. Pricing and Payment
   Reseller purchases at Wholesale Price (Schedule A).
   Reseller sets its own retail price.
   Payment is due Net-30 from invoice date.

4. Support
   Reseller handles Tier 1 support (basic questions, account management).
   Company handles Tier 2/3 support (technical issues, bugs).
   Support escalation process defined in Schedule B.

5. Branding
   Reseller may use Company's trademarks for marketing.
   Reseller may NOT claim ownership of the Product.
   White-label partners may rebrand (per separate Addendum).

6. Term and Termination
   Initial term: 12 months. Auto-renew unless terminated.
   Either party may terminate with 30 days notice.
   Company may terminate immediately for breach.

7. Non-Compete
   During this agreement, Reseller may not sell competing products.

8. Confidentiality
   Both parties protect each other's confidential information.

9. Limitation of Liability
   Company's liability is limited to fees paid by Reseller in last
   12 months.

10. Governing Law
   [State] law.

Signatures:
Company: _______________   Reseller: _______________
Date: __________________   Date: __________________
```

**Schedule A — Pricing:**
```
Product: [Product Name]
Wholesale Price (Monthly):      $50 per seat (50% off $100 MSRP)
Wholesale Price (Annual):       $480 per seat (60% off $1,200 MSRP)
Minimum Monthly Commit:         $500 (after 3-month ramp period)
Commission (Referral Only):     20% of first 12 months revenue
Payment Terms:                  Net-30
Price Changes:                  30 days notice
```

### Step 6: Enable and Support Partners

**Partner onboarding process:**

```
Week 1: Setup
  → Sign partner agreement
  → Create partner account in your system
  → Provide access to partner portal
  → Set up referral tracking (links, codes)
  → Kickoff call (30 minutes)

Week 2-3: Training
  → Product demo and walkthrough
  → Sales playbook and objection handling
  → Support escalation process
  - Technical setup (if white-label)
  → Competitive positioning

Week 4: First deal
  → Shadow a real demo (you present)
  → Co-sell first deal (you close together)
  → Review process and refine

Ongoing:
  → Weekly check-in calls (first month)
  → Monthly partner newsletter
  → Quarterly business review
  → Partner portal with resources
  → Slack/Discord community for partners
```

### Step 7: Pay Commissions

**Commission structure:**

| Partner Type | Commission | Payment Schedule |
|-------------|-----------|-----------------|
| **Referral** | 20% of first 12 months | Monthly, 30 days after customer payment |
| **Reseller** | 30-50% discount on wholesale | Monthly, Net-30 |
| **White-label** | 40-60% discount on wholesale | Monthly, Net-30 |

**Commission payment best practices:**
- Pay automatically (Stripe + automated transfers)
- Pay on time, every time (builds trust)
- Provide clear commission statements
- Handle clawbacks (if customer churns within 90 days, claw back commissions)

## Managing Channel Conflict

Channel conflict arises when you sell directly to a customer who might also be a partner's prospect.

### Strategies to Avoid Conflict:

```
1. Define territories clearly
   → Geographic (US vs EU vs APAC)
   → Segment (SMB vs Enterprise)
   → Industry (Healthcare vs Technology)

2. Lead registration
   → Partner registers a lead → gets exclusive commission
   → You don't sell direct to registered leads
   → Registration expires after 60-90 days without progress

3. Deal registration benefits
   → Registered leads get better pricing for partner
   → Registered leads don't count against minimums
   → First-to-register gets priority

4. Channel-first policy
   → If a partner is active in a territory, route leads to them
   → Only sell direct if no partner exists in that area
```

**Lead registration process:**

```
1. Partner submits lead via portal:
   → Company name
   → Contact name and email
   - Estimated deal size
   → Expected close date

2. You check:
   → Is this lead already registered? (First-to-register wins)
   → Is this lead already a direct customer? (If yes, no commission)

3. If approved:
   → Lead registered for 90 days
   → Partner receives better discount (additional 5-10%)
   → You won't sell direct to this lead

4. If no progress in 90 days:
   → Registration expires
   → Lead becomes available to other partners or direct
```

## Partner Program Metrics

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| **Partner count** | Program size | Depends on stage |
| **Active partners** | % of partners sending leads monthly | > 50% |
| **Partner-driven revenue** | Revenue from channel | 20-50% of total |
| **Partner churn** | % of partners leaving per quarter | < 10%/quarter |
| **Partner satisfaction (NPS)** | How happy partners are | > 50 |
| **Lead-to-customer conversion** | Partner lead quality | 10-20% |
| **Average deal size (partner)** | Deal value from channel | Compare to direct |
| **Time to first partner sale** | Onboarding effectiveness | < 30 days |

## Partner Program by Stage

### Stage 1: Pre-Revenue / Early ($0-5k MRR)

```
Focus: Referral program
Action:
  → Set up simple referral tracking (referral code + spreadsheet)
  → Offer 25% commission on first 6 months
  → Recruit 3-5 initial partners (friends, network, early customers)

Warning: Don't spend too much time on this early. Focus on product.
Time investment: 2-4 hours/month
```

### Stage 2: Growth ($5-20k MRR)

```
Focus: Formal referral program + first reseller
Action:
  → Implement referral tool (PartnerStack, FirstPromoter)
  → Define partner tiers (Referral + Reseller)
  → Recruit 10-20 partners
  → Create partner enablement kit
  → Hire part-time partner manager (or you manage)

Time investment: 5-10 hours/week
```

### Stage 3: Scale ($20k+ MRR)

```
Focus: Full reseller channel
Action:
  → Launch reseller program with multiple tiers
  → Recruit regional partners for geographic expansion
  → Add white-label option for MSPs/large agencies
  → Build partner portal and training program
  → Hire dedicated partner manager

Time investment: 15-20 hours/week
```

## Common Reseller Mistakes

| Mistake | Why It's Bad | Prevention |
|---------|-------------|-----------|
| **No partner minimums** | Partners with zero productivity drain your time | Minimum commit or inactivity termination |
| **No lead registration** | Partners compete with each other and with you | Clear first-to-register policy |
| **Paying upfront commissions** | Customer can churn before commission is earned | Pay after customer pays (monthly) |
| **No partner training** | Partner misrepresents your product | Mandatory training + certification |
| **Over-discounting** | You can't sustain the economics | Start at 20-30% discount, increase for volume |
| **Ignoring partner feedback** | Partners know your market | Quarterly partner feedback sessions |
| **Too many partners** | Diluted support and attention | Limit partners by capacity |
| **Partner takes your customer** | Partner switches customer to competitor | Non-compete, strong relationship with end customer |

## Solo Founder vs Enterprise Partner Programs

| Aspect | Solo Founder Approach | Enterprise Approach |
|--------|----------------------|-------------------|
| **Partner agreements** | Simple, standardized | Custom contracts per partner |
| **Discounts** | Fixed 20-30% | Negotiated, volume-based |
| **Support** | Email + Slack | Dedicated partner manager |
| **Training** | Self-paced online | Live + certification |
| **Partner portal** | Simple dashboard | Full CRM integration |
| **Co-marketing** | Basic co-branding | Joint webinars, events, case studies |
| **Lead registration** | Manual (spreadsheet) | Automated in CRM |
| **Payment** | Stripe/ PayPal | Net-30 invoicing |
| **Minimum commitment** | $500-1000/month | $5,000-50,000/month |

## Resources

- [PartnerStack](https://partnerstack.com/) — Partner management platform
- [FirstPromoter](https://firstpromoter.com/) — Referral and affiliate tracking
- [Impact](https://impact.com/) — Enterprise partner management
- [ReferralCandy](https://www.referralcandy.com/) — Simple referral programs
- [Partner Agreement Template (Rocket Lawyer)](https://www.rocketlawyer.com/)
- [Salesforce AppExchange Partner Program](https://www.salesforce.com/products/appexchange/overview/)
- [Shopify Partner Program](https://www.shopify.com/partners)
- [HubSpot Solutions Partner Program](https://www.hubspot.com/partners)
