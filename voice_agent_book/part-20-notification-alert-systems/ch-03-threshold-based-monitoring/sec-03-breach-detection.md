# Section 03: Breach Detection

## Overview

Breach detection identifies when metric values cross defined thresholds. The system distinguishes between sustained breaches (value remains above threshold for multiple evaluations) and spike breaches (transient spikes). Breach severity is computed based on magnitude, duration, and historical context.

## Implementation Approach

```typescript
type BreachType = 'sustained' | 'spike' | 'recovery';

interface BreachEvent {
  id: string;
  thresholdId: string;
  metricValue: number;
  thresholdValue: number;
  type: BreachType;
  severity: BreachSeverity;
  startedAt: string;
  duration: number;
  magnitude: number; // percentage above threshold
}

interface BreachSeverity {
  level: 'critical' | 'major' | 'minor';
  score: number;
}

class BreachDetector {
  private sustainedBreachTracker: Map<string, SustainedBreachState> = new Map();

  async detect(threshold: Threshold, metricValue: number): Promise<BreachEvent | null> {
    const isBreach = this.evaluateBreach(threshold, metricValue);
    const state = this.getState(threshold.id);

    if (isBreach) {
      state.consecutiveBreaches++;
      state.lastBreachValue = metricValue;

      if (state.consecutiveBreaches >= (threshold.conditions[0]?.sustainedFor || 1)) {
        return this.createBreach(threshold, metricValue, 'sustained', state);
      }
      return this.createBreach(threshold, metricValue, 'spike', state);
    } else {
      if (state.consecutiveBreaches > 0) {
        // Recovery
        const event: BreachEvent = {
          id: generateId(),
          thresholdId: threshold.id,
          metricValue,
          thresholdValue: threshold.conditions[0].value,
          type: 'recovery',
          severity: { level: 'minor', score: 0 },
          startedAt: state.startedAt,
          duration: Date.now() - new Date(state.startedAt).getTime(),
          magnitude: 0,
        };
        this.resetState(threshold.id);
        return event;
      }
      this.resetState(threshold.id);
    }
    return null;
  }

  private evaluateBreach(threshold: Threshold, value: number): boolean {
    return threshold.conditions.some(c => {
      switch (c.operator) {
        case '>': return value > c.value;
        case '>=': return value >= c.value;
        case '<': return value < c.value;
        case '<=': return value <= c.value;
        default: return false;
      }
    });
  }

  private createBreach(threshold: Threshold, value: number, type: BreachType, state: SustainedBreachState): BreachEvent {
    const magnitude = Math.abs((value - threshold.conditions[0].value) / threshold.conditions[0].value) * 100;
    return {
      id: generateId(),
      thresholdId: threshold.id,
      metricValue: value,
      thresholdValue: threshold.conditions[0].value,
      type,
      severity: this.computeSeverity(magnitude, state.consecutiveBreaches),
      startedAt: state.startedAt,
      duration: Date.now() - new Date(state.startedAt).getTime(),
      magnitude,
    };
  }

  private computeSeverity(magnitude: number, consecutiveBreaches: number): BreachSeverity {
    if (magnitude > 50 || consecutiveBreaches > 10) return { level: 'critical', score: 1.0 };
    if (magnitude > 25 || consecutiveBreaches > 5) return { level: 'major', score: 0.7 };
    return { level: 'minor', score: 0.3 };
  }
}
```

## Integration Points

- **Threshold Evaluator**: Receives evaluation results
- **Alert Engine**: Creates alerts from breach events
- **Dashboard**: Shows active breaches

## Production Considerations

- **Consecutive Breach Tuning**: Adjust sustained_for to balance sensitivity vs false positives
- **Severity Calibration**: Review severity distribution regularly
- **Recovery Detection**: Alert resolution triggers on recovery
