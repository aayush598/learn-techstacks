# Section 03: Magento Integration

## Overview

Magento (Adobe Commerce) integration connects the voice platform with Magento-powered e-commerce stores. Magento provides REST APIs for orders, products, customers, quotes (carts), shipments, invoices, credit memos (refunds), and inventory. The adapter supports order management, customer service, product inquiries, and inventory checks through voice conversations. Magento's API is more enterprise-oriented than Shopify or WooCommerce, with complex authentication (OAuth 1.0a or bearer tokens), granular ACL-based permissions, and support for multi-website/multi-store configurations.

Magento's architecture includes several unique concepts: website/store/store view hierarchy, customer groups and shared catalogs, configurable products with associated simple products, bundle products and grouped products, tier pricing and customer group pricing, and integration with enterprise ERP through message queues. The adapter must handle Magento's complex product types — a "configurable product" inquiry requires checking multiple associated simple products for variant availability.

## Architecture

```
                    Magento Integration Architecture

   Voice Agent → Commerce Intent → Magento Adapter → Magento REST API
        |
        v
   +------------------+     +------------------+
   | Magento Adapter   | --> | REST API (V1)    |
   | • Order lookup    |     | • Orders         |
   | • Customer mgmt   |     | • Products       |
   | • Inventory       |     | • Customers      |
   | • Returns/RMA     |     | • Inventory      |
   +------------------+     | • Credit Memos   |
        |                   +------------------+
        v
   +------------------+
   | Integration       |
   | • Admin token     |
   | • Website scope   |
   | • Store context   |
   +------------------+
```

## Design Decisions

- **Admin bearer token for server-to-server integration:** Magento supports admin bearer tokens (created via POST /V1/integration/admin/token) for service integrations. The adapter authenticates once per session and caches the token. Tokens are scoped to the integration's API resources as configured in the Magento admin panel. For multi-website Magento instances, the token's scope determines which websites are accessible. Trade-off: bearer tokens are simpler than OAuth 1.0a but require careful token management and rotation.

- **Website-aware queries for multi-store Magento:** Magento supports multiple websites and store views under a single installation. The adapter includes the store ID or website code in API requests to scope queries correctly. Customer and order lookups are scoped to the appropriate website based on integration configuration or call context. Trade-off: website-scoped queries add a required parameter to most API calls but prevent cross-website data leakage.

- **Configurable product resolution with stock calculation:** When querying a configurable product (e.g., "blue shirt in size M"), the adapter resolves the configurable product to its child simple products and checks stock for each combination. The adapter returns a structured response listing available options and their stock status. This enables the voice agent to guide the caller through variant selection. Trade-off: configurable product resolution requires multiple API calls (parent product → children → stock for each child).

## Implementation Approach

```
class MagentoAdapter extends BaseAdapter {
  private baseUrl: string;
  private adminToken: string;

  async initialize(config: MagentoConfig) {
    this.baseUrl = `${config.storeUrl}/rest/${config.storeCode || 'default'}`;
    await this.authenticate();
  }

  private async authenticate() {
    const response = await this.execute({
      method: 'POST',
      url: `${this.baseUrl}/V1/integration/admin/token`,
      data: { username: this.config.adminUsername, password: this.config.adminPassword }
    });
    this.adminToken = response.data;
  }

  private async request(method: string, path: string, data?: any): Promise<any> {
    return this.execute({
      method, url: `${this.baseUrl}/V1${path}`, data,
      headers: { Authorization: `Bearer ${this.adminToken}`, 'Content-Type': 'application/json' }
    });
  }

  async getOrderByIncrementId(incrementId: string): Promise<AdapterResponse<OrderData>> {
    // Magento uses increment IDs (order numbers visible to customer)
    const response = await this.request('GET', `/orders?searchCriteria[filter_groups][0][filters][0][field]=increment_id&searchCriteria[filter_groups][0][filters][0][value]=${incrementId}`);
    return { success: true, data: this.mapOrder(response.data.items[0]) };
  }

  async getCustomerByEmail(email: string): Promise<AdapterResponse<CustomerData | null>> {
    const response = await this.request('GET', `/customers/search?searchCriteria[filter_groups][0][filters][0][field]=email&searchCriteria[filter_groups][0][filters][0][value]=${email}`);
    return { success: true, data: response.data.items?.[0] ? this.mapCustomer(response.data.items[0]) : null };
  }

  async getProductOptions(configurableSku: string): Promise<AdapterResponse<{
    attributes: { code: string; label: string; options: { value: string; label: string }[] }[];
    stockByOption: Record<string, number>;
  }>> {
    // Get configurable product options
    const productResponse = await this.request('GET', `/products/${configurableSku}`);
    const product = productResponse.data;
    const extensionAttrs = product.extension_attributes;

    // Get child products
    const children = extensionAttrs.configurable_product_links || [];
    const stockData: Record<string, number> = {};

    for (const childId of children) {
      const childResponse = await this.request('GET', `/products/${childId}`);
      const childSku = childResponse.data.sku;
      const stockResponse = await this.request('GET', `/stockItems/${childId}`);
      stockData[childSku] = stockResponse.data.qty || 0;
    }

    return {
      success: true,
      data: {
        attributes: extensionAttrs.configurable_product_options?.map(opt => ({
          code: opt.attribute_code,
          label: opt.label,
          options: opt.values?.map(v => ({ value: v.value_index, label: v.label })) || []
        })) || [],
        stockByOption: stockData
      }
    };
  }

  async createCreditMemo(invoiceId: number, items: { orderItemId: number; qty: number }[], reason: string): Promise<AdapterResponse<{ creditMemoId: number }>> {
    const response = await this.request('POST', `/creditmemo`, {
      invoice_id: invoiceId,
      items: items.map(i => ({ order_item_id: i.orderItemId, qty: i.qty })),
      comment: { comment: reason, is_visible_on_front: 0 }
    });
    return { success: true, data: { creditMemoId: response.data.entity_id } };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Axios** (MIT) | HTTP client | REST API communication |
| **Redis** (BSD) | Cache | Token and product cache |

## Production Considerations

**Scaling:** Magento API performance varies significantly with hosting and caching configuration. Magento's full-page cache does not apply to API requests. Implement aggressive response caching (product data, customer data). Use Magento's async API (POST /V1/async/bulk) for batch operations.

**Security:** Admin bearer tokens provide broad access. Use a dedicated integration with minimum required ACL resources. Rotate admin credentials regularly. Monitor for API requests from unexpected IPs.

**Monitoring:** Track API response times (Magento can be slow without proper caching), admin token expiration and renewal, configurable product resolution latency, and error rates by endpoint. Alert on authentication failures (token expired or invalid), API response times exceeding 15 seconds, and high error rates from the Magento instance.
