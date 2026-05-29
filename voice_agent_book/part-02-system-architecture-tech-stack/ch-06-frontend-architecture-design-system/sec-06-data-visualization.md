# Section 06: Data Visualization

## Chart Architecture

Data visualization uses **Recharts** for standard charts and **Nivo** for advanced visualizations. **TanStack Table** powers data tables with sorting, filtering, pagination, and column visibility controls.

```
┌─────────────────────────────────────────────────────────────────────┐
│                  DATA VISUALIZATION LAYER                          │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    CHART COMPONENTS                          │   │
│  │                                                              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │   │
│  │  │ LineChart│  │ BarChart │  │ AreaChart│  │  PieChart  │  │   │
│  │  │ (Recharts)│  │(Recharts)│  │(Recharts)│  │  (Nivo)   │  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────────┘  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │   │
│  │  │ Heatmap  │  │  Gauge   │  │  TreeMap │  │  Funnel    │  │   │
│  │  │  (Nivo)  │  │  (Nivo)  │  │  (Nivo)  │  │  (Recharts)│  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    DATA TABLE LAYER                         │   │
│  │                                                              │   │
│  │  ┌────────────────────────────────────────────────────────┐  │   │
│  │  │  TanStack Table (React Table v8)                      │  │   │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │  │   │
│  │  │  │ Sorting  │ │ Filtering│ │Pagination│ │ Column   │ │  │   │
│  │  │  │          │ │          │ │          │ │Visibility│ │  │   │
│  │  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ │  │   │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │  │   │
│  │  │  │Row Select│ │ Expand   │ │  Column  │ │  Global  │ │  │   │
│  │  │  │          │ │(Subrows) │ │  Pinning │ │  Search  │ │  │   │
│  │  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ │  │   │
│  │  └────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                DASHBOARD GRID LAYER                         │   │
│  │  ┌────────────────────────────────────────────────────────┐  │   │
│  │  │  Grid Layout (react-grid-layout)                      │  │   │
│  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │  │   │
│  │  │  │ Drag to  │ │ Resize   │ │ Add/     │ │ Layout   │ │  │   │
│  │  │  │ Rearrange│ │ Widgets  │ │ Remove   │ │ Persist  │ │  │   │
│  │  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ │  │   │
│  │  └────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Chart Component Pattern

```typescript
interface ChartConfig {
  data: Record<string, unknown>[];
  xKey: string;
  yKeys: { key: string; label: string; color: string }[];
  height?: number;
  showLegend?: boolean;
  showTooltip?: boolean;
  showGrid?: boolean;
  animate?: boolean;
  interval?: '1m' | '5m' | '15m' | '1h' | '1d';
}

// Example: Call volume chart with real-time updates
function CallVolumeChart() {
  const { data } = useRealtimeSubscription<CallMetric[]>({
    channel: 'metrics',
    event: 'call:volume',
  });

  return (
    <ChartCard title="Call Volume (24h)" interval="5m">
      <AreaChart data={data} height={300}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="timestamp" tickFormatter={formatTime} />
        <YAxis />
        <Tooltip />
        <Area
          type="monotone"
          dataKey="inbound"
          stroke="#3B82F6"
          fill="#3B82F6"
          fillOpacity={0.1}
        />
        <Area
          type="monotone"
          dataKey="outbound"
          stroke="#10B981"
          fill="#10B981"
          fillOpacity={0.1}
        />
      </AreaChart>
    </ChartCard>
  );
}
```

## Data Table with TanStack Table

```typescript
interface TableColumn<TData> {
  id: string;
  header: string;
  accessorKey: keyof TData;
  cell?: (info: CellContext<TData, unknown>) => React.ReactNode;
  enableSorting?: boolean;
  enableFiltering?: boolean;
  enableHiding?: boolean;
  size?: number; // Column width in pixels
}

function CallsDataTable() {
  const table = useReactTable({
    data: calls,
    columns: [
      { id: 'callId', header: 'Call ID', accessorKey: 'id', size: 100 },
      { id: 'agent', header: 'Agent', accessorKey: 'agentName', enableSorting: true },
      { id: 'status', header: 'Status', accessorKey: 'status',
        cell: ({ row }) => <StatusBadge status={row.original.status} />,
        enableFiltering: true,
      },
      { id: 'duration', header: 'Duration', accessorKey: 'duration',
        cell: ({ row }) => formatDuration(row.original.duration),
        enableSorting: true,
      },
      { id: 'cost', header: 'Cost', accessorKey: 'cost',
        cell: ({ row }) => `$${row.original.cost.toFixed(4)}`,
      },
    ],
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    initialState: { pagination: { pageSize: 25 } },
  });

  return <DataTable table={table} />;
}
```

## Real-Time Chart Updates

Charts receive streaming data updates via WebSocket and animate transitions:

```typescript
function RealTimeChart() {
  const [history, setHistory] = useState<DataPoint[]>([]);

  useRealtimeSubscription({
    channel: 'metrics',
    event: 'call:metric',
    onData: (point: DataPoint) => {
      setHistory((prev) => {
        const next = [...prev, point];
        // Keep last 100 points for 5-minute view
        return next.length > 100 ? next.slice(-100) : next;
      });
    },
  });

  return (
    <LineChart data={history}>
      <Line
        type="monotone"
        dataKey="value"
        stroke="#8884d8"
        animationDuration={300}
        dot={false}
        isAnimationActive={true}
      />
    </LineChart>
  );
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Chart library | Recharts (primary) + Nivo (advanced) | Recharts for 80% use cases, Nivo for heatmaps/sankey |
| Table library | TanStack Table v8 | Headless, virtual scrolling, infinite rows |
| Dashboard grid | react-grid-layout | Drag/resize, persist layout to localStorage |
| Color palette | Tailwind color scale | Consistent with design tokens, accessible contrast |
| Animations | Framer Motion layout animations | Smooth axis transitions, enter/exit animations |

## Integration Points

- **Ch 03 (Database)** — Chart queries use ClickHouse for time-series aggregation
- **Ch 04 (Real-Time)** — WebSocket feeds live chart data at 5-second intervals
- **Ch 09 (Data Flow)** — Materialized views optimized for dashboard queries

## Production Considerations

- **Performance**: Charts virtualize > 1000 data points via Downsampling; tables use TanStack Virtual for > 10000 rows
- **Bundle Size**: Recharts ~45KB gzipped, Nivo ~60KB gzipped, TanStack Table ~25KB gzipped
- **Lazy Loading**: Each chart type loaded dynamically — call volume chart doesn't load Nivo dependencies
- **Empty States**: Charts show "No data yet" illustration for first-time users
- **Export**: Charts exportable as PNG/SVG, tables exportable as CSV/XLSX via `xlsx` library
- **Accessibility**: All charts include `role="img"` with `aria-label` descriptions, keyboard-navigable tooltips
