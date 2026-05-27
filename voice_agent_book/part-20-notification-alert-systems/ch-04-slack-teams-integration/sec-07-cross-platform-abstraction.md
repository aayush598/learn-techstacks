# Section 07: Cross-Platform Abstraction

## Overview

The cross-platform abstraction layer provides a unified API for sending notifications to Slack and Teams. It defines a platform-independent message model and adapters that translate to platform-specific formats. This enables sending to multiple platforms with a single API call and ensures feature parity where possible.

## Implementation Approach

```typescript
interface UnifiedMessage {
  title: string;
  body: string;
  severity?: string;
  actions: UnifiedAction[];
  fields: UnifiedField[];
  metadata: Record<string, unknown>;
}

interface UnifiedAction {
  id: string;
  label: string;
  type: 'acknowledge' | 'resolve' | 'escalate' | 'view' | 'custom';
  url?: string;
  style?: 'primary' | 'danger' | 'default';
}

interface UnifiedField {
  label: string;
  value: string;
  isShort?: boolean;
}

abstract class PlatformAdapter {
  abstract send(message: UnifiedMessage, channel: ChannelRef): Promise<void>;
  abstract update(messageId: string, message: UnifiedMessage): Promise<void>;
  abstract supports(feature: PlatformFeature): boolean;
}

class SlackPlatformAdapter extends PlatformAdapter {
  async send(message: UnifiedMessage, channel: ChannelRef): Promise<void> {
    const blocks = this.convertToBlocks(message);
    await this.slackService.sendMessage(channel.workspaceId, channel.channelId, {
      text: message.title,
      blocks,
    });
  }

  private convertToBlocks(message: UnifiedMessage): Block[] {
    const blocks: Block[] = [
      { type: 'header', text: { type: 'plain_text', text: message.title, emoji: true } },
      { type: 'section', text: { type: 'mrkdwn', text: message.body } },
    ];

    if (message.fields.length > 0) {
      blocks.push({
        type: 'section',
        fields: message.fields.map(f => ({
          type: 'mrkdwn',
          text: `*${f.label}:* ${f.value}`,
        })),
      });
    }

    if (message.actions.length > 0) {
      blocks.push({
        type: 'actions',
        elements: message.actions.map(a => ({
          type: 'button',
          text: { type: 'plain_text', text: a.label, emoji: true },
          style: a.style,
          action_id: a.id,
          url: a.url,
          value: a.id,
        })),
      });
    }

    return blocks;
  }

  supports(feature: PlatformFeature): boolean {
    return ['blocks', 'buttons', 'modals', 'context'].includes(feature);
  }
}

class TeamsPlatformAdapter extends PlatformAdapter {
  async send(message: UnifiedMessage, channel: ChannelRef): Promise<void> {
    const card = this.convertToAdaptiveCard(message);
    await this.teamsService.sendAdaptiveCard(channel.workspaceId, channel.channelId, card);
  }

  private convertToAdaptiveCard(message: UnifiedMessage): AdaptiveCard {
    return {
      $schema: 'http://adaptivecards.io/schemas/adaptive-card.json',
      type: 'AdaptiveCard',
      version: '1.4',
      body: [
        { type: 'TextBlock', size: 'Large', weight: 'Bolder', text: message.title },
        { type: 'TextBlock', text: message.body, wrap: true },
        ...(message.fields.length > 0 ? [{
          type: 'FactSet',
          facts: message.fields.map(f => ({ title: f.label, value: f.value })),
        }] : []),
      ],
      actions: message.actions.map(a => ({
        type: a.url ? 'Action.OpenUrl' : 'Action.Submit',
        title: a.label,
        url: a.url,
        data: a.url ? undefined : { action: a.id },
      })),
    };
  }

  supports(feature: PlatformFeature): boolean {
    return ['adaptive_cards', 'buttons', 'facts'].includes(feature);
  }
}

class PlatformRouter {
  private adapters: Map<string, PlatformAdapter> = new Map();

  async send(message: UnifiedMessage, targets: ChannelTarget[]): Promise<void> {
    await Promise.all(targets.map(async target => {
      const adapter = this.adapters.get(target.platform);
      if (!adapter) throw new Error(`No adapter for platform: ${target.platform}`);

      // Fallback for unsupported features
      const requiredFeatures = this.getRequiredFeatures(message);
      const unsupported = requiredFeatures.filter(f => !adapter.supports(f));
      const adaptedMessage = this.applyFallbacks(message, unsupported);

      await adapter.send(adaptedMessage, target.channel);
    }));
  }
}
```

## Integration Points

- **Channel Targets**: Platform + channel reference pairs
- **Feature Detection**: Check platform capabilities before sending
- **Fallback Formatting**: Simplify messages for less capable platforms

## Production Considerations

- **Platform Differences**: Test on all target platforms
- **Feature Parity Map**: Document which features work on which platform
- **Progressive Enhancement**: Use platform-specific features when available
