# Section 05: Usage Alerting & Notifications

Usage alerts notify tenants when they approach or exceed their plan limits. Alerts prevent bill shock and help tenants manage consumption proactively. The alerting system supports multiple thresholds: warning (80% of limit), critical (95%), exceeded (100%), and projected (AI-predicted overage based on current burn rate).

Alert delivery channels include: email (daily digest or immediate), in-app notification (toast in dashboard), webhook (POST to tenant's webhook URL), SMS (for critical billing alerts). Tenants configure their notification preferences per resource type and threshold level.

For a voice agent platform, alerts also cover unusual usage patterns (spike detection), cost anomalies (unexpected increase in AI model usage), and approaching billing thresholds (next tier would be more cost-effective). The alert system uses rule evaluation every 5 minutes against current usage data.
