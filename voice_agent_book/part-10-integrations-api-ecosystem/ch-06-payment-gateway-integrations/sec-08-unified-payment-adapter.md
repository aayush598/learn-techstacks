# Section 08: Unified Payment Adapter

## Overview

The Unified Payment Adapter provides a consistent abstraction layer over multiple payment gateways (Stripe, Braintree/PayPal, Square, Adyen and others), enabling the voice agent platform to process payments, manage subscriptions, and handle refunds through a single, gateway-agnostic interface. The unified adapter implements the Strategy pattern — each payment gateway has a concrete strategy class that implements the common interface, and the adapter selects the appropriate strategy at runtime based on the tenant's payment gateway configuration.

The unified adapter standardizes payment operations: payment intent creation and confirmation, refund processing, subscription lifecycle management, customer vault operations, webhook handling, and settlement reconciliation. It also provides a common data model for payment entities (PaymentIntent, Transaction, Subscription, Refund, Payout) that normalizes the different schemas from each gateway into a canonical form that the rest of the platform consumes.

## Architecture

```
                 Unified Payment Adapter Layer

   Voice Agent ←→ Unified Payment API ←→ Payment Strategy ←→ Gateway
                        |
   +----------------------------------------------------------+
   |            Unified Payment Adapter Architecture          |
   |                                                          |
   |  +----------------------------------------------------+ |
   |  |   PaymentController (Unified API Surface)          | |
   |  |   - createPayment / confirmPayment / refund        | |
   |  |   - createSubscription / changePlan / cancel       | |
   |  |   - createInvoice / recordPayment                  | |
   |  +----------------------------------------------------+ |
   |              |            |            |                 |
   |              v            v            v                 |
   |  +----------+  +----------+  +----------+  +----------+ |
   |  | Stripe   |  | Braintree|  | Square   |  | Adyen    | |
   |  | Strategy |  | Strategy |  | Strategy |  | Strategy | |
   |  +----------+  +----------+  +----------+  +----------+ |
   |                                                          |
   |  Common Data Model:                                      |
   |  - PaymentRecord (canonical)                             |
   |  - SubscriptionRecord (canonical)                        |
   |  - InvoiceRecord (canonical)                             |
   |  - RefundRecord (canonical)                              |
   |  - PayoutRecord (canonical)                              |
   +----------------------------------------------------------+
```

## Design Decisions

- **Strategy pattern with runtime resolution over static binding:** The unified adapter selects the payment strategy at runtime based on the tenant's configured gateway. Each strategy implements the `PaymentStrategy` interface and encapsulates all gateway-specific logic. New gateways can be added by implementing the interface without modifying existing code. Trade-off: runtime resolution adds a virtual method call overhead per operation but enables per-tenant gateway configuration without deployment changes.

- **Canonical data model with two-way mapping over leaky abstraction:** The adapter defines a canonical payment data model that normalizes the concepts across different gateways. Two-way mappers convert between canonical records and gateway-specific objects for both read and write operations. For fields that only exist in specific gateways (e.g., Braintree's `merchantAccountId`, Adyen's `pspReference`), the canonical model stores them in a `gatewaySpecific` JSON field. Trade-off: canonical mapping adds complexity for gateway-specific features but prevents gateway-specific concepts from leaking into the rest of the platform.

- **Webhook unification with a common event bus over per-gateway endpoints:** The unified adapter provides a single webhook endpoint that all gateway webhooks point to. The endpoint inspects the webhook payload to determine the originating gateway (based on headers or payload structure), routes to the appropriate strategy's webhook handler, and emits a normalized event to the platform's event bus. Trade-off: single endpoint requires payload inspection logic but eliminates per-gateway webhook configuration and provides consistent event handling.

## Implementation Approach

```
interface PaymentStrategy {
  readonly gatewayType: string;

  initialize(config: PaymentGatewayConfig): Promise<void>;
  healthCheck(): Promise<HealthStatus>;

  // Payment operations
  createPaymentIntent(request: PaymentIntentRequest): Promise<Result<PaymentRecord>>;
  confirmPayment(intentId: string, params?: ConfirmParams): Promise<Result<PaymentRecord>>;
  refundPayment(intentId: string, amount?: number): Promise<Result<RefundRecord>>;

  // Subscription operations
  createSubscription(request: SubscriptionRequest): Promise<Result<SubscriptionRecord>>;
  updateSubscription(id: string, updates: SubscriptionUpdate): Promise<Result<SubscriptionRecord>>;
  cancelSubscription(id: string): Promise<Result<SubscriptionRecord>>;

  // Customer operations
  createOrFetchCustomer(customerData: CustomerData): Promise<Result<string>>;
  attachPaymentMethod(customerId: string, paymentMethodId: string): Promise<Result<void>>;

  // Invoice operations
  createInvoice(request: InvoiceRequest): Promise<Result<InvoiceRecord>>;
  finalizeInvoice(id: string): Promise<Result<InvoiceRecord>>;

  // Webhook handling
  parseWebhook(payload: any, headers: Record<string, string>): Promise<WebhookEvent>;
}

abstract class BasePaymentStrategy implements PaymentStrategy {
  abstract readonly gatewayType: string;
  protected config!: PaymentGatewayConfig;

  async initialize(config: PaymentGatewayConfig): Promise<void> {
    this.config = config;
    await this.onInitialize();
  }

  protected abstract onInitialize(): Promise<void>;
  abstract healthCheck(): Promise<HealthStatus>;
  abstract createPaymentIntent(request: PaymentIntentRequest): Promise<Result<PaymentRecord>>;
  abstract confirmPayment(intentId: string, params?: ConfirmParams): Promise<Result<PaymentRecord>>;
  abstract refundPayment(intentId: string, amount?: number): Promise<Result<RefundRecord>>;
  abstract createSubscription(request: SubscriptionRequest): Promise<Result<SubscriptionRecord>>;
  abstract updateSubscription(id: string, updates: SubscriptionUpdate): Promise<Result<SubscriptionRecord>>;
  abstract cancelSubscription(id: string): Promise<Result<SubscriptionRecord>>;
  abstract createOrFetchCustomer(customerData: CustomerData): Promise<Result<string>>;
  abstract attachPaymentMethod(customerId: string, paymentMethodId: string): Promise<Result<void>>;
  abstract createInvoice(request: InvoiceRequest): Promise<Result<InvoiceRecord>>;
  abstract finalizeInvoice(id: string): Promise<Result<InvoiceRecord>>;
  abstract parseWebhook(payload: any, headers: Record<string, string>): Promise<WebhookEvent>;
}

class UnifiedPaymentAdapter {
  private strategies = new Map<string, PaymentStrategy>();

  registerStrategy(strategy: PaymentStrategy) {
    this.strategies.set(strategy.gatewayType, strategy);
  }

  async processPayment(tenantId: string, request: PaymentIntentRequest): Promise<Result<PaymentRecord>> {
    const config = await this.getTenantConfig(tenantId);
    const strategy = this.strategies.get(config.gatewayType);
    if (!strategy) return { success: false, error: `No strategy for ${config.gatewayType}` };

    const result = await strategy.createPaymentIntent(request);
    if (result.success) {
      await this.emitEvent('payment.created', {
        tenantId,
        gatewayType: config.gatewayType,
        payment: result.data,
      });
    }
    return result;
  }

  async handleWebhook(payload: any, headers: Record<string, string>): Promise<void> {
    const gatewayType = this.detectGateway(payload, headers);
    const strategy = this.strategies.get(gatewayType);
    if (!strategy) throw new Error(`Unknown gateway: ${gatewayType}`);

    const event = await strategy.parseWebhook(payload, headers);
    await this.eventBus.emit(event.type, {
      gatewayType,
      gatewayEventId: event.id,
      data: event.data,
    });
  }

  private detectGateway(payload: any, headers: Record<string, string>): string {
    if (headers['stripe-signature']) return 'stripe';
    if (headers['braintree-signature']) return 'braintree';
    if (payload.NotificationRequestItem?.pspReference) return 'adyen';
    if (payload.merchant_id) return 'square';
    throw new Error('Unable to detect payment gateway from webhook payload');
  }
}

// Canonical Payment Record
interface PaymentRecord {
  id: string;
  gatewayType: string;
  gatewayPaymentId: string;
  status: PaymentStatus;
  amount: number;
  currency: string;
  customerId: string;
  paymentMethodType?: string;
  failureReason?: string;
  metadata: Record<string, string>;
  createdAt: Date;
  gatewaySpecific: Record<string, any>;
}

type PaymentStatus = 'pending' | 'requires_action' | 'processing' | 'succeeded' | 'failed' | 'refunded' | 'partially_refunded';
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Zod (MIT) | Validation | Unified schema validation |
| P-map (MIT) | Concurrency | Parallel gateway operations |
| Pino (MIT) | Logging | Structured payment logs |

## Production Considerations

**Scaling:** The unified adapter is a critical path in payment flows — latency adds directly to call duration. Keep strategy resolution cached (in-memory map, refreshed every 60 seconds). Use connection pooling per strategy instance. The webhook handler must be horizontally scalable — process webhook events on a distributed queue (Bull/BullMQ with Redis) and deduplicate by gateway event ID.

**Security:** The unified adapter should never log payment data across strategies — use a common sanitization layer that redacts sensitive fields before any logging. Strategy implementations inherit the security posture of their respective gateways. The webhook endpoint must validate signatures for all gateways. Tenant configuration (API keys, secrets) must be encrypted at rest and decrypted per-request in the adapter's memory space.

**Monitoring:** Track per-strategy metrics: operation latency, success/failure rates, error code distribution, webhook processing lag, and strategy initialization time. Monitor strategy health checks and alert on unhealthy strategies. Track the distribution of payment volume across gateways (useful for cost optimization and A/B testing). Monitor webhook deduplication rates and alert on duplicate events exceeding 1%.
