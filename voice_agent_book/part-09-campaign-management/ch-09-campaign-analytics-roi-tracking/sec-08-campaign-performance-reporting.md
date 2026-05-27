# Section 08: Campaign Performance Reporting

## Overview

Campaign performance reporting transforms raw analytics data into actionable business intelligence through scheduled reports, automated delivery, and stakeholder-specific views. Reports cover campaign performance (KPIs, conversion rates, ROI), operational efficiency (agent utilization, cost metrics, abandonment rates), compliance status (DNC scrutiny, consent rates, calling window adherence), and trend analysis (performance over time, period-over-period comparisons, anomaly detection). Each stakeholder group has distinct reporting needs — executives need aggregate portfolio performance with ROI highlights, campaign managers need detailed campaign-level diagnostics, compliance officers need regulatory adherence reports, and agents need personal performance summaries.

The reporting system supports multiple delivery channels (email, Slack, in-app dashboard, PDF export, API access) and formats (interactive dashboards, static PDF summaries, CSV raw data exports, PowerPoint slide decks for executive presentations). Reports can be scheduled on recurring cadences (daily, weekly, monthly) or triggered by specific events (campaign completion, threshold breach, manual request). The system also supports ad-hoc report generation through a self-service interface where users select metrics, filters, date ranges, and visualization types.

## Architecture

```
                 Campaign Performance Reporting Architecture

   +------------------+  +------------------+  +------------------+
   | Data Sources     |  | Report Templates |  | Delivery Channels|
   | • ClickHouse     |  | • Executive      |  | • Email (SMTP)   |
   | • PostgreSQL     |  | • Campaign       |  | • Slack Webhook  |
   | • Redis (real-   |  | • Agent          |  | • Dashboard       |
   |   time metrics)  |  | • Compliance     |  | • API (REST)     |
   | • API (external) |  | • Custom         |  | • PDF Export     |
   +------------------+  +------------------+  +------------------+
           |                     |                      |
           v                     v                      v
   +------------------------------------------------------------+
   |                  Report Generation Engine                  |
   |                                                            |
   |  1. Schedule triggers report generation                    |
   |  2. Query data sources based on template configuration     |
   |  3. Apply formatting, charts, and conditional formatting   |
   |  4. Generate output in requested format(s)                 |
   |  5. Deliver via configured channels                        |
   |  6. Log delivery status and metric snapshots               |
   +------------------------------------------------------------+
           |                     |                      |
           v                     v                      v
   +------------------+  +------------------+  +------------------+
   | Report Storage   |  | Delivery Queue   |  | Audit Log        |
   | (Object Store)   |  | (BullMQ)         |  | (PostgreSQL)     |
   +------------------+  +------------------+  +------------------+
```

## Design Decisions

- **Template-driven report generation over ad-hoc query builder:** Pre-defined report templates ensure consistency and quality across all reports. Templates define data sources, metrics, visualizations, formatting rules, and delivery configurations. Users customize templates through parameter selection (date range, campaigns, filters) rather than building reports from scratch. Trade-off: template approach limits flexibility for completely custom reports, which are handled by the separate Custom Report Builder (Chapter 09).

- **Multi-format generation with format-specific optimization:** Reports are generated in multiple formats simultaneously (HTML email, PDF attachment, CSV data) from a single query execution. Each format has optimized templates — HTML for inline email viewing with interactive charts, PDF for professional stakeholder presentation, CSV for data analysis. Trade-off: generating multiple formats increases computational cost per report and requires maintaining format-specific templates.

- **Snapshot-based historical reporting with point-in-time accuracy:** Each scheduled report captures a snapshot of the metrics at the time of generation, preserving the exact state even if underlying data changes (retroactive corrections, late-arriving events). This ensures report consistency and auditability — last week's report remains accurate even if data was corrected this week. Trade-off: snapshots consume significant storage for high-frequency reports.

## Implementation Approach

```
interface ReportSchedule {
  id: string;
  templateId: string;
  name: string;
  frequency: 'daily' | 'weekly' | 'monthly' | 'custom';
  cronExpression?: string;
  parameters: {
    campaignIds?: string[];
    dateRange: { type: 'last_7_days' | 'last_30_days' | 'current_month' | 'custom'; customStart?: number; customEnd?: number };
    metrics: string[];
    filters: Record<string, any>;
  };
  formats: ('email_html' | 'pdf' | 'csv' | 'slack')[];
  delivery: {
    email?: { recipients: string[]; subject: string };
    slack?: { channels: string[]; webhookUrl: string };
  };
  enabled: boolean;
}

interface ReportGenerationResult {
  id: string;
  scheduleId: string;
  generatedAt: number;
  status: 'success' | 'partial' | 'failed';
  formats: { format: string; storageUrl: string; size: number }[];
  metrics: { metric: string; value: number; change: number }[];
  deliveryStatus: { channel: string; success: boolean; error?: string }[];
}

class ReportGenerationService {
  constructor(queue, dataService, templateEngine, deliveryService) {
    this.queue = queue;
    this.dataService = dataService;
    this.templateEngine = templateEngine;
    this.deliveryService = deliveryService;
  }

  async generateAndDeliver(scheduleId: string) {
    const schedule = await this.getSchedule(scheduleId);
    const snapshot = await this.dataService.queryMetrics(schedule.parameters);
    const generated = await this.generateFormats(schedule, snapshot);
    await this.storeReport(generated);
    await this.deliverReport(generated, schedule.delivery);
    return generated;
  }

  async scheduleReportGeneration(schedule: ReportSchedule) {
    const job = await this.queue.add('generate_report', {
      scheduleId: schedule.id,
      templateId: schedule.templateId,
      parameters: schedule.parameters
    }, {
      repeat: { cron: schedule.cronExpression },
      removeOnComplete: { age: 3600 * 24 * 7 }
    });
    return job.id;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **BullMQ** (MIT) | Queue | Report job scheduling |
| **Puppeteer** (Apache 2.0) | Rendering | PDF generation from HTML |
| **Handlebars** (MIT) | Templates | Email template engine |
| **Apache ECharts** (Apache 2.0) | Charts | Chart rendering for reports |
| **MinIO** (AGPLv3) | Storage | Report artifact storage |
| **Nodemailer** (MIT) | Email | Email delivery |

## Production Considerations

**Scaling:** Report generation is CPU and memory intensive (PDF rendering, chart generation, large data sorting). Use a dedicated BullMQ queue with controlled concurrency (max 5 concurrent report generations per worker) to prevent resource exhaustion. Scale workers horizontally based on queue depth. Store generated reports in object storage (S3/MinIO) with 90-day retention and automatic cleanup of old artifacts.

**Security:** Reports contain sensitive campaign, financial, and agent performance data. Implement report-level access control — recipients must be authorized for all data in the report. PDF reports should support optional password protection. Email delivery should use TLS. Log all report access and delivery events. Support data masking for PII in exported CSV files.

**Monitoring:** Track report generation duration, delivery success rate (target > 99%), report size trends, failed delivery reasons, and schedule adherence (was the report generated on time?). Alert on generation failures, delivery failures, and missed schedules. Provide a report generation dashboard showing current queue depth, recent completions, and failure rates.
