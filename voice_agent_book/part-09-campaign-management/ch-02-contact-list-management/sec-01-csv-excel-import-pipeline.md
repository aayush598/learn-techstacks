# Section 01: CSV & Excel Import Pipeline

## Overview

The CSV and Excel import pipeline is the primary mechanism for getting contact lists into the campaign system. Business users upload spreadsheets containing contact data (names, phone numbers, custom fields), and the pipeline parses, validates, transforms, and imports the data into the campaign contact list. The pipeline must handle files ranging from a few dozen rows to millions of rows, detect column headers automatically, validate phone number formats globally, and provide real-time progress feedback to users.

A production-grade import pipeline consists of file upload, header detection, column mapping, row parsing, validation with error aggregation, deduplication, and bulk insert into the contact database. Each step must handle partial failures — a file with 10,000 rows may have 200 invalid rows that need individual error reporting while the remaining 9,800 import successfully. The user should see per-row error details without having to open the original file.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Raw Audio|--->| Codec    |--->| Resample |--->| Buffer   |--->| Formatted|
| Opus/PCM |    | Decode   |    | 48->16kHz|    | (ring    |    | 16kHz    |
| 48kHz    |    | (Opus)   |    | (Kaiser) |    |  buf)    |    | mono PCM |
+----------+    +----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```
class ContactImportPipeline {
  constructor(storage, contactService, dncService) {
    this.storage = storage; // File storage
    this.contacts = contactService;
    this.dnc = dncService;
  }

  async processImport(uploadId, campaignId, options) {
    const file = await this.storage.get(uploadId);
    const parser = this.getParser(file.extension);
    
    const stream = parser.createReadStream(file.path);
    const headerRow = await stream.readHeaders();
    const mapping = this.mapColumns(headerRow, options.columnOverrides);
    
    let batch = [];
    let errors = [];
    let processed = 0;

    for await (const row of stream) {
      processed++;
      const validation = this.validateRow(row, mapping);
      
      if (!validation.valid) {
        errors.push({ row: processed, errors: validation.errors });
        continue;
      }

      const contact = this.transformRow(row, mapping);
      
      if (await this.dnc.isListed(contact.phone)) {
        errors.push({ row: processed, errors: ['Phone on DNC list'] });
        continue;
      }

      batch.push(contact);

      if (batch.length >= 10000) {
        await this.contacts.bulkCreate(campaignId, batch);
        batch = [];
        await this.emitProgress(uploadId, { processed, errors: errors.length });
      }
    }

    // Final batch
    if (batch.length > 0) {
      await this.contacts.bulkCreate(campaignId, batch);
    }

    return this.generateSummary(processed, errors);
  }

  validateRow(row, mapping) {
    const errors = [];
    for (const [field, config] of Object.entries(mapping)) {
      if (config.required && !row[field]) {
        errors.push(`Missing required field: ${config.name}`);
      }
      if (field === 'phone' && row[field]) {
        const formatted = this.formatE164(row[field]);
        if (!formatted) errors.push('Invalid phone number format');
      }
    }
    return { valid: errors.length === 0, errors };
  }

  formatE164(phone) {
    // Strip non-digits, validate length, prepend country code
    const cleaned = phone.replace(/\D/g, '');
    if (cleaned.length < 10 || cleaned.length > 15) return null;
    return cleaned.length === 10 ? `+1${cleaned}` : `+${cleaned}`;
  }
}
```

## Integration Points

- **File Storage (MinIO/S3):** Stores uploaded CSV/Excel files for import processing
- **Contact Service (Ch 02):** Handles bulk contact creation in the database
- **DNC Service (Ch 07):** Pre-checks imported contacts against DNC lists
- **Campaign Service (Ch 01):** Associates imported contacts with specific campaigns
- **Notification Service:** Sends import completion notifications via webhook or email
- **Analytics (Ch 09):** Tracks import volume, error rates, and import velocity

## Open-Source Tools

- **SoX** (GPL 2.0): Audio processing
- **node-opus** (MIT): Opus codec
- **lame** (LGPL): MP3 encoding
## Production Considerations

- Set maximum file size limits per tenant (e.g., 100MB) to prevent memory exhaustion
- Implement file type validation using magic bytes, not just extension checking
- Phone number validation should support international formats with country code detection
- Import progress must be persisted so it survives server restarts
- Large imports (>1M rows) should run as background jobs with email notification on completion
- Row-level error reporting should include enough context for users to fix their source data
- Consider implementing a preview step that shows first 20 rows before full import begins
- Rate-limit concurrent imports per tenant to prevent database contention
- Store the original file and import metadata for audit purposes and potential re-import
- Compression (gzip) can significantly reduce upload time for CSV files
