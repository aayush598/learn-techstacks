# Section 02: Test Phone Numbers

## Overview

Test phone numbers are virtual numbers that simulate real telephony behavior without connecting to the PSTN. These numbers support predefined test scenarios — echo test, silence detection, DTMF input, and busy signals. Developers can dial test numbers to verify their agent configurations in a controlled environment.

## Architecture

```
Test Phone Number System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Test Number Range:
  +1555-000-0000  → Echo Test: Repeats caller's speech
  +1555-000-0001  → Silence Test: No audio input
  +1555-000-0002  → DTMF Test: Responds to keypad input
  +1555-000-0003  → Busy Signal: Returns busy tone
  +1555-000-0004  → No Answer: Rings without pickup
  +1555-000-0005  → Predefined Script: Follows test scenario
  +1555-000-0999  → Custom Scenario: Developer-defined

Test Call Flow:
  [Developer's Phone] → Dial +1555-000-0000 (Echo Test)
       │
  [Sandbox Telephony Gateway]
       │
  [Mock SIP Server] → Identifies test number
       │
  [Scenario Engine] → Selects "Echo Test" scenario
       │
  [Call Established]
       │
  Developer: "Hello, this is a test"
  Agent:     "Hello, this is a test" (echoed back)

Test Number Management:
  Creating: POST /v1/sandbox/test-numbers
  {
    "number": "+15550000005",
    "scenario": "custom",
    "config": {
      "greeting": "Welcome to the test scenario",
      "steps": [
        { "type": "say", "text": "Press 1 for support" },
        { "type": "expect_dtmf", "expected": "1" },
        { "type": "say", "text": "You pressed 1" }
      ]
    }
  }
```

## Design Decisions

- **Dedicated Number Range**: Easily identifiable test numbers; never confused with real numbers
- **Predefined Scenarios**: Common test patterns available without configuration
- **Custom Scenarios**: Developers define their own test scripts for specific use cases
- **No PSTN Connectivity**: Test numbers route entirely within the sandbox environment

## Implementation Approach

```typescript
// Test number registry
interface TestNumber {
  number: string;
  scenario: TestScenarioType;
  config?: ScenarioConfig;
  tenantId: string;
  createdAt: Date;
}

type TestScenarioType = 'echo' | 'silence' | 'dtmf' | 'busy' | 'no_answer' | 'predefined' | 'custom';

interface ScenarioConfig {
  greeting?: string;
  steps: ScenarioStep[];
}

interface ScenarioStep {
  type: 'say' | 'expect_speech' | 'expect_dtmf' | 'wait' | 'hangup';
  text?: string;
  expected?: string;
  duration?: number;
}

// Test number service
class TestNumberService {
  private numbers: Map<string, TestScenario> = new Map();

  constructor() {
    this.registerDefaultScenarios();
  }

  private registerDefaultScenarios(): void {
    this.numbers.set('+15550000000', new EchoScenario());
    this.numbers.set('+15550000001', new SilenceScenario());
    this.numbers.set('+15550000002', new DtmfScenario());
    this.numbers.set('+15550000003', new BusyScenario());
    this.numbers.set('+15550000004', new NoAnswerScenario());
    this.numbers.set('+15550000005', new PredefinedScriptScenario());
  }

  getScenario(number: string): TestScenario | undefined {
    return this.numbers.get(number);
  }

  async createCustom(tenantId: string, config: ScenarioConfig): Promise<TestNumber> {
    const number = await this.allocateNumber(tenantId);
    const scenario = new CustomScenario(config);

    this.numbers.set(number, scenario);

    return {
      number,
      scenario: 'custom',
      config,
      tenantId,
      createdAt: new Date(),
    };
  }

  private async allocateNumber(tenantId: string): Promise<string> {
    // Allocate next available number from pool
    const baseNumber = '+1555000';
    const count = await this.getTenantNumberCount(tenantId);
    return `${baseNumber}${String(1000 + count).padStart(4, '0')}`;
  }
}

// Scenario interface
interface TestScenario {
  name: string;
  handleCall(call: TestCall, events: CallEventEmitter): Promise<void>;
}

class EchoScenario implements TestScenario {
  name = 'Echo Test';

  async handleCall(call: TestCall, events: CallEventEmitter): Promise<void> {
    events.emit('connected', { number: call.from });

    call.on('speech', async (text: string) => {
      // Echo back with slight delay
      await delay(500);
      events.emit('speech', text);
    });

    call.on('dtmf', async (digit: string) => {
      events.emit('speech', `You pressed ${digit}`);
    });
  }
}

class BusyScenario implements TestScenario {
  name = 'Busy Signal';

  async handleCall(call: TestCall, events: CallEventEmitter): Promise<void> {
    events.emit('busy', {});
    await delay(2000);
    events.emit('disconnected', { reason: 'busy' });
  }
}
```

## Integration Points

- **Sandbox Telephony Gateway**: Routes calls to test number service based on number prefix
- **Developer Portal**: Test number management UI for creating custom test numbers
- **CLI**: `voiceagent sandbox test-numbers create --scenario custom --file scenario.yaml`

## Production Considerations

- **Number Pool Management**: Ensure sufficient test numbers for all sandbox tenants
- **Number Recycling**: Release test numbers when tenants are deleted
- **Rate Limits on Test Numbers**: Limit calls per test number to prevent abuse
- **Test Number Documentation**: List available test numbers with scenario descriptions in documentation

## Open-Source Tools

- **Jambonz**: Open-source telephony server that can be configured for mock scenarios
- **FreeSWITCH**: Media server for audio processing in test scenarios
