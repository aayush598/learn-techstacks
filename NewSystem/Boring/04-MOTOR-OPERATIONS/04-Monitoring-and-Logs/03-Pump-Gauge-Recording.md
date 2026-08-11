# PUMP GAUGE RECORDING

**Folder:** `04-MOTOR-OPERATIONS/04-Monitoring-and-Logs/`

---

## 1. PURPOSE

The pressure gauge at the motor room is the colony's **single honest witness**
to how the pump is behaving. Reading it correctly, at the right times, tells the
colony whether the pump is healthy, whether yield is falling, and whether the
schedule needs adjustment. This file defines how to read it and what the numbers
mean.

## 2. HOW TO READ THE GAUGE

1. The gauge shows **pump discharge pressure** (in bar or kg/cm²) — the
   pressure the pump produces, not the household tap pressure.
2. Read the value **only after the motor has run steadily for 2 minutes**;
   readings in the first seconds are unsteady and misleading.
3. Record the value at **start** (after warm-up) and **stop** of every run, into
   the Motor Run Log (`01-Motor-Run-Log.md`).
4. Tap the glass gently if the needle sticks; read straight-on, not at an angle,
   to avoid parallax error.
5. If the needle vibrates or the gauge is damaged, log "gauge suspect" and
   arrange replacement through the maintenance track.

## 3. THE STANDARD OPERATING VALUES

The assembly publishes the **standard operating range**, fixed by the pump's
rating and the pipeline layout:

| Reading | Meaning |
|---------|---------|
| **Normal range** (published, e.g. 3.0–4.5 bar) | Pump healthy, yield normal. |
| **Above normal range** | Blockage downstream, or a valve closed — pressure building against a closed line. Risk of burst pipe. |
| **Below normal range** | Falling yield, worn impeller, air in the line, or a leak opening downstream. |
| **Reading drops steadily within one run** | Borewell water level falling faster than recharge — a yield problem. |
| **Zero / no pressure with motor running** | Pump running dry or prime lost — stop and report immediately to protect the pump. |

## 4. WHEN AN OUT-OF-RANGE READING = A FAULT REPORT

| Reading | Immediate action | Track |
|---------|------------------|-------|
| Above normal range | Do not continue long runs; reduce run and check for closed valve | Fault report → `05-MAINTENANCE-REPAIR/02-Breakdown-Repair/01-Fault-Reporting.md` |
| Below normal range for 2 consecutive runs | Record, monitor, and report; check yield and pump | Fault report (minor/fault check) |
| Running dry (no pressure) | **Stop the motor** to prevent burn-out | Emergency → `10-RISK-AND-EMERGENCY/02-Motor-Breakdown/` |
| Gauge frozen or erratic | Log as suspect; replace the gauge | Maintenance |

**The duty operator is the first line of this check** and is never penalised for
stopping the motor on a proven dry-run reading — stopping to protect the pump is
a logged, protected action, not an unauthorized stop
(`01-Daily-Schedule/04-Notification-Protocol.md`).

## 5. LINKING GAUGE TO THE LOG

1. Every out-of-range reading is written into the Motor Run Log with the fault
   number once reported.
2. The gauge trend (start-to-stop values over the week) is summarised weekly by
   the water committee and used for:
   - Yield-based decisions (grouping, `02-Seasonal-Rotation/01-Summer-Grouping.md`)
   - Compensation evidence (`02-Seasonal-Rotation/03-Slot-Fairness-Compensation.md`)
   - Repair priority (`05-MAINTENANCE-REPAIR/`)

## 6. WHO MAY TOUCH THE GAUGE AND PUMP SETTINGS

1. The **duty operator** may read the gauge and log it — and may stop the motor
   on a proven dry-run reading.
2. Only the **trained repair team** may adjust the pressure switch, valve, or
   pump settings, with a logged work order.
3. **No one else adjusts pump settings.** A changed setting is a tampering
   offence unless covered by a logged work order
   (`05-Irregularities/01-Unauthorized-Turning-On.md`).

## 7. SCENARIO: "THE PRESSURE FELL BY HALF"

One morning the gauge reads 2.0 bar instead of the usual 3.8. The operator logs
it, runs the slot, and reports the anomaly. The next day it reads 1.8. The
water committee opens a fault check: impeller wear is found and the repair is
scheduled. Meanwhile the affected group's low storage is compensated from the
same logs. **No member had to complain twice; the gauge had already spoken.**

---

*The gauge is the colony's witness. It is read at every run, compared against
the published range, and reported the moment it lies outside it. The pump's
health is never a secret and never a guess.*
