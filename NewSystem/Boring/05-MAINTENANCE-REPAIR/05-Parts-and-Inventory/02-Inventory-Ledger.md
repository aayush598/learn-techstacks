# 02 - INVENTORY LEDGER

**Folder:** `05-MAINTENANCE-REPAIR/05-Parts-and-Inventory/`

---

## 1. PURPOSE

Stock disappears when nobody counts it. The inventory ledger makes every part
**counted, traceable, and public** — where it came from, where it went, which
repair it served, and what it cost (P6). A part that is "in the cabinet" on
paper but not in fact is a discovered loss, not a shrug.

## 2. THE LEDGER FORMAT

The ledger records every part with a running balance, one row per movement:

| Date | Item | Opening | In (+qty) | Out (-qty) | Balance | Used for (fault no.) | Cost | Taken by | Signature |
|------|------|---------|-----------|-----------|---------|----------------------|------|----------|-----------|
| 10-Jun-2026 | Capacitor 50uF | 2 | 0 | 1 | 1 | F-2026-018 | — | A. Mehta | A. Mehta |
| 12-Jun-2026 | Capacitor 50uF | 1 | 2 | 0 | 3 | (purchase) | ₹380 | R. Iyer | R. Iyer |

## 3. RULES OF THE LEDGER

1. **Every movement is logged on the day it happens.** A part taken out on
   Monday and logged on Friday is treated as unrecorded until proven.
2. Each entry names the **fault number or PM round** the part served. Stock
   released without a fault number is a red flag.
3. **In** entries cite the purchase voucher (`06-FINANCE/03-Bookkeeping/02-Expense-Voucher-Rule.md`);
   **Out** entries are signed by the taker.
4. The ledger lives in the motor room register or the shared spreadsheet,
   backed up monthly. It is public; any member may inspect it.
5. The ledger is separate from the cash books but reconciled with them: every
   rupee spent on parts appears in both.

## 4. THE CUSTODIAN

1. One committee member is the **inventory custodian** for a month, rotating
   monthly, so no single person controls the stock year-round (P3).
2. The custodian issues parts, logs movements, and keeps the cabinet key (or
   shares the motor-room dual-key rule
   (`03-ROTATION-DUTY/05-Key-and-Control/`)).
3. Handover of the custodian role includes a physical count and a signed
   transfer note.

## 5. QUARTERLY COUNT

1. **Twice a year** (before summer and before monsoon) — and **annually** with
   the stock refill — the stock is physically counted by **two members**, at
   least one of whom is not the custodian.
2. The count sheet lists: part, ledger balance, counted quantity, difference.
3. Results:

| Difference | Action |
|-----------|--------|
| Within normal use | Recorded; ledger adjusted with the using fault numbers |
| Unexplained shortage | Recorded as a loss; investigation follows; if loss is deliberate, a Level 3-4 offence |
| Surplus | Recorded; verify the ledger is not under-issued |

4. The count sheet is signed by both counters and published.

## 6. USEFULNESS IN DISPUTES

1. When a repair claims "we used ₹1,200 of parts", the ledger shows exactly
   which parts, from where, for which fault — and the vendor's invoice is
   cross-checked against it.
2. A vendor who bills for a part that the colony already has in stock is
   caught by the ledger, not by luck.
3. In a handover or a dispute about who took what, the ledger is the evidence.

## 7. SCENARIO — THE VANISHING TAPE

Members suspect stock is leaking out of the motor room. The physical count
shows two coils of cable unaccounted for, while the ledger says they are in
stock. The custodian cannot produce a fault number for them. The loss is
recorded and reported; the custodian is questioned under the conflict process;
the enforcement ladder applies. Without the ledger and the count, the tape
would simply have "gone".

## 8. CROSS-REFERENCES

| Item | Reference |
|------|-----------|
| What is stocked | `01-Critical-Spare-Parts.md` |
| Refill process | `03-Stock-Refill-Process.md` |
| Voucher rule | `06-FINANCE/03-Bookkeeping/02-Expense-Voucher-Rule.md` |
| Enforcement ladder | `07-CONFLICT-RESOLUTION/05-Enforcement/01-Enforcement-Ladder.md` |
