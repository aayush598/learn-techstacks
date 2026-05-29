# Section 07: Add-On & Upsell Strategy

## Expansion Revenue Framework

Expansion revenue (upsells, cross-sells, add-ons) drives net revenue retention above 120%. Every customer relationship should have a defined expansion path.

```
Expansion Revenue Flywheel
                    ┌──────────────────────┐
                    │  Base Subscription   │
                    │  (Entry Point)       │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │  Usage Growth        │
                    │  (Natural expansion) │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
     ┌────────▼──────┐ ┌──────▼───────┐ ┌──────▼───────┐
     │ Tier Upgrade  │ │ Add-On       │ │ Marketplace  │
     │ (Higher plan) │ │ Purchases    │ │ Purchases    │
     └───────────────┘ └──────────────┘ └──────────────┘
```

## Add-On Catalog

| Add-On | Price | Target Tier | Target Segment | Gross Margin |
|--------|-------|-------------|----------------|--------------|
| Extra voice minutes | $0.03-0.08/min | All | All | 70% |
| Extra agents | $19/mo per agent | Starter, Pro | SMB | 95% |
| Extra team seats | $15/mo per seat | All | All | 95% |
| Premium voices | $9/mo per voice | Pro+ | All | 85% |
| Advanced analytics | $49/mo | Pro+ | Mid-market | 90% |
| Custom LLM gateway | $99/mo | Pro+ | Developer, Enterprise | 80% |
| SMS capability | $29/mo | Starter+ | All | 60% |
| HIPAA compliance | $999/mo | Business+ | Healthcare | 90% |
| White-label (basic) | $499/mo | Business+ | Agency | 85% |
| White-label (pro) | $1,499/mo | Enterprise | Agency | 85% |
| Self-hosted | $1,999/mo | Enterprise | Enterprise | 95% |
| Dedicated support | $999/mo | Business+ | Enterprise | 90% |
| Custom integrations | $99/mo each | Pro+ | Mid-market | 80% |
| Extended data retention | $0.10/GB/mo | All | Compliance | 90% |

## Tier Upgrade Paths

```
┌────────────────────────────────────────────────────────────────────┐
│ Upgrade Triggers & Timing                                         │
├────────────────────────────────────────────────────────────────────┤
│ Current Tier │ Trigger                    │ Suggested Upgrade     │
├────────────────────────────────────────────────────────────────────┤
│ Free         │ Hit 80 min in first week   │ Starter ($49)         │
│ Free         │ Tried to add 2nd agent     │ Starter ($49)         │
│ Starter      │ Used >800 min for 2 months │ Pro ($199)            │
│ Starter      │ Tried to add 3rd agent     │ Pro ($199)            │
│ Pro          │ Used >8K min for 2 months  │ Business ($499)       │
│ Pro          │ Needs team collaboration   │ Business ($499)       │
│ Pro          │ Needs custom LLM           │ Pro + add-on OR       │
│              │                            │ Business (included)   │
│ Business     │ Used >80K min              │ Enterprise (custom)   │
│ Business     │ Asked about HIPAA          │ Enterprise + HIPAA    │
│ Business     │ Asked about SSO            │ Enterprise            │
└────────────────────────────────────────────────────────────────────┘
```

## Upsell Data Model

```typescript
interface AddOn {
  id: string;
  name: string;
  description: string;
  price: number;
  unit: 'monthly' | 'per_user' | 'per_agent' | 'usage' | 'one_time';
  targetTiers: string[];
  requirements: string[]; // features required for this add-on to work
  
  // Upsell automation
  triggers: UpsellTrigger[];
  recommendedOrder: number; // which add-on to suggest first
}

interface UpsellTrigger {
  event: string;
  condition: string;
  delay: number; // seconds after event
  channel: 'in_app' | 'email' | 'push' | 'support';
  message: string;
}

const upsellTriggers: UpsellTrigger[] = [
  {
    event: 'usage_threshold',
    condition: 'monthly_minutes > 800',
    delay: 0,
    channel: 'in_app',
    message: 'You\'re approaching your Starter plan limit. Upgrade to Pro for more minutes and features.',
  },
  {
    event: 'agent_count',
    condition: 'agents_created >= 2',
    delay: 3600, // 1 hour
    channel: 'in_app',
    message: 'Need more agents? Upgrade to Pro for up to 5 agents.',
  },
  {
    event: 'team_invite_sent',
    condition: 'user.invites >= 2',
    delay: 86400, // 24 hours
    channel: 'email',
    message: 'Your team is growing! Business plan gives you 10 seats with collaboration features.',
  },
];
```

## Expansion Metrics & Targets

```typescript
interface ExpansionMetrics {
  netRevenueRetention: number; // Target: >120%
  grossRevenueRetention: number; // Target: >95%
  expansionMRR: number;
  expansionRate: number; // % of existing customer revenue expanding
  
  upsell: {
    tierUpgradeRate: number; // Target: 8% quarterly
    addOnAdoptionRate: number; // Target: 25% of eligible
    averageUpsellValue: number; // Target: $85/mo
    timeToFirstUpgrade: number; // Target: 90 days
  };
  
  crossSell: {
    marketplaceAdoptionRate: number; // Target: 15%
    pluginInstallRate: number; // Target: 20%
    voicePackPurchaseRate: number; // Target: 10%
  };
}

function calculateExpansionPotential(customer: Customer): ExpansionOpportunity {
  const tier = customer.tier;
  const currentUsage = customer.currentUsage;
  const limits = tier.limits;
  
  const naturalUpgrade = !tier.isEnterprise && (
    currentUsage.monthlyMinutes > limits.voiceMinutes * 0.8 ||
    currentUsage.agents > limits.agents * 0.8
  );
  
  return {
    suggestedUpgrade: naturalUpgrade ? getNextTier(tier.id) : null,
    suggestedAddOns: suggestAddOns(customer),
    expectedRevenueIncrease: calculateExpectedIncrease(customer),
    priority: naturalUpgrade ? 'high' : 'medium',
    timeline: naturalUpgrade ? 'immediate' : 'next_quarter',
  };
}
```

## In-App Upsell Patterns

**Pattern 1: "You've hit your limit" modal.** When user tries to exceed limit (e.g., create 3rd agent on Starter), show upgrade prompt. Not nagging — contextual and helpful.

**Pattern 2: Usage bar with upgrade CTA.** Dashboard shows usage meter (e.g., 847/1000 minutes). "Need more? Upgrade to Pro for 10K minutes."

**Pattern 3: Feature discovery card.** "Pro tip: Upgrade to unlock custom voices." Shown when user explores voice settings but feature is locked.

**Pattern 4: End-of-month summary.** Email: "You used 1,240 minutes this month. Save 30% by upgrading to Pro."

## Email Sequence for Expansion

| Day | Event | Email Content |
|-----|-------|--------------|
| 1 | After signup | Welcome, personalization survey |
| 14 | Usage check | "You've used X% of your minutes" |
| 30 | First billing | "See what you could get with Pro" |
| 45 | Feature exploration | "Did you know? Pro has custom LLM" |
| 60 | Usage milestone | "Congratulations on X calls! Here's your next step." |
| 90 | Value review | "You've saved $X with our platform. Upgrade to save more." |

## Competitive Add-On Comparison

| Add-On | Us | Retell AI | Vapi | Bland AI |
|--------|-----|-----------|------|----------|
| Extra agents | $19/agent | None | None | None |
| Premium voices | $9/mo | Included | $0.01/min extra | Included |
| Analytics | $49/mo | Included | $49/mo | $29/mo |
| Custom LLM | $99/mo | None | None | None |
| HIPAA add-on | $999/mo | $2K/mo | None | None |
| White-label | $499-1,499/mo | Custom quote | None | None |

## Tools & Resources

- **Upsell automation:** PostHog (product analytics + feature flags), Customer.io (email)
- **Usage tracking:** PostHog, Amplitude
- **In-app messaging:** Appcues, Userflow, Chameleon
- **Pricing page:** Custom with A/B testing (GrowthBook)
- **Revenue optimization:** ChartMogul, ProfitWell
- **CPQ (enterprise):** Salesforce CPQ, PandaDoc
