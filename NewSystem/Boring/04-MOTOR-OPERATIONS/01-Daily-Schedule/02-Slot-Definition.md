# SLOT DEFINITION

**Folder:** `04-MOTOR-OPERATIONS/01-Daily-Schedule/`

---

## 1. WHAT A SLOT IS

A **slot** is one fixed time window during which the motor runs for a defined
group or area. Every slot has an exact, published definition. A slot that cannot
be described precisely is not a slot — it is a loophole.

## 2. THE EIGHT ELEMENTS OF EVERY SLOT

| Element | Meaning | Example |
|---------|---------|---------|
| **Start time** | The minute the motor is switched on | 05:30 |
| **End time** | The minute the motor is switched off | 06:30 |
| **Group served** | Which area/connection list is served | Group A (Streets 1–3) |
| **Expected duration** | Planned minutes of run | 60 minutes |
| **Yield buffer** | Extra allowed minutes if the borewell yield is low that day | +10 minutes, but only with an entry in the run log |
| **Service target** | The minimum stored volume expected per connection | 200 litres/connection |
| **Fallback run** | A pre-planned window if the primary run misses due to power cut | Same-day evening or next morning |
| **Operator** | The duty operator and backup for the run | From the roster |

## 3. HOW SLOT LENGTHS ARE SET — FAIR SHARE OF PUMPING MINUTES

Slot lengths are not a matter of mood. They follow the **fair share formula**:

1. The assembly determines the **total usable pumping minutes per day** from
   measured discharge yield and recharge (recorded over a full week in the
   Pressure and Quality Log, `04-Monitoring-and-Logs/02-Pressure-and-Quality-Log.md`).
2. Each group's share is proportional to the **number of connections in the
   group**, adjusted for documented physical factors (tap level, pipe distance)
   via `09-PROJECTS-AND-EXPANSION/04-Network-Improvements/01-Tap-Height-Compensation.md`.
3. The resulting minutes are divided into the published slots. A group is never
   given a slot shorter than its fair share because someone "needed more time".
4. The fair-share calculation and its underlying data are published with the
   schedule, so any member can re-check the arithmetic.

## 4. THE YIELD BUFFER

1. Borewell yield varies day to day. Each slot carries a **small published
   buffer** (default 10 minutes, set by assembly) that the operator may use
   **only if**:
   - The group's connection was visibly not filling; and
   - The extra run is logged with the gauge reading at start and end; and
   - The buffer does not push into the next group's slot.
2. If a group still does not receive its share after the buffer, the matter is
   a **missed slot** under `05-Irregularities/02-Missed-Slot-Protocol.md`, not a
   silent loss.

## 5. RECORDING THE ACTUAL RUN

The actual run **must** be recorded immediately, not from memory:

| Field | Source |
|-------|--------|
| Scheduled start/end | The published schedule |
| Actual start/end | The clock read at the motor room, in the log |
| Operator name | Roster + signature in the log |
| Gauge at start/end | `04-Monitoring-and-Logs/03-Pump-Gauge-Recording.md` |
| Any anomaly | Note in the log and a report per `05-Irregularities/04-Reporting-Violations.md` |

The template is `12-TEMPLATES/04-Motor-Run-Log.md`. The Motor Run Log is the
evidence record for every dispute; see `04-Monitoring-and-Logs/01-Motor-Run-Log.md`.

## 6. UNIFORMITY OF SLOT DEFINITION

1. A slot applies to a **group**, never to a named favourite. A group's member
   list is published and updated only by membership procedures.
2. A slot's **start and end** are identical for every member of the group. No
   member may be given a private extension, earlier start, or extra run.
3. Deviations in who actually receives water within a slot (for example, a
   member whose tap fails) are handled by the network compensation rules, not by
   changing the slot.

## 7. SCENARIO: LOW YIELD MORNING

The morning slot starts on time, but the pump delivers weakly because the
borewell level has dropped overnight. The operator:

1. Runs the published slot.
2. Uses the 10-minute buffer if the group is still not served, and logs it.
3. Records gauge readings at start and end.
4. Reports the yield drop through the reporting protocol; the water committee
   checks whether summer grouping must be declared
   (`02-Seasonal-Rotation/01-Summer-Grouping.md`).

No member, however, extends a slot on their own. **Only the schedule, the
buffer, and the log decide.**

---

*Every slot is fully defined before it runs, measured while it runs, and
recorded after it runs. What cannot be defined, measured, and recorded is not a
slot and must not be run.*
