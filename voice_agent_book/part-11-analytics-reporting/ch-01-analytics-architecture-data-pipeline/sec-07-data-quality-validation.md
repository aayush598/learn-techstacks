# Section 07: Data Quality and Validation

## Overview

Data quality and validation ensures that the analytics pipeline produces accurate, complete, and trustworthy data. Given the volume of events (thousands per second from multiple sources), data quality issues are inevitable: missing fields, duplicate events, out-of-order timestamps, schema violations, and late-arriving data. The data quality framework detects, reports, and (where possible) automatically corrects these issues before they affect dashboards and reports.

The framework implements a three-layer quality strategy: schema validation at ingestion (preventing malformed data from entering the pipeline), real-time quality checks in the stream processor (detecting anomalies in event patterns), and batch-level reconciliation (comparing stream results against batch-computed exact values). Quality dashboards display data health scores, and alerts notify operators of quality degradation.

## Architecture

```
   Events → Ingestion → Stream → Batch → Serving
              |           |        |        |
              v           v        v        v
          Schema      Pattern   Recon-   Quality
          Validate    Detect    ciliation Score
```

## Design Decisions

- **Automated correction of common issues over manual intervention:** The framework automatically corrects known data quality issues: duplicates are deduplicated (using event ID dedup cache), missing timestamps are filled with the ingestion timestamp, out-of-order events are reordered within a 30-second window, and schema violations for optional fields are silently dropped (not rejected). Only irreparable issues (missing required fields, corrupted payloads) are sent to the dead-letter queue for manual review. Trade-off: automated corrections may mask underlying source bugs but prevent data quality issues from blocking the pipeline.

- **Data health score with trend tracking over pass/fail quality checks:** Rather than a binary pass/fail quality gate, the framework computes a continuous data health score (0-100%) based on multiple weighted dimensions: completeness (non-null rates), consistency (distribution similarity to historical baseline), timeliness (ingestion lag), and validity (schema compliance rate). The score is tracked over time — a sudden drop triggers an alert before the score falls below a threshold. Trade-off: a continuous score is more complex to compute but provides early warning of quality degradation.

- **Reconciliation at the aggregate level over record-level comparison:** Rather than comparing every stream-computed metric against the batch-computed exact value (which requires storing all intermediate state), reconciliation compares aggregate metrics at the hourly level. If the stream-reported answered call count for a tenant-hour differs from the batch-computed count by more than 2%, the batch value replaces the stream value and an alert is generated. Trade-off: aggregate reconciliation catches systemic issues but cannot identify which specific records were processed incorrectly by the stream layer.

## Implementation Approach

```
interface DataQualityCheck {
  name: string;
  type: 'schema' | 'completeness' | 'consistency' | 'timeliness' | 'uniqueness';
  severity: 'warning' | 'error' | 'critical';
  evaluate(context: QualityContext): Promise<QualityResult>;
}

interface QualityResult {
  passed: boolean;
  score: number;           // 0-100
  details: string;
  suggestedAction?: string;
}

class DataQualityEngine {
  private checks: DataQualityCheck[] = [];

  async runQualityChecks(tenantId: string, period: { start: Date; end: Date }): Promise<QualityReport> {
    let totalScore = 0;
    const checkResults: QualityCheckResult[] = [];

    for (const check of this.checks) {
      try {
        const result = await check.evaluate({ tenantId, period });
        checkResults.push({
          checkName: check.name,
          type: check.type,
          passed: result.passed,
          score: result.score,
          details: result.details,
        });
        totalScore += result.score;
      } catch (error) {
        checkResults.push({
          checkName: check.name,
          type: check.type,
          passed: false,
          score: 0,
          details: `Check threw exception: ${(error as Error).message}`,
        });
      }
    }

    const healthScore = this.checks.length > 0 ? Math.round(totalScore / this.checks.length) : 100;

    const report: QualityReport = {
      tenantId,
      period,
      healthScore,
      checks: checkResults,
      generatedAt: new Date(),
    };

    if (healthScore < 80) {
      await this.alertService.sendQualityAlert(report);
    }

    return report;
  }

  registerCheck(check: DataQualityCheck) {
    this.checks.push(check);
  }
}

// Built-in quality checks
const COMPLETENESS_CHECK: DataQualityCheck = {
  name: 'Field Completeness',
  type: 'completeness',
  severity: 'warning',
  evaluate: async (ctx) => {
    const query = `
      SELECT
        countIf(duration IS NULL) / count() * 100 AS durationNullPct,
        countIf(customerPhone IS NULL) / count() * 100 AS phoneNullPct,
        countIf(agentId IS NULL) / count() * 100 AS agentNullPct
      FROM call_events
      WHERE tenantId = '${ctx.tenantId}'
        AND timestamp BETWEEN '${ctx.period.start.toISOString()}' AND '${ctx.period.end.toISOString()}'
    `;
    const result = await clickHouse.query(query);
    const nullRates = result[0];

    // Score based on null rates
    const nullScore = Math.max(0, 100 - (nullRates.durationNullPct + nullRates.phoneNullPct * 2 + nullRates.agentNullPct));
    return {
      passed: nullScore >= 80,
      score: nullScore,
      details: `Null rates: duration=${nullRates.durationNullPct.toFixed(1)}%, phone=${nullRates.phoneNullPct.toFixed(1)}%, agent=${nullRates.agentNullPct.toFixed(1)}%`,
      suggestedAction: nullScore < 80 ? 'Check event producers (telephony engine) for missing fields' : undefined,
    };
  },
};

const CONSISTENCY_CHECK: DataQualityCheck = {
  name: 'Distribution Consistency',
  type: 'consistency',
  severity: 'warning',
  evaluate: async (ctx) => {
    // Compare current duration distribution to historical baseline
    const baselineQuery = `
      SELECT avg(duration) as avgDuration, quantile(0.5)(duration) as p50
      FROM call_events
      WHERE tenantId = '${ctx.tenantId}'
        AND timestamp BETWEEN '${new Date(ctx.period.start.getTime() - 86400000).toISOString()}' AND '${ctx.period.start.toISOString()}'
    `;
    const currentQuery = `
      SELECT avg(duration) as avgDuration, quantile(0.5)(duration) as p50
      FROM call_events
      WHERE tenantId = '${ctx.tenantId}'
        AND timestamp BETWEEN '${ctx.period.start.toISOString()}' AND '${ctx.period.end.toISOString()}'
    `;

    const baseline = await clickHouse.query(baselineQuery);
    const current = await clickHouse.query(currentQuery);

    if (!baseline[0] || !current[0]) return { passed: true, score: 100, details: 'Insufficient data for comparison' };

    const avgDiff = Math.abs(current[0].avgDuration - baseline[0].avgDuration) / baseline[0].avgDuration * 100;
    const score = Math.max(0, 100 - avgDiff * 2);

    return {
      passed: score >= 80,
      score,
      details: `Average duration changed by ${avgDiff.toFixed(1)}% vs yesterday`,
      suggestedAction: avgDiff > 20 ? 'Significant duration change detected — verify no telephony configuration changes' : undefined,
    };
  },
};

const UNIQUENESS_CHECK: DataQualityCheck = {
  name: 'Duplicate Detection',
  type: 'uniqueness',
  severity: 'error',
  evaluate: async (ctx) => {
    const query = `
      SELECT count() - countDistinct(callSid) AS duplicateCount, count() AS total
      FROM call_events
      WHERE tenantId = '${ctx.tenantId}'
        AND timestamp BETWEEN '${ctx.period.start.toISOString()}' AND '${ctx.period.end.toISOString()}'
    `;
    const result = await clickHouse.query(query);
    const dupRate = result[0].total > 0 ? (result[0].duplicateCount / result[0].total) * 100 : 0;
    const score = Math.max(0, 100 - dupRate * 10);

    return {
      passed: dupRate < 5,
      score,
      details: `${result[0].duplicateCount} duplicates out of ${result[0].total} events (${dupRate.toFixed(2)}%)`,
      suggestedAction: dupRate > 5 ? 'Duplicate rate elevated — check producer idempotency and dedup configuration' : undefined,
    };
  },
};

// Register default checks
const qualityEngine = new DataQualityEngine();
qualityEngine.registerCheck(COMPLETENESS_CHECK);
qualityEngine.registerCheck(CONSISTENCY_CHECK);
qualityEngine.registerCheck(UNIQUENESS_CHECK);
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Great Expectations (Apache 2.0) | Python | Data quality validation |
| Soda (Apache 2.0) | Python | Data quality monitoring |
| Deequ (Apache 2.0) | JVM | Spark data quality checks |

## Production Considerations

**Scaling:** Data quality checks query ClickHouse — ensure queries are optimized with indexes and use materialized views for baseline comparisons. Heavy checks (full distribution comparison) run hourly; lightweight checks (completeness, uniqueness) run every 5 minutes. Store quality check results in a separate ClickHouse table (small, fast queries) with 90-day retention. Alerting should be on trend (3 consecutive declining scores) rather than single-point failures.

**Security:** Quality reports contain tenant-level metric summaries — ensure they are accessible only to authorized admin users. Quality dashboards should not expose raw event data. Data quality alert content should be sanitized (no PII in alert messages).

**Monitoring:** Track the monitoring system itself — data quality check execution time, success/failure rate of checks, and quality score trends per tenant. Alert on check execution failures (the quality system itself failing), health scores dropping below 70% for any tenant, and persistent quality issues that survive automated correction.
