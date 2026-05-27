# Section 04: Tier-Based Rate Limiting

Rate limiting per tier ensures fair resource allocation across tenants of different plan levels. Higher tiers get higher rate limits (more API calls per second, more concurrent calls), while lower tiers are more restricted. Rate limits are applied per-tenant at the API gateway and enforced using sliding window counters in Redis.

Rate limit configuration per tier: API calls (requests/second, burst capacity), concurrent calls (max simultaneous voice sessions), call duration (max minutes per call), daily call volume (max calls per day), and AI processing (max STT/TTS seconds per hour). Exceeding limits returns 429 Too Many Requests with Retry-After headers.

The rate limiter uses a multi-tier architecture: global rate limits (all tenants combined, prevents platform overload), per-tier aggregate limits, per-tenant individual limits, and per-endpoint fine-grained limits. This protects the platform while providing predictable performance for each tenant.
