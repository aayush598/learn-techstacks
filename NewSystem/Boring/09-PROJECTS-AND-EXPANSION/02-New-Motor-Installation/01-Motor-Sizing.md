# NEW MOTOR INSTALLATION — MOTOR SIZING

**Folder:** `09-PROJECTS-AND-EXPANSION/02-New-Motor-Installation/`

---

## 1. WHY THIS FILE EXISTS

A motor is bought wrong in two ways: too small, so it strains and burns out;
too big, so it wastes power every single day and empties the well faster than
it refills. In the old system the size was decided by the shopkeeper's stock or
the "expert" member's guess. Here it is decided by a documented calculation.

## 2. THE INPUTS TO THE CALCULATION

| Input | Where it comes from |
|-------|---------------------|
| Static water level | Dip readings (`04-MOTOR-OPERATIONS/04-Monitoring-and-Logs/`) |
| Dynamic level under pumping | Pumping test or recent duty logs |
| Depth of the boring and casing | Asset Register (`05-Infrastructure-Asset-Register/`) |
| Head — height to the top tap or tank | Network survey (`04-Network-Improvements/01-Tap-Height-Compensation.md`) |
| Friction losses in pipes | Pipe length and size, standard tables |
| Required discharge per hour | Slot schedule and household needs |
| Running hours per day | Published schedule (`04-MOTOR-OPERATIONS/01-Daily-Schedule/`) |

## 3. TWO INDEPENDENT SOURCES OF ADVICE

1. Sizing advice is obtained from **two independent sources**:
   - an authorised dealer's technical calculation, and
   - a second dealer or a licensed electrician with no connection to the
     dealer that is likely to supply the motor.
2. If the two calculations disagree materially (different HP), a **third
   independent source** is consulted.
3. The advice is written down, not telephoned.

## 4. THE CALCULATION IS DOCUMENTED AND PRESENTED

1. The chosen size is presented to the assembly as a written calculation:
   head in metres, discharge in litres/minute, and the resulting rating in HP
   or kW, plus the reason for the choice.
2. The file records why a larger and a smaller size were rejected.
   - **Oversizing** wastes power and empties the well.
   - **Undersizing** fails under load and burns the motor.
   Both reasons are the point of the documentation: the assembly sees the
   trade-off, not a magic number.
3. The calculation is filed in the project file and is public (P6).

## 5. NO EXCEPTION FOR "FREE" SOURCES

- A "free" motor given by a relative is welcome as a donation — but it is
  installed only if it matches the documented size. A donated motor of the
  wrong size is neither a bargain nor an obligation.

## 6. EXAMPLE FROM COLONY LIFE

The old 1 HP motor burned out on a 120-foot boring. One dealer recommends 1.5 HP,
another recommends 2 HP. The third source, a retired pump technician, confirms
1.5 HP at the measured head with the existing pipe size. The assembly approves
1.5 HP — and the written calculation goes on the notice board so every member
sees why a "bigger is better" cousin was overruled.

## 7. REVIEW WHEN CIRCUMSTANCES CHANGE

- The sizing file is reopened whenever the water level falls significantly,
  the head changes (new tank), or a motor must be replaced. The old motor's
  failure report is the first input to the new calculation.

---

*The right motor is the smallest motor that reliably does the job — and the
assembly knows exactly why, because the numbers are written down.*
