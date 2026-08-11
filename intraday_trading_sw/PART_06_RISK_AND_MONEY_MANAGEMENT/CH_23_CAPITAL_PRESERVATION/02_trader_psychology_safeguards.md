# 02 — Trader Psychology Safeguards

## Purpose
Design the software so human emotion — greed, fear, revenge, overconfidence —
cannot override the rules.

## Where emotion enters (and how the software blocks it)
1. **Manual overrides**: UI must not offer "cancel risk check", "go bigger",
   "one more trade". Any manual order still passes the full risk gate (CH_20/00).
2. **Revenge trading**: consecutive-loss counter (CH_23/01) pauses the system;
   the trader is informed, not enabled.
3. **Chasing**: entries are only accepted from the strategy/risk pipeline at
   predefined levels — no mid-move "jump in" button that bypasses rules.
4. **Average-down temptation**: strategy defines its own add/scale rules; manual
   adds on losing positions are blocked by the per-trade/portfolio gates.
5. **Overtrading after wins**: profit-target halt (CH_23/01) is automatic.
6. **Grief/loss aversion**: after a loss, daily limits (not mood) govern.

## Human-verifiable guardrails
- Kill switch: a big red **FLAT ALL** that is always available and always works
  (exercises through the same broker layer with top priority).
- Read-only demo of risk decisions: every rejected order shows the reason, so
  the trader learns the rules instead of fighting them.
- Daily journal: system logs decisions vs outcomes for post-session review.

## Pseudo-code: kill switch
```
def kill_switch():
    log("manual_flat", severity=HIGH)
    flatten_all(MARKET)
    halt_new_entries(session)
    alert("manual_flat_requested")
```

## Rules
- UI can add constraints but never remove risk constraints.
- The trader's role is to *review and configure*, the risk layer enforces.
- Psychology safeguards are tested like any feature (QA, CH_36) — the "angry
  user clicks everything" test.
