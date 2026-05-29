# Section 08: Usage API & Webhooks

The Usage API exposes programmatic access for tenants to query their current usage, retrieve historical consumption data, and configure alert thresholds. The API is RESTful with JSON responses, supporting the same authentication as the main platform API. Tenants can use this API to integrate usage data into their own dashboards or automation systems.

Key endpoints include: GET /usage/current (real-time usage summary), GET /usage/history (time-series data for charts), GET /usage/costs (cost breakdown by resource), POST /usage/alerts (configure alert rules), GET /usage/prepaid (prepaid credit balance), and GET /usage/limits (current plan limits and remaining allowances).

Usage webhooks notify tenants of important events: threshold reached, overage started, plan limit changed, prepaid credit low, and billing period reset. Webhooks include a usage snapshot payload. The webhook delivery uses retry logic with exponential backoff and dead-letter queues for failed deliveries.
