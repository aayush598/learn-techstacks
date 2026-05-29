# Section 03: Mock Voice Agent Engine

## Overview

The mock voice agent engine simulates AI agent behavior without calling real AI APIs. It uses predefined conversation flows, canned responses, and configurable latency to mimic real agent behavior. Developers can test call flows, verify response handling, and simulate edge cases (errors, timeouts, unexpected inputs) deterministically.

## Architecture

```
Mock Engine Architecture
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Call Event] → [Mock Voice Agent Engine]
                    │
              ┌─────┴──────┐
              │ Scenario   │
              │ Matcher    │── Finds matching scenario
              └─────┬──────┘
                    │
              ┌─────┴──────┐
              │ Response   │
              │ Generator  │── Returns canned response
              └─────┬──────┘
                    │
              ┌─────┴──────┐
              │ Latency    │
              │ Simulator  │── Adds configurable delay
              └─────┬──────┘
                    │
              [Response to Call]

Mock Configuration:
  {
    "use_mock_ai": true,
    "mock_responses": {
      "default": "I'm a mock agent. How can I help you?",
      "greeting": "Hello! Welcome to the test call.",
      "farewell": "Thank you for calling. Goodbye!",
      "error": "I'm sorry, I encountered an error.",
      "intent:refund_request": "I understand you need a refund.",
      "intent:technical_support": "Let me help you with technical support."
    },
    "latency": {
      "min_ms": 200,
      "max_ms": 1000
    },
    "error_injection": {
      "rate": 0.05,
      "types": ["timeout", "server_error", "invalid_response"]
    }
  }
```

## Design Decisions

- **Deterministic Responses**: Same input always produces same output — vital for test reproducibility
- **Configurable Latency**: Simulate real-world AI response times for realistic timeout testing
- **Error Injection**: Random error simulation to test error handling in client applications
- **Intent Matching**: Mock engine can match caller utterances to intents using keyword matching

## Implementation Approach

```typescript
// Mock AI engine
interface MockAiConfig {
  responses: Record<string, string>;
  latency: { minMs: number; maxMs: number };
  errorInjection?: { rate: number; types: string[] };
  intentPatterns?: Record<string, RegExp[]>;
}

class MockAiEngine {
  private config: MockAiConfig;

  constructor(config: Partial<MockAiConfig> = {}) {
    this.config = {
      responses: {
        default: "I'm a mock agent. How can I help you?",
        greeting: 'Hello! This is a simulated call.',
        farewell: 'Thank you for calling. Goodbye!',
        error: 'An error occurred in the mock agent.',
      },
      latency: { minMs: 200, maxMs: 1000 },
      ...config,
    };
  }

  async processUtterance(
    utterance: string,
    context: ConversationContext,
  ): Promise<MockResponse> {
    // Simulate latency
    await this.simulateLatency();

    // Check for error injection
    if (this.shouldInjectError()) {
      return this.generateErrorResponse();
    }

    // Match intent
    const intent = this.matchIntent(utterance);
    const response = this.getResponse(intent, context);

    return {
      text: response,
      intent: intent || 'unknown',
      confidence: 0.95,
      latency: Date.now() - context.startedAt,
    };
  }

  async processGreeting(): Promise<MockResponse> {
    await this.simulateLatency();
    return {
      text: this.config.responses['greeting'] || this.config.responses.default,
      intent: 'greeting',
      confidence: 1.0,
      latency: this.config.latency.minMs,
    };
  }

  private matchIntent(utterance: string): string | null {
    const lower = utterance.toLowerCase();

    for (const [intent, patterns] of Object.entries(this.config.intentPatterns || {})) {
      for (const pattern of patterns) {
        if (pattern.test(lower)) {
          return intent;
        }
      }
    }

    return null;
  }

  private getResponse(intent: string | null, context: ConversationContext): string {
    if (intent && this.config.responses[`intent:${intent}`]) {
      return this.config.responses[`intent:${intent}`];
    }

    if (context.stepCount > 10) {
      return this.config.responses.farewell;
    }

    return this.config.responses.default;
  }

  private async simulateLatency(): Promise<void> {
    const { minMs, maxMs } = this.config.latency;
    const delay = minMs + Math.random() * (maxMs - minMs);
    await new Promise(resolve => setTimeout(resolve, delay));
  }

  private shouldInjectError(): boolean {
    if (!this.config.errorInjection) return false;
    return Math.random() < this.config.errorInjection.rate;
  }

  private generateErrorResponse(): MockResponse {
    const errorTypes = this.config.errorInjection?.types || ['server_error'];
    const errorType = errorTypes[Math.floor(Math.random() * errorTypes.length)];

    switch (errorType) {
      case 'timeout':
        throw new Error('Simulated timeout');
      case 'server_error':
        throw new Error('Simulated AI service error');
      case 'invalid_response':
        return {
          text: '',
          intent: 'error',
          confidence: 0,
          latency: 0,
          error: 'Simulated invalid response',
        };
      default:
        throw new Error('Simulated error');
    }
  }
}

interface MockResponse {
  text: string;
  intent: string;
  confidence: number;
  latency: number;
  error?: string;
}

interface ConversationContext {
  callId: string;
  stepCount: number;
  startedAt: number;
  utterances: string[];
}

// Predefined conversation flows
const predefinedFlows: Record<string, string[]> = {
  'support_refund': [
    'Hello! You have reached customer support. How can I help you?',
    'I understand you need a refund. Let me look up your order.',
    'Your refund of $49.99 has been processed. You will receive it in 5-7 business days.',
    'Is there anything else I can help you with?',
    'Thank you for calling. Have a great day!',
  ],
  'tech_support': [
    'Welcome to technical support. Please describe your issue.',
    'Let me help you troubleshoot that.',
    'Have you tried restarting the device?',
    'I will escalate this to our senior team.',
    'A specialist will contact you within 24 hours.',
  ],
};
```

## Integration Points

- **Sandbox Gateway**: Routes AI requests to MockAiEngine when mock mode is enabled
- **CLI Test**: `voiceagent agents test` uses mock engine for offline testing
- **Scenario Simulation**: Mock engine can be configured per-test for specific scenarios

## Production Considerations

- **Feature Parity**: Mock engine should cover all intent patterns that the real AI handles
- **Latency Distribution**: Real response latency follows a distribution; mock should match
- **Deterministic Mode**: For reproducible tests, support a seed-based random mode
- **Mock Limitations**: Document what the mock engine doesn't simulate (e.g., hallucinations)

## Open-Source Tools

- **OpenAI Mock**: Mock server for OpenAI API responses
- **WireMock**: HTTP mock server for simulating API responses
