# Section 02: Quota Enforcement Middleware

Quota enforcement intercepts API requests and real-time events to check whether the tenant has remaining allowance for the requested resource. Enforcement happens at multiple layers: API gateway (for REST/gRPC calls), call router (for voice calls), and streaming pipeline (for real-time audio processing). Each layer checks the tenant's current usage against their plan's limits.

The middleware architecture uses a token bucket algorithm for burstable limits and a fixed window for hard caps. Soft limits trigger warnings; hard limits block the request. The middleware caches quota status in Redis for low-latency checks (sub-millisecond overhead) and falls back to the database if cache is unavailable.

For a voice agent platform, quota enforcement prevents resource exhaustion by one tenant from affecting others. It also provides clear error messages when limits are reached, including current usage, limit, reset time, and upgrade options.
