# gRPC Design for Internal Recommendation Services

## 1. Why gRPC for Internal Communication

### 1.1 Advantages Over REST
- **Performance**: Protocol Buffers binary serialization is ~10x faster than JSON
- **Type Safety**: Schema-enforced contracts prevent runtime serialization errors
- **Streaming**: Native bidirectional streaming for real-time updates
- **Code Generation**: Auto-generated client/server stubs in 10+ languages
- **HTTP/2**: Multiplexed connections, header compression, server push
- **Deadline Propagation**: Built-in timeout propagation across service calls

### 1.2 When to Use gRPC
- Service-to-service internal communication
- High-throughput, low-latency requirements
- Streaming data (model updates, real-time features)
- Polyglot services (different programming languages)
- Strong API contracts between teams

### 1.2 When NOT to Use gRPC
- Client-facing APIs (use REST or GraphQL)
- Browser-to-server communication (use REST with gRPC-Web)
- Simple APIs with few endpoints
- When human-readable payloads are needed for debugging

---

## 2. Protocol Buffer Schema Design

### 2.1 Service Definition Pattern
```protobuf
syntax = "proto3";
package recommendation.v1;

service CandidateService {
  rpc GetCandidates(CandidateRequest) returns (CandidateResponse);
  rpc StreamCandidates(stream CandidateRequest) returns (stream CandidateResponse);
}

service RankingService {
  rpc RankItems(RankRequest) returns (RankResponse);
  rpc ExplainRanking(ExplainRequest) returns (ExplainResponse);
}

service FeatureService {
  rpc GetFeatures(FeatureRequest) returns (FeatureResponse);
  rpc GetBulkFeatures(BulkFeatureRequest) returns (BulkFeatureResponse);
  rpc StreamFeatureUpdates(stream FeatureSubscription) returns (stream FeatureUpdate);
}

service UserProfileService {
  rpc GetUserProfile(ProfileRequest) returns (UserProfile);
  rpc UpdatePreferences(UpdateRequest) returns (UserProfile);
}
```

### 2.2 Message Design Best Practices
- Use explicit field numbers (never reuse deleted field numbers)
- Use string for IDs (UUID/ULID encoded as string)
- Use enums for categorical fields with limited values
- Use google.protobuf.Timestamp for timestamps
- Use google.protobuf.Duration for durations
- Include metadata in response messages (model version, latency)
- Use maps for dynamic key-value pairs

### 2.3 Schema Evolution Rules
1. Never change field numbers of existing fields
2. Never change the type of existing fields
3. New fields must use new field numbers
4. Use reserved for removed field numbers and names
5. Always provide defaults for new optional fields
6. Use proto3 optional for explicit optional fields

---

## 3. Streaming Patterns

### 3.1 Server Streaming
- **Use Case**: Model update notifications, feature update streams
- **Pattern**: Client sends one request, server streams multiple responses
- **Example**: Feature service streams real-time feature updates to ranking service

### 3.2 Client Streaming
- **Use Case**: Batch event submission, bulk feature updates
- **Pattern**: Client streams multiple requests, server sends one response
- **Example**: Interaction service streams user events to feature computation service

### 3.3 Bidirectional Streaming
- **Use Case**: Real-time collaborative filtering, live recommendation updates
- **Pattern**: Both client and server stream independently
- **Example**: Real-time recommendation stream as user browses

---

## 4. Error Handling

### 4.1 gRPC Status Codes for Recommendations
| Code | Name | Usage |
|---|---|---|
| OK (0) | Success | Successful recommendation |
| INVALID_ARGUMENT (3) | Bad Request | Invalid user_id, item_id format |
| NOT_FOUND (5) | Not Found | User or item not found |
| ALREADY_EXISTS (6) | Duplicate | Duplicate interaction event |
| RESOURCE_EXHAUSTED (8) | Overloaded | Model serving at capacity |
| FAILED_PRECONDITION (9) | State Error | Feature store not ready |
| ABORTED (10) | Conflicting | Concurrent modification conflict |
| UNAVAILABLE (14) | Service Down | Upstream service unavailable |
| DATA_LOSS (15) | Data Loss | Unrecoverable data corruption |

### 4.2 Rich Error Details
```protobuf
message RecommendationError {
  string error_code = 1;
  string message = 2;
  map<string, string> context = 3;
  repeated string suggestions = 4;
}
```

---

## 5. Deadline Propagation

### 5.1 Why Deadlines Matter
Without deadline propagation, a slow downstream call can cause:
- Cascading timeouts
- Resource exhaustion (threads waiting on slow calls)
- Poor user experience (long request latencies)

### 5.2 Implementation
```
User Request (200ms total deadline)
  → API Gateway: Sets 200ms deadline
    → Candidate Service: Receives 200ms deadline, passes 150ms to Feature Store
      → Feature Store: Receives 150ms deadline
    → Ranking Service: Receives 150ms deadline, passes 50ms to Model Serving
      → Model Serving: Receives 50ms deadline
```

### 5.3 Deadline Exceeded Handling
- Return DEADLINE_EXCEEDED status code
- Caller implements fallback (cached results, popular items)
- Log the slow call for investigation
- Monitor deadline exceed rate per service

---

## 6. gRPC Best Practices

### 6.1 Connection Management
- Maintain persistent connections to downstream services
- Use connection pooling for high-throughput services
- Configure keepalive to detect dead connections
- Use gRPC health checking protocol

### 6.2 Load Balancing
- Client-side load balancing with round-robin or weighted
- Use gRPC resolver for service discovery
- Consider pick_first for affinity-based routing
- Use consistent hashing for cache-friendly routing

### 6.3 Interceptor Patterns
- **Logging Interceptor**: Log all gRPC calls with latency, status
- **Metrics Interceptor**: Record request count, latency, error rate
- **Tracing Interceptor**: Propagate OpenTelemetry trace context
- **Auth Interceptor**: Validate JWT tokens on incoming calls
- **Retry Interceptor**: Automatic retry for idempotent calls
- **Deadline Interceptor**: Set and propagate deadlines
