# The SQLSTATE Classification Table

> Part IX · Chapter 22 · Sections 22.3–22.13, 22.17, 22.20 · _Estimated reading time: 25 min_
> **Prerequisite:** [Schema, Migrations, Corruption, and Translation](../01-concepts/05-schema-migrations-corruption-and-translation.md)

## In one sentence

`SQLSTATE` is a **five-character standard code** whose first two characters identify a class,
and **the class — not the message — determines retry, status, and alerting**; individual codes
only refine the user-facing meaning.

## Why this matters in production

Messages change between Postgres versions and locales; constraint names change with every
schema edit. The **class** is stable. If your classifier keys on `"duplicate key value violates
unique constraint"` text, a minor upgrade or a translated server breaks it silently. A table
keyed on class and code survives upgrades, works across drivers, and gives every reviewer the
same answer to "should this retry?".

## Core concept

A Postgres `SQLSTATE` is `class (2 chars) + subclass (3 chars)`. Class `23` is *integrity
constraint violation*; `23505` is its *unique violation* subclass. MySQL also exposes a
`SQLSTATE` (usually `23000` for integrity errors) **plus** a numeric `errno` that is far more
specific — you need both.

```text
  2 3 5 0 5
  └─┘ └──┘
  class  subclass
  "23"   "505"
  integrity   unique
```

### The class-level decision table

| Class | Name | Includes | App category | Transient | HTTP | Alert |
| ----- | ---- | -------- | ------------ | --------- | ---- | ----- |
| `08` | Connection exception | `08001`, `08003`, `08006`, `08007`, `08P01` | DEPENDENCY | **yes** | `503` | only if sustained |
| `22` | Data exception | `22001`, `22003`, `22P02`, `22007`, `22012` | VALIDATION | no | `422` | no |
| `23` | Integrity constraint violation | `23502`, `23503`, `23505`, `23514`, `23P01` | CONFLICT / VALIDATION | no | `409`/`422` | no |
| `25` | Invalid transaction state | `25P02`, `25P03`, `25006` | INTERNAL / ROUTING | no / routing | `500`/`503` | `25P02` yes |
| `28` | Invalid authorization | `28000`, `28P01` | CONFIG | no | `500` | **yes** |
| `3D` | Invalid catalog name | `3D000` | CONFIG | no | `500` | **yes** |
| `3F` | Invalid schema name | `3F000` | CONFIG / SCHEMA | no | `500` | **yes** |
| `40` | Transaction rollback | `40001`, `40002`, `40003` | CONCURRENCY | **yes** (`40001`) | `409`/`503` | no |
| `42` | Syntax error / access rule | `42601`, `42703`, `42P01`, `42501` | SCHEMA / INTERNAL | no | `500` | **yes** |
| `53` | Insufficient resources | `53100`, `53200`, `53300` | CAPACITY | **yes** | `503` | yes if sustained |
| `54` | Program limit exceeded | `54001`, `54011`, `54023` | INTERNAL | no | `500` | **yes** |
| `55` | Object not in prerequisite state | `55P03`, `55006` | CONCURRENCY / STATE | `55P03` yes | `409`/`503` | no |
| `57` | Operator intervention | `57014`, `57P01`, `57P03` | DEPENDENCY / TIMEOUT | **yes** | `504`/`503` | `57P01` yes |
| `58` | System error (I/O) | `58000`, `58P01` | INFRASTRUCTURE | no | `503` | **yes** |
| `XX` | Internal error | `XX000`, `XX001`, `XX002` | CORRUPTION | no | `503` | **yes** |

### The codes you will actually meet

| SQLSTATE | Name | Meaning in a SaaS | Category | Retry |
| -------- | ---- | ----------------- | -------- | ----- |
| `08001` | `sqlclient_unable_to_establish_sqlconnection` | wrong host/TLS during config | CONFIG | no |
| `08003` | `connection_does_not_exist` | socket died | DEPENDENCY | **yes** |
| `08006` | `connection_failure` | failover, restart, network | DEPENDENCY | **yes** |
| `08007` | `transaction_resolution_unknown` | commit sent, outcome unknown | AMBIGUOUS | read-back, not blind retry |
| `23502` | `not_null_violation` | required field missing | VALIDATION | no |
| `23503` | `foreign_key_violation` | parent row missing / still referenced | VALIDATION | no |
| `23505` | `unique_violation` | duplicate submission / replay | CONFLICT | no (dedupe instead) |
| `23514` | `check_violation` | storage-level business rule | VALIDATION | no |
| `23P01` | `exclusion_violation` | overlapping ranges (bookings) | CONFLICT | no |
| `25P02` | `in_failed_sql_transaction` | you kept querying after an error | BUG | no |
| `25P03` | `idle_in_transaction_session_timeout` | transaction left open | BUG/CAPACITY | no |
| `40001` | `serialization_failure` | SSI conflict / RR update conflict | CONCURRENCY | **yes, whole txn** |
| `40P01` | `deadlock_detected` | lock cycle | CONCURRENCY | **yes, whole txn** |
| `42501` | `insufficient_privilege` | missing grant after migration | CONFIG | no, alert |
| `42601` | `syntax_error` | broken SQL / bad deploy | SCHEMA | no, alert |
| `42703` | `undefined_column` | code/schema mismatch | SCHEMA | no, alert |
| `42P01` | `undefined_table` | dropped/renamed table | SCHEMA | no, alert |
| `53300` | `too_many_connections` | server capacity | CAPACITY | yes + shed |
| `55P03` | `lock_not_available` | `lock_timeout` expired | CONCURRENCY | yes |
| `57014` | `query_canceled` | `statement_timeout` / user cancel | TIMEOUT | yes, inspect |
| `57P01` | `admin_shutdown` | server restarting | DEPENDENCY | yes, backoff |
| `57P03` | `cannot_connect_now` | starting up | DEPENDENCY | yes, backoff |
| `58P01` | `disk_error` (I/O) | disk full / failing | INFRASTRUCTURE | no, alert |
| `XX001` | `data_corrupted` | bad page/checksum | CORRUPTION | **no**, fail closed |
| `XX002` | `index_corrupted` | broken index | CORRUPTION | **no**, rebuild |

## How it works (mechanics)

1. **Extract** the class and code from the driver (`pgcode`, `err.code` for node-pg, `*pq.Error`,
   `pgconn.PgError`, MySQL `errno` + `sqlState`).
2. **Bucket by class** first. If the class is not in your table, bucket as `UNKNOWN` — never
   default to "transient".
3. **Refine within the class** only where behavior differs (`23505` vs `23503`; `40001` vs
   `40003`; `57014` vs `57P03`).
4. **Decide** the four policy bits: `transient`, `httpStatus`, `alert`, `retryScope`
   (`statement` / `transaction` / `none`).
5. **Translate** to an application code and drop the raw code into `cause` only.

```text
SQLSTATE ──▶ class ──▶ bucket ──▶ policy bits ──▶ app code ──▶ HTTP
 23505       23        INTEGRITY   no/409/no      ALREADY_EXISTS  409
 40001       40        CONFLICT    yes/409/no     RETRYABLE       409 after exhaustion
 42P01       42        SCHEMA      no/500/YES     SCHEMA_MISMATCH 500
```

## Worked example

```ts
type Policy = {
  transient: boolean;
  http: number;
  alert: boolean;
  retryScope: "none" | "transaction" | "statement";
};

const CLASS_POLICY: Record<string, Policy> = {
  "08": { transient: true, http: 503, alert: false, retryScope: "transaction" },
  "22": { transient: false, http: 422, alert: false, retryScope: "none" },
  "23": { transient: false, http: 409, alert: false, retryScope: "none" },
  "40": { transient: true, http: 409, alert: false, retryScope: "transaction" },
  "42": { transient: false, http: 500, alert: true, retryScope: "none" },
  "53": { transient: true, http: 503, alert: false, retryScope: "transaction" },
  "55": { transient: true, http: 409, alert: false, retryScope: "transaction" },
  "57": { transient: true, http: 503, alert: false, retryScope: "transaction" },
  "58": { transient: false, http: 503, alert: true, retryScope: "none" },
  XX: { transient: false, http: 503, alert: true, retryScope: "none" },
};

export function policyFor(sqlstate: string): Policy {
  const cls = sqlstate.slice(0, 2);
  return CLASS_POLICY[cls] ?? { transient: false, http: 500, alert: true, retryScope: "none" };
}
```

Override only where the subclass genuinely differs: `25P02` is a **bug** (`alert: true`),
`25006` is **routing** (`retryScope: "transaction"` after reconnecting to the new primary).

## Key data / numbers

- `SQLSTATE` is **5 characters**; class is the first 2. Postgres emits it for nearly every
  server-side error; client/network errors often have none.
- **Class `40` + `08` + `53` + `57`** → transient; **class `23` + `22` + `42` + `XX`** →
  permanent. Class `25` is context-dependent.
- **`08007`** is the code for "transaction resolution unknown" — the formal name for an
  ambiguous commit.
- MySQL integrity errors usually report `SQLSTATE 23000`; **you must read `errno`** (`1062`,
  `1452`, `1048`, `1213`, `1205`) to distinguish them.
- Alerting rule: class `42`, `XX`, `58`, `28`, `3D`, `3F` page; class `23`, `22`, `40` never do.

## Real-world use case — Acme SaaS

Acme's old classifier switched on English message text. After a Postgres minor upgrade changed
one message's wording, `23505` stopped matching and duplicates started returning `500`s.
Rewriting it as a **class-first table** (with `23505` as the only subclass override for the
conflict code) made the classifier version-independent and identical across node-pg, psycopg2,
and pgx. The support load from duplicate invitations dropped to zero, and the same table now
backs both the API mapping and the retry policy.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Class-first table | stable, small, version-proof | needs subclass overrides | default |
| Full per-code table | precise | large, churns per version | mature platform teams |
| Message-string matching | quick to write | breaks on upgrades/locales | never |
| ORM-code table (P2002…) | portable | loses DB detail | ORM-only codebases |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Key on class, refine on code | Match English error messages |
| Default unknown codes to permanent + alert | Default unknown codes to "retry" |
| Keep `retryScope` in the policy | Retry a statement after `40001` |
| Map `08007` to "unknown outcome" | Treat `08007` as a plain failure |
| Page on class `42`/`XX` | Hide schema errors behind `422` |

## Common mistakes

- **Treating class `25P02` as a connection error** — it is your code ignoring a failed
  transaction.
- **Bucketing `55P03` as permanent** — it is a lock timeout and retries fine.
- **Forgetting MySQL `errno`** — every integrity error looks like `23000`.
- **Adding a new code to the table without a default** — unknown codes then crash the handler.
- **Alerting on class `40`** — deadlocks are expected under contention and self-heal on retry.

## Checklist

- [ ] Classifier buckets by the first two characters first.
- [ ] Every class has all four policy bits, including `retryScope`.
- [ ] Unknown class/code → permanent + alert, never silent retry.
- [ ] Subclass overrides are limited to behavior-changing codes.
- [ ] No message-text matching anywhere in the path.

## Related

- [Driver and Vendor Error Shapes](./02-driver-and-vendor-error-shapes.md)
- [SQLSTATE → Domain Error Mapping](../03-practical-examples/01-sqlstate-to-domain-error-mapping.md)
- [Chapter 22 Reference — Cheat Sheet](../05-reference/README.md)
- [Error Translation and Normalization (16.4)](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/01-concepts/02-translation-directions.md)
