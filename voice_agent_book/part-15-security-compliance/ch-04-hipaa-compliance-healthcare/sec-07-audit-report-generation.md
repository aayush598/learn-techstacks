# Section 07: Audit Report Generation

Audit report generation creates compliance-ready reports summarizing security events over a specified period. Reports are used for SOC 2 evidence, HIPAA audits, GDPR compliance documentation, and internal security reviews. The report system automates what previously required manual evidence gathering.

Report types: user access report (who accessed what, when, success/failure), admin activity report (all admin actions across the platform), data access report (PII access, exports, deletions), authentication report (login attempts, MFA usage, SSO activity), configuration change report (tenant, agent, integration changes), and custom reports (ad-hoc query results formatted as PDF).

Report generation: user selects report type, time range, and filters → system queries audit store → formats results (tables, charts, summary statistics)→ generates PDF with cover page, table of contents, and data export (CSV for raw data). Reports are digitally signed to prove authenticity. Scheduled reports (monthly, quarterly) are automatically generated and sent to compliance teams.
