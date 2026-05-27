# Section 04: Order Lookup & Status

## Overview

Order lookup and status queries enable callers to check their order information through voice conversations. This is one of the most common e-commerce voice use cases — customers call to ask "Where is my order?", "When will it arrive?", "Can I change my shipping address?", or "Why was my order cancelled?" The order lookup service provides a unified interface across connected e-commerce platforms (Shopify, WooCommerce, Magento) for querying orders by order number, customer email, phone number, or date range.

The order lookup service retrieves comprehensive order information: current status (pending, processing, shipped, delivered, cancelled), fulfillment status (fulfilled, partial, unfulfilled), payment status (paid, authorized, refunded, partially refunded), shipping details (carrier, tracking number, estimated delivery), line items (products, quantities, prices), and order timeline (creation, payment, fulfillment, shipment events). The service also enables proactive status checks — scheduled jobs can monitor order statuses and trigger notifications or follow-up calls when statuses change.

## Architecture

```
                    Order Lookup & Status Architecture

   Caller: "Where is my order?"
        |
        v
   +------------------+
   | Order Lookup      |
   | • By order number |
   | • By email/phone  |
   | • By date range   |
   +------------------+
        |
        v
   +----------------------------------------------------+
   |              Order Status Engine                    |
   |                                                    |
   |  +------------------+  +------------------+        |
   |  | E-Commerce       |  | Status           |        |
   |  | Adapter Router   |  | Normalizer       |        |
   |  | • Shopify        |  | • Shop: "fulfilled"|       |
   |  | • WooCommerce    |  | • WC: "completed" |       |
   |  | • Magento        |  | • Mag: "complete" |       |
   |  +------------------+  +------------------+        |
   |  +------------------+  +------------------+        |
   |  | Enrichment       |  | Response Builder |        |
   |  | • Tracking       |  | • Text summary   |        |
   |  | • ETA from carrier|  | • Structured     |        |
   |  | • Return eligibility| |   data          |        |
   |  +------------------+  +------------------+        |
   +----------------------------------------------------+
```

## Design Decisions

- **Unified order model across e-commerce platforms:** Each platform has different status values, field names, and data structures. The order lookup service normalizes all responses into a canonical order model. Status values are mapped to standard states (pending, processing, completed, cancelled, refunded). Platform-specific details are preserved in a metadata map. Trade-off: some platform-specific status nuance may be lost in normalization.

- **Carrier tracking integration for estimated delivery:** After retrieving tracking numbers from the e-commerce platform, the service queries carrier APIs (UPS, FedEx, USPS, DHL) for detailed tracking events and estimated delivery dates. This provides more accurate information than what the e-commerce platform stores. Tracking results are cached per tracking number for 1 hour. Trade-off: carrier API calls add latency and cost but provide superior tracking information.

- **Proactive order status monitoring with webhook and polling:** The service monitors order status changes via e-commerce webhooks (real-time) and periodic polling (fallback). When a status change is detected (e.g., "shipped"), the service can trigger notifications (SMS, email) or schedule follow-up calls (satisfaction survey after delivery). Monitoring is configurable per merchant and per order status. Trade-off: proactive monitoring adds infrastructure complexity but enables automated customer outreach.

## Implementation Approach

```
interface OrderLookupRequest {
  queryType: 'order_number' | 'email' | 'phone' | 'date_range';
  queryValue: string;
  dateRange?: { start: string; end: string };
  platform?: string;       // Specific platform or 'all'
}

interface CanonicalOrder {
  platform: string;
  orderNumber: string;
  externalId: string;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled' | 'refunded' | 'on_hold';
  paymentStatus: 'paid' | 'authorized' | 'refunded' | 'partial_refund' | 'unpaid';
  fulfillmentStatus: 'fulfilled' | 'partial' | 'unfulfilled';
  createdAt: string;
  updatedAt: string;
  customer: { name: string; email: string; phone?: string };
  shippingAddress: { address1: string; city: string; state: string; zip: string; country: string };
  lineItems: { name: string; sku: string; quantity: number; price: number }[];
  totals: { subtotal: number; shipping: number; tax: number; total: number; currency: string };
  tracking: { carrier?: string; trackingNumber?: string; estimatedDelivery?: string; events: { date: string; description: string }[] };
  metadata: Record<string, any>;
}

class OrderLookupService {
  async lookupOrder(request: OrderLookupRequest): Promise<AdapterResponse<CanonicalOrder[]>> {
    const platforms = request.platform
      ? [this.adapterFactory.getAdapter(request.platform)]
      : this.adapterFactory.getAllAdapters();

    const results = await Promise.all(
      platforms.map(async (adapter) => {
        try {
          switch (request.queryType) {
            case 'order_number':
              return adapter.getOrderByNumber(request.queryValue);
            case 'email':
              return adapter.getOrdersByEmail(request.queryValue);
            default:
              return { success: false, data: [] };
          }
        } catch (error) {
          return { success: false, data: [], error: error.message };
        }
      })
    );

    const orders = results
      .filter(r => r.success && r.data)
      .map(r => this.normalizeOrder(r.data))
      .flat();

    // Enrich with tracking data
    for (const order of orders) {
      if (order.tracking?.trackingNumber) {
        await this.enrichTracking(order);
      }
    }

    return { success: true, data: orders };
  }

  private async enrichTracking(order: CanonicalOrder): Promise<void> {
    const cacheKey = `tracking:${order.tracking.carrier}:${order.tracking.trackingNumber}`;
    const cached = await this.cache.get(cacheKey);
    if (cached) {
      order.tracking.events = JSON.parse(cached);
      return;
    }

    try {
      const carrierAdapter = this.carrierRegistry.get(order.tracking.carrier);
      const events = await carrierAdapter.getTracking(order.tracking.trackingNumber);
      order.tracking.events = events;
      order.tracking.estimatedDelivery = events.find(e => e.type === 'delivered')?.date
        || events.find(e => e.type === 'estimated_delivery')?.date;
      await this.cache.set(cacheKey, JSON.stringify(events), 3600);
    } catch (error) {
      // Tracking enrichment failure is non-fatal
      Logger.warn(`Tracking enrichment failed for ${order.orderNumber}`, error);
    }
  }

  private normalizeOrder(rawOrder: any): CanonicalOrder[] {
    // Platform-specific normalization to canonical model
    const platform = rawOrder.platform || rawOrder.source;
    const orders = Array.isArray(rawOrder) ? rawOrder : [rawOrder];
    return orders.map(o => ({
      platform: o.platform || 'unknown',
      orderNumber: o.name || o.orderNumber || o.increment_id,
      externalId: o.id,
      status: this.mapStatus(o.status || o.order_status, platform),
      paymentStatus: this.mapPaymentStatus(o.financial_status || o.payment_status, platform),
      fulfillmentStatus: this.mapFulfillmentStatus(o.fulfillment_status || o.fulfillment, platform),
      createdAt: o.created_at || o.createdAt,
      updatedAt: o.updated_at || o.updatedAt,
      customer: { name: o.customer?.name, email: o.email || o.customer?.email, phone: o.phone || o.customer?.phone },
      shippingAddress: o.shipping_address || {},
      lineItems: (o.line_items || o.items || []).map(i => ({ name: i.name || i.product_name, sku: i.sku, quantity: i.quantity, price: parseFloat(i.price) })),
      totals: { subtotal: 0, shipping: 0, tax: 0, total: parseFloat(o.total_price || o.grand_total || 0), currency: o.currency },
      tracking: { carrier: o.carrier, trackingNumber: o.tracking_number, events: [] },
      metadata: o.metadata || o.extension_attributes || {}
    }));
  }

  private mapStatus(status: string, platform: string): CanonicalOrder['status'] {
    const statusMap = {
      shopify: { pending: 'pending', processing: 'processing', fulfilled: 'shipped', delivered: 'delivered', cancelled: 'cancelled', refunded: 'refunded' },
      woocommerce: { pending: 'pending', processing: 'processing', 'on-hold': 'on_hold', completed: 'delivered', cancelled: 'cancelled', refunded: 'refunded' },
      magento: { pending: 'pending', processing: 'processing', complete: 'delivered', cancelled: 'cancelled', closed: 'delivered' }
    };
    return statusMap[platform]?.[status?.toLowerCase()] || 'processing';
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Redis** (BSD) | Cache | Tracking cache and order state |
| **BullMQ** (MIT) | Queue | Status monitoring jobs |
| **Axios** (MIT) | HTTP client | Carrier API integration |

## Production Considerations

**Scaling:** Order lookup may query multiple e-commerce platforms in parallel. Cache order results for 30 seconds to handle repeated queries for the same order. Tracking enrichment should be done asynchronously — show basic order info immediately, enrich tracking data when available.

**Security:** Order data contains PII (customer name, address, payment status). Restrict order lookup access to authenticated callers (verify phone number or email matches the order). Log all order lookup attempts for fraud monitoring.

**Monitoring:** Track order lookup volume by platform, lookup success rate, enrichment latency (tracking data), and cache hit rates. Alert on high lookup failure rates (may indicate e-commerce platform issues) and tracking enrichment failures.
