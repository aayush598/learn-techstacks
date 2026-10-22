# A Full Boundary Map for an Acme SaaS Request

> Part VI · Chapter 15 · All sections · _Estimated reading time: 22 min_
> **Prerequisite:** [Runtime Boundaries](../01-concepts/03-runtime-boundaries.md)

## In one sentence

This is a worked, end-to-end **boundary map** for one Acme SaaS request — `POST /projects/{id}/invite`
— showing every line, its owner, its fallback, and the exact failure each one contains.

## Why this matters in production

Reading about boundaries is easy; placing them in a real request is the skill. This example shows
the whole decision chain for a request that touches auth, tenancy, Postgres, an email provider,
and an optional LLM enrichment — the recurring cast in one flow.

## The request

`Invite a teammate to a project.` It must:

1. Authenticate and authorize (tenant-scoped).
2. Validate the email (syntax).
3. Insert an invitation row (unique per project+email).
4. Send an invitation email via an external provider (optional-ish).
5. Enrich with a suggested role via an LLM (optional).
6. Return `201` with the invitation, or a precise error.

## The boundary map

```text
Client
  │  POST /projects/42/invite  { email }
  ▼
┌──────────────────────────── Request boundary (owner: HTTP controller) ────────────────────────┐
│  • authn (401), authz (403), tenant scope (404 vs 403)                                         │
│  • parse/validate body → 422 with field details                                                │
│  • catch-all: domain → status; unknown → 500 (sanitized)                                       │
│  ┌──────────────────── Application service boundary (owner: InviteService) ─────────────────┐  │
│  │  • owns the unit of work (transaction)                                                    │  │
│  │  • idempotency: same (project,email) → returns existing invitation (200/201)              │  │
│  │  ┌──────────── Repository boundary (owner: InvitationRepository) ──────────────────────┐  │  │
│  │  │  • insert row; translate SQLSTATE 23505 → InvitationAlreadyExists                    │  │  │
│  │  │  • translate 23503 (FK: bad project) → ProjectNotFound                               │  │  │
│  │  │  • translate 40001/40P01 (transient) → RetryableConflict                             │  │  │
│  │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
│  │  ┌──────────── Integration boundaries (owners: EmailAdapter, LlmAdapter) ───────────────┐  │  │
│  │  │  • EmailAdapter: translate provider errors; degrade to "queued" on transient         │  │  │
│  │  │  • LlmAdapter: optional; on failure, isolate → roleSuggestion = null                 │  │  │
│  │  └──────────────────────────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Step 1 — Request boundary (owner: controller)

Owns authentication, authorization, parsing, and the final status/body. It translates domain
outcomes; it never inspects a `SQLSTATE`.

```ts
app.post("/projects/:id/invite", auth, async (req, res) => {
  const requestId = req.id;
  try {
    const dto = InviteDto.parse(req.body); // throws ValidationError → 422
    const result = await inviteService.invite({
      projectId: req.params.id,
      tenantId: req.tenant.id,     // tenant scope comes from auth, never the body
      actorId: req.user.id,
      email: dto.email,
      requestId,
    });
    return res.status(result.created ? 201 : 200).json(result.invitation);
  } catch (err) {
    if (err instanceof ValidationError)
      return res.status(422).json(fieldProblem(err, requestId));
    if (err.code === "INVITATION_ALREADY_EXISTS")
      return res.status(409).json(problem(err, requestId));
    if (err.code === "PROJECT_NOT_FOUND")
      return res.status(404).json(problem(err, requestId));
    if (err.code === "FORBIDDEN")
      return res.status(403).json(problem(err, requestId));
    log.error({ err, requestId }, "invite failed");
    return res.status(500).json(internalProblem(requestId)); // sanitized
  }
});
```

**Owner decision:** `409` vs `422` vs `403`. **Leak rule:** never return `err.message`; only
allowlisted Problem Details.

## Step 2 — Application service boundary (owner: InviteService)

Owns the **transaction** and **idempotency**. It may retry transient conflicts; it does not build
HTTP responses.

```ts
class InviteService {
  async invite(cmd: InviteCommand) {
    await this.authz.require(cmd.actorId, cmd.projectId, "project.invite"); // 403/404

    return this.uow.transaction(async (tx) => {
      for (let attempt = 0; attempt < 3; attempt++) {
        try {
          const existing = await tx.invitations.findByProjectAndEmail(cmd.projectId, cmd.email);
          if (existing) return { created: false, invitation: existing }; // idempotent replay

          const invitation = await tx.invitations.insert({
            projectId: cmd.projectId,
            tenantId: cmd.tenantId,
            email: cmd.email,
            requestedBy: cmd.actorId,
          });
          return { created: true, invitation };
        } catch (err) {
          if (err.code === "RETRYABLE_CONFLICT" && attempt < 2) {
            continue; // serialization failure / deadlock — transient, owner retries
          }
          throw err; // already-translated domain error; propagate
        }
      }
    });
  }
}
```

**Owner decision:** commit/rollback and whether to retry `40001`/`40P01`. **Leak rule:** a driver
error must already be translated by the repository; the service never sees one.

## Step 3 — Repository boundary (owner: InvitationRepository)

Owns the **SQLSTATE → domain** translation. This is the only file that knows Postgres.

```ts
async insert(inv: NewInvitation): Promise<Invitation> {
  try {
    const row = await this.db.query(
      "insert into invitations(project_id, tenant_id, email, requested_by) values ($1,$2,$3,$4) returning *",
      [inv.projectId, inv.tenantId, inv.email, inv.requestedBy],
    );
    return toInvitation(row);
  } catch (err) {
    const state = (err as any).code; // pg exposes SQLSTATE on .code
    switch (state) {
      case "23505": // unique_violation
        throw new DomainError("INVITATION_ALREADY_EXISTS", { cause: err });
      case "23503": // foreign_key_violation → the project row is gone
        throw new DomainError("PROJECT_NOT_FOUND", { cause: err });
      case "40001": // serialization_failure
      case "40P01": // deadlock_detected
        throw new RetryableError("RETRYABLE_CONFLICT", { cause: err });
      case "53300": // too_many_connections
      case "08006": // connection_failure
        throw new InfrastructureError("DB_UNAVAILABLE", { transient: true, cause: err });
      default:
        throw new InfrastructureError("DB_WRITE_FAILED", { cause: err });
    }
  }
}
```

**Owner decision:** what each SQLSTATE *means* in the domain. **Leak rule:** the `SQLSTATE` and the
SQL text live only in `cause`, never in the domain error's `code` or `message`.

## Step 4 — Integration boundaries (owners: EmailAdapter, LlmAdapter)

Email is required-but-degradable; the LLM suggestion is optional.

```ts
// EmailAdapter: required delivery, but a transient failure is queued, not fatal.
async sendInvite(email: string, token: string): Promise<"sent" | "queued"> {
  try {
    await this.provider.send({ to: email, template: "invite", data: { token } });
    return "sent";
  } catch (err) {
    if (isProviderTransient(err)) {
      await this.queue.enqueue("email.invite", { email, token }); // fallback: retry later
      return "queued";
    }
    throw new IntegrationError("EMAIL_PROVIDER_REJECTED", { cause: err }); // permanent
  }
}

// LlmAdapter: optional enrichment. On any failure, isolate → null.
async suggestRole(project: Project): Promise<Role | null> {
  try {
    const out = await this.llm.complete(rolePrompt(project));
    return parseRole(out);
  } catch (err) {
    log.warn({ err }, "role suggestion unavailable; degrading");
    return null; // isolation: page still renders
  }
}
```

**Owner decision:** degrade vs fail. **Leak rule:** the vendor error (Stripe/email/LLM) is
translated to an internal code; the vendor identity never leaves this file.

## The failure table for this request

| Failure | Boundary that contains it | Domain outcome | HTTP |
| ------- | ------------------------- | -------------- | ---- |
| No/bad token | Request (authn) | `UNAUTHENTICATED` | 401 |
| Wrong tenant scope | Request (authz) | `FORBIDDEN` / `PROJECT_NOT_FOUND` | 403 / 404 |
| Malformed email | Request (validate) | `EMAIL_INVALID` | 422 |
| Duplicate invitation | Repository (`23505`) | `INVITATION_ALREADY_EXISTS` | 409 |
| Project deleted | Repository (`23503`) | `PROJECT_NOT_FOUND` | 404 |
| Deadlock | Repository (`40P01`) → service retries | transparent | 201 |
| Email provider 500 | EmailAdapter | `queued` | 201 (degraded) |
| LLM timeout | LlmAdapter | `roleSuggestion=null` | 201 (degraded) |
| Any unknown | Request (catch-all) | `INTERNAL_ERROR` | 500 |

## Key data / numbers

- `SQLSTATE 23505` unique, `23503` FK, `40001` serialization, `40P01` deadlock, `53300` too many
  connections, `08006` connection failure.
- HTTP: `401`, `403`, `404`, `409`, `422`, `500`; use `Retry-After` on `503`.
- Idempotent replay of an existing invitation returns `200`, not a second `201`.

## Real-world use case — Acme SaaS

Before the map existed, this endpoint returned `500` for a duplicate invitation (violating the
user's mental model) and leaked `invitations_project_id_email_key` in the body. After assigning
boundaries: the repository owns the `23505` → `INVITATION_ALREADY_EXISTS` mapping, the service owns
the idempotent replay, the controller owns `409`, the LLM failure degrades silently. Support
tickets for "can't invite" dropped to near zero.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give each line in the map an owner and a fallback | Let the controller inspect SQLSTATE |
| Translate SQLSTATE at the repository only | Map every DB error to one generic `DB_ERROR` |
| Isolate the LLM and degrade the page | Put the LLM on the critical path |
| Return `200` for an idempotent replay | Return a second `201` for the same invite |

## Common mistakes

- **Tenant scope read from the body** instead of the token — a cross-tenant leak (Ch. 35).
- **Retrying `23505`** — it is permanent; retry only `40001`/`40P01`.
- **Email provider failure failing the whole invite** — the invitation row exists; degrade to
  "queued."

## Checklist

- [ ] Every boundary in the map has an owner and a fallback.
- [ ] Only the repository knows SQLSTATE.
- [ ] Only the controller sets HTTP statuses.
- [ ] Optional enrichments are isolated; required steps propagate.
- [ ] Idempotent replays are `200`, not a duplicate `201`.

## Related

- [Postgres SQLSTATE at the Boundary](./02-postgres-sqlstate-boundary-map.md)
- [Runtime Boundaries](../01-concepts/03-runtime-boundaries.md)
- [SQLSTATE → Domain → HTTP map](../../16-error-translation-and-normalization/03-practical-examples/01-postgres-sqlstate-to-domain-to-http.md)
