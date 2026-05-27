# Section 05: Overage Invoice Items

## Overage Line Items on Invoices

Overage charges appear as separate line items on invoices, clearly distinguished from base plan charges. Each overage line item shows the meter, quantity, rate, and total cost.

```typescript
interface OverageLineItem {
  type: 'overage';
  meterId: string;
  meterName: string;
  allowance: number;
  actualUsage: number;
  overageQuantity: number;
  overageRate: number;
  totalCost: number;
  tieredBreakdown?: OverageTierLine[];
}

interface OverageTierLine {
  tierName: string;
  quantity: number;
  rate: number;
  cost: number;
}

class OverageInvoiceService {
  async generateOverageLineItems(
    tenantId: string,
    periodKey: string
  ): Promise<InvoiceLineItem[]> {
    const overage = await this.overageCalculator.calculateOverage(tenantId, periodKey);
    const items: InvoiceLineItem[] = [];

    for (const meter of overage.meters) {
      if (meter.overage <= 0) continue;

      const description = meter.tieredOverage.length > 1
        ? this.buildTieredDescription(meter)
        : `${meter.meterName} Overage — ${meter.overage} units @ ${formatCurrency(meter.overageRate)}/unit`;

      items.push({
        id: generateId('li'),
        description,
        type: LineItemType.USAGE,
        quantity: meter.overage,
        unitPrice: Math.round(meter.overageRate * 100),
        amount: Math.round(meter.overageCost * 100),
        taxAmount: 0,
        discountAmount: 0,
        metadata: {
          meterId: meter.meterId,
          overageType: 'usage',
          tieredBreakdown: JSON.stringify(meter.tieredOverage),
        },
      });
    }

    return items;
  }

  private buildTieredDescription(meter: OverageMeterCalculation): string {
    const parts = meter.tieredOverage.map(tier =>
      `${tier.usageInTier} @ ${formatCurrency(tier.rate)}`
    );
    return `${meter.meterName} Overage (${parts.join(', ')})`;
  }
}
```

## Aggregated Overage Billing

For high-volume customers, overage can be aggregated rather than itemized per meter. A single "Total Overage" line item simplifies the invoice.

```typescript
interface AggregatedOverageBilling {
  enabled: boolean;
  aggregationThreshold: number;  // Minimum overage cost to aggregate
  aggregationFormat: 'single' | 'category' | 'detailed';
}

function buildAggregatedOverageItem(
  meters: OverageMeterCalculation[],
  config: AggregatedOverageBilling
): InvoiceLineItem {
  const totalOverage = meters.reduce((s, m) => s + m.overageCost, 0);
  const totalUnits = meters.reduce((s, m) => s + m.overage, 0);

  return {
    id: generateId('li'),
    description: `Total overage (${totalUnits} units across ${meters.length} meters)`,
    type: LineItemType.USAGE,
    quantity: 1,
    unitPrice: Math.round(totalOverage * 100),
    amount: Math.round(totalOverage * 100),
    taxAmount: 0,
    discountAmount: 0,
    metadata: {
      overageType: 'aggregated',
      meterCount: meters.length.toString(),
      totalUnits: totalUnits.toString(),
    },
  };
}
```

## Per-Category Overage Breakdown

For transparency, invoices can show overage broken down by category (voice, transcription, TTS, storage, API).

```
Overage Breakdown on Invoice:
┌──────────────────────────────────────────────────────────────────┐
│ Overage Charges                                                   │
│                                                                  │
│ Category        │ Usage  │ Rate       │ Amount                  │
├─────────────────┼────────┼────────────┼─────────────────────────┤
│ Voice Minutes   │ 2,350  │ $0.035/min │ $82.25                  │
│                 │  min   │            │                         │
│ Transcription   │ 15,200 │ $0.006/sec │ $91.20                  │
│                 │  sec   │            │                         │
│ TTS Characters  │ 42,000 │ $0.0001/ch │ $4.20                   │
│                 │  chars │            │                         │
│ API Requests    │ 8,500  │ $0.001/req │ $8.50                   │
├─────────────────┼────────┼────────────┼─────────────────────────┤
│ Total Overage   │        │            │ $186.15                 │
└──────────────────────────────────────────────────────────────────┘
```

## Overage Invoice Integration

Overage charges are integrated into the standard invoice generation flow. The invoice generator checks for overage after calculating base plan charges.

```typescript
async function generateInvoiceWithOverage(
  subscriptionId: string,
  periodStart: string,
  periodEnd: string
): Promise<Invoice> {
  const subscription = await subscriptionService.getSubscription(subscriptionId);
  const periodKey = formatPeriodKey(periodStart);

  // Start with base plan line items
  const lineItems = await baseInvoiceService.generateLineItems(
    subscription,
    periodStart,
    periodEnd
  );

  // Add overage line items
  const overageItems = await overageInvoiceService.generateOverageLineItems(
    subscription.tenantId,
    periodKey
  );
  lineItems.push(...overageItems);

  // Calculate totals including overage
  const subtotal = lineItems.reduce((sum, li) => sum + li.amount, 0);
  const taxTotal = await taxService.calculateTaxTotal(subscription.tenantId, lineItems);

  // Create the invoice
  return invoiceService.createInvoice({
    subscriptionId,
    tenantId: subscription.tenantId,
    periodStart,
    periodEnd,
    lineItems,
    subtotal,
    taxTotal,
    total: subtotal + taxTotal,
  });
}
```

## Open-Source Tools

- **PostgreSQL** — Overage line item storage
- **pdfmake** (MIT) — Overage breakdown on invoice PDFs
- **Stripe API** — Overage as metered usage charge
- **BullMQ** — Schedule overage calculation for invoice generation

## Integration Points

Overage invoice items connect to the overage calculation engine (Section 1), the invoice generation service (Chapter 4 Section 2), the PDF generation service (Chapter 4 Section 3), and the tax service (Chapter 8).

## Production Considerations

- Clearly distinguish overage charges from plan charges
- Show overage rates prominently on invoices
- Provide drill-down from invoice line items to usage details
- Test overage invoice scenarios thoroughly
- Monitor overage-to-base revenue ratio

## Open-Source First Philosophy

Overage line items are calculated using PostgreSQL and BullMQ, rendered with pdfmake, and submitted through Stripe. This eliminates the need for proprietary billing platforms that charge per transaction for overage handling.
