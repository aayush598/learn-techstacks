# 02 — Open Source Obligations

## Purpose
Keep the project genuinely open while honoring the obligations that come with
open source (and any third-party licenses).

## License choices (documented in CH_12/CH_41)
- Choose a permissive license for code (e.g., Apache-2.0 / MIT) — decide once,
  document clearly.
- **Data is not code**: market data has its own licenses; distribution rules
  differ and may not permit redistribution at all. Ship tools + your own
  downloaders, not vendor data files, unless licensed.
- **Attribution**: keep third-party license texts and notices (NOTICE file).

## Obligations checklist
- [ ] LICENSE file present and correct.
- [ ] Third-party package licenses documented (dependency audit, CH_41).
- [ ] Data sources' redistribution terms documented (CH_05).
- [ ] Contributor agreement / DCO policy defined (CH_42/00).
- [ ] Trademark/name usage rules, if any, stated.
- [ ] Security policy: how to report vulnerabilities privately (CH_41).

## Why this matters for trust
- Users will deploy this to trade real money; license clarity and provenance
  are part of their due diligence.
- Undisclosed dependencies or data licenses = legal risk for every user.

## Rules
- No proprietary code in the repo; no "open-core" surprises in core modules.
- Every dependency has a license note; an audit job checks this (CH_41 CI).
- If a license question arises, resolve it in the open (issues, CH_42/01).
