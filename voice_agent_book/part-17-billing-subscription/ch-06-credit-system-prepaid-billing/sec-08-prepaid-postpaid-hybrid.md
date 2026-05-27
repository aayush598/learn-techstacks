# Section 08: Prepaid vs Postpaid Hybrid

## Prepaid Balance First, Then Postpaid Billing

The hybrid billing model uses prepaid credits first for all consumption. When prepaid credits are exhausted, consumption automatically switches to postpaid billing (invoice-based). This provides the best customer experience — uninterrupted service with a monthly safety net.

```typescript
interface HybridBillingConfig {
  tenantId: string;
  mode: 'prepaid_only' | 'postpaid_only' | 'hybrid';
  consumptionOrder: ConsumptionOrder;
  postpaidLimit: number;        // Max postpaid usage before auto-topup
  postpaidBillingPeriod: 'monthly' | 'weekly';
  autoTopupOnPostpaid: boolean;
  notificationThresholds: number[];  // Credit balance thresholds
}

enum ConsumptionOrder {
  PREPAID_FIRST = 'prepaid_first',     // Use prepaid → then postpaid
  POSTPAID_FIRST = 'postpaid_first',   // Invoice-based → then prepaid
  PARALLEL = 'parallel',               // Split between both
}

class HybridBillingService {
  async processUsage(
    tenantId: string,
    meter: string,
    quantity: number,
    unitPrice: number,
    metadata: any
  ): Promise<HybridBillingResult> {
    const config = await this.getHybridConfig(tenantId);
    const creditsNeeded = Math.ceil(quantity * unitPrice);
    const prepaidBalance = await this.ledgerService.getBalance(tenantId);

    // Always try prepaid first (if in hybrid mode)
    if (config.mode === 'hybrid' || config.mode === 'prepaid_only') {
      if (prepaidBalance >= creditsNeeded) {
        // Consume from prepaid balance
        await this.ledgerService.recordTransaction({
          tenantId,
          type: CreditTransactionType.CONSUMPTION,
          amount: -creditsNeeded,
          currency: 'credits',
          description: `${meter}: ${quantity} units`,
          metadata: { ...metadata, billingMode: 'prepaid' },
          effectiveAt: new Date().toISOString(),
        });

        return {
          source: 'prepaid',
          creditsConsumed: creditsNeeded,
          remainingPrepaid: prepaidBalance - creditsNeeded,
          totalCost: 0, // Already paid via prepaid
        };
      }

      // Partial prepaid, rest goes to postpaid
      if (prepaidBalance > 0) {
        const partialCredits = Math.min(prepaidBalance, creditsNeeded);
        await this.ledgerService.recordTransaction({
          tenantId,
          type: CreditTransactionType.CONSUMPTION,
          amount: -partialCredits,
          currency: 'credits',
          description: `${meter}: Partial prepaid (${partialCredits} credits)`,
          metadata: { ...metadata, billingMode: 'prepaid_partial' },
          effectiveAt: new Date().toISOString(),
        });
      }
    }

    // Remaining goes to postpaid
    if (config.mode === 'hybrid' || config.mode === 'postpaid_only') {
      const postpaidCredits = creditsNeeded - Math.min(prepaidBalance, creditsNeeded);
      await this.recordPostpaidUsage(tenantId, meter, postpaidCredits, unitPrice, metadata);

      return {
        source: 'postpaid',
        creditsConsumed: prepaidBalance > 0 ? Math.min(prepaidBalance, creditsNeeded) : 0,
        remainingPrepaid: Math.max(0, prepaidBalance - creditsNeeded),
        postpaidCredits,
        totalCost: postpaidCredits * unitPrice * getCreditMonetaryValue(),
      };
    }

    return { source: 'none', creditsConsumed: 0, remainingPrepaid: prepaidBalance };
  }
}
```

## Hybrid Consumption Order

The hybrid model treats the credit balance as the primary payment method and invoicing as the backup. This creates a seamless customer experience where service is never interrupted.

```
Hybrid Consumption Flow:
┌────────────────────────────────────────────────────────────────┐
│ [Service Request]                                                │
│     ↓                                                            │
│ [Check Prepaid Balance]                                          │
│     ├── Sufficient → Deduct from prepaid ✓                      │
│     │                                                            │
│     └── Insufficient → Partial from prepaid                     │
│              ↓                                                   │
│         [Remaining → Postpaid Invoice]                          │
│              ↓                                                   │
│         [Record as Usage for Next Invoice]                      │
│              ↓                                                   │
│         [Check Auto-Topup Threshold]                            │
│              ├── Below threshold → Auto-purchase credits        │
│              └── Above threshold → Continue monitoring          │
└──────────────────────────────────────────────────────────────────┘
```

## Postpaid Usage Recording

Postpaid usage is recorded as pending invoice items. At the end of the billing period, all postpaid usage is aggregated into an invoice.

```typescript
interface PostpaidUsageRecord {
  id: string;
  tenantId: string;
  meter: string;
  credits: number;
  unitPrice: number;
  amount: number;             // Monetary value in cents
  recordedAt: string;
  invoiceId?: string;
  billed: boolean;
}

class PostpaidBillingService {
  async recordPostpaidUsage(
    tenantId: string,
    meter: string,
    credits: number,
    unitPrice: number,
    metadata: any
  ): Promise<void> {
    const monetaryValue = Math.round(credits * unitPrice * getCreditMonetaryValue());

    await this.db.postpaidUsage.create({
      id: `pp_${nanoid(16)}`,
      tenantId,
      meter,
      credits,
      unitPrice,
      amount: monetaryValue,
      recordedAt: new Date().toISOString(),
      billed: false,
    });

    // Check postpaid limit
    const periodTotal = await this.getPeriodPostpaidTotal(tenantId);
    const config = await this.getHybridConfig(tenantId);

    if (periodTotal >= config.postpaidLimit) {
      if (config.autoTopupOnPostpaid) {
        await this.autoTopupService.executeTopup(tenantId);
      }

      await this.notificationService.sendPostpaidLimitWarning(
        tenantId,
        periodTotal,
        config.postpaidLimit
      );
    }
  }

  async generatePostpaidInvoice(tenantId: string): Promise<Invoice> {
    const periodEnd = new Date();
    const periodStart = new Date(periodEnd.getTime() - 30 * 86400000);

    const usage = await this.db.postpaidUsage.find({
      tenantId,
      billed: false,
      recordedAt: {
        $gte: periodStart.toISOString(),
        $lt: periodEnd.toISOString(),
      },
    }).toArray();

    if (usage.length === 0) return null;

    const totalAmount = usage.reduce((sum, u) => sum + u.amount, 0);

    // Create invoice
    const invoice = await this.invoiceService.generateInvoice({
      tenantId,
      periodStart: periodStart.toISOString(),
      periodEnd: periodEnd.toISOString(),
      lineItems: [{
        description: `Postpaid usage (${formatDate(periodStart)} — ${formatDate(periodEnd)})`,
        type: 'postpaid',
        quantity: 1,
        unitPrice: totalAmount,
        amount: totalAmount,
      }],
    });

    // Mark usage as billed
    await this.db.postpaidUsage.updateMany(
      { _id: { $in: usage.map(u => u._id) } },
      { $set: { billed: true, invoiceId: invoice.id } }
    );

    return invoice;
  }
}
```

## Invoice Integration

Postpaid usage appears as line items on invoices, alongside subscription charges. The invoice clearly distinguishes between prepaid (already paid) and postpaid (due now) charges.

```typescript
function buildHybridInvoiceLineItems(
  subscription: Subscription,
  postpaidUsage: PostpaidUsageRecord[],
  prepaidConsumed: number
): InvoiceLineItem[] {
  const items: InvoiceLineItem[] = [];

  // Subscription plan charge
  items.push({
    description: `${subscription.planName} — Monthly`,
    type: 'plan',
    quantity: 1,
    unitPrice: subscription.planPrice,
    amount: subscription.planPrice,
  });

  // Prepaid credits consumed (informational, $0 line)
  if (prepaidConsumed > 0) {
    items.push({
      description: `Prepaid credits consumed (${prepaidConsumed})`,
      type: 'credit',
      quantity: 1,
      unitPrice: 0,
      amount: 0,
      notes: 'Covered by prepaid balance',
    });
  }

  // Postpaid usage
  if (postpaidUsage.length > 0) {
    const totalPostpaid = postpaidUsage.reduce((s, u) => s + u.amount, 0);
    items.push({
      description: `Postpaid usage — ${postpaidUsage.length} transactions`,
      type: 'usage',
      quantity: 1,
      unitPrice: totalPostpaid,
      amount: totalPostpaid,
    });
  }

  return items;
}
```

## Open-Source Tools

- **PostgreSQL** — Hybrid billing configuration and postpaid usage records
- **BullMQ** (MIT) — Schedule postpaid invoice generation
- **Redis** — Real-time credit balance for hybrid routing
- **Stripe API** — Postpaid invoice creation

## Integration Points

The hybrid model connects to the credit ledger (prepaid balance), the usage metering system (consumption), the invoice service (postpaid billing), and the auto-topup service (Chapter 7 Section 4).

## Production Considerations

- Monitor prepaid-to-postpaid ratio to optimize credit pack sizing
- Set postpaid credit limits to prevent runaway usage
- Send clear notifications when switching to postpaid
- Allow customers to configure their hybrid preferences
- Test hybrid billing at boundary conditions (prepaid exhaustion)

## Open-Source First Philosophy

The hybrid billing model is implemented entirely on PostgreSQL and Redis, with Stripe handling payments and invoices. BullMQ manages the postpaid billing schedule. This approach provides sophisticated prepaid/postpaid hybrid billing without the licensing costs of enterprise billing platforms like Chargebee or Recurly.
