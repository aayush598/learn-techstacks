# Packaged Device Testing

## Overview

Packaged device testing validates that the iPACE-CHIP maintains full functionality and specification compliance after the packaging process. Unlike wafer sort which tests bare die, packaged device testing must account for package parasitic effects, thermal behavior, and the additional stress introduced during die attach, wire bonding, and encapsulation. This stage is the second major quality gate and provides the first opportunity to test the device at full supply voltage with complete thermal characterization.

---

## 1. Package-Related Test Considerations

### 1.1 Package Parasitic Effects

The iPACE-CHIP uses a medical-grade hermetic QFN package (64-pin, 9mm x 9mm) with the following parasitic characteristics:

| Parasitic | Typical Value | Impact on Testing |
|-----------|---------------|-------------------|
| Bond wire inductance | 2-5 nH | Limits high-frequency signal integrity |
| Lead frame resistance | 50-100 mOhm | Voltage drop under load |
| Pad capacitance | 0.3-0.8 pF | Signal edge rate degradation |
| Package thermal resistance | 35 deg-C/W | Junction temperature rise |
| Lead-to-lead capacitance | 0.1-0.3 pF | Crosstalk between adjacent pins |

### 1.2 Package Integrity Verification

Before functional testing, basic package integrity is verified:

**Visual inspection (100% automated optical inspection):**
- Bond wire integrity: no broken, swept, or crossed wires
- Die attach quality: no voids visible (X-ray inspection for 10% sample)
- Mold compound: no voids, cracks, or delamination
- Lead coplanarity: less than 0.1mm variation
- Marking legibility and correctness

**Package seal test (hermetic):**
- Fine leak test: He leak rate less than 1x10^-8 atm-cc/sec
- Gross leak test: No bubbles observed in fluorocarbon bath
- Internal humidity: less than 500 ppm H2O (per MIL-STD-883)
- These tests verify hermetic seal for implantable longevity

### 1.3 Thermal Characterization

The packaged device has different thermal characteristics than bare die:

```
Junction Temperature Calculation:
Tj = Ta + (Pd x theta_JA)

Where:
  Ta = Ambient temperature (37 deg-C for implant)
  Pd = Power dissipation (350 uW typical)
  theta_JA = Junction-to-ambient thermal resistance (35 deg-C/W)

Tj = 37 + (350e-6 x 35) = 37.01 deg-C

For worst-case (active pacing):
Tj = 37 + (2e-3 x 35) = 37.07 deg-C

Thermal margin: Well within 85 deg-C rated maximum
```

---

## 2. Pre-Test Setup

### 2.1 Test Socket and Handler

The iPACE-CHIP packaged devices are tested using automated handling:

**Test Socket Specifications:**

| Parameter | Value |
|-----------|-------|
| Socket type | Open-top clamshell |
| Contact method | Cantilever spring pins |
| Contact resistance | less than 50 mOhm per pin |
| Maximum current | 1A per contact |
| RF bandwidth | DC to 6 GHz |
| Lifetime | greater than 500,000 insertions |
| Thermal interface | Optional thermoelectric cooler |

**Handler Specifications:**

| Parameter | Value |
|-----------|-------|
| Throughput | 2,000 UPH (units per hour) |
| Insertion/removal force | less than 15N insertion, less than 5N removal |
| Temperature range | -40 deg-C to +155 deg-C |
| Bin capacity | 32 pass/fail bins |
| ESD protection | less than 100V HBM at contact point |

### 2.2 Test Program Architecture

```
iPACE-CHIP Test Program Structure:
  Program initialization
    Load test limits (version controlled)
    Calibrate ATE channels
    Initialize handler interface
    Load golden reference data

  Device insertion detection
    Continuity check (all pins)
    Verify device power-up

  Test execution (sequenced by test time)
    DC parametric tests
    Scan chain tests
    BIST tests
    Functional tests
    RF/telemetry tests
    IDDQ tests

  Results logging
    All parametric values (not just pass/fail)
    Test execution time
    Handler bin assignment
    Lot/wafer/die coordinate

  Device sort and marking
    Bin assignment
    Ink marking (for wafer-level sort only)
    Tape and reel (for shipping)
```

---

## 3. DC Parametric Testing (Packaged)

### 3.1 Supply Current Measurement

Packaged device supply current testing includes multiple operating modes:

**Quiescent Supply Current (IDDQ):**
```
Conditions: All inputs static, no clock activity
  VDD = 1.8V, Ta = 25 deg-C
  Typical: 1.2 uA
  Maximum: 5 uA
  Measurement time: 100 us settling + 10 us measurement
  Failure: greater than 5 uA indicates defect or excessive leakage
```

**Active Supply Current (IDD_ACTIVE):**
```
Conditions: Full-speed operation, all peripherals active
  VDD = 1.8V, Ta = 25 deg-C
  Typical: 350 uW (194 uA)
  Maximum: 500 uW (278 uA)
  Measurement: Average over 10ms window
  Failure: greater than 500 uW indicates excessive dynamic power
```

**Sleep Mode Current (IDD_SLEEP):**
```
Conditions: Deep sleep mode, oscillator running, all digital blocks disabled
  VDD = 1.8V, Ta = 25 deg-C
  Typical: 0.8 uA
  Maximum: 2 uA
  Measurement: 1ms integration time
  Failure: greater than 2 uA indicates sleep mode malfunction
```

### 3.2 Input/Output Electrical Tests

**Input Threshold Voltage (VIH/VIL):**
```
For each digital input:
  Increase voltage from 0V, measure when output transitions
  VIH_min = 0.7 x VDD = 1.26V
  VIL_max = 0.3 x VDD = 0.54V
  Hysteresis: 200mV minimum (Schmitt trigger inputs)
  Pass: VIH less than 1.26V and VIL greater than 0.54V

For analog inputs:
  Measure input impedance: greater than 10 MOhm
  Measure input capacitance: less than 5pF
  Input voltage range: -0.3V to VDD+0.3V (abs max)
  Input leakage: less than 1nA at VDD/2
```

**Output Drive (VOH/VOL):**
```
For each digital output:
  VOH at IOH = -1mA: greater than VDD - 0.4V = 1.4V
  VOL at IOL = 1mA: less than VSS + 0.4V = 0.4V
  VOH at IOH = -4mA (high drive): greater than VDD - 0.6V = 1.2V
  VOL at IOL = 4mA (high drive): less than VSS + 0.6V = 0.6V
  Pass: All outputs meet drive requirements

For analog outputs (pacing):
  Output impedance: 500 Ohm +/-10% (450 to 550 Ohm)
  Maximum output voltage: 7.5V (pacing pulse)
  Output current limit: 10mA
  Output leakage (disabled): less than 100nA
  Pass: All parameters within specification
```

### 3.3 ESD Protection Verification

```
ESD verification (production sample test):
  HBM test: +/-2kV on all pins (100% on production)
  CDM test: +/-500V
  Test method: Apply ESD pulse, then measure parametric
  Criteria: No parametric degradation after ESD
  100% HBM screening on production lot
```

---

## 4. Functional Testing (Packaged)

### 4.1 Clock System Test

```
Clock verification:
  Crystal oscillator startup: less than 1ms
  Oscillation frequency: 32.768 kHz +/-100ppm
  System clock (PLL output): target +/-0.1%
  PLL lock time: less than 100us
  Clock jitter: less than 50ps RMS
  Clock switching: seamless failover between sources
  Clock monitor: verify frequency within window
  Pass: All clock parameters meet specification
```

### 4.2 Power Management Test

```
Power system verification:
  Voltage regulator output: 1.8V +/-2%
  Low-brown-out detection: trigger at 1.65V
  Power-on-reset: functional below 1.62V
  Power switching (main to backup): less than 10us
  Battery monitoring accuracy: +/-50mV
  Charge pump operation (for pacing): output voltage correct
  Power-good signal timing
  Pass: All power modes functional
```

### 4.3 Pacing Output Test

**Critical safety test - double verification required:**

```
Pacing output verification:
  Output impedance: 500 Ohm +/-10% (measured at 1kHz)
  Maximum output voltage: 7.5V +/-5%
  Output pulse shape: rectangular, less than 1us rise/fall
  Pulse duration programmability: 0.1ms to 2ms (+/-5%)
  Output current limiting: 10mA +/-10%
  Output leakage (disabled): less than 100nA
  Charge recovery: greater than 99% within 10us
  Double verification: Independent measurement channels
  Pass: All parameters within safety specification
```

### 4.4 Sensing Channel Test

```
Sensing channel verification:
  Input impedance: greater than 10 MOhm at 1kHz
  Input noise: less than 20 uV RMS
  ADC accuracy: +/-1 LSB (12-bit, full scale)
  CMRR: greater than 80dB
  Input protection: clamps at +/-300mV
  Input bandwidth: 0.05Hz to 150Hz (bandpass for ECG)
  Sample rate: 500 SPS (samples per second)
  Pass: All channels within specification
```

### 4.5 Telemetry Test

```
Telemetry verification:
  TX output power: -30dBm +/-3dB
  TX modulation: FSK, deviation +/-50kHz
  TX data rate: 128 kbps +/-1%
  RX sensitivity: less than -70dBm (BER less than 10^-3)
  RX data rate tolerance: +/-1%
  Antenna impedance match: VSWR less than 2:1
  Frequency accuracy: +/-50ppm
  Pass: Full-duplex link operational
```

### 4.6 Firmware Boot Test

```
Firmware boot verification:
  Boot from ROM: successful within 10ms
  Firmware checksum: matches golden reference
  Firmware version register: correct value
  Watchdog timer: functional (triggers reset)
  Secure boot: signature verification pass
  Fail: Any boot failure triggers immediate reject
```

---

## 5. Multi-Site Testing

### 5.1 Four-Site Parallel Testing

The iPACE-CHIP uses 4-site testing to maximize throughput:

```
Site Configuration:
  Site 0: Channels A[0:63]
  Site 1: Channels B[0:63]
  Site 2: Channels C[0:63]
  Site 3: Channels D[0:63]

Resource sharing:
  Shared: Digital timing generators (time-interleaved)
  Shared: Power supply units (sequenced between sites)
  Dedicated: Per-site comparator channels
  Dedicated: Per-site RF ports (telemetry test)

Throughput improvement: 4x (theoretical)
Actual improvement: 3.2x (accounting for setup/teardown)
```

### 5.2 Multi-Site Calibration

Each test site requires independent calibration:

```
Per-site calibration:
  DC parametric: Offset and gain calibration per channel
  Digital: Timing edge calibration per site
  RF: Path loss calibration per site
  Power: Voltage and current sense calibration

Calibration frequency: Start of each test lot
Calibration standard: NIST-traceable reference
Calibration uncertainty: less than 0.1% for DC, less than 0.5dB for RF
```

---

## 6. Environmental Testing

### 6.1 Temperature Testing

Production temperature testing at three corners:

```
Corner 1: Room Temperature (25 deg-C)
  All DC parametric tests
  All functional tests at nominal frequency
  IDDQ measurement

Corner 2: Cold (-40 deg-C)
  DC parametric (supply current, I/O levels)
  Functional at full frequency (fast corner)
  Reduced test set (critical functions only)
  Soak time: 5 minutes before measurement

Corner 3: Hot (+85 deg-C)
  DC parametric (leakage current emphasis)
  Functional at full frequency (slow corner)
  IDDQ at elevated temperature
  Thermal shutdown verification
  Soak time: 5 minutes before measurement
```

### 6.2 Voltage Testing

```
Voltage corners:
  Nominal: 1.80V (100% VDD)
  Low: 1.62V (90% VDD)
  High: 1.98V (110% VDD)
  Abs max: 2.10V (117% VDD) - brief stress only

At each voltage corner:
  Functional verification
  Parametric measurement
  Pass/fail determination uses corner-specific limits
```

---

## 7. Reliability Screening

### 7.1 Early Life Failure Rate (ELFR) Screening

The iPACE-CHIP implements ELFR screening to reduce infant mortality:

```
ELFR Screening Methods:
  High-temperature operating life (HTOL) stress:
    Temperature: 125 deg-C
    Duration: 168 hours (1 week)
    Supply voltage: 1.2x nominal
    Sample size: per JESD47 requirements
    Pass criteria: less than 50 FIT

  High-temperature storage (HTSL):
    Temperature: 150 deg-C
    Duration: 168 hours
    No bias (storage only)
    Sample size: per JESD47

  Temperature cycling:
    Range: -65 deg-C to +150 deg-C
    Cycles: 1000
    Soak time: 10 minutes per extreme
    Sample size: per JESD47
```

### 7.2 Burn-In

Production burn-in for high-reliability lots:

```
Burn-in Conditions:
  Temperature: 125 deg-C
  Supply voltage: 1.1x nominal (1.98V)
  Duration: 48 hours
  Test pattern: Functional cycling (continuous pacing simulation)
  Monitoring: IDDQ measured at start and end

Post burn-in:
  Full parametric test at 25 deg-C
  Compare with pre-burn-in baseline
  Flag any parametric drift greater than 10%
  Failed devices removed from lot
```

### 7.3 Outgoing Quality Level (OQL)

```
OQL targets for iPACE-CHIP:
  Defective parts per million (DPPM): less than 1
  Confidence level: 95%
  Sample size: per ANSI/ASQ Z1.4 (Level III, AQL=0.01%)

Testing at OQL:
  Complete parametric suite
  Full functional verification
  IDDQ at room and hot temperatures
  BIST execution (all seeds)
  Telemetry link verification
```

---

## 8. Production Test Flow

### 8.1 Complete Test Flow Diagram

```
Incoming packaged device lot
  |
  v
Visual/AOI inspection (100%)
  |
  v
Test floor setup
  Load handler
  Calibrate ATE
  Verify test program
  |
  v
Room temperature test (100%)
  DC parametric
  Scan/BIST
  Functional
  Telemetry
  IDDQ
  |
  v
Pass/Fail sort
  |
  +---> Fail bin ---> Failure analysis queue
  |
  v
Cold test (100%)
  Reduced parametric
  Critical functional
  |
  v
Hot test (100%)
  Leakage emphasis
  Slow-corner functional
  Thermal verification
  |
  v
Final bin assignment
  |
  +---> All pass ---> Grade A (production release)
  +---> Cold fail only ---> Grade B (limited use, engineering review)
  +---> Any hot fail ---> Reject (failure analysis)
  +---> Room fail ---> Reject (failure analysis)
  |
  v
Tape and reel
  |
  v
Shipping to system assembly
```

### 8.2 Test Time Summary

| Test Phase | Time (seconds) | Notes |
|-----------|----------------|-------|
| Handler insertion | 0.5 | Mechanical handling |
| Continuity check | 0.1 | Pin contact verify |
| DC parametric | 1.2 | All parametric measurements |
| Scan/BIST | 3.5 | Full test suite |
| Functional | 2.0 | All functional tests |
| Telemetry | 1.0 | RF test |
| IDDQ | 0.3 | Quiescent current |
| Total (25 deg-C) | 8.6 | Per device |
| Cold test | 5.0 | Reduced test set |
| Hot test | 5.0 | Reduced test set |
| Handler removal | 0.3 | Mechanical handling |
| **Total per device** | **19.4** | **All corners** |

### 8.3 Throughput Calculation

```
Multi-site (4-site) testing:
  Effective test time per device: 19.4 / 3.2 = 6.1 seconds
  Theoretical throughput: 3600 / 6.1 = 590 UPH
  With overhead (15%): 590 x 0.85 = 501 UPH
  Daily capacity (20hr operation): 10,020 devices
  Monthly capacity: 250,500 devices
```

---

## 9. Medical Device Packaging Test Requirements

### 9.1 ISO 13485 Traceability

Every packaged device receives:

- Unique device serial number (laser marked)
- Lot number (traceable to wafer, fab, and assembly)
- Test date and ATE serial number
- Complete parametric data (stored in database)
- Pass/fail grade and bin assignment

### 9.2 Packaging Qualification

The package must pass qualification testing before production:

| Test | Standard | Condition | Acceptance |
|------|----------|-----------|------------|
| Temperature cycling | JESD22-A104 | 1000 cycles, -65 to 150C | No cracks, leaks |
| Thermal shock | JESD22-A106 | 500 cycles, -40 to 125C | No failures |
| HTOL | JESD22-A108 | 1000hr, 125C, 1.2x VDD | less than 10 FIT |
| ESD (HBM) | JEDEC JS-001 | +/-2kV on all pins | No damage |
| ESD (CDM) | JEDEC JS-002 | +/-500V | No damage |
| Solderability | J-STD-002 | 3 reflow cycles | greater than 95% coverage |
| Salt spray | MIL-STD-883 | 48 hours | No corrosion |
| Vibration | JESD22-B103 | 20g, 20-2000Hz | No resonance failure |

### 9.3 Biocompatibility Considerations

For the iPACE-CHIP implantable package:

- Package materials must be ISO 10993 compliant
- Leachable substances below threshold limits
- No cytotoxic potential from package materials
- Extractables/leachables testing on package materials
- Package integrity over 10-year implant life

---

## 10. Summary

Packaged device testing is the comprehensive quality gate that validates iPACE-CHIP functionality, parametric compliance, and reliability after the assembly process. Multi-corner testing across voltage and temperature ensures operation across the full specification range. Automated handling with 4-site parallel testing achieves production throughput targets while maintaining the thoroughness required for medical device quality. ELFR screening and burn-in provide the reliability assurance demanded by implantable applications, targeting less than 1 DPPM outgoing quality.

---

## References

- JEDEC Standard JESD47: Stress-Test-Driven Qualification of Integrated Circuits
- JEDEC Standard JESD22: Reliability Test Methods for Semiconductor Devices
- IEC 60747-1: Semiconductor Devices - General
- IEC 62132-4: Integrated Circuit Electromagnetic Immunity
- ISO 13485:2016: Medical Devices - Quality Management Systems
- ISO 10993-1:2018: Biological Evaluation of Medical Devices
- MIL-STD-883: Test Methods and Procedures for Microelectronics
