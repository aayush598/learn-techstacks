# Section 06: Marketplace Facilitator Rules

## Marketplace vs Seller of Record

When operating a marketplace (e.g., allowing third-party voice agents), the platform may be considered the "marketplace facilitator" and is responsible for collecting and remitting sales tax on behalf of sellers. This shifts the tax burden from individual sellers to the platform.

```typescript
interface MarketplaceFacilitatorConfig {
  platformType: 'direct' | 'marketplace' | 'hybrid';
  taxResponsibility: 'platform' | 'seller' | 'shared';
  facilitatorStates: string[];    // States where we're the facilitator
  reportingRequirements: 'monthly' | 'quarterly' | 'annual';
}

class MarketplaceTaxService {
  async determineTaxResponsibility(
    transaction: Transaction,
    sellerInfo: SellerInfo
  ): Promise<TaxResponsibility> {
    const sellerState = sellerInfo.businessState;
    const customerState = transaction.billingState;

    // Check if both parties are in facilitator states
    const isFacilitatorState = FACILITATOR_STATES.includes(customerState);

    if (isFacilitatorState) {
      return {
        responsible: 'platform',
        rule: 'marketplace_facilitator',
        notes: `Platform collects tax as marketplace facilitator in ${customerState}`,
      };
    }

    // Fall back to seller responsibility
    return {
      responsible: 'seller',
      rule: 'seller_of_record',
      notes: 'Seller is responsible for tax collection',
    };
  }

  async calculateMarketplaceTax(
    transaction: Transaction,
    sellerInfo: SellerInfo
  ): Promise<TaxResult> {
    const responsibility = await this.determineTaxResponsibility(transaction, sellerInfo);

    if (responsibility.responsible === 'platform') {
      // Platform calculates and collects tax
      const rate = await this.getTaxRate(
        transaction.billingState,
        transaction.productTaxCode
      );

      return {
        taxAmount: Math.round(transaction.amount * rate),
        taxRate: rate,
        collectedBy: 'platform',
        rule: 'marketplace_facilitator',
        reportingCategory: 'facilitator_sales',
      };
    } else {
      // Seller is responsible — pass through
      return {
        taxAmount: 0,
        taxRate: 0,
        collectedBy: 'seller',
        rule: 'seller_of_record',
        reportingCategory: 'seller_responsible',
        sellerNote: 'Seller must collect and remit tax',
      };
    }
  }
}
```

## Tax Collection Responsibility

Marketplace facilitator rules vary by state. As of 2024, most US states with sales tax have enacted marketplace facilitator laws. The platform must track its responsibility in each state.

```
Marketplace Facilitator States (US):
┌──────────────────────────────────────────────────────────────────┐
│ Status      │ States                                             │
├─────────────┼────────────────────────────────────────────────────┤
│ Enacted     │ AL, AZ, CA, CO, CT, DC, FL, GA, HI, IL, IN, IA,  │
│             │ KY, LA, ME, MD, MA, MI, MN, MS, NE, NV, NJ, NM,  │
│             │ NY, NC, ND, OH, OK, PA, RI, SC, SD, TN, TX, UT,  │
│             │ VT, VA, WA, WV, WI, WY                            │
│ Not enacted │ AK*, DE*, MT*, NH*, OR* (*No sales tax)           │
│ Pending     │ KS, MO                                             │
└──────────────────────────────────────────────────────────────────┘
```

## Reporting Requirements

Marketplace facilitators must report sales separately from direct sales. Reports are filed in each state where the platform has facilitator responsibility.

```typescript
interface FacilitatorReport {
  state: string;
  period: string;
  platformSales: MarketplaceSalesSummary;
  sellerSales: SellerSalesSummary[];
  totalTaxCollected: number;
  filingDeadline: string;
}

interface MarketplaceSalesSummary {
  totalTransactions: number;
  totalSales: number;
  totalTaxableSales: number;
  totalTaxCollected: number;
  productBreakdown: ProductTaxBreakdown[];
}

async function generateFacilitatorReport(
  state: string,
  period: string
): Promise<FacilitatorReport> {
  const platformSales = await this.db.invoices.aggregate([
    {
      $match: {
        'taxBreakdown.jurisdiction.state': state,
        'metadata.facilitator_sale': 'true',
        createdAt: { $regex: period },
      },
    },
    {
      $group: {
        _id: null,
        totalTransactions: { $sum: 1 },
        totalSales: { $sum: '$total' },
        totalTaxableSales: { $sum: '$subtotal' },
        totalTaxCollected: { $sum: '$taxTotal' },
      },
    },
  ]).toArray();

  // Get seller-level breakdown
  const sellerSales = await this.db.invoices.aggregate([
    {
      $match: {
        'taxBreakdown.jurisdiction.state': state,
        'metadata.facilitator_sale': 'true',
        createdAt: { $regex: period },
      },
    },
    {
      $group: {
        _id: '$metadata.seller_id',
        sellerName: { $first: '$metadata.seller_name' },
        totalSales: { $sum: '$total' },
        taxableSales: { $sum: '$subtotal' },
        taxCollected: { $sum: '$taxTotal' },
        transactions: { $sum: 1 },
      },
    },
  ]).toArray();

  return {
    state,
    period,
    platformSales: platformSales[0] || {
      totalTransactions: 0,
      totalSales: 0,
      totalTaxableSales: 0,
      totalTaxCollected: 0,
      productBreakdown: [],
    },
    sellerSales: sellerSales.map(s => ({
      sellerId: s._id,
      sellerName: s.sellerName,
      totalSales: s.totalSales,
      taxableSales: s.taxableSales,
      taxCollected: s.taxCollected,
      transactions: s.transactions,
    })),
    totalTaxCollected: platformSales[0]?.totalTaxCollected || 0,
    filingDeadline: this.getFilingDeadline(period, state),
  };
}
```

## International Marketplace Rules

Marketplace facilitator rules also apply in the EU (platform VAT rules) and other jurisdictions. Digital platforms are responsible for VAT on sales by third-party sellers.

```typescript
interface InternationalPlatformRule {
  jurisdiction: string;
  ruleType: 'marketplace_facilitator' | 'deemed_supplier' | 'platform_vat';
  threshold?: number;
  responsibility: 'platform' | 'seller';
  effectiveDate: string;
}

const INTERNATIONAL_PLATFORM_RULES: InternationalPlatformRule[] = [
  { jurisdiction: 'EU', ruleType: 'deemed_supplier', threshold: null, responsibility: 'platform', effectiveDate: '2021-07-01' },
  { jurisdiction: 'UK', ruleType: 'platform_vat', threshold: null, responsibility: 'platform', effectiveDate: '2021-01-01' },
  { jurisdiction: 'AU', ruleType: 'marketplace_facilitator', threshold: 75000, responsibility: 'platform', effectiveDate: '2018-07-01' },
  { jurisdiction: 'NZ', ruleType: 'marketplace_facilitator', threshold: 60000, responsibility: 'platform', effectiveDate: '2019-12-01' },
  { jurisdiction: 'SG', ruleType: 'marketplace_facilitator', threshold: null, responsibility: 'platform', effectiveDate: '2023-01-01' },
];
```

## Open-Source Tools

- **PostgreSQL** — Facilitator rule configuration and transaction data
- **BullMQ** — Schedule facilitator report generation
- **Metabase** (Apache 2.0) — Facilitator compliance dashboards
- **Stripe Tax** — Marketplace tax calculation

## Integration Points

Marketplace facilitator rules connect to the tax engine (calculation), the seller management system (seller identification), the invoice service (facilitator flagging), and the tax reporting system (separate filings).

## Production Considerations

- Track facilitator registration status in each state
- Monitor legislative changes for new facilitator laws
- Clearly distinguish marketplace vs direct sales in transaction metadata
- Provide sellers with tax documentation for their filings
- Test marketplace scenarios with different seller configurations

## Open-Source First Philosophy

PostgreSQL stores facilitator rules and transaction classifications. Metabase provides compliance monitoring dashboards. BullMQ manages report generation schedules. This approach avoids specialized marketplace tax software while maintaining compliance with complex facilitator regulations.
