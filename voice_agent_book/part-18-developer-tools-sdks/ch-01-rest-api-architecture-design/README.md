# Chapter 01: REST API Architecture & Design

> **Part:** 18 - Developer Tools, SDKs & API Layer

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [RESTful Design Principles](sec-01-restful-design-principles.md) | Resource-oriented design, HTTP method semantics, statelessness, HATEOAS, uniform interface |
| 02 | [Resource Naming Conventions](sec-02-resource-naming-conventions.md) | Plural nouns, hierarchical relationships, consistency patterns, URL structure best practices |
| 03 | [Pagination & Filtering](sec-03-pagination-filtering.md) | Cursor vs offset pagination, sorting, field selection, complex filtering, search syntax |
| 04 | [API Versioning Strategy](sec-04-api-versioning-strategy.md) | URL versioning, header versioning, backward compatibility, deprecation policy, sunset headers |
| 05 | [Error Response Format](sec-05-error-response-format.md) | Standard error envelope, error codes, error details, validation errors, rate limit errors |
| 06 | [Request Validation](sec-06-request-validation.md) | Zod/ Yup schemas, input sanitization, type coercion, idempotency enforcement |
| 07 | [API Rate Limiting](sec-07-api-rate-limiting.md) | Rate limit algorithms (token bucket, leaky bucket), distributed enforcement, rate limit headers |
| 08 | [API Documentation Standards](sec-08-api-documentation-standards.md) | OpenAPI 3.1 specification, operation IDs, response examples, API changelog, documentation generation |

---

## RESTful URL Structure

```
# Collection
GET    /v1/agents                # List agents
POST   /v1/agents                # Create agent

# Resource
GET    /v1/agents/:id            # Get agent
PATCH  /v1/agents/:id            # Update agent
DELETE /v1/agents/:id            # Delete agent

# Sub-collection
GET    /v1/agents/:id/calls      # List agent's calls
POST   /v1/agents/:id/calls      # Create call for agent

# Actions
POST   /v1/agents/:id/deploy     # Action (non-CRUD)
POST   /v1/calls/:id/transfer    # Action
```

---

## Learning Objectives

- Apply RESTful design principles to voice agent API
- Design consistent resource naming conventions
- Implement cursor-based pagination with filtering
- Define API versioning strategy with deprecation policy
- Create standard error response format
- Build request validation with Zod schemas
- Implement distributed rate limiting
- Generate OpenAPI documentation from code
