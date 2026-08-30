# 01 — Platform Build: From Source to a Stable Sellable Product

The product lives in `~/aayush/projects/pendrive_finance/software/`. This chapter gives you a **pragmatic build plan** so you get a stable, sellable platform FAST — without boiling the ocean.

## Core Truth

> You do NOT need all 38 modules to sell. You need a **stable, tested runtime + Designer + your niche templates** that reliably solves the niche's top 3–5 jobs (Part 09). Everything else can come later, funded by sales.

## The "Sell-Ready" Definition (what "done" means to sell)

A platform build qualifies as sellable when:
1. **Runtime** reliably renders forms from metadata (your templates).
2. **Designer** lets YOU build/customize a niche template without coding.
3. **Database** stores data safely (SQLite + encryption).
4. **Security** — login, roles, audit, encryption works.
5. **Backup/Restore** works reliably.
6. **Offline portable** — runs from a pen drive on a clean Windows PC.
7. **Passes the testing checklist** (Part 09) on the niche template.

## Pragmatic Build Order (matches the fast-track MVP)

Focus on the **fastest path to sell**, not the full roadmap:

```
Phase 0: Runtime + DB + Security + Basic forms   [FOUNDATION]
Phase 1: Niche template(s) via Designer          [SELLABLE MVP]
Phase 2: Reporting + printing + export            [REQUIRED for finance]
Phase 3: Billing/Inventory/Accounting modules     [CORE VALUE]
Phase 4: Everything else (workflows, AI, plugins...)  [ITERATE AFTER SALES]
```

## Detailed Build Phases

### Phase 0 — Foundation (the engine)
- **Runtime** — load & render metadata-defined apps, navigation, plugin loader.
- **Database** — encrypted SQLite, CRUD, migrations.
- **Security** — AES-256, Argon2id hashing, RBAC, audit log.
- **Portable USB layer** — autodetect drive, run without installation, no traces.

**Exit:** Can render a basic form, save/read data, login, and run from a pen drive. *Test every part (Part 09).*

### Phase 1 — Designer + First Niche Template
- **Form/Table/Menu designers** — drag & drop, property panel.
- Build your **Retail (or chosen niche) template**: products, billing, customers, stock, reports (Part 09).
- Theme/branding (business name/logo/colors).

**Exit:** You can create & customize a full niche app in the Designer without coding.

### Phase 2 — Reporting, Printing, Export (CRITICAL for finance)
- **Report designer** — invoices, sales summaries, P&L.
- **PDF/invoice printing** (incl. GST invoice format), **Excel export/import**.

**Exit:** Invoice prints correctly with business branding; basic reports correct.

### Phase 3 — Core Finance Modules
- **Accounting** (ledger, journal, P&L, balance sheet).
- **Sales/Purchase/Inventory** (billing, stock, suppliers).
- **Expenses/Income/Cash-Bank**.
- **Taxation/GST** (rates, tax invoices, return-friendly reports).
- **CRM/Vendor/Product** basics.

**Exit:** A complete finance app for your niche — this is your sellable product.

### Phase 4 — Iterate (fund by sales)
- Payroll, fixed assets, loans, budgets, multi-branch, i18n, workflows, AI, plugins — only as customers request/pay (Part 09: never build un-requested features).

## Build Discipline

- **Smallest working slice first** (Part 09). Don't gold-plate.
- **Test-first**: every module has tests before "done" (Part 19 ch. 3).
- **Version & document** every build (Part 19 ch. 2).
- **Back up your own build + build tools.**
- **Time-box** the foundation so you reach a sellable state quickly (Part 15).

## "Too Much Engineering" Warning

Engineering perfection delays revenue. **Use the platform to sell fast; enhance the engine only when it blocks you.** Revenue funds real development.

---

**Next:** `19-technical-product-roadmap/02-architecture/01-architecture-and-docs.md`