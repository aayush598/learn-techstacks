# Section 03: PDF Report Generation

## Overview

PDF reports produce visually formatted, print-ready documents suitable for executive presentations, client deliverables, and compliance documentation. PDFs are generated server-side using headless Chromium (Puppeteer) with HTML/CSS templates.

```
PDF Generation Pipeline
┌─────────────────────────────────────────────────────────────────────────┐
│ Report Definition     Template Engine            Puppeteer             │
│ ┌──────────────┐    ┌──────────────────┐    ┌────────────────────┐   │
│ │ Widgets      │    │ Template (HTML)  │    │ Launch Chromium    │   │
│ │ Data sources │───▶│ + CSS            │───▶│ Load HTML          │   │
│ │ Filters      │    │ + Handlebars     │    │ Wait for rendering │   │
│ │ Layout       │    │ + Chart images   │    │ Generate PDF       │   │
│ └──────────────┘    └──────────────────┘    │ Close browser      │   │
│                                              └────────────────────┘   │
│        │                        │                                      │
│        ▼                        ▼                                      │
│ ┌──────────────┐    ┌──────────────────┐                              │
│ │ Data Fetcher │    │ Chart Renderer   │                              │
│ │ ClickHouse   │    │ SVG → PNG        │                              │
│ │ → JSON       │    │ ECharts/Recharts │                              │
│ └──────────────┘    └──────────────────┘                              │
└─────────────────────────────────────────────────────────────────────────┘
```

## Template System

PDF templates are HTML files with Handlebars template syntax. Templates support variables for data, charts (rendered as base64 PNG images), and metadata. Built-in templates include Executive Summary, Detailed Report, and Compliance Audit.

### Template Example

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: 'Inter', sans-serif; font-size: 11pt; color: #1a1a2e; }
    .header { border-bottom: 3px solid #6366f1; padding-bottom: 12px; margin-bottom: 20px; }
    .header h1 { font-size: 18pt; margin: 0; }
    .header .meta { color: #64748b; font-size: 9pt; margin-top: 4px; }
    
    .chart { margin: 20px 0; page-break-inside: avoid; }
    .chart img { width: 100%; max-height: 300px; }
    .chart .caption { font-size: 9pt; color: #64748b; margin-top: 4px; }
    
    table.kpi-table { width: 100%; border-collapse: collapse; margin: 16px 0; }
    table.kpi-table th { background: #f1f5f9; padding: 8px 12px; text-align: left; font-size: 9pt; }
    table.kpi-table td { padding: 8px 12px; border-bottom: 1px solid #e2e8f0; font-size: 10pt; }
    .kpi-value { font-weight: 700; font-size: 12pt; }
    .kpi-label { color: #64748b; font-size: 8pt; text-transform: uppercase; }
    
    .footer { position: fixed; bottom: 0; width: 100%; text-align: center; 
              font-size: 8pt; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 8px; }
    .page-break { page-break-before: always; }
  </style>
</head>
<body>
  <div class="header">
    <h1>{{reportName}}</h1>
    <div class="meta">
      Generated: {{generatedAt}} | Period: {{dateRange.start}} - {{dateRange.end}}
      | Tenant: {{tenantName}}
    </div>
  </div>
  
  <div class="kpi-summary">
    <table class="kpi-table">
      <tr>
        {{#each kpis}}
        <td>
          <div class="kpi-label">{{label}}</div>
          <div class="kpi-value" style="color: {{color}}">{{value}}</div>
        </td>
        {{/each}}
      </tr>
    </table>
  </div>
  
  {{#each sections}}
  <div class="section">
    {{#if pageBreak}}<div class="page-break"></div>{{/if}}
    <h2>{{title}}</h2>
    
    {{#if chart}}
    <div class="chart">
      <img src="data:image/png;base64,{{chart}}" alt="{{title}}" />
      <div class="caption">{{caption}}</div>
    </div>
    {{/if}}
    
    {{#if table}}
    <table class="kpi-table">
      <tr>
        {{#each table.headers}}
        <th>{{this}}</th>
        {{/each}}
      </tr>
      {{#each table.rows}}
      <tr>
        {{#each this}}
        <td>{{this}}</td>
        {{/each}}
      </tr>
      {{/each}}
    </table>
    {{/if}}
  </div>
  {{/each}}
  
  <div class="footer">
    Page <span class="pageNumber"></span> of <span class="totalPages"></span>
  </div>
</body>
</html>
```

## Implementation

```typescript
interface PDFExportConfig {
  templateId: string;
  orientation: 'portrait' | 'landscape';
  paperSize: 'a4' | 'letter' | 'legal';
  margins: { top: number; right: number; bottom: number; left: number };
  
  includeFooter: boolean;
  includePageNumbers: boolean;
  
  chartResolution: number; // DPI for chart images (default: 144)
  renderDelay: number; // ms to wait for chart animations (default: 1000)
  
  watermark?: {
    text: string;
    opacity: number;
  };
  
  password?: string; // PDF encryption password
  permissions?: {
    printing: boolean;
    copying: boolean;
    modifying: boolean;
  };
}

class PDFGenerator {
  private browserPool: BrowserPool;
  private templateEngine: TemplateEngine;
  private chartRenderer: ChartRenderer;
  
  async generate(
    data: ReportData,
    config: PDFExportConfig
  ): Promise<Buffer> {
    // 1. Fetch template
    const template = await this.templateEngine.get(config.templateId);
    
    // 2. Render charts to base64 PNGs
    const chartImages = await this.renderCharts(data.charts, config.chartResolution);
    
    // 3. Build template context
    const context = {
      reportName: data.reportName,
      generatedAt: new Date().toLocaleString(),
      dateRange: data.dateRange,
      tenantName: data.tenantName,
      kpis: data.kpis.map(kpi => ({
        label: kpi.label,
        value: kpi.formattedValue,
        color: kpi.trend === 'up' ? '#22c55e' : kpi.trend === 'down' ? '#ef4444' : '#64748b',
      })),
      sections: data.sections.map((section, i) => ({
        title: section.title,
        chart: chartImages[i] || null,
        caption: section.caption,
        table: section.table ? {
          headers: section.table.columns.map(c => c.label),
          rows: section.table.rows.map(r => section.table.columns.map(c => r[c.key])),
        } : null,
        pageBreak: i > 0 && section.forcePageBreak,
      })),
    };
    
    // 4. Render HTML
    const html = template.render(context);
    
    // 5. Generate PDF with Puppeteer
    const browser = await this.browserPool.acquire();
    try {
      const page = await browser.newPage();
      await page.setContent(html, { waitUntil: 'networkidle0' });
      
      // Wait for chart rendering and fonts
      await page.waitForTimeout(config.renderDelay);
      
      const pdf = await page.pdf({
        format: config.paperSize,
        orientation: config.orientation,
        margin: config.margins,
        printBackground: true,
        displayHeaderFooter: config.includeFooter,
        headerTemplate: '<span></span>',
        footerTemplate: config.includePageNumbers
          ? '<div style="font-size:8pt;color:#94a3b8;text-align:center;width:100%">Page <span class="pageNumber"></span> of <span class="totalPages"></span></div>'
          : '<span></span>',
      });
      
      // Apply encryption if password is set
      if (config.password) {
        return await this.encryptPDF(pdf, config.password, config.permissions);
      }
      
      return pdf;
      
    } finally {
      await this.browserPool.release(browser);
    }
  }
  
  private async renderCharts(
    chartConfigs: ChartConfig[],
    resolution: number
  ): Promise<string[]> {
    const promises = chartConfigs.map(async (chartConfig) => {
      // Render chart to SVG using the same charting library (ECharts/Recharts)
      const svg = await this.chartRenderer.renderToSVG(chartConfig, {
        width: 800,
        height: 400,
        theme: 'print',
      });
      
      // Convert SVG to PNG at specified resolution
      const png = await sharp(Buffer.from(svg))
        .resize({
          width: 800 * (resolution / 72),
          height: 400 * (resolution / 72),
        })
        .png()
        .toBuffer();
      
      return png.toString('base64');
    });
    
    return Promise.all(promises);
  }
  
  private async encryptPDF(
    pdf: Buffer,
    password: string,
    permissions?: PDFExportConfig['permissions']
  ): Promise<Buffer> {
    // Use qpdf or similar for PDF encryption
    const tmpInput = `/tmp/pdf-${generateId()}.pdf`;
    const tmpOutput = `/tmp/pdf-${generateId()}.encrypted.pdf`;
    
    await fs.writeFile(tmpInput, pdf);
    
    const args = [
      '--encrypt',
      password, // user password
      password, // owner password
      '256', // key length
      ...(permissions?.printing ? [] : ['--no-print']),
      ...(permissions?.copying ? [] : ['--no-copy']),
      ...(permissions?.modifying ? [] : ['--no-modify']),
      tmpInput,
      tmpOutput,
    ];
    
    await exec('qpdf', args);
    const encrypted = await fs.readFile(tmpOutput);
    
    // Cleanup
    await Promise.all([
      fs.unlink(tmpInput),
      fs.unlink(tmpOutput),
    ]);
    
    return encrypted;
  }
}
```

## Built-in Templates

| Template | Best For | Sections | Orientation |
|----------|----------|----------|-------------|
| Executive Summary | Leadership, clients | KPI cards, trend charts, key insights | Portrait |
| Detailed Report | Operations, QA | KPI cards, trend charts, tables, agent breakdown | Portrait |
| Compliance Report | Auditors, regulators | All data tables, no charts, watermark | Portrait |
| Agent Performance | HR, management | Scorecards, trend charts, comparison | Landscape |
| Call Log Detail | Operations | Full data table, minimal formatting | Landscape |

## Performance Benchmarks

| Report Complexity | Pages | Data Points | Generation Time | File Size |
|-------------------|-------|-------------|-----------------|-----------|
| Simple (KPI cards only) | 1-2 | 10-20 | 1.5 seconds | 150 KB |
| Standard (KPI + 2 charts) | 3-5 | 50-100 | 3 seconds | 500 KB |
| Complex (KPI + 4 charts + table) | 6-10 | 200-500 | 5 seconds | 1.2 MB |
| Full (all sections, 10+ charts) | 15-25 | 1000+ | 10 seconds | 3 MB |

## Open Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Puppeteer (Apache 2.0) | Server | Headless Chromium PDF generation |
| Puppeteer Cluster (MIT) | Server | Browser pool management |
| Handlebars (MIT) | Template | HTML templating |
| ECharts (Apache 2.0) | Chart | Server-side SVG rendering |
| sharp (Apache 2.0) | Image | SVG → PNG conversion |
| qpdf (Artistic 2.0) | PDF | PDF encryption and manipulation |

## Production Considerations

**Browser pooling:** Maintain a pool of 5-10 warm Chromium instances to avoid cold-start latency (which adds ~2 seconds per PDF). Each browser handles one PDF at a time. If queue depth exceeds pool capacity, jobs are queued in BullMQ with a priority system (interactive downloads > scheduled reports).

**Resource limits:** Each PDF job is allocated 512 MB RAM and 30 seconds max runtime. Puppeteer runs in a sandboxed container with no network access (all assets pre-loaded). Font files are bundled with the application to ensure consistent rendering across environments.

**Error handling:** If a PDF fails (timeout, OOM, Chromium crash), the job retries up to 3 times with exponential backoff. Failed PDFs fall back to CSV export if the user has enabled that preference. All PDF generation errors are logged with the template version and data snapshot for debugging.
