# Section 06: Data Retention Policies

Data retention policies define how long different categories of data are kept before automatic deletion. Retention periods are based on legal requirements, business needs, and data minimization principles (GDPR Article 5). The retention system automatically enforces these policies, deleting or anonymizing data when retention expires.

Retention schedule: call recordings (90 days default, configurable up to 7 years for compliance), call logs (1 year), transcripts (1 year), analytics aggregates (3 years), billing records (7 years for tax compliance), audit logs (3 years, 7 years for security events), user accounts (until deletion request or 2 years of inactivity), and email notifications (30 days).

Retirement enforcement: a scheduled job runs daily, querying data by age, deleting expired records according to policy, and logging deletion actions. Recordings have a grace period (30 days after expiry) during which they are hidden but recoverable on request. After grace, deletion is irreversible. Exclusion: data under legal hold is preserved regardless of retention policy.
