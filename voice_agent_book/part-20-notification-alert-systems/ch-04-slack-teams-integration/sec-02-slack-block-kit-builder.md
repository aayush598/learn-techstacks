# Section 02: Slack Block Kit Builder

## Overview

Block Kit provides rich interactive message layouts for Slack notifications. The builder simplifies creating Block Kit messages with sections, actions, context, and interactive elements. It provides typed builders for alert notifications, approval requests, and status updates.

## Implementation Approach

```typescript
interface BlockKitMessage {
  blocks: Block[];
  text?: string;
}

class BlockKitBuilder {
  static alertBlock(alert: Alert): BlockKitMessage {
    const severityColors = {
      critical: '#FF0000',
      major: '#FFA500',
      minor: '#FFD700',
      warning: '#808080',
    };

    return {
      blocks: [
        {
          type: 'header',
          text: { type: 'plain_text', text: `🚨 ${alert.title}`, emoji: true },
        },
        {
          type: 'section',
          text: { type: 'mrkdwn', text: alert.message },
        },
        {
          type: 'context',
          elements: [
            { type: 'mrkdwn', text: `*Severity:* ${alert.severity}` },
            { type: 'mrkdwn', text: `*Source:* ${alert.metadata.source}` },
            { type: 'mrkdwn', text: `*Time:* ${new Date(alert.createdAt).toLocaleString()}` },
          ],
        },
        {
          type: 'divider',
        },
        {
          type: 'actions',
          elements: [
            {
              type: 'button',
              text: { type: 'plain_text', text: 'Acknowledge', emoji: true },
              style: 'primary',
              action_id: 'acknowledge_alert',
              value: alert.id,
            },
            {
              type: 'button',
              text: { type: 'plain_text', text: 'View Details', emoji: true },
              url: `${this.baseUrl}/alerts/${alert.id}`,
              action_id: 'view_alert',
            },
            {
              type: 'button',
              text: { type: 'plain_text', text: 'Silence', emoji: true },
              style: 'danger',
              confirm: {
                title: { type: 'plain_text', text: 'Silence this alert?' },
                text: { type: 'mrkdwn', text: 'This will silence notifications for this alert for 1 hour.' },
                confirm: { type: 'plain_text', text: 'Silence' },
                deny: { type: 'plain_text', text: 'Cancel' },
              },
              action_id: 'silence_alert',
              value: alert.id,
            },
          ],
        },
        {
          type: 'divider',
        },
        {
          type: 'section',
          fields: [
            { type: 'mrkdwn', text: `*Metric:* ${alert.metadata.metricName}` },
            { type: 'mrkdwn', text: `*Value:* ${alert.metadata.metricValue}` },
            { type: 'mrkdwn', text: `*Threshold:* ${alert.metadata.thresholdValue}` },
            { type: 'mrkdwn', text: `*Duration:* ${alert.metadata.duration}s` },
          ],
        },
      ],
      text: `Alert: ${alert.title}`,
    };
  }

  static modalForm(callbackId: string, title: string, fields: FormField[]): ModalView {
    return {
      type: 'modal',
      callback_id: callbackId,
      title: { type: 'plain_text', text: title, emoji: true },
      submit: { type: 'plain_text', text: 'Submit', emoji: true },
      close: { type: 'plain_text', text: 'Cancel', emoji: true },
      blocks: fields.map(f => ({
        type: 'input',
        block_id: f.blockId,
        label: { type: 'plain_text', text: f.label, emoji: true },
        element: {
          type: f.type === 'textarea' ? 'plain_text_input' : 'static_select',
          action_id: f.actionId,
          ...(f.type === 'select' ? { options: f.options?.map(o => ({ text: { type: 'plain_text', text: o.label }, value: o.value })) } : { multiline: f.type === 'textarea' }),
        },
        optional: f.optional,
      })),
    };
  }

  static digestBlock(items: DigestItem[]): BlockKitMessage {
    return {
      blocks: [
        { type: 'header', text: { type: 'plain_text', text: '📊 Daily Digest', emoji: true } },
        ...items.map(item => ({
          type: 'section',
          text: { type: 'mrkdwn', text: `*${item.title}*\n${item.summary}` },
          accessory: {
            type: 'button',
            text: { type: 'plain_text', text: 'View', emoji: true },
            url: item.url,
            action_id: `view_${item.id}`,
          },
        })),
      ],
    };
  }
}
```

## Integration Points

- **Alert Engine**: Converts alerts to Block Kit messages
- **Interactive Handlers**: Button actions handled by Slack event handlers
- **Modal Views**: Forms for configuring notifications

## Production Considerations

- **Block Limits**: Slack limits messages to 50 blocks
- **Interactive Expiry**: Buttons expire after a few hours
- **Accessibility**: Provide fallback text alongside blocks
