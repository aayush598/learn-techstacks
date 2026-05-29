# Section 03: Usage-Based Billing Model

## Billing Architecture

Usage-based billing is central to our monetization strategy, capturing value proportional to customer success. The billing system must handle real-time metering, rate aggregation, invoice generation, and dunning.

```
Usage-Based Billing System Architecture
┌────────────────────────────────────────────────────────────────────┐
│                         Event Collection Layer                     │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────────┐  │
│ │ Call     │ │ SMS      │ │ Storage  │ │ API Request          │  │
│ │ Events   │ │ Events   │ │ Events   │ │ Events               │  │
│ └──────────┘ └──────────┘ └──────────┘ └──────────────────────┘  │
│       │            │            │                │                 │
│       ▼            ▼            ▼                ▼                 │
│ ┌─────────────────────────────────────────────────────────────┐   │
│ │                 Event Bus (Kafka/Redis Streams)               │   │
│ └─────────────────────────────────────────────────────────────┘   │
├────────────────────────────────────────────────────────────────────┤
│                     Metering Layer                                 │
│ ┌─────────────────────────────────────────────────────────────┐   │
│ │              Usage Metering Engine                          │   │
│ │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │   │
│ │  │ Voice    │ │ SMS      │ │ Storage  │ │ LLM Tokens   │  │   │
│ │  │ Meter    │ │ Meter    │ │ Meter    │ │ Meter        │  │   │
│ │  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │   │
│ └─────────────────────────────────────────────────────────────┘   │
├────────────────────────────────────────────────────────────────────┤
│                     Rating & Pricing Layer                         │
│ ┌─────────────────────────────────────────────────────────────┐   │
│ │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │   │
│ │  │ Tier     │ │ Volume   │ │ Committed│ │ Promo        │  │   │
│ │  │ Pricing  │ │ Discount │ │ Credits  │ │ Credits      │  │   │
│ │  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │   │
│ └─────────────────────────────────────────────────────────────┘   │
├────────────────────────────────────────────────────────────────────┤
│                     Billing & Invoicing Layer                      │
│ ┌─────────────────────────────────────────────────────────────┐   │
│ │  Invoice Generation → Payment Processing → Dunning/Retry   │   │
│ └─────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────┘
```

## Metering Units & Rates

| Service | Default Unit | Tier-Free | Tier-Starter | Tier-Pro | Tier-Business | Tier-Enterprise |
|---------|-------------|-----------|-------------|----------|---------------|-----------------|
| Voice minutes | Per minute | 100 incl. | 1K incl. | 10K incl. | 100K incl. | Custom |
| Voice overage | Per minute | N/A | $0.08 | $0.06 | $0.04 | $0.02-0.04 |
| STT processing | Per minute | Included | Included | Included | Included | Included |
| TTS generation | Per minute | Included | Included | Included | Included | Included |
| LLM inference | Per 1K tokens | 50K incl. | 500K incl. | 5M incl. | 50M incl. | Custom |
| SMS messages | Per message | N/A | N/A | $0.01 | $0.008 | $0.0075 |
| Storage | Per GB/month | 0.5 GB | 5 GB | 25 GB | 100 GB | Custom |
| API requests | Per request | 10K/mo | 100K/mo | 1M/mo | 10M/mo | Custom |

## Real-Time Usage Tracking

```typescript
interface UsageEvent {
  tenantId: string;
  userId: string;
  eventType: 'voice_minute' | 'llm_token' | 'sms_message' | 'storage_gb' | 'api_request';
  quantity: number;
  timestamp: Date;
  metadata: Record<string, string>;
}

interface UsageMeter {
  tenantId: string;
  billingPeriod: {
    start: Date;
    end: Date;
  };
  meters: {
    voiceMinutes: RunningTotal;
    llmTokens: RunningTotal;
    smsMessages: RunningTotal;
    storageGB: RunningTotal;
    apiRequests: RunningTotal;
  };
  currentTierLimits: UsageLimits;
  isOverLimit: boolean;
  overageRates: OverageRates;
}

class UsageTrackingService {
  private eventBuffer: UsageEvent[] = [];
  private flushInterval = 5000; // 5 seconds

  async trackUsage(event: UsageEvent): Promise<void> {
    this.eventBuffer.push(event);
    if (this.eventBuffer.length >= 100) {
      await this.flushEvents();
    }
  }

  private async flushEvents(): Promise<void> {
    const batch = this.eventBuffer.splice(0);
    await this.ingestBatch(batch);
    
    // Update real-time meters in Redis
    for (const event of batch) {
      await this.updateRealtimeMeter(event);
    }
    
    // Check thresholds
    for (const event of batch) {
      const meter = await this.getMeter(event.tenantId);
      if (meter.isNearLimit(0.8)) {
        await this.sendUsageAlert(event.tenantId, '80% threshold reached');
      }
      if (meter.isOverLimit) {
        await this.enforceOveragePolicy(event.tenantId);
      }
    }
  }

  async getCurrentUsage(tenantId: string, period: BillingPeriod): Promise<UsageSummary> {
    const meters = await this.aggregateMeters(tenantId, period);
    const costs = this.rateUsage(meters);
    
    return {
      meters,
      costs,
      totalCost: costs.reduce((sum, c) => sum + c.amount, 0),
      estimatedMonthly: this.projectMonthly(tenantId, meters),
    };
  }
}
```

## Overage vs Hard Cap Decision

**Approach: Soft cap with overage pricing.** Customers receive usage alerts at 80% and 100% of their limit. If they exceed the limit, service continues at overage rates (no service interruption). This maximizes revenue while maintaining customer experience.

**Trade-off:** Hard caps prevent bill shock but limit revenue. Soft caps with overage alerts give customers control while allowing us to monetize growth. Real-time usage dashboard prevents surprises.

## Billing Cycle & Invoice Generation

- **Billing cycle:** Monthly (1st-31st). Prorated for mid-cycle signups.
- **Invoice timing:** Generated on 1st of each month for previous month's usage.
- **Payment terms:** Net 7 for monthly credit card. Net 30 for annual invoices ($5K+).
- **Invoice format:** PDF via email + downloadable from dashboard.
- **Line items:** Subscription base + usage overages + marketplace purchases + credits.

```typescript
interface InvoiceLineItem {
  description: string;
  quantity: number;
  unitPrice: number;
  total: number;
  type: 'subscription' | 'usage' | 'marketplace' | 'credit' | 'adjustment';
}

function generateInvoice(tenantId: string, period: BillingPeriod): Invoice {
  const subscription = getSubscriptionCharge(tenantId, period);
  const usage = getUsageCharges(tenantId, period);
  const credits = getAppliedCredits(tenantId);
  const marketplace = getMarketplacePurchases(tenantId, period);
  
  const lineItems: InvoiceLineItem[] = [
    ...subscription,
    ...usage,
    ...marketplace.map(item => ({
      description: item.name,
      quantity: 1,
      unitPrice: item.price,
      total: item.price,
      type: 'marketplace' as const,
    })),
    ...(credits.length > 0 ? [{ description: 'Credits applied', quantity: 1, unitPrice: -credits.total, total: -credits.total, type: 'credit' as const }] : []),
  ];
  
  return {
    tenantId,
    period,
    lineItems,
    subtotal: lineItems.reduce((sum, item) => sum + item.total, 0),
    tax: calculateTax(lineItems, getTenantRegion(tenantId)),
    total: calculateTotal(lineItems),
    status: 'pending',
    dueDate: period.end.plus({ days: 7 }),
  };
}
```

## Dunning & Failed Payment Handling

**Grace period:** 3 days. **Retry schedule:** Day 0, Day 1, Day 3, then suspend. **Suspension:** Read-only dashboard, API disabled, agents paused (not deleted). **Data retention post-suspension:** 30 days before permanent deletion.

## Open Source Tools

| Tool | Purpose | Alternative |
|------|---------|-------------|
| Stripe | Payment processing | Paddle, Lemon Squeezy |
| Lago | Usage-based billing | Metronome, Chargebee |
| OpenMeter | Usage metering | Custom (PostgreSQL) |
| Invoiceninja | Invoice generation | Custom PDF generation |
| Kafka | Event streaming | RabbitMQ, Redis Streams |

## Production Considerations

- Usage events must be idempotent — deduplicate on (tenant_id, event_id, timestamp)
- Real-time metering in Redis with persistence to PostgreSQL
- Event buffer to handle traffic spikes (buffer then batch insert)
- Separate read path for dashboard (PostgreSQL aggregates) from write path (Kafka + Redis)
- Rate limit usage event ingestion per tenant (10K events/sec max)
- Budget alerts for enterprise customers (custom spending limits)

## Tools & Resources

- **Billing platform:** Stripe (primary), Lago (usage metering)
- **Usage analytics:** PostHog, Mixpanel
- **Invoice templates:** React-PDF, PDFMake
- **Tax calculation:** TaxJar, Stripe Tax
- **Revenue recognition:** Zuora, RevPro
