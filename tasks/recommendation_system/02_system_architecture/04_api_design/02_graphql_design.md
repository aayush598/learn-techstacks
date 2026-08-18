# GraphQL Design for Recommendation Systems

## 1. GraphQL Schema Design

### 1.1 Core Types
```graphql
type Query {
  recommendations(input: RecommendationInput!): RecommendationConnection!
  similarItems(itemId: ID!, limit: Int): [ScoredItem!]!
  userPreferences(userId: ID!): UserPreferences
  item(itemId: ID!): Item
  trending(input: TrendingInput!): [ScoredItem!]!
}

type Mutation {
  recordInteraction(input: InteractionInput!): InteractionPayload!
  updatePreferences(userId: ID!, preferences: PreferencesInput!): UserPreferences!
  submitRating(input: RatingInput!): RatingPayload!
}

type Subscription {
  recommendationUpdates(userId: ID!): RecommendationUpdate!
}
```

### 1.2 Recommendation Types
```graphql
type RecommendationConnection {
  edges: [RecommendationEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
  metadata: RecommendationMetadata!
}

type RecommendationEdge {
  node: ScoredItem!
  score: Float!
  rank: Int!
  explanation: Explanation
}

type ScoredItem {
  id: ID!
  title: String!
  category: Category!
  imageUrl: String
  score: Float!
  explanation: Explanation
  metadata: ItemMetadata
}

type Explanation {
  type: ExplanationType!
  reason: String!
  confidence: Float!
  contributingFeatures: [FeatureContribution!]
}

type RecommendationMetadata {
  modelVersion: String!
  experimentId: String
  latencyMs: Int!
  totalCandidates: Int!
  candidatesScored: Int!
}
```

---

## 2. Query Optimization

### 2.1 DataLoader Pattern
Prevents N+1 queries when resolving related data:
- Batch multiple requests for same resource into single database query
- Cache results within single request lifecycle
- Example: Load all item details for recommendation results in one query instead of N individual queries

### 2.2 Query Complexity Analysis
- Assign complexity cost to each field
- Reject queries exceeding complexity threshold
- Prevent abuse through deeply nested queries
- Example: recommendations query costs 10 + edges×5 + node×1 = 10 + 20×6 = 130

### 2.3 Persisted Queries
- Pre-register query documents on server
- Clients send query ID instead of full query string
- Reduces request payload size
- Enables query whitelisting for security

---

## 3. Caching Strategies

### 3.1 Response-Level Caching
- Cache entire GraphQL responses based on query + variables
- Use cache key: hash(query + variables + user_id)
- TTL based on recommendation freshness requirements

### 3.2 Field-Level Caching
- Cache individual field resolvers
- Item data cached longer than user-specific data
- Recommendation results cached for short duration

### 3.3 CDN Caching
- Public queries (trending, popular) cacheable at CDN
- Use query complexity to determine cacheability
- Personalized queries bypass CDN

---

## 4. GraphQL vs REST for Recommendations

| Aspect | GraphQL | REST |
|---|---|---|
| Over-fetching | Client requests only needed fields | Fixed response schema |
| Under-fetching | Single query for related data | Multiple API calls needed |
| Caching | More complex (POST requests) | Simple HTTP caching |
| Learning curve | Higher (schema, resolvers) | Lower |
| Tooling | GraphiQL, Apollo Studio | Swagger, Postman |
| File upload | Requires specification extension | Native HTTP support |
| Real-time | Subscriptions | WebSockets/SSE |
| Versioning | Schema evolution | URI versioning |

**Recommendation**: Use REST for simple, high-performance serving; GraphQL for client-facing APIs requiring flexibility.

---

## 5. Rate Limiting for GraphQL

### 5.1 Query Complexity-Based Rate Limiting
- Assign cost to each query based on complexity
- Track cumulative cost per user per time window
- Reject queries exceeding budget
- Example: User gets 1000 complexity points per minute

### 5.2 Depth-Based Rate Limiting
- Limit maximum query nesting depth
- Prevent abusive deeply nested queries
- Typical limit: 5-7 levels deep

### 5.3 Field-Level Rate Limiting
- Limit specific expensive fields (e.g., recommendations limited to 10 requests/minute)
- Allow unlimited access to cheap fields (e.g., item metadata)
