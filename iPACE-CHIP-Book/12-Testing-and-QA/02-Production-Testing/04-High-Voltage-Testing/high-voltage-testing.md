# High-Voltage Testing

## Overview

High-voltage testing of the iPACE-CHIP encompasses two distinct domains: (1) testing the high-voltage pacing output circuitry that generates therapeutic pulses up to 7.5V from a low-voltage supply, and (2) dielectric withstand and insulation testing to ensure the device can safely operate in the conductive environment of the human body without creating leakage paths that could harm the patient. Both domains are critical for implantable medical device safety and are governed by IEC 60601-1 and ISO 14971 requirements.

---

## 1. Pacing Output High-Voltage Testing

### 1.1 Pacing Output Architecture

The iPACE-CHIP includes an on-chip charge pump and H-bridge output stage for generating pacing pulses:

```
Pacing Output Block Diagram:

Battery (3.0V)
    |
    v
+-----------+
| Charge    |  Generates high voltage rail
| Pump      |  Output: 7.5V (regulated)
+-----+-----+
      |
      v
+-----------+
| H-Bridge  |  Controls pulse polarity and amplitude
| Output    |  Bidirectional current flow
| Stage     |  through pacing leads
+-----+-----+
      |
      v
Pacing Leads (to heart)
```

### 1.2 High-Voltage Rail Testing

**Charge Pump Output Verification:**
```
Test conditions:
  VDD = 1.8V, load = 100kOhm (typical)
  Measure HV_RAIL voltage
  
Specifications:
  Output voltage: 7.5V +/-5% (7.125V to 7.875V)
  Ripple: less than 50mV peak-to-peak
  Load regulation: less than 1% from no-load to full-load
  Line regulation: less than 0.5% for VDD +/-10%
  Efficiency: greater than 80%
  Startup time: less than 500us
  
High-voltage rail current measurement:
  Quiescent: less than 5uA (charge pump running, no load)
  Maximum: 5mA (during pacing pulse)
  Shutdown: less than 100nA (charge pump disabled)
```

### 1.3 Output Stage High-Voltage Testing

**Pacing Pulse Characterization:**
```
Output voltage test:
  Set pacing amplitude to maximum (7.5V)
  Measure output at PACE_A and PACE_B terminals
  Verify differential voltage: 7.5V +/-5%
  Verify pulse shape: rectangular with less than 1us edges
  
Output impedance test:
  Apply 1kHz AC signal (10mV amplitude)
  Measure voltage and current
  Calculate impedance: 500 Ohm +/-10%
  Verify at DC as well: 500 Ohm +/-15%

Output current limiting test:
  Set output to maximum voltage
  Apply external load to force current
  Verify current limits at 10mA +/-10%
  Verify current foldback (short-circuit protection)
  Measure short-circuit current: less than 15mA
```

### 1.4 Charge Recovery Testing

After each pacing pulse, the output must recover to baseline:

```
Charge recovery test:
  Apply pacing pulse (7.5V, 1ms duration)
  Measure output voltage recovery after pulse
  Recovery specification:
    Time to 1% of peak: less than 10us
    Time to 0.1% of peak: less than 50us
    Residual voltage: less than 50mV after 100us
    
Charge balance test:
  Measure positive and negative charge delivered
  Charge imbalance: less than 0.1% of total charge
  Critical for patient safety (DC charge delivery causes tissue damage)
```

### 1.5 High-Voltage Isolation Testing

```
Isolation between HV_RAIL and VDD:
  Apply 15V DC between HV_RAIL and VDD
  Measure leakage current: less than 10nA
  Verify no breakdown up to 20V (abs max)

Isolation between HV_RAIL and substrate:
  Apply 15V DC between HV_RAIL and VSS
  Measure leakage current: less than 10nA
  Verify no latch-up at elevated temperature

Isolation between pacing outputs and sensing inputs:
  Apply 7.5V DC on PACE_A
  Measure interference on SENSE_CH1: less than 1mV
  Critical: pacing artifact must not corrupt sensing
```

---

## 2. Dielectric Withstand Testing

### 2.1 Insulation Requirements

The iPACE-CHIP package must maintain insulation between:

| Insulation Path | Required Withstand | Test Voltage | Leakage Limit |
|----------------|-------------------|--------------|---------------|
| Pacing output to sensing input | 2500 VAC | 1500 VAC | less than 5uA |
| Pacing output to system ground | 1500 VAC | 1000 VAC | less than 5uA |
| Sensing input to system ground | 500 VAC | 250 VAC | less than 1uA |
| Telemetry to system ground | 500 VAC | 250 VAC | less than 1uA |
| Power supply isolation | 500 VAC | 250 VAC | less than 1uA |

### 2.2 Hi-Pot Testing

```
Hi-Pot test procedure:
  Step 1: Connect all pins except DUT (device under test) to ground
  Step 2: Apply test voltage to DUT pin
  Step 3: Ramp voltage at 100V/second
  Step 4: Hold at test voltage for 60 seconds
  Step 5: Measure leakage current continuously
  Step 6: If leakage less than limit for full duration: PASS
  Step 7: If leakage exceeds limit at any point: FAIL

Test conditions:
  Voltage accuracy: +/-5%
  Current sensitivity: 0.1uA
  Ramp rate: 100V/sec (per IEC 60601-1)
  Test duration: 60 seconds (production)
  Environmental: Room temperature, dry conditions
```

### 2.3 Insulation Resistance Testing

```
Insulation resistance measurement:
  Apply 500V DC between isolated circuits
  Wait 1 minute for polarization current to stabilize
  Measure leakage current
  Calculate resistance: R = V_applied / I_leakage
  
Specifications:
  Pacing to sensing: greater than 100 MOhm
  Pacing to ground: greater than 100 MOhm
  Sensing to ground: greater than 1 GOhm
  Telemetry to ground: greater than 1 GOhm

Measurement equipment:
  Megohmmeter: Keithley 6517A or equivalent
  Accuracy: +/-2%
  Range: 1kOhm to 10TOhm
```

### 2.4 Partial Discharge Testing

For the iPACE-CHIP hermetic package, partial discharge detection identifies incipient insulation defects:

```
Partial discharge test:
  Apply AC voltage at 1.5x rated voltage
  Frequency: 50/60 Hz
  Duration: 60 seconds
  Detection sensitivity: less than 5pC (picocoulombs)
  
Acceptance criteria:
  No partial discharge events greater than 5pC
  Partial discharge inception voltage: greater than 1.5x rated
  Partial discharge extinction voltage: greater than 1.2x rated

Equipment:
  Partial discharge detector: IEC 60270 compliant
  Coupling capacitor: 100pF, rated for test voltage
  Filtering: Faraday cage enclosure
```

---

## 3. ESD and Overvoltage Testing

### 3.1 Human Body Model (HBM) ESD Testing

```
HBM ESD test (per JEDEC JS-001):
  Test voltage levels:
    Production: +/-2kV on all pins
    Qualification: +/-4kV on critical pins
    
  Test procedure:
    Step 1: Charge 100pF capacitor to test voltage
    Step 2: Discharge through 1.5kOhm resistor
    Step 3: Apply to DUT pin (positive and negative polarity)
    Step 4: Repeat 3 times per pin per polarity
    Step 5: Measure parametric after ESD
    Step 6: Functional verification
    
  Pass criteria:
    No parametric degradation greater than 10%
    No functional failure
    No visible damage (optical inspection)
    
  Critical pins (4kV qualification):
    PACE_A, PACE_B (pacing outputs)
    SENSE_CH1, SENSE_CH2 (sensing inputs)
    VDD, VSS (power supply)
    TCK, TMS (JTAG - for production access)
```

### 3.2 Charged Device Model (CDM) ESD Testing

```
CDM ESD test (per JEDEC JS-002):
  Test voltage: +/-500V (production)
  Qualification: +/-1000V
  
  Test conditions:
    Device charged to test voltage
    Discharged to ground through single-pin contact
    Rise time: less than 400ps
    
  CDM is critical for:
    Small geometries (gate oxide damage)
    Floating pins during handling
    Automated handling environments
```

### 3.3 Overvoltage Withstand Testing

```
Overvoltage test conditions:
  Apply abs-max voltage to each pin
  Duration: 100ms (simulates transient)
  Monitor for:
    Leakage current increase
    Functional disruption
    Latch-up initiation
    
Abs-max voltage ratings:
  Digital I/O: VDD + 0.3V (2.1V absolute max)
  Analog inputs: +/-300mV beyond supply
  Pacing output: 10V absolute max
  Power supply: 2.5V absolute max
  
Latch-up test:
  Force +/-100mA into each pin
  Verify no latch-up (current returns to normal when force removed)
  Test at 25 deg-C and 85 deg-C
```

---

## 4. Thermal Testing at High Voltage

### 4.1 Charge Pump Thermal Characterization

```
Thermal test under high-voltage operation:
  Condition: Continuous pacing at maximum rate (180 bpm)
  Duty cycle: 2ms pulse every 333ms (0.6% duty)
  Charge pump: Running continuously
  
  Measurements:
    Die temperature (on-chip sensor): 
      Max during pulse: 37.5 deg-C (ambient 37 deg-C)
      Steady state: 37.1 deg-C
    HV_RAIL stability during thermal ramp: less than 1% drift
    Pacing output accuracy at elevated temperature: within spec
```

### 4.2 High-Voltage Stress at Temperature

```
Combined stress test:
  Temperature: 85 deg-C (hot ambient)
  Voltage: 1.1x nominal (1.98V VDD)
  HV_RAIL: 8.25V (1.1x of 7.5V)
  Duration: 1000 hours
  
  Measurements at intervals:
    0, 168, 500, 1000 hours:
      Pacing output impedance
      HV_RAIL voltage and ripple
      Charge pump efficiency
      Output leakage current
      IDDQ baseline
      
  Pass criteria:
    No parametric drift greater than 5%
    No functional degradation
    No new failure modes
```

---

## 5. Implantation-Simulation Testing

### 5.1 Saline Immersion Test

```
Saline immersion test (simulates body environment):
  Solution: 0.9% NaCl (physiological saline)
  Temperature: 37 deg-C (body temperature)
  Duration: 24 hours (production), 30 days (qualification)
  
  Measurements:
    Insulation resistance before and after immersion
    Leakage current in saline: less than 1uA at 5V
    Corrosion assessment (visual and electrical)
    Package seal integrity after immersion
    
  Pass criteria:
    No change in insulation resistance
    No corrosion visible at 10x magnification
    Package seal maintained
```

### 5.2 Thermal Cycling with High-Voltage Operation

```
Thermal cycling test:
  Range: -20 deg-C to +60 deg-C (implant temperature range)
  Cycles: 1000
  Dwell time: 30 minutes at each extreme
  During cycling: Continuous pacing at 60 bpm
  Monitor: Output voltage, current, and impedance
  
  Post-test:
    Full parametric test at 25 deg-C
    Compare with pre-cycling baseline
    X-ray inspection for package integrity
```

### 5.3 Electrical Safety Testing

```
Leakage current test (simulates patient safety):
  Condition: Device operating at maximum output
  Measure current through simulated patient load (500 Ohm)
  
  DC leakage: less than 10uA (through pacing path)
  AC leakage: less than 10uA at 60Hz (through insulation)
  Single-fault condition: less than 50uA
  
  Test per IEC 60601-1 requirements:
    Normal condition
    Single fault condition (one insulation failure)
    Simultaneous measurement of all leakage paths
```

---

## 6. Production High-Voltage Test Flow

### 6.1 Test Sequence

```
High-voltage test flow (production):
  Step 1: Low-voltage parametric (VDD = 1.8V)
    ├── All DC parametric tests
    └── Pass/Fail checkpoint

  Step 2: Charge pump characterization
    ├── HV_RAIL voltage and regulation
    ├── Efficiency measurement
    └── Ripple measurement

  Step 3: Pacing output verification
    ├── Output impedance
    ├── Maximum voltage
    ├── Current limiting
    └── Charge recovery

  Step 4: Isolation testing
    ├── Insulation resistance (500V DC)
    ├── Leakage current at 250V AC (sample basis)
    └── Partial discharge (qualification only)

  Step 5: ESD verification
    ├── HBM +/-2kV (100% screening)
    └── Post-ESD parametric check

  Step 6: Final functional
    ├── Pacing output pulse verification
    ├── Sensing channel with pacing interference
    └── Telemetry link (not affected by HV)
```

### 6.2 Test Equipment Requirements

| Equipment | Purpose | Accuracy |
|-----------|---------|----------|
| HV power supply | Isolation testing | 0.1% voltage, 0.01uA current |
| Megohmmeter | Insulation resistance | 2% at 100MOhm |
| HV probe | Pacing output measurement | 0.5% at 10V |
| Current sense amplifier | Leakage current | 0.1nA sensitivity |
| ESD gun | HBM/CDM testing | Per JEDEC JS-001/002 |
| Thermal chamber | Temperature testing | +/-0.5 deg-C |
| Faraday cage | Partial discharge | Shielding greater than 80dB |

### 6.3 Safety Precautions

```
High-voltage test safety:
  Personnel:
    Only trained operators for HV testing
    ESD-safe workstations
    Lockout/tagout for HV equipment
    
  Equipment:
    HV interlocks on test enclosures
    Emergency stop buttons
    HV warning signs
    Current-limited supplies (less than 5mA short-circuit)
    
  Device handling:
    HV-tested devices may retain charge
    Discharge procedure before handling
    Insulated tools for HV probe connections
```

---

## 7. Medical Device Compliance

### 7.1 IEC 60601-1 Compliance Matrix

| Requirement | Test Method | Acceptance | iPACE-CHIP Status |
|-------------|-------------|------------|-------------------|
| Dielectric strength | Hi-Pot, 60s | No breakdown | 2500VDC tested |
| Insulation resistance | 500V DC, 1min | >100MOhm | Tested 100% |
| Leakage current | Direct measurement | <10uA | Tested 100% |
| Earth leakage | N/A (floating) | N/A | Not applicable |
| Patient leakage | Via saline simulation | <10uA | Tested at qualification |
| Single fault | Simulated fault | <50uA | Tested at qualification |
| Creepage/clearance | Design rule | Per voltage table | Verified in layout |
| Material compatibility | ISO 10993 | Biocompatible | Verified |

### 7.2 ISO 14971 Risk Analysis

```
High-voltage related hazards:
  Hazard 1: Patient burn from excessive pacing output
    Cause: Charge pump overvoltage, output stage failure
    Severity: Serious injury
    Risk control: Output current limiting, voltage monitoring
    Residual risk: Low (redundant protection)

  Hazard 2: Insulation failure leading to leakage
    Cause: Package defect, dielectric breakdown
    Severity: Potentially fatal (cardiac arrhythmia)
    Risk control: Hi-Pot screening, insulation monitoring
    Residual risk: Very low (multi-layer protection)

  Hazard 3: ESD damage causing functional failure
    Cause: Handling ESD events
    Severity: Device malfunction
    Risk control: HBM testing, ESD-safe handling
    Residual risk: Low (production screening)
```

---

## 8. Summary

High-voltage testing of the iPACE-CHIP addresses two critical safety domains: verification of the on-chip pacing output circuitry that generates therapeutic pulses, and dielectric/insulation testing to ensure patient safety in the conductive body environment. The comprehensive test strategy combines parametric verification of the charge pump and output stage, insulation resistance and hi-pot testing, ESD qualification, and implantation-simulation testing. These tests collectively ensure compliance with IEC 60601-1 and ISO 14971, providing the safety assurance necessary for a life-sustaining implantable medical device.

---

## References

- IEC 60601-1:2005+A1:2012+A2:2020: Medical Electrical Equipment - General Requirements
- IEC 60601-1-2:2014+A1:2020: Electromagnetic Disturbances
- JEDEC JS-001: ESD Sensitivity Testing, Human Body Model
- JEDEC JS-002: ESD Sensitivity Testing, Charged Device Model
- ISO 14971:2019: Application of Risk Management to Medical Devices
- ISO 10993-1:2018: Biological Evaluation of Medical Devices
- IEC 60270:2000: High-Voltage Test Techniques - Partial Discharge Measurements
- MIL-STD-883: Test Methods for Microelectronics (Method 1011 - Dielectric Withstand)
