# Section 01: Zendesk API Integration

## Overview

Zendesk API integration enables the voice platform to create, update, and query support tickets based on voice conversations. When a customer calls about a support issue, the voice agent can create a Zendesk ticket, update an existing ticket with call notes, verify ticket status, or add public/private comments with call context. Zendesk's REST API provides access to tickets, users, organizations, groups, macros, triggers, automations, and custom fields.

Zendesk's API uses incremental exports for efficient data synchronization, side-loading for related data, and cursor-based pagination. The API supports both the standard Support API (tickets, users) and the Voice API (call logging, voicemail). Authentication is via API token (with user email) or OAuth 2.0. The adapter must handle Zendesk-specific concepts: ticket forms (custom fields with conditional logic), satisfaction ratings (CSAT after ticket resolution), ticket side conversations (multi-channel threads), and Zendesk Sunshine (custom profile objects).

## Architecture

```
                    Zendesk Integration Architecture

   Voice Agent Call → Ticket Context → Zendesk API → Ticket Update
        |
        v
   +------------------+
   | Zendesk Adapter   |
   | • Ticket CRUD     |
   | • User lookup     |
   | • Comment add     |
   | • Satisfaction    |
   +------------------+
        |
        v
   +------------------+
   | Zendesk API      |
   | • /api/v2/tickets |
   | • /api/v2/users   |
   | • /api/v2/search  |
   | • /api/v2/voice   |
   +------------------+
```

## Design Decisions

- **Ticket creation with call context enriched via custom fields:** Created tickets include the call recording URL, call duration, agent name, conversation summary, and sentiment in custom ticket fields. This provides agents picking up the ticket with full call context without needing to switch to the voice platform. Trade-off: requires custom field configuration in Zendesk and may be limited by Zendesk's custom field types.

- **Async ticket creation with queue-based processing:** Ticket creation is queued and processed asynchronously to avoid impacting call handling. The queue supports batching (multiple updates to the same ticket are merged) and deduplication (same call doesn't create duplicate tickets). Trade-off: queues introduce 5-30 second delay between call completion and ticket creation.

- **Webhook-based ticket update notifications:** Zendesk webhooks (via triggers or the Events API) notify the platform when tickets are updated. The platform can use these to trigger follow-up calls (e.g., when a ticket status changes to "Open" after being "Pending"). Webhooks are registered per-subdomain and filtered by relevant events. Trade-off: webhook setup requires manual configuration in each Zendesk instance.

## Implementation Approach

```
class ZendeskAdapter extends BaseAdapter {
  private baseUrl: string;

  constructor(config: ZendeskConfig) {
    super(config);
    this.baseUrl = `https://${config.subdomain}.zendesk.com/api/v2`;
  }

  async createTicket(ticket: {
    subject: string; description: string; requesterEmail: string;
    priority?: string; type?: string; customFields?: Record<string, any>;
    callData?: { recordingUrl?: string; duration?: number; summary?: string };
  }): Promise<AdapterResponse<{ id: string }>> {
    const zendeskTicket = {
      ticket: {
        subject: ticket.subject,
        comment: { body: ticket.description, public: false },
        requester: { email: ticket.requesterEmail },
        priority: ticket.priority || 'normal',
        type: ticket.type || 'task',
        custom_fields: this.buildCustomFields(ticket),
        tags: ['voice', 'call']
      }
    };

    const response = await this.execute({
      method: 'POST', url: `${this.baseUrl}/tickets.json`,
      data: zendeskTicket
    });
    return { success: true, data: { id: String(response.data.ticket.id) } };
  }

  async addComment(ticketId: string, comment: {
    body: string; isPublic: boolean; authorId?: string;
  }): Promise<AdapterResponse<void>> {
    await this.execute({
      method: 'PUT', url: `${this.baseUrl}/tickets/${ticketId}.json`,
      data: { ticket: { comment: { body: comment.body, public: comment.isPublic, author_id: comment.authorId } } }
    });
    return { success: true, data: undefined };
  }

  async searchTickets(query: string): Promise<AdapterResponse<Ticket[]>> {
    const response = await this.execute({
      method: 'GET', url: `${this.baseUrl}/search.json`,
      params: { query: `type:ticket ${query}`, sort_by: 'updated_at', sort_order: 'desc' }
    });
    return { success: true, data: response.data.results.map(this.mapTicket) };
  }

  async getTicketContext(requesterEmail: string): Promise<AdapterResponse<{
    openTickets: number; recentTicket?: TicketData; satisfaction?: string;
  }>> {
    const response = await this.execute({
      method: 'GET', url: `${this.baseUrl}/search.json`,
      params: { query: `type:ticket requester:${requesterEmail} status<closed`, sort_by: 'updated_at' }
    });
    const tickets = response.data.results;
    return {
      success: true,
      data: {
        openTickets: tickets.length,
        recentTicket: tickets[0] ? this.mapTicket(tickets[0]) : undefined,
        satisfaction: tickets[0]?.satisfaction_rating?.score
      }
    };
  }

  private buildCustomFields(ticket: { callData?: any }): { id: number; value: any }[] {
    const fields = [];
    if (ticket.callData?.recordingUrl) {
      fields.push({ id: this.config.customFieldIds.recordingUrl, value: ticket.callData.recordingUrl });
    }
    if (ticket.callData?.summary) {
      fields.push({ id: this.config.customFieldIds.callSummary, value: ticket.callData.summary });
    }
    return fields;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Axios** (MIT) | HTTP client | REST API communication |
| **Zendesk Node** (MIT) | Client | Zendesk API client |
| **BullMQ** (MIT) | Queue | Async ticket processing |

## Production Considerations

**Scaling:** Zendesk rate limits are 700 requests per minute for most plans. Use incremental API exports for batch operations. Implement token bucket rate limiting. Monitor API usage against limits and queue non-urgent operations when limits are constrained.

**Security:** Zendesk API tokens are user-specific — use a dedicated Zendesk user with minimal permissions for the integration. Restrict API token access to the specific API scopes required. Enable Zendesk audit logging for integration actions.

**Monitoring:** Track ticket creation rate, API call volume vs. rate limit, ticket search latency, webhook delivery success rate. Alert on rate limit hits, ticket creation failures, and webhook delivery lag exceeding 5 minutes.
