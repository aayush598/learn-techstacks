# Section 06: Contract Renewal Automation

## Renewal Notification

The renewal automation system sends timely notifications to account managers and customers as contract end approaches.

```
[Contract Active]
    ↓
[T-90 Days: Renewal Notice]
    ├── Notify account manager
    ├── Generate renewal report
    └── Flag in CRM
    ↓
[T-60 Days: Customer Notification]
    ├── Send renewal proposal
    ├── Include price escalation details
    └── Request renewal decision
    ↓
[T-30 Days: Follow-Up]
    ├── Reminder to customer
    ├── Escalate if no response
    └── Prepare discount offers
    ↓
[T-0: Contract End]
    ├── If auto-renew → New term starts
    ├── If manual → Final notice
    └── If no response → Grace period
```

```typescript
interface RenewalNotification {
  contractId: string;
  tenantId: string;
  customerId: string;
  type: 'internal' | 'customer';
  recipientRole?: string;        // For internal notifications
  channel: 'email' | 'in_app' | 'slack' | 'crm';
  template: string;
  daysBeforeEnd: number;
  sentAt?: string;
  status: 'pending' | 'sent' | 'failed' | 'read';
}

class RenewalNotificationService {
  private readonly notificationSchedule: RenewalNotification[];

  constructor() {
    this.notificationSchedule = [
      { contractId: '', tenantId: '', customerId: '', type: 'internal', recipientRole: 'account_manager', channel: 'email', template: 'renewal_internal_90d', daysBeforeEnd: 90, status: 'pending' },
      { contractId: '', tenantId: '', customerId: '', type: 'customer', channel: 'email', template: 'renewal_customer_60d', daysBeforeEnd: 60, status: 'pending' },
      { contractId: '', tenantId: '', customerId: '', type: 'internal', recipientRole: 'account_manager', channel: 'slack', template: 'renewal_internal_30d', daysBeforeEnd: 30, status: 'pending' },
      { contractId: '', tenantId: '', customerId: '', type: 'customer', channel: 'email', template: 'renewal_customer_14d', daysBeforeEnd: 14, status: 'pending' },
      { contractId: '', tenantId: '', customerId: '', type: 'customer', channel: 'email', template: 'renewal_customer_7d', daysBeforeEnd: 7, status: 'pending' },
      { contractId: '', tenantId: '', customerId: '', type: 'internal', recipientRole: 'director', channel: 'email', template: 'renewal_internal_expired', daysBeforeEnd: 0, status: 'pending' },
    ];
  }

  async scheduleRenewalNotifications(contract: Contract): Promise<void> {
    for (const notification of this.notificationSchedule) {
      const sendDate = new Date(contract.term.endDate);
      sendDate.setDate(sendDate.getDate() - notification.daysBeforeEnd);

      // Schedule the notification
      await this.renewalQueue.add(
        'renewal-notification',
        {
          contractId: contract.id,
          tenantId: contract.tenantId,
          customerId: contract.customerId,
          template: notification.template,
          channel: notification.channel,
          type: notification.type,
          recipientRole: notification.recipientRole,
        },
        { delay: sendDate.getTime() - Date.now() }
      );
    }
  }

  async sendRenewalNotification(
    contract: Contract,
    notification: RenewalNotification
  ): Promise<void> {
    const daysUntilEnd = this.calculateDaysUntilEnd(contract.term.endDate);

    if (notification.type === 'internal') {
      await this.sendInternalNotification(contract, notification, daysUntilEnd);
    } else {
      await this.sendCustomerNotification(contract, notification, daysUntilEnd);
    }
  }

  private async sendCustomerNotification(
    contract: Contract,
    notification: RenewalNotification,
    daysUntilEnd: number
  ): Promise<void> {
    const template = await this.getTemplate(notification.template);
    const escalation = contract.renewalTerms?.priceEscalation;
    const newPrice = escalation?.rate
      ? contract.pricing.monthlyPrice * (1 + escalation.rate / 100)
      : contract.pricing.monthlyPrice;

    await this.notificationService.send({
      customerId: contract.customerId,
      channel: notification.channel,
      template: notification.template,
      context: {
        customerName: contract.customerName,
        contractNumber: contract.contractNumber,
        currentPrice: contract.pricing.monthlyPrice,
        newPrice: Math.round(newPrice),
        escalationRate: escalation?.rate,
        renewalDate: contract.term.endDate,
        daysUntilEnd,
        autoRenew: contract.autoRenew,
        actionUrl: `${APP_URL}/contracts/${contract.id}/renew`,
      },
    });
  }

  private calculateDaysUntilEnd(endDate: string): number {
    const end = new Date(endDate);
    const now = new Date();
    return Math.ceil((end.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
  }
}
```

## Price Escalation Calculation

```typescript
interface PriceEscalationResult {
  originalPrice: number;
  escalatedPrice: number;
  increaseAmount: number;
  increasePercent: number;
  escalationType: string;
  indexUsed?: string;
  indexValue?: number;
}

class PriceEscalationCalculator {
  async calculateEscalation(
    contract: Contract
  ): Promise<PriceEscalationResult> {
    const escalation = contract.renewalTerms?.priceEscalation;
    if (!escalation) {
      return {
        originalPrice: contract.pricing.monthlyPrice,
        escalatedPrice: contract.pricing.monthlyPrice,
        increaseAmount: 0,
        increasePercent: 0,
        escalationType: 'none',
      };
    }

    switch (escalation.type) {
      case 'fixed_percentage':
        return this.calculateFixedPercentage(
          contract.pricing.monthlyPrice,
          escalation.rate!,
          escalation.cap
        );

      case 'cpi_indexed': {
        const cpiData = await this.getCPIData(
          escalation.indexSource || 'CPI-U',
          contract.term.startDate,
          contract.term.endDate
        );
        return this.calculateCPIBased(
          contract.pricing.monthlyPrice,
          cpiData,
          escalation.cap
        );
      }

      case 'negotiated':
        return {
          originalPrice: contract.pricing.monthlyPrice,
          escalatedPrice: contract.pricing.monthlyPrice,
          increaseAmount: 0,
          increasePercent: 0,
          escalationType: 'negotiated',
        };

      default:
        return {
          originalPrice: contract.pricing.monthlyPrice,
          escalatedPrice: contract.pricing.monthlyPrice,
          increaseAmount: 0,
          increasePercent: 0,
          escalationType: 'none',
        };
    }
  }

  private calculateFixedPercentage(
    currentPrice: number,
    rate: number,
    cap?: number
  ): PriceEscalationResult {
    let increasePercent = rate;
    if (cap && rate > cap) {
      increasePercent = cap;
    }

    const increaseAmount = currentPrice * (increasePercent / 100);
    const escalatedPrice = currentPrice + increaseAmount;

    return {
      originalPrice: currentPrice,
      escalatedPrice: Math.round(escalatedPrice),
      increaseAmount: Math.round(increaseAmount),
      increasePercent,
      escalationType: 'fixed_percentage',
    };
  }

  private async calculateCPIBased(
    currentPrice: number,
    cpiData: CPIData,
    cap?: number
  ): Promise<PriceEscalationResult> {
    const cpiChangePercent = ((cpiData.currentCPI - cpiData.baseCPI) / cpiData.baseCPI) * 100;

    let increasePercent = cpiChangePercent;
    if (cap && cpiChangePercent > cap) {
      increasePercent = cap;
    }

    const increaseAmount = currentPrice * (increasePercent / 100);
    const escalatedPrice = currentPrice + increaseAmount;

    return {
      originalPrice: currentPrice,
      escalatedPrice: Math.round(escalatedPrice),
      increaseAmount: Math.round(increaseAmount),
      increasePercent,
      escalationType: 'cpi_indexed',
      indexUsed: cpiData.indexName,
      indexValue: cpiChangePercent,
    };
  }
}
```

## Renewal Negotiation Tracking

```typescript
interface RenewalNegotiation {
  contractId: string;
  tenantId: string;
  status: 'not_started' | 'in_progress' | 'agreed' | 'lost' | 'escalated';
  accountManagerId: string;
  customerContact: string;
  proposedTerms: {
    price: number;
    termMonths: number;
    discounts: DiscountApplication[];
    features: string[];
  };
  counterTerms?: {
    price: number;
    termMonths: number;
    discounts: DiscountApplication[];
    features: string[];
  };
  negotiationHistory: NegotiationEvent[];
  deadline: string;
  probability: number;           // 0-100
}

interface NegotiationEvent {
  date: string;
  type: 'proposal' | 'counter' | 'meeting' | 'email' | 'note';
  from: string;
  content: string;
  attachments?: string[];
}

class RenewalNegotiationTracker {
  async startNegotiation(
    contract: Contract
  ): Promise<RenewalNegotiation> {
    const escalation = await this.escalationCalculator.calculateEscalation(contract);

    const negotiation: RenewalNegotiation = {
      contractId: contract.id,
      tenantId: contract.tenantId,
      status: 'not_started',
      accountManagerId: contract.accountManagerId,
      customerContact: contract.customerContact,
      proposedTerms: {
        price: escalation.escalatedPrice,
        termMonths: contract.term.durationMonths,
        discounts: [],
        features: contract.features,
      },
      negotiationHistory: [],
      deadline: this.calculateNegotiationDeadline(contract),
      probability: 80,
    };

    await this.storeNegotiation(negotiation);
    return negotiation;
  }

  async updateProbability(
    negotiationId: string,
    newProbability: number
  ): Promise<void> {
    await this.updateNegotiation(negotiationId, {
      probability: newProbability,
      status: newProbability > 50 ? 'in_progress' : 'escalated',
    });

    // Alert if probability drops significantly
    if (newProbability < 30) {
      await this.escalateNegotiation(negotiationId, 'low_probability');
    }
  }
}
```

## Automated Renewal Execution

```typescript
class RenewalExecutor {
  async processAutoRenewal(contractId: string): Promise<RenewalResult> {
    const contract = await this.getContract(contractId);

    if (!contract.autoRenew) {
      return { renewed: false, reason: 'auto_renew_disabled' };
    }

    // Calculate new pricing
    const escalationResult = await this.escalationCalculator.calculateEscalation(contract);

    // Create new term dates
    const newStart = contract.term.endDate;
    const newEnd = this.calculateEndDate(newStart, contract.term.durationMonths);

    // Update subscription pricing
    await this.updateSubscriptionPricing(
      contract.tenantId,
      escalationResult.escalatedPrice
    );

    // Extend subscription term
    await this.extendSubscriptionTerm(contract.tenantId, newEnd);

    // Update contract with new term
    contract.term.startDate = newStart;
    contract.term.endDate = newEnd;
    contract.pricing.monthlyPrice = escalationResult.escalatedPrice;
    contract.status = 'renewed';
    contract.updatedAt = new Date().toISOString();

    await this.updateContract(contract);

    // Notify customer
    await this.sendRenewalConfirmation(contract, escalationResult);

    // Schedule next renewal notifications
    await this.notificationService.scheduleRenewalNotifications(contract);

    return {
      renewed: true,
      newContractId: contract.id,
      oldPrice: escalationResult.originalPrice,
      newPrice: escalationResult.escalatedPrice,
      newTermEnd: newEnd,
    };
  }
}
```

## Open-Source Tools

- **BullMQ** — Renewal notification and execution scheduling
- **PostgreSQL** — Renewal negotiation and contract state
- **Redis** — Renewal pipeline cache
- **Metabase** (Apache 2.0) — Renewal pipeline dashboards
- **Handlebars** (MIT) — Renewal email templates
- **Slack SDK** (MIT) — Internal renewal notifications via Slack
- **OpenTelemetry** — Renewal process tracing

## Integration Points

Renewal automation integrates with the contract management system (term tracking), pricing engine (escalation calculation), subscription system (term extension), CRM (renewal pipeline), and notification service (renewal communications).

## Production Considerations

- Track renewal win/loss rates by account manager
- Alert on accounts with high churn risk during renewal
- Provide renewal dashboard with pipeline view
- Support mid-term amendments that affect renewal terms
- Handle multi-year contracts with staggered renewals
- Implement renewal probability scoring
- Track renewal cycle time for process improvement
- Support usage-based renewal with commitment renegotiation

## Open-Source First Philosophy

BullMQ orchestrates the entire renewal lifecycle with scheduled notifications and automated execution. PostgreSQL stores the complete renewal negotiation history. Metabase provides the renewal pipeline dashboard for sales leadership. This open-source stack replaces proprietary renewal management platforms while providing complete control over renewal strategies and customer retention.
