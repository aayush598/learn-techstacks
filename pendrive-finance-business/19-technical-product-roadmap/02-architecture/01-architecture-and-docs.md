# 01 — Architecture & Documentation (Keep the Codebase Sane)

The source already has an architecture (see `docs/architecture/`). This chapter tells you how to USE it and keep it healthy as you build the business on it.

## Existing Architecture (map — from the source)

| Doc | Concern |
|-----|---------|
| 1-high-level-architecture | Overall component interaction |
| 2-metadata-engine | Metadata schema, validation, versioning |
| 3-runtime-engine | Runtime execution & rendering pipeline |
| 4-database-engine | Database design, encryption, optimization |
| 5-security-engine | Security model (AES, auth, RBAC, audit) |
| 6-designer-architecture | Visual designer components |
| 7-workflow-engine | Workflow execution design |
| 8-report-engine | Report generation pipeline |
| 9-deployment-engine | USB/packaging system |
| 10-plugin-system | Plugin architecture |

**Source layout:** `src/` has `runtime`, `designer`, `business`, `common`, `libs`. `tests/` has unit + integration tests.

## How To Work With It (as a founder, not just a dev)

- **Business layer first** (`src/business`): wrap your niche finance modules here (billing, inventory, accounting) — this is the highest-value code.
- **Reuse `common`/`libs`** — don't reinvent utilities.
- **Designer + Runtime are your sales tools** — keep them stable; a broken designer halts customization.
- **Keep metadata versioned** (Part 19 ch. 3) — your customer templates ARE data; versioning protects them.

## Documentation Discipline (you'll thank yourself)

- **Keep README + PLAN updated** as you change scope.
- **Document every module** you add (what it does, fields, reports) — mirrors Part 02 module library.
- **Record "how to build a niche template"** — so you (or a future helper, Part 13) can repeat it.
- **Changelog** — track what changed each release (helps support + renewals, Part 10/04).

## Source Control (non-negotiable)

- **Commit often, small, with clear messages** (`feat:` / `fix:` / `docs:`).
- **Branch for features**; keep `main` stable/sellable.
- **Never commit secrets** (encryption keys, passwords) — use config/env (Part 07/11 security).
- **Tag releases** (v0.1.0, v1.0.0) — map to what you actually shipped/sold.

## The "Sellable" Branch Concept

Keep a branch/version that is **proven sellable** (tested, stable). Only merge enhancements that pass QA (Part 19 ch. 3). Never ship from an in-progress branch.

## Documentation As An Asset

Good docs + versioning = a business you can delegate/scale/sell (Part 13). A messy codebase is a liability. Treat docs as part of the product.

---

**Next:** `19-technical-product-roadmap/03-quality-ci/01-quality-and-ci.md`