# Deep Dive — Timing Attacks and User Enumeration

> Part XIII · Chapter 34 · Sections 34.9–34.10 (mechanics) · _Estimated reading time: 20 min_
> **Prerequisite:** [Authorization Disclosure, Enumeration, and Timing](../01-concepts/04-authorization-disclosure-enumeration-and-timing.md)

## In one sentence

A **timing attack** infers a secret from how long a comparison takes, and **user enumeration** uses
any observable difference (code, message, timing, or even response size) to learn which accounts are
registered; both are closed by making the observable output — *including time* — independent of the
secret.

## Why this matters in production

Timing side channels are invisible in code review: `a === b` looks correct. But comparison
short-circuits, so a secret compared byte-by-byte leaks its prefix through latency. In authentication,
the effect compounds: if the password hash only runs when the user exists, the *presence of work*
itself announces the user's existence. This deep dive shows the exact mechanics, the constant-time
primitives per language, and how to measure your own leakage so you can prove the fix.

## The mechanics of a comparison leak

String/byte comparison stops at the first mismatch:

```text
guess "aaaaaaaa" vs secret "s3cr3txx"
a≠s → stop after 1 byte      (fast)
guess "s3cr3txx"... wait, attacker cannot see secret; they see TIME.
guess "s........." (correct first byte) → compare 2 bytes → slightly slower
```

Attacker sends many guesses, measures the average latency for each candidate first byte, keeps the
slowest (most-matching) one, and repeats. With enough samples the whole secret is recovered. This is
why **all** secret comparisons must use constant-time primitives.

```text
 latency
   │            ╭─ full match region is measurably slower
   │        ╭───╯
   │   ╭────╯
   │╭──╯
   └────────────────────────▶ bytes matched
```

## Constant-time comparison per language

```ts
// Node.js — timingSafeEqual (equal length required)
import { timingSafeEqual } from "node:crypto";

function ctEqual(a: Buffer, b: Buffer): boolean {
  // Length is not secret in most designs; if it is, hash both to a fixed length first.
  if (a.length !== b.length) return false; // length must not correlate with secret content
  return timingSafeEqual(a, b);
}
```

```python
# Python — hmac.compare_digest (works on str/bytes of equal length)
import hmac
def ct_equal(a: bytes, b: bytes) -> bool:
    return hmac.compare_digest(a, b)
```

```go
// Go — crypto/subtle.ConstantTimeCompare
import "crypto/subtle"
func ctEqual(a, b []byte) bool {
    return subtle.ConstantTimeCompare(a, b) == 1
}
```

Rule: **compare digests, not raw secrets**, and compare them constantly. For signatures, compare the
computed HMAC against the provided one with the constant-time primitive (see `WebhookIngest`).

## The enumeration oracle

Enumeration is broader than timing. Any of these, appearing between "unknown identifier" and "known
identifier, bad credential", is an oracle:

| Observable | Naive difference | Fix |
| ---------- | ---------------- | --- |
| Status code | `404` vs `401` | Same code both cases |
| Error code | `NO_USER` vs `BAD_PASSWORD` | Single `INVALID_CREDENTIALS` |
| Message text | "No account" vs "Wrong password" | Identical message |
| Body length | Different strings | Identical body |
| Latency | Fast miss vs slow hash | Constant-work path |
| Reset behavior | "Email not found" vs "Link sent" | Uniform "if an account exists…" |
| Signup behavior | "Email taken" | Uniform/rate-limited flow |

## The constant-work authentication pattern

```ts
const DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=1$..."; // a real hash of a random password

async function authenticate(email: string, password: string): Promise<User | null> {
  const user = await users.findByEmail(email); // step 1: lookup
  // step 2+3: ALWAYS run the same hash verification, real or dummy
  const hash = user?.passwordHash ?? DUMMY_HASH;
  const ok = await verifyPassword(password, hash);
  if (!user || !ok) return null; // step 4: one uniform failure
  return user;
}
```

Two requirements that are easy to miss:

1. **`DUMMY_HASH` must use the current algorithm and cost.** A dummy bcrypt hash when real users use
   argon2id gives a different timing profile — the oracle returns.
2. **A benign unknown-user path must still do the DB lookup.** If you skip the lookup entirely on a
   malformed email, you reintroduce a fast path. Keep the shape of the work constant.

## Measuring your own leakage

You cannot fix what you do not measure. A simple harness:

```python
import statistics, time, urllib.request

def latency(url, samples=200):
    ts = []
    for _ in range(samples):
        t0 = time.perf_counter()
        try:
            urllib.request.urlopen(url)
        except Exception:
            pass  # 4xx is expected
        ts.append(time.perf_counter() - t0)
    return statistics.median(ts), statistics.pstdev(ts)

# Compare unknown-user vs known-user-wrong-password over the network.
u_med, u_sd = latency("http://localhost:8080/login?email=nobody@x.com")
k_med, k_sd = latency("http://localhost:8080/login?email=real@x.com")
print(f"unknown={u_med*1000:.1f}ms  known={k_med*1000:.1f}ms  gap={(k_med-u_med)*1000:.1f}ms")
```

Interpretation: if the gap is small relative to the standard deviation, the paths are
indistinguishable. If the known-user path is consistently tens of milliseconds slower, the hash-work
difference is leaking. Run enough samples that the medians are stable.

## Key data / numbers

- **CWE-208: Observable Timing Discrepancy** and **CWE-203: Observable Discrepancy** are the
  canonical timing weaknesses; **CWE-204: Observable Response Discrepancy** covers message/code
  differences.
- **OWASP A07: Identification and Authentication Failures** names user enumeration and recommends
  uniform responses; OWASP's Authentication Cheat Sheet recommends equal-time responses for
  login/password-reset.
- **argon2 / bcrypt cost**: verification commonly takes tens of milliseconds by design; that is the
  signal you are trying to hide, so always pay it (real or dummy) on the failure path.
- **Statistical separation**: distinguish signal from jitter by comparing medians **and** standard
  deviations over many samples; a few samples prove nothing.

## Real-world use case — Acme SaaS

Acme's password-reset endpoint responded in ~4 ms for unknown emails and ~70 ms for known emails
(it only generated and emailed a token for known ones). A researcher enumerated 12,000 registered
emails via the latency gap alone, with no rate limit triggering because each request was valid. Fix:
the endpoint now always generates a token (for unknown emails it discards it), always writes a
uniform audit record, returns an identical `200` "if an account exists…", and is rate-limited per IP
and per email. Post-fix, the two medians were within a few milliseconds across 500 samples.
`WebhookIngest` signature checks were also converted from `===` to `timingSafeEqual`, closing the same
class of bug on a different path.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Constant-work auth path | No timing oracle | Small extra CPU per miss | All auth/reset endpoints |
| Uniform response, no timing fix | Cheap | Still enumerable via latency | Insufficient alone |
| DoS-hardened constant time (dummy hash plus rate limit) | Robust | Rate limits can annoy users | Public auth endpoints |

## Common mistakes

- **`===` on secrets.** Use `timingSafeEqual`/`compare_digest`/`subtle`.
- **Comparing raw values instead of digests.** Length differences leak; hash to fixed length.
- **A "constant-time" function that early-returns on length.** Not constant-time.
- **Dummy hash with the wrong algorithm/cost.** The oracle returns.
- **Only fixing the message.** Body length and latency still differ.
- **Skipping the DB lookup for malformed input.** Reintroduces a fast path.
- **Trusting a single sample.** Always measure with enough samples to defeat jitter.

## Checklist

- [ ] Are all secret/signature comparisons constant-time?
- [ ] Does the login path always run a real-cost hash, real or dummy?
- [ ] Is the unknown-user response identical in code, message, length, and timing?
- [ ] Do reset/signup paths avoid confirming account existence?
- [ ] Have you measured the timing gap with enough samples?
- [ ] Are auth endpoints rate-limited per IP and per account?

## Related

- [Authorization Disclosure, Enumeration, and Timing](../01-concepts/04-authorization-disclosure-enumeration-and-timing.md)
- [Chapter 35 — Authentication, Authorization, and Tenant Isolation Errors](../../35-auth-authorization-and-tenant-isolation-errors/README.md)
- [Chapter 33 — Webhook Signatures](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/01-concepts/04-webhook-signatures-retries-timeouts.md)
- [Information Disclosure Channels](./01-information-disclosure-channels.md)
- [Glossary](../../../GLOSSARY.md)
