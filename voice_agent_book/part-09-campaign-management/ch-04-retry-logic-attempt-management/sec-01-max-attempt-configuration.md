# Section 01: Max Attempt Configuration

## Overview

Maximum attempt configuration defines how many times the system will attempt to reach a contact before marking them as exhausted. This seemingly simple setting has significant implications for campaign effectiveness, compliance, telephony costs, and customer experience. Too few attempts miss opportunities to connect; too many attempts can annoy contacts, increase costs, and violate regulatory call frequency limits.

The configuration supports global maximums (applied to all campaigns for a tenant), per-campaign overrides, per-contact overrides (for high-value leads), and time-based attempt counting (e.g., max 3 attempts within 7 days, then reset). The system must track attempt counts accurately, distinguish between attempted outcomes (no answer, busy, voicemail, answered), and apply different maximums based on result type. Regulatory compliance often dictates maximum attempt frequency — for example, debt collection regulations limit calls to 7 per 7 days per debt.

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
class AttemptConfigManager {
  constructor(configStore) {
    this.configStore = configStore;
  }

  async getEffectiveConfig(contact, campaign) {
    // Resolve configuration hierarchy
    const defaults = await this.configStore.getDefault();
    const campaignConfig = await this.configStore.getCampaignConfig(campaign.id);
    const contactConfig = await this.configStore.getContactConfig(contact.id);
    const segmentConfig = await this.getSegmentConfig(contact);

    // Merge with priority: contact > segment > campaign > default
    return {
      maxAttempts: contactConfig?.maxAttempts 
        || segmentConfig?.maxAttempts 
        || campaignConfig?.maxAttempts 
        || defaults.maxAttempts,
      
      maxPerDay: contactConfig?.maxPerDay 
        || campaignConfig?.maxPerDay 
        || defaults.maxPerDay,
      
      maxPerWeek: contactConfig?.maxPerWeek 
        || campaignConfig?.maxPerWeek 
        || defaults.maxPerWeek,
      
      weightByOutcome: campaignConfig?.weightByOutcome || defaults.weightByOutcome,
      
      resetOnPositive: campaignConfig?.resetOnPositive ?? defaults.resetOnPositive,
      
      outcomesRequiringHighWeight: ['wrong_number', 'disconnected', 'do_not_call']
    };
  }

  async canAttempt(contact, campaign) {
    const config = await this.getEffectiveConfig(contact, campaign);
    const history = await this.getAttemptHistory(contact.id, campaign.id);

    // Count weighted attempts
    const weightedTotal = this.calculateWeightedTotal(history, config);
    if (weightedTotal >= config.maxAttempts) {
      return { allowed: false, reason: 'max_attempts_reached', 
               current: weightedTotal, max: config.maxAttempts };
    }

    // Check daily limit
    const todayAttempts = this.filterByDate(history, 'today').length;
    if (todayAttempts >= config.maxPerDay) {
      return { allowed: false, reason: 'daily_limit',
               current: todayAttempts, max: config.maxPerDay };
    }

    // Check weekly limit
    const weekAttempts = this.filterByDate(history, 'week').length;
    if (weekAttempts >= config.maxPerWeek) {
      return { allowed: false, reason: 'weekly_limit',
               current: weekAttempts, max: config.maxPerWeek };
    }

    // Check for exhaustion on high-weight outcomes
    const highWeightOutcomes = history.filter(h =>
      config.outcomesRequiringHighWeight.includes(h.outcome)
    );
    if (highWeightOutcomes.length >= 1) {
      return { allowed: false, reason: 'high_weight_outcome',
               outcome: highWeightOutcomes[0].outcome };
    }

    return { allowed: true };
  }

  calculateWeightedTotal(history, config) {
    const weights = {
      'no_answer': 0.5,
      'busy': 0.5,
      'voicemail': 0.75,
      'answered': 1.0,
      'wrong_number': 2.0,
      'disconnected': 3.0,
      'opt_out': 0 // Final - don't count, just block
    };

    return history.reduce((total, attempt) => {
      const weight = config.weightByOutcome 
        ? (weights[attempt.outcome] || 1.0)
        : 1.0;
      return total + weight;
    }, 0);
  }

  resetOnPositiveOutcome(contactId, campaignId, positiveOutcome) {
    if (positiveOutcome) {
      // Reset attempt counter — contact is responsive
      return this.attemptStore.resetCounter(contactId, campaignId);
    }
  }
}
```

## Integration Points

- **Retry Engine (sec-02 to sec-06):** Max attempts configuration drives retry decisions
- **Campaign Lifecycle (Ch 01):** Exhausted contacts are removed from active campaign lists
- **Contact Suppression (Ch 02, sec-06):** Contacts reaching max attempts may be suppressed
- **Compliance Engine (Ch 07):** Regulatory call frequency limits correspond to max attempt config
- **Analytics (Ch 09):** Attempt exhaustion rate tracking and optimization
- **UI:** Attempt configuration interface in campaign settings

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Attempt count checks must be in the hot path (before every dial) — target sub-5ms with Redis caching
- Weighted counting can surprise operators — show the "effective attempts" in the contact history UI
- Time-window limiting requires careful boundary handling — a call at 11:59 PM and another at 12:01 AM are close in time but in different days
- Reset on positive outcome is valuable but can lead to infinite retries if not bounded — use absolute max attempts as a hard ceiling
- Regulatory limits (FCC's 7-in-7 for debt collection) must be enforced even if the configured max is higher
- Provide a "contact exhaustion forecast" — "This contact will reach max attempts in 2 more no-answers"
- Attempt configurations should be auditable — who changed what and when
- Consider seasonal max adjustments — higher max attempts during holiday seasons, lower during regulatory audit periods
- Export attempt exhaustion data for compliance reporting
- Monitor contacts reaching max attempts without any positive outcome — may indicate list quality issues
