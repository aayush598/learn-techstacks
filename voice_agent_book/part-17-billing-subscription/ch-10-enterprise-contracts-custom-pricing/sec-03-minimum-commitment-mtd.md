# Section 03: Minimum Commitment (MTD)

## Monthly Minimum Spend

Enterprise contracts often include a Minimum Traffic Direction (MTD) or monthly minimum spend requirement.

```
[Contract Activated]
    ↓
[Monthly Minimum Defined]
    ├── Amount: $10,000/month
    ├── Period: Monthly
    └── True-up: Quarterly
    ↓
[Monthly Billing Cycle]
    ├── Track actual usage
    ├── Calculate usage charges
    ├── Compare vs minimum
    └── Determine shortfall or overage
    ↓
[Period End (True-Up)]
    ├── If usage ≥ minimum → Bill actual usage
    ├── If usage < minimum → Bill shortfall
    └── Carry forward overage (if allowed)
```

```typescript
interface MinimumCommitment {
  id: string;
  contractId: string;
  tenantId: string;
  commitmentType: 'monthly_spend' | 'monthly_usage' | 'annual_spend';
  minimumAmount: number;
  minimumUnits?: number;
  unitType?: string;
  currency: string;
  billingPeriod: 'monthly' | 'quarterly' | 'annual';
  trueUpFrequency: 'monthly' | 'quarterly' | 'annual';
  carryForwardOverage: boolean;
  carryForwardMonths: number;
  overageRate: number;
  shortfallRate: number;
  effectiveDate: string;
  expirationDate?: string;
}

interface MonthlyUsageRecord {
  tenantId: string;
  contractId: string;
  period: { year: number; month: number };
  usageAmount: number;
  usageUnits: number;
  minimumAmount: number;
  shortfall: number;
  overage: number;
  carryForwardBalance: number;
  totalCharged: number;
  status: 'met' | 'shortfall' | 'overage';
}

class MinimumCommitmentTracker {
  async trackMonthlyUsage(
    tenantId: string,
    contractId: string,
    period: { year: number; month: number }
  ): Promise<MonthlyUsageRecord> {
    const commitment = await this.getActiveCommitment(contractId);
    if (!commitment) {
      throw new Error('No active minimum commitment found');
    }

    // Get actual usage for this period
    const actualUsage = await this.getUsageForPeriod(
      tenantId,
      period.year,
      period.month
    );

    // Get carry forward balance from previous months
    const carryForward = commitment.carryForwardOverage
      ? await this.getCarryForward(tenantId, period)
      : 0;

    const totalUsage = actualUsage + carryForward;
    const minimum = commitment.minimumAmount;
    const variance = totalUsage - minimum;

    let shortfall = 0;
    let overage = 0;
    let shortfallCharge = 0;
    let overageCharge = 0;

    if (variance < 0) {
      shortfall = Math.abs(variance);
      shortfallCharge = shortfall * commitment.shortfallRate;
    } else if (variance > 0) {
      overage = variance;
      overageCharge = overage * commitment.overageRate;
    }

    const record: MonthlyUsageRecord = {
      tenantId,
      contractId,
      period,
      usageAmount: actualUsage,
      usageUnits: actualUsage / (commitment.minimumUnits || 1),
      minimumAmount: minimum,
      shortfall,
      overage,
      carryForwardBalance: commitment.carryForwardOverage ? overage : 0,
      totalCharged: Math.max(actualUsage, minimum) + overageCharge,
      status: variance >= 0 ? 'met' : 'shortfall',
    };

    await this.storeUsageRecord(record);

    // Invoice if true-up is monthly
    if (commitment.trueUpFrequency === 'monthly') {
      await this.processTrueUp(record);
    }

    return record;
  }

  private async getCarryForward(
    tenantId: string,
    currentPeriod: { year: number; month: number }
  ): Promise<number> {
    const records = await this.getPreviousRecords(
      tenantId,
      currentPeriod,
      3 // Look back up to 3 months
    );

    return records
      .filter(r => r.status === 'overage')
      .reduce((sum, r) => sum + r.overage, 0);
  }
}
```

## True-Up at Period End

At the end of each true-up period, the system reconciles actual usage against commitments and invoices any shortfall or overage.

```typescript
interface TrueUpResult {
  contractId: string;
  period: { start: string; end: string };
  totalCommitted: number;
  totalUsed: number;
  totalInvoiced: number;
  shortfallAmount: number;
  overageAmount: number;
  trueUpAmount: number;
  invoiceId?: string;
  items: TrueUpLineItem[];
}

interface TrueUpLineItem {
  month: string;
  committed: number;
  used: number;
  shortfall: number;
  overage: number;
  carryForwardUsed: number;
  amountCharged: number;
}

class TrueUpProcessor {
  async processQuarterlyTrueUp(
    contractId: string,
    quarter: number,
    year: number
  ): Promise<TrueUpResult> {
    const commitment = await this.getActiveCommitment(contractId);
    const months = this.getQuarterMonths(quarter, year);

    const items: TrueUpLineItem[] = [];

    for (const month of months) {
      const record = await this.tracker.trackMonthlyUsage(
        commitment.tenantId,
        contractId,
        { year, month }
      );
      items.push({
        month: `${year}-${String(month).padStart(2, '0')}`,
        committed: record.minimumAmount,
        used: record.usageAmount,
        shortfall: record.shortfall,
        overage: record.overage,
        carryForwardUsed: 0,
        amountCharged: record.totalCharged,
      });
    }

    const totalCommitted = items.reduce((s, i) => s + i.committed, 0);
    const totalUsed = items.reduce((s, i) => s + i.used, 0);
    const totalInvoiced = items.reduce((s, i) => s + i.amountCharged, 0);

    // Net true-up: if total usage < total commitment, charge shortfall
    const shortfallAmount = Math.max(0, totalCommitted - totalUsed);
    const overageAmount = Math.max(0, totalUsed - totalCommitted);

    const result: TrueUpResult = {
      contractId,
      period: {
        start: `${year}-${String(months[0]).padStart(2, '0')}-01`,
        end: `${year}-${String(months[2]).padStart(2, '0')}-28`,
      },
      totalCommitted,
      totalUsed,
      totalInvoiced,
      shortfallAmount,
      overageAmount,
      trueUpAmount: shortfallAmount > 0 ? shortfallAmount * commitment.shortfallRate : 0,
      items,
    };

    // Generate true-up invoice
    if (result.trueUpAmount > 0) {
      const invoice = await this.generateTrueUpInvoice(result, commitment);
      result.invoiceId = invoice.id;
    }

    return result;
  }
}
```

## Shortfall Billing

When usage falls below commitment, the shortfall is billed at the end of the period.

```typescript
interface ShortfallBilling {
  contractId: string;
  tenantId: string;
  period: string;
  committedAmount: number;
  actualAmount: number;
  shortfallAmount: number;
  shortfallRate: number;
  shortfallCharge: number;
  invoiceId?: string;
  paymentStatus: 'pending' | 'paid' | 'overdue';
}

class ShortfallBillingService {
  async processShortfall(record: MonthlyUsageRecord): Promise<ShortfallBilling> {
    if (record.status !== 'shortfall') {
      throw new Error('No shortfall to process');
    }

    const commitment = await this.getActiveCommitment(record.contractId);
    const shortfallCharge = record.shortfall * commitment.shortfallRate;

    const billing: ShortfallBilling = {
      contractId: record.contractId,
      tenantId: record.tenantId,
      period: `${record.period.year}-${String(record.period.month).padStart(2, '0')}`,
      committedAmount: record.minimumAmount,
      actualAmount: record.usageAmount,
      shortfallAmount: record.shortfall,
      shortfallRate: commitment.shortfallRate,
      shortfallCharge,
      paymentStatus: 'pending',
    };

    // Create invoice for shortfall
    if (shortfallCharge > 0) {
      const invoice = await this.createShortfallInvoice(billing);
      billing.invoiceId = invoice.id;
    }

    return billing;
  }

  private async createShortfallInvoice(
    billing: ShortfallBilling
  ): Promise<Invoice> {
    // Create invoice with shortfall line item
    return this.invoiceService.createInvoice({
      tenantId: billing.tenantId,
      customerId: '',             // Resolved from contract
      items: [{
        description: `MTD Shortfall - ${billing.period}`,
        amount: billing.shortfallCharge,
        quantity: 1,
        type: 'shortfall',
      }],
      dueDate: this.addDays(new Date(), 30).toISOString(),
      metadata: {
        contract_id: billing.contractId,
        shortfall_period: billing.period,
      },
    });
  }
}
```

## Commitment Tracking Dashboard

```typescript
interface CommitmentDashboardData {
  contractId: string;
  currentPeriod: string;
  committedMonthly: number;
  actualMTD: number;
  projectedEOM: number;
  projectedShortfall: number;
  carryForwardBalance: number;
  historical: MonthlyUsageRecord[];
}

function CommitmentDashboard({ data }: { data: CommitmentDashboardData }) {
  const shortfallPercent = ((data.committedMonthly - data.projectedEOM) / data.committedMonthly) * 100;

  return (
    <div className="commitment-dashboard">
      <div className="commitment-summary">
        <div className="metric">
          <label>Monthly Commitment</label>
          <value>${data.committedMonthly.toLocaleString()}</value>
        </div>
        <div className="metric">
          <label>Usage MTD</label>
          <value>${data.actualMTD.toLocaleString()}</value>
        </div>
        <div className="metric">
          <label>Projected EOM</label>
          <value>${data.projectedEOM.toLocaleString()}</value>
        </div>
        <div className={`metric ${shortfallPercent > 0 ? 'warning' : 'success'}`}>
          <label>Projected Shortfall</label>
          <value>${Math.max(0, data.projectedShortfall).toLocaleString()}</value>
        </div>
      </div>
    </div>
  );
}
```

## Open-Source Tools

- **PostgreSQL** — Commitment tracking and usage records
- **BullMQ** — True-up scheduling and shortfall billing
- **Redis** — MTD usage aggregation counters
- **Stripe** — Shortfall invoice creation
- **Metabase** (Apache 2.0) — Commitment tracking dashboards
- **OpenTelemetry** — Commitment tracking events

## Integration Points

Minimum commitment tracking integrates with the usage metering system (actual usage), contract management (commitment terms), invoice generation (shortfall billing), and customer portal (commitment visibility).

## Production Considerations

- Project end-of-month usage early for proactive alerts
- Allow carry-forward of overage within contract terms
- Support mid-contract commitment renegotiation
- Track commitment attainment trends for forecasting
- Alert account managers when shortfall exceeds threshold
- Handle multi-currency commitments
- Support commitment-free grace periods for new contracts
- Provide self-service commitment dashboard for customers

## Open-Source First Philosophy

Redis aggregates MTD usage in real-time for instant commitment comparisons. PostgreSQL stores the definitive commitment tracking history. BullMQ schedules true-up processing and shortfall invoicing. Metabase provides customer-facing commitment dashboards. This open-source stack replaces vendor commitment tracking features while providing transparent, customizable commitment management.
