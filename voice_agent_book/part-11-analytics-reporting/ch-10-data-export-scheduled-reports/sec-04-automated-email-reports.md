# Section 04: Automated Email Reports

## Overview

Automated email reports deliver exports directly to inboxes on a recurring schedule. Users configure recipients, subject, body, attachment format, and schedule (daily, weekly, monthly, or custom cron). The system handles delivery, tracking, and bounce management.

```
Email Report Pipeline
┌─────────────────────────────────────────────────────────────────────────┐
│ Schedule Trigger (Cron)       Generate Report       Deliver via Email │
│ ┌──────────────────────┐    ┌──────────────────┐   ┌───────────────┐  │
│ │ BullMQ Scheduler     │    │ Export Worker     │   │ SendGrid API  │  │
│ │ checks every minute  │───▶│ generates CSV/    │──▶│ or SMTP       │  │
│ │ for due schedules    │    │ JSON/PDF          │   │ server        │  │
│ └──────────────────────┘    │ uploads to S3     │   └───────────────┘  │
│                             └──────────────────┘                      │
│ Schedule DB (Postgres)      File Store (S3)       Email Logs (DB)     │
│ ┌──────────────────────┐    ┌──────────────────┐   ┌───────────────┐  │
│ │ schedule_id          │    │ export-tenant-   │   │ email_id      │  │
│ │ report_id            │    │ id/file.pdf      │   │ to, from, sub │  │
│ │ cron: '0 8 * * 1'    │    │ signed URL (7d)  │   │ status: sent  │  │
│ │ enabled: true        │    └──────────────────┘   │ opened: true  │  │
│ └──────────────────────┘                           └───────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

## Schedule Configuration

```typescript
interface EmailReportConfig {
  recipients: string[];
  cc: string[];
  bcc: string[];
  
  subject: string; // supports template vars: {{reportName}}, {{date}}, {{tenant}}
  bodyText: string;
  bodyHtml?: string; // optional HTML body
  
  attachmentFormat: 'csv' | 'json' | 'pdf';
  attachmentName: string; // supports template vars
  
  schedule: {
    frequency: 'daily' | 'weekly' | 'monthly' | 'custom';
    cron: string;
    timezone: string;
    timeOfDay: string; // HH:mm (for daily/weekly/monthly)
    dayOfWeek?: number; // 0=Sun, 1=Mon... (for weekly)
    dayOfMonth?: number; // 1-31 (for monthly)
    startDate: string;
    endDate?: string; // optional expiration
  };
  
  options: {
    includeCSV: boolean;
    includeJSON: boolean;
    includePDF: boolean;
    inlineData?: boolean; // embed key metrics in email body
    attachScreenshot?: boolean;
    password?: string; // PDF password
  };
  
  filters: {
    dateRange: 'today' | 'yesterday' | 'last7days' | 'last30days' | 'thisMonth' | 'lastMonth' | 'custom';
    customDateRange?: { start: string; end: string };
    additionalFilters: Record<string, any>;
  };
}
```

## Scheduler Implementation

```typescript
class EmailReportScheduler {
  private cronParser: CronParser;
  private jobQueue: Queue;
  private emailService: EmailService;
  
  async createSchedule(
    userId: string,
    tenantId: string,
    reportId: string,
    config: EmailReportConfig
  ): Promise<ExportSchedule> {
    // Validate cron expression
    if (config.schedule.frequency === 'custom') {
      if (!this.cronParser.validate(config.schedule.cron)) {
        throw new Error('Invalid cron expression');
      }
    }
    
    // Generate cron from frequency + time
    const cron = this.generateCron(config.schedule);
    
    const schedule: ExportSchedule = {
      id: generateId(),
      reportId,
      tenantId,
      name: `${config.subject} (${config.schedule.frequency})`,
      enabled: true,
      format: config.attachmentFormat,
      channel: 'email',
      cron,
      timezone: config.schedule.timezone,
      config: {
        dateRange: config.filters.dateRange === 'custom'
          ? { type: 'custom', start: config.filters.customDateRange!.start, end: config.filters.customDateRange!.end }
          : { type: config.filters.dateRange },
        filters: config.filters.additionalFilters,
        columns: [],
        rowLimit: 0,
        includeHeader: true,
        templateId: config.attachmentFormat === 'pdf' ? 'email-report' : undefined,
      },
      delivery: {
        email: {
          to: config.recipients,
          subject: config.subject,
          body: config.bodyText,
        },
      },
      lastRun: null,
      lastStatus: null,
      nextRun: this.calculateNextRun(cron, config.schedule.timezone),
      runCount: 0,
      createdBy: userId,
      createdAt: Date.now(),
      updatedAt: Date.now(),
    };
    
    await this.scheduleStore.create(schedule);
    
    // Register with cron scheduler
    await this.registerCronJob(schedule);
    
    return schedule;
  }
  
  async executeSchedule(scheduleId: string): Promise<void> {
    const schedule = await this.scheduleStore.get(scheduleId);
    if (!schedule || !schedule.enabled) return;
    
    // Update last run
    await this.scheduleStore.update(scheduleId, {
      lastRun: Date.now(),
      lastStatus: 'queued',
    });
    
    // Create export job
    const jobResult = await this.exportOrchestrator.createExportJob(
      schedule.reportId,
      schedule.tenantId,
      {
        format: schedule.format,
        channel: 'email',
        config: schedule.config,
        delivery: schedule.delivery,
      }
    );
    
    // Wait for export completion
    const exportJob = await this.waitForJob(jobResult.jobId);
    
    if (exportJob.status === 'completed') {
      // Send email with attachment
      await this.emailService.sendWithAttachment({
        to: schedule.delivery.email!.to,
        subject: this.renderTemplate(schedule.delivery.email!.subject, schedule),
        body: this.renderTemplate(schedule.delivery.email!.body, schedule),
        attachment: {
          url: exportJob.result.downloadUrl,
          filename: `${schedule.reportId}.${schedule.format}`,
          mimeType: this.getMimeType(schedule.format),
        },
      });
      
      await this.scheduleStore.update(scheduleId, {
        lastStatus: 'completed',
        runCount: schedule.runCount + 1,
        nextRun: this.calculateNextRun(schedule.cron, schedule.timezone),
      });
    } else {
      // Send failure notification to creator
      await this.sendFailureNotification(schedule, exportJob.error);
      
      await this.scheduleStore.update(scheduleId, {
        lastStatus: 'failed',
        nextRun: this.calculateNextRun(schedule.cron, schedule.timezone),
      });
    }
  }
  
  private generateCron(schedule: EmailReportConfig['schedule']): string {
    const [hour, minute] = schedule.timeOfDay.split(':').map(Number);
    
    switch (schedule.frequency) {
      case 'daily':
        return `${minute} ${hour} * * *`;
      case 'weekly':
        return `${minute} ${hour} * * ${schedule.dayOfWeek || 1}`;
      case 'monthly':
        return `${minute} ${hour} ${schedule.dayOfMonth || 1} * *`;
      case 'custom':
        return schedule.cron;
    }
  }
  
  private calculateNextRun(cron: string, timezone: string): number {
    // Use cron-parser to get next scheduled time
    const interval = this.cronParser.parse(cron);
    return interval.next().toMillis();
  }
}
```

## Email Templates

### Daily Summary Email
```
Subject: 📊 {{reportName}} — {{date}}
To: {{recipients}}

Hi there,

Here's your daily {{reportName}} for {{date}}.

Key Metrics:
• Total Calls: {{metrics.totalCalls}} ({{metrics.change}}% vs yesterday)
• Avg Handle Time: {{metrics.avgHandleTime}}
• Success Rate: {{metrics.successRate}}%
• CSAT: {{metrics.csat}}/5

[View in Dashboard]({{dashboardUrl}})

{{reportName}} report is attached.

—
{{tenantName}} • Powered by Voice AI Platform
```

### Weekly Digest Email
```
Subject: 📈 Weekly Analytics Digest — {{weekRange}}
To: {{recipients}}

Your weekly analytics are ready.

Top Highlights:
• {{metrics.totalCalls}} calls handled ({{metrics.weeklyChange}}% WoW)
• Top agent: {{metrics.topAgent}} ({{metrics.topAgentScore}}% CSAT)
• Busiest day: {{metrics.busiestDay}}
• Most common intent: {{metrics.topIntent}}

Download full report attached.

—
{{tenantName}} • Powered by Voice AI Platform
```

## Delivery Tracking

| Metric | Tracked Via | Display |
|--------|-------------|---------|
| Sent | SendGrid event webhook | ✓ status per recipient |
| Opened | Tracking pixel in HTML | % open rate |
| Clicked | Link tracking | % click rate |
| Bounced | SMTP bounce code | Bounce reason |
| Spam | Feedback loop | Spam report count |
| Failed | Delivery error | Error message |

## Open Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| BullMQ (MIT) | Queue | Cron schedule management |
| cron-parser (MIT) | Parse | Cron expression parsing |
| node-cron (MIT) | Scheduler | In-process cron (dev only) |
| Handlebars (MIT) | Template | Email template rendering |
| Nodemailer (MIT) | SMTP | SMTP email delivery (dev) |

## Production Considerations

**Deliverability:** Use a dedicated email sending service (SendGrid, AWS SES, Mailgun) with SPF, DKIM, and DMARC configured. Warm up dedicated IP addresses for high-volume senders (>10K/month). Monitor bounce rate (<2%) and spam complaint rate (<0.1%).

**Rate limiting:** Max 100 recipients per email, 10 attachments per email (each <25MB total). Max 50 scheduled email reports per tenant. Rate limit: 10 emails/minute per tenant, 500/hour per IP.

**Retention:** Delivery logs retained for 90 days. Bounced addresses are automatically suppressed after 3 consecutive bounces. Users are notified via in-app notification when a scheduled report fails delivery.
