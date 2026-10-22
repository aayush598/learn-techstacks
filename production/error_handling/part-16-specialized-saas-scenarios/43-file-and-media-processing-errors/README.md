# Chapter 43 — File and Media Processing Errors

> Part XVI · _Estimated reading time: 80–100 min_
> **Prerequisite:** [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)

## One-sentence summary

Files fail at **every hop** — validation, upload, storage, transformation, scanning, delivery —
and the dangerous failures are the quiet ones: an interrupted multipart upload that bills you
forever, a resumable job that reprocesses the same object twice, a "validated" upload that is
really just a renamed executable.

## Why this chapter matters

File handling is the one part of a SaaS product where **users control the bytes** and the
vendor controls the bill. A 10 GB upload that dies at 90% either resumes or wastes 9 GB of
transfer; an incomplete S3 multipart upload keeps charging for parts nobody can see; a
transcode worker that retries without an idempotency key produces duplicate renditions and
double the CPU; a scan that times out and "fails open" serves malware from your CDN. Every one
of these is an error-handling design decision, and each is covered below with concrete limits
and a safe default.

## Chapter map

The chapter has 14 sections grouped into ten files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-upload-validation-and-storage-failures.md`](./01-concepts/01-upload-validation-and-storage-failures.md) | 43.1–43.3 | Validation at the trust boundary, size/type checks, storage-provider failures |
| [`01-concepts/02-interrupted-uploads-and-multipart.md`](./01-concepts/02-interrupted-uploads-and-multipart.md) | 43.4–43.5 | Interrupted uploads, multipart semantics, resumability |
| [`01-concepts/03-processing-scanning-and-temp-urls.md`](./01-concepts/03-processing-scanning-and-temp-urls.md) | 43.6–43.9 | Transformation failures, malformed files, malware scanning, signed URLs |
| [`01-concepts/04-downloads-cleanup-and-batch.md`](./01-concepts/04-downloads-cleanup-and-batch.md) | 43.10–43.14 | Streaming/range downloads, temp cleanup, duplicate processing, resume, batch |
| [`02-deep-dive/01-multipart-resume-and-cleanup-mechanics.md`](./02-deep-dive/01-multipart-resume-and-cleanup-mechanics.md) | 43.4, 43.5, 43.11 | Part numbering, ETags, resume protocol, abort/lifecycle cleanup |
| [`02-deep-dive/02-malware-scanning-and-quarantine-flow.md`](./02-deep-dive/02-malware-scanning-and-quarantine-flow.md) | 43.6–43.8 | Quarantine → scan → promote flow, scanner failure taxonomy |
| [`03-practical-examples/01-s3-multipart-upload-with-cleanup.ts`](./03-practical-examples/01-s3-multipart-upload-with-cleanup.ts) | 43.2–43.5, 43.11 | End-to-end resumable upload + abort + lifecycle rule |
| [`03-practical-examples/02-processing-pipeline-with-checkpoints.md`](./03-practical-examples/02-processing-pipeline-with-checkpoints.md) | 43.6, 43.13, 43.14 | Checkpointed pipeline, derivative keys, per-item batch results |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Upload/processing rules and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | S3 limits, HTTP range/status map, cleanup checklist, glossary |

## Learning objectives

By the end you can:

- Validate uploads by **content**, not extension, at the trust boundary, with explicit size
  and type limits.
- Explain S3 multipart semantics: **5 MB minimum part (except the last), 10,000 parts, 5 TB
  object maximum**, and why incomplete uploads cost money.
- Design a **resume protocol** using part numbers and ETags that survives a dropped connection.
- Make processing idempotent with deterministic derivative keys, and resume long jobs from
  checkpoints instead of restarting.
- Scan untrusted files without failing open, and serve them only through short-lived signed
  URLs.
- Run large batches with **per-item success/failure** instead of all-or-nothing.

## Key takeaways

1. **Validation is a security boundary, not a UX nicety.** Sniff magic bytes, enforce an
   allowlist, cap decompressed size, and never trust `Content-Type` from the client.
2. **Multipart is a protocol with a cleanup obligation.** Every `CreateMultipartUpload` must
   end in `Complete` or `Abort`; the leftovers are invisible but billed, so add an
   `AbortIncompleteMultipartUpload` lifecycle rule.
3. **Resume is part of the upload feature.** Lost bytes should cost a part, not the whole file.
4. **Processing retries need a content identity.** `sha256(bytes)` plus a transformation
   version is the key that makes a retry a no-op.
5. **Quarantine, then serve.** Malware scanning failures must fail closed, and downloads should
   go through expiring signed URLs with the correct content type.
6. **Cleanup is a failure path, not housekeeping.** Temp objects, partial parts, and stale
   derivatives need owners, TTLs, and metrics.

## Exercises

1. Take your current upload endpoint and list every check it performs. Mark which ones trust
   the client.
2. Start a multipart upload, abort it mid-way, and verify the parts are deleted (or scheduled
   for deletion by lifecycle).
3. Write the resume logic for a 200 MB file that drops at part 7 of 40, and prove part 1–6 are
   not re-uploaded.
4. Reprocess the same object twice and prove the second run is a no-op (same derivative keys).
5. Serve a file that fails malware scanning and confirm it is never reachable by URL.
6. Run a 1,000-item batch where 3 items are corrupt and confirm the response reports 997
   successes and 3 itemized failures.

## Related

- [Chapter 42 — Authentication, Billing, and Subscription Workflows](../42-auth-billing-and-subscription-workflows/README.md)
- [Chapter 44 — AI, LLM, and Tool-Calling Application Errors](../44-ai-llm-and-tool-calling-application-errors/README.md)
- [Chapter 32 — Background Jobs, Queues, and Scheduled Tasks](../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
- [Chapter 39 — Partial Failures and Multi-Step Operations](../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)
