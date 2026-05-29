# Section 07: Report Templates & Themes

## Templates Framework

Report templates provide reusable report configurations that users can instantiate with their own data sources and filters. Themes control the visual appearance of reports including colors, typography, and layout spacing.

```
Templates & Themes Architecture
┌─────────────────────────────────────────────────────────────────────────┐
│ Template Store        Theme Engine        User Preferences             │
│ ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐          │
│ │ Built-in     │    │ Base Theme   │    │ User overrides   │          │
│ │ templates    │───▶│ (CSS vars)   │───▶│ saved per report │          │
│ │ (20+)        │    │              │    │                  │          │
│ └──────────────┘    │ Color palette│    │ Layout density   │          │
│ ┌──────────────┐    │ Typography   │    │ Widget defaults  │          │
│ │ Community    │    │ Spacing      │    │                  │          │
│ │ templates    │───▶│ Radius       │    │ Brand overlays   │          │
│ │ (uploaded)   │    │              │    │                  │          │
│ └──────────────┘    └──────┬───────┘    └──────────────────┘          │
│ ┌──────────────┐           │                                           │
│ │ Custom user  │           ▼                                           │
│ │ templates    │    Compiled Theme (CSS output)                        │
│ │ (saved)      │                                                       │
│ └──────────────┘                                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

## Template System

### Built-in Templates
- **Call Performance Overview:** Call volume, duration, success rate, avg handle time
- **Agent Scorecard:** Agent metrics, QA scores, CSAT, adherence
- **Sentiment Trend:** Sentiment over time, by agent, by topic
- **Conversion Funnel:** Funnel stages, conversion rates, drop-off points
- **Revenue Report:** Revenue by plan, usage, MRR, ARPU
- **Quality Dashboard:** WER, latency, error rate, health score
- **Compliance Report:** Consent tracking, data retention, audit log
- **Executive Summary:** High-level KPIs, trends, growth metrics

### Template Data Model

```typescript
interface ReportTemplate {
  id: string;
  name: string;
  description: string;
  category: 'operations' | 'quality' | 'sales' | 'support' | 'compliance';
  predefined: boolean;
  version: number;
  
  definition: ReportDefinition;
  
  metadata: {
    author: string;
    thumbnail: string;
    screenshotUrl: string;
    tags: string[];
    usageCount: number;
    rating: number;
  };
  
  configuration: {
    requiredDataSources: DataSourceType[];
    defaultFilters: FilterConfig[];
    suggestedDateRange: 'today' | '7d' | '30d' | 'thisMonth';
    dataSourceMapping: Record<string, string>; // template source → user source
  };
}
```

## Theme System

Themes use CSS custom properties (CSS variables) so they can be applied at runtime without recompiling the UI. Users can customize colors, fonts, spacing, and border radius through a visual editor.

```
Theme Variables
┌─────────────────────────────────────────────────────────────────────────┐
│ --color-primary: #6366f1    --font-heading: Inter    --radius-sm: 4px  │
│ --color-secondary: #8b5cf6  --font-body: Inter       --radius-md: 8px  │
│ --color-success: #22c55e    --font-mono: JetBrains   --radius-lg: 12px │
│ --color-warning: #f59e0b    --font-size-sm: 12px                       │
│ --color-error: #ef4444      --font-size-md: 14px    --spacing-sm: 8px  │
│ --color-bg: #ffffff         --font-size-lg: 16px    --spacing-md: 16px │
│ --color-bg-secondary: #f8f9fa                      --spacing-lg: 24px │
│ └───────────────────────────────────────────────────────────────────────┘
```

### Theme Data Model

```typescript
interface ReportTheme {
  id: string;
  name: string;
  type: 'light' | 'dark' | 'custom';
  
  colors: {
    primary: string;
    secondary: string;
    success: string;
    warning: string;
    error: string;
    info: string;
    
    background: string;
    backgroundSecondary: string;
    foreground: string;
    foregroundSecondary: string;
    border: string;
    
    chartColors: string[]; // 10-color palette for chart series
    chartBackground: string; // fills/gridlines
  };
  
  typography: {
    fontHeading: string;
    fontBody: string;
    fontMono: string;
    fontSize: {
      xs: number;
      sm: number;
      md: number;
      lg: number;
      xl: number;
      '2xl': number;
    };
  };
  
  spacing: {
    xs: number;
    sm: number;
    md: number;
    lg: number;
    xl: number;
  };
  
  borderRadius: {
    sm: number;
    md: number;
    lg: number;
    full: number;
  };
  
  customCSS?: string; // additional overrides
}

function compileTheme(theme: ReportTheme): Record<string, string> {
  const vars: Record<string, string> = {};
  
  Object.entries(theme.colors).forEach(([key, value]) => {
    vars[`--color-${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`] = value;
  });
  
  Object.entries(theme.typography.fontSize).forEach(([key, value]) => {
    vars[`--font-size-${key}`] = `${value}px`;
  });
  
  Object.entries(theme.spacing).forEach(([key, value]) => {
    vars[`--spacing-${key}`] = `${value}px`;
  });
  
  Object.entries(theme.borderRadius).forEach(([key, value]) => {
    vars[`--radius-${key}`] = `${value}px`;
  });
  
  return vars;
}
```

## Template Instantiation Flow

When a user picks a template, the system creates a copy of the report definition, maps the template's generic data sources to the user's actual data sources, applies default filters, and renders with the user's selected theme.

```typescript
class TemplateManager {
  async instantiateTemplate(params: {
    templateId: string;
    userId: string;
    dataSourceMappings: Record<string, string>; // templateSourceId → userSourceId
    overrides?: Partial<ReportDefinition>;
  }): Promise<string> {
    const template = await this.templateStore.get(params.templateId);
    if (!template) throw new Error('Template not found');
    
    const mappedReport = {
      ...template.definition,
      id: generateId(),
      name: `${template.name} (Copy)`,
      createdAt: Date.now(),
      createdBy: params.userId,
      
      dataSources: template.definition.dataSources.map(ds => ({
        ...ds,
        sourceId: params.dataSourceMappings[ds.sourceId] || ds.sourceId,
      })),
      
      widgets: template.definition.widgets.map(widget => ({
        ...widget,
        dataSource: widget.dataSource?.sourceId
          ? { ...widget.dataSource, sourceId: params.dataSourceMappings[widget.dataSource.sourceId] || widget.dataSource.sourceId }
          : widget.dataSource,
      })),
    };
    
    const merged = params.overrides
      ? this.deepMerge(mappedReport, params.overrides)
      : mappedReport;
    
    return this.reportStore.create(merged);
  }
  
  async saveAsTemplate(reportId: string, userId: string): Promise<string> {
    const report = await this.reportStore.get(reportId);
    
    const template: ReportTemplate = {
      id: generateId(),
      name: report.name,
      description: `Saved from report ${report.name}`,
      category: 'custom',
      predefined: false,
      version: 1,
      definition: this.anonymizeDefinition(report),
      metadata: {
        author: userId,
        thumbnail: await this.generateThumbnail(report.id),
        screenshotUrl: '',
        tags: [],
        usageCount: 0,
        rating: 0,
      },
      configuration: {
        requiredDataSources: report.dataSources.map(ds => ds.type),
        defaultFilters: [],
        suggestedDateRange: '7d',
        dataSourceMapping: {},
      },
    };
    
    return this.templateStore.create(template);
  }
}
```

## Built-in Themes

| Theme | Type | Best For | Key Colors |
|-------|------|----------|------------|
| Default Light | Light | General | Indigo #6366f1 |
| Default Dark | Dark | Dashboards | Indigo #818cf8 |
| Monochrome | Light | Print/PDF | Gray scale |
| Ocean | Light | Call centers | Blue #3b82f6 |
| Forest | Light | Quality | Green #22c55e |
| Sunset | Dark | Executive | Orange #f97316 |
| Midnight | Dark | Operations | Slate #64748b |
| High Contrast | Light | Accessibility | Black/white |
| Brand A | Light | Enterprise A | Custom |
| Brand B | Light | Enterprise B | Custom |

## Open Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Theme UI (MIT) | UI | Theme specification |
| Tailwind CSS (MIT) | CSS | Utility-based theming |
| CSS Variables | Standard | Runtime theme switching |
| html2canvas (MIT) | Client | Thumbnail generation |
| Chromium (BSD) | Server | Server-side PDF rendering |
