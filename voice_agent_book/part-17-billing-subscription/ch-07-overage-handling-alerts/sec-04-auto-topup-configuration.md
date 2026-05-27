# Section 04: Auto-Topup Configuration

## Auto-Recharge Threshold

Auto-topup automatically purchases additional credits when the balance drops below a configurable threshold. This prevents service interruption and provides peace of mind for customers.

```typescript
interface AutoTopupConfig {
  tenantId: string;
  enabled: boolean;
  triggerBalance: number;       // Credits balance triggering topup
  topupAmount: number;           // Credits to purchase
  topupPackId: string;           // Which credit pack to purchase
  maxTopupsPerPeriod: number;   // Maximum topups per billing period
  paymentMethodId: string;       // Payment method to charge
  notificationOnTopup: boolean;
  status: 'active' | 'paused' | 'disabled';
}

class AutoTopupService {
  async configureAutoTopup(
    tenantId: string,
    config: Omit<AutoTopupConfig, 'tenantId' | 'status'>
  ): Promise<void> {
    // Validate payment method
    const methods = await this.paymentMethodService.listPaymentMethods(tenantId);
    if (!methods.find(m => m.id === config.paymentMethodId)) {
      throw new Error('Invalid payment method');
    }

    // Validate credit pack
    const pack = CREDIT_PACK_TIERS.find(p => p.id === config.topupPackId);
    if (!pack) throw new Error('Invalid credit pack');

    await this.db.autoTopupConfigs.updateOne(
      { tenantId },
      {
        $set: {
          ...config,
          tenantId,
          status: 'active',
          updatedAt: new Date().toISOString(),
        },
      },
      { upsert: true }
    );

    await this.notificationService.sendAutoTopupConfigured(tenantId, config);
  }

  async checkAndExecuteTopup(tenantId: string): Promise<void> {
    const config = await this.db.autoTopupConfigs.findOne({
      tenantId,
      enabled: true,
      status: 'active',
    });

    if (!config) return;

    const balance = await this.ledgerService.getBalance(tenantId);

    if (balance >= config.triggerBalance) return;

    // Check period limits
    const periodTopups = await this.db.autoTopupHistory.countDocuments({
      tenantId,
      createdAt: {
        $gte: new Date(Date.now() - 30 * 86400000).toISOString(),
      },
    });

    if (periodTopups >= config.maxTopupsPerPeriod) {
      await this.notificationService.sendAutoTopupLimitReached(tenantId);
      await this.db.autoTopupConfigs.updateOne(
        { tenantId },
        { $set: { status: 'paused', pauseReason: 'Max topups reached' } }
      );
      return;
    }

    await this.executeTopup(tenantId, config);
  }

  async executeTopup(tenantId: string): Promise<void> {
    const config = await this.db.autoTopupConfigs.findOne({ tenantId });
    const pack = CREDIT_PACK_TIERS.find(p => p.id === config.topupPackId);

    // Charge the payment method
    const paymentIntent = await stripe.paymentIntents.create({
      amount: pack.price,
      currency: pack.currency,
      customer: await this.getStripeCustomerId(tenantId),
      payment_method: config.paymentMethodId,
      off_session: true,
      confirm: true,
      metadata: {
        tenant_id: tenantId,
        purchase_type: 'auto_topup',
        auto_topup: 'true',
      },
      description: `Auto-topup: ${pack.name}`,
    });

    if (paymentIntent.status === 'succeeded') {
      // Issue credits
      await this.ledgerService.recordTransaction({
        tenantId,
        type: CreditTransactionType.PURCHASE,
        amount: pack.credits + (pack.bonusCredits || 0),
        currency: 'credits',
        description: `Auto-topup: ${pack.name}`,
        metadata: { source: 'auto_topup', autoTopup: 'true' },
        stripePaymentIntentId: paymentIntent.id,
        effectiveAt: new Date().toISOString(),
      });

      // Record topup history
      await this.db.autoTopupHistory.create({
        tenantId,
        amount: pack.credits,
        price: pack.price,
        timestamp: new Date().toISOString(),
      });

      // Notify
      if (config.notificationOnTopup) {
        await this.notificationService.sendAutoTopupExecuted(
          tenantId,
          pack.credits,
          pack.price
        );
      }
    }
  }
}
```

## Top-Up Amount Configuration

The top-up amount should be large enough to last a reasonable period but not so large that it creates credit liability. Recommended top-up amounts are based on the tenant's average daily consumption.

```typescript
interface TopupRecommendation {
  recommendedAmount: number;
  recommendedPackId: string;
  averageDailyConsumption: number;
  estimatedDaysOfCoverage: number;
  availablePacks: CreditPack[];
}
```

## Payment Method Charge

Auto-topup payments are processed off-session using a saved payment method. Stripe's off-session payment handling requires the payment method to be set up for future usage.

```typescript
async function setupAutoTopupPaymentMethod(
  tenantId: string,
  paymentMethodId: string
): Promise<void> {
  const customerId = await getStripeCustomerId(tenantId);

  // Set up for off-session usage
  const setupIntent = await stripe.setupIntents.create({
    customer: customerId,
    payment_method: paymentMethodId,
    usage: 'off_session',
  });

  await stripe.setupIntents.confirm(setupIntent.id);

  // Set as default for auto-topup
  await autoTopupService.configureAutoTopup(tenantId, {
    enabled: true,
    triggerBalance: 500,
    topupAmount: 5000,
    topupPackId: 'credits_5000',
    maxTopupsPerPeriod: 4,
    paymentMethodId,
    notificationOnTopup: true,
  });
}
```

## Top-Up Notification

When an auto-topup executes, the customer receives a notification with the receipt and updated balance.

```typescript
class AutoTopupNotificationService {
  async sendTopupExecuted(
    tenantId: string,
    creditsAdded: number,
    amount: number
  ): Promise<void> {
    const tenant = await this.tenantService.getTenant(tenantId);
    const newBalance = await this.ledgerService.getBalance(tenantId);

    await this.emailService.send({
      to: tenant.email,
      subject: 'Auto-topup completed',
      template: 'auto_topup',
      data: {
        creditsAdded: creditsAdded.toLocaleString(),
        amount: `$${(amount / 100).toFixed(2)}`,
        newBalance: newBalance.toLocaleString(),
        date: new Date().toLocaleDateString(),
        manageUrl: `${APP_URL}/billing/auto-topup`,
      },
    });
  }
}
```

## Open-Source Tools

- **Stripe API** — Off-session payment processing
- **BullMQ** (MIT) — Schedule periodic balance checks
- **Redis** — Cache balance for fast topup decisions
- **PostgreSQL** — Auto-topup configuration and history
- **Nodemailer** (MIT) — Top-up notification emails

## Integration Points

Auto-topup connects to the credit ledger (balance monitoring), the credit purchase system (credit issuance), the payment method service (charging), and the notification service (alerts).

## Production Considerations

- Monitor auto-topup success rate (should be > 99%)
- Set up alerts for auto-topup failures
- Handle insufficient funds for auto-topup gracefully
- Allow customers to pause auto-topup temporarily
- Test auto-topup flows thoroughly with test mode

## Open-Source First Philosophy

Stripe handles off-session payments for auto-topup. BullMQ manages balance check scheduling. PostgreSQL stores configuration and history. This open-source stack provides automated credit replenishment without proprietary subscription management features.
