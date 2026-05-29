# Section 06: Scenario Simulation

## Overview

Scenario simulation allows developers to test their agents against predefined and custom call scenarios. Scenarios define conversation flows with expected agent responses, edge cases (silence, interruptions, background noise), and load simulation. Scenarios are defined in YAML/JSON and can be executed individually or as part of a test suite.

## Architecture

```
Scenario Simulation Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scenario Definition (YAML):
  name: "Customer Support - Refund Request"
  description: "Test agent handling a refund request"
  config:
    language: "en-US"
    noise_level: "low"
    latency_profile: "normal"

  steps:
    - role: caller
      action: say
      text: "Hi, I'd like to request a refund"
      expected_agent_response: "understand_issue"

    - role: agent
      verify:
        - "Intent recognition: refund_request"
        - "Sentiment: neutral"

    - role: caller
      action: say
      text: "My order number is ORD-12345"
      expected_agent_response: "request_details"

    - role: agent
      verify:
        - "Entity extraction: order_id = ORD-12345"
        - "Polite tone maintained"

    - role: caller
      action: say
      text: "I want a full refund to my card"
      expected_agent_response: "process_refund"

    - role: agent
      verify:
        - "Refund amount correctly calculated"
        - "Payment method confirmed"

Execution:
  [Scenario Engine] → Create sandbox call
       │
  [Execute Steps Sequentially]
       │
  Step 1: Caller: "Hi, I'd like a refund"
       │
  Step 2: Agent → Check response matches expected
       │
  Step 3: Caller: "Order ORD-12345"
       │
  Step 4: Agent → Verify entity extraction
       │
  [Generate Report]
  ├── Pass/Fail for each step
  ├── Response accuracy
  ├── Latency measurements
  └── Full transcript
```

## Design Decisions

- **YAML/JSON Definitions**: Human-readable scenario format; easy to version control
- **Step-by-Step Execution**: Each step is executed sequentially with verification
- **Dual Verification**: Server-side verification (entity extraction, intent) + response comparison
- **Reusable Steps**: Steps can reference named sub-flows for complex scenarios

## Implementation Approach

```typescript
// Scenario definition types
interface Scenario {
  name: string;
  description?: string;
  config?: ScenarioConfig;
  steps: ScenarioStep[];
}

interface ScenarioConfig {
  language?: string;
  noiseLevel?: 'low' | 'medium' | 'high';
  latencyProfile?: 'fast' | 'normal' | 'slow';
  errorRate?: number;
}

interface ScenarioStep {
  role: 'caller' | 'agent';
  action?: 'say' | 'wait' | 'hangup' | 'dtmf';
  text?: string;
  duration?: number;
  expected_agent_response?: string;
  verify?: string[];
}

// Scenario execution engine
class ScenarioEngine {
  async execute(scenario: Scenario, agentId: string): Promise<ScenarioResult> {
    const call = await this.createSandboxCall(agentId);
    const results: StepResult[] = [];

    try {
      for (let i = 0; i < scenario.steps.length; i++) {
        const step = scenario.steps[i];
        const result = await this.executeStep(step, call, i);
        results.push(result);

        if (result.status === 'failed' && step.role === 'agent') {
          // Agent verification failed — stop scenario
          break;
        }
      }
    } finally {
      await call.hangup();
    }

    return {
      scenarioName: scenario.name,
      agentId,
      totalSteps: scenario.steps.length,
      passed: results.filter(r => r.status === 'passed').length,
      failed: results.filter(r => r.status === 'failed').length,
      steps: results,
      transcript: call.getTranscript(),
      latency: results.map(r => r.latencyMs),
      duration: results.reduce((sum, r) => sum + r.durationMs, 0),
    };
  }

  private async executeStep(step: ScenarioStep, call: SandboxCall, index: number): Promise<StepResult> {
    const startTime = Date.now();

    try {
      if (step.role === 'caller') {
        switch (step.action) {
          case 'say':
            await call.simulateSpeech(step.text || '');
            break;
          case 'dtmf':
            await call.simulateDtmf(step.text || '');
            break;
          case 'wait':
            await new Promise(r => setTimeout(r, step.duration || 1000));
            break;
          case 'hangup':
            await call.hangup();
            break;
        }

        return {
          stepIndex: index,
          role: 'caller',
          action: step.action || 'say',
          status: 'passed',
          durationMs: Date.now() - startTime,
        };
      }

      // Agent verification step
      const response = await call.getLastAgentResponse();

      const verificationResults = step.verify?.map(v => ({
        check: v,
        passed: this.verifyCheck(v, response),
      })) || [];

      const allPassed = verificationResults.every(v => v.passed);
      const expectedMatch = step.expected_agent_response
        ? response?.intent === step.expected_agent_response
        : true;

      return {
        stepIndex: index,
        role: 'agent',
        status: allPassed && expectedMatch ? 'passed' : 'failed',
        latencyMs: response?.latency,
        durationMs: Date.now() - startTime,
        verificationResults,
        expectedIntent: step.expected_agent_response,
        actualIntent: response?.intent,
        agentResponse: response?.text,
      };
    } catch (error) {
      return {
        stepIndex: index,
        role: step.role,
        status: 'error',
        error: (error as Error).message,
        durationMs: Date.now() - startTime,
      };
    }
  }

  private verifyCheck(check: string, response: MockResponse | null): boolean {
    // Example: "Intent recognition: refund_request"
    if (check.startsWith('Intent recognition:')) {
      const expectedIntent = check.split(':')[1].trim();
      return response?.intent === expectedIntent;
    }

    // Example: "Sentiment: positive"
    if (check.startsWith('Sentiment:')) {
      const expectedSentiment = check.split(':')[1].trim();
      return response?.sentiment === expectedSentiment;
    }

    // Example: "Entity extraction: order_id = ORD-12345"
    if (check.startsWith('Entity extraction:')) {
      const [entity, value] = check.split(':')[1].trim().split('=').map(s => s.trim());
      return response?.entities?.[entity] === value;
    }

    return true;
  }
}

// Predefined edge case scenarios
const EDGE_CASE_SCENARIOS: Scenario[] = [
  {
    name: 'Silence Detection',
    description: 'Caller says nothing for 10 seconds',
    steps: [
      { role: 'caller', action: 'wait', duration: 10_000 },
      { role: 'agent', verify: ['Silence detection triggered', 'Prompted caller to respond'] },
    ],
  },
  {
    name: 'Interruption',
    description: 'Caller interrupts agent mid-speech',
    steps: [
      { role: 'caller', action: 'say', text: 'Hi' },
      { role: 'caller', action: 'say', text: 'I need help now!' },
      { role: 'agent', verify: ['Interruption handled gracefully'] },
    ],
  },
];
```

## Integration Points

- **CLI**: `voiceagent agents test --scenario refund-request.yaml`
- **CI/CD**: Scenario execution in CI pipeline for regression testing
- **Developer Portal**: Scenario runner with visual step-by-step display

## Production Considerations

- **Scenario Library**: Maintain library of standard scenarios covering common use cases
- **Test Data Management**: Each scenario run creates isolated test data; auto-cleanup
- **Timeouts**: Maximum scenario duration of 5 minutes to prevent runaway tests
- **Parallel Execution**: Support concurrent scenario execution for load testing

## Open-Source Tools

- **Mocha/Jest**: Scenario runner test framework integration
- **Chai**: Assertion library for scenario verification
