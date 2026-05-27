# Section 04: Visualization Type Selector

## Overview

The visualization type selector provides a palette of chart and display widgets that report builders can add to the canvas and configure. It includes standard analytics visualizations (line charts, bar charts, pie charts, area charts, scatter plots, heatmaps), KPI-focused widgets (metric cards, gauges, progress bars), tabular views (sortable data tables, pivot tables, cross-tabulations), and special-purpose visualizations (funnel charts, geo maps, word clouds, timeline views).

Each visualization type has a configuration panel that dynamically renders field mapping controls based on the widget's data requirements. For example, a line chart requires at least one time dimension (x-axis) and one metric (y-axis), while a pie chart requires one dimension (slice) and one metric (value). The selector suggests appropriate visualizations based on the selected data fields — if the user selects one time field and one numeric field, the system highlights line chart and area chart as "recommended" visualizations.

## Architecture

```
              Visualization Type Selector Architecture

   Report Builder → Widget Palette → Visualization Registry
                                          |
                              ┌───────────┼───────────┐
                              ▼           ▼           ▼
                        Time Series    Categorical   KPI / Single
                        (line, area,   (bar, pie,    Value
                         scatter)       heatmap)     (metric, gauge)
                              |           |           |
                              ▼           ▼           ▼
                        Config Panels   Field Mappings   Data Validators
                              |           |           |
                              └───────────┼───────────┘
                                          ▼
                                    Render Engine
                                    (ECharts / D3)
```

## Design Decisions

- **Dynamic configuration panels per visualization type over fixed config form:** Each registered visualization type provides its own React component for the configuration panel. A line chart config panel shows x-axis, y-axis, series grouping, and line style options. A geo map config panel shows latitude, longitude, and value fields, plus map region selector. This allows each visualization to expose type-specific options without a bloated universal form. Trade-off: maintaining 15+ configuration panel components requires more development effort than a single config form, but provides a much better user experience.

- **Type-based data validation over runtime error handling:** Each visualization type declares a data schema (required fields, allowed field types, cardinality constraints) that is validated when the user applies the configuration. If a line chart's x-axis is set to a non-temporal field, an inline error is shown before query execution. Trade-off: the validation schema cannot catch all runtime issues (e.g., a date field with all null values), but reduces the most common configuration errors.

- **ECharts as primary renderer with D3 escape hatch over single charting library:** ECharts provides declarative configuration, built-in animations, and good performance for most visualization types. For custom visualizations (custom Sankey diagrams, network graphs, specialized geo overlays), a D3 renderer is available as a plugin. Trade-off: maintaining two rendering pipelines increases code complexity, and widget configurations must specify which renderer they target (limiting cross-renderer widget reuse).

## Implementation Approach

```typescript
interface VisualizationType {
  id: string;
  name: string;
  category: 'time_series' | 'categorical' | 'kpi' | 'tabular' | 'geo' | 'custom';
  icon: string;
  description: string;
  renderer: 'echarts' | 'd3' | 'html';
  defaultConfig: Record<string, unknown>;
  dataSchema: DataSchema;
  ConfigPanel: React.ComponentType<ConfigPanelProps>;
  validateData(data: QueryResult, config: Record<string, unknown>): ValidationResult;
  toRendererConfig(data: QueryResult, config: Record<string, unknown>): Record<string, unknown>;
}

interface DataSchema {
  requiredFields: FieldRequirement[];
  optionalFields: FieldOption[];
  constraints: DataConstraint[];
}

interface FieldRequirement {
  role: string; // 'x_axis', 'y_axis', 'value', 'series', 'latitude', 'longitude', 'slice'
  allowedTypes: ('string' | 'number' | 'date' | 'timestamp')[];
  cardinality: 'single' | 'multiple';
  description: string;
}

interface ConfigPanelProps {
  config: Record<string, unknown>;
  onChange: (config: Record<string, unknown>) => void;
  dataSource: DataSourceBinding;
  schema: DataSourceSchema;
}

class VisualizationRegistry {
  private types: Map<string, VisualizationType> = new Map();

  register(type: VisualizationType): void {
    this.types.set(type.id, type);
  }

  get(id: string): VisualizationType | undefined {
    return this.types.get(id);
  }

  getAll(): VisualizationType[] {
    return Array.from(this.types.values());
  }

  getByCategory(category: string): VisualizationType[] {
    return this.getAll().filter(t => t.category === category);
  }

  recommend(dataSource: DataSourceBinding, schema: DataSourceSchema): VisualizationType[] {
    const recommendations: VisualizationType[] = [];
    const selectedFields = Object.values(dataSource.fieldMappings);
    const hasDateField = selectedFields.some(f => {
      const col = this.findColumn(schema, f);
      return col?.type === 'date' || col?.type === 'timestamp';
    });
    const numericFieldCount = selectedFields.filter(f => {
      const col = this.findColumn(schema, f);
      return col?.isMetric;
    }).length;

    for (const type of this.types.values()) {
      const requirements = type.dataSchema.requiredFields;
      const allRequiredMet = requirements.every(req => {
        if (req.role === 'x_axis' && req.allowedTypes.includes('timestamp')) {
          return hasDateField;
        }
        if (req.role === 'y_axis' || req.role === 'value') {
          return numericFieldCount >= (req.cardinality === 'single' ? 1 : 2);
        }
        return true;
      });

      if (allRequiredMet) {
        recommendations.push(type);
      }
    }

    return recommendations;
  }

  private findColumn(schema: DataSourceSchema, fieldPath: string): ColumnSchema | null {
    for (const table of schema.tables) {
      const col = table.columns.find(c => c.name === fieldPath.split('.').pop());
      if (col) return col;
    }
    return null;
  }

  render(data: QueryResult, typeId: string, config: Record<string, unknown>): unknown {
    const type = this.get(typeId);
    if (!type) throw new Error(`Unknown visualization type: ${typeId}`);

    const rendererConfig = type.toRendererConfig(data, config);

    if (type.renderer === 'echarts') {
      return { type: 'echarts', option: rendererConfig };
    }

    if (type.renderer === 'd3') {
      return { type: 'd3', config: rendererConfig, data };
    }

    return { type: 'html', config: rendererConfig };
  }
}

// Example: Line chart registration
const lineChartType: VisualizationType = {
  id: 'line_chart',
  name: 'Line Chart',
  category: 'time_series',
  icon: 'chart-line',
  description: 'Trend over time',
  renderer: 'echarts',
  defaultConfig: {
    smooth: true,
    showSymbol: false,
    areaStyle: false,
    connectNulls: true,
  },
  dataSchema: {
    requiredFields: [
      { role: 'x_axis', allowedTypes: ['date', 'timestamp'], cardinality: 'single', description: 'Time dimension' },
      { role: 'y_axis', allowedTypes: ['number'], cardinality: 'multiple', description: 'Metric values' },
    ],
    optionalFields: [
      { role: 'series', allowedTypes: ['string'], cardinality: 'single', description: 'Group by field' },
    ],
    constraints: [
      { type: 'min_rows', value: 2, message: 'Line chart requires at least 2 data points' },
    ],
  },
  ConfigPanel: LineChartConfigPanel,
  validateData(data, config) {
    if (!data.rows || data.rows.length < 2) {
      return { valid: false, errors: ['At least 2 data points required'] };
    }
    return { valid: true, errors: [] };
  },
  toRendererConfig(data, config) {
    return {
      xAxis: { type: 'time', data: data.rows.map(r => r[config.xField as string]) },
      yAxis: { type: 'value' },
      series: (config.yFields as string[]).map((field: string) => ({
        name: field,
        type: 'line',
        smooth: config.smooth,
        areaStyle: config.areaStyle ? {} : undefined,
        data: data.rows.map(r => r[field]),
      })),
      tooltip: { trigger: 'axis' },
      grid: { containLabel: true },
    };
  },
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ECharts (Apache 2.0) | Client | Primary chart rendering engine |
| D3.js (ISC) | Client | Custom visualization rendering |
| React (MIT) | Client | Configuration panel components |
| react-colorful (MIT) | Client | Color picker for chart styling |

## Production Considerations

**Scaling:** Visualization rendering runs entirely on the client — the server only executes data queries and returns raw results. For reports with 20+ charts, lazy rendering with intersection observers ensures only visible charts are rendered initially, reducing DOM nodes by 60-80%. Chart animations are disabled when the browser detects reduced motion preferences or when the report contains more than 10 charts (CPU conservation).

**Security:** Visualization type registry is restricted per tenant — not all tenants have access to every visualization type. Custom visualization types (D3 plugins) are sandboxed in a web worker to prevent DOM manipulation outside the widget container. Chart configuration is validated against the type's JSON schema to prevent injection of malicious renderer options.

**Monitoring:** Track visualization type usage distribution (most/least used types), render latency per type (p50, p95), configuration validation failure rate, and data-to-visualization conversion error rate. Alert if render latency for any type exceeds 3 seconds, if configuration validation failures exceed 5% of save attempts, or if any visualization type has zero usage for 30 days (candidate for deprecation).
