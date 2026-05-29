# Section 07: Customer Satisfaction Metrics

## Satisfaction Framework

Customer satisfaction metrics measure how customers perceive the value, quality, and support experience of our platform. These are leading indicators of retention, expansion, and advocacy.

```
Satisfaction Metrics Hierarchy
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                       Net Promoter Score (NPS)                         │
│                    "How likely to recommend?"                           │
│                            ▲                                            │
│            ┌───────────────┼───────────────┐                            │
│            │               │               │                            │
│     Customer Sat.     Customer Effort    Support                       │
│     Score (CSAT)      Score (CES)        Satisfaction                  │
│     "Satisfied?"      "Easy to use?"     "Helped?"                     │
│            │               │               │                            │
│            ▼               ▼               ▼                            │
│    Post-call survey   In-app survey     Ticket feedback                 │
│                      (Sprig)           (CSAT after close)               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Satisfaction Metrics

### Net Promoter Score (NPS)
**Scale:** 0-10 (Detractors 0-6, Passives 7-8, Promoters 9-10). **Target:** >40 (good), >60 (great). **Frequency:** Monthly to all active users. **Channel:** Email + in-app (Sprig).

### Customer Satisfaction Score (CSAT)
**Scale:** 1-5. **Target:** >4.2/5.0. **Frequency:** After every call (post-call survey). **Channel:** IVR + SMS.

### Customer Effort Score (CES)
**Scale:** 1-7 (1 = very difficult, 7 = very easy). **Target:** >5.5. **Frequency:** Weekly (in-app). **Channel:** In-app widget (Sprig).

### Support Satisfaction
**Scale:** 1-5. **Target:** >4.5/5.0. **Frequency:** After every ticket close. **Channel:** Email survey.

## Satisfaction Data Model

```typescript
interface SatisfactionMetrics {
  nps: {
    score: number;
    promoters: number;
    passives: number;
    detractors: number;
    responses: number;
  };
  
  csat: {
    score: number;
    bySegment: Record<string, number>;
    postCallScore: number;
    responses: number;
  };
  
  ces: {
    score: number;
    byFeature: Record<string, number>;
    responses: number;
  };
  
  support: {
    csat: number;
    avgResolutionTime: number;
    firstResponseTime: number;
    ticketsByCategory: Record<string, number>;
  };
  
  trends: {
    weeklyNPS: number[];
    monthlyCSAT: number[];
    quarterlyCES: number[];
  };
}

function analyzeSatisfaction(metrics: SatisfactionMetrics): SatisfactionAnalysis {
  const promoterScore = metrics.nps.promoters / metrics.nps.responses;
  const detractorScore = metrics.nps.detractors / metrics.nps.responses;
  
  const topComplaints = Object.entries(metrics.support.ticketsByCategory)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 3)
    .map(([category, count]) => ({ category, count }));
  
  return {
    npsScore: promoterScore - detractorScore,
    isHealthy: metrics.nps.score > 40,
    topComplaints,
    atRiskAccounts: findAtRiskByNPS(metrics),
    recommendedActions: generateActions(topComplaints),
  };
}
```

## Survey Implementation

### Post-Call IVR Survey
After call ends: "On a scale of 1 to 5, how satisfied were you with this call?" Voice response captured and analyzed.

### In-App NPS Survey (Sprig)
Monthly: "How likely are you to recommend our platform to a colleague?" (0-10). Follow-up: "What's the primary reason for your score?"

### In-App CES Survey
After key actions (agent creation, integration setup): "How easy was it to [action]?" (1-7).

### Churn Survey
On cancellation: "What's the primary reason you're leaving?" Multi-choice + free text.

## Satisfaction Dashboard

```
Satisfaction Dashboard (May 2026)
┌─────────────────────────────────────────────────────────────────────────┐
│ NPS: 52 (+3 pts MoM)   CSAT: 4.3/5.0   CES: 5.8/7.0                  │
│                                                                         │
│ NPS Distribution                                                        │
│ Promoters (9-10): 62%   Passives (7-8): 22%   Detractors (0-6): 16%  │
│                                                                         │
│ CSAT Trend                                                               │
│ 4.5 ┤███████████████████████████████                                   │
│ 4.0 ┤███████████████████████████████████████████████████               │
│ 3.5 ┤████████████                                                        │
│ 3.0 ┤█████                                                              │
│     └────────────────────────────────────────────                         │
│       Jan   Feb   Mar   Apr   May                                       │
│                                                                         │
│ Top Complaints: "Latency" (23), "Voice quality" (18), "Pricing" (12)  │
│ Support CSAT: 4.6/5.0   Avg Resolution: 4.2 hours                     │
└─────────────────────────────────────────────────────────────────────────┘
```

## Satisfaction Targets by Segment

| Segment | NPS Target | CSAT Target | CES Target | Primary Driver |
|---------|-----------|-------------|------------|----------------|
| Free users | >20 | >3.8 | >5.0 | Ease of use |
| Starter | >30 | >4.0 | >5.5 | Value for money |
| Pro | >40 | >4.2 | >6.0 | Feature depth |
| Business | >50 | >4.4 | >6.5 | Support + reliability |
| Enterprise | >60 | >4.6 | >6.5 | Compliance + support |

## Satisfaction Improvement Levers

| Lever | NPS Impact | Timeline | Implementation |
|-------|-----------|----------|----------------|
| Reduce latency by 500ms | +5-8 pts | 4-8 weeks | GPU optimization, edge inference |
| Improve TTS naturalness | +3-5 pts | 4-6 weeks | Coqui XTTS v2 upgrade |
| Faster support response | +2-4 pts | 2 weeks | Chat-first support, SLA enforcement |
| Proactive usage insights | +3-5 pts | 6-8 weeks | Monthly ROI report |
| Template library expansion | +2-3 pts | Ongoing | Community + internal templates |

## Closed-Loop Feedback

Every detractor (NPS 0-6) receives: (1) Automated email from founder within 24 hours, (2) Phone call from customer success within 48 hours (if email not replied), (3) Follow-up after issue resolution.

## Tools & Resources

- **NPS/CSAT surveys:** Sprig, Delighted, Satismeter
- **Post-call IVR survey:** Custom (voice agent) + Twilio
- **Churn survey:** Intercom, Customer.io
- **Feedback analysis:** Thematic, MonkeyLearn
- **Support analytics:** Zendesk, Intercom, Freshdesk
- **Customer success:** HubSpot, Gainsight, Churned
