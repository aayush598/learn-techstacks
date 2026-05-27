# Chapter 07: SSO & Identity Provider

> **Part:** 16 - User Management & Access Control

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [SSO Architecture Overview](sec-01-sso-architecture-overview.md) | SSO flow, identity provider roles, service provider configuration, IdP-initiated vs SP-initiated SSO |
| 02 | [SAML 2.0 Integration](sec-02-saml-2-0-integration.md) | SAML metadata exchange, assertion consumer service, attribute mapping, signing certificates |
| 03 | [OIDC Provider Integration](sec-03-oidc-provider-integration.md) | OpenID Connect discovery, authorization code flow, ID token validation, userinfo endpoint |
| 04 | [IdP Discovery & Metadata](sec-04-idp-discovery-metadata.md) | Tenant-specific IdP configuration, IdP metadata storage, auto-discovery via email domain |
| 05 | [Just-In-Time Provisioning](sec-05-just-in-time-provisioning.md) | JIT user creation on first SSO login, attribute-based role assignment, profile sync |
| 06 | [SCIM User Sync](sec-06-scim-user-sync.md) | SCIM 2.0 for user/group sync, IdP-driven user deactivation, group membership sync |
| 07 | [SSO Session Mapping](sec-07-sso-session-mapping.md) | Mapping IdP sessions to app sessions, session timeout alignment, forced re-authentication |
| 08 | [Multi-IdP Support](sec-08-multi-idp-support.md) | Multiple identity providers per tenant, IdP priority, conditional IdP selection based on email domain |

---

## SSO Flow (SP-Initiated)

```
[User] → Access App → Redirect to Login Page
    ↓
[User] → Selects "Login with Company SSO"
    ↓
[App] → Asks for Company Email Domain
    ↓
[App] → Looks up IdP configuration → Redirect to IdP
    ↓
[IdP] → Authenticates User → SAML/OIDC Response
    ↓
[App] → Validates Assertion (signature, audience, expiry)
    ↓
[App] → JIT Provision or Update User Profile
    ↓
[App] → Create Session → Redirect to Dashboard
```

---

## Learning Objectives

- Design SSO architecture supporting SAML 2.0 and OIDC
- Implement SAML 2.0 integration with metadata exchange
- Build OIDC provider integration with authorization code flow
- Create IdP discovery based on tenant configuration and email domain
- Implement just-in-time user provisioning on first SSO login
- Integrate SCIM 2.0 for automated user and group sync
- Map IdP sessions to application sessions with alignment
- Support multiple identity providers per tenant
