# Section 08: Real-Time Dashboards & Status

## Overview

Real-time dashboards display active alerts, alert history, SLA timers, and system status. WebSocket connections push updates to dashboards as alerts fire, acknowledge, or resolve. The dashboard service aggregates alert data and computes real-time status indicators.

## Implementation Approach

```typescript
interface DashboardState {
  activeAlerts: ActiveAlert[];
  alertHistory: AlertSummary[];
  slaTimers: SLATimer[];
  systemStatus: SystemStatus;
  metrics: DashboardMetrics;
}

interface ActiveAlert {
  id: string;
  title: string;
  severity: string;
  status: string;
  elapsed: number; // seconds since firing
  slaRemaining: number; // seconds
  assignee?: string;
}

class AlertDashboardService {
  async getDashboardState(tenantId: string): Promise<DashboardState> {
    const [active, history, metrics] = await Promise.all([
      this.getActiveAlerts(tenantId),
      this.getAlertHistory(tenantId),
      this.computeMetrics(tenantId),
    ]);

    return {
      activeAlerts: active.map(a => ({
        ...a,
        elapsed: this.getElapsedSeconds(a.createdAt),
        slaRemaining: this.getSLARemaining(a),
      })),
      alertHistory: history,
      slaTimers: this.computeSLATimers(active),
      systemStatus: this.computeSystemStatus(active),
      metrics,
    };
  }

  // WebSocket push for real-time updates
  async pushAlertUpdate(alert: Alert): Promise<void> {
    const state = await this.getDashboardState(alert.tenantId);
    await this.wsServer.publish(`dashboard:${alert.tenantId}`, {
      type: 'alert_update',
      alert,
      state,
    });
  }

  async subscribeToUpdates(tenantId: string, ws: WebSocket): Promise<void> {
    const channel = `dashboard:${tenantId}`;
    await this.wsServer.subscribe(channel, ws);

    // Push initial state
    const initialState = await this.getDashboardState(tenantId);
    ws.send(JSON.stringify({ type: 'initial_state', state: initialState }));
  }

  private computeSLATimers(alerts: ActiveAlert[]): SLATimer[] {
    return alerts.map(a => {
      const remaining = a.slaRemaining - a.elapsed;
      return {
        alertId: a.id,
        severity: a.severity,
        remaining,
        breached: remaining < 0,
      };
    });
  }

  private computeSystemStatus(alerts: ActiveAlert[]): SystemStatus {
    const criticalCount = alerts.filter(a => a.severity === 'critical').length;
    if (criticalCount > 0) return { level: 'critical', message: `${criticalCount} critical alerts` };
    if (alerts.length > 5) return { level: 'degraded', message: `${alerts.length} active alerts` };
    return { level: 'healthy', message: 'All systems operational' };
  }
}
```

## Integration Points

- **WebSocket Server**: Real-time push to browser dashboards
- **Alert API**: REST endpoints for dashboard data
- **Status Page**: Public status page showing system health

## Production Considerations

- **Connection Scaling**: WebSocket connections scale horizontally
- **Throttling**: Throttle dashboard updates to prevent UI overload
- **Caching**: Dashboard state cached for quick initial load
