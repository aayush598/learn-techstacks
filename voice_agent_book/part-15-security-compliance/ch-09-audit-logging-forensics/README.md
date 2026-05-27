# Chapter 09: Audit Logging & Forensics

> **Part:** 15 - Security, Compliance & Governance

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Audit Log Schema Design](sec-01-audit-log-schema.md) | Event schema, mandatory fields, actor/target/action model, correlation IDs |
| 02 | [Log Ingestion Pipeline](sec-02-log-ingestion-pipeline.md) | Log shipping, buffer queue, batch processing, schema validation, enrichment |
| 03 | [Immutable Log Storage](sec-03-immutable-log-storage.md) | Append-only database, write-once-read-many storage, cryptographic chaining, tamper detection |
| 04 | [Forensic Query Patterns](sec-04-forensic-query-patterns.md) | Timeline reconstruction, user activity trail, privilege escalation detection, anomaly queries |
| 05 | [Alerting on Audit Events](sec-05-alerting-on-audit-events.md) | Suspicious activity rules, real-time alert pipeline, severity classification, notification routing |
| 06 | [Log Retention Policies](sec-06-log-retention-policies.md) | Retention tiers (hot/warm/cold), compliance-driven retention, archival to S3 Glacier, deletion scheduling |
| 07 | [Audit Log Integrity](sec-07-audit-log-integrity.md) | Digital signatures for log entries, hash chain verification, periodic integrity audits, tamper response |
| 08 | [Compliance Reporting](sec-08-compliance-reporting.md) | SOC 2 audit report generation, GDPR processing records, HIPAA access reports, customizable report templates |

---

## Audit Log Schema

```json
{
  "id": "evt_abc123",
  "timestamp": "2025-06-01T10:00:00Z",
  "actor": { "type": "user", "id": "user_xxx", "email": "admin@example.com" },
  "action": "call.transcript.exported",
  "target": { "type": "transcript", "id": "trans_yyy" },
  "context": {
    "tenant_id": "tenant_zzz",
    "ip_address": "203.0.113.1",
    "user_agent": "Mozilla/5.0...",
    "session_id": "sess_aaa"
  },
  "changes": { "before": null, "after": { "format": "pdf" } },
  "metadata": { "correlation_id": "corr_bbb", "request_id": "req_ccc" }
}
```

---

## Learning Objectives

- Design comprehensive audit log schema with actor/target/action model
- Build scalable log ingestion pipeline with validation
- Implement immutable log storage with tamper detection
- Create forensic query patterns for investigation
- Build real-time alerting on suspicious audit events
- Design log retention policies for compliance requirements
- Ensure audit log integrity with cryptographic chaining
- Generate compliance reports from audit data
