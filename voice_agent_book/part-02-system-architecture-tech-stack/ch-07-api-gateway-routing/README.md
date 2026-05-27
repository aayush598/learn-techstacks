# Chapter 07: API Gateway & Routing Strategy

> **Part:** 02 - System Architecture & Technology Stack

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [API Gateway Role & Responsibilities](sec-01-api-gateway-role-responsibilities.md) | Entry point for all external API traffic, routing, auth, rate limiting, transformation |
| 02 | [API Versioning Strategy](sec-02-api-versioning-strategy.md) | URL-based versioning (v1, v2), header-based negotiation, deprecation policy, sunset headers |
| 03 | [Rate Limiting & Throttling](sec-03-rate-limiting-throttling.md) | Per-key rate limits, tier-based limits (free/pro/enterprise), burst allowance, rate limit headers |
| 04 | [Authentication & Authorization](sec-04-authentication-authorization.md) | API key validation, OAuth 2.0 token validation, scope enforcement, tenant resolution |
| 05 | [Request/Response Transformation](sec-05-request-response-transformation.md) | Normalization, validation, pagination enforcer, response envelope, error formatting |
| 06 | [API Route Organization in Next.js](sec-06-api-route-organization-in-nextjs.md) | Route handler patterns, grouping by domain, shared middleware, error boundaries |
| 07 | [Documentation & Discovery](sec-07-documentation-discovery.md) | OpenAPI 3.1 spec generation, Scalar/Swagger UI, SDK generation, API changelog |
| 08 | [Compatibility & Breaking Changes](sec-08-compatibility-breaking-changes.md) | Backward compatibility, migration guides, sunset periods, feature flags for gradual rollout |

---

## API Rate Limits by Tier

| Tier | Rate Limit | Burst | Concurrent |
|------|-----------|-------|------------|
| Free | 10 req/min | 20 | 2 |
| Starter | 60 req/min | 100 | 5 |
| Pro | 300 req/min | 500 | 20 |
| Business | 1000 req/min | 2000 | 50 |
| Enterprise | Custom | Custom | Custom |

---

## Key Takeaways

- API Gateway as the single entry point for all external API traffic
- URL-based versioning (v1, v2) for clear upgrade path
- Rate limiting per API key with tier-based quotas
- OpenAPI 3.1 spec auto-generated from route definitions
- Standardized error format: `{ error: { code, message, details } }`
- Deprecation policy with minimum 6-month sunset period
