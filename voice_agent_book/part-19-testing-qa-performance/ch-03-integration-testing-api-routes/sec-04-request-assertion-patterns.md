# Section 04: Request & Assertion Patterns

## Overview

Consistent request and assertion patterns across API tests improve readability, maintainability, and developer experience. The voice AI platform establishes standard patterns for constructing test requests, validating responses, asserting on common response structures (pagination, errors, status codes), and handling authentication and authorization scenarios.

Request builders simplify the construction of HTTP requests with proper headers, body serialization, and authentication. Response matchers provide type-safe assertions on response bodies, including partial matching, array validation, and nested object verification. Error response assertions validate status codes, error messages, validation details, and error correlation IDs.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Simulator|--->| Utterance|--->| Flow     |--->| Debug    |--->| Report   |
| (in-     |    | Player   |    | Executor |    | Panel    |    | (pass/   |
|  browser)|    | (text/   |    | (step    |    | (log,    |    |  fail    |
|          |    |  audio)  |    |  thru)   |    |  state)  |    |  + trace)|
+----------+    +----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **In-Browser Simulator**: Full conversation simulation with WASM runtime. No backend needed.
- **Utterance Testing**: Pre-defined test utterances with assertions on path and response.
- **Flow Validation**: Graph analysis for unreachable nodes, infinite loops, missing required fields.
## Implementation Approach

```typescript
// Request builder pattern
class ApiRequestBuilder {
  private headers: Record<string, string> = {};
  private queryParams: Record<string, string> = {};
  private requestBody: any;

  constructor(private app: Express.Application) {}

  as(token: string) {
    this.headers['Authorization'] = `Bearer ${token}`;
    return this;
  }

  withHeader(name: string, value: string) {
    this.headers[name] = value;
    return this;
  }

  query(params: Record<string, string | number>) {
    this.queryParams = { ...this.queryParams, ...params } as Record<string, string>;
    return this;
  }

  body(data: any) {
    this.requestBody = data;
    return this;
  }

  async get(url: string) {
    return supertest(this.app)
      .get(url)
      .query(this.queryParams)
      .set(this.headers);
  }

  async post(url: string) {
    return supertest(this.app)
      .post(url)
      .send(this.requestBody)
      .set(this.headers);
  }

  async put(url: string) {
    return supertest(this.app)
      .put(url)
      .send(this.requestBody)
      .set(this.headers);
  }

  async delete(url: string) {
    return supertest(this.app)
      .delete(url)
      .set(this.headers);
  }
}

// Custom response matchers
expect.extend({
  toBePaginated(received: ApiResponse) {
    const { body } = received;
    const pass = body.data && Array.isArray(body.data) &&
      typeof body.total === 'number' &&
      typeof body.page === 'number' &&
      typeof body.limit === 'number';
    return {
      pass,
      message: () => pass
        ? 'Expected response not to be paginated'
        : 'Expected response to be paginated (data[], total, page, limit)',
    };
  },

  toHaveError(received: ApiResponse, expectedCode: string) {
    const { body } = received;
    const pass = body.error?.code === expectedCode;
    return {
      pass,
      message: () => pass
        ? `Expected error not to be ${expectedCode}`
        : `Expected error code ${expectedCode}, got ${body.error?.code}`,
      actual: body.error?.code,
      expected: expectedCode,
    };
  },
});
```

## Integration Points

- **Test Context**: Request builder integrated into test context object
- **Shared Matchers**: Custom matchers registered globally in setup file
- **API Documentation**: Patterns documented in API testing guide
- **Type Generation**: Request/response types generated from OpenAPI schema
- **Test Templates**: Reusable test templates for common API patterns (CRUD)

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Response Size**: Assert on relevant fields only; large response assertions slow tests
- **Error Message Stability**: Don't assert exact error messages; assert error codes instead
- **Header Variability**: Some headers (date, request-id) vary; use property matchers
- **Pagination Consistency**: Ensure pagination behavior is consistent across all list endpoints
- **Cross-Version Testing**: Test API versioning by asserting on correct version headers
