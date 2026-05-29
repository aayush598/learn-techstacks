# Section 06: Overage & Throttling Policies

Overage policies define what happens when a tenant exceeds their plan limits. The system supports multiple enforcement strategies: hard throttle (block new usage until reset), soft throttle (allow overage but charge premium rates), degradation (reduce quality but keep serving), and warning-only (monitor and notify but don't block). The policy is configurable per tier and per resource.

Overage billing uses a separate rate card (higher unit prices than in-plan rates). Tenants can enable or disable overage in their billing settings. Disabling overage means hard throttling at the limit. Enabling overage allows continued usage at premium rates. Monthly overage caps protect tenants from unlimited charges.

Throttling responses include: HTTP 429 (for API rate limits), busy signals (for concurrent call limits), call termination (for duration limits), and degraded quality (lower bitrate audio for media limits). Each response includes the specific limit that was hit and when it resets.
