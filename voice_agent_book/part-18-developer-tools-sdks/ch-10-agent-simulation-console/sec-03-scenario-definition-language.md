# Section 03: Scenario Definition Language

## Overview

The Scenario Definition Language (SDL) uses YAML/JSON to define test scenarios for voice agents. Each scenario describes a conversation flow with steps for caller inputs and expected agent responses. SDL supports conditional branching, variable interpolation, and verification assertions for comprehensive testing.

## Architecture

```
Scenario Definition Language
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Scenario YAML] → [SDL Parser] → [Scenario AST] → [Simulation Engine]
       │                │                │
  Human-readable    Validates         Executable
  conversation      syntax &          step sequence
  definition        references         with branching

Scenario Structure:
  scenario/
  ├── metadata/
  │   ├── name: "Refund Request"
  │   ├── description: "Test refund flow"
  │   └── tags: ["refund", "customer-support"]
  ├── variables/
  │   ├── order_id: "ORD-{{$randomNumber}}"
  │   └── customer_name: "John Doe"
  ├── config/
  │   ├── exit_on_failure: true
  │   └── max_steps: 20
  └── steps/
      ├── step-01: caller say + verify
      ├── step-02: agent verify
      ├── step-03: conditional branch
      └── step-04: caller say + verify

Variable Interpolation:
  - {{$randomNumber}}    → Random number
  - {{$randomEmail}}     → Random email
  - {{$isoTimestamp}}    → Current ISO timestamp
  - {{variables.name}}   → Scenario variable
  - {{steps.0.response}} → Previous step response
```

## Design Decisions

- **YAML Primary, JSON Compatible**: YAML for readability; JSON for CI/CD automation
- **Declarative Steps**: Each step describes what to do, not how
- **Embedded Verification**: Verification assertions inline with conversation steps
- **Variable System**: Template variables for dynamic data and cross-step references

## Implementation Approach

```typescript
// SDL types
interface Scenario {
  name: string;
  description?: string;
  tags?: string[];
  variables?: Record<string, string>;
  config?: ScenarioConfig;
  steps: ScenarioStep[];
  exitOnFailure?: boolean;
}

interface ScenarioConfig {
  exitOnFailure?: boolean;
  maxSteps?: number;
  timeoutMs?: number;
  voiceConfig?: {
    callerVoice?: string;
    agentVoice?: string;
  };
}

type ScenarioStep = CallerStep | AgentStep | WaitStep | BranchStep;

interface BaseStep {
  id?: string;
  description?: string;
}

interface CallerStep extends BaseStep {
  role: 'caller';
  action: 'say';
  text: string;
  expectedAgentResponse?: string;
  timeoutMs?: number;
}

interface AgentStep extends BaseStep {
  role: 'agent';
  verify: string[];
}

interface WaitStep extends BaseStep {
  role: 'system';
  action: 'wait';
  durationMs: number;
}

interface BranchStep extends BaseStep {
  role: 'system';
  action: 'branch';
  condition: string;
  steps: ScenarioStep[];
  elseSteps?: ScenarioStep[];
}

// SDL Parser
class SdlParser {
  parse(content: string, format: 'yaml' | 'json'): ParsedScenario {
    const raw = format === 'yaml'
      ? yaml.parse(content)
      : JSON.parse(content);

    this.validateSchema(raw);
    this.validateReferences(raw);
    this.validateBranchConditions(raw);

    return this.normalize(raw);
  }

  private validateSchema(raw: any): void {
    if (!raw.name) throw new Error('Scenario must have a name');
    if (!raw.steps || !Array.isArray(raw.steps)) {
      throw new Error('Scenario must have steps array');
    }
    if (raw.steps.length === 0) {
      throw new Error('Scenario must have at least one step');
    }

    raw.steps.forEach((step: any, i: number) => {
      if (!step.role) throw new Error(`Step ${i} missing role`);
      if (!['caller', 'agent', 'system'].includes(step.role)) {
        throw new Error(`Step ${i} invalid role: ${step.role}`);
      }
      if (step.role === 'caller' && step.action !== 'say') {
        throw new Error(`Step ${i} caller steps must use action 'say'`);
      }
    });
  }

  private validateReferences(raw: any): void {
    const definedSteps = new Set(raw.steps.map((_: any, i: number) => `steps.${i}`));

    // Check variable references in step text
    raw.steps.forEach((step: any, i: number) => {
      if (step.text) {
        const refs = step.text.match(/\{\{steps\.(\d+)\.response\}\}/g) || [];
        refs.forEach((ref: string) => {
          const stepIndex = ref.match(/\d+/)?.[0];
          if (stepIndex && !definedSteps.has(`steps.${stepIndex}`)) {
            throw new Error(`Step ${i} references non-existent step ${stepIndex}`);
          }
        });
      }
    });
  }

  private normalize(raw: any): Scenario {
    return {
      name: raw.name,
      description: raw.description,
      tags: raw.tags,
      variables: raw.variables,
      config: raw.config,
      steps: raw.steps.map((step: any) => ({
        ...step,
        text: this.interpolateVariables(step.text, raw.variables),
      })),
    };
  }

  private interpolateVariables(text: string, variables?: Record<string, string>): string {
    if (!text) return text;

    return text.replace(/\{\{(\$?\w+(?:\.\w+)?)\}\}/g, (match, varName) => {
      if (varName.startsWith('$')) {
        return this.generateRandomValue(varName);
      }
      return variables?.[varName] || match;
    });
  }

  private generateRandomValue(varName: string): string {
    const generators: Record<string, () => string> = {
      '$randomNumber': () => Math.floor(Math.random() * 100000).toString(),
      '$randomEmail': () => `test-${Date.now()}@example.com`,
      '$isoTimestamp': () => new Date().toISOString(),
      '$randomPhone': () => `+1${Math.floor(Math.random() * 10000000000)}`,
    };
    return generators[varName]?.() || varName;
  }

  escapeRegex(str: string): string {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }
}

// Example scenario
const scenarioExample = `
name: "Customer Support - Refund Request"
description: "Test agent handling a refund request with conditional branching"
variables:
  order_id: "ORD-{{$randomNumber}}"
  customer_email: "{{$randomEmail}}"
config:
  exit_on_failure: true
  max_steps: 20
steps:
  - role: caller
    action: say
    text: "Hi, I'd like to request a refund for order {{variables.order_id}}"
    expected_agent_response: "understand_issue"

  - role: agent
    verify:
      - "Intent recognition: refund_request"
      - "Entity extraction: order_id = {{variables.order_id}}"

  - role: caller
    action: say
    text: "The product was damaged when it arrived"
    expected_agent_response: "apologize_and_ask_details"

  - role: agent
    verify:
      - "Sentiment: sympathetic"
      - "Resolution offered: refund or replacement"

  - role: system
    action: branch
    condition: "steps.3.response.contains('refund')"
    steps:
      - role: caller
        action: say
        text: "I'd prefer a full refund"
        expected_agent_response: "process_refund"
    elseSteps:
      - role: caller
        action: say
        text: "Send me a replacement instead"
        expected_agent_response: "process_replacement"

  - role: agent
    verify:
      - "Resolution status: completed"
`;
```

## Integration Points

- **Scenario Library**: Pre-built scenarios for common use cases
- **CI/CD Integration**: Scenarios executed as part of test suite
- **Scenario Generator**: Auto-generate scenarios from call recordings

## Production Considerations

- **Scenario Validation**: Syntax and reference validation before execution
- **Scenario Versioning**: Scenarios stored in version control alongside agent code
- **Scenario Library**: Curated library of test scenarios for different use cases
- **Complexity Limits**: Maximum 50 steps per scenario to prevent runaway tests

## Open-Source Tools

- **js-yaml**: YAML parsing in Node.js
- **Ajv**: JSON Schema validation for scenario format
- **Chance.js**: Random data generation for variables
