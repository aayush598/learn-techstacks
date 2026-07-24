# Wafer-Level Testing

## Overview

Wafer-level testing (wafer sort or probe test) is the first electrical screening of the iPACE-CHIP after fabrication. Every die on the silicon wafer is contacted via probe card and subjected to parametric, functional, and BIST testing to identify defective die before the expensive packaging process. For a medical-grade implantable device, wafer sort must achieve extremely high defect detection with minimal overkill of good die, directly impacting both product quality and manufacturing cost.

---

## 1. Wafer Sort Strategy

### 1.1 Testing Philosophy

The iPACE-CHIP wafer sort employs a multi-tiered testing approach:

```
Tier 1: Parametric Screening (100% die)
├── Supply current measurement (IDDQ)
├── Input/output voltage levels
├── Leakage current at all pads
├── Oscillator frequency verification
└── Pass/Fail: Binary decision

Tier 2: Structural Testing (100% die)
├── Scan chain integrity
├── Memory BIST
├── Logic BIST (reduced set)
├── Boundary scan chain verification
└── Pass/Fail: Binary decision

Tier 3: Functional Testing (100% die)
├── Clock system verification
├── Power-on-reset sequence
├── Basic telemetry link test
├── Pacing output driver test
├── Lead impedance measurement
└── Pass/Fail: Binary decision

Tier 4: Parametric Characterization (sample-based)
├── Full voltage sweep
├── Frequency sweep
├── Temperature sweep (limited by probe setup)
└── Characterization data for design validation
```

### 1.2 Test Insertion Points

```
Wafer Probe Card Contact
         │
         ▼
┌─────────────────────────────────────────────┐
│              Probe Station                   │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │         Probe Card (custom)            │  │
│  │   ├── 64 signal probes                 │  │
│  │   ├── 8 power probes (VDD/VSS pairs)   │  │
│  │   ├── 4 guard probes (analog ground)   │  │
│  │   └── Thermal chuck interface          │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │         Probe Station                  │  │
│  │   ├── Manual/semi-auto for dev         │  │
│  │   ├── Fully auto for production        │  │
│  │   ├── Vision alignment system          │  │
│  │   └── Chuck temperature: -40 to 125°C  │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │         ATE Interface                  │  │
│  │   ├── Keithley 4200A (DC parametric)   │  │
│  │   ├── Teradyne J750 (digital test)     │  │
│  │   ├── Custom RF module (telemetry)     │  │
│  │   └── Precision current meters         │  │
│  └────────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### 1.3 Probe Card Design

The probe card is custom-designed for the iPACE-CHIP die layout:

| Parameter | Specification |
|-----------|--------------|
| Probe count | 72 (64 signal + 8 power) |
| Probe pitch | 100 μm minimum |
| Probe tip material | tungsten-rhenium |
| Contact force | 25-50 mN per probe |
| Probe card life | >500,000 contacts |
| Alignment accuracy | ±5 μm |
| RF probe bandwidth | DC to 3 GHz (telemetry test) |
| DC current capability | ±10 mA per signal probe |
| Power delivery | 500 mA per power pair |

---

## 2. Probe Card Layout

### 2.1 Die Pad Arrangement

The iPACE-CHIP die uses a peripheral pad arrangement optimized for probe testing:

```
Die Dimensions: 3.2mm × 3.2mm (active area)
Pad pitch: 120 μm
Pad size: 80μm × 80μm (probe compatible)
Pad opening: 65μm × 65μm

Pad ring layout (top view):
┌─────────────────────────────────────────┐
│  VDD  TCK TMS TDI TDO TRST  VDD  VDD  │
│  VSS  SENSE_A SENSE_B ... PACE_A VSS   │
│                                         │
│            ACTIVE AREA                  │
│          (iPACE-CHIP core)              │
│                                         │
│  VSS  TELE_TX TELE_RX ... SPI_CLK VSS  │
│  VDD  XTAL_IN XTAL_OUT ... VDD  VDD  VDD│
└─────────────────────────────────────────┘
```

### 2.2 Probe Card Electrical Design

**Signal integrity considerations:**
- Controlled impedance traces: 50Ω single-ended
- Trace length matching: ±0.5mm for differential pairs
- Crosstalk isolation: >40dB between adjacent probes
- Return loss: <-15dB at 1 GHz

**Power delivery:**
- Low-inductance power probes with integrated decoupling
- Probe resistance: <100 mΩ per power probe
- Current capacity: 1A continuous per power pair
- Transient response: <100mV droop during 100mA step

### 2.3 Probe Card Maintenance

| Maintenance Task | Frequency | Criteria |
|-----------------|-----------|----------|
| Visual inspection | Every 10,000 contacts | No bent/damaged tips |
| Cleaning | Every 5,000 contacts | IPA soak + ultrasonic |
| Electrical check | Every 1,000 contacts | Contact resistance <1Ω |
| Replacement | Per maintenance log | >500,000 contacts or damage |
| Alignment verification | Start of each lot | ±5μm on pad center |

---

## 3. Parametric Testing

### 3.1 DC Parametric Tests

**Supply Current (IDDQ):**

```
Measurement Setup:
├── VDD = 1.8V (nominal)
├── VSS = 0V
├── All inputs driven to known state
├── Wait 100μs for current stabilization
├── Measurement accuracy: ±1μA
└── Pass criteria: IDDQ < 5μA (quiescent)

IDDQ Specification:
├── Typical: 1.2μA
├── Maximum: 5μA (production limit)
├── Reliability limit: 10μA (samples only)
└── Failure indication: >5μA (possible defect)
```

**Input Leakage Current:**

```
For each input pad:
├── Apply VDD to pad, measure current to VSS
├── Apply VSS to pad, measure current to VDD
├── Specification: |ILEAK| < 1μA
└── Failure: Excessive leakage indicates ESD damage or oxide defect
```

**Output Drive Strength:**

```
For each output pad:
├── Measure VOH at IOH = -1mA (output high, sinking current)
├── Measure VOL at IOL = 1mA (output low, sourcing current)
├── VOH specification: >VDD - 0.4V
├── VOL specification: <VSS + 0.4V
└── Failure: Output cannot drive specified load
```

### 3.2 Oscillator Verification

```
Measurement:
├── Apply power, measure XTAL_OUT frequency
├── Expected: 32.768 kHz ± 100ppm
├── Measure startup time: <1ms
├── Measure amplitude: >0.5Vpp
└── Failure: No oscillation, wrong frequency, slow startup

For system clock PLL:
├── Enable PLL after oscillator stable
├── Measure PLL lock time: <100μs
├── Verify PLL output: target frequency ±0.1%
├── Jitter measurement: <50ps RMS
└── Failure: PLL fails to lock, wrong output frequency
```

### 3.3 Voltage Reference Verification

```
Bandgap reference output:
├── Measure output voltage at pin
├── Expected: 1.220V ± 1%
├── Temperature coefficient: <50ppm/°C
├── Line regulation: <0.1%/V
└── Failure: Out of specification

Internal voltage regulators:
├── Measure each regulated rail
├── Verify load regulation
├── Check dropout voltage
└── Failure: Regulation failure indicates analog defect
```

---

## 4. Structural Testing

### 4.1 Scan Chain Test

```
Scan chain integrity check:
├── Apply known pattern through TAP controller
├── Verify all chains shift correctly
├── Maximum shift frequency test
├── Identify broken/shorted chains
└── Pass: All chains shift correctly at 20 MHz

Production scan ATPG:
├── Run compressed stuck-at patterns (250 patterns)
├── Run compressed transition patterns (100 patterns)
├── Compare responses against golden reference
└── Pass: All patterns match, >99% fault coverage
```

### 4.2 Memory BIST

```
MBIST execution sequence:
├── Run March RAW on arrhythmia buffer (critical)
├── Run March G on register file
├── Run March C- on telemetry FIFO, ADC buffer
├── Run March G on firmware cache
├── Capture fail addresses and data
├── Run redundancy analysis
├── If repairable: program repair fuses (laser fuse)
└── Pass: All memories pass or successfully repaired

Memory test results:
├── Pass: No fails detected
├── Repass: Fails detected, repaired, retest passes
├── Fail: Fails detected, not repairable → die marked defective
└── Conditional pass: Limited fails within budget → engineering review
```

### 4.3 Logic BIST

```
LBIST execution:
├── Run 3 seeds × 1M patterns (production subset)
├── Verify signature after each seed
├── Compare against golden signature
├── Pass: All signatures match
└── Fail: Signature mismatch → further investigation required
```

---

## 5. Functional Testing

### 5.1 Power-On-Reset (POR) Sequence

```
POR verification:
├── Apply power ramp (0V to 1.8V in 1ms)
├── Monitor reset pin: must be asserted until VDD > 1.62V
├── Verify internal reset sequence completes
├── Verify oscillator starts and PLL locks
├── Verify firmware boot from flash (or ROM)
├── Verify functional mode entry
└── Pass: Complete POR sequence within 5ms
```

### 5.2 Pacing Output Driver Test

```
Pacing output verification:
├── Enable pacing output driver
├── Measure output voltage at PACE_A and PACE_B
├── Verify output pulse: amplitude, duration, shape
├── Verify output impedance: 500Ω ±10%
├── Verify leakage when output disabled
├── Verify current limiting (10mA max)
└── Pass: All parameters within specification

Safety-critical measurement:
├── Double measurement for redundancy
├── Independent measurement channel
├── Tighter specification (±5% vs. ±10%)
└── Any failure → immediate die reject
```

### 5.3 Telemetry Link Test

```
Telemetry verification:
├── Enable telemetry transmitter
├── Verify RF output power: -30dBm ±3dB at antenna pin
├── Modulation test: verify data encoding
├── Data rate verification: target ±1%
├── Enable telemetry receiver (if full-duplex capable)
├── Verify sensitivity: <-70dBm
└── Pass: Both TX and RX meet specification
```

### 5.4 Analog Front-End Test

```
Sensing channel verification:
├── Apply known test signal to SENSE_CH1/CH2
├── Verify ADC conversion accuracy: ±1 LSB (12-bit)
├── Measure input impedance: >10MΩ
├── Verify common-mode rejection: >80dB
├── Check input protection (apply overvoltage, verify clamping)
└── Pass: All channels within specification
```

---

## 6. Wafer Map Analysis

### 6.1 Wafer Map Generation

After testing all die, a wafer map is generated showing pass/fail status:

```
Wafer Map Example (200mm wafer, ~1500 die):
┌──────────────────────────────────────────────┐
│ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
│ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
│ ○ ○ ○ ○ ○ ○ ○ ● ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
│ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
│ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
│ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
│ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
│ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
│ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
│ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
│ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
│ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
│ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
│ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
│ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
│ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
│ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
│ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
│ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
│ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │
└──────────────────────────────────────────────┘

Legend: ○ = Pass  ● = Fail (functional)  ◐ = Fail (parametric)  ●● = Fail (multiple)
```

### 6.2 Yield Calculation

```
Yield Metrics:
├── Gross yield: Pass die / Total die × 100%
├── Parametric yield: Pass parametric / Total die × 100%
├── Functional yield: Pass functional / Total die × 100%
├── Composite yield: Pass all tests / Total die × 100%
└── Repair yield: (Pass + Repaired) / Total die × 100%

Target: Composite yield >92% (after maturity ramp)
```

### 6.3 Defect Spatial Analysis

Wafer map patterns reveal systematic defects:

| Pattern | Description | Possible Cause |
|---------|-------------|----------------|
| Edge cluster | Failures concentrated at wafer edge | Edge process non-uniformity |
| Scratch line | Linear cluster of failures | Mechanical damage |
| Zone pattern | Failures in specific annular zone | CMP or etch uniformity |
| Random | Distributed failures | Random particle defects |
| Quadrant | Failures in one quadrant | Process tool issue |

---

## 7. Wafer Sort Optimization

### 7.1 Test Time Reduction

| Optimization | Test Time Reduction | Trade-off |
|-------------|-------------------|-----------|
| Parallel testing (multi-site) | 4× (4-die simultaneous) | Complex probe card |
| Pattern compression | 3800× | Slight coverage reduction |
| Adaptive testing | 30-50% | Requires baseline data |
| BIST parallel execution | 2× | More complex controller |
| Reduced pattern set | 40% | Lower fault coverage |

### 7.2 Adaptive Testing

The iPACE-CHIP uses adaptive test limits based on lot history:

```
Lot-level adaptation:
├── New lot (first wafer): Full test suite, nominal limits
├── Mature lot: Tightened limits based on baseline data
├── Known-good lot: Reduced test set (skip redundant tests)
└── Problem lot: Expanded test set, tightened limits

Die-level adaptation:
├── Based on parametric measurements: Adjust functional limits
├── Based on IDDQ: Tighten or relax subsequent tests
└── Based on position: Edge die get additional screening
```

### 7.3 Test Cost Analysis

```
Wafer Sort Cost Model:
├── Probe card: $50,000 (amortized over 500K contacts)
├── ATE time: $0.50/second (J750 rental rate)
├── Test time per die: 2.5 seconds
├── Cost per die: $1.25
├── Probe card consumables: $0.10/die
├── Operator time: $0.25/die
└── Total: $1.60/die

Production volume: 100K die/year
Annual test cost: $160,000
Target: <$2.00/die for cost competitiveness
```

---

## 8. Medical Device Wafer Sort Requirements

### 8.1 ISO 13485 Compliance

The wafer sort process must comply with ISO 13485 QMS:

- Documented test procedures for each test
- Calibration records for all measurement equipment
- Training records for all test operators
- Non-conformance handling procedures
- Lot traceability from wafer to packaged device

### 8.2 Lot Acceptance Criteria

```
Lot acceptance criteria (iPACE-CHIP):
├── Gross yield >85%
├── No systematic defect patterns (quadrant, zone)
├── IDDQ distribution within ±3σ of baseline
├── Zero parametric outliers beyond ±5σ
├── BIST pass rate >98%
├── All safety-critical functions: 100% pass
└── Engineering review required for any lot below criteria
```

### 8.3 Traceability Requirements

Every die tested at wafer sort receives:

- Unique die coordinate on wafer (row, column)
- Wafer ID and lot number
- Test timestamp and ATE serial number
- Complete test results (parametric values, not just pass/fail)
- Operator ID and test program version

---

## 9. Summary

Wafer-level testing is the critical first quality gate in iPACE-CHIP manufacturing. The multi-tiered approach combines parametric screening, structural testing through scan and BIST, and functional verification to detect defective die before costly packaging. The probe card design, test program optimization, and adaptive testing strategies balance thorough defect detection against manufacturing cost. Spatial defect analysis drives continuous process improvement, while full traceability ensures regulatory compliance for the medical device manufacturing lifecycle.

---

## References

- Johnson, B.W. *The Design and Analysis of Fault-Tolerant Digital Systems*. Addison-Wesley, 1998.
- IEC 60747-1: Semiconductor Devices — General
- JEDEC Standard JESD35-A: Procedure for the Wafer-Level Testing of Thin Die
- SEMI E10-0814: Specification for Definition and Measurement of Equipment Reliability
- ISO 13485:2016: Medical Devices — Quality Management Systems
- IEC 60601-1: General Requirements for Medical Electrical Equipment
