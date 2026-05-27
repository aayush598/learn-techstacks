# Section 02: EU VAT Compliance

## VAT Registration Thresholds

Each EU member state has a VAT registration threshold for cross-border digital services. Under the EU's One-Stop Shop (OSS) scheme, businesses can register in a single member state and report VAT for all EU sales.

```typescript
interface VATThreshold {
  countryCode: string;
  countryName: string;
  thresholdAmount: number;    // Annual revenue threshold in EUR
  currency: string;
  registrationRequired: boolean;
  ossApplicable: boolean;
}

const EU_VAT_THRESHOLDS: Record<string, VATThreshold> = {
  DE: { countryCode: 'DE', countryName: 'Germany', thresholdAmount: 0, currency: 'EUR', registrationRequired: true, ossApplicable: true },
  FR: { countryCode: 'FR', countryName: 'France', thresholdAmount: 0, currency: 'EUR', registrationRequired: true, ossApplicable: true },
  IT: { countryCode: 'IT', countryName: 'Italy', thresholdAmount: 0, currency: 'EUR', registrationRequired: true, ossApplicable: true },
  ES: { countryCode: 'ES', countryName: 'Spain', thresholdAmount: 0, currency: 'EUR', registrationRequired: true, ossApplicable: true },
  NL: { countryCode: 'NL', countryName: 'Netherlands', thresholdAmount: 0, currency: 'EUR', registrationRequired: true, ossApplicable: true },
  IE: { countryCode: 'IE', countryName: 'Ireland', thresholdAmount: 0, currency: 'EUR', registrationRequired: true, ossApplicable: true },
  AT: { countryCode: 'AT', countryName: 'Austria', thresholdAmount: 0, currency: 'EUR', registrationRequired: true, ossApplicable: true },
  BE: { countryCode: 'BE', countryName: 'Belgium', thresholdAmount: 0, currency: 'EUR', registrationRequired: true, ossApplicable: true },
  // ... all 27 EU member states
};

class EUVATService {
  async determineVATResponsibility(
    customerCountry: string,
    customerVatId?: string,
    annualRevenue?: number
  ): Promise<VATResponsibility> {
    // B2B: Reverse charge if customer has valid VAT ID
    if (customerVatId) {
      const isValid = await this.validateVIES(customerVatId);
      if (isValid) {
        return {
          applies: true,
          rate: 0,
          mechanism: 'reverse_charge',
          notes: 'B2B reverse charge — customer accounts for VAT',
        };
      }
    }

    // B2C: Charge VAT at customer's country rate
    const threshold = EU_VAT_THRESHOLDS[customerCountry];
    if (!threshold) {
      return { applies: false, mechanism: 'no_vat', notes: 'Non-EU customer' };
    }

    return {
      applies: true,
      rate: await this.getVATRate(customerCountry),
      mechanism: 'oss',
      jurisdiction: customerCountry,
      notes: `B2C — VAT at ${customerCountry} rate via OSS`,
    };
  }

  async validateVIES(vatId: string): Promise<boolean> {
    try {
      // VIES (VAT Information Exchange System) validation
      const response = await fetch(
        `https://ec.europa.eu/taxation_customs/vies/rest-api/check-vat-number`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ vatNumber: vatId }),
        }
      );

      const data = await response.json();
      return data.valid;
    } catch (error) {
      logger.error('VIES validation failed', { vatId, error });
      // Fall back to format validation
      return this.validateVATFormat(vatId);
    }
  }
}
```

## MOSS/IOSS

The Union One-Stop Shop (OSS) and Import One-Stop Shop (IOSS) simplify VAT compliance for cross-border digital services. MOSS (Mini One-Stop Shop) was the predecessor.

```typescript
interface OSSRegistration {
  countryCode: string;       // Country of registration
  registrationNumber: string;
  scheme: 'union_oss' | 'import_oss' | 'non_union_oss';
  effectiveDate: string;
  status: 'active' | 'suspended' | 'cancelled';
}

class OSSService {
  async calculateOSSVAT(
    salesByCountry: Map<string, number>
  ): Promise<OSSReturn> {
    const returns: OSSLineItem[] = [];

    for (const [country, netSales] of salesByCountry) {
      const vatRate = await this.getVATRate(country);
      const vatAmount = Math.round(netSales * vatRate);

      returns.push({
        country,
        netSales,
        vatRate: vatRate * 100, // Percentage for display
        vatAmount,
        currency: 'EUR',
      });
    }

    return {
      period: this.getCurrentQuarter(),
      totalNetSales: Array.from(salesByCountry.values()).reduce((a, b) => a + b, 0),
      totalVAT: returns.reduce((a, b) => a + b.vatAmount, 0),
      lines: returns,
      currency: 'EUR',
    };
  }

  private getCurrentQuarter(): string {
    const now = new Date();
    const quarter = Math.floor(now.getMonth() / 3) + 1;
    return `Q${quarter} ${now.getFullYear()}`;
  }
}
```

## Reverse Charge

The reverse charge mechanism moves VAT accounting from the supplier to the customer (B2B). The supplier issues an invoice without VAT, and the customer accounts for the VAT themselves.

```typescript
function applyReverseCharge(
  invoice: Invoice,
  customerVatId: string
): Invoice {
  // Check if B2B reverse charge applies
  if (!customerVatId) return invoice;

  // Remove VAT from all line items
  invoice.lineItems = invoice.lineItems.map(item => ({
    ...item,
    taxAmount: 0,
    taxRate: 0,
    metadata: {
      ...item.metadata,
      taxTreatment: 'reverse_charge',
      customerVatId,
    },
  }));

  invoice.taxTotal = 0;
  invoice.total = invoice.subtotal;

  invoice.metadata.taxTreatment = 'reverse_charge';
  invoice.metadata.customerVatId = customerVatId;

  return invoice;
}
```

## VAT Rate Lookup Per Member State

Each EU member state sets its own VAT rates. Standard rates range from 17% (Luxembourg) to 27% (Hungary). Reduced rates apply to specific goods and services.

```typescript
const EU_VAT_RATES: Record<string, { standard: number; reduced: number; superReduced?: number }> = {
  AT: { standard: 0.20, reduced: 0.10 },
  BE: { standard: 0.21, reduced: 0.12, superReduced: 0.06 },
  BG: { standard: 0.20, reduced: 0.09 },
  DE: { standard: 0.19, reduced: 0.07 },
  DK: { standard: 0.25, reduced: 0.0 },
  EE: { standard: 0.22, reduced: 0.09 },
  ES: { standard: 0.21, reduced: 0.10, superReduced: 0.04 },
  FI: { standard: 0.25, reduced: 0.14, superReduced: 0.10 },
  FR: { standard: 0.20, reduced: 0.10, superReduced: 0.055 },
  // ... all member states
};
```

## Open-Source Tools

- **PostgreSQL** — VAT rate tables and OSS data
- **BullMQ** — Schedule quarterly OSS return generation
- **Nodemailer** (MIT) — VAT documentation delivery
- **Stripe Tax** — Automatic EU VAT calculation

## Integration Points

EU VAT compliance integrates with the tax engine (rate lookup), the invoice system (reverse charge handling), the customer management system (VAT ID collection), and the tax reporting system (OSS returns).

## Production Considerations

- Validate VAT IDs with VIES API before applying reverse charge
- Maintain VAT rate database with automatic updates
- Track OSS thresholds across all EU member states
- Keep historical VAT rates for audit compliance
- File quarterly OSS returns on time to avoid penalties

## Open-Source First Philosophy

VIES API validation is free through the EU Commission. PostgreSQL stores VAT rate tables. Stripe Tax's free tier handles EU VAT for most transaction volumes. This approach avoids expensive EU VAT compliance software while maintaining regulatory compliance.
