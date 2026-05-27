# Section 08: Stripe Test Mode Strategy

## Test Clock Usage

Stripe's test clock allows simulating time-based billing scenarios: subscription creation, invoice generation, payment attempts, and plan changes. This is essential for testing the entire subscription lifecycle without waiting for real time.

```typescript
class TestClockService {
  async createTestClock(
    name: string,
    frozenTime: Date
  ): Promise<Stripe.TestHelpers.TestClock> {
    return await stripe.testHelpers.testClocks.create({
      name,
      frozen_time: Math.floor(frozenTime.getTime() / 1000),
    });
  }

  async advanceTestClock(
    clockId: string,
    targetTime: Date
  ): Promise<Stripe.TestHelpers.TestClock> {
    return await stripe.testHelpers.testClocks.advance(clockId, {
      frozen_time: Math.floor(targetTime.getTime() / 1000),
    });
  }

  async runSubscriptionLifecycleTest(): Promise<void> {
    // Create test clock frozen at subscription start
    const clock = await this.createTestClock('lifecycle-test', new Date('2025-06-01'));

    // Create test customer
    const customer = await stripe.customers.create({
      name: 'Test Customer',
      email: 'test@example.com',
      test_clock: clock.id,
    });

    // Create subscription with trial
    const subscription = await stripe.subscriptions.create({
      customer: customer.id,
      items: [{ price: 'price_test_monthly' }],
      trial_period_days: 14,
      test_clock: clock.id,
    });

    // Advance to trial end
    await this.advanceTestClock(clock.id, new Date('2025-06-15'));

    // Verify trial converted and invoice generated
    const updatedSub = await stripe.subscriptions.retrieve(subscription.id);
    console.assert(updatedSub.status === 'active', 'Trial should convert to active');

    // Advance to end of billing period
    await this.advanceTestClock(clock.id, new Date('2025-07-01'));

    // Verify new invoice was created
    const invoices = await stripe.invoices.list({
      customer: customer.id,
    });
    console.assert(invoices.data.length >= 2, 'Should have multiple invoices');

    // Clean up
    await stripe.testHelpers.testClocks.delete(clock.id);
  }
}
```

## Test Card Numbers

Stripe provides specific card numbers that trigger different payment outcomes: success, decline, requires authentication, and more. These are essential for testing payment scenarios.

```typescript
const TEST_CARD_NUMBERS = {
  // Success scenarios
  success: '4242424242424242',
  success_visa: '4242424242424242',
  success_mastercard: '5555555555554444',
  success_amex: '378282246310005',

  // Authentication required
  requires_auth: '4000002500003155',
  requires_3ds: '4000002760003184',

  // Decline scenarios
  declined_generic: '4000000000000002',
  declined_insufficient_funds: '4000000000009995',
  declined_stolen_card: '4000000000009979',
  declined_expired_card: '4000000000000069',
  declined_processing_error: '4000000000000119',

  // SEPA
  sepa_success: 'DE89370400440532013000',
  sepa_fail: 'DE62370400440532013001',

  // ACH
  ach_success: '000123456789',
  ach_fail: '000123456788',
};

function getTestPaymentMethod(cardNumber: string): Stripe.PaymentMethodCreateParams {
  return {
    type: 'card',
    card: {
      number: cardNumber,
      exp_month: 12,
      exp_year: 2030,
      cvc: '123',
    },
  };
}
```

## Webhook Simulation

The Stripe CLI supports triggering webhook events for testing. This is essential for verifying webhook handler logic without a real Stripe integration.

```typescript
// Stripe CLI commands for webhook testing
// stripe trigger customer.subscription.created
// stripe trigger invoice.paid
// stripe trigger invoice.payment_failed
// stripe trigger payment_intent.succeeded

class WebhookTestSimulator {
  async simulateWebhook(
    eventType: string,
    data?: Record<string, any>
  ): Promise<void> {
    const { execSync } = require('child_process');

    const cmd = [
      'stripe',
      'trigger',
      eventType,
      ...(data ? Object.entries(data).map(([k, v]) => `--override ${k}=${v}`) : []),
    ].join(' ');

    execSync(cmd, { stdio: 'inherit' });
  }

  async runWebhookTestSuite(): Promise<void> {
    const scenarios = [
      { type: 'customer.subscription.created', description: 'New subscription' },
      { type: 'customer.subscription.updated', description: 'Subscription update' },
      { type: 'customer.subscription.deleted', description: 'Subscription cancel' },
      { type: 'invoice.paid', description: 'Payment success' },
      { type: 'invoice.payment_failed', description: 'Payment failure' },
      { type: 'invoice.upcoming', description: 'Upcoming invoice' },
      { type: 'payment_intent.succeeded', description: 'Payment intent success' },
      { type: 'payment_intent.payment_failed', description: 'Payment intent failure' },
    ];

    for (const scenario of scenarios) {
      console.log(`Testing: ${scenario.description}`);
      await this.simulateWebhook(scenario.type);
    }
  }
}
```

## Testing Billing Scenarios

Comprehensive billing tests cover subscription lifecycle, proration, metered billing, invoice generation, and dunning scenarios.

```typescript
class BillingTestSuite {
  async runAllTests(): Promise<TestResult[]> {
    return [
      await this.testCreateSubscription(),
      await this.testUpgradePlan(),
      await this.testDowngradePlan(),
      await this.testCancelSubscription(),
      await this.testProration(),
      await this.testMeteredBilling(),
      await this.testFreeTrial(),
      await this.testPaymentFailure(),
      await this.testPaymentMethodUpdate(),
      await this.testInvoiceGeneration(),
      await this.testCreditNotes(),
    ];
  }

  async testMeteredBilling(): Promise<TestResult> {
    const clock = await this.createTestClock('metered-test', new Date('2025-06-01'));
    const customer = await stripe.customers.create({
      name: 'Metered Test',
      test_clock: clock.id,
    });

    const subscription = await stripe.subscriptions.create({
      customer: customer.id,
      items: [
        { price: 'price_flat' },
        { price: 'price_metered' },
      ],
      test_clock: clock.id,
    });

    // Submit usage records
    const meteredItem = subscription.items.data.find(
      i => i.price.id === 'price_metered'
    );

    await stripe.subscriptionItems.createUsageRecord(meteredItem.id, {
      quantity: 500,
      timestamp: Math.floor(new Date('2025-06-15').getTime() / 1000),
    });

    await stripe.subscriptionItems.createUsageRecord(meteredItem.id, {
      quantity: 300,
      timestamp: Math.floor(new Date('2025-06-20').getTime() / 1000),
    });

    // Advance to period end
    await this.advanceTestClock(clock.id, new Date('2025-07-01'));

    // Verify invoice includes metered charges
    const invoices = await stripe.invoices.list({ customer: customer.id });
    const invoice = invoices.data[0];
    const meteredLine = invoice.lines.data.find(l => l.price.id === 'price_metered');

    const passed = meteredLine && meteredLine.quantity === 800;
    return {
      name: 'Metered billing with usage records',
      passed,
      details: passed
        ? `Metered line: ${meteredLine.quantity} units at $${meteredLine.unit_amount/100}`
        : 'Metered line not found or quantity incorrect',
    };
  }
}
```

## Open-Source Tools

- **Stripe CLI** — Webhook simulation and test mode management
- **Stripe API** — Test clock creation and management
- **Jest** (MIT) — Test framework for automated billing tests
- **PostgreSQL** — Test database for integration testing

## Integration Points

Test mode strategy covers all billing components: subscription lifecycle, webhook handling, invoice generation, tax calculation, dunning management, and payment method management.

## Production Considerations

- Run billing test suite in CI/CD pipeline for every deployment
- Maintain separate Stripe test mode credentials from production
- Use distinct test API keys for different environments
- Regularly clean up test clock data to avoid clutter
- Document test scenarios for onboarding new developers

## Open-Source First Philosophy

Stripe's test mode is free with no usage limits. Jest provides the automated testing framework at no cost. The combination enables comprehensive billing testing without expensive test infrastructure. All test artifacts (test plans, scenarios, data) are stored in the git repository as code, maintaining the open-source first philosophy of code-as-configuration.
