# Section 03: Cross-Tenant Data Isolation

Cross-tenant data isolation prevents one tenant from accessing another tenant's data through API requests. The isolation architecture relies on the tenant ID extracted from authentication and enforced at every data access layer. No API endpoint should return data from a different tenant than the authenticated one.

The enforcement chain: API gateway validates tenant ID from token, controller extracts tenant context from request, service layer adds tenant ID to all database queries, ORM/query builder applies tenant filter automatically, object storage paths include tenant prefix, and cache keys are namespaced by tenant. This defense-in-depth approach ensures no single layer failure exposes cross-tenant data.

Common vulnerability patterns to prevent: IDOR (Insecure Direct Object Reference) by enforcing tenant ownership checks on every resource ID parameter, mass assignment attacks by filtering tenant ID from request bodies, and race conditions by using database row-level security as a backstop.
