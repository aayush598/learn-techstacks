# Section 05: Quality Alerts & Thresholds

## Overview

Quality alerts notify operations when call quality degrades below acceptable thresholds. Thresholds are defined per metric (MOS < 3.0, jitter > 50ms, packet loss > 3%) and can be aggregated across calls, agents, or regions. Alerts are routed based on severity: warning (investigate during business hours), critical (immediate action required).

## Implementation Approach

```typescript
interface QualityThreshold {
  metric: string;
  warning: number;
  critical: number;
  window: number; // Sliding window in seconds
  minSamples: number; // Minimum data points before alerting
}

const defaultThresholds: QualityThreshold[] = [
  { metric: 'mos', warning: 3.5, critical: 3.0, window: 300, minSamples: 10 },
  { metric: 'jitter', warning: 30, critical: 50, window: 60, minSamples: 5 },
  { metric: 'packetLoss', warning: 1, critical: 3, window: 60, minSamples: 5 },
  { metric: 'rtt', warning: 200, critical: 400, window: 60, minSamples: 5 },
];

class QualityAlertEngine {
  evaluate(calls: CallQuality[]): Alert[] {
    const alerts: Alert[] = [];
    const windowed = this.getWindowedData(calls);

    for (const threshold of defaultThresholds) {
      const values = windowed.filter(w => w.metric === threshold.metric);
      if (values.length < threshold.minSamples) continue;

      const avg = values.reduce((s, v) => s + v.value, 0) / values.length;
      const severity = avg <= threshold.critical ? 'critical' :
                       avg <= threshold.warning ? 'warning' : null;

      if (severity) {
        alerts.push({
          id: uuid(),
          severity,
          metric: threshold.metric,
          current: avg,
          threshold: threshold[severity],
          timestamp: new Date(),
          message: `${threshold.metric} degraded: ${avg.toFixed(1)} (threshold: ${threshold[severity]})`,
        });
      }
    }

    return alerts;
  }
}
```

## Integration Points

- **AlertManager**: Routes alerts to Slack/PagerDuty
- **Quality Dashboard**: Current threshold status
- **On-Call**: Critical alerts page on-call engineer

## Production Considerations

- **Alert Fatigue**: Tune thresholds to minimize false positives
- **Seasonal Patterns**: Account for daily/weekly traffic patterns
- **Silencing**: Maintenance windows suppress known degradations
