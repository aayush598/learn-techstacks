# Section 06: Message Actions & Workflows

## Overview

Message actions extend notification functionality with workflows triggered from Slack/Teams messages. Actions include creating tickets, triggering runbooks, opening incident bridges, and updating status pages. Workflow definitions specify sequences of automated steps triggered by Slack interactions.

## Implementation Approach

```typescript
interface WorkflowDefinition {
  id: string;
  name: string;
  trigger: WorkflowTrigger;
  steps: WorkflowStep[];
  timeout: number;
  onError: ErrorHandlingStrategy;
}

interface WorkflowTrigger {
  type: 'message_action' | 'slash_command' | 'event' | 'schedule';
  actionId?: string;
  command?: string;
  conditions?: Record<string, unknown>;
}

interface WorkflowStep {
  id: string;
  type: 'webhook' | 'notification' | 'delay' | 'condition' | 'sub_workflow';
  config: Record<string, unknown>;
  onComplete?: string; // next step id
  onFailure?: string;
}

class NotificationWorkflowEngine {
  private workflows: Map<string, WorkflowDefinition> = new Map();

  async execute(definition: WorkflowDefinition, context: WorkflowContext): Promise<WorkflowResult> {
    const execution = this.createExecution(definition, context);

    for (const step of definition.steps) {
      try {
        execution.currentStep = step.id;
        await this.executeStep(step, context);
        execution.completedSteps.push(step.id);
      } catch (error) {
        execution.errors.push({ step: step.id, error: error.message });
        if (definition.onError === 'abort') break;
        if (step.onFailure) {
          const fallback = definition.steps.find(s => s.id === step.onFailure);
          if (fallback) await this.executeStep(fallback, context);
        }
      }
    }

    return execution;
  }

  private async executeStep(step: WorkflowStep, context: WorkflowContext): Promise<void> {
    switch (step.type) {
      case 'webhook':
        await fetch(step.config.url as string, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ ...context, ...step.config.payload }),
        });
        break;
      case 'notification': {
        const channels = step.config.channels as string[];
        await Promise.all(channels.map(ch => this.notificationService.send(context.alert, ch)));
        break;
      }
      case 'delay':
        await new Promise(r => setTimeout(r, step.config.duration as number));
        break;
      case 'condition': {
        const condition = step.config.expression as string;
        const result = this.evaluateCondition(condition, context);
        const nextStep = result ? step.config.ifTrue : step.config.ifFalse;
        if (nextStep) {
          const next = context.workflow.steps.find(s => s.id === nextStep);
          if (next) await this.executeStep(next, context);
        }
        break;
      }
    }
  }

  // Pre-built workflow: Incident Response
  static readonly INCIDENT_RESPONSE_WORKFLOW: WorkflowDefinition = {
    id: 'incident_response',
    name: 'Incident Response',
    trigger: { type: 'message_action', actionId: 'trigger_incident_response' },
    steps: [
      { id: 'step1', type: 'webhook', config: { url: 'https://pagerduty.com/incidents', payload: { source: 'alert' } }, onComplete: 'step2' },
      { id: 'step2', type: 'notification', config: { channels: ['slack', 'sms'] }, onComplete: 'step3' },
      { id: 'step3', type: 'delay', config: { duration: 300000 }, onComplete: 'step4' },
      { id: 'step4', type: 'condition', config: { expression: 'alert.status !== "acknowledged"', ifTrue: 'step5' }, onComplete: 'step5' },
      { id: 'step5', type: 'notification', config: { channels: ['phone'] } },
    ],
    timeout: 3600000,
    onError: 'continue',
  };
}
```

## Integration Points

- **Slack Message Actions**: Workflows triggered from message action menus
- **External Systems**: Tickets, runbooks, status pages
- **Webhook Targets**: Third-party systems called during workflow

## Production Considerations

- **Workflow Timeouts**: Prevent runaway workflows
- **Error Recovery**: Define error handling per step
- **Audit Trail**: Log each workflow execution step
