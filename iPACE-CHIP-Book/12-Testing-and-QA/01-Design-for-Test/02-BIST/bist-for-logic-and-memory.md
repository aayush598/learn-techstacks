# BIST for Logic and Memory

## Overview

Built-In Self-Test (BIST) is a DFT methodology that embeds test generation and response analysis hardware directly on the iPACE-CHIP silicon. Unlike external ATE-based testing, BIST enables in-field self-diagnosis, reduces production test cost, and provides autonomous health monitoring — capabilities essential for an implantable medical device that must operate reliably for 10+ years without physical access.

The iPACE-CHIP employs two distinct BIST architectures: Logic BIST (LBIST) for testing random logic blocks and Memory BIST (MBIST) for testing embedded SRAM arrays. Together, these complement scan-based external testing to achieve the comprehensive fault coverage demanded by ISO 14971 risk management.

---

## 1. Logic BIST (LBIST)

### 1.1 Architecture Overview

The iPACE-CHIP LBIST architecture consists of three core components:

```
┌─────────────────────────────────────────────────┐
│                  LBIST Controller                 │
│                                                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐   │
│  │   PRPG   │───►│ Scan     │───►│   SRSG   │   │
│  │(LFSR)    │    │ Chains   │    │(MISR)    │   │
│  └────┬─────┘    └──────────┘    └────┬─────┘   │
│       │                               │          │
│       │    ┌──────────────────┐       │          │
│       └───►│ Control Logic    │───────┘          │
│            │ (FSM + Counter)  │                  │
│            └──────────────────┘                  │
└─────────────────────────────────────────────────┘
```

**PRPG (Pseudo-Random Pattern Generator):**
- Linear Feedback Shift Register (LFSR) polynomial: x^32 + x^7 + x^5 + x^3 + x^2 + 1
- 32-bit LFSR generates pseudo-random patterns
- Seed programmable through JTAG/TAP controller
- Maximum sequence length: 2^32 - 1 unique patterns per seed

**SRSG (Signature Response Signature Generator):**
- Multiple-Input Signature Register (MISR) for output compaction
- Polynomial: x^32 + x^28 + x^19 + x + 1
- 32-bit signature for each scan chain output group
- Gold signature comparison for pass/fail determination

**Control FSM:**
- States: IDLE → SHIFT → CAPTURE → SHIFT → ... → SIGNATURE_CHECK → DONE
- Configurable shift count per test session
- Supports warm-up shifting (discard initial patterns)

### 1.2 LBIST for iPACE-CHIP Logic Blocks

The LBIST covers the following logic domains:

| Block | LBIST Coverage Target | Rationale |
|-------|----------------------|-----------|
| Digital controller FSM | 95% stuck-at | Safety-critical state machine |
| Telemetry encoder/decoder | 90% stuck-at | Communication reliability |
| Clock management unit | 95% stuck-at | Clock failure = device failure |
| Watchdog timer | 95% stuck-at | Safety watchdog |
| Lead-on-chip interface | 90% stuck-at | Patient interface |
| Interrupt controller | 85% stuck-at | System coordination |
| Temperature sensor interface | 85% stuck-at | Safety monitoring |

### 1.3 LBIST Operation Modes

**Production LBIST Mode:**
- Runs during wafer sort and final test
- Maximum test coverage with all seeds
- Full signature verification
- Controlled frequency and voltage

**In-Field LBIST Mode:**
- Activated by firmware command during device self-test
- Reduced pattern count for faster execution
- Compromised signature threshold (allows ±1 bit for aging-related degradation)
- Must complete within watchdog timeout window

**Periodic Self-Test Mode:**
- Scheduled during recharge cycles (for rechargeable variant)
- Subset of critical paths tested
- Background operation during low-priority tasks
- Results stored in non-volatile status register

### 1.4 LBIST Pattern Count Optimization

For the iPACE-CHIP, LBIST pattern count is optimized through fault simulation:

```
Seed 1:  Coverage = 78.3% (1M patterns)
Seed 2:  Coverage = 84.1% (1M patterns, cum.)
Seed 3:  Coverage = 87.6% (1M patterns, cum.)
Seed 5:  Coverage = 90.2% (1M patterns, cum.)
Seed 8:  Coverage = 91.8% (1M patterns, cum.)
Seed 12: Coverage = 92.7% (1M patterns, cum.)
Seed 16: Coverage = 93.1% (1M patterns, cum.)
──────────────────────────────────────────────
Diminishing returns beyond 12 seeds
Production LBIST: 12 seeds × 1M patterns = 12M patterns
In-field LBIST: 3 seeds × 1M patterns = 3M patterns
```

### 1.5 Fault Coverage Gap Analysis

LBIST achieves 93% stuck-at coverage on average, leaving a 7% gap vs. the 99%+ target. This gap is addressed by:

- **Scan-based ATPG:** Targeted patterns for remaining untestable faults
- **Functional patterns:** Deterministic patterns for complex protocol sequences
- **IDDQ testing:** Quiescent current measurement for bridging faults
- **X-masking:** Reduces unknown contamination that reduces effective coverage

---

## 2. Memory BIST (MBIST)

### 2.1 iPACE-CHIP Embedded Memory Inventory

| Memory Block | Type | Size | Width | Criticality |
|-------------|------|------|-------|-------------|
| Register file (RF) | SRAM | 512×32 | 32-bit | High |
| Arrhythmia buffer | SRAM | 2048×16 | 16-bit | Critical |
| Telemetry FIFO | SRAM | 256×8 | 8-bit | Medium |
| ADC sample buffer | SRAM | 1024×12 | 12-bit | High |
| Firmware code cache | SRAM | 4096×32 | 32-bit | High |
| Lookup table (LUT) | ROM | 256×16 | 16-bit | Medium |

### 2.2 March Test Algorithms

The MBIST implements standard March test algorithms, selected based on fault coverage requirements:

**March C- (31n complexity):**
```
{⇕(w0); ↑(r0,w1); ↑(r1,w0); ↓(r0,w1); ↓(r1,w0); ⇕(r0)}
```
- Detects: SA0, SA1, TF, AF, CF, some linked faults
- Coverage: ~97% of simple faults
- Used for: Telemetry FIFO, LUT

**March G (59n complexity):**
```
{⇕(w0); ↑(r0,w1,r1); ↑(r1,w0,r0); ↓(r0,w1,r1); ↓(r1,w0,r0); ⇕(r0,w1); ⇕(r1,w0); ⇕(r0)}
```
- Detects: All March C- faults plus coupling, address decoder faults
- Coverage: ~99% of static faults
- Used for: Register file, ADC buffer

**March RAW (74n complexity):**
```
Extended March G with read-after-write disturbance checks
```
- Detects: Read disturb faults, write disturb faults
- Coverage: >99.5% including dynamic faults
- Used for: Arrhythmia buffer (critical), firmware code cache

### 2.3 MBIST Controller Architecture

```
┌────────────────────────────────────────────────────────┐
│                    MBIST Controller                      │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Algorithm     │  │ Address      │  │ Data         │  │
│  │ FSM           │  │ Generator    │  │ Generator    │  │
│  │ (March steps) │  │ (Up/Down)    │  │ (w0/w1)      │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                  │           │
│         └─────────────────┼──────────────────┘           │
│                           │                              │
│  ┌────────────────────────┼────────────────────────┐    │
│  │              Memory Interface                    │    │
│  │   ADDR ◄──────────────┤                         │    │
│  │   DATA_W ◄────────────┤                         │    │
│  │   DATA_R ────────────►│                         │    │
│  │   WEN ◄───────────────┤                         │    │
│  │   CLK ◄───────────────┤                         │    │
│  └─────────────────────────────────────────────────┘    │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Response Analyzer                                   │   │
│  │  • Expected data comparator                        │   │
│  │  • Fail address capture                            │   │
│  │  • Fail data capture                               │   │
│  │  • Multiple fail accumulation register             │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────┘
```

### 2.4 MBIST Repair Strategy (Redundancy Analysis)

The iPACE-CHIP SRAMs include redundant rows and columns for post-manufacturing repair:

```
Redundancy Resources per Memory:
┌──────────────────┬──────────┬──────────┬───────────┐
│ Memory           │ Redundant│ Redundant│ Max Repair │
│                  │ Rows     │ Columns  │ Rate      │
├──────────────────┼──────────┼──────────┼───────────┤
│ Register file    │ 4        │ 2        │ ~2.0%     │
│ Arrhythmia buffer│ 8        │ 4        │ ~1.5%     │
│ Telemetry FIFO   │ 2        │ 1        │ ~2.3%     │
│ ADC sample buffer│ 4        │ 2        │ ~1.5%     │
│ Firmware cache   │ 16       │ 8        │ ~1.5%     │
└──────────────────┴──────────┴──────────┴───────────┘
```

**Repair Flow:**
1. Run full March test on all memories
2. Capture fail addresses and expected/actual data
3. Run redundancy analysis algorithm (graph-based row/column allocation)
4. Determine repair solution (fuse-blow coordinates)
5. If repairable: program fuses and re-test
6. If not repairable: mark die as defective

### 2.5 MBIST Timing Constraints

Memory BIST must operate within the power and timing envelope of the iPACE-CHIP:

- **MBIST clock frequency:** Max 25 MHz (limited by memory access time + overhead)
- **MBIST power budget:** <500 μW during test (vs. 180 μW functional)
- **MBIST execution time:** <50 ms for all memories (production test time constraint)
- **MBIST voltage:** 1.62V - 1.98V (nominal 1.8V ±10%)

---

## 3. BIST Integration

### 3.1 BIST Controller Shared Resources

The iPACE-CHIP shares certain DFT infrastructure between LBIST and MBIST:

```
                    JTAG/TAP Controller
                           │
                           │ BIST trigger, status readback
                           ▼
                    ┌──────────────┐
                    │  BIST Arbiter │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │                         │
       ┌──────┴──────┐          ┌──────┴──────┐
       │  LBIST FSM  │          │  MBIST FSM  │
       │  Controller │          │  Controller │
       └─────────────┘          └─────────────┘
```

**Arbitration rules:**
- LBIST and MBIST cannot run simultaneously (power constraint)
- MBIST runs first (memories initialized before logic test)
- LBIST can capture memory read outputs during shift (opportunistic)

### 3.2 BIST Result Reporting

Test results are stored in a status register accessible via JTAG:

```
BIST Status Register (32-bit):
┌─────┬─────┬─────┬─────┬──────────────┬───────────┐
│[31] │[30] │[29] │[28] │  [27:16]     │ [15:0]    │
│ LB  │ MB  │ MB  │ MB  │ Fail Address │ Fail Data │
│ Pass│ RF  │ ARR │ ADC │ (12 bits)    │ (16 bits) │
│     │ Fail│ Fail│ Fail│              │           │
└─────┴─────┴─────┴─────┴──────────────┴───────────┘

Additional bits:
[15] Telemetry FIFO MBIST fail
[14] Firmware cache MBIST fail
[13:8] Reserved
[7:0] BIST iteration count (seed index for LBIST)
```

### 3.3 BIST and Functional Safety

For the iPACE-CHIP medical device application, BIST serves dual roles:

**Production Testing:**
- Complementary coverage to scan ATPG
- Memory-specific fault detection
- In-system test capability during incoming inspection

**In-Field Health Monitoring:**
- Periodic self-test during device operation
- Aging-related degradation detection
- Pre-failure warning before critical fault develops
- Logged results for physician download via telemetry

---

## 4. Advanced BIST Techniques

### 4.1 Logic BIST with Weighted Random Patterns

Pure LFSR-generated patterns have biased toggle probabilities. For the iPACE-CHIP, weighted random patterns improve coverage of hard-to-detect faults:

**Weight assignment by fault class:**

| Weight Pattern | Target Faults | Coverage Improvement |
|---------------|---------------|---------------------|
| Balanced (50%) | Random-pattern testable | Baseline |
| High-0 (80% 0) | Control signal stuck-at-1 | +2.3% |
| High-1 (80% 1) | Control signal stuck-at-0 | +1.8% |
| Alternating | Toggle-dependent faults | +0.7% |

### 4.2 X-Masking for Unknown Handling

Unknown values (X) in scan chain outputs corrupt the MISR signature. The iPACE-CHIP employs:

- **X-blocking logic:** AND gates mask X-affected scan chain outputs before MISR
- **X-tolerant MISR:** Modified MISR that tolerates up to 3 unknown values per capture
- **Deterministic X-masking:** ATPG identifies X sources and generates mask patterns

### 4.3 Micro-BIST for Block-Level Testing

The iPACE-CHIP implements micro-BIST controllers at the IP block level:

- Each memory has its own MBIST controller
- LBIST is segmented by clock domain
- Individual blocks can be tested independently
- Enables selective in-field testing of critical blocks only

---

## 5. Production BIST Flow

### 5.1 Wafer-Level BIST

During wafer sort, BIST follows this sequence:

```
1. Probe contact verification
   └── Check all test pads for continuity

2. IDDQ measurement (pre-BIST)
   └── Baseline quiescent current

3. MBIST execution
   ├── Run March RAW on all memories
   ├── Capture fail information
   └── Run redundancy analysis

4. Memory repair (if needed)
   └── Laser fuse programming

5. LBIST execution
   ├── 12 seeds × 1M patterns
   └── Signature comparison

6. IDDQ measurement (post-BIST)
   └── Compare with pre-BIST baseline

7. Pass/Fail determination
   └── Coordinate marking for defective die
```

### 5.2 Final Test BIST

During packaged device final test, BIST is expanded:

```
1. All MBIST tests at 3 voltage/temperature corners
   ├── Nominal: 1.8V, 25°C
   ├── Fast: 2.0V, -40°C
   └── Slow: 1.6V, 85°C

2. All LBIST tests at 3 corners
   └── Same conditions as MBIST

3. Additional MBIST with elevated voltage
   └── 2.1V for early-life defect screening (ELDS)

4. BIST timing margin characterization
   └── Sweep frequency to find BIST pass/fail boundary
```

---

## 6. BIST for Medical Device Compliance

### 6.1 IEC 62304 Software Life Cycle

The iPACE-CHIP BIST firmware is developed per IEC 62304 Class C (capable of contributing to a hazardous situation):

- BIST firmware has formal requirements specification
- Code coverage target: 100% branch coverage
- Static analysis with zero critical/MISRA violations
- Full regression testing after any modification

### 6.2 Fault Detection Coverage Requirements

Per ISO 14971 risk analysis:

| Hazard | Required Detection Method | BIST Role |
|--------|--------------------------|-----------|
| Loss of pacing | LBIST + MBIST on RF | Primary detection |
| Incorrect arrhythmia detection | MBIST on arrhythmia buffer | Primary detection |
| Loss of telemetry | LBIST on encoder/decoder | Complementary |
| Power management failure | LBIST + functional test | Complementary |
| Clock system failure | LBIST on clock MUX logic | Primary detection |

### 6.3 In-Field Self-Test Protocol

The iPACE-CHIP implements a hierarchical in-field self-test:

```
Level 1: Quick health check (10 ms)
  ├── Verify BIST golden signature register
  ├── Check memory ECC status
  └── Compare IDDQ with stored baseline

Level 2: Periodic self-test (500 ms)
  ├── Run 3-seed LBIST on critical paths
  ├── Run March C- on arrhythmia buffer
  └── Verify all clock monitors

Level 3: Comprehensive self-test (50 ms, annual)
  ├── Full MBIST on all memories
  ├── Full LBIST (all seeds)
  ├── IDDQ measurement and comparison
  └── Results stored for physician retrieval
```

---

## 7. BIST Debug and Diagnostics

### 7.1 BIST Failure Analysis Flow

When BIST fails during production:

```
1. Capture BIST failure data
   ├── LBIST: failing seed index, scan chain number
   ├── MBIST: failing memory, fail address, fail data
   └── Store in on-chip debug register

2. Correlate with scan ATPG results
   ├── Run external ATPG on failing die
   ├── Compare fault locations
   └── Determine if defect is random or systematic

3. Physical failure analysis (PFA) preparation
   ├── Mark failing die for cross-sectioning
   ├── Identify potential defect site
   └── Guide sample preparation

4. Root cause investigation
   ├── Defect type classification
   ├── Process window analysis
   └── Corrective action determination
```

### 7.2 BIST Diagnostic Resolution

The iPACE-CHIP MBIST provides diagnostic resolution to the failing:

- **Word line level:** Which row contains the defect
- **Bit line level:** Which column contains the defect
- **Cell level:** Which specific bit in the failing word
- **Fail pattern:** Stuck-at, transition, coupling, or address decoder fault type

---

## 8. Summary

BIST for logic and memory is an indispensable component of the iPACE-CHIP test strategy. LBIST provides at-speed pseudo-random testing with >93% stuck-at coverage, complemented by targeted scan ATPG to reach the >99% coverage required for medical devices. MBIST implements industry-standard March algorithms with on-chip redundancy analysis and repair, achieving >99.5% fault coverage for all embedded memories. Together with in-field self-test capabilities, BIST ensures the iPACE-CHIP maintains its zero-defect quality posture throughout its operational life in the patient.

---

## References

- Bardell, P.H., McAnney, W.H., & Savir, J. *Built-In Test for VLSI: Pseudo-Random Techniques*. Wiley, 1987.
- van de Goor, A.J. *Testing Semiconductor Memories: Theory and Practice*. Comtex Publishing, 1991.
- IEC 62304:2006+A1:2015: Medical Device Software — Software Life Cycle Processes
- ISO 14971:2019: Medical Devices — Application of Risk Management to Medical Devices
- IEEE 1500-2005: Standard for Embedded Core Test
- Bushnell, M.L. & Agrawal, V.D. *Essentials of Electronic Testing*. Springer, 2000.
