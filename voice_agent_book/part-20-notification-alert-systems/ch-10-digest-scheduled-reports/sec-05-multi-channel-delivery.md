# Section 05: Multi-Channel Delivery

## Overview

Digests are delivered across multiple channels based on user preferences — email, in-app notification, Slack, and SMS summary. Each channel has a tailored format optimized for the medium while maintaining consistent content.

## Architecture

```
Multi-Channel Delivery
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Digest Content] → [Channel Adapter] → [Channel-Specific Format] → [Send]
       │                    │                       │                   │
  Unified digest       EmailAdapter:             HTML email           SendGrid
  content with         SlackAdapter:            Slack blocks          Slack API
  modules and          InAppAdapter:            JSON payload          WebSocket
  items                SMSAdapter:              Truncated text        Twilio

Channel Format Differences:
  ┌──────────┬────────────────────────────────────────────────────┐
  │ Channel  │ Format                                              │
  ├──────────┼────────────────────────────────────────────────────┤
  │ Email    │ Full HTML with branding, clickable links, images    │
  │ In-App   │ Rich notification with deep links, collapsible      │
  │ Slack    │ Slack Block Kit with buttons, truncate to 50 items  │
  │ SMS      │ Single text message with critical alerts only       │
  └──────────┴────────────────────────────────────────────────────┘

Channel Delivery Matrix:
  User Preference → Deliver To
  ┌─────────────────────────────────────────────┐
  │ Full digest: Email + In-App                  │
  │ Summary: Slack channel                       │
  │ Critical only: SMS                           │
  │                                               │
  │ Example:                                      │
  │   08:00 ET → Email (full)                     │
  │   08:00 ET → In-App (full)                    │
  │   08:00 ET → Slack (summary)                  │
  │   On critical alert → SMS (immediate)         │
  └─────────────────────────────────────────────┘
```

## Design Decisions

- **Adapter Pattern**: Each channel implements a common adapter interface
- **Format Specificity**: Content trimmed/expanded per channel capabilities
- **Failover**: If primary channel fails, fallback to secondary
- **Channel Precedence**: Some content types only sent to specific channels

## Implementation Approach

```typescript
interface ChannelAdapter {
  channel: string;
  format(digest: Digest, preferences: DigestPreferences): Promise<ChannelPayload>;
  send(payload: ChannelPayload): Promise<ChannelResult>;
}

interface ChannelPayload {
  channel: string;
  userId: string;
  content: Record<string, unknown>;
  metadata: {
    digestId: string;
    template: string;
    priority: 'normal' | 'high';
  };
}

interface ChannelResult {
  success: boolean;
  messageId?: string;
  error?: string;
}

class EmailAdapter implements ChannelAdapter {
  channel = 'email';

  async format(digest: Digest, preferences: DigestPreferences): Promise<ChannelPayload> {
    const html = await this.renderTemplate(digest, 'email');
    const text = this.stripHtml(html);

    return {
      channel: 'email',
      userId: digest.userId,
      content: {
        subject: `Your Digest — ${this.formatDate(digest.generatedAt)}`,
        html,
        text,
        unsubscribeLink: await this.getUnsubscribeLink(digest.userId),
      },
      metadata: { digestId: digest.id, template: 'email-default', priority: 'normal' },
    };
  }

  async send(payload: ChannelPayload): Promise<ChannelResult> {
    // Use SendGrid or SES
    try {
      const messageId = await emailClient.send({
        to: payload.userId,
        subject: payload.content.subject,
        html: payload.content.html,
        text: payload.content.text,
        headers: {
          'List-Unsubscribe': `<${payload.content.unsubscribeLink}>`,
          'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click',
        },
      });
      return { success: true, messageId };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  private async renderTemplate(digest: Digest, template: string): Promise<string> {
    // Use Handlebars or MJML for email rendering
    return `
      <!DOCTYPE html>
      <html>
      <head><meta charset="utf-8"></head>
      <body style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
        <header style="background: #f8f9fa; padding: 20px; border-bottom: 2px solid #dee2e6;">
          <h1>Your Voice Agent Digest</h1>
          <p>${this.formatDate(digest.generatedAt)}</p>
        </header>
        ${digest.modules.map(m => this.renderModule(m)).join('')}
        <footer style="padding: 20px; color: #6c757d; font-size: 12px;">
          <p><a href="${this.getUnsubscribeLink(digest.userId)}">Unsubscribe</a></p>
          <p>© Voice Agent</p>
        </footer>
      </body>
      </html>
    `;
  }

  private renderModule(module: DigestModuleContent): string {
    const colorMap = { critical: '#dc3545', warning: '#ffc107', info: '#0d6efd' };
    return `
      <div style="margin: 20px 0; padding: 15px; border-left: 4px solid ${colorMap[module.priority]};">
        <h2 style="margin-top: 0;">${module.title}</h2>
        ${module.items.map(item => `
          <div style="padding: 8px 0; border-bottom: 1px solid #eee;">
            <a href="${item.link || '#'}" style="color: #0d6efd;">${item.title}</a>
            ${item.description ? `<p style="margin: 4px 0; color: #6c757d;">${item.description}</p>` : ''}
            <small style="color: #adb5bd;">${this.formatTime(item.timestamp)}</small>
          </div>
        `).join('')}
      </div>
    `;
  }
}

class SlackAdapter implements ChannelAdapter {
  channel = 'slack';

  async format(digest: Digest, preferences: DigestPreferences): Promise<ChannelPayload> {
    const blocks: any[] = [
      {
        type: 'header',
        text: { type: 'plain_text', text: `📬 Your Digest — ${this.formatDate(digest.generatedAt)}` },
      },
      { type: 'divider' },
    ];

    for (const module of digest.modules.slice(0, 2)) { // Max 2 modules for Slack
      const emojiMap = { critical: '🔴', warning: '🟡', info: 'ℹ️' };
      blocks.push({
        type: 'section',
        text: { type: 'mrkdwn', text: `*${emojiMap[module.priority]} ${module.title}*` },
      });

      const items = module.items.slice(0, 10).map(item =>
        `${item.link ? `<${item.link}|${item.title}>` : item.title}`
      );

      blocks.push({
        type: 'section',
        text: { type: 'mrkdwn', text: items.join('\n') },
      });
    }

    blocks.push(
      { type: 'divider' },
      {
        type: 'context',
        elements: [
          { type: 'mrkdwn', text: `<${this.getPreferencesLink(digest.userId)}|Manage preferences>` },
        ],
      },
    );

    return {
      channel: 'slack',
      userId: digest.userId,
      content: { blocks, text: `Your digest for ${this.formatDate(digest.generatedAt)}` },
      metadata: { digestId: digest.id, template: 'slack-blocks', priority: 'normal' },
    };
  }

  async send(payload: ChannelPayload): Promise<ChannelResult> {
    try {
      const result = await slackClient.chat.postMessage({
        channel: payload.userId,
        blocks: payload.content.blocks,
        text: payload.content.text,
      });
      return { success: true, messageId: result.ts };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
}

class SMSAdapter implements ChannelAdapter {
  channel = 'sms';

  async format(digest: Digest, preferences: DigestPreferences): Promise<ChannelPayload> {
    // SMS only includes critical items
    const criticalItems = digest.modules
      .flatMap(m => m.items)
      .filter(i => i.severity === 'critical')
      .slice(0, 3);

    const text = criticalItems.length > 0
      ? `🔴 ${criticalItems.length} critical: ${criticalItems.map(i => i.title).join(' | ')}`
      : '✅ No critical alerts in your latest digest';

    return {
      channel: 'sms',
      userId: digest.userId,
      content: { body: text },
      metadata: { digestId: digest.id, template: 'sms-critical', priority: 'high' },
    };
  }

  async send(payload: ChannelPayload): Promise<ChannelResult> {
    try {
      const result = await twilioClient.messages.create({
        body: payload.content.body,
        to: payload.userId,
      });
      return { success: true, messageId: result.sid };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
}

// Multi-channel delivery orchestrator
class MultiChannelDeliverer {
  private adapters: ChannelAdapter[] = [
    new EmailAdapter(),
    new SlackAdapter(),
    new SMSAdapter(),
    new InAppAdapter(),
  ];

  async deliver(digest: Digest, preferences: DigestPreferences): Promise<void> {
    const channels = preferences.channelPreferences.filter(c => c.enabled);

    const results = await Promise.allSettled(
      channels.map(async channelPref => {
        const adapter = this.adapters.find(a => a.channel === channelPref.channel);
        if (!adapter) throw new Error(`No adapter for channel ${channelPref.channel}`);

        const payload = await adapter.format(digest, preferences);
        const result = await adapter.send(payload);

        if (!result.success) {
          // Attempt fallback
          await this.fallback(channelPref.channel, digest, preferences);
        }

        return result;
      })
    );

    // Log delivery results
    for (const result of results) {
      if (result.status === 'rejected') {
        console.error(`Digest delivery failed:`, result.reason);
      }
    }
  }

  private async fallback(
    failedChannel: string,
    digest: Digest,
    preferences: DigestPreferences,
  ): Promise<void> {
    // Fallback to in-app notification if email fails
    if (failedChannel === 'email') {
      const inApp = this.adapters.find(a => a.channel === 'in_app');
      if (inApp) {
        const payload = await inApp.format(digest, preferences);
        await inApp.send(payload);
      }
    }
  }
}
```

## Integration Points

- **SendGrid**: Email delivery
- **Slack API**: Slack Block Kit messages
- **Twilio**: SMS delivery for critical alerts
- **WebSocket Server**: In-app notification delivery

## Production Considerations

- **Channel Reliability**: Retry failed channel delivery once before fallback
- **Rate Limits**: Respect Slack rate limits (1 message per second per conversation)
- **SMS Costs**: Limit SMS to critical alerts only
- **Email Rendering**: Test across email clients (Outlook, Gmail, Apple Mail)

## Open-Source Tools

- **Handlebars**: Email template rendering
- **MJML**: Responsive email framework
- **Slack Block Kit Builder**: Slack message design
