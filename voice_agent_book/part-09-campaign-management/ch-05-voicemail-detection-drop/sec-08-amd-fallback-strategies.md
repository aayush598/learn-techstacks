# Section 08: AMD Fallback Strategies

## Overview

AMD Fallback Strategies define what happens when the Answering Machine Detection engine cannot confidently classify a call as human-answered or machine-answered. Even the best AMD systems produce uncertain classifications — typically 5-15% of calls depending on carrier, audio quality, and language. How the system handles these uncertain calls directly impacts campaign performance: routing an uncertain call to a human agent when it's actually a voicemail wastes agent time, while dropping an uncertain call that's actually a human frustrates the recipient and damages brand reputation.

A robust fallback strategy uses a multi-layered decision framework: confidence thresholds determine routing, carrier-specific profiles adjust behavior, retry logic gives uncertain calls a second chance, and real-time escalation to human agents handles the most ambiguous cases. The goal is not to eliminate uncertainty entirely but to manage it gracefully — routing each uncertain call to the least harmful outcome for both the campaign and the called party. Production systems typically target <2% false human hang-ups while keeping agent waste from uncertainty below 5% of total call volume.

## Architecture

```
                  AMD Fallback Decision Framework

                    +------------------+
                    | AMD Result In    |
                    | (confidence: 0.3-|
                    |  0.7 = uncertain)|
                    +--------+---------+
                             |
                             v
              +----------------------------+
              | Fallback Decision Engine   |
              |                            |
              |  confidence > 0.7 → human |
              |  confidence < 0.3 → drool  |
              |  0.3 <= c <= 0.7 → ?      |
              +----------------------------+
                      /         |         \
                     v          v          v
           +----------+  +----------+  +----------+
           | Carrier  |  | Retry    |  | Campaign |
           | Profile  |  | Strategy |  | Config   |
           +----------+  +----------+  +----------+
                |              |              |
                v              v              v
           +---------------------------------------+
           |    Fallback Action Selector            |
           |                                        |
           |  1. Wait & gather more audio (2s more) |
           |  2. Play disclaimer & connect           |
           |  3. Route to human agent                |
           |  4. Retry call later (different trunk)  |
           |  5. Apply carrier-specific rule         |
           |  6. Drop with wrong-party treatment     |
           +---------------------------------------+
                              |
                              v
                    +------------------+
                    | Action Executed  |
                    | (logged for      |
                    |  model training) |
                    +------------------+
```

## Design Decisions

- **Three-tier confidence threshold:** Human (>0.7), uncertain (0.3-0.7), machine (<0.3). The uncertain band is where fallback strategies apply. Trade-off: narrower uncertain band reduces fallback cases but increases misclassification risk; wider band catches more edge cases but triggers more fallback overhead.

- **Carrier-specific fallback profiles:** Fallback behavior is not one-size-fits-all. Carriers with known poor AMD accuracy (e.g., some VoIP providers that truncate audio) get more aggressive fallback. Trade-off: increased configuration complexity vs. significantly better outcomes for known problem carriers.

- **Audio buffering for deferred decision:** The system buffers 5-10 seconds of audio post-answer and can replay analysis with more context if initial classification is uncertain. Trade-off: memory/processing overhead vs. significant accuracy improvement from longer audio windows.

- **Progressive certainty model:** Instead of a single classification, AMD updates its certainty level continuously as more audio arrives. Fallback decisions are re-evaluated at each certainty update. Trade-off: more complex state management vs. faster resolution of uncertainty.

## Implementation Approach

```
class AmdFallbackManager {
  constructor(amdEngine, agentRouter, campaignConfig) {
    this.amdEngine = amdEngine;
    this.agentRouter = agentRouter;
    this.campaignConfig = campaignConfig;
    this.fallbackStrategies = {
      wait_and_listen: new WaitAndListenStrategy(),
      play_disclaimer: new PlayDisclaimerStrategy(),
      route_to_agent: new RouteToAgentStrategy(),
      retry_call: new RetryCallStrategy(),
      carrier_specific: new CarrierSpecificStrategy(),
      drop_wrong_party: new DropWrongPartyStrategy()
    };
  }

  async handleUncertainCall(callContext, amdResult) {
    const logEntry = {
      callId: callContext.callId,
      campaignId: callContext.campaignId,
      carrier: callContext.carrier,
      initialConfidence: amdResult.confidence,
      humanProbability: amdResult.humanProbability
    };

    // Step 1: Evaluate context
    const context = await this.evaluateContext(callContext, amdResult);

    // Step 2: Build fallback strategy stack
    const strategyStack = this.buildStrategyStack(context);

    // Step 3: Execute strategies in order
    let outcome = null;
    for (const strategy of strategyStack) {
      outcome = await strategy.execute(callContext, amdResult);
      if (outcome.decision !== 'continue') break;
    }

    // Step 4: Log decision for model improvement
    logEntry.finalOutcome = outcome;
    logEntry.strategiesTried = strategyStack.map(s => s.name);
    logEntry.executionTimeMs = Date.now() - callContext.startTime;
    await this.logFallbackDecision(logEntry);

    return outcome;
  }

  async evaluateContext(callContext, amdResult) {
    const campaign = await this.campaignConfig.get(callContext.campaignId);

    return {
      callContext,
      amdResult,
      campaign,
      carrierProfile: await this.loadCarrierProfile(callContext.carrier),
      contactHistory: await this.loadContactHistory(callContext.contactId),
      agentAvailability: await this.agentRouter.getAvailability(),
      retryCount: callContext.retryCount || 0,
      timeRemaining: this.computeTimeRemaining(callContext),
      businessCriticality: campaign.businessCriticality || 'normal'
    };
  }

  buildStrategyStack(context) {
    const stack = [];
    const campaign = context.campaign;
    const carrierProfile = context.carrierProfile;

    // Strategy 1: Wait for more audio (always first — cheapest)
    if (context.timeRemaining > 3000) {
      stack.push(this.fallbackStrategies.wait_and_listen);
    }

    // Strategy 2: Carrier-specific rules (if profile says this carrier is unreliable)
    if (carrierProfile && carrierProfile.amdReliability < 0.7) {
      stack.push(this.fallbackStrategies.carrier_specific);
    }

    // Strategy 3: Play disclaimer (if campaign allows it)
    if (campaign.allowDisclaimer) {
      stack.push(this.fallbackStrategies.play_disclaimer);
    }

    // Strategy 4: Route to agent (if available and campaign allows)
    if (context.agentAvailability.available > 0 && campaign.allowAgentFallback) {
      stack.push(this.fallbackStrategies.route_to_agent);
    }

    // Strategy 5: Retry call (different trunk / carrier)
    if (context.retryCount < campaign.maxFallbackRetries) {
      stack.push(this.fallbackStrategies.retry_call);
    }

    // Strategy 6: Drop with wrong-party treatment (last resort)
    stack.push(this.fallbackStrategies.drop_wrong_party);

    return stack;
  }

  loadCarrierProfile(carrier) {
    const profiles = {
      'verizon': { amdReliability: 0.85, fallback: 'wait_3s' },
      'tmobile': { amdReliability: 0.82, fallback: 'wait_3s' },
      'att': { amdReliability: 0.80, fallback: 'wait_3s' },
      'twilio': { amdReliability: 0.75, fallback: 'wait_5s_or_agent' },
      'vonage': { amdReliability: 0.70, fallback: 'play_disclaimer' },
      'bandwidth': { amdReliability: 0.78, fallback: 'wait_3s' },
      'default': { amdReliability: 0.70, fallback: 'route_to_agent' }
    };
    return profiles[carrier] || profiles['default'];
  }
}

// Wait & Listen Strategy
class WaitAndListenStrategy {
  constructor() {
    this.name = 'wait_and_listen';
    this.maxWaitMs = 5000;
    this.bufferSizeMs = 2000;
  }

  async execute(callContext, amdResult) {
    const startTime = Date.now();
    let confidence = amdResult.confidence;
    let elapsed = 0;

    while (elapsed < this.maxWaitMs) {
      const audioChunk = await callContext.audioStream.readChunk();
      const newResult = await callContext.amdEngine.analyzeAudio(
        audioChunk,
        callContext.carrier
      );

      confidence = newResult.confidence;
      elapsed = Date.now() - startTime;

      if (confidence >= callContext.campaignConfig.humanThreshold) {
        return {
          decision: 'human_routed',
          confidence,
          action: 'connect_call',
          detail: 'Confidence rose above human threshold with additional audio'
        };
      }

      if (confidence < callContext.campaignConfig.machineThreshold) {
        return {
          decision: 'machine_confirmed',
          confidence,
          action: 'trigger_voicemail',
          detail: 'Confidence dropped below machine threshold with additional audio'
        };
      }
    }

    // Still uncertain — pass to next strategy
    return {
      decision: 'continue',
      confidence,
      action: 'next_strategy',
      detail: `Remained uncertain after ${elapsed}ms of additional audio`
    };
  }
}

// Play Disclaimer Strategy
class PlayDisclaimerStrategy {
  constructor() {
    this.name = 'play_disclaimer';
    this.disclaimerMessage = 'This call may be recorded for quality assurance purposes.';
  }

  async execute(callContext, amdResult) {
    // Play a brief disclaimer that encourages human response
    const interactionId = await callContext.telphony.playAudio(
      callContext.callSid,
      this.disclaimerMessage
    );

    // Wait 1.5 seconds for response
    await sleep(1500);

    // Read audio chunk and re-analyze
    const responseAudio = await callContext.audioStream.readChunk();
    const newResult = await callContext.amdEngine.analyzeAudio(
      responseAudio,
      callContext.carrier
    );

    // A human who hears a disclaimer typically responds ("Hello? Who is this?")
    // A machine continues playing its greeting unaffected
    if (newResult.confidence >= callContext.campaignConfig.humanThreshold) {
      return {
        decision: 'human_confirmed',
        confidence: newResult.confidence,
        action: 'connect_call',
        detail: 'Human responded to disclaimer'
      };
    }

    return {
      decision: 'continue',
      confidence: newResult.confidence,
      action: 'next_strategy',
      detail: 'No response or machine-like response after disclaimer'
    };
  }
}

// Route to Agent Strategy
class RouteToAgentStrategy {
  constructor() {
    this.name = 'route_to_agent';
  }

  async execute(callContext, amdResult) {
    const agent = await callContext.agentRouter.findAvailableAgent(
      callContext.campaignId
    );

    if (!agent) {
      return {
        decision: 'continue',
        confidence: amdResult.confidence,
        action: 'next_strategy',
        detail: 'No agent available for uncertain call routing'
      };
    }

    // Bridge the call to agent with AMD uncertainty context
    await callContext.agentRouter.bridgeCall(
      callContext.callSid,
      agent.id,
      {
        uncertaintyContext: {
          confidence: amdResult.confidence,
          humanProbability: amdResult.humanProbability,
          carrier: callContext.carrier
        },
        suggestDisposition: 'confirm_human_or_machine'
      }
    );

    return {
      decision: 'routed_to_agent',
      confidence: amdResult.confidence,
      action: 'bridge_call',
      detail: `Routed uncertain call to agent ${agent.id}`,
      agentId: agent.id
    };
  }
}

// Retry Call Strategy
class RetryCallStrategy {
  constructor() {
    this.name = 'retry_call';
    this.minRetryDelayMs = 30000;
  }

  async execute(callContext, amdResult) {
    const campaign = callContext.campaignConfig;

    // Schedule retry with different carrier (trunk group)
    const newCarrier = this.selectAlternativeCarrier(
      callContext.carrier,
      campaign.availableCarriers
    );

    if (!newCarrier) {
      return {
        decision: 'continue',
        confidence: amdResult.confidence,
        action: 'next_strategy',
        detail: 'No alternative carrier available for retry'
      };
    }

    await callContext.retryScheduler.schedule({
      contactId: callContext.contactId,
      campaignId: callContext.campaignId,
      phoneNumber: callContext.phoneNumber,
      carrier: newCarrier,
      delayMs: this.minRetryDelayMs + Math.random() * 60000,
      reason: 'amd_uncertainty',
      previousCallSid: callContext.callSid,
      attemptNumber: callContext.retryCount + 1
    });

    // End current call
    await callContext.telphony.hangup(callContext.callSid);

    return {
      decision: 'retry_scheduled',
      confidence: amdResult.confidence,
      action: 'schedule_retry',
      detail: `Scheduled retry with carrier ${newCarrier}`,
      retryCarrier: newCarrier,
      retryDelayMs: this.minRetryDelayMs
    };
  }

  selectAlternativeCarrier(currentCarrier, availableCarriers) {
    return availableCarriers.find(c => c !== currentCarrier) || null;
  }
}

// Drop with Wrong-Party Treatment Strategy
class DropWrongPartyStrategy {
  constructor() {
    this.name = 'drop_wrong_party';
  }

  async execute(callContext, amdResult) {
    // Final fallback: treat as wrong party
    // Play apology message before disconnecting
    const apology = 'We apologize for the interruption. Goodbye.';
    await callContext.telphony.playAudio(callContext.callSid, apology);

    // Wait for playback to complete
    await sleep(1000);

    // Hang up
    await callContext.telphony.hangup(callContext.callSid);

    return {
      decision: 'dropped',
      confidence: amdResult.confidence,
      action: 'disconnect_with_apology',
      detail: 'Uncertain classification — dropped with wrong-party treatment'
    };
  }
}
```

## Integration Points

- **AMD Engine (sec-01, sec-02):** Fallback strategies consume AMD confidence scores and feature vectors
- **Agent Router (Part 08):** Human agent fallback for uncertain calls requiring manual classification
- **Call Retry (Ch 04):** Retry fallback schedules call retry with different trunk/carrier
- **Campaign Config (Ch 01):** Per-campaign fallback strategy selection and threshold configuration
- **Voicemail Drop (sec-03):** Machine-confirmed outcomes trigger voicemail drop flow
- **Carrier Profiles (Part 07):** Carrier-specific AMD reliability ratings guide fallback selection
- **Analytics (Ch 09):** Fallback strategy effectiveness tracking by outcome and cost
- **Consent & Compliance (Ch 07):** Disclaimer playback for compliance with uncertain classifications

## Open-Source Tools

- **BullMQ:** Retry job scheduling for uncertain call retries
- **Redis:** Call state storage for multi-strategy fallback orchestration
- **PostgreSQL:** Fallback decision logging and analysis
- **Prometheus + Grafana:** Fallback strategy effectiveness monitoring dashboards
- **OpenTelemetry:** Distributed tracing for fallback decision chains
- **node-audio-lame:** Audio playback for disclaimer messages

## Production Considerations

- False human hang-up rate (classifying human as machine) must be <2% — tune fallback aggression accordingly
- Wait-and-listen strategy adds 2-5 seconds to call setup time — consider the customer experience impact
- Disclaimer playback may confuse legitimate human answered calls — use sparingly
- Agent fallback for uncertain calls costs ~$0.50-1.00 per call — monitor cost impact of this strategy
- Retry strategy increases total dial volume — factor into pacing and carrier rate limits
- Carrier-specific AMD reliability should be updated monthly based on actual performance data
- Progressive certainty model works best — maintain a running classification, not a single snapshot
- Monitor fallback strategy distribution: if >20% of calls go through fallback, AMD tuning is needed
- Log full audio for a sample of uncertain calls (1-5%) for manual review and model improvement
- Wrong-party drop should be a last resort — it burns the phone number's reputation
- A/B test fallback strategy configurations to find the optimal balance for each campaign type
- Compliance note: disclaimer messages may be required in some jurisdictions when recording uncertain calls
- Fallback decision chains should have a total timeout to prevent calls from consuming resources indefinitely
- Consider ML-based strategy selection: train a model to predict the best fallback strategy based on call features
