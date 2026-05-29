# Section 06: Webhook Report Delivery

## Overview

Webhook delivery enables programmatic consumption of report exports by sending data to a user-specified HTTP endpoint. This is used for integrating with external systems (CRM, data warehouses, custom dashboards) and building automated workflows (Zapier, Make, n8n).

```
Webhook Delivery Flow
┌─────────────────────────────────────────────────────────────────────────┐
│ Schedule Trigger          Generate Export        POST to Webhook       │
│ ┌─────────────────────┐  ┌──────────────────┐  ┌────────────────────┐ │
│ │ BullMQ cron fires   │  │ Export Worker     │  │ HTTP POST          │ │
│ │ WebhookSchedule     │─▶│ → CSV/JSON/PDF   │─▶│ → URL from config  │ │
│ │                     │  │ → Upload to S3    │  │ → Include payload  │ │
│ └─────────────────────┘  │ → Get signed URL  │  │ → Handle response  │ │
│                          └──────────────────┘  └────────────────────┘ │
│ Schedule Store (DB)        File Store (S3)       Delivery Log (DB)    │
│ ┌─────────────────────┐  ┌──────────────────┐  ┌────────────────────┐ │
│ │ schedule_id         │  │ export-url       │  │ webhook_id         │ │
│ │ url, method, headers│  │ (signed, 7d)     │  │ status: 200        │ │
│ │ retry, secret       │  └──────────────────┘  │ response: OK       │ │
│ └─────────────────────┘                        └────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Webhook Configuration

```typescript
interface WebhookReportConfig {
  name: string;
  url: string; // HTTPS endpoint
  method: 'POST' | 'PUT';
  headers: Record<string, string>; // custom headers
  
  authentication: {
    type: 'none' | 'bearer' | 'basic' | 'custom-header';
    token?: string;
    username?: string;
    password?: string;
    headerName?: string;
    headerValue?: string;
  };
  
  payloadFormat: 'full' | 'url_only' | 'custom';
  customPayloadTemplate?: string; // Handlebars template for custom JSON body
  
  attachmentFormat: 'csv' | 'json' | 'pdf';
  
  retry: {
    maxAttempts: number; // default: 3
    backoffMinutes: number[]; // custom backoff intervals
    retryOnTimeout: boolean;
    retryOnServerError: boolean;
    retryOnClientError: boolean;
  };
  
  filters: {
    dateRange: DateRange;
    additionalFilters: Record<string, any>;
  };
  
  schedule: {
    frequency: 'daily' | 'weekly' | 'monthly' | 'hourly' | 'custom';
    cron: string;
    timezone: string;
    timeOfDay: string;
  };
  
  validation: {
    expectedStatusCode: number; // default: 200
    requireSuccessResponse: boolean;
    successResponsePattern?: string; // regex for response body
    timeout: number; // ms, default: 30000
    maxPayloadSize: number; // bytes, default: 25MB
  };
}

interface WebhookDelivery {
  id: string;
  scheduleId: string;
  
  url: string;
  method: string;
  requestHeaders: Record<string, string>;
  requestBody?: string; // truncated in DB
  requestSize: number;
  
  attemptNumber: number;
  maxAttempts: number;
  
  statusCode: number | null;
  responseHeaders: Record<string, string> | null;
  responseBody: string | null; // truncated
  responseSize: number;
  responseTime: number; // ms
  
  error: {
    code: string; // 'TIMEOUT' | 'NETWORK' | 'DNS' | 'SSL' | 'HTTP_ERROR' | 'INVALID_RESPONSE'
    message: string;
  } | null;
  
  success: boolean;
  createdAt: number;
  completedAt: number;
}
```

## Webhook Delivery Implementation

```typescript
class WebhookReportDeliverer {
  private deliverers: Map<string, Deliverer>;
  
  async deliver(
    schedule: ExportSchedule,
    exportJob: ExportJob
  ): Promise<WebhookDelivery> {
    const config: WebhookReportConfig = schedule.config.webhookConfig!;
    const startTime = Date.now();
    
    let lastError: Error | null = null;
    
    for (let attempt = 1; attempt <= config.retry.maxAttempts; attempt++) {
      try {
        const delivery = await this.attemptDelivery(schedule, exportJob, config, attempt);
        
        // Check if response meets validation criteria
        if (this.validateResponse(delivery, config)) {
          return delivery;
        }
        
        // Response didn't match validation criteria
        lastError = new Error(`Invalid response: status ${delivery.statusCode}, body: ${delivery.responseBody?.slice(0, 100)}`);
        
        if (attempt < config.retry.maxAttempts) {
          await this.delay(config.retry.backoffMinutes[attempt - 1] * 60 * 1000);
        }
      } catch (error) {
        lastError = error;
        
        const shouldRetry = this.shouldRetry(error, config, attempt);
        if (!shouldRetry) break;
        
        if (attempt < config.retry.maxAttempts) {
          await this.delay(config.retry.backoffMinutes[attempt - 1] * 60 * 1000);
        }
      }
    }
    
    return {
      id: generateId(),
      scheduleId: schedule.id,
      url: config.url,
      method: config.method,
      requestHeaders: {},
      requestSize: 0,
      attemptNumber: config.retry.maxAttempts,
      maxAttempts: config.retry.maxAttempts,
      statusCode: null,
      responseHeaders: null,
      responseBody: null,
      responseSize: 0,
      responseTime: Date.now() - startTime,
      error: {
        code: 'MAX_RETRIES_EXCEEDED',
        message: lastError?.message || 'All delivery attempts failed',
      },
      success: false,
      createdAt: startTime,
      completedAt: Date.now(),
    };
  }
  
  private async attemptDelivery(
    schedule: ExportSchedule,
    exportJob: ExportJob,
    config: WebhookReportConfig,
    attemptNumber: number
  ): Promise<WebhookDelivery> {
    const url = new URL(config.url);
    if (url.protocol !== 'https:') {
      throw new Error('Webhook URL must use HTTPS');
    }
    
    // Build payload
    let body: string;
    let contentType: string;
    
    switch (config.payloadFormat) {
      case 'url_only':
        body = JSON.stringify({ downloadUrl: exportJob.result.downloadUrl });
        contentType = 'application/json';
        break;
      case 'custom':
        if (config.customPayloadTemplate) {
          const template = Handlebars.compile(config.customPayloadTemplate);
          body = template({
            reportName: schedule.name,
            dateRange: schedule.config.dateRange,
            downloadUrl: exportJob.result.downloadUrl,
            fileSize: exportJob.result.fileSize,
            rowCount: exportJob.result.rowCount,
            format: schedule.format,
            generatedAt: new Date().toISOString(),
          });
        } else {
          body = JSON.stringify({ downloadUrl: exportJob.result.downloadUrl });
          contentType = 'application/json';
        }
        // If template output is JSON or not
        contentType = this.detectContentType(body) || 'application/json';
        break;
      case 'full':
      default:
        // Fetch the file content from S3 and send inline
        const fileContent = await this.storage.get(exportJob.result.storagePath!);
        body = fileContent.toString();
        contentType = this.getContentType(schedule.format);
        break;
    }
    
    // Build headers
    const headers: Record<string, string> = {
      'Content-Type': contentType,
      'User-Agent': 'VoiceAI-Export/1.0',
      'X-Export-Job-Id': exportJob.id,
      'X-Export-Schedule-Id': schedule.id,
      'X-Export-Attempt': String(attemptNumber),
      ...config.headers,
    };
    
    // Add auth headers
    this.applyAuth(headers, config.authentication);
    
    // Add signature for verification
    const signature = this.signPayload(body, schedule.tenantId);
    headers['X-Export-Signature'] = signature;
    
    // Make request
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), config.validation.timeout);
    
    try {
      const response = await fetch(config.url, {
        method: config.method,
        headers,
        body: body.length > 1024 * 1024 ? undefined : body, // only inline for <1MB
        signal: controller.signal,
      });
      
      const responseBody = await response.text();
      const responseTime = Date.now() - startTime;
      
      return {
        id: generateId(),
        scheduleId: schedule.id,
        url: config.url,
        method: config.method,
        requestHeaders: headers,
        requestSize: body.length,
        attemptNumber,
        maxAttempts: config.retry.maxAttempts,
        statusCode: response.status,
        responseHeaders: Object.fromEntries(response.headers.entries()),
        responseBody: responseBody.slice(0, 1000), // truncate
        responseSize: responseBody.length,
        responseTime,
        error: null,
        success: response.status >= 200 && response.status < 300,
        createdAt: startTime,
        completedAt: Date.now(),
      };
    } finally {
      clearTimeout(timeout);
    }
  }
  
  private validateResponse(
    delivery: WebhookDelivery,
    config: WebhookReportConfig
  ): boolean {
    if (delivery.statusCode !== config.validation.expectedStatusCode) {
      return false;
    }
    
    if (config.validation.requireSuccessResponse) {
      if (!delivery.responseBody) return false;
      
      if (config.validation.successResponsePattern) {
        const regex = new RegExp(config.validation.successResponsePattern);
        if (!regex.test(delivery.responseBody)) return false;
      }
    }
    
    return true;
  }
  
  private shouldRetry(
    error: Error,
    config: WebhookReportConfig,
    attempt: number
  ): boolean {
    if (error.name === 'AbortError') return config.retry.retryOnTimeout;
    if (error.message.includes('ECONNREFUSED') || error.message.includes('ENOTFOUND') || error.message.includes('ETIMEDOUT')) {
      return config.retry.retryOnServerError;
    }
    if (error.message.includes('4')) return config.retry.retryOnClientError;
    
    return attempt < config.retry.maxAttempts;
  }
  
  private signPayload(payload: string, tenantId: string): string {
    const secret = this.tenantSecrets.get(tenantId);
    return crypto
      .createHmac('sha256', secret)
      .update(payload)
      .digest('hex');
  }
  
  private applyAuth(headers: Record<string, string>, auth: WebhookReportConfig['authentication']): void {
    switch (auth.type) {
      case 'bearer':
        headers['Authorization'] = `Bearer ${auth.token}`;
        break;
      case 'basic':
        headers['Authorization'] = `Basic ${Buffer.from(`${auth.username}:${auth.password}`).toString('base64')}`;
        break;
      case 'custom-header':
        headers[auth.headerName!] = auth.headerValue!;
        break;
    }
  }
}
```

## Webhook Security

- **HTTPS required:** Non-HTTPS URLs are rejected
- **Payload signing:** HMAC-SHA256 signature in `X-Export-Signature` header for receiver verification
- **Secret rotation:** Webhook secrets can be rotated without changing the URL (versioned secrets, `X-Export-Secret-Version` header)
- **IP allowlisting:** Optional — exports originate from a fixed set of IPs
- **Rate limiting:** Max 1 delivery per 5 seconds per webhook URL

## Delivery Monitoring

```
Webhook Deliveries Dashboard
┌─────────────────────────────────────────────────────────────────────────┐
│ Webhook: https://api.acme.com/webhooks/reports                         │
│                                                                         │
│ Last 24 Hours                                                           │
│ ┌───────────────┬──────────┬───────────┬──────────┬────────────────┐  │
│ │ Time          │ Status   │ Latency   │ Attempts │ Response       │  │
│ ├───────────────┼──────────┼───────────┼──────────┼────────────────┤  │
│ │ 14:32:01      │ ✅ 200   │ 1,243ms  │ 1        │ {"status":"ok"}│  │
│ │ 14:22:00      │ ✅ 200   │ 987ms    │ 1        │ {"status":"ok"}│  │
│ │ 14:12:02      │ ❌ 500   │ 30,012ms │ 3 (max)  │ Server error   │  │
│ │ 14:02:01      │ ✅ 200   │ 1,101ms  │ 1        │ {"status":"ok"}│  │
│ └───────────────┴──────────┴───────────┴──────────┴────────────────┘  │
│                                                                         │
│ Success Rate: 98.4%    Avg Latency: 1.2s    P95 Latency: 3.1s        │
└─────────────────────────────────────────────────────────────────────────┘
```

## Open Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| undici (MIT) | HTTP | Node.js HTTP client |
| node-fetch (MIT) | HTTP | HTTP client (alternative) |
| p-retry (MIT) | Retry | Retry with backoff |
| Handlebars (MIT) | Template | Custom payload templates |
| Zod (MIT) | Validation | Webhook response validation |

## Production Considerations

**Payload size:** For full payload delivery (inline file content), limit to 10MB. Larger files should use `url_only` mode where the webhook receives a signed download URL. The webhook receiver can then download the file directly from S3 within the URL's expiry window (7 days).

**Webhook reliability:** Implement idempotency via `X-Export-Job-Id` header — receivers should deduplicate by this ID. The system expects a 2xx response for success; any other status triggers retry. Dead webhooks (5 consecutive failures) are automatically disabled and the creator is notified.
