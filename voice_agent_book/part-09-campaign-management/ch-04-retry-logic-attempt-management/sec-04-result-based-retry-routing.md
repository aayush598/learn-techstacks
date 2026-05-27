# Section 04: Result-Based Retry Routing

## Overview

Result-based retry routing tailors retry behavior to the specific outcome of each call attempt. Different outcomes warrant different follow-up actions — a busy signal might trigger a quick retry, a wrong number should terminate all further attempts, and a voicemail delivery might route to a different channel. This outcome-driven approach improves efficiency by avoiding futile retries and adapting the retry strategy based on what happened.

The routing engine receives the call outcome from the telephony layer or AI agent analysis, classifies it into a standardized outcome type, and consults the campaign's retry routing rules to determine the next action. Actions include scheduling a retry (with specific interval), routing to a different channel (SMS, email), flagging for manual review, or marking the contact as exhausted. The system also supports conditional routing where the action depends on the attempt number combined with the outcome.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Audio    |--->| WebSocket|--->| Jitter   |--->| PLC      |--->| Player   |
| Producer |    | (WSS)    |    | Buffer   |    | (Packet  |    | (smooth  |
| (100ms   |    | (binary) |    | (adaptive|    |  Loss    |    |  output) |
|  chunks) |    |          |    |  60-200) |    |  Conceal)|    +----------+
+----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```
class ResultBasedRouter {
  constructor(ruleEngine, actionExecutors) {
    this.ruleEngine = ruleEngine;
    this.executors = actionExecutors;
  }

  async route(contact, campaign, attempt, outcome, agentResult) {
    // Classify the raw outcome
    const classified = await this.classifyOutcome(outcome, agentResult);

    // Find matching rules (ordered by specificity)
    const rules = await this.ruleEngine.findRules(
      campaign.id,
      classified.type,
      attempt.number,
      contact.segmentId
    );

    if (rules.length === 0) {
      // Default routing
      return this.defaultRoute(contact, classified);
    }

    const results = [];

    for (const rule of rules) {
      const executor = this.executors[rule.action.type];
      if (!executor) {
        console.error(`No executor for action: ${rule.action.type}`);
        continue;
      }

      try {
        const result = await executor.execute(contact, campaign, {
          ...rule.action.params,
          attempt,
          outcome: classified
        });
        results.push(result);
      } catch (error) {
        await this.handleRoutingError(contact, rule, error);
      }

      // Check if we should stop after this action
      if (rule.stopOnMatch) break;
    }

    return {
      outcome: classified,
      rules: rules.map(r => r.id),
      actions: results
    };
  }

  async classifyOutcome(rawOutcome, agentResult) {
    // Merge telephony and AI agent signals
    const telephonyType = this.classifyTelephony(rawOutcome);
    
    // If AI agent provided a structured outcome, use it
    if (agentResult && agentResult.disposition) {
      return {
        type: agentResult.disposition,
        confidence: agentResult.confidence || 0.9,
        details: agentResult.details,
        source: 'agent'
      };
    }

    return {
      type: telephonyType,
      confidence: rawOutcome.confidence || 0.8,
      details: rawOutcome.details,
      source: 'telephony'
    };
  }

  classifyTelephony(raw) {
    // Map telephony signals to outcome types
    if (raw.status === 'completed' && raw.duration > 0) {
      return 'answered';
    }
    if (raw.status === 'no-answer') return 'no_answer';
    if (raw.status === 'busy') return 'busy';
    if (raw.sitDetected) {
      if (raw.sitType === 'vacant') return 'disconnected';
      if (raw.sitType === 'no_circuit') return 'network_busy';
      return 'sit_tone';
    }
    if (raw.answeringMachineDetected) return 'voicemail';
    if (raw.faxDetected) return 'fax_detected';
    return 'unknown';
  }

  defaultRoute(contact, outcome) {
    // Sensible defaults when no rules match
    switch (outcome.type) {
      case 'answered':
      case 'converted':
        return { action: 'mark_success', retry: false };
      case 'no_answer':
      case 'busy':
        return { action: 'retry', interval: 3600000, retry: true };
      case 'wrong_number':
      case 'disconnected':
        return { action: 'suppress', retry: false };
      default:
        return { action: 'retry', interval: 7200000, retry: true };
    }
  }
}

// Retry executor example
class RetryExecutor {
  constructor(retryQueue) {
    this.queue = retryQueue;
  }

  async execute(contact, campaign, params) {
    const nextTime = new Date(Date.now() + params.interval);
    
    // Apply jitter to prevent thundering herd
    const jitter = (Math.random() - 0.5) * params.interval * 0.2;
    nextTime.setMilliseconds(nextTime.getMilliseconds() + jitter);

    const job = await this.queue.add('retry_contact', {
      contactId: contact.id,
      campaignId: campaign.id,
      attemptNumber: params.attempt.number + 1
    }, {
      delay: Math.max(0, nextTime.getTime() - Date.now())
    });

    return { scheduled: true, jobId: job.id, nextTime };
  }
}
```

## Integration Points

- **Telephony Layer (Part 07):** Raw call outcome signals (SIT tones, status codes, duration)
- **AI Agent Runtime (Part 06):** Agent-provided outcomes (dispositions, intent analysis)
- **Retry Queue (BullMQ):** Retry actions add jobs to the retry queue
- **Suppression Engine (Ch 02, sec-06):** Suppress actions add contacts to suppression lists
- **Multi-Channel Engine:** Channel-switching actions route to SMS/email systems
- **Human Handoff (Part 08):** Escalation actions create handoff tickets
- **Analytics (Ch 09):** Outcome distribution and routing effectiveness tracking

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Outcome classification accuracy directly impacts retry quality — misclassifying a wrong number as "no answer" wastes resources
- SIT tone detection requires audio analysis — use the AMD engine (Ch 05) for accurate classification
- Channel-switching should respect contact preferences — some contacts have opted out of SMS but not voice
- Routing rules should support A/B testing — test different retry strategies against each other
- Log each routing decision with the rule ID, outcome, and action for compliance and optimization
- Provide a routing rule simulation tool — "What would happen if this contact got this outcome on attempt 3?"
- Backup routing: if all executors fail, the contact should not be stuck — default to a standard retry
- Multi-action atomicity: if one action fails (e.g., SMS send fails), the voice retry should still proceed
- Review routing effectiveness regularly — outcomes with very high retry rates but low conversion may need rule adjustment
- Compliance: some outcomes (wrong number, opt-out) must result in immediate cessation of all calling — no exceptions
