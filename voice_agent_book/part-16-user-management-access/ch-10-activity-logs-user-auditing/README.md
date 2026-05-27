# Chapter 10: Activity Logs & User Auditing

> **Part:** 16 - User Management & Access Control

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Activity Log Data Model](sec-01-activity-log-data-model.md) | Event schema, actor/action/target pattern, metadata fields, correlation IDs |
| 02 | [Event Capture Architecture](sec-02-event-capture-architecture.md) | Instrumentation layer, automatic event capture, manual event logging, async event processing |
| 03 | [User Activity Timeline](sec-03-user-activity-timeline.md) | Per-user activity feed, chronological view, activity grouping, search and filtering |
| 04 | [Admin Audit Trail](sec-04-admin-audit-trail.md) | Admin action logging, configuration changes, permission modifications, sensitive data access |
| 05 | [Log Search & Filtering](sec-05-log-search-filtering.md) | Full-text search, structured query filters, date range filtering, Elasticsearch integration |
| 06 | [Export & Reporting](sec-06-export-reporting.md) | CSV/JSON export, scheduled report delivery, compliance report generation, API access to logs |
| 07 | [Retention & Archival](sec-07-retention-archival.md) | Retention policy configuration, hot/warm/cold storage tiers, S3 Glacier archival, deletion scheduling |
| 08 | [Real-Time Monitoring](sec-08-real-time-monitoring.md) | Streaming activity feed, anomaly detection, suspicious activity alerts, webhook notifications |

---

## Activity Event Model

```json
{
  "id": "act_evt_001",
  "timestamp": "2025-06-01T10:30:00Z",
  "actor": {
    "id": "user_abc",
    "type": "user",
    "email": "admin@company.com",
    "ip": "203.0.113.1"
  },
  "action": "campaign.created",
  "target": {
    "id": "camp_xyz",
    "type": "campaign",
    "name": "Q3 Outreach"
  },
  "changes": { "before": null, "after": { "status": "draft", "name": "Q3 Outreach" } },
  "context": {
    "tenant_id": "tenant_123",
    "session_id": "sess_456",
    "user_agent": "Mozilla/5.0..."
  }
}
```

---

## Learning Objectives

- Design activity log data model with actor/action/target
- Build event capture architecture with automatic instrumentation
- Create user activity timeline with search and filtering
- Implement admin audit trail for sensitive actions
- Build log search with Elasticsearch integration
- Create export and reporting for compliance
- Design retention and archival with tiered storage
- Implement real-time activity monitoring and alerting
