# Input Validation

## 1. Overview

Input validation is the first line of defense against injection attacks, data corruption,
and unexpected behavior in recommendation system APIs. Every piece of data entering the
system must be validated before processing. This document covers schema validation, type
checking, length limits, range validation, regex patterns, and injection prevention for
SQL, XSS, and command injection.

### 1.1 Input Validation Principles

| Principle | Description | Implementation |
|---|---|---|
| Deny by default | Reject unknown inputs | Allowlist approach |
| Validate early | Check at system boundary | API gateway validation |
| Validate thoroughly | Check all aspects | Multi-layer validation |
| Never trust client | All client input is suspect | Server-side validation |
| Fail safely | Invalid input → reject, not process | Error handling |

---

## 2. Schema Validation

### 2.1 Request Schema Validation

Validate entire request structure before processing:

```json
{
  "type": "object",
  "required": ["user_id", "context"],
  "properties": {
    "user_id": {
      "type": "string",
      "pattern": "^usr_[a-f0-9]{16}$",
      "maxLength": 50
    },
    "context": {
      "type": "object",
      "required": ["device"],
      "properties": {
        "device": {
          "type": "string",
          "enum": ["mobile", "desktop", "tablet"]
        },
        "timestamp": {
          "type": "string",
          "format": "date-time"
        }
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
```

### 2.2 Response Schema Validation

Validate outbound responses in development/testing:

- Ensure responses match OpenAPI specification
- Verify no sensitive data leaked in responses
- Check response size within limits
- Validate content-type header matches body

### 2.3 Schema Validation Tools

| Tool | Use Case | Language |
|---|---|---|
| JSON Schema | JSON request/response validation | Any |
| OpenAPI validator | API spec compliance | Any |
| Protobuf | gRPC message validation | Any |
| Pydantic | Python model validation | Python |
| Zod | TypeScript schema validation | TypeScript |
| Joi | Node.js validation | JavaScript |

---

## 3. Type Checking

### 3.1 Type Validation Rules

| Type | Validation | Example |
|---|---|---|
| Integer | Is integer, within int32/int64 range | `count: 20` |
| Float | Is number, within float range, not NaN/Inf | `score: 0.85` |
| String | Is string, correct encoding (UTF-8) | `name: "John"` |
| Boolean | Is boolean (not "true" string) | `active: true` |
| Array | Is array, elements correct type | `tags: ["a", "b"]` |
| Object | Is object, required fields present | `{user_id: "..."}` |
| Null | Explicitly allowed only where expected | `middle_name: null` |
| Date/Time | Valid ISO 8601 format | `2026-01-15T10:30:00Z` |

### 3.2 Type Coercion Risks

| Risk | Example | Prevention |
|---|---|---|
| String to number | `"1; DROP TABLE"` as number | Reject non-numeric strings |
| Number to string | `123` as `"123"` for string comparison | Strict type checking |
| Boolean confusion | `"false"` (truthy) vs `false` (falsy) | Reject string booleans |
| Array vs object | `[]` vs `{}` confusion | Schema validation |

---

## 4. Length Limits

### 4.1 Field Length Limits

| Field Type | Maximum Length | Rationale |
|---|---|---|
| User ID | 50 characters | Prevent buffer overflow |
| Email | 254 characters | RFC 5321 limit |
| Name | 200 characters | Reasonable name length |
| Search query | 500 characters | Prevent abuse |
| API key | 100 characters | Standard key length |
| Comment/review | 5000 characters | Content limit |
| URL | 2048 characters | Browser URL limit |
| File upload | 10 MB | Reasonable file size |

### 4.2 Request Size Limits

| Endpoint Type | Maximum Size | Rationale |
|---|---|---|
| GET request | 8 KB (URL + headers) | Standard HTTP limit |
| POST JSON | 1 MB | Reasonable payload |
| File upload | 10 MB | Content limit |
| Batch request | 10 MB | Bulk operation limit |
| WebSocket message | 64 KB | Real-time message limit |

---

## 5. Range Validation

### 5.1 Numeric Range Validation

| Field | Min | Max | Rationale |
|---|---|---|---|
| Recommendation count | 1 | 100 | Reasonable request size |
| Page offset | 0 | 10000 | Prevent deep pagination |
| Rating | 1 | 5 | Standard rating scale |
| Confidence score | 0.0 | 1.0 | Probability range |
| Price | 0.00 | 1000000 | Reasonable price range |
| Age | 0 | 150 | Human age range |

### 5.2 Date Range Validation

| Scenario | Validation | Example |
|---|---|---|
| Historical query | Start < End, within retention | `start: 2025-01-01, end: 2026-01-15` |
| Future query | Not in future | `date: 2026-01-15` (today) |
| Time window | Duration within limits | `window: 30d` (max 365d) |
| Timestamp precision | Correct format | ISO 8601 with timezone |

---

## 6. Regex Patterns

### 6.1 Common Validation Patterns

| Field | Pattern | Description |
|---|---|---|
| User ID | `^usr_[a-f0-9]{16}$` | User identifier format |
| Email | `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` | Email format |
| UUID | `^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$` | UUID v4 |
| Date | `^\d{4}-\d{2}-\d{2}$` | ISO date format |
| Phone | `^\+?[1-9]\d{1,14}$` | E.164 phone format |
| Alphanumeric | `^[a-zA-Z0-9]+$` | Letters and numbers only |

### 6.2 Regex Security

| Risk | Description | Prevention |
|---|---|---|
| ReDoS | Regex denial of service | Avoid nested quantifiers |
| Backtracking | Catastrophic backtracking | Test with worst-case inputs |
| Bypass | Malformed input passes regex | Use allowlist, not blocklist |
| Unicode bypass | Unicode characters bypass regex | Use Unicode-aware regex |

### 6.3 Safe Regex Practices

- **Use allowlist patterns**: Match what IS valid, not what ISN'T
- **Test for ReDoS**: Run regex against worst-case inputs
- **Limit input before regex**: Apply length limits before regex matching
- **Use non-backtracking engines**: RE2 or similar when available
- **Compile once, use many**: Pre-compile regex patterns

---

## 7. Injection Prevention

### 7.1 SQL Injection Prevention

| Technique | Implementation | Priority |
|---|---|---|
| Parameterized queries | Use prepared statements | Critical |
| ORM usage | Never construct raw SQL | High |
| Stored procedures | Encapsulate DB logic | Medium |
| Input validation | Validate before query | High |
| Least privilege | DB user has minimal permissions | Critical |

### 7.2 XSS Prevention

| Technique | Implementation | Priority |
|---|---|---|
| Output encoding | HTML, JavaScript, URL encoding | Critical |
| Content Security Policy | Restrict script sources | High |
| Input validation | Sanitize before storage | High |
| HttpOnly cookies | Prevent JavaScript access | High |
| Trusted types | Prevent DOM injection | Medium |

### 7.3 Command Injection Prevention

| Technique | Implementation | Priority |
|---|---|---|
| Avoid shell commands | Use language-native APIs | Critical |
| Input sanitization | Remove shell metacharacters | High |
| Parameterized execution | Use exec with argument arrays | High |
| Sandboxing | Run with minimal privileges | Medium |

### 7.4 NoSQL Injection Prevention

| Technique | Implementation | Priority |
|---|---|---|
| Schema validation | Validate document structure | Critical |
| Query parameterization | Use driver query builders | High |
| Input type checking | Ensure expected types | High |
| Query limits | Limit result set size | Medium |

---

## 8. Validation Testing

### 8.1 Validation Test Categories

| Test Type | Description | Tool |
|---|---|---|
| Fuzz testing | Random malformed input | AFL, libFuzzer |
| Boundary testing | Min/max/edge values | Custom test suite |
| Injection testing | SQL, XSS, command injection | OWASP ZAP, Burp Suite |
| Schema testing | Invalid JSON, missing fields | Custom test suite |
| Encoding testing | Unicode, special characters | Custom test suite |

### 8.2 Validation Test Automation

- **Unit tests**: Test individual validation functions
- **Integration tests**: Test validation in API context
- **Security scans**: Automated vulnerability scanning
- **Penetration testing**: Manual security testing quarterly
- **Fuzz testing**: Continuous fuzzing in CI pipeline
