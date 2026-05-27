# Section 04: Zoho CRM Integration

## Overview

Zoho CRM integration connects the voice platform with Zoho CRM, a popular CRM platform with strong presence in small-to-medium businesses. Zoho provides REST APIs covering modules (their term for objects) including Leads, Contacts, Accounts, Deals, Activities (calls, tasks, events), Notes, Attachments, and custom modules. Zoho's API uses OAuth 2.0 authentication with a unique grant flow that requires a refresh token with specific scope.

Zoho CRM has several unique characteristics that the adapter must handle: module-specific field naming (field API names vary by Zoho CRM edition), territory management (record access based on organizational hierarchy), layout and validation rules (field requirements enforced server-side), mass update triggers (single API call can update related records), and Zoho's proprietary "blueprint" workflow (state-machine-based business processes). The adapter must also handle Zoho's rate limiting which is more restrictive than Salesforce or HubSpot (varying by plan, typically 250-1000 requests per minute per API token).

## Architecture

```
                    Zoho CRM Integration Architecture

   +------------------+     +------------------+     +------------------+
   | Voice Platform   | --> | Zoho CRM         | --> | Zoho REST API    |
   | (Agent Runtime)  |     | Adapter          |     | (zohoapis.com)   |
   +------------------+     +------------------+     +------------------+
                                   |
                                   v
                            +------------------+
                            | Module Registry  |
                            | • Lead           |
                            | • Contact        |
                            | • Account        |
                            | • Deal           |
                            | • Custom modules |
                            +------------------+
                                   |
                                   v
                            +------------------+
                            | Field Mapping    |
                            | • Field API names|
                            | • Picklist values|
                            | • Layout access  |
                            +------------------+
```

## Design Decisions

- **Module-aware adapter with dynamic field discovery:** Zoho CRM editions (Standard, Professional, Enterprise, CRM Plus) expose different modules and fields. The adapter uses Zoho's Module API (GET /settings/modules) to discover available modules and fields at setup time, then caches this schema. This enables the adapter to work across Zoho editions without code changes. Trade-off: module discovery consumes API calls and requires periodic cache refresh.

- **Bulk API for large operations:** Zoho's Bulk API (v2/bulk-read) supports reading up to 100,000 records and Bulk Write (v2/bulk-write) supports creating/updating up to 10,000 records per job. The adapter uses Bulk API for contact list import (uploading lists from campaigns to Zoho) and nightly synchronization. Single-record API (v2/{module}) is used for real-time operations during calls. Trade-off: Bulk API introduces 5-15 minute processing latency but handles volume efficiently.

- **Trigger and workflow bypass for record operations:** Zoho CRM has workflows, validation rules, and assignment rules that trigger on record create/update. For bulk synchronization operations, the adapter uses the "trigger" parameter set to "workflow" (to fire workflows) or omits it (to bypass). By default, record operations from voice agent conversations trigger workflows (sending notification emails), while bulk sync operations bypass them to avoid notification storms. Trade-off: bypassing workflows may miss important automation but prevents duplicate notifications during sync.

## Implementation Approach

```
class ZohoCRMAdapter extends CRMMAdapter {
  private baseUrl = 'https://www.zohoapis.com/crm/v7';
  private moduleCache: Map<string, ModuleSchema>;

  async initialize() {
    const modules = await this.getModules();
    for (const module of modules) {
      const fields = await this.getModuleFields(module.api_name);
      this.moduleCache.set(module.api_name, { ...module, fields });
    }
  }

  async createContact(contact: ContactData): Promise<AdapterResponse<{ id: string }>> {
    const zohoContact = this.mapToZohoContact(contact);
    const response = await this.execute({
      method: 'POST',
      url: `${this.baseUrl}/Contacts`,
      data: { data: [zohoContact] },
      params: { trigger: 'workflow' }  // Fire workflows for voice-created contacts
    });

    if (response.data.data?.[0]?.status === 'error') {
      const error = response.data.data[0];
      if (error.code === 'DUPLICATE_DATA') {
        // Merge with existing contact
        return this.handleDuplicateContact(error, contact);
      }
      throw new ZohoError(error);
    }
    return { success: true, data: { id: response.data.data[0].details.id } };
  }

  async logCallActivity(contactId: string, callData: {
    subject: string; duration: number; disposition: string;
    recordingUrl?: string; agentName?: string;
  }): Promise<AdapterResponse<void>> {
    const activity = {
      Subject: callData.subject,
      Call_Type: 'Outbound',
      Call_Start_Time: new Date().toISOString(),
      Call_Duration: String(Math.round(callData.duration)),
      Call_Status: callData.disposition,
      Who_Id: contactId,  // Contact or Lead ID
      Description: `Call handled by ${callData.agentName || 'Voice Agent'}\nRecording: ${callData.recordingUrl || 'N/A'}`
    };

    await this.execute({
      method: 'POST',
      url: `${this.baseUrl}/Calls`,
      data: { data: [activity] }
    });
    return { success: true, data: undefined };
  }

  private async getModules(): Promise<any[]> {
    const response = await this.execute({ method: 'GET', url: `${this.baseUrl}/settings/modules` });
    return response.data.modules;
  }

  private async getModuleFields(moduleName: string): Promise<any[]> {
    const response = await this.execute({
      method: 'GET', url: `${this.baseUrl}/settings/fields?module=${moduleName}`
    });
    return response.data.fields;
  }

  private mapToZohoContact(contact: ContactData): Record<string, any> {
    return {
      First_Name: contact.firstName,
      Last_Name: contact.lastName,
      Email: contact.email || '',
      Phone: contact.phone || '',
      Lead_Source: 'Voice Call',
      ...contact.customFields
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Axios** (MIT) | HTTP client | REST API communication |
| **Redis** (BSD) | Cache | Module and field schema cache |
| **Zod** (MIT) | Validation | API response validation |

## Production Considerations

**Scaling:** Zoho rate limits are per-token (typically 250-1000 req/min). Multiple tenants sharing the same Zoho org token share this limit. Implement adaptive rate limiting based on Zoho's X-RATELIMIT-* response headers. For bulk operations, use Zoho's Bulk API which has separate, higher limits. Monitor API token usage and alert approaching limits.

**Security:** Zoho OAuth2 tokens are valid for 1 hour (access token) with a refresh token that expires after a configurable period (typically 30 days for self-client, does not expire for authorized application). Implement refresh token rotation and secure storage of client credentials. Use Zoho's China endpoint (zohoapis.com.cn) for tenants in China.

**Monitoring:** Track API call volume by module, rate limit utilization, synchronization latency for bulk jobs, field schema cache freshness, and OAuth token refresh success rate. Alert on bulk job failures, rate limit exhaustion, and schema changes that require field mapping updates.
