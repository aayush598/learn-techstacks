# Section 08: Tenant Data Backup Isolation

## Overview

Backup and restore operations in a multi-tenant environment must preserve tenant isolation. A backup of one tenant's data must not be accessible to another tenant, and the restore process must not contaminate other tenants' data. This is both a security requirement (a tenant's call recordings and transcripts should never leak) and a compliance requirement (GDPR requires the ability to fully delete a tenant's data, which includes backup copies).

The backup strategy must account for the isolation model: shared+RLS backups contain all tenants' data and require tenant-aware extraction tools, schema-per-tenant backups can be per-schema, and database-per-tenant backups are naturally isolated at the database level. Each model requires different approaches for point-in-time recovery (PITR), selective tenant restore, and cross-region backup replication.

For a voice agent platform, backup isolation is complicated by the volume and nature of the data. Call recordings are large binary files (typically stored in S3, not PostgreSQL), while call metadata, transcripts, and configurations are in the database. Backups must span both the database and object storage, maintaining consistency between them for point-in-time recovery.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Audio    |--->| WebSocket|--->| Jitter   |--->| PLC      |--->| Player   |
| Producer |    | (WSS)    |    | Buffer   |    | (Packet  |    | (smooth  |
| (100ms   |    | (binary) |    | (adaptive|    |  Loss    |    |  output) |
|  chunks) |    |          |    |  60-200) |    |  Conceal)|    +----------+
+----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```typescript
interface BackupConfig {
  tenantId: string;
  model: 'shared' | 'schema' | 'dedicated';
  schedule: string; // cron expression
  retention: {
    daily: number;   // days
    weekly: number;  // weeks
    monthly: number; // months
  };
  encryption: {
    enabled: boolean;
    kmsKeyId?: string;
  };
  crossRegion: boolean;
}

class TenantBackupManager {
  constructor(
    private pool: Pool,
    private s3: S3Client,
    private kms: KMSClient,
    private config: BackupConfig
  ) {}

  async createTenantBackup(tenantId: string): Promise<BackupResult> {
    const startTime = Date.now();
    const backupId = `backup_${tenantId}_${Date.now()}`;

    try {
      // 1. Lock tenant data for consistency
      await this.acquireConsistencyLock(tenantId);

      // 2. Create backup manifest
      const manifest = await this.createManifest(tenantId, backupId);

      // 3. Database backup
      const dbBackupPath = await this.backupDatabase(tenantId, backupId);
      manifest.dbBackupPath = dbBackupPath;

      // 4. Object storage snapshot (recordings, transcripts)
      const storageSnapshot = await this.snapshotObjectStorage(tenantId, backupId);
      manifest.storageSnapshot = storageSnapshot;

      // 5. Generate checksums
      manifest.checksum = await this.generateChecksum(backupId);

      // 6. Encrypt backup
      const encryptedPath = await this.encryptBackup(backupId, tenantId);

      // 7. Upload manifest and backup
      await this.uploadBackup(encryptedPath, manifest);

      // 8. Replicate to secondary region
      if (this.config.crossRegion) {
        await this.replicateToRegion(encryptedPath, this.config.secondaryRegion);
      }

      // 9. Cleanup old backups per retention policy
      await this.cleanupOldBackups(tenantId);

      const duration = Date.now() - startTime;
      return { backupId, tenantId, status: 'completed', duration, size: manifest.totalSize };
    } catch (error) {
      await this.alertService.send({
        type: 'backup_failed',
        tenantId,
        error: error.message,
      });
      return { backupId, tenantId, status: 'failed', error: error.message };
    }
  }

  private async backupDatabase(tenantId: string, backupId: string): Promise<string> {
    const tenant = await this.getTenant(tenantId);
    const backupDir = `/tmp/backups/${backupId}`;
    
    switch (tenant.isolationTier) {
      case 'shared':
        return this.backupSharedTenant(tenantId, backupDir);
      case 'schema':
        return this.backupSchemaTenant(tenantId, backupDir);
      case 'dedicated':
        return this.backupDedicatedTenant(tenantId, backupDir);
    }
  }

  private async backupSharedTenant(tenantId: string, backupDir: string): Promise<string> {
    // Dump all data, then extract tenant-specific rows
    const fullDumpPath = `${backupDir}/full_dump.sql`;
    await exec(`pg_dump -Fc ${this.connectionString} -f ${fullDumpPath}`);

    // Extract tenant data using pg_restore with filter
    const tenantDumpPath = `${backupDir}/tenant_dump.sql`;
    await exec(
      `pg_restore -Fc ${fullDumpPath} -f ${tenantDumpPath} ` +
      `--schema=public --data-only --table=calls,transcripts,agents,configurations ` +
      `--where="tenant_id='${tenantId}'"`
    );

    // Also extract schema definitions (shared across tenants)
    const schemaPath = `${backupDir}/schema.sql`;
    await exec(
      `pg_dump -Fc ${this.connectionString} ` +
      `--schema-only -f ${schemaPath}`
    );

    return tenantDumpPath;
  }

  private async backupSchemaTenant(tenantId: string, backupDir: string): Promise<string> {
    const schemaName = `tenant_${tenantId.slice(0, 12)}`;
    const dumpPath = `${backupDir}/schema_dump.sql`;
    
    await exec(
      `pg_dump -Fc ${this.connectionString} ` +
      `--schema=${schemaName} -f ${dumpPath}`
    );

    return dumpPath;
  }

  private async backupDedicatedTenant(tenantId: string, backupDir: string): Promise<string> {
    const tenantConnString = await this.getTenantConnectionString(tenantId);
    const dumpPath = `${backupDir}/full_dump.sql`;
    
    await exec(`pg_dump -Fc ${tenantConnString} -f ${dumpPath}`);
    
    return dumpPath;
  }

  private async restoreTenantBackup(
    tenantId: string,
    backupId: string,
    targetTier?: string
  ): Promise<RestoreResult> {
    // Find backup
    const backup = await this.findBackup(tenantId, backupId);
    
    // Download and decrypt
    const decryptedPath = await this.downloadAndDecrypt(backup);

    // Consistent point-in-time: restore DB + storage
    await this.restoreDatabase(tenantId, decryptedPath, targetTier);
    await this.restoreObjectStorage(tenantId, backup.storageSnapshot);

    // Verify integrity
    await this.verifyRestore(tenantId, backup);

    return { tenantId, status: 'restored', backupId };
  }

  private async cleanupOldBackups(tenantId: string): Promise<void> {
    const { daily, weekly, monthly } = this.config.retention;
    
    // List all backups for tenant
    const backups = await this.listBackups(tenantId);
    
    // Group by period and apply retention
    const toDelete = this.applyRetentionPolicy(backups, { daily, weekly, monthly });
    
    for (const backup of toDelete) {
      await this.s3.deleteObject({
        Bucket: this.backupBucket,
        Key: backup.key,
      });
    }
  }
}

// GDPR deletion from backups
class GDPRBackupHandler {
  async deleteTenantFromBackups(tenantId: string): Promise<void> {
    // Identify all backups containing this tenant's data
    const backups = await this.findBackupsWithTenant(tenantId);
    
    for (const backup of backups) {
      // Download backup
      const backupFile = await this.downloadBackup(backup);
      
      // Remove tenant rows
      const cleanedFile = await this.removeTenantFromDump(backupFile, tenantId);
      
      // Re-upload cleaned backup (overwrite)
      await this.uploadBackup(backup.backupId, cleanedFile);
      
      // Log the modification
      await this.auditService.log('gdpr_backup_cleaned', {
        tenantId,
        backupId: backup.backupId,
        timestamp: new Date().toISOString(),
      });
    }
  }

  private async removeTenantFromDump(dumpPath: string, tenantId: string): Promise<string> {
    const cleanedPath = dumpPath.replace('.sql', '_cleaned.sql');
    
    // Remove rows matching tenant_id from each table
    const tables = ['calls', 'transcripts', 'agents', 'configurations'];
    for (const table of tables) {
      await exec(
        `sed -i '/INSERT INTO ${table}.*${tenantId}/d' ${dumpPath}`
      );
    }
    
    return cleanedPath;
  }
}
```

## Integration Points

- **GDPR Deletion (Ch 10):** Backup cleanup must be part of GDPR right to erasure workflow
- **Disaster Recovery:** Tenant-specific restore procedures for DR scenarios
- **SLA Monitoring (Ch 09):** Backup success/failure metrics feed into SLA compliance
- **Billing (Part 17):** Backup storage costs allocated to tenants
- **Audit Logging:** All backup and restore operations are logged immutably

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Backup Storage Cost:** Per-tenant backups increase storage costs linearly with tenant count. Implement deduplication for shared data (schema-only is shared, data is per-tenant). Compress backups with zstd.
- **Backup Verification:** Automated restore testing is more important than the backup itself. Regularly test restoring a tenant's backup to a staging environment and verify data integrity.
- **PITR for Shared Models:** Point-in-time recovery for shared+RLS requires restoring the entire database to a point in time, which affects all tenants. Coordinate PITR maintenance windows across all tenants.
- **Consistency Between DB and Storage:** Database backup and S3 snapshot must be at the same point in time. Use S3 versioning and database transaction snapshots to maintain consistency.
- **GDPR Deletion Window:** GDPR requires data deletion within 30 days of request. Backup cleanup must complete within this window. Automate deletion from all backup tiers.
- **Cross-Region Replication Cost:** Replicating backups to a secondary region doubles storage costs. Weigh against RPO requirements. Consider using cheaper storage classes (Glacier) for cross-region copies.
- **Encryption Key Management:** Per-tenant encryption keys for backups require careful management. If a tenant's key is lost, their backups are unrecoverable. Implement key escrow.
- **Retention Policy Enforcement:** Automate retention policy enforcement. A bug that stops deleting old backups can rapidly increase storage costs. Monitor backup storage growth per tenant.
