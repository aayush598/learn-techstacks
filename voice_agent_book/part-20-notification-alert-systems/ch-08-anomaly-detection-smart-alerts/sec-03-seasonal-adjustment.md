# Section 03: Seasonal Adjustment

## Overview

Seasonal adjustment removes predictable periodic patterns from metrics to reveal underlying trends and anomalies. Time series decomposition separates data into trend, seasonal, and residual components. Holiday effects and day-of-week patterns are modeled to prevent false alerts from expected cyclical behavior.

## Architecture

```
Time Series Decomposition
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Raw Metric] → [Decomposition] → [Components] → [Adjusted Value]
     │                │                │                │
  Original         STL or         Trend: long-term   Residual =
  time series      additive        direction         raw - trend - seasonal
  data             decomposition                     Used for anomaly
                     │              Seasonal:        detection
                  Smooth,         weekly, daily,
                  loess-based     hourly patterns
                  seasonal
                  extraction      Residual: noise,
                                  anomalies,
                                  irregularities

Example: Call Volume by Day of Week
  Raw:
  1200 ┤    ╭──╮
  1000 ┤   ╭╯  ╰╮
   800 ┤  ╭╯    ╰╮
      ─┼──╯      ╰────────
       Mon Tue Wed Thu Fri Sat Sun

  Seasonal Component:
    +200 ┤╭──╮          ╭──╮╭──╮
       0 ┤╯  ╰──────────╯  ╰╯  ╰──
    -200 ┤
       Mon Tue Wed Thu Fri Sat Sun

  Residual (after removing seasonal + trend):
     +50 ┤  ·
       0 ┤──·────·──·────·────·──
     -50 ┤     ·           ·
       Mon Tue Wed Thu Fri Sat Sun
```

## Design Decisions

- **STL Decomposition**: Robust to outliers, handles any seasonality period
- **Multi-Seasonality**: Daily, weekly, and annual patterns modeled separately
- **Holiday Calendar**: Pre-defined holiday list prevents false positives
- **Additive Decomposition**: Assumes seasonal amplitude constant over time

## Implementation Approach

```typescript
interface SeasonalConfig {
  metric: string;
  periods: number[]; // e.g., [24, 168] for hourly and weekly
  holidayCalendar?: string[]; // ISO date strings
  seasonalSmoothing?: number;
  trendSmoothing?: number;
}

interface DecomposedComponents {
  trend: number[];
  seasonal: number[];
  residual: number[];
  adjustedValues: number[]; // raw - seasonal
  strength: {
    trend: number;
    seasonal: number;
    residual: number;
  };
}

class SeasonalAdjustmentService {
  private holidayCache: Set<string> = new Set();

  async decompose(data: number[], config: SeasonalConfig): Promise<DecomposedComponents> {
    const n = data.length;
    const trend = this.computeTrend(data, config.trendSmoothing || n / 3);

    const seasonal = this.computeSeasonal(data, trend, config);
    const residual = data.map((v, i) => v - trend[i] - seasonal[i]);
    const adjustedValues = data.map((v, i) => v - seasonal[i]);
    const strength = this.computeStrength(data, trend, seasonal, residual);

    return { trend, seasonal, residual, adjustedValues, strength };
  }

  private computeTrend(data: number[], smoothingWindow: number): number[] {
    const trend: number[] = [];
    const halfWindow = Math.floor(smoothingWindow / 2);

    for (let i = 0; i < data.length; i++) {
      const start = Math.max(0, i - halfWindow);
      const end = Math.min(data.length, i + halfWindow + 1);
      const window = data.slice(start, end);
      trend.push(window.reduce((s, v) => s + v, 0) / window.length);
    }

    return trend;
  }

  private computeSeasonal(data: number[], trend: number[], config: SeasonalConfig): number[] {
    const detrended = data.map((v, i) => v - trend[i]);

    // Compute seasonal factors for each period
    const seasonal: number[] = new Array(data.length).fill(0);

    for (const period of config.periods) {
      if (period >= data.length) continue;

      const seasonalFactors: number[] = [];
      for (let p = 0; p < period; p++) {
        const values: number[] = [];
        for (let i = p; i < data.length; i += period) {
          values.push(detrended[i]);
        }
        const median = values.sort((a, b) => a - b)[Math.floor(values.length / 2)];
        seasonalFactors.push(median);
      }

      // Normalize factors to sum to zero
      const meanFactor = seasonalFactors.reduce((s, v) => s + v, 0) / seasonalFactors.length;
      const normalizedFactors = seasonalFactors.map(v => v - meanFactor);

      for (let i = 0; i < data.length; i++) {
        seasonal[i] += normalizedFactors[i % period];
      }
    }

    return seasonal;
  }

  private computeStrength(
    data: number[], trend: number[], seasonal: number[], residual: number[]
  ): DecomposedComponents['strength'] {
    const varTotal = this.variance(data);
    const varResidual = this.variance(residual);

    return {
      trend: 1 - this.variance(residual) / this.variance(data.map((v, i) => v - trend[i])),
      seasonal: 1 - this.variance(residual) / this.variance(data.map((v, i) => v - seasonal[i])),
      residual: this.variance(residual) / varTotal,
    };
  }

  private variance(values: number[]): number {
    const mean = values.reduce((s, v) => s + v, 0) / values.length;
    return values.reduce((s, v) => s + (v - mean) ** 2, 0) / values.length;
  }

  isHoliday(date: Date, calendar?: string[]): boolean {
    const dateStr = date.toISOString().slice(0, 10);
    return calendar?.includes(dateStr) || false;
  }

  async applyHolidayAdjustment(
    data: number[], timestamps: Date[], calendar: string[]
  ): Promise<number[]> {
    const adjusted = [...data];

    for (let i = 0; i < timestamps.length; i++) {
      if (this.isHoliday(timestamps[i], calendar)) {
        // Replace holiday value with average of surrounding non-holiday days
        const before = adjusted.slice(Math.max(0, i - 7), i);
        const after = adjusted.slice(i + 1, i + 8);
        const surrounding = [...before, ...after]
          .filter((_, idx) => !this.isHoliday(
            timestamps[Math.max(0, i - 7) + idx] || timestamps[i],
            calendar
          ));

        if (surrounding.length > 0) {
          adjusted[i] = surrounding.reduce((s, v) => s + v, 0) / surrounding.length;
        }
      }
    }

    return adjusted;
  }
}
```

## Integration Points

- **Metrics Pipeline**: Raw metric data ingested before seasonal adjustment
- **Anomaly Detection**: Adjusted values (residuals) used for anomaly scoring
- **Holiday Calendar API**: External calendar integration for holiday dates

## Production Considerations

- **Seasonal Strength Validation**: Low seasonal strength indicates no seasonal adjustment needed
- **Recalculation Frequency**: Seasonal factors recomputed weekly
- **Holiday Calendar Maintenance**: Automatically updated from public holiday APIs

## Open-Source Tools

- **simple-statistics**: Variance and median calculations
- **date-holidays**: Holiday detection library
