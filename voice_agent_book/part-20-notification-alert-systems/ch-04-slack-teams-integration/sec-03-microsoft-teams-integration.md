# Section 03: Microsoft Teams Integration

## Overview

The Microsoft Teams integration enables notification delivery through Teams channels and bots. It uses Teams app manifests, Adaptive Cards for interactive messages, the Bot Framework for conversational interactions, and webhook connectors for simple message posting.

## Implementation Approach

```typescript
interface TeamsConfig {
  appId: string;
  appPassword: string;
  tenantId: string;
  botEndpoint: string;
}

class TeamsIntegrationService {
  private bot: BotBuilder;
  private connector: TeamsConnectorClient;

  constructor(config: TeamsConfig) {
    this.bot = new BotBuilder(config);
    this.connector = new TeamsConnectorClient(config);
  }

  async sendAdaptiveCard(teamId: string, channelId: string, card: AdaptiveCard): Promise<void> {
    const conversation = await this.connector.conversations.createConversation({
      activity: {
        type: 'message',
        channelData: { team: { id: teamId }, channel: { id: channelId } },
        attachments: [{
          contentType: 'application/vnd.microsoft.card.adaptive',
          content: card,
        }],
      },
    });
  }

  async sendViaWebhook(webhookUrl: string, payload: TeamsWebhookPayload): Promise<void> {
    await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        '@type': 'MessageCard',
        '@context': 'http://schema.org/extensions',
        themeColor: payload.color,
        title: payload.title,
        text: payload.text,
        sections: payload.sections,
        potentialAction: payload.actions,
      }),
    });
  }

  buildAlertAdaptiveCard(alert: Alert): AdaptiveCard {
    return {
      $schema: 'http://adaptivecards.io/schemas/adaptive-card.json',
      type: 'AdaptiveCard',
      version: '1.4',
      body: [
        {
          type: 'TextBlock',
          size: 'Large',
          weight: 'Bolder',
          text: alert.title,
          color: this.getColor(alert.severity),
        },
        {
          type: 'TextBlock',
          text: alert.message,
          wrap: true,
        },
        {
          type: 'FactSet',
          facts: [
            { title: 'Severity', value: alert.severity },
            { title: 'Source', value: alert.metadata.source },
            { title: 'Time', value: new Date(alert.createdAt).toLocaleString() },
          ],
        },
      ],
      actions: [
        {
          type: 'Action.Submit',
          title: 'Acknowledge',
          data: { action: 'acknowledge', alertId: alert.id },
        },
        {
          type: 'Action.OpenUrl',
          title: 'View Details',
          url: `${this.baseUrl}/alerts/${alert.id}`,
        },
      ],
    };
  }

  private getColor(severity: string): string {
    switch (severity) {
      case 'critical': return 'attention';
      case 'major': return 'warning';
      case 'minor': return 'accent';
      default: return 'default';
    }
  }

  async registerMessagingExtension(): Promise<void> {
    // Register bot commands
    await this.bot.registerCommands([
      { id: 'subscribe', title: 'Subscribe to notifications', description: 'Subscribe to alert notifications' },
      { id: 'unsubscribe', title: 'Unsubscribe from notifications', description: 'Stop receiving alerts' },
      { id: 'status', title: 'System status', description: 'Check current system status' },
    ]);
  }
}
```

## Integration Points

- **Bot Framework**: Bot communicates with Teams via Bot Framework protocol
- **Connector API**: Send messages directly to Teams channels
- **Webhook Connectors**: Simple message posting without bot registration

## Production Considerations

- **App Registration**: Teams app must be registered in Azure Portal
- **Bot Channels Registration**: Bot registered with Azure Bot Service
- **Adaptive Card Versioning**: Different Teams versions support different card versions
