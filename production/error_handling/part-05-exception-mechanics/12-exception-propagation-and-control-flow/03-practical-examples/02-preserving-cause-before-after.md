# Preserving Cause — Before/After Stack Views

> Part V · Chapter 12 · Sections 12.12–12.18 (practical) · _Estimated reading time: 20 min_
> **Prerequisite:** [Rethrow, Wrap, and Preserve Cause](../01-concepts/04-rethrow-wrap-and-preserve-cause.md)

## In one sentence

The difference between a diagnosable incident and a forensic mystery is whether the **before**
stack (masking) or the **after** chain (wrapping with cause) is what the log shows.

## Why this matters in production

Every wrap either preserves the trail or erases it. This file shows the exact log output produced
by masking versus preserving across a realistic four-layer call, then gives you a review checklist
for catching masking before it ships. **You cannot recover cause once it is discarded** — the
information is not recorded anywhere else.

## Scenario

An `ExportJob` reads a large orders table, writes a chunk to S3, then commits an offset. Three
failure sources: a DB read timeout, an S3 `AccessDenied`, and a commit conflict. Watch the same
S3 failure travel through the layers under two coding styles.

```text
worker handler
  └ exportChunk()
      └ writeToS3()
          └ s3.putObject()   ← AccessDenied originates here
```

## Before — masking everywhere

```ts
async function writeToS3(key: string, body: Buffer) {
  try {
    await s3.putObject({ Bucket: BUCKET, Key: key, Body: body });
  } catch (err) {
    throw new Error("S3 upload failed");        // ← cause dropped
  }
}

async function exportChunk(chunk: Chunk) {
  try {
    await writeToS3(chunk.key, chunk.body);
  } catch (err) {
    throw new Error(`Export failed`);            // ← cause dropped again
  }
}

async function runExport(job: ExportJob) {
  try {
    await exportChunk(job.chunk);
  } catch (err) {
    logger.error("export error: " + err);        // ← string, structure lost
    throw new Error("export failed");            // ← cause dropped a third time
  }
}
```

Log output:

```text
export error: Error: export failed
    at runExport (export.ts:21:11)
    at processJob (worker.ts:9:5)
```

Everything below `runExport` is gone. No bucket, no key, no `AccessDenied`, no `aws-sdk` frames.

## After — wrapping that preserves the chain

```ts
class ExportError extends Error {
  constructor(readonly stage: string, cause: unknown) {
    super(`export failed at stage: ${stage}`, { cause });
    this.name = "ExportError";
  }
}

async function writeToS3(key: string, body: Buffer) {
  try {
    await s3.putObject({ Bucket: BUCKET, Key: key, Body: body });
  } catch (err) {
    throw new ExportError(`s3-put:${key}`, err); // cause kept
  }
}

async function exportChunk(chunk: Chunk) {
  try {
    await writeToS3(chunk.key, chunk.body);
    await commitOffset(chunk.offset);
  } catch (err) {
    throw new ExportError(`chunk:${chunk.index}`, err); // adds context, keeps cause
  }
}

async function runExport(job: ExportJob) {
  try {
    await exportChunk(job.chunk);
  } catch (err) {
    logger.error({ err }, "export failed"); // structured: serializes cause chain
    throw err;                              // rethrow original identity
  }
}
```

Log output (structured logger walks `cause`):

```text
export failed
  ExportError: export failed at stage: chunk:42
    at exportChunk (export.ts:24:11)
    caused by ExportError: export failed at stage: s3-put:orders/42.csv
      at writeToS3 (export.ts:12:11)
      caused by AccessDenied: Access Denied
        at deserializeAws_restXmlPutObjectCommandError (s3.ts:4102)
        at async Object.putObject (s3.ts:88)
```

Now you know: **chunk 42, object key `orders/42.csv`, Access Denied from S3.**

## The stack "unwind" view

```text
BEFORE (masking)                 AFTER (preserving)
──────────────────               ──────────────────
runExport ← top of stack         ExportError   (chunk:42)
  (the only frame left)            ExportError (s3-put:orders/42.csv)
                                    AccessDenied ← true origin
  cause: ∅                         cause: complete chain
```

## Translating at a boundary

When the export is triggered by an API request, translate before returning — strip internals but
keep an internal correlation ID (Chapter 16, Chapter 20):

```ts
function toHttp(err: unknown, requestId: string): ProblemDetails {
  if (err instanceof ExportError) {
    return {
      type: "https://errors.acme.example/export-failed",
      title: "Export could not be started",
      status: 503,
      detail: "A dependency was unavailable. Retry later.",
      instance: requestId,
    };
  }
  return { status: 500, title: "Unexpected error", instance: requestId };
}
```

The **full chain is logged internally** against `requestId`; the client sees a safe envelope.

## Key data / numbers

- **S3 `AccessDenied`** returns HTTP `403` and an XML `<Code>AccessDenied</Code>` body — the
  message is stable enough to log, never to leak to end users.
- **Structured loggers** (pino, zap, structlog) serialize `Error.cause` / `__cause__` chains when
  configured with a serializer that walks the chain.
- **`requestId`** must be attached to *both* the log record and the external envelope to join them
  later; typically a UUID in `X-Request-Id`.

## Real-world use case — Acme SaaS

Acme's first export incident read "export failed" with a single stack frame. It took 3.5 hours and
two engineers to find that a bucket policy had changed. After adopting the after-pattern above,
the *next* export incident was diagnosed in under 10 minutes from the log line alone ("chunk 42,
s3-put:orders/42.csv, AccessDenied"). The team made "wrap with cause" a required review item.

## Trade-offs

| Style | Diagnosis speed | Log volume | Risk |
| ----- | --------------- | ---------- | ---- |
| Masking (rethrow generic) | Hours | Low (useless) | Recurring blind incidents |
| Wrap with cause | Minutes | Moderate | Requires structured logging |
| Wrap + log at every layer | Minutes | High (duplicates) | Log noise, cost |
| Wrap + log once at boundary | Minutes | Healthy | Needs one clear boundary |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Put operation + key in the wrapper message | Write "export failed" |
| Attach cause via `{ cause }` / `from` / `%w` | Create a fresh error without cause |
| Log the structured error object once | Concatenate `err` into a string |
| Rethrow the same object when only logging | Re-create the error to "clean it up" |
| Keep `requestId` on internal + external | Leak the internal chain to clients |

## Common mistakes

- **Logging `"error: " + err`** — coerces to a string, discards `cause`.
- **Re-wrapping at the boundary with a fresh error** — the chain the client path needs is gone;
  translate, but keep the internal chain logged.
- **Naming the wrapper the same as the cause** — duplicate-looking entries confuse readers.
- **Forgetting the cause on the *first* wrap** — every later wrap inherits the hole.

## Checklist

- [ ] Each wrapper message names the operation and a key.
- [ ] Cause is attached at every wrap.
- [ ] Exactly one structured log per failure, at the boundary.
- [ ] The full chain is logged internally; the client gets a safe envelope.
- [ ] `requestId` appears in both logs and responses.

## Related

- [Stack Traces and Cause Chains](../02-deep-dive/01-stack-traces-and-cause-chains.md)
- [Propagation Across Languages](./01-propagation-across-languages.md)
- [Error Translation and Normalization (Part VI)](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
- [Rethrow, Wrap, and Preserve Cause](../01-concepts/04-rethrow-wrap-and-preserve-cause.md)
