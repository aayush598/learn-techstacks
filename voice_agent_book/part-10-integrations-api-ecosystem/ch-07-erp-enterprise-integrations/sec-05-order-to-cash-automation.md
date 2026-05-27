# Section 05: Order-to-Cash Automation

## Overview

Order-to-cash (O2C) automation enables the voice agent platform to execute the complete sales fulfillment cycle: from order creation through invoice generation and payment collection, all triggered through natural language voice interactions. When a customer calls to place an order, the voice agent verifies their identity and account, looks up product catalog and pricing, creates the sales order in the ERP, initiates fulfillment, generates the invoice, and processes payment — all within a single call session without human intervention.

The O2C flow integrates multiple platform components: the voice call runtime (for DTMF payment collection), the payment gateway adapters (for charging), the ERP adapter (for order creation and status tracking), and the notification system (for order confirmation and shipping updates). The automation engine orchestrates these components through a configurable workflow, handling enterprise-specific variations like approval gates (orders above a threshold), credit checks, and tax calculation at each step.

## Architecture

```
              Order-to-Cash Automation Flow

   Customer Call → O2C Engine → ERP → Payment → Notification
                      |
   +----------------------------------------------------------+
   |              O2C Workflow State Machine                  |
   |                                                          |
   |  [Identify] → [Catalog] → [Order] → [Credit] → [Pay]   |
   |     |          Lookup      Create    Check      |        |
   |     v                                              v      |
   |  Customer                                          |     |
   |  Verification                                    [Invoice]
   |                                                      |    |
   |  Approval Gate (if > threshold)                     v    |
   |  → Manual approval required                    [Fulfill] |
   |  → Escalated to supervisor                         |     |
   |                                                     v    |
   |                                                [Shipping] |
   |                                                     |    |
   |                                                     v    |
   |                                               [Confirm]  |
   +----------------------------------------------------------+
```

## Design Decisions

- **Workflow-as-code with configuration over BPMN engine:** O2C workflows are defined as TypeScript classes implementing a `WorkflowStep` interface, with step sequencing defined in a JSON configuration file. This approach avoids the overhead of BPMN engines while providing enough structure to define enterprise approval flows. Workflows can include conditional branches (credit check required?), parallel steps (check inventory + validate pricing), and compensation handlers (rollback order if payment fails). Trade-off: workflow-as-code requires programming knowledge to modify but provides full expressiveness without BPMN tooling.

- **Saga pattern for distributed transactions across heterogeneous systems:** The O2C flow touches the ERP (order creation), the payment gateway (charge), the CRM (activity logging), and the notification system (confirmation). Since these are separate systems with no distributed transaction coordinator, the O2C engine implements the Saga pattern: each step has a forward action and a compensating action. If payment fails after order creation, the compensation cancels the order in the ERP. Trade-off: Saga adds complexity for compensation logic but provides data consistency without distributed transactions.

- **Approval gate for high-value orders over auto-approve:** Orders above a configurable threshold (default $5,000) are held for manual approval. The O2C engine creates the order in "Hold" status, notifies the sales supervisor via the notification system, and provides a dashboard for review/approval/rejection. The voice agent informs the customer: "Your order exceeds our standard processing limit. We will review and call you back within 2 hours." Trade-off: manual approval breaks the fully-automated flow for high-value orders but provides necessary enterprise controls for credit risk management.

## Implementation Approach

```
type WorkflowStepHandler = (context: WorkflowContext) => Promise<StepResult>;
type CompensationHandler = (context: WorkflowContext) => Promise<void>;

interface WorkflowDefinition {
  name: string;
  version: string;
  steps: WorkflowStepConfig[];
  timeout: number; // Overall workflow timeout in ms
}

interface WorkflowStepConfig {
  id: string;
  handler: string;
  compensation?: string;
  retryConfig?: { maxAttempts: number; backoffMs: number };
  condition?: string; // JSONPath expression to conditionally execute
}

interface WorkflowContext {
  workflowId: string;
  callSid: string;
  customerId: string;
  data: Record<string, any>;
  errors: StepError[];
  completedSteps: string[];
  startTime: Date;
}

class O2CEngine {
  private stepHandlers = new Map<string, WorkflowStepHandler>();
  private compensationHandlers = new Map<string, CompensationHandler>();
  private workflows: Map<string, WorkflowDefinition>;

  registerStep(name: string, handler: WorkflowStepHandler, compensation?: CompensationHandler) {
    this.stepHandlers.set(name, handler);
    if (compensation) this.compensationHandlers.set(name, compensation);
  }

  async executeO2CFlow(workflowName: string, initialData: Record<string, any>): Promise<WorkflowResult> {
    const workflow = this.workflows.get(workflowName);
    if (!workflow) throw new Error(`Workflow ${workflowName} not found`);

    const context: WorkflowContext = {
      workflowId: generateId('wf'),
      callSid: initialData.callSid,
      customerId: initialData.customerId,
      data: { ...initialData },
      errors: [],
      completedSteps: [],
      startTime: new Date(),
    };

    const compensationStack: string[] = [];

    for (const step of workflow.steps) {
      if (step.condition) {
        const shouldExecute = evaluateJsonPath(context.data, step.condition);
        if (!shouldExecute) continue;
      }

      try {
        const result = await this.executeWithRetry(step, context);
        context.data[step.id] = result.data;
        context.completedSteps.push(step.id);
        compensationStack.unshift(step.id);
      } catch (error) {
        context.errors.push({ stepId: step.id, error: (error as Error).message, timestamp: new Date() });

        // Execute compensation in reverse order
        for (const completedStepId of compensationStack) {
          const compensation = workflow.steps.find(s => s.id === completedStepId)?.compensation;
          if (compensation) {
            await this.compensationHandlers.get(compensation)!(context).catch(e => {
              logger.error(`Compensation failed for ${completedStepId}:`, e);
            });
          }
        }

        return { success: false, context, failedStep: step.id };
      }
    }

    return { success: true, context };
  }

  private async executeWithRetry(step: WorkflowStepConfig, context: WorkflowContext): Promise<StepResult> {
    const handler = this.stepHandlers.get(step.handler);
    if (!handler) throw new Error(`Handler ${step.handler} not registered`);

    const maxAttempts = step.retryConfig?.maxAttempts || 1;
    let lastError: Error | undefined;

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      try {
        return await handler(context);
      } catch (error) {
        lastError = error as Error;
        if (attempt < maxAttempts) {
          await sleep(step.retryConfig!.backoffMs * attempt);
        }
      }
    }

    throw lastError;
  }
}

// Registration of O2C steps
const o2cEngine = new O2CEngine();

o2cEngine.registerStep(
  'identifyCustomer',
  async (ctx) => {
    const customer = await erpAdapter.findCustomer(ctx.data.phoneNumber);
    ctx.data.customer = customer;
    return { success: true, data: customer };
  },
  async () => { /* No compensation needed for read */ }
);

o2cEngine.registerStep(
  'createOrder',
  async (ctx) => {
    const order = await erpAdapter.createSalesOrder(ctx.data.orderRequest);
    ctx.data.orderId = order.id;
    return { success: true, data: order };
  },
  async (ctx) => {
    if (ctx.data.orderId) {
      await erpAdapter.cancelSalesOrder(ctx.data.orderId);
    }
  }
);

o2cEngine.registerStep(
  'processPayment',
  async (ctx) => {
    const payment = await paymentAdapter.confirmPayment(ctx.data.paymentIntentId, {
      amount: ctx.data.orderTotal,
    });
    ctx.data.paymentResult = payment;
    return { success: true, data: payment };
  },
  async (ctx) => {
    if (ctx.data.paymentResult?.transactionId) {
      await paymentAdapter.refundPayment(ctx.data.paymentResult.transactionId);
    }
  }
);
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Zod (MIT) | Validation | Workflow config schema |
| Pino (MIT) | Logging | Step-level audit logging |
| NanoId (MIT) | IDs | Workflow correlation IDs |

## Production Considerations

**Scaling:** O2C workflows are long-running processes (30 seconds to several minutes depending on approval gates). Each workflow execution is persisted to a database and the engine can be distributed across multiple workers. Use a workflow queue (Bull/BullMQ) to distribute execution across worker processes. If a worker crashes mid-workflow, the engine rehydrates the context from the database and resumes from the last completed step.

**Security:** O2C workflows handle financial data — ensure that step handlers never log sensitive information (credit card data, full SSN). Each step should validate that the caller is authorized for the action (e.g., a customer cannot approve their own high-value order). Implement the "four eyes" principle for approval gates: the approver must be different from the requestor.

**Monitoring:** Track O2C workflow completion rate, average execution time per workflow and per step, step failure rates, compensation execution rates, and approval gate frequency. Monitor workflow timeout rate and identify frequently timing-out flows. Alert on workflow failures (especially payment step failures), compensation failures (data inconsistency risk), and approval gate backlog. Track O2C conversion rate: started vs. completed workflows.
