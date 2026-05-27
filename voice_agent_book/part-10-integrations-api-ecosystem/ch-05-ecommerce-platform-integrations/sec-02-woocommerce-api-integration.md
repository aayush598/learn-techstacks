# Section 02: WooCommerce API Integration

## Overview

WooCommerce API integration connects the voice platform with WooCommerce-powered WordPress stores. WooCommerce provides a comprehensive REST API covering orders, products, customers, coupons, refunds, shipping, and taxonomies. The adapter enables order lookup and status, customer management, product inquiries, return processing, and inventory checks through voice conversations.

WooCommerce's API differs from Shopify's in several ways: it uses WordPress-style authentication (Consumer Key + Consumer Secret via OAuth 1.0a), the API is REST-only (no GraphQL), it supports WordPress multisite networks, and the data model includes WordPress-specific concepts (post types, taxonomies, meta fields). The adapter must handle WooCommerce's extension ecosystem — many stores have custom fields and product types from plugins. The adapter also handles the WordPress user model where customers can be either registered users (with accounts) or guest customers (with just an email).

## Architecture

```
                    WooCommerce Integration Architecture

   Voice Agent → Commerce Intent → WooCommerce Adapter → WooCommerce REST API
        |
        v
   +------------------+     +------------------+
   | WooCommerce       | --> | REST API (v3)    |
   | Adapter           |     | • Orders         |
   | • Order lookup    |     | • Products       |
   | • Customer mgmt   |     | • Customers      |
   | • Refund/RMA      |     | • Refunds        |
   | • Inventory       |     +------------------+
   +------------------+
        |
        v
   +------------------+
   | Webhooks         |
   | (WordPress       |
   |  webhook system) |
   +------------------+
```

## Design Decisions

- **OAuth 1.0a auto-signing for API requests:** WooCommerce uses OAuth 1.0a for API authentication, which requires signing each request with the consumer key and secret. The adapter automatically handles the signing process for every outgoing request, including generating the OAuth nonce, timestamp, and signature. This is transparent to the rest of the platform. Trade-off: OAuth 1.0a signing adds overhead per request but is more secure than API keys transmitted in the clear.

- **Meta field discovery for custom plugin data:** WooCommerce stores plugin-specific data in order and product meta fields. The adapter uses the `_` prefix convention (protected meta) and the `meta_data` API response to discover available fields. If the integration configuration specifies expected meta fields, the adapter includes them in API requests. This enables the platform to access custom data from subscription plugins, booking plugins, and custom field plugins. Trade-off: meta field discovery requires per-store customization and may change when plugins update.

- **Webhook-based order synchronization:** WooCommerce's built-in webhook system sends real-time notifications for order lifecycle events (created, updated, deleted, refunded). The adapter registers webhooks for these topics during initialization. Webhooks are sent as POST requests to the platform's endpoint with WooCommerce's HMAC signature for verification. Trade-off: WooCommerce webhook delivery is less reliable than Shopify's — implement a periodic reconciliation sync as backup.

## Implementation Approach

```
class WooCommerceAdapter extends BaseAdapter {
  private baseUrl: string;

  async initialize(config: WooCommerceConfig) {
    this.baseUrl = `${config.storeUrl}/wp-json/wc/v3`;
  }

  private async request(method: string, path: string, data?: any): Promise<any> {
    const url = `${this.baseUrl}${path}`;
    const params = {
      oauth_consumer_key: this.config.consumerKey,
      oauth_timestamp: Math.floor(Date.now() / 1000),
      oauth_nonce: crypto.randomBytes(16).toString('hex'),
      oauth_signature_method: 'HMAC-SHA256',
      oauth_version: '1.0'
    };
    const signature = this.signOAuth(method, url, params, data);
    return this.execute({
      method, url, data,
      headers: { Authorization: `OAuth ${this.formatOAuthParams({ ...params, oauth_signature: signature })}` }
    });
  }

  async getOrder(orderId: number): Promise<AdapterResponse<OrderData>> {
    const response = await this.request('GET', `/orders/${orderId}`);
    return { success: true, data: this.mapOrder(response.data) };
  }

  async getOrderByNumber(orderNumber: string): Promise<AdapterResponse<OrderData | null>> {
    const response = await this.request('GET', '/orders', { search: orderNumber });
    return { success: true, data: response.data.length > 0 ? this.mapOrder(response.data[0]) : null };
  }

  async getCustomerByEmail(email: string): Promise<AdapterResponse<CustomerData | null>> {
    const response = await this.request('GET', '/customers', { email });
    return { success: true, data: response.data.length > 0 ? this.mapCustomer(response.data[0]) : null };
  }

  async processRefund(orderId: number, refundData: {
    amount: string; reason: string; lineItems?: { id: number; quantity: number }[];
  }): Promise<AdapterResponse<{ refundId: number }>> {
    const response = await this.request('POST', `/orders/${orderId}/refunds`, {
      amount: refundData.amount,
      reason: refundData.reason,
      line_items: refundData.lineItems?.map(i => ({ id: i.id, quantity: i.quantity }))
    });
    return { success: true, data: { refundId: response.data.id } };
  }

  async getProductBySku(sku: string): Promise<AdapterResponse<ProductData | null>> {
    const response = await this.request('GET', '/products', { sku });
    return { success: true, data: response.data.length > 0 ? this.mapProduct(response.data[0]) : null };
  }

  async checkStock(sku: string): Promise<AdapterResponse<{ inStock: boolean; quantity: number }>> {
    const product = await this.getProductBySku(sku);
    if (!product.data) return { success: true, data: { inStock: false, quantity: 0 } };
    return { success: true, data: { inStock: product.data.stockStatus === 'instock', quantity: product.data.stockQuantity } };
  }

  private signOAuth(method: string, url: string, params: any, body?: any): string {
    const sortedParams = Object.keys(params).sort().map(k => `${k}=${params[k]}`).join('&');
    const signatureBase = `${method.toUpperCase()}&${encodeURIComponent(url)}&${encodeURIComponent(sortedParams)}`;
    return crypto.createHmac('sha256', this.config.consumerSecret).update(signatureBase).digest('base64');
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Axios** (MIT) | HTTP client | REST API communication |
| **oauth-1.0a** (MIT) | Auth | OAuth 1.0a signing |
| **Redis** (BSD) | Cache | Product/customer cache |

## Production Considerations

**Scaling:** WooCommerce REST API performance depends on the underlying WordPress hosting. Rate limits are typically configured at the server level (Apache/Nginx), not by WooCommerce itself. Implement client-side throttling to avoid overwhelming shared hosting. Cache product queries aggressively. Use WooCommerce's `_fields` parameter to request only needed fields.

**Security:** WooCommerce consumer keys and secrets provide admin-level API access. Store encrypted. Rotate keys periodically. Use HTTPS-only communication. Webhook verification uses HMAC-SHA256 with the consumer secret.

**Monitoring:** Track API response times (varies significantly based on hosting), order lookup volume, refund processing rate, cache hit rates, and webhook delivery reliability. Alert on API response times exceeding 10 seconds (common for poorly hosted WooCommerce stores), authentication failures, and excessive order lookup failures.
