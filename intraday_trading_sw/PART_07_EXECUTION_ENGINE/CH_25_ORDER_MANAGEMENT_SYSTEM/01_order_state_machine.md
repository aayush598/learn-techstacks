# 01 — Order State Machine

## Purpose
Define every legal order state and every legal transition, so the system can
never be in a contradictory state (e.g., "filled" and "pending" at once).

## States
`NEW` → `ACK` → `LIVE` → `FILLED`
                      ↘ `PARTIAL` → `LIVE` (resume) / `FILLED`
          `REJECTED` (from NEW/ACK)
          `CANCELLED` (from LIVE/PARTIAL)
          `EXPIRED` (timeout/end-of-day)
          `UNKNOWN` (response lost — must reconcile before any other action)

## Legal transitions (whitelist)
- NEW → ACK | REJECTED
- ACK → LIVE | REJECTED
- LIVE → FILLED | PARTIAL | CANCELLED | EXPIRED
- PARTIAL → LIVE | FILLED | CANCELLED
- UNKNOWN → (reconcile) → any resolved state
Any other transition = bug: raise, alert, halt for that symbol.

## Pseudo-code: transition guard
```
def transition(st, ev):
    if ev not in ALLOWED[st]:
        alert(f"illegal_transition {st}->{ev}")
        risk.circuit_breaker("oms_state_error")
        return
    state = ev; journal.append({st, ev, ts})
```

## Event payload (audit completeness)
`{internal_id, broker_id, event, ts, price?, qty?, reason?, raw_payload}` —
raw_payload preserved for forensic debugging (CH_33).

## Rule interactions
- FILLED/PARTIAL events update positions (CH_24/03).
- CANCELLED/EXPIRED trigger bracket cleanup (CH_03/01).
- Any order still LIVE at the close → flatten/expire per policy (CH_23/01).

## Rules
- State changes are persisted before notifications (journal-first, CH_25/00).
- The state machine is unit-tested exhaustively (every transition, CH_36).
- UNKNOWN is transient: the OMS resolves it by reconciliation before proceeding.
