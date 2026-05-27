# Section 04: Stripe Webhook Handler

## Webhook Endpoint Setup

Stripe sends webhook events for asynchronous billing activities: subscription updates, invoice completion, payment success/failure, and more. The webhook handler must be idempotent, secure, and resilient.

```typescript
class StripeWebhookHandler {
  private webhookSecret: string;

  constructor() {
    this.webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;
  }

  async handleWebhook(req: Request, res: Response): Promise<void> {
    const sig = req.headers['stripe-signature'];

    let event: Stripe.Event;
    try {
      event = stripe.webhooks.constructEvent(
        req.body,
        sig,
        this.webhookSecret
      );
    } catch (err) {
      logger.error('Webhook signature verification failed', { error: err.message });
      res.status(400).send(`Webhook Error: ${err.message}`);
      return;
    }

    // Idempotency check
    const processed = await this.idempotencyService.check(event.id);
    if (processed) {
      logger.info('Webhook already processed', { eventId: event.id });
      res.json({ received: true });
      return;
    }

    try {
      await this.processEvent(event);
      await this.idempotencyService.markProcessed(event.id);
      res.json({ received: true });
    } catch (error) {
      logger.error('Webhook processing failed', {
        eventId: event.id,
        type: event.type,
        error: error.message,
      });
      res.status(500).json({ error: 'Webhook processing failed' });
    }
  }

  private async processEvent(event: Stripe.Event): Promise<void> {
    switch (event.type) {
      case 'customer.subscription.created':
        await this.handleSubscriptionCreated(event.data.object as Stripe.Subscription);
        break;
      case 'customer.subscription.updated':
        await this.handleSubscriptionUpdated(event.data.object as Stripe.Subscription);
        break;
      case 'customer.subscription.deleted':
        await this.handleSubscriptionDeleted(event.data.object as Stripe.Subscription);
        break;
      case 'invoice.paid':
        await this.handleInvoicePaid(event.data.object as Stripe.Invoice);
        break;
      case 'invoice.payment_failed':
        await this.handleInvoicePaymentFailed(event.data.object as Stripe.Invoice);
        break;
      case 'payment_intent.succeeded':
        await this.handlePaymentSucceeded(event.data.object as Stripe.PaymentIntent);
        break;
      case 'payment_intent.payment_failed':
        await this.handlePaymentFailed(event.data.object as Stripe.PaymentIntent);
        break;
      case 'customer.updated':
        await this.handleCustomerUpdated(event.data.object as Stripe.Customer);
        break;
      default:
        logger.info('Unhandled webhook event type', { type: event.type });
    }
  }
}
```

## Signature Verification

Every webhook request includes a `Stripe-Signature` header. The handler verifies the signature using the webhook signing secret. This prevents fraudulent webhook requests.

```typescript
function verifyWebhookSignature(
  payload: Buffer,
  signature: string,
  secret: string
): Stripe.Event {
  try {
    return stripe.webhooks.constructEvent(payload, signature, secret);
  } catch (err) {
    if (err.type === 'StripeSignatureVerificationError') {
      throw new Error('Invalid webhook signature');
    }
    throw err;
  }
}
```

## Event Processing

Each event type maps to a specific handler. Handlers update internal state, trigger notifications, or modify tenant feature access. Critical events include subscription status changes and invoice payment results.

```typescript
class WebhookEventHandler {
  async handleSubscriptionCreated(subscription: Stripe.Subscription): Promise<void> {
    const tenantId = subscription.metadata.tenant_id;
    const planId = subscription.metadata.plan_id;

    await this.db.subscriptions.create({
      id: subscription.id,
      tenantId,
      planId,
      status: subscription.status,
      stripeStatus: subscription.status,
      currentPeriodStart: new Date(subscription.current_period_start * 1000),
      currentPeriodEnd: new Date(subscription.current_period_end * 1000),
      trialStart: subscription.trial_start
        ? new Date(subscription.trial_start * 1000)
        : null,
      trialEnd: subscription.trial_end
        ? new Date(subscription.trial_end * 1000)
        : null,
    });

    // Apply plan features
    await this.featureGateService.applyPlan(tenantId, planId);

    // Send welcome email
    await this.notificationService.sendSubscriptionWelcome(tenantId, planId);
  }

  async handleSubscriptionUpdated(subscription: Stripe.Subscription): Promise<void> {
    const tenantId = subscription.metadata.tenant_id;

    await this.db.subscriptions.updateOne(
      { id: subscription.id },
      {
        $set: {
          status: subscription.status,
          currentPeriodStart: new Date(subscription.current_period_start * 1000),
          currentPeriodEnd: new Date(subscription.current_period_end * 1000),
          cancelAtPeriodEnd: subscription.cancel_at_period_end,
        },
      }
    );

    // Check for plan change
    const newPlanId = subscription.metadata.plan_id;
    const currentSub = await this.db.subscriptions.findOne({ id: subscription.id });
    if (currentSub.planId !== newPlanId) {
      await this.featureGateService.applyPlan(tenantId, newPlanId);
    }
  }

  async handleInvoicePaid(invoice: Stripe.Invoice): Promise<void> {
    const tenantId = invoice.metadata.tenant_id;

    // Store invoice record
    await this.invoiceService.storeInvoice(invoice);

    // Send receipt
    await this.notificationService.sendPaymentReceipt(tenantId, invoice.id);

    // If subscription was past_due, it's now active
    if (invoice.subscription) {
      const sub = await stripe.subscriptions.retrieve(invoice.subscription);
      if (sub.status === 'active') {
        await this.featureGateService.restoreFullAccess(tenantId);
      }
    }
  }

  async handleInvoicePaymentFailed(invoice: Stripe.Invoice): Promise<void> {
    const tenantId = invoice.metadata.tenant_id;

    // Start dunning process
    await this.dunningService.startDunningProcess(tenantId, invoice);

    // Send payment failure notification
    await this.notificationService.sendPaymentFailed(tenantId, invoice.id);
  }
}
```

## Idempotent Handling

Stripe guarantees at-least-once webhook delivery. Each event has a unique ID that the handler uses for idempotency. Processing state is stored in Redis with a TTL matching Stripe's webhook retention (3 days).

```typescript
const IDEMPOTENCY_TTL = 72 * 60 * 60; // 72 hours

async function ensureIdempotent(
  eventId: string,
  processor: () => Promise<void>
): Promise<void> {
  const key = `webhook:processed:${eventId}`;

  const already = await redis.setnx(key, Date.now().toString());
  if (already === 0) {
    logger.info('Skipping already processed webhook', { eventId });
    return;
  }

  await redis.expire(key, IDEMPOTENCY_TTL);

  try {
    await processor();
  } catch (error) {
    // Remove key on failure to allow retry
    await redis.del(key);
    throw error;
  }
}
```

## Open-Source Tools

- **Stripe CLI** — Local webhook forwarding for development
- **Redis** — Idempotency tracking and rate limiting
- **BullMQ** — Queue webhook processing for reliability
- **Prometheus** — Webhook processing metrics (latency, errors, by type)

## Integration Points

The webhook handler integrates with the subscription service, invoice service, dunning service, feature gate service, notification service, and reconciliation service. It is the central nervous system connecting Stripe events to internal business logic.

## Production Considerations

- Register webhook endpoint in Stripe Dashboard with all relevant events
- Set up monitoring for webhook processing latency and error rates
- Implement dead letter queue for webhook events that fail repeatedly
- Log all webhook events for audit trail
- Test webhook handling with Stripe test clock functionality
- Handle Stripe API version upgrades carefully

## Open-Source First Philosophy

Stripe's webhook system is free to use and well-documented. Redis provides idempotency tracking at negligible cost. BullMQ queues webhook processing for reliable execution. Prometheus and Grafana monitor webhook health. This entirely open-source stack handles millions of webhook events reliably without proprietary queuing or monitoring infrastructure.
