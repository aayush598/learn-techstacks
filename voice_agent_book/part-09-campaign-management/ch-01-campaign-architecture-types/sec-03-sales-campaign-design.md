# Section 03: Sales Campaign Design

## Overview

Sales campaigns are the most demanding campaign type, requiring tight integration with lead scoring systems, CRM pipelines, and revenue attribution models. Unlike reminder or survey campaigns, sales campaigns depend on lead quality, agent skill matching, and real-time decision making about which contact to call next. The call list must be dynamically prioritized based on lead score, engagement history, and contact availability to maximize conversion rates.

A well-designed sales campaign architecture supports lead prioritization, agent skill-based routing, real-time CRM synchronization, and disposition-driven list management. The system must handle multiple lead sources, deduplicate across lists, and track the complete sales journey from first contact to closed deal. Integration with the CRM is bidirectional — the campaign reads lead scores and contact data, and writes call outcomes, notes, and opportunity updates back to the CRM.

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
class SalesCampaign {
  constructor(config, crmAdapter) {
    this.config = config;
    this.crm = crmAdapter;
    this.scoringModel = new LeadScoringModel();
  }

  async selectNextContact(agent) {
    const candidates = await this.contactQueue.getCandidates(
      this.config.batchSize
    );
    
    const scored = await Promise.all(
      candidates.map(async (contact) => ({
        contact,
        score: await this.scoringModel.score(contact, agent),
        crmData: await this.crm.getLeadData(contact.crmId)
      }))
    );

    // Sort by composite score descending
    scored.sort((a, b) => b.score.composite - a.score.composite);
    
    // Match to best available agent
    for (const candidate of scored) {
      if (this.matchesAgentSkills(candidate, agent)) {
        return {
          ...candidate.contact,
          script: this.buildPersonalizedScript(
            candidate.crmData,
            candidate.score
          )
        };
      }
    }
    return null;
  }

  async recordDisposition(contactId, disposition, notes) {
    await this.crm.updateLead(
      contactId,
      this.mapDispositionToPipelineStage(disposition),
      notes
    );
    
    await this.updateContactScore(contactId, disposition);
    
    if (disposition === 'not_interested') {
      await this.scheduleFollowUp(contactId, '30_days');
    } else if (disposition === 'meeting_booked') {
      await this.crm.createOpportunity(contactId);
    }
  }
}
```

## Integration Points

- **CRM Integration (Part 10, Ch 02):** Bidirectional contact and opportunity sync
- **Agent Builder (Part 06):** Agent skill profiles and availability management
- **Dynamic Scripts (Ch 06):** Personalized scripts based on CRM data and lead score
- **Analytics (Ch 09):** Sales conversion tracking and pipeline analytics
- **Calendar Integration (Part 10, Ch 04):** Meeting booking during sales calls
- **Payment Gateway (Part 10, Ch 06):** Credit card capture during sales close

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Lead scoring models should be trained on historical conversion data and retrained monthly
- CRM API rate limits must be respected — implement a circuit breaker for each CRM adapter
- Agent skill matching requires a real-time presence system with sub-second updates
- Sales campaign reporting must differentiate between MQL, SQL, and opportunity stages
- List prioritization should allow manual overrides for high-priority leads from sales management
- Implement lead rotation rules to ensure fair distribution across the sales team
- Monitor conversion velocity — if leads are progressing too slowly, trigger re-scoring
