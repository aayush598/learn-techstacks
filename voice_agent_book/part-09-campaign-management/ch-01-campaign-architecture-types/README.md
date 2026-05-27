# Chapter 01: Campaign Architecture & Types

> **Part:** 09 - Campaign Management

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Campaign Types Overview](sec-01-campaign-types-overview.md) | Predictive, preview, progressive, broadcast — dialing mode comparison and architecture |
| 02 | [Campaign Lifecycle Management](sec-02-campaign-lifecycle-management.md) | Draft, active, paused, completed, archived — lifecycle state machine and transitions |
| 03 | [Sales Campaign Design](sec-03-sales-campaign-design.md) | Outbound sales campaign specifics — lead scoring integration, call list prioritization |
| 04 | [Survey & Feedback Campaigns](sec-04-survey-feedback-campaigns.md) | Survey campaign architecture — IVR-based surveys, sentiment collection, response aggregation |
| 05 | [Reminder & Notification Campaigns](sec-05-reminder-notification-campaigns.md) | Reminder campaign design — appointment reminders, payment reminders, event notifications |
| 06 | [Collection & Recovery Campaigns](sec-06-collection-recovery-campaigns.md) | Debt collection campaign design — compliance requirements, right-party contact, payment IVR |
| 07 | [Multi-Campaign Orchestration](sec-07-multi-campaign-orchestration.md) | Running multiple concurrent campaigns — resource allocation, priority queuing, conflict resolution |
| 08 | [Campaign Tenant Isolation](sec-08-campaign-tenant-isolation.md) | Multi-tenant campaign data isolation — partition strategies, access control, resource quotas |

---

## Key Takeaways

- Four primary dialing modes: predictive, preview, progressive, and broadcast
- Campaign lifecycle managed through a state machine with controlled transitions
- Each campaign type (sales, survey, reminder, collection) has distinct architecture requirements
- Multi-campaign orchestration requires careful resource allocation and priority management
- Tenant isolation is critical for multi-tenant SaaS deployments
