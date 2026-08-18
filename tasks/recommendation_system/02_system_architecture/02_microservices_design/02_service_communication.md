# Service Communication Patterns

## 1. Synchronous vs Asynchronous Communication

### 1.1 Synchronous Communication
**When to Use**:
- Client needs immediate response (real-time recommendations)
- Operation requires confirmation before proceeding
- Low-latency data retrieval needed (feature fetching)
- Request-response pattern is natural

**Protocols**:
- **REST/HTTP**: Universal compatibility; JSON payloads; HTTP/2 multiplexing
- **gRPC**: Binary protocol buffers; bidirectional streaming; HTTP/2; ~10x faster than REST
- **GraphQL**: Flexible client-driven queries; single endpoint; schema introspection

**Tradeoffs**:
- Tight coupling: caller waits for callee; both must be available
- Cascading failures: callee failure causes caller failure
- Timeout management: must set appropriate timeouts
- Load management: caller's load directly impacts callee

### 1.2 Asynchronous Communication
**When to Use**:
- Result not immediately needed (event logging, feature updates)
- High throughput needed (interaction events, impression tracking)
- Loose coupling desired (services evolve independently)
- Natural event-driven workflow (user action triggers downstream processing)
- Load leveling needed (buffer bursts of requests)

**Technologies**:
- **Apache Kafka**: High throughput, durable, ordered event streaming
- **RabbitMQ**: Flexible routing, message acknowledgment, priority queues
- **Redis Streams**: Lightweight event streaming, in-memory performance
- **NATS**: Ultra-lightweight, high-performance messaging

**Tradeoffs**:
- Eventual consistency: data may not be immediately consistent
- Complexity: more infrastructure, harder to debug
- Ordering: ordering guarantees limited to partition/topic level
- Delivery semantics: at-least-once vs exactly-once considerations

---

## 2. Communication Matrix

### 2.1 Service-to-Service Communication Patterns

| Source → Destination | Pattern | Protocol | Latency Budget | Rationale |
|---|---|---|---|---|
| Client → API Gateway | Request-Response | REST/GraphQL | N/A | External API |
| API Gateway → User Profile | Request-Response | gRPC | <5ms | Need user data for request |
| API Gateway → Experiment | Request-Response | gRPC | <3ms | Need experiment assignment |
| Candidate Gen → Item Search | Request-Response | gRPC | <20ms | Need search results |
| Candidate Gen → Feature Store | Request-Response | Redis Protocol | <3ms | Need user features |
| Ranking → Feature Store | Request-Response | Redis Protocol | <5ms | Need user+item features |
| Ranking → Model Serving | Request-Response | gRPC | <30ms | Need model predictions |
| User Action → Interaction Service | Fire-and-Forget | Kafka | N/A | Event logging |
| Interaction Service → Feature Compute | Event-Driven | Kafka | N/A | Feature updates |
| Feature Compute → Feature Store | Request-Response | Redis Protocol | <3ms | Feature materialization |
| Model Registry → Model Serving | Streaming | gRPC | <100ms | Model updates |
| All Services → Monitoring | Fire-and-Forget | Prometheus | N/A | Metrics collection |

---

## 3. API Gateway Patterns

### 3.1 Gateway Responsibilities
- **Request Routing**: Route requests to appropriate backend services
- **Authentication**: Validate JWT tokens and API keys
- **Rate Limiting**: Protect backend services from overload
- **Request Validation**: Validate request schemas before forwarding
- **Response Caching**: Cache recommendation results
- **Load Balancing**: Distribute requests across service instances
- **Circuit Breaking**: Protect against cascading failures
- **Request Transformation**: Protocol translation (REST → gRPC)
- **Response Aggregation**: Combine responses from multiple services
- **API Versioning**: Route based on API version
- **Logging and Analytics**: Track API usage patterns

### 3.2 Backend for Frontend (BFF) Pattern
Different clients have different needs:
- **Web BFF**: Optimized for browser clients; server-side rendering support; GraphQL
- **Mobile BFF**: Optimized for mobile networks; reduced payload sizes; aggressive caching
- **Internal BFF**: Optimized for service-to-service; gRPC; detailed metadata

### 3.3 Open Source API Gateway Options

| Gateway | Language | Key Features | Best For |
|---|---|---|---|
| Kong | Lua/Nginx | Plugin ecosystem, enterprise features | Enterprise deployments |
| Traefik | Go | Auto-discovery, Let's Encrypt, Kubernetes native | Kubernetes environments |
| APISIX | Lua/Nginx | High performance, dynamic routing | High-throughput APIs |
| Envoy | C++ | Service mesh proxy, xDS protocol | Service mesh integration |
| KrakenD | Go | Aggregation, high performance | API aggregation |

---

## 4. gRPC Design for Internal Services

### 4.1 Why gRPC for Internal Communication
- **Performance**: Protocol Buffers are ~10x faster than JSON serialization
- **Type Safety**: Schema-enforced contracts between services
- **Streaming**: Bidirectional streaming for real-time updates
- **Code Generation**: Auto-generated client/server stubs in multiple languages
- **HTTP/2**: Multiplexed connections, header compression

### 4.2 Service Definition Example Pattern
```protobuf
service RecommendationService {
  rpc GetRecommendations(RecommendationRequest) returns (RecommendationResponse);
  rpc StreamRecommendations(stream RecommendationRequest) returns (stream RecommendationResponse);
  rpc GetSimilarItems(SimilarItemsRequest) returns (SimilarItemsResponse);
}

message RecommendationRequest {
  string user_id = 1;
  string context_id = 2;
  Context context = 3;
  int32 num_results = 4;
  repeated Filter filters = 5;
}

message RecommendationResponse {
  repeated RecommendedItem items = 1;
  string experiment_id = 2;
  string model_version = 3;
  map<string, string> metadata = 4;
}
```

### 4.3 gRPC Best Practices for Recommendations
- **Deadline Propagation**: Pass deadline through all service calls
- **Load Balancing**: Client-side load balancing with gRPC resolver
- **Connection Pooling**: Maintain persistent connections to downstream services
- **Error Handling**: Use standard gRPC status codes
- **Retry Policy**: Configure retry with exponential backoff for idempotent calls
- **Health Checking**: Implement gRPC health checking protocol

---

## 5. Message Queue Patterns

### 5.1 Point-to-Point
- **Pattern**: One producer, one consumer per message
- **Use Case**: Task distribution (e.g., model training jobs, feature computation jobs)
- **Kafka Implementation**: Single consumer group
- **RabbitMQ Implementation**: Default queue behavior

### 5.2 Publish-Subscribe
- **Pattern**: One producer, multiple consumers per message
- **Use Case**: Event broadcasting (e.g., user interaction event triggers multiple processors)
- **Kafka Implementation**: Multiple consumer groups reading same topic
- **RabbitMQ Implementation**: Fanout exchange with multiple bound queues

### 5.3 Request-Reply
- **Pattern**: Producer sends request and waits for reply on separate channel
- **Use Case**: Service-to-service calls over message broker (when HTTP/gRPC not preferred)
- **Implementation**: Correlation ID to match requests with replies; reply queue per client

### 5.4 Competing Consumers
- **Pattern**: Multiple consumers process messages from same queue
- **Use Case**: Horizontal scaling of message processing
- **Load Balancing**: Round-robin (RabbitMQ) or partition assignment (Kafka)
- **Ordering**: Maintain ordering per partition/key

---

## 6. Service Mesh for Recommendations

### 6.1 What a Service Mesh Provides
- **mTLS**: Automatic mutual TLS for all inter-service communication
- **Traffic Management**: Load balancing, routing, circuit breaking, retries
- **Observability**: Automatic metrics, distributed tracing, access logging
- **Security**: Authorization policies, rate limiting at mesh level
- **Resilience**: Timeout, retry, circuit breaking without application code

### 6.2 Service Mesh Options
- **Istio**: Feature-rich, Envoy-based, extensive traffic management
- **Linkerd**: Lightweight, simple, excellent performance
- **Cilium**: eBPF-based, high performance, kernel-level networking

### 6.3 Service Mesh for Recommendation-Specific Needs
- **Latency Monitoring**: Automatic P50/P95/P99 latency tracking for every service-to-service call
- **Circuit Breaking**: Protect model serving from overload
- **Retries**: Automatic retries for transient failures in feature store calls
- **Canary Routing**: Route percentage of traffic to new model version
- **mTLS**: Encrypt all internal communication including feature data

---

## 7. Dead Letter Queue Handling

### 7.1 DLQ Architecture
- **DLQ Topic**: Separate topic for messages that fail processing after max retries
- **DLQ Metadata**: Original topic, partition, offset, error message, retry count, timestamp
- **DLQ Consumer**: Separate consumer that processes failed messages (reprocess, alert, archive)
- **DLQ Dashboard**: Monitor DLQ depth, error patterns, and processing rate

### 7.2 DLQ Processing Strategies
1. **Retry with Correction**: Fix the issue and retry the message
2. **Manual Inspection**: Route to admin interface for manual investigation
3. **Archive**: Store for debugging and analysis
4. **Drop**: Discard messages that are no longer relevant (with logging)

### 7.3 Error Classification
- **Transient**: Network timeout, temporary overload → retry automatically
- **Persistent**: Schema validation error, missing required field → DLQ
- **Poison**: Message causes processing crash → DLQ after max retries
- **Business**: Data violates business rule → DLQ with business error metadata
