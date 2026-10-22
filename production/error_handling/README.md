# Production-Grade Error Handling Architecture for SaaS Applications

A complete, reusable curriculum and reference for designing error handling that survives
real production: multi-tenant SaaS, distributed systems, payments, background jobs, and
AI/LLM features.

**Learning objective.** Build a reusable, scalable, maintainable error-handling system that can
be applied across multiple SaaS projects, from an early-stage startup to a large-scale
production application.

**Scope boundary.** This resource is about **error handling only**. Logging, monitoring,
tracing, metrics, alerting, testing strategy, CI/CD, and deployment architecture are out of
scope except where they directly shape error-handling design (for example: what information an
error must carry so those systems can consume it). Error handling defines *what* is available;
those systems implement *how* it is observed.

**End goal.** A reusable error-handling **standard**, not a massive framework. The standard
should make routine errors straightforward, unusual failures explicit, and critical failures
safe and predictable — without redesigning error handling for every new SaaS project.

---

## How to read this resource

- Start with [`_STYLE_GUIDE.md`](./_STYLE_GUIDE.md) if you are contributing or editing.
- Start with [`GLOSSARY.md`](./GLOSSARY.md) to lock down vocabulary.
- Every part has a `README.md`; every chapter has a `README.md` that indexes its files.
- Every chapter is split into five subfolders: `01-concepts`, `02-deep-dive`,
  `03-practical-examples`, `04-dos-and-donts`, `05-reference`.
- A recurring cast of examples (`Acme SaaS`, `Checkout`, `ExportJob`, `WebhookIngest`,
  `AgentRun`) runs through the whole book so ideas connect. See the style guide §5.
- Follow the recommended learning sequence at the bottom to avoid advanced abstractions before
  fundamentals.

---

## Recommended learning sequence

| Phase | Chapters | Primary objective |
| ----- | -------- | ----------------- |
| 1. Foundations | 1–3 | Understand error semantics and design principles |
| 2. Error modeling | 4–8 | Establish a consistent taxonomy, types, and codes |
| 3. Architecture | 9–16 | Control error propagation, boundaries, and translation |
| 4. Application behavior | 17–24 | Handle validation, business logic, APIs, and persistence |
| 5. Resilience | 25–33 | Handle dependencies, retries, concurrency, and async failures |
| 6. Security & full stack | 34–38 | Prevent leakage; align client and server behavior |
| 7. Advanced reliability | 39–44 | Handle partial failures and specialized SaaS workflows |
| 8. Maintainability | 45–55 | Create reusable, consistent error-handling infrastructure |
| 9. Advanced decisions | 56–58 | Evaluate trade-offs and unusual failure modes |
| 10. Standardization | 59–62 | Build a repeatable blueprint for future projects |

---

## Table of contents

### [Part I — Foundations of Production-Grade Error Handling](./part-01-foundations/README.md)
- [1. Understanding Errors and Failures](./part-01-foundations/01-understanding-errors-and-failures/README.md)
- [2. Principles of High-Quality Error Handling](./part-01-foundations/02-principles-of-high-quality-error-handling/README.md)
- [3. Error-Handling Requirements for a SaaS Product](./part-01-foundations/03-error-handling-requirements-for-saas/README.md)

### [Part II — Error Taxonomy and Classification](./part-02-error-taxonomy/README.md)
- [4. Designing a Comprehensive Error Taxonomy](./part-02-error-taxonomy/04-designing-a-comprehensive-error-taxonomy/README.md)
- [5. Error Categories in Detail](./part-02-error-taxonomy/05-error-categories-in-detail/README.md)

### [Part III — Error Models and Representation](./part-03-error-models/README.md)
- [6. Designing the Application's Error Model](./part-03-error-models/06-designing-the-applications-error-model/README.md)
- [7. Error Classes, Types, and Structured Results](./part-03-error-models/07-error-classes-types-and-structured-results/README.md)
- [8. Error Codes and Error Registries](./part-03-error-models/08-error-codes-and-error-registries/README.md)

### [Part IV — Error-Handling Architecture and System Boundaries](./part-04-architecture/README.md)
- [9. Designing a Layered Error-Handling Architecture](./part-04-architecture/09-layered-error-handling-architecture/README.md)
- [10. Centralized and Distributed Error Handling](./part-04-architecture/10-centralized-and-distributed-error-handling/README.md)
- [11. The Error Lifecycle](./part-04-architecture/11-the-error-lifecycle/README.md)

### [Part V — Exception Handling Mechanics](./part-05-exception-mechanics/README.md)
- [12. Exception Propagation and Control Flow](./part-05-exception-mechanics/12-exception-propagation-and-control-flow/README.md)
- [13. Catch Blocks and Recovery Logic](./part-05-exception-mechanics/13-catch-blocks-and-recovery-logic/README.md)
- [14. Resource Cleanup and Failure-Safe Execution](./part-05-exception-mechanics/14-resource-cleanup-and-failure-safe-execution/README.md)

### [Part VI — Error Boundaries and Translation](./part-06-boundaries-and-translation/README.md)
- [15. Error Boundaries](./part-06-boundaries-and-translation/15-error-boundaries/README.md)
- [16. Error Translation and Normalization](./part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)

### [Part VII — Input Validation and Business Errors](./part-07-validation-and-business-errors/README.md)
- [17. Input Validation Error Handling](./part-07-validation-and-business-errors/17-input-validation-error-handling/README.md)
- [18. Domain and Business Logic Errors](./part-07-validation-and-business-errors/18-domain-and-business-logic-errors/README.md)

### [Part VIII — HTTP and API Error Handling](./part-08-http-and-api/README.md)
- [19. HTTP Error Semantics](./part-08-http-and-api/19-http-error-semantics/README.md)
- [20. Standardized API Error Responses](./part-08-http-and-api/20-standardized-api-error-responses/README.md)
- [21. API Boundary and Middleware Error Handling](./part-08-http-and-api/21-api-boundary-and-middleware-error-handling/README.md)

### [Part IX — Database, Persistence, and Transaction Errors](./part-09-database-and-transactions/README.md)
- [22. Database Error Classification](./part-09-database-and-transactions/22-database-error-classification/README.md)
- [23. Transaction and Rollback Error Handling](./part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
- [24. Repository and Data Access Error Handling](./part-09-database-and-transactions/24-repository-and-data-access-error-handling/README.md)

### [Part X — External Dependencies and Integration Errors](./part-10-external-dependencies/README.md)
- [25. Third-Party API Error Handling](./part-10-external-dependencies/25-third-party-api-error-handling/README.md)
- [26. Network and Distributed Communication Errors](./part-10-external-dependencies/26-network-and-distributed-communication-errors/README.md)

### [Part XI — Retry Logic and Resilience](./part-11-retry-and-resilience/README.md)
- [27. Retry Policies](./part-11-retry-and-resilience/27-retry-policies/README.md)
- [28. Idempotency and Duplicate-Operation Safety](./part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [29. Timeouts, Circuit Breakers, and Bulkheads](./part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [30. Graceful Degradation and Fallbacks](./part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)

### [Part XII — Asynchronous Processing and Background Jobs](./part-12-async-and-background-jobs/README.md)
- [31. Asynchronous Error Handling](./part-12-async-and-background-jobs/31-asynchronous-error-handling/README.md)
- [32. Background Jobs, Queues, and Scheduled Tasks](./part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
- [33. Events, Webhooks, and Message Processing](./part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)

### [Part XIII — Security-Aware Error Handling](./part-13-security-aware/README.md)
- [34. Security Principles for Error Handling](./part-13-security-aware/34-security-principles-for-error-handling/README.md)
- [35. Authentication, Authorization, and Tenant Isolation Errors](./part-13-security-aware/35-auth-authorization-and-tenant-isolation-errors/README.md)
- [36. Sensitive Data and Error Context](./part-13-security-aware/36-sensitive-data-and-error-context/README.md)

### [Part XIV — Frontend and Full-Stack Error Handling](./part-14-frontend-and-full-stack/README.md)
- [37. Frontend Error Handling](./part-14-frontend-and-full-stack/37-frontend-error-handling/README.md)
- [38. Full-Stack Error Contracts](./part-14-frontend-and-full-stack/38-full-stack-error-contracts/README.md)

### [Part XV — Advanced Distributed-System Failure Handling](./part-15-distributed-failures/README.md)
- [39. Partial Failures and Multi-Step Operations](./part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)
- [40. Consistency and Concurrency Failures](./part-15-distributed-failures/40-consistency-and-concurrency-failures/README.md)
- [41. Process, Runtime, and Resource Failures](./part-15-distributed-failures/41-process-runtime-and-resource-failures/README.md)

### [Part XVI — Specialized SaaS Error Scenarios](./part-16-specialized-saas-scenarios/README.md)
- [42. Authentication, Billing, and Subscription Workflows](./part-16-specialized-saas-scenarios/42-auth-billing-and-subscription-workflows/README.md)
- [43. File and Media Processing Errors](./part-16-specialized-saas-scenarios/43-file-and-media-processing-errors/README.md)
- [44. AI, LLM, and Tool-Calling Application Errors](./part-16-specialized-saas-scenarios/44-ai-llm-and-tool-calling-application-errors/README.md)

### [Part XVII — Error Handling in Architecture and Code Organization](./part-17-organization/README.md)
- [45. Organizing Error-Handling Modules](./part-17-organization/45-organizing-error-handling-modules/README.md)
- [46. Error-Handling Patterns and Anti-Patterns](./part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)

### [Part XVIII — Error Handling Across Languages and Frameworks](./part-18-languages-and-frameworks/README.md)
- [47. Language-Level Error Semantics](./part-18-languages-and-frameworks/47-language-level-error-semantics/README.md)
- [48. Framework and Runtime Integration](./part-18-languages-and-frameworks/48-framework-and-runtime-integration/README.md)

### [Part XIX — Error Contracts, Compatibility, and Governance](./part-19-contracts-and-governance/README.md)
- [49. Error Contract Design and Versioning](./part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)
- [50. Error Handling as an Engineering Standard](./part-19-contracts-and-governance/50-error-handling-as-an-engineering-standard/README.md)

### [Part XX — Error-Handling Correctness and Validation](./part-20-correctness-and-validation/README.md)
- [51. Correctness Properties of Error Handling](./part-20-correctness-and-validation/51-correctness-properties-of-error-handling/README.md)
- [52. Failure-Path Analysis](./part-20-correctness-and-validation/52-failure-path-analysis/README.md)

### [Part XXI — Error Handling for Maintainability and Developer Productivity](./part-21-maintainability/README.md)
- [53. Reducing Error-Handling Complexity](./part-21-maintainability/53-reducing-error-handling-complexity/README.md)
- [54. Reusable Error-Handling Infrastructure](./part-21-maintainability/54-reusable-error-handling-infrastructure/README.md)
- [55. Error-Handling Documentation](./part-21-maintainability/55-error-handling-documentation/README.md)

### [Part XXII — Advanced Error-Handling Design Decisions](./part-22-design-decisions/README.md)
- [56. Choosing Between Competing Approaches](./part-22-design-decisions/56-choosing-between-competing-approaches/README.md)
- [57. Error Handling Under Load and at Scale](./part-22-design-decisions/57-error-handling-under-load-and-at-scale/README.md)

### [Part XXIII — Special Cases and Frequently Overlooked Failure Modes](./part-23-special-cases/README.md)
- [58. Less Obvious Error-Handling Scenarios](./part-23-special-cases/58-less-obvious-error-handling-scenarios/README.md)

### [Part XXIV — Building a Repeatable Error-Handling Blueprint](./part-24-repeatable-blueprint/README.md)
- [59. Defining the Standard Error-Handling Blueprint](./part-24-repeatable-blueprint/59-defining-the-standard-error-handling-blueprint/README.md)
- [60. Applying the Blueprint to Different SaaS Architectures](./part-24-repeatable-blueprint/60-applying-the-blueprint-to-different-saas-architectures/README.md)
- [61. Error-Handling Maturity Model](./part-24-repeatable-blueprint/61-error-handling-maturity-model/README.md)
- [62. Final Reference Materials](./part-24-repeatable-blueprint/62-final-reference-materials/README.md)

---

## The recurring cast

| Name | What it is | Used to teach |
| ---- | ---------- | ------------- |
| **Acme SaaS** | Multi-tenant B2B project-management tool (REST, Postgres, Redis, Stripe, S3, queue workers, LLM summaries) | Layering, tenancy, API contracts |
| **Checkout** | Subscription/payment workflow | Idempotency, partial failure, sagas |
| **ExportJob** | Long-running data export on a queue | Retries, dead-letter, checkpointing |
| **WebhookIngest** | Inbound Stripe webhooks | Signature checks, duplicates, replays |
| **AgentRun** | LLM tool-calling agent | Provider errors, token limits, tool failures |

---

## The five defining questions

Whenever you design or review error handling, answer these five questions. The entire book is
organized around helping you answer them well:

1. **What can fail here?** (taxonomy, failure-path analysis)
2. **What does each failure mean?** (error model, codes, classification)
3. **Where is it caught, translated, or propagated?** (boundaries, layers, lifecycle)
4. **What is the safe outcome?** (retry, fallback, compensation, terminate)
5. **What does the outside world see, and can it act on it?** (API/error contracts, security)

---

## Contributing / editing

1. Read [`_STYLE_GUIDE.md`](./_STYLE_GUIDE.md).
2. Match the file anatomy exactly; reuse the recurring cast.
3. Keep links relative and verify they resolve.
4. Add new vocabulary to [`GLOSSARY.md`](./GLOSSARY.md).
