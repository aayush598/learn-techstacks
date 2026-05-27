# Section 02: Contract Term Management

## Annual / Multi-Year Contracts

Enterprise contracts define specific term lengths, start/end dates, and renewal terms that differ from standard month-to-month subscriptions.

```
[Contract Created]
    ├── Term: 12/24/36 months
    ├── Start date: Negotiated
    ├── End date: Start + term
    └── Auto-renew: Configurable
    ↓
[During Term]
    ├── Price locked for term
    ├── Feature access guaranteed
    ├── SLA in effect
    └── Usage tracked against commitment
    ↓
[Term End (90 days before)]
    ├── Renewal notification sent
    ├── Negotiation begins
    ├── Price escalation applied
    └── Customer decision due
    ↓
[Term End]
    ├── If renewed: New term starts
    ├── If not renewed: Contract expires
    └── Data retention period begins
```

```typescript
interface Contract {
  id: string;
  tenantId: string;
  customerId: string;
  status: ContractStatus;
  term: ContractTerm;
  pricing: ContractPricing;
  autoRenew: boolean;
  renewalTerms?: RenewalTerms;
  terminationClause: TerminationClause;
  documents: ContractDocument[];
  approvalStatus: ApprovalStatus;
  signedAt?: string;
  createdAt: string;
  updatedAt: string;
}

type ContractStatus =
  | 'draft'
  | 'pending_approval'
  | 'pending_signature'
  | 'active'
  | 'expiring'
  | 'expired'
  | 'terminated'
  | 'renewed';

interface ContractTerm {
  startDate: string;
  endDate: string;
  durationMonths: number;
  type: 'monthly' | 'annual' | 'multi_year';
  years?: number;
  renewalNoticeDays: number;
  autoRenew: boolean;
  renewalTermMonths?: number;
}

interface TerminationClause {
  earlyTerminationFee: number;
  noticePeriodDays: number;
  allowedReasons: string[];
  forceMajeureIncluded: boolean;
  dataReturnProvision: string;
}

class ContractTermManager {
  async createContract(
    contractData: Omit<Contract, 'id' | 'createdAt' | 'updatedAt'>
  ): Promise<Contract> {
    // Validate term dates
    this.validateTerm(contractData.term);

    const contract: Contract = {
      ...contractData,
      id: generateId('contract'),
      status: 'draft',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    await this.storeContract(contract);

    // Schedule renewal notification
    if (contract.term.autoRenew) {
      await this.scheduleRenewalNotification(contract);
    }

    // Schedule term expiry
    await this.scheduleTermExpiry(contract);

    return contract;
  }

  async activateContract(contractId: string): Promise<Contract> {
    const contract = await this.getContract(contractId);
    if (contract.status !== 'pending_signature') {
      throw new Error('Contract must be signed before activation');
    }

    contract.status = 'active';
    contract.signedAt = new Date().toISOString();
    contract.updatedAt = new Date().toISOString();

    // Apply pricing to Stripe
    await this.applyContractPricing(contract);

    // Create subscription with contract terms
    await this.createSubscriptionsFromContract(contract);

    await this.updateContract(contract);

    return contract;
  }

  private async scheduleRenewalNotification(contract: Contract): Promise<void> {
    const noticeDate = new Date(contract.term.endDate);
    noticeDate.setDate(noticeDate.getDate() - contract.term.renewalNoticeDays);

    await this.renewalQueue.add(
      'renewal-notification',
      { contractId: contract.id },
      { delay: noticeDate.getTime() - Date.now() }
    );
  }

  private async scheduleTermExpiry(contract: Contract): Promise<void> {
    const expiryDate = new Date(contract.term.endDate);

    await this.termQueue.add(
      'term-expiry',
      { contractId: contract.id },
      { delay: expiryDate.getTime() - Date.now() }
    );
  }

  validateTerm(term: ContractTerm): void {
    const start = new Date(term.startDate);
    const end = new Date(term.endDate);

    if (end <= start) {
      throw new Error('End date must be after start date');
    }

    const durationMonths = (end.getFullYear() - start.getFullYear()) * 12
      + (end.getMonth() - start.getMonth());

    if (term.type === 'annual' && durationMonths < 12) {
      throw new Error('Annual contract must be at least 12 months');
    }
  }
}
```

## Contract Renewal and Auto-Renewal

```typescript
interface RenewalTerms {
  priceEscalation: PriceEscalation;
  renewalTerm: ContractTerm;
  renegotiationWindowDays: number;
  automaticIfNoResponse: boolean;
  renewalDiscount?: number;
}

interface PriceEscalation {
  type: 'fixed_percentage' | 'cpi_indexed' | 'negotiated';
  rate?: number;                 // Fixed percentage increase
  cap?: number;                  // Maximum increase
  indexSource?: string;          // CPI or other index
}

class ContractRenewalService {
  async processRenewal(contractId: string): Promise<RenewalResult> {
    const contract = await this.getContract(contractId);

    if (!contract.autoRenew) {
      return { renewed: false, reason: 'auto_renew_disabled' };
    }

    // Calculate new pricing with escalation
    const newPricing = this.calculateRenewalPricing(contract);

    // Create renewal contract
    const renewedContract = await this.createRenewalContract(contract, newPricing);

    // Update subscription pricing
    await this.updateSubscriptionPricing(contract.tenantId, newPricing);

    return {
      renewed: true,
      newContractId: renewedContract.id,
      newPricing,
      oldPricing: contract.pricing,
      effectiveDate: renewedContract.term.startDate,
    };
  }

  calculateRenewalPricing(contract: Contract): ContractPricing {
    const escalation = contract.renewalTerms?.priceEscalation;
    if (!escalation || escalation.type === 'negotiated') {
      return contract.pricing; // Price stays same until negotiated
    }

    const newPricing = { ...contract.pricing };

    if (escalation.type === 'fixed_percentage' && escalation.rate) {
      newPricing.monthlyPrice = Math.round(
        contract.pricing.monthlyPrice * (1 + escalation.rate / 100)
      );
      newPricing.annualPrice = newPricing.monthlyPrice * 12 * 0.9; // 10% annual discount
    }

    return newPricing;
  }

  private async createRenewalContract(
    oldContract: Contract,
    pricing: ContractPricing
  ): Promise<Contract> {
    const newTerm: ContractTerm = {
      ...oldContract.renewalTerms!.renewalTerm,
      startDate: oldContract.term.endDate,
      endDate: this.calculateEndDate(
        oldContract.term.endDate,
        oldContract.renewalTerms!.renewalTerm.durationMonths
      ),
    };

    return this.createContract({
      tenantId: oldContract.tenantId,
      customerId: oldContract.customerId,
      status: 'active',
      term: newTerm,
      pricing,
      autoRenew: oldContract.autoRenew,
      renewalTerms: oldContract.renewalTerms,
      terminationClause: oldContract.terminationClause,
      documents: [],
      approvalStatus: 'approved',
    });
  }
}
```

## Early Termination Fees

```typescript
interface EarlyTermination {
  contractId: string;
  requestedBy: string;
  reason: string;
  effectiveDate: string;
  fee: number;
  feeWaived: boolean;
  waiverReason?: string;
  dataRetentionPlan: string;
}

class EarlyTerminationService {
  calculateTerminationFee(contract: Contract): number {
    const clause = contract.terminationClause;
    if (clause.earlyTerminationFee > 0) {
      return clause.earlyTerminationFee;
    }

    // Calculate remaining value
    const endDate = new Date(contract.term.endDate);
    const now = new Date();
    const remainingMonths = (endDate.getFullYear() - now.getFullYear()) * 12
      + (endDate.getMonth() - now.getMonth());

    // Standard: 50% of remaining contract value
    return Math.round(contract.pricing.monthlyPrice * remainingMonths * 0.5);
  }

  async processTermination(
    contractId: string,
    reason: string,
    waivedBy?: string
  ): Promise<EarlyTermination> {
    const contract = await this.getContract(contractId);
    const fee = this.calculateTerminationFee(contract);
    const isWaived = !!waivedBy;

    const termination: EarlyTermination = {
      contractId,
      requestedBy: 'system',
      reason,
      effectiveDate: new Date().toISOString(),
      fee: isWaived ? 0 : fee,
      feeWaived: isWaived,
      waiverReason: isWaived ? 'Admin override' : undefined,
      dataRetentionPlan: '30_day_retention_then_delete',
    };

    // Apply termination fee if not waived
    if (!isWaived && fee > 0) {
      await this.invoiceTerminationFee(contract.tenantId, fee);
    }

    // Update contract status
    contract.status = 'terminated';
    contract.updatedAt = new Date().toISOString();
    await this.updateContract(contract);

    // Schedule data retention
    await this.scheduleDataRetention(contract.tenantId, termination);

    return termination;
  }
}
```

## Open-Source Tools

- **PostgreSQL** — Contract state and term management
- **BullMQ** — Renewal and expiry scheduling
- **Stripe** — Subscription management with contract terms
- **DocuSeal** (AGPL v3) — Contract signing and document management
- **Metabase** (Apache 2.0) — Contract lifecycle dashboards
- **OpenTelemetry** — Contract event tracing

## Integration Points

Contract term management integrates with the subscription system (term-based subscriptions), billing engine (pricing application), customer portal (contract visibility), CRM (renewal pipeline), and legal (contract documents).

## Production Considerations

- Send renewal notifications well before notice period (90 days recommended)
- Track contract milestone dates with automated alerts
- Maintain contract document versions with digital signatures
- Support contract amendments during active term
- Handle mid-term pricing adjustments with proration
- Automate early termination fee calculation and invoicing
- Provide contract status dashboard for account managers
- Implement contract data archival on termination

## Open-Source First Philosophy

PostgreSQL stores the complete contract data model with JSONB for flexible term configurations. BullMQ schedules all contract lifecycle events with precise timing. DocuSeal provides self-hosted contract signing. Metabase delivers contract lifecycle dashboards. This open-source stack replaces Salesforce CPQ and Apttus contract management while maintaining complete control over contract data and workflows.
