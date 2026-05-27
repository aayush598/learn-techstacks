# Section 02: Braintree/PayPal Integration

## Overview

The Braintree/PayPal integration adapter enables voice agents to process payments through Braintree's payment gateway, including PayPal transactions, credit/debit cards, and digital wallets like Venmo and Apple Pay. Braintree provides a unified API that aggregates multiple payment methods under a single integration, making it ideal for platforms that need to offer diverse payment options without managing individual gateway integrations. The adapter handles transaction creation, customer vault management, subscription billing, and settlement reconciliation.

Braintree's client token generation enables PCI-compliant card data collection via the Braintree Drop-In UI or Hosted Fields for voice-based payment flows. The adapter supports Braintree's Transparent Redirect for server-side payment processing, which is critical for voice calls where the agent captures payment information via DTMF input. The integration also handles PayPal billing agreements for recurring payments and instant settlement via Braintree's merchant account configuration.

## Architecture

```
                  Braintree/PayPal Integration

   Voice Call ←→ Payment Gateway ←→ Braintree Adapter ←→ Braintree API
                                                              |
   +----------------------------------------------------------+
   |                 Braintree Adapter Flow                    |
   |                                                          |
   |  +----------------+  +---------------+  +--------------+ |
   |  | Client Token   |  | Transaction   |  | Customer     | |
   |  | Generation     |  | • Sale        |  | Vault        | |
   |  | • Auth intent  |  | • Auth/Capture|  | • Create     | |
   |  | • Nonce        |  | • Refund/Void |  | • Payment    | |
   |  | verification   |  | • Settlement  |  |   methods    | |
   |  +----------------+  +---------------+  +--------------+ |
   |  +----------------+  +---------------+  +--------------+ |
   |  | PayPal         |  | Subscriptions |  | Reporting    | |
   |  | • Billing      |  | • Recurring   |  | • Settlement | |
   |  |   agreements   |  | • Plan        |  | • Disputes   | |
   |  | • Payouts      |  |   management  |  | • Reconcile  | |
   |  +----------------+  +---------------+  +--------------+ |
   +----------------------------------------------------------+
```

## Design Decisions

- **Client token-based auth over server-side credentials for PCI scope:** Braintree's client-side authentication uses a client token generated server-side per transaction. The token authorizes a single payment operation without exposing the merchant API credentials. For voice flows, the server generates a client token, the agent collects card details through DTMF (passed to Braintree via server-side API), and the transaction is processed server-side. Trade-off: server-side processing increases PCI scope but enables full control over the voice payment flow.

- **Separate merchant account per tenant for marketplace platforms:** In multi-tenant deployments, each tenant can have a dedicated Braintree merchant account, enabling independent settlement, fee structures, and reporting. The adapter routes transactions to the appropriate merchant account based on the tenant configuration. Trade-off: per-tenant merchant accounts increase operational overhead (each requires underwriting) but provides clear financial separation and regulatory compliance.

- **Authorization-only with delayed capture for voice transactions:** Voice payments use a two-phase flow: authorize the amount when the customer provides card details, then capture when the order is fulfilled. This prevents charging the customer before the service is delivered (e.g., the call analysis completes). Authorization holds expire after 29 days. Trade-off: two-phase adds implementation complexity but prevents chargebacks from undelivered services.

## Implementation Approach

```
interface BraintreeAdapterConfig {
  merchantId: string;
  publicKey: string;
  privateKey: string;
  environment: 'sandbox' | 'production';
  merchantAccountId?: string;
}

interface TransactionRequest {
  amount: number;
  paymentMethodNonce?: string;
  customerId?: string;
  deviceData?: string;
  options: {
    submitForSettlement: boolean;
    storeInVaultOnSuccess: boolean;
  };
  idempotencyKey: string;
}

class BraintreePaymentAdapter extends BasePaymentAdapter {
  private gateway: braintree.BraintreeGateway;

  constructor(config: BraintreeAdapterConfig) {
    super(config);
    this.gateway = new braintree.BraintreeGateway({
      environment: config.environment === 'production'
        ? braintree.Environment.Production
        : braintree.Environment.Sandbox,
      merchantId: config.merchantId,
      publicKey: config.publicKey,
      privateKey: config.privateKey,
    });
  }

  async generateClientToken(customerId?: string): Promise<AdapterResponse<string>> {
    const result = await this.gateway.clientToken.generate({
      customerId,
      merchantAccountId: this.config.merchantAccountId,
    });
    return { success: true, data: result.clientToken };
  }

  async createTransaction(
    request: TransactionRequest
  ): Promise<AdapterResponse<TransactionResult>> {
    const saleRequest: braintree.TransactionRequest = {
      amount: String(request.amount),
      paymentMethodNonce: request.paymentMethodNonce,
      customerId: request.customerId,
      options: request.options,
      deviceData: request.deviceData,
      merchantAccountId: this.config.merchantAccountId,
    };

    const result = await this.gateway.transaction.sale(saleRequest);
    if (!result.success) {
      return {
        success: false,
        data: null as any,
        error: result.message || 'Transaction failed',
      };
    }
    return {
      success: true,
      data: this.mapTransaction(result.transaction!),
    };
  }

  async submitForSettlement(transactionId: string, amount?: number): Promise<AdapterResponse<void>> {
    const result = await this.gateway.transaction.submitForSettlement(
      transactionId, amount ? String(amount) : undefined
    );
    return { success: result.success, data: undefined };
  }

  private mapTransaction(tx: braintree.Transaction): TransactionResult {
    return {
      transactionId: tx.id,
      status: tx.status,
      amount: parseFloat(tx.amount),
      currency: tx.currencyIsoCode,
      createdAt: tx.createdAt,
      processorResponse: tx.processorResponseText,
      paymentMethodType: tx.paymentInstrumentType,
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Braintree SDK (MIT) | Node.js | Braintree API client |
| PayPal SDK (MIT) | Node.js | PayPal REST API |
| NanoId (MIT) | IDs | Idempotency key generation |
| Luxon (MIT) | Dates | Settlement date calculations |

## Production Considerations

**Scaling:** Braintree enforces rate limits of 60 requests per 10 seconds per merchant. Implement a token bucket rate limiter per merchant account. Reuse gateway instances across requests — they are thread-safe and maintain connection pools. Transaction ID lookups should be cached in Redis (30-second TTL) to reduce duplicate API calls during order processing.

**Security:** The private key must be stored encrypted with envelope encryption. Never expose the private key in client-side code. Use Braintree's Advanced Fraud Tools (device data collection, Kount integration) for voice-based transactions where card-not-present risk is higher. Enable CVV and AVS verification rules in the Braintree control panel. Log transaction IDs without full card data.

**Monitoring:** Track auth-to-capture ratios, settlement timing (same-day vs. next-day), refund rates, chargeback ratios, and processor decline codes. Monitor authorization hold expiry rates (conversions lost due to expired holds). Alert on settlement failures, elevated decline rates (>10%), and chargeback ratio approaching Visa/Mastercard thresholds. Reconcile settled transactions daily against the bank statement.
