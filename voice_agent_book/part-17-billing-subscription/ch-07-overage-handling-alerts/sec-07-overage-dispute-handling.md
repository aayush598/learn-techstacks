# Section 07: Overage Dispute Handling

## Usage Verification

Customers may dispute overage charges if they believe the usage data is incorrect. The dispute process starts with usage verification — comparing the billed usage against raw event data.

```typescript
interface OverageDispute {
  id: string;
  tenantId: string;
  invoiceId: string;
  meterId: string;
  disputedAmount: number;
  disputedQuantity: number;
  reason: string;
  status: DisputeStatus;
  evidence: DisputeEvidence;
  resolution?: DisputeResolution;
  createdAt: string;
  resolvedAt?: string;
}

enum DisputeStatus {
  OPEN = 'open',
  UNDER_REVIEW = 'under_review',
  RESOLVED = 'resolved',
  REJECTED = 'rejected',
}

interface DisputeEvidence {
  customerClaims: string;
  internalNotes: string;
  rawEventCount: number;
  aggregatedTotal: number;
  discrepancy: number;
  supportingLogs: string[];
}

class OverageDisputeService {
  async verifyUsage(
    disputeId: string
  ): Promise<VerificationResult> {
    const dispute = await this.db.overageDisputes.findOne({ id: disputeId });

    // Query raw usage events for the disputed period and meter
    const rawEvents = await this.db.usageRecords.find({
      tenantId: dispute.tenantId,
      meterId: dispute.meterId,
      eventTimestamp: {
        $gte: dispute.billingPeriodStart,
        $lte: dispute.billingPeriodEnd,
      },
    }).toArray();

    const aggregatedTotal = rawEvents.reduce(
      (sum, e) => sum + e.quantity, 0
    );

    // Compare with billing amount
    const billedAmount = dispute.disputedQuantity;
    const discrepancy = Math.abs(aggregatedTotal - billedAmount);

    const evidence: DisputeEvidence = {
      customerClaims: dispute.reason,
      internalNotes: '',
      rawEventCount: rawEvents.length,
      aggregatedTotal,
      discrepancy,
      supportingLogs: rawEvents.slice(0, 100).map(e =>
        `${e.eventTimestamp}: ${e.quantity} ${e.unit} (${e.id})`
      ),
    };

    return {
      disputeId,
      verified: discrepancy === 0,
      billedAmount,
      actualAmount: aggregatedTotal,
      discrepancy,
      evidence,
      status: discrepancy === 0 ? 'verified' : 'discrepancy_found',
    };
  }

  async resolveDispute(
    disputeId: string,
    resolution: DisputeResolution
  ): Promise<void> {
    const dispute = await this.db.overageDisputes.findOne({ id: disputeId });

    switch (resolution.type) {
      case 'accept':
        // Customer is correct — issue credit
        await this.creditNoteService.createCreditNote({
          tenantId: dispute.tenantId,
          invoiceId: dispute.invoiceId,
          reason: CreditNoteReason.OTHER,
          lineItems: [{
            lineItemId: dispute.meterId,
            amount: dispute.disputedAmount,
            reason: 'Overage dispute — verified customer claim',
          }],
        });
        break;

      case 'reject':
        // Customer is incorrect — provide evidence
        await this.provideUsageEvidence(dispute.tenantId, dispute.id);
        break;

      case 'partial':
        // Partial credit
        const partialAmount = Math.round(dispute.disputedAmount * resolution.percentage);
        await this.creditNoteService.createCreditNote({
          tenantId: dispute.tenantId,
          invoiceId: dispute.invoiceId,
          reason: CreditNoteReason.OTHER,
          lineItems: [{
            lineItemId: dispute.meterId,
            amount: partialAmount,
            reason: `Partial credit: ${resolution.percentage * 100}% of disputed amount`,
          }],
        });
        break;
    }

    await this.db.overageDisputes.updateOne(
      { id: disputeId },
      {
        $set: {
          status: 'resolved',
          resolution,
          resolvedAt: new Date().toISOString(),
        },
      }
    );

    await this.notificationService.sendDisputeResolved(
      dispute.tenantId,
      disputeId,
      resolution
    );
  }
}
```

## Invoice Adjustment

If the dispute is resolved in the customer's favor, a credit note or invoice adjustment is issued. The adjustment is linked to the original invoice for audit trail.

```typescript
async function adjustInvoiceForDispute(
  dispute: OverageDispute,
  adjustmentAmount: number
): Promise<void> {
  // Create credit note
  const creditNote = await stripe.creditNotes.create({
    invoice: dispute.invoiceId,
    amount: adjustmentAmount,
    reason: 'other',
    memo: `Overage dispute adjustment: ${dispute.reason}`,
    metadata: {
      dispute_id: dispute.id,
      tenant_id: dispute.tenantId,
    },
  });

  // Update internal invoice
  await db.invoices.updateOne(
    { stripeInvoiceId: dispute.invoiceId },
    {
      $inc: { total: -adjustmentAmount, amountDue: -adjustmentAmount },
      $push: {
        adjustments: {
          type: 'dispute',
          disputeId: dispute.id,
          amount: adjustmentAmount,
          date: new Date().toISOString(),
        },
      },
    }
  );
}
```

## Credit Issuance for Disputes

When usage data confirms the customer is correct, credits are issued to their account as a goodwill gesture.

```typescript
async function issueDisputeCredit(
  tenantId: string,
  disputeId: string,
  creditAmount: number
): Promise<void> {
  await ledgerService.recordTransaction({
    tenantId,
    type: CreditTransactionType.ADJUSTMENT,
    amount: creditAmount,
    currency: 'credits',
    description: `Credit for resolved overage dispute`,
    metadata: {
      source: 'dispute_resolution',
      reference: disputeId,
      tags: ['dispute', 'goodwill'],
    },
    effectiveAt: new Date().toISOString(),
  });
}
```

## Dispute Tracking

All disputes are tracked with full lifecycle information for analysis and pattern detection.

```typescript
interface DisputeMetrics {
  totalDisputes: number;
  resolvedInCustomerFavor: number;
  resolvedInPlatformFavor: number;
  averageResolutionTime: number; // Hours
  totalDisputedAmount: number;
  totalCreditedAmount: number;
  commonMeters: Array<{ meter: string; count: number }>;
  commonReasons: Array<{ reason: string; count: number }>;
}

async function getDisputeMetrics(
  periodStart: string,
  periodEnd: string
): Promise<DisputeMetrics> {
  const disputes = await db.overageDisputes.find({
    createdAt: { $gte: periodStart, $lte: periodEnd },
  }).toArray();

  const customerFavor = disputes.filter(d =>
    d.resolution?.type === 'accept' || d.resolution?.type === 'partial'
  );
  const platformFavor = disputes.filter(d =>
    d.resolution?.type === 'reject'
  );

  const resolutionTimes = disputes
    .filter(d => d.resolvedAt)
    .map(d => (Date.parse(d.resolvedAt) - Date.parse(d.createdAt)) / 3600000);

  return {
    totalDisputes: disputes.length,
    resolvedInCustomerFavor: customerFavor.length,
    resolvedInPlatformFavor: platformFavor.length,
    averageResolutionTime: resolutionTimes.length > 0
      ? resolutionTimes.reduce((a, b) => a + b, 0) / resolutionTimes.length
      : 0,
    totalDisputedAmount: disputes.reduce((s, d) => s + d.disputedAmount, 0),
    totalCreditedAmount: customerFavor.reduce((s, d) => s + (d.resolution?.amount || 0), 0),
    commonMeters: [], // Aggregate by meter
    commonReasons: [], // Aggregate by reason
  };
}
```

## Open-Source Tools

- **PostgreSQL** — Dispute records and tracking
- **BullMQ** — Schedule dispute deadline reminders
- **Metabase** (Apache 2.0) — Dispute analysis dashboards
- **Nodemailer** (MIT) — Dispute communication emails

## Integration Points

Overage disputes connect to the usage metering database (evidence gathering), the credit note system (adjustments), the invoice system (corrections), and the notification service (customer communications).

## Production Considerations

- Set up automatic evidence gathering for common dispute types
- Implement SLA for dispute resolution (e.g., respond within 24 hours)
- Track dispute-to-revenue ratio as quality metric
- Monitor dispute patterns for systematic billing issues
- Escalate unresolved disputes automatically

## Open-Source First Philosophy

PostgreSQL stores all dispute data with complete audit trails. Metabase provides analytics for dispute trend identification. BullMQ manages resolution deadlines. This open-source approach avoids proprietary dispute management platforms while providing effective dispute resolution capabilities.
