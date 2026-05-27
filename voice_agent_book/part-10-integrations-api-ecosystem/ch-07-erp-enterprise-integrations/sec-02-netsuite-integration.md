# Section 02: NetSuite Integration

## Overview

The NetSuite ERP integration adapter enables voice agents to interact with Oracle NetSuite's business management suite, handling core ERP functions: customer records, sales orders, inventory inquiries, invoice lookups, and case management. The adapter uses NetSuite's SuiteTalk REST Web Services (RESTlets) and the SuiteQL query API for data access, providing a modern RESTful interface to NetSuite's comprehensive ERP data model.

NetSuite's integration presents unique challenges compared to other ERPs: a complex record-centric data model with custom fields, custom segments, and custom record types; a permission system based on roles with feature-level access control; and a deployment model where custom integrations are deployed as SuiteScript files or RESTlets within the NetSuite account. The adapter abstracts this complexity behind a clean ERP interface, handling authentication via TBA (Token-Based Authentication) and OAuth 2.0.

## Architecture

```
                   NetSuite ERP Integration

   Voice Agent ←→ ERP Gateway ←→ NetSuite Adapter ←→ SuiteTalk API
                                                              |
   +----------------------------------------------------------+
   |               NetSuite Adapter Structure                 |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Token Auth       |  | RESTlet Client    |            |
   |  | • TBA / OAuth2   |  | • Custom endpoints|            |
   |  | • Signature      |  | • SuiteQL queries |            |
   |  | • Nonce mgmt     |  | • SuiteScript     |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Record Service   |  | Search Service    |            |
   |  | • Customer       |  | • SuiteQL         |            |
   |  | • Sales Order    |  | • Advanced search |            |
   |  | • Item / Invoice |  | • Saved search    |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Custom Fields    |  | File Cabinet      |            |
   |  | • Dynamic lookup |  | • Attachment upload|           |
   |  | • Type mapping   |  | • Document links   |           |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **SuiteQL over RESTlet-based queries for data retrieval:** SuiteQL provides an ODBC/JDBC-compatible SQL interface to NetSuite data, supporting JOINs across record types, filtering, and aggregation. The adapter uses SuiteQL for all read operations (customer lookup, order history, inventory status) and RESTlets only for write operations (creating records that require SuiteScript business logic). Trade-off: SuiteQL requires NetSuite 2021.1+ and ODBC or REST Web Services license but provides dramatically more flexible querying than saved searches.

- **RESTlet-based write operations with unified error handling:** All create, update, and delete operations go through a custom RESTlet deployed in the NetSuite account. The RESTlet handles record creation with field validation, custom segment assignment, and subsidiary routing. The RESTlet returns a standardized response envelope with success/error/fieldErrors. Trade-off: RESTlet development requires SuiteScript (JavaScript) knowledge and deployment within each NetSuite account but provides centralized business logic and consistent error responses.

- **Bundled custom fields schema vs. dynamic discovery:** Unlike Salesforce's open metadata API, NetSuite's custom field discovery is more limited through external APIs. The adapter maintains a configuration-driven field mapping file that defines how platform fields map to NetSuite fields (standard and custom), including field types, lists, and validation rules. This mapping is deployed alongside the adapter and versioned. Trade-off: bundled mapping requires updates when NetSuite custom fields change but avoids runtime schema discovery latency and works around NetSuite's API limitations.

## Implementation Approach

```
interface NetSuiteAdapterConfig {
  accountId: string;
  consumerKey: string;
  consumerSecret: string;
  tokenId: string;
  tokenSecret: string;
  restletUrl: string;
  suiteqlEndpoint?: string;
}

interface NetSuiteRecord {
  id: string;
  type: string;
  fields: Record<string, any>;
}

class NetSuiteERPAdapter extends BaseERPAdapter {
  private oauthClient: OAuthClient;

  constructor(config: NetSuiteAdapterConfig) {
    super(config);
    this.oauthClient = new OAuthClient({
      consumerKey: config.consumerKey,
      consumerSecret: config.consumerSecret,
      tokenId: config.tokenId,
      tokenSecret: config.tokenSecret,
      realm: config.accountId,
      signatureMethod: 'HMAC-SHA256',
    });
  }

  async lookupCustomer(phoneNumber: string): Promise<AdapterResponse<CustomerData>> {
    const query = `
      SELECT
        id, companyname, email, phone, altphone,
        custentity_platform_id, datecreated
      FROM customer
      WHERE phone = '${phoneNumber}' OR altphone = '${phoneNumber}'
    `;
    const result = await this.executeSuiteQL(query);
    if (result.data.length === 0) {
      return { success: false, data: null as any, error: 'Customer not found' };
    }
    return { success: true, data: this.mapNetSuiteCustomer(result.data[0]) };
  }

  async createSalesOrderFromCall(params: {
    customerId: string;
    items: { internalId: string; quantity: number; rate?: number }[];
    callSid: string;
    memo?: string;
  }): Promise<AdapterResponse<SalesOrderResult>> {
    const restletPayload = {
      action: 'createSalesOrder',
      data: {
        entity: { id: params.customerId },
        item: {
          items: params.items.map(item => ({
            item: { internalId: item.internalId },
            quantity: item.quantity,
            rate: item.rate,
          })),
        },
        memo: params.memo || `Created from voice call ${params.callSid}`,
        custbody_call_sid: params.callSid,
      },
    };

    const response = await this.postRestlet(restletPayload);
    if (!response.success) {
      return { success: false, data: null as any, error: response.errorMessage };
    }
    return {
      success: true,
      data: {
        salesOrderId: response.recordId,
        internalId: response.internalId,
        total: response.total,
        createdDate: response.createdDate,
      },
    };
  }

  async checkInventory(internalId: string, locationId?: string): Promise<AdapterResponse<InventoryResult>> {
    const query = `
      SELECT
        location, quantityavailable, quantityonhand, quantitycommitted
      FROM itemfulfillment
      WHERE item = '${internalId}'
      ${locationId ? `AND location = '${locationId}'` : ''}
    `;
    const result = await this.executeSuiteQL(query);
    return {
      success: true,
      data: {
        itemId: internalId,
        locations: result.data.map((r: any) => ({
          locationId: r.location,
          available: r.quantityavailable,
          onHand: r.quantityonhand,
          committed: r.quantitycommitted,
        })),
      },
    };
  }

  private async executeSuiteQL(query: string): Promise<{ data: any[] }> {
    const headers = this.oauthClient.createHeaders({
      url: `${this.config.suiteqlEndpoint}/query/v1/suiteql`,
      method: 'POST',
    });
    const response = await axios.post(
      this.config.suiteqlEndpoint!,
      { q: query },
      { headers: { ...headers, 'Content-Type': 'application/json' } }
    );
    return { data: response.data.items || [] };
  }

  private async postRestlet(payload: any): Promise<any> {
    const headers = this.oauthClient.createHeaders({
      url: this.config.restletUrl,
      method: 'POST',
    });
    const response = await axios.post(this.config.restletUrl, payload, {
      headers: { ...headers, 'Content-Type': 'application/json' },
    });
    return response.data;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| OAuth 1.0a (MIT) | Node.js | TBA signature generation |
| Axios (MIT) | HTTP | SuiteQL and RESTlet client |
| Zod (MIT) | Validation | Response validation |

## Production Considerations

**Scaling:** NetSuite governance limits are strict — each RESTlet/SuiteQL call consumes governance units (default 10,000 per account per day, 1,000 per integration user per day). Optimize SuiteQL queries to return only needed fields. Batch record creation through the RESTlet (accept arrays of records). Cache customer and item lookups aggressively (10-minute TTL for items, 30-minute for customers). Implement governance usage monitoring to avoid hitting daily limits during peak call times.

**Security:** NetSuite TBA tokens provide direct data access — scope the integration role to only the required records and fields. The OAuth consumer secret must be encrypted at rest. Never log the token secret or consumer secret. Use IP allowlisting for the integration user. Each NetSuite environment (Sandbox vs. Production) requires separate OAuth credentials. Implement field-level security by validating all field writes against allowed fields.

**Monitoring:** Track governance unit consumption rate, daily quota utilization, SuiteQL query performance (response time by query pattern), RESTlet execution errors by type, OAuth token refresh rate, and integration user API call volume. Alert on governance consumption exceeding 75% daily limit, RESTlet failures, SuiteQL timeouts, and authentication failures. Monitor average order creation time from voice call to NetSuite record creation.
