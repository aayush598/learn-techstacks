# Section 04: Payment Reconciliation

## Stripe Payment Intents to Invoice Matching

Payment reconciliation matches Stripe Payment Intents (the payment attempt) to invoices. Each Invoice in Stripe has an associated Payment Intent that processes the payment. The reconciliation ensures every payment is correctly attributed to the right invoice.

```typescript
interface PaymentReconciliation {
  paymentIntentId: string;
  invoiceId: string;
  subscriptionId: string;
  tenantId: string;
  amount: number;
  currency: string;
  status: ReconciliationStatus;
  paymentMethod: string;
  fee: number;                   // Stripe processing fee
  netAmount: number;             // Amount - fee
  capturedAt: string;
  matchedAt: string;
}

enum ReconciliationStatus {
  MATCHED = 'matched',           // Payment matches invoice
  PARTIAL = 'partial',          // Partial payment
  UNMATCHED = 'unmatched',      // Payment without matching invoice
  MISMATCHED = 'mismatched',    // Amount differs from invoice
  DISPUTED = 'disputed',        // Payment under dispute
}

class PaymentReconciliationService {
  async reconcilePayment(
    paymentIntent: Stripe.PaymentIntent
  ): Promise<PaymentReconciliation> {
    // Extract invoice ID from payment intent metadata
    const invoiceId = paymentIntent.metadata?.invoice_id
      || paymentIntent.invoice;

    if (!invoiceId) {
      return {
        paymentIntentId: paymentIntent.id,
        invoiceId: null,
        subscriptionId: null,
        tenantId: null,
        amount: paymentIntent.amount_received,
        currency: paymentIntent.currency,
        status: ReconciliationStatus.UNMATCHED,
        paymentMethod: paymentIntent.payment_method_types?.[0],
        fee: 0,
        netAmount: paymentIntent.amount_received,
        capturedAt: new Date(paymentIntent.created * 1000).toISOString(),
        matchedAt: new Date().toISOString(),
      };
    }

    // Find the invoice
    const invoice = await stripe.invoices.retrieve(invoiceId);
    const tenantId = invoice.metadata?.tenant_id
      || (await this.getInternalInvoice(invoiceId))?.tenantId;

    const amount = paymentIntent.amount_received;
    const invoiceTotal = invoice.amount_due;

    let status: ReconciliationStatus;
    if (amount === invoiceTotal) {
      status = ReconciliationStatus.MATCHED;
    } else if (amount > 0 && amount < invoiceTotal) {
      status = ReconciliationStatus.PARTIAL;
    } else if (amount !== invoiceTotal) {
      status = ReconciliationStatus.MISMATCHED;
    }

    // Calculate Stripe fee
    const charges = await stripe.charges.list({
      payment_intent: paymentIntent.id,
    });
    const fee = charges.data.reduce((sum, c) => sum + (c.balance_transaction
      ? await this.getFeeAmount(c.balance_transaction)
      : 0), 0);

    const reconciliation: PaymentReconciliation = {
      paymentIntentId: paymentIntent.id,
      invoiceId,
      subscriptionId: invoice.subscription,
      tenantId,
      amount,
      currency: paymentIntent.currency,
      status,
      paymentMethod: paymentIntent.payment_method_types?.[0],
      fee,
      netAmount: amount - fee,
      capturedAt: new Date(paymentIntent.created * 1000).toISOString(),
      matchedAt: new Date().toISOString(),
    };

    // Store reconciliation record
    await this.db.paymentReconciliations.create(reconciliation);

    // Update invoice payment status
    if (status === ReconciliationStatus.MATCHED) {
      await this.db.invoices.updateOne(
        { stripeInvoiceId: invoiceId },
        {
          $set: {
            paymentStatus: PaymentStatus.PAID,
            amountPaid: amount,
            amountDue: 0,
            amountRemaining: 0,
            paidAt: new Date().toISOString(),
          },
        }
      );
    }

    return reconciliation;
  }

  private async getFeeAmount(
    balanceTransactionId: string
  ): Promise<number> {
    const tx = await stripe.balanceTransactions.retrieve(balanceTransactionId);
    return Math.abs(tx.fee);
  }
}
```

## Payment Status Tracking

Payment status is tracked through the entire lifecycle: pending → processing → succeeded/failed → reconciled. Each transition triggers appropriate actions.

```typescript
enum PaymentStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  SUCCEEDED = 'succeeded',
  FAILED = 'failed',
  DISPUTED = 'disputed',
  REFUNDED = 'refunded',
  PARTIALLY_REFUNDED = 'partially_refunded',
}

class PaymentTracker {
  async trackPayment(
    paymentIntentId: string,
    status: PaymentStatus,
    details?: any
  ): Promise<void> {
    await this.db.paymentEvents.create({
      paymentIntentId,
      status,
      timestamp: new Date().toISOString(),
      details,
    });

    // Update invoice status
    const reconciliation = await this.db.paymentReconciliations.findOne({
      paymentIntentId,
    });

    if (reconciliation) {
      const update: any = {};
      switch (status) {
        case PaymentStatus.SUCCEEDED:
          update.paymentStatus = PaymentStatus.PAID;
          update.paidAt = new Date().toISOString();
          break;
        case PaymentStatus.FAILED:
          update.paymentStatus = PaymentStatus.UNPAID;
          break;
        case PaymentStatus.DISPUTED:
          update.paymentStatus = PaymentStatus.UNCOLLECTIBLE;
          break;
        case PaymentStatus.REFUNDED:
          update.paymentStatus = PaymentStatus.REFUNDED;
          break;
      }

      await this.db.invoices.updateOne(
        { stripeInvoiceId: reconciliation.invoiceId },
        { $set: update }
      );
    }
  }
}
```

## Bank Reconciliation

For payments that don't go through Stripe (wire transfers, checks, ACH), manual bank reconciliation matches bank statement entries to invoices.

```typescript
interface BankTransaction {
  id: string;
  date: string;
  description: string;
  amount: number;
  currency: string;
  reference?: string;         // Invoice number or payment reference
  matched: boolean;
  matchedInvoiceId?: string;
  matchedAt?: string;
}

class BankReconciliationService {
  async reconcileBankStatement(
    transactions: BankTransaction[]
  ): Promise<ReconciliationSummary> {
    let matched = 0;
    let unmatched = 0;

    for (const tx of transactions) {
      // Try to match by invoice number
      if (tx.reference) {
        const invoice = await this.db.invoices.findOne({
          number: tx.reference,
        });
        if (invoice) {
          await this.matchTransactionToInvoice(tx, invoice);
          matched++;
          continue;
        }
      }

      // Try to match by amount and approximate date
      const candidates = await this.db.invoices.find({
        total: Math.round(tx.amount * 100), // Convert to cents
        status: InvoiceStatus.OPEN,
        dueDate: {
          $gte: new Date(Date.parse(tx.date) - 7 * 86400000).toISOString(),
          $lte: new Date(Date.parse(tx.date) + 7 * 86400000).toISOString(),
        },
      }).toArray();

      if (candidates.length === 1) {
        await this.matchTransactionToInvoice(tx, candidates[0]);
        matched++;
      } else {
        unmatched++;
      }
    }

    return { matched, unmatched, total: transactions.length };
  }

  private async matchTransactionToInvoice(
    transaction: BankTransaction,
    invoice: Invoice
  ): Promise<void> {
    await this.db.invoices.updateOne(
      { id: invoice.id },
      {
        $set: {
          paymentStatus: PaymentStatus.PAID,
          paidAt: transaction.date,
          amountPaid: Math.round(transaction.amount * 100),
          amountDue: 0,
        },
      }
    );

    await this.db.bankTransactions.updateOne(
      { id: transaction.id },
      { $set: { matched: true, matchedInvoiceId: invoice.id, matchedAt: new Date().toISOString() } }
    );
  }
}
```

## Open-Source Tools

- **Stripe API** — Payment intent and balance transaction retrieval
- **PostgreSQL** — Payment reconciliation records
- **BullMQ** — Schedule reconciliation jobs
- **Metabase** (Apache 2.0) — Reconciliation dashboards

## Integration Points

Payment reconciliation connects to the Stripe webhook handler (payment events), the invoice service (status updates), the dunning service (failed payments), and the accounting system (journal entries).

## Production Considerations

- Run reconciliation continuously (event-driven from Stripe webhooks)
- Set up alerts for unmatched payments older than 48 hours
- Handle partial payments and overpayments with credit notes
- Maintain audit trail for all manual reconciliations
- Reconcile daily with bank statements for accuracy

## Open-Source First Philosophy

Payment reconciliation uses Stripe's API for payment data and PostgreSQL for reconciliation records. BullMQ schedules reconciliation jobs reliably. Metabase provides dashboards for the finance team. This open-source stack avoids proprietary reconciliation software while providing complete financial audit capability.
