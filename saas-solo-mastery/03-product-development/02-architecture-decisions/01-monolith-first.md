# Monolith First: Why Start with a Monolithic Architecture

## The Architecture Debate

Every solo founder faces the architecture question: "Should I start with microservices or a monolith?" The answer, for 95% of solo founders, is a resounding monolith first. This guide explains why, provides concrete patterns for building a "modular monolith," and details exactly when and how to split.

## Why Monolith First

### The Solo Founder's Calculus

As a solo founder, your constraints are:

1. **Time**: You have limited hours. Every minute spent on infrastructure is a minute not spent on product.
2. **Focus**: You can only hold so much complexity in your head. Microservices multiply complexity.
3. **Resources**: You're paying for everything out of pocket. Distributed systems cost more.
4. **Scale**: You have zero users. You will not have scaling problems for months or years.

Given these constraints, the monolith is the only rational choice.

### The Cost of Microservices (For Solo Founders)

```
Microservices Cost Prematurely:

Complexity Cost:
- Multiple services to develop, test, deploy
- Inter-service communication (RPC, message queues)
- Distributed transactions
- Service discovery
- API gateway
- Container orchestration
- Network configuration

Cognitive Cost:
- Context switching between services
- Debugging across service boundaries
- Understanding the full system
- Keeping service contracts in sync

Infrastructure Cost:
- Multiple deployments
- Multiple databases (or shared database — defeating the purpose)
- Container registry
- Orchestration platform
- Monitoring across services
- Log aggregation
- Tracing

Money Cost:
- Multiple servers/VMs
- Container orchestration (hosted or self-managed)
- Monitoring tools
- Data transfer between services
```

### What the Monolith Gives You

```
Monolith Advantages for Solo Founders:

1. Simple Deployment
  - One codebase → one build → one deploy
  - Deploy in minutes, not hours
  - Rollback is a single command

2. Simple Development
  - One language, one framework
  - One way to test (integration tests catch everything)
  - One process to debug
  - Full stack in one IDE project

3. Simple Operations
  - One process to monitor
  - One set of logs
  - One place to configure
  - One backup strategy

4. Simple Data
  - One database
  - ACID transactions across all entities
  - No distributed consistency headaches
  - Simple joins and queries

5. Fast Development
  - No service boundary negotiation
  - No API versioning between services
  - No serialization/deserialization overhead
  - Refactoring across concerns is easy

6. Low Cost
  - One server ($5-20/mo)
  - No inter-service networking costs
  - Simple monitoring (free tier tools)
  - No container orchestration fees
```

## The Modular Monolith Pattern

A "modular monolith" is a monolith that's organized like microservices internally but deployed as a single unit. This gives you the development speed of a monolith with a path to splitting later.

### Structure Overview

```
project-root/
├── modules/                    # Domain modules
│   ├── billing/               # Billing context
│   │   ├── domain/            # Domain models and logic
│   │   │   ├── Invoice.ts
│   │   │   ├── Subscription.ts
│   │   │   └── Payment.ts
│   │   ├── application/       # Application services
│   │   │   ├── InvoiceService.ts
│   │   │   └── SubscriptionService.ts
│   │   ├── infrastructure/    # Database, external APIs
│   │   │   ├── StripeClient.ts
│   │   │   └── BillingRepository.ts
│   │   ├── api/               # HTTP/REST endpoints
│   │   │   ├── BillingController.ts
│   │   │   └── WebhookController.ts
│   │   └── index.ts           # Public API of the module
│   │
│   ├── users/                 # User management context
│   │   ├── domain/
│   │   │   ├── User.ts
│   │   │   └── Team.ts
│   │   ├── application/
│   │   │   └── UserService.ts
│   │   ├── infrastructure/
│   │   │   └── UserRepository.ts
│   │   ├── api/
│   │   │   └── UserController.ts
│   │   └── index.ts
│   │
│   ├── projects/              # Core domain context
│   │   ├── domain/
│   │   ├── application/
│   │   ├── infrastructure/
│   │   ├── api/
│   │   └── index.ts
│   │
│   └── analytics/             # Analytics context
│       ├── domain/
│       ├── application/
│       ├── infrastructure/
│       ├── api/
│       └── index.ts
│
├── shared/                    # Shared kernel (use sparingly)
│   ├── kernel/               # Base types, value objects
│   │   ├── Entity.ts
│   │   ├── ValueObject.ts
│   │   └── AggregateRoot.ts
│   ├── infrastructure/       # Shared infrastructure
│   │   ├── Database.ts
│   │   └── EventBus.ts
│   └── utils/
│       ├── pagination.ts
│       └── validation.ts
│
├── main.ts                    # Application entry point
└── routes.ts                  # Route registration
```

### Module Boundaries

Each module must have:

1. **Public API (`index.ts`):** What other modules can call. Only expose interfaces, not internals.
2. **Internal implementation:** Everything else is private to the module.
3. **Domain models:** Business logic that is independent of infrastructure.
4. **Infrastructure:** Database access, external API clients.

### Module Communication Rules

```
Rule 1: Modules communicate through their public API only
  ✅ billing.public.createSubscription(userId, planId)
  ❌ billing.infrastructure.StripeClient.createCustomer()

Rule 2: Modules don't access each other's databases
  ✅ projects.public.getProjectsForUser(userId)
  ❌ SELECT * FROM billing.invoices WHERE user_id = ?

Rule 3: Modules don't import each other's internals
  ✅ import { billing } from '@/modules/billing'
  ❌ import { StripeClient } from '@/modules/billing/infrastructure'

Rule 4: Shared kernel is minimal and stable
  ✅ import { Entity } from '@/shared/kernel'
  ❌ import { DateUtils } from '@/shared/utils' (avoids creating shared utils)
```

### Module API Example

```typescript
// modules/billing/index.ts — Public API of the billing module

import { CreateSubscriptionDTO } from './domain/types';
import { SubscriptionService } from './application/SubscriptionService';
import { InvoiceService } from './application/InvoiceService';
import { UserId } from '@/shared/kernel';

// This is the ONLY thing other modules can import from billing
export const billing = {
  createSubscription(userId: UserId, planId: string) {
    const service = new SubscriptionService();
    return service.create(userId, planId);
  },

  cancelSubscription(userId: UserId) {
    const service = new SubscriptionService();
    return service.cancel(userId);
  },

  getInvoices(userId: UserId) {
    const service = new InvoiceService();
    return service.getForUser(userId);
  },

  handleStripeWebhook(event: unknown) {
    const service = new SubscriptionService();
    return service.handleWebhook(event);
  },
};

// Other modules use it like:
// import { billing } from '@/modules/billing';
// await billing.createSubscription(userId, planId);
```

### Internal Module Structure

```typescript
// modules/billing/domain/Subscription.ts
// Domain model — pure business logic, no infrastructure

export class Subscription {
  constructor(
    public readonly id: string,
    public readonly userId: string,
    public readonly planId: string,
    public readonly status: 'active' | 'canceled' | 'past_due' | 'trialing',
    public readonly currentPeriodEnd: Date,
  ) {}

  // Business logic lives here
  cancel(): Subscription {
    if (this.status === 'canceled') {
      throw new Error('Subscription already canceled');
    }
    return new Subscription(
      this.id,
      this.userId,
      this.planId,
      'canceled',
      this.currentPeriodEnd,
    );
  }

  isActive(): boolean {
    return this.status === 'active' || this.status === 'trialing';
  }
}
```

```typescript
// modules/billing/application/SubscriptionService.ts
// Application service — orchestrates domain logic and infrastructure

import { SubscriptionRepository } from '../infrastructure/SubscriptionRepository';
import { StripeClient } from '../infrastructure/StripeClient';
import { Subscription } from '../domain/Subscription';

export class SubscriptionService {
  constructor(
    private repo = new SubscriptionRepository(),
    private stripe = new StripeClient(),
  ) {}

  async create(userId: string, planId: string): Promise<Subscription> {
    const stripeCustomer = await this.stripe.createCustomer(userId);
    const stripeSubscription = await this.stripe.createSubscription(
      stripeCustomer.id,
      planId,
    );

    const subscription = new Subscription(
      stripeSubscription.id,
      userId,
      planId,
      'trialing',
      new Date(stripeSubscription.current_period_end * 1000),
    );

    await this.repo.save(subscription);
    return subscription;
  }

  async cancel(userId: string): Promise<Subscription> {
    const subscription = await this.repo.findActiveByUser(userId);
    if (!subscription) {
      throw new Error('No active subscription found');
    }
    const canceled = subscription.cancel();
    await this.stripe.cancelSubscription(canceled.id);
    await this.repo.save(canceled);
    return canceled;
  }
}
```

### Database Schema for Modular Monolith

Each module has its own database tables but they live in the same database.

```sql
-- All in the same database instance

-- users module
CREATE SCHEMA IF NOT EXISTS users;
CREATE TABLE users.users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- billing module
CREATE SCHEMA IF NOT EXISTS billing;
CREATE TABLE billing.subscriptions (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users.users(id),
  plan_id VARCHAR(50) NOT NULL,
  status VARCHAR(20) NOT NULL,
  current_period_end TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE billing.invoices (
  id UUID PRIMARY KEY,
  subscription_id UUID REFERENCES billing.subscriptions(id),
  amount_cents INTEGER NOT NULL,
  status VARCHAR(20) NOT NULL,
  paid_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- projects module
CREATE SCHEMA IF NOT EXISTS projects;
CREATE TABLE projects.projects (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users.users(id),
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### The Module Dependency Graph

Keep your module dependencies acyclic and hierarchical:

```
            users
           /     \
          /       \
    projects    billing
          \       /
           \     /
          analytics
```

Rules:
- Lower-level modules don't depend on higher-level modules
- Circular dependencies between modules are forbidden
- Each module depends on modules in layers below it

### When Modules Become Too Coupled

Signs your monolith modules are too coupled:

```
1. Module A frequently calls 5+ methods on Module B's API
2. Changes to Module B require changes in Module A
3. You can't test Module A without Module B's database
4. Module API boundaries are frequently crossed in transactions
5. You have circular dependencies between modules
6. Module boundaries keep shifting (code is reorganized weekly)
```

Fix: Extract a shared module for the coupled functionality, or merge the modules.

## When to Split

### The Split Decision Framework

Don't split until you have a concrete reason. Reasons to split (in priority order):

```markdown
1. Team Scaling
   You've hired a second developer. They need clear ownership boundaries.
   → Split when: You have 2+ developers working on the codebase

2. Deployment Coupling
   Every deployment requires all services to be deployed simultaneously.
   → Split when: Deploy frequency causes coordination overhead

3. Scalability Requirements
   One part of the system has different scaling requirements than others.
   (e.g., API calls scale differently than background job processing)
   → Split when: You need to scale parts independently

4. Failure Isolation
   A bug in one module brings down the entire application.
   → Split when: Reliability requirements demand fault isolation

5. Data Isolation
   Different parts of the system have different data requirements
   (e.g., one part needs a graph DB, another needs a document store)
   → Split when: A single database type can't serve all needs

6. Security Boundaries
   Different compliance requirements for different data
   (e.g., billing data vs. analytics data)
   → Split when: Compliance requires strict data segregation

7. Team Specialization
   Developers want to use different tech stacks
   → Split when: You have a team with diverse expertise
```

### The Solo Founder's Split Triggers

For solo founders specifically, you should NOT split until:

```
☐ You have > 1000 paying customers
☐ Monthly revenue > $20,000 MRR
☐ You've hired at least 2 other developers
☐ Deploy frequency is multiple times per day
☐ You have > 100k users
☐ Your database is experiencing scaling issues
☐ You're spending > 20 hours/month on infrastructure
```

If you haven't checked most of these boxes, you don't need microservices.

### What to Split First

When you do split, split the modules that provide the most benefit:

```
First Split Candidate: Background Jobs
  Why: Different scaling profile, doesn't need real-time
  Split into: Worker service
  Monolith remains: Web server (handles HTTP requests)

Second Split: Billing / Payments
  Why: Security isolation, compliance requirements
  Split into: Billing service
  Monolith remains: Core product logic

Third Split: API / Public API
  Why: Different traffic patterns, API versioning
  Split into: API gateway + API service
  Monolith remains: Core product

Fourth Split: Admin / Internal tools
  Why: Different access patterns, lower priority
  Split into: Admin service
  Monolith remains: Customer-facing product
```

## The Database-First Extraction Strategy

When splitting a module into a service, the database is the hardest part.

### Phase 1: Logical Schema Separation

While still a monolith, separate schemas in the database:

```sql
-- Before: Everything in one schema
CREATE TABLE users (...);
CREATE TABLE subscriptions (...);
CREATE TABLE projects (...);

-- After: Schemas per module
CREATE SCHEMA users;
CREATE SCHEMA billing;
CREATE SCHEMA projects;

CREATE TABLE users.users (...);
CREATE TABLE billing.subscriptions (...);
CREATE TABLE billing.invoices (...);
CREATE TABLE projects.projects (...);
```

### Phase 2: Repository Pattern

Wrap all database access in repositories that could be pointed at a different database:

```typescript
// Before: Direct SQL in controllers
app.get('/api/projects', async (req, res) => {
  const projects = await db.query('SELECT * FROM projects WHERE user_id = $1', [req.userId]);
  res.json(projects);
});

// After: Repository pattern
interface IProjectRepository {
  findByUser(userId: string): Promise<Project[]>;
  save(project: Project): Promise<void>;
}

class PostgresProjectRepository implements IProjectRepository {
  async findByUser(userId: string): Promise<Project[]> {
    const rows = await db.query('SELECT * FROM projects.projects WHERE user_id = $1', [userId]);
    return rows.map(row => Project.fromDatabase(row));
  }
}
```

### Phase 3: HTTP Facade

When you're ready to split, add an HTTP facade:

```typescript
// Before split — direct function call
const projects = await billing.getInvoices(userId);

// During split — use feature flag to route
const billingClient = process.env.BILLING_SERVICE_URL
  ? new BillingHttpClient(process.env.BILLING_SERVICE_URL) // Remote
  : billing; // Local

const invoices = await billingClient.getInvoices(userId);
```

### Phase 4: Data Migration

The actual data split — this is the risky part:

```markdown
Data Migration Plan When Splitting:

1. Create a copy of the data in the new service's database
2. Run both systems in parallel (dual-write)
3. Verify data consistency between systems
4. Switch reads to the new system
5. Remove writes to the old system
6. Clean up old data

Example: Splitting billing into its own service

Week 1: Create billing service with its own database
         Copy billing schema and data to new database
         Run sync job to keep data in sync

Week 2: Dual-write phase
         Every write goes to both old and new databases
         Compare results, fix inconsistencies
         Test billing service API

Week 3: Switch reads
         Route billing reads through billing service
         Keep writes going to both

Week 4: Switch writes
         Route all billing operations through billing service
         Remove old database writes
         Verify everything works

Week 5: Cleanup
         Remove billing tables from main database
         Remove billing code from monolith
```

### The Async Communication Pattern

When services communicate, prefer async over sync:

```typescript
// Before (monolith): Sync function call
await billing.createSubscription(userId, planId);

// After (microservices): Async message
// Service A publishes event
await eventBus.publish('subscription.created', {
  userId,
  planId,
  timestamp: new Date(),
});

// Service B (email service) subscribes
eventBus.subscribe('subscription.created', async (event) => {
  await emailService.sendWelcomeEmail(event.data.userId);
});
```

## Common Monolith Misconceptions

### Misconception 1: "Monolith = Unmaintainable Spaghetti"

A well-structured monolith is more maintainable than poorly-structured microservices. The modular monolith pattern keeps things organized without the overhead of distributed systems.

**Reality:** Clean code is clean code regardless of deployment topology. Bad code is bad code regardless of how many services you split it into.

### Misconception 2: "Monolith Can't Scale"

Most monoliths can scale to millions of users. GitHub ran as a monolith (Rails) for years serving millions of developers. Shopify runs as a monolith. Basecamp runs as a monolith.

**Reality:** Scaling a monolith means scaling the entire application. Scaling microservices means scaling only the hot path. But for solo founders with < 100k users, scaling the entire app is trivially cheap.

### Misconception 3: "Microservices Are the Professional Way"

Microservices are a trade-off, not an upgrade. They trade simplicity for flexibility. For a solo founder, simplicity is more valuable than flexibility.

**Reality:** The most professional approach is the one that ships value to customers. Customers don't care about your architecture.

### Misconception 4: "You'll Never Be Able to Migrate"

Migration from monolith to microservices is well-understood. Shopify did it. Etsy did it. Most successful SaaS companies did it. The monolith-first approach doesn't lock you in — it gives you time to understand your domain before splitting.

**Reality:** A domain that's been built as a well-structured monolith is easier to split than a domain that was prematurely split into microservices based on guesses about boundaries.

## The "Monolith with Escape Hatches" Architecture

Build your monolith with specific escape hatches that make future splitting easier:

### Escape Hatch 1: Feature Flags

```typescript
// config/features.ts
export const features = {
  useBillingMicroservice: false, // Flip to true when ready
  useSeparateSearchService: false,
  useBackgroundWorker: false,
};

// In code:
if (features.useBillingMicroservice) {
  return await billingHttpClient.createSubscription(userId, planId);
} else {
  return await localBillingService.createSubscription(userId, planId);
}
```

### Escape Hatch 2: Event Bus

Even in a monolith, emit events. This makes it easy to add event-driven services later.

```typescript
// shared/infrastructure/EventBus.ts
type EventHandler = (event: any) => Promise<void>;

class EventBus {
  private handlers: Map<string, EventHandler[]> = new Map();
  private storeEvents: boolean = false;

  subscribe(event: string, handler: EventHandler) {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, []);
    }
    this.handlers.get(event)!.push(handler);
  }

  async publish(event: string, data: unknown) {
    const handlers = this.handlers.get(event) || [];
    await Promise.all(handlers.map(h => h({ type: event, data })));

    if (this.storeEvents) {
      await this.saveToOutbox(event, data);
    }
  }

  private async saveToOutbox(event: string, data: unknown) {
    // Saves events to an outbox table for reliable delivery later
  }
}

export const eventBus = new EventBus();
```

### Escape Hatch 3: Service Interface

Define each module's public API through an interface that could be implemented remotely:

```typescript
// billing/public/BillingApi.ts

export interface BillingApi {
  createSubscription(userId: string, planId: string): Promise<Subscription>;
  cancelSubscription(userId: string): Promise<void>;
  getInvoices(userId: string): Promise<Invoice[]>;
  handleWebhook(event: unknown): Promise<void>;
}

// Local implementation (monolith)
class LocalBillingApi implements BillingApi {
  // Direct function calls
}

// Remote implementation (microservices)
class RemoteBillingApi implements BillingApi {
  constructor(private baseUrl: string) {}

  async createSubscription(userId: string, planId: string) {
    const response = await fetch(`${this.baseUrl}/subscriptions`, {
      method: 'POST',
      body: JSON.stringify({ userId, planId }),
    });
    return response.json();
  }
}

// Switch at config level
const billingApi: BillingApi = config.useRemoteBilling
  ? new RemoteBillingApi(config.billingServiceUrl)
  : new LocalBillingApi();
```

### Escape Hatch 4: Database Per Module (Same Server)

Use separate schemas/databases on the same server:

```sql
-- Same Postgres instance, separate databases
CREATE DATABASE billing_db;
CREATE DATABASE projects_db;
CREATE DATABASE users_db;

-- Or same database, separate schemas (easier to split later)
CREATE SCHEMA billing;
CREATE SCHEMA projects;
CREATE SCHEMA users;
```

### Escape Hatch 5: API Gateway Pattern (Within Monolith)

Structure your route handling as if behind an API gateway:

```typescript
// main.ts — API Gateway-like routing
const app = express();

// Billing routes — could be moved to separate service
app.use('/api/billing', billingRouter);

// Users routes — could be moved to separate service
app.use('/api/users', usersRouter);

// Projects routes — could be moved to separate service
app.use('/api/projects', projectsRouter);

// Health check
app.get('/health', (req, res) => res.json({ status: 'ok' }));
```

## Real-World Examples

### Example 1: Basecamp (37signals)

Basecamp ran as a Ruby on Rails monolith for over a decade. It served hundreds of thousands of businesses with a small team. When they needed to scale specific features (like real-time updates), they extracted only those specific components.

**Key takeaway:** A well-built monolith can serve a very successful SaaS business for years.

### Example 2: Shopify

Shopify started as a monolith (Ruby on Rails). As they grew to serve millions of merchants, they extracted specific services:
- Authentication service (early)
- Payments service (mid-stage)
- Checkout service (mid-stage)
- Search service (late stage)

**Key takeaway:** Even at massive scale, Shopify extracted services incrementally, not upfront.

### Example 3: GitHub

GitHub was a Ruby on Rails monolith for most of its early life. They extracted services as needed:
- Background job processing (Sidekiq early on)
- Git data storage (when they needed specialized storage)
- Search (when Elasticsearch made sense)

**Key takeaway:** Extract only when you have a concrete, measurable reason.

## Architecture Decision Record Template

```markdown
# ADR: Architecture Approach

## Title
Monolith-first architecture

## Status
Accepted

## Context
- Solo founder building first version of product
- No paying customers yet
- Limited development time
- Need to ship quickly

## Decision
Use a modular monolith architecture with well-defined module boundaries,
domain-driven design within the monolith, and clear public APIs for each module.

We will NOT use microservices, containers, or distributed systems.

## Consequences
**Positive:**
- Fast development speed
- Simple deployment and operations
- Low infrastructure costs
- Easy to refactor and iterate

**Negative:**
- Will need to split services as we grow
- Cannot scale individual components independently
- Single deployment unit (any change = full deploy)

## Triggers for Reconsideration
- When we have > 1000 paying customers
- When we hire > 2 developers
- When deployment frequency causes coordination issues
- When specific module needs independent scaling
```

## Summary

Build a monolith first. Build it as a modular monolith with clear boundaries and well-defined APIs. This gives you speed, simplicity, and a clear path to splitting later if needed. The modular monolith is not a compromise — it's the optimal architecture for solo founders building SaaS products.

**The mantra:** Monolith first. Microservices last. Modular always.
