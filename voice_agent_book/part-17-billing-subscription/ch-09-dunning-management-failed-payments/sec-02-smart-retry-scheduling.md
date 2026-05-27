# Section 02: Smart Retry Scheduling

## Exponential Backoff Retry

Smart retry scheduling uses exponential backoff aligned with card network retry windows to maximize recovery probability.

```
[Payment Failed]
    ↓
[Analyze Failure Reason]
    ├── Insufficient funds → Retry in 2-3 days
    ├── Card expired → Request new card
    ├── Card declined → Check retry window
    ├── Network error → Retry in minutes
    └── Fraud block → No retry (manual review)
    ↓
[Calculate Backoff]
    ├── base = 1 hour
    ├── multiplier = 2
    ├── max = 168 hours (7 days)
    └── jitter = random(0, 0.3 * delay)
    ↓
[Pick Optimal Window]
    ├── Card network preferred times
    ├── Customer timezone
    └── Business hours consideration
    ↓
[Schedule Retry]
    └── BullMQ delayed job
```

```typescript
interface RetryConfig {
  maxAttempts: number;
  baseDelayMs: number;
  multiplier: number;
  maxDelayMs: number;
  jitterFactor: number;
  networkWindows: NetworkRetryWindow[];
  failureTypeOverrides: Record<string, Partial<RetryConfig>>;
}

interface NetworkRetryWindow {
  network: 'visa' | 'mastercard' | 'amex' | 'discover';
  minDelayHours: number;
  maxDelayHours: number;
  preferredHourUTC: number;
  maxAttemptsPerWindow: number;
}

class SmartRetryScheduler {
  private config: RetryConfig = {
    maxAttempts: 5,
    baseDelayMs: 3600000,        // 1 hour
    multiplier: 2,
    maxDelayMs: 604800000,       // 7 days
    jitterFactor: 0.3,
    networkWindows: [
      { network: 'visa', minDelayHours: 0, maxDelayHours: 168, preferredHourUTC: 14, maxAttemptsPerWindow: 3 },
      { network: 'mastercard', minDelayHours: 0, maxDelayHours: 168, preferredHourUTC: 15, maxAttemptsPerWindow: 5 },
      { network: 'amex', minDelayHours: 2, maxDelayHours: 72, preferredHourUTC: 10, maxAttemptsPerWindow: 3 },
      { network: 'discover', minDelayHours: 0, maxDelayHours: 168, preferredHourUTC: 12, maxAttemptsPerWindow: 3 },
    ],
    failureTypeOverrides: {
      insufficient_funds: { baseDelayMs: 86400000, maxAttempts: 3 },     // 24 hours base
      card_expired: { maxAttempts: 0 },                                   // No retry
      fraud_block: { maxAttempts: 0 },                                    // No retry
      network_error: { baseDelayMs: 300000, maxAttempts: 10 },            // 5 minutes base
      processing_error: { baseDelayMs: 3600000, multiplier: 1.5 },
    },
  };

  async calculateNextRetry(
    failure: PaymentFailure,
    attemptNumber: number
  ): Promise<RetryDecision> {
    // Get failure-specific overrides
    const overrides = this.config.failureTypeOverrides[failure.reason];
    if (overrides?.maxAttempts === 0) {
      return { shouldRetry: false, reason: 'no_retry_for_failure_type' };
    }

    if (attemptNumber >= (overrides?.maxAttempts ?? this.config.maxAttempts)) {
      return { shouldRetry: false, reason: 'max_attempts_reached' };
    }

    // Calculate exponential backoff with overrides
    const baseDelay = overrides?.baseDelayMs ?? this.config.baseDelayMs;
    const multiplier = overrides?.multiplier ?? this.config.multiplier;
    const maxDelay = this.config.maxDelayMs;

    let delayMs = baseDelay * Math.pow(multiplier, attemptNumber - 1);

    // Add jitter
    const jitter = delayMs * this.config.jitterFactor * Math.random();
    delayMs = Math.min(delayMs + jitter, maxDelay);

    // Align with card network window
    const networkWindow = this.getNetworkWindow(failure.cardNetwork);
    delayMs = this.alignToRetryWindow(delayMs, networkWindow);

    const retryAt = new Date(Date.now() + delayMs);

    return {
      shouldRetry: true,
      delayMs: Math.round(delayMs),
      retryAt: retryAt.toISOString(),
      networkWindow: failure.cardNetwork,
      attemptNumber: attemptNumber + 1,
    };
  }

  private alignToRetryWindow(
    delayMs: number,
    window: NetworkRetryWindow
  ): number {
    const now = new Date();
    const proposedTime = new Date(now.getTime() + delayMs);

    // Adjust to preferred hour if outside business hours
    proposedTime.setUTCHours(window.preferredHourUTC, 0, 0, 0);

    if (proposedTime.getTime() <= now.getTime()) {
      proposedTime.setUTCDate(proposedTime.getUTCDate() + 1);
    }

    return proposedTime.getTime() - now.getTime();
  }

  private getNetwork(cardBrand: string): NetworkRetryWindow | undefined {
    return this.config.networkWindows.find(w => w.network === cardBrand.toLowerCase());
  }
}
```

## Card Network Retry Windows

Different card networks have specific rules about retry timing and frequency.

```typescript
interface CardNetworkRules {
  network: string;
  maxRetriesPerDay: number;
  minIntervalHours: number;
  preferredTimes: number[];     // UTC hours
  coolDownPeriod: number;       // Hours after success
}

const CARD_NETWORK_RULES: Record<string, CardNetworkRules> = {
  visa: {
    network: 'visa',
    maxRetriesPerDay: 3,
    minIntervalHours: 0,
    preferredTimes: [10, 14, 18],
    coolDownPeriod: 24,
  },
  mastercard: {
    network: 'mastercard',
    maxRetriesPerDay: 5,
    minIntervalHours: 0,
    preferredTimes: [9, 12, 15, 18, 21],
    coolDownPeriod: 24,
  },
  amex: {
    network: 'amex',
    maxRetriesPerDay: 3,
    minIntervalHours: 2,
    preferredTimes: [8, 12, 16],
    coolDownPeriod: 48,
  },
};

async function shouldRetryBasedOnNetwork(
  failure: PaymentFailure,
  attemptHistory: PaymentAttempt[]
): Promise<boolean> {
  const rules = CARD_NETWORK_RULES[failure.cardBrand];
  if (!rules) return true; // Unknown network, allow retry

  // Check daily limit
  const todayAttempts = attemptHistory.filter(
    a => a.cardBrand === failure.cardBrand
      && isSameDay(new Date(a.attemptedAt), new Date())
  ).length;

  if (todayAttempts >= rules.maxRetriesPerDay) return false;

  return true;
}
```

## Optimal Retry Times

Retry timing considers customer behavior patterns and business hours.

```typescript
interface OptimalRetryTime {
  hourUTC: number;
  dayOfWeek: number;             // 0=Sunday, 6=Saturday
  weight: number;                // Success probability weight
  reason: string;
}

function getOptimalRetryTimes(customer: Customer): OptimalRetryTime[] {
  const timezone = customer.timezone || 'UTC';
  const offset = getTimezoneOffset(timezone);

  // Business hours in customer's timezone
  return [
    {
      hourUTC: getUTCHour(9, offset),   // 9 AM local
      dayOfWeek: getCurrentDayOfWeek(offset),
      weight: 1.0,
      reason: 'morning_business_hours',
    },
    {
      hourUTC: getUTCHour(12, offset),  // Noon local
      dayOfWeek: getCurrentDayOfWeek(offset),
      weight: 0.9,
      reason: 'lunch_hour',
    },
    {
      hourUTC: getUTCHour(15, offset),  // 3 PM local
      dayOfWeek: getCurrentDayOfWeek(offset),
      weight: 0.85,
      reason: 'afternoon_window',
    },
    {
      hourUTC: getUTCHour(19, offset),  // 7 PM local
      dayOfWeek: getCurrentDayOfWeek(offset),
      weight: 0.7,
      reason: 'evening_window',
    },
  ];
}

async function scheduleRetryAtOptimalTime(
  payment: PendingPayment,
  failure: PaymentFailure
): Promise<void> {
  const customer = await getCustomer(payment.customerId);
  const optimalTimes = getOptimalRetryTimes(customer);
  const bestTime = optimalTimes.reduce((a, b) => a.weight > b.weight ? a : b);

  // Schedule via BullMQ with specific time
  await paymentRetryQueue.add(
    'retry-payment',
    { paymentId: payment.id, attemptNumber: failure.attemptNumber + 1 },
    {
      delay: calculateDelayUntil(bestTime.hourUTC),
      attempts: 1,              // BullMQ will not auto-retry, we handle scheduling
      backoff: { type: 'fixed', delay: 0 },
    }
  );
}
```

## Max Retry Limits

```typescript
interface RetryLimitConfig {
  absoluteMaxAttempts: number;
  maxDaysFromFirstFailure: number;
  maxTotalRetryWindowDays: number;
  limitsByFailureReason: Record<string, number>;
}

const RETRY_LIMITS: RetryLimitConfig = {
  absoluteMaxAttempts: 10,
  maxDaysFromFirstFailure: 30,
  maxTotalRetryWindowDays: 45,
  limitsByFailureReason: {
    insufficient_funds: 5,
    card_declined: 3,
    processing_error: 8,
    network_error: 10,
    lost_card: 0,
    stolen_card: 0,
    fraud_block: 0,
    expired_card: 0,
    invalid_cvv: 2,
  },
};

function shouldStopRetry(failure: PaymentFailure): StopRetryReason | null {
  const limits = RETRY_LIMITS;
  if (failure.attemptNumber >= limits.absoluteMaxAttempts) {
    return { stop: true, reason: 'Absolute max attempts reached', escalate: true };
  }

  const daysSinceFirstFailure = daysBetween(failure.firstFailedAt, new Date());
  if (daysSinceFirstFailure >= limits.maxDaysFromFirstFailure) {
    return { stop: true, reason: 'Retry window expired', escalate: true };
  }

  const reasonLimit = limits.limitsByFailureReason[failure.reason];
  if (reasonLimit !== undefined && failure.attemptNumber >= reasonLimit) {
    return { stop: true, reason: `Max retries for failure type: ${failure.reason}`, escalate: false };
  }

  return null;
}
```

## Open-Source Tools

- **BullMQ** — Delayed job scheduling for retry timing
- **Redis** — Retry state and rate limiting
- **PostgreSQL** — Retry history and analytics
- **node-schedule** (MIT) — Cron-based retry scheduling
- **OpenTelemetry** — Retry attempt tracing and monitoring

## Integration Points

Smart retry scheduling integrates with the payment gateway (retry execution), dunning workflow (stage transition), customer notification (retry attempt alerts), and monitoring (retry metrics).

## Production Considerations

- Always add jitter to prevent thundering herd problems
- Respect card network retry rules to avoid blacklisting
- Track retry success rates by failure reason and card network
- Implement circuit breaker for persistent failures
- Alert on abnormal retry patterns (possible fraud)
- Consider customer timezone for optimal delivery
- Store full retry decision audit trail
- Handle concurrent payment updates gracefully

## Open-Source First Philosophy

BullMQ's delayed job scheduling provides precise retry timing without external dependencies. Redis handles rate limiting and retry state with sub-millisecond latency. PostgreSQL stores the complete retry audit trail for compliance. This stack delivers enterprise-grade smart retry scheduling without proprietary payment recovery solutions like Stripe Billing's smart retries or Recurly's dunning engine.
