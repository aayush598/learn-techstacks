# Section 06: Tenant Health Scoring

Tenant health scoring combines multiple signals into a single numeric score that indicates the tenant's overall well-being. The score is used for proactive support—reaching out to tenants before they churn or experience issues. Health scores are calculated daily and tracked over time to identify trends.

Health score components: usage health (call success rate, error rate, latency—35%), support health (open tickets, response satisfaction, escalation frequency—25%), billing health (payment success rate, invoice aging—15%), engagement health (login frequency, feature adoption, API usage trends—15%), and sentiment health (survey responses, NPS scores—10%).

Each component is scored 0-100 and weighted. The composite score is used to trigger actions: score 80+ (green—healthy, no action), 50-80 (yellow—monitor, send check-in), below 50 (red—proactive outreach required). Enterprise tenants have dedicated account managers who review health scores weekly.
