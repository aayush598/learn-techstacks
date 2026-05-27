# Section 06: Retry Exhaustion Handling

## Overview

Retry exhaustion occurs when a contact has reached the maximum configured attempts without a successful outcome. What happens at this point is critical — the contact should not be called again in this campaign, but the system may need to take additional actions. Exhaustion handling defines the terminal disposition, triggers post-exhaustion workflows, and may route the contact to alternative channels or different campaigns.

The exhaustion pipeline assigns a final disposition to the contact (e.g., "No Contact - Max Attempts"), triggers configurable actions (send SMS, flag for human review, update CRM), and moves the contact out of the active campaign queue. The system must handle exhaustion differently based on the last attempted outcome — a contact exhausted after 5 no-answers has a different profile than one exhausted after 5 answered-but-not-interested outcomes.

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
class ExhaustionHandler {
  constructor(attemptHistory, campaignService, channelService, crmAdapter) {
    this.attempts = attemptHistory;
    this.campaigns = campaignService;
    this.channels = channelService;
    this.crm = crmAdapter;
  }

  async handleExhaustion(contact, campaign, attemptHistory) {
    // Determine exhaustion pattern
    const pattern = this.analyzeAttemptPattern(attemptHistory);
    const finalDisposition = this.assignFinalDisposition(pattern);

    // Execute post-exhaustion actions
    const actions = await this.executeActions(
      contact, campaign, finalDisposition, pattern
    );

    // Update contact status in campaign
    await this.campaigns.updateContactStatus(
      contact.id,
      campaign.id,
      'exhausted',
      finalDisposition
    );

    // Check cross-campaign eligibility
    const crossCampaigns = await this.findEligibleCampaigns(
      contact, campaign, finalDisposition
    );

    return {
      finalDisposition,
      pattern,
      actions,
      crossCampaigns,
      exhaustedAt: new Date()
    };
  }

  analyzeAttemptPattern(attempts) {
    const outcomes = attempts.map(a => a.outcome);
    const uniqueOutcomes = [...new Set(outcomes)];
    const lastNAttempts = {};

    // Count outcomes in last 3 attempts (most recent patterns matter most)
    for (let i = 0; i < Math.min(3, attempts.length); i++) {
      lastNAttempts[attempts[i].outcome] = 
        (lastNAttempts[attempts[i].outcome] || 0) + 1;
    }

    if (uniqueOutcomes.length === 1) {
      return { type: 'uniform', outcome: uniqueOutcomes[0], lastNAttempts };
    }

    if (uniqueOutcomes.includes('answered') || uniqueOutcomes.includes('converted')) {
      return { type: 'partial_engagement', outcomes: uniqueOutcomes, lastNAttempts };
    }

    if (outcomes.some(o => ['wrong_number', 'disconnected'].includes(o))) {
      return { type: 'invalid_contact', outcomes: uniqueOutcomes, lastNAttempts };
    }

    return { type: 'mixed', outcomes: uniqueOutcomes, lastNAttempts };
  }

  assignFinalDisposition(pattern) {
    const dispositions = {
      'uniform_no_answer': 'No Contact - Unreachable',
      'uniform_busy': 'No Contact - Network Issue',
      'uniform_voicemail': 'Left Voicemail - No Response',
      'partial_engagement': 'Partial Engagement - Not Converted',
      'invalid_contact': 'Invalid Contact Information',
      'declined': 'Contact Declined',
      'mixed': 'No Contact - Multiple Issues'
    };

    const key = `${pattern.type}_${pattern.outcomes?.[0] || 'mixed'}`;
    return dispositions[key] || 'No Contact - Max Attempts';
  }

  async executeActions(contact, campaign, disposition, pattern) {
    const actions = [];
    const config = campaign.exhaustionConfig || {};

    // Action: Send SMS follow-up
    if (config.smsFollowUp) {
      const smsResult = await this.channels.sendSMS(
        contact.phone,
        this.buildSMSMessage(contact, campaign, disposition)
      );
      actions.push({ type: 'sms', result: smsResult });
    }

    // Action: Update CRM
    if (config.updateCRM) {
      const crmResult = await this.crm.updateContact(
        contact.crmId,
        { status: disposition, lastCampaign: campaign.name }
      );
      actions.push({ type: 'crm_update', result: crmResult });
    }

    // Action: Flag for human review
    if (this.shouldFlagForReview(pattern)) {
      const flagResult = await this.createReviewTicket(
        contact, campaign, disposition, pattern
      );
      actions.push({ type: 'human_review', result: flagResult });
    }

    // Action: Reactivation schedule
    if (config.reactivationDays) {
      const reactivationDate = new Date();
      reactivationDate.setDate(reactivationDate.getDate() + config.reactivationDays);
      
      await this.scheduleReactivation(contact, campaign, reactivationDate);
      actions.push({ type: 'reactivation', scheduledDate: reactivationDate });
    }

    return actions;
  }

  shouldFlagForReview(pattern) {
    return pattern.type === 'invalid_contact' ||
      pattern.lastNAttempts?.wrong_number > 0 ||
      pattern.lastNAttempts?.disconnected > 0;
  }

  async createReviewTicket(contact, campaign, disposition, pattern) {
    // Create a ticket for manual review of the contact
    return {
      ticketId: crypto.randomUUID(),
      priority: pattern.type === 'invalid_contact' ? 'high' : 'normal',
      description: `Contact ${contact.id} exhausted in campaign ${campaign.name} with disposition: ${disposition}`
    };
  }
}
```

## Integration Points

- **Attempt History (sec-05):** Provides the full attempt record for pattern analysis
- **Campaign Lifecycle (Ch 01):** Updates contact campaign status to exhausted
- **Multi-Channel Engine:** Executes SMS/email follow-ups after exhaustion
- **CRM Integration (Part 10, Ch 02):** Updates CRM with final disposition
- **Human Handoff (Part 08):** Creates review tickets for invalid contacts
- **Analytics (Ch 09):** Exhaustion rate tracking and disposition distribution reporting
- **Billing (Part 17):** Exhaustion events may affect billing (per-contact pricing)

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Exhaustion pattern analysis should consider the sequence of outcomes, not just distribution. A contact who answered on attempt 1 but not on attempts 2-5 is different from one who never answered.
- Reactivation should be opt-in by default — only re-contact exhausted contacts if they haven't opted out or complained.
- Cross-campaign eligibility should check mutual exclusivity rules — some contacts may be in a "no-contact" period across all campaigns.
- Exhaustion disposition data feeds back into contact scoring — contacts exhausted with "invalid contact" should have their quality score reduced.
- Provide a manual exhaust function in the UI for operators who need to override automated exhaustion decisions.
- Monitor exhaustion rate by campaign — sudden increases may indicate contact list quality issues or dialing problems.
- Exhaustion reasons should be summarized in campaign completion reports.
- When a contact is reactivated, the new attempt history should reference the previous campaign's exhaustion data.
- Consider time-based exhaustion: if a contact has been in a campaign for 90 days without reaching max attempts, auto-exhaust.
- Exhaustion handling should be auditable — record the exhaustion reason, pattern analysis, and all executed actions.
