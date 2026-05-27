# Section 02: Freshdesk Integration

## Overview

Freshdesk integration connects the voice platform with Freshworks' customer support platform. Freshdesk provides REST APIs for tickets, contacts, companies, agents, groups, canned responses, solutions, and customer satisfaction ratings. The adapter enables ticket creation from voice calls, contact lookup for screen pop, ticket status updates, conversation logging, and CSAT data retrieval.

Freshdesk's API design differs from Zendesk: tickets can have multiple "type" classifications (Question, Problem, Feature Request), contacts are distinct from users (more like a CRM contact model), and the API uses numeric IDs with domain-specific prefixes. Freshdesk also has a unique "conversation" model where ticket updates are threaded conversations rather than linear comments. The adapter must handle Freshdesk's email integration (tickets can be created by email, requiring deduplication) and marketplace app framework for deeper integration.

## Architecture

```
                    Freshdesk Integration Architecture

   Voice Call → Contact Lookup → Ticket Context → Call Handling → Ticket Update
                                                                        |
                                                                        v
   +-------------------+         +-------------------+         +-------------------+
   | Freshdesk Adapter | ------> | Freshdesk API v2  | ------> | Freshdesk         |
   |                   |         |                   |         | Dashboard         |
   +-------------------+         +-------------------+         +-------------------+
        |                              |
        v                              v
   +-------------------+         +-------------------+
   | Contact Cache     |         | Rate Limiter      |
   | (Redis)           |         | (Token bucket)    |
   +-------------------+         +-------------------+
```

## Design Decisions

- **Conversation-based ticket updates over single-body updates:** Freshdesk's conversation model treats each ticket update as a separate conversation entry. The adapter adds voice call transcripts and summaries as private conversations (visible to agents only), preserving the ticket's public thread for customer-facing updates. This provides agents with full call context without exposing it to the customer. Trade-off: multiple private conversations can clutter the ticket if not managed carefully.

- **Contact-first lookup strategy:** Before any ticket operation, the adapter looks up the contact by phone number or email in Freshdesk. If the contact exists, their tickets and custom fields are cached for the call duration. If not, a new contact is created. This ensures consistent contact identity across ticket operations. Trade-off: contact lookup adds 50-200ms latency before ticket operations begin.

- **Freshdesk marketplace app for custom call logging fields:** The adapter uses Freshdesk's marketplace app framework to add custom fields to the ticket interface (call recording URL, call duration, voice agent name). The app is installed per-Freshdesk instance and configured with the integration's webhook URL for real-time notifications. Trade-off: marketplace app installation requires manual setup in each Freshdesk instance.

## Implementation Approach

```
class FreshdeskAdapter extends BaseAdapter {
  private baseUrl: string;

  constructor(config: FreshdeskConfig) {
    super(config);
    this.baseUrl = `https://${config.subdomain}.freshdesk.com/api/v2`;
  }

  async findContact(emailOrPhone: string): Promise<AdapterResponse<Contact | null>> {
    const cacheKey = `fd:contact:${emailOrPhone}`;
    const cached = await this.cache.get(cacheKey);
    if (cached) return { success: true, data: JSON.parse(cached) };

    const response = await this.execute({
      method: 'GET', url: `${this.baseUrl}/search/contacts`,
      params: { query: `email:"${emailOrPhone}" OR phone:"${emailOrPhone}"` }
    });

    const contact = response.data.results?.[0] || null;
    if (contact) await this.cache.set(cacheKey, JSON.stringify(contact), 300);
    return { success: true, data: contact ? this.mapContact(contact) : null };
  }

  async createTicket(ticket: {
    subject: string; description: string; contactId: number;
    priority?: number; status?: number; type?: string;
    callData?: { recordingUrl?: string; duration?: number };
  }): Promise<AdapterResponse<{ id: string }>> {
    const freshdeskTicket = {
      subject: ticket.subject,
      description: ticket.description,
      requester_id: ticket.contactId,
      priority: ticket.priority || 2,    // Medium
      status: ticket.status || 2,         // Open
      type: ticket.type || 'Problem',
      custom_fields: {
        cf_call_recording_url: ticket.callData?.recordingUrl || '',
        cf_call_duration: String(ticket.callData?.duration || 0)
      },
      tags: ['voice_call'],
      source: 1  // Phone
    };

    const response = await this.execute({
      method: 'POST', url: `${this.baseUrl}/tickets`,
      data: freshdeskTicket
    });
    return { success: true, data: { id: String(response.data.id) } };
  }

  async addConversation(ticketId: string, conversation: {
    body: string; isPrivate: boolean; userId?: number;
  }): Promise<AdapterResponse<void>> {
    await this.execute({
      method: 'POST', url: `${this.baseUrl}/tickets/${ticketId}/conversations`,
      data: {
        body: conversation.body,
        private: conversation.isPrivate,
        user_id: conversation.userId
      }
    });
    return { success: true, data: undefined };
  }

  async getTicketContext(contactId: number): Promise<AdapterResponse<{
    openTickets: number; recentTickets: any[];
  }>> {
    const response = await this.execute({
      method: 'GET', url: `${this.baseUrl}/tickets`,
      params: { requester_id: contactId, per_page: 5 }
    });
    return {
      success: true,
      data: {
        openTickets: response.data.filter(t => t.status < 4).length,
        recentTickets: response.data.slice(0, 3).map(t => ({
          id: t.id, subject: t.subject, status: t.status, priority: t.priority
        }))
      }
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Axios** (MIT) | HTTP client | REST API communication |
| **Redis** (BSD) | Cache | Contact search caching |

## Production Considerations

**Scaling:** Freshdesk rate limits vary by plan (typically 50-200 requests/minute). Implement aggressive caching of contact lookups (cached for 5-15 minutes). Use Freshdesk's bulk API (v2/bulk_tickets) for batch ticket creation during list imports. Monitor API usage and implement queue-based processing during peak hours.

**Security:** Freshdesk API keys are admin-level — use a dedicated agent account with minimal role for the integration. Restrict API key IP access to the voice platform's IP range. Enable Freshdesk audit logs to track integration actions.

**Monitoring:** Track ticket creation velocity, contact search cache hit rate, conversation add latency, API utilization vs. limits, and error rate by error type. Alert on rate limit hits, ticket creation failures, and contact search failures (may indicate Freshdesk connectivity issues).
