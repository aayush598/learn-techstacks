# Section 03: Filter and Date Range Configuration

## Overview

The filter and date range configuration system enables report builders to define reusable filter conditions and time window presets that apply across all widgets in a report. Global filters (applied to every widget) and widget-level filters (scoped to a specific widget) are both supported, with a cascade priority: widget-level filters override global filters for conflicting fields. The date range selector provides common presets (Last 7 days, This month, Last quarter, Year to date) and custom range pickers with calendar widgets.

Filters support multiple value types — single-select, multi-select, range sliders, date pickers, text search — and conditions that combine multiple rules with AND/OR/NOT logic. The filter state is stored as part of the report definition JSON and is applied at query time by the data source connectors. When report viewers interact with filter controls, the report re-renders in real-time with updated data, with debounced queries to avoid overwhelming the backend.

## Architecture

```
                 Filter and Date Range Architecture

   Report Builder → Filter Manager
                        |
              ┌─────────┴─────────┐
              ▼                   ▼
       Global Filters        Widget-Scoped
       (all widgets)         Filters
              |                   |
              └─────────┬─────────┘
                        ▼
                 Filter Combiner
                 (cascade priority)
                        |
              ┌─────────┴─────────┐
              ▼                   ▼
         Query Builder        URL Sync
         (apply filters)     (shareable URLs)
```

## Design Decisions

- **Global + scoped filter cascade over single-layer filters:** Global filters apply to every widget in the report (e.g., "Campaign = Summer Promo"). Widget-level filters override specific fields for individual widgets (e.g., a CSAT trend widget shows only "CSAT" survey type). This two-layer approach reduces redundancy while allowing per-widget customization. Trade-off: the cascade logic can be confusing when a widget shows unexpected data because a global filter and widget filter conflict in non-obvious ways; a "filter inspector" panel shows all active filters and their source.

- **Debounced query execution over immediate execution on every filter change:** When a user drags a date range slider or types in a text filter, the system debounces query execution by 500 ms. This prevents a burst of 20+ queries during rapid slider adjustment while still feeling responsive. Trade-off: the 500 ms debounce means the report preview lags slightly behind the mouse during rapid filter manipulation — users who need instant feedback must release the control and wait.

- **URL-serialized filter state over server-side session storage:** Active filter values are encoded in the URL query string using a compact serialization format (e.g., `?filters=campaign:summer,csatMin:4&daterange=last7d`). This enables bookmarking, sharing, and browser back/forward navigation for filter state. Trade-off: complex filters with many values can produce long URLs exceeding browser limits (2 KB in IE, 8 KB in modern browsers); these cases fall back to a short URL pointing to a server-stored filter config.

## Implementation Approach

```typescript
interface FilterConfig {
  id: string;
  type: 'date_range' | 'multi_select' | 'single_select' | 'range_slider' | 'text_search' | 'boolean';
  field: string;
  label: string;
  scope: 'global' | 'widget';
  widgetId?: string; // only for widget-scoped
  operator: 'eq' | 'neq' | 'in' | 'not_in' | 'between' | 'gt' | 'gte' | 'lt' | 'lte' | 'contains';
  value: FilterValue;
  defaultValue: FilterValue;
  options?: FilterOption[];
  enabled: boolean;
}

type FilterValue = string | number | boolean | string[] | number[] | DateRangeValue | null;

interface DateRangeValue {
  type: 'preset' | 'custom';
  preset?: 'last_24h' | 'last_7d' | 'last_30d' | 'this_month' | 'last_month'
         | 'this_quarter' | 'last_quarter' | 'this_year' | 'last_year' | 'all_time';
  customStart?: number;
  customEnd?: number;
  granularity?: 'raw' | 'hour' | 'day' | 'week' | 'month' | 'quarter';
}

interface FilterOption {
  label: string;
  value: string | number;
  group?: string;
}

class FilterManager {
  private globalFilters: FilterConfig[] = [];
  private widgetFilters: Map<string, FilterConfig[]> = new Map();
  private subscribers: Set<() => void> = new Set();
  private debounceTimer: NodeJS.Timeout | null = null;

  addGlobalFilter(filter: FilterConfig): void {
    this.globalFilters.push(filter);
    this.notify();
  }

  addWidgetFilter(widgetId: string, filter: FilterConfig): void {
    const existing = this.widgetFilters.get(widgetId) || [];
    existing.push(filter);
    this.widgetFilters.set(widgetId, existing);
    this.notify();
  }

  setFilterValue(filterId: string, value: FilterValue): void {
    // Find and update filter in global or widget scoped
    const filter = this.globalFilters.find(f => f.id === filterId)
      || Array.from(this.widgetFilters.values())
        .flat()
        .find(f => f.id === filterId);

    if (filter) {
      filter.value = value;
      this.debouncedNotify();
    }
  }

  setDateRange(preset: string): void {
    const dateFilter = this.globalFilters.find(f => f.type === 'date_range');
    if (dateFilter) {
      dateFilter.value = { type: 'preset', preset: preset as DateRangeValue['preset'] };
      this.debouncedNotify();
    }
  }

  getEffectiveFilters(widgetId: string): QueryParams['filters'] {
    const global = this.globalFilters
      .filter(f => f.enabled && f.value !== null && f.value !== undefined)
      .map(f => this.toQueryFilter(f));

    const widget = (this.widgetFilters.get(widgetId) || [])
      .filter(f => f.enabled && f.value !== null)
      .map(f => this.toQueryFilter(f));

    // Widget filters override global filters on the same field
    const globalMap = new Map(global.map(f => [f.field, f]));
    for (const wf of widget) {
      globalMap.set(wf.field, wf);
    }

    return Array.from(globalMap.values());
  }

  getEffectiveDateRange(): DateRangeValue | null {
    const dateFilter = this.globalFilters.find(f => f.type === 'date_range');
    return dateFilter?.value as DateRangeValue || null;
  }

  private toQueryFilter(filter: FilterConfig): QueryFilter {
    if (filter.type === 'date_range') {
      const range = filter.value as DateRangeValue;
      const { start, end } = this.resolveDateRange(range);
      return { field: 'timestamp', operator: 'between', value: [start, end] };
    }

    return {
      field: filter.field,
      operator: filter.operator,
      value: filter.value,
    };
  }

  private resolveDateRange(range: DateRangeValue): { start: number; end: number } {
    const now = Date.now();
    const presets: Record<string, { start: number; end: number }> = {
      last_24h: { start: now - 86400000, end: now },
      last_7d: { start: now - 7 * 86400000, end: now },
      last_30d: { start: now - 30 * 86400000, end: now },
      this_month: { start: this.startOfMonth(now), end: now },
      last_month: { start: this.startOfMonth(this.subtractMonth(now)), end: this.startOfMonth(now) },
      all_time: { start: 0, end: now },
    };

    if (range.type === 'preset' && range.preset && presets[range.preset]) {
      return presets[range.preset];
    }

    return {
      start: range.customStart || now - 7 * 86400000,
      end: range.customEnd || now,
    };
  }

  serializeToURL(): string {
    const params = new URLSearchParams();
    const activeFilters = this.globalFilters.filter(f => f.enabled && f.value !== null && f.value !== undefined);

    for (const filter of activeFilters) {
      const val = typeof filter.value === 'object' ? JSON.stringify(filter.value) : String(filter.value);
      params.set(`f_${filter.field}`, val);
    }

    const dateRange = this.getEffectiveDateRange();
    if (dateRange) {
      params.set('dr', dateRange.type === 'preset' ? dateRange.preset! : `${dateRange.customStart}_${dateRange.customEnd}`);
    }

    return params.toString();
  }

  private debouncedNotify(): void {
    if (this.debounceTimer) clearTimeout(this.debounceTimer);
    this.debounceTimer = setTimeout(() => this.notify(), 500);
  }

  private notify(): void {
    this.subscribers.forEach(cb => cb());
  }

  subscribe(cb: () => void): () => void {
    this.subscribers.add(cb);
    return () => this.subscribers.delete(cb);
  }

  private startOfMonth(ts: number): number {
    const d = new Date(ts);
    return new Date(d.getFullYear(), d.getMonth(), 1).getTime();
  }

  private subtractMonth(ts: number): number {
    const d = new Date(ts);
    return new Date(d.getFullYear(), d.getMonth() - 1, 1).getTime();
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| react-datepicker (MIT) | Client | Date range picker UI component |
| dayjs (MIT) | Client | Date manipulation and formatting |
| Immer (MIT) | Client | Immutable filter state updates |
| qs (MIT) | Client | URL query string serialization |

## Production Considerations

**Scaling:** Filter values are evaluated at query time, not pre-computed. For filters with many distinct values (e.g., "Agent" select with 10,000 agents), the filter options are loaded asynchronously with search-as-you-type rather than rendering a 10,000-item dropdown. Date range presets are computed client-side to avoid server round-trips; only custom date ranges require a server query.

**Security:** Filter field names are validated against the data source schema to prevent filter injection through URL manipulation. Multi-select filter value arrays are limited to 100 items per filter to prevent query bloat. The URL serialization does not include sensitive filter values; if a filter value contains PII (e.g., "Phone = 555-0100"), it is excluded from URL serialization and stored server-side.

**Monitoring:** Track filter application latency (time from filter change to query execution), average number of active filters per report, date range preset usage distribution, and URL serialization length percentiles. Alert if filter-to-query latency exceeds 2 seconds, if any single filter has more than 10,000 options (indicating a missing filter hierarchy), or if URL serialization truncation occurs more than 1% of the time.
