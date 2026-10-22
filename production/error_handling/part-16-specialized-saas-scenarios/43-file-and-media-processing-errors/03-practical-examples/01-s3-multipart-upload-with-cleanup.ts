/**
 * S3 Multipart Upload with Cleanup — Part XVI · Chapter 43 · Sections 43.2–43.5, 43.11
 *
 * The resumable upload protocol from "Multipart Resume and Cleanup — Mechanics":
 *   43.2 size/type limits enforced before a byte is transferred
 *   43.3 storage-provider errors classified (transient vs permanent)
 *   43.4 interrupted uploads resumed from the store's own part list
 *   43.5 multipart limits honoured (5 MiB min part, 10,000 parts, 5 TiB max)
 *   43.11 every artifact this code creates gets an owner and a TTL
 *
 * Key data: 5 MiB minimum part · 10,000 parts max · 5 TiB object max ·
 * presigned URL max 7 days (this code issues 15 minutes) · lifecycle backstop
 * AbortIncompleteMultipartUpload / DaysAfterInitiation: 7.
 *
 * The recurring cast: Acme SaaS serves multi-tenant project management with
 * customer uploads; `ExportJob` batches produce large media derivatives.
 */

import { createHash } from "node:crypto";
import {
  S3Client, AbortMultipartUploadCommand, CompleteMultipartUploadCommand,
  CreateMultipartUploadCommand, GetObjectCommand, HeadObjectCommand,
  ListPartsCommand, UploadPartCommand, type CompletedPart,
} from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const s3 = new S3Client({ region: process.env.AWS_REGION });
const BUCKET = process.env.UPLOAD_BUCKET!;
const QUARANTINE_PREFIX = "quarantine";   // unreadable by the serving role
const MEDIA_PREFIX = "media";             // the only prefix the API may serve

/** Hard limits from the plan (section 43.2). */
const LIMITS = {
  maxBytes: 2 * 1024 * 1024 * 1024,        // 2 GiB object ceiling
  minPartBytes: 5 * 1024 * 1024,           // 5 MiB — S3 multipart minimum
  maxParts: 10_000,                        // S3 multipart maximum
  maxObjectBytes: 5 * 1024 ** 4,           // 5 TiB — S3 hard ceiling
  partUrlTtlSeconds: 15 * 60,              // short-lived part URLs
} as const;

const ALLOWED_MIME = new Set(["image/png", "image/jpeg", "image/webp", "application/pdf"]);
// --- 1. Error taxonomy: one place decides retry policy for the whole path
export type UploadErrorCode =
  | "UPLOAD_TOO_LARGE"          // 413 — permanent, user-correctable
  | "UPLOAD_TYPE_NOT_ALLOWED"   // 415 — permanent, user-correctable
  | "UPLOAD_TOO_MANY_PARTS"     // 400 — permanent, detected before transfer
  | "UPLOAD_PART_MISMATCH"      // 502 — transient, re-list and re-send the part
  | "UPLOAD_SESSION_EXPIRED"    // 410 — terminal: the session was aborted or expired
  | "UPLOAD_NOT_CLEARED"        // 409 — the malware gate has not cleared the file
  | "STORAGE_UNAVAILABLE";      // 503 — transient, retry with backoff

export class UploadError extends Error {
  constructor(
    readonly code: UploadErrorCode,
    readonly detail: Record<string, unknown> = {},
    readonly retryable = false,
  ) { super(code); this.name = "UploadError"; }
}

/**
 * Storage-provider error names that are safe to retry (section 43.3). Everything else
 * — AccessDenied, SignatureDoesNotMatch, NoSuchBucket — is a configuration error and must
 * fail fast rather than burn a retry budget.
 */
const RETRYABLE_STORAGE_ERRORS = new Set([
  "SlowDown", "InternalError", "RequestTimeout", "ExpiredToken", "ECONNRESET", "ETIMEDOUT",
]);

export function isRetryableStorageError(err: unknown): boolean {
  const name = (err as { name?: string; Code?: string })?.name ?? (err as { Code?: string })?.Code;
  return typeof name === "string" && RETRYABLE_STORAGE_ERRORS.has(name);
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
/** Bounded exponential backoff with jitter — never a fixed sleep. */
async function withRetry<T>(fn: () => Promise<T>, attempts = 4): Promise<T> {
  let lastErr: unknown;
  for (let i = 0; i < attempts; i++) {
    try { return await fn(); } catch (err) {
      lastErr = err;
      if (!isRetryableStorageError(err)) throw err;
      await sleep(Math.random() * Math.min(2 ** i * 250, 5_000));
    }
  }
  throw new UploadError("STORAGE_UNAVAILABLE", { cause: String(lastErr) }, true);
}

// --- 2. Session model: the server-side source of truth for resume
export type StoredPart = { partNumber: number; eTag: string; size: number; checksumSha256?: string };
export type UploadSession = {
  id: string;
  tenantId: string;
  uploadId: string;           // S3 multipart upload id
  key: string;                // quarantine/{tenantId}/{id}
  partSize: number;
  expectedBytes: number;
  contentSha256: string;      // binds the session to specific bytes
  status: "open" | "completed" | "aborted" | "expired";
  expiresAt: string;          // 43.11 — every session has a TTL
};

/** Sessions live in a table; the sweeper queries this index. */
export const UPLOAD_SESSION_SQL = `
  CREATE TABLE upload_session (
    id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL,
    upload_id TEXT NOT NULL,            -- needed by the sweeper to abort
    object_key TEXT NOT NULL, part_size INTEGER NOT NULL,
    expected_bytes INTEGER NOT NULL, content_sha256 TEXT NOT NULL,
    status TEXT NOT NULL,               -- open|completed|aborted|expired
    created_at TIMESTAMPTZ NOT NULL, expires_at TIMESTAMPTZ NOT NULL);`;

// --- 3. Step 1: validate, then plan the parts
export type UploadRequest = {
  tenantId: string;
  fileId: string;
  declaredBytes: number;
  declaredMime: string;
  headBytes: Buffer;         // first bytes of the file, for magic-number sniffing
};

export function sniffMime(head: Buffer): string | null {
  const PNG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
  if (head.subarray(0, 8).equals(PNG)) return "image/png";
  if (head[0] === 0xff && head[1] === 0xd8 && head[2] === 0xff) return "image/jpeg";
  if (head.subarray(0, 4).toString("ascii") === "%PDF") return "application/pdf";
  if (head.subarray(0, 4).toString("ascii") === "RIFF") return "image/webp";
  return null;
}

/** Choose a part size satisfying every multipart constraint at once:
 *  partSize >= 5 MiB (except the last part) AND ceil(size / partSize) <= 10,000. */
export function planParts(expectedBytes: number, preferred = 64 * 1024 * 1024) {
  if (expectedBytes > LIMITS.maxObjectBytes) throw new UploadError("UPLOAD_TOO_LARGE",
    { maxBytes: LIMITS.maxObjectBytes });
  let partSize = Math.min(preferred, Math.max(LIMITS.minPartBytes, expectedBytes));
  while (Math.ceil(expectedBytes / partSize) > LIMITS.maxParts) partSize *= 2;
  const count = Math.ceil(expectedBytes / partSize);
  // Detected BEFORE a single byte moves, not at completion time.
  if (count > LIMITS.maxParts) throw new UploadError("UPLOAD_TOO_MANY_PARTS",
    { needed: count, max: LIMITS.maxParts });
  return { partSize, count };
}

/** Validate the request, plan the parts, and open the multipart session. */
export async function initUpload(req: UploadRequest): Promise<UploadSession> {
  if (req.declaredBytes > LIMITS.maxBytes) throw new UploadError("UPLOAD_TOO_LARGE",
    { maxBytes: LIMITS.maxBytes });
  const sniffed = sniffMime(req.headBytes);
  if (!sniffed || !ALLOWED_MIME.has(sniffed)) throw new UploadError("UPLOAD_TYPE_NOT_ALLOWED",
    { declared: req.declaredMime, sniffed });
  const { partSize } = planParts(req.declaredBytes);
  const key = `${QUARANTINE_PREFIX}/${req.tenantId}/${req.fileId}`;

  const created = await withRetry(() => s3.send(new CreateMultipartUploadCommand({
    Bucket: BUCKET, Key: key, ContentType: sniffed, ChecksumAlgorithm: "SHA256",
    Metadata: { "x-scan-status": "pending" },   // the malware gate starts closed
  })));
  const now = new Date();
  return {
    id: req.fileId, tenantId: req.tenantId, uploadId: created.UploadId!, key, partSize,
    expectedBytes: req.declaredBytes,
    contentSha256: createHash("sha256").update(req.headBytes).digest("hex"),
    status: "open", expiresAt: new Date(now.getTime() + 24 * 3600_000).toISOString(),
  };
}

// --- 4. Step 2: hand the client short-lived part URLs
export async function issuePartUrl(session: UploadSession, partNumber: number): Promise<string> {
  return getSignedUrl(s3, new UploadPartCommand({ Bucket: BUCKET, Key: session.key,
    UploadId: session.uploadId, PartNumber: partNumber }),
  { expiresIn: LIMITS.partUrlTtlSeconds });   // 15 minutes, never 7 days
}

// --- 5. Step 3: upload a part (idempotent by part number)
export async function uploadPart(session: UploadSession, partNumber: number,
                                 body: Buffer): Promise<StoredPart> {
  const res = await withRetry(() => s3.send(new UploadPartCommand({ Bucket: BUCKET,
    Key: session.key, UploadId: session.uploadId, PartNumber: partNumber, Body: body,
    ChecksumAlgorithm: "SHA256" })));
  const checksum = res.ChecksumSHA256;
  // A corrupted part is worse than a missing one: re-send it under the same number.
  if (checksum && checksum !== createHash("sha256").update(body).digest("base64")) {
    throw new UploadError("UPLOAD_PART_MISMATCH", { partNumber }, true);
  }
  return { partNumber, eTag: res.ETag!, size: body.length, checksumSha256: checksum };
}

// --- 6. Step 4: resume — ask the store what already exists (43.4)
export async function listCompletedParts(session: UploadSession): Promise<StoredPart[]> {
  const parts: StoredPart[] = [];
  let marker: string | undefined;
  do {
    const page = await withRetry(() => s3.send(new ListPartsCommand({ Bucket: BUCKET,
      Key: session.key, UploadId: session.uploadId, PartNumberMarker: marker })));
    for (const p of page.Parts ?? []) parts.push({ partNumber: p.PartNumber!,
      eTag: p.ETag!, size: p.Size!, checksumSha256: p.ChecksumSHA256 });
    marker = page.IsTruncated ? page.NextPartNumberMarker : undefined;
  } while (marker);
  // The store's list is the truth. A part whose size disagrees with the plan is
  // stale (a truncated retry) and must be re-sent under the same part number.
  const total = Math.ceil(session.expectedBytes / session.partSize);
  return parts.filter((p) => {
    const isLast = p.partNumber === total;
    const expected = isLast ? session.expectedBytes - session.partSize * (p.partNumber - 1)
                            : session.partSize;
    return p.size === expected;
  });
}

/** The parts the client still needs to send. */
export function missingParts(session: UploadSession, uploaded: StoredPart[]): number[] {
  const done = new Set(uploaded.map((p) => p.partNumber));
  const total = Math.ceil(session.expectedBytes / session.partSize);
  return Array.from({ length: total }, (_, i) => i + 1).filter((n) => !done.has(n));
}

// --- 7. Step 5: complete — check, then decide (the ambiguous call)
export async function completeUpload(session: UploadSession): Promise<{ key: string; eTag?: string }> {
  const parts = await listCompletedParts(session);
  const missing = missingParts(session, parts);
  if (missing.length > 0) throw new UploadError("UPLOAD_PART_MISMATCH",
    { missing: missing.slice(0, 5) }, true);
  const ordered: CompletedPart[] = parts.sort((a, b) => a.partNumber - b.partNumber)
    .map((p) => ({ PartNumber: p.partNumber, ETag: p.eTag }));
  try {
    const res = await withRetry(() => s3.send(new CompleteMultipartUploadCommand({
      Bucket: BUCKET, Key: session.key, UploadId: session.uploadId,
      MultipartUpload: { Parts: ordered }, ChecksumMode: "ENABLED" })));
    return { key: session.key, eTag: res.ETag };
  } catch (err) {
    if ((err as { name?: string }).name === "NoSuchUpload") {
      // Either a previous attempt already completed it, or it was aborted/expired.
      // A blind retry reports failure for an object that exists.
      const head = await s3.send(new HeadObjectCommand({ Bucket: BUCKET, Key: session.key }))
        .catch(() => null);
      if (head) return { key: session.key, eTag: head.ETag };
      throw new UploadError("UPLOAD_SESSION_EXPIRED", { uploadId: session.uploadId }); }
    throw err;
  }
}

// --- 8. Step 6: abort, and the cleanup obligation (43.11)
/** Abort is idempotent: aborting an aborted or completed upload is a no-op success. */
export async function abortUpload(session: UploadSession): Promise<void> {
  await s3.send(new AbortMultipartUploadCommand({ Bucket: BUCKET, Key: session.key,
    UploadId: session.uploadId })).catch((err: { name?: string }) => {
    if (err?.name === "NoSuchUpload") return;   // already gone — success
    throw err;
  });
}

/** The sweeper the lifecycle rule cannot replace: aborts sessions past their TTL.
 *  The lifecycle rule is the backstop for sessions never persisted at all. */
export async function sweepExpiredSessions(now = new Date()): Promise<number> {
  const expired = await db.query<UploadSession>(
    `SELECT * FROM upload_session WHERE status = 'open' AND expires_at < $1 LIMIT 500`,
    [now.toISOString()]);
  for (const s of expired) {
    await abortUpload(s).catch(() => undefined);
    await db.query(`UPDATE upload_session SET status = 'expired' WHERE id = $1`, [s.id]);
  }
  return expired.length;
}

/** The lifecycle rule catches the crash between "CreateMultipartUpload" and the DB
 *  write. Choose it as: longer than any legitimate upload session, short enough
 *  that the storage bill stays bounded. */
export const LIFECYCLE_RULE = {
  Rules: [{
    ID: "abort-incomplete-multipart-uploads", Status: "Enabled",
    Filter: { Prefix: `${QUARANTINE_PREFIX}/` },
    AbortIncompleteMultipartUpload: { DaysAfterInitiation: 7 },   // 7 days
    Expiration: { Days: 30 } },
]};

// --- 9. Step 7: serve only what the malware gate cleared
/** Promotion is copy -> mark clean -> delete quarantine (deep dive 2). Only objects
 *  whose scan status is `clean` ever get a URL: the gate fails closed. */
export async function issueDownloadUrl(tenantId: string, fileId: string,
  scanStatus: "pending" | "clean" | "infected" | "error"): Promise<string> {
  if (scanStatus !== "clean") throw new UploadError("UPLOAD_NOT_CLEARED", { scanStatus });
  return getSignedUrl(s3, new GetObjectCommand({
    Bucket: BUCKET, Key: `${MEDIA_PREFIX}/${tenantId}/${fileId}`,
    ResponseContentType: "application/octet-stream",
    ResponseContentDisposition: "attachment",
  }), { expiresIn: 300 });                        // 5 minutes for private files
}

// --- Real-world use case ----------------------------------------------------
//
// Acme's desktop client uploaded 4 GB exports in 5 MiB parts and kept resume state only
// in browser memory. Every restart began a NEW multipart upload and the old one kept its
// parts: over one quarter the bucket accumulated 2.1 TB of invisible incomplete uploads
// (~$50/month) and support said "upload failed at 92%".
//
// The fix was the protocol in this file: the session row (uploadId + partSize +
// expectedBytes + contentSha256) persisted server-side so a restart RESUMES from ListParts;
// planParts() rejecting a too-many-parts upload before transfer starts; and
// AbortIncompleteMultipartUpload / DaysAfterInitiation: 7 as the backstop for sessions
// that crashed before they were persisted. Storage spend returned to baseline and resume
// success went from 0% to ~98%.
//
// Key data: 5 MiB minimum part, 10,000 parts max, 5 TiB object max, presigned URL max
// 7 days (15 minutes here for parts, 5 for downloads), backstop at 7 days.
//
// --- Checklist --------------------------------------------------------------
// [ ] Part size planned so ceil(size / partSize) <= 10,000, before transfer.
// [ ] Size and sniffed type validated before a multipart upload is opened.
// [ ] Session row persists uploadId, key, partSize, expectedBytes, contentSha256.
// [ ] Resume reconciles with ListParts; stale-size parts are re-sent.
// [ ] Complete sorts parts ascending; NoSuchUpload is resolved with HeadObject.
// [ ] AbortMultipartUpload on cancel, on TTL, and via the lifecycle rule.
// [ ] Storage errors classified: SlowDown retried, AccessDenied not retried.
// [ ] Per-part SHA256 checksum requested and compared; URLs only for `clean`.
//
// --- Related ---------------------------------------------------------------
//
// - Multipart Resume and Cleanup — Mechanics: ../02-deep-dive/01-multipart-resume-and-cleanup-mechanics.md
// - Processing Pipeline with Checkpoints: ./02-processing-pipeline-with-checkpoints.md
// - Chapter 43 Reference: ../05-reference/README.md
