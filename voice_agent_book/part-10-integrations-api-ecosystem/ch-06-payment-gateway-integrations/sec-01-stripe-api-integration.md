# Section 01: Stripe API Integration

## Overview

The Stripe API integration enables the voice agent platform to process payments, manage subscriptions, and handle refunds through Stripe's payment infrastructure. This adapter allows voice agents to take credit card payments over the phone, retrieve payment method details via PCI-compliant Stripe Elements, create invoices, and manage customer payment lifecycle. The adapter wraps Stripe's REST API and client SDK, exposing payment operations through the unified payment adapter interface.

The integration handles the complete payment flow: customer creation or lookup, payment method attachment (via Stripe's tokenization or SetupIntents), charge creation or PaymentIntent confirmation, invoice generation, subscription management, and refund processing. All payment operations are logged for audit and reconciliation purposes. The adapter supports Stripe's Connect platform for marketplace scenarios where payment processing flows through different connected accounts.

## Architecture

```
                   Stripe Integration Flow

   Voice Agent ←→ Payment Gateway ←→ Stripe Adapter ←→ Stripe API
                        |
   +---------------------------------------------------------------+
   |                   Stripe Adapter Internal Flow                |
   |                                                               |
   |  +----------------+  +-------------------+  +--------------+  |
   |  | Tokenization   |  | Customer Mgmt     |  | Payment Proc |  |
   |  | • Stripe.js    |  | • Create/Update   |  | • Charge     |  |
   |  | • Elements SDK |  | • PaymentMethods  |  | • Refund     |  |
   |  | • PCI DSS      |  | • Sources         |  | • Disputes   |  |
   |  +----------------+  +-------------------+  +--------------+  |
   |  +----------------+  +-------------------+  +--------------+  |
   |  | Subscriptions  |  | Invoices          |  | Reporting    |  |
   |  | • Create       |  | • Generate        |  | • Balance    |  |
   |  | • Update       |  | • Finalize        |  | • Payouts    |  |
   |  | • Cancel       |  | • Send            |  | • Reconcile  |  |
   |  +----------------+  +-------------------+  +--------------+  |
   +---------------------------------------------------------------+
```

## Design Decisions

- **Server-side confirmation over client-side tokenization only:** Payment Intents are created server-side with the amount and currency, then confirmed either server-side (for voice payments where the agent collects card details via DTMF) or client-side (for web-based flows). Server-side confirmation gives the voice platform control over retry logic and idempotency. Trade-off: server-side confirmation requires PCI-compliant infrastructure (SAQ D) while client-side reduces PCI scope but adds latency to voice flows.

- **Idempotency key on every write operation:** All payment mutations (charge, refund, subscription create) include an idempotency key derived from the call session ID and operation sequence number. This ensures that retries due to timeouts or network failures do not result in duplicate charges. Stripe enforces idempotency for 24 hours. Trade-off: idempotency keys require deterministic generation and storage but prevent double-charging in the event of retries.

- **Webhook-driven state reconciliation over polling:** The adapter registers Stripe webhooks for charge.succeeded, payment_intent.succeeded, invoice.paid, charge.dispute.created, and related events. The webhook handler updates the local payment state and triggers business logic (e.g., marking an order as paid). Polling is used as a fallback for webhook delivery failures. Trade-off: webhooks require public endpoint exposure and signature verification but provide near-instant state updates without API rate limit consumption.

## Implementation Approach

```
interface StripeAdapterConfig {
  secretKey: string;
  publishableKey: string;
  webhookSecret: string;
  defaultCurrency: string;
  statementDescriptor: string;
  connectAccountId?: string;
}

interface PaymentIntentRequest {
  amount: number;
  currency: string;
  customerId?: string;
  paymentMethodId?: string;
  metadata: Record<string, string>;
  idempotencyKey: string;
}

interface PaymentResult {
  paymentIntentId: string;
  status: 'succeeded' | 'requires_action' | 'processing' | 'failed';
  amount: number;
  currency: string;
  failureReason?: string;
  nextAction?: { type: string; clientSecret: string };
}

class StripePaymentAdapter extends BasePaymentAdapter {
  private stripe: Stripe;

  constructor(config: StripeAdapterConfig) {
    super(config);
    this.stripe = new Stripe(config.secretKey, {
      apiVersion: '2023-10-16',
      maxNetworkRetries: 3,
    });
  }

  async createPaymentIntent(
    request: PaymentIntentRequest
  ): Promise<AdapterResponse<PaymentResult>> {
    const intent = await this.stripe.paymentIntents.create({
      amount: request.amount,
      currency: request.currency,
      customer: request.customerId,
      payment_method: request.paymentMethodId,
      metadata: request.metadata,
      statement_descriptor: this.config.statementDescriptor?.slice(0, 22),
      confirmation_method: 'automatic',
    }, { idempotencyKey: request.idempotencyKey });

    return {
      success: intent.status !== 'requires_payment_method',
      data: this.mapIntentToResult(intent),
    };
  }

  async confirmPayment(paymentIntentId: string): Promise<AdapterResponse<PaymentResult>> {
    const intent = await this.stripe.paymentIntents.confirm(paymentIntentId);
    return { success: intent.status === 'succeeded', data: this.mapIntentToResult(intent) };
  }

  async createRefund(paymentIntentId: string, amount?: number): Promise<AdapterResponse<void>> {
    await this.stripe.refunds.create({
      payment_intent: paymentIntentId,
      amount: amount,
    }, { idempotencyKey: `refund-${paymentIntentId}` });
    return { success: true, data: undefined };
  }

  private mapIntentToResult(intent: Stripe.PaymentIntent): PaymentResult {
    return {
      paymentIntentId: intent.id,
      status: intent.status as PaymentResult['status'],
      amount: intent.amount,
      currency: intent.currency,
      failureReason: intent.last_payment_error?.message,
      nextAction: intent.next_action ? {
        type: intent.next_action.type,
        clientSecret: intent.client_secret!,
      } : undefined,
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Stripe SDK (MIT) | Node.js | Stripe API client |
| Stripe Webhooks (MIT) | Node.js | Webhook signature verification |
| Pino (MIT) | Logging | Structured payment audit logs |
| ioredis (MIT) | Redis | Idempotency key dedup cache |

## Production Considerations

**Scaling:** Stripe API rate limits vary by endpoint (default 100 read ops/s, 100 write ops/s). Implement client-side rate limiting to avoid 429 responses. Use Stripe's auto-pagination for list endpoints. Cache customer and payment method lookups in Redis with 5-minute TTL. Webhook processing should be idempotent and queued through a worker to avoid blocking on Stripe acknowledgment.

**Security:** Never log full card numbers or CVV. Use Stripe's PCI-compliant hosted fields or Elements for card data collection. Store only the last four digits and expiration month/year in your database. Rotate Stripe API keys regularly. Validate webhook signatures using the webhook secret. Restrict API key permissions to the minimum required operations.

**Monitoring:** Track charge success rate, refund rate (watch for abnormal patterns), dispute rate, webhook delivery lag, and API error rate by error type. Alert on charge failures exceeding 5% in a 5-minute window and disputes exceeding 1% of volume. Monitor Stripe API latency (p95) and webhook processing throughput. Set up daily reconciliation reports comparing Stripe balance to local payment records.
