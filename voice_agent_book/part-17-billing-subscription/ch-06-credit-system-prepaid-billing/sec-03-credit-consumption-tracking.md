# Section 03: Credit Consumption Tracking

## Usage Deduction from Balance

When a billable action occurs, credits are deducted from the tenant's prepaid balance. The deduction happens in real-time, synchronized with the usage metering pipeline.

```typescript
class CreditConsumptionService {
  async consumeCredits(
    tenantId: string,
    meter: string,
    quantity: number,
    unitPrice: number,       // Credits per unit
    metadata: {
      callId?: string;
      agentId?: string;
      source: string;
    }
  ): Promise<ConsumptionResult> {
    const creditsNeeded = Math.ceil(quantity * unitPrice);

    // Check balance
    const balance = await this.ledgerService.getBalance(tenantId);

    if (balance < creditsNeeded) {
      return {
        consumed: false,
        reason: 'insufficient_balance',
        balance,
        required: creditsNeeded,
        alternativeAction: 'postpaid_billing', // Fall back to postpaid
      };
    }

    // Deduct credits
    const entry = await this.ledgerService.recordTransaction({
      tenantId,
      type: CreditTransactionType.CONSUMPTION,
      amount: -creditsNeeded,
      currency: 'credits',
      description: `${meter}: ${quantity} units @ ${unitPrice} credits/unit`,
      metadata: {
        source: metadata.source,
        reference: metadata.callId,
        tags: ['consumption', meter],
      },
      effectiveAt: new Date().toISOString(),
    });

    // Check low balance threshold
    const remaining = balance - creditsNeeded;
    if (remaining < this.getLowBalanceThreshold(tenantId)) {
      await this.notificationService.sendLowBalanceWarning(
        tenantId,
        remaining
      );
    }

    return {
      consumed: true,
      balance: remaining,
      required: creditsNeeded,
      entryId: entry.id,
    };
  }

  async batchConsumeCredits(
    tenantId: string,
    items: Array<{ meter: string; quantity: number; unitPrice: number; metadata: any }>
  ): Promise<BatchConsumptionResult> {
    let totalCredits = 0;
    const results: ConsumptionResult[] = [];

    // Calculate total needed
    for (const item of items) {
      const creditsNeeded = Math.ceil(item.quantity * item.unitPrice);
      totalCredits += creditsNeeded;
    }

    // Single atomic check and deduction
    const balance = await this.ledgerService.getBalance(tenantId);
    if (balance < totalCredits) {
      // Fall back to postpaid for the entire batch
      return {
        consumed: false,
        reason: 'insufficient_balance',
        balance,
        required: totalCredits,
        fallbackToPostpaid: true,
        results: items.map(() => ({
          consumed: false,
          reason: 'insufficient_balance',
        })),
      };
    }

    // Deduct all at once
    const entry = await this.ledgerService.recordTransaction({
      tenantId,
      type: CreditTransactionType.CONSUMPTION,
      amount: -totalCredits,
      currency: 'credits',
      description: `Batch consumption: ${items.length} items`,
      metadata: {
        source: 'batch',
        tags: ['consumption', 'batch'],
      },
      effectiveAt: new Date().toISOString(),
    });

    return {
      consumed: true,
      balance: balance - totalCredits,
      required: totalCredits,
      entryId: entry.id,
      results: items.map(() => ({ consumed: true })),
    };
  }

  private getLowBalanceThreshold(tenantId: string): number {
    // Return 10% of average monthly consumption
    return 100; // Default threshold
  }
}
```

## Insufficient Credit Handling

When a tenant has insufficient credits, the system can fall back to postpaid billing (invoice-based), block the action, or prompt for credit purchase.

```typescript
async function handleInsufficientCredits(
  tenantId: string,
  creditsNeeded: number,
  balance: number
): Promise<Action> {
  const tenant = await tenantService.getTenant(tenantId);
  const plan = await planService.getTenantPlan(tenantId);

  // Check if postpaid fallback is enabled
  if (plan.features.postpaidFallback) {
    // Record as postpaid usage — will be invoiced
    await postpaidBillingService.recordUsage(tenantId, creditsNeeded);
    return { type: 'postpaid_fallback', message: 'Charged to your account' };
  }

  // Check if auto-topup is configured
  if (tenant.autoTopup?.enabled) {
    await autoTopupService.executeTopup(tenantId);
    return { type: 'auto_topup_initiated', message: 'Auto-recharging credits...' };
  }

  // Block the action
  return {
    type: 'blocked',
    message: `Insufficient credits. You need ${creditsNeeded} credits but have ${balance}.`,
    promptUrl: `${APP_URL}/billing/credits`,
  };
}
```

## Partial Consumption

For actions that consume partial credits, the system rounds up to the nearest integer credit. Partial credit accounting ensures that credits are fairly deducted for variable-length actions.

```typescript
function calculateCreditConsumption(
  durationMs: number,
  ratePerMinute: number
): number {
  // Rate is in credits per minute
  // Duration is in milliseconds
  const minutes = durationMs / 60000;
  const rawCredits = minutes * ratePerMinute;

  // Round up to nearest integer credit
  return Math.ceil(rawCredits);
}

// Example: A 45-second call at 2 credits/minute
// calculates: 0.75 min × 2 credits/min = 1.5 → ceil to 2 credits
```

## Refund Scenarios

When a service is interrupted or a call fails, consumed credits may need to be refunded. Refunds create a positive ledger entry with a reference to the original consumption.

```typescript
async function refundCredits(
  tenantId: string,
  originalConsumptionId: string,
  amount: number,
  reason: string
): Promise<CreditLedgerEntry> {
  const originalEntry = await this.db.creditLedger.findOne({
    id: originalConsumptionId,
    tenantId,
  });

  if (!originalEntry) {
    throw new Error('Original consumption entry not found');
  }

  if (amount > Math.abs(originalEntry.amount)) {
    throw new Error('Refund amount exceeds original consumption');
  }

  return await this.ledgerService.recordTransaction({
    tenantId,
    type: CreditTransactionType.REFUND,
    amount,
    currency: 'credits',
    description: `Refund: ${reason}`,
    metadata: {
      source: 'refund',
      reference: originalConsumptionId,
      tags: ['refund'],
    },
    effectiveAt: new Date().toISOString(),
  });
}
```

## Open-Source Tools

- **PostgreSQL** — Credit consumption ledger with ACID transactions
- **Redis** — Real-time balance tracking and locking
- **BullMQ** (MIT) — Queue consumption events
- **Stripe API** — Postpaid billing fallback

## Integration Points

Credit consumption connects to every billable service (voice calls, transcription, TTS), the credit ledger (balance deductions), the notification service (low balance alerts), and the postpaid billing fallback (Chapter 6 Section 8).

## Production Considerations

- Monitor credit consumption rate for anomaly detection
- Set up low balance alerts at configurable thresholds
- Implement consumption retry with exponential backoff
- Handle partial consumption for partial service delivery
- Audit credit consumption regularly for accuracy

## Open-Source First Philosophy

Credit consumption runs entirely on PostgreSQL and Redis — no proprietary metering or deduction engine required. The consumption logic is straightforward debit operations that are testable, auditable, and maintainable. This approach avoids the per-transaction costs of third-party billing platforms.
