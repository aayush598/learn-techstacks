# Section 07: Invoice Generation and Tracking

## Overview

Invoice generation and tracking provides a comprehensive billing document management system for the voice agent platform. The system generates invoices for one-time payments, subscription renewals, and manual charges across all payment gateways. Each invoice captures line-item details (products/services, quantities, unit prices, taxes, discounts), payment status, and provides a unified view of the customer's billing history regardless of which payment gateway processed the transaction.

The invoice engine integrates with the payment adapters to leverage each gateway's native invoice capabilities (Stripe Invoices, Square Invoices, Adyen Invoices) while maintaining a canonical invoice model in the platform's database. This hybrid approach ensures that invoices are always consistent with gateway-side financial records while enabling platform-specific features like custom invoice numbering, PO number fields, and consolidated billing across multiple subscriptions.

## Architecture

```
                   Invoice Generation System

   Voice Agent ←→ Invoice Engine ←→ Payment Adapter ←→ Gateway
                      |
   +----------------------------------------------------------+
   |               Invoice Lifecycle                          |
   |                                                          |
   |  +----------+    +----------+    +----------+           |
   |  | Draft    |--->| Open     |--->| Paid     |           |
   |  | (editing)|    | (awaiting|    |          |           |
   |  |          |    |  payment)|    |          |           |
   |  +----------+    +----------+    +----------+           |
   |       |               |              |                   |
   |       v               v              v                   |
   |  +----------+    +----------+    +----------+           |
   |  | Voided   |    | Past Due |    | Partially|           |
   |  |          |    | (overdue)|    | Paid     |           |
   |  +----------+    +----------+    +----------+           |
   |                                                          |
   |  Invoice Components:                                     |
   |  • Header (number, dates, PO, currency)                  |
   |  • Line Items (description, qty, unit price, total)     |
   |  • Tax Breakdown (by jurisdiction/rate)                  |
   |  • Discounts and Adjustments                             |
   |  • Payment Transactions (mapped to gateway references)   |
   |  • Memos and Terms                                       |
   +----------------------------------------------------------+
```

## Design Decisions

- **Canonical invoice model with gateway mapping over raw gateway invoices:** The platform stores a canonical invoice model in its database that mirrors but is independent of the gateway's invoice. A mapping layer tracks the relationship between platform invoice IDs and gateway invoice/charge IDs (e.g., platform invoice `inv_123` ↔ Stripe `in_1ABC`). This decouples the voice platform from any specific gateway's invoice schema and enables switching gateways without losing invoice history. Trade-off: dual storage doubles write overhead for invoice creation but provides gateway-independent financial records.

- **Invoice number generation at the platform level over gateway-assigned:** Invoice numbers follow a platform-defined format (e.g., `INV-2026-00001`) that is consistent across all gateways and payment methods. The platform assigns the number before sending the invoice to the gateway. The invoice number is stored in the gateway's invoice `description` or `metadata` field for cross-reference. Trade-off: platform-level numbering requires a counter sequence with gap handling but ensures professional, sequential numbering across all billing.

- **Deferred tax calculation with gateway fallback:** Tax calculation is performed by a third-party tax engine (TaxJar, Stripe Tax) at invoice finalization time. If the tax engine is unavailable, the system falls back to the gateway's built-in tax calculation or uses the last-known tax rate for the customer's jurisdiction. Tax calculation results are cached for 24 hours for the same customer/address combination. Trade-off: deferred calculation adds latency to invoice finalization but ensures the most current tax rates are applied.

## Implementation Approach

```
interface Invoice {
  id: string;
  number: string;
  customerId: string;
  subscriptionId?: string;
  status: 'draft' | 'open' | 'paid' | 'past_due' | 'void' | 'uncollectible';
  currency: string;
  total: number;
  subtotal: number;
  taxTotal: number;
  discountTotal: number;
  amountPaid: number;
  amountDue: number;
  lineItems: InvoiceLineItem[];
  taxBreakdown: TaxEntry[];
  transactions: PaymentTransaction[];
  periodStart: Date;
  periodEnd: Date;
  issuedAt: Date;
  paidAt?: Date;
  metadata: Record<string, string>;
}

interface InvoiceLineItem {
  description: string;
  quantity: number;
  unitPrice: number;
  total: number;
  taxRate?: number;
  type: 'subscription' | 'one_time' | 'adjustment' | 'tax' | 'shipping';
  metadata?: Record<string, string>;
}

class InvoiceEngine {
  private db: Database;
  private taxEngine: TaxEngine;
  private sequenceCounter: SequenceCounter;

  async generateInvoice(params: {
    customerId: string;
    subscriptionId?: string;
    lineItems: InvoiceLineItem[];
    currency: string;
    poNumber?: string;
    metadata?: Record<string, string>;
  }): Promise<Invoice> {
    const subtotal = params.lineItems.reduce((s, li) => s + li.total, 0);
    const invoiceNumber = await this.sequenceCounter.next('invoice');

    const taxResult = params.lineItems.some(li => li.taxRate !== undefined)
      ? await this.calculateTaxes(params)
      : { totalTax: 0, breakdown: [] };

    const discountTotal = 0;
    const total = subtotal + taxResult.totalTax - discountTotal;

    const invoice: Invoice = {
      id: generateId('inv'),
      number: `INV-${invoiceNumber.toString().padStart(8, '0')}`,
      customerId: params.customerId,
      subscriptionId: params.subscriptionId,
      status: 'draft',
      currency: params.currency,
      subtotal,
      taxTotal: taxResult.totalTax,
      discountTotal,
      total,
      amountPaid: 0,
      amountDue: total,
      lineItems: params.lineItems,
      taxBreakdown: taxResult.breakdown,
      transactions: [],
      periodStart: new Date(),
      periodEnd: new Date(),
      issuedAt: new Date(),
      metadata: params.metadata || {},
    };

    await this.db.invoices.insert(invoice);
    await this.emitEvent('invoice.created', { invoiceId: invoice.id, customerId: params.customerId });
    return invoice;
  }

  async finalizeAndSend(invoiceId: string, adapterType: string): Promise<Invoice> {
    const invoice = await this.db.invoices.find(invoiceId);
    if (!invoice || invoice.status !== 'draft') {
      throw new Error('Invoice must be in draft status to finalize');
    }

    const adapter = this.paymentAdapters.get(adapterType)!;
    const gatewayInvoice = await adapter.createInvoice({
      customerId: invoice.customerId,
      amount: invoice.total,
      currency: invoice.currency,
      description: `Invoice ${invoice.number}`,
      metadata: { platformInvoiceId: invoice.id, invoiceNumber: invoice.number },
    });

    invoice.status = 'open';
    invoice.issuedAt = new Date();
    const gwInvoiceId = gatewayInvoice?.data?.id;
    if (gwInvoiceId) {
      invoice.metadata.gatewayInvoiceId = gwInvoiceId;
    }

    await this.db.invoices.update(invoiceId, invoice);
    return invoice;
  }

  async recordPayment(invoiceId: string, payment: {
    transactionId: string;
    amount: number;
    currency: string;
    gateway: string;
    paymentMethod: string;
  }): Promise<Invoice> {
    const invoice = await this.db.invoices.find(invoiceId);
    if (!invoice) throw new Error('Invoice not found');

    invoice.transactions.push({
      id: payment.transactionId,
      amount: payment.amount,
      currency: payment.currency,
      gateway: payment.gateway,
      paymentMethod: payment.paymentMethod,
      timestamp: new Date(),
    });

    invoice.amountPaid += payment.amount;
    invoice.amountDue = invoice.total - invoice.amountPaid;

    if (invoice.amountDue <= 0) {
      invoice.status = 'paid';
      invoice.paidAt = new Date();
      await this.emitEvent('invoice.paid', { invoiceId, customerId: invoice.customerId });
    } else if (invoice.amountPaid > 0) {
      invoice.status = 'open';
    }

    await this.db.invoices.update(invoiceId, invoice);
    return invoice;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| TaxJar SDK (MIT) | Node.js | Sales tax calculation |
| PDFKit (MIT) | Node.js | PDF invoice generation |
| Mustache (MIT) | Templates | Invoice email templates |

## Production Considerations

**Scaling:** Invoice generation can be batched during subscription renewal runs. Generate invoices in the background and notify customers asynchronously. The invoice number counter must be atomic and distributed-safe — use PostgreSQL sequences or Redis INCR with WAL logging. Archive finalized invoices to cold storage (S3 Glacier, 30-day S3 standard then transition) to keep the database size manageable.

**Security:** Invoice data contains PII (customer name, address) — encrypt at rest and control access with role-based permissions (billing admin, read-only, customer portal). Never include full card data in invoice records. Validate PO numbers and tax IDs against configured patterns. Generate invoice PDFs server-side to prevent data exposure. Implement invoice voiding with a mandatory reason field for audit trails.

**Monitoring:** Track invoice generation volume, average time from draft to paid, overdue invoice aging buckets (0-30, 31-60, 61-90, 90+ days), void rate, and collection effectiveness index. Alert on high volumes of overdue invoices, unusual voiding patterns, and discrepancies between platform invoice totals and gateway totals. Run daily reconciliation reports and weekly aging summaries.
