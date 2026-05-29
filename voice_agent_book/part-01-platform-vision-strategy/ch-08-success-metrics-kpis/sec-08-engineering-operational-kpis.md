# Section 08: Engineering & Operational KPIs

## Engineering Excellence Framework

Engineering KPIs measure the health of the development organization. They track velocity, quality, reliability, and operational efficiency. These metrics are reviewed weekly by the engineering team.

```
Engineering KPI Dashboard
┌─────────────────────────────────────────────────────────────────────────┐
│ Velocity              Quality                 Reliability              │
│ ┌────────────────┐   ┌────────────────┐   ┌────────────────┐         │
│ • Deploys/week   │   • Change fail    │   • MTTR           │         │
│ • Lead time      │     rate           │   • MTBF           │         │
│ • Cycle time     │   • Test coverage  │   • Availability    │         │
│ • Throughput     │   • Bug escape     │   • Incident count │         │
│   (story points) │     rate           │   • On-call        │         │
│                  │   • Code review    │     health         │         │
│                  │     coverage       │                    │         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Engineering KPIs

### Velocity Metrics
- **Deployment frequency:** How often code ships to production (target: daily)
- **Lead time:** Time from commit to production (target: <1 hour)
- **Cycle time:** Time from start work to deploy (target: <3 days)
- **Throughput:** Story points delivered per sprint (target: consistent velocity)
- **WIP:** Work in progress (target: <3 items per engineer)

### Quality Metrics
- **Change failure rate:** % of deployments causing failures (target: <5%)
- **Test coverage:** Line coverage (target: >80%), branch coverage (target: >70%)
- **Bug escape rate:** Bugs found in production vs. development (target: <10%)
- **Code review coverage:** % of PRs reviewed (target: 100%)
- **Revert rate:** % of commits reverted (target: <2%)

### Reliability Metrics
- **Mean Time to Resolve (MTTR):** Time to fix production issues (target: <1 hour critical)
- **Mean Time Between Failures (MTBF):** Time between incidents (target: >14 days)
- **Availability:** Service uptime (target: >99.9%)
- **Incident count:** Number of P0/P1 incidents per month (target: <2)
- **On-call health:** Incidents per on-call shift, sleep quality

## Engineering Data Model

```typescript
interface EngineeringKPIs {
  velocity: {
    deploysPerWeek: number;
    leadTimeMinutes: number;
    cycleTimeDays: number;
    throughputStoriesPerSprint: number;
    wipPerEngineer: number;
  };
  
  quality: {
    changeFailureRate: number;
    testCoverage: number;
    bugEscapeRate: number;
    codeReviewCoverage: number;
    revertRate: number;
  };
  
  reliability: {
    mttrMinutes: number;
    mtbfDays: number;
    availabilityPercent: number;
    incidentCount: number;
    onCallHealth: 'good' | 'fair' | 'burnout';
  };
  
  costs: {
    cloudInfraPerCall: number;
    infraPerMAU: number;
    engineeringCostPerCall: number;
    costEfficiencyTrend: number;
  };
}

function calculateEngineeringHealth(kpis: EngineeringKPIs): EngineeringHealth {
  const velocityScore = (
    Math.min(kpis.velocity.deploysPerWeek / 7, 1) * 0.3 +
    Math.max(0, 1 - kpis.velocity.leadTimeMinutes / 60) * 0.3 +
    Math.max(0, 1 - kpis.velocity.cycleTimeDays / 5) * 0.4
  );
  
  const qualityScore = (
    Math.max(0, 1 - kpis.quality.changeFailureRate) * 0.3 +
    kpis.quality.testCoverage * 0.2 +
    Math.max(0, 1 - kpis.quality.bugEscapeRate) * 0.3 +
    kpis.quality.codeReviewCoverage * 0.2
  );
  
  const reliabilityScore = (
    Math.max(0, 1 - kpis.reliability.mttrMinutes / 120) * 0.3 +
    Math.min(kpis.reliability.mtbfDays / 14, 1) * 0.3 +
    Math.max(0, 1 - kpis.reliability.incidentCount / 4) * 0.4
  );
  
  return {
    score: (velocityScore + qualityScore + reliabilityScore) / 3,
    velocityScore,
    qualityScore,
    reliabilityScore,
    risks: identifyRisks(kpis),
    recommendations: generateRecommendations(kpis),
  };
}
```

## SLO Targets

| Service | SLO | Measurement | Burn Rate |
|---------|-----|-------------|-----------|
| Call pipeline | 99.95% success | Error budget: 0.05% | 2% / week |
| API (REST) | 99.9% availability | Uptime monitoring | 5% / week |
| Dashboard | 99.5% availability | Uptime monitoring | 10% / week |
| TTS Generation | 99.9% success | Error budget: 0.1% | 5% / week |
| STT Pipeline | 99.8% success | Error budget: 0.2% | 5% / week |

## Incident Response

```
Incident Severity Levels
┌─────────────────────────────────────────────────────────────────────────┐
│ Severity │ Description       │ Response    │ Communication              │
├─────────────────────────────────────────────────────────────────────────┤
│ P0       │ Complete outage   │ 15 minutes  │ Status page, email, Slack  │
│          │ or data loss      │             │                            │
│ P1       │ Major feature     │ 30 minutes  │ Slack channel, email if    │
│          │ degraded          │             │ customer-impacting          │
│ P2       │ Partial feature   │ 4 hours     │ Slack channel              │
│          │ issue             │             │                            │
│ P3       │ Minor bug, no     │ Next sprint │ Jira ticket                │
│          │ customer impact   │             │                            │
│ P4       │ Cosmetic,         │ Backlog     │ Jira ticket                │
│          │ enhancement       │             │                            │
└─────────────────────────────────────────────────────────────────────────┘
```

## On-Call Process

- **Rotation:** Weekly, 2 engineers (primary + secondary)
- **Hours:** 24/7 for P0/P1, business hours for P2+
- **Follow-the-sun:** US timezone (initial), expanding to EU (Year 2)
- **Compensation:** $500/week on-call stipend + comp time
- **Escalation:** Primary → Secondary → Engineering Manager → CTO

## Deployment Process

```
CI/CD Pipeline (Average: 15 min from merge to production)
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ PR       │→│ Lint +   │→│ Build +  │→│ Staging  │→│ Canary   │→│ Production│
│ Created  │  │ Type     │  │ Unit     │  │ Deploy   │  │ (5%)     │  │ 100%     │
│          │  │ Check    │  │ Tests    │  │ + E2E    │  │ 2 min    │  │          │
│ 1 min    │  │ 2 min    │  │ 3 min    │  │ 5 min    │  │          │  │ 2 min    │
└──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
```

## Engineering Weekly Dashboard

```
Engineering Weekly Dashboard
┌─────────────────────────────────────────────────────────────────────────┐
│ Deploys: 8 this week   Lead Time: 45 min   Cycle Time: 2.1 days      │
│                                                                         │
│ Change Fail Rate: 2.1% (✅ <5%)     Test Coverage: 84% (✅ >80%)     │
│ Incidents: 1 (P2)   MTTR: 38 min    MTBF: 12 days                     │
│                                                                         │
│ Top WIP Items:                                                          │
│ • Marketplace payment flow (3 days active)                              │
│ • Visual builder - drag nodes (2 days active)                           │
│ • SSO integration test automation (1 day active)                        │
│                                                                         │
│ Cost Efficiency: $0.027/call (-12% MoM)     Infra per MAU: $1.42      │
│ Cloud Cost: $8,247 this month ($285/day avg)                           │
└─────────────────────────────────────────────────────────────────────────┘
```

## Tools & Resources

- **Source control:** GitHub (DORA metrics via GitHub Insights)
- **CI/CD:** GitHub Actions
- **Monitoring:** Grafana + Prometheus + Loki + Tempo
- **Incident management:** PagerDuty, Incident.io
- **Error tracking:** Sentry
- **Cost monitoring:** AWS Cost Explorer, Vantage, CloudHealth
- **Project tracking:** Linear (velocity reports)
- **Post-mortems:** Blameless culture, template in Notion
