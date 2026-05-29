# Section 01: Export Engine Overview

## Architecture

The export engine is responsible for transforming report definitions into downloadable files (CSV, JSON, PDF) and delivering them through various channels (email, Slack, webhooks). It operates as an asynchronous job queue with status tracking.

```
Export Engine Architecture
┌─────────────────────────────────────────────────────────────────────────┐
│ API Request (Export Now / Schedule)                                   │
│     │                                                                  │
│     ▼                                                                  │
│ Export Orchestrator                                                    │
│ ┌────────────────────────────────────────────────────────────────────┐ │
│ │ 1. Resolve report definition + filters + date range                │ │
│ │ 2. Generate export configuration (format, channel, template)       │ │
│ │ 3. Create ExportJob in queue                                       │ │
│ │ 4. Return job ID for status polling                                │ │
│ └────────┬───────────────────────────────────────────────────────────┘ │
│          │                                                              │
│          ▼                                                              │
│ Job Queue (BullMQ / Redis)                                              │
│ ┌────────────────────────────────────────────────────────────────────┐ │
│ │ Export Worker Pool (10 workers, up to 50 parallel jobs)           │ │
│ │                                                                   │ │
│ │ ┌──────────┐ ┌──────────┐ ┌──────────┐                          │ │
│ │ │ Worker 1 │ │ Worker 2 │ │ Worker N │                          │ │
│ │ │ CSV Gen  │ │ PDF Gen  │ │ JSON Gen │                          │ │
│ │ └────┬─────┘ └────┬─────┘ └────┬─────┘                          │ │
│ │      │            │            │                                 │ │
│ │      ▼            ▼            ▼                                 │ │
│ │ ┌──────────┐ ┌──────────┐ ┌──────────┐                          │ │
│ │ │ ClickHouse Qry │ Puppeteer │ │ Data    │                          │ │
│ │ │ → CSV stream    │ → PDF     │ │ → JSON  │                          │ │
│ │ └──────────┘ └──────────┘ └──────────┘                          │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│          │                                                              │
│          ▼                                                              │
│ Delivery Worker                                                         │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐                               │ │
│ │ Email    │ │ Slack    │ │ Webhook  │                               │ │
│ │ (SendGrid)│ │ (Incoming)│ │ (HTTP)  │                               │ │
│ └──────────┘ └──────────┘ └──────────┘                               │ │
│          │                                                              │
│          ▼                                                              │
│ Storage (S3 / GCS)                                                      │
│ Files: exports/{tenant}/{job-id}/{report-name}.{format}                 │
│ Retention: 30 days, configurable per tenant                             │
└─────────────────────────────────────────────────────────────────────────┘
```

## Data Model

```typescript
type ExportFormat = 'csv' | 'json' | 'pdf';
type DeliveryChannel = 'download' | 'email' | 'slack' | 'webhook';
type JobStatus = 'queued' | 'processing' | 'completed' | 'failed' | 'partial';

interface ExportJob {
  id: string;
  reportId: string;
  tenantId: string;
  
  format: ExportFormat;
  channel: DeliveryChannel;
  
  config: {
    dateRange: DateRange;
    filters: Record<string, any>;
    columns: string[]; // selected columns to include
    rowLimit: number;
    includeHeader: boolean;
    delimiter?: string; // CSV only: comma, tab, pipe
    templateId?: string; // PDF template
  };
  
  delivery: {
    email?: { to: string[]; subject: string; body: string };
    slack?: { channel: string; message: string };
    webhook?: { url: string; headers: Record<string, string> };
  };
  
  status: JobStatus;
  progress: number; // 0-100
  error?: { code: string; message: string; details?: any };
  
  result: {
    storagePath?: string;
    fileSize?: number;
    rowCount?: number;
    downloadUrl?: string;
    expiresAt: number; // signed URL expiry
  };
  
  createdAt: number;
  startedAt?: number;
  completedAt?: number;
}

interface ExportSchedule {
  id: string;
  reportId: string;
  tenantId: string;
  
  name: string;
  enabled: boolean;
  
  format: ExportFormat;
  channel: DeliveryChannel;
  
  cron: string; // cron expression
  timezone: string;
  
  config: ExportJob['config'];
  delivery: ExportJob['delivery'];
  
  lastRun: number | null;
  lastStatus: JobStatus | null;
  nextRun: number;
  runCount: number;
  
  createdBy: string;
  createdAt: number;
  updatedAt: number;
}
```

## Job Lifecycle

```
Job States
┌──────────┐    ┌──────────┐    ┌──────────┐
│ QUEUED   │───▶│PROCESSING│───▶│COMPLETED │
└──────────┘    └──────────┘    └──────────┘
                    │                │
                    ▼                ▼
               ┌──────────┐    ┌──────────┐
               │  FAILED  │    │ PARTIAL  │
               └──────────┘    └──────────┘
                    │
                    ▼
               ┌──────────┐
               │  RETRY   │──▶ QUEUED
               └──────────┘

Retry Policy:
- 1st retry: 30 seconds
- 2nd retry: 5 minutes
- 3rd retry: 30 minutes
- Max retries: 3
After max retries → FAILED
```

## Orchestrator

```typescript
class ExportOrchestrator {
  private jobQueue: Queue;
  private workerPool: WorkerPool;
  private deliveryWorker: DeliveryWorker;
  private storage: ObjectStorage;
  
  async createExportJob(
    reportId: string,
    tenantId: string,
    params: {
      format: ExportFormat;
      channel: DeliveryChannel;
      config: ExportJob['config'];
      delivery: ExportJob['delivery'];
    }
  ): Promise<{ jobId: string; statusUrl: string }> {
    const job: ExportJob = {
      id: generateId(),
      reportId,
      tenantId,
      format: params.format,
      channel: params.channel,
      config: params.config,
      delivery: params.delivery,
      status: 'queued',
      progress: 0,
      createdAt: Date.now(),
      result: { expiresAt: Date.now() + 7 * 24 * 3600 * 1000 }, // 7 days
    };
    
    await this.jobQueue.add(job.id, job, {
      priority: params.channel === 'download' ? 1 : 2, // interactive > background
      attempts: 3,
      backoff: { type: 'exponential', delay: 30000 },
    });
    
    return {
      jobId: job.id,
      statusUrl: `/api/v1/exports/${job.id}/status`,
    };
  }
  
  async processExportJob(job: ExportJob): Promise<void> {
    const startTime = Date.now();
    
    try {
      // Step 1: Fetch report definition and resolve data (10%)
      await this.updateProgress(job.id, 10);
      const reportDefinition = await this.reportStore.get(job.reportId);
      const data = await this.dataFetcher.fetch(reportDefinition, {
        dateRange: job.config.dateRange,
        filters: job.config.filters,
        columns: job.config.columns,
        rowLimit: job.config.rowLimit,
      });
      
      // Step 2: Generate file (10-80%)
      const fileResult = await this.generateFile(data, {
        format: job.format,
        columns: job.config.columns,
        delimiter: job.config.delimiter,
        templateId: job.config.templateId,
        onProgress: (pct) => this.updateProgress(job.id, 10 + pct * 0.7),
      });
      
      // Step 3: Upload to storage (80-90%)
      await this.updateProgress(job.id, 90);
      const storagePath = `exports/${job.tenantId}/${job.id}/${job.reportId}.${job.format}`;
      await this.storage.put(storagePath, fileResult.buffer, {
        contentType: fileResult.mimeType,
        metadata: { 'job-id': job.id, 'tenant-id': job.tenantId },
      });
      
      const signedUrl = await this.storage.getSignedUrl(storagePath, 7 * 24 * 3600);
      
      // Step 4: Deliver (90-100%)
      await this.updateProgress(job.id, 95);
      const deliveryResult = await this.deliveryWorker.deliver({
        channel: job.channel,
        config: job.delivery,
        attachment: {
          url: signedUrl,
          filename: `${job.reportId}.${job.format}`,
          mimeType: fileResult.mimeType,
          fileSize: fileResult.buffer.length,
        },
      });
      
      // Step 5: Mark complete
      await this.jobStore.update(job.id, {
        status: deliveryResult.success ? 'completed' : 'partial',
        progress: 100,
        completedAt: Date.now(),
        result: {
          storagePath,
          fileSize: fileResult.buffer.length,
          rowCount: data.length,
          downloadUrl: signedUrl,
          expiresAt: Date.now() + 7 * 24 * 3600 * 1000,
        },
        error: deliveryResult.success ? undefined : {
          code: 'DELIVERY_PARTIAL',
          message: 'File generated but delivery had issues',
          details: deliveryResult.errors,
        },
      });
      
      // Log metrics
      this.emitExportMetrics({
        jobId: job.id,
        format: job.format,
        channel: job.channel,
        fileSize: fileResult.buffer.length,
        rowCount: data.length,
        duration: Date.now() - startTime,
        rowsPerSecond: data.length / ((Date.now() - startTime) / 1000),
      });
      
    } catch (error) {
      await this.jobStore.update(job.id, {
        status: 'failed',
        error: { code: 'EXPORT_FAILED', message: error.message },
      });
      throw error;
    }
  }
  
  private async generateFile(
    data: any[],
    params: { format: ExportFormat; columns: string[]; delimiter?: string; templateId?: string }
  ): Promise<{ buffer: Buffer; mimeType: string }> {
    switch (params.format) {
      case 'csv':
        return { buffer: this.csvGenerator.generate(data, { columns: params.columns, delimiter: params.delimiter }), mimeType: 'text/csv' };
      case 'json':
        return { buffer: this.jsonGenerator.generate(data), mimeType: 'application/json' };
      case 'pdf':
        return { buffer: await this.pdfGenerator.generate(data, { templateId: params.templateId }), mimeType: 'application/pdf' };
      default:
        throw new Error(`Unsupported format: ${params.format}`);
    }
  }
}
```

## Scalability

- **Worker pool:** Auto-scaled based on queue depth (min 5, max 50 workers)
- **File size limits:** CSV/JSON 100MB, PDF 50MB (50K rows for PDF)
- **Concurrent jobs per tenant:** Max 5 export + 50 scheduled
- **Rate limiting:** 10 export requests/minute per user, 100/minute per tenant
- **Storage:** S3 with multipart upload for large files, 30-day auto-cleanup

## Open Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| BullMQ (MIT) | Queue | Job queue with Redis |
| Puppeteer (Apache 2.0) | PDF | Server-side PDF rendering |
| papaparse (MIT) | CSV | CSV parsing/generation |
| json2csv (MIT) | CSV | JSON to CSV conversion |
| Node.js streams | Native | Memory-efficient streaming |
| Handlebars (MIT) | Templates | PDF template rendering |
