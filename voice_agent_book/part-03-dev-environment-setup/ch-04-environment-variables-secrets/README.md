# Chapter 04: Environment Variables & Secrets Management

> **Part:** 03 - Development Environment & Project Setup

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Environment Variable Strategy](sec-01-environment-variable-strategy.md) | .env.local, .env.development, .env.production, .env.test — precedence and merging |
| 02 | [Zod Validation Schema](sec-02-zod-validation-schema.md) | Runtime validation of env vars, type generation, validation at startup, error messages |
| 03 | [Secret Rotation & Lifecycle](sec-03-secret-rotation-lifecycle.md) | Rotation schedule, automated rotation via Vault, downtime impact, rotation testing |
| 04 | [Doppler/Vault Integration](sec-04-doppler-vault-integration.md) | HashiCorp Vault setup, Doppler for simpler alternative, sync to .env, CI integration |
| 05 | [Environment-Specific Config](sec-05-environment-specific-config.md) | Dev/staging/prod differences, feature flags via env, API endpoints, logging levels |
| 06 | [CI/CD Environment Injection](sec-06-cicd-environment-injection.md) | GitHub Actions secrets, environment protection rules, PR preview environments, env sync |

---

## Key Takeaways

- Runtime validation of all env vars using Zod schema
- .env.local for local overrides (gitignored)
- HashiCorp Vault for production secrets with auto-rotation
- Zod schema generates TypeScript types for env vars
- Strict separation: dev/staging/prod environments
- CI secrets injected via GitHub Actions with environment protection
