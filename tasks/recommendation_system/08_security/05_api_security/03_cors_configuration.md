# CORS Configuration

## 1. Overview

Cross-Origin Resource Sharing (CORS) controls which external origins can access
recommendation system APIs from web browsers. Misconfigured CORS is a common security
vulnerability that can allow unauthorized access to user data. This document covers origin
whitelisting, preflight requests, credentials handling, client-specific CORS, and common
CORS mistakes.

### 1.1 CORS in Recommendation Systems

| Client Type | CORS Needed | Configuration |
|---|---|---|
| Web application (same origin) | No | Same-origin by default |
| Web application (different origin) | Yes | Whitelist specific origins |
| Mobile application | No | Not affected by CORS |
| Server-to-server | No | Not affected by CORS |
| Browser extension | Yes | Whitelist extension origin |

---

## 2. Origin Whitelisting

### 2.1 Origin Policy

```
Allowed Origins:
├── https://app.rec.example.com        (main web app)
├── https://admin.rec.example.com      (admin dashboard)
├── https://partner.example.com        (partner portal)
├── http://localhost:3000              (development)
└── https://staging.rec.example.com    (staging environment)
```

### 2.2 CORS Headers

| Header | Value | Purpose |
|---|---|---|
| `Access-Control-Allow-Origin` | Specific origin or `*` | Allowed origins |
| `Access-Control-Allow-Methods` | `GET, POST, PUT, DELETE` | Allowed HTTP methods |
| `Access-Control-Allow-Headers` | `Content-Type, Authorization` | Allowed request headers |
| `Access-Control-Allow-Credentials` | `true` | Allow cookies/auth headers |
| `Access-Control-Max-Age` | `86400` | Preflight cache duration |
| `Access-Control-Expose-Headers` | `X-RateLimit-Limit` | Headers exposed to JS |

### 2.3 Dynamic Origin Validation

For multiple allowed origins, validate dynamically:

```
Request Origin → Check against allowlist → Set Access-Control-Allow-Origin header
       ↓                    ↓                           ↓
  Origin header       Match found?              Set specific origin
  from request        Yes → allow               (never use * with credentials)
                      No → reject
```

### 2.4 Origin Validation Rules

| Rule | Implementation | Security |
|---|---|---|
| Exact match | Compare full origin string | High |
| Subdomain match | Validate parent domain | Moderate (caution) |
| Protocol match | Require HTTPS | High |
| Port match | Include port in validation | High |
| Regex match | Avoid if possible | Lower (regex bypass risk) |

---

## 3. Preflight Requests

### 3.1 Preflight Flow

```
Browser                    Server
  │                          │
  │── OPTIONS /api/recs ────>│  (Preflight request)
  │   Origin: https://app.example.com
  │   Access-Control-Request-Method: POST
  │   Access-Control-Request-Headers: Content-Type, Authorization
  │                          │
  │<── 204 No Content ──────│  (Preflight response)
  │   Access-Control-Allow-Origin: https://app.example.com
  │   Access-Control-Allow-Methods: GET, POST
  │   Access-Control-Allow-Headers: Content-Type, Authorization
  │   Access-Control-Max-Age: 86400
  │                          │
  │── POST /api/recs ──────>│  (Actual request)
  │<── 200 OK ──────────────│
```

### 3.2 When Preflight Occurs

| Request Type | Preflight Required | Reason |
|---|---|---|
| GET with standard headers | No | Simple request |
| POST with Content-Type: application/json | Yes | Non-simple content type |
| POST with Authorization header | Yes | Non-simple header |
| PUT/DELETE/PATCH | Yes | Non-simple method |
| Any request with custom headers | Yes | Non-simple header |

### 3.3 Preflight Caching

- **Max-Age header**: Cache preflight response for specified seconds
- **Cache invalidation**: Clear cache when CORS policy changes
- **Cache key**: Origin + Method + Headers combination
- **Recommended cache time**: 24 hours (86400 seconds)

---

## 4. Credentials Handling

### 4.1 Credentials Mode

| Mode | Header | Cookie Behavior | Auth Header Behavior |
|---|---|---|---|
| `same-origin` | Not sent | Sent for same origin | Sent for same origin |
| `include` | `Access-Control-Allow-Credentials: true` | Sent for all origins | Sent for all origins |
| `omit` | Not sent | Never sent | Never sent |

### 4.2 Credentials Security

| Rule | Rationale |
|---|---|
| Never use `Access-Control-Allow-Origin: *` with credentials | Security vulnerability |
| Always specify exact origin with credentials | Prevents origin spoofing |
| Validate credentials on every request | Prevent session hijacking |
| Use SameSite cookies | Prevent CSRF attacks |
| Require HTTPS for credentialed requests | Prevent credential interception |

### 4.3 Credentials Configuration

```
# Correct configuration
Access-Control-Allow-Origin: https://app.rec.example.com
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST
Access-Control-Allow-Headers: Content-Type, Authorization

# WRONG (never do this)
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
```

---

## 5. CORS for Different Clients

### 5.1 Web Application CORS

| Endpoint | Allowed Origin | Methods | Credentials |
|---|---|---|---|
| `/v1/recommendations` | `https://app.rec.example.com` | GET, POST | Yes |
| `/v1/items` | `https://app.rec.example.com` | GET | Yes |
| `/v1/interactions` | `https://app.rec.example.com` | POST | Yes |
| `/admin/models` | `https://admin.rec.example.com` | GET, POST, PUT | Yes |
| `/v1/health` | `*` | GET | No |

### 5.2 Mobile Application CORS

Mobile applications are not affected by CORS (browsers enforce CORS, not native apps).
However:

- Use API key authentication for mobile
- Validate API key origin in server-side middleware
- Rate limit per API key
- No CORS headers needed for mobile-only endpoints

### 5.3 API-to-API CORS

Server-to-server communication is not affected by CORS. Use:

- mTLS for service identity
- API keys for authentication
- Network policies for access control
- Internal DNS for service discovery

---

## 6. Common CORS Mistakes

### 6.1 Critical Mistakes

| Mistake | Vulnerability | Fix |
|---|---|---|
| `Access-Control-Allow-Origin: *` with credentials | Any origin can steal data | Use specific origin |
| Reflecting origin without validation | Any origin can access | Validate against allowlist |
| Missing `Access-Control-Allow-Credentials` | Auth cookies not sent | Add header when needed |
| Overly permissive methods | Unintended write access | Limit to required methods |
| Overly permissive headers | Header injection | Limit to required headers |
| No CORS on sensitive endpoints | Direct browser access | Apply CORS to all endpoints |

### 6.2 CORS Testing

| Test | Method | Expected Result |
|---|---|---|
| Origin validation | Send request with different origins | Only whitelisted origins allowed |
| Method restriction | Send disallowed methods | 405 Method Not Allowed |
| Header restriction | Send disallowed headers | Preflight rejected |
| Credentials | Send with credentials | Credentials properly handled |
| Preflight caching | Send duplicate preflight | Cached response returned |

### 6.3 CORS Monitoring

- **Log all CORS rejections**: Monitor for attack attempts
- **Track origin patterns**: Identify legitimate vs suspicious origins
- **Alert on unusual origins**: New origins accessing API
- **Audit CORS policy**: Quarterly review of allowed origins
- **Test after changes**: Verify CORS configuration after any change
