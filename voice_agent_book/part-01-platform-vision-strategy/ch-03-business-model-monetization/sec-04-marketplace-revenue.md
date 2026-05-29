# Section 04: Marketplace Revenue

## Marketplace Vision

The marketplace is a strategic revenue stream and ecosystem moat. It enables third-party creators to build and sell templates, voices, plugins, and themes — with our platform taking a revenue share.

```
Marketplace Architecture
┌────────────────────────────────────────────────────────────────────┐
│                        Marketplace Storefront                      │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐             │
│  │ Templates    │ │ Voice Packs  │ │ Plugins      │             │
│  │ (Agent flows)│ │ (Custom TTS) │ │ (Integrations)│             │
│  └──────────────┘ └──────────────┘ └──────────────┘             │
│  ┌──────────────┐ ┌──────────────┐                               │
│  │ Themes       │ │ AI Models    │                               │
│  │ (UI skins)   │ │ (Fine-tuned) │                               │
│  └──────────────┘ └──────────────┘                               │
├────────────────────────────────────────────────────────────────────┤
│                        Creator Ecosystem                            │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────────┐    │
│  │ Revenue Share  │ │ Analytics &    │ │ Creator Tools      │    │
│  │ (20-30% platf.)│ │ Performance    │ │ (publish, version) │    │
│  └────────────────┘ └────────────────┘ └────────────────────┘    │
├────────────────────────────────────────────────────────────────────┤
│                      Payment & Fulfillment                         │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────────┐    │
│  │ Stripe Connect │ │ License Key    │ │ Subscription       │    │
│  │ Payouts        │ │ Management     │ │ Syncing            │    │
│  └────────────────┘ └────────────────┘ └────────────────────┘    │
└────────────────────────────────────────────────────────────────────┘
```

## Marketplace Categories

### Category 1: Agent Templates (30% platform commission)
**What:** Pre-built agent configurations for specific use cases. **Examples:** Dental office scheduler, e-commerce order status, real estate lead qualifier, healthcare appointment reminder. **Creator economics:** $29-99 per template. Top creator earns $5K+/month. **Volume target:** 200+ templates by end of Year 1.

### Category 2: Voice Packs (20% platform commission)
**What:** Custom TTS voice models. **Examples:** Regional accents, celebrity voices (licensed), industry-specific tone, multilingual voices. **Creator economics:** $9-29 per voice pack. **Volume target:** 100+ voice packs by end of Year 1.

### Category 3: Plugins & Integrations (25% platform commission)
**What:** Third-party integrations and extensions. **Examples:** Salesforce data sync, custom sentiment analysis model, appointment scheduling (Calendly), payment processing (Stripe). **Creator economics:** $49-199 per plugin, or subscription ($9-49/mo). **Volume target:** 50+ plugins by end of Year 1.

### Category 4: UI Themes (15% platform commission)
**What:** Dashboard and agent customization themes. **Creator economics:** $9-29 per theme. **Volume target:** 50+ themes by end of Year 1.

## Revenue Share Model

```
Marketplace Revenue Distribution
┌────────────────────────────────────────────────────────────────────────┐
│ Item        │ Price   │ Platform Share │ Creator Share │ Platform Rev  │
├────────────────────────────────────────────────────────────────────────┤
│ Template    │ $49     │ 30% ($14.70)   │ 70% ($34.30)  │ $14.70        │
│ Voice pack  │ $19     │ 20% ($3.80)    │ 80% ($15.20)  │ $3.80         │
│ Plugin (1x) │ $99     │ 25% ($24.75)   │ 75% ($74.25)  │ $24.75        │
│ Plugin (sub)│ $19/mo  │ 25% ($4.75)    │ 75% ($14.25)  │ $4.75/mo      │
│ Theme       │ $19     │ 15% ($2.85)    │ 85% ($16.15)  │ $2.85         │
└────────────────────────────────────────────────────────────────────────┘
```

## Marketplace Data Model

```typescript
interface MarketplaceItem {
  id: string;
  type: 'template' | 'voice' | 'plugin' | 'theme';
  name: string;
  description: string;
  creatorId: string;
  price: number;
  subscriptionPrice?: number; // for plugins with monthly pricing
  commissionRate: number; // 0.15 - 0.30
  version: string;
  compatibility: string; // e.g., ">=1.0.0"
  rating: number;
  downloadCount: number;
  revenue: number;
  status: 'draft' | 'published' | 'deprecated' | 'removed';
}

interface CreatorAccount {
  id: string;
  userId: string;
  totalEarnings: number;
  pendingPayout: number;
  lifetimeSales: number;
  items: MarketplaceItem[];
  payoutMethod: 'stripe' | 'paypal' | 'bank';
  taxInfo: TaxInfo;
}

function calculateCreatorPayout(creatorId: string, period: DateRange): PayoutSummary {
  const items = getCreatorItems(creatorId);
  let totalSales = 0;
  let platformFees = 0;
  
  for (const item of items) {
    const sales = getItemSales(item.id, period);
    totalSales += sales.revenue;
    platformFees += sales.revenue * item.commissionRate;
  }
  
  return {
    grossRevenue: totalSales,
    platformCommission: platformFees,
    creatorEarnings: totalSales - platformFees,
    payoutDate: period.end.plus({ days: 15 }), // Net 15 to creators
  };
}
```

## Marketplace Revenue Projection

```
Year 1 Marketplace Revenue Forecast
Month 1-3:   Platform development, no marketplace revenue
Month 4-6:   Beta launch, 20 templates, 10 voices → $500/mo platform rev
Month 7-9:   Public launch, 100 items → $3K/mo platform rev
Month 10-12: Growth phase, 200+ items → $8K/mo platform rev
Year 2:      $50K/mo platform revenue
Year 3:      $200K/mo platform revenue (10% of total company rev)
```

## Creator Onboarding & Incentives

**Launch incentives:** First 50 creators get 0% platform commission for 6 months (100% creator earnings). **Featured status:** Top creators get homepage placement, newsletter features, social media promotion. **Creator tiers:** Bronze (<$1K earnings), Silver ($1-10K), Gold ($10-100K), Platinum ($100K+). Higher tiers get lower commission rates and dedicated support.

## Quality Control & Moderation

- Automated review: Malware scanning, schema validation, test execution
- Manual review: Every item reviewed by platform team before publishing
- Rating system: 1-5 stars with mandatory review text
- Reporting: Abuse reporting system for policy violations
- Removal: Platform right to remove items that violate terms (with appeal process)

## Competitive Comparison

| Marketplace Feature | Us | Retell AI | Vapi | Bland AI |
|-------------------|-----|-----------|------|----------|
| Marketplace | ✅ Planned | ❌ | ❌ | ❌ |
| Creator payouts | ✅ Stripe Connect | N/A | N/A | N/A |
| Revenue share | 15-30% | N/A | N/A | N/A |
| Template library | ✅ | Limited (in-house) | ❌ | ❌ |
| Voice packs | ✅ | ❌ | ❌ | ❌ |
| Plugin system | ✅ | ❌ | ❌ | ❌ |

## Pricing & Commission Strategy

**Why 15-30%:** Industry standard for SaaS marketplaces. Shopify: 15-30%. Salesforce AppExchange: 15-25%. Atlassian Marketplace: 15-30%. Lower rates for themes (15%) to encourage customization. Higher for templates (30%) where platform provides more value.

## Legal & Tax Considerations

- Creator terms of service with IP ownership clarity
- Platform indemnification for IP-infringing items
- Tax withholding for international creators (W-8BEN, W-9)
- Revenue recognition: Recognize platform commission at point of sale
- Creator payouts: Net 15, minimum $50 payout threshold

## Tools & Resources

- **Marketplace platform:** Custom (Next.js + Stripe Connect)
- **Payouts:** Stripe Connect, Tipalti (at scale)
- **Asset delivery:** Cloudflare R2, AWS S3 + CloudFront
- **Review system:** Custom with automated scanning
- **Creator dashboard:** Retool, Appsmith (internal tools)
- **Analytics:** PostHog (product analytics), Metabase (business analytics)
