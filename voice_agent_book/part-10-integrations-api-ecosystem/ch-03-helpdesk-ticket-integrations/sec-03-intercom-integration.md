# Section 03: Intercom Integration

## Overview

Intercom integration connects the voice platform with Intercom's customer communications platform, which combines a CRM, help desk, and messaging platform. Intercom's REST API provides access to contacts, conversations, companies, tags, notes, events, and articles. The adapter enables conversation creation from voice calls, contact enrichment with call data, event tracking for voice interactions, and note attachment to contacts with call summaries.

Intercom's API is distinct from traditional helpdesk platforms in several ways: it uses a conversation model (threaded messaging rather than tickets), contacts are the primary entity (conversations are associated with contacts, not the other way around), and the platform emphasizes real-time messaging. Intercom uses a REST API with GraphQL-like nested resource fetching, OAuth 2.0 authentication (with client credentials grant for server-to-server), and a unique role-based permission model. The adapter must handle Intercom's data model where companies and contacts are loosely associated through an "added_to" relationship.

## Architecture

```
                    Intercom Integration Architecture

   Voice Call → Contact Lookup → Conversation Context → Call Note → Event Log
                                                                        |
                                                                        v
   +-------------------+         +-------------------+         +-------------------+
   | Intercom Adapter  | ------> | Intercom REST API | ------> | Intercom          |
   |                   |         | (v2)              |         | Dashboard         |
   +-------------------+         +-------------------+         +-------------------+
        |                              |
        v                              v
   +-------------------+         +-------------------+
   | Contact Cache     |         | Rate Limiter      |
   | (Redis)           |         | (Sliding window)  |
   +-------------------+         +-------------------+
```

## Design Decisions

- **Event-based voice interaction tracking over conversation creation:** Instead of creating a conversation for every call (which clutters the Inbox), the adapter logs voice calls as Intercom Events ("voice-call-completed", "voice-call-missed") with associated metadata (duration, disposition, campaign name, recording URL). Events appear in the contact timeline without creating Inbox noise. Conversations are only created when the call requires follow-up action. Trade-off: events have less visibility than conversations and may be missed by agents who only monitor the Inbox.

- **Note attachment with AI-generated call summary:** After each call, the adapter creates a contact note (Intercom Note type) containing the AI-generated call summary, key topics, sentiment score, and action items. Notes are visible in the contact's timeline and provide agents with call context when the contact reaches out via other channels. Trade-off: notes can become numerous for frequent callers, requiring periodic cleanup or compression.

- **Webhook-based real-time conversation updates:** Intercom's webhook topics (conversation.created, conversation.admin.replied) notify the platform when conversations are updated. The platform uses these to trigger outbound calls based on conversation activity (e.g., a customer asks a complex question → schedule a voice call). Webhook verification uses Intercom's signed payloads. Trade-off: webhook subscription requires configuring a webhook URL in each Intercom workspace.

## Implementation Approach

```
class IntercomAdapter extends BaseAdapter {
  private baseUrl = 'https://api.intercom.io';

  async findContact(email: string): Promise<AdapterResponse<ContactData | null>> {
    const response = await this.execute({
      method: 'POST', url: `${this.baseUrl}/contacts/search`,
      data: {
        query: { field: 'email', operator: '=', value: email },
        per_page: 1
      }
    });
    const contact = response.data.data?.[0];
    return {
      success: true,
      data: contact ? { id: contact.id, email: contact.email, externalId: contact.external_id } : null
    };
  }

  async createOrUpdateContact(contact: {
    email: string; name: string; phone?: string;
  }): Promise<AdapterResponse<{ id: string }>> {
    const response = await this.execute({
      method: 'POST', url: `${this.baseUrl}/contacts`,
      data: {
        email: contact.email,
        name: contact.name,
        phone: contact.phone || '',
        external_id: contact.email  // Use email as external ID for dedup
      }
    });
    return { success: true, data: { id: response.data.id } };
  }

  async logVoiceEvent(contactId: string, event: {
    type: 'completed' | 'missed' | 'failed' | 'voicemail';
    duration: number; disposition?: string; campaign?: string;
    recordingUrl?: string; summary?: string;
  }): Promise<AdapterResponse<void>> {
    await this.execute({
      method: 'POST', url: `${this.baseUrl}/events`,
      data: {
        event_name: `voice-call-${event.type}`,
        created_at: Math.floor(Date.now() / 1000),
        email: null,  // Use contact_id instead
        contact_id: contactId,
        metadata: {
          duration: event.duration,
          disposition: event.disposition || '',
          campaign: event.campaign || '',
          recording_url: event.recordingUrl || '',
          call_summary: event.summary || ''
        }
      }
    });
    return { success: true, data: undefined };
  }

  async addNote(contactId: string, note: {
    body: string; authorId?: string;
  }): Promise<AdapterResponse<void>> {
    await this.execute({
      method: 'POST', url: `${this.baseUrl}/contacts/${contactId}/notes`,
      data: { body: note.body, admin_id: note.authorId }
    });
    return { success: true, data: undefined };
  }

  async getConversationContext(contactId: string): Promise<AdapterResponse<{
    recentConversations: number; lastConversation?: { subject: string; state: string };
  }>> {
    const response = await this.execute({
      method: 'POST', url: `${this.baseUrl}/conversations/search`,
      data: {
        query: {
          operator: 'AND',
          operands: [
            { field: 'contact_ids', operator: '=', value: contactId },
            { field: 'state', operator: 'IN', value: ['open', 'snoozed'] }
          ]
        },
        per_page: 1
      }
    });
    return {
      success: true,
      data: {
        recentConversations: response.data.total_count,
        lastConversation: response.data.data?.[0] ? {
          subject: response.data.data[0].title,
          state: response.data.data[0].state
        } : undefined
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

**Scaling:** Intercom rate limits are 1000 requests/minute for most plans. Event ingestion has separate, higher limits. Use batch event submission (up to 500 events per request) for high-volume call logging. Intercom's search API is more expensive (5x rate limit cost) — cache search results aggressively.

**Security:** Intercom access tokens should be scoped to the minimum required resources (contacts, conversations, events). Use separate tokens for read and write operations.Enable Intercom's IP restriction for API access. Implement webhook signature verification using Intercom's signing secret.

**Monitoring:** Track event logging throughput, contact search latency, note creation rate, API utilization vs. limits. Alert on event submission failures (these are often silently dropped if invalid), contact search failures, and authentication token expiry.
