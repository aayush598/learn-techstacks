# Section 08: Usage Data Reconciliation

## Stripe vs Internal Usage Comparison

Usage reconciliation compares the usage recorded in our internal systems against what Stripe has recorded for billing. Discrepancies can arise from network failures, race conditions, or processing bugs. Regular reconciliation ensures accurate billing and detects issues early.

The reconciliation process runs after each billing period closes. It compares internal usage records against Stripe's usage record summaries for the same subscription and period.

```typescript
interface ReconciliationReport {
  periodKey: string;
  tenantId: string;
  subscriptionId: string;
  meters: MeterReconciliation[];
  status: 'matched' | 'discrepancy' | 'investigating';
  generatedAt: string;
}

interface MeterReconciliation {
  meterId: string;
  internalTotal: number;
  stripeTotal: number;
  difference: number;
  tolerance: Tolerance;
  status: 'ok' | 'warn' | 'critical';
  events: ReconciliationEvent[];
}

interface ReconciliationEvent {
  eventId: string;
  timestamp: string;
  internalQuantity: number;
  stripeQuantity: number;
  source: string;
}

class ReconciliationService {
  private readonly TOLERANCE_PERCENT = 0.01; // 1% tolerance

  async reconcile(
    tenantId: string,
    subscriptionId: string,
    periodKey: string
  ): Promise<ReconciliationReport> {
    // Internal usage aggregated
    const internalUsage = await this.getInternalUsage(tenantId, periodKey);

    // Stripe usage records
    const stripeUsage = await this.getStripeUsage(subscriptionId, periodKey);

    const meters: MeterReconciliation[] = [];

    for (const [meterId, internalTotal] of Object.entries(internalUsage)) {
      const stripeTotal = stripeUsage[meterId] || 0;
      const difference = Math.abs(internalTotal - stripeTotal);
      const tolerance = internalTotal * this.TOLERANCE_PERCENT;

      let status: 'ok' | 'warn' | 'critical';
      if (difference === 0) {
        status = 'ok';
      } else if (difference <= tolerance) {
        status = 'warn';
      } else {
        status = 'critical';
      }

      meters.push({
        meterId,
        internalTotal,
        stripeTotal,
        difference,
        tolerance,
        status,
        events: await this.getEventsForMeter(tenantId, meterId, periodKey),
      });
    }

    const status = meters.some(m => m.status === 'critical')
      ? 'discrepancy'
      : meters.some(m => m.status === 'warn')
        ? 'investigating'
        : 'matched';

    return {
      periodKey,
      tenantId,
      subscriptionId,
      meters,
      status,
      generatedAt: new Date().toISOString(),
    };
  }

  private async getStripeUsage(
    subscriptionId: string,
    periodKey: string
  ): Promise<Record<string, number>> {
    const subscription = await stripe.subscriptions.retrieve(subscriptionId);

    const usage: Record<string, number> = {};
    for (const item of subscription.items.data) {
      if (item.metadata.meter) {
        const summaries = await stripe.subscriptionItems.listUsageRecordSummaries(
          item.id,
          { limit: 100 }
        );
        const periodSummary = summaries.data.find(s =>
          s.period.start <= periodKey && s.period.end >= periodKey
        );
        if (periodSummary) {
          usage[item.metadata.meter] = periodSummary.total_usage;
        }
      }
    }

    return usage;
  }
}
```

## Discrepancy Detection

Discrepancies are categorized by severity and cause. Common causes include:

- **Timing mismatch**: Events arrived after Stripe period closed (late events)
- **Deduplication failure**: Same event counted twice in one system
- **Conversion error**: Quantity rounding differs between systems
- **Pipeline failure**: Events lost in processing pipeline
- **Stripe API error**: Usage record submission failed

```
Discrepancy Classification:
┌──────────────────────────────────────────────────────────────────┐
│ Difference │ Category      │ Action                             │
├────────────┼───────────────┼────────────────────────────────────┤
│ < 1%       │ Within tol.   │ Log and monitor                    │
│ 1-5%       │ Minor         │ Investigate, adjust if needed      │
│ 5-20%      │ Significant   │ Create adjustment, audit pipeline  │
│ > 20%      │ Critical      │ Pause billing, full investigation  │
└──────────────────────────────────────────────────────────────────┘
```

## Manual Adjustment Tools

When discrepancies are identified, the billing team needs tools to make adjustments. Adjustments are logged as credit notes or additional invoices, and the audit trail records the reason and approval.

```typescript
interface UsageAdjustment {
  id: string;
  tenantId: string;
  periodKey: string;
  meter: string;
  adjustmentType: 'credit' | 'debit';
  quantity: number;
  reason: string;
  approvedBy: string;
  reconciliationId: string;
  createdAt: string;
}

class AdjustmentService {
  async createAdjustment(
    adjustment: Omit<UsageAdjustment, 'id' | 'createdAt'>
  ): Promise<UsageAdjustment> {
    // Validate adjustment
    const report = await this.reconciliationService.reconcile(
      adjustment.tenantId,
      adjustment.subscriptionId,
      adjustment.periodKey
    );

    // Create credit note or additional invoice via Stripe
    if (adjustment.adjustmentType === 'credit') {
      await stripe.creditNotes.create({
        invoice: adjustment.invoiceId,
        amount: this.calculateAmount(adjustment),
        reason: 'other',
        metadata: {
          reconciliation_id: adjustment.reconciliationId,
          adjustment_reason: adjustment.reason,
        },
      });
    }

    // Record adjustment
    const record = await this.db.usageAdjustments.create({
      ...adjustment,
      id: `adj_${nanoid(16)}`,
      createdAt: new Date().toISOString(),
    });

    return record;
  }
}
```

## Audit Reports

All reconciliation runs produce audit reports that are stored for compliance and historical reference. Reports include the full event-level breakdown for each meter, the exact difference calculated, and any adjustments applied.

```typescript
interface AuditReport {
  reportId: string;
  generatedAt: string;
  period: string;
  totalTenants: number;
  matchedTenants: number;
  discrepancyCount: number;
  totalAdjustments: number;
  adjustmentValue: number;
  discrepancies: Array<{
    tenantId: string;
    meter: string;
    diff: number;
    cause: string;
    resolved: boolean;
  }>;
}
```

## Open-Source Tools

- **PostgreSQL** — Store reconciliation reports and adjustment history
- **BullMQ** — Schedule periodic reconciliation jobs
- **Metabase** (Apache 2.0) — Reconciliation dashboards for billing team
- **Stripe API** — Retrieve usage record summaries for comparison

## Integration Points

Reconciliation connects to the usage aggregation system (for internal totals), the Stripe API (for usage record summaries), the invoice system (for adjustment creation), and the notification system (for alerting billing team about discrepancies).

## Production Considerations

- Schedule reconciliation to run 24-48 hours after period end
- Set up automated alerting for critical discrepancies
- Maintain audit trail of all adjustments for compliance
- Implement approval workflows for adjustments above threshold
- Track reconciliation health metrics (match rate, resolution time)
- Continuously improve tolerance thresholds based on historical data

## Open-Source First Philosophy

Usage reconciliation is built on open-source foundations: PostgreSQL for persistent storage, BullMQ for job scheduling, Metabase for billing team dashboards, and the Stripe API for external data comparison. The entire reconciliation system avoids proprietary billing audit tools while providing complete auditability and transparency.
