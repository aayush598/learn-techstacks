# 00 — Licensing and Attribution

## Purpose
Choose and document the project's license and every attribution obligation —
clarity is what makes "open source" trustworthy.

## Code license (decision to make first)
- Recommended: **Apache-2.0** (permissive, includes explicit patent grant) or
  **MIT** (simplest). Decide once and put it in the repo root as `LICENSE`.
- Never mix licenses casually: each module/package keeps its own header if the
  license requires it.

## Attribution files
- `NOTICE` — third-party copyright notices.
- `THIRD_PARTY_LICENSES` — per-dependency license text (generated/audited in CI).
- Data sources: redistribution terms documented per source (CH_05, CH_39/02).

## Steps to release-ready licensing
1. Choose license; add `LICENSE` + headers.
2. Generate dependency license report; fix or remove unlicensed deps
   (dependency minimization helps here, CH_00/02).
3. Document data licensing explicitly (what can/cannot ship in the repo).
4. Add a `COPYRIGHT`/`CONTRIBUTORS` policy (who owns what).

## Pseudo-code: CI license check
```
audit_licenses():
    for dep in deps: assert dep.license in ALLOWED_SET
    assert LICENSE exists and matches config
    assert NOTICE present
```

## Rules
- Code = one permissive license; data = separate, per-source terms.
- No dependency enters the repo without a known, allowed license.
- Attribution obligations are enforced by CI, not by memory.
