# Section 05: Slack Report Integration

## Overview

Slack integration delivers report exports and summaries directly to Slack channels. Users can configure reports to be posted as messages (with key metrics inline) or as file uploads. The integration supports private channels, direct messages, and public channels via Slack app installation.

```
Slack Integration Architecture
┌─────────────────────────────────────────────────────────────────────────┐
│ Our Platform                    Slack                                  │
│ ┌──────────────────────┐      ┌────────────────────────────────────┐  │
│ │ Slack OAuth Flow     │─────▶│ App Manifest Installation          │  │
│ │ • Bot token scope    │      │ • chat:write                       │  │
│ │ • Channel scope      │      │ • files:write                      │  │
│ │ • User token         │      │ • channels:read                    │  │
│ └──────────────────────┘      └────────────────────────────────────┘  │
│                          │                                             │
│ ┌──────────────────────┐ │      ┌────────────────────────────────────┐  │
│ │ Schedule Trigger     │─┤─────▶│ Post message + file               │  │
│ │ BullMQ cron job      │ │      │ to: #reports channel              │  │
│ │ Export CSV/PDF/JSON  │ │      │ format: Slack Block Kit           │  │
│ └──────────────────────┘ │      └────────────────────────────────────┘  │
│                          │                                             │
│ ┌──────────────────────┐ │      ┌────────────────────────────────────┐  │
│ │ Slash command handler│─┘─────▶│ /report [name] [period]           │  │
│ │ • /report            │        │ Response: ephemeral message       │  │
│ │ • /report-schedule   │        │ with generated report             │  │
│ │ • /report-list       │        │                                    │  │
│ └──────────────────────┘        └────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

## Slack App Setup

The Slack app requires the following OAuth scopes:
- `chat:write` — Post messages to channels
- `chat:write.public` — Post to public channels without joining
- `files:write` — Upload file attachments
- `channels:read` — List public channels
- `groups:read` — List private channels
- `commands` — Register slash commands
- `incoming-webhook` — Incoming webhooks

## Message Delivery

```typescript
interface SlackReportConfig {
  channel: string; // #channel-name or DM user ID
  messageType: 'summary' | 'full' | 'attachment_only';
  
  summaryFormat: {
    includeKPIs: boolean;
    includeTrend: boolean;
    includeTopAgents: boolean;
    includeComparison: boolean; // vs previous period
  };
  
  attachmentFormat: 'csv' | 'json' | 'pdf';
  attachmentName: string;
  
  schedule: {
    frequency: 'daily' | 'weekly' | 'monthly' | 'custom';
    cron: string;
    timezone: string;
    timeOfDay: string;
    dayOfWeek?: number;
    dayOfMonth?: number;
  };
}

class SlackReportDeliverer {
  private slackClient: WebClient;
  private reportService: ReportService;
  
  async deliverReport(
    reportId: string,
    tenantId: string,
    config: SlackReportConfig
  ): Promise<DeliveryResult> {
    // Generate the report data
    const reportData = await this.reportService.getReportData(reportId, {
      dateRange: this.resolveDateRange(config.schedule),
    });
    
    // Build Slack message
    const blocks: Block[] = [];
    
    if (config.messageType === 'summary' || config.messageType === 'full') {
      blocks.push({
        type: 'header',
        text: { type: 'plain_text', text: `📊 ${reportData.name}`, emoji: true },
      });
      
      blocks.push({
        type: 'context',
        elements: [{
          type: 'mrkdwn',
          text: `*Period:* ${reportData.dateRange} | *Generated:* ${new Date().toLocaleString()}`,
        }],
      });
      
      blocks.push({ type: 'divider' });
      
      if (config.summaryFormat.includeKPIs) {
        const kpiFields = reportData.kpis.map(kpi => ({
          type: 'mrkdwn',
          text: `*${kpi.label}:* ${kpi.formattedValue} ${kpi.change ? `(${kpi.change > 0 ? '📈' : '📉'} ${kpi.change}%)` : ''}`,
        }));
        
        // Group KPI fields in sections of 2
        for (let i = 0; i < kpiFields.length; i += 2) {
          blocks.push({
            type: 'section',
            fields: kpiFields.slice(i, i + 2),
          });
        }
      }
      
      if (config.summaryFormat.includeTrend && reportData.trendChart) {
        // Upload chart as image and reference in message
        const chartUpload = await this.uploadChartImage(reportData.trendChart);
        blocks.push({
          type: 'image',
          image_url: chartUpload.permalink,
          alt_text: 'Trend chart',
        });
      }
      
      if (config.summaryFormat.includeTopAgents) {
        const agentText = reportData.topAgents
          .map((a, i) => `${i + 1}. *${a.name}* — ${a.calls} calls, ${a.csat}/5 CSAT`)
          .join('\n');
        
        blocks.push({
          type: 'section',
          text: { type: 'mrkdwn', text: `*🏆 Top Agents*\n${agentText}` },
        });
      }
      
      if (config.summaryFormat.includeComparison) {
        blocks.push({
          type: 'section',
          text: {
            type: 'mrkdwn',
            text: `*📈 Period Comparison*\n• Calls: ${reportData.comparison.calls}% ${reportData.comparison.calls > 0 ? '↑' : '↓'}\n• Duration: ${reportData.comparison.duration}%\n• CSAT: ${reportData.comparison.csat} pts`,
          },
        });
      }
    }
    
    // Add CTA button
    blocks.push({
      type: 'actions',
      elements: [{
        type: 'button',
        text: { type: 'plain_text', text: '🔍 View Full Report', emoji: true },
        url: `${BASE_URL}/reports/${reportId}`,
        action_id: 'view_report',
      }],
    });
    
    // Post message
    const messageResult = await this.slackClient.chat.postMessage({
      channel: config.channel,
      text: `${reportData.name} — ${reportData.dateRange}`,
      blocks,
      unfurl_links: false,
    });
    
    // Upload attachment if needed
    let fileResult = null;
    if (config.messageType !== 'summary' || config.messageType === 'attachment_only') {
      const exportBuffer = await this.generateExport(reportId, config.attachmentFormat);
      
      fileResult = await this.slackClient.files.upload({
        channels: config.channel,
        filename: `${config.attachmentName || reportData.name}.${config.attachmentFormat}`,
        file: exportBuffer,
        title: reportData.name,
        initial_comment: 'Full report attached 📎',
      });
    }
    
    return {
      success: true,
      messageTs: messageResult.ts,
      fileId: fileResult?.file?.id,
    };
  }
}
```

## Slash Commands

| Command | Description | Response |
|---------|-------------|----------|
| `/report [name] [period]` | Generate and post a report | Ephemeral message with report |
| `/report-schedule` | Open schedule configuration modal | Modal with schedule form |
| `/report-list` | List all scheduled reports | Ephemeral message with list |
| `/report-help` | Show available commands | Ephemeral message with help |

### Slash Command Handler

```typescript
class SlackCommandHandler {
  async handleCommand(command: SlashCommand): Promise<SlackCommandResponse> {
    switch (command.command) {
      case '/report': {
        const [reportName, period] = command.text.split(' ').filter(Boolean);
        
        const report = await this.findReport(command.team_id, reportName);
        if (!report) {
          return {
            response_type: 'ephemeral',
            text: `Report "${reportName}" not found. Available reports: ${await this.listReports(command.team_id)}`,
          };
        }
        
        const dateRange = period ? this.parsePeriod(period) : 'last7days';
        const reportData = await this.reportService.getReportData(report.id, { dateRange });
        
        return {
          response_type: 'in_channel',
          blocks: this.buildSummaryBlocks(reportData),
        };
      }
      
      case '/report-schedule': {
        // Open a modal for schedule configuration
        return {
          response_type: 'ephemeral',
          text: 'Opening schedule configuration...',
          trigger_id: command.trigger_id,
        };
      }
      
      case '/report-list': {
        const schedules = await this.scheduleStore.listByTeam(command.team_id);
        const scheduleList = schedules.map(s =>
          `• *${s.name}* — ${s.frequency}, next: ${new Date(s.nextRun).toLocaleString()}`
        ).join('\n');
        
        return {
          response_type: 'ephemeral',
          text: scheduleList || 'No scheduled reports. Use `/report-schedule` to create one.',
        };
      }
    }
  }
}
```

## Configuration UI (Block Kit Modal)

The Slack schedule configuration is presented as a Block Kit modal:
- Channel selector (multi-select, max 5)
- Report selector (dropdown of available reports)
- Message type (summary, full, attachment only)
- Summary options (checkboxes for KPIs, trends, agents, comparison)
- Schedule (daily, weekly, monthly with time selector)
- Timezone selector

## Open Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| @slack/web-api (MIT) | Client | Slack API client |
| @slack/bolt (MIT) | Framework | Slack app framework |
| @slack/interactive-messages (MIT) | Messages | Block Kit builder |
| node-slack-sdk (MIT) | SDK | Slack integration |

## Production Considerations

**Rate limits:** Slack API rate limits: 1 message per second per channel, 50 messages per minute per workspace. For high-frequency reports, batch deliveries with a 1-second delay between channels. Use Slack's `chat.postMessage` with `as_user: false` (bot token) to avoid user rate limits.

**Error handling:** If the Slack workspace is unreachable, retry with exponential backoff (30s → 2m → 10m → 1h). If the bot is removed from a channel, disable the schedule and notify the creator via in-app notification. Slack API errors (token revoked, scope missing, channel not found) are logged and the schedule is paused.

**Security:** Store Slack tokens encrypted at rest. Support Slack's granular permissions (bot token scopes only). Allow admins to restrict which channels reports can be posted to. Audit all Slack actions with user ID, timestamp, and channel.
