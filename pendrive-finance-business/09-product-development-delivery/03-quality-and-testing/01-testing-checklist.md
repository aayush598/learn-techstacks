# 01 — Testing & Quality Checklist (Never Deliver Broken Software)

One broken delivery can cost you referrals and reputation. Make testing automatic and end-to-end.

## The Pre-Delivery Test Checklist (run EVERY time)

### Data & Forms
- [ ] Add / edit / delete records save correctly.
- [ ] Required fields & validation work.
- [ ] Numeric totals (billing, tax, discount) calculate correctly.

### Billing & Invoices
- [ ] Create a sale; invoice prints with correct business name/logo/GST.
- [ ] Discount/tax correct.
- [ ] Credit/cash handling correct.

### Stock & Inventory
- [ ] Sale reduces stock correctly.
- [ ] Reorder alerts fire when below threshold.
- [ ] Purchase/stock-in adds correctly.

### Reports
- [ ] Sales / profit / customer-ledger reports show correct numbers.
- [ ] Date filters work.
- [ ] Export (Excel) works if promised.

### Security & Users
- [ ] Login works; passwords protected.
- [ ] Roles/permissions enforced (staff can't see everything).
- [ ] Audit trail records actions.

### Backup & Restore
- [ ] Backup creates a file.
- [ ] **Restore actually works** (test once — restore into a copy and verify data).

### Offline / Portability
- [ ] Runs from the pen drive on a **clean Windows PC** (no installation).
- [ ] No internet required.
- [ ] No leftover data from other customers in this copy.

## The "Clean Machine Test" (non-negotiable)

Before delivery, test on a **different, clean Windows computer** (not your dev machine):
- Plug pen drive → app opens → works.
- This catches "works only on my machine" problems.

## Bug Handling During Dev

- Track bugs simply (spreadsheet): description, how to reproduce, fix status.
- Fix blockers first; note minor ones for next update.
- Re-test everything after any fix (regression).

## When To Bring A Second Pair of Eyes

- For after your own test, ask a **friend/tester** to click through and break it.
- Fresh eyes find what you're blind to.

## The "Demo-Readiness" Test

The version you show in demos **must be rock solid** (a crash in a demo kills the sale):
- Demo on your most stable build.
- Have backup access/computer ready in case of failure.
- Practice the demo flow (Part 05).

## Quality = Referrals

Reliable software + good support = customers who refer you (Part 10). Quality is not a cost — it's your cheapest marketing.

## Known-Issues Discipline

- If you know a limitation, **tell the customer upfront** (honesty protects trust).
- Offer a workaround or timeline for fix.
- Never ship something and hope they don't notice.

---

**Next:** `09-product-development-delivery/04-hardware-fulfillment/01-pendrive-selection.md`
