# MEMBER REGISTRY — FORMAT

**Folder:** `01-MEMBERSHIP/04-Member-Registry/`

---

## 1. PURPOSE

The Member Registry is the single authoritative list of who belongs to the
system, who owes what, and who may vote and take water. It is the backbone of
P6 transparency: if it is not in the registry, it did not happen.

## 2. THE REGISTRY TABLE

The registry is a single table with the following standard columns:

| Column | Content | Updated by |
|--------|---------|------------|
| **Connection ID** | Unique ID, e.g., `CWSS-001`; never reused | Registry Keeper |
| **Household** | House/plot number and street in the colony | Registry Keeper |
| **Member name** | Registered connection holder's full name | Registry Keeper |
| **Contact** | Phone number (or neighbour's, if none) | Registry Keeper |
| **Phase** | Founding / Regular / Late joiner / Tenant / On leave / Exited | Registry Keeper |
| **Buy-in status** | Total buy-in, paid amount, balance, installments | Registry Keeper + Finance |
| **Dues** | Monthly contribution arrears, outstanding charges | Finance |
| **Duty status** | Current roster position, leave, cover charges | Duty coordinator |
| **Notes** | Grievances pending, hardship flag, corrections log | Various, per rule |

The printed template is `12-TEMPLATES/01-Membership-Application.md` (the
application) and the registry ledger layout is kept with the Finance
bookkeeping templates in `06-FINANCE/03-Bookkeeping/`.

## 3. FORMAT RULES

1. **One row per connection.** A connection ID appears exactly once. History
   (changes of holder) is kept in the notes and a change log, not by
   overwriting rows blindly.
2. **Written in ink or a single master digital sheet.** If digital, it is
   versioned and backed up weekly; if paper, entries are made in ink and
   corrections are struck out (never erased) with date and initials.
3. **Numbered pages** that are counted and signed at every handover
   (`02-Registry-Keeper-Rotation.md`).
4. **Rupee amounts** in INR, with dates, so every figure can be cross-checked
   against receipts.

## 4. MAINTENANCE RULES

| Event | Action |
|-------|--------|
| New admission | New row added within 7 days |
| Buy-in payment | Paid and balance columns updated with receipt number |
| Monthly contribution | Dues column updated at month end by Finance |
| Duty turn | Duty status updated by the duty coordinator |
| Change of occupant | Holder/contact updated; history preserved in notes |
| Exit / transfer | Row marked exited/transferred; ID retired |

## 5. THE CHANGE LOG

- Any change to a row records: what changed, when, by whom, and why.
- A member whose own row is changed without their knowledge can demand a
  correction and an explanation; unexplained changes are a Level 2 offence.

## 6. ACCESS

- Every member may inspect the registry at any announced time (P6).
- A member may photograph **their own** row; they may read, but not copy,
  other members' rows (see `03-Data-Privacy-Rules.md`).
- The registry may not be taken home by a single keeper permanently; it stays
  in the system's custody and travels only for assemblies and audits.

## 7. EXAMPLE FROM COLONY LIFE

A member claims at an assembly that "the new family never paid their buy-in."
The Registry Keeper opens the row for `CWSS-022`: buy-in ₹24,000, paid
₹24,000, balance ₹0, final receipt no. 88. The claim collapses on evidence,
and the maker of the false claim is warned for spreading falsehood — because
the registry makes truth cheap and rumour expensive.

## 8. RECONCILIATION

- At every monthly assembly, the registry's dues column is reconciled with the
  Finance books. Discrepancies are resolved before the meeting ends, or are
  recorded as an open issue with a date.

---

*The registry is the memory of the system. A system with a clean registry can
answer any accusation with a row and a receipt.*
