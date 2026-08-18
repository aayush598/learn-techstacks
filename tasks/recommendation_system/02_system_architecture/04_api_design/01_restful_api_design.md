# RESTful API Design for Recommendation Systems

## 1. API Design Principles

### 1.1 Resource Modeling
Resources in a recommendation system:
- **Users**: User profiles and preferences
- **Items**: Content/product metadata
- **Recommendations**: Generated recommendation lists
- **Interactions**: User-item interaction events
- **Experiments**: A/B test configurations
- **Models**: ML model metadata and versions

### 1.2 URL Design Conventions
- Use nouns, not verbs for resources
- Use plural nouns for collections
- Use nesting to express relationships
- Use query parameters for filtering, sorting, pagination

### 1.3 Standard Endpoints

**Recommendation Endpoints**:
- `GET /v1/recommendations/home` — Home page personalized recommendations
- `GET /v1/recommendations/for-you` — "For You" personalized feed
- `GET /v1/recommendations/similar/{item_id}` — Similar items to given item
- `GET /v1/recommendations/trending` — Trending/popular items
- `GET /v1/recommendations/category/{category_id}` — Category-based recommendations
- `GET /v1/recommendations/search` — Search with personalized ranking

**User Endpoints**:
- `GET /v1/users/{user_id}/profile` — User profile
- `GET /v1/users/{user_id}/preferences` — User preferences
- `PUT /v1/users/{user_id}/preferences` — Update preferences
- `GET /v1/users/{user_id}/history` — Interaction history
- `GET /v1/users/{user_id}/recommendations` — User-specific recommendations

**Item Endpoints**:
- `GET /v1/items/{item_id}` — Item details
- `GET /v1/items/{item_id}/similar` — Similar items
- `GET /v1/items/{item_id}/also-viewed` — Items also viewed
- `GET /v1/items/{item_id}/also-purchased` — Items also purchased

**Interaction Endpoints**:
- `POST /v1/interactions` — Record interaction event
- `POST /v1/ratings` — Submit rating
- `DELETE /v1/interactions/{interaction_id}` — Remove interaction

---

## 2. Request/Response Design

### 2.1 Request Envelope
```json
{
  "user_id": "user_123",
  "context": {
    "device": "mobile",
    "platform": "ios",
    "session_id": "sess_456"
  },
  "filters": {
    "category": "electronics",
    "price_range": {"min": 50, "max": 200},
    "exclude_purchased": true
  },
  "pagination": {
    "cursor": "eyJpdGVtX2lkIjoiMTAwIn0=",
    "limit": 20
  }
}
```

### 2.2 Response Envelope
```json
{
  "data": {
    "recommendations": [
      {
        "item_id": "item_789",
        "score": 0.95,
        "rank": 1,
        "explanation": {
          "type": "collaborative",
          "reason": "Users similar to you enjoyed this",
          "confidence": 0.87
        },
        "metadata": {
          "model_version": "v4.2.1",
          "experiment_id": "exp_123",
          "variant": "treatment_a"
        }
      }
    ]
  },
  "pagination": {
    "next_cursor": "eyJpdGVtX2lkIjoiMTIwIn0=",
    "has_more": true
  },
  "meta": {
    "total_candidates": 1000000,
    "candidates_scored": 500,
    "latency_ms": 85,
    "model_version": "v4.2.1"
  }
}
```

### 2.3 Error Response (RFC 7807)
```json
{
  "type": "https://api.recommendations.com/errors/rate-limited",
  "title": "Rate Limit Exceeded",
  "status": 429,
  "detail": "Request rate exceeded 100 requests per minute",
  "instance": "/v1/recommendations/home",
  "retry_after": 30
}
```

---

## 3. Pagination Patterns

### 3.1 Cursor-Based Pagination (Recommended)
- Use opaque cursor encoding last item position
- Consistent results even with data changes
- No skip/offset performance issues
- Works well with real-time data

### 3.2 Offset-Based Pagination
- Simple skip/limit parameters
- Consistent page sizes
- Performance degrades with large offsets
- Better for admin interfaces

### 3.3 Infinite Scroll Pagination
- Cursor-based pagination optimized for infinite scroll UIs
- Return 20-50 items per page
- Client requests more as user scrolls
- Pre-fetch next page when user nears bottom

---

## 4. Filtering and Sorting

### 4.1 Filter Parameters
- `category` — Filter by category
- `price_min` / `price_max` — Price range
- `brand` — Filter by brand
- `rating_min` — Minimum rating
- `exclude_ids` — Exclude specific items
- `available_only` — Only available items
- `created_after` — Item freshness filter

### 4.2 Sort Parameters
- `sort_by=relevance` — Default personalized ranking
- `sort_by=popularity` — Sort by popularity
- `sort_by=newest` — Sort by creation date
- `sort_by=price_asc` / `price_desc` — Sort by price
- `sort_by=rating` — Sort by rating

---

## 5. API Versioning

### 5.1 URI Versioning
- `GET /v1/recommendations/home` — Version 1
- `GET /v2/recommendations/home` — Version 2
- Pros: Explicit, easy to route, easy to document
- Cons: URL proliferation, cache invalidation complexity

### 5.2 Header Versioning
- `Accept: application/vnd.api.v1+json`
- Pros: Clean URLs, content negotiation
- Cons: Less visible, harder to test in browser

### 5.3 Version Lifecycle
1. **New Version**: Released with new features
2. **Supported**: Actively maintained and bug-fixed
3. **Deprecated**: Still functional but marked for removal
4. **Sunset**: Removed after deprecation period (typically 6-12 months)

---

## 6. HTTP Status Codes for Recommendations

| Code | Usage |
|---|---|
| 200 OK | Successful recommendation response |
| 201 Created | Interaction event recorded |
| 204 No Content | Preference updated successfully |
| 400 Bad Request | Invalid request parameters |
| 401 Unauthorized | Missing or invalid authentication |
| 403 Forbidden | Insufficient permissions |
| 404 Not Found | User or item not found |
| 429 Too Many Requests | Rate limit exceeded |
| 500 Internal Server Error | Server error (fallback to cached results) |
| 502 Bad Gateway | Upstream service unavailable |
| 503 Service Unavailable | System temporarily unavailable |

---

## 7. Caching Headers

### 7.1 Cache-Control for Recommendations
```
# Personalized recommendations (short cache)
Cache-Control: private, max-age=300, stale-while-revalidate=60

# Similar items (medium cache)
Cache-Control: public, max-age=3600, stale-while-revalidate=300

# Trending items (longer cache)
Cache-Control: public, max-age=1800, stale-while-revalidate=600

# Item metadata (long cache)
Cache-Control: public, max-age=86400, stale-while-revalidate=3600
```

### 7.2 ETag Support
- Generate ETag based on recommendation content hash
- Support If-None-Match for conditional requests
- Reduce bandwidth for unchanged recommendations
