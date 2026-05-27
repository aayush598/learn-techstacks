# Section 06: Contact Synchronization Engine

## Overview

The contact synchronization engine manages bidirectional data flow between the voice platform and CRM systems, ensuring contact information remains consistent across systems. The engine handles initial bulk sync (importing existing contacts from CRM to the voice platform), incremental sync (propagating changes bidirectionally as they occur), conflict resolution (handling simultaneous updates to the same contact in both systems), field mapping (transforming between data models), and health monitoring (detecting sync failures and data drift).

Synchronization is a complex distributed data problem. Contacts can be created or updated in either system at any time. The engine must detect changes, determine the direction of propagation, handle the same record being changed in both systems simultaneously, and recover from failures without data loss. The engine uses a combination of timestamp-based change tracking (comparing last-modified timestamps), cursor-based pagination (for initial bulk reads), and webhook/change data capture (for real-time change notification). The engine supports configurable sync direction per field — some fields are CRM-primary (CRM changes overwrite platform), some are platform-primary (voice platform changes overwrite CRM), and some are "last-writer-wins" (most recent change wins regardless of system).

## Architecture

```
                    Contact Synchronization Engine

   +------------------+         +------------------+
   | Voice Platform   | <-----> | Sync Engine      | <-----> | CRM (SF, HubSpot, etc.)
   | Contact Store    |         |                  |
   +------------------+         | +--------------+ |         +------------------+
                                | | Change       | |         
                                | | Detection    | |         
                                | +--------------+ |         
                                | +--------------+ |         
                                | | Conflict     | |         
                                | | Resolution   | |         
                                | +--------------+ |         
                                | +--------------+ |         
                                | | Field Mapping| |         
                                | +--------------+ |         
                                +------------------+         
```

## Design Decisions

- **Timestamp-based change tracking with cursor pagination over version vectors:** Each sync run records the last successful sync timestamp. The next run queries both systems for records modified since that timestamp, using cursor-based pagination for efficient iteration. This is simpler than version vectors (which require maintaining per-record version numbers in both systems). Trade-off: timestamp-based sync can miss changes that occur during the sync window (a record modified after the query starts but before it completes) — mitigated by overlapping sync windows and periodic full re-scans.

- **Configurable field-level sync direction over full record direction:** Each mapped field has a sync direction configuration: CRM→Platform, Platform→CRM, Bidirectional (last-writer-wins), or Read-only. A contact's CRM ID is CRM-primary, while the conversation opt-out flag is platform-primary. This enables fine-grained control over data ownership. Trade-off: field-level direction configuration is complex to set up and maintain, especially for custom fields.

- **Change queue with ordered processing over immediate sync:** Changes are queued (BullMQ) and processed in order by contact ID. This ensures that updates to the same contact are processed sequentially, preventing race conditions. The queue supports retry with backoff for transient failures and dead-lettering for persistent failures requiring manual intervention. Trade-off: queued processing introduces latency (seconds to minutes) between change and sync, which may be unacceptable for real-time use cases.

## Implementation Approach

```
interface SyncConfig {
  direction: 'bidirectional' | 'crm_to_platform' | 'platform_to_crm';
  fieldMappings: {
    platformField: string;
    crmField: string;
    direction: 'crm_primary' | 'platform_primary' | 'last_writer_wins';
    transform?: (value: any) => any;
  }[];
  conflictResolution: 'last_writer_wins' | 'crm_wins' | 'platform_wins' | 'manual';
  schedule: { frequency: 'realtime' | 'every_n_minutes' | 'daily'; interval?: number };
}

class ContactSyncEngine {
  async runSync(integrationId: string, tenantId: string): Promise<SyncResult> {
    const config = await this.getSyncConfig(integrationId, tenantId);
    const lastSync = await this.getLastSyncTimestamp(integrationId, tenantId);
    const now = Date.now();

    const [platformChanges, crmChanges] = await Promise.all([
      this.getPlatformChanges(tenantId, lastSync, now),
      this.getCRMChanges(integrationId, tenantId, lastSync, now)
    ]);

    const resolved = this.resolveConflicts(platformChanges, crmChanges, config);
    const applied = await this.applyChanges(resolved, config);

    await this.recordSyncResult(integrationId, tenantId, {
      lastSyncTimestamp: now,
      platformChangesFound: platformChanges.length,
      crmChangesFound: crmChanges.length,
      conflictsResolved: resolved.conflicts,
      recordsUpdated: applied
    });

    return applied;
  }

  private resolveConflicts(
    platformChanges: Change[],
    crmChanges: Change[],
    config: SyncConfig
  ): ResolvedChanges {
    const changes: Change[] = [];
    const conflicts: Conflict[] = [];

    for (const crmChange of crmChanges) {
      const platformChange = platformChanges.find(p => p.externalId === crmChange.externalId);
      if (!platformChange) {
        changes.push({ ...crmChange, direction: this.getDirection(config.direction) });
        continue;
      }

      // Both systems changed - need conflict resolution
      const resolved = this.resolveFieldConflicts(crmChange, platformChange, config);
      conflicts.push(resolved);
      changes.push(resolved.resolvedChange);
    }

    for (const platformChange of platformChanges) {
      if (!crmChanges.find(c => c.externalId === platformChange.externalId)) {
        changes.push({ ...platformChange, direction: 'platform_to_crm' });
      }
    }

    return { changes, conflicts: conflicts.length };
  }

  private resolveFieldConflicts(
    crmChange: Change, platformChange: Change, config: SyncConfig
  ): ConflictResolution {
    const resolvedFields = {};
    for (const field of config.fieldMappings) {
      const crmVal = crmChange.fields[field.crmField];
      const platVal = platformChange.fields[field.platformField];
      if (field.direction === 'crm_primary') resolvedFields[field.platformField] = crmVal;
      else if (field.direction === 'platform_primary') resolvedFields[field.platformField] = platVal;
      else resolvedFields[field.platformField] = crmChange.timestamp > platformChange.timestamp ? crmVal : platVal;
    }
    return {
      resolvedChange: { externalId: crmChange.externalId, fields: resolvedFields, direction: 'bidirectional' },
      fieldConflicts: config.fieldMappings.filter(f => crmChange.fields[f.crmField] !== platformChange.fields[f.platformField])
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **BullMQ** (MIT) | Queue | Change queue processing |
| **Redis** (BSD) | Data store | Sync state and timestamps |
| **PostgreSQL** (PostgreSQL) | Data store | Contact storage |
| **ClickHouse** (Apache 2.0) | Analytics | Sync metrics and audit log |

## Production Considerations

**Scaling:** Full initial sync for a large CRM database (500K+ contacts) can take hours. Use incremental sync (sync only recent changes) for ongoing operations with a weekly full re-sync to catch missed changes. Sync jobs should be distributed across worker instances. Monitor sync queue depth and worker throughput.

**Security:** Sync data contains PII that must be handled according to data protection regulations. Encrypt data in transit during sync operations. Log sync operations for audit but exclude PII from logs. Implement data retention and purging that respects both platform and CRM data policies.

**Monitoring:** Track sync success rate, records synced per run, conflict rate (should be low, < 1%), sync duration, queue depth, and data drift (difference between platform and CRM data for sampled records). Alert on sync failures, high conflict rates (> 5%), and excessive sync duration (> 2x baseline).
