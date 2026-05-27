# Section 08: Retry Analytics & Optimization

## Overview

Retry analytics provides insights into how effectively the retry system is performing and identifies opportunities for optimization. Without analytics, retry configuration is guesswork — are we retrying too aggressively? Too conservatively? Are certain retry patterns more effective than others? The analytics system tracks retry effectiveness across multiple dimensions and provides actionable recommendations for configuration improvements.

Key metrics include answer rate by attempt number, conversion rate by attempt number, optimal interval between attempts, attempt-to-connect ratio, and cost per successful contact. The system also supports A/B testing of retry strategies, allowing operators to compare different interval configurations, prioritization schemes, and exhaustion rules against each other in controlled experiments.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Audio    |--->| WebSocket|--->| Jitter   |--->| PLC      |--->| Player   |
| Producer |    | (WSS)    |    | Buffer   |    | (Packet  |    | (smooth  |
| (100ms   |    | (binary) |    | (adaptive|    |  Loss    |    |  output) |
|  chunks) |    |          |    |  60-200) |    |  Conceal)|    +----------+
+----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```
class RetryAnalytics {
  constructor(analyticsDb, campaignService) {
    this.db = analyticsDb;
    this.campaigns = campaignService;
  }

  async getRetryMetrics(campaignId, dateRange) {
    const metrics = {};

    // Attempt-level breakdown
    metrics.byAttempt = await this.db.$queryRaw`
      SELECT 
        attempt_number,
        COUNT(*) as total_attempts,
        SUM(CASE WHEN outcome = 'answered' THEN 1 ELSE 0 END) as answers,
        SUM(CASE WHEN disposition IN ('converted', 'sale', 'meeting_booked') 
            THEN 1 ELSE 0 END) as conversions,
        AVG(CASE WHEN outcome = 'answered' THEN duration_ms END) as avg_duration,
        COUNT(DISTINCT contact_id) as unique_contacts
      FROM call_attempts
      WHERE campaign_id = ${campaignId}
        AND timestamp BETWEEN ${dateRange.start} AND ${dateRange.end}
      GROUP BY attempt_number
      ORDER BY attempt_number
    `;

    // Calculate rates
    metrics.byAttempt = metrics.byAttempt.map(row => ({
      ...row,
      answer_rate: row.answers / row.total_attempts,
      conversion_rate: row.conversions / row.total_attempts,
      cost_per_attempt: 0.02, // From billing service
      cost_per_conversion: row.conversions > 0 
        ? (row.total_attempts * 0.02) / row.conversions 
        : null
    }));

    // Interval effectiveness
    metrics.intervalEffectiveness = await this.analyzeIntervalEffectiveness(
      campaignId, dateRange
    );

    // Outcome distribution
    metrics.outcomeDistribution = await this.db.$queryRaw`
      SELECT outcome, COUNT(*) as count
      FROM call_attempts
      WHERE campaign_id = ${campaignId}
        AND timestamp BETWEEN ${dateRange.start} AND ${dateRange.end}
      GROUP BY outcome
      ORDER BY count DESC
    `;

    return metrics;
  }

  async analyzeIntervalEffectiveness(campaignId, dateRange) {
    // For each pair of consecutive attempts, calculate the interval
    // and whether the subsequent attempt was answered
    const result = await this.db.$queryRaw`
      WITH attempt_pairs AS (
        SELECT 
          a1.contact_id,
          a1.timestamp as prev_time,
          a2.timestamp as next_time,
          a2.outcome as next_outcome,
          EXTRACT(EPOCH FROM (a2.timestamp - a1.timestamp)) / 3600 as interval_hours
        FROM call_attempts a1
        JOIN call_attempts a2 
          ON a1.contact_id = a2.contact_id 
          AND a1.campaign_id = a2.campaign_id
          AND a2.attempt_number = a1.attempt_number + 1
        WHERE a1.campaign_id = ${campaignId}
          AND a2.timestamp BETWEEN ${dateRange.start} AND ${dateRange.end}
      )
      SELECT 
        CASE 
          WHEN interval_hours < 0.5 THEN '< 30 min'
          WHEN interval_hours < 1 THEN '30-60 min'
          WHEN interval_hours < 2 THEN '1-2 hours'
          WHEN interval_hours < 4 THEN '2-4 hours'
          WHEN interval_hours < 24 THEN '4-24 hours'
          ELSE '> 24 hours'
        END as interval_bucket,
        COUNT(*) as attempts,
        SUM(CASE WHEN next_outcome = 'answered' THEN 1 ELSE 0 END) as answers,
        AVG(interval_hours) as avg_interval
      FROM attempt_pairs
      GROUP BY interval_bucket
      ORDER BY avg_interval
    `;

    return result.map(row => ({
      ...row,
      answer_rate: row.answers / row.attempts
    }));
  }

  async getOptimizationRecommendations(campaignId) {
    const metrics = await this.getRetryMetrics(campaignId, { 
      start: new Date(Date.now() - 30 * 86400000), 
      end: new Date() 
    });

    const recommendations = [];

    // Analyze diminishing returns of additional attempts
    const attempts = metrics.byAttempt;
    for (let i = 1; i < attempts.length; i++) {
      const prevRate = attempts[i - 1].answer_rate;
      const currRate = attempts[i].answer_rate;
      const drop = ((prevRate - currRate) / prevRate) * 100;

      if (drop > 30 && attempts[i].conversion_rate < 0.01) {
        recommendations.push({
          type: 'reduce_max_attempts',
          priority: 'high',
          message: `Attempt ${i + 1} has ${drop.toFixed(0)}% lower answer rate than attempt ${i} with negligible conversion. Consider reducing max attempts to ${i}.`,
          expectedImpact: `${(attempts[i].total_attempts * 0.02).toFixed(2)} cost savings`
        });
      }
    }

    // Analyze optimal intervals
    const intervals = metrics.intervalEffectiveness;
    if (intervals.length > 0) {
      const bestInterval = intervals.reduce((best, curr) => 
        curr.answer_rate > best.answer_rate ? curr : best
      );

      recommendations.push({
        type: 'optimal_interval',
        priority: 'medium',
        message: `Optimal retry interval is ${bestInterval.interval_bucket} with ${(bestInterval.answer_rate * 100).toFixed(1)}% answer rate. Consider adjusting current interval strategy.`,
        expectedImpact: '5-15% improvement in answer rates'
      });
    }

    // Analyze exhaustion patterns
    const exhaustionRate = attempts[attempts.length - 1]?.total_attempts / 
      attempts.reduce((sum, a) => sum + a.total_attempts, 0) * 100;

    if (exhaustionRate > 10) {
      recommendations.push({
        type: 'high_exhaustion_rate',
        priority: 'medium',
        message: `${exhaustionRate.toFixed(1)}% of attempts are on the final attempt. Consider SMS/email fallback before final voice attempt.`,
        expectedImpact: 'Improved contact rates at lower cost'
      });
    }

    return recommendations;
  }

  async abTestRetryStrategy(campaignId, testConfig) {
    // Create an A/B test for retry strategies
    const test = await this.campaigns.createABTest(campaignId, {
      name: `Retry Strategy Test - ${new Date().toISOString()}`,
      variable: 'retry_strategy',
      controlConfig: testConfig.currentConfig,
      variantConfig: testConfig.proposedConfig,
      split: testConfig.split || 0.5,
      minSampleSize: testConfig.minSampleSize || 1000,
      metrics: ['answer_rate', 'conversion_rate', 'cost_per_conversion'],
      minDuration: testConfig.minDuration || 7 // days
    });

    return test;
  }
}
```

## Integration Points

- **Attempt History (sec-05):** Primary data source for retry metrics
- **Campaign Configuration (Ch 01):** Optimization recommendations modify retry configuration
- **A/B Testing (Ch 10):** Retry strategy A/B testing integration
- **Billing (Part 17):** Cost per attempt data for financial metrics
- **Billing/Telephony (Part 07):** Telephony cost per minute for cost tracking
- **Analytics Dashboard (Part 11):** Retry analytics displayed in campaign dashboards
- **ML Pipeline:** Retry strategy optimization model training

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Retry analytics queries can be heavy on large datasets — use materialized views or ClickHouse for sub-second query performance
- A/B tests require sufficient sample size — recommend minimum 1,000 contacts per variant
- Interval effectiveness analysis requires pairs of consecutive attempts — ensure the data model supports this join
- Cost-per-conversion optimization may conflict with customer experience goals — balance financial and experience metrics
- Retry analytics should be available in real-time (last hour) and historical (last 30 days) views
- Optimization recommendations should include confidence scores based on data volume
- Track retry strategy changes and their impact over time — did the recommended change actually improve metrics?
- Export retry analytics for external analysis and regulatory reporting
- Consider seasonality in retry metrics — answer rates vary by day of week and time of month
- Provide a "retry simulator" that lets operators test different configurations against historical data
