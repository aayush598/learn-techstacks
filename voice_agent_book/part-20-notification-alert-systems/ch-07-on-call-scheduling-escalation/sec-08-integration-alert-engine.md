# Section 08: Integration with Alert Engine

## Overview

The on-call system integrates with the alert engine to route incoming alerts to the appropriate on-call engineer. Alerts are dynamically assigned based on the current rotation, escalation policies are triggered on no-acknowledgment, and incident context is enriched with team and shift information. War rooms can be automatically created for critical incidents.

## Architecture

```
Alert → On-Call Routing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Alert Engine] → [On-Call Router] → [Assignment Decision] → [Notification]
      │                  │                     │                  │
  Alert fired       Resolve current        Direct assign      Notify on-call
  (critical/        on-call rotation         to primary        via preferred
   major/etc.)       + escalation            or escalate        channel
                     + schedule              to secondary
                     overrides               or next tier
                           │
                    [Enrichment Context]
                    - Shift details
                    - Team info
                    - Previous incidents
                    - Runbook links

Routing Flow:
  1. Alert received with severity and metadata
  2. Resolve current primary on-call engineer
  3. Check for schedule overrides or blackout
  4. Assign alert to on-call engineer
  5. If not acknowledged within SLA:
     a. Escalate to secondary
     b. Escalate to next tier
     c. Escalate to engineering manager
  6. Create war room for critical alerts
```

## Integration Points

- **Alert Engine**: Alert creation and lifecycle management
- **Incident Management**: War room creation for critical incidents
- **Notification System**: Multi-channel notification to on-call engineer
- **Status Page**: Incident status updates

## Production Considerations

- **Assignment Latency**: Alert to assignment < 100ms
- **Overlap Handling**: Concurrent shifts handled by round-robin
- **Failover**: Secondary notification path if primary on-call unreachable
- **Audit Trail**: All assignment decisions logged for compliance

## Open-Source Tools

- **BullMQ**: Alert assignment job queue
- **Novu**: Multi-channel notification to on-call engineer
