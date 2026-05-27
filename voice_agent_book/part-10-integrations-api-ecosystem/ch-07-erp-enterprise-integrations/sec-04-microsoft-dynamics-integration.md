# Section 04: Microsoft Dynamics 365 Integration

## Overview

The Microsoft Dynamics 365 integration adapter connects the voice agent platform with Dynamics 365 Sales, Customer Service, Finance & Operations, and Business Central. The adapter enables voice agents to access customer records, create leads and opportunities, check case status, retrieve order history, and interact with Dynamics' unified customer data platform (Customer Insights) and Dataverse.

The integration leverages Microsoft's Power Platform API ecosystem: the Dataverse Web API (formerly Common Data Service API) for Customer Engagement apps, the Finance & Operations OData API for ERP functions, and Microsoft Graph for organizational data. The adapter handles Dynamics' complex hierarchical business model (business units, teams, sharing), field-level security, and process automation (Power Automate workflows triggered by data changes).

## Architecture

```
                 Microsoft Dynamics 365 Integration

   Voice Agent ←→ ERP Gateway ←→ Dynamics Adapter ←→ Dataverse API
                                                            |
   +--------------------------------------------------------+
   |           Dynamics 365 Adapter Components              |
   |                                                        |
   |  +------------------+  +-------------------+          |
   |  | Auth & Identity  |  | Dataverse API     |          |
   |  | • Azure AD OAuth2|  | • CRUD operations  |          |
   |  | • Client creds   |  | • FetchXML queries |          |
   |  | • Token cache    |  | • Bound/unbound    |          |
   |  +------------------+  |   actions          |          |
   |  +------------------+  +-------------------+          |
   |  | FO OData API     |  | BC API Client     |          |
   |  | • Finance & Ops  |  | • Business Central|          |
   |  | • Purchase order |  | • Inventory       |          |
   |  | • Invoice lookup |  | • Customer        |          |
   |  +------------------+  +-------------------+          |
   +--------------------------------------------------------+
```

## Design Decisions

- **Dataverse Web API as the primary integration point:** Dataverse provides a single OData v4 endpoint for all Customer Engagement entities (Account, Contact, Lead, Opportunity, Case, Quote). The adapter uses this as the primary data access method, falling back to Finance & Operations API only for ERP-specific functions not available in Dataverse. Trade-off: Dataverse-centric design works best for Sales/Service scenarios but requires the FO API for finance-specific operations, creating a split data access pattern.

- **FetchXML over OData filter queries for Dynamics CE:** While the Dataverse API supports standard OData filters, FetchXML provides access to advanced Dynamics features: aggregate queries (count, sum, avg), cross-entity linkages with aliases, link-entity outer joins, and user context filtering (only records the calling user can see). The adapter uses FetchXML for all complex queries and OData filters only for simple lookups. Trade-off: FetchXML is Dynamics-specific (not portable) but provides access to platform-native query capabilities like rollup fields and calculated fields.

- **Azure AD managed identity for production over client credentials:** For production deployments on Azure, the adapter uses Azure Managed Identity (system-assigned or user-assigned) authenticated against Dynamics. This eliminates credential management entirely — the identity is bound to the compute resource (App Service, AKS pod). For development and on-premise deployments, OAuth 2.0 client credentials flow with a service principal is used. Trade-off: managed identity only works in Azure but provides the most secure and operationally simple authentication.

## Implementation Approach

```
interface DynamicsAdapterConfig {
  environmentUrl: string;
  authType: 'clientCredentials' | 'managedIdentity' | 'deviceCode';
  clientId?: string;
  clientSecret?: string;
  tenantId?: string;
  foEndpoint?: string;
  bcEndpoint?: string;
}

interface DynamicsCustomer {
  accountId?: string;
  contactId?: string;
  name: string;
  email?: string;
  phone?: string;
  address?: AddressData;
}

class DynamicsERPAdapter extends BaseERPAdapter {
  private dataverseClient: DataverseClient;
  private foClient?: FOClient;
  private bcClient?: BCClient;
  private tokenProvider: TokenProvider;

  constructor(config: DynamicsAdapterConfig) {
    super(config);
    this.tokenProvider = config.authType === 'managedIdentity'
      ? new ManagedIdentityTokenProvider()
      : new ClientCredentialsTokenProvider({
          clientId: config.clientId!,
          clientSecret: config.clientSecret!,
          tenantId: config.tenantId!,
        });
    this.dataverseClient = new DataverseClient({
      environmentUrl: config.environmentUrl,
      tokenProvider: this.tokenProvider,
    });
    if (config.foEndpoint) {
      this.foClient = new FOClient({ baseUrl: config.foEndpoint, tokenProvider: this.tokenProvider });
    }
  }

  async findCustomerByPhone(phone: string): Promise<AdapterResponse<DynamicsCustomer>> {
    const fetchXml = `
      <fetch version="1.0" output-format="xml-platform" mapping="logical" distinct="true">
        <entity name="account">
          <attribute name="accountid" />
          <attribute name="name" />
          <attribute name="telephone1" />
          <attribute name="emailaddress1" />
          <filter type="or">
            <condition attribute="telephone1" operator="eq" value="${phone}" />
            <condition attribute="telephone2" operator="eq" value="${phone}" />
          </filter>
        </entity>
      </fetch>`;

    const response = await this.dataverseClient.fetchXml('accounts', fetchXml);
    if (response.value.length > 0) {
      const a = response.value[0];
      return { success: true, data: this.mapToCustomer(a, 'account') };
    }

    // Try contact lookup
    const contactFetchXml = `
      <fetch version="1.0" output-format="xml-platform" mapping="logical">
        <entity name="contact">
          <attribute name="contactid" />
          <attribute name="fullname" />
          <attribute name="telephone1" />
          <attribute name="emailaddress1" />
          <filter>
            <condition attribute="telephone1" operator="eq" value="${phone}" />
          </filter>
        </entity>
      </fetch>`;

    const contactResponse = await this.dataverseClient.fetchXml('contacts', contactFetchXml);
    if (contactResponse.value.length === 0) {
      return { success: false, data: null as any, error: 'Customer not found' };
    }
    const c = contactResponse.value[0];
    return { success: true, data: this.mapToCustomer(c, 'contact') };
  }

  async createOpportunityFromCall(params: {
    customerId: string;
    customerType: 'account' | 'contact';
    description: string;
    estimatedValue: number;
    callSid: string;
  }): Promise<AdapterResponse<{ opportunityId: string }>> {
    const customerLookup = {
      [`${params.customerType}id@odata.bind`]: `/accounts(${params.customerId})`,
    };

    const opportunity = {
      [`${params.customerType === 'account' ? 'parentaccountid' : 'parentcontactid'}@odata.bind`]:
        params.customerType === 'account'
          ? `/accounts(${params.customerId})`
          : `/contacts(${params.customerId})`,
      name: `Call Opportunity - ${new Date().toISOString().split('T')[0]}`,
      description: `${params.description}\nCall SID: ${params.callSid}`,
      estimatedvalue: params.estimatedValue,
      'msdyn_forecastcategory': 1, // Pipeline
      leadqualitycodes: 2, // Warm
    };

    const response = await this.dataverseClient.create('opportunities', opportunity);
    return { success: true, data: { opportunityId: response.opportunityid } };
  }

  async lookupOrderStatus(orderId: string): Promise<AdapterResponse<OrderStatusData>> {
    if (this.foClient) {
      const foOrder = await this.foClient.getSalesOrder(orderId);
      return {
        success: true,
        data: {
          orderId: foOrder.SalesOrderNumber,
          status: foOrder.DocumentStatus,
          totalAmount: foOrder.TotalAmount,
          currency: foOrder.CurrencyCode,
          createdDate: foOrder.CreatedDateTime,
          deliveryDate: foOrder.RequestedDeliveryDate,
          lineItems: foOrder.SalesOrderLines?.map((l: any) => ({
            itemId: l.ItemNumber,
            description: l.ItemDescription,
            quantity: l.Quantity,
            unitPrice: l.UnitPrice,
          })),
        },
      };
    }

    // Fallback to Dataverse order
    const fetchXml = `<fetch version="1.0"><entity name="salesorder">
      <attribute name="salesorderid" /><attribute name="ordernumber" />
      <attribute name="totalamount" /><attribute name="statecode" />
      <filter><condition attribute="ordernumber" operator="eq" value="${orderId}" /></filter>
    </entity></fetch>`;

    const response = await this.dataverseClient.fetchXml('salesorders', fetchXml);
    if (!response.value.length) return { success: false, data: null as any, error: 'Order not found' };

    const o = response.value[0];
    return { success: true, data: { orderId: o.ordernumber, status: o.statecode, totalAmount: o.totalamount } };
  }

  private mapToCustomer(record: any, type: 'account' | 'contact'): DynamicsCustomer {
    return {
      [`${type}Id`]: record[`${type}id`],
      name: type === 'account' ? record.name : record.fullname,
      email: record.emailaddress1,
      phone: record.telephone1,
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| @azure/identity (MIT) | Azure SDK | Managed Identity + OAuth |
| Dataverse SDK (MIT) | Node.js | Dataverse Web API client |
| Axios (MIT) | HTTP | FO OData HTTP client |

## Production Considerations

**Scaling:** Dynamics 365 API limits are based on entitlement (5,000 requests per 5 minutes per user for production). For integration users, higher limits apply. Implement aggressive caching for Entity Definitions (metadata) — cache for 24 hours since metadata changes are infrequent. Use $batch requests for bulk operations (max 500 requests per batch). Monitor API entitlement consumption using the Dynamics 365 Request Quota header in responses.

**Security:** Service principal (Application User) must be created in Dynamics with appropriate security role. Use the principle of least privilege — create a custom security role with only the entities and privileges the integration needs. Business Unit scoping: the application user should be scoped to the root business unit for cross-unit access, or scoped to a specific business unit for tenant isolation. Never log the client secret. Use Azure Key Vault for credential storage.

**Monitoring:** Track API request quota utilization, FetchXML query performance, batch operation sizes, Dataverse Web API latency, FO OData response times, and authentication token refresh rates. Monitor error types: privilege denial, record not found, duplicate detection, concurrency conflicts. Alert on quota utilization exceeding 70%, authentication failures, record creation failures (which block the voice flow), and long-running FetchXML queries.
