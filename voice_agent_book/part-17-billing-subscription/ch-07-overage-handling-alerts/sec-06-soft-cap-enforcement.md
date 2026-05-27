# Section 06: Soft Cap Enforcement

## Soft Cap Notifications

Soft caps provide usage limits that, when exceeded, trigger notifications and upgrade prompts but don't block service. They're designed to encourage upgrades without disrupting business operations.

```typescript
interface SoftCapConfig {
  meter: string;
  allowance: number;           // Plan's included amount
  softCapMultiplier: number;   // e.g., 2x = 200% of allowance
  softCapThreshold: number;    // Calculated: allowance × softCapMultiplier
  action: SoftCapAction;
  escalationDelay: number;     // Hours before escalating to next action
}

enum SoftCapAction {
  NOTIFY = 'notify',                    // Send notification only
  UPGRADE_PROMPT = 'upgrade_prompt',   // Show upgrade prompt
  REQUEST_APPROVAL = 'request_approval', // Need admin approval
  BLOCK = 'block',                      // Block additional usage (hard cap)
}

class SoftCapService {
  async evaluateSoftCap(
    tenantId: string,
    meter: string,
    currentUsage: number,
    requestedQuantity: number
  ): Promise<SoftCapResult> {
    const plan = await this.planService.getTenantPlan(tenantId);
    const meterConfig = plan.meters.find(m => m.id === meter);

    if (!meterConfig || !meterConfig.softCap) {
      return { allowed: true };
    }

    const softCapThreshold = meterConfig.allowance * meterConfig.softCap.multiplier;
    const projectedUsage = currentUsage + requestedQuantity;

    if (projectedUsage <= softCapThreshold) {
      return { allowed: true };
    }

    // We're at or above the soft cap
    const escalation = await this.getEscalationLevel(tenantId, meter, projectedUsage);

    switch (escalation.action) {
      case SoftCapAction.NOTIFY:
        await this.sendSoftCapNotification(tenantId, meter, projectedUsage, softCapThreshold);
        return { allowed: true, warning: `Soft cap approaching: ${Math.round(projectedUsage / softCapThreshold * 100)}% used` };

      case SoftCapAction.UPGRADE_PROMPT:
        await this.sendSoftCapNotification(tenantId, meter, projectedUsage, softCapThreshold);
        return {
          allowed: true,
          warning: `You've exceeded ${softCapThreshold.toLocaleString()} ${meter}. Consider upgrading.`,
          upgradePrompt: {
            show: true,
            suggestedPlan: plan.upgradePlanId,
            savings: this.calculateUpgradeSavings(plan, meter, projectedUsage),
          },
        };

      case SoftCapAction.BLOCK:
        return {
          allowed: false,
          reason: `Soft cap of ${softCapThreshold.toLocaleString()} ${meter} reached. Please upgrade to continue.`,
          blockLevel: 'temporary',
          upgradeRequired: true,
        };

      default:
        return { allowed: true };
    }
  }

  private calculateUpgradeSavings(
    currentPlan: PlanDefinition,
    meter: string,
    projectedUsage: number
  ): UpgradeSavings {
    const upgradePlan = planCatalog.getPlan(currentPlan.upgradePlanId);
    const currentOverageCost = Math.max(0, projectedUsage - currentPlan.meters.find(m => m.id === meter).allowance) * 0.025;
    const upgradeCost = upgradePlan.price;

    return {
      currentOverageCost,
      upgradePrice: upgradeCost,
      monthlySavings: Math.max(0, currentOverageCost - upgradeCost),
      breakEvenDays: upgradeCost > 0 ? Math.ceil(currentOverageCost > 0 ? upgradeCost / (currentOverageCost / 30) : 30) : 0,
    };
  }
}
```

## Overage Allowance

The soft cap includes an overage allowance — usage beyond the plan allowance but within the cap is treated as "acceptable overage" with notifications but no service impact.

```
Soft Cap Zones:
┌──────────────────────────────────────────────────────────────────┐
│ Zone        │ Usage Range          │ Action                      │
├─────────────┼──────────────────────┼─────────────────────────────┤
│ Green       │ 0-80% of allowance  │ No action                   │
│ Yellow      │ 80-100% of allowance│ Info notification            │
│ Orange      │ 100-150% of allow.  │ Warning + upgrade prompt     │
│ Red         │ 150-200% of allow.  │ High urgency + auto-topup    │
│ Hard Cap    │ 200%+               │ Block additional usage       │
└──────────────────────────────────────────────────────────────────┘
```

## Cap Escalation

Escalation escalates the cap enforcement over time. If a customer remains above the soft cap for multiple periods, the enforcement becomes progressively stricter.

```typescript
interface EscalationState {
  tenantId: string;
  meter: string;
  consecutivePeriodsAboveCap: number;
  currentAction: SoftCapAction;
  escalatedAt: string;
}

async function escalateEnforcement(
  tenantId: string,
  meter: string
): Promise<void> {
  const state = await getEscalationState(tenantId, meter);

  // After 1 period: Notify
  // After 2 periods: Upgrade prompt
  // After 3 periods: Block

  switch (state.consecutivePeriodsAboveCap) {
    case 1:
      await updateEscalation(tenantId, meter, SoftCapAction.NOTIFY);
      break;
    case 2:
      await updateEscalation(tenantId, meter, SoftCapAction.UPGRADE_PROMPT);
      break;
    case 3:
      await updateEscalation(tenantId, meter, SoftCapAction.BLOCK);
      break;
  }

  await incrementEscalationPeriod(tenantId, meter);
}
```

## Hard Cap Configuration

Hard caps are absolute limits that block usage when reached. They prevent runaway costs for both the customer and the platform.

```typescript
interface HardCapConfig {
  enabled: boolean;
  hardCapMultiplier: number;   // e.g., 3x allowance
  hardCapThreshold: number;    // allowance × hardCapMultiplier
  action: 'block' | 'throttle' | 'downgrade_quality';
  blockDuration: 'period' | 'hour' | 'day';
  blockMessage: string;
}

function checkHardCap(
  meterConfig: MeterConfig,
  currentUsage: number,
  requestedQuantity: number
): { blocked: boolean; reason?: string } {
  if (!meterConfig.hardCap?.enabled) {
    return { blocked: false };
  }

  const hardCap = meterConfig.allowance * meterConfig.hardCap.hardCapMultiplier;
  const projected = currentUsage + requestedQuantity;

  if (projected > hardCap) {
    return {
      blocked: true,
      reason: `Hard cap of ${hardCap.toLocaleString()} ${meterConfig.name} reached. Service will resume next billing period.`,
    };
  }

  return { blocked: false };
}
```

## Open-Source Tools

- **Redis** — Real-time soft cap counters
- **PostgreSQL** — Escalation state tracking
- **BullMQ** — Schedule escalation evaluation
- **Unleash** (Apache 2.0) — Feature flag-based cap configuration

## Integration Points

Soft cap enforcement connects to the usage metering pipeline (real-time counters), the notification service (upgrade prompts), the plan catalog (cap configuration), and the billing dashboard.

## Production Considerations

- Allow enterprise customers to configure custom caps
- Monitor cap enforcement frequency and impact
- Test cap enforcement at boundary conditions
- Provide clear upgrade paths when caps are hit
- Escalate enforcement gradually to avoid customer frustration

## Open-Source First Philosophy

Redis powers real-time cap enforcement. PostgreSQL stores escalation states. BullMQ schedules periodic evaluations. Unleash manages cap configurations as feature flags. This all-open-source stack replaces proprietary usage management platforms while providing sophisticated cap enforcement capabilities.
