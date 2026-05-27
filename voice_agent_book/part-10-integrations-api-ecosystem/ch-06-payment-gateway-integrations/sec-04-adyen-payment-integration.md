# Section 04: Adyen Payment Integration

## Overview

The Adyen Payment integration adapter enables the voice agent platform to process payments through Adyen's unified commerce platform, supporting credit/debit cards, digital wallets (Apple Pay, Google Pay), local payment methods (iDEAL, Bancontact, SEPA), and buy-now-pay-later options (Klarna, Afterpay). Adyen is especially relevant for global voice agent deployments requiring multi-currency, cross-border payment processing with local acquiring.

The adapter implements Adyen's Checkout API (v71) for payment processing, the Recurring API for stored payment methods and subscription billing, the Payout API for mass payouts to connected accounts, and the webhook notification system for asynchronous payment state updates. Adyen's unique selling proposition is its single integration point for 250+ payment methods and 150+ currencies through one API contract, making it ideal for international voice agent deployments.

## Architecture

```
                    Adyen Payment Integration

   Voice Agent ←→ Payment Gateway ←→ Adyen Adapter ←→ Adyen API
                                                           |
   +-------------------------------------------------------+
   |                  Adyen Adapter Layer                  |
   |                                                       |
   |  +----------------+  +----------------+  +----------+ |
   |  | Checkout API   |  | Recurring API  |  | Payouts  | |
   |  | • Sessions     |  | • Stored PM    |  | • Instant| |
   |  | • Payments     |  | • Schedules    |  | • Batch  | |
   |  | • 3DS          |  | • Disable      |  | • Review | |
   |  +----------------+  +----------------+  +----------+ |
   |  +----------------+  +----------------+               |
   |  | Local PMs      |  | Notifications  |               |
   |  | • iDEAL        |  | • Webhooks     |               |
   |  | • SEPA         |  | • HMAC verify  |               |
   |  | • Klarna/BNPL  |  | • Retry queue  |               |
   |  +----------------+  +----------------+               |
   +-------------------------------------------------------+
```

## Design Decisions

- **Session-based checkout over direct payment submission:** For voice payments, the server creates an Adyen checkout session with the amount, currency, return URL, and allowed payment methods. The session returns a payment link that can be sent to the customer via SMS or email for self-service payment, or processed server-side when card details are collected via DTMF. Trade-off: session-based flow requires an additional redirect step but provides better 3DS handling and fraud scoring.

- **Risk-based routing between payment methods:** The adapter uses Adyen's risk analysis (fraud scores, transaction velocity, device fingerprinting) to recommend the optimal payment method and processing route. For low-risk voice transactions, card payments are processed directly. For high-risk transactions, the flow routes to manual review or alternative payment methods with better liability shift. Trade-off: risk analysis adds latency but reduces chargeback exposure on voice payments.

- **Webhook-driven state machine for payment reconciliation:** Adyen sends webhooks for every state transition (authorisation, capture, refund, chargeback). The adapter maintains a local payment state machine and transitions on each webhook event, matching against the pspReference. The final settlement confirmation webhook triggers order fulfillment. Trade-off: the state machine must handle out-of-order and duplicate webhook delivery but provides reliable payment reconciliation.

## Implementation Approach

```
interface AdyenAdapterConfig {
  apiKey: string;
  merchantAccount: string;
  hmacKey: string;
  liveEndpointUrlPrefix?: string;
  environment: 'test' | 'live';
}

interface CheckoutSessionRequest {
  amount: { value: number; currency: string };
  reference: string;
  returnUrl: string;
  allowedPaymentMethods?: string[];
  shopperLocale?: string;
  metadata?: Record<string, string>;
}

class AdyenPaymentAdapter extends BasePaymentAdapter {
  private client: Adyen.Client;
  private checkout: Adyen.CheckoutAPI;
  private recurring: Adyen.RecurringAPI;

  constructor(config: AdyenAdapterConfig) {
    super(config);
    this.client = new Adyen.Client({
      apiKey: config.apiKey,
      environment: config.environment === 'test' ? 'TEST' : 'LIVE',
      liveEndpointUrlPrefix: config.liveEndpointUrlPrefix,
    });
    this.checkout = new Adyen.CheckoutAPI(this.client);
    this.recurring = new Adyen.RecurringAPI(this.client);
  }

  async createCheckoutSession(request: CheckoutSessionRequest): Promise<AdapterResponse<SessionResult>> {
    const session = await this.checkout.PaymentsApi.sessions({
      amount: request.amount,
      reference: request.reference,
      returnUrl: request.returnUrl,
      merchantAccount: this.config.merchantAccount,
      allowedPaymentMethods: request.allowedPaymentMethods,
      shopperLocale: request.shopperLocale,
      metadata: request.metadata,
      channel: 'iOS',  // Voice payments treated as app-based
    });

    return {
      success: true,
      data: {
        sessionId: session.id,
        sessionData: session.sessionData,
        url: session.url!,
        expiresAt: session.expiresAt,
      },
    };
  }

  async submitPayment(details: {
    sessionData: string;
    paymentMethod: Record<string, string>;
  }): Promise<AdapterResponse<PaymentResult>> {
    const response = await this.checkout.PaymentsApi.payments({
      sessionData: details.sessionData,
      paymentMethod: details.paymentMethod,
      merchantAccount: this.config.merchantAccount,
    });

    return {
      success: response.resultCode === 'Authorised' || response.resultCode === 'Received',
      data: {
        pspReference: response.pspReference,
        resultCode: response.resultCode as PaymentResult['resultCode'],
        refusalReason: response.refusalReason,
        additionalData: response.additionalData,
      },
    };
  }

  async verifyWebhookNotification(notification: {
    payload: string;
    hmacSignature: string;
  }): Promise<boolean> {
    return Adyen.HMACValidator.validateHMAC(
      notification.payload,
      this.config.hmacKey,
      notification.hmacSignature
    );
  }

  async listStoredPaymentMethods(shopperReference: string): Promise<AdapterResponse<StoredPM[]>> {
    const response = await this.recurring.RecurringApi.listRecurringDetails({
      merchantAccount: this.config.merchantAccount,
      shopperReference,
      recurring: { contract: 'RECURRING' },
    });
    const methods = response.details?.flatMap(d => d?.RecurringDetail || []) || [];
    return {
      success: true,
      data: methods.map(m => ({
        recurringDetailReference: m.recurringDetailReference,
        variant: m.variant,
        lastFour: m.card?.number || '',
        expiryMonth: m.card?.expiryMonth || '',
        expiryYear: m.card?.expiryYear || '',
      })),
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Adyen SDK (MIT) | Node.js | Adyen API client |
| Adyen HMAC (MIT) | Node.js | Webhook verification |
| P-map (MIT) | Concurrency | Parallel payment operations |

## Production Considerations

**Scaling:** Adyen rate limits vary by endpoint (checkout sessions: 60/min, payments: 300/min). Implement progressive rate limiting per merchant account. Cache recurring contract lookups in Redis (15-minute TTL). Process webhook notifications on a dedicated worker queue with at-least-once delivery semantics. Use Adyen's balance platform for marketplace deployments with split payments.

**Security:** The Adyen API key provides full account access — restrict to production-only in vault storage. Never log the API key or HMAC key. Use Adyen's 3DS2 for voice payments processed server-side to shift liability. Implement server-side origin checks on webhook endpoints to prevent CSRF. Store only the pspReference and last four digits locally. Enable PCI DSS SAQ A compliance by using Adyen's hosted payment pages.

**Monitoring:** Track authorization rates by payment method and currency, 3DS challenge rates, refund-to-sale ratios, chargeback rates by reason code, and webhook processing lag. Monitor Adyen's performance endpoint for API availability. Alert on authorization rate drops exceeding 5%, chargeback ratios approaching thresholds, webhook queue backlogs, and settlement timing deviations. Set up daily reconciliation using Adyen's settlement reports API.
