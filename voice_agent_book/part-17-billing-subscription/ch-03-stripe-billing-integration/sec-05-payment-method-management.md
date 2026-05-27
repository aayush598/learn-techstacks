# Section 05: Payment Method Management

## Card Setup via Stripe Elements

Payment method collection uses Stripe Elements, a set of pre-built UI components that securely capture card details without exposing sensitive data to our servers. Elements tokens are exchanged for PaymentMethod objects on the Stripe Customer.

```typescript
// Frontend: Stripe Elements Integration (React)
function PaymentMethodForm({ onSuccess }: { onSuccess: (pmId: string) => void }) {
  const stripe = useStripe();
  const elements = useElements();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!stripe || !elements) return;

    const { error, paymentMethod } = await stripe.createPaymentMethod({
      type: 'card',
      card: elements.getElement(CardNumberElement),
      billing_details: {
        name: customerName,
        email: customerEmail,
      },
    });

    if (error) {
      setError(error.message);
      return;
    }

    // Attach to customer via backend
    const result = await fetch('/api/billing/payment-methods', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        paymentMethodId: paymentMethod.id,
        setAsDefault: true,
      }),
    });

    if (result.ok) {
      onSuccess(paymentMethod.id);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <CardNumberElement />
      <CardExpiryElement />
      <CardCvcElement />
      <button type="submit">Add Payment Method</button>
    </form>
  );
}

// Backend: Attach payment method
async function attachPaymentMethod(
  tenantId: string,
  paymentMethodId: string,
  setAsDefault: boolean
): Promise<void> {
  const stripeCustomerId = await getStripeCustomerId(tenantId);

  // Attach to customer
  await stripe.paymentMethods.attach(paymentMethodId, {
    customer: stripeCustomerId,
  });

  if (setAsDefault) {
    // Set as default payment method
    await stripe.customers.update(stripeCustomerId, {
      invoice_settings: {
        default_payment_method: paymentMethodId,
      },
    });

    // Update internal record
    await db.tenants.updateOne(
      { id: tenantId },
      { $set: { defaultPaymentMethod: paymentMethodId } }
    );
  }

  // Log payment method addition
  await auditLogService.log({
    tenantId,
    action: 'payment_method_added',
    details: { paymentMethodId, setAsDefault },
  });
}
```

## Payment Method Updates

Customers can update their payment method through the Customer Portal or directly in the app. Updates involve attaching a new payment method and optionally setting it as the default.

```typescript
class PaymentMethodService {
  async listPaymentMethods(tenantId: string): Promise<PaymentMethod[]> {
    const stripeCustomerId = await this.getStripeCustomerId(tenantId);

    const methods = await stripe.paymentMethods.list({
      customer: stripeCustomerId,
      type: 'card',
    });

    return methods.data.map(m => ({
      id: m.id,
      brand: m.card.brand,
      last4: m.card.last4,
      expMonth: m.card.exp_month,
      expYear: m.card.exp_year,
      isDefault: m.id === this.defaultPaymentMethodId,
      isExpiring: m.card.exp_year === new Date().getFullYear()
        && m.card.exp_month <= new Date().getMonth() + 1,
    }));
  }

  async detachPaymentMethod(tenantId: string, paymentMethodId: string): Promise<void> {
    const stripeCustomerId = await this.getStripeCustomerId(tenantId);

    // Check if this is the default method
    const customer = await stripe.customers.retrieve(stripeCustomerId);
    if (customer.invoice_settings?.default_payment_method === paymentMethodId) {
      throw new Error('Cannot detach default payment method. Set a new default first.');
    }

    await stripe.paymentMethods.detach(paymentMethodId);

    await auditLogService.log({
      tenantId,
      action: 'payment_method_removed',
      details: { paymentMethodId },
    });
  }

  async setDefaultPaymentMethod(tenantId: string, paymentMethodId: string): Promise<void> {
    const stripeCustomerId = await this.getStripeCustomerId(tenantId);

    await stripe.customers.update(stripeCustomerId, {
      invoice_settings: {
        default_payment_method: paymentMethodId,
      },
    });

    await this.db.tenants.updateOne(
      { id: tenantId },
      { $set: { defaultPaymentMethod: paymentMethodId } }
    );
  }
}
```

## SEPA/ACH Support

European customers prefer SEPA Direct Debit, and US customers prefer ACH. Stripe supports both payment methods. The integration uses Stripe Elements to collect the necessary account information.

```typescript
interface SepaDebitConfig {
  type: 'sepa_debit';
  iban: string;
  billingDetails: {
    name: string;
    email: string;
    address?: Stripe.Address;
  };
}

interface AchConfig {
  type: 'us_bank_account';
  accountNumber: string;
  routingNumber: string;
  accountHolderName: string;
  accountHolderType: 'individual' | 'company';
}

async function createSepaPaymentMethod(
  tenantId: string,
  config: SepaDebitConfig
): Promise<Stripe.PaymentMethod> {
  const paymentMethod = await stripe.paymentMethods.create({
    type: 'sepa_debit',
    sepa_debit: {
      iban: config.iban,
    },
    billing_details: config.billingDetails,
  });

  const stripeCustomerId = await getStripeCustomerId(tenantId);
  await stripe.paymentMethods.attach(paymentMethod.id, {
    customer: stripeCustomerId,
  });

  return paymentMethod;
}
```

```
Payment Method Decision Matrix:
┌──────────────────────────────────────────────────────────────────┐
│ Region    │ Primary         │ Secondary      │ Use Case          │
├───────────┼─────────────────┼────────────────┼───────────────────┤
│ US        │ Credit Card     │ ACH            │ Most customers    │
│ EU        │ SEPA Direct Debit│ Credit Card   │ Lower fees (EU)   │
│ UK        │ Card             │ BACS Direct Debit │ Common for B2B│
│ Australia │ Card             │ BECS           │ Local preference │
│ Asia      │ Card             │ Konbini (JP)   │ Alternative methods │
│ Global    │ PayPal           │ Wire Transfer  │ B2B preference   │
└──────────────────────────────────────────────────────────────────┘
```

## Open-Source Tools

- **Stripe Elements** — Secure payment form components
- **PostgreSQL** — Payment method metadata storage
- **Redis** — Cache default payment method for fast retrieval
- **BullMQ** — Schedule payment method expiry notifications

## Integration Points

Payment method management integrates with the subscription service (for auto-charging), the customer portal (for self-service updates), the dunning system (Chapter 9), and the notification service (for expiry reminders).

## Production Considerations

- Handle payment method expiry (send email reminders 30 days before)
- Validate payment methods immediately on addition (charge $0 or use setup intent)
- Implement retry logic for payment method validation
- Store only payment method references, never card numbers
- Monitor payment method failure rates by type and region

## Open-Source First Philosophy

Stripe Elements provides PCI-compliant payment form components at no additional cost (Stripe's standard processing fees apply). PostgreSQL stores minimal payment metadata (last4, brand, expiry). This approach avoids the complexity and liability of handling card data directly while keeping the infrastructure simple and auditable.
