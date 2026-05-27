# Section 06: Collection & Recovery Campaigns

## Overview

Collection and recovery campaigns are among the most regulated outbound campaign types, operating under strict legal frameworks like the Fair Debt Collection Practices Act (FDCPA) in the US and equivalent regulations globally. These campaigns must balance recovery effectiveness with compliance, consumer protection, and brand reputation. The architecture must support right-party contact verification, payment processing over voice, dispute handling, and detailed record-keeping for regulatory audit.

The AI agent in collection campaigns must handle sensitive conversations with empathy while collecting payments or negotiating payment arrangements. The system must verify the contact's identity before discussing debt details, support payment via credit card or bank account over the phone, and document every interaction for compliance purposes. Integration with billing systems and payment gateways is essential for real-time balance inquiry and payment processing.

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
class CollectionCampaign {
  constructor(config, billingAdapter, paymentGateway) {
    this.billing = billingAdapter;
    this.payment = paymentGateway;
    this.compliance = new ComplianceChecker(config.jurisdiction);
  }

  async conductCollectionCall(contact, agent) {
    await agent.say(this.compliance.getMiniMiranda());
    
    const rpcResult = await this.verifyRightParty(contact, agent);
    if (!rpcResult.verified) {
      await agent.say("I'm sorry, I cannot discuss this matter further.");
      return { outcome: 'wrong_party', details: rpcResult };
    }

    const debtInfo = await this.billing.getOutstandingBalance(contact.accountId);
    
    const paymentResult = await this.discussAndCollect(debtInfo, agent);
    
    return {
      outcome: paymentResult.outcome,
      amount: paymentResult.amount,
      paymentMethod: paymentResult.method,
      paymentPlan: paymentResult.plan,
      receiptRef: paymentResult.receiptId
    };
  }

  async verifyRightParty(contact, agent) {
    // Multi-factor verification
    const dobResponse = await agent.ask("Can you confirm your date of birth?");
    const zipResponse = await agent.ask("And your ZIP code?");
    
    return {
      verified: this.matchIdentity(contact, dobResponse, zipResponse),
      confidence: this.calculateConfidence(dobResponse, zipResponse)
    };
  }

  async discussAndCollect(debtInfo, agent) {
    const intent = await agent.determineIntent();
    
    switch (intent) {
      case 'pay_full':
        return this.processFullPayment(debtInfo, agent);
      case 'payment_plan':
        return this.setupPaymentPlan(debtInfo, agent);
      case 'dispute':
        return this.handleDispute(debtInfo, agent);
      case 'hardship':
        return this.offerHardshipOptions(debtInfo, agent);
      default:
        return this.scheduleFollowUp(debtInfo);
    }
  }
}
```

## Integration Points

- **Payment Gateway (Part 10, Ch 06):** PCI-compliant payment processing with tokenization
- **Billing System (Part 17):** Balance inquiry, payment posting, and account status updates
- **Compliance Engine (Ch 07):** DNC checking, TCPA compliance, call recording consent
- **CRM Integration (Part 10, Ch 02):** Collection activity logging and account notes
- **Case Management System:** Dispute case creation and routing
- **Human Handoff (Part 08):** Escalation for complex negotiations or dispute resolution

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Collection campaigns must use a separate, higher-compliance telephony configuration — different caller ID, different carrier, distinct compliance settings
- Every call must be recorded with consent, and recordings must be retained per regulatory requirements (typically 2-7 years)
- Payment card data must never be stored or logged — use tokenization and PCI-compliant payment gateways exclusively
- Right-party contact verification failure rate can be 20-30% — design the flow to handle this gracefully
- Debt dispute handling must include a case number generation and written dispute confirmation
- Consumer protection regulations limit call frequency — enforce strict per-contact and per-week call limits
- Collection campaigns should have a do-not-call opt-out that is immediate and irreversible for the campaign
- All collection communications must include the debt collector's business name and contact information
- Monitor complaint rates closely — a spike in complaints can trigger regulatory investigation
