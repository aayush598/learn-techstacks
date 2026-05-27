# Section 05: Ticket Creation from Calls

## Overview

Ticket creation from calls is the core workflow of helpdesk integrations — automatically generating support tickets from voice conversations. When a customer calls with a support issue, the system creates a ticket in the connected helpdesk platform with all relevant call context: conversation summary, call recording link, contact identification, priority assessment, issue categorization, and related ticket references. This eliminates manual ticket creation by support agents and ensures no call-generated issues are lost.

The ticket creation workflow involves several steps: call intent detection (is this a support issue requiring a ticket?), contact identification (find or create the contact in the helpdesk), issue categorization (AI-based classification into appropriate categories), ticket creation (with varied priority based on sentiment and urgency), context enrichment (add call recording, summary, sentiment), and notification (alert appropriate team or agent). The system supports both automatic ticket creation (for clearly identified support issues) and suggested ticket creation (where the system drafts a ticket but requires agent confirmation).

## Architecture

```
                    Ticket Creation Workflow

   Call Conversation → Intent Detection → Support Issue? → Create Ticket
                                                               |
                                                               v
   +--------------------------------------------------------------+
   | Ticket Creation Pipeline                                      |
   |                                                               |
   |  1. Contact Identification                                    |
   |     • Look up existing contact by phone/email                  |
   |     • Create new contact if not found                          |
   |                                                               |
   |  2. Issue Classification (AI)                                  |
   |     • Category (Billing, Technical, Account, General)          |
   |     • Priority (Critical, High, Medium, Low)                   |
   |     • Sub-category (specific product/feature)                  |
   |                                                               |
   |  3. Context Assembly                                           |
   |     • Conversation summary (AI-generated)                      |
   |     • Call recording URL                                       |
   |     • Call metadata (duration, time, campaign)                 |
   |     • Customer sentiment score                                 |
   |     • Action items identified                                  |
   |                                                               |
   |  4. Helpdesk API Call                                          |
   |     • Create ticket with all context                           |
   |     • Link to existing related tickets                         |
   |     • Assign to appropriate group                              |
   |                                                               |
   |  5. Result Handling                                            |
   |     • Return ticket ID to voice agent                          |
   |     • Log ticket creation event                                |
   |     • Notify agent/group                                       |
   +--------------------------------------------------------------+
```

## Design Decisions

- **AI-based issue classification for ticket routing:** The call transcript is analyzed by an LLM to determine the issue category, priority, and required skill group. Classification accuracy targets 90%+ for defined categories. Low-confidence classifications are flagged for manual review rather than incorrect auto-routing. Trade-off: AI classification requires LLM API calls (cost and latency) and may misclassify unusual issues.

- **Queue-based ticket creation for resilience:** Ticket creation requests are placed on a work queue (BullMQ) for processing. The queue handler retries with exponential backoff on transient failures (rate limits, network issues), uses dead-letter queues for persistent failures, and supports prioritization (critical issues processed before standard ones). This prevents customer-facing latency during call handling. Trade-off: queue processing introduces 5-60 second delay between call end and ticket creation.

- **Conditional ticket creation with configurable triggers:** Not every call needs a ticket. Ticket creation is triggered based on configurable rules: call disposition (support issue identified), customer request (explicitly asked for follow-up), sentiment threshold (negative sentiment triggers ticket), campaign type (support campaigns always create tickets), or manual agent request. This prevents ticket spam from informational calls. Trade-off: conditional rules must be tuned to balance missed tickets vs. unnecessary tickets.

## Implementation Approach

```
interface TicketCreationRequest {
  callId: string;
  tenantId: string;
  contact: {
    email: string;
    name: string;
    phone: string;
    externalIds: Record<string, string>;  // CRM/helpdesk IDs
  };
  conversation: {
    summary: string;
    transcriptUrl: string;
    sentiment: number;
    topics: { topic: string; confidence: number }[];
    actionItems: string[];
  };
  classification: {
    category: string;
    priority: 'critical' | 'high' | 'medium' | 'low';
    subCategory?: string;
    confidence: number;
  };
  helpdeskConfig: {
    type: 'zendesk' | 'freshdesk' | 'intercom' | 'servicenow';
    integrationId: string;
    config: Record<string, any>;
  };
}

class TicketCreationService {
  async createTicketFromCall(request: TicketCreationRequest): Promise<{ ticketId: string; status: string }> {
    // Classify the issue if not pre-classified
    if (!request.classification || request.classification.confidence < 0.5) {
      request.classification = await this.classifyIssue(request.conversation);
    }

    const job = await this.queue.add('create_ticket', request, {
      priority: this.getPriority(request.classification.priority),
      attempts: 5,
      backoff: { type: 'exponential', delay: 5000 }
    });

    return { ticketId: job.id, status: 'queued' };
  }

  async processTicketCreation(job: Job<TicketCreationRequest>): Promise<string> {
    const request = job.data;
    const adapter = this.adapterRegistry.get(request.helpdeskConfig.type);
    const integrationConfig = request.helpdeskConfig.config;

    // Create ticket via adapter
    const response = await adapter.createTicket({
      subject: this.buildSubject(request),
      description: this.buildDescription(request),
      requesterEmail: request.contact.email,
      priority: this.mapPriority(request.classification.priority),
      type: request.classification.category,
      callData: {
        recordingUrl: request.conversation.transcriptUrl,
        duration: 0,
        summary: request.conversation.summary
      }
    });

    return response.data.id;
  }

  async classifyIssue(conversation: {
    summary: string; topics: { topic: string; confidence: number }[];
    sentiment: number;
  }): Promise<TicketCreationRequest['classification']> {
    const prompt = `Classify the following customer service call:\nSummary: ${conversation.summary}\nTopics: ${conversation.topics.map(t => t.topic).join(', ')}\nSentiment: ${conversation.sentiment}\n\nRespond with JSON: { "category": "...", "priority": "...", "subCategory": "...", "confidence": 0.0-1.0 }`;

    const response = await this.llmService.classify(prompt);
    return JSON.parse(response);
  }

  private buildSubject(request: TicketCreationRequest): string {
    const prefix = request.classification.priority === 'critical' ? '[URGENT] ' : '';
    const topics = request.conversation.topics.slice(0, 3).map(t => t.topic);
    return `${prefix}${request.classification.category}: ${topics.join(', ')}`;
  }

  private buildDescription(request: TicketCreationRequest): string {
    return `Voice Call Summary\n==================\n\n${request.conversation.summary}\n\nSentiment: ${request.conversation.sentiment}\n\nAction Items:\n${request.conversation.actionItems.map(a => `- ${a}`).join('\n')}\n\nCall Recording: ${request.conversation.transcriptUrl}`;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **BullMQ** (MIT) | Queue | Ticket creation job queue |
| **Redis** (BSD) | Data store | Queue state |
| **OpenAI/Anthropic** (API) | AI | Issue classification |

## Production Considerations

**Scaling:** AI-based classification is the bottleneck. Implement classification caching (same issue description → same classification). Use a fast classification model (classifier with < 500ms response) for real-time and a more accurate model for batch reprocessing. Queue-based processing absorbs traffic spikes.

**Security:** Ticket descriptions contain PII from call transcripts. Implement field-level encryption for sensitive fields. Classify transcripts for PII detection and redact before including in tickets (unless legally required). Log all ticket creation actions for audit.

**Monitoring:** Track ticket creation throughput (tickets/minute), classification confidence distribution, auto-creation rate vs. manual, queue depth and processing latency, and helpdesk-specific success/failure rates. Alert on classification confidence dropping below 70% average, ticket creation failures, and queue backlog exceeding 10 minutes.
