# Section 06: Credit Notes & Adjustments

## Credit Note Creation

Credit notes are issued to correct billing errors, provide refunds, or apply goodwill adjustments. They reduce the amount owed on future invoices or trigger a refund to the original payment method.

```typescript
class CreditNoteService {
  async createCreditNote(params: {
    tenantId: string;
    invoiceId: string;
    reason: CreditNoteReason;
    lineItems: CreditNoteLineItemInput[];
    memo?: string;
    sendNotification?: boolean;
  }): Promise<CreditNote> {
    const invoice = await this.db.invoices.findOne({
      id: params.invoiceId,
      tenantId: params.tenantId,
    });
    if (!invoice) throw new Error('Invoice not found');

    // Validate credit amount
    const totalCredit = params.lineItems.reduce(
      (sum, li) => sum + li.amount, 0
    );
    if (totalCredit > invoice.total) {
      throw new Error('Credit amount exceeds invoice total');
    }

    // Create in Stripe
    const stripeCreditNote = await stripe.creditNotes.create({
      invoice: invoice.stripeInvoiceId,
      reason: this.mapReasonToStripe(params.reason),
      amount: totalCredit,
      memo: params.memo,
      credit_amount: totalCredit,
    });

    // Create internal record
    const creditNote: CreditNote = {
      id: `cn_${nanoid(16)}`,
      number: await this.generateCreditNoteNumber(),
      invoiceId: params.invoiceId,
      tenantId: params.tenantId,
      reason: params.reason,
      total: totalCredit,
      taxTotal: Math.round(totalCredit * this.calculateTaxProportion(invoice)),
      lineItems: params.lineItems.map(li => ({
        originalLineItemId: li.lineItemId,
        amount: li.amount,
        taxAmount: Math.round(li.amount * this.calculateTaxProportion(invoice)),
        reason: li.reason || params.reason,
      })),
      status: 'issued',
      issuedAt: new Date().toISOString(),
      stripeCreditNoteId: stripeCreditNote.id,
    };

    await this.db.creditNotes.create(creditNote);

    // Update original invoice status
    const totalCredits = await this.getTotalCreditsForInvoice(params.invoiceId);
    if (totalCredits >= invoice.total) {
      await this.db.invoices.updateOne(
        { id: params.invoiceId },
        { $set: { paymentStatus: PaymentStatus.REFUNDED } }
      );
    }

    // Send notification
    if (params.sendNotification) {
      await this.notificationService.sendCreditNoteIssued(
        params.tenantId,
        creditNote
      );
    }

    return creditNote;
  }

  async issueRefundCreditNote(
    tenantId: string,
    invoiceId: string,
    amount: number,
    reason: string
  ): Promise<CreditNote> {
    const invoice = await this.db.invoices.findOne({ id: invoiceId, tenantId });

    // Refund via Stripe
    const refund = await stripe.refunds.create({
      payment_intent: invoice.stripePaymentIntentId,
      amount,
      reason: 'requested_by_customer',
    });

    return this.createCreditNote({
      tenantId,
      invoiceId,
      reason: CreditNoteReason.OTHER,
      lineItems: [{
        lineItemId: invoice.lineItems[0]?.id,
        amount,
        reason,
      }],
      memo: `Refund: ${reason}`,
      sendNotification: true,
    });
  }

  private mapReasonToStripe(reason: CreditNoteReason): string {
    const mapping: Record<CreditNoteReason, string> = {
      [CreditNoteReason.DUPLICATE]: 'duplicate',
      [CreditNoteReason.FRAUDULENT]: 'fraudulent',
      [CreditNoteReason.ORDER_CHANGE]: 'order_change',
      [CreditNoteReason.PRODUCT_UNSATISFACTORY]: 'product_unsatisfactory',
      [CreditNoteReason.SUBSCRIPTION_CHANGE]: 'subscription_change',
      [CreditNoteReason.OTHER]: 'other',
    };
    return mapping[reason];
  }

  private calculateTaxProportion(invoice: Invoice): number {
    if (invoice.subtotal === 0) return 0;
    return invoice.taxTotal / invoice.subtotal;
  }
}
```

## Application to Future Invoices

Credit notes can be applied to future invoices rather than issuing a refund. This is common when a customer overpaid and the credit will offset future charges.

```typescript
class CreditNoteApplicationService {
  async applyCreditToInvoice(
    creditNoteId: string,
    targetInvoiceId: string
  ): Promise<void> {
    const creditNote = await this.db.creditNotes.findOne({ id: creditNoteId });
    const targetInvoice = await this.db.invoices.findOne({ id: targetInvoiceId });

    if (creditNote.status !== 'issued') {
      throw new Error('Credit note has already been applied');
    }

    // Apply via Stripe
    await stripe.creditNotes.update(creditNote.stripeCreditNoteId, {
      invoice: targetInvoice.stripeInvoiceId,
    });

    // Update internal records
    await this.db.creditNotes.updateOne(
      { id: creditNoteId },
      {
        $set: {
          status: 'applied',
          appliedToInvoiceId: targetInvoiceId,
          appliedAt: new Date().toISOString(),
        },
      }
    );

    // Update target invoice total
    await this.db.invoices.updateOne(
      { id: targetInvoiceId },
      {
        $inc: {
          total: -creditNote.total,
          amountDue: -creditNote.total,
        },
      }
    );
  }

  async autoApplyCredits(tenantId: string): Promise<void> {
    // Find all open credit notes for this tenant
    const openCredits = await this.db.creditNotes.find({
      tenantId,
      status: 'issued',
    }).toArray();

    if (openCredits.length === 0) return;

    // Find the next open invoice
    const nextInvoice = await this.db.invoices.findOne({
      tenantId,
      status: InvoiceStatus.OPEN,
      paymentStatus: PaymentStatus.UNPAID,
    }, { sort: { issueDate: 1 } });

    if (!nextInvoice) return;

    // Apply credits in FIFO order
    for (const credit of openCredits) {
      if (nextInvoice.amountDue <= 0) break;
      const applyAmount = Math.min(credit.total, nextInvoice.amountDue);
      await this.applyCreditToInvoice(credit.id, nextInvoice.id);
    }
  }
}
```

## Refund Processing

Refunds return money to the customer's original payment method. Stripe supports full and partial refunds, with the option to refund the full amount or a portion.

```typescript
class RefundService {
  async processRefund(params: {
    tenantId: string;
    invoiceId: string;
    amount: number;
    reason: string;
    approvedBy: string;
  }): Promise<RefundResult> {
    const invoice = await this.db.invoices.findOne({
      id: params.invoiceId,
      tenantId: params.tenantId,
    });

    // Validate
    if (!invoice) throw new Error('Invoice not found');
    if (invoice.paymentStatus !== PaymentStatus.PAID) {
      throw new Error('Can only refund paid invoices');
    }
    if (params.amount > invoice.amountPaid) {
      throw new Error('Refund amount exceeds paid amount');
    }

    // Process in Stripe
    const refund = await stripe.refunds.create({
      payment_intent: invoice.stripePaymentIntentId,
      amount: params.amount,
      reason: 'requested_by_customer',
      metadata: {
        tenant_id: params.tenantId,
        invoice_id: params.invoiceId,
        approved_by: params.approvedBy,
      },
    });

    // Create credit note
    await this.creditNoteService.createCreditNote({
      tenantId: params.tenantId,
      invoiceId: params.invoiceId,
      reason: CreditNoteReason.OTHER,
      lineItems: [{
        lineItemId: invoice.lineItems[0]?.id,
        amount: params.amount,
        reason: params.reason,
      }],
      memo: `Refund: ${params.reason}`,
      sendNotification: true,
    });

    // Update invoice
    const newPaidAmount = invoice.amountPaid - params.amount;
    const paymentStatus = newPaidAmount <= 0
      ? PaymentStatus.REFUNDED
      : PaymentStatus.PARTIALLY_REFUNDED;

    await this.db.invoices.updateOne(
      { id: params.invoiceId },
      {
        $set: {
          paymentStatus,
          amountPaid: newPaidAmount,
          amountRemaining: newPaidAmount > 0 ? 0 : 0,
        },
      }
    );

    return {
      refundId: refund.id,
      amount: params.amount,
      status: refund.status,
    };
  }
}
```

## Adjustment Audit Trail

All credit notes and adjustments are logged with full audit information: who created it, why, what invoice it affects, and when.

```typescript
interface AdjustmentAuditEntry {
  id: string;
  type: 'credit_note' | 'refund' | 'manual_adjustment';
  tenantId: string;
  invoiceId: string;
  amount: number;
  reason: string;
  createdBy: string;
  approvedBy?: string;
  createdAt: string;
  metadata: Record<string, string>;
}
```

## Open-Source Tools

- **Stripe API** — Credit notes and refunds
- **PostgreSQL** — Credit note records and audit trail
- **BullMQ** — Schedule auto-application of credits
- **Nodemailer** (MIT) — Credit note notifications via email

## Integration Points

Credit notes integrate with the invoice service (status updates), the payment reconciliation system (refund matching), the notification service (customer communication), and the accounting system (journal entries).

## Production Considerations

- Implement approval workflows for credits above threshold
- Maintain complete audit trail for all adjustments
- Handle currency conversion for cross-currency refunds
- Monitor credit note patterns for potential abuse
- Test refund scenarios with Stripe test mode

## Open-Source First Philosophy

Stripe's credit note and refund APIs handle the financial operations, while PostgreSQL stores the complete audit trail. This avoids proprietary refund management software while maintaining full compliance with financial regulations.
