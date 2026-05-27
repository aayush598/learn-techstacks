# Section 06: Promotional Credits

## Promo Credit Creation

Promotional credits are issued as part of marketing campaigns, customer reactivation, or goodwill gestures. They differ from purchased credits in their source, expiration, and usage restrictions.

```typescript
interface PromotionalCreditCampaign {
  id: string;
  name: string;
  description: string;
  creditAmount: number;
  targetSegments: string[];
  maxRedemptions: number;
  redemptionsUsed: number;
  validFrom: string;
  validTo: string;
  expiryDays: number;
  usageRestrictions: PromoUsageRestrictions;
  status: 'active' | 'paused' | 'completed';
}

interface PromoUsageRestrictions {
  applicableMeters?: string[];   // Which meters can use these credits
  minPurchaseAmount?: number;    // Minimum purchase to use promo
  maxDiscountPercent?: number;   // Max discount promo can provide
  onePerCustomer: boolean;
}

class PromotionalCreditService {
  async createCampaign(campaign: PromotionalCreditCampaign): Promise<void> {
    await this.db.promotionalCampaigns.create({
      ...campaign,
      createdAt: new Date().toISOString(),
    });
  }

  async issuePromotionalCredits(
    tenantId: string,
    campaignId: string,
    reason?: string
  ): Promise<CreditLedgerEntry> {
    const campaign = await this.db.promotionalCampaigns.findOne({
      id: campaignId,
      status: 'active',
    });

    if (!campaign) throw new Error('Campaign not found or inactive');
    if (campaign.redemptionsUsed >= campaign.maxRedemptions) {
      throw new Error('Campaign max redemptions reached');
    }

    // Check one-per-customer restriction
    if (campaign.usageRestrictions.onePerCustomer) {
      const existing = await this.db.creditLedger.findOne({
        tenantId,
        type: CreditTransactionType.PROMO_CREDIT,
        'metadata.campaignId': campaignId,
      });

      if (existing) {
        throw new Error('Customer already received this promotional credit');
      }
    }

    // Issue credits
    const entry = await this.ledgerService.recordTransaction({
      tenantId,
      type: CreditTransactionType.PROMO_CREDIT,
      amount: campaign.creditAmount,
      currency: 'credits',
      description: `Promotional credit: ${campaign.name}`,
      metadata: {
        source: 'promotion',
        campaignId: campaign.id,
        tags: ['promo', campaign.id],
        usageRestrictions: campaign.usageRestrictions,
      },
      effectiveAt: new Date().toISOString(),
      expiresAt: new Date(Date.now() + campaign.expiryDays * 86400000).toISOString(),
    });

    // Update campaign counter
    await this.db.promotionalCampaigns.updateOne(
      { id: campaignId },
      { $inc: { redemptionsUsed: 1 } }
    );

    return entry;
  }
}
```

## Campaign Attribution

Promotional credits are tracked with campaign attribution to measure marketing effectiveness. Attribution data links credit issuance to specific campaigns, channels, and touchpoints.

```typescript
interface CreditAttribution {
  creditEntryId: string;
  tenantId: string;
  campaignId: string;
  campaignName: string;
  channel: string;              // 'email', 'in_app', 'referral', 'support'
  touchpoint: string;           // Specific email campaign, banner, etc.
  attributedBy: string;         // System or user who attributed
  conversionValue?: number;     // Revenue generated from this customer
}

class CreditAttributionService {
  async attributeCredits(
    options: {
      tenantId: string;
      campaignId: string;
      channel: string;
      touchpoint: string;
      creditEntryId: string;
      attributedBy: string;
    }
  ): Promise<void> {
    await this.db.creditAttributions.create({
      ...options,
      createdAt: new Date().toISOString(),
    });
  }

  async getCampaignROI(campaignId: string): Promise<CampaignROI> {
    const campaign = await this.db.promotionalCampaigns.findOne({ id: campaignId });
    const attributions = await this.db.creditAttributions.find({
      campaignId,
    }).toArray();

    // Total credits issued
    const totalCreditsIssued = campaign.creditAmount * campaign.redemptionsUsed;
    const totalCost = totalCreditsIssued * 0.005; // Credit cost

    // Revenue from attributed customers
    let totalRevenue = 0;
    for (const attr of attributions) {
      const revenue = await this.getCustomerRevenue(attr.tenantId);
      totalRevenue += revenue;
    }

    return {
      campaignId,
      campaignName: campaign.name,
      totalIssued: totalCreditsIssued,
      totalCost,
      totalRevenue,
      roi: totalCost > 0 ? (totalRevenue - totalCost) / totalCost : 0,
      conversionCount: attributions.length,
    };
  }

  private async getCustomerRevenue(tenantId: string): Promise<number> {
    const result = await this.db.invoices.aggregate([
      { $match: { tenantId, status: 'paid' } },
      { $group: { _id: null, total: { $sum: '$total' } } },
    ]).toArray();
    return result[0]?.total || 0;
  }
}
```

## Usage Restrictions

Promotional credits may have restrictions on which services they can be used for. For example, promotion credits might only apply to voice minutes, not to add-ons.

```typescript
async function validatePromoCreditUsage(
  tenantId: string,
  meter: string,
  amount: number
): Promise<{ allowed: boolean; remainingPromoBalance: number }> {
  // Check promotional credit balance
  const promoBalance = await this.db.creditLedger.aggregate([
    {
      $match: {
        tenantId,
        type: CreditTransactionType.PROMO_CREDIT,
        expiresAt: { $gt: new Date().toISOString() },
      },
    },
    { $group: { _id: null, balance: { $sum: '$amount' } } },
  ]).toArray();

  const availablePromo = promoBalance[0]?.balance || 0;
  if (availablePromo <= 0) {
    return { allowed: true, remainingPromoBalance: 0 }; // No promo to restrict
  }

  // Check if this meter is covered by promo restrictions
  const promoEntries = await this.db.creditLedger.find({
    tenantId,
    type: CreditTransactionType.PROMO_CREDIT,
    amount: { $gt: 0 },
  }).toArray();

  for (const entry of promoEntries) {
    const restrictions = entry.metadata?.usageRestrictions as PromoUsageRestrictions;
    if (restrictions?.applicableMeters && !restrictions.applicableMeters.includes(meter)) {
      // Promo credits can't be used for this meter — skip promo balance
      continue;
    }
  }

  return { allowed: true, remainingPromoBalance: availablePromo };
}
```

## Expiry Configuration

Promotional credits typically have shorter expiry periods than purchased credits to create urgency. Standard promotional credit expiry is 30-90 days.

```typescript
const PROMO_EXPIRY_CONFIG = {
  defaultDays: 90,
  minimumDays: 14,
  maximumDays: 365,

  // Per-campaign expiry
  campaignDefaults: {
    welcome_bonus: { days: 90 },
    reactivation: { days: 30 },
    referral_reward: { days: 180 },
    seasonal_promo: { days: 60 },
    support_goodwill: { days: 365 },
  },
};
```

## Open-Source Tools

- **PostgreSQL** — Campaign and attribution storage
- **BullMQ** — Schedule campaign activation/deactivation
- **Redis** — Cache campaign eligibility checks
- **Metabase** (Apache 2.0) — Campaign ROI dashboards

## Integration Points

Promotional credits connect to the marketing automation system (campaign triggers), the credit ledger (issuance), the usage consumption system (restriction enforcement), and the analytics service (ROI tracking).

## Production Considerations

- Limit promotional credit campaigns to prevent abuse
- Track promotional credit cost as a marketing expense
- Set up campaign budget alerts
- Monitor promotional credit impact on paid credit purchases
- A/B test promotional credit amounts for optimal ROI

## Open-Source First Philosophy

PostgreSQL stores campaign data and attribution, Metabase provides ROI dashboards, and BullMQ manages campaign scheduling. This all-open-source approach replaces expensive marketing promotion platforms while providing complete control over promotional credit campaigns.
