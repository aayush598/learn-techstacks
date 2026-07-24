# FMEA Analysis

## Overview

Failure Mode and Effects Analysis (FMEA) is a systematic, proactive methodology for evaluating the iPACE-CHIP design and manufacturing processes to identify potential failure modes, their causes, and their effects on patient safety and device performance. As required by ISO 14971 for medical device risk management, FMEA provides a structured framework for prioritizing risks and implementing preventive actions. For the iPACE-CHIP, FMEA encompasses both Design FMEA (DFMEA) and Process FMEA (PFMEA) throughout the product lifecycle.

---

## 1. FMEA Fundamentals

### 1.1 FMEA Types for iPACE-CHIP

```
FMEA Types:
  DFMEA (Design FMEA):
    Scope: IC design, architecture, firmware
    Responsibility: Design engineering team
    Timing: Throughout design phases
    Goal: Eliminate or reduce design-related failures
    
  PFMEA (Process FMEA):
    Scope: Manufacturing and test processes
    Responsibility: Manufacturing engineering team
    Timing: Process development and production
    Goal: Eliminate or reduce process-related failures
    
  SFMEA (System FMEA):
    Scope: System-level interactions (iPACE-CHIP + leads + firmware)
    Responsibility: Systems engineering team
    Timing: System design phase
    Goal: Identify system-level failure modes
```

### 1.2 Risk Priority Number (RPN)

The traditional FMEA uses RPN to prioritize failure modes:

```
RPN = Severity (S) x Occurrence (O) x Detection (D)

Severity Scale (1-10):
  10: Patient death or life-threatening injury
   9: Serious injury, device failure in critical function
   8: Device malfunction requiring intervention
   7: Device degradation, reduced performance
   6: Minor device impact, no patient effect
   5: Device cosmetic issue, no functional impact
   4: Manufacturing defect, no device effect
   3: Process variation, within specification
   2: Negligible effect
   1: No effect

Occurrence Scale (1-10):
  10: Very high (greater than 1 in 10)
   9: High (1 in 20)
   8: Moderately high (1 in 80)
   7: Moderate (1 in 400)
   6: Low-moderate (1 in 2,000)
   5: Low (1 in 15,000)
   4: Very low (1 in 150,000)
   3: Remote (1 in 1,500,000)
   2: Very remote (1 in 15,000,000)
   1: Nearly impossible (less than 1 in 15,000,000)

Detection Scale (1-10):
  10: No detection method available
   9: Very low probability of detection
   8: Low probability of detection
   7: Moderate probability of detection
   6: Moderately high probability of detection
   5: High probability of detection
   4: Very high probability of detection
   3: Almost certain detection
   2: Very high detection (redundant methods)
   1: Almost certain detection (automated, verified)
```

### 1.3 Action Priority (AP) - AIAG/VDA Method

The newer AIAG/VDA FMEA uses Action Priority instead of RPN:

```
AP Level:
  High (H): Must take action, reduce risk
  Medium (M): Should take action, risk reduction recommended
  Low (L): Could take action, risk acceptable

AP is determined by combined S-O-D ratings
More nuanced than RPN (prevents RPN masking)
```

---

## 2. Design FMEA (DFMEA) for iPACE-CHIP

### 2.1 Scope and Boundary

```
DFMEA Scope for iPACE-CHIP:
  In scope:
    ├── IC architecture and circuit design
    ├── Physical layout and parasitic effects
    ├── Package design and materials
    ├── Firmware design and algorithms
    ├── DFT and testability features
    └── User interface (telemetry protocol)

  Out of scope:
    ├── Lead design (system-level FMEA)
    ├── Surgical procedure (clinical FMEA)
    ├── Patient selection (clinical FMEA)
    └── System-level integration (separate SFMEA)
```

### 2.2 DFMEA Worksheet Excerpts

**Failure Mode 1: Pacing output overvoltage**

```
DFMEA Entry: FM-001
Function: Generate pacing output voltage
Failure Mode: Output voltage exceeds 7.5V specification
Effect: Patient tissue damage from excessive stimulation
Severity: 10 (life-threatening)

Cause: Charge pump regulator failure
Occurrence: 2 (very remote - redundant regulation)

Current controls:
  Design: Voltage monitoring circuit with shutdown
  Test: Production voltage measurement (+/-5%)
  Detection: Real-time monitoring during operation

Detection: 2 (very high - redundant monitoring)

RPN: 10 x 2 x 2 = 40
AP: Low (L)
Action: Maintain current design and test coverage
```

**Failure Mode 2: Arrhythmia detection miss**

```
DFMEA Entry: FM-002
Function: Detect cardiac arrhythmia
Failure Mode: Fail to detect ventricular tachycardia
Effect: Patient does not receive timely therapy
Severity: 9 (life-threatening, delayed treatment)

Cause: Sensing ADC noise exceeds threshold
Occurrence: 3 (remote - qualified ADC design)

Current controls:
  Design: Redundant sensing channels
  Test: Full ADC characterization at production
  Detection: Self-test during device operation

Detection: 2 (very high - redundant channels)

RPN: 9 x 3 x 2 = 54
AP: Medium (M)
Action: Add sensing noise self-test during operation
```

**Failure Mode 3: Telemetry data corruption**

```
DFMEA Entry: FM-003
Function: Transmit patient data via telemetry
Failure Mode: Corrupted data transmitted to external reader
Effect: Incorrect clinical decisions based on faulty data
Severity: 7 (serious - incorrect diagnosis)

Cause: FSK modulation error due to PLL drift
Occurrence: 4 (very low - PLL locked in production)

Current controls:
  Design: CRC protection on telemetry packets
  Test: Full telemetry BER test at production
  Detection: CRC checking at receiver

Detection: 3 (almost certain - CRC detection)

RPN: 7 x 4 x 3 = 84
AP: Medium (M)
Action: Implement adaptive PLL tracking in firmware
```

### 2.3 Top DFMEA Risks

| Risk ID | Failure Mode | Severity | Occurrence | Detection | RPN | AP |
|---------|-------------|----------|------------|-----------|-----|-----|
| FM-001 | Pacing overvoltage | 10 | 2 | 2 | 40 | L |
| FM-002 | Arrhythmia miss | 9 | 3 | 2 | 54 | M |
| FM-003 | Telemetry corruption | 7 | 4 | 3 | 84 | M |
| FM-004 | Clock failure | 10 | 2 | 2 | 40 | L |
| FM-005 | Power management failure | 9 | 2 | 3 | 54 | M |
| FM-006 | Firmware boot failure | 8 | 2 | 2 | 32 | L |
| FM-007 | Lead impedance error | 7 | 3 | 3 | 63 | M |
| FM-008 | Temperature sensor error | 6 | 4 | 4 | 96 | M |

---

## 3. Process FMEA (PFMEA) for iPACE-CHIP

### 3.1 Manufacturing Process Map

```
iPACE-CHIP manufacturing process steps:
  1. Wafer fabrication (outsourced)
     ├── Front-end processing (transistor formation)
     ├── Back-end processing (metallization)
     ├── Wafer sort test
     └── Wafer storage

  2. Wafer dicing
     ├── Laser grooving
     ├── Mechanical dicing
     ├── Wafer cleaning
     └── Die inspection

  3. Die attach
     ├── Epoxy dispensing
     ├── Die pick and place
     ├── Epoxy curing
     └── X-ray inspection (sample)

  4. Wire bonding
     ├── Ball bonding (gold wire)
     ├── Wedge bonding
     ├── Bond pull test
     └── Bond shear test

  5. Molding
     ├── Mold compound mixing
     ├── Transfer molding
     ├── Deflash
     └── Cure verification

  6. Plating and trimming
     ├── Lead frame plating
     ├── Singulation
     ├── Lead trimming
     └── Forming

  7. Marking
     ├── Laser marking
     ├── Mark verification
     └── Visual inspection

  8. Final test
     ├── Electrical test
     ├── Burn-in (sample)
     ├── Tape and reel
     └── Shipping
```

### 3.2 PFMEA Worksheet Excerpts

**Process Step: Wire Bonding**

```
PFMEA Entry: PFM-001
Process Step: Wire bonding (ball bond)
Function: Electrical connection between die and lead frame
Failure Mode: Wire bond lift (non-stick)
Effect: Open circuit, device failure
Severity: 9 (device failure in implant)

Cause: Contaminated bond pad surface
Occurrence: 3 (remote - cleaned surface, controlled environment)

Current controls:
  Prevention: Bond pad pre-clean, controlled environment
  Detection: 100% bond pull test
  Detection capability: Automated pull test with force threshold

Detection: 2 (very high - 100% automated test)

RPN: 9 x 3 x 2 = 54
AP: Medium (M)
Action: Implement real-time bond quality monitoring (force vs. time)
```

**Process Step: Mold Compound**

```
PFMEA Entry: PFM-002
Process Step: Transfer molding
Function: Encapsulate die and bonds for protection
Failure Mode: Mold void near die surface
Effect: Moisture ingress, corrosion, reliability degradation
Severity: 8 (latent failure, reliability impact)

Cause: Incomplete mold fill (viscosity variation)
Occurrence: 4 (very low - process monitoring)

Current controls:
  Prevention: Mold compound viscosity monitoring
  Detection: X-ray inspection (sample), C-mode scanning (qualification)
  Detection capability: X-ray detects voids greater than 50um

Detection: 5 (high - X-ray sampling)

RPN: 8 x 4 x 5 = 160
AP: High (H)
Action: Implement 100% X-ray inspection for implantable devices
```

**Process Step: Final Test**

```
PFMEA Entry: PFM-003
Process Step: Final electrical test
Function: Screen defective devices
Failure Mode: Test escape (defective device passes test)
Effect: Defective device reaches patient
Severity: 10 (patient safety)

Cause: Test program bug or test limit error
Occurrence: 2 (very remote - validated test program)

Current controls:
  Prevention: Test program validation, golden device verification
  Detection: Correlation testing between ATE sites
  Detection capability: Daily golden device check, limit verification

Detection: 2 (very high - multiple verification methods)

RPN: 10 x 2 x 2 = 40
AP: Low (L)
Action: Maintain test program validation procedures
```

### 3.3 Top PFMEA Risks

| Risk ID | Process Step | Failure Mode | Severity | Occurrence | Detection | RPN | AP |
|---------|-------------|-------------|----------|------------|-----------|-----|-----|
| PFM-002 | Molding | Mold void | 8 | 4 | 5 | 160 | H |
| PFM-001 | Wire bond | Bond lift | 9 | 3 | 2 | 54 | M |
| PFM-003 | Final test | Test escape | 10 | 2 | 2 | 40 | L |
| PFM-004 | Die attach | Die crack | 9 | 2 | 3 | 54 | M |
| PFM-005 | Plating | Lead corrosion | 7 | 3 | 4 | 84 | M |
| PFM-006 | Marking | Incorrect marking | 6 | 2 | 2 | 24 | L |
| PFM-007 | Dicing | Die chipping | 8 | 3 | 3 | 72 | M |
| PFM-008 | Burn-in | Incomplete stress | 7 | 2 | 3 | 42 | M |

---

## 4. FMEA Process for iPACE-CHIP

### 4.1 FMEA Team Composition

```
DFMEA Team:
  Design lead (moderator)
  Circuit design engineer
  Layout engineer
  Firmware engineer
  Test engineer
  Quality engineer
  Reliability engineer
  Customer representative (optional)

PFMEA Team:
  Manufacturing engineer (moderator)
  Process engineer
  Quality engineer
  Test engineer
  Reliability engineer
  Supplier quality engineer (if outsourced)
  Equipment engineer
```

### 4.2 FMEA Execution Timeline

```
FMEA Schedule:
  Concept phase:
    ├── System FMEA initiation
    ├── High-level DFMEA
    └── Preliminary risk assessment

  Design phase:
    ├── Detailed DFMEA (iterative)
    ├── Design review integration
    └── DFM/DFT feedback

  Validation phase:
    ├── DFMEA verification through testing
    ├── PFMEA initiation for production
    └── Process FMEA development

  Production phase:
    ├── PFMEA refinement
    ├── Production data integration
    └── Continuous FMEA updates

  Post-market:
    ├── Field failure data integration
    ├── FMEA revision based on complaints
    └── Periodic review (annual minimum)
```

### 4.3 FMEA Review and Update

```
FMEA review triggers:
  Scheduled: Quarterly review meetings
  Event-driven:
    Design change (any modification)
    Process change (any modification)
    Customer complaint (related failure mode)
    CAPA initiation (related root cause)
    Audit finding (FMEA gap identified)
    New risk identified (through testing or field data)

Update documentation:
  Change log with rationale
  Before/after comparison
  Approval by FMEA team lead and quality
  Version control with change history
```

---

## 5. Risk Mitigation Strategies

### 5.1 Design Risk Mitigation

```
Mitigation approaches for DFMEA:
  Redundancy:
    Dual sensing channels for arrhythmia detection
    Redundant voltage regulators for pacing output
    Triple modular redundancy for safety-critical FSMs
    
  Monitoring:
    Watchdog timer for clock supervision
    IDDQ monitoring for defect detection
    Temperature monitoring for thermal protection
    Voltage monitoring for supply supervision
    
  Testability:
    Scan chain for high fault coverage
    BIST for memory and logic verification
    Boundary scan for interconnect testing
    Self-test during operation (in-field)
```

### 5.2 Process Risk Mitigation

```
Mitigation approaches for PFMEA:
  Prevention:
    SPC monitoring for process parameters
    Preventive maintenance on equipment
    Operator training and certification
    Incoming material inspection
    
  Detection:
    100% electrical test (parametric and functional)
    Automated optical inspection (AOI)
    X-ray inspection for internal defects
    Acoustic microscopy for delamination
    
  Correction:
    Real-time SPC response
    CAPA for systematic defects
    Process improvement projects
    Equipment calibration and maintenance
```

---

## 6. FMEA Integration with ISO 14971

### 6.1 Risk Management File

```
FMEA as part of Risk Management File:
  ISO 14971 Risk Analysis:
    ├── Hazard identification (from FMEA failure modes)
    ├── Risk estimation (using FMEA severity and occurrence)
    ├── Risk evaluation (using FMEA RPN/AP as input)
    └── Risk control (using FMEA mitigation strategies)

  FMEA as input to:
    ├── Risk-benefit analysis
    ├── Residual risk evaluation
    ├── Production and post-production monitoring
    └── Post-market surveillance plan
```

### 6.2 Risk Acceptability Matrix

```
Risk Acceptability (ISO 14971 aligned):
  Severity 9-10: Unacceptable risk (must reduce)
  Severity 7-8: ALARP region (reduce if practicable)
  Severity 1-6: Broadly acceptable (monitor)

FMEA drives:
  Severity determines risk acceptability
  Occurrence determines feasibility of risk reduction
  Detection determines residual risk level
```

---

## 7. FMEA Metrics and Reporting

### 7.1 FMEA Effectiveness Metrics

```
FMEA Quality Metrics:
  Risk reduction achieved:
    Before mitigation: Average RPN = 120
    After mitigation: Average RPN = 45
    Reduction: 62.5%
    
  High-risk items resolved:
    AP=High items: 3 identified, 3 resolved
    AP=Medium items: 12 identified, 10 resolved (83%)
    AP=Low items: 25 identified, no action needed (by definition)
    
  FMEA currency:
    FMEA age: Updated within 90 days of last change
    Review compliance: 100% quarterly reviews completed
    Team participation: 95% attendance at review meetings
```

### 7.2 FMEA Reporting

```
FMEA reporting to management:
  Quarterly: Summary of high-risk items and mitigation status
  Annually: Full FMEA review and update summary
  Event-driven: Any new high-risk item identified
  Post-market: Field failure correlation with FMEA predictions
```

---

## 8. Summary

FMEA provides the iPACE-CHIP organization with a systematic framework for identifying, evaluating, and mitigating potential failure modes across both design and manufacturing processes. The DFMEA ensures that patient safety is protected through redundant design features, comprehensive testing, and continuous monitoring. The PFMEA ensures manufacturing quality through process controls, inspection strategies, and corrective action procedures. Together with ISO 14971 risk management, FMEA forms the quantitative risk assessment backbone of the iPACE-CHIP quality assurance program.

---

## References

- AIAG & VDA. *FMEA Handbook*. 1st Edition, 2019.
- ISO 14971:2019: Medical Devices - Application of Risk Management
- IEC 60812:2018: Failure Modes and Effects Analysis (FMEA and FMECA)
- IEC 62304:2006+A1:2015: Medical Device Software - Software Life Cycle
- MIL-STD-1629A: Procedures for Performing a Failure Mode, Effects and Criticality Analysis
- J.E. Norman, FMEA *A Practical Approach*. SAE International, 2008
