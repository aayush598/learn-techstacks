# Section 03: Latency Budgets & Allocation

## Overview

Latency budgets define maximum acceptable time for each pipeline stage. Budgets are allocated based on user experience requirements and technical constraints. The total E2E budget is decomposed into per-component allocations, each with its own monitoring and enforcement. Budgets are enforced in CI and production.

## Budget Allocation

```
Total E2E Budget: 2000ms (p95)

Allocation:
├── Network & Transport: 200ms (10%)
│   ├── Audio upload: 100ms
│   └── Response download: 100ms
├── Voice Pipeline: 1500ms (75%)
│   ├── VAD: 50ms
│   ├── STT: 400ms
│   ├── LLM: 800ms
│   └── TTS: 250ms
├── Application Logic: 200ms (10%)
│   ├── Intent matching: 50ms
│   ├── Context building: 50ms
│   └── Response formatting: 100ms
└── Buffer/Margin: 100ms (5%)
```

## Implementation Approach

```typescript
interface BudgetDef {
  stage: string;
  budget: number; // ms
  current: number; // ms (rolling average)
  tolerance: number; // % over budget before alert
}

class BudgetEnforcer {
  private budgets: Map<string, BudgetDef> = new Map();

  constructor() {
    this.budgets.set('vad', { stage: 'vad', budget: 50, current: 0, tolerance: 20 });
    this.budgets.set('stt', { stage: 'stt', budget: 400, current: 0, tolerance: 15 });
    this.budgets.set('llm', { stage: 'llm', budget: 800, current: 0, tolerance: 10 });
    this.budgets.set('tts', { stage: 'tts', budget: 250, current: 0, tolerance: 20 });
  }

  check(stage: string, measured: number): BudgetCheck {
    const def = this.budgets.get(stage);
    if (!def) return { stage, withinBudget: true };

    const usagePercent = (measured / def.budget) * 100;
    const withinBudget = usagePercent <= (100 + def.tolerance);
    
    if (!withinBudget) {
      this.alert(stage, measured, def.budget);
    }

    return { stage, withinBudget, used: measured, budget: def.budget, usagePercent };
  }

  private alert(stage: string, current: number, budget: number): void {
    logger.warn({ stage, current, budget, percentage: (current/budget)*100 }, 'Budget exceeded');
    metrics.increment('latency_budget_exceeded', { stage });
  }
}
```

## Integration Points

- **CI Pipeline**: Budgets enforced in CI as performance gates
- **Production Monitoring**: Real-time budget tracking in dashboards
- **Alerting**: Budget violations trigger alerts

## Production Considerations

- **Budget Reviews**: Review budgets quarterly against user research
- **Headroom**: Maintain buffer in budgets for traffic spikes
- **User Perception**: Budgets based on user-perceived latency, not technical measurements
