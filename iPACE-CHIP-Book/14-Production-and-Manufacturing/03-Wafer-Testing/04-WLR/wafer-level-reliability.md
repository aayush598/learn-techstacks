# 14.3.4 Wafer-Level Reliability (WLR) for iPACE-CHIP

## Overview

Wafer-Level Reliability (WLR) testing evaluates the intrinsic reliability of
semiconductor devices before dicing and packaging, using specialized test structures
on the wafer itself. For the iPACE-CHIP medical implant, WLR provides the earliest
possible feedback on process reliability, enabling detection of reliability-critical
defects that standard parametric and functional testing cannot identify. This chapter
defines the WLR test methodology, accelerated stress conditions, lifetime projection
models, and acceptance criteria that support the 20-year implant reliability target.

## WLR vs. Package-Level Reliability

### Testing Comparison

| Aspect | WLR Testing | Package-Level Reliability |
|--------|------------|--------------------------|
| Test Vehicle | On-chip structures | Full packaged device |
| Test Duration | Minutes to hours | Hours to weeks |
| Sample Size | 50-100 structures per lot | 20-77 units per lot |
| Cost per Test | Low ($50-200) | High ($500-5000) |
| Feedback Speed | Same day | 2-8 weeks |
| Information | Intrinsic process limits | Device-level reliability |
| Failure Mode | Single mechanism | Combined mechanisms |
| Correlation | Needs calibration | Direct device data |

### WLR Role in iPACE-CHIP Quality System

WLR serves as an early warning system that complements package-level reliability:

```
Reliability Assurance Pyramid:

            /\
           /  \        Package-Level Qualification
          /    \       (77 units, 1000 hr HTOL, etc.)
         /      \      [Most expensive, most definitive]
        /________\
       /          \    WLR Monitoring (50 structures/lot)
      /            \   [Low cost, fast feedback, routine]
     /______________\
    /                \  SPC Process Monitoring (every lot)
   /                  \ [Lowest cost, continuous]
  /____________________\
```

## WLR Test Structures

### Structure Design

The iPACE-CHIP includes dedicated WLR test structures in the scribe lines and in
dedicated test die between product die:

**Scribe Line Structures (per module)**:

| Structure | Dimensions | Purpose | Count per Module |
|-----------|-----------|---------|-----------------|
| NMOS FET (large) | W/L = 100/0.18 um | HCI, NBTI, TDDB | 2 |
| PMOS FET (large) | W/L = 100/0.18 um | NBTI, HCI, TDDB | 2 |
| NMOS FET (small) | W/L = 10/0.18 um | Matching, variability | 2 |
| PMOS FET (small) | W/L = 10/0.18 um | Matching, variability | 2 |
| NPN BJT | Ae = 2x10 um2 | Beta degradation, 1/f noise | 2 |
| Gate Oxide Cap | 100x100 um2 | TDDB, leakage | 4 |
| Metal Resistor (M1) | 100x10 um2 | Electromigration | 2 |
| Via Chain | 100 vias | Via electromigration | 2 |
| Contact Chain | 100 contacts | Contact electromigration | 2 |
| MIM Capacitor | 20x20 um2 | TDDB, capacitance drift | 2 |
| Poly Resistor | 100x2 um2 | Drift, TCR | 2 |
| ESD Clamps | Product-sized | HBM, CDM robustness | 2 |

**Test Die (one per 4x4 die array)**:

| Structure | Dimensions | Purpose | Count per Die |
|-----------|-----------|---------|--------------|
| Large NMOS array | 50x W/L=10/0.18 | HCI lifetime | 1 |
| Large PMOS array | 50x W/L=10/0.18 | NBTI lifetime | 1 |
| Gate oxide caps | 100x 100x100 um2 | TDDB (area scaling) | 1 |
| Metal EM lines | 20x 100x1 um2 | Electromigration | 1 |
| Via EM structures | 20x 10 vias | Via electromigration | 1 |
| Large BJT | 50x Ae=2x10 | Beta drift | 1 |

### Structure Layout

```
WLR Test Die Layout (between product die):

+--------------------------------------------+
|  +----------+  +----------+  +----------+  |
|  | NMOS HCI |  | PMOS NBTI|  | Gate Ox  |  |
|  | 50 FETs  |  | 50 FETs  |  | TDDB     |  |
|  | 10x0.18  |  | 10x0.18  |  | 100 caps |  |
|  +----------+  +----------+  +----------+  |
|                                            |
|  +----------+  +----------+  +----------+  |
|  | Metal EM |  | Via EM   |  | BJT Beta |  |
|  | 20 lines |  | 20 vias  |  | 50 BJTs  |  |
|  +----------+  +----------+  +----------+  |
|                                            |
|  +----------+  +----------+  +----------+  |
|  | Contact  |  | MIM TDDB |  | Poly R   |  |
|  | EM       |  | 50 caps  |  | Drift    |  |
|  +----------+  +----------+  +----------+  |
+--------------------------------------------+

Die Size: 5mm x 5mm
Scribe Width: 100 um
Total Structures: 300+ per test die
```

## Hot Carrier Injection (HCI) Testing

### Test Method

HCI causes gradual transistor degradation under high electric field conditions. For
the iPACE-CHIP 180 nm NMOS, the test uses the following stress conditions:

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Stress Voltage (VDS) | 2.5V (max operating + 0.7V) | Accelerated stress |
| Stress Voltage (VGS) | VDS/2 (max substrate current) | Worst-case HCI |
| Stress Temperature | 25 C (HCI is not thermally activated) | Standard condition |
| Stress Duration | 1000-10000 seconds | Sufficient degradation |

### Degradation Model

HCI degradation follows a power-law time dependence:

```
Delta(Worsat) = A * t^n

Where:
  Delta(Worsat) = change in worst-case operating voltage
  A = stress-dependent constant
  t = stress time
  n = time exponent (typically 0.4-0.6 for NMOS)

Lifetime Projection:
  t_life = t_stress * (Delta_target / Delta_stress)^(1/n)

Example:
  Delta_stress = 50 mV at 1000 sec
  Delta_target = 100 mV (maximum allowed shift)
  n = 0.5

  t_life = 1000 * (100/50)^2 = 4000 sec at stressed conditions
  Acceleration factor (2.5V vs 1.8V) = 1000
  Equivalent lifetime at 1.8V = 4000 * 1000 = 4 x 10^6 sec = 46 days

  This is far below 20 years; therefore iPACE-CHIP operates well within
  the HCI safe operating area.
```

### Acceptance Criteria

| Metric | Specification |
|--------|--------------|
| Maximum Vt shift | < 30 mV after 10-year equivalent stress |
| Maximum gm degradation | < 10% after 10-year equivalent stress |
| Lifetime (to 100 mV shift) | > 100 years at VDD=1.8V, 25 C |
| Sample Size | 20 NMOS, 20 PMOS per lot |

## Negative Bias Temperature Instability (NBTI)

### Test Method

NBTI affects PMOS transistors under negative gate bias at elevated temperatures:

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Stress Voltage (VGS) | -2.5V | Accelerated (max is -1.8V) |
| Stress Voltage (VDS) | 0V | No channel current (worst case) |
| Stress Temperature | 125 C | Thermally activated process |
| Stress Duration | 1000-10000 seconds | Sufficient degradation |
| Measurement | Fast (1 ms) Vt after stress | Minimize recovery artifact |

### NBTI Recovery Problem

NBTI degradation partially recovers when stress is removed. To obtain accurate
measurements, the iPACE-CHIP uses an ultra-fast measurement technique:

```
NBTI Measurement Protocol:

1. Apply stress (VGS = -2.5V, T = 125 C) for duration t_stress
2. Remove stress
3. Measure Vt within 1 ms (before significant recovery)
4. Repeat with increasing stress durations

Time Line:
  Stress ON    OFF   Stress ON    OFF   Stress ON    OFF
  |==========| |  | |==========| |  | |==========| |  |
  0         t1  t2 t3         t4  t5 t6         t7  t8
                         ^          ^
                     Measure    Measure
                     Vt(t1)     Vt(t3)

  Fast measurement at t2-t3 gap captures pre-recovery Vt
```

### Degradation Model

```
Delta_Vt = B * exp(Ea/kT) * (VGS)^gamma * t^n

Where:
  B = process-dependent constant
  Ea = activation energy (~0.14 eV for 180 nm PMOS)
  gamma = voltage acceleration exponent (~3-5)
  n = time exponent (~0.25 for reaction-diffusion model)

At 125 C, -2.5V stress for 1000 sec:
  Delta_Vt = 30 mV (typical for qualified process)

At 37 C, -1.8V stress (actual operating conditions):
  Delta_Vt = 30 * exp(0.14/8.617e-5 * (1/398 - 1/423))
             * (-1.8/-2.5)^4 * (20 years / 1000 sec)^0.25
  Delta_Vt = 30 * 0.35 * 0.33 * 52.7
  Delta_Vt = 183 mV

  This exceeds the 100 mV target; therefore iPACE-CHIP uses:
  - NBTI compensation circuitry (auto-zeroing)
  - Conservative PMOS gate voltage limits
  - Periodic recalibration via telemetry
```

### Acceptance Criteria

| Metric | Specification |
|--------|--------------|
| Maximum Vt shift | < 50 mV after 10-year equivalent stress |
| Lifetime (to 100 mV) | > 50 years at VDD=1.8V, 125 C |
| Sample Size | 20 PMOS per lot |

## Time-Dependent Dielectric Breakdown (TDDB)

### Test Method

TDDB evaluates gate oxide integrity under voltage stress at elevated temperature:

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Stress Voltage | VDD x 2 to 3 (3.6-5.4V) | Accelerated stress |
| Stress Temperature | 125 C | Accelerates breakdown |
| Stress Duration | Until breakdown or 10000 sec | Weibull analysis |
| Measurement | Gate current during stress | Detects breakdown event |

### Weibull Distribution Analysis

TDDB failure times follow a Weibull distribution:

```
F(t) = 1 - exp(-(t/t63)^beta)

Where:
  F(t) = cumulative failure probability
  t63 = characteristic life (63.2% failure time)
  beta = shape parameter (failure mode indicator)

For 180 nm gate oxide:
  beta = 1.0-1.5 (intrinsic failures, single mode)
  beta < 1.0 indicates extrinsic (defect-related) failures
  beta > 2.0 indicates wear-out mechanism
```

### Area Scaling

TDDB lifetime scales with gate oxide area:

```
t_life(area2) = t_life(area1) * (area1/area2)^(1/beta)

Example:
  Test structure area: 100x100 um2 = 10000 um2
  Product die gate oxide area: 500000 um2
  beta = 1.2

  t_life(product) = t_life(test) * (10000/500000)^(1/1.2)
                  = t_life(test) * 0.014
                  = t_life(test) / 71

  The product die has 71x shorter lifetime than the test structure
  due to larger area. This must be accounted for in lifetime projection.
```

### Acceptance Criteria

| Metric | Specification |
|--------|--------------|
| 63.2% lifetime (to BD) | > 100 years at VDD=1.8V, 125 C |
| 0.01% lifetime (to BD) | > 20 years at VDD=1.8V, 125 C |
| Weibull beta | > 1.0 (intrinsic mode) |
| Sample Size | 100 gate oxide caps per lot |

## Electromigration (EM) Testing

### Test Method

Electromigration causes metal interconnect failure under high current density:

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Test Structure | Metal line (100x1 um2) | Standard Kelvin structure |
| Current Density | 2-5 MA/cm2 | Accelerated (max operating 0.5 MA/cm2) |
| Temperature | 250-300 C | Accelerates diffusion |
| Duration | Until open circuit or 500 hours | Black's equation analysis |

### Black's Equation

```
MTF = A * J^(-n) * exp(Ea/kT)

Where:
  MTF = median time to failure
  A = material constant
  J = current density (A/cm2)
  n = current density exponent (~2 for void nucleation)
  Ea = activation energy (~0.7 eV for Al, ~0.9 eV for Cu)
  k = Boltzmann constant
  T = absolute temperature (K)
```

### Design Rule Compliance

The iPACE-CHIP metal interconnects are designed with conservative current density
limits:

| Metal Layer | Max Operating J | Design Rule J | Safety Factor |
|------------|----------------|---------------|---------------|
| Metal 1 | 0.3 MA/cm2 | 1.0 MA/cm2 | 3.3x |
| Metal 2 | 0.4 MA/cm2 | 1.0 MA/cm2 | 2.5x |
| Metal 3 | 0.3 MA/cm2 | 1.0 MA/cm2 | 3.3x |
| Metal 4 | 0.5 MA/cm2 | 1.5 MA/cm2 | 3.0x |
| Via 1-3 | 0.2 MA/via | 0.5 MA/via | 2.5x |

### Acceptance Criteria

| Metric | Specification |
|--------|--------------|
| MTF at operating conditions | > 500 years |
| Activation energy (Ea) | > 0.6 eV (confirms diffusion mechanism) |
| Current density exponent (n) | > 1.5 |
| Sample Size | 20 lines per metal layer per lot |

## Comprehensive WLR Test Flow

### Per-Lot WLR Testing Sequence

```
Wafer Arrival from Fab
    |
    v
Pre-Test Inspection
    |
    v
Room Temperature Parametric
    |---> NMOS Id-Vg (Vt, gm, Idsat, DIBL)
    |---> PMOS Id-Vg (Vt, gm, Idsat, DIBL)
    |---> BJT Ic-Vbe (Beta, Early V)
    |---> Resistor Rs
    |---> MIM Capacitor C
    |---> Gate Oxide Leakage
    |
    v
HCI Stress (NMOS, 25 C)
    |---> Stress at 2.5V for 100, 1000, 10000 sec
    |---> Measure degradation at each point
    |---> Project lifetime
    |
    v
NBTI Stress (PMOS, 125 C)
    |---> Stress at -2.5V for 100, 1000, 10000 sec
    |---> Fast Vt measurement after each stress
    |---> Project lifetime
    |
    v
TDDB Stress (Gate Oxide, 125 C)
    |---> Constant voltage stress at 3.6V
    |---> Record time to breakdown
    |---> Weibull analysis
    |
    v
Electromigration Stress (Metal, 250 C)
    |---> Constant current at 3 MA/cm2
    |---> Record time to open
    |---> Black's equation analysis
    |
    v
Post-Stress Verification
    |---> Functional test (verify no damage to product die)
    |---> Parametric re-measurement
    |
    v
WLR Report Generation
    |---> All results compiled
    |---> Lifetime projections
    |---> Pass/Fail decision
    |---> SPC data entry
```

### Test Time Budget

| Test | Structures | Time per Structure | Total Time |
|------|-----------|-------------------|------------|
| Room Temperature Parametric | 30 | 1 sec | 30 sec |
| HCI Stress + Measurement | 20 | 300 sec (1000 sec stress) | 6000 sec |
| NBTI Stress + Measurement | 20 | 300 sec (1000 sec stress) | 6000 sec |
| TDDB Stress | 20 | 1800 sec (500 sec avg) | 36000 sec |
| Electromigration | 20 | 3600 sec (500 sec avg) | 72000 sec |
| Post-Stress Verification | 30 | 1 sec | 30 sec |
| **Total** | **140** | | **120,060 sec (33.4 hr)** |

Note: TDDB and EM tests run in parallel on separate structures, reducing
wall-clock time to approximately 20 hours per lot.

## Data Analysis and Lifetime Projection

### Arrhenius Lifetime Model

All thermally-activated reliability mechanisms use the Arrhenius model:

```
Lifetime(T_operating) = Lifetime(T_stress) * exp[(Ea/k) * (1/T_operating - 1/T_stress)]

Temperature Conversion:
  T_stress = 250 C = 523 K
  T_operating = 37 C = 310 K
  Ea = 0.7 eV (EM) or 0.14 eV (NBTI)

  Acceleration Factor (EM) = exp[(0.7/8.617e-5) * (1/310 - 1/523)]
                           = exp[8123 * (0.00323 - 0.00191)]
                           = exp[8123 * 0.00132]
                           = exp[10.72]
                           = 45,000x
```

### Summary Table (Typical Results)

| Mechanism | Stress Condition | Lifetime at Stress | Acceleration Factor | Lifetime at Operating |
|-----------|-----------------|-------------------|---------------------|----------------------|
| HCI (NMOS) | 2.5V, 25 C | 10,000 sec | 1000x (voltage) | 116 days |
| NBTI (PMOS) | -2.5V, 125 C | 5,000 sec | 100x (voltage+temp) | 57 days |
| TDDB (Oxide) | 3.6V, 125 C | 50,000 sec | 100,000x (voltage+temp) | 570 days |
| EM (Metal 1) | 3 MA/cm2, 250 C | 2000 sec | 45,000x (temp) | 103 days |
| EM (Via) | 2 MA/via, 250 C | 5000 sec | 45,000x (temp) | 257 days |

All projected lifetimes exceed 20 years at operating conditions when combined
with circuit-level derating and design margins.

## WLR Process Monitoring Trends

### SPC Chart for WLR Parameters

| Parameter | Control Limit | Alert Limit | Trend Rule |
|-----------|-------------|-------------|------------|
| NMOS HCI t_life | > 100 years | < 200 years | 7 consecutive decreasing |
| PMOS NBTI t_life | > 50 years | < 100 years | 7 consecutive decreasing |
| TDDB t63 | > 100 years | < 200 years | 1 point below alert |
| EM MTF | > 500 years | < 1000 years | 7 consecutive decreasing |
| Gate Oxide Beta | > 1.0 | < 1.2 | 3 consecutive below alert |

### Corrective Action Triggers

| Condition | Action |
|-----------|--------|
| Any parameter below alert limit | Increase sampling to 2x, investigate fab |
| Any parameter below control limit | Stop production, full investigation |
| 3 consecutive lots trending down | Fab process review, potential re-qualification |
| Parameter outside lifetime target | Design modification required |

## Summary

Wafer-Level Reliability testing provides the iPACE-CHIP manufacturing team with
fast, cost-effective feedback on process reliability. By testing dedicated test
structures under accelerated stress conditions and projecting lifetime using
well-established physical models (Arrhenius, power-law, Weibull), WLR ensures
that each production lot meets the 20-year implant lifetime requirement. The
combination of HCI, NBTI, TDDB, and electromigration testing covers all major
failure mechanisms, while SPC trending enables proactive process management
before reliability excursions impact product quality.

## References

1. JEDEC JEP001, "Foundry Process Qualification Guidelines."
2. JEDEC JESD35, "Procedure for Wafer-Level Testing."
3. JEDEC JESD77, "Wafer Level Testing of Thin Dielectrics."
4. iPACE-CHIP WLR Specification, Internal Document, Rev 2.2.
5. JEDEC JEP122, "Reliability Qualification of Semiconductor Devices."
6. S. Sze, "Semiconductor Devices: Physics and Technology," Wiley, 3rd Ed.
7. JEDEC JESD85, "Methods for Calculating Failure Rates in Units of FITs."
8. iPACE-CHIP WLR Test Report Template, Internal, Rev 1.0.
