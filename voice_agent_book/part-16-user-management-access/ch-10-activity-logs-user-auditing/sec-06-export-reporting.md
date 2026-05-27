# Export & Reporting

## Overview

Log export provides activity data in CSV/JSON formats for compliance reporting, security analysis, and integration with external SIEM systems. Scheduled reports deliver logs to stakeholders on a recurring basis.

## Export Service

```typescript
class LogExportService {
  async exportLogs(query: LogSearchQuery, format: 'csv' | 'json'): Promise<ExportResult> {
    const logs = await this.searchService.search({
      ...query,
      limit: 10000, // Max export size
    });

    if (format === 'csv') {
      const csv = this.toCsv(logs.hits);
      const key = `exports/${query.context.tenantId}/${Date.now()}_activity_logs.csv`;
      await this.storage.put(key, csv);
      return { downloadUrl: await this.getSignedUrl(key), format, recordCount: logs.hits.length };
    }

    const key = `exports/${query.context.tenantId}/${Date.now()}_activity_logs.json`;
    await this.storage.put(key, JSON.stringify(logs.hits));
    return { downloadUrl: await this.getSignedUrl(key), format, recordCount: logs.hits.length };
  }

  async scheduleReport(config: ScheduledReportConfig): Promise<void> {
    await this.db.insert('scheduled_reports', {
      ...config,
      nextRunAt: this.calculateNextRun(config.schedule),
      createdAt: new Date(),
    });

    // Schedule via cron
    await this.queue.schedule({
      type: 'generate_report',
      data: { configId: config.id },
      cron: config.schedule,
    });
  }

  private toCsv(events: ActivityEvent[]): string {
    const headers = 'Timestamp,Actor,Action,Target Type,Target ID,Severity,Source\n';
    const rows = events.map(e =>
      `${e.timestamp.toISOString()},${e.actor.email || e.actor.id},${e.action},${e.target.type},${e.target.id},${e.severity},${e.context.source}`
    ).join('\n');
    return headers + rows;
  }
}
```

## Compliance Report

```typescript
async function generateComplianceReport(tenantId: string, period: { start: Date; end: Date }, framework: string): Promise<Report> {
  const adminActions = await adminAuditService.getAdminAuditTrail(tenantId, {
    startDate: period.start,
    endDate: period.end,
    limit: 10000,
  });

  const summary = {
    totalAdminActions: adminActions.data.length,
    criticalActions: adminActions.data.filter(a => a.severity === 'critical').length,
    uniqueAdmins: new Set(adminActions.data.map(a => a.actor.id)).size,
    mostCommonActions: groupBy(adminActions.data, 'action'),
    userManagementActions: adminActions.data.filter(a => a.action.startsWith('user.')).length,
    roleChanges: adminActions.data.filter(a => a.action.startsWith('role.')).length,
    permissionChanges: adminActions.data.filter(a => a.action.startsWith('permission.')).length,
  };

  return {
    title: `${framework.toUpperCase()} Compliance Report`,
    tenantId,
    period,
    generatedAt: new Date(),
    framework,
    summary,
    details: adminActions.data,
    format: 'pdf',
  };
}
```

## Open-Source Tools

- **PDFKit** (MIT) — PDF generation for reports
- **json2csv** (MIT) — JSON to CSV conversion
- **BullMQ** (MIT) — Scheduled report generation

## Production Considerations

- Max export: 10,000 records per export
- Export links expire after 24 hours
- All exports are audited (who exported, when, what filter)
- Scheduled reports deliver via email or webhook
- Support CSV, JSON, and PDF formats
- Include metadata header in CSV (time range, filters applied)
- Rate-limit exports: max 5 per hour per user
- Compress large exports (gzip) before storage
