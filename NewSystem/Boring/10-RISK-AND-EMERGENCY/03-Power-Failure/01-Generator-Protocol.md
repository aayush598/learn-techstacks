# 01 - GENERATOR PROTOCOL

**Folder:** `10-RISK-AND-EMERGENCY/03-Power-Failure/`

---

## 1. PURPOSE

The borewell motor needs power; power cuts are a fact of the region,
especially in summer. A colony generator (owned or hired) keeps water flowing
through a cut. But a generator is also a noise, a fuel bill, and — in the old
system — a private convenience: "power cut today, the generator runs only for
my house." This protocol makes the generator a **shared, budgeted, scheduled
common asset** (P1).

## 2. DOES THE COLONY HAVE ONE?

1. The assembly decides once a year whether the colony owns a generator, hires
   one on demand, or runs on power-cut duty rotation only.
2. Decision inputs: frequency of cuts (from the run log), bore tank capacity,
   household needs, fuel cost, and the availability of a rental.
3. If owning: the generator is a common asset purchased from the Reserve Fund
   by assembly resolution, kept in the motor room, and inventoried like spare
   parts (`05-MAINTENANCE-REPAIR/05-Parts-and-Inventory/`).
4. If hiring: the approved rental supplier is on the vendor list, with the
   recorded hire rate.

## 3. WHEN THE GENERATOR RUNS

| Situation | Rule |
|-----------|------|
| Power cut expected/announced during supply hours | Generator runs to cover the scheduled slots |
| Cut longer than 2 hours with tank empty | Generator runs to fill the tank / cover the next slot |
| Cut during a crisis (rationing, breakdown) | Generator runs per the ERT's published schedule |
| Off-hours / night, no scheduled supply | Generator does not run for private convenience; exception only by assembly rule |

1. The running schedule is **published in advance** wherever the cut is known,
   or within 30 minutes of an unexpected cut.
2. Generator hours are logged in the motor run log: start, stop, fuel filled,
   litres used, slots covered.

## 4. SHARING AND NOISE RULES

1. Running hours are limited to the supply schedule plus filling time —
   typically not before 6 a.m. nor after 9 p.m. unless an assembly resolution
   extends them for a crisis.
2. The generator is placed for minimum noise nuisance (away from bedrooms,
   muffler maintained). A member whose sick relative needs quiet may request
   a one-time schedule adjustment through the ERT; the request is recorded.
3. Fuel and noise complaints are heard at the assembly; the schedule is a
   public rule, not a negotiable favour.

## 5. FUEL COST

1. Fuel is paid from the **Common Fund** as a power line item (or Repair Fund
   in a breakdown scenario), by voucher — never cash from a member's pocket
   (`06-FINANCE/03-Bookkeeping/02-Expense-Voucher-Rule.md`).
2. Fuel purchases are logged: date, litres, rate, receipt. The fuel tank is
   part of the inventory.
3. A member who uses the generator for a private purpose pays the recorded
   cost per hour plus a penalty; using it without a log entry is an offence.

## 6. WHO OPERATES

1. Only **trained members** operate the generator — a standing list of at
   least 3 trained operators is maintained (`05-MAINTENANCE-REPAIR/03-Skilled-Member-Program/05-No-Over-Reliance-on-Individual.md`).
2. Operation training is part of the duty training
   (`03-ROTATION-DUTY/02-Duty-Training/`).
3. Untrained operation, refueling while hot, and covering the generator are
   safety offences under `04-Health-and-Safety/02-Electrical-Safety.md`.

## 7. SCENARIO — THE PRIVATE POWER

A power cut hits at 6 p.m. during the evening slot. A member with influence
starts the generator "just to pump my sump". Under this rule, the generator's
schedule was published at the cut; the duty operator follows the schedule and
logs the run; the member's private request is refused by the log, not by a
person. The generator served the colony's slot, the fuel was vouchered, and
the member's private use would have been a recorded offence.

## 8. CROSS-REFERENCES

| Item | Reference |
|------|-----------|
| Inverter sharing | `02-Inverter-Sharing.md` |
| Electrical safety | `04-Health-and-Safety/02-Electrical-Safety.md` |
| Common Fund | `06-FINANCE/02-Fund-Management/01-Common-Fund.md` |
| Motor run log | `04-MOTOR-OPERATIONS/04-Monitoring-and-Logs/01-Motor-Run-Log.md` |
