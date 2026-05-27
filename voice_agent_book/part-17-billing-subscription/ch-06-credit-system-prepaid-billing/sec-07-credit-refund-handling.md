# Section 07: Credit Refund Handling

## Refund Scenarios

Credit refunds occur in several scenarios: service issues, customer dissatisfaction, regulatory requirements, or business policy changes. Each scenario has specific handling requirements.

```typescript
interface CreditRefundRequest {
  id: string;
  tenantId: string;
  type: RefundType;
  amount: number;
  reason: string;
  supportingEvidence?: string[];
  status: RefundStatus;
  requiresApproval: boolean;
  approvedBy?: string;
  originalTransactionId?: string;
  createdAt: string;
  processedAt?: string;
}

enum RefundType {
  SERVICE_ISSUE = 'service_issue',
  CUSTOMER_REQUEST = 'customer_request',
  DUPLICATE_CHARGE = 'duplicate_charge',
  PROMO_ADJUSTMENT = 'promo_adjustment',
  REGULATORY = 'regulatory',
  GOODWILL = 'goodwill',
}

enum RefundStatus {
  PENDING = 'pending',
  APPROVED = 'approved',
  REJECTED = 'rejected',
  PROCESSED = 'processed',
}

class CreditRefundService {
  async requestRefund(
    tenantId: string,
    request: Omit<CreditRefundRequest, 'id' | 'status' | 'createdAt' | 'requiresApproval'>
  ): Promise<CreditRefundRequest> {
    // Check if refund requires approval
    const requiresApproval = request.amount > 10000; // > 10,000 credits

    const refundRequest: CreditRefundRequest = {
      id: `refund_${nanoid(16)}`,
      tenantId,
      ...request,
      status: requiresApproval ? 'pending' : 'approved',
      requiresApproval,
      createdAt: new Date().toISOString(),
    };

    await this.db.creditRefunds.create(refundRequest);

    if (requiresApproval) {
      await this.notificationService.sendRefundApprovalRequest(refundRequest);
    } else {
      await this.processRefund(refundRequest.id);
    }

    return refundRequest;
  }

  async approveRefund(refundId: string, approvedBy: string): Promise<void> {
    await this.db.creditRefunds.updateOne(
      { id: refundId },
      {
        $set: {
          status: 'approved',
          approvedBy,
        },
      }
    );

    await this.processRefund(refundId);
  }

  async processRefund(refundId: string): Promise<void> {
    const refund = await this.db.creditRefunds.findOne({ id: refundId });

    // Issue credit to ledger
    const entry = await this.ledgerService.recordTransaction({
      tenantId: refund.tenantId,
      type: CreditTransactionType.REFUND,
      amount: refund.amount, // Positive — adding credits back
      currency: 'credits',
      description: `Refund: ${refund.reason}`,
      metadata: {
        source: 'refund',
        reference: refund.id,
        refundType: refund.type,
        tags: ['refund', refund.type],
      },
      effectiveAt: new Date().toISOString(),
    });

    // If the original purchase was via Stripe, issue payment refund
    if (refund.originalTransactionId) {
      const purchase = await this.db.creditPurchases.findOne({
        id: refund.originalTransactionId,
      });

      if (purchase?.stripePaymentIntentId) {
        const monetaryAmount = Math.round(
          refund.amount * (purchase.price / purchase.amount)
        );

        await stripe.refunds.create({
          payment_intent: purchase.stripePaymentIntentId,
          amount: monetaryAmount,
          metadata: {
            refund_id: refund.id,
            tenant_id: refund.tenantId,
          },
        });
      }
    }

    // Update refund status
    await this.db.creditRefunds.updateOne(
      { id: refundId },
      {
        $set: {
          status: 'processed',
          processedAt: new Date().toISOString(),
        },
      }
    );

    // Notify tenant
    await this.notificationService.sendRefundProcessed(
      refund.tenantId,
      refund.id,
      refund.amount
    );
  }
}
```

## Unused Credit Refund

When customers cancel their account, unused prepaid credits may be refunded. The refund policy determines whether unused credits are refundable.

```typescript
interface UnusedCreditRefundPolicy {
  refundable: boolean;
  refundPercentage: number;    // Percentage of unused credits to refund
  processingFee: number;       // Flat processing fee (in cents)
  minRefundAmount: number;     // Minimum refund to process
  maxRefundAge: number;        // Max age of credits eligible for refund
}

async function calculateUnusedRefund(
  tenantId: string
): Promise<RefundCalculation> {
  const policy = await getRefundPolicy(tenantId);
  if (!policy.refundable) {
    return { refundable: false, reason: 'Credits are non-refundable' };
  }

  // Get remaining credit balance
  const balance = await getCreditBalance(tenantId);

  // Exclude promotional credits (not refundable)
  const promoBalance = await getPromoCreditBalance(tenantId);
  const refundableBalance = balance - promoBalance;

  if (refundableBalance <= 0) {
    return { refundable: false, reason: 'No refundable credits remaining' };
  }

  if (refundableBalance * getCreditValue() < policy.minRefundAmount) {
    return {
      refundable: false,
      reason: `Minimum refund amount is ${policy.minRefundAmount}`,
    };
  }

  const refundAmount = refundableBalance * policy.refundPercentage / 100;
  const fee = policy.processingFee;
  const netRefund = Math.max(0, refundAmount - fee);

  return {
    refundable: true,
    balance,
    refundableBalance,
    refundPercentage: policy.refundPercentage,
    grossRefund: refundAmount,
    processingFee: fee,
    netRefund,
  };
}

async function processUnusedRefund(tenantId: string): Promise<void> {
  const calculation = await calculateUnusedRefund(tenantId);
  if (!calculation.refundable) {
    throw new Error(calculation.reason);
  }

  // Refund credits via monetary refund
  await refundService.processRefund({
    tenantId,
    amount: calculation.refundableBalance,
    type: RefundType.CUSTOMER_REQUEST,
    reason: 'Account cancellation — unused credit refund',
    requiresApproval: true,
  });
}
```

## Partial Refund

Partial refunds apply when only a portion of a credit purchase is refunded. The system calculates the pro-rata amount based on consumed vs remaining credits.

```typescript
function calculatePartialRefund(
  purchaseAmount: number,
  purchasePrice: number,
  consumed: number
): number {
  // Calculate the monetary value of unconsumed credits
  const unconsumed = Math.max(0, purchaseAmount - consumed);
  const perCreditPrice = purchasePrice / purchaseAmount;
  return Math.round(unconsumed * perCreditPrice);
}

// Example: Customer bought 10,000 credits for $80
// Used 3,000 credits, requesting refund for remaining 7,000
// Refund = 7,000 × ($80 / 10,000) = $56
```

## Refund to Original Payment Method

Monetary refunds for credit purchases go back to the original payment method when possible. Stripe's refund API handles this seamlessly.

```typescript
async function refundToOriginalPayment(
  purchaseId: string,
  amount: number
): Promise<Stripe.Refund> {
  const purchase = await db.creditPurchases.findOne({ id: purchaseId });

  if (!purchase?.stripePaymentIntentId) {
    throw new Error('Cannot refund: no original payment found');
  }

  const refund = await stripe.refunds.create({
    payment_intent: purchase.stripePaymentIntentId,
    amount, // Amount in cents
    reason: 'requested_by_customer',
    metadata: {
      purchase_id: purchaseId,
      refund_type: 'credit_unused',
    },
  });

  // Log refund in ledger
  await ledgerService.recordTransaction({
    tenantId: purchase.tenantId,
    type: CreditTransactionType.REFUND,
    amount: -purchase.amount, // Remove the credits
    currency: 'credits',
    description: `Payment refund: $${(amount / 100).toFixed(2)}`,
    metadata: {
      source: 'payment_refund',
      reference: refund.id,
      tags: ['refund', 'payment'],
    },
    stripePaymentIntentId: purchase.stripePaymentIntentId,
    effectiveAt: new Date().toISOString(),
  });

  return refund;
}
```

## Open-Source Tools

- **Stripe API** — Payment refunds
- **PostgreSQL** — Refund request tracking
- **BullMQ** — Schedule refund processing
- **Nodemailer** (MIT) — Refund notifications

## Integration Points

Credit refunds connect to the credit ledger (balance adjustments), the Stripe payment system (monetary refunds), the notification service (customer communications), and the approval workflow (admin approvals).

## Production Considerations

- Implement approval workflows for refunds above threshold
- Log all refunds with complete audit trail
- Monitor refund-to-revenue ratio
- Handle refunds in compliance with local regulations
- Test refund scenarios thoroughly with Stripe test mode

## Open-Source First Philosophy

Stripe handles the payment refund infrastructure. PostgreSQL tracks all refund requests and processing history. BullMQ schedules refund workflows. This open-source approach avoids proprietary refund management platforms while maintaining complete refund auditability.
