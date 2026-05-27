# Section 06: Inventory Synchronization

## Overview

Inventory synchronization ensures that voice agents have real-time access to product availability data across all sales channels. When a customer calls to inquire about a product or place an order, the voice agent must provide accurate stock information — available quantity, expected restock dates, and location-specific availability. The inventory sync engine connects to each ERP adapter and maintains a synchronized view of inventory data, handling the complexities of multi-warehouse inventory, batch/lot tracking, and reservation management.

The synchronization engine supports both real-time lookups (direct ERP queries during a live call) and batch sync (periodic full inventory dumps for offline processing). It maintains an inventory cache that reduces latency during voice calls while ensuring data freshness through TTL-based invalidation and change data capture (CDC) where supported by the ERP. The engine also handles inventory reservation during order placement — reducing available quantity to prevent overselling across channels.

## Architecture

```
                 Inventory Synchronization Engine

   Voice Agent ←→ Inventory Service ←→ ERP Adapter ←→ ERP System
                      |
   +----------------------------------------------------------+
   |              Inventory Sync Architecture                 |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Inventory Cache  |  | Real-time Lookup  |            |
   |  | • Redis          |  | • Direct ERP call |            |
   |  | • TTL per SKU   |  | • During call      |            |
   |  | • Stale-while   |  | • On-demand        |            |
   |  |   revalidate    |  +-------------------+            |
   |  +------------------+                                    |
   |  +------------------+  +-------------------+            |
   |  | Batch Sync      |  | Reservation      |              |
   |  | • Daily full    |  | • Hold during call|             |
   |  | • Delta/CDC     |  | • Timeout release |             |
   |  | • CSV import    |  | • Commit/release  |             |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Multi-Warehouse  |  | Status Mgmt       |            |
   |  | • Location tree  |  | • In stock        |            |
   |  | • Primary/backup |  | • Low stock alert |            |
   |  | • Transfer       |  | • Out of stock    |            |
   |  +------------------+  | • Backordered     |            |
   |                        +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **Cache-aside with stale-while-revalidate over write-through caching:** Inventory data is read from the ERP on cache miss, stored in Redis with a short TTL (30 seconds for hot SKUs, 5 minutes for cold SKUs), and served from cache on subsequent reads. The `stale-while-revalidate` pattern allows serving stale data (up to 30 seconds past TTL) while asynchronously refreshing from the ERP. Trade-off: stale reads are possible during ERP latency spikes but provide sub-100ms inventory lookups during voice calls.

- **Optimistic reservation with timeout-based release over pessimistic locking:** When a voice agent begins an order flow, the system reserves the requested quantity with a configurable timeout (default 10 minutes). If the order is not completed (customer hangs up, payment fails), the reservation expires and the quantity is released. The reservation is optimistic — the actual ERP inventory is updated only when the order is confirmed, reducing the risk of locked inventory due to abandoned calls. Trade-off: optimistic can lead to overselling if concurrent calls exceed available stock but maintains ERP performance.

- **ERP-agnostic inventory schema with adapter-specific mapping:** The inventory service defines a canonical inventory record (SKU, quantity, warehouse, status, last updated) that each ERP adapter maps to and from its native format. ERP-specific concepts like SAP's storage location and batch, NetSuite's bin numbering, and Dynamics' warehouse hierarchy are mapped to the canonical schema with metadata preserved in a custom fields map. Trade-off: canonical schema loses some ERP-specific refinements but provides a uniform inventory interface across all ERP types.

## Implementation Approach

```
interface InventoryRecord {
  sku: string;
  productName: string;
  warehouseId: string;
  warehouseName: string;
  quantityAvailable: number;
  quantityOnHand: number;
  quantityCommitted: number;
  quantityOnOrder: number;
  reorderPoint?: number;
  status: 'in_stock' | 'low_stock' | 'out_of_stock' | 'backordered';
  restockDate?: Date;
  unitPrice?: number;
  currency?: string;
  lastUpdated: Date;
  erpSpecific: Record<string, any>;
}

interface InventoryReservation {
  id: string;
  sku: string;
  warehouseId: string;
  quantity: number;
  callSid: string;
  status: 'active' | 'committed' | 'expired' | 'released';
  createdAt: Date;
  expiresAt: Date;
}

class InventorySyncEngine {
  private cache: RedisCache;
  private erpAdapter: BaseERPAdapter;
  private reservations = new Map<string, InventoryReservation>();

  async getInventory(sku: string, warehouseId?: string): Promise<AdapterResponse<InventoryRecord>> {
    const cacheKey = `inv:${sku}:${warehouseId || 'all'}`;
    const cached = await this.cache.get<InventoryRecord>(cacheKey);

    if (cached && !this.isStale(cached)) {
      return { success: true, data: cached };
    }

    const record = await this.erpAdapter.getInventory(sku, warehouseId);
    if (record.success) {
      const reserved = this.getReservedQuantity(sku, warehouseId);
      record.data.quantityAvailable -= reserved;
      record.data.status = this.calculateStatus(record.data);
      await this.cache.set(cacheKey, record.data, { ttl: 30 });
      return record;
    }

    if (cached && this.isWithinStaleWindow(cached)) {
      return { success: true, data: cached, stale: true };
    }

    return { success: false, data: null as any, error: 'Inventory unavailable' };
  }

  async reserveInventory(params: {
    sku: string; warehouseId: string; quantity: number; callSid: string;
  }): Promise<AdapterResponse<InventoryReservation>> {
    const current = await this.getInventory(params.sku, params.warehouseId);
    if (!current.success || current.data.quantityAvailable < params.quantity) {
      return { success: false, data: null as any, error: 'Insufficient inventory' };
    }

    const reservation: InventoryReservation = {
      id: generateId('res'),
      sku: params.sku,
      warehouseId: params.warehouseId,
      quantity: params.quantity,
      callSid: params.callSid,
      status: 'active',
      createdAt: new Date(),
      expiresAt: addMinutes(new Date(), 10),
    };

    this.reservations.set(reservation.id, reservation);
    this.scheduleRelease(reservation.id, reservation.expiresAt);

    await this.evictCache(params.sku, params.warehouseId);
    return { success: true, data: reservation };
  }

  async commitReservation(reservationId: string, orderId: string): Promise<AdapterResponse<void>> {
    const reservation = this.reservations.get(reservationId);
    if (!reservation || reservation.status !== 'active') {
      return { success: false, data: undefined, error: 'Invalid reservation' };
    }

    reservation.status = 'committed';
    await this.erpAdapter.deductInventory({
      sku: reservation.sku,
      warehouseId: reservation.warehouseId,
      quantity: reservation.quantity,
      orderId,
    });

    await this.evictCache(reservation.sku, reservation.warehouseId);
    return { success: true, data: undefined };
  }

  async runDailySync(skus?: string[]): Promise<SyncResult> {
    const allSkus = skus || await this.erpAdapter.getAllActiveSKUs();
    const batchSize = 100;
    let updated = 0;

    for (let i = 0; i < allSkus.length; i += batchSize) {
      const batch = allSkus.slice(i, i + batchSize);
      const records = await this.erpAdapter.batchGetInventory(batch);

      const pipeline = this.cache.pipeline();
      for (const record of records) {
        const cacheKey = `inv:${record.sku}:${record.warehouseId || 'all'}`;
        pipeline.set(cacheKey, record, { ttl: 30 });
      }
      await pipeline.exec();
      updated += records.length;
    }

    return { skusProcessed: allSkus.length, recordsUpdated: updated };
  }

  private getReservedQuantity(sku: string, warehouseId?: string): number {
    let total = 0;
    for (const res of this.reservations.values()) {
      if (res.sku === sku && res.status === 'active') {
        if (!warehouseId || res.warehouseId === warehouseId) {
          total += res.quantity;
        }
      }
    }
    return total;
  }

  private calculateStatus(inv: InventoryRecord): InventoryRecord['status'] {
    if (inv.quantityAvailable <= 0 && inv.quantityOnOrder > 0) return 'backordered';
    if (inv.quantityAvailable <= 0) return 'out_of_stock';
    if (inv.reorderPoint && inv.quantityAvailable <= inv.reorderPoint) return 'low_stock';
    return 'in_stock';
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ioredis (MIT) | Node.js | Redis cache client |
| Cron (MIT) | Node.js | Batch sync scheduler |
| P-map (MIT) | Concurrency | Parallel inventory lookups |

## Production Considerations

**Scaling:** Inventory cache TTL must balance freshness (for voice call accuracy) against ERP load. Hot SKUs (queried frequently) should have shorter TTLs, cold SKUs longer. Use Redis Cluster for horizontal cache scaling. The batch sync should run during off-peak hours (e.g., 3 AM local time per timezone). Implement gradual cache warming — on deployment restart, prime the cache with top-1000 SKUs rather than letting voice calls trigger a thundering herd of cache misses.

**Security:** Inventory data is commercially sensitive — ensure cache access is authenticated. Reservation IDs should be non-guessable (crypto-random). Never expose ERP internal warehouse IDs directly — use a mapping table. Log all inventory adjustments with audit trail (who reserved, which call, how much, when). Implement inventory correction jobs that reconcile cache and reservation state with the ERP system daily.

**Monitoring:** Track cache hit/miss ratio by SKU category, average inventory lookup latency (cached vs. uncached), reservation-to-commit ratio, reservation expiry rate (lost sales), stale read rate, and batch sync duration. Alert on cache hit ratios below 80%, reservation expiry rates above 10%, stale reads exceeding 1%, and batch sync failures. Monitor for inventory drift: discrepancies between cached inventory and ERP-reported inventory.
