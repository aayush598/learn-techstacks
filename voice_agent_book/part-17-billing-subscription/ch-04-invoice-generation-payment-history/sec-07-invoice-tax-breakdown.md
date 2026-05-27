# Section 07: Invoice Tax Breakdown

## Per-Line-Item Tax

Each line item on an invoice can have different tax treatments. Some items may be taxable at the standard rate, others at a reduced rate, and some may be exempt. Per-line-item tax breakdown provides transparency and helps customers understand their tax obligations.

```typescript
interface LineItemTaxDetail {
  lineItemId: string;
  description: string;
  taxJurisdictions: TaxJurisdictionDetail[];
  totalTax: number;
  taxInclusive: boolean;
}

interface TaxJurisdictionDetail {
  jurisdiction: string;       // 'US-CA', 'EU-DE', 'IN'
  taxType: string;            // 'sales_tax', 'vat', 'gst'
  taxRate: number;
  taxableAmount: number;
  taxAmount: number;
  exemptionInfo?: {
    exempt: boolean;
    exemptionType?: string;
    certificateReference?: string;
  };
}

class LineItemTaxCalculator {
  async calculateLineItemTax(
    item: InvoiceLineItem,
    customer: TaxCustomer,
    billingPeriod: { start: string; end: string }
  ): Promise<LineItemTaxDetail> {
    const jurisdictions = await this.taxEngine.determineJurisdictions(
      customer.billingAddress,
      customer.serviceLocation
    );

    const taxDetails: TaxJurisdictionDetail[] = [];

    for (const jurisdiction of jurisdictions) {
      const rate = await this.taxEngine.getTaxRate(
        jurisdiction,
        item.type,
        customer.exemptionStatus
      );

      const taxableAmount = item.amount;

      taxDetails.push({
        jurisdiction: `${jurisdiction.country}${jurisdiction.state ? '-' + jurisdiction.state : ''}`,
        taxType: jurisdiction.taxType,
        taxRate: rate,
        taxableAmount,
        taxAmount: Math.round(taxableAmount * rate),
        exemptionInfo: customer.exemptionStatus
          ? {
              exempt: rate === 0,
              exemptionType: customer.exemptionType,
              certificateReference: customer.exemptionCertificateRef,
            }
          : undefined,
      });
    }

    const totalTax = taxDetails.reduce((sum, j) => sum + j.taxAmount, 0);

    return {
      lineItemId: item.id,
      description: item.description,
      taxJurisdictions: taxDetails,
      totalTax,
      taxInclusive: false, // We use exclusive tax display
    };
  }
}
```

## Jurisdiction Breakdown

Invoices show a breakdown of tax by jurisdiction. This is especially important for customers who operate in multiple tax regions and need to understand their tax obligations for each.

```
Invoice Tax Breakdown Example:
┌─────────────────────────────────────────────────────────────────┐
│ Tax Summary                                                      │
│                                                                  │
│ Line Item              │ Jurisdiction  │ Rate   │ Tax Amount   │
├────────────────────────┼───────────────┼────────┼──────────────┤
│ Growth Plan - Monthly  │ US-CA (CA)    │ 8.75%  │ $17.41       │
│                        │ US-NY (NY)    │ 4.00%  │ $7.96        │
│ Overage Minutes (500)  │ US-CA (CA)    │ 8.75%  │ $1.09        │
│                        │ US-NY (NY)    │ 4.00%  │ $0.50        │
│ Addon: Voice Clone (2) │ US-CA (CA)    │ 8.75%  │ $8.75        │
│                        │ US-NY (NY)    │ 4.00%  │ $4.00        │
├────────────────────────┼───────────────┼────────┼──────────────┤
│ Total Tax              │               │        │ $39.71       │
└─────────────────────────────────────────────────────────────────┘
```

## Tax Rate Display

Tax rates are displayed as percentages with the applicable jurisdiction. The display format follows local conventions: "VAT 20%" (EU), "Sales Tax 8.75%" (US), "GST 18%" (India), "HST 13%" (Canada).

```typescript
function formatTaxRate(rate: number, taxType: string, locale: string): string {
  const percentage = (rate * 100).toFixed(
    rate % 1 === 0 ? 0 : 2
  );

  switch (taxType) {
    case 'vat':
      return `VAT ${percentage}%`;
    case 'sales_tax':
      return `Sales Tax ${percentage}%`;
    case 'gst':
      return `GST ${percentage}%`;
    case 'hst':
      return `HST ${percentage}%`;
    case 'pst':
      return `PST ${percentage}%`;
    default:
      return `Tax ${percentage}%`;
  }
}
```

## Exempt Status Indicators

When a customer is tax-exempt, their invoices show the exemption information prominently. Exempt customers include non-profits, government entities, and resellers with valid exemption certificates.

```typescript
interface ExemptionIndicator {
  exempt: boolean;
  type?: 'nonprofit' | 'government' | 'reseller' | 'other';
  certificateId?: string;
  jurisdiction?: string;
  expiryDate?: string;
}

class TaxExemptionDisplay {
  generateExemptionSection(customer: TaxCustomer): any {
    if (!customer.exemptionStatus?.exempt) {
      return null;
    }

    return {
      text: 'Tax Exemption',
      bold: true,
      fontSize: 12,
      color: '#2e7d32',
      margin: [0, 10, 0, 5],
    };

    return {
      stack: [
        {
          text: [
            { text: 'This invoice is tax-exempt. ', bold: false },
            { text: `Exemption Type: ${customer.exemptionStatus.type}`, bold: false },
          ],
          fontSize: 10,
          color: '#555',
        },
        customer.exemptionStatus.certificateId
          ? { text: `Certificate: ${customer.exemptionStatus.certificateId}`, fontSize: 10, color: '#555' }
          : null,
      ].filter(Boolean),
    };
  }
}
```

## Tax Inclusive vs Exclusive Display

Different regions expect different tax display: EU businesses typically display prices tax-inclusive, while US businesses display tax-exclusive. The invoice must respect regional conventions.

```typescript
enum TaxDisplayMode {
  INCLUSIVE = 'inclusive',  // Price includes tax (display: $120 including $20 tax)
  EXCLUSIVE = 'exclusive',  // Price excludes tax (display: $100 + $20 tax = $120)
}

function renderTaxTotal(
  subtotal: number,
  taxTotal: number,
  mode: TaxDisplayMode,
  currency: string
): string {
  switch (mode) {
    case TaxDisplayMode.INCLUSIVE:
      return `Total (incl. tax): ${formatCurrency(subtotal / 100)}`;
    case TaxDisplayMode.EXCLUSIVE:
      return `Subtotal: ${formatCurrency(subtotal / 100)}\nTax: ${formatCurrency(taxTotal / 100)}\nTotal: ${formatCurrency((subtotal + taxTotal) / 100)}`;
  }
}
```

## Open-Source Tools

- **Stripe Tax** — Automated per-line-item tax calculation
- **PostgreSQL** — Tax rate snapshots and jurisdiction data
- **pdfmake** (MIT) — Tax breakdown rendering in PDF invoices

## Integration Points

Tax breakdown integrates with the tax calculation engine (Chapter 8), the invoice generation service (Section 2), the PDF generation service (Section 3), and the customer portal.

## Production Considerations

- Snapshot tax rates at time of invoice generation (rates change)
- Validate tax breakdown against Stripe Tax calculation
- Support tax rounding rules per jurisdiction
- Test tax display for all supported regions
- Handle tax rate changes mid-billing-period

## Open-Source First Philosophy

Stripe Tax handles the complex tax calculation, while PostgreSQL stores snapshotted tax rates for audit. pdfmake renders the breakdown on invoices. This open-source-friendly stack avoids proprietary tax display engines while providing compliant, transparent tax information to customers.
