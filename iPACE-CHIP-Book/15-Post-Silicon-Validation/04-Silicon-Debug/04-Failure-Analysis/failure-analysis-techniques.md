# Failure Analysis Techniques

## 15.16.1 Overview

Failure analysis (FA) is the systematic process of identifying the root cause of a failed semiconductor device. For the iPACE-CHIP, failure analysis is critical both during post-silicon validation (where die-level defects may be discovered) and during production (where field returns must be analyzed). The goal of FA is not merely to determine that a device has failed, but to understand why it failed, whether the failure is systematic or random, and what design or process changes can prevent recurrence. This chapter describes the complete failure analysis workflow from initial diagnosis through physical defect identification.

## 15.16.2 Failure Classification

### Failure Categories

```
iPACE-CHIP Failure Categories:

Category A: Systematic Failures
  - Affect all die in a lot or wafer region
  - Root cause: Design bug, mask error, process excursion
  - Examples: Timing violation, logic error, analog out of spec
  - FA approach: Design analysis, simulation, parametric review

Category B: Parametric Failures
  - Device functions but parameters out of specification
  - Root cause: Process variation, contamination, wear-out
  - Examples: High leakage, low speed, offset drift
  - FA approach: Electrical characterization, PCM correlation

Category C: Random Defect Failures
  - Single die affected, random spatial distribution
  - Root cause: Particle contamination, scratch, void
  - Examples: Stuck bit, open interconnect, short circuit
  - FA approach: Physical analysis (decap, SEM, FIB)

Category D: Functional Failures
  - Device does not function correctly
  - Root cause: Design bug or random defect
  - Examples: Wrong output, hangs, reset loop
  - FA approach: Electrical diagnosis, then physical analysis
```

### Failure Rate Breakdown

```
iPACE-CHIP Failure Analysis Data (500 units tested):

Failure Category          | Count | Percentage | Avg FA Time
--------------------------|-------|------------|------------
A: Systematic design      | 2     | 0.4%       | 2 weeks
B: Parametric             | 8     | 1.6%       | 1 week
C: Random defect          | 12    | 2.4%       | 2 weeks
D: Functional (unknown)   | 5     | 1.0%       | 3 weeks
No failure found          | 3     | 0.6%       | 1 week
--------------------------|-------|------------|------------
Total failed              | 30    | 6.0%       | 1.8 weeks avg
Passing                   | 470   | 94.0%      | N/A
```

## 15.16.3 FA Workflow

### Standard FA Process Flow

```
Step 1: Failure Documentation
  - Record failure symptom, test conditions, test program version
  - Save all test logs and measurement data
  - Classify failure category (A/B/C/D)

Step 2: Electrical Characterization
  - Repeat failure at original test conditions
  - Characterize across voltage and temperature
  - Perform additional parametric measurements
  - Run BIST (MBIST, LBIST) for fault isolation

Step 3: Fault Isolation
  - Use non-destructive techniques first:
    * Scan chain analysis (identify failing flip-flops)
    * OBIC (Optical Beam Induced Current) for leakage location
    * Thermal imaging for hot spots
    * E-beam probing for voltage waveforms
  - Narrow down to specific functional block or circuit

Step 4: Physical Analysis
  - Decapsulation (chemical or laser)
  - Optical inspection (stereo microscope)
  - SEM (Scanning Electron Microscope) imaging
  - FIB (Focused Ion Beam) cross-sectioning
  - EDX (Energy Dispersive X-ray) for material analysis

Step 5: Root Cause Identification
  - Correlate physical defect with electrical failure
  - Determine if defect is systematic or random
  - Assess impact on yield and reliability

Step 6: Corrective Action
  - For design bugs: RTL fix and respin
  - For process defects: Process adjustment or inspection improvement
  - For marginal designs: Guardband adjustment or redesign
  - Document findings and corrective actions
```

## 15.16.4 Non-Destructive Analysis

### Optical Inspection

```
Stereo Microscope Inspection:

Equipment: Zeiss Stemi 305 with 10x-50x zoom
Purpose: First-pass visual inspection of die surface

What to Look For:
  - Particles on die surface (potential short or contamination)
  - Scratches on metal layers (potential open circuit)
  - Discoloration (potential thermal damage)
  - Bond wire integrity (lifted ball, neck break, sweep)
  - Die attach quality (voids, delamination)
  - Solder ball alignment (for BGA packages)

iPACE-CHIP Inspection Checklist:
  [ ] Die surface clean (no particles > 5 um)
  [ ] All bond wires intact (64 wires for QFN package)
  [ ] Bond wire sweep < 2 wire widths
  [ ] Die attach void < 10% of pad area
  [ ] No visible scratches on top metal
  [ ] Passivation layer intact (no cracks)
  [ ] Marking legible (lot, date, revision)
```

### X-Ray Inspection

```
X-Ray Inspection for iPACE-CHIP:

Equipment: Nordson DAGE Quadra 7
Purpose: Inspect internal structure without decapsulation

Inspection Areas:
  1. Bond wire integrity
     - Wire bond pull strength estimate
     - Wire sweep measurement
     - Ball bond diameter measurement
  
  2. Die attach quality
     - Void percentage measurement
     - Void distribution pattern
  
  3. Solder ball alignment (BGA variant if applicable)
     - Ball-to-pad alignment
     - Solder bridge detection
  
  4. Lead frame integrity
     - Lead coplanarity
     - Lead damage or bending

Results (typical iPACE-CHIP):
  Bond wire sweep: 0.3 wire widths (limit: 2.0) PASS
  Die attach void: 5.2% (limit: 10%) PASS
  Ball bond diameter: 72 um (spec: 70-80 um) PASS
```

### Scanning Acoustic Microscopy (SAM)

```
SAM Inspection for iPACE-CHIP:

Equipment: Sonoscan D9000
Purpose: Detect internal delamination, voids, cracks

Frequency: 150 MHz (high resolution for small die)
Scan mode: C-mode (planar view at specific depth)

Inspection Layers:
  1. Mold compound / die interface (delamination detection)
  2. Die attach interface (void detection)
  3. Lead frame / mold compound interface
  4. Bond pad / bond wire interface

Results:
  Delamination: None detected at any interface
  Die attach voids: 5% (within specification)
  Lead frame: No delamination
  Bond pads: All bonds intact
  Status: PASS
```

## 15.16.5 Fault Isolation Techniques

### Scan Chain Analysis

```
Objective: Identify failing flip-flops from scan chain test data

Procedure:
  1. Run LBIST with scan chain test
  2. Record failing scan chain number and position
  3. Map flip-flop position to RTL module and gate name
  4. Identify the logic cone driving the failing flip-flop
  5. Analyze the logic cone for potential faults

Example Results:
  Failing chain: Chain 2 (Pacing state machine + timing)
  Failing FF: Chain 2, position 3,456
  RTL module: pace_ctrl.v
  Signal name: pace_ctrl/state_reg[3]
  Logic cone input: pace_ctrl/next_state[3]
  
  Fault type: Stuck-at-1 (FF always reads 1 regardless of input)
  
  Next step: Locate state_reg[3] on die and investigate physical defect
```

### OBIC (Optical Beam Induced Current)

```
Objective: Locate leakage current paths on the die

Equipment: Laser Scanning Microscope with OBIC detector
Principle: Focused laser generates electron-hole pairs in silicon
           Leakage junctions collect more photocurrent than normal junctions

Procedure:
  1. Decapsulate the die
  2. Illuminate the die with focused laser (1064 nm, below Si bandgap)
  3. Measure photocurrent at each supply pin
  4. Map photocurrent vs. beam position
  5. Bright spots indicate leakage junctions

Results:
  Leakage location: SRAM array, bank 2, row 15, column 8
  Leakage current at bright spot: 85 nA
  Nearby structures: SRAM cell access transistors
  
  Conclusion: A single SRAM cell has a gate oxide defect causing
  leakage from VDD to GND through the access transistor.
```

### Thermal Imaging

```
Objective: Locate hot spots indicating excessive power dissipation

Equipment: InfraTec ImageIR 8300 (microbolometer, 3-5 um)
Resolution: 5 um spatial, 20 mK thermal

Procedure:
  1. Power on die at nominal voltage
  2. Operate in known failing mode
  3. Capture thermal image
  4. Compare with thermal image of known-good die
  5. Identify temperature anomalies

Results:
  Good die thermal map: Uniform 42C across die (at 25C ambient)
  Failing die thermal map: Hot spot at (3.2 mm, 2.1 mm) = 58C
  Temperature delta: +16C at hot spot
  
  Hot spot location corresponds to VDD_DIG power switch in the
  telemetry block. The elevated temperature indicates excessive
  current through this switch.
  
  Root cause: Power switch transistor gate oxide defect causing
  partial conduction (leakage path through the switch).
```

## 15.16.6 Physical Failure Analysis

### Decapsulation

```
Chemical Decapsulation Procedure:

Equipment: Nordson DAGE Chemdek 8600
Chemicals: Fuming nitric acid (HNO3, 98%), sulfuric acid (H2SO4)

Procedure:
  1. Mount package in decapsulation chamber
  2. Heat fuming nitric acid to 110C
  3. Expose acid to package surface for 8-12 minutes
  4. Rinse with fresh nitric acid
  5. Rinse with acetone and IPA
  6. Dry with nitrogen gun
  7. Inspect under stereo microscope

Critical Parameters for iPACE-CHIP (QFN package):
  Acid temperature: 110C (not higher to protect bond wires)
  Exposure time: 10 minutes (enough to clear mold compound)
  Acid flow rate: 200 mL/min
  Final inspection: 20x magnification

Post-Decap Inspection:
  [ ] Die surface visible
  [ ] Bond wires intact (no acid damage)
  [ ] Die surface clean (no residual mold compound)
  [ ] Bond pads accessible for probing
```

### SEM Imaging

```
Scanning Electron Microscope Imaging:

Equipment: Zeiss Sigma 300 VP-SEM
Acceleration voltage: 1-20 kV (adjustable for contrast)
Detector: SE2 (secondary electron), In-lens, BSE (backscattered)

Imaging Modes for iPACE-CHIP FA:

1. Surface Topography (SE2 detector):
   - Reveals physical features (particles, scratches, voids)
   - Voltage: 5 kV, Working distance: 8 mm
   - Resolution: 5 nm

2. Voltage Contrast (SE2 detector):
   - Reveals electrical state (conducting vs. insulating)
   - Voltage: 1 kV (low voltage for surface sensitivity)
   - Bright = positive voltage, Dark = negative voltage

3. Material Contrast (BSE detector):
   - Reveals material differences (metal vs. silicon vs. oxide)
   - Voltage: 15 kV, Working distance: 10 mm
   - Bright = heavy elements (metal), Dark = light elements (oxide)

4. Cross-Section Imaging (after FIB):
   - Reveals vertical structure of defect
   - Voltage: 5 kV, Working distance: 5 mm
   - Resolution: 2 nm
```

### SEM Inspection Results

```
iPACE-CHIP Physical Defect Analysis (from 12 random defect failures):

Defect # | Location          | Type              | Size    | Impact
---------|-------------------|-------------------|---------|------------------
1        | SRAM Bank 0       | Particle on metal | 2.3 um  | Short circuit
2        | SRAM Bank 2       | Gate oxide defect | 50 nm   | Leakage path
3        | AFE input stage   | Metal void        | 1.5 um  | Open circuit
4        | Clock buffer      | Particle on gate  | 800 nm  | Threshold shift
5        | Pacing output     | Metal bridge      | 3.2 um  | Short to GND
6        | Telemetry block   | Via void          | 400 nm  | Open connection
7        | Flash array       | Oxide pinhole     | 30 nm   | Data retention
8        | Power grid        | Particle on via   | 1.8 um  | High resistance
9        | SPI interface     | Metal scratch     | 5 um    | Open trace
10       | Bandgap reference | Contamination    | 2.5 um  | Offset error
11       | Watchdog timer    | Particle on gate  | 1.2 um  | Timing error
12       | ADC comparator    | Metal void        | 900 nm  | Offset error

Defect Size Distribution:
  < 100 nm: 2 defects (17%)
  100-500 nm: 3 defects (25%)
  500 nm - 1 um: 2 defects (17%)
  1-3 um: 4 defects (33%)
  > 3 um: 1 defect (8%)

Most defects are in the 100 nm - 3 um range, consistent with
particle contamination from the fabrication environment.
```

### FIB Cross-Sectioning

```
Focused Ion Beam Cross-Section:

Equipment: FEI Helios NanoLab 600i (dual-beam SEM/FIB)
Ion beam: Ga+ at 30 kV
Milling current: 0.5-10 nA (depending on precision needed)

Procedure:
  1. Navigate to defect location (from SEM inspection)
  2. Deposit protective platinum layer (100 nm)
  3. Mill cross-section trench with high-current beam (10 nA)
  4. Clean cross-section surface with low-current beam (100 pA)
  5. Image cross-section with SEM

Cross-Section Results (Defect #5: Metal bridge):
  Image shows metallic material bridging two adjacent metal lines
  Bridge width: 3.2 um (matching particle size from top-view)
  Bridge composition: Copper (from EDX analysis)
  
  Root cause: Copper particle from CMP process landed on metal layer
  during fabrication, creating a short circuit between M2 lines.
  
  Corrective action: Improve post-CMP cleaning process,
  add additional particle inspection after M2 deposition.
```

## 15.16.7 EDX Analysis

### Energy Dispersive X-ray Spectroscopy

```
Objective: Identify chemical composition of defect materials

Equipment: Oxford Instruments X-Max 80 (attached to Zeiss Sigma SEM)
X-ray energy range: 0-20 keV
Spatial resolution: ~1 um

Analysis of Defect #1 (Particle on metal):
  Element     | Weight % | Expected
  ------------|----------|--------
  Copper (Cu) | 95.2     | Particle material
  Silicon (Si)| 2.1      | Substrate
  Oxygen (O)  | 1.8      | Oxide layer
  Carbon (C)  | 0.9      | Residual organics
  
  Conclusion: Copper particle (from CMP slurry or interconnect)
  Probability: CMP process contamination

Analysis of Defect #10 (Bandgap contamination):
  Element     | Weight % | Expected
  ------------|----------|--------
  Silicon (Si)| 68.5     | Substrate
  Oxygen (O)  | 28.3     | Oxide
  Sodium (Na) | 2.1      | Contamination!
  Chlorine(Cl)| 1.1      | Contamination!
  
  Conclusion: Sodium and chlorine contamination
  Source: Likely from inadequate rinsing after wet processing
  Impact: Sodium drifts in oxide, causing threshold voltage shift
  Corrective action: Improve rinsing protocol, add sodium monitor
```

## 15.16.8 Failure Analysis Report Template

### Standard FA Report Structure

```
iPACE-CHIP Failure Analysis Report

1. Header Information
   - Report number: iPACE-FA-NNN
   - Date: YYYY-MM-DD
   - Analyst: Name
   - Device: iPACE-CHIP, Lot XXX, Wafer YY, Die (row, col)
   - Package: 64-pin QFN

2. Failure Description
   - Test that detected failure: Test ID and name
   - Failure symptom: Detailed description
   - Test conditions: Voltage, temperature, test program version
   - Failure rate: How many units with same symptom

3. Electrical Analysis
   - Reproducibility: Can failure be repeated? Conditions?
   - Fault isolation: Scan chain, OBIC, thermal imaging results
   - Root cause hypothesis: Based on electrical evidence

4. Physical Analysis
   - Decapsulation: Method, inspection results
   - Optical inspection: Findings
   - SEM imaging: Defect images and measurements
   - FIB cross-section: Internal structure images
   - EDX analysis: Material composition

5. Root Cause Confirmation
   - Correlation between physical defect and electrical failure
   - Defect mechanism: How the defect causes the failure
   - Defect origin: When/where in the process did the defect occur

6. Corrective Action
   - Design change (if applicable): RTL modification
   - Process change (if applicable): Process recipe adjustment
   - Test improvement: Additional tests to screen similar defects
   - Monitoring: Enhanced inspection at specific process steps

7. Conclusion
   - Root cause summary
   - Impact on yield and reliability
   - Recommendation for next steps
```

## 15.16.9 Failure Analysis Data Management

### FA Database

```
iPACE-CHIP FA Database Schema:

Tables:
  failures:
    failure_id (PK)
    lot_number
    wafer_id
    die_row
    die_col
    test_id
    failure_mode
    failure_category (A/B/C/D)
    status (open/analyzing/complete)
    date_detected
    analyst

  analyses:
    analysis_id (PK)
    failure_id (FK)
    analysis_type (electrical/physical/chemical)
    technique
    result
    image_path
    date

  defects:
    defect_id (PK)
    failure_id (FK)
    defect_type
    location_x
    location_y
    size_um
    material
    root_cause
    corrective_action
```

### FA Trend Analysis

```
Monthly FA Trend (iPACE-CHIP):

Month    | Units Tested | Failed | Yield  | Top Failure Mode
---------|-------------|--------|--------|------------------
January  | 4500        | 180    | 96.0%  | Random defect
February | 5200        | 195    | 96.3%  | Random defect
March    | 5800        | 174    | 97.0%  | Random defect
April    | 6100        | 165    | 97.3%  | Parametric
May      | 6500        | 156    | 97.6%  | Parametric
June     | 7000        | 147    | 97.9%  | Random defect

Trend: Yield improving over time as process matures.
The shift from random defect to parametric as dominant failure mode
indicates that random defects are being reduced by improved process
control, while parametric failures remain due to process variation.
```

## 15.16.10 Corrective Action Effectiveness

```
Corrective Action Tracking:

CA-001: Improve post-CMP cleaning
  - Defect type: Copper particles (Defect #5)
  - Implementation: Additional megasonic clean step
  - Effective date: March 2026
  - Result: Copper particle failures reduced from 5 to 1 per 5000 units

CA-002: Add sodium monitor to wet bench
  - Defect type: Sodium contamination (Defect #10)
  - Implementation: Daily sodium measurement in rinse water
  - Effective date: April 2026
  - Result: Sodium-related failures eliminated

CA-003: Tighten particle spec for incoming wafers
  - Defect type: Particles on gate (Defect #4, #11)
  - Implementation: Incoming wafer inspection at > 200 nm
  - Effective date: May 2026
  - Result: Gate particle failures reduced from 4 to 0 per 5000 units

Overall FA effectiveness:
  Pre-CA yield: 96.0%
  Post-CA yield: 97.9%
  Yield improvement: 1.9 percentage points
  Annual revenue impact: ~$2M (at projected volume)
```

## 15.16.11 Summary

The failure analysis methodology for the iPACE-CHIP combines electrical fault isolation with physical defect characterization to identify root causes of failures with high confidence. The systematic approach, from non-destructive techniques (optical inspection, X-ray, SAM) through fault isolation (scan chain analysis, OBIC, thermal imaging) to physical analysis (SEM, FIB, EDX), ensures that no failure mode is overlooked. The FA data management system enables trend analysis and corrective action tracking, driving continuous improvement in yield and reliability. With an overall yield of 97.9% and a well-understood failure population, the iPACE-CHIP manufacturing process is mature and controllable.
