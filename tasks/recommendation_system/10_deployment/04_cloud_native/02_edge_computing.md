# Edge Computing for Recommendation Systems

Edge computing brings computation closer to the user, reducing latency and enabling personalized experiences even when backend services are slow or unavailable. For recommendation systems, edge computing means serving personalized content from CDN edge nodes, executing lightweight personalization logic in edge functions, and running small ML models directly in the browser. This document covers CDN caching for recommendations, edge functions, edge ML inference, caching strategies, latency reduction, and bandwidth optimization.

---

## 1. CDN Caching for Recommendations

### 1.1 What Can Be Cached at the Edge

| Content Type | Cacheability | TTL Strategy | Invalidation |
|---|---|---|---|
| Popular item lists | Highly cacheable | 5–15 minutes | Tag-based purge |
| Category-based recommendations | Cacheable | 10–30 minutes | Tag-based purge |
| Trending items | Moderately cacheable | 1–5 minutes | Short TTL |
| Personalized recommendations | Not directly cacheable | N/A | Use edge functions |
| Real-time features | Not cacheable | N/A | Compute at edge |
| Static assets (thumbnails, descriptions) | Highly cacheable | 24 hours | Versioned URLs |

### 1.2 CDN Provider Comparison

| Provider | Edge Locations | Edge Compute | ML Support | Pricing Model |
|---|---|---|---|---|
| Cloudflare | 300+ | Workers (V8 isolates) | Workers AI (ONNX) | Bandwidth-based |
| Fastly | 70+ | Compute@Edge (Wasm) | Limited | Bandwidth-based |
| AWS CloudFront | 400+ | Lambda@Edge, CloudFront Functions | SageMaker endpoints | Request + bandwidth |
| Akamai | 4000+ | EdgeWorkers | Limited | Bandwidth-based |

### 1.3 Cache Key Design for Recommendations

| Cache Key Component | Example | Purpose |
|---|---|---|
| User segment | `segment:power-user` | Segment-based caching |
| Content type | `type:trending` | Different cache policies per type |
| Region | `region:us-west` | Geo-specific recommendations |
| Device type | `device:mobile` | Device-appropriate content |
| Language | `lang:en` | Locale-specific content |

**Effective cache key:** `segment:power-user/type:trending/region:us-west/device:mobile/lang:en`

### 1.4 Cache Hit Optimization

| Strategy | Implementation | Expected Hit Rate |
|---|---|---|
| Segment-based caching | Cache per user segment, not per user | 85–95% |
| Popular item pre-warming | Push trending items to edge before peak hours | 90–98% |
| Tiered caching | Regional edge → origin shield → origin | 70–85% |
| stale-while-revalidate | Serve stale, refresh in background | 95%+ |

---

## 2. Edge Functions for Personalization

### 2.1 Cloudflare Workers

Cloudflare Workers execute JavaScript/Wasm at 300+ edge locations within milliseconds.

**Use cases for recommendation systems:**

| Function | Trigger | Logic | Latency |
|---|---|---|---|
| Personalization router | Every request | Route to appropriate recommendation model | < 5ms |
| A/B test assignment | Every request | Assign user to experiment group | < 2ms |
| Feature assembly | Every request | Assemble features from KV store | < 5ms |
| Fallback generation | Origin timeout | Serve cached/alternate recommendations | < 3ms |
| Content filtering | Every request | Filter recommendations by region, compliance | < 2ms |

### 2.2 Edge Function Architecture

```
User Request → CDN Edge Node → Edge Function → KV Store (cached features)
                                      ↓
                              [Cache Hit] → Return cached recommendation
                              [Cache Miss] → Forward to origin API
                                      ↓
                              Origin responds → Cache at edge → Return to user
```

### 2.3 Edge KV for Feature Storage

| Store Type | Latency | Use Case | Size Limit |
|---|---|---|---|
| Cloudflare Workers KV | 10–50ms (eventual consistency) | User preferences, item metadata | 25 GB per namespace |
| Cloudflare D1 (SQLite) | 10–30ms | Structured queries, item catalog | 10 GB per database |
| Cloudflare R2 | 50–100ms (object access) | Large model artifacts, embeddings | Unlimited |
| Fastly KV Store | 10–30ms | Similar to Workers KV | 10 GB per store |

### 2.4 Edge Function Limitations

| Limitation | Cloudflare Workers | Impact |
|---|---|---|
| CPU time | 30ms (free), 30s (paid) | Complex inference not feasible |
| Memory | 128MB | Large models won't fit |
| Cold start | < 5ms (V8 isolates) | Near-instant startup |
| Concurrency | 1000+ per request | Fan-out for feature assembly |
| Subrequests | 50 per request | Multiple KV/API calls allowed |

---

## 3. Edge ML Inference

### 3.1 ONNX Runtime Web

ONNX Runtime Web enables running ML models directly in the browser:

| Aspect | Configuration |
|---|---|
| Model format | ONNX (converted from PyTorch/TensorFlow) |
| Execution backend | WebAssembly (CPU), WebGL/WebGPU (GPU) |
| Model size limit | ~50MB practical (for fast loading) |
| Inference latency | 5–50ms depending on model complexity |
| Browser support | Chrome, Firefox, Safari, Edge |

### 3.2 Browser-Based Recommendation Models

| Model Type | Size | Latency | Use Case |
|---|---|---|---|
| Embedding similarity (dot product) | 1–5MB | < 5ms | Item similarity recommendations |
| Lightweight neural ranking | 5–20MB | 10–30ms | Re-rank pre-computed candidates |
| Decision tree ensemble | 1–10MB | < 5ms | Feature-based scoring |
| Collaborative filtering (matrix factorization) | 10–50MB | 10–20ms | User-item score computation |

### 3.3 Edge Inference Architecture

1. **Origin** computes candidate recommendations (hundreds of items)
2. **Edge function** retrieves candidates and user features from edge cache
3. **Browser** runs lightweight re-ranking model on candidates
4. **Result** is personalized, low-latency recommendation without origin round-trip

### 3.4 Model Distribution Strategy

| Strategy | Implementation | Use Case |
|---|---|---|
| CDN-cached models | Serve ONNX files from CDN edge | Browser inference |
| Service worker caching | Cache model in browser's Service Worker | Offline-capable recommendations |
| Preloading | `<link rel="preload">` for model files | Predictable access patterns |
| Progressive loading | Load model in chunks as needed | Large models, low-priority pages |

---

## 4. Edge Caching Strategies

### 4.1 Cache Hierarchy

| Tier | Location | Latency | Capacity | Freshness |
|---|---|---|---|---|
| L1: Browser cache | User's device | < 1ms | 50–500MB | TTL-based |
| L2: Edge cache | CDN PoP closest to user | 5–20ms | 100GB+ per PoP | TTL + purge |
| L3: Regional cache | Central CDN nodes | 20–50ms | 1TB+ | TTL + purge |
| L4: Origin shield | CDN's origin-facing cache | 50–100ms | 10TB+ | Source of truth |
| L5: Origin | Your data center / cloud | 100–500ms | Unlimited | Always fresh |

### 4.2 Cache Invalidation Patterns

| Pattern | Mechanism | Latency | Use Case |
|---|---|---|---|
| TTL expiration | Automatic after duration | N/A (eventual) | Trending content |
| Tag-based purge | Purge by cache tag | 5–15 seconds | New model deployment |
| Instant purge | Purge all edge nodes | 150ms–5 seconds | Emergency content removal |
| Versioned URLs | New URL for new content | Instant (new request) | Static assets |
| Surrogate keys | Purge by key in response header | 5–30 seconds | Granular invalidation |

### 4.3 Stale-While-Revalidate

Serve stale cached content immediately while refreshing in the background:

- User gets response in < 10ms (stale cache)
- Edge function refreshes cache from origin in parallel
- Next user gets fresh content
- Reduces perceived latency to near-zero for cache misses

---

## 5. Latency Reduction

### 5.1 Latency Budget Breakdown

| Hop | Without Edge | With Edge | Improvement |
|---|---|---|---|
| DNS resolution | 20–50ms | 5–10ms (DNS cache) | 75% reduction |
| TLS handshake | 30–100ms | 5–15ms (TLS resumption) | 80% reduction |
| TCP connection | 20–50ms | 2–5ms (connection reuse) | 90% reduction |
| Server processing | 50–200ms | 5–20ms (edge function) | 90% reduction |
| **Total** | **120–400ms** | **17–50ms** | **80%+ reduction** |

### 5.2 Techniques for Latency Reduction

| Technique | Savings | Complexity |
|---|---|---|
| Edge caching | 80–95% latency reduction for cached content | Low |
| Edge computing | 70–90% latency reduction for personalized content | Medium |
| Connection keep-alive | 30–50% for repeat visitors | Low |
| HTTP/3 (QUIC) | 10–30% on lossy networks | Low |
| Early hints (103) | 50–100ms for preloaded resources | Low |
| Edge-side rendering | 50–200ms for server-rendered pages | High |

---

## 6. Bandwidth Optimization

### 6.1 Response Optimization

| Technique | Description | Bandwidth Savings |
|---|---|---|
| Gzip/Brotli compression | Compress API responses | 60–80% |
| Response field selection | Return only requested fields | 30–50% |
| Pagination | Limit items per response | 50–90% |
| Delta responses | Send only changed items since last request | 70–95% |
| Protocol buffers | Binary serialization vs JSON | 30–60% |

### 6.2 Client-Side Optimization

| Technique | Implementation | Impact |
|---|---|---|
| Prefetching | Predict next page, preload recommendations | Reduces perceived latency |
| Lazy loading | Load recommendations as user scrolls | Reduces initial payload |
| Client-side caching | Cache recommendations in localStorage/IndexedDB | Eliminates repeat requests |
| Web workers | Compute scoring in background thread | Non-blocking UI |

### 6.3 Edge-Side Includes (ESI)

ESI allows fragment-level caching within a page:

- **Cacheable fragments**: Trending items, popular categories (long TTL)
- **Personalized fragments**: User-specific recommendations (short TTL or compute at edge)
- **Static fragments**: Headers, footers, navigation (very long TTL)
- **Assembly at edge**: CDN combines fragments into final page

This enables mixing highly cacheable content with personalized content on the same page.
