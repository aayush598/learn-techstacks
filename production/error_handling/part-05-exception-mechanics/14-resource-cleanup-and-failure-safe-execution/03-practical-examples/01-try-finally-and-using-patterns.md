# try/finally and using Patterns

> Part V · Chapter 14 · Sections 14.1–14.9 (practical) · _Estimated reading time: 21 min_
> **Prerequisite:** [Scoped Cleanup Mechanics](../02-deep-dive/01-scoped-cleanup-mechanics.md)

## In one sentence

This file shows one realistic operation — reading a file, querying a DB, writing to S3 — with its
resources released correctly via `try/finally`, try-with-resources, and `using`, in four languages.

## Why this matters in production

Copy-paste-friendly patterns for the exact resources you use daily prevent the leaks that are
invisible in review. Each example acquires *before* the cleanup scope, releases *inside* it, and
preserves the primary error when release fails.

## Scenario

**Acme SaaS `ExportJob`**: for a range of orders, read from the DB (connection + transaction),
write a CSV to a temp file, upload it to S3, and record the offset. Resources: one DB connection,
one transaction, one temp file, one S3 client (pooled).

```text
acquire conn ─▶ begin tx ─▶ [read rows, write temp file] ─▶ upload S3 ─▶ commit offset
     │             │              │
   release       commit/        delete temp
   (finally)     rollback       (finally)
```

## TypeScript — `try/finally`, acquire before try

```ts
async function exportRange(jobId: string, from: number, to: number): Promise<ExportResult> {
  const conn = await pool.acquire();               // acquire BEFORE try
  const tmp = await fs.mkdtemp(path.join(os.tmpdir(), "export-"));

  try {
    const tx = await conn.begin();                 // transaction as a scope
    try {
      const rows = await readRows(tx, from, to);
      const csvPath = path.join(tmp, "orders.csv");
      await writeCsv(csvPath, rows);

      const key = `exports/${jobId}/${from}-${to}.csv`;
      await s3.upload({ Bucket: BUCKET, Key: key, Body: fs.createReadStream(csvPath) });
      await recordOffset(tx, jobId, to);

      await tx.commit();                           // success → commit
      return { key, rows: rows.length };
    } catch (err) {
      await tx.rollback().catch((rbErr) => {       // rollback is best-effort
        log.warn({ rbErr, jobId }, "rollback failed");
      });
      throw err;                                   // primary preserved
    }
  } finally {
    await fs.rm(tmp, { recursive: true, force: true }); // temp dir always removed
    conn.release();                                     // connection always returned
  }
}
```

## Java — try-with-resources

```java
public ExportResult exportRange(String jobId, long from, long to) throws Exception {
    Path tmpDir = Files.createTempDirectory("export-");
    try (Connection conn = pool.getConnection();                 // LIFO close
         var stmt = conn.prepareStatement("select * from orders where id between ? and ?")) {

        List<OrderRow> rows = readRows(stmt, from, to);
        Path csv = tmpDir.resolve("orders.csv");
        try (var out = Files.newBufferedWriter(csv)) {           // flush+close on exit
            writeCsv(out, rows);
        }

        String key = "exports/" + jobId + "/" + from + "-" + to + ".csv";
        try (var in = Files.newInputStream(csv)) {
            s3.putObject(BUCKET, key, in, csv.toFile().length());
        }

        recordOffset(conn, jobId, to);                            // autocommit or explicit tx below
        return new ExportResult(key, rows.size());
    } finally {
        deleteRecursively(tmpDir);                                // temp dir always removed
    }
}

// With an explicit transaction instead of autocommit:
try (Connection conn = pool.getConnection()) {
    conn.setAutoCommit(false);
    try {
        /* ... work ... */
        conn.commit();
    } catch (Exception e) {
        conn.rollback();          // if rollback throws, it is suppressed by e (caught above? no—)
        throw e;
    }
}
```

> ⚠️ In the explicit-transaction form, wrap `rollback()` so its failure does not replace the
> primary (see `02-primary-vs-secondary-errors.md`).

## C# — `using`

```csharp
using var conn = await pool.OpenAsync();
using var tmp = new TempDirectory("export-");        // custom IDisposable: deletes on Dispose
await using var tx = await conn.BeginTransactionAsync();

try
{
    var rows = await ReadRows(conn, from, to);
    var csv = Path.Combine(tmp.Path, "orders.csv");
    await WriteCsv(csv, rows);
    await s3.PutObjectAsync(new PutObjectRequest { BucketName = Bucket, Key = key, FilePath = csv });
    await RecordOffset(tx, jobId, to);
    await tx.CommitAsync();
    return new ExportResult(key, rows.Count);
}
catch
{
    await tx.RollbackAsync();                        // runs before `using` disposal (reverse)
    throw;
}
```

`using` disposes in reverse order at scope exit, including when an exception propagates.

## Python — context managers

```python
def export_range(job_id: str, lo: int, hi: int) -> ExportResult:
    with pool.acquire() as conn:                     # released on exit / exception
        with tempfile.TemporaryDirectory() as tmp:   # removed on exit / exception
            rows = read_rows(conn, lo, hi)
            csv = os.path.join(tmp, "orders.csv")
            with open(csv, "w", newline="") as f:    # closed on exit / exception
                write_csv(f, rows)
            key = f"exports/{job_id}/{lo}-{hi}.csv"
            s3.upload(BUCKET, key, csv)
            with conn.transaction():                 # commit on success, rollback on exception
                record_offset(conn, job_id, hi)
            return ExportResult(key=key, rows=len(rows))
```

## Comparison

| Concern | TS | Java | C# | Python |
| ------- | -- | ---- | -- | ------ |
| Connection | `finally` | try-with-resources | `using` | `with pool.acquire()` |
| Transaction | manual commit/rollback | manual or JTA | `await using` + manual | `with conn.transaction()` |
| Temp dir | `finally rm` | `finally deleteRecursively` | `using TempDirectory` | `with TemporaryDirectory()` |
| File/stream | `finally` | try-with-resources | `using` | `with open()` |
| Error on close | manual suppressed | auto-suppressed | auto-suppressed | `__exit__` |

## Key data / numbers

- **`TemporaryDirectory`/`mkdtemp` + `rm -rf`**: guarantees recursive removal; safer than tracking
  individual files.
- **try-with-resources** suppresses close errors automatically (JLS 14.20.3).
- **S3 `putObject`** with a stream requires a known length or multipart upload for large files.
- **Pool checkout timeout**: set one (e.g. 5s) so a leak surfaces as a fast `503`, not a hang.

## Real-world use case — Acme SaaS

Acme's export handler originally released the connection at the end of the function. When reading
rows threw (a permission error on one tenant), the connection leaked. After 100 such errors the
pool exhausted and *all* tenants' API calls failed. The `try/finally` refactor above fixed it, and
a temp-directory helper stopped the matching temp-file leak. The same incident motivated the
pool-checkout timeout so future leaks fail fast and visibly.

## Trade-offs

| Pattern | Pros | Cons | When |
| ------- | ---- | ---- | ---- |
| `try/finally` | Works everywhere | Manual ordering | No scoped construct |
| try-with-resources / `using` | Ordering + suppression automatic | Needs the interface | Resource classes |
| Context manager | Powerful `__exit__` semantics | Truthy can suppress | Python |
| Pooled acquire/release | Efficient reuse | Must return faithfully | DB/HTTP clients |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Acquire before the cleanup scope | Acquire inside `try` then release in `finally` |
| Use `mkdtemp` + recursive remove | Track temp files individually |
| Let try-with-resources suppress close errors | Hand-throw over the primary |
| Set pool checkout timeouts | Wait forever for a leaked connection |
| Flush before closing streams | Close without flushing |

## Common mistakes

- **Missing `finally` on the temp dir** — disk fills after repeated failures.
- **Transaction `commit` without `rollback` on the error path** — stuck locks.
- **Closing a stream without flush** — truncated CSV.
- **Releasing the connection before the transaction finishes** — undefined behavior.

## Checklist

- [ ] Connections acquired before `try` and released in `finally`.
- [ ] Transactions commit on success, rollback on error.
- [ ] Temp dirs/files removed on every path.
- [ ] Streams flushed and closed via scope.
- [ ] Pool checkout has a timeout.

## Related

- [Scoped Cleanup Mechanics](../02-deep-dive/01-scoped-cleanup-mechanics.md)
- [defer, Context Managers, and Cancellation-Safe Cleanup](./02-defer-context-managers-and-cancellation-safe.md)
- [Cleanup for Common Resources](../01-concepts/02-cleanup-for-common-resources.md)
- [File and Media Processing Errors (Part XVI)](../../../part-16-specialized-saas-scenarios/43-file-and-media-processing-errors/README.md)
