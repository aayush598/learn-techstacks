# REPAIR FUND

**Folder:** `06-FINANCE/02-Fund-Management/`

---

## 1. WHAT THE REPAIR FUND IS

The Repair Fund is the dedicated pool for **keeping the system running**:
preventive maintenance (PM) and breakdown repairs. In the old system a repair
was an open cheque — the money-keeper quoted any amount, added his margin,
and nobody could check the cost. The Repair Fund, by contrast, is a bounded
sub-account spent **only** through the published approval matrix, so the cost
of every repair is decided before money moves and verified after.

## 2. WHAT IT COVERS

| Item | Source rule |
|------|-------------|
| Preventive maintenance (greasing, servicing, electrical checks, pump tests) | `05-MAINTENANCE-REPAIR/01-Preventive-Maintenance/` |
| Breakdown repairs (motor, starter, pipes, valves, cables) | `05-MAINTENANCE-REPAIR/02-Breakdown-Repair/` |
| Vendor labour and materials | `05-MAINTENANCE-REPAIR/04-Vendor-Management/` |
| Consumables and spare parts | `05-MAINTENANCE-REPAIR/05-Parts-and-Inventory/` |

It does **not** cover: power bills, stipends, new boring, new motor — those
are Common Fund and Reserve Fund items.

## 3. HOW IT IS FILLED

1. The Annual Budget allocates a **monthly Repair Fund provision**, a fixed
   line item (for example, 5-8% of the monthly contributions, or a fixed sum).
   This is part of the monthly contribution formula
   (`01-Contributions/01-Monthly-Contribution.md`).
2. Every month the Finance Committee **transfers** the provision from the
   Common Fund to the Repair Fund. The transfer is recorded in the ledger with
   a voucher and appears in the statements.
3. The Repair Fund may also receive a share of year-end surplus by assembly
   decision (`05-Distribution-and-Refunds/01-Surplus-Distribution.md`).
4. If the Repair Fund runs low mid-year, the Finance Committee may not
   quietly raise the provision; it reports to the assembly, which decides
   between a budget reallocation or a crisis call
   (`05-Fund-Raise-Crisis-Calls.md`).

## 4. THE MINIMUM AND THE FLOOR

1. The Repair Fund keeps a **floor** equal to one typical breakdown cost (for
   example, the cost of a common motor repair), set in the Annual Budget.
2. Spending that would push the Repair Fund below the floor needs a written
   assembly note (`03-Bookkeeping/05-Annual-Budget.md`) or a 3/4 vote for a
   declared emergency.

## 5. HOW IT IS SPENT — THE APPROVAL MATRIX

No repair rupee moves without the matrix. The full matrix is in
`05-MAINTENANCE-REPAIR/02-Breakdown-Repair/03-Repair-Approval-Matrix.md`.
In summary:

| Repair size | Approval needed |
|-------------|-----------------|
| Small (below the small-threshold, e.g. ₹1,000) | Duty/PM team decision, voucher + receipt, reported at next meeting |
| Medium (up to the medium-threshold, e.g. ₹10,000) | Finance Committee + one independent member, two quotes |
| Large (above medium-threshold) | Assembly vote on a published cost sheet, three quotes |

Every repair ends with a **voucher with attachments** (quote, invoice, before
and after photos where possible) filed in date order
(`03-Bookkeeping/02-Expense-Voucher-Rule.md`).

> **Scenario:** A member reports the motor tripping. Another member appears
> with "a mechanic who will do it for ₹6,000, cash only." This is rejected on
> the spot: no cash, the amount triggers the medium lane, two quotes are
> required, and the voucher is filed before payment.

## 6. NO REPAIR, NO REQUEST — "REPAIR" IS NOT AN EXCUSE

1. Money leaves the Repair Fund **only** against a repair request recorded in
   the log with a fault description (`05-MAINTENANCE-REPAIR/02-Breakdown-Repair/`).
2. Collecting contributions "for repair" is **forbidden**. The monthly
   contribution already contains the repair provision; a separate repair
   collection is a red flag (Level 4 if unrecorded).
3. If a member alleges a repair happened but no log entry, no matrix approval,
   and no voucher exist, it is treated as suspected misappropriation
   (`04-Audit/05-Misuse-Consequences.md`).

## 7. TRANSPARENCY

- Repair Fund balance, provision transfer, and every repair spend appear in
  the bimonthly statement (`03-Bookkeeping/04-Bimonthly-Statement.md`).
- Repair vouchers and quotes are public records open to any member
  (`04-Audit/04-Right-of-Any-Member-to-Audit.md`).
- A member can always answer "what did the last repair really cost?" by
  reading the public file — the exact reason the old system is gone.

---

*Repair Fund and Common Fund work together: the Common Fund fills it monthly,
the matrix spends it, and the audit checks it. Nobody guesses, nobody
pockets.*
