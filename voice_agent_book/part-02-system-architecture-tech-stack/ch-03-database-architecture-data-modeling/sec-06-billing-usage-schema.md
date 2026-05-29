# Section 06: Billing & Usage Schema

## Billing Data Model

The billing system tracks subscriptions, usage-based metering, invoices, and payments. It supports multiple pricing models (per-minute, per-call, per-seat, overage) and integrates with external payment processors.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      BILLING & USAGE SCHEMA                            │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     PLAN DEFINITIONS                            │    │
│  │                                                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │    │
│  │  │  Free        │  │  Starter     │  │  Pro         │          │    │
│  │  │  $0/mo       │  │  $29/mo      │  │  $99/mo      │          │    │
│  │  │  • 100 min   │  │  • 1000 min  │  │  • 10000 min │          │    │
│  │  │  • 1 agent   │  │  • 3 agents  │  │  • 10 agents  │          │    │
│  │  │  • 1 user    │  │  • 5 users   │  │  • 25 users   │          │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘          │    │
│  │                                                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐                              │    │
│  │  │  Business    │  │  Enterprise  │                              │    │
│  │  │  $299/mo     │  │  Custom      │                              │    │
│  │  │  • 50000 min │  │  • Unlimited │                              │    │
│  │  │  • 25 agents │  │  • Unlimited │                              │    │
│  │  │  • 100 users │  │  • Custom    │                              │    │
│  │  └──────────────┘  └──────────────┘                              │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    SUBSCRIPTIONS                                │    │
│  │                                                                  │    │
│  │  ┌─────────┬──────────┬──────────┬──────────┬──────────┬──────┐  │    │
│  │  │ tenant  │ plan     │ status   │ period   │ current  │ next │  │    │
│  │  │         │          │          │ start    │ period   │ period│  │    │
│  │  ├─────────┼──────────┼──────────┼──────────┼──────────┼──────┤  │    │
│  │  │ t_acme  │ pro      │ active   │ 2025-01  │ 2025-01  │2025-02│  │    │
│  │  │ t_beta  │ free     │ active   │ 2025-01  │ 2025-01  │2025-02│  │    │
│  │  │ t_gamma │ business │ paused   │ 2024-11  │ 2024-11  │null   │  │    │
│  │  └─────────┴──────────┴──────────┴──────────┴──────────┴──────┘  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                      USAGE RECORDS                              │    │
│  │                                                                  │    │
│  │  Hourly metering of:                                            │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │    │
│  │  │  Call Minutes │  │  STU Seconds │  │  API Calls   │          │    │
│  │  │  45 min       │  │  2700 sec    │  │  1500 req    │          │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘          │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │    │
│  │  │  Recordings  │  │  Knowledge   │  │  Team Members│          │    │
│  │  │  25 GB       │  │  Base Docs   │  │  5 active    │          │    │
│  │  │              │  │  50 docs     │  │              │          │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘          │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                      INVOICES & PAYMENTS                        │    │
│  │                                                                  │    │
│  │  ┌─────────┬──────────┬──────────┬──────────┬──────────┬──────┐  │    │
│  │  │ invoice │ tenant   │ amount   │ status   │ due_date │ paid │  │    │
│  │  │  #       │          │          │          │          │ date │  │    │
│  │  ├─────────┼──────────┼──────────┼──────────┼──────────┼──────┤  │    │
│  │  │ INV-001 │ t_acme   │ $99.00   │ paid     │ 2025-02  │ 2025 │  │    │
│  │  │ INV-002 │ t_acme   │ $112.50  │ pending  │ 2025-03  │ null │  │    │
│  │  │         │          │ (overage) │          │  -01     │      │  │    │
│  │  │ INV-003 │ t_gamma  │ $299.00  │ overdue  │ 2025-02  │ null │  │    │
│  │  └─────────┴──────────┴──────────┴──────────┴──────────┴──────┘  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Prisma Schema

```prisma
// Plan definitions (seeded data, rarely changed)
model PlanDefinition {
  id          String          @id @default(uuid()) @db.Uuid
  name        String          @unique @db.VarChar(100)
  tier        PlanTier
  description String?         @db.Text
  priceCents  Int             @map("price_cents")    // Monthly price in cents
  features    Json            @default("{}")
  limits      Json            @default("{}")
  overageRates Json           @default("{}")          // Per-unit overage pricing
  isActive    Boolean         @default(true) @map("is_active")
  sortOrder   Int             @default(0) @map("sort_order")
  createdAt   DateTime        @default(now()) @map("created_at")
  updatedAt   DateTime        @updatedAt @map("updated_at")

  subscriptions Subscription[]

  @@map("plan_definitions")
}

enum PlanTier {
  free
  starter
  pro
  business
  enterprise
}

// Plan features shape
// {
//   "call_minutes": 10000,      // Included monthly minutes
//   "agents": 10,               // Max agents
//   "team_members": 25,         // Max users
//   "api_calls_per_min": 300,   // API rate limit
//   "storage_gb": 50,           // Recording storage
//   "knowledge_bases": 10,     // Max KB documents
//   "custom_voices": true,
//   "advanced_analytics": true,
//   "white_label": false,
//   "sla": "99.9%",
//   "support": "email_chat"
// }

// Plan overage rates shape
// {
//   "call_minute_overage_cents": 0.5,    // Per minute over plan
//   "stt_second_overage_cents": 0.02,
//   "storage_gb_overage_cents": 10,
//   "api_call_overage_cents": 0.001
// }

// Subscription — one per active tenant
model Subscription {
  id               String           @id @default(uuid()) @db.Uuid
  tenantId         String           @unique @map("tenant_id") @db.Uuid
  planId           String           @map("plan_id") @db.Uuid
  status           SubscriptionStatus
  currentPeriodStart DateTime        @map("current_period_start")
  currentPeriodEnd   DateTime        @map("current_period_end")
  trialStart       DateTime?        @map("trial_start")
  trialEnd         DateTime?        @map("trial_end")
  canceledAt       DateTime?        @map("canceled_at")
  cancelAtPeriodEnd Boolean          @default(false) @map("cancel_at_period_end")
  pausedAt         DateTime?        @map("paused_at")
  resumedAt        DateTime?        @map("resumed_at")
  stripeCustomerId String?          @map("stripe_customer_id") @db.VarChar(100)
  stripeSubId      String?          @map("stripe_subscription_id") @db.VarChar(100)
  metadata         Json             @default("{}")
  createdAt        DateTime         @default(now()) @map("created_at")
  updatedAt        DateTime         @updatedAt @map("updated_at")

  tenant      Tenant        @relation(fields: [tenantId], references: [id])
  plan        PlanDefinition @relation(fields: [planId], references: [id])
  usageRecords UsageRecord[]
  invoices    Invoice[]

  @@index([tenantId])
  @@index([status, currentPeriodEnd])
  @@map("subscriptions")
}

enum SubscriptionStatus {
  trialing
  active
  past_due
  paused
  canceled
  expired
}

// Usage records — metered every hour
model UsageRecord {
  id             String   @id @default(uuid()) @db.Uuid
  tenantId       String   @map("tenant_id") @db.Uuid
  subscriptionId String   @map("subscription_id") @db.Uuid
  metric         UsageMetric
  amount         Float    // Numeric value for this metric
  unit           String   // "minutes", "seconds", "requests", "bytes"
  recordedAt     DateTime @default(now()) @map("recorded_at")
  source         String   // "call_service", "api_gateway", "storage_service"
  metadata       Json     @default("{}")

  tenant       Tenant       @relation(fields: [tenantId], references: [id])
  subscription Subscription @relation(fields: [subscriptionId], references: [id])

  @@index([tenantId, metric, recordedAt])
  @@index([subscriptionId, recordedAt])
  @@index([recordedAt])
  @@map("usage_records")
}

enum UsageMetric {
  call_minutes
  stt_seconds
  tts_characters
  api_requests
  storage_bytes
  active_agents
  team_members
  knowledge_docs
  recordings_count
}

// Invoices
model Invoice {
  id              String        @id @default(uuid()) @db.Uuid
  invoiceNumber   String        @unique @map("invoice_number") @db.VarChar(50)
  tenantId        String        @map("tenant_id") @db.Uuid
  subscriptionId  String        @map("subscription_id") @db.Uuid
  status          InvoiceStatus
  amountCents     Int           @map("amount_cents")     // Total in cents
  subtotalCents   Int           @map("subtotal_cents")
  taxCents        Int           @default(0) @map("tax_cents")
  currency        String        @default("USD") @db.VarChar(3)
  periodStart     DateTime      @map("period_start")
  periodEnd       DateTime      @map("period_end")
  dueDate         DateTime      @map("due_date")
  paidAt          DateTime?     @map("paid_at")
  stripeInvoiceId String?       @map("stripe_invoice_id") @db.VarChar(100)
  hostedUrl       String?       @map("hosted_url") @db.VarChar(500)
  pdfUrl          String?       @map("pdf_url") @db.VarChar(500)
  lineItems       Json          @default("[]")     // Array of line items
  metadata        Json          @default("{}")
  createdAt       DateTime      @default(now()) @map("created_at")
  updatedAt       DateTime      @updatedAt @map("updated_at")

  tenant       Tenant       @relation(fields: [tenantId], references: [id])
  subscription Subscription @relation(fields: [subscriptionId], references: [id])
  payments     Payment[]

  @@index([tenantId, status])
  @@index([tenantId, createdAt])
  @@index([dueDate, status])
  @@map("invoices")
}

enum InvoiceStatus {
  draft
  open
  paid
  past_due
  uncollectable
  void
}

// Line item shape
// {
//   "items": [
//     {
//       "description": "Pro Plan - Monthly",
//       "amount_cents": 9900,
//       "quantity": 1,
//       "type": "subscription"
//     },
//     {
//       "description": "Overage - Call Minutes (1,250 min @ $0.005/min)",
//       "amount_cents": 625,
//       "quantity": 1250,
//       "unit_price_cents": 0.5,
//       "type": "overage"
//     },
//     {
//       "description": "Storage over 50GB (25GB @ $0.10/GB)",
//       "amount_cents": 250,
//       "quantity": 25,
//       "unit_price_cents": 10,
//       "type": "overage"
//     }
//   ]
// }

// Payments
model Payment {
  id               String         @id @default(uuid()) @db.Uuid
  invoiceId        String         @map("invoice_id") @db.Uuid
  amountCents      Int            @map("amount_cents")
  currency         String         @default("USD") @db.VarChar(3)
  status           PaymentStatus
  paymentMethod    PaymentMethod
  stripePaymentId  String?        @map("stripe_payment_id") @db.VarChar(100)
  failureMessage   String?        @map("failure_message") @db.Text
  paidAt           DateTime?      @map("paid_at")
  createdAt        DateTime       @default(now()) @map("created_at")

  invoice Invoice @relation(fields: [invoiceId], references: [id])

  @@index([invoiceId])
  @@map("payments")
}

enum PaymentStatus {
  pending
  succeeded
  failed
  refunded
  partially_refunded
}

enum PaymentMethod {
  credit_card
  ach
  wire_transfer
  invoice
}
```

## Usage Metering

```typescript
// lib/billing/usage-meter.ts
import { prisma } from '@/lib/db'
import { redis } from '@/lib/redis'

export async function recordUsage(
  tenantId: string,
  metric: UsageMetric,
  amount: number,
  unit: string,
  source: string,
  metadata?: Record<string, unknown>
) {
  const subscription = await prisma.subscription.findUnique({
    where: { tenantId },
    include: { plan: true }
  })

  if (!subscription || subscription.status !== 'active') {
    // Don't record usage for inactive subscriptions
    return
  }

  // Write to PostgreSQL (source of truth)
  await prisma.usageRecord.create({
    data: {
      tenantId,
      subscriptionId: subscription.id,
      metric,
      amount,
      unit,
      source,
      metadata: metadata ?? {}
    }
  })

  // Update Redis counters for real-time dashboard
  const today = new Date().toISOString().split('T')[0]
  const keys = [
    `usage:${tenantId}:${metric}:${today}`,
    `usage:${tenantId}:${metric}:total`
  ]

  const pipeline = redis.pipeline()
  keys.forEach(key => pipeline.incrByFloat(key, amount))
  pipeline.expire(keys[0], 86400 * 90) // 90 day TTL for daily
  await pipeline.exec()

  // Check if approaching limits and alert
  await checkUsageLimits(subscription, metric)
}

export async function getCurrentUsage(
  tenantId: string,
  metric: UsageMetric
): Promise<number> {
  const today = new Date().toISOString().split('T')[0]
  const cached = await redis.get(`usage:${tenantId}:${metric}:${today}`)
  if (cached) return parseFloat(cached)

  // Fallback to DB aggregation
  const result = await prisma.usageRecord.aggregate({
    where: {
      tenantId,
      metric,
      recordedAt: { gte: new Date(today) }
    },
    _sum: { amount: true }
  })

  return result._sum.amount ?? 0
}

async function checkUsageLimits(
  subscription: Subscription & { plan: PlanDefinition },
  metric: UsageMetric
) {
  const limits = subscription.plan.limits as Record<string, number>
  const metricKey = metric.toLowerCase()
  const limit = limits[metricKey]
  if (!limit) return

  const currentUsage = await getCurrentUsage(
    subscription.tenantId,
    metric
  )

  // Alert at 80%, 90%, and 100% of limit
  const thresholds = [0.8, 0.9, 1.0]
  for (const threshold of thresholds) {
    if (currentUsage >= limit * threshold && currentUsage < limit * (threshold + 0.01)) {
      // Send notification (async)
      await notifyUsageThreshold(subscription.tenantId, metric, currentUsage, limit)
    }
  }
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Pricing Storage | Cents (integer) | Avoid floating point precision issues |
| Metering | Hourly buckets in PostgreSQL + Redis counters | Accurate + fast real-time display |
| Payment Processor | Stripe (primary), invoices (backup) | Industry standard, webhook integration |
| Plan Features | JSON column | Flexible feature sets, no schema per plan |
| Overage | Prorated per usage record | Fair billing, granular tracking |

## Integration Points

- **Part 17 (Billing & Subscription)** — Full billing implementation
- **Part 11 (Analytics)** — Usage data powers billing analytics
- **Part 07 (API Gateway)** — Rate limits tied to plan tier
- **Part 20 (Notifications)** — Usage threshold alerts

## Production Considerations

- **Data Volume**: Usage records at ~100M+ per month; partition by month in ClickHouse
- **Accuracy**: Usage metering is eventually consistent; PostgreSQL is source of truth
- **Cost Protection**: Maximum usage cap per tenant (configurable) prevents runaway costs
- **Retry Logic**: Failed usage writes retried via BullMQ with exponential backoff
- **Audit Trail**: All billing changes logged immutably
- **Free Tier Limits**: Hard-enforced at API gateway and service layer
