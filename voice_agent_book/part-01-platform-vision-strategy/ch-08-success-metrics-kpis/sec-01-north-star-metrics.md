# Section 01: North Star Metrics

## North Star Definition

Our North Star metric is **Active Agent Minutes Processed** — the total number of minutes where an AI voice agent is actively engaged in a conversation with a customer. This metric directly correlates with revenue (usage-based pricing) and customer value (minutes = calls handled = cost savings).

```
North Star Metric Framework
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│          Active Agent Minutes Processed (North Star)                   │
│                        ▲                                                │
│                        │                                                │
│   ┌────────────────────┼────────────────────┐                          │
│   │                    │                    │                          │
│   ▼                    ▼                    ▼                          │
│ Agent Deployments   Call Success Rate   Avg Call Duration              │
│ (Adoption)         (Quality)            (Engagement)                   │
│   │                    │                    │                          │
│   ▼                    ▼                    ▼                          │
│ Onboarding           Pipeline           Response                       │
│ Completion           Reliability        Quality                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Why Active Agent Minutes?

**Revenue correlate:** With per-minute pricing, every active minute generates revenue. Tracking this metric gives forward-looking revenue visibility.

**Value signal:** Minutes = calls handled = customer value. More minutes means the platform is replacing human agent time.

**Usage-led growth:** As customers find value, they use more minutes. This creates natural expansion without active sales.

**Product quality signal:** If minutes drop, either adoption is failing or quality is poor. Both require immediate investigation.

## North Star Metric Breakdown

```typescript
interface NorthStarMetric {
  activeAgentMinutes: number; // Total minutes with active AI conversation
  breakdown: {
    byTenant: TenantMetrics[];
    byAgent: AgentMetrics[];
    byTimeframe: TimeframeMetrics;
    byPlan: PlanMetrics;
  };
  
  components: {
    totalCalls: number;
    avgCallDuration: number; // minutes
    callSuccessRate: number; // % of calls fully handled by AI
    agentUtilization: number; // % of time agents are in active conversation
  };
  
  targets: {
    monthlyGrowth: number; // Target: 15% MoM
    annualTarget: number; // Target: 10M minutes by Year 1
  };
}

function calculateNorthStarProgress(
  current: NorthStarMetric,
  target: number
): NorthStarStatus {
  const progress = current.activeAgentMinutes / target;
  const velocity = current.components.totalCalls * 
    current.components.avgCallDuration * 
    current.components.callSuccessRate;
  
  const predictedDate = projectTargetDate(
    current.activeAgentMinutes,
    current.targets.monthlyGrowth,
    target
  );
  
  return {
    currentValue: current.activeAgentMinutes,
    progressPercent: progress * 100,
    onTrack: progress >= 0.8, // 80% of linear path
    velocity,
    projectedTargetDate: predictedDate,
    risks: identifyRisks(current),
    recommendations: generateRecommendations(current),
  };
}
```

## Supporting Metrics

### Input Metrics (Leading Indicators)
- **New agent deployments:** Weekly count of new agents deployed
- **Onboarding completion rate:** % of signups completing first call
- **Call volume growth:** Week-over-week call count change
- **First call quality score:** % of first calls with successful outcome

### Output Metrics (Lagging Indicators)
- **Minutes per customer:** Average active minutes per paying customer
- **Minutes per agent:** Average minutes per deployed agent
- **Revenue per minute:** Blended average revenue per minute
- **Customer lifetime minutes:** Total minutes over customer lifetime

## Dashboard & Reporting

```
North Star Dashboard
┌─────────────────────────────────────────────────────────────────────────┐
│ Active Agent Minutes: 847,239     Daily: 28,241  MTD: 847,239          │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │                                                                     │ │
│ │  Monthly Active Minutes Chart                                       │ │
│ │  ████████████████████████████████████████░░░░░░░░░░░░ 847K / 1M   │ │
│ │                                                                     │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ Deployed Agents: 1,247   Success Rate: 94.2%   Avg Duration: 3.7min   │
│ Growth (WoW): +12.3%     On Track: ✅         ETA: March 15           │
└─────────────────────────────────────────────────────────────────────────┘
```

## North Star Cascading Goals

| Level | Metric | Target | Owner |
|-------|--------|--------|-------|
| Company | Active agent minutes | 10M/mo by Year 1 | CEO |
| Product | Agent deployment rate | 20% MoM growth | Product |
| Engineering | Call success rate | >98% uptime, <2s latency | Engineering |
| Marketing | Trial-to-activated | >60% conversion | Marketing |
| Sales | Enterprise minutes | 30% of total | Sales |
| CS | Customer health score | >80% healthy | Customer Success |

## Quarterly North Star Reviews

Each quarter, review: (1) Are we on track for annual target? (2) Which segments are driving growth (or decline)? (3) What levers can we pull to accelerate? (4) Is the North Star metric still the right metric?

## Tools & Resources

- **North Star tracking:** PostHog dashboard, ChartMogul
- **Goal cascading:** OKR framework in Notion/Linear
- **Forecasting:** Spreadsheet model + Causal
- **Dashboard:** Metabase, Grafana, PostHog
- **Review cadence:** Weekly metrics review (all hands), Monthly deep-dive, Quarterly OKR review
