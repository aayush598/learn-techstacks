# Section 06: Dashboard Configuration Persistence

## Overview

Dashboard configuration persistence allows supervisors and operators to customize their monitoring dashboard layout, save multiple dashboard configurations, share dashboards with team members, and restore configurations across sessions and devices. Each user can have multiple dashboards (e.g., "Call Center Overview," "Agent Performance," "Queue Management"), each with a unique grid layout, widget selection, metric thresholds, and filter presets.

Configurations are stored server-side as JSON blobs in PostgreSQL, with versioning and audit history. The frontend manages UI state through a dedicated state machine that serializes layout changes, widget configs, and filter states. When a user modifies their dashboard (rearranges widgets, changes metrics, sets new thresholds), the changes are auto-saved after a 2-second debounce period. The system supports dashboard templates — pre-built configurations for common use cases that users can clone and customize.

## Architecture

```
              Dashboard Configuration System

   Frontend                          Backend
   ────────                          ────────
   Layout Engine                     Dashboard API
   (react-grid-layout)               (CRUD + Clone + Share)
         │                                │
   Config Store                    PostgreSQL
   (Zustand + persist)             (dashboards, widgets,
         │                          templates, shares)
   useAutoSave (debounce 2s)
         │                                │
   Version History                 Audit Log (Redis)
   (undo/redo stack)
```

## Design Decisions

- **Server-side storage as source of truth over localStorage:** While localStorage provides offline access and faster initial load, server-side storage ensures configuration consistency across devices, enables sharing, and provides backup. The frontend loads the configuration from the server on login, caches it in localStorage as a fallback, and syncs changes back to the server. Trade-off: server-side storage adds latency on save (50-100 ms), and conflicts can occur if a user makes changes from two devices simultaneously — the last write wins, with a notification to the user about the overwritten version.

- **Versioned configurations with undo history over single-config overwrite:** Each save creates a new version entry (stored in a `dashboard_versions` table), allowing users to undo changes, restore previous versions, and compare configurations. The frontend maintains a stack of the last 50 local states for immediate undo/redo without network calls. Server-side version history is retained for 30 days. Trade-off: versioning increases storage requirements (each dashboard generates ~10 versions per day on average), but compression (gzip of JSON config) keeps each version under 5 KB.

- **Granular widget permissions over monolithic dashboard access:** Each widget in a dashboard can be assigned a visibility level (private, team, tenant-wide) and edit permissions (owner only, team editors, anyone). This allows supervisors to create dashboards containing both public metrics and sensitive widgets (e.g., agent-by-agent performance) that are visible only to specific roles. Trade-off: granular permissions add complexity to the frontend authorization logic and require additional database queries, but they prevent data leakage without requiring multiple separate dashboards.

## Implementation Approach

```typescript
interface DashboardConfig {
  id: string;
  name: string;
  description: string;
  tenantId: string;
  ownerId: string;
  layout: WidgetLayout[];
  sharing: {
    visibility: 'private' | 'team' | 'tenant';
    sharedWith: Array<{ userId: string; role: 'viewer' | 'editor' }>;
  };
  filters: {
    campaignIds: string[];
    agentIds: string[];
    dateRange: { type: 'relative' | 'absolute'; value: string; start?: string; end?: string };
  };
  version: number;
  createdAt: number;
  updatedAt: number;
}

interface WidgetLayout {
  widgetId: string;
  widgetType: string;
  title: string;
  x: number;
  y: number;
  width: number;
  height: number;
  config: Record<string, unknown>;  // widget-specific config
  permissions: {
    visibility: 'private' | 'team' | 'tenant';
    editableBy: 'owner' | 'team' | 'anyone';
  };
}

class DashboardConfigService {
  private db: PostgresClient;
  private cache: Redis;

  async getDashboard(dashboardId: string, userId: string): Promise<DashboardConfig | null> {
    // Check cache first
    const cached = await this.cache.get(`dashboard:${dashboardId}`);
    if (cached) return JSON.parse(cached);

    const dashboard = await this.db.query(
      'SELECT * FROM dashboards WHERE id = $1 AND (owner_id = $2 OR visibility != \'private\')',
      [dashboardId, userId]
    );

    if (dashboard.rows.length === 0) return null;

    // Cache for 5 minutes
    const config = dashboard.rows[0].config;
    await this.cache.setex(`dashboard:${dashboardId}`, 300, JSON.stringify(config));
    return config;
  }

  async saveDashboard(
    config: DashboardConfig,
    userId: string
  ): Promise<void> {
    const newVersion = config.version + 1;

    // Insert new version
    await this.db.query(
      `INSERT INTO dashboard_versions (dashboard_id, version, config, created_by, created_at)
       VALUES ($1, $2, $3, $4, NOW())`,
      [config.id, newVersion, JSON.stringify(config), userId]
    );

    // Update dashboard record
    await this.db.query(
      `UPDATE dashboards SET config = $1, version = $2, updated_at = NOW()
       WHERE id = $3 AND (owner_id = $4 OR $4 IN (
         SELECT user_id FROM dashboard_shares WHERE dashboard_id = $3 AND role = 'editor'
       ))`,
      [JSON.stringify(config), newVersion, config.id, userId]
    );

    // Invalidate cache
    await this.cache.del(`dashboard:${config.id}`);
  }

  async cloneDashboard(
    sourceId: string,
    newName: string,
    userId: string
  ): Promise<DashboardConfig> {
    const source = await this.getDashboard(sourceId, userId);
    if (!source) throw new Error('Dashboard not found');

    const cloned: DashboardConfig = {
      ...source,
      id: generateId(),
      name: newName,
      ownerId: userId,
      sharing: { visibility: 'private', sharedWith: [] },
      version: 1,
      createdAt: Date.now(),
      updatedAt: Date.now(),
    };

    await this.saveDashboard(cloned, userId);
    return cloned;
  }
}

// Frontend auto-save hook
function useAutoSave(
  dashboardId: string,
  config: DashboardConfig,
  delayMs: number = 2000
): { isSaving: boolean; lastSaved: number | null; error: string | null } {
  const [isSaving, setIsSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const debouncedConfig = useDebounce(config, delayMs);

  useEffect(() => {
    if (!debouncedConfig) return;

    setIsSaving(true);
    setError(null);

    dashboardApi.saveDashboard(dashboardId, debouncedConfig)
      .then(() => {
        setLastSaved(Date.now());
        setIsSaving(false);
      })
      .catch((err) => {
        setError(err.message);
        setIsSaving(false);
      });
  }, [debouncedConfig, dashboardId]);

  return { isSaving, lastSaved, error };
}

// Undo/redo stack
class ConfigHistory {
  private stack: DashboardConfig[] = [];
  private pointer = -1;
  private maxSize = 50;

  push(config: DashboardConfig): void {
    // Discard future states if we're in the middle of the history
    this.stack = this.stack.slice(0, this.pointer + 1);
    this.stack.push(config);
    if (this.stack.length > this.maxSize) {
      this.stack.shift();
    }
    this.pointer = this.stack.length - 1;
  }

  undo(): DashboardConfig | null {
    if (this.pointer > 0) {
      this.pointer--;
      return { ...this.stack[this.pointer] };
    }
    return null;
  }

  redo(): DashboardConfig | null {
    if (this.pointer < this.stack.length - 1) {
      this.pointer++;
      return { ...this.stack[this.pointer] };
    }
    return null;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| PostgreSQL (PostgreSQL) | Server | Dashboard config storage |
| Zustand (MIT) | Client | State management with persist |
| react-grid-layout (MIT) | Client | Dashboard grid layout engine |
| use-debounce (MIT) | Client | Debounced auto-save hook |

## Production Considerations

**Scaling:** Dashboard configurations are small (< 10 KB per dashboard) and infrequently accessed (on page load and save). PostgreSQL handles millions of config records without issue. Use Redis caching with 5-minute TTL to reduce database load. For tenants with 10,000+ dashboards, partition the `dashboards` table by tenant ID. Archive dashboard versions older than 30 days to cold storage (S3 Parquet) for audit compliance.

**Security:** Dashboard ownership and sharing permissions are enforced at the API level. The `getDashboard` query filters by visibility (`private` dashboards only return if the requesting user is the owner, `team` dashboards return if the user is in the same team as the owner, `tenant` dashboards return for anyone in the tenant). Widget-level permissions are enforced on the frontend by filtering the widget list after loading the dashboard config. All save operations check that the user has `editor` permission.

**Monitoring:** Track dashboard load time (p50 < 100 ms, p95 < 300 ms), save success rate, and auto-save conflict rate. Alert if save failures exceed 2% — this may indicate database connectivity issues. Monitor dashboard version history growth and set TTL-based cleanup for old versions. Log all sharing changes (add/remove user, change visibility) with the acting user ID and timestamp.
