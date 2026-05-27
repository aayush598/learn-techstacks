# Section 01: Slack API Integration Architecture

## Overview

The Slack integration connects the notification system to Slack workspaces. It uses Bolt framework for event handling, OAuth for workspace authentication, and Slack API methods for message posting. The architecture supports multiple Slack workspaces, channel subscriptions, and interactive messages.

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Slack App   │     │  Integration  │     │  Your App    │
│              │     │  Service      │     │              │
│  Slash Cmd   │────▶│  Bolt Router  │────▶│  Handlers    │
│  Events API  │────▶│  OAuth Flow   │────▶│  Logic       │
│  Interactv   │────▶│  Web API      │────▶│  Notify Svc  │
│              │     │  Socket Mode  │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
```

## Implementation Approach

```typescript
import { App, ExpressReceiver } from '@slack/bolt';

class SlackIntegrationService {
  private app: App;
  private workspaceTokens: Map<string, string> = new Map();

  constructor(signingSecret: string, clientId: string, clientSecret: string) {
    const receiver = new ExpressReceiver({ signingSecret });

    this.app = new App({
      receiver,
      clientId,
      clientSecret,
      stateSecret: crypto.randomBytes(32).toString('hex'),
      scopes: ['chat:write', 'channels:read', 'commands', 'reactions:read'],
      installerOptions: {
        stateVerification: true,
        directInstall: true,
      },
    });

    this.registerEventHandlers();
  }

  private registerEventHandlers(): void {
    this.app.event('app_mention', async ({ event, say }) => {
      await say(`Hello <@${event.user}>! How can I help?`);
    });

    this.app.command('/notify', async ({ command, ack, respond }) => {
      await ack();
      await respond({
        text: `Processing notification request...`,
        response_type: 'in_channel',
      });
      // Forward to notification service
    });

    this.app.action('acknowledge_alert', async ({ body, ack, respond }) => {
      await ack();
      await respond({
        text: `Alert acknowledged by <@${body.user.id}>`,
        replace_original: true,
      });
    });
  }

  async sendMessage(workspaceId: string, channelId: string, message: SlackMessage): Promise<void> {
    const token = this.workspaceTokens.get(workspaceId);
    if (!token) throw new Error('Workspace not installed');

    await this.app.client.chat.postMessage({
      token,
      channel: channelId,
      text: message.text,
      blocks: message.blocks,
      attachments: message.attachments,
    });
  }

  async getChannels(workspaceId: string): Promise<ChannelInfo[]> {
    const token = this.workspaceTokens.get(workspaceId);
    const result = await this.app.client.conversations.list({ token, limit: 200 });
    return result.channels?.map(c => ({
      id: c.id!,
      name: c.name!,
      isPrivate: c.is_private || false,
    })) || [];
  }

  getReceiver(): ExpressReceiver {
    return this.app.receiver as ExpressReceiver;
  }
}
```

## Integration Points

- **OAuth Flow**: User installs Slack app to workspace
- **Event Subscriptions**: Listen for Slack events
- **Web API**: Send messages, manage channels

## Production Considerations

- **Rate Limits**: Respect Slack API rate limits (1 message per second per channel)
- **Token Storage**: Encrypt and securely store workspace tokens
- **Socket Mode**: Use Socket Mode for development to avoid public endpoints
