# End to End: CreateProject DTO → Field Errors → HTTP 422 Envelope

> Part VII · Chapter 17 · All sections · _Estimated reading time: 24 min_
> **Prerequisite:** [Aggregation, Field-Level Representation, and Stable Codes](../01-concepts/04-aggregation-and-field-error-representation.md)

## In one sentence

This is the full worked path for one endpoint: a **CreateProject DTO**, an **accumulating
validator** emitting pointer+code issues, and the canonical **RFC 9457 `application/problem+json`
422 envelope** — every member justified, every rule registered.

## Why this matters in production

This file is the template to copy for every write endpoint. Once `CreateProject` works this way,
`CreateTask`, `UpdateMembership`, and `BulkInvite` are the same shape with different specs — and
one shared envelope builder means a contract change is one diff, not fifty.

## Step 1 — The DTO and its rules (L2 contract)

```ts
import { z } from "zod";

export const CreateProjectDto = z.object({
  name:   z.string().trim().min(1).max(80),
  slug:   z.string().regex(/^[a-z][a-z0-9-]{2,38}$/, { params: { format: "slug" } }),
  seats:  z.number().int().min(1).max(500),
  startAt: z.iso.datetime({ params: { format: "iso8601-datetime" } }).optional(),
  endAt:   z.iso.datetime({ params: { format: "iso8601-datetime" } }).optional(),
  billing: z.discriminatedUnion("mode", [
    z.object({ mode: z.literal("card") }),
    z.object({ mode: z.literal("invoice"), taxId: z.string().min(9).max(20) }),
  ]).optional(),
}).strict();
```

Rule inventory (each row = one registered rule):

| Rule | Class (§) | Code | Params |
| ---- | --------- | ---- | ------ |
| unknown top-level key | structure 17.2 | `unknown_field` | `key` |
| `name` present & 1–80 after trim | required/range 17.3/17.5 | `required` / `out_of_range` | `min`,`max` |
| `slug` pattern | format 17.6 | `format_invalid` | `format: "slug"` |
| `seats` integer 1–500 | type/range 17.4/17.5 | `type_mismatch` / `out_of_range` | `min`,`max` |
| `endAt` ≥ `startAt` | cross-field 17.7 | `cross_field_invalid` | `rule`,`other` |
| `taxId` when `billing.mode=invoice` | conditional 17.8 | `conditional_rule_failed` | `when` |

Note what is **not** here: plan limits (L3, Ch. 18), uniqueness of `slug` in the tenant (L3),
"project count within plan" (L3). The DTO owns the contract; the domain owns the world.

## Step 2 — Accumulate and convert

```ts
type Issue = { pointer: string; code: string; message?: string; params?: object };

export function validateCreateProject(body: unknown): Issue[] {
  const r = CreateProjectDto.safeParse(body);      // no throw; aggregates per-field issues
  const issues: Issue[] = (r.success ? [] : r.error.issues).map(i => ({
    pointer: "/" + i.path.map(String).join("/"),   // RFC 6901, root = "/"
    code:    zCodeToStable(i),                     // map library issue → registry code
    message: defaultEnglish(i),                    // replaceable presentation
    params:  i.params,                             // interpolation-complete
  }));

  // Dependent rules run only when inputs are clean (17.7/17.8).
  if (!r.success) {
    const v = flatten(r.error);                    // safe view of parsed values
    if (v.startAt && v.endAt && v.endAt < v.startAt && !hasIssue(issues, "/endAt")) {
      issues.push({ pointer: "/endAt", code: "cross_field_invalid",
                    params: { rule: "end_after_start", other: "/startAt" } });
    }
    const billing = asBilling(v.billing);
    if (billing?.mode === "invoice" && !billing.taxId) {
      issues.push({ pointer: "/billing/taxId", code: "conditional_rule_failed",
                    params: { when: "billing.mode=invoice" } });
    }
  }
  return dedupeByPointerCode(issues).slice(0, MAX_ISSUES);   // cap + truncation handled by builder
}
```

```ts
// One envelope builder — the only constructor of a 422 in the codebase.
export function toValidationProblem(issues: Issue[], ctx: Ctx) {
  return {
    status: 422,
    headers: { "content-type": "application/problem+json" },
    body: {
      type: "https://errors.acme.example/validation",
      title: "VALIDATION_FAILED",
      status: 422,
      detail: `The request contains ${issues.length} invalid field(s).`,
      instance: ctx.path,                 // or a URI reference for this request
      requestId: ctx.requestId,
      errors: issues,
      ...(issues.length >= MAX_ISSUES ? { errorsTruncated: true } : {}),
    },
  };
}
```

## Step 3 — The failing request

```http
POST /v1/projects HTTP/1.1
content-type: application/json
authorization: Bearer …

{
  "naem": "Apollo",
  "name": "",
  "seats": "five",
  "startAt": "2026-11-01T00:00:00Z",
  "endAt":   "2026-10-01T00:00:00Z",
  "billing": { "mode": "invoice" }
}
```

## Step 4 — The response

```http
HTTP/1.1 422 Unprocessable Content
content-type: application/problem+json
```

```json
{
  "type": "https://errors.acme.example/validation",
  "title": "VALIDATION_FAILED",
  "status": 422,
  "detail": "The request contains 5 invalid field(s).",
  "instance": "/v1/projects",
  "requestId": "req_8f2c1a",
  "errors": [
    { "pointer": "/",      "code": "unknown_field", "message": "Unknown field \"naem\".",
      "params": { "key": "naem" } },
    { "pointer": "/name",  "code": "required", "message": "Name is required." },
    { "pointer": "/seats", "code": "type_mismatch",
      "message": "Seats must be an integer.", "params": { "expected": "integer", "received": "string" } },
    { "pointer": "/endAt", "code": "cross_field_invalid",
      "message": "End date must not be before start date.",
      "params": { "rule": "end_after_start", "other": "/startAt" } },
    { "pointer": "/billing/taxId", "code": "conditional_rule_failed",
      "message": "Tax ID is required for invoice billing.",
      "params": { "when": "billing.mode=invoice" } }
  ]
}
```

Why each piece is present:

- **`type`** — stable URI identifying the problem type; clients may branch on it alone
  (RFC 9457). The `.example` TLD keeps it a reserved identifier, not a live URL.
- **`status`** — repeated in-body so logs and offline captures are self-describing.
- **`requestId`** — the correlation ID support asks for; also `instance`'s practical twin.
- **`errors[]`** — the extension member carrying our field contract (`pointer` + `code` +
  `params` + optional `message`).
- **`startAt` produced no error** — `type_mismatch` on `seats` did not suppress it, and the
  cross-field rule still ran because *both dates parsed cleanly*.

## The success path (for contrast)

Same endpoint, valid body → `201 Created` with `Location`. **No `200`-with-errors hybrid**,
and no validation data in the success body. If `slug` collides *in the tenant*, that is L3 and
arrives as `409` with `code: "SLUG_TAKEN"` — a different envelope family, per
[Chapter 18](../../18-domain-and-business-logic-errors/README.md).

## Variant — same contract, different stack

The envelope and codes are language-agnostic; only the validator swaps:

```python
# FastAPI/Pydantic — default framework 422 uses detail[].loc/msg/type;
# override it so the OUTBOUND contract matches ours.
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc: RequestValidationError):
    errors = [
        {"pointer": "/" + "/".join(str(p) for p in e["loc"][1:]),   # skip body root
         "code": PYDANTIC_CODE_TO_STABLE[e["type"]],                # e.g. missing → required
         "message": DEFAULT_EN.get(e["type"], "Invalid value."),
         "params": {k: v for k, v in e.items() if k in ("min_length", "max_length", "expected")}}
        for e in exc.errors()
    ]
    return JSONResponse(status_code=422, content=problem_body(errors, request))
```

⚠️ **Hazard.** Framework defaults (`{"detail":[{"loc":…,"msg":…,"type":…}]}`) are a *different
contract*. Pick one outbound shape per API and translate framework issue types into your registry
codes — clients must never see both.

## Key data / numbers

- Content type: **`application/problem+json`**; status **`422`** (RFC 9110 *Unprocessable
  Content*).
- Envelope members: `type`, `title`, `status`, `detail`, `instance` (RFC 9457) +
  `requestId`, `errors[]` (extensions).
- Field entry: `pointer` (RFC 6901, `""`/`"/"` for root), `code`, optional `message`, `params`.
- This endpoint's registered codes: `unknown_field`, `unexpected_shape`, `required`,
  `type_mismatch`, `out_of_range`, `format_invalid`, `cross_field_invalid`,
  `conditional_rule_failed`.

## Real-world use case — Acme SaaS

Acme's web form originally submitted to an endpoint returning `400 {"error":"validation failed"}`.
The frontend guessed field names from prose ("Name is required" → highlight `#name`), which broke
the day messages were reworded and *catastrophically* broke for German users. After adopting this
envelope: the renderer keys on `pointer` + `code`, dictionaries localize via `messageKey`, and
telemetry grouped by `code` exposed that `format_invalid` on `/slug` was 38% of all rejections —
a regex the design team later loosened with a one-line contract change and zero client deploys.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Build the 422 in one shared function | Hand-roll envelopes per handler |
| Translate framework issue types to registry codes | Leak Pydantic/Zod issue `type` strings raw |
| Run dependent rules only on clean inputs | Emit cross-field errors for unparseable fields |
| Keep L3 checks out of the DTO | Ask the DB inside a schema validator |

## Common mistakes

- **`pointer` includes `body` prefix** (`/body/name`) because a framework's `loc` starts there —
  agree on prefix-free paths and strip it once.
- **`message` interpolated with unescaped user input** (`Unknown field "<script>…"`).
- **Returning `200` + errors** when *some* fields defaulted — either the request is valid (apply
  defaults, `201`) or it is not (`422`).

## Checklist

- [ ] DTO is strict; unknown keys → `unknown_field`.
- [ ] All issues accumulated; dependent rules gated; capped.
- [ ] One `toValidationProblem` builder; `application/problem+json`.
- [ ] Every `code` in the response is registry-listed.
- [ ] Framework default shapes translated, never exposed.

## Related

- [Validation Reference — contract and decision tables](../05-reference/README.md)
- [Bulk, Cross-Field, and Cast Examples](./02-bulk-cross-field-and-cast.md)
- [Chapter 20 — Standardized API Error Responses](../../../part-08-http-and-api/20-standardized-api-error-responses/README.md)
