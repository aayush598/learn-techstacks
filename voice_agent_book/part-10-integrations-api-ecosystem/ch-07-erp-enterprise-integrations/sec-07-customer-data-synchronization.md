# Section 07: Customer Data Synchronization

## Overview

Customer data synchronization ensures that customer profiles, preferences, and interaction history remain consistent between the voice agent platform and the enterprise ERP/CRM systems. When a customer provides updated information during a call (new address, preferred contact method, recent purchase intent), the sync engine propagates those changes to the connected ERP system in near real-time. Conversely, changes made in the ERP (account status change, credit limit update, segmentation assignment) are synced back to the voice platform to inform future interactions.

The synchronization engine implements a bidirectional sync with conflict resolution, handling entity mapping across heterogeneous systems. A customer might be an "Account" in Salesforce, a "Customer" in SAP, a "Contact" in Dynamics, and a "Customer Record" in NetSuite — the engine maintains a cross-reference mapping (external ID ↔ platform customer ID) and transforms data between each system's schema. The engine also handles related entities: addresses, contacts, communication preferences, and custom fields.

## Architecture

```
              Customer Data Synchronization

   Voice Platform ←→ Sync Engine ←→ ERP System
                        |
   +----------------------------------------------------------+
   |              Customer Sync Architecture                  |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Cross-Reference  |  | Field Mapping     |            |
   |  | Map              |  | Engine            |            |
   |  | • External ID ↔  |  | • Platform → ERP  |           |
   |  |   Platform ID    |  | • ERP → Platform  |           |
   |  | • Type mapping   |  | • Transformation  |           |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Change Detection |  | Conflict Resolver |            |
   |  | • Change Data    |  | • Last-write-wins |            |
   |  |   Capture        |  | • Field-level     |            |
   |  | • Webhook events |  | • Manual override |            |
   |  | • Polling        |  | • Version vectors |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Sync Scheduler   |  | Audit Logger      |            |
   |  | • Real-time      |  | • Change history   |            |
   |  | • Batch (off-peak)|  | • Actor tracking  |            |
   |  | • Full sync      |  | • Rollback plan   |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **Platform as the system of record for profile data, ERP for financial data:** Customer communication preferences, interaction history, and behavioral data (call frequency, preferred language) are maintained in the voice platform and synced to ERP as metadata. Financial data (credit limit, payment terms, tax status) originates in the ERP and is synced to the platform read-only. This split ensures the platform does not overwrite ERP financial data while keeping communication preferences available for voice interactions. Trade-off: dual-system-of-record increases architecture complexity but aligns with each system's strengths.

- **Change Data Capture (CDC) over polling for ERP-to-platform sync:** Where the ERP supports change tracking (Salesforce CDC, Dataverse Change Tracking, SAP CDS delta queries), the sync engine uses CDC to detect changes rather than polling. CDC reduces API consumption and provides sub-minute propagation. For ERPs without CDC support, the engine falls back to timestamp-based polling with configurable intervals (default 5 minutes). Trade-off: CDC requires ERP-specific implementation but provides lower latency and lower API overhead than polling.

- **Field-level conflict resolution with last-write-wins default:** When both the platform and ERP update the same field concurrently, the engine applies last-write-wins based on the update timestamp. Each field is tracked independently — a platform update to email does not conflict with an ERP update to phone. The engine maintains a version vector (field, timestamp, source) for conflict detection. Conflicts are logged for audit and optionally trigger manual review. Trade-off: last-write-wins is simple but may lose updates from the "loser" — field-level granularity reduces this risk compared to record-level resolution.

## Implementation Approach

```
interface SyncEntity {
  entityType: 'customer' | 'contact' | 'address';
  platformId: string;
  externalId: string;
  externalSystem: string;
  fields: Record<string, any>;
  version: Record<string, { value: any; updatedAt: Date; source: string }>;
  lastSyncedAt?: Date;
}

interface SyncChange {
  entityType: string;
  platformId: string;
  externalId: string;
  field: string;
  newValue: any;
  changedAt: Date;
  source: 'platform' | 'erp';
}

class CustomerSyncEngine {
  private db: Database;
  private erpAdapter: BaseERPAdapter;
  private conflictResolver: ConflictResolver;

  async syncFromPlatform(entityType: string, platformId: string): Promise<SyncResult> {
    const entity = await this.db.syncEntities.findOne({ entityType, platformId });
    if (!entity) {
      // New entity — create in ERP
      return this.createInERP(entityType, platformId);
    }

    // Detect changes since last sync
    const currentData = await this.getCurrentPlatformData(entityType, platformId);
    const changes = this.detectChanges(entity, currentData);

    if (changes.length === 0) return { type: 'noop' };

    // Apply changes to ERP
    const erpUpdate = await this.erpAdapter.updateCustomer(entity.externalId, this.buildERPUpdate(changes));
    if (!erpUpdate.success) {
      return { type: 'failed', error: erpUpdate.error };
    }

    // Update sync state
    const now = new Date();
    for (const change of changes) {
      entity.version[change.field] = {
        value: change.newValue,
        updatedAt: now,
        source: 'platform',
      };
    }
    entity.lastSyncedAt = now;
    await this.db.syncEntities.update(entity);

    await this.logSyncChange({ ...changes[0], changedAt: now, source: 'platform' });
    return { type: 'synced', fieldsUpdated: changes.map(c => c.field) };
  }

  async handleERPWebhook(webhookEvent: ERPWebhookEvent): Promise<SyncResult> {
    const entity = await this.db.syncEntities.findOne({
      externalSystem: webhookEvent.system,
      externalId: webhookEvent.recordId,
    });

    if (!entity) return { type: 'ignored', reason: 'Unknown entity' };

    const erpData = await this.erpAdapter.getCustomer(webhookEvent.recordId);
    if (!erpData.success) return { type: 'failed', error: erpData.error };

    const platformConflicts: Conflict[] = [];

    for (const [field, value] of Object.entries(erpData.data)) {
      const currentVersion = entity.version[field];
      if (currentVersion && currentVersion.source === 'platform' && currentVersion.updatedAt > webhookEvent.changedAt) {
        // Platform has a newer update that hasn't been synced yet — conflict
        platformConflicts.push({
          field,
          platformValue: currentVersion.value,
          erpValue: value,
        });
      }
    }

    if (platformConflicts.length > 0) {
      const resolution = await this.conflictResolver.resolve(entity, platformConflicts);
      if (resolution === 'platform_wins') {
        // Push platform value back to ERP
        const reapply = platformConflicts.reduce((acc, c) => {
          acc[c.field] = c.platformValue;
          return acc;
        }, {} as Record<string, any>);
        await this.erpAdapter.updateCustomer(entity.externalId, reapply);
        return { type: 'resolved', resolution: 'platform_wins', conflicts: platformConflicts };
      }
      // ERP wins — update platform
      await this.updatePlatformFromERP(entity, erpData.data, platformConflicts, webhookEvent.changedAt);
      return { type: 'resolved', resolution: 'erp_wins', conflicts: platformConflicts };
    }

    // No conflicts — apply ERP changes to platform
    await this.updatePlatformFromERP(entity, erpData.data, [], webhookEvent.changedAt);
    return { type: 'synced', fieldsUpdated: Object.keys(erpData.data) };
  }

  private async updatePlatformFromERP(
    entity: SyncEntity, erpData: Record<string, any>,
    conflicts: Conflict[], changedAt: Date
  ): Promise<void> {
    const now = new Date();
    for (const [field, value] of Object.entries(erpData)) {
      if (conflicts.some(c => c.field === field)) continue;
      entity.version[field] = { value, updatedAt: changedAt || now, source: 'erp' };
    }
    entity.lastSyncedAt = now;
    await this.db.syncEntities.update(entity);
    await this.updatePlatformRecord(entity.platformId, erpData);
  }

  private detectChanges(
    entity: SyncEntity, currentData: Record<string, any>
  ): SyncChange[] {
    const changes: SyncChange[] = [];
    for (const [field, value] of Object.entries(currentData)) {
      const currentVersion = entity.version[field];
      if (!currentVersion || JSON.stringify(currentVersion.value) !== JSON.stringify(value)) {
        changes.push({
          entityType: entity.entityType,
          platformId: entity.platformId,
          externalId: entity.externalId,
          field,
          newValue: value,
          changedAt: new Date(),
          source: 'platform',
        });
      }
    }
    return changes;
  }

  private buildERPUpdate(changes: SyncChange[]): Record<string, any> {
    const fieldMapping = this.getFieldMapping();
    const update: Record<string, any> = {};
    for (const change of changes) {
      const erpField = fieldMapping[change.field];
      if (erpField) update[erpField] = change.newValue;
    }
    return update;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| P-map (MIT) | Concurrency | Batch sync operations |
| Zod (MIT) | Validation | Sync schema validation |
| Pino (MIT) | Logging | Sync audit logging |

## Production Considerations

**Scaling:** Customer sync operations must not block voice calls. All sync operations (platform-to-ERP and ERP-to-platform) are asynchronous — enqueued to a worker queue and processed with configurable concurrency. The cross-reference map is cached in Redis with 1-hour TTL. For initial bulk sync (thousands of customers), use a dedicated batch sync job with progress tracking and throttling to avoid ERP rate limits.

**Security:** Sync operations involve PII data transfer — ensure all sync channels are encrypted (TLS 1.3). Never sync sensitive payment data (card numbers, CVV) to ERP systems. Log all sync operations with the initiating actor (call SID, admin user, system). Implement field-level access control — some fields may be readable from ERP but not writable from the platform (e.g., credit rating).

**Monitoring:** Track sync volume (records synced per hour), sync latency (detection to completion), conflict rate, conflict resolution patterns, error rate by sync direction and ERP target. Alert on sync failures exceeding 5%, conflict rates above 10%, sync backlog growing (pending sync count > 1000), and cross-reference map integrity issues (orphaned platform IDs). Run daily reconciliation comparing platform and ERP customer records.
