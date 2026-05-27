# Section 08: Bulk Tenant Import

## Overview

Bulk tenant import enables enterprise sales and partner operations to provision multiple tenants simultaneously. This is essential for resellers onboarding sub-tenants, enterprise customers creating department-level divisions, and migration from competitor platforms. The import process accepts structured data (CSV/JSON/API) and orchestrates tenant creation with minimal manual effort.

The bulk import pipeline consists of: file upload and parsing, validation (schema, duplicates, data quality), preview and confirmation, parallel tenant provisioning, progress monitoring, and comprehensive error reporting. Each tenant in the import is processed independently, so a single tenant failure does not block the entire import.

For a voice agent platform with a reseller model (Part 14, Ch 06), bulk import is a critical capability. A reseller may onboard 50 new sub-tenants at once after signing a partnership agreement. The import tool must handle this volume efficiently while respecting rate limits on downstream services.

## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```typescript
interface BulkImportRecord {
  companyName: string;
  adminEmail: string;
  adminName: string;
  tier: string;
  industry?: string;
  timezone?: string;
  phoneAreaCode?: string;
  customFields?: Record<string, string>;
}

class BulkImportService {
  private maxConcurrentImports = 10;

  async parseImportFile(filePath: string, format: 'csv' | 'json'): Promise<BulkImportPreview> {
    let records: BulkImportRecord[];
    
    if (format === 'csv') {
      records = await this.parseCSV(filePath);
    } else {
      records = JSON.parse(await fs.readFile(filePath, 'utf-8'));
    }

    // Validate all records
    const results = await Promise.allSettled(
      records.map((record, index) => this.validateRecord(record, index))
    );

    const valid: RecordValidation[] = [];
    const errors: RecordValidation[] = [];

    results.forEach((result, index) => {
      if (result.status === 'fulfilled') {
        valid.push({ record: records[index], index, errors: [], warnings: result.value.warnings });
      } else {
        errors.push({ record: records[index], index, errors: [result.reason], warnings: [] });
      }
    });

    return {
      totalRecords: records.length,
      validCount: valid.length,
      errorCount: errors.length,
      validRecords: valid,
      errorRecords: errors,
      estimatedDuration: this.estimateDuration(valid.length),
      warnings: this.generateWarnings(valid),
    };
  }

  async startBulkImport(
    records: BulkImportRecord[],
    options: ImportOptions
  ): Promise<BulkImportJob> {
    const jobId = crypto.randomUUID();
    
    // Create import job record
    await this.pool.query(`
      INSERT INTO bulk_imports (id, total_count, status, options, created_at)
      VALUES ($1, $2, 'processing', $3, NOW())
    `, [jobId, records.length, JSON.stringify(options)]);

    // Enqueue tenant creation jobs
    const jobs = records.map(record => ({
      name: 'bulk-create-tenant',
      data: {
        jobId,
        record,
        options,
      },
      opts: {
        attempts: 3,
        backoff: { type: 'exponential', delay: 2000 },
      },
    }));

    await this.queue.addBulk(jobs);

    return {
      jobId,
      totalRecords: records.length,
      status: 'processing',
    };
  }

  async getImportProgress(jobId: string): Promise<ImportProgress> {
    const [job, completed, failed] = await Promise.all([
      this.pool.query('SELECT * FROM bulk_imports WHERE id = $1', [jobId]),
      this.pool.query(
        `SELECT COUNT(*) FROM import_results WHERE job_id = $1 AND status = 'success'`,
        [jobId]
      ),
      this.pool.query(
        `SELECT COUNT(*) FROM import_results WHERE job_id = $1 AND status = 'failed'`,
        [jobId]
      ),
    ]);

    return {
      jobId,
      total: parseInt(job.rows[0].total_count),
      completed: parseInt(completed.rows[0].count),
      failed: parseInt(failed.rows[0].count),
      status: job.rows[0].status,
      progress: Math.round(
        (parseInt(completed.rows[0].count) + parseInt(failed.rows[0].count)) /
        parseInt(job.rows[0].total_count) * 100
      ),
    };
  }

  private async validateRecord(
    record: BulkImportRecord, 
    index: number
  ): Promise<{ warnings: string[] }> {
    const warnings: string[] = [];
    
    if (!record.companyName) throw new Error(`Row ${index + 1}: Company name is required`);
    if (!record.adminEmail) throw new Error(`Row ${index + 1}: Admin email is required`);
    if (!this.isValidEmail(record.adminEmail)) throw new Error(`Row ${index + 1}: Invalid email format`);
    
    // Check for duplicate
    const existing = await this.pool.query(
      'SELECT id FROM tenants WHERE slug = $1',
      [this.slugify(record.companyName)]
    );
    if (existing.rows.length > 0) {
      warnings.push(`Row ${index + 1}: Company "${record.companyName}" may already exist`);
    }

    // Validate tier
    const validTiers = ['starter', 'growth', 'enterprise'];
    if (!validTiers.includes(record.tier)) {
      throw new Error(`Row ${index + 1}: Invalid tier "${record.tier}". Must be one of: ${validTiers.join(', ')}`);
    }

    return { warnings };
  }

  private estimateDuration(recordCount: number): string {
    // Average 30s per tenant provisioning
    const totalSeconds = (recordCount / this.maxConcurrentImports) * 30;
    if (totalSeconds < 60) return `${Math.round(totalSeconds)} seconds`;
    if (totalSeconds < 3600) return `${Math.round(totalSeconds / 60)} minutes`;
    return `${Math.round(totalSeconds / 3600)} hours`;
  }

  async downloadImportReport(jobId: string, format: 'csv' | 'json'): Promise<string> {
    const results = await this.pool.query(
      'SELECT * FROM import_results WHERE job_id = $1 ORDER BY record_index',
      [jobId]
    );

    if (format === 'csv') {
      return this.generateCSV(results.rows);
    }
    return JSON.stringify(results.rows, null, 2);
  }
}

// Job processor for individual tenant creation
async function processBulkTenantCreation(job: Job): Promise<void> {
  const { jobId, record, options } = job.data;
  
  try {
    // Create tenant using the standard provisioning pipeline
    const tenantId = await provisioningPipeline.startProvisioning({
      companyName: record.companyName,
      adminEmail: record.adminEmail,
      adminName: record.adminName,
      tier: record.tier,
      industry: record.industry,
      timezone: record.timezone,
      source: 'bulk_import',
    });

    // Record success
    await pool.query(`
      INSERT INTO import_results (job_id, record_index, status, tenant_id, completed_at)
      VALUES ($1, $2, 'success', $3, NOW())
    `, [jobId, record.index, tenantId]);

  } catch (error) {
    // Record failure
    await pool.query(`
      INSERT INTO import_results (job_id, record_index, status, error, completed_at)
      VALUES ($1, $2, 'failed', $3, NOW())
    `, [jobId, record.index, error.message]);
  }
}
```

## Integration Points

- **Reseller Portal (Ch 06):** Bulk tenant import is a core reseller feature
- **Provisioning Pipeline (Sec 02):** Reuses standard provisioning for each tenant
- **Admin Dashboard:** Import management UI with upload, preview, and monitoring
- **Email Notifications:** Welcome emails sent to each imported tenant's admin
- **Audit Logging:** All bulk imports logged with user attribution

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **File Size Limits:** Limit import files to 10MB or 10,000 records. Beyond this, require splitting into multiple imports or use API-based batch import.
- **Rate Limit Awareness:** Bulk imports must respect downstream service rate limits (Stripe, cloud providers). Implement a rate limiter per service in the import pipeline.
- **Duplicate Detection:** Check for duplicate email addresses and company names before creating. Offer "skip duplicates" and "update existing" options.
- **Transactional Integrity:** Each tenant import is its own transaction. A failure in one does not affect others. But the import job itself should be atomic in terms of tracking.
- **User Notification:** Imported tenant admins receive the standard welcome email. Consider a custom email template for bulk imports indicating they were set up by their parent organization.
- **Import Results:** Generate a downloadable report listing success/failure for each record with detailed error messages. This is essential for the reseller to fix issues and retry.
- **Security Considerations:** Bulk import files contain sensitive data (admin emails, company names). Encrypt at rest during processing. Delete uploaded files after processing.
