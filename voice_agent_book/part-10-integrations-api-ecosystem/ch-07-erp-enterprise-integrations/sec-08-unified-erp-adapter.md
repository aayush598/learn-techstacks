# Section 08: Unified ERP Adapter

## Overview

The Unified ERP Adapter provides a consistent abstraction over multiple enterprise resource planning systems (Salesforce, NetSuite, SAP S/4HANA, Microsoft Dynamics 365, and other ERP platforms). Following the same strategy pattern as the payment adapter, the unified ERP adapter defines a common interface for ERP operations — customer management, order processing, inventory lookup, invoicing, and price checks — with concrete strategy implementations for each ERP system.

The unified adapter normalizes the significant differences between ERP systems: different data models (account vs. customer vs. business partner), different query languages (SOQL, SuiteQL, OData, FetchXML), different authentication mechanisms (OAuth2 JWT, TBA, SAML bearer, client credentials), and different business process flows (order-to-cash, procure-to-pay). The adapter provides a canonical ERP data model that maps to each system's native objects while preserving each system's unique capabilities in a metadata layer.

## Architecture

```
                  Unified ERP Adapter Architecture

   Voice Agent ←→ Unified ERP API ←→ ERP Strategy ←→ ERP System
                        |
   +----------------------------------------------------------+
   |              Unified ERP Adapter Layer                   |
   |                                                          |
   |  +----------------------------------------------------+ |
   |  |   ERPController (Unified API Surface)              | |
   |  |   - findCustomer / createCustomer / updateCustomer | |
   |  |   - createOrder / getOrderStatus / cancelOrder     | |
   |  |   - checkInventory / reserveInventory              | |
   |  |   - getPricing / applyDiscount                     | |
   |  |   - createInvoice / getInvoice                     | |
   |  |   - getProductCatalog / searchProducts             | |
   |  +----------------------------------------------------+ |
   |              |            |            |                 |
   |              v            v            v                 |
   |  +----------+ +----------+ +----------+ +--------------+ |
   |  | Salesforce| | NetSuite | | SAP      | | Dynamics 365| |
   |  | Strategy  | | Strategy | | Strategy | | Strategy    | |
   |  +----------+ +----------+ +----------+ +--------------+ |
   |                                                          |
   |  Canonical Data Models:                                   |
   |  - CustomerRecord, OrderRecord, InventoryRecord          |
   |  - ProductRecord, InvoiceRecord, PricingRecord           |
   |  - AddressRecord, PaymentTermsRecord                     |
   +----------------------------------------------------------+
```

## Design Decisions

- **Capability enumeration over uniform interface assumption:** Not all ERP systems support the same operations. SAP may support material availability checks natively while Salesforce may not. The ERP adapter declares its capabilities through a `Capability` enum (`CustomerSearch`, `OrderCreation`, `InventoryCheck`, `PricingEngine`, `InvoiceCreation`, `ProductCatalog`, `CreditCheck`). The unified controller checks capability flags before dispatching operations and provides graceful fallbacks for unsupported operations (e.g., "Inventory check not available for this ERP"). Trade-off: capability checks add branching logic but accurately represent heterogeneous ERP capabilities.

- **Strategy-specific configuration over shared config schema:** Each ERP strategy requires fundamentally different configuration: Salesforce needs instance URL, client ID, private key, and username; NetSuite needs account ID, consumer key/secret, token ID/secret, and RESTlet URL; SAP needs destination URL, client number, and authentication type. The configuration is strategy-specific with a common envelope (strategy type, enabled flag, environment). Trade-off: strategy-specific config prevents a unified configuration UI but allows each strategy to capture its exact connectivity requirements.

- **Canonical query language with strategy-specific translation:** The unified adapter introduces a query abstraction — `ERPQuery` — that expresses data retrieval in a system-agnostic way. Each strategy translates the canonical query into its native language (SOQL, SuiteQL, OData filter, FetchXML). The query abstraction supports field selection, filtering, sorting, pagination, and includes. Complex queries that are ERP-specific are supported through a `rawQuery` escape hatch that passes the query directly to the strategy. Trade-off: query abstraction is imperfect for complex ERP-specific queries but handles 90% of common lookups uniformly.

## Implementation Approach

```
enum ERPCapability {
  CUSTOMER_SEARCH = 'customer_search',
  CUSTOMER_CREATE = 'customer_create',
  CUSTOMER_UPDATE = 'customer_update',
  ORDER_CREATE = 'order_create',
  ORDER_STATUS = 'order_status',
  ORDER_CANCEL = 'order_cancel',
  INVENTORY_CHECK = 'inventory_check',
  INVENTORY_RESERVE = 'inventory_reserve',
  PRICING_LOOKUP = 'pricing_lookup',
  PRICE_CALCULATE = 'price_calculate',
  INVOICE_CREATE = 'invoice_create',
  INVOICE_GET = 'invoice_get',
  PRODUCT_SEARCH = 'product_search',
  CREDIT_CHECK = 'credit_check',
}

interface ERPStrategy {
  readonly type: string;
  readonly capabilities: ERPCapability[];

  initialize(config: ERPStrategyConfig): Promise<void>;
  healthCheck(): Promise<HealthStatus>;

  // Customer operations
  findCustomer(query: CustomerQuery): Promise<Result<CustomerRecord>>;
  createCustomer(data: CustomerCreateData): Promise<Result<CustomerRecord>>;
  updateCustomer(id: string, data: Partial<CustomerCreateData>): Promise<Result<CustomerRecord>>;

  // Order operations
  createOrder(request: OrderRequest): Promise<Result<OrderRecord>>;
  getOrderStatus(orderId: string): Promise<Result<OrderRecord>>;
  cancelOrder(orderId: string): Promise<Result<OrderStatusData>>;

  // Inventory
  checkInventory(sku: string, warehouseId?: string): Promise<Result<InventoryRecord>>;
  reserveInventory(request: InventoryReserveRequest): Promise<Result<InventoryReservation>>;

  // Pricing
  getPricing(skus: string[], customerId?: string): Promise<Result<PricingRecord[]>>;
  calculatePrice(request: PriceCalculationRequest): Promise<Result<PriceResult>>;

  // Invoice
  createInvoice(request: InvoiceRequest): Promise<Result<InvoiceRecord>>;
  getInvoice(invoiceId: string): Promise<Result<InvoiceRecord>>;

  // Product
  searchProducts(query: string, options?: ProductSearchOptions): Promise<Result<ProductRecord[]>>;
}

class UnifiedERPAdapter {
  private strategies = new Map<string, ERPStrategy>();
  private tenantConfigs = new Map<string, string>(); // tenantId → strategy type

  registerStrategy(strategy: ERPStrategy) {
    this.strategies.set(strategy.type, strategy);
  }

  setTenantStrategy(tenantId: string, strategyType: string) {
    this.tenantConfigs.set(tenantId, strategyType);
  }

  private getStrategy(tenantId: string): ERPStrategy {
    const type = this.tenantConfigs.get(tenantId);
    if (!type) throw new Error(`No ERP configured for tenant ${tenantId}`);
    const strategy = this.strategies.get(type);
    if (!strategy) throw new Error(`ERP strategy ${type} not registered`);
    return strategy;
  }

  private checkCapability(strategy: ERPStrategy, capability: ERPCapability): void {
    if (!strategy.capabilities.includes(capability)) {
      throw new Error(`ERP ${strategy.type} does not support ${capability}`);
    }
  }

  // Unified API surface
  async findCustomer(tenantId: string, query: CustomerQuery): Promise<Result<CustomerRecord>> {
    const strategy = this.getStrategy(tenantId);
    this.checkCapability(strategy, ERPCapability.CUSTOMER_SEARCH);
    const result = await strategy.findCustomer(query);
    if (result.success) {
      await this.emitEvent('erp.customer.found', { tenantId, query, result: result.data });
    }
    return result;
  }

  async createOrder(tenantId: string, request: OrderRequest): Promise<Result<OrderRecord>> {
    const strategy = this.getStrategy(tenantId);
    this.checkCapability(strategy, ERPCapability.ORDER_CREATE);

    await this.preOrderValidation(tenantId, request);
    const result = await strategy.createOrder(request);
    if (result.success) {
      await this.emitEvent('erp.order.created', { tenantId, orderId: result.data.id, total: result.data.totalAmount });
    }
    return result;
  }

  async checkInventory(tenantId: string, sku: string): Promise<Result<InventoryRecord>> {
    const strategy = this.getStrategy(tenantId);
    this.checkCapability(strategy, ERPCapability.INVENTORY_CHECK);
    return strategy.checkInventory(sku);
  }

  async searchProducts(
    tenantId: string, query: string, options?: ProductSearchOptions
  ): Promise<Result<ProductRecord[]>> {
    const strategy = this.getStrategy(tenantId);
    this.checkCapability(strategy, ERPCapability.PRODUCT_SEARCH);
    return strategy.searchProducts(query, options);
  }

  async createInvoice(tenantId: string, request: InvoiceRequest): Promise<Result<InvoiceRecord>> {
    const strategy = this.getStrategy(tenantId);
    this.checkCapability(strategy, ERPCapability.INVOICE_CREATE);
    const result = await strategy.createInvoice(request);
    if (result.success) {
      await this.emitEvent('erp.invoice.created', { tenantId, invoiceId: result.data.id });
    }
    return result;
  }

  async healthCheckAll(): Promise<Record<string, HealthStatus>> {
    const results: Record<string, HealthStatus> = {};
    for (const [type, strategy] of this.strategies) {
      try {
        results[type] = await strategy.healthCheck();
      } catch {
        results[type] = { status: 'unhealthy', error: 'Health check threw exception' };
      }
    }
    return results;
  }
}

// Canonical Entity: CustomerRecord
interface CustomerRecord {
  id: string;
  externalId: string;
  name: string;
  email?: string;
  phone?: string;
  type: 'individual' | 'company';
  addresses: AddressRecord[];
  customFields: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Zod (MIT) | Validation | Canonical model validation |
| Pino (MIT) | Logging | Unified audit logging |
| P-retry (MIT) | Retry | Unified retry across strategies |

## Production Considerations

**Scaling:** The unified adapter is a moderate-traffic component (1-5 requests per call). Caching is critical — cache ERP strategy instances per tenant (initialized on first request), cache customer lookups (30-second TTL during calls), cache product catalogs (hourly refresh). The unified adapter should not add more than 5ms overhead per operation — strategy resolution is a Map lookup, capability check is a Set has, event emission is async.

**Security:** Strategy configuration (credentials) is stored encrypted per tenant and decrypted only when initializing the strategy instance. Strategy instances are isolated per tenant — one tenant's credentials should never be accessible from another tenant's requests. The unified adapter logs the operation type and tenant ID but never the payload data containing PII. Implement rate limiting per tenant per ERP strategy to prevent one tenant from overwhelming the shared ERP infrastructure.

**Monitoring:** Track per-strategy operation counts, success/failure rates, latency percentiles, capability utilization (which operations are used most), strategy initialization time, and tenant-to-strategy distribution. Monitor strategy health check results and alert on unhealthy strategies. Track the "graceful degradation" rate — how often operations fall back or fail due to missing capabilities. Monitor credential expiry and alert 30 days before expiration.
