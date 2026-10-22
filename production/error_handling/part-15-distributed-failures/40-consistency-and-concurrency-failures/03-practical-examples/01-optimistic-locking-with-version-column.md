# Optimistic Locking with a Version Column

> Part XV · Chapter 40 · Sections 40.2, 40.3, 40.8 · _Estimated reading time: 26 min_
> **Prerequisite:** [Races, Optimistic Control, and Version Conflicts (40.1–40.3)](../01-concepts/01-races-optimistic-control-and-version-conflicts.md)

## In one sentence

This is **one version column, end to end** — schema, SQL, repository, HTTP `409`/`412`, and client
retry — so two concurrent writers can never silently overwrite each other and the loser always gets
a response it can act on.

## Why this matters in production

A version column is five lines of schema and about fifty lines of code. Skipping it is how
"someone's edit disappeared" becomes a two-week investigation with no reproduction. The example
below is deliberately boring and copy-pasteable: a `documents` table (a stand-in for any editable
row: tenant settings, tickets, project boards), a guarded `UPDATE`, a conflict mapped to `409` with
the current version, and a client that refetches and merges. It is the single highest-value
concurrency change most SaaS applications can make.

## Schema

```sql
CREATE TABLE documents (
  id          uuid PRIMARY KEY,
  tenant_id   text        NOT NULL,
  title       text        NOT NULL,
  body        text        NOT NULL,
  version     bigint      NOT NULL DEFAULT 0,   -- bumped on EVERY write
  updated_by  text,
  updated_at  timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT body_length CHECK (char_length(body) <= 100000)
);

CREATE INDEX documents_tenant_idx ON documents (tenant_id);
-- Optional but useful: an append-only history of resolutions for audits.
CREATE TABLE document_conflicts (
  id            bigserial PRIMARY KEY,
  document_id   uuid NOT NULL REFERENCES documents(id),
  expected_version bigint NOT NULL,
  actual_version   bigint NOT NULL,
  resolved_by   text,
  resolved_at   timestamptz NOT NULL DEFAULT now()
);
```

## Repository — the guarded update

```ts
export type Document = { id: string; tenantId: string; title: string; body: string; version: number };

export class VersionConflict extends DomainError {
  constructor(readonly current: Document) {
    super("DOCUMENT_VERSION_CONFLICT", {
      http: 409,
      details: { currentVersion: current.version, current: current.body },
    });
  }
}

export async function updateDocument(
  tenantId: string,
  id: string,
  expectedVersion: number,
  patch: { title?: string; body?: string; updatedBy: string },
): Promise<Document> {
  const res = await db.query(
    `UPDATE documents
        SET title      = COALESCE($4, title),     -- only fields the caller owns
            body       = COALESCE($5, body),
            version    = version + 1,
            updated_by = $6,
            updated_at = now()
      WHERE id = $1 AND tenant_id = $2 AND version = $3
      RETURNING id, tenant_id AS "tenantId", title, body, version`,
    [id, tenantId, expectedVersion, patch.title ?? null, patch.body ?? null, patch.updatedBy],
  );

  if (res.rowCount === 1) return res.rows[0];

  // Disambiguate: missing row vs. stale version. Never report 409 for a 404.
  const current = await db.oneOrNone(
    `SELECT id, tenant_id AS "tenantId", title, body, version
       FROM documents WHERE id = $1 AND tenant_id = $2`, [id, tenantId]);
  if (!current) throw new DomainError("DOCUMENT_NOT_FOUND", { http: 404 });

  await db.query(
    `INSERT INTO document_conflicts (document_id, expected_version, actual_version, resolved_by)
     VALUES ($1, $2, $3, $4)`, [id, expectedVersion, current.version, patch.updatedBy]);
  throw new VersionConflict(current);            // 409 + current state for the client
}
```

## HTTP layer — `409` in the body, `412` for `If-Match`

```ts
// PUT /v1/documents/:id
// - body carries `version` (typical for JSON APIs) → 409 on mismatch
// - OR the client sends If-Match: "v7" (HTTP-native) → 412 on mismatch
export async function putDocument(req: Request, res: Response) {
  const ifMatch = req.header("If-Match");                 // optional
  const expected = ifMatch
    ? parseStrongEtag(ifMatch)                            // "v7" → 7  (reject W/"..." weak etags)
    : req.body.version;

  if (typeof expected !== "number")
    throw new DomainError("MISSING_PRECONDITION", { http: 428 });  // Precondition Required

  try {
    const doc = await updateDocument(req.tenantId, req.params.id, expected, {
      title: req.body.title, body: req.body.body, updatedBy: req.user.id,
    });
    res.setHeader("ETag", `"v${doc.version}"`);
    return res.status(200).json(doc);
  } catch (err) {
    if (err instanceof VersionConflict) {
      res.setHeader("ETag", `"v${err.current.version}"`);
      return res.status(ifMatch ? 412 : 409).json(problem({
        type: "DOCUMENT_VERSION_CONFLICT",
        title: "The document changed since you loaded it",
        status: ifMatch ? 412 : 409,
        detail: `Expected version ${expected}, current version ${err.current.version}`,
        currentVersion: err.current.version,
      }));
    }
    throw err;
  }
}

// GET must emit the same ETag so If-Match round-trips.
// GET /v1/documents/:id → 200, ETag: "v7"
```

```http
PUT /v1/documents/d_42
If-Match: "v7"
{ "title": "Q3 plan", "body": "..." }
→ 412 Precondition Failed
ETag: "v8"

{ "type": "DOCUMENT_VERSION_CONFLICT", "status": 412,
  "currentVersion": 8, "detail": "Expected version 7, current version 8" }
```

## Client — refetch, re-apply intent, retry

```ts
async function saveWithRetry(docId: string, intent: (doc: Document) => Partial<Document>) {
  for (let attempt = 1; attempt <= 3; attempt++) {
    const current = await api.getDocument(docId);            // fresh state every attempt
    const patch = intent(current);                           // INTENT applied to CURRENT state
    try {
      return await api.putDocument(docId, { ...patch, version: current.version });
    } catch (err) {
      if (err.status !== 409 && err.status !== 412) throw err;
      if (attempt === 3) {
        // Give up gracefully: show the user the latest and let them decide.
        throw new SaveConflict(err.body.currentVersion, err.body.current);
      }
      await sleep(100 * attempt + Math.random() * 100);      // bounded, jittered
    }
  }
}

// Usage: "append this paragraph", not "set body to the text I read 30 s ago".
await saveWithRetry("d_42", (doc) => ({ body: doc.body + "\n\nUpdated by agent." }));
```

> ⚠️ **Hazard.** The `intent` function is the entire safety property. `(doc) => ({ body: staleBody })`
> captures the old value and **re-creates the lost update** even though every request returns `409`.
> Pass an intent ("append", "set status to reviewed"), never a snapshot.

## Concurrency trace

```text
t0  Client A: GET → { body: "A", version: 7 }
t1  Client B: GET → { body: "A", version: 7 }
t2  A: PUT body="A1", version=7  → rowCount=1 → 200, ETag "v8"
t3  B: PUT body="A2", version=7  → rowCount=0 → SELECT → version=8 → 409 + currentVersion=8
t4  B: GET → { body: "A1", version: 8 }; intent(doc) = doc.body + "2" → "A12"
t5  B: PUT body="A12", version=8 → 200, ETag "v9"

Result: both intents applied. No edit lost. document_conflicts has one audit row.
```

## Failure-injection test

```python
def test_concurrent_put_one_wins(pool):
    doc = create_document(pool, body="A")                       # version 0
    a = update_document(pool, doc.id, expected_version=0, patch={"body": "A1"})
    assert a.version == 1
    with pytest.raises(VersionConflict) as exc:
        update_document(pool, doc.id, expected_version=0, patch={"body": "A2"})
    assert exc.value.current.version == 1                       # tells the client where it stands
    b = update_document(pool, doc.id, expected_version=1, patch={"body": "A12"})
    assert b.version == 2

def test_rowcount_zero_is_conflict_not_success(pool):
    # The bug guard: a missing rowCount check reports 200 for a lost write.
    doc = create_document(pool, body="A")
    update_document(pool, doc.id, 0, {"body": "A1"})
    with pytest.raises(VersionConflict):
        update_document(pool, doc.id, 0, {"body": "A2"})
```

## Key data / numbers

- `HTTP 409 Conflict` for a stale `version` in the body; `HTTP 412 Precondition Failed` for a failed
  `If-Match`; `HTTP 428 Precondition Required` when the endpoint requires a precondition and the
  client sent none; `404` when the row is gone.
- ETags used for concurrency must be **strong** (`"v7"`), not weak (`W/"v7"`).
- Version type: **`bigint`** (or `int`), incremented in the same statement as the write; never a
  timestamp for concurrency control.
- Client retry: **3 attempts**, **~100 ms × attempt + jitter**; surface a merge UI after that.
- `document_conflicts` capture rate is the metric that tells you whether clients are holding state
  too long (a rising rate usually means stale caches or background writers, not humans).

## Real-world use case — Acme SaaS

Acme's project board autosaved every keystroke-debounce with `PUT /projects/:id` carrying the whole
board (columns + cards). Two people dragging cards in the same board erased each other's moves —
and because autosave happened every 800 ms, the loss was instantaneous and mostly invisible. They
added `version` to `projects`, returned `409 { currentVersion }`, switched autosave to send an
`intent` (the specific card move) rather than the whole board, and had the client merge on `409`.
Board-move losses dropped to zero; the conflict metric showed a peak of ~2.5% on shared boards and
near-zero on private ones, confirming the model. `document_conflicts` also became the evidence
they needed when a customer claimed "the app deleted my card."

## Trade-offs

| Choice | Pros | Cons | When to use |
|--------|------|------|-------------|
| Version in body (`409`) | simple, works everywhere | client must carry the version | default JSON APIs |
| `If-Match`/ETag (`412`) | HTTP-native, cache-friendly | requires correct GET ETags | public/HTTP-first APIs |
| Whole-object PUT + version | simplest client | conflicts on unrelated field edits | small objects, single writer |
| Intent/PATCH + version | fewer conflicts, safer | per-field ownership design | multi-writer documents |
| No version | zero code | silent lost updates | never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Bump `version` on every write, including background jobs | Bump only on user edits |
| Check `rowCount` and map `0` to `409`/`404` deliberately | Return `200` after a zero-row update |
| Return `currentVersion` + current state on conflict | Return only "conflict" with no way forward |
| Use an `intent` in the retry closure | Retry the snapshot you read before the conflict |
| Emit a strong ETag on GET for `If-Match` users | Send weak ETags for concurrency |
| Record conflict resolutions for audits | Delete conflict rows after handling |

## Common mistakes

- **Version read outside the transaction** that performs the write — the check is not atomic.
- **`PUT` returning `200` with the *attempted* version bump but no row updated** — a subtle
  `200`-for-failure that hides every conflict.
- **Client retry loops that resend the same payload** — they conflict `maxAttempts` times and then
  surface a scarier error than the `409` they started with.
- **Background writers that do `UPDATE ... SET` without a version check** — they bypass the model
  entirely and re-introduce lost updates.
- **Treating `409` as `500`** in the client — logs fill with errors for a normal, expected outcome.
- **No conflict metric** — you cannot tell healthy contention from a persistent stale client.

## Checklist

- [ ] `version bigint NOT NULL DEFAULT 0` on every editable table (background writers included).
- [ ] Every write uses `WHERE version = $expected` and checks `rowCount`.
- [ ] `409` (body version) / `412` (`If-Match`) / `404` / `428` are all covered.
- [ ] Conflicts return `currentVersion` and current state.
- [ ] Clients retry with an `intent` function, not a captured snapshot.
- [ ] GET emits strong ETags wherever `If-Match` is supported.
- [ ] Conflict rate and resolution counts are monitored.
- [ ] A two-writer integration test reproduces the conflict on demand.

## Related

- [Optimistic Concurrency vs Deadlock — mechanics](../02-deep-dive/01-optimistic-concurrency-vs-deadlock.md)
- [Races, Optimistic Control, and Version Conflicts (40.1–40.3)](../01-concepts/01-races-optimistic-control-and-version-conflicts.md)
- [Chapter 40 Reference — conflict decision tables](../05-reference/README.md)
- [HTTP Error Semantics (Ch. 19)](../../../part-08-http-and-api/19-http-error-semantics/README.md)
