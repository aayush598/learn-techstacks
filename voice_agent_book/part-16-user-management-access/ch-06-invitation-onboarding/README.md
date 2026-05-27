# Chapter 06: Invitation & Onboarding

> **Part:** 16 - User Management & Access Control

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Invitation Token Design](sec-01-invitation-token-design.md) | Secure token generation, expiry configuration, one-time use enforcement, token payload structure |
| 02 | [Email Invitation Flow](sec-02-email-invitation-flow.md) | Transactional email design, send grid/ SES integration, click tracking, bounce handling |
| 03 | [Self-Registration Approval](sec-03-self-registration-approval.md) | Open registration vs approval required, admin approval queue, auto-approval rules, domain whitelist |
| 04 | [User Onboarding Checklist](sec-04-user-onboarding-checklist.md) | Guided first-time setup, profile completion, tool connection, training modules, progress tracking |
| 05 | [Default Permission Assignment](sec-05-default-permission-assignment.md) | Role assignment at invite, department-based defaults, onboarding permission escalation |
| 06 | [Bulk User Import](sec-06-bulk-user-import.md) | CSV/JSON import, validation pipeline, duplicate detection, error reporting, rollback on failure |
| 07 | [SCIM Provisioning Standard](sec-07-scim-provisioning.md) | SCIM 2.0 implementation, user provisioning, group provisioning, IdP-driven lifecycle management |
| 08 | [Invitation Expiry & Cleanup](sec-08-invitation-expiry-cleanup.md) | Expired token cleanup, re-invitation flow, stale invitation reports, automatic revocation |

---

## Invitation Flow

```
[Admin] → Select User Details → Generate Invite Token
    ↓
[System] → Store Token (hash) + Expiry + Role
    ↓
[System] → Send Invitation Email with Link
    ↓
[User] → Clicks Link
    ↓
[System] → Validate Token (not expired, not used)
    ↓
[User] → Complete Registration (password, profile)
    ↓
[System] → Mark Token Used → Auto-Assign Role
    ↓
[System] → Redirect to Onboarding Checklist
```

---

## Learning Objectives

- Design secure invitation tokens with expiry and one-time use
- Build email invitation flow with delivery tracking
- Implement self-registration with approval workflow
- Create user onboarding checklist with progress tracking
- Configure default permission assignment on invitation
- Build bulk user import with validation pipeline
- Implement SCIM 2.0 for automated user provisioning
- Handle invitation expiry, cleanup, and re-invitation
