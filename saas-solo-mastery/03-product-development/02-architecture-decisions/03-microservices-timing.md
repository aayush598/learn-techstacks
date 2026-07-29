# When to Migrate to Microservices (If Ever)

## The Microservices Reality Check

Microservices are not an upgrade. They are a trade-off. You trade simplicity for flexibility, monolith complexity for distributed complexity, and development speed for operational overhead. The decision to migrate should be driven by concrete, measurable problems — not by fear of future scale or desire for "modern architecture."

This guide covers the specific signals that indicate it's time to migrate, the migration strategy that minimizes risk, and how to make the transition without breaking your business.

## The Truth About Microservices

### What You Actually Get

```
What marketing promised:
  - "Easier to maintain"
  - "Faster development"
  - "Automatically scalable"
  - "More reliable"

What you actually get:
  - Independent deployability
  - Independent scalability
  - Technology diversity
  - Team ownership boundaries
  - Failure isolation

The hidden costs:
  - Network latency between services
  - Distributed data consistency
  - Debugging across service boundaries
  - Deployment coordination
  - Service discovery complexity
  - Testing across services
  - Monitoring and observability overhead
  - Duplicated infrastructure
  - Operational complexity
```

### The Solo Founder's Math

For a solo founder, microservices math rarely works out:

```
Cost of Monolith (10k users, 1 developer):
  Development speed: VERY FAST (one codebase, one deploy)
  Infrastructure: $20-50/mo (one server + database)
  Operations: 2 hours/week (deployments, monitoring)
  Debugging: Minutes (single process, single log stream)

Cost of Microservices (10k users, 1 developer):
  Development speed: SLOW (context switching between services)
  Infrastructure: $200-500/mo (multiple servers, LB, service mesh)
  Operations: 10+ hours/week (deploy multiple services)
  Debugging: Hours (tracing across services, correlating logs)

Net benefit of microservices at 10k users: NEGATIVE
```

## Signals That It's Time to Migrate

### Signal 1: Team Scaling

Your team has grown to 3+ developers and you're stepping on each other's toes.

```
The Signal:
  - Merge conflicts are frequent (every PR touches the same files)
  - Deployments are blocked by one team's changes
  - Developers need to understand the entire codebase to make changes
  - Code reviews are slow because PRs are too large

The Threshold:
  - 3+ developers working on the same codebase
  - Deployment cadence > 1 per day
  - Average PR size > 500 lines

The Solution:
  - Extract services aligned with team boundaries
  - Each team owns one or more services
  - Teams can deploy independently
```

### Signal 2: Scalability Bottlenecks

One part of your system has different scaling requirements than the rest.

```
The Signal:
  - Background job processing is slow, but web responses are fine
  - Search queries are resource-intensive but CRUD operations are light
  - Report generation takes 30 seconds, blocking other requests
  - One endpoint gets 100x more traffic than others

The Threshold:
  - One component requires 10x more resources than others
  - Scaling the monolith for one component wastes resources on others
  - Response time variance > 5x between different endpoints

The Solution:
  - Extract the hot path into a separate service
  - Scale only the hot service independently
  - Keep the rest as a monolith
```

### Signal 3: Deployment Frequency Conflicts

Different parts of the system change at different speeds.

```
The Signal:
  - API changes need immediate deployment, frontend changes are weekly
  - Background job changes have different testing requirements
  - Admin tool changes don't need same QA as customer-facing
  - A bug fix for one feature requires full regression testing

The Threshold:
  - Different parts have > 2x deployment frequency difference
  - Full regression suite takes > 30 minutes
  - Stakeholders have conflicting deployment schedules

The Solution:
  - Extract fast-moving components into separate services
  - Fast-movers deploy daily, slow-movers deploy weekly
  - Each service has its own deployment pipeline
```

### Signal 4: Data Isolation Requirements

Different parts of your system have different data needs or compliance.

```
The Signal:
  - Billing data has compliance requirements (PCI, SOC2) others don't
  - User data has different backup requirements than analytics
  - Some data needs to be encrypted differently
  - Data retention policies vary by dataset

The Threshold:
  - Compliance applies to only a subset of data
  - Different schemas have fundamentally different access patterns
  - GDPR deletion requests complicated by shared database

The Solution:
  - Extract compliant services with dedicated databases
  - Apply security controls only where needed
  - Simplify compliance scope
```

### Signal 5: Failure Isolation

A bug in one feature brings down the entire application.

```
The Signal:
  - Uncaught exception in reporting crashes payment endpoint
  - Memory leak in background jobs affects web request latency
  - Admin panel bug causes DB connection pool exhaustion
  - Feature A's dependency failure makes Feature B unavailable

The Threshold:
  - Any crash takes down the entire application
  - Mean time to recover (MTTR) > 30 minutes
  - Incident blast radius includes unrelated features

The Solution:
  - Isolate critical paths (payment, auth) into separate services
  - Implement bulkheads (separate thread pools, connection pools)
  - Extract high-risk features into isolated services
```

### Signal 6: Technology Lock-In

You need different technologies for different parts of the system.

```
The Signal:
  - Need a graph database for one feature but Postgres for everything else
  - ML models need Python but your stack is Node.js
  - Real-time needs WebSockets but main app is request-response
  - Want to try a new framework without rewriting everything

The Threshold:
  - The new technology provides > 10x improvement for a use case
  - Spending significant time fighting existing tech limitations
  - Tech constraint blocks a feature customers are asking for

The Solution:
  - Extract the tech-specific component into its own service
  - Use the right tool for the job
  - Keep the monolith for everything else
```

## The Migration Decision Matrix

Score your situation to determine if migration is warranted:

```
| Signal                          | Weight | Score (0-5) | Weighted |
|---|---|---|---|
| Team scaling issues             | 3      | [Score]     | [WxS]    |
| Scalability bottlenecks         | 2      | [Score]     | [WxS]    |
| Deployment frequency conflicts  | 2      | [Score]     | [WxS]    |
| Data isolation requirements     | 1      | [Score]     | [WxS]    |
| Failure isolation issues        | 2      | [Score]     | [WxS]    |
| Technology lock-in              | 1      | [Score]     | [WxS]    |
| Total                           | 11     |             | [Total]  |

Scoring:
0 = Not a problem at all
1 = Minor annoyance
2 = Noticeable friction
3 = Significant problem
4 = Critical issue
5 = Business-threatening

Results:
< 15  = Stay monolithic. Not worth migrating.
15-25 = Consider migrating the highest-scoring component only.
> 25  = Migration is justified. Start planning.
```

## The Incremental Extraction Strategy

### Overview

The safest way to migrate from monolith to microservices is incrementally — one service at a time. This is the "Strangler Fig" pattern.

```
Phase 0: Before Migration
  +-------------------------------------------+
  |               Monolith                     |
  |  [Auth] [Billing] [Core] [Reports]        |
  |              [Database]                    |
  +-------------------------------------------+

Phase 1: Extract First Service
  +------------+  +---------------------------+
  |  Billing   |  |         Monolith          |
  |  Service   |  | [Auth] [Core] [Reports]   |
  |  [DB]      |  |        [Main DB]          |
  +------------+  +---------------------------+

Phase 2: Extract Second Service
  +------------+  +----------+  +-------------+
  |  Billing   |  |   Auth   |  |  Monolith   |
  |  Service   |  |  Service |  | [Core]      |
  |  [DB]      |  |  [DB]    |  | [Reports]   |
  +------------+  +----------+  | [Main DB]   |
                                +-------------+

Phase 3: Continue Extracting
  +----------+  +--------+  +--------+  +--------+
  | Billing  |  |  Auth  |  |  Core  |  | Reports|
  | Service  |  |Service |  |Service |  |Service |
  | [DB]     |  | [DB]   |  | [DB]   |  | [DB]   |
  +----------+  +--------+  +--------+  +--------+
```

### Step-by-Step Extraction Process

#### Step 1: Identify the Extraction Candidate

Choose the right first service to extract.

```
Best First Extraction Candidates:
1. Billing/Payments - Clear boundary, compliance-driven
2. Authentication - Well-understood, stable interface
3. Background jobs - Different scaling profile
4. Notifications - Async, fire-and-forget

Worst First Extraction Candidates:
1. Core business logic - Tightly coupled, high risk
2. Search - Complex, heavy dependencies
3. Reporting - Read-heavy but tightly coupled
4. Admin features - Low value, don't need independent scaling
```

#### Step 2: Define the Service Boundary

Identify what the service owns:

```
Service: Billing

Owns:
  - Subscription management
  - Invoice generation
  - Payment processing
  - Billing data (dedicated database)

Does NOT Own:
  - User profiles (owned by Auth)
  - Feature access (owned by Core)
  - Usage metrics (owned by Analytics)

External Dependencies:
  - Stripe API
  - Email service (for invoices)
```

#### Step 3: Create the Service Contract

Define the API contract between monolith and the new service:

```typescript
// contracts/billing-service.ts
interface BillingServiceContract {
  createSubscription(
    userId: string, planId: string, paymentMethodId: string
  ): Promise<SubscriptionDTO>;
  cancelSubscription(subscriptionId: string): Promise<void>;
  changePlan(subscriptionId: string, newPlanId: string): Promise<SubscriptionDTO>;
  getSubscription(userId: string): Promise<SubscriptionDTO | null>;
  listInvoices(userId: string, page: number, limit: number): Promise<PaginatedResult<InvoiceDTO>>;
  getInvoice(invoiceId: string): Promise<InvoiceDTO>;
  downloadInvoice(invoiceId: string): Promise<Buffer>;
  handleStripeWebhook(payload: unknown, signature: string): Promise<void>;
  health(): Promise<HealthDTO>;
}

interface SubscriptionDTO {
  id: string;
  userId: string;
  planId: string;
  status: 'active' | 'canceled' | 'past_due' | 'incomplete' | 'trialing';
  currentPeriodStart: string;
  currentPeriodEnd: string;
  cancelAtPeriodEnd: boolean;
}

interface InvoiceDTO {
  id: string;
  amountCents: number;
  currency: string;
  status: 'paid' | 'open' | 'void' | 'uncollectible';
  paidAt: string | null;
  pdfUrl: string | null;
}

interface HealthDTO {
  status: 'healthy' | 'degraded' | 'unhealthy';
  database: 'connected' | 'disconnected';
  uptime: number;
}
```

#### Step 4: Implement the Service Alongside the Monolith

Build the new service while the monolith still handles billing:

```typescript
// billing-service/src/handlers/createSubscription.ts
import { Request, Response } from 'express';
import { SubscriptionService } from '../domain/SubscriptionService';

export async function createSubscription(req: Request, res: Response) {
  const { userId, planId, paymentMethodId } = req.body;
  try {
    const subscription = await SubscriptionService.create(
      userId, planId, paymentMethodId
    );
    res.status(201).json(subscription);
  } catch (error) {
    if (error instanceof InvalidPlanError) {
      return res.status(400).json({ error: 'Invalid plan' });
    }
    if (error instanceof PaymentError) {
      return res.status(402).json({ error: 'Payment failed' });
    }
    console.error('createSubscription error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}
```

```typescript
// monolith/src/services/BillingService.ts (temporary)
// Calls the new billing service via HTTP
class BillingService {
  private baseUrl = process.env.BILLING_SERVICE_URL;

  async createSubscription(
    userId: string, planId: string, paymentMethodId: string
  ) {
    const response = await fetch(`${this.baseUrl}/subscriptions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userId, planId, paymentMethodId }),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error);
    }
    return response.json();
  }

  async cancelSubscription(subscriptionId: string) {
    const response = await fetch(
      `${this.baseUrl}/subscriptions/${subscriptionId}/cancel`,
      { method: 'POST' }
    );
    if (!response.ok) throw new Error('Failed to cancel subscription');
  }
}
```

#### Step 5: Data Migration

The most complex part — moving data to the new service's database.

```typescript
// migration-scripts/extract-billing-data.ts
import { Pool } from 'pg';

const sourcePool = new Pool({ connectionString: process.env.MONOLITH_DB_URL });
const targetPool = new Pool({ connectionString: process.env.BILLING_DB_URL });

async function migrateBillingData() {
  const client = sourcePool.connect();
  try {
    // 1. Migrate subscriptions
    const subscriptions = await sourcePool.query(
      'SELECT * FROM billing.subscriptions'
    );
    for (const sub of subscriptions.rows) {
      await targetPool.query(
        `INSERT INTO subscriptions (id, user_id, plan_id, status,
          current_period_start, current_period_end, cancel_at_period_end,
          created_at, updated_at)
         VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
         ON CONFLICT (id) DO NOTHING`,
        [sub.id, sub.user_id, sub.plan_id, sub.status,
         sub.current_period_start, sub.current_period_end,
         sub.cancel_at_period_end, sub.created_at, sub.updated_at]
      );
    }

    // 2. Migrate invoices
    const invoices = await sourcePool.query(
      'SELECT * FROM billing.invoices'
    );
    for (const inv of invoices.rows) {
      await targetPool.query(
        `INSERT INTO invoices (id, subscription_id, amount_cents,
          currency, status, paid_at, pdf_url, created_at)
         VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
         ON CONFLICT (id) DO NOTHING`,
        [inv.id, inv.subscription_id, inv.amount_cents,
         inv.currency, inv.status, inv.paid_at, inv.pdf_url, inv.created_at]
      );
    }

    console.log(`Migrated ${subscriptions.rows.length} subscriptions`);
    console.log(`Migrated ${invoices.rows.length} invoices`);
  } finally {
    client.release();
  }
}

migrateBillingData().catch(console.error);
```

### Step 6: Dual-Write Phase

Run both systems in parallel to verify consistency:

```typescript
// monolith/src/services/BillingService.ts (dual-write version)
class BillingService {
  private remoteUrl = process.env.BILLING_SERVICE_URL;
  private dualWrite = true; // Feature flag

  async createSubscription(userId: string, planId: string) {
    // Always write to monolith DB (source of truth during migration)
    const localResult = await this.localCreateSubscription(userId, planId);

    // Also write to remote service if dual-write is enabled
    if (this.dualWrite) {
      try {
        await fetch(`${this.remoteUrl}/subscriptions`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ userId, planId }),
        });
      } catch (error) {
        // Log but don't fail - monolith is still the source of truth
        console.error('Dual-write to billing service failed:', error);
        // Queue for retry
        await this.queueDualWriteRetry('createSubscription', { userId, planId });
      }
    }

    return localResult;
  }

  private async queueDualWriteRetry(operation: string, data: any) {
    await db.query(
      `INSERT INTO dual_write_queue (operation, payload) VALUES ($1, $2)`,
      [operation, JSON.stringify(data)]
    );
  }
}
```

#### Step 7: Switch Reads

Once dual-writes are verified consistent, switch read operations:

```typescript
// monolith/src/services/BillingService.ts (read from new service)
class BillingService {
  private remoteUrl = process.env.BILLING_SERVICE_URL;
  private readFromRemote = false; // Toggle when ready

  async getSubscription(userId: string) {
    if (this.readFromRemote) {
      const response = await fetch(
        `${this.remoteUrl}/subscriptions/${userId}`
      );
      if (!response.ok) {
        // Fallback to local if remote fails
        return this.localGetSubscription(userId);
      }
      return response.json();
    }
    return this.localGetSubscription(userId);
  }
}
```

#### Step 8: Switch Writes

Finally, switch write operations. Now the new service is the source of truth:

```typescript
// monolith/src/services/BillingService.ts (all operations go to remote)
class BillingService {
  private remoteUrl = process.env.BILLING_SERVICE_URL;

  async createSubscription(userId: string, planId: string) {
    const response = await fetch(`${this.remoteUrl}/subscriptions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userId, planId }),
    });
    if (!response.ok) throw new Error('Failed to create subscription');
    return response.json();
  }

  // All billing operations now go to the remote service
  // Local database calls removed
}
```

#### Step 9: Clean Up Old Code

Remove the old billing code from the monolith:

```
Files to Remove:
  monolith/src/services/billing/
  monolith/src/controllers/billing/
  monolith/src/models/billing/
  monolith/db/migrations/billing/

Tables to Remove:
  billing.subscriptions
  billing.invoices
  billing.payment_methods
```

### Phase Timelines

Realistic timeline for extracting one service:

```
Week 1-2: Design and implement the new service
  - Service boundaries defined
  - API contract designed
  - Service implemented with its own database
  - Tests pass for the new service

Week 3: Data migration and dual-write
  - Data migrated from monolith to new service
  - Dual-write implemented in monolith
  - Consistency verified

Week 4: Switch reads
  - Read operations point to new service
  - Monitor for errors
  - Fix any issues

Week 5: Switch writes
  - Write operations point to new service
  - Old writes disabled
  - Monitor for errors

Week 6: Cleanup
  - Old code removed from monolith
  - Old tables dropped
  - Documentation updated
  - Team trained on new service
```

Total: 6 weeks for one service extraction. Plan accordingly.

## The Anti-Corruption Layer Pattern

When connecting a new microservice to an existing monolith, use an anti-corruption layer to translate between the old and new systems:

```typescript
// monolith/src/anticorruption/BillingTranslator.ts
// Translates between the monolith's internal types and the billing service's types

class BillingTranslator {
  // Translate monolith request to billing service format
  translateCreateRequest(internalRequest: InternalCreateSubscriptionRequest): BillingApiRequest {
    return {
      user_id: internalRequest.userId,
      plan_id: this.mapPlanToExternal(internalRequest.planName),
      payment_method_id: internalRequest.paymentInfo.stripePaymentMethodId,
      coupon_code: internalRequest.discountCode,
    };
  }

  // Translate billing service response to monolith format
  translateSubscriptionResponse(apiResponse: BillingApiSubscription): InternalSubscription {
    return {
      id: apiResponse.id,
      userId: apiResponse.user_id,
      planName: this.mapPlanToInternal(apiResponse.plan_id),
      status: this.mapStatus(apiResponse.status),
      currentPeriodStart: new Date(apiResponse.current_period_start),
      currentPeriodEnd: new Date(apiResponse.current_period_end),
      cancelAtPeriodEnd: apiResponse.cancel_at_period_end,
    };
  }

  private mapPlanToExternal(planName: string): string {
    const planMap: Record<string, string> = {
      'Starter': 'price_starter_001',
      'Professional': 'price_pro_001',
      'Enterprise': 'price_enterprise_001',
    };
    return planMap[planName] || planName;
  }

  private mapPlanToInternal(planId: string): string {
    const planMap: Record<string, string> = {
      'price_starter_001': 'Starter',
      'price_pro_001': 'Professional',
      'price_enterprise_001': 'Enterprise',
    };
    return planMap[planId] || planId;
  }

  private mapStatus(status: string): InternalSubscription['status'] {
    const statusMap: Record<string, InternalSubscription['status']> = {
      'active': 'active',
      'canceled': 'canceled',
      'past_due': 'pastDue',
      'trialing': 'trialing',
    };
    return statusMap[status] || 'unknown';
  }
}
```

## The Circuit Breaker Pattern

When calling remote services, implement circuit breakers to prevent cascading failures:

```typescript
// shared/infrastructure/CircuitBreaker.ts

enum CircuitState {
  CLOSED,    // Normal operation - requests pass through
  OPEN,      // Service is failing - requests are blocked
  HALF_OPEN, // Testing if service has recovered
}

class CircuitBreaker {
  private state: CircuitState = CircuitState.CLOSED;
  private failureCount = 0;
  private lastFailureTime: number | null = null;
  private readonly threshold: number;
  private readonly timeout: number; // ms before trying again

  constructor(
    private readonly serviceName: string,
    threshold = 5,
    timeout = 30000,
  ) {
    this.threshold = threshold;
    this.timeout = timeout;
  }

  async call<T>(fn: () => Promise<T>, fallback: () => Promise<T>): Promise<T> {
    if (this.state === CircuitState.OPEN) {
      if (Date.now() - (this.lastFailureTime || 0) > this.timeout) {
        this.state = CircuitState.HALF_OPEN;
      } else {
        console.warn(`Circuit breaker OPEN for ${this.serviceName}, using fallback`);
        return fallback();
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      console.warn(`Circuit breaker FAILURE for ${this.serviceName}, using fallback`);
      return fallback();
    }
  }

  private onSuccess() {
    this.failureCount = 0;
    this.state = CircuitState.CLOSED;
  }

  private onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    if (this.failureCount >= this.threshold) {
      this.state = CircuitState.OPEN;
      console.error(`Circuit breaker OPENED for ${this.serviceName}`);
    }
  }
}

// Usage
const billingCircuitBreaker = new CircuitBreaker('billing-service', 5, 30000);

async function getSubscription(userId: string) {
  return billingCircuitBreaker.call(
    // Primary: call remote service
    async () => {
      const response = await fetch(`${BILLING_URL}/subscriptions/${userId}`);
      if (!response.ok) throw new Error('Billing service error');
      return response.json();
    },
    // Fallback: use cached data or return degraded response
    async () => {
      const cached = await cache.get(`subscription:${userId}`);
      if (cached) return cached;
      return { error: 'Billing service unavailable', cached: false };
    },
  );
}
```

## The Saga Pattern for Distributed Transactions

When operations span multiple services, use the Saga pattern to maintain data consistency:

```typescript
// saga/create-subscription-saga.ts
// Coordinates multiple services for a complete business transaction

class CreateSubscriptionSaga {
  async execute(userId: string, planId: string, paymentMethodId: string) {
    const sagaId = crypto.randomUUID();

    try {
      // Step 1: Create customer in billing
      const customer = await billingService.createCustomer(userId);

      // Step 2: Charge payment method
      const payment = await billingService.charge(
        customer.id, paymentMethodId, planId
      );

      // Step 3: Create subscription
      const subscription = await billingService.createSubscription(
        customer.id, planId, payment.id
      );

      // Step 4: Update user record with subscription info
      await userService.setSubscription(userId, subscription.id);

      // Step 5: Enable features based on plan
      await featureService.enablePlanFeatures(userId, planId);

      // Step 6: Send confirmation
      await notificationService.sendSubscriptionConfirmation(userId, planId);

      return subscription;
    } catch (error) {
      // Compensating transactions (rollback)
      console.error(`Saga ${sagaId} failed, starting compensation:`, error);
      await this.compensate(userId, error);
      throw error;
    }
  }

  private async compensate(userId: string, error: Error) {
    // These are compensating actions for each step that succeeded
    try {
      await billingService.cancelCustomer(userId);
    } catch (e) {
      console.error('Compensation failed for billing:', e);
    }
    try {
      await featureService.disableAllFeatures(userId);
    } catch (e) {
      console.error('Compensation failed for features:', e);
    }
  }
}
```

## Service Communication Patterns

### Pattern 1: Synchronous HTTP (Simplest)

```typescript
// Service A calls Service B directly over HTTP
// Good for: Request-response workflows, query operations
// Bad for: Long-running operations, high-throughput events

class InventoryServiceClient {
  async checkStock(productId: string): Promise<StockLevel> {
    const response = await fetch(
      `${INVENTORY_SERVICE_URL}/stock/${productId}`,
      { headers: { 'Authorization': `Bearer ${this.apiKey}` } }
    );
    if (!response.ok) throw new Error('Inventory service error');
    return response.json();
  }
}
```

### Pattern 2: Asynchronous Events (More Resilient)

```typescript
// Service A publishes an event, Service B consumes it
// Good for: Decoupled workflows, cross-cutting concerns
// Bad for: Request-response workflows

// Using a message broker (Redis Streams, RabbitMQ, Kafka)
class EventPublisher {
  constructor(private broker: MessageBroker) {}

  async publishOrderPlaced(order: Order) {
    await this.broker.publish('orders.placed', {
      orderId: order.id,
      userId: order.userId,
      totalCents: order.totalCents,
      items: order.items,
      timestamp: new Date().toISOString(),
    });
  }
}

class InventoryService {
  constructor(private broker: MessageBroker) {}

  start() {
    this.broker.subscribe('orders.placed', async (event) => {
      // Update inventory levels
      for (const item of event.data.items) {
        await this.decrementStock(item.productId, item.quantity);
      }
    });
  }
}
```

### Pattern 3: Command Query Responsibility Segregation (CQRS)

```typescript
// Separate read and write paths
// Good for: Complex domains with different read/write patterns
// Bad for: Simple CRUD operations

// Write path
class OrderCommandService {
  async placeOrder(items: OrderItem[]): Promise<void> {
    // Validate, process payment, create order
    await db.query('INSERT INTO orders ...');
    await eventBus.publish('order.placed', { orderId, items });
  }
}

// Read path (may use a different data store)
class OrderQueryService {
  async getOrderSummary(orderId: string): Promise<OrderSummary> {
    // Returns pre-joined, denormalized read model
    return db.query(
      'SELECT * FROM order_summaries WHERE order_id = $1',
      [orderId]
    );
  }
}
```

## Monitoring a Distributed System

### What Changes When You Go Distributed

```
Monolith Monitoring:
  - One application to monitor
  - One log stream
  - One error tracking source
  - One performance profile

Distributed Monitoring (add these):
  - Service health per service
  - Inter-service latency
  - Error rate per service
  - Request tracing (correlation IDs)
  - Log aggregation (centralized logging)
  - Dependency graph
  - Circuit breaker status
  - Message queue depth
```

### Correlation IDs

```typescript
// Attach a correlation ID to every request that flows through services

// API Gateway: Generate correlation ID
app.use((req, res, next) => {
  req.correlationId = req.headers['x-correlation-id']
    || crypto.randomUUID();
  res.setHeader('x-correlation-id', req.correlationId);
  next();
});

// Service A: Pass to downstream services
class HttpClient {
  async get(url: string, correlationId: string) {
    return fetch(url, {
      headers: { 'x-correlation-id': correlationId },
    });
  }
}

// Service B: Log with correlation ID
class Logger {
  info(message: string, correlationId: string, extra?: any) {
    console.log(JSON.stringify({
      level: 'info',
      message,
      correlationId,
      service: 'billing-service',
      timestamp: new Date().toISOString(),
      ...extra,
    }));
  }
}
```

### Health Check Aggregation

```typescript
// API Gateway: Aggregate health checks from all services
app.get('/health', async (req, res) => {
  const services = ['billing', 'auth', 'core', 'notifications'];

  const healthResults = await Promise.allSettled(
    services.map(async (service) => {
      const response = await fetch(
        `http://${service}.internal:3000/health`
      );
      return { service, status: response.ok ? 'healthy' : 'unhealthy' };
    })
  );

  const overallStatus = healthResults.every(
    r => r.status === 'fulfilled' && r.value.status === 'healthy'
  ) ? 'healthy' : 'degraded';

  res.json({
    status: overallStatus,
    services: healthResults.map(r =>
      r.status === 'fulfilled' ? r.value : { status: 'unreachable' }
    ),
  });
});
```

## When NOT to Migrate

### The "Never Migrate" Scenarios

```
Keep the monolith forever if:
1. You're a solo founder or have < 3 developers
2. You have < 100k users
3. You're pre-product-market fit (still iterating rapidly)
4. Your deploy process takes < 10 minutes
5. Your test suite runs in < 5 minutes
6. You can't afford the infrastructure cost increase
7. You're already shipping features faster than competitors

The monolith is not a "temporary" architecture. Many successful
SaaS companies never migrated:
- Basecamp: Monolith Rails app, profitable for 15+ years
- GitHub: Monolith until 2015 (after acquisition, millions of users)
- Shopify: Monolith until they had thousands of merchants
- Mailchimp: Monolith for 15+ years, $700M revenue
```

### The Cost-Benefit Analysis

```
Before migrating, calculate:

Migration Cost:
  Development time: X weeks
  Infrastructure cost increase: $Y/mo
  Operational complexity increase: Z hours/week
  Risk of data loss/inconsistency: [Low/Med/High]

Expected Benefits:
  Development speed improvement: [Negligible/Small/Large]
  Scalability improvement: [Negligible/Small/Large]
  Reliability improvement: [Negligible/Small/Large]
  Team productivity improvement: [Negligible/Small/Large]

Rule of thumb: If migration takes > 3 months of one developer's time,
the benefits need to be transformative, not incremental.
```

## Real-World Migration Case Studies

### Case Study 1: Extract Billing Service

```
Company: InvoiceSaaS (fictional)
Context: 50k users, 4 developers, 2 years post-launch

Problem:
- Every deploy required QA on billing (PCI compliance concerns)
- Billing code was 30% of the codebase but 5% of changes
- Compliance audit required isolating billing data

Approach:
1. Extracted billing service (6 weeks)
2. Used dedicated Postgres database
3. API gateway routed /api/billing/* to new service
4. Monolith kept everything else

Result:
- Billing deploys reduced from 45 min to 10 min
- Compliance scope reduced by 40%
- Monolith complexity reduced
```

### Case Study 2: Extract Search Service

```
Company: ContentPlatform (fictional)
Context: 100k users, 8 developers, 3 years post-launch

Problem:
- Search queries were CPU-intensive (Elasticsearch)
- Search was causing database connection pool exhaustion
- Every search deploy required full regression testing

Approach:
1. Extracted search into dedicated service (4 weeks)
2. Used Elasticsearch with its own cluster
3. Monolith published content changes to search service via events
4. Search queries went directly to search service

Result:
- Search latency improved from 800ms to 50ms
- Database CPU dropped from 80% to 20%
- Search service independently scalable
```

### Case Study 3: Extract Authentication Service

```
Company: APIFirst (fictional)
Context: 200k users, 6 developers, multi-product company

Problem:
- Multiple products needed consistent auth
- Each product had its own auth implementation
- Security vulnerabilities found in multiple products

Approach:
1. Built auth service as the single source of truth (8 weeks)
2. All products authenticated through auth service
3. SSO, MFA, social login added once, used everywhere
4. Auth service became a platform, not a migration

Result:
- One auth implementation for all products
- Security updates deployed once
- 80% reduction in auth-related bugs
```

## The Solo Founder's Microservices Decision Tree

```
Are you a solo founder?
|-- YES --> Stay monolithic. Revisit when you hire.
|
|-- NO --> Do you have < 3 developers?
    |-- YES --> Do you have > 100k users?
    |   |-- YES --> Consider extracting 1-2 services
    |   |-- NO --> Stay monolithic
    |
    |-- NO --> Do you have > 5 developers?
        |-- YES --> Microservices may be justified
        |
        |-- NO --> Mixed approach:
            1. Keep monolith for core product
            2. Extract 1-2 services for clear boundaries
            3. Evaluate before extracting more
```

## Summary: The Microservices Decision Framework

1. **Start monolithic.** It's always the right choice initially.
2. **Extract incrementally.** One service at a time, only when needed.
3. **Measure the need.** Use the decision matrix. Don't migrate on gut feel.
4. **Migration is 6 weeks per service.** Plan accordingly.
5. **The Strangler Fig pattern.** Never rewrite. Always extract.
6. **Add anti-corruption layers.** Protect the monolith from service changes.
7. **Implement circuit breakers.** Prevent cascading failures.
8. **Use correlation IDs.** Debugging distributed systems requires tracing.
9. **Consider the cost.** Microservices cost more in infrastructure, operations, and complexity.
10. **Some monoliths never need splitting.** And that's fine.

The best architecture is the one that lets you ship features to customers. If your monolith is doing that effectively, you don't need microservices. If it's not, identify the specific bottleneck and extract only that component.
