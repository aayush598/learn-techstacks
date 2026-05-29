# Section 07: Report Export Templates

## Overview

Export templates define the structure, formatting, and branding of exported reports. They allow users to create consistent, branded exports across CSV, JSON, and PDF formats. Templates include column selection, header/footer content, branding assets, and custom styles.

```
Export Template Architecture
┌─────────────────────────────────────────────────────────────────────────┐
│ Template Editor                     Export Pipeline                    │
│ ┌──────────────────────┐          ┌─────────────────────────────────┐ │
│ │ Visual Template      │          │ Export Job                      │ │
│ │ Builder              │─────────▶│ ┌────────────────────────┐      │ │
│ │ • Column selector    │          │ │ Resolve Template      │      │ │
│ │ • Header/footer      │          │ │ Merge with report data│      │ │
│ │ • Branding           │          │ │ Apply formatting       │      │ │
│ │ • Format-specific    │          │ │ Generate file          │      │ │
│ │   config (CSV/PDF)   │          │ └────────────────────────┘      │ │
│ └──────────────────────┘          └─────────────────────────────────┘ │
│        │                                                               │
│        ▼                                                               │
│ Template Store (JSON)            Template Preview                     │
│ ┌──────────────────────┐          ┌─────────────────────────────────┐ │
│ │ tenant-templates/    │          │ Live preview w/ sample data     │ │
│ │ ├── default-csv      │          │ "See what your template         │ │
│ │ ├── default-pdf      │          │  looks like with real data"     │ │
│ │ ├── executive-pdf    │          │ Refresh on any edit             │ │
│ │ └── custom-json      │          └─────────────────────────────────┘ │
│ └──────────────────────┘                                               │
└─────────────────────────────────────────────────────────────────────────┘
```

## Template Data Model

```typescript
interface ExportTemplate {
  id: string;
  tenantId: string;
  name: string;
  description: string;
  type: 'csv' | 'json' | 'pdf';
  
  isDefault: boolean;
  isBuiltin: boolean;
  
  format: 'csv' | 'json' | 'pdf';
  
  // Common settings (all formats)
  common: {
    branding: {
      logoUrl?: string;
      logoPosition: 'header' | 'footer' | 'top-left' | 'top-right';
      logoMaxWidth: number; // px
      primaryColor: string;
      secondaryColor: string;
      accentColor: string;
      companyName: string;
      companyAddress?: string;
    };
    
    header: {
      showTitle: boolean;
      showDateRange: boolean;
      showGeneratedAt: boolean;
      showTenantName: boolean;
      customHeaderText?: string;
    };
    
    footer: {
      showPageNumbers: boolean;
      showGeneratedAt: boolean;
      showDisclaimer: boolean;
      customFooterText?: string;
      disclaimerText?: string;
    };
    
    columns: {
      include: string[]; // selected field IDs
      order: string[]; // display order
      aliases: Record<string, string>; // field ID → display name
      visibility: Record<string, 'show' | 'hide'>;
      formatting: Record<string, ColumnFormat>;
    };
    
    localization: {
      locale: string; // e.g., 'en-US', 'de-DE'
      timezone: string;
      dateFormat: string;
      numberFormat: NumberFormat;
      currency: string;
    };
  };
  
  // CSV-specific settings
  csv: {
    delimiter: ',' | '\t' | '|' | ';';
    quoting: 'auto' | 'always' | 'never';
    encoding: 'utf8' | 'utf8-bom';
    includeHeader: boolean;
    nullRepresentation: string;
    booleanFormat: 'true/false' | 'yes/no' | '1/0';
    dateFormat: string;
    numberFormat: NumberFormat;
  };
  
  // JSON-specific settings
  json: {
    rootStructure: 'array' | 'keyedById' | 'keyedByDate';
    idField?: string;
    nesting: 'flatten' | 'preserve' | 'separateArrays';
    flattenSeparator: string;
    dateFormat: string;
    bigIntAsString: boolean;
    pretty: boolean;
    indent: number;
    includeNullFields: boolean;
    omitFields: string[];
  };
  
  // PDF-specific settings
  pdf: {
    templateId: string; // HTML template ID
    orientation: 'portrait' | 'landscape';
    paperSize: 'a4' | 'letter' | 'legal';
    margins: { top: number; right: number; bottom: number; left: number };
    chartResolution: number;
    renderDelay: number;
    watermark?: { text: string; opacity: number };
    password?: string;
    permissions: { printing: boolean; copying: boolean; modifying: boolean };
    colorScheme: 'light' | 'dark' | 'brand';
    fontFamily: string;
    fontSize: number;
  };
  
  metadata: {
    createdBy: string;
    createdAt: number;
    updatedAt: number;
    version: number;
    usageCount: number;
    lastUsedAt: number;
  };
}

interface ColumnFormat {
  type: 'number' | 'currency' | 'percentage' | 'date' | 'duration' | 'string' | 'boolean';
  precision?: number; // decimal places
  prefix?: string;
  suffix?: string;
  datePattern?: string;
  durationFormat?: 'seconds' | 'minutes' | 'hours' | 'auto';
  BooleanLabels?: { true: string; false: string };
  conditionalColor?: {
    rules: Array<{
      operator: 'gt' | 'gte' | 'lt' | 'lte' | 'eq' | 'neq' | 'between';
      value: number | [number, number];
      color: string;
    }>;
  };
}
```

## Template Editor Implementation

```typescript
class ExportTemplateService {
  async applyTemplate(
    templateId: string,
    reportData: ReportData,
    format: 'csv' | 'json' | 'pdf'
  ): Promise<ExportResult> {
    const template = await this.getTemplate(templateId);
    if (!template) throw new Error(`Template ${templateId} not found`);
    
    // Filter and order columns
    const columns = template.common.columns.include.filter(
      col => template.common.columns.visibility[col] !== 'hide'
    );
    
    const orderedColumns = template.common.columns.order.filter(c => columns.includes(c));
    const finalColumns = orderedColumns.length > 0
      ? orderedColumns
      : columns;
    
    // Apply column formatting
    const formattedData = reportData.rows.map(row => {
      const formatted: Record<string, any> = {};
      for (const col of finalColumns) {
        const rawValue = row[col];
        const format = template.common.columns.formatting[col];
        formatted[template.common.columns.aliases[col] || col] = format
          ? this.applyFormatting(rawValue, format, template.common.localization)
          : rawValue;
      }
      return formatted;
    });
    
    // Apply branding and header/footer
    const exportConfig = this.buildExportConfig(template, finalColumns);
    
    // Generate file
    const generator = this.getGenerator(format);
    const buffer = await generator.generate(formattedData, {
      ...exportConfig,
      header: this.renderHeader(template, reportData),
      footer: this.renderFooter(template),
      branding: template.common.branding,
    });
    
    return {
      buffer,
      mimeType: this.getMimeType(format),
      columns: finalColumns,
      rowCount: formattedData.length,
    };
  }
  
  private applyFormatting(
    value: any,
    format: ColumnFormat,
    locale: Localization
  ): string {
    if (value === null || value === undefined) return '';
    
    switch (format.type) {
      case 'number': {
        return this.formatNumber(value, format.precision || 0, locale);
      }
      case 'currency': {
        const formatted = this.formatNumber(value, format.precision || 2, locale);
        return `${format.prefix || locale.currency}${formatted}`;
      }
      case 'percentage': {
        const formatted = this.formatNumber(value * 100, format.precision || 1, locale);
        return `${formatted}%`;
      }
      case 'date': {
        if (format.datePattern) {
          return dayjs(value).format(format.datePattern);
        }
        return dayjs(value).format(locale.dateFormat);
      }
      case 'duration': {
        const seconds = typeof value === 'number' ? value : parseInt(value);
        switch (format.durationFormat) {
          case 'minutes': return `${(seconds / 60).toFixed(2)} min`;
          case 'hours': return `${(seconds / 3600).toFixed(2)} hrs`;
          case 'auto': {
            if (seconds < 60) return `${seconds}s`;
            if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${seconds % 60}s`;
            return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`;
          }
          default: return `${seconds}s`;
        }
      }
      case 'boolean': {
        return value ? format.BooleanLabels?.true || 'Yes' : format.BooleanLabels?.false || 'No';
      }
      default:
        return String(value);
    }
  }
  
  private renderHeader(template: ExportTemplate, reportData: ReportData): string {
    const parts: string[] = [];
    
    if (template.common.branding.logoUrl) {
      parts.push(`<img src="${template.common.branding.logoUrl}" style="max-width:${template.common.branding.logoMaxWidth}px" />`);
    }
    
    if (template.common.header.showTitle) {
      parts.push(`<h1 style="color:${template.common.branding.primaryColor}">${reportData.name}</h1>`);
    }
    
    if (template.common.header.showDateRange) {
      parts.push(`<div>Period: ${reportData.dateRange.start} — ${reportData.dateRange.end}</div>`);
    }
    
    if (template.common.header.showGeneratedAt) {
      parts.push(`<div>Generated: ${new Date().toLocaleString()}</div>`);
    }
    
    if (template.common.header.showTenantName) {
      parts.push(`<div>${template.common.branding.companyName}</div>`);
    }
    
    if (template.common.header.customHeaderText) {
      parts.push(`<div>${template.common.header.customHeaderText}</div>`);
    }
    
    return parts.join('\n');
  }
  
  private renderFooter(template: ExportTemplate): string {
    const parts: string[] = [];
    
    if (template.common.footer.showPageNumbers) {
      parts.push('Page {{page}} of {{totalPages}}');
    }
    
    if (template.common.footer.showGeneratedAt) {
      parts.push(`Generated: ${new Date().toLocaleString()}`);
    }
    
    if (template.common.footer.showDisclaimer) {
      parts.push(template.common.footer.disclaimerText || 'Confidential — for authorized recipients only');
    }
    
    if (template.common.footer.customFooterText) {
      parts.push(template.common.footer.customFooterText);
    }
    
    return parts.join(' | ');
  }
}
```

## Built-in Templates

| Template | Format | Best For | Key Features |
|----------|--------|----------|-------------|
| Default CSV | CSV | Spreadsheets | UTF-8 BOM, comma delimiter, headers |
| Default JSON | JSON | API integration | Array structure, pretty print, ISO dates |
| Default PDF | PDF | General | A4, portrait, light theme, header/footer |
| Executive Summary | PDF | Leadership | Landscape, chart images, KPI cards, watermark |
| Data Dump | CSV | Analysis | Tab delimiter, no header, all columns |
| Compliance Export | JSON | Auditing | Keyed by date, nested structure, audit trail |
| Custom Branded | PDF | Client deliverables | Company logo, brand colors, custom disclaimer |

## Open Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Handlebars (MIT) | Template | Header/footer rendering |
| dayjs (MIT) | Date | Date formatting with locales |
| numeral.js (MIT) | Number | Number/currency formatting |
| sharp (Apache 2.0) | Image | Logo resize and format conversion |
| Puppeteer (Apache 2.0) | PDF | Server-side PDF with HTML templates |

## Production Considerations

**Template caching:** Templates are cached in Redis with a 5-minute TTL to avoid database lookups on every export. Template updates invalidate the cache entry. Built-in templates are loaded from the application bundle (not the database) for fast cold-start.

**Versioning:** Templates are versioned — when a template is edited, a new version is created. Exports use the version that was active at schedule creation time (not the latest version) to ensure consistency. Users can "update to latest" on all scheduled exports using a template.

**Performance:** Column formatting is applied in a streaming pipeline for CSV/JSON exports. PDF template rendering uses pre-compiled Handlebars templates. Brand assets (logos) are cached at the CDN level with 1-hour TTL.
