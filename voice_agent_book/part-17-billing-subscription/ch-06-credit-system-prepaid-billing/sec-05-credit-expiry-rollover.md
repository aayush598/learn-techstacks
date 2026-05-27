# Section 05: Credit Expiry & Rollover

## Credit Expiration Policies

Credits have expiration dates to encourage usage and manage liability. Different credit types have different expiration policies:
- **Purchased credits**: Valid for 12 months
- **Promotional credits**: Valid for 30-90 days
- **Bonus credits**: Same expiry as associated purchase
- **Rolled-over credits**: Valid for an additional 3 months

```typescript
interface CreditExpiryPolicy {
  creditType: string;
  defaultValidityDays: number;
  maxValidityDays: number;
  extendable: boolean;
  extensionDays: number;
  notificationDays: number[];  // Days before expiry to notify
}

const EXPIRY_POLICIES: Record<string, CreditExpiryPolicy> = {
  purchase: {
    creditType: 'purchase',
    defaultValidityDays: 365,
    maxValidityDays: 730,
    extendable: false,
    extensionDays: 0,
    notificationDays: [30, 14, 7, 3, 1],
  },
  promo: {
    creditType: 'promo_credit',
    defaultValidityDays: 90,
    maxValidityDays: 180,
    extendable: true,
    extensionDays: 30,
    notificationDays: [14, 7, 3, 1],
  },
  rollover: {
    creditType: 'rollover',
    defaultValidityDays: 90,
    maxValidityDays: 180,
    extendable: false,
    extensionDays: 0,
    notificationDays: [14, 7, 3, 1],
  },
};

class CreditExpiryService {
  async processExpiredCredits(): Promise<void> {
    const now = new Date().toISOString();

    // Find all credits that have expired
    const expiredEntries = await this.db.creditLedger.find({
      expiresAt: { $lte: now },
      type: { $in: ['purchase', 'promo_credit', 'rollover'] },
      amount: { $gt: 0 },
      expired: { $ne: true },
    }).toArray();

    for (const entry of expiredEntries) {
      // Check if there's remaining balance in this batch
      const remainingBalance = await this.calculateRemainingBalance(entry);
      if (remainingBalance <= 0) continue;

      // Create expiry entry
      await this.ledgerService.recordTransaction({
        tenantId: entry.tenantId,
        type: CreditTransactionType.EXPIRY,
        amount: -remainingBalance,
        currency: 'credits',
        description: `Credit expiry: ${entry.description}`,
        metadata: {
          source: 'expiry',
          reference: entry.id,
          tags: ['expiry'],
        },
        effectiveAt: now,
      });

      // Mark original as expired
      await this.db.creditLedger.updateOne(
        { id: entry.id },
        { $set: { expired: true, expiredAt: now } }
      );

      // Notify tenant
      await this.notificationService.sendCreditExpiryNotice(
        entry.tenantId,
        remainingBalance
      );
    }
  }

  private async calculateRemainingBalance(entry: CreditLedgerEntry): Promise<number> {
    // Calculate how much of this batch remains unconsumed
    const totalFromBatch = await this.db.creditLedger.aggregate([
      {
        $match: {
          $or: [
            { id: entry.id },
            {
              type: CreditTransactionType.CONSUMPTION,
              'metadata.reference': entry.id,
            },
          ],
        },
      },
      { $group: { _id: null, total: { $sum: '$amount' } } },
    ]).toArray();

    return totalFromBatch[0]?.total || 0;
  }
}
```

## Use-It-Or-Lose-It vs Rollover

Two competing credit policies exist: use-it-or-lose-it (credits expire regardless) and rollover (unused credits carry forward). The optimal policy depends on customer psychology and business goals.

```
Credit Policy Comparison:
┌──────────────────────────────────────────────────────────────────┐
│ Policy          │ Pros                     │ Cons                │
├─────────────────┼──────────────────────────┼─────────────────────┤
│ Use-it-or-lose  │ Higher urgency to use    │ Customer anxiety    │
│                 │ Predictable liability    │ Perceived unfairness│
│                 │ Higher breakage revenue  │                      │
├─────────────────┼──────────────────────────┼─────────────────────┤
│ Full rollover   │ Customer friendly         │ Lower urgency       │
│                 │ Reduces churn             │ Growing liability   │
│                 │ Competitive advantage     │ Revenue deferral    │
├─────────────────┼──────────────────────────┼─────────────────────┤
│ Partial rollover│ Balanced approach         │ More complex        │
│ (50%)           │ Moderate urgency          │ Needs clear UI      │
│                 │ Manageable liability      │                      │
└──────────────────────────────────────────────────────────────────┘
```

## Automatic Consumption Order

When consuming credits, the system uses a specific ordering to minimize customer credit loss:

1. **Earliest expiring credits first** (FEFO — First Expiry, First Out)
2. **Promotional credits first** (more restrictive)
3. **Purchased credits next**
4. **Rolled-over credits last**

```typescript
class ConsumptionOrderService {
  async consumeWithExpiryAwareness(
    tenantId: string,
    amount: number,
    metadata: any
  ): Promise<void> {
    // Find all active credit batches sorted by expiry (earliest first)
    const batches = await this.db.creditLedger.find({
      tenantId,
      type: { $in: ['purchase', 'promo_credit', 'rollover'] },
      expiresAt: { $gt: new Date().toISOString() },
      amount: { $gt: 0 },
    }).sort({ expiresAt: 1, type: 1 }).toArray();

    let remainingToConsume = amount;

    for (const batch of batches) {
      if (remainingToConsume <= 0) break;

      const available = batch.amount - (batch.consumed || 0);
      if (available <= 0) continue;

      const toConsume = Math.min(available, remainingToConsume);

      // Deduct from this batch
      await this.ledgerService.recordTransaction({
        tenantId,
        type: CreditTransactionType.CONSUMPTION,
        amount: -toConsume,
        currency: 'credits',
        description: `Consumption from batch ${batch.id}`,
        metadata: {
          ...metadata,
          batchReference: batch.id,
        },
        effectiveAt: new Date().toISOString(),
      });

      // Update consumed tracking
      await this.db.creditLedger.updateOne(
        { id: batch.id },
        { $inc: { consumed: toConsume } }
      );

      remainingToConsume -= toConsume;
    }

    if (remainingToConsume > 0) {
      throw new InsufficientCreditsError(amount - remainingToConsume, amount);
    }
  }
}
```

## Rollover Processing

At the end of each period, unused credits are rolled over according to the rollover policy.

```typescript
async function processRollover(tenantId: string): Promise<void> {
  const policy = await getTenantRolloverPolicy(tenantId);

  // Find expiring credits
  const expiringSoon = await db.creditLedger.find({
    tenantId,
    type: { $in: ['purchase', 'rollover'] },
    expiresAt: {
      $lte: new Date(Date.now() + 30 * 86400000).toISOString(),
    },
    amount: { $gt: 0 },
  }).toArray();

  for (const batch of expiringSoon) {
    const remaining = batch.amount - (batch.consumed || 0);
    if (remaining <= 0) continue;

    let rolloverAmount: number;
    switch (policy) {
      case 'full':
        rolloverAmount = remaining;
        break;
      case 'partial':
        rolloverAmount = Math.floor(remaining * 0.5);
        break;
      case 'none':
        rolloverAmount = 0;
        break;
    }

    if (rolloverAmount > 0) {
      // Create rollover batch with extended expiry
      await ledgerService.recordTransaction({
        tenantId,
        type: CreditTransactionType.ROLLOVER,
        amount: rolloverAmount,
        currency: 'credits',
        description: `Rollover from batch ${batch.id}`,
        metadata: {
          source: 'rollover',
          reference: batch.id,
          tags: ['rollover'],
        },
        effectiveAt: new Date().toISOString(),
        expiresAt: new Date(Date.now() + 90 * 86400000).toISOString(),
      });
    }
  }
}
```

## Open-Source Tools

- **BullMQ** — Schedule daily credit expiry processing
- **Redis** — Cache expiry dates for fast lookup
- **PostgreSQL** — Credit batch tracking with expiry
- **Nodemailer** (MIT) — Expiry notification emails

## Integration Points

Credit expiry connects to the credit ledger (batch tracking), the notification service (expiry warnings), and the usage consumption system (consumption order).

## Production Considerations

- Run expiry processing during off-peak hours
- Notify customers 30, 14, 7, 3, and 1 day before expiry
- Monitor credit expiry impact on customer satisfaction
- Allow admin extension of credit expiry for special cases
- Track credit breakage rate as a business metric

## Open-Source First Philosophy

BullMQ handles daily credit expiry processing reliably without proprietary job schedulers. PostgreSQL tracks credit batches with expiry dates, and Redis provides fast lookups. This open-source approach provides enterprise-grade credit expiry management without specialized subscription management software.
