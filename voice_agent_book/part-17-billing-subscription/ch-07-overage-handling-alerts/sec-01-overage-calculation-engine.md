# Section 01: Overage Calculation Engine

## Usage vs Allowance Comparison

The overage calculation engine compares actual usage against plan allowances to determine overage amounts. It runs continuously for real-time visibility and at period boundaries for final billing.

```typescript
interface OverageCalculation {
  tenantId: string;
  periodKey: string;
  meters: OverageMeterCalculation[];
  totalOverageCost: number;
  currency: string;
  calculatedAt: string;
}

interface OverageMeterCalculation {
  meterId: string;
  meterName: string;
  planAllowance: number;
  actualUsage: number;
  overage: number;               // actualUsage - planAllowance
  overageRate: number;           // Price per unit of overage
  overageCost: number;           // overage × overageRate
  tieredOverage: OverageTier[];
  calculatedAt: string;
}

interface OverageTier {
  from: number;
  to: number | 'inf';
  rate: number;
  usageInTier: number;
  costInTier: number;
}

class OverageCalculator {
  async calculateOverage(
    tenantId: string,
    periodKey: string
  ): Promise<OverageCalculation> {
    const plan = await this.planService.getTenantPlan(tenantId);
    const usage = await this.usageService.getPeriodUsage(tenantId, periodKey);

    const calculations: OverageMeterCalculation[] = [];

    for (const meter of plan.meters) {
      const actualUsage = usage.find(u => u.meterId === meter.id)?.total || 0;
      const allowance = meter.included;
      const overage = Math.max(0, actualUsage - allowance);

      if (overage === 0) continue;

      // Calculate tiered overage pricing
      const tiers = meter.overageTiers || [
        { from: 0, to: 'inf', rate: meter.overageRate },
      ];

      let remainingOverage = overage;
      const tieredOverage: OverageTier[] = [];

      for (const tier of tiers) {
        if (remainingOverage <= 0) break;

        const tierLimit = tier.to === 'inf' ? remainingOverage : Math.min(tier.to, remainingOverage);
        const usageInTier = Math.min(tierLimit, remainingOverage);

        tieredOverage.push({
          from: tier.from,
          to: tier.to,
          rate: tier.rate,
          usageInTier,
          costInTier: usageInTier * tier.rate,
        });

        remainingOverage -= usageInTier;
      }

      const totalCost = tieredOverage.reduce((sum, t) => sum + t.costInTier, 0);

      calculations.push({
        meterId: meter.id,
        meterName: meter.name,
        planAllowance: allowance,
        actualUsage,
        overage,
        overageRate: meter.overageRate,
        overageCost: totalCost,
        tieredOverage,
        calculatedAt: new Date().toISOString(),
      });
    }

    const totalOverageCost = calculations.reduce((sum, m) => sum + m.overageCost, 0);

    return {
      tenantId,
      periodKey,
      meters: calculations,
      totalOverageCost,
      currency: 'usd',
      calculatedAt: new Date().toISOString(),
    };
  }

  async realtimeOverageCheck(
    tenantId: string,
    meter: string,
    currentUsage: number,
    additionalQuantity: number
  ): Promise<RealtimeOverageResult> {
    const plan = await this.planService.getTenantPlan(tenantId);
    const meterConfig = plan.meters.find(m => m.id === meter);

    if (!meterConfig) {
      return { allowed: true };
    }

    const projectedUsage = currentUsage + additionalQuantity;
    const overage = Math.max(0, projectedUsage - meterConfig.included);

    if (overage > 0 && !meterConfig.overageAllowed) {
      return {
        allowed: false,
        reason: 'Overage not allowed for this meter',
        currentUsage,
        projectedUsage,
        allowance: meterConfig.included,
        action: 'block',
      };
    }

    return {
      allowed: true,
      currentUsage,
      projectedUsage,
      allowance: meterConfig.included,
      overage,
      overageRate: meterConfig.overageRate,
      estimatedCost: overage * meterConfig.overageRate,
    };
  }
}
```

## Overage Rate Tables

Overage rates are defined per plan and per meter. They can be flat or tiered. Tiered rates provide volume discounts for heavy usage.

```
Overage Rate Table — Growth Plan:
┌──────────────────────────────────────────────────────────────────┐
│ Meter             │ Allowance │ Overage Rate  │ Tier Structure  │
├───────────────────┼───────────┼───────────────┼─────────────────┤
│ Monthly Minutes   │ 10,000    │ $0.025/min    │ Flat             │
│ AI Agents         │ 10        │ $5/agent/mo   │ Flat             │
│ Transcription     │ Included  │ $0.006/sec    │ Tiered:          │
│                   │           │               │ 0-50K: $0.006    │
│                   │           │               │ 50K-200K: $0.004│
│                   │           │               │ 200K+: $0.003   │
│ TTS Characters    │ 500K      │ $0.0001/char  │ Flat             │
│ API Requests      │ 100K/day  │ $0.001/req    │ Flat             │
└──────────────────────────────────────────────────────────────────┘
```

## Real-Time Calculation

The overage calculation engine runs in real-time alongside the usage metering pipeline. When usage exceeds allowance, the overage amount and cost are immediately available for display in the dashboard.

```typescript
class RealtimeOverageEngine {
  async getRealtimeOverage(tenantId: string): Promise<OverageSummary> {
    const plan = await this.planService.getTenantPlan(tenantId);
    const currentUsage = await this.usageService.getCurrentUsage(tenantId);
    const periodKey = this.getCurrentPeriodKey();

    const meters = [];

    for (const meterConfig of plan.meters) {
      const usage = currentUsage.find(u => u.meterId === meterConfig.id)?.total || 0;
      const allowance = meterConfig.included;
      const overage = Math.max(0, usage - allowance);

      meters.push({
        meterId: meterConfig.id,
        meterName: meterConfig.name,
        allowance,
        usage,
        usagePercent: allowance > 0 ? Math.min(100, (usage / allowance) * 100) : 0,
        overage,
        overageCost: overage * meterConfig.overageRate,
      });
    }

    return {
      tenantId,
      periodKey,
      meters,
      totalOverageCost: meters.reduce((s, m) => s + m.overageCost, 0),
      calculatedAt: new Date().toISOString(),
    };
  }

  private getCurrentPeriodKey(): string {
    const now = new Date();
    return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
  }
}
```

## Open-Source Tools

- **Redis** — Real-time usage counters for overage calculation
- **PostgreSQL** — Overage rate configuration and calculation history
- **BullMQ** — Schedule period-end overage calculation
- **Stripe API** — Submit overage as metered usage records

## Integration Points

The overage engine connects to the usage metering pipeline (actual usage), the plan catalog (allowances), the alert system (Section 3), the invoice system (Section 5), and the cap enforcement system (Section 6).

## Production Considerations

- Cache overage calculations for dashboard display
- Run period-end calculations in batch for accuracy
- Monitor overage calculation accuracy vs invoice amounts
- Test overage scenarios at boundary conditions (exactly at allowance)
- Handle multiple meters independently for composite overage

## Open-Source First Philosophy

The overage calculation engine runs on PostgreSQL and Redis — no proprietary billing engine required. Overage rates are configured in the plan catalog YAML files and synced to Stripe. This open-source approach provides sophisticated overage handling without the cost of enterprise billing platforms.
