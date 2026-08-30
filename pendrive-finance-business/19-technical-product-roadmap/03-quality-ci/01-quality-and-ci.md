# 01 — Quality, Testing & (Light) CI (Never Ship Broken Software)

Quality is your reputation (Part 11). This chapter gives you a pragmatic testing + release system that works for a solo dev, without heavy ceremony.

## The Gold Standard (for a solo build)

> **A "main/sellable" build that always passes tests + a manual QA pass before you hand it to a customer.**

## Automated Testing (unit + integration)

The source uses Google Test (see `tests/unit`, `tests/integration`). Aim for:
- **Unit tests** on core logic (calculations, encryption, metadata validation, security).
- **Integration tests** on critical flows (billing math, stock updates, backup/restore, login).
- **Target coverage:** ≥90% on core components (per PLAN.md standards).

**Rule:** Every module has tests before it's "done." A test that fails = feature not done.

## Bug Tracking (simple)

Spreadsheet (Part 14 style):
| # | Bug/Feature | Severity | Reproduce steps | Fixed in | Status |
|---|-------------|----------|-----------------|----------|--------|
| | | High/Med/Low | | | |

- Fix **High** (blocking) first; schedule Med; batch Low into updates.
- **Re-test after every fix** (regression).

## Manual QA Checklist (before ANY delivery)

Run the full checklist in Part 09 ch. 3 on a **clean Windows PC from the pen drive**:
- forms save, billing math correct, stock updates, reports correct, login/permissions, backup restores, offline works, no stray data.

## The "Release" Process (light CI, solo-friendly)

1. **Develop** on a feature branch.
2. **Run automated tests** + fix till green.
3. **Manual QA pass** (checklist above).
4. **Merge to `main`** (sellable branch).
5. **Tag a release** + write changelog + build the pen drive image.
6. Only then is it a version you sell/deliver.

> Full CI (GitHub Actions/etc.) is optional and helpful — build + run tests on every push. Start simple; add automation when it saves you time.

## Versioning & Backups

- **Keep prior versions** — if a new build has an issue, roll back to the last sellable one.
- **Back up** your build tools, source, and every template/config (Part 09).
- **Migrate old data safely** — test migrations before applying to customer data.

## Performance Snapshot (from PLAN.md)

- Form load < 100ms; report generation < 2s for 10k rows.
- Watch these as you add modules — keep delivery snappy for the customer's old PC.

## When You Don't Have Time To Test (danger)

Never use "no time" as an excuse to skip QA. A single broken delivery costs more (reputation + refunds) than the QA time (Part 11). **If you can't QA it, don't ship it.**

---

**Next (Part 20):** `../20-sop-runbooks/`