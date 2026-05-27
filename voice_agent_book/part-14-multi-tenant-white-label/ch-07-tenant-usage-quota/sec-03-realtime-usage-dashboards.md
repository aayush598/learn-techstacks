# Section 03: Real-Time Usage Dashboards

Real-time usage dashboards give tenants visibility into their current consumption across all metered resources. The dashboard shows: usage vs limits (progress bars for each resource type), current billing period consumption, projected end-of-period usage (based on burn rate), recent spikes, and cost breakdown by agent or department.

The dashboard fetches data from the time-series database using aggregated queries. Auto-refresh (every 30 seconds) provides near-real-time visibility. Historical comparison (today vs yesterday, this month vs last month) helps tenants understand usage patterns.

For a voice agent platform, the dashboard also shows active call slots (current concurrent calls), call quality metrics (average latency, error rate), and AI model usage (STT seconds, TTS characters, LLM tokens). This helps tenants optimize their usage and plan upgrades.
