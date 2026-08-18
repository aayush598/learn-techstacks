# API Gateway Patterns for Recommendation Systems

## 1. API Gateway Role and Responsibilities

### 1.1 Single Entry Point
The API Gateway serves as the single entry point for all recommendation API consumers. It decouples internal service architecture from external API contracts.

**Core Responsibilities**:
- **Request Routing**: Map external API paths to internal service endpoints
- **Protocol Translation**: Convert REST/GraphQL to internal gRPC calls
- **Authentication**: Validate JWT tokens, API keys, OAuth2 tokens
- **Authorization**: Enforce access control policies per endpoint
- **Rate Limiting**: Protect services from overload with per-user and global limits
- **Request Validation**: Validate request payloads against schemas
- **Response Caching**: Cache recommendation results to reduce model inference load
- **Response Transformation**: Modify response payloads for different clients
- **Circuit Breaking**: Detect failing services and provide fallback responses
- **Request Aggregation**: Combine responses from multiple services into single response
- **API Versioning**: Route requests based on API version headers
- **Logging and Analytics**: Track all API requests for monitoring and analytics

---

## 2. Rate Limiting Strategies

### 2.1 Algorithms

**Token Bucket**:
- Tokens added at fixed rate up to bucket capacity
- Each request consumes one token
- If bucket empty, request rejected
- Allows bursts up to bucket capacity
- Good for: General API rate limiting

**Sliding Window Log**:
- Track timestamps of all requests in current window
- Count requests in sliding window
- Reject if count exceeds limit
- Precise but memory-intensive
- Good for: Accurate rate limiting with small windows

**Sliding Window Counter**:
- Weighted combination of current and previous window counts
- Memory efficient with good accuracy
- Good for: Production rate limiting at scale

**Leaky Bucket**:
- Requests queued in FIFO bucket
- Processed at fixed rate
- Reject when bucket full
- Smooths out traffic bursts
- Good for: Downstream service protection

### 2.2 Rate Limiting Dimensions for Recommendations
- **Per User**: Limit requests per user per time window (e.g., 100 requests/minute)
- **Per API Key**: Limit requests per API key for third-party integrations
- **Per Endpoint**: Different limits for different endpoints (home vs similar)
- **Per IP**: Prevent abuse from single IP addresses
- **Global**: Total system throughput limit
- **Model Inference**: Limit model inference calls to protect GPU resources

### 2.3 Rate Limit Response
When rate limit exceeded:
- Return HTTP 429 Too Many Requests
- Include Retry-After header with seconds until next request allowed
- Include X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset headers
- Provide cached/default recommendations as fallback

---

## 3. Authentication and Authorization

### 3.1 JWT Token Design
```
Header:
  - algorithm: RS256
  - key_id: signing-key-id

Payload:
  - sub: user_id
  - iss: auth-service
  - aud: recommendation-api
  - exp: expiration_timestamp
  - iat: issued_at_timestamp
  - scope: ["read:recommendations", "write:interactions"]
  - tenant_id: organization_id (for multi-tenant systems)
  - experiment_assignments: {experiment_id: variant_id}
```

### 3.2 OAuth2 Flows for Different Clients
- **Authorization Code Flow**: For web applications with user login
- **Client Credentials Flow**: For server-to-server API calls
- **PKCE Flow**: For mobile applications and SPAs
- **Device Code Flow**: For smart TV and device-based clients

### 3.3 API Key Authentication
- For third-party integrations and batch access
- API key passed in X-API-Key header
- Rate limits applied per API key
- API keys rotated regularly with grace period for old keys

### 3.4 Authorization Policies
- **Endpoint-based**: Different endpoints require different permissions
- **Resource-based**: Users can only access their own recommendations
- **Tenant-based**: Multi-tenant isolation (enterprise recommendations)
- **Role-based**: Admin, ML engineer, API consumer roles

---

## 4. Response Caching

### 4.1 Cache Strategy
- **Cache Key**: hash(user_id + endpoint + context + filters)
- **Cache TTL**: Based on data freshness requirements
  - Home recommendations: 5-15 minutes
  - Similar items: 1-24 hours (items change slowly)
  - Trending: 5-30 minutes
  - Search results: 1-5 minutes

### 4.2 Cache Invalidation
- **TTL-based**: Automatic expiration after configured duration
- **Event-driven**: Invalidate cache when underlying data changes (new interaction, model update)
- **Manual**: Admin can flush cache for specific users or globally
- **Selective**: Invalidate only affected cache entries (user-specific or item-specific)

### 4.3 Cache Hierarchy
1. **Client-side Cache**: Browser/app cache (respects Cache-Control headers)
2. **CDN Cache**: Edge caching for public recommendation endpoints
3. **Gateway Cache**: Redis-backed cache at API gateway level
4. **Service Cache**: Application-level caching within recommendation service
5. **Model Prediction Cache**: Cache model scores for same user-item pairs

---

## 5. Circuit Breaking

### 5.1 Configuration
```yaml
circuit_breaker:
  failure_threshold: 5        # Open after 5 consecutive failures
  success_threshold: 3        # Close after 3 consecutive successes
  timeout: 30s                # Wait 30s before half-open test
  half_open_max_requests: 3   # Test with 3 requests in half-open
  fallback: cached_response   # Return cached recommendations on failure
```

### 5.2 Fallback Strategies
- **Cached Recommendations**: Return most recent cached recommendations
- **Popular Items**: Return globally or segment-popular items
- **Default Recommendations**: Return editorially curated recommendations
- **Degraded Mode**: Return fewer recommendations with reduced personalization
- **Error Response**: Return error with retry-after for non-critical endpoints

---

## 6. Request Aggregation

### 6.1 Home Page Recommendation Aggregation
A single home page request may need data from multiple services:
```
Request → API Gateway
  ├── Fan-out to User Profile Service (user preferences)
  ├── Fan-out to Recommendation Service (personalized recs)
  ├── Fan-out to Trending Service (trending items)
  └── Fan-out to Experiment Service (experiment assignments)
Aggregate results → Return to client
```

### 6.2 Aggregation Strategies
- **Parallel Fan-out**: Call all services in parallel; wait for all responses
- **Timeout Aggregation**: Return partial results if some services timeout
- **Progressive Enhancement**: Return base results immediately; enhance as additional services respond
- **Graceful Degradation**: If one service fails, return results from other services

---

## 7. Open Source API Gateway Comparison

### 7.1 Kong
- **Language**: Lua (Nginx/OpenResty)
- **Features**: Plugin ecosystem, admin API, enterprise support
- **Plugins**: Rate limiting, authentication, logging, transformation
- **Deployment**: Kubernetes, Docker, bare metal
- **Pros**: Mature, extensive plugin library, enterprise features
- **Cons**: Lua-based (less common), enterprise features require license

### 7.2 Traefik
- **Language**: Go
- **Features**: Auto-discovery, Let's Encrypt, Kubernetes native
- **Deployment**: Kubernetes, Docker, file-based
- **Pros**: Kubernetes-native, automatic service discovery, simple config
- **Cons**: Fewer plugins, less mature than Kong

### 7.3 Apache APISIX
- **Language**: Lua (Nginx/OpenResty)
- **Features**: Dynamic routing, plugin ecosystem, high performance
- **Deployment**: Kubernetes, Docker, bare metal
- **Pros**: High performance, dynamic configuration, active community
- **Cons**: Smaller community than Kong

### 7.4 Envoy
- **Language**: C++
- **Features**: L4/L7 proxy, xDS protocol, service mesh
- **Deployment**: Standalone, sidecar (Istio), Kubernetes
- **Pros**: High performance, service mesh integration, extensible
- **Cons**: Complex configuration, designed primarily as sidecar proxy

### 7.5 Recommendation for Production
- **Standalone**: Kong or APISIX for dedicated API gateway
- **Kubernetes-native**: Traefik for automatic service discovery
- **Service Mesh**: Envoy (via Istio) for integrated gateway + mesh
- **High Performance**: APISIX or Envoy for maximum throughput
