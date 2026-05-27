# Chapter 09: Data Flow & State Management

> **Part:** 02 - System Architecture & Technology Stack

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Event-Driven Data Flow](sec-01-event-driven-data-flow.md) | Events as first-class citizens, event catalog, producer/consumer patterns, event versioning |
| 02 | [Call Lifecycle State Machine](sec-02-call-lifecycle-state-machine.md) | States: Queued → Ringing → Connected → InProgress → Paused → Transferred → Completed/Failed |
| 03 | [CQRS (Command Query Responsibility Segregation)](sec-03-cqrs-command-query-responsibility.md) | Write path (commands) vs read path (queries), materialized views, eventual consistency |
| 04 | [Event Sourcing for Audit](sec-04-event-sourcing-for-audit.md) | Event store append-only log, event replay, snapshots, audit trail |
| 05 | [Real-Time Data Pipeline](sec-05-real-time-data-pipeline.md) | Event → Kafka → Stream Processor → Materialized View → WebSocket → Dashboard |
| 06 | [Data Consistency Patterns](sec-06-data-consistency-patterns.md) | Saga pattern for distributed transactions, outbox pattern, idempotency keys |
| 07 | [State Recovery & Resilience](sec-07-state-recovery-resilience.md) | Crash recovery, replay, dead letter queues, state reconciliation, idempotency |

---

## Call State Machine

```
Queued → Ringing → Connected → InProgress → [Paused/Resumed] → Completed
                  ↓              ↓                                 ↓
              No Answer      Transfer → Transferred            Failed
                  ↓              ↓
              Voicemail     Escalated → HumanHandoff
```

---

## Key Takeaways

- Event-driven architecture with Kafka as event backbone
- Call lifecycle managed by a state machine for auditability
- CQRS: Separate write-optimized (commands) and read-optimized (queries) paths
- Event sourcing with append-only log for complete audit trail
- Outbox pattern ensures reliable event publishing with database transactions
- Saga pattern for multi-service operations (e.g., billing + usage + notifications)
