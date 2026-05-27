# Section 02: JWT Token Issuance & Validation

JWT tokens enable stateless authentication for tenant users and API consumers. The JWT carries claims including tenant ID, user ID, roles, permissions, and token expiry. Tokens are signed with the platform's private key using RS256 (asymmetric) to allow verification by downstream services without sharing secrets.

Token issuance flow: authenticate user (credentials, OAuth, SSO), generate JWT with claims (sub = user ID, ten = tenant ID, roles = array, scope = permissions), sign with private key, set expiry (15 minutes for user tokens, 1 hour for service tokens). Refresh tokens (long-lived, stored in database) enable seamless session extension.

Token validation: each service verifies the JWT signature using the public key (fetched from a well-known endpoint or cached locally), checks expiry, validates tenant ID matches the request context, and verifies the required scope for the endpoint. Validation is performed at the API gateway and can be verified downstream if needed.
