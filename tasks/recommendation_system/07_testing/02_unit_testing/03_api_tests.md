# API Testing

## 1. Overview

API testing is critical for recommendation systems because APIs are the primary interface
between clients and the recommendation engine. Every recommendation request, feature update,
and model management operation flows through APIs. This document covers request/response
validation, status code testing, error handling, rate limiting, authentication, and contract
testing for recommendation system APIs.

### 1.1 API Layers in Recommendation Systems

| Layer | Protocol | Purpose | Examples |
|---|---|---|---|
| Client-facing API | REST/gRPC | Serve recommendations to apps | `/v1/recommendations` |
| Internal service API | gRPC | Inter-service communication | Feature serving, model inference |
| Admin API | REST | System management | Model deployment, feature registration |
| Batch API | gRPC/REST | Bulk operations | Batch prediction, data export |
| Webhook API | REST | Event notifications | Model training completion, alerts |

### 1.2 API Testing Pyramid

```
                    ┌──────────┐
                    │  E2E     │ ← Full flow with real services
                   ┌┴──────────┴┐
                   │  Contract  │ ← Schema and consumer-driven
                  ┌┴────────────┴┐
                  │ Integration   │ ← Multi-service, real dependencies
                 ┌┴──────────────┴┐
                 │    Functional   │ ← Business logic validation
                ┌┴────────────────┴┐
                │   Parameterized   │ ← Data-driven, edge cases
                └──────────────────┘ ← Fast, isolated, many
```

---

## 2. Request/Response Validation

### 2.1 Request Schema Validation

Every API endpoint must validate incoming requests against a defined schema.

**Request validation dimensions:**

| Dimension | Description | Failure Response |
|---|---|---|
| Required fields | All mandatory fields present | 400 Bad Request |
| Field types | Each field matches expected type | 400 Bad Request |
| Value constraints | Values within defined ranges | 400 Bad Request |
| Nested objects | Sub-objects conform to schema | 400 Bad Request |
| Array contents | Array elements meet item schema | 400 Bad Request |
| Enum values | Categorical fields in allowed set | 400 Bad Request |

**Example validation for recommendation request:**

```json
{
  "user_id": "usr_a1b2c3d4e5f6",     // Required, string, pattern match
  "context": {
    "device": "mobile",               // Required, enum: [mobile, desktop, tablet]
    "timestamp": "2026-01-15T10:30:00Z", // Required, ISO 8601 datetime
    "location": {                      // Optional
      "latitude": 37.7749,             // Optional, float, range [-90, 90]
      "longitude": -122.4194           // Optional, float, range [-180, 180]
    }
  },
  "request_params": {
    "count": 20,                       // Required, integer, range [1, 100]
    "offset": 0,                       // Optional, integer, min 0
    "category_filter": ["electronics", "books"]  // Optional, array of strings
  }
}
```

### 2.2 Response Schema Validation

Response validation ensures the API returns correctly structured data.

**Response validation checklist:**

- All fields defined in OpenAPI spec are present
- Field types match specification exactly
- Nullable fields are either null or absent (per spec)
- Nested objects are complete and correctly typed
- Array lengths respect any defined constraints
- String fields have expected maximum lengths
- Numeric fields have expected precision

### 2.3 Response Content Validation

Beyond schema, validate the actual content of responses:

| Validation | Description | Example |
|---|---|---|
| Recommendation count | Returned count matches requested | `count: 20` returns 20 items |
| Item existence | All recommended items exist | Item IDs are valid |
| Deduplication | No duplicate recommendations | All item IDs unique |
| Relevance ordering | Items ordered by relevance score | Scores are descending |
| Score range | Relevance scores in valid range | 0.0 ≤ score ≤ 1.0 |
| Category diversity | Distribution matches policy | No single category > 50% |

### 2.4 Content-Type and Serialization

- Verify Content-Type header matches response body format
- Test JSON serialization handles special characters correctly
- Verify empty responses return valid empty structures (not null)
- Test response encoding with Unicode characters
- Validate date/time formats in responses

---

## 3. Status Code Tests

### 3.1 Success Status Codes

| Code | Meaning | When to Use |
|---|---|---|
| 200 OK | Successful retrieval | GET /recommendations |
| 201 Created | Resource created | POST /models (deploy new model) |
| 202 Accepted | Async operation accepted | POST /batch-predict |
| 204 No Content | Successful mutation, no body | DELETE /recommendations/cache |

### 3.2 Client Error Status Codes

| Code | Meaning | Test Scenario |
|---|---|---|
| 400 Bad Request | Invalid request syntax | Missing required fields, invalid types |
| 401 Unauthorized | Authentication failure | Missing or invalid auth token |
| 403 Forbidden | Authorization failure | Valid token, insufficient permissions |
| 404 Not Found | Resource doesn't exist | Non-existent user ID, model ID |
| 409 Conflict | Resource state conflict | Deploying model with duplicate name |
| 422 Unprocessable Entity | Valid syntax, invalid semantics | User ID format valid but user doesn't exist |
| 429 Too Many Requests | Rate limit exceeded | Exceeding QPS threshold |

### 3.3 Server Error Status Codes

| Code | Meaning | Test Scenario |
|---|---|---|
| 500 Internal Server Error | Unexpected server failure | Unhandled exception in handler |
| 502 Bad Gateway | Upstream service failure | Feature store unreachable |
| 503 Service Unavailable | Server overloaded or down | Maintenance mode, overload |
| 504 Gateway Timeout | Upstream timeout | Slow model inference |

### 3.4 Status Code Test Matrix

Test each endpoint against all applicable status code scenarios:

```
Endpoint: GET /v1/recommendations/{user_id}

Test Cases:
├── 200: Valid user_id, sufficient features
├── 400: Missing user_id parameter
├── 400: user_id with invalid format
├── 401: No Authorization header
├── 401: Expired JWT token
├── 403: Token valid but user not in allowed audience
├── 404: user_id not found in user database
├── 429: Exceeding rate limit (1000 QPS)
├── 502: Feature store service unavailable
├── 503: Model serving overloaded
└── 504: Feature store timeout (> 500ms)
```

---

## 4. Error Handling Tests

### 4.1 Error Response Structure

All error responses must follow a consistent structure:

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "No user found with the specified user_id",
    "details": {
      "user_id": "usr_unknown123",
      "suggestion": "Verify the user_id exists in the system"
    },
    "request_id": "req_abc123def456",
    "timestamp": "2026-01-15T10:30:00Z",
    "documentation_url": "https://docs.example.com/errors/USER_NOT_FOUND"
  }
}
```

### 4.2 Error Handling Test Categories

#### 4.2.1 Input Validation Errors

- Missing required fields return 400 with specific field identification
- Invalid field types return 400 with type mismatch details
- Out-of-range values return 400 with expected range information
- Invalid enum values return 400 with allowed value list
- Malformed JSON returns 400 with parse error details

#### 4.2.2 Business Logic Errors

- Non-existent entities return 404 with entity identification
- State conflicts return 409 with current state description
- Permission denied returns 403 with required permission information
- Quota exceeded returns 429 with retry-after and quota details

#### 4.2.3 Infrastructure Errors

- Database unavailable returns 503 with estimated recovery time
- Feature store timeout returns 504 with partial results if available
- Model serving failure returns 502 with fallback model information
- Cache miss returns 200 with degraded but acceptable results

### 4.3 Graceful Degradation Testing

Recommendation systems must degrade gracefully rather than fail completely:

| Failure Scenario | Expected Behavior | Fallback Strategy |
|---|---|---|
| Feature store timeout | Return cached features or defaults | Use most recent available features |
| Model serving failure | Return popularity-based recommendations | Use pre-computed popular items |
| Cache failure | Compute recommendations in real-time | Direct model inference |
| User profile unavailable | Return cold-start recommendations | Use context-only features |
| Category filter service down | Return unfiltered recommendations | Apply client-side filtering |

### 4.4 Error Recovery Tests

- API recovers gracefully after temporary dependency failure
- Error rates return to normal after dependency recovery
- Circuit breaker trips and resets correctly
- Retry-after headers are respected by clients
- Partial failures don't leave inconsistent state

---

## 5. Rate Limiting Tests

### 5.1 Rate Limiting Strategies

| Strategy | Description | Use Case |
|---|---|---|
| Fixed window | X requests per Y-second window | Simple API protection |
| Sliding window | Rolling window counter | Smoother rate limiting |
| Token bucket | Tokens consumed per request | Bursty traffic patterns |
| Leaky bucket | Fixed processing rate | Backpressure mechanism |
| Adaptive | Rate adjusts based on load | Dynamic capacity management |

### 5.2 Rate Limit Test Scenarios

**Under limit:**

- Send 99 requests within 100-request limit → all succeed
- Each response includes rate limit headers
- Remaining count decrements correctly
- Reset time is accurate

**At limit:**

- Send exactly 100 requests → last succeeds, remaining = 0
- Response headers indicate limit reached

**Over limit:**

- Send 101 requests → 101st returns 429
- Response includes Retry-After header
- After waiting Retry-After seconds, next request succeeds
- Rate limit resets at window boundary

**Rate limit headers:**

```
X-RateLimit-Limit: 1000          # Max requests per window
X-RateLimit-Remaining: 742       # Remaining requests in window
X-RateLimit-Reset: 1705312800    # Unix timestamp when window resets
X-RateLimit-Policy: 1000;w=60    # 1000 requests per 60-second window
Retry-After: 12                  # Seconds to wait (only on 429)
```

### 5.3 Multi-Tier Rate Limiting

Recommendation APIs typically have multiple rate limiting tiers:

| Tier | Limit | Window | Burst Allowance |
|---|---|---|---|
| Anonymous | 100 req/min | Sliding | No burst |
| Authenticated | 1,000 req/min | Sliding | 2x burst |
| Premium | 10,000 req/min | Sliding | 5x burst |
| Internal service | 100,000 req/min | Sliding | 10x burst |
| Batch operations | 10 req/min | Fixed | No burst |

### 5.4 Rate Limiting Edge Cases

- **Clock skew**: Rate limit windows handle clock differences between servers
- **Distributed rate limiting**: Redis-backed counters with consistency guarantees
- **Concurrent requests**: Race conditions in counter updates
- **Header injection**: Rate limit headers not manipulable by clients
- **IP spoofing**: Rate limits apply per authenticated user, not just IP
- **Grace period**: Brief grace period after window reset to prevent thundering herd

---

## 6. Authentication Tests

### 6.1 Authentication Method Tests

| Method | Test Focus | Example |
|---|---|---|
| JWT Bearer token | Token validity, expiry, claims | Bearer eyJhbGci... |
| API Key | Key existence, validity, scope | X-API-Key: sk_live_... |
| OAuth 2.0 | Authorization code, refresh token | Authorization: Bearer ... |
| mTLS | Certificate validity, CA chain | Client certificate verification |
| HMAC signature | Signature computation, timestamp freshness | X-Signature: sha256=... |

### 6.2 Authentication Failure Scenarios

- Missing authentication credentials → 401 with WWW-Authenticate header
- Expired token → 401 with token expiry information
- Invalid token format → 401 with generic error (no token structure leakage)
- Revoked token → 401 with revocation information
- Token from wrong issuer → 401 with issuer validation failure
- Insufficient token scope → 403 with required scope information

### 6.3 Token Validation Tests

- **Signature verification**: Valid signatures pass, tampered signatures fail
- **Expiry check**: Expired tokens rejected, near-expiry tokens accepted
- **Audience validation**: Tokens for wrong audience rejected
- **Issuer validation**: Tokens from wrong issuer rejected
- **Claim validation**: Custom claims meet business requirements
- **Refresh token flow**: Expired access tokens refresh successfully

---

## 7. Contract Tests

### 7.1 API Contract Definition

API contracts define the expected behavior between service providers and consumers.

**Contract elements:**

- **Endpoint definitions**: URL patterns, HTTP methods, parameters
- **Request schemas**: Complete request body specifications
- **Response schemas**: Complete response body specifications including errors
- **Status codes**: All possible status codes and when they occur
- **Headers**: Required request and response headers
- **Examples**: Concrete request/response examples for each endpoint

### 7.2 Consumer-Driven Contract Testing

Each service consumer defines their expectations as a contract:

```
Consumer: Mobile App
Provider: Recommendation API

Contract:
1. GET /v1/recommendations/{user_id}
   - Requires: user_id path parameter
   - Requires: Authorization header with valid JWT
   - Expects: 200 with recommendations array
   - Expects: recommendations array length <= requested count
   - Expects: each recommendation has item_id and score
   - Accepts: 401 for auth failures
   - Accepts: 404 for unknown users
   - Accepts: 429 for rate limits
```

### 7.3 Contract Testing Tools and Approaches

| Approach | Description | Tool Examples |
|---|---|---|
| Pact | Consumer-driven contract testing | Pact, Pactflow |
| Schema validation | Response schema against OpenAPI spec | Dredd, Schemathesis |
| Snapshot testing | Record and compare API responses | Bidbid, vcrpy |
| Spec generation | Generate tests from OpenAPI spec | openapi-generator |

### 7.4 Contract Evolution Management

When changing API contracts:

1. **Additive changes**: New fields, new endpoints → backward-compatible
2. **Deprecation period**: Mark old fields as deprecated, maintain for N versions
3. **Version negotiation**: Client and server agree on API version
4. **Feature flags**: New behavior gated behind feature flags
5. **Shadow traffic**: Test new responses alongside old before switching

### 7.5 Contract Testing in CI/CD

```
PR Created → Consumer Tests → Provider Tests → Contract Verification → Deploy
              (expectations)    (compliance)     (compatibility check)
```

- Consumer tests run on consumer service changes
- Provider tests run on provider service changes
- Contract verification runs on both to catch incompatibilities
- Deployment blocked if contract verification fails
