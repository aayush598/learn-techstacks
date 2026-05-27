# Section 01: Shopify REST & GraphQL Integration

## Overview

Shopify integration connects the voice platform with Shopify's commerce platform, enabling order management, customer service, and product inquiries through voice conversations. Shopify provides both REST and GraphQL APIs — REST for simpler CRUD operations and GraphQL for complex queries involving nested resources (order with line items, fulfillment status, customer data). The adapter supports order lookup by number or customer, order status checks, return/refund processing, inventory availability queries, customer account management, and product information retrieval.

Shopify's API has specific characteristics: REST uses admin API scopes with per-request OAuth tokens, GraphQL uses a single endpoint with persistent queries for performance, rate limits are per-store (40 requests per second for REST, 1000 cost points per second for GraphQL), and the API supports both online (instant) and offline (long-lived) access tokens. The adapter must handle Shopify's unique resource hierarchy: products have variants, orders have fulfillments and transactions, customers have addresses and saved payment methods.

## Architecture

```
                    Shopify Integration Architecture

   Voice Agent → Commerce Intent → Shopify Adapter → Shopify API
        |
        v
   +------------------+     +------------------+
   | Shopify Adapter   | --> | REST API         |
   | • Order lookup    |     | (admin REST)     |
   | • Return/RMA      |     |                  |
   | • Inventory       | --> | GraphQL Admin    |
   | • Customer mgmt   |     | API              |
   | • Product info    |     +------------------+
   +------------------+
        |
        v
   +------------------+
   | Webhook Processor|
   | • Order updates  |
   | • Fulfillment    |
   | • Inventory      |
   +------------------+
```

## Design Decisions

- **GraphQL for complex queries, REST for simple operations:** Order lookup with line items, fulfillment status, and customer data is a single GraphQL query vs. 3-4 REST calls. Product variant inventory checks use GraphQL for batch efficiency. Simple operations (create customer, create order note) use REST for simplicity. Trade-off: maintaining two API styles increases adapter code but optimizes for both simple and complex scenarios.

- **Webhook-based order status change detection:** Shopify sends real-time webhooks for order creation, fulfillment, cancellation, and refund. The adapter registers webhooks for relevant topics (orders/create, orders/updated, fulfillments/create). Webhook payloads include the full order object, enabling immediate action without API calls. Webhook verification uses Shopify's HMAC-SHA256 signature. Trade-off: webhooks require a publicly accessible endpoint and can be lost if the platform is down.

- **Access token management per store:** Each Shopify store has its own API credentials and access token (given during OAuth install). The adapter maintains a token registry mapping store domains to tokens. When processing call context, the system determines which store the customer belongs to (based on URL, customer record, or campaign configuration) and uses the appropriate token. Trade-off: multi-store management adds complexity but is required for multi-tenant commerce platforms.

## Implementation Approach

```
class ShopifyAdapter extends BaseAdapter {
  private graphqlEndpoint: string;
  private restEndpoint: string;

  async initialize(config: ShopifyConfig) {
    this.graphqlEndpoint = `https://${config.storeDomain}/admin/api/2024-01/graphql.json`;
    this.restEndpoint = `https://${config.storeDomain}/admin/api/2024-01`;
  }

  async getOrderByOrderNumber(orderNumber: string): Promise<AdapterResponse<OrderData>> {
    const query = `
      query getOrder($orderNumber: String!) {
        orders(first: 1, query: "name:${orderNumber}") {
          edges {
            node {
              id, name, email, phone, totalPriceSet { presentmentMoney { amount currencyCode } }
              createdAt, displayFulfillmentStatus, displayFinancialStatus
              lineItems(first: 10) { edges { node { name quantity } } }
              customer { id firstName lastName email phone }
              shippingAddress { address1 city provinceCode countryCode zip }
            }
          }
        }
      }`;
    const response = await this.graphql(query);
    const order = response.data.orders.edges[0]?.node;
    return { success: true, data: order ? this.mapOrder(order) : null };
  }

  async getInventoryBySku(skus: string[]): Promise<AdapterResponse<InventoryData[]>> {
    const query = `
      query getInventory($skus: [String!]!) {
        productVariants(first: 50, query: { skus: $skus }) {
          edges { node { id sku displayName inventoryQuantity } }
        }
      }`;
    const response = await this.graphql(query, { skus });
    return { success: true, data: response.data.productVariants.edges.map(e => ({
      sku: e.node.sku, name: e.node.displayName, quantity: e.node.inventoryQuantity
    })) };
  }

  async processReturn(orderId: string, items: { lineItemId: string; quantity: number }[], reason: string): Promise<AdapterResponse<{ returnId: string }>> {
    const mutation = `
      mutation createReturn($returnInput: ReturnInput!) {
        returnCreate(returnInput: $returnInput) {
          return { id status }
          userErrors { field message }
        }
      }`;
    const response = await this.graphql(mutation, {
      returnInput: { orderId, returnLineItems: items.map(i => ({
        lineItemId: i.lineItemId, quantity: i.quantity
      })), returnReason: reason }
    });
    return { success: true, data: { returnId: response.data.returnCreate.return.id } };
  }

  async getCustomerByEmail(email: string): Promise<AdapterResponse<CustomerData | null>> {
    const response = await this.restGet(`/customers/search.json?query=email:${email}`);
    return { success: true, data: response.data.customers?.[0] ? this.mapCustomer(response.data.customers[0]) : null };
  }

  private async graphql(query: string, variables?: any): Promise<any> {
    return this.execute({
      method: 'POST', url: this.graphqlEndpoint,
      data: { query, variables },
      headers: { 'X-Shopify-Access-Token': this.config.accessToken, 'Content-Type': 'application/json' }
    });
  }

  private async restGet(path: string): Promise<any> {
    return this.execute({
      method: 'GET', url: `${this.restEndpoint}${path}`,
      headers: { 'X-Shopify-Access-Token': this.config.accessToken }
    });
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Axios** (MIT) | HTTP client | REST API communication |
| **graphql-request** (MIT) | GraphQL | GraphQL client |
| **Redis** (BSD) | Cache | Product/customer cache |

## Production Considerations

**Scaling:** Shopify rate limits are 40 requests/second for REST and 1000 cost points/second for GraphQL (query cost varies). Monitor cost points per query and optimize expensive GraphQL queries. Cache product information (infrequently changed) for 5-15 minutes. Use Shopify's Bulk API for large data operations.

**Security:** Shopify access tokens provide full admin access to the store. Store tokens encrypted. Implement OAuth install flow for multi-store scenarios. Use Shopify's HMAC webhook verification. Monitor for unusual API patterns that may indicate token compromise.

**Monitoring:** Track API request volume (REST vs. GraphQL), GraphQL query cost points, cache hit rate for product/customer data, webhook delivery reliability, and error rates by endpoint. Alert on rate limit throttling, GraphQL query costs approaching limits, and webhook verification failures.
