# Section 08: Unified Commerce Adapter

## Overview

The unified commerce adapter provides a consistent interface across multiple e-commerce platforms (Shopify, WooCommerce, Magento) behind a single abstraction. This enables the voice platform to work with any e-commerce system through the same API, simplifying commerce-related voice workflows and enabling multi-platform commerce operations.

The unified adapter defines common operations: order management (lookup, status), product management (lookup, inventory, variants), customer management (lookup, creation, update), return/refund processing, and sync operations (bulk data import/export). Each platform-specific adapter implements these operations using its system's API semantics. The unified layer handles cross-cutting concerns like authentication, rate limiting, error mapping, capability detection, and data normalization.

## Architecture

```
                    Unified Commerce Adapter

   +----------------------------------------------------------+
   |           Unified Commerce Interface                       |
   |                                                          |
   |  getOrder() | getOrdersByEmail() | getProduct()          |
   |  getProductBySku() | getInventory() | createReturn()     |
   |  getCustomer() | updateCustomer() | processRefund()       |
   +----------------------------------------------------------+
              |              |              |
              v              v              v
   +------------------+  +------------------+  +------------------+
   | Shopify          |  | WooCommerce      |  | Magento          |
   | Adapter          |  | Adapter          |  | Adapter          |
   +------------------+  +------------------+  +------------------+
              |              |              |
              v              v              v
   +----------------------------------------------------------+
   |           Cross-Cutting Services                         |
   |                                                          |
   |  Authentication | Rate Limiting | Caching | Observability|
   +----------------------------------------------------------+
```

## Design Decisions

- **Capability-based feature detection:** Each commerce adapter declares its capabilities (supportsReturns, supportsInventory, supportsCustomerManagement, supportsMultiLocation, supportsPreOrder). The platform checks capabilities before executing operations and provides clear error messages for unsupported operations. This enables graceful handling of platforms with different feature sets. Trade-off: capability checks add a code path but prevent runtime errors from unsupported operations.

- **Canonical order model with platform-specific extensions:** The unified adapter defines a canonical order model that captures the common fields across all e-commerce platforms. Platform-specific fields (Shopify's `note_attributes`, WooCommerce's `meta_data`, Magento's `extension_attributes`) are available through a `metadata` map. This preserves platform-specific data while providing a clean common interface. Trade-off: platform-specific metadata may be opaque to consumers who don't know the platform's data model.

- **Bulk synchronization interface for data import/export:** The unified adapter defines a bulk sync interface for importing/exporting products, customers, and orders. Each platform adapter implements this interface using its platform's bulk API (Shopify Bulk GraphQL, WooCommerce batch endpoints, Magento async APIs). The sync interface supports incremental sync (changes since last sync) and full sync. Trade-off: bulk sync implementation is platform-specific and requires separate testing per platform.

## Implementation Approach

```
interface CommerceAdapter {
  readonly platform: string;
  readonly capabilities: CommerceCapabilities;

  initialize(config: CommerceConfig): Promise<void>;

  // Order operations
  getOrder(orderNumber: string): Promise<AdapterResponse<CanonicalOrder>>;
  getOrdersByEmail(email: string): Promise<AdapterResponse<CanonicalOrder[]>>;
  getOrderStatus(orderNumber: string): Promise<AdapterResponse<OrderStatus>>;

  // Product operations
  getProductBySku(sku: string): Promise<AdapterResponse<CanonicalProduct | null>>;
  getProductVariants(productId: string): Promise<AdapterResponse<CanonicalVariant[]>>;
  getInventory(sku: string): Promise<AdapterResponse<InventoryInfo[]>>;

  // Customer operations
  getCustomerByEmail(email: string): Promise<AdapterResponse<CanonicalCustomer | null>>;
  createCustomer(customer: CustomerInput): Promise<AdapterResponse<{ id: string }>>;
  updateCustomer(customerId: string, update: Partial<CustomerInput>): Promise<AdapterResponse<void>>;
  addCustomerAddress(customerId: string, address: AddressInput): Promise<AdapterResponse<{ id: string }>>;

  // Return/Refund operations
  createReturn(returnReq: ReturnInput): Promise<AdapterResponse<ReturnResult>>;
  processRefund(orderId: string, refundData: RefundInput): Promise<AdapterResponse<{ refundId: string }>>;
  restockItem(sku: string, quantity: number): Promise<AdapterResponse<void>>;

  // Sync operations
  bulkExportProducts?(lastSync?: string): AsyncIterable<CanonicalProduct[]>;
  bulkExportOrders?(lastSync?: string): AsyncIterable<CanonicalOrder[]>;
  bulkImportProducts?(products: CanonicalProduct[]): Promise<BulkImportResult>;

  // Webhooks
  registerWebhook?(topic: string, url: string): Promise<AdapterResponse<{ id: string }>>;
  verifyWebhook?(payload: any, signature: string): boolean;
}

interface CommerceCapabilities {
  orders: boolean;
  products: boolean;
  inventory: boolean;
  customers: boolean;
  returns: boolean;
  refunds: boolean;
  multiLocation: boolean;
  preOrder: boolean;
  giftCards: boolean;
  subscriptions: boolean;
}

// Canonical types
interface CanonicalProduct {
  platform: string;
  id: string;
  sku: string;
  name: string;
  description: string;
  price: number;
  compareAtPrice?: number;
  currency: string;
  images: string[];
  variants: { sku: string; name: string; price: number; options: Record<string, string> }[];
  status: 'active' | 'draft' | 'archived';
  categories: string[];
  tags: string[];
  createdAt: string;
  updatedAt: string;
  weight?: number;
  metadata: Record<string, any>;
}

class CommerceAdapterFactory {
  private adapters = new Map<string, CommerceAdapter>();

  register(type: string, adapter: CommerceAdapter) {
    this.adapters.set(type, adapter);
  }

  getAdapter(type: string): CommerceAdapter {
    const adapter = this.adapters.get(type);
    if (!adapter) throw new Error(`Unsupported commerce platform: ${type}`);
    return adapter;
  }

  getAllAdapters(): CommerceAdapter[] {
    return Array.from(this.adapters.values());
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **TypeScript** (Apache 2.0) | Language | Interface definitions |
| **Zod** (MIT) | Validation | Canonical model validation |
| **Axios** (MIT) | HTTP client | API communication |

## Production Considerations

**Scaling:** The unified adapter adds abstraction overhead. Profile per-operation overhead to ensure < 10ms above raw API call. Cache adapter instances by integration configuration. For multi-platform merchants, parallelize platform queries.

**Security:** Adapters should not expose platform-specific credentials through the unified interface. Error messages must be sanitized to remove internal implementation details. Logging should not include full API request/response bodies.

**Monitoring:** Track adapter distribution, per-operation latency by platform, capability utilization, and platform-specific error rates. Alert on adapter health check failures, operations exceeding capability boundaries, and unusual error patterns.
