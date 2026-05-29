# Section 07: Code Review Guidelines

## Overview

Code review is the primary quality control mechanism for the voice agent platform. Reviews follow a structured checklist with mandatory approval requirements, reviewer rotation to distribute knowledge, and security-specific review triggers for sensitive changes. The process is designed to catch bugs, enforce conventions, share knowledge, and maintain architectural consistency — in that priority order.

## Review Flow

```text
┌────────────────────────────────────────────────────────────┐
│                   Code Review Flow                           │
├────────────────────────────────────────────────────────────┤
│                                                              │
│  Author creates PR with description + checklist               │
│       │                                                      │
│       ▼                                                      │
│  CI passes (lint, typecheck, test, build)                     │
│       │                                                      │
│       ▼                                                      │
│  First reviewer assigned (rotation)                           │
│       │                                                      │
│       ├── Request changes ──── Author addresses feedback     │
│       │       │                       │                      │
│       │       └── Re-request review ──┘                      │
│       │                                                      │
│       └── Approve ──── Second reviewer assigned              │
│               │                                              │
│               ├── Request changes ──── Loop                  │
│               │                                              │
│               └── Approve ──── Author merges                 │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

**Two-person review rule**: Every PR requires approvals from two reviewers. The first reviewer checks implementation correctness. The second reviewer checks architectural consistency and edge cases. For trivial changes (typo fixes, dependency bumps), a single approval suffices if annotated with `[trivial]` in the PR title.

## PR Description Template

Every PR must include a description following this template:

```markdown
## Description
<!-- What does this PR do? Why is it needed? -->

## Related Issues
<!-- Closes #123, Related to #456 -->

## Type of Change
- [ ] feat: New feature
- [ ] fix: Bug fix
- [ ] refactor: Code change that neither fixes nor adds
- [ ] chore: Maintenance, dependencies, tooling
- [ ] docs: Documentation only
- [ ] test: Adding or fixing tests
- [ ] perf: Performance improvement
- [ ] security: Security fix

## Testing
- [ ] Added/modified unit tests
- [ ] Added/modified integration tests
- [ ] Manual testing performed
- [ ] Tested on staging environment

## Checklist
- [ ] Code follows naming conventions
- [ ] No new ESLint warnings/errors
- [ ] TypeScript strict mode passes
- [ ] Coverage meets thresholds (≥80%)
- [ ] API changes are backward compatible
- [ ] Database migrations are reversible
- [ ] Error handling is implemented
- [ ] Logging is appropriate (no PII)
- [ ] Documentation updated (JSDoc, README)
```

## Review Checklist

Reviewers evaluate PRs against these criteria, in priority order:

### 1. Correctness
- Does the code do what the description says?
- Are edge cases handled (empty states, error states, race conditions)?
- Are there any concurrency issues (shared state mutation, unguarded async)?
- Are external API calls resilient (timeouts, retries, circuit breakers)?
- Are database queries indexed and N+1-free?

### 2. Security
- Are user inputs validated and sanitized?
- Are there any hardcoded secrets or credentials?
- Is authentication/authorization enforced at the right boundary?
- Is rate limiting applied to user-facing endpoints?
- Have dependencies been checked for known vulnerabilities?

### 3. Architecture
- Does the change follow the established patterns (Repository, Service, Component)?
- Is the change in the correct package layer (app vs package)?
- Are new dependencies justified? Could existing packages be reused?
- Is the change backward compatible? If not, is a migration path provided?
- Are there circular dependencies introduced?

### 4. Maintainability
- Is the code readable without excessive comments?
- Are functions and components reasonably sized (< 200 lines)?
- Are names descriptive and consistent with conventions?
- Are there unnecessary abstractions (premature generalization)?
- Are tests meaningful (test behavior, not implementation)?

### 5. Performance
- Are there unnecessary re-renders in React components?
- Are expensive computations memoized?
- Are database queries using selective fields (not `SELECT *`)?
- Are N+1 query patterns avoided?
- Are assets and bundles optimized?

## Reviewer Rotation

```yaml
# .github/CODEOWNERS
# Global owners (any change needs at least one)
* @voice-agent/tech-leads

# Package-specific owners
packages/voice/ @voice-agent/voice-team
packages/ai/ @voice-agent/ai-team
packages/ui/ @voice-agent/ui-team
apps/web/ @voice-agent/web-team
apps/api/ @voice-agent/api-team
packages/db/ @voice-agent/api-team @voice-agent/voice-team
```

Reviewer rotation follows a weekly schedule:

```typescript
// scripts/assign-reviewer.ts
const teams = {
  'voice-team': ['alice', 'bob', 'charlie'],
  'ai-team': ['diana', 'eve', 'frank'],
  'ui-team': ['grace', 'heidi', 'ivan'],
  'web-team': ['judy', 'karl', 'leo'],
  'api-team': ['maria', 'nick', 'oliver'],
};

// Round-robin assignment based on PR number
export function assignReviewer(prNumber: number, team: string): string {
  const members = teams[team];
  const index = prNumber % members.length;
  return members[index];
}
```

## Code Review Etiquette

**For authors:**
- Keep PRs focused and small (< 400 lines changed). Large PRs are split into logical commits or separate PRs.
- Respond to feedback within 24 hours. If you disagree, explain your reasoning with code or data.
- Self-review before requesting: check for obvious issues, run tests, check the diff yourself.
- Do not merge your own PR without approval (even for urgent fixes — at minimum get a verbal approval).

**For reviewers:**
- Review within 24 hours of assignment. Set aside focused time for review (not during context switches).
- Distinguish between blockers and suggestions. Prefix comments with `blocking:` or `nit:` or `question:`.
- Be respectful and constructive. Ask "What do you think about..." rather than making demands.
- Approve only when you're confident the PR is correct. If unsure, request a third opinion.

## Security Review Flow

Changes touching security-sensitive areas require an additional security review:

```yaml
# Triggered by paths-filter
security-sensitive-paths:
  - "packages/db/**"
  - "**/auth/**"
  - "**/api-keys/**"
  - "**/encryption/**"
  - "Dockerfile*"
  - ".github/workflows/*"
  - "packages/config/eslint/*"
```

When these paths are changed, CODEOWNERS automatically assigns a security reviewer from the security team. The security reviewer checks for:
- Proper authentication mechanism
- Authorization enforcement at the API gateway level
- Encryption in transit and at rest
- Secret management (no secrets in code, environment variables, or config files)
- Input validation and output encoding

## Integration Points

- **GitHub Branch Protection**: Merging requires passing CI, two approvals, no unresolved conversations, and up-to-date branch
- **GitHub CODEOWNERS**: Automatic reviewer assignment based on changed file paths
- **CI status checks**: All checks must pass (lint, typecheck, test, coverage, security scan)
- **Merge queue**: GitHub Merge Queue enforces that PRs are tested against the latest base branch before merging

## Production Considerations

1. **Review velocity**: Track median time-to-review per team. If it exceeds 24 hours, investigate bottlenecks. Consider synchronous review sessions for large, cross-cutting changes.
2. **Bottleneck identification**: If a single person is the only reviewer for a package, cross-train another team member. Use CODEOWNERS to require at least two owners per directory.
3. **Objective standards**: Use automated linting, formatting, and type checking to remove subjective style debates from reviews. Reserve human review for logic, architecture, and security.
4. **Post-merge review**: For hotfixes that bypass review, schedule a post-merge review within 24 hours. Roll back the fix if the review identifies issues.
5. **Review metrics**: Track review depth (comments per PR), review speed (time to first comment), and review quality (bugs caught in review vs. bugs found post-merge). Use these to improve the process, not to evaluate individuals.
