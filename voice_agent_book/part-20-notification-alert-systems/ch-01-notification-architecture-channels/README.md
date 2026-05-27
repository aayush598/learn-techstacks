# Chapter 01: Notification Architecture & Channels

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Notification Bus Architecture](sec-01-notification-bus-architecture.md) | Event-driven notification bus, pub/sub model, channel abstraction, message brokering |
| 02 | [Channel Abstraction Layer](sec-02-channel-abstraction-layer.md) | Channel interface design, provider adapter pattern, channel registry, fallback chains |
| 03 | [Delivery Guarantees](sec-03-delivery-guarantees.md) | At-least-once delivery, exactly-once semantics, delivery receipts, retry queues |
| 04 | [Template System](sec-04-template-system.md) | Notification templates, dynamic variable rendering, multi-channel template variants, template versioning |
| 05 | [Preference Management](sec-05-preference-management.md) | User notification preferences, channel opt-in/out, frequency controls, quiet hours |
| 06 | [Message Queue Integration](sec-06-message-queue-integration.md) | BullMQ queue setup, job prioritization, delayed delivery, batch processing |
| 07 | [Notification Logging & Audit Trail](sec-07-notification-logging-audit.md) | Delivery logs, status tracking, audit trail, delivery analytics |
| 08 | [Multi-Tenant Isolation](sec-08-multi-tenant-isolation.md) | Per-tenant channel config, tenant-level preferences, tenant delivery quotas, billing integration |
