# Chapter 03: Tenant Onboarding & Provisioning

> **Part:** 14 - Multi-Tenant & White-Label

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Self-Service Signup Flow](sec-01-self-service-signup.md) | Registration form, email verification, tenant creation, initial setup, welcome sequence |
| 02 | [Automated Tenant Provisioning Pipeline](sec-02-automated-provisioning-pipeline.md) | Infrastructure provisioning, database creation, schema setup, default resource allocation |
| 03 | [Default Configuration Templates](sec-03-default-configuration-templates.md) | Per-tier configuration defaults, feature flags, quota limits, regional settings |
| 04 | [Setup Wizard Implementation](sec-04-setup-wizard.md) | Multi-step onboarding wizard, progress persistence, guided configuration, skip-and-configure-later |
| 05 | [Welcome Flow & Email Automation](sec-05-welcome-flow-email.md) | Transactional email sequence, in-app welcome messages, getting-started checklist |
| 06 | [Provisioning Status Tracking](sec-06-provisioning-status-tracking.md) | Real-time provisioning status, async task queue, status API endpoint, error notifications |
| 07 | [Failed Provisioning Recovery](sec-07-failed-provisioning-recovery.md) | Retry logic with exponential backoff, partial cleanup, manual intervention workflow |
| 08 | [Bulk Tenant Import](sec-08-bulk-tenant-import.md) | CSV/API bulk creation, validation pipeline, progress monitoring, error reporting |

---

## Provisioning Pipeline

```
Signup Request
     ↓
[Validate] → Email Verification
     ↓
[Create Tenant Record] → Generate tenant_id
     ↓
[Provision Infrastructure] → DB, Storage, Queues
     ↓
[Apply Configuration] → Feature flags, Quotas
     ↓
[Create Admin User] → First admin account
     ↓
[Send Welcome] → Email + In-app onboarding
     ↓
[Setup Wizard] → Guided first-time configuration
```

---

## Learning Objectives

- Build a self-service tenant signup flow with email verification
- Implement automated provisioning pipeline with async task processing
- Design tier-specific default configuration templates
- Create a multi-step setup wizard for first-time configuration
- Implement welcome email sequences and in-app onboarding
- Track provisioning status in real-time
- Handle provisioning failures with graceful recovery
- Support bulk tenant import for enterprise onboarding
