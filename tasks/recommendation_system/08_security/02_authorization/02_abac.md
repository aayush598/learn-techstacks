# Attribute-Based Access Control (ABAC)

## 1. Overview

Attribute-Based Access Control (ABAC) is an authorization model that evaluates access
decisions based on attributes of the requestor, the resource, the action, and the
environment. For recommendation systems, ABAC provides fine-grained access control that
can adapt to complex multi-tenant, multi-role, and context-dependent authorization
scenarios that RBAC alone cannot handle.

### 1.1 ABAC vs RBAC Comparison

| Aspect | RBAC | ABAC |
|---|---|---|
| Decision basis | Role membership | Attribute combinations |
| Granularity | Coarse (role-level) | Fine-grained (attribute-level) |
| Flexibility | Static role hierarchy | Dynamic policy evaluation |
| Scalability | Limited by role explosion | Scales with attribute combinations |
| Context awareness | No | Yes (environment attributes) |
| Policy management | Simple | Complex but powerful |
| Performance | Fast (role lookup) | Moderate (policy evaluation) |

### 1.2 When to Use ABAC in Recommendation Systems

- Multi-tenant access control with different policies per tenant
- Context-dependent access (time-of-day, location, device)
- Data-level access control (which features, which models)
- Dynamic permission changes based on user attributes
- Complex compliance requirements (GDPR, CCPA)

---

## 2. Policy Definitions

### 2.1 Policy Language Structure

ABAC policies are expressed as conditions over attributes:

```
Policy Structure:
├── Subject Attributes: Who is requesting (user, service, role)
├── Resource Attributes: What is being accessed (endpoint, data, model)
├── Action Attributes: What operation (read, write, deploy)
├── Environment Attributes: Context (time, location, risk level)
└── Effect: Permit or Deny
```

### 2.2 Policy Examples

**Example 1: Model deployment access**

```
Policy: deploy_model
Effect: Permit
Subject: role == "ml_engineer" AND team == "recommendation"
Resource: type == "model" AND environment == "production"
Action: action == "deploy"
Environment: time BETWEEN "09:00" AND "17:00" AND day IN ["mon","tue","wed","thu","fri"]
Condition: approval_count >= 2
```

**Example 2: Feature data access**

```
Policy: read_features
Effect: Permit
Subject: role IN ["data_scientist", "ml_engineer"]
Resource: type == "feature" AND classification IN ["public", "internal"]
Action: action == "read"
Environment: ip_in_vpn == true
Condition: project membership verified
```

**Example 3: Multi-tenant recommendation data**

```
Policy: tenant_data_access
Effect: Permit
Subject: tenant_id == resource.tenant_id
Resource: type == "recommendation_data"
Action: action IN ["read", "write"]
Environment: always
Condition: account_status == "active"
```

### 2.3 Policy Decision Matrix

| Subject Role | Resource Type | Action | Environment | Effect |
|---|---|---|---|---|
| Admin | Any | Any | Any | Permit |
| ML Engineer | Model | Deploy | Business hours | Permit |
| ML Engineer | Model | Deploy | After hours | Deny |
| Data Scientist | Feature | Read | VPN only | Permit |
| Data Scientist | Feature | Write | Any | Deny |
| Partner | Recommendation | Read | Any | Permit (rate limited) |
| Anonymous | Recommendation | Read | Any | Deny |

---

## 3. Attribute Categories

### 3.1 Subject Attributes

| Attribute | Type | Source | Example |
|---|---|---|---|
| user_id | string | Authentication | `usr_a1b2c3` |
| role | set | Role service | `["ml_engineer", "data_scientist"]` |
| team | string | Organization service | `recommendation` |
| tenant_id | string | Authentication | `tenant_acme` |
| clearance_level | integer | Security service | `3` |
| account_status | enum | User service | `active` |
| mfa_verified | boolean | Auth service | `true` |
| last_password_change | timestamp | Auth service | `2026-01-01` |

### 3.2 Resource Attributes

| Attribute | Type | Source | Example |
|---|---|---|---|
| resource_type | enum | System | `model`, `feature`, `data` |
| environment | enum | Configuration | `production`, `staging` |
| classification | enum | Data governance | `public`, `internal`, `confidential` |
| owner | string | Metadata | `team_recommendation` |
| tenant_id | string | Resource metadata | `tenant_acme` |
| region | string | Resource config | `us-east-1` |
| version | string | Resource version | `v2.3.1` |

### 3.3 Action Attributes

| Attribute | Type | Description |
|---|---|---|
| action_type | enum | `read`, `write`, `delete`, `deploy` |
| batch | boolean | Whether operation is batch |
| scope | string | Specific scope of action |
| target_count | integer | Number of resources affected |

### 3.4 Environment Attributes

| Attribute | Type | Source | Example |
|---|---|---|---|
| time_of_day | time | System clock | `14:30:00` |
| day_of_week | enum | System clock | `monday` |
| ip_address | string | Request | `192.168.1.100` |
| ip_in_vpn | boolean | Network service | `true` |
| risk_score | float | Risk engine | `0.15` |
| mfa_level | enum | Auth service | `strong` |
| device_trust | enum | Device service | `managed` |

---

## 4. Policy Enforcement Points (PEP)

### 4.1 PEP Architecture

```
Client Request → PEP (Enforcement) → PDP (Decision) → PIP (Data) → Resource
                      ↓                    ↓                ↓
                 Intercepts          Evaluates policy    Fetches
                 all requests        against attributes  attributes
```

### 4.2 PEP Implementation

The Policy Enforcement Point intercepts every API request:

| PEP Location | Scope | Implementation |
|---|---|---|
| API Gateway | All external requests | Middleware plugin |
| Service mesh | Service-to-service | Sidecar proxy (Envoy) |
| Application layer | Specific endpoints | Framework middleware |
| Data layer | Data access | Database proxy |

### 4.3 PEP Decision Flow

```
Request arrives at PEP
    ↓
Extract subject attributes (from JWT/session)
    ↓
Extract resource attributes (from request path/body)
    ↓
Extract action attributes (from HTTP method)
    ↓
Extract environment attributes (from context)
    ↓
Send all attributes to PDP
    ↓
PDP evaluates policies
    ↓
┌───┴───┐
│ Permit│ → Forward request to resource
│ Deny  │ → Return 403 Forbidden
│ Error │ → Return 500 Internal Server Error
└───────┘
```

### 4.4 PEP Performance Considerations

- **Attribute caching**: Cache attribute lookups for repeated requests
- **Async evaluation**: Non-blocking policy evaluation where possible
- **Fail-closed**: Deny on PDP unavailability (configurable)
- **Decision caching**: Cache decisions for identical attribute combinations
- **Timeout handling**: PDP timeout → deny with alert

---

## 5. Policy Decision Point (PDP)

### 5.1 PDP Architecture

The PDP evaluates policies against provided attributes and returns a decision.

| Component | Responsibility |
|---|---|
| Policy store | Stores all active policies |
| Policy engine | Evaluates policies against attributes |
| Decision cache | Caches decisions for performance |
| Audit logger | Logs all decisions for compliance |

### 5.2 Policy Evaluation Algorithm

```
1. Collect all applicable policies for the resource type
2. Evaluate each policy against provided attributes
3. Collect all Permit and Deny decisions
4. Apply conflict resolution:
   a. Deny overrides (Deny always wins)
   b. Or: First-applicable (first matching policy)
   c. Or: Priority-based (highest priority policy wins)
5. Return final decision with matched policy ID
```

### 5.3 PDP Performance

| Metric | Target | Measurement |
|---|---|---|
| Decision latency | < 5ms | p99 latency |
| Throughput | > 100K decisions/second | Sustained load |
| Cache hit rate | > 90% | Monitoring |
| Policy evaluation time | < 1ms | Per policy evaluation |

---

## 6. Policy Information Point (PIP)

### 6.1 PIP Responsibilities

The PIP fetches attribute values from external data sources when not available in the request.

| Attribute Source | PIP Implementation |
|---|---|
| User profile | REST API call to user service |
| Team membership | LDAP/AD query |
| Resource metadata | Database query |
| Risk score | Risk engine API call |
| Device trust | Device management API |
| Network info | Network service API |

### 6.2 PIP Caching Strategy

- **Attribute TTL**: Cache each attribute type with appropriate TTL
- **Refresh on miss**: Fetch from source on cache miss
- **Stale-on-error**: Return stale cached value on PIP failure
- **Pre-fetching**: Pre-fetch attributes for known request patterns

---

## 7. Attribute Management

### 7.1 Attribute Lifecycle

```
Attribute Definition → Attribute Assignment → Attribute Evaluation → Attribute Audit
        ↓                      ↓                      ↓                   ↓
    Define schema        Assign to subjects      Use in policies      Track changes
    Define types         Assign to resources     Log decisions        Compliance report
    Define source        Update on change        Detect drift         Retention policy
```

### 7.2 Attribute Governance

| Governance Aspect | Requirement | Implementation |
|---|---|---|
| Attribute accuracy | Attributes reflect current state | Regular validation |
| Attribute completeness | All required attributes available | Coverage monitoring |
| Attribute freshness | Attributes updated within SLA | Staleness detection |
| Attribute consistency | Same attribute value across systems | Cross-system reconciliation |
| Attribute audit | All changes tracked | Change audit log |

### 7.3 ABAC Policy Testing

| Test Type | Description | Frequency |
|---|---|---|
| Unit test | Policy evaluates correctly for specific attributes | Per policy change |
| Integration test | PEP correctly intercepts and enforces | Per deployment |
| Regression test | Existing access patterns not broken | Per policy change |
| Penetration test | Unauthorized access attempts blocked | Quarterly |
| Audit test | All decisions logged correctly | Monthly |
