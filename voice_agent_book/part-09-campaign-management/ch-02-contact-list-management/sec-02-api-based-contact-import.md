# Section 02: API-Based Contact Import

## Overview

API-based contact import enables programmatic integration between the campaign system and external platforms — CRMs, ERPs, databases, and custom applications. REST endpoints accept contact data in JSON format, validate and process it, and return import results. The API must support single-contact creation (low latency) and bulk import (high throughput) with consistent validation and error handling across both modes.

The API import system must handle authentication, rate limiting, request validation, idempotency for retry safety, and comprehensive error responses. For bulk operations, the API supports both synchronous imports (for small batches) and asynchronous imports with job tracking (for large batches). Webhook notifications on import completion enable external systems to react to import results programmatically.

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

```
class ApiContactImportController {
  constructor(contactService, bulkJobQueue) {
    this.contacts = contactService;
    this.bulkQueue = bulkJobQueue;
  }

  // POST /api/contacts
  async createSingle(req, res) {
    const schema = z.object({
      phoneNumber: z.string().transform(v => this.formatE164(v)),
      firstName: z.string().min(1).max(100),
      lastName: z.string().min(1).max(100).optional(),
      email: z.string().email().optional(),
      customFields: z.record(z.string(), z.any()).optional(),
      campaignId: z.string().uuid(),
      listId: z.string().uuid().optional(),
      tags: z.array(z.string()).optional()
    });

    const parsed = schema.parse(req.body);
    const contact = await this.contacts.create(req.tenantContext, parsed);
    
    return res.status(201).json({ id: contact.id, ...contact });
  }

  // POST /api/contacts/bulk
  async createBulk(req, res) {
    const bulkSchema = z.object({
      contacts: z.array(contactItemSchema).max(50000),
      campaignId: z.string().uuid(),
      options: z.object({
        deduplicate: z.boolean().default(true),
        returnErrors: z.boolean().default(true),
        idempotencyKey: z.string().optional()
      }).optional()
    });

    const parsed = bulkSchema.parse(req.body);
    
    const job = await this.bulkQueue.add('import_contacts', {
      tenantId: req.tenantContext.tenantId,
      contacts: parsed.contacts,
      campaignId: parsed.campaignId,
      options: parsed.options
    }, {
      deduplication: {
        id: parsed.options?.idempotencyKey
      }
    });

    return res.status(202).json({
      jobId: job.id,
      status: 'processing',
      estimatedCount: parsed.contacts.length
    });
  }

  // GET /api/contacts/imports/:jobId
  async getImportStatus(req, res) {
    const job = await this.bulkQueue.getJob(req.params.jobId);
    
    return res.json({
      jobId: job.id,
      status: await job.getState(),
      progress: job.progress(),
      result: job.returnvalue
    });
  }
}
```

## Integration Points

- **API Gateway:** Authentication, rate limiting, request routing for import endpoints
- **Contact Service:** Core contact creation logic shared with CSV import pipeline
- **DNC Service (Ch 07):** Real-time DNC validation during import
- **Webhook System (Part 10, Ch 08):** Import completion notifications
- **Campaign Service (Ch 01):** Association of imported contacts with campaigns
- **Audit Log:** Import activity logging for compliance
- **Analytics (Ch 09):** Import volume and error rate tracking

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Implement rate limiting per API key — 100 req/s for single imports, 10 req/min for bulk imports
- Set maximum batch size (50,000 contacts) to prevent request timeout and memory issues
- API responses must include clear error codes and messages for programmatic error handling
- Use request compression (gzip) for bulk imports to reduce bandwidth
- Implement request size limits at the API gateway level (e.g., 10MB max per request)
- Idempotency keys should expire after 24 hours to prevent key storage bloat
- Provide a dedicated import status endpoint so clients can poll async job progress
- Support field name aliases (e.g., "phone", "phone_number", "phoneNumber") for client convenience
- Webhook payload for completed imports should include success and error counts
- Document API endpoints with OpenAPI/Swagger and provide client SDK examples
