# 03 - STOCK REFILL PROCESS

**Folder:** `05-MAINTENANCE-REPAIR/05-Parts-and-Inventory/`

---

## 1. PURPOSE

A spare-parts inventory works only if it is **refilled before it is empty**.
The refill process is mechanical: it triggers on levels, is budgeted in
advance, and is executed without panic. A colony that refills only after a
breakdown has already lost the point of the inventory (P9).

## 2. MINIMUM LEVELS — THE REFILL TRIGGER

Each stocked part has a **minimum level** recorded in the inventory ledger.
When the balance falls to the minimum, a refill is triggered:

| Part | Minimum level | Refill target |
|------|---------------|---------------|
| Capacitor | 1 | 2 |
| Starter/contactor | 0 (1 in stock) | 1 |
| Cable (coil) | 0 | 1 |
| Fuses / fuse wire | ½ box | 1 box |
| Unions / valves | 1 | 2 |
| Foot valve / strainer | 0 (1 in stock) | 1 |
| Consumables (tape, sealant) | 1 each | 2 each |

1. The trigger is checked automatically at every quarterly count and after
   every stock issue.
2. When triggered, the custodian notes "REFILL NEEDED" in the ledger and the
   Repair Committee processes the refill.
3. A part at minimum level that is also the only one of its kind is flagged
   as a **critical gap** and refilled within 7 days, not at the next quarter.

## 3. THE REFILL CYCLE

| Step | Who | Detail |
|------|-----|--------|
| 1. Identify | Custodian / quarterly count | List parts at or below minimum |
| 2. Price | Repair Committee | Obtain 2 prices from approved suppliers (`04-Vendor-Management/02-Multiple-Quotes-Rule.md`) for stock above ₹1,000 total |
| 3. Approve | Within approved PM budget: committee; beyond budget: assembly | Recorded decision |
| 4. Buy | Committee member + witness | Purchase against the approved list; receipt and voucher saved |
| 5. Receive and verify | Custodian + second member | Count, check spec/brand, enter In entries in the ledger |
| 6. Publish | Committee | Refill summary published (items, cost, stock level) |

## 4. BUDGET AND MONEY

1. Routine refills are within the annual PM budget
   (`01-Preventive-Maintenance/04-PM-Budget.md`) — the "spare stock refill"
   line.
2. A refill that exceeds the budget line requires assembly approval.
3. Refills are paid from the Repair Fund by voucher, never in cash
   (`06-FINANCE/03-Bookkeeping/02-Expense-Voucher-Rule.md`).
4. **No panic buying.** During a breakdown, the colony does not buy parts at
   whatever the shop demands — it uses its stock and refills calmly afterwards,
   at normal prices. This is the whole economic point of the inventory.

## 5. SEASONAL REFILL CYCLES

| Before | Refill emphasis |
|--------|-----------------|
| **Summer (March)** | Capacitors, starters (winding stress), valves, hose |
| **Monsoon (June)** | Cable, glands, weather covers, earthing items |
| **Post-monsoon (October)** | Fuses, sealant, general consumables |

These are checked during the PM rounds of those seasons
(`01-Preventive-Maintenance/01-PM-Schedule.md`).

## 6. SCENARIO — THE EMERGENCY SHOP

During a July night power surge, the starter burns out. The inventory has a
matching starter in stock. The fault is fixed the same night, and the refill
trigger fires: the minimum level for starters is 0, so "REFILL NEEDED" is
logged. Next week, at normal shop prices and with two quotes, the starter is
replaced in stock. The colony never entered the emergency market, never paid
panic prices, and never waited.

## 7. CROSS-REFERENCES

| Item | Reference |
|------|-----------|
| What is stocked | `01-Critical-Spare-Parts.md` |
| Ledger and counts | `02-Inventory-Ledger.md` |
| PM budget | `01-Preventive-Maintenance/04-PM-Budget.md` |
| Repair Fund | `06-FINANCE/02-Fund-Management/03-Repair-Fund.md` |
