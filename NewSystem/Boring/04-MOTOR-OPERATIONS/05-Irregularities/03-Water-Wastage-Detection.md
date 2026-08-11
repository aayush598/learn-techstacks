# WATER WASTAGE DETECTION

**Folder:** `04-MOTOR-OPERATIONS/05-Irregularities/`

---

## 1. PURPOSE

Wastage steals water from everyone. An overflowing tank, a silent leak, an open
bypass, or a private tanker filled from the colony line all reduce the water
that the schedule promised to other members. This file defines how wastage is
**detected by fact**, reported, and answered.

## 2. WHAT CONSTITUTES WASTAGE

| Act | Example |
|-----|---------|
| **Overflow** | A tank left filling past capacity so water runs down the drain. |
| **Leak** | A member's connection or pipe leaking continuously, unreported for days. |
| **Open bypass** | A valve or bypass line opened so water flows without storage control. |
| **Tanker misuse** | A private tanker filled from the colony line/connection (without the event process) and sold or taken away. |
| **Unreported damage** | A burst pipe left running because "someone else will report it". |

## 3. DETECTION — FOUR MECHANICAL PATHS

| Path | How | Who |
|------|-----|-----|
| **Log cross-check** | Run time × recorded flow rate compared against stored volume. If the motor ran 60 minutes at 60 L/min but tanks only stored 1,000 litres, roughly 2,600 litres went somewhere else. | Duty operator + water committee, weekly |
| **Periodic patrol** | A published, rotating patrol walks the line at slot times checking for overflow, open bypasses, and leaking joints. | Rotating member duty |
| **Member reports** | Any member reports suspected wastage through `04-Reporting-Violations.md`. | All members |
| **Gauge/quality anomalies** | Sustained low pressure with no logged cause points to a leak or open line (`04-Monitoring-and-Logs/03-Pump-Gauge-Recording.md`). | Duty operator |

## 4. THE LOG CROSS-CHECK — A CONCRETE EXAMPLE

1. Published flow rate at normal gauge: 60 litres/minute.
2. Slot: 05:00–06:00 → expected ≈ 3,600 litres stored.
3. End-of-slot storage check: 1,000 litres added.
4. Difference ≈ 2,600 litres — investigation opened: overflow (ball valve
   failed), a leak, or an open bypass.
5. The finding is logged with the evidence (photos, meter readings) and the
   repair/penalty follows.

## 5. RESPONSIBILITY AND CONSEQUENCES

| Finding | Responsibility | Consequence |
|---------|----------------|-------------|
| **Overflow / faulty valve** | The member whose tank/valve it is | Repair within 48 hours (or a published plan); wastage volume charged at normal rate if proven reckless; repeat = Ladder escalation. |
| **Unreported leak on a member's line** | The member | Repair within the timeline; delay after notice attracts a wastage charge. |
| **Open bypass / deliberate diversion** | The member | **Level 3 offence** (`07-CONFLICT-RESOLUTION/05-Enforcement/01-Enforcement-Ladder.md`); water diverted charged at penalty rate; restoration to the affected group. |
| **Private tanker from the line** | The member who arranged it | **Level 4 offence** (stealing common water at scale); full volume at penalty rate + restoration + Ladder; repeated = expulsion process. |
| **Colony-line leak (common pipe)** | The system | Treated as a network fault, repaired from the Repair Fund (`05-MAINTENANCE-REPAIR/`), not charged to members. |

## 6. THE ROTATING PATROL

1. A patrol roster rotates by lot (P2, P3) — no one is the permanent "water
   policeman".
2. The patrol looks for: overflowing tanks during slots, open or tampered
   valves, visible leaks, hoses/couplings drawing water outside the schedule,
   and tankers at the line.
3. The patrol records what it sees in the **patrol log** (time, location,
   observation, photo). A patrol that reports nothing unusual signs a "no
   anomaly" line — a blank patrol day is not a reporting day.

## 7. SCENARIO: THE OVERFLOW THAT LEAKED ALL NIGHT

The evening slot ends and the pump stops. At 22:00 a patrol member finds a
household's overhead tank overflowing — the ball valve has failed and water has
been running down for hours. The patrol photographs it, notes the time, and the
household is informed. The next morning: the overflow is stopped (valve repair
same day), the lost volume is estimated from the flow rate and the hours, and
the household is charged the wastage rate for the proven excess. The affected
group's next-day storage is protected by an early slot. **The water that was
wasted is paid for, the damage is repaired, and the log carries the whole
story.**

## 8. WASTAGE IS A MEMBER'S PROBLEM — THE LINE, NOT THE EXCUSE

1. Every connection is responsible for its own line and valves, per the
   membership agreement (`01-MEMBERSHIP/`).
2. "It was already broken" does not excuse silence; **reporting a leak
   immediately** is the duty that keeps the colony's water in the system
   (`00-CONSTITUTION/03-Fundamental-Duties/04-Duty-to-Protect-Common-Resources.md`).
3. A member who reports a leak on their own line faces **no penalty** — the
   repair timeline applies, and the colony's water is saved.

---

*Wastage is detected by arithmetic and patrol, proven by the log, and answered
by repair, recovery, and the Ladder. Every litre wasted is a litre stolen from a
scheduled promise — and the schedule does not forgive.*
