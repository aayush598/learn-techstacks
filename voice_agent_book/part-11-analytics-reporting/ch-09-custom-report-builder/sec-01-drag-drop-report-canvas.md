# Section 01: Drag-and-Drop Report Canvas

## Overview

The drag-and-drop report canvas is the visual workspace where analysts build custom reports by dragging widgets — charts, tables, KPIs, text blocks — onto a grid layout and configuring their data bindings. The canvas provides real-time preview as widgets are added, resized, and rearranged, with snap-to-grid alignment and responsive breakpoints for dashboard and print layouts. It serves as the primary interface for the custom report builder, enabling non-technical users to create sophisticated analytics reports without SQL or code.

The canvas is built on a 12-column fluid grid system where each widget occupies a configurable number of columns and rows. Widgets are rendered inside draggable and resizable containers that emit position and dimension changes as the user manipulates them. The canvas state — widget positions, sizes, data bindings, and filter configurations — is serialized as a JSON report definition that can be saved, shared, and versioned. The canvas supports undo/redo, keyboard shortcuts, and multi-select for bulk operations.

## Architecture

```
                  Drag-and-Drop Report Canvas

   Report Builder UI (React) → Canvas Component
                                    |
                         ┌──────────┴──────────┐
                         ▼                     ▼
                   Grid Layout              Widget Renderer
                   (react-grid-layout)       (dynamic registry)
                         |                     |
                         ▼                     ▼
                   Position Store          Widget Config Store
                   (widget layout)         (data bindings)
                         |                     |
                         └──────────┬──────────┘
                                    ▼
                            Report Definition
                            (JSON serialized)
                                    |
                            Save / Share / Schedule
```

## Design Decisions

- **react-grid-layout with custom snap behavior over free-form positioning:** The canvas uses react-grid-layout's grid-based positioning with a configurable column count (default 12) and row height (default 50 px). Widgets snap to grid intersections, ensuring alignment without manual adjustment. Trade-off: grid layout cannot support overlapping widgets or absolute positioning, which some users may expect for presentation-style reports.

- **Widget registry with lazy loading over monolithic renderer:** Each widget type (line chart, bar chart, KPI card, data table, text block) is registered in a plugin-style registry and loaded on demand. This keeps the initial bundle size small (only the canvas + 2-3 core widget types) and allows third-party widget plugins. Trade-off: lazy loading introduces a brief loading indicator when a user first adds a widget type that hasn't been loaded yet (~500 ms for charting libraries).

- **Optimistic local state with periodic auto-save over explicit save-only:** The canvas saves the report definition to localStorage every 30 seconds and to the server every 2 minutes. If the user navigates away without saving, a dialog warns of unsaved changes. This reduces data loss risk while avoiding save-button fatigue. Trade-off: auto-save creates many small API calls; debouncing and diff-based saves (send only changed widgets) minimize server load.

## Implementation Approach

```typescript
interface ReportDefinition {
  id: string;
  tenantId: string;
  name: string;
  description?: string;
  layout: GridLayout;
  widgets: ReportWidget[];
  filters: ReportFilter[];
  dateRange: DateRangeConfig;
  version: number;
  createdAt: number;
  updatedAt: number;
  tags: string[];
}

interface ReportWidget {
  id: string;
  type: 'line_chart' | 'bar_chart' | 'pie_chart' | 'kpi_card' | 'data_table' | 'text_block'
       | 'gauge' | 'heatmap' | 'funnel' | 'geo_map';
  title: string;
  position: { x: number; y: number; width: number; height: number };
  dataSource: DataSourceBinding;
  visualizationConfig: Record<string, unknown>;
  style?: WidgetStyle;
}

interface DataSourceBinding {
  sourceId: string;
  query: string;
  fieldMappings: Record<string, string>;
  aggregation: 'sum' | 'avg' | 'count' | 'min' | 'max' | 'distinct';
  groupBy?: string[];
  sortBy?: { field: string; direction: 'asc' | 'desc' };
  limit?: number;
}

interface WidgetStyle {
  backgroundColor?: string;
  borderColor?: string;
  titleFontSize?: number;
  showLegend?: boolean;
  showDataLabels?: boolean;
  colorPalette?: string[];
}

class ReportCanvasStore {
  private definition: ReportDefinition;
  private autoSaveTimer: NodeJS.Timeout | null = null;
  private undoStack: ReportDefinition[] = [];
  private redoStack: ReportDefinition[] = [];

  constructor(initial: ReportDefinition) {
    this.definition = initial;
    this.startAutoSave();
  }

  addWidget(type: ReportWidget['type'], position: { x: number; y: number }): void {
    this.pushUndo();
    const widget: ReportWidget = {
      id: generateId(),
      type,
      title: `New ${type.replace('_', ' ')}`,
      position: { ...position, width: 4, height: 2 },
      dataSource: { sourceId: '', query: '', fieldMappings: {}, aggregation: 'count' },
      visualizationConfig: this.getDefaultConfig(type),
    };
    this.definition.widgets.push(widget);
    this.definition.updatedAt = Date.now();
  }

  updateWidgetPosition(
    widgetId: string,
    position: { x: number; y: number; width: number; height: number }
  ): void {
    const widget = this.definition.widgets.find(w => w.id === widgetId);
    if (widget) {
      widget.position = position;
      this.definition.updatedAt = Date.now();
    }
  }

  updateWidgetConfig(widgetId: string, config: Partial<ReportWidget>): void {
    this.pushUndo();
    const widget = this.definition.widgets.find(w => w.id === widgetId);
    if (widget) {
      Object.assign(widget, config);
      this.definition.updatedAt = Date.now();
    }
  }

  removeWidget(widgetId: string): void {
    this.pushUndo();
    this.definition.widgets = this.definition.widgets.filter(w => w.id !== widgetId);
    this.definition.updatedAt = Date.now();
  }

  undo(): void {
    if (this.undoStack.length === 0) return;
    this.redoStack.push(structuredClone(this.definition));
    this.definition = this.undoStack.pop()!;
  }

  redo(): void {
    if (this.redoStack.length === 0) return;
    this.undoStack.push(structuredClone(this.definition));
    this.definition = this.redoStack.pop()!;
  }

  private pushUndo(): void {
    this.undoStack.push(structuredClone(this.definition));
    if (this.undoStack.length > 50) {
      this.undoStack.shift();
    }
    this.redoStack = [];
  }

  private startAutoSave(): void {
    this.autoSaveTimer = setInterval(() => {
      this.saveToLocalStorage();
    }, 30000);
  }

  dispose(): void {
    if (this.autoSaveTimer) clearInterval(this.autoSaveTimer);
  }

  private saveToLocalStorage(): void {
    try {
      localStorage.setItem(
        `report:draft:${this.definition.id}`,
        JSON.stringify(this.definition)
      );
    } catch {
      // localStorage full — skip
    }
  }

  serialize(): ReportDefinition {
    return structuredClone(this.definition);
  }

  getLayout(): GridLayout {
    return {
      items: this.definition.widgets.map(w => ({
        id: w.id,
        x: w.position.x,
        y: w.position.y,
        width: w.position.width,
        height: w.position.height,
      })),
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| react-grid-layout (MIT) | Client | Drag-and-drop grid layout engine |
| React DnD (MIT) | Client | Drag-and-drop widget palette |
| Immer (MIT) | Client | Immutable state management for undo/redo |
| localStorage (built-in) | Client | Draft auto-save |

## Production Considerations

**Scaling:** The canvas serializes the full report definition as JSON; reports with 50+ widgets may produce definitions exceeding 500 KB. Implement lazy widget deserialization — load widget configs on demand as the user scrolls to them. For collaborative editing, replace localStorage auto-save with WebSocket-based operational transform (OT) to handle concurrent edits without conflicts.

**Security:** Report definitions are tenant-scoped and validated server-side before save to prevent injection of malicious widget configurations. The data source binding query field is parameterized to prevent injection attacks — users select from pre-defined data sources and metrics rather than writing raw queries. Widget type registry validates that only approved widget types are instantiated per tenant.

**Monitoring:** Track canvas load time, auto-save success rate, undo/redo stack depth distribution, average report widget count, and session duration. Alert if auto-save success rate drops below 99%, if canvas load exceeds 3 seconds, or if any report definition exceeds 1 MB (indicating a bloated report that may cause performance issues).
