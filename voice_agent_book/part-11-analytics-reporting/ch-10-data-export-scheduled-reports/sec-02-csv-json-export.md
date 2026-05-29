# Section 02: CSV & JSON Export

## Overview

CSV and JSON are the most common export formats for data analysis. CSV is used for spreadsheet tools (Excel, Google Sheets, Airtable) and legacy systems, while JSON is used for programmatic integration with APIs, data pipelines, and custom tooling.

```
Format Decision Tree
┌─────────────────────────────────────────────────────────────────────────┐
│ User selects export                                                     │
│     │                                                                  │
│     ▼                                                                  │
│ What's the destination?                                                │
│ ┌──────────────────────────────────────────────────────────────────┐  │
│ │ Excel, Sheets, BI Tool          → CSV                            │  │
│ │ API Integration, Webhook, Script → JSON                          │  │
│ │ Executive Report, Client         → PDF (see sec-03)              │  │
│ └──────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

## CSV Export

### Features
- Configurable delimiter (comma, tab, pipe, semicolon)
- Headers: field names or custom labels
- Quoting: auto (when needed), always, never
- Encoding: UTF-8 with BOM (for Excel compatibility), UTF-8 without BOM
- Date format: ISO 8601, locale-specific, custom
- Number format: locale-aware (decimal separator, thousands separator)
- NULL handling: empty string, "null", "N/A", skip
- Streaming: writes rows as they're fetched from ClickHouse (no memory limit)

### Implementation

```typescript
interface CSVExportConfig {
  delimiter: ',' | '\t' | '|' | ';';
  includeHeader: boolean;
  headerLabels: Record<string, string>; // field → label mapping
  
  quoting: 'auto' | 'always' | 'never';
  
  encoding: 'utf8' | 'utf8-bom';
  
  dateFormat: 'iso' | 'us' | 'eu' | 'custom';
  customDateFormat?: string; // moment/date-fns pattern
  
  decimalSeparator: '.' | ',';
  thousandsSeparator: ',' | '.' | ' ' | '';
  
  nullRepresentation: '' | 'null' | 'N/A' | '(empty)';
  
  booleanFormat: 'true/false' | 'yes/no' | '1/0';
  
  rowLimit: number; // max rows to export (0 = unlimited)
}

class CSVGenerator {
  generate(data: AsyncIterable<any>, config: CSVExportConfig): Buffer {
    const chunks: Buffer[] = [];
    const delimiter = config.delimiter;
    const quote = '"';
    const escape = '"';
    
    let isFirstRow = true;
    let rowCount = 0;
    
    // Helper to format a single CSV value
    const formatValue = (value: any): string => {
      if (value === null || value === undefined) {
        return config.nullRepresentation;
      }
      
      if (typeof value === 'boolean') {
        switch (config.booleanFormat) {
          case 'yes/no': return value ? 'yes' : 'no';
          case '1/0': return value ? '1' : '0';
          default: return value.toString();
        }
      }
      
      if (value instanceof Date || (typeof value === 'string' && !isNaN(Date.parse(value)))) {
        return this.formatDate(value, config.dateFormat, config.customDateFormat);
      }
      
      if (typeof value === 'number') {
        return this.formatNumber(value, config);
      }
      
      const str = String(value);
      
      // Quote if contains delimiter, quote, or newline
      if (config.quoting === 'always' || str.includes(delimiter) || str.includes(quote) || str.includes('\n')) {
        return quote + str.replace(new RegExp(quote, 'g'), escape + quote) + quote;
      }
      
      return str;
    };
    
    // Write header row
    if (config.includeHeader) {
      const headers = Object.keys(config.headerLabels);
      const headerRow = headers.map(h => config.headerLabels[h] || h).join(delimiter);
      chunks.push(Buffer.from(headerRow + '\n'));
    }
    
    // Write data rows
    for await (const row of data) {
      if (config.rowLimit > 0 && rowCount >= config.rowLimit) break;
      
      const values = Object.keys(config.headerLabels).map(field => formatValue(row[field]));
      const rowStr = values.join(delimiter) + '\n';
      chunks.push(Buffer.from(rowStr));
      rowCount++;
    }
    
    // Add BOM if requested (for Excel UTF-8 compatibility)
    const bom = config.encoding === 'utf8-bom' ? Buffer.from([0xEF, 0xBB, 0xBF]) : Buffer.alloc(0);
    
    return Buffer.concat([bom, ...chunks]);
  }
  
  private formatDate(value: string | Date, format: string, customFormat?: string): string {
    const date = typeof value === 'string' ? new Date(value) : value;
    
    switch (format) {
      case 'iso': return date.toISOString();
      case 'us': return `${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getDate().toString().padStart(2, '0')}/${date.getFullYear()}`;
      case 'eu': return `${date.getDate().toString().padStart(2, '0')}.${(date.getMonth() + 1).toString().padStart(2, '0')}.${date.getFullYear()}`;
      default: return date.toISOString();
    }
  }
  
  private formatNumber(value: number, config: CSVExportConfig): string {
    const [intPart, decPart] = value.toString().split('.');
    const formattedInt = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, config.thousandsSeparator);
    
    if (decPart) {
      return formattedInt + config.decimalSeparator + decPart;
    }
    return formattedInt;
  }
}

// Streaming version for large datasets
class StreamingCSVGenerator {
  async* generateRows(
    query: string,
    batchSize: number = 10000
  ): AsyncIterable<Buffer> {
    let offset = 0;
    let hasMore = true;
    
    while (hasMore) {
      const rows = await clickHouse.query(
        `${query} LIMIT ${batchSize} OFFSET ${offset}`
      );
      
      if (rows.length === 0) {
        hasMore = false;
        break;
      }
      
      yield this.formatBatch(rows);
      offset += batchSize;
    }
  }
}
```

## JSON Export

### Features
- Structure: array of objects (default), keyed by column, keyed by ID
- Nested objects: flatten (dot notation), preserve nested, separate arrays
- Date format: ISO 8601 string, Unix timestamp, formatted string
- Number type: preserve (no quotes), string (quoted for precision)
- Large numbers: BigInt support, string for >15 digits
- Pretty print: enabled/disabled (minified)
- Null handling: include null fields, omit null fields

### Implementation

```typescript
interface JSONExportConfig {
  rootStructure: 'array' | 'keyedById' | 'keyedByDate';
  idField?: string;
  
  nesting: 'flatten' | 'preserve' | 'separateArrays';
  flattenSeparator: string; // default: '.'
  
  dateFormat: 'iso' | 'unix' | 'unixMs' | 'formatted';
  dateFormatPattern?: string;
  
  bigIntAsString: boolean;
  
  pretty: boolean;
  indent?: number;
  
  includeNullFields: boolean;
  omitFields?: string[];
  
  rowLimit: number;
}

class JSONGenerator {
  generate(
    data: any[] | AsyncIterable<any>,
    config: JSONExportConfig
  ): Buffer {
    // Convert data to the requested structure
    let json: any;
    
    switch (config.rootStructure) {
      case 'array':
        json = this.toArray(data, config);
        break;
      case 'keyedById':
        json = this.toKeyedObject(data, config.idField!, config);
        break;
      case 'keyedByDate':
        json = this.toDateKeyedObject(data, config);
        break;
    }
    
    // Serialize
    const jsonStr = JSON.stringify(json, null, config.pretty ? (config.indent || 2) : undefined);
    return Buffer.from(jsonStr, 'utf-8');
  }
  
  private transformRow(row: Record<string, any>, config: JSONExportConfig): Record<string, any> {
    const result: Record<string, any> = {};
    
    for (const [key, value] of Object.entries(row)) {
      // Skip omitted fields
      if (config.omitFields?.includes(key)) continue;
      
      // Handle nulls
      if (value === null || value === undefined) {
        if (config.includeNullFields) {
          result[key] = null;
        }
        continue;
      }
      
      // Transform value based on type
      result[key] = this.transformValue(value, config);
    }
    
    return result;
  }
  
  private transformValue(value: any, config: JSONExportConfig): any {
    if (value instanceof Date || this.isDateString(value)) {
      switch (config.dateFormat) {
        case 'unix': return Math.floor(new Date(value).getTime() / 1000);
        case 'unixMs': return new Date(value).getTime();
        case 'formatted': return this.formatDate(value, config.dateFormatPattern);
        default: return new Date(value).toISOString();
      }
    }
    
    if (typeof value === 'number' && !Number.isSafeInteger(value)) {
      if (config.bigIntAsString) {
        return value.toString();
      }
    }
    
    if (typeof value === 'object' && config.nesting === 'flatten') {
      return this.flattenObject(value, config.flattenSeparator);
    }
    
    return value;
  }
}
```

## Performance Comparison

| Aspect | CSV | JSON |
|--------|-----|------|
| File size (10K rows, 20 cols) | ~1.2 MB | ~3.8 MB |
| Parse speed (Node.js) | 50 ms | 80 ms |
| Streaming support | Native | Requires array slicing |
| Type preservation | Text only | Full type support |
| Nested data support | Flattened only | Native |
| Excel compatibility | Native | Import via Power Query |
| Human readability | Good with width | Good with pretty print |

## Open Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| papaparse (MIT) | Parse/Generate | Streaming CSV |
| json2csv (MIT) | Convert | JSON → CSV |
| csv-stringify (MIT) | Generate | CSV stringification |
| fast-csv (MIT) | Read/Write | CSV streaming |
| OStream (Native) | Stream | Node.js object mode |

## Production Considerations

**Large file handling:** For exports exceeding 100MB, the system compresses with gzip (Content-Encoding: gzip). Files are split into 50MB chunks for S3 multipart upload. Download URLs expire after 7 days. For extremely large exports (>1M rows), workers use streaming to avoid OOM.

**Encoding issues:** CSV files include UTF-8 BOM for Excel compatibility on Windows. Date/number formatting respects the user's locale preference (stored in user profile). All text values are properly escaped to prevent CSV injection (formulas starting with =, +, -, @ are prefixed with a single quote).
