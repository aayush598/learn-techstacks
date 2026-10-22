# Practical: A Repository That Translates Every CRUD Failure (24.1–24.8)

> Part IX · Chapter 24 · Sections 24.1–24.8 · _Estimated reading time: 25 min_
> **Prerequisite:** [CRUD Failure Semantics](../01-concepts/03-crud-failure-semantics.md)

## What we're building

`ProjectRepository` for Acme SaaS — a complete TypeScript adapter that:

- imports the driver **only** here;
- exposes intent-named methods with explicit absence semantics;
- distinguishes `null`, `NOT_FOUND`, `CONFLICT`, and `INTERNAL`;
- returns the written row instead of re-reading;
- preserves `cause` while never serializing it.

## The error contract

```ts
export type RepoCode =
  | "NOT_FOUND" | "CONFLICT" | "REFERENCE_MISSING" | "RESOURCE_IN_USE"
  | "STALE_VERSION" | "VALIDATION" | "DB_UNAVAILABLE" | "DB_TIMEOUT" | "INTERNAL";

export interface RepoError extends Error {
  code: RepoCode;
  category: "CONFLICT" | "VALIDATION" | "DEPENDENCY" | "INTERNAL";
  transient: boolean;
  retryScope: "none" | "statement" | "transaction";
  alert: boolean;
  safeMessage: string;
  field?: string;
  op: string;
  resource: string;
  cause: unknown;            // never serialized
}

const FIELDS: Record<string, string> = {
  projects_slug_key: "slug",
  projects_name_tenant_key: "name",
};

export function repoError(e: Omit<RepoError, "name">): RepoError {
  const err = new Error(e.safeMessage) as RepoError;
  Object.assign(err, e);
  err.name = "RepoError";
  Object.defineProperty(err, "cause", { value: e.cause, enumerable: false });
  return err;
}

export function translate(err: any, op: string, resource: string): RepoError {
  const sqlstate: string | undefined = err?.code;
  const constraint: string | undefined = err?.constraint;

  switch (sqlstate) {
    case "23505":                                    // unique violation
      return repoError({
        code: "CONFLICT", category: "CONFLICT", transient: false,
        retryScope: "none", alert: false,
        safeMessage: "That value is already taken.",
        field: constraint ? FIELDS[constraint] : undefined,
        op, resource, cause: err,
      });
    case "23503":                                    // FK violation
      return repoError({
        code: "REFERENCE_MISSING", category: "VALIDATION", transient: false,
        retryScope: "none", alert: false,
        safeMessage: "A referenced record does not exist.",
        field: constraint ? FIELDS[constraint] : undefined,
        op, resource, cause: err,
      });
    case "23502":                                    // not-null violation
      return repoError({
        code: "VALIDATION", category: "VALIDATION", transient: false,
        retryScope: "none", alert: false,
        safeMessage: "A required value is missing.",
        field: err?.column, op, resource, cause: err,
      });
    case "40001":                                    // serialization failure
    case "40P01":                                    // deadlock
      return repoError({
        code: "CONFLICT", category: "DEPENDENCY", transient: true,
        retryScope: "transaction", alert: false,
        safeMessage: "The request conflicted with another change; retry.",
        op, resource, cause: err,
      });
    case "53300":                                    // too many connections
    case "08006":                                    // connection failure
      return repoError({
        code: "DB_UNAVAILABLE", category: "DEPENDENCY", transient: true,
        retryScope: "transaction", alert: true,
        safeMessage: "The service is temporarily unavailable.",
        op, resource, cause: err,
      });
    case "57014":                                    // query canceled (timeout)
      return repoError({
        code: "DB_TIMEOUT", category: "DEPENDENCY", transient: true,
        retryScope: "statement", alert: false,
        safeMessage: "The request took too long; retry.",
        op, resource, cause: err,
      });
    default:
      return repoError({
        code: "INTERNAL", category: "INTERNAL", transient: false,
        retryScope: "none", alert: true,
        safeMessage: "An internal error occurred.",
        op, resource, cause: err,
      });
  }
}
```

## The repository

```ts
type Project = { id: string; tenantId: string; slug: string; name: string; version: number };
type Tx = {
  maybeOne(sql: string, p: unknown[]): Promise<any | null>;
  one(sql: string, p: unknown[]): Promise<any>;
  any(sql: string, p: unknown[]): Promise<any[]>;
  execute(sql: string, p: unknown[]): Promise<{ rowCount: number }>;
};

const toProject = (r: any): Project => ({
  id: r.id, tenantId: r.tenant_id, slug: r.slug, name: r.name, version: r.version,
});

export class ProjectRepository {
  // 24.4 / 24.5 — optional lookup: absence is a value, failure throws.
  async findById(tx: Tx, id: string): Promise<Project | null> {
    try {
      const row = await tx.maybeOne(
        `SELECT id, tenant_id, slug, name, version FROM projects WHERE id=$1`, [id],
      );
      return row ? toProject(row) : null;
    } catch (err) {
      throw translate(err, "projects.findById", "projects");
    }
  }

  // 24.4 — required read: absence is NOT_FOUND.
  async getById(tx: Tx, id: string): Promise<Project> {
    const p = await this.findById(tx, id);
    if (!p) {
      throw repoError({
        code: "NOT_FOUND", category: "VALIDATION", transient: false,
        retryScope: "none", alert: false,
        safeMessage: "Project not found.", op: "projects.getById",
        resource: "projects", cause: undefined,
      });
    }
    return p;
  }

  // 24.6 — insert; duplicates are CONFLICT, and `RETURNING` avoids a re-read.
  async insert(tx: Tx, p: Omit<Project, "id" | "version">): Promise<Project> {
    try {
      const row = await tx.one(
        `INSERT INTO projects (tenant_id, slug, name)
         VALUES ($1,$2,$3)
         RETURNING id, tenant_id, slug, name, version`,
        [p.tenantId, p.slug, p.name],
      );
      return toProject(row);
    } catch (err) {
      throw translate(err, "projects.insert", "projects");
    }
  }

  // 24.7 — optimistic update; 0 rows is disambiguated, never reported as success.
  async update(
    tx: Tx, id: string, tenantId: string, name: string, expectedVersion: number,
  ): Promise<Project> {
    let row: any | null;
    try {
      const res = await tx.execute(
        `UPDATE projects SET name=$1, version=version+1
          WHERE id=$2 AND tenant_id=$3 AND version=$4
        RETURNING id, tenant_id, slug, name, version`,
        [name, id, tenantId, expectedVersion],
      );
      row = (res as any).rows?.[0] ?? null;
    } catch (err) {
      throw translate(err, "projects.update", "projects");
    }
    if (row) return toProject(row);

    const current = await this.findById(tx, id);
    if (!current) {
      throw repoError({
        code: "NOT_FOUND", category: "VALIDATION", transient: false,
        retryScope: "none", alert: false, safeMessage: "Project not found.",
        op: "projects.update", resource: "projects", cause: undefined,
      });
    }
    throw repoError({
      code: "STALE_VERSION", category: "CONFLICT", transient: false,
      retryScope: "none", alert: false,
      safeMessage: "This project was changed by someone else. Reload and retry.",
      op: "projects.update", resource: "projects", cause: undefined,
    });
  }

  // 24.8 — idempotent delete; FK in use is a conflict, not an internal error.
  async delete(tx: Tx, id: string, tenantId: string): Promise<boolean> {
    try {
      const res = await tx.execute(
        `DELETE FROM projects WHERE id=$1 AND tenant_id=$2`, [id, tenantId],
      );
      return res.rowCount > 0;
    } catch (err) {
      const e = translate(err, "projects.delete", "projects");
      if (e.code === "REFERENCE_MISSING" || (err as any)?.code === "23503") {
        throw repoError({
          code: "RESOURCE_IN_USE", category: "CONFLICT", transient: false,
          retryScope: "none", alert: false,
          safeMessage: "Project still has dependent records.",
          op: "projects.delete", resource: "projects", cause: err,
        });
      }
      throw e;
    }
  }
}
```

## Service-level decisions

```ts
// The service, not the repository, decides that duplicate = 409 and replay = 200.
async function createProject(cmd: CreateProject) {
  return db.tx(async (tx) => {
    try {
      return await repo.insert(tx, cmd);
    } catch (e) {
      if (isRepo(e) && e.code === "CONFLICT" && cmd.idempotencyKey) {
        const existing = await repo.findBySlug(tx, cmd.slug);
        if (existing) return existing;             // replay: success
      }
      throw e;                                     // controller maps to 409
    }
  });
}
```

## Tests that catch the regressions

```ts
test("findById returns null, does not throw, for a missing row", async () => {
  await expect(repo.findById(tx, "missing")).resolves.toBeNull();
});

test("findById throws DB_UNAVAILABLE, not null, on a connection error", async () => {
  tx.maybeOne = async () => { throw { code: "08006" }; };
  const e = await repo.findById(tx, "x").catch((x) => x);
  expect(e.code).toBe("DB_UNAVAILABLE");
});

test("update reports STALE_VERSION instead of silently succeeding", async () => {
  const e = await repo.update(tx, "p1", "t1", "new", 99).catch((x) => x);
  expect(e.code).toBe("STALE_VERSION");
});

test("delete is idempotent", async () => {
  await expect(repo.delete(tx, "missing", "t1")).resolves.toBe(false);
});

test("API payload never contains SQL or constraint names", async () => {
  const e = await repo.insert(tx, dup).catch((x) => x);
  const body = toProblem(e);
  expect(JSON.stringify(body)).not.toMatch(/23505|projects_slug_key|INSERT/);
});
```

## Failure-to-response table

| Repository outcome | Code | HTTP | Client action |
| ------------------ | ---- | ---- | ------------- |
| `findById` → `null` | — | `404` (use-case decides) | create / navigate |
| `getById` missing | `NOT_FOUND` | `404` | refresh list |
| insert duplicate | `CONFLICT` | `409` + `field` | change value |
| insert FK missing | `REFERENCE_MISSING` | `422` | fix reference |
| update 0 rows, exists | `STALE_VERSION` | `409`/`412` | reload + retry |
| update 0 rows, absent | `NOT_FOUND` | `404` | refresh |
| delete 0 rows | `false` | `204` | none |
| delete FK referenced | `RESOURCE_IN_USE` | `409` | remove children |
| connection failure | `DB_UNAVAILABLE` | `503` + `Retry-After` | retry |
| statement timeout | `DB_TIMEOUT` | `503`/`504` | retry smaller page |

## Takeaways

- The repository is the **only** place that knows SQLSTATE.
- `find` vs `get` makes absent-vs-required explicit at the call site.
- `RETURNING` removes the post-write read and closes the read-your-writes gap.
- 0-row updates are disambiguated with a follow-up `SELECT`.
- Idempotent delete returns `false`, not an exception.
- `cause` is preserved in-process and structurally excluded from responses.

## Related

- [Leak Prevention and Metadata Preservation](../02-deep-dive/01-leak-prevention-and-metadata-preservation.md)
- [Bulk Partial Success with the Cast](./02-bulk-partial-success-with-cast.md)
- [SQLSTATE → Domain → HTTP (Ch. 16)](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/03-practical-examples/01-postgres-sqlstate-to-domain-to-http.md)
- [Chapter 24 Do's and Don'ts](../04-dos-and-donts/README.md)
