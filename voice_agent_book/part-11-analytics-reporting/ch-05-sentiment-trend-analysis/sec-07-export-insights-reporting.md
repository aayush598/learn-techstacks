# Section 07: Export and Insights Reporting

## Overview

The export and insights reporting module enables users to extract sentiment analysis data and generated insights into formats suitable for sharing, presentation, and offline analysis. Exports include raw data (CSV, JSON with per-call sentiment scores), summary reports (PDF with charts and trend analysis), and insight cards (auto-generated natural-language summaries of key findings with recommended actions). Reports can be generated on-demand or scheduled for automated delivery.

The insights engine analyzes sentiment data to produce narrative summaries: "Customer sentiment declined 15% this week, driven primarily by the Technical Support queue. The top contributor was hold times exceeding 3 minutes. Recommended action: review hold procedures and consider staffing adjustments during peak hours (2-4 PM)." These insights are generated using a combination of statistical analysis (comparing current period to baseline) and templated natural language generation.

## Architecture

```
            Export and Insights Pipeline

   ClickHouse (sentiment data)
        |
   Insights Generator
   (statistical analysis + NLG templates)
        |
   ┌────┴────────────┐
   |                 |
   Report Builder   Export Formatter
   (PDF with         (CSV, JSON, XLSX)
    charts + text)
   |                 |
   Export API        Scheduled Reports
   (on-demand)       (BullMQ cron)
        |
   Email / Slack / Download
```

## Design Decisions

- **Insight generation using statistical analysis + template-based NLG over LLM-based generation:** Template-based natural language generation (NLG) produces consistent, predictable output that is always accurate and never hallucinates. The system analyzes the data to find statistically significant changes, then fills in pre-written templates with the specific values. LLM-based generation would be more flexible but risks hallucinating findings or producing inconsistent formatting. Trade-off: template-based NLG can only express findings that the templates cover — novel patterns may go unmentioned. Templates are reviewed by the product team and can be extended as new patterns are discovered.

- **Multi-format export engine over single-format focus:** Different stakeholders need different formats: operational teams need CSV (for Excel pivot tables), management needs PDF (for presentations), and data scientists need JSON (for further analysis). The export engine supports CSV, JSON, PDF, and XLSX formats. PDF generation uses a server-side headless browser (Puppeteer) to render React chart components to a PDF. Trade-off: supporting multiple formats triples the development effort for the export module; each format has its own quirks (PDF pagination, CSV encoding, XLSX sheet limits).

- **Scheduled report delivery via BullMQ cron over in-process scheduling:** Report schedules (daily, weekly, monthly) are stored in Redis via BullMQ repeatable jobs. The job processor generates the report, converts it to the requested format, and sends it via the configured channel (email, Slack, S3). Using an external job queue ensures reports are generated even if the web server restarts, and allows scaling report generation across multiple worker processes. Trade-off: BullMQ requires Redis and adds infrastructure complexity, but provides reliable scheduling and retry semantics.

## Implementation Approach

```typescript
interface SentimentReportConfig {
  id: string;
  tenantId: string;
  name: string;
  format: 'csv' | 'json' | 'pdf' | 'xlsx';
  timeRange: { type: 'relative' | 'absolute'; value: string; start?: string; end?: string };
  filters: {
    campaignIds?: string[];
    queueIds?: string[];
    agentIds?: string[];
  };
  includeInsights: boolean;
  includeCharts: boolean;
  schedule?: {
    cron: string;             // e.g., '0 8 * * 1' for Monday 8 AM
    channel: 'email' | 'slack' | 's3';
    recipients?: string[];
    slackChannel?: string;
  };
  createdAt: number;
  updatedAt: number;
}

interface SentimentInsight {
  id: string;
  type: 'trend_change' | 'anomaly' | 'topic_shift' | 'agent_alert' | 'campaign_performance';
  severity: 'info' | 'warning' | 'critical';
  title: string;
  description: string;
  metrics: Record<string, number>;
  recommendation?: string;
  dimensionBreakdown?: Array<{ label: string; value: number; change: number }>;
}

class InsightsGenerator {
  private clickhouse: ClickHouseClient;

  async generateInsights(
    tenantId: string,
    start: number,
    end: number
  ): Promise<SentimentInsight[]> {
    const insights: SentimentInsight[] = [];

    // Trend change detection
    const periodDuration = end - start;
    const previousStart = start - periodDuration;

    const trendChange = await this.detectTrendChange(tenantId, start, end, previousStart);
    if (trendChange) insights.push(trendChange);

    // Topic shift detection
    const topicShifts = await this.detectTopicShifts(tenantId, start, end, previousStart);
    insights.push(...topicShifts);

    // Worst-performing agents
    const agentAlerts = await this.detectAgentAlerts(tenantId, start, end);
    insights.push(...agentAlerts);

    // Campaign performance insights
    const campaignInsights = await this.detectCampaignChanges(tenantId, start, end, previousStart);
    insights.push(...campaignInsights);

    return insights.sort((a, b) => {
      const severityOrder = { critical: 0, warning: 1, info: 2 };
      return severityOrder[a.severity] - severityOrder[b.severity];
    });
  }

  private async detectTrendChange(
    tenantId: string,
    start: number,
    end: number,
    previousStart: number
  ): Promise<SentimentInsight | null> {
    const current = await this.clickhouse.query(`
      SELECT avg(customerSentiment) as avg, count() as count
      FROM call_sentiment_analysis
      WHERE tenantId = '${tenantId}' AND timestamp >= ${start} AND timestamp <= ${end}
    `);

    const previous = await this.clickhouse.query(`
      SELECT avg(customerSentiment) as avg
      FROM call_sentiment_analysis
      WHERE tenantId = '${tenantId}' AND timestamp >= ${previousStart} AND timestamp < ${start}
    `);

    if (current[0].count < 50) return null;

    const currentAvg = current[0].avg;
    const previousAvg = previous[0]?.avg ?? currentAvg;
    const delta = currentAvg - previousAvg;
    const pctChange = previousAvg !== 0 ? (delta / Math.abs(previousAvg)) * 100 : 0;

    if (Math.abs(pctChange) < 5) return null;

    return {
      id: generateId(),
      type: 'trend_change',
      severity: Math.abs(pctChange) > 20 ? 'critical' : Math.abs(pctChange) > 10 ? 'warning' : 'info',
      title: `Customer sentiment ${delta > 0 ? 'improved' : 'declined'} by ${Math.abs(pctChange).toFixed(1)}%`,
      description: `Average sentiment changed from ${previousAvg.toFixed(3)} to ${currentAvg.toFixed(3)} over the past ${this.formatPeriod(start, end)}.`,
      metrics: { previousAvg, currentAvg, delta, pctChange },
      recommendation: delta < 0
        ? 'Review the top contributing factors using the drill-down tool to identify root causes.'
        : 'Continue current practices that are driving improvement.',
    };
  }

  private async detectTopicShifts(
    tenantId: string,
    start: number,
    end: number,
    previousStart: number
  ): Promise<SentimentInsight[]> {
    const insights: SentimentInsight[] = [];

    const topics = await this.clickhouse.query(`
      SELECT
        topicId, topicName,
        avg(sentimentScore) as avgSentiment,
        count() as mentions
      FROM call_topic_sentiment
      WHERE tenantId = '${tenantId}' AND timestamp >= ${start} AND timestamp <= ${end}
      GROUP BY topicId, topicName
      HAVING count() >= 20
    `);

    const previousTopics = await this.clickhouse.query(`
      SELECT topicId, avg(sentimentScore) as avgSentiment
      FROM call_topic_sentiment
      WHERE tenantId = '${tenantId}' AND timestamp >= ${previousStart} AND timestamp < ${start}
      GROUP BY topicId
    `);

    const prevMap = new Map(previousTopics.map((t: any) => [t.topicId, t.avgSentiment]));

    for (const topic of topics) {
      const prev = prevMap.get(topic.topicId);
      if (prev == null) continue;

      const delta = topic.avgSentiment - prev;
      if (Math.abs(delta) < 0.15) continue;

      insights.push({
        id: generateId(),
        type: 'topic_shift',
        severity: Math.abs(delta) > 0.3 ? 'warning' : 'info',
        title: `Sentiment shift in "${topic.topicName}"`,
        description: `Sentiment for "${topic.topicName}" changed by ${delta > 0 ? '+' : ''}${delta.toFixed(2)} (from ${prev.toFixed(2)} to ${topic.avgSentiment.toFixed(2)}), mentioned in ${topic.mentions} interactions.`,
        metrics: { previousSentiment: prev, currentSentiment: topic.avgSentiment, delta },
        dimensionBreakdown: [{ label: topic.topicName, value: topic.avgSentiment, change: delta }],
      });
    }

    return insights;
  }

  private async detectAgentAlerts(
    tenantId: string,
    start: number,
    end: number
  ): Promise<SentimentInsight[]> {
    const agents = await this.clickhouse.query(`
      SELECT
        agentId, agentName,
        avg(customerSentiment) as avgSentiment,
        count() as callCount
      FROM call_sentiment_analysis
      WHERE tenantId = '${tenantId}' AND timestamp >= ${start} AND timestamp <= ${end}
      GROUP BY agentId, agentName
      HAVING count() >= 20
      ORDER BY avgSentiment ASC
      LIMIT 3
    `);

    return agents
      .filter((a: any) => a.avgSentiment < -0.1)
      .map((a: any) => ({
        id: generateId(),
        type: 'agent_alert' as const,
        severity: a.avgSentiment < -0.3 ? 'critical' as const : 'warning' as const,
        title: `Low customer sentiment for ${a.agentName}`,
        description: `${a.agentName} has an average customer sentiment of ${a.avgSentiment.toFixed(2)} across ${a.callCount} calls, below the team average.`,
        metrics: { agentSentiment: a.avgSentiment, callCount: a.callCount },
        recommendation: 'Review recent calls for this agent and consider coaching on customer engagement techniques.',
      }));
  }

  private async detectCampaignChanges(
    tenantId: string,
    start: number,
    end: number,
    previousStart: number
  ): Promise<SentimentInsight[]> {
    const campaigns = await this.clickhouse.query(`
      SELECT
        campaignId, campaignName,
        avg(customerSentiment) as avgSentiment,
        count() as callCount
      FROM call_sentiment_analysis
      WHERE tenantId = '${tenantId}' AND timestamp >= ${start} AND timestamp <= ${end}
      GROUP BY campaignId, campaignName
      HAVING count() >= 30
    `);

    const previousCampaigns = await this.clickhouse.query(`
      SELECT campaignId, avg(customerSentiment) as avgSentiment
      FROM call_sentiment_analysis
      WHERE tenantId = '${tenantId}' AND timestamp >= ${previousStart} AND timestamp < ${start}
      GROUP BY campaignId
    `);

    const prevMap = new Map(previousCampaigns.map((c: any) => [c.campaignId, c.avgSentiment]));
    const insights: SentimentInsight[] = [];

    for (const camp of campaigns) {
      const prev = prevMap.get(camp.campaignId);
      if (prev == null) continue;

      const delta = camp.avgSentiment - prev;
      if (Math.abs(delta) < 0.1) continue;

      insights.push({
        id: generateId(),
        type: 'campaign_performance',
        severity: delta < -0.2 ? 'warning' : 'info',
        title: `Campaign "${camp.campaignName}" sentiment ${delta > 0 ? 'improved' : 'declined'}`,
        description: `Sentiment changed by ${delta > 0 ? '+' : ''}${delta.toFixed(2)} (${camp.callCount} calls).`,
        metrics: { campaignSentiment: camp.avgSentiment, delta, callCount: camp.callCount },
      });
    }

    return insights;
  }

  private formatPeriod(start: number, end: number): string {
    const diffMs = end - start;
    const days = Math.round(diffMs / (24 * 3600 * 1000));
    if (days <= 1) return '24 hours';
    if (days <= 7) return `${days} days`;
    if (days <= 31) return `${Math.round(days / 7)} weeks`;
    return `${Math.round(days / 30)} months`;
  }
}

// Exported report structure
async function generateReport(config: SentimentReportConfig): Promise<Buffer> {
  const insights = await new InsightsGenerator().generateInsights(
    config.tenantId,
    new Date(config.timeRange.start!).getTime(),
    new Date(config.timeRange.end!).getTime()
  );

  switch (config.format) {
    case 'csv':
      return generateCsvExport(insights);
    case 'json':
      return Buffer.from(JSON.stringify(insights, null, 2));
    case 'pdf':
      return generatePdfReport(insights, config);
    case 'xlsx':
      return generateXlsxExport(insights);
    default:
      throw new Error(`Unsupported format: ${config.format}`);
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| BullMQ (MIT) | Server | Report scheduling |
| Puppeteer (Apache 2.0) | Server | PDF generation from HTML |
| ExcelJS (MIT) | Server | XLSX export generation |
| Nodemailer (MIT) | Server | Email delivery of reports |

## Production Considerations

**Scaling:** Report generation is CPU-intensive (PDF rendering, XLSX generation). Offload to a worker process via BullMQ to avoid blocking the web server. Set a maximum report size of 10 MB — larger reports may cause PDF generation to timeout. Queue concurrent report generation to at most 5 workers per server. Cache frequently requested reports (daily sentiment summary) with a 1-hour TTL.

**Security:** Report exports contain aggregate and individual sentiment data. Access requires the same permissions as viewing the data in the dashboard. Email reports must be sent only to verified email addresses within the tenant domain. Slack report delivery should use the authenticated user's Slack connection (OAuth), not a shared webhook. CSV/JSON exports of raw data (per-call sentiment) require explicit confirmation that the user understands this contains PII-adjacent data.

**Monitoring:** Track report generation time by format, report delivery success rate, and insight generation quality (user rating of "was this insight helpful?"). Alert if PDF generation success rate drops below 95%. Monitor BullMQ job queue depth — if it exceeds 50 pending jobs, add more worker processes.
