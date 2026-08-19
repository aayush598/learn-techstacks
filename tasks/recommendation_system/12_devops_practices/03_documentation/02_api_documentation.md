# API Documentation

## Overview

API documentation describes how external and internal consumers interact with the recommendation system's interfaces. For ML systems, API documentation must cover not only traditional REST endpoints but also model serving interfaces, batch prediction APIs, and feature retrieval APIs. Clear, accurate API documentation reduces integration time, prevents misuse, and enables self-service for downstream consumers.

## OpenAPI/Swagger for REST

### OpenAPI Specification

OpenAPI (formerly Swagger) is the industry standard for documenting REST APIs. It provides a machine-readable specification that can generate interactive documentation, client SDKs, and server stubs.

### OpenAPI Document Structure

```yaml
openapi: 3.1.0
info:
  title: Recommendation Service API
  version: 2.3.0
  description: |
    API for retrieving personalized recommendations.
    Supports real-time ranking, batch predictions, and model management.
  contact:
    name: ML Platform Team
    email: ml-platform@company.com

servers:
  - url: https://recs-api.company.com/v2
    description: Production
  - url: https://recs-api-staging.company.com/v2
    description: Staging

paths:
  /recommendations/{user_id}:
    get:
      summary: Get personalized recommendations for a user
      operationId: getRecommendations
      tags: [Recommendations]
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
            format: int64
          description: Unique user identifier
        - name: n
          in: query
          required: false
          schema:
            type: integer
            default: 10
            minimum: 1
            maximum: 100
          description: Number of recommendations to return
        - name: context
          in: query
          required: false
          schema:
            $ref: '#/components/schemas/Context'
          description: Recommendation context (time, device, etc.)
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RecommendationResponse'
        '400':
          description: Invalid request
        '404':
          description: User not found
        '429':
          description: Rate limit exceeded
        '500':
          description: Internal server error
      security:
        - ApiKeyAuth: []

components:
  schemas:
    RecommendationResponse:
      type: object
      properties:
        user_id:
          type: integer
        recommendations:
          type: array
          items:
            $ref: '#/components/schemas/RecommendationItem'
        model_version:
          type: string
        latency_ms:
          type: number
        request_id:
          type: string

    RecommendationItem:
      type: object
      properties:
        item_id:
          type: integer
        score:
          type: number
          format: float
          description: Model prediction score (0–1)
        reason:
          type: string
          description: Human-readable recommendation reason
        metadata:
          type: object
          additionalProperties: true

    Context:
      type: object
      properties:
        device:
          type: string
          enum: [mobile, desktop, tablet]
        time_of_day:
          type: string
          format: date-time
        session_id:
          type: string

  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
```

### Interactive Documentation

| Tool | Description | Hosting |
|------|-------------|---------|
| **Swagger UI** | Interactive API explorer | Self-hosted or cloud |
| **Redoc** | Three-panel documentation | Self-hosted or cloud |
| **Stoplight** | Design-first API platform | Cloud |
| **Scalar** | Modern API reference | Self-hosted or cloud |

### OpenAPI Best Practices

1. **Version the API**: Include version in URL path (`/v2/...`)
2. **Document all error codes**: List every possible response code with description
3. **Include examples**: Provide request and response examples for every endpoint
4. **Use refs**: Reference shared schemas to avoid duplication
5. **Document rate limits**: Include rate limit headers in responses
6. **Add request IDs**: Always include request IDs for debugging

## gRPC Documentation (protoc-gen-doc)

### gRPC for ML Services

gRPC is often preferred for ML model serving because of its performance (binary protocol, HTTP/2 multiplexing, streaming support).

### Proto Definition

```protobuf
syntax = "proto3";

package recsys.v1;

service RecommendationService {
  // Get real-time recommendations for a user
  rpc GetRecommendations (RecommendationRequest)
      returns (RecommendationResponse);

  // Stream real-time recommendations
  rpc StreamRecommendations (RecommendationRequest)
      returns (stream RecommendationItem);

  // Batch prediction for multiple users
  rpc BatchPredict (BatchPredictionRequest)
      returns (BatchPredictionResponse);
}

message RecommendationRequest {
  int64 user_id = 1;
  int32 n = 2;
  Context context = 3;
  map<string, string> filters = 4;
}

message RecommendationResponse {
  int64 user_id = 1;
  repeated RecommendationItem recommendations = 2;
  string model_version = 3;
  double latency_ms = 4;
  string request_id = 5;
}

message RecommendationItem {
  int64 item_id = 1;
  float score = 2;
  string reason = 3;
  map<string, string> metadata = 4;
}

message Context {
  string device = 1;
  string time_of_day = 2;
  string session_id = 3;
}

message BatchPredictionRequest {
  repeated RecommendationRequest requests = 1;
}

message BatchPredictionResponse {
  repeated RecommendationResponse responses = 1;
}
```

### gRPC Documentation Generation

```bash
# Generate documentation from proto files
protoc --doc_out=html --doc_opt=html,index.html \
  recsys/v1/recommendation.proto

# Generate with custom template
protoc --doc_out=custom_template.html \
  --doc_opt=custom_template.html,output.html \
  recsys/v1/recommendation.proto
```

## GraphQL Documentation (GraphQL Playground)

### GraphQL Schema for Recommendations

```graphql
type Query {
  """Get personalized recommendations for a user"""
  recommendations(
    userId: ID!
    limit: Int = 10
    context: ContextInput
    filters: [FilterInput]
  ): RecommendationConnection!

  """Get recommendation reasons for specific items"""
  explanation(
    userId: ID!
    itemIds: [ID!]!
  ): [Explanation!]!
}

type RecommendationConnection {
  edges: [RecommendationEdge!]!
  pageInfo: PageInfo!
  modelVersion: String!
  latencyMs: Float!
}

type RecommendationEdge {
  node: RecommendationItem!
  score: Float!
  reason: String
}

type RecommendationItem {
  id: ID!
  title: String!
  category: String!
  imageUrl: String
  metadata: JSON
}

type Explanation {
  itemId: ID!
  reasons: [ExplanationReason!]!
  featureContributions: [FeatureContribution!]!
}

input ContextInput {
  device: DeviceType
  timeOfDay: DateTime
  sessionId: String
}

enum DeviceType {
  MOBILE
  DESKTOP
  TABLET
}
```

## API Changelog

### Changelog Format

```markdown
# API Changelog

## [2.3.0] - 2024-01-15

### Added
- `context` parameter for device-aware recommendations
- `reason` field in recommendation items
- Batch prediction endpoint (`/v2/batch`)

### Changed
- `score` field now normalized to [0, 1] range
- Rate limit increased from 100 to 500 req/min

### Deprecated
- `/v1/recommendations` endpoint (use `/v2/recommendations`)
- `old_score` field (use `score` instead)

### Removed
- `/v1/batch` endpoint (migrated to `/v2/batch`)

### Fixed
- Fixed null handling in context parameter

## [2.2.0] - 2023-11-01
...
```

### Changelog Best Practices

1. **Follow Keep a Changelog format**: Added, Changed, Deprecated, Removed, Fixed, Security
2. **Include migration guides**: When breaking changes are introduced
3. **Link to issues/PRs**: For traceability
4. **Version semantic**: MAJOR.MINOR.PATCH
5. **Announce breaking changes**: Email/notification for breaking API changes

## SDK Documentation

### Python SDK Example

```python
"""
Recommendation Service Python SDK

Installation:
    pip install recsys-sdk

Quick Start:
    from recsys import RecommendationClient

    client = RecommendationClient(api_key="your-api-key")
    recs = client.get_recommendations(user_id=12345, n=10)
    for item in recs:
        print(f"{item.item_id}: {item.score:.3f} - {item.reason}")
"""

from recsys import RecommendationClient
from recsys.models import Context, RecommendationResponse

# Initialize client
client = RecommendationClient(
    api_key="your-api-key",
    base_url="https://recs-api.company.com/v2",
    timeout=5.0,
    max_retries=3,
)

# Get recommendations
response: RecommendationResponse = client.get_recommendations(
    user_id=12345,
    n=10,
    context=Context(device="mobile"),
    filters={"category": ["electronics", "gadgets"]},
)

print(f"Model version: {response.model_version}")
print(f"Latency: {response.latency_ms:.1f}ms")
for item in response.recommendations:
    print(f"  {item.item_id}: {item.score:.3f}")
```

## Postman Collections

### Collection Structure

```json
{
  "info": {
    "name": "Recommendation Service API",
    "version": "2.3.0",
    "description": "API collection for recommendation endpoints"
  },
  "item": [
    {
      "name": "Get Recommendations",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/recommendations/{{user_id}}?n=10",
        "header": [
          {"key": "X-API-Key", "value": "{{api_key}}"},
          {"key": "Content-Type", "value": "application/json"}
        ]
      },
      "response": []
    }
  ]
}
```

## API Testing Documentation

### Test Coverage Matrix

| Endpoint | Method | Happy Path | Edge Cases | Error Cases | Performance |
|----------|--------|-----------|-----------|-------------|-------------|
| /recommendations/{id} | GET | ✅ | ✅ | ✅ | ✅ |
| /batch | POST | ✅ | ✅ | ✅ | ✅ |
| /model/info | GET | ✅ | — | ✅ | — |
| /health | GET | ✅ | — | — | — |

### Test Categories

| Category | Description | Tools |
|----------|-------------|-------|
| **Unit tests** | Test individual API handlers | pytest |
| **Integration tests** | Test API with database/dependencies | pytest, testcontainers |
| **Contract tests** | Verify API matches OpenAPI spec | Schemathesis, Dredd |
| **Load tests** | Test API under production traffic | Locust, k6 |
| **Chaos tests** | Test API resilience to failures | Chaos Monkey, Litmus |
