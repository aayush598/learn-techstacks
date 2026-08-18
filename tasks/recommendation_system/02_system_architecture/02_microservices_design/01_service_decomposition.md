# Microservices Design — Service Decomposition

## 1. Domain-Driven Design for Recommendations

### 1.1 Bounded Contexts
Domain-Driven Design (DDD) identifies logical boundaries in the system where specific business rules apply.

**User Context**:
- User profiles, preferences, interaction history
- User segmentation and clustering
- Privacy and consent management
- Bounded by: user identity and lifecycle

**Item Context**:
- Item metadata, content, embeddings
- Item lifecycle management
- Content moderation and quality
- Bounded by: item identity and catalog

**Recommendation Context**:
- Candidate generation, ranking, re-ranking
- Model serving and inference
- Recommendation caching and delivery
- Bounded by: recommendation request and response

**Interaction Context**:
- User-item interactions (clicks, views, purchases)
- Feedback collection and processing
- Label generation for training
- Bounded by: interaction event

**Analytics Context**:
- Metrics computation and reporting
- Experimentation and A/B testing
- Business intelligence dashboards
- Bounded by: analytical queries

**ML Platform Context**:
- Model training and evaluation
- Feature engineering and serving
- Experiment tracking and model registry
- Bounded by: ML model lifecycle

### 1.2 Aggregate Design
Aggregates are clusters of domain objects treated as a single unit for data changes.

**User Aggregate**:
- Root: User
- Entities: UserProfile, UserPreferences, UserSegment
- Invariants: User must have at least one preference category; segment must be valid
- Consistency boundary: All user data changes within single transaction

**Item Aggregate**:
- Root: Item
- Entities: ItemMetadata, ItemEmbedding, ItemStatistics
- Invariants: Item must have title and category; embeddings must match metadata version
- Consistency boundary: Item updates are atomic

**Recommendation Request Aggregate**:
- Root: RecommendationRequest
- Entities: CandidateItem, ScoredItem, RankedItem
- Invariants: Candidates must pass validation; scores must be in valid range
- Consistency boundary: Single request processed atomically

**Interaction Aggregate**:
- Root: Interaction
- Entities: InteractionEvent, InteractionContext, InteractionOutcome
- Invariants: Interaction must reference valid user and item; timestamp must be valid
- Consistency boundary: Interaction recorded atomically

---

## 2. Service Boundary Identification

### 2.1 High Cohesion Criteria
Services should be cohesive around business capabilities:
- User Profile Service: All user-related operations
- Item Catalog Service: All item-related operations
- Recommendation Service: All recommendation generation operations
- Interaction Service: All interaction recording and processing
- Feature Service: All feature computation and serving
- Experiment Service: All experimentation operations
- Analytics Service: All analytics and reporting

### 2.2 Loose Coupling Criteria
Services should be loosely coupled through:
- Well-defined APIs (no shared databases)
- Event-driven communication (no synchronous dependencies where possible)
- Independent deployability
- Technology independence
- Data ownership (each service owns its data)

### 2.3 Service Boundary Anti-Patterns
- **Distributed Monolith**: Services that must be deployed together
- **Shared Database**: Multiple services reading/writing the same tables
- **God Service**: A single service that does everything
- **Nano Service**: A service so small it adds operational overhead without benefit
- **Temporal Coupling**: Synchronous calls that require both services to be up simultaneously

---

## 3. Database Per Service Pattern

### 3.1 Implementation
Each service owns its data store exclusively:
- **User Service**: PostgreSQL database `user_db`
- **Item Service**: PostgreSQL database `item_db` + Elasticsearch index
- **Feature Store**: Redis Cluster (online) + Parquet files on MinIO (offline)
- **Interaction Service**: Kafka topics + ClickHouse for analytics
- **Experiment Service**: PostgreSQL database `experiment_db`
- **Model Service**: PostgreSQL database `model_db` + S3/MinIO for artifacts

### 3.2 Cross-Service Data Access
When Service A needs data from Service B:
1. **API Call**: Service A calls Service B's API (synchronous)
2. **Event Propagation**: Service B publishes events; Service A maintains local copy
3. **API Composition**: API Gateway or BFF aggregates data from multiple services
4. **CQRS Materialization**: Pre-join data from multiple services into read-optimized stores

### 3.3 Data Consistency
- **Within Service**: Strong consistency using database transactions
- **Across Services**: Eventual consistency using events
- **Compensating Transactions**: For operations spanning multiple services (Saga pattern)
- **Idempotent Operations**: All cross-service operations designed for retry safety

---

## 4. Saga Pattern for Complex Workflows

### 4.1 Recommendation Delivery Saga
Scenario: Delivering a recommendation involves multiple services.

**Steps**:
1. API Gateway receives recommendation request
2. Candidate Service retrieves candidates
3. Feature Store provides features
4. Ranking Service scores candidates
5. Re-ranking Service applies business rules
6. Interaction Service logs the recommendation
7. Response sent to user

**Failure Handling**:
- If Candidate Service fails → Return trending/popular items (fallback)
- If Feature Store fails → Use cached features or default features
- If Ranking Service fails → Return candidates sorted by popularity
- If Interaction Service fails → Log asynchronously (non-critical path)

### 4.2 User Onboarding Saga
**Steps**:
1. User Service creates user account
2. Preference Service initializes default preferences
3. Feature Service computes initial user features
4. Experiment Service assigns user to experiments
5. Recommendation Service generates initial recommendations

**Compensation**:
- If any step fails, compensate by cleaning up previous steps
- User account creation is the anchor; all other steps can be retried

### 4.3 Model Deployment Saga
**Steps**:
1. Model Registry transitions model to "staging"
2. Integration tests run against staging model
3. Canary deployment to 5% traffic
4. Monitoring period (configurable duration)
5. Full promotion or rollback

**Compensation**:
- If tests fail → Revert to "development" stage
- If canary metrics degrade → Revert traffic to previous model
- If promotion fails → Rollback to previous version

---

## 5. Service Size and Complexity Guidelines

### 5.1 When to Split a Service
- **Team Growth**: When a service is maintained by more than 2-3 teams
- **Deployment Frequency**: When deployment of one feature requires deploying unrelated features
- **Scaling Mismatch**: When different parts of the service need different scaling
- **Technology Diversity**: When different parts need different runtimes or frameworks
- **Failure Isolation**: When failure in one capability should not affect others
- **Bounded Context Change**: When new business requirements create new bounded contexts

### 5.2 When to Merge Services
- **Low Traffic**: When a service handles very low request volume
- **High Communication**: When two services communicate synchronously on every request
- **Shared Data**: When services share most of their data and are always deployed together
- **Operational Overhead**: When the operational cost exceeds the architectural benefit
- **Latency Sensitivity**: When inter-service network latency is unacceptable

### 5.3 Service Complexity Budget
Each service should aim for:
- **Team Size**: 3-8 engineers per service
- **Code Size**: Manageable by a small team in reasonable time
- **API Surface**: 5-15 endpoints maximum
- **Dependencies**: Maximum 5-7 downstream dependencies
- **Data Entities**: 3-5 core entities per service

---

## 6. Strangler Fig Pattern for Migration

### 6.1 Monolith to Microservices Migration
When migrating from an initial monolith to microservices:

1. **Identify Boundary**: Choose a well-defined bounded context to extract first
2. **Create New Service**: Build the new service alongside the monolith
3. **Route Traffic**: Use API gateway to route requests to new service for new users
4. **Monitor**: Compare outputs from monolith and new service
5. **Expand**: Gradually shift more traffic to the new service
6. **Extract Data**: Migrate data ownership to the new service
7. **Remove Dead Code**: Clean up monolith code once traffic is fully migrated
8. **Repeat**: Move to next bounded context

### 6.2 Recommended Extraction Order
1. **Recommendation Serving** (first): Stateless, well-defined, high business value
2. **Feature Service**: Clear interface, independent data stores
3. **Interaction Service**: Event-driven, natural service boundary
4. **Experiment Service**: Well-scoped, clear API
5. **User Service**: Requires careful data migration
6. **Item Service**: Requires careful data migration
7. **Analytics Service**: Can be extracted last as it's read-only
