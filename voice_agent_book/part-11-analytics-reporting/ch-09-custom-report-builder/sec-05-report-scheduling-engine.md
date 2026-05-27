# Section 05: Report Scheduling Engine

## Overview

The report scheduling engine enables users to configure automated report delivery on recurring schedules. Users can schedule any saved report to be generated and delivered via email (PDF or CSV attachment), Slack (chart thumbnail with link), or webhook (JSON payload) on a daily, weekly, monthly, or custom cron schedule. The engine handles timezone-aware scheduling, delivery retry logic, and failure notifications.

When a scheduled report triggers, the engine loads the report definition, executes all data source queries, renders charts server-side using a headless browser (Puppeteer), composes the delivery payload according to the channel configuration, and sends it. The entire pipeline runs asynchronously with timeout management and concurrency limits. Scheduled reports also support parameter injection, allowing each delivery to include dynamic content like "This week's CSAT report for {{campaign}}" where the campaign is drawn from a rotating list.

## Architecture

```
                 Report Scheduling Engine

   User Configures → Schedule Store (PostgreSQL)
                          |
                   Cron Scheduler (node-cron / Bull)
                          |
                   ┌──────┴──────┐
                   ▼             ▼
              Due Report      Recurring
              Trigger         Schedule
                   |             |
                   ▼             ▼
              Report Executor
                   |
          ┌────────┼────────┐
          ▼        ▼        ▼
     Query      Render    Compose
     Runner     (PDF/     Delivery
                Image)    Payload
          |        |        |
          └────────┼────────┘
                   ▼
             Delivery Router
                   |
          ┌────────┼────────┐
          ▼        ▼        ▼
        Email    Slack    Webhook
```

## Design Decisions

- **Bull queue for execution management over in-process cron execution:** Scheduled report execution can take 30 seconds to 5 minutes per report (including rendering). Using Bull (Redis-backed job queue) allows executing reports in background worker processes, provides retry with exponential backoff, and handles concurrency limiting. If a worker crashes mid-render, the job is retried on a different worker. Trade-off: Bull requires Redis, adding infrastructure complexity, and job visibility into pending/active/completed states requires the Bull Board UI.

- **Server-side rendering with Puppeteer over client-side screenshot API:** Charts are rendered server-side using ECharts in a headless Chromium instance. This produces consistent, high-resolution output regardless of the viewer's browser, and avoids needing the report viewer to have a browser open for scheduled deliveries. Trade-off: Puppeteer is resource-heavy (50-100 MB per instance); a rendering pool of 2-4 instances with request queuing is needed to handle concurrent report generation.

- **Timezone-aware scheduling stored as cron expression + timezone over UTC-only scheduling:** Users select their timezone when creating a schedule. The schedule stores the cron expression and IANA timezone string. The scheduler evaluates the cron expression in the report's timezone to determine the next run time. This ensures that a "Monday 9 AM" report arrives at 9 AM in the recipient's timezone, not UTC. Trade-off: Daylight Saving Time transitions can cause a report to fire twice or skip once; the scheduler skips duplicate runs within 1 hour.

## Implementation Approach

```typescript
interface ReportSchedule {
  id: string;
  reportId: string;
  tenantId: string;
  name: string;
  description?: string;
  enabled: boolean;
  cronExpression: string; // standard 5-field cron
  timezone: string; // IANA timezone, e.g., "America/New_York"
  deliveryChannels: DeliveryChannelConfig[];
  params: Record<string, unknown>;
  startDate: number;
  endDate?: number;
  lastRunAt?: number;
  nextRunAt?: number;
  createdAt: number;
  updatedAt: number;
}

interface DeliveryChannelConfig {
  type: 'email' | 'slack' | 'webhook';
  enabled: boolean;
  config: EmailConfig | SlackConfig | WebhookConfig;
}

interface EmailConfig {
  recipients: string[];
  subjectTemplate: string;
  bodyTemplate: string;
  attachments: ('pdf' | 'csv' | 'png')[];
  replyTo?: string;
}

interface SlackConfig {
  channelIds: string[];
  messageTemplate: string;
  includeChartImage: boolean;
}

interface WebhookConfig {
  url: string;
  method: 'POST' | 'PUT';
  headers: Record<string, string>;
  payloadTemplate: string; // JSON template
  secret?: string; // HMAC secret
}

class ReportScheduler {
  private queue: Bull.Queue;
  private scheduleStore: ScheduleStore;

  async createSchedule(schedule: ReportSchedule): Promise<void> {
    await this.scheduleStore.save(schedule);
    await this.scheduleNextRun(schedule);
  }

  async updateSchedule(schedule: ReportSchedule): Promise<void> {
    // Cancel existing jobs and reschedule
    await this.cancelScheduledJob(schedule.id);
    await this.scheduleStore.update(schedule);
    await this.scheduleNextRun(schedule);
  }

  private async scheduleNextRun(schedule: ReportSchedule): Promise<void> {
    if (!schedule.enabled) return;

    const nextRun = this.computeNextRun(
      schedule.cronExpression,
      schedule.timezone,
      schedule.startDate,
      schedule.endDate
    );

    if (!nextRun) return;

    await this.scheduleStore.update(schedule.id, { nextRunAt: nextRun });

    // Schedule the Bull job at the computed time
    await this.queue.add(
      'execute_report',
      { scheduleId: schedule.id },
      {
        delay: nextRun - Date.now(),
        jobId: `${schedule.id}:${nextRun}`,
        attempts: 3,
        backoff: { type: 'exponential', delay: 60000 },
        removeOnComplete: true,
        removeOnFail: false, // Keep failed jobs for debugging
      }
    );
  }

  private computeNextRun(
    cronExpression: string,
    timezone: string,
    startDate: number,
    endDate?: number
  ): number | null {
    const cronParser = new CronParser();
    const now = Date.now();

    // Find the next cron match in the given timezone
    let next = cronParser.next(cronExpression, new Date(now), { tz: timezone });

    if (!next) return null;

    const nextTs = next.getTime();

    // Respect start/end date boundaries
    if (nextTs < startDate) return null;
    if (endDate && nextTs > endDate) return null;

    return nextTs;
  }

  async executeSchedule(scheduleId: string): Promise<void> {
    const schedule = await this.scheduleStore.get(scheduleId);
    if (!schedule || !schedule.enabled) return;

    const report = await this.loadReport(schedule.reportId);
    const params = this.interpolateParams(schedule.params);

    // 1. Execute queries
    const queryResults = await this.executeReportQueries(report);

    // 2. Render charts and tables
    const artifacts = await this.renderReport(report, queryResults, schedule.deliveryChannels);

    // 3. Deliver via each configured channel
    for (const channel of schedule.deliveryChannels) {
      if (!channel.enabled) continue;

      try {
        await this.deliver(channel, artifacts, params);
        await this.recordDelivery(schedule.id, channel.type, 'success');
      } catch (error) {
        await this.recordDelivery(schedule.id, channel.type, 'failed', error.message);
        // Channel-level failure doesn't fail the entire schedule
      }
    }

    // 4. Update schedule metadata
    await this.scheduleStore.update(schedule.id, {
      lastRunAt: Date.now(),
    });

    // 5. Schedule next run
    await this.scheduleNextRun(schedule);
  }

  private async renderReport(
    report: ReportDefinition,
    queryResults: Map<string, QueryResult>,
    channels: DeliveryChannelConfig[]
  ): Promise<ReportArtifacts> {
    const artifacts: ReportArtifacts = {};

    for (const channel of channels) {
      if (channel.type === 'email' && (channel.config as EmailConfig).attachments.includes('pdf')) {
        artifacts.pdf = await this.renderPDF(report, queryResults);
      }
      if (channel.type === 'slack' && (channel.config as SlackConfig).includeChartImage) {
        artifacts.chartImages = await this.renderChartImages(report, queryResults);
      }
    }

    return artifacts;
  }

  private async renderPDF(report: ReportDefinition, queryResults: Map<string, QueryResult>): Promise<Buffer> {
    const browser = await this.browserPool.acquire();
    try {
      const page = await browser.newPage();
      const html = this.generateReportHTML(report, queryResults);
      await page.setContent(html, { waitUntil: 'networkidle0', timeout: 30000 });
      const pdf = await page.pdf({ format: 'A4', printBackground: true });
      return Buffer.from(pdf);
    } finally {
      await this.browserPool.release(browser);
    }
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Bull (MIT) | Server | Redis-backed job queue for report execution |
| node-cron (ISC) | Server | Cron expression parsing and evaluation |
| Puppeteer (Apache 2.0) | Server | Headless browser for PDF/image rendering |
| Nodemailer (MIT) | Server | Email delivery via SMTP |

## Production Considerations

**Scaling:** Report execution workers scale horizontally behind Bull's Redis-backed queue. Each worker handles up to 2 concurrent report executions (Puppeteer memory constraint). If the queue backlog exceeds 100 jobs, new schedules are rejected with a "try again later" error. PDF rendering is the bottleneck — a pool of 4 Puppeteer instances handles approximately 200 PDF reports per hour. Reports with more than 15 charts are split into parallel rendering batches.

**Security:** Scheduled reports execute in a sandboxed worker process with access only to the report definition store and data source connectors (read-only). Email recipients are validated against the tenant's allowed domain list. Webhook payloads include an HMAC signature header for endpoint verification. Report parameters are sanitized to prevent template injection in subject/body templates.

**Monitoring:** Track schedule execution latency (time from trigger to delivery), success/failure rate per channel, PDF render time per report, queue depth, and Puppeteer pool utilization. Alert if execution success rate drops below 95%, if queue depth exceeds 50, if Puppeteer memory exceeds 500 MB per instance, or if any schedule has been failing for 3+ consecutive runs.
