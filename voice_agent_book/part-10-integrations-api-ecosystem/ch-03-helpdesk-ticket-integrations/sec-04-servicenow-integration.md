# Section 04: ServiceNow Integration

## Overview

ServiceNow integration connects the voice platform with ServiceNow's IT Service Management (ITSM) and Customer Service Management (CSM) platforms. ServiceNow provides REST APIs for incidents, service requests, change requests, problems, users, and configuration items (CI). The adapter enables incident creation from voice calls, CI lookup for screen pop, service request fulfillment, ticket status updates with call context, and knowledge base article retrieval for agent assistance.

ServiceNow's integration is more complex than most helpdesk platforms due to its highly configurable nature. Each ServiceNow instance has custom tables, fields, business rules, client scripts, ACLs (Access Control Lists), and workflows. The adapter must dynamically discover the instance's schema (tables, fields, choice lists) and respect ACL restrictions. ServiceNow also uses a unique sys_id (globally unique 32-character hex string) for record identification and supports both REST Table API and REST Aggregate API for different query patterns.

## Architecture

```
                    ServiceNow Integration Architecture

   Voice Call → CI Lookup → Incident Check → Call Handling → Incident Update/Add Work Note
                                                                        |
                                                                        v
   +-------------------+         +-------------------+         +-------------------+
   | ServiceNow        | ------> | ServiceNow REST   | ------> | ServiceNow        |
   | Adapter           |         | API (Table API)   |         | Portal            |
   +-------------------+         +-------------------+         +-------------------+
        |                              |
        v                              v
   +-------------------+         +-------------------+
   | Schema Cache      |         | Rate Limiter      |
   | (Table definitions,|         | (Instance-level)  |
   |  Field metadata)  |         |                   |
   +-------------------+         +-------------------+
```

## Design Decisions

- **Dynamic schema discovery with caching:** ServiceNow instances have unique table and field configurations. The adapter uses the REST API's `/now/doc/rest/resource` schema endpoint (or Table API's `sys_dictionary` table) to discover available tables and fields at setup time. The schema is cached and refreshed daily or on demand. This eliminates hardcoded field references and adapts to each instance's customizations. Trade-off: schema discovery adds initial setup time (10-30 seconds) and API calls.

- **Work note creation for call context over incident description updates:** Call details (summary, recording URL, duration, sentiment) are added as work notes (internal, not visible to end users) rather than updating the incident description. This preserves the original incident description for end users while providing agents with full call context in the work notes. Trade-off: work notes can become verbose for calls with multiple interactions.

- **Configuration Item (CI) lookup for context enrichment:** When a customer calls about an IT issue, the adapter looks up the relevant CI (computer, application, network device) based on caller information or call context. CI details (owner, status, support group, last maintenance) are provided to the voice agent for context. If the CI has an active incident, that incident's status is also retrieved. Trade-off: CI lookup requires integration with ServiceNow's CMDB, which may have data quality issues.

## Implementation Approach

```
class ServiceNowAdapter extends BaseAdapter {
  private baseUrl: string;
  private tableSchema: Map<string, TableSchema>;

  constructor(config: ServiceNowConfig) {
    super(config);
    this.baseUrl = `${config.instanceUrl}/api/now`;
  }

  async initialize() {
    this.tableSchema = await this.discoverSchema();
  }

  async createIncident(incident: {
    shortDescription: string; description: string;
    callerId?: string; category?: string; impact?: number; urgency?: number;
    callData?: { recordingUrl?: string; duration?: number; summary?: string };
  }): Promise<AdapterResponse<{ id: string; number: string }>> {
    const snIncident = {
      short_description: incident.shortDescription,
      description: incident.description,
      caller_id: incident.callerId,
      category: incident.category || 'software',
      impact: incident.impact || 3,
      urgency: incident.urgency || 3,
      contact_type: 'phone',
      ...incident.callData ? {} : {}
    };

    const response = await this.execute({
      method: 'POST', url: `${this.baseUrl}/table/incident`,
      data: snIncident
    });

    const sysId = response.data.result.sys_id;

    // Add call context as work note
    if (incident.callData?.summary) {
      await this.addWorkNote(sysId, `Call Summary (Voice Agent): ${incident.callData.summary}`);
    }

    return {
      success: true,
      data: { id: sysId, number: response.data.result.number }
    };
  }

  async addWorkNote(incidentId: string, note: string): Promise<AdapterResponse<void>> {
    await this.execute({
      method: 'PUT', url: `${this.baseUrl}/table/incident/${incidentId}`,
      data: { work_notes: note }
    });
    return { success: true, data: undefined };
  }

  async lookupCI(query: string): Promise<AdapterResponse<CIData[]>> {
    const response = await this.execute({
      method: 'GET', url: `${this.baseUrl}/table/cmdb_ci`,
      params: {
        sysparm_query: `nameLIKE${query}^ORsys_class_nameLIKE${query}`,
        sysparm_limit: 10,
        sysparm_fields: 'sys_id,name,sys_class_name,operational_status,assigned_to'
      }
    });
    return { success: true, data: response.data.result.map(this.mapCI) };
  }

  async getActiveIncidents(callerId: string): Promise<AdapterResponse<any[]>> {
    const response = await this.execute({
      method: 'GET', url: `${this.baseUrl}/table/incident`,
      params: {
        sysparm_query: `caller_id=${callerId}^stateIN1,2,3`,
        sysparm_fields: 'sys_id,number,short_description,state,priority',
        sysparm_limit: 10
      }
    });
    return { success: true, data: response.data.result.map(i => ({
      sysId: i.sys_id, number: i.number, description: i.short_description,
      state: i.state, priority: i.priority
    })) };
  }

  private async discoverSchema(): Promise<Map<string, TableSchema>> {
    const tables = ['incident', 'cmdb_ci', 'sys_user', 'sc_request', 'problem'];
    const schema = new Map();
    for (const table of tables) {
      const response = await this.execute({
        method: 'GET', url: `${this.baseUrl}/table/sys_dictionary`,
        params: { sysparm_query: `name=${table}`, sysparm_limit: 100 }
      });
      schema.set(table, { name: table, fields: response.data.result.map(f => ({
        name: f.element, label: f.column_label, type: f.internal_type, mandatory: f.mandatory === 'true'
      })) });
    }
    return schema;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Axios** (MIT) | HTTP client | REST API communication |
| **Redis** (BSD) | Cache | Schema and query result cache |

## Production Considerations

**Scaling:** ServiceNow instances have API rate limits that vary (typically 100-500 requests/minute depending on edition). Use the ServiceNow REST API Explorer to discover limits. Implement request batching using ServiceNow's Batch API (POST /api/now/batch) for multiple operations. Cache schema and configuration item data aggressively to reduce API calls.

**Security:** ServiceNow credentials should use a dedicated integration user with roles limited to the specific tables and operations required (incident creation, CI read). Use basic authentication with password or OAuth with JWT. Restrict access by IP address. Enable ServiceNow audit logging for integration actions.

**Monitoring:** Track incident creation rate, API call volume vs. limits, CI lookup latency and cache hit rate, schema cache freshness, and error distribution. Alert on rate limit hits, incident creation failures, and schema discovery failures (may indicate ServiceNow instance changes).
