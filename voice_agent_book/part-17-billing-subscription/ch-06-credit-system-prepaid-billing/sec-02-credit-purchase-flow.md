# Section 02: Credit Purchase Flow

## Credit Pack Purchase

Users purchase credit packs through the billing interface. Each pack has a fixed price and credit amount. The purchase flow creates a Stripe PaymentIntent, collects payment, and issues credits upon confirmation.

```typescript
interface CreditPack {
  id: string;
  name: string;
  credits: number;          // Amount of credits
  price: number;            // Price in cents
  currency: string;
  bonusCredits?: number;    // Bonus credits for this pack
  popular?: boolean;        // Highlighted on UI
  description: string;
  validityDays?: number;    // Days until credit expiry
}

interface CreditPurchase {
  id: string;
  tenantId: string;
  creditPackId: string;
  amount: number;
  price: number;
  currency: string;
  status: 'pending' | 'completed' | 'failed';
  stripePaymentIntentId?: string;
  ledgerEntryId?: string;
  purchasedAt?: string;
}

const CREDIT_PACKS: CreditPack[] = [
  { id: 'credits_1000', name: '1,000 Credits', credits: 1000, price: 1000, currency: 'usd', popular: false, description: 'For light usage', validityDays: 365 },
  { id: 'credits_5000', name: '5,000 Credits', credits: 5000, price: 4500, currency: 'usd', bonusCredits: 500, popular: true, description: 'Best value for growing teams', validityDays: 365 },
  { id: 'credits_25000', name: '25,000 Credits', credits: 25000, price: 20000, currency: 'usd', bonusCredits: 5000, popular: false, description: 'For high-volume users', validityDays: 365 },
];

class CreditPurchaseService {
  async initiatePurchase(
    tenantId: string,
    creditPackId: string
  ): Promise<CreditPurchase> {
    const pack = CREDIT_PACKS.find(p => p.id === creditPackId);
    if (!pack) throw new Error('Invalid credit pack');

    const stripeCustomerId = await this.getStripeCustomerId(tenantId);

    // Create PaymentIntent
    const paymentIntent = await stripe.paymentIntents.create({
      amount: pack.price,
      currency: pack.currency,
      customer: stripeCustomerId,
      metadata: {
        tenant_id: tenantId,
        purchase_type: 'credit_pack',
        credit_pack_id: creditPackId,
      },
      description: `${pack.name} — ${pack.credits} credits`,
    });

    const purchase: CreditPurchase = {
      id: `cp_${nanoid(16)}`,
      tenantId,
      creditPackId,
      amount: pack.credits + (pack.bonusCredits || 0),
      price: pack.price,
      currency: pack.currency,
      status: 'pending',
      stripePaymentIntentId: paymentIntent.id,
    };

    await this.db.creditPurchases.create(purchase);

    return purchase;
  }

  async completePurchase(paymentIntentId: string): Promise<void> {
    const purchase = await this.db.creditPurchases.findOne({
      stripePaymentIntentId: paymentIntentId,
    });

    if (!purchase || purchase.status !== 'pending') return;

    const pack = CREDIT_PACKS.find(p => p.id === purchase.creditPackId);
    const totalCredits = purchase.amount;

    // Issue credits to ledger
    const expiryDate = pack?.validityDays
      ? new Date(Date.now() + pack.validityDays * 86400000).toISOString()
      : undefined;

    const entry = await this.ledgerService.recordTransaction({
      tenantId: purchase.tenantId,
      type: CreditTransactionType.PURCHASE,
      amount: totalCredits,
      currency: 'credits',
      description: `Purchased ${pack?.name}`,
      metadata: {
        source: 'credit_purchase',
        reference: purchase.id,
        tags: ['purchase'],
      },
      effectiveAt: new Date().toISOString(),
      expiresAt: expiryDate,
      stripePaymentIntentId: paymentIntentId,
    });

    // Update purchase record
    await this.db.creditPurchases.updateOne(
      { id: purchase.id },
      {
        $set: {
          status: 'completed',
          ledgerEntryId: entry.id,
          purchasedAt: new Date().toISOString(),
        },
      }
    );

    // Send receipt
    await this.notificationService.sendCreditPurchaseReceipt(
      purchase.tenantId,
      purchase.id,
      totalCredits,
      purchase.price
    );
  }
}
```

## Stripe Payment Intent

The PaymentIntent flow creates a secure payment session. The frontend confirms the payment using Stripe Elements, and the webhook handler processes the completion.

```typescript
// Frontend: Confirm payment
async function confirmCreditPurchase(
  purchaseId: string,
  stripe: Stripe,
  elements: StripeElements
): Promise<void> {
  const response = await fetch('/api/billing/credits/purchase', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ purchaseId }),
  });

  const { clientSecret } = await response.json();

  const { error } = await stripe.confirmCardPayment(clientSecret, {
    payment_method: {
      card: elements.getElement(CardNumberElement),
    },
  });

  if (error) {
    throw new Error(`Payment failed: ${error.message}`);
  }
}
```

## Immediate Credit Issuance

Credits are issued immediately upon payment confirmation, not after settlement. This provides instant gratification for the customer. If the payment later fails, the credits are reversed.

```typescript
async function handlePaymentSuccess(paymentIntent: Stripe.PaymentIntent): Promise<void> {
  if (paymentIntent.metadata.purchase_type === 'credit_pack') {
    // Issue credits immediately
    await creditPurchaseService.completePurchase(paymentIntent.id);

    // If auto-settlement is enabled, settle after 24 hours
    // Otherwise, the funds are available immediately
    await bullQueue.add('settleCreditPurchase', {
      paymentIntentId: paymentIntent.id,
    }, {
      delay: 24 * 60 * 60 * 1000, // 24 hours
    });
  }
}
```

## Receipt Generation

Purchase receipts are generated as credit note entries in the ledger and sent via email.

```typescript
async function generateCreditReceipt(purchase: CreditPurchase): Promise<void> {
  const receipt = {
    id: `receipt_${nanoid(16)}`,
    tenantId: purchase.tenantId,
    type: 'credit_purchase',
    amount: purchase.price,
    credits: purchase.amount,
    description: `Credit Pack Purchase — ${purchase.amount} credits`,
    date: new Date().toISOString(),
  };

  await this.db.receipts.create(receipt);

  await this.pdfService.generateReceiptPdf(receipt);
  await this.emailService.send({
    to: (await this.tenantService.getTenant(purchase.tenantId)).email,
    subject: 'Credit Purchase Receipt',
    template: 'credit_receipt',
    data: receipt,
  });
}
```

## Open-Source Tools

- **Stripe API** — Payment intent creation and confirmation
- **BullMQ** (MIT) — Schedule credit settlement jobs
- **PostgreSQL** — Purchase and receipt records
- **pdfmake** (MIT) — Receipt PDF generation
- **Nodemailer** (MIT) — Receipt email delivery

## Integration Points

Credit purchase connects to the Stripe payment service, the credit ledger (credit issuance), the notification service (receipts), and the accounting system (revenue recognition).

## Production Considerations

- Handle payment timeouts gracefully (release pending credits after 30 min)
- Implement idempotency for purchase completion
- Monitor purchase-to-issuance latency
- Test purchase cancellation and refund flows
- Display purchase history prominently in the billing UI

## Open-Source First Philosophy

The credit purchase flow uses Stripe for payment processing and BullMQ for post-purchase jobs. PostgreSQL stores all purchase records. pdfmake generates receipt PDFs. This open-source stack provides a complete prepaid credit purchasing experience without proprietary billing add-ons.
