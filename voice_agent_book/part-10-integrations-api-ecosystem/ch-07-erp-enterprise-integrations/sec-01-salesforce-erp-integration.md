# Section 01: Salesforce ERP Integration

## Overview

The Salesforce ERP integration enables voice agents to interact with Salesforce's business applications, including Sales Cloud, Service Cloud, Financial Services Cloud, and Revenue Cloud. This adapter allows voice agents to look up accounts and contacts, create opportunities from sales calls, log activities against records, check case status, and process orders. The integration uses Salesforce's comprehensive REST API suite and the Bulk API 2.0 for high-volume data synchronization.

The adapter implements the Enterprise Salesforce data model, supporting standard objects (Account, Contact, Opportunity, Case, Order, Product) and custom objects through a dynamic schema discovery mechanism. The integration handles Salesforce's complex permission model (profiles, permission sets, sharing rules), field-level security, and record type assignment. It also supports Salesforce's duplicate management rules that prevent duplicate record creation during voice-triggered data entry.

## Architecture

```
                Salesforce ERP Integration

   Voice Agent ←→ ERP Gateway ←→ Salesforce Adapter ←→ Salesforce
                                                              |
   +----------------------------------------------------------+
   |              Salesforce Adapter Components               |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Auth & Session   |  | REST API Client   |            |
   |  | • OAuth2 JWT     |  | • CRUD operations  |           |
   |  | • Token refresh  |  | • SOQL queries     |           |
   |  | • Session pool   |  | • SOSL search      |           |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Bulk API 2.0     |  | Metadata API      |            |
   |  | • Large jobs     |  | • Object describe  |            |
   |  | • CSV/JSON       |  | • Field discovery  |            |
   |  | • Callback       |  | • Picklist values  |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **JWT Bearer OAuth2 flow over username-password auth:** Salesforce JWT Bearer Token flow enables server-to-server authentication without user interaction. The integration uses a Connected App with a certificate-based private key JWT assertion to obtain an access token. Tokens are cached and refreshed automatically. Trade-off: JWT setup requires certificate management and Connected App configuration but provides the most secure and reliable server-to-server authentication.

- **Dynamic schema discovery over hard-coded object models:** On initialization, the adapter queries Salesforce Metadata API and Tooling API to discover object schemas, field definitions, relationship names, and picklist values. These schemas are cached for 24 hours and used to dynamically generate SOQL queries and map platform fields to Salesforce fields. Trade-off: schema discovery adds startup latency and cache maintenance but eliminates hard-coded field mappings and automatically adapts to Salesforce schema changes.

- **Composite API for multi-record operations over individual calls:** When the voice agent creates an account, contact, and opportunity in a single call flow, the adapter uses Salesforce's Composite API to batch these operations in a single HTTP request with internal reference chaining (e.g., using the auto-generated account ID as the AccountId for the contact). Trade-off: Composite API requests are more complex to construct but reduce round trips from N to 1 and provide transactional consistency within the composite boundary.

## Implementation Approach

```
interface SalesforceAdapterConfig {
  instanceUrl: string;
  clientId: string;
  clientSecret: string;
  privateKey: string;
  username: string;
  apiVersion?: string;
}

interface SObjectRecord {
  Id?: string;
  attributes?: { type: string; url?: string };
  [field: string]: any;
}

class SalesforceERPAdapter extends BaseERPAdapter {
  private auth: SalesforceAuth;
  private restClient: AxiosInstance;
  private schemaCache = new Map<string, ObjectSchema>();

  constructor(config: SalesforceAdapterConfig) {
    super(config);
    this.auth = new SalesforceAuth({
      clientId: config.clientId,
      privateKey: config.privateKey,
      username: config.username,
      instanceUrl: config.instanceUrl,
      apiVersion: config.apiVersion || 'v60.0',
    });
    this.restClient = Axios.create({ timeout: 30000 });
  }

  async connect(): Promise<void> {
    const token = await this.auth.obtainToken();
    this.restClient.defaults.headers['Authorization'] = `Bearer ${token.accessToken}`;
    this.restClient.defaults.baseURL = `${token.instanceUrl}/services/data/${this.auth.apiVersion}/`;
  }

  async startOpportunityFromCall(params: {
    accountName: string;
    contactEmail?: string;
    productInterest: string;
    estimatedValue: number;
    callSid: string;
  }): Promise<AdapterResponse<OpportunityResult>> {
    const composite = {
      compositeRequest: [
        {
          referenceId: 'refAccount',
          method: 'POST',
          url: '/services/data/v60.0/sobjects/Account',
          body: { Name: params.accountName, Type: 'Prospect', Description: `Created from call ${params.callSid}` },
        },
        ...(params.contactEmail ? [{
          referenceId: 'refContact',
          method: 'POST',
          url: '/services/data/v60.0/sobjects/Contact',
          body: {
            Email: params.contactEmail,
            LastName: params.contactEmail.split('@')[0],
            AccountId: '@{refAccount.id}',
          },
        }] : []),
        {
          referenceId: 'refOpportunity',
          method: 'POST',
          url: '/services/data/v60.0/sobjects/Opportunity',
          body: {
            Name: `${params.productInterest} - ${params.accountName}`,
            StageName: 'Prospecting',
            Amount: params.estimatedValue,
            AccountId: '@{refAccount.id}',
            LeadSource: 'Phone',
            Description: `Voice call opportunity: ${params.callSid}`,
          },
        },
      ],
    };

    const response = await this.restClient.post('composite', composite);
    const results = response.data.compositeResponse;
    return {
      success: results.every((r: any) => r.httpStatusCode < 300),
      data: {
        accountId: results[0].body.id,
        contactId: results[1]?.body?.id,
        opportunityId: results[results.length - 1].body.id,
      },
    };
  }

  async queryWithSOQL(soql: string): Promise<AdapterResponse<SObjectRecord[]>> {
    const response = await this.restClient.get('query', { params: { q: soql } });
    const records: SObjectRecord[] = response.data.records;

    if (response.data.totalSize > response.data.records.length && response.data.nextRecordsUrl) {
      let nextUrl = response.data.nextRecordsUrl;
      while (nextUrl) {
        const nextResponse = await this.restClient.get(nextUrl.replace('/services/data/v60.0/', ''));
        records.push(...nextResponse.data.records);
        nextUrl = nextResponse.data.nextRecordsUrl;
      }
    }
    return { success: true, data: records };
  }

  async describeObject(objectType: string): Promise<ObjectSchema> {
    if (this.schemaCache.has(objectType)) return { success: true, data: this.schemaCache.get(objectType)! };

    const response = await this.restClient.get(`sobjects/${objectType}/describe`);
    const schema: ObjectSchema = {
      name: response.data.name,
      fields: response.data.fields.map((f: any) => ({
        name: f.name,
        type: f.type,
        label: f.label,
        required: f.nillable === false && f.defaultedOnCreate === false,
        picklistValues: f.picklistValues?.map((p: any) => p.value) || [],
        relationshipName: f.relationshipName,
        referenceTo: f.referenceTo,
      })),
    };
    this.schemaCache.set(objectType, schema);
    setTimeout(() => this.schemaCache.delete(objectType), 24 * 60 * 60 * 1000);
    return { success: true, data: schema };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| JSForce (MIT) | Node.js | Salesforce API client |
| JSON Web Token (MIT) | Node.js | JWT assertion generation |
| Axios (MIT) | HTTP | HTTP client |

## Production Considerations

**Scaling:** Salesforce enforces API request limits based on license type (e.g., 15,000-1,000,000 API calls per 24 hours per org). Implement a usage tracking middleware that monitors daily API consumption and alerts when approaching limits. Use the Bulk API 2.0 for data-intensive operations (over 10,000 records). Cache describe results aggressively. Implement request batching via the Composite API to maximize throughput within rate limits.

**Security:** Salesforce API access is controlled through a Connected App with IP allowlisting. The JWT private key must be stored encrypted and loaded only into memory. Never log session IDs or access tokens. Validate that the Salesforce user account used for integration has only the minimum required permissions. Implement field-level security checks before writing to sensitive fields.

**Monitoring:** Track API call volume by endpoint, daily API limit utilization, Composite API batch sizes, SOQL query performance (long-running queries), authentication token refresh rate, and Bulk API job completion rates. Alert on API limit utilization exceeding 80%, authentication failures, and Bulk API job failures. Monitor average response times by Salesforce instance and set up proactive alerts for Salesforce maintenance windows.
