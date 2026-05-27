# Section 08: Contact List Versioning

## Overview

Contact list versioning provides auditability and recovery capabilities for campaign contact lists. When contacts are imported, modified, or removed, the versioning system captures snapshots that enable rollback, historical comparison, and compliance audit. Versioning is particularly important for regulated industries where contact list changes must be tracked and attributable to specific users or processes.

The versioning system operates at the list level — each time a list is imported, has contacts added or removed, or is edited, a new version is created. Each version records the full contact set as a snapshot, the change type (import, manual add, dedup merge, suppression), the actor who made the change, and the timestamp. The system retains a configurable number of versions per list, with the ability to pin specific versions for compliance hold.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Agent    |--->| Snapshot |--->| Diff     |--->| Rollback |--->| Publish  |
| Editor   |    | (deep    |    | (JSON    |    | (restore |    | (draft   |
|          |    |  clone)  |    |  diff)   |    |  snap)   |    |  ->live) |
+----------+    +----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Snapshot-Based**: Deep clone of complete agent config on each publish. Includes flow, prompts, voice.
- **Diff View**: JSON diff shows added/removed/changed. Side-by-side visual diff for flow.
- **Draft/Live Separation**: Draft edits don't affect live calls. Publish promotes draft to live instantly.
## Implementation Approach

```
class ContactListVersionManager {
  constructor(storage, prisma) {
    this.storage = storage; // S3/MinIO for compressed snapshots
    this.prisma = prisma;
    this.maxVersions = 20; // Configurable per tenant
  }

  async createVersion(listId, changeType, actor, delta) {
    const list = await this.prisma.contactList.findUnique({
      where: { id: listId },
      include: { contacts: true }
    });

    const versionNumber = list.currentVersion + 1;

    // Compress and store contact snapshot
    const snapshotKey = `lists/${listId}/v${versionNumber}.json.gz`;
    const compressed = zlib.gzipSync(
      JSON.stringify(list.contacts.map(c => c.id))
    );
    await this.storage.put(snapshotKey, compressed);

    // Create version record
    const version = await this.prisma.listVersion.create({
      data: {
        list_id: listId,
        version: versionNumber,
        snapshot_key: snapshotKey,
        change_type: changeType,
        actor,
        contact_count: list.contacts.length,
        added_count: delta?.added || 0,
        removed_count: delta?.removed || 0,
        created_at: new Date()
      }
    });

    // Update list current version
    await this.prisma.contactList.update({
      where: { id: listId },
      data: { currentVersion: versionNumber }
    });

    // Enforce version retention
    await this.enforceRetention(listId);

    return version;
  }

  async rollback(listId, targetVersion, actor) {
    const current = await this.prisma.contactList.findUnique({
      where: { id: listId }
    });

    if (targetVersion >= current.currentVersion) {
      throw new Error('Target version must be less than current version');
    }

    // Load target snapshot
    const version = await this.prisma.listVersion.findFirst({
      where: { list_id: listId, version: targetVersion }
    });

    const compressed = await this.storage.get(version.snapshot_key);
    const contactIds = JSON.parse(zlib.gunzipSync(compressed).toString());

    // Replace current list contacts with snapshot contacts
    await this.prisma.$transaction(async (tx) => {
      await tx.contactListContact.deleteMany({
        where: { list_id: listId }
      });
      
      await tx.contactListContact.createMany({
        data: contactIds.map(id => ({
          list_id: listId,
          contact_id: id
        }))
      });
    });

    // Create rollback version
    await this.createVersion(listId, 'rollback', actor, {
      added: contactIds.length,
      removed: 0,
      rolledBackTo: targetVersion
    });
  }

  async enforceRetention(listId) {
    const versions = await this.prisma.listVersion.findMany({
      where: {
        list_id: listId,
        pinned: false
      },
      orderBy: { version: 'desc' },
      skip: this.maxVersions
    });

    for (const version of versions) {
      // Delete snapshot from storage
      await this.storage.delete(version.snapshot_key);
      // Delete version record
      await this.prisma.listVersion.delete({
        where: { id: version.id }
      });
    }
  }

  async getVersionDiff(listId, fromVersion, toVersion) {
    const v1 = await this.loadSnapshot(listId, fromVersion);
    const v2 = await this.loadSnapshot(listId, toVersion);

    const setV1 = new Set(v1);
    const setV2 = new Set(v2);

    return {
      added: v2.filter(id => !setV1.has(id)),
      removed: v1.filter(id => !setV2.has(id)),
      kept: v1.filter(id => setV2.has(id))
    };
  }
}
```

## Integration Points

- **Contact Import (sec-01, sec-02):** Every import creates a new version
- **Deduplication (sec-03):** Dedup merges create a version recording removed duplicates
- **Suppression (sec-06):** Suppression actions create a version recording removed contacts
- **Campaign Service (Ch 01):** Campaign references specific list versions for call records
- **Compliance Audit (Ch 07):** Compliance reports include list version history
- **UI:** Version comparison tool showing list changes between versions

## Open-Source Tools

- **diff** (MIT): JSON diff library
- **Zod** (MIT): Schema validation
- **ioredis** (MIT): Snapshot storage
## Production Considerations

- Snapshot compression typically achieves 80-90% reduction — a 100K contact list stores in ~200KB compressed
- Set per-tenant version retention limits — 20 versions is a good default; adjust based on storage budget
- Pinned versions for compliance should be flagged in the database and exempt from cleanup
- Rollback creates a new version rather than deleting intermediate versions — this preserves the full audit trail
- Version comparison UI should load only version metadata initially, then lazily load contact diffs
- Externalize snapshot storage to S3/MinIO rather than database BLOBs for cost efficiency
- Implement snapshot verification — periodic checksum validation of stored snapshots
- List version creation should be asynchronous for large lists to avoid blocking the import response
- Consider differential versioning (store only changes) for lists that change frequently with small deltas
- Expose version REST API endpoints for programmatic access by external systems and CI/CD pipelines
