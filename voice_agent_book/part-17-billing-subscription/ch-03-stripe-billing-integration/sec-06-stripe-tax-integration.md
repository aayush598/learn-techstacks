# Section 06: Stripe Tax Integration

## Automatic Tax Calculation

Stripe Tax automatically calculates sales tax, VAT, and GST based on the customer's location and the product/service being sold. It eliminates the need for a separate tax engine by providing built-in tax determination.

```typescript
class StripeTaxService {
  async enableTaxForCustomer(tenantId: string): Promise<void> {
    const stripeCustomerId = await this.getStripeCustomerId(tenantId);
    const tenant = await this.tenantService.getTenant(tenantId);

    // Set customer tax details
    await stripe.customers.update(stripeCustomerId, {
      tax: {
        ip_address: tenant.signupIp,
        location: {
          country: tenant.billingAddress?.country,
          state: tenant.billingAddress?.state,
          postal_code: tenant.billingAddress?.postalCode,
        },
      },
      tax_id_data: tenant.taxIds?.map(taxId => ({
        type: taxId.type,  // 'eu_vat', 'us_ein', etc.
        value: taxId.value,
      })),
    });
  }

  async createTaxSettingsForProduct(
    stripeProductId: string,
    taxCode: string
  ): Promise<void> {
    await stripe.products.update(stripeProductId, {
      tax_code: taxCode,
    });
  }

  async calculateTax(
    customerId: string,
    amount: number,
    currency: string,
    items: Array<{ product: string; amount: number; quantity: number }>
  ): Promise<Stripe.TaxCalculation> {
    return await stripe.tax.calculations.create({
      customer: customerId,
      currency: currency,
      line_items: items.map(item => ({
        amount: item.amount,
        reference: item.product,
        quantity: item.quantity,
        tax_behavior: 'exclusive',
      })),
    });
  }
}
```

## Tax Code Mapping

Stripe uses tax codes to determine the applicable tax rate for each product. Voice agent services typically fall under "digital goods" or "saas" tax codes.

```typescript
const TAX_CODE_MAPPING = {
  // Stripe tax codes for SaaS products
  services: 'txcd_10000000',       // General services
  saas: 'txcd_10101000',           // Software as a Service
  digital_goods: 'txcd_20030000',  // Digital goods
  telecom: 'txcd_30010000',        // Telecommunications services
  support: 'txcd_10102000',        // Technical support services
};
```

## Jurisdiction Handling

Tax rates vary by jurisdiction — state, county, city, and even special districts. Stripe Tax handles jurisdiction identification automatically, but we must provide accurate customer location data.

```typescript
interface TaxJurisdiction {
  country: string;
  state?: string;
  county?: string;
  city?: string;
  special_district?: string;
  tax_type: 'vat' | 'sales_tax' | 'gst' | 'digital_service_tax';
}

interface CalculatedTax {
  jurisdiction: TaxJurisdiction;
  rate: number;
  amount: number;
  tax_type: string;
  exemption_status: 'none' | 'partial' | 'full';
  breakdown?: TaxBreakdownLine[];
}

class JurisdictionResolver {
  async resolveJurisdiction(
    customerId: string,
    taxCalculation: Stripe.TaxCalculation
  ): Promise<TaxJurisdiction[]> {
    const jurisdictions: TaxJurisdiction[] = [];

    for (const lineItem of taxCalculation.line_items) {
      for (const taxBreakdown of lineItem.tax_breakdown) {
        jurisdictions.push({
          country: taxBreakdown.jurisdiction.country,
          state: taxBreakdown.jurisdiction.state,
          county: taxBreakdown.jurisdiction.county,
          city: taxBreakdown.jurisdiction.city,
          special_district: taxBreakdown.jurisdiction.special_district,
          tax_type: 'sales_tax',
        });
      }
    }

    return jurisdictions;
  }
}
```

## Tax Reporting

Stripe Tax provides transaction-level tax data for reporting. The data includes the tax rate applied, jurisdiction details, and exemption information. This data feeds into tax reports for filing.

```typescript
interface TaxReportData {
  period: string;
  jurisdiction: string;
  taxableSales: number;
  taxCollected: number;
  taxRate: number;
  transactionCount: number;
  exemptions: {
    count: number;
    amount: number;
  };
}

class TaxReportService {
  async generateTaxReport(
    periodStart: string,
    periodEnd: string,
    jurisdiction?: string
  ): Promise<TaxReportData[]> {
    // Query Stripe Tax for transaction data
    const transactions = await stripe.tax.transactions.list({
      period: {
        start: Math.floor(new Date(periodStart).getTime() / 1000),
        end: Math.floor(new Date(periodEnd).getTime() / 1000),
      },
      limit: 100,
    });

    // Aggregate by jurisdiction
    const byJurisdiction = new Map<string, TaxReportData>();

    for (const tx of transactions.data) {
      const jKey = `${tx.jurisdiction.country}-${tx.jurisdiction.state || 'none'}`;

      const existing = byJurisdiction.get(jKey) || {
        period: periodStart,
        jurisdiction: jKey,
        taxableSales: 0,
        taxCollected: 0,
        taxRate: tx.tax_rate || 0,
        transactionCount: 0,
        exemptions: { count: 0, amount: 0 },
      };

      existing.taxableSales += tx.taxable_amount;
      existing.taxCollected += tx.tax_amount;
      existing.transactionCount++;

      if (tx.exemption_status === 'exempt') {
        existing.exemptions.count++;
        existing.exemptions.amount += tx.amount;
      }

      byJurisdiction.set(jKey, existing);
    }

    return Array.from(byJurisdiction.values());
  }
}
```

## Open-Source Tools

- **Stripe Tax** (Proprietary, free tier up to 100K transactions) — Tax calculation
- **PostgreSQL** — Tax transaction audit storage
- **BullMQ** — Schedule tax report generation
- **Metabase** (Apache 2.0) — Tax dashboards for finance team

## Integration Points

Stripe Tax integrates with the invoice service (Chapter 4), the customer management service (Section 1), the subscription service (Section 2), and the tax exemption system (Chapter 8 Section 4).

## Production Considerations

- Verify tax rates are correct for each jurisdiction during testing
- Monitor Stripe Tax accuracy with periodic manual audits
- Set up tax report generation schedules aligned with filing deadlines
- Handle Stripe Tax errors gracefully (fall back to manual calculation)
- Test tax scenarios for all supported jurisdictions

## Open-Source First Philosophy

Stripe Tax provides automated tax calculation at a fraction of the cost of dedicated tax engines like Avalara or TaxJar. For early-stage SaaS, the free tier covers up to 100,000 transactions. Combined with Metabase for reporting and PostgreSQL for audit storage, this stack handles global tax compliance without expensive specialized software.
