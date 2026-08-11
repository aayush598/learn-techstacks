# 05 - OPERATIONAL CONFLICTS

**Folder:** `07-CONFLICT-RESOLUTION/01-Conflict-Types/`  
**Cross-reference:** `03-ROTATION-DUTY/`, `04-MOTOR-OPERATIONS/`, `05-MAINTENANCE-REPAIR/`

---

## 1. WHAT THEY ARE

Disputes about how the system runs: who operates when, whose slot was missed,
who left the motor running, who failed to log, whose repair is being done
first, which vendor to call.

## 2. THE DESIGN PRINCIPLE

Operational matters are the most rule-covered area of the system. Almost every
operational question already has a written answer in the roster, the schedule,
the logs, and the repair procedures. An operational conflict is therefore
usually a question of **what the log and the roster say** — not a contest of
personalities.

## 3. THE RULE ORDER FOR OPERATIONAL DECISIONS

| Question | Answered by |
|----------|-------------|
| Who operates when? | The duty roster (`03-ROTATION-DUTY/01-Duty-Roster/`) |
| What time does the motor run? | The daily schedule (`04-MOTOR-OPERATIONS/01-Daily-Schedule/`) |
| Did the motor actually run then? | The motor run log and duty log (`04-MOTOR-OPERATIONS/04-Monitoring-and-Logs/`) |
| Was a duty missed? | The duty log; then `03-ROTATION-DUTY/04-Duty-Failure/` |
| Whose repair comes first? | The repair queue in `05-MAINTENANCE-REPAIR/02-Breakdown-Repair/` (first-in, first-out, by severity) |

## 4. MISSED-SLOT COMPENSATION

If a member's slot was missed because of a system error — operator forgot, motor
broke down, roster mix-up — the remedy is **compensation, not revenge**:

1. The missed member records the miss in writing within 24 hours.
2. The log is checked: was the miss the member's fault or the system's?
3. If the system's fault: a make-up run is scheduled within 3 days, or the
   missed member earns compensation credits at the published rate
   (`04-MOTOR-OPERATIONS/05-Irregularities/`).
4. If the member's own fault: no compensation, but also no punishment beyond
   the published missed-duty rule.

*Example:* The roster shows House 8's slot at 6:00 a.m., but the operator
stopped the motor at 5:45 to catch a bus. House 8 files the miss. The log
confirms it. House 8 gets a make-up run the next morning and time-credits for
the inconvenience. No one is shamed; the operator is reminded of the published
completion rule.

## 5. NO PERSONAL ATTACKS IN OPERATIONAL DISPUTES

Operational disputes are about **actions and records**, not about character.

| Allowed | Not allowed |
|---------|-------------|
| "The log shows you stopped the motor 15 minutes early." | "You are a lazy, careless person and always were." |
| "Your signature is not on the duty log for Sunday." | "You people are always cheating." |
| "This repair quote is higher than the last one." | "You are clearly in league with the vendor." |

A remark that attacks a member instead of the record is itself a violation
(P10, Dignity) and is handled under `01-Interpersonal-Conflicts.md` — separate
from the operational question.

## 6. THE DISPUTE-PROOF LOG

The best operational conflict is the one the logs prevent. Therefore:

- Every run, duty, and repair is logged with date, time, name, and signature
  (`12-TEMPLATES/04-Motor-Run-Log.md`).
- Logs are checked and countersigned by the next duty holder.
- Logs are readable by every member (P6).
- A log entry that is missing or blank is treated as a recorded fact: the
  absence of a record is itself evidence in a dispute.

## 7. WHEN THE LOG AND THE MEMORY CONFLICT

A member may genuinely remember something the log does not show. The rule:

1. The log stands as the official record.
2. The member's account is heard and recorded as a correction request.
3. A correction is accepted only with evidence — a second witness, a photo, a
   time-stamped message, a gauge reading.
4. If the log is found wrong, it is corrected and the correction is logged too.
   The system prefers an honestly corrected log over a confident wrong one.
