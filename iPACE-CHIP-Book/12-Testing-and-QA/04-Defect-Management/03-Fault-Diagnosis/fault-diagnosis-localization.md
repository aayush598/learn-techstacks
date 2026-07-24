# Fault Diagnosis and Localization

## Overview

Fault diagnosis and localization is the process of identifying the physical location and root cause of defects detected during iPACE-CHIP electrical testing. When a device fails wafer sort or final test, fault diagnosis uses the test failure information to narrow down the possible defect locations, enabling efficient physical failure analysis (PFA). For the iPACE-CHIP medical device, accurate fault diagnosis is essential for yield improvement, reliability assessment, and ensuring no systematic defects reach patients.

---

## 1. Fault Diagnosis Fundamentals

### 1.1 Diagnosis Flow Overview

```
Electrical Test Failure
    |
    v
Test Response Analysis
    |
    v
Fault Dictionary Lookup
    |
    v
Diagnostic Pattern Generation
    |
    v
Candidate Fault List
    |
    v
Physical Failure Analysis (PFA)
    |
    v
Root Cause Identification
    |
    v
Corrective Action
```

### 1.2 Fault Diagnosis Approaches

| Approach | Method | Accuracy | Speed | Cost |
|----------|--------|----------|-------|------|
| Dictionary-based | Pre-computed fail signatures | High | Fast | Low |
| Simulation-based | Re-simulate with fault models | Very high | Slow | Medium |
| Machine learning | Trained on historical data | High | Fast | Low |
| Probe-based | Direct electrical probing | Very high | Slow | High |
| E-beam | Voltage contrast imaging | Very high | Medium | High |

### 1.3 Failure Signature Types

```
Failure signatures from iPACE-CHIP testing:
  Scan chain failures:
    ├── Single scan cell failure: localized to one FF
    ├── Multiple cell failures: logic cone analysis
    ├── Chain break: specific location in chain
    └── Chain short: adjacent chain interference
    
  IDDQ failures:
    ├── Current above threshold: bridging or leakage
    ├── Spatial pattern: indicates systematic defect
    └── Correlation with test vector: narrows location
    
  Functional failures:
    ├── Single output failure: trace back to logic cone
    ├── Multiple related failures: common cause analysis
    └── Timing failure: critical path identification
    
  Memory failures:
    ├── Single bit failure: specific SRAM cell
    ├── Row failure: word line issue
    ├── Column failure: bit line issue
    └── Multiple random failures: systematic process issue
```

---

## 2. Dictionary-Based Diagnosis

### 2.1 Fault Dictionary Construction

```
Fault Dictionary Structure:
  For each detectable fault:
    Fault ID: Unique identifier
    Location: Net name, gate, pin
    Physical location: (x, y) on die
    Detection patterns: List of test patterns that detect this fault
    Failure response: Expected vs. actual for each detection pattern
    Equivalent faults: Other faults with same signature
    
Example dictionary entry:
  Fault: SA0 on U1234/A (AND gate input)
  Location: Module arrhythmia_detector, cell U1234
  Physical: (1250, 800) um from die origin
  Detection patterns: [452, 1207, 8934]
  Pattern 452 response: Chain 3, Cell 847 reads 0 (expected 1)
  Pattern 1207 response: Chain 5, Cell 203 reads 0 (expected 1)
  Equivalent faults: [U1234/A SA0, U1233/Y SA0]
```

### 2.2 Dictionary Lookup Algorithm

```
Dictionary Lookup Process:
  Step 1: Capture failing pattern(s) and response(s)
    Example: Pattern 452 fails, Chain 3 Cell 847 = 0 (expected 1)
    
  Step 2: Search dictionary for matching entries
    Match on: Pattern number + Failing cell + Actual value
    Results: 15 candidate faults match this signature
    
  Step 3: Apply additional failing patterns for discrimination
    Pattern 1207 also fails: Chain 5, Cell 203
    Additional matching reduces candidates to 3
    
  Step 4: Rank candidates by likelihood
    Candidate 1: U1234/A SA0 (matched 2 patterns, closest physical)
    Candidate 2: U1233/Y SA0 (matched 2 patterns)
    Candidate 3: U1235/B SA0 (matched 2 patterns)
    
  Step 5: Output ranked candidate list with confidence
    Top candidate: 75% confidence
    Second candidate: 15% confidence
    Third candidate: 10% confidence
```

### 2.3 Diagnostic Resolution

```
Diagnostic resolution metrics:
  Resolution: Number of unique candidates per failure
  
  For iPACE-CHIP:
    Single-bit scan failures: Resolution = 1 (exact location)
    Multi-bit scan failures: Resolution = 2-5 candidates
    IDDQ failures: Resolution = 5-20 candidates
    Functional failures: Resolution = 3-10 candidates
    
  Diagnostic accuracy:
    Top-1 accuracy (correct in first candidate): 72%
    Top-3 accuracy (correct in top 3 candidates): 91%
    Top-5 accuracy: 96%
```

---

## 3. Scan Chain Diagnosis

### 3.1 Scan Chain Fault Models

```
Scan chain fault types:
  Stuck-at fault:
    Scan cell output stuck at 0 or 1
    Detection: Chain integrity test (shift known pattern)
    Localization: Shift-in known pattern, identify failing cell
    
  Open fault:
    Break in scan chain between two cells
    Detection: Chain test (upstream cells shift correctly, downstream don't)
    Localization: Binary search to isolate break point
    
  Short fault:
    Adjacent scan chains shorted together
    Detection: Cross-chain interference during shift
    Localization: Compare individual chain responses
    
  Hold fault:
    Scan cell holds previous value (not updating)
    Detection: Pattern comparison between consecutive shifts
    Localization: Cell-level identification through timing analysis
```

### 3.2 Scan Chain Diagnosis Flow

```
Scan chain diagnosis procedure:
  Step 1: Run chain integrity test
    ├── Shift 01010101 pattern through all chains
    ├── Compare output with expected pattern
    └── Identify failing chain(s) and failing cell(s)
    
  Step 2: Localize failing cell
    ├── Binary search: shift pattern to isolate failing segment
    ├── For N-cell chain: log2(N) steps to locate
    ├── iPACE-CHIP chain: log2(1250) = 11 steps
    └── Result: Exact failing cell number
    
  Step 3: Determine fault type
    ├── Cell stuck at 0: Input forced to 0
    ├── Cell stuck at 1: Input forced to 1
    ├── Cell not updating: Clock or enable issue
    └── Open in chain: Signal not propagating
    
  Step 4: Physical location mapping
    ├── Map cell number to physical (x, y) location
    ├── Cross-reference with layout database
    └── Output PFA coordinates
```

### 3.3 Scan Chain Diagnostic Example

```
Example diagnosis:
  Device: iPACE-CHIP-LOT045-DIE1234
  Test: Scan chain integrity test
  Result: FAIL on Chain 5
  
  Diagnosis:
    Chain 5 has 1250 cells
    Shift 01010101: Output matches for first 342 cells
    Output mismatches starting at cell 343
    
    Binary search:
      Cells 1-625: Output matches for first 342, fails at 343
      Cells 343-625: All output 0 (stuck at 0)
      Cells 343-484: All output 0
      Cells 343-413: All output 0
      Cells 343-378: All output 0
      Cells 343-360: All output 0
      Cells 343-351: All output 0
      Cells 343-347: All output 0
      Cell 343: Output stuck at 0
      
    Diagnosis: Cell 343 on Chain 5 stuck at 0
    Physical location: (1248, 796) um
    Layout trace: Scan FF in arrhythmia_detector module
    Probable defect: Via open or metal open in scan path
```

---

## 4. Logic Cone Diagnosis

### 4.1 Logic Cone Analysis

```
Logic cone analysis for scan failures:
  For each failing scan cell:
    1. Trace backward through combinational logic
    2. Identify all gates that drive the failing cell
    3. This forms the "logic cone" of the failing cell
    
  Example:
    Failing cell: Chain 3, Cell 847
    Logic cone:
      ├── Gate U456 (AND): Inputs from U123, U445
      ├── Gate U445 (OR): Inputs from U111, U321
      ├── Gate U321 (XOR): Inputs from U222, U223
      └── Gate U222 (INV): Input from U123
      
    Candidate fault locations:
      All nets and gates within the logic cone
      Total: 12 gates, 25 nets = 37 candidate locations
      
    Refinement with multiple patterns:
      Pattern 1207 also fails: Narrowed to 8 candidate locations
      Additional patterns reduce candidates further
```

### 4.2 Fault Simulation for Diagnosis

```
Fault simulation approach:
  Step 1: Re-simulate failing pattern with candidate faults
    Inject each candidate fault one at a time
    Compare simulation output with actual failure
    
  Step 2: Score each candidate
    Exact match: High confidence
    Partial match: Medium confidence
    No match: Low confidence
    
  Step 3: Report ranked candidate list
    For iPACE-CHIP:
      Typically 3-5 candidates after 3 patterns
      Top candidate correct 75% of the time
      Top 3 correct 91% of the time
```

---

## 5. IDDQ-Based Diagnosis

### 5.1 IDDQ Failure Analysis

```
IDDQ diagnosis methodology:
  IDDQ failure indicates excess quiescent current
  
  Diagnosis steps:
    1. Measure IDDQ at multiple test vectors
    2. Compare current levels across vectors
    3. Use current magnitude to estimate defect type:
       - 5-50 uA: Gate oxide leakage (small defect)
       - 50-500 uA: Junction leakage (medium defect)
       - 500 uA to 5 mA: Metal bridging (large defect)
       - greater than 5 mA: Power supply short
    4. Use spatial analysis to narrow location
    
  Spatial analysis:
    Compare IDDQ failure map with layout
    Defects cluster in specific regions
    Correlate with process step inspection data
```

### 5.2 IDDQ Diagnostic Patterns

```
IDDQ diagnostic pattern generation:
  Objective: Generate patterns that maximize IDDQ
  sensitivity at specific defect locations
  
  Pattern types:
    ├── stuck-at activation: Drive fault site to opposite value
    ├── Bridge activation: Drive adjacent nets to opposite values
    └── Leakage activation: Maximize voltage across suspect junction
    
  For each candidate defect location:
    Generate pattern that maximizes IDDQ sensitivity
    Apply pattern and measure IDDQ
    Compare with baseline to confirm or eliminate candidate
```

---

## 6. Memory Fault Diagnosis

### 6.1 SRAM Fault Diagnosis

```
SRAM fault diagnosis from MBIST:
  Fault type identification:
    SA0 (Stuck-at-0):
      Fails when writing 1 and reading back
      Read always returns 0
      
    SA1 (Stuck-at-1):
      Fails when writing 0 and reading back
      Read always returns 1
      
    TF (Transition fault):
      Fails to transition 0->1 or 1->0
      Detected by March elements with read-after-write
      
    AF (Address decoder fault):
      Multiple addresses map to same cell
      Detected by March elements with address ordering
      
    CF (Coupling fault):
      One cell affects another cell
      Detected by March elements with specific cell ordering
      
  Diagnostic output:
    Failing address: Row and column coordinates
    Failing bit: Expected vs. actual value
    Fault type: Classified based on March pattern analysis
    Physical location: Mapped to SRAM cell coordinates
```

### 6.2 SRAM Fault Localization

```
SRAM fault localization flow:
  Step 1: Run MBIST and capture fail data
    Fail address: Row 128, Column 45
    Fail bit: Expected 1, Actual 0
    
  Step 2: Determine fault type
    Write 0, read: 0 (pass)
    Write 1, read: 0 (fail)
    Conclusion: SA0 on bit 45 of row 128
    
  Step 3: Map to physical location
    Row 128: Word line WL_128
    Column 45: Bit line pair BL_45/BLB_45
    Physical: (x=1245, y=812) um on die
    
  Step 4: Assess repairability
    Redundancy analysis:
      Row 128 is in active array (not redundant row)
      Column 45 can be replaced with redundant column
      Repair solution: Blow column repair fuse
    Re-test after repair: PASS
```

---

## 7. Physical Failure Analysis

### 7.1 PFA Techniques

```
PFA techniques for iPACE-CHIP:
  Non-destructive:
    ├── Optical microscopy (50x to 200x magnification)
    ├── X-ray inspection (internal structure)
    ├── C-mode scanning acoustic microscopy (C-SAM)
    └── Emission microscopy (EMMI) for hot spot detection
    
  Semi-destructive:
    ├── De-layering (chemical or mechanical)
    ├── Selective etching (expose specific layers)
    └── Focused ion beam (FIB) for cross-sectioning
    
  Destructive:
    ├── Full cross-sectioning for TEM analysis
    ├── Energy dispersive X-ray (EDX) for composition
    └── Secondary ion mass spectrometry (SIMS) for profiling
```

### 7.2 Emission Microscopy (EMMI)

```
EMMI for fault localization:
  Principle: Defective transistors emit photons during switching
  Sensitivity: Detects leakage paths as small as 1 nA
  
  For iPACE-CHIP IDDQ failures:
    Apply IDDQ-failing test vector
    Image die surface with EMMI camera
    Bright spots indicate leakage sources
    
  Example result:
    IDDQ failure at vector #452
    EMMI image shows bright spot at (1250, 800) um
    Cross-reference with layout: NMOS transistor M456
    Physical defect: Gate oxide breakdown at M456
    
  PFA preparation:
    Mark location for SEM cross-sectioning
    FIB cut at (1250, 800) um
    SEM imaging of cross-section
    Defect confirmed: Oxide void at gate edge
```

### 7.3 Failure Analysis Report

```
Failure Analysis Report Template:
  Device Information:
    ├── Device ID and serial number
    ├── Lot number and wafer number
    ├── Die coordinates
    └── Test failure information
    
  Electrical Analysis:
    ├── Failing test and pattern
    ├── Failure signature description
    ├── Diagnostic results (candidate faults)
    └── EMMI/emission results
    
  Physical Analysis:
    ├── Cross-section images (SEM)
    ├── EDX composition analysis
    ├── Defect description and location
    └── Comparison with reference (good device)
    
  Root Cause:
    ├── Defect mechanism
    ├── Process step of origin
    ├── Systematic vs. random
    └── Risk to other devices in lot
    
  Corrective Action:
    ├── Immediate containment
    ├── Root cause elimination
    ├── Process improvement recommendation
    └── Verification of effectiveness
```

---

## 8. Diagnostic Software Tools

### 8.1 EDA Diagnostic Tools

```
Diagnostic software used for iPACE-CHIP:
  Synopsys Diagnostics (TD):
    ├── Scan chain diagnosis
    ├── Logic cone analysis
    ├── Fault simulation
    └── Diagnostic resolution: Typically 1-5 candidates
    
  Cadence Modus DFT:
    ├── Scan diagnosis
    ├── Logic diagnosis
    ├── Cell-aware diagnosis
    └── Diagnostic accuracy: 80% top-1
    
  Siemens Tessent Diagnosis:
    ├── Multi-chain diagnosis
    ├── Cell-aware fault models
    ├── Defect probability ranking
    └── Integration with PFA tools
    
  Mentor Graphics (Siemens) HyperScan:
    ├── Scan chain diagnosis
    ├── Bridge fault diagnosis
    └── Netlist-to-layout correlation
```

### 8.2 Diagnostic Data Flow

```
Diagnostic data flow:
  ATE test results (failure data)
    |
    v
Diagnostic database
    |
    v
EDA diagnostic tool (TD, Modus, etc.)
    |
    v
Candidate fault list
    |
    v
Layout database (GDS/OASIS)
    |
    v
PFA coordinate mapping
    |
    v
PFA lab (SEM, FIB, EMMI)
    |
    v
Root cause report
    |
    v
Corrective action (CAPA system)
```

---

## 9. Summary

Fault diagnosis and localization transforms electrical test failures into actionable physical defect information for the iPACE-CHIP. Dictionary-based and simulation-based diagnostic methods provide candidate fault locations with 91% top-3 accuracy, enabling efficient physical failure analysis. Scan chain diagnosis pinpoints specific failing cells, IDDQ analysis identifies leakage mechanisms, and memory diagnosis classifies SRAM fault types. The combination of automated diagnostic software and systematic PFA provides the root cause information essential for yield improvement and defect prevention in this zero-defect medical device manufacturing program.

---

## References

- Abramovici, M., Breuer, M.A., & Friedman, A.D. *Digital Systems Testing and Testable Design*. IEEE Press, 1990.
- Bushnell, M.L. & Agrawal, V.D. *Essentials of Electronic Testing*. Springer, 2000.
- Synopsys TestMAX Diagnostics User Guide
- Cadence Modus DFT Software Solution User Guide
- Siemens Tessent Diagnosis User Guide
- MIL-STD-883: Test Methods for Microelectronics (Method 1014 - Failure Analysis)
- IEC 60747-1: Semiconductor Devices - General
