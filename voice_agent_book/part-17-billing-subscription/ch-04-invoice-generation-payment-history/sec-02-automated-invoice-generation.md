# Section 02: Automated Invoice Generation

## Invoice Generation Trigger

Invoices are generated automatically at the end of each billing period. The trigger is the subscription's period-end, detected via Stripe's invoice webhook or by scheduled job.

```typescript
class InvoiceGenerationService {
  async generateInvoiceForPeriod(
    subscriptionId: string,
    periodStart: string,
    periodEnd: string
  ): Promise<Invoice> {
    const subscription = await this.subscriptionService.getSubscription(subscriptionId);
    const plan = await this.planCatalog.getPlan(subscription.planId);
    const usage = await this.usageService.getPeriodUsage(
      subscription.tenantId,
      periodStart,
      periodEnd
    );

    // Build line items
    const lineItems: InvoiceLineItem[] = [];

    // 1. Base plan charge
    lineItems.push({
      id: generateId('li'),
      description: `${plan.name} — ${formatDate(periodStart)} to ${formatDate(periodEnd)}`,
      type: LineItemType.PLAN,
      quantity: 1,
      unitPrice: plan.price,
      amount: plan.price,
      taxAmount: 0,
      discountAmount: 0,
    });

    // 2. Metered usage (overage)
    const overageUsage = usage.filter(u => u.overage > 0);
    for (const u of overageUsage) {
      const overageAmount = Math.round(u.overage * u.overageRate);
      lineItems.push({
        id: generateId('li'),
        description: `${u.meterName} Overage — ${u.overage} ${u.unit} @ ${formatCurrency(u.overageRate)}/${u.unit}`,
        type: LineItemType.USAGE,
        quantity: u.overage,
        unitPrice: Math.round(u.overageRate * 100), // In cents
        amount: overageAmount,
        taxAmount: 0,
        discountAmount: 0,
        metadata: { meter: u.meterId },
      });
    }

    // 3. Add-ons
    for (const addon of subscription.addons) {
      lineItems.push({
        id: generateId('li'),
        description: addon.name,
        type: LineItemType.ADDON,
        quantity: 1,
        unitPrice: addon.price,
        amount: addon.price,
        taxAmount: 0,
        discountAmount: 0,
      });
    }

    // Calculate totals
    const subtotal = lineItems.reduce((sum, li) => sum + li.amount, 0);
    const discountTotal = 0; // Applied later
    const taxTotal = await this.taxService.calculateTaxTotal(
      subscription.tenantId,
      lineItems
    );

    const invoice: Invoice = {
      id: generateId('inv'),
      number: await this.generateInvoiceNumber(),
      tenantId: subscription.tenantId,
      subscriptionId,
      periodStart,
      periodEnd,
      issueDate: new Date().toISOString(),
      dueDate: this.calculateDueDate(subscription),
      subtotal,
      discountTotal,
      taxTotal,
      total: subtotal - discountTotal + taxTotal,
      amountPaid: 0,
      amountDue: subtotal - discountTotal + taxTotal,
      amountRemaining: subtotal - discountTotal + taxTotal,
      currency: 'usd',
      status: InvoiceStatus.DRAFT,
      paymentStatus: PaymentStatus.UNPAID,
      lineItems,
      taxBreakdown: [],
      discounts: [],
      metadata: {},
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    await this.db.invoices.create(invoice);
    return invoice;
  }

  async finalizeInvoice(invoiceId: string): Promise<Invoice> {
    const invoice = await this.db.invoices.findById(invoiceId);
    if (invoice.status !== InvoiceStatus.DRAFT) {
      throw new Error(`Cannot finalize invoice in status ${invoice.status}`);
    }

    // Push to Stripe
    const stripeInvoice = await this.createStripeInvoice(invoice);

    // Update with Stripe ID
    await this.db.invoices.updateOne(
      { id: invoiceId },
      {
        $set: {
          stripeInvoiceId: stripeInvoice.id,
          status: InvoiceStatus.OPEN,
          dueDate: new Date(stripeInvoice.due_date * 1000).toISOString(),
        },
      }
    );

    return { ...invoice, status: InvoiceStatus.OPEN, stripeInvoiceId: stripeInvoice.id };
  }

  private async createStripeInvoice(invoice: Invoice): Promise<Stripe.Invoice> {
    const subscription = await this.stripeService.getSubscription(invoice.subscriptionId);

    // Create pending invoice items
    for (const lineItem of invoice.lineItems) {
      if (lineItem.type === LineItemType.USAGE) {
        // Usage is already tracked via Stripe metered billing
        continue;
      }

      await stripe.invoiceItems.create({
        customer: subscription.customer,
        subscription: invoice.subscriptionId,
        amount: lineItem.amount,
        currency: invoice.currency,
        description: lineItem.description,
        period: {
          start: Math.floor(new Date(invoice.periodStart).getTime() / 1000),
          end: Math.floor(new Date(invoice.periodEnd).getTime() / 1000),
        },
        metadata: { internal_line_item_id: lineItem.id },
      });
    }

    // Finalize the invoice
    return await stripe.invoices.finalizeInvoice(invoice.stripeInvoiceId);
  }
}
```

## Period-End Processing

Period-end processing runs after each billing period closes. It aggregates usage, calculates charges, generates invoices, and initiates payment.

```
Period-End Processing Flow:
┌──────────────────────────────────────────────────────────────────┐
│ [Subscription Period Ends]                                       │
│     ↓                                                            │
│ [Collect Usage] → Query usage aggregation for period             │
│     ↓                                                            │
│ [Calculate Overage] → Usage vs plan inclusion comparison        │
│     ↓                                                            │
│ [Build Line Items] → Plan charge + overage + addons             │
│     ↓                                                            │
│ [Calculate Tax] → Apply Stripe Tax or internal calculation      │
│     ↓                                                            │
│ [Create Invoice] → Draft invoice in database                     │
│     ↓                                                            │
│ [Push to Stripe] → Stripe invoice creation and finalization     │
│     ↓                                                            │
│ [Attempt Payment] → Auto-charge default payment method          │
│     ↓                                                            │
│ [Send Invoice] → Email invoice PDF to customer                  │
│     ↓                                                            │
│ [Close Period] → Mark billing period as processed               │
└──────────────────────────────────────────────────────────────────┘
```

## Proration Calculations

Proration occurs when a customer changes plans mid-cycle. The proration adjusts the invoice to reflect the proportional charge for each plan during the billing period.

```typescript
function calculateProrationLineItems(
  currentPlan: PlanDefinition,
  newPlan: PlanDefinition,
  changeDate: Date,
  periodStart: Date,
  periodEnd: Date
): InvoiceLineItem[] {
  const daysInPeriod = daysBetween(periodStart, periodEnd);
  const daysBeforeChange = daysBetween(periodStart, changeDate);
  const daysAfterChange = daysBetween(changeDate, periodEnd);

  const items: InvoiceLineItem[] = [];

  // Credit for unused portion of current plan
  if (daysAfterChange > 0) {
    const dailyRate = currentPlan.price / daysInPeriod;
    const credit = Math.round(dailyRate * daysAfterChange);

    items.push({
      id: generateId('li'),
      description: `Credit: ${currentPlan.name} (unused ${daysAfterChange} days)`,
      type: LineItemType.PRORATION,
      quantity: 1,
      unitPrice: -credit,
      amount: -credit,
      taxAmount: 0,
      discountAmount: 0,
      metadata: { proration_type: 'credit' },
    });
  }

  // Charge for new plan remaining days
  if (daysAfterChange > 0) {
    const dailyRate = newPlan.price / daysInPeriod;
    const charge = Math.round(dailyRate * daysAfterChange);

    items.push({
      id: generateId('li'),
      description: `${newPlan.name} (${daysAfterChange} days prorated)`,
      type: LineItemType.PRORATION,
      quantity: 1,
      unitPrice: charge,
      amount: charge,
      taxAmount: 0,
      discountAmount: 0,
      metadata: { proration_type: 'charge' },
    });
  }

  return items;
}
```

## Consolidated Invoices

For enterprise customers with multiple subscriptions, invoices can be consolidated into a single document. This simplifies accounts payable processing.

```typescript
interface ConsolidatedInvoice {
  id: string;
  tenantId: string;
  subscriptionIds: string[];
  invoices: Invoice[];        // Individual invoices
  periodStart: string;
  periodEnd: string;
  total: number;
  currency: string;
}
```

## Open-Source Tools

- **BullMQ** (MIT) — Schedule period-end invoice generation
- **PostgreSQL** — Invoice and line item storage
- **Stripe API** — Invoice creation and finalization
- **node-cron** (ISC) — Cron-based invoice generation triggers

## Integration Points

Invoice generation connects to the subscription service (plan details, period dates), the usage metering system (metered charges), the tax service (tax calculation), the payment service (auto-payment), and the notification service (invoice delivery).

## Production Considerations

- Generate invoices during off-peak hours to reduce load
- Implement idempotency for invoice generation (avoid duplicates)
- Handle partial period usage for new subscriptions (first invoice is prorated)
- Monitor invoice generation failures and alert billing team
- Maintain invoice generation SLA (e.g., within 1 hour of period end)

## Open-Source First Philosophy

BullMQ handles all scheduled invoice generation jobs reliably without a proprietary scheduler. PostgreSQL stores invoice data with full audit capability. This open-source stack avoids the licensing costs of enterprise billing engines while providing reliable, auditable invoice generation at scale.
