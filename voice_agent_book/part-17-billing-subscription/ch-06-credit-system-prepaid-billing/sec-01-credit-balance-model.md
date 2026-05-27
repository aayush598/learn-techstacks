# Section 01: Credit Balance Model

## Credit Ledger Design

The credit ledger is the system of record for prepaid balances. Every transaction — purchase, consumption, refund, expiry — is recorded as an immutable ledger entry. The current balance is derived by summing all entries.

```typescript
interface CreditLedgerEntry {
  id: string;
  tenantId: string;
  type: CreditTransactionType;
  amount: number;            // Positive = credit, Negative = debit
  balanceAfter: number;      // Running balance after this entry
  currency: string;
  description: string;
  metadata: CreditMetadata;

  // Correlation
  invoiceId?: string;
  stripePaymentIntentId?: string;
  creditPackId?: string;

  // Timing
  createdAt: string;
  effectiveAt: string;       // When the credit becomes available
  expiresAt?: string;        // When the credit expires
}

enum CreditTransactionType {
  PURCHASE = 'purchase',
  CONSUMPTION = 'consumption',
  PROMO_CREDIT = 'promo_credit',
  REFUND = 'refund',
  EXPIRY = 'expiry',
  ADJUSTMENT = 'adjustment',
  ROLLOVER = 'rollover',
  TRANSFER = 'transfer',
}

interface CreditMetadata {
  source: string;
  reference?: string;
  tags?: string[];
  notes?: string;
}

class CreditLedgerService {
  private db: Database;

  async recordTransaction(entry: Omit<CreditLedgerEntry, 'id' | 'balanceAfter'>): Promise<CreditLedgerEntry> {
    // Serialize access to prevent race conditions
    const lockKey = `credit_ledger:${entry.tenantId}`;
    const unlock = await this.acquireLock(lockKey);

    try {
      // Get current balance
      const currentBalance = await this.getBalance(entry.tenantId, entry.currency);

      // Calculate new balance
      const balanceAfter = currentBalance + entry.amount;

      if (balanceAfter < 0) {
        throw new Error('Insufficient credit balance');
      }

      // Create ledger entry
      const ledgerEntry: CreditLedgerEntry = {
        id: `cl_${nanoid(16)}`,
        ...entry,
        balanceAfter,
        createdAt: new Date().toISOString(),
      };

      await this.db.creditLedger.create(ledgerEntry);

      // Update cached balance
      await this.cacheBalance(entry.tenantId, entry.currency, balanceAfter);

      return ledgerEntry;
    } finally {
      await unlock();
    }
  }

  async getBalance(tenantId: string, currency: string = 'credits'): Promise<number> {
    // Check cache first
    const cached = await this.redis.get(`credit_balance:${tenantId}:${currency}`);
    if (cached !== null) {
      return parseFloat(cached);
    }

    // Calculate from ledger
    const result = await this.db.creditLedger.aggregate([
      { $match: { tenantId, currency } },
      { $group: { _id: null, balance: { $sum: '$amount' } } },
    ]).toArray();

    const balance = result[0]?.balance || 0;
    await this.cacheBalance(tenantId, currency, balance);
    return balance;
  }

  async getTransactionHistory(
    tenantId: string,
    options: { limit?: number; offset?: number; type?: CreditTransactionType }
  ): Promise<CreditLedgerEntry[]> {
    const query: any = { tenantId };
    if (options.type) query.type = options.type;

    return await this.db.creditLedger.find(query)
      .sort({ createdAt: -1 })
      .skip(options.offset || 0)
      .limit(options.limit || 50)
      .toArray();
  }

  private async acquireLock(key: string): Promise<() => Promise<void>> {
    const lock = await this.redis.setnx(`lock:${key}`, Date.now().toString());
    if (lock === 0) {
      // Retry with backoff
      await new Promise(resolve => setTimeout(resolve, 100));
      return this.acquireLock(key);
    }
    await this.redis.expire(`lock:${key}`, 30);

    return async () => {
      await this.redis.del(`lock:${key}`);
    };
  }

  private async cacheBalance(tenantId: string, currency: string, balance: number): Promise<void> {
    await this.redis.setex(`credit_balance:${tenantId}:${currency}`, 300, balance.toString());
  }
}
```

## Balance Per Tenant

Each tenant has an independent credit balance. The balance is stored in the tenant's currency of choice. Balances are non-transferable between tenants.

```typescript
interface TenantCreditBalance {
  tenantId: string;
  currency: string;
  balance: number;
  pendingCredits: number;    // Credits not yet available
  availableCredits: number;  // balance - pending
  lastUpdated: string;
  expirySummary: {
    expiringWithin30Days: number;
    expiringWithin60Days: number;
    expiringWithin90Days: number;
  };
}
```

## Pending vs Settled Credits

When a credit is purchased, it goes through a pending state until the payment settles. This prevents spending credits before the payment is confirmed.

```typescript
interface CreditSettlement {
  pendingEntryId: string;
  stripePaymentIntentId: string;
  status: 'pending' | 'settled' | 'failed';
  settledAt?: string;
  retryCount: number;
}

class CreditSettlementService {
  async handlePaymentSuccess(paymentIntentId: string): Promise<void> {
    // Find pending credit entries linked to this payment
    const pendingEntries = await this.db.creditLedger.find({
      stripePaymentIntentId: paymentIntentId,
      type: CreditTransactionType.PURCHASE,
    }).toArray();

    for (const entry of pendingEntries) {
      // Mark as settled — credits are now available
      await this.db.creditLedger.updateOne(
        { id: entry.id },
        { $set: { status: 'settled', settledAt: new Date().toISOString() } }
      );
    }
  }

  async handlePaymentFailure(paymentIntentId: string): Promise<void> {
    // Reverse pending credits
    const pendingEntries = await this.db.creditLedger.find({
      stripePaymentIntentId: paymentIntentId,
      type: CreditTransactionType.PURCHASE,
    }).toArray();

    for (const entry of pendingEntries) {
      // Create reversing entry
      await this.ledgerService.recordTransaction({
        tenantId: entry.tenantId,
        type: CreditTransactionType.REFUND,
        amount: -entry.amount,
        currency: entry.currency,
        description: `Reversed: ${entry.description} (payment failed)`,
        metadata: { source: 'payment_failure', reference: paymentIntentId },
      });

      // Mark original as failed
      await this.db.creditLedger.updateOne(
        { id: entry.id },
        { $set: { status: 'failed' } }
      );
    }
  }
}
```

## Concurrent Balance Updates

Credit balances must handle concurrent updates correctly. A pessimistic lock on the tenant's ledger prevents race conditions where two operations could read the same balance and both succeed with insufficient funds.

```typescript
async function deductCredits(
  tenantId: string,
  amount: number,
  description: string,
  metadata: CreditMetadata
): Promise<CreditLedgerEntry> {
  // Use Redis-based distributed lock
  const lockKey = `credit_lock:${tenantId}`;
  const lock = await redis.setnx(lockKey, '1');

  if (!lock) {
    throw new Error('Concurrent credit operation in progress');
  }

  try {
    await redis.expire(lockKey, 10);

    const balance = await getBalance(tenantId);
    if (balance < amount) {
      throw new InsufficientCreditsError(balance, amount);
    }

    return await recordTransaction({
      tenantId,
      type: CreditTransactionType.CONSUMPTION,
      amount: -amount,
      currency: 'credits',
      description,
      metadata,
      effectiveAt: new Date().toISOString(),
    });
  } finally {
    await redis.del(lockKey);
  }
}
```

## Open-Source Tools

- **PostgreSQL** — Credit ledger with ACID compliance
- **Redis** — Balance caching and distributed locking
- **BullMQ** — Schedule credit expiry processing
- **Stripe API** — Payment processing for credit purchases

## Integration Points

The credit balance model connects to the usage metering pipeline (credit consumption), the invoice system (credit application), the payment service (credit purchase), and the notification service (low balance alerts).

## Production Considerations

- Use database transactions for ledger operations
- Implement idempotency for all credit transactions
- Monitor credit balance accuracy with periodic reconciliation
- Alert on unusual credit consumption patterns
- Test concurrent balance scenarios under load

## Open-Source First Philosophy

The credit ledger is built on PostgreSQL with Redis for caching and locking — both open-source and battle-tested. BullMQ handles credit expiry scheduling. This stack avoids proprietary ledger systems (like Chargebee or Recurly's credit features) while providing full control and auditability over prepaid balances.
