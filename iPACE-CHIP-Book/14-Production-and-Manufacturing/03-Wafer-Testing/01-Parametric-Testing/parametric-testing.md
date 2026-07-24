# 14.3.1 Parametric Testing for iPACE-CHIP

## Overview

Parametric testing verifies that the electrical characteristics of every iPACE-CHIP
die fall within specified limits before assembly. Unlike functional testing which
determines pass/fail operation, parametric testing measures continuous-valued
electrical parameters and compares them against statistical process control limits.
This chapter defines the parametric test methodology, equipment requirements, test
structure design, measurement techniques, and data analysis frameworks that ensure
only die meeting the zero-defect quality standard proceed to packaging.

## Test Philosophy

### Parametric vs. Functional Testing

| Aspect | Parametric Testing | Functional Testing |
|--------|-------------------|-------------------|
| Measurement | DC voltages, currents, resistances | Digital logic, analog function |
| Equipment | Precision SMU, parametric analyzer | Functional ATE |
| Sample Size | 100% of die (every die tested) | 100% of die (reduced for some) |
| Test Time | 5-15 seconds per die | 10-60 seconds per die |
| Output | Continuous data (current, voltage) | Binary (pass/fail) |
| Purpose | Process monitoring, binning | Functional verification |
| Defect Detection | Parametric shifts, marginal devices | Stuck-at faults, timing violations |

### Why Parametric Testing is Critical for Medical Devices

For the iPACE-CHIP, parametric testing serves three essential functions:

1. **Process Health Monitoring**: Trends in parametric data detect fab process
   excursions before they cause yield loss
2. **Reliability Screening**: Devices with parameters near specification limits
   have reduced lifetime margins (accelerated aging risk)
3. **Binning and Sorting**: Analog performance varies with process corner;
   parametric data enables optimal bin assignment

### Parametric Test Flow

```
Wafer Loading
    |
    v
Probe Contact (All pads)
    |
    v
Continuity Test (Bond pad contact verification)
    |
    v
DC Parametric Suite (48 measurements)
    |
    v
AC Parametric Suite (8 measurements)
    |
    v
Data Logging (all measurements to database)
    |
    v
Real-Time SPC Analysis
    |
    +---> All Pass ---> Bin 1 (Ship) ---> Next Die
    |
    +---> Marginal ---> Bin 2 (Review) ---> Engineering Analysis
    |
    +---> Fail ---> Bin 3 (Reject) ---> Failure Analysis
```

## Test Structure Design

### On-Chip Test Structures

The iPACE-CHIP includes dedicated test structures in the scribe line and on-chip
test pads for parametric measurement:

**Scribe Line Test Structures**:

| Structure | Measurement | Size | Location |
|-----------|------------|------|----------|
| NMOS Id-Vg | Vt, gm, Idsat, DIBL | 10x10 um | Every 5mm |
| PMOS Id-Vg | Vt, gm, Idsat, DIBL | 10x10 um | Every 5mm |
| NPN BJT (Ic-Vbe) | Beta, Early V, Vbe | 8x8 um | Every 10mm |
| Poly Resistor | Rsh, TCR, matching | 2x20 um | Every 5mm |
| TaN Resistor | Rsh, TCR, matching | 2x20 um | Every 10mm |
| MIM Capacitor | C/area, VCC, TCC | 10x10 um | Every 10mm |
| Contact Chain | Rc (per contact) | 100 contacts | Every 10mm |
| Via Chain | Rv (per via) | 100 vias | Every 10mm |
| Metal Sheet Rs | Rsh per layer | 10x100 um | Every layer |
| Gate Oxide Cap | Tox, Vbd, leakage | 100x100 um | Every 10mm |

**On-Die Test Pads**:

The iPACE-CHIP die includes a dedicated test pad ring for wafer-level parametric
measurement without probing the functional I/O pads:

```
Die Test Pad Layout:

    +-----------------------------------------+
    |  TP1   TP2   TP3   TP4   TP5   TP6    |
    |  VDDA  VSSA  VDDD  VSSD  VREF  VBAND  |
    |                                         |
    |  TP7   TP8   TP9   TP10  TP11  TP12    |
    |  IBIAS ITEMP VBG  FOSC  ISENSE VTELEM  |
    |                                         |
    |  +----------------------------------+   |
    |  |                                  |   |
    |  |        iPACE-CHIP Core           |   |
    |  |        (Functional Circuit)      |   |
    |  |                                  |   |
    |  +----------------------------------+   |
    |                                         |
    |  TP13  TP14  TP15  TP16  TP17  TP18    |
    |  DOUT1 DOUT2 DIN1  DIN2  STIM+ STIM-  |
    +-----------------------------------------+

    TP = Test Pad (80x80 um, TiW/Al)
    Total: 18 test pads for parametric measurement
```

## DC Parametric Measurements

### Power Supply Parameters

| Measurement | Parameter | Nominal | Min | Max | Unit | Method |
|------------|-----------|---------|-----|-----|------|--------|
| IDDQ | Quiescent Supply Current | 50 | 0 | 100 | uA | SMU, VDD=1.8V, all blocks off |
| IDD_MAX | Maximum Supply Current | 5.0 | 0 | 8.0 | mA | SMU, VDD=1.8V, all blocks active |
| VDD_LEAK | Input Leakage Current | 0 | -10 | 10 | nA | SMU, VDD pin, all inputs at GND |
| VDDZ | Supply Current (Standby) | 5.0 | 0 | 10 | uA | SMU, VDD=1.8V, sleep mode |
| VREG_OUT | Regulator Output Voltage | 1.20 | 1.15 | 1.25 | V | SMU, measure VREG pin |
| VREG_LOAD_REG | Load Regulation | 0 | -5 | 5 | mV | Delta VREG from 0 to 1 mA load |

### Analog Front-End Parameters

| Measurement | Parameter | Nominal | Min | Max | Unit | Method |
|------------|-----------|---------|-----|-----|------|--------|
| VOFFSET | Input Offset Voltage | 0 | -20 | 20 | uV | Short inputs, measure output |
| NOISE_FLOOR | Input Referred Noise | 1.5 | 0 | 2.0 | uVrms | Bandpass 1-7 kHz, 10s average |
| GBW | Gain-Bandwidth Product | 2.0 | 1.5 | 2.5 | MHz | 3dB point measurement |
| CMRR | Common-Mode Rejection | 80 | 70 | - | dB | 50 Hz common-mode rejection |
| PSRR | Supply Rejection Ratio | 70 | 60 | - | dB | 100 mVpp on VDD, measure output |
| INPUT_IMP | Input Impedance | 100 | 50 | - | MOhm | 1V DC bias, measure I |
| GAIN_ERROR | Gain Error | 0 | -2 | 2 | % | 1 mVpp input, measure output |

### Stimulation Output Parameters

| Measurement | Parameter | Nominal | Min | Max | Unit | Method |
|------------|-----------|---------|-----|-----|------|--------|
| STIM_CURR | Stimulation Current | 1.00 | 0.95 | 1.05 | mA | Load 1 kOhm, measure V |
| STIM_ACCURACY | Current Accuracy | 0 | -5 | 5 | % | vs. ideal 1 mA target |
| STIM合规 | Compliance Voltage | 8.0 | 6.0 | - | V | Maximum voltage at rated current |
| STIM Leakage | Leakage Current | 0 | -10 | 10 | nA | No load, measure current |
| STIM Settling | Settling Time | 10 | 0 | 20 | us | 1% of final value |
| CHARGE_BAL | Charge Balance Error | 0 | -2 | 2 | % | Net charge over full cycle |

### Reference and Bias Parameters

| Measurement | Parameter | Nominal | Min | Max | Unit | Method |
|------------|-----------|---------|-----|-----|------|--------|
| VBG | Bandgap Voltage | 1.250 | 1.230 | 1.270 | V | SMU high-impedance measure |
| VBG_TC | Bandgap Temp Coeff | 0 | -25 | 25 | ppm/C | 25C and 85C measurement |
| IBIAS | Reference Current | 10.0 | 8.0 | 12.0 | uA | SMU, measure IBIAS pin |
| VBG_LINE | Line Regulation | 0 | -5 | 5 | mV/V | VDD from 1.6V to 2.0V |

### Digital Parameters

| Measurement | Parameter | Nominal | Min | Max | Unit | Method |
|------------|-----------|---------|-----|-----|------|--------|
| VIL | Input Low Voltage | 0 | - | 0.3xVDD | V | Functional test |
| VIH | Input High Voltage | VDD | 0.7xVDD | - | V | Functional test |
| VOL | Output Low Voltage | 0 | - | 0.2xVDD | V | Measure at 1 mA load |
| VOH | Output High Voltage | VDD | 0.8xVDD | - | V | Measure at 1 mA load |
| IIL | Input Low Current | 0 | -1 | 1 | uA | Apply 0V, measure current |
| IIH | Input High Current | 0 | -1 | 1 | uA | Apply VDD, measure current |

## AC Parametric Measurements

| Measurement | Parameter | Nominal | Min | Max | Unit | Method |
|------------|-----------|---------|-----|-----|------|--------|
| FOSC | Oscillator Frequency | 10.0 | 9.5 | 10.5 | MHz | Frequency counter |
| FPLL_LOCK | PLL Lock Frequency | 48.0 | 46.0 | 50.0 | MHz | Frequency counter |
| FTELEM | Telemetry Frequency | 13.56 | 13.46 | 13.66 | MHz | Frequency counter |
| FCLK | System Clock | 1.0 | 0.95 | 1.05 | MHz | Frequency counter |
| JITTER_RMS | Clock Jitter | 50 | 0 | 100 | ps RMS | Jitter analyzer |
| T_RISE | Signal Rise Time | 2.0 | 0 | 5.0 | ns | 10%-90% measurement |
| T_FALL | Signal Fall Time | 2.0 | 0 | 5.0 | ns | 10%-90% measurement |
| BW_AMP | Amplifier Bandwidth | 7.0 | 6.0 | 8.0 | kHz | 3dB point measurement |

## Measurement Equipment

### Probe Station Configuration

| Component | Specification | Example |
|-----------|--------------|---------|
| Probe Station | Semi-automatic, 200mm | Cascade Summit 12000 |
| Microscope | Stereo, 7-45x zoom | Nikon SMZ-25 |
| Chuck | Vacuum, heated/cooled | Temp range: -40 to 200 C |
| Alignment | Manual + auto-alignment | Video-based, < 1 um accuracy |
| Lighting | Ring LED, dark/bright field | Fiber optic |

### Parametric Analyzer

| Component | Specification | Example |
|-----------|--------------|---------|
| SMU Channels | 4 minimum (VDD, GND, IN, OUT) | Keithley 2600B |
| Voltage Resolution | 10 uV | 22-bit ADC |
| Current Resolution | 10 fA | Electrometer grade |
| Voltage Range | -10V to +10V | Bipolar |
| Current Range | 100 fA to 1A | Auto-range |
| Source Accuracy | 0.01% (voltage), 0.02% (current) | Calibrated |
| Measurement Speed | < 1 ms per point | For high throughput |

### Frequency Measurement

| Component | Specification | Example |
|-----------|--------------|---------|
| Frequency Counter | DC to 500 MHz | Agilent 53230A |
| Resolution | 12 digits/second | High precision |
| Timebase | OCXO (stability < 0.1 ppm) | Calibrated to GPS |
| Period Measurement | 20 ps resolution | For jitter analysis |

## Measurement Accuracy Requirements

### Source-Measure-Unit Error Budget

For a critical measurement like bandgap voltage (VBG = 1.250V, tolerance +/-20 mV):

```
Total Measurement Error Budget:

Systematic Errors:
  SMU calibration accuracy:     +/- 0.01% = +/- 0.125 mV
  Lead resistance (2-wire):     +/- 0.5 mV (at 1 uA)
  Thermal EMF:                  +/- 0.05 mV
  Offset voltage (amplifier):   +/- 0.02 mV

Random Errors:
  SMU noise (10 uV typical):   +/- 0.01 mV
  Probe contact resistance:     +/- 0.1 mV (at 1 uA)
  Temperature drift:            +/- 0.05 mV/C (over 5 C range)

Total 1-sigma error: sqrt(0.125^2 + 0.5^2 + 0.05^2 + 0.02^2 + 0.01^2 + 0.1^2 + 0.25^2)
                   = sqrt(0.0156 + 0.25 + 0.0025 + 0.0004 + 0.0001 + 0.01 + 0.0625)
                   = sqrt(0.3411) = 0.584 mV

Total 3-sigma error = 3 x 0.584 = 1.75 mV

Measurement guard band = Specification tolerance / Error
                       = 20 mV / 1.75 mV = 11.4x
```

This 11.4x guard band ensures that measurement uncertainty does not cause false
pass or false reject decisions.

### Four-Wire (Kelvin) Measurements

For low-resistance measurements (contact resistance, wire bond resistance),
four-wire measurement eliminates lead and contact resistance errors:

```
Four-Wire Measurement Setup:

    Current Source (I_force)
         |          |
         |          |
    +----+          +----+
    | Force+         Force-|
    |                       |
    |  Device Under Test    |
    |                       |
    +----+          +----+
    | Sense+        Sense-|
    |          |
    |          |
    Voltmeter (V_measure)

    R = V_measure / I_force

    Error: Only voltmeter input impedance matters (< 0.001% error)
```

## Statistical Data Analysis

### Cpk Calculation and Trending

For each parametric measurement across a wafer, the Cpk is calculated:

```
Cpk = min[(USL - Xbar)/(3*sigma), (Xbar - LSL)/(3*sigma)]

Where:
  USL = Upper Specification Limit
  LSL = Lower Specification Limit
  Xbar = Sample mean
  sigma = Sample standard deviation (within-subgroup)
```

**Cpk Action Levels**:

| Cpk Range | Status | Action |
|-----------|--------|--------|
| > 2.0 | Excellent | Continue production |
| 1.67 - 2.0 | Good | Monitor trends |
| 1.33 - 1.67 | Acceptable | Increase sampling, investigate |
| 1.0 - 1.33 | Marginal | Process adjustment, 100% review |
| < 1.0 | Unacceptable | Stop production, corrective action |

### Wafer Map Analysis

Parametric data is plotted as wafer maps to identify systematic patterns:

```
Wafer Map: Bandgap Voltage (mV) at 25C

    +------------------------------------------------+
    |    ·    ·    ·    ·    ·    ·    ·    ·       |
    |  ·    ·    ·    ·    ·    ·    ·    ·    ·    |
    |    ·    ·    ·   (●)  ·    ·    ·    ·    ·   |
    |  ·    ·    ·    ·    ·    ·    ·    ·    ·    |
    |    ·    ·    ·    ·    ·    ·    ·    ·    ·   |
    |  ·    ·    ·    ·    ·    ·    ·    ·    ·    |
    |    ·    ·    ·    ·    ·    ·    ·    ·       |
    +------------------------------------------------+

    · = 1.248-1.252 V (within Cpk > 2 range)
    (●) = 1.255 V (marginal, investigate)
    
    Overall Cpk: 1.85
    Mean: 1.2498 V
    Sigma: 2.1 mV
    Recommendation: Ship wafer, monitor trend
```

### Correlation Analysis

Cross-correlation of parametric measurements identifies hidden relationships:

| Measurement Pair | Correlation Coefficient | Significance |
|-----------------|------------------------|--------------|
| VBG vs IBIAS | 0.92 | Strong (both depend on poly Rs) |
| NOISE_FLOOR vs VOFFSET | 0.78 | Moderate (matching dependent) |
| FOSC vs VREG_OUT | 0.65 | Moderate (frequency depends on VDD) |
| STIM_CURR vs IBIAS | 0.88 | Strong (current reference) |
| GBW vs IDDQ | 0.45 | Weak (different circuit blocks) |

High correlation (> 0.8) between measurements suggests redundant tests that can
be eliminated to reduce test time without sacrificing quality coverage.

## Test Time Optimization

### Test Partitioning

The iPACE-CHIP parametric test is partitioned into groups for parallel execution:

| Group | Measurements | Time | Equipment |
|-------|-------------|------|-----------|
| G1: Power | IDDQ, VDD_LEAK, VREG_OUT | 1.5 sec | SMU 1 |
| G2: Analog | VOFFSET, NOISE, GBW, CMRR | 4.0 sec | SMU 2 |
| G3: Stim | STIM_CURR, COMPLIANCE, LEAKAGE | 2.0 sec | SMU 3 |
| G4: Reference | VBG, IBIAS, VBG_TC | 2.5 sec | SMU 4 |
| G5: Digital | VIL, VIH, VOL, VOH, IIL, IIH | 1.0 sec | Digital I/O |
| G6: AC | FOSC, FPLL, FTELEM, JITTER | 2.0 sec | Counter |
| **Total** | **48 measurements** | **13.0 sec** | **Parallel** |

### Test Time vs. Coverage Tradeoff

| Test Level | Measurements | Time | Defect Coverage |
|-----------|-------------|------|-----------------|
| Quick Screen | 8 critical | 3 sec | 85% |
| Standard | 48 | 13 sec | 98% |
| Extended | 72 (add margin tests) | 25 sec | 99.5% |
| Full Characterization | 120+ | 60 sec | 100% |

The iPACE-CHIP uses Standard test level for production and Full Characterization
for first article inspection and quarterly process audits.

## Reject Handling and Failure Analysis

### Bin Classification

| Bin | Description | Criteria | Handling |
|-----|------------|----------|----------|
| Bin 1 | Ship Quality | All 48 parameters pass | Proceed to assembly |
| Bin 2 | Marginal | 1-2 parameters in guard band | Engineering review |
| Bin 3 | Parametric Fail | Any parameter outside spec | Failure analysis |
| Bin 4 | Probe Damage | Contact pad damage detected | Scrap |
| Bin 5 | Visual Defect | Particle or pattern defect | Review by visual inspection |

### Failure Analysis Process

```
Reject from Parametric Test
    |
    v
Data Review (which parameter, by how much)
    |
    +---> Consistent Fail ---> Process excursion ---> Fab investigation
    |
    +---> Random Fail ---> Possible defect ---> Physical failure analysis
    |
    +---> Margin Fail ---> Reliability risk ---> Additional screening
```

## Summary

Parametric testing of the iPACE-CHIP encompasses 48 DC and AC measurements performed
on every die at wafer probe, providing comprehensive process monitoring and quality
screening. The measurement system achieves 10x minimum guard band on all critical
parameters, ensuring measurement uncertainty does not impact pass/fail decisions.
Statistical process control with Cpk tracking enables early detection of fab process
excursions, while wafer map analysis identifies systematic patterns requiring
corrective action. The 13-second test time per die balances thoroughness with
production throughput requirements.

## References

1. MIL-STD-883, "Test Methods for Microelectronics," Methods 1001-1020.
2. JEDEC JESD35, "Procedure for the Wafer-Level Testing of Thin-Film Dielectrics."
3. iPACE-CHIP Parametric Test Specification, Internal Document, Rev 2.1.
4. Keithley Instruments, "Parametric Measurement Guide," Application Note, 2023.
5. S. Ma, "Statistical Methods for Semiconductor Test," IEEE ITC, 2022.
6. SEMI E10, "Equipment Reliability, Availability, and Maintainability."
7. iPACE-CHIP Test Program User Manual, Internal Document, Rev 1.5.
