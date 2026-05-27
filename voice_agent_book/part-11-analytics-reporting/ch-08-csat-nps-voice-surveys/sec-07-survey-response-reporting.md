# Section 07: Survey Response Reporting

## Overview

The survey response reporting system transforms raw CSAT, NPS, and voice survey data into actionable dashboards, scheduled reports, and exportable datasets. It provides both real-time summaries (last 24 hours of responses) and historical trend analysis (daily, weekly, monthly aggregates) with filtering by agent, campaign, channel, and survey type. Reports are consumed through the analytics dashboard UI, emailed PDF snapshots, and API access for integration with external BI tools.

The reporting engine supports common survey-specific visualizations: CSAT score trend lines with confidence intervals, NPS gauge charts with Promoter/Passive/Detractor breakdowns, response rate funnels (delivered → opened → started → completed), and word cloud visualizations for open-ended feedback. Reports are generated on-demand with sub-5-second response time for the last 90 days of data, or pre-cached hourly for slower queries spanning larger time ranges.

## Architecture

```
               Survey Response Reporting Pipeline

   Survey Responses → Kafka → Survey Response Store
                                  |
                     ┌────────────┴────────────┐
                     ▼                         ▼
               Real-Time Aggregator      Batch Aggregator
               (Redis, 15-min windows)   (TimescaleDB, hourly)
                     |                         |
                     ▼                         ▼
               Materialized Views          Data Mart
               (latest 7 days)          (historical 90d+)
                     |                         |
                     └────────────┬────────────┘
                                  ▼
                          Report Query Engine
                                  |
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
             Dashboard API    PDF Export    CSV/JSON Export
```

## Design Decisions

- **Two-tier aggregation (real-time + batch) over single-tier storage:** Real-time aggregations in Redis (15-minute granularity, 7-day retention) serve dashboard queries with sub-100 ms response time. Batch aggregations in TimescaleDB (hourly granularity, unlimited retention) serve historical reports and exports. The query engine transparently routes range queries to the appropriate tier. Trade-off: queries spanning the boundary between real-time and batch tiers (e.g., "last 8 days") must merge results from both, adding ~50 ms of merge overhead.

- **Materialized view pre-computation over query-time aggregation:** Common report dimensions — per-agent average CSAT, per-campaign NPS, daily response counts by channel — are pre-computed and stored as materialized views that refresh every 15 minutes. This ensures consistent sub-second response for the most-used dashboard queries. Trade-off: pre-computation adds write amplification (each response update may touch 5-10 materialized views), and custom ad-hoc queries that reference non-standard dimensions must fall back to raw aggregation.

- **Open-ended feedback with PII redaction over raw text storage:** Survey comments and transcribed voice feedback are processed through an automated PII redaction pipeline before being stored in the reporting database. The redaction engine uses regex patterns and NER models to mask phone numbers, email addresses, credit card numbers, and names. Redacted text is stored alongside the original (access-controlled) for QA review. Trade-off: redaction can mask clinical terms or product names that look like PII (e.g., "My order number is 123-45-6789"), requiring a manual override workflow.

## Implementation Approach

```typescript
interface SurveyReportQuery {
  tenantId: string;
  surveyTypes?: string[];
  agentIds?: string[];
  campaignIds?: string[];
  channels?: string[];
  startTime: number;
  endTime: number;
  granularity: 'hour' | 'day' | 'week' | 'month';
  metrics: ('response_rate' | 'average_score' | 'distribution' | 'trend')[];
}

interface SurveyReportResult {
  timeSeries: TimeSeriesPoint[];
  summary: SurveySummary;
  distributions: SurveyDistribution[];
  feedbackWords: WordCloudEntry[];
}

interface TimeSeriesPoint {
  timestamp: number;
  metrics: Record<string, number>;
}

interface SurveySummary {
  totalDelivered: number;
  totalResponded: number;
  responseRate: number;
  averageScore: number;
  scoreChange: number; // vs previous period
  promoterPercent?: number;
  detractorPercent?: number;
  npsScore?: number;
}

class SurveyReportEngine {
  private realTimeAggregator: RealTimeAggregator;
  private batchAggregator: BatchAggregator;
  private materializedViews: MaterializedViewStore;

  async generateReport(query: SurveyReportQuery): Promise<SurveyReportResult> {
    const timeSeries = await this.getTimeSeries(query);
    const summary = await this.getSummary(query);
    const distributions = await this.getDistributions(query);
    const feedbackWords = await this.getFeedbackWordCloud(query);

    return { timeSeries, summary, distributions, feedbackWords };
  }

  private async getTimeSeries(
    query: SurveyReportQuery
  ): Promise<TimeSeriesPoint[]> {
    const now = Date.now();
    const isRecent = (now - query.startTime) < 7 * 86400000;

    if (isRecent) {
      // Use real-time aggregator for recent data
      return this.realTimeAggregator.query({
        ...query,
        granularity: query.granularity === 'hour' ? 'hour' : 'day',
      });
    }

    // Use batch aggregator for historical data
    return this.batchAggregator.query(query);
  }

  private async getSummary(query: SurveyReportQuery): Promise<SurveySummary> {
    const cacheKey = `survey:summary:${JSON.stringify(query)}`;
    const cached = await this.materializedViews.get(cacheKey);
    if (cached) return cached;

    const responses = await this.queryRawResponses(query);
    const previousQuery = {
      ...query,
      startTime: query.startTime - (query.endTime - query.startTime),
      endTime: query.startTime,
    };
    const previousResponses = await this.queryRawResponses(previousQuery);

    const delivered = responses.length;
    const responded = responses.filter(r => !r.abandoned).length;
    const previousResponded = previousResponses.filter(r => !r.abandoned).length;

    const validScores = responses.filter(r => !r.abandoned && r.score !== undefined);
    const averageScore = validScores.length > 0
      ? validScores.reduce((sum, r) => sum + r.score, 0) / validScores.length
      : 0;

    const previousValidScores = previousResponses.filter(
      r => !r.abandoned && r.score !== undefined
    );
    const previousAverage = previousValidScores.length > 0
      ? previousValidScores.reduce((sum, r) => sum + r.score, 0) / previousValidScores.length
      : 0;

    const summary: SurveySummary = {
      totalDelivered: delivered,
      totalResponded: responded,
      responseRate: delivered > 0 ? (responded / delivered) * 100 : 0,
      averageScore: Math.round(averageScore * 100) / 100,
      scoreChange: previousAverage > 0
        ? Math.round((averageScore - previousAverage) * 100) / 100
        : 0,
    };

    // Add NPS-specific metrics
    if (query.surveyTypes?.includes('NPS')) {
      const promoters = validScores.filter(r => r.score >= 9).length;
      const detractors = validScores.filter(r => r.score <= 6).length;
      summary.promoterPercent = responded > 0 ? (promoters / responded) * 100 : 0;
      summary.detractorPercent = responded > 0 ? (detractors / responded) * 100 : 0;
      summary.npsScore = Math.round(summary.promoterPercent - summary.detractorPercent);
    }

    // Cache for 5 minutes
    await this.materializedViews.set(cacheKey, summary, 300);

    return summary;
  }

  private async getDistributions(
    query: SurveyReportQuery
  ): Promise<SurveyDistribution[]> {
    if (query.surveyTypes?.includes('NPS')) {
      return this.buildNPSDistribution(query);
    }
    return this.buildCSATDistribution(query);
  }

  private async getFeedbackWordCloud(
    query: SurveyReportQuery
  ): Promise<WordCloudEntry[]> {
    const responses = await this.queryOpenEndedFeedback(query);
    const terms = new Map<string, number>();

    for (const response of responses) {
      if (!response.feedback) continue;
      const words = response.feedback
        .toLowerCase()
        .replace(/[^a-z\s]/g, '')
        .split(/\s+/)
        .filter(w => w.length > 3 && !STOP_WORDS.has(w));

      for (const word of words) {
        terms.set(word, (terms.get(word) || 0) + 1);
      }
    }

    return Array.from(terms.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 50)
      .map(([word, count]) => ({ word, count }));
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| TimescaleDB (Apache 2.0) | Server | Time-series survey data storage |
| Redis (RSAL) | Server | Real-time aggregation cache |
| Elasticsearch (ELASTIC) | Server | Feedback text search and word cloud |
| Puppeteer (Apache 2.0) | Server | PDF report generation |

## Production Considerations

**Scaling:** Report queries covering large time ranges (6+ months) for high-volume tenants use pre-aggregated daily rollups rather than scanning raw responses. The report engine limits queryable time range to 90 days for on-demand queries; longer ranges trigger an async job that emails results. Materialized views are invalidated by a change-data-capture stream from the response store, ensuring cache freshness within 15 minutes.

**Security:** Survey report API endpoints enforce tenant isolation through the authenticated tenant ID (never trust the payload tenant ID). Individual agent scores are hidden when the agent has fewer than 5 responses in the queried period. Open-ended feedback exports require explicit PII review permission and log an audit trail of every export action including the file recipient.

**Monitoring:** Track report generation latency (p99 under 5 seconds for 90-day ranges), materialized view refresh time, cache hit ratio, and export volume by format. Alert if report generation exceeds 30 seconds, if cache hit ratio falls below 70%, or if materialized view refresh takes longer than 5 minutes.
