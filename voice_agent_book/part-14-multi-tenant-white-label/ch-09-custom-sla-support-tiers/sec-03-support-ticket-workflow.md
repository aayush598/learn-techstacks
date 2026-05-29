# Section 03: Support Ticket Workflow

The support ticket workflow manages tenant support requests from submission through resolution. Each ticket is tagged with the tenant's SLA tier, which determines priority and response time commitments. The workflow integrates with the tenant's white-label support portal and the internal agent desk.

Ticket lifecycle: submission (dashboard form, email, API, widget) → triage (auto-categorization by AI, priority assignment based on SLA) → assignment (round-robin for standard, named engineer for enterprise) → investigation (linked to tenant context, logs, metrics) → resolution (fix, workaround, or escalation) → verification (tenant confirms) → closure (survey, knowledge base article).

The ticketing system supports SLA timers: first response time, update frequency (every 24 hours minimum), and resolution deadline. Breached SLAs trigger escalation to next tier and automatic credit calculation. All ticket interactions are logged and available in the tenant's support portal.
