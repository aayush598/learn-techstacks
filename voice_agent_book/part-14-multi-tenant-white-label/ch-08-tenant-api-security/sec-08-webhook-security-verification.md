# Section 08: Webhook Security Verification

Webhook security ensures that HTTP callbacks sent to tenant-configured endpoints are authenticated and verified. Without verification, attackers could spoof webhook events and inject false data. The platform signs every webhook payload and provides verification methods for tenants to validate authenticity.

Webhook signing uses HMAC-SHA256 with a per-tenant secret. The signature is included in the X-Signature-256 header as a hex-encoded HMAC of the request body. Tenants verify the signature using their secret (shared during webhook configuration). Optional: the platform also sends a X-Timestamp header for replay attack prevention.

Webhook delivery includes: retry with exponential backoff (3 attempts, then dead letter), payload idempotency key (X-Idempotency-Key header for deduplication), and delivery logging. Tenants can view webhook delivery logs in the dashboard with request/response inspection for debugging.
