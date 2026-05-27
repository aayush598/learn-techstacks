# Section 08: Integration Testing Strategy

## Overview

Integration testing strategy defines how the platform verifies that adapters work correctly with external APIs, handle errors gracefully, perform within latency budgets, and maintain backward compatibility as APIs evolve. Integration testing is uniquely challenging because it involves external systems that the platform does not control — APIs change without notice, rate limits vary, network conditions fluctuate, and test data must be carefully managed to avoid polluting production systems.

The testing strategy covers multiple levels: unit tests (adapter logic in isolation with mocked HTTP), integration tests (against sandbox/test environments of external APIs), contract tests (validating API request/response schemas match expectations), end-to-end tests (full workflow across multiple integrations), and chaos tests (verifying graceful degradation under failure conditions). The strategy also includes automated regression detection — when an external API changes, the system detects the change and alerts the integration team before the change causes production failures.

## Architecture

```
                  Integration Testing Architecture

   +------------------------------------------------------+
   |              Integration Test Framework               |
   |                                                      |
   |  Test Levels:                                        |
   |  +------------------+  +-------------------------+   |
   |  | Unit Tests       |  | Integration Tests       |   |
   |  | • Mock HTTP      |  | • Sandbox API           |   |
   |  | • Transform      |  | • Test data management  |   |
   |  | • Error handling |  | • Credential management |   |
   |  +------------------+  +-------------------------+   |
   |  +------------------+  +-------------------------+   |
   |  | Contract Tests   |  | End-to-End Tests        |   |
   |  | • Schema         |  | • Full workflow         |   |
   |  |   validation     |  | • Multi-adapter         |   |
   |  | • OpenAPI/SOAP   |  | • Timing-sensitive      |   |
   |  +------------------+  +-------------------------+   |
   |                                                    |
   |  Test Infrastructure:                               |
   |  - WireMock for HTTP stubs                          |
   |  - Test containers for sandbox environments         |
   |  - Snapshot testing for response changes            |
   |  - CI/CD pipeline integration                       |
   +------------------------------------------------------+
```

## Design Decisions

- **Contract testing as the primary API change detection mechanism:** Contract tests validate that the platform's API requests match the external API's expected schema and that responses match the platform's expected schema. Contracts are stored as OpenAPI specifications for REST APIs, WSDL for SOAP APIs, and GraphQL schemas for GraphQL APIs. When a contract test fails (schema mismatch), the system generates a detailed diff showing what changed and which adapters are affected. Trade-off: contract tests only detect structural changes, not behavioral changes (same schema but different semantics).

- **Sandbox-first testing with production shadow mode:** All integration tests run against sandbox/test environments by default. Critical integrations additionally run in "shadow mode" in production — requests are duplicated to the production API but the responses are only logged, not acted upon. This detects issues that only manifest in production (rate limits, network topology, authentication differences) without risking production data. Trade-off: shadow mode doubles API call volume, which may exceed rate limits or incur additional costs.

- **Snapshot-based regression detection for response changes:** Integration tests capture API responses as snapshots and compare them on subsequent runs. Any change to the response structure or values (within allowed tolerance) is flagged for review. This detects silent API changes that don't break schemas but change behavior — for example, a field that previously always returned a value now sometimes returns null. Trade-off: snapshot tests are brittle and require frequent baseline updates for APIs with dynamic response data.

## Implementation Approach

```
interface IntegrationTestConfig {
  adapterType: string;
  testEnvironment: 'sandbox' | 'staging' | 'shadow';
  testData: {
    setupScript?: string;    // Script to create test data in sandbox
    cleanupScript?: string;  // Script to remove test data
    requiredEntities: string[];
  };
  contractValidation: {
    schemaPath: string;      // Path to OpenAPI/WSDL schema
    strictMode: boolean;     // Reject unknown fields
  };
  performance: {
    latencyThresholds: { p50: number; p95: number; p99: number };
    throughputTarget: number;
  };
}

class IntegrationTestRunner {
  async runAdapterTests(adapterType: string, config: IntegrationTestConfig): Promise<TestResults> {
    const results: TestResult[] = [];

    // Unit tests (no external dependency)
    results.push(await this.runUnitTests(adapterType));

    // Contract tests
    const contractSchema = await this.loadContractSchema(config.contractValidation.schemaPath);
    results.push(await this.runContractTests(adapterType, contractSchema, config));

    // Integration tests (against sandbox)
    if (config.testEnvironment === 'sandbox') {
      await this.setupTestData(config);
      results.push(await this.runSandboxTests(adapterType, config));
      await this.cleanupTestData(config);
    }

    // Performance tests
    results.push(await this.runPerformanceTests(adapterType, config));

    return this.aggregateResults(results);
  }

  async runContractTests(adapterType: string, schema: any, config: IntegrationTestConfig): Promise<TestResult> {
    const requestValidator = this.buildRequestValidator(schema);
    const responseValidator = this.buildResponseValidator(schema);

    const testCases = this.getTestCases(adapterType);
    const failures = [];

    for (const testCase of testCases) {
      const request = await this.buildRequest(testCase);
      const requestErrors = requestValidator.validate(request);
      if (requestErrors.length > 0) {
        failures.push({ testCase: testCase.name, type: 'request', errors: requestErrors });
      }

      if (config.testEnvironment !== 'sandbox') continue;

      try {
        const response = await this.executeRealRequest(request);
        const responseErrors = responseValidator.validate(response);
        if (responseErrors.length > 0) {
          failures.push({ testCase: testCase.name, type: 'response', errors: responseErrors });
        }
      } catch (error) {
        failures.push({ testCase: testCase.name, type: 'error', error: error.message });
      }
    }

    return {
      suite: `${adapterType} contract tests`,
      passed: testCases.length - failures.length,
      failed: failures.length,
      failures
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Jest** (MIT) | Testing | Test framework |
| **WireMock** (Apache 2.0) | Stubbing | HTTP stub server |
| **Testcontainers** (MIT) | Containers | Integration test environments |
| **OpenAPI Enforcer** (MIT) | Validation | API contract enforcement |
| **Playwright** (Apache 2.0) | Testing | E2E test automation |

## Production Considerations

**Scaling:** Integration tests should run in parallel across adapter types. Use test sharding in CI/CD to distribute tests across multiple runners. Maintain a test data pool (pre-created test records in sandboxes) to avoid test setup delays. For sandbox rate limits, stagger test execution across time windows.

**Security:** Test credentials should be distinct from production credentials with restricted access. Test data should be clearly marked (test flag, specific domain names, identifiable patterns) to prevent confusion with real data. Never use production data in sandbox tests. Rotate test credentials regularly.

**Monitoring:** Track test suite execution time, flaky test rate (tests that fail intermittently), sandbox availability during test execution, contract test failure rate (detects API changes), and time to detect API breaking changes. Alert on contract test failures that suggest an API breaking change requiring adapter updates.
