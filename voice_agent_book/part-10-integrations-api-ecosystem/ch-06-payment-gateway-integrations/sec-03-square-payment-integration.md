# Section 03: Square Payment Integration

## Overview

The Square Payment integration adapter enables voice agents to process payments through Square's payment ecosystem, including point-of-sale transactions, e-commerce charges, recurring billing, and Square Invoices. The adapter wraps Square's Connect v2 API, exposing payment operations that are optimized for telephony-based commerce scenarios such as ordering products over the phone, booking services with payment deposits, or managing subscription billing for ongoing services.

Square excels in omnichannel commerce, allowing a single merchant account to process payments across phone, web, mobile, and in-person channels. The adapter leverages Square's Customers API for unified customer profiles, the Catalog API for product/service lookups during voice calls, and the Payments API for transaction processing. The integration also supports Square's Terminal API for scenarios where a physical card reader is used in conjunction with a voice call (e.g., curbside pickup payments).

## Architecture

```
                    Square Payment Integration

   Voice Agent ←→ Payment Gateway ←→ Square Adapter ←→ Square API
                                                              |
   +----------------------------------------------------------+
   |                Square Adapter Components                 |
   |                                                          |
   |  +------------------+  +------------------+  +---------+ |
   |  | Catalog Lookup   |  | Checkout Creation|  | Payment | |
   |  | • Items          |  | • Order creation |  | Process | |
   |  | • Variations     |  | • Payment link   |  | • Card  | |
   |  | • Modifiers      |  | • Terminal push  |  | • Cash  | |
   |  +------------------+  +------------------+  +---------+ |
   |  +------------------+  +------------------+  +---------+ |
   |  | Recurring        |  | Invoices         |  | Refund  | |
   |  | • Subscription   |  | • Create/send    |  | • Full  | |
   |  | • Plan           |  | • Payment        |  | • Partial| |
   |  | • Charging       |  |   reminders      |  | • Void  | |
   |  +------------------+  +------------------+  +---------+ |
   +----------------------------------------------------------+
```

## Design Decisions

- **Catalog-driven pricing over hard-coded amounts:** During a voice call, the agent can look up items from Square's Catalog API, get current prices, and build an order in real time. The order total is computed server-side using Square's Orders API, which applies taxes, discounts, and modifiers consistently. This prevents pricing discrepancies between voice orders and in-store orders. Trade-off: catalog lookups add API latency during calls but ensure pricing accuracy and consistency across channels.

- **Sandbox-first development with webhook simulation:** Square provides a robust sandbox environment with simulated payment cards (success, decline, insufficient funds) for testing all payment scenarios. The adapter uses Square's webhook simulation endpoints to trigger events (payment.created, refund.created) during integration testing. Trade-off: testing requires maintaining separate sandbox credentials and test data but catches integration issues before production deployment.

- **Idempotency via idempotency key with order-level dedup:** Square requires idempotency keys on all payment and order mutations. The adapter generates keys from the call session ID and step sequence (e.g., `call-abc-123:order-create:1`). If a request fails with a network error, the same key is used on retry. Square deduplicates within 24 hours. Trade-off: keys must be persisted across retries but prevents duplicate charges when the client times out before receiving the response.

## Implementation Approach

```
interface SquareAdapterConfig {
  accessToken: string;
  locationId: string;
  applicationId: string;
  webhookSignatureKey: string;
  environment: 'sandbox' | 'production';
}

interface SquareOrderRequest {
  lineItems: { catalogObjectId: string; quantity: string; }[];
  customerId?: string;
  referenceId: string;
  note?: string;
}

class SquarePaymentAdapter extends BasePaymentAdapter {
  private client: Square.Client;

  constructor(config: SquareAdapterConfig) {
    super(config);
    this.client = new Square.Client({
      accessToken: config.accessToken,
      environment: config.environment === 'sandbox'
        ? Square.Environment.Sandbox : Square.Environment.Production,
    });
  }

  async createPaymentOrder(request: SquareOrderRequest): Promise<AdapterResponse<OrderResult>> {
    const orderRequest: Square.CreateOrderRequest = {
      order: {
        locationId: this.config.locationId,
        lineItems: request.lineItems.map(item => ({
          catalogObjectId: item.catalogObjectId,
          quantity: item.quantity,
        })),
        customerId: request.customerId,
        referenceId: request.referenceId,
      },
      idempotencyKey: generateIdempotencyKey(request.referenceId, 'create-order'),
    };

    const { result, errors } = await this.client.ordersApi.createOrder(orderRequest);
    if (errors?.length) {
      return { success: false, data: null as any, error: errors[0].detail };
    }
    return { success: true, data: this.mapOrder(result.order!) };
  }

  async processCardPayment(params: {
    sourceId: string; orderId: string; amount: Money;
  }): Promise<AdapterResponse<PaymentResult>> {
    const paymentRequest: Square.CreatePaymentRequest = {
      sourceId: params.sourceId,
      orderId: params.orderId,
      amountMoney: params.amount,
      locationId: this.config.locationId,
      autocomplete: true,
      idempotencyKey: generateIdempotencyKey(params.orderId, 'payment'),
    };

    const { result, errors } = await this.client.paymentsApi.createPayment(paymentRequest);
    if (errors?.length) {
      return { success: false, data: null as any, error: errors[0].detail };
    }
    return { success: true, data: this.mapPayment(result.payment!) };
  }

  async createSubscription(params: {
    planId: string; customerId: string; cardId: string;
  }): Promise<AdapterResponse<SubscriptionResult>> {
    const { result, errors } = await this.client.subscriptionsApi.createSubscription({
      locationId: this.config.locationId,
      planId: params.planId,
      customerId: params.customerId,
      cardId: params.cardId,
      idempotencyKey: generateIdempotencyKey(params.customerId + params.planId, 'sub'),
    });
    if (errors?.length) {
      return { success: false, data: null as any, error: errors[0].detail };
    }
    return { success: true, data: { id: result.subscription!.id, status: result.subscription!.status } };
  }

  async verifyWebhook(signature: string, body: string): Promise<boolean> {
    return Square.Webhook.verifySignature({
      signatureHeader: signature,
      signatureKey: this.config.webhookSignatureKey,
      body,
    });
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Square SDK (Apache 2.0) | Node.js | Square Connect v2 API |
| Zod (MIT) | Validation | Square response validation |
| Date-fns (MIT) | Dates | Subscription billing cycles |

## Production Considerations

**Scaling:** Square's API rate limit is 100 requests per minute per endpoint per location. The adapter implements a token bucket rate limiter with separate buckets for catalog, orders, payments, and subscriptions endpoints. Catalog data should be cached locally with daily synchronization to reduce read API calls. Webhook events should be processed asynchronously via a message queue to handle burst traffic during peak hours.

**Security:** Square access tokens should be scoped to the minimum required permissions (payments_write, catalog_read, customers_read). Use Square's OAuth flow for multi-tenant deployments where each merchant connects their own Square account. Never log the access token or customer card nonces. Validate webhook signatures on every incoming notification to prevent event spoofing. Store only Square-issued card IDs, never raw card data.

**Monitoring:** Track payment success rates by location, refund rate, subscription churn, average order value, and catalog cache freshness. Monitor Square API error codes by category (authentication, rate limiting, validation). Alert on payment failure rates exceeding 8%, webhook signature validation failures, and subscription billing failures. Reconcile daily sales from Square against platform records using the Square Reports API.
