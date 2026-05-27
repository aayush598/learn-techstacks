# Section 05: Interactive Notification Messages

## Overview

Interactive notifications allow users to take action directly from the notification message. Buttons enable acknowledgment, escalation, and resolution without leaving Slack/Teams. The system handles interaction events, updates original messages to reflect actions, and processes confirmation flows.

## Implementation Approach

```typescript
interface InteractiveAction {
  actionId: string;
  type: 'button' | 'select' | 'datepicker' | 'overflow';
  label: string;
  style?: 'primary' | 'danger' | 'default';
  confirm?: ConfirmationDialog;
  value?: string;
}

interface ActionHandler {
  actionId: string;
  handler: (payload: ActionPayload) => Promise<void>;
}

class InteractiveMessageManager {
  private handlers: Map<string, ActionHandler> = new Map();

  registerHandler(actionId: string, handler: (payload: ActionPayload) => Promise<void>): void {
    this.handlers.set(actionId, { actionId, handler });
  }

  async handleInteraction(payload: ActionPayload): Promise<void> {
    const handler = this.handlers.get(payload.actionId);
    if (!handler) throw new Error(`Unknown action: ${payload.actionId}`);
    await handler.handler(payload);
  }

  async handleAcknowledge(payload: ActionPayload): Promise<void> {
    const alertId = payload.value;
    await this.alertService.acknowledge(alertId, payload.user.id);

    // Update the original message
    await this.slackService.updateMessage(payload.responseUrl, {
      text: `✅ Alert acknowledged by ${payload.user.name}`,
      blocks: [
        {
          type: 'section',
          text: { type: 'mrkdwn', text: `✅ *Alert Acknowledged*\nAcknowledged by <@${payload.user.id}> at ${new Date().toLocaleString()}` },
        },
      ],
    });
  }

  async handleEscalate(payload: ActionPayload): Promise<void> {
    const { alertId, level } = JSON.parse(payload.value);
    await this.alertService.escalate(alertId, level);

    // Send escalation notification to next responder
    await this.notificationService.send({
      alertId,
      type: 'escalation',
      level,
      timestamp: new Date().toISOString(),
    });

    // Update original message
    await this.slackService.updateMessage(payload.responseUrl, {
      text: `⬆️ Alert escalated to Level ${level}`,
      blocks: [
        {
          type: 'section',
          text: { type: 'mrkdwn', text: `⬆️ *Alert Escalated*\nEscalated to Level ${level} by <@${payload.user.id}>` },
        },
      ],
    });
  }

  async handleResolve(payload: ActionPayload): Promise<void> {
    const alertId = payload.value;
    const reason = await this.collectResolutionReason(payload);
    await this.alertService.resolve(alertId, payload.user.id, reason);

    await this.slackService.updateMessage(payload.responseUrl, {
      text: `✅ Alert resolved by ${payload.user.name}`,
      blocks: [
        {
          type: 'section',
          text: { type: 'mrkdwn', text: `✅ *Alert Resolved*\nResolved by <@${payload.user.id}>\nReason: ${reason}` },
        },
      ],
    });
  }

  private async collectResolutionReason(payload: ActionPayload): Promise<string> {
    // Open a modal to collect reason
    const modal = {
      type: 'modal',
      callback_id: 'resolve_reason',
      title: { type: 'plain_text', text: 'Resolution Reason', emoji: true },
      submit: { type: 'plain_text', text: 'Submit', emoji: true },
      close: { type: 'plain_text', text: 'Cancel', emoji: true },
      blocks: [
        {
          type: 'input',
          block_id: 'reason_block',
          label: { type: 'plain_text', text: 'What was the root cause?', emoji: true },
          element: {
            type: 'plain_text_input',
            action_id: 'reason_input',
            multiline: true,
            placeholder: { type: 'plain_text', text: 'Describe the cause and resolution...', emoji: true },
          },
        },
      ],
    };
    const response = await this.slackService.openModal(payload.triggerId, modal);
    return response.submissions.reason_block.reason_input;
  }
}
```

## Integration Points

- **Slack Events API**: Receives interaction payloads
- **Alert Service**: Performs acknowledge/escalate/resolve operations
- **Message Updates**: Updates original message to reflect action

## Production Considerations

- **Token Verification**: Verify Slack request signatures
- **Action Expiry**: Interactive components expire after a few hours
- **Error Handling**: Show error messages in Slack on failures
