# Section 04: Real-Time Data Views

## WebSocket Subscription Architecture

Real-time data views subscribe to WebSocket channels for live updates on calls, agent status, and system metrics. The subscription layer manages connection lifecycle, automatic reconnection, and optimistic state updates.

```
┌─────────────────────────────────────────────────────────────────────┐
│               REAL-TIME DATA VIEW PIPELINE                         │
│                                                                     │
│  ┌──────────┐    ┌──────────────┐    ┌─────────────────────┐       │
│  │ Backend  │    │  WebSocket   │    │   React Client      │       │
│  │ Service  │    │  Server      │    │                     │       │
│  │          │    │              │    │  ┌───────────────┐  │       │
│  │ Event →  │───→│  Broadcast   │───→│  │ useRealtime  │  │       │
│  │ Kafka    │    │  to Channel  │    │  │  Subscription │  │       │
│  │          │    │              │    │  └───────┬───────┘  │       │
│  │ Call     │    │  /calls      │    │          │          │       │
│  │ Service  │    │  /agents/123 │    │  ┌───────┴───────┐  │       │
│  │          │    │  /metrics    │    │  │  Optimistic   │  │       │
│  │ Agent    │    │  /campaign/7 │    │  │  Update Engine│  │       │
│  │ Service  │    │              │    │  └───────┬───────┘  │       │
│  │          │    │              │    │          │          │       │
│  │ Notif.   │    │              │    │  ┌───────┴───────┐  │       │
│  │ Service  │    │              │    │  │  React State  │  │       │
│  │          │    │              │    │  │  (Zustand)    │  │       │
│  └──────────┘    └──────────────┘    │  └───────┬───────┘  │       │
│                                       │          │          │       │
│                                       │  ┌───────┴───────┐  │       │
│                                       │  │  UI Component │  │       │
│                                       │  └───────────────┘  │       │
│                                       └─────────────────────┘       │
└─────────────────────────────────────────────────────────────────────┘
```

## WebSocket Subscription Hook

```typescript
interface SubscriptionConfig<TData> {
  channel: string;           // e.g., "calls", "agents:123"
  event: string;             // e.g., "call:status", "agent:state"
  initialData?: TData;
  onData?: (data: TData) => void;
  onError?: (error: Error) => void;
  enabled?: boolean;
}

interface SubscriptionState<TData> {
  data: TData | null;
  isConnected: boolean;
  isSubscribed: boolean;
  error: Error | null;
  lastUpdated: Date | null;
}

function useRealtimeSubscription<TData>(
  config: SubscriptionConfig<TData>
): SubscriptionState<TData> & {
  updateOptimistic: (data: Partial<TData>) => void;
  reconnect: () => void;
};
```

### Usage Example

```typescript
function ActiveCallsWidget() {
  const { data, isConnected, updateOptimistic } = useRealtimeSubscription<CallStatus[]>({
    channel: 'calls',
    event: 'call:status',
    initialData: [],
  });

  // Optimistic update for local mutations
  const handleMute = (callId: string) => {
    updateOptimistic((prev) =>
      prev.map((call) =>
        call.id === callId ? { ...call, isMuted: true } : call
      )
    );
  };

  return (
    <div>
      <LiveIndicator isConnected={isConnected} />
      <CallList calls={data} onMute={handleMute} />
    </div>
  );
}
```

## Optimistic Update Engine

Optimistic updates apply mutations locally before server confirmation, with rollback on error:

```typescript
interface OptimisticUpdate<TData> {
  id: string;
  apply: (data: TData) => TData;
  rollback: (data: TData) => TData;
  timestamp: number;
}

class OptimisticEngine<TData> {
  private pending: Map<string, OptimisticUpdate<TData>> = new Map();

  apply(update: OptimisticUpdate<TData>, currentData: TData): TData {
    this.pending.set(update.id, update);
    return update.apply(currentData);
  }

  confirm(updateId: string, currentData: TData): TData {
    this.pending.delete(updateId);
    return currentData;
  }

  reject(updateId: string, currentData: TData): TData {
    const update = this.pending.get(updateId);
    if (!update) return currentData;
    this.pending.delete(updateId);
    return update.rollback(currentData);
  }
}
```

## Skeleton Loading

```typescript
interface SkeletonConfig {
  variant: 'text' | 'circle' | 'rect' | 'card' | 'table';
  width?: string | number;
  height?: string | number;
  count?: number;            // Repeat skeleton N times
  animate?: boolean;         // Pulse animation
}

// Predefined skeletons for common views
const SKELETON_PRESETS = {
  statCard: { variant: 'card', width: '100%', height: 120 },
  tableRow: { variant: 'rect', width: '100%', height: 48, count: 5 },
  chart: { variant: 'rect', width: '100%', height: 300 },
  avatar: { variant: 'circle', size: 40 },
};
```

## Live Indicators

```typescript
interface LiveIndicatorProps {
  isConnected: boolean;
  label?: string;
  showLabel?: boolean;
  pulse?: boolean;
  variant?: 'dot' | 'badge' | 'bar';
}

// Connection states
type ConnectionQuality = 'excellent' | 'good' | 'degraded' | 'disconnected';
// Threshold: latency < 100ms, 100-300ms, 300-1000ms, > 1000ms
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Subscription library | Custom hook over Socket.IO client | Lightweight, framework-agnostic, tree-shakeable |
| State management | Zustand for real-time state | No boilerplate, built-in subscriptions, devtools |
| Optimistic updates | Local engine with rollback | Instant UI, consistent on conflict resolution |
| Connection indicator | WebSocket ping/pong latency | Real metric vs synthetic heartbeat |
| Skeleton loading | Tailwind animate-pulse | Zero JS, CSS-native, customizable |

## Integration Points

- **Ch 04 (Real-Time)** — WebSocket server event format matches subscription config
- **Ch 09 (Data Flow)** — Optimistic updates ordered via event sourcing ledger
- **Ch 10 (Security)** — WebSocket channel authorization via JWT claim validation

## Production Considerations

- **Connection Pooling**: Single WebSocket connection per tab, multiplexed subscriptions via channel messages
- **Reconnection Strategy**: Exponential backoff (1s, 2s, 4s, 8s, max 30s) with jitter
- **Memory Management**: Subscription cleanup on component unmount, max 50 active subscriptions per page
- **Error Recovery**: Automatic resubscribe on reconnect, missed events caught via last-event-id cursor
- **Bundle Size**: Real-time hooks add ~6KB gzipped, Zustand adds ~3KB gzipped
- **Latency Targets**: UI update within 200ms of server event, skeleton shown if > 500ms
