# Section 05: SLA Breach & Credit Management

SLA breach management detects when commitments are not met and automatically calculates credits. The system monitors all SLA metrics in real-time, and when a breach is detected, it logs the incident, calculates the credit amount, and initiates the credit workflow. This process must be transparent and auditable.

Breach detection evaluates: uptime below threshold (calculated monthly), response time exceeded (per-ticket measurement), resolution time exceeded (per-ticket measurement), and scheduled maintenance without notice. Each breach type has specific credit calculation: for uptime breaches, 5% of monthly fee per 0.1% below SLA; for response/resolution breaches, 10% of monthly fee per incident.

Credit workflow: breach detected → incident logged with evidence → credit calculated → tenant notified → credit applied (deducted from next invoice) or paid out (for prepaid tenants). Tenants can dispute breaches with evidence. The system provides a breach dashboard showing current and historical compliance.
