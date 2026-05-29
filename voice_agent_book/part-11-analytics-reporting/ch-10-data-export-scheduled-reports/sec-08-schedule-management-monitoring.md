# Section 08: Schedule Management & Monitoring

## Overview

The schedule management system provides a unified interface for creating, viewing, pausing, editing, and deleting scheduled exports across all delivery channels (email, Slack, webhook). The monitoring layer tracks delivery success rates, latency, and failures with alerting.

```
Schedule Management Architecture
┌─────────────────────────────────────────────────────────────────────────┐
│ Schedule Manager (API + UI)                                            │
│ ┌────────────────────────────────────────────────────────────────────┐ │
│ │ Schedule CRUD   │ Pause/Resume   │ Run Now    │ Clone  │ Delete   │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│         │                                                               │
│         ▼                                                               │
│ Schedule Registry (Postgres)                                            │
│ ┌────────────────────────────────────────────────────────────────────┐ │
│ │ export_schedules table                                              │ │
│ │ id, tenant_id, report_id, name, enabled, cron, timezone,           │ │
│ │ format, channel, config (JSONB), delivery_config (JSONB),          │ │
│ │ last_run, last_status, next_run, run_count, created_by, created_at │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│         │                                                               │
│         ▼                                                               │
│ BullMQ Scheduler   │  Delivery Monitor   │  Alert Engine              │
│ ┌──────────────┐    │  ┌──────────────┐   │  ┌────────────────────┐  │
│ │ Checkpoint   │    │  │ Delivery Log │   │  │ Consecutive        │  │
│ │ every 60s    │    │  │ → status     │   │  │ failures ≥ 3       │  │
│ │ for due jobs │    │  │ → latency    │   │  │ → notify creator   │  │
│ └──────────────┘    │  │ → attempts   │   │  │ Delivery rate      │  │
│                     │  │ → errors     │   │  │ drop > 20% → alert │  │
│                     │  └──────────────┘   │  └────────────────────┘  │
│                     └────────────────────┘                           │
└─────────────────────────────────────────────────────────────────────────┘
```

## Schedule CRUD API

```typescript
interface ScheduleManager {
  // CRUD operations
  create(userId: string, tenantId: string, params: CreateScheduleParams): Promise<ExportSchedule>;
  get(scheduleId: string): Promise<ExportSchedule>;
  list(tenantId: string, filters?: ScheduleFilters): Promise<PaginatedResult<ExportSchedule>>;
  update(scheduleId: string, params: Partial<CreateScheduleParams>): Promise<ExportSchedule>;
  delete(scheduleId: string): Promise<void>;
  
  // Lifecycle operations
  pause(scheduleId: string): Promise<void>;
  resume(scheduleId: string): Promise<void>;
  runNow(scheduleId: string): Promise<string>; // returns job ID
  clone(scheduleId: string, newName: string): Promise<ExportSchedule>;
  
  // Monitoring
  getDeliveryHistory(scheduleId: string, limit?: number): Promise<DeliveryLog[]>;
  getScheduleStats(scheduleId: string, period: DateRange): Promise<ScheduleStats>;
  getTenantStats(tenantId: string): Promise<TenantScheduleStats>;
}

class ScheduleManagerImpl implements ScheduleManager {
  private scheduleStore: ScheduleStore;
  private jobQueue: Queue;
  private cronService: CronService;
  private alertService: AlertService;
  
  async create(
    userId: string,
    tenantId: string,
    params: CreateScheduleParams
  ): Promise<ExportSchedule> {
    // Validate format/channel compatibility
    this.validateConfig(params);
    
    // Check tenant limits
    const currentCount = await this.scheduleStore.countByTenant(tenantId);
    const tenant = await this.tenantStore.get(tenantId);
    if (currentCount >= tenant.maxSchedules) {
      throw new Error(`Schedule limit reached (${tenant.maxSchedules})`);
    }
    
    const schedule: ExportSchedule = {
      id: generateId(),
      tenantId,
      reportId: params.reportId,
      name: params.name,
      enabled: true,
      format: params.format,
      channel: params.channel,
      cron: params.cron,
      timezone: params.timezone,
      config: params.config,
      delivery: params.delivery,
      lastRun: null,
      lastStatus: null,
      nextRun: this.cronService.getNextRun(params.cron, params.timezone),
      runCount: 0,
      createdBy: userId,
      createdAt: Date.now(),
      updatedAt: Date.now(),
    };
    
    await this.scheduleStore.create(schedule);
    await this.cronService.register(schedule);
    
    this.emitScheduleEvent('schedule.created', schedule);
    return schedule;
  }
  
  async pause(scheduleId: string): Promise<void> {
    const schedule = await this.scheduleStore.get(scheduleId);
    if (!schedule) throw new Error('Schedule not found');
    
    await this.scheduleStore.update(scheduleId, { enabled: false });
    await this.cronService.unregister(scheduleId);
    
    // Cancel any pending jobs
    await this.cancelPendingJobs(scheduleId);
    
    this.emitScheduleEvent('schedule.paused', schedule);
  }
  
  async resume(scheduleId: string): Promise<void> {
    const schedule = await this.scheduleStore.get(scheduleId);
    if (!schedule) throw new Error('Schedule not found');
    
    await this.scheduleStore.update(scheduleId, {
      enabled: true,
      nextRun: this.cronService.getNextRun(schedule.cron, schedule.timezone),
    });
    
    await this.cronService.register(schedule);
    
    // Reset consecutive failure counter
    await this.failureTracker.reset(scheduleId);
    
    this.emitScheduleEvent('schedule.resumed', schedule);
  }
  
  async runNow(scheduleId: string): Promise<string> {
    const schedule = await this.scheduleStore.get(scheduleId);
    if (!schedule) throw new Error('Schedule not found');
    
    // Create a one-off export job bypassing the cron trigger
    const jobId = await this.exportOrchestrator.createExportJob(
      schedule.reportId,
      schedule.tenantId,
      {
        format: schedule.format,
        channel: schedule.channel,
        config: schedule.config,
        delivery: schedule.delivery,
      }
    );
    
    this.emitScheduleEvent('schedule.run_now', { scheduleId, jobId: jobId.jobId });
    return jobId.jobId;
  }
  
  async clone(scheduleId: string, newName: string): Promise<ExportSchedule> {
    const original = await this.scheduleStore.get(scheduleId);
    if (!original) throw new Error('Schedule not found');
    
    const clone: ExportSchedule = {
      ...original,
      id: generateId(),
      name: newName,
      enabled: false, // disabled by default
      lastRun: null,
      lastStatus: null,
      nextRun: this.cronService.getNextRun(original.cron, original.timezone),
      runCount: 0,
      createdBy: original.createdBy, // same creator
      createdAt: Date.now(),
      updatedAt: Date.now(),
    };
    
    await this.scheduleStore.create(clone);
    return clone;
  }
  
  async delete(scheduleId: string): Promise<void> {
    const schedule = await this.scheduleStore.get(scheduleId);
    if (!schedule) throw new Error('Schedule not found');
    
    await this.cronService.unregister(scheduleId);
    await this.cancelPendingJobs(scheduleId);
    await this.scheduleStore.delete(scheduleId);
    
    // Archive delivery logs (mark as orphaned)
    await this.deliveryLogStore.orphanBySchedule(scheduleId);
    
    this.emitScheduleEvent('schedule.deleted', schedule);
  }
}
```

## Schedule Management UI

The schedule management page provides:
- **List view:** Table with name, channel, format, frequency, last run, next run, status (enabled/paused/failing)
- **Status indicators:** Green (healthy), yellow (last failed), red (consecutive failures ≥3)
- **Quick actions:** Pause/Resume, Run Now, Clone, Delete
- **Schedule editor:** Full configuration form matching the create flow
- **Delivery history:** Per-schedule log of recent deliveries with status, latency, error details

## Monitoring Dashboard

```
Schedule Monitor Dashboard
┌─────────────────────────────────────────────────────────────────────────┐
│ All Schedules     Active: 24     Paused: 3     Failed: 1               │
│                                                                         │
│ Delivery Health (Last 7 Days)                                           │
│ ┌──────────────────────────────────────────────────────────────────┐  │
│ │ Channel    │ Total   │ Success │ Failed │ Rate   │ Avg Latency  │  │
│ ├──────────────────────────────────────────────────────────────────┤  │
│ │ Email      │ 1,247   │ 1,238   │ 9      │ 99.3%  │ 4.2s         │  │
│ │ Slack      │ 845     │ 842     │ 3      │ 99.6%  │ 2.1s         │  │
│ │ Webhook    │ 412     │ 405     │ 7      │ 98.3%  │ 1.8s         │  │
│ │ Download   │ 2,301   │ 2,301   │ 0      │ 100%   │ 0.5s         │  │
│ └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│ Failing Schedules                                                       │
│ ┌────────────────────────────────────────────────────────────────────┐ │
│ │ Schedule                  │ Channel │ Failed │ Since    │ Last     │ │
│ ├────────────────────────────────────────────────────────────────────┤ │
│ │ 🔴 Weekly Report – Ops  │ Webhook │ 5 of 5 │ Apr 28   │ TIMEOUT  │ │
│ │ 🟡 Daily CSAT Summary   │ Email   │ 2 of 7 │ May 25   │ Bounced  │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ Recent Deliveries                                                       │
│ ┌────────────────────────────────────────────────────────────────────┐ │
│ │ Time           │ Schedule              │ Status  │ Latency │       │ │
│ ├────────────────────────────────────────────────────────────────────┤ │
│ │ 14:32:01       │ Daily Ops Summary    │ ✅ Delivered │ 3.2s  │       │ │
│ │ 14:30:00       │ Weekly CSAT Report   │ ❌ Failed    │ 30s   │       │ │
│ │ 14:25:00       │ Agent Scorecards     │ ✅ Delivered │ 2.1s  │       │ │
│ └────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Alerting Rules

| Condition | Severity | Action |
|-----------|----------|--------|
| 3 consecutive delivery failures | Warning | Notify schedule creator (in-app + email) |
| 5 consecutive delivery failures | Critical | Auto-pause schedule + notify + notify tenant admin |
| Delivery rate drop > 20% (7-day avg) | Warning | Notify tenant admin |
| Export generation failure rate > 5% | Warning | Notify engineering |
| Schedule not run for 30 days | Info | Notify creator: "This schedule hasn't been used in 30 days" |
| Recipient bounce rate > 5% (email) | Warning | Notify creator: "Some recipients are bouncing" |

## Batch Operations

```typescript
class ScheduleBatchOps {
  async bulkPause(tenantId: string, scheduleIds: string[]): Promise<BatchResult> {
    const results: BatchResultItem[] = [];
    
    for (const id of scheduleIds) {
      try {
        await this.scheduleManager.pause(id);
        results.push({ id, success: true });
      } catch (error) {
        results.push({ id, success: false, error: error.message });
      }
    }
    
    return { total: scheduleIds.length, succeeded: results.filter(r => r.success).length, results };
  }
  
  async bulkUpdateFrequency(
    tenantId: string,
    scheduleIds: string[],
    newCron: string,
    newTimezone: string
  ): Promise<BatchResult> {
    // Similar with per-item error handling
  }
  
  async migrateChannel(
    scheduleIds: string[],
    oldChannel: DeliveryChannel,
    newChannel: DeliveryChannel,
    channelConfig: any
  ): Promise<BatchResult> {
    // Migrate schedules from one channel to another
    // e.g., migrate all email schedules to Slack
  }
}
```

## Open Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| BullMQ (MIT) | Queue | Cron scheduling and job management |
| cron-parser (MIT) | Parse | Cron expression parsing |
| cronstrue (MIT) | Display | Human-readable cron descriptions |
| node-cron (MIT) | Scheduler | Lightweight in-process cron |
| timespan (MIT) | Time | Time range calculations |

## Production Considerations

**Cron accuracy:** BullMQ scheduler checks for due jobs every 60 seconds. For schedules requiring minute-level precision (<5 min intervals), use a dedicated scheduler with 10-second polling interval. All schedule times are stored in UTC and converted to the user's timezone for display.

**Scale limits:** Max 100 active schedules per tenant (configurable per plan). Max 50 schedules created per hour per tenant (rate-limited). The scheduler handles up to 10,000 active schedules across all tenants on a single BullMQ worker.

**Data retention:** Schedule definitions kept indefinitely. Delivery logs retained for 90 days, then aggregated into monthly stats (total deliveries, success rate, avg latency). Orphaned schedules (report deleted) are auto-paused and flagged for cleanup after 30 days.
