# Section 07: Conversation Linking & History

## Overview

Conversation linking creates bidirectional associations between voice calls and helpdesk tickets, providing a complete communication history across channels. When a customer calls about an existing ticket, the voice platform retrieves the ticket context and presents it to the agent. After the call, the conversation is linked to the ticket as a work note, comment, or activity record. This creates a unified timeline — support agents can see all voice interactions related to a ticket alongside emails and chat messages.

The conversation linking system maintains a mapping table (ticket ID ↔ call ID with metadata) that enables both directions: given a ticket, find all related calls; given a call, find all related tickets. The system also supports linking across different helpdesk instances (a customer might call about a Zendesk ticket and a Freshdesk ticket in the same call) and linking to non-ticket entities (CRM opportunities, customer accounts, or custom objects).

## Architecture

```
                    Conversation Linking Architecture

   +------------------+     +------------------+     +------------------+
   | Voice Call       | --> | Link Manager     | --> | Helpdesk Ticket  |
   | (Call ID)        |     |                  |     | (Ticket ID)      |
   +------------------+     | +--------------+ |     +------------------+
                            | | Mapping Table| |
   +------------------+     | | call→ticket  | |     +------------------+
   | Helpdesk Webhook | --> | | ticket→call  | | --> | Voice Platform   |
   | (Ticket updated) |     | +--------------+ |     | (Call lookup)    |
   +------------------+     +------------------+     +------------------+
```

## Design Decisions

- **Database mapping table over helpdesk custom fields:** Links are stored in a dedicated database table (call_id, ticket_id, helpdesk_type, link_type, created_at, metadata) rather than in helpdesk custom fields. This provides faster queries, cross-helpdesk linking, and richer metadata. The helpdesk ticket also gets a reference (custom field or note) pointing back to the call for agent visibility. Trade-off: the mapping table is a separate system that must be backed up and managed independently of the helpdesk.

- **Automatic call-ticket linking based on conversation context:** The system automatically links calls to tickets by analyzing the conversation for ticket ID mentions ("I'm calling about ticket #12345"), customer phone/email matching the ticket requester, or call classification identifying the issue category matching an open ticket. When confidence is high (> 90%), links are created automatically; otherwise, they're suggested for agent confirmation. Trade-off: auto-linking may create incorrect associations at low confidence thresholds.

- **Rich link metadata for context preservation:** Each link stores metadata including the linking method (auto-detected, agent-specified, webhook-triggered), conversation summary at the time of linking, call disposition, and relevance score. This enables queries like "find all calls that were automatically linked to high-priority tickets with negative sentiment." Trade-off: storing rich metadata increases storage per link but enables more sophisticated analysis.

## Implementation Approach

```
interface CallTicketLink {
  id: string;
  callId: string;
  ticketId: string;
  helpdeskType: string;
  linkType: 'auto_detected' | 'agent_linked' | 'webhook' | 'manual';
  confidence?: number;       // 0-1 for auto-detected links
  metadata: {
    conversationSummary?: string;
    callDisposition?: string;
    sentimentAtLink?: number;
    agentId?: string;
  };
  createdAt: number;
}

class ConversationLinkService {
  async linkCallToTicket(link: CallTicketLink): Promise<void> {
    const existing = await this.findExistingLink(link.callId, link.ticketId);
    if (existing) {
      await this.updateLink(existing.id, link.metadata);
      return;
    }
    await this.storeLink(link);

    // Add reference in helpdesk ticket (if configured)
    if (link.linkType !== 'webhook') {
      await this.addHelpdeskReference(link);
    }
  }

  async autoDetectLinks(callId: string, transcript: string): Promise<CallTicketLink[]> {
    const links: CallTicketLink[] = [];

    // Method 1: Extract ticket IDs from transcript
    const ticketMentions = this.extractTicketIds(transcript);
    for (const mention of ticketMentions) {
      links.push({
        callId, ticketId: mention.ticketId,
        helpdeskType: mention.helpdeskType,
        linkType: 'auto_detected',
        confidence: mention.confidence,
        metadata: {}, createdAt: Date.now()
      });
    }

    // Method 2: Match caller to ticket requester
    const requesterLinks = await this.matchByRequester(callId);
    links.push(...requesterLinks);

    // Method 3: Match issue topic to open ticket categories
    const topicLinks = await this.matchByTopic(callId, transcript);
    links.push(...topicLinks);

    return links.filter(l => l.confidence >= 0.9);
  }

  async getCallContextForTicket(ticketId: string, helpdeskType: string): Promise<{
    recentCalls: number; lastCallSummary?: string;
    totalDuration: number; sentimentTrend: number[];
  }> {
    const links = await this.getLinksByTicket(ticketId, helpdeskType);
    const callIds = links.map(l => l.callId);
    const calls = await this.callService.getCalls(callIds);

    return {
      recentCalls: calls.length,
      lastCallSummary: calls[0]?.summary,
      totalDuration: calls.reduce((sum, c) => sum + c.duration, 0),
      sentimentTrend: calls.map(c => c.sentiment).reverse()
    };
  }

  async getTicketsForCall(callId: string): Promise<{
    helpdeskType: string;
    ticketId: string;
    status: string;
    subject: string;
  }[]> {
    const links = await this.getLinksByCall(callId);
    const results = [];
    for (const link of links) {
      const ticket = await this.helpdeskService.getTicket(
        link.helpdeskType, link.ticketId
      );
      if (ticket) {
        results.push({ helpdeskType: link.helpdeskType, ticketId: link.ticketId, status: ticket.status, subject: ticket.subject });
      }
    }
    return results;
  }

  private extractTicketIds(transcript: string): { ticketId: string; helpdeskType: string; confidence: number }[] {
    const patterns = [
      { regex: /ticket\s*#?(\d{5,})/gi, helpdeskType: 'zendesk' },
      { regex: /(?:INC|REQ|CHG)\d{7,}/gi, helpdeskType: 'servicenow' },
      { regex: /case\s*#?(\d{6,})/gi, helpdeskType: 'freshdesk' }
    ];
    return patterns.flatMap(p => {
      const matches = [...transcript.matchAll(p.regex)];
      return matches.map(m => ({ ticketId: m[1] || m[0], helpdeskType: p.helpdeskType, confidence: 0.95 }));
    });
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **PostgreSQL** (PostgreSQL) | Data store | Link mapping table |
| **Redis** (BSD) | Cache | Link lookup cache |
| **BullMQ** (MIT) | Queue | Async link processing |

## Production Considerations

**Scaling:** The link mapping table grows with call volume. Partition by month and archive data older than 12 months. Index by call_id and ticket_id for fast lookups. Use Redis cache with 1-hour TTL for recent lookups.

**Security:** Links expose the relationship between calls and tickets. Restrict link query access to authorized users within the same tenant. The ticket reference in helpdesk (custom field or note) should not expose sensitive call metadata that should remain internal to the voice platform.

**Monitoring:** Track auto-link rate (% of calls successfully linked), link confidence distribution, manual link corrections (agent overrides of auto-links), and query latency. Alert on auto-link rate dropping below 50% (may indicate ticket ID detection issues) and link creation failures.
