# Section 02: Control Mapping & Evidence Collection

Control mapping links each SOC 2 requirement to specific platform controls and automated evidence collection. Instead of manual evidence gathering during audit, the platform continuously collects evidence of control operation. The evidence collection is automated and tamper-proof, providing auditors with on-demand access to control evidence.

Control examples: logical access (control: MFA required for all admin accounts, evidence: MFA configuration snapshot from access management system), change management (control: all production changes require approved ticket, evidence: CI/CD pipeline logs with ticket references), data encryption (control: AES-256 at rest, evidence: encryption config scanning report), and availability (control: 99.9% uptime SLA, evidence: uptime monitoring data from synthetic probes).

Evidence collection pipeline: control definition → automated collector (agent or API integration) → evidence aggregation → timestamped storage → control operation report. Collectors run on schedules (daily for config checks, continuous for access logs). Evidence is stored immutably with hash-chain verification. The evidence management system provides auditors with read-only access to control operation data.
