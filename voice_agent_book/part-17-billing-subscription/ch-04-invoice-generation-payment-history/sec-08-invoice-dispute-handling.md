# Section 08: Invoice Dispute Handling

## Dispute Intake

Invoice disputes (chargebacks) occur when a customer disputes a charge with their bank. The dispute process is managed through Stripe, which provides detailed information about the dispute reason, evidence requirements, and timeline.

```typescript
interface Dispute {
  id: string;
  chargeId: string;
  paymentIntentId: string;
  invoiceId: string;
  tenantId: string;
  amount: number;
  currency: string;
  reason: DisputeReason;
  status: DisputeStatus;
  evidence: DisputeEvidence;
  timeline: DisputeTimeline;
  createdAt: string;
  resolvedAt?: string;
  outcome?: 'won' | 'lost' | 'accepted';
}

enum DisputeReason {
  GENERAL = 'general',
  DUPLICATE = 'duplicate',
  FRAUDULENT = 'fraudulent',
  SUBSCRIPTION_CANCELED = 'subscription_canceled',
  PRODUCT_UNACCEPTABLE = 'product_unacceptable',
  PRODUCT_NOT_RECEIVED = 'product_not_received',
  UNRECOGNIZED = 'unrecognized',
  CREDIT_NOT_PROCESSED = 'credit_not_processed',
  INCORRECT_AMOUNT = 'incorrect_amount',
}

enum DisputeStatus {
  NEEDS_RESPONSE = 'needs_response',
  UNDER_REVIEW = 'under_review',
  WON = 'won',
  LOST = 'lost',
  ACCEPTED = 'accepted',
  WARNING_CLOSED = 'warning_closed',
  WARNING_NEEDS_RESPONSE = 'warning_needs_response',
}

class DisputeService {
  async handleDisputeCreated(dispute: Stripe.Dispute): Promise<Dispute> {
    const invoice = await this.getInvoiceByChargeId(dispute.charge);
    const tenantId = invoice?.tenantId;

    const internalDispute: Dispute = {
      id: dispute.id,
      chargeId: dispute.charge as string,
      paymentIntentId: dispute.payment_intent as string,
      invoiceId: invoice?.id,
      tenantId,
      amount: dispute.amount,
      currency: dispute.currency,
      reason: dispute.reason as DisputeReason,
      status: DisputeStatus.NEEDS_RESPONSE,
      evidence: {
        submitted: false,
        productDescription: 'Voice agent subscription services',
        customerEmail: invoice?.customerEmail,
      },
      timeline: {
        created: new Date(dispute.created * 1000).toISOString(),
        evidenceDeadline: new Date(dispute.evidence_details?.due_by * 1000).toISOString(),
      },
      createdAt: new Date().toISOString(),
    };

    await this.db.disputes.create(internalDispute);

    // Notify billing team
    await this.notificationService.sendDisputeNotification(tenantId, {
      disputeId: dispute.id,
      amount: dispute.amount,
      reason: dispute.reason,
      deadline: internalDispute.timeline.evidenceDeadline,
    });

    return internalDispute;
  }
}
```

## Evidence Submission

Responding to disputes requires submitting evidence to Stripe within the dispute deadline. Evidence includes proof of service delivery, customer communication, and billing agreement.

```typescript
interface DisputeEvidence {
  submitted: boolean;
  submittedAt?: string;
  productDescription?: string;
  customerEmail?: string;
  customerPurchaseIp?: string;
  customerSignature?: string;
  billingAddress?: string;
  receiptUrl?: string;
  serviceDocumentation?: string;
  refundPolicy?: string;
  uncategorizedText?: string;
  additionalEvidenceUrls?: string[];
}

class EvidenceSubmissionService {
  async prepareEvidence(disputeId: string): Promise<DisputeEvidence> {
    const dispute = await this.db.disputes.findOne({ id: disputeId });

    // Gather evidence
    const invoice = await this.db.invoices.findOne({ id: dispute.invoiceId });
    const subscription = await this.subscriptionService.getSubscription(invoice.subscriptionId);
    const tenant = await this.tenantService.getTenant(dispute.tenantId);

    // Generate service usage report
    const usageEvidence = await this.generateUsageEvidence(dispute);

    return {
      productDescription: 'Voice agent platform subscription services including automated outbound calling, real-time transcription, and AI-powered conversation analytics.',
      customerEmail: tenant.email,
      customerPurchaseIp: tenant.signupIp,
      billingAddress: tenant.billingAddress
        ? `${tenant.billingAddress.line1}, ${tenant.billingAddress.city}, ${tenant.billingAddress.state} ${tenant.billingAddress.postalCode}`
        : undefined,
      receiptUrl: invoice.pdfUrl,
      serviceDocumentation: usageEvidence,
      refundPolicy: 'Our refund policy is available at https://platform.com/refund-policy. Customers may cancel at any time with prorated refunds for unused service.',
      additionalEvidenceUrls: await this.collectCallLogs(dispute.tenantId, invoice.periodStart, invoice.periodEnd),
    };
  }

  async submitEvidence(disputeId: string): Promise<void> {
    const dispute = await this.db.disputes.findOne({ id: disputeId });
    const evidence = await this.prepareEvidence(disputeId);

    // Upload evidence files to Stripe
    const fileUploads = [];
    for (const url of evidence.additionalEvidenceUrls || []) {
      const file = await this.uploadFileToStripe(url);
      fileUploads.push(file.id);
    }

    // Submit via Stripe API
    await stripe.disputes.update(disputeId, {
      evidence: {
        product_description: evidence.productDescription,
        customer_email: evidence.customerEmail,
        customer_purchase_ip: evidence.customerPurchaseIp,
        customer_signature: evidence.customerSignature,
        billing_address: evidence.billingAddress,
        receipt: evidence.receiptUrl,
        service_documentation: evidence.serviceDocumentation,
        refund_policy: evidence.refundPolicy,
        uncategorized_text: evidence.uncategorizedText,
        ...(fileUploads.length > 0 ? { additional_evidence: fileUploads } : {}),
      },
    });

    await this.db.disputes.updateOne(
      { id: disputeId },
      {
        $set: {
          'evidence.submitted': true,
          'evidence.submittedAt': new Date().toISOString(),
          status: DisputeStatus.UNDER_REVIEW,
        },
      }
    );
  }

  private async uploadFileToStripe(fileUrl: string): Promise<Stripe.File> {
    const response = await fetch(fileUrl);
    const buffer = await response.buffer();
    return await stripe.files.create({
      purpose: 'dispute_evidence',
      file: {
        data: buffer,
        name: 'evidence_document.pdf',
        type: 'application/pdf',
      },
    });
  }
}
```

## Dispute Resolution

Disputes can be won (evidence accepted), lost (evidence insufficient), or accepted (merchant chooses not to contest). Each outcome has different financial implications.

```typescript
class DisputeResolutionService {
  async handleDisputeResolved(disputeId: string): Promise<void> {
    const stripeDispute = await stripe.disputes.retrieve(disputeId);
    const dispute = await this.db.disputes.findOne({ id: disputeId });

    let outcome: 'won' | 'lost' | 'accepted';
    if (stripeDispute.status === 'won') {
      outcome = 'won';
    } else if (stripeDispute.status === 'lost') {
      outcome = 'lost';
    } else {
      outcome = 'accepted';
    }

    await this.db.disputes.updateOne(
      { id: disputeId },
      {
        $set: {
          status: outcome === 'won' ? DisputeStatus.WON
            : outcome === 'lost' ? DisputeStatus.LOST
            : DisputeStatus.ACCEPTED,
          outcome,
          resolvedAt: new Date().toISOString(),
        },
      }
    );

    if (outcome === 'lost') {
      // Write off the amount
      await this.db.invoices.updateOne(
        { id: dispute.invoiceId },
        { $set: { paymentStatus: PaymentStatus.UNCOLLECTIBLE } }
      );
    } else if (outcome === 'won') {
      // Re-invoice or restore payment
      await this.db.invoices.updateOne(
        { id: dispute.invoiceId },
        { $set: { paymentStatus: PaymentStatus.PAID } }
      );
    }

    // Notify customer
    await this.notificationService.sendDisputeOutcome(
      dispute.tenantId,
      disputeId,
      outcome
    );
  }
}
```

## Chargeback Prevention

Preventing chargebacks is more effective than disputing them. Prevention strategies include clear billing descriptors, proactive communication, and easy cancellation flows.

```typescript
interface ChargebackPreventionConfig {
  statementDescriptor: string;        // Max 22 chars, recognizable on bank statement
  statementDescriptorPrefix?: string; // For SaaS platforms
  emailReceipt: boolean;
  preDisputeNotification: boolean;
  easyCancellation: boolean;
  refundPolicy: RefundPolicy;
}

async function configureBillingDescriptor(tenantId: string): Promise<void> {
  const tenant = await this.tenantService.getTenant(tenantId);

  await stripe.accounts.update(accountId, {
    settings: {
      card_payments: {
        statement_descriptor_prefix: 'VOICEAGENT',
      },
    },
  });
}

async function sendPreDisputeNotification(
  tenantId: string,
  invoiceId: string
): Promise<void> {
  // If payment fails, send notification before dispute arises
  const invoice = await this.db.invoices.findOne({ id: invoiceId });

  if (invoice.paymentStatus === PaymentStatus.UNPAID
    && daysSince(invoice.dueDate) > 5) {
    await this.notificationService.sendPaymentReminder(tenantId, invoiceId, {
      subject: 'Having trouble with payment?',
      message: 'We noticed your recent payment didn\'t go through. Please update your payment method to avoid service interruption.',
      actionUrl: `${APP_URL}/billing/payment-methods`,
    });
  }
}
```

## Open-Source Tools

- **Stripe API** — Dispute management and evidence submission
- **BullMQ** — Schedule dispute deadline reminders
- **PostgreSQL** — Dispute records and evidence tracking
- **Nodemailer** (MIT) — Dispute notification emails

## Integration Points

Dispute handling integrates with the Stripe webhook handler (dispute events), the invoice service (status updates), the notification service (customer and team alerts), and the reconciliation service (financial impact tracking).

## Production Considerations

- Set up alerts for dispute creation (immediate notification)
- Track dispute-to-revenue ratio as a key metric
- Maintain evidence templates for common dispute types
- Monitor dispute trends by customer segment and region
- Implement automated evidence gathering where possible
- Keep dispute response time under 24 hours

## Open-Source First Philosophy

Stripe handles the complex dispute lifecycle with regulatory compliance. PostgreSQL stores dispute records for analysis and trend tracking. BullMQ schedules evidence deadline reminders. This open-source approach avoids proprietary chargeback management software while maintaining effective dispute handling capabilities.
