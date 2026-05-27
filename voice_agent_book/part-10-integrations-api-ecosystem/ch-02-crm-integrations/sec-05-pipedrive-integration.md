# Section 05: Pipedrive Integration

## Overview

Pipedrive integration connects the voice platform with Pipedrive, a sales-focused CRM built around a visual sales pipeline. Pipedrive's REST API provides access to deals, persons (contacts), organizations (companies), activities (calls, meetings, tasks), notes, pipelines, stages, products, and custom fields. Pipedrive's data model is deal-centric — the core workflow revolves around moving deals through pipeline stages. The adapter supports creating and updating persons and deals from voice conversations, logging call activities against persons and deals, updating deal stages based on call outcomes, and retrieving deal context for agent screen-pops.

Pipedrive's API design emphasizes simplicity: all endpoints use JSON, authentication is via API token (optional OAuth2), rate limits are generous (200 requests per minute per organization), and the data model is flatter than Salesforce. Unique characteristics include mandatory deal title (no auto-generation), strict person-organization relationship, activity type configuration (custom activity types), note threading, and Pipedrive's custom field system which requires knowing field keys (strings like "field_hash") rather than names.

## Architecture

```
                    Pipedrive Integration Architecture

   +------------------+     +------------------+     +------------------+
   | Voice Platform   | --> | Pipedrive        | --> | Pipedrive REST   |
   | (Agent Runtime)  |     | Adapter          |     | API (v1)         |
   +------------------+     +------------------+     +------------------+
                                   |
                                   v
                            +------------------+
                            | Pipedrive        |
                            | Entities:        |
                            | • Persons        |
                            | • Organizations  |
                            | • Deals          |
                            | • Activities     |
                            | • Notes          |
                            +------------------+
                                   |
                                   v
                            +------------------+
                            | Pipeline Mapper  |
                            | • Stage lookup   |
                            | • Deal movement  |
                            | • Activity types |
                            +------------------+
```

## Design Decisions

- **Deal creation from voice calls with pipeline stage assignment:** When a voice conversation identifies a sales opportunity, the adapter creates a new deal in Pipedrive and assigns it to the appropriate pipeline stage. Pipeline and stage identification is configurable — either specified at integration setup (all calls create deals in the same pipeline) or dynamically determined by call context (campaign, product interest, contact industry). Trade-off: dynamic pipeline assignment requires richer call context extraction but enables more accurate pipeline management.

- **Activity logging with call recordings as notes:** Call activities are created with type "call" and linked to the person and (if applicable) deal. Call recordings are attached as Pipedrive notes with the recording URL and a brief transcript summary. Pipedrive notes support rich text and file links, enabling embedding call details directly in the CRM timeline. Trade-off: storing recording URLs rather than actual files avoids file size limits but requires the user to navigate to the voice platform to listen.

- **Webhook-based deal stage change detection for outbound trigger:** Pipedrive webhooks notify the platform when deal stages change. The platform can trigger follow-up actions based on stage changes: if a deal moves to "Negotiation," schedule a follow-up call; if a deal is "Won," trigger a satisfaction survey campaign. This enables CRM-driven call scheduling. Trade-off: webhook processing requires maintaining deal-to-contact mappings and handling webhook delivery guarantees.

## Implementation Approach

```
class PipedriveAdapter extends CRMMAdapter {
  private baseUrl = 'https://api.pipedrive.com/v1';

  async findPersonByPhone(phone: string): Promise<AdapterResponse<PersonData | null>> {
    const response = await this.execute({
      method: 'GET',
      url: `${this.baseUrl}/persons/search`,
      params: { term: phone, fields: 'phone', exact_match: true }
    });
    const person = response.data.data?.items?.[0]?.item;
    return {
      success: true,
      data: person ? this.mapFromPipedrivePerson(person) : null
    };
  }

  async createPerson(person: PersonData): Promise<AdapterResponse<{ id: string }>> {
    const pipedrivePerson = {
      name: `${person.firstName} ${person.lastName}`.trim(),
      email: person.email ? [{ value: person.email, primary: true }] : [],
      phone: person.phone ? [{ value: person.phone, primary: true }] : [],
      ...person.customFields
    };
    const response = await this.execute({
      method: 'POST', url: `${this.baseUrl}/persons`,
      data: pipedrivePerson
    });
    return { success: true, data: { id: String(response.data.data.id) } };
  }

  async logCallActivity(personId: string, callData: {
    duration: number; disposition: string; dealId?: string;
    recordingUrl?: string; summary?: string;
  }): Promise<AdapterResponse<void>> {
    const activity = {
      subject: `Outbound Call - ${callData.disposition}`,
      type: 'call',
      done: true,
      person_id: Number(personId),
      deal_id: callData.dealId ? Number(callData.dealId) : undefined,
      note: callData.summary || '',
      duration: String(Math.round(callData.duration)),
      public_description: `Call duration: ${Math.round(callData.duration)}s\nRecording: ${callData.recordingUrl || 'N/A'}`
    };
    await this.execute({
      method: 'POST', url: `${this.baseUrl}/activities`,
      data: activity
    });
    return { success: true, data: undefined };
  }

  async updateDealStage(dealId: string, stageId: string): Promise<AdapterResponse<void>> {
    await this.execute({
      method: 'PUT',
      url: `${this.baseUrl}/deals/${dealId}`,
      data: { stage_id: Number(stageId) }
    });
    return { success: true, data: undefined };
  }

  async getDealContext(dealId: string): Promise<AdapterResponse<DealContext>> {
    const response = await this.execute({
      method: 'GET', url: `${this.baseUrl}/deals/${dealId}`
    });
    return { success: true, data: response.data.data };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Axios** (MIT) | HTTP client | REST API communication |
| **Redis** (BSD) | Cache | Search result caching |
| **Webhook** (Node.js) | Listeners | Webhook processing |

## Production Considerations

**Scaling:** Pipedrive rate limits are 200 requests/minute per organization. This is sufficient for most voice platform workloads but can be tight during peak dialing. Cache person search results aggressively (same contact may be searched multiple times during retry cycles). Use Pipedrive's bulk endpoints (POST /v1/bulk) for operations involving many records.

**Security:** Pipedrive API tokens provide full access to the organization. Implement token scoping by using Pipedrive's API key restrictions (if available) or by creating a dedicated voice platform user with limited permissions. Monitor for unusual API access patterns that could indicate token compromise.

**Monitoring:** Track API call volume vs. rate limit, person search cache hit rate, deal creation rate, activity logging latency, and webhook processing success rate. Alert on rate limit hits, person search failures (may indicate connection issues), and webhook processing lag exceeding 5 minutes.
