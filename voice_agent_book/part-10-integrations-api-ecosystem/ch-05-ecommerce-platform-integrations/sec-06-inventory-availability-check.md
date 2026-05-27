# Section 06: Inventory Availability Check

## Overview

Inventory availability checking enables callers to verify product stock levels across warehouses and locations through voice conversations. The inventory service answers questions like "Do you have this in stock?", "Is the blue shirt available in size M?", "When will it be back in stock?", and "Which store has it available?" The service aggregates inventory data from the e-commerce platform's inventory system, potentially across multiple warehouses, retail locations, and dropshipping partners.

Inventory checking involves resolving product variants (size, color, configuration), querying stock levels across locations, considering safety stock and allocation (reserved for existing orders), and computing realistic availability estimates (not just binary in/out-of-stock). The service supports back-in-stock notifications — when an item is out of stock, the caller can request notification when it's available again. The service also handles pre-order items where stock is expected but not yet received.

## Architecture

```
                    Inventory Availability Check

   Caller: "Is this in stock?"
        |
        v
   +------------------+
   | Product Resolution|
   | • SKU lookup      |
   | • Variant config  |
   | • Bundle products |
   +------------------+
        |
        v
   +------------------+
   | Inventory Query   |
   | • E-commerce API  |
   | • WMS integration |
   | • Multi-warehouse |
   +------------------+
        |
        v
   +------------------+
   | Availability Calc |
   | • Stock - Reserve |
   | • Safety stock    |
   | • In-transit stock|
   | • Pre-order stock |
   +------------------+
        |
        v
   +------------------+     +------------------+
   | Response         |     | Back-in-Stock    |
   | • Quantity       |     | Notification     |
   | • Locations      |     | Registration     |
   | • ETA for restock|     |                  |
   +------------------+     +------------------+
```

## Design Decisions

- **Real-time inventory queries with brief caching:** Inventory data changes in real-time (orders consume stock). The service queries the e-commerce platform's real-time inventory API for each check. Results are cached for only 30-60 seconds to balance accuracy with API load. For high-traffic products, consider using a webhook-driven inventory cache that updates on stock changes. Trade-off: real-time queries increase API load but provide accurate availability information.

- **Multi-location inventory with unified availability view:** Many merchants operate multiple warehouses, retail stores, and dropshipping partners. The inventory service queries all locations and presents a unified view with location breakdown. Availability can be filtered by geographical proximity (find a store near the caller with stock). Location-specific availability enables "buy online, pick up in store" (BOPIS) workflows. Trade-off: multi-location queries multiply API calls but enable location-aware fulfillment.

- **Allocation-aware stock calculation:** Not all inventory is available for sale — some stock is reserved for existing orders (unfulfilled), allocated to bundles/kits, or held as safety stock. The inventory service calculates "available to promise" (ATP) by subtracting allocated quantities from current stock. ATP = on_hand - reserved - allocated - safety_stock. This provides a more accurate availability picture than raw stock levels. Trade-off: ATP calculation requires understanding the merchant's allocation logic, which varies by platform and configuration.

## Implementation Approach

```
interface InventoryRequest {
  productId?: string;
  sku: string;
  variantOptions?: { attribute: string; value: string }[];
  locationFilter?: { type: 'nearby' | 'warehouse' | 'store'; coordinates?: { lat: number; lng: number }; radiusKm?: number };
}

interface InventoryResult {
  sku: string;
  productName: string;
  available: boolean;
  availableQuantity: number;
  locations: {
    id: string; name: string; type: string;
    quantity: number; available: number;
    distanceKm?: number;
  }[];
  estimatedRestock?: { date: string; quantity: number };
  preOrderAvailable: boolean;
  preOrderEta?: string;
}

class InventoryService {
  async checkAvailability(request: InventoryRequest): Promise<AdapterResponse<InventoryResult>> {
    const cacheKey = `inventory:${request.sku}:${JSON.stringify(request.variantOptions)}`;
    const cached = await this.cache.get(cacheKey);
    if (cached) return { success: true, data: JSON.parse(cached) };

    // Get product info and resolve SKU
    const product = await this.resolveProduct(request);
    if (!product) return { success: true, data: null };

    // Query inventory across locations
    const adapter = this.adapterFactory.getAdapter(product.platform);
    const inventoryData = await adapter.getInventoryBySku(product.sku);

    // Calculate available-to-promise
    const locations = inventoryData.map(loc => ({
      ...loc,
      available: loc.quantity - (loc.reserved || 0) - (loc.safetyStock || 0)
    }));

    const totalAvailable = locations.reduce((sum, l) => sum + Math.max(0, l.available), 0);
    const inStockLocations = locations.filter(l => l.available > 0);

    const result: InventoryResult = {
      sku: product.sku,
      productName: product.name,
      available: totalAvailable > 0,
      availableQuantity: totalAvailable,
      locations: inStockLocations,
      estimatedRestock: product.restockDate ? { date: product.restockDate, quantity: product.restockQty } : undefined,
      preOrderAvailable: product.preOrder || false,
      preOrderEta: product.preOrderEta
    };

    await this.cache.set(cacheKey, JSON.stringify(result), request.locationFilter ? 5 : 30);
    return { success: true, data: result };
  }

  private async resolveProduct(request: InventoryRequest): Promise<{ platform: string; sku: string; name: string; restockDate?: string; restockQty?: number; preOrder?: boolean; preOrderEta?: string } | null> {
    if (request.sku) {
      // Query all connected platforms for this SKU
      const adapters = this.adapterFactory.getAllAdapters();
      for (const adapter of adapters) {
        const product = await adapter.getProductBySku(request.sku);
        if (product.data) return product.data;
      }
    }

    if (request.variantOptions?.length) {
      // Resolve variant: e.g., "shirt, blue, M" → SKU "SHIRT-BLU-M"
      const resolvedSku = await this.variantResolver.resolve(request);
      if (resolvedSku) return this.resolveProduct({ ...request, sku: resolvedSku });
    }

    return null;
  }

  async registerBackInStock(request: { sku: string; email: string; phone?: string }): Promise<AdapterResponse<void>> {
    // Check if already registered
    const existing = await this.notificationStore.findBySkuAndContact(request.sku, request.email);
    if (existing) return { success: true, data: undefined };

    // Register for notification
    await this.notificationStore.create({
      sku: request.sku, email: request.email, phone: request.phone,
      createdAt: new Date().toISOString(), notified: false
    });

    // Monitor stock for this SKU
    await this.startStockMonitoring(request.sku);
    return { success: true, data: undefined };
  }

  private async startStockMonitoring(sku: string) {
    const existing = await this.monitorStore.isMonitoring(sku);
    if (existing) return;
    // Schedule periodic stock check via BullMQ
    await this.queue.add('monitor_stock', { sku }, {
      repeat: { every: 3600000 }, // Every hour
      removeOnComplete: true
    });
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Redis** (BSD) | Cache | Inventory result caching |
| **BullMQ** (MIT) | Queue | Stock monitoring jobs |
| **Axios** (MIT) | HTTP client | E-commerce API communication |

## Production Considerations

**Scaling:** Inventory queries for configurable products (multiple variants) can generate many API calls. Cache resolved variant-to-SKU mappings permanently (they rarely change). Cache inventory results with short TTL appropriate for the merchant's sales velocity.

**Security:** Inventory data may be commercially sensitive (stock levels, restock dates). Restrict access to authenticated merchants and their customers. Do not expose exact stock levels for low-inventory items (may encourage competitors). Consider showing "Low Stock" vs. exact quantities.

**Monitoring:** Track inventory query volume, cache hit rate, variant resolution success rate, back-in-stock registration rate, and stock monitoring job execution. Alert on variant resolution failures (may indicate product data issues), and stock monitoring job failures (missed restock events).
