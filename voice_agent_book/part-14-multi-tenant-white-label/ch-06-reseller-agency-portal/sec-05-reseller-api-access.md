# Section 05: Reseller API Access

The Reseller API provides programmatic access for resellers to manage their sub-accounts, automate provisioning, retrieve aggregated analytics, and configure branding. The API is scoped to the reseller's hierarchy—a reseller can only access data and manage accounts within their tree. API keys are generated per reseller with granular permissions.

Key API endpoints include: sub-account CRUD (create tenant, suspend, delete), usage metrics (aggregated and per-sub-account), billing management (invoice history, plan changes), branding configuration, and webhook events (sub-account created, usage threshold reached). The API uses the same authentication and rate limiting as the main platform API, but with reseller-specific scopes.

Rate limits for reseller API are higher than standard API tiers, reflecting the reseller's need to manage multiple sub-accounts. Webhooks notify resellers of important events across their sub-accounts, enabling automation of onboarding, billing, and support workflows.
