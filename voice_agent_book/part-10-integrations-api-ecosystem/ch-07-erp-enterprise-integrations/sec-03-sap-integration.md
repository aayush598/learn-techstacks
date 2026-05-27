# Section 03: SAP Integration

## Overview

The SAP ERP integration adapter connects the voice agent platform with SAP S/4HANA and SAP ECC systems, enabling voice-driven interactions with SAP's core business functions: customer master data, sales order processing, pricing and availability checks, invoice retrieval, and service management (SAP Service Cloud / SAP CRM). The adapter uses SAP's modern API offerings including SAP API Business Hub, OData v4 services, and the SAP Cloud SDK for data access.

SAP integration is typically more complex than other ERP integrations due to SAP's unique data model (client/company code/plant structure), the prevalence of custom BAPI/Z-functions, and the strict RFC/gateway security model. The adapter abstracts this complexity behind a unified SAP interface, supporting both SAP S/4HANA Cloud (via OData) and SAP ECC on-premise (via SAP Cloud Connector and RFC-to-OData bridging). The integration handles SAP's complex authorization model (PFCG roles, authorization objects) and field-level security.

## Architecture

```
                      SAP ERP Integration

   Voice Agent ←→ ERP Gateway ←→ SAP Adapter ←→ SAP S/4HANA
                                                      |
   +--------------------------------------------------+
   |              SAP Adapter Components              |
   |                                                  |
   |  +------------------+  +-------------------+    |
   |  | Auth & SSO       |  | OData Client      |    |
   |  | • Basic Auth     |  | • CRUD operations  |    |
   |  | • SAML Bearer    |  | • Function imports |    |
   |  | • x509 cert      |  | • Batch requests   |    |
   |  +------------------+  +-------------------+    |
   |  +------------------+  +-------------------+    |
   |  | BAPI/RFC Bridge  |  | Pricing Engine    |    |
   |  | • BAPI calls     |  | • Price enquiry   |    |
   |  | • Z-function mod |  | • Condition rec   |    |
   |  | • RFC read table |  | • Discount calc   |    |
   |  +------------------+  +-------------------+    |
   +--------------------------------------------------+
```

## Design Decisions

- **OData v4 primary with BAPI fallback for custom logic:** SAP S/4HANA exposes OData v4 services for standard business objects (Customer, Sales Order, Material, Invoice). The adapter uses these services for all CRUD operations. For custom business logic (Z-functions, BAPIs with complex validation), the adapter uses SAP's BAPI/RFC framework via the SAP Cloud SDK or an OData custom service wrapper. Trade-off: OData provides modern RESTful access but does not cover all custom SAP functionality; BAPI fallback ensures comprehensive coverage at the cost of additional integration points.

- **Connection multiplexing over single-gateway architecture:** The adapter maintains a pool of authenticated connections to SAP, each bound to a specific client and language. Connection reuse is critical since SAP logon is expensive (5-15 seconds for the first call). The pool size is configurable per tenant and scales based on concurrent call volume. Idle connections are health-checked every 5 minutes. Trade-off: connection pooling adds memory overhead and requires careful lifecycle management but eliminates logon latency from the call path.

- **SAP Cloud SDK for node.js over raw OData client library:** The SAP Cloud SDK provides type-safe OData v2/v4 client abstractions, automatic CSRF token handling, middleware for logging and error mapping, and out-of-the-box destination configuration (Cloud Foundry, Kubernetes, on-premise via Cloud Connector). Trade-off: the SDK adds a dependency on SAP's library ecosystem and learning curve but significantly reduces boilerplate for authentication, CSRF, and error mapping common to all SAP integrations.

## Implementation Approach

```
interface SAPAdapterConfig {
  destination: SAPDestination;
  client: string;
  language?: string;
  pricingProcedure?: string;
}

interface SAPDestination {
  url: string;
  authType: 'basic' | 'saml' | 'x509' | 'oauth2';
  credentials?: { username: string; password: string };
  cloudConnectorLocationId?: string;
}

interface SAPSalesOrderRequest {
  salesOrderType: string;
  soldToParty: string;
  shipToParty?: string;
  plant: string;
  items: {
    material: string;
    quantity: number;
    plant?: string;
  }[];
  pricingDate?: Date;
  purchaseOrderNumber?: string;
}

class SAPERPAdapter extends BaseERPAdapter {
  private odataClient: ODataClient;
  private destination: SAPDestination;
  private sessionPool: ConnectionPool;

  constructor(config: SAPAdapterConfig) {
    super(config);
    this.destination = config.destination;
    this.odataClient = new SAPCloudSDK.ODataClient({
      destination: this.mapDestination(config.destination),
    });
    this.sessionPool = new ConnectionPool({
      min: 2,
      max: 10,
      acquireTimeout: 15000,
      create: () => this.createSession(config.destination),
    });
  }

  async checkMaterialAvailability(materialId: string, plant: string): Promise<AdapterResponse<AvailabilityResult>> {
    const query = this.odataClient
      .requestBuilder()
      .getAll('/sap/opu/odata/sap/API_MATERIAL_AVAILABILITY_SRV')
      .filter(`Material eq '${materialId}' and Plant eq '${plant}'`);

    const response = await query.execute({ destination: this.destination.url });
    const availability = response.value?.[0];

    return {
      success: true,
      data: {
        materialId,
        plant,
        availableQuantity: availability?.AvailQty || 0,
        baseUnit: availability?.BaseUnit,
        availabilityDate: availability?.AvailDate,
        checkingRule: availability?.CheckingRule,
      },
    };
  }

  async createSalesOrder(request: SAPSalesOrderRequest): Promise<AdapterResponse<SalesOrderResult>> {
    const csrfToken = await this.fetchCSRFToken();
    const session = await this.sessionPool.acquire();

    try {
      const response = await this.odataClient
        .requestBuilder()
        .create('/sap/opu/odata/sap/API_SALES_ORDER_SRV/A_SalesOrder')
        .withCsrfToken(csrfToken)
        .payload({
          SalesOrderType: request.salesOrderType,
          SoldToParty: request.soldToParty,
          ShipToParty: request.shipToParty || request.soldToParty,
          Plant: request.plant,
          PurchaseOrderByCustomer: request.purchaseOrderNumber,
          to_Item: request.items.map(item => ({
            Material: item.material,
            Quantity: item.quantity,
            Plant: item.plant || request.plant,
          })),
        })
        .execute({ destination: this.destination.url });

      return {
        success: true,
        data: {
          salesOrderId: response.SalesOrder,
          soldToParty: request.soldToParty,
          totalNetValue: response.TotalNetAmount,
          currency: response.TransactionCurrency,
          createdAt: response.CreationDate,
        },
      };
    } finally {
      this.sessionPool.release(session);
    }
  }

  async getCustomerDetails(customerId: string): Promise<AdapterResponse<CustomerData>> {
    const response = await this.odataClient
      .requestBuilder()
      .getAll('/sap/opu/odata/sap/API_BUSINESS_PARTNER/A_BusinessPartner')
      .filter(`BusinessPartner eq '${customerId}'`)
      .expand('to_BusinessPartnerAddress')
      .execute({ destination: this.destination.url });

    const bp = response.value?.[0];
    if (!bp) return { success: false, data: null as any, error: 'Customer not found' };

    return {
      success: true,
      data: {
        id: bp.BusinessPartner,
        name: bp.BusinessPartnerFullName,
        category: bp.BusinessPartnerCategory,
        addresses: (bp.to_BusinessPartnerAddress || []).map((addr: any) => ({
          street: addr.StreetName,
          city: addr.CityName,
          postalCode: addr.PostalCode,
          country: addr.Country,
        })),
      },
    };
  }

  private async fetchCSRFToken(): Promise<string> {
    const response = await axios.head(this.destination.url, {
      headers: {
        'X-CSRF-Token': 'Fetch',
        'Authorization': this.buildAuthHeader(),
      },
    });
    return response.headers['x-csrf-token']!;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| SAP Cloud SDK (Apache 2.0) | Node.js | OData client + auth |
| Axios (MIT) | HTTP | CSRF token requests |
| Generic Pool (MIT) | Pool | Connection pool management |

## Production Considerations

**Scaling:** SAP connection pool sizing depends on SAP license (dialog vs. service user) and SAP application server capacity. Each SAP connection consumes a dialog work process on the application server — monitor work process utilization and set pool max to avoid exhausting server resources. Use SAP's bulk processing (OData batch requests, BAPI transaction grouping) for operations involving multiple records. Implement circuit breaker pattern for SAP destination availability.

**Security:** SAP credentials (username/password, x509 certificates) must be stored encrypted. Use SAP's Secure Store & Forward (SSF) for credential management if available. For on-premise SAP, use SAP Cloud Connector for secure tunnel without opening firewall ports. Implement PFCG role-based authorization — the integration user should have only the minimum required roles and authorization objects. Log all RFC and OData calls with correlation IDs for audit.

**Monitoring:** Track SAP connection pool utilization (active/inactive/pending), work process utilization on the application server, OData response times by service, BAPI execution times, CSRF token acquisition time, and session creation duration. Monitor SAP error categories (ABAP dump, RFC error, authorization failure, lock conflicts). Alert on connection pool exhaustion, authentication failures, authorization errors, and response time degradation.
