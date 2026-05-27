# Section 03: Payment Method Update Flow

## Payment Link Generation

When a payment fails, the system generates secure payment update links that allow customers to update their payment method without logging into the full portal.

```
[Payment Failure Detected]
    ↓
[Generate Secure Token]
    ├── JWT with short expiration (7 days)
    ├── Token includes: subscription_id, customer_id, tenant_id
    └── Single-use or multi-use based on stage
    ↓
[Create Payment Link]
    ├── https://app.example.com/update-payment/{token}
    ├── White-labeled domain
    └── Trackable with UTM parameters
    ↓
[Send to Customer]
    ├── Email with CTA button
    ├── SMS with shortened URL
    ├── In-app notification
    └── Push notification (mobile)
    ↓
[Customer Opens Link]
    ├── Validate token
    ├── Show masked current card info
    ├── Stripe Elements or Checkout
    └── Confirm update
```

```typescript
interface PaymentUpdateToken {
  token: string;
  customerId: string;
  subscriptionId: string;
  tenantId: string;
  redirectUrl: string;
  expiresAt: string;
  maxUses: number;
  currentUses: number;
  metadata: Record<string, string>;
}

interface PaymentUpdateLink {
  url: string;
  token: PaymentUpdateToken;
  shortUrl?: string;
  qrCode?: string;
}

class PaymentLinkService {
  private readonly jwtSecret: string;
  private readonly baseUrl: string;

  async generatePaymentLink(
    subscription: Subscription,
    options?: PaymentLinkOptions
  ): Promise<PaymentUpdateLink> {
    const token: PaymentUpdateToken = {
      token: this.generateToken(),
      customerId: subscription.customerId,
      subscriptionId: subscription.id,
      tenantId: subscription.tenantId,
      redirectUrl: options?.redirectUrl || `${this.baseUrl}/billing`,
      expiresAt: this.calculateExpiry(options?.expiresInDays || 7),
      maxUses: options?.maxUses || 1,
      currentUses: 0,
      metadata: options?.metadata || {},
    };

    // Store token reference
    await this.storeToken(token);

    const url = `${this.baseUrl}/update-payment/${token.token}`;

    return {
      url,
      token,
      shortUrl: options?.shortenUrl ? await this.shortenUrl(url) : undefined,
    };
  }

  async validateToken(token: string): Promise<PaymentUpdateToken | null> {
    const stored = await this.getToken(token);
    if (!stored) return null;
    if (new Date(stored.expiresAt) < new Date()) return null;
    if (stored.currentUses >= stored.maxUses) return null;

    return stored;
  }

  async consumeToken(token: string): Promise<boolean> {
    const stored = await this.getToken(token);
    if (!stored) return false;

    stored.currentUses += 1;
    await this.updateToken(stored);
    return true;
  }

  private generateToken(): string {
    return crypto.randomBytes(32).toString('hex');
  }

  private calculateExpiry(days: number): string {
    const expiry = new Date();
    expiry.setDate(expiry.getDate() + days);
    return expiry.toISOString();
  }
}
```

## Customer Portal Redirect

For customers already authenticated, the system redirects directly to the payment update section.

```typescript
interface PortalRedirectConfig {
  returnUrl: string;
  configuration: Stripe.BillingPortal.ConfigurationCreateParams;
}

async function createPortalSession(
  customerId: string,
  subscriptionId: string
): Promise<string> {
  // Use Stripe Customer Portal or your own implementation
  const session = await stripe.billingPortal.sessions.create({
    customer: customerId,
    return_url: `${APP_URL}/billing?updated=true`,
    flow_data: {
      type: 'payment_method_update',
      after_completion: {
        type: 'redirect',
        redirect: { url: `${APP_URL}/billing` },
      },
    },
  });

  return session.url;
}

// Self-hosted payment update portal
class PaymentUpdatePortal {
  async setupPaymentUpdateSession(
    customerId: string,
    tenantId: string
  ): Promise<SetupIntent> {
    // Create a SetupIntent for saving a new payment method
    const setupIntent = await stripe.setupIntents.create({
      customer: customerId,
      usage: 'off_session',
      metadata: {
        tenant_id: tenantId,
        source: 'dunning',
      },
    });

    // Store session for tracking
    await this.storeSession({
      customerId,
      setupIntentId: setupIntent.id,
      status: 'pending',
      createdAt: new Date().toISOString(),
    });

    return setupIntent;
  }
}
```

## In-App Payment Update

The application provides an in-app payment method update flow with Stripe Elements.

```typescript
// Frontend: React component for payment method update
interface PaymentMethodUpdateProps {
  clientSecret: string;
  onSuccess: () => void;
  onError: (error: PaymentError) => void;
}

function PaymentMethodForm({ clientSecret, onSuccess, onError }: PaymentMethodUpdateProps) {
  const stripe = useStripe();
  const elements = useElements();

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();

    if (!stripe || !elements) return;

    const { error, setupIntent } = await stripe.confirmSetup({
      elements,
      confirmParams: {
        return_url: `${window.location.origin}/billing`,
      },
      redirect: 'if_required',
    });

    if (error) {
      onError({ code: error.code || 'unknown', message: error.message || '' });
      return;
    }

    // Payment method saved successfully
    await confirmUpdateToServer(setupIntent.payment_method);
    onSuccess();
  }

  return (
    <form onSubmit={handleSubmit}>
      <PaymentElement />
      <button type="submit">Update Payment Method</button>
    </form>
  );
}

// Backend: Handle successful payment method update
class PaymentMethodUpdateHandler {
  async handleWebhook(event: Stripe.Event): Promise<void> {
    if (event.type === 'setup_intent.succeeded') {
      const setupIntent = event.data.object as Stripe.SetupIntent;

      // Update default payment method on subscription
      await this.updateSubscriptionPaymentMethod(
        setupIntent.metadata.customer_id,
        setupIntent.payment_method as string
      );

      // Trigger immediate retry if there is a pending invoice
      await this.retryPendingInvoice(setupIntent.metadata.customer_id);

      // Send confirmation to customer
      await this.sendUpdateConfirmation(setupIntent.metadata.customer_id);
    }
  }

  private async updateSubscriptionPaymentMethod(
    customerId: string,
    paymentMethodId: string
  ): Promise<void> {
    // Attach payment method to customer
    await stripe.paymentMethods.attach(paymentMethodId, { customer: customerId });

    // Set as default payment method
    await stripe.customers.update(customerId, {
      invoice_settings: {
        default_payment_method: paymentMethodId,
      },
    });
  }

  private async retryPendingInvoice(customerId: string): Promise<void> {
    const pendingInvoices = await stripe.invoices.list({
      customer: customerId,
      status: 'open',
      limit: 1,
    });

    if (pendingInvoices.data.length > 0) {
      const invoice = pendingInvoices.data[0];
      await stripe.invoices.pay(invoice.id);
    }
  }
}
```

## Auto-Retry After Update

Once the payment method is updated, the system automatically retries all pending invoices.

```typescript
class AutoRetryAfterUpdate {
  private readonly retryQueue: Queue;

  async scheduleRetryAfterUpdate(
    customerId: string,
    paymentMethodId: string
  ): Promise<RetryResult> {
    // Get all unpaid invoices
    const unpaidInvoices = await this.getUnpaidInvoices(customerId);

    const results: RetryResultItem[] = [];

    for (const invoice of unpaidInvoices) {
      try {
        const paymentIntent = await stripe.invoices.pay(invoice.id, {
          payment_method: paymentMethodId,
        });

        results.push({
          invoiceId: invoice.id,
          amount: invoice.amount_due,
          status: paymentIntent.status,
          paymentIntentId: paymentIntent.id,
        });

        // Small delay between retries to avoid rate limits
        await delay(200);
      } catch (error) {
        results.push({
          invoiceId: invoice.id,
          amount: invoice.amount_due,
          status: 'failed',
          error: error.message,
        });
      }
    }

    // Update dunning state
    const allSuccess = results.every(r => r.status === 'succeeded' || r.status === 'requires_capture');
    if (allSuccess) {
      await this.resolveDunning(customerId);
    }

    return {
      customerId,
      paymentMethodId,
      retriedCount: results.length,
      successCount: results.filter(r => r.status === 'succeeded').length,
      results,
    };
  }
}
```

## Open-Source Tools

- **Stripe** — Payment method storage and setup intents
- **BullMQ** — Retry scheduling after payment method update
- **Redis** — Token storage for payment links
- **PostgreSQL** — Payment method update audit trail
- **Handlebars** (MIT) — Email templates for payment update links
- **QRCode** (MIT) — QR code generation for payment links

## Integration Points

Payment method update flow integrates with the dunning workflow (triggers on failure), notification service (sends payment links), subscription management (updates payment method reference), and payment gateway (processes the update).

## Production Considerations

- Expire payment links after 7 days for security
- Log all payment method update attempts for fraud analysis
- Notify customer immediately on successful update
- Handle concurrent update requests gracefully
- Validate payment method before attaching to subscription
- Support multiple payment methods per customer
- Implement rate limiting on token generation
- Support SCA (Strong Customer Authentication) for European customers

## Open-Source First Philosophy

BullMQ orchestrates the auto-retry flow after payment updates. Redis provides ephemeral token storage with automatic expiry. PostgreSQL maintains the permanent audit trail. Handlebars renders payment update email templates. This open-source stack replaces proprietary solutions like Chargebee's payment update flows while providing more flexibility and control.
