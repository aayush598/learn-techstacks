# Section 03: US Sales Tax Automation

## Economic Nexus

US sales tax is determined by economic nexus — a business must collect sales tax in states where it has significant economic activity. Nexus thresholds vary by state (typically $100K-$500K in sales or 200 transactions).

```typescript
interface NexusThreshold {
  state: string;
  stateName: string;
  salesThreshold: number;       // Annual sales in USD
  transactionThreshold: number;  // Number of transactions
  effectiveDate: string;
}

const NEXUS_THRESHOLDS: NexusThreshold[] = [
  { state: 'CA', stateName: 'California', salesThreshold: 500000, transactionThreshold: 0, effectiveDate: '2019-04-01' },
  { state: 'TX', stateName: 'Texas', salesThreshold: 500000, transactionThreshold: 0, effectiveDate: '2019-10-01' },
  { state: 'NY', stateName: 'New York', salesThreshold: 500000, transactionThreshold: 100, effectiveDate: '2019-06-01' },
  { state: 'FL', stateName: 'Florida', salesThreshold: 100000, transactionThreshold: 0, effectiveDate: '2021-07-01' },
  { state: 'IL', stateName: 'Illinois', salesThreshold: 100000, transactionThreshold: 200, effectiveDate: '2020-07-01' },
  { state: 'PA', stateName: 'Pennsylvania', salesThreshold: 100000, transactionThreshold: 0, effectiveDate: '2019-07-01' },
  // ... all 45+ states with sales tax
];

class NexusTracker {
  async checkNexus(
    stateCode: string,
    annualSales: number,
    annualTransactions: number
  ): Promise<NexusStatus> {
    const threshold = NEXUS_THRESHOLDS.find(t => t.state === stateCode);
    if (!threshold) return { nexus: false, reason: 'No sales tax in this state' };

    const hasNexus = annualSales >= threshold.salesThreshold
      || (threshold.transactionThreshold > 0 && annualTransactions >= threshold.transactionThreshold);

    return {
      nexus: hasNexus,
      threshold,
      currentSales: annualSales,
      currentTransactions: annualTransactions,
      reason: hasNexus
        ? `Economic nexus established in ${stateCode}`
        : `Below nexus threshold in ${stateCode}`,
    };
  }

  async trackNexusByState(): Promise<Record<string, NexusStatus>> {
    const totalsByState = await this.db.invoices.aggregate([
      {
        $group: {
          _id: '$billingState',
          totalSales: { $sum: '$total' },
          totalTransactions: { $sum: 1 },
        },
      },
    ]).toArray();

    const results: Record<string, NexusStatus> = {};

    for (const state of totalsByState) {
      results[state._id] = await this.checkNexus(
        state._id,
        state.totalSales,
        state.totalTransactions
      );
    }

    return results;
  }
}
```

## State-by-State Rates

US sales tax rates vary by state, county, city, and special district. The combined rate is the sum of all applicable rates.

```typescript
interface SalesTaxRate {
  jurisdiction: string;       // e.g., 'US-CA-075' (California, San Francisco)
  stateRate: number;
  countyRate: number;
  cityRate: number;
  specialDistrictRate: number;
  combinedRate: number;       // Sum of all rates
  effectiveFrom: string;
  effectiveTo?: string;
  taxType: 'sales_tax' | 'use_tax';
}

async function getCombinedRate(
  state: string,
  zipCode: string,
  address: string
): Promise<SalesTaxRate> {
  // Use Stripe Tax or internal rate database
  const rate = await stripe.tax.calculations.create({
    currency: 'usd',
    line_items: [{ amount: 10000, reference: 'test', tax_behavior: 'exclusive' }],
    customer_details: {
      address: {
        line1: address,
        city: '',
        state,
        postal_code: zipCode,
        country: 'US',
      },
      address_source: 'billing',
    },
  });

  const breakdown = rate.line_items[0]?.tax_breakdown || [];

  return {
    jurisdiction: `US-${state}`,
    stateRate: breakdown.find(b => b.jurisdiction.level === 'state')?.tax_rate || 0,
    countyRate: breakdown.find(b => b.jurisdiction.level === 'county')?.tax_rate || 0,
    cityRate: breakdown.find(b => b.jurisdiction.level === 'city')?.tax_rate || 0,
    specialDistrictRate: breakdown.find(b => b.jurisdiction.level === 'special_district')?.tax_rate || 0,
    combinedRate: breakdown.reduce((sum, b) => sum + b.tax_rate, 0),
    effectiveFrom: new Date().toISOString(),
    taxType: 'sales_tax',
  };
}
```

## Product Taxability

Different products have different taxability rules. Voice agent services may be classified as "digital goods" (taxable) or "software as a service" (taxable in most states).

```typescript
interface ProductTaxability {
  taxCode: string;              // Stripe tax code
  description: string;
  isTaxable: Record<string, boolean>;  // Per-state taxability
  taxRateType: 'standard' | 'reduced' | 'exempt';
}

const PRODUCT_TAXABILITY: Record<string, ProductTaxability> = {
  voice_calls: {
    taxCode: 'txcd_20030000',      // Digital goods
    description: 'Voice call minutes',
    isTaxable: {
      'CA': true, 'TX': true, 'NY': true, 'FL': false, // Florida exempts SaaS
      // ... all states
    },
    taxRateType: 'standard',
  },
  transcription: {
    taxCode: 'txcd_10101000',      // SaaS
    description: 'Transcription services',
    isTaxable: {
      'CA': true, 'TX': true, 'NY': true, 'FL': false,
    },
    taxRateType: 'standard',
  },
  tts: {
    taxCode: 'txcd_20030000',
    description: 'Text-to-speech processing',
    isTaxable: {
      'CA': true, 'TX': true, 'NY': true, 'FL': false,
    },
    taxRateType: 'standard',
  },
};
```

## Origin vs Destination Sourcing

Sourcing rules determine which jurisdiction's tax rate applies. Origin sourcing applies the seller's location rate. Destination sourcing applies the buyer's location rate.

```typescript
enum SourcingRule {
  ORIGIN = 'origin',         // Seller's location
  DESTINATION = 'destination', // Buyer's location
  MIXED = 'mixed',           // Depends on product type
}

const STATE_SOURCING_RULES: Record<string, SourcingRule> = {
  'CA': SourcingRule.DESTINATION,
  'TX': SourcingRule.DESTINATION,
  'NY': SourcingRule.DESTINATION,
  'FL': SourcingRule.DESTINATION,
  'IL': SourcingRule.DESTINATION,
  'PA': SourcingRule.DESTINATION,
  'OH': SourcingRule.DESTINATION,
  'MI': SourcingRule.DESTINATION,
  'NC': SourcingRule.DESTINATION,
  'GA': SourcingRule.DESTINATION,
  'TN': SourcingRule.ORIGIN,    // Origin sourcing
  'VA': SourcingRule.DESTINATION,
  'WA': SourcingRule.DESTINATION,
  'AZ': SourcingRule.DESTINATION,
  'MA': SourcingRule.DESTINATION,
  'MN': SourcingRule.DESTINATION,
  'CO': SourcingRule.DESTINATION,
  'MD': SourcingRule.DESTINATION,
  'MO': SourcingRule.ORIGIN,    // Origin sourcing
};
```

## Open-Source Tools

- **Stripe Tax** (Proprietary, free tier) — Automated US sales tax
- **PostgreSQL** — Nexus tracking and rate data
- **BullMQ** — Schedule nexus threshold evaluation
- **Metabase** (Apache 2.0) — Sales tax compliance dashboards

## Integration Points

US sales tax automation integrates with the tax engine (rate lookup), the invoice system (tax calculation), the customer management system (billing address collection), and the nexus tracking system.

## Production Considerations

- Monitor nexus thresholds monthly
- Register for sales tax permits when thresholds are met
- File returns based on each state's schedule (monthly/quarterly/annual)
- Maintain exemption certificate records
- Use Stripe Tax for accurate rate lookups

## Open-Source First Philosophy

Stripe Tax's free tier handles US sales tax calculation for most startups. PostgreSQL tracks nexus thresholds and registration status. Metabase provides compliance dashboards. This approach avoids dedicated US sales tax software while maintaining compliance across all states.
