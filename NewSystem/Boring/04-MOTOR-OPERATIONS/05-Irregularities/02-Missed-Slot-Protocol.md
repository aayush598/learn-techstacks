# MISSED SLOT PROTOCOL

**Folder:** `04-MOTOR-OPERATIONS/05-Irregularities/`

---

## 1. PURPOSE

Sometimes a slot is missed — a power cut, a motor failure, a pipe burst, or an
operator error. The old system let such losses fall silently on whoever was
least able to complain. This protocol makes **every missed slot visible,
compensated, and logged**. There is no "silent loss" in the new system.

## 2. WHAT COUNTS AS A MISSED SLOT

| Cause | Example |
|-------|---------|
| Power failure | Grid cut during the slot |
| Motor failure | Pump trips or burns mid-run |
| Network failure | Burst pipe, valve failure, air lock |
| Operator error | Operator absent or late without backup |
| Unauthorized interference | Someone ran the motor earlier and drained the borewell (reported separately under `01-Unauthorized-Turning-On.md`) |

## 3. WHO INFORMS WHOM — THE NOTIFICATION LADDER

| Step | Actor | Action | Time limit |
|------|-------|--------|------------|
| 1 | Duty operator / backup | Confirm the slot is missed and record it in the Motor Run Log | Immediately |
| 2 | Duty operator | Notify the water committee convenor and the issuing officer | Within 15 minutes |
| 3 | Issuing officer | Issue the emergency "slot missed" notice to ALL members through `01-Daily-Schedule/04-Notification-Protocol.md` | Within 30 minutes |
| 4 | Water committee | Decide the compensation method (Section 4) and publish it | Within 24 hours |
| 5 | Duty operator | Execute the compensation run and log it | Per the published time |

A member who learned of the miss by **word of mouth only** is still entitled to
the compensation — the notification failure is a separate reporting issue, not
a reason to deny water.

## 4. COMPENSATION — NO SILENT LOSS

The affected group's water is made up by one of the following, chosen by the
rule in order:

| Method | How it works |
|--------|--------------|
| **Extra slot next day** | The group receives an additional slot (or an extended run) the next day, published and logged, so its weekly volume reaches target. |
| **Credit** | Where the borewell cannot support an extra run, the shortfall is converted to a documented credit for the group per `02-Seasonal-Rotation/03-Slot-Fairness-Compensation.md`. |
| **Priority recovery** | The missed group moves to the front of the next day's order (after medical needs) until its stored volume is back to target. |

1. Compensation is **automatic by rule** — the affected members do not have to
   beg, and no committee member may refuse it.
2. If the miss was caused by an **unauthorized run** (someone drained the
   borewell), the compensation cost is recovered from the offender
   (`01-Unauthorized-Turning-On.md`); the affected group still gets its water
   first.
3. If the miss recurs 3 or more times in a month for the same cause, the
   water committee must investigate the cause as a system problem (yield,
   network, motor) rather than patch each slot.

## 5. RECORDING

1. The miss and the compensation are **two log entries**: one for the missed
   run ("slot missed, power cut, 06:00–07:00") and one for the compensation run
   ("compensation for 14 June, 05:30–06:30").
2. Both are visible in the Motor Run Log and to all members
   (`04-Monitoring-and-Logs/01-Motor-Run-Log.md`).
3. Weekly, the water committee publishes a **missed-slot summary** (count,
   causes, compensation delivered) so the colony can see the pattern.

## 6. OPERATOR ERROR — SEPARATE FROM COMPENSATION

1. The group's compensation is **never denied** because the miss was an
   operator error. The members' water right is independent of the operator's
   performance.
2. The operator's error is handled separately: replacement through the backup
   list, a duty-failure record, and consequences per
   `03-ROTATION-DUTY/04-Duty-Failure/`.
3. A pattern of operator errors at the **same time of day** is investigated as
   possible sabotage (a deliberate attempt to create a recurring miss).

## 7. SCENARIO: POWER CUT AT 06:00

The morning slot for Group A is cancelled by a power cut. The operator logs it,
notifies the committee within 15 minutes, and the officer posts the emergency
notice by 06:45. By 20:00 the committee publishes the compensation: Group A gets
a 06:30–07:30 slot the next morning, ahead of the routine order. The run is
logged with reason "compensation for 15 June". No member of Group A had to
complain, and no member of any other group lost their own slot. **The miss cost
the group one morning and cost the system nothing but one extra logged run.**

---

*A missed slot is an event of the system, not a misfortune of the member. It is
reported, published, compensated, and learned from — always, and for everyone
alike.*
