# Template Versioning

## Overview

Template Versioning defines the operational processes and workflow automation for the 02 Agent Template Marketplace domain. This section covers the step-by-step execution model, error handling, retry logic, and monitoring of the workflow.

## Workflow State Machine

```
                    ┌──────────────────┐
                    │   INITIATED      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  VALIDATING      │◄──────────────┐
                    └────────┬─────────┘               │
                             │                          │
                    ┌────────▼─────────┐               │
                    │  Validation      │──► FAILED ────┼──► COMPLETED
                    │  Passed?         │               │      (with errors)
                    └────────┬─────────┘               │
                             │ Yes                      │
                             ▼                          │
                    ┌──────────────────┐               │
                    │   PROCESSING     │──► FAILED ────┘
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  Processing      │
                    │  Complete?       │
                    └────────┬─────────┘
                             │ Yes
                             ▼
                    ┌──────────────────┐
                    │   COMPLETED      │
                    │   (Success)      │
                    └──────────────────┘
```

## Implementation

```typescript
// Workflow orchestration engine
interface WorkflowStep<TInput, TOutput> {
  name: string;
  execute(input: TInput, context: WorkflowContext): Promise<TOutput>;
  compensate?(input: TInput, context: WorkflowContext): Promise<void>;
  timeout?: number;
  retries?: number;
}

class WorkflowOrchestrator {
  private steps: WorkflowStep<any, any>[] = [];
  private completedSteps: string[] = [];
  private logger: Logger;

  constructor() {
    this.logger = pino({ name: 'workflow' });
  }

  addStep(step: WorkflowStep<any, any>): void {
    this.steps.push(step);
  }

  async execute<TInput, TOutput>(
    input: TInput,
    context: WorkflowContext
  ): Promise<TOutput> {
    let currentInput: any = input;

    for (const step of this.steps) {
      this.logger.info({ step: step.name }, 'Executing workflow step');
      
      try {
        const result = await this.executeWithRetry(step, currentInput, context);
        this.completedSteps.push(step.name);
        currentInput = result;
      } catch (err) {
        this.logger.error({ step: step.name, err }, 'Workflow step failed');
        await this.compensate(context);
        throw new WorkflowError(
          `Workflow failed at step ${step.name}: ${(err as Error).message}`,
          step.name
        );
      }
    }

    return currentInput as TOutput;
  }

  private async executeWithRetry(
    step: WorkflowStep<any, any>,
    input: any,
    context: WorkflowContext
  ): Promise<any> {
    const maxRetries = step.retries ?? 3;
    const timeout = step.timeout ?? 30000;

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        return await Promise.race([
          step.execute(input, context),
          new Promise((_, reject) =>
            setTimeout(() => reject(new TimeoutError(step.name)), timeout)
          ),
        ]);
      } catch (err) {
        if (attempt === maxRetries) throw err;
        this.logger.warn({ step: step.name, attempt }, 'Retrying step');
        await new Promise(r => setTimeout(r, Math.pow(2, attempt) * 1000));
      }
    }
  }

  private async compensate(context: WorkflowContext): Promise<void> {
    // Rollback completed steps in reverse order
    const compensated: string[] = [];
    for (const stepName of [...this.completedSteps].reverse()) {
      const step = this.steps.find(s => s.name === stepName);
      if (step?.compensate) {
        try {
          await step.compensate(context.input, context);
          compensated.push(stepName);
        } catch (err) {
          this.logger.error({ step: stepName, err }, 'Compensation failed');
        }
      }
    }
    this.logger.info({ compensated }, 'Compensation completed');
  }
}
```

## Retry & Error Handling

The workflow engine implements a sophisticated retry strategy:

| Attempt | Delay | Jitter | Backoff Factor |
|---------|-------|--------|----------------|
| 1 | 1s | ±100ms | - |
| 2 | 2s | ±200ms | 2x |
| 3 | 4s | ±400ms | 2x |
| 4 | 8s | ±800ms | 2x |
| 5 | 16s | ±1.6s | 2x |

After 5 attempts, the workflow is placed in a dead letter queue for manual review.

## Monitoring & Observability

Each workflow execution emits:

1. **Start event**: Workflow ID, step count, input summary
2. **Step completion**: Step name, duration, output summary
3. **Step failure**: Step name, error details, attempt number
4. **Workflow completion**: Total duration, steps, success/failure
5. **Workflow failure**: Failed step, error, compensation status

## Open Source Tools

- **BullMQ**: Redis-backed job queue for workflow steps
- **Temporal**: Workflow orchestration engine (for complex workflows)
- **Zod**: Input/output validation at each step
- **Pino**: Structured logging for workflow traces

## Production Configuration

```typescript
const workflowConfig = {
  defaultTimeout: 30000,
  maxRetries: 3,
  retryDelay: 1000,
  retryBackoff: 2,
  retryJitter: 100,
  deadLetterQueue: true,
  maxConcurrentWorkflows: 100,
  monitoringInterval: 5000,
};
```

## Summary

The workflow patterns described for Template Versioning provide a robust foundation for building reliable, observable, and maintainable business processes in the voice agent platform. The state machine approach with compensation ensures consistency even when failures occur.
