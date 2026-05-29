# Section 01: Simulation Engine Architecture

## Overview

The simulation engine provides a controlled environment for testing voice agents without making live calls. It generates synthetic conversations by simulating caller inputs, runs them through the agent pipeline, and captures results for analysis. The engine supports configurable timing, voice simulation, and event injection for comprehensive testing.

## Architecture

```
Simulation Engine Architecture
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Scenario Definition] → [Simulation Engine] → [Results & Analytics]
         │                       │                        │
    YAML/JSON scenario      Orchestrator             Transcript
    - conversation steps    - step executor           Response metrics
    - expected responses    - timing control          Latency data
    - conditional branches  - event simulation        Diff view
                             - voice simulation
                                   │
                    ┌──────────────┴──────────────┐
                    │                              │
            [Agent Pipeline]              [Call Infrastructure]
            - STT/TTS engines             - WebRTC simulation
            - NLU processing              - SIP simulation
            - Dialog management           - Media stream mock
            - Knowledge retrieval         - Event injection

Simulation Flow:
  1. Load scenario YAML/JSON
  2. Initialize simulated session
  3. For each step:
     a. Inject caller input (text or audio)
     b. Process through agent pipeline
     c. Capture agent response
     d. Verify against expected response
     e. Measure latency
  4. Generate simulation report
```

## Design Decisions

- **Isolated Pipeline Instance**: Each simulation runs in its own agent pipeline instance
- **Synthetic Audio**: Audio input generated via TTS instead of pre-recorded files
- **Deterministic Timing**: Configurable timing simulation (fast-forward or real-time)
- **Step-by-Step Execution**: Manual step-through mode for debugging

## Implementation Approach

```typescript
// Core simulation engine
interface SimulationConfig {
  scenarioPath: string;
  mode: 'automated' | 'step-through';
  timing: 'realtime' | 'fast' | 'manual';
  voiceSimulation: boolean;
  pipelineConfig: {
    sttEngine: string;
    ttsEngine: string;
    nluModel: string;
  };
}

interface SimulationStep {
  role: 'caller' | 'agent';
  action: 'say' | 'wait' | 'verify';
  text?: string;
  expectedAgentResponse?: string;
  verify?: string[];
  timeoutMs?: number;
}

interface StepResult {
  stepIndex: number;
  callerInput?: string;
  agentResponse: string;
  latencyMs: number;
  verificationResults: Array<{
    check: string;
    passed: boolean;
    actual: string;
    expected: string;
  }>;
  status: 'passed' | 'failed' | 'timed_out';
}

class SimulationEngine {
  private agentPipeline: AgentPipeline;
  private eventBus: EventBus;

  constructor(config: SimulationConfig) {
    this.agentPipeline = new AgentPipeline(config.pipelineConfig);
    this.eventBus = new EventBus();
  }

  async runScenario(scenario: Scenario): Promise<SimulationResult> {
    const steps: StepResult[] = [];

    for (let i = 0; i < scenario.steps.length; i++) {
      const step = scenario.steps[i];

      if (this.config.mode === 'step-through') {
        await this.waitForUserAdvance();
      }

      if (step.role === 'caller') {
        const result = await this.executeCallerStep(step, i);
        steps.push(result);

        this.eventBus.emit('step-completed', result);

        if (result.status === 'failed' && scenario.exitOnFailure) {
          break;
        }
      }
    }

    return {
      scenarioName: scenario.name,
      completedAt: new Date(),
      totalSteps: scenario.steps.length,
      passedSteps: steps.filter(s => s.status === 'passed').length,
      failedSteps: steps.filter(s => s.status === 'failed').length,
      timedOutSteps: steps.filter(s => s.status === 'timed_out').length,
      averageLatencyMs: this.calculateAverageLatency(steps),
      steps,
      transcript: this.generateTranscript(steps),
    };
  }

  private async executeCallerStep(step: SimulationStep, index: number): Promise<StepResult> {
    const startTime = performance.now();

    let agentResponse: string;
    let verificationResults: Array<{ check: string; passed: boolean; actual: string; expected: string }> = [];

    if (this.config.voiceSimulation) {
      // Simulate voice input via TTS + STT round trip
      const audioInput = await this.simulateVoiceInput(step.text!);
      agentResponse = await this.agentPipeline.processAudio(audioInput, { simulation: true });
    } else {
      // Direct text input to NLU
      agentResponse = await this.agentPipeline.processText(step.text!, { simulation: true });
    }

    const latencyMs = performance.now() - startTime;

    if (step.verify && step.verify.length > 0) {
      verificationResults = await this.runVerifications(step.verify, agentResponse);
    }

    const status = this.determineStepStatus(verificationResults, latencyMs, step.timeoutMs);

    return {
      stepIndex: index,
      callerInput: step.text,
      agentResponse,
      latencyMs,
      verificationResults,
      status,
    };
  }

  private async runVerifications(checks: string[], agentResponse: string): Promise<VerificationResult[]> {
    return checks.map(check => {
      const passed = agentResponse.includes(check)
        || new RegExp(this.escapeRegex(check)).test(agentResponse);
      return {
        check,
        passed,
        actual: agentResponse,
        expected: check,
      };
    });
  }

  private async simulateVoiceInput(text: string): Promise<AudioBuffer> {
    const tts = new TtsEngine({ provider: 'simulation' });
    const audio = await tts.synthesize(text);
    return audio;
  }

  private generateTranscript(steps: StepResult[]): string {
    return steps.map(s =>
      `[Caller]: ${s.callerInput || ''}\n[Agent]: ${s.agentResponse}\n`
    ).join('\n');
  }
}

// Event-based simulation progress
class SimulationEventBus {
  private handlers: Map<string, Function[]> = new Map();

  on(event: 'step-completed' | 'simulation-ended' | 'error', handler: (data: any) => void): void {
    const handlers = this.handlers.get(event) || [];
    handlers.push(handler);
    this.handlers.set(event, handlers);
  }

  emit(event: string, data: any): void {
    const handlers = this.handlers.get(event) || [];
    handlers.forEach(h => h(data));
  }
}
```

## Integration Points

- **Developer Portal**: Initiate simulations from web UI
- **Agent Pipeline**: Reuse same pipeline components as production
- **Results Storage**: Simulation results stored for trend analysis

## Production Considerations

- **Resource Isolation**: Simulation instances run in separate containers
- **Timeouts**: Maximum simulation duration prevents runaway tests
- **Cost Tracking**: Voice simulation TTS costs tracked per simulation

## Open-Source Tools

- **BullMQ**: Simulation job queue for concurrent execution
- **Pino**: Structured logging for simulation debugging
- **Chance.js**: Random data generation for test scenarios
