# Part 16: User Management & Access Control

> **Duration:** Auth Phase (Weeks 4-8, ongoing)  
> **Goal:** Build a comprehensive user management system with authentication, authorization, team management, and SSO.

---

## Chapters Overview

| # | Chapter | Description |
|---|---------|-------------|
| 01 | [Authentication System Architecture](ch-01-authentication-system-architecture/README.md) | Auth.js (NextAuth) setup, session management, JWT vs database sessions, refresh tokens, secure cookies |
| 02 | [Multi-Factor Authentication (MFA)](ch-02-multi-factor-authentication/README.md) | TOTP setup, SMS/email OTP, recovery codes, backup methods, MFA enrollment flow |
| 03 | [Role-Based Access Control (RBAC)](ch-03-role-based-access-control/README.md) | Predefined roles (Admin, Manager, Agent, Developer, Viewer), permission matrix, resource scoping |
| 04 | [Custom Roles & Permissions](ch-04-custom-roles-permissions/README.md) | Custom role creation, granular permission assignment, role cloning, permission validation |
| 05 | [Team & Department Management](ch-05-team-department-management/README.md) | Hierarchical org structure, team grouping, department leads, cross-department access, team settings |
| 06 | [Invitation-Based Onboarding](ch-06-invitation-onboarding/README.md) | Email invitations, invite link expiration, role assignment during invite, onboarding wizard, welcome emails |
| 07 | [SSO & Identity Provider Integration](ch-07-sso-identity-provider/README.md) | SAML 2.0, OIDC, Google Workspace, Microsoft Entra ID, Okta, SCIM provisioning, Just-in-Time provisioning |
| 08 | [Session Management & Security](ch-08-session-management-security/README.md) | Session timeout, concurrent session control, device management, forced logout, session revocation |
| 09 | [API Key Management & Scoping](ch-09-api-key-management-scoping/README.md) | Key generation, permission scoping, key rotation, usage tracking, key revocation, environment scoping |
| 10 | [Activity Logs & User Auditing](ch-10-activity-logs-user-auditing/README.md) | User action tracking, login history, audit trail viewer, anomaly detection, exportable logs |

---

## User Roles Matrix

| Permission | Admin | Manager | Agent | Developer | Viewer |
|------------|-------|---------|-------|-----------|--------|
| View Dashboard | ✅ | ✅ | ✅ | ✅ | ✅ |
| Manage Agents | ✅ | ✅ | — | ✅ | — |
| View Reports | ✅ | ✅ | ✅ | ✅ | ✅ |
| Manage Users | ✅ | ✅ | — | — | — |
| Billing Access | ✅ | — | — | — | — |
| API Keys | ✅ | — | — | ✅ | — |
| System Settings | ✅ | — | — | — | — |

---

## Key Open-Source Tools

- **Auth.js / NextAuth** (ISC) — Authentication
- **ory Kratos** (Apache 2.0) — Identity & user management
- **Casbin** (Apache 2.0) — Authorization framework
- **Permit.io** (Apache 2.0) — Fine-grained authorization
- **Resend** (MIT) — Transactional emails (open-source)

---

## Learning Objectives

- Build a secure authentication system with Auth.js
- Implement MFA with TOTP and recovery options
- Design a comprehensive RBAC system with predefined and custom roles
- Create team and department management with hierarchical structure
- Build invitation-based onboarding with role assignment
- Implement SSO integration with SAML and OIDC providers
- Manage user sessions with security best practices
- Create API key management with fine-grained scoping
- Build user activity logging with audit trail capabilities
