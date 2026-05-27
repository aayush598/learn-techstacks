# Section 01: Tax Engine Architecture

## Tax Determination Logic

The tax engine determines the applicable tax rate for each transaction based on the customer's location, the product type, and any applicable exemptions. The engine supports multiple tax jurisdictions and can integrate with third-party tax providers.

```typescript
interface TaxEngine {
  type: 'internal' | 'stripe_tax' | 'taxjar' | 'vertex';
  jurisdictionResolution: JurisdictionMethod;
  rateLookup: RateLookupMethod;
  calculationMethod: 'line_item' | 'invoice_total';
  rounding: 'per_item' | 'per_transaction';
}

enum JurisdictionMethod {
  BILLING_ADDRESS = 'billing_address',
  SERVICE_LOCATION = 'service_location',
  IP_GEOLOCATION = 'ip_geolocation',
  BUSINESS_REGISTRATION = 'business_registration',
}

interface TaxRequest {
  tenantId: string;
  customerId: string;
  billingAddress: Address;
  serviceLocation?: Address;
  lineItems: TaxLineItem[];
  currency: string;
  transactionDate: string;
}

interface TaxLineItem {
  id: string;
  description: string;
  amount: number;          // In cents
  quantity: number;
  taxCode: string;         // Product tax code
  taxBehavior: 'inclusive' | 'exclusive';
  metadata?: Record<string, string>;
}

interface TaxResult {
  transactionId: string;
  jurisdictions: TaxJurisdictionResult[];
  totalTax: number;
  taxRate: number;
  breakdown: TaxBreakdownItem[];
  provider: string;
  calculatedAt: string;
}

class TaxEngineService {
  async calculateTax(request: TaxRequest): Promise<TaxResult> {
    // Determine jurisdiction
    const jurisdictions = await this.resolveJurisdictions(
      request.billingAddress,
      request.serviceLocation
    );

    const breakdown: TaxBreakdownItem[] = [];

    for (const lineItem of request.lineItems) {
      for (const jurisdiction of jurisdictions) {
        // Look up tax rate
        const rate = await this.getTaxRate(
          jurisdiction,
          lineItem.taxCode,
          request.transactionDate
        );

        // Check exemption
        const exemption = await this.checkExemption(
          request.customerId,
          jurisdiction
        );

        const applicableRate = exemption.exempt ? 0 : rate;
        const taxAmount = this.calculateTaxAmount(
          lineItem.amount,
          applicableRate,
          lineItem.taxBehavior
        );

        breakdown.push({
          lineItemId: lineItem.id,
          jurisdiction: jurisdiction,
          taxRate: applicableRate,
          taxableAmount: lineItem.amount,
          taxAmount,
          taxBehavior: lineItem.taxBehavior,
          exemption: exemption,
        });
      }
    }

    // Aggregate by jurisdiction for reporting
    const jurisdictionResults = this.aggregateByJurisdiction(breakdown);
    const totalTax = breakdown.reduce((sum, b) => sum + b.taxAmount, 0);

    return {
      transactionId: `tax_${nanoid(16)}`,
      jurisdictions: jurisdictionResults,
      totalTax,
      taxRate: request.lineItems.reduce((sum, li) => sum + li.amount, 0) > 0
        ? totalTax / request.lineItems.reduce((sum, li) => sum + li.amount, 0)
        : 0,
      breakdown,
      provider: this.engineType,
      calculatedAt: new Date().toISOString(),
    };
  }

  private async resolveJurisdictions(
    billingAddress: Address,
    serviceLocation?: Address
  ): Promise<TaxJurisdiction[]> {
    // Primary: billing address
    const primary = await this.jurisdictionDb.findByAddress(billingAddress);

    // Secondary: service location (if different)
    if (serviceLocation && !this.addressesEqual(billingAddress, serviceLocation)) {
      const secondary = await this.jurisdictionDb.findByAddress(serviceLocation);
      return [primary, secondary];
    }

    return [primary];
  }

  private async getTaxRate(
    jurisdiction: TaxJurisdiction,
    taxCode: string,
    date: string
  ): Promise<number> {
    // Try cache first
    const cacheKey = `tax_rate:${jurisdiction.id}:${taxCode}:${date}`;
    const cached = await this.redis.get(cacheKey);
    if (cached) return parseFloat(cached);

    // Look up from database
    const rateRecord = await this.taxRateDb.findCurrentRate(
      jurisdiction.id,
      taxCode,
      date
    );

    const rate = rateRecord?.rate || 0;

    // Cache for 1 hour
    await this.redis.setex(cacheKey, 3600, rate.toString());

    return rate;
  }

  private calculateTaxAmount(
    amount: number,
    rate: number,
    behavior: 'inclusive' | 'exclusive'
  ): number {
    if (behavior === 'inclusive') {
      // Tax is included in the amount
      return Math.round(amount * rate / (1 + rate));
    } else {
      // Tax is added on top
      return Math.round(amount * rate);
    }
  }
}
```

## Rate Lookup

Tax rates are stored in a database table indexed by jurisdiction, product tax code, and effective date. Rates change over time, so historical rates must be preserved for audit.

```typescript
interface TaxRateRecord {
  id: string;
  jurisdictionId: string;
  taxCode: string;
  rate: number;               // As decimal (0.0875 for 8.75%)
  effectiveFrom: string;
  effectiveTo?: string;
  rateType: 'standard' | 'reduced' | 'zero' | 'exempt';
  description: string;
}

async function lookupTaxRate(
  jurisdictionId: string,
  taxCode: string,
  transactionDate: string
): Promise<number> {
  const rate = await db.taxRates.findOne({
    jurisdictionId,
    taxCode,
    effectiveFrom: { $lte: transactionDate },
    $or: [
      { effectiveTo: { $gte: transactionDate } },
      { effectiveTo: null },
    ],
  });

  return rate?.rate || 0;
}
```

## Third-Party Tax Providers

Third-party providers like Stripe Tax, TaxJar, or Vertex can handle complex tax calculations. The architecture supports swapping between internal and external providers.

```typescript
interface TaxProvider {
  name: string;
  calculate(request: TaxRequest): Promise<TaxResult>;
  validateAddress(address: Address): Promise<AddressValidation>;
  getExemptionStatus(customerId: string, jurisdiction: TaxJurisdiction): Promise<ExemptionStatus>;
}

class StripeTaxProvider implements TaxProvider {
  name = 'stripe_tax';

  async calculate(request: TaxRequest): Promise<TaxResult> {
    const calculation = await stripe.tax.calculations.create({
      customer: request.customerId,
      currency: request.currency,
      line_items: request.lineItems.map(item => ({
        amount: item.amount,
        reference: item.id,
        quantity: item.quantity,
        tax_behavior: item.taxBehavior,
        tax_code: item.taxCode,
      })),
      customer_details: {
        address: {
          line1: request.billingAddress.line1,
          city: request.billingAddress.city,
          state: request.billingAddress.state,
          postal_code: request.billingAddress.postalCode,
          country: request.billingAddress.country,
        },
        address_source: 'billing',
      },
    });

    return this.mapStripeResult(calculation);
  }
}

class TaxJarProvider implements TaxProvider {
  name = 'taxjar';
  private client: TaxJarClient;

  async calculate(request: TaxRequest): Promise<TaxResult> {
    const response = await this.client.taxForOrder({
      from_country: 'US',
      from_zip: '94105',
      to_country: request.billingAddress.country,
      to_zip: request.billingAddress.postalCode,
      to_state: request.billingAddress.state,
      to_city: request.billingAddress.city,
      amount: request.lineItems.reduce((s, i) => s + i.amount, 0) / 100,
      shipping: 0,
      line_items: request.lineItems.map(item => ({
        id: item.id,
        quantity: item.quantity,
        unit_price: item.amount / item.quantity / 100,
        product_tax_code: item.taxCode,
      })),
    });

    return this.mapTaxJarResult(response);
  }
}
```

## Open-Source Tools

- **PostgreSQL** — Tax rate and jurisdiction database
- **Redis** — Tax rate caching for performance
- **Stripe Tax** (Proprietary, free tier) — Third-party tax provider
- **TaxJar** (Proprietary) — Alternative US-focused provider
- **Vertex** (Proprietary) — Enterprise tax provider

## Integration Points

The tax engine integrates with the invoice generation service (Chapter 4), the Stripe billing integration (Chapter 3 Section 6), the customer management service (billing address), and the tax exemption system (Section 4).

## Production Considerations

- Cache tax rates aggressively but respect rate changes
- Snapshot tax rate at time of transaction for audit
- Handle multi-jurisdiction transactions (US state + county + city)
- Test tax calculation for all supported jurisdictions
- Monitor tax calculation accuracy monthly

## Open-Source First Philosophy

PostgreSQL serves as the tax rate database, Redis provides caching, and the tax engine can use Stripe Tax's free tier or open-source rate tables for basic calculations. This approach avoids expensive enterprise tax engines (Avalara, Vertex) for early-stage operations while maintaining compliance.
