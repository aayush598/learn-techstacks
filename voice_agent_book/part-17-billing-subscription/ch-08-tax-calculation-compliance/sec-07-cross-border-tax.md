# Section 07: Cross-Border Tax

## Digital Services Taxes

Several countries have enacted Digital Services Taxes (DST) that apply to revenue from digital services provided to users in that jurisdiction. DST rates typically range from 1.5% to 7.5%.

```typescript
interface DigitalServicesTax {
  country: string;
  countryCode: string;
  rate: number;
  threshold: number;           // Revenue threshold in local currency
  applicableServices: string[];
  effectiveDate: string;
  filingFrequency: 'quarterly' | 'annual';
}

const DIGITAL_SERVICES_TAXES: DigitalServicesTax[] = [
  { country: 'France', countryCode: 'FR', rate: 0.03, threshold: 25000000, applicableServices: ['digital_platform', 'advertising', 'data_transmission'], effectiveDate: '2019-01-01', filingFrequency: 'annual' },
  { country: 'Italy', countryCode: 'IT', rate: 0.03, threshold: 7500000, applicableServices: ['digital_services'], effectiveDate: '2020-01-01', filingFrequency: 'annual' },
  { country: 'Spain', countryCode: 'ES', rate: 0.03, threshold: 3000000, applicableServices: ['digital_services'], effectiveDate: '2021-01-16', filingFrequency: 'quarterly' },
  { country: 'United Kingdom', countryCode: 'UK', rate: 0.02, threshold: 25000000, applicableServices: ['social_media', 'search_engine', 'online_marketplace'], effectiveDate: '2020-04-01', filingFrequency: 'annual' },
  { country: 'Austria', countryCode: 'AT', rate: 0.05, threshold: 25000000, applicableServices: ['online_advertising'], effectiveDate: '2020-01-01', filingFrequency: 'annual' },
  { country: 'Turkey', countryCode: 'TR', rate: 0.075, threshold: 20000000, applicableServices: ['digital_services'], effectiveDate: '2020-03-01', filingFrequency: 'monthly' },
];

class DigitalServicesTaxService {
  async calculateDST(
    countryCode: string,
    annualRevenue: number,
    revenueByService: Record<string, number>
  ): Promise<DSTResult | null> {
    const dst = DIGITAL_SERVICES_TAXES.find(t => t.countryCode === countryCode);
    if (!dst) return null;

    if (annualRevenue < dst.threshold) return null;

    // Calculate DST on applicable services
    let dstRevenue = 0;
    for (const [service, revenue] of Object.entries(revenueByService)) {
      if (dst.applicableServices.includes(service)) {
        dstRevenue += revenue;
      }
    }

    return {
      country: dst.country,
      rate: dst.rate,
      applicableRevenue: dstRevenue,
      taxAmount: Math.round(dstRevenue * dst.rate),
      threshold: dst.threshold,
      filingFrequency: dst.filingFrequency,
    };
  }
}
```

## Withholding Tax

Withholding tax applies to cross-border payments for services. The rate depends on the country and any applicable double taxation treaty.

```typescript
interface WithholdingTaxRule {
  sourceCountry: string;
  recipientCountry: string;
  rate: number;                // Withholding tax rate
  treatyRate?: number;         // Reduced rate under tax treaty
  conditions: string[];
  formRequired: string;        // e.g., 'W-8BEN', 'W-8BEN-E'
}

async function calculateWithholdingTax(
  payment: CrossBorderPayment
): Promise<WithholdingTaxResult> {
  // Check if tax treaty applies
  const treaty = await getTaxTreaty(payment.sourceCountry, payment.recipientCountry);

  let rate: number;
  let formRequired: string | null;

  if (treaty && payment.hasValidForm) {
    rate = treaty.rate;
    formRequired = null; // Form already on file
  } else {
    rate = getDefaultWithholdingRate(payment.sourceCountry);
    formRequired = getRequiredForm(payment.sourceCountry, payment.recipientCountry);
  }

  const withholdingAmount = Math.round(payment.grossAmount * rate);

  return {
    grossAmount: payment.grossAmount,
    withholdingRate: rate,
    withholdingAmount,
    netAmount: payment.grossAmount - withholdingAmount,
    treatyApplied: !!treaty && payment.hasValidForm,
    formRequired,
    remittanceInstructions: {
      authority: getTaxAuthority(payment.sourceCountry),
      deadline: getFilingDeadline(payment.sourceCountry),
      formType: formRequired,
    },
  };
}
```

## Double Taxation Treaties

Double taxation treaties prevent the same income from being taxed in two countries. They typically reduce or eliminate withholding tax on cross-border payments.

```typescript
interface DoubleTaxationTreaty {
  country1: string;
  country2: string;
  article: string;
  withholdingRate: {
    dividends: number;
    interest: number;
    royalties: number;
    services: number;
  };
  conditions: TreatyCondition[];
  effectiveDate: string;
}

const US_UK_TREATY: DoubleTaxationTreaty = {
  country1: 'US',
  country2: 'UK',
  article: 'Article 12 — Royalties',
  withholdingRate: {
    dividends: 0.15,
    interest: 0,
    royalties: 0,
    services: 0,
  },
  conditions: [
    { description: 'Beneficial ownership required', type: 'ownership' },
    { description: 'No permanent establishment in source country', type: 'pe' },
    { description: 'Valid W-8BEN-E form on file', type: 'documentation' },
  ],
  effectiveDate: '2002-01-01',
};
```

## Cross-Border Invoicing

Cross-border invoices must include specific information for international transactions: tax IDs, treaty claims, and jurisdiction-specific fields.

```typescript
interface CrossBorderInvoiceFields {
  invoiceNumber: string;
  supplierInfo: {
    name: string;
    address: string;
    taxId: string;             // VAT number, EIN, etc.
    registrationNumber?: string;
  };
  customerInfo: {
    name: string;
    address: string;
    taxId?: string;
    isBusiness: boolean;
  };
  taxTreatment: {
    domesticTax: TaxDetail;
    foreignTax: CrossBorderTaxDetail[];
    treatyClaim?: TreatyClaim;
  };
  additionalFields: {
    placeOfSupply: string;
    serviceType: string;
    reverseCharge: boolean;
    selfBilling: boolean;
  };
}

interface CrossBorderTaxDetail {
  jurisdiction: string;
  taxType: 'vat' | 'withholding' | 'dst' | 'gst';
  rate: number;
  amount: number;
  exemptionReason?: string;
}
```

## Open-Source Tools

- **PostgreSQL** — Treaty and DST rate database
- **BullMQ** — Schedule cross-border tax filing
- **Stripe Tax** — International tax determination
- **Metabase** (Apache 2.0) — Cross-border tax dashboards

## Integration Points

Cross-border tax handles integrates with the tax engine (rate determination), the invoice system (additional fields), the customer management system (tax ID collection), and the payment system (withholding).

## Production Considerations

- Validate tax ID formats for each country
- Track treaty eligibility based on customer documentation
- Monitor DST thresholds per country
- Maintain W-8/W-9 form collection workflow
- Stay updated on digital services tax developments

## Open-Source First Philosophy

PostgreSQL stores treaty rates and DST configurations. BullMQ manages compliance deadlines. Metabase provides cross-border tax dashboards. This approach avoids specialized international tax software while maintaining compliance with complex cross-border tax regulations.
