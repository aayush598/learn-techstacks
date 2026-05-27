# Department Billing Allocation

## Overview

Department billing allocation tracks costs at the department and team level, enabling chargeback models, cost center tracking, and departmental budget management. This is essential for enterprise tenants with multiple departments sharing the platform.

## Billing Allocation Model

```typescript
interface BillingAllocation {
  id: string;
  tenantId: string;
  departmentId: string;
  period: {
    start: Date;
    end: Date;
  };
  costs: CostBreakdown;
  budget: BudgetInfo;
  chargeback: ChargebackInfo;
}

interface CostBreakdown {
  total: number;
  subscription: number;
  usage: {
    callMinutes: number;
    callCost: number;
    aiTokens: number;
    aiCost: number;
    storage: number;
    storageCost: number;
    phoneNumbers: number;
    phoneNumberCost: number;
  };
  overage: number;
  credits: number;
}

interface BudgetInfo {
  monthly: number;
  used: number;
  remaining: number;
  utilizationPercent: number;
  alertThreshold: number;      // Alert at this utilization %
  overageAllowed: boolean;
}

interface ChargebackInfo {
  costCenter: string;
  poNumber?: string;
  allocationMethod: 'direct' | 'proportional' | 'fixed';
  proportionalShare?: number;
}
```

## Cost Tracking Service

```typescript
class BillingAllocationService {
  async allocateCost(
    usageEvent: UsageEvent,
    userId: string
  ): Promise<void> {
    const user = await this.userService.getUser(userId);
    if (!user?.departmentId) return;

    const allocation = await this.getOrCreateAllocation(
      user.tenantId,
      user.departmentId,
      this.getCurrentPeriod()
    );

    // Add cost to department allocation
    allocation.costs.total += usageEvent.cost;
    allocation.costs.usage.callMinutes += usageEvent.callMinutes || 0;
    allocation.costs.usage.callCost += usageEvent.callCost || 0;
    allocation.costs.usage.aiTokens += usageEvent.aiTokens || 0;
    allocation.costs.usage.aiCost += usageEvent.aiCost || 0;

    await this.updateAllocation(allocation);

    // Check budget threshold
    if (allocation.budget.utilizationPercent >= allocation.budget.alertThreshold) {
      await this.alertBudgetThreshold(allocation);
    }
  }

  async getDepartmentUsage(
    departmentId: string,
    period: { start: Date; end: Date }
  ): Promise<BillingAllocation> {
    return this.db.findOne('billing_allocations', {
      departmentId,
      'period.start': period.start,
      'period.end': period.end,
    });
  }

  async getTeamBreakdown(departmentId: string, period: { start: Date; end: Date }): Promise<TeamCostBreakdown[]> {
    const teams = await this.teamService.getDepartmentTeams(departmentId);
    const breakdowns: TeamCostBreakdown[] = [];

    for (const team of teams) {
      const teamCost = await this.calculateTeamCost(team.id, period);
      breakdowns.push({
        teamId: team.id,
        teamName: team.name,
        ...teamCost,
      });
    }

    return breakdowns;
  }

  private async calculateTeamCost(
    teamId: string,
    period: { start: Date; end: Date }
  ): Promise<{ totalCost: number; usage: CostBreakdown['usage'] }> {
    const teamMembers = await this.teamService.getTeamMemberIds(teamId);
    const costs = { totalCost: 0, usage: { callMinutes: 0, callCost: 0, aiTokens: 0, aiCost: 0, storage: 0, storageCost: 0, phoneNumbers: 0, phoneNumberCost: 0 } };

    for (const userId of teamMembers) {
      const usage = await this.usageService.getUserUsage(userId, period);
      costs.totalCost += usage.totalCost;
      costs.usage.callMinutes += usage.callMinutes;
      costs.usage.callCost += usage.callCost;
      costs.usage.aiTokens += usage.aiTokens;
      costs.usage.aiCost += usage.aiCost;
    }

    return costs;
  }

  private async alertBudgetThreshold(allocation: BillingAllocation): Promise<void> {
    const department = await this.departmentService.getDepartment(allocation.departmentId);
    if (!department?.headUserId) return;

    await this.notificationService.notify({
      type: 'budget_threshold_reached',
      recipients: [department.headUserId],
      data: {
        departmentId: allocation.departmentId,
        utilization: allocation.budget.utilizationPercent,
        used: allocation.budget.used,
        budget: allocation.budget.monthly,
      },
    });
  }
}
```

## Chargeback Report

```
Department: Engineering
Month: June 2025
┌────────────────────────────────────────────┐
│ Budget: $50,000                             │
│ Used: $32,450 (64.9%)                       │
│ Remaining: $17,550                          │
│ Alert threshold: 80%                        │
├────────────────────────────────────────────┤
│ Cost Breakdown                              │
├────────────────┬───────────┬────────────────┤
│ Category       │ Amount    │ % of Total     │
├────────────────┼───────────┼────────────────┤
│ Call Minutes   │ $18,200   │ 56.1%          │
│ AI Tokens      │ $9,750    │ 30.0%          │
│ Phone Numbers  │ $2,500    │ 7.7%           │
│ Storage        │ $1,200    │ 3.7%           │
│ Overage        │ $800      │ 2.5%           │
├────────────────┼───────────┼────────────────┤
│ Total          │ $32,450   │ 100%           │
├────────────────┴───────────┴────────────────┤
│ Per-Team Breakdown                           │
│ Backend: $12,300 (37.9%)                     │
│ Frontend: $8,900 (27.4%)                     │
│ Infrastructure: $7,250 (22.3%)               │
│ QA: $4,000 (12.3%)                           │
└────────────────────────────────────────────┘
```

## Open-Source Tools

- **Stripe** (Commercial) — Usage-based billing and chargeback
- **Lago** (MIT) — Open-source usage-based billing
- **Metronome** (Commercial) — Usage metering and billing

## Production Considerations

- Allocate costs daily via batch job (avoid real-time cost calculation overhead)
- Support multiple allocation methods: direct (per-user costs), proportional (by headcount), fixed (per-department)
- Allow cost center code input per department for enterprise accounting integration
- Export billing allocation data in accounting software format (CSV, Xero, QuickBooks)
- Provide budget rollover option (unused budget carries to next month)
- Alert department heads before billing cycle close to prevent surprises
- Support pre-paid budgets (annual commitment vs monthly allocation)
