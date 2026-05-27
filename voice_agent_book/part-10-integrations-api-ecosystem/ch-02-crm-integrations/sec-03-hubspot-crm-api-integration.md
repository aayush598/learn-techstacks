# Section 03: HubSpot CRM API Integration

## Overview

HubSpot CRM API integration connects the voice platform with HubSpot's marketing, sales, and service hub. HubSpot provides REST APIs for contacts, companies, deals, engagements (calls, emails, meetings), notes, tasks, and custom objects. The HubSpot adapter enables outbound call management within HubSpot's contact timeline, automatic logging of call activities, deal stage updates based on call outcomes, contact property enrichment from voice conversations, and workflow trigger integration.

HubSpot's API differs significantly from Salesforce's in several ways: all communication is REST-only (no SOAP), API versioning is handled through scopes rather than versioned endpoints, rate limits are per-app rather than per-org, properties are dynamic (created through the app rather than through HubSpot's UI), and HubSpot enforces a "magic" CRM model where contacts, companies, and deals are loosely associated. The adapter must handle HubSpot's unique association model where objects are linked through association labels rather than foreign keys.

## Architecture

```
                    HubSpot CRM API Integration

   +------------------+     +------------------+     +------------------+
   | Voice Platform   | --> | HubSpot          | --> | HubSpot REST     |
   | (Agent Runtime)  |     | Adapter          |     | API              |
   +------------------+     +------------------+     +------------------+
                                   |
                                   v
                            +------------------+
                            | HubSpot Objects: |
                            | • Contacts       |
                            | • Companies      |
                            | • Deals          |
                            | • Engagements    |
                            | • Notes          |
                            +------------------+
                                   |
                                   v
                            +------------------+
                            | Association Mgr  |
                            | • Contact↔Deal  |
                            | • Company↔Deal  |
                            | • Custom assoc   |
                            +------------------+
```

## Design Decisions

- **Custom property creation on integration setup:** HubSpot allows creating custom contact, company, and deal properties through the API. On first integration setup, the adapter auto-creates required voice-specific properties (lastCallDate, callDisposition, voiceSentiment, preferredContactTime, optOutVoice). These properties are then available for contact enrichment and list segmentation. Trade-off: auto-creating properties requires the API scope for property management and may create unused properties if the integration is later disabled.

- **Engagement-based call logging with call disposition properties:** HubSpot's Engagement API is used to log calls with start/end times, duration, disposition, and notes. The adapter extends the standard call engagement with voice-specific properties (agent name, call recording URL, sentiment score, campaign name) stored in HubSpot custom properties. This creates a rich call history within HubSpot's contact timeline. Trade-off: storing extensive call metadata in HubSpot properties may approach property value size limits.

- **Webhook-based real-time updates over polling:** HubSpot's webhook subscriptions (part of the App Marketplace) deliver real-time notifications when contacts, deals, or custom objects change. The adapter registers webhooks for relevant object changes (contact updated, deal stage changed) and processes them to update the platform's local contact state. This avoids API polling and reduces API call volume. Trade-off: webhook delivery has no retry guarantee — if the platform is down, webhook events may be lost.

## Implementation Approach

```
class HubSpotAdapter extends CRMMAdapter {
  private baseUrl = 'https://api.hubapi.com';

  async createContact(contact: ContactData): Promise<AdapterResponse<{ id: string }>> {
    const hubspotContact = this.buildContactProperties(contact);
    try {
      const response = await this.execute({
        method: 'POST',
        url: `${this.baseUrl}/crm/v3/objects/contacts`,
        data: { properties: hubspotContact }
      });
      return { success: true, data: { id: response.data.id } };
    } catch (error) {
      // Handle duplicate contact (matched by email)
      if (error.response?.status === 409) {
        const existingId = error.response.data.message.match(/Existing ID: (\d+)/)?.[1];
        if (existingId) return this.updateContact(existingId, contact);
      }
      throw error;
    }
  }

  async logCall(callData: {
    contactId: string; duration: number; disposition: string;
    recordingUrl?: string; sentiment?: number; agentName?: string;
  }): Promise<AdapterResponse<void>> {
    const engagement = {
      properties: {
        hs_timestamp: new Date().toISOString(),
        hs_call_body: `Call handled by ${callData.agentName || 'Voice Agent'}`,
        hs_call_duration: String(Math.round(callData.duration * 1000)),
        hs_call_from_number: 'Voice Platform',
        hs_call_status: 'COMPLETED',
        hs_call_recording_url: callData.recordingUrl || '',
        hs_call_disposition: callData.disposition,
        hs_call_to_number: ''
      }
    };

    const response = await this.execute({
      method: 'POST',
      url: `${this.baseUrl}/crm/v3/objects/calls`,
      data: engagement
    });

    // Associate call with contact
    await this.createAssociation(
      response.data.id, 'calls', callData.contactId, 'contacts', 'call_to_contact'
    );
    return { success: true, data: undefined };
  }

  private buildContactProperties(contact: ContactData): Record<string, string> {
    return {
      firstname: contact.firstName,
      lastname: contact.lastName,
      email: contact.email || '',
      phone: contact.phone || '',
      hs_lead_status: 'NEW',
      ...contact.customFields
    };
  }

  async createAssociation(
    sourceId: string, sourceType: string,
    targetId: string, targetType: string, associationType: string
  ): Promise<void> {
    await this.execute({
      method: 'PUT',
      url: `${this.baseUrl}/crm/v4/objects/${sourceType}/${sourceId}/associations/default/${targetType}/${targetId}`
    });
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Axios** (MIT) | HTTP client | REST API communication |
| **Redis** (BSD) | Cache | Token and property cache |
| **Zod** (MIT) | Validation | Response schema validation |

## Production Considerations

**Scaling:** HubSpot API rate limits are per-app (100 requests per 10 seconds by default, up to 300 with higher volume tier). Use a token bucket rate limiter per tenant to stay within limits. Batch property creation requests. The search API (POST /crm/v3/objects/{object}/search) is more efficient than individual lookups for batch operations. Use webhook event batching to reduce per-event processing overhead.

**Security:** HubSpot API keys (private app access tokens) are encrypted at rest. Use OAuth 2.0 for multi-tenant marketplace apps where each HubSpot org installs the integration. The OAuth flow requires a redirect URI and handles authorization code exchange. Store refresh tokens for automatic token renewal.

**Monitoring:** Track API call volume by endpoint, rate limit hits (429 responses), webhook delivery success rate, association creation success rate, and contact creation/update latency. Alert on rate limit hits exceeding 5% of total calls, webhook delivery failures, and OAuth token refresh failures.
