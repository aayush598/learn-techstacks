# Section 01: Salesforce REST Integration

## Overview

Salesforce REST integration provides the primary API pathway for connecting the voice platform with Salesforce CRM. The Salesforce REST API (version 58.0+) supports comprehensive CRUD operations on standard and custom objects, SOQL and SOSL queries, bulk data operations, Apex REST endpoints, and platform event publishing. The integration adapter wraps the Salesforce REST API behind the common CRM adapter interface, enabling contact synchronization, lead creation, opportunity updates, activity logging, and case management through voice conversations.

The Salesforce adapter must handle Salesforce-specific considerations: API version locking (breaking changes between versions), org-specific customizations (custom fields, custom objects), record type selection, picklist value validation, compound field handling (Address, Name), and Salesforce governor limits (API call limits per org per rolling 24-hour period). The adapter supports both single-record operations (for real-time updates during calls) and bulk operations (for nightly synchronization of large datasets).

## Architecture

```
                    Salesforce REST Integration Architecture

   +------------------+     +------------------+     +------------------+
   | Voice Platform   | --> | Salesforce       | --> | Salesforce      |
   | (Agent Runtime)  |     | Adapter          |     | REST API        |
   +------------------+     +------------------+     +------------------+
                                   |
                                   v
                            +------------------+
                            | Salesforce        |
                            | Connection Pool   |
                            | • OAuth2 tokens   |
                            | • Session mgmt    |
                            | • API version     |
                            +------------------+
                                   |
                                   v
                            +------------------+
                            | Cache Layer       |
                            | • Record cache    |
                            | • Describe cache  |
                            | • SOQL results    |
                            +------------------+
```

## Design Decisions

- **REST API as primary with SOAP fallback:** The REST API is the primary interface due to its simplicity, modern authentication, and JSON format. SOAP API is used as fallback for operations not available in REST (some metadata operations, certain legacy features) and for bulk operations using the SOAP-based Bulk API. Trade-off: maintaining both REST and SOAP implementations doubles adapter code but ensures comprehensive Salesforce coverage.

- **Dynamic describe API caching with auto-refresh:** Salesforce schema varies by org (custom fields, custom objects). The adapter uses Salesforce's Describe API to discover the org-specific schema at integration setup and caches it. The cache auto-refreshes daily or on demand when field mapping validation fails. This enables dynamic field mapping without hardcoding Salesforce field names. Trade-off: describe API calls consume API quota and caching delays schema change propagation.

- **Bulk API 2.0 for large data operations over REST single-record:** For operations involving more than 100 records (list imports, batch contact sync), the adapter switches to Bulk API 2.0 which supports asynchronous job submission and parallel record processing. Bulk API is more efficient for large datasets but adds latency (jobs take seconds to minutes). Trade-off: needing two different API paths adds complexity but is necessary for Salesforce governor limit compliance.

## Implementation Approach

```
class SalesforceRestAdapter extends CRMMAdapter {
  private baseUrl: string;
  private apiVersion: string = 'v58.0';

  constructor(config: SalesforceConfig) {
    super(config);
    this.baseUrl = `${config.instanceUrl}/services/data/${this.apiVersion}`;
  }

  async createContact(contact: ContactData): Promise<AdapterResponse<{ id: string }>> {
    const sfContact = this.mapToSalesforceContact(contact);
    const response = await this.execute({
      method: 'POST',
      url: `${this.baseUrl}/sobjects/Contact`,
      data: sfContact
    });
    return { success: true, data: { id: response.data.id } };
  }

  async searchContacts(query: string): Promise<AdapterResponse<ContactData[]>> {
    const cacheKey = `sf:search:${query}`;
    const cached = await this.cache.get(cacheKey);
    if (cached) return { success: true, data: cached };

    const soql = `SELECT Id, FirstName, LastName, Email, Phone FROM Contact WHERE Name LIKE '%${this.escapeSOQL(query)}%'`;
    const response = await this.execute({
      method: 'GET',
      url: `${this.baseUrl}/query`,
      params: { q: soql }
    });

    const contacts = response.data.records.map(r => this.mapFromSalesforceContact(r));
    await this.cache.set(cacheKey, contacts, 300); // 5-minute cache
    return { success: true, data: contacts };
  }

  async logActivity(contactId: string, activity: ActivityData): Promise<AdapterResponse<void>> {
    const task = {
      WhoId: contactId,
      Subject: activity.subject,
      Description: activity.description,
      ActivityDate: new Date().toISOString().split('T')[0],
      Status: 'Completed',
      CallDurationInSeconds: activity.duration,
      CallDisposition: activity.disposition,
      Type: 'Call'
    };
    await this.execute({
      method: 'POST',
      url: `${this.baseUrl}/sobjects/Task`,
      data: task
    });
    return { success: true, data: undefined };
  }

  private escapeSOQL(value: string): string {
    return value.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **jsforce** (MIT) | Salesforce | Salesforce API client library |
| **Axios** (MIT) | HTTP client | REST API communication |
| **Redis** (BSD) | Cache | Describe API and query caching |

## Production Considerations

**Scaling:** Salesforce imposes API call limits per org (varies by edition, typically 15,000-150,000 API calls per rolling 24 hours). Track API call usage in Redis with rolling window counters. Prioritize real-time call operations (create lead during a sales call) over batch operations (nightly sync) when approaching limits. Implement a queue for non-urgent API calls that can be deferred if limits are constrained.

**Security:** Salesforce connected app credentials are encrypted at rest. Implement IP allowlisting for the voice platform's outgoing IPs. Use the principle of least privilege — the Salesforce connected app should only have permissions for the objects and operations the integration requires. Enable Salesforce event monitoring to audit API usage.

**Monitoring:** Track Salesforce API call volume vs. daily limit, API response times (p50/p95/p99), error rates by error type (timeout, limit exceeded, invalid field, record not found), bulk job completion rates, and cache hit rates for describe and query caches. Alert when API usage exceeds 80% of daily limit and when error rates exceed 5%.
